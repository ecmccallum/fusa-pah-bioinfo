# Stage 6 — Target Gene Families: PAH Candidate Search
## *Fusarium solani* Genome Annotation Project

**Last updated:** May 2026  
**Status:** ⏳ Pending — script to be written after `funannotate annotate` is complete  
**Repository:** ecmccallum/fusarium-pah-bioinformatics

---

## Key Principle

Annotation evidence identifies **candidate** genes only. No candidate can be described as a confirmed PAH-degrading gene without experimental validation (protein expression, substrate assay, activity measurement). All candidates require manual review before reporting.

The goal of Stage 6 is to generate a **ranked candidate list** for manual review and possible downstream validation — not to claim PAH degradation.

---

## Search Strategy Overview

Three complementary layers will be used. Candidates detected by multiple layers receive higher confidence.

| Layer | Method | Sensitivity | Specificity |
|---|---|---|---|
| 1 | Keyword search — annotation text fields (product name, notes, GO descriptions) | High | Low |
| 2 | Pfam/InterPro domain search — domain accession matching in InterProScan output | Medium | High |
| 3 | Homology — UniProt/Swiss-Prot curated hit descriptions | Medium | Medium |

**eggNOG and KEGG are not included as core inputs.** They are not part of the current Funannotate workflow. If added later, they will be treated as optional downstream layers.

---

## Section 1 — Oxidative Enzymes: Initial PAH Attack

### Cytochrome P450 Monooxygenases (CYPs)

CYPs are the primary candidates for initial PAH hydroxylation in *Fusarium*. The Fungal Cytochrome P450 Database (FCPD; Moktali et al. 2012) classifies fungal CYPs into families with known substrate associations. Specific subfamilies are prioritised here based on documented PAH/xenobiotic roles in the literature.

> ⚠️ **Important:** All CYPs share **PF00067**. Pfam alone cannot distinguish subfamilies. Subfamily assignment requires FCPD classification or phylogenetic analysis. Expect ~133 CYP genes in the *F. solani* genome — systematic classification is essential.

| Family / Subfamily | Search Terms | Pfam | Default Confidence | Basis |
|---|---|---|---|---|
| CYP monooxygenases (general) | cytochrome P450, CYP, monooxygenase, P450, unspecific monooxygenase, EC 1.14.14.1 | PF00067 | Medium | — |
| **CYP5144 subfamily** | CYP5144 | PF00067 + FCPD | **High** | Moktali 2012 — documented PAH-related roles |
| **CYP504 subfamily** | CYP504 | PF00067 + FCPD | **High** | Moktali 2012 — benzoate/aromatic compound metabolism |
| **CYP52 subfamily** | CYP52 | PF00067 + FCPD | **High** | Moktali 2012 — alkane/fatty acid hydroxylation; hydrophobic substrates |
| **CYP53 subfamily** | CYP53 | PF00067 + FCPD | **High** | Moktali 2012 — benzoate/xenobiotic hydroxylation |

### CYP450 Reductases

Not PAH-degrading enzymes themselves, but essential redox partners required for CYP activity. Co-occurrence with a high-priority CYP gene on the same scaffold is meaningful supporting evidence.

| Family | Search Terms | Pfam | Default Confidence | Basis |
|---|---|---|---|---|
| NADPH-cytochrome P450 reductase | cytochrome P450 reductase, CPR, NADPH-P450 reductase, P450 reductase | FAD/FMN oxidoreductase domains — verify against InterProScan output | Medium (supporting) | Vergara-Fernández 2019 |

### Other Oxidative Enzymes

