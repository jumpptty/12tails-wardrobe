import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
for name, e in d["effects"].items():
    print("==", name)
    for i, n in enumerate(e["nodes"]):
        cs = []
        for c in n["comps"]:
            t = c["type"]
            if t == "EffectControl":
                cs.append(f"EC(life={c['life']} after={c['afterLife']} fP={c['followPosition']} fS={c['followState']} vel={c.get('velocity')})")
            elif t == "ParticleSystem":
                mods = [k for k, v in c.items() if k.endswith("Module") and isinstance(v, dict) and v.get("enabled") not in (False, 0)]
                cs.append(f"PS(dur={c.get('lengthInSec')} loop={c.get('looping')} sim={c.get('moveWithTransform')} mods={','.join(m.replace('Module','') for m in mods)})")
            elif t == "ParticleSystemRenderer":
                cs.append(f"PSR(mode={c.get('m_RenderMode')} align={c.get('m_RenderAlignment')} mesh={c.get('m_Mesh')} mats={c.get('m_Materials')})")
            elif t == "AudioSource":
                cs.append(f"AS(clip={c.get('clip')} vol={c.get('volume')} poa={c.get('playOnAwake')} loop={c.get('loop')})")
            elif t == "MeshFilter":
                cs.append(f"MF({c.get('m_Mesh')})")
            elif t == "MeshRenderer":
                cs.append(f"MR({c.get('m_Materials')})")
            elif t in ("Transform",):
                pass
            else:
                keys = [k for k in c if k != "type"]
                cs.append(f"{t}{{{', '.join(keys[:30])}}}")
        print(f"  [{i}] {n['name']} p={n['parent']} pos={n.get('pos')} rot={n.get('rot')} sc={n.get('scale')} {'INACTIVE ' if n.get('active') is False else ''}" + " | ".join(cs))
print("materials", json.dumps(d["materials"], indent=0)[:6000])
print("textures", d["textures"]); print("sounds", d["sounds"])
