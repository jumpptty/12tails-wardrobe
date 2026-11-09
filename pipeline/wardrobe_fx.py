r"""Skill effects (VFX) and skill sounds for the wardrobe, read from BB's own data (2026-11-09 pilot; user: "let's try
wolf cross break, armor break, and grand cross"). Why not the rip: AssetRipper kept every effect's hierarchy, materials
and Unity's legacy particles, but the game's own emitter scripts (RingEmitter, ImageEmitter, LineEmitter, EffectControl)
come out as a bare m_Script: their settings are only in 12TailsOnline_Data/resources.assets, as raw bytes in the fields'
declaration order (the file's type tree stops at MonoBehaviour's header). So: mainData's ResourceManager maps the
Resources path to the prefab in resources.assets; GameObject / Transform / renderers / legacy particles / AudioSource /
Material read through the type tree; MonoBehaviour fields decoded with LAYOUTS, and every decode must use up exactly
the object's bytes (the self-check); the script's name from its MonoScript in sharedassets0.assets.

Kept in Unity's space (left-handed): the page builds each effect inside a group scaled (-1, 1, 1), the same mirror as
wardrobe_data.py's x -> -x, so positions, rotations and emitter vectors need no conversion here.

  uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py wolf
builds every effect and voice the class's cue file names (wardrobe/fx_cues/<cls>.json, the page's cues: "fx" and
"voice" cues, "a|b" = both); --fx a,b [--voices c,d] builds those instead (probing a skill before its cues are written).
-> wardrobe/data/<cls>/fx.json (effects, materials, which sound each plays), wardrobe/data/fx/tex/<texture>.webp,
   wardrobe/data/<cls>/sfx/<sound>.mp3 (64 kbps mono: plays in every browser)
"""
import argparse
import io
import json
import os
import struct
import subprocess

import UnityPy

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "wardrobe", "data")
BIBLE = next((p for p in (r"D:\12tails", r"C:\Users\Jump\Desktop\12tails") if os.path.isdir(p + r"\12TailsOnline_Data")), r"D:\12tails")
GAME = os.path.join(BIBLE, "12TailsOnline_Data")
RIP = os.path.join(BIBLE, r"RippedAssets\ExportedProject\Assets\Resources\gameassets")
# Unity 3.5's built-in shaders by their id in "unity default resources": the Particle shader files in alphabetical order
# from 200 (Add, AddMultiply, AddSmooth, Alpha Blend ...), which the materials bear out (2026-11-09, 1,200 of them):
# every 200 material saves a _TintColor (Additive has one), 202's mostly don't (Additive (Soft) has none) and its
# textures are 75% alpha-less on black, 203's carry alpha 97% of the time (Alpha Blended); 7 = Diffuse
BUILTIN_BLEND = {200: "add", 202: "addsoft", 203: "alpha", 7: "opaque"}

