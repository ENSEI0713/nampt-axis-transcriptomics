#!/usr/bin/env python3
"""Download first-priority public GEO processed files.

The manifest is intentionally explicit so the first analysis batch is stable
and auditable. Large raw archives are left out until a processed matrix is not
available or the analysis requires re-processing from raw data.
"""

from __future__ import annotations

import csv
import hashlib
import json
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data_audit" / "downloads" / "geo_processed"
OUT_DIR = ROOT / "data_audit" / "outputs"


FILES = [
    {
        "accession": "GSE312393",
        "label": "24h_exercise_tpm",
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE312nnn/GSE312393/suppl/GSE312393_human_gene_24H_exercise_tpm.tsv.gz",
    },
    {
        "accession": "GSE312393",
        "label": "6weeks_tpm",
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE312nnn/GSE312393/suppl/GSE312393_human_gene_6weeks_tpm.tsv.gz",
    },
    {
        "accession": "GSE318937",
        "label": "gene_per_sample_order",
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE318nnn/GSE318937/suppl/GSE318937_genePerSampleOrder_FortitudeUnil.csv.gz",
    },
    {
        "accession": "GSE305038",
        "label": "inactive_post_vs_pre_edger",
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE305nnn/GSE305038/suppl/GSE305038_20250714_M008795_edgeRglm_Counts_Inactive_Post-Inactive_Pre.xlsx",
    },
    {
        "accession": "GSE305038",
        "label": "normal_post_vs_pre_edger",
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE305nnn/GSE305038/suppl/GSE305038_20250714_M008795_edgeRglm_Counts_Normal_Post-Normal_Pre.xlsx",
    },
    {
        "accession": "GSE292369",
        "label": "transcript_counts",
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE292nnn/GSE292369/suppl/GSE292369_Partek_KE_recovery_transcript_counts.txt.gz",
    },
    {
        "accession": "GSE292369",
        "label": "deseq2_normalized",
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE292nnn/GSE292369/suppl/GSE292369_Partek_KE_recovery_Normalization_Outliers_Removed_Deseq2.txt.gz",
    },
    {
        "accession": "GSE32575",
        "label": "non_normalized",
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE32nnn/GSE32575/suppl/GSE32575_non-normalized.txt.gz",
    },
    {
        "accession": "GSE272133",
        "label": "processed_rnaseq",
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE272nnn/GSE272133/suppl/GSE272133_processed_data_RNASeq.tsv.gz",
    },
    {
        "accession": "GSE294150",
        "label": "expression_grch38_gene",
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE294nnn/GSE294150/suppl/GSE294150_Expression_Profile.GRCh38.gene.txt.gz",
    },
    {
        "accession": "GSE282850",
        "label": "vst_counts",
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE282nnn/GSE282850/suppl/GSE282850_tovar-nishino_rnaseq_vst_counts.txt.gz",
    },
    {
        "accession": "GSE282850",
        "label": "raw_counts",
        "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE282nnn/GSE282850/suppl/GSE282850_tovar-nishino_rnaseq_raw_counts.txt.gz",
    },
]


def filename_from_url(url: str) -> str:
    return url.rsplit("/", 1)[-1]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(url: str, path: Path) -> None:
    tmp_path = path.with_suffix(path.suffix + ".part")
    with urllib.request.urlopen(url, timeout=120) as response:
        with tmp_path.open("wb") as handle:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                handle.write(chunk)
    tmp_path.replace(path)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    rows = []
    for item in FILES:
        accession_dir = DATA_DIR / item["accession"]
        accession_dir.mkdir(parents=True, exist_ok=True)
        filename = filename_from_url(item["url"])
        dest = accession_dir / filename
        status = "exists" if dest.exists() else "downloaded"
        error = ""
        try:
            if not dest.exists():
                print(f"Downloading {item['accession']} {filename}")
                download(item["url"], dest)
                time.sleep(0.3)
            size_bytes = dest.stat().st_size
            sha256 = sha256_file(dest)
        except Exception as exc:  # noqa: BLE001 - audit script records failures
            status = "error"
            error = str(exc)
            size_bytes = 0
            sha256 = ""
        rows.append(
            {
                "accession": item["accession"],
                "label": item["label"],
                "url": item["url"],
                "local_path": str(dest.relative_to(ROOT)),
                "size_bytes": size_bytes,
                "sha256": sha256,
                "status": status,
                "error": error,
            }
        )

    manifest_csv = OUT_DIR / "geo_processed_download_manifest.csv"
    fieldnames = ["accession", "label", "url", "local_path", "size_bytes", "sha256", "status", "error"]
    with manifest_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    (OUT_DIR / "geo_processed_download_manifest.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(f"Wrote manifest to {manifest_csv}")


if __name__ == "__main__":
    main()
