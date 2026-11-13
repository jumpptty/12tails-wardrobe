r"""The Cat after a reference picture (2026-11-13; user: "try doing this character, you pick the best fit female class
yourself"; bases limited to royal / legend / summer / hallow / the bug set; the reskin-from-image skill: only what the
picture shows). The picture: a slim young woman, short dark violet hair (side-swept fringe, a small bun behind), green
eyes, fair skin, a black choker, a white sleeveless shirt with a collar and a thin black ribbon tied at it, charcoal
high-waisted shorts with one button, black thigh-high socks, dark brown loafers.
The base (wardrobe_outfit_sheet.py: the five allowed sets on Cat, Sheep, Rabbit, Bat): the Cat's **summer**: a sleeveless
top, shorts, bare arms and legs, slip-on shoes, a neck scarf: every part of the picture has a shape to sit on.
  uv run --no-project --with pillow --with numpy --with scipy --with playwright python -I pipeline/wardrobe_cat_shorts.py [--debug] [--noshots]
Outputs plans/reskins/cat/shorts/: look/summer.png (2048 px), look/Cat_default.png (the hair: her head piece), shots/,
compare.png, look.html."""
import asyncio, sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0, str(Path(__file__).resolve().parent))      # python -I leaves the script's folder off the path
from wardrobe_repaint import ROOT, DATA, cached_maps, sstep, ramp, tone, shots, paint_under
from wardrobe_bat_robe import vnoise, folds

CLS, OUTFIT = "cat", "summer"
OUT = ROOT / "plans" / "reskins" / "cat" / "shorts"
HI = 4                                           # 2048 px
FACE = 5                                         # BB's face 5: closed eyes, each one arched stroke, soft brows, a small smile.
# The stroke is used as the upper lid of an eye painted under it on the skin (user 2026-11-13: "you may be able to work
# on top of these faces ... it is easy to work on top of a single eye stroke"): half-lidded green eyes, as the reference's
EYES = ((24, 55), (87, 118))                     # the two strokes on the 512 px sheet: x from, to; their ends at y 59, the top at 49
EYE = ("#1d5a34", "#4cb062", "#9be896")          # the iris: the bright green of the user's close-up, dark under the lid
AA = 0.0005                                      # about a texel at 2048 px, in body units (the Cat is 1.65 tall)

# Colours: k-means of the reference's pixels, each a shadow / base / light ramp
SKIN = ("#e6b29f", "#ffdccc", "#fff6ef")       # (a first, pinker shadow turned the arms mauve under the page's light)
HAIR = ("#221a30", "#413c5f", "#77709f")
SHIRT = ("#a698a6", "#f1e9ee", "#ffffff")
SHORTS = ("#131216", "#323037", "#5a5762")
SOCK = ("#0e0f13", "#24272f", "#4a4e5c")
SHOE = ("#130e0e", "#372f2e", "#6a5650")
INK = "#141318"

# Sheet seeds (x, y on the game's 512 px sheet); body coordinates x front, y left, z up: neck 1.22-1.27, the top
# 1.03-1.20, the waist 0.88-1.03, the shorts 0.66-0.88, legs 0.05-0.66, the shoes under 0.09
SEEDS = dict(head=(73, 81), scarfKnot=(349, 15), knot=(457, 15), inner=(160, 48), back=(435, 121), front=(288, 122),
             ears=(61, 193), shorts=(210, 250), scarf=(450, 244), strapA=(291, 315), hand1=(94, 246), hand2=(31, 250),
             strapB=(316, 312), strapC=(337, 352), hand3=(22, 290), arm=(170, 372), leg=(453, 377), strapD=(237, 367),
             band=(57, 347), shoe=(373, 410), tip=(49, 456), tail=(229, 487), soleA=(429, 467), soleB=(381, 487))
WAIST = 0.972                                    # the shorts' high waist: its top, painted on the body above the shorts
SOCK_Z = 0.560                                   # the thigh-highs' top
hexv = lambda c: np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], float)


