r"""A skin (or the outfit's UV islands, numbered) on the hero from any side, also from above and below (2026-11-14, the
Bat's coat: "seen from behind / below, between the coat's two small spiky flaps"; island_shots only turns round the
hero). Each view is yaw:pitch (degrees; pitch < 0 = the camera below, looking up) and an optional zoom.

--islands colours every UV island of the outfit and writes its number where it shows (a ray per few pixels through the
page's own pieceAt-style ray, its uv -> the island), with a legend: number -> a sheet point (x, y on the game's sheet,
as wardrobe_bat_enemies.py's m((x, y)) takes it), its height range (z, bind pose) and its size. So the user can point
at a piece by number before anything is painted on it (the skill's rule 12).

  uv run --no-project --with pillow --with numpy --with scipy --with playwright python -I pipeline/wardrobe_skin_views.py
      bat royal <out dir> [--skin <name>=<png>]... [--head butterflyHood] [--prop <skin key>@<png>]... [--face 11]
      [--views 180:0,180:-35,0:-35] [--zoom 1.6] [--aim 0.6 | --at Head [--lift 0.1]] [--islands --cache <dir> --K 2]
Writes <out>/<name>_<yaw>_<pitch>.png per skin and view (and islands_*.png + islands_legend.txt), then one sheet.png
(a row per skin), or with --per-job [--cols 4] one sheet_<name>.png per skin (8 sides full body: --views 0:0,45:0,...,315:0)."""
import argparse, asyncio, base64, functools, http.server, sys, threading
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wardrobe_repaint as wr

ROOT = wr.ROOT


