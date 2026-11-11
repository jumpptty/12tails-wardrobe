"""Headless check of TTO online (2026-11-09; user: "add TTO stuff to the public deployement ... 1. Change the pink dot to TTO
small logo instead. 2. TTO shouldn't be downloadable nor uploadable, it's preview only 3. only include released assets, I
will mark them from html picker"):
  - the picker (wardrobe/tto_picker.html, after a publish wrote wardrobe_dist_tto.json): every class tab, tiles, a click
    toggles an item, select-all / none in a section, the JSON it saves names exactly the chosen items
  - the wardrobe with ?ttolock (what the published copy does): TTO tiles carry the TTO mark (no pink dot), a TTO piece's
    menu has no download / upload actions but the preview-only note, a BB piece's menu still has them
Writes <out>/picker.png, <out>/tto_menu.png, <out>/tto_tiles.png; exit 1 on a failure or a page error.
  uv run --no-project --with playwright python -I pipeline/wardrobe_tto_check.py D:/12tails-wardrobe checks/<dir>"""
import asyncio, functools, http.server, json, sys, threading
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")
ROOT, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


http.server.ThreadingHTTPServer.request_queue_size = 128
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{srv.server_address[1]}/wardrobe/"
# the middle one of the outfit's hits (the first hit can sit on an edge the idle sway moves off: a flaky miss, 2026-11-09)
POINT = """() => { const { pieceAt, renderer } = wardrobe.debug(), r = renderer.domElement.getBoundingClientRect(), hits = [];
  for (let y = r.top + r.height * .3; y < r.bottom; y += 8) for (let x = r.left + r.width * .3; x < r.right - r.width * .2; x += 8) { const t = pieceAt(x, y); if (t?.slot === 'outfit') hits.push([x, y]); }
  return hits.length ? hits[Math.floor(hits.length / 2)] : null; }"""
MENU = "() => ({ items: [...document.querySelectorAll('#pmenu .pm-item')].map(b => b.dataset.a), lock: !!document.querySelector('#pmenu .pm-lock'), name: document.querySelector('#pmenu .pm-name')?.innerText })"


async def main():
    errors, fails = [], []
    check = lambda ok, what: (print(("ok   " if ok else "FAIL ") + what), ok or fails.append(what))
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        ctx = await b.new_context(viewport={"width": 1366, "height": 768})
        page = await ctx.new_page()
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: m.type == "error" and not m.text.startswith("Failed to load resource") and errors.append(m.text))
        # the picker asks for tto_released.json, which is missing until the first save
        page.on("response", lambda r: r.status >= 400 and not r.url.endswith("/tto_released.json") and errors.append(f"{r.status} {r.url}"))

        # the picker
        await page.goto(BASE + "tto_picker.html")
        await page.wait_for_function("window.picker", timeout=60000)
        await page.evaluate("() => localStorage.clear()"); await page.reload(); await page.wait_for_function("window.picker")
        n_items = await page.evaluate("() => picker.items.length")
        tabs = await page.locator(".tab").count()
        check(n_items > 0 and tabs >= 12, f"picker: {n_items} items, {tabs} class tabs")
        await page.click('.tab[data-c="wolf"]')
        first = page.locator('section[data-kind="outfits"] .it').first
        k = await first.get_attribute("data-k")
        was = await first.get_attribute("aria-pressed")
        await first.click()
        now = await page.locator(f'.it[data-k="{k}"]').get_attribute("aria-pressed")
        check(was != now, f"a click toggles {k}: {was} -> {now}")
        await page.click('section[data-kind="weapons"] [data-all="1"]')
        on = await page.locator('section[data-kind="weapons"] .it[aria-pressed=true]').count()
        allw = await page.locator('section[data-kind="weapons"] .it').count()
        check(on == allw, f"select all in a section: {on}/{allw}")
        out = json.loads(await page.evaluate("() => picker.output()"))
        chosen = await page.evaluate("() => [...picker.sel].sort()")
        listed = sorted(f"{c}|{kd}|{n}" for c, kinds in out.items() if not c.startswith("_") for kd, ns in kinds.items() for n in ns)
        check(listed == chosen, f"the saved JSON names exactly the {len(chosen)} chosen items")
        await page.screenshot(path=str(OUT / "picker.png"), full_page=False)
        await page.evaluate("() => localStorage.clear()")

        # the wardrobe, preview-only TTO
        await page.goto(BASE + "index.html?ttolock")
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
        await page.evaluate("() => wardrobe.show('wolf')")
        await page.click('#topics [data-t="outfit"]'); await page.wait_for_selector("#pkBody .pk-item")
        marks = await page.locator("#pkBody .tto-mark").count()
        pink = await page.locator("#pkBody .dot:not(.tto-mark):not(.tot)").count()
        check(marks > 0 and pink == 0, f"outfit picker: {marks} TTO marks, {pink} pink dots")
        await page.locator("#pkBody .tto-mark").first.scroll_into_view_if_needed()
        await page.screenshot(path=str(OUT / "tto_tiles.png"))
        await page.click("#pkClose")
        tto = await page.evaluate("() => wardrobe.debug().C.outfits.find(o => o.tto && !o.tot)?.name")
        await page.evaluate("n => wardrobe.setOutfit(n)", tto); await page.wait_for_timeout(800)
        await page.evaluate("() => wardrobe.show('wolf')"); await page.wait_for_timeout(500)
        pt = await page.evaluate(POINT)
        await page.mouse.click(*pt); await page.wait_for_timeout(300)
        m = await page.evaluate(MENU)
        check(m["items"] and not {"png", "glb", "up", "reset"} & set(m["items"]), f"TTO outfit {tto}: {m['items']} (no download / upload)")
        await page.screenshot(path=str(OUT / "tto_menu.png"))
        await page.keyboard.press("Escape")
        await page.evaluate("() => wardrobe.setOutfit('standard')"); await page.wait_for_timeout(800)
        await page.evaluate("() => wardrobe.show('wolf')"); await page.wait_for_timeout(500)
        pt = await page.evaluate(POINT)
        await page.mouse.click(*pt); await page.wait_for_timeout(300)
        m = await page.evaluate(MENU)
        check(not m["lock"] and {"png", "glb", "up"} <= set(m["items"]), f"BB outfit standard: {m['items']}")
        await b.close()
    print("errors:", errors)
    sys.exit(1 if errors or fails else 0)


asyncio.run(main())
