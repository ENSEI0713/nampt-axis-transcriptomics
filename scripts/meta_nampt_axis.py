#!/usr/bin/env python3
"""Random-effects meta-analysis of NAMPT-axis predefined contrasts.

Reads the Phase 1 formal contrast stats and the per-sample scores, then pools
effect directions across datasets with a DerSimonian-Laird random-effects model,
stratified by domain (exercise vs obesity) and metric
(NAMPT_z / inflammatory_score / repair_score / balance_score).

The analysis uses standardized within-dataset mean deltas only, never raw
cross-platform expression. Results are for direction-of-effect pooling, not
clinical effect claims.

Outputs:
  data_audit/outputs/meta/meta_results.csv
  data_audit/outputs/meta/meta_report.md
"""
from __future__ import annotations

import csv
import math
import os
from collections import defaultdict
from datetime import datetime, timezone

import numpy as np

BASE = os.path.join(os.path.dirname(__file__), "..", "data_audit", "outputs")
CONTRASTS_CSV = os.path.join(BASE, "nampt_axis_formal_contrast_stats.csv")
SAMPLES_CSV = os.path.join(BASE, "nampt_axis_sample_scores.csv")
OUT_DIR = os.path.join(BASE, "meta")

METRICS = ["NAMPT_z", "inflammatory_score", "repair_score", "balance_score"]

# Dataset -> domain stratification
DOMAIN_MAP = {
    "GSE312393_24h_exercise": "exercise",
    "GSE312393_6weeks_training": "exercise",
    "GSE318937_exercise_oleuropein": "exercise",
    "GSE305038_activity_inactivity_exercise": "exercise",
    "GSE292369_exercise_ketone_recovery": "exercise",
    "GSE32575_monocytes_obesity_surgery": "obesity",
    "GSE272133_muscle_bariatric": "obesity",
    "GSE294150_visceral_adipose": "obesity",
    "GSE282850_muscle_cell_aicar_palmitate": "obesity_cell_model",
}


