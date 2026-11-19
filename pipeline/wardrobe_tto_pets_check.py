r"""Headless check of the TTO pet picker, wardrobe/tto_pets.html (2026-11-19; user: "create a html picker for TTO pet for me
to curate which one to upload, TTO pets model and texture shouldn't be downloadable"): it lists the 37 TTO pets of
data/pets/index.json; its preview (the wardrobe in a frame) shows the first one in the viewer with no bob; a tick, Ctrl+Z
and Ctrl+Y; ArrowRight previews the next; a tile click previews that pet and the big button ticks it; output() keeps every
other key of wardrobe/tto_released.json as the file has it and lists the ticked pets (sorted as tto_picker.html sorts);
no page error or failed request. Never writes the file. Serves the folder on a free port (never 8771). Exit 1 on a failure.
  uv run --no-project --with playwright==1.65.1 python -I -X utf8 pipeline/wardrobe_tto_pets_check.py [<root> [<out>]]"""
import asyncio, json, socket, subprocess, sys, time
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "checks" / "tto_pets"
fails = []


def check(ok, msg):
    print(("ok   " if ok else "FAIL ") + msg)
    if not ok:
        fails.append(msg)


SC = "() => document.getElementById('frame').contentWindow.wardrobe.debug().Showcase"
SHOWN = "n => { const S = (" + SC + ")(); return S.phase === 'on' && S.cur?.item === n && S.piece && !S.pieceTw && !S.next; }"


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
            pg = await (await b.new_context(viewport={"width": 1600, "height": 900})).new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("requestfailed", lambda r: errs.append("failed " + r.url))
            pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
            await pg.goto(f"http://127.0.0.1:{port}/wardrobe/tto_pets.html")
            await pg.wait_for_function("() => document.getElementById('wait').hidden", timeout=120000)
            pets = await pg.evaluate("() => petPicker.pets")
            want = sorted(r["name"] for r in json.loads((ROOT / "wardrobe" / "data" / "pets" / "index.json").read_text(encoding="utf-8")) if r.get("tto"))
            await pg.wait_for_function(SHOWN, arg=pets[0], timeout=60000)
            bob = await pg.evaluate("() => (" + SC + ")().bob")
            check(sorted(pets) == want and bob == 0, f"{len(pets)} TTO pets (the index has {len(want)}); the preview shows {pets[0]} in the viewer, bob {bob}")
            await pg.screenshot(path=str(OUT / "tto_pets_first.png"))
            # a tick, undo, redo
            await pg.click(f'.it[data-n="{pets[3]}"] .chk')
            a = await pg.evaluate("() => [...petPicker.sel]")
            await pg.keyboard.press("Control+z")
            z = await pg.evaluate("() => [...petPicker.sel]")
            await pg.keyboard.press("Control+y")
            y = await pg.evaluate("() => [...petPicker.sel]")
            check(a == [pets[3]] and z == [] and y == [pets[3]], f"tick {a}, Ctrl+Z {z}, Ctrl+Y {y}")
            # the arrow previews the next; a tile click previews that pet, the big button ticks it
            await pg.keyboard.press("ArrowRight")
            await pg.wait_for_function(SHOWN, arg=pets[1], timeout=60000)
            check(True, f"ArrowRight previews {pets[1]}")
            last = pets[-1]
            await pg.click(f'.it[data-n="{last}"] .pv')
            await pg.wait_for_function(SHOWN, arg=last, timeout=60000)
            await pg.click("#pick")
            sel = await pg.evaluate("() => [...petPicker.sel]")
            label = await pg.inner_text("#pick")
            check(sorted(sel) == sorted([pets[3], last]) and "แล้ว" in label, f"the big button ticks the previewed {last}: {sel}, it reads {label.strip()!r}")
            await pg.wait_for_timeout(600)
            await pg.screenshot(path=str(OUT / "tto_pets_ticked.png"))
            # the output: every other key as the file has it, the ticked pets
            out = json.loads(await pg.evaluate("() => petPicker.output()"))
            f = json.loads((ROOT / "wardrobe" / "tto_released.json").read_text(encoding="utf-8"))
            got = out.get("all", {}).pop("pets", None)
            f.get("all", {}).pop("pets", None)
            check(out == f and got == sorted(sel, key=str.lower), f"output: everything else unchanged ({out == f}), all.pets {got}")
            check(not errs, f"no page error or failed request {errs[:3]}")
            await b.close()
    finally:
        srv.terminate()
    print(f"shots in {OUT}")
    sys.exit(1 if fails else 0)


asyncio.run(main())
