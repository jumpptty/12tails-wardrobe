"""Read only: Resources container keys under sheep/voices and sheep/sounds matching argv[1] (regex).
  uv run --no-project --with UnityPy python -I checks/fx_sheep_research/cast_b/containers.py seal"""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "pipeline"))
import wardrobe_fx as W  # noqa: E402
g = W.Game()
pat = re.compile(sys.argv[1], re.I)
for k in sorted(g.container):
    if k.startswith("gameassets/characters/heroes/sheep/") and pat.search(k):
        print(k)
