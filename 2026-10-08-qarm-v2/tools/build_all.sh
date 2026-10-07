#!/bin/bash
# Rebuild everything: slides.py -> slides/src/*.json -> .excalidraw + .svg -> PDF -> HTML deck + speaker notes.
set -e
cd "$(dirname "$0")"
rm -f ../slides/src/*.json ../slides/svg/*.svg ../slides/excalidraw/*.excalidraw
python3 build.py
cd render
[ -d node_modules ] || npm ci
[ -f dist/bundle.js ] || npx esbuild entry.js --bundle --format=iife --outfile=dist/bundle.js --loader:.css=empty --define:process.env.NODE_ENV='"production"' --minify --log-level=error
node render.mjs ../../slides/src/*.json
node pdf.mjs ../../slides/qarm-v2.pdf ../../slides/svg/*.svg
cd ..
python3 make_deck.py
