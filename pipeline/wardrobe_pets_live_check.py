"""The pets on a PUBLISHED copy (a wardrobe_dist folder, or the live site): what wardrobe_dist_check.py does not cover.

  uv run --no-project --with playwright==1.65.1 python -I pipeline/wardrobe_pets_live_check.py D:/12tails-wardrobe/wardrobe_dist checks/pets_live
  uv run --no-project --with playwright==1.65.1 python -I pipeline/wardrobe_pets_live_check.py https://12tails-wardrobe.jumpthai.workers.dev/ checks/pets_live

A folder is served on a free port (headless Chromium, an isolated context, never the user's browser). Checks: the
published pets/index.json's TTO rows are exactly the TTO pets wardrobe/tto_released.json lists ("all" -> "pets", picked in
wardrobe/tto_pets.html; none until the user picks), each row's file is there, every unreleased TTO-only pet's file is not
(404), each released one's file is scrambled (the mark "TTOx": its mesh, user 2026-11-19 "yes, scramble") and up to three
of them go on stage with their idle playing, preview only (the page's TTO_LOCK and the row's tto: no download item); Bloom Pulse is
in neither icons.json nor props_trinkets.json (read unscrambled, the key taken from the published page's SCR_KEY); a few
BB pets (a follower, a far follower, a
kite, a balloon) go on stage with their idle playing and their PNG / GLB download items in the pet's menu data (not
ttoLocked), the Pet topic's picker lists as many pet tiles as the index has rows, and no page error / failed request.
Screenshots of each pet on stage go to <out>. Exit 1 on any failure. Written 2026-11-19 for the pets deploy (the final
review's M9: the dist check has no pet step).
"""
import asyncio, functools, http.server, json, sys, threading
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
TARGET, OUT = sys.argv[1], Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
PETS = ["smallAnubi", "miniMokBug", "kiteChula", "momBalloon"]     # follow / far follow / kite (ParentPosition) / float behind
LOCAL_INDEX = json.loads((ROOT / "wardrobe/data/pets/index.json").read_text(encoding="utf-8"))
TTO_ONLY = sorted(r["name"] for r in LOCAL_INDEX if r.get("tto"))
# the TTO pets the user released (wardrobe/tto_pets.html saves them in tto_released.json); the rest must stay offline
_rel = ROOT / "wardrobe/tto_released.json"
RELEASED = sorted(set((json.loads(_rel.read_text(encoding="utf-8")) if _rel.exists() else {}).get("all", {}).get("pets") or []) & set(TTO_ONLY))
UNRELEASED = sorted(set(TTO_ONLY) - set(RELEASED))
# a published file read as the page reads it (dataBytes: the mark "TTOx", then XOR the page's SCR_KEY), as text
READ = """async ([u, key]) => { const r = await fetch(u); if (!r.ok) return ''; let b = new Uint8Array(await r.arrayBuffer());
  if (b.length >= 4 && b[0] === 84 && b[1] === 84 && b[2] === 79 && b[3] === 120) { const k = new TextEncoder().encode(key); b = b.slice(4);
    for (let i = 0; i < b.length; i++) b[i] ^= k[i % k.length]; }
  return new TextDecoder().decode(b); }"""

if TARGET.startswith("http"):
    URL = TARGET if TARGET.endswith("/") else TARGET + "/"
else:
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    http.server.ThreadingHTTPServer.request_queue_size = 128
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(Path(TARGET))))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    URL = f"http://127.0.0.1:{srv.server_address[1]}/"

WEAR = """async n => { const { setPet, C } = wardrobe.debug(); let e = null;
  try { await setPet(n); } catch (x) { e = String(x?.stack || x); }
  const o = C.props.Pet, el = document.getElementById('status');
  return { err: e, on: o?.userData.pet ?? null, mixer: !!o?.userData.mixer, t: o?.userData.mixer?.time ?? null,
    tto: !!o?.userData.tto, toast: el.classList.contains('err') ? el.textContent : '' }; }"""
MIX_T = "() => wardrobe.debug().C.props.Pet?.userData.mixer?.time ?? null"


