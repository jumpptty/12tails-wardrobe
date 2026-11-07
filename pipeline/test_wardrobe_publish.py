r"""Tests for wardrobe_publish.py. Each test builds a tiny wardrobe (page + data/) and a tiny BB rip (AssetRipper YAML
meshes, clips and prefabs, PNG pictures) in a temp folder, publishes it and reads the result.

  cd /d D:\12tails-video\comic-skit && py -3 -m unittest pipeline.test_wardrobe_publish -v
"""
import json
import math
import os
import re
import struct
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from pipeline import wardrobe_publish as wp

# the page's anchors exactly as wardrobe/index.html has them (CRLF, like the real page)
PAGE = """<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<title>12 Tails Wardrobe</title>
<style>
@font-face { font-family: "Prompt"; font-weight: 600; src: url("../fonts/Prompt-SemiBold.ttf") format("truetype"); }
@font-face { font-family: "Prompt"; font-weight: 700; src: url("../fonts/Prompt-Bold.ttf") format("truetype"); }
.bar button { border: 0; }
</style>
</head>
<body>
    <div class="bar">
      <button type="button" id="shot">บันทึกภาพ</button>
      <button type="button" class="primary" id="copy">คัดลอกให้ Claude</button>
    </div>
<script type="module">
const DATA = "data/";
// no-cache = ask the server every time (a 304 when unchanged): a rebuilt outfits.json (the R / V editions, 2026-11-05)
// was otherwise served stale from the browser's cache
const getJSON = async p => { const r = await fetch(p, { cache: "no-cache" }); if (!r.ok) throw new Error(p + " " + r.status); return r.json(); };
      const t = texLoader.load(`../props/tex/${m.tex}`);
$("shot").onclick = () => {};
$("copy").onclick = async () => {
  const s = C.state;
  try { await navigator.clipboard.writeText(text); toast("คัดลอกแล้ว · วางในแชทได้เลย"); } catch (e) { prompt("คัดลอกข้อความนี้", text); }
};
function err(e) { console.error(e); }
</script>
</body>
</html>
""".replace("\n", "\r\n")

TTO_RGBA = (250, 20, 200, 255)     # the data's own (TTO-extracted) pictures
BB_RGBA = (30, 140, 60, 255)       # the BB rip's pictures
TRI = [(0.5, 0.0, 0.25), (0.1, 0.2, 0.3), (-0.75, 1.0, 0.0), (0.0, 0.5, -0.5)]   # Unity space
TRIS = [(0, 1, 2), (0, 2, 3)]
CLIP = [("m_RotationCurves", "Cat_tri/Root", [(0.0, (0.1, 0.2, 0.3, 0.9), (0, 0, 0, 0), (0, 0, 0, 0)),
                                              (0.5, (0.0, 0.1, 0.0, 1.0), (0.5, -0.25, 0, 0), (0.5, -0.25, 0, 0))]),
        ("m_PositionCurves", "Cat_tri/Root/Spine1", [(0.0, (0.5, 0.25, 0.0), (0, 0, 0), (0, 0, 0)),
                                                     (1.0, (0.4, 0.25, 0.1), (0, 0, 0), (0, 0, 0))])]
PLACE = {"bone": "Head", "p": [0, 0, 0], "q": [0, 0, 0, 1], "s": 1.0, "kwr": False, "kps": False}
f32 = lambda x: struct.unpack("<f", struct.pack("<f", x))[0]


def png(path, rgba=BB_RGBA, size=(8, 8)):
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGBA", size, rgba).save(path)


def webp(path, rgba=TTO_RGBA):
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGBA", (8, 8), rgba).save(path, "WEBP", lossless=True)


def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj), encoding="utf-8")


def mesh_yaml(name, positions, tris):
    """A Unity 4 YAML mesh as AssetRipper writes BB's (positions only, one triangle-list submesh)."""
    vdata = b"".join(struct.pack("<3f", *p) for p in positions).hex()
    idx = b"".join(struct.pack("<3H", *t) for t in tris).hex()
    streams = "".join(f"    m_Streams[{s}]:\n      channelMask: {1 if s == 0 else 0}\n      offset: 0\n"
                      f"      stride: {12 if s == 0 else 0}\n      align: 16\n" for s in range(4))
    return (f"%YAML 1.1\n%TAG !u! tag:unity3d.com,2011:\n--- !u!43 &4300000\nMesh:\n  serializedVersion: 6\n"
            f"  m_Name: {name}\n  m_SubMeshes:\n  - firstByte: 0\n    indexCount: {len(tris) * 3}\n    isTriStrip: 0\n"
            f"    triangleCount: {len(tris)}\n  m_MeshCompression: 0\n  m_IndexBuffer: {idx}\n  m_Skin: []\n"
            f"  m_VertexData:\n    m_CurrentChannels: 1\n    m_VertexCount: {len(positions)}\n{streams}"
            f"    m_DataSize: {len(positions) * 12}\n    _typelessdata: {vdata}\n")


