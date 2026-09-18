#!/usr/bin/env python3
"""Build a candidate variant table near NAMPT-axis core genes.

Strategy: use Ensembl REST /overlap/region to retrieve variants with known
REF/ALT alleles in high-information windows around each core NAMPT-axis
gene. Primary windows are the promoter / near-gene regulatory region (±1 kb
around the gene's upstream anchor), with an option to widen. Ensembl gives
chromosome, start, end, and allele list, which is what the Evo2 ref/alt
scoring needs.

This is a PUBLIC-API candidate screen, not a claim of causality. Output
variants are candidates for the Evo2 ref/alt scoring step, to be filtered
against eQTL/GWAS/regulatory evidence downstream.

Outputs:
  data_audit/outputs/evo2/candidates.csv
  data_audit/raw/ensembl_<gene>_raw.json   (cached responses)
"""
from __future__ import annotations

import csv
import json
import os
import time
import urllib.request
import collections

BASE = os.path.join(os.path.dirname(__file__), "..", "data_audit")
OUT_DIR = os.path.join(BASE, "outputs", "evo2")
RAW_DIR = os.path.join(BASE, "raw")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(RAW_DIR, exist_ok=True)

ENSEMBL = "https://rest.ensembl.org"

# Gene -> (chrom, tss_position, half_window). TSS from Ensembl GRCh38 lookup
# (strand-aware): NAMPT/SIRT3/SIRT6 are on the minus strand, so their TSS is
# the gene end. The promoter-proximal window (± half_window bp) is where
# regulatory variants most plausibly affect expression.
GENE_ANCHORS = {
    "NAMPT":  ("7",  106_291_225, 2_000),  # strand -, TSS=end
    "CD38":   ("4",  15_778_275,  2_000),
    "BST1":   ("4",  15_702_993,  2_000),
    "SIRT1":  ("10", 67_884_647,  2_000),
    "IL6":    ("7",  22_725_884,  2_000),
    "TNF":    ("6",  31_575_558,  2_000),
    "SIRT3":  ("11", 236_931,     2_000),  # strand negative TSS=end
    "SIRT6":  ("19", 4_182_604,   2_000),  # strand negative TSS=end
}

UA = "evo2-40b-research/0.1"


def fetch_json(url: str, timeout: int = 30) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def ensembl_overlap(gene: str) -> list[dict]:
    chrom, anchor, win = GENE_ANCHORS[gene]
    start = anchor - win
    end = anchor + win
    url = f"{ENSEMBL}/overlap/region/human/{chrom}:{start}-{end}?feature=variation&content-type=application/json"
    cache = os.path.join(RAW_DIR, f"ensembl_{gene}_raw.json")
    if os.path.exists(cache):
        with open(cache, encoding="utf-8") as f:
            return json.load(f)
    data = fetch_json(url)
    with open(cache, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    time.sleep(0.4)
    return data


def pick_alleles(v: dict) -> dict:
    """Extract REF/ALT if possible; Ensembl gives a flat allele list."""
    alleles = v.get("alleles") or []
    # Prefer a variant where we can assign REF (first) and an ALT
    ref = alleles[0] if alleles else ""
    alt = ",".join(alleles[1:]) if len(alleles) > 1 else ""
    return {
        "chromosome": v.get("seq_region_name"),
        "position": v.get("start"),
        "end": v.get("end"),
        "rsid": v.get("id"),
        "ref": ref,
        "alt": alt,
        "n_alleles": len(alleles),
        "consequence": v.get("consequence_type") or "",
        "clinical_significance": v.get("clinical_significance") or "",
    }


def main() -> None:
    all_rows = []
    for gene in GENE_ANCHORS:
        print(f"[{gene}] Ensembl overlap ...", flush=True)
        vs = ensembl_overlap(gene)
        print(f"  {len(vs)} variants in promoter window", flush=True)
        for v in vs:
            if not v.get("id") or not v.get("start"):
                continue
            row = pick_alleles(v)
            if not row["alt"]:  # require at least one ALT allele
                continue
            row["gene_window"] = gene
            all_rows.append(row)
        time.sleep(0.3)

    # Dedup by (chr,pos)
    seen = set()
    dedup = []
    for r in all_rows:
        key = (r["chromosome"], r["position"])
        if key in seen:
            continue
        seen.add(key)
        dedup.append(r)

    dedup.sort(key=lambda r: (r["gene_window"], r["position"]))

    out_csv = os.path.join(OUT_DIR, "candidates.csv")
    fields = ["gene_window", "rsid", "chromosome", "position", "end",
              "ref", "alt", "n_alleles", "consequence", "clinical_significance"]
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in dedup:
            w.writerow(r)

    # ---- Priority subset ----
    # Tier-0: any ClinVar annotation OR strong functional consequence
    # (missense / splice / 5'UTR / TF binding / regulatory region).
    # For genes with a flood of TF-binding/regulatory variants (SIRT1, TNF,
    # IL6, SIRT3, SIRT6, CD38, BST1), keep at most PRIORITY_CAP per gene,
    # ranked by functional priority then position. NAMPT gets all its few
    # candidates (deep coverage of the focal gene).
    func_rank = [
        "missense_variant", "splice_region_variant", "5_prime_UTR_variant",
        "TF_binding_site_variant", "regulatory_region_variant",
    ]
    def priority_key(r):
        if r["clinical_significance"]:
            return 0
        for i, f in enumerate(func_rank):
            if f in r["consequence"]:
                return i + 1
        return 99

    PRIORITY_CAP = 60  # per gene

    by_gene = collections.defaultdict(list)
    for r in dedup:
        k = priority_key(r)
        if k == 99:
            continue
        by_gene[r["gene_window"]].append((k, r))

    priority_rows = []
    for gene, items in sorted(by_gene.items()):
        items.sort(key=lambda x: (x[0], x[1]["position"]))
        cap = PRIORITY_CAP if gene != "NAMPT" else 10_000  # NAMPT: keep all
        priority_rows.extend(r for _, r in items[:cap])

    priority_csv = os.path.join(OUT_DIR, "candidates_priority.csv")
    with open(priority_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in priority_rows:
            w.writerow(r)

    from collections import Counter
    print(f"\nWrote {len(dedup)} variants with REF/ALT to {out_csv}")
    print(f"Wrote {len(priority_rows)} priority variants to {priority_csv}")
    print("priority by gene:", dict(Counter(r["gene_window"] for r in priority_rows)))


if __name__ == "__main__":
    main()