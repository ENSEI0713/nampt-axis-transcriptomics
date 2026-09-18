# NAMPT-axis Phase 1b sensitivity report

## Scope

This report tests whether Phase 1 transcriptomic NAMPT-axis results are driven by a small set of high-profile genes or modules. Scores are recomputed from saved per-dataset expression matrices, then the same predefined contrasts and paired/unpaired rules are rerun. Original Phase 1 files are not overwritten.

## Variants tested

| sensitivity_variant | variant_type | excluded_genes | excluded_modules |
| --- | --- | --- | --- |
| primary | baseline |  |  |
| drop_nampt | gene_drop | NAMPT |  |
| drop_classic_cytokines | gene_drop | CCL2;CXCL8;IL1B;IL6;TNF |  |
| drop_nfkb_module | module_drop |  | nfkb_inflammation |
| drop_monocyte_macrophage | module_drop |  | monocyte_macrophage |
| drop_nad_salvage_core | module_drop |  | nad_salvage_core |
| drop_nad_consumption | module_drop |  | nad_consumption_inflammation;nad_consumption_repair |
| drop_mito_repair | module_drop |  | ampk_mitochondria_repair;mitochondrial_biogenesis;mitochondrial_stress;oxidative_stress_repair;sirtuin_repair |
| drop_autophagy_dna_repair | module_drop |  | autophagy_repair;dna_damage_repair |
| drop_insulin_adipose_metabolism | module_drop |  | adipose_metabolism_inflammation;adipose_metabolism_resolution;insulin_metabolism |

## Primary recompute audit

The primary sensitivity score should reproduce the original Phase 1 sample-level scores. Very small floating point differences are expected.

| metric | matched_samples | max_abs_difference | median_abs_difference |
| --- | --- | --- | --- |
| NAMPT_z | 346 | 6.661e-15 | 1.11e-16 |
| inflammatory_score | 346 | 1.901e-15 | 3.331e-16 |
| repair_score | 346 | 2.054e-15 | 6.106e-16 |
| balance_score | 346 | 2.276e-15 | 5.829e-16 |

## Overall stability versus primary

| sensitivity_variant | direction_agreement_pct | direction_flips | primary_ci_supported | ci_support_retained | ci_support_lost | ci_support_gained | median_abs_delta_difference |
| --- | --- | --- | --- | --- | --- | --- | --- |
| drop_nampt | 100 | 0 | 29 | 29 | 0 | 0 | 0 |
| drop_monocyte_macrophage | 93.42 | 5 | 29 | 28 | 1 | 0 | 0.01068 |
| drop_autophagy_dna_repair | 93.42 | 5 | 29 | 26 | 3 | 2 | 0.02398 |
| drop_nad_salvage_core | 92.11 | 6 | 29 | 27 | 2 | 1 | 0.01333 |
| drop_insulin_adipose_metabolism | 90.79 | 7 | 29 | 29 | 0 | 0 | 0.02337 |
| drop_mito_repair | 90.79 | 7 | 29 | 28 | 1 | 2 | 0.05082 |
| drop_nad_consumption | 89.47 | 8 | 29 | 27 | 2 | 3 | 0.05159 |
| drop_classic_cytokines | 89.47 | 8 | 29 | 24 | 5 | 3 | 0.04015 |
| drop_nfkb_module | 84.21 | 12 | 29 | 20 | 9 | 3 | 0.06029 |

## Metric-level stability

