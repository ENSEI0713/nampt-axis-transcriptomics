#!/usr/bin/env python3
"""NAMPT-axis internal immune-gene burden sensitivity.

NOTE: the saved axis expression matrices contain only the 59 NAMPT-axis genes,
so this is NOT a cell-type deconvolution. It measures how much of each NAMPT-axis
score is carried by the axis-internal immune/macrophage genes, i.e. a burden
proxy. Use it to qualify interpretations, never as composition adjustment.

The 59-gene axis set already contains several immune/macrophage genes
(CD14, CD68, ITGAM, MRC1, TLR4, TNF, IL6, CCL2, ...). This script averages
the detected subset of a marker list per sample to form a burden proxy, and
then reports the within-dataset correlation between each axis score and that
proxy. High correlation flags that the axis score is heavily carried by its
own immune genes, which must be disclosed.

Outputs:
  data_audit/outputs/cell_composition/cell_scores.csv
  data_audit/outputs/cell_composition/sensitivity_report.md
"""
from __future__ import annotations

import csv
import glob
import os
from datetime import datetime, timezone

import numpy as np

BASE = os.path.join(os.path.dirname(__file__), "..", "data_audit", "outputs")
EXPR_DIR = os.path.join(BASE, "nampt_axis_expression")
OUT_DIR = os.path.join(BASE, "cell_composition")
SCORES_CSV = os.path.join(BASE, "nampt_axis_sample_scores.csv")

# Public, tissue-agnostic marker genes (symbols upper-cased) for common
# immune / structural compartments. Keep short, high-confidence genes.
MARKER_SETS = {
    "immune_pan_leukocyte": ["PTPRC", "CD3D", "CD3E", "CD8A", "CD4", "CD19", "NKG7",
                             "CD68", "ITGAM", "FCGR3A", "MS4A1", "LYZ", "CXCR2"],
    "macrophage_monocyte": ["CD14", "CD68", "ITGAM", "MRC1", "FCGR3A", "LYZ",
                            "CSF1R", "TLR4", "CD86", "TNF"],
    "t_cell": ["CD3D", "CD3E", "CD8A", "CD4", "TRAC", "CD2"],
    "blood_erythroid": ["HBB", "HBA1", "HBA2", "ALAS2", "GYP", "GYPA"],
    "fibroblast_stroma": ["COL1A1", "COL1A2", "COL3A1", "DCN", "LUM", "VIM"],
    "adipocyte": ["ADIPOQ", "LEP", "PLIN1", "FABP4", "PPARG", "ADRB3", "LPL"],
    "skeletal_muscle_fiber": ["MYH7", "MYH1", "MYH2", "MYH4", "ACTA1", "TNNC1",
                              "TNNT3", "ATP2A1", "MB"],
}


def marker_set_for(source_marker: list[str]) -> set[str]:
    return {g.upper() for g in source_marker}


