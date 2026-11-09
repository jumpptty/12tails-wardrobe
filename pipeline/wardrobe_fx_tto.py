r"""TTO's skill effects for the wardrobe (2026-11-09; plans/fx_wolf/tto.md, build_rules.md agent E): the prefabs a class's
TTO-only skills spawn, read from TTO's decrypted client bundles (the video folder's tto_assets/<date>/dec + catalog.bin,
read only) with UnityPy, in the same JSON shape as pipeline/wardrobe_fx.py's BB effects. Why the bundles and not the rip
(tto.md 4.1): the catalog address is exactly what the game loads (gameassets/characters/heroes/<cls>/effects/<name>,
BaseHero::ArcanaLoad, TTO1102:Wolf::Row6Spawn@0x1F0F050), so the default style never gets mixed up with the Ronin arcana
copy (.../arcana/ronin/effects/<name>, which AssetRipper flattened into X / X_0 at random); and every object reads with a
full type tree (no byte layouts). The office PC has no TTO bundles: build at home (same limit as wardrobe_data.py).

  uv run --no-project --with UnityPy --with pillow --with imageio-ffmpeg python -I pipeline/wardrobe_fx_tto.py wolf
builds the class's TTO effects: SKILL_FX[cls] (every prefab its TTO skills spawn) plus every "tto/<prefab>" fx cue in
wardrobe/fx_cues/<cls>.json; --fx a,b builds those instead; --probe [a,b] prints the effects' JSON and writes nothing.
-> wardrobe/data/<cls>/fx.json: effects "tto/<prefab>" and materials "tto_<material>" merged in (every other entry kept),
   wardrobe/data/fx/tex/tto_<texture>.webp, wardrobe/data/<cls>/sfx/<clip>.mp3 (the AudioSources' clips: TTO's default
   clips are BB's own recordings, tto.md 4.3, so they come from BB's rip WAVs through wardrobe_fx.rip_wav)

Output, per node (as wardrobe_fx.effect): {name, parent, pos, rot (x, y, z, w), scale, comps, mats?, active?}, Unity's own
left-handed space (the page mirrors, tto.md 4.4). Components:
- the game's old emitters (EffectControl, ImageEmitter, RingEmitter, LineEmitter): exactly BB's fields and value shapes
  (wardrobe_fx.LAYOUTS: colours / vectors as lists, bools as booleans, a reference as [fileID, pathID]); checked field
  for field against LAYOUTS (TTO has BB's fields in BB's order, tto.md 3)
- TTO's own scripts (GroundHugEmitter, ArcRibbonEmitter, GroundFollower, ...): {"type": <script>, <serialized name>: value}
  with Color -> [r, g, b, a], Vector2/3/4 / Quaternion -> lists, bool fields (by the type tree) -> booleans, references
  resolved (see ref() below; GroundHugEmitter.motes -> {"node": i, "type": "ParticleSystem"})
- Unity components (ParticleSystem, ParticleSystemRenderer, MeshFilter, MeshRenderer, AudioSource, anything else): their
  read_typetree() dict minus m_GameObject, plus "type"; floats rounded to 6 places, +-inf -> +-1e30; references resolved
  (ref()); a ParticleSystem's disabled modules shrink to {"enabled": false}; AudioSource also carries BB's keys clip /
  volume / playOnAwake / loop (what the page plays); a renderer's first materials also go to the node's "mats" (the page
  hands mats[0] to the part)
"""
import argparse
import importlib.util
import json
import math
import os
import subprocess
import sys

import UnityPy

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "wardrobe", "data")
VIDEO = os.path.join(os.path.dirname(ROOT), "12tails-video")          # extracted inputs, read only (CLAUDE.md)
ASSETS = os.path.join(VIDEO, "tto_assets", "2026-11-04")
BIBLE = next((p for p in (r"D:\12tails", r"C:\Users\Jump\Desktop\12tails") if os.path.isdir(p)), r"D:\12tails")
AA_CATALOG = os.path.join(BIBLE, "DecompiledSource_TTO_2026-11-02", "tools", "aa_catalog.py")