# serialized fields of the game's scripts, in declaration order: (name, type); f float, i int, b bool (1 byte, then
# aligned to 4), v2 / v3 / c (Color) / q, r (a reference: fileID + pathID, 8 bytes in Unity 3.5)
LAYOUTS = {
    "RingEmitter": [("Life", "f"), ("Delay", "f"), ("Emission", "f"), ("EmissionPeriod", "f"), ("startRadius", "f"),
                    ("endRadius", "f"), ("rndRadius", "f"), ("startHeight", "f"), ("endHeight", "f"), ("rndHeight", "f"),
                    ("startWidth", "f"), ("endWidth", "f"), ("rndWidth", "f"), ("localVelocity", "v3"), ("rndVelocity", "v3"),
                    ("Color1", "c"), ("Color2", "c"), ("Color3", "c"), ("Color4", "c"), ("Color5", "c"),
                    ("localRotation", "v3"), ("uvRotation", "f"), ("ringTri", "i"), ("uvTile", "f"),
                    ("repeatForever", "b"), ("qualitySetting", "i")],
    # EffectControl.cs:549-564 (32 bytes: each bool in its own 4 bytes; effectRotationMode 0 normal, 1 followObject,
    # 2 faceCamera, 3 faceUp, 4 freeze)
    "EffectControl": [("life", "f"), ("afterLife", "f"), ("followPosition", "b"), ("followState", "b"),
                      ("effectRotationMode", "i"), ("velocity", "v3")],
    # ImageEmitter.cs:1275-1366 (188 bytes; ImageEmitterMode 0 FaceCamera, 1 Horizontal, 2 Vertical, 3 LocalRotation)
    "ImageEmitter": [("Emission", "i"), ("EmissionTime", "f"), ("Life", "f"), ("Delay", "f"), ("startHeight", "f"),
                     ("endHeight", "f"), ("startWidth", "f"), ("endWidth", "f"), ("rndScale", "f"), ("rndLife", "f"),
                     ("startPosition", "v3"), ("localVelocity", "f"), ("rndVelocity", "f"), ("worldVelocity", "v3"),
                     ("ImageEmitterMode", "i"), ("useWorldSpace", "b"), ("Color1", "c"), ("Color2", "c"), ("Color3", "c"),
                     ("Color4", "c"), ("Color5", "c"), ("Rotation", "f"), ("rndRotation", "f"), ("startAngle", "f"),
                     ("spreadAngle", "f"), ("repeatForever", "b"), ("mMeshFilter", "r")],
    # LineEmitter.cs:1433-1502 (180 bytes; lineEmitterMode 0 directional, 1 alwaysUp, 2 alwaysHorizontal, 3 faceCamera,
    # 4 localUp; symetry is never read)
    "LineEmitter": [("Life", "f"), ("Delay", "f"), ("Emission", "f"), ("EmissionTime", "f"), ("startRadius", "f"),
                    ("endRadius", "f"), ("rndRadius", "f"), ("startHeight", "f"), ("endHeight", "f"), ("rndHeight", "f"),
                    ("startWidth", "f"), ("endWidth", "f"), ("rndWidth", "f"), ("localVelocity", "v3"), ("rndVelocity", "v3"),
                    ("Color1", "c"), ("Color2", "c"), ("Color3", "c"), ("Color4", "c"), ("Color5", "c"),
                    ("lineEmitterMode", "i"), ("symetry", "b"), ("localRotation", "v3"), ("repeatForever", "b")],
}
SIZES = {"f": 4, "i": 4, "v2": 8, "v3": 12, "c": 16, "q": 16, "r": 8}


def decode(raw, layout, off):
    """The fields after the MonoBehaviour header; raises when the layout doesn't use up exactly the object's bytes."""
    out = {}
    for name, ty in layout:
        if ty == "b":
            out[name] = bool(raw[off]); off = (off + 4) & ~3
        elif ty == "i":
            out[name] = struct.unpack_from("<i", raw, off)[0]; off += 4
        elif ty == "r":
            out[name] = list(struct.unpack_from("<ii", raw, off)); off += 8
        else:
            n = SIZES[ty] // 4
            v = struct.unpack_from(f"<{n}f", raw, off); off += 4 * n
            out[name] = v[0] if n == 1 else [round(x, 5) for x in v]
    if off != len(raw):
        raise ValueError(f"layout used {off} of {len(raw)} bytes")
    return {k: round(v, 5) if isinstance(v, float) else v for k, v in out.items()}


def header_len(raw):
    """m_GameObject (8) + m_Enabled (4) + m_Script (8) + m_Name (int length + bytes, aligned to 4)."""
    n = struct.unpack_from("<i", raw, 20)[0]
    return 24 + ((n + 3) & ~3)


