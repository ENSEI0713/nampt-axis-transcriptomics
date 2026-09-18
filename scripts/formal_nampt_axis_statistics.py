#!/usr/bin/env python3
"""Run formal statistics for NAMPT-axis public-data contrasts.

The script treats each dataset as its own analysis scale. It upgrades the
first-pass mean deltas into explicit paired/unpaired designs, permutation
p-values, bootstrap confidence intervals, effect sizes, and figure source data.
"""

from __future__ import annotations

import itertools
import math
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data_audit" / "outputs"
FIGURE_DIR = OUT_DIR / "figure_sources"

SAMPLE_SCORES_PATH = OUT_DIR / "nampt_axis_sample_scores.csv"
PREDEFINED_CONTRASTS_PATH = OUT_DIR / "nampt_axis_predefined_contrasts.csv"
GENE_COVERAGE_PATH = OUT_DIR / "nampt_axis_gene_coverage.csv"
INVENTORY_PATH = OUT_DIR / "curated_dataset_inventory.csv"

FORMAL_STATS_PATH = OUT_DIR / "nampt_axis_formal_contrast_stats.csv"
REPORT_PATH = OUT_DIR / "nampt_axis_phase1_statistics_report.md"

RNG_SEED = 20260616
BOOTSTRAPS = 5000
PERMUTATIONS = 20000
EXACT_SIGN_FLIP_MAX_N = 18
EXACT_UNPAIRED_COMBO_MAX = 50000

METRICS = [
    "NAMPT_z",
    "inflammatory_score",
    "repair_score",
    "balance_score",
]

PAIRING_RULES: dict[tuple[str, str], tuple[str, ...]] = {
    ("GSE312393_6weeks_training", "post_training_vs_pre_training"): ("participant",),
    ("GSE305038_activity_inactivity_exercise", "active_post_vs_active_pre"): ("participant_id",),
    ("GSE305038_activity_inactivity_exercise", "inactive_post_vs_inactive_pre"): ("participant_id",),
    ("GSE292369_exercise_ketone_recovery", "exercised_vs_rest"): ("participant", "treatment"),
    ("GSE32575_monocytes_obesity_surgery", "obese_after_vs_obese_before"): ("participant_id",),
    ("GSE272133_muscle_bariatric", "OB_w52_vs_OB_w0"): ("participant_id",),
    ("GSE272133_muscle_bariatric", "T2D_w52_vs_T2D_w0"): ("participant_id",),
    ("GSE282850_muscle_cell_aicar_palmitate", "aicar_vs_differentiated"): ("participant_id",),
    ("GSE282850_muscle_cell_aicar_palmitate", "palmitate_vs_differentiated"): ("participant_id",),
}

INDEPENDENT_UNIT_RULES: dict[tuple[str, str], tuple[str, ...]] = {
    ("GSE32575_monocytes_obesity_surgery", "obese_before_vs_lean"): ("participant_id",),
}

EXERCISE_DATASETS = {
    "GSE312393_24h_exercise",
    "GSE312393_6weeks_training",
    "GSE305038_activity_inactivity_exercise",
    "GSE292369_exercise_ketone_recovery",
    "GSE318937_exercise_oleuropein",
}

OBESITY_DATASETS = {
    "GSE32575_monocytes_obesity_surgery",
    "GSE272133_muscle_bariatric",
    "GSE282850_muscle_cell_aicar_palmitate",
}


def numeric_array(values: pd.Series) -> np.ndarray:
    arr = pd.to_numeric(values, errors="coerce").dropna().to_numpy(dtype=float)
    return arr[np.isfinite(arr)]


def mean_or_nan(values: np.ndarray) -> float:
    return float(np.mean(values)) if values.size else math.nan


def sd_or_nan(values: np.ndarray) -> float:
    return float(np.std(values, ddof=1)) if values.size > 1 else math.nan


def cohen_dz(deltas: np.ndarray) -> float:
    sd = sd_or_nan(deltas)
    if not np.isfinite(sd) or sd == 0:
        return math.nan
    return float(np.mean(deltas) / sd)


def hedges_g(control: np.ndarray, case: np.ndarray) -> float:
    n0, n1 = control.size, case.size
    if n0 < 2 or n1 < 2:
        return math.nan
    var0 = np.var(control, ddof=1)
    var1 = np.var(case, ddof=1)
    pooled_num = (n0 - 1) * var0 + (n1 - 1) * var1
    pooled_den = n0 + n1 - 2
    if pooled_den <= 0 or pooled_num <= 0:
        return math.nan
    pooled_sd = math.sqrt(pooled_num / pooled_den)
    if pooled_sd == 0:
        return math.nan
    d = (np.mean(case) - np.mean(control)) / pooled_sd
    correction = 1 - (3 / (4 * pooled_den - 1)) if pooled_den > 1 else 1.0
    return float(d * correction)


