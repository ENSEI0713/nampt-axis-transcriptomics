# NAMPT-axis Phase 1 formal statistics report

## Scope

This report upgrades the first-pass public GEO NAMPT-axis scoring into explicit statistical contrasts. Each dataset is analyzed on its own within-dataset z-score scale. NAMPT mRNA, inflammatory score, repair score, and balance score are not interpreted as extracellular NAMPT protein or clinical biomarkers.

## Statistical design

- Paired contrasts use matched participant-level deltas, a two-sided sign-flip permutation p-value, paired Cohen dz, and 5000 paired bootstrap resamples for the 95% confidence interval.
- Unpaired contrasts use two-sided label permutation, Hedges g, and 5000 unpaired bootstrap resamples for the 95% confidence interval.
- Multiple testing is controlled with Benjamini-Hochberg FDR globally and separately within each metric.
- Small-sample contrasts are retained as evidence-generating signals, not definitive clinical claims.

## Contrast design audit

| dataset_id | contrast | analysis_design | pairing_keys | control_n_raw | case_n_raw | paired_n |
| --- | --- | --- | --- | --- | --- | --- |
| GSE272133_muscle_bariatric | OB_w52_vs_OB_w0 | paired | participant_id | 13 | 13 | 13 |
| GSE272133_muscle_bariatric | T2D_w52_vs_T2D_w0 | paired | participant_id | 13 | 13 | 13 |
| GSE282850_muscle_cell_aicar_palmitate | aicar_vs_differentiated | paired_intersection | participant_id | 4 | 3 | 3 |
| GSE282850_muscle_cell_aicar_palmitate | palmitate_vs_differentiated | paired | participant_id | 4 | 4 | 4 |
| GSE292369_exercise_ketone_recovery | exercised_vs_rest | paired_intersection | participant+treatment | 16 | 18 | 16 |
| GSE305038_activity_inactivity_exercise | active_post_vs_active_pre | paired_intersection | participant_id | 6 | 6 | 4 |
| GSE305038_activity_inactivity_exercise | inactive_post_vs_inactive_pre | paired_intersection | participant_id | 6 | 7 | 6 |
| GSE312393_24h_exercise | 24h_exercise_vs_control | unpaired |  | 4 | 3 | 0 |
| GSE312393_6weeks_training | post_training_vs_pre_training | paired | participant | 3 | 3 | 3 |
| GSE318937_exercise_oleuropein | MICE_active_24h_vs_pre | paired | participant_id | 10 | 10 | 10 |
| GSE318937_exercise_oleuropein | MICE_active_post_vs_pre | paired | participant_id | 10 | 10 | 10 |
| GSE318937_exercise_oleuropein | MICE_placebo_24h_vs_pre | paired_intersection | participant_id | 9 | 10 | 9 |
| GSE318937_exercise_oleuropein | MICE_placebo_post_vs_pre | paired_intersection | participant_id | 9 | 10 | 9 |
| GSE318937_exercise_oleuropein | SIE_active_24h_vs_pre | paired | participant_id | 10 | 10 | 10 |
| GSE318937_exercise_oleuropein | SIE_active_post_vs_pre | paired | participant_id | 10 | 10 | 10 |
| GSE318937_exercise_oleuropein | SIE_placebo_24h_vs_pre | paired | participant_id | 10 | 10 | 10 |
| GSE318937_exercise_oleuropein | SIE_placebo_post_vs_pre | paired | participant_id | 10 | 10 | 10 |
| GSE32575_monocytes_obesity_surgery | obese_after_vs_obese_before | paired | participant_id | 18 | 18 | 18 |
| GSE32575_monocytes_obesity_surgery | obese_before_vs_lean | unpaired_independent_unit_mean |  | 12 | 18 | 0 |

## Direction summary

| metric | positive_delta_contrasts | negative_delta_contrasts | total_contrasts |
| --- | --- | --- | --- |
| NAMPT_z | 17 | 2 | 19 |
| balance_score | 5 | 14 | 19 |
| inflammatory_score | 14 | 5 | 19 |
| repair_score | 7 | 12 | 19 |

## CI-supported directional candidates

These rows have a bootstrap 95% CI that does not cross zero. They are candidates for main or supplementary figure annotation after biological review.