class Game:
    def __init__(self):
        self.env = UnityPy.load(*(os.path.join(GAME, f) for f in ("mainData", "resources.assets", "sharedassets0.assets")))
        self.files = {os.path.basename(k): f for k, f in self.env.files.items()}
        self.ra = self.files["resources.assets"]
        md = self.files["mainData"]
        rm = next(o for o in md.objects.values() if o.type.name == "ResourceManager").read_typetree()
        self.container = {k: v for k, v in rm["m_Container"]}
        self.scripts = {}

    def obj(self, pptr, base=None):
        """The object a PPtr names, read against the file that holds the reference (fileID 0 = that file; each file
        numbers its externals its own way); a sharedassets file is loaded the first time it is named. None when the
        file isn't in the game folder (Unity's built-in resources)."""
        base = base or self.ra
        fid, pid = (pptr["m_FileID"], pptr["m_PathID"]) if isinstance(pptr, dict) else pptr
        if fid == 0:
            return base.objects.get(pid)
        name = os.path.basename(base.externals[fid - 1].path)
        if name not in self.files and os.path.exists(os.path.join(GAME, name)):
            env = UnityPy.load(os.path.join(GAME, name))
            self.files.update({os.path.basename(k): f for k, f in env.files.items()})
        f = self.files.get(name)
        return f.objects.get(pid) if f else None

    def script_name(self, raw, base=None):
        """The MonoBehaviour's script, its PPtr read against the file holding the component (base; resources.assets by
        default; Mole megapunch_hit's are in another file, 2026-11-09)."""
        base = base or self.ra
        fid, pid = struct.unpack_from("<ii", raw, 12)
        key = (base.name, fid, pid)
        if key not in self.scripts:
            o = self.obj((fid, pid), base)
            self.scripts[key] = o.read_typetree()["m_ClassName"] if o is not None and o.type.name == "MonoScript" else f"?{fid}:{pid}"
        return self.scripts[key]


def material(game, pptr, base, mats, texs):
    o = game.obj(pptr, base)
    if o is None:
        return None
    t = o.read_typetree()
    name = t["m_Name"]
    if name in mats:
        return name
    sh, own = t["m_Shader"], o.assets_file
    if sh["m_FileID"] and "default resources" in own.externals[sh["m_FileID"] - 1].path:
        blend = BUILTIN_BLEND.get(sh["m_PathID"], "add")
    else:                                             # the game's own shader: named in its source's first line
        so = game.obj(sh, own)
        src = so.read_typetree().get("m_Script", "") if so else ""
        blend = "shader:" + (src.split('"')[1] if src.count('"') >= 2 else "?")
    props = t["m_SavedProperties"]
    tex = None; scale = [1, 1]; offset = [0, 0]
    key = lambda k: k["name"] if isinstance(k, dict) else k     # Unity 3.5: FastPropertyName {name}
    for k, v in props["m_TexEnvs"]:
        if key(k) == "_MainTex":
            to = game.obj(v["m_Texture"], own)
            if to is not None:
                tex = to.read().m_Name
                if tex not in texs:
                    texs[tex] = to
            scale = [v["m_Scale"]["x"], v["m_Scale"]["y"]]; offset = [v["m_Offset"]["x"], v["m_Offset"]["y"]]
    colors = {key(k): [v["r"], v["g"], v["b"], v["a"]] for k, v in props["m_Colors"]}
    mats[name] = {"blend": blend, "tex": tex, "scale": scale, "offset": offset,
                  "tint": colors.get("_TintColor"), "color": colors.get("_Color")}
    return name


