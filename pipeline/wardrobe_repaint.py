r"""A set repainted on the 3D surface (2026-11-12; user: a reference picture of a black school dress, white collar, red
ribbon, white cuffs, black knee socks, white shoes, "try using this reference for rabbit summer set, make sure it looks
good in 3D", "don't bake in the eyes"). Where wardrobe_reskin.py moves hues on the flat sheet, this knows what every
texel is: the outfit's mesh (o_<name>.bin) is drawn into the texture's UV space, so each texel has its place on the
body (x front, y left, z up, the bind pose) and its bone. A design then paints by body part and height (sleeves down
to the wrist, socks up to the knee) and keeps the original's painted shading: each area's luminance runs through a
three-colour ramp (shadow, base, light). The gutters between islands take their nearest island's paint (no seams).
The face block's eyes and mouth are the page's overlay (composeTexture): nothing is drawn there.

  uv run --no-project --with pillow --with numpy --with scipy --with playwright python -I pipeline/wardrobe_repaint.py [--preview]
Outputs plans/reskins/rabbit/summer_uniform_<A|B>/ (summer.png, Rabbit_summerHat.png: the originals' sizes) and, with
--preview, shots/ + uniform.html. A = the uniform on the pink Rabbit; B = black hair and ears, fair skin on the thighs too."""
import argparse, functools, http.server, json, sys, threading
from pathlib import Path
from types import SimpleNamespace
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "wardrobe" / "data"
sys.stdout.reconfigure(encoding="utf-8")


# ---------- what each texel is ----------
def texel_maps(cls, name, size):
    """bone (index into .bones), pos (x, y, z), lab (UV island) per texel; uncovered texels take the nearest covered one's."""
    o = next(x for x in json.loads((DATA / cls / "outfits.json").read_text("utf-8")) if x["name"] == name)
    buf = (DATA / cls / f"o_{name}.bin").read_bytes()
    W, H = size
    names = sorted({b for m in o["meshes"] for b in m["bones"]})
    bone, pos = np.full((H, W), -1, int), np.zeros((H, W, 3))
    for m in o["meshes"]:
        n = m["verts"]
        P = np.frombuffer(buf, np.float32, n * 3, m["pos"]).reshape(-1, 3)
        uv = np.frombuffer(buf, np.float32, n * 2, m["uv"]).reshape(-1, 2)
        J = np.frombuffer(buf, np.uint16, n * 4, m["j"]).reshape(-1, 4)
        Wt = np.frombuffer(buf, np.float32, n * 4, m["w"]).reshape(-1, 4)
        idx = np.frombuffer(buf, np.uint32, m["tris"] * 3, m["idx"]).reshape(-1, 3)
        gid = np.array([names.index(b) for b in m["bones"]])
        px = np.stack([uv[:, 0] * W, (1 - uv[:, 1]) * H], 1)          # the page's texture is flipped (flipY)
        for t in idx:
            a, b, c = px[t]
            x0, x1 = max(int(min(a[0], b[0], c[0])), 0), min(int(np.ceil(max(a[0], b[0], c[0]))), W - 1)
            y0, y1 = max(int(min(a[1], b[1], c[1])), 0), min(int(np.ceil(max(a[1], b[1], c[1]))), H - 1)
            den = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
            if x1 < x0 or y1 < y0 or abs(den) < 1e-9:
                continue
            xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            l0 = ((b[1] - c[1]) * (xs - c[0]) + (c[0] - b[0]) * (ys - c[1])) / den
            l1 = ((c[1] - a[1]) * (xs - c[0]) + (a[0] - c[0]) * (ys - c[1])) / den
            inside = (l0 >= -0.02) & (l1 >= -0.02) & (1 - l0 - l1 >= -0.02)
            yy, xx = np.where(inside)
            L = np.stack([l0[inside], l1[inside], 1 - l0[inside] - l1[inside]], 1)
            pos[yy + y0, xx + x0] = L @ P[t]
            bw = np.zeros((len(yy), len(names)))
            for k in range(3):
                for q in range(4):
                    bw[:, gid[J[t[k], q]]] += L[:, k] * Wt[t[k], q]
            bone[yy + y0, xx + x0] = bw.argmax(1)
    covered = bone >= 0
    lab, _ = ndimage.label(covered)
    iy, ix = ndimage.distance_transform_edt(~covered, return_distances=False, return_indices=True)
    return SimpleNamespace(bones=names, bone=bone[iy, ix], pos=pos[iy, ix], lab=lab[iy, ix], covered=covered)


