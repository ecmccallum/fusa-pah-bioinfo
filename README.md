# Fusarium solani PAH Bioinformatics

Documented bioinformatics workflow for identifying candidate genes potentially involved in PAH transformation or degradation in a Fusarium solani strain. All analysis runs on the UPPA Pyrene HPC cluster.

**Live reports:** [ecmccallum.github.io/fusa-pah-bioinfo](https://ecmccallum.github.io/fusa-pah-bioinfo/)

**Organism:** Fusarium solani species complex
**Data:** Paired-end Illumina, 150 bp, ~47.2 million reads, ~62x coverage
**Platform:** UPPA Pyrene HPC cluster
**Status:** Stage 1 in progress

## Pipeline Stages

| Stage | Description | Status |
|-------|-------------|--------|
| 1 | Quality control and read cleaning | In progress |
| 2 | Contamination screening (Kraken2) | Pending |
| 3 | De novo genome assembly | Pending |
| 4 | Assembly quality control | Pending |
| 5 | Gene prediction and annotation | Pending |
| 6 | Functional annotation and PAH candidates | Pending |

## Environment

All analysis runs within a conda environment (`fusarium_env`) on the UPPA Pyrene HPC cluster. Full setup details and confirmed tool versions are documented in [docs/environment_setup.md](docs/environment_setup.md).

## Contamination Note

A secondary GC peak at 67-69% was identified during QC and confirmed by BLAST as Methylorubrum populi, a methylotrophic bacterium commonly found in fungal cultures. Kraken2 will be used to classify and filter reads before assembly.

## Reference Genome

NCBI accession GCF_023522795.1 (NDSU_Fsol_1.0), 19 sequences, 59.4 Mb, N50 4.0 Mb.

## Important Note

Candidate enzymes identified through this workflow are hypotheses only. Confirmation requires expression data, enzyme assays, or functional validation.
