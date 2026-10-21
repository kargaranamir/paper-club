"""Native Excalidraw figures for the Iranic NLP poster. All values are copied from the paper's tables, text and
figure labels (see ../SOURCES.txt)."""
from pathlib import Path
import json, math, os
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
INK = '#1B1712'; MUTED = '#5E564B'; GRID = '#E2D7C4'; WHITE = '#FFFBF3'
SW = '#C4502B'; NW = '#24386B'; EA = '#2E7A57'; OS = '#7B4FA6'
LAPIS = '#1F5AA6'; TURQ = '#138C8C'; SAFFRON = '#F2B233'; POM = '#B8323E'; PALE = '#E6F1EE'
LEVEL = {'H': ('#2E7A57', 'HIGH'), 'M': ('#7FA35A', 'MED'), 'L': ('#E3A23A', 'LOW'), 'VL': ('#B8323E', 'VERY LOW')}

f = TTFont(os.environ.get('FIGURE_FONT', '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'))
cm = f.getBestCmap(); hm = f['hmtx']; up = f['head'].unitsPerEm


def tw(t, sz):
    return max(sum(hm[cm.get(ord(c), cm[32])][0] for c in l) / up * sz for l in t.split('\n'))


class Fig:
    def __init__(self, name, w, h, bg=WHITE):
        self.name = name; self.w = w; self.h = h; self.k = 0
        self.e = [dict(type='cameraUpdate', x=0, y=0, width=1200, height=900)]
        self.rect(0, 0, w, h, bg, 'transparent', 0)

    def add(self, **el):
        self.k += 1; el['id'] = f'{self.name}-{self.k}'; self.e.append(el)

    def rect(self, x, y, w, h, fill, stroke=GRID, sw=1, rough=0, round_=False, dashed=False):
        el = dict(type='rectangle', x=x, y=y, width=w, height=h, backgroundColor=fill, strokeColor=stroke,
                  fillStyle='solid', strokeWidth=sw, roughness=rough)
        if round_:
            el['roundness'] = {'type': 3}
        if dashed:
            el['strokeStyle'] = 'dashed'
        self.add(**el)

    def text(self, x, y, t, sz=26, col=INK, anchor='l', bold=False):
        x -= tw(t, sz) * (0.5 if anchor == 'c' else 1 if anchor == 'r' else 0)
        self.add(type='text', x=x, y=y, text=t, fontSize=sz, fontFamily=2, strokeColor=col)

    def line(self, pts, col=GRID, sw=1, dashed=False, head=None, rough=0):
        x, y = pts[0]
        self.add(type='arrow' if head else 'line', x=x, y=y,
                 width=max(a for a, b in pts) - min(a for a, b in pts),
                 height=max(b for a, b in pts) - min(b for a, b in pts),
                 points=[[a - x, b - y] for a, b in pts], strokeColor=col, strokeWidth=sw,
                 strokeStyle='dashed' if dashed else 'solid', roughness=rough, endArrowhead=head, startArrowhead=None)

    def dot(self, x, y, col, r=7):
        self.add(type='ellipse', x=x - r, y=y - r, width=2 * r, height=2 * r, strokeColor=INK, backgroundColor=col,
                 strokeWidth=1.5, fillStyle='solid', roughness=0)

    def node(self, x, y, w, h, t, fill=PALE, col=INK, sz=26, sw=2):
        self.rect(x, y, w, h, fill, col, sw, 0, True)
        lines = t.split('\n')
        for i, l in enumerate(lines):
            self.text(x + w / 2, y + h / 2 - sz * 0.62 * len(lines) + i * sz * 1.25, l, sz, col, 'c')

    def write(self):
        (ROOT / 'figures/src' / f'{self.name}.json').write_text(json.dumps(dict(width=self.w, height=self.h, elements=self.e)))


