r"""Themed recolours of a class's outfit sets (2026-11-12; user: "reskin the textures, 3 variants each for Rabbit, legend,
summer set, royal and Ant"; then "Whole set", "Themed recolours", "Preview page first"). Each variant recolours the
set's outfit (colour 1) and its pieces (hat, gun, trinket) with one palette, so the set reads as one theme:
  - the outfit's body (fur, face, hair) is left alone: a pixel is body when it equals the median of all the class's
    outfits, or when the outfit's colour options change it (they recolour the fur); closed and opened to drop specks
  - a rule moves one source hue band to a target hue; with "dark" / "bright" it splits the band by value (a dark base
    and a glowing trim of one hue); a neutral rule tints whites / greys / blacks; shading and local hue variation stay
Outputs plans/reskins/<cls>/<set>_<n>/<texture>.png at the original's size (the community-skin rule) and, with
--preview, a shot of every variant on the hero (the local page, headless) and plans/reskins/<cls>/preview.html.
  uv run --no-project --with pillow --with numpy --with playwright python -I pipeline/wardrobe_reskin.py rabbit [--preview]"""
import argparse, functools, http.server, json, sys, threading
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "wardrobe" / "data"
sys.stdout.reconfigure(encoding="utf-8")

# hue in degrees; s = saturation multiplier, sa = added, vm = value multiplier, va = added; dark / bright split by value
SETS = {"rabbit": {
    "legend": {"pieces": {"Head": "legendHelmet", "R": "legendGun", "Back": "legendTrinket"}, "themes": [
        ("เพลิงนิล", [dict(h=205, w=40, dark=dict(h=20, s=0.45, vm=0.9), bright=dict(h=30, s=1.15, vm=1.05), v0=0.25, v1=0.55)]),
        ("อเมทิสต์", [dict(h=205, w=40, dark=dict(h=268, s=0.9), bright=dict(h=300, s=1.0, vm=1.05), v0=0.25, v1=0.55)]),
        ("มรกต", [dict(h=205, w=40, dark=dict(h=165, s=0.8, vm=0.95), bright=dict(h=95, s=1.0, vm=1.05), v0=0.25, v1=0.55)]),
    ]},
    "summer": {"pieces": {"Head": "summerHat"}, "themes": [
        ("ซันเซ็ต", [dict(h=225, w=30, to=dict(h=182, s=0.9, vm=1.1)), dict(h=355, w=25, to=dict(h=22, s=1.0, vm=1.05)),
                     dict(neutral=0.2, to=dict(h=40, s=1.0, sa=0.13))]),
        ("พาสเทล", [dict(h=225, w=30, to=dict(h=158, s=0.55, vm=1.35, va=0.05)), dict(h=355, w=25, to=dict(h=335, s=0.6, vm=1.2)),
                    dict(neutral=0.2, to=dict(h=270, s=1.0, sa=0.07))]),
        ("ราตรี", [dict(h=225, w=30, to=dict(h=44, s=0.85, vm=1.7)), dict(h=355, w=25, to=dict(h=350, s=1.0, vm=0.85)),
                   dict(neutral=0.2, to=dict(h=230, s=1.0, sa=0.12, vm=0.28, va=0.06))]),
    ]},
    "royal": {"pieces": {"Head": "royalHat", "R": "royalGun"}, "themes": [
        ("ไพลิน", [dict(h=318, w=50, dark=dict(h=225, s=1.0), bright=dict(h=205, s=0.45, vm=1.05), v0=0.45, v1=0.7),
                   dict(h=52, w=22, to=dict(h=210, s=0.25, vm=1.08))]),
        ("มรกตทอง", [dict(h=318, w=50, dark=dict(h=150, s=0.9, vm=0.9), bright=dict(h=48, s=0.75, vm=1.05), v0=0.45, v1=0.7),
                     dict(h=52, w=22, to=dict(h=44, s=2.2, vm=1.0))]),
        ("ทับทิมดำ", [dict(h=318, w=50, dark=dict(h=330, s=0.25, vm=0.4), bright=dict(h=352, s=1.25, vm=0.95), v0=0.45, v1=0.7),
                      dict(h=52, w=22, to=dict(h=44, s=2.2, vm=1.0))]),
    ]},
    "ant": {"pieces": {"Head": "antHelmet", "R": "antShotgun"}, "themes": [
        ("แตนทอง", [dict(h=2, w=28, to=dict(h=44, s=1.0, vm=1.3)), dict(h=232, w=25, to=dict(h=8, s=1.0, vm=1.1))]),
        ("ด้วงเขียว", [dict(h=2, w=28, to=dict(h=135, s=0.85, vm=0.95)), dict(h=232, w=25, to=dict(h=35, s=1.0, vm=1.2))]),
        ("โคบอลต์", [dict(h=2, w=28, to=dict(h=218, s=0.95, vm=1.0)), dict(h=232, w=25, to=dict(h=25, s=1.0, vm=1.25))]),
    ]},
}}


