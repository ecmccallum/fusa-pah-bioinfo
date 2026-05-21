# PAH Candidate Gene Search — Python Script Plan

## Purpose
After Funannotate annotation is complete, a Python script will parse the annotation 
output files and identify candidate genes potentially involved in PAH transformation 
or degradation in *Fusarium solani*. All candidates are hypotheses only — confirmation 
requires expression data, enzyme assays, or functional validation.

---

## Input Files (Funannotate output)
The script will parse one or more of the following output files:

| File | Contents |
|------|----------|
| `annotations.txt` | Tab-delimited gene annotations |
| `annotations.gff3` | Gene feature file with functional annotations |
| `proteins.fasta` | Predicted protein sequences |
| `interproscan.xml` | InterProScan domain annotations |
| `eggnog.annotations` | eggNOG ortholog and pathway assignments |

*Exact filenames to be confirmed once Funannotate has run.*

---

## Target Gene Families

### Oxidative enzymes — initial PAH attack
| Gene Family | Search Terms | Pfam Domains |
|-------------|-------------|--------------|
| Cytochrome P450 monooxygenases (CYPs) | CYP, cytochrome P450, monooxygenase | PF00067 |
| Laccases | laccase, multicopper oxidase | PF00394, PF07731, PF07732 |
| Manganese peroxidases (MnP) | manganese peroxidase, MnP | PF01036 |
| Lignin peroxidases (LiP) | lignin peroxidase, LiP | PF01036 |
| Dye-decolourising peroxidases (DyP) | DyP, dye decolourising peroxidase | PF04261 |

### Downstream metabolism
| Gene Family | Search Terms | Pfam Domains |
|-------------|-------------|--------------|
| Epoxide hydrolases | epoxide hydrolase | PF00561 |
| FAD-dependent monooxygenases | FAD monooxygenase, flavin monooxygenase | PF00743 |
| Dioxygenases | dioxygenase, ring cleavage | PF00775 |

### Detoxification and conjugation
| Gene Family | Search Terms | Pfam Domains |
|-------------|-------------|--------------|
| Glutathione S-transferases (GSTs) | glutathione S-transferase, GST | PF02798, PF00043 |
| UDP-glucuronosyltransferases | UDP-glucuronosyltransferase, UGT | PF00201 |

### Transport
| Gene Family | Search Terms | Pfam Domains |
|-------------|-------------|--------------|
| ABC transporters | ABC transporter, ATP-binding cassette | PF00005 |
| MFS transporters | major facilitator, MFS transporter | PF07690 |

### Stress response
| Gene Family | Search Terms | Pfam Domains |
|-------------|-------------|--------------|
| Superoxide dismutases | superoxide dismutase, SOD | PF00080 |
| Catalases | catalase | PF00199 |

---

## Search Strategy
The script will use **three complementary approaches** to avoid missing candidates:

**1. Keyword search**
Search annotation text fields for gene family names and synonyms.
Flexible but may produce false positives — needs filtering.

**2. Pfam domain search**
Search InterProScan output for known domain accessions (PF numbers above).
More specific than keyword search — catches distant homologs BLAST might miss.

**3. KEGG pathway search**
Search eggNOG output for relevant KEGG pathway assignments.
Useful for contextualising candidates in metabolic pathways.

*All three approaches will be combined and deduplicated into a final candidate list.*

---

## Output
The script will produce:

- `pah_candidates.tsv` — tab-delimited table of all candidates with gene ID, 
annotation, domain hits, search method that identified it
- `pah_candidates_summary.txt` — count of candidates per gene family
- `pah_candidates.fasta` — protein sequences of all candidates for downstream 
phylogenetic analysis or BLAST

---

## Important Caveats
- Keyword-based searches alone are fragile — a gene annotated as "hypothetical 
protein" will be missed even if it has a CYP domain
- Domain searches are more sensitive but Pfam accessions must be verified against 
the actual InterProScan version used
- All candidates require manual review before being reported
- No candidate should be described as a "PAH-degrading enzyme" — use 
"candidate gene potentially involved in PAH transformation" throughout

---

## Status
⏳ Pending — will be written after Funannotate annotation is complete (Stage 5)
