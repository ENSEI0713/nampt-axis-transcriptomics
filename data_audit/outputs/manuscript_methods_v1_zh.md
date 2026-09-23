# Methods（v1，中文草稿）— 状态依赖的 NAMPT 轴转录程序：公共转录组与 Evo2 序列模型证据

> 本稿基于 2026-09-18/2026-09-20 落盘核验后的分析管线与统计输出。所有参数、阈值与数字均可追溯至
> `data_audit/outputs/` 下的结果表与 `scripts/` 下的可复现脚本；本稿为中文工作稿，转英文时逐项核验，
> 不改动任何数字与论断边界。配套：Results（`manuscript_results_v2_zh.md`）、
> Intro/Abstract/Title（`manuscript_frontmatter_v1_zh.md`）、论断边界与期刊定位（`manuscript_logic_v1_zh.md`）。

---

## 1. 研究设计与数据来源

本研究为基于公共人类转录组数据的二次分析（观察性、计算性设计），无新的人类受试者或动物实验，无个体层面干预。分析对象为**状态依赖的 NAMPT 轴转录程序**在肥胖、运动适应与代谢压力背景下的表达模式；全部证据限于转录组层面（NAMPT mRNA 及轴内基因表达），不构成 eNAMPT 蛋白或 NAD 代谢物丰度的测量。

### 1.1 数据筛选流程

公共数据集通过预设查询式在 GEO（Gene Expression Omnibus）检索获得（关键词覆盖运动/训练、骨骼肌、血液/PBMC、肥胖、脂肪组织、减重/代谢手术、肌肉损伤/恢复等），经逐条人工标注纳入优先级后，仅纳入满足全部条件的矩阵：

- **人类样本或人源细胞模型**；
- 公开可下载的处理表达矩阵，且有明确的样本级元数据（可解析条件、时间点、组织、干预）；
- 组织/细胞与问题相关：骨骼肌、脂肪组织、全血、PBMC、CD14+ 单核细胞、巨噬细胞或人骨骼肌细胞；
- 有明确对照结构（运动前后、训练前后、活动减少前后、营养恢复、肥胖/正常体重、减重/手术前后、代谢状态差异等）。

排除或降级标准：动物数据仅作机制补充、不进入主证据梯；癌症/严重感染/严重血管病等强混杂疾病队列不纳入；无法解析样本条件或缺少基本元数据者降级；仅有 NAMPT mRNA 的数据不用于支持 eNAMPT 蛋白结论。

### 1.2 纳入数据集与样本

共纳入 **9 个转录组分析单元、337 个样本**（8 个 GEO accession；GSE312393 拆分为急性运动 24h 与 6 周训练两个分析单元）。多数数据集 59 基因轴覆盖率 100%（GSE305038 84.7%、GSE282850 79.7%，缺失基因在评分时按可用基因计算）。数据集清单：

| 数据集单元 | 组织/细胞 | 设计背景 | 分析样本数 |
| --- | --- | --- | --- |
| GSE312393_24h_exercise | 骨骼肌 | 急性运动 24h 后 vs 对照 | 7 |
| GSE312393_6weeks_training | 骨骼肌 | 6 周训练前后 | 6 |
| GSE305038_activity_inactivity_exercise | 骨骼肌 | 正常/低活动背景下运动前后 | 25 |
| GSE292369_exercise_ketone_recovery | 骨骼肌 | 运动 + 酮体/安慰剂恢复 | 34 |
| GSE318937_exercise_oleuropein | 骨骼肌 | MICE/SIE × 补充剂/安慰剂 × 即刻/24h | 119 |
| GSE32575_monocytes_obesity_surgery | CD14+ 单核细胞 | 瘦 vs 肥胖；减重手术前后 | 48 |
| GSE272133_muscle_bariatric | 骨骼肌 | 肥胖/肥胖+T2D 减重手术前后 | 52 |
| GSE294150_visceral_adipose | 内脏脂肪 | 重度肥胖（减重手术时点） | 40 |
| GSE282850_muscle_cell_aicar_palmitate | 人骨骼肌细胞（LHCN-M2） | 分化 vs AICAR（运动模拟）vs palmitate（脂毒性） | 15 |

> 说明：样本计数口径经投稿前审稿核验统一为 337（9 个分析单元合计；GSE312393 两单元样本不重复计数）。
> 全部样本级评分表见 `nampt_axis_sample_scores.csv`（346 行含表头）。

### 1.3 数据下载与预处理

