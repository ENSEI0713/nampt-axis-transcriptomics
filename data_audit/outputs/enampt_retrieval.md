# eNAMPT / NAD protein-metabolite public evidence: retrieval record

Generated: 2026-09-18

## 1. Objective

Determine whether public, downloadable protein (eNAMPT/visfatin) and
metabolite (NAD / NMN / NR / NAM / tryptophan-kynurenine) data exist for
exercise / obesity / weight-loss studies. This decides whether eNAMPT can
enter the core paper claims or must be demoted to a stated hypothesis.

## 2. What was probed (real API calls, 2026-09-18)

| Source | Endpoint / method | Result |
| --- | --- | --- |
| MetaboLights | `GET /ws/studies?size=100&page=N` | ✅ works; 20,526 studies listed |
| MetaboLights | `GET /ws/studies?query=<term>` | ⚠️ query ignored — always returns same total (3,421 sample); term filtering NOT functional on this endpoint |
| MetaboLights | `GET /ws/studies/search?query=` (3 path variants) | ❌ 400 / 404 |
| MetaboLights | `GET /ws/studies/MTBLS1` (detail) | ✅ works; nested `mtblsStudy`/`isaInvestigation`/`validation` |
| PRIDE Archive | `GET /pride/ws/archive/v2/projects/` | ❌ 404 (endpoint path wrong for current API) |
| PRIDE Archive | (no working endpoint confirmed this run) | ⚠️ needs endpoint discovery (e.g. `/pride/ws/archive/v2/projects` with different base) |
| NCBI dbSNP eutils | esearch/esummary | ✅ works (used for variant candidates) |
| Ensembl REST | overlap / sequence | ✅ works (used for variant candidates) |
| GWAS Catalog REST | `/gwas/rest/api/...` region/SNP endpoints | ❌ 404 (REST path changed) |

## 3. Preliminary availability judgement

- **Metabolite (NAD/NMN/NR/NAM) studies**: MetaboLights hosts large numbers
  of metabolomics studies, and NAD-related studies do exist in the
  literature (NMN/NR supplementation trials), but the current API cannot
  be filtered by keyword programmatically. Manual web search
  (https://www.ebi.ac.uk/metabolights/) with terms like "nicotinamide",
  "NAD+", "NMN" is required to identify downloadable matched studies.
- **Protein (eNAMPT/visfatin) studies**: PRIDE holds proteomics datasets
  but the probed endpoint failed; Olink/aptamer studies are usually
  supplementary to clinical papers and rarely deposited as raw
  downloadable matrices.
- **Pairing with exercise/obesity phenotype**: the scarce part is
  studies that simultaneously provide plasma/serum NAMPT or NAD
  metabolites AND exercise/obesity contrasts with public downloads.

## 4. Decision (Step 15)

Based on this probe and the earlier feasibility report (which already
flagged this risk), the honest decision is:

**eNAMPT / NAD metabolite claims are DEMOTED to a stated hypothesis in the
current paper.** The core paper will:

1. State explicitly: "NAMPT mRNA state changes are transcriptomic
   evidence; they are not extracellular NAMPT protein or NAD abundance."
2. Frame eNAMPT directionality as a *testable prediction* from the axis
   model, with the specific prediction that plasma eNAMPT would follow
   the inflammatory program in obesity and follow repair markers after
   training — pending protein/metabolite validation.
3. NOT claim any clinical biomarker performance for NAMPT mRNA.
4. Keep a supplementary "evidence gap" note listing the exact public
   resources to mine later (MetaboLights manual search; PRIDE once its
   current API is mapped; Olink/aptamer study supplements; MoTrPAC).

This keeps the manuscript defensible without inventing data that the
public archives do not (yet) expose programmatically.

## 5. Open follow-up (if eNAMPT evidence is wanted for a stronger paper)

- Manual web review of MetaboLights for NMN/NR/serum-NAD studies with
  exercise or obesity cohorts (~half-day human work).
- PRIDE API v2 endpoint discovery via its Swagger/OpenAPI page, then
  search "visfatin", "NAMPT", "NAD" + exercise/obesity.
- MoTrPAC (multi-omics exercise atlas) release includes proteomics and
  metabolomics — check current public release coverage for plasma NAD
  pathway analytes.