def dl_random_effects(effects: list[float], variances: list[float]) -> dict:
    """DerSimonian-Laird random-effects pooling.

    Returns pooled effect, its SE, 95% CI, I^2, tau^2, and Cochran Q.
    """
    n = len(effects)
    if n == 0:
        return {}
    w = [1.0 / v for v in variances]
    sw = sum(w)
    theta_fixed = sum(wi * ei for wi, ei in zip(w, effects)) / sw
    Q = sum(wi * (ei - theta_fixed) ** 2 for wi, ei in zip(w, effects))
    df = n - 1
    k = n
    C = sw - sum(wi**2 for wi in w) / sw
    tau2 = max(0.0, (Q - df) / C) if C > 0 else 0.0
    # I^2 (could be negative -> 0)
    i2 = max(0.0, (Q - df) / Q * 100.0) if Q > 0 else 0.0
    w2 = [1.0 / (v + tau2) for v in variances]
    sw2 = sum(w2)
    theta = sum(wi * ei for wi, ei in zip(w2, effects)) / sw2
    se = math.sqrt(1.0 / sw2) if sw2 > 0 else float("nan")
    z = theta / se if se else float("nan")
    lo = theta - 1.96 * se
    hi = theta + 1.96 * se
    p = 2 * (1 - _norm_cdf(abs(z))) if se else float("nan")
    return {
        "k": k,
        "pooled_effect": theta,
        "se": se,
        "ci95_low": lo,
        "ci95_high": hi,
        "z": z,
        "p_value": p,
        "I2_pct": i2,
        "tau2": tau2,
        "Q": Q,
    }


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def load_contrasts() -> list[dict]:
    with open(CONTRASTS_CSV, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    rows = load_contrasts()

    # Exclude unpaired contrasts without a usable effect size (GSE312393_24h unpaired)
    # Keep paired & paired_intersection designs; compute SE from delta_sd / sqrt(n).
    usable = []
    for r in rows:
        design = r.get("analysis_design", "")
        if design not in ("paired", "paired_intersection"):
            continue
        delta_sd = _float(r.get("delta_sd"))
        n = _int(r.get("analysis_n"))
        effect = _float(r.get("effect_size"))
        delta = _float(r.get("mean_delta"))
        ci_lo = _float(r.get("ci95_low"))
        ci_hi = _float(r.get("ci95_high"))
        if delta_sd is None or n is None or n <= 1 or effect is None or delta is None:
            continue
        se = delta_sd / math.sqrt(n)
        var = se**2
        metric = r.get("metric")
        if metric not in METRICS:
            continue
        usable.append({**r, "_se": se, "_var": var, "_delta": delta,
                       "_effect": effect, "_ci_lo": ci_lo, "_ci_hi": ci_hi})

    # Stratify: domain (exercise / obesity) x metric
    strat = defaultdict(list)
    for r in usable:
        ds = r["dataset_id"]
        domain = DOMAIN_MAP.get(ds, "other")
        strat[(domain, r["metric"])].append(r)

    results = []
    md_lines = []
    md_lines.append("# NAMPT-axis random-effects meta-analysis")
    md_lines.append("")
    md_lines.append(f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    md_lines.append("")
    md_lines.append(
        "Model: DerSimonian-Laird random effects on within-dataset standardized "
        "mean deltas (paired designs only). Directional pooling only; raw "
        "cross-platform expression values are never merged."
    )
    md_lines.append("")

    for (domain, metric), items in sorted(strat.items()):
        if len(items) < 2:
            md_lines.append(f"## {domain} / {metric} — insufficient contrasts (k={len(items)}), skipped")
            md_lines.append("")
            continue
        effects = [it["_effect"] for it in items]
        variances = [it["_var"] for it in items]
        res = dl_random_effects(effects, variances)
        # direction agreement
        pos = sum(1 for e in effects if e > 0)
        neg = sum(1 for e in effects if e < 0)
        res["domain"] = domain
        res["metric"] = metric
        res["n_positive"] = pos
        res["n_negative"] = neg
        res["direction_agreement_pct"] = max(pos, neg) / len(effects) * 100.0
        res["datasets"] = ";".join(sorted({it["dataset_id"] for it in items}))
        results.append(res)

        md_lines.append(f"## {domain} / {metric}")
        md_lines.append("")
        md_lines.append(
            f"k={res['k']} contrasts · pooled effect "
            f"{res['pooled_effect']:.3f} (95% CI {res['ci95_low']:.3f}–{res['ci95_high']:.3f})"
            f" · I²={res['I2_pct']:.1f}% · tau²={res['tau2']:.4f} · Q={res['Q']:.2f}"
        )
        md_lines.append(f"- direction: {pos} positive / {neg} negative ({res['direction_agreement_pct']:.0f}% agreement)")
        md_lines.append(f"- p-value (z-test): {res['p_value']:.4g}")
        md_lines.append("")
        md_lines.append("| dataset | contrast | n | mean_delta | effect | 95% CI |")
        md_lines.append("|---|---|---|---|---|---|")
        for it in items:
            ci_lo = it["_ci_lo"] if it["_ci_lo"] is not None else float("nan")
            ci_hi = it["_ci_hi"] if it["_ci_hi"] is not None else float("nan")
            eff = it["_effect"]
            se_eff = math.sqrt(it["_var"]) if it["_var"] is not None else float("nan")
            if math.isfinite(se_eff) and se_eff > 0:
                eff_lo = eff - 1.96 * se_eff
                eff_hi = eff + 1.96 * se_eff
            else:
                eff_lo = eff_hi = float("nan")
            md_lines.append(
                f"| {it['dataset_id']} | {it['contrast']} | {it['analysis_n']} | "
                f"{it['_delta']:+.3f} | {eff:+.3f} | "
                f"{eff_lo:.2f}–{eff_hi:.2f} |"
            )
        md_lines.append("")

    # Write results CSV
    fieldnames = [
        "domain", "metric", "k", "pooled_effect", "se", "ci95_low", "ci95_high",
        "z", "p_value", "I2_pct", "tau2", "Q",
        "n_positive", "n_negative", "direction_agreement_pct", "datasets",
    ]
    with open(os.path.join(OUT_DIR, "meta_results.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for res in results:
            w.writerow(res)

    # Per-contrast table used as meta input
    with open(os.path.join(OUT_DIR, "meta_input_contrasts.csv"), "w", newline="", encoding="utf-8") as f:
        fieldnames_in = [
            "dataset_id", "contrast", "domain", "metric", "analysis_design",
            "analysis_n", "mean_delta", "delta_sd", "se", "effect_size", "ci95_low", "ci95_high",
        ]
        w = csv.DictWriter(f, fieldnames=fieldnames_in)
        w.writeheader()
        for r in usable:
            w.writerow({
                "dataset_id": r["dataset_id"],
                "contrast": r["contrast"],
                "domain": DOMAIN_MAP.get(r["dataset_id"], "other"),
                "metric": r["metric"],
                "analysis_design": r["analysis_design"],
                "analysis_n": r["analysis_n"],
                "mean_delta": r["_delta"],
                "delta_sd": r.get("delta_sd"),
                "se": round(r["_se"], 6),
                "effect_size": r["_effect"],
                "ci95_low": r["_ci_lo"],
                "ci95_high": r["_ci_hi"],
            })

    with open(os.path.join(OUT_DIR, "meta_report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"Wrote {len(results)} meta strata to {OUT_DIR}")
    for res in results:
        print(
            f"  {res['domain']}/{res['metric']}: k={res['k']} pooled={res['pooled_effect']:.3f} "
            f"I2={res['I2_pct']:.1f}% dir_agree={res['direction_agreement_pct']:.0f}%"
        )


def _float(v) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _int(v) -> int | None:
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


if __name__ == "__main__":
    main()
