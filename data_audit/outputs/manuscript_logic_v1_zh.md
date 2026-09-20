# NAMPT-NAD inflammatory-repair axis manuscript logic v1

## 1. 论文主轴

### 工作题目

Public multi-omic and sequence-model dissection of a state-dependent NAMPT-NAD inflammatory-repair axis in obesity and exercise adaptation

中文工作题目：基于公共多组学与 Evo2-40B 序列模型解析肥胖和运动适应中的状态依赖性 NAMPT-NAD 炎症-修复轴

### 一句话论点

在肥胖和运动适应中，NAMPT-NAD 系统不是简单的“有益”或“有害”信号，而是一个状态依赖性轴：慢性代谢压力下它更接近免疫/脂肪炎症负荷，运动和训练背景下它可转向 NAD 代谢、线粒体功能、细胞修复和适应性重塑；公共人类组学数据可用于建立这一轴的表达证据，而 Evo2-40B 可进一步把候选调控变异与这种状态转换联系起来。

### 论文应聚焦单一子方向还是三个方向

建议聚焦一个主方向：肥胖相关低度慢性炎症与运动适应中的 NAMPT-NAD 炎症-修复轴。

营养代谢和损伤/修复不要拆成三篇主线，而应作为同一主轴下的两个机制模块：营养代谢回答“能量和 NAD 前体/消耗状态如何影响这条轴”，损伤/修复回答“运动应激何时是适应性修复，何时可能变成炎症负担”。这样论文的问题更尖锐，也更符合高水平期刊对单一核心概念的要求。

## 2. 研究问题的来源

### 真实问题

肥胖人群常处于低度慢性炎症、胰岛素抵抗、线粒体功能下降和运动风险升高的交叉状态。对这类人群来说，科学运动的关键不是简单“多运动”，而是如何识别运动引发的是可恢复的适应性应激，还是叠加在已有炎症背景上的额外负荷。

NAMPT 正好处在这个问题的中心。一方面，细胞内 NAMPT 通过 NAD salvage 支持 SIRT、AMPK、PGC1A、线粒体功能、DNA 修复和自噬。另一方面，细胞外 NAMPT/visfatin/PBEF 又常被放在肥胖、单核细胞/巨噬细胞活化、NF-kB、IL-6、TNF 和低度炎症框架中讨论。现在的关键矛盾不是 NAMPT 到底好还是坏，而是：不同生理状态下，NAMPT 相关循环究竟是在标记炎症负荷，还是在标记修复能力。

### 当前解释缺口

现有研究通常有三类不足：

1. 把 NAMPT 或 eNAMPT 当成单一方向的标志物，忽略 iNAMPT、eNAMPT、NAD 代谢和免疫炎症之间的状态依赖性。
2. 单队列研究较多，缺少跨组织、跨干预、跨时间尺度的公共数据证据梯。
3. 很少把表达状态、调控变异、组织特异性 enhancer/eQTL/GWAS 证据和大规模 DNA 序列模型放在一个逻辑链中。

## 3. 三个创新点

### 创新点 1：提出状态依赖的 NAMPT 轴转录程序

本研究不再问 NAMPT 是好还是坏，而是把 NAMPT 相关生物学拆成两个可测量状态：

- 炎症 NAMPT 程序：NAMPT 与 CD38/BST1/PARP、NF-kB、IL6/TNF/IL1B/CCL2、NLRP3、单核细胞/巨噬细胞标志物共同变化，代表慢性代谢压力、先天免疫激活和潜在 eNAMPT 相关炎症负荷。
- 修复 NAMPT 程序：NAMPT 与 NAD salvage、SIRT1/3/6、AMPK、PGC1A、线粒体生物发生、抗氧化、自噬和 DNA 修复共同变化，代表运动适应、线粒体重塑和细胞修复能力。

核心创新不在于发现 NAMPT 参与 NAD 或炎症，而在于把二者纳入同一状态转换框架，并用公共人类数据进行可复现检验。

### 创新点 2：建立跨扰动的人类公共数据证据梯

研究不依赖单一队列，而是构建从健康运动、运动训练、短期活动减少、营养恢复、肥胖、减重/代谢手术、单核细胞、脂肪组织和肌细胞模型组成的证据梯。每个数据集只做内部对照，避免把不同平台的原始表达量直接混合。

