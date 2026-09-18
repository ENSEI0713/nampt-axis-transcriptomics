# First-pass feasibility report

## Working manuscript axis

Working title: Public multi-omic and sequence-model dissection of the NAMPT-NAD inflammatory repair axis in obesity and exercise adaptation.

One-sentence argument: In human obesity and exercise adaptation, we will test whether the NAMPT-NAD system behaves as a state-dependent axis that separates chronic low-grade inflammatory signalling from exercise-induced metabolic repair, using harmonized public omics data and Evo2-40B sequence-level priors for regulatory variants.

## Core scientific problem

NAMPT has an unresolved dual identity. Intracellular NAMPT supports NAD salvage, mitochondrial function, DNA repair, SIRT/AMPK/PGC1A signalling and adaptive stress responses. Extracellular NAMPT, often discussed as visfatin/PBEF/eNAMPT, has been linked to adipose and immune stress, monocyte activation, obesity-associated inflammation and NF-kB-related cytokine biology. The key question is therefore not whether NAMPT is good or bad. The stronger question is whether public human data can resolve when the NAMPT-NAD axis marks inflammatory load and when it marks adaptive repair.

This project should focus on one main direction rather than three disconnected domains. The recommended center is: obesity-related low-grade inflammation and exercise-induced repair/metabolic adaptation. Nutrition metabolism and injury/recovery should be included as mechanistic modules only when they help test the same axis.

## Proposed thesis and innovation points

1. State-dependent NAMPT model. The paper will formalize NAMPT biology as two measurable states: an inflammatory NAMPT program enriched for eNAMPT-associated immune/adipose stress, NF-kB cytokines, CD38/PARP activity and macrophage/monocyte signals; and a repair NAMPT program enriched for intracellular NAD salvage, SIRT/AMPK/PGC1A, oxidative metabolism, mitochondrial remodelling, autophagy and DNA repair.

2. Public-data evidence ladder across perturbations. Instead of relying on a single cohort, the study will build an evidence ladder across exercise challenge, short-term inactivity, nutritional recovery, obesity, bariatric/weight-loss reversal, blood/monocyte immune state, adipose tissue and skeletal muscle. A finding will be considered stronger only if the direction of NAMPT-axis scores is coherent across more than one dataset class.

3. Evo2-40B as a regulatory-prior layer. Evo2-40B should not be framed as a clinical exercise-prescription tool. Its defensible role is to score or prioritize sequence perturbations in regulatory DNA near NAMPT/NAD/inflammation/repair genes. This links population genetics and regulatory genomics to transcriptomic states, and can nominate variants or enhancer contexts for later wet-lab validation.

## Public data screening logic

Search sources used in this first audit:

- NCBI GEO/GDS for human exercise, skeletal muscle, blood/PBMC, obesity, adipose tissue, weight loss, bariatric surgery and muscle damage datasets.
- NCBI PubMed for NAMPT/NAD/exercise/obesity/inflammation literature anchors.
- NCBI SRA for optional exercise microbiome datasets.

Inclusion criteria for main analysis:

- Human samples or human cell models.
- Publicly resolvable GEO/SRA accession or equivalent repository record.
- Relevant tissue or cell state: skeletal muscle, adipose tissue, whole blood, PBMC, CD14+ monocytes or human skeletal muscle cells.
- Perturbation or contrast relevant to the main axis: acute exercise, exercise training, inactivity before exercise, nutrition during recovery, obesity, weight loss, bariatric surgery, insulin resistance or inflammatory state.
- Omics assay compatible with gene-level or regulatory analysis: RNA-seq, microarray, DNA methylation, snRNA/snATAC, MPRA or matched expression/regulatory data.
- Sufficient sample metadata to recover condition, time point, tissue and intervention.

Exclusion or secondary-use criteria:

- Animal-only datasets are mechanistic support only, not primary human evidence.
- Strong disease confounding, such as cancer or severe vascular disease, is excluded from the primary evidence ladder unless the biological question specifically requires it.
- Datasets without downloadable matrix files or usable sample metadata require manual review before use.
- eNAMPT protein claims cannot be inferred from NAMPT mRNA alone. They require plasma/serum protein data, literature anchors or proteomic datasets.

## Main candidate data modules

Exercise skeletal muscle and recovery:

- GSE312393: human muscle RNA-seq after acute eccentric exercise and six-week resistance training. Useful for acute repair and training adaptation.
- GSE318937: human vastus lateralis RNA-seq after moderate continuous or sprint interval exercise with olive leaf extract versus placebo. Strong exercise plus nutrition/supplement interaction.
- GSE305038: human skeletal muscle RNA-seq before and after exercise following normal activity or a day of reduced activity. Strong for safety/adaptation and low activity context.
- GSE292369: human skeletal muscle RNA-seq around cycling exercise with ketone ester versus placebo during recovery. Strong for nutrition recovery.
- GSE270703 and GSE189298: smaller exercise skeletal muscle datasets, useful as secondary confirmation or spatial/cell-context support.

Obesity, immune state and weight-loss reversal:

- GSE32575: CD14+ monocyte transcriptomes from lean controls and obese patients before and after bariatric surgery. Key dataset for low-grade inflammatory immune state.
- GSE328810: blood methylation before and after eight weeks of combined exercise in women with obesity, with body composition and VO2-related metadata. Key obesity plus exercise dataset.
- GSE323980: whole-blood expression in an obesity diet-composition trial. Useful nutrition/obesity supplement, not an exercise core dataset.

Obesity, skeletal muscle and adipose tissue:

