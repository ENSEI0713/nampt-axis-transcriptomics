# 前言、摘要与题目（frontmatter v1，中文草稿）

> 本稿基于 2026-09-18 落盘核验后的 Results（`manuscript_results_v2_zh.md`）与论断边界
> （`manuscript_logic_v1_zh.md` §9）。所有数字可追溯。写作遵循 nature-writing skill：
> 论断与环境校准动词强度、边界如实、不编造。
>
> 状态：Introduction 全文；Abstract 已按"最后写"原则浓缩；Title 含备选。研究者确认后转英文。

---

## 一、Introduction（漏斗式，中文）

**Para 1 — 领域利害（肥胖低度炎症 × 运动应激的交叉）。**
肥胖人群常处于低度慢性炎症、胰岛素抵抗和线粒体功能下降的共存状态；科学运动的挑战因此不是"要不要动"，而是要判断运动引发的是可恢复的适应性应激，还是叠加在既有炎症背景上的额外负荷。两者在样本、时间点和组织层面难以凭单一标志物区分——这正是代谢-运动研究长期面对的基本张力。

**Para 2 — 收窄到 NAMPT 的已知张力。**
NAMPT 相关生物学连接了 NAD salvage、细胞修复以及免疫和代谢压力等不同过程。已有研究分别从细胞内 NAMPT、细胞外 NAMPT/visfatin/PBEF 及相关炎症通路讨论这些联系，但这些对象并不等同。本研究聚焦可由公共转录组数据评估的 **NAMPT 轴基因表达程序**，并检验其在不同组织、时间点和代谢背景下更接近炎症样还是修复样转录状态。细胞外 NAMPT 蛋白和 NAD 代谢物的方向仍属于待验证预测，而不是本研究直接测得的结果。

**Para 3 — 已有什么、缺口是什么。**
现有研究常将 NAMPT 相关表达或蛋白信号解释为单一方向指标，但细胞内与细胞外 NAMPT、NAD 代谢物以及免疫炎症状态并不是同一层面的测量对象。公共表达研究又多局限于单组织、单时点或单一干预，缺少跨组织、跨干预和跨时间尺度的转录组证据梯。因此，本研究首先建立并检验一个 **NAMPT 轴转录程序** 的状态依赖框架；其与 eNAMPT 蛋白及 NAD 代谢物的对应关系仍需后续实验验证。

**Para 4 — 本研究切入点与路线预览（不列数字）。**
我们提出一个**状态依赖的 NAMPT 轴转录程序模型**，并用公共人类转录组证据与 Evo2-40B 序列模型进行检验。具体地，我们 (1) 构建 59 个 NAMPT 轴基因的双程序评分框架，并用模块共表达对其进行结构描述；(2) 跨 9 个公共数据集、4 个运动队列、肥胖/减重队列与细胞模型，比较 NAMPT 轴转录程序在不同状态下的炎症样与修复样方向；(3) 用 Evo2-40B 对 432 个候选调控变异进行序列层面的优先级评分，并与公共 eQTL/GWAS 证据分层。该框架为 NAMPT 相关状态依赖性提供转录组层面的可检验起点，但不等同于对 eNAMPT 蛋白或 NAD 代谢物变化的测量，也不单独解释这些层面的机制。

---

## 二、Abstract（摘要，中文；按"最短证据链"浓缩）

> Nature 风格模式：精确问题/缺口 → 答之设计 → 主要发现 → 关键支持与边界 → 受限含义。

肥胖人群的运动应激叠加在低度炎症、胰岛素抵抗与线粒体功能下降之上，而 NAMPT 轴转录程序在修复相关 NAD salvage 程序与炎症/免疫程序之间的状态依赖性仍不清楚。我们提出一个状态依赖的 **NAMPT 轴转录程序模型**，将转录组中的修复样程序与炎症样程序分开评估，并用 9 个公共人类矩阵、337 个样本及细胞模型加以检验。结果：(i) 轴的双程序结构在跨数据集共表达中成立（大队列修复模块 Cronbach α = 0.79–0.91）；(ii) 急性运动后 NAMPT_z 普遍上调（随机效应 meta 汇总 +0.85，95%CI 0.53–1.17，92% 方向一致，p≈1.8e-7；按数据集为独立单元重估后仍稳健，k=4，+0.965，p≈2.8e-4），但 repair_score 未随之显著上升（−0.33，p=0.05），balance_score 在聚类感知下失去显著性（k=4，−0.47，p=0.24）——NAMPT 上升并非自动等于修复，平衡方向为弱证据；(iii) 同一 NAMPT 上调在脂毒性刺激下耦合更强的炎症程序（细胞模型 meta：inflammatory_score +0.55，p≈7.6e-4），在 AICAR 运动模拟条件下则表现为不同于 palmitate 的转录背景；该结果不构成 NAD 代谢物变化的证据；Evo2-40B 对 432 个轴候选变异打分并与公共 eQTL/GWAS 分层，但因高扰动短名单以稀有变异为主，Tier A/B 为空，该模块降为补充并留下可验证候选。结论：NAMPT-NAD 系统的状态不能用单一方向指标刻画，需在时间、训练状态与代谢背景下解释；公共数据支持该模型，但证据范围限于转录组，未做 eNAMPT 蛋白/NAD 代谢物与因果验证。

---

## 三、Title（含备选）

**首选（陈述式、可检索、可辩护）。**
> State-dependent NAMPT-axis transcriptional programs in obesity and exercise adaptation: public transcriptomic and Evo2 sequence-model evidence

中文工作题：肥胖与运动适应中的状态依赖性 NAMPT 轴转录程序：公共转录组与 Evo2 序列模型证据

**备选 2（发现式）。**
> Acute exercise raises NAMPT without establishing a stable inflammatory-repair balance: transcriptomic evidence across obesity and training

**备选 3（机制式）。**
> State-dependent NAMPT-axis transcriptional programs across obesity, training and metabolic stress

**备选 4（保守式）。**
> State-dependent NAMPT-axis transcriptional programs in obesity and exercise: transcriptomic and variant-level evidence

> 规则核查：首选为"系统/对象 + 能力 + 应用"陈述式，无"Toward/A study of"样式；备选 2 的 "raises NAMPT" 有聚类感知 meta 支撑，但不再声称 balance 稳定转向炎症；无夸张词。

---

## 备注 / 待补输入（Assumptions & missing inputs）

- **语言**：本稿为中文工作稿，最终应转英文（zh-to-en）。转英时按数字落盘表逐项核验，不得改动数字与边界。
- **期刊**：未定。logic v1 §10：冲 Nature 主刊需补 MoTrPAC/蛋白代谢物/MPRA/前瞻队列；当前按 Nature-family/generic 措辞强度撰写。投稿前按目标期刊核对字数与格式。
- **数字来源**：337（9 矩阵总样本）、α 0.79–0.91、meta +0.85/−0.62、细胞层 inflammatory +0.55 均来自落盘（`meta_results.csv`、`module_alpha.csv`、`tiers.csv`），已核验一致。
- **eNAMPT** 仅为待验证假说；Abstract 与正文均不写蛋白/代谢物证据。
- 无编造内容；所有存疑点以上述备注显式列出。