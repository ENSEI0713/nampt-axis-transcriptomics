# NAMPT-axis internal immune-gene burden sensitivity

Generated: 2026-09-18T03:17:07+00:00

IMPORTANT SCOPE: the saved axis expression matrices contain only the
59 NAMPT-axis genes. This is NOT a cell-type deconvolution. The 'immune'
and 'macro/mono' columns are the within-axis immune-gene burden proxy
(mean z of axis genes that also appear in the marker list), not an
estimate of leukocyte abundance. Columns that are empty ('—') mean the
marker genes are not present in the 59-gene axis matrix.

Correlation between each NAMPT-axis score and the axis-internal immune
burden proxy across samples within dataset. High positive r for
inflammatory_score indicates that the inflammatory program is largely
carried by its own immune genes in that dataset; this qualifies (but
does not replace) interpretation, and must be disclosed in the paper.

## Pearson r (axis score vs axis-internal immune burden proxy), by dataset

| dataset | n | metric | immune_pan | macro/mono | adipocyte |
|---|---|---|---|---|---|
| GSE272133_muscle_bariatric | 51 | NAMPT_z | +0.49 | +0.55 | +0.29 |
| GSE272133_muscle_bariatric | 51 | inflammatory_score | +0.82 | +0.89 | +0.55 |
| GSE272133_muscle_bariatric | 51 | repair_score | +0.65 | +0.72 | +0.49 |
| GSE272133_muscle_bariatric | 51 | balance_score | +0.03 | +0.06 | +0.13 |

| GSE282850_muscle_cell_aicar_palmitate | 14 | NAMPT_z | -0.39 | +0.12 | +0.85 |
| GSE282850_muscle_cell_aicar_palmitate | 14 | inflammatory_score | +0.88 | +0.54 | -0.39 |
| GSE282850_muscle_cell_aicar_palmitate | 14 | repair_score | +0.15 | +0.45 | +0.60 |
| GSE282850_muscle_cell_aicar_palmitate | 14 | balance_score | -0.67 | -0.23 | +0.63 |

| GSE292369_exercise_ketone_recovery | 33 | NAMPT_z | -0.14 | +0.29 | -0.13 |
| GSE292369_exercise_ketone_recovery | 33 | inflammatory_score | +0.40 | +0.73 | -0.04 |
| GSE292369_exercise_ketone_recovery | 33 | repair_score | +0.07 | -0.10 | +0.11 |
| GSE292369_exercise_ketone_recovery | 33 | balance_score | -0.33 | -0.69 | +0.08 |

| GSE294150_visceral_adipose | 39 | NAMPT_z | -0.33 | -0.00 | +0.30 |
| GSE294150_visceral_adipose | 39 | inflammatory_score | +0.51 | +0.69 | -0.70 |
| GSE294150_visceral_adipose | 39 | repair_score | -0.03 | +0.25 | +0.40 |
| GSE294150_visceral_adipose | 39 | balance_score | -0.45 | -0.46 | +0.82 |

| GSE305038_activity_inactivity_exercise | 24 | NAMPT_z | +0.31 | +0.39 | +0.17 |
| GSE305038_activity_inactivity_exercise | 24 | inflammatory_score | +0.68 | +0.77 | +0.57 |
| GSE305038_activity_inactivity_exercise | 24 | repair_score | +0.44 | +0.57 | +0.47 |
| GSE305038_activity_inactivity_exercise | 24 | balance_score | -0.50 | -0.35 | -0.09 |

| GSE312393_24h_exercise | 6 | NAMPT_z | +0.51 | +0.46 | +0.33 |
| GSE312393_24h_exercise | 6 | inflammatory_score | +0.47 | +0.61 | +0.47 |
| GSE312393_24h_exercise | 6 | repair_score | -0.22 | -0.38 | +0.11 |
| GSE312393_24h_exercise | 6 | balance_score | -0.42 | -0.61 | -0.21 |

| GSE312393_6weeks_training | 5 | NAMPT_z | +0.27 | +0.17 | +0.66 |
| GSE312393_6weeks_training | 5 | inflammatory_score | +0.95 | +0.91 | +0.57 |
| GSE312393_6weeks_training | 5 | repair_score | +0.62 | +0.36 | +0.39 |
| GSE312393_6weeks_training | 5 | balance_score | -0.40 | -0.67 | -0.21 |

| GSE318937_exercise_oleuropein | 118 | NAMPT_z | +0.28 | +0.25 | -0.02 |
| GSE318937_exercise_oleuropein | 118 | inflammatory_score | +0.82 | +0.89 | +0.51 |
| GSE318937_exercise_oleuropein | 118 | repair_score | +0.31 | +0.38 | +0.37 |
| GSE318937_exercise_oleuropein | 118 | balance_score | -0.59 | -0.59 | -0.18 |

| GSE32575_monocytes_obesity_surgery | 47 | NAMPT_z | +0.60 | +0.75 | +0.61 |
| GSE32575_monocytes_obesity_surgery | 47 | inflammatory_score | +0.89 | +0.91 | +0.66 |
| GSE32575_monocytes_obesity_surgery | 47 | repair_score | +0.78 | +0.71 | +0.76 |
| GSE32575_monocytes_obesity_surgery | 47 | balance_score | -0.17 | -0.38 | +0.27 |
