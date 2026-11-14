"""Headless check of the one weapon topic (2026-11-14; user: "having 2 weapons slot is confusing to the users, merge the 2
slots to one which applies both main and sub weapon"). The page's อาวุธ topic replaced อาวุธหลัก + อาวุธที่ 2; a pick puts on
the game's whole weapon (index.html weaponOf / setWeapon). Checked against the rules worked out here apart from the page:
  - item_map.json's two-piece codes (Chameleon bow + arrow, Whale lance + shield): first piece R, second L; ToT's student
    pieces (no code) bow -> arrow, lance -> shield;
  - <name>_L / _R pieces (Panda's gloves, the Wolf's hallowSaw / specialSword): each in its hand;
  - the Wolf's other swords in both hands; every other weapon R only.
For every class: the panel has one weapon topic named อาวุธ and no L topic; the picker's tiles = one per weapon (its R
piece); the page's weaponOf agrees for every tile; picking a two-handed one wears both hands (C.props too); ไม่ใส่ takes both
off; one undo step brings both back. On the Chameleon: a click on the arrow on the model opens its menu with อีกชิ้นของ
อาวุธนี้ (opening the bow's menu) and ถอดอาวุธออก (both hands off). Shots of the panel in <out>: desktop, a short screen,
a phone. No page / console errors. Exit 1 on any failure.
  uv run --no-project --with playwright python -I pipeline/wardrobe_weapon_slot_check.py D:/12tails-wardrobe checks/<dir>"""
import asyncio, functools, http.server, json, re, sys, threading
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")
ROOT, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
DATA = ROOT / "wardrobe" / "data"
CLASSES = ["bat", "bison", "cat", "chameleon", "mole", "monkey", "panda", "penguin", "rabbit", "sheep", "whale", "wolf"]
TOT_PAIRS = {"studentBow": "studentArrow", "studentLance": "studentShield"}   # ToT's student weapons (NOTES.md 2026-11-0x ToT)


def expected(cls):
    """{tile (R piece or a lone piece): (R, L)} by the game's rules, from the class's weapon list and item_map.json."""
    names = [p["name"] for p in json.loads((DATA / cls / "props_weapons.json").read_text(encoding="utf-8"))]
    have = set(names)
    pair_of, first_of = {}, {}
    for ms in json.loads((DATA / "item_map.json").read_text(encoding="utf-8")).get(cls, {}).get("weapon", {}).values():
        if len(ms) == 2:
            pair_of.setdefault(ms[0], ms[1]); first_of.setdefault(ms[1], ms[0])
    for a, b in TOT_PAIRS.items():
        if a in have and b in have and a not in pair_of and b not in first_of:
            pair_of[a], first_of[b] = b, a
    out = {}
    for n in names:
        m = re.match(r"^(.*)_([LRlr])$", n)
        if m:
            hand = lambda h: next((x for x in (f"{m[1]}_{h}", f"{m[1]}_{h.lower()}") if x in have), None)
            r, l = hand("R"), hand("L")
        elif n in pair_of:
            r, l = n, pair_of[n]
        elif n in first_of:
            r, l = first_of[n], n
        else:
            r, l = n, (n if cls == "wolf" else None)
        if (r or n) == n:
            out[n] = (r, l)
    return out


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


http.server.ThreadingHTTPServer.request_queue_size = 128
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/wardrobe/index.html"
STATE = "() => { const { C } = wardrobe.debug(); return { R: C.state.R || null, L: C.state.L || null, pR: !!C.props.R, pL: !!C.props.L }; }"
POINTS = """() => { const { pieceAt, renderer } = wardrobe.debug(), r = renderer.domElement.getBoundingClientRect(), hits = {};
  for (let y = r.top + 6; y < r.bottom; y += 6) for (let x = r.left + 6; x < r.right; x += 6) {
    const t = pieceAt(x, y); if (t) (hits[t.slot] ||= []).push([x, y]); }
  const out = {};
  for (const [s, ps] of Object.entries(hits)) { const cx = ps.reduce((a, p) => a + p[0], 0) / ps.length, cy = ps.reduce((a, p) => a + p[1], 0) / ps.length;
    out[s] = ps.reduce((b, p) => (Math.hypot(p[0] - cx, p[1] - cy) < Math.hypot(b[0] - cx, b[1] - cy) ? p : b)); }
  return out; }"""


