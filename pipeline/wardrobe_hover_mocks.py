"""Hover looks side by side (2026-11-09; user: "suggest a few more hover effect mocks"). The Wolf in a hat and a main-hand
weapon, the idle paused so every shot has the same pose; each look (?hover=...) hovering the outfit, the hat and the
weapon, the animated ones (pulse, sweep) at three moments. Writes <out>/<look>_<piece>[_<t>].png, <out>/compare.html
and <out>/grid.png (the hero's middle, one row per look). Exit 1 on a page error.
  uv run --no-project --with playwright --with pillow python -I pipeline/wardrobe_hover_mocks.py D:/12tails-wardrobe checks/hover_mocks [looks]"""
import asyncio, functools, http.server, sys, threading
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
ROOT, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
LOOKS = (sys.argv[3] if len(sys.argv) > 3 else "none,rimpulse,gold,pulse,outline,rim,sweep").split(",")
TIMES = {"pulse": [0, 350, 700], "rimpulse": [0, 350, 700], "sweep": [300, 800, 1300]}      # ms into the animation
PIECES = ["outfit", "Head", "R"]
CLIP = {"x": 600, "y": 70, "width": 620, "height": 640}


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


http.server.ThreadingHTTPServer.request_queue_size = 128
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/wardrobe/index.html"
POINTS = """() => { const { pieceAt, renderer } = wardrobe.debug(), r = renderer.domElement.getBoundingClientRect(), hits = {};
  for (let y = r.top + 8; y < r.bottom; y += 8) for (let x = r.left + 8; x < r.right; x += 8) {
    const t = pieceAt(x, y); if (t) (hits[t.slot] ||= []).push([x, y]); }
  const out = {};
  for (const [s, ps] of Object.entries(hits)) { const cx = ps.reduce((a, p) => a + p[0], 0) / ps.length, cy = ps.reduce((a, p) => a + p[1], 0) / ps.length;
    out[s] = ps.reduce((b, p) => (Math.hypot(p[0] - cx, p[1] - cy) < Math.hypot(b[0] - cx, b[1] - cy) ? p : b)); }
  return out; }"""


async def main():
    errors, shots = [], {}
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        page = await b.new_page(viewport={"width": 1366, "height": 768})
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: m.type == "error" and errors.append(m.text))
        for look in LOOKS:
            await page.goto(URL + "?hover=" + (look if look != "none" else "gold"))
            await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
            await page.evaluate("() => wardrobe.show('wolf', { Head: 'afro', R: 'bdWeapon' })")
            await page.evaluate("() => { wardrobe.debug().C.mixer.timeScale = 0; }")
            await page.wait_for_timeout(500)
            pts = await page.evaluate(POINTS)
            for piece in (["none"] if look == "none" else PIECES):
                if piece != "none" and piece not in pts:
                    print(f"{look}: {piece} not on screen"); continue
                await page.mouse.move(*(pts[piece] if piece != "none" else (1340, 140)))
                await page.wait_for_timeout(300)
                for t in TIMES.get(look, [None]):
                    if t is not None:                     # the animation at a set moment
                        await page.evaluate("t => { wardrobe.debug().Hover.t0 = performance.now() - t; }", t)
                        await page.wait_for_timeout(60)
                    name = f"{look}_{piece}" + (f"_{t}" if t is not None else "")
                    await page.screenshot(path=str(OUT / f"{name}.png"), clip=CLIP)
                    shots.setdefault(look, []).append(name)
            print(look, "done")
        await b.close()
    # the page and the grid
    rows = "".join(f"<tr><th>{look}</th>" + "".join(f'<td><img src="{n}.png"><br>{n}</td>' for n in ns) + "</tr>" for look, ns in shots.items())
    (OUT / "compare.html").write_text("<!doctype html><meta charset=utf-8><title>Hover looks</title><style>body{font:13px sans-serif;margin:16px}"
                                      "img{width:260px}td{vertical-align:top;text-align:center}</style><table>" + rows + "</table>", encoding="utf-8")
    box, w = (120, 20, 500, 600), 0
    cols = max(len(ns) for ns in shots.values())
    cw, ch = (box[2] - box[0]) // 2, (box[3] - box[1]) // 2
    g = Image.new("RGB", (90 + cw * cols, ch * len(shots)), "white"); dr = ImageDraw.Draw(g)
    for i, (look, ns) in enumerate(shots.items()):
        dr.text((6, i * ch + ch // 2), look, fill="black")
        for j, n in enumerate(ns):
            g.paste(Image.open(OUT / f"{n}.png").crop(box).resize((cw, ch)), (90 + j * cw, i * ch))
            dr.text((90 + j * cw + 4, i * ch + 4), n.split("_", 1)[1] if "_" in n else n, fill="black")
    g.save(OUT / "grid.png")
    print("errors:", errors)
    sys.exit(1 if errors else 0)


asyncio.run(main())
