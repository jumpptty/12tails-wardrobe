r"""The public copy of the 12 Tails Wardrobe, for Cloudflare Pages (plan docs/superpowers/plans/2026-11-07-wardrobe-online.md
in the Bible repo, Task 1).

  py -3 pipeline/wardrobe_publish.py [--src <repo>\wardrobe] [--out <repo>\wardrobe_dist]
                                     [--bb-rip D:\12tails\RippedAssets\ExportedProject\Assets\Resources]
  py -3 pipeline/wardrobe_publish.py --check <dir>
  -> <out>\index.html, <out>\fonts\, <out>\data-<hash>\, <out>\_headers, and <out>_report.json beside it (every
     dropped item with the reason, the kept TTO faces, warnings, check problems). Exit 1 when check() finds problems.

The user's content rule (2026-11-07): "BB 3D models only; the only thing you may bring from TTO are face paints, 50% of
their own face paints." wardrobe_data.py and extract_tto_props.py extract every outfit, clip and prop from TTO's
bundles, BB's own items included, so an item is published only when
  - its tto flag is false (wardrobe_data.py: outfits not among BB's armor prefabs, clips that are bare AnimationClips;
    extract_tto_props.py tto_new: props not among BB's prefabs), and
  - each of its 3D files equals BB's client data in the BB rip (AssetRipper YAML, read here without PyYAML): an
    outfit's meshes = the vertex positions and triangle count of the BB armor prefab's skinned meshes; a clip = every
    key of BB's AnimationClip; a prop = every mesh against the BB prefab's mesh of the same node, and an animated
    prop's clips against BB's. A file that differs, or cannot be compared (a skinned prop the extractor baked into a
    pose), is dropped with whatever needs it.
Every picture is taken again from the BB rip: outfit colour and edition textures (armors/materials), BB's faces 0-22
(armors/overlay), item icons, class portraits, emote and skill icons (gamegui/icons), prop textures (Assets/Texture2D);
a picture with no BB file is dropped with whatever needs it (a prop: the prop; an icon: the tile shows no picture).
TTO's own faces: the first half per class by face number, rounded down (plan ruling R8). rig.json (BB's skeleton,
built from the BB rip by extract.py) is copied as built; placements.json (TTO's own mount table, Config/*Placement)
keeps only the entries of published items' codes.

The page is rewritten by exact string replacement (a missing anchor = the page changed: PublishError): DATA points at
data-<first 10 hex of SHA-256 over the published data>/, the fetches drop cache: "no-cache" (a changed file gets a new
folder, so _headers can make the data immutable), the "copy for Claude" button and its handler give way to a link to
the Bible, ../fonts/ and ../props/tex/ point inside the copy, and GoatCounter counts the page as /wardrobe/.
check() then applies Cloudflare Pages' limits (20,000 files a deploy, 25 MiB a file) and compares every path the page
builds from the JSON with the stored names case-sensitively (a Windows test server hides a case slip, Cloudflare 404s).
"""
import argparse
import hashlib
import json
import math
import os
import re
import shutil
import struct
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
BB_RIP = Path(r"D:\12tails\RippedAssets\ExportedProject\Assets\Resources")
BIBLE_URL = "https://jumpptty.github.io/12tails/12t_projects/bible/"
MAX_FILES = 20_000                       # Cloudflare Pages, free plan: files a deploy
MAX_FILE_BYTES = 25 * 1024 * 1024        # and bytes a file
PROP_KINDS = {"weapons": "weapons", "accessories": "headpieces", "trinkets": "back_trinkets"}   # data file -> report kind
SHARED_KINDS = ("accessories", "trinkets")        # the page loads all/props_<kind>.json for these
ROOT_JSON = ("meta.json", "icons.json", "placements.json", "item_map.json", "ui.json")
ITEM_ICON_FOLDERS = {"weapon", "armor", "accessory", "acessory", "trinket"}    # icons/<folder> = gamegui/icons/items/<folder>
GOATCOUNTER = ('<script data-goatcounter="https://jumpptty.goatcounter.com/count"\n'
               '        data-goatcounter-settings=\'{"path": "/wardrobe/"}\'\n'
               '        async src="https://gc.zgo.at/count.js"></script>\n')
PROVENANCE = ("wardrobe_data.py and extract_tto_props.py extracted every outfit mesh, clip and prop of this copy through "
              "TTO's client bundles (tto_assets/2026-11-04), BB's own items included. wardrobe_publish.py kept a BB item "
              "(tto flag false) only where each of its 3D files was verified equal to BB's client data in the BB rip: "
              "outfit meshes by vertex positions and triangle count, clips by every key, props by every mesh's vertex "
              "positions and triangle count and an animated prop's clip keys. Every picture was taken again from the BB "
              "rip. rig.json (BB's skeleton, built from the BB rip by extract.py) is copied as built. placements.json is "
              "TTO's own mount table (Config/*Placement), kept for the published items' codes only. From TTO itself the "
              "copy holds only the first half of TTO's own faces per class.")


class PublishError(Exception):
    """The source cannot be published as it is: a page anchor is missing (the page changed), a font is missing."""


class BBDataError(Exception):
    """A BB rip file could not be read the way this script expects."""


