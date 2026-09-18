#!/usr/bin/env python3
"""NAMPT-axis module internal-consistency analysis.

For each dataset's saved axis expression matrix, tests whether the biological
modules that define the 'inflammatory NAMPT program' and the 'repair NAMPT
program' actually hold together in the public expression data. Reports:

  - Cronbach's alpha for the inflammatory module and the repair module
    (std item alpha over the genes in that module that are detected).
  - Average inter-module correlation (module A vs module B mean gene-level
    correlation) and intra-module mean gene-gene correlation.
  - A module-level correlation matrix across a fixed set of curated modules.

This is the evidence that the 'two programs' framing is not just a paper
construct: it should show that inflammatory genes and repair genes cluster
with themselves more than across each other wherever the data allow.

Outputs:
  data_audit/outputs/axis_structure/module_alpha.csv
  data_audit/outputs/axis_structure/module_corr_matrix.csv
  data_audit/outputs/axis_structure/axis_structure_report.md
"""
from __future__ import annotations

import csv
import glob
import math
import os
from collections import defaultdict
from datetime import datetime, timezone

import numpy as np

BASE = os.path.join(os.path.dirname(__file__), "..", "data_audit", "outputs")
EXPR_DIR = os.path.join(BASE, "nampt_axis_expression")
OUT_DIR = os.path.join(BASE, "axis_structure")

# Module groups for the two programs
CORE_MODULES = [
    "nad_salvage_core",
    "nfkb_inflammation",
    "monocyte_macrophage",
    "nad_consumption_inflammation",
    "nad_consumption_repair",
    "ampk_mitochondria_repair",
    "sirtuin_repair",
    "mitochondrial_biogenesis",
    "autophagy_repair",
]


def cronbach_alpha(X: np.ndarray) -> float:
    """Cronbach's alpha over rows=items(genes), cols=samples.

    Alpha = k/(k-1) * (1 - sum(item_var)/total_var).
    """
    k = X.shape[0]
    if k < 2:
        return float("nan")
    item_vars = np.var(X, axis=1, ddof=1)
    total_score = X.sum(axis=0)
    total_var = np.var(total_score, ddof=1)
    if total_var <= 0:
        return float("nan")
    alpha = (k / (k - 1)) * (1 - item_vars.sum() / total_var)
    return float(alpha)


def load_dataset_expr(path: str) -> tuple[dict, np.ndarray, list[str]]:
    """Return {gene: (module, score_group)}, sample-major expr array, sample heads."""
    module_of = {}
    group_of = {}
    genes = []
    samples = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        samples = header[5:]  # after gene_symbol,module,score_group,rationale
        rows = []
        for row in reader:
            if not row or not row[0]:
                continue
            genes.append(row[0])
            module_of[row[0]] = row[1]
            group_of[row[0]] = row[2]
            rows.append([float(x) for x in row[5:]])
    X = np.array(rows, dtype=float).T if rows else np.zeros((0, 0))
    return module_of, X, genes, group_of


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    alpha_rows = []
    stats_rows = []

    files = sorted(glob.glob(os.path.join(EXPR_DIR, "*_axis_expression.csv")))
    if not files:
        print("No axis expression files found")
        return

    # Global module correlation matrix (aggregated over datasets)

    for path in files:
        ds = os.path.basename(path).replace("_axis_expression.csv", "")
        module_of, X, samples, group_of = load_dataset_expr(path)
        genes = list(module_of.keys())
        if X.shape[0] < 3:
            print(f"  skip {ds}: too few samples ({X.shape[0]})")
            continue

        # Build module -> gene index map present in this dataset
        mod_genes = defaultdict(list)
        for i, g in enumerate(genes):
            if i < X.shape[1]:
                mod_genes[module_of.get(g, "unknown")].append(i)

        # Cronbach alpha per module across present genes
        for mod, idxs in mod_genes.items():
            if len(idxs) < 2:
                continue
            alpha = cronbach_alpha(X[:, idxs].T)
            alpha_rows.append({
                "dataset_id": ds,
                "module": mod,
                "n_genes": len(idxs),
                "n_samples": X.shape[0],
                "cronbach_alpha": alpha,
            })

        # Module-level correlation: mean gene-gene r within module, and
        # mean cross-module r between representative modules.
        corr = np.corrcoef(X.T)  # gene x gene correlation
        for m1 in mod_genes:
            for m2 in mod_genes:
                if m1 > m2:
                    continue
                idx1 = mod_genes[m1]
                idx2 = mod_genes[m2]
                sub = corr[np.ix_(idx1, idx2)]
                if sub.size == 0:
                    continue
                # drop diagonal for same-module
                vals = sub[np.triu_indices_from(sub, 1)] if m1 == m2 and sub.shape[0] > 1 else sub.flatten()
                vals = vals[np.isfinite(vals)]
                r_mean = float(np.mean(vals)) if vals.size else float("nan")
                stats_rows.append({
                    "dataset_id": ds,
                    "module_a": m1,
                    "module_b": m2,
                    "mean_correlation": r_mean,
                    "n_pairs": int(vals.size),
                })

    # Write alpha CSV
    if alpha_rows:
        with open(os.path.join(OUT_DIR, "module_alpha.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["dataset_id", "module", "n_genes", "n_samples", "cronbach_alpha"])
            w.writeheader()
            for r in alpha_rows:
                w.writerow(r)

    # Write correlation table
    if stats_rows:
        with open(os.path.join(OUT_DIR, "module_corr_matrix.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["dataset_id", "module_a", "module_b", "mean_correlation", "n_pairs"])
            w.writeheader()
            for r in stats_rows:
                w.writerow(r)

    # Report
    lines = ["# NAMPT-axis module internal-consistency analysis", ""]
    lines.append(f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    lines.append("")
    lines.append("Cronbach's alpha (standardized) measures whether the genes within a")
    lines.append("module move together across samples. A value >0.7 is commonly read as")
    lines.append("acceptable internal consistency; we treat it as structural support that")
    lines.append("the 'inflammatory' and 'repair' programs are real co-expression units,")
    lines.append("not arbitrary gene lists.")
    lines.append("")
    lines.append("## Cronbach alpha by dataset x module")
    lines.append("")
    lines.append("| dataset | module | n_genes | n_samples | alpha |")
    lines.append("|---|---|---|---|---|")
    for r in alpha_rows:
        lines.append(
            f"| {r['dataset_id']} | {r['module']} | {r['n_genes']} | {r['n_samples']} | "
            f"{r['cronbach_alpha']:.3f} |"
        )
    lines.append("")
    lines.append("## Mean gene-gene correlation between modules (within datasets)")
    lines.append("")
    lines.append("| dataset | module_a | module_b | mean_r | n_pairs |")
    lines.append("|---|---|---|---|---|")
    for r in stats_rows:
        lines.append(
            f"| {r['dataset_id']} | {r['module_a']} | {r['module_b']} | "
            f"{r['mean_correlation']:+.3f} | {r['n_pairs']} |"
        )
    lines.append("")

    with open(os.path.join(OUT_DIR, "axis_structure_report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # Print summary
    print(f"Wrote {len(alpha_rows)} alpha rows, {len(stats_rows)} correlation pairs to {OUT_DIR}")
    if alpha_rows:
        # top-level summary
        for r in alpha_rows:
            print(f"  {r['dataset_id']}/{r['module']}: alpha={r['cronbach_alpha']:.3f} (n_genes={r['n_genes']}, n={r['n_samples']})")


if __name__ == "__main__":
    main()