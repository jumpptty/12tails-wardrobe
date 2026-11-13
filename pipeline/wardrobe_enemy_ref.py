r"""An in-game enemy as a 3D reference for a reskin (2026-11-13; user: "it will be 3D model reference this time ... in-game
enemy Lady Noir and Bat Cult"): the enemy's mesh from BB's game files (UnityPy), its texture from the Bible's rip, shot
from eight sides in a bare three.js page (unlit: the texture's own paint), one labelled sheet per enemy.
  uv run --no-project --with UnityPy --with pillow --with playwright python -I pipeline/wardrobe_enemy_ref.py <out dir> LadyNoir BatCult
A name N reads the meshes whose name starts with N (N_tri: the body) and the rip's Texture2D/N.png; extra pieces as
N+Mesh:Texture (LadyNoir+NoirWand:NoirWand); N@<axis><degrees> turns the model first (BatCult@x-90: its mesh has z up in the
bind pose). Outputs <out>/<N>.obj, <N>_sheet.png. The bind pose, no animation."""
import asyncio, functools, http.server, json, sys, threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIBLE = next(p for p in (Path(r"D:\12tails"), Path.home() / "Desktop" / "12tails") if p.exists())
DATA = next(p for p in (BIBLE / "12TailsOnline_Data", BIBLE / "12TailsReborn_Data") if p.exists())
RIP = BIBLE / "RippedAssets" / "ExportedProject" / "Assets"
OUT = Path(sys.argv[1]).resolve()
NAMES = sys.argv[2:]

PAGE = """<!doctype html><meta charset=utf-8><style>html,body{margin:0;background:#e6e1d8}canvas{display:block}</style>
<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js"}}</script>
<script type="module">
import * as THREE from "three";
const q = new URLSearchParams(location.search), parts = JSON.parse(q.get("parts"));
const r = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true }); r.setSize(700, 900); document.body.append(r.domElement);
const scene = new THREE.Scene(); scene.background = new THREE.Color(0xe6e1d8);
const cam = new THREE.PerspectiveCamera(28, 700 / 900, 0.01, 100), box = new THREE.Box3(), grp = new THREE.Group(); scene.add(grp);
for (const [obj, tex] of parts) {
  const txt = await (await fetch(obj)).text(), P = [], T = [], pos = [], uv = [];
  for (const l of txt.split("\\n")) { const a = l.trim().split(/\\s+/);
    if (a[0] === "v") P.push(a.slice(1, 4).map(Number)); else if (a[0] === "vt") T.push(a.slice(1, 3).map(Number));
    else if (a[0] === "f") for (const c of a.slice(1, 4)) { const [i, j] = c.split("/").map(Number); pos.push(...P[i - 1]); uv.push(...(T[(j || i) - 1] || [0, 0])); } }
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2));
  const map = await new THREE.TextureLoader().loadAsync(tex); map.colorSpace = THREE.SRGBColorSpace;
  grp.add(new THREE.Mesh(g, new THREE.MeshBasicMaterial({ map, side: THREE.DoubleSide })));
}
const turn = q.get("turn") || "x0"; grp.rotation[turn[0]] = +turn.slice(1) * Math.PI / 180; grp.updateMatrixWorld(true);
box.setFromObject(grp); const c = box.getCenter(new THREE.Vector3()), s = box.getSize(new THREE.Vector3()), d = Math.max(s.y, s.x, s.z) * 2.25;
window.shoot = yaw => { const a = yaw * Math.PI / 180; cam.position.set(c.x + d * Math.sin(a), c.y + s.y * 0.05, c.z + d * Math.cos(a)); cam.lookAt(c); r.render(scene, cam); };
window.size = [s.x, s.y, s.z]; window.ready = true;
</script>"""


TURN = {}


def meshes():
    import UnityPy
    want = {}
    for n in NAMES:
        n, _, rz = n.partition("@")
        body, *more = n.split("+")
        TURN[body] = rz or "x0"
        want[body] = [(body, body)] + [tuple(m.split(":")) for m in more]
    env = UnityPy.load(str(DATA))
    found = {}
    for o in env.objects:
        if o.type.name != "Mesh":
            continue
        name = o.peek_name() or ""
        for body, parts in want.items():
            for mesh, tex in parts:
                if name == mesh or name.startswith(mesh + "_") and mesh == body:
                    f = OUT / f"{name}.obj"
                    f.write_text(o.read().export(), encoding="utf-8")
                    found.setdefault(body, []).append((f.name, tex))
    return found


async def shoot(found):
    from playwright.async_api import async_playwright
    from PIL import Image, ImageDraw
    Q = type("Q", (http.server.SimpleHTTPRequestHandler,), {"log_message": lambda *a: None})
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Q, directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    (OUT / "_ref.html").write_text(PAGE, encoding="utf-8")
    rel = "/" + OUT.relative_to(ROOT).as_posix()
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        page = await (await b.new_context(viewport={"width": 700, "height": 900})).new_page()
        page.on("pageerror", lambda e: print("pageerror:", e))
        for body, parts in found.items():
            for _, tex in parts:
                (OUT / f"{tex}.png").write_bytes((RIP / "Texture2D" / f"{tex}.png").read_bytes())
            arg = json.dumps([[f"{rel}/{f}", f"{rel}/{t}.png"] for f, t in parts])
            await page.goto(f"http://127.0.0.1:{srv.server_port}{rel}/_ref.html?turn={TURN[body]}&parts={arg}")
            await page.wait_for_function("window.ready", timeout=60000)
            print(body, "size (x, y, z):", [round(v, 3) for v in await page.evaluate("window.size")], "parts:", [f for f, _ in parts])
            yaws = list(range(0, 360, 45))
            sheet = Image.new("RGB", (700 * 4, 900 * 2 + 30), "white")
            for i, y in enumerate(yaws):
                await page.evaluate("y => shoot(y)", y)
                f = OUT / f"_{body}_{y}.png"
                await page.locator("canvas").screenshot(path=str(f))
                sheet.paste(Image.open(f), ((i % 4) * 700, 30 + (i // 4) * 900))
                f.unlink()
            ImageDraw.Draw(sheet).text((8, 8), f"{body}: yaw 0 45 90 135 / 180 225 270 315", fill="black")
            sheet.save(OUT / f"{body}_sheet.png")
            print(OUT / f"{body}_sheet.png")
        await b.close()
    srv.shutdown()


OUT.mkdir(parents=True, exist_ok=True)
found = meshes()
assert found, f"no mesh named {NAMES} in {DATA}"
asyncio.run(shoot(found))