def ssgsea_score(genes: list[str], X: np.ndarray, marker: set[str]) -> np.ndarray:
    """Per-sample mean z-score of detected marker genes (inflitrate proxy).

    X is a 1-D array of gene expression for one sample (genes aligned to `genes`).
    """
    idx = [i for i, g in enumerate(genes) if g.upper() in marker]
    if not idx:
        return np.nan
    vals = X[idx]
    return float(np.mean(vals))


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)

    # Load per-sample scores to align
    with open(SCORES_CSV, newline="", encoding="utf-8-sig") as f:
        score_rows = list(csv.DictReader(f))
    score_idx = {(r["dataset_id"], r["sample_id"]): r for r in score_rows}

    out = []
    files = sorted(glob.glob(os.path.join(EXPR_DIR, "*_axis_expression.csv")))
    for path in files:
        ds = os.path.basename(path).replace("_axis_expression.csv", "")
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            header = next(reader)
            genes = []
            rows = []
            samples = header[5:]
            for row in reader:
                if not row or not row[0]:
                    continue
                genes.append(row[0])
                rows.append([float(x) for x in row[5:]])
        if not rows:
            continue
        X = np.array(rows)  # genes x samples
        for si, s in enumerate(samples):
            idx_key = (ds, s)
            score = score_idx.get(idx_key)
            if score is None:
                continue
            cell = {"dataset_id": ds, "sample_id": s}
            for name, marker in MARKER_SETS.items():
                cell[name] = ssgsea_score(genes, X[:, si], marker)
            # store the axis baseline scores to allow correlation
            cell["NAMPT_z"] = float(score["NAMPT_z"])
            cell["inflammatory_score"] = float(score["inflammatory_score"])
            cell["repair_score"] = float(score["repair_score"])
            cell["balance_score"] = float(score["balance_score"])
            out.append(cell)

    # Write cell scores CSV
    os.makedirs(OUT_DIR, exist_ok=True)
    fields = ["dataset_id", "sample_id", "NAMPT_z", "inflammatory_score",
              "repair_score", "balance_score"] + list(MARKER_SETS.keys())
    with open(os.path.join(OUT_DIR, "cell_scores.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in out:
            # keep only finite values
            w.writerow({k: r.get(k) for k in fields})

    # ---- Correlation of NAMPT axis scores with immune marker proxy ----
    lines = ["# NAMPT-axis internal immune-gene burden sensitivity", ""]
    lines.append(f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    lines.append("")
    lines.append("IMPORTANT SCOPE: the saved axis expression matrices contain only the")
    lines.append("59 NAMPT-axis genes. This is NOT a cell-type deconvolution. The 'immune'")
    lines.append("and 'macro/mono' columns are the within-axis immune-gene burden proxy")
    lines.append("(mean z of axis genes that also appear in the marker list), not an")
    lines.append("estimate of leukocyte abundance. Columns that are empty ('—') mean the")
    lines.append("marker genes are not present in the 59-gene axis matrix.")
    lines.append("")
    lines.append("Correlation between each NAMPT-axis score and the axis-internal immune")
    lines.append("burden proxy across samples within dataset. High positive r for")
    lines.append("inflammatory_score indicates that the inflammatory program is largely")
    lines.append("carried by its own immune genes in that dataset; this qualifies (but")
    lines.append("does not replace) interpretation, and must be disclosed in the paper.")
    lines.append("")
    lines.append("## Pearson r (axis score vs axis-internal immune burden proxy), by dataset")
    lines.append("")
    lines.append("| dataset | n | metric | immune_pan | macro/mono | adipocyte |")
    lines.append("|---|---|---|---|---|---|")
    for ds in sorted({r["dataset_id"] for r in out}):
        ds_rows = [r for r in out if r["dataset_id"] == ds]
        for metric in ["NAMPT_z", "inflammatory_score", "repair_score", "balance_score"]:
            y = _vec(ds_rows, metric)
            row = [ds, str(len(ds_rows)), metric]
            for mname in ["immune_pan_leukocyte", "macrophage_monocyte", "adipocyte"]:
                x = _vec(ds_rows, mname)
                r = _pearson(y, x)
                row.append(_fmt(r))
            lines.append("| " + " | ".join(row) + " |")
        lines.append("")

    with open(os.path.join(OUT_DIR, "sensitivity_report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Wrote {len(out)} cell-adjusted score rows to {OUT_DIR}")
    print(f"datasets: {sorted({r['dataset_id'] for r in out})}")


def _vec(rows, key):
    vals = [float(r[key]) for r in rows if _isnum(r.get(key))]
    return np.array(vals)


def _isnum(v):
    try:
        float(v)
        return True
    except (TypeError, ValueError):
        return False


def _pearson(x, y):
    if len(x) < 3 or len(y) < 3:
        return None
    if len(x) != len(y):
        return None
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() < 3:
        return None
    sx, sy = x[mask], y[mask]
    if np.std(sx) == 0 or np.std(sy) == 0:
        return None
    return float(np.corrcoef(sx, sy)[0, 1])


def _fmt(v):
    return f"{v:+.2f}" if v is not None else "—"


if __name__ == "__main__":
    main()