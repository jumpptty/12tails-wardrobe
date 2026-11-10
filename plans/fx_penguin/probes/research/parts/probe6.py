"""Read-only probe (fx_penguin_research/parts): for every hero class's effects (the Resources effects folders), which
use a material the page draws through a fallback: the game's own shaders other than FX/Phoenix and FX/DistortGlass, and
Unity built-ins outside wardrobe_fx.BUILTIN_BLEND (the extractor writes those as "add"; their path ID is re-read here).
Prints shader -> class/effect/material. Writes nothing.
  uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I checks/fx_penguin_research/parts/probe6.py
"""
import collections, importlib.util, os
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("wfx", os.path.join(HERE, "..", "..", "..", "pipeline", "wardrobe_fx.py"))
wfx = importlib.util.module_from_spec(spec); spec.loader.exec_module(wfx)
spec2 = importlib.util.spec_from_file_location("lay", os.path.join(HERE, "layouts.py"))
lay = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(lay); wfx.LAYOUTS.update(lay.PENGUIN)
game = wfx.Game()
orig = wfx.BUILTIN_BLEND
class Tag(dict):                       # BUILTIN_BLEND.get(id, "add") -> "builtin:<id>" for an id it lacks
    def get(self, k, d=None): return orig[k] if k in orig else f"builtin:{k}"
wfx.BUILTIN_BLEND = Tag()
uses = collections.defaultdict(list); fails = []
for k in sorted(game.container):
    parts = k.split("/")
    if len(parts) != 6 or parts[2] != "heroes" or parts[4] != "effects":
        continue
    o = game.obj(game.container[k], game.files["mainData"])
    if o is None or o.type.name != "GameObject":
        continue
    mats = {}
    try:
        wfx.effect(game, parts[3], parts[5], mats, {}, set())
    except Exception as e:      # noqa: BLE001 (no layout: its materials up to the failing node are still listed)
        fails.append(f"{parts[3]}/{parts[5]}: {e}")
    for m, v in mats.items():
        b = v["blend"]
        if b.startswith("builtin:") or (b.startswith("shader:") and b not in ("shader:FX/Phoenix", "shader:FX/DistortGlass")):
            uses[b].append(f"{parts[3]}/{parts[5]}:{m}")
for b, l in sorted(uses.items(), key=lambda x: -len(x[1])):
    print(f"{b}: {len(l)}  " + ", ".join(l))
print("effects not fully read (a script with no layout):", len(fails))
