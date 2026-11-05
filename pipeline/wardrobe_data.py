r"""Data for the wardrobe app (user 2026-11-04: "an html wardrobe app, each class in idle animation, where I can freely
change clothes and equipments, add emotes animations too").

  uv run --no-project --with UnityPy --with pillow python wardrobe_data.py [--only sheep,rabbit] [--no-props]
  -> wardrobe/data/meta.json, wardrobe/data/<cls>/{rig.json, outfits.json, o_<armor>.bin, tex/*.webp, faces/*.webp,
     clips.json, props_<kind>.json}; wardrobe/data/all/props_trinkets.json (the shared trinkets)

Everything is converted to three.js space here, which is build_rabbit.py's mirrored space (right-handed, Y up): Unity
positions x -> -x, quaternions (x, y, z, w) -> (x, -y, -z, w), bind poses S B S with S = diag(-1, 1, 1, 1), triangle
winding chosen to agree with the stored normals. Sources: the class skeleton = BB's (outfits/<cls>_standard_mesh.json,
extract.py), every outfit and every clip from the TTO client (tto_assets/<date>: BB's items and TTO's new ones;
BB's clips sit in animation prefabs, TTO's new ones are bare AnimationClips), faces = BB overlays 0-22 + tex/faces_tto,
props = props/json (extract_tto_props.py). Clips keep the game's Hermite keys (mirrored; an infinite slope = a step,
written as +-1e30); the app samples them.
"""
import io
import json
import math
import os
import re
import struct
import subprocess
import sys

import UnityPy
from PIL import Image
from UnityPy.helpers.MeshHelper import MeshHandler

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HEROES = r"D:\12tails\RippedAssets\ExportedProject\Assets\Resources\gameassets\characters\heroes"
TOOLS = r"D:\12tails\DecompiledSource_TTO_2026-11-02\tools"
argv = sys.argv[1:]
ASSETS = argv[argv.index("--assets") + 1] if "--assets" in argv else os.path.join(ROOT, "tto_assets", "2026-11-04")
ONLY = set(argv[argv.index("--only") + 1].lower().split(",")) if "--only" in argv else None
OUT = os.path.join(ROOT, "wardrobe", "data")
CLASSES = ["bat", "bison", "cat", "chameleon", "mole", "monkey", "panda", "penguin", "rabbit", "sheep", "whale", "wolf"]
EMOTES = {"wave", "bow", "cheer", "cry", "laugh", "dance", "sit", "sleep", "talk", "beg", "clap", "wai", "cooking",
          "mining", "planting"}
BASE = {"root", "battle", "run", "ko", "falling", "getup"}

r5 = lambda x: (1e30 if x > 0 else -1e30) if math.isinf(x) else round(x, 5)
mp = lambda p: [-p[0], p[1], p[2]]
mq = lambda q: [q[0], -q[1], -q[2], q[3]]

cat = subprocess.run([sys.executable, "-P", os.path.join(TOOLS, "aa_catalog.py"), os.path.join(ASSETS, "catalog.bin"),
                      "--grep", r"heroes/[a-z]+/(armors/[a-z]+_[a-z0-9]+|armors/materials/[a-z]+_[a-z0-9]+|animations/[a-z0-9_]+)$"],
                     capture_output=True, text=True, encoding="utf-8", check=True).stdout
addr = {}
for line in cat.splitlines():
    p = line.split("\t")
    if len(p) >= 4:
        addr[p[0]] = (p[1].split(".")[-1], p[2], p[3].split())
bundles = sorted({b for t, i, bs in addr.values() for b in bs})
print(f"{len(addr)} assets in {len(bundles)} bundles", flush=True)
env = UnityPy.load(*[os.path.join(ASSETS, "dec", b) for b in bundles])
container = dict(env.container.items())
P = lambda c: c.component if hasattr(c, "component") else c[1]


def get(a):
    return container[addr[a][1]].read()


def webp(img, path, lossless=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, "WEBP", quality=90, method=4, lossless=lossless)


