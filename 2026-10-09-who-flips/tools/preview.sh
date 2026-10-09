#!/bin/bash
# usage: tools/preview.sh [slide-ids...]  -> builds, renders, tiles 2x2 PNGs into $PNG
set -e
cd "$(dirname "$0")"
PNG=${PNG:-/tmp/slide-previews}
python3 build.py "$@" | tail -1
names=$(python3 build.py "$@" | tail -1 | sed 's/.*built: //')
srcs=""; svgs=""
for n in $names; do srcs="$srcs ../../slides/src/$n.json"; svgs="$svgs ../../slides/svg/$n.svg"; done
(cd render && node render.mjs $srcs >/dev/null && node shoot.mjs $PNG $svgs)
PNG=$PNG python3 - $names <<'PY'
import sys; from PIL import Image
import os; d=os.environ.get('PNG','/tmp/slide-previews')
ns=sys.argv[1:]
for i in range(0,len(ns),4):
    im=Image.new('RGB',(1600,900),'white')
    for j,n in enumerate(ns[i:i+4]):
        t=Image.open(f'{d}/{n}.png').convert('RGB').resize((800,450)); im.paste(t,((j%2)*800,(j//2)*450))
    im.save(f'{d}/tile-{ns[i]}.png'); print(f'{d}/tile-{ns[i]}.png')
PY
