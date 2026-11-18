r"""The pets' data for the wardrobe (user 2026-11-18: "Add Pet section, standing behind the hero how it would work in
game. Bring their models together with their texture and animations"; "I meant pet idle animation only").

  uv run --no-project --with UnityPy --with pillow python -I pipeline/wardrobe_pets.py [--assets tto_assets/2026-11-18] [--only <name,...>]
  -> wardrobe/data/pets/index.json      one row per pet (below), loaded with the page
     wardrobe/data/pets/<name>.json     one pet = a props entry {name, tto, nodes, anim: {default, clips: {<idle>}}}
     wardrobe/data/props/tex/<tex>.png  its textures, by the game's texture name (as the props')
     wardrobe/data/icons/pet/<code>.webp  the game's icon by pet code (gamegui/icons/items/pet/<code>, lossless; an
                                          upscale of the same picture is left alone: wardrobe_icons_upscale.py)
     tto_config/PetScale.json           TTO's Config/PetScale, copied from the installed client's resources.assets
  --assets: a decrypted TTO client (catalog.bin + dec/<bundle>, pipeline/wardrobe_tto_fetch.py; default this folder's
  tto_assets/2026-11-18, else the home PC's D:\12tails-wardrobe\tto_assets\2026-11-18). --only: those pets (prefab names,
  any case); their index rows replace the old ones. The run stops when a texture name already in props/tex holds another
  picture, and prints the pets with particles, with no clip, and every one skipped with why.

The rules are TTO 1.7.0's (plans/wardrobe_pets_tto_rules.md; TTO1118 = its GameAssembly.dll RVAs), the same as BB's
except where noted:
- Which prefabs: every catalog GameObject under gameassets/characters/pet(s)/ (effects/ aside) with a PetControl. The
  code -> prefab link: BB's from the 12 DecompiledSource\<Class>Equipment.cs EquipPet switches (bb_pet_codes; BB's
  pets load GameAssets/Characters/Pet/<name>), TTO's own from TTO1118:CharacterEquipment::EquipPet@0x1adac10 and
  EquipmentUtility::MapPetCodeName (TTO_PETS below, rules section 5). "tto" = no prefab of that name in BB's rip.
- Rest point (rest_point): Instantiate at hero - forward with the hero's rotation, then PetControl.Init / LateUpdate
  (TTO1118 0x1a928a0 / 0x1a930e0 = BB PetControl.cs): followType 1 / 2 / 3 rest at hero - followDistance x forward,
  0 (FloatBehind) there + offset_<class>, 4 / 5 (ParentPosition / ParentAll) at hero + offset_<class>.
- Size (pet_scale): TTO1118:CharacterEquipment::GetPetSize@0x1adcff0: the Cute Cats p_all31-35 a flat 4.0; else
  (0.1 + 0.01 x level for p_svk, else 0.9 + 0.1 x level = BB SheepEquipment.cs:5021) x
  PetScales.Multiplier(hero, code)@0x1af5440 over Config/PetScale. Level = 1 for p_all codes; else the shop's highest
  (pet_level: BB's 47 upgradable families Lv 9, PetShopData.cs:123-670; the 7 without a recipe Lv 1; TTO's own families
  Lv 9 as a guess, flagged "level_guess": their upgrade list is server data).
- Idle clip (idle_clip): TTO1118:PetControl::FindClip@0x1a92600 with the prefab's idlePrefix, played by PlayIdle at rest
  for followType 1 / 2 / 3; else the Animation's default clip when it plays automatically; else the prefab pose.
- Names (game): BB's PetData.cs getData (itemClass.name; a family's level appended as the game does); TTO's names are
  server data, so only "S.ValkorNoct" (a string literal of the client) is known, written "S.ValkorNoct 9" like BB's
  names; the rest null (the page humanizes).

Index row: {name, file, code (no level digit), level, game, icon, tto, follow: {type, dist, offset: {cls: [x, y, z]}},
rest: {cls: [x, y, z]}, scale: {cls: s}, size: [w, h, d], particles: N [, level_guess: true]}. Positions are in
three.js space, both follow.offset and rest: x mirrored, mp() of the game's Unity values. rest = rest_point of the
game's (Unity-space) values: where the page puts the pet's root beside a hero at the origin facing +z. Do not feed the
row's follow back to rest_point, which takes Unity values and would mirror x twice. In three.js space rest is
[0, 0, -dist] for types 1 / 2 / 3, [0, 0, -dist] + offset for 0, and offset for 4 / 5. size = the drawn meshes'
bounds at scale 1 as the pet rests (rest_size: the idle clip's first frame, else the prefab pose). Particle systems
are not extracted, only counted.
A pet file's nodes are the prefab tree (the props' p / q / s), kept where a mesh, a skin's bone or the idle clip needs
them. The root is at identity (the game replaces its transform: Instantiate + localScale). Skinned meshes are the props'
live skins (on the pet's own nodes, bones = node indices, ibm). Materials come from wardrobe_convert's prop_mats: BB's
material of the texture's name for BB pets; for TTO's own, the bundle shader's opacity (tto_shader). The idle clip's
tracks are keyed by node index, in the game's Hermite keys, mirrored.
Tests: pipeline/test_wardrobe_pets.py (the pure functions; no UnityPy at import).
"""
import io
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)                    # run as a script (-I), pipeline/ is not a package: the sibling module by its bare name
from wardrobe_convert import clip_dict, mp, mq, prop_mats, prop_mesh, r5   # noqa: E402  (the props' conversion, shared)

