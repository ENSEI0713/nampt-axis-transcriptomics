#!/usr/bin/env python3
"""Public dataset audit for the NAMPT-NAD exercise/obesity project.

The script queries public NCBI endpoints conservatively and writes both raw
responses and a first-pass candidate dataset table. It intentionally avoids
third-party dependencies so the audit is easy to reproduce.
"""

from __future__ import annotations

import csv
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data_audit" / "raw"
OUT_DIR = ROOT / "data_audit" / "outputs"

NCBI_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
EMAIL = "yanji-research-audit@example.com"
TOOL = "nampt_public_data_audit"


QUERIES = [
    {
        "query_id": "exercise_skeletal_muscle_human_geo",
        "db": "gds",
        "term": '(exercise OR training OR "physical activity" OR HIIT OR endurance OR resistance) AND ("skeletal muscle" OR "vastus lateralis") AND ("Homo sapiens" OR human) AND (transcriptome OR "RNA-seq" OR microarray OR proteome OR metabolome)',
        "theme": "exercise",
    },
    {
        "query_id": "exercise_blood_pbmc_human_geo",
        "db": "gds",
        "term": '(exercise OR training OR "physical activity" OR marathon OR endurance) AND (blood OR PBMC OR leukocyte OR plasma OR serum) AND ("Homo sapiens" OR human) AND (transcriptome OR "RNA-seq" OR microarray OR proteome OR metabolome)',
        "theme": "exercise",
    },
    {
        "query_id": "obesity_adipose_inflammation_geo",
        "db": "gds",
        "term": '(obesity OR obese OR overweight OR "weight loss" OR bariatric) AND (adipose OR "adipose tissue" OR subcutaneous OR visceral) AND (inflammation OR inflammatory OR NAMPT OR visfatin OR NAD OR transcriptome OR "RNA-seq" OR microarray)',
        "theme": "obesity",
    },
    {
        "query_id": "obesity_muscle_metabolism_geo",
        "db": "gds",
        "term": '(obesity OR obese OR overweight OR "insulin resistance" OR "type 2 diabetes") AND ("skeletal muscle" OR "vastus lateralis") AND (inflammation OR mitochondria OR NAD OR NAMPT OR transcriptome OR "RNA-seq" OR microarray)',
        "theme": "obesity",
    },
    {
        "query_id": "weight_loss_exercise_adipose_muscle_geo",
        "db": "gds",
        "term": '("weight loss" OR diet OR caloric OR bariatric OR exercise) AND (adipose OR "skeletal muscle" OR blood OR PBMC) AND (obesity OR obese OR overweight) AND ("Homo sapiens" OR human)',
        "theme": "weight_loss",
    },
    {
        "query_id": "nampt_nad_exercise_pubmed",
        "db": "pubmed",
        "term": '(NAMPT OR visfatin OR PBEF OR NAD OR CD38 OR SIRT1) AND (exercise OR training OR "physical activity") AND (obesity OR inflammation OR "skeletal muscle" OR adipose OR PBMC OR blood)',
        "theme": "literature",
    },
    {
        "query_id": "exercise_muscle_damage_geo",
        "db": "gds",
        "term": '("eccentric exercise" OR "muscle damage" OR DOMS OR recovery OR tendinopathy) AND (human OR "Homo sapiens") AND ("skeletal muscle" OR tendon OR blood) AND (transcriptome OR "RNA-seq" OR microarray)',
        "theme": "repair",
    },
    {
        "query_id": "exercise_microbiome_sra",
        "db": "sra",
        "term": '(exercise OR athlete OR marathon OR "physical activity") AND (microbiome OR metagenome OR gut) AND (human OR "Homo sapiens")',
        "theme": "microbiome_optional",
    },
]


def fetch(url: str, retries: int = 5, delay: float = 0.5) -> bytes:
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=40) as response:
                return response.read()
        except Exception as exc:  # noqa: BLE001 - preserve stdlib-only simplicity
            last_error = exc
            sleep_for = delay * (2**attempt)
            time.sleep(sleep_for)
    raise RuntimeError(f"Failed to fetch after {retries} attempts: {url}\n{last_error}")


def eutils_url(endpoint: str, params: dict[str, str | int]) -> str:
    merged = {"tool": TOOL, "email": EMAIL, **params}
    return f"{NCBI_BASE}/{endpoint}?{urllib.parse.urlencode(merged)}"


def esearch(db: str, term: str, retmax: int = 30) -> list[str]:
    url = eutils_url(
        "esearch.fcgi",
        {"db": db, "term": term, "retmax": retmax, "sort": "relevance", "retmode": "xml"},
    )
    raw = fetch(url)
    return [node.text or "" for node in ET.fromstring(raw).findall(".//Id")]


