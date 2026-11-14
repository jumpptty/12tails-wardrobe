"""Headless check of the pickers' search and the Bible's nicknames (2026-11-14; user: "1. add search box by name 2. nickname
should work in search box 3. see nicknamed items from the class guide in the bible hub ... sort them first at the top for
the wardrobe"; the look: "swap", the nickname in place of the name, the name small under it). Per class, in the outfit,
weapon, hat, back and set pickers:
  - the nicknamed tiles come first (after ไม่ใส่ / ถอดทั้งหมด), in the Bible's order (no level, rank-gated highest rank
    first, then level highest first), worked out here from wardrobe/data/nicknames.json apart from the page; each shows
    its nickname (.nk-main) over its name (.nk-sub = the tooltip's name); the others show no nickname
  - every picker has a ค้นหา box; a nickname typed without its space ("70ดล") leaves only that nickname's tiles; a game
    name (nicknames.json "game") finds its tile; nonsense shows ไม่พบที่ค้นหา; a redraw of the picker keeps the query
  - the piece viewer's → steps in the picker's order
  - screenshots of the Rabbit's weapon, outfit and set pickers at 1366x768 and 390x844 in <out> (Thai marks by eye); no page errors
Exit 1 on any failure.
  uv run --no-project --with playwright==1.65.1 python -I pipeline/wardrobe_nick_check.py D:/12tails-wardrobe checks/nick_check [classes]"""
import asyncio, functools, http.server, json, re, sys, threading
from pathlib import Path
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")
ROOT, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
CLASSES = (sys.argv[3].split(",") if len(sys.argv) > 3 else
           ["bat", "bison", "cat", "chameleon", "mole", "monkey", "panda", "penguin", "rabbit", "sheep", "whale", "wolf"])
NICK = json.loads((ROOT / "wardrobe" / "data" / "nicknames.json").read_text(encoding="utf-8"))
KIND = {"outfit": "outfits", "R": "weapons", "Head": "accessories", "Back": "trinkets"}
NOT_FOUND = "ไม่พบที่ค้นหา"
BASE_HEAD = {"cat": "default"}           # the page's BASE_HEAD


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


http.server.ThreadingHTTPServer.request_queue_size = 128
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/wardrobe/index.html"


def row_of(cls, topic, key):
    """nicknames.json's row of a tile, looked up the way the page looks up its icon (iconOf)."""
    kind = KIND[topic]
    t = NICK.get(cls, {}).get(kind, {})
    if key in t:
        return t[key]
    base = re.sub(r"_[LRlr]$", "", key)
    if base in t:
        return t[base]
    return NICK.get("all", {}).get(kind, {}).get(key.lower(), {})


def order_key(lv):
    """The Bible's classGuideGearSortKey after the nickname test: no level, rank-gated (highest rank first), level desc."""
    return (0, 0) if lv is None else (1, lv) if lv < 0 else (2, -lv)


def squash(s):
    return re.sub(r"\s+", "", s).lower()


TILES = """() => [...document.querySelectorAll('#pkBody .pk-item')].map(b => ({
  key: b.dataset.o != null ? b.dataset.o + (b.dataset.e ? '|' + b.dataset.e : '') : b.dataset.p != null ? b.dataset.p : b.dataset.s != null ? 'set:' + b.dataset.s : null,
  main: b.querySelector('.nk-main')?.textContent ?? null, sub: b.querySelector('.nk-sub')?.textContent ?? null,
  title: b.title || '', lbl: b.querySelector('.lbl')?.textContent || '' }))"""
NOTE = "() => [...document.querySelectorAll('#pkBody .pk-note')].map(n => n.textContent).join(' ')"
# should a nicknames.json row have a tile? (an item the page has, in any case: an outfit with that edition, a weapon's R
# piece, a hat / back piece by name or name without _L / _R)
TILE_EXPECTED = """([t, k]) => { const D = wardrobe.debug(), C = D.C, low = s => s.toLowerCase();
  if (t === 'outfit') { const [n, e] = k.split('|'), o = C.outfits.find(o => low(o.name) === low(n)); return !!o && (!e || !!o.editions?.[e]); }
  const list = C.propLists[{ R: 'weapons', Head: 'accessories', Back: 'trinkets' }[t]] || [];
  const p = list.find(p => low(p.name) === low(k) || low(p.name.replace(/_[LRlr]$/, '')) === low(k));
  return !!p && (t !== 'R' || D.weaponOf(p.name).R === p.name || !D.weaponOf(p.name).R); }"""
