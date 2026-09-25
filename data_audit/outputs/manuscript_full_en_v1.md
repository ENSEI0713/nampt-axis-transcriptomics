# State-dependent NAMPT-axis transcriptional programs in obesity and exercise

**Yanjing Chen¹,²,³\*, Zhenyu Shao³, Min Zhang³, Yan Zhang³,⁴\***

¹ Laboratory and State-Owned Assets Management Division, Capital University of Physical Education and Sports, Beijing 100191, China.
² Precision Omics Laboratory for Sport Medicine & Engineering, Beijing, China (affiliated to Beijing Key Laboratory of Interdisciplinary Intelligent Technologies in Sports Medicine and Engineering).
³ Sports & Medicine Integrative Innovation Center, Capital University of Physical Education and Sports, Beijing 100191, China.
⁴ Beijing Key Laboratory of Interdisciplinary Intelligent Technologies in Sports Medicine and Engineering, Beijing 100191, China.

\* Correspondence: Yan Zhang (zhangyan2021@cupes.edu.cn); Yanjing Chen (chenyanjing@cupes.edu.cn).

---

## Abstract

Obesity combines low-grade inflammation with reduced mitochondrial function, and exercise decisions require distinguishing adaptive stress from additional inflammatory load. The NAMPT axis links NAD salvage and repair to immune and metabolic stress, yet whether its transcriptional programs behave as inflammation-like or repair-like across tissue, time and metabolic background remains unclear. We constructed a 59-gene, two-program NAMPT-axis score and applied it within 9 public human transcriptomic units (337 samples). Here, we show that acute exercise reproducibly raises NAMPT expression while the repair program does not increase and the axis balance loses significance at cluster-aware precision; the same upregulation instead couples to a stronger inflammatory program under lipotoxic stimulation. An Evo2-40B prioritization of 432 regulatory variants yields no Tier A/B support and is reported as supplementary. The NAMPT-NAD system is therefore not captured by a single directional marker; its transcriptional state is context-dependent.

## Introduction

Obesity is commonly accompanied by low-grade chronic inflammation, insulin resistance and reduced mitochondrial function. For people with obesity, the challenge of exercise is not simply "whether to exercise", but how to tell whether a given bout produces a recoverable adaptive stress or an additional load superimposed on an already inflamed background. The two situations are difficult to separate with a single marker at the level of sample, time point and tissue, a long-standing tension in metabolic-exercise research.

Abbreviations used throughout: NAMPT, nicotinamide phosphoribosyltransferase; NAD, nicotinamide adenine dinucleotide; T2D, type 2 diabetes; MICE, moderate-intensity continuous exercise; SIE, sprint-interval exercise; GRCh38, Genome Reference Consortium Human Build 38; LODO, leave-one-dataset-out; BH-FDR, Benjamini–Hochberg false discovery rate; CI, confidence interval.

NAMPT-related biology connects NAD salvage, cellular repair, and immune and metabolic stress. Intracellular NAMPT (iNAMPT) supports NAD salvage and the SIRT/AMPK/PGC1A axis, mitochondrial function, DNA repair and autophagy; extracellular NAMPT (eNAMPT/visfatin/PBEF) is frequently discussed within NF-κB, monocyte/macrophage activation and low-grade inflammation. These objects are not equivalent, and studies often treat NAMPT-related expression or protein signals as a single-direction marker. This study focuses on what can be assessed from public transcriptomic data: **NAMPT-axis gene-expression programs**, and whether they behave as more inflammation-like or repair-like transcriptional states across tissue, time point and metabolic background. eNAMPT protein and NAD-metabolite directionality remain testable predictions rather than measured results here.

Existing studies are limited in three ways: they often interpret NAMPT or eNAMPT as a single-direction biomarker, neglecting the state dependence among iNAMPT, eNAMPT, NAD metabolism and immune-inflammatory status; public expression studies are mostly single-tissue, single-time-point or single-intervention, lacking a cross-tissue, cross-intervention and cross-timescale transcriptomic evidence ladder; and few studies place expression state, regulatory variants, tissue-specific expression quantitative trait locus (eQTL)/genome-wide association study (GWAS) evidence and large-scale DNA sequence models in one logical chain.

We therefore propose and test a **state-dependent NAMPT-axis transcriptional-program model** using public human transcriptomic evidence and the Evo2-40B sequence model<sup>[1]</sup>. Specifically, we (1) construct a 59-gene, two-program NAMPT-axis scoring framework and describe its structure with module co-expression; (2) compare the direction of NAMPT-axis transcriptional programs across 9 public matrices, 4 exercise cohorts, obesity/weight-loss cohorts and a cell model under different states; and (3) use Evo2-40B to prioritize 432 candidate regulatory variants at the sequence level and stratify them against public eQTL/GWAS evidence, using the Genotype-Tissue Expression (GTEx) project<sup>[2]</sup> and the GWAS Catalog<sup>[3]</sup>. The framework provides a transcriptomic, testable starting point for NAMPT-related state dependence, but it is not a measurement of eNAMPT protein or NAD-metabolite change, nor does it alone explain mechanism at those levels.

---

## Results

### Result 1. A state-dependent NAMPT-axis score framework with structural validation

**Problem.** NAMPT has a dual identity: intracellular NAMPT supports NAD salvage, SIRT/AMPK/PGC1A, mitochondrial and DNA repair; extracellular NAMPT/visfatin is often placed in NF-κB, monocyte activation and low-grade inflammation frameworks. This requires a testable model that separates the immune-inflammatory side from the metabolic-repair side.