def rgb2hsv(a):
    a = a / 255.0
    mx, mn = a.max(-1), a.min(-1)
    d = mx - mn
    safe = np.where(d > 1e-6, d, 1)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    h = np.select([d <= 1e-6, mx == r, mx == g], [0, ((g - b) / safe) % 6, (b - r) / safe + 2], (r - g) / safe + 4) * 60
    return h, np.where(mx > 0, d / np.where(mx > 0, mx, 1), 0), mx


def hsv2rgb(h, s, v):
    h = (h % 360) / 60
    i = np.floor(h).astype(int) % 6
    f = h - np.floor(h)
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    r = np.choose(i, [v, q, p, p, t, v]); g = np.choose(i, [t, v, v, q, p, p]); b = np.choose(i, [p, p, t, v, v, q])
    return np.clip(np.stack([r, g, b], -1) * 255, 0, 255)


def hdist(a, b):
    return np.abs((a - b + 180) % 360 - 180)


def target(h, s, v, src, t):
    """One band's pixels moved to the target: the hue variation inside the band kept at half strength."""
    dh = ((h - src + 180) % 360 - 180) * 0.5 if src is not None else 0
    s2 = np.clip(s * t.get("s", 1) + t.get("sa", 0), 0, 1)
    v2 = np.clip(v * t.get("vm", 1) + t.get("va", 0), 0, 1)
    return hsv2rgb(t["h"] + dh, s2, v2)


def recolor(rgb, rules, keep=None):
    """rgb: HxWx3 uint8 -> the themed copy; keep: a mask of pixels left alone (the body)."""
    h, s, v = rgb2hsv(rgb.astype(float))
    out, wsum = np.zeros(rgb.shape, float), np.zeros(rgb.shape[:2])
    for r in rules:
        if "neutral" in r:
            w = np.clip(1 - s / r["neutral"], 0, 1)
            col = target(h, s, v, None, r["to"])
        else:
            w = np.clip(1 - hdist(h, r["h"]) / r["w"], 0, 1) ** 0.6 * np.clip((s - 0.12) / 0.1, 0, 1)
            if "to" in r:
                col = target(h, s, v, r["h"], r["to"])
            else:
                k = np.clip((v - r["v0"]) / (r["v1"] - r["v0"]), 0, 1)[..., None]
                col = target(h, s, v, r["h"], r["dark"]) * (1 - k) + target(h, s, v, r["h"], r["bright"]) * k
        out += col * w[..., None]; wsum += w
    wsum3 = wsum[..., None]
    res = np.where(wsum3 > 0, out / np.maximum(wsum3, 1e-6) * np.minimum(wsum3, 1) + rgb * (1 - np.minimum(wsum3, 1)), rgb)
    if keep is not None:
        res[keep] = rgb[keep]
    return res.astype(np.uint8)


@functools.cache
def outfit_median(cls, size):
    names = [o["name"] for o in json.loads((DATA / cls / "outfits.json").read_text("utf-8")) if o.get("colors") and not o.get("tto")]
    return np.median(np.stack([np.asarray(Image.open(DATA / cls / "tex" / f"{n}1.webp").convert("RGB").resize(size)).astype(np.int16)
                               for n in names if (DATA / cls / "tex" / f"{n}1.webp").exists()]), 0)


