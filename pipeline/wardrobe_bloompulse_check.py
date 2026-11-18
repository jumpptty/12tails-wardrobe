r"""Headless look check of Bloom Pulse (2026-11-19, the pets plan's Task 10; user: "add t_all_tto_bloompulse to the
wardrobe too if it has a model for it", "Do the meshes at max level for Bloom Pulse"). On the real page (wardrobe.show /
wardrobe.debug()): the Sheep in standard wears aura_bloompulse in the ประดับ (Back) slot.
  - the worn prop holds the 17 meshes (Moat, Ribbon, Flower1 / 3 / 4 x Inner / Heart / Pulse, Twin0, Twin1, Ring: the
    controller's ruling R6; not 18), every one with its material, and the data's entry says "tto": true
  - the Back picker has an aura_bloompulse tile with its icon (an <img>: gamegui/icons/items/trinket/alllkt2lv9)
  - screenshots from 3 angles (front, three-quarter from the right, from above) of the Sheep with it, plus the Sheep
    with aura_bloodmoon (the existing aura, same placement rule) for comparison, into <out>
  - no page errors, console errors or failed requests (zero: any 404 is real)
Exit 1 on any failure. Serves the folder itself on a free port (never 8771).
  uv run --no-project --with playwright==1.65.1 python -I pipeline/wardrobe_bloompulse_check.py [D:/12tails-wardrobe-pets checks/bloompulse]"""
import functools, http.server, json, math, sys, threading
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
ROOT = Path(ARGS[0]) if ARGS else HERE.parent
OUT = Path(ARGS[1]) if len(ARGS) > 1 else ROOT / "checks" / "bloompulse"
OUT.mkdir(parents=True, exist_ok=True)
MESHES = ["Moat", "Ribbon", "Flower1", "Flower1Inner", "Flower1Heart", "Flower1Pulse", "Flower3", "Flower3Inner",
          "Flower3Heart", "Flower3Pulse", "Flower4", "Flower4Inner", "Flower4Heart", "Flower4Pulse", "Twin0", "Twin1", "Ring"]


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


http.server.ThreadingHTTPServer.request_queue_size = 128     # the page loads dozens of icons at once
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/wardrobe/index.html"

WORN = """() => { const { C } = wardrobe.debug(), o = C.props.Back; if (!o) return null;
  const meshes = []; o.traverse(x => { if (x.isMesh && !x.userData.hoverOverlay) meshes.push([x.name, [].concat(x.material).length]); });
  return { name: C.state.Back, placement: o.userData.placement, meshes, pos: o.position.toArray(), scale: o.scale.toArray(),
           parent: o.parent && o.parent.name }; }"""
# a camera direction around the hero's middle, the distance fitted to the whole body, the hero's middle as the target
SHOT = """([az, el]) => { const { C, THREE, camera, controls } = wardrobe.debug();
  const b = new THREE.Box3().setFromObject(C.root, true), c = b.getCenter(new THREE.Vector3()), r = b.getSize(new THREE.Vector3()).length() * 1.25;
  const a = az * Math.PI / 180, e = el * Math.PI / 180;
  camera.position.set(c.x + r * Math.sin(a) * Math.cos(e), c.y + r * Math.sin(e), c.z + r * Math.cos(a) * Math.cos(e));
  controls.target.copy(c); camera.lookAt(c); controls.update(); }"""


def main():
    errors, fails = [], []
    check = lambda ok, what: (print(("ok   " if ok else "FAIL ") + what), ok or fails.append(what))
    entry = next(e for e in json.loads((ROOT / "wardrobe/data/all/props_trinkets.json").read_text(encoding="utf-8")) if e["name"] == "aura_bloompulse")
    check(entry.get("tto") is True and entry.get("mount"), f"the data entry: tto {entry.get('tto')}, mount {entry.get('mount')}")
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        page = b.new_context(viewport={"width": 1280, "height": 900}).new_page()
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: m.type == "error" and errors.append(m.text + " " + (m.location or {}).get("url", "")))
        page.on("requestfailed", lambda r: errors.append("request failed " + r.url))
        page.goto(URL)
        page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)

        for aura, tag in (("aura_bloompulse", "bloompulse"), ("aura_bloodmoon", "bloodmoon")):
            page.evaluate("c => wardrobe.show('sheep', c)", {"Back": aura})      # wardrobe.show's 2nd argument: prop slots only
            page.wait_for_function(f"() => wardrobe.debug().C.props.Back && wardrobe.debug().C.state.Back === '{aura}'", timeout=60000)
            page.wait_for_timeout(1500)                      # the textures
            w = page.evaluate(WORN)
            print(f"{aura}: {w['placement']}, parent {w['parent']}, position {w['pos']}, scale {w['scale']}")
            if aura == "aura_bloompulse":
                # the page names a node's object p<index>: the data's 17 mesh nodes, by their indices
                want = sorted(f"p{i}" for i, n in enumerate(entry["nodes"]) if "mesh" in n)
                got = sorted(m[0] for m in w["meshes"])
                check(len(got) == 17 and got == want, f"the worn aura_bloompulse holds the 17 meshes ({len(got)}: {got})")
                named = sorted(n["name"] for n in entry["nodes"] if "mesh" in n)
                check(named == sorted(MESHES), f"the data's 17 mesh nodes are the named ones ({named})")
                check(all(m[1] >= 1 for m in w["meshes"]), "every mesh has a material")
            for name, az, el in (("front", 0, 8), ("three_quarter", 50, 18), ("above", 20, 65)):
                page.evaluate(SHOT, [az, el])
                page.wait_for_timeout(500)
                page.screenshot(path=str(OUT / f"{tag}_{name}.png"))
                print("  shot", OUT / f"{tag}_{name}.png")

        # the picker's tile
        page.evaluate("c => wardrobe.show('sheep', c)", {"Back": None})
        page.click('#topics [data-t="Back"]')
        page.wait_for_selector('#pkBody[data-topic="Back"] .pk-cell')
        tile = page.evaluate("() => { const c = document.querySelector('#pkBody .pk-cell[data-item=\"aura_bloompulse\"]'); return c ? { img: !!c.querySelector('img') } : null; }")
        check(tile is not None and tile["img"], f"the Back picker has an aura_bloompulse tile with its icon ({tile})")
        b.close()
    check(not errors, f"no page errors, console errors or failed requests ({errors[:3]})")
    print("FAILED: " + "; ".join(fails) if fails else "all ok")
    sys.exit(1 if fails else 0)


main()