各数据集从 GEO 下载官方处理矩阵（series matrix 或补充处理文件，下载日期记录于 `geo_processed_download_manifest.csv`）。表达值按数据集自带单位使用（counts/FPKM/CPM 等），**仅在数据集内部做基因 z-score 标准化，绝不跨平台/跨数据集合并原始表达值**。预处理的变换类型逐数据集记录于 `nampt_axis_gene_coverage.csv`（如 log2(x+1) 或已是对数样值则不重复变换）。

## 2. NAMPT 轴基因集与评分

### 2.1 基因集构建

基于 NAMPT/NAD 生物学构建 v1 基因集（`NAMPT_axis_gene_set_v1.csv`）：**59 个 NAMPT 轴基因**，按功能模块归类（20 个模块），并按炎症样/修复样/双向三层分层：

- **repair（修复样，34 基因）**：NAD salvage 核心（NMNAT1/2/3、NAPRT、NADSYN1 等）、de novo NAD（QPRT）、sirtuin 修复（SIRT1/3/6）、AMPK-线粒体（PRKAA1/2、PPARGC1A）、线粒体生物发生（TFAM、NRF1）、氧化应激（NFE2L2、SOD2、CAT、GPX1）、巨噬 resolution（MRC1、ARG1）、脂肪代谢 resolution（PPARG、ADIPOQ）、胰岛素代谢（INSR、IRS1、SLC2A4、AKT2）、应激修复（FOXO3）、DNA 损伤修复（ATM、XRCC1、OGG1）、自噬（ATG5、BECN1、MAP1LC3B）等；
- **inflammatory（炎症样，19 基因）**：NAD 消耗-炎症（CD38、BST1）、NF-κB（NFKB1、RELA、TNF、IL6、IL1B、CCL2、CXCL8）、固有免疫（TLR4、NLRP3、CASP1）、单核/巨噬 marker（ITGAM、CD14、CD68、ADGRE1）、色氨酸-犬尿氨酸（KYNU、IDO1）、脂肪炎症（LEP）等；
- **both（双向，6 基因）**：NAMPT、PARP1/2（NAD 消耗-修复）、SQSTM1、MTOR、UCP2、UCP3 中按模块双重归类的基因（NAMPT 为核心基因，另 5 个按 both 层计）。

（注：34+19+6=59；both 层 6 基因在每数据集炎症/修复评分中按所属侧计入，具体基因使用情况见 `nampt_axis_gene_coverage.csv`。）

### 2.2 样本级评分

对每个数据集矩阵：

1. 提取 59 基因（或该数据集可检测到的子集）的表达；
2. **按基因在数据集内 z-score**（跨全部样本）：
   `z_gi = (x_gi − mean_g) / sd_g`；
3. 计算样本级分数：
   - `NAMPT_z`：NAMPT 基因的 z-score；
   - `inflammatory_score = mean(z over inflammatory 基因)`；
   - `repair_score = mean(z over repair 基因)`；
   - `balance_score = repair_score − inflammatory_score`（正值 = 相对修复样，负值 = 相对炎症样）。

所有分数仅用于数据集内部比较；跨数据集仅汇总方向一致性与随机效应 meta，不合并原始分数。

## 3. 预设对照与统计分析

### 3.1 对照定义

共定义 **19 个预设对照比较**（`nampt_axis_predefined_contrasts.csv`、`nampt_axis_formal_contrast_stats.csv`），全部优先采用研究内部对照：

- **运动层（exercise，12 个配对对照，嵌套于 4 个数据集）**：GSE312393（6 周训练配对对照；急性 24h 单元为非配对设计，计入 19 个预设对照但不进入配对 meta）、GSE305038（正常/低活动 × 运动前后）、GSE292369（运动 vs 静息）、GSE318937（MICE/SIE × 活性/安慰剂 × 即刻/24h，8 个配对对照）；
- **肥胖层（obesity，3 个预设对照比较）**：GSE32575（肥胖术后 vs 术前）、GSE272133（OB w52 vs w0；T2D w52 vs w0）；
- **细胞模型层（obesity_cell_model，2 个配对对照）**：GSE282850（AICAR vs 分化；palmitate vs 分化）。

### 3.2 效应量与检验

