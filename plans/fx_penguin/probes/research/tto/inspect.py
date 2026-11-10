"""Print chosen details of the probe: SkinnedMeshRenderer comps, mesh-particle meshes, non-legacy materials, AudioSources,
LineRenderer / TrailRendererModern keys. py -3 -I inspect.py probe.json"""
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
for name, e in d["effects"].items():
    for i, n in enumerate(e["nodes"]):
        for c in n["comps"]:
            t = c["type"]
            if t == "SkinnedMeshRenderer":
                print(name, i, n["name"], "SMR", {k: (v if len(json.dumps(v)) < 200 else f"<{len(json.dumps(v))} chars>") for k, v in c.items()})
            if t == "ParticleSystemRenderer" and c.get("m_RenderMode") == 4:
                m = c.get("mesh") or c.get("m_Mesh")
                print(name, i, n["name"], "PSR4 mesh:", (m.get("name"), m.get("verts")) if isinstance(m, dict) else m)
            if t == "LineRenderer":
                print(name, i, n["name"], "LR", {k: c[k] for k in c if k in ("m_Positions", "m_UseWorldSpace", "m_Loop", "m_Enabled")}, "params:", list(c.get("m_Parameters", {}).keys())[:12])
            if t == "StaticMesh":
                print(name, i, n["name"], "StaticMesh", c.get("name"), c.get("verts"), "sub", c.get("sub"))
for k, m in d["materials"].items():
    if m.get("shader") or m.get("blend") in ("opaque",):
        print("MAT", k, {x: m[x] for x in m if x != "props"}, "props:", list((m.get("props") or {}).keys()))
