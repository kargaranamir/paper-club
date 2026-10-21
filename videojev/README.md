# VideoJev: paper club

**Paper:** Yuhan Zhu, Xiangyu Zeng, Qingyi Si, … , Nan Duan, Limin Wang (Nanjing University, JD.com, et al.).
*VideoJev: System One Model for Video Understanding and Interaction.*
[arXiv:2610.18615](https://arxiv.org/abs/2610.18615) (13 Oct 2026) ·
[project page](https://mcg-nju.github.io/VideoJev/) · [code](https://github.com/MCG-NJU/VideoJev) ·
[models](https://huggingface.co/collections/MCG-NJU/videojev)

| What | Where |
|---|---|
| Clickable deck (arrow keys, `N` notes, `O` overview, `F` full screen) | [`slides/index.html`](slides/index.html) |
| PDF (26 slides, 16:9) | [`slides/videojev.pdf`](slides/videojev.pdf) |
| Speaker notes (six-sentence story first, then a script per slide) | [`slides/speaker-notes.md`](slides/speaker-notes.md) |
| Editable Excalidraw file per slide | [`slides/excalidraw/`](slides/excalidraw), open on excalidraw.com (menu → Open) |
| Every number used, with its table or section | [`references/digest.md`](references/digest.md) |

## Outline (26 slides)

1 Title · 2 The paper in one slide · 3 Glossary
- **Part I, background:** 4 two tasks: When? and Which? · 5 today's MLLMs write their answers · 6 Thinking, Fast and Slow (Kahneman) · 7 the System One
  idea (Jev) · 8 why video is harder
- **Part II, method:** 9 architecture · 10 the shared scorer · 11 why one candidate = two frames · 12 grounding as many yes/no decisions · 13 decoding
  one span (real README output) · 14 QA as option scoring · 15 Cached and Joint inference · 16 training recipe
- **Part III, results:** 17 temporal grounding · 18 video QA vs Thinking · 19 quality against latency ·
  20 ten questions about one video · 21 architecture or data? · 22 ablations · 23 confidence and calibration ·
  24 System 2 asks, System 1 checks
- **Part IV, discussion:** 25 strengths and weaknesses · 26 takeaways

All figures are redrawn in Excalidraw; the paper's own figures are not copied. Slide 13 uses the recorded output
from the repository README.

## Editing

Same toolchain as the QARM V2 deck. Edit the source, not the files in `slides/`.

- `tools/slides.py`: one function per slide; order = the `SLIDES` list at the bottom.
- `tools/notes.py`: speaker notes (`STORY` + one note per slide slug).
- `tools/slidekit.py`: palette and drawing helpers.

```bash
pip install --break-system-packages fonttools brotli pillow
cd tools/render && npm ci && npx esbuild entry.js --bundle --format=iife --outfile=dist/bundle.js \
  --loader:.css=empty --define:process.env.NODE_ENV='"production"' --minify --log-level=error && cd ../..
tools/preview.sh 9 11           # rebuild two slides, PNGs in /tmp/slide-previews
tools/build_all.sh              # everything: .excalidraw, .svg, PDF, HTML deck, notes
```
