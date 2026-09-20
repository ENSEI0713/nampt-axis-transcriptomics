#!/usr/bin/env python3
"""Describe moderator coverage and feasibility without fitting an invalid meta-regression.

The current project has dataset-nested exercise contrasts and incomplete,
dataset-specific moderator fields. This script reports observable coverage and
within-dataset strata only. It intentionally does not fit a pooled moderator
meta-regression, because the available effect-size covariance and common
moderator coding are insufficient.
"""
from __future__ import annotations
import csv, os
from collections import Counter, defaultdict
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(__file__))
OUT = os.path.join(ROOT, "data_audit", "outputs", "meta")
SAMPLES = os.path.join(ROOT, "data_audit", "outputs", "nampt_axis_sample_scores.csv")
PREDEFINED = os.path.join(ROOT, "data_audit", "outputs", "nampt_axis_predefined_contrasts.csv")
FORMAL = os.path.join(ROOT, "data_audit", "outputs", "nampt_axis_formal_contrast_stats.csv")
MOD_FIELDS = ["timepoint", "exercise_type", "nutrition_or_treatment", "intervention", "treatment"]

def nonempty(v):
    return bool(str(v or "").strip())

def main():
    with open(SAMPLES, encoding="utf-8-sig", newline="") as f:
        samples = list(csv.DictReader(f))
    with open(PREDEFINED, encoding="utf-8-sig", newline="") as f:
        contrasts = list(csv.DictReader(f))
    with open(FORMAL, encoding="utf-8-sig", newline="") as f:
        formal = list(csv.DictReader(f))
    os.makedirs(OUT, exist_ok=True)

    coverage = []
    for field in MOD_FIELDS:
        n = sum(nonempty(r.get(field)) for r in samples)
        coverage.append({"field": field, "n_nonempty": n, "n_total": len(samples), "missing_pct": round(100*(len(samples)-n)/len(samples), 2)})
    with open(os.path.join(OUT, "moderator_coverage.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(coverage[0]))
        w.writeheader(); w.writerows(coverage)

    def count_where(pred, fields):
        c = Counter()
        for r in samples:
            if pred(r):
                key = tuple(r.get(k, "") for k in fields)
                c[key] += 1
        return c

    g318 = count_where(lambda r: r.get("dataset_id") == "GSE318937_exercise_oleuropein", ["exercise_type", "nutrition_or_treatment", "timepoint"])
    g305 = count_where(lambda r: r.get("dataset_id") == "GSE305038_activity_inactivity_exercise", ["condition", "timepoint"])
    g312 = count_where(lambda r: r.get("dataset_id") in {"GSE312393_24h_exercise", "GSE312393_6weeks_training"}, ["dataset_id", "condition", "timepoint"])

    md = ["# Moderator feasibility report", "", f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}", "",
          "## Scope", "",
          f"样本级文件共 {len(samples)} 行，formal contrast 文件共 {len(formal)} 行，预定义 contrast 共 {len(contrasts)} 个。",
          "本报告只做字段覆盖和单数据集内分层描述，不拟合跨研究 moderator 元回归。原因是 effect size 嵌套在数据集/受试者内，且没有统一的跨研究 moderator 编码与效应协方差。", "",
          "## Moderator field coverage", "", "| field | non-empty | total | missing % |", "|---|---:|---:|---:|"]
    for r in coverage:
        md.append(f"| {r['field']} | {r['n_nonempty']} | {r['n_total']} | {r['missing_pct']:.2f} |")
    md += ["", "## Within-dataset strata", "", "### GSE318937", "", "| exercise_type | nutrition_or_treatment | timepoint | n |", "|---|---|---|---:|"]
    for k,n in sorted(g318.items()): md.append(f"| {' | '.join(k)} | {n} |" )
    md += ["", "### GSE305038", "", "| condition | timepoint | n |", "|---|---|---:|"]
    for k,n in sorted(g305.items()): md.append(f"| {' | '.join(k)} | {n} |")
    md += ["", "### GSE312393", "", "| dataset_id | condition | timepoint | n |", "|---|---|---|---:|"]
    for k,n in sorted(g312.items()): md.append(f"| {' | '.join(k)} | {n} |")
    md += ["", "## Feasibility conclusion", "",
           "- 可以做：GSE318937、GSE305038、GSE312393 内部的时间点/训练状态/干预背景描述。",
           "- 当前不能做：把所有研究的 timepoint、training_status、nutrition_background 直接拼成统一跨研究元回归。",
           "- 需要新增材料后才能做：逐 contrast moderator 编码、数据集聚类结构、重复测量效应协方差和预先定义的 moderator 模型。",
           "- 因此本轮不报告正式 moderator p 值，不把 I² 本身解释为状态依赖性证据。"]
    with open(os.path.join(OUT, "moderator_feasibility_report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print(f"Wrote {len(coverage)} coverage rows and within-dataset strata to {OUT}")

if __name__ == "__main__":
    main()
