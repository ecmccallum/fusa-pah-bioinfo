#!/usr/bin/env python3
"""
Stage 6A — PAH Candidate Gene Screening
Fusarium solani PAH Bioinformatics Project
Author: Emma McCallum | UPPA | May 2026

Parses the funannotate-annotated GFF3 and screens all mRNA features
against a target family dictionary (keywords + Pfam domain accessions).
Outputs a TSV candidate table and a family summary.

Usage:
    python stage6a_candidate_screen.py \
        --gff results/annotation/funannotate/predict_v2/annotate_results/Fusarium_solani.gff3 \
        --outdir results/stage6

All candidates are provisional. No hit should be interpreted as a
confirmed PAH-degradation gene without experimental validation.
"""

import argparse
import csv
import os
import sys
from collections import defaultdict
from datetime import datetime

# =============================================================================
# TARGET FAMILY DICTIONARY
# =============================================================================

TARGET_FAMILIES = {

    # -------------------------------------------------------------------------
    # SECTION 1 — Oxidative Enzymes: Initial PAH Attack
    # -------------------------------------------------------------------------

    "CYP_general": {
        "section": "1_oxidative",
        "keywords": [
            "cytochrome p450", "cyp", "p450", "monooxygenase",
            "unspecific monooxygenase", "ec 1.14.14.1", "ec 1.14.13"
        ],
        "pfam": ["PF00067"],
        "default_confidence": "Medium",
        "contamination_risk": False,
        "notes": "All CYPs share PF00067. Subfamily assignment requires FCPD. monooxygenase keyword kept intentionally — clean up at manual review stage."
    },

    "CYP5144": {
        "section": "1_oxidative",
        "keywords": ["cyp5144"],
        "pfam": [],
        "default_confidence": "High",
        "contamination_risk": False,
        "notes": "High-priority — documented PAH-related roles (Moktali 2012)"
    },

    "CYP504": {
        "section": "1_oxidative",
        "keywords": ["cyp504"],
        "pfam": [],
        "default_confidence": "High",
        "contamination_risk": False,
        "notes": "High-priority — benzoate/aromatic compound metabolism (Moktali 2012)"
    },

    "CYP52": {
        "section": "1_oxidative",
        "keywords": ["cyp52"],
        "pfam": [],
        "default_confidence": "High",
        "contamination_risk": False,
        "notes": "High-priority — alkane/fatty acid hydroxylation (Moktali 2012)"
    },

    "CYP53": {
        "section": "1_oxidative",
        "keywords": ["cyp53"],
        "pfam": [],
        "default_confidence": "High",
        "contamination_risk": False,
        "notes": "High-priority — benzoate/xenobiotic hydroxylation (Moktali 2012)"
    },

    "CYP_reductase": {
        "section": "1_oxidative",
        "keywords": [
            "cytochrome p450 reductase", "cpr", "nadph-p450 reductase",
            "p450 reductase", "nadph cytochrome p450"
        ],
        "pfam": [],
        "default_confidence": "Medium",
        "contamination_risk": False,
        "notes": "Supporting evidence — redox partner for CYPs (Vergara-Fernandez 2019)"
    },

    "laccase_MCO": {
        "section": "1_oxidative",
        "keywords": ["laccase", "multicopper oxidase", "mco", "copper oxidase"],
        "pfam": ["PF00394", "PF07731", "PF07732"],
        "default_confidence": "Medium",
        "contamination_risk": False,
        "notes": "Upgrade to High if secretion signal present"
    },

    "manganese_peroxidase": {
        "section": "1_oxidative",
        "keywords": ["manganese peroxidase", "mnp"],
        "pfam": ["PF01036"],
        "default_confidence": "Medium",
        "contamination_risk": False,
        "notes": "Upgrade if secretion signal present"
    },

    "lignin_peroxidase": {
        "section": "1_oxidative",
        "keywords": ["lignin peroxidase", "lip"],
        "pfam": ["PF01036"],
        "default_confidence": "Medium",
        "contamination_risk": False,
        "notes": ""
    },

    "DyP_peroxidase": {
        "section": "1_oxidative",
        "keywords": ["dyp", "dye decolouri", "dye decolori"],
        "pfam": ["PF04261"],
        "default_confidence": "Medium",
        "contamination_risk": False,
        "notes": ""
    },

    "FAD_monooxygenase": {
        "section": "1_oxidative",
        "keywords": [
            "fad monooxygenase", "flavin monooxygenase", "fmo",
            "ec 1.14.13.1", "salicylate monooxygenase"
        ],
        "pfam": ["PF00743"],
        "default_confidence": "Medium",
        "contamination_risk": False,
        "notes": "Includes salicylate-1-monooxygenase"
    },

    "phenol_monooxygenase": {
        "section": "1_oxidative",
        "keywords": [
            "phenol monooxygenase", "phenol-2-monooxygenase", "ec 1.14.13.7"
        ],
        "pfam": ["PF00743"],
        "default_confidence": "Medium",
        "contamination_risk": False,
        "notes": "Annotated in F. solani (San Martin-Davison 2024)"
    },

    "alcohol_oxidase": {
        "section": "1_oxidative",
        "keywords": [
            "alcohol oxidase", "methanol oxidase", "aryl alcohol oxidase",
            "glucose oxidase"
        ],
        "pfam": ["PF01565", "PF00732"],
        "default_confidence": "Medium",
        "contamination_risk": False,
        "notes": "Vergara-Fernandez 2019"
    },

    # -------------------------------------------------------------------------
    # SECTION 2 — Downstream Transformation and Detoxification
    # -------------------------------------------------------------------------

    "epoxide_hydrolase": {
        "section": "2_downstream",
        "keywords": ["epoxide hydrolase", "epoxide hydratase"],
        "pfam": ["PF00561"],
        "default_confidence": "Medium",
        "contamination_risk": False,
        "notes": "Downstream of CYP-mediated hydroxylation. ' eh ' keyword removed — too short, risk of false matches."
    },

    "aryl_sulfatase": {
        "section": "2_downstream",
        "keywords": [
            "arylsulfatase", "aryl sulfatase", "sulfatase",
            "sulfate ester", "aryl-sulfate sulfohydrolase"
        ],
        "pfam": ["PF00884"],
        "default_confidence": "Medium",
        "contamination_risk": False,
        "notes": "Han et al. 2026 — 6-hydroxybenzo[a]pyrene sulfate metabolite"
    },

    "GST": {
        "section": "2_downstream",
        "keywords": ["glutathione s-transferase", "glutathione transferase", "gst"],
        "pfam": ["PF00043", "PF02798"],
        "default_confidence": "Medium",
        "contamination_risk": False,
        "notes": "Core conjugation/detoxification family"
    },

    "UGT": {
        "section": "2_downstream",
        "keywords": [
            "glycosyltransferase", "udp-glucosyltransferase", "ugt",
            "udp-glucuronosyltransferase", "udp glucosyl"
        ],
        "pfam": ["PF00201"],
        "default_confidence": "Medium",
        "contamination_risk": False,
        "notes": "Phase II conjugation"
    },

    "formaldehyde_dehydrogenase": {
        "section": "2_downstream",
        "keywords": ["formaldehyde dehydrogenase"],
        "pfam": ["PF00107"],
        "default_confidence": "Medium",
        "contamination_risk": False,
        "notes": "Vergara-Fernandez 2019 — downstream of methanol oxidase"
    },

    "aldehyde_dehydrogenase": {
        "section": "2_downstream",
        "keywords": ["aldehyde dehydrogenase", "aldh"],
        "pfam": ["PF00171"],
        "default_confidence": "Low",
        "contamination_risk": False,
        "notes": "Large family — keyword match alone insufficient; require Pfam support for meaningful hits"
    },

    "SDR": {
        "section": "2_downstream",
        "keywords": ["short-chain dehydrogenase", "short chain dehydrogenase", "sdr"],
        "pfam": ["PF00106"],
        "default_confidence": "Low",
        "contamination_risk": False,
        "notes": "Very large superfamily — Pfam support required; keyword alone not meaningful"
    },

    # -------------------------------------------------------------------------
    # SECTION 3 — Aromatic Ring-Related Enzymes (CONTAMINATION RISK)
    # -------------------------------------------------------------------------

    "dioxygenase": {
        "section": "3_aromatic_contamination_risk",
        "keywords": [
            "dioxygenase", "ring cleavage", "catechol dioxygenase",
            "ring-hydroxylating dioxygenase", "ring hydroxylating"
        ],
        "pfam": ["PF00775", "PF00848"],
        "default_confidence": "Low",
        "contamination_risk": True,
        "notes": "HIGH contamination risk — check BLAST hit taxonomy and scaffold GC content"
    },

    "aromatic_oxygenase": {
        "section": "3_aromatic_contamination_risk",
        "keywords": [
            "aromatic oxygenase", "aromatic compound oxygenase",
            "ring hydroxylating oxygenase"
        ],
        "pfam": [],
        "default_confidence": "Low",
        "contamination_risk": True,
        "notes": "HIGH contamination risk — bacterial pathway"
    },

    "catechol_related": {
        "section": "3_aromatic_contamination_risk",
        "keywords": ["catechol", "protocatechuate", "gentisate"],
        "pfam": [],
        "default_confidence": "Low",
        "contamination_risk": True,
        "notes": "HIGH contamination risk — predominantly bacterial pathways"
    },

    # -------------------------------------------------------------------------
    # SECTION 4 — Transport and Efflux
    # -------------------------------------------------------------------------

    "ABC_transporter": {
        "section": "4_transport",
        "keywords": ["abc transporter", "atp-binding cassette", "atp binding cassette"],
        "pfam": ["PF00005"],
        "default_confidence": "Low",
        "contamination_risk": False,
        "notes": "Broad family — relevant for PAH efflux/tolerance. Report separately."
    },

    "MFS_transporter": {
        "section": "4_transport",
        "keywords": ["major facilitator", "mfs transporter", "mfs superfamily"],
        "pfam": ["PF07690"],
        "default_confidence": "Low",
        "contamination_risk": False,
        "notes": "Report separately from catalytic enzymes"
    },

    "PDR_transporter": {
        "section": "4_transport",
        "keywords": ["pleiotropic drug resistance", "pdr transporter", "pdr pump"],
        "pfam": [],
        "default_confidence": "Low",
        "contamination_risk": False,
        "notes": "Fungal xenobiotic efflux"
    },

    "efflux_pump": {
        "section": "4_transport",
        "keywords": ["efflux transporter", "multidrug transporter", "efflux pump"],
        "pfam": [],
        "default_confidence": "Low",
        "contamination_risk": False,
        "notes": ""
    },

    # -------------------------------------------------------------------------
    # SECTION 5 — Oxidative Stress and Cellular Defence
    # -------------------------------------------------------------------------

    "catalase": {
        "section": "5_stress_defence",
        "keywords": ["catalase"],
        "pfam": ["PF00199"],
        "default_confidence": "Low",
        "contamination_risk": False,
        "notes": "General stress response — expected in any fungal genome"
    },

    "SOD": {
        "section": "5_stress_defence",
        "keywords": ["superoxide dismutase", "sod"],
        "pfam": ["PF00080", "PF00081"],
        "default_confidence": "Low",
        "contamination_risk": False,
        "notes": ""
    },

    "peroxiredoxin": {
        "section": "5_stress_defence",
        "keywords": ["peroxiredoxin", "thioredoxin peroxidase"],
        "pfam": ["PF00578"],
        "default_confidence": "Low",
        "contamination_risk": False,
        "notes": ""
    },

    "glutathione_peroxidase": {
        "section": "5_stress_defence",
        "keywords": ["glutathione peroxidase", "gpx"],
        "pfam": ["PF00255"],
        "default_confidence": "Low",
        "contamination_risk": False,
        "notes": ""
    },

    "thioredoxin_glutaredoxin": {
        "section": "5_stress_defence",
        "keywords": ["thioredoxin", "glutaredoxin"],
        "pfam": [],
        "default_confidence": "Low",
        "contamination_risk": False,
        "notes": ""
    },

    # -------------------------------------------------------------------------
    # CONTAMINATION MARKERS
    # -------------------------------------------------------------------------

    "bacterial_contamination_marker": {
        "section": "0_contamination_marker",
        "keywords": [
            "groel", "groels", "flagellar", "flagellin",
            "xoxf", "lanthanide", "methanol dehydrogenase",
            "lold", "lolb", "lolc", "lole",
            "phnc", "phosphonate import",
            "flgi", "flgj", "flgk",
            "nqo3", "nqo13", "nuoa", "nuof",
        ],
        "pfam": [],
        "default_confidence": "Low",
        "contamination_risk": True,
        "notes": "Likely Methylorubrum populi contamination — verify scaffold GC and taxonomy"
    },
}


