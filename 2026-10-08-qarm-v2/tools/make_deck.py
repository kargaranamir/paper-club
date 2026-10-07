"""Assemble slides/index.html (self-contained deck) and slides/speaker-notes.md from slides/svg/*.svg."""
import base64
import glob
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from notes import NOTES, STORY  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TITLE = "QARM V2: Quantitative Alignment Multi-Modal Recommendation for Reasoning User Sequence Modeling"

svgs = sorted(glob.glob(os.path.join(ROOT, "slides/svg/*.svg")))
slides = []
for f in svgs:
    name = os.path.basename(f)[:-4]
    data = base64.b64encode(open(f, "rb").read()).decode()
    slides.append({"name": name, "src": "data:image/svg+xml;base64," + data, "note": NOTES.get(name[3:], "")})

# ---------------------------------------------------------------- speaker notes
with open(os.path.join(ROOT, "slides/speaker-notes.md"), "w") as f:
    f.write(f"# Speaker notes — {TITLE}\n\nPaper club · 8 October 2026 · arXiv:2602.08559 (predecessor: arXiv:2411.11739)\n\n")
    f.write(STORY + "\n\n---\n\n")
    for i, s in enumerate(slides, 1):
        f.write(f"## {i}. {s['name'][3:].replace('-', ' ')}\n\n![slide {i}](svg/{s['name']}.svg)\n\n{s['note']}\n\n")

