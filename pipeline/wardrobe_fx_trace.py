"""QA trace (2026-11-10): plays one tile and logs, every frame, each live effect whose name matches a regex: its age, its
root's position in the effect's own (Unity world) space and how many vertices its meshes hold, and its materials' opacity (AlphaTimer).
  uv run --no-project --with playwright python -I pipeline/wardrobe_fx_trace.py <repo> <cls> <tile> <regex> [seconds]"""
import asyncio, functools, http.server, sys, threading
from pathlib import Path

ROOT, CLS, TILE, RX = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
SECS = float(sys.argv[5]) if len(sys.argv) > 5 else 3


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


http.server.ThreadingHTTPServer.request_queue_size = 128
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/wardrobe/index.html?fxbg=dark"


async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--autoplay-policy=no-user-gesture-required"])
        page = await b.new_page(viewport={"width": 1366, "height": 768})
        page.on("console", lambda m: m.type in ("error", "warning") and "GL Driver" not in m.text and print("console", m.type, m.text))
        page.on("pageerror", lambda e: print("pageerror", e))
        await page.goto(URL)
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
        await page.evaluate("c => wardrobe.show(c)", CLS)
        await page.wait_for_function("c => wardrobe.debug().C?.cls === c && wardrobe.debug().FX.cueTab[c]", arg=CLS, timeout=120000)
        await page.click('button.topic[data-t="move"]')
        for g in ("skill", "emotion", "base"):
            if await page.locator(f'.pk-tab[data-g="{g}"]').count():
                await page.click(f'.pk-tab[data-g="{g}"]')
                if await page.locator(f'#pkBody .pk-item[data-m="{TILE}"]').count():
                    break
        await page.evaluate("""rx => { window.__log = []; const { FX } = wardrobe.debug(), t0 = performance.now(), re = new RegExp(rx);
          const f = () => { const t = (performance.now() - t0) / 1000;
            for (const x of FX.live) if (re.test(x.name)) { let v = 0, op = []; x.group.traverse(o => { v += o.geometry?.attributes?.position?.count || 0; if (o.isMesh && !Array.isArray(o.material) && o.material.userData?.fxBlend) op.push(o.material.opacity.toFixed(2)); });
              const p = x.root.position; window.__log.push(`${t.toFixed(3)} ${x.name} age ${x.age.toFixed(3)} root ${p.x.toFixed(2)},${p.y.toFixed(2)},${p.z.toFixed(2)} s ${x.root.scale.x.toFixed(2)} v ${v} vis ${x.group.visible} op ${op.join('/')}`); }
            if (t < 30) requestAnimationFrame(f); };
          requestAnimationFrame(f); }""", RX)
        await page.click(f'#pkBody .pk-item[data-m="{TILE}"]')
        await page.wait_for_timeout(int(SECS * 1000))
        for line in await page.evaluate("() => window.__log"):
            print(line)
        await b.close()


asyncio.run(main())
