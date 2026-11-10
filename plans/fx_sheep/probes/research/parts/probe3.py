"""Read-only: the projectiles' legacy emitter flags (world space, min range, emitter velocity scale) and their animator
force; the SphereCollider radii. Writes nothing.
  uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I checks/fx_sheep_research/parts/probe3.py
"""
import importlib.util, os
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("wfx", os.path.join(HERE, "..", "..", "..", "pipeline", "wardrobe_fx.py"))
wfx = importlib.util.module_from_spec(spec); spec.loader.exec_module(wfx)
game = wfx.Game()
for n in ["nAttack", "cAttack", "homingLight"]:
    root = game.obj(game.container[f"gameassets/characters/heroes/sheep/effects/{n.lower()}"], game.files["mainData"])
    def walk(go_obj):
        go = go_obj.read_typetree(); kids = []
        for comp in go["m_Component"]:
            c = game.obj(comp[1] if isinstance(comp, (list, tuple)) else comp.get("second"), go_obj.assets_file)
            if c is None: continue
            if c.type.name == "Transform": kids = c.read_typetree()["m_Children"]
            if c.type.name == "EllipsoidParticleEmitter":
                t = c.read_typetree()
                print(n, go["m_Name"], {k: t[k] for k in t if k in ("Simulate in Worldspace?", "m_MinEmitterRange", "emitterVelocityScale", "m_OneShot", "minEmission", "maxEmission", "minEnergy", "maxEnergy")})
            if c.type.name == "ParticleAnimator":
                t = c.read_typetree(); print("   animator", {k: t[k] for k in t if k in ("force", "rndForce", "sizeGrow", "damping", "autodestruct")})
        for ch in kids:
            tro = game.obj(ch, go_obj.assets_file)
            if tro is not None: walk(game.obj(tro.read_typetree()["m_GameObject"], tro.assets_file))
    walk(root)
