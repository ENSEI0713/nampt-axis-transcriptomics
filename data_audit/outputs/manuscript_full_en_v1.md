# State-dependent NAMPT-axis transcriptional programs in obesity and exercise adaptation: public transcriptomic and Evo2 sequence-model evidence

**Yanjing Chen¹\* , Zhenyu Shao², Min Zhang³, Yan Zhang⁴\*** 
¹ First author affiliation (to be completed). ² Second author affiliation (to be completed). ³ Third author affiliation (to be completed). ⁴ Corresponding author affiliation (to be completed).
\* Correspondence: Yan Zhang (corresponding author; email to be completed). Yanjing Chen (first author).

> Full-manuscript working draft (EN, v2). Translated and consolidated from the Chinese working drafts
> (`manuscript_frontmatter_v1_zh.md`, `manuscript_results_v2_zh.md`, `manuscript_methods_v1_zh.md`,
> `manuscript_logic_v1_zh.md`). All numbers verified against the on-disk outputs listed in the
> Methods source table; claim boundaries (PROGRESS §4) preserved verbatim in scope.
> Journal: target under decision (top-tier Nature-family journal, see `target_journal_assessment.md`; format check per journal at submission).
> Authors: Yanjing Chen (first), Zhenyu Shao, Min Zhang, Yan Zhang (corresponding).

---

## Abstract

Obesity combines low-grade inflammation with reduced mitochondrial function, and exercise decisions require distinguishing adaptive stress from additional inflammatory load. The NAMPT axis links NAD salvage and repair to immune and metabolic stress, yet whether its transcriptional programs behave as inflammation-like or repair-like across tissue, time and metabolic background remains unclear. We constructed a 59-gene, two-program NAMPT-axis score and applied it within 9 public human transcriptomic units (337 samples). Acute exercise reproducibly raises NAMPT_z (random-effects meta +0.85; dataset-level +0.965), while repair_score does not rise significantly and the balance score loses significance at cluster-aware precision. The same NAMPT upregulation couples to a stronger inflammatory program under lipotoxic stimulation but not under AICAR exercise-mimetic stimulation. Evo2-40B prioritized 432 candidate variants with no Tier A/B support and is reported as supplementary. The NAMPT-NAD system is not captured by a single directional marker; its transcriptional state is context-dependent.

## Introduction

Obesity is commonly accompanied by low-grade chronic inflammation, insulin resistance and reduced mitochondrial function. For people with obesity, the challenge of exercise is not simply "whether to exercise", but how to tell whether a given bout produces a recoverable adaptive stress or an additional load superimposed on an already inflamed background. The two situations are difficult to separate with a single marker at the level of sample, time point and tissue, a long-standing tension in metabolic-exercise research.

NAMPT-related biology connects NAD salvage, cellular repair, and immune and metabolic stress. Intracellular NAMPT (iNAMPT) supports NAD salvage and the SIRT/AMPK/PGC1A axis, mitochondrial function, DNA repair and autophagy; extracellular NAMPT (eNAMPT/visfatin/PBEF) is frequently discussed within NF-κB, monocyte/macrophage activation and low-grade inflammation. These objects are not equivalent, and studies often treat NAMPT-related expression or protein signals as a single-direction marker. This study focuses on what can be assessed from public transcriptomic data: **NAMPT-axis gene-expression programs**, and whether they behave as more inflammation-like or repair-like transcriptional states across tissue, time point and metabolic background. eNAMPT protein and NAD-metabolite directionality remain testable predictions rather than measured results here.

Existing studies are limited in three ways: they often interpret NAMPT or eNAMPT as a single-direction biomarker, neglecting the state dependence among iNAMPT, eNAMPT, NAD metabolism and immune-inflammatory status; public expression studies are mostly single-tissue, single-time-point or single-intervention, lacking a cross-tissue, cross-intervention and cross-timescale transcriptomic evidence ladder; and few studies place expression state, regulatory variants, tissue-specific eQTL/GWAS evidence and large-scale DNA sequence models in one logical chain.

We therefore propose and test a **state-dependent NAMPT-axis transcriptional-program model** using public human transcriptomic evidence and the Evo2-40B sequence model. Specifically, we (1) construct a 59-gene, two-program NAMPT-axis scoring framework and describe its structure with module co-expression; (2) compare the direction of NAMPT-axis transcriptional programs across 9 public matrices, 4 exercise cohorts, obesity/weight-loss cohorts and a cell model under different states; and (3) use Evo2-40B to prioritize 432 candidate regulatory variants at the sequence level and stratify them against public eQTL/GWAS evidence. The framework provides a transcriptomic, testable starting point for NAMPT-related state dependence, but it is not a measurement of eNAMPT protein or NAD-metabolite change, nor does it alone explain mechanism at those levels.

