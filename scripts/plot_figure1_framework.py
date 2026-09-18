#!/usr/bin/env python3
"""Figure 1 - conceptual framework for the NAMPT-NAD inflammatory-repair axis.

Panel A: NAMPT dual identity (intracellular iNAMPT vs extracellular eNAMPT/
visfatin/PBEF) and the two measurable programs.
Panel B: the state-dependent axis: chronic metabolic stress / obesity loads
the inflammatory program; exercise adaptation drives the repair program.
Panel C: the multi-layer evidence design: public transcriptomic axis scores
-> state-dependent contrasts -> Evo2-40B regulatory-variant prioritization.

Outputs (4 formats):
  data_audit/outputs/figures_phase2/figure1_framework.{pdf,svg,png,tiff}
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data_audit" / "outputs" / "figures_phase2"
OUT.mkdir(parents=True, exist_ok=True)

# palette (colorblind-friendly)
C_REPAIR = "#2c7fb8"    # blue  - repair program
C_INFLAM = "#d95f0e"    # orange - inflammatory program
C_NAMPT = "#756bb1"     # purple - NAMPT focal
C_GREY = "#636363"
C_EVO = "#31a354"       # green - Evo2 layer


def box(ax, x, y, w, h, text, fc, ec="none", fs=9, tc="white", lw=1.0, style="round,pad=0.02"):
    b = FancyBboxPatch((x, y), w, h, boxstyle=style,
                       linewidth=lw, edgecolor=ec, facecolor=fc)
    ax.add_patch(b)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=tc, fontweight="bold", wrap=True)


def arrow(ax, x1, y1, x2, y2, color=C_GREY, lw=1.6, style="-|>", ls="-"):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                        mutation_scale=14, linewidth=lw, color=color,
                        linestyle=ls, zorder=5)
    ax.add_patch(a)


def main() -> None:
    fig = plt.figure(figsize=(12.5, 7.0))
    gs = fig.add_gridspec(2, 3, height_ratios=[1.0, 0.78], hspace=0.32, wspace=0.30)

    # ---------------- Panel A (top-left): dual identity ----------------
    axA = fig.add_subplot(gs[0, 0])
    axA.set_xlim(0, 10); axA.set_ylim(0, 10); axA.axis("off")
    axA.set_title("a  NAMPT dual identity", fontsize=11, fontweight="bold", loc="left")

    # central NAMPT
    box(axA, 3.1, 4.3, 3.8, 1.4, "NAMPT\n(visfatin / PBEF)",
        C_NAMPT, fs=10)
    # iNAMPT arm
    box(axA, 0.2, 6.6, 4.4, 1.3, "iNAMPT (intracellular)\nNAD salvage + SIRT/AMPK/PGC1A\nmitochondria / DNA repair",
        C_REPAIR, fs=8)
    arrow(axA, 3.1, 5.7, 2.4, 6.6, C_REPAIR)
    # eNAMPT arm
    box(axA, 0.2, 2.1, 4.4, 1.3, "eNAMPT (extracellular)\nNF-κB / IL6 / TNF / CCL2\nmonocyte-macrophage stress",
        C_INFLAM, fs=8)
    arrow(axA, 3.1, 4.3, 2.4, 3.4, C_INFLAM)
    # two programs
    box(axA, 5.8, 6.6, 4.0, 1.3, "REPAIR program\n'adaptive metabolic state'", C_REPAIR, fs=8)
    box(axA, 5.8, 2.1, 4.0, 1.3, "INFLAMMATORY program\n'metabolic-immune stress'", C_INFLAM, fs=8)
    arrow(axA, 6.9, 5.7, 7.8, 6.6, C_REPAIR)
    arrow(axA, 6.9, 4.3, 7.8, 3.4, C_INFLAM)
    # key question
    axA.text(5.0, 0.6, "Key question: when does NAMPT signal\nrepair vs. inflammatory load?",
             ha="center", va="center", fontsize=9, style="italic", color=C_GREY)

    # ---------------- Panel B (top-middle): state-dependent axis ----------------
    axB = fig.add_subplot(gs[0, 1])
    axB.set_xlim(0, 10); axB.set_ylim(0, 10); axB.axis("off")
    axB.set_title("b  State-dependent axis", fontsize=11, fontweight="bold", loc="left")

    # horizontal axis
    arrow(axB, 0.6, 5.0, 9.4, 5.0, C_GREY, lw=2.2)
    axB.text(0.8, 5.3, "Obesity / chronic metabolic stress", fontsize=9, color=C_INFLAM)
    axB.text(6.2, 5.3, "Exercise training / adaptation", fontsize=9, color=C_REPAIR)
    # axis markers
    for x, lab in [(2.5, "eNAMPT-immune load\nCD38 / PARP / NF-κB"),
                   (5.5, "transition\nstate"),
                   (8.0, "NAD salvage + repair\nSIRT1/3 / AMPK / PGC1A")]:
        axB.plot([x, x], [4.7, 5.3], color=C_GREY, lw=1.0)
        axB.text(x, 3.2, lab, ha="center", va="top", fontsize=8, color=C_GREY)
    box(axB, 0.3, 7.2, 3.4, 1.4, "Chronic low-grade\ninflammation", C_INFLAM, fs=9)
    box(axB, 6.3, 7.2, 3.4, 1.4, "Adaptive repair /\nmitochondrial remodelling", C_REPAIR, fs=9)
    axB.text(5.0, 0.5, "The same gene set, different states\n-> balance_score flips direction",
             ha="center", va="center", fontsize=9, style="italic", color=C_GREY)

    # ---------------- Panel C (top-right): evidence ladder ----------------
    axC = fig.add_subplot(gs[0, 2])
    axC.set_xlim(0, 10); axC.set_ylim(0, 10); axC.axis("off")
    axC.set_title("c  Multi-layer public-data evidence", fontsize=11, fontweight="bold", loc="left")

    layers = [
        ("Public GEO expression", "9 matrices / 346 samples", C_REPAIR),
        ("NAMPT-axis scores", "59-gene axis: NAMPT_z, infl, repair, balance", C_NAMPT),
        ("State contrasts + meta", "19 paired contrasts, random-effects meta", C_REPAIR),
        ("Evo2-40B regulatory variants", "ref/alt allele surprisal -> Tier A/B/C", C_EVO),
    ]
    y = 8.2
    for title, sub, color in layers:
        box(axC, 0.4, y, 9.2, 1.35, f"{title}\n{sub}", color, fs=8.5)
        y -= 2.0
        if y > 1.0:
            arrow(axC, 5.0, y + 1.55, 5.0, y + 2.05, C_GREY, lw=1.4)

    # ---------------- Panel D (bottom-left): repair program box ----------------
    axD = fig.add_subplot(gs[1, 0])
    axD.set_xlim(0, 10); axD.set_ylim(0, 10); axD.axis("off")
    axD.set_title("d  Repair program (transcript evidence)", fontsize=10, fontweight="bold", loc="left")
    repair_genes = "NAMPT  NMNAT1/2/3  NAPRT  NADSYN1\nSIRT1  SIRT3  SIRT6  PRKAA1/2\nPPARGC1A  TFAM  NRF1  SOD2\nCAT  GPX1  ATG5  BECN1  XRCC1"
    axD.text(0.4, 5.0, repair_genes, fontsize=8.5, family="monospace",
             va="center", color=C_REPAIR)
    axD.text(5.2, 8.6, "co-expression support:", fontsize=9, color=C_GREY)
    axD.text(5.2, 7.6, "GSE272133 repair modules α = 0.79-0.91", fontsize=8.5, color=C_REPAIR)
    axD.text(5.2, 6.6, "GSE305038 α mean 0.78; GSE32575 α mean 0.61", fontsize=8.5, color=C_REPAIR)

    # ---------------- Panel E (bottom-middle): inflammatory program box ----------------
    axE = fig.add_subplot(gs[1, 1])
    axE.set_xlim(0, 10); axE.set_ylim(0, 10); axE.axis("off")
    axE.set_title("e  Inflammatory program (transcript evidence)", fontsize=10, fontweight="bold", loc="left")
    inflam_genes = "NAMPT  CD38  BST1  PARP1/2\nNFKB1  RELA  TNF  IL6  IL1B\nCCL2  CXCL8  TLR4  NLRP3\nCASP1  CD14  CD68  ITGAM"
    axE.text(0.4, 5.0, inflam_genes, fontsize=8.5, family="monospace",
             va="center", color=C_INFLAM)
    axE.text(5.2, 8.6, "state evidence:", fontsize=9, color=C_GREY)
    axE.text(5.2, 7.6, "acute exercise: NAMPT_z +0.85 (92% agree)", fontsize=8.5, color=C_INFLAM)
    axE.text(5.2, 6.6, "balance -0.62 (83%); NF-κB-module sensitive", fontsize=8.5, color=C_INFLAM)

    # ---------------- Panel F (bottom-right): balance summary ----------------
    axF = fig.add_subplot(gs[1, 2])
    axF.set_xlim(0, 10); axF.set_ylim(0, 10); axF.axis("off")
    axF.set_title("f  Balance score across states", fontsize=10, fontweight="bold", loc="left")

    states = [
        ("Acute exercise (k=12)", -0.62, C_INFLAM),
        ("Obesity (k=3)", -0.10, C_GREY),
        ("Cell model (k=2)", -0.07, C_GREY),
        ("6-wk training (n=3)", 0.27, C_REPAIR),
    ]
    y = 8.4
    for name, val, col in states:
        axF.text(0.4, y, name, fontsize=8.5, color=C_GREY, va="center")
        # bar
        x0 = 4.5
        width = abs(val) * 1.6
        x_lo = x0 if val >= 0 else x0 - width
        axF.add_patch(plt.Rectangle((x_lo, y - 0.28), width, 0.56,
                                    facecolor=col, edgecolor="none", alpha=0.85))
        axF.text(x0 + (0.1 if val >= 0 else -0.1), y, f"{val:+.2f}",
                 fontsize=8.5, color=C_GREY, va="center",
                 ha="left" if val >= 0 else "right")
        y -= 1.6
    axF.text(4.5, 1.1, "repair-negative <- balance -> repair-positive", fontsize=8,
             color=C_GREY, ha="center")

    fig.suptitle("State-dependent NAMPT-NAD inflammatory-repair axis in obesity and exercise adaptation",
                 fontsize=13, fontweight="bold", y=0.98)

    for ext in ["pdf", "svg", "png", "tiff"]:
        path = OUT / f"figure1_framework.{ext}"
        fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
        print(f"wrote {path}")
    plt.close(fig)


if __name__ == "__main__":
    main()