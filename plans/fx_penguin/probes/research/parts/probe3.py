"""Read-only probe (fx_penguin_research/parts): the full wardrobe_fx.effect() JSON of the named Penguin effects (argv[1]),
with the Penguin candidate layouts patched in (the --probe of wardrobe_fx.py stops at a script with no layout).
  uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I checks/fx_penguin_research/parts/probe3.py tornado3,typhoon3
"""
import importlib.util, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("wfx", os.path.join(HERE, "..", "..", "..", "pipeline", "wardrobe_fx.py"))
wfx = importlib.util.module_from_spec(spec); spec.loader.exec_module(wfx)
spec2 = importlib.util.spec_from_file_location("probe2layouts", os.path.join(HERE, "layouts.py"))
lay = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(lay)
wfx.LAYOUTS.update(lay.PENGUIN)
game = wfx.Game()
for n in sys.argv[1].split(","):
    mats, sounds = {}, set()
    e = wfx.effect(game, "penguin", n, mats, {}, sounds)
    print(json.dumps({n: e, "materials": mats, "sounds": sorted(sounds)}, indent=1))
