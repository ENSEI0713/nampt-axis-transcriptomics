# Reporting Summary（投稿用草稿 — 转填 Nature Portfolio 官方 PDF 模板）

## Life Sciences Reporting Summary

### 1. Data & Materials
- **Data sources**: 8 GEO accessions, 9 transcriptomic units, 337 samples (GSE312393, GSE305038, GSE292369, GSE318937, GSE32575, GSE272133, GSE294150, GSE282850). All public, processed matrices downloaded from GEO.
- **Primary data**: Not applicable — secondary analysis of public transcriptomic data; no new primary data generated.
- **Data availability statement**: Provided in manuscript (Data Availability section).
- **Code availability statement**: Provided (Code Availability section; repository URL and Zenodo DOI to be assigned upon archiving).
- **Supplementary data**: Supplementary Data 1–8 (xlsx), packaged in submission_pack/.

### 2. Experimental Models & Statistics
- **Samples**: Human-derived transcriptomic matrices (skeletal muscle, adipose, CD14+ monocytes, whole blood-derived cells, LHCN-M2 human muscle cells). No animals.
- **Sample size**: 337 samples across 9 units; per-dataset sizes listed in Methods Table 1.
- **Inclusion/exclusion**: Predefined in Methods §1.1.
- **Randomization / blinding**: Not applicable — public data secondary analysis; no intervention allocation.
- **Replication**: Cross-dataset evidence ladder (9 units, 4 exercise cohorts); leave-one-dataset-out sensitivity.
- **Statistical methods**: DerSimonian–Laird random-effects meta-analysis; Benjamini–Hochberg FDR (q values); Cronbach's α internal consistency; Pearson/Spearman correlations; cluster-aware dataset-level estimation.
- **Multiple comparisons**: BH-FDR per comparison family; α index distinguished from significance α.
- **Software versions**: Python 3.14.5, NumPy 2.4.6, SciPy 1.18.0.

### 3. Statistics for specific analyses
- R1 module consistency: Cronbach α — done
- R2 exercise meta: DL random effects + dataset-level + LODO — done
- R2 immune-load correlation: Pearson/Spearman r (all samples) — done (FDR boundary noted; confirm at submission)
- R3 obesity layer: k=3 directional — done
- R4 cell model: k=2 directional — done
- R5 Evo2: Score A/B/C + Tier stratification — done

### 4. Editorial policy
- **Competing interests**: none declared (End Notes).
- **Author contributions**: provided (End Notes).
- **Ethics/consent**: Not applicable — public-data secondary analysis; no human/animal experiments, no ethical approval required (statement in Methods §1).
- **Figure legends**: 6 figures, complete legends in Figure Legends section; display items ≤10 each.
- **Title**: 8 words (≤15). **Abstract**: 141 words (≤150, no references).

---
*Draft v1 — 2026-09-20. To be transcribed into the official Nature Portfolio Reporting Summary PDF template.*