def anim_yaml(name, curves):
    """A legacy AnimationClip as AssetRipper writes BB's."""
    def vec(v):
        return "{" + ", ".join(f"{c}: {x!r}" for c, x in zip("xyzw", v)) + "}"
    out = [f"%YAML 1.1\n%TAG !u! tag:unity3d.com,2011:\n--- !u!74 &7400000\nAnimationClip:\n  serializedVersion: 3\n"
           f"  m_Name: {name}\n  m_Compressed: 0\n"]
    for field in ("m_RotationCurves", "m_PositionCurves", "m_ScaleCurves"):
        mine = [c for c in curves if c[0] == field]
        if not mine:
            out.append(f"  {field}: []\n")
            continue
        out.append(f"  {field}:\n")
        for _, path, keys in mine:
            out.append("  - curve:\n      serializedVersion: 2\n      m_Curve:\n")
            for t, v, i, o in keys:
                out.append(f"      - time: {t!r}\n        value: {vec(v)}\n        inSlope: {vec(i)}\n"
                           f"        outSlope: {vec(o)}\n        tangentMode: 0\n")
            out.append(f"      m_PreInfinity: 2\n      m_PostInfinity: 2\n    path: {path}\n")
    out.append("  m_FloatCurves: []\n  m_SampleRate: 30\n  m_WrapMode: 0\n")
    return "".join(out)


def prefab_yaml(objects):
    """objects: [{name, parent (index or None), filter / skin: mesh guid, clips: [clip guids]}] -> prefab YAML."""
    docs = []
    for i, o in enumerate(objects):
        go, tr = 100 + i * 10, 101 + i * 10
        comps = [f"  - 4: {{fileID: {tr}}}\n"]
        father = 0 if o.get("parent") is None else 101 + o["parent"] * 10
        docs.append(f"--- !u!4 &{tr}\nTransform:\n  m_GameObject: {{fileID: {go}}}\n  m_Father: {{fileID: {father}}}\n")
        if o.get("filter"):
            comps.append(f"  - 33: {{fileID: {go + 2}}}\n")
            docs.append(f"--- !u!33 &{go + 2}\nMeshFilter:\n  m_GameObject: {{fileID: {go}}}\n"
                        f"  m_Mesh: {{fileID: 4300000, guid: {o['filter']}, type: 2}}\n")
        if o.get("skin"):
            comps.append(f"  - 137: {{fileID: {go + 3}}}\n")
            docs.append(f"--- !u!137 &{go + 3}\nSkinnedMeshRenderer:\n  m_GameObject: {{fileID: {go}}}\n  m_Enabled: 1\n"
                        f"  m_Mesh: {{fileID: 4300000, guid: {o['skin']}, type: 2}}\n  m_Bones: []\n")
        if o.get("clips"):
            comps.append(f"  - 111: {{fileID: {go + 4}}}\n")
            lines = "".join(f"  - {{fileID: 7400000, guid: {g}, type: 2}}\n" for g in o["clips"])
            docs.append(f"--- !u!111 &{go + 4}\nAnimation:\n  m_GameObject: {{fileID: {go}}}\n  m_Enabled: 1\n"
                        f"  m_Animation: {{fileID: 7400000, guid: {o['clips'][0]}, type: 2}}\n  m_Animations:\n{lines}"
                        f"  m_WrapMode: 0\n")
        docs.insert(0, f"--- !u!1 &{go}\nGameObject:\n  m_Component:\n{''.join(comps)}  m_Name: {o['name']}\n  m_IsActive: 1\n")
    return "%YAML 1.1\n%TAG !u! tag:unity3d.com,2011:\n" + "".join(docs)


def hero_rows(keys, slot):
    """wardrobe_data.py clip_dict: three.js space, rounded to 5 places."""
    sign = {"q": (1, -1, -1, 1), "p": (-1, 1, 1), "s": (1, 1, 1)}[slot]
    return [[round(f32(t), 5)] + [round(f32(x) * s, 5) for part in (v, i, o) for x, s in zip(part, sign)]
            for t, v, i, o in keys]


def prop_rows(keys, slot):
    """extract_tto_props.py clip_keys (6 places) + wardrobe_data.py mirror_rows."""
    neg = {"q": (2, 3, 6, 7, 10, 11), "p": (1, 4, 7)}.get(slot, ())
    rows = [[round(f32(t), 6)] + [round(f32(x), 6) for part in (v, i, o) for x in part] for t, v, i, o in keys]
    return [[-x if k in neg else x for k, x in enumerate(r)] for r in rows]


