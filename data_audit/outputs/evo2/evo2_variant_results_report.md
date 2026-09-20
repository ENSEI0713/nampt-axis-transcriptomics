# Evo2-40B variant module status and main-figure gate assessment

Generated: 2026-09-18
Last scoring run: 2026-09-18 (Score A allele surprisal, flank = 200 bp)

## 1. Current pipeline status

| Stage | Status | Artifact |
| --- | --- | --- |
| Candidate variant build (Ensembl REST) | ✅ done | `candidates.csv` (12,961 raw) → `candidates_priority.csv` (432 functional) |
| GRCh38 ref/alt windows (2 kb) | ✅ done | `windows.bed` (432), `windows.fasta` (864 seqs, ref+alt) |
| Ref/alt integrity check | ✅ done | 430/432 single-base SNP; 2 indels (correctly built as del/ins); 0 skipped ref mismatches |
| Evo2 scoring script | ✅ run | `scripts/run_evo2_scoring.py` (Score A allele surprisal, resume-safe, secret-safe) |
| Actual Evo2 Score A | ✅ complete | `scores.csv` (432 unique rsids) / `scoring_log.jsonl` (432 lines, no secrets) |
| Score B / Score C | ⚠️ C degenerate / B running | `scores_B.csv` (mode B, shortlist 104); C: pilot 10×5 seeds all sd=0 (see §6) |
| eQTL + GWAS merge | ⛔ not run | GTEx / eQTL Catalogue / OpenGWAS / FinnGen still required for Tier A/B/C |

## 2. Score A run log

- Pilot `--limit 20` succeeded after one code fix: BED `start` is a string; `position` now uses `int(variant["start"]) + offset`.
- Full batch `--limit 0 --resume` scored the remaining 412 variants with 0 HTTP/API errors.
- Completeness: 432/432 candidates scored; 432 unique rsids; 0 missing; 0 duplicates.
- Endpoint: NVIDIA hosted Evo2-40B generate (`enable_logits=true`, 1 generated token).
- Metric: `delta_surprisal = log P(alt) − log P(ref)` on DNA-normalized A/C/G/T softmax. Sign is **not** interpreted as beneficial or harmful.

## 3. Candidate composition (unchanged)

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
| **Total** | **432** | Score A complete (one generate call per variant) |

Functional annotations present: missense, splice_region, 5'UTR, TF_binding_site,
regulatory_region, plus 130 ClinVar-annotated variants.

## 4. Score A distribution

| statistic | value |
| --- | --- |
| n | 432 |
| delta min / max | −8.844 / +3.432 |
| delta mean / median | −1.665 / −0.805 |
| \|delta\| mean / median | 2.033 / 1.118 |
| n(delta > 0) / n(< 0) / n(= 0) | 128 / 300 / 4 |
| n(\|delta\| ≥ 1 / 2 / 3 / 4 / 5) | 220 / 174 / 136 / 94 / 43 |

Negative deltas dominate: the model more often assigns higher probability to the reference base than to the alternate base. That is expected for a reference-trained genomic LM and is **not** a pathogenicity call.

### 4.1 By gene window

| gene | n | \|delta\| median | n(\|delta\| ≥ 2) | n(\|delta\| ≥ 4) |
| --- | ---: | ---: | ---: | ---: |
| IL6 | 60 | 4.091 | 45 | 35 |
| SIRT1 | 60 | 3.389 | 40 | 26 |
| TNF | 60 | 3.273 | 41 | 23 |
| NAMPT | 12 | 0.494 | 5 | 2 |
| SIRT6 | 60 | 0.508 | 14 | 4 |
| BST1 | 60 | 0.503 | 16 | 3 |
| SIRT3 | 60 | 0.583 | 1 | 0 |
| CD38 | 60 | 0.454 | 12 | 1 |

High-|delta| mass concentrates in **IL6 / SIRT1 / TNF**. This is a scoring observation, not evidence that those loci are more biologically causal. Local sequence entropy, GC, and window composition can drive the same pattern. Score B/C and eQTL/GWAS intersection are required before ranking genes.

### 4.2 Largest \|delta\| (top 10)

| gene | rsid | delta | p_ref | p_alt | consequence | ClinVar |
| --- | --- | ---: | ---: | ---: | --- | --- |
| SIRT1 | rs1450691401 | −8.844 | 0.998 | 0.00014 | missense | uncertain significance |
| SIRT1 | rs531048058 | −8.031 | 0.997 | 0.00032 | missense | uncertain significance |
| TNF | rs1770982841 | −7.828 | 0.999 | 0.00040 | missense | — |
| TNF | rs1770989222 | −7.797 | 0.998 | 0.00041 | missense | — |
| IL6 | rs1372637551 | −7.594 | 0.999 | 0.00050 | missense | — |
| IL6 | rs749300991 | −7.586 | 0.998 | 0.00051 | missense | — |
| SIRT1 | rs1405762679 | −7.500 | 0.999 | 0.00055 | synonymous | likely benign |
| IL6 | rs755658631 | −7.312 | 0.992 | 0.00066 | missense | — |
| SIRT1 | rs1466187737 | −6.930 | 0.997 | 0.00098 | missense | uncertain significance |
| SIRT1 | rs1471411863 | −6.914 | 0.997 | 0.00099 | synonymous | likely benign |

