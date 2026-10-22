"""slidekit — tiny helper to author 1600x900 slides as Excalidraw element skeletons.

The output format is the one accepted by the Excalidraw MCP `create_view` tool
(and by Excalidraw's `convertToExcalidrawElements`): shapes may carry a `label`,
and a leading `cameraUpdate` frames the slide.  tools/render/render.mjs turns the
same JSON into .excalidraw + .svg files, so the MCP preview and the deck share one
source of truth.
"""
import glob
import json
import math
import os

from fontTools.ttLib import TTFont

W, H = 1600, 900

# ---------------------------------------------------------------- palette
# Taken from the reference figure (Excalidraw pastel blocks on white).
P = {
    "ink": "#1e1e1e",
    "muted": "#6b6f76",
    "faint": "#adb5bd",
    "grid": "#e9ecef",
    "paper": "#f1f3f5",
    "orange": {"stroke": "#e8a33d", "fill": "#f9d8aa", "text": "#b5690b", "soft": "#fdf0dc"},
    "blue": {"stroke": "#5b9be6", "fill": "#b8d6fb", "text": "#2c68c9", "soft": "#eaf2fd"},
    "green": {"stroke": "#5cbf6a", "fill": "#d9f5dc", "text": "#2f8a3d", "soft": "#effaf0"},
    "purple": {"stroke": "#8a63e8", "fill": "#e3dcfb", "text": "#6a45c9", "soft": "#f3effd"},
    "yellow": {"stroke": "#1e1e1e", "fill": "#fdf3c4", "text": "#1e1e1e", "soft": "#fffae3"},
    "gray": {"stroke": "#ced4da", "fill": "#f1f3f5", "text": "#495057", "soft": "#f8f9fa"},
    "red": {"stroke": "#e8590c", "fill": "#ffd8c2", "text": "#c2410c", "soft": "#fff1e8"},
}

# ---------------------------------------------------------------- text metrics
_FONTDIR = os.path.join(os.path.dirname(__file__), "render/node_modules/@excalidraw/excalidraw/dist/prod/fonts")
_ADV = {}


def _load(fam):
    if fam in _ADV:
        return _ADV[fam]
    adv = {}
    for f in glob.glob(os.path.join(_FONTDIR, fam, "*.woff2")):
        t = TTFont(f)
        hmtx = t["hmtx"]
        upm = t["head"].unitsPerEm
        for cp, g in t.getBestCmap().items():
            adv.setdefault(cp, hmtx[g][0] / upm)
    _ADV[fam] = adv
    return adv


def text_width(s, fs, mono=False):
    adv = _load("ComicShanns" if mono else "Excalifont")
    best = 0.0
    for line in s.split("\n"):
        w = 0.0
        for ch in line:
            cp = ord(ch)
            if cp in adv:
                w += adv[cp]
            elif 0x2E80 <= cp <= 0x9FFF or 0xAC00 <= cp <= 0xD7AF:
                w += 1.0
            else:
                w += 0.55
        best = max(best, w * fs)
    return best


LH = 1.25  # Excalidraw line height for Excalifont / Comic Shanns


def text_height(s, fs):
    return (s.count("\n") + 1) * fs * LH


