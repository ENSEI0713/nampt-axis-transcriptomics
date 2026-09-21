# PROGRESS — NAMPT-NAD 炎症-修复轴项目接续索引

> 最后更新：2026-09-20 15:20 UTC+8
> 用途：本文件是任何新对话接续本项目的唯一索引。新对话先读本文件，再按需读列出的产物。

## 1. 项目是什么

用公共人类多组学（GEO 表达矩阵）与 Evo2-40B 序列模型，解析肥胖和运动适应中**状态依赖的 NAMPT 轴转录程序**（审稿后由"NAMPT-NAD 炎症-修复轴"收敛而来，eNAMPT/NAD 代谢物为待验证预测）。论文主轴单一：NAMPT 轴转录程序的状态依赖性。

## 2. 已完成（git 提交 018c0f1 → 44a1f66，工作区干净，工作区干净）

### Phase A 基线化
- `.gitignore`（排除 downloads/、__pycache__、_quick_test.py、.env）
- `README.md`（目录结构 + 运行顺序）
- 首次提交 `018c0f1`；git 作者为仓库级 `yanji <yanji@local>`

### Phase B 统计证据梯（新增，均为论文级证据）
- **随机效应 meta**：`scripts/meta_nampt_axis.py` → `data_audit/outputs/meta/`
  - 运动层 k=12：NAMPT_z 汇总 **+0.85**（95%CI 0.53–1.17，方向一致 92%，p=1.8e-7，I²=64%）；balance **−0.62**（CI −1.12–−0.12，83%，p=0.016，I²=98%）；inflammatory +0.28 (ns)；repair −0.33 (ns)
  - 肥胖层 k=3：NAMPT_z +0.14（I²=0%）；inflammatory +0.57（高异质性）→ 仅方向性
  - 细胞模型 k=2：NAMPT_z +1.42（100% 方向一致）
- **轴结构一致性**：`scripts/axis_structure_analysis.py` → `data_audit/outputs/axis_structure/`
  - 大队列 repair 模块 α 0.79–0.91（GSE272133 n=51）；GSE305038 均值 0.78；GSE32575 均值 0.61；小样本负 α（如实披露）
- **轴内免疫负荷代理**：`scripts/cell_composition_sensitivity.py` → `data_audit/outputs/cell_composition/`
  - 明确不是细胞去卷积（macro/mono 是与轴基因重叠的 marker burden proxy）；炎症分数与轴内单核/巨噬基因代理高相关（r=0.7–0.9），仅作轴内共变描述，不作独立细胞比例或因果证据
- `manuscript_logic_v1_zh.md` 已更新（Result 1-3 补入新证据）

### Phase C Evo2 管线（Score A + B 完成；C 退化；eQTL/GWAS 合并完成）
- `scripts/build_variant_candidates.py`（Ensembl REST）：12,961 原始 → **432 优先级功能候选** `data_audit/outputs/evo2/candidates_priority.csv`
- `scripts/build_ref_alt_windows.py`：GRCh38 ref/alt 2kb 窗口 **432 对**（430 SNP + 2 indel，0 条 ref 不匹配）→ `windows.bed` / `windows.fasta`
- `scripts/run_evo2_scoring.py`：Score A allele surprisal + Score B pseudo-likelihood + Score C stability（`--mode A/B/C`，密钥门控、断点续跑、日志脱敏）
  - 修复：BED `start` 为字符串，`position` 改为 `int(start)+offset`
  - **Score A 全量**：432/432 unique rsid，0 缺失、0 重复 → `scores.csv`
    - delta 中位 −0.81，\|delta\| 中位 1.12；\|delta\|≥2 n=174，≥4 n=94；高 \|delta\| 在 IL6 / SIRT1 / TNF（观察，非因果）
  - **Score C 实证退化**：pilot 10×5 seeds 全 `sd=0` —— hosted 端点 logits 不随 seed 变，多 seed 稳定性无信息（见报告 §6），不跑全量
  - **Score B 完整**：短名单 \|delta\|≥4 (n=94) + NAMPT 全窗口 (n=12)=104 条，0 失败 → `scores_B.csv` + `scoring_B_log.jsonl`
    - delta_PLL 中位 −0.88；Score A↔B 符号一致 87%；**strand 一致仅 65%**（fwd/rc 相关性 r≈0.13，如实披露）
