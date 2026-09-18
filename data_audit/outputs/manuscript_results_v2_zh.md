# Results (draft v2) — NAMPT-NAD 炎症-修复轴

> 本稿基于 2026-09-18 完成的真实分析落盘：随机效应 meta（`outputs/meta/`）、
> 模块一致性（`outputs/axis_structure/`）、轴内免疫负荷（`outputs/cell_composition/`）、
> Evo2 候选与窗口（`outputs/evo2/`）。所有数字可追溯，论断遵守边界。

---

## Result 1 — 状态依赖的 NAMPT-NAD 炎症-修复轴：评分框架与结构验证

**问题。** NAMPT 具有双重身份：胞内 iNAMPT 支持 NAD salvage、SIRT/AMPK/PGC1A、线粒体与 DNA 修复；胞外 eNAMPT/visfatin 常被置于 NF-κB、单核细胞活化和低度炎症框架。这要求一个能把免疫炎症侧与代谢修复侧分开的可检验模型。

**做法。** 构建 59 个 NAMPT 轴基因（repair 34 / inflammatory 19 / both 6），覆盖 NAD salvage、NAD 消耗、NF-κB 炎症、单核/巨噬、线粒体、自噬、DNA 修复等 20 个模块。每个表达矩阵内部按基因 z-score，计算 `NAMPT_z`、`inflammatory_score`、`repair_score`、`balance_score`（= repair − inflammatory）。9 个公共矩阵、346 个样本，多数数据集轴基因覆盖率 100%。

**结构验证（新）。** 对每个数据集计算模块内 Cronbach α 与模块间相关：
- 大队列支持双程序框架：GSE272133 骨骼肌（n=51）中 nad_salvage_core α=0.79、sirtuin_repair α=0.82、ampk_mitochondria_repair α=0.83、oxidative_stress_repair α=0.91、dna_damage_repair α=0.86；GSE305038（n=25）模块 α 均值 0.78；GSE32575 单核细胞（n=48）α 均值 0.61。
- 小样本队列 α 不稳定（GSE312393、GSE282850 出现负 α），模块一致性证据优先引自大队列，并如实披露局限。

**主张。** 59 基因轴 + 双程序评分能把 NAMPT 免疫炎症侧与代谢修复侧分开；模块 α 为"两个程序"提供了独立于先验基因清单的共表达统计支持。该框架仅在转录组层面成立。

---

## Result 2 — 运动诱导的 NAMPT 轴：急性应激与训练适应的分离

**做法。** 整合 4 个运动队列（GSE312393、GSE305038、GSE292369、GSE318937），12 个配对对照，随机效应 meta（DerSimonian-Laird）。

**meta 结果（新）。**
| 指标 | 汇总效应 | 95% CI | 方向一致 | p | I² |
| --- | --- | --- | --- | --- | --- |
| NAMPT_z | **+0.85** | 0.53–1.17 | 92% (11/12) | 1.8e-7 | 64% |
| balance_score | **−0.62** | −1.12–−0.12 | 83% (10 neg) | 0.016 | 98% |
| inflammatory_score | +0.28 | −0.03–+0.58 | 75% | 0.07 | 89% |
| repair_score | −0.33 | — | 83% | ns | 96% |

急性运动后 NAMPT_z 普遍上调但 balance 系统性转负——NAMPT 上升**并非自动等于修复**。虽说法在时间/训练状态/营养背景上显著分层（高 I²），它正是状态依赖性的统计特征。

**轴内免疫负荷（新）。** 在 GSE318937（n=118）与 GSE305038 中，运动后 inflammatory_score 与轴内单核/巨噬基因负荷高度相关（r=0.7–0.9 范围），独立印证 Phase 1b 敏感性中"急性炎症样信号主要由 NF-κB/细胞因子模块驱动"的结论。该急性信号在 24 h 后回落（GSE318937 即时 vs 24h balance 差异）。

---

## Result 3 — 肥胖与减重：NAMPT 轴的组织与疾病背景依赖性

**做法。** 整合单核细胞（GSE32575）、骨骼肌（GSE272133）、内脏脂肪（GSE294150）。

**发现。**
- meta 肥胖层（k=3）：NAMPT_z 汇总 +0.14（I²=0%）、inflammatory_score 汇总 +0.57（方向一致 67%，高异质性）——仅作方向性。
- GSE32575 单核细胞：肥胖 vs 瘦 NAMPT_z +0.92（CI 0.33–1.51）；术后 inflammatory_score +0.82（q=0.007）与 repair_score +0.61 **同时**上升——减重不能简单解释为"炎症必然下降"，需结合时间点、药物与免疫细胞重塑。
- 轴内免疫负荷：GSE32575 中 NAMPT_z 与 macro/mono 负荷 r=+0.75，inflammatory_score r=+0.91——肥胖免疫细胞中 NAMPT 炎症轴与免疫基因强共变（因果不可分）。
- 代谢病背景：GSE272133 中 T2D 术后 repair_score +0.30（非 T2D 无此效应），提示代谢病状态改变减重后骨骼肌适应方向。

---

## Result 4 — 细胞模型：同样 NAMPT 上升可对应不同代谢刺激

**做法。** GSE282850 LHCN-M2 人肌细胞：分化 vs AICAR（运动模拟）vs palmitate（脂毒性）。

**发现。** AICAR 与 palmitate 均升高 NAMPT_z（meta 细胞模型 NAMPT_z 汇总 +1.42，方向一致 100%），但 palmitate 对应的 inflammatory_score 更高、balance_score 更偏炎症侧。支持"同为 NAMPT 上升、代谢意义不同"的核心论点。样本数小（n=4 配对），方向性证据。

---

## Result 5 — Evo2-40B 调控变异优先级（管线就绪，分数待密钥）

**管线（本稿已完成）。** 从 Ensembl REST 构建 NAMPT 核心基因（NAMPT/CD38/BST1/SIRT1/SIRT3/SIRT6/IL6/TNF）TSS ±2 kb 启动子窗口内带 REF/ALT 的候选：12,961 条原始 → **432 条优先级功能候选**（missense / splice / 5'UTR / TF_binding / regulatory_region / ClinVar 注释），NAMPT 全保留 12 条。GRCh38 ref/alt 2 kb 窗口已构建并经完整性校验（430 条单碱基 SNP + 2 条 indel，0 条 ref 不匹配）。

**打分状态。** `run_evo2_scoring.py` 已就绪（allele surprisal，密钥门控、断点续跑、日志脱敏），实际打分待 `NVIDIA_API_KEY` 配置后运行。

**门槛判定。** Evo2 是否进入主图，取决于 (a) 分数稳定、(b) eQTL/GWAS 支撑合并。两者均可执行，当前未决（见 `outputs/evo2/evo2_variant_results_report.md`）。

---

## 论断边界

- NAMPT mRNA ≠ eNAMPT 蛋白；本稿为转录组证据。
- eNAMPT 方向性已降级为可检验预测（见论断边界章节）。
- Evo2 只做候选优先级，不证明因果，不预测临床风险。
- 小样本对照（n≤4）只作方向性证据。