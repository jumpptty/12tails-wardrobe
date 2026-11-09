"""Headless check of the skill effects and sounds (2026-11-09 pilot: Wolf Armor Break, Cross Break, Grand Cross, Feral Strike). Plays
each skill tile, samples which effects are alive (and their emitters' vertex counts) over time, screenshots each skill at
the moments its effects show and at its busiest frame (peak), once per backdrop (?fxbg=dark / spot / white, side by side in <out>/compare.html), and
fails on a page error, a console error or a failed request.
  uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py D:/12tails-wardrobe checks/<dir> [dark,spot,white]"""
import asyncio, functools, http.server, sys, threading
from pathlib import Path
from playwright.async_api import async_playwright

ROOT, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
VARIANTS = (sys.argv[3] if len(sys.argv) > 3 else "dark,spot,white").split(",")
SKILLS = {"armorBreak": [0.15, 0.8], "crossBreak": [0.3, 1.35], "grandCross": [0.2, 0.75], "feralStrike": [0.15, 0.5]}   # seconds to screenshot at


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


# the stdlib server queues 5 connections; the page loads dozens of icons at once and the rest were refused
# (ERR_CONNECTION_REFUSED, 2026-11-09: data/icons/skills/emotion/beg.webp)
http.server.ThreadingHTTPServer.request_queue_size = 128
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/wardrobe/index.html"
LIVE = """() => { const { FX } = wardrobe.debug();
  return FX.live.map(f => f.name + ':' + f.emitters.reduce((s, e) => s + (f.attached(e.node) ?
    (e.node.children.find(c => c.isMesh)?.geometry.attributes.position?.count || 0) : 0), 0) + 'v'); }"""


async def main():
    errors = []
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--autoplay-policy=no-user-gesture-required"])
        page = await b.new_page(viewport={"width": 1366, "height": 768})
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: m.type == "error" and errors.append(m.text + " " + (m.location or {}).get("url", "")))
        page.on("requestfailed", lambda r: errors.append("request failed " + r.url))
        page.on("response", lambda r: r.status >= 400 and errors.append(f"{r.status} {r.url}"))
        for var in VARIANTS:
            await page.goto(URL + "?fxbg=" + var)
            await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
            await page.evaluate("c => wardrobe.show(c)", "wolf")
            await page.click('button.topic[data-t="move"]')
            await page.click('.pk-tab[data-g="skill"]')
            for skill, shots in SKILLS.items():
                if await page.locator('#picker').is_hidden():                      # reopen the move picker's skill tab
                    await page.click('button.topic[data-t="move"]')
                    await page.click('.pk-tab[data-g="skill"]')
                await page.click(f'#pkBody .pk-item[data-m="{skill}"]')
                await page.click('#pkClose') if await page.locator('#pkClose').count() else None
                t0 = await page.evaluate("() => performance.now()")
                samples, shot_i, peak = [], 0, 0
                for _ in range(80):
                    now = (await page.evaluate("() => performance.now()") - t0) / 1000
                    live = await page.evaluate(LIVE)
                    samples.append(f"{now:.2f}s " + ",".join(live))
                    total = sum(int(x.rsplit(":", 1)[1][:-1]) for x in live if ":" in x)
                    if total > peak:                                   # the frame with the most effect geometry
                        peak = total; await page.screenshot(path=str(OUT / f"{var}_{skill}_peak.png"))
                    if shot_i < len(shots) and now >= shots[shot_i]:
                        await page.screenshot(path=str(OUT / f"{var}_{skill}_{shot_i}.png")); shot_i += 1
                    if now > 2.2:
                        break
                    await page.wait_for_timeout(30)
                print(f"== {var} {skill}: " + " | ".join(samples[::3]))
        snd = await page.evaluate("() => { const { Sound } = wardrobe.debug(); return { ctx: Sound.ctx?.state, loaded: Object.keys(Sound.bufs).length }; }")
        print("sound:", snd)
        await b.close()
    rows = "".join(f"<tr><th>{s} {i}</th>" + "".join(f'<td><img src="{v}_{s}_{i}.png"></td>' for v in VARIANTS) + "</tr>"
                   for s, sh in SKILLS.items() for i in [*range(len(sh)), "peak"])
    (OUT / "compare.html").write_text("<!doctype html><meta charset=utf-8><title>Effect backdrops</title><style>body{font:14px sans-serif;"
                                      "margin:16px}img{width:100%}td{vertical-align:top}</style><table><tr><th></th>"
                                      + "".join(f"<th>{v}</th>" for v in VARIANTS) + f"</tr>{rows}</table>", encoding="utf-8")
    print("errors:", errors)
    sys.exit(1 if errors else 0)


asyncio.run(main())