def body_mask(cls, name):
    """The outfit texture's body (fur, face, hair): equal to the class's median outfit, or changed by a colour option."""
    o = next(x for x in json.loads((DATA / cls / "outfits.json").read_text("utf-8")) if x["name"] == name)
    L = lambda c: np.asarray(Image.open(DATA / cls / "tex" / f"{name}{c}.webp").convert("RGB")).astype(np.int16)
    a = L(o["colors"][0])
    m = np.abs(a - outfit_median(cls, a.shape[1::-1])).max(-1) < 20
    for c in o["colors"][1:]:
        m |= np.abs(a - L(c)).max(-1) > 30
    im = Image.fromarray((m * 255).astype("uint8"))
    im = im.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(3))   # close
    im = im.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(5))                                      # open: specks go
    return np.asarray(im) > 128, o["colors"][0]


def prop_tex(cls, kind, item):
    for owner in (cls, "all"):
        p = next((x for x in json.loads((DATA / owner / f"props_{kind}.json").read_text("utf-8")) if x["name"] == item), None) \
            if (DATA / owner / f"props_{kind}.json").exists() else None
        if p:
            return sorted({m["tex"] for n in p.get("nodes", []) for m in n.get("mats") or [] if m.get("tex")})
    raise SystemExit(f"{cls} has no {kind} piece {item}")


KIND = {"Head": "accessories", "R": "weapons", "L": "weapons", "Back": "trinkets"}


def build(cls, out):
    """Every variant's textures -> out/<set>_<n>/; returns the variants for the preview."""
    made = []
    for name, st in SETS[cls].items():
        keep, color = body_mask(cls, name)
        src = {"": (Image.open(DATA / cls / "tex" / f"{name}{color}.webp").convert("RGBA"), keep)}
        for slot, item in st["pieces"].items():
            for t in prop_tex(cls, KIND[slot], item):
                src[t] = (Image.open(DATA / "props" / "tex" / t).convert("RGBA"), None)
        for n, (title, rules) in enumerate(st["themes"], 1):
            d = out / f"{name}_{n}"
            d.mkdir(parents=True, exist_ok=True)
            files = {}
            for t, (im, k) in src.items():
                a = np.asarray(im)
                res = np.dstack([recolor(a[..., :3], rules, k), a[..., 3]])
                f = d / (f"{name}.png" if t == "" else t)
                Image.fromarray(res, "RGBA").save(f)
                files[t] = f
            made.append({"set": name, "n": n, "title": title, "pieces": st["pieces"], "files": files})
            print(f"{name}_{n} {title}: {len(files)} textures")
    return made


async def shots(cls, made, out):
    """Each variant (and each set's original) on the hero, front and back, from the local page (headless)."""
    from playwright.async_api import async_playwright
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(type("Q", (http.server.SimpleHTTPRequestHandler,),
                                          {"log_message": lambda *a: None}), directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_port}/"
    (out / "shots").mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        page = await (await b.new_context(viewport={"width": 1400, "height": 1000})).new_page()
        page.on("pageerror", lambda e: print("pageerror:", e))
        await page.goto(base + "wardrobe/")
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
        await page.add_style_tag(content="*{visibility:hidden!important} canvas{visibility:visible!important}")   # the 3D view only
        sets = {}
        for v in made:
            sets.setdefault(v["set"], []).append(v)
        for name, vs in sets.items():
            for v in [{"set": name, "n": 0, "pieces": vs[0]["pieces"], "files": {}}] + vs:
                skins = {(f"{cls}|outfits|{name}|" if t == "" else f"{cls}|{KIND[s]}|{i}|{t}"): "/" + f.relative_to(ROOT).as_posix()
                         for t, f in v["files"].items() for s, i in ([("", "")] if t == "" else
                         [(s, i) for s, i in v["pieces"].items() if t in prop_tex(cls, KIND[s], i)])}
                await page.evaluate("""async ([cls, name, pieces, skins]) => {
                  const { SKINS } = wardrobe.debug(); SKINS.clear();
                  for (const [k, url] of Object.entries(skins)) {
                    const img = await createImageBitmap(await (await fetch(url)).blob()), c = new OffscreenCanvas(img.width, img.height);
                    const g = c.getContext("2d"); g.drawImage(img, 0, 0);
                    SKINS.set(k, { w: img.width, h: img.height, data: g.getImageData(0, 0, img.width, img.height).data });
                  }
                  await wardrobe.show(cls, {}); await wardrobe.setOutfit(name, 1);
                  for (const s of ["Head", "R", "L", "Back"]) await wardrobe.show(cls, { [s]: pieces[s] || null });
                }""", [cls, name, v["pieces"], skins])
                for yaw, side in ((20, "front"), (200, "back")):
                    await page.evaluate("([c, y]) => wardrobe.show(c, {}, y)", [cls, yaw])
                    await page.wait_for_timeout(400)
                    f = out / "shots" / f"{name}_{v['n']}_{side}.png"
                    await page.locator("canvas").first.screenshot(path=str(f))
                    crop(f)
                print("shot", name, v["n"])
        await b.close()
    srv.shutdown()