# ---------- colour ----------
def hsv(rgb):
    a = rgb / 255.0
    mx, mn = a.max(-1), a.min(-1)
    d = mx - mn
    safe = np.where(d > 1e-6, d, 1)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    h = np.select([d <= 1e-6, mx == r, mx == g], [0, ((g - b) / safe) % 6, (b - r) / safe + 2], (r - g) / safe + 4) * 60
    return h, np.where(mx > 0, d / np.where(mx > 0, mx, 1), 0), mx


hd = lambda h, c: np.abs((h - c + 180) % 360 - 180)
hexc = lambda s: np.array([int(s[i:i + 2], 16) for i in (1, 3, 5)], float)
sstep = lambda x, a, b: np.clip((x - a) / (b - a), 0, 1) ** 2 * (3 - 2 * np.clip((x - a) / (b - a), 0, 1))


def ramp(t, cols):
    """t 0..1 -> shadow, base (t = 0.5), light."""
    c0, c1, c2 = map(hexc, cols)
    t = t[..., None]
    return np.where(t < 0.5, c0 + (c1 - c0) * t * 2, c1 + (c2 - c1) * (t * 2 - 1))


def tone(L, ref, lo=3, hi=99.5):
    """The area's luminance as 0..1: its median = 0.5 (the base colour), so the painted folds and rims keep their place."""
    a, m, b = np.percentile(L[ref], [lo, 50, hi])
    span = 0.12                                  # a floor: a nearly flat area is not stretched into noise
    return np.clip(np.where(L < m, 0.5 * (L - a) / max(m - a, span), 0.5 + 0.5 * (L - m) / max(b - m, span)), 0, 1)


BLACK = ("#141217", "#2b282f", "#57515f")       # the dress: near black, a cool violet lift in the light
SOCK = ("#100f13", "#232127", "#454049")
WHITE = ("#a6a1b3", "#f0eff4", "#ffffff")
RED = ("#5c060c", "#b00c17", "#e8414c")
SOLE = ("#18171b", "#34323a", "#5d5a66")
METAL = ("#2a272c", "#6f6a73", "#c9c4cc")
HAIR = ("#0f0d14", "#25222e", "#5a5470")        # black hair with a violet sheen
SKIN = ("#d1a48f", "#f6dccb", "#fff3e8")        # the face's own cream, for B's thighs
EAR_IN = ("#4a2a36", "#a86f7e", "#d9a9b3")
LINE = "#bdb8c9"


