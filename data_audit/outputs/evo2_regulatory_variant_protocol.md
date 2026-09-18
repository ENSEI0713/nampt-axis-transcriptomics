# Evo2-40B regulatory-variant protocol for the NAMPT-NAD inflammatory-repair axis

## 1. Scientific role of Evo2-40B

This project should use Evo2-40B as a sequence-level regulatory prior, not as a clinical prediction model. The biological question is whether inherited or acquired regulatory sequence contexts near NAMPT-axis genes help explain why NAMPT-associated biology sometimes appears as inflammatory load and sometimes as adaptive repair.

The defensible claim is: Evo2-40B can prioritize regulatory variants or enhancer contexts whose reference and alternate sequences are predicted to differ in genomic plausibility under local DNA context. These candidates then need support from public regulatory evidence, eQTL/GWAS evidence, and expression-state evidence before being discussed as mechanistic hypotheses.

## 2. Inputs and outputs

### Inputs

- NAMPT-axis gene list: `data_audit/outputs/NAMPT_axis_gene_set_v1.csv`.
- Candidate variants from public genetic resources: GWAS Catalog, OpenGWAS, FinnGen, GTEx, eQTL Catalogue, eQTLGen and tissue-specific QTL resources.
- Regulatory annotations: ENCODE, Roadmap Epigenomics, FANTOM5, GTEx epigenomics, ABC enhancer-gene links where available, and GSE247455 skeletal-muscle snRNA/snATAC/QTL/MPRA resources.
- GRCh38 reference genome sequence.
- Tissue/cell context labels: skeletal muscle, adipose tissue, monocytes/macrophages, PBMC/whole blood and human skeletal muscle cells.

### Outputs

- A ranked variant table with genomic location, ref/alt allele, linked gene, tissue regulatory evidence, trait/eQTL evidence, Evo2 score and final evidence tier.
- Ref/alt FASTA windows and BED files for reproducibility.
- Per-call JSON logs containing Evo2 endpoint, model name, parameters, sequence window metadata and score calculation details.
- A short list of variants/enhancers suitable for MPRA, CRISPRi/a or allele-specific reporter validation.

## 3. Candidate gene and region definition

### Gene modules

- Core NAMPT/NAD salvage: `NAMPT`, `NMNAT1`, `NMNAT2`, `NMNAT3`, `NAPRT`, `NADSYN1`, `QPRT`.
- NAD consumption and repair: `CD38`, `BST1`, `PARP1`, `PARP2`, `SIRT1`, `SIRT3`, `SIRT6`.
- Exercise/mitochondrial repair: `PRKAA1`, `PRKAA2`, `PPARGC1A`, `TFAM`, `NRF1`, `NFE2L2`, `SOD2`, `CAT`, `GPX1`, autophagy and DNA-repair genes.
- Inflammation/NF-kB/innate immunity: `NFKB1`, `RELA`, `TNF`, `IL6`, `IL1B`, `CCL2`, `CXCL8`, `TLR4`, `NLRP3`, `CASP1`, monocyte/macrophage markers.

### Variant search regions

- Primary cis-regulatory window: gene body plus 250 kb upstream/downstream of each NAMPT-axis gene.
- Expanded window: distal enhancer-gene links from ABC, promoter-capture Hi-C, eQTL colocalization or MPRA data when available.
- Coding variants are retained only as a separate sensitivity set, because the main Evo2 hypothesis here is regulatory rather than protein coding.

## 4. Public variant evidence sources

### Trait sources

Prioritize variants associated with the following traits:

- Obesity and adiposity: BMI, waist-hip ratio, body-fat percentage, severe obesity and weight-loss response.
- Low-grade inflammation: CRP, IL-6, TNF-related traits, leukocyte counts and monocyte-related traits.
- Metabolic disease: fasting glucose, fasting insulin, insulin resistance, type 2 diabetes and lipid traits.
- Exercise/fitness: physical activity, cardiorespiratory fitness, VO2max, grip strength, muscle mass and recovery-related traits where available.

### Molecular QTL sources

- GTEx for skeletal muscle, whole blood, adipose subcutaneous and adipose visceral eQTL/sQTL.
- eQTL Catalogue and eQTLGen for immune-cell and blood expression evidence.
- Tissue-specific chromatin QTL, caQTL, mQTL or MPRA resources where available.
- GSE247455 should be used as a high-value skeletal-muscle regulatory benchmark because it includes single-cell/nucleus regulatory information and MPRA-related evidence.

## 5. Variant filtering and harmonization

### Inclusion criteria

- Variant maps unambiguously to GRCh38 with known ref and alt alleles.
- Variant lies within a NAMPT-axis cis window or a supported distal regulatory element linked to an axis gene.
- Variant overlaps at least one regulatory feature in a relevant tissue or cell type: promoter, enhancer, ATAC peak, H3K27ac/H3K4me1/H3K4me3 region, TF motif or MPRA-tested element.
- Variant has at least one external biological signal: GWAS association, eQTL/sQTL/caQTL/mQTL evidence, fine-mapping posterior probability, or LD with a reported lead variant.

### Exclusion criteria

- Ambiguous alleles that cannot be strand-harmonized.
- Variants in repetitive or low-mappability regions unless there is strong independent regulatory evidence.
- Variants with no tissue relevance and no link to NAMPT-axis genes.
- Clinical pathogenicity claims without clinical-grade evidence.