第一轮已跑通 9 个表达矩阵、337 个样本，NAMPT 轴基因覆盖率多数为 100%。初步结果显示同一 NAMPT 轴在不同状态下方向并不相同：训练和活动背景下更偏修复/适应，急性运动后可出现短暂炎症样信号，肥胖/减重和代谢状态则呈现组织和疾病背景依赖性。这种“不简单一致”本身是论文的关键发现，因为它解释了 NAMPT/eNAMPT 文献中长期存在的矛盾。

### 创新点 3：用 Evo2-40B 把调控序列变异连接到表达状态

Evo2-40B 的合理位置不是替代生物实验，而是作为 DNA 序列层面的调控先验。研究将候选变异限定在 NAMPT/NAD/炎症/修复基因附近的组织特异性调控区域，再用 ref/alt 序列窗口比较 Evo2 扰动分数，并与 GTEx/eQTL、GWAS、ENCODE/Roadmap/FANTOM5、GSE247455 snATAC/MPRA 等公共证据整合。

这样 Evo2 解决的是“大问题中的一部分”：帮助从大量公共遗传和调控候选中优先筛出可能影响 NAMPT 轴状态转换的 enhancer/variant，为后续 MPRA、CRISPRi/a 或临床队列验证提供基础。

## 4. 公共数据库筛选方法

### 搜索来源

- GEO/GDS：运动、训练、骨骼肌、血液/PBMC、肥胖、脂肪组织、减重、代谢手术、肌肉损伤/恢复等关键词。
- SRA：可补充原始测序数据，尤其是缺少处理矩阵但元数据清晰的研究。
- PubMed：用于建立 NAMPT/NAD/运动/肥胖/炎症文献锚点。
- GTEx、eQTL Catalogue、eQTLGen：表达 QTL 与组织特异性调控证据。
- GWAS Catalog、OpenGWAS、FinnGen：BMI、肥胖、CRP、IL-6、T2D、胰岛素抵抗、体力活动、VO2max、肌力和恢复相关性状。
- ENCODE、Roadmap、FANTOM5、GTEx epigenomics、GSE247455：骨骼肌、脂肪、免疫细胞调控区域。
- PRIDE/ProteomeXchange、MetaboLights/Metabolomics Workbench：后续补充 eNAMPT 蛋白、NAD/NAM/NMN/NR、色氨酸-犬尿氨酸和脂代谢证据。

### 主分析纳入标准

- 人类样本或人类细胞模型。
- 有公开 accession、可下载矩阵或可重建表达/调控数据。
- 组织/细胞与问题相关：骨骼肌、脂肪组织、全血、PBMC、CD14+ 单核细胞、巨噬细胞或人骨骼肌细胞。
- 有明确对照：运动前后、训练前后、活动减少前后、营养恢复、肥胖/正常体重、减重/手术前后、代谢状态差异等。
- 样本元数据足以提取条件、时间点、组织、干预和基本人群信息。
- 基因层面或调控层面可与 NAMPT 轴整合。

### 排除或降级标准

- 动物数据只能作为机制补充，不能作为人类主证据。
- 癌症、严重感染、严重血管病等强混杂疾病队列不进入主证据梯。
- 无法解析样本条件、无可下载矩阵或缺少最基本元数据的数据集降为候选。
- 仅有 NAMPT mRNA 的数据不能直接支持 eNAMPT 蛋白结论。
- 不能把公共数据分析结果转化为个人诊断或运动处方。

## 5. 当前已完成的第一轮数据基础

### 已纳入打分的数据模块

- GSE312393：人骨骼肌急性运动 24 h 与 6 周训练。
- GSE305038：正常活动/短期低活动背景下运动前后骨骼肌转录组。
- GSE292369：运动与酮体恢复相关骨骼肌转录组。
- GSE318937：中等连续运动/冲刺间歇运动与补充剂/安慰剂背景下骨骼肌转录组。
- GSE32575：瘦人、肥胖者代谢手术前后 CD14+ 单核细胞转录组。
- GSE272133：肥胖或肥胖合并 T2D 人群代谢手术前后骨骼肌转录组。
- GSE294150：重度肥胖人群内脏脂肪组织转录组。
- GSE282850：人骨骼肌细胞 AICAR 与 palmitate 模型。

### 第一轮预设对照的主要方向

