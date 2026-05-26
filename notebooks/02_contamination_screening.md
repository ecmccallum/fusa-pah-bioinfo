# Stage 2: Contamination Screening

**Date:** 21 May 2026
**Operator:** E. McCallum
**Platform:** UPPA Pyrene HPC cluster
**Environment:** fusarium_env
**Tools:** Kraken2 v2.17.1, extract_kraken_reads.py

---

## 2.1 Overview

Trimmed paired-end reads from Stage 1 were screened for contamination using Kraken2 taxonomic classification. A pre-built 8GB standard Kraken2 database was downloaded and used to classify all reads against known reference sequences. Reads classified as non-fungal were removed, and the remaining unclassified reads were retained as the clean dataset for genome assembly at Stage 3.

---

## 2.2 Rationale

FastQC analysis at Stage 1 identified a secondary GC peak at approximately 67–69%, inconsistent with the expected GC content of *Fusarium solani* (~52%). Previous BLAST screening had indicated the likely presence of *Methylorubrum populi*, a high-GC methylotrophic bacterium commonly associated with fungal cultures. Kraken2 was used to systematically classify and quantify reads by taxonomic origin and to separate *Fusarium*-associated reads from contaminant reads prior to assembly.

---

## 2.3 Database

A pre-built Kraken2 standard database (8GB) was downloaded from the Genome Index repository and extracted to the home directory on the Pyrene cluster.

```bash
mkdir -p ~/kraken2_db
cd ~/kraken2_db
wget https://genome-idx.s3.amazonaws.com/kraken/k2_standard_08gb_20240904.tar.gz
tar -xvzf k2_standard_08gb_20240904.tar.gz
```

**Database details:**
- Version: k2_standard_08gb_20240904
- Size: 5.54 GB compressed, ~14 GB extracted
- Contents: Bacteria, Archaea, Viruses, Human, UniVec

> **Note:** The 8GB database is a reduced version of the full Kraken2 standard database (~70 GB). It may underestimate contamination levels as it does not contain all reference sequences. Reads not matching any database entry are classified as unclassified and are assumed to represent the target organism (*Fusarium solani*).

---

## 2.4 Kraken2 Classification

Kraken2 was run on the trimmed paired-end reads on a compute node via an interactive SLURM session:

```bash
srun --cpus-per-task=8 --mem=64G --time=06:00:00 --pty bash
conda activate fusarium_env
```

```bash
mkdir -p ~/fusarium_pah/results/kraken2

kraken2 --db ~/kraken2_db \
  --paired \
  --threads 8 \
  --output ~/fusarium_pah/results/kraken2/kraken2_output.txt \
  --report ~/fusarium_pah/results/kraken2/kraken2_report.txt \
  ~/fusarium_pah/data/trimmed/fusa_1_trimmed.fq.gz \
  ~/fusarium_pah/data/trimmed/fusa_2_trimmed.fq.gz
```

**Run statistics:**

| Metric | Value |
|--------|-------|
| Total sequences processed | 23,298,174 pairs |
| Total bases processed | 6,988.64 Mbp |
| Processing time | 413.97 seconds |
| Sequences classified | 3,696,473 (15.87%) |
| Sequences unclassified | 19,601,701 (84.13%) |

---

## 2.5 Classification Results

### Summary

| Category | Read pairs | Percentage |
|----------|-----------|------------|
| Unclassified (retained) | 19,601,701 | 84.13% |
| Classified (contamination) | 3,696,473 | 15.87% |

### Contamination breakdown

| Taxon | Reads | % of total |
|-------|-------|------------|
| *Methylorubrum* (genus) | 1,359,981 | 5.84% |
| — *Methylorubrum populi* | 523,344 | 2.25% |
| — *Methylorubrum extorquens* | 388,145 | 1.67% |
| *Methylobacterium* (genus) | 1,051,713 | 4.51% |
| Betaproteobacteria (other) | ~350,000 | ~1.50% |
| Gammaproteobacteria (other) | ~260,000 | ~1.11% |
| Actinomycetota | ~50,000 | ~0.21% |
| Bacillota | ~50,000 | ~0.21% |
| *Homo sapiens* | 5,389 | 0.02% |
| Other | ~620,000 | ~2.66% |

### Interpretation

The dominant contaminant was *Methylorubrum populi* (2.25%) and related *Methylorubrum* species (5.84% total), consistent with the secondary GC peak observed at Stage 1 and with prior BLAST identification. *Methylorubrum* species are methylotrophic Alphaproteobacteria with GC content of ~67–69%, explaining the bimodal GC distribution.

A small number of reads (5,389; 0.02%) were classified as *Homo sapiens*, consistent with routine low-level human DNA contamination during library preparation, commonly observed in sequencing datasets.

The remaining classified reads represent a diverse mixture of environmental bacteria at very low abundance, likely reflecting trace environmental contamination during culture or library preparation.

**Important caveat:** The 8GB database does not include *Fusarium solani* or most fungal reference genomes. Consequently, genuine *Fusarium* reads will appear as unclassified. The 84.13% unclassified fraction is therefore expected to represent primarily *Fusarium* sequence, but may still contain a small proportion of undetected bacterial contamination not represented in the database. Any residual contamination will be assessed post-assembly by screening contigs by GC content and coverage.

---

## 2.6 Read Extraction

Unclassified reads (taxid 0) were extracted using extract_kraken_reads.py to produce the clean paired-end files for assembly:

```bash
mkdir -p ~/fusarium_pah/data/decontaminated

extract_kraken_reads.py \
  -k ~/fusarium_pah/results/kraken2/kraken2_output.txt \
  -r ~/fusarium_pah/results/kraken2/kraken2_report.txt \
  -s1 ~/fusarium_pah/data/trimmed/fusa_1_trimmed.fq.gz \
  -s2 ~/fusarium_pah/data/trimmed/fusa_2_trimmed.fq.gz \
  -o ~/fusarium_pah/data/decontaminated/fusa_1_clean.fq.gz \
  -o2 ~/fusarium_pah/data/decontaminated/fusa_2_clean.fq.gz \
  --taxid 0 --include-children \
  --fastq-output
```

**Extraction results:**

| Metric | Value |
|--------|-------|
| Read IDs saved | 19,601,701 |
| Reads written to fusa_1_clean.fq.gz | 19,601,701 |
| Reads written to fusa_2_clean.fq.gz | 19,601,701 |
| Output file size (each) | 6.9 GB |

---

## 2.7 Output Files

| File | Location |
|------|----------|
| Kraken2 classification output | `results/kraken2/kraken2_output.txt` |
| Kraken2 report | `results/kraken2/kraken2_report.txt` |
| Clean reads R1 | `data/decontaminated/fusa_1_clean.fq.gz` |
| Clean reads R2 | `data/decontaminated/fusa_2_clean.fq.gz` |

---

## 2.8 Conclusions

Kraken2 classification identified 15.87% of trimmed reads as bacterial contamination, dominated by *Methylorubrum populi* and related Alphaproteobacteria. This is consistent with the secondary GC peak at 67–69% observed in FastQC reports at Stage 1, confirming the contamination identified by prior BLAST screening.

After extraction of unclassified reads, 19,601,701 read pairs (84.13% of the trimmed dataset) were retained as the clean dataset. These reads represent the putative *Fusarium solani* fraction and are ready for de novo genome assembly at Stage 3.

Residual contamination not represented in the 8GB database may be present at low levels and will be assessed post-assembly by examining contig GC content and coverage distribution.

The files `fusa_1_clean.fq.gz` and `fusa_2_clean.fq.gz` are ready for genome assembly using SPAdes.
