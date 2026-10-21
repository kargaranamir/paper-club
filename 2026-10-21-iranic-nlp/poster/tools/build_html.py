"""Embed fonts, Excalidraw SVG figures and vector QR codes into one offline HTML file."""
from pathlib import Path
import base64, re, json
from reportlab.graphics.barcode.qr import QrCodeWidget

ROOT = Path(__file__).resolve().parents[1]
src = (ROOT / 'poster.template.html').read_text()
css = []
for stem, fam, wt in [('bricolage-grotesque-400', 'Bricolage Grotesque', 400), ('bricolage-grotesque-700', 'Bricolage Grotesque', 700),
                      ('bricolage-grotesque-800', 'Bricolage Grotesque', 800), ('space-mono-400', 'Space Mono', 400),
                      ('space-mono-700', 'Space Mono', 700)]:
    data = base64.b64encode((ROOT / 'fonts' / (stem + '.woff2')).read_bytes()).decode()
    css.append(f"@font-face{{font-family:'{fam}';font-weight:{wt};font-style:normal;font-display:block;src:url(data:font/woff2;base64,{data}) format('woff2')}}")
src = src.replace('__FONT_CSS__', '\n'.join(css))
lic = {f.name: f.read_text() for f in (ROOT / 'licenses').glob('*.txt')}
src = src.replace('</head>', '<script type="application/json" id="font-license-notices">' + json.dumps(lic).replace('</', '<\\/') + '</script>\n</head>')
for name in ['family', 'papers-speakers', 'timeline', 'tasks', 'parallel']:
    svg = (ROOT / 'figures/svg' / (name + '.svg')).read_text()
    src = src.replace('__SVG_' + name.upper().replace('-', '_') + '__', svg)


def qr(url):
    q = QrCodeWidget(url); q.qr.make(); m = q.qr.modules; n = len(m)
    paths = [f'M{c + 4} {r + 4}h1v1h-1z' for r, row in enumerate(m) for c, on in enumerate(row) if on]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n + 8} {n + 8}" role="img" aria-label="QR code">'
            f'<rect width="100%" height="100%" fill="#fffbf3"/><path fill="#1b1712" d="{"".join(paths)}"/></svg>')


src = src.replace('__IMG_MAP__', 'data:image/png;base64,' + base64.b64encode((ROOT / 'figures/map-crop.png').read_bytes()).decode())
for name, url in [('SITE', 'https://sigiranic.github.io')]:
    src = src.replace('__QR_' + name + '__', qr(url))
assert not re.search(r'__(SVG|QR|FONT|IMG)_', src)
(ROOT / 'iranic-nlp-a0.html').write_text(src)
print('built', len(src.encode()), 'bytes')
