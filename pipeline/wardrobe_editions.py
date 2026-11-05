r"""Recolour editions of the outfits for the wardrobe (user 2026-11-05: "the R and V variants didn't get the texture
colour change, only the hat"). BB ships <Class>_<armor><colour>R / V.png beside the 5 base colours (Sheep cleric R,
holyRobe R + V, standard R + V ...): the outfit of a set's R / V edition. wardrobe_data.py packed only the base colours;
this copies the editions from the BB rip to wardrobe/data/<cls>/tex/<armor><colour><E>.webp and lists them in each
outfits.json entry as "editions". (wardrobe_data.py packs them too from now on, from the TTO bundles.)

  uv run --no-project --with pillow python -I wardrobe_editions.py
"""
import json
import os
import re

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIBLE = next((p for p in (r"D:\12tails", r"C:\Users\Jump\Desktop\12tails") if os.path.isdir(p + r"\RippedAssets")), r"D:\12tails")
HEROES = BIBLE + r"\RippedAssets\ExportedProject\Assets\Resources\gameassets\characters\heroes"
DATA = os.path.join(ROOT, "wardrobe", "data")

total = 0
for cls in sorted(os.listdir(DATA)):
    oj = os.path.join(DATA, cls, "outfits.json")
    mats = os.path.join(HEROES, cls, "armors", "materials")
    if not (os.path.exists(oj) and os.path.isdir(mats)):
        continue
    outfits = json.load(open(oj, encoding="utf-8"))
    files = {f.lower(): f for f in os.listdir(mats)}
    cap = cls.capitalize()
    n = 0
    for o in outfits:
        eds = {}
        for c in o["colors"]:
            for e in "RV":
                f = files.get(f"{cap}_{o['name']}{c}{e}.png".lower())
                if f:
                    try:
                        im = Image.open(os.path.join(mats, f)).convert("RGBA")
                    except OSError as ex:          # the rip has a few broken files (Monkey_spider4R.png)
                        print(f"  skipped {f}: {ex}")
                        continue
                    im.save(os.path.join(DATA, cls, "tex", f"{o['name']}{c}{e}.webp"), "WEBP", quality=90, method=4)
                    eds.setdefault(e, []).append(c)
                    n += 1
        if eds:
            o["editions"] = {e: sorted(cs) for e, cs in sorted(eds.items())}   # edition -> the colours it has
    json.dump(outfits, open(oj, "w"))
    print(f"{cls}: {n} edition textures, outfits {[o['name'] + '+' + ''.join(o['editions']) for o in outfits if o.get('editions')]}")
    total += n
print("total", total)