# a worn nicknamed tile against an unworn one: the name line's colour and the edge
WORN = """() => { const b = [...document.querySelectorAll('#pkBody .pk-item.is-nick')], on = b.find(x => x.getAttribute('aria-pressed') === 'true'),
  off = b.find(x => x.getAttribute('aria-pressed') !== 'true'), st = x => x && { sub: getComputedStyle(x.querySelector('.nk-sub')).color, edge: getComputedStyle(x).boxShadow };
  return { on: st(on), off: st(off) }; }"""


async def check_viewing(page, cls, tiles, ok):
    """The viewer on an outfit whose R / V tile is sorted before it: the dashed mark is on the outfit's own tile."""
    keys = [x["key"] for x in tiles]
    name = next((k.split("|")[0] for i, k in enumerate(keys) if "|" in k and k.split("|")[0] in keys[i + 1:]), None)
    if not name:
        return
    await page.evaluate("n => wardrobe.debug().Showcase.enter('outfit', n)", name)
    await page.wait_for_function("() => wardrobe.debug().Showcase.cur && !wardrobe.debug().Showcase.loading", timeout=30000)
    await page.wait_for_timeout(200)
    got = await page.evaluate("() => { const b = document.querySelector('#pkBody .pk-item[data-viewing]'); return b && [b.dataset.o, b.dataset.e]; }")
    ok(got == [name, ""], f"{cls} outfit: viewing {name} marks its own tile ({got})")
    await page.keyboard.press("Escape")
    await page.wait_for_timeout(400)


async def check_worn(page, ok):
    """A worn nicknamed tile stands apart from the unworn ones (2026-11-14 review: the gold label used to be the mark)."""
    await open_topic(page, "R")
    await page.locator("#pkBody .pk-item.is-nick").first.click()
    await page.wait_for_function("() => document.querySelector('#pkBody .pk-item.is-nick[aria-pressed=true]')", timeout=30000)
    s = await page.evaluate(WORN)
    ok(s["on"] and s["off"] and s["on"]["sub"] != s["off"]["sub"] and s["on"]["edge"] != s["off"]["edge"], f"worn nicknamed tile apart: {s}")
    await page.locator('#pkBody .pk-item[data-p=""]').click()
    await page.wait_for_timeout(300)


async def open_topic(page, t):
    await page.evaluate("() => { if (!document.getElementById('picker').hidden) document.getElementById('pkClose').click(); }")
    await page.click(f'button[data-t="{t}"]')
    await page.wait_for_selector("#pkBody .pk-item")
    await page.wait_for_timeout(150)


async def search(page, q):
    await page.fill("#pkTools input[type=search]", q)
    await page.wait_for_timeout(80)
    return await page.evaluate(TILES)


def set_rows(cls, s):
    """A set's piece rows: its outfit in the set's own edition (no fallback to the plain outfit's), weapon, hat, back."""
    o = s["outfit"] and row_of(cls, "outfit", s["outfit"] + ("|" + s["v"] if s["v"] else ""))
    return [o or {}] + [row_of(cls, t, n) if n else {} for t, n in (("R", s["R"] or s["L"]), ("Head", s["Head"]), ("Back", s["Back"]))]


def set_nick(cls, s):
    """The set's nickname row: its outfit's, else the first of its weapon, hat, back that has one."""
    return next((r for r in set_rows(cls, s) if "nick" in r), {})


SETS = """() => wardrobe.debug().C.sets.map(s => ({ theme: s.theme, v: s.v || '', outfit: s.outfit, R: s.R, L: s.L, Head: s.Head, Back: s.Back }))"""


