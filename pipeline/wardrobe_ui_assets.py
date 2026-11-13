r"""Icons and face thumbnails for the wardrobe's topic rows and pickers (user 2026-11-04: "each topic shows only the topic
name and the icon of the current selection in a circular frame ... for the face, use something that only focuses on
the face overlay itself, not the entire texture UV").

  uv run --no-project --with UnityPy --with pillow --with numpy python wardrobe_ui_assets.py [--faces-only]
  -> wardrobe/data/icons/heroes/<class>1-5.webp, icons/skills/emotion/<name>.webp, icons/skills/<class>/<name>.webp
     wardrobe/data/ui.json  {heroes: {cls: icon}, emotion: [names], skills: {cls: [names]},
                             faceBox: {cls: [x0, y0, x1, y1]}}
faceBox: the square of the 256 face overlay where that class's faces draw (union of every face's pixels); the page
crops the overlay webp (data/<class>/faces/<n>.webp, user: "use this for the face icon") to it with object-view-box.
--faces-only: keep the icons and ui.json, recompute faceBox only.
The icons are written at the game's size; one already upscaled from the same picture is left alone (run
wardrobe_icons_upscale.py afterwards for the new ones).
"""
import json
import os
import re
import subprocess
import sys

import numpy as np
import UnityPy
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from wardrobe_icons_upscale import keep as keep_upscaled   # noqa: E402
ROOT = os.path.dirname(HERE)
VIDEO = os.path.join(os.path.dirname(ROOT), "12tails-video")  # extracted inputs, read only (the 2026-11-09 repo split)
ASSETS = os.path.join(VIDEO, "tto_assets", "2026-11-04")
TOOLS = r"D:\12tails\DecompiledSource_TTO_2026-11-02\tools"
OUT = os.path.join(ROOT, "wardrobe", "data")
CLASSES = ["bat", "bison", "cat", "chameleon", "mole", "monkey", "panda", "penguin", "rabbit", "sheep", "whale", "wolf"]

UI_JSON = os.path.join(OUT, "ui.json")
if "--faces-only" in sys.argv:
    ui = json.load(open(UI_JSON))
else:
    cat = subprocess.run([sys.executable, "-P", os.path.join(TOOLS, "aa_catalog.py"), os.path.join(ASSETS, "catalog.bin"),
                          "--grep", r"^gamegui/icons/(heroes|skills/[a-z]+)/[^/]+$"],
                         capture_output=True, text=True, encoding="utf-8", check=True).stdout
    want, bundles = {}, set()
    for line in cat.splitlines():
        p = line.split("\t")
        if len(p) >= 4 and p[1].endswith("Texture2D"):
            sub = p[0][len("gamegui/icons/"):]
            want[sub] = p[2]
            bundles.add(p[3].split()[0])
    env = UnityPy.load(*[os.path.join(ASSETS, "dec", b) for b in sorted(bundles)])
    cont = dict(env.container.items())
    ui = {"heroes": {}, "emotion": [], "skills": {c: [] for c in CLASSES}}
    for sub, iid in sorted(want.items()):
        if iid not in cont:
            continue
        path = os.path.join(OUT, "icons", *sub.split("/")) + ".webp"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        image = cont[iid].read().image
        if not keep_upscaled(path, image):                  # its upscale stays (wardrobe_icons_upscale.py)
            image.save(path, "WEBP", lossless=True)
        parts = sub.split("/")
        if parts[0] == "heroes":
            m = re.fullmatch(r"([a-z]+)(\d)", parts[1])
            if m and m.group(2) == "1":
                ui["heroes"][m.group(1)] = f"icons/{sub}.webp"
        elif parts[1] == "emotion":
            ui["emotion"].append(parts[2])
        elif parts[1] in ui["skills"]:
            ui["skills"][parts[1]].append(parts[2])
    print("icons:", len(want), "| heroes", len(ui["heroes"]), "| emotion", len(ui["emotion"]),
          "| skills", sum(len(v) for v in ui["skills"].values()), flush=True)

# face frames: the overlays are 256 x 256 (the face block). A square around where 96% of all the class's faces' drawn
# pixels fall (2nd-98th percentile per axis): the outer edge of every face together is set by a few tears / blushes /
# shading and left the eyes small in a corner (Sheep: 224 px wide against 90 px for the features)
ui["faceBox"] = {}
for cls in CLASSES:
    fdir = os.path.join(OUT, cls, "faces")
    acc = np.zeros((256, 256))
    for f in os.listdir(fdir):
        if f.endswith(".webp"):
            acc += np.asarray(Image.open(os.path.join(fdir, f)).convert("RGBA"))[:, :, 3] > 24
    span = lambda v: [int(np.searchsorted(np.cumsum(v) / v.sum(), q)) for q in (0.02, 0.98)]
    (x0, x1), (y0, y1) = span(acc.sum(0)), span(acc.sum(1))
    side = min(256, int(max(x1 - x0, y1 - y0) * 1.15) + 8)   # square, a little margin, kept inside the 256 block
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    sx, sy = max(0, min(256 - side, cx - side // 2)), max(0, min(256 - side, cy - side // 2))
    ui["faceBox"][cls] = [sx, sy, sx + side, sy + side]
    print(f"{cls}: face frame {ui['faceBox'][cls]} of the 256 overlay", flush=True)
json.dump(ui, open(UI_JSON, "w"), separators=(",", ":"))
print("written", os.path.join(OUT, "ui.json"))
