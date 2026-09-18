# PROGRESS — NAMPT-NAD 炎症-修复轴项目接续索引

> 最后更新：2026-09-18 05:17 UTC+8
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

### Phase C Evo2 管线（全部就绪，分数待跑）
- `scripts/build_variant_candidates.py`（Ensembl REST）：12,961 原始 → **432 优先级功能候选** `data_audit/outputs/evo2/candidates_priority.csv`
- `scripts/build_ref_alt_windows.py`：GRCh38 ref/alt 2kb 窗口 **432 对**（430 SNP + 2 indel，0 条 ref 不匹配）→ `windows.bed` / `windows.fasta`
- `scripts/run_evo2_scoring.py`：Score A allele surprisal，密钥门控、断点续跑、日志脱敏，**语法已验证**
- 门槛报告：`data_audit/outputs/evo2/evo2_variant_results_report.md`（主图/补充图未决）

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

### P0 Evo2 实际打分（唯一硬阻塞：NVIDIA_API_KEY 未在当前进程生效）
1. 用户已执行 `setx NVIDIA_API_KEY "..."`（PowerShell 确认保存）——但 setx 只影响**新建进程**，当前已打开的进程读不到
2. **必须完全退出 EvoX 桌面应用再重新打开**（不是开新对话，是重启进程）
3. 新会话中先验证：`python -c "import os; print('set' if os.environ.get('NVIDIA_API_KEY') else 'not set')"`（只输出布尔，绝不打印密钥）
4. 确认后跑 pilot：`python scripts/run_evo2_scoring.py --limit 20`
5. pilot 通过后批量：`python scripts/run_evo2_scoring.py --limit 0`（跑全部 432）
6. top 候选跑 Score B（pseudo-likelihood）与 Score C（扰动稳定性）——脚本待扩展
7. 合并 eQTL（GTEx/eQTL Catalogue）+ GWAS（OpenGWAS/FinnGen）→ Tier A/B/C 分层
8. 更新 `evo2_variant_results_report.md`，判定主图/补充图

### P1 论文推进
- 写 Introduction / Abstract / Title（Results 已有 v2 草案）
- 用 ccf-humanization + ccf-paper-writer 技能打磨 Results
- MoTrPAC 公共释放的蛋白/代谢组覆盖检查（若 eNAMPT 要升回核心结论）

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
scripts/run_evo2_scoring.py        → scores.csv（待跑，密钥门控）
     ↓ 密钥就绪后
scores.csv → Tier A/B/C → evo2_variant_results_report.md → Figure 5 更新
```
