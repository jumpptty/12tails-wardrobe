"""Summarise probe.json: per effect, its nodes' component types, EffectControl fields, AudioSource clips, Animation clips."""
import json, re, sys
txt = open(sys.argv[1], encoding="utf-8").read()
dec = json.JSONDecoder(); i = 0
while i < len(txt):
    while i < len(txt) and txt[i].isspace(): i += 1
    if i >= len(txt): break
    obj, i = dec.raw_decode(txt, i)
    for name, e in obj.items():
        print("==", name)
        if not isinstance(e, dict): print("  ", e); continue
        for k in e:
            if k != "nodes": print("  key", k, str(e[k])[:200])
        for n in e.get("nodes", []):
            parts = []
            for c in n.get("comps", []):
                t = c.get("type")
                if t == "EffectControl":
                    parts.append("EC(" + ", ".join(f"{k}={c.get(k)}" for k in ("life", "afterLife", "followState", "followPosition", "effectRotationMode") ) + ")")
                elif t == "AudioSource":
                    parts.append("Audio(" + ", ".join(f"{k}={v}" for k, v in c.items() if k != "type") [:150] + ")")
                elif t == "Animation":
                    parts.append(f"Anim(play={c.get('play')}, clip={c.get('clip')}, clips={ {k: v.get('len') for k, v in c.get('clips', {}).items()} })")
                else:
                    extra = ""
                    for k in ("Life", "Delay", "repeatForever", "EmissionTime"):
                        if k in c: extra += f" {k}={c[k]}"
                    parts.append(t + extra)
            print(f"  [{n.get('name')} p={n.get('parent')} pos={n.get('pos')} rot={n.get('rot')} sc={n.get('scale')}]", "; ".join(parts))
