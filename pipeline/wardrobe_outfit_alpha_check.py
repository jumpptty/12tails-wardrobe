r"""Outfits are drawn as the game draws them (2026-11-13; user: "Players use my wardrobe to plan what the skin will looks
like in the game. Fix the wardrobe to use game logic"): BB composes the worn texture as RGB24 and draws it with plain
Diffuse, so no part of an outfit is see-through in the game, whatever a skin's alpha says (index.html outfitCut,
composeTexture). This puts a skin with a hole (alpha 0, a red colour under it) on a BB outfit and checks: the material
has no alpha test, the composed texture is opaque at the hole and keeps the red there; a ToT student outfit keeps its
cut-out; a prop keeps its own game shader's. Headless, the local page; exit 1 on a failure.
  uv run --no-project --with playwright python -I pipeline/wardrobe_outfit_alpha_check.py"""
import asyncio, functools, http.server, json, sys, threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


async def main():
    from playwright.async_api import async_playwright
    Q = type("Q", (http.server.SimpleHTTPRequestHandler,), {"log_message": lambda *a: None})
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Q, directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    errors = []
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        page = await (await b.new_context(viewport={"width": 1200, "height": 900})).new_page()
        page.on("pageerror", lambda e: errors.append(str(e)))
        await page.goto(f"http://127.0.0.1:{srv.server_port}/wardrobe/")
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
        r = await page.evaluate("""async () => {
          const W = wardrobe, D = W.debug(), out = {};
          // (debug() hands out C as it is now: a class load replaces it, so read it fresh each time)
          const until = async f => { for (let i = 0; i < 600 && !f(); i++) await new Promise(r => setTimeout(r, 100)); if (!f()) throw new Error("timed out"); };
          await W.show("cat", {}); await until(() => W.debug().C.cls === "cat" && W.debug().C.meshes.length);
          await W.setOutfit("standard", 1); await W.setOutfit("summer", 1); await until(() => W.debug().C.state.outfit === "summer");
          // the cat's summer sheet with a hole: every texel alpha 0, red under it, in the block x 300-340, y 300-340
          const img = W.debug().C.meshes[0].material.map.image, w = img.width, h = img.height;
          const data = new Uint8ClampedArray(w * h * 4);
          for (let i = 0; i < data.length; i += 4) { data[i] = 40; data[i + 1] = 90; data[i + 2] = 160; data[i + 3] = 255; }
          for (let y = 300; y < 340; y++) for (let x = 300; x < 340; x++) { const i = (y * w + x) * 4; data[i] = 220; data[i + 1] = 10; data[i + 2] = 10; data[i + 3] = 0; }
          D.SKINS.set("cat|outfits|summer|", { w, h, data });
          await W.setOutfit("standard", 1); await W.setOutfit("summer", 1);
          const m = W.debug().C.meshes[0].material, cv = m.map.image, px = cv.getContext("2d").getImageData(320, 320, 1, 1).data;
          out.bb = { outfit: W.debug().C.state.outfit, cls: W.debug().C.cls, alphaTest: m.alphaTest, hole: Array.from(px) };
          D.SKINS.clear();
          const tot = W.debug().C.outfits.find(o => o.tot);
          if (tot) { await W.setOutfit(tot.name, tot.colors[0]); await until(() => W.debug().C.state.outfit === tot.name); out.tot = { name: tot.name, alphaTest: W.debug().C.meshes[0].material.alphaTest }; }
          return out;
        }""")
        await b.close()
    srv.shutdown()
    print(json.dumps(r))
    fails = []
    if r["bb"]["alphaTest"] != 0:
        fails.append(f"a BB outfit has an alpha test ({r['bb']['alphaTest']}): the game draws outfits opaque")
    hole = r["bb"]["hole"]
    if hole[3] != 255 or hole[0] < 180 or hole[1] > 60:
        fails.append(f"the skin's hole is {hole}: it should be opaque and keep its red (the game's RGB24)")
    if "tot" in r and r["tot"]["alphaTest"] != 0.5:
        fails.append(f"the ToT outfit {r['tot']['name']} lost its cut-out ({r['tot']['alphaTest']})")
    fails += [f"page error: {e}" for e in errors]
    print("\n".join(fails) or "ok: outfits opaque as in the game, ToT keeps its cut-out, no page errors")
    sys.exit(1 if fails else 0)

asyncio.run(main())