- **eQTL/GWAS 合并**：`scripts/merge_qtl_gwas.py`（GTEx REST v2：4 相关组织 + GWAS Catalog；带缓存与失败缓存）→ `data_audit/outputs/evo2/tiers.csv`
  - Tier 分布：A=0、B=0、C=97（Evo2 扰动无外部支持）、External-only=9（常见位点如 rs1800629/rs1800795 有强 eQTL+GWAS 但 Evo2 温和）、Excluded=326
  - **Tier A/B=0 是如实结果**：短名单 Evo2 扰动候选几乎全是稀有变异，GTEx 不测稀有变异、GWAS Catalog 覆盖稀疏 → Evo2 扰动与外部支持几乎不重叠
- 门槛报告：`data_audit/outputs/evo2/evo2_variant_results_report.md`（**主图定案：NOT MAIN FIGURE**，Evo2 模块降为补充/探索性；§5/§8 已更新）

### Phase D 图件（新增 3 张，×4 格式 pdf/svg/png/tiff）
- `figure1_framework`（概念框架 6 面板）— `scripts/plot_figure1_framework.py`
- `figure3_meta_forest`（meta 森林图）— `scripts/plot_meta_forest.py`
- `figure5_evo2_prioritization`（流程+候选构成）— `scripts/plot_evo2_figure.py`
- 全部在 `data_audit/outputs/figures_phase2/`

### Phase E eNAMPT 决策（已定案）
- 检索记录：`data_audit/outputs/enampt_retrieval.md`（MetaboLights 关键词过滤 API 不可用、PRIDE 端点 404）
- **决策：eNAMPT/NAD 代谢物降级为可检验预测，不进核心结论**（已写入 manuscript_logic_v1_zh.md 论断边界）

### Phase F 写作
- `data_audit/outputs/manuscript_results_v2_zh.md`：Results 1-5 草案（全部数字有落盘支撑）
- `data_audit/outputs/manuscript_frontmatter_v1_zh.md`：Introduction/Abstract/Title 中文草稿（Title 首选 State-dependent NAMPT-axis transcriptional programs...）

## 3. 待办（按优先级）

### P0 Evo2 分层（Score A + B + eQTL/GWAS 合并完成；主图定案 NOT MAIN FIGURE）
1. ~~密钥生效 + Score A pilot 20 + 全量 432~~ **done**（`scores.csv`）
2. ~~Score B 短名单 + Score C 验证~~ **done**
   - B：\|delta\|≥4 (94) + NAMPT (12) = 104 条全量 → `scores_B.csv`（delta_PLL 中位 −0.88；Score A↔B 符号一致 87%；**strand 一致 65%**，如实披露）
   - C：实证退化（端点确定性，seed 不影响 logits，pilot 10×5 sd=0），不跑全量
3. ~~eQTL（GTEx）+ GWAS（GWAS Catalog）合并 → Tier 分层~~ **done** → `tiers.csv`
   - A=0、B=0、C=97、External-only=9、Excluded=326（原因见 Phase C，如实披露）
   - 若论文需要"Evo2 推荐 + 外部支持"重叠，可放宽 \|Score A\|≥2 (n=174) 或加 GTEx LD 代理——需在正文论证，不悄悄塞
4. Figure 5：维持流程+候选构成面板；如需要可加补充图带打分面板，**不把裸 |delta| 排名做进主图**
5. ~~更新 `evo2_variant_results_report.md` 主图判定~~ **done**（NOT MAIN FIGURE，Evo2 降为补充/探索）

### P1 论文推进
- ~~写 Introduction / Abstract / Title~~ **done（中文草稿）** → `data_audit/outputs/manuscript_frontmatter_v1_zh.md`  - 含 4 段漏斗 Introduction、Nature 式浓缩 Abstract、4 个 Title 备选
  - 前置完成：Results 数字核验修正（337 样本、n=24/47、α 0.60、repair CI、补细胞层 inflammatory +0.55；"运动后"口径注明全样本相关）、Result 5 重写为 Evo2 完成态（Tier A/B=0 如实披露）
- ~~用 ccf-humanization + ccf-paper-writer 技能打磨 Results~~ **done**
  - em dash 16→0（`check_prose_quality.py` PASS；负号/区间用 U+2212 不受影响）；删 3 处"如实披露/如实结果"流程旁白；科学边界（转录组证据、小样本方向性、Evo2 非因果）保留
- ~~MoTrPAC 公共释放的蛋白/代谢组覆盖检查~~ **done** → `data_audit/outputs/motrpac_coverage_check.md`
  - 结论：MoTrPAC 确有蛋白/代谢组（论文级事实），但人类数据受控（dbGaP phs002292）、门户 API 不可程序化、NAD 通路分析物覆盖未人工核验 → **eNAMPT 继续保持在"可检验预测"，不升核心结论**
