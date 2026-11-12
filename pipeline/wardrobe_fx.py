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
"voice" cues, "a|b" = both; and an entry's "builds", the effects and sounds a page part spawns that no cue names,
2026-11-13); --fx a,b [--voices c,d] builds those instead (probing a skill before its cues are written).
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
# textures are 75% alpha-less on black, 203's carry alpha 97% of the time (Alpha Blended); 7 = Diffuse. The same rule one
# step on (plans/fx_penguin/parts.md "Read this first" 4, 2026-11-10; medium sure, the ids are not in the game files):
# 205 = Particles/Multiply (its 24 materials in the rip are BlackTrail, ShadowLine1-4, Smoke4_multiply ...: dark on white),
# so 206 = Particles/Multiply (Double) (15 materials: the Penguin's fallingComet1 and giantComet comet bodies) and 207 =
# Particles/Alpha Blended Premultiply (13: every class's <cls>_dead, netherBane, fireWall). The page draws them in
# fxMaterial (wardrobe/index.html: "multiply2", "premul"). 205 = "multiply" since 2026-11-13 (the Bat's shadow effects:
# ShadowRay, ShadowLine1 / 3, Smoke4_multiply, nightmare_bolt, darkStalker ...; plans/fx_bat/decisions.md 40, parts.md
# part 9: drawn by wardrobe/fxparts/particles.js through api.shader; before, they fell back to "add" and glowed where the
# game darkens). An unknown id still falls back to "add". 205 / 206 / 207 are CERTAIN since 2026-11-13 (plans/fx_cat/
# parts.md "Read this first" 4, decisions.md 56): TTO re-serialised BB's prefabs with Unity's own shader names
# (checks/fx_cat_research/parts/tto_bbcopies.json, tto_probe.json): ShadowLine2 (205) = Legacy Shaders/Particles/Multiply,
# Bomb2 (206; rip Material/Bomb2_0.mat m_Shader fileID 206) = Legacy Shaders/Particles/Multiply (Double), cat_dead (207) =
# Legacy Shaders/Particles/Alpha Blended Premultiply
BUILTIN_BLEND = {200: "add", 202: "addsoft", 203: "alpha", 7: "opaque", 205: "multiply", 206: "multiply2", 207: "premul"}

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
# the Wolf's other effect parts (plans/fx_wolf/parts.md, 2026-11-09): every instance in the 12 classes decodes and uses up
# exactly its bytes (VortexEmitter 164 / 31, EmblemEmitter 68 / 24, TrailEmitter 124 / 22, EmitterControl 12 / 32,
# ShatterMesh 56 / 5)
LAYOUTS.update({
    "EmitterControl": [("Delay", "f"), ("Life", "f"), ("AfterLife", "f")],          # EmitterControl.cs:175-181
    "VortexEmitter": [("Life", "f"), ("Delay", "f"), ("startRadius", "f"), ("endRadius", "f"), ("rndRadius", "f"),
                      ("startWidth", "f"), ("endWidth", "f"), ("length", "i"), ("alwaysUp", "b"), ("localVelocity", "v3"),
                      ("Color1", "c"), ("Color2", "c"), ("Color3", "c"), ("Color4", "c"), ("Color5", "c"),
                      ("Rotation", "f"), ("vortexCount", "i"), ("vortexRadian", "f"), ("Spin", "v3"),
                      ("VortexEmitterMode", "i"), ("UVTile", "f"), ("repeatForever", "b")],
    "EmblemEmitter": [("Life", "f"), ("Delay", "f"), ("image", "r"), ("startHeight", "f"), ("endHeight", "f"),
                      ("startWidth", "f"), ("endWidth", "f"), ("rndScale", "f"), ("velocity", "v3"), ("alpha1", "f"),
                      ("alpha2", "f"), ("alpha3", "f"), ("alpha4", "f"), ("alpha5", "f")],
    "TrailEmitter": [("startWidth", "f"), ("endWidth", "f"), ("life", "f"), ("alwaysUp", "b"), ("minDistance", "f"),
                     ("Color1", "c"), ("Color2", "c"), ("Color3", "c"), ("Color4", "c"), ("TrailEmitterMode", "i"),
                     ("uvHeight", "f"), ("localVelocity", "f"), ("worldVelocity", "f"), ("isTimer", "b"), ("delay", "f"),
                     ("easeIn", "f"), ("easeMiddle", "f"), ("easeOut", "f"), ("minQuality", "i")],
    "ShatterMesh": [("Life", "f"), ("Delay", "f"), ("worldVelocity", "v3"), ("localVelocity", "v3"),
                    ("rndVelocity", "v3"), ("rndRotation", "v3")],
})
# the Sheep's parts (plans/fx_sheep/parts.md, 2026-11-10): every AlphaTimer (56) and ProjectileControl (20) in the 12
# classes and the Sheep's 4 Sheep_seal decode and use up exactly their bytes; the Sheep's movers and Eden Sanctuary keep
# every field private (0 field bytes: the empty layout makes the self-check say so)
LAYOUTS.update({
    # AlphaTimer.cs:378-402 (36 bytes): fades its own renderer's _Color, else _TintColor (wardrobe/fxparts/alphatimer.js)
    "AlphaTimer": [("MinAlpha", "f"), ("MaxAlpha", "f"), ("FadeDelay", "f"), ("FadeEaseIn", "f"), ("FadeMiddle", "f"),
                   ("FadeEaseOut", "f"), ("eraseShadow", "b"), ("repeat", "b"), ("endDestroy", "b")],
    # ProjectileControl.cs:72-87 (32 bytes): data only; life is the hero code's (Sheep.cs:9343, :11472, :9838), not this
    "ProjectileControl": [("life", "f"), ("dmg", "f"), ("velocity", "v3"), ("OwnerID", "i"), ("isInitialized", "b"),
                          ("isDestroyed", "b")],
    "Sheep_seal": [("mSealType", "i")],             # Sheep_seal.cs:348 (0 attack, 1 defense, 2 earth, 3 heaven)
    "Sheep_nAttack": [], "Sheep_homingLight": [], "Sheep_cAttack": [], "Sheep_edenSanctuary": [],
})
# the Penguin's parts (plans/fx_penguin/parts.md, 2026-11-10; proved by --probe on this PC's BB data, read only,
# checks/fx_penguin_build/page_pipeline/layouts.txt): every Penguin_tornado / _typhoon (3 each), the arcticEmperor and the
# iceBlock decode and use up exactly their bytes; the other Penguin scripts keep every field private (0 field bytes)
LAYOUTS.update({
    # Penguin_tornado.cs:605, :635, :638 / Penguin_typhoon.cs:515, :557, :560 (28 bytes): mLv = the hit radius (m) and
    # the steering force 11 - mLv; nPosition / nVelocity = the owner's network copy (0 in the prefab)
    "Penguin_tornado": [("mLv", "i"), ("nPosition", "v3"), ("nVelocity", "v3")],
    "Penguin_typhoon": [("mLv", "i"), ("nPosition", "v3"), ("nVelocity", "v3")],
    # Penguin_arcticEmperor.cs:225-246 (32 bytes): AlphaTimer's fade on _TintColor.a plus a second one on _Emission.a
    "Penguin_arcticEmperor": [("MinAlpha", "f"), ("MaxAlpha", "f"), ("MinEmission", "f"), ("MaxEmission", "f"),
                              ("FadeDelay", "f"), ("FadeEaseIn", "f"), ("FadeMiddle", "f"), ("FadeEaseOut", "f")],
    "Penguin_iceBlock": [("mLife", "i"), ("mLv", "i")],     # Penguin_iceBlock.cs:264, :267 (8 bytes); Init overwrites both
    "Penguin_cosmicFriday": [], "Penguin_nAttack": [], "Penguin_manaMissile": [], "Penguin_snowMan": [],
})
# the Mana Vortex summon (Resources characters/elementals/manavortex/ManaVortex, Penguin.cs:10421; plans/fx_penguin/cast_a.md
# "Read this first" 2; checks/fx_penguin_build/page_pipeline/vortex.txt): its BoltEmitter (BoltEmitter.cs:499-553, 152
# bytes: the lightning from the node to TargetObject, drawn by the page's boltEmitter) and ManaVortex (ManaVortex.cs:540-549,
# 28 bytes: data only; the page's ManaVortex part plays its create / root clips)
LAYOUTS.update({
    "BoltEmitter": [("TargetPosition", "v3"), ("TargetObject", "r"), ("TargetCollider", "r"), ("Height", "f"),
                    ("StartWidth", "f"), ("EndWidth", "f"), ("Width1", "f"), ("Width2", "f"), ("Width3", "f"),
                    ("Width4", "f"), ("Width5", "f"), ("rndWidth", "f"), ("rndZigg", "f"), ("Color1", "c"), ("Color2", "c"),
                    ("Color3", "c"), ("Color4", "c"), ("Color5", "c"), ("BoltCount", "i")],
    "ManaVortex": [("novaFlare", "r"), ("mCreator", "r"), ("mCreatorChar", "r"), ("isSummon", "b")],
})
# the Bat's parts (plans/fx_bat/parts.md, 2026-11-13; checks/fx_bat_research/parts/probe.txt: each instance's bytes are
# the listed fields exactly; Bat_nAttack / Bat_illusionFire keep every field private)
LAYOUTS.update({
    "Bat_echoes": [("mTarget", "r"), ("mEchoesLv", "i")],                       # Bat_echoes.cs:577, :580 (12 bytes)
    "Bat_mirageOrb": [("isVisible", "b")],                                       # Bat_mirageOrb.cs:408 (4; Init sets it)
    "Bat_guardianOfTheNight": [("guardianBlade", "r"), ("castEffect", "r")],     # Bat_guardianOfTheNight.cs:169, :175 (16)
    # Bat_illusion.cs:2894-2945 (80 bytes): references only (the clone copies the hero, part 6)
    "Bat_illusion": [("mChar", "r"), ("Weapon", "r"), ("nAttack_fire", "r"), ("nAttack_hit", "r"), ("Bat_drainLife", "r"),
                     ("Bat_drainLife_charge", "r"), ("cAttack_hit", "r"), ("castEffect_illusion", "r"),
                     ("castRing_illusion", "r"), ("illusion_dust", "r")],
    "Bat_nAttack": [], "Bat_illusionFire": [],
    # AudioControl.cs:233-248 (24 bytes; Bat nefariousWhip_hit, and one effect each of Mole, Monkey, Panda, Whale)
    "AudioControl": [("minVolume", "f"), ("maxVolume", "f"), ("delay", "f"), ("fadein", "f"), ("middle", "f"),
                     ("fadeout", "f")],
})
# the Bison's parts (plans/fx_bison/parts.md, 2026-11-13, decisions.md 36, 39; checks/fx_bison_research/parts/probe.txt:
# UVScroll's three instances are its two floats exactly, (0.2, -0.2); Bison_earthRupture / Bison_overLord keep every
# field private)
LAYOUTS.update({
    "UVScroll": [("scroll_x", "f"), ("scroll_y", "f")],   # UVScroll.cs:67, :70 (8 bytes; Bison 2, Cat 1, Whale 1)
    "Bison_earthRupture": [],                             # Bison_earthRupture.cs:218-228: all private (the mover, fxparts/bison.js)
    "Bison_overLord": [],                                 # Bison_overLord.cs:206-215: all private (an aura trigger: draws nothing)
})
# the Cat's parts (plans/fx_cat/parts.md, 2026-11-13, decisions.md 49, 50; checks/fx_cat_research/parts/probe.txt: each
# instance's bytes are the listed fields exactly; UVScroll is the Bison's line above, deltaStrike_tri's (1, 1); StatusControl
# keeps every field private, 0 bytes, so it needs no entry)
LAYOUTS.update({
    "Cat_grandCasinoArcade": [("mRenderer", "r")],        # Cat_grandCasinoArcade.cs:144 (8 bytes: its own SMR; fxparts/cat.js)
    "Cat_supportFire": [("mVelocity", "v3")],             # Cat_supportFire.cs:240 (12 bytes; (0, 0, 30): fxparts/cat.js)
})
# BB effects whose Unity 3.5 Shuriken (ParticleSystem + ParticleSystemRenderer) this file does not decode, grafted from
# TTO's client copy of the same prefab (2026-11-13, plans/fx_bison/decisions.md 40, parts.md part 5): magmaClutter_ring2's
# TrailEmitter node carries the swing's puffs; TTO's copy has them decoded but loses the node's Animation `cleave` (the
# swing), so BB's effect stays (its TrailEmitter keeps ["ExplosionRay"] and the swing) and TTO's two components go on a new
# child of that node at local identity. Their material: SHURIKEN_MAT, BB's own of the same shader (TTO's tto_Bomb2 is
# Legacy Shaders/Particles/Multiply (Double); BB's Bomb2 is built-in 206 = multiply2, read from the BB effect named
# beside it), so no TTO texture ships and fxparts/shuriken.js reads it as any node's mats[0]
# The Cat's supportFire_hit (2026-11-13, plans/fx_cat/decisions.md 54, parts.md part 6): its node "ParticleSystem" is a
# Unity 3.5 Shuriken only (12 puffs at 0 in a 25 deg cone); TTO's re-serialised copy matches BB's values field for field
# (checks/fx_cat_research/parts/tto_probe.json, ps_sum.txt), so it is grafted the same way, its material BB's Bomb2 (206,
# multiply2) read from supportFire_hit's own Shuriken renderer (bb_material: effect() skips a ParticleSystemRenderer)
SHURIKEN_FROM_TTO = {"bison": ["magmaClutter_ring2"], "cat": ["supportFire_hit"]}
SHURIKEN_MAT = {"bison": ("Bomb2", "magmaClutter_ring1"),   # (BB material, a BB effect of the class that has it)
                "cat": ("Bomb2", "supportFire_hit")}