def uniform(variant):
    """The Rabbit's summer outfit as the reference's uniform -> (outfit RGBA, hat RGBA)."""
    im = Image.open(DATA / "rabbit" / "tex" / "summer1.webp").convert("RGBA")
    src = np.asarray(im).astype(float)
    rgb, out = src[..., :3], src[..., :3].copy()
    M = texel_maps("rabbit", "summer", im.size)
    h, s, v = hsv(rgb)
    # smoothed where it is flat: the webp's blocks are invisible on white cloth and plain to see once that cloth is near
    # black; a fold or a trim line (a real step in luminance) keeps its edge
    L0 = rgb @ [0.299, 0.587, 0.114] / 255
    G = ndimage.gaussian_filter(L0, 2.5)
    # (the edge mask reaches as far as the blur does, or a small mark grows a dark halo around itself)
    edge = ndimage.gaussian_filter(sstep(ndimage.maximum_filter(np.abs(L0 - G), 13), 0.025, 0.07), 1.5)
    L = G * (1 - edge) + ndimage.gaussian_filter(ndimage.median_filter(L0, 3), 0.8) * edge
    isl = lambda x, y: M.lab == M.lab[y, x]
    X, Y, Z = M.pos[..., 0], np.abs(M.pos[..., 1]), M.pos[..., 2]
    pink = (hd(h, 350) < 30) & (s > 0.2) & (v > 0.3)
    navy_k = sstep(s, 0.18, 0.4) * (hd(h, 225) < 40)           # how blue (soft, for the anti-aliased edges)
    gold_k = sstep(s, 0.25, 0.45) * (hd(h, 42) < 18) * (v > 0.4)

    def mix(m, col, k=1.0):                                    # paint col over the area m, k = how much (a soft mask)
        k = np.broadcast_to(np.asarray(k, float), m.shape)[..., None]
        out[m] = (out * (1 - k) + col * k)[m]

    # the dress: white cloth -> black; the navy trim and stripes fall to the ramp's shadow (tone on tone); buttons dark metal
    dress = isl(250, 330)
    cloth = dress & ~pink
    mix(cloth, ramp(tone(L, dress & (s < 0.2) & (v > 0.5)), BLACK))
    # the striped inset under the coat's front (slate bars on white, sheet x 305-348, y 283-412): one plain black, as the
    # reference's dress is. ponytail: a box on the sheet, this outfit only; by 3D position if another design needs it
    yy, xx = np.mgrid[:im.size[1], :im.size[0]]
    bars = sstep(-L0, -0.62, -0.45) * ((xx > 305) & (xx < 348) & (yy > 283) & (yy < 412))
    mix(cloth, ramp(np.full(L.shape, 0.42), BLACK), ndimage.gaussian_filter(bars, 0.7))
    mix(dress, ramp(tone(L, dress & (gold_k > 0.5)), METAL), gold_k)
    # the shoulders: the summer dress is sleeveless, its bare shoulder tops (|y| 0.04-0.09, z 0.83-0.90) are fur on two
    # islands (the dress's top edge, and a strip of its own); the reference's dress covers them (user: "at the shoulder,
    # it is still rabbit skin color")
    pink_k = sstep(s, 0.2, 0.3) * (hd(h, 350) < 30)
    for sh in (dress, isl(360, 252)):
        mix(sh, ramp(np.clip(0.5 + (tone(L, sh & pink) - 0.5) * 0.6, 0.42, 1), BLACK), pink_k)
    under = isl(450, 485)                                       # the skirt's inside
    mix(under, ramp(tone(L, under) * 0.6, BLACK))

    # the sailor collar: navy -> white, its white line a soft grey
    for seed in ((300, 480), (358, 455)):
        col = isl(*seed)
        line = sstep(v, 0.6, 0.85) * (1 - sstep(s, 0.15, 0.35))
        mix(col, ramp(np.clip(0.5 + (tone(L, col & (navy_k > 0.5)) - 0.5) * 0.55, 0.25, 0.8), WHITE))
        mix(col, hexc(LINE), line)

    # long sleeves on the arms, a white cuff at the wrist (the right wrist's band is the cuff itself)
    arm = isl(470, 60)
    t = np.clip(0.5 + (tone(L, arm & pink) - 0.5) * 0.6, 0.42, 1)   # the fur's shading, calmer (it is cloth now); no elbow dimples
    cuff = sstep(Y, 0.296, 0.302)
    mix(arm, ramp(t, BLACK))
    mix(arm, ramp(np.clip(t, 0.25, 1), WHITE), cuff)
    mix(arm, hexc("#8d8899"), sstep(Y, 0.297, 0.301) * (1 - sstep(Y, 0.306, 0.312)) * 0.9)     # the cuff's seam
    band = isl(450, 415)
    mix(band, ramp(np.clip(tone(L, band & (navy_k > 0.5)), 0.3, 0.62), WHITE))

    # knee socks, the foot inside the sandal too; a ribbed top
    leg = isl(470, 200)
    sock = sstep(-Z, -0.374, -0.368)
    t = tone(L, leg & pink)
    mix(leg, ramp(t, SOCK), sock)
    mix(leg, hexc("#4a4650"), sstep(Z, 0.352, 0.356) * sock * 0.8)
    for seed in ((360, 190), (360, 231)):
        foot = isl(*seed)
        mix(foot, ramp(tone(L, foot), SOCK))

    # the shoes stay white; navy trim and soles -> charcoal, the buttons dark metal
    shoe = isl(350, 300)
    mix(shoe, ramp(tone(L, shoe & (navy_k > 0.5)), SOLE), navy_k)
    mix(shoe, ramp(tone(L, shoe & (gold_k > 0.5)), METAL), gold_k)
    sole = isl(297, 180)
    mix(sole, ramp(tone(L, sole) * 0.7, SOLE))

    # the ear's ribbon: blue -> the reference's red, its white frill kept
    for seed in ((470, 327), (470, 300)):
        bow = isl(*seed)
        mix(bow, ramp(tone(L, bow & (navy_k > 0.5)), RED), navy_k)

    if variant == "B":                                          # the full look: black hair and ears, fair skin
        face = isl(70, 60) | isl(45, 145)
        head = np.isin(M.bone, [i for i, b in enumerate(M.bones) if b in ("Head", "Neck")])
        hair = (head & ~face) | isl(40, 300) | isl(60, 470)    # every head island but the face, and the ears' outside
        red_k = sstep(s, 0.18, 0.32) * (hd(h, 352) < 35)
        mix(hair, ramp(tone(L, isl(250, 70) & pink), HAIR), red_k)
        inner = isl(120, 300) | isl(160, 470)                   # the ears' inside: a dusty rose beside black, not the fur's hot pink
        mix(inner, ramp(tone(L, inner & pink), EAR_IN), red_k)
        # the fringe's edge painted on the face island (a stricter test: the forehead's peach shade is skin)
        mix(face, ramp(tone(L, isl(250, 70) & pink), HAIR), sstep(s, 0.3, 0.45) * (hd(h, 352) < 30))
        mix(face & ~M.covered, ramp(tone(L, isl(250, 70) & pink), HAIR), red_k)      # and its gutter: no pink seam at the hairline
        skin = leg & pink                                       # the thighs between the hem and the socks
        mix(skin, ramp(tone(L, leg & pink), SKIN), (1 - sock) * sstep(s, 0.2, 0.3))

    res = np.dstack([np.clip(out, 0, 255), src[..., 3]]).astype(np.uint8)

    # the cap to match: black crown, white band, the red ribbon as it is
    him = Image.open(DATA / "props" / "tex" / "Rabbit_summerHat.png").convert("RGBA")
    a = np.asarray(him).astype(float)
    c, o2 = a[..., :3], a[..., :3].copy()
    hh, hs, hv = hsv(c)
    HL = c @ [0.299, 0.587, 0.114] / 255
    white = (hs < 0.2)
    nk = sstep(hs, 0.2, 0.45) * (hd(hh, 225) < 40)
    o2[...] = np.where(white[..., None], ramp(tone(HL, white & (hv > 0.5)), BLACK), o2)
    o2 = o2 * (1 - nk[..., None]) + ramp(tone(HL, nk > 0.5), WHITE) * nk[..., None]
    hat = np.dstack([np.clip(o2, 0, 255), a[..., 3]]).astype(np.uint8)
    return res, hat


