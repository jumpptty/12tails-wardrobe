r"""ToT-only outfits for the LOCAL wardrobe (user 2026-11-07: "add ToT exclusive outfits models to the 3D LOCAL wardrobe
only first").

  py -3.10 pipeline/wardrobe_tot.py [--assets tot_assets/2026-11-07] [--only cat,sheep]

What is ToT-only: ToT's armor list equals TTO's minus Halloween and the two goddess outfits, so the only outfit TTO
lacks is ToT's **student set**, one per class (catalog `gameassets/characters/heroes/<cls>/student/`; ToT's code loads
`<Cls>_Student` as the armor, `<Cls>_Student_accessories` as the headpiece and `<Cls>_Student_weapons` as the weapon,
Chameleon `_bow` + `_arrow`, Whale `_lance` + `_shield`: string literals in TTOLegacyArmor / Accessory / Weapon
ResourceMap..cctor).

Input: `tot_assets/<date>/dec/*.bundle` = ToT's bundles for those paths and their dependencies, decrypted (TTOENC01:
per 64 KB block a 16-byte IV + AES-256-CBC, key = base64 const TTOBundleCipher.ClientKey; recipe and tool in
D:\12tails-assets-archive\tot-skins-2026-11-07\_tools\README.md, benc.js), and `student_resources.json` (the catalog rows
for those paths: key, bundle, address = the bundle's container key).

Output, per class, into wardrobe/data/<cls>/ (entries carry "tot": true; a re-run replaces them, so run this again after
wardrobe_data.py, which rewrites these files):
  o_student.bin + tex/student1..5.webp + outfits.json entry {"name": "student", "tot": true, "face": "quarter"}
  props_accessories.json + "studentHat": skinned to the hero's own bones ("heroSkin": the page binds it like an outfit)
  props_weapons.json + the student weapon(s) (plain nodes; a skinned one, Monkey's mic, baked into its prefab pose)
  ../props/tex/tot_<texture>.png for the hat and weapon materials.
wardrobe_publish.py keeps only items verified against BB's files, so none of this reaches the online copy.

Face: ToT's CharacterAppearance.TryBuildLegacyArmorMaterial (ToT GameAssembly 0x18138a070) loads
`heroes/<cls>/student/<Cls>_Student_<colour>` and blends the face overlay with TryBlendLegacySkinOverlay (0x181389a30):
a 512 x 512 sheet takes the 256 overlay on its top-left quarter; any other size (the student sheets are 1024) takes the
overlay stretched bilinearly over the top-left quarter (width / 2 x height / 2, alpha blend). So "face": "quarter".
"""
import json
import os
import struct
import sys

import numpy as np
import UnityPy
from PIL import Image
from UnityPy.helpers.MeshHelper import MeshHandler

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
argv = sys.argv[1:]
ASSETS = argv[argv.index("--assets") + 1] if "--assets" in argv else os.path.join(ROOT, "tot_assets", "2026-11-07")
ONLY = set(argv[argv.index("--only") + 1].lower().split(",")) if "--only" in argv else None
OUT = os.path.join(ROOT, "wardrobe", "data")
PTEX = os.path.join(ROOT, "props", "tex")
CLASSES = ["bat", "bison", "cat", "chameleon", "mole", "monkey", "panda", "penguin", "rabbit", "sheep", "whale", "wolf"]
WEAPON_PARTS = {"weapons": "studentWeapon", "bow": "studentBow", "arrow": "studentArrow", "lance": "studentLance",
                "shield": "studentShield"}

mp = lambda p: [-p[0], p[1], p[2]]
mq = lambda q: [q[0], -q[1], -q[2], q[3]]
P = lambda c: c.component if hasattr(c, "component") else c[1]

dec = os.path.join(ASSETS, "dec")
env = UnityPy.load(*[os.path.join(dec, f) for f in sorted(os.listdir(dec)) if f.endswith(".bundle")])
container = dict(env.container.items())
rows = json.load(open(os.path.join(ASSETS, "student_resources.json"), encoding="utf-8"))


def asset(cls, name, typ):
    """The student asset <name> of this class with Unity type <typ> (the catalog repeats a name per type)."""
    for r in rows:
        if r["key"].lower() == f"gameassets/characters/heroes/{cls}/student/{name}".lower():
            o = container.get(r["address"])
            if o is not None and o.type.name == typ:
                return o.read()
    return None