# a summon's gameplay scripts, kept by name only (no layout: CharacterControl's 684 bytes are the character's stats and
# state, nothing an effect draws)
NOT_DRAWN = {"CharacterControl"}
# effects the hero's code takes from another folder than heroes/<cls>/effects (tried in this order after it): Nova Flare's
# blast is the Mana Vortex's field (ManaVortex.cs:540, Resources characters/elementals/manavortex/effects/novaFlare;
# plans/fx_penguin/own_skills.md "Read this first" 1); the Mana Vortex summon itself (the cue name manaVortex)
EXTRA_FOLDERS = {"penguin": ["gameassets/characters/elementals/manavortex/effects", "gameassets/characters/elementals/manavortex"]}
# an effect the page names otherwise than its prefab, because the class's own folder has a prefab of that name too: the
# name -> its Resources container path, tried before the class's folder (2026-11-13, plans/fx_bat/parts.md Interfaces 6:
# Guardian of the Night's hits are Shade4's Effects/nAttack_hit, Bat.cs:12606-12619, not the Bat's own nAttack_hit)
# (2026-11-13, plans/fx_cat/decisions.md 55, skills_a.md part 3: Casino Doom's doom is the Bat's effect, the status look
# CharacterControl.cs:40491 loads from heroes/bat/effects whoever holds it; one effect, not the whole Bat folder)
ALIASES = {"bat": {"guardian_hit": "gameassets/characters/elementals/shade4/effects/nattack_hit"},
           "cat": {"doom": "gameassets/characters/heroes/bat/effects/doom"}}