| dataset_id | contrast | metric | analysis_design | analysis_n | mean_delta | ci95_low | ci95_high | p_value | q_value_metric | evidence_flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GSE318937_exercise_oleuropein | MICE_active_post_vs_pre | NAMPT_z | paired | 10 | 1.173 | 0.6994 | 1.654 | 0.003906 | 0.05885 | ci_excludes_zero;nominal_p_lt_0.05;metric_fdr_lt_0.10 |
| GSE318937_exercise_oleuropein | MICE_placebo_24h_vs_pre | NAMPT_z | paired_intersection | 9 | 1.11 | 0.5722 | 1.69 | 0.007812 | 0.05885 | small_n;ci_excludes_zero;nominal_p_lt_0.05;metric_fdr_lt_0.10 |
| GSE318937_exercise_oleuropein | SIE_placebo_24h_vs_pre | NAMPT_z | paired | 10 | 1.307 | 0.5704 | 2.075 | 0.01172 | 0.05885 | ci_excludes_zero;nominal_p_lt_0.05;metric_fdr_lt_0.10 |
| GSE292369_exercise_ketone_recovery | exercised_vs_rest | NAMPT_z | paired_intersection | 16 | 0.8474 | 0.28 | 1.452 | 0.01239 | 0.05885 | ci_excludes_zero;nominal_p_lt_0.05;metric_fdr_lt_0.10 |
| GSE318937_exercise_oleuropein | MICE_active_24h_vs_pre | NAMPT_z | paired | 10 | 1.297 | 0.3382 | 2.56 | 0.02344 | 0.0804 | ci_excludes_zero;nominal_p_lt_0.05;metric_fdr_lt_0.10 |
| GSE318937_exercise_oleuropein | SIE_active_24h_vs_pre | NAMPT_z | paired | 10 | 0.9832 | 0.3272 | 1.659 | 0.02539 | 0.0804 | ci_excludes_zero;nominal_p_lt_0.05;metric_fdr_lt_0.10 |
| GSE32575_monocytes_obesity_surgery | obese_before_vs_lean | NAMPT_z | unpaired_independent_unit_mean | 24 | 0.9231 | 0.3255 | 1.514 | 0.0298 | 0.08088 | ci_excludes_zero;nominal_p_lt_0.05;metric_fdr_lt_0.10 |
| GSE282850_muscle_cell_aicar_palmitate | palmitate_vs_differentiated | NAMPT_z | paired | 4 | 0.5426 | 0.2247 | 0.7837 | 0.125 | 0.2721 | very_small_n;ci_excludes_zero |
| GSE282850_muscle_cell_aicar_palmitate | aicar_vs_differentiated | NAMPT_z | paired_intersection | 3 | 0.6974 | 0.04596 | 1.371 | 0.25 | 0.3958 | very_small_n;ci_excludes_zero |
| GSE312393_6weeks_training | post_training_vs_pre_training | NAMPT_z | paired | 3 | 1.107 | 0.5387 | 1.643 | 0.25 | 0.3958 | very_small_n;ci_excludes_zero |
| GSE292369_exercise_ketone_recovery | exercised_vs_rest | balance_score | paired_intersection | 16 | -0.3608 | -0.4974 | -0.2305 | 0.0002441 | 0.004639 | ci_excludes_zero;nominal_p_lt_0.05;metric_fdr_lt_0.10 |
| GSE318937_exercise_oleuropein | MICE_active_post_vs_pre | balance_score | paired | 10 | -1.069 | -1.428 | -0.723 | 0.001953 | 0.01237 | ci_excludes_zero;nominal_p_lt_0.05;metric_fdr_lt_0.10 |
| GSE318937_exercise_oleuropein | SIE_active_post_vs_pre | balance_score | paired | 10 | -0.4747 | -0.714 | -0.2731 | 0.001953 | 0.01237 | ci_excludes_zero;nominal_p_lt_0.05;metric_fdr_lt_0.10 |
| GSE318937_exercise_oleuropein | SIE_placebo_post_vs_pre | balance_score | paired | 10 | -0.5004 | -0.6758 | -0.2875 | 0.003906 | 0.01855 | ci_excludes_zero;nominal_p_lt_0.05;metric_fdr_lt_0.10 |
| GSE32575_monocytes_obesity_surgery | obese_after_vs_obese_before | balance_score | paired | 18 | -0.2131 | -0.394 | -0.05639 | 0.01965 | 0.07465 | ci_excludes_zero;nominal_p_lt_0.05;metric_fdr_lt_0.10 |
| GSE305038_activity_inactivity_exercise | inactive_post_vs_inactive_pre | balance_score | paired_intersection | 6 | -0.4203 | -0.6075 | -0.2105 | 0.03125 | 0.09896 | small_n;ci_excludes_zero;nominal_p_lt_0.05;metric_fdr_lt_0.10 |
| GSE318937_exercise_oleuropein | MICE_placebo_post_vs_pre | balance_score | paired_intersection | 9 | -0.5755 | -0.998 | -0.05425 | 0.05859 | 0.159 | small_n;ci_excludes_zero |
| GSE312393_6weeks_training | post_training_vs_pre_training | balance_score | paired | 3 | 0.2694 | 0.07035 | 0.5007 | 0.25 | 0.5278 | very_small_n;ci_excludes_zero |
| GSE32575_monocytes_obesity_surgery | obese_after_vs_obese_before | inflammatory_score | paired | 18 | 0.8198 | 0.4787 | 1.147 | 0.0003891 | 0.007393 | ci_excludes_zero;nominal_p_lt_0.05;metric_fdr_lt_0.10 |
| GSE292369_exercise_ketone_recovery | exercised_vs_rest | inflammatory_score | paired_intersection | 16 | 0.2648 | 0.1337 | 0.4035 | 0.0009766 | 0.009277 | ci_excludes_zero;nominal_p_lt_0.05;metric_fdr_lt_0.10 |
| GSE272133_muscle_bariatric | T2D_w52_vs_T2D_w0 | inflammatory_score | paired | 13 | 0.1757 | 0.06006 | 0.2965 | 0.01978 | 0.1252 | ci_excludes_zero;nominal_p_lt_0.05 |
| GSE318937_exercise_oleuropein | MICE_active_post_vs_pre | inflammatory_score | paired | 10 | 0.4724 | 0.09342 | 0.8434 | 0.04492 | 0.2134 | ci_excludes_zero;nominal_p_lt_0.05 |
| GSE312393_24h_exercise | 24h_exercise_vs_control | inflammatory_score | unpaired | 7 | -0.3047 | -0.6118 | -0.04423 | 0.1714 | 0.4653 | small_n;ci_excludes_zero |
| GSE32575_monocytes_obesity_surgery | obese_after_vs_obese_before | repair_score | paired | 18 | 0.6067 | 0.1977 | 1.03 | 0.01392 | 0.1162 | ci_excludes_zero;nominal_p_lt_0.05 |
| GSE318937_exercise_oleuropein | MICE_active_post_vs_pre | repair_score | paired | 10 | -0.5961 | -1.006 | -0.2271 | 0.01562 | 0.1162 | ci_excludes_zero;nominal_p_lt_0.05 |
| GSE292369_exercise_ketone_recovery | exercised_vs_rest | repair_score | paired_intersection | 16 | -0.09601 | -0.163 | -0.02658 | 0.01834 | 0.1162 | ci_excludes_zero;nominal_p_lt_0.05 |
| GSE272133_muscle_bariatric | T2D_w52_vs_T2D_w0 | repair_score | paired | 13 | 0.2956 | 0.07096 | 0.4959 | 0.02686 | 0.1276 | ci_excludes_zero;nominal_p_lt_0.05 |
| GSE282850_muscle_cell_aicar_palmitate | palmitate_vs_differentiated | repair_score | paired | 4 | 0.1789 | 0.06012 | 0.2976 | 0.125 | 0.3393 | very_small_n;ci_excludes_zero |
| GSE305038_activity_inactivity_exercise | active_post_vs_active_pre | repair_score | paired_intersection | 4 | -0.1452 | -0.227 | -0.06327 | 0.125 | 0.3393 | very_small_n;ci_excludes_zero |

## Output files

- `data_audit/outputs/nampt_axis_formal_contrast_stats.csv`
- `data_audit/outputs/figure_sources/figure2_dataset_coverage.csv`
- `data_audit/outputs/figure_sources/figure3_exercise_axis_contrasts.csv`
- `data_audit/outputs/figure_sources/figure4_obesity_axis_contrasts.csv`

## Interpretation boundary

The current evidence supports a public-data, transcriptomic, state-dependent NAMPT-axis model. It does not establish eNAMPT directionality, plasma NAMPT performance, exercise prescription thresholds, or causality. Those claims require protein/secretion data, clinical covariates, and prospective validation.
