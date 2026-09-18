# evo2-40b — NAMPT-NAD 炎症-修复轴公共数据研究

## 一句话

用公共人类多组学（GEO 表达矩阵）与 Evo2-40B 序列模型，解析肥胖和运动适应中**状态依赖的 NAMPT-NAD 炎症-修复轴**：慢性代谢压力下偏向炎症负荷，运动/训练背景下偏向 NAD 代谢与适应性修复。

## 目录结构

```
evo2-40b/
├── scripts/                    # 分析管线（按运行顺序编号见下）
│   ├── public_data_audit.py        # (1) 公共数据库审计与候选筛选
│   ├── download_geo_processed.py   # (2) 下载精选 GEO 处理矩阵
│   ├── profile_geo_processed.py    # (3) 矩阵可用性 profile
│   ├── extract_geo_metadata.py     # (4) 提取 GEO 元数据
│   ├── extract_geo_sample_table.py # (5) 样本级元数据表
│   ├── build_nampt_axis_scores.py  # (6) NAMPT 轴基因集 + 评分
│   ├── formal_nampt_axis_statistics.py   # (7) Phase 1 正式统计（19 对照）
│   ├── phase1b_nampt_axis_sensitivity.py # (8) Phase 1b 敏感性分析
│   ├── plot_nampt_axis_figures_py.py     # (9) Figure 2-4 渲染
│   ├── plot_nampt_axis_figures.R         # R 版渲染（备用）
│   ├── meta_nampt_axis.py           # (10) 随机效应 meta 分析（新）
│   ├── axis_structure_analysis.py   # (11) 模块一致性/alpha（新）
│   ├── cell_composition_sensitivity.py # (12) 细胞组成校正（新）
│   ├── build_variant_candidates.py  # (13) Evo2 候选变异表（新）
│   ├── build_ref_alt_windows.py     # (14) GRCh38 ref/alt 窗口（新）
│   └── run_evo2_scoring.py          # (15) Evo2 打分（新，需密钥）
├── data_audit/
│   ├── downloads/              # 原始下载（.gitignore 排除，不入库）
│   ├── raw/                    # 检索原始 XML/JSON 存档
│   └── outputs/                # 全部处理结果与报告
│       ├── meta/               # 随机效应 meta 结果（新）
│       ├── axis_structure/     # 模块结构分析（新）
│       ├── cell_composition/   # 细胞组成敏感性（新）
│       ├── evo2/               # Evo2 候选与打分（新）
│       └── figures_phase2/     # 论文图件
└── README.md
```

## 运行顺序

```
public_data_audit → download_geo_processed → profile_geo_processed
→ extract_geo_metadata → extract_geo_sample_table
→ build_nampt_axis_scores → formal_nampt_axis_statistics → phase1b_nampt_axis_sensitivity
→ plot_nampt_axis_figures_py
→ meta_nampt_axis → axis_structure_analysis → cell_composition_sensitivity
→ build_variant_candidates → build_ref_alt_windows → run_evo2_scoring（需 NVIDIA_API_KEY）
```

## Evo2 密钥

API key 只通过环境变量 `NVIDIA_API_KEY` 或 `NVCF_RUN_KEY` 提供（Windows: `setx NVIDIA_API_KEY <key>` 后重启终端）。密钥绝不写入脚本、日志或文档。

## 关键结论边界

- NAMPT mRNA ≠ eNAMPT 蛋白；公共表达数据不构成个体诊断或运动处方依据
- Evo2 只做调控变异候选优先级，不证明因果，不预测临床风险
- 小样本对照（n≤4）只作方向性证据
