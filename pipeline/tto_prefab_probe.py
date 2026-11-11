"""Print a TTO prefab's node tree as the game holds it: each node's local scale, its mesh (vertex count, bounds) and
materials' textures (2026-11-11: checking the Sheep's halloweenLantern and the Bat's halloweenWand against the TTO
patch of 2026-11-07). Reads decrypted bundles (the Bible's tools/bundle_decrypt.js) and the catalog that lists them.
  uv run --no-project --with UnityPy python -I pipeline/tto_prefab_probe.py <dec folder> <catalog.bin> <address> [<address> ...]
  address = the catalog key, e.g. gameassets/characters/heroes/bat/weapons/halloweenwand"""
import os
import subprocess
import sys

import UnityPy

DEC, CAT, ADDRS = sys.argv[1], sys.argv[2], sys.argv[3:]
BIBLE = next((p for p in (r"D:\12tails", r"C:\Users\Jump\Desktop\12tails") if os.path.isdir(p)), r"D:\12tails")
TOOL = os.path.join(BIBLE, "DecompiledSource_TTO_2026-11-02", "tools", "aa_catalog.py")
rows = {}
for a in ADDRS:
    out = subprocess.run([sys.executable, "-P", TOOL, CAT, "--grep", a + "$"], capture_output=True, text=True,
                         encoding="utf-8", check=True).stdout
    for line in out.splitlines():
        p = line.split("\t")
        if len(p) >= 4 and p[1].endswith("GameObject") and p[0].lower() == a.lower():
            rows[a] = (p[2], p[3].split())
bundles = sorted({b for _, bs in rows.values() for b in bs if os.path.exists(os.path.join(DEC, b))})
env = UnityPy.load(*[os.path.join(DEC, b) for b in bundles])
container = dict(env.container.items())
P = lambda c: c.component if hasattr(c, "component") else c[1]

for a, (iid, _) in rows.items():
    obj = container.get(iid)
    print("==", a, "(not in the loaded bundles)" if obj is None else "")
    if obj is None:
        continue

    def walk(tr, depth):
        g = tr.m_GameObject.read()
        s, q, p = tr.m_LocalScale, tr.m_LocalRotation, tr.m_LocalPosition
        line = f"{'  ' * depth}{g.m_Name}  p=({p.x:.3f},{p.y:.3f},{p.z:.3f}) s=({s.x:.3f},{s.y:.3f},{s.z:.3f}) q=({q.x:.2f},{q.y:.2f},{q.z:.2f},{q.w:.2f})"
        for c in g.m_Component:
            t = P(c).type.name
            if t == "MeshFilter":
                m = P(c).read().m_Mesh.read()
                b = m.m_LocalAABB
                line += f"\n{'  ' * depth}  mesh {m.m_Name}: {m.m_VertexData.m_VertexCount} verts, size ({2 * b.m_Extent.x:.3f},{2 * b.m_Extent.y:.3f},{2 * b.m_Extent.z:.3f}) centre ({b.m_Center.x:.3f},{b.m_Center.y:.3f},{b.m_Center.z:.3f})"
            elif t in ("MeshRenderer", "SkinnedMeshRenderer"):
                r = P(c).read()
                texs = []
                for mp in r.m_Materials:
                    try:
                        mat = mp.read()
                        tx = [v.m_Texture.read().m_Name for k, v in mat.m_SavedProperties.m_TexEnvs if v.m_Texture.m_PathID]
                        texs.append(f"{mat.m_Name}{tx}")
                    except Exception as e:
                        texs.append(f"? {type(e).__name__}")
                line += f"\n{'  ' * depth}  {t}: {texs}"
            elif t == "ParticleSystem":
                line += "  [particles]"
        print(line)
        for ch in tr.m_Children:
            walk(ch.read(), depth + 1)

    go = obj.read()
    tr = next(P(c).read() for c in go.m_Component if P(c).type.name == "Transform")
    walk(tr, 0)