Largest **positive** deltas (alt more expected than ref): IL6 `rs867032078` / `rs1784026797` / `rs1784027001` (+3.432), SIRT1 `rs1406007212` (+3.248), NAMPT `rs1306770923` (+3.039).

Note: several extreme negative scores have p_ref ≈ 1 and p_alt ≈ 0, and at least two of the top-10 are synonymous / likely benign. Extreme |delta| is therefore **not** a clinical-severity proxy. Treat the tail as a shortlist for Score B/C, not as a result.

## 5. Main-figure gate (per evo2_regulatory_variant_protocol.md §11)

To be a MAIN FIGURE, the analysis must deliver a compact set of variants that
satisfy ALL of:

- [x] linked to NAMPT or another high-priority NAMPT-axis gene (all 432)
- [x] located in a relevant skeletal muscle / adipose / immune regulatory
      element — promoter-proximal windows (±2 kb of TSS) with functional
      consequence annotation
- [x] supported by at least one public QTL or GWAS source —
      **merged (GTEx + GWAS Catalog, §8)**; 9 External-only variants have
      strong support, but **none overlap with Evo2-perturbing candidates**
      (Tier A/B = 0)
- [x] stable ref/alt Evo2 perturbation score — **Score A + Score B complete**;
      Score C degenerate (deterministic endpoint, §6); strand consistency 65%
- [x] connects to a gene whose expression belongs to the inflammatory or
      repair axis in the public transcriptomic analysis (all candidate genes
      are axis genes with measured expression)

**Verdict (current): NOT A MAIN FIGURE — resolved.** Score A and Score B are
in hand; Score C is empirically degenerate (deterministic endpoint). eQTL +
GWAS merge is done (§8): **Tier A/B = 0** because Evo2-perturbing candidates
are rare variants with no public QTL/GWAS support, while the common loci with
strong support have mild Evo2 signal. The §11 criterion "stable Evo2
perturbation supported by at least one public QTL or GWAS source" is unmet
for every variant. Figure 5 stays a **pipeline + composition** panel; a
scored-variant panel belongs in a supplement, not the main claim.

## 6. Score C (perturbation stability): empirically degenerate on this endpoint

Per protocol §7, Score C was planned as a multi-seed repeat of Score A to test
whether the ref/alt difference is stable. Pilot (10 shortlist variants × 5
random seeds) gave **sd = 0.0000, range = 0.0000** for every variant: the
hosted Evo2-40B generate endpoint returns **identical logits regardless of
`random_seed`** (seed affects only sampling, not the log-probabilities used
by Score A).

Consequences, recorded as an empirical finding rather than a silent skip:
- Score A is deterministic on this endpoint; a multi-seed "stability" score is
  vacuous by construction and would add zero information. Re-running it on the
  remaining 94 shortlist variants would waste ~500 API calls.
- Stability in the protocol's spirit (does the ranking survive perturbations?)
  is better served by **Score B strand consistency** (fwd vs rc) and by
  eQTL/GWAS replication, which we run instead.
- Any manuscript text should describe Score A as deterministic and cite
  strand consistency + external QTL replication as the stability evidence.

## 7. Score B (local pseudo-likelihood propagation): complete (104 variants)

Per protocol §7, Score B propagates the observed downstream sequence one base
at a time (`PLL = Σ_i log P(base_i | context + allele + bases<i>)`) and reports
`delta_PLL = PLL(alt) − PLL(ref)` on **both** forward and reverse-complement
strands. Context = upstream 200 bp flank + allele; observed downstream = 8 bp
taken from the ref window (identical for both alleles). 32 generate calls per
variant.

Results (104 shortlist variants, 0 API failures):

| metric | value |
| --- | --- |
| delta_PLL mean | −1.506 |
| delta_PLL median | −0.876 |
| range | −6.487 … +0.906 |
| n(mean > 0) / < 0 | 12 / 92 |
| strand-consistent (fwd & rc same sign) | 68 / 104 (65%) |
| Score A ↔ Score B sign agreement | 90 / 104 (87%) |
| corr(delta_pll_fwd, delta_pll_rc) | 0.13 |