async def main():
    errors, fails = [], []
    check = lambda ok, what: (print(("ok   " if ok else "FAIL ") + what), ok or fails.append(what))
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        ctx = await b.new_context(viewport={"width": 1920, "height": 1200})
        page = await ctx.new_page()
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: m.type == "error" and errors.append(m.text + " " + (m.location or {}).get("url", "")))
        page.on("requestfailed", lambda r: errors.append("request failed " + r.url))
        await page.goto(URL)
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)

        async def open_weapons():
            if await page.evaluate("() => document.getElementById('picker').hidden || document.querySelector('#pkBody').dataset.topic !== 'R'"):
                await page.click('#topics [data-t="R"]')
            await page.wait_for_selector('#pkBody[data-topic="R"] .pk-cell')

        for cls in CLASSES:
            await page.evaluate(f"() => wardrobe.show('{cls}', {{ R: null, L: null }})")
            await page.wait_for_timeout(200)
            topics = await page.evaluate("() => [...document.querySelectorAll('#topics [data-t]')].map(b => b.dataset.t)")
            name = await page.inner_text('#topics [data-t="R"] .tname')
            check("L" not in topics and name == "อาวุธ", f"{cls}: one weapon topic ({name}), no L topic")
            await open_weapons()
            tiles = await page.evaluate("() => [...document.querySelectorAll('#pkBody .pk-cell')].map(c => c.dataset.item)")
            exp = expected(cls)
            check(set(tiles) == set(exp) and len(tiles) == len(exp),
                  f"{cls}: {len(tiles)} tiles = {len(exp)} weapons" + ("" if set(tiles) == set(exp) else
                  f" (extra {sorted(set(tiles) - set(exp))[:4]}, missing {sorted(set(exp) - set(tiles))[:4]})"))
            got = await page.evaluate("ns => Object.fromEntries(ns.map(n => { const w = wardrobe.debug().weaponOf(n); return [n, [w.R, w.L]]; }))", tiles)
            bad = [f"{n}: page {got[n]} want {list(exp[n])}" for n in tiles if n in exp and tuple(got[n]) != exp[n]]
            check(not bad, f"{cls}: every tile's hands match the game's rule" + (f" ({bad[:3]})" if bad else ""))
            # wear a two-handed weapon (else any), by a click on its tile; then ไม่ใส่; then undo
            two = "royalSword" if cls == "wolf" else (next((n for n in tiles if exp.get(n, (0, 0))[1] and exp[n][1] != n), None) or tiles[1])
            await page.click(f'#pkBody .pk-cell[data-item="{two}"] .pk-item')
            await page.wait_for_function(f"() => wardrobe.debug().C.state.R === {json.dumps(exp[two][0])}", timeout=30000)
            st = await page.evaluate(STATE)
            want = exp[two]
            check((st["R"], st["L"]) == want and st["pR"] == bool(want[0]) and st["pL"] == bool(want[1]),
                  f"{cls}: the {two} tile wears R {st['R']} + L {st['L']} (want {want[0]} + {want[1]})")
            pressed = await page.evaluate("() => [...document.querySelectorAll('#pkBody .pk-item[aria-pressed=true]')].map(b => b.closest('.pk-cell')?.dataset.item || 'none')")
            check(pressed == [two], f"{cls}: only its tile is pressed ({pressed})")
            if cls in ("chameleon", "whale", "panda", "wolf"):
                await page.screenshot(path=str(OUT / f"{cls}_worn.png"))
            await page.click('#pkBody .pk-item[data-p=""]')
            await page.wait_for_function("() => !wardrobe.debug().C.state.R && !wardrobe.debug().C.state.L", timeout=30000)
            st = await page.evaluate(STATE)
            check(not (st["R"] or st["L"] or st["pR"] or st["pL"]), f"{cls}: ไม่ใส่ takes both hands off")
            await page.click("#undo")
            await page.wait_for_function(f"() => wardrobe.debug().C.state.R === {json.dumps(want[0])}", timeout=30000)
            st = await page.evaluate(STATE)
            check((st["R"], st["L"]) == want, f"{cls}: one undo brings both back ({st['R']} + {st['L']})")
            await page.keyboard.press("Escape")

        # the Chameleon: the arrow on the model -> its menu -> the other piece; ถอดอาวุธออก takes both off
        await page.evaluate("() => wardrobe.show('chameleon', { R: 'royalBow', L: 'royalArrow' })")
        await page.evaluate("() => { const { C } = wardrobe.debug(); C.mixer.timeScale = 0; }")
        await page.wait_for_timeout(2500)          # the camera's glide to the new class ends first
        pts = await page.evaluate(POINTS)
        if "L" in pts:                             # still the arrow there (nothing moved since)
            at = await page.evaluate("([x, y]) => wardrobe.debug().pieceAt(x, y)?.slot", pts["L"])
            check(at == "L", f"chameleon: the arrow's point still hits the arrow ({at})")
        check("L" in pts and "R" in pts, f"chameleon: bow and arrow on screen ({sorted(pts)})")
        if "L" in pts:
            await page.mouse.click(*pts["L"])
            await page.wait_for_selector("#pmenu:not([hidden]) .pm-item")
            items = await page.evaluate("() => [...document.querySelectorAll('#pmenu .pm-item')].map(b => b.dataset.a + '|' + b.innerText)")
            name = await page.inner_text("#pmenu .pm-name")
            check(any(i.startswith("other|") for i in items) and any(i.startswith("remove|ถอดอาวุธออก") for i in items),
                  f"chameleon arrow menu ({name}): {[i for i in items if i.split('|')[0] in ('other', 'remove', 'change')]}")
            await page.screenshot(path=str(OUT / "menu_arrow.png"))
            await page.click('#pmenu .pm-item[data-a="other"]')
            await page.wait_for_selector("#pmenu:not([hidden]) .pm-item")
            name2 = await page.inner_text("#pmenu .pm-name")
            check(name2 != name and "Bow" in name2.replace(" ", ""), f"อีกชิ้นของอาวุธนี้ opens the bow's menu ({name2})")
            await page.click('#pmenu .pm-item[data-a="remove"]')
            await page.wait_for_function("() => !wardrobe.debug().C.state.R && !wardrobe.debug().C.state.L", timeout=30000)
            check(True, "chameleon: ถอดอาวุธออก takes bow and arrow off")
            await page.click("#undo")
            await page.wait_for_function("() => wardrobe.debug().C.state.L === 'royalArrow'", timeout=30000)
            check((await page.evaluate(STATE))["R"] == "royalBow", "chameleon: one undo brings both back")

        # the panel at three sizes (the weapon topic beside ประดับ, ท่าทาง across the last row)
        for w, h, tag in ((1920, 1200, "desktop"), (1366, 768, "short"), (390, 844, "phone")):
            await page.set_viewport_size({"width": w, "height": h})
            await page.wait_for_timeout(500)
            el = page.locator("#topics")
            await el.screenshot(path=str(OUT / f"panel_{tag}.png"))
            boxes = await page.evaluate("""() => Object.fromEntries([...document.querySelectorAll('#topics > .topic[data-t]')].map(b => {
              const r = b.getBoundingClientRect(); return [b.dataset.t, [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)]]; }))""")
            R, B, M = boxes.get("R"), boxes.get("Back"), boxes.get("move")
            check(R and B and M and R[1] == B[1] and M[1] > R[1] and M[2] >= R[2] + B[2],
                  f"{tag}: อาวุธ beside ประดับ, ท่าทาง below across the row ({R}, {B}, {M})")
            rings = await page.evaluate("() => ['R', 'Back', 'move'].map(t => Math.round(document.querySelector(`#topics [data-t=${t}] .ring`).getBoundingClientRect().width))")
            check(max(rings) - min(rings) <= 1, f"{tag}: the three rings one size ({rings})")
        await b.close()
    check(not errors, f"no page errors ({errors[:3]})")
    print(f"shots in {OUT}")
    sys.exit(1 if fails else 0)


asyncio.run(main())