# every prefab the class's TTO skills spawn, default style (tto.md section 0 and 2; the two the page cannot cue because
# they land on a hit enemy, resonanceClaw_burst and windBound, are built too)
SKILL_FX = {
    "wolf": [
        # Blade Surge: TTO1102:Wolf.<RPC_bladeSurge>d__317::MoveNext@0x1F1F640
        "bladeSurge_aura", "bladeSurge_zone", "bladeSurge_cut", "bladeSurge_flicker", "bladeSurge_sheathe",
        "bladeSurge_shatter", "bladeSurge_shards",
        # Resonance Claw: <RPC_resonanceClaw>d__329::MoveNext@0x1F3C1E0 (+ RPC_resonanceBurst@0x1F0DB20 on hit targets)
        "resonanceClaw_charge", "resonanceClaw_rake", "resonanceClaw_wave_twin", "resonanceClaw_wave_light",
        "resonanceClaw_wave_dark", "resonanceClaw_burst",
        # Wind Bound Domain: <RPC_windBoundDomain>d__313::MoveNext@0x1F51890 (+ CharacterControl::AddWindBoundFx@0x24AF350)
        "windBoundDomain_cast", "windBoundDomain_plant", "windBoundDomain_domain", "windBoundDomain_pulse", "windBound",
    ],
}
# Unity's built-in legacy particle shaders by name, to wardrobe_fx.BUILTIN_BLEND's words (the page's fxMaterial knows
# these); any other shader -> "shader:<name>"
SHADER_BLEND = {"Legacy Shaders/Particles/Additive": "add", "Legacy Shaders/Particles/Additive (Soft)": "addsoft",
                "Legacy Shaders/Particles/Alpha Blended": "alpha", "Legacy Shaders/Diffuse": "opaque"}
DROP = {"m_GameObject"}                          # dropped from every Unity component's dict
MESH_RENDERER_KEEP = {"type", "m_Enabled", "m_Materials", "m_SortingLayerID", "m_SortingLayer", "m_SortingOrder",
                      "m_RendererPriority"}
MB_HEADER = {"m_GameObject", "m_Enabled", "m_Script", "m_Name", "m_EditorHideFlags", "m_EditorClassIdentifier"}


def load_path(name, path):
    """A module by its path (python -I leaves the script's folder off sys.path)."""
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


_bb = None


def bb():
    """pipeline/wardrobe_fx.py (LAYOUTS, rip_wav, cue_lists); imported lazily: it needs nothing loaded at import time."""
    global _bb
    if _bb is None:
        _bb = load_path("wardrobe_fx", os.path.join(HERE, "wardrobe_fx.py"))
    return _bb


def num(x):
    """A JSON-safe float: 6 places, +-inf -> +-1e30 (wardrobe_data.py's convention), NaN -> None."""
    if math.isnan(x):
        return None
    if math.isinf(x):
        return 1e30 if x > 0 else -1e30
    return round(x, 6)


class Tto:
    """TTO's bundles for a set of effect addresses: the catalog resolves address -> internal id -> bundles (bundle names
    change every TTO build, so never by file name); each bundle's own AssetBundle m_Container is keyed by the internal id
    (env.container is empty for these, tto.md 4.1)."""

    def __init__(self, cls, names, assets=ASSETS, style=""):
        self.cls = cls
        cat = load_path("aa_catalog", AA_CATALOG).Catalog(os.path.join(assets, "catalog.bin"))
        base = f"gameassets/characters/heroes/{cls}/{style}effects/"
        want = {base + n.lower(): n for n in names}
        self.iid, deps = {}, set()                  # internal id -> prefab name
        for addr, loc in cat.entries():
            if addr in want:
                self.iid[loc["id"]] = want[addr]
                deps.update(loc["bundles"])
        missing = sorted(set(want.values()) - set(self.iid.values()))
        if missing:
            raise SystemExit(f"not in TTO's catalog under {base}: {missing}")
        self.env = UnityPy.load(*[os.path.join(assets, "dec", b) for b in sorted(deps)])
        self.sf = {}                                # serialized file name (lower case) -> file, to follow externals
        for f in self.env.files.values():
            self._collect(f, None)
        self.roots = {}                             # prefab name -> its root GameObject
        for o in self.env.objects:
            if o.type.name == "AssetBundle":
                for k, v in o.read_typetree()["m_Container"]:
                    if k in self.iid:
                        self.roots[self.iid[k]] = o.assets_file.objects[v["asset"]["m_PathID"]]
        self.scripts = {}

    def _collect(self, f, key):
        if type(f).__name__ == "BundleFile":
            for k, sub in f.files.items():
                self._collect(sub, k)
        elif hasattr(f, "objects") and hasattr(f, "externals") and isinstance(key, str):
            self.sf[os.path.basename(key).lower()] = f

    def deref(self, af, p):
        """The object a PPtr names, read against the file that holds the reference; None for a null one or a file not
        loaded (Unity's built-in resources)."""
        if not p or not p.get("m_PathID"):
            return None
        if p["m_FileID"] == 0:
            return af.objects.get(p["m_PathID"])
        f = self.sf.get(os.path.basename(af.externals[p["m_FileID"] - 1].path).lower())
        return f.objects.get(p["m_PathID"]) if f is not None else None

    def script(self, o, t):
        key = (o.assets_file.name, t["m_Script"]["m_FileID"], t["m_Script"]["m_PathID"])
        if key not in self.scripts:
            so = self.deref(o.assets_file, t["m_Script"])
            self.scripts[key] = so.read_typetree()["m_ClassName"] if so is not None else "?"
        return self.scripts[key]


