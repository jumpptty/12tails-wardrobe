r"""TTO's own equipment placements for the wardrobe (user 2026-11-04: shared wings sat turned 90 deg on the back).

  uv run --no-project --with UnityPy python wardrobe_placements.py
  -> tto_config/{Trinket,Accessory,Weapon}Placement.json (copies, read from the installed client; untracked, in this
     folder since the 2026-11-09 repo split, never in the video folder's tto_assets)
     wardrobe/data/placements.json = {trinkets|accessories|weapons: {hero: {entries: {code: P}, fallback: P}}}
     P = {bone, p, q, s, kwr, kps} in three.js space (p x -> -x; q from Unity Euler degrees, then (x, -y, -z, w))

TTO keeps per-hero, per-item-code placements as Resources TextAssets (built in, resources.assets, not the encrypted
bundles): Placements..cctor -> 'Config/TrinketPlacement', 'Config/AccessoryPlacement', 'Config/WeaponPlacement'
(TTO1102 0x1a85900), read by PlacementTable.EnsureLoaded with JsonUtility. PlacementData {heroes: [{hero, fallback,
entries: [{code, bone, pos, euler, scale, keepWorldRot, keepPrefabScale}]}]}; weapon heroes "<Hero>#2" = the second
hand (Placements.WeaponKey). CharacterEquipment.ApplyPlacement (0x1a748b0): parent to the bone (findChildObject; empty
= the character root), localPosition = pos, localRotation = Quaternion.Euler(euler) (degrees x 0.0174533 ->
Internal_FromEulerRad) unless keepWorldRot, then localScale. E.g. Sheep shade_wing t_all78: Spine2, pos (0, 0.25, 0),
euler 0 (the wardrobe had BB's class-trinket rule, Spine1 + Euler(0, -90, 90): 90 deg off). Items with no entry keep
BB's mount rule in the page.
"""
import json
import math
import os
import sys

import UnityPy

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = os.path.join(ROOT, "tto_config")
GAME = os.path.join(os.environ["LOCALAPPDATA"], "TailsTopia", "game", "TailsTopia", "TailsTopiaOnline_Data")
os.makedirs(CFG, exist_ok=True)

env = UnityPy.load(os.path.join(GAME, "resources.assets"))
for obj in env.objects:
    if obj.type.name == "TextAsset":
        t = obj.read()
        if t.m_Name in ("TrinketPlacement", "AccessoryPlacement", "WeaponPlacement"):
            s = t.m_Script if isinstance(t.m_Script, str) else t.m_Script.decode("utf-8", "replace")
            open(os.path.join(CFG, t.m_Name + ".json"), "w", encoding="utf-8").write(s)


def unity_euler(x, y, z):
    """Unity Quaternion.Euler (degrees): z, then x, then y -> (x, y, z, w)."""
    def axis(a, deg):
        h = math.radians(deg) / 2
        v = [0.0, 0.0, 0.0]
        v[a] = math.sin(h)
        return v + [math.cos(h)]

    def mul(p, q):
        px, py, pz, pw = p
        qx, qy, qz, qw = q
        return [pw * qx + px * qw + py * qz - pz * qy, pw * qy - px * qz + py * qw + pz * qx,
                pw * qz + px * qy - py * qx + pz * qw, pw * qw - px * qx - py * qy - pz * qz]
    return mul(mul(axis(1, y), axis(0, x)), axis(2, z))


def conv(e):
    q = unity_euler(e["euler"]["x"], e["euler"]["y"], e["euler"]["z"])
    return {"bone": e.get("bone") or "", "p": [-e["pos"]["x"], e["pos"]["y"], e["pos"]["z"]],
            "q": [round(q[0], 6), round(-q[1], 6), round(-q[2], 6), round(q[3], 6)], "s": e.get("scale", 1.0),
            "kwr": bool(e.get("keepWorldRot")), "kps": bool(e.get("keepPrefabScale"))}


out = {}
for slot, name in (("trinkets", "TrinketPlacement"), ("accessories", "AccessoryPlacement"), ("weapons", "WeaponPlacement")):
    d = json.load(open(os.path.join(CFG, name + ".json"), encoding="utf-8"))
    out[slot] = {h["hero"].lower(): {"fallback": conv(h["fallback"]) if h.get("fallback") else None,
                                     "entries": {e["code"]: conv(e) for e in h.get("entries", []) if e.get("code")}}
                 for h in d.get("heroes", [])}
    print(slot, {k: len(v["entries"]) for k, v in out[slot].items()})
json.dump(out, open(os.path.join(ROOT, "wardrobe", "data", "placements.json"), "w"), separators=(",", ":"))
print("written wardrobe/data/placements.json")
