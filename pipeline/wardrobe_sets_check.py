"""Headless check of the wardrobe's sets and R / V editions (2026-11-09; user: "Chameleon Legend set doesn't have legend
bow", "Panda doesn't have Worm R in the armor selection, but it can be chosen from the set equip"). For every class:
  - foreign weapons: a set's R / L piece named after ANOTHER outfit (Chameleon legend got standardBow from item_map's
    wrong w_chm61 = standardBow + legendArrow; the game loads legendBow + legendArrow for w_chm60 / 61)
  - editions: every outfits.json R / V edition, whether a set reaches it and whether the ชุด picker has its tile (one
    per edition since 2026-11-09); Panda's Worm R picked there, undone, and plain Worm dropping the edition
Writes <out>/sets.json and <out>/panda_outfits.png; exit 1 on a foreign weapon, an edition no set reaches or with no
ชุด tile, or a wrong pressed tile.
uv run --no-project --with playwright python -I pipeline/wardrobe_sets_check.py D:/12tails-wardrobe checks/<dir>"""
import asyncio, functools, http.server, json, re, sys, threading
from pathlib import Path
from playwright.async_api import async_playwright

ROOT, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
CLASSES = ["bat", "bison", "cat", "chameleon", "mole", "monkey", "panda", "penguin", "rabbit", "sheep", "whale", "wolf"]


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


# the stdlib server queues 5 connections; the page loads dozens of icons at once and the rest were refused
# (ERR_CONNECTION_REFUSED, 2026-11-09: data/icons/skills/emotion/beg.webp)
http.server.ThreadingHTTPServer.request_queue_size = 128
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/wardrobe/index.html"
DUMP = """() => { const { C } = wardrobe.debug();
  return { outfits: C.outfits.map(o => ({ name: o.name, editions: o.editions || {} })),
           sets: C.sets.map(s => ({ theme: s.theme, v: s.v, outfit: s.outfit, R: s.R, L: s.L, Head: s.Head, Back: s.Back })) }; }"""


def stem(n):                       # legendBowR_L -> legendBow
    return re.sub(r"(?<=[a-z0-9])[A-Z]$", "", re.sub(r"\d+$", "", re.sub(r"_[LRlr]$", "", n)))


def owned_by(name, theme):         # theme at a word boundary: legendArrow -> legend, not legendary -> legend
    s = stem(name)
    return s == theme or (s.startswith(theme) and s[len(theme):len(theme) + 1].isupper())


def audit(d):
    # foreign = another set's own weapon (standardBow is the standard set's): a piece joined by its code number alone
    # (Penguin box a_pgn5 + paperCup w_pgn5 + beggarHat, the beggar costume) is no other set's, so it isn't flagged
    owned = {s[k] for s in d["sets"] for k in ("R", "L") if s[k] and owned_by(s[k], s["theme"])}
    foreign = [f'{s["theme"]}{s["v"]}: {k}={s[k]}' for s in d["sets"] for k in ("R", "L") if s[k]
               and not owned_by(s[k], s["theme"]) and s[k] in owned]
    reach = {(s["outfit"], s["v"]) for s in d["sets"] if s["outfit"]}
    eds = [(o["name"], e) for o in d["outfits"] for e in o["editions"]]
    return foreign, eds, [f"{o} {e}" for o, e in eds if (o, e) not in reach]


async def main():
    errors, report, bad = [], {}, 0
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        page = await b.new_page(viewport={"width": 1366, "height": 607})
        page.on("pageerror", lambda e: errors.append(str(e)))
        await page.goto(URL)
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
        async def open_outfits():                 # the ชุด picker drawn fresh for the class now loaded
            if await page.evaluate("() => !document.getElementById('picker').hidden && document.getElementById('pkBody').dataset.topic === 'outfit'"):
                await page.click('button.topic[data-t="outfit"]')
            await page.click('button.topic[data-t="outfit"]')
            await page.wait_for_selector('#pkBody .pk-item[data-o]')
        STATE = "() => { const s = wardrobe.debug().C.state; return s.outfit + '/' + (s.edition || ''); }"
        PRESSED = "() => [...document.querySelectorAll('#pkBody .pk-item[aria-pressed=true]')].map(b => b.dataset.o + '/' + b.dataset.e).join(',')"
        for cls in CLASSES:
            await page.evaluate("c => wardrobe.show(c)", cls)
            await page.wait_for_function("c => { const C = wardrobe.debug().C; return C.cls === c && C.sets; }", arg=cls, timeout=60000)
            d = await page.evaluate(DUMP)
            foreign, eds, unreached = audit(d)
            # the ชุด picker: one tile per edition (user 2026-11-09: "Panda doesn't have Worm R in the armor selection")
            await open_outfits()
            tiles = set(await page.evaluate("() => [...document.querySelectorAll('#pkBody .pk-item[data-e]:not([data-e=\"\"])')].map(b => b.dataset.o + ' ' + b.dataset.e)"))
            untiled = [f"{o} {e}" for o, e in eds if f"{o} {e}" not in tiles]
            report[cls] = {**d, "foreign": foreign, "unreached": unreached, "untiled": untiled}
            bad += len(foreign) + len(unreached) + len(untiled)
            print(f"{cls:10} sets {len(d['sets']):3}  editions {len(eds):2} (no set: {len(unreached)}, no outfit-picker tile: {len(untiled)})  foreign weapons {len(foreign)}")
            for x in foreign: print("   foreign:", x)
            for x in unreached: print("   edition no set reaches:", x)
            for x in untiled: print("   edition with no outfit-picker tile:", x)
        # Panda's Worm R from the ชุด picker: worn, its tile pressed, one undo step; then plain Worm drops the edition
        await page.evaluate("c => wardrobe.show(c)", "panda")
        await open_outfits()
        before = await page.evaluate(STATE)
        steps = []
        for sel, want in (('[data-o="worm"][data-e="R"]', "worm/R"), ("#undo", before), ('[data-o="worm"][data-e=""]', "worm/"),
                          ('[data-o="worm"][data-e="R"]', "worm/R")):
            await page.click(sel if sel == "#undo" else f"#pkBody .pk-item{sel}")
            await page.wait_for_function(f"() => ({STATE})() === {json.dumps(want)}", timeout=30000)
            pressed = await page.evaluate(PRESSED)
            steps.append(f"{sel} -> {want} pressed {pressed}")
            if sel != "#undo" and pressed != want:
                errors.append(f"pressed {pressed}, want {want}")
        print("Panda Worm R:", *steps, sep="\n   ")
        await page.locator('#pkBody .pk-item[data-o="worm"][data-e="R"]').scroll_into_view_if_needed()
        await page.screenshot(path=str(OUT / "panda_outfits.png"))
        await b.close()
    (OUT / "sets.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print("errors:", errors)
    sys.exit(1 if bad or errors else 0)


asyncio.run(main())