**Approach.** We built a 59-gene NAMPT-axis gene set (repair 34 / inflammatory 19 / both 6) covering NAD salvage, NAD consumption, NF-κB inflammation, monocyte/macrophage, mitochondrial, autophagy, DNA repair and related modules (20 modules). Within each expression matrix, genes were z-scored and `NAMPT_z`, `inflammatory_score`, `repair_score` and `balance_score` (= repair − inflammatory) were computed. Nine public matrices with 337 samples were analyzed; axis-gene coverage was 100% in most datasets (Fig. 2a); the framework is summarized in Fig. 1.

**Structural validation.** For each dataset we computed module-level Cronbach α<sup>[4]</sup> (an internal-consistency index, not a significance test of between-group differences) and between-module correlations:
- Large cohorts support the two-program framework: in GSE272133<sup>[5]</sup> skeletal muscle (n = 52), nad_salvage_core α = 0.79, sirtuin_repair α = 0.82, ampk_mitochondria_repair α = 0.83, oxidative_stress_repair α = 0.91, dna_damage_repair α = 0.86; GSE305038<sup>[6]</sup> (n = 24) module-α mean 0.78; GSE32575<sup>[7]</sup> monocytes (n = 48) α mean 0.60.
- Small cohorts show unstable α (GSE312393, GSE282850 show negative α), so module-consistency evidence is preferentially drawn from large cohorts; small-sample module α is unreliable.

**Claim.** A 59-gene axis with two-program scoring separates the NAMPT immune-inflammatory side from the metabolic-repair side; module α provides co-expression support for the two programs that is independent of the prior gene list. The framework holds at the transcriptomic level only.

### Result 2. Exercise-induced NAMPT axis: separation of acute stress and training adaptation

**Approach.** Four exercise cohorts (GSE312393<sup>[8]</sup>, GSE305038<sup>[6]</sup>, GSE292369<sup>[9]</sup>, GSE318937<sup>[10]</sup>) with 12 paired contrasts were integrated by random-effects meta-analysis (DerSimonian–Laird)<sup>[11]</sup>.

**Meta results (Fig. 4).**
| Metric | Pooled effect | 95% CI | Direction agreement | p | I² |
| --- | --- | --- | --- | --- | --- |
| NAMPT_z | **+0.85** | 0.53–1.17 | 92% (11/12) | 1.8e-7 | 64% |
| balance_score | **−0.62** | −1.12–−0.12 | 83% (10 neg) | 0.016 | 98% |
| inflammatory_score | +0.28 | −0.03–+0.58 | 75% | 0.07 | 89% |
| repair_score | −0.33 | −0.67–+0.00 | 83% | 0.05 (ns) | 96% |

NAMPT_z is broadly upregulated after acute exercise. NAMPT upregulation is not automatically repair: repair_score does not rise significantly (−0.33, p = 0.05, CI includes 0). A systematic negative shift of the axis balance requires caution: the 12 contrasts are nested in 4 datasets (GSE318937 contributes 8 alone); after re-estimating with datasets as effective independent units, balance_score pooled −0.47 (95% CI −1.25–+0.32, p = 0.24) loses significance (Methods, "Sensitivity analysis"). NAMPT_z upregulation remains robust at the dataset level (k = 4, +0.965, 95% CI 0.445–1.485, p = 2.8e-4) and under leave-one-dataset-out (positive in all 4 drops). High I² (64–98%) indicates consistent direction but magnitude varying with background; the balance direction is weak evidence, and state-dependent interpretation requires moderator-type examination rather than I² alone.

**Axis-internal immune load.** In GSE318937 (n = 119) and GSE305038, dataset-wide inflammatory_score correlates highly with an axis-internal monocyte/macrophage gene-burden proxy (r = 0.77–0.89, within the 0.7–0.9 range). This proxy is a marker-gene burden overlapping the NAMPT axis, not a cell-type deconvolution; the correlation therefore reflects axis-internal gene co-variation and cannot serve as independent cell-proportion or causal evidence. This is consistent with Phase 1b (predefined-contrast sensitivity) in which the acute inflammation-like signal is mainly driven by NF-κB/cytokine modules; the acute signal returns toward baseline by 24 h (GSE318937 immediate vs 24h balance difference; Fig. 3b). Correlations are computed on dataset-wide all samples, not split by post-exercise time point.

### Result 3. Obesity and weight loss: tissue- and disease-background dependence of the NAMPT axis

**Approach.** Monocytes (GSE32575<sup>[7]</sup>), skeletal muscle (GSE272133<sup>[5]</sup>), and visceral adipose (GSE294150, unpublished; cited as a GEO dataset in Data Availability) were integrated.

**Findings (Fig. 5).**
- The obesity layer contains 3 predefined comparisons (k = 3): NAMPT_z pooled +0.14 (I² = 0%); inflammatory_score pooled +0.57, 67% direction agreement, high heterogeneity. Because comparison number is small and tissue/disease backgrounds differ, this layer is directional evidence only.
- GSE32575 monocytes: obesity vs lean NAMPT_z +0.92 (CI 0.33–1.51); post-surgery inflammatory_score +0.82 (recorded BH-FDR q = 0.007) and repair_score +0.61 rise together; the specific multiple-comparison correction and comparison family are stated in the statistical methods; weight loss cannot be simplified to "inflammation necessarily falls": time point, medication and immune-cell remodeling must be considered.
- Axis-internal immune load: in GSE32575, NAMPT_z correlates with macro/mono burden proxy r = +0.75 and inflammatory_score r = +0.91. This proxy is not deconvolution; results indicate axis-internal immune gene-load co-variation and cannot separate compositional confounding from causation.
- Metabolic-disease background: in GSE272133, type 2 diabetes (T2D) post-surgery repair_score +0.30 (absent in non-T2D), suggesting metabolic-disease status changes the direction of skeletal-muscle adaptation after weight loss.