def bootstrap_ci_paired(deltas: np.ndarray, rng: np.random.Generator) -> tuple[float, float]:
    if deltas.size == 0:
        return math.nan, math.nan
    if deltas.size == 1:
        value = float(deltas[0])
        return value, value
    indices = rng.integers(0, deltas.size, size=(BOOTSTRAPS, deltas.size))
    estimates = deltas[indices].mean(axis=1)
    low, high = np.percentile(estimates, [2.5, 97.5])
    return float(low), float(high)


def bootstrap_ci_unpaired(control: np.ndarray, case: np.ndarray, rng: np.random.Generator) -> tuple[float, float]:
    if control.size == 0 or case.size == 0:
        return math.nan, math.nan
    ctrl_idx = rng.integers(0, control.size, size=(BOOTSTRAPS, control.size))
    case_idx = rng.integers(0, case.size, size=(BOOTSTRAPS, case.size))
    estimates = case[case_idx].mean(axis=1) - control[ctrl_idx].mean(axis=1)
    low, high = np.percentile(estimates, [2.5, 97.5])
    return float(low), float(high)


def sign_flip_pvalue(deltas: np.ndarray, rng: np.random.Generator) -> float:
    deltas = deltas[np.isfinite(deltas)]
    if deltas.size == 0:
        return math.nan
    observed = abs(float(np.mean(deltas)))
    if observed == 0:
        return 1.0
    if deltas.size <= EXACT_SIGN_FLIP_MAX_N:
        total = 0
        extreme = 0
        for signs in itertools.product((-1, 1), repeat=deltas.size):
            total += 1
            estimate = abs(float(np.mean(deltas * np.asarray(signs))))
            if estimate >= observed - 1e-12:
                extreme += 1
        return float(extreme / total)
    signs = rng.choice((-1, 1), size=(PERMUTATIONS, deltas.size))
    estimates = np.abs((signs * deltas).mean(axis=1))
    return float((np.sum(estimates >= observed - 1e-12) + 1) / (PERMUTATIONS + 1))


def unpaired_permutation_pvalue(control: np.ndarray, case: np.ndarray, rng: np.random.Generator) -> float:
    if control.size == 0 or case.size == 0:
        return math.nan
    observed = abs(float(np.mean(case) - np.mean(control)))
    pooled = np.concatenate([control, case])
    n_control = control.size
    total_combos = math.comb(pooled.size, n_control)
    if total_combos <= EXACT_UNPAIRED_COMBO_MAX:
        extreme = 0
        total = 0
        all_idx = np.arange(pooled.size)
        for ctrl_idx_tuple in itertools.combinations(range(pooled.size), n_control):
            total += 1
            ctrl_idx = np.fromiter(ctrl_idx_tuple, dtype=int)
            case_idx = np.setdiff1d(all_idx, ctrl_idx, assume_unique=True)
            estimate = abs(float(np.mean(pooled[case_idx]) - np.mean(pooled[ctrl_idx])))
            if estimate >= observed - 1e-12:
                extreme += 1
        return float(extreme / total)
    extreme = 0
    for _ in range(PERMUTATIONS):
        permuted = rng.permutation(pooled)
        ctrl = permuted[:n_control]
        cas = permuted[n_control:]
        estimate = abs(float(np.mean(cas) - np.mean(ctrl)))
        if estimate >= observed - 1e-12:
            extreme += 1
    return float((extreme + 1) / (PERMUTATIONS + 1))


def bh_adjust(pvalues: Iterable[float]) -> list[float]:
    pvals = list(pvalues)
    qvals = [math.nan] * len(pvals)
    valid = [(idx, p) for idx, p in enumerate(pvals) if np.isfinite(p)]
    if not valid:
        return qvals
    valid.sort(key=lambda item: item[1])
    m = len(valid)
    running_min = 1.0
    for rank_from_end, (idx, p) in enumerate(reversed(valid), start=1):
        rank = m - rank_from_end + 1
        running_min = min(running_min, p * m / rank)
        qvals[idx] = float(min(running_min, 1.0))
    return qvals


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


def pair_keys_for(dataset_id: str, contrast: str) -> tuple[str, ...]:
    if dataset_id == "GSE318937_exercise_oleuropein":
        return ("participant_id",)
    return PAIRING_RULES.get((dataset_id, contrast), ())


