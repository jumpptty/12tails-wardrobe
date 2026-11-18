r"""Headless check of the pet on stage (2026-11-18, the pets plan's Task 5; user: "Add Pet section, standing behind the
hero how it would work in game"). On the real page through its scripting hook (wardrobe.show / wardrobe.debug()):
  - placement: for 4 classes x {smallAnubi, miniMokBug, kiteChula, smallKumo, smallDragonZ (TTO's own), soccerBall (x
    offsets: the mirror)}, setPet(name): the pet stands beside the hero (on none of its bones), its world position = the index
    row's rest[cls] = pipeline/wardrobe_pets.py's rest_point of the game's Unity-space values (the row's offsets x -> -x)
    within 1e-3, its rotation the hero's, its scale the row's scale[cls]; its idle clip loops and its mixer advances (a
    node's quaternion changes over 0.5 s; smallKumo's clip turns nothing, its one node bobs: its position / scale); no
    mixer when its file has no clip
  - Review Focus 1: a saved loadout naming a pet the data does not have ("noSuchPet"): the class loads with no pet, no
    request for it, no error toast, no console error
  - Review Focus 2: two picks 50 ms apart (pets not loaded yet; the first one's file held back 1 s, so the second lands
    first; then with no hold): only the second is on stage at the end, the held one never, one undo step per pick
    (undo: the first, then none; redo back)
  - Review Focus 3: class switches with a pet out: TianlongA (p_all85) at 1.5x beside the Bison, 2.0x beside the Whale,
    each class's own pet back at its rest point and scale after a switch and after a reload; a kite at each class's height
  - Review Focus 4: ชมชิ้นส่วน (Showcase) on the outfit hides the pet with the character; its exit shows it again
  - the คัดลอกให้ Claude line names the pet (สัตว์เลี้ยง <name>); no page errors, console errors or failed requests
  - skill effects (the controller's ruling 2026-11-19: in the game the pet is a GameObject of its own): with smallAnubi
    out, the Bison's Enrage (grow + tint), its Titan Drop (a lift), the Chameleon's Back Step (FX/Blend shells) and the
    Bat's Shadow Illusion (two HeroClones) each take hold on the hero and leave the pet as it was (world position and
    scale, material colours, layers, no shell on it, no copy of it in a clone); the Chameleon's Thunder Dragon (a
    whole-hero hide) hides it with the hero (TTO's PetControl.OnParentHide@0x1a94140) and shows it again after
  - downloads (the pets plan's Task 8; user 2026-11-18: "the model and texture should be downloadable like other assets,
    Same logic, TTO exclusive remains undownloadable"), each on its own page, the menu opened by a click on the pet on
    stage (the ray pieceAt casts; the hover lights the pet): a BB pet's menu lists exactly change (once the สัตว์เลี้ยง
    topic exists) / ถอดสัตว์เลี้ยงออก / ดาวน์โหลดลาย (PNG) per texture (numbered when two) / ดาวน์โหลดโมเดล 3D (GLB): no
    view-alone, upload, reset or community item, no Ctrl+V hint; each download is 12tails_<class in Thai>_<pet>[_ลาย<n>]
    .png / .glb, the PNG byte-equal to the data's, the GLB loading back in GLTFLoader with the pet's skins on their bones
    and every texture embedded byte-equal (smallAnubi on the Sheep; miniAncientBug, two textures, on the Wolf); the TTO
    pet (smallDragonZ) downloads locally too; with ?ttolock (the online rule, Review Focus 5) the TTO pet's menu has no
    download item and a BB pet's keeps both; a picture pasted or dropped on the pet puts no skin on anything; ถอด takes
    it off in one undo step; the ring's เปลี่ยนสัตว์เลี้ยง opens the สัตว์เลี้ยง picker; a picker tile's menu (right-click)
    on a pet whose file is not loaded yet lists its downloads (a BB pet) or none (TTO's under ?ttolock)
  - the สัตว์เลี้ยง topic, its picker and the camera (the pets plan's Task 7; the picks of 2026-11-18,
    plans/wardrobe_pets_design.md), at 1600x1000 and 390x700 (and 1600x1200 for the layout): the blocks two by two
    (หมวก + ชุด, อาวุธ + ประดับ, สัตว์เลี้ยง + ท่าทาง), the ring empty (the slot's outline) or the worn pet's icon; the
    picker = ไม่ใส่ + one tile per index row (its icon, the game's name or the name as words, TTO's mark), nicknamed
    first, the ค้นหา box (a game name "L. Carron", "Anubi", a nickname "ALL 9" / "all9", nonsense); a pick = one undo
    step, the picker stays open; the camera: no pet = today's front view exactly (FIT_DIR, today's heroFitPose
    recomputed here), a pet = turned 40 deg, rise .10 (FIT_DIR_PET), gliding there unless the visitor moved it, the
    hero's and the pet's box corners on the free part of the stage (the toolbar band clear) for a walker 1 m and 2 m
    back, a kite, TianlongA at 2x, and after the desktop picker closes and opens again; the สัตว์เลี้ยง label on a phone:
    no mark clipped, its ink centred by eye in its block (gaps within 2 px at 2x); screenshots in checks/pet_ui/ (a run
    given an out folder: <out>/pet_ui)
  - the pet's whole idle framed (Task 7's fix round 1): for TianlongA beside the Whale, smallAnubi and miniMokBug, the
    desktop picker open, closed and open again (a phone: its sheet open), the idle held (hero and pet: their mixers'
    times unchanged through each screenshot), then the frame shown and 16 more of the pet's idle clip rendered through
    the live camera: no drawn pixel (alpha >= 128) under the picker, on the stage's edge rows / columns or behind the
    toolbar, and the pet's box inside the fit's margins at every frame
Exit 1 on any failure. Serves the folder itself on a free port (never 8771, the main folder's page). --downloads / --ui
run that part alone.
  uv run --no-project --with playwright==1.65.1 python -I pipeline/wardrobe_pet_check.py [D:/12tails-wardrobe checks/pet_check] [--downloads | --ui]"""
import asyncio, base64, functools, http.server, json, math, re, struct, sys, threading
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")       # Thai on any console
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))                  # -I leaves the script's folder off the path: the rules' module by its bare name
from wardrobe_pets import rest_point           # noqa: E402  (the pure rules; no UnityPy at import)

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
DOWNLOADS_ONLY = "--downloads" in sys.argv
UI_ONLY = "--ui" in sys.argv
ROOT = Path(ARGS[0]) if ARGS else HERE.parent
OUT = Path(ARGS[1]) if len(ARGS) > 1 else ROOT / "checks" / "pet_check"
OUT.mkdir(parents=True, exist_ok=True)
ROWS = {r["name"]: r for r in json.loads((ROOT / "wardrobe" / "data" / "pets" / "index.json").read_text(encoding="utf-8"))}
CLASSES = ["sheep", "bison", "mole", "wolf"]
PETS = ["smallAnubi", "miniMokBug", "kiteChula", "smallKumo", "smallDragonZ", "soccerBall"]
SAVED = {"cls": "sheep", "sheep": {"outfit": "standard", "color": 1, "edition": "", "face": 14, "Pet": "noSuchPet"}}


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


http.server.ThreadingHTTPServer.request_queue_size = 128     # the page loads dozens of icons at once
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/wardrobe/index.html"

# the pet on stage: what the state says, what stands under the hero's root, where and how big
PET = """() => { const { C, THREE, scene } = wardrobe.debug(), o = C.props.Pet;
  const pets = []; scene.traverse(x => { if (x.userData.pet) pets.push(x.userData.pet); });
  const base = { cls: C.cls, state: 'Pet' in C.state ? C.state.Pet : '(no key)', pets };
  if (!o) return { ...base, on: null };
  o.updateWorldMatrix(true, false);
  const p = o.getWorldPosition(new THREE.Vector3()), s = o.getWorldScale(new THREE.Vector3());
  const q = o.getWorldQuaternion(new THREE.Quaternion()), h = C.root.getWorldQuaternion(new THREE.Quaternion());
  let shown = true, top = o, onBone = false; for (let x = o; x; x = x.parent) { if (!x.visible) shown = false; if (x === C.tri) onBone = true; top = x; }
  const pa = o.userData.propAnim;
  return { ...base, on: o.userData.pet, onBone, p: p.toArray(), s: s.toArray(), qdot: Math.abs(q.dot(h)),
    mixer: !!o.userData.mixer, loop: pa ? pa.act.loop === THREE.LoopRepeat : null, shown: shown && top === scene }; }"""
# the idle clip's nodes now: the mixer's time, each animated node's quaternion, position and scale
MOTION = """() => { const o = wardrobe.debug().C.props.Pet, pa = o?.userData.propAnim; if (!pa) return null;
  const names = [...new Set(pa.act.getClip().tracks.map(t => t.name.split('.')[0]))];
  return { t: o.userData.mixer.time, nodes: names.map(n => { const x = o.getObjectByName(n);
    return x ? [...x.quaternion.toArray(), ...x.position.toArray(), ...x.scale.toArray()] : null; }) }; }"""
SHOW = "c => wardrobe.show(c)"
SET = "n => wardrobe.debug().setPet(n)"


def unity(follow):          # the row's follow is three.js space (x mirrored); rest_point takes the game's Unity values
    return {**follow, "offset": {c: [-v[0], v[1], v[2]] for c, v in follow["offset"].items()}}


def near(a, b, tol):
    return a is not None and b is not None and len(a) == len(b) and all(abs(x - y) <= tol for x, y in zip(a, b))


# ---- downloads (Task 8)
TEX = ROOT / "wardrobe" / "data" / "props" / "tex"
CLASS_TH = {"sheep": "แกะ", "wolf": "หมาป่า"}
STEM = {"smallAnubi": "Small_Anubi", "miniAncientBug": "Mini_Ancient_Bug", "smallDragonZ": "Small_Dragon_Z"}   # humanize(), spaces -> _
# the pet's screen points under the page's own ray (pieceAt), inside the pet's projected box: the one nearest their middle
PET_POINT = """() => { const { pieceAt, renderer, camera, C, THREE } = wardrobe.debug(), o = C.props.Pet; if (!o) return null;
  const r = renderer.domElement.getBoundingClientRect(), b = new THREE.Box3().setFromObject(o, true), v = new THREE.Vector3();
  let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
  for (let i = 0; i < 8; i++) { v.set(i & 1 ? b.max.x : b.min.x, i & 2 ? b.max.y : b.min.y, i & 4 ? b.max.z : b.min.z).project(camera);
    const x = r.left + (v.x + 1) / 2 * r.width, y = r.top + (1 - v.y) / 2 * r.height;
    x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
  const ps = [];
  for (let y = Math.max(r.top + 2, y0); y < Math.min(r.bottom - 2, y1); y += 4) for (let x = Math.max(r.left + 2, x0); x < Math.min(r.right - 2, x1); x += 4)
    if (pieceAt(x, y)?.slot === 'Pet') ps.push([Math.round(x), Math.round(y)]);
  if (!ps.length) return null;
  const cx = ps.reduce((a, p) => a + p[0], 0) / ps.length, cy = ps.reduce((a, p) => a + p[1], 0) / ps.length;
  return ps.reduce((a, p) => (Math.hypot(p[0] - cx, p[1] - cy) < Math.hypot(a[0] - cx, a[1] - cy) ? p : a)); }"""
