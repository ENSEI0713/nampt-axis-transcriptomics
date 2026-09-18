#!/usr/bin/env python3
"""Build a per-sample metadata table from GEO series-matrix files.

The existing audit stores one row per GEO series. This script expands the same
public records into one row per sample, which makes downstream scoring and
within-study contrasts auditable.
"""

from __future__ import annotations

import csv
import gzip
import re
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data_audit" / "outputs"

ACCESSIONS = [
    "GSE312393",
    "GSE318937",
    "GSE305038",
    "GSE292369",
    "GSE32575",
    "GSE272133",
    "GSE294150",
    "GSE282850",
]

SAMPLE_KEYS = {
    "geo_accession",
    "title",
    "source_name_ch1",
    "organism_ch1",
    "characteristics_ch1",
    "treatment_protocol_ch1",
    "growth_protocol_ch1",
    "extract_protocol_ch1",
    "molecule_ch1",
}


def geo_series_url(acc: str) -> str:
    digits = re.search(r"GSE(\d+)", acc).group(1)  # type: ignore[union-attr]
    return f"https://ftp.ncbi.nlm.nih.gov/geo/series/GSE{digits[:-3]}nnn/{acc}/matrix/{acc}_series_matrix.txt.gz"


def split_quoted_fields(line: str) -> list[str]:
    return [field.strip().strip('"') for field in line.rstrip("\n").split("\t")[1:]]


