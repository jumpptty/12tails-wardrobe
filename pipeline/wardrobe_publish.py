r"""The public copy of the 12 Tails Wardrobe, for Cloudflare Pages (plan plans/wardrobe_online_plan.md, Task 1).

  py -3 pipeline/wardrobe_publish.py [--src <repo>\wardrobe] [--data <src>\data] [--out <repo>\wardrobe_dist]
                                     [--bb-rip D:\12tails\RippedAssets\ExportedProject\Assets\Resources]
  py -3 pipeline/wardrobe_publish.py --check <dir>
  -> <out>\index.html, its tab icons, <out>\ui-<hash>\, <out>\data-<hash>\, <out>\_headers, and <out>_report.json beside it
     (every dropped item with the reason, the kept TTO faces, warnings, check problems; the previous run's report is
     kept as <out>_report.prev.json and the count changes against it are printed). Exit 1 when check() finds problems.
  --src gives the page and its icons, --data the data (default <src>\data): a git worktree publishes its own page
  with the main checkout's data, with no link to that data inside the worktree (a junction there is emptied by
  `git worktree remove` / `git clean -x`). The previous copy in --out stays whole until the new one is in place.

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
The page's own pictures, ui/recolor1-5.webp (the colour topic), are 2x upscales of BB's Recolor Drug icons cropped to
the potions' square (UI_CROP in BB's 64 px); each is proven against that box of BB's field/rsc<n>.png.
TTO online (user 2026-11-09: "Also add TTO stuff to the public deployement, I've got the green light, BUT 1. Change the
pink dot to TTO small logo instead. 2. TTO shouldn't be downloadable nor uploadable, it's preview only 3. only include
released assets, I will mark them from html picker."): <src>/tto_released.json, written by wardrobe/tto_picker.html,
names per class the TTO-sourced items to publish ({cls: {kind: [names]}}; kinds outfits, weapons, accessories, trinkets,
clips, faces; "all": accessories, trinkets). TTO-sourced = what the BB rule above would drop for being TTO's: its tto flag,
no BB prefab or file to compare with, or a 3D file that differs from BB's (TTO's copy of a BB item). A released one is
published from the local data (there is no BB file to re-take it from), with its own textures and icons, and marked
"tto": true (the page shows the TTO mark and keeps it preview-only: TTO_LOCK). Every candidate, released or not, is
listed in <out>_tto.json for the picker. ToT's own items never go online. With no tto_released.json, TTO's faces follow
the old rule (TTO_FACES_ALL_RELEASED, else the first half per class by face number, plan ruling R8). rig.json (BB's skeleton,
built from the BB rip by extract.py) is copied as built; placements.json (TTO's own mount table, Config/*Placement)
keeps only the entries of published items' codes.

The page is rewritten by exact string replacement (a missing anchor = the page changed: PublishError): DATA points at
data-<first 10 hex of SHA-256 over the published data>/ and UI_DIR at ui-<10 hex over the ui pictures>/, the fetches
drop cache: "no-cache" (a changed file gets a new folder, so _headers makes both folders immutable for a year), the
"copy for Claude" button and its handler go, the Bible's logo in the panel's lockup becomes a link to the Bible (new tab),
and GoatCounter counts the page as /wardrobe/. Prop textures load from ${DATA}props/tex/ locally and online alike (the
local copy is wardrobe_props_tex.py's, since the 2026-11-09 repo split). The page loads its fonts from Google Fonts (the
Bible's own sheet), so no font files are published; a page that still points at ../fonts/ or ../props/ fails.
check() then applies Cloudflare Pages' limits (20,000 files a deploy, 25 MiB a file) and compares every path the page
builds from the JSON, its ui pictures and its tab icon with the stored names case-sensitively (a Windows test server
hides a case slip, Cloudflare 404s). Outfits with no colours (colors: []) are dropped: the page cannot dress them.
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

from PIL import Image, ImageChops, ImageStat

ROOT = Path(__file__).resolve().parent.parent
# either PC's Bible (home D:\12tails, office Desktop\12tails), so the office can publish too (user 2026-11-09)
BB_RIP = next((p for p in (Path(r"D:\12tails\RippedAssets\ExportedProject\Assets\Resources"),
                          Path(r"C:\Users\Jump\Desktop\12tails\RippedAssets\ExportedProject\Assets\Resources")) if p.is_dir()),
              Path(r"D:\12tails\RippedAssets\ExportedProject\Assets\Resources"))
BIBLE_URL = "https://jumpptty.github.io/12tails/12t_projects/bible/"
MAX_FILES = 20_000                       # Cloudflare Pages, free plan: files a deploy
MAX_FILE_BYTES = 25 * 1024 * 1024        # and bytes a file
PROP_KINDS = {"weapons": "weapons", "accessories": "headpieces", "trinkets": "back_trinkets"}   # data file -> report kind
SHARED_KINDS = ("accessories", "trinkets")        # the page loads all/props_<kind>.json for these
ROOT_JSON = ("meta.json", "icons.json", "placements.json", "item_map.json", "ui.json")
PAGE_FILES = ("wardrobe_icon.svg", "wardrobe.ico")   # copied from --src next to the page: its tab icon (and the .ico)
# the effects' own folders, copied from --src next to the page (the page loads fx_cues/<cls>.json and fxparts/<file>.js
# relative to itself): the cue files (one per class, {} = none) and the effect part modules (2026-11-09)
PAGE_DIRS = ("fx_cues", "fxparts")
UI_DIR = "ui"                                          # <src>/ui/recolor<n>.webp: the page's own pictures (the colour topic)
UI_ICON = re.compile(r"recolor([1-5])\.webp")          # = BB's Recolor Drug n, gamegui/icons/items/field/rsc<n>.png
UI_TTO = "tto.webp"                    # the TTO mark on TTO's tiles (user 2026-11-09: "Change the pink dot to TTO small logo")
UI_COUNT = 5                                           # the page shows colours 1-5: all five pictures are needed
UI_CROP = (4, 7, 56, 59)                               # the potions' common square in BB's 64 px icons (task 14b)
UI_MAX_DIFF = 6                                        # mean absolute difference per channel, at BB's size, over black
# what a publish writes beside its data-<hash> and ui-<hash> folders; "fonts" and "ui" are what earlier publishes wrote
# (the self-hosted fonts, the unhashed ui folder): listed so a new publish removes them
OUTPUT_NAMES = ("index.html", "fonts", "_headers", UI_DIR) + PAGE_FILES + PAGE_DIRS
HASHED_PREFIXES = ("data-", "ui-")
ITEM_ICON_FOLDERS = {"weapon", "armor", "accessory", "acessory", "trinket"}    # icons/<folder> = gamegui/icons/items/<folder>
GOATCOUNTER = ('<script data-goatcounter="https://jumpptty.goatcounter.com/count"\n'
               '        data-goatcounter-settings=\'{"path": "/wardrobe/"}\'\n'
               '        async src="https://gc.zgo.at/count.js"></script>\n')
PROVENANCE = ("wardrobe_data.py and extract_tto_props.py extracted every outfit mesh, clip and prop of this copy through "
              "TTO's client bundles (tto_assets/2026-11-04), BB's own items included. wardrobe_publish.py kept a BB item "
              "(tto flag false) only where each of its 3D files was verified equal to BB's client data in the BB rip: "
              "outfit meshes by vertex positions and triangle count, clips by every key, props by every mesh's vertex "
              "positions and triangle count and an animated prop's clip keys. Every picture was taken again from the BB "
              "rip, except ui-<hash>/recolor1-5.webp: 2x upscales of BB's field/rsc1-5.png cropped to the potions' square, "
              "proven by a downscale comparison against the same box of the BB rip. rig.json (BB's skeleton, built from the BB rip by extract.py) is copied as built. placements.json is "
              "TTO's own mount table (Config/*Placement), kept for the published items' codes only. From TTO itself the "
              "copy holds only the first half of TTO's own faces per class.")


class PublishError(Exception):
    """The source cannot be published as it is: a page anchor is missing (the page changed), a ui picture is missing."""


class BBDataError(Exception):
    """A BB rip file could not be read the way this script expects."""


# ---------------------------------------------------------------- the page
def page_edits(data_dir, ui_dir):
    """(what, old, new, count): the exact replacements; count 1 = exactly once, 0 = at least once."""
    return [
        ("data folder", 'const DATA = "data/";', f'const DATA = "{data_dir}/";', 1),
        ("ui folder", 'const UI_DIR = "ui/";', f'const UI_DIR = "{ui_dir}/";', 1),
        ("no-cache comment",
         "// no-cache = ask the server every time (a 304 when unchanged): a rebuilt outfits.json (the R / V editions, 2026-11-05)\n"
         "// was otherwise served stale from the browser's cache\n",
         "// the published copy (wardrobe_publish.py) keeps its data in a folder named by a hash of the content: a rebuilt\n"
         "// file gets a new address, so the browser may keep every file it has\n", 1),
        ("no-cache fetch", 'fetch(p, { cache: "no-cache" })', "fetch(p)", 1),
        ("no-cache effects", 'dataBytes(`${DATA}${cls}/fx.json`, { cache: "no-cache" })', "dataBytes(`${DATA}${cls}/fx.json`)", 1),
        # the local copy's toolbar ends with a "copy for Claude" button behind a divider: both go
        ("copy button", '<span class="tb-sep" aria-hidden="true"></span><button type="button" class="tb txt" id="copy">คัดลอกให้ Claude</button>',
         "", 1),
        # the Bible's logo in the panel's lockup (task 14b ruling R66; the logo itself since task 15) becomes the link to
        # the Bible, in a new tab (the page's uploaded skins live in its tab only): only its opening tag changes
        ("Bible link", '<a class="brand" id="bible" aria-label="12 Tails Bible">',
         f'<a class="brand" id="bible" href="{BIBLE_URL}" target="_blank" rel="noopener" aria-label="12 Tails Bible">', 1),
        ("analytics", "</head>", GOATCOUNTER + "</head>", 1),
        # the skill effects and sounds are online since the Wolf was finished (user 2026-11-09: "life the restriction on
        # sfx and vfx on the public deploy, we have finished Wolf"; until then the pilot was hidden: FX_ON false)
        # TTO's items are preview only online (user 2026-11-09): no skin download / upload, no 3D file
        ("TTO preview only", 'const TTO_LOCK = new URLSearchParams(location.search).has("ttolock");', "const TTO_LOCK = true;", 1),
        # the page's scripting hook (wardrobe.debug() hands out the whole scene, a few console lines from a .glb with TTO's
        # pieces) only for automated browsers online: the checks (wardrobe_dist_check.py) run in Playwright, where
        # navigator.webdriver is true; a visitor's browser never gets it (user 2026-11-10: "stop casual copying")
        ("scripting hook", "window.wardrobe = {", "if (navigator.webdriver) window.wardrobe = {", 1),
        # community skins (2026-11-11): the send dialog's Turnstile site key from wardrobe/community_config.json (empty:
        # the send action stays hidden); the local page's ?submitkey= test hook goes
        ("send key", 'const SUBMIT_KEY = new URLSearchParams(location.search).get("submitkey") || "";',
         f'const SUBMIT_KEY = "{submit_key()}";', 1),
    ]


def submit_key(path=None):
    """The Turnstile site key (public by design) the published page's send dialog uses; "" = no send action."""
    p = Path(path) if path else ROOT / "wardrobe" / "community_config.json"
    key = json.loads(p.read_text(encoding="utf-8")).get("turnstile_site_key", "") if p.exists() else ""
    if not re.fullmatch(r"[0-9A-Za-z_-]*", key):
        raise PublishError(f"{p.name}: turnstile_site_key {key!r} is not a site key")
    return key