- **配对设计**：以受试者内 delta（后 − 前）为基础，报告 `mean_delta`、标准差、标准误、标准化效应量（Hedges 类）与 95% CI（`nampt_axis_formal_contrast_stats.csv`、`meta/meta_input_contrasts.csv`）；
- 非配对/多组设计按研究内对照结构处理，报告方向与 CI；
- **多重比较控制**：同一比较家族内的检验按指标报告 q 值（BH-FDR）；Cronbach α 仅作为模块内部一致性描述，**不**作为组间差异的显著性检验，与显著性 α/FDR 明确区分（审稿 CB-5 闭环口径）；
- 小样本对照（n≤4）与单一细胞系来源的对照**仅作方向性证据**，不赋予推断统计意义（审稿 CB-4 闭环口径）。

### 3.3 随机效应 meta 分析

- 方法：**DerSimonian–Laird 随机效应模型**，输入为数据集内标准化均值差（仅配对设计；方向性合并）；
- 输出：汇总效应、95% CI、方向一致率、I²、τ²、Q（`meta/meta_report.md`、`meta_results.csv`）；
- **聚类感知敏感性（审稿 CB-1 闭环）**：因 12 个运动对照嵌套于 4 个数据集（GSE318937 单独贡献 8 个），补充：
  1. **数据集级 DL**（以数据集为有效独立单元，k=4）：NAMPT_z 汇总 +0.965（95%CI 0.445–1.485，p=2.8e-4，方向 4/4）；balance_score −0.466（p=0.24，失去显著性）；inflammatory/repair 不显著（p=0.19/0.096）；
  2. **leave-one-dataset-out（LODO）**：NAMPT_z 在每次剔除后仍全部为正（k=11/10/11/4，p 均 <0.05）；
  - 敏感性输出：`meta/meta_sensitivity_dataset_level.csv`、`meta_sensitivity_lodo.csv`、`meta_sensitivity_report.md`。
- 高 I²（64–98%）如实报告为"效应方向一致但幅度随背景变化"，**不作为状态依赖性的统计证据**（审稿 CB-2 闭环）；状态依赖解读以数据集内时间点/训练状态描述与 moderator 可行性审计为准（见 §7）。

### 3.4 模块一致性（结构验证）

对每个数据集计算**模块内 Cronbach α** 与模块间相关矩阵（`axis_structure/module_alpha.csv`、`module_corr_matrix.csv`、`axis_structure_report.md`）：

- α 为内部一致性指标，仅用于描述"炎症程序 / 修复程序"是否形成可复现的共表达单元；
- 大队列（GSE272133 n=51、GSE305038、GSE32575）修复模块 α 0.79–0.91 支持双程序框架；小样本队列（GSE312393、GSE282850）出现负 α，α 证据优先引自大队列并如实披露小样本局限。

### 3.5 轴内免疫负荷代理

在 GSE318937（n=119 全样本）、GSE305038、GSE32575 中计算轴内单核/巨噬基因负荷代理（macro/mono marker burden，与 NAMPT 轴基因重叠的 marker 基因集）与炎症分数的相关（r=0.7–0.9 范围；GSE318937/GSE305038 r=0.77–0.89，GSE32575 中 NAMPT_z r=+0.75、inflammatory r=+0.91）：

- 该代理**不是细胞类型去卷积**（未使用 CIBERSORT/xCell 类方法），结果仅反映轴内基因共变，**不能作为独立细胞比例或因果证据**（审稿 R1-M5 闭环口径）；
- 相关计算基于数据集内全样本，未按运动后时间点子集拆分（"运动后"口径为全样本相关）。

## 4. 敏感性分析（Phase 1b）

基于保存的逐数据集表达矩阵重算评分并重跑相同预设对照（不覆盖原始 Phase 1 文件；`phase1b_sensitivity/`）。测试 9 个变体：

- 基因剔除：`drop_nampt`（删 NAMPT）、`drop_classic_cytokines`（删 CCL2/CXCL8/IL1B/IL6/TNF）；
- 模块剔除：`drop_nfkb_module`、`drop_monocyte_macrophage`、`drop_nad_salvage_core`、`drop_nad_consumption`、`drop_mito_repair`、`drop_autophagy_dna_repair`、`drop_insulin_adipose_metabolism`。

判读标准：与主分析的方向一致率、方向翻转数、CI 支持保留/丢失/新增、每变体最小保留基因数（`nampt_axis_sensitivity_*` 输出）。主 recompute audit 与原始样本级分数最大绝对差 ≤2.3e-15（浮点级）。主结论对剔除 NAMPT 及多数模块稳健；`drop_nfkb_module` 与 `drop_classic_cytokines` 造成最多 CI 支持变化，已在 Results 中按脆弱性措辞（`phase1b_sensitivity_report.md`）。

## 5. Moderator 可行性审计