> **新增（2026-09-18，后经聚类感知敏感性修正）**：随机效应 meta（DerSimonian-Laird）已完成，见 `outputs/meta/`。运动层 12 个对照的 NAMPT_z 汇总 +0.85（92% 方向一致，p=1.8e-7），数据集级聚类感知重估为 k=4、+0.965（p=2.8e-4）；balance_score 的对照级效应 −0.62（p=0.016），聚类感知后 −0.47（p=0.24），因此 balance 仅作弱方向性证据。肥胖层 3 个预设对照比较仅作方向性。轴结构分析（`outputs/axis_structure/`）与轴内免疫负荷代理（`outputs/cell_composition/`）见 Result 1-3 更新。


这些结果是方向性筛查，不是最终统计结论：

- GSE312393 6 周训练后，NAMPT_z 上升 1.107，repair_score 上升 0.430，balance_score 上升 0.269，提示训练适应可能更偏修复/代谢重塑。
- GSE305038 中，正常活动背景下运动后 repair_score 上升 0.575，高于 inflammatory_score 上升 0.265，balance_score 上升 0.310；低活动背景下运动后 inflammatory_score 反而下降 0.359，提示活动背景会改变运动反应。
- GSE318937 中，MICE/SIE 运动后即刻 NAMPT_z 普遍上升，同时 inflammatory_score 上升更明显；24 h 后 inflammatory_score 接近基线，说明急性运动信号可能是短暂炎症样应激，而不是慢性炎症。
- GSE292369 中，运动相对静息 NAMPT_z 上升 0.728，inflammatory_score 上升 0.258，但 repair_score 下降 0.092，提示恢复期营养/时间点对轴的方向很重要。
- GSE32575 中，肥胖者相对瘦人 NAMPT_z 上升 0.923，但炎症与修复综合分数变化较小；术后相对术前 inflammatory_score 和 repair_score 同时上升，提示单核细胞转录状态不能简单解释为“减重后炎症必然下降”，需要结合时间点、药物、免疫细胞重塑和 eNAMPT 蛋白证据。
- GSE272133 中，肥胖非 T2D 术后 NAMPT_z 和炎症/修复分数小幅下降，而 T2D 术后修复分数上升，提示代谢病背景会改变减重后的骨骼肌适应方向。
- GSE282850 中，AICAR 和 palmitate 均提高 NAMPT_z，但 palmitate 的 inflammatory_score 更高，支持“同样 NAMPT 上升可对应不同代谢状态”的观点。

## 6. 拟定结果结构

### Result 1：定义 NAMPT-NAD 炎症-修复轴

问题：如何把 iNAMPT/eNAMPT、NAD、NF-kB、线粒体和修复放入同一个可检验模型？

做法：构建 59 个 NAMPT 轴基因，分成 inflammatory、repair 和 both 三类。表达矩阵内部按基因 z-score，计算 NAMPT_z、inflammatory_score、repair_score 和 balance_score。**结构验证（新增）**：对每个数据集计算模块内 Cronbach alpha 与模块间相关矩阵，检验"炎症程序 / 修复程序"是否在公共数据中形成真实共表达单元而非人为基因清单。初步结构证据：大队列（GSE272133 n=51、GSE305038、GSE32575）中 nad_salvage_core、sirtuin_repair、ampk_mitochondria_repair、oxidative_stress_repair 等修复模块 alpha 达 0.7–0.9，支持双程序框架；小样本队列（GSE312393、GSE282850）alpha 不稳定（含负值），模块一致性证据应优先引自大队列并如实披露小样本局限。

预期主张：这个评分框架能把 NAMPT 的免疫炎症侧和代谢修复侧分开，使后续跨数据集比较变得可解释；结构一致性（alpha）为"两个程序"提供独立于先验基因清单的统计支持。

### Result 2：运动诱导 NAMPT 轴的急性应激与训练适应不同

问题：运动后 NAMPT 相关变化是炎症还是修复？

做法：整合 GSE312393、GSE305038、GSE292369 和 GSE318937。**随机效应 meta（新增）**：对 12 个运动类配对对照按指标汇总（DerSimonian-Laird）：NAMPT_z 汇总效应 +0.85（95%CI 0.53–1.17，方向一致 92%，p=1.8e-7）；balance_score 汇总 −0.62（95%CI −1.12–−0.12，方向一致 83%，p=0.016）；inflammatory_score 汇总 +0.28（ns）；repair_score 汇总 −0.33。高 I²（64–98%）表明效应幅度随背景变化，但不单独证明状态依赖性；现有字段支持数据集内时间点/训练状态描述，不支持统一跨研究 moderator 元回归。

