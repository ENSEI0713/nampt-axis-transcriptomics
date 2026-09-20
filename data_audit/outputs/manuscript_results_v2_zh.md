# Results (draft v2)：NAMPT-NAD 炎症-修复轴

> 本稿基于 2026-09-18 完成的真实分析落盘：随机效应 meta（`outputs/meta/`）、
> 模块一致性（`outputs/axis_structure/`）、轴内免疫负荷（`outputs/cell_composition/`）、
> Evo2 候选与窗口（`outputs/evo2/`）。所有数字可追溯，论断遵守边界。

---

## Result 1：状态依赖的 NAMPT-NAD 炎症-修复轴：评分框架与结构验证

**问题。** NAMPT 具有双重身份：胞内 iNAMPT 支持 NAD salvage、SIRT/AMPK/PGC1A、线粒体与 DNA 修复；胞外 eNAMPT/visfatin 常被置于 NF-κB、单核细胞活化和低度炎症框架。这要求一个能把免疫炎症侧与代谢修复侧分开的可检验模型。

**做法。** 构建 59 个 NAMPT 轴基因（repair 34 / inflammatory 19 / both 6），覆盖 NAD salvage、NAD 消耗、NF-κB 炎症、单核/巨噬、线粒体、自噬、DNA 修复等 20 个模块。每个表达矩阵内部按基因 z-score，计算 `NAMPT_z`、`inflammatory_score`、`repair_score`、`balance_score`（= repair − inflammatory）。9 个公共矩阵、337 个样本，多数数据集轴基因覆盖率 100%。

**结构验证（新）。** 对每个数据集计算模块内 Cronbach α（内部一致性指标，不作为组间差异的显著性检验）与模块间相关：
- 大队列支持双程序框架：GSE272133 骨骼肌（n=51）中 nad_salvage_core α=0.79、sirtuin_repair α=0.82、ampk_mitochondria_repair α=0.83、oxidative_stress_repair α=0.91、dna_damage_repair α=0.86；GSE305038（n=24）模块 α 均值 0.78；GSE32575 单核细胞（n=47）α 均值 0.60。
- 小样本队列 α 不稳定（GSE312393、GSE282850 出现负 α），故模块一致性证据优先引自大队列；小样本的模块 α 不可靠。

**主张。** 59 基因轴 + 双程序评分能把 NAMPT 免疫炎症侧与代谢修复侧分开；模块 α 为"两个程序"提供了独立于先验基因清单的共表达统计支持。该框架仅在转录组层面成立。

---

## Result 2：运动诱导的 NAMPT 轴：急性应激与训练适应的分离

**做法。** 整合 4 个运动队列（GSE312393、GSE305038、GSE292369、GSE318937），12 个配对对照，随机效应 meta（DerSimonian-Laird）。

**meta 结果（新）。**
| 指标 | 汇总效应 | 95% CI | 方向一致 | p | I² |
| --- | --- | --- | --- | --- | --- |
| NAMPT_z | **+0.85** | 0.53–1.17 | 92% (11/12) | 1.8e-7 | 64% |
| balance_score | **−0.62** | −1.12–−0.12 | 83% (10 neg) | 0.016 | 98% |
| inflammatory_score | +0.28 | −0.03–+0.58 | 75% | 0.07 | 89% |
| repair_score | −0.33 | −0.67–+0.00 | 83% | 0.05 (ns) | 96% |

急性运动后 NAMPT_z 普遍上调。NAMPT 上升**并非自动等于修复**：repair_score 未显著上升（−0.33，p=0.05，CI 含 0）。但"轴平衡系统性转负"需谨慎：12 个对照嵌套在 4 个数据集（GSE318937 单独贡献 8 个），按数据集为有效独立单元重估后 balance_score 汇总 −0.47（95%CI −1.25–+0.32，p=0.24）失去显著性（见 `outputs/meta/meta_sensitivity_report.md`）。NAMPT_z 上调在数据集级（k=4，+0.965，95%CI 0.45–1.49，p=2.8e-4）与 leave-one-dataset-out（全部 4 次为正）下均稳健。高 I²（64–98%）提示效应方向一致但幅度随背景变化；balance 方向性为弱证据，状态依赖性解读需 moderator 检验而非仅凭 I²。

**轴内免疫负荷（新）。** 在 GSE318937（n=118）与 GSE305038 中，数据集内全样本的 inflammatory_score 与轴内单核/巨噬基因负荷代理高度相关（r=0.77–0.89，落在 0.7–0.9 范围）。该代理是与 NAMPT 轴重叠的 marker-gene burden，不是细胞类型去卷积；因此相关结果反映轴内基因共变，不能作为独立细胞比例或因果证据。该结果与 Phase 1b 中急性炎症样信号主要由 NF-κB/细胞因子模块驱动的观察一致。该急性信号在 24 h 后回落（GSE318937 即时 vs 24h balance 差异）。相关计算基于数据集内全样本，未按运动后时间点子集拆分。

---

