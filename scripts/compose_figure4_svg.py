#!/usr/bin/env python3
from pathlib import Path
from xml.etree import ElementTree as ET
import re
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data_audit/outputs/figures_phase3_tidyplots'
OUT=SRC/'Figure4_meta_tidyplots_composite.svg'
W,H,G=183.0,72.0,5.0

def panel(path, y, label):
    txt=path.read_text(encoding='utf-8')
    txt=re.sub(r'<\?xml[^>]*\?>','',txt)
    r=ET.fromstring(txt)
    vb=r.attrib.get('viewBox','0 0 518.74 204.09')
    content=''.join(ET.tostring(c,encoding='unicode') for c in list(r))
    return f'<svg x="0" y="{y}mm" width="{W}mm" height="{H}mm" viewBox="{vb}" preserveAspectRatio="none" aria-label="{label}">{content}</svg>'
items=[('Figure4_meta_tidyplots_panel_a.svg','Panel a: contrast-level meta-analysis'),('Figure4_meta_tidyplots_panel_b.svg','Panel b: dataset-level sensitivity'),('Figure4_meta_tidyplots_panel_c.svg','Panel c: leave-one-dataset-out robustness')]
body='\n'.join(panel(SRC/n,i*(H+G),label) for i,(n,label) in enumerate(items))
total=H*3+G*2
OUT.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{total}mm" viewBox="0 0 {W} {total}" role="img" aria-labelledby="title desc"><title id="title">Figure 4. Cross-dataset validation of the NAMPT axis</title><desc id="desc">Contrast-level meta-analysis, dataset-level sensitivity, and leave-one-dataset-out robustness.</desc><rect width="100%" height="100%" fill="white"/>{body}</svg>''',encoding='utf-8')
print('wrote',OUT,OUT.stat().st_size)
