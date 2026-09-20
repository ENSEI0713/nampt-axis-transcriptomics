#!/usr/bin/env python3
"""Merge external public eQTL + GWAS evidence for Evo2-scored NAMPT-axis
candidate variants and assign evidence tiers.

Evidence sources (validated endpoints, 2026-09-18):
  * GTEx REST v2 (eQTL):
      GET https://gtexportal.org/api/v2/association/singleTissueEqtl
          ?variantId=chr{chrom}_{pos}_{ref}_{alt}_b38
          &tissueSiteDetailId={tissue}
    Fields used: data[].pValue (float), data[].geneSymbol,
                 data[].nes (effect size), data[].tissueSiteDetailId,
                 data[].datasetId.
  * GWAS Catalog REST (associations by rsid):
      GET https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{rsid}/associations
    Fields used: _embedded.associations[].pvalueMantissa / pvalueExponent
                 (p = mantissa * 10**exponent), .description (trait),
                 .loci[].strongestRiskAlleles[].riskAlleleName,
                 .pvalueDescription.

Coordinate source: candidates_priority.csv carries the TRUE variant
coordinates (position/ref/alt). Do NOT use windows.bed window starts — they
are window-start coordinates, not variant coordinates.

Tier rules (protocol §8, applied to each variant):

  Evo2 perturbation (E):  |Score A delta| >= 4  OR  Score B strand-consistent
                          (fwd & rc same sign, only defined for shortlist).
  eQTL evidence (Q):      any relevant tissue with GTEx pValue < 1e-4.
  GWAS evidence (G):      any GWAS Catalog association with p < 5e-8.

  Tier A: E and Q and G
  Tier B: E and (Q or G)
  Tier C: E and neither Q nor G (exploratory only)
  Excluded: no Evo2 perturbation and no external evidence

Notes (recorded honestly, not papered over):
  * The Tier-A shortlist (104 variants) is dominated by rare variants; GTEx
    eQTL are computed for common variants only, so most shortlist variants are
    expected to have no GTEx hit. That is a documented expectation, not a bug.
  * eQTL/GWAS association != causality. Tier A still requires experimental
    validation. Public data are not for individual diagnosis or exercise
    prescription.
  * API failures: one retry, then recorded as NA (missing evidence), never
    fabricated.

Outputs:
  data_audit/raw/gtex_{rsid}_{tissue}.json      (cached responses)
  data_audit/raw/gwas_{rsid}.json               (cached responses)
  data_audit/outputs/evo2/tiers.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import time
import urllib.request

BASE = os.path.join(os.path.dirname(__file__), "..", "data_audit")
RAW_DIR = os.path.join(BASE, "raw")
OUT_DIR = os.path.join(BASE, "outputs", "evo2")
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

UA = "evo2-40b-research/0.1 (NAMPT-NAD axis; contact local)"
GTEX_URL = "https://gtexportal.org/api/v2/association/singleTissueEqtl"
GWAS_URL = "https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{rsid}/associations"
TISSUES = [
    "Muscle_Skeletal",
    "Adipose_Subcutaneous",
    "Adipose_Visceral_Omentum",
    "Whole_Blood",
]
GTEX_P_THRESH = 1e-4
GWAS_P_THRESH = 5e-8
EVO2_ABS_A_THRESH = 4.0


def fetch(url: str, timeout: int = 40) -> dict | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def fetch_with_retry(url: str, cache_path: str | None = None,
                     retries: int = 2, backoff: float = 3.0) -> dict | None:
    """Fetch with retries and backoff; cache successes AND failures to disk.

    A cached failure is stored as an explicit empty marker so a re-run does
    not hammer a throttling endpoint (e.g. GTEx HTTP 500) for the same
    variant again.
    """
    if cache_path and os.path.exists(cache_path):
        with open(cache_path, encoding="utf-8") as f:
            return json.load(f)
    for attempt in range(retries + 1):
        try:
            data = fetch(url)
            if cache_path:
                with open(cache_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False)
            return data
        except Exception as e:
            if attempt < retries:
                print(f"    fetch retry {attempt+1}/{retries} ({type(e).__name__}: {str(e)[:80]}), "
                      f"waiting {backoff}s", flush=True)
                time.sleep(backoff)
                backoff *= 2
                continue
            # Exhausted retries: cache the failure so we never touch it again.
            if cache_path:
                with open(cache_path, "w", encoding="utf-8") as f:
                    json.dump({"__fetch_failed__": True}, f)
            print(f"    fetch fail after {retries} retries: "
                  f"{type(e).__name__}: {str(e)[:120]}", flush=True)
    return None


def variant_id(v: dict) -> str:
    alt = v["alt"].split(",")[0].strip()
    return f"chr{v['chromosome']}_{v['position']}_{v['ref']}_{alt}_b38"


def gtex_evidence(v: dict) -> dict:
    """Query GTEx across relevant tissues; return min-p eQTL summary."""
    min_p = None
    best = None
    genes = set()
    for tissue in TISSUES:
        cache = os.path.join(RAW_DIR, f"gtex_{v['rsid']}_{tissue}.json")
        url = (f"{GTEX_URL}?variantId={variant_id(v)}"
               f"&tissueSiteDetailId={tissue}")
        data = fetch_with_retry(url, cache)
        if not data:
            continue
        for item in data.get("data", []):
            p = item.get("pValue")
            if p is None:
                continue
            p = float(p)
            if p < 1e-300:
                p = 1e-300
            genes.add(item.get("geneSymbol") or "")
            if min_p is None or p < min_p:
                min_p = p
                best = item
        time.sleep(0.2)
    return {
        "gtex_min_p": min_p,
        "gtex_nes": best.get("nes") if best else None,
        "gtex_genes": ";".join(sorted(g for g in genes if g)) or "",
        "gtex_best_tissue": best.get("tissueSiteDetailId") if best else "",
    }


def gwas_evidence(rsid: str) -> dict:
    """Query GWAS Catalog associations; return min p and traits."""
    cache = os.path.join(RAW_DIR, f"gwas_{rsid}.json")
    url = GWAS_URL.format(rsid=rsid)
    data = fetch_with_retry(url, cache)
    min_p = None
    traits = set()
    risk_alleles = set()
    if not data:
        # Cache an explicit empty marker so re-runs skip the 404 retry noise.
        if not os.path.exists(cache):
            with open(cache, "w", encoding="utf-8") as f:
                json.dump({}, f)
        return {"gwas_min_p": None, "gwas_traits": "", "gwas_risk_allele": ""}
    for a in data.get("_embedded", {}).get("associations", []):
        mant = a.get("pvalueMantissa")
        exp = a.get("pvalueExponent")
        if mant is not None and exp is not None:
            p = float(mant) * (10.0 ** int(exp))
            if min_p is None or p < min_p:
                min_p = p
        desc = a.get("description") or a.get("pvalueDescription") or ""
        if desc:
            traits.add(desc.strip())
        for locus in a.get("loci", []) or []:
            for ra in locus.get("strongestRiskAlleles", []) or []:
                name = ra.get("riskAlleleName")
                if name:
                    risk_alleles.add(name)
    return {
        "gwas_min_p": min_p,
        "gwas_traits": ";".join(sorted(traits)[:5]),
        "gwas_risk_allele": ";".join(sorted(risk_alleles)[:5]),
    }


def evo2_perturbation(row_scores: dict) -> tuple[bool, str]:
    """True if Evo2 signal qualifies. Returns (ok, reason)."""
    sA = row_scores.get("scoreA_delta")
    reason = ""
    if sA is not None and abs(float(sA)) >= EVO2_ABS_A_THRESH:
        return True, f"|scoreA|={abs(float(sA)):.2f}>=4"
    sB = row_scores.get("scoreB_strand_consistent")
    if sB is not None and str(sB).lower() in ("true", "1"):
        return True, "scoreB strand-consistent"
    return False, reason


def tier_of(row_scores: dict) -> tuple[str, str]:
    e, e_reason = evo2_perturbation(row_scores)
    q = bool(row_scores.get("gtex_min_p")) and float(row_scores["gtex_min_p"]) < GTEX_P_THRESH
    g = bool(row_scores.get("gwas_min_p")) and float(row_scores["gwas_min_p"]) < GWAS_P_THRESH
    if e and q and g:
        return "A", f"E({e_reason});Q(gtex p={row_scores['gtex_min_p']:.2e});G(gwas p={row_scores['gwas_min_p']:.2e})"
    if e and (q or g):
        if q:
            return "B", f"E({e_reason});Q(gtex p={row_scores['gtex_min_p']:.2e})"
        return "B", f"E({e_reason});G(gwas p={row_scores['gwas_min_p']:.2e})"
    if e:
        return "C", f"E({e_reason});no external support"
    if q or g:
        # External evidence exists but Evo2 shows no perturbation. Not an
        # Evo2-recommended candidate; keep it labeled separately from variants
        # with NO evidence at all (protocol §8: Evo2-only candidates are
        # excluded; the mirror case gets its own label for honesty).
        return "External-only", "external eQTL/GWAS evidence; no Evo2 perturbation"
    return "Excluded", "no Evo2 perturbation, no external evidence"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()

    cand_path = os.path.join(OUT_DIR, "candidates_priority.csv")
    scores_a_path = os.path.join(OUT_DIR, "scores.csv")
    scores_b_path = os.path.join(OUT_DIR, "scores_B.csv")
    out_path = os.path.join(OUT_DIR, "tiers.csv")

    with open(cand_path, encoding="utf-8") as f:
        candidates = list(csv.DictReader(f))
    scoreA = {}
    if os.path.exists(scores_a_path):
        with open(scores_a_path, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                scoreA[r["rsid"]] = float(r["delta_surprisal"])
    scoreB = {}
    if os.path.exists(scores_b_path):
        with open(scores_b_path, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                scoreB[r["rsid"]] = r  # keep full row

    # Resume: skip rsids already written
    done = set()
    if args.resume and os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                done.add(r["rsid"])

    todo = [c for c in candidates if c["rsid"] not in done]
    if args.limit and args.limit > 0:
        todo = todo[: args.limit]
    print(f"Merging {len(todo)} variants (limit={args.limit}, resume={args.resume})...", flush=True)

    out_rows = []
    for i, v in enumerate(todo, 1):
        rsid = v["rsid"]
        print(f"  [{i}/{len(todo)}] {rsid} {v['gene_window']} ({variant_id(v)})", flush=True)
        gtex = gtex_evidence(v)
        gwas = gwas_evidence(rsid)
        b = scoreB.get(rsid, {})
        row = {
            "rsid": rsid,
            "gene_window": v["gene_window"],
            "chrom": v["chromosome"],
            "pos": v["position"],
            "ref": v["ref"],
            "alt": v["alt"],
            "consequence": v.get("consequence", ""),
            "scoreA_delta": scoreA.get(rsid, ""),
            "scoreB_mean": b.get("delta_pll_mean", ""),
            "scoreB_strand_consistent": b.get("strand_consistent", ""),
        }
        row.update(gtex)
        row.update(gwas)
        tier, why = tier_of(row)
        row["tier"] = tier
        row["tier_reason"] = why
        out_rows.append(row)
        print(f"      tier={tier}  {why}  (gtex_min_p={row['gtex_min_p']} gwas_min_p={row['gwas_min_p']})", flush=True)

    # Append to tiers.csv
    fields = [
        "rsid", "gene_window", "chrom", "pos", "ref", "alt", "consequence",
        "scoreA_delta", "scoreB_mean", "scoreB_strand_consistent",
        "gtex_min_p", "gtex_nes", "gtex_genes", "gtex_best_tissue",
        "gwas_min_p", "gwas_traits", "gwas_risk_allele",
        "tier", "tier_reason",
    ]
    write_header = not os.path.exists(out_path) or os.path.getsize(out_path) == 0
    with open(out_path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if write_header:
            w.writeheader()
        for r in out_rows:
            w.writerow({k: r.get(k, "") for k in fields})

    print(f"Wrote {len(out_rows)} rows -> {out_path}", flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