# =============================================================================
# GFF3 PARSER
# =============================================================================

def parse_attributes(attr_str):
    attrs = {}
    for part in attr_str.strip().rstrip(";").split(";"):
        part = part.strip()
        if "=" in part:
            key, _, val = part.partition("=")
            attrs[key.strip()] = val.strip()
    return attrs


def extract_pfam_ids(dbxref_str):
    pfam_ids = []
    for ref in dbxref_str.split(","):
        ref = ref.strip()
        if ref.startswith("PFAM:"):
            pfam_ids.append(ref[5:])
    return pfam_ids


def extract_merops_ids(dbxref_str, note_str):
    merops = []
    for src in [dbxref_str, note_str]:
        for ref in src.split(","):
            ref = ref.strip()
            if ref.startswith("MEROPS:"):
                merops.append(ref[7:])
    return merops


def extract_busco_ids(dbxref_str, note_str):
    busco = []
    for src in [dbxref_str, note_str]:
        for ref in src.split(","):
            ref = ref.strip()
            if ref.startswith("BUSCO:"):
                busco.append(ref[6:])
    return busco


# =============================================================================
# CANDIDATE SCREENING
# =============================================================================

def screen_gene(product, pfam_ids, note_str):
    """
    Screen a gene against all target families.
    Returns list of (family_name, matched_keywords, matched_pfam) tuples.
    All matches are kept — multiple families can match the same gene.
    """
    product_lower = product.lower()
    note_lower = note_str.lower()
    search_text = product_lower + " " + note_lower

    matches = []
    for fam_name, fam_data in TARGET_FAMILIES.items():
        matched_kw = []
        matched_pf = []

        for kw in fam_data.get("keywords", []):
            if kw in search_text:
                matched_kw.append(kw)

        for pfam_id in pfam_ids:
            if pfam_id in fam_data.get("pfam", []):
                matched_pf.append(pfam_id)

        if matched_kw or matched_pf:
            matches.append((fam_name, matched_kw, matched_pf))

    return matches