def effect(game, cls, name, mats, texs, sounds):
    key = f"gameassets/characters/heroes/{cls}/effects/{name.lower()}"
    root = game.obj(game.container[key], game.files["mainData"])
    nodes = []

    def walk(go_obj, parent):
        go = go_obj.read_typetree()
        node = {"name": go["m_Name"], "parent": parent, "comps": []}
        idx = len(nodes); nodes.append(node)
        tr_children = []
        for comp in go["m_Component"]:                 # Unity 3.5: (classID, reference) pairs
            c = game.obj(comp[1] if isinstance(comp, (list, tuple)) else comp.get("second", comp.get("component")), go_obj.assets_file)
            if c is None:
                continue
            ty = c.type.name
            if ty == "Transform":
                t = c.read_typetree()
                p, r, s = t["m_LocalPosition"], t["m_LocalRotation"], t["m_LocalScale"]
                node["pos"] = [round(p["x"], 5), round(p["y"], 5), round(p["z"], 5)]
                node["rot"] = [round(r["x"], 6), round(r["y"], 6), round(r["z"], 6), round(r["w"], 6)]
                node["scale"] = [round(s["x"], 5), round(s["y"], 5), round(s["z"], 5)]
                tr_children = t["m_Children"]
            elif ty == "MonoBehaviour":
                raw = c.get_raw_data()
                sname = game.script_name(raw, c.assets_file)
                lay = LAYOUTS.get(sname)
                entry = {"type": sname}
                if lay is not None:
                    entry.update(decode(raw, lay, header_len(raw)))
                elif len(raw) > header_len(raw):
                    raise ValueError(f"{name}/{node['name']}: no layout for {sname} ({len(raw) - header_len(raw)} field bytes)")
                node["comps"].append(entry)
            elif ty in ("MeshRenderer", "ParticleRenderer"):
                t = c.read_typetree()
                node["mats"] = [material(game, m, c.assets_file, mats, texs) for m in t["m_Materials"]]
                if ty == "ParticleRenderer":
                    node["comps"].append({"type": ty, **{k: v for k, v in t.items() if not k.startswith("m_") or k in ("m_StretchParticles", "m_LengthScale", "m_VelocityScale", "m_MaxParticleSize", "m_CameraVelocityScale", "UV Animation")}})
            elif ty in ("EllipsoidParticleEmitter", "ParticleAnimator"):
                t = c.read_typetree()
                node["comps"].append({"type": ty, **{k: v for k, v in t.items() if k not in ("m_GameObject", "m_Enabled")}})
            elif ty == "AudioSource":
                t = c.read_typetree()
                clip = game.obj(t["m_audioClip"], c.assets_file)
                if clip is not None:
                    sn = clip.read().m_Name
                    sounds.add(sn)
                    node["comps"].append({"type": "AudioSource", "clip": sn, "volume": t.get("m_Volume", 1),
                                          "playOnAwake": bool(t.get("m_PlayOnAwake", 1)), "loop": bool(t.get("Loop", 0))})
        for ch in tr_children:
            tro = game.obj(ch, go_obj.assets_file)
            if tro is not None:
                walk(game.obj(tro.read_typetree()["m_GameObject"], tro.assets_file), idx)

    walk(root, -1)
    return {"nodes": nodes}


def rip_wav(cls, name, folder=None):
    """The rip's WAV: from the class's voices/ or sounds/ when the cue says which (they share names: crusader1, nAttack1
    ... are different recordings in each, 2026-11-09), else sounds/ then voices/ then anywhere (an effect's own sound)."""
    if folder:
        p = os.path.join(RIP, "characters", "heroes", cls, folder, name + ".wav")
        return p if os.path.exists(p) else None
    for sub in (f"characters/heroes/{cls}/sounds", f"characters/heroes/{cls}/voices"):
        p = os.path.join(RIP, *sub.split("/"), name + ".wav")
        if os.path.exists(p):
            return p
    # an effect's sound kept elsewhere: anywhere under gameassets, then anywhere under Resources (Blade Fang's ring plays
    # Resources/sound/fx/aura1.wav, 2026-11-09)
    for top in (RIP, os.path.dirname(RIP)):
        for root, _, fs in os.walk(top):
            if name + ".wav" in fs:
                return os.path.join(root, name + ".wav")
    return None


def cue_lists(entry):
    """An entry's cue lists: its cues, or every skill's of a shared clip ({skills: {name: {cues}}})."""
    return [entry.get("cues", [])] + [s.get("cues", []) for s in entry.get("skills", {}).values()]