def rewrite_page(html, data_dir, ui_dir="ui-" + "0" * 10):
    """The hosted page. Raises PublishError when an anchor is missing or the result still has a local-only part (a
    ../ path: the self-hosted fonts or anything else outside the copy)."""
    nl = "\r\n" if "\r\n" in html else "\n"
    for what, old, new, count in page_edits(data_dir, ui_dir):
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
    # the cut ends at the first "};" line: a handler that gains one inside leaves its clipboard code behind
    for left in ("no-cache", "คัดลอกให้ Claude", '$("copy")', "navigator.clipboard", "../"):
        if left in html:
            raise PublishError(f"index.html: {left!r} is still in the published page; update wardrobe_publish.py")
    return html


def page_icons(html):
    """The tab icons the page links (<link rel="icon" href="...">)."""
    return re.findall(r'<link rel="icon" href="([^"]+)"', html)


# ---------------------------------------------------------------- the BB rip (AssetRipper YAML, read as text)
_DOC = re.compile(r"^--- !u!(\d+) &(-?\d+)(?: stripped)?\n", re.M)
_GUID = re.compile(r"^guid: ([0-9a-f]{32})", re.M)
_STREAM = re.compile(r"^    m_Streams\[\d\]:\n      channelMask: (\d+)\n      offset: (\d+)\n      stride: (\d+)\n", re.M)
_SUBMESH = re.compile(r"^  - firstByte: (\d+)\n    indexCount: (\d+)\n    isTriStrip: (\d+)\n", re.M)
# the newer layout (the Reborn rip, a later Unity: VertexData serializedVersion 3): channels instead of streams, and a
# topology per submesh (0 triangles, 1 = Unity's internal triangle strip, BB's isTriStrip)
_CHANNEL = re.compile(r"^    - stream: (\d+)\n      offset: (\d+)\n      format: (\d+)\n      dimension: (\d+)\n", re.M)
_SUBMESH_NEW = re.compile(r"^    firstByte: (\d+)\n    indexCount: (\d+)\n    topology: (\d+)\n", re.M)
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
    comp = re.search(r"^  m_MeshCompression: (\d+)$", text, re.M)
    if comp and comp.group(1) != "0":
        raise BBDataError(f"{Path(path).name}: a compressed mesh")
    nv = re.search(r"^    m_VertexCount: (\d+)$", text, re.M)
    vdata = re.search(r"^    _typelessdata: ([0-9a-fA-F]*)$", text, re.M)
    ibuf = re.search(r"^  m_IndexBuffer: ?([0-9a-fA-F]*)$", text, re.M)
    if not (nv and vdata and ibuf):
        raise BBDataError(f"{Path(path).name}: no vertex count, vertex data or index buffer")
    nv, raw = int(nv.group(1)), bytes.fromhex(vdata.group(1))
    chans = [tuple(map(int, c)) for c in _CHANNEL.findall(text)]
    if chans:                                      # the newer layout: position = channel 0, float32 x 3
        s0, off0, fmt0, dim0 = chans[0]
        if s0 != 0 or fmt0 != 0 or (dim0 & 15) < 3:
            raise BBDataError(f"{Path(path).name}: positions not float32 xyz in stream 0")
        if not any(s for s, _, _, d in chans if d & 15):
            if not nv or len(raw) % nv:
                raise BBDataError(f"{Path(path).name}: vertex data is not a whole number of vertices")
            stream = (off0, len(raw) // nv)        # one stream: its stride = the data / the vertices
        else:
            # several streams (2026-11-10: Reborn's skinned Monkey trinkets keep UVs and bone weights in streams 1-2):
            # each stream is its channels end to end (Unity 2019+ VertexFormat sizes), stream 0 first at byte 0, each
            # next one 16-byte aligned; the sizes must add up to the data exactly, or the layout is not understood
            size = (4, 2, 1, 1, 2, 2, 1, 1, 2, 2, 4, 4)
            strides = {}
            for s, o, f, d in chans:
                if d & 15:
                    if f >= len(size):
                        raise BBDataError(f"{Path(path).name}: unknown vertex format {f}")
                    strides[s] = max(strides.get(s, 0), o + (d & 15) * size[f])
            total = 0
            for s in sorted(strides):
                total = -(-total // 16) * 16 + nv * strides[s]
            if total != len(raw):
                raise BBDataError(f"{Path(path).name}: vertex streams add up to {total} bytes, the data has {len(raw)}")
            stream = (off0, strides[0])
    else:
        stream = next(((int(o), int(s)) for m, o, s in _STREAM.findall(text) if int(m) & 1), None)
    if stream is None:
        raise BBDataError(f"{Path(path).name}: no stream holds the positions")
    offset, stride = stream
    if offset + (nv - 1) * stride + 12 > len(raw):
        raise BBDataError(f"{Path(path).name}: vertex data shorter than {nv} vertices")
    positions = [struct.unpack_from("<3f", raw, offset + i * stride) for i in range(nv)]
    hexidx = ibuf.group(1)
    if re.search(r"^  m_IndexFormat: 1$", text, re.M):
        raise BBDataError(f"{Path(path).name}: 32-bit indices")
    idx = struct.unpack(f"<{len(hexidx) // 4}H", bytes.fromhex(hexidx)) if hexidx else ()
    subs = _SUBMESH.findall(text)
    if not subs:
        subs = []
        for first, count, topo in _SUBMESH_NEW.findall(text):
            if topo not in ("0", "1"):
                raise BBDataError(f"{Path(path).name}: submesh topology {topo}")
            subs.append((first, count, topo))
    tris = 0
    for first, count, strip in subs:
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
        # the newer layout (the Reborn rip, 2026-11-10): each key opens with its serializedVersion, time on the next line
        elif re.match(r"^      - serializedVersion: \d+$", line) and keys is not None:
            key = {}
            keys.append(key)
        elif (m := re.match(r"^        time: (\S+)$", line)) and key is not None:
            key["time"] = _f32(m.group(1))
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

    def __init__(self, resources, fallback=None):
        self.res = Path(resources)
        self.assets = self.res.parent
        self.heroes = self.res / "gameassets" / "characters" / "heroes"
        self.icons = self.res / "gamegui" / "icons"
        self.texture2d = self.assets / "Texture2D"
        if not self.heroes.is_dir():
            raise PublishError(f"no BB rip at {self.res} (no gameassets/characters/heroes)")
        self._listings, self._guids, self._clips, self._meshes = {}, None, {}, {}
        # the Reborn rip (a BB-client build) for a prop whose BB prefab this rip has lost (2026-11-09: the office's rip has
        # 24 zero-filled Monkey trinket prefabs and 2 missing): the prop is compared with Reborn's prefab and meshes
        # instead, so it still has to equal them exactly; a BB prefab that reads fine is never replaced
        self.fallback, self.fallback_used = fallback, []

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

    def bb_hero_tracks(self, cls, name):
        """[(path, tracks)] of BB's clips of this name for the class, the tracks in the wardrobe's form (clips.json)."""
        out = []
        for path in self.class_clips(cls).get(name, []):
            bb = {}
            for field, curve_path, keys in read_clip(path)[1]:
                if keys:
                    slot = CURVE_SLOTS[field][0]
                    bb.setdefault(curve_path.rsplit("/", 1)[-1], {})[slot] = hero_rows(keys, slot)
            out.append((path, bb))
        return out

    def compare_hero_clip(self, cls, name, tracks):
        """None when BB has a clip of this name for the class whose keys give exactly these tracks, else the reason."""
        found = self.bb_hero_tracks(cls, name)
        if not found:
            return f"no BB clip named {name} in heroes/{cls}/animations, so it cannot be compared"
        if any(bb == tracks for _, bb in found):
            return None
        return f"keys differ from BB's {', '.join(p.name for p, _ in found)}"

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
        lost = "missing" if prefab is None else "zero-filled" if zero_filled(prefab) else None
        if lost and self.fallback is not None:
            why = self.fallback.compare_prop(cls, kind, prop)
            if why is None:
                self.fallback_used.append(f"{cls}/{prop['name']}: BB's prefab is {lost} in this rip; equal to Reborn's copy")
                return None
            return f"{why} (compared with Reborn's copy: BB's prefab is {lost} in this rip)"
        if prefab is None:
            return f"no BB prefab heroes/{cls}/{kind}/{prop['name']}.prefab, so it cannot be compared"
        pf = read_prefab(prefab)
        nodes = prop["nodes"]
        for n in nodes:
            for key in ("mesh", "skin"):
                if key not in n:
                    continue
                m = n[key]
                if n["name"].startswith("baked_"):
                    # extract_tto_props.py baked this skinned mesh into the prefab's pose: the positions can't be compared
                    # with BB's raw mesh, but baking keeps the vertex and triangle counts, so it is BB's when BB's prefab
                    # has the skinned mesh of that name with the same counts (user 2026-11-09: the Chinese Lantern is BB
                    # stuff, "remove stuff like Chinese Lantern from the picker")
                    base, nv, nt = n["name"][len("baked_"):], len(m["pos"]) // 3, len(m["idx"]) // 3
                    seen = []
                    for g in pf["skins"].get(base, []):
                        try:
                            path, (bb_pos, bb_tris) = self.mesh_shape(g)
                        except BBDataError as e:
                            seen.append(str(e))
                            continue
                        if len(bb_pos) == nv and bb_tris == nt:
                            break
                        seen.append(f"BB's {path.name} has {len(bb_pos)} vertices / {bb_tris} triangles, the wardrobe's {nv} / {nt}")
                    else:
                        return (f"node {n['name']}: extract_tto_props.py baked this skinned mesh into the prefab's pose, and "
                                f"BB's skinned mesh {base} " + ("; ".join(seen) if seen else "is not in the prefab"))
                    continue
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


def zero_filled(path):
    """A rip file that is all zeros at the start: a damaged copy (the office's rip, 2026-11-09)."""
    with open(path, "rb") as fh:
        head = fh.read(64)
    return len(head) > 0 and not any(head)


# TTO's files online are scrambled (user 2026-11-10: "I just want to stop casual copying"): the mark, then the bytes XOR
# a repeating key, so a saved file or a direct link opens as nothing. The page's dataBytes() undoes it (SCR_MARK /
# SCR_KEY in index.html, the same two values; a test holds them equal). Anyone reading the page can undo it too: the
# user accepts that ("those who can reverse engineer the page can already get the files from the offline game copy")
SCRAMBLE_MARK, SCRAMBLE_KEY = b"TTOx", b"12tails-wardrobe-tto-preview-only"


def scramble(data):
    """SCRAMBLE_MARK + data XOR SCRAMBLE_KEY repeated (one big-integer XOR: fast on a 1 MB texture)."""
    key = (SCRAMBLE_KEY * (len(data) // len(SCRAMBLE_KEY) + 1))[:len(data)]
    return SCRAMBLE_MARK + (int.from_bytes(data, "little") ^ int.from_bytes(key, "little")).to_bytes(len(data), "little")


def reborn_rip(bb_rip):
    """The Reborn rip beside the BB rip in the same Bible folder (<bible>\\RippedAssets_Reborn\\ExportedProject\\Assets\\
    Resources for <bible>\\RippedAssets\\ExportedProject\\Assets\\Resources), or None."""
    p = Path(bb_rip)
    if len(p.parents) < 4 or p.parents[2].name != "RippedAssets":
        return None
    r = p.parents[3] / "RippedAssets_Reborn" / p.parents[1].name / p.parents[0].name / p.name
    return r if (r / "gameassets" / "characters" / "heroes").is_dir() else None


def read_clip_name(path):
    with open(path, encoding="utf-8") as fh:
        m = re.search(r"^  m_Name: (.*)$", fh.read(4096), re.M)
    if not m:
        raise BBDataError(f"{Path(path).name}: no m_Name")
    return _unquote(m.group(1))


# ---------------------------------------------------------------- one publish run
class Run:
    """The filtered data being written to the staging folder, with the drop list and warnings."""

    def __init__(self, data, stage, bb, released=None):
        self.data, self.stage, self.bb = Path(data), Path(stage), bb
        self.dropped, self.warnings = {}, []
        self._pictures, self._prop_tex = {}, {}
        self.released, self.candidates = released, []

    def candidate(self, cls, kind, name, reason, default=False, **extra):
        """A TTO-sourced item, listed for the picker; True when the released list has it (no list: default)."""
        rel = default if self.released is None else str(name) in self.released.get(cls, {}).get(kind, ())
        self.candidates.append({"cls": cls, "kind": kind, "name": name, "reason": reason, "released": rel, **extra})
        return rel

    def local_copy(self, rel, scrambled=False):
        """Copy a released TTO item's file from the local data; False when the data has no such file. scrambled: the
        item's own mesh or picture, written scramble()d (an icon stays plain: tiles show it as it is)."""
        if not (self.data / rel).is_file():
            return False
        self.copy(rel, scrambled)
        return True

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

    def copy(self, rel, scrambled=False):
        p = self.stage / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if scrambled:
            p.write_bytes(scramble((self.data / rel).read_bytes()))
        else:
            shutil.copy2(self.data / rel, p)

    def usable(self, bb_file):
        """bb_file, or BB's own copy of it when the rip's file can't be read: the office PC's rip has 52 zero-filled
        Monkey PNGs (2026-11-09), so pipeline/bb_rip_fix.py exports them from BB's game data (12TailsOnline_Data) into
        data/bb_rip_fix/<path under Assets>; without that copy the picture is dropped as before."""
        try:
            with Image.open(bb_file) as im:
                im.verify()
            return bb_file
        except OSError:
            try:
                fix = self.data / "bb_rip_fix" / Path(bb_file).relative_to(self.bb.assets)
            except ValueError:
                return bb_file
            if fix.exists():
                self.warnings.append(f"{Path(bb_file).name}: the rip's copy can't be read; used BB's game data (bb_rip_fix)")
                return fix
            return bb_file

    def picture(self, rel, bb_file, how):
        """Write stage/rel from BB's file: "texture" = lossy WebP q90 (wardrobe_data.py), "face" = the 256 px face
        block, lossless, "icon" = lossless WebP. Returns None, or why the BB file could not be used."""
        if rel in self._pictures:
            return self._pictures[rel]
        bb_file = self.usable(bb_file)
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

    def icon(self, rel, kind="icons", local_ok=False):
        """An icons/<sub>.webp picture taken again from BB's gamegui/icons/<sub>.png (item icons sit under items/);
        returns rel, or None when BB has no usable file (then it is listed under kind). local_ok (a released TTO item's
        icon): with no BB file, the local data's picture is copied instead."""
        if not rel:
            return None
        if rel in self._pictures and self._pictures[rel] and local_ok and self.local_copy(rel):
            self._pictures[rel] = None
        if rel in self._pictures:
            return None if self._pictures[rel] else rel
        parts = rel.split("/")
        if parts[0] != "icons" or len(parts) < 3 or not rel.endswith(".webp"):
            why = "not an icons/<folder>/<name>.webp path, so it has no BB counterpart"
        else:
            sub = "/".join((["items"] if parts[1] in ITEM_ICON_FOLDERS else []) + parts[1:])[:-len(".webp")] + ".png"
            bb_file = self.bb.find_rel(self.bb.icons, sub)
            why = self.picture(rel, bb_file, "icon") if bb_file else f"no BB file gamegui/icons/{sub}"
        if why and local_ok and self.local_copy(rel):
            why = None
        if why:
            self._pictures[rel] = why
            self.drop(kind, rel, why)
            return None
        return rel

    def prop_texture(self, tex, local_ok=False):
        """None when props/tex/<tex> is written from BB's Assets/Texture2D (local_ok, a released TTO item: else from the
        local data's props/tex), else why not."""
        if self._prop_tex.get(tex) and local_ok and self.local_copy(f"props/tex/{tex}", scrambled=True):
            self._prop_tex[tex] = None
        if tex not in self._prop_tex:
            bb_file = self.bb.find(self.bb.texture2d, tex)
            if bb_file is None:
                self._prop_tex[tex] = f"texture {tex} has no BB file in Assets/Texture2D"
            else:
                bb_file = self.usable(bb_file)
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
            if self._prop_tex[tex] and local_ok and self.local_copy(f"props/tex/{tex}", scrambled=True):
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
    icons = run.load("icons.json", default={}).get(cls, {}).get("outfits", {})
    for o in run.load(f"{cls}/outfits.json"):
        name = f"{cls}/{o['name']}"
        if o.get("tot"):
            run.drop("outfits", name, "ToT's own outfit (never online)")
            continue
        if not o["colors"]:              # a wardrobe_data.py bug (bat/shirt, mole/steamSuit, wolf/novice); ruling R24
            run.drop("outfits", name, "no colours: cannot be dressed")
            continue
        why = "TTO's own outfit (tto flag)" if o.get("tto") else run.bb.compare_outfit(cls, o, run.data / cls / f"o_{o['name']}.bin")
        if why and run.candidate(cls, "outfits", o["name"], why, icon=(icons.get(o["name"]) or {}).get("icon")):
            # released TTO: the local mesh and textures, every colour and edition the data has
            colours = [c for c in o["colors"] if run.local_copy(f"{cls}/tex/{o['name']}{c}.webp", scrambled=True)]
            editions = {e: [c for c in cs if c in colours and run.local_copy(f"{cls}/tex/{o['name']}{c}{e}.webp", scrambled=True)]
                        for e, cs in (o.get("editions") or {}).items()}
            editions = {e: cs for e, cs in editions.items() if cs}
            if not colours or not run.local_copy(f"{cls}/o_{o['name']}.bin", scrambled=True):
                run.drop("outfits", name, "released TTO outfit, but its mesh or colour textures are not in the data")
                continue
            out = {k: v for k, v in o.items() if k != "editions"} | {"colors": colours, "tto": True}
            kept.append(out | ({"editions": editions} if editions else {}))
            continue
        if why:
            run.drop("outfits", name, why + "; not in the released list")
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
        if not colours:
            run.drop("outfits", name, "none of its colour textures has a usable BB file")
            continue
        run.copy(f"{cls}/o_{o['name']}.bin")
        out = {k: v for k, v in o.items() if k != "editions"} | {"colors": colours}
        kept.append(out | ({"editions": editions} if editions else {}))
    run.write_json(f"{cls}/outfits.json", kept)
    return kept


# Classes whose TTO face paints are all released (user 2026-11-07); every other class keeps the first half. Used only
# when there is no tto_released.json (then it is also the picker's starting choice for faces)
TTO_FACES_ALL_RELEASED = {"bison", "chameleon", "mole", "monkey", "penguin", "whale"}
RELEASED_NAME = "tto_released.json"      # <src>/tto_released.json, the picker's file
TTO_KINDS = ("outfits", "weapons", "accessories", "trinkets", "clips", "faces")


def load_released(src):
    """The released list ({cls: {kind: set of names}}), or None when there is no file. A kind or class the picker
    doesn't know stops the publish (a typo would quietly publish nothing)."""
    p = Path(src) / RELEASED_NAME
    if not p.is_file():
        return None
    raw = json.loads(p.read_text(encoding="utf-8"))
    out = {}
    for cls, kinds in raw.items():
        if cls.startswith("_"):
            continue
        if not isinstance(kinds, dict) or set(kinds) - set(TTO_KINDS):
            raise PublishError(f"{RELEASED_NAME}: {cls}: kinds must be among {TTO_KINDS}, got {sorted(kinds) if isinstance(kinds, dict) else kinds!r}")
        out[cls] = {k: {str(n) for n in v} for k, v in kinds.items()}
    return out


def emo_map(page):
    """The page's emote -> emotion icon table (const EMO = {...}), so a released TTO emote's icon can be published."""
    m = re.search(r"const EMO = \{(.*?)\};", page, re.S)
    return dict(re.findall(r'(\w+): "(\w+)"', m.group(1))) if m else {}


def publish_faces(run, cls, faces):
    """BB's faces from the BB rip plus TTO's released ones (the released list; with none, the old rule: all of them for
    TTO_FACES_ALL_RELEASED classes, else the first half by number, rounded down)."""
    own = sorted(f["n"] for f in faces if f.get("tto"))
    legacy = set(own if cls in TTO_FACES_ALL_RELEASED else own[:len(own) // 2])
    overlay, kept, keep_tto = run.bb.heroes / cls / "armors" / "overlay", [], []
    for f in faces:
        rel, name = f"{cls}/faces/{f['n']}.webp", f"{cls}/{f['n']}"
        if f.get("tto"):
            if run.candidate(cls, "faces", f["n"], "TTO's own face", default=f["n"] in legacy, icon=rel) and run.local_copy(rel, scrambled=True):
                kept.append(f)
                keep_tto.append(f["n"])
            else:
                run.drop("faces", name, "TTO's own face, not in the released list")
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
        if c.get("tot"):
            run.drop(kind, f"{cls}/{name}", "ToT's own clip (never online)")
            continue
        why = "TTO's own clip (tto flag)" if c.get("tto") else run.bb.compare_hero_clip(cls, name, c["tracks"])
        if why and why.startswith("keys differ") and not c.get("tto"):
            # BB has this clip but TTO's copy differs (Whale talk: the right foot's 360-degree twist at 1.3-1.7 s is gone in
            # TTO's; pipeline/clip_diff.py): BB's own keys go online instead (user 2026-11-09: "yes you should do that")
            path, tracks = run.bb.bb_hero_tracks(cls, name)[0]
            kept[name] = dict(c, tracks=tracks)
            run.warnings.append(f"{cls}/{name}: TTO's keys differ from BB's {path.name}; published BB's own keys")
            continue
        if why and run.candidate(cls, "clips", name, why, group=c.get("group")):
            kept[name] = dict(c, tto=True)
        elif why:
            run.drop(kind, f"{cls}/{name}", why + ("; not in the released list" if c.get("tto") else ""))
        else:
            kept[name] = c
    run.write_json(f"{cls}/clips.json", kept)
    return kept


def publish_props(run, cls, kind):
    """props_<kind>.json: BB props whose geometry (and clips) equal BB's and whose textures BB has."""
    report_kind, kept = PROP_KINDS[kind], []
    slot = run.load("icons.json", default={}).get(cls, {}).get(kind, {})
    for p in run.load(f"{cls}/props_{kind}.json", default=[]):
        name = f"{cls}/{p['name']}"
        if p.get("tot") or p.get("heroSkin"):
            run.drop(report_kind, name, "ToT's own item (never online)")
            continue
        textures = sorted({m["tex"] for n in p["nodes"] for m in n.get("mats", []) if m.get("tex")})
        why = "TTO's own item (tto flag)" if p.get("tto") else run.bb.compare_prop(cls, kind, p)
        if why:
            ic = slot.get(p["name"]) or slot.get(strip_hand(p["name"])) or slot.get(p["name"].lower()) or {}
            if run.candidate(cls, kind, p["name"], why, icon=ic.get("icon")):
                miss = next((w for w in (run.prop_texture(t, local_ok=True) for t in textures) if w), None)
                if miss:
                    run.drop(report_kind, name, "released TTO item, but " + miss)
                else:
                    kept.append(dict(p, tto=True))
            else:
                run.drop(report_kind, name, why + ("; not in the released list" if p.get("tto") else ""))
            continue
        why = next((w for w in map(run.prop_texture, textures) if w), None)
        if why:
            run.drop(report_kind, name, why)
        else:
            kept.append(p)
    run.write_json(f"{cls}/props_{kind}.json", kept)
    return kept


def publish_community(run, outfits, props):
    """community.json and its pictures (community skins, 2026-11-11; pipeline/wardrobe_community.py): a skin goes online
    when its piece is published and is BB's: a TTO piece has none (user 2026-11-11: "TTO upload should work only on
    private version"; the pop-up shows the 2D texture). Always written, empty or not (the page asks for it)."""
    pub = {("outfits", cls, o["name"]): bool(o.get("tto")) for cls, kept in outfits.items() for o in kept}
    pub |= {(kind, cls, p["name"]): bool(p.get("tto")) for (cls, kind), kept in props.items() for p in kept}
    skins = []
    for s in run.load("community.json", default={"skins": []}).get("skins", []):
        key = (s["kind"], s["cls"], s["item"])
        if key not in pub or pub[key]:
            run.drop("community", f"{s['cls']}/{s['item']}/{s['id']}", "its piece is TTO's" if pub.get(key) else "its piece is not published")
            continue
        for rel in s["tex"].values():
            run.copy(rel)
        skins.append(s)
    run.write_json("community.json", {"skins": skins})


def strip_hand(name):
    return re.sub(r"_[LRlr]$", "", name)


def publish_icons(run, outfits, props):
    """icons.json for the published items only (the page looks a prop up by name, name without _L / _R, then the shared
    table by lower-case name); every picture from the BB rip, a missing one becomes "no icon" (the codes stay: they
    pick TTO's placement entry)."""
    names = {cls: {"outfits": {o["name"] for o in os_}} for cls, os_ in outfits.items()}
    tto = {cls: {"outfits": {o["name"] for o in os_ if o.get("tto")}} for cls, os_ in outfits.items()}
    shared, shared_tto = {}, {}
    for (cls, kind), ps in props.items():
        mine = {p["name"] for p in ps} | {strip_hand(p["name"]) for p in ps}
        names.setdefault(cls, {}).setdefault(kind, set()).update(mine)
        tto.setdefault(cls, {}).setdefault(kind, set()).update(n for p in ps if p.get("tto") for n in (p["name"], strip_hand(p["name"])))
        shared.setdefault(kind, set()).update(p["name"].lower() for p in ps)
        shared_tto.setdefault(kind, set()).update(p["name"].lower() for p in ps if p.get("tto"))
    out = {}
    for cls, slots in run.load("icons.json").items():
        out[cls] = {}
        for slot, entries in slots.items():
            keep = shared.get(slot, set()) if cls == "all" else names.get(cls, {}).get(slot, set())
            out[cls][slot] = {}
            for name, e in entries.items():
                if name not in keep:
                    continue
                local = name in (shared_tto.get(slot, set()) if cls == "all" else tto.get(cls, {}).get(slot, set()))
                e = dict(e, icon=run.icon(e.get("icon"), local_ok=local))
                if e.get("editions"):
                    e["editions"] = {k: v for k, v in ((k, run.icon(v, local_ok=local)) for k, v in e["editions"].items()) if v}
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


def publish_ui(run, classes, tto_clips=None, emo=None):
    """ui.json: the class portraits, emotion and skill icons BB has (re-taken from gamegui/icons), plus the local ones a
    released TTO clip shows (tto_clips {cls: names}; the page's moveIcon: an emote by emo (const EMO) or pose*, a skill by
    its name or its name without the trailing number)."""
    ui, tto_clips, emo = run.load("ui.json"), tto_clips or {}, emo or {}
    out = dict(ui, heroes={}, emotion=[], skills={})
    for cls, rel in ui.get("heroes", {}).items():
        if cls in classes and run.icon(rel, "portraits"):
            out["heroes"][cls] = rel
    emo_used = {emo.get(n.lower()) or ("pose" if n.lower().startswith("pose") else None) for ns in tto_clips.values() for n in ns}
    out["emotion"] = [n for n in ui.get("emotion", []) if run.icon(f"icons/skills/emotion/{n}.webp", local_ok=n in emo_used)]
    bare = lambda x: re.sub(r"\d+$", "", x.lower())
    out["skills"] = {cls: [n for n in names if run.icon(f"icons/skills/{cls}/{n}.webp",
                                                         local_ok=any(n == c.lower() or bare(n) == bare(c) for c in tto_clips.get(cls, ())))]
                     for cls, names in ui.get("skills", {}).items() if cls in classes}
    run.write_json("ui.json", out)


def publish_fx(run, classes):
    """The skill effects and sounds (online since 2026-11-09): for a class that has them, <cls>/fx.json, every texture
    its materials and emblems name (fx/tex/<name>.webp, shared by the classes) and its sounds (<cls>/sfx/). TTO's effects
    (tto/...) are only cued for released TTO skills (the cue files are written against the released list). Returns the
    classes published with effects."""
    done = []
    for cls in classes:
        fx = run.data / cls / "fx.json"
        if not fx.is_file():
            continue
        d = json.loads(fx.read_text(encoding="utf-8"))
        texs = {m.get("tex") for m in d.get("materials", {}).values()} | {c.get("imageTex") for e in d.get("effects", {}).values()
                                                                          for n in e.get("nodes", []) for c in n.get("comps", [])}
        # TTO's effect textures (tto_*) and a fx.json holding TTO effects (the Sheep's Grand Codex book is a whole 3D model)
        # are scrambled like TTO's items (user 2026-11-10: "stop casual copying"); the page's dataBytes() undoes both
        missing = [t for t in sorted(t for t in texs if t) if not run.local_copy(f"fx/tex/{t}.webp", scrambled=t.startswith("tto_"))]
        if missing:
            run.warnings.append(f"{cls}: effect textures not in the data: {missing}")
        run.copy(f"{cls}/fx.json", scrambled=any(k.startswith("tto/") for k in d.get("effects", {})))
        sfx = run.data / cls / "sfx"
        for f in sorted(sfx.glob("*.mp3")) if sfx.is_dir() else []:
            run.copy(f"{cls}/sfx/{f.name}")
        done.append(cls)
    return done


def publish_hd_icons(run, pub_clips):
    """icons/hd/: the Bible's upscaled skill icons (pipeline/wardrobe_skill_icons.py; the user 2026-11-09: "borrow
    upscaled skill icon from the bible"): only the skills whose clips are published (BB's, released TTO ones), and the
    index filtered to them. No index in the data: nothing."""
    index = run.load("icons/hd/index.json", default={})
    out = {}
    for cls, skills in index.items():
        keep = {s: dict(v, clips=[c for c in v["clips"] if c in pub_clips.get(cls, set())]) for s, v in skills.items()}
        keep = {s: v for s, v in keep.items() if v["clips"] and run.local_copy(v["icon"])}
        if keep:
            out[cls] = keep
    if index:
        run.write_json("icons/hd/index.json", out)


def stage_data(data, stage, bb, released=None, candidates=None, emo=None):
    """Write the filtered data to stage/; returns (dropped, tto_faces, warnings). released: load_released()'s list;
    candidates, a list, gets every TTO-sourced item (for the picker)."""
    run = Run(data, stage, bb, released)
    tto_clips, pub_clips = {}, {}
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
        tto_clips[cls] = [k for k, v in clips.items() if v.get("tto")]
        pub_clips[cls] = set(clips)
        for kind in PROP_KINDS:
            props[(cls, kind)] = publish_props(run, cls, kind)
        meta_out["classes"].append(dict(c, outfits=len(outfits[cls]), faces=faces,
                                        clips={k: v for k, v in c["clips"].items() if k in clips}))
    for kind in SHARED_KINDS:
        props[("all", kind)] = publish_props(run, "all", kind)
    publish_community(run, outfits, props)
    icons = publish_icons(run, outfits, props)
    publish_item_map(run, outfits, props)
    publish_placements(run, icons)
    publish_ui(run, classes, tto_clips, emo)
    publish_hd_icons(run, pub_clips)
    publish_fx(run, classes)
    run.write_json("meta.json", meta_out)
    if candidates is not None:
        candidates.extend(run.candidates)
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


def headers_text(data_dir, ui_dir):
    # Cloudflare allows one splat a rule, so each rule names this publish's folder; both folders are named by a hash of
    # their content, so a changed file always comes under a new name and the old one may stay cached for a year
    immutable = "  Cache-Control: public, max-age=31536000, immutable\n"
    # the effects' cue files and part modules keep their names across publishes: asked for again every time (no-cache)
    return (f"/{data_dir}/*\n{immutable}/{ui_dir}/*\n{immutable}/\n  Cache-Control: no-cache\n"
            "/fx_cues/*\n  Cache-Control: no-cache\n/fxparts/*\n  Cache-Control: no-cache\n")


def remove(path):
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def over_black(im):
    base = Image.new("RGBA", im.size, (0, 0, 0, 255))
    base.alpha_composite(im.convert("RGBA"))
    return base.convert("RGB")


def verify_ui_icons(src, bb):
    """The page's own pictures (src/ui/*.webp) are BB's Recolor Drug icons (the colour topic), upscaled and cropped to
    the potions' square: each is shrunk to the size of UI_CROP and compared with that box of
    gamegui/icons/items/field/rsc<n>.png over black; a mean absolute difference above UI_MAX_DIFF in any channel, a file
    with no BB counterpart, a missing BB file or a missing picture (the page needs all five) stops the publish.
    Returns the file names."""
    folder = Path(src) / UI_DIR
    names = sorted(p.name for p in folder.iterdir()) if folder.is_dir() else []
    want = [f"recolor{n}.webp" for n in range(1, UI_COUNT + 1)]
    missing = [n for n in want if n not in names]
    if missing:
        raise PublishError(f"{UI_DIR}/: the page's colour pictures {missing} are missing")
    if UI_TTO not in names:
        raise PublishError(f"{UI_DIR}/{UI_TTO}: the TTO mark is missing")
    for name in names:
        if name == UI_TTO:                  # TTO's own logo, not BB's: allowed since TTO is online (2026-11-09)
            continue
        m = UI_ICON.fullmatch(name)
        if not m:
            raise PublishError(f"{UI_DIR}/{name}: not a BB Recolor Drug icon (recolor1.webp .. recolor5.webp only), "
                               "so it cannot be proven to be BB's")
        bb_file = bb.find_rel(bb.icons, f"items/field/rsc{m.group(1)}.png")
        if bb_file is None:
            raise PublishError(f"{UI_DIR}/{name}: no BB file gamegui/icons/items/field/rsc{m.group(1)}.png to compare with")
        with Image.open(bb_file) as ref_im, Image.open(folder / name) as mine_im:
            ref = over_black(ref_im.convert("RGBA").crop(UI_CROP))
            mine = over_black(mine_im.resize(ref.size, Image.LANCZOS))
        diff = ImageStat.Stat(ImageChops.difference(ref, mine)).mean
        if max(diff) > UI_MAX_DIFF:
            raise PublishError(f"{UI_DIR}/{name} is not BB's Recolor Drug {m.group(1)}: its mean difference from "
                               f"rsc{m.group(1)}.png (box {UI_CROP}) over black is {max(diff):.1f} per channel (limit {UI_MAX_DIFF})")
    return names


def publish(src, out, bb_rip, data=None, fallback_rip="beside"):
    """Build the public copy of src (wardrobe/: index.html, its icons and ui pictures) with the data in data (default
    src/data) in out. Returns {files, bytes, data_dir, ui_dir, ui_files, dropped: {kind: [{name, reason}]},
    tto_faces: {cls: [kept numbers]}, warnings}. The previous copy stays whole until the new data is staged; then its files are moved aside into
    out/.previous, the new ones put in place and the old ones deleted. On any failure the new files go, the old ones
    come back and neither .data-staging nor .previous is left in out (wrangler would upload them)."""
    src, out = Path(src), Path(out)
    data = src / "data" if data is None else Path(data)
    with open(src / "index.html", encoding="utf-8", newline="") as fh:
        page = fh.read()
    rewrite_page(page, "data-" + "0" * 10)                   # a changed page fails before anything is written
    missing = [f for f in PAGE_FILES if not (src / f).is_file()]
    if missing:
        raise PublishError(f"the page's icon files {missing} are not in {src}")
    if not (data / "meta.json").is_file():
        raise PublishError(f"no wardrobe data at {data} (no meta.json); --data names the data folder")
    fallback_rip = reborn_rip(bb_rip) if fallback_rip == "beside" else fallback_rip
    bb = BBRip(bb_rip, fallback=BBRip(fallback_rip) if fallback_rip else None)
    ui_files = verify_ui_icons(src, bb)             # before anything is written
    ui_dir = "ui-" + tree_hash(src / UI_DIR)        # its name changes with any of its pictures (a year-long cache)
    out.mkdir(parents=True, exist_ok=True)
    stage, previous = out / ".data-staging", out / ".previous"
    remove(stage)
    remove(previous)                                # a run killed mid-swap: the data rebuilds the copy anyway
    try:
        candidates = []
        dropped, tto_faces, warnings = stage_data(data, stage, bb, load_released(src), candidates, emo_map(page))
        warnings = warnings + bb.fallback_used
        data_dir = "data-" + tree_hash(stage)
        previous.mkdir()
    except BaseException:
        remove(stage)
        raise
    old = [p.name for p in out.iterdir() if p.name.startswith(HASHED_PREFIXES) or p.name in OUTPUT_NAMES]
    moved, written = [], []                         # every old file is moved aside before the first new one is written

    def put(name, write):
        written.append(name)                        # before the write: a half-written file goes too on a failure
        write(out / name)

    def copy_ui(folder):
        folder.mkdir()
        for f in ui_files:
            shutil.copy2(src / UI_DIR / f, folder / f)
    try:
        for name in old:
            (out / name).rename(previous / name)
            moved.append(name)
        put(data_dir, stage.rename)
        put("index.html", lambda p: p.write_text(rewrite_page(page, data_dir, ui_dir), encoding="utf-8", newline=""))
        put(ui_dir, copy_ui)
        for f in PAGE_FILES:
            put(f, lambda p: shutil.copy2(src / p.name, p))
        for f in PAGE_DIRS:                        # the effects' cue files and part modules (only their own files)
            if (src / f).is_dir():
                put(f, lambda p: shutil.copytree(src / p.name, p, ignore=shutil.ignore_patterns("*.tmp", ".*")))
        put("_headers", lambda p: p.write_text(headers_text(data_dir, ui_dir), encoding="utf-8", newline="\n"))
    except BaseException as e:
        try:
            for name in written:
                remove(out / name)
            for name in moved:
                (previous / name).rename(out / name)
            remove(previous)
            remove(stage)
        except OSError as undo:
            raise PublishError(f"the publish failed ({e!r}) and putting the previous copy back failed too ({undo}): "
                               f"the previous copy is in {previous}; move its contents back into {out} by hand") from e
        raise
    remove(previous)
    files = [p for p in out.rglob("*") if p.is_file()]
    return {"files": len(files), "bytes": sum(p.stat().st_size for p in files), "data_dir": data_dir,
            "ui_dir": ui_dir, "ui_files": list(ui_files),
            "dropped": dropped, "tto_faces": tto_faces, "warnings": warnings, "tto_candidates": candidates,
            "tto_released_file": (src / RELEASED_NAME).is_file()}


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
    ui = re.search(r'const UI_DIR = "([^"]*)/";', html)
    ui_refs = []
    if ui and not re.fullmatch(r"ui-[0-9a-f]{10}", ui.group(1)):
        problems.append(f'index.html has no hashed ui folder (const UI_DIR = "{ui.group(1)}/";)')
    elif ui:
        ui_refs = [f"{ui.group(1)}/recolor{n}.webp" for n in range(1, UI_COUNT + 1)]
        if f"/{ui.group(1)}/*\n" not in headers:
            problems.append(f"_headers has no rule for /{ui.group(1)}/* (the ui pictures would not be cached)")
    icons = page_icons(html)
    if not icons:
        problems.append('index.html has no tab icon (<link rel="icon" href="...">)')
    refs = icons + ui_refs
    refs += [f"{data_dir}/{r}" for r in data_references(out / data_dir, problems)]
    walker = CaseSensitive(out)
    problems += [p for p in (walker.problem(r) for r in dict.fromkeys(refs)) if p]
    return problems


# ---------------------------------------------------------------- command line
def report_path(out, suffix=""):
    return Path(out).parent / f"{Path(out).name}_report{suffix}.json"


def report_counts(report):
    """What two runs are compared on: files, bytes, dropped items per kind, kept TTO faces per class."""
    counts = {"files": report.get("files", 0), "bytes": report.get("bytes", 0)}
    counts |= {f"dropped {kind}": len(items) for kind, items in (report.get("dropped") or {}).items()}
    counts |= {f"kept TTO faces {cls}": len(kept) for cls, kept in (report.get("tto_faces") or {}).items()}
    return counts


def count_changes(prev, cur):
    """'what: old -> new (+-n)' for every count that differs between two reports (a count a report lacks is 0)."""
    a, b = report_counts(prev), report_counts(cur)
    keys = ["files", "bytes"] + sorted((a.keys() | b.keys()) - {"files", "bytes"})
    return [f"{k}: {a.get(k, 0):,} -> {b.get(k, 0):,} ({b.get(k, 0) - a.get(k, 0):+,})"
            for k in keys if a.get(k, 0) != b.get(k, 0)]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Publish the 12 Tails Wardrobe for Cloudflare Pages (BB items only).")
    ap.add_argument("--src", type=Path, default=ROOT / "wardrobe", help="the wardrobe folder (index.html and its icons)")
    ap.add_argument("--data", type=Path, help="the wardrobe data folder (default: <src>/data)")
    ap.add_argument("--out", type=Path, default=ROOT / "wardrobe_dist", help="the output folder")
    ap.add_argument("--bb-rip", type=Path, default=BB_RIP, help="BB's rip: ...\\ExportedProject\\Assets\\Resources")
    ap.add_argument("--check", type=Path, metavar="DIR", help="only check an existing output folder")
    a = ap.parse_args(argv)
    if a.check:
        problems = check(a.check)
        print("\n".join(problems) or "no problems")
        return 1 if problems else 0
    try:
        result = publish(a.src, a.out, a.bb_rip, a.data)
    except PublishError as e:
        print(f"publish failed: {e}", file=sys.stderr)
        return 1
    problems = check(a.out)
    candidates = result.pop("tto_candidates")
    tto_path = Path(a.out).parent / f"{Path(a.out).name}_tto.json"      # the picker's list (wardrobe/tto_picker.html)
    tto_path.write_text(json.dumps({"released_file": result.pop("tto_released_file"), "items": candidates}, indent=1, ensure_ascii=False), encoding="utf-8")
    report = {"provenance": PROVENANCE, **result, "problems": problems}
    path, prev_path, prev = report_path(a.out), report_path(a.out, ".prev"), None
    if path.is_file():                                  # the last run's report becomes <out>_report.prev.json
        try:
            prev = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, UnicodeDecodeError):
            prev = "unreadable"
        os.replace(path, prev_path)
    path.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{a.out}: {result['files']:,} files, {result['bytes'] / 1e6:.1f} MB, data folder {result['data_dir']}")
    print(f"  ui folder {result['ui_dir']}: " + ", ".join(result["ui_files"]))
    for kind, items in sorted(result["dropped"].items()):
        print(f"  dropped {kind}: {len(items)}")
    print("  kept TTO faces: " + ", ".join(f"{cls} {v[0]}-{v[-1]}" if v else f"{cls} none" for cls, v in result["tto_faces"].items()))
    for w in result["warnings"]:
        print(f"  warning: {w}")
    if not isinstance(prev, dict):
        print("changes: " + ("no previous report to compare with" if prev is None else f"{prev_path} could not be read"))
    else:
        changes = count_changes(prev, result)
        print(f"changes since the previous report ({prev_path.name}):" + ("" if changes else " none"))
        for line in changes:
            print(f"  {line}")
    n_rel = sum(1 for c in candidates if c["released"])
    print(f"TTO: {n_rel} of {len(candidates)} TTO-sourced items released ({tto_path.name})")
    print(f"report: {path}")
    print("\n".join(f"  problem: {p}" for p in problems) or "check: no problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
