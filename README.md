# Fusarium solani PAH Bioinformatics

A documented bioinformatics workflow for identifying candidate genes potentially 
involved in PAH (polycyclic aromatic hydrocarbon) transformation or degradation 
in a *Fusarium solani* strain.

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
| 3 | De novo genome assembly (SPAdes) | 🔄 In progress |
| 4 | Assembly quality control (QUAST/BUSCO) | ⏳ Pending |
| 5 | Gene prediction and annotation (Funannotate) | ⏳ Pending |
| 6 | PAH candidate gene identification | ⏳ Pending |

## Key Findings So Far
- Secondary GC peak at 67-69% identified in raw reads and confirmed as 
*Methylorubrum populi* contamination via FastQC, BLAST and Kraken2
- 84.13% of trimmed reads classified as *Fusarium* (unclassified by Kraken2 
as expected — fungal genomes absent from bacterial database)
- 19,601,701 clean read pairs passed to assembly

## Reference Genome
NCBI accession [GCF_023522795.1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_023522795.1/) 
(NDSU_Fsol_1.0) — 19 sequences, 59.4 Mb, N50 4.0 Mb

## Environment
All analysis runs within a conda environment (`fusarium_env`) on the UPPA Pyrene 
HPC cluster. Confirmed tool versions and full setup details are documented in 
[docs/environment_setup.md](docs/environment_setup.md).

## Important Note
All candidate genes identified through this workflow are hypotheses only. 
Confirmation requires expression data, enzyme assays, or functional validation.
