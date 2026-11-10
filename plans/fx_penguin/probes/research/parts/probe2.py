"""Penguin parts probe 2 (read only): Rigidbody / Collider / AudioSource fields and each Animation clip's length, wrap
and what it moves (first and last key per track), for the effects blocked on a Penguin script. From the repo root:
  uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I checks/fx_penguin_research/parts/probe2.py > checks/fx_penguin_research/parts/probe2.txt
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "pipeline"))
import wardrobe_fx as W
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
W.LAYOUTS.update({
    "Penguin_tornado": [("mLv", "i"), ("nPosition", "v3"), ("nVelocity", "v3")],
    "Penguin_typhoon": [("mLv", "i"), ("nPosition", "v3"), ("nVelocity", "v3")],
    "Penguin_arcticEmperor": [("MinAlpha", "f"), ("MaxAlpha", "f"), ("MinEmission", "f"), ("MaxEmission", "f"),
                              ("FadeDelay", "f"), ("FadeEaseIn", "f"), ("FadeMiddle", "f"), ("FadeEaseOut", "f")],
    "Penguin_iceBlock": [("mLife", "i"), ("mLv", "i")],
    "Penguin_cosmicFriday": [], "Penguin_nAttack": [],
})
NAMES = sys.argv[1].split(",") if len(sys.argv) > 1 else \
    "tornado1,tornado2,tornado3,typhoon1,typhoon2,typhoon3,arcticEmperor,cosmicFriday,iceBlock,spreadShot_fire,tornado_ring,tornado_hit".split(",")
game = W.Game()
for n in NAMES:
    key = f"gameassets/characters/heroes/penguin/effects/{n.lower()}"
    root = game.obj(game.container[key], game.files["mainData"])
    print(f"## {n}")
    def walk(go_obj, depth):
        go = go_obj.read_typetree()
        for comp in go["m_Component"]:
            c = game.obj(comp[1] if isinstance(comp, (list, tuple)) else comp.get("second"), go_obj.assets_file)
            if c is None: continue
            ty = c.type.name
            if ty in ("Rigidbody", "SphereCollider", "BoxCollider", "CapsuleCollider", "MeshCollider", "AudioSource"):
                t = c.read_typetree()
                keep = {k: v for k, v in t.items() if k not in ("m_GameObject", "m_audioClip", "rolloffCustomCurve", "panLevelCustomCurve", "spreadCustomCurve", "m_Mesh")}
                print("  " * depth, go["m_Name"], ty, json.dumps(keep, default=str)[:600])
        tr = next(game.obj(c[1] if isinstance(c, (list, tuple)) else c.get("second"), go_obj.assets_file) for c in go["m_Component"]
                  if game.obj(c[1] if isinstance(c, (list, tuple)) else c.get("second"), go_obj.assets_file).type.name == "Transform")
        for ch in tr.read_typetree()["m_Children"]:
            tro = game.obj(ch, go_obj.assets_file)
            walk(game.obj(tro.read_typetree()["m_GameObject"], tro.assets_file), depth + 1)
    walk(root, 1)
    e = W.effect(game, "penguin", n, {}, {}, set())
    for i, nd in enumerate(e["nodes"]):
        for c in nd["comps"]:
            if c["type"] == "Animation":
                print(f"  Animation on [{i}] {nd['name']}: default {c['clip']} play {c['play']} wrap {c['wrap']}")
                for cn, cd in c["clips"].items():
                    print(f"    clip {cn}: len {cd['len']} wrap {cd['wrap']}")
                    for ni, tk in cd["tracks"].items():
                        for kind in ("p", "q", "s"):
                            ks = tk.get(kind)
                            if ks:
                                dim = 4 if kind == "q" else 3
                                print(f"      [{ni}] {tk['path']} {kind}: {len(ks)} keys, t {ks[0][0]}..{ks[-1][0]}, first {ks[0][1:1+dim]}, last {ks[-1][1:1+dim]}")