- ~~投稿前模拟审稿（3 路盲审）~~ **done** → `data_audit/outputs/pre_submission_review_synthesis.md`
- ~~按审稿建议修订 CB-2/CB-3/CB-5/R2-M3~~ **done** → `data_audit/outputs/meta/moderator_feasibility_report.md`；新增 moderator 覆盖与可行性报告，肥胖层/多重比较/NAMPT 轴转录程序边界已同步，未伪造跨研究元回归
  - 共识优势：Tier A/B=0 诚实报告、边界纪律、概念框架、跨数据集设计
  - 共识 blocking：meta 12 配对对照未处理聚类(CB-1)、高 I² 误当状态依赖证据(CB-2)、肥胖层 k=3 不足(CB-3)、细胞模型 p=3.2e-10 精度虚高(CB-4)、无多重比较控制(CB-5)
  - 其他：balance 两腿不显著但措辞过强(R2-M1)、"NAMPT-NAD"过度承诺(R2-M3)、免疫负荷相关机械性(R1-M5)、C 类改 strand 一致子集(R1-M7)
  - 不改变结论，需改统计呈现与标题/摘要对象收敛
  - CB-1 已修：聚类感知敏感性（数据集级 DL + leave-one-dataset-out）→ `meta_sensitivity_dataset_level.csv`/`lodo.csv`/`report.md`；NAMPT_z 稳健（k=4 +0.965 p=2.8e-4），balance 在聚类感知下失去显著性（p=0.24），Results/Abstract/Result 4 已如实降级
- ~~R1-M5 / R1-M7 / Phase 1b 定义~~ **done**：免疫负荷代理边界已写清（非去卷积）；Tier C 97 个中 68 个（70%）在 strand 一致子集，标为假设集；Phase 1b 首次出现处已给定义
- **审稿遗留全部闭环**（CB-1~CB-5、R1-M5/M7、R2-M1/M3、样本数口径、Abstract 限定）——见 `data_audit/outputs/pre_submission_review_synthesis.md` §7 与各 commit

### P2 投稿推进（进行中）
- **写 Methods** ✅ 中文草稿完成 → `data_audit/outputs/manuscript_methods_v1_zh.md`
  - 10 节：数据来源与纳入 / 基因集与评分 / 预设对照与统计（含 DL meta + 聚类感知 + LODO + BH-FDR 口径）/ 模块一致性 / 轴内免疫负荷 / Phase 1b 敏感性 / moderator 可行性 / Evo2 管线（Score A/B/C、GTEx+GWAS Catalog、Tier 规则）/ 可复现性 / 数字来源对照表
  - 所有数字已对照落盘（meta_results.csv、module_alpha.csv、scores.csv、tiers.csv 等）核验
- **转英文全文** ✅ v2（含完整 Discussion）→ `data_audit/outputs/manuscript_full_en_v1.md`
  - Abstract/Introduction/Results 1-5/Methods/Discussion（完整 5 段）/边界；Abstract 141 词（NC "Here, we show" 结尾）、无 em dash
  - 中英数字已逐项抽检一致（EN 内部两处舍入精度 0.445–1.485、1.118 已统一）
- **定期刊** ✅ 定案：**第一目标 Nature Communications，第二 Genome Biology，保底 Communications Biology**（用户指示）
  - 已按 **NC 作者指南**核对：Title ≤15 词无标点 ✅（现 8 词）、Abstract ≤150 词 ✅（141，Here we show 结尾）、参考文献编号制 ≤70 条 ✅（16 条）、主文 ≤6000 词 ✅、图 ≤10 ✅（6 图）、Data/Code Availability ✅、Reporting Summary 投稿即需
  - 湿实验决策：用户明确不做 MoTrPAC/MPRA/CRISPRi（本篇作研究基石，另备综述+meta 分析形成系列）
- **参考文献** ✅ v2 → `data_audit/outputs/references_v1.bib`（15 条：6 基础 + 6 GEO 原论文 + 3 eNAMPT/NAD 综述，已核验）
  - GSE32575 原论文 ✅ 已核验补入（Hulsmans 2012, PLoS ONE 7(1):e30414；三源一致）
  - GSE294150（未发表）投稿时按数据集引用（Data Availability 引用 accession）
- **作者** ✅ 已写入 EN 稿头部：Yanjing Chen（一作）/ Zhenyu Shao / Min Zhang / Yan Zhang（通讯）
  - 邮箱：chenyanjing@cupes.edu.cn（一作）、zhangyan2021@cupes.edu.cn（通讯）
  - 单位：①Laboratory and State-Owned Assets Management Division, Capital University of Physical Education and Sports, Beijing 100191 ②Sports & Medicine Integrative Innovation Center, CUPES ③Beijing Key Laboratory of Interdisciplinary Intelligent Technologies in Sports Medicine and Engineering ④Precision Omics Laboratory for Sport Medicine & Engineering（隶属③）
  - 关系：Yanjing Chen 为 Yan Zhang 教授团队老师（不同部门同一团队）；Zhenyu Shao 硕士研究生、Min Zhang 博士研究生
