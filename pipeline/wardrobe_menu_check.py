"""Headless check of the piece menu and the hover (2026-11-09; user: "hover and click at each individual item in the model
directly, with mild hover effect, clicking at each piece will then show basic info of that item and dropdown list of
actions download upload, view this item only, etc."). On the Wolf with a hat and a main-hand weapon worn:
  - hover: the piece under the mouse is lit (Hover.slot), the cursor a pointer, nothing lit off the model; shots of the
    three looks (?hover=gold / lift / dim) side by side in <out>/hover.html
  - a click on each piece opens its menu (head: name + slot; the actions), inside the window; a drag opens nothing
  - the actions: ดาวน์โหลดลาย (a PNG download), ดาวน์โหลดโมเดล 3D (a .glb download), อัปโหลดลาย (the file chooser; the skin
    goes on, the tile's ลายของคุณ badge shows), คืนลายเดิม, ถอดออก (one undo step), ดูชิ้นนี้อย่างเดียว (the viewer; its card's
    ตัวเลือก opens the same menu without "view"; Esc closes the menu, then the viewer)
  - a right-click on a picker tile not worn: the menu with ใส่ชิ้นนี้, which wears it
  - keyboard: Shift+F10 on a focused tile opens the menu under it, arrows move, Esc closes and gives the focus back
  - a phone-sized window: a tap opens the menu inside the screen
  - no tile tools and no toolbar ชมชิ้นส่วน left; no page / console errors
Exit 1 on any failure.
  uv run --no-project --with playwright python -I pipeline/wardrobe_menu_check.py D:/12tails-wardrobe checks/<dir>"""
import asyncio, functools, http.server, sys, threading
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")       # Thai and the menu's · on any console
ROOT, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


http.server.ThreadingHTTPServer.request_queue_size = 128     # the page loads dozens of icons at once
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/wardrobe/index.html"
# a screen point on each worn piece, found with the page's own ray (pieceAt): the point nearest each piece's middle
POINTS = """() => { const { pieceAt, renderer } = wardrobe.debug(), r = renderer.domElement.getBoundingClientRect(), hits = {};
  for (let y = r.top + 8; y < r.bottom; y += 10) for (let x = r.left + 8; x < r.right; x += 10) {
    const t = pieceAt(x, y); if (t) (hits[t.slot] ||= []).push([x, y]); }
  const out = {};
  for (const [s, ps] of Object.entries(hits)) { const cx = ps.reduce((a, p) => a + p[0], 0) / ps.length, cy = ps.reduce((a, p) => a + p[1], 0) / ps.length;
    out[s] = ps.reduce((b, p) => (Math.hypot(p[0] - cx, p[1] - cy) < Math.hypot(b[0] - cx, b[1] - cy) ? p : b)); }
  return out; }"""
MENU = """() => { const el = document.getElementById('pmenu'), r = el.getBoundingClientRect();
  return { open: !el.hidden, name: el.querySelector('.pm-name')?.innerText, meta: el.querySelector('.pm-meta')?.innerText,
    items: [...el.querySelectorAll('.pm-item')].map(b => b.dataset.a + (b.dataset.tex ? ':' + b.dataset.tex : '') + (b.disabled ? '(off)' : '')),
    from: wardrobe.debug().PM.cur?.from, inside: r.left >= 0 && r.top >= 0 && r.right <= innerWidth && r.bottom <= innerHeight,
    focus: document.activeElement?.className }; }"""
STATE = "() => { const { C, SKINS, Showcase, Hover } = wardrobe.debug(); return { Head: C.state.Head, R: C.state.R, skins: SKINS.size, viewer: Showcase.on, hover: Hover.slot, cursor: C && document.querySelector('canvas').style.cursor }; }"


