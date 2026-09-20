# 目标期刊评估：顶刊定位（2026-09-20，用户指示更新版）

> 用户指示（2026-09-20）：目标期刊 = Nature 这种级别的顶刊，或能力范围内能达到的最顶期刊。
> 本文件在 `manuscript_logic_v1_zh.md` §10 原始评估基础上，按"能力范围内最顶"重新评估，
> 给出分档投稿策略与前提条件。

## 1. 现状一句话

论文是一篇**纯公共数据 + 计算**的转录组/序列模型分析（无新增实验），核心贡献 = 状态依赖的
NAMPT 轴转录程序模型 + 跨 9 数据集证据梯 + Evo2 候选优先级（Tier A/B=0 如实披露）。

## 2. 分档目标与真实门槛

| 档位 | 期刊 | 门槛（真实） | 本稿现状 | 差距 |
| --- | --- | --- | --- | --- |
| **T0 主刊** | Nature / Science / Cell | 决定性概念推进 + 闭合证据链 + 通常伴随强机制或大规模验证 | 概念框架有意义，但**无实验验证、无蛋白/代谢物、无前瞻队列** | 大：logic §10 已列 5 类决定性证据，一类都没有 |
| **T1 顶刊子刊** | Nature Metabolism / Nature Medicine / Nature Communications | 显著推进领域理解；代谢机制深度；可含纯计算/公共数据分析，但需机制性或大规模验证 | 与 Nat Metab 范围吻合（代谢×运动×免疫），但机制深度不足 | 中：缺蛋白/代谢物/机制实验 |
| **T2 计算/专刊** | Genome Biology / npj Syst Biol Appl / Bioinformatics / CSBJ / iScience | 计算方法或概念框架新颖、可复现、证据梯完整 | 概念框架 + 证据梯 + Evo2 管线完整，**能力范围内最匹配** | 小 |
| **T3 学科刊** | 代谢/运动医学专刊 | 领域相关、证据扎实 | 完全满足 | 无 |

## 3. 关键判断

- **直冲 T0（Nature 主刊）在无新实验前提下风险极高**——logic §10 与投稿前模拟审稿均指向这一点；
  审稿人会问：为什么没有蛋白/代谢物验证？没有实验验证 Evo2 候选？样本量仅 337、肥胖层 k=3？
- **"能力范围内最顶"的现实解是 T1 与 T2 之间**：
  - 若维持现稿（无新实验），**T2 头部（如 Genome Biology、npj Syst Biol Appl）是最顶可达目标**，
    T1（Nat Metab/Nat Commun）需在投稿信中把"概念框架 + 证据梯 + 边界纪律"讲足，仍有相当被拒风险；
  - 若要够 T1（Nat Metab），最低成本加码是**补 1-2 个蛋白/代谢物公共数据验证**（如 MoTrPAC 人类数据
    的 eNAMPT/NAD 分析物，logic §10 已列）或**对 1-3 个 Evo2 Tier C 候选做实验验证**（MPRA/CRISPRi）——
    这些是 T0/T1 与 T2 之间的分水岭。
- **Tier A/B=0 与负结果是诚实的优点**（审稿共识），但不是顶刊加分项；顶刊要的是"新机制或大规模验证"。

## 4. 建议投稿路径（能力范围内最顶，按优先级）

1. **首选冲刺档（维持现稿，零新增成本）**：先投 **T1 的 Nature Communications**（接受面最宽、
   纯计算/公共数据论文有先例）或 **Genome Biology**（计算基因组旗舰）。若被拒，转投
   **npj Systems Biology and Applications** / **iScience** / **CSBJ**（T2 中影响因子与定位最合适）。
   - 理由：与其一次冲 Nature 主刊被秒拒再层层下放，不如从"最顶的合理接收面"开始，
     投稿信强调概念框架 + 证据梯 + 边界纪律。
2. **加码升级档（若愿意补证据）**：补 MoTrPAC 人类 eNAMPT/NAD 蛋白代谢物验证 或
   Evo2 Tier C 候选的 MPRA/CRISPRi 实验 → 可够 **Nature Metabolism** / **Nature Medicine** 的
   "机制深度"门槛，显著提升 T1 命中率。
3. **稳妥保底档**：若时间/资源受限，**Communications Biology**（原默认）仍为稳妥选择，
   但按用户指示优先级降为保底。

## 5. 与已做工作的关系

- 本评估不改变稿件内容与边界（内容层 90% 完成，投稿就绪层待办不变：编号制文献、Title、Data/Code
  Availability、END NOTES、Reporting Checklist、模拟审稿）。
- 期刊格式核对（`commbiol_format_check.md`）基于 Comm Biol；若改投 T1/T2 其他期刊，格式要求
  （Abstract 字数、参考文献制式、显示项限制）需按目标期刊重核——但**初投多期刊均不强制格式**，
  不阻塞内容定稿。
- Title 占位（顶刊偏好，陈述式 ≤15 词候选）已提供，全文完成后润色。

## 6. 下一步（需要用户拍板）

- [ ] A. 是否加码补证据（MoTrPAC 蛋白/代谢物验证 或 MPRA/CRISPRi 实验）→ 决定能否够 T1；
- [ ] B. 若不加码：确认先投 Nature Communications 还是 Genome Biology（或维持 Comm Biol 保底）；
- [ ] C. 作者单位/邮箱信息补齐（EN 稿作者块已留占位）。

*2026-09-20 更新。依据：Nature Metabolism Aims & Scope 官方页、logic §10、投稿前模拟审稿综合。*
