#!/usr/bin/env python3
"""Convert the English manuscript Markdown to a submission-ready .docx.

Reads data_audit/outputs/manuscript_full_en_v1.md, converts headings/paragraphs/
lists/tables/superscript citations to Word styles, and writes
data_audit/outputs/submission_pack/manuscript_full_en_v1.docx.
"""
from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data_audit/outputs/manuscript_full_en_v1.md"
OUT = ROOT / "data_audit/outputs/submission_pack/manuscript_full_en_v1.docx"


def parse_table(lines: list[str]) -> str:
    """Turn a markdown pipe table (with header + separator row) into lines."""
    body: list[str] = []
    for ln in lines:
        if ln.strip().startswith("|"):
            body.append(ln)
        else:
            continue
    return "\n".join(body)


def convert(md: str) -> None:
    doc = Document()
    # base style
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(11)

    lines = md.splitlines()
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].rstrip()
        stripped = line.strip()

        # skip horizontal rules
        if stripped in ("---", "***", "___"):
            i += 1
            continue

        # headings
        if stripped.startswith("#"):
            hashes = len(stripped) - len(stripped.lstrip("#"))
            level = min(hashes, 4)
            text = stripped.lstrip("#").strip()
            doc.add_heading(text, level=level)
            i += 1
            continue

        # table block: collect consecutive | lines
        if stripped.startswith("|"):
            block: list[str] = []
            while i < n and lines[i].strip().startswith("|"):
                block.append(lines[i].strip())
                i += 1
            # drop separator row (---)
            rows = [ln for ln in block if not set(ln.replace("|", "").replace(" ", "")) <= set("-:")]
            if rows:
                doc.add_paragraph(parse_table(rows), style=None)
            continue

        # blockquote
        if stripped.startswith(">"):
            text = stripped.lstrip(">").strip()
            p = doc.add_paragraph()
            run = p.add_run(text)
            run.italic = True
            i += 1
            continue

        # unordered list
        if stripped.startswith(("- ", "* ", "+ ")):
            text = stripped[2:].strip()
            doc.add_paragraph(text, style="List Bullet")
            i += 1
            continue

        # ordered list
        if stripped[:2] in ("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9."):
            text = "." in stripped and stripped.split(". ", 1)[1] or stripped
            doc.add_paragraph(text, style="List Number")
            i += 1
            continue

        # empty line
        if not stripped:
            i += 1
            continue

        # normal paragraph with inline formatting
        text = inline_format(line)
        p = doc.add_paragraph()
        add_runs(p, text)
        i += 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print(f"wrote {OUT}")


def inline_format(text: str) -> str:
    """Convert markdown inline markup to plain text with markers handled by add_runs."""
    # bold **x** -> \x01B\x02x\x01/B\x02 ; italics *x* -> \x01I\x02x\x01/I\x02 ; code `x` stays as x
    import re

    def b_repl(m):
        return "\x01B\x02" + m.group(1) + "\x01/B\x02"

    def i_repl(m):
        return "\x01I\x02" + m.group(1) + "\x01/I\x02"

    # bold
    text = re.sub(r"\*\*(.+?)\*\*", b_repl, text)
    # italic
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", i_repl, text)
    # code spans: keep plain
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return text


def add_runs(p, text: str) -> None:
    """Parse \x01\x02 markers into bold/italic runs; superscript <sup> handled too."""
    import re

    # split on markers
    tokens = re.split(r"(\x01[B/I]\x02|\x01/[B/I]\x02)", text)
    mode: dict[str, bool] = {"B": False, "I": False}
    for tok in tokens:
        if tok == "\x01B\x02":
            mode["B"] = True
            continue
        if tok == "\x01/B\x02":
            mode["B"] = False
            continue
        if tok == "\x01I\x02":
            mode["I"] = True
            continue
        if tok == "\x01/I\x02":
            mode["I"] = False
            continue
        if not tok:
            continue
        # handle superscript citations <sup>[n]</sup>
        parts = re.split(r"(<sup>[^<]*</sup>)", tok)
        for part in parts:
            if not part:
                continue
            m = re.fullmatch(r"<sup>([^<]*)</sup>", part)
            if m:
                r = p.add_run(m.group(1))
                r.font.superscript = True
                if mode["B"]:
                    r.bold = True
                if mode["I"]:
                    r.italic = True
            else:
                r = p.add_run(part)
                if mode["B"]:
                    r.bold = True
                if mode["I"]:
                    r.italic = True


if __name__ == "__main__":
    convert(SRC.read_text(encoding="utf-8"))
    print("done")