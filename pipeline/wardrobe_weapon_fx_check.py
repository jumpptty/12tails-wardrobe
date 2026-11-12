r"""Weapons' own effects on the model (pipeline/wardrobe_weapon_fx.py -> data/<cls>/weapon_fx.json; index.html weaponFx),
headless Playwright on its own server, so the user's browser is left alone:

  uv run --no-project --with pillow --with playwright python -I pipeline/wardrobe_weapon_fx_check.py [out.png] [cls:item ...]

Per weapon: put it in the right hand, wait 2.5 s, count the live weapon effects and the triangles they draw, and shoot a
close-up on a dark stage (out.png: a contact sheet, default plans/weapon_fx_check.png). Then take the weapon off and
check its effect is gone. Fails (exit 1) when a weapon with particles draws nothing, an effect outlives its weapon, or the
page throws.
"""
import asyncio
import functools
import http.server
import json
import sys
import threading
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
args = [a for a in sys.argv[1:] if ":" not in a or a[1] == ":"]
OUT = Path(args[0]) if args else ROOT / "plans" / "weapon_fx_check.png"
ITEMS = [a.split(":") for a in sys.argv[1:] if ":" in a and a[1] != ":"] or [
    ["bat", "flamingWand"], ["bat", "hallowCandle"], ["wolf", "flamingBrand"], ["whale", "specialLance"],
    ["bat", "timeWand"], ["wolf", "timeSword"], ["sheep", "flamingBook"], ["cat", "starRadio"], ["panda", "mummyClaw_R"]]


async def main():
    Q = type("Q", (http.server.SimpleHTTPRequestHandler,), {"log_message": lambda *a: None})
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Q, directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    bad = []
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        page = await (await b.new_context(viewport={"width": 900, "height": 900})).new_page()
        errs = []
        page.on("pageerror", lambda e: errs.append(str(e)))
        await page.goto(f"http://127.0.0.1:{srv.server_port}/wardrobe/")
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
        await page.add_style_tag(content="*{visibility:hidden!important} canvas{visibility:visible!important}")
        tiles = []
        for cls, item in ITEMS:
            await page.evaluate("""async ([cls, item]) => {
              const { scene, THREE } = wardrobe.debug(); scene.background = new THREE.Color(0x1d1f26);
              await wardrobe.show(cls, { R: item }, 0); }""", [cls, item])
            await page.wait_for_timeout(2500)
            info = await page.evaluate("""() => {
              const { C, WFX, camera, controls, THREE } = wardrobe.debug(), r = C.props.R;
              if (!r) return { err: "no prop" };
              const box = new THREE.Box3().setFromObject(r), c = box.getCenter(new THREE.Vector3()), s = Math.max(box.getSize(new THREE.Vector3()).length(), 0.5);
              controls.target.copy(c); camera.position.set(c.x + s * 0.3, c.y + s * 0.15, c.z + s * 1.3); controls.update();
              let tris = 0; for (const f of WFX.live) f.group.traverse(o => { if (o.geometry?.index) tris += o.geometry.index.count / 3; });
              return { live: WFX.live.map(f => f.name), emitters: WFX.live.reduce((n, f) => n + f.emitters.length, 0), tris };
            }""")
            print(cls, item, json.dumps(info))
            if info.get("err") or not info["live"]:
                bad.append(f"{cls}/{item}: no effect ({info})")
            elif info["tris"] == 0 and "Trail" not in json.dumps(info):
                bad.append(f"{cls}/{item}: its effect draws nothing")
            await page.wait_for_timeout(700)
            f = OUT.with_name("_weapon_fx_tmp.png")
            await page.locator("canvas").first.screenshot(path=str(f))
            tiles.append(Image.open(f).convert("RGB").resize((450, 450), Image.LANCZOS))
            f.unlink()
        left = await page.evaluate("""async () => { const { C, WFX } = wardrobe.debug(); await wardrobe.show(C.cls, { R: null });
          await new Promise(r => setTimeout(r, 500)); return WFX.live.length; }""")
        print("after taking the weapon off:", left, "live")
        if left:
            bad.append(f"{left} weapon effect(s) outlived the weapon")
        bad += [f"page error: {e}" for e in errs]
        await b.close()
    srv.shutdown()
    cols = 3
    sheet = Image.new("RGB", (450 * cols, 450 * ((len(tiles) + cols - 1) // cols)))
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % cols) * 450, (i // cols) * 450))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT)
    print("sheet:", OUT)
    print("FAIL:\n  " + "\n  ".join(bad) if bad else "OK")
    sys.exit(1 if bad else 0)


asyncio.run(main())