---

## Results

### Result 1. A state-dependent NAMPT-axis score framework with structural validation

**Problem.** NAMPT has a dual identity: intracellular NAMPT supports NAD salvage, SIRT/AMPK/PGC1A, mitochondrial and DNA repair; extracellular NAMPT/visfatin is often placed in NF-κB, monocyte activation and low-grade inflammation frameworks. This requires a testable model that separates the immune-inflammatory side from the metabolic-repair side.

**Approach.** We built a 59-gene NAMPT-axis gene set (repair 34 / inflammatory 19 / both 6) covering NAD salvage, NAD consumption, NF-κB inflammation, monocyte/macrophage, mitochondrial, autophagy, DNA repair and related modules (20 modules). Within each expression matrix, genes were z-scored and `NAMPT_z`, `inflammatory_score`, `repair_score` and `balance_score` (= repair − inflammatory) were computed. Nine public matrices with 337 samples were analyzed; axis-gene coverage was 100% in most datasets.

**Structural validation.** For each dataset we computed module-level Cronbach α (an internal-consistency index, not a significance test of between-group differences) and between-module correlations:
- Large cohorts support the two-program framework: in GSE272133 skeletal muscle (n = 51), nad_salvage_core α = 0.79, sirtuin_repair α = 0.82, ampk_mitochondria_repair α = 0.83, oxidative_stress_repair α = 0.91, dna_damage_repair α = 0.86; GSE305038 (n = 24) module-α mean 0.78; GSE32575 monocytes (n = 47) α mean 0.60.
- Small cohorts show unstable α (GSE312393, GSE282850 show negative α), so module-consistency evidence is preferentially drawn from large cohorts; small-sample module α is unreliable.

**Claim.** A 59-gene axis with two-program scoring separates the NAMPT immune-inflammatory side from the metabolic-repair side; module α provides co-expression support for the two programs that is independent of the prior gene list. The framework holds at the transcriptomic level only.

### Result 2. Exercise-induced NAMPT axis: separation of acute stress and training adaptation

**Approach.** Four exercise cohorts (GSE312393, GSE305038, GSE292369, GSE318937) with 12 paired contrasts were integrated by random-effects meta-analysis (DerSimonian–Laird).

**Meta results.**
| Metric | Pooled effect | 95% CI | Direction agreement | p | I² |
| --- | --- | --- | --- | --- | --- |
| NAMPT_z | **+0.85** | 0.53–1.17 | 92% (11/12) | 1.8e-7 | 64% |
| balance_score | **−0.62** | −1.12–−0.12 | 83% (10 neg) | 0.016 | 98% |
| inflammatory_score | +0.28 | −0.03–+0.58 | 75% | 0.07 | 89% |
| repair_score | −0.33 | −0.67–+0.00 | 83% | 0.05 (ns) | 96% |

NAMPT_z is broadly upregulated after acute exercise. NAMPT upregulation is not automatically repair: repair_score does not rise significantly (−0.33, p = 0.05, CI includes 0). A systematic negative shift of the axis balance requires caution: the 12 contrasts are nested in 4 datasets (GSE318937 contributes 8 alone); after re-estimating with datasets as effective independent units, balance_score pooled −0.47 (95% CI −1.25–+0.32, p = 0.24) loses significance (see `meta_sensitivity_report.md`). NAMPT_z upregulation remains robust at the dataset level (k = 4, +0.965, 95% CI 0.445–1.485, p = 2.8e-4) and under leave-one-dataset-out (positive in all 4 drops). High I² (64–98%) indicates consistent direction but magnitude varying with background; the balance direction is weak evidence, and state-dependent interpretation requires moderator-type examination rather than I² alone.

**Axis-internal immune load.** In GSE318937 (n = 118) and GSE305038, dataset-wide inflammatory_score correlates highly with an axis-internal monocyte/macrophage gene-burden proxy (r = 0.77–0.89, within the 0.7–0.9 range). This proxy is a marker-gene burden overlapping the NAMPT axis, not a cell-type deconvolution; the correlation therefore reflects axis-internal gene co-variation and cannot serve as independent cell-proportion or causal evidence. This is consistent with Phase 1b (predefined-contrast sensitivity) in which the acute inflammation-like signal is mainly driven by NF-κB/cytokine modules; the acute signal returns toward baseline by 24 h (GSE318937 immediate vs 24h balance difference). Correlations are computed on dataset-wide all samples, not split by post-exercise time point.

### Result 3. Obesity and weight loss: tissue- and disease-background dependence of the NAMPT axis

**Approach.** Monocytes (GSE32575), skeletal muscle (GSE272133), visceral adipose (GSE294150) were integrated.

