# Communications Biology 格式核对（manuscript_full_en_v1 对照官方 checklist）

> 依据：Comm Biol 官方 Manuscript Checklist（`https://www.nature.com/documents/commsbio_checklist.pdf`，
> 2026-09-20 抓取）+ Content types 页（Article ~5,000 词建议）。
> 状态：对照当前 HEAD 的 `data_audit/outputs/manuscript_full_en_v1.md`（EN v1，含完整 Discussion、
> Abstract 143 词、无 em dash）与 `references_v1.bib`（v2，15 条，含 GEO + eNAMPT/NAD 综述）。

## 硬性要求 vs 当前状态

| 项目 | Comm Biol 要求 | 当前状态 | 差距 |
| --- | --- | --- | --- |
| Title | ≤15 词，不含句读（逗号/括号可） | 首选 Title 17 词（含子标题冒号后部分），见下 | ⚠ 需压缩到 ≤15 词 |
| Abstract | ≤150 词；不含引用；现时态；2-3 句背景开头；'Here we show' 式主体；结尾结论+含义 | **143 词**，无引用，现时态，背景开头，结尾结论 | ✅ 通过（背景 2 句、主体 3 句、结尾 1 句，结构合规） |
| 主文总长 | ≤5,000 词（Intro+Results+Discussion） | 当前 EN 稿约 4,600-4,800 词（Methods 不计入 5k） | ✅ 估算通过（提交前精算） |
| 章节顺序 | Title→Abstract→Introduction→Results→Discussion→Methods→References→End Notes→Figure legends→Tables | 当前顺序符合（EN 稿内 Discussion 在 Methods 前） | ✅ |
| Introduction | ~≤1,000 词；无子标题；末段含结果+结论摘要；不引用显示项 | 4 段漏斗，无子标题，末段含预览 | ✅ 估算通过 |
| Results | 子标题 <60 字符；无 'data not shown' | Result 1-5 子标题均 <60 字符 | ✅ |
| Discussion | 无子标题；与 Results 少重叠 | 完整 5 段，无子标题 | ✅ |
| Methods | 主文内；子标题 <60 字符；含 Statistics and Reproducibility 小节 | 中文稿 8 节；EN 稿 Methods 含统计与可复现性 | ✅ 转英时把 §3 统计、§7 可复现性组织为独立小节 |
| Data availability | 必需：数据可用性声明 | 稿内有 accession 引用 + Zenodo/OSF 计划 | ⚠ 需成独立 "Data Availability" 小节（EN 稿） |
| Code availability | 如适用：代码可用性声明 | 计划归档 Zenodo/OSF + GitHub 链接 | ⚠ 需成独立 "Code Availability" 小节 |
| 参考文献 | **按出现顺序编号**；格式 'Authors, Title, Journal, Volume, First-last page, (year)'；仅已发表/在版（含 doi） | **当前 bib 为作者-年份制（author-year）** | ⚠ **最大差距**：Comm Biol 用**编号制**，需把 bib 转为编号制并按正文出现顺序重排 |
| 显示项 | 图+表合计 ≤10；图注 ≤350 词/条；避免红绿配色 | 6 图（figure1-5，其中 figure3 含 2 张）+ 计划中表 | ✅ 数量合规（6 图 0 表，≤10） |
| 补充材料 | 单 PDF ≤30 MB；不含 Results；补充引用独立编号 | Evo2 打分面板建议入补充 | ✅ 规划中 |
| 报告清单 | Life Sciences Reporting Summary（现为 Reporting Checklist） | 投稿前需填 | ⚠ 待办 |

## 需要执行的修正（按优先级）

1. **参考文献制式**（最大改动）：`references_v1.bib` 目前是 author-year（BibTeX 默认）；
   Comm Biol 要求**数字编号、按正文首次出现顺序**。方案：
   - 在 EN 稿正文为每个引用加 `[n]` 编号占位；
   - bib 条目加 `sortkey`/按出现顺序重排，或直接用 `\bibliographystyle`（若投稿用 Word，则手动按顺序列出）；
   - 格式样例：`Aguet, F. et al. The GTEx Consortium atlas of genetic regulatory effects across human tissues. Science 369, 1318-1330 (2020).`
2. **Title 压缩到 ≤15 词**：当前首选 `State-dependent NAMPT-axis transcriptional programs in obesity and exercise adaptation: public transcriptomic and Evo2 sequence-model evidence` 为 17 词。
   建议：`State-dependent NAMPT-axis transcriptional programs in obesity and exercise`（10 词）+ 副题不要（Comm Biol 主标题含冒号算词数）。
   或保留副题但整体 ≤15 词：`State-dependent NAMPT-axis programs in obesity and exercise: transcriptomic and Evo2 evidence`（14 词）。
3. **补 Data Availability / Code Availability 独立小节**（EN 稿 Methods 之后、References 之前）。
4. **END NOTES**：Acknowledgements、Author contributions、Competing interests 三声明（投稿时加）。
5. **投稿前**：填 Reporting Checklist（https://www.nature.com/authors/policies/ReportingSummary.pdf）。

## 检索来源

- Comm Biol Manuscript Checklist PDF: https://www.nature.com/documents/commsbio_checklist.pdf
- Content types: https://www.nature.com/commsbio/submit/content-types
- 说明：Comm Biol 明确"initial submission 不强制格式，格式仅在 acceptance 前应用"，因此上述修正可在
  投稿前一次性完成，不阻塞初稿内容。

*本核对记录 2026-09-20。*
