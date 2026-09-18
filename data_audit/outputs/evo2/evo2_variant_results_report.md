# Evo2-40B variant module status and main-figure gate assessment

Generated: 2026-09-18

## 1. Current pipeline status

| Stage | Status | Artifact |
| --- | --- | --- |
| Candidate variant build (Ensembl REST) | ✅ done | `candidates.csv` (12,961 raw) → `candidates_priority.csv` (432 functional) |
| GRCh38 ref/alt windows (2 kb) | ✅ done | `windows.bed` (432), `windows.fasta` (864 seqs, ref+alt) |
| Ref/alt integrity check | ✅ done | 430/432 single-base SNP; 2 indels (correctly built as del/ins); 0 skipped ref mismatches |
| Evo2 scoring script | ✅ written, key-gated | `scripts/run_evo2_scoring.py` (Score A allele surprisal, resume-safe, secret-safe) |
| Actual Evo2 scores | ⛔ not run | `scores.csv` / `scoring_log.jsonl` pending `NVIDIA_API_KEY` |

## 2. Candidate composition

| gene_window | priority variants | notes |
| --- | --- | --- |
| NAMPT | 12 | all retained (deep coverage of focal gene) |
| CD38 | 60 | capped |
| BST1 | 60 | capped |
| SIRT1 | 60 | includes 2 indels (inframe del/ins) |
| SIRT3 | 60 | capped |
| SIRT6 | 60 | capped |
| IL6 | 60 | capped |
| TNF | 60 | capped |
| **Total** | **432** | priority subset, ~864 API calls for full Score A |

Functional annotations present: missense, splice_region, 5'UTR, TF_binding_site,
regulatory_region, plus 130 ClinVar-annotated variants.

## 3. Main-figure gate (per evo2_regulatory_variant_protocol.md §11)

To be a MAIN FIGURE, the analysis must deliver a compact set of variants that
satisfy ALL of:

- [x] linked to NAMPT or another high-priority NAMPT-axis gene (all 432)
- [x] located in a relevant skeletal muscle / adipose / immune regulatory
      element — promoter-proximal windows (±2 kb of TSS) with functional
      consequence annotation
- [x] supported by at least one public QTL or GWAS source —
      **NOT YET DONE**: candidates come from dbSNP/Ensembl; eQTL/GWAS
      intersection (GTEx/OpenGWAS) is a remaining step
- [ ] stable ref/alt Evo2 perturbation score — **PENDING key + run**
- [x] connects to a gene whose expression belongs to the inflammatory or
      repair axis in the public transcriptomic analysis (all candidate genes
      are axis genes with measured expression)

**Verdict (current): NOT DECIDED.** The pipeline is fully built and the
candidate set is well-formed; the decision between main figure and
supplementary figure hinges on (a) whether Evo2 scores come out stable, and
(b) whether eQTL/GWAS support can be merged. Both are actionable next steps
once the API key is configured.

## 4. Remaining work for the gate to resolve

1. Configure `NVIDIA_API_KEY` (user side, `setx NVIDIA_API_KEY <key>` +
   terminal restart). Do NOT paste the key into the chat.
2. Run `python scripts/run_evo2_scoring.py --limit 20` as a pilot, then
   batch the full 432.
3. Score B (pseudo-likelihood) and Score C (perturbation stability) for the
   top candidates only.
4. Merge eQTL (GTEx/eQTL Catalogue) and GWAS (OpenGWAS/FinnGen) evidence for
   the scored set → Tier A/B/C assignment.

## 5. Interpretation boundary (unchanged)

Evo2 scores support regulatory hypotheses. They do not establish eNAMPT
protein secretion, clinical inflammatory status, exercise safety, causal
disease risk, or personalized exercise prescription.