- **Title** ✅ 已定稿：**"State-dependent NAMPT-axis transcriptional programs in obesity and exercise"**（8 词，≤15 达标；无标点）— 2026-09-20 定稿
- **EN 稿投稿清理** ✅（读稿审稿 blocking 项已清）：backtick 文件路径、审稿代号（CB/R1-M/R2-M）、§8 内部核数表、占位符已清除；章节重排为 Abstract→Intro→Results→Discussion→Methods→Data/Code Availability→References→Figure Legends→End Notes；已补 Data Availability / Code Availability / References（编号制 1-16）/ End Notes（Acknowledgements + Author contributions + Competing interests）
- **GSE32575 引用** ✅ 已核验补入 bib（Hulsmans 2012, PLoS ONE 7(1):e30414；三源核验）
- **湿实验决策**：用户明确不做 MoTrPAC/MPRA/CRISPRi 湿实验（后续有经费再补）；本篇作为研究基石，另备综述 + meta 分析各一篇
- **引用编号重排** ✅（2026-09-20）：正文 16 条引用严格按首次出现顺序 1→16 递增；References 同步重排；GEO 数据集条目（Beiter/Gries/Mosquera-Lopez/Lanfranchi/Kovac/Hulsmans/Nishino）编号 5-12 且正文带 <sup> 标注；Gries 2025 补卷期页 330, E26–E37 (2026)（Crossref 核验）
- **缩写定义** ✅（审稿 M5）：Intro 增加 "Abbreviations used throughout: T2D…MICE…SIE…GRCh38…LODO…BH-FDR"；正文首次出现处展开全称
- **图件引用** ✅（审稿 M6）：Figure 1 已在 Result 1 引用；Figure Legends 节已插入正文（6 图图注，figure_legends_supp_data.md 审定版）
- **投稿资产** ✅（2026-09-20 生成，`data_audit/outputs/submission_pack/`）：
  - Supplementary Data 1-8（xlsx，源 CSV 全部核实存在）
  - cover_letter_v1.md（NC 投稿信草稿）
  - reporting_summary_draft_v1.md（Reporting Summary 草稿，待转填官方 PDF 模板）
- **checklist** ✅ 已同步：Title 8 词 / Abstract 141 词 / 软件版本（Python 3.14.5 + NumPy 2.4.6 + SciPy 1.18.0）/ 图注完整 / 补充材料清单 8 份源文件核实
- **参考文献 bib** ✅ 已补全：5 条 GEO 文献作者展开（0 占位）、Gries 卷期页+DOI、cronbach 类型修正为 @article
- **待办（投稿前需用户/作者完成，非代码可做）**：
  1. 代码归档后填 [GitHub repository URL] 与 Zenodo/OSF DOI（正文 Code/Data Availability 占位）
  2. 8 个 Supplementary Data xlsx 上传 + 图件（tiff/png ≥300 dpi）随稿提交
  3. Reporting Summary 官方 PDF 模板转填（草稿在 submission_pack/）
  4. Cover letter 作者签名与日期确认（草稿在 submission_pack/）
  5. 作者单位/邮箱最终核对（头部已写 CUPES，投稿系统填写时确认）
- **最后一轮审稿复检** ✅（2026-09-20 三线：写作/数字/格式）全部通过，修复项已闭环：
  - 数字核验：meta（+0.85/0.53–1.17/p=1.8e-7/I²=64%、balance −0.62、k=4 +0.965、LODO 全正）、Evo2 Tier（A=0/B=0/C=97/Ext=9/Excl=326）、median|delta|=1.118、≥2=174/≥4=94、strand 65%、α 值（0.79/0.82/0.83/0.91/0.86）、免疫负荷 r（0.77–0.89；0.75/0.91）全部与落盘 CSV 一致
  - 样本数口径：346 rows（9 单元，GSE312393 双计 13）→ 337 unique samples（去重后），L132 已补说明
  - 3 处 dataset n 值统一为表格值（GSE272133 52 / GSE32575 48 / GSE318937 119）
  - 104 shortlist = 94+12−2（2 个 NAMPT 变体 |delta|≥4 重叠）已验证并注明
  - GSE294150 未发表 → 正文注明按数据集引用（Data Availability）
  - 12 处缩写首现定义补齐（GWAS/eQTL/GTEx/TSS/MPRA/CRISPRi/DAMP/MoTrPAC/PBMC/GEO/OB/q）
  - 标点空格修正 3 处；Fig.4a 图注补 p 值；L96 措辞歧义修正
