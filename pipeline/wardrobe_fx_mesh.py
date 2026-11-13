"""Mesh parts of the game's effects, for pipeline/wardrobe_fx.py (2026-11-09; plans/fx_wolf/parts.md steps 5, 7, 9:
StaticMesh = a MeshFilter drawn by a MeshRenderer with no emitter, SkinnedMeshRenderer, Animation, and the data
ShatterMesh needs). Its own file so the mesh work never edits wardrobe_fx.py.

component(game, comp_obj, ty, node, ctx) is called for every MeshFilter, SkinnedMeshRenderer and Animation component of
an effect node; it returns a list of component dicts to append to node["comps"] (JSON-safe), or None. ctx: cls, effect
(the prefab's name), mats / texs / sounds (the run's collections: add to them), material (wardrobe_fx.material: call
ctx["material"](game, pptr, comp_obj.assets_file, ctx["mats"], ctx["texs"]) for a renderer's materials).

Everything stays in Unity's space (no x -> -x: the page's effect group mirrors), unlike wardrobe_data.py's heroes. Shapes:
  mesh  {name, verts, pos [x y z ...], nrm [..] | null, uv [u v ...] | null, col [r g b a ...] | null,
         idx [a b c ...] (every submesh's triangles in Unity's own order and winding: ShatterMesh's normals need it),
         sub [[first index, index count], ...]}
  {"type": "StaticMesh", mesh}                                           a MeshFilter with a mesh (an emitter's own
        MeshFilter has none: 1,580 of them across the 12 classes, none with a mesh; scan 2026-11-09). Drawn with the
        node's MeshRenderer materials (node.mats, one per submesh)
  {"type": "SkinnedMeshRenderer", mesh + {w [4 per vertex], j [4 per vertex], bind [16 per bone, column-major]},
        bones [node index per m_Bones entry], root (node index | null), mats [material names]}
  {"type": "Animation", clip (the default clip's name | null), play (m_PlayAutomatically), wrap (m_WrapMode),
        clips {name: {len, wrap (the clip's own m_WrapMode), tracks {node index: {path, q / p / s: keys}}}}}
        keys = [[time, value..., inSlope..., outSlope...], ...] as wardrobe_data.py clip_dict writes them (the page's
        hermite()), infinite slopes as +-1e30 (a step). Node indices count the effect's nodes in wardrobe_fx.py's walk
        order (the prefab root 0, depth first, children in m_Children order), so a curve's path is resolved here the way
        Unity's Transform.Find does it: the first child with that name at each step (dualBrand_slash2 has Slash2 under
        Slash2).
No clip in any class's effects has float curves, events, compressed rotations or an empty path (scan of every hero
effect, 2026-11-09), so only the three transform curve kinds are read; anything else raises.

  uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py wolf --probe bladefang_underslash,mirrorblade_mirror
shows what this gives (read only).
"""
import math
import struct

from UnityPy.helpers.MeshHelper import MeshHandler

# (a NaN, as some of warCapital's normals: 0, 2026-11-13; JSON has no NaN and the page's JSON.parse refused the whole
# fx.json, so every Mole effect read as missing)
r5 = lambda x: 0.0 if math.isnan(x) else (1e30 if x > 0 else -1e30) if math.isinf(x) or abs(x) >= 1e29 else round(x, 5)
_trees = {}            # (file name, root Transform path id) -> {(file name, Transform path id): node index}


def _go_name(game, tr_obj):
    return game.obj(tr_obj.read_typetree()["m_GameObject"], tr_obj.assets_file).read_typetree()["m_Name"]


def _transform_of(game, comp_obj):
    """The Transform on the component's GameObject."""
    go = game.obj(comp_obj.read_typetree()["m_GameObject"], comp_obj.assets_file)
    for c in go.read_typetree()["m_Component"]:
        o = game.obj(c[1] if isinstance(c, (list, tuple)) else c.get("second", c.get("component")), go.assets_file)
        if o is not None and o.type.name == "Transform":
            return o
    raise ValueError(f"{comp_obj.type.name} on a GameObject with no Transform")


