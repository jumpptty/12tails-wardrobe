"""Headless check of the built public copy (wardrobe_dist) itself, served on its own (2026-11-09, TTO online): the page
loads with no errors or failed requests; the Wolf's Halloween outfit (released TTO) is in the outfit list with the TTO
mark, wears, and its menu has no download / upload (preview only); a BB outfit's menu still has them; a released TTO
skill tile (Blade Surge) and Clap are in the move lists; the effects are on (the sound button shown).
  uv run --no-project --with playwright python -I pipeline/wardrobe_dist_check.py D:/12tails-wardrobe/wardrobe_dist checks/<dir>"""
import asyncio, functools, http.server, sys, threading
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")
DIST, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


http.server.ThreadingHTTPServer.request_queue_size = 128
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(DIST)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/index.html"
POINT = """() => { const { pieceAt, renderer } = wardrobe.debug(), r = renderer.domElement.getBoundingClientRect(), hits = [];
  for (let y = r.top + r.height * .3; y < r.bottom; y += 8) for (let x = r.left + r.width * .3; x < r.right - r.width * .2; x += 8) { const t = pieceAt(x, y); if (t?.slot === 'outfit') hits.push([x, y]); }
  return hits.length ? hits[Math.floor(hits.length / 2)] : null; }"""
MENU = "() => [...document.querySelectorAll('#pmenu .pm-item')].map(b => b.dataset.a)"


async def main():
    errors, fails = [], []
    check = lambda ok, what: (print(("ok   " if ok else "FAIL ") + what), ok or fails.append(what))
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        page = await b.new_page(viewport={"width": 1366, "height": 768})
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: m.type == "error" and not m.text.startswith("Failed to load resource") and errors.append(m.text))
        page.on("response", lambda r: r.status >= 400 and "goatcounter" not in r.url and errors.append(f"{r.status} {r.url}"))
        await page.goto(URL)
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
        await page.evaluate("() => wardrobe.show('wolf')")
        check(await page.locator("#sound").is_visible(), "effects on (the sound button shown; online since 2026-11-09)")
        await page.click('#topics [data-t="outfit"]'); await page.wait_for_selector("#pkBody .pk-item")
        tile = page.locator('#pkBody .pk-item[data-o="halloween"][data-e=""]')
        check(await tile.count() == 1 and await tile.locator(".tto-mark").count() == 1, "Halloween outfit tile with the TTO mark")
        await tile.click(); await page.wait_for_timeout(1500)
        await page.click("#pkClose")
        await page.evaluate("() => wardrobe.show('wolf')"); await page.wait_for_timeout(600)
        worn = await page.evaluate("() => wardrobe.debug().C.state.outfit")
        pt = await page.evaluate(POINT)
        await page.mouse.click(*pt); await page.wait_for_timeout(300)
        items = await page.evaluate(MENU)
        check(worn == "halloween" and items and not {"png", "glb", "up"} & set(items), f"wearing {worn}: menu {items} (preview only)")
        await page.screenshot(path=str(OUT / "dist_tto_menu.png"))
        await page.keyboard.press("Escape")
        await page.evaluate("() => wardrobe.setOutfit('standard')"); await page.wait_for_timeout(1200)
        await page.evaluate("() => wardrobe.show('wolf')"); await page.wait_for_timeout(600)
        pt = await page.evaluate(POINT)
        await page.mouse.click(*pt); await page.wait_for_timeout(300)
        items = await page.evaluate(MENU)
        check({"png", "glb", "up"} <= set(items), f"BB outfit: menu {items}")
        await page.keyboard.press("Escape")
        await page.click('#topics [data-t="move"]'); await page.click('.pk-tab[data-g="skill"]'); await page.wait_for_timeout(300)
        check(await page.locator('#pkBody .pk-item[data-m="bladeSurge"]').count() == 1, "skill tile Blade Surge (released TTO)")
        await page.click('.pk-tab[data-g="emote"]'); await page.wait_for_timeout(300)
        check(await page.locator('#pkBody .pk-item[data-m="clap"]').count() == 1, "emote tile Clap (released TTO)")
        await page.locator('#pkBody .pk-item[data-m="clap"]').click(); await page.wait_for_timeout(800)
        await b.close()
    print("errors:", errors)
    sys.exit(1 if errors or fails else 0)


asyncio.run(main())