| sensitivity_variant | metric | direction_agreement_pct | direction_flips | primary_ci_supported | variant_ci_supported | ci_support_retained | ci_support_lost | ci_support_gained | median_abs_delta_difference | median_relative_abs_delta_difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| drop_autophagy_dna_repair | NAMPT_z | 100 | 0 | 10 | 10 | 10 | 0 | 0 | 0 | 0 |
| drop_classic_cytokines | NAMPT_z | 100 | 0 | 10 | 10 | 10 | 0 | 0 | 0 | 0 |
| drop_insulin_adipose_metabolism | NAMPT_z | 100 | 0 | 10 | 10 | 10 | 0 | 0 | 0 | 0 |
| drop_mito_repair | NAMPT_z | 100 | 0 | 10 | 10 | 10 | 0 | 0 | 0 | 0 |
| drop_monocyte_macrophage | NAMPT_z | 100 | 0 | 10 | 10 | 10 | 0 | 0 | 0 | 0 |
| drop_nad_consumption | NAMPT_z | 100 | 0 | 10 | 11 | 10 | 0 | 1 | 0 | 0 |
| drop_nad_salvage_core | NAMPT_z | 100 | 0 | 10 | 11 | 10 | 0 | 1 | 0 | 0 |
| drop_nampt | NAMPT_z | 100 | 0 | 10 | 10 | 10 | 0 | 0 | 0 | 0 |
| drop_nfkb_module | NAMPT_z | 100 | 0 | 10 | 10 | 10 | 0 | 0 | 0 | 0 |
| drop_nampt | balance_score | 100 | 0 | 8 | 8 | 8 | 0 | 0 | 0 | 0 |
| drop_insulin_adipose_metabolism | balance_score | 89.47 | 2 | 8 | 8 | 8 | 0 | 0 | 0.04002 | 0.2695 |
| drop_mito_repair | balance_score | 73.68 | 5 | 8 | 8 | 8 | 0 | 0 | 0.08853 | 0.5831 |
| drop_autophagy_dna_repair | balance_score | 89.47 | 2 | 8 | 8 | 7 | 1 | 1 | 0.03898 | 0.4314 |
| drop_monocyte_macrophage | balance_score | 84.21 | 3 | 8 | 7 | 7 | 1 | 0 | 0.02137 | 0.3294 |
| drop_nad_consumption | balance_score | 78.95 | 4 | 8 | 7 | 7 | 1 | 0 | 0.08705 | 0.4033 |
| drop_nad_salvage_core | balance_score | 78.95 | 4 | 8 | 7 | 7 | 1 | 0 | 0.02665 | 0.1643 |
| drop_classic_cytokines | balance_score | 73.68 | 5 | 8 | 5 | 5 | 3 | 0 | 0.08029 | 0.5928 |
| drop_nfkb_module | balance_score | 68.42 | 6 | 8 | 4 | 3 | 5 | 1 | 0.1206 | 0.7755 |
| drop_mito_repair | inflammatory_score | 100 | 0 | 5 | 5 | 5 | 0 | 0 | 0.02008 | 0.1513 |
| drop_nad_salvage_core | inflammatory_score | 100 | 0 | 5 | 5 | 5 | 0 | 0 | 0 | 0 |
| drop_nampt | inflammatory_score | 100 | 0 | 5 | 5 | 5 | 0 | 0 | 0 | 0 |
| drop_autophagy_dna_repair | inflammatory_score | 94.74 | 1 | 5 | 5 | 5 | 0 | 0 | 0.01419 | 0.1148 |
| drop_insulin_adipose_metabolism | inflammatory_score | 94.74 | 1 | 5 | 5 | 5 | 0 | 0 | 0.01772 | 0.07191 |
| drop_monocyte_macrophage | inflammatory_score | 89.47 | 2 | 5 | 5 | 5 | 0 | 0 | 0.02137 | 0.2178 |
| drop_nad_consumption | inflammatory_score | 84.21 | 3 | 5 | 5 | 4 | 1 | 1 | 0.09084 | 0.6019 |
| drop_classic_cytokines | inflammatory_score | 84.21 | 3 | 5 | 6 | 3 | 2 | 3 | 0.08029 | 0.8002 |
| drop_nfkb_module | inflammatory_score | 68.42 | 6 | 5 | 3 | 1 | 4 | 2 | 0.1206 | 1.107 |
| drop_classic_cytokines | repair_score | 100 | 0 | 6 | 6 | 6 | 0 | 0 | 0 | 0 |
| drop_monocyte_macrophage | repair_score | 100 | 0 | 6 | 6 | 6 | 0 | 0 | 0 | 0 |
| drop_nampt | repair_score | 100 | 0 | 6 | 6 | 6 | 0 | 0 | 0 | 0 |
| drop_nfkb_module | repair_score | 100 | 0 | 6 | 6 | 6 | 0 | 0 | 0 | 0 |
| drop_nad_consumption | repair_score | 94.74 | 1 | 6 | 7 | 6 | 0 | 1 | 0.01612 | 0.08577 |
| drop_insulin_adipose_metabolism | repair_score | 78.95 | 4 | 6 | 6 | 6 | 0 | 0 | 0.02902 | 0.1834 |
| drop_mito_repair | repair_score | 89.47 | 2 | 6 | 7 | 5 | 1 | 2 | 0.08156 | 0.4013 |
| drop_nad_salvage_core | repair_score | 89.47 | 2 | 6 | 5 | 5 | 1 | 0 | 0.02665 | 0.1722 |
| drop_autophagy_dna_repair | repair_score | 89.47 | 2 | 6 | 5 | 4 | 2 | 1 | 0.03377 | 0.1232 |

