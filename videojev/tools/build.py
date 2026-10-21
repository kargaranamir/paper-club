"""Generate every slide skeleton into slides/src/*.json (Excalidraw MCP format).
Usage: python3 build.py [slide numbers or names]  (no arguments = all slides)"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from slidekit import dump  # noqa: E402
from slides import SLIDES  # noqa: E402

only = set(sys.argv[1:])
out = []
for i, f in enumerate(SLIDES, 1):
    s = f(i)
    # file names are numbered by position, so inserting/removing a slide renumbers everything
    s.name = f"{i:02d}-" + (s.name[3:] if s.name[:2].isdigit() else s.name)
    if not only or s.name in only or str(i) in only:
        out.append(s)
dump(out, os.path.join(os.path.dirname(__file__), "../slides/src"))
print(len(SLIDES), "slides;", "built:", " ".join(s.name for s in out))