def determine_evidence_strength(matched_kw_all, matched_pf_all):
    """
    Returns evidence_strength based on which evidence types contributed.
    keyword_only / pfam_only / keyword_plus_pfam
    Does NOT automatically upgrade default_confidence.
    """
    has_kw = bool(matched_kw_all)
    has_pf = bool(matched_pf_all)
    if has_kw and has_pf:
        return "keyword_plus_pfam"
    elif has_kw:
        return "keyword_only"
    elif has_pf:
        return "pfam_only"
    return "none"


def is_contamination_flagged(matches):
    for fam_name, _, _ in matches:
        if TARGET_FAMILIES[fam_name].get("contamination_risk", False):
            return True
    return False


def highest_confidence(matches):
    """
    Returns the highest default_confidence among matched families.
    No automatic upgrade logic — family-level priors only.
    """
    rank = {"High": 3, "Medium": 2, "Low": 1}
    best = "Low"
    for fam_name, _, _ in matches:
        conf = TARGET_FAMILIES[fam_name]["default_confidence"]
        if rank.get(conf, 0) > rank.get(best, 0):
            best = conf
    return best


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Stage 6A — PAH candidate gene screen from annotated GFF3"
    )
    parser.add_argument("--gff", required=True,
        help="Path to annotated GFF3 (funannotate annotate output)")
    parser.add_argument("--outdir", default="results/stage6",
        help="Output directory (default: results/stage6)")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    hits_path    = os.path.join(args.outdir, "candidate_keyword_domain_hits.tsv")
    summary_path = os.path.join(args.outdir, "candidate_family_summary.tsv")
    log_path     = os.path.join(args.outdir, "stage6a_screen_log.txt")

    fieldnames = [
        "gene_id", "transcript_id", "scaffold", "start", "end", "strand",
        "product", "pfam_ids", "merops_ids", "busco_ids",
        "matched_families", "matched_keywords", "matched_pfam",
        "evidence_strength", "default_confidence", "contamination_flag", "notes"
    ]

    total_genes = 0
    total_hits  = 0
    family_counts  = defaultdict(int)
    section_counts = defaultdict(int)
    contamination_count = 0

    log_lines = [
        "Stage 6A — PAH Candidate Screen",
        f"Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"GFF3: {args.gff}",
        f"Target families: {len(TARGET_FAMILIES)}",
        "",
    ]

    with open(hits_path, "w", newline="") as hits_fh:
        writer = csv.DictWriter(hits_fh, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()

        with open(args.gff) as gff_fh:
            for line in gff_fh:
                if line.startswith("#"):
                    continue
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 9 or parts[2] != "mRNA":
                    continue

                scaffold = parts[0]
                start, end, strand = parts[3], parts[4], parts[6]
                attrs = parse_attributes(parts[8])

                transcript_id = attrs.get("ID", "")
                gene_id       = attrs.get("Parent", "")
                product       = attrs.get("product", "")
                dbxref        = attrs.get("Dbxref", "")
                note          = attrs.get("note", "")

                pfam_ids   = extract_pfam_ids(dbxref)
                merops_ids = extract_merops_ids(dbxref, note)
                busco_ids  = extract_busco_ids(dbxref, note)

                total_genes += 1
                matches = screen_gene(product, pfam_ids, note)

                if not matches:
                    continue

                total_hits += 1

                matched_families = []
                all_kw = []
                all_pf = []

                for fam_name, matched_kw, matched_pf in matches:
                    matched_families.append(fam_name)
                    all_kw.extend(matched_kw)
                    all_pf.extend(matched_pf)
                    family_counts[fam_name] += 1
                    section_counts[TARGET_FAMILIES[fam_name]["section"]] += 1

                # Deduplicate preserving order
                matched_families = list(dict.fromkeys(matched_families))
                all_kw = list(dict.fromkeys(all_kw))
                all_pf = list(dict.fromkeys(all_pf))

                evidence_strength = determine_evidence_strength(all_kw, all_pf)
                confidence        = highest_confidence(matches)
                contam_flag       = is_contamination_flagged(matches)

                if contam_flag:
                    contamination_count += 1

                fam_notes = []
                for fam_name in matched_families:
                    n = TARGET_FAMILIES[fam_name].get("notes", "")
                    if n:
                        fam_notes.append(f"{fam_name}: {n}")

                writer.writerow({
                    "gene_id":          gene_id,
                    "transcript_id":    transcript_id,
                    "scaffold":         scaffold,
                    "start":            start,
                    "end":              end,
                    "strand":           strand,
                    "product":          product,
                    "pfam_ids":         "|".join(pfam_ids),
                    "merops_ids":       "|".join(merops_ids),
                    "busco_ids":        "|".join(busco_ids),
                    "matched_families": "|".join(matched_families),
                    "matched_keywords": "|".join(all_kw),
                    "matched_pfam":     "|".join(all_pf),
                    "evidence_strength":evidence_strength,
                    "default_confidence": confidence,
                    "contamination_flag": "YES" if contam_flag else "no",
                    "notes":            " | ".join(fam_notes)
                })

    # Family summary
    with open(summary_path, "w", newline="") as sum_fh:
        sum_writer = csv.DictWriter(sum_fh, delimiter="\t", fieldnames=[
            "section", "family", "hit_count", "default_confidence",
            "contamination_risk", "notes"
        ])
        sum_writer.writeheader()
        for fam_name in sorted(TARGET_FAMILIES,
                key=lambda x: (TARGET_FAMILIES[x]["section"], x)):
            sum_writer.writerow({
                "section":            TARGET_FAMILIES[fam_name]["section"],
                "family":             fam_name,
                "hit_count":          family_counts.get(fam_name, 0),
                "default_confidence": TARGET_FAMILIES[fam_name]["default_confidence"],
                "contamination_risk": TARGET_FAMILIES[fam_name]["contamination_risk"],
                "notes":              TARGET_FAMILIES[fam_name].get("notes", "")
            })

    # Log
    log_lines += [
        f"Total mRNA features processed: {total_genes}",
        f"Total candidate hits: {total_hits}",
        f"Contamination-flagged hits: {contamination_count}",
        "",
        "Hits by family (sorted by count):",
    ]
    for fam_name in sorted(family_counts, key=lambda x: -family_counts[x]):
        conf   = TARGET_FAMILIES[fam_name]["default_confidence"]
        contam = " [CONTAMINATION RISK]" if TARGET_FAMILIES[fam_name]["contamination_risk"] else ""
        log_lines.append(f"  {fam_name}: {family_counts[fam_name]} ({conf}){contam}")

    log_lines += [
        "",
        "Hits by section:",
    ]
    for sec in sorted(section_counts):
        log_lines.append(f"  {sec}: {section_counts[sec]}")

    log_lines += [
        "",
        "Output files:",
        f"  {hits_path}",
        f"  {summary_path}",
        f"  {log_path}",
        "",
        "IMPORTANT: All candidates are provisional.",
        "No hit should be interpreted as a confirmed PAH-degradation",
        "gene without experimental validation.",
        "",
        "evidence_strength values:",
        "  keyword_only       — matched by product/note text only",
        "  pfam_only          — matched by Pfam domain accession only",
        "  keyword_plus_pfam  — matched by both (stronger evidence)",
        "",
        "default_confidence reflects family-level prior from Stage 6 plan.",
        "No automatic upgrades are applied — manual review required.",
    ]

    with open(log_path, "w") as log_fh:
        log_fh.write("\n".join(log_lines) + "\n")

    print("\n".join(log_lines))
    print(f"\nDone. Outputs written to {args.outdir}/")


if __name__ == "__main__":
    main()