def mesh_block(smr, buf):
    """Append one skinned mesh to buf; return its descriptor (byte offsets into the .bin)."""
    m = smr.m_Mesh.read()
    h = MeshHandler(m)
    h.process()
    pos = [mp(v) for v in h.m_Vertices]
    nrm = [mp(v) for v in h.m_Normals] if h.m_Normals else None
    tris = [t for sub in h.get_triangles() for t in sub]
    if nrm:
        def cross_dot(a, b, c):
            u = [pos[b][k] - pos[a][k] for k in range(3)]
            v = [pos[c][k] - pos[a][k] for k in range(3)]
            n = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
            s = [nrm[a][k] + nrm[b][k] + nrm[c][k] for k in range(3)]
            return n[0] * s[0] + n[1] * s[1] + n[2] * s[2]
        agree = sum(1 for a, b, c in tris if cross_dot(a, b, c) > 0)
        if agree < len(tris) / 2:
            tris = [(a, c, b) for a, b, c in tris]
    d = {"verts": len(pos), "tris": len(tris), "bones": [b.read().m_GameObject.read().m_Name for b in smr.m_Bones]}
    S = (-1, 1, 1, 1)
    ibm = []
    for b in m.m_BindPose:                                         # column-major for three.js Matrix4.fromArray
        ibm += [getattr(b, f"e{r}{c}") * S[r] * S[c] for c in range(4) for r in range(4)]
    d["ibm"] = [round(x, 6) for x in ibm]

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
    put("idx", "I", [x for t in tris for x in t])
    return d


def clip_dict(tt):
    tracks, length = {}, 0.0
    for field, slot in (("m_RotationCurves", "q"), ("m_PositionCurves", "p"), ("m_ScaleCurves", "s")):
        for cv in tt.get(field) or []:
            ks = cv["curve"]["m_Curve"]
            if not ks:
                continue
            comps = "xyzw" if slot == "q" else "xyz"
            sign = {"q": (1, -1, -1, 1), "p": (-1, 1, 1), "s": (1, 1, 1)}[slot]
            rows = []
            for k in ks:
                row = [round(float(k["time"]), 5)]
                for part in ("value", "inSlope", "outSlope"):
                    row += [r5(float(k[part][c]) * s) for c, s in zip(comps, sign)]
                rows.append(row)
            tracks.setdefault(cv["path"].rsplit("/", 1)[-1], {})[slot] = rows
            length = max(length, float(ks[-1]["time"]))
    return {"len": round(length, 4), "rate": float(tt["m_SampleRate"]), "loop": int(tt["m_WrapMode"]) == 2,
            "tracks": tracks}


