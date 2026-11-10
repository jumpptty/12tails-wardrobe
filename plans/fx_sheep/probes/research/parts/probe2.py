"""Read-only: wardrobe_fx.effect() on the 13 Sheep effects with candidate layouts patched in (in memory), printing each
effect's materials (blend / tint / color) and the comps the page would get; and shader 6:77's name. Writes nothing.
  uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I checks/fx_sheep_research/parts/probe2.py
"""
import importlib.util, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("wfx", os.path.join(HERE, "..", "..", "..", "pipeline", "wardrobe_fx.py"))
wfx = importlib.util.module_from_spec(spec); spec.loader.exec_module(wfx)
wfx.LAYOUTS.update({
    "AlphaTimer": [("MinAlpha", "f"), ("MaxAlpha", "f"), ("FadeDelay", "f"), ("FadeEaseIn", "f"), ("FadeMiddle", "f"),
                   ("FadeEaseOut", "f"), ("eraseShadow", "b"), ("repeat", "b"), ("endDestroy", "b")],
    "ProjectileControl": [("life", "f"), ("dmg", "f"), ("velocity", "v3"), ("OwnerID", "i"), ("isInitialized", "b"), ("isDestroyed", "b")],
    "Sheep_seal": [("mSealType", "i")],
})
game = wfx.Game()
for n in ["nAttack", "cAttack", "homingLight", "divinityAxe", "divinitySpear", "divinitySword", "edenSanctuary", "lullaby_ring",
          "soulOfArms", "sealOfAttack", "sealOfDefense", "sealOfEarth", "sealOfHeaven"]:
    mats, texs = {}, {}
    try:
        e = wfx.effect(game, "sheep", n, mats, texs, set())
    except Exception as ex:
        print(n, "FAIL", ex); continue
    print("==", n)
    for i, nd in enumerate(e["nodes"]):
        ts = [c["type"] for c in nd["comps"]]
        extra = {c["type"]: {k: v for k, v in c.items() if k != "type" and k != "clips"} for c in nd["comps"] if c["type"] in ("Animation", "SkinnedMeshRenderer", "StaticMesh")}
        for c in nd["comps"]:
            if c["type"] == "Animation": extra["Animation"]["clipnames"] = list(c.get("clips", {}))
            if c["type"] == "SkinnedMeshRenderer": extra["SkinnedMeshRenderer"] = {k: (v if not isinstance(v, (list, dict)) or len(json.dumps(v)) < 80 else "...") for k, v in c.items()}
            if c["type"] == "StaticMesh": extra["StaticMesh"] = {k: (v if not isinstance(v, (list, dict)) or len(json.dumps(v)) < 80 else "...") for k, v in c.items()}
        print(f"  [{i}] {nd['name']} parent {nd['parent']} mats {nd.get('mats')} {ts}", json.dumps(extra)[:400] if extra else "")
    print("  mats", json.dumps(mats))
# the game's shader behind divinitySpear's material: its source's Properties
md = game.files
for n in ["divinitySpear"]:
    key = f"gameassets/characters/heroes/sheep/effects/{n.lower()}"
