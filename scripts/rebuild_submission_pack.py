#!/usr/bin/env python3
"""Rebuild the NAMPT manuscript submission pack zip (2026-09-23 snapshot).

Structure mirrors the 09-21 pack but uses ASCII filenames (no GBK mojibake),
includes the 09-23 regenerated figures, updated manuscript/methods/legends,
new docx + PDF manuscript builds, and updated bib.
Output: data_audit/outputs/NAMPT_manuscript_submission_pack_2026-09-23.zip
"""
from __future__ import annotations

import zipfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "data_audit/outputs"
SUB = OUTPUTS / "submission_pack"
ASSETS = OUTPUTS / "submission_assets"

stamp = "2026-09-26"
OUT = OUTPUTS / f"NAMPT_manuscript_submission_pack_{stamp}.zip"

# (zip_relative_path, absolute_source_path)
entries: list[tuple[str, Path]] = [
    # 01 Manuscript (ASCII names; latest 09-23 content)
    ("01_Manuscript/manuscript_full_en_v1.md", OUTPUTS / "manuscript_full_en_v1.md"),
    ("01_Manuscript/manuscript_frontmatter_v1_zh.md", OUTPUTS / "manuscript_frontmatter_v1_zh.md"),
    ("01_Manuscript/manuscript_logic_v1_zh.md", OUTPUTS / "manuscript_logic_v1_zh.md"),
    ("01_Manuscript/manuscript_methods_v1_zh.md", OUTPUTS / "manuscript_methods_v1_zh.md"),
    ("01_Manuscript/manuscript_results_v2_zh.md", OUTPUTS / "manuscript_results_v2_zh.md"),
    ("01_Manuscript/manuscript_full_en_v1.docx", SUB / "manuscript_full_en_v1.docx"),
    ("01_Manuscript/manuscript_full_en_v1.pdf", SUB / "manuscript_full_en_v1.pdf"),
    # 02 Figures
    ("02_Figures/figure_legends_supp_data.md", OUTPUTS / "figure_legends_supp_data.md"),
    ("02_Figures/figure1_editable_source.svg", OUTPUTS / "figures_phase3_tidyplots/Figure1_NAMPT_axis_editable.svg"),
    ("02_Figures/figure3_phase3_composite.svg", OUTPUTS / "figures_phase3_tidyplots/Figure3_exercise_tidyplots_composite.svg"),
    ("02_Figures/figure4_phase3_composite.svg", OUTPUTS / "figures_phase3_tidyplots/Figure4_meta_tidyplots_composite.svg"),
    ("02_Figures/figure5_phase3_composite.svg", OUTPUTS / "figures_phase3_tidyplots/Figure5_obesity_tidyplots_composite.svg"),
    ("02_Figures/figure6_exploratory_tier_panel.svg", OUTPUTS / "figures_phase3_tidyplots/Figure6_evo2_exploratory_tidyplots_panel_c.svg"),
    ("02_Figures/phase3_figure_qc/figure3_qc.txt", OUTPUTS / "figures_phase3_tidyplots/Figure3_exercise_tidyplots_panels_qc.txt"),
    ("02_Figures/phase3_figure_qc/figure4_qc.txt", OUTPUTS / "figures_phase3_tidyplots/Figure4_meta_tidyplots_qc.txt"),
    ("02_Figures/phase3_figure_qc/figure5_qc.txt", OUTPUTS / "figures_phase3_tidyplots/Figure5_obesity_tidyplots_qc.txt"),
    ("02_Figures/phase3_figure_qc/figure6_qc.txt", OUTPUTS / "figures_phase3_tidyplots/Figure6_evo2_exploratory_tidyplots_panel_c_qc.txt"),
    ("02_Figures/submission_assets/Figure1_framework.pdf", ASSETS / "Figure1_framework.pdf"),
    ("02_Figures/submission_assets/Figure1_framework.png", ASSETS / "Figure1_framework.png"),
    ("02_Figures/submission_assets/Figure1_framework.svg", ASSETS / "Figure1_framework.svg"),
    ("02_Figures/submission_assets/Figure1_framework.tiff", ASSETS / "Figure1_framework.tiff"),
    ("02_Figures/submission_assets/Figure2_public_data_framework.pdf", ASSETS / "Figure2_public_data_framework.pdf"),
    ("02_Figures/submission_assets/Figure2_public_data_framework.png", ASSETS / "Figure2_public_data_framework.png"),
    ("02_Figures/submission_assets/Figure2_public_data_framework.svg", ASSETS / "Figure2_public_data_framework.svg"),
    ("02_Figures/submission_assets/Figure2_public_data_framework.tiff", ASSETS / "Figure2_public_data_framework.tiff"),
    ("02_Figures/submission_assets/Figure3_exercise_nampt_axis.pdf", ASSETS / "Figure3_exercise_nampt_axis.pdf"),
    ("02_Figures/submission_assets/Figure3_exercise_nampt_axis.png", ASSETS / "Figure3_exercise_nampt_axis.png"),
    ("02_Figures/submission_assets/Figure3_exercise_nampt_axis.svg", ASSETS / "Figure3_exercise_nampt_axis.svg"),
    ("02_Figures/submission_assets/Figure3_exercise_nampt_axis.tiff", ASSETS / "Figure3_exercise_nampt_axis.tiff"),
    ("02_Figures/submission_assets/Figure4_meta_forest.pdf", ASSETS / "Figure4_meta_forest.pdf"),
    ("02_Figures/submission_assets/Figure4_meta_forest.png", ASSETS / "Figure4_meta_forest.png"),
    ("02_Figures/submission_assets/Figure4_meta_forest.svg", ASSETS / "Figure4_meta_forest.svg"),
    ("02_Figures/submission_assets/Figure4_meta_forest.tiff", ASSETS / "Figure4_meta_forest.tiff"),
    ("02_Figures/submission_assets/Figure5_obesity_nampt_axis.pdf", ASSETS / "Figure5_obesity_nampt_axis.pdf"),
    ("02_Figures/submission_assets/Figure5_obesity_nampt_axis.png", ASSETS / "Figure5_obesity_nampt_axis.png"),
    ("02_Figures/submission_assets/Figure5_obesity_nampt_axis.svg", ASSETS / "Figure5_obesity_nampt_axis.svg"),
    ("02_Figures/submission_assets/Figure5_obesity_nampt_axis.tiff", ASSETS / "Figure5_obesity_nampt_axis.tiff"),
    ("02_Figures/submission_assets/Figure6_evo2_prioritization.pdf", ASSETS / "Figure6_evo2_prioritization.pdf"),
    ("02_Figures/submission_assets/Figure6_evo2_prioritization.png", ASSETS / "Figure6_evo2_prioritization.png"),
    ("02_Figures/submission_assets/Figure6_evo2_prioritization.svg", ASSETS / "Figure6_evo2_prioritization.svg"),
    ("02_Figures/submission_assets/Figure6_evo2_prioritization.tiff", ASSETS / "Figure6_evo2_prioritization.tiff"),
    ("02_Figures/figure_sources/figure2_dataset_coverage.csv", OUTPUTS / "figure_sources/figure2_dataset_coverage.csv"),
    ("02_Figures/figure_sources/figure3_exercise_axis_contrasts.csv", OUTPUTS / "figure_sources/figure3_exercise_axis_contrasts.csv"),
    ("02_Figures/figure_sources/figure4_obesity_axis_contrasts.csv", OUTPUTS / "figure_sources/figure4_obesity_axis_contrasts.csv"),
    # 03 Supplementary Data
    ("03_Supplementary_Data/Supplementary_Data_1_sample_scores.xlsx", SUB / "Supplementary_Data_1_sample_scores.xlsx"),
    ("03_Supplementary_Data/Supplementary_Data_2_nampt_axis_gene_set.xlsx", SUB / "Supplementary_Data_2_nampt_axis_gene_set.xlsx"),
    ("03_Supplementary_Data/Supplementary_Data_3_predefined_contrasts.xlsx", SUB / "Supplementary_Data_3_predefined_contrasts.xlsx"),
    ("03_Supplementary_Data/Supplementary_Data_4_meta_results.xlsx", SUB / "Supplementary_Data_4_meta_results.xlsx"),
    ("03_Supplementary_Data/Supplementary_Data_5_module_consistency.xlsx", SUB / "Supplementary_Data_5_module_consistency.xlsx"),
    ("03_Supplementary_Data/Supplementary_Data_6_phase1b_sensitivity.xlsx", SUB / "Supplementary_Data_6_phase1b_sensitivity.xlsx"),
    ("03_Supplementary_Data/Supplementary_Data_7_moderator_coverage.xlsx", SUB / "Supplementary_Data_7_moderator_coverage.xlsx"),
    ("03_Supplementary_Data/Supplementary_Data_8_evo2_scoring_tiers.xlsx", SUB / "Supplementary_Data_8_evo2_scoring_tiers.xlsx"),
    # Supplementary evidence 9-14 and machine-readable sources
    ("03_Supplementary_Data/Supplementary_Data_9_gene_module_inventory.xlsx", OUTPUTS / "supplementary_evidence/Supplementary_Data_9_gene_module_inventory.xlsx"),
    ("03_Supplementary_Data/Supplementary_Data_9_expression_file_inventory.csv", OUTPUTS / "supplementary_evidence/Supplementary_Data_9_expression_file_inventory.csv"),
    ("03_Supplementary_Data/Supplementary_Data_10_module_structure.xlsx", OUTPUTS / "supplementary_evidence/Supplementary_Data_10_module_structure.xlsx"),
    ("03_Supplementary_Data/Supplementary_Data_11_sensitivity_atlas.xlsx", OUTPUTS / "supplementary_evidence/Supplementary_Data_11_sensitivity_atlas.xlsx"),
    ("03_Supplementary_Data/Supplementary_Data_12_evo2_external_evidence.xlsx", OUTPUTS / "supplementary_evidence/Supplementary_Data_12_evo2_external_evidence.xlsx"),
    ("03_Supplementary_Data/Supplementary_Data_13_sample_trajectory_records.xlsx", OUTPUTS / "supplementary_evidence/Supplementary_Data_13_sample_trajectory_records.xlsx"),
    ("03_Supplementary_Data/Supplementary_Data_14_formal_contrast_statistics.xlsx", OUTPUTS / "supplementary_evidence/Supplementary_Data_14_formal_contrast_statistics.xlsx"),
    ("03_Supplementary_Data/machine_readable_supplementary_evidence_manifest.csv", OUTPUTS / "supplementary_evidence/supplementary_evidence_manifest.csv"),
    # 04 References (updated)
    ("04_References/references_v1.bib", OUTPUTS / "references_v1.bib"),
    # 05 Submission docs
    ("05_Submission_Docs/cover_letter_v1.md", SUB / "cover_letter_v1.md"),
    ("05_Submission_Docs/GITHUB_ZENODO_FIRST_TIME_GUIDE.md", SUB / "GITHUB_ZENODO_FIRST_TIME_GUIDE.md"),
    ("05_Submission_Docs/reporting_summary_draft_v1.md", SUB / "reporting_summary_draft_v1.md"),
    ("05_Submission_Docs/reporting_summary_formatted.pdf", SUB / "reporting_summary_formatted.pdf"),
    ("05_Submission_Docs/submission_system_texts.md", SUB / "submission_system_texts.md"),
    # 06 Journal checks
    ("06_Journal_Checks/target_journal_assessment.md", OUTPUTS / "target_journal_assessment.md"),
    # 07 Review records (09-22 synthesis)
    ("07_Review_Records/mock_review_en_v1.md", OUTPUTS / "mock_review_en_v1.md"),
    ("07_Review_Records/pre_submission_review_synthesis.md", OUTPUTS / "pre_submission_review_synthesis.md"),
    # 08 Project status
    ("08_Project_Status/PROGRESS.md", ROOT / "PROGRESS.md"),
    ("08_Project_Status/README.md", ROOT / "README.md"),
    ("08_Project_Status/evidence_manifest.md", OUTPUTS / "evidence_manifest.md"),
    ("08_Project_Status/requirements-r.txt", ROOT / "requirements-r.txt"),
    ("08_Project_Status/supplementary_evidence_manifest.xlsx", OUTPUTS / "supplementary_evidence/supplementary_evidence_manifest.xlsx"),
    # 09 Archive metadata
    ("09_Archive/.zenodo.json", ROOT / ".zenodo.json"),
    ("09_Archive/ARCHIVE_README.md", ROOT / "ARCHIVE_README.md"),
    ("09_Archive/CITATION.cff", ROOT / "CITATION.cff"),
    ("09_Archive/LICENSE", ROOT / "LICENSE"),
    ("09_Archive/requirements.txt", ROOT / "requirements.txt"),
    # 10 Submission TODO checklist (from 09-21 pack, unchanged)
    ("10_Submission_TODO/SUBMISSION_TODO_CHECKLIST.md", OUTPUTS / "submission_todo_checklist.md"),
]


def main() -> None:
    missing = [(z, p) for z, p in entries if not p.exists()]
    if missing:
        for z, p in missing:
            print(f"MISSING: {z} -> {p}")
        raise SystemExit(1)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for zname, src in entries:
            zf.write(src, zname)
    print(f"wrote {OUT} ({len(entries)} entries)")
    with zipfile.ZipFile(OUT) as zf:
        names = zf.namelist()
        print("entries:", len(names))
        for head in sorted(set(n.split("/")[0] for n in names)):
            print(" -", head)


if __name__ == "__main__":
    main()