meta = {"classes": []}
PROPS_ONLY = "--props-only" in argv          # re-convert props/json only (e.g. after extract_tto_props.py)
for cls in CLASSES:
    if (ONLY and cls not in ONLY) or PROPS_ONLY:
        continue
    cap = cls.capitalize()
    od = os.path.join(OUT, cls)
    os.makedirs(od, exist_ok=True)
    # ---- rig ----
    S = json.load(open(os.path.join(ROOT, "outfits", f"{cls}_standard_mesh.json")))
    names = [b["name"] for b in S["bones"]]
    rig = {"tri": {"p": mp(S["tri_local"]["p"]), "q": mq(S["tri_local"]["q"]), "s": S["tri_local"]["s"]},
           "bones": [{"name": b["name"], "parent": names.index(b["parent"]) if b["parent"] in names else -1,
                      "p": mp(b["p"]), "q": mq(b["q"]), "s": b["s"]} for b in S["bones"]]}
    json.dump(rig, open(os.path.join(od, "rig.json"), "w"))
    # ---- outfits ----
    bb_armors = {f[len(cls) + 1:-7].lower() for f in os.listdir(os.path.join(HEROES, cls, "armors")) if f.endswith(".prefab")}
    outfits = []
    for a in sorted(x for x in addr if re.fullmatch(rf".*heroes/{cls}/armors/{cls}_[a-z0-9]+", x) and addr[x][0] == "GameObject"):
        low = a.rsplit("_", 1)[1]
        try:
            go = get(a)
        except Exception as e:
            print(f"  {cls}/{low}: {type(e).__name__}")
            continue
        armor = go.m_Name.split("_", 1)[1] if "_" in go.m_Name else low
        smrs = []

        def walk(tr, root=False):
            g = tr.m_GameObject.read()
            for c in g.m_Component:
                if P(c).type.name == "SkinnedMeshRenderer":
                    smrs.append((not root, g.m_Name, P(c).read()))
            for ch in tr.m_Children:
                walk(ch.read())
        walk(next(P(c) for c in go.m_Component if P(c).type.name == "Transform").read(), True)
        smrs.sort(key=lambda s: s[0])
        buf, meshes = bytearray(), []
        for _, gname, smr in smrs:
            try:
                d = mesh_block(smr, buf)
            except Exception as e:
                print(f"  {cls}/{armor} {gname}: {type(e).__name__}: {e}")
                continue
            if all(n in names for n in d["bones"]):
                d["name"] = gname
                meshes.append(d)
        if not meshes:
            continue
        open(os.path.join(od, f"o_{armor}.bin"), "wb").write(bytes(buf))
        colours, editions = [], {}
        for c in range(1, 10):
            ta = f"gameassets/characters/heroes/{cls}/armors/materials/{cls}_{low}{c}"
            if ta in addr:
                webp(get(ta).image, os.path.join(od, "tex", f"{armor}{c}.webp"))
                colours.append(c)
            # the recolour editions <armor><c>R / V (a set's R / V outfit; 2026-11-05, wardrobe_editions.py did the first
            # pack from the BB rip). Untested from here: the office PC has no TTO bundles
            for e in "rv":
                if ta + e in addr:
                    webp(get(ta + e).image, os.path.join(od, "tex", f"{armor}{c}{e.upper()}.webp"))
                    editions.setdefault(e.upper(), []).append(c)
        outfits.append({"name": armor, "tto": low not in bb_armors, "colors": colours, "meshes": meshes}
                       | ({"editions": editions} if editions else {}))
    outfits.sort(key=lambda o: (o["name"] != "standard", o["tto"], o["name"].lower()))
    json.dump(outfits, open(os.path.join(od, "outfits.json"), "w"))
    # ---- faces ----
    faces = []
    for d_, tto in ((os.path.join(HEROES, cls, "armors", "overlay"), False), (os.path.join(ROOT, "tex", "faces_tto", cls), True)):
        for f in os.listdir(d_) if os.path.isdir(d_) else []:
            m = re.fullmatch(cap + r"(\d+)\.png", f)
            if m and int(m.group(1)) not in {x["n"] for x in faces}:
                webp(Image.open(os.path.join(d_, f)).convert("RGBA").crop((0, 0, 256, 256)),
                     os.path.join(od, "faces", f"{m.group(1)}.webp"), lossless=True)
                faces.append({"n": int(m.group(1)), "tto": tto})
    faces.sort(key=lambda x: x["n"])
    # ---- clips ----
    clips = {}
    for a in sorted(x for x in addr if re.fullmatch(rf".*heroes/{cls}/animations/[a-z0-9_]+", x)):
        t, iid, _ = addr[a]
        try:
            obj = container[iid].read()
            if t == "GameObject":
                anim = next(P(c) for c in obj.m_Component if P(c).type.name == "Animation").read()
                tt = next(x for x in anim.m_Animations if x.m_PathID).deref_parse_as_dict()
            else:
                tt = container[iid].read_typetree()
        except Exception as e:
            print(f"  {cls} clip {a.rsplit('/', 1)[1]}: {type(e).__name__}")
            continue
        if not tt.get("m_Legacy") or tt.get("m_Compressed") or tt.get("m_EulerCurves"):
            print(f"  {cls} clip {tt.get('m_Name')}: not plain legacy curves - skipped")
            continue
        name = tt["m_Name"]
        low = name.lower()
        group = "base" if low in BASE else "emote" if (low in EMOTES or low.startswith(("pose", "fishing"))) else "skill"
        clips[name] = dict(clip_dict(tt), group=group, tto=t == "AnimationClip")
    json.dump(clips, open(os.path.join(od, "clips.json"), "w"), separators=(",", ":"))
    meta["classes"].append({"cls": cls, "outfits": len(outfits), "faces": faces,
                            "clips": {k: {"group": v["group"], "loop": v["loop"], "len": v["len"], "tto": v["tto"]}
                                      for k, v in clips.items()}})
    print(f"{cls}: {len(outfits)} outfits ({sum(o['tto'] for o in outfits)} TTO), {len(faces)} faces, {len(clips)} clips "
          f"({sum(1 for c in clips.values() if c['group'] == 'emote')} emotes)", flush=True)

