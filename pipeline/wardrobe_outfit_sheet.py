r"""Every outfit of a class on the hero, front and back, in one labelled picture (2026-11-12; user: "find the best cat outfit
that can best represent this reference image"): for picking the outfit whose shape suits a repaint (wardrobe_repaint.py).
The local page, headless; no props, colour 1.
  uv run --no-project --with pillow --with numpy --with scipy --with playwright python -I pipeline/wardrobe_outfit_sheet.py cat <out.png> [outfit ...]"""
import asyncio, functools, http.server, json, sys, threading
from pathlib import Path
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).resolve().parent))      # python -I leaves the script's folder off the path
from wardrobe_repaint import ROOT, DATA, crop

CLS, OUT, ONLY = sys.argv[1], Path(sys.argv[2]), sys.argv[3:]      # names after the picture: only those, larger
S = 640 if ONLY else 360


async def main():
    from playwright.async_api import async_playwright
    names = [o["name"] for o in json.loads((DATA / CLS / "outfits.json").read_text("utf-8")) if o.get("colors") and (not ONLY or o["name"] in ONLY)]
    Q = type("Q", (http.server.SimpleHTTPRequestHandler,), {"log_message": lambda *a: None})
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Q, directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    tmp = OUT.parent / "_sheet"
    tmp.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        page = await (await b.new_context(viewport={"width": 1400, "height": 1100})).new_page()
        await page.goto(f"http://127.0.0.1:{srv.server_port}/wardrobe/")
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
        await page.add_style_tag(content="*{visibility:hidden!important} canvas{visibility:visible!important}")
        await page.evaluate("""async cls => { const { scene, THREE } = wardrobe.debug(); scene.background = new THREE.Color(0xe6e1d8);
          await wardrobe.show(cls, {}); for (const s of ["Head", "R", "L", "Back"]) await wardrobe.show(cls, { [s]: null }); }""", CLS)
        for n in names:
            await page.evaluate("n => wardrobe.setOutfit(n, 1)", n)
            for yaw, side in ((20, "f"), (200, "b")):
                await page.evaluate("([c, y]) => wardrobe.show(c, {}, y)", [CLS, yaw])
                await page.wait_for_timeout(300)
                f = tmp / f"{n}_{side}.png"
                await page.locator("canvas").first.screenshot(path=str(f))
                crop(f, size=S)
        await b.close()
    srv.shutdown()
    cols = 2 if ONLY else 4
    sheet = Image.new("RGB", (cols * 2 * S, -(-len(names) // cols) * (S + 24)), "white")
    d = ImageDraw.Draw(sheet)
    for i, n in enumerate(names):
        x, y = (i % cols) * 2 * S, (i // cols) * (S + 24)
        sheet.paste(Image.open(tmp / f"{n}_f.png"), (x, y + 24)); sheet.paste(Image.open(tmp / f"{n}_b.png"), (x + S, y + 24))
        d.text((x + 8, y + 4), n, fill="black")
    sheet.save(OUT)
    print(OUT, len(names), "outfits")

asyncio.run(main())