def prop_mesh(positions, tris):
    """wardrobe_data.py prop_mesh: x mirrored, rounded to 5 places."""
    return {"pos": [round(x, 5) for p in positions for x in (-f32(p[0]), f32(p[1]), f32(p[2]))], "nrm": None, "uv": None,
            "idx": [i for t in tris for i in t], "groups": [[0, len(tris) * 3, 0]]}


class World:
    """A wardrobe source + BB rip for one class (cat), filled by the add_* helpers, written by finish()."""

    def __init__(self, tmp):
        self.tmp = Path(tmp)
        self.src = self.tmp / "comic" / "wardrobe"
        self.data = self.src / "data"
        self.rip = self.tmp / "rip" / "Assets" / "Resources"
        self.assets = self.rip.parent
        self.heroes = self.rip / "gameassets" / "characters" / "heroes"
        self.icon_dir = self.rip / "gamegui" / "icons"
        self.out = self.tmp / "dist"
        self.n_guid = 0
        self.outfits, self.clips, self.faces = [], {}, []
        self.props = {("cat", k): [] for k in ("weapons", "accessories", "trinkets")}
        self.props.update({("all", k): [] for k in ("accessories", "trinkets")})
        self.icons = {"cat": {"outfits": {}, "weapons": {}, "accessories": {}, "trinkets": {}},
                      "all": {"outfits": {}, "weapons": {}, "accessories": {}, "trinkets": {}}}
        self.item_map = {"cat": {"armor": {}, "weapon": {}, "accessory": {}, "trinket": {}}, "all": {"trinket": {}}}
        self.placements = {t: {"cat": {"fallback": PLACE, "entries": {}}} for t in ("weapons", "accessories", "trinkets")}
        self.ui = {"heroes": {}, "emotion": [], "skills": {"cat": []}, "faceBox": {"cat": [0, 0, 256, 256]}}

    def guid(self):
        self.n_guid += 1
        return f"{self.n_guid:032x}"

    def bb_asset(self, path, text):
        """A YAML asset in the BB rip with its .meta (guid); returns the guid."""
        g = self.guid()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        Path(str(path) + ".meta").write_text(f"fileFormatVersion: 2\nguid: {g}\n", encoding="utf-8")
        return g

    def add_outfit(self, name, colors=(1,), editions=None, tto=False):
        mesh = f"Cat_{name}_tri"
        buf = b"".join(struct.pack("<3f", -p[0], p[1], p[2]) for p in TRI)
        idx_at = len(buf)
        buf += b"".join(struct.pack("<3I", *t) for t in TRIS)
        (self.data / "cat").mkdir(parents=True, exist_ok=True)
        (self.data / "cat" / f"o_{name}.bin").write_bytes(buf)
        o = {"name": name, "tto": tto, "colors": list(colors),
             "meshes": [{"verts": len(TRI), "tris": len(TRIS), "bones": [], "ibm": [], "pos": 0, "idx": idx_at, "name": mesh}]}
        if editions:
            o["editions"] = editions
        self.outfits.append(o)
        for c in colors:
            webp(self.data / "cat" / "tex" / f"{name}{c}.webp")
        for e, cs in (editions or {}).items():
            for c in cs:
                webp(self.data / "cat" / "tex" / f"{name}{c}{e}.webp")
        if not tto:
            armors = self.heroes / "cat" / "armors"
            g = self.bb_asset(armors / f"{mesh}.asset", mesh_yaml(mesh, TRI, TRIS))
            (armors / f"Cat_{name}.prefab").write_text(prefab_yaml([{"name": f"Cat_{name}"}, {"name": mesh, "parent": 0, "skin": g}]),
                                                         encoding="utf-8")
            for c in colors:
                png(armors / "materials" / f"Cat_{name}{c}.png")
            for e, cs in (editions or {}).items():
                for c in cs:
                    png(armors / "materials" / f"Cat_{name}{c}{e}.png")

    def add_clip(self, name, group, tto=False, curves=CLIP):
        tracks = {}
        for field, path, keys in curves:
            slot = {"m_RotationCurves": "q", "m_PositionCurves": "p", "m_ScaleCurves": "s"}[field]
            tracks.setdefault(path.rsplit("/", 1)[-1], {})[slot] = hero_rows(keys, slot)
        self.clips[name] = {"len": 1.0, "rate": 30.0, "loop": False, "tracks": tracks, "group": group, "tto": tto}
        if not tto:
            g = self.bb_asset(self.assets / "AnimationClip" / f"{name}_3.anim", anim_yaml(name, curves))
            p = self.heroes / "cat" / "animations" / f"{name}.prefab"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(prefab_yaml([{"name": name, "clips": [g]}]), encoding="utf-8")

    def add_face(self, n, tto=False):
        self.faces.append({"n": n, "tto": tto})
        webp(self.data / "cat" / "faces" / f"{n}.webp")
        if not tto:
            png(self.heroes / "cat" / "armors" / "overlay" / f"Cat{n}.png", size=(256, 256))

    def add_prop(self, kind, name, tex, tto=False, cls="cat", node=None, positions=TRI):
        """A static prop: one node with a mesh (MeshFilter in BB) and one textured material."""
        node = node or name
        n = {"name": node, "parent": -1, "p": [0, 0, 0], "q": [0, 0, 0, 1], "s": [1, 1, 1], "on": True,
             "mesh": prop_mesh(positions, TRIS), "mats": [{"tex": tex, "color": [1, 1, 1, 1]}]}
        self.props[(cls, kind)].append({"name": name, "tto": tto, "mount": "Head", "nodes": [n]})
        if not tto:
            cap = cls.capitalize()
            g = self.bb_asset(self.assets / "Mesh" / f"{cap}_{name}_tri.asset", mesh_yaml(f"{cap}_{name}_tri", positions, TRIS))
            p = self.heroes / cls / kind / f"{name}.prefab"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(prefab_yaml([{"name": node, "filter": g}]), encoding="utf-8")
            png(self.assets / "Texture2D" / tex)

    def add_live_prop(self, kind, name, tex, curves):
        """An animated skinned prop (a wing): root with the Animation, a child "blade" with a live skin."""
        rows = {}
        for field, path, keys in curves:
            slot = {"m_RotationCurves": "q", "m_PositionCurves": "p", "m_ScaleCurves": "s"}[field]
            rows.setdefault("1", {})[slot] = prop_rows(keys, slot)        # every test curve drives node 1, "blade"
        nodes = [{"name": name, "parent": -1, "p": [0, 0, 0], "q": [0, 0, 0, 1], "s": [1, 1, 1], "on": True},
                 {"name": "blade", "parent": 0, "p": [0, 0, 0], "q": [0, 0, 0, 1], "s": [1, 1, 1], "on": True,
                  "skin": dict(prop_mesh(TRI, TRIS), w=[], j=[], ibm=[], bones=[1]),
                  "mats": [{"tex": tex, "color": [1, 1, 1, 1]}]}]
        self.props[("cat", kind)].append({"name": name, "tto": False, "mount": "Spine1", "nodes": nodes,
                                          "anim": {"default": "flap", "clips": {"flap": {"len": 1.0, "rate": 30.0, "loop": True,
                                                                                         "tracks": rows}}}})
        mg = self.bb_asset(self.assets / "Mesh" / f"Cat_{name}_tri.asset", mesh_yaml(f"Cat_{name}_tri", TRI, TRIS))
        cg = self.bb_asset(self.assets / "AnimationClip" / "flap.anim", anim_yaml("flap", curves))
        p = self.heroes / "cat" / kind / f"{name}.prefab"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(prefab_yaml([{"name": name, "clips": [cg]}, {"name": "blade", "parent": 0, "skin": mg}]), encoding="utf-8")
        png(self.assets / "Texture2D" / tex)

    def add_icon(self, cls, slot, name, rel, codes, bb=True):
        """An icons.json entry; the data's copy is TTO's (pink), the BB rip's at gamegui/icons/items/<folder>/<file>.png."""
        self.icons[cls][slot][name] = {"icon": rel, "codes": codes}
        webp(self.data / rel)
        if bb:
            folder, file = rel.split("/")[1:]
            png(self.icon_dir / "items" / folder / (file[:-5] + ".png"))

    def finish(self):
        d = self.data
        dump(d / "cat" / "rig.json", {"tri": {}, "bones": []})
        dump(d / "cat" / "outfits.json", self.outfits)
        dump(d / "cat" / "clips.json", self.clips)
        for (cls, kind), props in self.props.items():
            dump(d / cls / f"props_{kind}.json", props)
        dump(d / "meta.json", {"classes": [{"cls": "cat", "outfits": len(self.outfits), "faces": self.faces,
                                            "clips": {k: {"group": v["group"], "loop": v["loop"], "len": v["len"], "tto": v["tto"]}
                                                      for k, v in self.clips.items()}}]})
        dump(d / "icons.json", self.icons)
        dump(d / "item_map.json", self.item_map)
        dump(d / "placements.json", self.placements)
        dump(d / "ui.json", self.ui)
        dump(d / "item_map_tto.json", {"cat": {"armor": {"a_cat99": ["Cat_ttoGown"]}}})   # not used by the page
        (d / "placement_sweep.md").write_text("ttoGown notes", encoding="utf-8")
        self.src.mkdir(parents=True, exist_ok=True)
        (self.src / "index.html").write_bytes(PAGE.encode("utf-8"))
        for f in ("Prompt-SemiBold.ttf", "Prompt-Bold.ttf"):
            p = self.tmp / "comic" / "fonts" / f
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b"font " + f.encode())
        return self

    def publish(self):
        return wp.publish(self.src, self.out, self.rip)