CLASSES = ["bat", "bison", "cat", "chameleon", "mole", "monkey", "panda", "penguin", "rabbit", "sheep", "whale", "wolf"]
BIBLE = next((p for p in (r"D:\12tails", r"C:\Users\Jump\Desktop\12tails") if os.path.isdir(os.path.join(p, "DecompiledSource"))),
             r"D:\12tails")
BB_SRC = os.path.join(BIBLE, "DecompiledSource")
BB_PET_DIR = os.path.join(BIBLE, r"RippedAssets\ExportedProject\Assets\Resources\gameassets\characters\pet")
TOOLS = os.path.join(BIBLE, "DecompiledSource_TTO_2026-11-14", "tools")      # aa_catalog.py (as wardrobe_tto_fetch.py)
GAME = os.path.join(os.environ.get("LOCALAPPDATA", ""), "TailsTopia", "game", "TailsTopia", "TailsTopiaOnline_Data")
OUT = os.path.join(ROOT, "wardrobe", "data")
CFG = os.path.join(ROOT, "tto_config")

# BB's pet shop (PetShopData.getUpgradeItem, PetShopData.cs:123-670; rules section 7): families that upgrade to Lv 9, and
# those with no recipe (Lv 1 only). p_lck / p_lpd have no prefab anywhere.
UPGRADABLE = set("p_lcr p_lcp p_lmp p_lpp p_lct p_lcc p_lpk p_lml p_lbd p_lcs p_lms p_lps p_lmc p_lmn p_lmo p_ldc p_ldm "
                 "p_ldp p_ldt p_ldn p_ldk p_skr p_skg p_sky p_skb p_skk p_sfb p_sim p_sam p_sob p_sgb p_slb p_stb p_spb "
                 "p_swb p_ssq p_snb p_sab p_spg p_spf p_msb p_mcb p_mab p_mrb p_mmb p_mgb p_mnb".split())
NO_RECIPE = set("p_srp p_sss p_sbb p_sdm p_sdv p_skz p_skm".split())

# TTO's own pets: code -> catalog address under gameassets/characters/pets/ (rules section 5: TTO1118 EquipPet's whole
# code compares 0x1adb656-0x1adb9fd and its family branch "GameAssets/Characters/Pets/" + MapPetCodeName(family),
# EquipmentUtility..cctor@0x165d8b0). The six-character family codes take a level digit; p_mrd (not p_mrb) is the blue
# Mini Rabby.
TTO_PETS = {
    "p_all57": "all57", "p_all58": "all58", "p_all59": "all59", "p_all70": "all70",
    "p_all83": "moneypiggy", "p_all85": "tianlonga", "p_all86": "tianlongb",
    "p_all87": "violeta", "p_all88": "apo", "p_all89": "koalia",
    "p_all31": "cutecat/cutecat_w", "p_all32": "cutecat/cutecat_b", "p_all33": "cutecat/cutecat_o",
    "p_all34": "cutecat/cutecat_v", "p_all35": "cutecat/cutecat_r",
    "p_all81": "dino/greenshark", "p_all76": "dino/blueshark", "p_all75": "dino/pinkshark",
    "p_allhlw": "smallselene/smallselene", "p_all90": "halloweenghost",
    "p_all63": "all63", "p_all64": "all64", "p_all65": "all65", "p_all66": "all66", "p_all67": "all67", "p_all68": "all68",
    "p_mrd": "minirabby/minirabbyb", "p_mrg": "minirabby/minirabbyg", "p_mrw": "minirabby/minirabbyw",
    "p_srb": "smallrabby/smallrabbyb", "p_srg": "smallrabby/smallrabbyg", "p_srs": "smallrabby/smallrabbys",
    "p_srw": "smallrabby/smallrabbyw",
    "p_drz": "smalldragonz/smalldragonz", "p_sfd": "smallflowerdryad/smallflowerdryad",
    "p_mtf": "motherflowerbug/motherflowerbug", "p_svk": "valkornoct_pet",
}
TTO_FAMILIES = {c for c in TTO_PETS if not c.startswith("p_all")}

# TTO's own pets' materials (no BB material to read): the bundle's shader. Opaque = ignores the texture's alpha
# (the page then draws it without the 0.5 alpha cut); anything else keeps the cut
TTO_OPAQUE_SHADERS = {"FlexibleCelShader/Cel No Outline", "Legacy Shaders/Diffuse", "Toon"}


# ---- pure rules (tested) ----

_EQUIP = re.compile(r'\b(?:a|nPet) == "(?P<code>p_\w+)"|Resources\.Load\("(?i:GameAssets/Characters/Pet/)(?P<name>[^"]+)"')
_NAMES = re.compile(r'\b(?:a|nCommand) == "(?P<code>p_\w+)"'
                    r'|itemClass\.name = "(?P<name>(?:[^"\\]|\\.)*)"(?P<lv>\s*\+\s*lastDigit)?\s*;')


def bb_pet_codes(cs_text):
    """BB's EquipPet switch (an Equipment file): pet code -> prefab name, each `a == "p_xxx"` / `nPet == "p_all1"`
    compare paired with the next Resources.Load("GameAssets/Characters/Pet/<name>") before another compare."""
    out, cur = {}, None
    for m in _EQUIP.finditer(cs_text):
        if m.group("code"):
            cur = m.group("code")
        elif cur is not None:
            out.setdefault(cur, m.group("name"))
            cur = None
    return out


def bb_pet_names(cs_text):
    """BB's PetData.getData: code -> (the name literal, whether the level digit is appended: `"L. Carron " + lastDigit`)."""
    out, cur = {}, None
    for m in _NAMES.finditer(cs_text):
        if m.group("code"):
            cur = m.group("code")
        elif cur is not None:
            out.setdefault(cur, (m.group("name"), bool(m.group("lv"))))
            cur = None
    return out


