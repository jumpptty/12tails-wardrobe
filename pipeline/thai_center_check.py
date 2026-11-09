"""Is Thai text centred by eye in its box? (2026-11-09; NOTES.md "Thai text: centring by eye".) Screenshots an element at
2x and, for each text run and each child box inside it, measures the ink: the first and last pixel rows darker than the
box's background, against the box's inner edges (inside its border). Prints the gap above and below in CSS px; equal
gaps (within ~0.5 px) = centred by eye. Text runs are the element's own text nodes (Range rects); boxes are the
children matching --boxes (their own text is measured inside them too).
  uv run --no-project --with playwright --with pillow python -I pipeline/thai_center_check.py <url> <selector> [--boxes kbd] [--out shot.png]"""
import argparse, asyncio, sys
from playwright.async_api import async_playwright
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
ap = argparse.ArgumentParser()
ap.add_argument("url"); ap.add_argument("selector")
ap.add_argument("--boxes", default="kbd")
ap.add_argument("--out", default="")
A = ap.parse_args()
S = 2                                                     # device scale

GEOM = """([sel, boxes]) => { const el = document.querySelector(sel), r = el.getBoundingClientRect(), cs = getComputedStyle(el);
  const inner = el => { const r = el.getBoundingClientRect(), c = getComputedStyle(el);
    return { x: r.left + parseFloat(c.borderLeftWidth), y: r.top + parseFloat(c.borderTopWidth),
             w: r.width - parseFloat(c.borderLeftWidth) - parseFloat(c.borderRightWidth), h: r.height - parseFloat(c.borderTopWidth) - parseFloat(c.borderBottomWidth) }; };
  const runs = [];
  const walk = n => { for (const k of n.childNodes) {
    if (k.nodeType === 3 && k.textContent.trim()) { const g = document.createRange(); g.selectNodeContents(k); const q = g.getBoundingClientRect(); runs.push({ text: k.textContent.trim(), x: q.left, w: q.width }); }
    else if (k.nodeType === 1 && !k.matches(boxes) && getComputedStyle(k).display !== 'none') walk(k); } };
  walk(el);
  return { box: inner(el), runs, boxes: [...el.querySelectorAll(boxes)].map(b => ({ text: b.textContent.trim(), ...inner(b), x0: b.getBoundingClientRect().left, w0: b.getBoundingClientRect().width,
    y0: b.getBoundingClientRect().top, h0: b.getBoundingClientRect().height })), origin: { x: r.left, y: r.top } }; }"""


def ink_rows(img, x0, x1, y0, y1, bg):
    """First and last rows in [y0, y1) with a pixel clearly darker than bg, columns [x0, x1)."""
    rows = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            p = img.getpixel((x, y))
            if sum(bg) - sum(p[:3]) > 150:
                rows.append(y); break
    return (rows[0], rows[-1]) if rows else None


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        pg = await b.new_page(viewport={"width": 1366, "height": 768}, device_scale_factor=S)
        await pg.goto(A.url)
        await pg.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
        await pg.evaluate("() => document.fonts.ready"); await pg.wait_for_timeout(800)
        g = await pg.evaluate(GEOM, [A.selector, A.boxes])
        shot = await pg.screenshot()
        await b.close()
    import io
    img = Image.open(io.BytesIO(shot)).convert("RGB")
    if A.out:
        o = g["box"]; img.crop((int(o["x"] * S) - 20, int(o["y"] * S) - 20, int((o["x"] + o["w"]) * S) + 20, int((o["y"] + o["h"]) * S) + 20)).save(A.out)
    box = g["box"]
    bg = img.getpixel((int((box["x"] + 3) * S), int((box["y"] + box["h"] / 2) * S)))
    y0, y1 = int(round(box["y"] * S)), int(round((box["y"] + box["h"]) * S))

    def report(name, x, w, top, bottom, bgc):
        r = ink_rows(img, int(x * S), int((x + w) * S), top, bottom, bgc)
        if not r:
            print(f"  {name}: no ink"); return
        above, below = (r[0] - top) / S, (bottom - 1 - r[1]) / S
        print(f"  {name}: ink {above:.1f} px below the top, {below:.1f} px above the bottom -> off by {(above - below) / 2:+.1f} px "
              f"({'low' if above > below else 'high' if below > above else 'centred'})")
    print(f"box {A.selector}: inner {box['w']:.0f} x {box['h']:.1f} px")
    for run in g["runs"]:
        report(f"text '{run['text']}'", run["x"], run["w"], y0, y1, bg)
    for k in g["boxes"]:
        # the child box in the row (its outer edges), then its text inside its own inner box
        kt, kb = int(round(k["y0"] * S)), int(round((k["y0"] + k["h0"]) * S))
        print(f"  box '{k['text']}': {(kt - y0) / S:.1f} px below the row's top, {(y1 - kb) / S:.1f} px above its bottom -> off by {((kt - y0) - (y1 - kb)) / 2 / S:+.1f} px")
        # one device pixel in from the border on each side: the border's antialiased edge is not ink
        it, ib = int(round(k["y"] * S)) + 1, int(round((k["y"] + k["h"]) * S)) - 1
        kbg = img.getpixel((int((k["x"] + 1.5) * S), int((k["y"] + k["h"] / 2) * S)))
        report(f"  its text '{k['text']}'", k["x"] + 1.5, k["w"] - 3, it, ib, kbg)


asyncio.run(main())
