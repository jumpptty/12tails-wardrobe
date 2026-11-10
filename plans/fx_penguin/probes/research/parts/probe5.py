"""Read-only probe (fx_penguin_research/parts): the settings of every Penguin effect that the page may draw differently
from the game: legacy particle fields the page doesn't model (tangentVelocity, emitterVelocityScale, rotation axes,
camera velocity scale), renderer modes, the mesh emitters' mode enums, EffectControl's rotation mode / follow flags,
and Animation on the root (the page never poses node 0). Writes nothing but stdout.
  uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I checks/fx_penguin_research/parts/probe5.py
"""
import importlib.util, os
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("wfx", os.path.join(HERE, "..", "..", "..", "pipeline", "wardrobe_fx.py"))
wfx = importlib.util.module_from_spec(spec); spec.loader.exec_module(wfx)
spec2 = importlib.util.spec_from_file_location("lay", os.path.join(HERE, "layouts.py"))
lay = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(lay); wfx.LAYOUTS.update(lay.PENGUIN)
game = wfx.Game()
PRE = "gameassets/characters/heroes/penguin/effects/"
nz = lambda d: d and any(abs(d[k]) > 1e-6 for k in ("x", "y", "z"))
for k in sorted(game.container):
    if not k.startswith(PRE) or game.obj(game.container[k], game.files["mainData"]).type.name != "GameObject":
        continue
    n = k[len(PRE):]
    e = wfx.effect(game, "penguin", n, {}, {}, set())
    out = []
    for i, nd in enumerate(e["nodes"]):
        for c in nd["comps"]:
            t = c["type"]
            if t == "EllipsoidParticleEmitter":
                if nz(c.get("tangentVelocity")): out.append(f"{nd['name']}: tangentVelocity {c['tangentVelocity']}")
                if c.get("Simulate in Worldspace?") and c.get("emitterVelocityScale"): out.append(f"{nd['name']}: world, emitterVelocityScale {c['emitterVelocityScale']}")
                if c.get("m_OneShot"): out.append(f"{nd['name']}: oneShot")
            elif t == "ParticleAnimator":
                for f in ("worldRotationAxis", "localRotationAxis"):
                    if nz(c.get(f)): out.append(f"{nd['name']}: {f} {c[f]}")
            elif t == "ParticleRenderer":
                if c.get("m_StretchParticles") not in (0, None): out.append(f"{nd['name']}: render mode {c['m_StretchParticles']} length {c.get('m_LengthScale')} vel {c.get('m_VelocityScale')}")
                if c.get("m_CameraVelocityScale"): out.append(f"{nd['name']}: cameraVelocityScale {c['m_CameraVelocityScale']}")
                uva = c.get("UV Animation")
                if uva and (uva.get("x Tile", 1) > 1 or uva.get("y Tile", 1) > 1): out.append(f"{nd['name']}: UV tiles {uva}")
            elif t == "EffectControl":
                if c["effectRotationMode"] or c["followPosition"] or c["followState"] or any(c["velocity"]):
                    out.append(f"{nd['name']}{'' if nd['parent'] < 0 else ' (child)'}: EC life {c['life']}+{c['afterLife']} rotMode {c['effectRotationMode']} followPos {c['followPosition']} followState {c['followState']} vel {c['velocity']}")
            elif t == "ImageEmitter" and c["ImageEmitterMode"]: out.append(f"{nd['name']}: ImageEmitterMode {c['ImageEmitterMode']} world {c['useWorldSpace']}")
            elif t == "LineEmitter" and c["lineEmitterMode"]: out.append(f"{nd['name']}: lineEmitterMode {c['lineEmitterMode']}")
            elif t == "VortexEmitter": out.append(f"{nd['name']}: VortexEmitterMode {c['VortexEmitterMode']} alwaysUp {c['alwaysUp']}")
            elif t == "Animation" and nd["parent"] < 0:
                tracks0 = [cn for cn, cl in c.get("clips", {}).items() if "0" in cl.get("tracks", {})]
                out.append(f"{nd['name']} (root): Animation default {c.get('clip')} play {c.get('play')} clips {list(c.get('clips', {}))}" + (f"; ROOT ANIMATED in {tracks0}" if tracks0 else ""))
            elif t in ("TrailRenderer", "Light"): out.append(f"{nd['name']}: {t}")
    print("==", n, *(["   " + x for x in out] or ["   (nothing unusual)"]), sep="\n")
