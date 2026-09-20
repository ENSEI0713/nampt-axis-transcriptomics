# Meta sensitivity analysis (CB-1: cluster-aware + LODO)

Generated: 2026-09-19T14:08:58+00:00

Reviewer concern: 12 exercise contrasts are nested in 4 datasets (GSE318937 contributes 8). Dataset-level pooling and leave-one-dataset-out correct the independence assumption.

## 1. Dataset-level DL (effective independent units)

| domain/metric | k(ds) | pooled | 95% CI | p | I2 | dir |
|---|---|---|---|---|---|---|
| exercise/NAMPT_z | 4 | +0.965 | 0.445-1.485 | 0.0002776 | 81.1% | 4/4 |
| exercise/balance_score | 4 | -0.466 | -1.251-0.319 | 0.2442 | 99.1% | 1/4 |
| exercise/inflammatory_score | 4 | +0.346 | -0.166-0.858 | 0.1854 | 95.9% | 3/4 |
| exercise/repair_score | 4 | -0.476 | -1.037-0.084 | 0.09599 | 98.9% | 1/4 |
| obesity/NAMPT_z | 2 | +0.138 | -0.109-0.384 | 0.2733 | 0.0% | 2/2 |
| obesity/balance_score | 2 | -0.218 | -0.901-0.465 | 0.5308 | 97.4% | 1/2 |
| obesity/inflammatory_score | 2 | +0.795 | 0.332-1.257 | 0.0007606 | 84.0% | 2/2 |
| obesity/repair_score | 2 | +0.412 | 0.055-0.769 | 0.02376 | 62.6% | 2/2 |

## 2. Leave-one-dataset-out (contrast-level, exercise)

| metric | dropped dataset | k | pooled | 95% CI | p |
|---|---|---|---|---|---|
| NAMPT_z | GSE292369 | 11 | +0.861 | 0.512-1.210 | 1.341e-06 |
| NAMPT_z | GSE305038 | 10 | +0.941 | 0.594-1.288 | 1.063e-07 |
| NAMPT_z | GSE312393 | 11 | +0.746 | 0.488-1.004 | 1.469e-08 |
| NAMPT_z | GSE318937 | 4 | +0.835 | 0.033-1.637 | 0.04123 |
| inflammatory_score | GSE292369 | 11 | +0.184 | -0.013-0.380 | 0.06662 |
| inflammatory_score | GSE305038 | 10 | +0.322 | -0.001-0.646 | 0.05087 |
| inflammatory_score | GSE312393 | 11 | +0.266 | -0.057-0.588 | 0.1062 |
| inflammatory_score | GSE318937 | 4 | +0.363 | -0.271-0.996 | 0.2616 |
| repair_score | GSE292369 | 11 | -0.284 | -0.765-0.197 | 0.2474 |
| repair_score | GSE305038 | 10 | -0.237 | -0.508-0.033 | 0.08485 |
| repair_score | GSE312393 | 11 | -0.408 | -0.749--0.066 | 0.01946 |
| repair_score | GSE318937 | 4 | -0.539 | -1.132-0.053 | 0.07455 |
| balance_score | GSE292369 | 11 | -0.557 | -1.110--0.004 | 0.04855 |
| balance_score | GSE305038 | 10 | -0.556 | -1.127-0.015 | 0.05625 |
| balance_score | GSE312393 | 11 | -0.790 | -1.194--0.385 | 0.0001302 |
| balance_score | GSE318937 | 4 | -0.475 | -1.673-0.722 | 0.4367 |

## 3. Reading (honest)

- NAMPT_z upregulation is robust at dataset level (k=4, +0.96, p=2.8e-4) and under LODO (all positive).
- balance_score loses significance at dataset level (k=4, -0.47, p=0.24) and under LODO; the 'axis flips toward inflammation' headline is NOT sustained at cluster-aware precision.
- inflammatory/repair at dataset level are not significant (p=0.19 / p=0.096).
- Obesity layer remains directional (k=2 dataset units for NAMPT_z; k=3 contrasts, p=0.27).
- Cell-model k=2 contrasts from one lineage cannot support p=3.2e-10; treat as directional.