PMENU = """() => { const el = document.getElementById('pmenu'), { PM } = wardrobe.debug();
  return { open: !el.hidden, slot: PM.cur?.slot ?? null, item: PM.cur?.item ?? null, from: PM.cur?.from ?? null,
    name: el.querySelector('.pm-name')?.innerText ?? null, meta: el.querySelector('.pm-meta')?.innerText ?? null,
    items: [...el.querySelectorAll('.pm-item')].map(b => ({ a: b.dataset.a, tex: b.dataset.tex ?? null, label: b.innerText.trim().replace(/\\s+/g, ' '), off: b.disabled })),
    foot: el.querySelector('.pm-foot')?.innerText ?? null }; }"""
HOVERED = "() => ({ slot: wardrobe.debug().Hover.slot, cursor: document.querySelector('canvas').style.cursor })"
# the downloaded GLB back through three's own GLTFLoader: its skinned meshes (bone names, every bone in the scene's tree,
# a texture on every material) and its plain meshes
LOAD_GLB = """async b64 => { const { GLTFLoader } = await import('three/addons/loaders/GLTFLoader.js');
  const bin = Uint8Array.from(atob(b64), c => c.charCodeAt(0)), g = await new GLTFLoader().parseAsync(bin.buffer, '');
  const inTree = x => { for (let y = x; y; y = y.parent) if (y === g.scene) return true; return false; };
  const skins = [], meshes = [];
  g.scene.traverse(o => { if (!o.isMesh) return; const e = { name: o.name, verts: o.geometry.attributes.position.count,
    maps: [].concat(o.material).map(m => !!m.map?.image) };
    if (o.isSkinnedMesh) skins.push({ ...e, bones: o.skeleton.bones.map(b => b.name), tree: o.skeleton.bones.every(inTree) }); else meshes.push(e); });
  return { skins, meshes }; }"""
# a picture on the pet: pasted with the pointer over it (Ctrl+V), then dropped on it
PICTURE = """async ([how, x, y]) => { const { SKINS, renderer } = wardrobe.debug();
  const png = await (await fetch('data/props/tex/Anubi.png')).blob(), dt = new DataTransfer();
  dt.items.add(new File([png], '12tails_แกะ_Small_Anubi.png', { type: 'image/png' }));
  document.getElementById('toast').innerHTML = '';
  if (how === 'paste') document.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
  else renderer.domElement.dispatchEvent(new DragEvent('drop', { dataTransfer: dt, clientX: x, clientY: y, bubbles: true, cancelable: true }));
  await new Promise(r => setTimeout(r, 600));
  return { skins: SKINS.size, toast: document.getElementById('toast').innerText, menu: !document.getElementById('pmenu').hidden }; }"""


def glb_parts(data):            # a binary glTF's JSON and its images' bytes
    magic, _, length = struct.unpack_from("<III", data, 0)
    if magic != 0x46546C67:
        return None, []
    off, js, bin_ = 12, None, b""
    while off < length:
        n, kind = struct.unpack_from("<II", data, off)
        if kind == 0x4E4F534A:
            js = json.loads(data[off + 8: off + 8 + n])
        elif kind == 0x004E4942:
            bin_ = data[off + 8: off + 8 + n]
        off += 8 + n
    imgs = []
    for im in (js or {}).get("images", []):
        bv = js["bufferViews"][im["bufferView"]]
        imgs.append((im.get("mimeType"), bin_[bv.get("byteOffset", 0): bv.get("byteOffset", 0) + bv["byteLength"]]))
    return js, imgs


def pet_parts(name):            # from the pet's file: its textures (the menu's order), the shown skins' bone names, shown meshes
    nodes = json.loads((ROOT / "wardrobe" / "data" / ROWS[name]["file"]).read_text(encoding="utf-8"))["nodes"]

    def shown(i):
        while i >= 0:
            if nodes[i].get("on") is False:
                return False
            i = nodes[i]["parent"]
        return True
    texs = list(dict.fromkeys(m["tex"] for n in nodes for m in (n.get("mats") or []) if m.get("tex")))
    drawn = list(dict.fromkeys(m["tex"] for i, n in enumerate(nodes) if shown(i) for m in (n.get("mats") or []) if m.get("tex")))
    # GLTFLoader's node names: PropertyBinding.sanitizeNodeName (white space -> _, [ ] . : / dropped)
    clean = lambda s: re.sub(r"[\[\].:/]", "", re.sub(r"\s", "_", s))
    skins = [[clean(nodes[b]["name"]) for b in n["skin"]["bones"]] for i, n in enumerate(nodes) if n.get("skin") and shown(i)]
    return texs, drawn, skins, sum(1 for i, n in enumerate(nodes) if n.get("mesh") and shown(i))


