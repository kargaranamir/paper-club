# Who Flips? Paper club, 9 October 2026

**Paper:**
*Who Flips? Self- and Cross-Model Counterarguments Reveal Answer Instability in LLMs.*
[arXiv:2606.16011v2](https://arxiv.org/abs/2606.16011v2), revised 30 August 2026; EMNLP Findings 2026.

A 28-slide, 16:9 presentation using the same Python → Excalidraw → SVG → HTML/PDF workflow as the QARM V2 deck in this repository. No new model inference experiments were run. Figures are original explanatory drawings based on the paper's published results. The teaching example on slide 3 is explicitly invented.

| What | Where |
|---|---|
| Self-contained clickable deck | [`slides/index.html`](slides/index.html) |
| PDF, 28 slides | [`slides/who-flips.pdf`](slides/who-flips.pdf) |
| Speaker notes | [`slides/speaker-notes.md`](slides/speaker-notes.md) |
| Editable Excalidraw file per slide | [`slides/excalidraw/`](slides/excalidraw/) |
| Vector exports | [`slides/svg/`](slides/svg/) |
| Numerical provenance and source audit | [`references/digest.md`](references/digest.md) |
| Machine-readable published values | [`references/data.json`](references/data.json) |

Download `slides/index.html` and open it in a browser. It embeds the slide images and notes and works offline. Arrow keys navigate, `N` shows notes, `O` opens the overview and `F` enters fullscreen. To edit a drawing directly, open its `.excalidraw` file at [excalidraw.com](https://excalidraw.com) using menu → Open. Generated exports will be overwritten on rebuild, so make lasting changes in the Python source.

## Story

1–2: title and main result. 3–6: worked teaching example, two-stage protocol, conditional AFR and attribution/source conditions. 7–8: model setup, eligibility and uncertainty. 9–15: model differences, argument length, scale, self-attribution, refusal, language and subjects. 16–19: cross-model matrix, average effects, variance decomposition and source/target roles. 20–22: MaxFlip selection, gains and producers. 23–28: controls, strengths, limitations, source audit, discussion and takeaways.

The source audit distinguishes minor rounding differences from larger prose/table inconsistencies. In particular, the producer shares remain exactly as printed, even though they sum to 96.1%. All reported effects retain their conditions; the blind average over lengths is not confused with the k = 10 baseline used for MaxFlip.

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
- `tools/slidekit.py`: original repository palette and drawing helpers.
- `tools/build.py`: Excalidraw element skeletons.
- `tools/render/render.mjs`: actual Excalidraw library conversion and SVG export.
- `tools/render/pdf.mjs`: browser PDF export and merge.
- `tools/make_deck.py`: self-contained HTML viewer and notes.
- `tools/validate.py`: source/export consistency, bounds and PDF page checks.

```bash
python tools/validate.py
# Optional visual previews of selected slides:
tools/preview.sh 12 16 21
```

The renderer retains stable element IDs and deterministic drawing seeds. The toolchain is adapted from this repository's [`2026-10-08-qarm-v2`](../2026-10-08-qarm-v2) presentation, itself derived from [glotlid-slides](https://github.com/kargaranamir/glotlid-slides).

## Sources and attribution

Paper [PDF](https://arxiv.org/pdf/2606.16011v2) and [LaTeX source](https://arxiv.org/src/2606.16011v2). Research code: [WhoFlips](https://github.com/nafisenik/WhoFlips). Dataset: [Hugging Face](https://huggingface.co/datasets/nafisehNik/WhoFlips). Paper attribution is provided through its title and source links. The repository's MIT license applies to this added presentation/tooling; this does not change the source paper's license.
