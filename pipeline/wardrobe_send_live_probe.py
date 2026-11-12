"""Probe the live site's send dialog (2026-11-12): the public page exposes wardrobe.debug() only to automated browsers
(navigator.webdriver), so this headless run puts a skin on the Sheep's BB mothLatern, opens ส่งลายนี้ให้ทีมงาน, fills it
and prints Send's state (cur / busy / token) before and after a submit. It does not send unless Turnstile passes.
  uv run --no-project --with playwright python -I pipeline/wardrobe_send_live_probe.py [url]"""
import asyncio, json, sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")
URL = sys.argv[1] if len(sys.argv) > 1 else "https://12tails-wardrobe.jumpthai.workers.dev/"
STATE = """() => { const S = wardrobe.debug().Send; return { cur: !!S.cur, busy: S.busy, token: S.token.length, widget: S.widget,
  msg: document.querySelector('.send-msg')?.textContent ?? null, open: !!document.querySelector('.send-back:not([hidden]) form.send') }; }"""


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        page = await (await b.new_context(viewport={"width": 1366, "height": 768})).new_page()
        page.on("console", lambda m: print("console:", m.type, m.text[:200]))
        page.on("pageerror", lambda e: print("pageerror:", e))
        page.on("request", lambda r: "api/submit" in r.url and print("request:", r.method, r.url))
        await page.goto(URL)
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
        await page.evaluate("() => wardrobe.show('sheep', { R: 'mothLatern' })")
        await page.evaluate("""() => { const { SKINS, C } = wardrobe.debug(); const w = 128, h = 128;
          SKINS.set(`${C.cls}|weapons|mothLatern|Sheep_mothLantern.png`, { w, h, data: new Uint8ClampedArray(w * h * 4).fill(200) }); }""")
        if not await page.locator('#pkBody .pk-cell[data-slot="R"]').count():
            await page.click('#topics [data-t="R"]')
        cell = page.locator('#pkBody .pk-cell[data-item="mothLatern"]').first
        await cell.scroll_into_view_if_needed(); await cell.click(button="right"); await page.wait_for_timeout(300)
        items = await page.evaluate("() => [...document.querySelectorAll('#pmenu .pm-item')].map(b => b.dataset.a)")
        print("menu:", items)
        await page.click('#pmenu .pm-item[data-a="send"]')
        await page.wait_for_selector(".send-back:not([hidden]) form.send")
        print("after open:", json.dumps(await page.evaluate(STATE)))
        dlg = page.locator("form.send")
        await dlg.locator('input[name="name"]').fill("probe")
        await dlg.locator('input[name="consent"]').check()
        print("after fill:", json.dumps(await page.evaluate(STATE)))
        try:
            await page.wait_for_function("() => wardrobe.debug().Send.token", timeout=20000)
        except Exception:
            print("no Turnstile token in headless (expected with a real key); submitting anyway to see the message")
        await dlg.locator('button[type="submit"]').click(); await page.wait_for_timeout(3000)
        print("after submit:", json.dumps(await page.evaluate(STATE)))
        await b.close()

asyncio.run(main())