# ---- props (from props/json, Unity space -> three.js) ----
def prop_mesh(M, nmats):
    """Unity mesh dict -> three.js arrays: x mirrored, triangles per submesh (material slot), winding by the normals."""
    pos = [mp(v) for v in M["pos"]]
    nrm = [mp(v) for v in M["nrm"]] if len(M["nrm"]) == len(pos) else None
    groups, idx = [], []
    for si, sub in enumerate(M["subs"]):
        tri = [tuple(t) for t in sub]
        groups.append([len(idx) * 3, len(tri) * 3, min(si, max(0, nmats - 1))])
        idx += tri
    flip = True
    if nrm and idx:
        ag = 0
        for a, b, c in idx:
            u = [pos[b][i] - pos[a][i] for i in range(3)]
            v = [pos[c][i] - pos[a][i] for i in range(3)]
            cr = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
            ag += sum(cr[i] * (nrm[a][i] + nrm[b][i] + nrm[c][i]) for i in range(3)) > 0
        flip = ag < len(idx) / 2
    if flip:
        idx = [(a, c, b) for a, b, c in idx]
    return {"pos": [round(x, 5) for v in pos for x in v], "nrm": [round(x, 4) for v in nrm for x in v] if nrm else None,
            "uv": [round(x, 5) for v in M["uv0"] for x in v[:2]] if len(M["uv0"]) == len(pos) else None,
            "idx": [x for t in idx for x in t], "groups": groups}


def mirror_rows(rows, slot):
    """Clip key rows [t, values, inSlopes, outSlopes] mirrored like the hero clips: q (x, -y, -z, w), p (-x, y, z)."""
    neg = {"q": (2, 3, 6, 7, 10, 11), "p": (1, 4, 7)}.get(slot, ())
    return [[-x if i in neg else x for i, x in enumerate(r)] for r in rows]