class Build:
    """One run's collections: materials and textures (by object, so two different assets with one name never share an
    output name), sounds."""

    def __init__(self, tto):
        self.tto = tto
        self.mats = {}           # output name -> material dict
        self.texs = {}           # output name -> Texture2D object reader
        self.names = {}          # (type, file, pathID) -> output name (materials and textures named apart)
        self.sounds = set()

    def out_name(self, o, name):
        key = (o.type.name, o.assets_file.name, o.path_id)
        if key in self.names:
            return self.names[key], False
        used = {v for k, v in self.names.items() if k[0] == key[0]}
        n, i = name, 2
        while n in used:                          # a second asset with the same name: never overwrite the first
            n = f"{name}_{i}"; i += 1
        self.names[key] = n
        return n, True

    def texture(self, o):
        n, new = self.out_name(o, "tto_" + o.read_typetree()["m_Name"])
        if new:
            self.texs[n] = o
        return n

    def material(self, o):
        t = o.read_typetree()
        n, new = self.out_name(o, "tto_" + t["m_Name"])
        if not new:
            return n
        sh = self.tto.deref(o.assets_file, t["m_Shader"])
        shn = sh.read_typetree().get("m_ParsedForm", {}).get("m_Name", "?") if sh is not None else "?"
        props = t["m_SavedProperties"]
        tex, scale, offset = None, [1, 1], [0, 0]
        for k, v in props["m_TexEnvs"]:
            if k == "_MainTex":
                to = self.tto.deref(o.assets_file, v["m_Texture"])
                if to is not None:
                    tex = self.texture(to)
                scale = [num(v["m_Scale"]["x"]), num(v["m_Scale"]["y"])]
                offset = [num(v["m_Offset"]["x"]), num(v["m_Offset"]["y"])]
        colors = {k: [num(v[c]) for c in "rgba"] for k, v in props["m_Colors"]}
        self.mats[n] = {"blend": SHADER_BLEND.get(shn, "shader:" + shn), "tex": tex, "scale": scale, "offset": offset,
                        "tint": colors.get("_TintColor"), "color": colors.get("_Color")}
        return n


def bool_fields(o):
    """The names of a MonoBehaviour's top-level bool fields, by its type tree (UnityPy reads them as 0 / 1). TTO's type
    trees write a C# bool as UInt8 (EffectControl's followPosition, m_Enabled); the new scripts' only UInt8 fields are
    bools in TTO's dump.cs (ArcRibbonEmitter.flat :11465, GroundHugEmitter.repeatForever :11671), none is a byte."""
    node = getattr(getattr(o, "serialized_type", None), "node", None)
    return {c.m_Name for c in getattr(node, "m_Children", []) if c.m_Type in ("bool", "UInt8")}