async def main():
    fails, n_ok = [], 0

    def check(ok, what):
        nonlocal n_ok
        print(("ok   " if ok else "FAIL ") + what)
        if ok: n_ok += 1
        else: fails.append(what)

    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        ctx = await b.new_context(viewport={"width": 1600, "height": 1000})
        page = await ctx.new_page()
        errors, bad = [], []
        page.on("pageerror", lambda e: errors.append(str(e)))
        # a failed fetch's console line mirrors its response: the responses are judged below (bad), not the lines
        page.on("console", lambda m: m.type == "error" and not m.text.startswith("Failed to load resource") and errors.append(m.text))
        page.on("response", lambda r: r.status >= 400 and bad.append(f"{r.status} {r.url}"))
        await page.goto(URL)
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=180000)
        await page.wait_for_timeout(1500)
        # the page's data folder (const DATA = "data-<hash>/" in the published page), read from the page's own HTML
        base, key, lock = await page.evaluate("""() => fetch(location.href, { cache: 'no-store' }).then(r => r.text()).then(t => {
            const m = t.match(/const DATA = "([^"]+)"/), k = t.match(/SCR_KEY = new TextEncoder[(][)][.]encode[(]"([^"]+)"[)]/);
            return [m ? new URL(m[1], location.href).href : null, k ? k[1] : null, t.includes('const TTO_LOCK = true;')]; })""")
        check(key is not None, "the page's SCR_KEY (to read scrambled files)")
        check(base is not None, f"the page's data folder ({base})")
        if base is None:
            print("errors:", fails); return 1
        index_url = base + "pets/index.json"
        rows = await page.evaluate("u => fetch(u).then(r => r.json())", index_url)
        tto_rows = sorted(r["name"] for r in rows if r.get("tto"))
        check(len(rows) > 0 and tto_rows == RELEASED, f"index: {len(rows)} rows, its TTO pets = the released list ({tto_rows}; released {RELEASED})")
        check(not ({r["name"] for r in rows} & set(UNRELEASED)), "index names no unreleased TTO-only pet")
        status = await page.evaluate("""async ([base, names]) => Promise.all(names.map(n =>
            fetch(base + 'pets/' + n + '.json', { method: 'HEAD' }).then(r => [n, r.status])))""", [base, [r["name"] for r in rows]])
        missing = [n for n, s in status if s != 200]
        check(not missing, f"every row's file is there ({len(status)} files){'; missing ' + ', '.join(missing) if missing else ''}")
        status = await page.evaluate("""async ([base, names]) => Promise.all(names.map(n =>
            fetch(base + 'pets/' + n + '.json', { method: 'HEAD' }).then(r => [n, r.status])))""", [base, UNRELEASED])
        leaked = [n for n, s in status if s == 200]
        check(not leaked, f"no unreleased TTO pet file online ({len(UNRELEASED)} tried){'; LEAKED ' + ', '.join(leaked) if leaked else ''}")
        heads = await page.evaluate("""async ([base, names]) => Promise.all(names.map(n => fetch(base + 'pets/' + n + '.json')
            .then(r => r.arrayBuffer()).then(b => [n, [...new Uint8Array(b.slice(0, 4))]])))""", [base, RELEASED])
        plain = [n for n, h in heads if bytes(h) != b"TTOx"]
        check(not plain, f"the released TTO pets' files scrambled ({len(heads)}){'; PLAIN ' + ', '.join(plain) if plain else ''}")
        bad[:] = [x for x in bad if "/pets/" not in x]          # the 404s just asked for
        icons = await page.evaluate("u => fetch(u).then(r => r.json())", base + "icons.json")
        check("aura_bloompulse" not in json.dumps(icons) and "bloompulse" not in json.dumps(icons).lower(), "icons.json: no Bloom Pulse")
        trink = await page.evaluate(READ, [base + "all/props_trinkets.json", key or ""])
        check(trink.startswith("[") and "bloompulse" not in trink.lower(), f"all/props_trinkets.json read as JSON ({trink[:1]!r}): no Bloom Pulse")

        for name in PETS:
            if name not in {r["name"] for r in rows}:
                check(False, f"{name} in the published index"); continue
            w = await page.evaluate(WEAR, name)
            check(w["err"] is None and w["on"] == name and not w["toast"], f"{name} on stage (err {w['err']}, toast '{w['toast']}')")
            if w["mixer"]:
                try:
                    await page.wait_for_function(f"t0 => ({MIX_T})() > t0 + 0.1", arg=w["t"] or 0, timeout=15000); moving = True
                except Exception:
                    moving = False
                check(moving, f"{name}: its idle plays")
            check(not w["tto"], f"{name}: not ttoLocked (its menu offers PNG / GLB)")
            await page.wait_for_timeout(600)
            await page.screenshot(path=str(OUT / f"{name}.png"))
        for name in RELEASED[:3]:                                # released TTO pets: on stage, preview only
            w = await page.evaluate(WEAR, name)
            check(w["err"] is None and w["on"] == name and not w["toast"], f"{name} (TTO, released) on stage (err {w['err']}, toast '{w['toast']}')")
            if w["mixer"]:
                try:
                    await page.wait_for_function(f"t0 => ({MIX_T})() > t0 + 0.1", arg=w["t"] or 0, timeout=15000); moving = True
                except Exception:
                    moving = False
                check(moving, f"{name}: its idle plays")
            row = next(r for r in rows if r["name"] == name)
            check(lock and row.get("tto"), f"{name}: preview only (the page's TTO_LOCK {lock}, its row tto {row.get('tto')}: its menu has no download item)")
            await page.screenshot(path=str(OUT / f"{name}.png"))
        await page.evaluate("() => wardrobe.debug().setPet(null)")

        await page.click('#topics button.topic[data-t="Pet"]')
        try:
            await page.wait_for_function("() => document.getElementById('pkBody')?.dataset.topic === 'Pet' && !document.getElementById('picker').hidden", timeout=15000)
            tiles = await page.evaluate("() => document.querySelectorAll('#pkBody .pk-item[data-p]:not([data-p=\"\"])').length")
            check(tiles >= len(rows), f"the Pet picker lists the pets ({tiles} tiles for {len(rows)} rows)")
            await page.screenshot(path=str(OUT / "picker.png"))
        except Exception as e:
            check(False, f"the Pet picker opens ({e.__class__.__name__})")
        check(not errors, f"no page / console errors{': ' + '; '.join(errors[:5]) if errors else ''}")
        if not TARGET.startswith("http"):                       # a folder has no Worker: its /api/ routes 404 here only
            bad[:] = [x for x in bad if "/api/" not in x]
        check(not bad, f"no failed requests{': ' + '; '.join(bad[:5]) if bad else ''}")
        await b.close()
    print(f"{n_ok} ok, {len(fails)} fail")
    print("errors:", fails)
    return 1 if fails else 0


sys.exit(asyncio.run(main()))