async def downloads(b, check, errors):
    """the pet's piece menu and its downloads, on pages of their own (the local copy, then ?ttolock)"""
    ctx = await b.new_context(viewport={"width": 1366, "height": 768}, accept_downloads=True)

    async def page_at(query):
        page = await ctx.new_page()
        page.on("pageerror", lambda e: errors.append(f"{query or 'local'}: {e}"))
        page.on("console", lambda m: m.type == "error" and errors.append(f"{query or 'local'}: {m.text} {(m.location or {}).get('url', '')}"))
        page.on("requestfailed", lambda r: errors.append(f"{query or 'local'}: request failed {r.url} {r.failure}"))
        await page.goto(URL + query)
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
        return page

    async def wear(page, cls, name):       # the pet out, seen from the side (yaw 110: it stands behind the hero), held still
        await page.evaluate("([c, n]) => wardrobe.show(c, { Pet: n }, 110)", [cls, name])
        await page.wait_for_function("n => { const { C } = wardrobe.debug(); return C.props.Pet?.userData.pet === n; }", arg=name, timeout=60000)
        await page.wait_for_timeout(500)                       # its textures in (the ray skips what alphaTest cuts)
        await page.keyboard.press("Space")                     # the idle held: the point found stays on the pet
        return await page.evaluate(PET_POINT)                  # (once: a skinned pet's rays are slow)

    async def menu(page, name, what, pt):  # a click on the pet on stage: its menu (the hover lights it first)
        if not pt:
            check(False, f"{what}: the pet is under no screen point (pieceAt never says slot 'Pet')")
            return None
        await page.mouse.move(*pt)
        await page.wait_for_timeout(300)
        hv = await page.evaluate(HOVERED)
        await page.mouse.click(*pt)
        await page.wait_for_timeout(250)
        m = await page.evaluate(PMENU)
        check(hv["slot"] == "Pet" and hv["cursor"] == "pointer", f"{what}: hover at {pt} lights {hv['slot']}, cursor {hv['cursor']!r}")
        check(m["open"] and m["slot"] == "Pet" and m["item"] == name and m["from"] == "model",
              f"{what}: a click on the pet opens its menu: open {m['open']}, {m['slot']} {m['item']} from {m['from']}")
        return m if m["open"] else None

    async def grab(page, sel):
        async with page.expect_download(timeout=60000) as d:
            await page.click(sel)
        dl = await d.value
        return dl.suggested_filename, Path(await dl.path()).read_bytes()

    def items_ok(m, name, cls, locked, tag=""):            # locked: no download item (a TTO pet under ?ttolock)
        texs = pet_parts(name)[0]
        want = ["change", "remove"]                        # (the สัตว์เลี้ยง topic exists: its change item always)
        if not locked:
            want += [f"png:{t}" for t in texs] + ["glb"]
        got = [i["a"] + (":" + i["tex"] if i["tex"] else "") for i in m["items"]]
        labels = {i["a"] + (":" + i["tex"] if i["tex"] else ""): i["label"] for i in m["items"]}
        want_labels = {"remove": "ถอดสัตว์เลี้ยงออก", "change": "เปลี่ยนสัตว์เลี้ยง", "glb": "ดาวน์โหลดโมเดล 3D (GLB)",
                       **{f"png:{t}": "ดาวน์โหลดลาย (PNG)" + (f" {k + 1}" if len(texs) > 1 else "") for k, t in enumerate(texs)}}
        row = ROWS[name]
        head = row["game"] or STEM[name].replace("_", " ")
        ok = (got == want and all(labels.get(k) == want_labels[k] for k in want) and not any(i["off"] for i in m["items"])
              and m["foot"] is None and m["name"] == head and "สัตว์เลี้ยง" in (m["meta"] or "") and "ใส่อยู่" in (m["meta"] or "")
              and (("ของจาก TTO" in m["meta"]) == bool(row["tto"])))
        check(ok, f"{cls:6} {name:14} {tag}menu {got} (want {want}); "
                  f"labels {[labels.get(k) for k in got]}; head {m['name']!r} [{m['meta']}]; Ctrl+V hint {m['foot']!r}")

    async def tile_menu(page, name, want, tag):   # right-click on a picker tile of a pet not loaded yet: its menu
        loaded = await page.evaluate("n => wardrobe.debug().C.propLists.pets.some(p => p.name === n)", name)
        if not await page.locator('#topics button.topic[data-t="Pet"]').count():
            check(False, f"{tag}: no สัตว์เลี้ยง topic to open")
            return
        if await page.evaluate("() => document.getElementById('pkBody').dataset.topic !== 'Pet' || document.getElementById('picker').hidden"):
            await page.click('#topics button.topic[data-t="Pet"]')
        cell = page.locator(f'#pkBody .pk-cell[data-slot="Pet"][data-item="{name}"]')
        try:
            await cell.wait_for(timeout=15000)
        except Exception:
            check(False, f"{tag}: no tile for {name} in the สัตว์เลี้ยง picker")
            return
        await cell.scroll_into_view_if_needed()
        await page.wait_for_timeout(400)              # (the list's scroll closes a tile's menu: done before the click)
        await cell.click(button="right")
        try:
            await page.wait_for_function("n => wardrobe.debug().PM.cur?.item === n", arg=name, timeout=15000)
        except Exception:
            pass
        m = await page.evaluate(PMENU)
        got = [i["a"] + (":" + i["tex"] if i["tex"] else "") for i in m["items"]]
        row = ROWS[name]
        check(not loaded and m["open"] and m["slot"] == "Pet" and m["from"] == "tile" and got == want and not any(i["off"] for i in m["items"])
              and (("ของจาก TTO" in (m["meta"] or "")) == bool(row["tto"])),
              f"{tag}: the tile's menu, its file not loaded before ({not loaded}): {got} (want {want}), "
              f"disabled {[i['a'] for i in m['items'] if i['off']]}, head {m['name']!r} [{m['meta']}]")
        await page.keyboard.press("Escape")
        await page.evaluate("() => { if (!document.getElementById('picker').hidden) document.getElementById('pkClose').click(); }")

    # ---- the local copy: every pet downloads
    page = await page_at("")
    # a tile's menu before the pet's file is in (Task 8's review): its downloads all there
    await tile_menu(page, "smallAnubi", ["wear", "png:Anubi.png", "glb"], "sheep  smallAnubi     tile")
    for cls, name in (("sheep", "smallAnubi"), ("wolf", "miniAncientBug"), ("sheep", "smallDragonZ")):
        pt = await wear(page, cls, name)
        m = await menu(page, name, f"{cls:6} {name:14}", pt)
        if not m:
            continue
        items_ok(m, name, cls, False)
        texs, drawn, skins, meshes = pet_parts(name)
        await page.keyboard.press("Escape")
        stem = f"12tails_{CLASS_TH[cls]}_{STEM[name]}"
        for k, t in enumerate(texs):
            if not await menu(page, name, f"{cls:6} {name:14} (for ลาย {k + 1})", pt):
                break
            if not await page.locator(f'#pmenu .pm-item[data-a="png"][data-tex="{t}"]').count():
                check(False, f"{cls:6} {name:14} no ดาวน์โหลดลาย item for {t}")
                await page.keyboard.press("Escape")
                continue
            fn, data = await grab(page, f'#pmenu .pm-item[data-a="png"][data-tex="{t}"]')
            want = stem + (f"_ลาย{k + 1}" if len(texs) > 1 else "") + ".png"
            check(fn == want and data == (TEX / t).read_bytes(), f"{cls:6} {name:14} ดาวน์โหลดลาย {t}: {fn} (want {want}), "
                                                                 f"{len(data)} bytes, byte-equal to data/props/tex/{t} {data == (TEX / t).read_bytes()}")
        if not await menu(page, name, f"{cls:6} {name:14} (for the GLB)", pt):
            continue
        if not await page.locator('#pmenu .pm-item[data-a="glb"]').count():
            check(False, f"{cls:6} {name:14} no ดาวน์โหลดโมเดล 3D item")
            await page.keyboard.press("Escape")
            continue
        fn, data = await grab(page, '#pmenu .pm-item[data-a="glb"]')
        (OUT / fn).write_bytes(data)
        js, imgs = glb_parts(data)
        want_imgs = sorted((TEX / t).read_bytes() for t in drawn)
        # GLTFExporter (r160 processBufferViewImage) pads each image's bufferView to 4 bytes, the padding in its byteLength:
        # what follows the PNG's own bytes must be that padding alone (fewer than 4 zero bytes)
        unpad = lambda i: next((i[:len(w)] for w in want_imgs if i[:len(w)] == w and len(i) - len(w) < 4 and not any(i[len(w):])), i)
        pad = [len(i) - len(unpad(i)) for _, i in imgs]
        imgs = [(mt, unpad(i)) for mt, i in imgs]
        got = await page.evaluate(LOAD_GLB, base64.b64encode(data).decode())
        bones_ok = (len(got["skins"]) == len(skins) and all(s["tree"] and all(s["maps"]) for s in got["skins"])
                    and sorted(s["bones"] for s in got["skins"]) == sorted(skins))
        check(fn == stem + ".glb" and js is not None and bones_ok and len(got["meshes"]) == meshes and all(all(e["maps"]) for e in got["meshes"])
              and all(mt == "image/png" for mt, _ in imgs) and sorted(i for _, i in imgs) == want_imgs,
              f"{cls:6} {name:14} ดาวน์โหลดโมเดล 3D: {fn} (want {stem}.glb), {len(data)} bytes; GLTFLoader: "
              f"{len(got['skins'])} skinned (want {len(skins)}) on {[len(s['bones']) for s in got['skins']]} bones (want {[len(s) for s in skins]}, "
              f"names {'equal' if bones_ok else [s['bones'][:4] for s in got['skins']]}), {len(got['meshes'])} plain meshes (want {meshes}); "
              f"{len(imgs)} images embedded, byte-equal to the data's {drawn}: {sorted(i for _, i in imgs) == want_imgs} "
              f"(+ {pad} zero bytes of the exporter's 4-byte padding)")

    # ---- a picture pasted or dropped on the pet: a pet takes no skin (not in v1); then ถอด, one undo step
    pt = await wear(page, "sheep", "smallAnubi")
    if pt:
        await page.mouse.move(*pt)
        await page.wait_for_timeout(200)
        for how in ("paste", "drop"):
            r = await page.evaluate(PICTURE, [how, *pt])
            check(r["skins"] == 0 and not r["menu"] and r["toast"] == "สัตว์เลี้ยงใส่ลายเองไม่ได้",
                  f"sheep  smallAnubi     a picture {how}{'d' if how == 'paste' else 'ped'} on the pet: skins {r['skins']}, menu open {r['menu']}, toast {r['toast']!r}")
    # the ring's menu (a right-click on the topic): เปลี่ยนสัตว์เลี้ยง opens the สัตว์เลี้ยง picker
    ring = page.locator('#topics button.topic[data-t="Pet"]')
    if await ring.count():
        await ring.click(button="right")
        await page.wait_for_timeout(250)
        m = await page.evaluate(PMENU)
        has = await page.locator('#pmenu .pm-item[data-a="change"]').count()
        if has:
            await page.click('#pmenu .pm-item[data-a="change"]')
            try:
                await page.wait_for_function("() => !document.getElementById('picker').hidden && document.getElementById('pkBody').dataset.topic === 'Pet'"
                                             " && document.querySelector('#pkBody .pk-cell[data-slot=\"Pet\"]')", timeout=15000)
            except Exception:
                pass
        pk = await page.evaluate("() => ({ open: !document.getElementById('picker').hidden, topic: document.getElementById('pkBody').dataset.topic, "
                                 "title: document.getElementById('pkTitle').textContent })")
        check(m["open"] and m["from"] == "ring" and has and pk["open"] and pk["topic"] == "Pet" and pk["title"] == "สัตว์เลี้ยง",
              f"sheep  smallAnubi     the ring's menu {[i['a'] for i in m['items']]}: เปลี่ยนสัตว์เลี้ยง opens the picker {pk}")
        await page.evaluate("() => { if (!document.getElementById('picker').hidden) document.getElementById('pkClose').click(); }")
    else:
        check(False, "sheep  smallAnubi     no สัตว์เลี้ยง topic (its ring's เปลี่ยนสัตว์เลี้ยง)")
    m = await menu(page, "smallAnubi", "sheep  smallAnubi     (for ถอด)", pt)
    if m and await page.locator('#pmenu .pm-item[data-a="remove"]').count():
        await page.click('#pmenu .pm-item[data-a="remove"]')
        try:
            await page.wait_for_function("() => { const { C, scene } = wardrobe.debug(); let n = 0; scene.traverse(x => { if (x.userData.pet) n++; });"
                                         " return C.state.Pet === null && !C.props.Pet && !n; }", timeout=15000)
            off = True
        except Exception:
            off = False
        await page.keyboard.press("Control+z")
        try:
            await page.wait_for_function("() => wardrobe.debug().C.props.Pet?.userData.pet === 'smallAnubi'", timeout=15000)
            back = True
        except Exception:
            back = False
        check(off and back, f"sheep  smallAnubi     ถอดสัตว์เลี้ยงออก: the pet off {off}, Ctrl+Z puts it back {back}")
    else:
        check(False, "sheep  smallAnubi     no ถอดสัตว์เลี้ยงออก item")
    await page.close()

    # ---- ?ttolock (the online rule; Review Focus 5): the TTO pet preview only, a BB pet keeps both downloads
    page = await page_at("?ttolock")
    # a tile's menu before the pet's file is in (Task 8's review): still TTO, so no download item
    await tile_menu(page, "smallDragonZ", ["wear"], "sheep  smallDragonZ   tile ?ttolock")
    for cls, name, locked in (("sheep", "smallDragonZ", True), ("sheep", "smallAnubi", False)):
        pt = await wear(page, cls, name)
        m = await menu(page, name, f"{cls:6} {name:14} ?ttolock", pt)
        if m:
            items_ok(m, name, cls, locked, "?ttolock ")
            await page.keyboard.press("Escape")
    await page.close()
    await ctx.close()


# ---- the สัตว์เลี้ยง topic, its picker and the camera (Task 7)
NICK = json.loads((ROOT / "wardrobe" / "data" / "nicknames.json").read_text(encoding="utf-8"))
# (a run given its own out folder, e.g. a mutation trial, shoots into <out>/pet_ui, never over checks/pet_ui/)
UI_OUT = OUT / "pet_ui" if len(ARGS) > 1 else ROOT / "checks" / "pet_ui"


def unit(*v):
    n = math.sqrt(sum(x * x for x in v))
    return [x / n for x in v]


FIT_DIR = unit(.48, .1, 2.55)                                                  # today's front view
FIT_DIR_PET = unit(math.sin(math.radians(40)), .10, math.cos(math.radians(40)))   # the pick: turn 40 deg, rise .10, x positive


def humanize(n):                # the page's humanize (nameParts): hallowSaw_r -> "Hallow Saw", all57 -> "All แบบ 57"
    s, num, ed = re.sub(r"_[LRlr]$", "", n), "", ""
    m = re.match(r"^(.*[A-Za-z])(\d+)$", s)
    if m:
        s, num = m.group(1), m.group(2)
    m = re.match(r"^(.*[a-z0-9])([RV])$", s)
    if m:
        s, ed = m.group(1), m.group(2)
    w = re.sub(r"[_-]+", " ", s)
    w = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", w)
    w = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", w)
    w = re.sub(r"([A-Za-z])(\d)", r"\1 \2", w)
    words = [x[0].upper() + x[1:] for x in w.strip().split()]
    return " ".join(words) + (f" แบบ {num}" if num else "") + (" " + ed if ed else "")


