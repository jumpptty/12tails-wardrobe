r"""Weapons' own effects (user 2026-11-12: "Can you add particle effects for weapons too?"): the flames, sparkles and
trails a BB weapon prefab carries beside its mesh, read from BB's own data the way pipeline/wardrobe_fx.py reads a skill
effect (its Game / effect / material: the prefab by its Resources path, gameassets/characters/heroes/<cls>/weapons/<name>;
the game loads weapons from there, e.g. BatEquipment.cs Resources.Load(".../Bat/Weapons/japanWagasa")).

  uv run --no-project --with UnityPy --with pillow python -I pipeline/wardrobe_weapon_fx.py [cls ...]
-> wardrobe/data/<cls>/weapon_fx.json {"effects": {<weapon name>: {nodes}}, "materials": {...}} (a file of its own:
   wardrobe_fx.py rewrites fx.json's effects and materials only), wardrobe/data/fx/tex/<texture>.webp (shared)

Kept per weapon: the nodes from the root to every node with an effect component (Unity 3.5's legacy particles, the
game's TrailEmitter, the built-in TrailRenderer, any of the game's emitter scripts), their transforms in Unity's space
(the page builds them inside a mirror group, as a skill effect, following the worn prop's root every frame). Dropped:
the weapon's own mesh, its material and texture (the prop draws it), its Animation (the prop plays it).
Unity 3.5's Shuriken (ParticleSystem; the time weapons, 15): wardrobe_fx.py does not decode it, so those weapons are
read whole from TTO's client copy instead (pipeline/wardrobe_fx_tto.py's Tto / effect with folder "weapons": TTO holds
BB's weapons at gameassets/characters/heroes/<cls>/weapons/<name>; its ParticleSystem as wardrobe/fxparts/shuriken.js
reads it; materials and textures named tto_*, as every TTO-read effect's). Which weapons: the BB rip's prefab has a
ParticleSystem (class 198).
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("wardrobe_fx", os.path.join(HERE, "wardrobe_fx.py"))
W = importlib.util.module_from_spec(spec)
spec.loader.exec_module(W)

RIP_WEAPONS = os.path.join(W.BIBLE, r"RippedAssets\ExportedProject\Assets\Resources\gameassets\characters\heroes")
spec_t = importlib.util.spec_from_file_location("wardrobe_fx_tto", os.path.join(HERE, "wardrobe_fx_tto.py"))
T = importlib.util.module_from_spec(spec_t)
spec_t.loader.exec_module(T)
CLASSES = ["bat", "bison", "cat", "chameleon", "mole", "monkey", "panda", "penguin", "rabbit", "sheep", "whale", "wolf"]
MESH = {"StaticMesh", "SkinnedMeshRenderer", "Animation"}      # the prop's own: drawn and played by the page's props
FX = {"EllipsoidParticleEmitter", "TrailEmitter", "TrailRenderer", "RingEmitter", "ImageEmitter", "LineEmitter",
      "BoltEmitter", "EmblemEmitter"}


def weapon(game, cls, name, mats, texs):
    """One weapon's effect nodes, or None when it has none."""
    e = W.effect(game, cls, name, mats, texs, set())
    nodes = e["nodes"]
    keep = [False] * len(nodes)
    for i, n in enumerate(nodes):
        n["comps"] = [c for c in n["comps"] if c["type"] not in MESH]
        if any(c["type"] in FX for c in n["comps"]):
            k = i
            while k >= 0 and not keep[k]:
                keep[k] = True
                k = nodes[k]["parent"]
    if not any(keep[1:]) and not (keep[0] and any(c["type"] in FX for c in nodes[0]["comps"])):
        return None
    remap, out = {}, []
    for i, n in enumerate(nodes):
        if not keep[i]:
            continue
        remap[i] = len(out)
        n = dict(n, parent=remap.get(n["parent"], -1))
        if not any(c["type"] in FX for c in n["comps"]):
            n.pop("mats", None)                        # a plain node (the root: the weapon's mesh material)
            n["comps"] = [c for c in n["comps"] if c["type"] != "ParticleRenderer"]
        out.append(n)
    return {"nodes": out}


