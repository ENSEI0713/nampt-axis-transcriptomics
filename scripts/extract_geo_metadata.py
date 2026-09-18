#!/usr/bin/env python3
"""Extract GEO series-matrix metadata for selected candidate series.

Series-matrix files expose the key sample metadata near the top of the file and
can be stopped before the expression table begins. That is much faster than
reading full family SOFT files for large transcriptomic studies.
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
    "GSE270703",
    "GSE189298",
    "GSE333506",
    "GSE328810",
    "GSE32575",
    "GSE272133",
    "GSE272137",
    "GSE294150",
    "GSE302599",
    "GSE329809",
    "GSE282850",
    "GSE247455",
    "GSE292357",
    "GSE292517",
    "GSE287158",
    "GSE282291",
    "GSE323980",
]


def geo_series_url(acc: str) -> str:
    digits = re.search(r"GSE(\d+)", acc).group(1)  # type: ignore[union-attr]
    prefix = digits[:-3]
    return f"https://ftp.ncbi.nlm.nih.gov/geo/series/GSE{prefix}nnn/{acc}/matrix/{acc}_series_matrix.txt.gz"


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def infer_category(series: dict[str, str], samples: list[dict[str, list[str]]]) -> str:
    text = " ".join(
        [series.get("title", ""), series.get("summary", ""), series.get("overall_design", "")]
        + [" ".join(v for values in sample.values() for v in values) for sample in samples[:30]]
    ).lower()
    human = "homo sapiens" in text or "human" in text
    mouse_or_rat = any(term in text for term in ["mus musculus", "mouse", "mice", "rattus", "rat "])
    exercise = any(term in text for term in ["exercise", "training", "endurance", "resistance", "sprint", "physical activity", "mice"])
    obesity = any(term in text for term in ["obesity", "obese", "bmi", "weight loss", "bariatric", "insulin resistance"])
    tissue = any(term in text for term in ["skeletal muscle", "vastus", "adipose", "monocyte", "pbmc", "blood", "plasma", "serum"])
    disease_confounded = any(term in text for term in ["cancer", "dialysis", "peripheral artery disease", "hyperparathyroidism", "leukemia"])
    if human and tissue and (exercise or obesity) and not disease_confounded:
        return "main_candidate"
    if human and tissue and (exercise or obesity):
        return "supplement_confounded"
    if mouse_or_rat and (exercise or obesity):
        return "mechanistic_animal_only"
    return "exclude_or_background"


def split_quoted_fields(line: str) -> list[str]:
    return [field.strip().strip('"') for field in line.rstrip("\n").split("\t")[1:]]


def parse_soft(acc: str) -> tuple[dict[str, str], list[dict[str, list[str]]]]:
    url = geo_series_url(acc)
    series: dict[str, str] = {"accession": acc, "url": url}
    samples: list[dict[str, list[str]]] = []
    sample_columns: list[dict[str, list[str]]] = []

    with urllib.request.urlopen(url, timeout=60) as response:
        with gzip.GzipFile(fileobj=response) as gz:
            for raw_line in gz:
                line = raw_line.decode("utf-8", errors="replace").rstrip("\n")
                if line.startswith("!series_matrix_table_begin"):
                    continue
                if line.startswith("!Series_title"):
                    series["title"] = clean(line.split("\t", 1)[1].strip('"') if "\t" in line else line.split("=", 1)[1])
                elif line.startswith("!Series_summary"):
                    fields = split_quoted_fields(line)
                    series["summary"] = clean(series.get("summary", "") + " " + " ".join(fields))
                elif line.startswith("!Series_overall_design"):
                    fields = split_quoted_fields(line)
                    series["overall_design"] = clean(series.get("overall_design", "") + " " + " ".join(fields))
                elif line.startswith("!Series_pubmed_id"):
                    fields = split_quoted_fields(line)
                    series["pubmed_id"] = ";".join(fields)
                elif line.startswith("!Series_supplementary_file"):
                    fields = split_quoted_fields(line)
                    series["supplementary_files"] = clean(series.get("supplementary_files", "") + ";" + ";".join(fields))
                elif line.startswith("!Sample_") and "\t" in line:
                    key = line.split("\t", 1)[0].replace("!Sample_", "").strip()
                    if key in {"geo_accession", "title", "source_name_ch1", "organism_ch1", "characteristics_ch1", "treatment_protocol_ch1", "growth_protocol_ch1", "extract_protocol_ch1", "molecule_ch1", "data_processing"}:
                        fields = split_quoted_fields(line)
                        while len(sample_columns) < len(fields):
                            sample_columns.append({})
                        for idx, value in enumerate(fields):
                            sample_columns[idx].setdefault(key, []).append(value)

    samples = sample_columns

    return series, samples


def summarize_samples(samples: list[dict[str, list[str]]]) -> dict[str, str]:
    sample_texts = []
    organisms = set()
    sources = set()
    characteristics = []
    for sample in samples:
        title = "; ".join(sample.get("title", []))
        source = "; ".join(sample.get("source_name_ch1", []))
        organism = "; ".join(sample.get("organism_ch1", []))
        char = "; ".join(sample.get("characteristics_ch1", []))
        if organism:
            organisms.add(organism)
        if source:
            sources.add(source)
        if char:
            characteristics.append(char)
        if len(sample_texts) < 8:
            sample_texts.append(clean(" | ".join([title, source, organism, char])))
    return {
        "sample_count_soft": str(len(samples)),
        "organisms_soft": "; ".join(sorted(organisms))[:500],
        "sources_soft": "; ".join(sorted(sources))[:500],
        "sample_characteristics_excerpt": " || ".join(characteristics[:8])[:1500],
        "sample_titles_excerpt": " || ".join(sample_texts)[:1500],
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for acc in ACCESSIONS:
        print(f"Extracting {acc}")
        try:
            series, samples = parse_soft(acc)
            row = {**series, **summarize_samples(samples)}
            row["analysis_category"] = infer_category(series, samples)
            row["geo_page"] = f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={acc}"
            rows.append(row)
        except Exception as exc:  # noqa: BLE001
            rows.append({"accession": acc, "error": str(exc), "analysis_category": "needs_manual_check"})
        time.sleep(0.4)

    fieldnames = [
        "analysis_category",
        "accession",
        "title",
        "summary",
        "overall_design",
        "pubmed_id",
        "sample_count_soft",
        "organisms_soft",
        "sources_soft",
        "sample_characteristics_excerpt",
        "sample_titles_excerpt",
        "supplementary_files",
        "geo_page",
        "url",
        "error",
    ]
    with (OUT_DIR / "selected_geo_metadata.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            for field in fieldnames:
                row.setdefault(field, "")
            writer.writerow(row)
    print(f"Wrote {len(rows)} rows to {OUT_DIR / 'selected_geo_metadata.csv'}")


if __name__ == "__main__":
    main()