# ---------------------------------------------------------------- slide
class Slide:
    def __init__(self, name, n=None, total=None):
        self.name = name
        self.n = n
        self.total = total
        self.els = [
            {"type": "cameraUpdate", "width": 1600, "height": 1200, "x": 0, "y": -150},
            {"type": "rectangle", "id": "slidebg", "x": 0, "y": 0, "width": W, "height": H,
             "strokeColor": "#dee2e6", "strokeWidth": 1, "roughness": 0,
             "backgroundColor": "#ffffff", "fillStyle": "solid"},
        ]
        self._k = 0
        self._fig = None
        self.figs = {}  # figure name -> element ids (standalone figures for the LaTeX deck)

    def fig(self, name):
        """Start recording elements for a standalone figure (latex/figures/<name>.pdf)."""
        self._fig = name
        self.figs.setdefault(name, [])

    def endfig(self):
        self._fig = None

    def _id(self, p="e"):
        self._k += 1
        return f"{p}{self._k}"

    def add(self, el):
        for k in ("x", "y", "width", "height"):
            if isinstance(el.get(k), float):
                el[k] = round(el[k], 1)
                if el[k] == int(el[k]):
                    el[k] = int(el[k])
        el.setdefault("id", self._id())
        self.els.append(el)
        if self._fig:
            self.figs[self._fig].append(el["id"])
        return el

    # -------------------------------------------------- primitives
    def text(self, x, y, s, fs=26, color=None, anchor="l", valign="t", mono=False, align=None, opacity=None):
        """Standalone text. anchor l/c/r is horizontal reference, valign t/m/b vertical."""
        h = text_height(s, fs)
        if valign == "m":
            y = y - h / 2
        elif valign == "b":
            y = y - h
        lines = s.split("\n")
        if anchor != "l" and len(lines) > 1:
            # one left-aligned element per line: renders identically everywhere
            el = None
            for i, ln in enumerate(lines):
                el = self.text(x, y + i * fs * LH, ln, fs, color, anchor, "t", mono, None, opacity)
            return el
        w = text_width(s, fs, mono)
        if anchor == "c":
            x = x - w / 2
        elif anchor == "r":
            x = x - w
        el = {"type": "text", "x": round(x, 1), "y": round(y, 1), "text": s, "fontSize": fs,
              "strokeColor": color or P["ink"]}
        if mono:
            el["fontFamily"] = 8
        if opacity:
            el["opacity"] = opacity
        return self.add(el)

    def box(self, x, y, w, h, label=None, c="gray", fs=24, fill=None, stroke=None, tcolor=None,
            round_=True, sw=2, style=None, dashed=False, mono=False, opacity=None, shape="rectangle", roughness=None):
        pal = P[c] if isinstance(c, str) and c in P else P["gray"]
        el = {"type": shape, "x": x, "y": y, "width": w, "height": h,
              "strokeColor": stroke or pal["stroke"], "backgroundColor": fill or pal["fill"],
              "fillStyle": style or "solid", "strokeWidth": sw}
        if round_ and shape == "rectangle":
            el["roundness"] = {"type": 3}
        if dashed:
            el["strokeStyle"] = "dashed"
        if opacity:
            el["opacity"] = opacity
        if roughness is not None:
            el["roughness"] = roughness
        el = self.add(el)
        if label is not None:
            # label as separate centred text (keeps full control of layout)
            self.text(x + w / 2, y + h / 2, label, fs, tcolor or pal["text"], anchor="c", valign="m", mono=mono)
        return el

    def arrow(self, pts, color=None, sw=2, dashed=False, head="arrow", start=None, roughness=None):
        x0, y0 = pts[0]
        rel = [[round(px - x0, 1), round(py - y0, 1)] for px, py in pts]
        xs = [p[0] for p in rel]
        ys = [p[1] for p in rel]
        el = {"type": "arrow", "x": x0, "y": y0, "width": max(xs) - min(xs), "height": max(ys) - min(ys),
              "points": rel, "strokeColor": color or P["ink"], "strokeWidth": sw,
              "endArrowhead": head, "startArrowhead": start}
        if dashed:
            el["strokeStyle"] = "dashed"
        if roughness is not None:
            el["roughness"] = roughness
        return self.add(el)

    def line(self, pts, color=None, sw=2, dashed=False, roughness=None):
        return self.arrow(pts, color, sw, dashed, head=None, roughness=roughness)

    # -------------------------------------------------- slide furniture
    def title(self, s, sub=None, part=None, pc="blue"):
        self.text(70, 42, s, 46)
        if sub:
            self.text(72, 108, sub, 26, P["muted"])
        if part:
            self.text(72, 14, part.upper(), 17, P[pc]["text"] if pc != "yellow" else P["muted"])

    def footer(self, src=None):
        if src:
            self.text(70, 868, src, 17, P["muted"], valign="m")
        if self.n:
            self.text(W - 60, 868, f"{self.n}", 18, P["faint"], anchor="r", valign="m")

    def takeaway(self, s, y=770, x=70, w=W - 140, h=64, fs=26):
        self.box(x, y, w, h, s, "yellow", fs, sw=2)

    def bullets(self, x, y, items, fs=26, color=None, gap=14, dot="•", dcolor=None, width=None):
        cy = y
        for it in items:
            sub = it.startswith("  ")
            s = it.strip()
            f = fs - 4 if sub else fs
            xx = x + (34 if sub else 0)
            self.text(xx, cy, "–" if sub else dot, f, dcolor or P["muted"])
            t = self.text(xx + 26, cy, s, f, color if not sub else P["muted"])
            cy += text_height(s, f) + gap
        return cy

    # -------------------------------------------------- table
    def table(self, x, y, cols, rows, header=None, fs=22, rh=None, hc="blue", zebra=True,
              aligns=None, colors=None, bold_rows=(), mono_cols=(), hfs=None, hl_rows=None, hl_c="blue"):
        """cols: list of widths. rows: list of lists (strings). colors[r][c] optional text color."""
        rh = rh or fs * 1.9
        hfs = hfs or fs
        tw = sum(cols)
        aligns = aligns or (["l"] + ["c"] * (len(cols) - 1))
        cy = y
        if header:
            hh = rh * (1 + max(h.count("\n") for h in header) * 0.75)
            self.box(x, cy, tw, hh, None, hc, fill=P[hc]["fill"], stroke=P[hc]["stroke"], sw=1, round_=False, roughness=0)
            cx = x
            for i, h in enumerate(header):
                self._cell(cx, cy, cols[i], hh, h, hfs, P[hc]["text"], aligns[i], False)
                cx += cols[i]
            cy += hh
        hl_rows = hl_rows or {}
        for r, row in enumerate(rows):
            if r in hl_rows:
                col = hl_rows[r]
                self.box(x, cy, tw, rh, None, col, fill=P[col]["soft"], stroke="transparent", sw=1, round_=False, roughness=0)
            elif zebra and r % 2 == 1:
                self.box(x, cy, tw, rh, None, "gray", fill="#f8f9fa", stroke="transparent", sw=1, round_=False, roughness=0)
            cx = x
            for i, v in enumerate(row):
                col = colors[r][i] if colors and colors[r] and colors[r][i] else P["ink"]
                self._cell(cx, cy, cols[i], rh, v, fs, col, aligns[i], i in mono_cols)
                cx += cols[i]
            cy += rh
        self.line([(x, cy), (x + tw, cy)], P["faint"], 1, roughness=0)
        return cy

    def _cell(self, x, y, w, h, s, fs, color, a, mono):
        if s is None or s == "":
            return
        pad = 14
        if a == "l":
            self.text(x + pad, y + h / 2, s, fs, color, "l", "m", mono=mono)
        elif a == "r":
            self.text(x + w - pad, y + h / 2, s, fs, color, "r", "m", mono=mono)
        else:
            self.text(x + w / 2, y + h / 2, s, fs, color, "c", "m", mono=mono)

    # -------------------------------------------------- charts
    def axes(self, x, y, w, h, ymin, ymax, yticks, fmt="{:g}", ylabel=None, fs=18, grid=True):
        def Y(v):
            return y + h - (v - ymin) / (ymax - ymin) * h
        for t in yticks:
            yy = Y(t)
            if grid:
                self.line([(x, yy), (x + w, yy)], P["grid"], 1, roughness=0)
            self.text(x - 12, yy, fmt.format(t), fs, P["muted"], "r", "m")
        self.line([(x, y + h), (x + w, y + h)], P["ink"], 2, roughness=0)
        self.line([(x, y), (x, y + h)], P["ink"], 2, roughness=0)
        if ylabel:
            self.text(x, y - 34, ylabel, fs, P["muted"])
        return Y

    def grouped_bars(self, x, y, w, h, cats, series, ymin, ymax, yticks, colors, names=None,
                     ylabel=None, fs=18, gap=0.3, values=False, vfmt="{:.1f}"):
        Y = self.axes(x, y, w, h, ymin, ymax, yticks, ylabel=ylabel, fs=fs)
        n = len(cats)
        k = len(series)
        slot = w / n
        bw = slot * (1 - gap) / k
        for i, c in enumerate(cats):
            x0 = x + i * slot + slot * gap / 2
            for j, s in enumerate(series):
                v = s[i]
                top = Y(v)
                pal = P[colors[j]]
                self.box(x0 + j * bw + 2, top, bw - 4, Y(ymin) - top, None, colors[j], sw=2, round_=False)
                if values:
                    self.text(x0 + j * bw + bw / 2, top - 6, vfmt.format(v), fs - 2, pal["text"], "c", "b")
            self.text(x + i * slot + slot / 2, y + h + 12, c, fs + 2, P["ink"], "c")
        return Y


def dump(slides, outdir):
    os.makedirs(outdir, exist_ok=True)
    for s in slides:
        with open(os.path.join(outdir, s.name + ".json"), "w") as f:
            json.dump(s.els, f, ensure_ascii=False, separators=(",", ":"))
