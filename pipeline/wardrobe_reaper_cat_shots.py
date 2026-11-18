r"""The Cat's ReaperTrinket (t_allhlw5) at its two places, for the user's pick (the pets branch's final review I2,
2026-11-19). TTO 1.7.0's TrinketPlacement moved it: Spine2 p (-0.193, 0.501, -0.034) -> Spine1 p (-0.363, 0.473, 0.180)
with a new q. wardrobe/data/placements.json keeps the old entry (pipeline/wardrobe_placements.py OVERRIDES) so the live
site and the video repo's Cat skits stay as they are; these shots show both on the real page.

  uv run --no-project --with playwright==1.65.1 python -I pipeline/wardrobe_reaper_cat_shots.py [<out folder>]

Serves this folder on a free port (never 8771), headless. The Cat wears ReaperTrinket (wardrobe.show('cat', {Back:
'ReaperTrinket'}, yaw)), the idle held at 0.5 s, from the front (yaw 0), the side (90) and the back (180):
  old_<front|side|back>.png     the data as committed (the old entry)
  tto170_<front|side|back>.png  the 1.7.0 entry, served in place of the committed one for that page only (a route; the
                                data on disk is never changed)
default out folder plans/pets/reaper_cat/ (tracked: the office PC sees them too). Each shot is the hero's box on the
stage with a margin, so the files stay small. Exit 1 if a page did not place the trinket on the entry asked for.
"""
import asyncio, functools, http.server, json, sys, threading
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "plans" / "pets" / "reaper_cat"
OUT.mkdir(parents=True, exist_ok=True)
PL = json.loads((ROOT / "wardrobe" / "data" / "placements.json").read_text(encoding="utf-8"))
OLD = PL["trinkets"]["cat"]["entries"]["t_allhlw5"]
# TTO 1.7.0's own entry, as wardrobe_placements.py converts it (tto_config/TrinketPlacement.json, the installed client
# of 2026-11-18; the pets branch's adda42c committed it before the override)
TTO170 = {"bone": "Spine1", "p": [-0.36309999227523804, 0.4733999967575073, 0.17970000207424164],
          "q": [0.506682, 0.571335, -0.529975, 0.368749], "s": 0.7912837266921997, "kwr": False, "kps": False}
ITEM = "ReaperTrinket"
VIEWS = (("front", 0), ("side", 90), ("back", 180))


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/wardrobe/index.html"

# the trinket's bone and placement, and the hero's drawn box on the canvas (CSS px), the idle held at 0.5 s
HOLD = """() => { const { C, THREE, camera, renderer, scene } = wardrobe.debug(), o = C.props.Back;
  C.mixer.setTime(0.5); for (const p of Object.values(C.props)) p.userData.mixer?.setTime(0); renderer.render(scene, camera);
  const box = new THREE.Box3(), v = new THREE.Vector3();
  for (const m of [...C.meshes, o]) { m.updateMatrixWorld(true); m.traverseVisible(x => { if (!x.isMesh) return;
    const n = x.geometry.attributes.position.count; for (let i = 0; i < n; i++) box.expandByPoint(x.getVertexPosition(i, v).applyMatrix4(x.matrixWorld)); }); }
  const r = renderer.domElement.getBoundingClientRect(); let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9;
  for (let i = 0; i < 8; i++) { v.set(i & 1 ? box.max.x : box.min.x, i & 2 ? box.max.y : box.min.y, i & 4 ? box.max.z : box.min.z).project(camera);
    const x = r.left + (v.x + 1) / 2 * r.width, y = r.top + (1 - v.y) / 2 * r.height;
    x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
  return { bone: o?.parent?.name ?? null, how: o?.userData.placement ?? null, p: o ? o.position.toArray() : null,
    clip: { x: Math.max(r.left, x0 - 40), y: Math.max(r.top, y0 - 40), x1: Math.min(r.right, x1 + 40), y1: Math.min(r.bottom, y1 + 40) } }; }"""


async def shots(b, tag, entry, served):
    ctx = await b.new_context(viewport={"width": 960, "height": 620})
    page = await ctx.new_page()
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)))
    page.on("console", lambda m: m.type == "error" and errs.append(m.text))
    if served is not None:                     # the page reads this placements.json instead of the one on disk
        body = json.dumps(served, separators=(",", ":"))
        await page.route("**/wardrobe/data/placements.json", lambda route: route.fulfill(status=200, content_type="application/json", body=body))
    await page.goto(URL)
    await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
    ok = True
    for view, yaw in VIEWS:
        await page.evaluate("([i, y]) => wardrobe.show('cat', { Back: i }, y)", [ITEM, yaw])
        if await page.evaluate("() => document.getElementById('khPause').textContent !== 'เล่นต่อ'"):
            await page.evaluate("() => document.activeElement?.blur()")
            await page.keyboard.press("Space")        # the idle held: both pages' shots at the same pose
        await page.wait_for_timeout(400)
        r = await page.evaluate(HOLD)
        here = r["bone"] == entry["bone"] and r["how"] == "entry" and all(abs(a - c) < 1e-6 for a, c in zip(r["p"] or [9, 9, 9], entry["p"]))
        ok &= here
        c = r["clip"]
        fn = OUT / f"{tag}_{view}.png"
        await page.screenshot(path=str(fn), clip={"x": c["x"], "y": c["y"], "width": c["x1"] - c["x"], "height": c["y1"] - c["y"]})
        print(("ok   " if here else "FAIL ") + f"{tag:6} {view:5} on {r['bone']} ({r['how']}) at {[round(x, 3) for x in r['p'] or []]} "
              f"(want {entry['bone']} {[round(x, 3) for x in entry['p']]}): {fn} {fn.stat().st_size // 1024} KB")
    if errs:
        print(f"FAIL {tag}: page errors {errs}")
    await ctx.close()
    return ok and not errs


async def main():
    if OLD["bone"] != "Spine2":
        print(f"note: the committed entry is on {OLD['bone']}, not the old Spine2 (the override changed?)")
    new = json.loads(json.dumps(PL))
    new["trinkets"]["cat"]["entries"]["t_allhlw5"] = TTO170
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        ok = await shots(b, "old", OLD, None)
        ok &= await shots(b, "tto170", TTO170, new)
        await b.close()
    print("all ok" if ok else "failed")
    sys.exit(0 if ok else 1)


asyncio.run(main())