def crop(f, pad=16):
    """The shot cut to the hero (whatever differs from the corner's backdrop), squared on that backdrop."""
    im = Image.open(f).convert("RGB")
    a = np.asarray(im).astype(int)
    ys, xs = np.where(np.abs(a - a[2, 2]).max(-1) > 12)
    if not len(xs):
        return
    x0, x1, y0, y1 = max(xs.min() - pad, 0), min(xs.max() + pad, a.shape[1]), max(ys.min() - pad, 0), min(ys.max() + pad, a.shape[0])
    side = max(x1 - x0, y1 - y0)
    sq = Image.new("RGB", (side, side), tuple(a[2, 2]))
    sq.paste(im.crop((x0, y0, x1, y1)), ((side - (x1 - x0)) // 2, (side - (y1 - y0)) // 2))
    sq.resize((480, 480), Image.LANCZOS).save(f)


def preview(cls, made, out):
    sets = {}
    for v in made:
        sets.setdefault(v["set"], []).append(v)
    cards = []
    for name, vs in sets.items():
        row = [f'<figure><img src="shots/{name}_0_front.png"><img src="shots/{name}_0_back.png"><figcaption>{name} · ของเดิม</figcaption></figure>']
        for v in vs:
            texs = "".join(f'<img class="t" src="{f.relative_to(out).as_posix()}">' for f in v["files"].values())
            row.append(f'<figure><img src="shots/{name}_{v["n"]}_front.png"><img src="shots/{name}_{v["n"]}_back.png">'
                       f'<figcaption>{name} {v["n"]} · {v["title"]}</figcaption><div class="ts">{texs}</div></figure>')
        cards.append(f"<h2>{name}</h2><div class=row>{''.join(row)}</div>")
    (out / "preview.html").write_text(f"""<!doctype html><meta charset=utf-8><title>Rabbit reskins</title>
<style>body{{font-family:system-ui,sans-serif;background:#f4f1ea;color:#222;margin:16px}}h2{{margin:24px 0 8px}}
.row{{display:flex;gap:12px;flex-wrap:wrap}}figure{{margin:0;background:#fff;border-radius:10px;padding:8px;box-shadow:0 1px 4px #0002}}
figure>img{{width:220px;height:220px;object-fit:cover;background:#fff}}figcaption{{font-weight:600;margin:6px 2px}}
.ts{{display:flex;gap:4px}}.t{{width:52px;height:52px;object-fit:contain;background:#555;border-radius:4px}}</style>
<h1>{cls}: ลายใหม่ 3 แบบต่อเซ็ต</h1>{''.join(cards)}""", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cls"); ap.add_argument("--preview", action="store_true")
    a = ap.parse_args()
    out = ROOT / "plans" / "reskins" / a.cls
    made = build(a.cls, out)
    if a.preview:
        import asyncio
        asyncio.run(shots(a.cls, made, out))
        preview(a.cls, made, out)
        print("preview:", (out / "preview.html").as_uri())


if __name__ == "__main__":
    main()
