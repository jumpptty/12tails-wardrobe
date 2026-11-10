"""Summarise wardrobe_fx.py --probe output (several JSON objects in one file): read only."""
import json, sys
txt = open(sys.argv[1], encoding="utf-8").read()
dec = json.JSONDecoder(); i = 0
while True:
    while i < len(txt) and txt[i] != "{": i += 1
    if i >= len(txt): break
    obj, i = dec.raw_decode(txt, i)
    for name, e in obj.items():
        if isinstance(e, str):
            print(name, "ERROR", e); continue
        types, extra = {}, []
        for n in e["nodes"]:
            for c in n["comps"]:
                t = c.get("type"); types[t] = types.get(t, 0) + 1
                if t == "EffectControl" and n["parent"] == -1:
                    extra.append("EC life %s after %s fPos %s fState %s rotMode %s" % (c["life"], c["afterLife"], c["followPosition"], c["followState"], c["effectRotationMode"]))
                if t == "AudioSource":
                    extra.append("audio %s" % {k: c.get(k) for k in c if k not in ("type",)})
                if t == "Animation":
                    extra.append("anim %s" % {k: c.get(k) for k in c if k not in ("type",)})
        root = e["nodes"][0]
        print(name, "rootrot", root["rot"], "scale", root["scale"], types)
        for x in extra: print("   ", str(x)[:400])
        for k in e:
            if k != "nodes": print("   key", k, str(e[k])[:200])