def independent_unit_keys_for(dataset_id: str, contrast: str) -> tuple[str, ...]:
    return INDEPENDENT_UNIT_RULES.get((dataset_id, contrast), ())


def add_pair_id(df: pd.DataFrame, keys: tuple[str, ...]) -> pd.DataFrame:
    data = df.copy()
    if not keys:
        data["_pair_id"] = ""
        data["_valid_pair"] = False
        return data
    key_frame = data.loc[:, list(keys)].fillna("").astype(str)
    valid = key_frame.apply(lambda row: all(str(value).strip() for value in row), axis=1)
    data["_pair_id"] = key_frame.apply(lambda row: "|".join(str(value).strip() for value in row), axis=1)
    data["_valid_pair"] = valid
    return data


def aggregate_independent_units(df: pd.DataFrame, metric: str, keys: tuple[str, ...]) -> np.ndarray:
    if not keys:
        return numeric_array(df[metric])
    data = add_pair_id(df, keys)
    valid = data[data["_valid_pair"]].copy()
    if valid.empty:
        return numeric_array(df[metric])
    values = valid.groupby("_pair_id", as_index=True)[metric].mean().dropna()
    return values.to_numpy(dtype=float)


def evidence_flags(row: dict[str, object]) -> str:
    flags: list[str] = []
    n = row.get("analysis_n", 0)
    p = row.get("p_value", math.nan)
    q_metric = row.get("q_value_metric", math.nan)
    ci_low = row.get("ci95_low", math.nan)
    ci_high = row.get("ci95_high", math.nan)
    try:
        n_float = float(n)
    except (TypeError, ValueError):
        n_float = 0
    if n_float < 5:
        flags.append("very_small_n")
    elif n_float < 10:
        flags.append("small_n")
    if np.isfinite(ci_low) and np.isfinite(ci_high) and ci_low <= 0 <= ci_high:
        flags.append("ci_crosses_zero")
    elif np.isfinite(ci_low) and np.isfinite(ci_high):
        flags.append("ci_excludes_zero")
    if np.isfinite(p) and p < 0.05:
        flags.append("nominal_p_lt_0.05")
    if np.isfinite(q_metric) and q_metric < 0.10:
        flags.append("metric_fdr_lt_0.10")
    return ";".join(flags) if flags else "directional_exploratory"


def analyze_contrast(
    scores: pd.DataFrame,
    contrast_row: pd.Series,
    metric: str,
    rng: np.random.Generator,
) -> dict[str, object]:
    dataset_id = str(contrast_row["dataset_id"])
    contrast = str(contrast_row["contrast"])
    control_condition = str(contrast_row["control_condition"])
    case_condition = str(contrast_row["case_condition"])
    pair_keys = pair_keys_for(dataset_id, contrast)
    independent_unit_keys = independent_unit_keys_for(dataset_id, contrast)

    subset = scores[scores["dataset_id"] == dataset_id].copy()
    control = subset[subset["condition"] == control_condition].copy()
    case = subset[subset["condition"] == case_condition].copy()

    raw_control_n = len(control)
    raw_case_n = len(case)

    base = {
        "dataset_id": dataset_id,
        "contrast": contrast,
        "contrast_source": contrast_row.get("contrast_source", "predefined"),
        "control_condition": control_condition,
        "case_condition": case_condition,
        "metric": metric,
        "control_n_raw": raw_control_n,
        "case_n_raw": raw_case_n,
        "pairing_keys": "+".join(pair_keys),
        "independent_unit_keys": "+".join(independent_unit_keys),
    }

    if pair_keys:
        control = add_pair_id(control, pair_keys)
        case = add_pair_id(case, pair_keys)
        control_pairs = (
            control[control["_valid_pair"]]
            .groupby("_pair_id", as_index=True)[metric]
            .mean()
            .dropna()
        )
        case_pairs = (
            case[case["_valid_pair"]]
            .groupby("_pair_id", as_index=True)[metric]
            .mean()
            .dropna()
        )
        common_pairs = sorted(set(control_pairs.index) & set(case_pairs.index))
        if len(common_pairs) >= 2:
            control_values = control_pairs.loc[common_pairs].to_numpy(dtype=float)
            case_values = case_pairs.loc[common_pairs].to_numpy(dtype=float)
            deltas = case_values - control_values
            ci_low, ci_high = bootstrap_ci_paired(deltas, rng)
            p_value = sign_flip_pvalue(deltas, rng)
            design = "paired"
            if len(common_pairs) < raw_control_n or len(common_pairs) < raw_case_n:
                design = "paired_intersection"
            return {
                **base,
                "analysis_design": design,
                "analysis_n": len(common_pairs),
                "paired_n": len(common_pairs),
                "analysis_n_control": len(common_pairs),
                "analysis_n_case": len(common_pairs),
                "control_mean": mean_or_nan(control_values),
                "case_mean": mean_or_nan(case_values),
                "mean_delta": mean_or_nan(deltas),
                "delta_sd": sd_or_nan(deltas),
                "ci95_low": ci_low,
                "ci95_high": ci_high,
                "effect_size_name": "paired_cohen_dz",
                "effect_size": cohen_dz(deltas),
                "p_value": p_value,
                "test_method": "paired_sign_flip_permutation",
                "ci_method": f"paired_percentile_bootstrap_{BOOTSTRAPS}",
            }

    control_values = aggregate_independent_units(control, metric, independent_unit_keys)
    case_values = aggregate_independent_units(case, metric, independent_unit_keys)
    ci_low, ci_high = bootstrap_ci_unpaired(control_values, case_values, rng)
    p_value = unpaired_permutation_pvalue(control_values, case_values, rng)
    design = "unpaired"
    if independent_unit_keys:
        design = "unpaired_independent_unit_mean"
    if pair_keys:
        design = "unpaired_fallback_insufficient_pairs"
    return {
        **base,
        "analysis_design": design,
        "analysis_n": int(control_values.size + case_values.size),
        "paired_n": 0,
        "analysis_n_control": int(control_values.size),
        "analysis_n_case": int(case_values.size),
        "control_mean": mean_or_nan(control_values),
        "case_mean": mean_or_nan(case_values),
        "mean_delta": mean_or_nan(case_values) - mean_or_nan(control_values),
        "delta_sd": math.nan,
        "ci95_low": ci_low,
        "ci95_high": ci_high,
        "effect_size_name": "hedges_g",
        "effect_size": hedges_g(control_values, case_values),
        "p_value": p_value,
        "test_method": "unpaired_label_permutation",
        "ci_method": f"unpaired_percentile_bootstrap_{BOOTSTRAPS}",
    }


