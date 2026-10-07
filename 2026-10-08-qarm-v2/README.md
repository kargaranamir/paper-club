# QARM V2: paper club, 8 October 2026

**Paper:** Tian Xia, Jiaqi Zhang, Yueyang Liu, Hongjian Dou, Tingya Yin, Jiangxia Cao et al. (Kuaishou).
*QARM V2: Quantitative Alignment Multi-Modal Recommendation for Reasoning User Sequence Modeling.*
[arXiv:2602.08559](https://arxiv.org/abs/2602.08559)

**Predecessor:** Xinchen Luo, Jiangxia Cao et al. (Kuaishou). *QARM: Quantitative Alignment Multi-Modal
Recommendation at Kuaishou.* [arXiv:2411.11739](https://arxiv.org/abs/2411.11739)

| What | Where |
|---|---|
| Clickable deck (arrow keys, `N` notes, `O` overview, `F` full screen) | [`slides/index.html`](slides/index.html) |
| PDF (28 slides, 16:9) | [`slides/qarm-v2.pdf`](slides/qarm-v2.pdf) |
| Speaker notes | [`slides/speaker-notes.md`](slides/speaker-notes.md) |
| Editable Excalidraw file per slide | [`slides/excalidraw/`](slides/excalidraw), open on excalidraw.com (menu → Open) |
| Every number used, with its table or section | [`references/digest.md`](references/digest.md) |

## Outline (28 slides)

1 Title · 2 The paper in one slide · 3–4 glossary (models; quantization, metrics, business terms)
- **Part I, background:** 5 Kuaishou setting · 6 GSU/ESU two-stage sequence modelling · 7 IDs vs LLM tokens ·
  8 why naive LLM embeddings give little · 9 QARM (2024) · 10 QARM results · 11 what V2 changes
- **Part II, GSU side:** 12 noisy alignment pairs · 13 reasoning data pipeline · 14 three-segment attention mask
- **Part III, ESU side:** 15 why semantic IDs collide (K-means vs FSQ) · 16 Res-KmeansFSQ: a semantic ID in three
  rounds · 17 how the embedding and SIDs enter the ranker · 18 frozen address, learned meaning · 19 what is trained,
  when, with which objective
- **Part IV, results:** does each part work? 20 retrieval hit rate · 21 code collisions · 22 GSU exclusive retrieval;
  does the whole work? 23 Amazon Book · 24 offline GAUC gains · 25 online ads and shopping · 26 online live streaming
- **Part V, discussion:** 27 strengths and weaknesses · 28 takeaways

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
