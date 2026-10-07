# QARM V2: paper club, 8 October 2026

**Paper:** Tian Xia, Jiaqi Zhang, Yueyang Liu, Hongjian Dou, Tingya Yin, Jiangxia Cao et al. (Kuaishou).
*QARM V2: Quantitative Alignment Multi-Modal Recommendation for Reasoning User Sequence Modeling.*
[arXiv:2602.08559](https://arxiv.org/abs/2602.08559)

**Predecessor:** Xinchen Luo, Jiangxia Cao et al. (Kuaishou). *QARM: Quantitative Alignment Multi-Modal
Recommendation at Kuaishou.* [arXiv:2411.11739](https://arxiv.org/abs/2411.11739)

| What | Where |
|---|---|
| Clickable deck (arrow keys, `N` notes, `O` overview, `F` full screen) | [`slides/index.html`](slides/index.html) |
| PDF (25 slides, 16:9) | [`slides/qarm-v2.pdf`](slides/qarm-v2.pdf) |
| Speaker notes | [`slides/speaker-notes.md`](slides/speaker-notes.md) |
| Editable Excalidraw file per slide | [`slides/excalidraw/`](slides/excalidraw), open on excalidraw.com (menu → Open) |
| Every number used, with its table or section | [`references/digest.md`](references/digest.md) |

## Outline (25 slides)

1 Title · 2 The paper in one slide
- **Part I, background:** 3 Kuaishou setting · 4 GSU/ESU two-stage sequence modelling · 5 IDs vs LLM tokens ·
  6 why naive LLM embeddings give little · 7 QARM (2024) · 8 QARM results · 9 what V2 changes
- **Part II, GSU side:** 10 noisy alignment pairs · 11 reasoning data pipeline · 12 three-segment attention mask
- **Part III, ESU side:** 13 why semantic IDs collide (K-means vs FSQ) · 14 Res-KmeansFSQ · 15 how embedding and
  SIDs enter the ranker
- **Part IV, results:** 16 Amazon Book · 17 offline GAUC gains · 18 online ads and shopping · 19 online live
  streaming · 20 retrieval hit rate · 21 code collisions · 22 GSU exclusive retrieval
- **Part V, discussion:** 23 strengths and weaknesses · 24 discussion questions · 25 takeaways

## Editing

All slides are generated from Python, so edit the source, not the files in `slides/`.

- `tools/slides.py`: one function per slide; order = the `SLIDES` list at the bottom.
- `tools/notes.py`: speaker notes, keyed by slide slug.
- `tools/slidekit.py`: palette and drawing helpers (text, boxes, arrows, tables, bar charts).

```bash
pip install --break-system-packages fonttools brotli pillow
cd tools/render && npm ci && npx esbuild entry.js --bundle --format=iife --outfile=dist/bundle.js \
  --loader:.css=empty --define:process.env.NODE_ENV='"production"' --minify --log-level=error && cd ../..
tools/preview.sh 12 13          # rebuild two slides, PNGs in /tmp/slide-previews
tools/build_all.sh              # everything: .excalidraw, .svg, PDF, HTML deck, notes
```

Rendering uses headless Chromium (`/opt/pw-browsers/chromium`, or set `CHROMIUM_PATH`) and `pdfunite` (poppler).
The toolchain is copied from [glotlid-slides](https://github.com/kargaranamir/glotlid-slides).
