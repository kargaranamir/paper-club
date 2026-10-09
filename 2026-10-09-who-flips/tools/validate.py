"""Validate the complete deck without requiring browser automation."""
from pathlib import Path
import json, re, sys
from pypdf import PdfReader
from slides import SLIDES
from notes import NOTES
from data import *
root=Path(__file__).resolve().parents[1]
errors=[]
expected=[f'{i:02d}-{f(i).name}' for i,f in enumerate(SLIDES,1)]
for folder,suffix in [('src','.json'),('excalidraw','.excalidraw'),('svg','.svg')]:
 actual=sorted(p.stem for p in (root/'slides'/folder).glob('*'+suffix))
 if actual!=expected: errors.append(f'{folder}: unexpected file set')
for stem in expected:
 if stem[3:] not in NOTES or len(NOTES[stem[3:]].split())<60: errors.append(f'{stem}: missing or sparse notes')
 p=root/'slides/excalidraw'/f'{stem}.excalidraw'
 scene=json.loads(p.read_text());els=scene['elements'];ids=[e['id'] for e in els]
 if len(ids)!=len(set(ids)): errors.append(f'{stem}: duplicate IDs')
 if scene['type']!='excalidraw' or scene['version']!=2: errors.append(f'{stem}: invalid scene header')
 for e in els:
  if e['type']=='text':
   if not (25<=e['x'] and e['x']+e['width']<=1550 and 0<=e['y'] and e['y']+e['height']<=890): errors.append(f"{stem}: text outside safe bounds: {e['text'][:60]}")
 svg=(root/'slides/svg'/f'{stem}.svg').read_text()
 if 'width="1600"' not in svg or 'height="900"' not in svg: errors.append(f'{stem}: SVG dimensions')
html=(root/'slides/index.html').read_text()
match=re.search(r'const S = (.*);\nlet i =',html)
entries=json.loads(match.group(1)) if match else []
if len(entries)!=len(expected): errors.append('HTML slide count')
for entry,stem in zip(entries,expected):
 if entry['name']!=stem or entry['note']!=NOTES[stem[3:]]: errors.append(f'{stem}: stale viewer data')
reader=PdfReader(root/'slides/who-flips.pdf')
if len(reader.pages)!=len(expected): errors.append('PDF page count')
for i,p in enumerate(reader.pages,1):
 w,h=float(p.mediabox.width),float(p.mediabox.height)
 if abs(w/h-16/9)>.001: errors.append(f'PDF page {i}: aspect ratio')
 if len(p.extract_text().strip())<40: errors.append(f'PDF page {i}: missing text')
if round(sum(PRODUCER),1)!=96.1: errors.append('published producer shares changed')
if len(MATRIX)!=7 or any(len(row)!=7 for row in MATRIX): errors.append('matrix dimensions')
board=json.loads((root/'slides/all-slides.excalidraw').read_text())
board_ids=[e['id'] for e in board['elements']]
frames={e['id'] for e in board['elements'] if e['type']=='frame'}
if len(frames)!=len(expected): errors.append('combined canvas frame count')
if len(board_ids)!=len(set(board_ids)): errors.append('combined canvas duplicate IDs')
for e in board['elements']:
 if e['type']=='image': errors.append('combined canvas contains a raster element')
 if e['type']!='frame' and e.get('frameId') not in frames: errors.append('combined canvas orphan element')
if errors:
 print('\n'.join(errors));sys.exit(1)
print(f'PASS: {len(expected)} source scenes, Excalidraw files, SVGs, notes and PDF pages; safe text bounds and embedded viewer consistency.')
