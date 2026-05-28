# Fusarium solani PAH Bioinformatics
A documented bioinformatics workflow for identifying candidate genes potentially 
involved in PAH (polycyclic aromatic hydrocarbon) transformation or degradation 
in a *Fusarium solani* strain isolated from PAH-contaminated soil.

## 🌐 Live Project Site
**[ecmccallum.github.io/fusa-pah-bioinfo](https://ecmccallum.github.io/fusa-pah-bioinfo/)**

All stage notebooks, QC reports, FastQC, MultiQC, fastp and Kraken2 outputs are 
live and browsable on the project site above.

## Project Overview
| | |
|---|---|
| **Organism** | *Fusarium solani* species complex |
| **Data** | Paired-end Illumina, 150 bp, ~47.2 million reads, ~62x coverage |
| **Platform** | UPPA Pyrene HPC cluster |
| **Goal** | Identify candidate PAH-related genes through de novo assembly and functional annotation |

## Pipeline Progress
| Stage | Description | Status |
|-------|-------------|--------|
| 1 | Quality control and read cleaning | ✅ Complete |
| 2 | Contamination screening (Kraken2) | ✅ Complete |
| 3 | De novo genome assembly (SPAdes) | ✅ Complete |
| 4 | Assembly quality control (QUAST/BUSCO) | ✅ Complete |
| 5 | Gene prediction and annotation (Funannotate) | 🔄 In progress |
| 6 | PAH candidate gene identification | ⏳ Pending |

## Key Findings So Far

### Stages 1–2: Quality Control and Contamination Screening
- Secondary GC peak at 67–69% identified in raw reads and confirmed as 
  *Methylorubrum populi* contamination via FastQC, BLAST and Kraken2
- ~36% of raw reads assigned to *Methylorubrum populi*; 84.13% of trimmed reads 
  classified as *Fusarium* (unclassified reads expected — fungal genomes absent 
  from Kraken2 bacterial database)
- 19,601,701 clean read pairs passed to assembly

### Stages 3–4: Assembly and Quality Assessment
- SPAdes assembly completed after OOM resolution on `midmem` partition (200G RAM)
- Assembly size: **57.4 Mb** (consistent with published *F. solani* genomes, ~50–60 Mb)
- N50: **635,698 bp** — outstanding for an Illumina-only fungal assembly
- Largest contig: **2.88 Mb** | L50: **24 contigs** | GC: **53.63%**
- BUSCO completeness: **99.4%** against *hypocreales_odb10* (4,494 BUSCOs)
- 6.9% of complete BUSCOs contain internal stop codons — likely frameshifts from 
  residual *M. populi* reads; noted as a limitation, does not affect annotation quality

## Assembly Statistics
| Metric | Value |
|--------|-------|
| Total length (≥ 500 bp) | 57.4 Mb |
| # contigs (≥ 500 bp) | 4,308 |
| Largest contig | 2.88 Mb |
| N50 | 635,698 bp |
| L50 | 24 contigs |
| GC content | 53.63% |
| N's per 100 kbp | 4.79 |
| BUSCO completeness | 99.4% (C:99.4% [S:98.7%, D:0.7%], F:0.1%, M:0.5%) |

## Reference Genome
NCBI accession [GCF_023522795.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_023522795.1/) 
(NDSU_Fsol_1.0) — 19 sequences, 59.4 Mb, N50 4.0 Mb

## Environment
All analysis runs within a conda environment (`fusarium_env`) on the UPPA Pyrene 
HPC cluster. Confirmed tool versions and full setup details are documented in 
[docs/environment_setup.md](docs/environment_setup.md).

## Important Note
All candidate genes identified through this workflow are hypotheses only. 
Confirmation requires expression data, enzyme assays, or functional validation 
experiments. Genome sequencing alone cannot confirm enzyme function.