# ---------------------------------------------------------------- the page
def page_edits(data_dir):
    """(what, old, new, count): the exact replacements; count 1 = exactly once, 0 = at least once."""
    return [
        ("data folder", 'const DATA = "data/";', f'const DATA = "{data_dir}/";', 1),
        ("no-cache comment",
         "// no-cache = ask the server every time (a 304 when unchanged): a rebuilt outfits.json (the R / V editions, 2026-11-05)\n"
         "// was otherwise served stale from the browser's cache\n",
         "// the published copy (wardrobe_publish.py) keeps its data in a folder named by a hash of the content: a rebuilt\n"
         "// file gets a new address, so the browser may keep every file it has\n", 1),
        ("no-cache fetch", 'fetch(p, { cache: "no-cache" })', "fetch(p)", 1),
        ("copy button", '<button type="button" class="primary" id="copy">คัดลอกให้ Claude</button>',
         f'<a class="primary" id="bible" href="{BIBLE_URL}">12 Tails Bible</a>', 1),
        ("fonts", 'url("../fonts/', 'url("fonts/', 0),
        ("prop textures", "texLoader.load(`../props/tex/${m.tex}`)", "texLoader.load(`${DATA}props/tex/${m.tex}`)", 1),
        ("bar style", "</style>", ".bar a { border-radius: 9px; padding: 7px 12px; text-decoration: none; }\n</style>", 1),
        ("analytics", "</head>", GOATCOUNTER + "</head>", 1),
    ]


def rewrite_page(html, data_dir):
    """The hosted page. Raises PublishError when an anchor is missing or the result still has a local-only part."""
    nl = "\r\n" if "\r\n" in html else "\n"
    for what, old, new, count in page_edits(data_dir):
        old, new = old.replace("\n", nl), new.replace("\n", nl)
        n = html.count(old)
        if n == 0 or (count == 1 and n != 1):
            raise PublishError(f"index.html: the {what} anchor {old!r} is {'missing' if n == 0 else f'there {n} times'}; "
                               f"the page has changed, update wardrobe_publish.py")
        html = html.replace(old, new)
    start, end = '$("copy").onclick = async () => {' + nl, nl + "};" + nl
    i = html.find(start)
    j = html.find(end, i) if i >= 0 else -1
    if html.count(start) != 1 or j < 0:
        raise PublishError(f"index.html: the copy handler anchor {start.strip()!r} ... '}};' is missing or repeated; "
                           f"the page has changed, update wardrobe_publish.py")
    html = html[:i] + html[j + len(end):]
    for left in ("no-cache", "คัดลอกให้ Claude", '$("copy")', "../"):
        if left in html:
            raise PublishError(f"index.html: {left!r} is still in the published page; update wardrobe_publish.py")
    return html


def page_fonts(html):
    return re.findall(r'url\("fonts/([^"/]+)"\)', html)


# ---------------------------------------------------------------- the BB rip (AssetRipper YAML, read as text)
_DOC = re.compile(r"^--- !u!(\d+) &(-?\d+)(?: stripped)?\n", re.M)
_GUID = re.compile(r"^guid: ([0-9a-f]{32})", re.M)
_STREAM = re.compile(r"^    m_Streams\[\d\]:\n      channelMask: (\d+)\n      offset: (\d+)\n      stride: (\d+)\n", re.M)
_SUBMESH = re.compile(r"^  - firstByte: (\d+)\n    indexCount: (\d+)\n    isTriStrip: (\d+)\n", re.M)
_VEC = re.compile(r"([xyzw]): ([^,}]+)")
CURVE_SLOTS = {"m_RotationCurves": ("q", "xyzw"), "m_PositionCurves": ("p", "xyz"), "m_ScaleCurves": ("s", "xyz")}


def _f32(text):
    """A YAML number as the float32 the game stored (YAML writes float32s in shortest form)."""
    x = float(text)
    return x if math.isinf(x) else struct.unpack("<f", struct.pack("<f", x))[0]


def _unquote(s):
    s = s.strip()
    return s[1:-1] if len(s) >= 2 and s[0] == s[-1] and s[0] in "'\"" else s


