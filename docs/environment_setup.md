# Environment Setup

## Platform

Cluster: UPPA Pyrene HPC  
Login node: pyrene-login02  
Access method: X2Go remote desktop

## Conda Environment

Environment name: `fusarium_env`

To activate:

    conda activate fusarium_env

To deactivate:

    conda deactivate

## Confirmed Tool Versions

| Tool | Version |
|------|---------|
| FastQC | v0.12.1 |
| fastp | 1.3.3 |
| MultiQC | 1.28 |
| Kraken2 | 2.17.1 |
| SPAdes | v4.2.0 |
| QUAST | v5.3.0 |
| BUSCO | 6.0.0 |

## Notes

All tools verified 20/05/2026. QUAST installed without optional databases (GRIDSS, SILVA, BUSCO). quast-download-busco to be run prior to Stage 4.