# the same for a sound (rip_wav): the name -> its WAV under the rip's gameassets, without ".wav" (the guardian's swing is
# Shade4's Sounds/nAttack, Bat_guardianOfTheNight.cs:1047; the Bat's own sounds/nAttack.wav would win by name)
SOUND_ALIASES = {"bat": {"guardian_nAttack": "characters/elementals/shade4/sounds/nAttack"}}
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


_mesh = None


def mesh_module():
    """pipeline/wardrobe_fx_mesh.py, loaded by its path (python -I leaves the script's folder off sys.path)."""
    global _mesh
    if _mesh is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location("wardrobe_fx_mesh", os.path.join(HERE, "wardrobe_fx_mesh.py"))
        _mesh = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_mesh)
    return _mesh


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
                  "tint": colors.get("_TintColor"), "color": colors.get("_Color"),
                  # FX/Phoenix's Emission [_Emission] (rip Assets/Resources/gameassets/shader/Phoenix.shader; fxparts/mesh.js),
                  # Transparent/AdditiveSaturate's pass-2 glow too (AdditiveSaturate.shader:27-43)
                  "emission": colors.get("_Emission")}
    # DiffuseAmbient's Ambient [_Ambient] (rip shader/diffuseambient.shader:1-19; the Penguin's snowMan), only when saved
    # (no other material has it: the other materials' data stays as it was)
    if colors.get("_Ambient") is not None:
        mats[name]["ambient"] = colors["_Ambient"]
    # Transparent/AdditiveAlpha's _AdditiveRange (2026-11-13, plans/fx_cat/parts.md part 3, decisions.md 52; rip
    # shader/AdditiveAlpha.shader:1-34: pass 1 lit with alpha test >= it, pass 2 additive with <= it; default 0.9) as
    # "cut", as wardrobe_data.py:281-297 does for the props (the Cat's supportFire_fire ball, PirateCannon_Fire 0.9; the
    # Mole's napalm / nAttack later; wardrobe/fxparts/additivealpha.js)
    if blend == "shader:Transparent/AdditiveAlpha":
        floats = {key(k): v for k, v in props.get("m_Floats", [])}
        mats[name]["cut"] = round(float(floats.get("_AdditiveRange", 0.9)), 4)
    return name