def read_mesh_shape(path):
    """(vertex positions in Unity space, triangle count) of an uncompressed Unity 4 YAML mesh (unity_yaml.read_mesh's
    rules: interleaved streams, 16-bit indices, strips without their degenerate triangles)."""
    text = Path(path).read_text(encoding="utf-8")
    if not re.search(r"^  m_MeshCompression: 0$", text, re.M):
        raise BBDataError(f"{Path(path).name}: a compressed mesh")
    nv = re.search(r"^    m_VertexCount: (\d+)$", text, re.M)
    vdata = re.search(r"^    _typelessdata: ([0-9a-fA-F]*)$", text, re.M)
    ibuf = re.search(r"^  m_IndexBuffer: ?([0-9a-fA-F]*)$", text, re.M)
    if not (nv and vdata and ibuf):
        raise BBDataError(f"{Path(path).name}: no vertex count, vertex data or index buffer")
    nv, raw = int(nv.group(1)), bytes.fromhex(vdata.group(1))
    stream = next(((int(o), int(s)) for m, o, s in _STREAM.findall(text) if int(m) & 1), None)
    if stream is None:
        raise BBDataError(f"{Path(path).name}: no stream holds the positions")
    offset, stride = stream
    if offset + (nv - 1) * stride + 12 > len(raw):
        raise BBDataError(f"{Path(path).name}: vertex data shorter than {nv} vertices")
    positions = [struct.unpack_from("<3f", raw, offset + i * stride) for i in range(nv)]
    hexidx = ibuf.group(1)
    idx = struct.unpack(f"<{len(hexidx) // 4}H", bytes.fromhex(hexidx)) if hexidx else ()
    tris = 0
    for first, count, strip in _SUBMESH.findall(text):
        seq = idx[int(first) // 2: int(first) // 2 + int(count)]
        if int(strip):
            tris += sum(1 for i in range(len(seq) - 2) if len({seq[i], seq[i + 1], seq[i + 2]}) == 3)
        else:
            tris += len(seq) // 3
    return positions, tris


def read_clip(path):
    """(m_Name, [(curve field, path, keys)]) of a legacy YAML AnimationClip; a key = {time, value, inSlope, outSlope}
    with float32 numbers."""
    name, curves, field, keys, key = None, [], None, None, None
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("  m_Name: ") and name is None:
            name = _unquote(line[len("  m_Name: "):])
            continue
        head = re.match(r"^  (m_\w+):", line)
        if head:
            field = head.group(1) if head.group(1) in CURVE_SLOTS else None
            continue
        if field is None:
            continue
        if line == "  - curve:":
            keys = []
        elif (m := re.match(r"^      - time: (\S+)$", line)) and keys is not None:
            key = {"time": _f32(m.group(1))}
            keys.append(key)
        elif (m := re.match(r"^        (value|inSlope|outSlope): \{(.*)\}$", line)) and key is not None:
            key[m.group(1)] = {c: _f32(v) for c, v in _VEC.findall(m.group(2))}
        elif (m := re.match(r"^    path: ?(.*)$", line)) and keys is not None:
            curves.append((field, _unquote(m.group(1)), keys))
            keys, key = None, None
    if name is None:
        raise BBDataError(f"{Path(path).name}: no m_Name")
    return name, curves


def read_prefab(path):
    """{filters: {GameObject name: [mesh guid]}, skins: {name: [mesh guid]}, clips: [clip guid], anim_node: name} of a
    YAML prefab (MeshFilter, SkinnedMeshRenderer and Animation components)."""
    parts = _DOC.split(Path(path).read_text(encoding="utf-8"))
    docs = list(zip(parts[1::3], parts[2::3], parts[3::3]))
    names = {fid: _unquote(m.group(1)) for cls, fid, body in docs if cls == "1"
             and (m := re.search(r"^  m_Name: (.*)$", body, re.M))}
    out = {"filters": {}, "skins": {}, "clips": [], "anim_node": None}
    for cls, _, body in docs:
        if cls not in ("33", "137", "111"):
            continue
        go = re.search(r"^  m_GameObject: \{fileID: (-?\d+)\}", body, re.M)
        name = names.get(go.group(1)) if go else None
        if cls in ("33", "137"):
            mesh = re.search(r"^  m_Mesh: \{fileID: -?\d+, guid: ([0-9a-f]{32})", body, re.M)
            if mesh and name is not None:
                out["filters" if cls == "33" else "skins"].setdefault(name, []).append(mesh.group(1))
        else:
            block = re.search(r"^  m_Animations:\n((?:  - .*\n)*)", body, re.M)
            out["clips"] += re.findall(r"guid: ([0-9a-f]{32})", block.group(1)) if block else []
            out["anim_node"] = name
    return out


def prop_position(p):
    """A BB vertex as wardrobe_data.py prop_mesh stores it: three.js space (x mirrored), 5 places."""
    return (round(-p[0], 5), round(p[1], 5), round(p[2], 5))


def hero_rows(keys, slot):
    """BB keys -> wardrobe_data.py clip_dict's rows: three.js space (mirrored), 5 places, an infinite slope = +-1e30."""
    comps = "xyzw" if slot == "q" else "xyz"
    sign = {"q": (1, -1, -1, 1), "p": (-1, 1, 1), "s": (1, 1, 1)}[slot]
    r5 = lambda x: (1e30 if x > 0 else -1e30) if math.isinf(x) else round(x, 5)
    return [[round(k["time"], 5)] + [r5(k[part][c] * s) for part in ("value", "inSlope", "outSlope") for c, s in zip(comps, sign)]
            for k in keys]


def prop_rows(keys, slot):
    """BB keys -> extract_tto_props.py clip_keys (6 places) mirrored by wardrobe_data.py mirror_rows."""
    comps = "xyzw" if slot == "q" else "xyz"
    neg = {"q": (2, 3, 6, 7, 10, 11), "p": (1, 4, 7)}.get(slot, ())
    num = lambda x: (1e30 if x > 0 else -1e30) if math.isinf(x) else round(x, 6)
    rows = [[num(k["time"])] + [num(k[part][c]) for part in ("value", "inSlope", "outSlope") for c in comps] for k in keys]
    return [[-x if i in neg else x for i, x in enumerate(r)] for r in rows]


class BBRip:
    """The BB client rip: case-insensitive lookups (AssetRipper keeps BB's casing: heroes/Bat1.png), a GUID index,
    and the comparisons of the wardrobe's 3D files with BB's."""

    def __init__(self, resources):
        self.res = Path(resources)
        self.assets = self.res.parent
        self.heroes = self.res / "gameassets" / "characters" / "heroes"
        self.icons = self.res / "gamegui" / "icons"
        self.texture2d = self.assets / "Texture2D"
        if not self.heroes.is_dir():
            raise PublishError(f"no BB rip at {self.res} (no gameassets/characters/heroes)")
        self._listings, self._guids, self._clips, self._meshes = {}, None, {}, {}

    def find(self, folder, name):
        """folder/<name> matched without case; None when absent or when several names differ only in case."""
        folder = Path(folder)
        if folder not in self._listings:
            listing = {}
            for f in (os.listdir(folder) if folder.is_dir() else []):
                listing.setdefault(f.lower(), []).append(f)
            self._listings[folder] = listing
        hits = self._listings[folder].get(name.lower(), [])
        return folder / hits[0] if len(hits) == 1 else None

    def find_rel(self, base, rel):
        cur = Path(base)
        for part in rel.split("/"):
            cur = self.find(cur, part)
            if cur is None:
                return None
        return cur

    def guid_path(self, guid):
        if self._guids is None:
            self._guids = {}
            for base in (self.assets / "Mesh", self.assets / "AnimationClip", self.heroes):
                for root, _, files in os.walk(base):
                    for f in files:
                        if f.endswith(".meta"):
                            with open(os.path.join(root, f), encoding="utf-8", errors="replace") as fh:
                                m = _GUID.search(fh.read(400))
                            if m:
                                self._guids[m.group(1)] = Path(root) / f[:-5]
        return self._guids.get(guid)

    def mesh_shape(self, guid):
        path = self.guid_path(guid)
        if path is None:
            raise BBDataError(f"mesh guid {guid} is not in the BB rip's Mesh/ or heroes/")
        if path not in self._meshes:
            self._meshes[path] = read_mesh_shape(path)
        return path, self._meshes[path]

    def same_mesh(self, guids, positions, tris, what, as_stored=lambda p: p):
        """None when one of BB's meshes (guids) has these sorted positions and this triangle count, else why.
        as_stored turns a BB position (Unity space, float32) into the wardrobe file's form."""
        if not guids:
            return f"{what}: BB's prefab has no mesh on a node of that name, so it cannot be compared"
        tried = []
        for g in guids:
            try:
                path, (bb_pos, bb_tris) = self.mesh_shape(g)
            except BBDataError as e:
                tried.append(str(e))
                continue
            if bb_tris == tris and sorted(map(as_stored, bb_pos)) == positions:
                return None
            tried.append(f"BB's {path.name} has {len(bb_pos)} vertices / {bb_tris} triangles, the wardrobe's "
                         f"{len(positions)} / {tris}" + ("" if len(bb_pos) != len(positions) or bb_tris != tris
                                                         else " with other vertex positions"))
        return f"{what}: mesh differs from BB's ({'; '.join(tried)})"

    def compare_outfit(self, cls, outfit, bin_path):
        """None when every mesh of the outfit's o_<name>.bin equals BB's armor prefab's, else the reason."""
        prefab = self.find(self.heroes / cls / "armors", f"{cls}_{outfit['name']}.prefab")
        if prefab is None:
            return f"no BB prefab heroes/{cls}/armors/{cls.capitalize()}_{outfit['name']}.prefab, so it cannot be compared"
        skins = read_prefab(prefab)["skins"]
        buf = Path(bin_path).read_bytes()
        for d in outfit["meshes"]:
            flat = struct.unpack_from(f"<{d['verts'] * 3}f", buf, d["pos"])
            mine = sorted((-flat[i], flat[i + 1], flat[i + 2]) for i in range(0, len(flat), 3))   # back to Unity space
            why = self.same_mesh(skins.get(d["name"], []), mine, d["tris"], f"mesh {d['name']}")
            if why:
                return why
        return None

    def class_clips(self, cls):
        """{clip m_Name: [.anim path]} of the class's BB animation prefabs (heroes/<cls>/animations/*.prefab)."""
        if cls not in self._clips:
            out, folder = {}, self.heroes / cls / "animations"
            for f in sorted(os.listdir(folder)) if folder.is_dir() else []:
                if f.endswith(".prefab"):
                    for g in read_prefab(folder / f)["clips"]:
                        path = self.guid_path(g)
                        if path is not None:
                            out.setdefault(read_clip_name(path), []).append(path)
            self._clips[cls] = out
        return self._clips[cls]

    def compare_hero_clip(self, cls, name, tracks):
        """None when BB has a clip of this name for the class whose keys give exactly these tracks, else the reason."""
        paths = self.class_clips(cls).get(name, [])
        if not paths:
            return f"no BB clip named {name} in heroes/{cls}/animations, so it cannot be compared"
        for path in paths:
            bb = {}
            for field, curve_path, keys in read_clip(path)[1]:
                if keys:
                    slot = CURVE_SLOTS[field][0]
                    bb.setdefault(curve_path.rsplit("/", 1)[-1], {})[slot] = hero_rows(keys, slot)
            if bb == tracks:
                return None
        return f"keys differ from BB's {', '.join(p.name for p in paths)}"

    def prop_prefab(self, cls, kind, name):
        if cls != "all":
            return self.find(self.heroes / cls / kind, name + ".prefab")
        for root, _, files in os.walk(self.heroes / "all"):            # shared items: anywhere under heroes/all
            hits = [f for f in files if f.lower() == name.lower() + ".prefab"]
            if hits:
                return Path(root) / hits[0]
        return None

    def compare_prop(self, cls, kind, prop):
        """None when every mesh (and an animated prop's every clip track) equals the BB prefab's, else the reason."""
        prefab = self.prop_prefab(cls, kind, prop["name"])
        if prefab is None:
            return f"no BB prefab heroes/{cls}/{kind}/{prop['name']}.prefab, so it cannot be compared"
        pf = read_prefab(prefab)
        nodes = prop["nodes"]
        for n in nodes:
            for key in ("mesh", "skin"):
                if key not in n:
                    continue
                if n["name"].startswith("baked_"):
                    return (f"node {n['name']}: extract_tto_props.py baked this skinned mesh into the prefab's pose, so it "
                            f"cannot be compared with BB's raw mesh")
                m = n[key]
                mine = sorted(zip(*[iter(m["pos"])] * 3))
                guids = pf["skins"].get(n["name"], []) + ([] if key == "skin" else pf["filters"].get(n["name"], []))
                why = self.same_mesh(guids, mine, len(m["idx"]) // 3, f"node {n['name']}", prop_position)
                if why:
                    return why
        anim = prop.get("anim")
        if anim:
            bb_clips = {}
            for g in pf["clips"]:
                path = self.guid_path(g)
                if path is not None:
                    clip_name, curves = read_clip(path)
                    bb_clips.setdefault(clip_name, []).append(curves)
            for cname, c in anim["clips"].items():
                if not any(self._prop_clip_equal(nodes, c["tracks"], curves, pf["anim_node"]) for curves in bb_clips.get(cname, [])):
                    return (f"clip {cname}: " + ("keys differ from BB's" if cname in bb_clips
                                                 else "not among the BB prefab's clips, so it cannot be compared"))
        return None

    @staticmethod
    def _prop_clip_equal(nodes, tracks, curves, anim_node):
        """Every wardrobe track (keyed by node index) equals a BB curve on a node of the same name and slot."""
        bb = {}
        for field, path, keys in curves:
            if keys:
                slot = CURVE_SLOTS[field][0]
                target = path.rsplit("/", 1)[-1] if path else anim_node
                bb.setdefault((target, slot), []).append(prop_rows(keys, slot))
        return all(rows in bb.get((nodes[int(idx)]["name"], slot), [])
                   for idx, tr in tracks.items() for slot, rows in tr.items())


def read_clip_name(path):
    with open(path, encoding="utf-8") as fh:
        m = re.search(r"^  m_Name: (.*)$", fh.read(4096), re.M)
    if not m:
        raise BBDataError(f"{Path(path).name}: no m_Name")
    return _unquote(m.group(1))


# ---------------------------------------------------------------- one publish run
class Run:
    """The filtered data being written to the staging folder, with the drop list and warnings."""

    def __init__(self, data, stage, bb):
        self.data, self.stage, self.bb = Path(data), Path(stage), bb
        self.dropped, self.warnings = {}, []
        self._pictures, self._prop_tex = {}, {}

    def drop(self, kind, name, reason):
        self.dropped.setdefault(kind, []).append({"name": name, "reason": reason})

    def load(self, rel, default=None):
        p = self.data / rel
        if not p.exists():
            if default is None:
                raise PublishError(f"the wardrobe data has no {rel}")
            return default
        return json.loads(p.read_text(encoding="utf-8"))

    def write_json(self, rel, obj):
        p = self.stage / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(obj, separators=(",", ":")), encoding="utf-8")

    def copy(self, rel):
        p = self.stage / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(self.data / rel, p)

    def picture(self, rel, bb_file, how):
        """Write stage/rel from BB's file: "texture" = lossy WebP q90 (wardrobe_data.py), "face" = the 256 px face
        block, lossless, "icon" = lossless WebP. Returns None, or why the BB file could not be used."""
        if rel in self._pictures:
            return self._pictures[rel]
        dst = self.stage / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            with Image.open(bb_file) as im:
                if how == "texture":
                    im.convert("RGBA").save(dst, "WEBP", quality=90, method=4)
                elif how == "face":
                    im.convert("RGBA").crop((0, 0, 256, 256)).save(dst, "WEBP", lossless=True)
                else:
                    im.save(dst, "WEBP", lossless=True)
            why = None
        except OSError as e:                              # the rip has a few broken PNGs (Monkey_spider4R.png)
            dst.unlink(missing_ok=True)
            why = f"BB's {Path(bb_file).name} cannot be read ({e})"
        self._pictures[rel] = why
        return why

    def icon(self, rel, kind="icons"):
        """An icons/<sub>.webp picture taken again from BB's gamegui/icons/<sub>.png (item icons sit under items/);
        returns rel, or None when BB has no usable file (then it is listed under kind)."""
        if not rel:
            return None
        if rel in self._pictures:
            return None if self._pictures[rel] else rel
        parts = rel.split("/")
        if parts[0] != "icons" or len(parts) < 3 or not rel.endswith(".webp"):
            why = "not an icons/<folder>/<name>.webp path, so it has no BB counterpart"
        else:
            sub = "/".join((["items"] if parts[1] in ITEM_ICON_FOLDERS else []) + parts[1:])[:-len(".webp")] + ".png"
            bb_file = self.bb.find_rel(self.bb.icons, sub)
            why = self.picture(rel, bb_file, "icon") if bb_file else f"no BB file gamegui/icons/{sub}"
        if why:
            self._pictures[rel] = why
            self.drop(kind, rel, why)
            return None
        return rel

    def prop_texture(self, tex):
        """None when props/tex/<tex> is written from BB's Assets/Texture2D, else why not."""
        if tex not in self._prop_tex:
            bb_file = self.bb.find(self.bb.texture2d, tex)
            if bb_file is None:
                self._prop_tex[tex] = f"texture {tex} has no BB file in Assets/Texture2D"
            else:
                try:
                    with Image.open(bb_file) as im:          # a broken BB PNG would leave the prop untextured
                        im.load()
                except OSError as e:
                    self._prop_tex[tex] = f"BB's texture {bb_file.name} cannot be read ({e})"
                else:
                    dst = self.stage / "props" / "tex" / tex
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(bb_file, dst)
                    self._prop_tex[tex] = None
        return self._prop_tex[tex]


def publish_outfits(run, cls):
    """outfits.json: BB outfits whose meshes equal BB's, with the colours and editions BB has a texture for."""
    cap, kept = cls.capitalize(), []
    materials = run.bb.heroes / cls / "armors" / "materials"

    def texture(stem):                    # <cls>/tex/<stem>.webp from BB's armors/materials/<Cls>_<stem>.png
        bb_file = run.bb.find(materials, f"{cap}_{stem}.png")
        return run.picture(f"{cls}/tex/{stem}.webp", bb_file, "texture") if bb_file \
            else f"no BB texture armors/materials/{cap}_{stem}.png"
    for o in run.load(f"{cls}/outfits.json"):
        name = f"{cls}/{o['name']}"
        if o.get("tto"):
            run.drop("outfits", name, "TTO's own outfit (tto flag)")
            continue
        why = run.bb.compare_outfit(cls, o, run.data / cls / f"o_{o['name']}.bin")
        if why:
            run.drop("outfits", name, why)
            continue
        colours, editions = [], {}
        for c in o["colors"]:
            why = texture(f"{o['name']}{c}")
            if why:
                run.drop("colours", f"{name} colour {c}", why)
            else:
                colours.append(c)
        for e, cs in (o.get("editions") or {}).items():
            for c in cs:
                why = texture(f"{o['name']}{c}{e}") if c in colours else f"its base colour {c} was dropped"
                if why:
                    run.drop("colours", f"{name} colour {c}{e}", why)
                else:
                    editions.setdefault(e, []).append(c)
        if o["colors"] and not colours:
            run.drop("outfits", name, "none of its colour textures has a usable BB file")
            continue
        if not o["colors"]:
            run.warnings.append(f"{name}: no colour textures in the data (colors: []), so the page cannot dress it; "
                                f"a wardrobe_data.py bug, published as it is")
        run.copy(f"{cls}/o_{o['name']}.bin")
        out = {k: v for k, v in o.items() if k != "editions"} | {"colors": colours}
        kept.append(out | ({"editions": editions} if editions else {}))
    run.write_json(f"{cls}/outfits.json", kept)
    return kept


def publish_faces(run, cls, faces):
    """BB's faces from the BB rip plus the first half of TTO's own (by number, rounded down)."""
    own = sorted(f["n"] for f in faces if f.get("tto"))
    keep_tto = set(own[:len(own) // 2])
    overlay, kept = run.bb.heroes / cls / "armors" / "overlay", []
    for f in faces:
        rel, name = f"{cls}/faces/{f['n']}.webp", f"{cls}/{f['n']}"
        if f.get("tto"):
            if f["n"] in keep_tto:
                run.copy(rel)
                kept.append(f)
            else:
                run.drop("faces", name, "TTO's own face beyond the first half of them (the user allows 50 %)")
            continue
        bb_file = run.bb.find(overlay, f"{cls}{f['n']}.png")
        why = run.picture(rel, bb_file, "face") if bb_file else f"no BB overlay armors/overlay/{cls.capitalize()}{f['n']}.png"
        if why:
            run.drop("faces", name, why)
        else:
            kept.append(f)
    return kept, sorted(keep_tto)


def publish_clips(run, cls):
    """clips.json: BB clips whose keys equal BB's AnimationClip."""
    kept = {}
    for name, c in run.load(f"{cls}/clips.json").items():
        kind = "emotes" if c.get("group") == "emote" else "moves"
        if c.get("tto"):
            run.drop(kind, f"{cls}/{name}", "TTO's own clip (tto flag)")
            continue
        why = run.bb.compare_hero_clip(cls, name, c["tracks"])
        if why:
            run.drop(kind, f"{cls}/{name}", why)
        else:
            kept[name] = c
    run.write_json(f"{cls}/clips.json", kept)
    return kept


def publish_props(run, cls, kind):
    """props_<kind>.json: BB props whose geometry (and clips) equal BB's and whose textures BB has."""
    report_kind, kept = PROP_KINDS[kind], []
    for p in run.load(f"{cls}/props_{kind}.json", default=[]):
        name = f"{cls}/{p['name']}"
        if p.get("tto"):
            run.drop(report_kind, name, "TTO's own item (tto flag)")
            continue
        why = run.bb.compare_prop(cls, kind, p)
        if not why:
            textures = sorted({m["tex"] for n in p["nodes"] for m in n.get("mats", []) if m.get("tex")})
            why = next((w for w in map(run.prop_texture, textures) if w), None)
        if why:
            run.drop(report_kind, name, why)
        else:
            kept.append(p)
    run.write_json(f"{cls}/props_{kind}.json", kept)
    return kept


def strip_hand(name):
    return re.sub(r"_[LRlr]$", "", name)


def publish_icons(run, outfits, props):
    """icons.json for the published items only (the page looks a prop up by name, name without _L / _R, then the shared
    table by lower-case name); every picture from the BB rip, a missing one becomes "no icon" (the codes stay: they
    pick TTO's placement entry)."""
    names = {cls: {"outfits": {o["name"] for o in os_}} for cls, os_ in outfits.items()}
    shared = {}
    for (cls, kind), ps in props.items():
        mine = {p["name"] for p in ps} | {strip_hand(p["name"]) for p in ps}
        names.setdefault(cls, {}).setdefault(kind, set()).update(mine)
        shared.setdefault(kind, set()).update(p["name"].lower() for p in ps)
    out = {}
    for cls, slots in run.load("icons.json").items():
        out[cls] = {}
        for slot, entries in slots.items():
            keep = shared.get(slot, set()) if cls == "all" else names.get(cls, {}).get(slot, set())
            out[cls][slot] = {}
            for name, e in entries.items():
                if name not in keep:
                    continue
                e = dict(e, icon=run.icon(e.get("icon")))
                if e.get("editions"):
                    e["editions"] = {k: v for k, v in ((k, run.icon(v)) for k, v in e["editions"].items()) if v}
                out[cls][slot][name] = e
    run.write_json("icons.json", out)
    return out


def published_models(cls, kind, outfits, props):
    """The item_map.json model names of one class and kind that are published, in the map's own spelling: armor
    models are <Class>_<outfit>, Panda's gloves map to <name> for props <name>_L / _R, shared ("all") models are lower
    case and match a published prop of any class."""
    if kind == "armor":                  # wardrobe_icons.py: <cls>_ (any case) is stripped to give the outfit name
        return {n.lower() for o in outfits.get(cls, []) for n in (f"{cls}_{o['name']}", o["name"])}
    slot = {"weapon": "weapons", "accessory": "accessories", "trinket": "trinkets"}.get(kind)
    names = {n for (c, k), ps in props.items() if k == slot and (c == cls or cls == "all")
             for p in ps for n in (p["name"], strip_hand(p["name"]))}
    return {n.lower() for n in names} if cls == "all" else names


def publish_item_map(run, outfits, props):
    """item_map.json without the models that are not published (TTO's items, dropped ones); codes left with no model
    go too."""
    out = {}
    for cls, kinds in run.load("item_map.json").items():
        out[cls] = {}
        for kind, codes in kinds.items():
            pub = published_models(cls, kind, outfits, props)
            key = (lambda m: m.lower()) if kind == "armor" or cls == "all" else (lambda m: m)
            kept = {code: [m for m in models if key(m) in pub] for code, models in codes.items()}
            out[cls][kind] = {code: ms for code, ms in kept.items() if ms}
    run.write_json("item_map.json", out)


def publish_placements(run, icons):
    """placements.json with only the entries of codes a published item carries (the page finds them through
    icons.json codes); each hero's fallback stays."""
    out = {}
    for table, heroes in run.load("placements.json").items():
        out[table] = {}
        for hero, t in heroes.items():
            cls = hero.split("#")[0]
            codes = {c for src in (icons.get(cls, {}), icons.get("all", {}))
                     for e in src.get(table, {}).values() for c in e.get("codes", [])}
            out[table][hero] = dict(t, entries={c: v for c, v in (t.get("entries") or {}).items() if c in codes})
    run.write_json("placements.json", out)


def publish_ui(run, classes):
    """ui.json: the class portraits, emotion and skill icons BB has (re-taken from gamegui/icons)."""
    ui = run.load("ui.json")
    out = dict(ui, heroes={}, emotion=[], skills={})
    for cls, rel in ui.get("heroes", {}).items():
        if cls in classes and run.icon(rel, "portraits"):
            out["heroes"][cls] = rel
    out["emotion"] = [n for n in ui.get("emotion", []) if run.icon(f"icons/skills/emotion/{n}.webp")]
    out["skills"] = {cls: [n for n in names if run.icon(f"icons/skills/{cls}/{n}.webp")]
                     for cls, names in ui.get("skills", {}).items() if cls in classes}
    run.write_json("ui.json", out)


def stage_data(data, stage, bb):
    """Write the filtered data to stage/; returns (dropped, tto_faces, warnings)."""
    run = Run(data, stage, bb)
    meta = run.load("meta.json")
    classes = [c["cls"] for c in meta["classes"]]
    outfits, props, tto_faces, meta_out = {}, {}, {}, {"classes": []}
    for c in meta["classes"]:
        cls = c["cls"]
        run.copy(f"{cls}/rig.json")
        outfits[cls] = publish_outfits(run, cls)
        faces, kept_tto = publish_faces(run, cls, c["faces"])
        if any(f.get("tto") for f in c["faces"]):
            tto_faces[cls] = kept_tto
        clips = publish_clips(run, cls)
        for kind in PROP_KINDS:
            props[(cls, kind)] = publish_props(run, cls, kind)
        meta_out["classes"].append(dict(c, outfits=len(outfits[cls]), faces=faces,
                                        clips={k: v for k, v in c["clips"].items() if k in clips}))
    for kind in SHARED_KINDS:
        props[("all", kind)] = publish_props(run, "all", kind)
    icons = publish_icons(run, outfits, props)
    publish_item_map(run, outfits, props)
    publish_placements(run, icons)
    publish_ui(run, classes)
    run.write_json("meta.json", meta_out)
    return run.dropped, tto_faces, run.warnings


def tree_hash(folder):
    """First 10 hex of SHA-256 over the sorted relative paths and bytes of every file under folder."""
    h = hashlib.sha256()
    files = sorted((p.relative_to(folder).as_posix(), p) for p in Path(folder).rglob("*") if p.is_file())
    for rel, p in files:
        b = p.read_bytes()
        h.update(rel.encode("utf-8") + b"\0" + len(b).to_bytes(8, "little"))
        h.update(b)
    return h.hexdigest()[:10]


def headers_text(data_dir):
    # Cloudflare allows one splat a rule, so the rule names this publish's data folder
    return (f"/{data_dir}/*\n  Cache-Control: public, max-age=31536000, immutable\n"
            f"/\n  Cache-Control: no-cache\n")


def remove(path):
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def publish(src, out, bb_rip):
    """Build the public copy of src (wardrobe/: index.html + data/) in out. Returns {files, bytes, data_dir,
    dropped: {kind: [{name, reason}]}, tto_faces: {cls: [kept numbers]}, warnings}."""
    src, out = Path(src), Path(out)
    with open(src / "index.html", encoding="utf-8", newline="") as fh:
        page = fh.read()
    fonts = page_fonts(rewrite_page(page, "data-" + "0" * 10))          # a changed page fails before anything is written
    font_dir = src.parent / "fonts"
    missing = [f for f in fonts if not (font_dir / f).is_file()]
    if missing:
        raise PublishError(f"the page loads fonts {missing}, not in {font_dir}")
    bb = BBRip(bb_rip)
    out.mkdir(parents=True, exist_ok=True)
    stage = out / ".data-staging"
    remove(stage)
    dropped, tto_faces, warnings = stage_data(src / "data", stage, bb)
    data_dir = "data-" + tree_hash(stage)
    for old in list(out.glob("data-*")) + [out / "fonts", out / "index.html", out / "_headers"]:
        remove(old)
    stage.rename(out / data_dir)
    with open(out / "index.html", "w", encoding="utf-8", newline="") as fh:
        fh.write(rewrite_page(page, data_dir))
    (out / "fonts").mkdir()
    for f in fonts:
        shutil.copy2(font_dir / f, out / "fonts" / f)
    (out / "_headers").write_text(headers_text(data_dir), encoding="utf-8", newline="\n")
    files = [p for p in out.rglob("*") if p.is_file()]
    return {"files": len(files), "bytes": sum(p.stat().st_size for p in files), "data_dir": data_dir,
            "dropped": dropped, "tto_faces": tto_faces, "warnings": warnings}


# ---------------------------------------------------------------- check
class CaseSensitive:
    """Path lookups the way Cloudflare serves them: every part of the path must match a stored name exactly."""

    def __init__(self, root):
        self.root, self._names = Path(root), {}

    def names(self, folder):
        if folder not in self._names:
            self._names[folder] = os.listdir(folder) if folder.is_dir() else []
        return self._names[folder]

    def problem(self, rel):
        cur, stored, exact = self.root, [], True
        for part in rel.split("/"):
            names = self.names(cur)
            if part not in names:
                alt = [n for n in names if n.lower() == part.lower()]
                if not alt:
                    return f"missing: {rel}"
                part, exact = alt[0], False
            stored.append(part)
            cur = cur / part
        if not cur.is_file():
            return f"missing: {rel} (not a file)"
        return None if exact else f"case mismatch: the page asks for {rel}, the copy stores {'/'.join(stored)}"


def _json(folder, rel, problems):
    p = folder / rel
    if not p.is_file():
        return None                                     # reported as missing by the path walk
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (ValueError, UnicodeDecodeError) as e:
        problems.append(f"{rel} is not valid JSON ({e})")
        return None


def _prop_textures(props):
    return [f"props/tex/{m['tex']}" for p in props or [] for n in p["nodes"] for m in n.get("mats", []) if m.get("tex")]


def data_references(folder, problems):
    """Every path (relative to the data folder) the page builds from the published JSON."""
    refs = list(ROOT_JSON)
    meta = _json(folder, "meta.json", problems) or {"classes": []}
    for c in meta["classes"]:
        cls = c["cls"]
        refs += [f"{cls}/rig.json", f"{cls}/outfits.json", f"{cls}/clips.json"]
        refs += [f"{cls}/faces/{f['n']}.webp" for f in c.get("faces", [])]
        for o in _json(folder, f"{cls}/outfits.json", problems) or []:
            refs.append(f"{cls}/o_{o['name']}.bin")
            refs += [f"{cls}/tex/{o['name']}{col}.webp" for col in o.get("colors", [])]
            refs += [f"{cls}/tex/{o['name']}{col}{e}.webp" for e, cs in (o.get("editions") or {}).items() for col in cs]
        for kind in PROP_KINDS:
            refs.append(f"{cls}/props_{kind}.json")
            refs += _prop_textures(_json(folder, f"{cls}/props_{kind}.json", problems))
    for kind in SHARED_KINDS:
        refs.append(f"all/props_{kind}.json")
        refs += _prop_textures(_json(folder, f"all/props_{kind}.json", problems))
    for slots in (_json(folder, "icons.json", problems) or {}).values():
        for entries in slots.values():
            for e in entries.values():
                refs += [r for r in [e.get("icon"), *(e.get("editions") or {}).values()] if r]
    ui = _json(folder, "ui.json", problems) or {}
    refs += list(ui.get("heroes", {}).values())
    refs += [f"icons/skills/emotion/{n}.webp" for n in ui.get("emotion", [])]
    refs += [f"icons/skills/{cls}/{n}.webp" for cls, names in ui.get("skills", {}).items() for n in names]
    return refs


def limit_problems(out):
    problems, n = [], 0
    for root, _, files in os.walk(out):
        for f in files:
            n += 1
            size = os.path.getsize(os.path.join(root, f))
            if size > MAX_FILE_BYTES:
                rel = Path(root, f).relative_to(out).as_posix()
                problems.append(f"{rel} is {size / 2 ** 20:.1f} MiB: Cloudflare Pages takes at most 25 MiB a file")
    if n > MAX_FILES:
        problems.append(f"{n:,} files: Cloudflare Pages takes at most 20,000 files a deploy")
    return problems


def check(out):
    """Problems with the published copy in out (empty = fine to deploy)."""
    out = Path(out)
    problems = limit_problems(out)
    page = out / "index.html"
    if not page.is_file():
        return problems + ["index.html is missing"]
    html = page.read_text(encoding="utf-8")
    m = re.search(r'const DATA = "(data-[0-9a-f]{10})/";', html)
    if not m:
        return problems + ['index.html has no hashed data folder (const DATA = "data-<10 hex>/";)']
    data_dir = m.group(1)
    headers = (out / "_headers").read_text(encoding="utf-8") if (out / "_headers").is_file() else ""
    if f"/{data_dir}/*\n" not in headers:
        problems.append(f"_headers has no rule for /{data_dir}/* (the data would not be cached)")
    refs = [f"fonts/{f}" for f in page_fonts(html)]
    refs += [f"{data_dir}/{r}" for r in data_references(out / data_dir, problems)]
    walker = CaseSensitive(out)
    problems += [p for p in (walker.problem(r) for r in dict.fromkeys(refs)) if p]
    return problems


# ---------------------------------------------------------------- command line
def report_path(out):
    return Path(out).parent / f"{Path(out).name}_report.json"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Publish the 12 Tails Wardrobe for Cloudflare Pages (BB items only).")
    ap.add_argument("--src", type=Path, default=ROOT / "wardrobe", help="the wardrobe folder (index.html + data/)")
    ap.add_argument("--out", type=Path, default=ROOT / "wardrobe_dist", help="the output folder")
    ap.add_argument("--bb-rip", type=Path, default=BB_RIP, help="BB's rip: ...\\ExportedProject\\Assets\\Resources")
    ap.add_argument("--check", type=Path, metavar="DIR", help="only check an existing output folder")
    a = ap.parse_args(argv)
    if a.check:
        problems = check(a.check)
        print("\n".join(problems) or "no problems")
        return 1 if problems else 0
    try:
        result = publish(a.src, a.out, a.bb_rip)
    except PublishError as e:
        print(f"publish failed: {e}", file=sys.stderr)
        return 1
    problems = check(a.out)
    report = {"provenance": PROVENANCE, **result, "problems": problems}
    report_path(a.out).write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{a.out}: {result['files']:,} files, {result['bytes'] / 1e6:.1f} MB, data folder {result['data_dir']}")
    for kind, items in sorted(result["dropped"].items()):
        print(f"  dropped {kind}: {len(items)}")
    print("  kept TTO faces: " + ", ".join(f"{cls} {v[0]}-{v[-1]}" if v else f"{cls} none" for cls, v in result["tto_faces"].items()))
    for w in result["warnings"]:
        print(f"  warning: {w}")
    print(f"report: {report_path(a.out)}")
    print("\n".join(f"  problem: {p}" for p in problems) or "check: no problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