预期主张：急性运动可出现 NAMPT 与炎症样转录信号的短暂上升；训练或合适活动背景下，repair_score 和 balance_score 可用于描述适应性重塑，但现有聚类感知分析不支持把 balance 转负写成稳健效应。NAMPT_z 上调在数据集级分析中保持稳健，运动反应仍需结合时间、训练状态和营养背景解释。**轴内免疫负荷（新增）**：部分运动数据集（GSE318937、GSE305038）的 inflammatory_score 与轴内单核/巨噬基因负担代理相关（r=0.7–0.9）。该代理不是细胞去卷积，相关结果反映轴内基因共变，不能作为独立细胞比例或因果证据。

### Result 3：肥胖和减重状态中的 NAMPT 轴具有组织与疾病背景依赖性

问题：肥胖人群的 NAMPT 变化是否可以标记低度慢性炎症？

做法：整合 GSE32575、GSE272133、GSE294150 及后续脂肪/血液数据。**随机效应 meta（新增）**：肥胖层包含 3 个预设对照比较（k=3）：NAMPT_z 汇总 +0.14（I²=0%），inflammatory_score 汇总 +0.57（方向一致 67%，异质性较高）；因比较数少且组织/疾病背景不同，仅作方向性证据。**轴内免疫负荷（新增）**：GSE32575 单核细胞中 NAMPT_z 与 macro/mono 负担代理 r=+0.75，inflammatory_score r=+0.91——肥胖免疫细胞中 NAMPT 炎症轴与轴内免疫基因表达强共变，支持"肥胖背景下 NAMPT 更接近免疫炎症负荷"的状态依赖解释，但无法区分因果与组成混杂。

预期主张：NAMPT_z 在肥胖免疫细胞中升高，但综合炎症/修复程序需要结合组织、时间点和代谢病背景解释。NAMPT mRNA 本身不足以定义 eNAMPT 或低度慢性炎症，需要蛋白和代谢物证据增强。

### Result 4：细胞模型揭示同样 NAMPT 上升可对应不同代谢刺激

问题：运动模拟和脂毒性刺激是否都能推高 NAMPT，但指向不同生物意义？

做法：使用 GSE282850 中 AICAR 与 palmitate 对比。

预期主张：AICAR 与 palmitate 都提高 NAMPT_z，但 palmitate 更偏炎症/代谢压力，支持 NAMPT 需要在上下文中解释。

### Result 5：Evo2-40B 优先筛选 NAMPT 轴调控变异

问题：为什么不同人对肥胖、运动、营养和损伤修复的 NAMPT 轴反应可能不同？

做法：在 NAMPT 轴基因附近筛选与 BMI、炎症、T2D、运动/体能相关的 GWAS/eQTL/调控变异，构建 GRCh38 ref/alt 序列窗口，用 Evo2-40B 计算序列扰动分数，并与组织调控证据合并。

预期主张：Evo2 不证明机制，但能提出一组更值得后续实验验证的调控候选，把表达状态和遗传调控连接起来。

## 7. 图件计划

### Figure 1：问题与总体框架

展示肥胖低度炎症、运动应激、NAD 修复、iNAMPT/eNAMPT 和 Evo2 调控变异之间的关系。核心信息是：本研究不是问 NAMPT 好坏，而是问状态转换。

### Figure 2：公共数据筛选漏斗与 NAMPT 轴评分体系

展示数据库搜索、纳入/排除标准、最终数据模块、59 基因轴、评分定义和覆盖率。当前可展示 9 个矩阵、337 个样本，多数数据集 NAMPT 轴覆盖率 100%。

### Figure 3：运动和训练中的 NAMPT 轴动态

展示急性运动、训练、低活动背景、酮体恢复和 MICE/SIE 的 NAMPT_z、inflammatory_score、repair_score、balance_score。重点突出急性应激与训练适应的分离。

### Figure 4：肥胖、减重和组织背景中的 NAMPT 轴