def effect(tto, b, name):
    root = tto.roots[name]
    af = root.assets_file
    # pass 1: every GameObject in the walk's order (depth first, children in order), so a reference to a component or
    # GameObject inside the prefab can name its node before that node is built
    order, where = [], {}                    # where: pathID of a GameObject or component -> (node index, type)
    stack = [(root, -1)]
    while stack:
        go, parent = stack.pop()
        idx = len(order); order.append((go, parent))
        t = go.read_typetree()
        where[go.path_id] = (idx, "GameObject")
        kids = []
        for c in t["m_Component"]:
            co = tto.deref(af, c["component"])
            if co is None:
                continue
            where[co.path_id] = (idx, co.type.name)
            if co.type.name == "Transform":
                kids = [tto.deref(af, tto.deref(af, ch).read_typetree()["m_GameObject"]) for ch in co.read_typetree()["m_Children"]]
        stack.extend((k, idx) for k in reversed(kids))

    def ref(holder, p):
        """A reference: null -> None; inside the prefab -> {"node": i, "type": component type} ({"node": i} for a
        GameObject); Material -> its "tto_" name (exported); Texture2D / Sprite -> its "tto_" texture name (exported);
        AudioClip -> its name (exported to sfx); anything else -> {"asset": type, "name": m_Name}."""
        if not p.get("m_PathID"):
            return None
        if p["m_FileID"] == 0 and p["m_PathID"] in where and holder.assets_file is af:
            i, ty = where[p["m_PathID"]]
            return {"node": i} if ty == "GameObject" else {"node": i, "type": ty}
        o = tto.deref(holder.assets_file, p)
        if o is None:
            return {"asset": "?", "file": p["m_FileID"], "pathID": p["m_PathID"]}
        ty = o.type.name
        if ty == "Material":
            return b.material(o)
        if ty == "Texture2D":
            return b.texture(o)
        if ty == "Sprite":
            to = tto.deref(o.assets_file, o.read_typetree()["m_RD"]["texture"])
            return b.texture(to) if to is not None else None
        if ty == "AudioClip":
            n = o.read_typetree()["m_Name"]
            b.sounds.add(n)
            return n
        # not exported (a Mesh: none of the Wolf's TTO effects names one, every MeshFilter's m_Mesh is null, the
        # scripts build their meshes at run time); say so, so the next class's run shows what needs writing
        n = o.read_typetree().get("m_Name")
        print(f"warning: {name}: a {ty} reference ({n}) is written by name only, not exported", file=sys.stderr)
        return {"asset": ty, "name": n}

    def safe(holder, v):
        """A Unity component's type-tree value, JSON-safe, references resolved."""
        if isinstance(v, dict):
            if set(v) == {"m_FileID", "m_PathID"}:
                return ref(holder, v)
            return {k: safe(holder, x) for k, x in v.items()}
        if isinstance(v, (list, tuple)):
            return [safe(holder, x) for x in v]
        if isinstance(v, float):
            return num(v)
        if isinstance(v, bytes):
            return v.hex()
        return v

    def field(holder, v, is_bool):
        """A script field, in wardrobe_fx's shapes: Color -> [r, g, b, a], vectors -> lists, bools -> booleans."""
        if is_bool:
            return bool(v)
        if isinstance(v, dict):
            ks = set(v)
            if ks == {"r", "g", "b", "a"}:
                return [num(v[c]) for c in "rgba"]
            for shape in ("xy", "xyz", "xyzw"):
                if ks == set(shape):
                    return [num(v[c]) for c in shape]
        return safe(holder, v)

    layouts = bb().LAYOUTS
    nodes = []
    for idx, (go_obj, parent) in enumerate(order):
        go = go_obj.read_typetree()
        node = {"name": go["m_Name"], "parent": parent, "comps": []}
        if not go.get("m_IsActive", 1):
            node["active"] = False                 # an inactive GameObject: not drawn by the game (the page ignores it)
        nodes.append(node)
        for c in go["m_Component"]:
            co = tto.deref(af, c["component"])
            if co is None:
                continue
            ty = co.type.name
            t = co.read_typetree()
            if ty == "Transform":
                p, r, s = t["m_LocalPosition"], t["m_LocalRotation"], t["m_LocalScale"]
                node["pos"] = [round(p[k], 5) for k in "xyz"]
                node["rot"] = [round(r[k], 6) for k in "xyzw"]
                node["scale"] = [round(s[k], 5) for k in "xyz"]
                continue
            if ty == "MonoBehaviour":
                sname = tto.script(co, t)
                entry = {"type": sname}
                fields = {k: v for k, v in t.items() if k not in MB_HEADER}
                lay = layouts.get(sname)
                if lay is not None and sname in ("EffectControl", "ImageEmitter", "RingEmitter", "LineEmitter"):
                    # the old emitters: BB's shapes exactly (the page draws these already); TTO kept BB's fields
                    if list(fields) != [n for n, _ in lay]:
                        raise ValueError(f"{name}/{node['name']}: TTO's {sname} fields {list(fields)} differ from "
                                         f"wardrobe_fx.LAYOUTS {[n for n, _ in lay]}")
                    for n, kind in lay:
                        v = fields[n]
                        if kind == "b":
                            entry[n] = bool(v)
                        elif kind == "r":
                            entry[n] = [v["m_FileID"], v["m_PathID"]]
                        elif kind in ("f",):
                            entry[n] = round(v, 5)
                        elif kind == "i":
                            entry[n] = v
                        else:
                            entry[n] = [round(v[k], 5) for k in ("rgba" if kind == "c" else "xyzw"[:len(v)])]
                else:
                    bools = bool_fields(co)
                    for n, v in fields.items():
                        entry[n] = field(co, v, n in bools)
                if not t.get("m_Enabled", 1):
                    entry["enabled"] = False
                node["comps"].append(entry)
                continue
            entry = {"type": ty, **{k: safe(co, v) for k, v in t.items() if k not in DROP}}
            if ty == "ParticleSystem":             # a disabled module's settings are never read by Unity: kept out
                for k, v in list(entry.items()):
                    if isinstance(v, dict) and v.get("enabled") in (False, 0) and k.endswith("Module"):
                        entry[k] = {"enabled": False}
            elif ty == "MeshRenderer":             # only what drawing reads: the rest (1 KB each, 76 in the Wolf's) is
                # shadow / light-probe / lightmap / ray-tracing plumbing, which the unlit particle shaders never read
                entry = {k: v for k, v in entry.items() if k in MESH_RENDERER_KEEP}
            elif ty == "AudioSource":              # + what the page plays (wardrobe_fx's AudioSource shape)
                clip = entry.get("m_Resource") or entry.get("m_audioClip")
                entry.update({"clip": clip, "volume": num(t.get("m_Volume", 1)),
                              "playOnAwake": bool(t.get("m_PlayOnAwake", 1)), "loop": bool(t.get("Loop", 0))})
            if "m_Materials" in entry and ty.endswith("Renderer") and "mats" not in node:
                node["mats"] = list(entry["m_Materials"])
            node["comps"].append(entry)
    return {"nodes": nodes}