def esummary(db: str, ids: list[str], query_id: str) -> bytes:
    if not ids:
        return b""
    url = eutils_url("esummary.fcgi", {"db": db, "id": ",".join(ids), "retmode": "xml"})
    raw = fetch(url)
    (RAW_DIR / f"{query_id}_{db}_esummary.xml").write_bytes(raw)
    return raw


def text_of(item: ET.Element, name: str) -> str:
    node = item.find(f"Item[@Name='{name}']")
    if node is None or node.text is None:
        return ""
    return re.sub(r"\s+", " ", node.text).strip()


def list_text(item: ET.Element, name: str) -> list[str]:
    node = item.find(f"Item[@Name='{name}']")
    if node is None:
        return []
    values = []
    for child in node.findall(".//Item"):
        if child.text:
            values.append(re.sub(r"\s+", " ", child.text).strip())
    return values


def infer_flags(text: str) -> dict[str, int | str]:
    t = text.lower()
    tissues = []
    for tissue, terms in {
        "skeletal_muscle": ["skeletal muscle", "vastus lateralis", "myotube", "muscle biopsy"],
        "adipose": ["adipose", "subcutaneous", "visceral", "fat biopsy"],
        "blood_pbmc": ["blood", "pbmc", "leukocyte", "plasma", "serum"],
        "tendon_repair": ["tendon", "tendinopathy", "achilles", "muscle damage", "recovery"],
        "microbiome": ["microbiome", "metagenome", "gut"],
    }.items():
        if any(term in t for term in terms):
            tissues.append(tissue)

    flags = {
        "has_human": int(any(x in t for x in ["homo sapiens", "human", "humans", "healthy males", "subjects"])),
        "has_exercise": int(any(x in t for x in ["exercise", "training", "endurance", "resistance", "hiit", "sprint", "marathon", "physical activity"])),
        "has_obesity": int(any(x in t for x in ["obesity", "obese", "overweight", "bmi", "weight loss", "bariatric", "insulin resistance"])),
        "has_inflammation": int(any(x in t for x in ["inflammation", "inflammatory", "nf-k", "nfkb", "il-6", "il6", "tnf", "crp", "macrophage"])),
        "has_nampt_axis": int(any(x in t for x in ["nampt", "visfatin", "pbef", "nad", "sirt", "cd38", "parp", "ampk"])),
        "has_omics": int(any(x in t for x in ["rna sequencing", "rna-seq", "transcript", "microarray", "proteom", "metabolom", "methylation", "sequencing"])),
        "tissues": ";".join(tissues) if tissues else "unclear",
    }
    return flags


def score_candidate(row: dict[str, str]) -> int:
    score = 0
    score += 2 if row.get("accession") else 0
    score += 2 if row.get("has_human") == "1" else 0
    score += 2 if row.get("has_omics") == "1" else 0
    score += 2 if row.get("tissues") not in {"", "unclear"} else 0
    score += 2 if row.get("has_exercise") == "1" else 0
    score += 2 if row.get("has_obesity") == "1" else 0
    score += 1 if row.get("has_inflammation") == "1" else 0
    score += 1 if row.get("has_nampt_axis") == "1" else 0
    try:
        n_samples = int(row.get("n_samples") or "0")
    except ValueError:
        n_samples = 0
    score += 2 if n_samples >= 20 else 1 if n_samples >= 8 else 0
    return score


def parse_gds_summary(raw: bytes, query: dict[str, str]) -> list[dict[str, str]]:
    if not raw:
        return []
    root = ET.fromstring(raw)
    rows = []
    for doc in root.findall("DocSum"):
        accession = text_of(doc, "Accession") or text_of(doc, "GSE")
        title = text_of(doc, "title")
        summary = text_of(doc, "summary")
        pubmed_ids = ";".join(list_text(doc, "PubMedIds"))
        row = {
            "query_id": query["query_id"],
            "theme": query["theme"],
            "source_db": "GEO/GDS",
            "uid": doc.findtext("Id", default=""),
            "accession": accession,
            "title": title,
            "summary": summary,
            "taxon": text_of(doc, "taxon"),
            "data_type": text_of(doc, "gdsType"),
            "n_samples": text_of(doc, "n_samples"),
            "pubmed_ids": pubmed_ids,
            "ftp_link": text_of(doc, "FTPLink"),
            "url": f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={accession}" if accession else "",
        }
        flags = infer_flags(" ".join([title, summary, row["taxon"], row["data_type"]]))
        row.update({k: str(v) for k, v in flags.items()})
        row["score"] = str(score_candidate(row))
        rows.append(row)
    return rows