# ---------- on the hero ----------
async def shots(variants, out, yaws=((20, "front"), (110, "left"), (200, "back"), (290, "right"))):
    from playwright.async_api import async_playwright
    Q = type("Q", (http.server.SimpleHTTPRequestHandler,), {"log_message": lambda *a: None})
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Q, directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    (out / "shots").mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        page = await (await b.new_context(viewport={"width": 1400, "height": 1100})).new_page()
        page.on("pageerror", lambda e: print("pageerror:", e))
        await page.goto(f"http://127.0.0.1:{srv.server_port}/wardrobe/")
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
        await page.add_style_tag(content="*{visibility:hidden!important} canvas{visibility:visible!important}")
        for name, files, hat in variants:
            skins = {k: "/" + f.relative_to(ROOT).as_posix() for k, f in files.items()}
            await page.evaluate("""async ([skins, hat]) => {
              const { SKINS, scene, THREE } = wardrobe.debug(); SKINS.clear();
              scene.background = new THREE.Color(0xe6e1d8);
              for (const [k, url] of Object.entries(skins)) {
                const img = await createImageBitmap(await (await fetch(url)).blob()), c = new OffscreenCanvas(img.width, img.height);
                const g = c.getContext("2d"); g.drawImage(img, 0, 0);
                SKINS.set(k, { w: img.width, h: img.height, data: g.getImageData(0, 0, img.width, img.height).data });
              }
              await wardrobe.show("rabbit", {}); await wardrobe.setOutfit("summer", 1);
              for (const s of ["Head", "R", "L", "Back"]) await wardrobe.show("rabbit", { [s]: s === "Head" && hat ? "summerHat" : null });
            }""", [skins, hat])
            for yaw, side in yaws:
                await page.evaluate("y => wardrobe.show('rabbit', {}, y)", yaw)
                await page.wait_for_timeout(350)
                f = out / "shots" / f"{name}_{side}.png"
                await page.locator("canvas").first.screenshot(path=str(f))
                crop(f)
            print("shot", name)
        await b.close()
    srv.shutdown()