def cue_tto(cls):
    """The "tto/<prefab>" names the class's fx cues use ("a|b" = both), without the prefix."""
    path = os.path.join(ROOT, "wardrobe", "fx_cues", cls + ".json")
    if not os.path.exists(path):
        return []
    out = []
    for entry in json.load(open(path, encoding="utf-8")).values():
        for cues in bb().cue_lists(entry):
            for cue in cues:
                if cue[1] == "fx":
                    for n in str(cue[2]).split("|"):
                        if n.startswith("tto/") and n[4:] not in out:
                            out.append(n[4:])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cls")
    ap.add_argument("--fx", default="", help="prefabs to build instead of SKILL_FX[cls] + the cue file's tto/ names")
    ap.add_argument("--probe", nargs="?", const="*", default="", help="print the effects (all, or these) as JSON; writes nothing")
    ap.add_argument("--assets", default=ASSETS, help="TTO's tto_assets/<date> folder (dec/ + catalog.bin)")
    a = ap.parse_args()
    if a.fx:
        names = [n.removeprefix("tto/") for n in a.fx.split(",") if n]
    elif a.probe and a.probe != "*":
        names = [n.removeprefix("tto/") for n in a.probe.split(",") if n]
    else:
        names = list(dict.fromkeys(SKILL_FX.get(a.cls, []) + cue_tto(a.cls)))
    if not names:
        ap.error(f"no TTO effects for {a.cls}: add SKILL_FX['{a.cls}'], tto/ cues, or pass --fx")
    tto = Tto(a.cls, names, a.assets)
    b = Build(tto)
    effects = {"tto/" + n: effect(tto, b, n) for n in names}
    if a.probe:
        print(json.dumps({"effects": effects, "materials": b.mats, "textures": sorted(b.texs), "sounds": sorted(b.sounds)}, indent=1))
        return
    tdir = os.path.join(DATA, "fx", "tex"); os.makedirs(tdir, exist_ok=True)
    for n, o in b.texs.items():
        o.read().image.save(os.path.join(tdir, n + ".webp"), "WEBP", quality=90, method=6)
    # sounds: BB's rip WAV of the same name (TTO's default clips are BB's recordings to the millisecond, tto.md 4.3),
    # 64 kbps mono mp3 as wardrobe_fx.py writes them
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    sdir = os.path.join(DATA, a.cls, "sfx"); os.makedirs(sdir, exist_ok=True)
    missing = []
    for n in sorted(b.sounds):
        src = bb().rip_wav(a.cls, n)
        if not src:
            missing.append(n); continue
        subprocess.run([ff, "-y", "-loglevel", "error", "-i", src, "-ac", "1", "-b:a", "64k", os.path.join(sdir, n + ".mp3")], check=True)
    out = os.path.join(DATA, a.cls, "fx.json")
    old = json.load(open(out, encoding="utf-8")) if os.path.exists(out) else {}
    merged = {**old, "effects": {**old.get("effects", {}), **effects}, "materials": {**old.get("materials", {}), **b.mats}}
    json.dump(merged, open(out, "w", encoding="utf-8"), indent=1)
    print(f"{a.cls}: {len(effects)} TTO effects, {len(b.mats)} materials, {len(b.texs)} textures, "
          f"{len(b.sounds) - len(missing)} sounds" + (f", missing sounds: {missing}" if missing else ""))


if __name__ == "__main__":
    main()
