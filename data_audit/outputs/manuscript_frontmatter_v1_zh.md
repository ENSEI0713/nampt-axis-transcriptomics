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
NAMPT（nicotinamide phosphoribosyltransferase）正处在这个张力的中心。细胞内的 NAMPT（iNAMPT）通过 NAD salvage 支持 SIRT、AMPK、PGC1A、线粒体与 DNA 修复；细胞外的 eNAMPT/visfatin/PBEF 又常被放进肥胖、单核/巨噬激活、NF-κB 与 IL-6/TNF 的低度炎症框架。文献中长期存在矛盾：同一条 NAMPT 信号，一边被当作修复与适应性标志，一边被当作炎症负荷标志。关键缺口不是"NAMPT 好坏"，而是它究竟标记哪一种状态——取决于上下文。

**Para 3 — 已有什么、缺口是什么。**
现有的单一标志物或单队列研究通常把 NAMPT（或 eNAMPT）当单一方向信号，无法处理 iNAMPT/eNAMPT、NAD 代谢与免疫炎症之间的状态依赖；表达研究又多局限于单组织单时点，缺少跨组织、跨干预、跨时间尺度的证据梯。结果是对运动/代谢状态下 NAMPT 究竟标记什么，缺乏一个可复现、可检验的框架，也缺少把表达状态、调控变异（eQTL/GWAS/MPRA）与大规模 DNA 序列模型放入同一逻辑链的尝试。

**Para 4 — 本研究切入点与路线预览（不列数字）。**
我们提出**状态依赖的 NAMPT-NAD 炎症-修复轴**这一可检验模型，并用公共人类转录组证据与大规模 DNA 序列模型 Evo2-40B 加以检验。具体地，我们 (1) 构建 59 个 NAMPT 轴基因的双程序评分框架，并用模块共表达对其做结构验证；(2) 跨 9 个公共数据集、4 个运动队列、肥胖/减重队列与细胞模型，检验 NAMPT 轴在不同状态下是偏向炎症还是修复；(3) 用 Evo2-40B 的 allele surprisal（Score A）与 pseudo-likelihood（Score B）打分，把 432 个 NAMPT 轴候选调控变异与公共 eQTL/GWAS 证据分层（Tier A/B/C），给出可供后续实验验证的候选。核心主张是：NAMPT 不简单地是"好"或"坏"，而是状态依赖的轴——这解释了文献矛盾，并为肥胖人群的运动相关状态判断提供了可检验的起点。边界：全部为转录组证据；eNAMPT 方向性仅是可检验预测；Evo2 只做候选优先级，不证明因果。

---

## 二、Abstract（摘要，中文；按"最短证据链"浓缩）

> Nature 风格模式：精确问题/缺口 → 答之设计 → 主要发现 → 关键支持与边界 → 受限含义。

肥胖人群的运动应激叠加在低度炎症、胰岛素抵抗与线粒体功能下降之上，而 NAMPT（iNAMPT/eNAMPT）长期在"修复/NAD 代谢"与"炎症/免疫负荷"两种解释之间摇摆。我们提出状态依赖的 NAMPT-NAD 炎症-修复轴模型，将转录组的修复程序与炎症程序分离，并用 9 个公共人类矩阵、337 个样本及细胞模型加以检验。结果：(i) 轴的双程序结构在跨数据集共表达中成立（大队列修复模块 Cronbach α = 0.79–0.91）；(ii) 急性运动后 NAMPT_z 普遍上调（随机效应 meta 汇总 +0.85，95%CI 0.53–1.17，92% 方向一致，p≈1.8e-7；按数据集为独立单元重估后仍稳健，k=4，+0.965，p≈2.8e-4），但 repair_score 未随之显著上升（−0.33，p=0.05），balance_score 在聚类感知下失去显著性（k=4，−0.47，p=0.24）——NAMPT 上升并非自动等于修复，平衡方向为弱证据；(iii) 同一 NAMPT 上调在脂毒性刺激下耦合更强的炎症程序（细胞模型 meta：inflammatory_score +0.55，p≈7.6e-4），在运动模拟下则对应 NAD/修复背景；Evo2-40B 对 432 个轴候选变异打分并与公共 eQTL/GWAS 分层，但因高扰动短名单以稀有变异为主，Tier A/B 为空，该模块降为补充并留下可验证候选。结论：NAMPT-NAD 系统的状态不能用单一方向指标刻画，需在时间、训练状态与代谢背景下解释；公共数据支持该模型，但证据范围限于转录组，未做 eNAMPT 蛋白/NAD 代谢物与因果验证。

---

## 三、Title（含备选）

**首选（陈述式、可检索、可辩护）。**
> State-dependent NAMPT-NAD inflammatory–repair axis in obesity and exercise adaptation: transcriptomic and Evo2 sequence-model evidence

中文工作题：基于公共转录组与 Evo2-40B 序列模型的状态依赖性 NAMPT-NAD 炎症-修复轴

**备选 2（发现式）。**
> Acute exercise raises NAMPT yet flips the axis balance toward inflammation: a state-dependent NAMPT-NAD axis across obesity and training

**备选 3（机制式）。**
> An inflammatory–repair switch in NAMPT-NAD signaling across obesity, training and metabolic stress

**备选 4（保守式）。**
> State-dependent NAMPT-NAD signaling in obesity and exercise: transcriptomic and variant-level evidence from public data

> 规则核查：首选为"系统/对象 + 能力 + 应用"陈述式，无"Toward/A study of"样式；备选 2 的 "raises NAMPT" 有 meta +0.85 支撑、"flips balance toward inflammation" 有 balance −0.62 支撑，可辩护；无夸张词。

---

## 备注 / 待补输入（Assumptions & missing inputs）

- **语言**：本稿为中文工作稿，最终应转英文（zh-to-en）。转英时按数字落盘表逐项核验，不得改动数字与边界。
- **期刊**：未定。logic v1 §10：冲 Nature 主刊需补 MoTrPAC/蛋白代谢物/MPRA/前瞻队列；当前按 Nature-family/generic 措辞强度撰写。投稿前按目标期刊核对字数与格式。
- **数字来源**：337（9 矩阵总样本）、α 0.79–0.91、meta +0.85/−0.62、细胞层 inflammatory +0.55 均来自落盘（`meta_results.csv`、`module_alpha.csv`、`tiers.csv`），已核验一致。
- **eNAMPT** 仅为待验证假说；Abstract 与正文均不写蛋白/代谢物证据。
- 无编造内容；所有存疑点以上述备注显式列出。