def paint(debug=False, K=HI):
    im = Image.open(DATA / CLS / "tex" / f"{OUTFIT}1.webp").convert("RGBA")
    im = im.resize((im.width * K, im.height * K), Image.LANCZOS)
    src = np.asarray(im).astype(float)
    M = cached_maps(CLS, OUTFIT, K, OUT / "_cache")
    L = ndimage.gaussian_filter(src[..., :3] @ [0.299, 0.587, 0.114] / 255, 1.0 * K)
    out = src[..., :3].copy()
    I = {k: (M.lab == M.lab[y * K + K // 2, x * K + K // 2]) for k, (x, y) in SEEDS.items()}
    ins = lambda d, aa=AA: 1 - sstep(d, -aa, aa)                 # 1 where d < 0, a soft edge
    X, Ys, Z = M.pos[..., 0], M.pos[..., 1], M.pos[..., 2]
    Y = np.abs(Ys)
    nx, ny, nz = M.nrm[..., 0], M.nrm[..., 1], M.nrm[..., 2]
    full = lambda x: np.full(Y.shape, float(x))
    rampc = lambda t, cols: ramp(np.clip(t, 0, 1), cols)
    if debug:
        for k, m in I.items():
            p = M.pos[m & M.covered]
            print(f"{k:9s} px={len(p):7d} X {p[:, 0].min():.3f}..{p[:, 0].max():.3f} Y {p[:, 1].min():.3f}..{p[:, 1].max():.3f} Z {p[:, 2].min():.3f}..{p[:, 2].max():.3f}")

    def mix(m, col, k=1.0):
        k = np.broadcast_to(np.asarray(k, float), m.shape)[..., None]
        out[m] = (out * (1 - k) + col * k)[m]

    # painted light: from above and the front, the islands' edges a shade darker
    form = ndimage.gaussian_filter(0.5 + 0.22 * nz + 0.08 * nx - 0.08 * np.abs(ny) - 0.10 * (1 - sstep(M.edge, 0, 6 * K)) * M.covered, 1.2 * K)
    theta = np.arctan2(Ys, X - 0.04)                             # round the body
    arc = theta * 0.10

    # ---------- the parts the reference does not have (the wristband, the top's tied knot, the braces) are painted as
    # what lies under them, at the end (paint_under): an outfit cannot hide anything in the game (RGB24 + Diffuse; user
    # 2026-11-13: "paint it, never make them transparent"). Hiding them by alpha had also opened the body's real holes
    # under the braces (the shoulder, the shorts' back: "it is hollow here") ----------
    straps = I["strapA"] | I["strapB"] | I["strapC"] | I["strapD"]

    # ---------- skin: face, neck, arms, hands, the thighs ----------
    head = I["head"]
    mix(head, rampc(0.56 + 0.70 * (tone(ndimage.gaussian_filter(L, 2 * K), head) - 0.5) + 0.25 * (form - 0.5), SKIN))
    mix(I["inner"], rampc(full(0.30), SKIN))
    A = I["arm"]
    mix(A, rampc(0.60 + 0.9 * (form - 0.5), SKIN))
    for k in ("hand1", "hand2", "hand3"):
        mix(I[k], rampc(0.28 + 0.70 * tone(L, I[k]), SKIN))
    # the eyes, under the face preset's two arched strokes (drawn on the sheet: the face is nearly flat there). After
    # the user's close-up of the reference's eyes ("yours is too generic"): long and narrow, a heavy dark upper lid that
    # runs out past the outer corner, a large bright green iris cut by both lids (dark under the lid, light at the foot,
    # a dark rim and a fine ring inside it), a small flat pupil, no light dots, a thin lower lid with a few short lashes
    # at its outer end, and fine hatching on the cheek under each eye
    yy, xx = np.mgrid[:Y.shape[0], :Y.shape[1]] / K
    LASH = hexv("#17131d")
    for (x0, x1), outer in zip(EYES, (-1, 1)):                    # outer: which way the eye's outer corner lies on the sheet
        cx, hw = (x0 + x1) / 2, (x1 - x0) / 2
        t = np.clip((xx - x0) / (x1 - x0), 0, 1)
        bow = 4 * t * (1 - t)
        upper, lower = 59.2 - 5.2 * bow ** 0.75, 59.4 + 2.9 * bow          # the lid's under edge (flatter than the stroke), the lower lid
        inx = ins(np.abs(xx - cx) - hw + 0.6, 0.3)
        eye = ins(upper - yy, 0.25) * ins(yy - lower, 0.25) * inx
        mix(head, LASH, ins(yy - upper, 0.25) * ins((59.0 - 7.2 * bow ** 0.8) - yy, 0.25) * inx)       # the lid's weight, under the stroke
        o = (xx - (cx + outer * hw)) * outer                          # past the outer corner: the lid's line runs on, down a little
        mix(head, LASH, ins(np.abs(yy - (59.3 + 0.35 * o)) - (1.0 - 0.22 * o), 0.25) * (o > -1.5) * (o < 4.2))
        white = ramp(np.clip(0.15 + (yy - upper) / 6.0, 0, 1), ("#8a8090", "#e4dde2", "#fbf8f9"))       # the lid's shade on the eye
        mix(head, white, eye)
        ix = cx - outer * 0.6                                         # the gaze a touch inward
        r = np.hypot((xx - ix) / 1.08, yy - 58.3)
        iris = ins(r - 6.2, 0.3) * eye
        mix(head, ramp(np.clip(0.10 + 0.95 * (yy - 54.0) / 7.5, 0, 1), EYE), iris)
        mix(head, hexv("#123a22"), ins(np.abs(r - 6.2) - 0.50, 0.25) * eye)                             # its rim
        mix(head, hexv("#1f6a3a"), ins(np.abs(r - 3.7) - 0.22, 0.2) * iris * 0.8)                        # the ring inside
        mix(head, hexv("#0c1a12"), ins(np.hypot((xx - ix) / 2.1, (yy - 58.3) / 1.15) - 1, 0.2) * eye)    # the pupil: small, flat
        mix(head, hexv("#7a5258"), ins(np.abs(yy - lower) - 0.32, 0.25) * inx * 0.9)                     # the lower lid
        for k_, dx in enumerate((0.55, 0.70, 0.84)):                                                    # lower lashes, outer end
            lx = cx + outer * hw * dx
            ly = 59.4 + 2.9 * 4 * (0.5 + outer * dx / 2) * (0.5 - outer * dx / 2)
            mix(head, hexv("#5c3f47"), ins(np.maximum(np.abs(xx - lx - outer * 0.35 * (yy - ly)) - 0.22, np.abs(yy - ly - 0.9) - 0.9), 0.2) * 0.85)
        hatch = ins(np.abs(((xx - cx) / 1.9 + 0.5) % 1 - 0.5) * 1.9 - 0.16, 0.2) * ins(np.abs(xx - cx - outer * 1.0) - 6.5, 0.6)             * ins(np.abs(yy - (66.6 + 0.10 * np.abs(xx - cx))) - 1.7, 0.5)
        mix(head, hexv("#d58f8c"), hatch * 0.55)                                                         # the cheek's hatching
    # the choker: a black band high on the neck
    mix(head, hexv(INK), ins(np.abs(Z - 1.268) - 0.011) * (Z < 1.30))
    mix(head, hexv("#4b4955"), ins(np.abs(Z - 1.2755) - 0.0012) * 0.6)

    # ---------- the shirt: white, sleeveless; the shorts' high waist painted over its foot ----------
    F, B = I["front"], I["back"]
    T = F | B
    drape = 0.5 * folds(arc, Z, 0.030, 11, long=7) + 0.5 * folds(arc + 0.4 * Z, Z, 0.016, 12, long=5)
    bunch = folds(Z, arc, 0.016, 13, long=2.5) * np.exp(-((Z - WAIST - 0.03) / 0.03) ** 2)        # the cloth gathered over the waistband
    cloth = 0.56 + 0.95 * (form - 0.5) + 0.10 * drape * sstep(1.17 - Z, 0.0, 0.12) + 0.16 * bunch
    mix(T | straps, rampc(cloth, SHIRT))
    mix(T, rampc(full(0.2), SHIRT), ins(Z - WAIST - 0.012, 0.010) * 0.45)                           # the blouse's shade on the waist
    # (nothing on the torso's islands is hidden: a first try cut "the cap sleeves" by their pink and cut the top's pink
    # emblem instead, a hole in the chest: user 2026-11-13 "it is hollow here". The top's little shoulder caps stay, in
    # the shirt's white: its shoulders)
    # the hidden placket: two fine lines down the front; the armhole's stitched edge
    mix(F, hexv("#b7aab5"), ins(np.abs(Y - 0.0125) - 0.0007) * sstep(nx, 0.2, 0.5) * 0.9)
    mix(T, hexv("#b7aab5"), ins(np.abs(M.edge - 3.2 * K) - 0.5 * K, 0.5) * M.covered * sstep(Z, 1.10, 1.14) * sstep(Y, 0.05, 0.07) * 0.8)
    mix(B, hexv("#b7aab5"), ins(np.abs(Z - (1.165 - 1.5 * Y ** 2)) - 0.0008) * 0.8)                # the back's yoke
    # the ribbon's two ends hanging from the collar, down the placket
    for sgn, ln in ((1, 0.115), (-1, 0.095)):
        d = np.abs(Ys * sgn - (0.004 + 0.10 * (1.20 - Z))) - 0.0030
        mix(F, hexv(INK), ins(np.maximum(d, np.maximum(Z - 1.21, (1.20 - ln) - Z))) * sstep(nx, 0.2, 0.5))
    # the waist: charcoal up to WAIST, a band with one button, the fly's line under it
    waist = ins(Z - WAIST)
    mix(T | straps, rampc(0.50 + 0.9 * (form - 0.5) + 0.06 * drape, SHORTS), waist)
    mix(T, rampc(full(0.95), SHORTS), ins(np.abs(Z - (WAIST - 0.003)) - 0.0012) * 0.55)
    mix(T, hexv("#0c0b0e"), ins(np.abs(Z - (WAIST - 0.034)) - 0.0010) * 0.9)                        # the band's lower seam
    btn = np.hypot(Ys, Z - (WAIST - 0.018))
    mix(F, hexv("#0c0b0e"), ins(btn - 0.0085))
    mix(F, rampc(full(0.85), SHORTS), ins(btn - 0.0068))
    mix(F, hexv("#0c0b0e"), ins(np.hypot(Y - 0.002, Z - (WAIST - 0.018)) - 0.0011))
    mix(F, hexv("#0c0b0e"), ins(np.abs(Ys - 0.014) - 0.0009) * ins(Z - (WAIST - 0.036)) * sstep(nx, 0.2, 0.5) * 0.9)   # the fly
    for sgn in (1, -1):                                          # a belt loop each side of the front
        mix(F, rampc(full(0.72), SHORTS), ins(np.abs(Ys * sgn - 0.055) - 0.0035) * ins(np.abs(Z - (WAIST - 0.017)) - 0.019))
    # the collar: the scarf in the shirt's white, the ribbon's bow at its front
    for k in ("scarf", "scarfKnot"):
        S = I[k]
        mix(S, rampc(0.58 + 0.8 * (form - 0.5) + 0.25 * (tone(ndimage.gaussian_filter(L, 4 * K), S) - 0.5), SHIRT))
        mix(S, hexv("#b7aab5"), ins(np.abs(M.edge - 2.6 * K) - 0.45 * K, 0.5) * M.covered * 0.7)
    S = I["scarf"]
    fr = sstep(nx, 0.15, 0.45)
    bz = Z - 1.212
    loop = np.minimum(*(np.hypot((Ys * s_ - 0.019) / 0.017, (bz - 0.35 * (Ys * s_ - 0.019)) / 0.0085) - 1 for s_ in (1, -1))) * 0.0085
    mix(S, hexv(INK), ins(np.abs(loop) - 0.0028) * fr)                                               # two loops, drawn as outlines
    mix(S, hexv(INK), ins(np.hypot(Ys, bz) - 0.0058) * fr)                                           # the knot
    for sgn, ln in ((1, 0.115), (-1, 0.095)):
        d = np.abs(Ys * sgn - (0.004 + 0.10 * (1.20 - Z))) - 0.0030
        mix(S, hexv(INK), ins(np.maximum(d, np.maximum(Z - 1.21, (1.20 - ln) - Z))) * fr)

    # ---------- the shorts: charcoal, their own seams kept as shading ----------
    Sh = I["shorts"]
    mix(Sh, rampc(0.50 + 0.50 * (tone(ndimage.gaussian_filter(ndimage.median_filter(L, 7 * K), 2 * K), Sh) - 0.5) + 0.5 * (form - 0.5), SHORTS))   # (the median: no rivets)

    # ---------- legs: skin above, black thigh-highs from SOCK_Z down; the foot in its sock ----------
    G = I["leg"]
    mix(G, rampc(0.60 + 0.9 * (form - 0.5) - 0.12 * sstep(Z, 0.62, 0.66), SKIN))
    sock = ins(Z - SOCK_Z)
    knee = np.exp(-((Z - 0.37) / 0.05) ** 2) * sstep(nx, 0.0, 0.7)
    mix(G, rampc(0.42 + 1.1 * (form - 0.5) + 0.16 * knee + 0.03 * np.sin(theta * 60), SOCK), sock)
    mix(G, rampc(full(0.80), SOCK), ins(np.abs(Z - (SOCK_Z - 0.006)) - 0.0050) * 0.55)               # the top's band
    mix(G, hexv("#c58f90"), ins(np.abs(Z - (SOCK_Z + 0.004)) - 0.0035, 0.003) * 0.5)                # its press on the thigh
    # ---------- loafers: dark brown, a strap over the instep, the toe's seam ----------
    P = I["shoe"]
    mix(P, rampc(0.42 + 0.35 * (tone(ndimage.gaussian_filter(ndimage.median_filter(L, 9 * K), 3 * K), P) - 0.5) + 0.9 * (form - 0.5)
                 + 0.30 * sstep(ndimage.gaussian_filter(nz, 3 * K), 0.55, 0.95), SHOE))
    top = sstep(nz, 0.25, 0.6)
    mix(P, hexv("#0f0b0b"), ins(np.abs(np.hypot((X - 0.035) / 0.060, (Y - 0.11) / 0.040) - 1) * 0.04 - 0.0014) * top * sstep(X, 0.03, 0.05) * 0.9)   # the apron's seam
    mix(P, rampc(full(0.62), SHOE), ins(np.abs(X - 0.022) - 0.011) * top)                              # the strap
    mix(P, hexv("#0f0b0b"), ins(np.abs(np.abs(X - 0.022) - 0.011) - 0.0010) * top * 0.9)
    mix(P, hexv("#0f0b0b"), ins(np.maximum(np.abs(X - 0.022) - 0.003, np.abs(Y - 0.11) - 0.012)) * top)   # its slot
    mix(P, hexv("#0f0b0b"), ins(Z - 0.018, 0.004))                                                    # the sole
    for k in ("soleA", "soleB"):
        mix(I[k], hexv("#0f0b0b"))

    # ---------- the Cat's own: ears and tail in the hair's violet ----------
    for k in ("ears", "tail", "tip"):
        mix(I[k], rampc(0.15 + 0.75 * tone(L, I[k]), HAIR))

    # ---------- last: the unwanted parts take the colour of what is under them ----------
    paint_under(out, M, I["band"], I["arm"])
    paint_under(out, M, I["knot"] | straps, I["front"] | I["back"])
    return np.dstack([np.clip(out, 0, 255), np.full(out.shape[:2], 255.0)]).astype(np.uint8)


def hair(K=4):
    """The Cat's hair is her head piece (accessory "default", Cat_default.png, 128 px): its own shading in the
    reference's dark violet."""
    im = Image.open(DATA / "props" / "tex" / "Cat_default.png").convert("RGBA")
    im = im.resize((im.width * K, im.height * K), Image.LANCZOS)
    a = np.asarray(im).astype(float)
    L = ndimage.gaussian_filter(a[..., :3] @ [0.299, 0.587, 0.114] / 255, 0.6 * K)
    return np.dstack([np.clip(ramp(np.clip(0.08 + 0.85 * tone(L, np.ones(L.shape, bool), lo=1), 0, 1), HAIR), 0, 255), a[..., 3]]).astype(np.uint8)


def main(debug, noshots):
    d = OUT / "look"
    d.mkdir(parents=True, exist_ok=True)
    skin = paint(debug)
    orig = Image.open(DATA / CLS / "tex" / f"{OUTFIT}1.webp")
    assert skin.shape[:2] == (orig.height * HI, orig.width * HI), "a skin is the original's size or 2x / 4x / 8x of it (the page's skinDims)"
    assert (skin[..., 3] == 255).all(), "an outfit skin is opaque: the game ignores alpha (paint a part, never hide it)"
    Image.fromarray(skin, "RGBA").save(d / f"{OUTFIT}.png", optimize=True)
    Image.fromarray(hair(), "RGBA").save(d / "Cat_default.png")
    print(f"{skin.shape[1]}x{skin.shape[0]} px, {(d / f'{OUTFIT}.png').stat().st_size / 1e6:.1f} MB")
    if noshots:
        return
    views = ((0, "front"), (90, "left"), (180, "back"), (270, "right"), (25, "q"))
    skins = {f"{CLS}|outfits|{OUTFIT}|": d / f"{OUTFIT}.png", f"{CLS}|accessories|default|Cat_default.png": d / "Cat_default.png"}
    asyncio.run(shots(CLS, OUTFIT, [("look", skins, {})], OUT, yaws=views, size=1000, dpr=2, face=FACE))
    panels = [Image.open(OUT / "shots" / f"{n}_front.png") for n in ("orig", "look")]
    ref = Image.open(OUT / "reference.png").convert("RGBA")                 # the user's picture: theirs, not in git
    bg = Image.new("RGBA", ref.size, (230, 225, 216, 255)); bg.alpha_composite(ref)
    panels.append(bg.convert("RGB").resize((round(ref.width * 1000 / ref.height), 1000), Image.LANCZOS))
    sheet = Image.new("RGB", (sum(p.width for p in panels), 1000), (230, 225, 216))
    x = 0
    for p in panels:
        sheet.paste(p, (x, 0)); x += p.width
    sheet.save(OUT / "compare.png")
    imgs = "".join(f"<img src=shots/look_{s}.png>" for _, s in views[:4])
    (OUT / "look.html").write_text(f"""<!doctype html><meta charset=utf-8><title>Cat: shirt and shorts</title>
<style>body{{font-family:system-ui,sans-serif;background:#f4f1ea;margin:16px}}figure{{margin:0 0 16px;background:#fff;border-radius:10px;padding:8px}}
figure img{{width:24%;min-width:200px}}.cmp img{{width:100%;min-width:0}}figcaption{{font-weight:600;margin:4px}}</style>
<h1>แมว · ชุด Summer ตามภาพอ้างอิง</h1>
<figure class=cmp><img src=compare.png><figcaption>ของเดิม · ของใหม่บนโมเดล 3D (หน้าแบบที่ {FACE}) · ภาพอ้างอิง</figcaption></figure>
<figure>{imgs}<figcaption>ของใหม่ · หน้า ซ้าย หลัง ขวา</figcaption></figure>
<figure><img src=look/{OUTFIT}.png style="width:48%"><img src=look/Cat_default.png style="width:24%"><figcaption>ลายชุด ({skin.shape[1]} × {skin.shape[0]}) · ลายผม (ชิ้นหัว default)</figcaption></figure>""", encoding="utf-8")
    print("preview:", (OUT / "look.html").as_uri())


if __name__ == "__main__":
    main("--debug" in sys.argv, "--noshots" in sys.argv)
