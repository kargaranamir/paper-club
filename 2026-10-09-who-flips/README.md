# Who Flips? Paper club, 9 October 2026

**Paper:**
*Who Flips? Self- and Cross-Model Counterarguments Reveal Answer Instability in LLMs.*
[arXiv:2606.16011v2](https://arxiv.org/abs/2606.16011v2), revised 30 August 2026; EMNLP Findings 2026.

A 16:9 presentation with **20 main slides and eight backups** using the same Python → Excalidraw → SVG → HTML/PDF workflow as the QARM V2 deck in this repository. No new model inference experiments were run. Figures are original explanatory drawings based on the paper's published results. The teaching dialogue on slide 2 and the selection outcomes on slide 13 are explicitly illustrative.

| What | Where |
|---|---|
| Self-contained clickable deck | [`slides/index.html`](slides/index.html) |
| Preview of selected slides | [`slides/preview.png`](slides/preview.png) |
| PDF, 28 slides | [`slides/who-flips.pdf`](slides/who-flips.pdf) |
| A0 portrait poster, HTML and editable sources | [`poster/`](poster/) |
| Print-ready A0 poster PDF | [`poster/who-flips-a0.pdf`](poster/who-flips-a0.pdf) |
| Speaker notes | [`slides/speaker-notes.md`](slides/speaker-notes.md) |
| All slides on one editable Excalidraw canvas | [`slides/all-slides.excalidraw`](slides/all-slides.excalidraw) |
| Editable Excalidraw file per slide | [`slides/excalidraw/`](slides/excalidraw/) |
| Vector exports | [`slides/svg/`](slides/svg/) |
| Numerical provenance and source audit | [`references/digest.md`](references/digest.md) |
| Machine-readable published values | [`references/data.json`](references/data.json) |

Download `slides/index.html` and open it in a browser. It embeds the slide images and notes and works offline. Arrow keys navigate, `N` shows notes, `O` opens the overview `F` enters fullscreen, and `B` jumps between the backups and the opening slide. To edit a drawing directly, open its `.excalidraw` file at [excalidraw.com](https://excalidraw.com) using menu → Open. Generated exports will be overwritten on rebuild, so make lasting changes in the Python source.

## Story

**Main talk (1–20):** a correct answer under challenge, the protocol and conditional AFR, the model comparison, argument length and attribution, subject differences, source and target roles, the cross-model matrix and EA–EP map, MaxFlip selection and gains, producer/refusal behavior, scope, proposed next experiments, and the takeaway.

**Backups (21–28):** exact model configurations, attribution conditions, all seven argument-length sweeps, coverage and uncertainty, model-size comparisons, linguistic correlates, variance decomposition, and source discrepancies.

The first empirical result is on slide 5. The main talk is designed for roughly 25 minutes, with the backups available for questions.

The source audit distinguishes minor rounding differences from larger prose/table inconsistencies. In particular, the producer shares remain exactly as printed, even though they sum to 96.1%. All reported effects retain their conditions; the blind average over lengths is not confused with the k = 10 baseline used for MaxFlip.

## Figures

All charts, diagrams, marks and labels remain native editable Excalidraw objects. Handwritten headings sit above plain chart labels. The deck uses point-and-interval comparisons, connected trajectories, a sequential matrix and model-role scatterplots. A concrete role-swap example introduces the matrix, and a candidate-by-target schematic explains MaxFlip selection.

The EA–EP map on slide 11 reproduces marker positions recovered from the original Figure 5 vector PDF. [Extraction provenance](references/ea-ep-provenance.json) records the coordinates and method. The positions are graphical reconstructions, not new estimates or means substituted from rounded matrix cells. The [GlotLID calibration report](https://kshkrvea.github.io/lid-calibration/report/) informed the earlier use of connected comparisons and repeated panels.

Open the combined canvas or an individual slide in [Excalidraw](https://excalidraw.com). Each slide has a named frame on the combined canvas. Editing an exported canvas does not update the generator; make lasting rebuildable changes in `tools/slides.py`.

## Rebuild

Requirements: Python 3, Node.js, npm, Chrome/Chromium, and Poppler (`pdfunite`). Install Python dependencies in a virtual environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install fonttools brotli pillow pypdf
cd tools/render
npm ci
npx esbuild entry.js --bundle --format=iife --outfile=dist/bundle.js \
  --loader:.css=empty --define:process.env.NODE_ENV='"production"' --minify --log-level=error
cd ../..
export CHROMIUM_PATH="/path/to/chrome-or-chromium"
tools/build_all.sh
```

On macOS, `CHROMIUM_PATH` can be `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`. The inherited Linux default is `/opt/pw-browsers/chromium`.

- `tools/slides.py`: one function per slide; the `SLIDES` list sets order.
- `tools/data.py`: transcribed results used by charts and tables.
- `tools/notes.py`: narrative and per-slide speaker notes.
- `tools/slidekit.py`: teal palette, text metrics and drawing helpers.
- `tools/build.py`: Excalidraw element skeletons.
- `tools/render/render.mjs`: actual Excalidraw library conversion and SVG export.
- `tools/render/pdf.mjs`: browser PDF export and merge.
- `tools/make_deck.py`: self-contained HTML viewer, notes and combined Excalidraw canvas.
- `tools/validate.py`: source/export consistency, bounds and PDF page checks.

```bash
python tools/validate.py
# Optional visual previews of selected slides:
tools/preview.sh 9 11 13 14
```

The renderer retains stable element IDs and deterministic drawing seeds. The toolchain is adapted from this repository's [`2026-10-08-qarm-v2`](../2026-10-08-qarm-v2) presentation, itself derived from [glotlid-slides](https://github.com/kargaranamir/glotlid-slides).

## Sources and attribution

Paper [PDF](https://arxiv.org/pdf/2606.16011v2) and [LaTeX source](https://arxiv.org/src/2606.16011v2). Research code: [WhoFlips](https://github.com/nafisenik/WhoFlips). Dataset: [Hugging Face](https://huggingface.co/datasets/nafisehNik/WhoFlips). Paper attribution is provided through its title and source links. The repository's MIT license applies to this added presentation/tooling; this does not change the source paper's license.