样本级文件 346 行、formal contrast 76 行、预定义对照 19 个。审计字段覆盖（`meta/moderator_coverage.csv`）：timepoint 非空 70.2%、exercise_type 34.4%、nutrition_or_treatment 34.4%、intervention 74.9%、treatment 51.5%。

**结论：不做跨研究 moderator 元回归**——效应量嵌套在数据集/受试者内，且无统一跨研究 moderator 编码与效应协方差。可在 GSE318937、GSE305038、GSE312393 内部做时间点/训练状态/干预背景的描述；不报告正式 moderator p 值，不把 I² 解释为状态依赖证据（`meta/moderator_feasibility_report.md`）。

## 6. Evo2-40B 调控变异管线

### 6.1 候选变异构建（Ensembl REST）

以 NAMPT 轴核心基因 **NAMPT/CD38/BST1/SIRT1/SIRT3/SIRT6/IL6/TNF** 的 TSS ±2 kb 启动子近端窗口为目标，经 Ensembl REST 检索变异注释（功能注释含 missense、splice_region、5'UTR、TF_binding_site、regulatory_region，及 130 个 ClinVar 注释位点）：

- 12,961 条原始记录 → **432 条优先级功能候选**（NAMPT 全保留 12 条；其余基因每窗上限 60 条；`build_variant_candidates.py`、`candidates_priority.csv`）。

### 6.2 GRCh38 ref/alt 窗口

对每个候选构建 **GRCh38 参考/替代等位 2 kb 窗口**（`build_ref_alt_windows.py` → `windows.bed`、`windows.fasta`）：430 条单碱基 SNP + 2 条 indel，0 条 ref 不匹配；每条候选一个 ref 序列与一个 alt 序列（共 864 条序列）。

### 6.3 Evo2 打分

Evo2-40B（NVIDIA hosted generate 端点，`enable_logits=true`，单 token）对窗口打分，三种分数（`run_evo2_scoring.py`）：

- **Score A（allele surprisal，全量完成）**：`delta_surprisal = log P(alt) − log P(ref)`，flank 200 bp，DNA 规范化 A/C/G/T softmax。432/432 唯一 rsid 完成，0 缺失、0 重复（`scores.csv`）。|delta| 中位 1.118；|delta|≥2 有 174 条、≥4 有 94 条；高扰动集中在 IL6/SIRT1/TNF 窗口（观察，非因果）。**符号不解释为有益/有害**；
- **Score B（pseudo-likelihood，短名单完成）**：对 104 条短名单（|delta|≥4 的 94 条 + NAMPT 全窗口 12 条）做下游 8 bp 双链传播：`PLL = Σ_i log P(base_i | context + allele + bases<i>)`，`delta_PLL = PLL(alt) − PLL(ref)`，fwd 与 rc 双链各 32 次 generate 调用/变异，0 失败（`scores_B.csv`）。delta_PLL 中位 −0.876；Score A↔B 符号一致 87%；**strand 一致 65%（68/104），fwd/rc 相关 r≈0.13**——双链一致性有限，Tier C 候选按假设集处理而非按稳定信号排序（审稿 R1-M7 闭环）；
- **Score C（多 seed 稳定性）实证退化**：pilot 10 变异 × 5 seed 全部 sd=0——hosted 端点 logits 不随 random_seed 变化（seed 只影响采样，不影响 score 所用的 log 概率），多 seed 稳定性无信息，不跑全量（如实披露，替代以 strand 一致性 + 外部 QTL 复现作为稳定性证据；`evo2_variant_results_report.md` §6）。

### 6.4 eQTL/GWAS 合并与 Tier 分层

- 证据源（2026-09-18 实时核验）：**GTEx REST v2**（`singleTissueEqtl`，组织：Muscle_Skeletal、Adipose_Subcutaneous、Adipose_Visceral_Omentum、Whole_Blood；取跨组织最小 p）+ **GWAS Catalog REST**（按 rsid 关联，p = mantissa × 10^exponent）。OpenGWAS 与 eQTL Catalogue 端点在本环境返回 404，如实记录并放弃（`merge_qtl_gwas.py`，带缓存与失败缓存，可 `--resume`）。
- **Tier 规则**：
  - Tier A：Evo2 扰动（|Score A|≥4 或 Score B strand 一致）且 GTEx p<1e-4 且 GWAS p<5e-8；
  - Tier B：Evo2 扰动且（GTEx 或 GWAS 达阈）；
  - Tier C：Evo2 扰动、无外部支持（仅探索）；
  - External-only：外部 eQTL/GWAS 证据强、但 Evo2 扰动温和；
  - Excluded：两侧均无证据。