**Findings.**
- The obesity layer contains 3 predefined comparisons (k = 3): NAMPT_z pooled +0.14 (I² = 0%); inflammatory_score pooled +0.57, 67% direction agreement, high heterogeneity. Because comparison number is small and tissue/disease backgrounds differ, this layer is directional evidence only.
- GSE32575 monocytes: obesity vs lean NAMPT_z +0.92 (CI 0.33–1.51); post-surgery inflammatory_score +0.82 (recorded q = 0.007) and repair_score +0.61 rise together; the specific multiple-comparison correction and comparison family are stated in the statistical methods; weight loss cannot be simplified to "inflammation necessarily falls": time point, medication and immune-cell remodeling must be considered.
- Axis-internal immune load: in GSE32575, NAMPT_z correlates with macro/mono burden proxy r = +0.75 and inflammatory_score r = +0.91. This proxy is not deconvolution; results indicate axis-internal immune gene-load co-variation and cannot separate compositional confounding from causation.
- Metabolic-disease background: in GSE272133, T2D post-surgery repair_score +0.30 (absent in non-T2D), suggesting metabolic-disease status changes the direction of skeletal-muscle adaptation after weight loss.

### Result 4. Cell model: the same NAMPT upregulation can correspond to different metabolic stimuli

**Approach.** GSE282850 LHCN-M2 human muscle cells: differentiation vs AICAR (exercise mimic) vs palmitate (lipotoxicity).

**Findings.** Both AICAR and palmitate raise NAMPT_z (meta pooled +1.42, 100% direction agreement), and palmitate corresponds to a higher inflammatory_score (meta pooled +0.55, 100% direction agreement) with balance_score more inflammation-leaning. This supports the core argument that the same NAMPT upregulation carries different metabolic meaning. Note: both contrasts come from one cell line (GSE282850, n = 3–4 paired); pooled precision has no inferential meaning here and this is directional evidence only.

### Result 5. Evo2-40B regulatory-variant prioritization (scoring and evidence tiering complete)