## Result 3：肥胖与减重：NAMPT 轴的组织与疾病背景依赖性

**做法。** 整合单核细胞（GSE32575）、骨骼肌（GSE272133）、内脏脂肪（GSE294150）。

**发现。**
- 肥胖层包含 3 个预设对照比较（k=3）：NAMPT_z 汇总 +0.14（I²=0%）；inflammatory_score 汇总 +0.57，方向一致率为 67%，异质性较高。由于比较数少且组织/疾病背景不同，本层结果仅作方向性证据。
- GSE32575 单核细胞：肥胖 vs 瘦 NAMPT_z +0.92（CI 0.33–1.51）；术后 inflammatory_score +0.82（当前记录的 q=0.007）与 repair_score +0.61 **同时**上升；具体多重比较校正方法与比较家族需在统计方法中明确；减重不能简单解释为"炎症必然下降"，需结合时间点、药物与免疫细胞重塑。
- 轴内免疫负荷：GSE32575 中 NAMPT_z 与 macro/mono 负荷代理 r=+0.75，inflammatory_score 与该代理 r=+0.91。该代理不是细胞去卷积，结果仅表示轴内免疫基因负荷与评分共变，不能区分细胞组成混杂与因果。
- 代谢病背景：GSE272133 中 T2D 术后 repair_score +0.30（非 T2D 无此效应），提示代谢病状态改变减重后骨骼肌适应方向。

---

## Result 4：细胞模型：同样 NAMPT 上升可对应不同代谢刺激

**做法。** GSE282850 LHCN-M2 人肌细胞：分化 vs AICAR（运动模拟）vs palmitate（脂毒性）。

**发现。** AICAR 与 palmitate 均升高 NAMPT_z（meta 汇总 +1.42，方向一致 100%），且 palmitate 对应的 inflammatory_score 更高（meta 汇总 +0.55，方向一致 100%）、balance_score 更偏炎症侧。支持"同为 NAMPT 上升、代谢意义不同"的核心论点。注意：两个对照来自同一细胞系（GSE282850，n=3–4 配对），合并精度不具推断意义，此处仅作方向性证据。

---

## Result 5：Evo2-40B 调控变异优先级（打分与证据分层已完成）

**管线。** 从 Ensembl REST 构建 NAMPT 核心基因（NAMPT/CD38/BST1/SIRT1/SIRT3/SIRT6/IL6/TNF）TSS ±2 kb 启动子窗口内带 REF/ALT 的候选：12,961 条原始 → **432 条优先级功能候选**（missense / splice / 5'UTR / TF_binding / regulatory_region / ClinVar 注释），NAMPT 全保留 12 条。GRCh38 ref/alt 2 kb 窗口已构建并经完整性校验（430 条单碱基 SNP + 2 条 indel，0 条 ref 不匹配）。

**Score A（allele surprisal，全量完成）。** 432/432 候选打分（flank 200 bp，Evo2-40B generate logits）。|delta| 中位 1.12；|delta|≥4 有 94 条。高扰动集中在 IL6 / SIRT1 / TNF 窗口（观察，非因果）。

**Score B（pseudo-likelihood，短名单完成）。** 对 104 条短名单（|delta|≥4 的 94 条 + NAMPT 全窗口 12 条）做下游 8 bp 双链传播。Score A↔B 符号一致 87%；strand 一致 65%，fwd/rc 相关性低（r≈0.13），是稳定性局限。

**Score C（多 seed 稳定性）实证退化。** 10×5 seeds 全 sd=0：该 hosted 端点 logits 不随 seed 变化，多 seed 稳定性无信息。以 strand 一致性替代稳定性证据。

**eQTL/GWAS 合并（全量完成）。** GTEx REST（4 相关组织）+ GWAS Catalog 逐条查询 432 候选 → `tiers.csv`。Tier 分布：**A=0、B=0、C=97、External-only=9、Excluded=326**。Tier A/B 为零：Evo2 高扰动短名单几乎全是稀有变异，GTEx 仅覆盖常见变异、GWAS Catalog 对其 rsid 覆盖稀疏，导致 Evo2 扰动与外部可复现支持几乎不重叠；9 个 External-only 是强证据常见位点（TNF rs1800629、IL6 rs1800795 等）但 Evo2 分数温和。

**门槛判定（定案）。** Evo2 模块未满足协议 §11"稳定扰动 + 公共 QTL/GWAS 支持"的重叠要求，**不作为主图**，降为补充/探索性模块（详见 `outputs/evo2/evo2_variant_results_report.md`）。Evo2 仍提出一组可检验调控候选（C 类 97 条），供后续 MPRA/CRISPRi 验证。

---

## 论断边界

- NAMPT mRNA ≠ eNAMPT 蛋白；本稿为转录组证据。
- eNAMPT 方向性已降级为可检验预测（见论断边界章节）。
- Evo2 只做候选优先级，不证明因果，不预测临床风险。
- 小样本对照（n≤4）只作方向性证据。