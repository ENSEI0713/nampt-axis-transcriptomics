#!/usr/bin/env python3
"""Figure 5 - Evo2-40B regulatory-variant prioritization pipeline.

Panel a: workflow from public genetic resources through candidate
collection (Ensembl/dbSNP), GRCh38 ref/alt window construction, Evo2-40B
allele-surprisal scoring, to multi-evidence Tier A/B/C assignment.
Panel b: composition of the current candidate set (432 functional variants
by gene window and by consequence class).

Note: actual Evo2 scores are pending the NVIDIA API key; this figure shows
the pipeline and candidate composition, and will be updated with a scored
variant panel once run_evo2_scoring.py has been executed.

Outputs:
  data_audit/outputs/figures_phase2/figure5_evo2_prioritization.{pdf,svg,png,tiff}
"""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data_audit" / "outputs"
CAND_CSV = OUT_DIR / "evo2" / "candidates_priority.csv"
FIG_OUT = OUT_DIR / "figures_phase2"
FIG_OUT.mkdir(parents=True, exist_ok=True)

C_EVO = "#31a354"
C_NAMPT = "#756bb1"
C_GREY = "#636363"
C_BLUE = "#2c7fb8"


def save_all(fig: plt.Figure, basename: str) -> None:
    for ext in ["pdf", "svg", "png", "tiff"]:
        fig.savefig(FIG_OUT / f"{basename}.{ext}", dpi=300, bbox_inches="tight", facecolor="white")


def box(ax, x, y, w, h, text, fc, fs=8.5, tc="white", ec="none"):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02", lw=1.0,
                       edgecolor=ec, facecolor=fc)
    ax.add_patch(b)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=tc, fontweight="bold")


def arrow(ax, x1, y1, x2, y2, color="#9A9A9A", lw=1.4):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=12, linewidth=lw, color=color, zorder=5))


def main() -> None:
    fig = plt.figure(figsize=(11.5, 5.0))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 0.9], wspace=0.35)

    # ---------- Panel a: workflow ----------
    axA = fig.add_subplot(gs[0])
    axA.set_xlim(0, 10); axA.set_ylim(0, 10); axA.axis("off")
    axA.set_title("a  Prioritization workflow", fontsize=11, fontweight="bold", loc="left")

    steps = [
        (0.5, 8.0, "Public genetic evidence\nGWAS / eQTL / ClinVar / dbSNP"),
        (0.5, 5.4, "Cis-window candidates\nNAMPT-axis gene ±2 kb promoter"),
        (0.5, 2.8, "GRCh38 ref/alt windows\n2 kb (ref + alt) per variant"),
    ]
    for x, y, t in steps:
        box(axA, x, y, 4.3, 1.7, t, C_BLUE, fs=8)
    # Evo2 scoring
    box(axA, 5.6, 5.4, 4.0, 1.7, "Evo2-40B\nallele surprisal\n(ref vs alt)", C_EVO, fs=8)
    # Tier assignment
    box(axA, 5.6, 2.8, 4.0, 1.7, "Evidence tiers\nA: Evo2 + eQTL + trait + reg.\nB: Evo2 + 2 evidence types\nC: exploratory only", C_NAMPT, fs=7.2)

    arrow(axA, 2.65, 8.0, 2.65, 7.1)
    arrow(axA, 2.65, 5.4, 2.65, 4.5)
    arrow(axA, 4.8, 6.25, 5.6, 6.25)
    arrow(axA, 7.6, 5.4, 7.6, 4.5)

    axA.text(0.5, 1.2, "Output: compact Tier A/B/C candidate list for\nMPRA / CRISPRi / reporter validation",
             fontsize=8.5, style="italic", color=C_GREY)

    # ---------- Panel b: candidate composition ----------
    axB = fig.add_subplot(gs[1])
    axB.set_title("b  Candidate set composition (n = 432)", fontsize=11, fontweight="bold", loc="left")
    rows = list(csv.DictReader(open(CAND_CSV, encoding="utf-8-sig")))
    by_gene = Counter(r["gene_window"] for r in rows)
    genes = [g for g, _ in by_gene.most_common()]
    counts = [by_gene[g] for g in genes]

    axB.barh(genes[::-1], counts[::-1], color=C_NAMPT, alpha=0.9)
    axB.set_xlabel("Priority variants")
    for i, (g, c) in enumerate(zip(genes[::-1], counts[::-1])):
        axB.text(c + 2, i, str(c), va="center", fontsize=8, color=C_GREY)
    axB.spines[["top", "right"]].set_visible(False)

    fig.suptitle("Evo2-40B regulatory-variant prioritization for the NAMPT-NAD axis",
                 fontsize=12, fontweight="bold", y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    save_all(fig, "figure5_evo2_prioritization")
    print("wrote figure5_evo2_prioritization")


if __name__ == "__main__":
    main()