def shuriken_weapons(cls):
    """The class's BB weapons whose prefab (the rip's YAML) holds a Unity ParticleSystem, by the prefab's name."""
    d = os.path.join(RIP_WEAPONS, cls, "weapons")
    out = []
    for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        if f.endswith(".prefab") and "--- !u!198 " in open(os.path.join(d, f), encoding="utf-8", errors="ignore").read():
            out.append(f[:-len(".prefab")])
    return out


def tto_weapons(cls, names, effects, mats, tdir):
    """names read whole from TTO's client copy (their Shuriken), replacing BB's partial read in effects."""
    tto = T.Tto(cls, names, folder="weapons")
    b = T.Build(tto)
    for n in names:
        e = T.effect(tto, b, n)
        drop = MESH | {"MeshFilter", "MeshRenderer", "SkinnedMeshRenderer"}
        for node in e["nodes"]:
            if any(c["type"] in ("MeshFilter", "MeshRenderer", "StaticMesh") for c in node["comps"]):
                node.pop("mats", None)                # the weapon's own material (the prop draws it)
            node["comps"] = [c for c in node["comps"] if c["type"] not in drop]
        effects[n] = e
    used = {m for e in (effects[n] for n in names) for nd in e["nodes"] for m in (nd.get("mats") or [])}
    used |= {m for e in (effects[n] for n in names) for nd in e["nodes"] for c in nd["comps"] for m in (c.get("mats") or []) if isinstance(m, str)}
    for k, v in b.mats.items():
        if k in used:
            mats[k] = v
    for k, o in b.texs.items():
        if any(m.get("tex") == k for m in mats.values()) and not os.path.exists(os.path.join(tdir, k + ".webp")):
            o.read().image.save(os.path.join(tdir, k + ".webp"), "WEBP", quality=90, method=6)


def main():
    classes = sys.argv[1:] or CLASSES
    game = W.Game()
    tdir = os.path.join(W.DATA, "fx", "tex")
    os.makedirs(tdir, exist_ok=True)
    for cls in classes:
        W.EXTRA_FOLDERS[cls] = W.EXTRA_FOLDERS.get(cls, []) + [f"gameassets/characters/heroes/{cls}/weapons"]
        prefix = f"gameassets/characters/heroes/{cls}/weapons/"
        mats, texs, effects, failed = {}, {}, {}, []
        for key in sorted(k for k in game.container if k.startswith(prefix) and "/" not in k[len(prefix):]):
            try:
                root = game.obj(game.container[key], game.files["mainData"])
                name = root.read_typetree()["m_Name"]             # the prefab's own spelling (the container is lower case)
                got = weapon(game, cls, name, mats, texs)
            except Exception as ex:                                # noqa: BLE001 (a script with no layout: say so, go on)
                failed.append(f"{key[len(prefix):]}: {type(ex).__name__}: {ex}")
                continue
            if got:
                effects[name] = got
        sh = shuriken_weapons(cls)
        if sh:
            try:
                tto_mats = {}
                tto_weapons(cls, sh, effects, tto_mats, tdir)
            except SystemExit as ex:                               # not in TTO's catalog: say so, keep BB's read
                failed.append(f"TTO copy: {ex}")
                tto_mats = {}
        else:
            tto_mats = {}
        used = {m for e in effects.values() for n in e["nodes"] for m in n.get("mats", []) or []}
        used |= {m for e in effects.values() for n in e["nodes"] for c in n["comps"] for m in c.get("mats", []) or []}
        mats = {**{k: v for k, v in mats.items() if k in used}, **tto_mats}
        wanted = {m["tex"] for m in mats.values() if m.get("tex")}
        for n, o in texs.items():
            if n in wanted and not os.path.exists(os.path.join(tdir, n + ".webp")):
                o.read().image.save(os.path.join(tdir, n + ".webp"), "WEBP", quality=90, method=6)
        out = os.path.join(W.DATA, cls, "weapon_fx.json")
        if effects:
            json.dump({"effects": effects, "materials": mats}, open(out, "w", encoding="utf-8"), separators=(",", ":"))
        elif os.path.exists(out):
            os.remove(out)
        print(f"{cls}: {len(effects)} weapons with effects {sorted(effects)}" + (f"; failed: {failed}" if failed else ""), flush=True)


if __name__ == "__main__":
    main()