def effect(game, cls, name, mats, texs, sounds):
    key = ALIASES.get(cls, {}).get(name, f"gameassets/characters/heroes/{cls}/effects/{name.lower()}")
    if key not in game.container:                    # another folder the class's code loads it from (EXTRA_FOLDERS)
        key = next((k for k in (f"{f}/{name.lower()}" for f in EXTRA_FOLDERS.get(cls, [])) if k in game.container), key)
    root = game.obj(game.container[key], game.files["mainData"])
    nodes, at = [], {}                                # at: (file, GameObject pathID) -> node index (a script's GameObject reference)

    def walk(go_obj, parent):
        go = go_obj.read_typetree()
        node = {"name": go["m_Name"], "parent": parent, "comps": []}
        idx = len(nodes); nodes.append(node)
        at[(go_obj.assets_file.name, go_obj.path_id)] = idx
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
                    if sname == "BoltEmitter":             # its TargetObject: a node of this prefab (BoltTarget), by index
                        ref = game.obj(entry["TargetObject"], c.assets_file) if entry["TargetObject"][1] else None
                        refs.append((entry, ref))
                elif sname in NOT_DRAWN:
                    pass
                elif len(raw) > header_len(raw):
                    raise ValueError(f"{name}/{node['name']}: no layout for {sname} ({len(raw) - header_len(raw)} field bytes)")
                if sname == "EmblemEmitter":           # its picture: a Texture2D reference, exported like a material's
                    to = game.obj(entry["image"], c.assets_file)
                    if to is not None:
                        img = to.read()
                        entry["imageTex"] = img.m_Name
                        entry["imageSize"] = [img.m_Width, img.m_Height]   # the emblem's pixel size (fxparts/emblem.js)
                        texs.setdefault(entry["imageTex"], to)
                node["comps"].append(entry)
            elif ty in ("MeshRenderer", "ParticleRenderer"):
                t = c.read_typetree()
                node["mats"] = [material(game, m, c.assets_file, mats, texs) for m in t["m_Materials"]]
                if ty == "ParticleRenderer":
                    node["comps"].append({"type": ty, **{k: v for k, v in t.items() if not k.startswith("m_") or k in ("m_StretchParticles", "m_LengthScale", "m_VelocityScale", "m_MaxParticleSize", "m_CameraVelocityScale", "UV Animation")}})
            # Unity built-ins: their fields as stored (+ a trail's materials); WorldParticleCollider since 2026-11-13
            # (plans/fx_cat/parts.md part 5, decisions.md 53: the Cat's luckyDice / treasureHunt legacy particles bounce on
            # the floor: m_BounceFactor, m_CollisionEnergyLoss, m_CollidesWith {m_Bits}, m_SendCollisionMessage,
            # m_MinKillVelocity; wardrobe/fxparts/worldcollider.js)
            elif ty in ("TrailRenderer", "Light", "WorldParticleCollider"):
                t = c.read_typetree()
                entry = {"type": ty, **{k: v for k, v in t.items() if k not in ("m_GameObject", "m_Materials")}}
                if "m_Materials" in t:
                    entry["mats"] = [material(game, m, c.assets_file, mats, texs) for m in t["m_Materials"]]
                node["comps"].append(json.loads(json.dumps(entry, default=str)))
            elif ty in ("MeshFilter", "SkinnedMeshRenderer", "Animation"):
                # meshes and legacy animations: pipeline/wardrobe_fx_mesh.py (its own file, so the mesh work stays apart)
                got = mesh_module().component(game, c, ty, node, {"cls": cls, "effect": name, "mats": mats, "texs": texs,
                                                                     "sounds": sounds, "material": material})
                if got:
                    node["comps"].extend(got)
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

    refs = []
    walk(root, -1)
    for entry, ref in refs:                           # resolved once every node is known (the target may come later)
        entry["TargetNode"] = at.get((ref.assets_file.name, ref.path_id), -1) if ref is not None else -1
    return {"nodes": nodes}


