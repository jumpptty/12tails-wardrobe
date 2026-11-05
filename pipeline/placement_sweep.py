r"""Sweep: how TTO places every wearable item on every class (user 2026-11-04: "quick sweep of every wearable item if
they have specific positions and rotations specific to each class, checked against the code").

  python placement_sweep.py   -> wardrobe/data/placement_sweep.md (+ a summary on stdout)

The rule is TTO's code (TTO1102 CharacterEquipment.PlaceTrinket 0x1a7a020, PlaceAccessory 0x1a79f00, PlaceWeapon
0x1a7a390): PlacementTable.Get(hero, code) -> else GetFallback(hero) -> ApplyPlacement; weapons look up "<Hero>#2" for
the second hand; Game.IsSpecialTrinket = the code is empty. Here: an item's codes come from icons.json (the code ->
model switches), the entries / fallbacks from placements.json (wardrobe_placements.py). Code-less wings of the
public_wing family (Devil, Champion) borrow Shade Wing's entry (t_all78), as the page does; marked "inferred".
"""
import collections
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "wardrobe", "data")
PL = json.load(open(os.path.join(D, "placements.json")))
IC = json.load(open(os.path.join(D, "icons.json")))
CLASSES = ["bat", "bison", "cat", "chameleon", "mole", "monkey", "panda", "penguin", "rabbit", "sheep", "whale", "wolf"]
KINDS = [("trinkets", "trinkets", "trinkets"), ("accessories", "accessories", "accessories"), ("weapons", "weapons", "weapons")]


def codes_of(cls, slot, name):
    e = IC.get(cls, {}).get(slot, {}).get(name) or IC.get(cls, {}).get(slot, {}).get(re.sub(r"_[LRlr]$", "", name)) \
        or IC.get("all", {}).get(slot, {}).get(name.lower())
    return e["codes"] if e else []


def euler_of(q):                     # for the report only: the quaternion back to readable degrees is not needed
    return "rot" if any(abs(x) > 1e-6 for x in q[:3]) else "no rot"


rows, summary, odd = [], collections.Counter(), []
for cls in CLASSES:
    for kind, slot, table in KINDS:
        props = []
        for src in (cls, "all"):
            p = os.path.join(D, src, f"props_{kind}.json")
            if os.path.exists(p) and (src == cls or kind != "weapons"):
                props += json.load(open(p))
        key = cls
        T = PL[table].get(key, {})
        for pr in props:
            if not pr.get("nodes"):
                continue
            codes = codes_of(cls, slot, pr["name"])
            e = next((T.get("entries", {}).get(c) for c in codes if c in T.get("entries", {})), None)
            how = "entry"
            if not e and not codes and any(re.match(r"^public_wing_\d+$", n["name"]) for n in pr["nodes"]):
                e, how = T.get("entries", {}).get("t_all78"), "inferred (Shade Wing's entry)"
                odd.append(f"{cls} {kind} {pr['name']}: no code, Shade Wing's entry")
            if not e:
                e, how = T.get("fallback"), "class fallback" if codes else "class fallback (no code)"
            summary[(cls, kind, how.split(" (")[0])] += 1
            rows.append((cls, kind, pr["name"], ",".join(codes[:3]) + ("..." if len(codes) > 3 else ""), how,
                         (e or {}).get("bone", "-") or "ROOT", ",".join(f"{x:g}" for x in (e or {}).get("p", [])),
                         (e or {}).get("s", "-")))

out = ["# Wearable placement sweep (TTO rules, per class)", "",
       "Rule (TTO1102 code): the class + item-code entry, else the class fallback; weapons' second hand is `<Class>#2`.",
       "Source: `wardrobe/data/placements.json` (TTO's Config/*Placement tables) + `icons.json` (code -> model).", "",
       "## Summary (items per class: entry / class fallback / inferred)", "",
       "| class | trinkets | headpieces | weapons |", "|---|---|---|---|"]
for cls in CLASSES:
    cell = lambda k: " / ".join(str(summary[(cls, k, h)]) for h in ("entry", "class fallback", "inferred"))
    out.append(f"| {cls} | {cell('trinkets')} | {cell('accessories')} | {cell('weapons')} |")
out += ["", "## Every item", "", "| class | kind | item | codes | placed by | bone | pos | scale |", "|---|---|---|---|---|---|---|---|"]
out += [f"| {' | '.join(str(x) for x in r)} |" for r in rows]
open(os.path.join(D, "placement_sweep.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out[7:7 + len(CLASSES) + 2]))
print("inferred:", odd[:6], len(odd))
print("written", os.path.join(D, "placement_sweep.md"), len(rows), "rows")
