"""Screenshot of one class's move picker tab, scrolled through (2026-11-10: checking the one-tile-per-skill tiles' names and
icons). Headless, swiftshader, one browser.
  uv run --no-project --with playwright python -I pipeline/wardrobe_picker_shot.py <repo> <out dir> <cls> [skill|emotion|base]
-> <out>/<cls>_<tab>_<n>.png (the picker body scrolled a page at a time) and the tiles' ids and names printed."""
import asyncio, functools, http.server, sys, threading
from pathlib import Path

ROOT, OUT, CLS = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
TAB = sys.argv[4] if len(sys.argv) > 4 else "skill"
OUT.mkdir(parents=True, exist_ok=True)


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


http.server.ThreadingHTTPServer.request_queue_size = 128
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/wardrobe/index.html"


async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        page = await b.new_page(viewport={"width": 1366, "height": 900})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        await page.goto(URL)
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
        await page.evaluate("c => wardrobe.show(c)", CLS)
        await page.wait_for_function("c => wardrobe.debug().C?.cls === c && wardrobe.debug().FX.cueTab[c]", arg=CLS, timeout=120000)
        await page.click('button.topic[data-t="move"]')
        await page.click(f'.pk-tab[data-g="{TAB}"]')
        await page.wait_for_timeout(1500)                     # the icons load
        tiles = await page.evaluate("() => [...document.querySelectorAll('#pkBody .pk-item')].map(b => b.dataset.m + ' = ' + b.textContent.trim())")
        print(f"{len(tiles)} tiles:", "; ".join(tiles))
        h = await page.evaluate("() => { const b = document.querySelector('#pkBody'); return [b.scrollHeight, b.clientHeight]; }")
        n, y = 0, 0
        while True:
            await page.evaluate("y => document.querySelector('#pkBody').scrollTop = y", y)
            await page.wait_for_timeout(600)
            await page.screenshot(path=str(OUT / f"{CLS}_{TAB}_{n}.png"))
            n += 1; y += h[1]
            if y >= h[0]:
                break
        print("shots:", n, "errors:", errors)
        await b.close()


asyncio.run(main())
