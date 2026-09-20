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
        "position": int(variant["start"]) + offset,
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


def revcomp(seq: str) -> str:
    comp = {"A": "T", "C": "G", "G": "C", "T": "A", "N": "N"}
    return "".join(comp.get(b, "N") for b in reversed(seq))


def next_base_probs(prompt: str, key: str, seed: int | None) -> dict[str, float] | None:
    """One-token call; return DNA-normalized probabilities for the next base."""
    res = call_endpoint(prompt, key, num_tokens=1, random_seed=seed)
    logits = res.get("logits")
    if not logits or not isinstance(logits, list) or len(logits) < 1:
        return None
    pos = logits[0]
    if not isinstance(pos, list) or len(pos) < max(BASE_TO_IDX.values()) + 1:
        return None
    return dna_softmax(pos)


def pseudo_ll(prefix: str, allele: str, downstream: str, key: str,
              seed: int | None) -> float | None:
    """PLL = sum_i log P(downstream[i] | prefix + allele + downstream[:i])."""
    import math
    total = 0.0
    ctx = prefix + allele
    for b in downstream:
        probs = next_base_probs(ctx, key, seed)
        if probs is None or b not in probs:
            return None
        total += math.log(probs[b])
        ctx += b
    return total


def score_B_one(fasta: dict, variant: dict, key: str, flank: int,
                downstream_len: int, seed: int | None) -> dict | None:
    """Score B: local pseudo-likelihood propagation on forward + reverse strand.

    delta_PLL(strand) = PLL(alt window) - PLL(ref window) on that strand.
    The observed downstream sequence is taken from the ref window so both
    alleles are scored against the identical downstream context.
    """
    name = f"{variant['rsid']}_ref_{variant['gene']}"
    alt_name = f"{variant['rsid']}_alt_{variant['gene']}"
    ref_seq = fasta.get(name)
    alt_seq = fasta.get(alt_name)
    if not ref_seq or not alt_seq:
        return None
    ref_allele = variant["ref_allele"].upper()
    alt_allele = first_alt(variant["alt_allele"])
    half = len(ref_seq) // 2
    center_hit = ref_seq.find(ref_allele, max(0, half - 200), half + 200)
    if center_hit < 0:
        center_hit = ref_seq.find(ref_allele)
    if center_hit < 0:
        return None
    offset = center_hit
    prompt = ref_seq[max(0, offset - flank):offset]
    if not prompt:
        return None
    alen = len(ref_allele)
    downstream = ref_seq[offset + alen:offset + alen + downstream_len]
    if len(downstream) < downstream_len:
        return None

    # Forward strand
    pll_ref_fwd = pseudo_ll(prompt, ref_allele, downstream, key, seed)
    pll_alt_fwd = pseudo_ll(prompt, alt_allele, downstream, key, seed)

    # Reverse-complement strand: rebuild prompt/downstream on rc windows
    rc_ref = revcomp(ref_seq)
    rc_alt = revcomp(alt_seq)
    rc_ref_allele = revcomp(ref_allele)
    rc_alt_allele = revcomp(alt_allele)
    half_rc = len(rc_ref) // 2
    off_rc = rc_ref.find(rc_ref_allele, max(0, half_rc - 200), half_rc + 200)
    if off_rc < 0:
        off_rc = rc_ref.find(rc_ref_allele)
    if off_rc < 0:
        return None
    rc_prompt = rc_ref[max(0, off_rc - flank):off_rc]
    rc_downstream = rc_ref[off_rc + len(rc_ref_allele):off_rc + len(rc_ref_allele) + downstream_len]
    if len(rc_downstream) < downstream_len:
        return None
    pll_ref_rc = pseudo_ll(rc_prompt, rc_ref_allele, rc_downstream, key, seed)
    pll_alt_rc = pseudo_ll(rc_prompt, rc_alt_allele, rc_downstream, key, seed)

    def d(alt, ref):
        return None if (alt is None or ref is None) else alt - ref

    delta_fwd = d(pll_alt_fwd, pll_ref_fwd)
    delta_rc = d(pll_alt_rc, pll_ref_rc)
    if delta_fwd is None or delta_rc is None:
        return None
    import math
    return {
        "gene_window": variant["gene"],
        "rsid": variant["rsid"],
        "chromosome": variant["chrom"],
        "position": int(variant["start"]) + offset,
        "ref_allele": ref_allele,
        "alt_allele": alt_allele,
        "flank_bp": flank,
        "downstream_bp": downstream_len,
        "pll_ref_fwd": round(pll_ref_fwd, 6),
        "pll_alt_fwd": round(pll_alt_fwd, 6),
        "delta_pll_fwd": round(delta_fwd, 6),
        "pll_ref_rc": round(pll_ref_rc, 6),
        "pll_alt_rc": round(pll_alt_rc, 6),
        "delta_pll_rc": round(delta_rc, 6),
        "delta_pll_mean": round((delta_fwd + delta_rc) / 2, 6),
        "strand_consistent": (delta_fwd > 0) == (delta_rc > 0) if delta_fwd != 0 and delta_rc != 0 else True,
        "seed": seed,
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def score_C_one(fasta: dict, variant: dict, key: str, flank: int,
                seeds: list[int], temperature: float) -> dict | None:
    """Score C: perturbation stability — repeat Score A across random seeds.

    Temperature does not change logits, so stability is probed with multiple
    seeds (endpoint-level repeatability of the ref/alt difference), not a
    temperature scan.
    """
    import math
    deltas = []
    rows = []
    for s in seeds:
        r = score_one(fasta, variant, key, flank, seed=s)
        if r:
            deltas.append(r["delta_surprisal"])
            rows.append(r)
    if not deltas:
        return None
    mean = sum(deltas) / len(deltas)
    sd = (sum((x - mean) ** 2 for x in deltas) / len(deltas)) ** 0.5
    return {
        "gene_window": variant["gene"],
        "rsid": variant["rsid"],
        "chromosome": variant["chrom"],
        "position": int(variant["start"]),
        "ref_allele": variant["ref_allele"].upper(),
        "alt_allele": first_alt(variant["alt_allele"]),
        "variant_class": variant.get("variant_class", ""),
        "flank_bp": flank,
        "n_seeds": len(deltas),
        "seeds": ",".join(str(s) for s in seeds),
        "temperature": temperature,
        "delta_mean": round(mean, 6),
        "delta_sd": round(sd, 6),
        "delta_min": round(min(deltas), 6),
        "delta_max": round(max(deltas), 6),
        "delta_range": round(max(deltas) - min(deltas), 6),
        "sign_consistent_all": len({1 if x > 0 else (-1 if x < 0 else 0) for x in deltas}) <= 1,
        "deltas": ",".join(f"{x:.4f}" for x in deltas),
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def load_shortlist(min_abs: float, keep_genes: set[str]) -> set[str]:
    """rsids with |Score A delta| >= min_abs OR gene in keep_genes."""
    out = set()
    p = os.path.join(OUT_DIR, "scores.csv")
    if not os.path.exists(p):
        return out
    with open(p, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if abs(float(row["delta_surprisal"])) >= min_abs or row["gene_window"] in keep_genes:
                out.add(row["rsid"])
    return out



def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=20,
                    help="max variants to score this run (default 20; use 0 for all)")
    ap.add_argument("--flank", type=int, default=200, help="upstream flank bp")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--resume", action="store_true",
                    help="skip rsids already present in scores.csv")
    ap.add_argument("--mode", choices=["A", "B", "C"], default="A",
                    help="A: allele surprisal; B: pseudo-likelihood; C: stability (multi-seed)")
    ap.add_argument("--downstream", type=int, default=32,
                    help="Score B: number of downstream bases to propagate (default 32)")
    ap.add_argument("--seeds", type=int, default=5,
                    help="Score C: number of random seeds (default 5)")
    ap.add_argument("--temperature", type=float, default=0.7,
                    help="Score C: temperature (logits are temperature-independent)")
    ap.add_argument("--shortlist", action="store_true",
                    help="restrict to |Score A| >= 4 or NAMPT window (Tier-A shortlist)")
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

    if args.mode in ("B", "C"):
        out_csv = os.path.join(OUT_DIR, f"scores_{args.mode}.csv")
        log_path = os.path.join(OUT_DIR, f"scoring_{args.mode}_log.jsonl")
    else:
        out_csv = os.path.join(OUT_DIR, "scores.csv")
        log_path = os.path.join(OUT_DIR, "scoring_log.jsonl")

    if args.shortlist:
        keep = load_shortlist(min_abs=4.0, keep_genes={"NAMPT"})
        variants = [v for v in variants if v["rsid"] in keep]
        print(f"Shortlist: {len(variants)} variants (|Score A| >= 4 or NAMPT)")

    # Existing scores for resume (keyed by rsid)
    done = set()
    if args.resume and os.path.exists(out_csv):
        with open(out_csv, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                done.add(row["rsid"])
    todo = [v for v in variants if v["rsid"] not in done]
    if args.limit and args.limit > 0:
        todo = todo[: args.limit]
    print(f"Scoring {len(todo)} variants (mode={args.mode}, flank={args.flank}bp)...")

    seeds_list = [random.randint(0, 1_000_000) for _ in range(args.seeds)]
    results = []
    for i, v in enumerate(todo, 1):
        try:
            if args.mode == "A":
                row = score_one(fasta, v, key, args.flank, args.seed)
            elif args.mode == "B":
                row = score_B_one(fasta, v, key, args.flank, args.downstream, args.seed)
            else:
                row = score_C_one(fasta, v, key, args.flank, seeds_list, args.temperature)
        except Exception as e:
            row = None
            print(f"  [{i}/{len(todo)}] {v['rsid']} ERROR {type(e).__name__}: {str(e)[:120]}")
        if row:
            results.append(row)
            with open(log_path, "a", encoding="utf-8") as f:
                log = {k: row[k] for k in row if k not in ("seed", "seeds", "deltas")}
                f.write(json.dumps(log) + "\n")
            if args.mode == "A":
                print(f"  [{i}/{len(todo)}] {v['rsid']} delta={row['delta_surprisal']:+.4f} "
                      f"(p_ref={row['p_ref']:.4f} p_alt={row['p_alt']:.4f})")
            elif args.mode == "B":
                print(f"  [{i}/{len(todo)}] {v['rsid']} dPLL_fwd={row['delta_pll_fwd']:+.4f} "
                      f"dPLL_rc={row['delta_pll_rc']:+.4f} mean={row['delta_pll_mean']:+.4f} "
                      f"consistent={row['strand_consistent']}")
            else:
                print(f"  [{i}/{len(todo)}] {v['rsid']} delta_mean={row['delta_mean']:+.4f} "
                      f"sd={row['delta_sd']:.4f} range={row['delta_range']:.4f} "
                      f"sign_all_same={row['sign_consistent_all']}")
        time.sleep(0.5)

    fieldnames = {
        "A": ["gene_window", "rsid", "chromosome", "position", "ref_allele",
              "alt_allele", "variant_class", "flank_bp", "log_p_ref", "log_p_alt",
              "delta_surprisal", "p_ref", "p_alt", "ts"],
        "B": ["gene_window", "rsid", "chromosome", "position", "ref_allele",
              "alt_allele", "flank_bp", "downstream_bp", "pll_ref_fwd", "pll_alt_fwd",
              "delta_pll_fwd", "pll_ref_rc", "pll_alt_rc", "delta_pll_rc",
              "delta_pll_mean", "strand_consistent", "ts"],
        "C": ["gene_window", "rsid", "chromosome", "position", "ref_allele",
              "alt_allele", "variant_class", "flank_bp", "n_seeds", "seeds",
              "temperature", "delta_mean", "delta_sd", "delta_min", "delta_max",
              "delta_range", "sign_consistent_all", "deltas", "ts"],
    }[args.mode]

    write_header = not os.path.exists(out_csv) or os.path.getsize(out_csv) == 0
    with open(out_csv, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            w.writeheader()
        for r in results:
            w.writerow({k: r.get(k) for k in fieldnames})

    print(f"Scored {len(results)} new variants (mode {args.mode}). "
          f"Total in {os.path.basename(out_csv)} now {_count_lines(out_csv)} rows (incl header).")


def _count_lines(p: str) -> int:
    try:
        with open(p, encoding="utf-8") as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())