# ------------------------------------------------------------------ 1. family tree (Table 1)
BRANCHES = [
    ('SOUTHWESTERN', SW, [('Persian', '91M', 'H'), ('Dari', '15M', 'M'), ('Tajik', '8M', 'L'),
                          ('Luri / Bakhtiari', '5M', 'VL'), ('Hazaragi', '3M', 'VL'), ('Laki', '0.7M', 'VL')]),
    ('NORTHWESTERN', NW, [('Kurdish', '26M', 'L'), ('Balochi', '9M', 'VL'), ('Gilaki', '3M', 'VL'),
                          ('S. Kurdish', '3M', 'VL'), ('Zazaki', '2–4M', 'VL'), ('Mazanderani', '1.4M', 'VL'),
                          ('Talysh', '0.8M', 'VL'), ('Gorani', '0.4M', 'VL')]),
    ('EASTERN', EA, [('Pashto', '51M', 'L'), ('Shughni', '0.1M', 'VL'), ('Wakhi', '0.06M', 'VL'),
                     ('Yaghnobi', '0.01M', 'VL')]),
    ('OSSETIC', OS, [('Ossetic', '0.6M', 'VL')]),
]
s = Fig('family', 1880, 560, '#FFFFFF')
s.node(690, 10, 500, 78, 'Iranic · 101 ISO 639-3 codes', '#FFF1C9', INK, 30, 2.5)
cw, gx = 440, 26
xs = [20 + i * (cw + gx) for i in range(4)]
for (name, col, langs), x in zip(BRANCHES, xs):
    s.line([(940, 92), (940, 112), (x + cw / 2, 112), (x + cw / 2, 140)], INK, 2, head='arrow')
    s.rect(x, 146, cw, 48, col, INK, 2, 0, True)
    s.text(x + cw / 2, 156, name, 24, '#FFFFFF', 'c')
    for i, (lang, spk, lvl) in enumerate(langs):
        y = 206 + i * 43
        s.rect(x, y, cw, 38, WHITE if i % 2 == 0 else '#F6EFE2', 'transparent', 0)
        s.text(x + 12, y + 7, lang, 22, INK)
        s.text(x + 250, y + 7, spk, 22, MUTED, 'r')
        c, lab = LEVEL[lvl]
        s.rect(x + 270, y + 6, 156, 26, c, INK, 1, 0, True)
        s.text(x + 348, y + 9, lab, 16, '#FFFFFF' if lvl in ('H', 'VL') else INK, 'c')
s.write()

# ------------------------------------------------------------------ 2. papers vs speakers (Figure 2 labels)
ROWS = [('Persian', 394, 91), ('Kurdish', 93, 26), ('Pashto', 29, 51), ('Luri / Laki', 5, 5), ('Balochi', 4, 8),
        ('Mazanderani / Gilaki', 4, 5)]
s = Fig('papers-speakers', 1100, 560, '#FFFFFF')
s.text(250, 0, 'PAPERS (2020–2026)', 22, LAPIS)
s.text(650, 0, 'SPEAKERS (M)', 22, SW)
s.text(1090, 0, 'PAPERS / M', 22, INK, 'r')
for i, (lang, p, sp) in enumerate(ROWS):
    y = 50 + i * 82
    s.text(232, y + 14, lang, 24, INK, 'r')
    s.rect(250, y, max(4, p / 394 * 320), 50, LAPIS, INK, 1.5)
    s.text(250 + max(4, p / 394 * 320) + 10, y + 12, str(p), 24, INK)
    s.rect(650, y, max(4, sp / 91 * 300), 50, SW, INK, 1.5)
    s.text(650 + max(4, sp / 91 * 300) + 10, y + 12, f'{sp}M', 24, INK)
    ratio = p / sp
    s.text(1090, y + 12, f'{ratio:.1f}', 26, POM if ratio < 1 else INK, 'r')
s.line([(240, 40), (240, 545)], INK, 2)
s.line([(640, 40), (640, 545)], GRID, 1, dashed=True)
s.write()

# ------------------------------------------------------------------ 3. timeline (Figure 3 totals)
YEARS = [(2020, 54), (2021, 43), (2022, 64), (2023, 85), (2024, 87), (2025, 131), (2026, 65)]
s = Fig('timeline', 1100, 600, '#FFFFFF')
X0, Y0, H = 80, 500, 420
for v in (0, 50, 100, 150):
    y = Y0 - v / 150 * H
    s.line([(X0, y), (1090, y)], GRID, 1.5)
    s.text(X0 - 14, y - 17, str(v), 28, MUTED, 'r')
bw = 118
for i, (yr, v) in enumerate(YEARS):
    x = X0 + 22 + i * 143
    h = v / 150 * H
    partial = yr == 2026
    s.rect(x, Y0 - h, bw, h, '#F3EEE4' if partial else TURQ, INK, 2, 0, False, dashed=partial)
    s.text(x + bw / 2, Y0 - h - 42, str(v), 34, INK, 'c')
    s.text(x + bw / 2, Y0 + 14, str(yr), 28, INK, 'c')
s.text(X0 + 22 + 6 * 143 + bw / 2, Y0 + 52, 'to May', 24, MUTED, 'c')
s.line([(X0, Y0), (1090, Y0)], INK, 2.5)
s.write()

# ------------------------------------------------------------------ 4. tasks (Figure 4 labels)
TASKS = [('Sentiment analysis', 116), ('Text classification', 70), ('Language modeling', 59),
         ('Question answering', 59), ('Machine translation', 41), ('Named entities', 38),
         ('Information extraction', 36), ('Morphology & syntax', 32), ('Information retrieval', 25),
         ('Lexical semantics', 24), ('Summarization', 10), ('Dialogue', 10), ('Text generation', 9)]