| Family | Search Terms | Pfam | Default Confidence | Notes |
|---|---|---|---|---|
| Laccases / multicopper oxidases | laccase, multicopper oxidase, MCO | PF00394, PF07731, PF07732 | Medium | Upgrade to High if secretion signal present |
| Manganese peroxidases (MnP) | manganese peroxidase, MnP | PF01036 | Medium | Upgrade if secretion signal present |
| Lignin peroxidases (LiP) | lignin peroxidase, LiP | PF01036 | Medium | |
| Dye-decolourising peroxidases (DyP) | DyP, dye decolourising peroxidase | PF04261 | Medium | |
| FAD-dependent monooxygenases | FAD monooxygenase, flavin monooxygenase, FMO, EC 1.14.13.1 | PF00743 | Medium | Includes salicylate-1-monooxygenase (EC 1.14.13.1) |
| Phenol monooxygenases | phenol monooxygenase, phenol-2-monooxygenase, EC 1.14.13.7 | PF00743 | Medium | Annotated in *F. solani* genomes — San Martín-Davison 2024 |
| Alcohol / methanol oxidases | alcohol oxidase, methanol oxidase, aryl alcohol oxidase | PF01565, PF00732 | Medium | Vergara-Fernández 2019 — *F. solani* as hydrocarbon-interacting fungus |

---

## Section 2 — Downstream Transformation and Detoxification

| Family | Search Terms | Pfam | Default Confidence | Basis / Notes |
|---|---|---|---|---|
| Epoxide hydrolases | epoxide hydrolase, EH | PF00561 | Medium | Downstream of CYP-mediated hydroxylation; produces trans-dihydrodiols |
| **Aryl sulfatases** | arylsulfatase, sulfatase, sulfate ester, aryl-sulfate sulfohydrolase | PF00884 | Medium | Han et al. 2026 — 6-hydroxybenzo[a]pyrene sulfate identified as key PAH metabolite |
| Glutathione S-transferases (GSTs) | glutathione S-transferase, GST | PF00043, PF02798 | Medium | Core conjugation/detoxification family |
| UDP-glycosyltransferases (UGTs) | glycosyltransferase, UDP-glucosyltransferase, UGT, UDP-glucuronosyltransferase | PF00201 | Medium | Phase II conjugation |
| Formaldehyde dehydrogenases | formaldehyde dehydrogenase | PF00107 | Medium | Vergara-Fernández 2019 — downstream of methanol oxidase; overlaps with oxidation pathway |
| Aldehyde dehydrogenases (ALDHs) | aldehyde dehydrogenase, ALDH | PF00171 | **Low** | Vergara-Fernández 2019; large family — expect many hits unrelated to PAHs. Keyword match alone insufficient; require Pfam support |
| Short-chain dehydrogenases / reductases (SDRs) | short-chain dehydrogenase, SDR, dehydrogenase, reductase | PF00106 | **Low** | Very large superfamily. Keyword match alone is not meaningful; Pfam support required. Flag as low-confidence by default |

---

## Section 3 — Aromatic Ring-Related Enzymes ⚠️

> **Contamination caution.** Classic bacterial ring-hydroxylating dioxygenases are well-characterised for PAH degradation but are **not central to fungal PAH metabolism**. Given the known ~36% *Methylorubrum populi* bacterial contamination in the raw reads, hits in this section must be treated as potentially indicative of **bacterial contamination in the assembly**, not fungal PAH degradation.
>
> For any hit in this section, check:
> - Is the best BLAST/UniProt hit fungal or bacterial?
> - Is the gene on a short scaffold that may be a bacterial contig?
> - Does the scaffold GC content or coverage look anomalous?

| Family | Search Terms | Pfam | Default Confidence | Contamination Risk |
|---|---|---|---|---|
| Dioxygenases | dioxygenase, ring cleavage, catechol dioxygenase, ring-hydroxylating dioxygenase | PF00775, PF00848 | Low | **High** |
| Aromatic compound oxygenases | aromatic oxygenase, ring hydroxylating oxygenase | — | Low | **High** |
| Catechol-related enzymes | catechol, protocatechuate, gentisate | — | Low | **High** — predominantly bacterial pathways |

---

## Section 4 — Transport and Efflux

Transporters are not direct PAH-degrading enzymes. They are relevant for PAH tolerance, efflux, membrane transport, and stress adaptation. Report separately from catalytic enzyme candidates.

