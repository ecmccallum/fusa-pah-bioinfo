# Fusarium solani PAH Bioinformatics

A documented bioinformatics workflow for identifying candidate genes potentially
involved in PAH (polycyclic aromatic hydrocarbon) transformation, detoxification,
or stress-response pathways in a *Fusarium solani* strain isolated from a
PAH-contaminated environment.

## Live Project Site

**[ecmccallum.github.io/fusa-pah-bioinfo](https://ecmccallum.github.io/fusa-pah-bioinfo/)**

All stage notebooks, QC reports, FastQC, MultiQC, fastp, Kraken2, and annotation
outputs are live and browsable on the project site above.

## Project Overview

| | |
|---|---|
| **Organism** | *Fusarium solani* species complex |
| **Data** | Paired-end Illumina, 150 bp, ~47.2 million reads, ~62x coverage |
| **Platform** | UPPA Pyrene HPC cluster |
| **Goal** | Identify candidate PAH-relevant genes through de novo assembly, functional annotation, and systematic enzyme family screening |

## Pipeline Progress

| Stage | Description | Status |
|-------|-------------|--------|
| 1 | Quality control and read cleaning | Complete |
| 2 | Contamination screening (Kraken2) | Complete |
| 3 | De novo genome assembly (SPAdes) | Complete |
| 4 | Assembly quality control (QUAST/BUSCO) | Complete |
| 5 | Gene prediction and annotation (Funannotate) | Complete |
| 6 | PAH candidate gene identification | In progress — 6.1 complete |

## Key Findings

### Stages 1 and 2: Quality Control and Contamination Screening

- Secondary GC peak at 67 to 69% identified in raw reads and confirmed as
  *Methylorubrum populi* contamination via FastQC, BLAST, and Kraken2
- Approximately 36% of raw reads assigned to *Methylorubrum populi*; 84.13% of
  trimmed reads classified as *Fusarium* (unclassified reads expected — fungal
  genomes are absent from the Kraken2 standard bacterial database)
- 19,601,701 clean read pairs passed to assembly after contamination filtering

### Stages 3 and 4: Assembly and Quality Assessment

- SPAdes assembly completed after OOM resolution on the midmem partition (200G RAM)
- Assembly size: 57.4 Mb (consistent with published *F. solani* genomes, 50 to 60 Mb)
- N50: 635,698 bp — strong contiguity for an Illumina-only fungal assembly
- Largest contig: 2.88 Mb | L50: 24 contigs | GC: 53.63%
- BUSCO completeness: 99.4% against hypocreales_odb10 (4,494 BUSCOs)
- 6.9% of complete BUSCOs contain internal stop codons; this is noted as a limitation
  and may reflect assembly errors, prediction artifacts, pseudogenes, or residual
  contamination. This does not invalidate the overall BUSCO completeness result, but
  it should be considered when interpreting individual gene models.

### Stage 5: Gene Prediction and Functional Annotation

- Funannotate v1.8.17 predict_v2 produced 22,338 predicted protein-coding gene models
  and 341 tRNAs from the 57.4 Mb assembly
- Protein evidence: 62,404 *F. solani* UniProt sequences used as EvidenceModeler input
- Exon/protein evidence overlap: 22.7% in predict_v2 (7.5x improvement over predict_v1)
- BUSCO genome completeness: C:98.3% S:97.0% D:1.3% F:1.0% M:0.7% (dikarya_odb9, n=1,312)
- BUSCO protein completeness: C:97.0% S:97.0% D:0.0% F:0.0% M:3.0%
- Functional annotation added Pfam domains to 15,170 genes, CAZyme annotations to 754
  genes, protease annotations to 760 genes, and UniProt product names to 1,177 genes
- eggNOG, InterProScan, SignalP, and Phobius were unavailable on Pyrene — GO terms,
  KEGG orthology, InterProScan domains, and secretome predictions are absent from the
  Funannotate output; these gaps are addressed in Stage 6 via Galaxy

### Stage 6: PAH Candidate Gene Identification (in progress)

- 6.1 complete: first-pass candidate screen of the annotated GFF3
- 22,338 genes screened using keyword and Pfam domain matching across 33 target families
- The initial screen identified 1,824 candidate hits across 33 target families. Raw hit
  counts are preliminary and require curation, especially broad families such as CYPs,
  SDRs, ALDHs, ABC transporters, and MFS transporters.
- Key preliminary hits: CYP_general 130 (pending stricter PF00067/explicit P450
  filtering), epoxide_hydrolase 77, GST 50, aryl_sulfatase 24, laccase_MCO 19,
  FAD_monooxygenase 10, phenol_monooxygenase 10, manganese_peroxidase 5
- Screening script: scripts/stage6a_candidate_screen.py
- 6.2 through 6.9 pending: curation, protein extraction, Galaxy enrichment, BLAST
  validation, evidence integration, ranked candidate table, and final reporting

## Assembly Statistics

| Metric | Value |
|--------|-------|
| Total length (>= 500 bp) | 57.4 Mb |
| Contigs (>= 500 bp) | 4,308 |
| Largest contig | 2.88 Mb |
| N50 | 635,698 bp |
| L50 | 24 contigs |
| GC content | 53.63% |
| N's per 100 kbp | 4.79 |
| BUSCO genome completeness | C:99.4% S:98.7% D:0.7% F:0.1% M:0.5% (hypocreales_odb10) |
| Predicted genes (funannotate) | 22,338 mRNA, 341 tRNA |
| BUSCO proteins (dikarya_odb9) | C:97.0% S:97.0% D:0.0% F:0.0% M:3.0% |

## Reference Genome

NCBI accession [GCF_023522795.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_023522795.1/)
(NDSU_Fsol_1.0) — 19 sequences, 59.4 Mb, N50 4.0 Mb, 18,900 annotated mRNA gene models

## Environment

All analysis runs on the UPPA Pyrene HPC cluster. Stage 5 uses a dedicated
funannotate_env conda environment built with mamba. Confirmed tool versions and
full setup details are documented in the Stage 5 notebook.

## Important Note

All candidate genes identified through this workflow are hypotheses only. They
represent sequence-similarity and domain-based candidates, not confirmed
PAH-degradation genes. Confirmation requires expression data, enzyme assays,
degradation assays, metabolite detection, or other functional validation experiments.
