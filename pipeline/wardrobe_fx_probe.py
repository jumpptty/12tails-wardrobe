"""Effect QA probe (2026-11-10, the Sheep's QA pass): plays tiles with the camera at a chosen view and prints, at set
times, each live effect's world bounding box in the hero's frame (y up, z ahead; x is three's, i.e. Unity's mirrored),
plus a screenshot per time (<out>/<cls>_<tile>_<view>_<t>[skill].png). The check's own shots (wardrobe_fx_check.py) sit
at the default camera, which faces the hero, so the cues 10 m ahead are behind it: "back" (behind the hero, looking
ahead) shows them. The orbit target stays clamped to the hero (the page's clampTarget), so every view looks at her.
Optional: a pool forced to one skill ("cast3=divinitySpear") and props worn ('{"R": "clericBook"}'). One browser.
  uv run --no-project --with playwright python -I pipeline/wardrobe_fx_probe.py <repo> <out dir> <cls> <tile>[,<tile>...]
      [t1,t2,...] [side|front|back|far|top|near|book|spot|bookside|bookback] [<cue key>=<skill>] [<props JSON>]
A tile listed twice plays twice (the second play has its files loaded, so its timing is the page's own)."""
import asyncio, functools, http.server, json, sys, threading
from pathlib import Path

ROOT, OUT, CLS, TILES = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4].split(",")
TIMES = [float(x) for x in (sys.argv[5] if len(sys.argv) > 5 else "0.5,1,2,3").split(",")]
VIEW = sys.argv[6] if len(sys.argv) > 6 else "side"
FORCE = sys.argv[7] if len(sys.argv) > 7 else ""
SLOTS = json.loads(sys.argv[8]) if len(sys.argv) > 8 else {}   # props to wear, {"R": "clericBook"}   # "<cue key>=<skill>": that pool plays only that skill
OUT.mkdir(parents=True, exist_ok=True)


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


http.server.ThreadingHTTPServer.request_queue_size = 128
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/wardrobe/index.html?fxbg=dark"
CAMS = {"side": ([20, 6, 5], [0, 1, 0]), "front": ([0, 3, 18], [0, 1, 0]), "back": ([0, 4, -10], [0, 1, 0]), "far": ([-8, 4, 20], [0, 1, 0]), "book": ([3, 3.5, 15.5], [0, 1, 0]), "bookside": ([8, 3.5, 11], [0, 1, 0]), "bookback": ([-2, 4, 5], [0, 1, 0]), "spot": ([5, 3, 17], [0, 1, 0]),
        "top": ([0.01, 22, 5], [0, 0, 5]), "near": ([4, 2, 4], [0, 1, 0])}
BOXES = """() => { const { FX, THREE, C } = wardrobe.debug(); const hp = new THREE.Vector3(); C.root.getWorldPosition(hp);
  const hq = new THREE.Quaternion(); C.root.getWorldQuaternion(hq); const inv = hq.clone().invert();
  return FX.live.map(f => { const b = new THREE.Box3(); f.group.updateMatrixWorld(true);
    f.group.traverse(o => { if ((o.isMesh || o.isLine || o.isPoints) && o.geometry?.attributes.position?.count) {
      o.geometry.computeBoundingBox(); const bb = o.geometry.boundingBox.clone();
      if (!bb.isEmpty()) b.union(bb.applyMatrix4(o.matrixWorld)); } });
    if (b.isEmpty()) return f.name + ': (nothing drawn)';
    const lo = b.min.clone().sub(hp).applyQuaternion(inv), hi = b.max.clone().sub(hp).applyQuaternion(inv);
    const mn = lo.clone().min(hi), mx = lo.clone().max(hi), r = v => v.toArray().map(x => x.toFixed(2)).join(',');
    return `${f.name}: min(${r(mn)}) max(${r(mx)}) [hero frame: x left?, y up, z ahead]`; }); }"""


async def main():
    from playwright.async_api import async_playwright
    errors = []
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--autoplay-policy=no-user-gesture-required"])
        page = await b.new_page(viewport={"width": 1366, "height": 768})
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: m.type in ("error", "warning") and errors.append(m.type + ": " + m.text))
        await page.goto(URL)
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
        await page.evaluate("([c, s]) => wardrobe.show(c, s)", [CLS, SLOTS])
        await page.wait_for_function("c => wardrobe.debug().C?.cls === c && wardrobe.debug().FX.cueTab[c]", arg=CLS, timeout=120000)
        pos, tgt = CAMS[VIEW]
        if FORCE:
            await page.evaluate("""([c, k, s]) => { const e = wardrobe.debug().FX.cueTab[c][k]; e.skills = { [s]: e.skills[s] }; }""", [CLS, *FORCE.split("=")])
        for tile in TILES:
            await page.click('button.topic[data-t="move"]') if await page.locator('#picker').is_hidden() else None
            await page.click('.pk-tab[data-g="skill"]')
            loc = page.locator(f'#pkBody .pk-item[data-m="{tile}"]')
            if await loc.count() == 0:
                await page.click('.pk-tab[data-g="emotion"]') if await page.locator('.pk-tab[data-g="emotion"]').count() else None
            await page.click(f'#pkBody .pk-item[data-m="{tile}"]')
            await page.click('#pkClose') if await page.locator('#pkClose').count() else None
            await page.evaluate("""([p, t]) => { const { camera, controls, C, THREE } = wardrobe.debug();
              const hq = new THREE.Quaternion(); C.root.getWorldQuaternion(hq); const hp = new THREE.Vector3(); C.root.getWorldPosition(hp);
              controls.maxDistance = 200; controls.minDistance = 0.1; controls.enableDamping = false;
              camera.position.copy(new THREE.Vector3(...p).applyQuaternion(hq).add(hp));
              controls.target.copy(new THREE.Vector3(...t).applyQuaternion(hq).add(hp)); controls.update(); }""", [pos, tgt])
            t0 = await page.evaluate("() => performance.now()")
            for t in TIMES:
                while (await page.evaluate("() => performance.now()") - t0) / 1000 < t:
                    await page.wait_for_timeout(15)
                now = (await page.evaluate("() => performance.now()") - t0) / 1000
                await page.evaluate("""([p, t]) => { const { camera, controls, C, THREE } = wardrobe.debug();
                  const hq = new THREE.Quaternion(); C.root.getWorldQuaternion(hq); const hp = new THREE.Vector3(); C.root.getWorldPosition(hp);
                  camera.position.copy(new THREE.Vector3(...p).applyQuaternion(hq).add(hp));
                  controls.target.copy(new THREE.Vector3(...t).applyQuaternion(hq).add(hp)); controls.update(); }""", [pos, tgt])
                boxes = await page.evaluate(BOXES)
                print(f"-- {tile} {now:.2f}s"); [print("   ", x) for x in boxes]
                await page.screenshot(path=str(OUT / f"{CLS}_{tile.lstrip('@')}_{VIEW}_{t:05.2f}{FORCE.split('=')[-1]}.png"))
        await b.close()
    print("console:", json.dumps(errors[:40], ensure_ascii=False, indent=0))


asyncio.run(main())
