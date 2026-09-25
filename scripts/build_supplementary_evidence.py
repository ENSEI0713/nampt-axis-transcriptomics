#!/usr/bin/env python3
"""Build transparent supplementary evidence tables from existing project outputs.

No new biological model is fitted here. Outputs are deterministic reorganizations
of already audited CSVs, with explicit provenance and counting units.
"""
from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data_audit/outputs/supplementary_evidence"
OUT.mkdir(parents=True, exist_ok=True)


def read(rel: str) -> pd.DataFrame:
    return pd.read_csv(ROOT / rel, encoding="utf-8-sig")


def save(df: pd.DataFrame, stem: str, sheet: str = "data") -> None:
    df.to_csv(OUT / f"{stem}.csv", index=False, encoding="utf-8-sig")
    try:
        df.to_excel(OUT / f"{stem}.xlsx", index=False, sheet_name=sheet[:31])
    except Exception as exc:
        print(f"XLSX skipped for {stem}: {exc}")


def main() -> None:
    gene = read("data_audit/outputs/NAMPT_axis_gene_set_v1.csv")
    alpha = read("data_audit/outputs/axis_structure/module_alpha.csv")
    corr = read("data_audit/outputs/axis_structure/module_corr_matrix.csv")
    sens = read("data_audit/outputs/phase1b_sensitivity/nampt_axis_sensitivity_summary.csv")
    evo = read("data_audit/outputs/evo2/tiers.csv")
    scores = read("data_audit/outputs/nampt_axis_sample_scores.csv")
    formal = read("data_audit/outputs/nampt_axis_formal_contrast_stats.csv")

    # SD9: gene/module annotation and expression availability. This is an inventory,
    # not a cross-platform differential-expression table.
    expr_dir = ROOT / "data_audit/outputs/nampt_axis_expression"
    expr_files = sorted(expr_dir.glob("*.csv"))
    availability = []
    for path in expr_files:
        d = pd.read_csv(path, encoding="utf-8-sig", nrows=0)
        availability.append({"expression_file": path.name, "dataset_id": path.stem.replace("_axis_expression", ""), "columns": len(d.columns), "gene_rows": sum(1 for _ in open(path, encoding="utf-8-sig")) - 1})
    avail = pd.DataFrame(availability)
    gene_counts = gene.groupby(["module", "score_group"], dropna=False).size().reset_index(name="gene_count")
    sd9 = gene.merge(gene_counts, on=["module", "score_group"], how="left")
    sd9["table_scope"] = "gene-set annotation and per-dataset expression availability; no cross-platform expression pooling"
    save(sd9, "Supplementary_Data_9_gene_module_inventory")
    avail.to_csv(OUT / "Supplementary_Data_9_expression_file_inventory.csv", index=False, encoding="utf-8-sig")

    # SD10: module structure tables combined with an explicit table_type column.
    alpha2 = alpha.copy(); alpha2["table_type"] = "module_internal_consistency_Cronbach_alpha"
    corr2 = corr.copy(); corr2["table_type"] = "module_pair_correlation"
    # align columns without losing fields
    sd10 = pd.concat([alpha2, corr2], ignore_index=True, sort=False)
    sd10["interpretation_boundary"] = "structural co-expression description; not a between-group significance test"
    save(sd10, "Supplementary_Data_10_module_structure")

    # SD11: sensitivity atlas directly from audited Phase 1b summary.
    sd11 = sens.copy()
    sd11["atlas_scope"] = "pre-specified Phase 1b gene/module-drop sensitivity variants"
    sd11["interpretation_boundary"] = "comparison to primary score; not a new independent experiment"
    save(sd11, "Supplementary_Data_11_sensitivity_atlas")

    # SD12: complete Evo2/QTL/GWAS table, preserving every audited candidate row.
    sd12 = evo.copy()
    sd12["table_scope"] = "432 priority candidates; Evo2 perturbation plus external evidence"
    sd12["interpretation_boundary"] = "exploratory hypothesis prioritization; no causality or clinical-risk inference"
    save(sd12, "Supplementary_Data_12_evo2_external_evidence")

    # SD13: auditable sample-level trajectory long table. No trajectory model is fitted.
    trajectory_cols = [c for c in [
        "dataset_id", "sample_id", "geo_accession", "participant", "participant_id", "subject_id",
        "condition", "timepoint", "intervention", "exercise_type", "nutrition_or_treatment",
        "tissue", "treatment", "disease_state", "NAMPT_z", "inflammatory_score",
        "repair_score", "balance_score", "analysis_unit_record"
    ] if c in scores.columns]
    traj = scores[trajectory_cols].copy()
    traj["analysis_unit_record"] = True
    traj["unique_biological_sample_id"] = traj["sample_id"].astype(str)
    traj["trajectory_scope"] = "sample-level records for descriptive paired trajectory reconstruction"
    traj["interpretation_boundary"] = "no mixed-effects or cross-study longitudinal model fitted"
    save(traj, "Supplementary_Data_13_sample_trajectory_records")

    # SD14: formal statistics audit table with explicit metric-level scope.
    sd14 = formal.copy()
    sd14["table_scope"] = "19 predefined contrasts x 4 metrics = 76 formal metric-level rows"
    sd14["interpretation_boundary"] = "contrast-level statistics; paired exercise meta uses 12 eligible paired contrasts"
    save(sd14, "Supplementary_Data_14_formal_contrast_statistics")

    # Machine-readable manifest.
    manifest = pd.DataFrame([
        ["Supplementary Data 9", "Gene/module inventory and expression-file availability", "59 gene annotations; 9 expression inventories", "inventory; no cross-platform pooling"],
        ["Supplementary Data 10", "Module structure", f"{len(alpha)} alpha rows + {len(corr)} correlation rows", "structural description"],
        ["Supplementary Data 11", "Phase 1b sensitivity atlas", f"{len(sens)} summary rows", "pre-specified variants only"],
        ["Supplementary Data 12", "Evo2 + GTEx/GWAS full evidence table", f"{len(evo)} priority candidates", "exploratory; A/B=0"],
        ["Supplementary Data 13", "Sample-level trajectory records", f"{len(traj)} analysis-unit records", "descriptive records; no new longitudinal model"],
        ["Supplementary Data 14", "Formal contrast statistics", f"{len(formal)} metric-level rows", "19 contrasts x 4 metrics"],
    ], columns=["supplementary_data", "content", "row_scope", "boundary"])
    manifest.to_csv(OUT / "supplementary_evidence_manifest.csv", index=False, encoding="utf-8-sig")
    manifest.to_excel(OUT / "supplementary_evidence_manifest.xlsx", index=False, sheet_name="manifest")
    print(f"Built supplementary evidence in {OUT}")
    print(manifest.to_string(index=False))


if __name__ == "__main__":
    main()