async def check_sets(page, cls, ok):
    await open_topic(page, "set")
    tag = f"{cls} set"
    ok(await page.locator("#pkTools input[type=search]").count() == 1, f"{tag}: a search box")
    sets = await page.evaluate(SETS)
    tiles = await page.evaluate(TILES)
    ok(tiles and tiles[0]["key"] == "set:clear", f"{tag}: ถอดทั้งหมด first")
    ok([x["key"] for x in tiles[1:]] == [f"set:{i}" for i in range(len(sets))], f"{tag}: tiles in the set list's order")
    rows = [set_nick(cls, s) for s in sets]
    named = [i for i, r in enumerate(rows) if r]
    ok(named == list(range(len(named))), f"{tag}: nicknamed sets first ({named[:6]}...)")
    keys = [order_key(rows[i].get("lv")) for i in named]
    ok(keys == sorted(keys), f"{tag}: the Bible's order {[sets[i]['theme'] + sets[i]['v'] for i in named]}")
    for x, r in zip(tiles[1:], rows):
        if r:
            ok(x["main"] == r["nick"] and x["sub"] == x["title"] and x["sub"], f"{tag} {x['key']}: label {x['main']!r} / {x['sub']!r}")
        else:
            ok(x["main"] is None, f"{tag} {x['key']}: no nickname shown")
    if named:
        nick = rows[named[0]]["nick"]
        want = sorted(f"set:{i}" for i, s in enumerate(sets) if any(r.get("nick") == nick for r in set_rows(cls, s)))
        got = await search(page, squash(nick))
        ok(got and got[0]["key"] == "set:clear" and sorted(x["key"] for x in got[1:]) == want,
           f"{tag}: search {squash(nick)!r} -> {[x['key'] for x in got]} (want clear + {want})")
        await page.evaluate("() => wardrobe.debug().openPicker('set')")
        await page.wait_for_timeout(150)
        ok(await page.input_value("#pkTools input[type=search]") == squash(nick)
           and [x["key"] for x in await page.evaluate(TILES)] == [x["key"] for x in got], f"{tag}: a redraw keeps the query")
    gone = await search(page, "zzqxv")
    ok(NOT_FOUND in await page.evaluate(NOTE) and [x["key"] for x in gone] == ["set:clear"], f"{tag}: nonsense -> ถอดทั้งหมด + {NOT_FOUND}")
    await search(page, "")


