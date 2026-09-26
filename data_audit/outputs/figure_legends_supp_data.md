# Figure legends + Supplementary Data manifest（投稿版）

> 目标期刊 Nature Communications（图注 ≤350 词/条，显示项 ≤10，标题 ≤15 词无标点，Abstract ≤150 词无引用）。
> 主文图候选源文件：`data_audit/outputs/figures_phase2/`；Phase 3 R/tidyplots 复核图件：`data_audit/outputs/figures_phase3_tidyplots/`。投稿前以最终 QC 选定唯一版本。
> 编号方案：投稿编号按正文首次出现顺序重排（原文件名 → 投稿编号见下）。
> 数据文件映射：Supplementary Data 1-8 对应 Methods 中 8 处引用（文件均在 `data_audit/outputs/` 下核实存在）。

---

## 图编号映射（6 图 ≤10 显示项 ✅）

| 投稿编号 | 原文件名 | 内容 | 面板 |
| --- | --- | --- | --- |
| Figure 1 | figure1_framework | 概念框架 | a-f（6 面板） |
| Figure 2 | figure2_public_data_framework | 公共数据证据基与分析设计 | a-c |
| Figure 3 | figure3_exercise_nampt_axis | 运动层 NAMPT 轴动态 | a-c |
| Figure 4 | figure3_meta_forest | 随机效应 meta（strata + 森林图） | a-b |
| Figure 5 | figure4_obesity_nampt_axis | 肥胖/减重层 | a-c |
| Figure 6 | figure5_evo2_prioritization | Evo2 变异优先级（探索性） | a-c |

---

## Figure legends（投稿稿插入正文用）

### Figure 1 | State-dependent NAMPT-axis framework.
**a**, Dual identity of NAMPT: intracellular NAMPT supports NAD salvage and repair; extracellular NAMPT (eNAMPT/visfatin) is linked to NF-κB and monocyte/macrophage activation. **b**, The state-dependent axis model: the same NAMPT upregulation can be inflammation-like or repair-like depending on tissue, time and metabolic background. **c**, Multi-layer public-data evidence base (9 transcriptomic units, 337 samples; exercise, obesity/weight-loss, cell model). **d**, Repair-program genes (NAD salvage, sirtuin, mitochondrial, DNA-repair modules). **e**, Inflammatory-program genes (NF-κB, innate immune, monocyte/macrophage modules). NAMPT itself belongs to both repair and inflammatory programs. **f**, Balance score (repair − inflammatory) across representative states.

### Figure 2 | Public transcriptomic evidence base and analysis design.
**a**, NAMPT-axis gene coverage across the 9 analysis units (59-gene axis; most datasets 100%, GSE305038 84.7%, GSE282850 79.7%); point size is proportional to sample size. **b**, Analysis design: bar chart of predefined contrasts by pairing type — 17 paired/intersection contrasts vs 2 unpaired. **c**, Evidence density by axis metric: number of contrasts with CI excluding 0 and with FDR < 0.10.

### Figure 3 | Exercise-induced NAMPT axis: acute stress and training adaptation.
**a**, NAMPT_z, inflammatory, repair and balance scores across exercise cohorts (13 contrasts plotted: 12 paired contrasts plus one unpaired acute vs 24 h comparison in GSE312393; 4 datasets). The unpaired display contrast is descriptive and is not included in the paired exercise meta-analysis. **b**, Immediate stress bias relaxes by 24 h (GSE318937 immediate vs 24h); NAMPT_z remains elevated at 24 h in most contrasts (Fig. 3a). **c**, Dataset-level summaries; acute inflammation-like signal mainly driven by NF-κB/cytokine modules (Phase 1b consistency).

### Figure 4 | Cross-dataset validation of the NAMPT axis.
**a**, Contrast-level random-effects estimates across exercise, obesity and cell-model strata; cell-model results are directional evidence from one dataset. **b**, Dataset-level cluster-aware estimates for exercise and obesity, with the number of independent datasets shown as k. **c**, Exercise leave-one-dataset-out robustness across the four NAMPT-axis metrics. The exercise contrast-level meta-analysis uses 12 paired contrasts.