### Result 4. Cell model: the same NAMPT upregulation can correspond to different metabolic stimuli

**Approach.** GSE282850<sup>[12]</sup> LHCN-M2 human muscle cells: differentiation vs AICAR (exercise mimic) vs palmitate (lipotoxicity).

**Findings.** Both AICAR and palmitate raise NAMPT_z (meta pooled +1.42, 100% direction agreement), and palmitate corresponds to a higher inflammatory_score (meta pooled +0.55, 100% direction agreement) with balance_score more inflammation-leaning. This supports the core argument that the same NAMPT upregulation carries different metabolic meaning. Note: both contrasts come from one cell line (GSE282850, n = 3–4 paired); pooled precision has no inferential meaning here and this is directional evidence only.

### Result 5. Evo2-40B regulatory-variant prioritization (scoring and evidence tiering complete)

**Pipeline.** Candidates were built from Ensembl REST within transcription start site (TSS) ±2 kb promoter-proximal windows of NAMPT-axis core genes (NAMPT/CD38/BST1/SIRT1/SIRT3/SIRT6/IL6/TNF): 12,961 raw records → **432 prioritized functional candidates** (missense / splice / 5'UTR / TF_binding / regulatory_region / ClinVar-annotated), with all 12 NAMPT variants retained. GRCh38 (hg38) ref/alt 2 kb windows were built and integrity-checked (430 single-base SNPs + 2 indels, 0 ref mismatches; Fig. 6a).

**Score A (allele surprisal, complete).** All 432 candidates scored (flank 200 bp, Evo2-40B generate logits). |delta| median 1.118; |delta| ≥ 4: 94 variants. High perturbation concentrates in IL6 / SIRT1 / TNF windows (observation, not causal).

**Score B (pseudo-likelihood, shortlist complete).** 104 shortlisted variants (94 with |delta| ≥ 4 plus the 12 NAMPT full-window set, of which 2 NAMPT variants also meet |delta| ≥ 4, so 94 + 12 − 2 = 104) were propagated 8 bp downstream on both strands. Score A↔B sign agreement 87%; strand consistency 65%, fwd/rc correlation low (r ≈ 0.13), a stability limitation. Of the 97 Tier C candidates, 68 (70%) lie in the strand-consistent subset; given the limited double-strand consistency, Tier C candidates are treated as a hypothesis set to be validated, not as a list ranked by stable signal.

**Score C (multi-seed stability) empirically degenerate.** 10×5 seeds all sd = 0: this hosted endpoint's logits do not vary with seed; multi-seed stability carries no information. Strand consistency is used instead as stability evidence.

**eQTL/GWAS merge (complete).** GTEx REST<sup>[2]</sup> (4 relevant tissues) + GWAS Catalog<sup>[3]</sup> per-rsid queries for all 432 candidates (Supplementary Data 8).

**Gate decision (final).** The Evo2 module does not meet the protocol's "stable perturbation + public QTL/GWAS support" overlap requirement and is **not a main figure**; it is downgraded to a supplementary/exploratory module (Methods, "Evo2-40B regulatory-variant pipeline"). Evo2 still yields a testable regulatory candidate list (Tier C, 97 variants) for future massively parallel reporter assay (MPRA)/CRISPR interference (CRISPRi) validation.

---

## Discussion

We set out to ask whether the NAMPT axis behaves as a single-direction marker or as a state-dependent transcriptional program across obesity and exercise adaptation. Across nine public human transcriptomic units, three findings stand out. First, the two-program structure (a repair-like program of NAD salvage, sirtuin, mitochondrial and DNA-repair modules, separable from an inflammation-like program of NF-κB, innate-immune and monocyte/macrophage modules), which is reproducibly supported in large cohorts by module-level internal consistency (repair-module Cronbach α = 0.79–0.91), indicating that the framework is not an arbitrary gene list but reflects co-expression units that recur across tissues. Second, acute exercise raises NAMPT_z reproducibly (contrast-level meta +0.85; dataset-level k = 4, +0.965, robust to leave-one-dataset-out), while repair_score does not rise significantly and balance_score loses significance at cluster-aware precision. Third, the same NAMPT upregulation carries different program direction under different stimuli: lipotoxic palmitate couples it to a stronger inflammatory program, whereas AICAR exercise-mimetic stimulation raises NAMPT without the inflammatory-program gain, in a distinct transcriptomic context. The NAMPT-NAD system is therefore not a single "good" or "bad" signal; its transcriptional state must be interpreted across time, training state and metabolic background.

**Relation to the literature.** The view that NAMPT is context-dependent is consistent with the dual-identity literature on extracellular NAMPT/visfatin, which is reported both as an NAD-salvage enzyme with repair functions and as a pro-inflammatory adipocytokine/damage-associated molecular pattern (DAMP) in obesity and metabolic disease<sup>[13,14]</sup>. Our data add a transcriptomic evidence ladder from public human cohorts to this literature: in obesity-related immune cells the NAMPT axis co-varies strongly with axis-internal immune gene load (r ≈ 0.75–0.91), while in skeletal muscle after acute exercise it rises without a reproducible repair-program gain. This pattern helps explain part of the apparent contradiction in the eNAMPT/NAD literature: the same gene product is described as both adaptive and inflammatory, in part because its transcriptional context differs by state. It also aligns with recent reviews of NAD metabolism in exercise adaptation<sup>[15]</sup>, which emphasize the state- and tissue-dependence of NAD-salvage signaling.

**Evidence boundaries.** All results are transcriptomic. NAMPT mRNA status is not eNAMPT protein abundance, and none of our analyses measure NAD metabolites, flux or eNAMPT secretion; eNAMPT directionality (obesity → inflammatory program; training → repair markers) is a testable prediction, not a measured result. Small-sample contrasts (n ≤ 4) and single-lineage cell-model comparisons are directional evidence only. Public transcriptomic data cannot support individual diagnosis or exercise prescription. The Evo2 module prioritizes regulatory hypotheses but does not establish causality or clinical risk.

**Limitations.** (i) The obesity layer contains only three comparisons across different tissues and disease backgrounds and is directional; the field lacks sufficiently large, harmonized human obesity transcriptomic cohorts to support a cross-study moderator meta-regression (moderator feasibility audit). (ii) The axis-internal immune-load analysis is a marker-gene burden proxy, not cell-type deconvolution; compositional confounding cannot be excluded. (iii) The Evo2 module is limited by the rare-variant overlap gap with public QTL/GWAS data, by 65% strand consistency in Score B, and by the degenerate multi-seed endpoint. (iv) Nine transcriptomic units are a moderate sample; effect magnitudes vary across backgrounds (I² = 64–98%), so pooled point estimates should be read with their cluster-aware intervals. (v) No eNAMPT protein, NAD metabolite, or experimental validation is included; these are the key missing evidence types for strengthening the causal claim.

**Implications and next steps.** The framework offers a practical way to separate "NAMPT is up" from "repair is happening" in exercise and obesity research: a single NAMPT readout is insufficient, and the axis balance (repair minus inflammatory programs) provides a more informative, though weaker, descriptor. The Evo2 module leaves a verifiable candidate list (Tier C, 97 variants; 68 within the strand-consistent subset) for future MPRA/CRISPRi testing. To strengthen the causal claim, three evidence types are needed in future work: (i) protein/metabolite validation of eNAMPT and NAD (e.g. the Molecular Transducers of Physical Activity Consortium (MoTrPAC) human multi-omics or targeted plasma eNAMPT/NAD measurements); (ii) prospective exercise-intervention cohorts relating the axis score to obesity, inflammation, fitness, recovery and safety endpoints; and (iii) experimental validation of a small number of Evo2-prioritized enhancer/variant candidates. Until then, the contribution of this study is a reproducible, boundary-respecting transcriptomic evidence ladder for the state-dependent NAMPT-axis model.

---



## Methods

### 1. Study design and data sources

This is a secondary analysis of public human transcriptomic data (observational, computational design); no new human subjects, animal experiments or individual-level interventions were performed. The object of analysis is the state-dependent NAMPT-axis transcriptional program in obesity, exercise adaptation and metabolic stress; all evidence is transcriptomic (NAMPT mRNA and axis gene expression) and does not constitute measurement of eNAMPT protein or NAD-metabolite abundance.

**1.1 Data screening.** Public datasets were identified in the Gene Expression Omnibus (GEO) by predefined queries (keywords covering exercise/training, skeletal muscle, blood/peripheral blood mononuclear cells (PBMC), obesity, adipose tissue, weight loss/metabolic surgery, muscle injury/recovery) and manually prioritized. Inclusion required: human samples or human-derived cell models; publicly downloadable processed expression matrices with sample-level metadata resolvable to condition, time point, tissue and intervention; tissue/cell types relevant to the question (skeletal muscle, adipose, whole blood, PBMC, CD14+ monocytes, macrophages, or human skeletal-muscle cells); explicit comparison structure (pre/post exercise or training, activity reduction, nutritional recovery, obesity/normal weight, pre/post weight-loss surgery, metabolic-state differences). Exclusion/downgrade: animal data as mechanism-only (not primary evidence ladder); cancer/severe infection/severe vascular disease cohorts; datasets whose sample conditions or metadata could not be resolved; NAMPT-mRNA-only data cannot support eNAMPT-protein claims.

**1.2 Included datasets and samples.** Nine transcriptomic analysis units, **337 unique formal analysis samples** (8 GEO accessions; GSE312393 split into acute 24h and 6-week training units). Coverage of the 59-gene axis was 100% in most datasets (GSE305038 84.7%, GSE282850 79.7%; missing genes scored from available genes). The sample-level score table contains 346 analysis-unit records because the 13 GSE312393 samples are represented in both split units; the long-format GEO metadata contains 351 provenance rows. These record counts are not additional biological samples.

| Unit | Tissue/cells | Design | Samples |
| --- | --- | --- | --- |
| GSE312393_24h_exercise | skeletal muscle | acute exercise 24h post vs control | 7 |
| GSE312393_6weeks_training | skeletal muscle | 6-week training pre/post | 6 |
| GSE305038_activity_inactivity_exercise | skeletal muscle | active/inactive background × pre/post exercise | 25 |
| GSE292369_exercise_ketone_recovery | skeletal muscle | exercise + ketone/placebo recovery | 34 |
| GSE318937_exercise_oleuropein | skeletal muscle | moderate-intensity continuous exercise (MICE) / sprint-interval exercise (SIE) × active/placebo × immediate/24h | 119 |
| GSE32575_monocytes_obesity_surgery | CD14+ monocytes | lean vs obese; pre/post weight-loss surgery | 48 |
| GSE272133_muscle_bariatric | skeletal muscle | obese / obese+T2D pre/post surgery | 52 |
| GSE294150_visceral_adipose | visceral adipose | severe obesity (surgery time point) | 40 |
| GSE282850_muscle_cell_aicar_palmitate | human muscle cells (LHCN-M2) | differentiation vs AICAR vs palmitate | 15 |

The sample-level score file contains 346 analysis-unit records across 9 units. After deduplication, GSE312393 contributes 13 unique biological samples to two units (7 acute + 6 training), giving 337 unique formal analysis samples. The separate long-format GEO metadata file contains 351 provenance rows. Sample-level scores are provided in Supplementary Data 1.

**1.3 Preprocessing.** Official processed matrices were downloaded from GEO (download dates in Supplementary Data 1). Expression values use each dataset's native units (counts/FPKM/CPM); **genes are z-scored within dataset only; raw values are never merged across platforms/datasets**. Per-dataset transformations (e.g. log2(x+1), or none if already log-like) are recorded in Supplementary Data 1.

### 2. NAMPT-axis gene set and scoring

**2.1 Gene set.** v1 gene set (Supplementary Data 2): **59 NAMPT-axis genes**, 20 functional modules, three layers:
- **repair (34)**: NAD salvage core (NMNAT1/2/3, NAPRT, NADSYN1, etc.), de novo NAD (QPRT), sirtuin repair (SIRT1/3/6), AMPK-mitochondria (PRKAA1/2, PPARGC1A), mitochondrial biogenesis (TFAM, NRF1), oxidative stress (NFE2L2, SOD2, CAT, GPX1), macrophage resolution (MRC1, ARG1), adipose resolution (PPARG, ADIPOQ), insulin metabolism (INSR, IRS1, SLC2A4, AKT2), stress repair (FOXO3), DNA damage repair (ATM, XRCC1, OGG1), autophagy (ATG5, BECN1, MAP1LC3B), etc.;
- **inflammatory (19)**: NAD consumption-inflammation (CD38, BST1), NF-κB (NFKB1, RELA, TNF, IL6, IL1B, CCL2, CXCL8), innate immunity (TLR4, NLRP3, CASP1), monocyte/macrophage markers (ITGAM, CD14, CD68, ADGRE1), tryptophan-kynurenine (KYNU, IDO1), adipose inflammation (LEP);
- **both (6)**: NAMPT and genes dual-classified across modules (PARP1/2, SQSTM1, MTOR, UCP2, UCP3 as counted; exact per-side usage in Supplementary Data 2).

**2.2 Sample-level scoring.** For each matrix: (1) extract the 59 genes (or detected subset); (2) z-score per gene across samples (`z_gi = (x_gi − mean_g)/sd_g`); (3) compute `NAMPT_z` (NAMPT gene z), `inflammatory_score = mean(z over inflammatory genes)`, `repair_score = mean(z over repair genes)`, `balance_score = repair − inflammatory` (positive = relatively repair-like). Scores are used for within-dataset comparisons only; across datasets only direction agreement and random-effects meta are pooled.

### 3. Predefined contrasts and statistics

**3.1 Contrasts.** 19 predefined contrasts (Supplementary Data 3), within-study controls preferred. Twelve paired exercise contrasts nested in four datasets enter the paired exercise meta-analysis; Figure 3 additionally displays one unpaired acute-24 h comparison for descriptive dynamics, so its plotted exercise display contains 13 contrasts:
- **exercise layer (12 paired contrasts nested in 4 datasets)**: GSE312393 (6-week training paired contrast; the acute-24h unit is an unpaired design, counted among the 19 predefined contrasts but not in the paired meta), GSE305038 (active/inactive × pre/post), GSE292369 (exercise vs rest), GSE318937 (MICE/SIE × active/placebo × immediate/24h; 8 paired contrasts);
- **obesity layer (3 contrasts)**: GSE32575 (post vs pre surgery), GSE272133 (obese (OB) w52 vs w0; T2D w52 vs w0);
- **cell-model layer (2 paired contrasts)**: GSE282850 (AICAR vs differentiated; palmitate vs differentiated).

**3.2 Effect sizes and tests.** Paired designs: within-subject delta (post − pre), reporting mean_delta, SD, SE, standardized effect size (Hedges-type) and 95% CI (Supplementary Data 3). Non-paired/multi-group designs follow within-study control structure, reporting direction and CI. **Multiple-comparison control**: q values (BH-FDR)<sup>[16]</sup> reported per metric within comparison families; Cronbach α is an internal-consistency description, not a between-group significance test, kept distinct from significance α/FDR. Small samples (n ≤ 4) and single-lineage contrasts are directional evidence only.

**3.3 Random-effects meta.** DerSimonian–Laird random effects on within-dataset standardized mean deltas (paired designs only; directional pooling). Outputs: pooled effect, 95% CI, direction agreement, I², τ² and Q (Supplementary Data 4). **Cluster-aware sensitivity**: 12 exercise contrasts nested in 4 datasets (GSE318937 alone contributes 8), so we report (1) dataset-level DL (k = 4): NAMPT_z +0.965 (95% CI 0.445–1.485, p = 2.8e-4, 4/4); balance −0.466 (p = 0.24, loses significance); inflammatory/repair ns (p = 0.19 / 0.096); (2) leave-one-dataset-out: NAMPT_z positive in all drops (k = 11/10/11/4, all p < 0.05). Cluster-aware and leave-one-dataset-out results are provided in Supplementary Data 4. High I² (64–98%) reflects consistent direction with magnitude varying by background, not as statistical evidence of state dependence; state-dependent interpretation uses within-dataset time-point/training-state description and the moderator-feasibility audit (§7).

**3.4 Module consistency.** Per-dataset module-level Cronbach α and between-module correlations (Supplementary Data 5). α is an internal-consistency index describing whether the two programs form reproducible co-expression units. Large cohorts (GSE272133 n = 51, GSE305038, GSE32575) support the framework (repair α 0.79–0.91); small cohorts (GSE312393, GSE282850) show negative α; α evidence is drawn preferentially from large cohorts with small-sample limitations disclosed.

**3.5 Axis-internal immune load.** In GSE318937 (n = 119 all samples), GSE305038 and GSE32575, correlation of axis scores with an axis-internal monocyte/macrophage gene-burden proxy (marker genes overlapping the NAMPT axis): GSE318937/GSE305038 r = 0.77–0.89; GSE32575 NAMPT_z r = +0.75, inflammatory r = +0.91. The proxy is **not** cell-type deconvolution (CIBERSORT/xCell-type methods not used); results reflect axis-internal co-variation and cannot serve as independent cell-proportion or causal evidence. Correlations use dataset-wide all samples, not split by post-exercise time point.

### 4. Sensitivity analysis (Phase 1b)

Scores recomputed from saved per-dataset matrices and the same predefined contrasts re-run (original Phase 1 files not overwritten). Nine variants: gene drops (`drop_nampt`, `drop_classic_cytokines`: CCL2/CXCL8/IL1B/IL6/TNF) and module drops (`drop_nfkb_module`, `drop_monocyte_macrophage`, `drop_nad_salvage_core`, `drop_nad_consumption`, `drop_mito_repair`, `drop_autophagy_dna_repair`, `drop_insulin_adipose_metabolism`). Criteria: direction agreement, direction flips, CI-support retained/lost/gained, minimum genes retained per variant (Supplementary Data 6). Primary recompute audit max absolute difference ≤ 2.3e-15 (floating-point level). Main conclusions robust to dropping NAMPT and most modules; `drop_nfkb_module` and `drop_classic_cytokines` produce the most CI-support changes, are reported with appropriate caution in Results.

### 5. Moderator feasibility audit

Sample-level file 346 rows, formal contrasts 76 rows, predefined contrasts 19. Field coverage (Supplementary Data 7): timepoint 70.2%, exercise_type 34.4%, nutrition_or_treatment 34.4%, intervention 74.9%, treatment 51.5%. **Conclusion: no cross-study moderator meta-regression**, because effect sizes are nested within datasets/subjects, with no unified cross-study moderator coding or effect covariance. Within-dataset descriptions are possible for GSE318937, GSE305038, GSE312393; no formal moderator p-values; I² is not interpreted as state-dependence evidence.

### 6. Evo2-40B regulatory-variant pipeline

**6.1 Candidate build (Ensembl REST).** TSS ±2 kb promoter-proximal windows of NAMPT-axis core genes (NAMPT/CD38/BST1/SIRT1/SIRT3/SIRT6/IL6/TNF); functional annotations include missense, splice_region, 5'UTR, TF_binding_site, regulatory_region, plus 130 ClinVar-annotated variants. 12,961 raw → **432 prioritized functional candidates** (all 12 NAMPT variants retained; other genes capped at 60 per window).

**6.2 GRCh38 ref/alt windows.** Per-candidate 2 kb reference/alternate windows: 430 SNPs + 2 indels, 0 ref mismatches; 864 sequences (ref + alt).

**6.3 Evo2 scoring.** Evo2-40B (NVIDIA hosted generate endpoint, `enable_logits=true`, 1 token):
- **Score A (allele surprisal, complete)**: `delta_surprisal = log P(alt) − log P(ref)`, flank 200 bp, DNA-normalized A/C/G/T softmax. 432/432 unique rsids, 0 missing, 0 duplicates. |delta| median 1.118; |delta| ≥ 2: 174, ≥ 4: 94; high perturbation in IL6/SIRT1/TNF windows (observation, not causal). Sign is not interpreted as beneficial/harmful;
- **Score B (pseudo-likelihood, shortlist complete)**: 104 shortlist (94 variants with |delta| ≥ 4 plus the 12 NAMPT full-window set, of which 2 NAMPT variants also meet |delta| ≥ 4, so 94 + 12 − 2 = 104), downstream 8 bp two-strand propagation: `PLL = Σ_i log P(base_i | context + allele + bases<i>)`, `delta_PLL = PLL(alt) − PLL(ref)`; 32 generate calls per variant, 0 failures. delta_PLL median −0.876; Score A↔B sign agreement 87%; **strand consistency 65% (68/104), fwd/rc r ≈ 0.13**, indicating limited double-strand convergence; Tier C treated as hypothesis set, not stable-ranked list;
- **Score C (multi-seed stability) empirically degenerate**: pilot 10 variants × 5 seeds all sd = 0: the hosted endpoint returns identical logits regardless of random_seed (seed affects sampling only, not the log-probabilities used by Score A); multi-seed stability vacuous, full run was not performed; strand consistency + external QTL replication used as stability evidence.

**6.4 eQTL/GWAS merge and Tier assignment.** Sources (validated live 2026-09-18): **GTEx REST v2** (`singleTissueEqtl`, tissues Muscle_Skeletal, Adipose_Subcutaneous, Adipose_Visceral_Omentum, Whole_Blood; min p across tissues) + **GWAS Catalog REST** (per-rsid; p = mantissa × 10^exponent). OpenGWAS and eQTL Catalogue endpoints returned 404 in this environment and were recorded and dropped. Tier rules: A = Evo2 perturbation (|Score A| ≥ 4 OR Score B strand-consistent) AND GTEx p < 1e-4 AND GWAS p < 5e-8; B = perturbation AND (GTEx OR GWAS above threshold); C = perturbation only (exploratory); External-only = external evidence strong but Evo2 mild; Excluded = neither. Distribution (432): **A = 0, B = 0, C = 97, External-only = 9, Excluded = 326**. Tier A/B are empty because the high-perturbation shortlist is dominated by rare variants; GTEx eQTLs are computed for common variants only and GWAS Catalog coverage of these rsids is sparse, so Evo2 perturbation and external support barely overlap. The 9 External-only are strongly supported common loci (TNF rs1800629: GTEx p ≈ 7e-24 + GWAS p ≈ 3e-28; IL6 rs1800795: GTEx p ≈ 3.5e-100 + GWAS p ≈ 2e-25, plus rs1799724, rs361525, rs1800630, rs2069830) with mild |Score A|. **Main-figure gate**: the "stable ref/alt Evo2 perturbation supported by at least one public QTL/GWAS source" criterion is unmet because of the rare-variant overlap gap; **Evo2 stays a supplementary/exploratory module; NOT a main figure**; Figure 6 keeps pipeline + composition panels; a scored-variant panel belongs in a supplement.

**6.5 Evo2 boundary.** Evo2 scores support regulatory-hypothesis prioritization only: no causality, no clinical-risk prediction, no replacement of experimental validation (basis for future MPRA/CRISPRi).

### 7. Software, reproducibility and ethical boundaries

All analysis code is available at https://github.com/ENSEI0713/nampt-axis-transcriptomics and archived at Zenodo (https://doi.org/10.5281/zenodo.22865789). All public data are cited by GEO accession (Supplementary Data 1), with download dates recorded. Main computation: Python 3 (NumPy/SciPy-type z-score, paired statistics, DL meta); Cronbach α by standard formula (gene × sample matrix within dataset); Evo2 scoring via NVIDIA hosted endpoint. Processed matrices, score tables and figure-source data are archived at Zenodo alongside the code (DOI: 10.5281/zenodo.22865789); third-party raw data are cited by accession and not redistributed. **Ethical/use boundary**: public-data secondary analysis, no individual intervention; public transcriptomic data must not be used for individual diagnosis or exercise prescription; NAMPT mRNA status ≠ eNAMPT protein or NAD metabolites; eNAMPT directionality is a testable prediction (obesity → inflammatory program; training → repair markers), pending protein/metabolite validation.



---

## Data Availability

All public datasets analysed in this study are available from the Gene Expression Omnibus (GEO) under the following accessions: GSE312393, GSE305038, GSE292369, GSE318937, GSE32575, GSE272133, GSE294150 and GSE282850 (Supplementary Data 1). Derived score tables, module-level statistics and Evo2 candidate/scoring outputs that support the findings of this study are provided as Supplementary Data 1–8 and archived at Zenodo (https://doi.org/10.5281/zenodo.22865789). 
## Code Availability

All analysis code (public-data audit, NAMPT-axis scoring, meta-analysis, module-consistency, cell-composition proxy, Phase 1b sensitivity, Evo2-40B candidate construction/scoring and eQTL/GWAS merge) is available at https://github.com/ENSEI0713/nampt-axis-transcriptomics and archived at Zenodo (https://doi.org/10.5281/zenodo.22865789). Evo2-40B inference was performed through the NVIDIA-hosted generate endpoint; no custom model weights are required.

## References

1. Brixi, G. et al. Genome modeling and design across all domains of life with Evo 2. Nature (2026). doi:10.1038/s41586-026-10176-5.
2. Aguet, F. et al. (GTEx Consortium). The GTEx Consortium atlas of genetic regulatory effects across human tissues. Science 369, 1318–1330 (2020).
3. Buniello, A. et al. The NHGRI-EBI GWAS Catalog of published genome-wide association studies, targeted arrays and summary statistics 2019. Nucleic Acids Res. 47, D1005–D1012 (2019).
4. Cronbach, L. J. Coefficient alpha and the internal structure of tests. Psychometrika 16, 297–334 (1951).
5. Kovac, L. et al. Different effects of bariatric surgery on epigenetic plasticity in skeletal muscle of individuals with and without type 2 diabetes. Diabetes Metab. 50, 101561 (2024). [GSE272133]
6. Gries, K. J. et al. A single day of reduced activity alters the next day's transcriptomic and metabolic exercise response. Am. J. Physiol. Endocrinol. Metab. 330, E26–E37 (2026). [GSE305038]
7. Hulsmans, M. et al. Interleukin-1 receptor-associated kinase-3 is a key inhibitor of inflammation in obesity and metabolic syndrome. PLoS One 7, e30414 (2012). [GSE32575]
8. Beiter, T. et al. The acute, short-, and long-term effects of endurance exercise on skeletal muscle transcriptome profiles. Int. J. Mol. Sci. 25, 2881 (2024). [GSE312393]
9. Mosquera-Lopez, E. et al. Acute nutritional ketosis during early recovery from aerobic exercise does not affect skeletal muscle transcriptomic response in humans. Eur. J. Appl. Physiol. 126, 1021–1032 (2025). [GSE292369]
10. Lanfranchi, C. et al. Oleuropein-based olive leaf extract enhances muscle mitochondrial bioenergetics response to moderate – but not maximal – intensity exercise in humans. J. Physiol. 604, 3802–3824 (2026). [GSE318937]
11. DerSimonian, R. & Laird, N. Meta-analysis in clinical trials. Control. Clin. Trials 7, 177–188 (1986).
12. Nishino, K. et al. Functional dissection of metabolic trait-associated gene regulation in steady state and stimulated human skeletal muscle cells. Preprint at bioRxiv (2024). doi:10.1101/2024.11.28.625886. [GSE282850]
13. Semerena, E., Nencioni, A. & Masternak, K. Extracellular nicotinamide phosphoribosyltransferase: role in disease pathophysiology and as a biomarker. Front. Immunol. 14, 1268756 (2023).
14. Dakroub, A. et al. Visfatin: a possible role in cardiovasculo-metabolic disorders. Cells 9, 2444 (2020).
15. Jiang, Z. et al. NAD+ homeostasis and its role in exercise adaptation: a comprehensive review. Free Radic. Biol. Med. 225, 346–358 (2024).
16. Benjamini, Y. & Hochberg, Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. J. R. Stat. Soc. Ser. B 57, 289–300 (1995).

## Figure Legends

### Figure 1 | State-dependent NAMPT-axis framework.
**a**, Dual identity of NAMPT: intracellular NAMPT supports NAD salvage and repair; extracellular NAMPT (eNAMPT/visfatin) is linked to NF-κB and monocyte/macrophage activation. **b**, The state-dependent axis model: the same NAMPT upregulation can be inflammation-like or repair-like depending on tissue, time and metabolic background. **c**, Multi-layer public-data evidence base (9 transcriptomic units, 337 samples; exercise, obesity/weight-loss, cell model). **d**, Repair-program genes (NAD salvage, sirtuin, mitochondrial, DNA-repair modules). **e**, Inflammatory-program genes (NF-κB, innate immune, monocyte/macrophage modules). **f**, Balance score (repair − inflammatory) across representative states.

### Figure 2 | Public transcriptomic evidence base and analysis design.
**a**, NAMPT-axis gene coverage across the 9 analysis units (59-gene axis; most datasets 100%, GSE305038 84.7%, GSE282850 79.7%). **b**, Analysis design: predefined contrasts by layer (exercise, obesity, cell model). **c**, Evidence density by axis metric: number of contrasts with CI excluding 0 and with FDR < 0.10.

### Figure 3 | Exercise-induced NAMPT axis: acute stress and training adaptation.
**a**, NAMPT_z, inflammatory, repair and balance scores across exercise cohorts (13 contrasts plotted: 12 paired contrasts plus one unpaired acute-24 h comparison; 4 datasets). The unpaired display contrast is descriptive and is not included in the paired meta-analysis. **b**, Immediate stress bias relaxes by 24 h (GSE318937 immediate vs 24h). **c**, Dataset-level summaries; acute inflammation-like signal mainly driven by NF-κB/cytokine modules (Phase 1b consistency).

### Figure 4 | Random-effects meta-analysis of the exercise NAMPT axis.
**a**, Pooled effects by stratum and metric (contrast-level DerSimonian–Laird: NAMPT_z +0.85, 95% CI 0.53–1.17, p = 1.8e-7; balance −0.62, p = 0.016; inflammatory +0.28, ns; repair −0.33, p = 0.05) with I² and τ². **b**, Per-contrast forest plot for exercise/NAMPT_z (12 contrasts); cluster-aware dataset-level estimate (k = 4, +0.965) and leave-one-dataset-out sensitivity are shown.

### Figure 5 | Obesity and weight loss: tissue- and disease-background dependence of the NAMPT axis.
**a**, Obesity-layer meta (k = 3, directional): NAMPT_z +0.14; inflammatory +0.57. **b**, Post-bariatric monocyte remodeling (GSE32575): inflammatory and repair scores rise together post-surgery. **c**, Skeletal-muscle response by metabolic-disease status (GSE272133): T2D post-surgery repair score +0.30.

### Figure 6 | Evo2-40B regulatory-variant prioritization.
**a**, Prioritization workflow: Ensembl REST candidate build (12,961 → 432 functional variants within TSS ±2 kb of NAMPT/CD38/BST1/SIRT1/SIRT3/SIRT6/IL6/TNF), GRCh38 (hg38) ref/alt 2 kb windows, Evo2-40B scoring (Score A allele surprisal; Score B pseudo-likelihood), GTEx/GWAS Catalog merge and Tier assignment. **b**, Candidate-set composition (n = 432 by gene window; NAMPT 12, CD38/BST1/SIRT1/SIRT3/SIRT6/IL6/TNF 60 each). **c**, Tier distribution (A = 0, B = 0, C = 97, External-only = 9, Excluded = 326). Evo2 is reported as an exploratory supplementary module, not as a validated mechanistic main result.

## End Notes

**Acknowledgements.** The authors thank the contributors of the public datasets analysed (see Data Availability). No funding was received for this study.

**Author contributions.** Y.C. conceived the study, performed the analyses and drafted the manuscript; Y.Z. supervised the study and revised the manuscript; Z.S. and M.Z. contributed to data interpretation and manuscript revision. All authors approved the final version.

**Competing interests.** The authors declare no competing interests.
