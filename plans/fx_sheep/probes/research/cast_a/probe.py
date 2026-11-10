"""Read only: per effect, its part types, EffectControl settings, AudioSources, Animation clips (nothing written).
  uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I checks/fx_sheep_research/cast_a/probe.py a,b"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "pipeline"))
import wardrobe_fx as W  # noqa: E402

g = W.Game()
for n in sys.argv[1].split(","):
    try:
        e = W.effect(g, "sheep", n, {}, {}, set())
    except Exception as ex:  # noqa: BLE001
        print(n, "ERROR", type(ex).__name__, ex)
        continue
    parts, ec, aud, anim = {}, [], [], []
    for nd in e["nodes"]:
        for c in nd["comps"]:
            t = c["type"]
            parts[t] = parts.get(t, 0) + 1
            if t == "EffectControl":
                ec.append((nd["name"], {k: c[k] for k in ("life", "afterLife", "followPosition", "followState", "effectRotationMode")}))
            elif t == "AudioSource":
                aud.append((nd["name"], c["clip"], c["volume"], c["playOnAwake"], c["loop"]))
            elif t == "Animation":
                anim.append((nd["name"], {k: v for k, v in c.items() if k not in ("type", "tracks", "curves")}))
    print(f"{n}: nodes {len(e['nodes'])}, root pos {e['nodes'][0].get('pos')} scale {e['nodes'][0].get('scale')}")
    print("   parts", parts)
    for x in ec:
        print("   EC", x)
    for x in aud:
        print("   audio", x)
    for x in anim:
        print("   anim", str(x)[:300])
