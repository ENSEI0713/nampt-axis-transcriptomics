# PROGRESS — NAMPT-NAD 炎症-修复轴项目接续索引

> 最后更新：2026-09-20 10:58 UTC+8
> 用途：本文件是任何新对话接续本项目的唯一索引。新对话先读本文件，再按需读列出的产物。

## 1. 项目是什么

用公共人类多组学（GEO 表达矩阵）与 Evo2-40B 序列模型，解析肥胖和运动适应中**状态依赖的 NAMPT-NAD 炎症-修复轴**：慢性代谢压力下 NAMPT 更接近免疫/脂肪炎症负荷，运动/训练背景下转向 NAD 代谢与适应性修复。论文主轴单一：NAMPT-NAD 炎症-修复轴的状态依赖性。

## 2. 已完成（git 提交 018c0f1 → e241d5f，共 15 次，工作区干净）

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
  - 明确不是细胞去卷积；炎症分数与轴内单核/巨噬基因高相关（r=0.7–0.9）→ 独立印证 Phase 1b"NF-κB 驱动急性炎症信号"
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
