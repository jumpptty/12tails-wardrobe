"""Read-only probe that skips MonoBehaviours with no layout (AlphaTimer), so the rest of an effect (its EffectControl life)
can be read. Writes nothing. Run from the repo root:
  uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I checks/fx_sheep_research/verify/probe_skipunknown.py sheep soulOfArms,lullaby_ring
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "pipeline"))
import wardrobe_fx as W


orig = W.decode
def decode(raw, layout, off):
    try:
        return orig(raw, layout, off)
    except ValueError as e:
        return {"undecoded": str(e)}
W.decode = decode
for k in ("AlphaTimer",):
    W.LAYOUTS.setdefault(k, [])

cls, names = sys.argv[1], sys.argv[2].split(",")
game = W.Game()
for n in names:
    print(json.dumps({n: W.effect(game, cls, n, {}, {}, set())}, default=str)[:20000])