def pet_level(code):
    """(level shown, guessed): the shop's highest level of a family; p_all codes have none (1)."""
    if code.startswith("p_all"):
        return 1, False
    if code in UPGRADABLE:
        return 9, False
    if code in TTO_FAMILIES:
        return 9, True
    return 1, False                                       # NO_RECIPE (and any family the shop lists nowhere)


def game_name(code, level, names):
    """The game's name: BB's PetData literal (+ the level digit where BB appends it); for TTO's own only S.ValkorNoct."""
    if code == "p_svk":
        return "S.ValkorNoct " + str(level)
    if code in names:
        text, with_level = names[code]
        return text + str(level) if with_level else text
    return None


def rest_point(follow, cls):
    """Where the pet's root rests beside a still hero at the origin facing +z, in three.js space. `follow` holds the
    prefab's PetControl values as the game has them (Unity space): {type, dist, offset: {cls: [x, y, z]}}."""
    t, d = follow["type"], follow.get("dist", 1.0)
    o = (follow.get("offset") or {}).get(cls, [0.0, 0.0, 0.0])
    if t in (1, 2, 3):                                    # FloatFollow / RunBehind / RunFollow: hero - fd x forward
        u = [0.0, 0.0, -d]
    elif t == 0:                                          # FloatBehind: that + the class offset, in world axes
        u = [o[0], o[1], o[2] - d]
    elif t in (4, 5):                                     # ParentPosition / ParentAll: hero + TransformDirection(offset)
        u = list(o)
    else:
        raise ValueError(f"followType {t}")
    return [round(x, 5) + 0.0 for x in mp(u)]


def family(code):
    """TTO1118:PetScales::Family@0x1af52b0: the five-character family of a six-character code, not p_all."""
    return code[:5] if len(code) == 6 and code[:5] != "p_all" else None


def multiplier(table, hero, code):
    """TTO1118:PetScales::Multiplier(hero, code)@0x1af5440 over Config/PetScale ({heroes: [{hero, scale, entries:
    [{code, scale}]}], pets: [{code, scale}]})."""
    if not code:
        return 1.0
    heroes = {h.get("hero"): h for h in (table or {}).get("heroes", [])}
    row = heroes.get(hero, {})
    by_code = {e.get("code"): e.get("scale", 0.0) for e in row.get("entries", [])}
    fam = family(code)
    for k in (code, fam):
        if k is not None and k in by_code:               # a per-class entry: returned alone
            return by_code[k] if by_code[k] > 0 else 1.0
    pets = {p.get("code"): p.get("scale", 0.0) for p in (table or {}).get("pets", [])}
    ps = pets[code] if pets.get(code, 0) > 0 else pets[fam] if fam is not None and pets.get(fam, 0) > 0 else 1.0
    hs = row["scale"] if code.startswith("p_all") and row.get("scale", 0) > 0 else 1.0
    return ps * hs


def pet_scale(code, level, cls, table):
    """The pet's localScale beside this class (TTO1118:CharacterEquipment::GetPetSize@0x1adcff0). `code` is the base
    code (p_lcr, p_all85); a family's level digit is added for the game's code (p_lcr9)."""
    if code.startswith("p_all"):
        level, npet = 1, code
    else:
        npet = code + str(level) if len(code) == 5 else code
    if len(npet) == 7 and npet.startswith("p_all3") and npet[6] in "12345":     # IsStaticLargePet: the Cute Cats
        return 4.0
    base = level * 0.01 + 0.1 if npet[:5] == "p_svk" else level * 0.1 + 0.9
    return round(base * multiplier(table, cls.capitalize(), npet), 6)


def find_clip(names, prefix):
    """TTO1118:PetControl::FindClip@0x1a92600 over the Animation's states (m_Animations order), case-blind: a state
    named the prefix or starting with prefix + "_" at once, else the first one starting with the prefix."""
    if not prefix:
        return None
    p, first = prefix.lower(), None
    for n in names:
        low = n.lower()
        if low == p or low.startswith(p + "_"):
            return n
        if first is None and low.startswith(p):
            first = n
    return first


def idle_clip(clip_names, default, idle_prefix, follow_type, play_automatically):
    """What plays at rest: PlayIdle's FindClip(idlePrefix) for followType 1 / 2 / 3 (LateUpdate's at-rest branch, its
    only caller); else the default clip when the Animation plays it automatically; else None (the prefab pose)."""
    if follow_type in (1, 2, 3):
        hit = find_clip(clip_names, idle_prefix)
        if hit is not None:
            return hit
    if play_automatically and default in clip_names:
        return default
    return None


def idle_loops(by_find, clip_wrap, anim_wrap):
    """Whether the idle repeats. Legacy WrapMode: 0 Default (the clip's takes the Animation's; both Default = once),
    1 Once, 2 Loop, 4 PingPong, 8 ClampForever. PlayIdle CrossFades every frame at rest, so a clip that stops at its end
    starts again; only ClampForever holds its last frame. A clip played automatically repeats only by its wrap mode."""
    wrap = clip_wrap or anim_wrap
    return wrap != 8 if by_find else wrap in (2, 4)


# ---- the build (UnityPy, Pillow) ----

def tto_shader(shader, mode):
    """A TTO pet's material behaviour from its bundle shader (Standard: _Mode 0 = opaque); prop_mats gives TTO's own
    items none (BB's rip has no material for them)."""
    if shader in TTO_OPAQUE_SHADERS or (shader == "Standard" and not mode):
        return {"shader": "opaque"}
    return {}


