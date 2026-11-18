r"""Bloom Pulse for the LOCAL wardrobe (user 2026-11-18: "add t_all_tto_bloompulse to the wardrobe too if it has a model
for it", then "Do the meshes at max level for Bloom Pulse").

  uv run --no-project --with UnityPy --with pillow python -I pipeline/wardrobe_tto_trinkets.py [--assets tto_assets/2026-11-18]

Run it again after wardrobe_data.py (which rewrites all/props_trinkets.json and icons.json), then
`uv run --no-project --with UnityPy python pipeline/wardrobe_placements.py` for TTO's placement tables.

A shared back trinket new in TTO 1.7.0: prefabs gameassets/characters/heroes/all/trinkets/aura_bloompulse + _lv1.._lv9
(the user's name for it: t_all_tto_bloompulse; the game's own codes, found in CharacterEquipment.LoadAura@0x1add4a0
(TTO1118), are t_alllkt2 and t_alllkt2lv1 .. lv9, one per level: t_alllkt2lv9 loads aura_bloompulse_lv9). Its look is mostly particles; the tile is **lv9's meshes**, static, at their prefab
transforms (the parents' 0.5-0.65 scales included): Moat, Ribbon, Flower1 / 3 / 4 with Inner / Heart / Pulse, Twin0,
Twin1, Ring (17). Every particle system and the scripts that move the meshes are left out, as for the other two auras.

Input: --assets, a decrypted TTO client (catalog.bin + dec/<bundle>; pipeline/wardrobe_tto_fetch.py --grep
"heroes/all/trinkets/aura_bloompulse"; default this folder's tto_assets/2026-11-18, else the home PC's
D:\12tails-wardrobe\tto_assets\2026-11-18).
Output:
  wardrobe/data/all/props_trinkets.json  the entry {"name": "aura_bloompulse", "tto": true, "mount": "Spine1", nodes}
                                         merged in by name (merge(): a re-run replaces it, the rest stays in order)
  wardrobe/data/props/tex/<tex>.png      its textures by the game's texture name (stops if a name already holds another
                                         picture)
  wardrobe/data/icons.json               ["all"]["trinkets"]["aura_bloompulse"] = {"icon": "icons/trinket/alllkt2lv9.webp",
                                         "codes": ["t_alllkt2lv9", "t_all_tto_bloompulse"]}: placementOf takes the first
                                         code TTO's TrinketPlacement has an entry for (t_alllkt2lv9: bone "" = the character
                                         root, keep world rotation, Sheep p (0, 0.008, 0) x 0.9)
  wardrobe/data/icons/trinket/alllkt2lv9.webp  the game's icon (gamegui/icons/items/trinket/alllkt2lv9, lossless at game
                                         size; an upscale of the same picture is left alone: wardrobe_icons_upscale.py)

Materials: every mesh's material is Taproot/VFX Mesh (TTO's own VFX shader: SrcAlpha One additive, no depth write, both
sides, tinted by _Color x _MainTex, with erosion / fresnel / fade parameters the page cannot play). The page's own modes
are opaque, addAlpha (its glow pass ignores the item's colour: all white) and the default alpha cut 0.5 (texture x colour,
the texture's alpha as the shape). The default one is used for all 17: it keeps the greens and the flower / streak
shapes (T_Flower_Tile and T_Streak_Tile carry their shape in alpha). No new material mode on the page.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)                    # run as a script (-I), pipeline/ is not a package: the sibling module by its bare name
from wardrobe_convert import mp, mq, prop_mesh   # noqa: E402  (the props' conversion, shared)

BIBLE = next((p for p in (r"D:\12tails", r"C:\Users\Jump\Desktop\12tails") if os.path.isdir(os.path.join(p, "DecompiledSource_TTO_2026-11-14"))),
             r"D:\12tails")
TOOLS = os.path.join(BIBLE, "DecompiledSource_TTO_2026-11-14", "tools")      # aa_catalog.py (as wardrobe_tto_fetch.py)
OUT = os.path.join(ROOT, "wardrobe", "data")
NAME = "aura_bloompulse"
PREFAB = "gameassets/characters/heroes/all/trinkets/aura_bloompulse_lv9"
CODES = ["t_alllkt2lv9", "t_all_tto_bloompulse"]    # the game's code for level 9 first (it has the placement), then the user's
ICON = "gamegui/icons/items/trinket/alllkt2lv9"
MOUNT = "Spine1"                            # as the other two auras
MESHES = ["Moat", "Ribbon", "Flower1", "Flower1Inner", "Flower1Heart", "Flower1Pulse", "Flower3", "Flower3Inner",
          "Flower3Heart", "Flower3Pulse", "Flower4", "Flower4Inner", "Flower4Heart", "Flower4Pulse", "Twin0", "Twin1", "Ring"]


# ---- pure rules (tested) ----

def merge(entries, new):
    """The entries with each of `new` replacing the one of its name (same place), else appended: a re-run changes nothing."""
    out = list(entries)
    for e in new:
        at = next((i for i, x in enumerate(out) if x["name"] == e["name"]), None)
        if at is None:
            out.append(e)
        else:
            out[at] = e
    return out


def meshes_only(nodes):
    """The nodes that hold a mesh and their ancestors, parents re-indexed; particle-only branches (Bloom, Pollen) go.
    The input is not changed."""
    keep = [False] * len(nodes)
    for k, n in enumerate(nodes):
        if "mesh" in n:
            while k >= 0 and not keep[k]:
                keep[k] = True
                k = nodes[k]["parent"]
    remap, out = {}, []
    for k, n in enumerate(nodes):
        if keep[k]:
            remap[k] = len(out)
            out.append({**n, "parent": remap.get(n["parent"], -1)})
    return out


# ---- the build (UnityPy, Pillow) ----

def main():
    import argparse
    import io

    import UnityPy
    from PIL import Image
    from UnityPy.helpers.MeshHelper import MeshHandler
    from wardrobe_icons_upscale import keep as keep_upscaled

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    own = os.path.join(ROOT, "tto_assets", "2026-11-18")
    ap = argparse.ArgumentParser(description="Bloom Pulse's lv9 meshes for the wardrobe")
    ap.add_argument("--assets", default=own if os.path.isdir(own) else r"D:\12tails-wardrobe\tto_assets\2026-11-18")
    a = ap.parse_args()
    P = lambda c: c.component if hasattr(c, "component") else c[1]       # noqa: E731
    v3 = lambda v: [v.x, v.y, v.z]                                       # noqa: E731
    q4 = lambda q: [q.x, q.y, q.z, q.w]                                  # noqa: E731

    out = subprocess.run([sys.executable, "-I", os.path.join(TOOLS, "aa_catalog.py"), os.path.join(a.assets, "catalog.bin"),
                          "--grep", "^" + re.escape(PREFAB) + "$"], capture_output=True, text=True, encoding="utf-8", check=True).stdout
    rows = [line.split("\t") for line in out.splitlines() if line.count("\t") >= 3]
    if not rows:
        sys.exit(f"{PREFAB} is not in {a.assets}\\catalog.bin")
    row = rows[0]
    bundles = row[3].split()
    missing = [b for b in bundles if not os.path.exists(os.path.join(a.assets, "dec", b))]
    if missing:
        sys.exit(f"{len(missing)} bundles not decrypted in {a.assets}\\dec (pipeline/wardrobe_tto_fetch.py --grep "
                 f"\"heroes/all/trinkets/aura_bloompulse\"): {missing[:3]} ...")
    env = UnityPy.load(*[os.path.join(a.assets, "dec", b) for b in bundles])
    go = dict(env.container.items())[row[2]].read()
    print(f"{PREFAB}: {len(bundles)} bundles ({a.assets})")

    textures, shaders, notes = {}, [], []          # texture file name -> PIL image

    def texture(ptr):
        if not ptr.m_PathID:
            return None
        t = ptr.read()
        fn = (re.sub(r"[^\w.-]", "_", t.m_Name) or "tex") + ".png"
        textures.setdefault(fn, t.image)
        return fn

    def material(ptr, mesh):
        m = ptr.read()
        tex, color = None, [1, 1, 1, 1]
        for k, v in m.m_SavedProperties.m_TexEnvs:
            if k == "_MainTex":
                tex = texture(v.m_Texture)
        for k, v in m.m_SavedProperties.m_Colors:
            if k == "_Color":
                color = [round(v.r, 3), round(v.g, 3), round(v.b, 3), round(v.a, 3)]
        sh = m.m_Shader.read()
        shader = sh.m_ParsedForm.m_Name if getattr(sh, "m_ParsedForm", None) is not None else sh.m_Name
        shaders.append((mesh, m.m_Name, shader, tex, color))
        return {"tex": tex, "color": color}          # the default mode: texture x colour, alpha cut 0.5

    nodes = []

    def walk(tr_ptr, parent):
        tr = tr_ptr.read()
        g = tr.m_GameObject.read()
        me = len(nodes)
        node = {"name": g.m_Name, "parent": parent, "p": [round(x, 5) + 0.0 for x in mp(v3(tr.m_LocalPosition))],
                "q": [round(x, 6) + 0.0 for x in mq(q4(tr.m_LocalRotation))],
                "s": [round(x, 5) for x in v3(tr.m_LocalScale)], "on": bool(getattr(g, "m_IsActive", True))}
        nodes.append(node)
        filt = None
        for c in g.m_Component:
            ptr = P(c)
            t = ptr.type.name
            if t == "MeshFilter":
                filt = ptr.read().m_Mesh
            elif t == "MeshRenderer":
                rr = ptr.read()
                if not getattr(rr, "m_Enabled", True) or filt is None or not filt.m_PathID:
                    continue
                h = MeshHandler(filt.read())
                h.process()
                M = {"pos": [list(v) for v in h.m_Vertices], "nrm": [list(v) for v in (h.m_Normals or [])],
                     "uv0": [list(v) for v in (h.m_UV0 or [])], "subs": [[list(t_) for t_ in sub] for sub in h.get_triangles()]}
                mats = [material(x, g.m_Name) for x in rr.m_Materials]
                node["mesh"], node["mats"] = prop_mesh(M, len(mats)), mats
            elif t == "ParticleSystem":
                notes.append(f"{g.m_Name}: particle system left out")
        for ch in tr.m_Children:
            walk(ch, me)
    walk(next(P(c) for c in go.m_Component if P(c).type.name == "Transform"), -1)
    nodes[0].update({"p": [0, 0, 0], "q": [0, 0, 0, 1], "s": [1, 1, 1]})     # the page places the root (as the other auras)
    nodes = meshes_only(nodes)
    got = [n["name"] for n in nodes if "mesh" in n]
    if sorted(got) != sorted(MESHES):
        sys.exit(f"expected the 17 meshes {sorted(MESHES)}, got {len(got)}: {sorted(got)}")
    entry = {"name": NAME, "tto": True, "mount": MOUNT, "nodes": nodes}

    # ---- textures: one picture per name in props/tex ----
    ptex = os.path.join(OUT, "props", "tex")
    os.makedirs(ptex, exist_ok=True)
    new_tex, same_tex = [], 0
    for fn, img in sorted(textures.items()):
        buf = io.BytesIO()
        img.save(buf, "PNG")
        path = os.path.join(ptex, fn)
        if os.path.exists(path):
            with Image.open(path) as old:
                if old.size == img.size and old.convert("RGBA").tobytes() == img.convert("RGBA").tobytes():
                    same_tex += 1
                    continue
            sys.exit(f"texture name clash: props/tex/{fn} already holds another picture: stop")
        new_tex.append((path, buf.getvalue()))
    for path, data in new_tex:
        open(path, "wb").write(data)

    # ---- the icon ----
    icon = None
    out = subprocess.run([sys.executable, "-I", os.path.join(TOOLS, "aa_catalog.py"), os.path.join(a.assets, "catalog.bin"),
                          "--grep", "^" + re.escape(ICON) + "$"], capture_output=True, text=True, encoding="utf-8", check=True).stdout
    irows = [line.split("	") for line in out.splitlines() if line.count("	") >= 3]
    if irows and os.path.exists(os.path.join(a.assets, "dec", irows[0][3].split()[0])):
        ienv = UnityPy.load(os.path.join(a.assets, "dec", irows[0][3].split()[0]))
        iobj = dict(ienv.container.items()).get(irows[0][2])
        if iobj is not None:
            ipath = os.path.join(OUT, "icons", "trinket", "alllkt2lv9.webp")
            img = iobj.read().image
            os.makedirs(os.path.dirname(ipath), exist_ok=True)
            if not keep_upscaled(ipath, img):
                img.save(ipath, "WEBP", lossless=True)
            icon = "icons/trinket/alllkt2lv9.webp"
    if icon is None:
        notes.append(f"no icon {ICON} in the loaded bundles: the page's no-icon tile")

    # ---- the entries ----
    fp = os.path.join(OUT, "all", "props_trinkets.json")
    entries = json.load(open(fp, encoding="utf-8"))
    json.dump(merge(entries, [entry]), open(fp, "w", encoding="utf-8", newline=""), separators=(",", ":"))
    ip = os.path.join(OUT, "icons.json")
    icons = json.load(open(ip, encoding="utf-8"))
    icons["all"]["trinkets"][NAME] = {"icon": icon, "codes": CODES}
    json.dump(icons, open(ip, "w", encoding="utf-8", newline=""), separators=(",", ":"))

    print(f"icon {icon}")
    print(f"entry {NAME}: {len(nodes)} nodes, {len(got)} meshes, textures {len(new_tex)} new, {same_tex} already in props/tex")
    print("meshes -> the page's material mode:")
    for mesh, mat, shader, tex, color in shaders:
        print(f"  {mesh:13s} {mat:26s} {shader} tex {tex} colour {color} -> default (alpha cut 0.5)")
    if notes:
        print(f"notes: {len(notes)}", *notes, sep="\n  ")
    print("done", fp)


if __name__ == "__main__":
    main()
