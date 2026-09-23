#!/usr/bin/env python3
"""Fallback Python renderer for NAMPT-axis Phase 1 figures.

The R renderer is kept as the preferred publication renderer, but some local
environments do not have Rscript available. This script reads the same figure
source CSV files and exports refreshed PDF/PNG/SVG/TIFF outputs.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data_audit" / "outputs"
FIGURE_SOURCE_DIR = OUT_DIR / "figure_sources"
FIGURE_OUT_DIR = OUT_DIR / "figures_phase2"

FIGURE2_PATH = FIGURE_SOURCE_DIR / "figure2_dataset_coverage.csv"
FIGURE3_PATH = FIGURE_SOURCE_DIR / "figure3_exercise_axis_contrasts.csv"
FIGURE4_PATH = FIGURE_SOURCE_DIR / "figure4_obesity_axis_contrasts.csv"
FORMAL_STATS_PATH = OUT_DIR / "nampt_axis_formal_contrast_stats.csv"

METRIC_ORDER = ["NAMPT_z", "inflammatory_score", "repair_score", "balance_score"]
METRIC_LABELS = {
    "NAMPT_z": "NAMPT mRNA\n(z)",
    "inflammatory_score": "Inflammatory\nscore",
    "repair_score": "Repair / metabolic\nscore",
    "balance_score": "Balance\n(repair - inflammatory)",
}

DATASET_LABELS = {
    "GSE312393_24h_exercise": "GSE312393\nacute exercise",
    "GSE312393_6weeks_training": "GSE312393\n6-week training",
    "GSE305038_activity_inactivity_exercise": "GSE305038\nactivity state",
    "GSE292369_exercise_ketone_recovery": "GSE292369\nketone recovery",
    "GSE318937_exercise_oleuropein": "GSE318937\nexercise + OLE",
    "GSE32575_monocytes_obesity_surgery": "GSE32575\nmonocytes",
    "GSE272133_muscle_bariatric": "GSE272133\nmuscle bariatric",
    "GSE282850_muscle_cell_aicar_palmitate": "GSE282850\nmyotube stress",
    "GSE294150_visceral_adipose": "GSE294150\nvisceral adipose",
}

CONTRAST_LABELS = {
    "24h_exercise_vs_control": "Eccentric exercise, 24 h",
    "post_training_vs_pre_training": "Resistance training, 6 weeks",
    "active_post_vs_active_pre": "Normal activity + exercise",
    "inactive_post_vs_inactive_pre": "Reduced activity + exercise",
    "exercised_vs_rest": "Cycling recovery",
    "MICE_placebo_post_vs_pre": "MICE placebo, immediate",
    "MICE_placebo_24h_vs_pre": "MICE placebo, 24 h",
    "MICE_active_post_vs_pre": "MICE OLE, immediate",
    "MICE_active_24h_vs_pre": "MICE OLE, 24 h",
    "SIE_placebo_post_vs_pre": "SIE placebo, immediate",
    "SIE_placebo_24h_vs_pre": "SIE placebo, 24 h",
    "SIE_active_post_vs_pre": "SIE OLE, immediate",
    "SIE_active_24h_vs_pre": "SIE OLE, 24 h",
    "obese_before_vs_lean": "Obesity vs lean monocytes",
    "obese_after_vs_obese_before": "Post-bariatric vs pre monocytes",
    "OB_w52_vs_OB_w0": "Obesity muscle, week 52 vs 0",
    "T2D_w52_vs_T2D_w0": "T2D muscle, week 52 vs 0",
    "aicar_vs_differentiated": "AICAR vs differentiated myotubes",
    "palmitate_vs_differentiated": "Palmitate vs differentiated myotubes",
}

EXERCISE_ORDER = [
    "Eccentric exercise, 24 h",
    "Resistance training, 6 weeks",
    "Normal activity + exercise",
    "Reduced activity + exercise",
    "Cycling recovery",
    "MICE placebo, immediate",
    "MICE placebo, 24 h",
    "MICE OLE, immediate",
    "MICE OLE, 24 h",
    "SIE placebo, immediate",
    "SIE placebo, 24 h",
    "SIE OLE, immediate",
    "SIE OLE, 24 h",
]

OBESITY_ORDER = [
    "Obesity vs lean monocytes",
    "Post-bariatric vs pre monocytes",
    "Obesity muscle, week 52 vs 0",
    "T2D muscle, week 52 vs 0",
    "AICAR vs differentiated myotubes",
    "Palmitate vs differentiated myotubes",
]

COLORS = {
    "dark": "#272727",
    "mid": "#767676",
    "light": "#D8D8D8",
    "blue": "#0F4D92",
    "teal": "#33B5A5",
    "red": "#B64342",
    "orange": "#E28E2C",
    "violet": "#6A51A3",
}

STATUS_COLORS = {
    "FDR < 0.10": COLORS["blue"],
    "CI excludes 0": COLORS["orange"],
    "Directional": COLORS["mid"],
}

GROUP_COLORS = {
    "Exercise": COLORS["blue"],
    "Obesity / weight loss": COLORS["red"],
    "Cell model": COLORS["teal"],
    "Other": COLORS["mid"],
}

METRIC_COLORS = {
    "NAMPT_z": COLORS["blue"],
    "inflammatory_score": COLORS["red"],
    "repair_score": COLORS["teal"],
    "balance_score": COLORS["violet"],
}


def configure_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 7,
            "axes.linewidth": 0.55,
            "axes.edgecolor": COLORS["dark"],
            "axes.labelcolor": COLORS["dark"],
            "xtick.color": COLORS["dark"],
            "ytick.color": COLORS["dark"],
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    data = pd.read_csv(path)
    numeric_cols = [
        "samples",
        "axis_genes_detected",
        "axis_gene_total",
        "axis_gene_coverage_pct",
        "analysis_n",
        "paired_n",
        "analysis_n_control",
        "analysis_n_case",
        "control_n_raw",
        "case_n_raw",
        "mean_delta",
        "ci95_low",
        "ci95_high",
        "p_value",
        "q_value_metric",
        "effect_size",
    ]
    for col in numeric_cols:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")
    return data


def label_from_map(value: str, mapping: dict[str, str]) -> str:
    return mapping.get(str(value), str(value).replace("_", " "))


def add_labels(data: pd.DataFrame) -> pd.DataFrame:
    out = data.copy()
    out["dataset_label"] = out["dataset_id"].map(lambda x: label_from_map(x, DATASET_LABELS))
    out["contrast_label"] = out["contrast"].map(lambda x: label_from_map(x, CONTRAST_LABELS))
    out["metric_label"] = out["metric"].map(lambda x: label_from_map(x, METRIC_LABELS))
    out["evidence_status"] = np.select(
        [out["q_value_metric"] < 0.10, out["ci95_low"] * out["ci95_high"] > 0],
        ["FDR < 0.10", "CI excludes 0"],
        default="Directional",
    )
    return out


def module_group(value: str) -> str:
    text = str(value).lower()
    if "exercise" in text:
        return "Exercise"
    if "obesity" in text or "weight" in text:
        return "Obesity / weight loss"
    if "cell" in text:
        return "Cell model"
    return "Other"


def ci_supported(data: pd.DataFrame) -> pd.Series:
    return (data["ci95_low"] * data["ci95_high"] > 0).fillna(False)


def save_all(fig: plt.Figure, basename: str) -> None:
    FIGURE_OUT_DIR.mkdir(parents=True, exist_ok=True)
    for ext, dpi in [("svg", 300), ("pdf", 300), ("png", 300), ("tiff", 600)]:
        fig.savefig(FIGURE_OUT_DIR / f"{basename}.{ext}", dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def add_panel_label(ax: plt.Axes, label: str) -> None:
    ax.text(-0.08, 1.05, label, transform=ax.transAxes, fontsize=10, fontweight="bold", va="bottom")


def forest_plot(ax: plt.Axes, data: pd.DataFrame, metric: str, title: str, order: list[str] | None = None) -> None:
    plot_data = data[data["metric"] == metric].copy()
    if order is None:
        plot_data = plot_data.sort_values("mean_delta")
        labels = plot_data["contrast_label"].tolist()
    else:
        plot_data["contrast_label"] = pd.Categorical(plot_data["contrast_label"], categories=order, ordered=True)
        plot_data = plot_data.sort_values("contrast_label")
        labels = [label for label in order if label in set(plot_data["contrast_label"].astype(str))]

    y = np.arange(len(plot_data))
    ax.axvline(0, color="#9A9A9A", linewidth=0.7, linestyle="--", zorder=0)
    for idx, row in enumerate(plot_data.itertuples(index=False)):
        status = getattr(row, "evidence_status")
        color = STATUS_COLORS.get(status, COLORS["mid"])
        ax.hlines(idx, row.ci95_low, row.ci95_high, color=color, linewidth=1.2)
        size = 22 + 3.0 * float(row.analysis_n if pd.notna(row.analysis_n) else 1)
        marker = "X" if str(getattr(row, "analysis_design", "")).lower() == "unpaired" else "o"
        ax.scatter(row.mean_delta, idx, s=size, marker=marker, color=color, edgecolor="white", linewidth=0.5, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=7.0)
    ax.invert_yaxis()
    ax.set_xlabel("Mean within-dataset change")
    ax.set_title(title, loc="left", fontsize=8.3, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)


def heatmap_plot(ax: plt.Axes, data: pd.DataFrame, title: str, order: list[str]) -> None:
    plot_data = data.copy()
    plot_data["contrast_label"] = pd.Categorical(plot_data["contrast_label"], categories=order, ordered=True)
    pivot = plot_data.pivot_table(index="contrast_label", columns="metric", values="mean_delta", aggfunc="mean")
    pivot = pivot.reindex(order).dropna(how="all")
    pivot = pivot.reindex(columns=METRIC_ORDER)
    values = pivot.to_numpy(dtype=float)
    finite = values[np.isfinite(values)]
    vmax = max(abs(float(np.nanmin(finite))), abs(float(np.nanmax(finite)))) if finite.size else 1.0
    image = ax.imshow(values, aspect="auto", cmap="RdBu_r", vmin=-vmax, vmax=vmax)
    ax.set_xticks(np.arange(len(METRIC_ORDER)))
    ax.set_xticklabels([METRIC_LABELS[m] for m in METRIC_ORDER], rotation=35, ha="right", fontsize=7.0)
    ax.set_yticks(np.arange(len(pivot.index)))
    ax.set_yticklabels([str(x) for x in pivot.index], fontsize=7.0)
    ax.set_title(title, loc="left", fontsize=8.3, fontweight="bold")

    fdr = plot_data[plot_data["q_value_metric"] < 0.10]
    row_lookup = {label: idx for idx, label in enumerate(pivot.index)}
    col_lookup = {metric: idx for idx, metric in enumerate(METRIC_ORDER)}
    for row in fdr.itertuples(index=False):
        r = row_lookup.get(getattr(row, "contrast_label"))
        c = col_lookup.get(row.metric)
        if r is not None and c is not None:
            ax.scatter(c, r, s=18, facecolor="white", edgecolor=COLORS["dark"], linewidth=0.45)
    ax.spines[:].set_visible(False)
    return image


def plot_figure2(coverage: pd.DataFrame, stats_all: pd.DataFrame) -> None:
    data = coverage.copy()
    data["dataset_label"] = data["dataset_id"].map(lambda x: label_from_map(x, DATASET_LABELS))
    data["module_group"] = data["module"].map(module_group)
    data = data.sort_values(["module_group", "axis_gene_coverage_pct", "dataset_id"], ascending=[True, True, True])

    fig = plt.figure(figsize=(7.2, 4.65))
    grid = fig.add_gridspec(2, 2, width_ratios=[1.45, 1.0], height_ratios=[1.0, 1.0], wspace=0.48, hspace=0.75)
    ax_a = fig.add_subplot(grid[:, 0])
    ax_b = fig.add_subplot(grid[0, 1])
    ax_c = fig.add_subplot(grid[1, 1])

    y = np.arange(len(data))
    ax_a.hlines(y, 0, data["axis_gene_coverage_pct"], color=COLORS["light"], linewidth=0.9)
    sizes = 24 + data["samples"].fillna(1).to_numpy(dtype=float) * 1.2
    colors = data["module_group"].map(GROUP_COLORS).fillna(COLORS["mid"])
    ax_a.scatter(data["axis_gene_coverage_pct"], y, s=sizes, color=colors, edgecolor="white", linewidth=0.5)
    ax_a.set_yticks(y)
    ax_a.set_yticklabels(data["dataset_label"], fontsize=7.0)
    ax_a.set_xlim(0, 105)
    ax_a.set_xlabel("NAMPT-axis gene coverage")
    ax_a.set_title("Public transcriptomic evidence base", loc="left", fontsize=8.4, fontweight="bold")
    ax_a.spines[["top", "right"]].set_visible(False)
    add_panel_label(ax_a, "a")

    design = stats_all[["dataset_id", "contrast", "analysis_design", "analysis_n"]].drop_duplicates().copy()
    design["design_group"] = np.where(design["analysis_design"].str.startswith("paired"), "Paired/intersection", "Unpaired")
    counts = design["design_group"].value_counts().reindex(["Paired/intersection", "Unpaired"]).fillna(0)
    ax_b.bar(counts.index, counts.values, color=[COLORS["blue"], COLORS["mid"]], width=0.6)
    for idx, value in enumerate(counts.values):
        ax_b.text(idx, value + 0.25, str(int(value)), ha="center", fontsize=7)
    ax_b.set_ylabel("Contrasts")
    ax_b.set_title("Analysis design", loc="left", fontsize=8.4, fontweight="bold")
    ax_b.tick_params(axis="x", rotation=20)
    ax_b.spines[["top", "right"]].set_visible(False)
    add_panel_label(ax_b, "b")

    evidence = stats_all.copy()
    evidence["ci_supported"] = ci_supported(evidence)
    evidence["fdr_supported"] = evidence["q_value_metric"] < 0.10
    x = np.arange(len(METRIC_ORDER))
    ci_counts = evidence.groupby("metric")["ci_supported"].sum().reindex(METRIC_ORDER).fillna(0)
    fdr_counts = evidence.groupby("metric")["fdr_supported"].sum().reindex(METRIC_ORDER).fillna(0)
    ax_c.bar(x - 0.18, ci_counts.values, width=0.34, color=COLORS["orange"], label="CI excludes 0")
    ax_c.bar(x + 0.18, fdr_counts.values, width=0.34, color=COLORS["blue"], label="FDR < 0.10")
    ax_c.set_xticks(x)
    ax_c.set_xticklabels([METRIC_LABELS[m] for m in METRIC_ORDER], rotation=30, ha="right", fontsize=7.0)
    ax_c.set_ylabel("Contrasts")
    ax_c.set_title("Evidence density by axis metric", loc="left", fontsize=8.4, fontweight="bold")
    ax_c.legend(frameon=False, fontsize=7.0, loc="upper right")
    ax_c.spines[["top", "right"]].set_visible(False)
    add_panel_label(ax_c, "c")

    group_handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor=color, markeredgecolor="white", markersize=6, label=label)
        for label, color in GROUP_COLORS.items()
    ]
    ax_a.legend(handles=group_handles, frameon=False, fontsize=7.0, loc="lower right")
    save_all(fig, "figure2_public_data_framework")


def plot_figure3(exercise: pd.DataFrame) -> None:
    data = add_labels(exercise)
    fig = plt.figure(figsize=(7.2, 6.0))
    grid = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.12], width_ratios=[1.35, 1.0], hspace=0.6, wspace=0.55)
    ax_a = fig.add_subplot(grid[0, 0])
    ax_b = fig.add_subplot(grid[0, 1])
    ax_c = fig.add_subplot(grid[1, :])

    forest_plot(ax_a, data, "NAMPT_z", "Exercise-associated NAMPT induction", EXERCISE_ORDER)
    add_panel_label(ax_a, "a")

    balance = data[(data["dataset_id"] == "GSE318937_exercise_oleuropein") & (data["metric"] == "balance_score")].copy()
    balance["timepoint"] = np.where(balance["contrast"].str.contains("24h"), "24 h", "Immediate")
    balance["time_x"] = balance["timepoint"].map({"Immediate": 0, "24 h": 1})
    balance["exercise_mode"] = np.where(balance["contrast"].str.contains("MICE"), "MICE", "SIE")
    balance["treatment"] = np.where(balance["contrast"].str.contains("active"), "OLE", "Placebo")
    for (mode, treatment), group in balance.groupby(["exercise_mode", "treatment"]):
        group = group.sort_values("time_x")
        color = COLORS["blue"] if mode == "MICE" else COLORS["red"]
        linestyle = "-" if treatment == "OLE" else "--"
        ax_b.plot(group["time_x"], group["mean_delta"], color=color, linestyle=linestyle, linewidth=1.15, label=f"{mode} + {treatment}")
        ax_b.errorbar(
            group["time_x"],
            group["mean_delta"],
            yerr=[group["mean_delta"] - group["ci95_low"], group["ci95_high"] - group["mean_delta"]],
            fmt="o",
            color=color,
            markersize=4,
            capsize=2,
            linewidth=0.8,
        )
    ax_b.axhline(0, color="#9A9A9A", linewidth=0.7, linestyle="--")
    ax_b.set_xticks([0, 1])
    ax_b.set_xticklabels(["Immediate", "24 h"])
    ax_b.set_ylabel("Balance-score delta")
    ax_b.set_title("Immediate stress bias relaxes by 24 h", loc="left", fontsize=8.3, fontweight="bold")
    ax_b.legend(frameon=False, fontsize=7.0)
    ax_b.spines[["top", "right"]].set_visible(False)
    add_panel_label(ax_b, "b")

    image = heatmap_plot(ax_c, data, "Exercise reshapes inflammatory and repair programs", EXERCISE_ORDER)
    add_panel_label(ax_c, "c")
    cbar = fig.colorbar(image, ax=ax_c, fraction=0.025, pad=0.02)
    cbar.set_label("Mean delta")

    save_all(fig, "figure3_exercise_nampt_axis")


def plot_figure4(obesity: pd.DataFrame) -> None:
    data = add_labels(obesity)
    fig = plt.figure(figsize=(7.2, 5.65))
    grid = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.12], width_ratios=[1.32, 1.0], hspace=0.6, wspace=0.55)
    ax_a = fig.add_subplot(grid[0, 0])
    ax_b = fig.add_subplot(grid[0, 1])
    ax_c = fig.add_subplot(grid[1, :])

    forest_plot(ax_a, data, "NAMPT_z", "Obesity and metabolic stress alter NAMPT expression", OBESITY_ORDER)
    add_panel_label(ax_a, "a")

    monocyte = data[(data["dataset_id"] == "GSE32575_monocytes_obesity_surgery") & (data["contrast"] == "obese_after_vs_obese_before")].copy()
    monocyte["metric"] = pd.Categorical(monocyte["metric"], categories=METRIC_ORDER, ordered=True)
    monocyte = monocyte.sort_values("metric")
    x = np.arange(len(monocyte))
    ax_b.axhline(0, color="#9A9A9A", linewidth=0.7, linestyle="--")
    for idx, row in enumerate(monocyte.itertuples(index=False)):
        color = METRIC_COLORS.get(row.metric, COLORS["mid"])
        ax_b.vlines(idx, row.ci95_low, row.ci95_high, color=color, linewidth=1.25)
        ax_b.scatter(idx, row.mean_delta, color=color, edgecolor="white", linewidth=0.5, s=42)
    ax_b.set_xticks(x)
    ax_b.set_xticklabels([METRIC_LABELS[str(m)].replace("\n", " ") for m in monocyte["metric"]], rotation=28, ha="right", fontsize=7.0)
    ax_b.set_ylabel("Post vs pre mean delta")
    ax_b.set_title("Post-bariatric monocyte remodeling", loc="left", fontsize=8.3, fontweight="bold")
    ax_b.spines[["top", "right"]].set_visible(False)
    add_panel_label(ax_b, "b")

    image = heatmap_plot(ax_c, data, "Obesity-linked states show heterogeneous axis remodeling", OBESITY_ORDER)
    add_panel_label(ax_c, "c")
    cbar = fig.colorbar(image, ax=ax_c, fraction=0.025, pad=0.02)
    cbar.set_label("Mean delta")

    save_all(fig, "figure4_obesity_nampt_axis")


def main() -> None:
    configure_style()
    coverage = read_csv(FIGURE2_PATH)
    exercise = read_csv(FIGURE3_PATH)
    obesity = read_csv(FIGURE4_PATH)
    stats_all = read_csv(FORMAL_STATS_PATH)
    plot_figure2(coverage, stats_all)
    plot_figure3(exercise)
    plot_figure4(obesity)
    print(f"Finished exporting fallback Python figures to: {FIGURE_OUT_DIR}")


if __name__ == "__main__":
    main()