def cue_names(cls):
    """The effects, voices and sounds the class's cue file names, as --fx / --voices / --sounds strings (in cue order, no
    repeats; "a|b" = both)."""
    path = os.path.join(os.path.dirname(DATA), "fx_cues", cls + ".json")
    names = {"fx": [], "voice": [], "sound": []}
    for entry in json.load(open(path, encoding="utf-8")).values():
        for cues in cue_lists(entry):
            for cue in cues:
                for n in str(cue[2]).split("|"):
                    if n not in names[cue[1]]:
                        names[cue[1]].append(n)
    return ",".join(names["fx"]), ",".join(names["voice"]), ",".join(names["sound"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cls")
    ap.add_argument("--fx", default="", help="effects to build instead of the cue file's")
    ap.add_argument("--voices", default="", help="Voices/ clips -> sfx/v_<name>.mp3")
    ap.add_argument("--sounds", default="", help="Sounds/ clips the hero's code plays -> sfx/<name>.mp3")
    ap.add_argument("--probe", default="", help="print these effects' nodes and components as JSON; writes nothing")
    a = ap.parse_args()
    if a.probe:                          # read only (the research agents' ask: --fx writes the shared data)
        game = Game()
        for n in a.probe.split(","):
            try:
                print(json.dumps({n: effect(game, a.cls, n, {}, {}, set())}, indent=1))
            except Exception as e:      # noqa: BLE001 (a script with no layout yet: say so, go on)
                print(json.dumps({n: f"{type(e).__name__}: {e}"}))
        return
    if not a.fx:
        a.fx, a.voices, a.sounds = cue_names(a.cls)
        if not a.fx and not a.voices and not a.sounds:
            ap.error(f"wardrobe/fx_cues/{a.cls}.json has no cues; write them first, or pass --fx")
    game = Game()
    mats, texs, sounds, effects = {}, {}, set(), {}
    for n in [n for n in a.fx.split(",") if n]:
        effects[n] = effect(game, a.cls, n, mats, texs, sounds)
    voices = [v for v in a.voices.split(",") if v]
    hero_sounds = [v for v in a.sounds.split(",") if v]
    # textures -> data/fx/tex (shared by every class), sounds -> data/<cls>/sfx
    tdir = os.path.join(DATA, "fx", "tex"); os.makedirs(tdir, exist_ok=True)
    for n, o in texs.items():
        o.read().image.save(os.path.join(tdir, n + ".webp"), "WEBP", quality=90, method=6)
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    sdir = os.path.join(DATA, a.cls, "sfx"); os.makedirs(sdir, exist_ok=True)
    missing, jobs = [], []
    # an effect's own sound and a Sounds/ cue: <name>.mp3 (from sounds/ first); a voice: v_<name>.mp3 from voices/ only
    jobs += [(n, rip_wav(a.cls, n), n) for n in sorted(sounds)]
    jobs += [(n, rip_wav(a.cls, n, "sounds"), n) for n in sorted(set(hero_sounds) - sounds)]
    jobs += [(n, rip_wav(a.cls, n, "voices"), "v_" + n) for n in sorted(set(voices))]
    for n, src, out_name in jobs:
        if not src:
            missing.append(out_name); continue
        subprocess.run([ff, "-y", "-loglevel", "error", "-i", src, "-ac", "1", "-b:a", "64k", os.path.join(sdir, out_name + ".mp3")], check=True)
    out = os.path.join(DATA, a.cls, "fx.json")
    old = json.load(open(out, encoding="utf-8")) if os.path.exists(out) else {}
    merged = {"effects": {**old.get("effects", {}), **effects}, "materials": {**old.get("materials", {}), **mats}}
    json.dump(merged, open(out, "w", encoding="utf-8"), indent=1)
    print(f"{a.cls}: {len(effects)} effects, {len(mats)} materials, {len(texs)} textures, {len(jobs) - len(missing)} sounds"
          + (f", missing sounds: {missing}" if missing else ""))


if __name__ == "__main__":
    main()
