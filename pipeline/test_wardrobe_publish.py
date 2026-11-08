r"""Tests for wardrobe_publish.py. Each test builds a tiny wardrobe (page + data/) and a tiny BB rip (AssetRipper YAML
meshes, clips and prefabs, PNG pictures) in a temp folder, publishes it and reads the result.

  cd /d D:\12tails-video\comic-skit && py -3 -m unittest pipeline.test_wardrobe_publish -v
"""
import contextlib
import io
import json
import math
import os
import re
import shutil
import struct
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

from PIL import Image

from pipeline import wardrobe_publish as wp

# the page's anchors exactly as wardrobe/index.html has them (LF, like the real page; the page tests run on a CRLF
# copy too: NEWLINES)
PAGE = """<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<title>ห้องแต่งตัว · 12 Tails</title>
<link rel="icon" href="wardrobe_icon.svg" type="image/svg+xml">
<link href="https://fonts.googleapis.com/css2?family=Prompt:wght@400;700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<style>
.bar button { border: 0; }
</style>
</head>
<body>
  <aside>
    <header class="brand"><span class="brand-mark" id="bible">12 Tails Bible</span><h1>ห้องแต่งตัว</h1></header>
  </aside>
    <div class="bar">
      <button type="button" class="tb primary" id="shot">บันทึกภาพ</button>
      <span class="tb-sep" aria-hidden="true"></span><button type="button" class="tb txt" id="copy">คัดลอกให้ Claude</button>
    </div>
<script type="module">
const DATA = "data/";
const UI_DIR = "ui/";
const colorIcon = c => `${UI_DIR}recolor${c}.webp`;
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
"""
NEWLINES = (("LF", "\n"), ("CRLF", "\r\n"))
PAGE_FILES = {"wardrobe_icon.svg": b'<svg xmlns="http://www.w3.org/2000/svg"></svg>', "wardrobe.ico": b"\0\0\1\0ico"}

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


def recolor(w, n, shade=0, name=None):
    """BB's Recolor Drug n in the rip (64 px, a gradient with a transparent corner) and the page's copy of it in src/ui:
    a 2x upscale cropped to the potions' square (wp.UI_CROP), brightened by `shade` (0 = a faithful copy)."""
    bb = Image.new("RGBA", (64, 64))
    bb.putdata([(40 + 3 * x, 20 + 2 * y, 90 + n * 20, 0 if x < 6 and y < 6 else 255) for y in range(64) for x in range(64)])
    (w.icon_dir / "items" / "field").mkdir(parents=True, exist_ok=True)
    bb.save(w.icon_dir / "items" / "field" / f"rsc{n}.png")
    big = bb.resize((128, 128), Image.LANCZOS).crop(tuple(2 * v for v in wp.UI_CROP))
    if shade:
        big = Image.eval(big.convert("RGB"), lambda v: min(255, v + shade)).convert("RGBA")
    dst = w.src / "ui" / (name or f"recolor{n}.webp")
    dst.parent.mkdir(parents=True, exist_ok=True)
    big.save(dst, "WEBP", quality=90)


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

    def __init__(self, tmp, nl="\n"):
        self.tmp, self.nl = Path(tmp), nl                # nl: the page's line endings
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
        self.write_page(PAGE)
        for name, b in PAGE_FILES.items():
            (self.src / name).write_bytes(b)
        for n in range(1, 6):                           # the colour topic's pictures (the page needs all five)
            recolor(self, n)
        return self

    def write_page(self, page):
        (self.src / "index.html").write_bytes(page.replace("\n", self.nl).encode("utf-8"))

    def publish(self, data=None):
        return wp.publish(self.src, self.out, self.rip, data)


def make_world(tmp, tto_faces=(30, 31, 32, 33), nl="\n"):
    """The standard test wardrobe: BB outfit a (colour 1 + edition R), TTO outfit ttoGown, BB clips root + wave, TTO
    emote ttoJig, BB faces 0 + 1 and TTO faces 30-33, BB weapon knife and headpiece hat, TTO trinkets ttoFlag (cat) and
    ttoWing (shared), item icons (two without a BB file), a class portrait, emotion icons wave (BB) and clap (TTO)."""
    w = World(tmp, nl)
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


