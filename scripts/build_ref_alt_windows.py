#!/usr/bin/env python3
"""Build ref/alt GRCh38 sequence windows for NAMPT-axis candidate variants.

Reference sequence is fetched ONCE per gene regulatory window via the
Ensembl sequence API and cached under data_audit/raw/ensembl_ref_<gene>.fa,
so the number of network calls scales with genes, not variants. For each
candidate variant the script then slices the centered window (2 kb default)
from the reference, builds the ALT version by substituting the variant
allele, and writes BED + FASTA outputs.

Note on strandedness: Ensembl region sequence is always returned on the
forward strand of the chromosome. For minus-strand genes the regulatory
window still lies on the chromosome, so forward-strand windows are the
correct substrate for a strand-agnostic sequence model like Evo2; strand
sensitivity is recorded for downstream analysis.

Outputs:
  data_audit/outputs/evo2/windows.bed
  data_audit/outputs/evo2/windows.fasta
  data_audit/raw/ensembl_ref_<gene>.fa
"""
from __future__ import annotations

import csv
import json
import os
import time
import urllib.request
from collections import defaultdict

BASE = os.path.join(os.path.dirname(__file__), "..", "data_audit")
OUT_DIR = os.path.join(BASE, "outputs", "evo2")
RAW_DIR = os.path.join(BASE, "raw")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(RAW_DIR, exist_ok=True)

CANDIDATES_CSV = os.path.join(OUT_DIR, "candidates_priority.csv")
ENSEMBL = "https://rest.ensembl.org"
UA = {"User-Agent": "evo2-40b-research/0.1", "Content-Type": "application/json"}

WINDOW_SIZES = [2000]  # centered on variant; extend to 8000/32000 later

# Gene regulatory windows (GRCh38), used to fetch reference once per gene.
# Span = TSS ± 20 kb so all 2 kb candidate windows are covered.
GENE_REG_WINDOWS = {
    "NAMPT":  ("7",  106_271_225, 106_311_225),  # TSS=106291225 ±20k
    "CD38":   ("4",  15_758_275,  15_798_275),
    "BST1":   ("4",  15_682_993,  15_722_993),
    "SIRT1":  ("10", 67_864_647,  67_904_647),
    "IL6":    ("7",  22_705_884,  22_745_884),
    "TNF":    ("6",  31_555_558,  31_595_558),
    "SIRT3":  ("11", 216_931,     256_931),
    "SIRT6":  ("19", 4_162_604,   4_202_604),
}


def fetch_ref(gene: str) -> tuple[str, int]:
    """Fetch gene regulatory window reference once; returns (seq, start_pos).

    Retries with exponential backoff on transient 5xx / timeouts.
    """
    chrom, start, end = GENE_REG_WINDOWS[gene]
    cache = os.path.join(RAW_DIR, f"ensembl_ref_{gene}.fa")
    if os.path.exists(cache):
        with open(cache, encoding="utf-8") as f:
            lines = f.read().splitlines()
        return "".join(lines[1:]), start
    url = f"{ENSEMBL}/sequence/region/human/{chrom}:{start}-{end}:1?content-type=application/json"
    seq = ""
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                d = json.loads(r.read().decode())
            seq = d.get("seq", "")
            break
        except Exception as e:  # HTTPError, TimeoutError, URLError
            print(f"  [{gene}] attempt {attempt + 1} failed: {type(e).__name__} "
                  f"{getattr(e, 'code', '')}", flush=True)
            time.sleep(2 * (attempt + 1))
    if not seq:
        raise RuntimeError(f"Failed to fetch reference for {gene} after 5 attempts")
    with open(cache, "w", encoding="utf-8") as f:
        f.write(f">{gene} GRCh38 chr{chrom}:{start}-{end}\n")
        for i in range(0, len(seq), 80):
            f.write(seq[i:i + 80] + "\n")
    time.sleep(1.0)  # gentle rate limit between gene fetches
    return seq, start


def first_alt(alt: str) -> str:
    return alt.split(",")[0].strip().upper()


def build_alt(seq: str, offset: int, ref: str, alt: str) -> str:
    """Build the ALT allele sequence at 0-based offset in `seq`.

    Handles both SNP (ref len == alt len) and indel (delete ref, insert alt).
    For multiallelic variants only the first ALT is used; the rest are noted
    in the output. Ref bases are validated against the reference at offset.
    """
    alt_first = first_alt(alt)
    ref_upper = ref.strip().upper()
    observed = seq[offset:offset + len(ref_upper)].upper()
    if observed != ref_upper:
        return None  # mismatch: skip with note
    # delete ref allele, insert alt allele
    return seq[:offset] + alt_first + seq[offset + len(ref_upper):]


def main() -> None:
    with open(CANDIDATES_CSV, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    ref_cache = {}
    bed_rows = []
    fasta_entries = []
    notes = []

    for r in rows:
        gene = r["gene_window"]
        chrom, start, end = GENE_REG_WINDOWS[gene]
        if gene not in ref_cache:
            ref_cache[gene], start = fetch_ref(gene)
        ref_seq = ref_cache[gene]
        pos = int(r["position"])
        rel = pos - start
        half = WINDOW_SIZES[0] // 2
        lo = max(0, rel - half)
        hi = min(len(ref_seq), rel + half)
        win_ref = ref_seq[lo:hi]
        ref_allele = r["ref"].strip().upper()
        alt_allele = r["alt"].strip().upper()
        if not ref_allele or not alt_allele:
            notes.append((gene, r["rsid"], "missing_ref_alt"))
            continue
        offset = rel - lo  # position of variant within the sliced window
        alt_seq = build_alt(win_ref, offset, ref_allele, alt_allele)
        if alt_seq is None:
            notes.append((gene, r["rsid"], "ref_mismatch"))
            continue
        bed_rows.append({
            "chrom": chrom, "start": start + lo, "end": start + hi,
            "gene": gene, "rsid": r["rsid"], "ref_allele": ref_allele,
            "alt_allele": alt_allele, "window_bp": WINDOW_SIZES[0],
            "variant_class": "indel" if len(ref_allele) != len(first_alt(r["alt"])) else "snp",
        })
        fasta_entries.append(f">{r['rsid']}_ref_{gene}")
        fasta_entries.append(win_ref)
        fasta_entries.append(f">{r['rsid']}_alt_{gene}")
        fasta_entries.append(alt_seq)

    bed_path = os.path.join(OUT_DIR, "windows.bed")
    with open(bed_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["chrom", "start", "end", "gene", "rsid",
                                          "ref_allele", "alt_allele", "window_bp",
                                          "variant_class"],
                           delimiter="\t")
        w.writeheader()
        for row in bed_rows:
            w.writerow(row)

    fasta_path = os.path.join(OUT_DIR, "windows.fasta")
    with open(fasta_path, "w", encoding="utf-8") as f:
        f.write("\n".join(fasta_entries) + "\n")

    note_path = os.path.join(OUT_DIR, "window_build_notes.csv")
    with open(note_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["gene", "rsid", "note"])
        for g, rs, note in notes:
            w.writerow([g, rs, note])

    print(f"Wrote {len(bed_rows)} windows to {bed_path}")
    print(f"Wrote {len(fasta_entries)//2} FASTA sequences to {fasta_path}")
    print(f"Notes: {len(notes)} skipped variants")
    if notes:
        from collections import Counter
        print(Counter(n for _, _, n in notes))


if __name__ == "__main__":
    main()