def transform(go):
    return next(P(c) for c in go.m_Component if P(c).type.name == "Transform").read()


def tree(go):
    """[(gameobject, transform, parent index)] depth first from the prefab root."""
    out = []

    def walk(tr, parent):
        k = len(out)
        out.append((tr.m_GameObject.read(), tr, parent))
        for ch in tr.m_Children:
            walk(ch.read(), k)
    walk(transform(go), -1)
    return out


def comp(go, typ):
    return next((P(c).read() for c in go.m_Component if P(c).type.name == typ), None)


def trs(tr):
    p, q, s = tr.m_LocalPosition, tr.m_LocalRotation, tr.m_LocalScale
    return [p.x, p.y, p.z], [q.x, q.y, q.z, q.w], [s.x, s.y, s.z]


def mat4(p, q, s):
    x, y, z, w = q
    R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                  [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                  [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
    M = np.eye(4)
    M[:3, :3] = R * np.array(s)
    M[:3, 3] = p
    return M


def handler(mesh):
    h = MeshHandler(mesh)
    h.process()
    return h


def winding(pos, nrm, tris):
    """Flip the triangle order where it disagrees with the stored normals (the mirror reverses every winding)."""
    if not nrm or not tris:
        return [(a, c, b) for a, b, c in tris]
    pos, nrm, t = np.array(pos), np.array(nrm), np.array(tris)
    cr = np.cross(pos[t[:, 1]] - pos[t[:, 0]], pos[t[:, 2]] - pos[t[:, 0]])
    agree = ((cr * (nrm[t[:, 0]] + nrm[t[:, 1]] + nrm[t[:, 2]])).sum(1) > 0).sum()
    return [tuple(x) for x in t[:, [0, 2, 1]]] if agree < len(t) / 2 else [tuple(x) for x in t]


def arrays(h, pos=None, nrm=None):
    """A mesh in three.js space for the page's prop format: x mirrored, triangles per submesh (material slot)."""
    pos = [mp(v) for v in (h.m_Vertices if pos is None else pos)]
    nrm = [mp(v) for v in (h.m_Normals if nrm is None else nrm)] if (h.m_Normals or nrm is not None) else None
    subs = h.get_triangles()
    allt = winding(pos, nrm, [t for sub in subs for t in sub])
    groups, k = [], 0
    for si, sub in enumerate(subs):
        groups.append([k * 3, len(sub) * 3, si])
        k += len(sub)
    return {"pos": [round(float(x), 5) for v in pos for x in v],
            "nrm": [round(float(x), 4) for v in nrm for x in v] if nrm else None,
            "uv": [round(float(x), 5) for v in h.m_UV0 for x in v[:2]] if h.m_UV0 else None,
            "idx": [int(x) for t in allt for x in t], "groups": groups}


def bindposes(mesh):
    S = (-1, 1, 1, 1)                                   # bind poses S B S, column-major for three.js
    return [round(getattr(b, f"e{r}{c}") * S[r] * S[c], 6) for b in mesh.m_BindPose for c in range(4) for r in range(4)]


def texture(tex_ptr):
    t = tex_ptr.read()
    fn = f"tot_{t.m_Name}.png"
    path = os.path.join(PTEX, fn)
    if not os.path.exists(path):
        t.image.save(path)
    return fn


def materials(renderer):
    out = []
    for mp_ in renderer.m_Materials:
        tex, color = None, [1, 1, 1, 1]
        try:
            m = mp_.read()
            for k, v in m.m_SavedProperties.m_TexEnvs:
                if k == "_MainTex" and v.m_Texture.m_PathID:
                    tex = texture(v.m_Texture)
            for k, v in m.m_SavedProperties.m_Colors:
                if k == "_Color":
                    color = [round(v.r, 3), round(v.g, 3), round(v.b, 3), round(v.a, 3)]
        except Exception as e:
            print(f"    material: {type(e).__name__}: {e}")
        out.append({"tex": tex, "color": color})
    return out


def body_block(smr, buf, rig):
    """wardrobe_data.py's mesh_block: one skinned mesh into the .bin, its descriptor back (None if a bone is missing)."""
    m = smr.m_Mesh.read()
    h = handler(m)
    pos = [mp(v) for v in h.m_Vertices]
    nrm = [mp(v) for v in h.m_Normals] if h.m_Normals else None
    tris = winding(pos, nrm, [t for sub in h.get_triangles() for t in sub])
    bones = [b.read().m_GameObject.read().m_Name for b in smr.m_Bones]
    if not all(b in rig for b in bones):
        return None
    d = {"verts": len(pos), "tris": len(tris), "bones": bones, "ibm": bindposes(m)}

    def put(key, fmt, values):
        d[key] = len(buf)
        buf.extend(struct.pack(f"<{len(values)}{fmt}", *values))
    put("pos", "f", [x for v in pos for x in v])
    put("nrm", "f", [x for v in (nrm or [[0, 1, 0]] * len(pos)) for x in v])
    put("uv", "f", [x for v in (h.m_UV0 or [[0, 0]] * len(pos)) for x in v[:2]])
    put("w", "f", [x for v in h.m_BoneWeights for x in v])
    put("j", "H", [x for v in h.m_BoneIndices for x in v])
    while len(buf) % 4:
        buf.append(0)
    put("idx", "I", [int(x) for t in tris for x in t])
    return d


def prop_nodes(go, rig):
    """A prefab as the page's prop: plain nodes (Unity TRS mirrored) with meshes and materials. A skinned mesh on the
    hero's own bones comes back as heroSkin; one on the prefab's own bones is baked into its prefab pose (relative to
    the root, which the page places)."""
    T = tree(go)
    nodes, hero = [], None
    world = []                                          # each node's matrix relative to the root (root excluded)
    for k, (g, tr, parent) in enumerate(T):
        p, q, s = trs(tr)
        world.append(np.eye(4) if parent < 0 else world[parent] @ mat4(p, q, s))
        e = {"name": g.m_Name, "parent": parent, "p": [round(x, 5) for x in mp(p)], "q": [round(x, 6) for x in mq(q)],
             "s": [round(x, 5) for x in s], "on": bool(g.m_IsActive)}
        mf, mr = comp(g, "MeshFilter"), comp(g, "MeshRenderer")
        if mf and mr and mf.m_Mesh.m_PathID:
            e["mesh"] = arrays(handler(mf.m_Mesh.read()))
            e["mats"] = materials(mr)
        nodes.append(e)
    for k, (g, tr, parent) in enumerate(T):
        smr = comp(g, "SkinnedMeshRenderer")
        if not smr or not smr.m_Mesh.m_PathID:
            continue
        m = smr.m_Mesh.read()
        h = handler(m)
        bones = [b.read().m_GameObject.read().m_Name for b in smr.m_Bones]
        if bones and all(b in rig for b in bones):
            hs = arrays(h)
            hs["w"] = [round(float(x), 5) for v in h.m_BoneWeights for x in (list(v) + [0, 0, 0, 0])[:4]]
            hs["j"] = [int(x) for v in h.m_BoneIndices for x in (list(v) + [0, 0, 0, 0])[:4]]
            hs["bones"], hs["ibm"] = bones, bindposes(m)
            hero = (hs, materials(smr))
            continue
        # own bones: Unity skinning, sum of w x bone (relative to the root) x bindpose x v
        idx = {T[i][1].m_GameObject.read().m_Name: i for i in range(len(T))}
        B = [world[idx[b]] if b in idx else np.eye(4) for b in bones]
        bp = [np.array([[getattr(b, f"e{r}{c}") for c in range(4)] for r in range(4)]) for b in m.m_BindPose]
        V, N = np.array(h.m_Vertices), np.array(h.m_Normals) if h.m_Normals else None
        W, J = np.array(h.m_BoneWeights), np.array(h.m_BoneIndices)
        pos, nrm = np.zeros_like(V), np.zeros_like(V) if N is not None else None
        for i in range(len(bones)):
            M = B[i] @ bp[i]
            w = (W * (J == i)).sum(1)[:, None]
            pos += w * (np.c_[V, np.ones(len(V))] @ M.T)[:, :3]
            if N is not None:
                nrm += w * (N @ np.linalg.inv(M[:3, :3]))
        if N is not None:
            nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-9
        nodes.append({"name": "baked_" + g.m_Name, "parent": 0, "p": [0, 0, 0], "q": [0, 0, 0, 1], "s": [1, 1, 1], "on": True,
                      "mesh": arrays(h, pos.tolist(), nrm.tolist() if nrm is not None else None), "mats": materials(smr)})
        if k == 0:                                     # the root itself held the skin: its own TRS is not part of it
            pass
    return nodes, hero


def webp(img, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.convert("RGBA").save(path, "WEBP", quality=90, method=4)


def merge(path, new, dump):
    """Replace this script's earlier entries ("tot") in a list file, keep everything else in place."""
    old = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else []
    keep = [x for x in old if not x.get("tot")]
    dump(keep + new, path)
    return len(keep)


os.makedirs(PTEX, exist_ok=True)
meta_p = os.path.join(OUT, "meta.json")
meta = json.load(open(meta_p, encoding="utf-8"))
for cls in CLASSES:
    if ONLY and cls not in ONLY:
        continue
    cap, od = cls.capitalize(), os.path.join(OUT, cls)
    rig = {b["name"] for b in json.load(open(os.path.join(od, "rig.json")))["bones"]}
    report = []
    # ---- the body: an outfit ----
    outfit = []
    go = asset(cls, f"{cap}_Student", "GameObject")
    if go:
        buf, meshes = bytearray(), []
        for g, tr, parent in tree(go):
            smr = comp(g, "SkinnedMeshRenderer")
            if smr and smr.m_Mesh.m_PathID:
                d = body_block(smr, buf, rig)
                if d:
                    d["name"] = g.m_Name
                    meshes.append(d)
                else:
                    report.append(f"body mesh {g.m_Name}: a bone is not in the rig - skipped")
        colours = []
        for c in range(1, 10):
            t = asset(cls, f"{cap}_Student_{c}", "Texture2D")
            if t:
                webp(t.image, os.path.join(od, "tex", f"student{c}.webp"))
                colours.append(c)
        if meshes and colours:
            open(os.path.join(od, "o_student.bin"), "wb").write(bytes(buf))
            outfit = [{"name": "student", "tto": False, "tot": True, "colors": colours, "face": "quarter", "meshes": meshes}]
            report.append(f"outfit student: {len(meshes)} mesh(es), {sum(d['verts'] for d in meshes)} verts, colours {colours}")
    n_out = merge(os.path.join(od, "outfits.json"), outfit, lambda v, p: json.dump(v, open(p, "w")))
    # ---- the hat: a headpiece ----
    hats = []
    go = asset(cls, f"{cap}_Student_accessories", "GameObject")
    if go:
        nodes, hero = prop_nodes(go, rig)
        e = {"name": "studentHat", "tto": False, "tot": True, "mount": "Head"}
        if hero:
            e["nodes"], e["heroSkin"], e["mats"] = [], hero[0], hero[1]
            report.append(f"headpiece studentHat: skinned to the hero's bones, {len(hero[0]['pos']) // 3} verts")
        elif any("mesh" in n for n in nodes):
            e["nodes"] = nodes
            report.append(f"headpiece studentHat: {sum('mesh' in n for n in nodes)} rigid mesh node(s)")
        else:
            e = None
            report.append("headpiece: no mesh found")
        if e:
            hats.append(e)
    merge(os.path.join(od, "props_accessories.json"), hats, lambda v, p: json.dump(v, open(p, "w"), separators=(",", ":")))
    # ---- the weapon(s) ----
    weapons = []
    for part, name in WEAPON_PARTS.items():
        go = asset(cls, f"{cap}_Student_{part}", "GameObject")
        if not go:
            continue
        nodes, hero = prop_nodes(go, rig)
        if hero:
            report.append(f"weapon {name}: skinned to the hero's bones - not expected, skipped")
            continue
        if any("mesh" in n for n in nodes):
            weapons.append({"name": name, "tto": False, "tot": True, "mount": "mount_Hand_R", "nodes": nodes})
            report.append(f"weapon {name}: {sum('mesh' in n for n in nodes)} mesh node(s)")
    merge(os.path.join(od, "props_weapons.json"), weapons, lambda v, p: json.dump(v, open(p, "w"), separators=(",", ":")))
    for c in meta["classes"]:
        if c["cls"] == cls:
            c["outfits"] = n_out + len(outfit)
    print(f"{cls}:", "; ".join(report), flush=True)
json.dump(meta, open(meta_p, "w"), separators=(",", ":"))
print("done", OUT)