def node_paths(nodes):
    """Each node's name path below the root ("" for the root, "magmaClutter_cleave/TrailEmitter" ...)."""
    out = []
    for n in nodes:
        out.append("" if n["parent"] < 0 else (out[n["parent"]] + "/" if out[n["parent"]] else "") + n["name"])
    return out


def bb_material(game, cls, name, want, mats, texs):
    """BB's material `want` from any renderer under the BB effect `name` whose m_Materials lists it, a Unity 3.5
    ParticleSystemRenderer too (effect() skips that component; 2026-11-13, the Cat's supportFire_hit, whose only renderer
    is its Shuriken's, material Bomb2), through material() into mats / texs; nothing when no renderer has it."""
    key = ALIASES.get(cls, {}).get(name, f"gameassets/characters/heroes/{cls}/effects/{name.lower()}")
    todo = [game.obj(game.container[key], game.files["mainData"])]
    while todo:
        go_obj = todo.pop()
        for comp in go_obj.read_typetree()["m_Component"]:
            c = game.obj(comp[1] if isinstance(comp, (list, tuple)) else comp.get("second", comp.get("component")), go_obj.assets_file)
            if c is None:
                continue
            if c.type.name == "Transform":
                for ch in c.read_typetree()["m_Children"]:
                    tro = game.obj(ch, go_obj.assets_file)
                    if tro is not None:
                        todo.append(game.obj(tro.read_typetree()["m_GameObject"], tro.assets_file))
            elif c.type.name.endswith("Renderer"):
                for m in c.read_typetree().get("m_Materials", []):
                    o = game.obj(m, c.assets_file)
                    if o is not None and o.read_typetree()["m_Name"] == want:
                        material(game, m, c.assets_file, mats, texs)
                        return


