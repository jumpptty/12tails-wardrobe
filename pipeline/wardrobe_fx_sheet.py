"""Contact sheets of effect QA shots (2026-11-13, the Penguin's QA pass): wardrobe_fx_shots.py's PNGs grouped by tile (and
forced skill / roll, backdrop, props), one row per group in shot-time order, each frame cropped to the middle of the
1366 x 768 page (the picker and the side panels left out) and labelled with its file name's tail.
  py -3 pipeline/wardrobe_fx_sheet.py <shots dir> <out dir> [--cols 6] [--width 360]
Writes <out>/<group>.png (a sheet per group) and <out>/index.html (every sheet on one page)."""
import argparse, html, re
from collections import defaultdict
from pathlib import Path
from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("shots", type=Path)
ap.add_argument("out", type=Path)
ap.add_argument("--cols", type=int, default=6)
ap.add_argument("--width", type=int, default=360)
A = ap.parse_args()
A.out.mkdir(parents=True, exist_ok=True)

# <cls>_<tile>_<view>_<t>[_rest].png  (wardrobe_fx_shots.py's names)
NAME = re.compile(r"^(?P<cls>[a-z]+)_(?P<tile>.+?)_(?P<view>side|front|back|far|top|near|book|spot|bookside|bookback|behind)_(?P<t>\d\d\.\d\d)(?P<rest>.*)\.png$")
groups = defaultdict(list)
for p in sorted(A.shots.glob("*.png")):
    m = NAME.match(p.name)
    if m:
        groups[f"{m['cls']}_{m['tile']}_{m['view']}{m['rest']}"].append((float(m["t"]), p))

CROP = (458, 60, 1248, 700)   # the stage around the hero (right of the side panel), 790 x 640
items = []
for g, shots in sorted(groups.items()):
    shots.sort()
    w = A.width; h = round(w * (CROP[3] - CROP[1]) / (CROP[2] - CROP[0]))
    rows = (len(shots) + A.cols - 1) // A.cols
    sheet = Image.new("RGB", (min(len(shots), A.cols) * w, rows * (h + 18) + 22), (40, 40, 40))
    d = ImageDraw.Draw(sheet)
    d.text((4, 4), g, fill=(255, 255, 255))
    for i, (t, p) in enumerate(shots):
        im = Image.open(p).convert("RGB").crop(CROP).resize((w, h))
        x, y = (i % A.cols) * w, 22 + (i // A.cols) * (h + 18)
        sheet.paste(im, (x, y))
        d.text((x + 4, y + h + 3), f"t {t:.2f} s", fill=(255, 220, 120))
    sheet.save(A.out / f"{g}.png")
    items.append(g)

(A.out / "index.html").write_text("<!doctype html><meta charset=utf-8><title>FX QA sheets</title><body style='background:#222;color:#eee;font:13px sans-serif'>"
                                  + "".join(f"<h3>{html.escape(g)}</h3><img src='{html.escape(g)}.png' style='max-width:100%'>" for g in items), encoding="utf-8")
print(len(items), "sheets in", A.out)