| Family | Search Terms | Pfam | Default Confidence | Notes |
|---|---|---|---|---|
| ABC transporters | ABC transporter, ATP-binding cassette | PF00005 | Low | Broad family; relevant for PAH efflux/tolerance |
| MFS transporters | major facilitator, MFS transporter | PF07690 | Low | Same caveat |
| PDR transporters | pleiotropic drug resistance, PDR transporter | ABC transporter subfamilies | Low | More specifically fungal xenobiotic efflux |
| Efflux pumps | efflux transporter, multidrug transporter | transporter domains | Low | |

---

## Section 5 — Oxidative Stress and Cellular Defence

General stress response enzymes. Expected in any fungal genome. Relevant as supporting context for PAH exposure response, but annotation alone is weak evidence for PAH-specific roles.

| Family | Search Terms | Pfam | Default Confidence | Notes |
|---|---|---|---|---|
| Catalases | catalase | PF00199 | Low | |
| Superoxide dismutases (SODs) | superoxide dismutase, SOD | PF00080, PF00081 | Low | |
| Peroxiredoxins | peroxiredoxin, thioredoxin peroxidase | PF00578 | Low | |
| Glutathione peroxidases | glutathione peroxidase, GPx | PF00255 | Low | |
| Thioredoxins / glutaredoxins | thioredoxin, glutaredoxin | redox defence domains | Low | |

---

## Confidence Upgrade / Downgrade Rules

Default confidence is set per gene family above. Individual candidates can be adjusted:

| Factor | Effect |
|---|---|
| Multiple evidence types agree (keyword + Pfam + UniProt) | Upgrade |
| CYP assignable to high-priority subfamily (CYP5144 / CYP504 / CYP52 / CYP53) | Upgrade to **High** |
| Secretion signal present (laccase, peroxidase, hydrolase) | Upgrade |
| Co-located CYP reductase on same scaffold as CYP | Supporting evidence note |
| Best BLAST/UniProt hit is bacterial, not fungal | Downgrade + contamination flag |
| Gene on short or suspicious scaffold | Downgrade + contamination flag |
| Only vague / hypothetical annotation with no domain support | Downgrade |
| SDR or ALDH — keyword match only, no Pfam support | Downgrade to minimal |

---

## Caveats

- **CYP subfamily assignment** (CYP5144, CYP504, CYP52, CYP53) requires FCPD database classification or phylogenetic analysis. PF00067 detects all CYPs equally and cannot distinguish subfamilies on its own.
- **Large superfamilies** (GSTs, SDRs, ALDHs, transporters, catalases) will produce many hits unrelated to PAH metabolism. High hit counts are expected and do not indicate PAH activity.
- **Laccases and peroxidases** are most relevant as extracellular oxidative enzymes. Secretion prediction adds meaningful support.
- **Dioxygenase hits must be treated with contamination suspicion** given the known bacterial contamination in the raw reads (~36% *Methylorubrum populi*).
- **EC numbers** (EC 1.14.13.7, EC 1.14.13.1, EC 1.14.14.1) should be included as keyword search terms — annotation tools often include them and keyword-only EC number matches may otherwise be missed.
- **All candidates require manual review** before being reported in figures, tables, or manuscripts.

---

## Literature Sources for Target Family Selections

| Source | Contribution to this document |
|---|---|
| Moktali et al. 2012 (FCPD) | CYP subfamily prioritisation (CYP5144, CYP504, CYP52, CYP53) |
| Han et al. 2026 | Aryl sulfatases — 6-hydroxybenzo[a]pyrene sulfate as key metabolite |
| Vergara-Fernández et al. 2019 | CYP reductases, alcohol/methanol oxidases, formaldehyde dehydrogenases, ALDHs |
| San Martín-Davison et al. 2024 | Phenol-2-monooxygenase and unspecific monooxygenase EC numbers annotated in *F. solani* |
| Fayeulle et al. 2014 | Intracellular degradation mechanism — supports search for intracellular enzymes |
| Kadri et al. 2017 | General fungal enzyme mechanism context |