def make_world(tmp, tto_faces=(30, 31, 32, 33)):
    """The standard test wardrobe: BB outfit a (colour 1 + edition R), TTO outfit ttoGown, BB clips root + wave, TTO
    emote ttoJig, BB faces 0 + 1 and TTO faces 30-33, BB weapon knife and headpiece hat, TTO trinkets ttoFlag (cat) and
    ttoWing (shared), item icons (two without a BB file), a class portrait, emotion icons wave (BB) and clap (TTO)."""
    w = World(tmp)
    w.add_outfit("a", editions={"R": [1]})
    w.add_outfit("ttoGown", tto=True)
    w.add_clip("root", "base")
    w.add_clip("wave", "emote")
    w.add_clip("ttoJig", "emote", tto=True)
    for n in (0, 1):
        w.add_face(n)
    for n in tto_faces:
        w.add_face(n, tto=True)
    w.add_prop("weapons", "knife", "Cat_knife.png")
    w.add_prop("accessories", "hat", "Cat_hat.png")
    w.add_prop("trinkets", "ttoFlag", "Cat_ttoFlag.png", tto=True)
    w.add_prop("trinkets", "ttoWing", "ttoWing.png", tto=True, cls="all")
    w.add_icon("cat", "outfits", "a", "icons/armor/cat1.webp", ["a_cat1"])
    w.icons["cat"]["outfits"]["a"]["editions"] = {"R": "icons/armor/cat1r.webp"}
    webp(w.data / "icons" / "armor" / "cat1r.webp")
    png(w.icon_dir / "items" / "armor" / "cat1r.png")
    w.add_icon("cat", "outfits", "ttoGown", "icons/armor/cat99.webp", ["a_cat99"], bb=False)
    w.add_icon("cat", "weapons", "knife", "icons/weapon/cat1.webp", ["w_cat1"])
    w.add_icon("cat", "accessories", "hat", "icons/accessory/cat2.webp", ["c_cat2"], bb=False)
    w.add_icon("cat", "trinkets", "ttoFlag", "icons/trinket/cat9.webp", ["t_cat9"], bb=False)
    w.add_icon("all", "trinkets", "ttowing", "icons/trinket/all1.webp", ["t_all1"], bb=False)
    w.item_map["cat"].update({"armor": {"a_cat1": ["Cat_a"], "a_cat99": ["Cat_ttoGown"]}, "weapon": {"w_cat1": ["knife"]},
                              "accessory": {"c_cat2": ["hat"]}, "trinket": {"t_cat9": ["ttoFlag"]}})
    w.item_map["all"]["trinket"] = {"t_all1": ["ttowing"]}
    w.placements["weapons"]["cat"]["entries"] = {"w_cat1": PLACE}
    w.placements["accessories"]["cat"]["entries"] = {"c_cat2": PLACE}
    w.placements["trinkets"]["cat"]["entries"] = {"t_cat9": PLACE}
    w.ui["heroes"]["cat"] = "icons/heroes/cat1.webp"
    webp(w.data / "icons" / "heroes" / "cat1.webp")
    png(w.icon_dir / "heroes" / "Cat1.png")                          # BB's portraits are capitalised
    w.ui["emotion"] = ["clap", "wave"]
    w.ui["skills"]["cat"] = ["slash"]
    for rel in ("skills/emotion/clap", "skills/emotion/wave", "skills/cat/slash"):
        webp(w.data / "icons" / (rel + ".webp"))
    png(w.icon_dir / "skills" / "emotion" / "wave.png")
    png(w.icon_dir / "skills" / "cat" / "slash.png")
    return w