def graft_shuriken(game, cls, effects, mats, texs):
    """SHURIKEN_FROM_TTO (decisions.md 40): for each listed effect built here, TTO's copy read through
    pipeline/wardrobe_fx_tto.py (Tto / Build / effect, as wardrobe_weapon_fx.tto_weapons does), and under every BB node
    whose name path matches a TTO node carrying a ParticleSystem, a new child node at local identity (pos 0, rot identity,
    scale 1) holding that node's ParticleSystem and ParticleSystemRenderer dicts, its mats (and the renderer's
    m_Materials) = SHURIKEN_MAT's BB material, added to mats. Only where TTO's bundles are (home): elsewhere a warning, and
    BB's effect stays as it is (no puffs)."""
    names = [n for n in SHURIKEN_FROM_TTO.get(cls, []) if n in effects]
    if not names:
        return
    import importlib.util
    import sys
    try:
        spec = importlib.util.spec_from_file_location("wardrobe_fx_tto", os.path.join(HERE, "wardrobe_fx_tto.py"))
        T = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(T)
        if not os.path.exists(os.path.join(T.ASSETS, "catalog.bin")) or not os.path.exists(T.AA_CATALOG):
            raise FileNotFoundError(f"TTO's bundles ({T.ASSETS}) or the catalog reader ({T.AA_CATALOG})")
        tto = T.Tto(cls, names)
        b = T.Build(tto)
        got = {n: T.effect(tto, b, n) for n in names}
    except (Exception, SystemExit) as ex:             # noqa: BLE001 (the office without TTO's bundles: BB's version stays)
        print(f"warning: {cls}: no Shuriken graft for {names} ({type(ex).__name__}: {ex}); BB's version kept", file=sys.stderr)
        return
    mat, src = SHURIKEN_MAT[cls]
    if mat not in mats:                               # BB's material of the same shader, read from a BB effect that has it
        tmp_m, tmp_t = {}, {}
        effect(game, cls, src, tmp_m, tmp_t, set())
        if mat not in tmp_m:                          # only on its Unity 3.5 Shuriken renderer (the Cat's supportFire_hit)
            bb_material(game, cls, src, mat, tmp_m, tmp_t)
        mats[mat] = tmp_m[mat]
        if tmp_m[mat].get("tex") in tmp_t:
            texs.setdefault(tmp_m[mat]["tex"], tmp_t[tmp_m[mat]["tex"]])
    for n in names:
        bb_nodes, tto_nodes = effects[n]["nodes"], got[n]["nodes"]
        tto_at = dict(zip(node_paths(tto_nodes), tto_nodes))
        for i, (path, node) in enumerate(list(zip(node_paths(bb_nodes), bb_nodes))):
            t = tto_at.get(path)
            comps = [c for c in (t or {}).get("comps", []) if c["type"] in ("ParticleSystem", "ParticleSystemRenderer")]
            if not any(c["type"] == "ParticleSystem" for c in comps):
                continue
            comps = json.loads(json.dumps(comps))
            for c in comps:
                if c["type"] == "ParticleSystemRenderer":
                    c["m_Materials"] = [mat]
            bb_nodes.append({"name": node["name"] + "_shuriken", "parent": i, "pos": [0, 0, 0], "rot": [0, 0, 0, 1],
                             "scale": [1, 1, 1], "comps": comps, "mats": [mat]})
            print(f"{cls}: {n}/{path}: TTO's ParticleSystem grafted (node {len(bb_nodes) - 1}, material {mat})", file=sys.stderr)