def mat4(p, q, s):
    x, y, z, w = q
    R = [[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
         [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
         [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]]
    return [[R[r][0] * s[0], R[r][1] * s[1], R[r][2] * s[2], p[r]] for r in range(3)] + [[0.0, 0.0, 0.0, 1.0]]


def mmul(A, B):
    return [[sum(A[r][k] * B[k][c] for k in range(4)) for c in range(4)] for r in range(4)]


def apply(M, v):
    return [M[r][0] * v[0] + M[r][1] * v[1] + M[r][2] * v[2] + M[r][3] for r in range(3)]


def rest_size(entry):
    """[w, h, d] of a pet file's drawn meshes at scale 1, the root at identity, in the pose it rests in: the idle
    clip's first keys over the prefab's TRS (the root's own track aside: the page places the root), or the prefab pose
    without a clip. A skin as the page draws it: sum of w x bone x ibm x v. The prefab pose alone is not what shows:
    the Dino sharks lie on their back in it, their Root bone stood up only by the clip."""
    nodes = entry["nodes"]
    a = entry.get("anim")
    tracks = a["clips"][a["default"]]["tracks"] if a else {}
    W, vis = [], []
    for k, n in enumerate(nodes):
        p, q, s = n["p"], n["q"], n["s"]
        tr = tracks.get(str(k)) if k else None
        if tr:
            q = tr["q"][0][1:5] if "q" in tr else q
            p = tr["p"][0][1:4] if "p" in tr else p
            s = tr["s"][0][1:4] if "s" in tr else s
        M = mat4(p, q, s)
        W.append(M if n["parent"] < 0 else mmul(W[n["parent"]], M))
        vis.append(n.get("on", True) and (n["parent"] < 0 or vis[n["parent"]]))
    lo, hi = [math.inf] * 3, [-math.inf] * 3

    def grow(v):
        for i in range(3):
            lo[i], hi[i] = min(lo[i], v[i]), max(hi[i], v[i])
    for k, n in enumerate(nodes):
        if not vis[k]:
            continue
        if "mesh" in n:
            pos = n["mesh"]["pos"]
            for i in range(0, len(pos), 3):
                grow(apply(W[k], pos[i:i + 3]))
        if "skin" in n:
            sk = n["skin"]
            Bm = [mmul(W[b], [[sk["ibm"][16 * j + 4 * c + r] for c in range(4)] for r in range(4)])
                  for j, b in enumerate(sk["bones"])]
            pos = sk["pos"]
            for i in range(len(pos) // 3):
                acc = [0.0, 0.0, 0.0]
                for t in range(4):
                    wt = sk["w"][4 * i + t]
                    if wt > 0:
                        pv = apply(Bm[sk["j"][4 * i + t]], pos[3 * i:3 * i + 3])
                        acc = [acc[x] + wt * pv[x] for x in range(3)]
                grow(acc)
    return [round(hi[i] - lo[i], 4) + 0.0 for i in range(3)] if hi[0] >= lo[0] else [0, 0, 0]


def main():
    import argparse
    import subprocess

    import UnityPy
    from PIL import Image
    from UnityPy.helpers.MeshHelper import MeshHandler
    from wardrobe_icons_upscale import keep as keep_upscaled

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    own = os.path.join(ROOT, "tto_assets", "2026-11-18")
    ap = argparse.ArgumentParser(description="The pets' data for the wardrobe")
    ap.add_argument("--assets", default=own if os.path.isdir(own) else r"D:\12tails-wardrobe\tto_assets\2026-11-18")
    ap.add_argument("--only", help="pet prefab names, comma separated (any case)")
    a = ap.parse_args()
    only = {x.strip().lower() for x in a.only.split(",")} if a.only else None
    P = lambda c: c.component if hasattr(c, "component") else c[1]       # noqa: E731
    v3 = lambda v: [v.x, v.y, v.z]                                       # noqa: E731
    q4 = lambda q: [q.x, q.y, q.z, q.w]                                  # noqa: E731

    # ---- Config/PetScale (Resources TextAsset, built in: resources.assets) ----
    os.makedirs(CFG, exist_ok=True)
    cfg = os.path.join(CFG, "PetScale.json")
    if os.path.exists(os.path.join(GAME, "resources.assets")):
        env = UnityPy.load(os.path.join(GAME, "resources.assets"))
        text = None
        for obj in env.objects:
            if obj.type.name == "TextAsset":
                t = obj.read()
                if t.m_Name == "PetScale":
                    text = t.m_Script if isinstance(t.m_Script, str) else t.m_Script.decode("utf-8", "replace")
        if text is None:
            sys.exit(f"no TextAsset PetScale in {GAME}\\resources.assets")
        open(cfg, "w", encoding="utf-8", newline="").write(text)              # the TextAsset's bytes as they are
        print(f"Config/PetScale copied from the installed client -> {cfg}")
    elif os.path.exists(cfg):
        print(f"no installed client: {cfg} as it is")
    else:
        sys.exit(f"no installed client ({GAME}) and no {cfg}")
    table = json.load(open(cfg, encoding="utf-8"))

    # ---- codes, names ----
    bb_codes, disagree = {}, []
    for cls in CLASSES:
        for code, name in bb_pet_codes(open(os.path.join(BB_SRC, f"{cls.capitalize()}Equipment.cs"), encoding="utf-8").read()).items():
            if bb_codes.setdefault(code, name) != name:
                disagree.append(f"{cls} {code}: {name} (others {bb_codes[code]})")
    if disagree:
        print("the classes' EquipPet disagree (the first kept):", *disagree, sep="\n  ")
    names = bb_pet_names(open(os.path.join(BB_SRC, "PetData.cs"), encoding="utf-8").read())
    bb_prefabs = {f[:-7].lower() for f in os.listdir(BB_PET_DIR) if f.endswith(".prefab")}
    by_addr = {"gameassets/characters/pet/" + n.lower(): c for c, n in bb_codes.items()}
    clash = [c for c in TTO_PETS if c in bb_codes]
    if clash:
        sys.exit(f"TTO's table repeats BB codes: {clash}")
    by_addr.update({"gameassets/characters/pets/" + p: c for c, p in TTO_PETS.items()})
    print(f"codes: {len(bb_codes)} BB ({len(bb_prefabs)} BB prefabs in the rip), {len(TTO_PETS)} TTO's own")

    # ---- the catalog ----
    out = subprocess.run([sys.executable, "-P", os.path.join(TOOLS, "aa_catalog.py"), os.path.join(a.assets, "catalog.bin"),
                          "--grep", r"(?i)^gameassets/characters/pets?/|^gamegui/icons/items/pet/"],
                         capture_output=True, text=True, encoding="utf-8", check=True).stdout
    rows = [line.split("\t") for line in out.splitlines() if line.count("\t") >= 3]
    pets = {r[0].lower(): r for r in rows if r[1].endswith("GameObject") and "/effects/" not in r[0].lower()
            and re.match(r"gameassets/characters/pets?/", r[0].lower())}
    icons = {r[0].rsplit("/", 1)[1].lower(): r for r in rows if r[1].endswith("Texture2D") and r[0].startswith("gamegui/icons/items/pet/")}
    skipped = []
    for addr, code in sorted(by_addr.items(), key=lambda kv: kv[1]):
        if addr not in pets:
            skipped.append(f"{code}: no prefab {addr} in the catalog")
    todo = []
    for addr, r in sorted(pets.items()):
        code = by_addr.get(addr)
        if code is None:
            skipped.append(f"{r[0]}: no pet code loads it")
        elif only is None or addr.rsplit("/", 1)[1] in only:
            todo.append((addr, r, code))
    if only is not None and only - {addr.rsplit("/", 1)[1] for addr, _, _ in todo}:
        sys.exit(f"--only: no pet prefab named {sorted(only - {addr.rsplit('/', 1)[1] for addr, _, _ in todo})}")
    bundles = sorted({b for _, r, _ in todo for b in r[3].split()} | {icons[c[2:]][3].split()[0] for _, _, c in todo if c[2:] in icons})
    missing = [b for b in bundles if not os.path.exists(os.path.join(a.assets, "dec", b))]
    if missing:
        sys.exit(f"{len(missing)} bundles not decrypted in {a.assets}\\dec (pipeline/wardrobe_tto_fetch.py): {missing[:3]} ...")
    env = UnityPy.load(*[os.path.join(a.assets, "dec", b) for b in bundles])
    container = dict(env.container.items())
    print(f"{len(todo)} pet prefabs in {len(bundles)} bundles ({a.assets})", flush=True)

    # ---- per pet ----
    textures = {}           # file name -> (key, PIL image): every texture once
    tex_of = {}             # (file, path id) -> file name
    shader_log = {}
    index, files, particles, no_clip, notes, moved_roots = [], {}, [], [], [], []

    def texture(ptr):
        if not ptr.m_PathID:
            return None
        try:
            t = ptr.read()
        except Exception as e:
            notes.append(f"texture: {type(e).__name__}: {e}")
            return None
        key = (t.assets_file.name, ptr.m_PathID)
        if key not in tex_of:
            fn = (re.sub(r"[^\w.-]", "_", t.m_Name) or "tex") + ".png"
            img = t.image
            if fn in textures and textures[fn][0] != key:
                prev = textures[fn][1]
                if prev.size != img.size or prev.convert("RGBA").tobytes() != img.convert("RGBA").tobytes():
                    sys.exit(f"two textures named {fn} with different pictures (pets {key} and {textures[fn][0]}): stop")
            else:
                textures[fn] = (key, img)
            tex_of[key] = fn
        return tex_of[key]

    def material(ptr, tto, pet):
        if not ptr.m_PathID:
            return {"tex": None, "color": [1, 1, 1, 1]}
        try:
            m = ptr.read()
        except Exception as e:
            notes.append(f"{pet}: material {type(e).__name__}: {e}")
            return {"tex": None, "color": [1, 1, 1, 1]}
        tex, color, mode = None, [1, 1, 1, 1], 0
        for k, v in m.m_SavedProperties.m_TexEnvs:
            if k == "_MainTex":
                tex = texture(v.m_Texture)
        for k, v in m.m_SavedProperties.m_Colors:
            if k == "_Color":
                color = [v.r, v.g, v.b, v.a]
        for k, v in m.m_SavedProperties.m_Floats:
            if k == "_Mode":
                mode = v
        try:
            sh = m.m_Shader.read()
            shader = sh.m_ParsedForm.m_Name if getattr(sh, "m_ParsedForm", None) is not None else sh.m_Name
        except Exception:
            shader = None
        out = prop_mats([{"tex": tex, "color": color}], tto)[0]     # BB pets: BB's material of the texture's name
        if tto:
            out.update(tto_shader(shader, mode))
            shader_log.setdefault((shader, out.get("shader", "cut 0.5")), set()).add(pet)
        return out

    def mesh_dict(mesh, skin, pet):
        h = MeshHandler(mesh)
        h.process()
        d = {"pos": [list(v) for v in h.m_Vertices], "nrm": [list(v) for v in (h.m_Normals or [])],
             "uv0": [list(v) for v in (h.m_UV0 or [])], "subs": [[list(t) for t in sub] for sub in h.get_triangles()]}
        if skin:
            d["w"] = [list(v) for v in (h.m_BoneWeights or [])]
            d["bi"] = [list(v) for v in (h.m_BoneIndices or [])]
            d["bind"] = [[[getattr(b, f"e{r}{c}") for c in range(4)] for r in range(4)] for b in mesh.m_BindPose]
            if d["bi"] and not d["w"]:                   # indices with no weight channel: one bone per vertex, weight 1
                d["w"] = [[1.0] + [0.0] * (len(v) - 1) for v in d["bi"]]
                notes.append(f"{pet} {mesh.m_Name}: no bone weights, one bone per vertex (weight 1)")
        return d

    for addr, r, code in todo:
        obj = container.get(r[2])
        if obj is None:
            skipped.append(f"{code} {r[0]}: not in the loaded bundles")
            continue
        go = obj.read()
        pet = go.m_Name
        tto = pet.lower() not in bb_prefabs
        nodes, node_of, pc, anims, skins, n_fx = [], {}, None, [], [], 0

        def walk(tr_ptr, parent):
            nonlocal pc, n_fx
            tr = tr_ptr.read()
            g = tr.m_GameObject.read()
            me = len(nodes)
            node = {"name": g.m_Name, "parent": parent, "p": v3(tr.m_LocalPosition), "q": q4(tr.m_LocalRotation),
                    "s": v3(tr.m_LocalScale), "on": bool(getattr(g, "m_IsActive", True))}
            nodes.append(node)
            node_of[tr_ptr.m_PathID] = me
            filt = None
            for c in g.m_Component:
                ptr = P(c)
                t = ptr.type.name
                if t == "MeshFilter":
                    filt = ptr.read().m_Mesh
                elif t in ("MeshRenderer", "SkinnedMeshRenderer"):
                    rr = ptr.read()
                    if not getattr(rr, "m_Enabled", True):
                        continue
                    mesh_ptr = filt if t == "MeshRenderer" else rr.m_Mesh
                    if mesh_ptr is None or not mesh_ptr.m_PathID:
                        continue
                    mats = [material(x, tto, pet) for x in rr.m_Materials]
                    if t == "SkinnedMeshRenderer" and getattr(rr, "m_Bones", None):
                        skins.append((me, mesh_dict(mesh_ptr.read(), True, pet), [b.m_PathID for b in rr.m_Bones], mats))
                    else:
                        node["mesh"], node["mats"] = mesh_dict(mesh_ptr.read(), False, pet), mats
                elif t == "Animation":
                    anims.append((me, ptr))
                elif t == "ParticleSystem":
                    n_fx += 1
                elif t == "MonoBehaviour" and pc is None:
                    try:
                        tt = ptr.read_typetree()
                    except Exception:
                        continue
                    if "followType" in tt and "followDistance" in tt:
                        pc = (me, tt)
            for ch in tr.m_Children:
                walk(ch, me)
        tp = next(P(c) for c in go.m_Component if P(c).type.name == "Transform")
        walk(tp, -1)
        if pc is None:
            skipped.append(f"{code} {pet}: no PetControl")
            continue
        pc_node, ptt = pc
        for me, md, bone_pids, mats in skins:
            if any(b not in node_of for b in bone_pids) or len(md["bind"]) != len(bone_pids):
                notes.append(f"{pet} {nodes[me]['name']}: a skinned mesh with bones outside the prefab - left out")
                continue
            nodes[me]["skin"] = {"mesh": md, "bones": [node_of[b] for b in bone_pids], "mats": mats}
        if not any("mesh" in n or "skin" in n for n in nodes):
            skipped.append(f"{code} {pet}: no mesh")
            continue

        # PetControl's values (a missing offset_<class>: Init's LogError, offset 0)
        ftype = int(ptt["followType"])
        dist = float(ptt["followDistance"])
        prefix = ptt["idlePrefix"] if "idlePrefix" in ptt else "root"            # the .ctor's default
        offs = {}
        for cls in CLASSES:
            o = ptt.get(f"offset_{cls}")
            if o is None:
                notes.append(f"{pet}: no offset_{cls} (0)")
            offs[cls] = [float(o["x"]), float(o["y"]), float(o["z"])] if o else [0.0, 0.0, 0.0]
        follow_u = {"type": ftype, "dist": dist, "offset": offs}

        # the idle clip: GetComponent<Animation>() on the PetControl's own object; another Animation in the tree only
        # plays its default clip
        anim = next((x for x in anims if x[0] == pc_node), anims[0] if anims else None)
        if len(anims) > 1:
            notes.append(f"{pet}: {len(anims)} Animations, the one on {nodes[anim[0]]['name']} used")
        clip = None
        if anim is not None:
            an_node, an_ptr = anim
            att = an_ptr.read_typetree()
            an = an_ptr.read()
            clip_ptrs = [cp for cp in an.m_Animations if cp.m_PathID]
            cnames = []
            for cp in clip_ptrs:
                try:
                    cnames.append(cp.read().m_Name)
                except Exception as e:
                    cnames.append(None)
                    notes.append(f"{pet}: a clip unreadable ({type(e).__name__})")
            dflt = None
            if an.m_Animation.m_PathID:
                try:
                    dflt = an.m_Animation.read().m_Name
                except Exception:
                    pass
            own_prefix = prefix if an_node == pc_node else ""                    # FindClip runs on the PetControl's own
            auto = bool(att.get("m_PlayAutomatically"))
            idle = idle_clip([c for c in cnames if c], dflt, own_prefix, ftype, auto)
            if idle is None:
                no_clip.append(f"{pet}: {cnames} default {dflt}, auto {auto}, type {ftype}, prefix {prefix!r}")
            else:
                tt = clip_ptrs[cnames.index(idle)].deref_parse_as_dict()
                if not tt.get("m_Legacy") or tt.get("m_Compressed") or tt.get("m_EulerCurves"):
                    no_clip.append(f"{pet}: idle {idle} not plain legacy curves - skipped")
                else:
                    kids = {}
                    for k, n in enumerate(nodes):
                        kids.setdefault(n["parent"], []).append(k)

                    def resolve(path):                    # a clip path is relative to the Animation's node
                        k = an_node
                        for part in [x for x in path.split("/") if x]:
                            k = next((c for c in kids.get(k, []) if nodes[c]["name"] == part), None)
                            if k is None:
                                return None
                        return k
                    lost = set()
                    tt2 = dict(tt)
                    for field in ("m_RotationCurves", "m_PositionCurves", "m_ScaleCurves"):
                        cvs = []
                        for cv in tt.get(field) or []:
                            k = resolve(cv["path"])
                            if k is None:
                                lost.add(cv["path"])
                            cvs.append({**cv, "path": "u" if k is None else str(k)})
                        tt2[field] = cvs
                    c = clip_dict(tt2)                    # tracks by node index, mirrored (x, -y, -z, w) / (-x, y, z)
                    c["tracks"].pop("u", None)
                    by_find = ftype in (1, 2, 3) and find_clip([x for x in cnames if x], own_prefix) == idle
                    c["loop"] = idle_loops(by_find, int(tt.get("m_WrapMode", 0)), int(att.get("m_WrapMode", 0)))
                    if lost:
                        notes.append(f"{pet}: idle {idle}: {len(lost)} curve paths not in the prefab, left out")
                    if tt.get("m_FloatCurves") or tt.get("m_PPtrCurves"):
                        notes.append(f"{pet}: idle {idle}: float / object curves not played "
                                     f"({len(tt.get('m_FloatCurves') or [])} / {len(tt.get('m_PPtrCurves') or [])})")
                    if not c["loop"]:
                        notes.append(f"{pet}: idle {idle} plays once (wrap {tt.get('m_WrapMode')}, Animation {att.get('m_WrapMode')})")
                    if "0" in c["tracks"]:
                        notes.append(f"{pet}: idle {idle} moves the root (the page places the root: not played)")
                    clip = (an_node, idle, c)
        else:
            no_clip.append(f"{pet}: no Animation")

        # keep the nodes a mesh, a skin's bone or the clip needs, and their parents
        keep = [False] * len(nodes)

        def mark(k):
            while k >= 0 and not keep[k]:
                keep[k] = True
                k = nodes[k]["parent"]
        for k, n in enumerate(nodes):
            if "mesh" in n or "skin" in n:
                mark(k)
            for b in n.get("skin", {}).get("bones", []):
                mark(b)
        if clip:
            mark(clip[0])
            for k in clip[2]["tracks"]:
                mark(int(k))
        mark(0)
        remap, nn = {}, []
        for k, n in enumerate(nodes):
            if not keep[k]:
                continue
            remap[k] = len(nn)
            root = k == 0
            e = {"name": n["name"], "parent": remap.get(n["parent"], -1),
                 "p": [0, 0, 0] if root else [round(x, 5) + 0.0 for x in mp(n["p"])],
                 "q": [0, 0, 0, 1] if root else [round(x, 6) + 0.0 for x in mq(n["q"])],
                 "s": [1, 1, 1] if root else [round(x, 5) for x in n["s"]], "on": n["on"]}
            if "mesh" in n:
                e["mesh"] = prop_mesh(n["mesh"], len(n["mats"]))
                e["mats"] = n["mats"]
            if "skin" in n:
                sk, M = n["skin"], n["skin"]["mesh"]
                e["skin"] = prop_mesh(M, len(sk["mats"]))
                e["skin"]["w"] = [round(float(x), 5) for v in M["w"] for x in (list(v) + [0, 0, 0, 0])[:4]]
                e["skin"]["j"] = [int(x) for v in M["bi"] for x in (list(v) + [0, 0, 0, 0])[:4]]
                Sg = (-1, 1, 1, 1)                            # bind poses S B S, column-major for three.js
                e["skin"]["ibm"] = [round(b[rr][cc] * Sg[rr] * Sg[cc], 6) for b in M["bind"] for cc in range(4) for rr in range(4)]
                e["mats"] = sk["mats"]
            nn.append(e)
        for k, n in enumerate(nodes):
            if keep[k] and "skin" in n:
                nn[remap[k]]["skin"]["bones"] = [remap[b] for b in n["skin"]["bones"]]
        root = nodes[0]
        if any(abs(x) > 1e-6 for x in root["p"]) or any(abs(x - y) > 1e-6 for x, y in zip(root["q"] + root["s"], [0, 0, 0, 1, 1, 1, 1])):
            moved_roots.append(pet)
        entry = {"name": pet, "tto": tto, "nodes": nn}
        if clip:
            _, idle, c = clip
            c["tracks"] = {str(remap[int(k)]): tr for k, tr in c["tracks"].items()}
            entry["anim"] = {"default": idle, "clips": {idle: c}}

        size = rest_size(entry)

        level, guess = pet_level(code)
        if not code.startswith("p_all") and code not in UPGRADABLE | NO_RECIPE | TTO_FAMILIES:
            notes.append(f"{pet}: {code} in no level list (Lv 1)")
        short = code[2:]
        if short in icons:
            ic = container.get(icons[short][2])
            if ic is None:
                notes.append(f"{pet}: icon {short} not in the loaded bundles")
                icon = None
            else:
                icon = f"icons/pet/{short}.webp"
                files[os.path.join(OUT, "icons", "pet", f"{short}.webp")] = ic.read().image
        else:
            icon = None
            notes.append(f"{pet}: no icon gamegui/icons/items/pet/{short}")
        row = {"name": pet, "file": f"pets/{pet}.json", "code": code, "level": level,
               "game": game_name(code, level, names) if not tto or code == "p_svk" else None, "icon": icon, "tto": tto,
               "follow": {"type": ftype, "dist": r5(dist), "offset": {cls: [round(x, 5) + 0.0 for x in mp(offs[cls])] for cls in CLASSES}},
               "rest": {cls: rest_point(follow_u, cls) for cls in CLASSES},
               "scale": {cls: pet_scale(code, level, cls, table) for cls in CLASSES},
               "size": size, "particles": n_fx}
        if guess:
            row["level_guess"] = True
        if not tto and row["game"] is None:
            notes.append(f"{pet}: {code} has no name in PetData.cs")
        if n_fx:
            particles.append(f"{pet} ({n_fx})")
        index.append(row)
        files[os.path.join(OUT, "pets", f"{pet}.json")] = entry
        print(f"  {pet:20s} {code:9s} Lv {level} {'TTO' if tto else 'BB '} type {ftype} dist {r5(dist)} "
              f"idle {clip[1] if clip else '-'}  nodes {len(nn)}  size {size}", flush=True)

    # ---- texture names: one picture per name in props/tex (the props' and the pets') ----
    ptex = os.path.join(OUT, "props", "tex")
    new_tex, same_tex = [], 0
    for fn, (key, img) in sorted(textures.items()):
        buf = io.BytesIO()
        img.save(buf, "PNG")
        data = buf.getvalue()
        path = os.path.join(ptex, fn)
        if os.path.exists(path):
            if open(path, "rb").read() == data:
                same_tex += 1
                continue
            with Image.open(path) as old:
                if old.size == img.size and old.convert("RGBA").tobytes() == img.convert("RGBA").tobytes():
                    same_tex += 1                          # the same picture, other PNG bytes: left as it is
                    continue
            sys.exit(f"texture name clash: props/tex/{fn} already holds another picture (pet texture {key}): stop")
        new_tex.append((path, data))

    # ---- write ----
    names_seen = {}
    for row in index:
        low = row["name"].lower()
        if low in names_seen:
            sys.exit(f"two pets named {row['name']} / {names_seen[low]} (one file name on Windows): stop")
        names_seen[low] = row["name"]
    os.makedirs(ptex, exist_ok=True)
    for path, data in new_tex:
        open(path, "wb").write(data)
    os.makedirs(os.path.join(OUT, "pets"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "icons", "pet"), exist_ok=True)
    n_icons = 0
    for path, obj in files.items():
        if path.endswith(".json"):
            json.dump(obj, open(path, "w", encoding="utf-8"), separators=(",", ":"))
        elif not keep_upscaled(path, obj):                 # its upscale stays (wardrobe_icons_upscale.py)
            obj.save(path, "WEBP", lossless=True)
            n_icons += 1
    ipath = os.path.join(OUT, "pets", "index.json")
    if only is not None and os.path.exists(ipath):
        old = [x for x in json.load(open(ipath, encoding="utf-8")) if x["name"] not in {r_["name"] for r_ in index}]
        index = old + index
    index.sort(key=lambda x: x["name"].lower())
    open(ipath, "w", encoding="utf-8", newline="\n").write("[\n" + ",\n".join(json.dumps(x, ensure_ascii=False, separators=(",", ":")) for x in index) + "\n]\n")
    if only is None:                                     # a full run: drop pet files no row names any more
        keep_files = {os.path.basename(x["file"]) for x in index} | {"index.json"}
        for f in sorted(os.listdir(os.path.join(OUT, "pets"))):
            if f not in keep_files:
                os.remove(os.path.join(OUT, "pets", f))
                print(f"removed stale pets/{f}")

    # ---- report ----
    done = [x for x in index if only is None or x["name"].lower() in only]
    print(f"\npets written: {len(done)} ({sum(x['tto'] for x in done)} TTO, {sum(not x['tto'] for x in done)} BB); "
          f"index {len(index)} rows; textures {len(new_tex)} new, {same_tex} already in props/tex; icons {n_icons} written")
    print(f"with particles (not extracted): {len(particles)}", *particles, sep="\n  ")
    print(f"with no idle clip (the prefab pose): {len(no_clip)}", *no_clip, sep="\n  ")
    print(f"skipped: {len(skipped)}", *skipped, sep="\n  ")
    print(f"level guessed (TTO's own families, Lv 9): {sorted(x['name'] for x in done if x.get('level_guess'))}")
    print("TTO pets' shaders -> the page:", *[f"{s} -> {k}: {', '.join(sorted(p))}" for (s, k), p in sorted(shader_log.items(), key=str)], sep="\n  ")
    print(f"prefab roots with a transform of their own, written as identity (Instantiate + localScale replace it): "
          f"{len(moved_roots)}: {', '.join(moved_roots)}")
    if notes:
        print(f"notes: {len(notes)}", *notes, sep="\n  ")
    print("done", os.path.join(OUT, "pets"))


if __name__ == "__main__":
    main()