## CI-supported rows that become fragile

Rows listed here had a primary 95% CI excluding zero but did not retain same-direction CI support under a sensitivity variant. These are wording-caution rows, not automatic exclusions.

| sensitivity_variant | dataset_id | contrast | metric | mean_delta_primary | mean_delta | delta_difference_vs_primary | p_value | q_value_metric |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| drop_autophagy_dna_repair | GSE312393_6weeks_training | post_training_vs_pre_training | balance_score | 0.2694 | 0.2717 | 0.002231 | 0.5 | 0.8214 |
| drop_classic_cytokines | GSE312393_6weeks_training | post_training_vs_pre_training | balance_score | 0.2694 | 0.08227 | -0.1872 | 0.5 | 0.8636 |
| drop_classic_cytokines | GSE318937_exercise_oleuropein | MICE_placebo_post_vs_pre | balance_score | -0.5755 | -0.1956 | 0.3799 | 0.375 | 0.8636 |
| drop_classic_cytokines | GSE318937_exercise_oleuropein | SIE_placebo_post_vs_pre | balance_score | -0.5004 | -0.2072 | 0.2932 | 0.1152 | 0.3649 |
| drop_monocyte_macrophage | GSE312393_6weeks_training | post_training_vs_pre_training | balance_score | 0.2694 | 0.2756 | 0.006144 | 0.5 | 0.942 |
| drop_nad_consumption | GSE312393_6weeks_training | post_training_vs_pre_training | balance_score | 0.2694 | 0.3004 | 0.03092 | 0.5 | 0.7917 |
| drop_nad_salvage_core | GSE318937_exercise_oleuropein | MICE_placebo_post_vs_pre | balance_score | -0.5755 | -0.5491 | 0.02642 | 0.08594 | 0.2333 |
| drop_nfkb_module | GSE292369_exercise_ketone_recovery | exercised_vs_rest | balance_score | -0.3608 | -0.0677 | 0.2931 | 0.2334 | 0.6334 |
| drop_nfkb_module | GSE312393_6weeks_training | post_training_vs_pre_training | balance_score | 0.2694 | 0.1909 | -0.07849 | 0.5 | 0.663 |
| drop_nfkb_module | GSE318937_exercise_oleuropein | MICE_placebo_post_vs_pre | balance_score | -0.5755 | -0.1292 | 0.4463 | 0.5234 | 0.663 |
| drop_nfkb_module | GSE318937_exercise_oleuropein | SIE_active_post_vs_pre | balance_score | -0.4747 | -0.1802 | 0.2945 | 0.1738 | 0.5505 |
| drop_nfkb_module | GSE318937_exercise_oleuropein | SIE_placebo_post_vs_pre | balance_score | -0.5004 | -0.1926 | 0.3078 | 0.1621 | 0.5505 |
| drop_classic_cytokines | GSE312393_24h_exercise | 24h_exercise_vs_control | inflammatory_score | -0.3047 | -0.3483 | -0.04361 | 0.1143 | 0.5429 |
| drop_classic_cytokines | GSE318937_exercise_oleuropein | MICE_active_post_vs_pre | inflammatory_score | 0.4724 | 0.009495 | -0.4629 | 0.9727 | 0.9785 |
| drop_nad_consumption | GSE312393_24h_exercise | 24h_exercise_vs_control | inflammatory_score | -0.3047 | -0.1341 | 0.1706 | 0.6 | 0.9392 |
| drop_nfkb_module | GSE272133_muscle_bariatric | T2D_w52_vs_T2D_w0 | inflammatory_score | 0.1757 | 0.114 | -0.06176 | 0.1621 | 0.616 |
| drop_nfkb_module | GSE292369_exercise_ketone_recovery | exercised_vs_rest | inflammatory_score | 0.2648 | -0.02831 | -0.2931 | 0.6555 | 0.9234 |
| drop_nfkb_module | GSE312393_24h_exercise | 24h_exercise_vs_control | inflammatory_score | -0.3047 | -0.3725 | -0.06777 | 0.1429 | 0.616 |
| drop_nfkb_module | GSE318937_exercise_oleuropein | MICE_active_post_vs_pre | inflammatory_score | 0.4724 | -0.09501 | -0.5674 | 0.6426 | 0.9234 |
| drop_autophagy_dna_repair | GSE292369_exercise_ketone_recovery | exercised_vs_rest | repair_score | -0.09601 | -0.08853 | 0.007477 | 0.09738 | 0.37 |
| drop_autophagy_dna_repair | GSE305038_activity_inactivity_exercise | active_post_vs_active_pre | repair_score | -0.1452 | -0.09856 | 0.04659 | 0.25 | 0.5938 |
| drop_mito_repair | GSE282850_muscle_cell_aicar_palmitate | palmitate_vs_differentiated | repair_score | 0.1789 | 0.01803 | -0.1608 | 0.75 | 0.8906 |
| drop_nad_salvage_core | GSE292369_exercise_ketone_recovery | exercised_vs_rest | repair_score | -0.09601 | -0.03713 | 0.05888 | 0.3917 | 0.8636 |