By gene window (median delta_PLL_mean): SIRT1 −1.62 (n=26), IL6 −1.28 (n=35),
NAMPT −0.24 (n=12), SIRT6 −0.57 (n=4), TNF −0.41 (n=23), BST1 −0.41 (n=3).

Largest |delta_PLL| (strand-consistent, negative): SIRT1 `rs1450691401`
(−5.46), IL6 `rs755658631` (−6.49), SIRT1 `rs1471411863` (−5.15).

Interpretation notes (recorded honestly):
- Sign agrees with Score A ~87% of the time, but **strand consistency is only
  65%** and the fwd/rc correlation is low (r ≈ 0.13). The two strands do not
  give a strongly convergent local-surprisal signal for the majority of the
  shortlist. Treat single-strand dominance as noise-prone; a Tier-A candidate
  should require both strands to agree OR flow to one strand only with the
  polarity justified.
- NAMPT window has mild dPLL (median −0.24). Score B does not single out the
  focal gene; polarization still leans to IL6 / SIRT1 / TNF.

## 8. eQTL + GWAS merge → Tier assignment (complete)

Evidence sources (validated live, 2026-09-18): GTEx REST v2
(`singleTissueEqtl`, tissues: Muscle_Skeletal, Adipose_Subcutaneous,
Adipose_Visceral_Omentum, Whole_Blood; min p across tissues) and GWAS Catalog
REST (associations by rsid; p = mantissa × 10^exponent). OpenGWAS and eQTL
Catalogue endpoints returned 404 in this environment and were dropped.
All responses cached under `data_audit/raw/gtex_*` / `gwas_*`; script
`scripts/merge_qtl_gwas.py` (reproducible, `--resume` + failure-caching).

Tier rules (protocol §8):
- Tier A: Evo2 perturbation (|Score A| ≥ 4 OR Score B strand-consistent) AND
  GTEx p < 1e-4 AND GWAS p < 5e-8.
- Tier B: Evo2 perturbation AND (GTEx OR GWAS above threshold).
- Tier C: Evo2 perturbation, no external support (exploratory only).
- External-only: external eQTL/GWAS evidence but no Evo2 perturbation
  (protocol §8's mirror case; labeled separately for honesty).
- Excluded: neither Evo2 perturbation nor external evidence.

Distribution (432 variants):

| tier | n | notes |
| --- | ---: | --- |
| A | 0 | requires Evo2 perturbation + GTEx + GWAS simultaneously |
| B | 0 | requires Evo2 perturbation + one external source |
| C | 97 | Evo2 perturbation only (shortlist, |Score A| ≥ 4 or NAMPT) |
| External-only | 9 | strong public evidence, mild Evo2 signal |
| Excluded | 326 | no evidence on either side |

Key honest findings:
- **Tier A/B = 0.** The Tier-A shortlist (97 Evo2-perturbing variants) is
  dominated by rare variants; GTEx eQTL are computed only for common variants,
  and GWAS Catalog coverage of these rsids is sparse. Evo2 perturbation and
  external QTL/GWAS support therefore barely overlap. This is a real,
  reportable result — not an error.
- The 9 External-only variants are the well-known common loci (TNF
  rs1800629: GTEx p ≈ 7e-24 + GWAS p ≈ 3e-28; IL6 rs1800795: GTEx p ≈ 3.5e-100
  + GWAS p ≈ 2e-25; plus rs1799724, rs361525, rs1800630, rs2069830). They have
  strong public support but mild |Score A| (< 4) and no Score B, so they do
  not enter Evo2-recommended tiers. They remain listed in `tiers.csv` for
  transparency.
- Main-figure gate (§11): the "stable ref/alt Evo2 perturbation **supported by
  at least one public QTL or GWAS source**" criterion is effectively unmet
  because of the rare-variant overlap gap. **Verdict: Evo2 stays a
  supplementary/exploratory module; NOT a main figure.** A scored-variant
  panel can be a supplement; the pipeline+composition panel already rendered
  remains appropriate.

## 9. Remaining work

1. ~~Score A / B / C~~ (A, B done; C degenerate, see §6).
2. ~~eQTL + GWAS merge → Tier A/B/C~~ done — no A/B by honest rules.
3. Optional: if the paper needs Evo2-recommended variants with external
   support, widen the Evo2 threshold (|Score A| ≥ 2, n = 174) or add
   eQTL-gen/GTEx LD-proxy lookups for the shortlist — both change scope and
   must be justified in the text, not slipped in.
4. Figure 5: keep pipeline + composition panels; add a supplementary scored
   panel if desired. Do not promote raw |delta| ranks into the main figure.

## 10. Interpretation boundary (unchanged)

Evo2 scores support regulatory hypotheses. They do not establish eNAMPT
protein secretion, clinical inflammatory status, exercise safety, causal
disease risk, or personalized exercise prescription. Score A does not prove
causality and does not predict clinical risk.
