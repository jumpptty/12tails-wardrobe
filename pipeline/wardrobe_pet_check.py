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
    it off in one undo step
Exit 1 on any failure. Serves the folder itself on a free port (never 8771, the main folder's page). --downloads runs the
downloads part alone.
  uv run --no-project --with playwright==1.65.1 python -I pipeline/wardrobe_pet_check.py [D:/12tails-wardrobe checks/pet_check] [--downloads]"""
import asyncio, base64, functools, http.server, json, re, struct, sys, threading
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")       # Thai on any console
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))                  # -I leaves the script's folder off the path: the rules' module by its bare name
from wardrobe_pets import rest_point           # noqa: E402  (the pure rules; no UnityPy at import)

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
DOWNLOADS_ONLY = "--downloads" in sys.argv
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

    def items_ok(m, name, cls, locked, topic, tag=""):     # locked: no download item (a TTO pet under ?ttolock)
        texs = pet_parts(name)[0]
        want = (["change"] if topic else []) + ["remove"]
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

    topic_js = "() => !!document.querySelector('#topics [data-t=\"Pet\"]')"

    # ---- the local copy: every pet downloads
    page = await page_at("")
    topic = await page.evaluate(topic_js)
    print(f"     (the สัตว์เลี้ยง topic {'exists: เปลี่ยนสัตว์เลี้ยง expected' if topic else 'is not on the page yet: no เปลี่ยนสัตว์เลี้ยง item'})")
    for cls, name in (("sheep", "smallAnubi"), ("wolf", "miniAncientBug"), ("sheep", "smallDragonZ")):
        pt = await wear(page, cls, name)
        m = await menu(page, name, f"{cls:6} {name:14}", pt)
        if not m:
            continue
        items_ok(m, name, cls, False, topic)
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
    for cls, name, locked in (("sheep", "smallDragonZ", True), ("sheep", "smallAnubi", False)):
        pt = await wear(page, cls, name)
        m = await menu(page, name, f"{cls:6} {name:14} ?ttolock", pt)
        if m:
            items_ok(m, name, cls, locked, topic, "?ttolock ")
            await page.keyboard.press("Escape")
    await page.close()
    await ctx.close()


async def main():
    errors, fails, requests = [], [], []
    check = lambda ok, what: (print(("ok   " if ok else "FAIL ") + what), ok or fails.append(what))
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        dl_errors = []                         # its own pages' (Focus 1 below wants none on its page so far)
        await downloads(b, check, dl_errors)
        if DOWNLOADS_ONLY:
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
