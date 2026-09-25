#!/usr/bin/env python3
from pathlib import Path
from xml.etree import ElementTree as ET
import re
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'data_audit/outputs/figures_phase3_tidyplots'; OUT=SRC/'Figure5_obesity_tidyplots_composite.svg'; W,H,G=183,72,5
items=[('Figure5_obesity_tidyplots_panel_a.svg','Panel a: obesity and weight-loss contrasts'),('Figure5_obesity_tidyplots_panel_b.svg','Panel b: post-bariatric monocyte remodeling'),('Figure5_obesity_tidyplots_panel_c.svg','Panel c: skeletal-muscle response by disease state')]
def one(name,y,label):
 t=re.sub(r'<\?xml[^>]*\?>','', (SRC/name).read_text(encoding='utf-8')); r=ET.fromstring(t); vb=r.attrib.get('viewBox','0 0 518.74 204.09'); c=''.join(ET.tostring(x,encoding='unicode') for x in list(r)); return f'<svg x="0" y="{y}mm" width="{W}mm" height="{H}mm" viewBox="{vb}" preserveAspectRatio="none" aria-label="{label}">{c}</svg>'
total=3*H+2*G; body=''.join(one(n,i*(H+G),l) for i,(n,l) in enumerate(items)); OUT.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{total}mm" viewBox="0 0 {W} {total}" role="img"><title>Figure 5. Obesity and weight-loss tissue and disease-background dependence</title><rect width="100%" height="100%" fill="white"/>{body}</svg>',encoding='utf-8'); print('wrote',OUT,OUT.stat().st_size)
