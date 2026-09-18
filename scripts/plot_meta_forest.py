#!/usr/bin/env python3
"""Forest plot of the NAMPT-axis random-effects meta-analysis.

Reads data_audit/outputs/meta/meta_results.csv and draws pooled effect
(95% CI) for each domain x metric stratum, plus per-contrast effect rows
for the exercise/NAMPT_z stratum as a classic forest panel.

Outputs:
  data_audit/outputs/figures_phase2/figure3_meta_forest.{pdf,svg,png,tiff}
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data_audit" / "outputs"
META_CSV = OUT_DIR / "meta" / "meta_results.csv"
INPUT_CSV = OUT_DIR / "meta" / "meta_input_contrasts.csv"
FIG_OUT = OUT_DIR / "figures_phase2"
FIG_OUT.mkdir(parents=True, exist_ok=True)

METRIC_LABELS = {
    "NAMPT_z": "NAMPT_z",
    "inflammatory_score": "Inflammatory",
    "repair_score": "Repair / metabolic",
    "balance_score": "Balance",
}
DOMAIN_LABELS = {
    "exercise": "Exercise",
    "obesity": "Obesity",
    "obesity_cell_model": "Cell model",
}


def save_all(fig: plt.Figure, basename: str) -> None:
    for ext in ["pdf", "svg", "png", "tiff"]:
        fig.savefig(FIG_OUT / f"{basename}.{ext}", dpi=300, bbox_inches="tight", facecolor="white")


def main() -> None:
    meta = pd.read_csv(META_CSV)
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 5.2), gridspec_kw={"width_ratios": [1.0, 1.25]})

    # ---- left: pooled effect by stratum ----
    ax = axes[0]
    rows = []
    for _, r in meta.iterrows():
        rows.append({
            "label": f"{DOMAIN_LABELS.get(r['domain'], r['domain'])} · {METRIC_LABELS.get(r['metric'], r['metric'])}",
            "est": r["pooled_effect"], "lo": r["ci95_low"], "hi": r["ci95_high"],
            "p": r["p_value"], "k": int(r["k"]), "i2": r["I2_pct"],
        })
    rows.sort(key=lambda x: x["est"], reverse=True)
    y = 0
    for row in rows:
        ax.plot([row["lo"], row["hi"]], [y, y], color="#636363", lw=1.6, zorder=3)
        ax.plot(row["est"], y, marker="D", markersize=6.5, color="#2c7fb8", zorder=4)
        ax.axvline(0, color="#9A9A9A", lw=0.8, ls="--", zorder=1)
        ax.text(row["hi"] + 0.08, y,
                f"{row['est']:+.2f} [{row['lo']:+.2f}, {row['hi']:+.2f}]\n"
                f"k={row['k']} · I²={row['i2']:.0f}% · p={row['p']:.1e}" if row["p"] < 0.05 else
                f"{row['est']:+.2f} [{row['lo']:+.2f}, {row['hi']:+.2f}]\n"
                f"k={row['k']} · I²={row['i2']:.0f}% · p={row['p']:.2f}",
                va="center", fontsize=7.3)
        y += 1.0
    ax.set_yticks([])
    ax.set_ylim(-0.6, y - 0.4)
    ax.set_xlabel("Pooled effect (within-dataset standardized delta)")
    ax.set_title("Random-effects meta-analysis by stratum", fontsize=10, fontweight="bold", loc="left")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.set_yticklabels([])

    # ---- right: forest per contrast for exercise/NAMPT_z ----
    ax2 = axes[1]
    inp = pd.read_csv(INPUT_CSV)
    ex_nampt = inp[(inp["domain"] == "exercise") & (inp["metric"] == "NAMPT_z")].copy()
    ex_nampt = ex_nampt.sort_values("effect_size")
    ys = list(range(len(ex_nampt)))
    for yi, (_, r) in zip(ys, ex_nampt.iterrows()):
        ci_lo = r["effect_size"] - 1.96 * r["se"]
        ci_hi = r["effect_size"] + 1.96 * r["se"]
        ax2.plot([ci_lo, ci_hi], [yi, yi], color="#9A9A9A", lw=1.2, zorder=3)
        ax2.plot(r["effect_size"], yi, marker="o", markersize=5, color="#d95f0e", zorder=4)
    ax2.axvline(0, color="#9A9A9A", lw=0.8, ls="--", zorder=1)
    # pooled diamond at top
    meta_ex = meta[(meta["domain"] == "exercise") & (meta["metric"] == "NAMPT_z")].iloc[0]
    pool_y = len(ex_nampt)
    ax2.plot([meta_ex["ci95_low"], meta_ex["ci95_high"]], [pool_y, pool_y], color="#2c7fb8", lw=3)
    ax2.plot(meta_ex["pooled_effect"], pool_y, marker="D", color="#2c7fb8", markersize=9)
    ax2.text(meta_ex["ci95_high"] + 0.1, pool_y,
             f"POOLED {meta_ex['pooled_effect']:+.2f} (p={meta_ex['p_value']:.1e})",
             fontsize=7.5, fontweight="bold", color="#2c7fb8", va="center")
    labels = [f"{r['dataset_id'].split('_')[0]}: {r['contrast'][:26]}" for _, r in ex_nampt.iterrows()]
    labels.append("Random-effects pooled")
    ax2.set_yticks(list(ys) + [pool_y])
    ax2.set_yticklabels(labels, fontsize=6.8)
    ax2.set_ylim(-0.8, pool_y + 0.8)
    ax2.set_xlabel("Effect size (Cohen dz)")
    ax2.set_title("Exercise / NAMPT_z: per-contrast forest", fontsize=10, fontweight="bold", loc="left")
    ax2.spines[["top", "right"]].set_visible(False)

    fig.suptitle("NAMPT-axis random-effects meta-analysis", fontsize=12, fontweight="bold", y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    save_all(fig, "figure3_meta_forest")
    print("wrote figure3_meta_forest")


if __name__ == "__main__":
    main()