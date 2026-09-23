#!/usr/bin/env python3
"""Convert manuscript_full_en_v1.md into a LaTeX manuscript for xelatex PDF build.

Output: data_audit/outputs/submission_pack/manuscript_full_en_v1.tex
Run xelatex afterwards.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data_audit/outputs/manuscript_full_en_v1.md"
OUT = ROOT / "data_audit/outputs/submission_pack/manuscript_full_en_v1.tex"


def esc_text(t: str) -> str:
    """Escape LaTeX special chars, applied AFTER markdown->LaTeX replacements."""
    # do not escape { } (we may have \textbf{...}); escape the rest
    t = t.replace("\\", r"\textbackslash{}")
    t = t.replace("&", r"\&").replace("%", r"\%").replace("#", r"\#")
    t = t.replace("_", r"\_").replace("$", r"\$")
    t = t.replace("^", r"\textasciicircum{}").replace("~", r"\textasciitilde{}")
    return t


def inline(t: str) -> str:
    """markdown inline -> latex inline (bold, sup, italic, code)."""
    t = re.sub(r"\*\*(.+?)\*\*", lambda m: r"\textbf{" + m.group(1) + "}", t)
    t = re.sub(r"<sup>([^<]*)</sup>", lambda m: r"\textsuperscript{" + m.group(1) + "}", t)
    t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", lambda m: r"\textit{" + m.group(1) + "}", t)
    t = re.sub(r"`([^`]+)`", r"\texttt{\1}", t)
    return esc_text(t)


def is_sep_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c.strip()) for c in cells if c.strip())


def convert(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    out.append(r"\documentclass[11pt]{article}")
    out.append(r"\usepackage[UTF8]{ctex}")
    out.append(r"\usepackage[margin=2.5cm]{geometry}")
    out.append(r"\usepackage{booktabs}")
    out.append(r"\usepackage{array}")
    out.append(r"\usepackage{amsmath}")
    out.append(r"\setlength{\parindent}{0pt}")
    out.append(r"\setlength{\parskip}{4pt}")
    out.append(r"\begin{document}")
    out.append(r"\begin{center}{\Large\bfseries State-dependent NAMPT-axis transcriptional programs in obesity and exercise}\end{center}")
    out.append(r"\begin{center}Yanjing Chen, Zhenyu Shao, Min Zhang, Yan Zhang --- manuscript for submission\end{center}")
    out.append(r"\vspace{4pt}\hrule\vspace{8pt}")

    i = 0
    n = len(lines)
    while i < n:
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        if s == "---":
            out.append(r"\vspace{4pt}\hrule\vspace{8pt}")
            i += 1
            continue
        if s.startswith("# "):
            i += 1
            continue
        if s.startswith("## "):
            out.append(r"\section*{" + inline(s[3:].strip()) + "}")
            i += 1
            continue
        if s.startswith("### "):
            out.append(r"\subsection*{" + inline(s[4:].strip()) + "}")
            i += 1
            continue
        # table block: consecutive | lines
        if s.startswith("|"):
            block: list[str] = []
            while i < n and lines[i].strip().startswith("|"):
                block.append(lines[i].strip())
                i += 1
            rows = []
            for ln in block:
                cells = [c.strip() for c in ln.strip("|").split("|")]
                if is_sep_row(cells):
                    continue
                rows.append(cells)
            if rows:
                ncols = len(rows[0])
                out.append(r"\begin{table}[h!]")
                out.append(r"\centering")
                out.append(r"\begin{tabular}{" + "l" * ncols + "}")
                out.append(r"\toprule")
                out.append(" & ".join(inline(c) for c in rows[0]) + r" \\")
                out.append(r"\midrule")
                for row in rows[1:]:
                    # pad short rows
                    row = row + [""] * (ncols - len(row))
                    out.append(" & ".join(inline(c) for c in row) + r" \\")
                out.append(r"\bottomrule")
                out.append(r"\end{tabular}")
                out.append(r"\end{table}")
                out.append(r"\par\vspace{4pt}")
            continue
        # lists
        if s.startswith(("- ", "* ")):
            items = []
            while i < n and (lines[i].strip().startswith("- ") or lines[i].strip().startswith("* ")):
                items.append(lines[i].strip()[2:].strip())
                i += 1
            out.append(r"\begin{itemize}\setlength{\itemsep}{1pt}")
            for it in items:
                out.append(r"\item " + inline(it))
            out.append(r"\end{itemize}")
            continue
        # ordered list
        m = re.match(r"^\d+\.\s+(.*)$", s)
        if m:
            out.append(r"\begin{enumerate}\setlength{\itemsep}{1pt}")
            while i < n:
                mm = re.match(r"^\d+\.\s+(.*)$", lines[i].strip())
                if not mm:
                    break
                out.append(r"\item " + inline(mm.group(1).strip()))
                i += 1
            out.append(r"\end{enumerate}")
            continue
        # blockquote
        if s.startswith(">"):
            out.append(r"\begin{quote}" + inline(s.lstrip(">").strip()) + r"\end{quote}")
            i += 1
            continue
        # normal paragraph
        out.append(inline(s))
        out.append("")
        i += 1

    out.append(r"\end{document}")
    return "\n".join(out)


if __name__ == "__main__":
    tex = convert(SRC.read_text(encoding="utf-8"))
    OUT.write_text(tex, encoding="utf-8")
    print(f"wrote {OUT} ({len(tex)} chars)")
