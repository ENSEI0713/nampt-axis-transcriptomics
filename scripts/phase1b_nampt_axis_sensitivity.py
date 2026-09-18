#!/usr/bin/env python3
"""Run Phase 1b sensitivity checks for the NAMPT-axis analysis.

The script recomputes sample-level axis scores directly from saved per-dataset
axis expression matrices, then reruns the predefined formal contrasts after
dropping biologically important genes or modules. Original Phase 1 outputs are
left untouched.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

import formal_nampt_axis_statistics as formal


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data_audit" / "outputs"
EXPR_DIR = OUT_DIR / "nampt_axis_expression"
SENS_DIR = OUT_DIR / "phase1b_sensitivity"

GENE_SET_PATH = OUT_DIR / "NAMPT_axis_gene_set_v1.csv"
ORIGINAL_SCORES_PATH = OUT_DIR / "nampt_axis_sample_scores.csv"
ORIGINAL_STATS_PATH = OUT_DIR / "nampt_axis_formal_contrast_stats.csv"
CONTRASTS_PATH = OUT_DIR / "nampt_axis_predefined_contrasts.csv"

SENSITIVITY_SCORES_PATH = SENS_DIR / "nampt_axis_sensitivity_sample_scores.csv"
SENSITIVITY_STATS_PATH = SENS_DIR / "nampt_axis_sensitivity_contrast_stats.csv"
SENSITIVITY_COMPARISON_PATH = SENS_DIR / "nampt_axis_sensitivity_comparison_to_primary.csv"
SENSITIVITY_SUMMARY_PATH = SENS_DIR / "nampt_axis_sensitivity_summary.csv"
SENSITIVITY_USAGE_PATH = SENS_DIR / "nampt_axis_sensitivity_gene_usage.csv"
RECOMPUTE_AUDIT_PATH = SENS_DIR / "nampt_axis_primary_recompute_audit.csv"
REPORT_PATH = SENS_DIR / "phase1b_sensitivity_report.md"

# Phase 1 already used the heavier formal resampling budget. Phase 1b is a
# stability screen across many variants, so use a lighter reproducible budget.
SENSITIVITY_BOOTSTRAPS = 1000
SENSITIVITY_PERMUTATIONS = 5000
SENSITIVITY_EXACT_SIGN_FLIP_MAX_N = 14
SENSITIVITY_EXACT_UNPAIRED_COMBO_MAX = 10000

ANNOTATION_COLS = ["gene_symbol", "module", "score_group", "rationale"]
METRICS = formal.METRICS
SCORE_OUTPUT_COLS = {
    "NAMPT_expression",
    "NAMPT_z",
    "inflammatory_score",
    "repair_score",
    "balance_score",
    "axis_genes_detected",
    "inflammatory_genes_used",
    "repair_genes_used",
}

CLASSIC_CYTOKINES = {"IL6", "TNF", "IL1B", "CCL2", "CXCL8"}


@dataclass(frozen=True)
class SensitivityVariant:
    variant_id: str
    variant_type: str
    description: str
    exclude_genes: frozenset[str] = field(default_factory=frozenset)
    exclude_modules: frozenset[str] = field(default_factory=frozenset)


TARGETED_VARIANTS = [
    SensitivityVariant(
        "primary",
        "baseline",
        "Primary score reconstructed from saved axis expression matrices.",
    ),
    SensitivityVariant(
        "drop_nampt",
        "gene_drop",
        "NAMPT is excluded from composite pools; NAMPT_z is still reported separately.",
        exclude_genes=frozenset({"NAMPT"}),
    ),
    SensitivityVariant(
        "drop_classic_cytokines",
        "gene_drop",
        "Drop classic cytokine/chemokine inflammatory genes.",
        exclude_genes=frozenset(CLASSIC_CYTOKINES),
    ),
    SensitivityVariant(
        "drop_nfkb_module",
        "module_drop",
        "Drop the NF-kB inflammation module.",
        exclude_modules=frozenset({"nfkb_inflammation"}),
    ),
    SensitivityVariant(
        "drop_monocyte_macrophage",
        "module_drop",
        "Drop the monocyte/macrophage module.",
        exclude_modules=frozenset({"monocyte_macrophage"}),
    ),
    SensitivityVariant(
        "drop_nad_salvage_core",
        "module_drop",
        "Drop the NAD salvage core module from composite pools.",
        exclude_modules=frozenset({"nad_salvage_core"}),
    ),
    SensitivityVariant(
        "drop_nad_consumption",
        "module_drop",
        "Drop NAD-consuming inflammatory and repair modules.",
        exclude_modules=frozenset({"nad_consumption_inflammation", "nad_consumption_repair"}),
    ),
    SensitivityVariant(
        "drop_mito_repair",
        "module_drop",
        "Drop mitochondrial, AMPK, sirtuin, and oxidative-stress repair modules.",
        exclude_modules=frozenset(
            {
                "ampk_mitochondria_repair",
                "mitochondrial_biogenesis",
                "mitochondrial_stress",
                "oxidative_stress_repair",
                "sirtuin_repair",
            }
        ),
    ),
    SensitivityVariant(
        "drop_autophagy_dna_repair",
        "module_drop",
        "Drop autophagy and DNA damage repair modules.",
        exclude_modules=frozenset({"autophagy_repair", "dna_damage_repair"}),
    ),
    SensitivityVariant(
        "drop_insulin_adipose_metabolism",
        "module_drop",
        "Drop insulin and adipose metabolism modules.",
        exclude_modules=frozenset(
            {
                "insulin_metabolism",
                "adipose_metabolism_inflammation",
                "adipose_metabolism_resolution",
            }
        ),
    ),
]


def format_float(value: object, digits: int = 4) -> str:
    try:
        value_float = float(value)
    except (TypeError, ValueError):
        return ""
    if not np.isfinite(value_float):
        return ""
    return f"{value_float:.{digits}g}"


def markdown_table(df: pd.DataFrame, columns: list[str], max_rows: int | None = None) -> str:
    view = df.loc[:, columns].copy()
    if max_rows is not None:
        view = view.head(max_rows)
    if view.empty:
        return "No rows."
    view = view.fillna("")
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    rows = [header, sep]
    for _, row in view.iterrows():
        rows.append("| " + " | ".join(str(row[col]) for col in columns) + " |")
    return "\n".join(rows)


def signed_direction(value: object) -> float:
    try:
        value_float = float(value)
    except (TypeError, ValueError):
        return math.nan
    if not np.isfinite(value_float):
        return math.nan
    if abs(value_float) < 1e-12:
        return 0.0
    return 1.0 if value_float > 0 else -1.0


def ci_supported(df: pd.DataFrame) -> pd.Series:
    low = pd.to_numeric(df["ci95_low"], errors="coerce")
    high = pd.to_numeric(df["ci95_high"], errors="coerce")
    return (low * high > 0).fillna(False)


def load_axis_expression(path: Path) -> tuple[pd.DataFrame, list[str]]:
    data = pd.read_csv(path, dtype=str).fillna("")
    missing = [col for col in ANNOTATION_COLS if col not in data.columns]
    if missing:
        raise ValueError(f"{path} is missing annotation columns: {missing}")
    sample_cols = [col for col in data.columns if col not in ANNOTATION_COLS]
    for col in sample_cols:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    data["gene_symbol"] = data["gene_symbol"].astype(str).str.upper()
    return data, sample_cols


def gene_zscores(expr_data: pd.DataFrame, sample_cols: list[str]) -> pd.DataFrame:
    matrix = expr_data.set_index("gene_symbol")[sample_cols].apply(pd.to_numeric, errors="coerce")
    matrix = matrix.groupby(level=0).mean()
    row_mean = matrix.mean(axis=1)
    row_sd = matrix.std(axis=1, ddof=1).replace(0, np.nan)
    return matrix.sub(row_mean, axis=0).div(row_sd, axis=0)


def metadata_for_dataset(dataset_id: str, sample_cols: list[str], original_scores: pd.DataFrame) -> pd.DataFrame:
    dataset_scores = original_scores[original_scores["dataset_id"] == dataset_id].copy()
    keep_cols = [col for col in dataset_scores.columns if col not in SCORE_OUTPUT_COLS]
    dataset_scores = dataset_scores.loc[:, keep_cols]

    if not dataset_scores.empty and "original_sample_column" in dataset_scores.columns:
        indexed = dataset_scores.drop_duplicates("original_sample_column").set_index("original_sample_column")
        if set(sample_cols).issubset(set(indexed.index)):
            meta = indexed.loc[sample_cols].reset_index()
            return meta

    return pd.DataFrame(
        {
            "accession": [dataset_id.split("_", 1)[0]] * len(sample_cols),
            "sample_id": sample_cols,
            "sample_title": sample_cols,
            "original_sample_column": sample_cols,
            "dataset_id": [dataset_id] * len(sample_cols),
        }
    )


def score_dataset_for_variant(
    dataset_id: str,
    expr_data: pd.DataFrame,
    sample_cols: list[str],
    original_scores: pd.DataFrame,
    variant: SensitivityVariant,
) -> pd.DataFrame:
    z = gene_zscores(expr_data, sample_cols)
    module_by_gene = expr_data.drop_duplicates("gene_symbol").set_index("gene_symbol")["module"].to_dict()
    score_group_by_gene = expr_data.drop_duplicates("gene_symbol").set_index("gene_symbol")["score_group"].to_dict()

    excluded_genes = {gene.upper() for gene in variant.exclude_genes}
    excluded_modules = set(variant.exclude_modules)

    def usable_for_composite(gene: str) -> bool:
        if gene == "NAMPT":
            return False
        if gene in excluded_genes:
            return False
        if module_by_gene.get(gene, "") in excluded_modules:
            return False
        return True

    inflammatory_genes = [
        gene
        for gene in z.index
        if score_group_by_gene.get(gene) in {"inflammatory", "both"} and usable_for_composite(gene)
    ]
    repair_genes = [
        gene
        for gene in z.index
        if score_group_by_gene.get(gene) in {"repair", "both"} and usable_for_composite(gene)
    ]

    meta = metadata_for_dataset(dataset_id, sample_cols, original_scores).reset_index(drop=True)
    meta["dataset_id"] = dataset_id

    expr_matrix = expr_data.set_index("gene_symbol")[sample_cols].apply(pd.to_numeric, errors="coerce")
    expr_matrix = expr_matrix.groupby(level=0).mean()

    scores = meta.copy()
    scores["sensitivity_variant"] = variant.variant_id
    scores["sensitivity_variant_type"] = variant.variant_type
    scores["sensitivity_description"] = variant.description
    scores["excluded_genes"] = ";".join(sorted(excluded_genes))
    scores["excluded_modules"] = ";".join(sorted(excluded_modules))
    scores["NAMPT_expression"] = (
        expr_matrix.loc["NAMPT", sample_cols].to_numpy(dtype=float) if "NAMPT" in expr_matrix.index else np.nan
    )
    scores["NAMPT_z"] = z.loc["NAMPT", sample_cols].to_numpy(dtype=float) if "NAMPT" in z.index else np.nan
    scores["inflammatory_score"] = (
        z.loc[inflammatory_genes, sample_cols].mean(axis=0).to_numpy(dtype=float) if inflammatory_genes else np.nan
    )
    scores["repair_score"] = z.loc[repair_genes, sample_cols].mean(axis=0).to_numpy(dtype=float) if repair_genes else np.nan
    scores["balance_score"] = scores["repair_score"] - scores["inflammatory_score"]
    scores["axis_genes_detected"] = int(len(z.index))
    scores["inflammatory_genes_used"] = int(len(inflammatory_genes))
    scores["repair_genes_used"] = int(len(repair_genes))
    scores["inflammatory_gene_symbols_used"] = ";".join(inflammatory_genes)
    scores["repair_gene_symbols_used"] = ";".join(repair_genes)
    return scores


def recompute_scores_for_variants(
    variants: list[SensitivityVariant],
    original_scores: pd.DataFrame,
) -> pd.DataFrame:
    all_scores: list[pd.DataFrame] = []
    expr_paths = sorted(EXPR_DIR.glob("*_axis_expression.csv"))
    if not expr_paths:
        raise FileNotFoundError(f"No axis expression files found in {EXPR_DIR}")

    for path in expr_paths:
        dataset_id = path.name.removesuffix("_axis_expression.csv")
        expr_data, sample_cols = load_axis_expression(path)
        for variant in variants:
            all_scores.append(score_dataset_for_variant(dataset_id, expr_data, sample_cols, original_scores, variant))

    scores = pd.concat(all_scores, ignore_index=True, sort=False)
    for metric in METRICS:
        scores[metric] = pd.to_numeric(scores[metric], errors="coerce")
    return scores


def run_stats_for_variants(scores: pd.DataFrame, contrasts: pd.DataFrame, variants: list[SensitivityVariant]) -> pd.DataFrame:
    rows: list[pd.DataFrame] = []
    for offset, variant in enumerate(variants):
        rng = np.random.default_rng(formal.RNG_SEED + offset)
        variant_scores = scores[scores["sensitivity_variant"] == variant.variant_id].copy()
        stats_rows: list[dict[str, object]] = []
        for _, contrast_row in contrasts.iterrows():
            for metric in METRICS:
                stats_rows.append(formal.analyze_contrast(variant_scores, contrast_row, metric, rng))
        stats = formal.add_multiple_testing_columns(pd.DataFrame(stats_rows))
        stats.insert(0, "sensitivity_variant", variant.variant_id)
        stats.insert(1, "sensitivity_variant_type", variant.variant_type)
        stats.insert(2, "sensitivity_description", variant.description)
        stats.insert(3, "excluded_genes", ";".join(sorted(variant.exclude_genes)))
        stats.insert(4, "excluded_modules", ";".join(sorted(variant.exclude_modules)))
        rows.append(stats)
        print(f"Finished stats for {variant.variant_id}: {len(stats)} rows")
    return pd.concat(rows, ignore_index=True, sort=False)


def audit_primary_recompute(primary_scores: pd.DataFrame, original_scores: pd.DataFrame) -> pd.DataFrame:
    key_cols = ["dataset_id", "original_sample_column"]
    merged = primary_scores[key_cols + METRICS].merge(
        original_scores[key_cols + METRICS],
        on=key_cols,
        how="inner",
        suffixes=("_recomputed", "_original"),
    )
    rows = []
    for metric in METRICS:
        left = pd.to_numeric(merged[f"{metric}_recomputed"], errors="coerce")
        right = pd.to_numeric(merged[f"{metric}_original"], errors="coerce")
        diff = (left - right).abs()
        rows.append(
            {
                "metric": metric,
                "matched_samples": int(diff.notna().sum()),
                "max_abs_difference": float(diff.max(skipna=True)) if diff.notna().any() else math.nan,
                "median_abs_difference": float(diff.median(skipna=True)) if diff.notna().any() else math.nan,
            }
        )
    return pd.DataFrame(rows)


def compare_to_primary(all_stats: pd.DataFrame) -> pd.DataFrame:
    key_cols = ["dataset_id", "contrast", "metric"]
    primary_cols = key_cols + [
        "mean_delta",
        "ci95_low",
        "ci95_high",
        "p_value",
        "q_value_metric",
        "evidence_flags",
    ]
    primary = all_stats[all_stats["sensitivity_variant"] == "primary"].loc[:, primary_cols].copy()
    comparison = all_stats.merge(primary, on=key_cols, how="left", suffixes=("", "_primary"))

    comparison["mean_delta"] = pd.to_numeric(comparison["mean_delta"], errors="coerce")
    comparison["mean_delta_primary"] = pd.to_numeric(comparison["mean_delta_primary"], errors="coerce")
    comparison["delta_difference_vs_primary"] = comparison["mean_delta"] - comparison["mean_delta_primary"]
    comparison["abs_delta_difference_vs_primary"] = comparison["delta_difference_vs_primary"].abs()
    comparison["relative_abs_delta_difference_vs_primary"] = comparison["abs_delta_difference_vs_primary"] / comparison[
        "mean_delta_primary"
    ].abs().replace(0, np.nan)

    comparison["direction"] = comparison["mean_delta"].map(signed_direction)
    comparison["direction_primary"] = comparison["mean_delta_primary"].map(signed_direction)
    valid_direction = comparison["direction"].notna() & comparison["direction_primary"].notna()
    comparison["direction_same_as_primary"] = np.where(
        valid_direction,
        comparison["direction"] == comparison["direction_primary"],
        np.nan,
    )
    primary_low = pd.to_numeric(comparison["ci95_low_primary"], errors="coerce")
    primary_high = pd.to_numeric(comparison["ci95_high_primary"], errors="coerce")
    comparison["primary_ci_supported"] = (primary_low * primary_high > 0).fillna(False)
    comparison["variant_ci_supported"] = ci_supported(comparison)
    comparison["ci_support_retained"] = (
        comparison["primary_ci_supported"]
        & comparison["variant_ci_supported"]
        & comparison["direction_same_as_primary"].fillna(False).astype(bool)
    )
    comparison["ci_support_lost"] = comparison["primary_ci_supported"] & ~comparison["variant_ci_supported"]
    comparison["ci_support_gained"] = ~comparison["primary_ci_supported"] & comparison["variant_ci_supported"]
    comparison["direction_flipped"] = valid_direction & (comparison["direction"] != comparison["direction_primary"])
    return comparison


def summarize_sensitivity(comparison: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    non_primary = comparison[comparison["sensitivity_variant"] != "primary"].copy()
    for (variant_id, metric), group in non_primary.groupby(["sensitivity_variant", "metric"], sort=True):
        valid = group[group["direction_same_as_primary"].notna()].copy()
        direction_agreement = float(valid["direction_same_as_primary"].mean() * 100) if len(valid) else math.nan
        rows.append(
            {
                "sensitivity_variant": variant_id,
                "metric": metric,
                "contrasts_evaluated": int(len(group)),
                "direction_agreement_pct": direction_agreement,
                "direction_flips": int(group["direction_flipped"].sum()),
                "primary_ci_supported": int(group["primary_ci_supported"].sum()),
                "variant_ci_supported": int(group["variant_ci_supported"].sum()),
                "ci_support_retained": int(group["ci_support_retained"].sum()),
                "ci_support_lost": int(group["ci_support_lost"].sum()),
                "ci_support_gained": int(group["ci_support_gained"].sum()),
                "median_abs_delta_difference": float(group["abs_delta_difference_vs_primary"].median(skipna=True)),
                "median_relative_abs_delta_difference": float(
                    group["relative_abs_delta_difference_vs_primary"].median(skipna=True)
                ),
            }
        )
    return pd.DataFrame(rows)


def summarize_gene_usage(scores: pd.DataFrame) -> pd.DataFrame:
    usage_cols = [
        "sensitivity_variant",
        "dataset_id",
        "axis_genes_detected",
        "inflammatory_genes_used",
        "repair_genes_used",
        "excluded_genes",
        "excluded_modules",
    ]
    usage = scores.loc[:, usage_cols].drop_duplicates().sort_values(["sensitivity_variant", "dataset_id"])
    return usage.reset_index(drop=True)


def write_report(
    variants: list[SensitivityVariant],
    recompute_audit: pd.DataFrame,
    summary: pd.DataFrame,
    comparison: pd.DataFrame,
    usage: pd.DataFrame,
) -> None:
    overall = (
        summary.groupby("sensitivity_variant", as_index=False)
        .agg(
            direction_agreement_pct=("direction_agreement_pct", "mean"),
            direction_flips=("direction_flips", "sum"),
            primary_ci_supported=("primary_ci_supported", "sum"),
            ci_support_retained=("ci_support_retained", "sum"),
            ci_support_lost=("ci_support_lost", "sum"),
            ci_support_gained=("ci_support_gained", "sum"),
            median_abs_delta_difference=("median_abs_delta_difference", "median"),
        )
        .sort_values(["direction_flips", "ci_support_lost", "sensitivity_variant"])
    )
    for col in ["direction_agreement_pct", "median_abs_delta_difference"]:
        overall[col] = overall[col].map(format_float)

    summary_view = summary.copy().sort_values(["metric", "ci_support_lost", "direction_flips", "sensitivity_variant"])
    for col in ["direction_agreement_pct", "median_abs_delta_difference", "median_relative_abs_delta_difference"]:
        summary_view[col] = summary_view[col].map(format_float)

    fragile = comparison[
        (comparison["sensitivity_variant"] != "primary")
        & (comparison["metric"].isin(["inflammatory_score", "repair_score", "balance_score"]))
        & (comparison["primary_ci_supported"])
        & (~comparison["ci_support_retained"])
    ].copy()
    fragile = fragile.sort_values(
        ["metric", "sensitivity_variant", "dataset_id", "contrast"],
        na_position="last",
    )
    for col in ["mean_delta_primary", "mean_delta", "delta_difference_vs_primary", "p_value", "q_value_metric"]:
        fragile[col] = fragile[col].map(format_float)

    recompute_view = recompute_audit.copy()
    for col in ["max_abs_difference", "median_abs_difference"]:
        recompute_view[col] = recompute_view[col].map(format_float)

    min_usage = (
        usage.groupby("sensitivity_variant", as_index=False)
        .agg(
            min_inflammatory_genes_used=("inflammatory_genes_used", "min"),
            min_repair_genes_used=("repair_genes_used", "min"),
        )
        .sort_values("sensitivity_variant")
    )

    variant_table = pd.DataFrame(
        [
            {
                "sensitivity_variant": variant.variant_id,
                "variant_type": variant.variant_type,
                "excluded_genes": ";".join(sorted(variant.exclude_genes)),
                "excluded_modules": ";".join(sorted(variant.exclude_modules)),
            }
            for variant in variants
        ]
    )

    report = f"""# NAMPT-axis Phase 1b sensitivity report