### Figure 5 | Obesity and weight-loss tissue and disease-background dependence.
**a**, Four obesity/weight-loss contrasts across monocyte and skeletal-muscle units, shown with metric-specific estimates and confidence intervals. **b**, Post-bariatric monocyte remodeling (GSE32575). **c**, Skeletal-muscle responses in obese and T2D states (GSE272133). Cell-model AICAR/palmitate contrasts are reported separately as supplementary evidence.

### Figure 6 | Exploratory Evo2-40B regulatory-variant extension.
**a**, Exploratory computational workflow from candidate construction through Evo2 scoring and external evidence integration. **b**, Candidate-set composition across 432 priority variants. **c**, Tier distribution (A = 0, B = 0, C = 97, External-only = 9, Excluded = 326), reported as exploratory evidence rather than a validated mechanism or causal ranking.

---

## Supplementary Data manifest（投稿附件，14 份）

| Supp Data | 内容 | 源文件（已核实存在） |
| --- | --- | --- |
| Supplementary Data 1 | 样本级评分、下载清单、基因覆盖 | `nampt_axis_sample_scores.csv`（346 条分析记录；对应 337 个正式去重样本）、`geo_sample_metadata_long.csv`（351 行 provenance metadata）、`geo_processed_download_manifest.csv`、`nampt_axis_gene_coverage.csv` |
| Supplementary Data 2 | NAMPT 轴基因集 v1 | `NAMPT_axis_gene_set_v1.csv`（59 基因） |
| Supplementary Data 3 | 预设对照与正式对比统计 | `nampt_axis_predefined_contrasts.csv`（19）、`nampt_axis_formal_contrast_stats.csv` |
| Supplementary Data 4 | 随机效应 meta 结果 + 聚类感知/LODO 敏感性 | `meta/meta_results.csv`、`meta/meta_sensitivity_dataset_level.csv`、`meta/meta_sensitivity_lodo.csv` |
| Supplementary Data 5 | 模块一致性（Cronbach α、模块相关） | `axis_structure/module_alpha.csv`、`module_corr_matrix.csv` |
| Supplementary Data 6 | Phase 1b 敏感性（9 变体） | `phase1b_sensitivity/nampt_axis_sensitivity_*.csv` |
| Supplementary Data 7 | Moderator 字段覆盖 | `meta/moderator_coverage.csv` |
| Supplementary Data 8 | Evo2 打分与 Tier 分层 | `evo2/candidates_priority.csv`、`scores.csv`、`scores_B.csv`、`scores_C.csv`、`tiers.csv` |
| Supplementary Data 9 | 基因/模块清单与表达文件可用性 | `supplementary_evidence/Supplementary_Data_9_gene_module_inventory.xlsx`、`Supplementary_Data_9_expression_file_inventory.csv` |
| Supplementary Data 10 | 模块结构（Cronbach α、模块相关） | `supplementary_evidence/Supplementary_Data_10_module_structure.xlsx` |
| Supplementary Data 11 | Phase 1b sensitivity atlas | `supplementary_evidence/Supplementary_Data_11_sensitivity_atlas.xlsx` |
| Supplementary Data 12 | Evo2 + GTEx/GWAS 全量证据表（432 候选） | `supplementary_evidence/Supplementary_Data_12_evo2_external_evidence.xlsx` |
| Supplementary Data 13 | 样本级轨迹重建记录（346 条分析记录） | `supplementary_evidence/Supplementary_Data_13_sample_trajectory_records.xlsx` |
| Supplementary Data 14 | 19 contrasts × 4 metrics formal statistics | `supplementary_evidence/Supplementary_Data_14_formal_contrast_statistics.xlsx` |

> 说明：投稿时把上述 CSV 打包为 8 个 Supplementary Data 文件（xlsx/csv），并在 Data Availability 中列出；
> 图件用 tiff/png（NC 要求 300 dpi 以上）与源数据（figure_sources/）一并提交。

---

*初版 2026-09-20；口径与补充证据扩充于 2026-09-25 更新。定量图正式迁移使用 R/tidyplots；当前 `figures_phase3_tidyplots/` 为原型输出，不等同于最终主文图。*
