"""Per prefab: EffectControl, each node's component types (PS modes / mesh / loop, AudioSource clip), and every component
type with the prefabs using it. py -3 -I compact.py probe.json"""
import json, sys, collections
d = json.load(open(sys.argv[1], encoding="utf-8")); use = collections.defaultdict(set)
for name, e in d["effects"].items():
    out = []
    for i, n in enumerate(e["nodes"]):
        cs = []
        for c in n["comps"]:
            t = c["type"]; use[t].add(name[4:])
            if t == "EffectControl": cs.append(f"EC {c['life']}+{c['afterLife']}" + (" fP" if c['followPosition'] else "") + (" fS" if c['followState'] else ""))
            elif t == "ParticleSystem":
                mods = [k[:-6] for k, v in c.items() if k.endswith("Module") and isinstance(v, dict) and v.get("enabled") not in (False, 0)]
                cs.append(f"PS {c.get('lengthInSec')}s{' loop' if c.get('looping') else ''} sim{c.get('moveWithTransform')} [{','.join(m for m in mods if m not in ('Initial','Shape','Emission'))}]")
            elif t == "ParticleSystemRenderer":
                cs.append(f"PSR m{c.get('m_RenderMode')}" + (f" mesh={c['m_Mesh'].get('name') if isinstance(c.get('m_Mesh'), dict) else c.get('m_Mesh')}" if c.get('m_Mesh') else ""))
            elif t == "AudioSource": cs.append(f"AS {c.get('clip')} v{c.get('volume')}{' loop' if c.get('loop') else ''}{'' if c.get('playOnAwake') else ' NOpoa'}")
            elif t in ("Transform", "MeshFilter", "MeshRenderer"): continue
            elif t == "StaticMesh": cs.append(f"StaticMesh {c.get('name')} {c.get('verts')}v")
            else: cs.append(t)
        flags = ("" if n.get("active", True) else " INACTIVE")
        out.append(f"{n['name']}{flags}: " + "; ".join(cs))
    print(f"== {name[4:]}: " + " | ".join(out))
print("\nTYPES:")
for t in sorted(use): print(f"  {t}: {', '.join(sorted(use[t]))}")
print("\ntextures", d["textures"]); print("sounds", d["sounds"])
shaders = collections.Counter(m.get("shader") or m.get("blend") for m in d["materials"].values()); print("shaders/blends", dict(shaders))
