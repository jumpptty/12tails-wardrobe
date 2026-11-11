"""Screenshots of a class holding each named weapon, with the weapon's size beside the hero's (2026-11-11: player reports
of a wrong Sheep Halloween weapon and an over-long Bat Halloween wand). Headless, swiftshader, one browser.
  uv run --no-project --with playwright python -I pipeline/wardrobe_weapon_shot.py <repo> <out dir> <cls> <weapon> [<weapon> ...]
-> <out>/<cls>_<weapon>.png and <cls>_<weapon>_close.png (aimed at the weapon), and per weapon its world-space box (longest side) and that side / the hero's height printed."""
import asyncio, functools, http.server, json, sys, threading
from pathlib import Path

ROOT, OUT, CLS, NAMES = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4:]
OUT.mkdir(parents=True, exist_ok=True)


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


http.server.ThreadingHTTPServer.request_queue_size = 128
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/wardrobe/index.html"

MEASURE = """() => { const { C, THREE } = wardrobe.debug(); const box = o => new THREE.Box3().setFromObject(o);
  const w = C.props.R, hb = new THREE.Box3(); C.meshes.forEach(m => hb.union(box(m)));   // the outfit only, not the props
  const wb = box(w), ws = wb.getSize(new THREE.Vector3()), hs = hb.getSize(new THREE.Vector3());
  const c = wb.getCenter(new THREE.Vector3()), hand = new THREE.Vector3(); w.parent.getWorldPosition(hand);
  return { centre: [c.x, c.y, c.z].map(v => +v.toFixed(2)), mount: w.parent.name, mount_at: [hand.x, hand.y, hand.z].map(v => +v.toFixed(2)),
           visible: w.visible, weapon: [ws.x, ws.y, ws.z].map(v => +v.toFixed(3)), hero_h: +hs.y.toFixed(3),
           ratio: +(Math.max(ws.x, ws.y, ws.z) / hs.y).toFixed(3) }; }"""


ZOOM = """() => { const { C, THREE, camera, controls, renderer, scene } = wardrobe.debug();
  const b = new THREE.Box3().setFromObject(C.props.R), c = b.getCenter(new THREE.Vector3()), r = b.getSize(new THREE.Vector3()).length();
  controls.target.copy(c); camera.position.set(c.x + r * 0.9, c.y + r * 0.35, c.z + r * 1.3); controls.update(); renderer.render(scene, camera); }"""


async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        page = await b.new_page(viewport={"width": 1100, "height": 900})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        await page.goto(URL)
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
        for n in NAMES:
            await page.evaluate(f"() => wardrobe.show({json.dumps(CLS)}, {{ R: {json.dumps(n)} }}, 35)")
            await page.wait_for_timeout(2500)
            try:
                m = await page.evaluate(MEASURE)
            except Exception as e:
                m = f"measure failed: {e}"
            print(n, m, flush=True)
            await page.screenshot(path=str(OUT / f"{CLS}_{n}.png"))
            await page.evaluate(ZOOM)          # a close-up: the camera aimed at the weapon's box
            await page.wait_for_timeout(800)
            await page.screenshot(path=str(OUT / f"{CLS}_{n}_close.png"))
        print("errors:", errors)
        await b.close()


asyncio.run(main())