async def render(cls, outfit, jobs, views, out, head, props, face, zoom, aim, rays, at=None, lift=0.0):
    from playwright.async_api import async_playwright
    Q = type("Q", (http.server.SimpleHTTPRequestHandler,), {"log_message": lambda *a: None})
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Q, directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    hits = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        page = await (await b.new_context(viewport={"width": 1000, "height": 1000})).new_page()
        page.on("pageerror", lambda e: print("pageerror:", e))
        await page.goto(f"http://127.0.0.1:{srv.server_port}/wardrobe/")
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
        await page.add_style_tag(content="*{visibility:hidden!important} canvas{visibility:visible!important}")
        for name, files in jobs:
            skins = {k: "/" + Path(f).resolve().relative_to(ROOT).as_posix() for k, f in {**files, **props}.items()}
            await page.evaluate("""async ([cls, outfit, skins, head, face]) => {
              const { SKINS, scene, THREE } = wardrobe.debug(); SKINS.clear();
              scene.background = new THREE.Color(0xe6e1d8);
              for (const [k, url] of Object.entries(skins)) {
                const img = await createImageBitmap(await (await fetch(url)).blob()), c = new OffscreenCanvas(img.width, img.height);
                const g = c.getContext("2d"); g.drawImage(img, 0, 0);
                SKINS.set(k, { w: img.width, h: img.height, data: g.getImageData(0, 0, img.width, img.height).data });
              }
              await wardrobe.show(cls, {});
              if (face != null) wardrobe.debug().C.state.face = face;
              await wardrobe.setOutfit(outfit, 1);
              for (const s of ["Head", "R", "L", "Back"]) await wardrobe.show(cls, { [s]: s === "Head" ? head : null });
            }""", [cls, outfit, skins, head, face])
            for yaw, pitch in views:
                r = await page.evaluate("""async ([cls, yaw, pitch, zoom, aim, rays, bone, lift]) => {
                  await wardrobe.show(cls, {}, yaw);
                  const { camera, controls, renderer, scene, C, THREE } = wardrobe.debug();
                  // aim: the height (share of the hero's own height, 0 = feet) the camera looks at
                  const box = new THREE.Box3(); for (const m of C.meshes) box.expandByObject(m);
                  const t = controls.target.clone(); t.y = box.min.y + aim * (box.max.y - box.min.y);
                  if (bone) {                    // --at <bone>: look at that bone (the page's own target sits in front of the hero)
                    let b = null; for (const m of C.meshes) m.traverse(o => { if (!b && o.isSkinnedMesh) b = o.skeleton.bones.find(x => x.name === bone); });
                    if (b) { b.updateWorldMatrix(true, false); b.getWorldPosition(t); t.y += lift; }
                  }
                  const off = camera.position.clone().sub(controls.target), d = off.length() / zoom;
                  const a = yaw * Math.PI / 180, e = pitch * Math.PI / 180;
                  // the page's orbit limits would pull a view from far below or above back (and move the target)
                  Object.assign(controls, { minPolarAngle: 0, maxPolarAngle: Math.PI, minDistance: 0, maxDistance: Infinity, enableDamping: false });
                  controls.target.copy(t);
                  camera.position.set(t.x + d * Math.cos(e) * Math.sin(a), t.y + d * Math.sin(e), t.z + d * Math.cos(e) * Math.cos(a));
                  camera.lookAt(t); camera.updateMatrixWorld(); renderer.render(scene, camera);
                  // the shot is read here, in the same task as the render: the page's own loop (its orbit controls, its
                  // camera tweens) would move the camera again before a screenshot from outside
                  const png = renderer.domElement.toDataURL("image/png");
                  if (!rays) return { png };
                  const el = renderer.domElement, R = el.getBoundingClientRect(), ray = new THREE.Raycaster(), out = [];
                  for (const m of C.meshes) m.traverse(o => { if (o.isSkinnedMesh) { o.boundingSphere = null; o.boundingBox = null; } });
                  const st = rays;
                  for (let y = 0; y < R.height; y += st) for (let x = 0; x < R.width; x += st) {
                    ray.setFromCamera(new THREE.Vector2(x / R.width * 2 - 1, -y / R.height * 2 + 1), camera);
                    const h = ray.intersectObjects(C.meshes, true)[0];
                    if (h && h.uv) out.push(x, y, h.uv.x, h.uv.y);
                  }
                  return { png, w: R.width, h: R.height, pts: out };
                }""", [cls, yaw, pitch, zoom, aim, rays if name == "islands" else 0, at, lift])
                f = Path(out) / f"{name}_{yaw}_{pitch}.png"
                f.write_bytes(base64.b64decode(r["png"].split(",", 1)[1]))
                if "pts" in r:
                    hits[(yaw, pitch)] = r
            print("shot", name)
        await b.close()
    srv.shutdown()
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cls"); ap.add_argument("outfit"); ap.add_argument("out")
    ap.add_argument("--skin", action="append", default=[], help="<name>=<png>: the outfit's skin, one job per skin")
    ap.add_argument("--head"); ap.add_argument("--prop", action="append", default=[], help="<skin key>@<png>, worn in every job")
    ap.add_argument("--face", type=int); ap.add_argument("--views", default="180:0,180:-35,0:-35,135:-20,225:-20")
    ap.add_argument("--zoom", type=float, default=1.0); ap.add_argument("--aim", type=float, default=0.5)
    ap.add_argument("--at", help="look at this bone (Head, Spine1, ...) instead of --aim"); ap.add_argument("--lift", type=float, default=0.0, help="with --at: that much higher (the page's units)")
    ap.add_argument("--per-job", action="store_true"); ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--rays", type=int, default=4, help="with --islands: a ray every that many pixels (also saved: hits_<yaw>_<pitch>.npy = x, y, u, v)")
    ap.add_argument("--islands", action="store_true"); ap.add_argument("--cache"); ap.add_argument("--K", type=int, default=2)
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    views = [tuple(int(v) for v in s.split(":")) for s in a.views.split(",")]
    jobs = [(n, {f"{a.cls}|outfits|{a.outfit}|": f}) for n, f in (s.split("=", 1) for s in a.skin)]
    M = None
    if a.islands:
        import colorsys
        M = wr.cached_maps(a.cls, a.outfit, a.K, a.cache or out / "_cache")
        n = int(M.lab.max()) + 1
        pal = np.array([[int(c * 255) for c in colorsys.hsv_to_rgb((i * 0.381) % 1, 0.45 + 0.4 * (i % 2), 1.0 - 0.3 * (i % 3 == 0))] for i in range(n)], np.uint8)
        f = out / "_islands.png"
        Image.fromarray(pal[M.lab]).save(f)
        jobs.append(("islands", {f"{a.cls}|outfits|{a.outfit}|": f}))
    props = dict(s.split("@", 1) for s in a.prop)
    hits = asyncio.run(render(a.cls, a.outfit, jobs, views, out, a.head, props, a.face, a.zoom, a.aim, a.rays, a.at, a.lift))
    if M is not None:
        H, W = M.lab.shape
        for (yaw, pitch), r in hits.items():                    # the rays themselves: screen x, y, u, v per hit (what shows where)
            np.save(out / f"hits_{yaw}_{pitch}.npy", np.array(r["pts"], np.float32).reshape(-1, 4))
        font = ImageFont.truetype("arialbd.ttf", 22)
        seen = set()
        for (yaw, pitch), r in hits.items():
            pts = np.array(r["pts"], float).reshape(-1, 4)
            lab = M.lab[np.clip(((1 - pts[:, 3]) * H).astype(int), 0, H - 1), np.clip((pts[:, 2] * W).astype(int), 0, W - 1)]
            f = out / f"islands_{yaw}_{pitch}.png"
            im = Image.open(f).convert("RGB"); g = ImageDraw.Draw(im)
            sx, sy = im.width / r["w"], im.height / r["h"]
            for L in np.unique(lab):
                k = lab == L
                if k.sum() < 12:
                    continue
                seen.add(int(L))
                q = pts[k][np.argmin(((pts[k, :2] - pts[k, :2].mean(0)) ** 2).sum(1))]      # the hit nearest the centroid
                x, y, t = q[0] * sx, q[1] * sy, str(L)
                g.text((x, y), t, font=font, fill="white", anchor="mm", stroke_width=3, stroke_fill="black")
            im.save(f)
        lines = []
        for L in sorted(seen):
            k = (M.lab == L) & M.covered
            ys, xs = np.where(k)
            i = np.argmin((ys - ys.mean()) ** 2 + (xs - xs.mean()) ** 2)
            z = M.pos[..., 2][k]
            lines.append(f"{L:4d}  sheet ({xs[i] // a.K}, {ys[i] // a.K})  z {z.min():.2f}-{z.max():.2f}  {int(k.sum() / a.K ** 2)} texels")
        (out / "islands_legend.txt").write_text("\n".join(lines) + "\n", "utf-8")
        print("\n".join(lines))
    # one sheet: a row per job, a column per view, each cropped to the hero; with --per-job a sheet per job instead
    # (sheet_<name>.png, --cols views a row, one crop for all its views: the same scale from every side)
    names = [n for n, _ in jobs]
    def crop_box(ims):
        x0 = y0 = 10 ** 6; x1 = y1 = 0
        for im in ims:
            a_ = np.asarray(im).astype(int)
            ys, xs = np.where(np.abs(a_ - np.array([230, 225, 216])).max(-1) > 14)
            if len(xs):
                x0, x1, y0, y1 = min(x0, xs.min()), max(x1, xs.max()), min(y0, ys.min()), max(y1, ys.max())
        return x0, y0, x1, y1
    def fit(im, box, w, h):
        x0, y0, x1, y1 = box
        sc = min(w / (x1 - x0 + 20), h / (y1 - y0 + 20))
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        bx = (int(cx - w / sc / 2), int(cy - h / sc / 2), int(cx + w / sc / 2), int(cy + h / sc / 2))
        sq = Image.new("RGB", (bx[2] - bx[0], bx[3] - bx[1]), (230, 225, 216))      # the backdrop where the crop runs off the shot
        sq.paste(im, (-bx[0], -bx[1]))
        return sq.resize((w, h), Image.LANCZOS)
    font = ImageFont.truetype("arial.ttf", 18)
    if a.per_job:
        cw, ch = 360, 560
        rows_ = -(-len(views) // a.cols)
        for n in names:
            ims = [Image.open(out / f"{n}_{yaw}_{pitch}.png").convert("RGB") for yaw, pitch in views]
            box = crop_box(ims)
            sh = Image.new("RGB", (cw * a.cols, (ch + 26) * rows_ + 34), (230, 225, 216))
            g = ImageDraw.Draw(sh)
            g.text((8, 6), n, fill="black", font=ImageFont.truetype("arialbd.ttf", 22))
            for i, ((yaw, pitch), im) in enumerate(zip(views, ims)):
                x, y = (i % a.cols) * cw, 34 + (i // a.cols) * (ch + 26)
                sh.paste(fit(im, box, cw, ch), (x, y + 26))
                g.text((x + 6, y + 4), f"yaw {yaw}" + (f"  pitch {pitch}" if pitch else ""), fill="black", font=font)
            sh.save(out / f"sheet_{n}.png")
            print(out / f"sheet_{n}.png")
        return
    cell = 420
    sheet = Image.new("RGB", (cell * len(views), (cell + 26) * len(names)), (255, 255, 255))
    g = ImageDraw.Draw(sheet)
    for j, n in enumerate(names):
        for i, (yaw, pitch) in enumerate(views):
            im = Image.open(out / f"{n}_{yaw}_{pitch}.png").convert("RGB")
            box = crop_box([im])
            side = max(box[2] - box[0], box[3] - box[1])
            sheet.paste(fit(im, box, cell, cell) if box[2] > box[0] else im.resize((cell, cell)), (i * cell, j * (cell + 26) + 26))
            g.text((i * cell + 6, j * (cell + 26) + 3), f"{n}  yaw {yaw}  pitch {pitch}", fill="black", font=font)
    sheet.save(out / "sheet.png")
    print(out / "sheet.png")

if __name__ == "__main__":
    main()
