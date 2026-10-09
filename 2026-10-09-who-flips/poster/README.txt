WHO FLIPS? — FLIPBOOK-INSPIRED A0 HTML POSTER

Open who-flips-a0.html in a modern browser. It is a complete, standalone HTML
file: fonts, diagrams, charts and QR codes are embedded. No network access or
installation is needed to view it. The research links open external pages.

The design draws on the warm paper, pink/yellow display lettering, dark
outlines and offset card shadows at https://hadro.github.io/flipbook/.
The poster layout, wording and graphics were created for Who Flips?.

VIEW AND PRINT
- Fit width fits the complete poster width to your screen.
- 100% lets you inspect the poster and pan at its full CSS size.
- Print A0 opens the browser's print dialog.
- Use A0 portrait (841 x 1189 mm), 100% / Actual Size, no margins,
  background graphics enabled, and browser headers/footers disabled.
- who-flips-a0.pdf is the checked, one-page A0 print export. Its page box is
  normalized to exact ISO A0 dimensions to remove browser rounding.

EDIT
poster.template.html contains the layout, text, CSS and simple screen controls.
who-flips-a0.html is the assembled, ready-to-use artifact.
figures/excalidraw contains native editable objects. The combined
all-poster-figures.excalidraw canvas contains the eight graphics used here, arranged in poster reading order.
figures/svg contains the vector exports embedded into the HTML.
figures/pdf contains optional vector PDFs for reuse.
The older protocol and attribution figures are retained as optional assets.

REBUILD
The delivered HTML and PDF do not require these build dependencies.
To regenerate the assembled HTML after edits:
  python -m pip install reportlab
  python tools/build_html.py
Fonts are supplied in fonts/ under the SIL Open Font License. License notices
are also embedded inside the standalone HTML as non-executable JSON.

To regenerate the Excalidraw graphics:
  python -m pip install fonttools
  python tools/build_figures.py
  cd tools
  npm install
  CHROMIUM_PATH="/path/to/chrome" node render_figures.mjs
Set FIGURE_FONT to an Arial-compatible TTF on systems without macOS Arial.
Rebuild the HTML after regenerating figures. Manual Excalidraw edits are not
read by build_figures.py; export edited SVGs directly instead.

To export the HTML with headless Chrome:
  CHROMIUM_PATH="/path/to/chrome" node tools/print_poster.mjs
The CSS @page rule defines the A0 sheet. The print stylesheet removes the
screen toolbar and zoom transform. All graphics remain vectors.

RESEARCH ATTRIBUTION AND DATA
Paper: Who Flips? Self- and Cross-Model Counterarguments Reveal Answer
Instability in LLMs, arXiv:2606.16011v2, 30 August 2026.
https://arxiv.org/abs/2606.16011v2
The poster credits the paper's published authors and affiliations.
Poster adaptation: Codex. No experiments were rerun.

baseline: Table 2; blind AFR means, reported CI half-widths and coverage.
length: Table 2; four explicitly selected models, all four sentence counts.
maxflip: Table 7; reported gains and CI half-widths, not rounded subtraction.
cross-matrix: Figure 4; its displayed whole-percent AFR values, recolored on
an absolute sequential scale. Source rows, target columns, k=10.
ea-ep: Figure 5; point positions redrawn from the original vector PDF.
Axis ticks calibrate the marker coordinates; these are graphical reconstructions,
not new estimates or raw data. Figure 5 positions are retained rather than
substituting Table 6 means or re-averaging Figure 4's rounded cells. Coordinates
and extraction provenance are supplied in figures/ea-ep-provenance.json.
EP is the off-diagonal column mean (target susceptibility); EA is the
off-diagonal row mean (efficacy of wrong arguments as a source).
pooling: schematic of the paper's MaxFlip procedure. The illustrated stack
represents a pool of candidates, not a measured number of sources or scores.
Selection maximizes the number of target models flipped for each question;
ties are broken randomly. Selection and evaluation share the model set.
mechanism: schematic of the protocol, not a quoted experimental example.

AFR remains conditional on initial correctness and an available argument.
Any final wrong option counts. The paper's distinctions between same-model
source, anonymous presentation and self-attribution are preserved.
GPT-5.1's MaxFlip gain is not labeled significant; its CI crosses zero.
No held-out-model or open-ended/multi-turn generalization is claimed.
Reported 95% CIs use 2,000 question-cluster bootstrap replicates.

TYPOGRAPHY
Bricolage Grotesque and Space Mono match the reference theme. Google Fonts
supplied the open-license source fonts; print subsets are embedded in HTML.
The native Excalidraw objects use its standard sans-serif font slot; the
HTML applies Bricolage Grotesque to inline vector text for a consistent theme.

Sources for the visual direction:
https://hadro.github.io/flipbook/
https://vilda.net/?page=typesetting

LATEST REVISION: SUBJECT-DOMAIN RESULTS
Removed the requested footer scope, bootstrap and date/source text.
The takeaway and research QR links now sit in the header.
The first two figure sources and all seven existing graphics are unchanged.
A full-width subject-domain strip shows the three lowest and three highest
subject-level AFRs from Table 5, with reported confidence intervals. These
are selected subject results, not averages of broad domain categories.
Values and category labels are recorded in figures/domain-data.json.
The source-target/EA-EP row follows, with both MaxFlip panels still last.
A0 portrait dimensions, embedded assets and the original theme are retained.

The explanatory caption below the baseline plot has been removed.

The poster omits figure/table references and citation wording in its text.
The arXiv paper, GitHub code and Hugging Face data QR links are retained.
Source provenance remains documented in this editable package.

The yellow self-attribution callout is omitted; its panel is now labeled
Argument Length. The optional attribution graphic remains in the source assets.

The header slogan is an editable inline-SVG speech cloud in poster.template.html.
Its text remains live HTML; the pale yellow fill, ink shadow and pink emphasis
follow the poster palette. No chart values changed for this revision.
