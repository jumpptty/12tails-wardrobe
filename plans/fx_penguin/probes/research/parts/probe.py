"""Penguin parts research probe (read only; writes nothing in wardrobe/data). Run from the repo root:
  uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I checks/fx_penguin_research/parts/probe.py > checks/fx_penguin_research/parts/probe.txt
Patches the candidate LAYOUTS in memory, then for every Penguin effect in the inventory prints each node's comps
(compact) and every material's shader (built-in id or the game's shader name), so blends the page draws wrongly show up.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "pipeline"))
import wardrobe_fx as W

W.LAYOUTS.update({
    "Penguin_tornado": [("mLv", "i"), ("nPosition", "v3"), ("nVelocity", "v3")],
    "Penguin_typhoon": [("mLv", "i"), ("nPosition", "v3"), ("nVelocity", "v3")],
    "Penguin_arcticEmperor": [("MinAlpha", "f"), ("MaxAlpha", "f"), ("MinEmission", "f"), ("MaxEmission", "f"),
                              ("FadeDelay", "f"), ("FadeEaseIn", "f"), ("FadeMiddle", "f"), ("FadeEaseOut", "f")],
    "Penguin_iceBlock": [("mLife", "i"), ("mLv", "i")],
    "Penguin_cosmicFriday": [], "Penguin_nAttack": [],
})
SHADER = {}
orig = W.material
def material(game, pptr, base, mats, texs):
    name = orig(game, pptr, base, mats, texs)
    if name and name not in SHADER:
        o = game.obj(pptr, base); t = o.read_typetree(); sh = t["m_Shader"]
        own = o.assets_file
        ext = own.externals[sh["m_FileID"] - 1].path if sh["m_FileID"] else "own"
        SHADER[name] = (ext.split("/")[-1], sh["m_PathID"], mats[name]["blend"])
    return name
W.material = material

inv = json.load(open("plans/fx_inventory.json", encoding="utf-8"))
names = sys.argv[1].split(",") if len(sys.argv) > 1 else None
if names is None:
    names = sorted(inv["penguin"]["own"])
game = W.Game()
SKIP = ("Color1", "Color2", "Color3", "Color4", "Color5")
for n in names:
    mats, texs = {}, {}
    try:
        e = W.effect(game, "penguin", n, mats, texs, set())
    except Exception as ex:
        print(f"## {n}: {type(ex).__name__}: {ex}"); continue
    print(f"## {n}")
    for i, nd in enumerate(e["nodes"]):
        print(f"  [{i}] {nd['name']} parent={nd['parent']} pos={nd.get('pos')} rot={nd.get('rot')} scale={nd.get('scale')} mats={nd.get('mats')}")
        for c in nd["comps"]:
            d = {k: v for k, v in c.items() if k not in SKIP and not (isinstance(v, list) and len(v) > 12) and k not in ("pos", "nrm", "uv", "col", "idx", "tracks", "clips", "weights", "bind")}
            if c["type"] in ("SkinnedMeshRenderer", "StaticMesh", "Animation"):
                d = {"type": c["type"], **{k: (v if not isinstance(v, (list, dict)) or len(json.dumps(v)) < 200 else f"<{len(v)}>") for k, v in c.items() if k != "type"}}
            print("      ", json.dumps(d, default=str)[:900])
    for m, d in mats.items():
        print(f"    mat {m}: shader={SHADER.get(m)} tint={d['tint']} color={d['color']} emission={d['emission']} tex={d['tex']}")
