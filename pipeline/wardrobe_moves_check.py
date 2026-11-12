"""Headless check of the wardrobe's move player (2026-11-09): every class's skill / base tiles to <out>/tiles.json, a
screenshot of the Sheep's skill tab, every class's parsed sequences with their step times to <out>/chains.json, then
timed traces (step:clip@seconds since the pick) of the Sheep's sequences, the Wolf's Blade Song and Blade Fang, the
Bison's Charge Attack and the Chameleon's Quick Fire (max rank), ko holding, run / falling looping, getUp back to idle.
uv run --no-project --with playwright python -I pipeline/wardrobe_moves_check.py D:/12tails-wardrobe checks/<dir> [page path]"""
import asyncio, functools, http.server, json, sys, threading
from pathlib import Path
from playwright.async_api import async_playwright

ROOT, OUT = Path(sys.argv[1]), Path(sys.argv[2])
PAGE = sys.argv[3] if len(sys.argv) > 3 else "wardrobe/index.html"
OUT.mkdir(parents=True, exist_ok=True)


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


# the stdlib server queues 5 connections; the page loads dozens of icons at once and the rest were refused
# (ERR_CONNECTION_REFUSED, 2026-11-09: data/icons/skills/emotion/beg.webp)
http.server.ThreadingHTTPServer.request_queue_size = 128
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/{PAGE}"

STATE = """() => { const { C } = wardrobe.debug(); const a = C.action;
  return { cur: C.cur, i: C.seq?.i, clip: a?.getClip().name, t: +(a?.time ?? 0).toFixed(2), paused: a?.paused, dur: C.seq?.dur, now: performance.now() }; }"""


async def trace(page, move, secs, step=0.05):
    seen, last, t0 = [], None, None
    for _ in range(int(secs / step)):
        s = await page.evaluate(STATE)
        t0 = s["now"] if t0 is None else t0
        key = (s["clip"], s["i"])
        if key != last:
            seen.append(f'{s["i"]}:{s["clip"]}@{(s["now"] - t0) / 1000:.1f}')
            last = key
        await page.wait_for_timeout(int(step * 1000))
    return seen, await page.evaluate(STATE)


async def main():
    errors = []
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        page = await b.new_page(viewport={"width": 1366, "height": 607})
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: m.type == "error" and errors.append(m.text + " " + (m.location or {}).get("url", "")))
        await page.goto(URL)
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
        async def tab(g):
            if not await page.evaluate("() => !document.getElementById('picker').hidden && document.getElementById('pkBody').dataset.topic === 'move'"):
                await page.click('button.topic[data-t="move"]')
            await page.click(f'.pk-tab[data-g="{g}"]')
            await page.wait_for_timeout(150)
        async def tiles():
            return await page.evaluate("() => [...document.querySelectorAll('#pkBody .pk-item')].map(b => b.dataset.m + '=' + b.querySelector('.lbl').textContent + (b.title ? ' [' + b.title + ']' : ''))")
        report, seqs = {}, {}
        for cls in ["bat", "bison", "cat", "chameleon", "mole", "monkey", "panda", "penguin", "rabbit", "whale", "wolf", "sheep"]:
            await page.evaluate("c => wardrobe.show(c)", cls)
            await tab("skill"); sk = await tiles()
            await tab("base"); bs = await tiles()
            report[cls] = {"skill": sk, "base": bs}
            seqs[cls] = await page.evaluate("() => (wardrobe.debug().C.chains || []).map(c => c.name + ': ' + c.steps.map(s => (s.alts || [s]).map(a => a.clip + (a.hold ? '*' : '') + (a.t != null ? '@' + a.t : '')).join('|')).join(' '))")
        (OUT / "tiles.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
        (OUT / "chains.json").write_text(json.dumps(seqs, ensure_ascii=False, indent=1), encoding="utf-8")
        async def run(g, m, secs):
            await tab(g)
            await page.click(f'#pkBody .pk-item[data-m="{m}"]')
            seen, end = await trace(page, None, secs)
            print(f"{m:16} {' '.join(seen)}  | end {end}")
        await tab("skill")
        await page.screenshot(path=str(OUT / "sheep_skill.png"))
        await run("skill", "@HolyLight", 11)
        await run("skill", "@ChargeAttack", 8)
        await run("skill", "@NormalAttack", 4)
        await run("skill", "@SoulofArms", 2)               # 2026-11-10 decision 16: cast1 > cast2 (0 s) > soulOfArms
        await run("skill", "@SealofAttack", 1.5)           # decision 17: cast3 alone, cut in ("!")
        await run("base", "ko", 3)
        await run("base", "run", 2)
        await run("base", "falling", 1.5)
        await run("base", "getUp", 3)
        await run("emote", "bow", 3.5)
        await page.evaluate("c => wardrobe.show(c)", "wolf")
        await run("skill", "@BladeSong", 9)               # max rank (2026-11-09): bladeSong3 @3.1, bladeSong4
        await run("skill", "@BladeFang", 3.5)             # 1 -> 2 (0.2) -> 3 (0.5) -> 2 (0.8)
        await run("skill", "@Counter", 2.5)
        for cls, m, secs in (("bison", "@ChargeAttack", 12), ("chameleon", "@QuickFire", 3.5)):
            await page.evaluate("c => wardrobe.show(c)", cls)
            await run("skill", m, secs)
        for cls, low in (("wolf", ["bladeSong1", "bladeSong2"]), ("bison", ["cAttack3", "cAttack4", "cAttack5"])):
            await page.evaluate("c => wardrobe.show(c)", cls)
            await tab("skill")
            shown = [t.split("=")[0] for t in await tiles()]
            listed = [m for m in low if m in shown]
            print(f"{cls}: {len(shown)} skill tiles, lower-rank clips listed: {listed}")
            if listed or not shown: errors.append(f"{cls} lists lower-rank clips {listed}")
        print(json.dumps(report, ensure_ascii=False)[:200])
        print("errors:", errors)
        await b.close()


asyncio.run(main())