s = Fig('tasks', 1100, 13 * 54, '#FFFFFF')
for i, (tk, v) in enumerate(TASKS):
    y = 6 + i * 54
    s.text(425, y + 5, tk, 29, INK, 'r')
    w = v / 116 * 560
    s.rect(442, y, w, 42, SAFFRON if i == 0 else '#F7D78C', INK, 1.5)
    s.text(442 + w + 12, y + 5, str(v), 29, INK)
s.write()

# ------------------------------------------------------------------ 5. wikimedia footprint (resources table)
WIKI = [('Persian', 1075000, 19248), ('Tajik', 118000, 430), ('N. Kurdish', 92000, 8254), ('Mazanderani', 65000, 337),
        ('Gilaki', 48000, 34), ('Zazaki', 43000, 1083), ('Pashto', 21000, 1100), ('Talysh', 10000, 302)]
s = Fig('wiki', 1100, 600)
X0, X1 = 230, 1060
def lx(v):
    return X0 + (math.log10(v) - 1) / (math.log10(2e6) - 1) * (X1 - X0)
for v, lab in [(10, '10'), (100, '100'), (1000, '1K'), (10000, '10K'), (100000, '100K'), (1000000, '1M')]:
    s.line([(lx(v), 20), (lx(v), 500)], GRID, 1)
    s.text(lx(v), 508, lab, 20, MUTED, 'c')
for i, (lang, wp, wt) in enumerate(WIKI):
    y = 30 + i * 58
    hollow = lang in ('Gilaki', 'Mazanderani')
    s.text(X0 - 14, y + 4, lang, 23, POM if hollow else INK, 'r')
    s.rect(X0, y, lx(wp) - X0, 30, LAPIS, INK, 1.5)
    s.line([(lx(wt), y + 15), (lx(wp), y + 15)], INK, 1, dashed=True)
    s.dot(lx(wt), y + 15, SAFFRON, 10)
s.rect(X0, 548, 30, 22, LAPIS, INK, 1.5); s.text(X0 + 40, 546, 'Wikipedia articles', 21, INK)
s.dot(X0 + 330, 559, SAFFRON, 10); s.text(X0 + 350, 546, 'Wiktionary entries (log scale)', 21, INK)
s.write()

# ------------------------------------------------------------------ 6. parallel data with English (Table 3)
PAR = [('Persian', 612200000, '612M'), ('Kurdish', 510633, '511K'), ('Gorani', 22497, '22K'), ('Gilaki', 9030, '9K'),
       ('Laki', 4633, '4.6K'), ('Mazanderani', 4483, '4.5K'), ('Zazaki', 4401, '4.4K'), ('Talysh', 2106, '2.1K'),
       ('S. Luri', 1997, '2K'), ('Balochi', 110, '110')]
s = Fig('parallel', 1100, 720, '#FFFFFF')
X0, X1 = 230, 950
def px(v):
    return X0 + (math.log10(v) - 1) / (math.log10(1e9) - 1) * (X1 - X0)
for v, lab in [(10, '10'), (1e3, '1K'), (1e5, '100K'), (1e7, '10M'), (1e9, '1B')]:
    s.line([(px(v), 0), (px(v), 620)], GRID, 1.5)
    s.text(px(v), 628, lab, 27, MUTED, 'c')
for i, (lang, v, lab) in enumerate(PAR):
    y = 6 + i * 61
    col = TURQ if i == 0 else LAPIS if i == 1 else POM if lang == 'Balochi' else '#8FB6D9'
    s.text(X0 - 14, y + 6, lang, 29, INK, 'r')
    s.rect(X0, y, px(v) - X0, 44, col, INK, 1.5)
    s.text(px(v) + 10, y + 6, lab, 29, INK)
s.text(X0, 672, 'sentence pairs with English (log scale)', 27, MUTED)
s.write()

# ------------------------------------------------------------------ 7. survey pipeline (§3)
s = Fig('pipeline', 1100, 560)
steps = [('5,878', 'candidate papers\n2020 – May 2026', '#FFF1C9'),
         ('Qwen3.5-9B', '1: relevance filter · 2: annotate language,\ntask, resource type, availability, year, venue', PALE),
         ('2 authors', 'verify every annotation;\na third arbitrates', PALE),
         ('495', 'papers in the survey', '#FFD9C9')]
for i, (big, small, fill) in enumerate(steps):
    y = 10 + i * 140
    s.rect(30, y, 1040, 110, fill, INK, 2, 0, True)
    s.text(60, y + 28, big, 44, INK)
    s.text(400, y + 24, small, 24, INK)
    if i < 3:
        s.line([(550, y + 112), (550, y + 138)], INK, 2.5, head='arrow')
s.write()
print('figures written')