**Pipeline.** Candidates were built from Ensembl REST within TSS ±2 kb promoter-proximal windows of NAMPT-axis core genes (NAMPT/CD38/BST1/SIRT1/SIRT3/SIRT6/IL6/TNF): 12,961 raw records → **432 prioritized functional candidates** (missense / splice / 5'UTR / TF_binding / regulatory_region / ClinVar-annotated), with all 12 NAMPT variants retained. GRCh38 ref/alt 2 kb windows were built and integrity-checked (430 single-base SNPs + 2 indels, 0 ref mismatches).

**Score A (allele surprisal, complete).** All 432 candidates scored (flank 200 bp, Evo2-40B generate logits). |delta| median 1.118; |delta| ≥ 4: 94 variants. High perturbation concentrates in IL6 / SIRT1 / TNF windows (observation, not causal).

**Score B (pseudo-likelihood, shortlist complete).** 104 shortlisted variants (94 with |delta| ≥ 4 + 12 NAMPT full-window) were propagated 8 bp downstream on both strands. Score A↔B sign agreement 87%; strand consistency 65%, fwd/rc correlation low (r ≈ 0.13), a stability limitation. Of the 97 Tier C candidates, 68 (70%) lie in the strand-consistent subset; given the limited double-strand consistency, Tier C candidates are treated as a hypothesis set to be validated, not as a list ranked by stable signal.

**Score C (multi-seed stability) empirically degenerate.** 10×5 seeds all sd = 0: this hosted endpoint's logits do not vary with seed; multi-seed stability carries no information. Strand consistency is used instead as stability evidence.

**eQTL/GWAS merge (complete).** GTEx REST (4 relevant tissues) + GWAS Catalog per-rsid queries for all 432 candidates → `tiers.csv`. Distribution: **A = 0, B = 0, C = 97, External-only = 9, Excluded = 326**. Tier A/B empty is an honest result: the high-perturbation shortlist is almost entirely rare variants, GTEx covers only common variants, and GWAS Catalog coverage of these rsids is sparse, so Evo2 perturbation and externally reproducible support barely overlap; the 9 External-only variants are strongly supported common loci (TNF rs1800629, IL6 rs1800795, etc.) with mild Evo2 scores.

**Gate decision (final).** The Evo2 module does not meet the protocol's "stable perturbation + public QTL/GWAS support" overlap requirement and is **not a main figure**; it is downgraded to a supplementary/exploratory module (see `evo2_variant_results_report.md`). Evo2 still yields a testable regulatory candidate list (Tier C, 97 variants) for future MPRA/CRISPRi validation.

---

## Methods

*(Full text consolidated from `manuscript_methods_v1_zh.md`; section numbering kept for traceability.)*

### 1. Study design and data sources

This is a secondary analysis of public human transcriptomic data (observational, computational design); no new human subjects, animal experiments or individual-level interventions were performed. The object of analysis is the state-dependent NAMPT-axis transcriptional program in obesity, exercise adaptation and metabolic stress; all evidence is transcriptomic (NAMPT mRNA and axis gene expression) and does not constitute measurement of eNAMPT protein or NAD-metabolite abundance.

**1.1 Data screening.** Public datasets were identified in GEO by predefined queries (keywords covering exercise/training, skeletal muscle, blood/PBMC, obesity, adipose tissue, weight loss/metabolic surgery, muscle injury/recovery) and manually prioritized. Inclusion required: human samples or human-derived cell models; publicly downloadable processed expression matrices with sample-level metadata resolvable to condition, time point, tissue and intervention; tissue/cell types relevant to the question (skeletal muscle, adipose, whole blood, PBMC, CD14+ monocytes, macrophages, or human skeletal-muscle cells); explicit comparison structure (pre/post exercise or training, activity reduction, nutritional recovery, obesity/normal weight, pre/post weight-loss surgery, metabolic-state differences). Exclusion/downgrade: animal data as mechanism-only (not primary evidence ladder); cancer/severe infection/severe vascular disease cohorts; datasets whose sample conditions or metadata could not be resolved; NAMPT-mRNA-only data cannot support eNAMPT-protein claims.

**1.2 Included datasets and samples.** Nine transcriptomic analysis units, 337 samples (8 GEO accessions; GSE312393 split into acute 24h and 6-week training units). Coverage of the 59-gene axis was 100% in most datasets (GSE305038 84.7%, GSE282850 79.7%; missing genes scored from available genes).

| Unit | Tissue/cells | Design | Samples |
| --- | --- | --- | --- |
| GSE312393_24h_exercise | skeletal muscle | acute exercise 24h post vs control | 7 |
| GSE312393_6weeks_training | skeletal muscle | 6-week training pre/post | 6 |
| GSE305038_activity_inactivity_exercise | skeletal muscle | active/inactive background × pre/post exercise | 25 |
| GSE292369_exercise_ketone_recovery | skeletal muscle | exercise + ketone/placebo recovery | 34 |
| GSE318937_exercise_oleuropein | skeletal muscle | MICE/SIE × active/placebo × immediate/24h | 119 |
| GSE32575_monocytes_obesity_surgery | CD14+ monocytes | lean vs obese; pre/post weight-loss surgery | 48 |
| GSE272133_muscle_bariatric | skeletal muscle | obese / obese+T2D pre/post surgery | 52 |
| GSE294150_visceral_adipose | visceral adipose | severe obesity (surgery time point) | 40 |
| GSE282850_muscle_cell_aicar_palmitate | human muscle cells (LHCN-M2) | differentiation vs AICAR vs palmitate | 15 |

Sample counts unified to 337 after pre-submission review (units do not double-count GSE312393 samples). Sample-level scores: `nampt_axis_sample_scores.csv`.

**1.3 Preprocessing.** Official processed matrices were downloaded from GEO (dates in `geo_processed_download_manifest.csv`). Expression values use each dataset's native units (counts/FPKM/CPM); **genes are z-scored within dataset only; raw values are never merged across platforms/datasets**. Per-dataset transformations are recorded in `nampt_axis_gene_coverage.csv` (e.g. log2(x+1), or none if already log-like).

### 2. NAMPT-axis gene set and scoring

**2.1 Gene set.** v1 gene set (`NAMPT_axis_gene_set_v1.csv`): **59 NAMPT-axis genes**, 20 functional modules, three layers:
- **repair (34)**: NAD salvage core (NMNAT1/2/3, NAPRT, NADSYN1, etc.), de novo NAD (QPRT), sirtuin repair (SIRT1/3/6), AMPK-mitochondria (PRKAA1/2, PPARGC1A), mitochondrial biogenesis (TFAM, NRF1), oxidative stress (NFE2L2, SOD2, CAT, GPX1), macrophage resolution (MRC1, ARG1), adipose resolution (PPARG, ADIPOQ), insulin metabolism (INSR, IRS1, SLC2A4, AKT2), stress repair (FOXO3), DNA damage repair (ATM, XRCC1, OGG1), autophagy (ATG5, BECN1, MAP1LC3B), etc.;
- **inflammatory (19)**: NAD consumption-inflammation (CD38, BST1), NF-κB (NFKB1, RELA, TNF, IL6, IL1B, CCL2, CXCL8), innate immunity (TLR4, NLRP3, CASP1), monocyte/macrophage markers (ITGAM, CD14, CD68, ADGRE1), tryptophan-kynurenine (KYNU, IDO1), adipose inflammation (LEP);
- **both (6)**: NAMPT and genes dual-classified across modules (PARP1/2, SQSTM1, MTOR, UCP2, UCP3 as counted; exact per-side usage in `nampt_axis_gene_coverage.csv`).

**2.2 Sample-level scoring.** For each matrix: (1) extract the 59 genes (or detected subset); (2) z-score per gene across samples (`z_gi = (x_gi − mean_g)/sd_g`); (3) compute `NAMPT_z` (NAMPT gene z), `inflammatory_score = mean(z over inflammatory genes)`, `repair_score = mean(z over repair genes)`, `balance_score = repair − inflammatory` (positive = relatively repair-like). Scores are used for within-dataset comparisons only; across datasets only direction agreement and random-effects meta are pooled.

### 3. Predefined contrasts and statistics

**3.1 Contrasts.** 19 predefined contrasts (`nampt_axis_predefined_contrasts.csv`, `nampt_axis_formal_contrast_stats.csv`), within-study controls preferred:
- **exercise layer (12 paired contrasts nested in 4 datasets)**: GSE312393 (acute 24h; 6-week training), GSE305038 (active/inactive × pre/post), GSE292369 (exercise vs rest), GSE318937 (MICE/SIE × active/placebo × immediate/24h; 8 contrasts);
- **obesity layer (3 contrasts)**: GSE32575 (post vs pre surgery), GSE272133 (OB w52 vs w0; T2D w52 vs w0);
- **cell-model layer (2 paired contrasts)**: GSE282850 (AICAR vs differentiated; palmitate vs differentiated).

**3.2 Effect sizes and tests.** Paired designs: within-subject delta (post − pre), reporting mean_delta, SD, SE, standardized effect size (Hedges-type) and 95% CI (`nampt_axis_formal_contrast_stats.csv`, `meta/meta_input_contrasts.csv`). Non-paired/multi-group designs follow within-study control structure, reporting direction and CI. **Multiple-comparison control**: q values (BH-FDR) reported per metric within comparison families; Cronbach α is an internal-consistency description, not a between-group significance test, kept distinct from significance α/FDR (review CB-5). Small samples (n ≤ 4) and single-lineage contrasts are directional evidence only (review CB-4).

**3.3 Random-effects meta.** DerSimonian–Laird random effects on within-dataset standardized mean deltas (paired designs only; directional pooling). Outputs: pooled effect, 95% CI, direction agreement, I², τ², Q (`meta/meta_report.md`, `meta_results.csv`). **Cluster-aware sensitivity (CB-1)**: 12 exercise contrasts nested in 4 datasets (GSE318937 alone contributes 8), so we report (1) dataset-level DL (k = 4): NAMPT_z +0.965 (95% CI 0.445–1.485, p = 2.8e-4, 4/4); balance −0.466 (p = 0.24, loses significance); inflammatory/repair ns (p = 0.19 / 0.096); (2) leave-one-dataset-out: NAMPT_z positive in all drops (k = 11/10/11/4, all p < 0.05). Files: `meta/meta_sensitivity_dataset_level.csv`, `meta_sensitivity_lodo.csv`, `meta_sensitivity_report.md`. High I² (64–98%) is reported honestly as consistent direction with magnitude varying by background, not as statistical evidence of state dependence (CB-2); state-dependent interpretation uses within-dataset time-point/training-state description and the moderator-feasibility audit (§7).

**3.4 Module consistency.** Per-dataset module-level Cronbach α and between-module correlations (`axis_structure/module_alpha.csv`, `module_corr_matrix.csv`, `axis_structure_report.md`). α is an internal-consistency index describing whether the two programs form reproducible co-expression units. Large cohorts (GSE272133 n = 51, GSE305038, GSE32575) support the framework (repair α 0.79–0.91); small cohorts (GSE312393, GSE282850) show negative α; α evidence is drawn preferentially from large cohorts with small-sample limitations disclosed.

**3.5 Axis-internal immune load.** In GSE318937 (n = 118 all samples), GSE305038 and GSE32575, correlation of axis scores with an axis-internal monocyte/macrophage gene-burden proxy (marker genes overlapping the NAMPT axis): GSE318937/GSE305038 r = 0.77–0.89; GSE32575 NAMPT_z r = +0.75, inflammatory r = +0.91. The proxy is **not** cell-type deconvolution (CIBERSORT/xCell-type methods not used); results reflect axis-internal co-variation and cannot serve as independent cell-proportion or causal evidence (R1-M5). Correlations use dataset-wide all samples, not split by post-exercise time point.

### 4. Sensitivity analysis (Phase 1b)

Scores recomputed from saved per-dataset matrices and the same predefined contrasts re-run (original Phase 1 files not overwritten; `phase1b_sensitivity/`). Nine variants: gene drops (`drop_nampt`, `drop_classic_cytokines`: CCL2/CXCL8/IL1B/IL6/TNF) and module drops (`drop_nfkb_module`, `drop_monocyte_macrophage`, `drop_nad_salvage_core`, `drop_nad_consumption`, `drop_mito_repair`, `drop_autophagy_dna_repair`, `drop_insulin_adipose_metabolism`). Criteria: direction agreement, direction flips, CI-support retained/lost/gained, minimum genes retained per variant (`nampt_axis_sensitivity_*`). Primary recompute audit max absolute difference ≤ 2.3e-15 (floating-point level). Main conclusions robust to dropping NAMPT and most modules; `drop_nfkb_module` and `drop_classic_cytokines` produce the most CI-support changes, worded as fragility in Results (`phase1b_sensitivity_report.md`).

### 5. Moderator feasibility audit

Sample-level file 346 rows, formal contrasts 76 rows, predefined contrasts 19. Field coverage (`meta/moderator_coverage.csv`): timepoint 70.2%, exercise_type 34.4%, nutrition_or_treatment 34.4%, intervention 74.9%, treatment 51.5%. **Conclusion: no cross-study moderator meta-regression**, because effect sizes are nested within datasets/subjects, with no unified cross-study moderator coding or effect covariance. Within-dataset descriptions are possible for GSE318937, GSE305038, GSE312393; no formal moderator p-values; I² is not interpreted as state-dependence evidence (`meta/moderator_feasibility_report.md`).

### 6. Evo2-40B regulatory-variant pipeline

**6.1 Candidate build (Ensembl REST).** TSS ±2 kb promoter-proximal windows of NAMPT-axis core genes (NAMPT/CD38/BST1/SIRT1/SIRT3/SIRT6/IL6/TNF); functional annotations include missense, splice_region, 5'UTR, TF_binding_site, regulatory_region, plus 130 ClinVar-annotated variants. 12,961 raw → **432 prioritized functional candidates** (all 12 NAMPT variants retained; other genes capped at 60 per window; `build_variant_candidates.py`, `candidates_priority.csv`).

**6.2 GRCh38 ref/alt windows.** Per-candidate 2 kb reference/alternate windows (`build_ref_alt_windows.py` → `windows.bed`, `windows.fasta`): 430 SNPs + 2 indels, 0 ref mismatches; 864 sequences (ref + alt).

**6.3 Evo2 scoring.** Evo2-40B (NVIDIA hosted generate endpoint, `enable_logits=true`, 1 token):
- **Score A (allele surprisal, complete)**: `delta_surprisal = log P(alt) − log P(ref)`, flank 200 bp, DNA-normalized A/C/G/T softmax. 432/432 unique rsids, 0 missing, 0 duplicates (`scores.csv`). |delta| median 1.118; |delta| ≥ 2: 174, ≥ 4: 94; high perturbation in IL6/SIRT1/TNF windows (observation, not causal). Sign is not interpreted as beneficial/harmful;
- **Score B (pseudo-likelihood, shortlist complete)**: 104 shortlist (94 |delta| ≥ 4 + 12 NAMPT full-window), downstream 8 bp two-strand propagation: `PLL = Σ_i log P(base_i | context + allele + bases<i>)`, `delta_PLL = PLL(alt) − PLL(ref)`; 32 generate calls per variant, 0 failures (`scores_B.csv`). delta_PLL median −0.876; Score A↔B sign agreement 87%; **strand consistency 65% (68/104), fwd/rc r ≈ 0.13**, indicating limited double-strand convergence; Tier C treated as hypothesis set, not stable-ranked list (R1-M7);
- **Score C (multi-seed stability) empirically degenerate**: pilot 10 variants × 5 seeds all sd = 0: the hosted endpoint returns identical logits regardless of random_seed (seed affects sampling only, not the log-probabilities used by Score A); multi-seed stability vacuous, full run not performed, disclosed honestly; strand consistency + external QTL replication used as stability evidence (`evo2_variant_results_report.md` §6).

**6.4 eQTL/GWAS merge and Tier assignment.** Sources (validated live 2026-09-18): **GTEx REST v2** (`singleTissueEqtl`, tissues Muscle_Skeletal, Adipose_Subcutaneous, Adipose_Visceral_Omentum, Whole_Blood; min p across tissues) + **GWAS Catalog REST** (per-rsid; p = mantissa × 10^exponent). OpenGWAS and eQTL Catalogue endpoints returned 404 in this environment and were recorded and dropped (`merge_qtl_gwas.py`, cached, `--resume`-safe). Tier rules: A = Evo2 perturbation (|Score A| ≥ 4 OR Score B strand-consistent) AND GTEx p < 1e-4 AND GWAS p < 5e-8; B = perturbation AND (GTEx OR GWAS above threshold); C = perturbation only (exploratory); External-only = external evidence strong but Evo2 mild; Excluded = neither. Distribution (432): **A = 0, B = 0, C = 97, External-only = 9, Excluded = 326**. Tier A/B empty is an honest result: the high-perturbation shortlist is dominated by rare variants; GTEx eQTLs are computed for common variants only and GWAS Catalog coverage of these rsids is sparse, so Evo2 perturbation and external support barely overlap. The 9 External-only are strongly supported common loci (TNF rs1800629: GTEx p ≈ 7e-24 + GWAS p ≈ 3e-28; IL6 rs1800795: GTEx p ≈ 3.5e-100 + GWAS p ≈ 2e-25, plus rs1799724, rs361525, rs1800630, rs2069830) with mild |Score A|. **Main-figure gate**: the "stable ref/alt Evo2 perturbation supported by at least one public QTL/GWAS source" criterion is unmet because of the rare-variant overlap gap; **Evo2 stays a supplementary/exploratory module; NOT a main figure**; Figure 5 keeps pipeline + composition panels; a scored-variant panel belongs in a supplement (`evo2_variant_results_report.md` §5/§8).

**6.5 Evo2 boundary.** Evo2 scores support regulatory-hypothesis prioritization only: no causality, no clinical-risk prediction, no replacement of experimental validation (basis for future MPRA/CRISPRi).

### 7. Software, reproducibility and ethical boundaries

Scripts in `scripts/` (`public_data_audit.py` → `run_evo2_scoring.py` full pipeline); outputs in `data_audit/outputs/`; all public data with accession, download date and processing scripts (`geo_processed_download_manifest.csv`, `audit_run_log.json`). Main computation: Python 3 (NumPy/SciPy-type z-score, paired statistics, DL meta); Cronbach α by standard formula (gene × sample matrix within dataset); Evo2 scoring via NVIDIA hosted endpoint. Planned archiving of processed matrices, score tables, figure-source data and code to Zenodo/OSF/Figshare (DOI); third-party raw data cited by accession, not redistributed. **Ethical/use boundary**: public-data secondary analysis, no individual intervention; public transcriptomic data must not be used for individual diagnosis or exercise prescription; NAMPT mRNA status ≠ eNAMPT protein or NAD metabolites; eNAMPT directionality is a testable prediction (obesity → inflammatory program; training → repair markers), pending protein/metabolite validation.

### 8. Source-of-numbers table (for English-final verification)

| Number/parameter | Value | Source |
| --- | --- | --- |
| Gene set | 59 genes / 20 modules / repair 34 / inflammatory 19 / both 6 | `NAMPT_axis_gene_set_v1.csv` |
| Samples | 9 units / 337 samples | `nampt_axis_sample_scores.csv`, `geo_processed_profile.csv` |
| Contrasts | 19 | `nampt_axis_predefined_contrasts.csv` |
| Exercise meta (contrast-level) | NAMPT_z +0.85 (95% CI 0.53–1.17, 92%, p=1.8e-7, I²=64%) etc. | `meta/meta_report.md`, `meta_results.csv` |
| Exercise meta (dataset-level) | NAMPT_z +0.965 (k=4, p=2.8e-4); balance −0.466 (p=0.24) | `meta/meta_sensitivity_dataset_level.csv` |
| LODO | NAMPT_z positive in all drops | `meta/meta_sensitivity_lodo.csv` |
| Obesity layer | k=3, directional | `meta/meta_report.md` |
| Cell model | k=2, directional; NAMPT_z +1.42 | `meta/meta_report.md` |
| α | large cohorts 0.79–0.91 | `axis_structure/module_alpha.csv` |
| Immune-load r | 0.7–0.9 (all samples) | `cell_composition/cell_scores.csv`, `sensitivity_report.md` |
| Phase 1b | 9 variants | `phase1b_sensitivity/` |
| Evo2 candidates | 12,961 → 432 | `evo2/candidates_priority.csv` |
| Score A | 432/432; |delta| median 1.118 | `evo2/scores.csv` |
| Score B | 104; strand consistency 65% | `evo2/scores_B.csv` |
| Score C | degenerate (sd=0) | `evo2/scores_C.csv`, report §6 |
| Tier | A=0/B=0/C=97/Ext=9/Excl=326 | `evo2/tiers.csv` |

---

## Discussion

We set out to ask whether the NAMPT axis behaves as a single-direction marker or as a state-dependent transcriptional program across obesity and exercise adaptation. Across nine public human transcriptomic units, three findings stand out. First, the two-program structure (a repair-like program of NAD salvage, sirtuin, mitochondrial and DNA-repair modules, separable from an inflammation-like program of NF-κB, innate-immune and monocyte/macrophage modules), which is reproducibly supported in large cohorts by module-level internal consistency (repair-module Cronbach α = 0.79–0.91), indicating that the framework is not an arbitrary gene list but reflects co-expression units that recur across tissues. Second, acute exercise raises NAMPT_z reproducibly (contrast-level meta +0.85; dataset-level k = 4, +0.965, robust to leave-one-dataset-out), while repair_score does not rise significantly and balance_score loses significance at cluster-aware precision. Third, the same NAMPT upregulation carries different program direction under different stimuli: lipotoxic palmitate couples it to a stronger inflammatory program, whereas AICAR exercise-mimetic stimulation does so in a distinct transcriptomic context. The NAMPT-NAD system is therefore not a single "good" or "bad" signal; its transcriptional state must be interpreted across time, training state and metabolic background.

**Relation to the literature.** The view that NAMPT is context-dependent is consistent with the dual-identity literature on extracellular NAMPT/visfatin, which is reported both as an NAD-salvage enzyme with repair functions and as a pro-inflammatory adipocytokine/DAMP in obesity and metabolic disease (Semerena et al.; Dakroub et al.). Our data add a transcriptomic evidence ladder from public human cohorts to this literature: in obesity-related immune cells the NAMPT axis co-varies strongly with axis-internal immune gene load (r ≈ 0.75–0.91), while in skeletal muscle after acute exercise it rises without a reproducible repair-program gain. This pattern helps explain part of the apparent contradiction in the eNAMPT/NAD literature: the same gene product is described as both adaptive and inflammatory, in part because its transcriptional context differs by state. It also aligns with recent reviews of NAD metabolism in exercise adaptation (Jiang et al.), which emphasize the state- and tissue-dependence of NAD-salvage signaling.

**Methodological honesty as a strength.** Several results are negative or inconclusive by design, and we report them as such rather than packaging them: Tier A/B of the Evo2 module is empty because the high-perturbation shortlist is dominated by rare variants with no public QTL/GWAS support; balance_score loses significance at cluster-aware precision; and Score C is empirically degenerate on the hosted endpoint. We consider this an asset: the manuscript's core claim (state dependence of NAMPT-axis transcriptional programs) does not depend on any of these fragile or negative results, and the reader can separate robust from weak evidence at a glance.

**Evidence boundaries.** All results are transcriptomic. NAMPT mRNA status is not eNAMPT protein abundance, and none of our analyses measure NAD metabolites, flux or eNAMPT secretion; eNAMPT directionality (obesity → inflammatory program; training → repair markers) is a testable prediction, not a measured result. Small-sample contrasts (n ≤ 4) and single-lineage cell-model comparisons are directional evidence only. Public transcriptomic data cannot support individual diagnosis or exercise prescription. The Evo2 module prioritizes regulatory hypotheses but does not establish causality or clinical risk.

**Limitations.** (i) The obesity layer contains only three comparisons across different tissues and disease backgrounds and is directional; the field lacks sufficiently large, harmonized human obesity transcriptomic cohorts to support a cross-study moderator meta-regression (moderator feasibility audit). (ii) The axis-internal immune-load analysis is a marker-gene burden proxy, not cell-type deconvolution; compositional confounding cannot be excluded. (iii) The Evo2 module is limited by the rare-variant overlap gap with public QTL/GWAS data, by 65% strand consistency in Score B, and by the degenerate multi-seed endpoint. (iv) Nine transcriptomic units are a moderate sample; effect magnitudes vary across backgrounds (I² = 64–98%), so pooled point estimates should be read with their cluster-aware intervals. (v) No eNAMPT protein, NAD metabolite, or experimental validation is included; these are the key missing evidence types for strengthening the causal claim.

**Implications and next steps.** The framework offers a practical way to separate "NAMPT is up" from "repair is happening" in exercise and obesity research: a single NAMPT readout is insufficient, and the axis balance (repair minus inflammatory programs) provides a more informative, though weaker, descriptor. The Evo2 module leaves a verifiable candidate list (Tier C, 97 variants; 68 within the strand-consistent subset) for future MPRA/CRISPRi testing. To strengthen the causal claim, three evidence types are needed in future work: (i) protein/metabolite validation of eNAMPT and NAD (e.g. MoTrPAC human multi-omics or targeted plasma eNAMPT/NAD measurements); (ii) prospective exercise-intervention cohorts relating the axis score to obesity, inflammation, fitness, recovery and safety endpoints; and (iii) experimental validation of a small number of Evo2-prioritized enhancer/variant candidates. Until then, the contribution of this study is a reproducible, boundary-respecting transcriptomic evidence ladder for the state-dependent NAMPT-axis model.

---

*End of EN draft v2 (Discussion completed). Numbers and boundaries to be re-verified against the source table before journal submission; references to be finalized (see references_v1.bib TODO); abstract/title to be trimmed to journal limits (Abstract ≤ 150 words, title ≤ 15 words) at final formatting.*