## Scope

This report tests whether Phase 1 transcriptomic NAMPT-axis results are driven by a small set of high-profile genes or modules. Scores are recomputed from saved per-dataset expression matrices, then the same predefined contrasts and paired/unpaired rules are rerun. Original Phase 1 files are not overwritten.

## Variants tested

{markdown_table(variant_table, ["sensitivity_variant", "variant_type", "excluded_genes", "excluded_modules"])}

## Primary recompute audit

The primary sensitivity score should reproduce the original Phase 1 sample-level scores. Very small floating point differences are expected.

{markdown_table(recompute_view, ["metric", "matched_samples", "max_abs_difference", "median_abs_difference"])}

## Overall stability versus primary

{markdown_table(overall, ["sensitivity_variant", "direction_agreement_pct", "direction_flips", "primary_ci_supported", "ci_support_retained", "ci_support_lost", "ci_support_gained", "median_abs_delta_difference"])}

## Metric-level stability

{markdown_table(summary_view, ["sensitivity_variant", "metric", "direction_agreement_pct", "direction_flips", "primary_ci_supported", "variant_ci_supported", "ci_support_retained", "ci_support_lost", "ci_support_gained", "median_abs_delta_difference", "median_relative_abs_delta_difference"], max_rows=80)}

## CI-supported rows that become fragile