def _index(game, tr_obj):
    """{(file, path id): node index} for the effect holding this Transform, numbered as wardrobe_fx.py's walk() numbers
    the nodes (pre-order, children in m_Children order, a missing child skipped)."""
    root = tr_obj
    while True:
        f = root.read_typetree()["m_Father"]
        if not f["m_PathID"]:
            break
        root = game.obj(f, root.assets_file)
    key = (root.assets_file.name, root.path_id)
    if key not in _trees:
        out = {}

        def walk(t):
            out[(t.assets_file.name, t.path_id)] = len(out)
            for ch in t.read_typetree()["m_Children"]:
                c = game.obj(ch, t.assets_file)
                if c is not None:
                    walk(c)
        walk(root)
        _trees[key] = out
    return _trees[key]


def _node_of(game, tr_obj):
    return _index(game, tr_obj)[(tr_obj.assets_file.name, tr_obj.path_id)]


def _find(game, tr_obj, path):
    """Unity's Transform.Find: each '/' step takes the first child with that name; None when a step is missing."""
    t = tr_obj
    for step in [s for s in path.split("/") if s]:
        nxt = None
        for ch in t.read_typetree()["m_Children"]:
            c = game.obj(ch, t.assets_file)
            if c is not None and _go_name(game, c) == step:
                nxt = c
                break
        if nxt is None:
            return None
        t = nxt
    return t


def _triangles(h, m):
    """Each submesh's triangles from the index buffer. Unity 3.5's SubMesh has isTriStrip (no topology): 0 a triangle
    list, else a strip (alternate windings flipped, degenerates dropped, as Unity unpacks it). UnityPy's own
    get_triangles reads every 3.x submesh as a strip, so it is not used. Checked against each submesh's triangleCount."""
    ib = list(h.m_IndexBuffer or [])
    idx, sub = [], []
    for s in m.m_SubMeshes:
        first = s.firstByte // (2 if h.m_Use16BitIndices else 4)
        part = ib[first:first + s.indexCount]
        tris = []
        if getattr(s, "isTriStrip", 0):
            for i in range(len(part) - 2):
                a, b, c = part[i:i + 3]
                if a == b or a == c or b == c:
                    continue
                tris.append((b, a, c) if i & 1 else (a, b, c))
        else:
            tris = [tuple(part[i:i + 3]) for i in range(0, len(part) - 2, 3)]
        want = getattr(s, "triangleCount", None)
        if want is not None and want != len(tris):
            raise ValueError(f"{m.m_Name}: submesh gave {len(tris)} triangles, triangleCount {want}")
        sub.append([len(idx), 3 * len(tris)])
        idx += [x for t in tris for x in t]
    return idx, sub


def mesh_dict(mesh, skinned=False):
    """A Mesh through MeshHandler (in this Unity 3.5 file the vertex fields are empty and the data is in m_VertexData),
    in Unity's space."""
    h = MeshHandler(mesh)
    h.process()
    pos = h.m_Vertices or []
    flat = lambda rows, n: [r5(float(x)) for v in rows for x in list(v)[:n]] if rows else None
    idx, sub = _triangles(h, mesh)
    d = {"name": mesh.m_Name, "verts": len(pos), "pos": flat(pos, 3), "nrm": flat(h.m_Normals, 3),
         "uv": flat(h.m_UV0, 2), "col": None, "idx": idx, "sub": sub}
    if h.m_Colors:                       # Color32 (0..255) or floats, by what the handler gives
        cs = [list(c) for c in h.m_Colors]
        big = any(x > 1.001 for c in cs for x in c)
        d["col"] = [round(x / 255 if big else x, 4) for c in cs for x in c[:4]]
    if skinned:
        d["w"] = [round(float(x), 5) for v in (h.m_BoneWeights or []) for x in list(v)[:4]]
        d["j"] = [int(x) for v in (h.m_BoneIndices or []) for x in list(v)[:4]]
        d["bind"] = [round(getattr(b, f"e{r}{c}"), 6) for b in mesh.m_BindPose for c in range(4) for r in range(4)]
    return d