def crop(f, pad=14, size=640):
    im = Image.open(f).convert("RGB")
    a = np.asarray(im).astype(int)
    ys, xs = np.where(np.abs(a - a[2, 2]).max(-1) > 14)
    if not len(xs):
        return
    x0, x1, y0, y1 = max(xs.min() - pad, 0), min(xs.max() + pad, a.shape[1]), max(ys.min() - pad, 0), min(ys.max() + pad, a.shape[0])
    side = max(x1 - x0, y1 - y0)
    sq = Image.new("RGB", (side, side), tuple(a[2, 2]))
    sq.paste(im.crop((x0, y0, x1, y1)), ((side - (x1 - x0)) // 2, (side - (y1 - y0)) // 2))
    sq.resize((size, size), Image.LANCZOS).save(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", action="store_true")
    a = ap.parse_args()
    out = ROOT / "plans" / "reskins" / "rabbit"
    variants = [("original", {}, True)]
    for v in ("A", "B"):
        d = out / f"summer_uniform_{v}"
        d.mkdir(parents=True, exist_ok=True)
        outfit, hat = uniform(v)
        orig = np.asarray(Image.open(DATA / "rabbit" / "tex" / "summer1.webp").convert("RGBA"))
        assert outfit.shape == orig.shape and (outfit[..., 3] == orig[..., 3]).all(), "a skin keeps the original's size and alpha"
        # the face presets' own pixels span x 24-114, y 18-87; B darkens the hairline's shade in its top rows (y < 30) only
        assert (outfit[30:88, 24:115] == orig[30:88, 24:115]).all(), "nothing painted where the face preset draws the eyes and mouth"
        Image.fromarray(outfit, "RGBA").save(d / "summer.png")
        Image.fromarray(hat, "RGBA").save(d / "Rabbit_summerHat.png")
        files = {"rabbit|outfits|summer|": d / "summer.png", "rabbit|accessories|summerHat|Rabbit_summerHat.png": d / "Rabbit_summerHat.png"}
        variants += [(f"uniform_{v}", files, False), (f"uniform_{v}_hat", files, True)]
        print("painted", d.relative_to(ROOT))
    if a.preview:
        import asyncio
        asyncio.run(shots(variants, out))
        label = {"original": "ของเดิม", "uniform_A": "A · ชุดนักเรียน บนกระต่ายสีชมพูเดิม", "uniform_A_hat": "A + หมวก",
                 "uniform_B": "B · ผมและหูดำ ผิวขาว", "uniform_B_hat": "B + หมวก"}
        cells = "".join(f'<figure>{"".join(f"<img src=shots/{n}_{s}.png>" for s in ("front", "left", "back", "right"))}<figcaption>{label[n]}</figcaption></figure>'
                        for n, _, _ in variants)
        (out / "uniform.html").write_text(f"""<!doctype html><meta charset=utf-8><title>Rabbit: uniform</title>
<style>body{{font-family:system-ui,sans-serif;background:#f4f1ea;margin:16px}}figure{{margin:0 0 16px;background:#fff;border-radius:10px;padding:8px}}
img{{width:24%;min-width:200px}}figcaption{{font-weight:600;margin:4px}}</style><h1>กระต่าย · ชุด Summer เป็นชุดนักเรียน</h1>{cells}""", encoding="utf-8")
        print("preview:", (out / "uniform.html").as_uri())


if __name__ == "__main__":
    main()