def data_dir(w):
    dirs = [p for p in w.out.iterdir() if p.name.startswith("data-")]
    assert len(dirs) == 1, dirs
    return dirs[0]


def dropped_names(result, kind):
    return [d["name"] for d in result["dropped"].get(kind, [])]


def pixels(path):
    with Image.open(path) as im:
        return im.convert("RGBA").getpixel((0, 0))


class PublishTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def world(self, **kw):
        return make_world(self.tmp, **kw).finish()

    def test_page_rewritten(self):
        w = self.world()
        result = w.publish()
        html = (w.out / "index.html").read_text(encoding="utf-8")
        self.assertRegex(html, r'const DATA = "data-[0-9a-f]{10}/";')
        self.assertIn(f'const DATA = "{result["data_dir"]}/";', html)
        self.assertNotIn("no-cache", html)
        self.assertNotIn("คัดลอกให้ Claude", html)
        self.assertNotIn('$("copy")', html)
        self.assertEqual(html.count("data-goatcounter="), 1)
        settings = re.search(r"data-goatcounter-settings='(\{[^']*\})'", html)
        self.assertIsNotNone(settings)
        self.assertEqual(json.loads(settings.group(1))["path"], "/wardrobe/")
        self.assertIn('href="https://jumpptty.github.io/12tails/12t_projects/bible/"', html)
        self.assertEqual(wp.check(w.out), [])

    def test_hash_changes_with_content(self):
        w = self.world()
        first = w.publish()["data_dir"]
        self.assertEqual(w.publish()["data_dir"], first)          # the same data gives the same folder
        rig = w.data / "cat" / "rig.json"
        b = bytearray(rig.read_bytes())
        b[-1:] = b" }"
        rig.write_bytes(bytes(b))
        self.assertNotEqual(w.publish()["data_dir"], first)

    def test_republish_keeps_one_data_folder(self):
        w = self.world()
        w.publish()
        (w.data / "cat" / "rig.json").write_text('{"tri": {}, "bones": [], "x": 1}', encoding="utf-8")
        w.publish()
        self.assertEqual(len([p for p in w.out.iterdir() if p.name.startswith("data-")]), 1)
        self.assertFalse(any(p.name.startswith(".") for p in w.out.iterdir()))   # no staging folder left behind

    def test_headers_file(self):
        w = self.world()
        result = w.publish()
        rules, path = {}, None
        for line in (w.out / "_headers").read_text(encoding="utf-8").splitlines():
            if line and not line.startswith((" ", "\t")):
                path = line.strip()
                rules[path] = []
            elif line.strip():
                rules[path].append(line.strip())
        # one splat per rule (Cloudflare: "You may only include a single splat in the URL"), so the rule names the
        # current data folder; any data-* folder is immutable
        self.assertEqual(rules[f"/{result['data_dir']}/*"], ["Cache-Control: public, max-age=31536000, immutable"])
        self.assertEqual(rules["/"], ["Cache-Control: no-cache"])

    def test_case_mismatch_is_reported(self):
        w = self.world()
        w.publish()
        d = data_dir(w)
        outfits = json.loads((d / "cat" / "outfits.json").read_text(encoding="utf-8"))
        outfits[0]["name"] = "A"                                 # the page now asks for cat/tex/A1.webp
        (d / "cat" / "outfits.json").write_text(json.dumps(outfits), encoding="utf-8")
        problems = wp.check(w.out)
        hit = [p for p in problems if "cat/tex/A1.webp" in p]
        self.assertEqual(len(hit), 1, problems)
        self.assertIn("cat/tex/a1.webp", hit[0])

    def test_limits_reported(self):
        w = self.world()
        w.publish()
        d = data_dir(w)
        with open(d / "big.bin", "wb") as f:
            f.truncate(26 * 1024 * 1024)
        problems = wp.check(w.out)
        self.assertTrue(any("big.bin" in p and "25 MiB" in p for p in problems), problems)
        (d / "big.bin").unlink()
        many = w.out / "many"
        many.mkdir()
        for i in range(20_001):
            open(many / f"{i}", "wb").close()
        problems = wp.check(w.out)
        self.assertTrue(any("20,000" in p for p in problems), problems)

    def test_bb_only_leaves_no_references(self):
        w = self.world()
        result = w.publish()
        names = ("ttoGown", "ttoJig", "ttoFlag", "ttoWing", "ttowing", "cat99", "a_cat99", "t_cat9", "t_all1")
        for p in w.out.rglob("*"):
            self.assertFalse(any(n.lower() in p.name.lower() for n in names), p)
            if p.suffix in (".json", ".html", ".md"):
                text = p.read_text(encoding="utf-8")
                for n in names:
                    self.assertNotIn(n, text, f"{p.name} still names {n}")
        self.assertFalse(list(w.out.rglob("item_map_tto.json")))        # files the page doesn't use stay out
        self.assertFalse(list(w.out.rglob("placement_sweep.md")))
        self.assertIn("cat/ttoGown", dropped_names(result, "outfits"))
        self.assertIn("cat/ttoJig", dropped_names(result, "emotes"))
        self.assertIn("cat/ttoFlag", dropped_names(result, "back_trinkets"))
        self.assertIn("all/ttoWing", dropped_names(result, "back_trinkets"))
        self.assertEqual(json.loads((data_dir(w) / "all" / "props_trinkets.json").read_text()), [])
        self.assertEqual(wp.check(w.out), [])

    def test_tto_faces_first_half(self):
        w = self.world()
        result = w.publish()
        faces = data_dir(w) / "cat" / "faces"
        self.assertEqual(sorted(p.name for p in faces.iterdir()), ["0.webp", "1.webp", "30.webp", "31.webp"])
        self.assertEqual(result["tto_faces"], {"cat": [30, 31]})
        meta = json.loads((data_dir(w) / "meta.json").read_text())
        self.assertEqual([f["n"] for f in meta["classes"][0]["faces"]], [0, 1, 30, 31])
        self.assertEqual(pixels(faces / "0.webp"), BB_RGBA)              # BB's faces are taken from the BB rip
        self.assertEqual(sorted(dropped_names(result, "faces")), ["cat/32", "cat/33"])

    def test_tto_faces_first_half_rounds_down(self):
        w = make_world(self.tmp, tto_faces=(30, 31, 32)).finish()
        result = w.publish()
        self.assertEqual(result["tto_faces"], {"cat": [30]})
        self.assertEqual(sorted(p.name for p in (data_dir(w) / "cat" / "faces").iterdir()), ["0.webp", "1.webp", "30.webp"])

    def test_icons_from_bb_rip(self):
        w = self.world()
        result = w.publish()
        d = data_dir(w)
        knife = d / "icons" / "weapon" / "cat1.webp"
        with Image.open(knife) as a, Image.open(w.icon_dir / "items" / "weapon" / "cat1.png") as b:
            self.assertEqual(a.convert("RGBA").tobytes(), b.convert("RGBA").tobytes())
        self.assertEqual(pixels(d / "icons" / "heroes" / "cat1.webp"), BB_RGBA)
        self.assertFalse((d / "icons" / "accessory" / "cat2.webp").exists())          # hat's icon has no BB file
        icons = json.loads((d / "icons.json").read_text())
        self.assertIsNone(icons["cat"]["accessories"]["hat"]["icon"])                    # its tile shows no picture
        self.assertEqual(icons["cat"]["accessories"]["hat"]["codes"], ["c_cat2"])       # the codes still place it
        self.assertIn("icons/accessory/cat2.webp", dropped_names(result, "icons"))
        ui = json.loads((d / "ui.json").read_text())
        self.assertEqual(ui["emotion"], ["wave"])                                      # TTO's clap icon is gone
        self.assertFalse((d / "icons" / "skills" / "emotion" / "clap.webp").exists())
        self.assertEqual(pixels(d / "icons" / "skills" / "emotion" / "wave.webp"), BB_RGBA)
        self.assertEqual(wp.check(w.out), [])

    def test_outfit_textures_from_bb_rip(self):
        w = self.world()
        w.publish()
        tex = data_dir(w) / "cat" / "tex"
        self.assertEqual(sorted(p.name for p in tex.iterdir()), ["a1.webp", "a1R.webp"])
        for f in ("a1.webp", "a1R.webp"):
            got = pixels(tex / f)
            self.assertTrue(all(abs(g - b) <= 6 for g, b in zip(got, BB_RGBA)), (f, got))   # lossy WebP of BB's PNG

    def test_mismatched_mesh_is_dropped(self):
        w = make_world(self.tmp)
        moved = [(x + 0.5, y, z) for x, y, z in TRI]
        (w.heroes / "cat" / "armors" / "Cat_a_tri.asset").write_text(mesh_yaml("Cat_a_tri", moved, TRIS), encoding="utf-8")
        (w.assets / "Mesh" / "Cat_knife_tri.asset").write_text(mesh_yaml("Cat_knife_tri", TRI, TRIS[:1]), encoding="utf-8")
        w.finish()
        result = w.publish()
        d = data_dir(w)
        self.assertIn("cat/a", dropped_names(result, "outfits"))
        self.assertIn("mesh", next(x["reason"] for x in result["dropped"]["outfits"] if x["name"] == "cat/a"))
        self.assertIn("cat/knife", dropped_names(result, "weapons"))
        self.assertFalse((d / "cat" / "o_a.bin").exists())
        self.assertFalse((d / "cat" / "tex").exists())
        self.assertEqual(json.loads((d / "cat" / "outfits.json").read_text()), [])
        icons = json.loads((d / "icons.json").read_text())
        self.assertNotIn("a", icons["cat"]["outfits"])
        self.assertNotIn("knife", icons["cat"]["weapons"])
        self.assertEqual(json.loads((d / "item_map.json").read_text())["cat"]["weapon"], {})
        self.assertEqual(wp.check(w.out), [])

    def test_mismatched_clip_is_dropped(self):
        w = make_world(self.tmp)
        changed = [(f, p, [(t + 0.25, v, i, o) for t, v, i, o in keys]) for f, p, keys in CLIP]
        (w.assets / "AnimationClip" / "wave_3.anim").write_text(anim_yaml("wave", changed), encoding="utf-8")
        w.finish()
        result = w.publish()
        d = data_dir(w)
        self.assertIn("cat/wave", dropped_names(result, "emotes"))
        self.assertEqual(sorted(json.loads((d / "cat" / "clips.json").read_text())), ["root"])
        self.assertEqual(sorted(json.loads((d / "meta.json").read_text())["classes"][0]["clips"]), ["root"])

    def test_prop_without_bb_texture_is_dropped(self):
        w = self.world()
        (w.assets / "Texture2D" / "Cat_hat.png").unlink()
        result = w.publish()
        d = data_dir(w)
        reason = next(x["reason"] for x in result["dropped"]["headpieces"] if x["name"] == "cat/hat")
        self.assertIn("Cat_hat.png", reason)
        self.assertEqual(json.loads((d / "cat" / "props_accessories.json").read_text()), [])
        self.assertNotIn("hat", json.loads((d / "icons.json").read_text())["cat"]["accessories"])
        self.assertEqual(sorted(p.name for p in (d / "props" / "tex").iterdir()), ["Cat_knife.png"])

    def test_uncomparable_prop_is_dropped(self):
        w = make_world(self.tmp)
        w.add_prop("accessories", "lantern", "Cat_lantern.png", node="baked_lantern")   # posed by the extractor
        w.finish()
        result = w.publish()
        reason = next(x["reason"] for x in result["dropped"]["headpieces"] if x["name"] == "cat/lantern")
        self.assertIn("cannot be compared", reason)

    def test_animated_prop_clips_compared(self):
        wing = [("m_RotationCurves", "Cat_wing_tri/blade", [(0.0, (0.0, 0.5, 0.0, 0.75), (0, 0, 0, 0), (0, 0, 0, 0)),
                                                            (0.5, (0.25, 0.5, 0.0, 0.75), (0, 0, 0, 0), (0, 0, 0, 0))])]
        w = make_world(self.tmp)
        w.add_live_prop("trinkets", "wing", "Cat_wing.png", wing)
        w.finish()
        result = w.publish()
        kept = json.loads((data_dir(w) / "cat" / "props_trinkets.json").read_text())
        self.assertEqual([p["name"] for p in kept], ["wing"], result["dropped"])
        changed = [(f, p, [(t, (v[0] + 0.5,) + v[1:], i, o) for t, v, i, o in keys]) for f, p, keys in wing]
        (w.assets / "AnimationClip" / "flap.anim").write_text(anim_yaml("flap", changed), encoding="utf-8")
        result = w.publish()
        self.assertIn("cat/wing", dropped_names(result, "back_trinkets"))

    def test_fonts_and_prop_textures_rewritten(self):
        w = self.world()
        w.publish()
        html = (w.out / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("../fonts/", html)
        self.assertNotIn("../props/tex/", html)
        self.assertIn('url("fonts/Prompt-SemiBold.ttf")', html)
        self.assertIn("texLoader.load(`${DATA}props/tex/${m.tex}`)", html)
        for f in ("Prompt-SemiBold.ttf", "Prompt-Bold.ttf"):
            self.assertEqual((w.out / "fonts" / f).read_bytes(), (self.tmp / "comic" / "fonts" / f).read_bytes())
        knife = data_dir(w) / "props" / "tex" / "Cat_knife.png"
        self.assertEqual(knife.read_bytes(), (w.assets / "Texture2D" / "Cat_knife.png").read_bytes())

    def test_missing_anchor_fails_loudly(self):
        anchors = ['const DATA = "data/";', 'fetch(p, { cache: "no-cache" })',
                   '<button type="button" class="primary" id="copy">คัดลอกให้ Claude</button>',
                   '$("copy").onclick = async () => {', 'url("../fonts/', "texLoader.load(`../props/tex/${m.tex}`)"]
        w = self.world()
        for anchor in anchors:
            with self.subTest(anchor=anchor):
                (w.src / "index.html").write_bytes(PAGE.replace(anchor, "changed").encode("utf-8"))
                with self.assertRaises(wp.PublishError) as e:
                    w.publish()
                self.assertIn("anchor", str(e.exception))
                self.assertFalse(w.out.exists())                     # nothing is written for a changed page

    def test_outfit_without_colours_is_a_warning(self):
        w = make_world(self.tmp)
        w.add_outfit("novice", colors=())
        w.finish()
        result = w.publish()
        self.assertTrue(any("cat/novice" in x for x in result["warnings"]), result["warnings"])
        self.assertIn("novice", [o["name"] for o in json.loads((data_dir(w) / "cat" / "outfits.json").read_text())])
        self.assertEqual(wp.check(w.out), [])


if __name__ == "__main__":
    unittest.main()