def _keys(ks, comps):
    rows = []
    for k in ks:
        row = [round(float(k["time"]), 5)]
        for part in ("value", "inSlope", "outSlope"):
            row += [r5(float(k[part][c])) for c in comps]
        rows.append(row)
    return rows


def clip_dict(game, clip_obj, anim_tr):
    """A legacy AnimationClip (uncompressed, as every effect clip is) with each curve's path resolved to a node index
    from the Animation's node; a path that names no node is dropped (Unity animates nothing there either)."""
    tt = clip_obj.read_typetree()
    if tt.get("m_Compressed") or tt.get("m_CompressedRotationCurves") or tt.get("m_FloatCurves") or tt.get("m_Events"):
        raise ValueError(f"clip {tt['m_Name']}: compressed / float curves / events are not read yet")
    tracks, length, lost = {}, 0.0, []
    for field, slot, comps in (("m_RotationCurves", "q", "xyzw"), ("m_PositionCurves", "p", "xyz"),
                               ("m_ScaleCurves", "s", "xyz")):
        for cv in tt.get(field) or []:
            ks = cv["curve"]["m_Curve"]
            if not ks:
                continue
            t = _find(game, anim_tr, cv["path"])
            if t is None:
                lost.append(cv["path"]); continue
            tr = tracks.setdefault(str(_node_of(game, t)), {"path": cv["path"]})
            tr[slot] = _keys(ks, comps)
            length = max(length, float(ks[-1]["time"]))
    out = {"len": round(length, 4), "wrap": int(tt["m_WrapMode"]), "tracks": tracks}
    if lost:
        out["lost"] = lost
    return tt["m_Name"], out


def component(game, comp_obj, ty, node, ctx):
    t = comp_obj.read_typetree()
    if ty == "MeshFilter":
        mo = game.obj(t["m_Mesh"], comp_obj.assets_file)
        if mo is None:                   # an emitter's MeshFilter: the emitter fills it at run time
            return None
        d = mesh_dict(mo.read())
        return [{"type": "StaticMesh", **d}] if d["verts"] else None
    if ty == "SkinnedMeshRenderer":
        mo = game.obj(t["m_Mesh"], comp_obj.assets_file)
        if mo is None:
            return None
        d = mesh_dict(mo.read(), skinned=True)
        bones = []
        for b in t["m_Bones"]:
            bo = game.obj(b, comp_obj.assets_file)
            bones.append(_node_of(game, bo) if bo is not None else None)
        rb = t.get("m_RootBone") or {}
        ro = game.obj(rb, comp_obj.assets_file) if rb.get("m_PathID") else None
        mats = [ctx["material"](game, m, comp_obj.assets_file, ctx["mats"], ctx["texs"]) for m in t["m_Materials"]]
        return [{"type": "SkinnedMeshRenderer", **d, "bones": bones, "root": _node_of(game, ro) if ro else None,
                 "mats": mats}]
    if ty == "Animation":
        tr = _transform_of(game, comp_obj)
        clips = {}
        for c in t["m_Animations"]:
            co = game.obj(c, comp_obj.assets_file)
            if co is not None:
                name, cd = clip_dict(game, co, tr)
                clips[name] = cd
        do = game.obj(t["m_Animation"], comp_obj.assets_file) if t["m_Animation"]["m_PathID"] else None
        return [{"type": "Animation", "clip": do.read_typetree()["m_Name"] if do else None,
                 "play": bool(t.get("m_PlayAutomatically", True)), "wrap": int(t.get("m_WrapMode", 0)),
                 "clips": clips}]
    return None


if __name__ == "__main__":
    print(__doc__)
