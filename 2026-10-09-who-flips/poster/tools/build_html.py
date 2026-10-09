"""Embed vector graphics, fonts and vector QR codes into one offline HTML file."""
from pathlib import Path
import base64,re,os,json
from reportlab.graphics.barcode.qr import QrCodeWidget
ROOT=Path(__file__).resolve().parents[1]
FONT_DIR=Path(os.environ.get('POSTER_FONT_DIR',ROOT/'fonts'))
source=(ROOT/'poster.template.html').read_text()
css=[]
for stem,family,weight in [('bricolage-grotesque-400','Bricolage Grotesque',400),('bricolage-grotesque-700','Bricolage Grotesque',700),('bricolage-grotesque-800','Bricolage Grotesque',800),('space-mono-400','Space Mono',400),('space-mono-700','Space Mono',700)]:
 data=base64.b64encode((FONT_DIR/(stem+'.woff2')).read_bytes()).decode()
 css.append(f"@font-face{{font-family:'{family}';font-weight:{weight};font-style:normal;font-display:block;src:url(data:font/woff2;base64,{data}) format('woff2')}}")
source=source.replace('__FONT_CSS__','\n'.join(css))
licenses={f.name:f.read_text() for f in (ROOT/'licenses').glob('*.txt')}
source=source.replace('</head>','<script type="application/json" id="font-license-notices">'+json.dumps(licenses).replace('</','<\\/')+'</script>\n</head>')
for name in ['mechanism','baseline','length','domains','maxflip','cross-matrix','ea-ep','pooling']:
 svg=(ROOT/'figures/svg'/(name+'.svg')).read_text()
 svg=re.sub(r'<svg ',f'<svg role="img" aria-label="{name.replace("-"," ")} figure" ',svg,count=1)
 source=source.replace('__SVG_'+name.upper().replace('-','_')+'__',svg)
def qr(url):
 q=QrCodeWidget(url);q.qr.make();m=q.qr.modules;n=len(m);paths=[]
 for row,vals in enumerate(m):
  for col,on in enumerate(vals):
   if on:paths.append(f'M{col+4} {row+4}h1v1h-1z')
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n+8} {n+8}" role="img" aria-label="QR code"><rect width="100%" height="100%" fill="#fffaf0"/><path fill="#16130f" d="{"".join(paths)}"/></svg>'
for name,url in [('PAPER','https://arxiv.org/abs/2606.16011v2'),('CODE','https://github.com/nafisenik/WhoFlips'),('DATA','https://huggingface.co/datasets/nafisehNik/WhoFlips')]:source=source.replace('__QR_'+name+'__',qr(url))
assert not re.search(r'__(SVG|QR|FONT)_',source)
(ROOT/'who-flips-a0.html').write_text(source)
print('Built offline HTML:',len(source.encode()),'bytes')
