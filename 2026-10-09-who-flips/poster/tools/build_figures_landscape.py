"""Extra figure for the landscape #betterposter: the subject-domain chart with its two halves stacked.

Reuses the Fig class and data from build_figures.py without re-running the other figures.
Usage: FIGURE_FONT=/path/Arial-or-LiberationSans.ttf OUT_ROOT=<dir> python3 build_figures_landscape.py
(writes <OUT_ROOT>/figures/src/domains-stacked.json; render it with render_figures.mjs).
"""
import os
from pathlib import Path
src = (Path(__file__).parent / 'build_figures.py').read_text()
exec(src[:src.index('# Flow diagram')], globals())
ROOT = Path(os.environ.get('OUT_ROOT', ROOT))
(ROOT / 'figures/src').mkdir(parents=True, exist_ok=True)

s = Fig('domains-stacked', 880, 440)
for top, title, rows, col in [
        (0, 'THREE LOWEST · STEM', [SUBJECTS[5], SUBJECTS[4], SUBJECTS[3]], '#0B765A'),
        (222, 'THREE HIGHEST · HUMANITIES / SOCIAL SCI.', SUBJECTS[:3], AMBER)]:
    s.text(12, top, title, 25, col)
    xx, ww = 355, 345
    for v in [0, 50, 100]:
        a = xx + ww * v / 100; s.line([(a, top + 43), (a, top + 172)], GRID, 1)
        s.text(a, top + 184, str(v), 26, MUTED, 'c')
    for i, (label, afr, ci) in enumerate(rows):
        label = {'Elementary mathematics': 'Elementary math.', 'College mathematics': 'College math.'}.get(label, label)
        yy = top + 60 + i * 47
        s.text(328, yy - 16, label, 30, INK, 'r')
        a, b = xx + ww * (afr - ci) / 100, xx + ww * (afr + ci) / 100
        s.line([(a, yy), (b, yy)], col, 2)
        for edge in [a, b]: s.line([(edge, yy - 7), (edge, yy + 7)], col, 2)
        s.dot(xx + ww * afr / 100, yy, col, 6)
        s.text(860, yy - 16, f'{afr:.1f}%', 30, col, 'r')
s.write()
print('wrote', ROOT / 'figures/src/domains-stacked.json')
