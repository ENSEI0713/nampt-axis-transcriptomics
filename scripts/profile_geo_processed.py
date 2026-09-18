#!/usr/bin/env python3
"""Profile downloaded GEO processed matrices for NAMPT-axis analysis readiness."""

from __future__ import annotations

import csv
import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DOWNLOAD_DIR = ROOT / "data_audit" / "downloads" / "geo_processed"
OUT_DIR = ROOT / "data_audit" / "outputs"
GENE_SET = OUT_DIR / "NAMPT_axis_gene_set_v1.csv"


ENSEMBL_RE = re.compile(r"^ENSG\d+(?:\.\d+)?$")
PROBE_RE = re.compile(r"^(ILMN_|[0-9]+_at|[A-Z]+_[0-9])")


def read_axis_genes() -> set[str]:
    with GENE_SET.open(newline="", encoding="utf-8") as handle:
        return {row["gene_symbol"].upper() for row in csv.DictReader(handle)}


def read_matrix(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".xlsx":
        return pd.read_excel(path, sheet_name=0)
    sep = "," if path.name.endswith(".csv.gz") or path.suffix.lower() == ".csv" else "\t"
    try:
        return pd.read_csv(path, sep=sep, compression="infer", low_memory=False)
    except pd.errors.ParserError:
        # Some GEO files have an unlabeled first identifier column.
        return pd.read_csv(path, sep=sep, compression="infer", header=None, low_memory=False)


def normalize_symbol(value: object) -> str:
    text = str(value).strip().strip('"')
    if "|" in text:
        text = text.rsplit("|", 1)[-1]
    return text.upper()


def classify_values(values: list[object]) -> str:
    sample = [str(v).strip().strip('"') for v in values if str(v).strip() and str(v).lower() != "nan"][:200]
    if not sample:
        return "empty_or_unknown"
    ensembl = sum(bool(ENSEMBL_RE.match(v.split("|", 1)[0])) for v in sample)
    pipe_symbol = sum("|" in v and len(v.rsplit("|", 1)[-1]) > 0 for v in sample)
    probe = sum(bool(PROBE_RE.match(v)) for v in sample)
    likely_symbol = sum(bool(re.match(r"^[A-Z][A-Z0-9.-]{1,15}$", v)) for v in sample)
    if pipe_symbol >= max(5, len(sample) * 0.25):
        return "ensembl_pipe_symbol"
    if ensembl >= max(5, len(sample) * 0.5):
        return "ensembl_id"
    if probe >= max(5, len(sample) * 0.5):
        return "array_probe_id"
    if likely_symbol >= max(5, len(sample) * 0.5):
        return "gene_symbol"
    return "mixed_or_unknown"


def candidate_symbol_columns(df: pd.DataFrame, axis_genes: set[str]) -> list[dict[str, object]]:
    candidates = []
    for column in df.columns[:12]:
        values = df[column].dropna().head(1000).tolist()
        symbols = {normalize_symbol(v) for v in values}
        overlap = sorted(symbols & axis_genes)
        dtype = classify_values(values)
        candidates.append(
            {
                "column": str(column),
                "id_type": dtype,
                "axis_overlap_count": len(overlap),
                "axis_overlap_genes": ";".join(overlap[:30]),
            }
        )
    return sorted(candidates, key=lambda x: int(x["axis_overlap_count"]), reverse=True)


def detect_column_gene_orientation(df: pd.DataFrame, axis_genes: set[str]) -> tuple[int, str]:
    cols = {normalize_symbol(c) for c in df.columns}
    overlap = sorted(cols & axis_genes)
    return len(overlap), ";".join(overlap[:30])


def accession_from_path(path: Path) -> str:
    try:
        return path.relative_to(DOWNLOAD_DIR).parts[0]
    except ValueError:
        return ""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    axis_genes = read_axis_genes()
    rows = []
    for path in sorted(DOWNLOAD_DIR.rglob("*")):
        if not path.is_file():
            continue
        print(f"Profiling {path}")
        row = {
            "accession": accession_from_path(path),
            "file": str(path.relative_to(ROOT)),
            "rows": "",
            "columns": "",
            "orientation_hint": "",
            "primary_id_type": "",
            "primary_id_column": "",
            "axis_overlap_count": 0,
            "axis_overlap_genes": "",
            "needs_mapping": "",
            "notes": "",
            "status": "ok",
            "error": "",
        }
        try:
            df = read_matrix(path)
            row["rows"] = len(df)
            row["columns"] = len(df.columns)
            col_overlap_count, col_overlap_genes = detect_column_gene_orientation(df, axis_genes)
            candidates = candidate_symbol_columns(df, axis_genes)
            best = candidates[0] if candidates else {"column": "", "id_type": "", "axis_overlap_count": 0, "axis_overlap_genes": ""}

            if col_overlap_count > int(best["axis_overlap_count"]):
                row["orientation_hint"] = "samples_as_rows_genes_as_columns"
                row["primary_id_type"] = "gene_symbol_columns"
                row["primary_id_column"] = "header"
                row["axis_overlap_count"] = col_overlap_count
                row["axis_overlap_genes"] = col_overlap_genes
                row["needs_mapping"] = "no_for_direct_symbol_subset"
            else:
                row["orientation_hint"] = "genes_as_rows_samples_as_columns"
                row["primary_id_type"] = best["id_type"]
                row["primary_id_column"] = best["column"]
                row["axis_overlap_count"] = best["axis_overlap_count"]
                row["axis_overlap_genes"] = best["axis_overlap_genes"]
                if best["id_type"] in {"ensembl_id", "array_probe_id", "mixed_or_unknown", "empty_or_unknown"}:
                    row["needs_mapping"] = "yes"
                elif best["id_type"] == "ensembl_pipe_symbol":
                    row["needs_mapping"] = "no_symbol_embedded"
                else:
                    row["needs_mapping"] = "no_for_direct_symbol_subset"

            if row["axis_overlap_count"] == 0 and row["primary_id_type"] == "ensembl_id":
                row["notes"] = "Requires Ensembl-to-symbol mapping before scoring."
            elif row["axis_overlap_count"] == 0 and row["primary_id_type"] == "array_probe_id":
                row["notes"] = "Requires platform probe annotation before scoring."
        except Exception as exc:  # noqa: BLE001 - audit should preserve failures
            row["status"] = "error"
            row["error"] = str(exc)
        rows.append(row)

    out_csv = OUT_DIR / "geo_processed_profile.csv"
    fieldnames = [
        "accession",
        "file",
        "rows",
        "columns",
        "orientation_hint",
        "primary_id_type",
        "primary_id_column",
        "axis_overlap_count",
        "axis_overlap_genes",
        "needs_mapping",
        "notes",
        "status",
        "error",
    ]
    with out_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote profile to {out_csv}")


if __name__ == "__main__":
    main()