- GSE272133: skeletal muscle RNA-seq before and after bariatric surgery in obesity with or without type 2 diabetes. Key for weight-loss reversal in muscle.
- GSE272137: matched skeletal muscle methylation array for GSE272133. Useful epigenetic support.
- GSE294150: visceral adipose tissue RNA-seq from severe obesity undergoing bariatric surgery. Key adipose-state dataset.
- GSE302599: human visceral adipose snRNA-seq. Useful for cell-type context if accessible and ethically/publicly usable.
- GSE329809: abdominal subcutaneous adipose RNA-seq across normal weight, overweight and post-weight-loss groups. Small but relevant.

Regulatory and mechanistic support:

- GSE282850: LHCN-M2 human skeletal muscle cells under differentiation, AICAR and palmitate. Useful for exercise-mimetic versus insulin-resistance-like stimulus.
- GSE247455: human skeletal muscle snRNA/snATAC/QTL/MPRA resource. Useful for regulatory benchmarking and Evo2 validation, not a direct intervention dataset.
- GSE292357 and GSE292517: mouse tendon/AMPK/wheel-running datasets. Mechanistic support for repair/AMPK, not primary evidence.

## Evo2-40B role in the study

Confirmed from the NVIDIA NIM documentation and model page:

- Evo 2 is described as a biological foundation model for long genomic sequences with sensitivity to single-nucleotide changes.
- The hosted endpoint is `https://health.api.nvidia.com/v1/biology/arc/evo2-40b/generate`.
- Generation inputs include `sequence`, `num_tokens`, `temperature`, `top_k`, `top_p`, `random_seed`, `enable_logits`, `enable_sampled_probs` and per-token timing options.
- Documentation notes that only A/C/T/G are meaningful output bases for DNA generation and maps DNA bases to logit indices.

Defensible use in this paper:

- Generate sequence-level priors for regulatory variants in NAMPT-axis genes.
- Compare reference and alternate alleles in matched genomic windows around variants.
- Prioritize variants that are also supported by GWAS/eQTL/caQTL/MPRA or tissue-specific enhancer evidence.
- Use Evo2-derived scores as one evidence layer, not as standalone proof of biological mechanism.

Variant and regulatory evidence sources to integrate later:

- GTEx, eQTL Catalogue and eQTLGen for expression QTLs.
- GWAS Catalog, OpenGWAS or FinnGen for BMI, obesity, CRP, IL6, type 2 diabetes, insulin resistance, physical activity, cardiorespiratory fitness, grip strength and injury/recovery traits where available.
- ENCODE, Roadmap, FANTOM5, GTEx epigenomics and GSE247455 for regulatory regions in skeletal muscle, adipose tissue and immune cells.
- GRCh38 reference sequence for ref/alt sequence windows.

Boundary: the current hosted generate API must be tested with an NVIDIA API key before claiming high-throughput scoring. If direct arbitrary-sequence likelihood or embeddings are not exposed, the fallback is to use output logits/probabilities for controlled sequence perturbation assays, the local NIM container if compute is available, or the open Evo2 implementation with a smaller model for method prototyping.

## Primary analysis plan

1. Build NAMPT-axis gene sets.
   - Inflammatory NAMPT score: NAMPT, CD38, BST1, PARP1, PARP2, NFKB1, RELA, TNF, IL6, IL1B, CCL2 and macrophage/monocyte activation markers.
   - Repair NAMPT score: NAMPT, NMNAT1/2/3, NAPRT, NADSYN1, SIRT1/3/6, PRKAA1/2, PPARGC1A, mitochondrial OXPHOS, autophagy and DNA repair markers.

2. Harmonize expression and methylation data.
   - Download public matrices and sample metadata.
   - Map sample metadata to tissue, intervention, time point and condition.
   - Convert expression to gene-level comparable matrices when possible.
   - Avoid cross-study batch correction for primary claims unless necessary; analyze within-dataset contrasts first, then meta-analyze effect direction.

3. Estimate axis behaviour within each dataset.
   - Test whether exercise increases repair NAMPT score more than inflammatory NAMPT score in healthy muscle.
   - Test whether obesity and monocyte/adipose states show higher inflammatory NAMPT score.
   - Test whether weight loss or exercise training shifts samples from inflammatory toward repair/adaptive states.
   - Test whether nutrition recovery datasets modulate the same axis or mainly leave it unchanged.

4. Integrate regulatory evidence.
   - Identify variants near NAMPT-axis genes that overlap tissue/cell regulatory regions.
   - Rank variants by multi-evidence support: GWAS/eQTL/caQTL/MPRA overlap, tissue relevance, gene expression correlation and Evo2 perturbation score.
   - Nominate a short list of variants/enhancers as mechanistic candidates for future validation.

## Feasibility verdict

Public data are sufficient for a first computational paper that proposes and tests a NAMPT-NAD inflammatory repair axis across public human exercise, obesity and weight-loss datasets. The strongest near-term paper is likely a high-quality computational biology or translational metabolism manuscript, with a possible Nature-family subjournal target if the integration is rigorous and the claims remain calibrated.

Main Nature journal would require a larger decisive element: for example MoTrPAC-scale human multi-omics integration, strong proteomic evidence for circulating NAMPT/NAD-related markers, external population genetic validation, or new experimental validation of Evo2-prioritized regulatory variants. Without that, the work should not overclaim clinical diagnosis, exercise prescription or causal mechanism.

## Immediate next work package

- Finalize curated dataset inventory and gene set v1.
- Download first-priority processed matrices from GEO.
- Parse sample metadata into a harmonized sample table.
- Compute preliminary NAMPT inflammatory and repair scores in three proof-of-concept datasets: GSE32575, GSE312393 and GSE272133.
- Test the Evo2-40B endpoint once an NVIDIA API key is available; record input/output schema and reproducibility limits.
