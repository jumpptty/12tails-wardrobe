"""Read-only probe: novaFlare (the ManaVortex's prefab, outside the hero folder) and arcticEmperor (with an in-memory
layout for Penguin_arcticEmperor, its 8 public floats, Penguin_arcticEmperor.cs:225-246). Writes nothing."""
import json, os, sys
sys.path.insert(0, os.path.join(sys.argv[1], "pipeline"))
import wardrobe_fx as W
W.LAYOUTS["Penguin_arcticEmperor"] = [(n, "f") for n in ("MinAlpha", "MaxAlpha", "MinEmission", "MaxEmission",
                                                        "FadeDelay", "FadeEaseIn", "FadeMiddle", "FadeEaseOut")]
g = W.Game()
g.container["gameassets/characters/heroes/penguin/effects/novaflare"] = g.container["gameassets/characters/elementals/manavortex/effects/novaflare"]
for n in ("novaFlare", "arcticEmperor"):
    try:
        print(json.dumps({n: W.effect(g, "penguin", n, {}, {}, set())}, indent=1))
    except Exception as e:
        print(json.dumps({n: f"{type(e).__name__}: {e}"}))
