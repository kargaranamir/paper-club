"""Build the one-slide MCML Flash Talk PDF from slide.template.html.

Reuses the poster's fonts, Excalidraw SVG figures and slogan cloud. Usage:
  python3 build.py && RENDER_DEPS=<dir with playwright-core> CHROMIUM_PATH=<chrome> node print.mjs
"""
from pathlib import Path
import base64, re
from reportlab.graphics.barcode.qr import QrCodeWidget

HERE = Path(__file__).resolve().parent
POSTER = HERE.parent / 'poster'
src = (HERE / 'slide.template.html').read_text()
css = []
for stem, fam, wt in [('bricolage-grotesque-400', 'Bricolage Grotesque', 400), ('bricolage-grotesque-700', 'Bricolage Grotesque', 700),
                      ('bricolage-grotesque-800', 'Bricolage Grotesque', 800), ('space-mono-400', 'Space Mono', 400),
                      ('space-mono-700', 'Space Mono', 700)]:
    data = base64.b64encode((POSTER / 'fonts' / (stem + '.woff2')).read_bytes()).decode()
    css.append(f"@font-face{{font-family:'{fam}';font-weight:{wt};font-style:normal;font-display:block;"
               f"src:url(data:font/woff2;base64,{data}) format('woff2')}}")
src = src.replace('__FONT_CSS__', '\n'.join(css))
for name in ['mechanism', 'baseline']:
    src = src.replace('__SVG_' + name.upper() + '__', (POSTER / 'figures/svg' / (name + '.svg')).read_text())
tpl = (POSTER / 'poster.betterposter.template.html').read_text()
i = tpl.index('<svg class="slogan-cloud"')
cloud = tpl[i:tpl.index('</svg>', i) + 6].replace('class="cloud-shadow"', 'fill="var(--ink)" stroke="var(--ink)"')
src = src.replace('__CLOUD__', cloud)


def qr(url):
    q = QrCodeWidget(url); q.qr.make(); m = q.qr.modules; n = len(m)
    p = ''.join(f'M{c + 4} {r + 4}h1v1h-1z' for r, row in enumerate(m) for c, on in enumerate(row) if on)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n + 8} {n + 8}" role="img" aria-label="QR code">'
            f'<rect width="100%" height="100%" fill="#fffaf0"/><path fill="#16130f" d="{p}"/></svg>')


src = src.replace('__QR_PAPER__', qr('https://arxiv.org/abs/2606.16011v2'))
assert not re.search(r'__(SVG|QR|FONT|CLOUD)', src)
(HERE / 'slide.html').write_text(src)
print('built slide.html', len(src.encode()), 'bytes')
