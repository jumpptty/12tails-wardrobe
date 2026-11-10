"""Read only: one line per node of each probed effect (probe.json holds several JSON objects back to back)."""
import json, sys
src = open(sys.argv[1], encoding="utf-8").read()
dec, i = json.JSONDecoder(), 0
while i < len(src):
    while i < len(src) and src[i].isspace(): i += 1
    if i >= len(src): break
    obj, i = dec.raw_decode(src, i)
    for name, fx in obj.items():
        print("==", name)
        for k, n in enumerate(fx.get("nodes", [])):
            bits = []
            for c in n["comps"]:
                t = c["type"]
                keep = {kk: c[kk] for kk in ("life", "afterLife", "followPosition", "followState", "effectRotationMode", "clip", "loop", "playOnAwake", "volume", "radius", "Life", "Delay", "repeatForever", "minSize", "maxSize", "minEnergy", "maxEnergy", "m_OneShot", "autodestruct", "EmissionTime", "Emission") if kk in c}
                bits.append(t + (json.dumps(keep) if keep else ""))
            print(f"  {k} {n['name']} p{n['parent']} pos{[round(v,3) for v in n['pos']]} rot{[round(v,3) for v in n['rot']]} sc{n['scale']}: " + "; ".join(bits))
        for kk in fx:
            if kk != "nodes": print("  +", kk, json.dumps(fx[kk])[:300])