def tree(folder):
    """{relative path: bytes} of every file under folder, and every folder (bytes None)."""
    return {p.relative_to(folder).as_posix(): (p.read_bytes() if p.is_file() else None) for p in Path(folder).rglob("*")}


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

    def newline_worlds(self):
        """The standard world twice: an LF page (like the real one) and a CRLF page, each in its own folder."""
        return [(label, make_world(self.tmp / label, nl=nl).finish()) for label, nl in NEWLINES]

    def test_ui_pictures_published_in_a_hashed_folder(self):
        """The colour pictures go to ui-<hash>/ (the page's UI_DIR points there), proven against BB's icons."""
        w = self.world()
        result = w.publish()
        self.assertRegex(result["ui_dir"], r"^ui-[0-9a-f]{10}$")
        self.assertEqual(result["ui_files"], [f"recolor{n}.webp" for n in range(1, 6)])
        self.assertIn("ui-<hash>/recolor1-5.webp", wp.PROVENANCE)
        for n in range(1, 6):
            self.assertEqual((w.out / result["ui_dir"] / f"recolor{n}.webp").read_bytes(), (w.src / "ui" / f"recolor{n}.webp").read_bytes())
        self.assertFalse((w.out / "ui").exists())
        self.assertIn(f'const UI_DIR = "{result["ui_dir"]}/";', (w.out / "index.html").read_text(encoding="utf-8"))
        self.assertEqual(wp.check(w.out), [])
        (w.out / result["ui_dir"] / "recolor1.webp").unlink()
        self.assertIn(f"missing: {result['ui_dir']}/recolor1.webp", wp.check(w.out))

    def test_ui_folder_name_follows_its_pictures(self):
        """The same pictures give the same folder; a changed one a new folder, and the old folder goes."""
        w = self.world()
        first = w.publish()["ui_dir"]
        self.assertEqual(w.publish()["ui_dir"], first)
        recolor(w, 3, shade=2)                              # still within the proof's limit, but other bytes
        second = w.publish()["ui_dir"]
        self.assertNotEqual(second, first)
        self.assertEqual([p.name for p in w.out.iterdir() if p.name.startswith("ui")], [second])

    def test_ui_recolor_icon_that_is_not_bb_fails_loudly(self):
        w = self.world()
        recolor(w, 2, shade=40)                            # a different picture: far from rsc2.png
        with self.assertRaises(wp.PublishError) as e:
            w.publish()
        self.assertIn("recolor2.webp is not BB's Recolor Drug 2", str(e.exception))
        self.assertFalse(w.out.exists())
        recolor(w, 2)
        recolor(w, 3, name="recolor7.webp")                # no BB counterpart
        with self.assertRaises(wp.PublishError) as e:
            w.publish()
        self.assertIn("recolor7.webp", str(e.exception))
        (w.src / "ui" / "recolor7.webp").unlink()
        (w.src / "ui" / "recolor4.webp").unlink()          # the page shows five colours: all five are needed
        with self.assertRaises(wp.PublishError) as e:
            w.publish()
        self.assertIn("recolor4.webp", str(e.exception))
        recolor(w, 4)
        (w.icon_dir / "items" / "field" / "rsc1.png").unlink()      # BB file missing
        with self.assertRaises(wp.PublishError) as e:
            w.publish()
        self.assertIn("rsc1.png", str(e.exception))
        self.assertFalse(w.out.exists())

    def test_page_rewritten(self):
        for label, w in self.newline_worlds():
            with self.subTest(page=label):
                result = w.publish()
                with open(w.out / "index.html", encoding="utf-8", newline="") as fh:
                    raw = fh.read()
                if w.nl == "\n":
                    self.assertNotIn("\r", raw)                   # the page keeps its own line endings
                else:
                    self.assertEqual(raw.count("\r\n"), raw.count("\n"))
                html = raw.replace("\r\n", "\n")
                self.assertRegex(html, r'const DATA = "data-[0-9a-f]{10}/";')
                self.assertIn(f'const DATA = "{result["data_dir"]}/";', html)
                self.assertNotIn("no-cache", html)
                self.assertNotIn("คัดลอกให้ Claude", html)
                self.assertNotIn('$("copy")', html)
                self.assertNotIn("navigator.clipboard", html)
                self.assertIn("function err(e)", html)               # the code after the copy handler stays
                self.assertEqual(html.count("data-goatcounter="), 1)
                settings = re.search(r"data-goatcounter-settings='(\{[^']*\})'", html)
                self.assertIsNotNone(settings)
                self.assertEqual(json.loads(settings.group(1))["path"], "/wardrobe/")
                # the Bible link (task 14b ruling R66): the mark in the panel's lockup, opening in a new tab; the toolbar
                # keeps neither a link nor the copy button's divider
                self.assertIn('<header class="brand"><a class="brand-mark" id="bible" href="https://jumpptty.github.io/12tails/12t_projects/bible/"'
                              ' target="_blank" rel="noopener">12 Tails Bible</a><h1>', html)
                self.assertEqual(html.count('id="bible"'), 1)
                bar = html[html.index('<div class="bar">'):html.index("</div>", html.index('<div class="bar">'))]
                self.assertNotIn("bible", bar)
                self.assertNotIn("tb-sep", bar)
                self.assertNotIn('id="copy"', html)
                self.assertIn(f'const UI_DIR = "{result["ui_dir"]}/";', html)
                self.assertIn("https://fonts.googleapis.com/css2?family=Prompt", html)   # the fonts come from Google Fonts
                self.assertIn('<link rel="icon" href="wardrobe_icon.svg" type="image/svg+xml">', html)
                self.assertEqual(wp.check(w.out), [])

    def test_copy_handler_cut_short_fails_loudly(self):
        """The handler is cut at its first "};" line: one inside it would leave the clipboard code in the page."""
        for label, w in self.newline_worlds():
            with self.subTest(page=label):
                w.write_page(PAGE.replace("  const s = C.state;\n", "  const s = C.state;\n};\nconst later = async () => {\n"))
                with self.assertRaises(wp.PublishError) as e:
                    w.publish()
                self.assertIn("navigator.clipboard", str(e.exception))
                self.assertFalse(w.out.exists())

    def test_tab_icon_published(self):
        w = self.world()
        w.publish()
        for name, b in PAGE_FILES.items():
            self.assertEqual((w.out / name).read_bytes(), b, name)        # next to the page, as in wardrobe/
        self.assertEqual(wp.check(w.out), [])
        (w.out / "wardrobe_icon.svg").unlink()
        self.assertIn("missing: wardrobe_icon.svg", wp.check(w.out))
        (w.src / "wardrobe_icon.svg").unlink()
        shutil.rmtree(w.out)
        with self.assertRaises(wp.PublishError) as e:
            w.publish()
        self.assertIn("wardrobe_icon.svg", str(e.exception))
        self.assertFalse(w.out.exists())                                  # nothing is written without the icon

    def test_page_without_tab_icon_is_reported(self):
        w = self.world()
        w.publish()
        page = w.out / "index.html"
        page.write_text(page.read_text(encoding="utf-8").replace('<link rel="icon" href="wardrobe_icon.svg" type="image/svg+xml">\n', ""),
                        encoding="utf-8")
        self.assertTrue(any("no tab icon" in p for p in wp.check(w.out)), wp.check(w.out))

    def test_data_folder_apart_from_the_page(self):
        """--data: a src folder with no data/ plus a data folder elsewhere gives the combined layout's output."""
        w = self.world()
        w.publish()
        combined = tree(w.out)
        apart = self.tmp / "elsewhere" / "data"
        apart.parent.mkdir()
        shutil.move(str(w.data), str(apart))
        self.assertFalse((w.src / "data").exists())
        out2 = self.tmp / "dist2"
        result = wp.publish(w.src, out2, w.rip, data=apart)
        self.assertEqual(tree(out2), combined)
        self.assertEqual(result["data_dir"], data_dir(w).name)
        self.assertEqual(wp.check(out2), [])
        with self.assertRaises(wp.PublishError) as e:                  # without --data the src's own data/ is used
            w.publish()
        self.assertIn("no wardrobe data", str(e.exception))
        self.assertEqual(tree(w.out), combined)                          # and the previous copy is left alone

    def test_failed_swap_keeps_previous_output(self):
        """A failure while the new copy replaces the old one (moving the old page aside, the staging rename, the tab
        icon's copy) puts the old one back and leaves no .data-staging / .previous folder for wrangler to upload."""
        real_rename, real_copy2 = Path.rename, shutil.copy2

        def rename(self, target):
            if self.name == ".data-staging":
                raise OSError("simulated: the staging folder is locked")
            return real_rename(self, target)

        def rename_old_page(self, target):
            if self.name == "index.html" and Path(target).parent.name == ".previous":
                raise OSError("simulated: the old page is open in an editor")
            return real_rename(self, target)

        def copy2(src, dst, **kw):
            if Path(dst).name == "wardrobe_icon.svg":
                raise OSError("simulated: disk full")
            return real_copy2(src, dst, **kw)
        w = self.world()
        old_dir = w.publish()["data_dir"]
        before = tree(w.out)
        (w.data / "cat" / "rig.json").write_text('{"tri": {}, "bones": [], "x": 1}', encoding="utf-8")   # a new hash
        for what, patch in (("moving the old page aside", mock.patch.object(Path, "rename", rename_old_page)),
                            ("staging rename", mock.patch.object(Path, "rename", rename)),
                            ("icon copy", mock.patch.object(wp.shutil, "copy2", copy2))):
            with self.subTest(failure=what):
                with patch, self.assertRaises(OSError):
                    w.publish()
                self.assertEqual(tree(w.out), before)
        self.assertNotEqual(w.publish()["data_dir"], old_dir)               # the next run goes through
        self.assertEqual(sorted(p.name for p in w.out.iterdir() if p.name.startswith((".", "data-"))), [data_dir(w).name])

    def test_republish_removes_an_older_publish_s_fonts_and_ui_folders(self):
        """An output written before task 14b has fonts/ (the self-hosted Prompt) and an unhashed ui/: both go."""
        w = self.world()
        for rel in ("fonts/Prompt-Bold.ttf", "ui/recolor1.webp"):
            (w.out / rel).parent.mkdir(parents=True, exist_ok=True)
            (w.out / rel).write_bytes(b"old")
        result = w.publish()
        self.assertFalse((w.out / "fonts").exists())
        self.assertFalse((w.out / "ui").exists())
        self.assertTrue((w.out / result["ui_dir"] / "recolor1.webp").is_file())

    def test_report_keeps_previous_and_prints_changes(self):
        w = self.world()
        args = ["--src", str(w.src), "--data", str(w.data), "--out", str(w.out), "--bb-rip", str(w.rip)]
        report, prev = self.tmp / "dist_report.json", self.tmp / "dist_report.prev.json"
        first_out = io.StringIO()
        with contextlib.redirect_stdout(first_out):
            self.assertEqual(wp.main(args), 0)
        self.assertIn("changes: no previous report to compare with", first_out.getvalue())
        self.assertFalse(prev.exists())
        first = json.loads(report.read_text(encoding="utf-8"))
        (w.assets / "Texture2D" / "Cat_hat.png").unlink()             # the hat goes: one headpiece more, one file less
        second_out = io.StringIO()
        with contextlib.redirect_stdout(second_out):
            self.assertEqual(wp.main(args), 0)
        self.assertEqual(json.loads(prev.read_text(encoding="utf-8")), first)
        second = json.loads(report.read_text(encoding="utf-8"))
        text = second_out.getvalue()
        self.assertIn("changes since the previous report (dist_report.prev.json):\n", text)
        self.assertIn(f"  files: {first['files']:,} -> {second['files']:,} (-1)\n", text)
        self.assertIn("  dropped headpieces: 0 -> 1 (+1)\n", text)
        self.assertNotIn("kept TTO faces cat", text.split("changes since")[1])   # unchanged counts are not listed
        third_out = io.StringIO()
        with contextlib.redirect_stdout(third_out):
            self.assertEqual(wp.main(args), 0)
        self.assertIn("changes since the previous report (dist_report.prev.json): none\n", third_out.getvalue())

    def test_count_changes(self):
        prev = {"files": 10, "bytes": 5000, "dropped": {"outfits": [1, 2], "faces": [1]}, "tto_faces": {"cat": [30, 31], "wolf": [23]}}
        cur = {"files": 9, "bytes": 5000, "dropped": {"outfits": [1, 2, 3], "emotes": [1]}, "tto_faces": {"cat": [30, 31]}}
        self.assertEqual(wp.count_changes(prev, cur), ["files: 10 -> 9 (-1)", "dropped emotes: 0 -> 1 (+1)",
                                                       "dropped faces: 1 -> 0 (-1)", "dropped outfits: 2 -> 3 (+1)",
                                                       "kept TTO faces wolf: 1 -> 0 (-1)"])
        self.assertEqual(wp.count_changes(cur, cur), [])

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
        # one splat per rule (Cloudflare: "You may only include a single splat in the URL"), so each rule names the
        # current folder; the data and ui folders are named by their content's hash, so both are immutable for a year
        self.assertEqual(rules[f"/{result['data_dir']}/*"], ["Cache-Control: public, max-age=31536000, immutable"])
        self.assertEqual(rules[f"/{result['ui_dir']}/*"], ["Cache-Control: public, max-age=31536000, immutable"])
        self.assertEqual(rules["/"], ["Cache-Control: no-cache"])
        self.assertEqual(len(rules), 3)
        headers = w.out / "_headers"
        headers.write_text(headers.read_text(encoding="utf-8").replace(f"/{result['ui_dir']}/*", "/ui/*"), encoding="utf-8")
        self.assertTrue(any("ui pictures would not be cached" in p for p in wp.check(w.out)), wp.check(w.out))

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

    def test_released_classes_keep_every_tto_face(self):
        class Run:
            def __init__(self):
                self.copied, self.dropped = [], []
                self.bb = types.SimpleNamespace(heroes=Path("none"))
            def copy(self, rel):
                self.copied.append(rel)
            def drop(self, kind, name, why):
                self.dropped.append(name)
        faces = [{"n": n, "tto": True} for n in (30, 31, 32, 33)]
        out = {}
        for cls in ("bison", "cat"):
            run = Run()
            kept, nums = wp.publish_faces(run, cls, faces)
            out[cls] = nums
            self.assertEqual([f["n"] for f in kept], nums)
        self.assertEqual(out, {"bison": [30, 31, 32, 33], "cat": [30, 31]})

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

    def test_prop_textures_rewritten_and_no_font_files(self):
        """The page takes its fonts from Google Fonts (the Bible's sheet, task 14b ruling R65): no fonts/ is written."""
        for label, w in self.newline_worlds():
            with self.subTest(page=label):
                w.publish()
                html = (w.out / "index.html").read_text(encoding="utf-8")
                self.assertNotIn("../", html)
                self.assertIn("texLoader.load(`${DATA}props/tex/${m.tex}`)", html)
                self.assertFalse((w.out / "fonts").exists())
                knife = data_dir(w) / "props" / "tex" / "Cat_knife.png"
                self.assertEqual(knife.read_bytes(), (w.assets / "Texture2D" / "Cat_knife.png").read_bytes())

    def test_page_with_local_fonts_fails_loudly(self):
        """A page that still loads the self-hosted fonts (../fonts/) would 404 online: the publish stops."""
        w = self.world()
        w.write_page(PAGE.replace("<style>\n", '<style>\n@font-face { font-family: "Prompt"; src: url("../fonts/Prompt-Bold.ttf"); }\n'))
        with self.assertRaises(wp.PublishError) as e:
            w.publish()
        self.assertIn("'../'", str(e.exception))
        self.assertFalse(w.out.exists())

    def test_missing_anchor_fails_loudly(self):
        anchors = ['const DATA = "data/";', 'const UI_DIR = "ui/";', 'fetch(p, { cache: "no-cache" })',
                   '<span class="tb-sep" aria-hidden="true"></span><button type="button" class="tb txt" id="copy">คัดลอกให้ Claude</button>',
                   '<span class="brand-mark" id="bible">12 Tails Bible</span>',
                   '$("copy").onclick = async () => {', "texLoader.load(`../props/tex/${m.tex}`)"]
        for label, w in self.newline_worlds():
            for anchor in anchors:
                with self.subTest(page=label, anchor=anchor):
                    w.write_page(PAGE.replace(anchor, "changed"))
                    with self.assertRaises(wp.PublishError) as e:
                        w.publish()
                    self.assertIn("anchor", str(e.exception))
                    self.assertFalse(w.out.exists())                 # nothing is written for a changed page

    def test_outfit_without_colours_is_dropped(self):
        """Ruling R24: an outfit whose colors is [] (a wardrobe_data.py bug) cannot be dressed, so it goes with its
        files and every reference."""
        w = make_world(self.tmp)
        w.add_outfit("novice", colors=())
        w.add_icon("cat", "outfits", "novice", "icons/armor/cat5.webp", ["a_cat5"])
        w.item_map["cat"]["armor"]["a_cat5"] = ["Cat_novice"]
        w.finish()
        result = w.publish()
        self.assertEqual([x["reason"] for x in result["dropped"]["outfits"] if x["name"] == "cat/novice"],
                         ["no colours: cannot be dressed"])
        self.assertEqual(result["warnings"], [])
        d = data_dir(w)
        self.assertEqual([o["name"] for o in json.loads((d / "cat" / "outfits.json").read_text())], ["a"])
        self.assertFalse((d / "cat" / "o_novice.bin").exists())
        self.assertFalse((d / "icons" / "armor" / "cat5.webp").exists())
        for p in d.rglob("*.json"):
            self.assertNotIn("novice", p.read_text(encoding="utf-8"), p.name)
            self.assertNotIn("a_cat5", p.read_text(encoding="utf-8"), p.name)
        self.assertEqual(wp.check(w.out), [])


if __name__ == "__main__":
    unittest.main()