async def main():
    errors, fails = [], []
    check = lambda ok, what: (print(("ok   " if ok else "FAIL ") + what), ok or fails.append(what))
    tiny = OUT / "skin.png"
    import struct, zlib                    # a 4 x 4 red PNG, written here
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    tiny.write_bytes(bytes.fromhex("89504e470d0a1a0a") + chunk(b"IHDR", struct.pack(">IIBBBBB", 4, 4, 8, 6, 0, 0, 0))
                     + chunk(b"IDAT", zlib.compress(bytes.fromhex("00" + "ff0000ff" * 4) * 4)) + chunk(b"IEND", b""))
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        ctx = await b.new_context(viewport={"width": 1366, "height": 768}, accept_downloads=True)
        page = await ctx.new_page()
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: m.type == "error" and errors.append(m.text + " " + (m.location or {}).get("url", "")))
        page.on("requestfailed", lambda r: errors.append("request failed " + r.url))
        await page.goto(URL)
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
        await page.evaluate("() => wardrobe.show('wolf')")
        check(await page.locator("#vmode").count() == 0, "no toolbar ชมชิ้นส่วน button")

        # dress: a hat and a main-hand weapon through the pickers (the second tile of each: the first is ไม่ใส่)
        for topic in ("Head", "R"):
            await page.click(f'#topics [data-t="{topic}"]')
            await page.wait_for_selector("#pkBody .pk-cell")
            check(await page.locator("#pkBody .sk, #pkBody .pk-skin").count() == 0, f"{topic} picker: no tile tools")
            await page.locator("#pkBody .pk-cell .pk-item").first.click()
            await page.wait_for_timeout(600)
        await page.click("#pkClose")
        await page.evaluate("() => { const { C } = wardrobe.debug(); wardrobe.show('wolf'); }")
        await page.wait_for_timeout(800)
        st = await page.evaluate(STATE)
        check(st["Head"] and st["R"], f"dressed: Head {st['Head']}, R {st['R']}")
        pts = await page.evaluate(POINTS)
        check({"outfit", "Head", "R"} <= set(pts), f"pieces on screen: {sorted(pts)}")

        # hover
        for slot, (x, y) in pts.items():
            await page.mouse.move(x, y); await page.wait_for_timeout(250)
            st = await page.evaluate(STATE)
            check(st["hover"] == slot and st["cursor"] == "pointer", f"hover {slot}: lit {st['hover']}, cursor {st['cursor']!r}")
        await page.mouse.move(1340, 120); await page.wait_for_timeout(250)     # empty stage
        check((await page.evaluate(STATE))["hover"] is None, "hover off the model: nothing lit")

        # click -> menu, per piece
        for slot, (x, y) in pts.items():
            await page.mouse.click(x, y); await page.wait_for_timeout(200)
            m = await page.evaluate(MENU)
            check(m["open"] and m["from"] == "model" and m["inside"] and m["name"], f"click {slot}: menu {m['name']!r} [{m['meta']}] {m['items']}")
            await page.screenshot(path=str(OUT / f"menu_{slot}.png"))
            await page.keyboard.press("Escape"); await page.wait_for_timeout(100)
        check(not (await page.evaluate(MENU))["open"], "Esc closes the menu")
        x, y = pts["outfit"]
        await page.mouse.move(x, y); await page.mouse.down(); await page.mouse.move(x + 60, y, steps=6); await page.mouse.up()
        await page.wait_for_timeout(200)
        check(not (await page.evaluate(MENU))["open"], "a drag on the model opens no menu")
        pts = await page.evaluate(POINTS)                  # the drag turned the camera

        async def menu_on(slot):
            x, y = pts[slot]; await page.mouse.click(x, y); await page.wait_for_timeout(200)
            return await page.evaluate(MENU)

        # downloads
        await menu_on("Head")
        async with page.expect_download() as d:
            await page.locator('#pmenu .pm-item[data-a="png"]').first.click()
        name = (await d.value).suggested_filename
        check(name.endswith(".png"), f"ดาวน์โหลดลาย: {name}")
        await menu_on("R")
        async with page.expect_download(timeout=60000) as d:
            await page.click('#pmenu .pm-item[data-a="glb"]')
        name = (await d.value).suggested_filename
        check(name.endswith(".glb"), f"ดาวน์โหลดโมเดล 3D: {name}")

        # upload -> skin on, badge on the tile; reset
        await menu_on("Head")
        async with page.expect_file_chooser() as fc:
            await page.locator('#pmenu .pm-item[data-a="up"]').first.click()
        await (await fc.value).set_files(str(tiny))
        try:
            await page.wait_for_function("() => wardrobe.debug().SKINS.size === 1", timeout=15000)
        except Exception:
            print("   toast:", await page.evaluate("() => document.getElementById('toast').innerText"), "errors:", errors)
        check((await page.evaluate(STATE))["skins"] == 1, "อัปโหลดลาย: the skin is on")
        if fails: print("errors:", errors); sys.exit(1)
        m = await menu_on("Head")
        check(any(i.startswith("reset") for i in m["items"]) and "ลายของคุณ" in (m["meta"] or ""), "the menu shows ลายของคุณ and คืนลายเดิม")
        await page.click('#pmenu .pm-item[data-a="reset"]'); await page.wait_for_timeout(500)
        check((await page.evaluate(STATE))["skins"] == 0, "คืนลายเดิม: the skin is off")

        # remove + undo
        head = (await page.evaluate(STATE))["Head"]
        await menu_on("Head"); await page.click('#pmenu .pm-item[data-a="remove"]'); await page.wait_for_timeout(500)
        check((await page.evaluate(STATE))["Head"] is None, "ถอดหมวกออก: the hat is off")
        await page.keyboard.press("Control+z"); await page.wait_for_timeout(800)
        check((await page.evaluate(STATE))["Head"] == head, "Ctrl+Z puts it back (one undo step)")
        pts = await page.evaluate(POINTS)

        # view this item only -> viewer; its card's ตัวเลือก
        await menu_on("R"); await page.click('#pmenu .pm-item[data-a="view"]')
        await page.wait_for_function("() => wardrobe.debug().Showcase.phase === 'on'", timeout=30000)
        await page.wait_for_timeout(500)
        await page.click('#showcase .sc-b[data-a="menu"]'); await page.wait_for_timeout(200)
        m = await page.evaluate(MENU)
        check(m["open"] and m["from"] == "viewer" and not any(i.startswith("view") for i in m["items"]) and m["inside"], f"viewer ตัวเลือก: {m['items']}")
        await page.screenshot(path=str(OUT / "menu_viewer.png"))
        await page.keyboard.press("Escape"); await page.wait_for_timeout(150)
        st = await page.evaluate(STATE)
        check(not (await page.evaluate(MENU))["open"] and st["viewer"], "Esc closes the menu first, the viewer stays")
        await page.keyboard.press("Escape"); await page.wait_for_timeout(1500)
        check(not (await page.evaluate(STATE))["viewer"], "the second Esc closes the viewer")

        # a double-click on a piece still opens the viewer, with no menu left behind
        pts = await page.evaluate(POINTS)
        await page.mouse.dblclick(*pts["outfit"])
        await page.wait_for_function("() => wardrobe.debug().Showcase.phase === 'on'", timeout=30000)
        check(not (await page.evaluate(MENU))["open"], "double-click: the viewer opens, no menu left open")
        await page.keyboard.press("Escape"); await page.wait_for_timeout(1500)

        # right-click a tile not worn -> ใส่ชิ้นนี้
        await page.click('#topics [data-t="Head"]'); await page.wait_for_selector("#pkBody .pk-cell")
        cells = page.locator("#pkBody .pk-cell")
        target = cells.nth(3)
        it = await target.get_attribute("data-item")
        await target.click(button="right"); await page.wait_for_timeout(200)
        m = await page.evaluate(MENU)
        check(m["open"] and m["from"] == "tile" and "wear" in m["items"] and m["inside"], f"right-click tile {it}: {m['items']}")
        await page.screenshot(path=str(OUT / "menu_tile.png"))
        await page.click('#pmenu .pm-item[data-a="wear"]'); await page.wait_for_timeout(700)
        check((await page.evaluate(STATE))["Head"] == it, f"ใส่ชิ้นนี้ wears {it}")

        # keyboard: Shift+F10 on a focused tile, arrows, Esc gives the focus back
        await cells.nth(4).locator(".pk-item").focus()
        await page.keyboard.press("Shift+F10"); await page.wait_for_timeout(200)
        m = await page.evaluate(MENU)
        check(m["open"] and "pm-item" in (m["focus"] or ""), f"Shift+F10: menu open, focus on {m['focus']!r}")
        await page.keyboard.press("ArrowDown")
        f2 = await page.evaluate("() => document.activeElement.dataset.a")
        await page.keyboard.press("Escape"); await page.wait_for_timeout(100)
        back = await page.evaluate("() => document.activeElement.closest('.pk-cell')?.dataset.item")
        check(f2 and back == await cells.nth(4).get_attribute("data-item"), f"arrows move ({f2}), Esc returns the focus to the tile ({back})")
        check(await page.locator("#picker").is_visible(), "Esc in the menu leaves the picker open")
        await page.click("#pkClose")

        # Space pauses / resumes the animation (after a pointer click; a new move resumes it)
        await page.mouse.click(1340, 140); await page.wait_for_timeout(200)
        mt = "() => wardrobe.debug().C.mixer.time"
        await page.keyboard.press("Space"); await page.wait_for_timeout(300)
        a = await page.evaluate(mt); await page.wait_for_timeout(500); b2 = await page.evaluate(mt)
        hint = await page.evaluate("() => document.getElementById('khPause').textContent")
        check(a == b2 and hint == "เล่นต่อ", f"Space pauses: mixer {a:.3f} -> {b2:.3f}, hint {hint!r}")
        await page.keyboard.press("Space"); await page.wait_for_timeout(500)
        check(await page.evaluate(mt) > b2, "Space again resumes")
        await page.keyboard.press("Space"); await page.wait_for_timeout(200)
        await page.evaluate("() => wardrobe.show('wolf')")      # plays the idle: a new move resumes
        c0 = await page.evaluate(mt); await page.wait_for_timeout(500)
        check(await page.evaluate(mt) > c0, "a new move resumes a paused animation")
        # R: back to the idle stance from another move
        await page.click('#topics [data-t="move"]'); await page.click('.pk-tab[data-g="emote"]')
        await page.locator('#pkBody .pk-item').first.click(); await page.click("#pkClose"); await page.wait_for_timeout(300)
        before = await page.evaluate("() => wardrobe.debug().C.cur")
        await page.mouse.click(1340, 140); await page.keyboard.press("r"); await page.wait_for_timeout(300)
        after = await page.evaluate("() => wardrobe.debug().C.cur")
        check(before != after and after.lower() == "root", f"R: {before} -> {after}")

        # hover looks side by side
        rows = []
        for look in ("gold", "lift", "dim"):
            await page.goto(URL + "?hover=" + look)
            await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
            await page.evaluate("() => wardrobe.show('wolf')"); await page.wait_for_timeout(800)
            pts2 = await page.evaluate(POINTS)
            for slot in ("outfit", "Head", "R"):
                if slot not in pts2: continue
                await page.mouse.move(*pts2[slot]); await page.wait_for_timeout(300)
                await page.screenshot(path=str(OUT / f"hover_{look}_{slot}.png"), clip={"x": 560, "y": 60, "width": 700, "height": 640})
            await page.mouse.move(1340, 120); await page.wait_for_timeout(300)
            await page.screenshot(path=str(OUT / f"hover_{look}_none.png"), clip={"x": 560, "y": 60, "width": 700, "height": 640})
        for slot in ("none", "outfit", "Head", "R"):
            rows.append(f"<tr><th>{slot}</th>" + "".join(f'<td><img src="hover_{l}_{slot}.png"></td>' for l in ("gold", "lift", "dim")) + "</tr>")
        (OUT / "hover.html").write_text("<!doctype html><meta charset=utf-8><title>Hover looks</title><style>body{font:14px sans-serif;margin:16px}"
                                        "img{width:100%}</style><table><tr><th></th><th>gold (default)</th><th>lift</th><th>dim</th></tr>"
                                        + "".join(rows) + "</table>", encoding="utf-8")

        # phone: a tap opens the menu inside the screen
        ph = await b.new_context(viewport={"width": 390, "height": 700}, has_touch=True, is_mobile=True)
        pp = await ph.new_page()
        pp.on("pageerror", lambda e: errors.append("phone: " + str(e)))
        await pp.goto(URL)
        await pp.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
        await pp.evaluate("() => wardrobe.show('wolf')"); await pp.wait_for_timeout(800)
        pp_pts = await pp.evaluate(POINTS)
        if "outfit" in pp_pts:
            await pp.touchscreen.tap(*pp_pts["outfit"]); await pp.wait_for_timeout(300)
            m = await pp.evaluate(MENU)
            check(m["open"] and m["inside"], f"phone tap: menu open {m['open']}, inside the screen {m['inside']}")
            await pp.screenshot(path=str(OUT / "phone_menu.png"))
        else:
            check(False, "phone: the outfit is on screen")
        await b.close()
    print("errors:", errors)
    sys.exit(1 if errors or fails else 0)


asyncio.run(main())
