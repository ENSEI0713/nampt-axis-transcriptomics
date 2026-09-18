#!/usr/bin/env python3
"""Build harmonized NAMPT-axis expression subsets and first-pass scores.

The output is intentionally conservative: scores are computed within each
dataset, then contrasted within the same dataset only. This avoids treating raw
values from different platforms as directly comparable.
"""

from __future__ import annotations

import csv
import gzip
import math
import re
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DOWNLOAD_DIR = ROOT / "data_audit" / "downloads" / "geo_processed"
ANNOTATION_DIR = ROOT / "data_audit" / "downloads" / "annotations"
OUT_DIR = ROOT / "data_audit" / "outputs"
EXPR_OUT = OUT_DIR / "nampt_axis_expression"

GENE_SET_PATH = OUT_DIR / "NAMPT_axis_gene_set_v1.csv"
SAMPLE_META_PATH = OUT_DIR / "geo_sample_metadata_long.csv"

HGNC_URL = "https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt"
GPL6102_URL = "https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL6nnn/GPL6102/annot/GPL6102.annot.gz"

ENSEMBL_RE = re.compile(r"ENSG\d+(?:\.\d+)?")


def download_if_missing(url: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size > 0:
        return
    print(f"Downloading {url}")
    with urllib.request.urlopen(url, timeout=90) as response:
        path.write_bytes(response.read())


def load_axis_gene_set() -> pd.DataFrame:
    axis = pd.read_csv(GENE_SET_PATH)
    axis["gene_symbol"] = axis["gene_symbol"].str.upper()
    return axis


def load_ensembl_map() -> dict[str, str]:
    path = ANNOTATION_DIR / "hgnc_complete_set.txt"
    download_if_missing(HGNC_URL, path)
    hgnc = pd.read_csv(path, sep="\t", dtype=str).fillna("")
    mapping: dict[str, str] = {}
    for _, row in hgnc.iterrows():
        symbol = row.get("symbol", "").upper()
        ensembl = row.get("ensembl_gene_id", "")
        if symbol and ensembl:
            mapping[ensembl.split(".", 1)[0]] = symbol
    return mapping


def load_gpl6102_map() -> dict[str, str]:
    path = ANNOTATION_DIR / "GPL6102.annot.gz"
    download_if_missing(GPL6102_URL, path)
    rows: list[dict[str, str]] = []
    in_table = False
    with gzip.open(path, "rt", errors="replace") as handle:
        reader: csv.DictReader[str] | None = None
        for line in handle:
            if line.startswith("!platform_table_begin"):
                in_table = True
                header = next(handle).rstrip("\n").split("\t")
                reader = csv.DictReader(handle, fieldnames=header, delimiter="\t")
                continue
            if not in_table or reader is None:
                continue
            if line.startswith("!platform_table_end"):
                break
            row = next(csv.DictReader([line], fieldnames=reader.fieldnames, delimiter="\t"))
            rows.append(row)
    mapping = {}
    for row in rows:
        probe = row.get("ID", "").strip()
        symbol = row.get("Gene symbol", "").strip().split(" /// ", 1)[0].upper()
        if probe and symbol:
            mapping[probe] = symbol
    return mapping


def clean_ensembl(value: object) -> str:
    text = str(value).strip().strip('"')
    if "|" in text:
        text = text.split("|", 1)[0]
    match = ENSEMBL_RE.search(text)
    if not match:
        return text.split(".", 1)[0]
    return match.group(0).split(".", 1)[0]


def symbol_from_mixed_id(value: object, ensembl_map: dict[str, str]) -> str:
    text = str(value).strip().strip('"')
    if "|" in text:
        tail = text.rsplit("|", 1)[-1].strip()
        if tail:
            return tail.upper()
    if ENSEMBL_RE.search(text):
        return ensembl_map.get(clean_ensembl(text), "")
    return text.upper()


def aggregate_by_symbol(df: pd.DataFrame, id_col: str, ensembl_map: dict[str, str] | None = None) -> pd.DataFrame:
    data = df.copy()
    if ensembl_map is None:
        data["gene_symbol"] = data[id_col].astype(str).str.upper()
    else:
        data["gene_symbol"] = data[id_col].map(lambda x: symbol_from_mixed_id(x, ensembl_map))
    data = data[data["gene_symbol"].str.len() > 0]
    numeric_cols = [col for col in data.columns if col not in {id_col, "gene_symbol"}]
    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    grouped = data.groupby("gene_symbol", as_index=True)[numeric_cols].mean()
    return grouped


def maybe_log2(matrix: pd.DataFrame, transform_hint: str) -> tuple[pd.DataFrame, str]:
    values = matrix.to_numpy(dtype=float)
    finite = values[np.isfinite(values)]
    if finite.size == 0:
        return matrix, "none_empty"
    max_value = float(np.nanmax(finite))
    if transform_hint == "already_log_like":
        return matrix.astype(float), "none_already_log_like"
    if max_value > 50:
        return np.log2(matrix.astype(float) + 1), "log2_x_plus_1"
    return matrix.astype(float), "none_low_dynamic_range"


def map_by_sample_order(acc: str, expr: pd.DataFrame, meta: pd.DataFrame) -> pd.DataFrame:
    rows = meta[meta["accession"] == acc].sort_values("series_sample_order")
    if len(rows) != len(expr.columns):
        return pd.DataFrame({"sample_id": expr.columns, "original_sample_column": expr.columns})
    mapping = pd.DataFrame({
        "sample_id": rows["sample_title"].tolist(),
        "original_sample_column": expr.columns.tolist(),
    })
    return mapping


def custom_sample_metadata(dataset_id: str, columns: list[str]) -> pd.DataFrame | None:
    acc = dataset_id.split("_", 1)[0]
    if dataset_id == "GSE312393_24h_exercise":
        rows = []
        for col in columns:
            is_exercise = col.startswith("Exercise24H")
            rows.append({
                "accession": acc,
                "sample_id": col,
                "sample_title": col,
                "original_sample_column": col,
                "condition": "24h_exercise" if is_exercise else "control",
                "participant": "",
                "timepoint": "24h_post" if is_exercise else "baseline",
            })
        return pd.DataFrame(rows)

    if dataset_id == "GSE312393_6weeks_training":
        rows = []
        for col in columns:
            match = re.search(r"_(Pre|Post)P(\d+)$", col)
            phase = match.group(1).lower() if match else ""
            participant = f"P{match.group(2)}" if match else ""
            rows.append({
                "accession": acc,
                "sample_id": col,
                "sample_title": col,
                "original_sample_column": col,
                "condition": "post_training" if phase == "post" else "pre_training",
                "participant": participant,
                "timepoint": "post_6weeks" if phase == "post" else "pre_training",
            })
        return pd.DataFrame(rows)

    if dataset_id == "GSE292369_exercise_ketone_recovery":
        path = DOWNLOAD_DIR / "GSE292369" / "GSE292369_Partek_KE_recovery_Normalization_Outliers_Removed_Deseq2.txt.gz"
        sample_meta = pd.read_csv(
            path,
            sep="\t",
            compression="infer",
            usecols=["Sample name", "Subject", "Condition", "Time point", "ConditionTimepoint"],
        )
        sample_meta = sample_meta[sample_meta["Sample name"].isin(columns)].copy()
        sample_meta["accession"] = acc
        sample_meta["sample_id"] = sample_meta["Sample name"].astype(str)
        sample_meta["sample_title"] = sample_meta["Sample name"].astype(str)
        sample_meta["original_sample_column"] = sample_meta["Sample name"].astype(str)
        sample_meta["condition"] = sample_meta["Time point"].map({"POST": "exercised", "PRE": "rest"}).fillna("")
        sample_meta["participant"] = "P" + sample_meta["Subject"].astype(str)
        sample_meta["timepoint"] = sample_meta["Time point"].astype(str).str.lower()
        sample_meta["treatment"] = sample_meta["Condition"].astype(str).str.lower()
        sample_meta["condition_timepoint"] = sample_meta["ConditionTimepoint"].astype(str)
        return sample_meta.drop(columns=["Sample name", "Subject", "Condition", "Time point", "ConditionTimepoint"])

    return None


def sample_metadata_for_columns(dataset_id: str, expr: pd.DataFrame, meta: pd.DataFrame) -> pd.DataFrame:
    acc = dataset_id.split("_", 1)[0]
    custom = custom_sample_metadata(dataset_id, expr.columns.tolist())
    if custom is not None and len(custom) == len(expr.columns):
        return custom

    acc_meta = meta[meta["accession"] == acc].copy()
    direct = acc_meta[acc_meta["sample_title"].isin(expr.columns)].copy()
    direct = direct.drop_duplicates("sample_title").set_index("sample_title", drop=False)
    if len(direct) == len(expr.columns):
        direct = direct.loc[expr.columns.tolist()].reset_index(drop=True)
        direct["sample_id"] = direct["sample_title"]
        direct["original_sample_column"] = direct["sample_title"]
        return direct

    order_map = map_by_sample_order(acc, expr, meta)
    if "sample_id" not in order_map:
        order_map["sample_id"] = order_map["original_sample_column"]
    merged = order_map.merge(acc_meta, left_on="sample_id", right_on="sample_title", how="left")
    merged["accession"] = acc
    return merged


def load_gse312393(en_map: dict[str, str]) -> list[tuple[str, pd.DataFrame, str]]:
    out = []
    p24 = DOWNLOAD_DIR / "GSE312393" / "GSE312393_human_gene_24H_exercise_tpm.tsv.gz"
    df24 = pd.read_csv(p24, sep="\t", compression="infer", index_col=0)
    df24.insert(0, "gene_id", df24.index)
    out.append(("GSE312393_24h_exercise", aggregate_by_symbol(df24, "gene_id", en_map), "tpm"))

    p6 = DOWNLOAD_DIR / "GSE312393" / "GSE312393_human_gene_6weeks_tpm.tsv.gz"
    df6 = pd.read_csv(p6, sep="\t", compression="infer")
    df6 = df6.drop(columns=["gene_id"])
    out.append(("GSE312393_6weeks_training", aggregate_by_symbol(df6, "gene_name"), "tpm"))
    return out


def load_gse272133(en_map: dict[str, str]) -> list[tuple[str, pd.DataFrame, str]]:
    path = DOWNLOAD_DIR / "GSE272133" / "GSE272133_processed_data_RNASeq.tsv.gz"
    df = pd.read_csv(path, sep="\t", compression="infer", index_col=0)
    df.insert(0, "gene_id", df.index)
    return [("GSE272133_muscle_bariatric", aggregate_by_symbol(df, "gene_id", en_map), "counts")]


def load_gse292369(_: dict[str, str]) -> list[tuple[str, pd.DataFrame, str]]:
    path = DOWNLOAD_DIR / "GSE292369" / "GSE292369_Partek_KE_recovery_Normalization_Outliers_Removed_Deseq2.txt.gz"
    df = pd.read_csv(path, sep="\t", compression="infer")
    meta_cols = {"Sample name", "Subject", "Condition", "Time point", "ConditionTimepoint"}
    expr = df.drop(columns=[col for col in meta_cols if col in df.columns]).copy()
    expr.index = df["Sample name"].astype(str)
    expr = expr.T
    return [("GSE292369_exercise_ketone_recovery", expr, "already_log_like")]


def load_gse32575(_: dict[str, str]) -> list[tuple[str, pd.DataFrame, str]]:
    probe_map = load_gpl6102_map()
    path = DOWNLOAD_DIR / "GSE32575" / "GSE32575_non-normalized.txt.gz"
    df = pd.read_csv(path, sep="\t", compression="infer")
    expr_cols = [col for col in df.columns if col == "ID_REF" or not str(col).startswith("Detection Pval")]
    expr = df[expr_cols].copy()
    expr["gene_symbol"] = expr["ID_REF"].map(probe_map).fillna("")
    expr = expr[expr["gene_symbol"].str.len() > 0]
    sample_cols = [col for col in expr.columns if col not in {"ID_REF", "gene_symbol"}]
    for col in sample_cols:
        expr[col] = pd.to_numeric(expr[col], errors="coerce")
    grouped = expr.groupby("gene_symbol")[sample_cols].mean()
    return [("GSE32575_monocytes_obesity_surgery", grouped, "microarray_intensity")]


def load_gse305038(en_map: dict[str, str]) -> list[tuple[str, pd.DataFrame, str]]:
    matrices = []
    for label, filename in [
        ("active", "GSE305038_20250714_M008795_edgeRglm_Counts_Normal_Post-Normal_Pre.xlsx"),
        ("inactive", "GSE305038_20250714_M008795_edgeRglm_Counts_Inactive_Post-Inactive_Pre.xlsx"),
    ]:
        path = DOWNLOAD_DIR / "GSE305038" / filename
        df = pd.read_excel(path, sheet_name=0)
        matrices.append(aggregate_by_symbol(df, "Unnamed: 0", en_map))
    combined = pd.concat(matrices, axis=1)
    combined = combined.loc[:, ~combined.columns.duplicated()]
    return [("GSE305038_activity_inactivity_exercise", combined, "counts")]


def load_gse318937(en_map: dict[str, str]) -> list[tuple[str, pd.DataFrame, str]]:
    path = DOWNLOAD_DIR / "GSE318937" / "GSE318937_genePerSampleOrder_FortitudeUnil.csv.gz"
    df = pd.read_csv(path, sep=",", compression="infer")
    return [("GSE318937_exercise_oleuropein", aggregate_by_symbol(df, "Unnamed: 0", en_map), "counts")]


def load_gse282850(en_map: dict[str, str]) -> list[tuple[str, pd.DataFrame, str]]:
    path = DOWNLOAD_DIR / "GSE282850" / "GSE282850_tovar-nishino_rnaseq_vst_counts.txt.gz"
    df = pd.read_csv(path, sep="\t", compression="infer")
    return [("GSE282850_muscle_cell_aicar_palmitate", aggregate_by_symbol(df, "ENSG_ID", en_map), "already_log_like")]


def load_gse294150(_: dict[str, str]) -> list[tuple[str, pd.DataFrame, str]]:
    path = DOWNLOAD_DIR / "GSE294150" / "GSE294150_Expression_Profile.GRCh38.gene.txt.gz"
    df = pd.read_csv(path, sep="\t", compression="infer", low_memory=False)
    sample_cols = [col for col in df.columns if str(col).endswith("_TPM")]
    expr = df[["Gene_Symbol", *sample_cols]].copy()
    expr = aggregate_by_symbol(expr, "Gene_Symbol")
    return [("GSE294150_visceral_adipose", expr, "tpm")]


LOADERS = [
    load_gse312393,
    load_gse305038,
    load_gse292369,
    load_gse318937,
    load_gse32575,
    load_gse272133,
    load_gse294150,
    load_gse282850,
]


def score_dataset(
    dataset_id: str,
    expr: pd.DataFrame,
    transform_hint: str,
    axis: pd.DataFrame,
    meta: pd.DataFrame,
) -> tuple[pd.DataFrame, dict[str, object], pd.DataFrame]:
    axis_symbols = axis["gene_symbol"].tolist()
    subset = expr.loc[expr.index.intersection(axis_symbols)].copy()
    subset = subset[~subset.index.duplicated(keep="first")]
    subset, transform = maybe_log2(subset, transform_hint)

    z = subset.sub(subset.mean(axis=1), axis=0).div(subset.std(axis=1).replace(0, np.nan), axis=0)
    annotated = axis.set_index("gene_symbol").join(subset, how="inner")
    annotated.to_csv(EXPR_OUT / f"{dataset_id}_axis_expression.csv")

    score_groups = axis.set_index("gene_symbol")["score_group"].to_dict()
    inflammatory_genes = [g for g in z.index if score_groups.get(g) in {"inflammatory", "both"} and g != "NAMPT"]
    repair_genes = [g for g in z.index if score_groups.get(g) in {"repair", "both"} and g != "NAMPT"]
    both_genes = [g for g in z.index if score_groups.get(g) == "both" and g != "NAMPT"]

    sample_meta = sample_metadata_for_columns(dataset_id, subset, meta)
    sample_meta = sample_meta.copy()
    if len(sample_meta) != len(subset.columns):
        sample_meta = pd.DataFrame({
            "accession": dataset_id.split("_", 1)[0],
            "sample_id": subset.columns,
            "original_sample_column": subset.columns,
        })
    sample_meta["dataset_id"] = dataset_id
    sample_meta["sample_id"] = sample_meta.get("sample_id", pd.Series(subset.columns)).fillna("")
    sample_meta["original_sample_column"] = sample_meta.get("original_sample_column", pd.Series(subset.columns)).fillna("")
    columns = subset.columns.tolist()
    if sample_meta["original_sample_column"].astype(str).tolist() != columns:
        raise ValueError(f"{dataset_id}: sample metadata is not aligned with expression columns")

    scores = sample_meta.reset_index(drop=True)
    scores["NAMPT_expression"] = subset.loc["NAMPT", columns].to_numpy() if "NAMPT" in subset.index else np.nan
    scores["NAMPT_z"] = z.loc["NAMPT", columns].to_numpy() if "NAMPT" in z.index else np.nan
    scores["inflammatory_score"] = z.loc[inflammatory_genes, columns].mean(axis=0).to_numpy() if inflammatory_genes else np.nan
    scores["repair_score"] = z.loc[repair_genes, columns].mean(axis=0).to_numpy() if repair_genes else np.nan
    scores["balance_score"] = scores["repair_score"] - scores["inflammatory_score"]
    scores["axis_genes_detected"] = len(subset)
    scores["inflammatory_genes_used"] = len(inflammatory_genes)
    scores["repair_genes_used"] = len(repair_genes)
    scores["transform"] = transform

    coverage = {
        "dataset_id": dataset_id,
        "input_genes": int(expr.shape[0]),
        "samples": int(expr.shape[1]),
        "axis_genes_detected": int(len(subset)),
        "axis_gene_total": int(len(axis_symbols)),
        "axis_gene_coverage_pct": round(100 * len(subset) / len(axis_symbols), 1),
        "has_NAMPT": "NAMPT" in subset.index,
        "inflammatory_genes_used": len(inflammatory_genes),
        "repair_genes_used": len(repair_genes),
        "both_genes_used_excluding_NAMPT": len(both_genes),
        "transform": transform,
        "detected_genes": ";".join(subset.index.tolist()),
    }
    return scores, coverage, annotated


def summarize_contrasts(scores: pd.DataFrame) -> pd.DataFrame:
    contrast_defs = [
        ("GSE312393_24h_exercise", "24h_exercise_vs_control", "24h_exercise", "control"),
        ("GSE312393_6weeks_training", "post_training_vs_pre_training", "post_training", "pre_training"),
        ("GSE305038_activity_inactivity_exercise", "active_post_vs_active_pre", "active_post", "active_pre"),
        ("GSE305038_activity_inactivity_exercise", "inactive_post_vs_inactive_pre", "inactive_post", "inactive_pre"),
        ("GSE292369_exercise_ketone_recovery", "exercised_vs_rest", "exercised", "rest"),
        ("GSE318937_exercise_oleuropein", "MICE_placebo_post_vs_pre", "MICE_Placebo_Post", "MICE_Placebo_Pre"),
        ("GSE318937_exercise_oleuropein", "MICE_placebo_24h_vs_pre", "MICE_Placebo_Post24h", "MICE_Placebo_Pre"),
        ("GSE318937_exercise_oleuropein", "MICE_active_post_vs_pre", "MICE_Active_Post", "MICE_Active_Pre"),
        ("GSE318937_exercise_oleuropein", "MICE_active_24h_vs_pre", "MICE_Active_Post24h", "MICE_Active_Pre"),
        ("GSE318937_exercise_oleuropein", "SIE_placebo_post_vs_pre", "SIE_Placebo_Post", "SIE_Placebo_Pre"),
        ("GSE318937_exercise_oleuropein", "SIE_placebo_24h_vs_pre", "SIE_Placebo_Post24h", "SIE_Placebo_Pre"),
        ("GSE318937_exercise_oleuropein", "SIE_active_post_vs_pre", "SIE_Active_Post", "SIE_Active_Pre"),
        ("GSE318937_exercise_oleuropein", "SIE_active_24h_vs_pre", "SIE_Active_Post24h", "SIE_Active_Pre"),
        ("GSE32575_monocytes_obesity_surgery", "obese_before_vs_lean", "obese_before", "lean"),
        ("GSE32575_monocytes_obesity_surgery", "obese_after_vs_obese_before", "obese_after", "obese_before"),
        ("GSE272133_muscle_bariatric", "OB_w52_vs_OB_w0", "OB_w52", "OB_w0"),
        ("GSE272133_muscle_bariatric", "T2D_w52_vs_T2D_w0", "T2D_w52", "T2D_w0"),
        ("GSE282850_muscle_cell_aicar_palmitate", "aicar_vs_differentiated", "aicar", "differentiated"),
        ("GSE282850_muscle_cell_aicar_palmitate", "palmitate_vs_differentiated", "palmitate", "differentiated"),
    ]
    rows = []
    metrics = ["NAMPT_z", "inflammatory_score", "repair_score", "balance_score"]
    for dataset_id, contrast, case, control in contrast_defs:
        ds = scores[scores["dataset_id"] == dataset_id]
        if ds.empty or "condition" not in ds.columns:
            continue
        a = ds[ds["condition"] == case]
        b = ds[ds["condition"] == control]
        if a.empty or b.empty:
            continue
        row: dict[str, object] = {
            "dataset_id": dataset_id,
            "contrast": contrast,
            "case_condition": case,
            "control_condition": control,
            "case_n": len(a),
            "control_n": len(b),
        }
        for metric in metrics:
            case_mean = float(a[metric].mean())
            ctrl_mean = float(b[metric].mean())
            pooled_sd = float(pd.concat([a[metric], b[metric]]).std())
            delta = case_mean - ctrl_mean
            row[f"{metric}_case_mean"] = round(case_mean, 4)
            row[f"{metric}_control_mean"] = round(ctrl_mean, 4)
            row[f"{metric}_delta"] = round(delta, 4)
            row[f"{metric}_std_delta"] = round(delta / pooled_sd, 4) if pooled_sd and math.isfinite(pooled_sd) else ""
        rows.append(row)
    return pd.DataFrame(rows)


def markdown_table(df: pd.DataFrame) -> str:
    """Render a small DataFrame as Markdown without optional tabulate dependency."""
    if df.empty:
        return ""
    text_df = df.copy().fillna("")
    headers = [str(col) for col in text_df.columns]
    rows = [[str(value) for value in row] for row in text_df.to_numpy()]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def write_markdown_summary(coverage: pd.DataFrame, contrasts: pd.DataFrame) -> None:
    lines = [
        "# NAMPT-axis first-pass scoring report",
        "",
        "## Scope",
        "",
        "This report harmonizes public GEO processed expression matrices into a NAMPT-axis gene subset and computes within-dataset z-scored inflammatory, repair, and balance scores. Scores are intended for direction-of-effect screening, not clinical inference.",
        "",
        "## Gene coverage",
        "",
        markdown_table(coverage[["dataset_id", "samples", "axis_genes_detected", "axis_gene_coverage_pct", "has_NAMPT", "transform"]]),
        "",
        "## Predefined contrast deltas",
        "",
    ]
    if contrasts.empty:
        lines.append("No predefined contrasts could be computed.")
    else:
        compact_cols = [
            "dataset_id", "contrast", "case_n", "control_n",
            "NAMPT_z_delta", "inflammatory_score_delta", "repair_score_delta", "balance_score_delta",
        ]
        lines.append(markdown_table(contrasts[compact_cols]))
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "NAMPT mRNA is not equivalent to extracellular NAMPT protein. The scores separate transcriptomic inflammatory and repair programs; eNAMPT-specific claims require protein, secretion, or external biomarker evidence.",
    ])
    (OUT_DIR / "nampt_axis_first_pass_scoring_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ANNOTATION_DIR.mkdir(parents=True, exist_ok=True)
    EXPR_OUT.mkdir(parents=True, exist_ok=True)
    axis = load_axis_gene_set()
    meta = pd.read_csv(SAMPLE_META_PATH, dtype=str).fillna("")
    meta["series_sample_order"] = pd.to_numeric(meta["series_sample_order"], errors="coerce")
    en_map = load_ensembl_map()

    all_scores = []
    coverage_rows = []
    for loader in LOADERS:
        for dataset_id, expr, transform_hint in loader(en_map):
            print(f"Scoring {dataset_id}: {expr.shape[0]} genes x {expr.shape[1]} samples")
            scores, coverage, _ = score_dataset(dataset_id, expr, transform_hint, axis, meta)
            all_scores.append(scores)
            coverage_rows.append(coverage)

    scores = pd.concat(all_scores, ignore_index=True, sort=False)
    coverage = pd.DataFrame(coverage_rows)
    contrasts = summarize_contrasts(scores)

    scores.to_csv(OUT_DIR / "nampt_axis_sample_scores.csv", index=False)
    coverage.to_csv(OUT_DIR / "nampt_axis_gene_coverage.csv", index=False)
    contrasts.to_csv(OUT_DIR / "nampt_axis_predefined_contrasts.csv", index=False)
    write_markdown_summary(coverage, contrasts)
    print(f"Wrote scores, coverage, contrasts and report to {OUT_DIR}")


if __name__ == "__main__":
    main()