- **自动化收尾** ✅（2026-09-20 第二轮，用户指示"能完成的都完成"）：
  - 正文微调：缩写清单补 NAMPT/NAD 词源 + CI 定义；作者行 `\* ,` 空格修复（F10 通读 2 处微调）
  - **代码归档就绪**：新增 LICENSE(MIT) / requirements.txt / ARCHIVE_README.md / .zenodo.json / CITATION.cff（Zenodo 硬性要求）；README 对齐 21 个脚本 + 补环境/数据来源/复现/归档章节
  - **Reporting Summary 转填稿**：`submission_pack/reporting_summary_formatted.pdf`（2 页，可直接对照官方模板）
  - **投稿系统文本**：`submission_pack/submission_system_texts.md`（Title/Abstract/Keywords/分类/COI/贡献/Data-Code 字段复制粘贴）
  - **Cover letter** 补 transfer 意向句（NC→Comms Biol 顺延）
  - **zip 重建**：`NAMPT_manuscript_submission_pack_2026-09-20.zip`（56 条目，9 分类 + 09_Archive 归档件）
  - 待办清单更新：F1-F10 全部 ✅；D1/D2/E1 代理完成；剩余仅 A 核对 / B 归档 / C 上传 / D3 / E2-E6
- **首次上传支持** ✅（2026-09-20 第三轮，用户首次 GitHub/Zenodo）：
  - 安全复核：全仓密钥零泄漏（git grep 433 跟踪文件 0 命中；key_status.txt 仅 "set"；脚本仅读环境变量）；.gitignore 完备
  - 环境检查：git 2.54 已装；仓库内身份 yanji@local（需用户设全局真实邮箱）；gh CLI 未装（走浏览器授权）；无远程；33 commits；__pycache__ 已清
  - 新手操作指南：`submission_pack/GITHUB_ZENODO_FIRST_TIME_GUIDE.md`（0-5 步：注册→建空仓库→设身份推送→检查→Zenodo 关联发 release 拿 DOI→填回正文；含 FAQ）
  - 待办清单 v3：B1-B6 拆到按钮级；B6 完成后可交回代填 URL/DOI
  - zip 重建 57 条目
- **GitHub + Zenodo 归档完成** ✅（2026-09-21，用户操作 + 代理收尾）：
  - GitHub 仓库：https://github.com/ENSEI0713/nampt-axis-transcriptomics
  - Zenodo DOI：10.5281/zenodo.22865789（https://doi.org/10.5281/zenodo.22865789）
  - 正文 3 处占位已填（L185 计划措辞→已归档陈述；L193/L196 URL+DOI）；重跑自检：零占位、Title 8 / Abstract 141 / 引用 1→16 全部通过
  - 归档元数据同步：.zenodo.json 补 doi + related_identifiers；CITATION.cff 补 doi/url；ARCHIVE_README 补实际 DOI/URL；README git clone 用实际 URL
  - 新 zip：NAMPT_manuscript_submission_pack_2026-09-21.zip（57 条目；旧 09-20 版已删）
  - 待办清单 v4：B 组全部 ✅；剩余 A 核对 / C 上传 / D3 / E2-E6
- 可选：Evo2 全量强制重跑（约 30-60 分钟 API）、GTEx LD 代理把 C 类与常见变异连接

## 4. 关键论断边界（写作用红线）

- NAMPT mRNA ≠ eNAMPT 蛋白；当前全部为转录组证据
- eNAMPT 方向性 = 可检验预测（肥胖→炎症程序；训练→修复标志物），待蛋白/代谢物验证
- Evo2 只做候选优先级，不证明因果、不预测临床风险
- 小样本对照（n≤4）只作方向性证据
- 公共数据不可用于个体诊断或运动处方

## 5. 关键路径

```
scripts/build_variant_candidates.py → candidates_priority.csv (432)
scripts/build_ref_alt_windows.py   → windows.bed/fasta (432 对)
scripts/run_evo2_scoring.py        → scores.csv（Score A 432/432）+ scores_B.csv（短名单 104）
     ↓
scripts/merge_qtl_gwas.py          → tiers.csv（GTEx + GWAS Catalog 合并）
     ↓
evo2_variant_results_report.md（主图定案 NOT MAIN FIGURE）→ Figure 5 维持流程面板
```