展示 CD14+ 单核细胞、骨骼肌和脂肪组织中的肥胖/术前术后变化。重点是异质性和组织依赖，而不是过度简化为“肥胖炎症高、减重炎症低”。

### Figure 5：Evo2-40B 调控变异优先级流程

展示从 GWAS/eQTL/ATAC/MPRA 候选变异到 ref/alt 序列窗口、Evo2 扰动分数、证据分层和候选 enhancer/variant 的流程。

### Figure 6：面向后续验证的转化模型

展示一个分层框架：表达轴用于群体层面状态识别，蛋白/代谢物用于 eNAMPT/NAD 生物标志物增强，Evo2 变异用于个体差异假设，最终需要前瞻性运动干预和实验验证。

## 8. 方法学主体

### Module 1：公共数据审计与筛选

使用预设查询式检索 GEO/GDS、SRA 和 PubMed，形成候选表；按人类相关性、组织相关性、干预相关性、组学类型、样本量、元数据可解析性和公开访问性打分；手动标注 first-priority、second-priority、supplement 或 exclude。

### Module 2：NAMPT 轴基因集与评分

基于 NAMPT/NAD salvage、NAD consumption、NF-kB/先天免疫、线粒体、自噬、DNA 修复、胰岛素和营养感知构建 v1 基因集。每个数据集内部转换表达矩阵、按基因 z-score，避免跨平台原始表达直接比较。

### Module 3：预设对照与统计分析

优先使用研究内部对照。配对设计使用 participant-level paired model 或 mixed model；非配对设计使用线性模型或稳健效应量；对每个预先定义的对照比较报告 delta、标准化 delta 和置信区间；同一比较家族内的多重检验需明确标注校正方法后的 q 值。Cronbach α 仅用于模块内部一致性描述，不作为差异显著性证据。跨数据集只做方向一致性和随机效应 meta-analysis，不把原始表达强行合并。

### Module 4：敏感性分析

包括去掉 NAMPT 后重算评分、去掉 IL6 等运动双重语义基因后重算、按 inflammatory/repair 模块分别 leave-one-module-out、调整细胞组成或使用 CIBERSORT/xCell 类方法估计免疫浸润、比较不同基因集构建策略。

### Module 5：Evo2-40B 调控变异分析

候选变异来自 GTEx/eQTL/GWAS/ENCODE/GSE247455 等公共资源。构建 ref/alt 序列窗口，计算 Evo2 allele surprisal 或 pseudo-likelihood perturbation，并要求候选同时有调控证据和组织/性状证据。Evo2-only 候选只作为探索，不进入核心机制主张。

### Module 6：数据与代码可复现性

所有公共数据保存 accession、下载日期、处理脚本和输出表。新生成的处理矩阵、评分表、图源数据和代码应存入 Zenodo/OSF/Figshare 或机构仓库，获得 DOI。第三方公共原始数据用 accession 引用，不随意重新分发。

## 9. 论断边界

### 可以说

- 公共人类数据支持 NAMPT 轴在肥胖、运动和代谢状态中具有状态依赖性。
- NAMPT mRNA 与 inflammatory/repair 程序的关系随组织、时间点、训练状态和代谢病背景变化。
- Evo2-40B 可作为调控变异优先级工具，为 NAMPT 轴个体差异提供可检验假设。

### 现在不能说

- 不能把 NAMPT mRNA 等同于 eNAMPT 蛋白。
- 不能仅凭公共表达数据判断个人是否处于低度慢性炎症。
- 不能说 Evo2 预测了运动方案或临床风险。
- 不能说减肥、手术或某种运动一定降低 NAMPT 相关炎症。
- 不能在没有实验验证时声称调控变异导致了 NAMPT 轴状态转换。

### eNAMPT/NAD 证据决策（2026-09-18 检索后确定）

依据 `outputs/enampt_retrieval.md` 的检索记录：MetaboLights 关键词过滤在当前 API 不可用、PRIDE 探测端点 404、可程序化获取的"运动/肥胖 × 血浆 eNAMPT/NAD 代谢物"配对数据未确认。**决策：eNAMPT/NAD 代谢物主张降级为待验证假说，不作为核心结论。** 论文将：