if "--no-props" not in argv:
    for f in sorted(os.listdir(os.path.join(ROOT, "props", "json"))):
        D = json.load(open(os.path.join(ROOT, "props", "json", f)))
        if ONLY and D["class"] not in ONLY and D["class"] != "all":
            continue
        out = []
        for prop in D["props"]:
            nodes = prop["nodes"]
            anim = prop.get("anim")
            # an animated skinned prop (the wings) goes in live: its skin on its own bones + the clips; the baked
            # still shape (extract_tto_props.py) is for the Blender libraries and props that do not move
            live = bool(anim) and any("skin" in n for n in nodes)
            kids = {}
            for k, n in enumerate(nodes):
                kids.setdefault(n["parent"], []).append(k)

            def resolve(start, path):                  # a clip path is relative to the Animation's node
                k = start
                for part in [x for x in path.split("/") if x]:
                    k = next((c for c in kids.get(k, []) if nodes[c]["name"] == part), None)
                    if k is None:
                        return None
                return k
            keep = [False] * len(nodes)

            def mark(k):
                while k is not None and not keep[k]:
                    keep[k] = True
                    k = nodes[k]["parent"]
            for k, n in enumerate(nodes):
                if "mesh" in n and not (live and n.get("baked")):
                    mark(k)
                if live and "skin" in n:
                    mark(k)
                    for b in n["skin"]["bones"]:
                        mark(b)
            at = {}
            if live:
                mark(anim["node"])
                for cname, c in anim["clips"].items():
                    for path in c["tracks"]:
                        t = resolve(anim["node"], path)
                        if t is not None:
                            at[(cname, path)] = t
                            mark(t)
            if not any(keep):
                continue
            remap, nn = {}, []
            for k, n in enumerate(nodes):
                if not keep[k]:
                    continue
                remap[k] = len(nn)
                e = {"name": n["name"], "parent": remap.get(n["parent"], -1), "p": [round(x, 5) for x in mp(n["p"])],
                     "q": [round(x, 6) for x in mq(n["q"])], "s": [round(x, 5) for x in n["s"]], "on": n.get("active", True)}
                if "mesh" in n and not (live and n.get("baked")):
                    e["mesh"] = prop_mesh(n["mesh"], len(n.get("mats", [])))
                    e["mats"] = [{"tex": m.get("tex"), "color": [round(x, 3) for x in m.get("color", [1, 1, 1, 1])]}
                                 for m in n.get("mats", [])]
                if live and "skin" in n:
                    sk = n["skin"]
                    M = sk["mesh"]
                    e["skin"] = prop_mesh(M, len(sk["mats"]))
                    e["skin"]["w"] = [round(float(x), 5) for v in M["w"] for x in (list(v) + [0, 0, 0, 0])[:4]]
                    e["skin"]["j"] = [int(x) for v in M["bi"] for x in (list(v) + [0, 0, 0, 0])[:4]]
                    Sg = (-1, 1, 1, 1)                 # bind poses S B S, column-major for three.js
                    e["skin"]["ibm"] = [round(b[r][c] * Sg[r] * Sg[c], 6) for b in M["bind"] for c in range(4) for r in range(4)]
                    e["mats"] = [{"tex": m.get("tex"), "color": [round(x, 3) for x in m.get("color", [1, 1, 1, 1])]}
                                 for m in sk["mats"]]
                nn.append(e)
            for k, n in enumerate(nodes):
                if keep[k] and live and "skin" in n:
                    nn[remap[k]]["skin"]["bones"] = [remap[b] for b in n["skin"]["bones"]]
            entry = {"name": prop["name"], "tto": prop["tto_new"], "mount": prop["mount"], "nodes": nn}
            if live:
                entry["anim"] = {"default": anim["default"], "clips": {
                    cname: {"len": c["len"], "rate": c["rate"], "loop": c["loop"],
                            "tracks": {str(remap[at[(cname, path)]]): {slot: mirror_rows(rows, slot) for slot, rows in tr.items()}
                                       for path, tr in c["tracks"].items() if (cname, path) in at}}
                    for cname, c in anim["clips"].items()}}
            out.append(entry)
        kind = D["kind"]
        os.makedirs(os.path.join(OUT, D["class"]), exist_ok=True)
        json.dump(out, open(os.path.join(OUT, D["class"], f"props_{kind}.json"), "w"), separators=(",", ":"))
        print(f"props {D['class']}/{kind}: {len(out)}", flush=True)

if PROPS_ONLY:
    pass                                       # meta.json is about classes: leave it as it is
elif not ONLY:
    json.dump(meta, open(os.path.join(OUT, "meta.json"), "w"), separators=(",", ":"))
else:
    p = os.path.join(OUT, "meta.json")
    old = json.load(open(p)) if os.path.exists(p) else {"classes": []}
    keep = [c for c in old["classes"] if c["cls"] not in {x["cls"] for x in meta["classes"]}]
    meta["classes"] = sorted(keep + meta["classes"], key=lambda c: c["cls"])
    json.dump(meta, open(p, "w"), separators=(",", ":"))
print("done", OUT)
