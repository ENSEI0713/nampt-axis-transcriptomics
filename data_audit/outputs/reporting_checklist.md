# Reporting Summary / Checklist（投稿前填写骨架）

> 依据：Nature Portfolio Life Sciences Reporting Summary（`https://www.nature.com/authors/policies/ReportingSummary.pdf`）
> 与 Communications Biology / Nature Communications 通用要求。本文件为投稿前填写骨架，
> 标记 ✅ 的项已可确认，⚠ 的项需作者/投稿时补充。目标期刊：Nature Communications / Genome Biology。

## 1. 数据与材料（Data & Materials）

| 项 | 状态 | 说明 |
| --- | --- | --- |
| 数据来源 | ✅ | 8 个 GEO accession（9 分析单元），全部公开可下载，accession 见 Data Availability |
| 数据可用性声明 | ✅ | 已写入 EN 稿 Data Availability 节 |
| 代码可用性声明 | ✅ | 已写入 EN 稿 Code Availability 节（[repository URL] 与 Zenodo DOI 待填） |
| 补充材料清单 | ✅ | 8 个 Supplementary Data 源文件已核实存在（figure_legends_supp_data.md manifest）；打包待执行 |
| 原始数据是否可获取 | ✅ | GEO 原始/处理矩阵均公开 |

## 2. 实验模型与统计（Experimental models & Statistics）

| 项 | 状态 | 说明 |
| --- | --- | --- |
| 样本量说明 | ✅ | 9 单元 337 样本；每数据集样本数列于 Methods 表 1 |
| 数据纳入/排除 | ✅ | Methods §1.1 纳入/排除标准明确 |
| 重复（replication） | ✅ | 跨 9 数据集/4 运动队列证据梯；LODO 敏感性 |
| 随机化/盲法 | ⚠ | 公共数据二次分析，无干预随机化；注明"不适用" |
| 统计方法 | ✅ | DL 随机效应 meta[4]、BH-FDR[5]、Cronbach α[6]、聚类感知数据集级 + LODO |
| 多重比较控制 | ✅ | q 值（BH-FDR）按比较家族报告；α 与显著性 α 区分 |
| 软件版本 | ✅ | Python 3.14.5 + NumPy 2.4.6 + SciPy 1.18.0（分析环境实测） |

## 3. 具体分析（按结果逐项）

| 结果 | 统计方法 | 状态 |
| --- | --- | --- |
| R1 模块一致性 | Cronbach α + 模块间相关 | ✅ |
| R2 运动 meta | DL 随机效应 + 数据集级 + LODO | ✅ |
| R2 免疫负荷 | Pearson/Spearman r（全样本） | ✅（未做 FDR——审稿 R1-M5 已注明边界，投稿时确认） |
| R3 肥胖层 | k=3 方向性 | ✅ |
| R4 细胞模型 | k=2 方向性 | ✅ |
| R5 Evo2 | Score A/B/C + Tier 分层 | ✅ |

## 4. 其他要求（Editorial policy）

| 项 | 状态 | 说明 |
| --- | --- | --- |
| 利益冲突声明 | ✅ | 已写入 End Notes（no competing interests） |
| 作者贡献 | ✅ | 已写入 End Notes（Y.C. 一作分析写作；Y.Z. 通讯指导；Z.S./M.Z. 解读修订） |
| 伦理/同意 | ⚠ | 公共数据二次分析——注明"本研究为公共数据二次分析，无需伦理审批"（投稿时在 Methods 或 cover letter 说明） |
| 图注完整性 | ✅ | 6 图图注已写入正文 Figure Legends 节（figure_legends_supp_data.md 审定版） |
| 图 ≤10 显示项 | ✅ | 6 图 0 表（补充材料不计入） |
| Title ≤15 词 | ✅ | 现 8 词（"State-dependent NAMPT-axis transcriptional programs in obesity and exercise"） |
| Abstract ≤150 词 | ✅ | 现 141 词（NC "Here, we show" 结尾） |
| 参考文献编号制 | ✅ | 已转编号制（1-16），正文已插 [n] 标记，按首次出现顺序重排 |

## 5. 投稿前待填占位（TODO）

- [ ] [repository URL] / Zenodo DOI（代码与数据归档后填）
- [ ] References 中 4 条 GEO 文献第一作者与卷期页核验（GSE292369/312393/318937/282850，bib 已标 TODO）
- [ ] 6 张图的图注（title + panel + error bar 定义）
- [ ] Supplementary Data 1-8 实际文件整理（对应 Methods 中 8 处引用）
- [ ] Reporting Summary 正式版提交（本骨架转填官方 PDF 模板）
- [ ] Cover letter（投稿信，突出概念框架 + 证据梯 + 边界纪律；NC/GB 强调纯公共数据计算论文的先例）

*2026-09-20 生成。*
