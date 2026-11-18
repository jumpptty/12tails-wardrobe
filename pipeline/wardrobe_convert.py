"""The Unity -> three.js conversion of meshes and clips, shared by wardrobe_data.py and the pet extractor: x mirrored,
quaternions (x, -y, -z, w), triangle winding chosen to agree with the normals. Pure Python (no UnityPy, no PIL), so
tests and other scripts can import it without loading the game's bundles. Also the props' materials (prop_mats,
game_shader: BB's material of the texture's name in the Bible's rip, read as text). Tests:
pipeline/test_wardrobe_convert.py.
"""
import math
import os
import re


r5 = lambda x: (1e30 if x > 0 else -1e30) if math.isinf(x) else round(x, 5)
mp = lambda p: [-p[0], p[1], p[2]]
mq = lambda q: [q[0], -q[1], -q[2], q[3]]


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


BIBLE_MATS = next((p for p in (r"D:\12tails", r"C:\Users\Jump\Desktop\12tails")
                   if os.path.isdir(os.path.join(p, "RippedAssets"))), r"D:\12tails") + r"\RippedAssets\ExportedProject\Assets\Material"
ADDITIVE_ALPHA = "184331bfe0c8b0c428d3876fa69d4cd1"       # Transparent/AdditiveAlpha (the champion weapons; its properties
# _AdditiveColor / _AdditiveRange are this shader's only), not a file in the rip: known by its materials


def game_shader(tex):
    """What the game's material of the same name does with the texture's alpha, as the page needs it. BB's prop
    materials sit in the Bible's rip (props/json leaves the shader empty). The page cuts every texel under alpha 0.5
    (alphaTest), right for most props, wrong for two kinds (user 2026-11-12: "Wolf Time Sword and Champion Sword why
    their textures are missing, champion sword shoe have aqua glass like blades along the edges"):
      opaque: the built-in Diffuse (fileID 7) ignores alpha, the texture's alpha is a mask for something else (the
              Time Sword's is 96 % under 0.5: it was cut almost away)
      addAlpha, cut: Transparent/AdditiveAlpha draws texels with alpha >= cut (_AdditiveRange, default 0.9) solid, the
              rest added as light (tex x alpha, Blend SrcAlpha One, both sides, no depth write): the glass edges
    """
    if not tex:
        return {}
    f = os.path.join(BIBLE_MATS, os.path.splitext(tex)[0] + ".mat")
    if not os.path.exists(f):
        return {}
    s = open(f, encoding="utf-8", errors="ignore").read()
    m = re.search(r"m_Shader: \{fileID: (\d+), guid: (\w+)", s)
    if not m:
        return {}
    if m.group(1) == "7" and m.group(2) == "0000000000000000e000000000000000":
        return {"shader": "opaque"}
    if m.group(2) == ADDITIVE_ALPHA:
        r = re.search(r"name: _AdditiveRange\s+second: ([\d.]+)", s)
        return {"shader": "addAlpha", "cut": round(float(r.group(1)) if r else 0.9, 4)}
    return {}


def prop_mats(mats, tto):
    """A node's materials for the page: texture, colour, and the game's shader where it matters (BB items only: TTO's
    new ones have no material in the rip)."""
    return [{"tex": m.get("tex"), "color": [round(x, 3) for x in m.get("color", [1, 1, 1, 1])],
             **({} if tto else game_shader(m.get("tex")))} for m in mats]
