# Moderator feasibility report

Generated: 2026-09-22T15:49:56+00:00

## Scope

样本级文件共 346 行，formal contrast 文件共 76 行，预定义 contrast 共 19 个。
本报告只做字段覆盖和单数据集内分层描述，不拟合跨研究 moderator 元回归。原因是 effect size 嵌套在数据集/受试者内，且没有统一的跨研究 moderator 编码与效应协方差。

## Moderator field coverage

| field | non-empty | total | missing % |
|---|---:|---:|---:|
| timepoint | 243 | 346 | 29.77 |
| exercise_type | 119 | 346 | 65.61 |
| nutrition_or_treatment | 119 | 346 | 65.61 |
| intervention | 259 | 346 | 25.14 |
| treatment | 178 | 346 | 48.55 |

## Within-dataset strata

### GSE318937

| exercise_type | nutrition_or_treatment | timepoint | n |
|---|---|---|---:|
| MICE | Active | Post | 10 |
| MICE | Active | Post24h | 10 |
| MICE | Active | Pre | 10 |
| MICE | Placebo | Post | 10 |
| MICE | Placebo | Post24h | 10 |
| MICE | Placebo | Pre | 9 |
| SIE | Active | Post | 10 |
| SIE | Active | Post24h | 10 |
| SIE | Active | Pre | 10 |
| SIE | Placebo | Post | 10 |
| SIE | Placebo | Post24h | 10 |
| SIE | Placebo | Pre | 10 |

### GSE305038

| condition | timepoint | n |
|---|---|---:|
| active_post | post | 6 |
| active_pre | pre | 6 |
| inactive_post | post | 7 |
| inactive_pre | pre | 6 |

### GSE312393

| dataset_id | condition | timepoint | n |
|---|---|---|---:|
| GSE312393_24h_exercise | 24h_exercise | 24h_post | 3 |
| GSE312393_24h_exercise | control | baseline | 4 |
| GSE312393_6weeks_training | post_training | post_6weeks | 3 |
| GSE312393_6weeks_training | pre_training | pre_training | 3 |

## Feasibility conclusion

- 可以做：GSE318937、GSE305038、GSE312393 内部的时间点/训练状态/干预背景描述。
- 当前不能做：把所有研究的 timepoint、training_status、nutrition_background 直接拼成统一跨研究元回归。
- 需要新增材料后才能做：逐 contrast moderator 编码、数据集聚类结构、重复测量效应协方差和预先定义的 moderator 模型。
- 因此本轮不报告正式 moderator p 值，不把 I² 本身解释为状态依赖性证据。
