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
Exit 1 on any failure. Serves the folder itself on a free port (never 8771, the main folder's page).
  uv run --no-project --with playwright==1.65.1 python -I pipeline/wardrobe_pet_check.py [D:/12tails-wardrobe checks/pet_check]"""
import asyncio, functools, http.server, json, sys, threading
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")       # Thai on any console
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))                  # -I leaves the script's folder off the path: the rules' module by its bare name
from wardrobe_pets import rest_point           # noqa: E402  (the pure rules; no UnityPy at import)

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "checks" / "pet_check"
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


async def main():
    errors, fails, requests = [], [], []
    check = lambda ok, what: (print(("ok   " if ok else "FAIL ") + what), ok or fails.append(what))
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
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
    print("errors:", errors)
    if errors:
        fails.append("page errors")
    print(f"{len(fails)} failed" if fails else "all ok")
    sys.exit(1 if fails else 0)


asyncio.run(main())
