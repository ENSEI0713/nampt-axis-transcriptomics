# Evidence manifest — NAMPT-axis manuscript

> Version: 2026-09-24. This manifest fixes the counting units used in the manuscript, figures and supplementary materials.

## Sample-count units

| Label | Value | Definition | Source | Permitted use |
|---|---:|---|---|---|
| Formal analysis samples | 337 | Unique samples across 9 transcriptomic analysis units after removing duplicate counting of the 13 GSE312393 samples represented in its acute-24 h and 6-week-training units | `nampt_axis_sample_scores.csv`; manuscript Methods §1.2 | Main-text headline sample count, abstract, figure overview |
| Sample-level score records | 346 | Rows in `nampt_axis_sample_scores.csv`; analysis-unit records, including duplicated representation of GSE312393 samples across the two analysis units | `nampt_axis_sample_scores.csv` | Supplementary data table size and audit description, never headline biological sample count |
| Long-format metadata rows | 351 | Rows in `geo_sample_metadata_long.csv`; metadata records before the formal analysis-unit deduplication/selection rules | `geo_sample_metadata_long.csv` | Provenance/moderator audit only, never sample-size claim |

## Contrast-count units

| Label | Value | Definition | Source | Permitted use |
|---|---:|---|---|---|
| Predefined contrasts | 19 | All prespecified comparisons across exercise, obesity/weight-loss and cell-model layers | `nampt_axis_predefined_contrasts.csv` | Study-design overview and Methods §3.1 |
| Exercise paired-meta contrasts | 12 | Paired contrasts nested in 4 exercise datasets and eligible for the exercise paired random-effects meta-analysis | `meta/meta_input_contrasts.csv`; `figure3_exercise_axis_contrasts.csv` | Meta-analysis claims, Figure 4 and paired exercise results |
| Exercise plotted contrasts | 13 | The 12 paired exercise contrasts plus the unpaired GSE312393 acute-24 h comparison shown for descriptive exercise dynamics | `figure3_exercise_axis_contrasts.csv` | Figure 3 display count only; not an independent-replication count |
| Formal metric-level rows | 76 | 19 contrasts × 4 axis metrics | `nampt_axis_formal_contrast_stats.csv` | Statistical output audit only |

## Figure-panel units

| Figure | Actual panels | Rule |
|---|---|---|
| Figure 1 | a–f | Conceptual framework; do not present conceptual arrows as causal measurements |
| Figure 2 | a–c | Evidence architecture and study design |
| Figure 3 | a–c | Exercise dynamics; panel a displays 13 contrasts, while paired meta claims remain n=12 |
| Figure 4 | a–b | Exercise meta-analysis and forest plot |
| Figure 5 | a–c | Obesity/weight-loss/tissue-background results; cell-model results remain separately identified |
| Figure 6 | a–c | Evo2 exploratory workflow, candidate composition and Tier distribution |

## Evidence boundaries

- `NAMPT mRNA` is not `eNAMPT protein`.
- No NAD metabolite abundance, NAD flux or eNAMPT secretion was measured.
- The 337 formal sample count is not the same as the 346 score-record rows or 351 metadata rows.
- The 13 plotted exercise contrasts must not be described as 13 independent studies or as the exercise meta-analysis sample; the paired meta uses 12 contrasts nested in 4 datasets.
- Evo2 is an exploratory regulatory-hypothesis prioritization module. Tier A/B are zero; Tier C is a hypothesis set, not a stable causal ranking.