def pet_nick(cls, name):        # the page's nickOf("pets", name): the class's table, else the shared one by lower-case name
    t = NICK.get(cls, {}).get("pets", {})
    return t.get(name) or t.get(re.sub(r"_[LRlr]$", "", name)) or NICK.get("all", {}).get("pets", {}).get(name.lower()) or {}


def squash(s):
    return re.sub(r"\s+", "", s or "").lower()


def pet_text(cls, name):        # what the ค้นหา box searches: the name, as words, the game's name, the nickname and its game names
    r, nk = ROWS[name], pet_nick(cls, name)
    return squash(" ".join(p for p in [name, humanize(name), r["game"], nk.get("nick"), *(nk.get("game") or [])] if p))


def pet_order(cls):             # nicknamed first (the class guide's order: no level, rank-gated, level), else the index's order
    key = lambda r: (1, 0, 0) if not r.get("nick") else (0, 0, 0) if "lv" not in r else (0, 1, r["lv"]) if r["lv"] < 0 else (0, 2, -r["lv"])
    return [n for _, n in sorted(enumerate(ROWS), key=lambda e: (key(pet_nick(cls, e[1])), e[0]))]


TOPIC_BOXES = """() => Object.fromEntries([...document.querySelectorAll('#topics button.topic')].map(b => { const r = b.getBoundingClientRect(),
  g = b.querySelector('.ring')?.getBoundingClientRect(); return [b.dataset.t, { x: r.left, y: r.top, w: r.width, h: r.height, ring: g ? g.width : 0,
  name: b.querySelector('.tname')?.textContent ?? null }]; }))"""
RING = """() => { const r = document.querySelector('#topics [data-t="Pet"] .ring');
  return r && { img: r.querySelector('img')?.getAttribute('src') ?? null, glyph: !!r.querySelector('.slot-glyph') }; }"""
PK_TILES = """() => [...document.querySelectorAll('#pkBody .pk-item')].map(b => ({ p: b.dataset.p ?? null, slot: b.closest('.pk-cell')?.dataset.slot ?? null,
  item: b.closest('.pk-cell')?.dataset.item ?? null, lbl: b.querySelector('.lbl')?.textContent ?? null, main: b.querySelector('.nk-main')?.textContent ?? null,
  sub: b.querySelector('.nk-sub')?.textContent ?? null, img: b.querySelector('.pic img')?.getAttribute('src') ?? null,
  glyph: !!b.querySelector('.pic .slot-glyph'), tto: !!b.querySelector('.tto-mark'), pressed: b.getAttribute('aria-pressed') === 'true' }))"""
# the page's visibleBox (what is drawn, skinned vertices where their bones put them)
VBOX = """const vbox = root => { const box = new THREE.Box3(), v = new THREE.Vector3(); root.updateMatrixWorld(true);
  root.traverseVisible(m => { if (!m.isMesh) return; const n = m.geometry.attributes.position.count;
    for (let i = 0; i < n; i++) box.expandByPoint(m.getVertexPosition(i, v).applyMatrix4(m.matrixWorld)); }); return box; };"""
# the camera, read in one task (the idle moves the hero between two evaluates): the page's fit (heroFitPose); today's fit
# (before the pet camera, 9d8244c) recomputed here apart from the page, so the no-pet framing must not move; the live
# camera; the hero's and the pet's box corners through the live camera (its view offset too) against the part of the
# stage the visitor sees: right of the desktop picker, under the toolbar's band, over the stage's foot (the fit's margins)
CAM = """() => { const { C, THREE, camera, controls, renderer, heroFitPose } = wardrobe.debug(), stage = document.getElementById('stage'), vw = stage.clientWidth, vh = stage.clientHeight;
  """ + VBOX + """
  const todayFit = () => {
    C.mixer.update(0); C.root.updateMatrixWorld(true);
    const body = new THREE.Box3();
    for (const m of C.meshes) body.union(vbox(m));
    if (body.isEmpty()) body.setFromCenterAndSize(new THREE.Vector3(0, .5, 0), new THREE.Vector3(.5, 1, .5));
    const h0 = Math.max(body.max.y - body.min.y, 0.5), box = body.clone();
    for (const [k, o] of Object.entries(C.props)) if (k !== 'Pet') box.union(vbox(o));
    box.intersect(new THREE.Box3(body.min.clone().add(new THREE.Vector3(-h0 * .4, -h0 * .05, -h0 * .4)), body.max.clone().add(new THREE.Vector3(h0 * .4, h0 * .65, h0 * .4))));
    const c = box.getCenter(new THREE.Vector3()), h = Math.max(box.max.y - box.min.y, 0.5), target = new THREE.Vector3(c.x, c.y - h * .01, c.z);
    const t = Math.tan(camera.fov * Math.PI / 360), dir = new THREE.Vector3(.48, .1, 2.55).normalize();
    let d = Math.max(h / (2 * t * .78), (box.max.x - box.min.x) / (2 * t * camera.aspect * .85));
    const cam = camera.clone(); cam.clearViewOffset(); cam.updateProjectionMatrix();
    const bar = document.querySelector('.bar').getBoundingClientRect().bottom - stage.getBoundingClientRect().top;
    const top = Math.max(64, bar + 8), foot = vh - 12, dy = matchMedia('(max-width: 760px)').matches ? 22 : 0, v = new THREE.Vector3();
    const pts = [];
    for (const x of [box.min.x, box.max.x]) for (const y of [box.min.y, box.max.y]) for (const z of [box.min.z, box.max.z]) pts.push(new THREE.Vector3(x, y, z));
    pts.push(new THREE.Vector3(c.x, 0, c.z + h0 * .26));
    const fits = dd => { cam.position.copy(target).addScaledVector(dir, dd); cam.lookAt(target); cam.updateMatrixWorld();
      return pts.every(p => { v.copy(p).project(cam); const y = (1 - v.y) / 2 * vh + dy, x = (v.x + 1) / 2 * vw; return y >= top && y <= foot && x >= 6 && x <= vw - 6; }); };
    if (!fits(d)) { let lo = d, hi = d * 1.25; for (let i = 0; i < 12 && !fits(hi); i++) { lo = hi; hi *= 1.25; }
      for (let i = 0; i < 20; i++) { const m = (lo + hi) / 2; if (fits(m)) hi = m; else lo = m; } d = hi; }
    return { pos: target.clone().addScaledVector(dir, d).toArray(), target: target.toArray(), h };
  };
  const corners = () => {
    C.mixer.update(0); C.props.Pet?.userData.mixer?.update(0);
    const body = new THREE.Box3(), o = C.props.Pet; for (const m of C.meshes) body.union(vbox(m));
    const r = renderer.domElement.getBoundingClientRect(), bar = document.querySelector('.bar').getBoundingClientRect().bottom;
    const pk = document.getElementById('picker'), phone = matchMedia('(max-width: 760px)').matches;
    const left = !pk.hidden && !phone ? pk.getBoundingClientRect().right : r.left;
    const lim = { x0: left + 6, x1: r.right - 6, y0: r.top + Math.max(64, bar - r.top + 8), y1: r.bottom - 12 };
    camera.updateMatrixWorld();
    const proj = b => { const out = [], v = new THREE.Vector3(); for (let i = 0; i < 8; i++) {
      v.set(i & 1 ? b.max.x : b.min.x, i & 2 ? b.max.y : b.min.y, i & 4 ? b.max.z : b.min.z).project(camera);
      out.push([r.left + (v.x + 1) / 2 * r.width, r.top + (1 - v.y) / 2 * r.height]); } return out; };
    return { lim, pet: o ? proj(vbox(o)) : null, hero: proj(body) };
  };
  const f = heroFitPose?.();
  return { fit: f ? { pos: f.pos.toArray(), target: f.target.toArray(), h: f.h } : null, today: todayFit(),
    live: { pos: camera.position.toArray(), target: controls.target.toArray() }, cs: corners() }; }"""
# the camera's positions frame by frame from now until it has stood still for 30 frames (or 4 s): a glide, a jump or no move
GLIDE = """() => { window.__glide = new Promise(res => { const { camera } = wardrobe.debug(), seen = [camera.position.toArray()], t0 = performance.now(); let still = 0;
  const f = () => { const p = camera.position.toArray(), l = seen[seen.length - 1];
    if (Math.hypot(p[0] - l[0], p[1] - l[1], p[2] - l[2]) > 1e-7) { seen.push(p); still = 0; } else still++;
    if ((seen.length > 1 && still > 30) || performance.now() - t0 > 4000) res(seen); else requestAnimationFrame(f); };
  requestAnimationFrame(f); }); }"""
# what the stage shows, frame by frame over the pet's idle: the frame now (held), then 16 more of its clip (between the
# page's own 24 samples), each rendered through the live camera; per frame the drawn pixels (the canvas is transparent
# where nothing is drawn; alpha >= 128: the models, not the soft shadows), those under the desktop picker, on the edge
# rows / columns or behind the toolbar, and the pet's box projected; the clip put back where it was
IDLE = """() => { const { C, THREE, camera, renderer, scene } = wardrobe.debug(), o = C.props.Pet, pa = o?.userData.propAnim;
  """ + VBOX + """
  const cv = renderer.domElement, r = cv.getBoundingClientRect(), W = Math.round(r.width), H = Math.round(r.height);
  const pk = document.getElementById('picker'), phone = matchMedia('(max-width: 760px)').matches;
  const freeL = !pk.hidden && !phone ? Math.max(0, Math.round(pk.getBoundingClientRect().right - r.left)) : 0;
  const q = document.querySelector('.bar').getBoundingClientRect(), bar = { x0: q.left - r.left, x1: q.right - r.left, y0: q.top - r.top, y1: q.bottom - r.top };
  const lim = { x0: freeL + 6, x1: W - 6, y0: Math.max(64, bar.y1 + 8), y1: H - 12 };
  const g = new OffscreenCanvas(W, H).getContext('2d', { willReadFrequently: true });
  let clear = null;
  const frame = () => {
    renderer.render(scene, camera); g.clearRect(0, 0, W, H); g.drawImage(cv, 0, 0, W, H);
    const d = g.getImageData(0, 0, W, H).data; let x0 = W, x1 = -1, y0 = H, y1 = -1, bad = 0;
    if (clear === null) clear = d[3];
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) { if (d[(y * W + x) * 4 + 3] < 128) continue;
      if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y;
      if (x < freeL || x >= W - 1 || y <= 0 || y >= H - 1 || (x >= bar.x0 && x < bar.x1 && y >= bar.y0 && y < bar.y1)) bad++; }
    camera.updateMatrixWorld();
    const b = vbox(o), v = new THREE.Vector3(); let bx0 = 1e9, bx1 = -1e9, by0 = 1e9, by1 = -1e9;
    for (let i = 0; i < 8; i++) { v.set(i & 1 ? b.max.x : b.min.x, i & 2 ? b.max.y : b.min.y, i & 4 ? b.max.z : b.min.z).project(camera);
      const x = (v.x + 1) / 2 * W, y = (1 - v.y) / 2 * H; bx0 = Math.min(bx0, x); bx1 = Math.max(bx1, x); by0 = Math.min(by0, y); by1 = Math.max(by1, y); }
    return { ink: [x0, x1, y0, y1], bad, box: [bx0, bx1, by0, by1] };
  };
  const now = frame(), t0 = pa ? pa.act.time : null, frames = [];
  if (pa) { const dur = pa.act.getClip().duration, n = 16;
    for (let i = 0; i < n; i++) { pa.act.time = dur * (i + .5) / n; pa.mixer.update(0); frames.push(frame()); }
    pa.act.time = t0; pa.mixer.update(0); renderer.render(scene, camera); }
  return { W, H, freeL, lim, clear, now, frames, t: [t0, pa ? pa.act.time : null], clip: pa ? pa.act.getClip().duration : 0 }; }"""
