#!/usr/bin/env python3
"""Test the Evo2-40B hosted generate endpoint and record schema + reproducibility.

NVIDIA NIM endpoint: https://health.api.nvidia.com/v1/biology/arc/evo2-40b/generate

Tests connectivity, documents the real input/output shapes, checks
token-probability and logit surfaces against the published docs, and writes a
structured log for reproducibility.
"""

from __future__ import annotations

import json
import os
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data_audit" / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

API_KEY = os.environ.get("NVIDIA_API_KEY") or os.environ.get("NVCF_RUN_KEY")
ENDPOINT = "https://health.api.nvidia.com/v1/biology/arc/evo2-40b/generate"

# Short synthetic for smoke-test / latency.
SYNTHETIC_20MER = "ACGTACGTACGTACGTACGT"

# NAMPT promoter flank (~80 bp regulatory window near gene body).
NAMPT_PROMOTER_FLANK = (
    "TGGGGTGGGGAGGGGTGGGGTGGGGAGGGGCGGGGCGGGGCGGGGCGGGGCGGGGCGGGGC"
    "GGGGCGGGGCGGGGCG"
)

SEQUENCES = {
    "synthetic_20mer": SYNTHETIC_20MER,
    "nampt_promoter_flank": NAMPT_PROMOTER_FLANK,
}


def build_payload(
    sequence: str,
    num_tokens: int = 10,
    temperature: float = 0.7,
    top_k: int = 4,
    top_p: float = 0.9,
    random_seed: int = 42,
    enable_logits: bool = True,
    enable_sampled_probs: bool = True,
) -> bytes:
    body = {
        "sequence": sequence,
        "num_tokens": num_tokens,
        "temperature": temperature,
        "top_k": top_k,
        "top_p": top_p,
        "random_seed": random_seed,
        "enable_logits": enable_logits,
        "enable_sampled_probs": enable_sampled_probs,
    }
    return json.dumps(body).encode("utf-8")


def post(endpoint: str, api_key: str, payload: bytes, timeout: int = 90) -> dict:
    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
    elapsed_s = time.perf_counter() - t0
    result = json.loads(raw)
    result["_meta"] = {
        "status_code": resp.status,
        "elapsed_s": round(elapsed_s, 3),
        "content_type": resp.headers.get("Content-Type", ""),
    }
    return result


def inspect_structure(obj, prefix: str = "") -> list[str]:
    """Flatten JSON structure into shape hints (type + list-lengths)."""
    lines: list[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            path = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                lines.append(f"{path}: dict[{len(v)}]")
                lines.extend(inspect_structure(v, path))
            elif isinstance(v, list):
                hint = f"list[{len(v)}]"
                if v and isinstance(v[0], (int, float)):
                    hint += " (numeric)"
                elif v and isinstance(v[0], str):
                    hint += " (string)"
                elif v and isinstance(v[0], dict):
                    hint += " (objects)"
                lines.append(f"{path}: {hint}")
                if v and isinstance(v[0], dict):
                    lines.extend(inspect_structure(v[0], f"{path}[0]"))
            elif isinstance(v, str):
                lines.append(f"{path}: str (len={len(v)})")
            elif isinstance(v, (int, float)):
                lines.append(f"{path}: {type(v).__name__} = {v}")
            elif isinstance(v, bool):
                lines.append(f"{path}: bool = {v}")
            elif v is None:
                lines.append(f"{path}: null")
            else:
                lines.append(f"{path}: {type(v).__name__}")
    return lines


def summarize_logits(logits: list) -> dict:
    """Return per-position logit stats (min, max, mean, most-active index)."""
    summary = []
    for i, pos in enumerate(logits):
        if not pos:
            summary.append({"position": i, "error": "empty"})
            continue
        max_idx = max(range(len(pos)), key=lambda j: pos[j])
        summary.append({
            "position": i,
            "len": len(pos),
            "min": round(min(pos), 4),
            "max": round(max(pos), 4),
            "mean": round(sum(pos) / len(pos), 4),
            "argmax_idx": max_idx,
            "argmax_value": round(pos[max_idx], 4),
        })
    return {"positions": len(summary), "per_position": summary}


def main() -> None:
    if not API_KEY:
        raise SystemExit("Set NVIDIA_API_KEY or NVCF_RUN_KEY before calling Evo2-40B.")

    results: list[dict] = []
    run_ts = datetime.now(timezone.utc).isoformat()

    for label, seq in SEQUENCES.items():
        print(f"\n{'='*60}")
        print(f"Testing {label}  (len={len(seq)})")
        print(f"{'='*60}")

        try:
            payload = build_payload(seq)
            resp = post(ENDPOINT, API_KEY, payload)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode(errors="replace")
            resp = {
                "_error": f"HTTP {exc.code}",
                "_body": body[:2000],
                "_meta": {"status_code": exc.code, "elapsed_s": 0},
            }
        except Exception as exc:
            resp = {"_error": str(exc), "_meta": {"status_code": 0, "elapsed_s": 0}}

        meta = resp.pop("_meta", {})
        structure = inspect_structure(resp)

        logits_summary = None
        if "logits" in resp and isinstance(resp["logits"], list):
            try:
                logits_summary = summarize_logits(resp["logits"])
            except Exception:
                logits_summary = {"error": "summarize_logits failed"}

        entry = {
            "run_ts": run_ts,
            "sequence_label": label,
            "sequence_len": len(seq),
            "sequence_first_30": seq[:30],
            "meta": meta,
            "structure": structure,
            "logits_summary": logits_summary,
        }

        if "generated_sequence" in resp:
            entry["generated_sequence"] = resp["generated_sequence"]
            gen = resp["generated_sequence"]
            if isinstance(gen, str):
                entry["generated_tokens"] = len(gen)

        if "sampled_probs" in resp:
            sp = resp["sampled_probs"]
            if isinstance(sp, list) and sp:
                entry["sampled_probs_preview"] = sp[:5]

        results.append(entry)

        print(f"  status: {meta.get('status_code', '?')}  "
              f"time: {meta.get('elapsed_s', '?')}s")
        if "generated_sequence" in resp:
            gen = resp["generated_sequence"]
            if isinstance(gen, str):
                print(f"  generated: {gen[:60]}{'...' if len(gen) > 60 else ''}")
        if logits_summary:
            print(f"  logit positions: {logits_summary['positions']}")
        sp = resp.get("sampled_probs", [])
        if sp and isinstance(sp, list):
            print(f"  sampled_probs (first 3): {sp[:3]}")
        if "_error" in resp:
            print(f"  ERROR: {resp['_error']}")
            if "_body" in resp:
                print(f"  body: {resp['_body'][:500]}")

    log_path = OUT_DIR / "evo2_endpoint_test_log.json"
    log_path.write_text(json.dumps(results, indent=2, ensure_ascii=False),
                        encoding="utf-8")
    print(f"\nFull log written to {log_path}")


if __name__ == "__main__":
    main()

