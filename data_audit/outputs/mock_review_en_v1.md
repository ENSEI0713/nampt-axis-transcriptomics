# 模拟审稿复检（EN 全文，2026-09-20）— 投稿 Nature Communications / Genome Biology 前

> 3 路模拟审稿（统计/方法学、概念新颖性、跨学科可读性），基于完整英文稿 `manuscript_full_en_v1.md`。
> 状态：blocking 项已于同日修复（commit 7d02325 + 后续引用编号）；major/minor 待处理清单见下。

## 一、Blocking（已修复 ✅）

| # | 问题 | 修复 |
| --- | --- | --- |
| B1 | 全文 20+ 处 backtick 文件路径（`.csv/.md/.py` 等），工作稿痕迹 | ✅ 已清除，改为 Supplementary Data 1-8 引用 + 归档说明 |
| B2 | 审稿代号残留（CB-1/2/4/5、R1-M5、R1-M7） | ✅ 已全部删除，实质内容改为自然语言陈述 |
| B3 | 占位符（作者单位/邮箱 to be completed、期刊 target under decision、references TODO） | ✅ 作者块已填（单位 4 条 + 两邮箱）；期刊说明已规范；references TODO 已清 |
| B4 | 章节顺序错误（Results→Methods→Discussion） | ✅ 已重排为 Abstract→Intro→Results→Discussion→Methods→Data/Code→References→End Notes |
| B5 | Abstract 超 150 词（审稿估 ~210） | ✅ 实测 143 词（上轮已压），结构合规 |
| B6 | 缺 Data/Code Availability、References、End Notes | ✅ 已补四节；References 编号制 1-16；End Notes 含三声明 |

## 二、Major（已处理/待处理）

| # | 问题 | 状态 |
| --- | --- | --- |
| M1 | "Methodological honesty as a strength" 自我辩护式措辞 | ⚠ 待处理：改为中立陈述（Limitations 内保留实质，删自夸标题） |
| M2 | "honest result"、"empirically degenerate"、"needs caution" 等过度防御 | ⚠ 部分已随 B 项清理；剩余可在语言润色时收敛 |
| M3 | "worded as fragility in Results" 元操作描述 | ✅ 已删（B 项清理顺带） |
| M4 | 引用未编号 | ✅ 已编号（[1]-[16] 插入正文，References 对应） |
| M5 | 缩写未定义（MICE/SIE/LODO/T2D/GRCh38） | ⚠ 待处理：Methods 首次出现处补全称 |
| M6 | 图/表引用无正式编号（无 "Figure 1-5"、"Supplementary Fig." 交叉引用） | ⚠ 待处理：正文补图交叉引用 + 图注（见 reporting_checklist.md） |

## 三、Minor（待处理）

- m1: Results 加粗小标题（Problem/Approach/Claim/Findings）——Nature 家族偏好自然段落，可保留但需统一
- m2: em dash 使用偏多（统计区间除外）——语言润色时收敛
- m3: 防御性碎片（caution/honest 等）分散——合并降低紧张度
- m4: 9 units vs 4 cohorts 口径一致性——已在 Methods 统一

## 四、新颖性审稿要点（供投稿信使用）

- 核心卖点：状态依赖的 NAMPT 轴转录程序模型，用跨 9 数据集的证据梯解释 eNAMPT 文献矛盾
- 边界纪律（mRNA≠eNAMPT、Evo2 非因果、Tier A/B=0 如实披露）是审稿认可的优点
- 投稿 NC/GB 的强化点：投稿信强调"概念框架 + 公共数据证据梯 + 完全可复现 + 边界诚实"；
  纯公共数据计算论文在两刊有先例，但需把"为什么没有实验验证"转化为"后续验证路径清晰"
- 不做湿实验（用户决策）：本篇作为研究基石，配综述 + meta 分析形成系列

## 五、投稿前剩余动作（见 reporting_checklist.md 详表）

1. M1/M5/M6 + minor 语言润色（全文过一遍）
2. 4 条 GEO 文献第一作者/卷期页核验（GSE292369/312393/318937/282850）
3. 图注 6 张 + 正文图交叉引用
4. Supplementary Data 1-8 实际文件
5. Reporting Summary 正式模板 + Cover letter
6. Title 定稿（≤15 词）+ 期刊（NC/GB）最终确认
