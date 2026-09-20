# 审稿包（Immutable review packet）— NAMPT-NAD 炎症-修复轴论文

本文件是模拟审稿的唯一不可变输入包。只含稿件事实、来源锚点与评估边界，不含任何分析结论或疑似问题。三份审稿报告均以本包为准。

## 1. 稿件范围与评估边界

- 输入范围：Results 全文（中文草稿 v2，`manuscript_results_v2_zh.md`）+ frontmatter（Introduction 4 段 + Abstract + Title 备选，`manuscript_frontmatter_v1_zh.md`）。
- 缺失材料（影响审稿置信度）：Methods 未成稿、图表未成稿、参考文献列表未成稿、英文全文未成稿。审稿只能基于现有文本与所列来源数字，对这些未提供材料不得臆测。
- 目标定位：logic 文档建议 Nature-family 子刊或计算/代谢/运动医学方向；审稿按 Nature 风格标准（原创性、科学重要性、跨学科读者、技术稳健性、非专业可读性）评估，但不做期刊接收决策。

## 2. 论文核心主张（来自稿件文本，非审稿结论）

1. NAMPT-NAD 系统是状态依赖的炎症-修复轴：慢性代谢压力下偏炎症程序，运动/训练背景下可转向修复。
2. 59 基因双程序评分框架可分开炎症/修复两侧，模块 Cronbach α 提供独立共表达支持。
3. 急性运动后 NAMPT_z 上调但 balance_score 转负：NAMPT 上升不自动等于修复（随机效应 meta）。
4. 肥胖/减重中 NAMPT 轴表现组织与疾病背景依赖；细胞模型中同样 NAMPT 上升可对应不同代谢刺激。
5. Evo2-40B 对 432 个 NAMPT 轴候选变异打分并与公共 eQTL/GWAS 分层；Tier A/B=0（如实报告），Evo2 降为补充/探索模块。

## 3. 稿件文本事实（可直接引用，行号即源）

### Results（manuscript_results_v2_zh.md）
- R1 框架：59 基因（repair 34 / inflammatory 19 / both 6），20 模块；9 个公共矩阵、337 样本；数据集内基因 z-score；模块 α：GSE272133（n=51）nad_salvage_core 0.79、sirtuin_repair 0.82、ampk_mitochondria_repair 0.83、oxidative_stress_repair 0.91、dna_damage_repair 0.86；GSE305038（n=24）α 均值 0.78；GSE32575（n=47）α 均值 0.60；小样本队列（GSE312393、GSE282850）负 α。
- R2 运动 meta：4 队列、12 配对对照、DerSimonian-Laird。NAMPT_z +0.85（CI 0.53–1.17，92% 方向一致，p=1.8e-7，I²=64%）；balance_score −0.62（CI −1.12–−0.12，83%，p=0.016，I²=98%）；inflammatory_score +0.28（p=0.07）；repair_score −0.33（CI −0.67–+0.00，p=0.05）。轴内免疫负荷：GSE318937（n=118）、GSE305038 全样本 inflammatory_score 与单核/巨噬负荷 r=0.77–0.89；24 h 后急性信号回落。
- R3 肥胖：meta 肥胖层 k=3 NAMPT_z +0.14（I²=0%）、inflammatory +0.57（67% 方向一致，高异质性）；GSE32575 肥胖 vs 瘦 NAMPT_z +0.92（CI 0.33–1.51）；术后 inflammatory +0.82（q=0.007）与 repair +0.61 同时上升；NAMPT_z 与 macro/mono r=+0.75、inflammatory r=+0.91；GSE272133 T2D 术后 repair +0.30。
- R4 细胞模型：GSE282850（LHCN-M2，n=4 配对）；NAMPT_z 汇总 +1.42（CI 0.98–1.86，100%，p=3.2e-10）；inflammatory_score +0.55（CI 0.23–0.87，100%，p=7.6e-4）。
- R5 Evo2：12,961 原始 → 432 候选（8 基因 TSS±2 kb 窗口，NAMPT 全保留 12 条；430 SNP + 2 indel）；Score A 全量 432（|delta| 中位 1.12，≥4 有 94 条）；Score B 短名单 104（Score A↔B 符号一致 87%，strand 一致 65%，fwd/rc r≈0.13）；Score C 实证退化（10×5 seeds sd=0）；Tier A=0、B=0、C=97、External-only=9、Excluded=326。
- 论断边界：NAMPT mRNA ≠ eNAMPT 蛋白；eNAMPT 方向性为可检验预测；Evo2 不证明因果；小样本（n≤4）仅方向性。

### Frontmatter（manuscript_frontmatter_v1_zh.md）
- Introduction 4 段漏斗：肥胖低度炎症×运动应激利害 → NAMPT 双重身份张力 → 现有研究缺口 → 本研究路线（59 基因框架、跨 9 数据集检验、Evo2-40B 432 候选分层）。
- Abstract（Nature 式）：问题 → 设计（9 矩阵 337 样本）→ 发现（α 0.79–0.91；meta +0.85/−0.62；细胞层 inflammatory +0.55）→ 边界（转录组证据、Tier A/B=0）。
- Title 首选：State-dependent NAMPT-NAD inflammatory-repair axis in obesity and exercise adaptation: transcriptomic and Evo2 sequence-model evidence。备选 3 个。

## 4. 可见证据基础（来源锚点，审稿可核对）

- `data_audit/outputs/meta/meta_results.csv`：R2/R4 meta 数字
- `data_audit/outputs/axis_structure/module_alpha.csv`：模块 α
- `data_audit/outputs/cell_composition/sensitivity_report.md`：轴内免疫负荷 r
- `data_audit/outputs/evo2/tiers.csv`、`scores.csv`、`scores_B.csv`：Evo2 数字
- `data_audit/outputs/manuscript_logic_v1_zh.md`：论断边界与定位
- `data_audit/outputs/motrpac_coverage_check.md`：eNAMPT 证据缺口结论

## 5. 共同审稿标准（五轴）

originality、scientific importance、interdisciplinary readership、technical soundness、readability for nonspecialists。技术问题按 12 轴清单内部覆盖（统计、因果、混杂、样本量、多重比较、方法归属等），但以五轴为输出主干。所有实质关切须给 Concern ID、claim_pointer（指向上述 R1-R5 或 frontmatter 段落）、evidence_pointer（指向 §4 来源或标注"缺失"）。禁止臆造审稿人身份、实验结果、引用或行号。

## 6. 隔离要求

三份审稿报告必须互相盲审：不得互相引用、预判、回应或共享关切清单。若环境无法保证隔离，须显式声明局限性。
