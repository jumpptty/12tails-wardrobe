r"""Headless check of the set ribbon's Thai text, centred by eye (2026-11-19; user: "E Ribbon, with D icon"; NOTES.md "Thai
text: centring by eye"). On the real page (the Bat, a first visit seeded through localStorage), at a desktop (1366 x 704)
and a phone (390 x 700) at 2x: the ribbon with no set (เลือกเซ็ต + the count) and with the Royal set worn (Royal + 3 ชิ้น);
in each 2x shot of the ribbon, the first and last rows with dark ink in the text's columns; the gap above and the gap below
must match within 2 device px (1 css px). The 1 px offset in index.html (.set-name, .set-meta { top: 1px }) came from
this measure. Serves the folder on a free port (never 8771). Exit 1 on a failure.
  uv run --no-project --with playwright==1.65.1 python -I -X utf8 pipeline/wardrobe_set_ribbon_check.py [<root> [<out>]]"""
import asyncio, base64, json, socket, subprocess, sys, time
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "checks" / "set_ribbon"
SAVED = {"cls": "bat", "bat": {"outfit": "royal", "color": 1, "face": 11, "edition": "", "Head": "butterflyHood", "R": None, "L": None, "Back": None, "Pet": None}}
# the first and last rows of dark ink (luminance < 95: the ribbon's gold is 150 or more) in the given columns of a PNG
INK = """async ([b64, x0, x1]) => { const im = new Image(); im.src = 'data:image/png;base64,' + b64; await im.decode();
  const c = new OffscreenCanvas(im.width, im.height), g = c.getContext('2d'); g.drawImage(im, 0, 0);
  const d = g.getImageData(0, 0, im.width, im.height).data; let top = -1, bot = -1;
  for (let y = 0; y < im.height; y++) for (let x = Math.max(0, Math.floor(x0)); x < Math.min(im.width, Math.ceil(x1)); x++) {
    const i = (y * im.width + x) * 4;
    if (.299 * d[i] + .587 * d[i + 1] + .114 * d[i + 2] < 95) { if (top < 0) top = y; bot = y; break; } }
  return { h: im.height, above: top, below: im.height - 1 - bot, top }; }"""
GEO = """() => { const b = document.querySelector('#topics button.topic[data-t="set"]'), r = b.getBoundingClientRect();
  const t = [...b.querySelectorAll('.set-name, .set-meta')].map(e => e.getBoundingClientRect());
  return { x0: Math.min(...t.map(q => q.left)) - r.left, x1: Math.max(...t.map(q => q.right)) - r.left, text: b.textContent.trim() }; }"""
fails = []


def check(ok, msg):
    print(("ok   " if ok else "FAIL ") + msg)
    if not ok:
        fails.append(msg)


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]
    srv = subprocess.Popen([sys.executable, str(ROOT / "pipeline" / "wardrobe_serve.py"), str(port)], cwd=ROOT,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.5)
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch()
            for tag, w, h in (("desktop", 1366, 704), ("phone", 390, 700)):
                ctx = await b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2)
                await ctx.add_init_script(f"localStorage.setItem('wardrobe_v1', JSON.stringify({json.dumps(SAVED)}))")
                pg = await ctx.new_page()
                await pg.goto(f"http://127.0.0.1:{port}/wardrobe/")
                await pg.wait_for_function("() => window.wardrobe && wardrobe.debug().C && wardrobe.debug().C.sets", timeout=120000)
                await pg.evaluate("() => document.fonts.ready")
                for state in ("none", "worn"):
                    if state == "worn":                      # the Royal set's pieces on; the set picker opened and closed redraws the panel
                        await pg.evaluate("() => wardrobe.show('bat', { R: 'royalWand', Head: 'royalCirclet' }, 0)")
                        await pg.evaluate("() => wardrobe.debug().openPicker('set')")
                        await pg.wait_for_timeout(500)
                        await pg.click("#pkClose")
                    geo = await pg.evaluate(GEO)
                    png = await pg.locator('#topics button.topic[data-t="set"]').screenshot(path=str(OUT / f"ribbon_{tag}_{state}.png"))
                    ink = await pg.evaluate(INK, [base64.b64encode(png).decode(), geo["x0"] * 2, geo["x1"] * 2])
                    want = "Royal" in geo["text"] if state == "worn" else "เลือกเซ็ต" in geo["text"]
                    check(want and ink["top"] >= 0 and abs(ink["above"] - ink["below"]) <= 2,
                          f"{tag:7} {state:4} {geo['text']!r}: {ink['above']} px above the ink, {ink['below']} below (2x, of {ink['h']})")
                await ctx.close()
            await b.close()
    finally:
        srv.terminate()
    sys.exit(1 if fails else 0)


asyncio.run(main())