# the hero's and the pet's mixers' times (held: unchanged through a screenshot)
TIMES = "() => { const { C } = wardrobe.debug(); return [C.mixer.time, C.props.Pet?.userData.mixer?.time ?? null]; }"
# a block's label ink in a 2x screenshot (decoded in the page): the first and last rows with a pixel clearly lighter (or
# darker) than the block's own background (its first rows, the weave's light and dark), in the label's columns, against the
# block's inner edges (inside its border), in device px
INK = """async ([b64, lab, box]) => { const im = new Image(); im.src = 'data:image/png;base64,' + b64; await im.decode();
  const c = new OffscreenCanvas(im.width, im.height), g = c.getContext('2d'); g.drawImage(im, 0, 0);
  const d = g.getImageData(0, 0, im.width, im.height).data, px = (x, y) => { const i = (y * im.width + x) * 4; return d[i] + d[i + 1] + d[i + 2]; };
  const x0 = Math.max(0, Math.floor(lab.x0)), x1 = Math.min(im.width, Math.ceil(lab.x1)), y0 = Math.ceil(box.y0), y1 = Math.floor(box.y1);
  let lo = Infinity, hi = -Infinity; for (let y = y0; y < y0 + 4; y++) for (let x = x0; x < x1; x++) { lo = Math.min(lo, px(x, y)); hi = Math.max(hi, px(x, y)); }
  let top = -1, bot = -1;
  for (let y = y0; y < y1; y++) for (let x = x0; x < x1; x++) if (px(x, y) > hi + 100 || px(x, y) < lo - 100) { if (top < 0) top = y; bot = y; break; }
  return { top, bot, above: top - y0, below: y1 - 1 - bot }; }"""
# a topic block's label: its columns, and the box its ink is measured in (the block inside its border; on a desktop the
# label is a title over the ring: down to the ring's top)
LABEL_GEOM = """t => { const b = document.querySelector(`#topics button.topic[data-t="${t}"]`), n = b.querySelector('.tname'), r = b.getBoundingClientRect(), cs = getComputedStyle(b);
  const g = document.createRange(); g.selectNodeContents(n); const q = g.getBoundingClientRect(), k = b.querySelector('.ring').getBoundingClientRect();
  const under = k.left < q.right && k.right > q.left, y1 = under ? k.top - r.top : r.height - parseFloat(cs.borderBottomWidth);
  return { box: { y0: parseFloat(cs.borderTopWidth), y1 }, lab: { x0: q.left - r.left, x1: q.right - r.left }, y: q.top, x: q.left }; }"""