## 6. Sequence-window construction

For each candidate variant, construct matched reference and alternate sequences from GRCh38.

- Standard windows: 2 kb, 8 kb and 32 kb centered on the variant.
- Allele insertion: replace only the variant allele while keeping all flanking bases identical.
- Strand handling: score both forward sequence and reverse complement, then average or report strand sensitivity.
- Ambiguous bases: exclude windows with `N` at or near the variant; record the exclusion reason.
- Coordinates: store chromosome, 1-based position, ref, alt, window start, window end and genome build.

## 7. Evo2-40B scoring plan

### Hosted endpoint

The tested hosted endpoint is:

```text
https://health.api.nvidia.com/v1/biology/arc/evo2-40b/generate
```

The endpoint accepts DNA sequence prompts and can return generated sequence, logits and sampled probabilities. Existing smoke-test logs show per-position logits over a 512-token vocabulary, with DNA bases represented by ASCII-like token indices for `A`, `C`, `G` and `T`.

API credentials must be supplied only through environment variables such as `NVIDIA_API_KEY` or `NVCF_RUN_KEY`. Do not write API keys to scripts, notebooks, logs, command history or manuscript files.

### Score A: allele surprisal at the variant

Use the upstream flank as a prompt and request one generated token with logits enabled. Convert logits for `A/C/G/T` into a DNA-normalized probability distribution:

```text
P(base | upstream flank) = softmax(logit_A, logit_C, logit_G, logit_T)
```

Then calculate:

```text
delta_surprisal = log P(alt allele | upstream flank) - log P(ref allele | upstream flank)
```

A large absolute value means the alternate allele changes the model's expected local genomic continuation. The sign should not be interpreted as beneficial or harmful by itself.

### Score B: local pseudo-likelihood propagation

For a stronger but more API-expensive score, calculate the probability of observed downstream bases after inserting the ref or alt allele. This can be approximated by iterative one-token calls:

```text
PLL(sequence) = sum_i log P(observed downstream base_i | upstream + allele + previous observed downstream bases)
delta_PLL = PLL(alt window) - PLL(ref window)
```

Run the same scoring on the reverse complement to reduce direction bias.

### Score C: perturbation stability

For selected top variants, run multiple random seeds and temperatures to test whether the ref/alt difference is stable. This is a sensitivity check, not the main score.

### Fallback if hosted scoring is insufficient

If the hosted generate endpoint does not expose robust forced likelihood for the required scale, use one of these fallbacks:

- Run a local Evo2/NIM model that exposes input-token log-likelihoods.
- Prototype the same scoring pipeline on a smaller open Evo2 model, then rerun top candidates on Evo2-40B.
- Keep Evo2 as a candidate-ranking layer only and require stronger eQTL/MPRA support for every reported variant.

## 8. Multi-evidence integration

Each candidate variant should receive an evidence tier rather than a single black-box score.

### Evidence features

- Trait evidence: GWAS p value, fine-mapping posterior probability or LD with lead variant.
- Molecular evidence: eQTL/sQTL/caQTL/mQTL association with a NAMPT-axis gene.
- Regulatory evidence: overlap with tissue-specific promoter/enhancer/ATAC/histone-mark/MPRA element.
- Expression-state evidence: linked gene belongs to the inflammatory, repair or both NAMPT-axis score group and changes in public exercise/obesity datasets.
- Evo2 evidence: absolute ref/alt sequence perturbation score and strand consistency.

### Proposed evidence tiers

- Tier A: Evo2 perturbation plus same-tissue eQTL or MPRA evidence plus trait association plus regulatory overlap.
- Tier B: Evo2 perturbation plus two independent external evidence types.
- Tier C: Evo2 perturbation plus one external evidence type, reported only as exploratory.
- Excluded: Evo2-only candidates with no public biological support.

## 9. Manuscript claim boundary

Evo2 scores can support regulatory hypotheses. They cannot establish eNAMPT protein secretion, clinical inflammatory status, exercise safety, causal disease risk or personalized exercise prescription. Any claim about eNAMPT specifically requires protein, secretion, plasma/serum biomarker, proteomic or validated literature evidence. Any claim about causality requires genetic colocalization, perturbation data or experimental validation.

## 10. Reproducibility checklist

- Record data source, accession, genome build and download date for every public resource.
- Keep raw variant tables, harmonized variant tables, BED files and FASTA windows.
- Log Evo2 endpoint, model name, parameters, sequence length, strand, random seed and response schema.
- Store only metadata and scores, never API keys.
- Publish code and processed result tables in a repository with a persistent identifier, such as Zenodo, OSF or Figshare, while keeping reused GEO/SRA/GTEx/ENCODE data cited by accession rather than redistributed when licence terms require it.

## 11. Minimal result needed for the paper

For the Evo2 module to be worth a main figure, the analysis should identify a compact set of NAMPT-axis regulatory candidates that satisfy all of the following:

- linked to `NAMPT` or another high-priority NAMPT-axis gene;
- located in a relevant skeletal muscle, adipose or immune regulatory element;
- supported by at least one public QTL or GWAS source;
- shows a stable ref/alt Evo2 perturbation score;
- connects to a gene whose expression belongs to the inflammatory or repair axis in the public transcriptomic analysis.

If this bar is not met, Evo2 should move to a supplementary exploratory figure rather than the main claim.
