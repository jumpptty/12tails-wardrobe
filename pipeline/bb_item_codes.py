r"""Item code -> model from BB's readable source, to fix the wardrobe's icons (user 2026-11-05: "wrong icons are being
used all over the wardrobe, but correct model application"). wardrobe_icons.py read code -> model out of TTO's compiled
string switches (a hash tree followed with capstone); some codes came out shifted (Rabbit a_rab10 -> superStar, a_rab11
-> summer, a_rab12 -> standard, where BB's RabbitEquipment.cs says a_rab10 / 11 / 12 = Rabbit_standard with textures
standard<c>, standard<c>R, standard<c>V). The models were right (they go by name), the icons (by code) were not.

BB's DecompiledSource/<Class>Equipment.cs (and CharacterEquipment.cs for the shared items) is plain C#: a compare
`nArmor == "a_rab10"` (nWeapon / nAccessory / nTrinket) is followed by the Resources.Load of its model; armor codes also
load their texture (".../Materials/Rabbit_standard" + num + "R": the R / V edition). Negated compares (`!(x == "c")`)
are skipped. Codes BB doesn't have (TTO's new items) keep wardrobe_icons.py's mapping.

  py -3 -I bb_item_codes.py
  -> wardrobe/data/item_map.json (corrected; the TTO-traced one kept as item_map_tto.json), wardrobe/data/icons.json
     (rebuilt from the icons already in wardrobe/data/icons; outfits also get "editions": {R: icon})
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BIBLE = next((p for p in (r"D:\12tails", r"C:\Users\Jump\Desktop\12tails") if os.path.isdir(p + r"\DecompiledSource")), r"D:\12tails")
SRC = os.path.join(BIBLE, "DecompiledSource")
OUT = os.path.join(ROOT, "wardrobe", "data")
KIND = {"nArmor": "armor", "nWeapon": "weapon", "nAccessory": "accessory", "nTrinket": "trinket"}
TOKEN = re.compile(r'(!\()?\b(nArmor|nWeapon|nAccessory|nTrinket)\s*==\s*"([a-z]{1,2}_[a-z]+\d+[a-z0-9]*)"'
                   r'|Resources\.Load\("GameAssets/Characters/Heroes/(\w+)/(\w+)/(?:(Materials)/)?(\w+)"(?:\s*\+\s*\w+(?:\s*\+\s*"([A-Z])")?)?')


def parse(path, cls):
    """{kind: {code: [model, ...]}}, {armor code: edition}: each load goes to the compare just before it."""
    txt = open(path, encoding="utf-8", errors="replace").read()
    out, eds, cur = {}, {}, None
    for m in TOKEN.finditer(txt):
        if m.group(2):
            cur = None if m.group(1) else (KIND[m.group(2)], m.group(3))
            continue
        if not cur:
            continue
        kind, code = cur
        hero, folder, mat, name, ed = m.group(4), m.group(5), m.group(6), m.group(7), m.group(8)
        if kind == "armor":
            if mat:                                   # the texture: the edition
                eds.setdefault(code, ed or "")
            elif folder.lower() == "armors":
                lst = out.setdefault(kind, {}).setdefault(code, [])
                if name not in lst:
                    lst.append(name)
        elif not mat:
            model = name.lower() if cls == "all" else name
            lst = out.setdefault(kind, {}).setdefault(code, [])
            if model not in lst:
                lst.append(model)
        cur = cur if kind == "weapon" else None       # a weapon code may load two pieces (bow + arrow)
    # two pieces per code is the Chameleon's bow + arrow and the Whale's weapon + shield: there nearly every weapon code
    # loads two. Elsewhere a second load is the switch's default branch (Rabbit w_rab79 eclipseRifle + standardGun)
    w = out.get("weapon", {})
    if w and sum(len(v) > 1 for v in w.values()) < len(w) / 2:
        out["weapon"] = {c: v[:1] for c, v in w.items()}
    return out, eds


tto = json.load(open(os.path.join(OUT, "item_map_tto.json" if os.path.exists(os.path.join(OUT, "item_map_tto.json"))
                                   else "item_map.json")))
if not os.path.exists(os.path.join(OUT, "item_map_tto.json")):
    json.dump(tto, open(os.path.join(OUT, "item_map_tto.json"), "w"), indent=1)
fixed, editions, report = {}, {}, {}
for cls, kinds in tto.items():
    f = os.path.join(SRC, ("CharacterEquipment" if cls == "all" else cls.capitalize() + "Equipment") + ".cs")
    bb, eds = parse(f, cls) if os.path.exists(f) else ({}, {})
    editions[cls] = eds
    merged, diff = {}, 0
    for kind in set(kinds) | set(bb):
        m = dict(kinds.get(kind, {}))
        for code, models in bb.get(kind, {}).items():
            if m.get(code) != models:
                diff += 1
            m[code] = models
        merged[kind] = m
    fixed[cls] = merged
    report[cls] = (sum(len(v) for v in bb.values()), diff, sum(1 for e in eds.values() if e))
json.dump(fixed, open(os.path.join(OUT, "item_map.json"), "w"), indent=1)

# ---- icons.json, from the icons already extracted (wardrobe_icons.py) ----
have = {(f, os.path.splitext(n)[0]) for f in os.listdir(os.path.join(OUT, "icons"))
        if os.path.isdir(os.path.join(OUT, "icons", f)) for n in os.listdir(os.path.join(OUT, "icons", f))}
FOLDERS = {"weapon": ["weapon"], "armor": ["armor"], "accessory": ["accessory", "acessory"], "trinket": ["trinket"]}
SLOT = {"armor": "outfits", "weapon": "weapons", "accessory": "accessories", "trinket": "trinkets"}
index = {}
for cls, kinds in fixed.items():
    entry = {"outfits": {}, "weapons": {}, "accessories": {}, "trinkets": {}}
    for kind, codes in kinds.items():
        for code, models in sorted(codes.items(), key=lambda kv: (len(kv[0]), kv[0])):
            ed = editions[cls].get(code, "") if kind == "armor" else ""
            short = code.split("_", 1)[1]
            icon = next((f"icons/{f}/{short}.webp" for f in FOLDERS[kind] if (f, short) in have), None)
            for model in models:
                name = model.split("_", 1)[1] if kind == "armor" and model.lower().startswith(cls + "_") else model
                if cls == "all":
                    name = name.lower()
                e = entry[SLOT[kind]].setdefault(name, {"icon": None, "codes": []})
                e["codes"].append(code)
                if ed:                                # an R / V edition's own icon
                    e.setdefault("editions", {}).setdefault(ed, icon)
                elif not e["icon"]:
                    e["icon"] = icon
    for e in entry["outfits"].values():               # an outfit known only by its editions
        if not e["icon"] and e.get("editions"):
            e["icon"] = next(iter(e["editions"].values()))
    index[cls] = entry
json.dump(index, open(os.path.join(OUT, "icons.json"), "w"), separators=(",", ":"))
for cls, (n, diff, ne) in report.items():
    print(f"{cls}: BB codes {n}, changed from the TTO trace {diff}, armor editions {ne}")
