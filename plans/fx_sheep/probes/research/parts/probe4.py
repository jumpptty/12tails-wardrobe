"""Read-only: the curve paths and key spans of the Animation clips on the Sheep's AlphaTimer / Eden effects (which node
each clip moves, first / last key values). Writes nothing.
  uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I checks/fx_sheep_research/parts/probe4.py
"""
import importlib.util, os
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("wfx", os.path.join(HERE, "..", "..", "..", "pipeline", "wardrobe_fx.py"))
wfx = importlib.util.module_from_spec(spec); spec.loader.exec_module(wfx)
game = wfx.Game()
def r(v): return [round(v[k], 3) for k in ("x", "y", "z", "w") if k in v] if isinstance(v, dict) else round(v, 3)
for n in ["edenSanctuary", "divinityAxe", "divinitySpear", "divinitySword", "lullaby_ring", "soulOfArms", "sealOfAttack"]:
    root = game.obj(game.container[f"gameassets/characters/heroes/sheep/effects/{n.lower()}"], game.files["mainData"])
    def walk(go_obj):
        go = go_obj.read_typetree(); kids = []
        for comp in go["m_Component"]:
            c = game.obj(comp[1] if isinstance(comp, (list, tuple)) else comp.get("second"), go_obj.assets_file)
            if c is None: continue
            if c.type.name == "Transform": kids = c.read_typetree()["m_Children"]
            if c.type.name == "Animation":
                for a in c.read_typetree()["m_Animations"]:
                    ao = game.obj(a, c.assets_file)
                    if ao is None: continue
                    at = ao.read_typetree()
                    print(n, "on", go["m_Name"], "clip", at["m_Name"], "wrap", at.get("m_WrapMode"))
                    for grp in ("m_RotationCurves", "m_PositionCurves", "m_ScaleCurves"):
                        for cv in at.get(grp, []):
                            ks = cv["curve"]["m_Curve"]
                            print("   ", grp[2:-6], repr(cv["path"]), len(ks), "keys", ks[0]["time"], r(ks[0]["value"]), "->", round(ks[-1]["time"], 3), r(ks[-1]["value"]))
        for ch in kids:
            tro = game.obj(ch, go_obj.assets_file)
            if tro is not None: walk(game.obj(tro.read_typetree()["m_GameObject"], tro.assets_file))
    walk(root)