def parse_pubmed_summary(raw: bytes, query: dict[str, str]) -> list[dict[str, str]]:
    if not raw:
        return []
    root = ET.fromstring(raw)
    rows = []
    for doc in root.findall("DocSum"):
        uid = doc.findtext("Id", default="")
        title = text_of(doc, "Title")
        journal = text_of(doc, "FullJournalName")
        pubdate = text_of(doc, "PubDate")
        row = {
            "query_id": query["query_id"],
            "theme": query["theme"],
            "source_db": "PubMed",
            "uid": uid,
            "accession": f"PMID:{uid}" if uid else "",
            "title": title,
            "summary": journal,
            "taxon": "",
            "data_type": "literature",
            "n_samples": "",
            "pubmed_ids": uid,
            "ftp_link": "",
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{uid}/" if uid else "",
            "year_or_date": pubdate,
        }
        flags = infer_flags(" ".join([title, journal]))
        row.update({k: str(v) for k, v in flags.items()})
        row["score"] = str(score_candidate(row))
        rows.append(row)
    return rows


def parse_sra_summary(raw: bytes, query: dict[str, str]) -> list[dict[str, str]]:
    if not raw:
        return []
    root = ET.fromstring(raw)
    rows = []
    for doc in root.findall("DocSum"):
        uid = doc.findtext("Id", default="")
        title = text_of(doc, "Title") or text_of(doc, "Study")
        exp_xml = text_of(doc, "ExpXml")
        runs = text_of(doc, "Runs")
        accession_match = re.search(r"(PRJ[EDN][A-Z]?\d+|SRP\d+|ERP\d+|DRP\d+)", " ".join([title, exp_xml, runs]))
        accession = accession_match.group(1) if accession_match else f"SRA:{uid}"
        row = {
            "query_id": query["query_id"],
            "theme": query["theme"],
            "source_db": "SRA",
            "uid": uid,
            "accession": accession,
            "title": title,
            "summary": exp_xml[:1000],
            "taxon": "",
            "data_type": "sequencing",
            "n_samples": "",
            "pubmed_ids": "",
            "ftp_link": "",
            "url": f"https://www.ncbi.nlm.nih.gov/sra/?term={urllib.parse.quote(accession)}",
        }
        flags = infer_flags(" ".join([title, exp_xml, runs]))
        row.update({k: str(v) for k, v in flags.items()})
        row["score"] = str(score_candidate(row))
        rows.append(row)
    return rows


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    fieldnames = [
        "score",
        "theme",
        "source_db",
        "query_id",
        "accession",
        "uid",
        "title",
        "summary",
        "taxon",
        "data_type",
        "n_samples",
        "tissues",
        "has_human",
        "has_exercise",
        "has_obesity",
        "has_inflammation",
        "has_nampt_axis",
        "has_omics",
        "pubmed_ids",
        "ftp_link",
        "url",
        "year_or_date",
    ]
    for row in rows:
        for name in fieldnames:
            row.setdefault(name, "")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    all_rows: list[dict[str, str]] = []
    run_log = []

    for query in QUERIES:
        query_id = query["query_id"]
        db = query["db"]
        print(f"Searching {db}: {query_id}")
        try:
            ids = esearch(db, query["term"], retmax=30)
            (RAW_DIR / f"{query_id}_{db}_ids.json").write_text(json.dumps(ids, indent=2), encoding="utf-8")
            time.sleep(0.4)
            raw = esummary(db, ids, query_id)
            if db == "gds":
                rows = parse_gds_summary(raw, query)
            elif db == "pubmed":
                rows = parse_pubmed_summary(raw, query)
            elif db == "sra":
                rows = parse_sra_summary(raw, query)
            else:
                rows = []
            all_rows.extend(rows)
            run_log.append({"query_id": query_id, "db": db, "ids": len(ids), "rows": len(rows), "status": "ok"})
        except Exception as exc:  # noqa: BLE001
            run_log.append({"query_id": query_id, "db": db, "ids": 0, "rows": 0, "status": f"error: {exc}"})
        time.sleep(1.0)

    # Deduplicate by accession, keeping the highest score and concatenating themes.
    deduped: dict[str, dict[str, str]] = {}
    for row in all_rows:
        key = row.get("accession") or row.get("uid") or row.get("title")
        if key not in deduped:
            deduped[key] = row
            continue
        existing = deduped[key]
        existing_score = int(existing.get("score") or 0)
        new_score = int(row.get("score") or 0)
        if new_score > existing_score:
            row["theme"] = ";".join(sorted(set((existing.get("theme", "") + ";" + row.get("theme", "")).split(";")) - {""}))
            deduped[key] = row
        else:
            existing["theme"] = ";".join(sorted(set((existing.get("theme", "") + ";" + row.get("theme", "")).split(";")) - {""}))

    rows = sorted(deduped.values(), key=lambda x: int(x.get("score") or 0), reverse=True)
    write_csv(rows, OUT_DIR / "candidate_public_datasets.csv")
    (OUT_DIR / "audit_run_log.json").write_text(json.dumps(run_log, indent=2), encoding="utf-8")
    print(f"Wrote {len(rows)} deduplicated candidates to {OUT_DIR / 'candidate_public_datasets.csv'}")


if __name__ == "__main__":
    main()