def rip_wav(cls, name, folder=None):
    """The rip's WAV: from the class's voices/ or sounds/ when the cue says which (they share names: crusader1, nAttack1
    ... are different recordings in each, 2026-11-09), else sounds/ then voices/ then anywhere (an effect's own sound).
    A name in SOUND_ALIASES[cls] is that file, whatever the folder."""
    alias = SOUND_ALIASES.get(cls, {}).get(name)
    if alias:
        p = os.path.join(RIP, *alias.split("/")) + ".wav"
        return p if os.path.exists(p) else None
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


def hero_sound_wav(cls, name):
    """A "sound" cue's WAV (the hero's code plays it): the class's sounds/ (never its voices/, which share names), else
    anywhere in the rip's Resources outside the characters' folders (2026-11-13, plans/fx_bat/attacks_emotes.md "Parts
    needed" 5a: the Bat's wing flap, Bat.cs's field wingFlap = Resources/sound/fx/step_fly1.wav; the other characters'
    clips are their own recordings under the same names, nAttack1 ..., so one of theirs takes a SOUND_ALIASES line)."""
    p = rip_wav(cls, name, "sounds")
    if p or SOUND_ALIASES.get(cls, {}).get(name):
        return p
    chars = os.path.normcase(os.path.join(RIP, "characters"))
    for root, dirs, fs in os.walk(os.path.dirname(RIP)):
        if os.path.normcase(root) == chars:
            dirs[:] = []
        elif name + ".wav" in fs:
            return os.path.join(root, name + ".wav")
    return None


def builds(entry):
    """An entry's "builds" (2026-11-13, plans/fx_bat/parts.md Interfaces 6: what a page part spawns or plays that no cue
    names, api.spawn / Sound.play; the guardian's blade, hits and swing) as (kind, name): "sound:<name>" / "voice:<name>"
    or ["sound", name], else an effect; a pool's skills may carry their own."""
    out = []
    for e in [entry] + list(entry.get("skills", {}).values()):
        for b in e.get("builds", []):
            if isinstance(b, (list, tuple)):
                out.append((b[0], b[1]))
            elif str(b).split(":", 1)[0] in ("sound", "voice", "fx") and ":" in str(b):
                out.append(tuple(str(b).split(":", 1)))
            else:
                out.append(("fx", str(b)))
    return out