def add_multiple_testing_columns(stats: pd.DataFrame) -> pd.DataFrame:
    data = stats.copy()
    data["q_value_global"] = bh_adjust(data["p_value"].tolist())
    data["q_value_metric"] = math.nan
    for metric, idx in data.groupby("metric").groups.items():
        adjusted = bh_adjust(data.loc[idx, "p_value"].tolist())
        data.loc[idx, "q_value_metric"] = adjusted
    rows = data.to_dict(orient="records")
    data["evidence_flags"] = [evidence_flags(row) for row in rows]
    return data


def write_figure_sources(stats: pd.DataFrame) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    coverage = pd.read_csv(GENE_COVERAGE_PATH, dtype=str).fillna("")
    coverage["accession"] = coverage["dataset_id"].str.split("_", n=1).str[0]
    if INVENTORY_PATH.exists():
        inventory = pd.read_csv(INVENTORY_PATH, dtype=str).fillna("")
        fig2 = coverage.merge(inventory, on="accession", how="left", suffixes=("", "_inventory"))
    else:
        fig2 = coverage.copy()
    used_datasets = set(stats["dataset_id"].unique())
    fig2["used_in_formal_contrasts"] = fig2["dataset_id"].isin(used_datasets)
    fig2.to_csv(FIGURE_DIR / "figure2_dataset_coverage.csv", index=False)

    fig3 = stats[stats["dataset_id"].isin(EXERCISE_DATASETS)].copy()
    fig3.to_csv(FIGURE_DIR / "figure3_exercise_axis_contrasts.csv", index=False)

    fig4 = stats[stats["dataset_id"].isin(OBESITY_DATASETS)].copy()
    fig4.to_csv(FIGURE_DIR / "figure4_obesity_axis_contrasts.csv", index=False)


def format_float(value: object, digits: int = 4) -> str:
    try:
        value_float = float(value)
    except (TypeError, ValueError):
        return ""
    if not np.isfinite(value_float):
        return ""
    return f"{value_float:.{digits}g}"


