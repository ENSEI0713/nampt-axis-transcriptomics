#!/usr/bin/env python3
"""Build an editable, text-preserving SVG concept figure for Figure 1."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data_audit/outputs/figures_phase3_tidyplots/Figure1_NAMPT_axis_editable.svg'
W,H=297,210

def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def text(x,y,s,size=4,weight='400',fill='#263238',anchor='start'):
 return f'<text x="{x}" y="{y}" font-family="Arial,Helvetica,sans-serif" font-size="{size}px" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{esc(s)}</text>'

def rect(x,y,w,h,fill='#F4F7F8',stroke='#CBD5D8',rx=2):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="0.5"/>'

def arrow(x1,y1,x2,y2,color='#718096',dash=''):
 return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="0.8" marker-end="url(#arrow)" stroke-dasharray="{dash}"/>'

parts=[f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">Figure 1. State-dependent NAMPT-axis transcriptional model</title>
<desc id="desc">Editable six-panel conceptual framework separating biological context, transcriptomic programs and state-dependent interpretation.</desc>
<defs><marker id="arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="#718096"/></marker></defs>
<rect width="100%" height="100%" fill="white"/>
{text(12,10,'State-dependent NAMPT-axis transcriptional programs',7,'700')}
{text(12,16,'Conceptual model: NAMPT upregulation requires tissue, time and metabolic context for interpretation.',3.5,'400','#52636A')}
''']
# panels a-f
panels=[(12,24,86,50,'a','Biological context'),(105,24,86,50,'b','State-dependent axis'),(198,24,87,50,'c','Evidence architecture'),(12,82,86,50,'d','Repair-like program'),(105,82,86,50,'e','Inflammation-like program'),(198,82,87,50,'f','Transcriptomic balance')]
for x,y,w,h,label,title in panels:
 parts += [rect(x,y,w,h), text(x+5,y+8,label,5,'700','#197C83'), text(x+14,y+8,title,4.2,'700')]
# a
parts += [rect(18,38,35,24,'#EAF6F4','#4D9A91'),text(21,45,'Intracellular NAMPT',3.5,'700','#197C83'),text(21,51,'NAD salvage',3.2),text(21,56,'Sirtuin / mitochondria',3.2),text(21,61,'DNA repair',3.2),rect(57,38,35,24,'#FFF1EE','#C9685A'),text(60,45,'Extracellular NAMPT',3.5,'700','#8E4B50'),text(60,51,'NF-kB / cytokines',3.2),text(60,56,'Monocyte / macrophage',3.2),text(60,61,'Inflammatory context',3.2),arrow(53,50,57,50,'#718096','2 1'),text(55,67,'mRNA ≠ protein',2.8,'400','#718096','middle')]
# b
parts += [rect(111,37,34,25,'#EAF6F4','#4D9A91'),text(128,45,'Repair-like',4,'700','#197C83','middle'),text(128,52,'NAD salvage · repair',3,'400','#52636A','middle'),rect(151,37,34,25,'#FFF1EE','#C9685A'),text(168,45,'Inflammation-like',4,'700','#8E4B50','middle'),text(168,52,'NF-kB · immune load',3,'400','#52636A','middle'),arrow(145,50,151,50,'#718096','3 2'),text(148,68,'same NAMPT upregulation, different context',2.8,'400','#52636A','middle')]
# c
for i,(lab,sub) in enumerate([('GEO','8 accessions'),('9 units','337 formal samples'),('Scores','4 transcriptomic metrics'),('Evo2','432 candidates')]):
 xx=204+(i%2)*39; yy=36+(i//2)*18; parts += [rect(xx,yy,34,13,'#F4F7F8','#AAB8BC'),text(xx+17,yy+5,lab,3.5,'700','#263238','middle'),text(xx+17,yy+10,sub,2.7,'400','#52636A','middle')]
# d/e
for x,color,title,items in [(18,'#197C83','Observed repair-like modules',['NAD salvage','Sirtuin / mitochondrial','DNA repair','Autophagy']), (111,'#B45150','Observed inflammatory-like modules',['NF-kB / cytokines','Innate immune','Monocyte burden','Metabolic stress'])]:
 for j,it in enumerate(items): parts += [rect(x,95+j*8,70,6,'#F8FBFB' if color=='#197C83' else '#FFF8F6',color),text(x+3,99+j*8,it,3.1,'400',color)]
 parts += [text(x+35,127,title,3.4,'700',color,'middle')]
# f
parts += [rect(204,94,75,30,'#F8FBFB','#AAB8BC'),text(241.5,101,'Transcriptomic balance descriptor',3.5,'700','#263238','middle'),text(241.5,108,'repair-like − inflammation-like',3.4,'400','#197C83','middle'),text(241.5,116,'descriptive, not causal',3,'400','#718096','middle')]
# state endpoint
parts += [rect(12,140,273,35,'#F4F7F8','#CBD5D8'),text(18,149,'State-dependent interpretation',4.6,'700'),rect(18,154,76,14,'#EAF6F4','#4D9A91'),text(56,160,'Acute exercise: NAMPT up, repair gain not reproducible',2.8,'400','#197C83','middle'),rect(108,154,76,14,'#F4F7F8','#718096'),text(146,160,'24 h recovery: stress signal relaxes',2.8,'400','#52636A','middle'),rect(198,154,76,14,'#FFF1EE','#C9685A'),text(236,160,'Metabolic stress: stronger inflammatory coupling',2.8,'400','#8E4B50','middle'),arrow(128,74,56,154,'#718096','2 1'),arrow(168,74,146,154,'#718096','2 1'),arrow(241,124,236,154,'#718096','2 1')]
parts += [text(12,188,'Evidence boundary: transcriptomic evidence only · eNAMPT protein and NAD metabolites were not measured · no causal or clinical-risk inference',3.1,'400','#52636A')]
parts += ['</svg>']
OUT.write_text(''.join(parts),encoding='utf-8')
print('wrote',OUT,OUT.stat().st_size)
