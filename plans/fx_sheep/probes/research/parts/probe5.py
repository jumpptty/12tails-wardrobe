"""Read-only: the AudioSource clips the 13 Sheep effects play themselves (name, loop), and whether that name is in the
rip's sheep voices/ and / or sounds/ folders (a collision = the same name in both). Writes nothing.
  uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I checks/fx_sheep_research/parts/probe5.py
"""
import importlib.util, os
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("wfx", os.path.join(HERE, "..", "..", "..", "pipeline", "wardrobe_fx.py"))
wfx = importlib.util.module_from_spec(spec); spec.loader.exec_module(wfx)
wfx.LAYOUTS.update({"AlphaTimer": [("a", "f")] * 6 + [("b1", "b"), ("b2", "b"), ("b3", "b")],
                    "ProjectileControl": [("l", "f"), ("d", "f"), ("v", "v3"), ("o", "i"), ("i", "b"), ("x", "b")], "Sheep_seal": [("t", "i")]})
game = wfx.Game()
base = os.path.join(wfx.RIP, "characters", "heroes", "sheep")
for n in ["nAttack", "cAttack", "homingLight", "divinityAxe", "divinitySpear", "divinitySword", "edenSanctuary", "lullaby_ring",
          "soulOfArms", "sealOfAttack", "sealOfDefense", "sealOfEarth", "sealOfHeaven"]:
    e = wfx.effect(game, "sheep", n, {}, {}, set())
    for nd in e["nodes"]:
        for c in nd["comps"]:
            if c["type"] == "AudioSource":
                inv = os.path.exists(os.path.join(base, "voices", c["clip"] + ".wav")); ins = os.path.exists(os.path.join(base, "sounds", c["clip"] + ".wav"))
                print(n, nd["name"], "plays", c["clip"], "loop", c["loop"], "vol", c["volume"], "| voices/" if inv else "", "| sounds/" if ins else "", "| found by rip_wav:", wfx.rip_wav("sheep", c["clip"]))
