# NAMPT-axis first-pass scoring report

## Scope

This report harmonizes public GEO processed expression matrices into a NAMPT-axis gene subset and computes within-dataset z-scored inflammatory, repair, and balance scores. Scores are intended for direction-of-effect screening, not clinical inference.

## Gene coverage

| dataset_id | samples | axis_genes_detected | axis_gene_coverage_pct | has_NAMPT | transform |
| --- | --- | --- | --- | --- | --- |
| GSE312393_24h_exercise | 7 | 59 | 100.0 | True | log2_x_plus_1 |
| GSE312393_6weeks_training | 6 | 59 | 100.0 | True | log2_x_plus_1 |
| GSE305038_activity_inactivity_exercise | 25 | 50 | 84.7 | True | log2_x_plus_1 |
| GSE292369_exercise_ketone_recovery | 34 | 59 | 100.0 | True | none_already_log_like |
| GSE318937_exercise_oleuropein | 119 | 59 | 100.0 | True | log2_x_plus_1 |
| GSE32575_monocytes_obesity_surgery | 48 | 59 | 100.0 | True | log2_x_plus_1 |
| GSE272133_muscle_bariatric | 52 | 59 | 100.0 | True | log2_x_plus_1 |
| GSE294150_visceral_adipose | 40 | 59 | 100.0 | True | log2_x_plus_1 |
| GSE282850_muscle_cell_aicar_palmitate | 15 | 47 | 79.7 | True | none_already_log_like |

## Predefined contrast deltas

| dataset_id | contrast | case_n | control_n | NAMPT_z_delta | inflammatory_score_delta | repair_score_delta | balance_score_delta |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GSE312393_24h_exercise | 24h_exercise_vs_control | 3 | 4 | 0.0256 | -0.3047 | -0.2828 | 0.0219 |
| GSE312393_6weeks_training | post_training_vs_pre_training | 3 | 3 | 1.107 | 0.1607 | 0.4302 | 0.2694 |
| GSE305038_activity_inactivity_exercise | active_post_vs_active_pre | 6 | 6 | 0.4758 | 0.122 | -0.0267 | -0.1487 |
| GSE305038_activity_inactivity_exercise | inactive_post_vs_inactive_pre | 7 | 6 | -0.2137 | 0.0981 | -0.3251 | -0.4232 |
| GSE292369_exercise_ketone_recovery | exercised_vs_rest | 18 | 16 | 0.7279 | 0.2583 | -0.0921 | -0.3503 |
| GSE318937_exercise_oleuropein | MICE_placebo_post_vs_pre | 10 | 9 | 0.6875 | 0.4243 | -0.1756 | -0.5999 |
| GSE318937_exercise_oleuropein | MICE_placebo_24h_vs_pre | 10 | 9 | 1.1029 | 0.062 | -0.0073 | -0.0693 |
| GSE318937_exercise_oleuropein | MICE_active_post_vs_pre | 10 | 10 | 1.1726 | 0.4724 | -0.5961 | -1.0685 |
| GSE318937_exercise_oleuropein | MICE_active_24h_vs_pre | 10 | 10 | 1.2975 | -0.0084 | -0.0138 | -0.0054 |
| GSE318937_exercise_oleuropein | SIE_placebo_post_vs_pre | 10 | 10 | 0.4057 | 0.3664 | -0.1339 | -0.5004 |
| GSE318937_exercise_oleuropein | SIE_placebo_24h_vs_pre | 10 | 10 | 1.3067 | 0.068 | 0.0093 | -0.0587 |
| GSE318937_exercise_oleuropein | SIE_active_post_vs_pre | 10 | 10 | 0.316 | 0.3998 | -0.0749 | -0.4747 |
| GSE318937_exercise_oleuropein | SIE_active_24h_vs_pre | 10 | 10 | 0.9832 | 0.0117 | -0.0279 | -0.0396 |
| GSE32575_monocytes_obesity_surgery | obese_before_vs_lean | 18 | 12 | 0.9231 | 0.0475 | 0.0378 | -0.0097 |
| GSE32575_monocytes_obesity_surgery | obese_after_vs_obese_before | 18 | 18 | 0.1952 | 0.8198 | 0.6067 | -0.2131 |
| GSE272133_muscle_bariatric | OB_w52_vs_OB_w0 | 13 | 13 | -0.1673 | -0.0432 | -0.0651 | -0.0218 |
| GSE272133_muscle_bariatric | T2D_w52_vs_T2D_w0 | 13 | 13 | 0.1239 | 0.1757 | 0.2956 | 0.1199 |
| GSE282850_muscle_cell_aicar_palmitate | aicar_vs_differentiated | 3 | 4 | 0.5559 | 0.0113 | 0.0744 | 0.063 |
| GSE282850_muscle_cell_aicar_palmitate | palmitate_vs_differentiated | 4 | 4 | 0.5426 | 0.1451 | 0.1789 | 0.0337 |

## Interpretation boundary

NAMPT mRNA is not equivalent to extracellular NAMPT protein. The scores separate transcriptomic inflammatory and repair programs; eNAMPT-specific claims require protein, secretion, or external biomarker evidence.