- 明确声明 NAMPT mRNA 状态变化是转录组证据，不构成 eNAMPT 蛋白或 NAD 丰度证据；
- 把 eNAMPT 方向性表述为轴模型的**可检验预测**（肥胖中跟随炎症程序、训练后跟随修复标志物），留给蛋白/代谢物验证；
- 在补充材料列出待挖掘的公共资源（MetaboLights 人工检索、PRIDE 修复端点后、Olink/aptamer 补充材料、MoTrPAC）。

## 10. Nature 级别定位

这篇论文真正有希望打动高水平期刊的地方，不是“用了 Evo2-40B”，而是提出并验证一个能解释 NAMPT 文献矛盾的状态依赖模型。Nature 看重的是问题重要、逻辑巧妙、证据链闭合和概念推进。

仅靠公共表达数据和 API，直接冲主刊 Nature 风险很高。要向 Nature 级别靠近，至少需要再补强以下一类决定性证据：

- MoTrPAC 或类似规模的人类运动多组学证据。
- 公共或合作获得的血浆/血清 eNAMPT、NAD 代谢物、CRP/IL-6/TNF 等蛋白/代谢物证据。
- GTEx/eQTL/GWAS/MPRA 与 Evo2 候选高度一致的调控变异证据。
- 对 1-3 个 Evo2 优先候选 enhancer/variant 的 MPRA、CRISPRi/a 或 reporter 实验验证。
- 前瞻性运动干预队列中，NAMPT 轴评分与肥胖、炎症、体能、恢复和安全性指标的关联。

如果暂时完全不做新实验，合理目标更可能是 Nature-family 子刊、计算生物学、代谢/运动医学或转化医学方向的高水平期刊；若 Evo2 调控变异模块和 eNAMPT/NAD 蛋白代谢证据补强，影响力会明显上升。

## 11. 下一步执行计划

### Phase 1：把第一轮结果做成可发表统计结果

- 完成每个数据集的配对关系解析。
- 为每个预设对照计算效应量、置信区间、FDR 和图源数据。
- 做敏感性分析：去掉 NAMPT、去掉 IL6、替代基因集、leave-one-module-out。
- 输出 Figure 2-4 的初稿图表。

### Phase 2：补齐 eNAMPT/NAD 证据

- 检索 PRIDE/ProteomeXchange、MetaboLights、Metabolomics Workbench 和公开 Olink/aptamer 研究。
- 优先寻找运动、肥胖、减重、炎症和血浆/血清 NAMPT/NAD 相关数据。
- 如果没有足够公共 eNAMPT 数据，就把 eNAMPT 明确作为待验证假说，不作为核心结论。

### Phase 3：运行 Evo2 调控变异模块

- 从 GTEx/eQTL/GWAS/ENCODE/GSE247455 建立候选变异表。
- 构建 GRCh38 ref/alt 序列窗口。
- 设置本地 `NVIDIA_API_KEY` 或 `NVCF_RUN_KEY` 后运行 Evo2 批量测试。
- 形成 Tier A/B/C 候选调控变异清单。

### Phase 4：写作与投稿路线

- 先写 Results，因为论文主张必须从实际证据长出来。
- 再写 Introduction，把问题收束到 NAMPT 轴转录程序的状态依赖性。
- 最后写 Abstract 和 Title，避免先写宏大叙事后证据接不住。

## 12. 需要继续收集的公共数据类型

尽管你没有自己的数据，仍然需要从公共数据库补齐这些信息：

- 样本层面 BMI、年龄、性别、训练状态、饮食/补充剂、药物、疾病状态、运动类型、强度、持续时间和采样时间点。
- 炎症标志物：CRP、IL-6、TNF、白细胞/单核细胞指标、NLRP3 或 NF-kB 相关读数。
- eNAMPT/visfatin 蛋白：血浆、血清或细胞外分泌证据。
- NAD 代谢物：NAD、NADH、NMN、NR、NAM、tryptophan-kynurenine pathway 相关代谢物。
- 体能和安全相关指标：VO2max、力量、胰岛素敏感性、肌肉损伤/恢复指标、CK、疼痛/DOMS、恢复时间。
- 遗传和调控信息：GWAS lead SNP、fine-mapped SNP、eQTL、caQTL、ATAC peak、enhancer、MPRA element。

这些数据不一定都要在第一篇论文中全部完成。第一篇应先把 NAMPT 轴模型和公共表达证据站稳，再用 Evo2 调控变异模块打通后续机制研究的第一步。