Rows listed here had a primary 95% CI excluding zero but did not retain same-direction CI support under a sensitivity variant. These are wording-caution rows, not automatic exclusions.

{markdown_table(fragile, ["sensitivity_variant", "dataset_id", "contrast", "metric", "mean_delta_primary", "mean_delta", "delta_difference_vs_primary", "p_value", "q_value_metric"], max_rows=80)}

## Minimum genes retained per variant

{markdown_table(min_usage, ["sensitivity_variant", "min_inflammatory_genes_used", "min_repair_genes_used"])}

## Output files

- `data_audit/outputs/phase1b_sensitivity/nampt_axis_sensitivity_sample_scores.csv`
- `data_audit/outputs/phase1b_sensitivity/nampt_axis_sensitivity_contrast_stats.csv`
- `data_audit/outputs/phase1b_sensitivity/nampt_axis_sensitivity_comparison_to_primary.csv`
- `data_audit/outputs/phase1b_sensitivity/nampt_axis_sensitivity_summary.csv`
- `data_audit/outputs/phase1b_sensitivity/nampt_axis_sensitivity_gene_usage.csv`
- `data_audit/outputs/phase1b_sensitivity/nampt_axis_primary_recompute_audit.csv`

## Interpretation boundary

Stable transcriptomic sensitivity supports using the NAMPT-axis score as a public-data foundation for a state-dependent inflammatory-repair model. It still does not prove extracellular NAMPT protein directionality, NAD abundance, clinical inflammation state, or exercise-prescription thresholds. Those claims require Phase 2 protein/metabolite evidence and later validation.
"""
    REPORT_PATH.write_text(report, encoding="utf-8")


def main() -> None:
    SENS_DIR.mkdir(parents=True, exist_ok=True)

    formal.BOOTSTRAPS = SENSITIVITY_BOOTSTRAPS
    formal.PERMUTATIONS = SENSITIVITY_PERMUTATIONS
    formal.EXACT_SIGN_FLIP_MAX_N = SENSITIVITY_EXACT_SIGN_FLIP_MAX_N
    formal.EXACT_UNPAIRED_COMBO_MAX = SENSITIVITY_EXACT_UNPAIRED_COMBO_MAX

    if not GENE_SET_PATH.exists():
        raise FileNotFoundError(GENE_SET_PATH)
    if not ORIGINAL_SCORES_PATH.exists():
        raise FileNotFoundError(ORIGINAL_SCORES_PATH)
    if not CONTRASTS_PATH.exists():
        raise FileNotFoundError(CONTRASTS_PATH)
    if not ORIGINAL_STATS_PATH.exists():
        raise FileNotFoundError(ORIGINAL_STATS_PATH)

    original_scores = pd.read_csv(ORIGINAL_SCORES_PATH, dtype=str).fillna("")
    contrasts = pd.read_csv(CONTRASTS_PATH, dtype=str).fillna("")
    contrasts["contrast_source"] = "predefined"

    variants = TARGETED_VARIANTS
    print(f"Running {len(variants)} sensitivity variants with {SENSITIVITY_BOOTSTRAPS} bootstraps and {SENSITIVITY_PERMUTATIONS} permutations")
    scores = recompute_scores_for_variants(variants, original_scores)
    print(f"Recomputed {len(scores)} sample-score rows")
    stats = run_stats_for_variants(scores, contrasts, variants)
    print(f"Computed {len(stats)} contrast-stat rows")
    comparison = compare_to_primary(stats)
    summary = summarize_sensitivity(comparison)
    usage = summarize_gene_usage(scores)
    recompute_audit = audit_primary_recompute(
        scores[scores["sensitivity_variant"] == "primary"].copy(),
        original_scores.copy(),
    )

    scores.to_csv(SENSITIVITY_SCORES_PATH, index=False)
    stats.to_csv(SENSITIVITY_STATS_PATH, index=False)
    comparison.to_csv(SENSITIVITY_COMPARISON_PATH, index=False)
    summary.to_csv(SENSITIVITY_SUMMARY_PATH, index=False)
    usage.to_csv(SENSITIVITY_USAGE_PATH, index=False)
    recompute_audit.to_csv(RECOMPUTE_AUDIT_PATH, index=False)
    write_report(variants, recompute_audit, summary, comparison, usage)

    print(f"Wrote {SENSITIVITY_SCORES_PATH}")
    print(f"Wrote {SENSITIVITY_STATS_PATH}")
    print(f"Wrote {SENSITIVITY_SUMMARY_PATH}")
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