def clean_key(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def parse_characteristics(values: list[str]) -> dict[str, str]:
    parsed: dict[str, list[str]] = {}
    for value in values:
        if ":" not in value:
            continue
        key, raw = value.split(":", 1)
        key = clean_key(key)
        raw = raw.strip()
        if key and raw:
            parsed.setdefault(key, []).append(raw)
    return {key: " | ".join(dict.fromkeys(items)) for key, items in parsed.items()}


def infer_condition(acc: str, title: str, kv: dict[str, str]) -> dict[str, str]:
    text = title.lower()
    out = {
        "condition": "",
        "timepoint": "",
        "intervention": "",
        "participant_id": "",
        "cohort": "",
        "exercise_type": "",
        "nutrition_or_treatment": "",
    }

    if acc == "GSE312393":
        out["intervention"] = "exercise"
        if "24 hours post-exercise" in text:
            out["condition"] = "24h_exercise"
            out["timepoint"] = "24h_post"
        elif "control" in text:
            out["condition"] = "control"
            out["timepoint"] = "baseline"
        elif "post-6 weeks" in text:
            out["condition"] = "post_training"
            out["timepoint"] = "post_6weeks"
        elif "pre-exercise training" in text:
            out["condition"] = "pre_training"
            out["timepoint"] = "pre_training"
        match = re.search(r"patient\s+(\d+)", text)
        if match:
            out["participant_id"] = f"P{match.group(1)}"

    elif acc == "GSE272133":
        match = re.search(r"(OB|T2D)_Participant_(\d+)_w(\d+)", title, re.I)
        if match:
            out["cohort"] = match.group(1).upper()
            out["participant_id"] = f"{out['cohort']}_{match.group(2)}"
            out["timepoint"] = f"w{match.group(3)}"
            out["condition"] = f"{out['cohort']}_{out['timepoint']}"
        out["intervention"] = "metabolic_surgery"

    elif acc == "GSE292369":
        out["intervention"] = "exercise_recovery"
        out["condition"] = "exercised" if "exercised" in text else "rest"
        out["timepoint"] = "post" if "exercised" in text else "pre"
        out["nutrition_or_treatment"] = "ketone_ester" if "ketone" in text else "placebo"
        match = re.search(r"\bP(\d+)\b", title)
        if match:
            out["participant_id"] = f"P{match.group(1)}"

    elif acc == "GSE305038":
        treatment = kv.get("treatment", "").lower()
        out["intervention"] = "exercise_after_activity_or_inactivity"
        if "inactive" in treatment:
            out["cohort"] = "inactive"
        elif "active" in treatment:
            out["cohort"] = "active"
        if "post" in treatment:
            out["timepoint"] = "post"
        elif "pre" in treatment:
            out["timepoint"] = "pre"
        match = re.search(r"I(\d+)", title, re.I)
        if match:
            out["participant_id"] = f"I{match.group(1)}"
        if out["cohort"] and out["timepoint"]:
            out["condition"] = f"{out['cohort']}_{out['timepoint']}"

    elif acc == "GSE32575":
        out["intervention"] = "bariatric_surgery"
        if "lean" in text:
            out["condition"] = "lean"
            match = re.search(r"(?:rep|pool)(\d+)", text)
            if match:
                out["participant_id"] = f"C{match.group(1)}"
        elif "obese_before" in text:
            out["condition"] = "obese_before"
        elif "obese_after" in text:
            out["condition"] = "obese_after"
        match = re.search(r"rep(\d+)", text)
        if match and out["condition"] != "lean":
            out["participant_id"] = f"GB{match.group(1)}"

    elif acc == "GSE318937":
        out["intervention"] = "acute_exercise_with_supplement"
        out["exercise_type"] = kv.get("type_of_exercise", "")
        out["timepoint"] = kv.get("time_of_the_biopsy_with_respect_to_the_end_of_exercise", "")
        out["nutrition_or_treatment"] = kv.get("treatment", "")
        out["participant_id"] = kv.get("subject_id", "")
        pieces = [out["exercise_type"], out["nutrition_or_treatment"], out["timepoint"]]
        out["condition"] = "_".join(piece for piece in pieces if piece)

    elif acc == "GSE282850":
        out["intervention"] = "human_muscle_cell_perturbation"
        if "undiff" in text:
            out["condition"] = "undifferentiated"
        elif "palmitate" in text:
            out["condition"] = "palmitate"
        elif "aicar" in text:
            out["condition"] = "aicar"
        elif "diff" in text:
            out["condition"] = "differentiated"
        match = re.search(r"rep\s*(\d+)", text)
        if match:
            out["participant_id"] = f"rep{match.group(1)}"

    return out


def parse_series(acc: str) -> tuple[dict[str, str], list[dict[str, str]]]:
    series = {"accession": acc, "series_matrix_url": geo_series_url(acc), "platform_id": ""}
    samples: list[dict[str, list[str]]] = []

    with urllib.request.urlopen(series["series_matrix_url"], timeout=60) as response:
        with gzip.GzipFile(fileobj=response) as gz:
            for raw in gz:
                line = raw.decode("utf-8", errors="replace").rstrip("\n")
                if line.startswith("!series_matrix_table_begin"):
                    break
                if line.startswith("!Series_platform_id"):
                    fields = split_quoted_fields(line)
                    series["platform_id"] = ";".join(fields)
                if not line.startswith("!Sample_") or "\t" not in line:
                    continue
                key = line.split("\t", 1)[0].replace("!Sample_", "").strip()
                if key not in SAMPLE_KEYS:
                    continue
                fields = split_quoted_fields(line)
                while len(samples) < len(fields):
                    samples.append({})
                for idx, value in enumerate(fields):
                    samples[idx].setdefault(key, []).append(value)

    rows: list[dict[str, str]] = []
    for idx, sample in enumerate(samples, start=1):
        characteristics = sample.get("characteristics_ch1", [])
        kv = parse_characteristics(characteristics)
        title = " | ".join(sample.get("title", []))
        row = {
            **series,
            "series_sample_order": str(idx),
            "geo_accession": " | ".join(sample.get("geo_accession", [])),
            "sample_title": title,
            "source_name": " | ".join(sample.get("source_name_ch1", [])),
            "organism": " | ".join(sample.get("organism_ch1", [])),
            "characteristics": "; ".join(characteristics),
        }
        row.update(kv)
        row.update(infer_condition(acc, title, kv))
        rows.append(row)
    return series, rows


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    all_rows: list[dict[str, str]] = []
    for acc in ACCESSIONS:
        print(f"Extracting per-sample metadata for {acc}")
        try:
            _, rows = parse_series(acc)
            all_rows.extend(rows)
        except Exception as exc:  # noqa: BLE001 - preserve partial audit results
            all_rows.append({"accession": acc, "error": str(exc)})
        time.sleep(0.4)

    fieldnames = sorted({key for row in all_rows for key in row})
    preferred = [
        "accession",
        "platform_id",
        "series_sample_order",
        "geo_accession",
        "sample_title",
        "condition",
        "timepoint",
        "intervention",
        "cohort",
        "participant_id",
        "exercise_type",
        "nutrition_or_treatment",
        "source_name",
        "organism",
        "characteristics",
        "series_matrix_url",
        "error",
    ]
    fieldnames = [field for field in preferred if field in fieldnames] + [field for field in fieldnames if field not in preferred]
    out_csv = OUT_DIR / "geo_sample_metadata_long.csv"
    with out_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in all_rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})
    print(f"Wrote {len(all_rows)} sample rows to {out_csv}")


if __name__ == "__main__":
    main()
