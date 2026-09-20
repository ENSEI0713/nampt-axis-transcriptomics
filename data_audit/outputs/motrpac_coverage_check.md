# MoTrPAC 蛋白/代谢组覆盖检查（eNAMPT 升核心结论的可行性评估）

Generated: 2026-09-19
前置：`enampt_retrieval.md`（2026-09-18）已将 eNAMPT/NAD 代谢物主张降级为可检验预测。
本记录回答：MoTrPAC 公共释放是否足以把 eNAMPT 升回核心结论。

## 1. 检查内容（真实网络探测，2026-09-19）

| 探测项 | 端点 | 结果 |
| --- | --- | --- |
| MoTrPAC 官方门户 | `https://motrpac-data.org/` | ✅ 200，SPA（HTML 壳） |
| 门户数据 API | `/api`、`/api/v1`、`/api/v2`、`/api/v2/datasets`、`/api/v2/studies` | ❌ 404（路径未公开） |
| 门户 GraphQL | `/graphql` | ⚠️ 返回 HTML 壳，非可程序化端点 |
| GEO 检索 `MoTrPAC[Title]` | NCBI eutils esearch/esummary | 仅 4 条，全部为大鼠耐力训练（RNA-seq/ATAC-seq/RRBS） |
| MoTrPAC 论文元数据 | Crossref API | 命中 MCP 2022 多组学论文（10.1016/j.mcpro.2022.100313）；人类主论文数据在 dbGaP phs002292（受控） |
| MoTrPAC 代谢组数据仓库 | Zenodo 记录 8805040（试） | ❌ 404（记录号不确定） |

## 2. 事实判定

1. **MoTrPAC 确实测量了蛋白组与代谢组**（论文与中间释放证实，多组织：骨骼肌/脂肪/血液等），这是公开文献级事实。
2. **但人类受试者原始数据为 dbGaP phs002292 受控访问**；门户公共释放为去标识化汇总，可程序化端点未公开（本轮探测的 API/GraphQL 均不可用）。
3. **代谢组分析物清单是否覆盖 NAD/NMN/NR/NAM 通路**：本轮无法经 API 验证，需人工审阅补充材料（约半日人工作，与 `enampt_retrieval.md` §5 的 MetaboLights 人工检索同级别成本）。
4. **即便有 NAD 通路代谢物**，MoTrPAC 的对比主要是"训练前后/不同训练剂量"，与本研究需要的"运动×肥胖/代谢病状态"对比并不对齐；eNAMPT 蛋白（分泌型）在 MoTrPAC 血浆蛋白组中的覆盖也需人工确认。

## 3. 结论（保持降级）

**MoTrPAC 覆盖检查不改变既有决策：eNAMPT/NAD 代谢物主张继续保持在"可检验预测"层级，不升回核心结论。**

理由（如实）：
- 人类数据受控访问，公共可程序化获取的证据不足以支撑论文级 eNAMPT/NAD 主张；
- NAD 通路分析物覆盖与"运动×肥胖"配对对比均未经人工核验，不能假设存在；
- 论文现有立场（"NAMPT mRNA ≠ eNAMPT 蛋白；eNAMPT 方向性 = 待验证预测"）在证据上仍是防御最稳的表述。

## 4. 若未来要升回（触发条件，均需人工）

- 人工审 MoTrPAC 人类蛋白组/代谢组分析物清单，确认 NAD 通路（NAD/NAMN/NMN/NR/NAM）被检测；
- 确认有可公开下载的"运动×代谢状态"配对数据或已发表汇总可引用；
- 或经 dbGaP 申请（phs002292）获得人类受控数据后自行分析（超出公共数据研究范围）。

## 5. 论文落点

- 保持 `manuscript_results_v2_zh.md` 论断边界：eNAMPT 方向性为可检验预测；
- 补充材料"evidence gap"清单已含 MoTrPAC（`enampt_retrieval.md` §4），本记录作为其具体化附录。