def cue_lists(entry):
    """An entry's cue lists: its cues, or every skill's of a shared clip ({skills: {name: {cues}}})."""
    return [entry.get("cues", [])] + [s.get("cues", []) for s in entry.get("skills", {}).values()]


def cue_names(cls):
    """The effects, voices and sounds the class's cue file names, as --fx / --voices / --sounds strings (in cue order, no
    repeats; "a|b" = both)."""
    path = os.path.join(os.path.dirname(DATA), "fx_cues", cls + ".json")
    names = {"fx": [], "voice": [], "sound": []}
    for entry in json.load(open(path, encoding="utf-8")).values():
        for cues in cue_lists(entry) + [[[0, k, n] for k, n in builds(entry)]]:
            for cue in cues:
                if cue[1] not in names:      # a "skin" / "clone" cue (the hero's own look, a copy of her): nothing to build
                    continue
                for n in str(cue[2]).split("|"):
                    if cue[1] == "fx" and n.startswith("tto/"):     # TTO's effects: pipeline/wardrobe_fx_tto.py builds them
                        continue
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
                pm = {}
                one = {n: effect(game, a.cls, n, pm, {}, set())}
                graft_shuriken(game, a.cls, one, pm, {})      # (SHURIKEN_FROM_TTO: TTO's Shuriken read too, in memory)
                print(json.dumps(one, indent=1))
            except Exception as e:      # noqa: BLE001 (a script with no layout yet: say so, go on)
                print(json.dumps({n: f"{type(e).__name__}: {e}"}))
        return
    if not a.fx:
        a.fx, a.voices, a.sounds = cue_names(a.cls)
        if not a.fx and not a.voices and not a.sounds:
            ap.error(f"wardrobe/fx_cues/{a.cls}.json has no cues; write them first, or pass --fx")
    game = Game()
    mats, texs, sounds, effects = {}, {}, set(), {}
    # the page looks an effect up by the cue's name: a --fx name in another case (the inventory's lower-case returncast,
    # plans/fx_sheep/tto.md) is stored under the cue's spelling (the prefab itself is found in any case, effect())
    spell = {n.lower(): n for n in cue_names(a.cls)[0].split(",") if n} if os.path.exists(os.path.join(os.path.dirname(DATA), "fx_cues", a.cls + ".json")) else {}
    for n in [n for n in a.fx.split(",") if n]:
        effects[spell.get(n.lower(), n)] = effect(game, a.cls, n, mats, texs, sounds)
    graft_shuriken(game, a.cls, effects, mats, texs)   # TTO's decoded Shuriken onto BB's effect (decisions.md 40)
    voices =[v for v in a.voices.split(",") if v]
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
    jobs += [(n, hero_sound_wav(a.cls, n), n) for n in sorted(set(hero_sounds) - sounds)]
    jobs += [(n, rip_wav(a.cls, n, "voices"), "v_" + n) for n in sorted(set(voices))]
    for n, src, out_name in jobs:
        if not src:
            missing.append(out_name); continue
        subprocess.run([ff, "-y", "-loglevel", "error", "-i", src, "-ac", "1", "-b:a", "64k", os.path.join(sdir, out_name + ".mp3")], check=True)
    out = os.path.join(DATA, a.cls, "fx.json")
    old = json.load(open(out, encoding="utf-8")) if os.path.exists(out) else {}
    merged = {"effects": {**old.get("effects", {}), **effects}, "materials": {**old.get("materials", {}), **mats}}
    json.dump(merged, open(out, "w", encoding="utf-8"), separators=(",", ":"))   # compact: meshes and clips (2026-11-09) doubled it indented
    print(f"{a.cls}: {len(effects)} effects, {len(mats)} materials, {len(texs)} textures, {len(jobs) - len(missing)} sounds"
          + (f", missing sounds: {missing}" if missing else ""))


if __name__ == "__main__":
    main()