async def ui(b, check, errors):
    """the สัตว์เลี้ยง topic, its picker and the camera: desktop 1600x1000 and phone 390x700, the layout at 1600x1200 too"""
    UI_OUT.mkdir(parents=True, exist_ok=True)
    near_v = lambda a, c, tol: a is not None and c is not None and all(abs(x - y) <= tol for x, y in zip(a, c))
    dir_of = lambda f: unit(*[p - q for p, q in zip(f["pos"], f["target"])]) if f else None
    fmt = lambda v: [round(x, 4) for x in v] if v else v

    for vw, vh, tag in ((1600, 1000, "desktop"), (390, 700, "phone"), (1600, 1200, "tall")):
        ctx = await b.new_context(viewport={"width": vw, "height": vh}, device_scale_factor=2)
        page = await ctx.new_page()
        page.on("pageerror", lambda e, tag=tag: errors.append(f"ui {tag}: {e}"))
        page.on("console", lambda m, tag=tag: m.type == "error" and errors.append(f"ui {tag}: {m.text} {(m.location or {}).get('url', '')}"))
        page.on("requestfailed", lambda r, tag=tag: errors.append(f"ui {tag}: request failed {r.url} {r.failure}"))
        await page.goto(URL)
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C && wardrobe.debug().C.cls === 'sheep'", timeout=120000)
        await page.evaluate("() => document.fonts.ready")
        await page.wait_for_timeout(800)
        T = f"{tag:7}"

        # ---- the block: two by two (หมวก + ชุด, อาวุธ + ประดับ, สัตว์เลี้ยง + ท่าทาง), the name, the ring
        tb = await page.evaluate(TOPIC_BOXES)
        pet = tb.get("Pet")
        same = lambda a, c, k, tol=.6: abs(tb[a][k] - tb[c][k]) <= tol
        grid = bool(pet) and all(same(a, c, "y") for a, c in (("Head", "outfit"), ("R", "Back"), ("Pet", "move"))) \
            and all(same(a, c, "x") for a, c in (("Head", "R"), ("R", "Pet"), ("outfit", "Back"), ("Back", "move"))) \
            and tb["Head"]["y"] < tb["R"]["y"] < tb["Pet"]["y"] and tb["Pet"]["x"] < tb["move"]["x"] \
            and all(same("Head", k, "w") and same("Head", k, "h") and same("Head", k, "ring") for k in ("outfit", "R", "Back", "Pet", "move"))
        check(grid and pet["name"] == "สัตว์เลี้ยง",
              f"{T} blocks two by two, สัตว์เลี้ยง beside ท่าทาง: " + ", ".join(f"{k} {fmt([v['x'], v['y'], v['w'], v['h']])} ring {round(v['ring'], 1)}"
                                                                         for k, v in tb.items() if k in ("Head", "outfit", "R", "Back", "Pet", "move")))
        if tag == "tall":
            await page.screenshot(path=str(UI_OUT / f"panel_{tag}.png"))
            await ctx.close()
            continue
        if not pet:
            await ctx.close()
            continue
        rg = await page.evaluate(RING)
        check(rg and rg["glyph"] and not rg["img"], f"{T} no pet: the ring shows the slot's outline {rg}")
        await page.locator("aside").screenshot(path=str(UI_OUT / f"panel_{tag}_none.png"))

        # ---- the label: no mark clipped, and on a phone its ink centred by eye in its block (NOTES.md "Thai text: centring
        # by eye"); every label's ink printed (the other topics' labels must not move)
        labels = {}
        for t in ("Head", "outfit", "R", "Back", "Pet", "move"):
            geo = await page.evaluate(LABEL_GEOM, t)
            blk = page.locator(f'#topics button.topic[data-t="{t}"]')
            s2 = lambda v: {k: x * 2 for k, x in v.items()}
            ink = await page.evaluate(INK, [base64.b64encode(await blk.screenshot()).decode(), s2(geo["lab"]), s2(geo["box"])])
            await page.add_style_tag(content=f'#topics button.topic[data-t="{t}"] .tname {{ overflow: visible !important; }}')
            free = await page.evaluate(INK, [base64.b64encode(await blk.screenshot()).decode(), s2(geo["lab"]), s2(geo["box"])])
            await page.evaluate("() => document.head.lastElementChild.remove()")
            labels[t] = (ink, free, geo)
            check(ink["top"] == free["top"] and ink["bot"] == free["bot"],
                  f"{T} {t:6} label ink rows {ink['top']}-{ink['bot']} (unclipped {free['top']}-{free['bot']}), above {ink['above']} / below {ink['below']} "
                  f"device px; label at x {round(geo['x'], 2)} y {round(geo['y'], 2)}")
        if tag == "phone":
            ink = labels["Pet"][0]
            check(abs(ink["above"] - ink["below"]) <= 2, f"{T} สัตว์เลี้ยง centred by eye: {ink['above']} px above the ink, {ink['below']} below (2x)")
            await page.locator('#topics button.topic[data-t="Pet"]').screenshot(path=str(UI_OUT / "label_phone_pet.png"))

        # ---- the camera with no pet: today's front view, exactly. The idle held from here (Space, as a visitor holds it):
        # the page's fit read now is then the one the camera glided to (a pet's idle can swing its box by a lot)
        async def hold():
            if await page.evaluate("() => document.getElementById('khPause').textContent !== 'เล่นต่อ'"):
                await page.evaluate("() => document.activeElement?.blur()")
                await page.keyboard.press("Space")
            return await page.evaluate("() => document.getElementById('khPause').textContent === 'เล่นต่อ'")
        check(await hold(), f"{T} the idle held (Space)")

        async def shot(fn):                      # a stage screenshot of the held moment (the mixers' times the same after)
            t0 = await page.evaluate(TIMES)
            await page.screenshot(path=str(UI_OUT / fn))
            t1 = await page.evaluate(TIMES)
            check(t0 == t1, f"{T} {fn}: the hero and the pet held through the shot (mixer times {t0} -> {t1})")

        async def idle_framed(what):             # the frame shown and 16 more of the pet's idle: all of it on the free stage
            r = await page.evaluate(IDLE)
            fr, lim = [r["now"]] + r["frames"], r["lim"]
            out = [i for i, f in enumerate(fr) if not (lim["x0"] - 3 <= f["box"][0] and f["box"][1] <= lim["x1"] + 3
                                                         and lim["y0"] - 3 <= f["box"][2] and f["box"][3] <= lim["y1"] + 3)]
            bad = [f["bad"] for f in fr]
            ink = [min(f["ink"][0] for f in fr), max(f["ink"][1] for f in fr), min(f["ink"][2] for f in fr), max(f["ink"][3] for f in fr)]
            bx = [min(f["box"][0] for f in fr), max(f["box"][1] for f in fr), min(f["box"][2] for f in fr), max(f["box"][3] for f in fr)]
            check(r["clear"] == 0 and len(r["frames"]) == 16 and not any(bad) and not out and r["t"][0] == r["t"][1],
                  f"{T} {what}: over the idle ({len(fr)} frames of a {r['clip']:.2f} s clip, put back {r['t'][0] == r['t'][1]}): "
                  f"drawn x {ink[0]}-{ink[1]}, y {ink[2]}-{ink[3]} of the {r['W']}x{r['H']} stage (free from x {r['freeL']}), "
                  f"pixels off the free stage {sum(bad)}; the pet's box x {round(bx[0])}-{round(bx[1])}, y {round(bx[2])}-{round(bx[3])} "
                  f"in x {round(lim['x0'])}-{round(lim['x1'])}, y {round(lim['y0'])}-{round(lim['y1'])}"
                  + (f"; frames outside {out}" if out else "") + ("" if r["clear"] == 0 else f"; the canvas is not clear ({r['clear']})"))
        cam = await page.evaluate(CAM)
        fit, today, live = cam["fit"], cam["today"], cam["live"]
        check(fit is not None and near_v(fit["pos"], today["pos"], 1e-9) and near_v(fit["target"], today["target"], 1e-9)
              and near_v(dir_of(fit), FIT_DIR, 1e-9) and near_v(live["pos"], today["pos"], today["h"] * .01),
              f"{T} no pet: heroFitPose {fmt(fit and fit['pos'])} -> {fmt(fit and fit['target'])} = today's {fmt(today['pos'])} -> {fmt(today['target'])}, "
              f"direction {fmt(dir_of(fit))} (FIT_DIR {fmt(FIT_DIR)}), the camera there {fmt(live['pos'])}")

        # ---- the picker: ไม่ใส่ + one tile per row, nicknamed first, the search
        await page.click('#topics button.topic[data-t="Pet"]')
        try:
            await page.wait_for_selector('#pkBody .pk-cell[data-slot="Pet"]', timeout=15000)
        except Exception:
            check(False, f"{T} the สัตว์เลี้ยง picker shows no pet tile")
            await ctx.close()
            continue
        await page.wait_for_timeout(900)                         # the icons in
        head = await page.evaluate("() => ({ title: document.getElementById('pkTitle').textContent, box: document.querySelector('#pkTools input[type=search]')?.placeholder ?? null, topic: document.getElementById('pkBody').dataset.topic })")
        tiles = await page.evaluate(PK_TILES)
        order = pet_order("sheep")
        none = tiles[0] if tiles else {}
        check(head == {"title": "สัตว์เลี้ยง", "box": "ค้นหา", "topic": "Pet"} and none.get("p") == "" and none.get("lbl") == "ไม่ใส่" and none.get("pressed")
              and none.get("glyph") and none.get("slot") is None,
              f"{T} the picker {head}: first tile {none}")
        got = [x["p"] for x in tiles[1:]]
        check(got == order and all(x["slot"] == "Pet" and x["item"] == x["p"] for x in tiles[1:]),
              f"{T} one tile per row ({len(got)} of {len(order)}), nicknamed first: {got[:12]} ... (want {order[:12]} ...)")
        bad = []
        for x in tiles[1:]:
            r, nk = ROWS[x["p"]], pet_nick("sheep", x["p"])
            name = r["game"] or humanize(x["p"])
            shown = x["sub"] if x["main"] is not None else x["lbl"]
            if not (x["img"] or "").endswith(r["icon"]) or shown != name or (x["main"] or None) != nk.get("nick") or x["tto"] != bool(r["tto"]) or x["pressed"]:
                bad.append(f"{x['p']}: icon {x['img']} name {shown!r} nick {x['main']!r} tto {x['tto']} pressed {x['pressed']}")
        check(not bad, f"{T} each tile: the row's icon, the game's name (else the name as words), its nickname over it, TTO's mark on TTO's own: "
                       f"{len(tiles) - 1 - len(bad)} right" + (f", wrong: {bad[:4]}" if bad else ""))
        await page.locator("#picker").screenshot(path=str(UI_OUT / f"picker_{tag}.png"))
        for q in ("Anubi", "L. Carron", "ALL 9", "all9", "zzqq"):
            await page.fill("#pkTools input[type=search]", q)
            await page.wait_for_timeout(120)
            ts = await page.evaluate(PK_TILES)
            note = await page.evaluate("() => [...document.querySelectorAll('#pkBody .pk-note')].map(n => n.textContent).join(' ')")
            want = [n for n in order if squash(q) in pet_text("sheep", n)]
            sane = {"Anubi": ["smallAnubi"], "ALL 9": ["littleBDMellon"], "all9": ["littleBDMellon"], "zzqq": []}.get(q, want)
            check([x["p"] for x in ts[1:]] == want == sane and ts[0]["p"] == "" and (("ไม่พบที่ค้นหา" in note) == (not want)),
                  f"{T} ค้นหา {q!r}: {[x['p'] for x in ts[1:]]} (want {want}){' ' + note if note else ''}")
            if q == "L. Carron":
                check(want and all(squash(q) not in squash(n + " " + humanize(n)) for n in want), f"{T}   (found by the game's name alone: {want})")
        await page.fill("#pkTools input[type=search]", "")
        await page.wait_for_timeout(120)

        # ---- a pick: one undo step, the picker open, the ring's icon; the camera glides to the pet's view
        async def pick(name, glide=True):
            if glide:
                await page.evaluate(GLIDE)
            sel = f'#pkBody .pk-item[data-p="{name}"]' if name else '#pkBody .pk-item[data-p=""]'
            await page.click(sel)
            await page.wait_for_function("n => { const { C } = wardrobe.debug(); return (C.state.Pet ?? null) === n && (C.props.Pet?.userData.pet ?? null) === n; }",
                                         arg=name, timeout=30000)
            return await page.evaluate("() => window.__glide") if glide else None

        async def framed(what, want_dir):           # the camera at the page's fit, in the direction wanted, every corner seen
            await page.wait_for_timeout(250)
            cam = await page.evaluate(CAM)
            fit, live, cs = cam["fit"], cam["live"], cam["cs"]
            lim, pts = cs["lim"], (cs["pet"] or []) + cs["hero"]
            out = [p for p in pts if not (lim["x0"] - 3 <= p[0] <= lim["x1"] + 3 and lim["y0"] - 3 <= p[1] <= lim["y1"] + 3)]
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            ok = (fit is not None and near_v(live["pos"], fit["pos"], 1e-5) and near_v(live["target"], fit["target"], 1e-5)
                  and near_v(dir_of(live), want_dir, 1e-6) and cs["pet"] is not None and not out)
            check(ok, f"{T} {what}: the camera {fmt(live['pos'])} -> {fmt(live['target'])} (the fit {fmt(fit and fit['pos'])}), "
                      f"direction {fmt(dir_of(live))} (want {fmt(want_dir)}); hero + pet corners x {round(min(xs))}-{round(max(xs))}, "
                      f"y {round(min(ys))}-{round(max(ys))} in x {round(lim['x0'])}-{round(lim['x1'])}, y {round(lim['y0'])}-{round(lim['y1'])}"
                      + (f"; outside: {[fmt(p) for p in out]}" if out else ""))

        u0 = await page.evaluate("() => !document.getElementById('undo').disabled")
        seen = await pick("smallAnubi")
        ts = await page.evaluate(PK_TILES)
        pressed = [x["p"] for x in ts if x["pressed"]]
        st = await page.evaluate("() => ({ open: !document.getElementById('picker').hidden, undo: !document.getElementById('undo').disabled })")
        rg = await page.evaluate(RING)
        check(not u0 and st["open"] and st["undo"] and pressed == ["smallAnubi"] and rg and (rg["img"] or "").endswith(ROWS["smallAnubi"]["icon"]),
              f"{T} pick smallAnubi: the picker open {st['open']}, an undo step {st['undo']} (none before: {not u0}), pressed {pressed}, the ring {rg}")
        check(len(seen) >= 4, f"{T} the camera glides there: {len(seen)} positions over the move")
        await framed("smallAnubi (Lv 9, 1 m back)", FIT_DIR_PET)
        await shot(f"stage_{tag}_smallAnubi.png")
        if tag == "desktop":                                     # (a phone's panel hides under the sheet: at the end)
            await page.locator("aside").screenshot(path=str(UI_OUT / f"panel_{tag}_smallAnubi.png"))
        await page.locator("#picker").screenshot(path=str(UI_OUT / f"picker_{tag}_smallAnubi.png"))
        # undo / redo (the camera follows each)
        await page.click("#undo")
        await page.wait_for_function("() => !wardrobe.debug().C.props.Pet && wardrobe.debug().C.state.Pet == null", timeout=15000)
        await page.wait_for_timeout(900)
        cam = await page.evaluate(CAM)
        live, today = cam["live"], cam["today"]
        check(near_v(live["pos"], today["pos"], today["h"] * .01) and near_v(dir_of(live), FIT_DIR, 1e-6)
              and await page.evaluate("() => document.getElementById('undo').disabled"),
              f"{T} undo: no pet, nothing more to undo, the camera back at today's view {fmt(live['pos'])} (today {fmt(today['pos'])})")
        await page.click("#redo")
        await page.wait_for_function("() => wardrobe.debug().C.props.Pet?.userData.pet === 'smallAnubi'", timeout=15000)
        await page.wait_for_timeout(900)
        await framed("redo: smallAnubi again", FIT_DIR_PET)

        # the visitor moves the camera: a pick leaves it there; the reset button fits the pet's view
        cv = await page.evaluate("() => { const r = wardrobe.debug().renderer.domElement.getBoundingClientRect(), p = document.getElementById('picker');"
                                 " const l = !p.hidden && innerWidth > 760 ? p.getBoundingClientRect().right : r.left; return [(l + r.right) / 2, r.top + r.height * .6]; }")
        before = (await page.evaluate(CAM))["live"]
        await page.mouse.move(*cv)
        await page.mouse.wheel(0, -240)                          # the visitor zooms in (a drag would coast on: the damping)
        await page.wait_for_timeout(600)
        moved = (await page.evaluate(CAM))["live"]
        check(not near_v(moved["pos"], before["pos"], 1e-3), f"{T} the wheel moved the camera: {fmt(before['pos'])} -> {fmt(moved['pos'])}")
        await pick("miniMokBug", glide=False)
        await page.wait_for_timeout(900)
        after = (await page.evaluate(CAM))["live"]
        check(near_v(after["pos"], moved["pos"], 1e-6) and near_v(after["target"], moved["target"], 1e-6),
              f"{T} the visitor moved the camera: a pick leaves it at {fmt(after['pos'])} (was {fmt(moved['pos'])})")
        await page.evaluate(GLIDE)
        await page.click("#resetCam")
        await page.evaluate("() => window.__glide")
        await framed("miniMokBug (2 m back), after the reset button", FIT_DIR_PET)
        await shot(f"stage_{tag}_miniMokBug.png")
        await pick("kiteChula")
        await framed("kiteChula (a kite over her)", FIT_DIR_PET)
        await shot(f"stage_{tag}_kiteChula.png")
        if tag == "desktop":                                     # the picker's width leaves the stage, then takes it again
            await page.evaluate(GLIDE)
            await page.click("#pkClose")
            await page.evaluate("() => window.__glide")
            await page.evaluate(GLIDE)
            await page.click("#resetCam")                        # (the fit made with the whole stage free)
            await page.evaluate("() => window.__glide")
            await framed("kiteChula, the picker closed", FIT_DIR_PET)
            await page.evaluate(GLIDE)
            await page.click('#topics button.topic[data-t="Pet"]')
            await page.evaluate("() => window.__glide")
            await page.wait_for_selector('#pkBody .pk-cell[data-slot="Pet"]', timeout=15000)
            await framed("kiteChula, the picker open again", FIT_DIR_PET)
        # none: today's view again, exactly
        await pick(None)
        await page.wait_for_timeout(300)
        cam = await page.evaluate(CAM)
        fit, today, live = cam["fit"], cam["today"], cam["live"]
        ts = await page.evaluate(PK_TILES)
        rg = await page.evaluate(RING)
        check(fit is not None and near_v(fit["pos"], today["pos"], 1e-9) and near_v(live["pos"], today["pos"], today["h"] * .01)
              and near_v(dir_of(live), FIT_DIR, 1e-6) and ts[0]["pressed"]
              and rg and rg["glyph"], f"{T} ไม่ใส่: no pet, the camera back at today's view {fmt(live['pos'])} (today {fmt(today['pos'])}), "
                                      f"ไม่ใส่ pressed {ts[0]['pressed']}, the ring's outline {rg}")
        # TianlongA at 2x beside the Whale
        await page.evaluate("() => wardrobe.show('whale')")
        if await page.evaluate("() => document.getElementById('picker').hidden"):
            await page.click('#topics button.topic[data-t="Pet"]')
        await page.wait_for_selector('#pkBody .pk-item[data-p="TianlongA"]', timeout=15000)
        await hold()                                             # (show() played the idle again)
        await pick("TianlongA", glide=False)
        await page.evaluate(GLIDE)
        await page.click("#resetCam")
        await page.evaluate("() => window.__glide")
        await framed("whale TianlongA (2x)", FIT_DIR_PET)
        await shot(f"stage_{tag}_whale_TianlongA.png")

        # ---- the pet's whole idle on the free stage (fix round 1): the desktop picker open, closed (its refit), open again
        for cls, name in (("whale", "TianlongA"), ("sheep", "smallAnubi"), ("sheep", "miniMokBug")):
            if await page.evaluate("() => wardrobe.debug().C.cls") != cls:
                await page.evaluate("c => wardrobe.show(c)", cls)
            if await page.evaluate("() => document.getElementById('picker').hidden"):
                await page.click('#topics button.topic[data-t="Pet"]')
            await page.wait_for_selector(f'#pkBody .pk-item[data-p="{name}"]', timeout=15000)
            await hold()                                         # (show() played the idle again)
            if await page.evaluate("() => wardrobe.debug().C.state.Pet") != name:
                await pick(name, glide=False)
            await page.evaluate(GLIDE)
            await page.click("#resetCam")
            await page.evaluate("() => window.__glide")
            await framed(f"{cls} {name}: the fit", FIT_DIR_PET)
            await idle_framed(f"{cls:6} {name}, {'the picker open' if tag == 'desktop' else 'the sheet open'}")
            await shot(f"stage_{tag}_{cls}_{name}_open.png")
            if tag != "desktop":
                continue
            await page.evaluate(GLIDE)
            await page.click("#pkClose")
            await page.evaluate("() => window.__glide")
            await idle_framed(f"{cls:6} {name}, the picker closed")
            await shot(f"stage_{tag}_{cls}_{name}_closed.png")
            await page.evaluate(GLIDE)
            await page.click('#topics button.topic[data-t="Pet"]')
            await page.evaluate("() => window.__glide")
            await page.wait_for_selector('#pkBody .pk-cell[data-slot="Pet"]', timeout=15000)
            await idle_framed(f"{cls:6} {name}, the picker open again")
        await page.click("#pkClose")
        await page.wait_for_timeout(600)
        await page.locator("aside").screenshot(path=str(UI_OUT / f"panel_{tag}_miniMokBug.png"))
        await ctx.close()


