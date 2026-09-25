#!/usr/bin/env python3
"""Compose the three audited tidyplots SVG panels into one vector SVG page."""
from __future__ import annotations
import re
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data_audit/outputs/figures_phase3_tidyplots"
OUT = SRC / "Figure3_exercise_tidyplots_composite.svg"

PANEL_W = 183.0
PANEL_H = 72.0
GAP = 5.0
TOTAL_H = PANEL_H * 2 + GAP


def inner(svg_path: Path, x: float, y: float, label: str) -> str:
    text = svg_path.read_text(encoding="utf-8")
    text = re.sub(r"<\?xml[^>]*\?>", "", text)
    root = ET.fromstring(text)
    # Preserve the panel as a nested SVG so all paths/text remain vector.
    viewbox = root.attrib.get("viewBox", "0 0 518.74 204.09")
    content = "".join(ET.tostring(child, encoding="unicode") for child in list(root))
    return f'<svg x="{x}mm" y="{y}mm" width="{PANEL_W}mm" height="{PANEL_H}mm" viewBox="{viewbox}" preserveAspectRatio="none" aria-label="{label}">{content}</svg>'

panels = [
    inner(SRC / "Figure3_exercise_tidyplots_panel_a.svg", 0, 0, "Panel a: exercise NAMPT z forest plot"),
    inner(SRC / "Figure3_exercise_tidyplots_panel_b.svg", PANEL_W, 0, "Panel b: immediate to 24 hour balance trajectory"),
    inner(SRC / "Figure3_exercise_tidyplots_panel_c.svg", 0, PANEL_H + GAP, "Panel c: four metric exercise heatmap"),
]
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{PANEL_W*2}mm" height="{TOTAL_H}mm" viewBox="0 0 {PANEL_W*2} {TOTAL_H}" role="img" aria-labelledby="title desc">
<title id="title">Figure 3. Exercise-induced NAMPT-axis dynamics</title>
<desc id="desc">Three vector panels showing 13 exercise contrasts, immediate to 24 hour balance trajectories, and four NAMPT-axis metrics.</desc>
<rect width="100%" height="100%" fill="white"/>
{''.join(panels)}
</svg>'''
OUT.write_text(svg, encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