async def main():
    errors, fails, n_ok = [], [], 0

    def ok(cond, what):
        nonlocal n_ok
        if cond:
            n_ok += 1
        else:
            fails.append(what); print("FAIL", what)

    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        page = await b.new_page(viewport={"width": 1366, "height": 768})
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: m.type == "error" and errors.append(m.text))
        await page.goto(URL)
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=180000)
        for cls in CLASSES:
            await page.evaluate("c => wardrobe.show(c, {})", cls)
            for t in ("outfit", "R", "Head", "Back"):
                await open_topic(page, t)
                tag = f"{cls} {t}"
                ok(await page.locator("#pkTools input[type=search]").count() == 1, f"{tag}: a search box")
                # ไม่ใส่ = key ""; the Cat's hood heads its hats as its "nothing" (BASE_HEAD: no ไม่ใส่ tile)
                tiles = [x for x in await page.evaluate(TILES) if x["key"] and not (t == "Head" and x["key"] == BASE_HEAD.get(cls))]
                rows = [row_of(cls, t, x["key"]) for x in tiles]
                named = [i for i, r in enumerate(rows) if "nick" in r]
                ok(named == list(range(len(named))), f"{tag}: nicknamed tiles first ({named[:6]}...)")
                keys = [order_key(rows[i].get("lv")) for i in named]
                ok(keys == sorted(keys), f"{tag}: the Bible's order {[tiles[i]['key'] for i in named]}")
                for x, r in zip(tiles, rows):
                    if "nick" in r:
                        ok(x["main"] == r["nick"] and x["sub"] == x["title"] and x["sub"], f"{tag} {x['key']}: label {x['main']!r} / {x['sub']!r}")
                    else:
                        ok(x["main"] is None, f"{tag} {x['key']}: no nickname shown")
                # every nicknamed row whose item the page has (in any case) shows on its tile (2026-11-14 review:
                # icons.json's PoseidonHelmet / shinjitsu hid the Bison's หมวกดันน้ำ and the Panda's 48 ดด)
                shown = {x["key"]: x["main"] for x in tiles}
                stripped = {re.sub(r"_[LRlr]$", "", k): v for k, v in shown.items()}
                for k, r in NICK.get(cls, {}).get(KIND[t], {}).items():
                    if "nick" not in r or (t == "Head" and k == BASE_HEAD.get(cls)):
                        continue
                    if k in shown or k in stripped:
                        ok((shown[k] if k in shown else stripped[k]) == r["nick"], f"{tag} {k}: shown as {r['nick']!r}")
                    elif await page.evaluate(TILE_EXPECTED, [t, k]):
                        ok(False, f"{tag} {k}: nicknamed row {r['nick']!r} has no tile")
                if t == "outfit":
                    await check_viewing(page, cls, tiles, ok)
                # a nickname without its space
                if named:
                    nick = rows[named[0]]["nick"]
                    want = sorted(x["key"] for x, r in zip(tiles, rows) if r.get("nick") == nick)
                    got = sorted(x["key"] for x in await search(page, squash(nick)) if x["key"])
                    ok(got == want, f"{tag}: search {squash(nick)!r} -> {got} (want {want})")
                # a game name that is not the tile's own name
                g = next(((x["key"], r["game"][0]) for x, r in zip(tiles, rows) if r.get("game") and squash(r["game"][0]) not in squash(x["title"])), None)
                if g:
                    got = [x["key"] for x in await search(page, g[1].upper())]
                    ok(g[0] in got, f"{tag}: game name {g[1]!r} finds {g[0]}")
                    # a redraw (the same topic opened again) keeps the query and its list
                    await page.evaluate("t => wardrobe.debug().openPicker(t)", t)
                    await page.wait_for_timeout(150)
                    again = [x["key"] for x in await page.evaluate(TILES)]
                    q = await page.input_value("#pkTools input[type=search]")
                    ok(q == g[1].upper() and again == got, f"{tag}: a redraw keeps {q!r}")
                gone = await search(page, "zzqxv")
                ok(NOT_FOUND in await page.evaluate(NOTE) and not [x for x in gone if x["key"]], f"{tag}: nonsense -> {NOT_FOUND}")
                await search(page, "")
            await check_sets(page, cls, ok)
            # the viewer's → follows the picker's order (the weapon picker, open)
            await open_topic(page, "R")
            order = [x["key"] for x in await page.evaluate(TILES) if x["key"]]
            if len(order) > 2:
                await page.evaluate("it => wardrobe.debug().Showcase.enter('R', it)", order[0])
                await page.wait_for_function("() => wardrobe.debug().Showcase.cur && !wardrobe.debug().Showcase.loading", timeout=30000)
                await page.keyboard.press("ArrowRight")
                await page.wait_for_function("k => wardrobe.debug().Showcase.cur?.item === k", arg=order[1], timeout=30000)
                ok(True, f"{cls}: the viewer steps to {order[1]}")
                await page.keyboard.press("Escape")
                await page.wait_for_timeout(300)
            print(f"{cls}: done")
        await page.evaluate("() => wardrobe.show('rabbit', {})")
        await check_worn(page, ok)
        for w, h in ((1366, 768), (390, 844)):
            await page.set_viewport_size({"width": w, "height": h})
            for t in ("R", "outfit", "set"):
                await open_topic(page, t)
                await page.wait_for_timeout(1200)
                await page.locator("#picker").screenshot(path=str(OUT / f"rabbit_{t}_{w}.png"))
        await b.close()
    ok(not errors, f"page errors: {errors[:5]}")
    print(f"{n_ok} ok, {len(fails)} failed")
    return 1 if fails else 0


sys.exit(asyncio.run(main()))