async def main():
    errors, fails, requests = [], [], []
    check = lambda ok, what: (print(("ok   " if ok else "FAIL ") + what), ok or fails.append(what))
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        dl_errors = []                         # its own pages' (Focus 1 below wants none on its page so far)
        if not UI_ONLY:
            await downloads(b, check, dl_errors)
        if not DOWNLOADS_ONLY:
            await ui(b, check, dl_errors)      # the topic, the picker, the camera: on pages of their own too
        if DOWNLOADS_ONLY or UI_ONLY:
            await b.close()
            print("errors:", dl_errors)
            print(f"{len(fails) + bool(dl_errors)} failed" if fails or dl_errors else "all ok")
            sys.exit(1 if fails or dl_errors else 0)
        ctx = await b.new_context(viewport={"width": 1366, "height": 768})
        # Review Focus 1's saved loadout, written once before the page's own script reads it (a reload keeps what the page saved)
        await ctx.add_init_script("if (!sessionStorage.getItem('petcheck')) { sessionStorage.setItem('petcheck', '1'); "
                                  f"localStorage.setItem('wardrobe_v1', {json.dumps(json.dumps(SAVED))}); }}")
        page = await ctx.new_page()
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: m.type == "error" and errors.append(m.text + " " + (m.location or {}).get("url", "")))
        reloading = [False]                    # a reload aborts what was still loading: not a failure
        page.on("requestfailed", lambda r: (reloading[0] and "ERR_ABORTED" in (r.failure or "")) or errors.append(f"request failed {r.url} {r.failure}"))
        page.on("request", lambda r: requests.append(r.url))
        await page.goto(URL)
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)

        # ---- Review Focus 1: a saved pet the data has not
        st = await page.evaluate(PET)
        toast = await page.evaluate("() => document.getElementById('status').classList.contains('err') ? document.getElementById('status').textContent : ''")
        asked = [u for u in requests if "noSuchPet" in u]
        check(st["cls"] == "sheep" and st["state"] is None and st["on"] is None and not st["pets"],
              f"saved Pet 'noSuchPet': the Sheep loads with no pet (state {st['state']!r}, on stage {st['pets']})")
        check(not asked and not toast and not errors, f"  no request for it {asked}, no error toast {toast!r}, no errors {errors}")
        hooks = await page.evaluate("() => { const d = wardrobe.debug(); return ['setPet', 'petIndex', 'pickPet'].filter(k => typeof d[k] !== 'function'); }")
        if hooks:
            check(False, f"no Pet slot: wardrobe.debug() has no {hooks}")
            await b.close()
            print("errors:", errors)
            sys.exit(1)
        rows = await page.evaluate("() => wardrobe.debug().petIndex().then(r => r.length)")
        check(rows == len(ROWS), f"petIndex(): {rows} rows (index.json {len(ROWS)})")

        # ---- placement, size and idle for every class x pet
        async def placed(name, cls, what=""):
            st = await page.evaluate(PET)
            row = ROWS[name]
            want, game = row["rest"][cls], rest_point(unity(row["follow"]), cls)
            ok = (st["on"] == name and st["state"] == name and st["pets"] == [name] and not st["onBone"]
                  and near(st["p"], want, 1e-3) and near(st["p"], game, 1e-3) and st["qdot"] > 1 - 1e-6
                  and near(st["s"], [row["scale"][cls]] * 3, 1e-6) and st["shown"])
            check(ok, f"{cls:6} {name:13} {what}at {[round(x, 4) for x in st.get('p') or []]} (rest {want}, rest_point {game}) "
                      f"x{round((st.get('s') or [0])[0], 4)} (row {row['scale'][cls]}), the hero's rotation {st.get('qdot', 0) > 1 - 1e-6}, "
                      f"on a hero bone {st.get('onBone')}, alone in the scene {st['pets']}, shown {st.get('shown')}")
            return st

        for cls in CLASSES:
            await page.evaluate(SHOW, cls)
            for name in PETS:
                await page.evaluate(SET, name)
                st = await placed(name, cls)
                has_clip = "anim" in json.loads((ROOT / "wardrobe" / "data" / ROWS[name]["file"]).read_text(encoding="utf-8"))
                if not has_clip:
                    check(not st["mixer"], f"{cls:6} {name:13}   no clip: no mixer")
                    continue
                m0 = await page.evaluate(MOTION)
                await page.wait_for_timeout(500)
                m1 = await page.evaluate(MOTION)
                dt = m1["t"] - m0["t"] if m0 and m1 else 0
                pairs = [(a, c) for a, c in zip(m0["nodes"], m1["nodes"]) if a and c] if m0 and m1 else []
                turn = max((1 - abs(sum(x * y for x, y in zip(a[:4], c[:4]))) for a, c in pairs), default=0)
                move = max((abs(x - y) for a, c in pairs for x, y in zip(a[4:], c[4:])), default=0)
                # a node's quaternion turns; a clip that turns nothing (smallKumo's one node only bobs) moves or squashes it
                check(st["loop"] and 0.25 < dt < 1.5 and (turn > 1e-7 or move > 1e-4),
                      f"{cls:6} {name:13}   idle loops {st['loop']}, mixer +{dt:.2f} s, a node turned {turn:.2e} (1 - |q0.q1|)"
                      + ("" if turn > 1e-7 else f", none turns: moved / scaled {move:.4f}"))
        await page.evaluate(SET, None)
        st = await page.evaluate(PET)
        check(st["on"] is None and st["state"] is None and not st["pets"], f"setPet(null): no pet ({st['pets']})")

        # ---- Review Focus 2: two picks 50 ms apart; the first's file held back so the second lands first, then no hold
        PICKS = """async ([a, b]) => { const { pickPet, C } = wardrobe.debug(), seen = [];
          const tick = setInterval(() => { const n = C.props.Pet?.userData.pet || null; if (seen[seen.length - 1] !== n) seen.push(n); }, 5);
          const pa = pickPet(a); await new Promise(r => setTimeout(r, 50)); const pb = pickPet(b);
          await Promise.all([pa, pb]); clearInterval(tick);
          const n = C.props.Pet?.userData.pet || null; if (seen[seen.length - 1] !== n) seen.push(n); return seen; }"""
        UNDO = "() => ({ undo: !document.getElementById('undo').disabled, redo: !document.getElementById('redo').disabled })"
        # (pets not picked yet: a file already loaded comes from the page's cache, with no request to hold)
        for cls, (pa, pb), held in (("sheep", ("littleCarron", "littlePeppon"), True), ("bison", ("littlePumpkon", "littleMellon"), False)):
            await page.evaluate(SHOW, cls)                       # another class: its history starts empty
            await page.evaluate(SET, None)                       # (no undo step: setPet alone is not a pick)
            u0 = await page.evaluate(UNDO)
            if held:
                async def hold(route):
                    await asyncio.sleep(1.0)
                    await route.continue_()
                await page.route(f"**/data/pets/{pa}.json", hold)
            seen = await page.evaluate(PICKS, [pa, pb])
            if held:
                await page.unroute(f"**/data/pets/{pa}.json")
            st = await page.evaluate(PET)
            tag = f"{cls}: {pa} then {pb} 50 ms later{' (' + pa + ' held 1 s)' if held else ''}"
            check(not u0["undo"] and st["on"] == pb and st["state"] == pb and st["pets"] == [pb] and (not held or pa not in seen),
                  f"{tag}: on stage {st['pets']}, seen {seen}")
            steps, ends = [], []
            for btn, want in (("undo", pa), ("undo", None), ("redo", pa), ("redo", pb)):
                await page.click(f"#{btn}")
                try:
                    await page.wait_for_function("w => { const { C } = wardrobe.debug(); return (C.state.Pet ?? null) === w && (C.props.Pet?.userData.pet ?? null) === w; }",
                                                 arg=want, timeout=15000)
                    ends.append(True)
                except Exception:                           # the step landed elsewhere (steps says where)
                    ends.append(False)
                steps.append(f"{btn} -> {(await page.evaluate(PET))['pets']} (want {want})")
                if want is None or want == pb:              # after the second undo / the second redo: nothing more that way
                    ends.append(not (await page.evaluate(UNDO))[btn])
            check(all(ends), f"{tag}: one undo step per pick: {', '.join(steps)}, then nothing more to undo / redo {ends}")

        # ---- Review Focus 3: class switches with a pet out
        for cls in ("whale", "bison"):
            await page.evaluate(SHOW, cls)
            await page.evaluate(SET, "TianlongA")
            await placed("TianlongA", cls, "picked ")
        for cls in ("whale", "bison", "whale"):
            await page.evaluate(SHOW, cls)
            await placed("TianlongA", cls, "back after the switch ")
        for cls in ("wolf", "mole"):
            await page.evaluate(SHOW, cls)
            await page.evaluate(SET, "kiteChula")
        for cls in ("wolf", "mole"):
            await page.evaluate(SHOW, cls)
            st = await placed("kiteChula", cls, "back after the switch ")
        check(abs(ROWS["kiteChula"]["rest"]["wolf"][1] - ROWS["kiteChula"]["rest"]["mole"][1]) > 0.1,
              f"the kite's height differs by class: wolf {ROWS['kiteChula']['rest']['wolf'][1]}, mole {ROWS['kiteChula']['rest']['mole'][1]}")
        saved = await page.evaluate("() => JSON.parse(localStorage.getItem('wardrobe_v1'))")
        check(saved.get("whale", {}).get("Pet") == "TianlongA" and saved.get("mole", {}).get("Pet") == "kiteChula",
              f"saved per class: whale {saved.get('whale', {}).get('Pet')}, mole {saved.get('mole', {}).get('Pet')}")
        reloading[0] = True
        await page.reload()
        reloading[0] = False
        await page.wait_for_function("() => window.wardrobe && wardrobe.debug().C && wardrobe.debug().C.props.Pet", timeout=120000)
        await placed("kiteChula", "mole", "after a reload ")
        await page.evaluate(SHOW, "whale")
        await placed("TianlongA", "whale", "after a reload ")

        # ---- the คัดลอกให้ Claude line
        await page.evaluate("() => { navigator.clipboard.writeText = t => { window.__copied = t; return Promise.resolve(); }; }")
        await page.click("#copy")
        await page.wait_for_function("() => window.__copied", timeout=10000)
        line = await page.evaluate("() => window.__copied")
        check(line.endswith(", สัตว์เลี้ยง TianlongA") or ", สัตว์เลี้ยง TianlongA," in line, f"copy line: {line}")

        # ---- Review Focus 4: ชมชิ้นส่วน on the outfit hides the pet with the character, its exit shows it again
        await page.evaluate("() => { const { Showcase, C } = wardrobe.debug(); Showcase.enter('outfit', C.state.outfit); }")
        await page.wait_for_function("() => { const { Showcase } = wardrobe.debug(); return Showcase.phase === 'on' && Showcase.piece; }", timeout=60000)
        st = await page.evaluate(PET)
        await page.screenshot(path=str(OUT / "showcase.png"))
        check(st["on"] == "TianlongA" and not st["shown"], f"Showcase on the outfit: the pet hidden (shown {st['shown']})")
        await page.evaluate("() => wardrobe.debug().Showcase.exit()")
        await page.wait_for_function("() => wardrobe.debug().Showcase.phase === 'off'", timeout=30000)
        st = await placed("TianlongA", "whale", "after Showcase's exit ")
        await page.screenshot(path=str(OUT / "whale_tianlong.png"))

        # ---- skill effects: a move that changes the hero's look or place leaves the pet as it was; a whole-hero hide hides it
        LOOKS = """() => { const { C, FX, THREE } = wardrobe.debug(), o = C.props.Pet;
          const mats = [], masks = [], geos = new Set(); let copies = 0;
          o.traverse(x => { if (!x.isMesh) return; if (x.userData.lookCopy) { copies++; return; } masks.push(x.layers.mask); geos.add(x.geometry);
            for (const m of [].concat(x.material)) if (m?.color) mats.push(m.color.getHexString()); });
          o.updateWorldMatrix(true, false);
          let clones = 0, petCopies = 0;
          for (const f of FX.live) if (f.name.startsWith('clone:') && f.group) { clones++; f.group.traverse(x => { if (x.isMesh && geos.has(x.geometry)) petCopies++; }); }
          return { p: o.getWorldPosition(new THREE.Vector3()).toArray(), s: o.getWorldScale(new THREE.Vector3()).toArray(), mats, masks, copies, clones, petCopies,
            heroScale: C.root.scale.x, heroY: C.root.position.y, heroMask: C.meshes[0]?.layers.mask ?? null }; }"""

        async def play(tile):                    # a skill tile of the move picker, as a visitor plays it
            if not await page.evaluate("() => !document.getElementById('picker').hidden && document.getElementById('pkBody').dataset.topic === 'move'"):
                await page.click('button.topic[data-t="move"]')
            await page.click('.pk-tab[data-g="skill"]')
            await page.click(f'#pkBody .pk-item[data-m="{tile}"]')

        def kept(a, ref):                        # the pet as it stood before the move
            return (near(a["p"], ref["p"], 1e-4) and near(a["s"], ref["s"], 1e-6) and a["mats"] == ref["mats"] and a["masks"] == ref["masks"]
                    and a["copies"] == 0 and a["petCopies"] == 0)

        def tell(a):
            return (f"pet at {[round(x, 3) for x in a['p']]} x{round(a['s'][0], 3)}, colours {a['mats'][:3]}, layers {sorted(set(a['masks']))}, "
                    f"shells on it {a['copies']}, {a['clones']} clones holding {a['petCopies']} copies of it; hero x{round(a['heroScale'], 2)} y {round(a['heroY'], 2)}")
        HOLDS = {"body": "C.root.scale.x > 1.2", "lift": "C.root.position.y > 1",
                 "shell": "C.meshes.some(m => m.children.some(k => k.userData.lookCopy))",
                 "clone": "FX.live.filter(f => f.name.startsWith('clone:')).length >= 2", "hide": "C.meshes[0]?.layers.mask === 0"}
        ref = None
        for cls, tile, kind, what in (("bison", "enrage", "body", "grow 1.25 + tint"), ("bison", "titanDrop", "lift", "up to 3 m"),
                                      ("chameleon", "backStep", "shell", "FX/Blend"), ("bat", "@ShadowIllusion", "clone", "two HeroClones"),
                                      ("chameleon", "@ThunderDragon", "hide", "the whole hero hidden")):
            if ref is None or await page.evaluate("() => wardrobe.debug().C.cls") != cls:
                await page.evaluate(SHOW, cls)
                await page.evaluate(SET, "smallAnubi")
                await page.wait_for_timeout(300)
                ref = await page.evaluate(LOOKS)
            await play(tile)
            try:
                await page.wait_for_function(f"() => {{ const {{ C, FX }} = wardrobe.debug(); return {HOLDS[kind]}; }}", timeout=30000)
                took = True
            except Exception:
                took = False
            st = await page.evaluate(LOOKS)
            if kind != "hide":
                check(took and kept(st, ref), f"{cls:9} {tile} ({what}) took hold {took}: {tell(st)}")
                continue
            hidden = took and bool(st["masks"]) and all(m == 0 for m in st["masks"])
            try:
                await page.wait_for_function("() => wardrobe.debug().C.meshes[0]?.layers.mask !== 0", timeout=30000)
            except Exception:
                pass
            after = await page.evaluate(LOOKS)
            check(hidden and kept(after, ref), f"{cls:9} {tile} ({what}) took hold {took}: the pet hidden with the hero "
                                               f"(layers {sorted(set(st['masks']))}), shown again after (layers {sorted(set(after['masks']))}), {tell(after)}")
        await b.close()
    errors += dl_errors
    print("errors:", errors)
    if errors:
        fails.append("page errors")
    print(f"{len(fails)} failed" if fails else "all ok")
    sys.exit(1 if fails else 0)


asyncio.run(main())
