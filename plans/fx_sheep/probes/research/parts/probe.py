"""Read-only probe (fx_sheep_research/parts): the 13 Sheep effects that need a missing part, with candidate layouts for
AlphaTimer / ProjectileControl / Sheep_seal patched in, every other component type listed (physics too), the raw field
bytes of each new script, and the Animation clips' names / lengths. Writes nothing but stdout.
  uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I checks/fx_sheep_research/parts/probe.py
"""
import importlib.util, json, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("wfx", os.path.join(HERE, "..", "..", "..", "pipeline", "wardrobe_fx.py"))
wfx = importlib.util.module_from_spec(spec); spec.loader.exec_module(wfx)
NEW = {
    # AlphaTimer.cs:378-402
    "AlphaTimer": [("MinAlpha", "f"), ("MaxAlpha", "f"), ("FadeDelay", "f"), ("FadeEaseIn", "f"), ("FadeMiddle", "f"),
                   ("FadeEaseOut", "f"), ("eraseShadow", "b"), ("repeat", "b"), ("endDestroy", "b")],
    # ProjectileControl.cs:72-87
    "ProjectileControl": [("life", "f"), ("dmg", "f"), ("velocity", "v3"), ("OwnerID", "i"), ("isInitialized", "b"),
                          ("isDestroyed", "b")],
    "Sheep_seal": [("mSealType", "i")],          # Sheep_seal.cs:348
}
wfx.LAYOUTS.update(NEW)
NAMES = sys.argv[1].split(",") if len(sys.argv) > 1 else ["nAttack", "cAttack", "homingLight", "divinityAxe", "divinitySpear",
         "divinitySword", "edenSanctuary", "lullaby_ring", "soulOfArms", "sealOfAttack", "sealOfDefense", "sealOfEarth", "sealOfHeaven"]
game = wfx.Game()
for name in NAMES:
    print("=" * 20, name)
    key = f"gameassets/characters/heroes/sheep/effects/{name.lower()}"
    root = game.obj(game.container[key], game.files["mainData"])
    def walk(go_obj, depth):
        go = go_obj.read_typetree()
        print("  " * depth + "node", go["m_Name"], "layer", go.get("m_Layer"), "active", go.get("m_IsActive"))
        kids = []
        for comp in go["m_Component"]:
            c = game.obj(comp[1] if isinstance(comp, (list, tuple)) else comp.get("second"), go_obj.assets_file)
            if c is None: continue
            ty = c.type.name
            pad = "  " * depth + "  - "
            if ty == "Transform":
                t = c.read_typetree(); kids = t["m_Children"]
                print(pad + "Transform", {k: t[k] for k in ("m_LocalPosition", "m_LocalRotation", "m_LocalScale")})
            elif ty == "MonoBehaviour":
                raw = c.get_raw_data(); sn = game.script_name(raw, c.assets_file); h = wfx.header_len(raw)
                lay = wfx.LAYOUTS.get(sn)
                body = raw[h:]
                dec = None
                if lay:
                    try: dec = wfx.decode(raw, lay, h)
                    except Exception as e: dec = f"DECODE FAIL {e}"
                print(pad + f"Mono {sn} ({len(body)} B)", dec if dec is not None else "", "" if lay else body.hex())
            elif ty in ("Rigidbody", "SphereCollider", "BoxCollider", "CapsuleCollider", "MeshCollider", "Light",
                        "EllipsoidParticleEmitter", "ParticleAnimator", "AudioSource"):
                t = c.read_typetree()
                keep = {k: v for k, v in t.items() if k not in ("m_GameObject",)}
                if ty == "EllipsoidParticleEmitter":
                    keep = {k: keep[k] for k in keep if k in ("enabled", "m_Enabled", "m_Emit", "minSize", "maxSize", "minEnergy", "maxEnergy", "minEmission", "maxEmission", "m_OneShot", "m_UseWorldSpace", "worldVelocity", "localVelocity", "rndVelocity", "emitterVelocityScale", "tangentVelocity", "m_Ellipsoid")}
                if ty == "ParticleAnimator":
                    keep = {k: keep[k] for k in keep if k in ("autodestruct", "Does Animate Color?", "sizeGrow", "damping")}
                print(pad + ty, json.dumps(keep, default=str)[:600])
            elif ty in ("MeshRenderer", "ParticleRenderer", "TrailRenderer", "SkinnedMeshRenderer"):
                t = c.read_typetree()
                ms = []
                for m in t["m_Materials"]:
                    mo = game.obj(m, c.assets_file)
                    if mo is not None:
                        mt = mo.read_typetree(); props = mt["m_SavedProperties"]
                        cols = {(k["name"] if isinstance(k, dict) else k): [round(x, 3) for x in (v["r"], v["g"], v["b"], v["a"])] for k, v in props["m_Colors"]}
                        sh = mt["m_Shader"]
                        ms.append((mt["m_Name"], f"shader {sh['m_FileID']}:{sh['m_PathID']}", cols))
                print(pad + ty, "enabled", t.get("m_Enabled"), ms)
            elif ty == "Animation":
                t = c.read_typetree(); clips = []
                for a in t["m_Animations"]:
                    ao = game.obj(a, c.assets_file)
                    if ao is not None:
                        at = ao.read_typetree()
                        nrot = len(at.get("m_RotationCurves", [])); npos = len(at.get("m_PositionCurves", [])); nsc = len(at.get("m_ScaleCurves", [])); nfl = len(at.get("m_FloatCurves", []))
                        ln = 0
                        for grp in ("m_RotationCurves", "m_PositionCurves", "m_ScaleCurves", "m_FloatCurves"):
                            for cv in at.get(grp, []):
                                ks = cv["curve"]["m_Curve"]
                                if ks: ln = max(ln, ks[-1]["time"])
                        fl = [(cv.get("attribute"), cv.get("path")) for cv in at.get("m_FloatCurves", [])]
                        clips.append((at["m_Name"], f"len {ln:.3f}", f"wrap {at.get('m_WrapMode')}", f"rot {nrot} pos {npos} scale {nsc} float {nfl}", fl[:6], f"events {len(at.get('m_Events', []))}"))
                do = game.obj(t["m_Animation"], c.assets_file) if t["m_Animation"]["m_PathID"] else None
                print(pad + "Animation default", do.read_typetree()["m_Name"] if do else None, "play", t.get("m_PlayAutomatically"), "wrap", t.get("m_WrapMode"), clips)
            else:
                print(pad + ty)
        for ch in kids:
            tro = game.obj(ch, go_obj.assets_file)
            if tro is not None:
                walk(game.obj(tro.read_typetree()["m_GameObject"], tro.assets_file), depth + 1)
    walk(root, 0)