## Minimum genes retained per variant

| sensitivity_variant | min_inflammatory_genes_used | min_repair_genes_used |
| --- | --- | --- |
| drop_autophagy_dna_repair | 16 | 27 |
| drop_classic_cytokines | 15 | 34 |
| drop_insulin_adipose_metabolism | 17 | 29 |
| drop_mito_repair | 16 | 21 |
| drop_monocyte_macrophage | 14 | 34 |
| drop_nad_consumption | 13 | 32 |
| drop_nad_salvage_core | 17 | 30 |
| drop_nampt | 17 | 34 |
| drop_nfkb_module | 13 | 34 |
| primary | 17 | 34 |

## Output files

- `data_audit/outputs/phase1b_sensitivity/nampt_axis_sensitivity_sample_scores.csv`
- `data_audit/outputs/phase1b_sensitivity/nampt_axis_sensitivity_contrast_stats.csv`
- `data_audit/outputs/phase1b_sensitivity/nampt_axis_sensitivity_comparison_to_primary.csv`
- `data_audit/outputs/phase1b_sensitivity/nampt_axis_sensitivity_summary.csv`
- `data_audit/outputs/phase1b_sensitivity/nampt_axis_sensitivity_gene_usage.csv`
- `data_audit/outputs/phase1b_sensitivity/nampt_axis_primary_recompute_audit.csv`

## Interpretation boundary

Stable transcriptomic sensitivity supports using the NAMPT-axis score as a public-data foundation for a state-dependent inflammatory-repair model. It still does not prove extracellular NAMPT protein directionality, NAD abundance, clinical inflammation state, or exercise-prescription thresholds. Those claims require Phase 2 protein/metabolite evidence and later validation.