# ---------------------------------------------------------------- deck
page = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>QARM V2 paper club</title>
<style>
:root{--bg:#f1f3f5;--ink:#1e1e1e;--muted:#6b6f76;--accent:#e8a33d;--card:#ffffff}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#1b1c1e;--ink:#e9ecef;--muted:#a0a4ab;--card:#26282b}}
:root[data-theme="dark"]{--bg:#1b1c1e;--ink:#e9ecef;--muted:#a0a4ab;--card:#26282b}
*{box-sizing:border-box}
html,body{margin:0;height:100%;background:var(--bg);color:var(--ink);font:15px/1.45 system-ui,-apple-system,Segoe UI,sans-serif}
#stage{position:fixed;inset:0 0 56px 0;display:flex;align-items:center;justify-content:center;padding:16px}
#stage img{max-width:100%;max-height:100%;aspect-ratio:16/9;background:#fff;border-radius:10px;box-shadow:0 6px 30px rgba(0,0,0,.12)}
#bar{position:fixed;left:0;right:0;bottom:0;min-height:56px;padding-bottom:env(safe-area-inset-bottom,0px)!important;display:flex;align-items:center;gap:10px;padding:0 16px}
#bar button{border:1px solid rgba(128,128,128,.35);background:var(--card);color:var(--ink);border-radius:8px;padding:6px 12px;font:inherit;cursor:pointer}
#count{color:var(--muted);min-width:64px;text-align:center}
#prog{flex:1;height:4px;background:rgba(128,128,128,.25);border-radius:2px;overflow:hidden}
#prog i{display:block;height:100%;background:var(--accent);width:0}
#notes{position:fixed;left:16px;right:16px;bottom:64px;max-height:42vh;white-space:pre-wrap;overflow:auto;background:var(--card);border-radius:10px;padding:12px 16px;box-shadow:0 4px 20px rgba(0,0,0,.15);display:none}
body.shownotes #notes{display:block}
#grid{position:fixed;inset:0;overflow:auto;background:var(--bg);padding:16px;display:none;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
body.overview #grid{display:grid}
#grid figure{margin:0;cursor:pointer}
#grid img{width:100%;background:#fff;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,.1)}
#grid figcaption{color:var(--muted);font-size:13px}
body:fullscreen #bar,body:fullscreen #notes{display:none}
body:fullscreen #stage{inset:0;padding:0;background:#fff}
body:fullscreen #stage img{border-radius:0;box-shadow:none}
@media (max-width:600px){#bar .opt{display:none}}
</style></head><body>
<div id="stage"><img id="slide" alt=""></div>
<div id="notes"></div>
<div id="grid"></div>
<div id="bar">
 <button id="prev" aria-label="Previous slide">&#8592;</button><span id="count"></span><button id="next" aria-label="Next slide">&#8594;</button>
 <div id="prog"><i></i></div>
 <button id="nb" class="opt">Notes (N)</button><button id="ob" class="opt">Overview (O)</button><button id="fb" class="opt">Full screen (F)</button>
</div>
<script>
const S = __SLIDES__;
let i = 0;
try { const h = parseInt(location.hash.slice(1)); if (h >= 1 && h <= S.length) i = h - 1; } catch (e) {}
const img = document.getElementById('slide'), cnt = document.getElementById('count'), notes = document.getElementById('notes'), prog = document.querySelector('#prog i');
function show(k){ i = Math.max(0, Math.min(S.length - 1, k)); img.src = S[i].src; img.alt = 'Slide ' + (i + 1);
  cnt.textContent = (i + 1) + ' / ' + S.length; notes.textContent = S[i].note; prog.style.width = ((i + 1) / S.length * 100) + '%';
  try { history.replaceState(null, '', '#' + (i + 1)); } catch (e) {} }
const grid = document.getElementById('grid');
S.forEach((s, k) => { const f = document.createElement('figure'); f.innerHTML = '<img loading="lazy" alt="">' + '<figcaption>' + (k + 1) + ' · ' + s.name.slice(3).replace(/-/g, ' ') + '</figcaption>';
  f.querySelector('img').src = s.src; f.onclick = () => { document.body.classList.remove('overview'); show(k); }; grid.appendChild(f); });
document.getElementById('prev').onclick = () => show(i - 1);
document.getElementById('next').onclick = () => show(i + 1);
document.getElementById('nb').onclick = () => document.body.classList.toggle('shownotes');
document.getElementById('ob').onclick = () => document.body.classList.toggle('overview');
document.getElementById('fb').onclick = () => document.fullscreenElement ? document.exitFullscreen() : document.body.requestFullscreen();
document.getElementById('stage').onclick = e => show(e.clientX > innerWidth / 3 ? i + 1 : i - 1);
addEventListener('keydown', e => { const k = e.key;
  if (['ArrowRight', 'PageDown', ' ', 'Enter'].includes(k)) { e.preventDefault(); show(i + 1); }
  else if (['ArrowLeft', 'PageUp', 'Backspace'].includes(k)) { e.preventDefault(); show(i - 1); }
  else if (k === 'Home') show(0); else if (k === 'End') show(S.length - 1);
  else if (k === 'n' || k === 'N') document.body.classList.toggle('shownotes');
  else if (k === 'o' || k === 'O' || k === 'Escape') document.body.classList.toggle('overview', k !== 'Escape' ? undefined : false);
  else if (k === 'f' || k === 'F') document.getElementById('fb').click(); });
let tx = null; addEventListener('touchstart', e => tx = e.touches[0].clientX, {passive: true});
addEventListener('touchend', e => { if (tx === null) return; const d = e.changedTouches[0].clientX - tx; if (Math.abs(d) > 40) show(d < 0 ? i + 1 : i - 1); tx = null; });
show(i);
</script></body></html>
"""
page = page.replace("__SLIDES__", json.dumps(slides))
with open(os.path.join(ROOT, "slides/index.html"), "w") as f:
    f.write(page)
print("deck:", len(slides), "slides,", round(len(page) / 1e6, 2), "MB")

# ---------------------------------------------------------------- artifact variant (no doctype/html/head/body)
import re  # noqa: E402
frag = re.sub(r'<!doctype html>\s*<html lang="en"><head><meta charset="utf-8">\s*<meta name="viewport"[^>]*>\s*', "", page)
frag = frag.replace("</style></head><body>", "</style>").replace("</script></body></html>", "</script>")
os.makedirs(os.path.join(ROOT, "tools/render/dist"), exist_ok=True)
with open(os.path.join(ROOT, "tools/render/dist/deck-artifact.html"), "w") as f:
    f.write(frag)
print("artifact page: tools/render/dist/deck-artifact.html")