def write_report(stats: pd.DataFrame) -> None:
    design_cols = [
        "dataset_id",
        "contrast",
        "analysis_design",
        "pairing_keys",
        "control_n_raw",
        "case_n_raw",
        "paired_n",
    ]
    design_summary = (
        stats[design_cols]
        .drop_duplicates()
        .sort_values(["dataset_id", "contrast"])
        .reset_index(drop=True)
    )

    main_candidates = stats[
        (stats["metric"].isin(["NAMPT_z", "inflammatory_score", "repair_score", "balance_score"]))
        & (stats["ci95_low"] * stats["ci95_high"] > 0)
    ].copy()
    main_candidates = main_candidates.sort_values(
        ["metric", "q_value_metric", "p_value", "dataset_id"], na_position="last"
    )
    for col in ["mean_delta", "ci95_low", "ci95_high", "p_value", "q_value_metric", "effect_size"]:
        main_candidates[col] = main_candidates[col].map(format_float)

    metric_direction = (
        stats.groupby(["metric", "dataset_id", "contrast"], as_index=False)
        .agg(mean_delta=("mean_delta", "mean"), q_value_metric=("q_value_metric", "mean"))
        .sort_values(["metric", "dataset_id", "contrast"])
    )
    direction_counts = []
    for metric, group in metric_direction.groupby("metric"):
        direction_counts.append(
            {
                "metric": metric,
                "positive_delta_contrasts": int((group["mean_delta"] > 0).sum()),
                "negative_delta_contrasts": int((group["mean_delta"] < 0).sum()),
                "total_contrasts": int(len(group)),
            }
        )
    direction_counts_df = pd.DataFrame(direction_counts)

    report = f"""# NAMPT-axis Phase 1 formal statistics report

## Scope

This report upgrades the first-pass public GEO NAMPT-axis scoring into explicit statistical contrasts. Each dataset is analyzed on its own within-dataset z-score scale. NAMPT mRNA, inflammatory score, repair score, and balance score are not interpreted as extracellular NAMPT protein or clinical biomarkers.

## Statistical design

- Paired contrasts use matched participant-level deltas, a two-sided sign-flip permutation p-value, paired Cohen dz, and {BOOTSTRAPS} paired bootstrap resamples for the 95% confidence interval.
- Unpaired contrasts use two-sided label permutation, Hedges g, and {BOOTSTRAPS} unpaired bootstrap resamples for the 95% confidence interval.
- Multiple testing is controlled with Benjamini-Hochberg FDR globally and separately within each metric.
- Small-sample contrasts are retained as evidence-generating signals, not definitive clinical claims.

## Contrast design audit

{markdown_table(design_summary, design_cols)}

## Direction summary

{markdown_table(direction_counts_df, ["metric", "positive_delta_contrasts", "negative_delta_contrasts", "total_contrasts"])}

## CI-supported directional candidates

These rows have a bootstrap 95% CI that does not cross zero. They are candidates for main or supplementary figure annotation after biological review.

{markdown_table(main_candidates, ["dataset_id", "contrast", "metric", "analysis_design", "analysis_n", "mean_delta", "ci95_low", "ci95_high", "p_value", "q_value_metric", "evidence_flags"], max_rows=30)}

## Output files

- `data_audit/outputs/nampt_axis_formal_contrast_stats.csv`
- `data_audit/outputs/figure_sources/figure2_dataset_coverage.csv`
- `data_audit/outputs/figure_sources/figure3_exercise_axis_contrasts.csv`
- `data_audit/outputs/figure_sources/figure4_obesity_axis_contrasts.csv`

## Interpretation boundary

The current evidence supports a public-data, transcriptomic, state-dependent NAMPT-axis model. It does not establish eNAMPT directionality, plasma NAMPT performance, exercise prescription thresholds, or causality. Those claims require protein/secretion data, clinical covariates, and prospective validation.
"""
    REPORT_PATH.write_text(report, encoding="utf-8")


def main() -> None:
    rng = np.random.default_rng(RNG_SEED)
    scores = pd.read_csv(SAMPLE_SCORES_PATH, dtype=str).fillna("")
    contrasts = pd.read_csv(PREDEFINED_CONTRASTS_PATH, dtype=str).fillna("")
    contrasts["contrast_source"] = "predefined"
    for metric in METRICS:
        scores[metric] = pd.to_numeric(scores[metric], errors="coerce")

    rows: list[dict[str, object]] = []
    for _, contrast_row in contrasts.iterrows():
        for metric in METRICS:
            rows.append(analyze_contrast(scores, contrast_row, metric, rng))

    stats = add_multiple_testing_columns(pd.DataFrame(rows))
    sort_cols = ["dataset_id", "contrast", "metric"]
    stats = stats.sort_values(sort_cols).reset_index(drop=True)
    stats.to_csv(FORMAL_STATS_PATH, index=False)
    write_figure_sources(stats)
    write_report(stats)
    print(f"Wrote {FORMAL_STATS_PATH}")
    print(f"Wrote {REPORT_PATH}")
    print(f"Wrote figure sources in {FIGURE_DIR}")


if __name__ == "__main__":
    main()
