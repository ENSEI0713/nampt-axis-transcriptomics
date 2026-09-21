# ARCHIVE README — evo2-40b NAMPT-axis analysis

This archive accompanies the manuscript:

> **State-dependent NAMPT-axis transcriptional programs in obesity and exercise**
> Nature Communications (submitted); Yanjing Chen, Zhenyu Shao, Min Zhang, Yan Zhang.

## Contents
- `scripts/` — full analysis pipeline (21 Python scripts, 1 R fallback). See `README.md` for run order.
- `data_audit/outputs/` — all derived tables, figures and reports referenced by the manuscript.
- `data_audit/raw/` — raw API responses (GTEx eQTL, GWAS Catalog, Ensembl) archived for provenance.
- `data_audit/downloads/` — original GEO processed matrices (NOT redistributed; third-party data).

## Data sources
All input data are public third-party data:
- GEO: GSE312393, GSE305038, GSE292369, GSE318937, GSE32575, GSE272133, GSE294150, GSE282850
- GTEx (REST v2), GWAS Catalog (REST), Ensembl REST — download dates in `Supplementary Data 1`.
Original data remain under their accessions; this archive does not redistribute them.

## Reproduce
1. `pip install -r requirements.txt` (Python >= 3.10; tested on 3.14.5)
2. Follow the numbered pipeline in `README.md` (steps 1-15 + Evo2 scoring).
3. Evo2-40B scoring requires the NVIDIA-hosted generate endpoint; the API key is provided at runtime
   via the environment variable `NVIDIA_API_KEY` or `NVCF_RUN_KEY` (never committed).

## License
MIT (see LICENSE). The MIT license covers the analysis code; third-party data remain under their
original terms.

## Zenodo metadata

This archive is deposited at Zenodo: https://doi.org/10.5281/zenodo.22865789
GitHub repository: https://github.com/ENSEI0713/nampt-axis-transcriptomics
Citation metadata: see `.zenodo.json` and `CITATION.cff`.
