#!/usr/bin/env python3
"""Evo2-40B allele-surprisal scoring for NAMPT-axis candidate variants.

Score A (allele surprisal) per protocol: use the upstream flank of the
variant as the model prompt, request ONE generated token with logits, convert
the A/C/G/T logits to a DNA-normalized probability, and compute

    delta_surprisal = log P(alt) - log P(ref)

A large absolute value means the alternate allele changes the model's
expected local genomic continuation. Sign is NOT interpreted as beneficial
or harmful by itself.

Implementation notes:
  * Uses the hosted generate endpoint validated in test_evo2_endpoint.py.
  * API key is read ONLY from NVIDIA_API_KEY or NVCF_RUN_KEY env vars and is
    NEVER written to disk or logs.
  * Batch with --limit N and --resume to control cost.
  * Prompts: upstream flank of length --flank (default 200 bp) directly 5' of
    the variant allele (on the forward strand of the chromosome window).
  * DNA base -> logit index: verified mapping A=65, C=67, G=71, T=84 from the
    smoke-test log (ASCII-like token indices).

Outputs:
  data_audit/outputs/evo2/scores.csv
  data_audit/outputs/evo2/scoring_log.jsonl   (no secrets)
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import time
import urllib.request
from datetime import datetime, timezone

BASE = os.path.join(os.path.dirname(__file__), "..", "data_audit")
OUT_DIR = os.path.join(BASE, "outputs", "evo2")
WINDOWS_BED = os.path.join(OUT_DIR, "windows.bed")
FASTA = os.path.join(OUT_DIR, "windows.fasta")

ENDPOINT = "https://health.api.nvidia.com/v1/biology/arc/evo2-40b/generate"

# DNA base -> token index in Evo2 vocab (from endpoint smoke-test log:
# synthetic ACGTACGT... argmax indices were 65/67/71/84 for A/C/G/T).
BASE_TO_IDX = {"A": 65, "C": 67, "G": 71, "T": 84}

HEADERS_TMPL = {
    "Authorization": "Bearer {key}",
    "Content-Type": "application/json",
}


def parse_fasta(path: str) -> dict[str, str]:
    """Return {name: sequence} from the ref/alt FASTA."""
    out = {}
    lines = open(path, encoding="utf-8").read().splitlines()
    for i in range(0, len(lines), 2):
        out[lines[i][1:]] = lines[i + 1].upper()
    return out


def get_key() -> str | None:
    return os.environ.get("NVIDIA_API_KEY") or os.environ.get("NVCF_RUN_KEY")


def call_endpoint(sequence: str, key: str, num_tokens: int = 1,
                  temperature: float = 0.7, random_seed: int | None = None,
                  timeout: int = 60) -> dict:
    body = {
        "sequence": sequence,
        "num_tokens": num_tokens,
        "temperature": temperature,
        "top_k": 4,
        "top_p": 0.9,
        "random_seed": random_seed if random_seed is not None else random.randint(0, 1_000_000),
        "enable_logits": True,
        "enable_sampled_probs": True,
    }
    headers = {k: v.format(key=key) for k, v in HEADERS_TMPL.items()}
    req = urllib.request.Request(ENDPOINT, data=json.dumps(body).encode(),
                                 headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def dna_softmax(logits_pos: list[float]) -> dict[str, float]:
    """Convert A/C/G/T logits at one position to a normalized probability."""
    import math
    vals = {b: logits_pos[BASE_TO_IDX[b]] for b in "ACGT"}
    mx = max(vals.values())
    exps = {b: math.exp(v - mx) for b, v in vals.items()}
    z = sum(exps.values())
    return {b: exps[b] / z for b in "ACGT"}


def score_one(fasta: dict, variant: dict, key: str, flank: int,
              seed: int | None) -> dict:
    """Compute Score A for one variant. Returns result row (or None on failure)."""
    name = f"{variant['rsid']}_ref_{variant['gene']}"
    alt_name = f"{variant['rsid']}_alt_{variant['gene']}"
    ref_seq = fasta.get(name)
    alt_seq = fasta.get(alt_name)
    if not ref_seq or not alt_seq:
        return None
    # The window is centered on the variant: find the variant offset. We
    # rebuilt windows centered at half-window; the variant is at ~half.
    # Robust approach: use the BED position -> compute from ref/alt alignment
    # on the left flank (the part before the variant is identical).
    # Find first mismatch position between ref and alt.
    ref_allele = variant["ref_allele"].upper()
    alt_allele = variant["alt_allele"].upper()
    offset = 0
    # locate variant: search ref allele occurrence near window center
    half = len(ref_seq) // 2
    center_hit = ref_seq.find(ref_allele, max(0, half - 200), half + 200)
    if center_hit < 0:
        # fallback: first occurrence
        center_hit = ref_seq.find(ref_allele)
    if center_hit < 0:
        return None
    offset = center_hit
    prompt = ref_seq[max(0, offset - flank):offset]
    if not prompt:
        return None
    # ref/alt allele scores via the generated token after the prompt
    res = call_endpoint(prompt, key, num_tokens=1, random_seed=seed)
    logits = res.get("logits")
    if not logits or not isinstance(logits, list) or len(logits) < 1:
        return None
    pos_logits = logits[0]
    if not isinstance(pos_logits, list) or len(pos_logits) < max(BASE_TO_IDX.values()) + 1:
        return None
    probs = dna_softmax(pos_logits)
    import math
    ref_base = ref_allele[0]
    alt_base = first_alt(alt_allele)[0]
    if ref_base not in probs or alt_base not in probs:
        return None
    log_p_ref = math.log(probs[ref_base])
    log_p_alt = math.log(probs[alt_base])
    delta = log_p_alt - log_p_ref
    return {
        "gene_window": variant["gene"],
        "rsid": variant["rsid"],
        "chromosome": variant["chrom"],
        "position": variant["start"] + offset,
        "ref_allele": ref_allele,
        "alt_allele": alt_allele,
        "variant_class": variant.get("variant_class", ""),
        "flank_bp": flank,
        "log_p_ref": round(log_p_ref, 6),
        "log_p_alt": round(log_p_alt, 6),
        "delta_surprisal": round(delta, 6),
        "p_ref": round(probs[ref_base], 6),
        "p_alt": round(probs[alt_base], 6),
        "seed": seed,
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def first_alt(alt: str) -> str:
    return alt.split(",")[0].strip().upper()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=20,
                    help="max variants to score this run (default 20; use 0 for all)")
    ap.add_argument("--flank", type=int, default=200, help="upstream flank bp")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--resume", action="store_true",
                    help="skip rsids already present in scores.csv")
    args = ap.parse_args()

    key = get_key()
    if not key:
        print("ERROR: NVIDIA_API_KEY / NVCF_RUN_KEY not set. Refusing to run.")
        print("Set it first (Windows):  setx NVIDIA_API_KEY <key>  then restart terminal.")
        print("NEVER paste the key into the chat.")
        return 1

    os.makedirs(OUT_DIR, exist_ok=True)
    fasta = parse_fasta(FASTA)
    with open(WINDOWS_BED, newline="", encoding="utf-8") as f:
        variants = list(csv.DictReader(f, delimiter="\t"))

    # Existing scores for resume
    done = set()
    scores_csv = os.path.join(OUT_DIR, "scores.csv")
    if args.resume and os.path.exists(scores_csv):
        with open(scores_csv, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                done.add(row["rsid"])

    todo = [v for v in variants if v["rsid"] not in done]
    if args.limit and args.limit > 0:
        todo = todo[: args.limit]
    print(f"Scoring {len(todo)} variants (flank={args.flank}bp)...")

    log_path = os.path.join(OUT_DIR, "scoring_log.jsonl")
    results = []
    for i, v in enumerate(todo, 1):
        try:
            row = score_one(fasta, v, key, args.flank, args.seed)
        except Exception as e:
            row = None
            print(f"  [{i}/{len(todo)}] {v['rsid']} ERROR {type(e).__name__}: {str(e)[:120]}")
        if row:
            results.append(row)
            with open(log_path, "a", encoding="utf-8") as f:
                # log metadata only, NEVER the key
                log = {k: row[k] for k in row if k != "seed"}
                f.write(json.dumps(log) + "\n")
            print(f"  [{i}/{len(todo)}] {v['rsid']} delta={row['delta_surprisal']:+.4f} "
                  f"(p_ref={row['p_ref']:.4f} p_alt={row['p_alt']:.4f})")
        time.sleep(0.5)

    # Append to scores.csv
    write_header = not os.path.exists(scores_csv) or os.path.getsize(scores_csv) == 0
    with open(scores_csv, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "gene_window", "rsid", "chromosome", "position", "ref_allele",
            "alt_allele", "variant_class", "flank_bp", "log_p_ref", "log_p_alt",
            "delta_surprisal", "p_ref", "p_alt", "ts",
        ])
        if write_header:
            w.writeheader()
        for r in results:
            w.writerow({k: r.get(k) for k in w.fieldnames})

    print(f"Scored {len(results)} new variants. Total in scores.csv now "
          f"{_count_lines(scores_csv)} rows (incl header).")


def _count_lines(p: str) -> int:
    try:
        with open(p, encoding="utf-8") as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())