- 分布（432 变异）：**A=0、B=0、C=97、External-only=9、Excluded=326**。Tier A/B 为空是如实结果：Evo2 高扰动短名单以稀有变异为主，GTEx 只测常见变异、GWAS Catalog 对其 rsid 覆盖稀疏，导致 Evo2 扰动与外部支持几乎不重叠。9 个 External-only 为强证据常见位点（TNF rs1800629：GTEx p≈7e-24 + GWAS p≈3e-28；IL6 rs1800795：GTEx p≈3.5e-100 + GWAS p≈2e-25 等），但 Evo2 分数温和。
- **主图门槛判定**：Evo2 模块未满足协议"稳定扰动 + 公共 QTL/GWAS 支持"的重叠要求，**不作为主图**，降为补充/探索性模块；Figure 5 保留流程 + 候选构成面板，打分面板放补充材料（`evo2_variant_results_report.md` §5/§8）。

### 6.5 Evo2 边界

Evo2 分数仅支持调控假说的优先级排序：不证明因果、不预测临床风险、不替代实验验证（MPRA/CRISPRi 等后续验证基础）。

## 7. 软件、可复现性与伦理边界

- 分析脚本位于 `scripts/`（含 `public_data_audit.py` → `run_evo2_scoring.py` 全管线），输出表位于 `data_audit/outputs/`；所有公共数据保存 accession、下载日期与处理脚本（`geo_processed_download_manifest.csv`、`audit_run_log.json`）。
- 主要计算：Python 3（NumPy/SciPy 类实现 z-score、配对统计与 DL meta）；Cronbach α 按标准公式（以数据集内基因 × 样本矩阵计算）；Evo2 打分经 NVIDIA hosted 端点。
- 计划将处理矩阵、评分表、图源数据与代码归档至 Zenodo/OSF/Figshare（获得 DOI）；第三方公共原始数据用 accession 引用，不随意重新分发。
- **伦理与用途边界**：全部为公共数据二次分析，无个体干预；公共转录组数据**不可用于个体诊断或运动处方**；NAMPT mRNA 状态 ≠ eNAMPT 蛋白或 NAD 代谢物；eNAMPT 方向性为可检验预测（肥胖→炎症程序；训练→修复标志物），待蛋白/代谢物验证。

## 8. 数字来源对照表（转英前核验用）

| 数字/参数 | 值 | 落盘来源 |
| --- | --- | --- |
| 基因集 | 59 基因 / 20 模块 / repair 34 / inflammatory 19 / both 6 | `NAMPT_axis_gene_set_v1.csv` |
| 样本 | 9 分析单元 / 337 样本 | `nampt_axis_sample_scores.csv`（346 行含表头）、`geo_processed_profile.csv` |
| 预设对照 | 19 | `nampt_axis_predefined_contrasts.csv` |
| 运动 meta（对照级） | NAMPT_z +0.85（95%CI 0.53–1.17，92%，p=1.8e-7，I²=64%）等 | `meta/meta_report.md`、`meta_results.csv` |
| 运动 meta（数据集级） | NAMPT_z +0.965（k=4，p=2.8e-4）；balance −0.466（p=0.24） | `meta/meta_sensitivity_dataset_level.csv` |
| LODO | NAMPT_z 全为正 | `meta/meta_sensitivity_lodo.csv` |
| 肥胖层 | k=3，方向性 | `meta/meta_report.md` |
| 细胞模型 | k=2，方向性；NAMPT_z +1.42 | `meta/meta_report.md` |
| α | 大队列 0.79–0.91 | `axis_structure/module_alpha.csv` |
| 免疫负荷 r | 0.7–0.9（全样本） | `cell_composition/cell_scores.csv`、`sensitivity_report.md` |
| Phase 1b | 9 变体 | `phase1b_sensitivity/` |
| Evo2 候选 | 12,961 → 432 | `evo2/candidates_priority.csv` |
| Score A | 432/432；\|delta\| 中位 1.118 | `evo2/scores.csv` |
| Score B | 104 条；strand 一致 65% | `evo2/scores_B.csv` |
| Score C | 退化（sd=0） | `evo2/scores_C.csv`、报告 §6 |
| Tier | A=0/B=0/C=97/Ext=9/Excl=326 | `evo2/tiers.csv` |

---

*工作稿结束。转英文全文时按 §8 逐项核验，并核对目标期刊格式要求。*
