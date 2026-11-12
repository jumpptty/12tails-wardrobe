r"""The Cat as the reference's knight (2026-11-12; user: a reference picture, a red bodysuit under silver armour with gold
trim, a white tabard with a gold border, "find the best cat outfit that can best represent this reference image", "I
don't want a simple recolor, I need the outlines to have a high matching percentage against the reference image too").
Step 1, picking the base: --blockout paints the two candidates (legend; champion with its shield hidden by alpha) in
the reference's colours, roughly, by body part and colour class, and shoots them side by side for the user to pick.
  uv run --no-project --with pillow --with numpy --with scipy --with playwright python -I pipeline/wardrobe_knight.py --blockout
Outputs plans/reskins/cat/blockout_<outfit>/<outfit>.png, shots/, blockout.html."""
import asyncio, sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0, str(Path(__file__).resolve().parent))      # python -I leaves the script's folder off the path
from wardrobe_repaint import ROOT, DATA, texel_maps, hsv, hd, sstep, ramp, tone, shots

RED = ("#560c14", "#b01f2b", "#e2565c")
SILVER = ("#3f4553", "#949baf", "#f8fafd")       # steel: mid grey-blue, white only in the highlights (user: "too white")
WHITE = ("#b9b6c2", "#f3f2f6", "#ffffff")
BLACK = ("#101014", "#25242b", "#4b4954")
OUT = ROOT / "plans" / "reskins" / "cat"


def load(outfit, K=1):
    im = Image.open(DATA / "cat" / "tex" / f"{outfit}1.webp").convert("RGBA")
    if K > 1:
        im = im.resize((im.width * K, im.height * K), Image.LANCZOS)
    src = np.asarray(im).astype(float)
    M = texel_maps("cat", outfit, im.size)
    h, s, v = hsv(src[..., :3])
    L = ndimage.gaussian_filter(src[..., :3] @ [0.299, 0.587, 0.114] / 255, 1.0 * K)
    grp = lambda *pre: np.isin(M.bone, [i for i, b in enumerate(M.bones) if b.startswith(pre)])
    return src, M, h, s, v, L, grp


def flat(L, ref, k=0.45):                # an area's shading, calmed (fur stripes and filigree are not the new cloth's folds)
    return 0.5 + (tone(L, ref) - 0.5) * k


def blockout_legend():
    src, M, h, s, v, L, grp = load("legend")
    out = src[..., :3].copy()
    gold = (hd(h, 38) < 16) & (s > 0.55) & (v > 0.45)
    body = grp("Spine", "Hip", "Thigh", "Neck") & ~grp("Head")
    limb = grp("Arm", "Leg", "Foot", "Toe")
    sleeve = grp("UpperArm")
    X, Y, Z = M.pos[..., 0], np.abs(M.pos[..., 1]), M.pos[..., 2]
    paint = lambda m, cols, t: out.__setitem__(m, ramp(t, cols)[m])
    paint(body & ~gold, RED, flat(L, body & ~gold))
    paint(sleeve & ~gold, RED, flat(L, sleeve & ~gold))
    blue = (hd(h, 218) < 30) & (s > 0.3)
    paint(sleeve & blue, SILVER, tone(L, sleeve & blue))                      # the pauldron's plates
    paint(limb & ~gold & (v > 0.12), SILVER, tone(L, limb & ~gold & (v > 0.12)))
    tabard = (M.lab == M.lab[300, 250]) & (X > 0.02) & (Y < 0.075) & (Z < 0.9)    # the body's front, between the tassets
    paint(tabard & ~gold, WHITE, flat(L, tabard & ~gold, 0.3))
    return np.dstack([np.clip(out, 0, 255), src[..., 3]]).astype(np.uint8)


def blockout_champion():
    src, M, h, s, v, L, grp = load("champion")
    out, alpha = src[..., :3].copy(), src[..., 3].copy()
    isl = lambda x, y: M.lab == M.lab[y, x]
    gold = (hd(h, 42) < 16) & (s > 0.6) & (v > 0.7)
    furry = (hd(h, 30) < 22) & (s > 0.2) & ~gold
    paint = lambda m, cols, t: out.__setitem__(m, ramp(t, cols)[m])
    alpha[isl(180, 135) | isl(497, 30)] = 0                                    # the shield: not drawn (the page's alphaTest)
    torso = isl(290, 100) | isl(430, 100)
    paint(torso & ~gold, RED, flat(L, torso & ~gold))
    for seed in ((170, 360), (450, 340)):                                      # the arm's fur, the thighs
        a = isl(*seed)
        paint(a & ~gold, RED, flat(L, a & ~gold))
    for seed in ((430, 222), (320, 217), (200, 219), (118, 357)):              # the crossed straps, the chest crest
        a = isl(*seed)
        paint(a & ~gold, BLACK, flat(L, a & ~gold))
    hands = grp("Hand", "Index", "Middle", "Thumb")
    paint(hands & furry, BLACK, flat(L, hands & furry))
    return np.dstack([np.clip(out, 0, 255), alpha]).astype(np.uint8)


def main():
    variants = []
    for outfit, fn in (("legend", blockout_legend), ("champion", blockout_champion)):
        d = OUT / f"blockout_{outfit}"
        d.mkdir(parents=True, exist_ok=True)
        Image.fromarray(fn(), "RGBA").save(d / f"{outfit}.png")
        variants.append((outfit, {f"cat|outfits|{outfit}|": d / f"{outfit}.png"}))
    for outfit, files in variants:
        asyncio.run(shots("cat", outfit, [(f"orig_{outfit}", {}, {}), (f"blockout_{outfit}", files, {})], OUT,
                          yaws=((0, "front"), (90, "left"), (180, "back"), (270, "right")), size=640))
    rows = "".join(f'<figure>{"".join(f"<img src=shots/{k}_{o}_{s}.png>" for s in ("front", "left", "back", "right"))}'
                   f'<figcaption>{o} · {"ของเดิม" if k == "orig" else "ลงสีคร่าว ๆ ตามภาพอ้างอิง (ยังไม่ใช่งานจริง)"}</figcaption></figure>'
                   for o, _ in variants for k in ("orig", "blockout"))
    (OUT / "blockout.html").write_text(f"""<!doctype html><meta charset=utf-8><title>Cat: knight base</title>
<style>body{{font-family:system-ui,sans-serif;background:#f4f1ea;margin:16px}}figure{{margin:0 0 16px;background:#fff;border-radius:10px;padding:8px}}
img{{width:24%;min-width:200px}}figcaption{{font-weight:600;margin:4px}}</style><h1>แมว · เลือกชุดตั้งต้น</h1>{rows}""", encoding="utf-8")
    print("preview:", (OUT / "blockout.html").as_uri())


# ---------- step 2: the detailed paint on champion (the user's pick, 2026-11-12: "You may go ahead, note that you can
# also change the skin color to match, you may also edit the faces your self") ----------
# The suit, the sleeves, the gloves, the skin and the fur are painted from the mesh alone (bone, bind-pose position,
# surface normal, UV island): the reference's lines are drawn in body coordinates (x front, y left, z up; the Cat's
# hips z 0.87, neck base 1.24, elbow |y| 0.30). The plate and the hip cloth keep the original's painted forms (their
# gold trims follow the modelled edges) in the reference's metals. Hair and eyes are not the outfit texture's: the hair
# is her head piece's own texture (hair(), below), the eyes are the face preset's (38: purple, calm).
GOLD = ("#74460e", "#d9a22c", "#ffe690")
STEEL = ("#474c5a", "#9298a8", "#e3e6ed")       # the plate's trim where the reference has no gold
SKIN = ("#b97a5e", "#efc5a9", "#fcdfca")
BLOND = ("#b0843f", "#ecd087", "#fdf1c4")       # the reference's golden blonde: the hair piece, her ears and tail
SEEDS = dict(torsoF=(290, 100), torsoB=(430, 100), arms=(170, 360), thighs=(450, 340), skirt=(270, 300), skirt2=(67, 319),
             sash=(430, 222), sash2=(364, 100), sash3=(500, 127), belt=(326, 217), belt2=(355, 34), straps=(200, 219),
             crest=(118, 357), wing=(212, 42), pauldronR=(235, 415), gauntR=(374, 435), gauntR2=(100, 430), gauntR3=(312, 391),
             gauntR4=(220, 355), bracerL=(300, 438), bandL=(455, 263), greave=(460, 450), rim=(175, 197), boot=(335, 348),
             boot2=(20, 392), boot3=(44, 360), boot4=(154, 436), head=(72, 90), ears=(64, 192), inner=(160, 50),
             hand1=(95, 249), hand2=(36, 247), hand3=(20, 292), hand4=(64, 296), tail=(238, 482), tip=(46, 450),
             shield=(180, 135), shield2=(497, 30))
AA = 0.0014                                      # about a texel of the game's 512 px sheet, in body units
HI = 4                                           # the skin's scale: 2048 px


def inside(d, aa=AA):                            # a signed distance (negative inside) -> a soft mask
    return 1 - sstep(d, -aa, aa)


def knight(debug=False, K=HI):
    """K: the texture's scale over the game's 512 px (user 2026-11-12: "you are allowed to ignore game logic and apply
    high-res texture"): the drawn lines are sharp at any K; the original's paint under the plate is enlarged (soft)."""
    src, M, h, s, v, L, grp = load("champion", K)
    out, alpha = src[..., :3].copy(), np.full(src.shape[:2], 255.0)
    I = {k: (M.lab == M.lab[y * K + K // 2, x * K + K // 2]) for k, (x, y) in SEEDS.items()}
    ins = lambda d: inside(d, AA / K)
    if debug:
        for k, m in I.items():
            ys, xs = np.where(m & M.covered)
            print(f"{k:10s} px={len(xs):7d} x {xs.min() // K}-{xs.max() // K} y {ys.min() // K}-{ys.max() // K}")
    X, Ys, Z = M.pos[..., 0], M.pos[..., 1], M.pos[..., 2]
    Y = np.abs(Ys)
    nx, ny, nz = M.nrm[..., 0], M.nrm[..., 1], M.nrm[..., 2]

    def mix(m, col, k=1.0):
        k = np.broadcast_to(np.asarray(k, float), m.shape)[..., None]
        out[m] = (out * (1 - k) + col * k)[m]

    # painted light for the new cloth: from above, the sides and the islands' edges a little darker
    form = ndimage.gaussian_filter(0.5 + 0.30 * nz - 0.10 * np.abs(ny) - 0.16 * (1 - sstep(M.edge, 0, 6 * K)) * M.covered, 1.2 * K)
    gold_k = sstep(s, 0.45, 0.65) * (hd(h, 42) < 20) * sstep(v, 0.5, 0.7)
    # polished metal (user 2026-11-12: "make the armor looks more silver shiny, now it looks too white"): what a plate
    # reflects by where it faces: bright sky above, a dark horizon band, a dimmer ground glow below; mixed with the paint
    env = np.interp(ndimage.gaussian_filter(nz, 1.5 * K), [-1, -0.45, -0.05, 0.12, 0.6, 1], [0.36, 0.5, 0.14, 0.48, 0.8, 1.0])
    # (capped below white: only a narrow highlight on the faces turned straight up reaches it, or the plate reads white)
    glint = 0.14 * sstep(ndimage.gaussian_filter(nz, 1.5 * K), 0.90, 0.99)
    metal = lambda t: np.clip(0.40 * t + 0.50 * env, 0, 0.84) + glint
    hexv = lambda c: np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], float)
    hexc_white = hexv(WHITE[1])

    # ----- the plate: the original's forms, silver for its white, the reference's gold for its gold
    plate = np.zeros(Y.shape, bool)
    for k in ("wing", "pauldronR", "gauntR", "gauntR2", "gauntR3", "gauntR4", "bracerL", "bandL", "greave", "rim", "boot", "boot2", "boot3", "boot4"):
        plate |= I[k]
    cloth = I["skirt"] | I["skirt2"] | I["sash"] | I["sash2"] | I["sash3"] | I["belt"] | I["belt2"]
    mix(plate, ramp(metal(tone(L, plate & (gold_k < 0.3) & (s < 0.25))), SILVER))
    mix(cloth, ramp(tone(L, cloth & (gold_k < 0.3) & (s < 0.25)), WHITE))
    for area in (plate, cloth):
        mix(area, ramp(0.75 * tone(L, area & (gold_k > 0.7)) + 0.25 * env, GOLD), gold_k)
    alpha[I["shield"] | I["shield2"]] = 0

    # the hip cloth: its thin gold ornaments (the wing) gone, plain white inside the gold border, as the reference's tabard
    # (a gold piece is a border when some part of it is thick; a per-texel test bit ragged notches into the borders' tips)
    gmask = cloth & (gold_k > 0.4)
    gl, _ = ndimage.label(gmask)
    border = np.isin(gl, np.unique(gl[ndimage.binary_opening(gmask, iterations=2 * K)])) & gmask
    near = ndimage.binary_dilation(border, iterations=K)
    Ls = ndimage.gaussian_filter(L, 3 * K)                     # and its grey filigree: the cloth plain, softly shaded
    mix(cloth, ramp(tone(Ls, cloth & (gold_k < 0.3) & (s < 0.25)), WHITE), (1 - gold_k) + gold_k * ~near)
    # (no dark line inside the border: at 512 px it is a texel wide and steps; the user: "the black outline looks cheap")
    # the legs: no gold but the knee emblems (user: "the boots shouldn't have any gold"): their trims a darker steel
    legs = I["greave"] | I["rim"] | I["boot"] | I["boot2"] | I["boot3"] | I["boot4"]
    mix(legs, ramp(tone(L, legs & (gold_k > 0.7)), STEEL), np.maximum(gold_k, sstep(s, 0.25, 0.45) * (hd(h, 42) < 25)))   # faint gold too
    # the knees: the reference's gold emblem, a black hexagon inside it (the greave's front, z 0.37, |y| 0.09)
    G = I["greave"]
    dy, dz = Y - 0.09, Z - 0.368
    hexd = np.maximum(np.abs(dy) * 0.866 + np.abs(dz) * 0.5, np.abs(dz))
    front = sstep(nx, 0.15, 0.4)
    mix(G, hexv("#1b1a20"), ins(hexd - 0.0345) * front)
    mix(G, ramp(form + 0.1, GOLD), ins(hexd - 0.031) * front)
    mix(G, hexv("#1b1a20"), ins(np.abs(hexd - 0.0185) - 0.0022) * front)
    # ----- the suit: the torso
    red = ramp(form, RED)
    for k in ("torsoF", "torsoB", "thighs", "arms"):
        mix(I[k], red)
    F, B = I["torsoF"], I["torsoB"]
    seam = np.abs(Y - (0.028 + 0.062 * np.clip((Z - 0.88) / 0.31, 0, 1) ** 1.2)) - 0.0020      # the princess seams
    mix(F | B, hexv("#4d0a13"), ins(seam) * 0.8)
    mix(F, ramp(form, BLACK), ins(Y - 0.0085) * (Z < 1.2))                                   # the placket and its zip
    mix(F, hexv("#aab0bd"), ins(Y - 0.0015) * (Z < 1.2))
    for z0 in (1.075, 1.040, 1.005):                                                            # the frog fasteners
        bar = np.maximum(np.abs(Z - z0) - 0.0048, Y - 0.040)
        tip = (np.abs(Y - 0.042) / 0.011 + np.abs(Z - z0) / 0.0105 - 1) * 0.008
        mix(F, ramp(form, BLACK), ins(np.minimum(bar, tip)))
        mix(F, hexv("#cfd2dc"), ins(np.hypot(Y - 0.021, Z - z0) - 0.0034))
    # the collar (user: "add details at her collar"): pointed white lapels, a black edge and a second trim line inside
    # it, the dark knot and its stud between them (the chest crest sits just below)
    col_d = (Z - (1.195 + 0.62 * Y)) / 1.18
    mix(F, ramp(form + 0.1, WHITE), ins(-col_d))
    mix(F, hexv("#1b1a20"), ins(np.abs(col_d) - 0.0028))
    mix(F, hexv("#1b1a20"), ins(np.abs(col_d - 0.0085) - 0.0011))
    knot = np.maximum(Y - (0.006 + 0.10 * (Z - 1.185)), 1.185 - Z)
    mix(F, ramp(form, BLACK), ins(knot))
    mix(F, hexv("#d5d8e2"), ins(np.hypot(Y, Z - 1.215) - 0.0036))
    mix(B, hexv("#4d0a13"), ins(Y - 0.0016) * 0.8)                                           # the back: a centre seam
    # (a white cape yoke was tried here: beside the fair skin it read as a bare back)
    mix(B, ramp(form + 0.1, WHITE), ins(-col_d))                                             # the collar goes round
    mix(B, hexv("#1b1a20"), ins(np.abs(col_d) - 0.0030))

    # ----- the sleeves: red to the elbow (|y| 0.30), a vambrace from there
    A = I["arms"]
    # the arm's own frame (it hangs 40 degrees off the y axis; both arms share these texels, mirrored): S = along the
    # arm from the shoulder, th = round it (0 on the outer / upper side)
    Pm = np.stack([X, Y, Z], -1)
    pts = Pm[A & M.covered]
    ax = np.linalg.svd(pts - pts.mean(0), full_matrices=False)[2][0]
    ax *= np.sign(ax[1])
    S = (Pm - pts.mean(0)) @ ax
    S = S - S[A & M.covered].min()
    up = np.array([0, 0, 1.0]) - ax[2] * ax
    up /= np.linalg.norm(up)
    Nm = np.stack([nx, ny * np.sign(Ys + 1e-9), nz], -1)
    th = np.arctan2(ndimage.gaussian_filter(Nm @ np.cross(ax, up), K), ndimage.gaussian_filter(Nm @ up, K))
    R_ARM = 0.028
    s_at = lambda y: float(np.median(S[A & M.covered & (np.abs(Y - y) < 0.006)]))
    s_el = s_at(0.300)
    if debug:
        print("arm axis", ax.round(3), "length", round(float(S[A & M.covered].max()), 3), "elbow s", round(s_el, 3), "band s", round(s_at(0.19), 3), round(s_at(0.29), 3))
    # a black stripe down the outer sleeve, gold piping each side (user: "more details along her red arm cloths")
    stripe = (np.abs(th) - 0.42) * R_ARM
    mix(A, ramp(form, GOLD), ins(stripe - 0.0042) * ins(S - s_el))
    mix(A, ramp(form, BLACK), ins(stripe) * ins(S - s_el))
    mix(A, hexv("#4d0a13"), ins(np.abs(stripe - 0.0055) - 0.0008) * ins(S - s_el) * 0.7)
    # the vambrace from the elbow
    mix(A, ramp(metal(form), SILVER), ins(s_el - S))
    mix(A, ramp(form, GOLD), ins(np.abs(S - s_el) - 0.005))
    # the shoulders (user: "add a fake texture at her right shoulder too, some white furs both left and right"): a
    # painted pauldron over the arm's top (two lames, a gold rim, dark edges) and the reference's white fringe under
    # it; the modelled pauldron of the other arm sits over the same paint
    rim = 0.100 - 0.030 * (np.abs(th) / 1.9) ** 2
    wrap = (np.abs(th) - 1.9) * R_ARM
    strands = np.abs(np.sin(th * 12))
    d_f = np.maximum(S - (rim + 0.040 - 0.010 * (1 - strands) ** 2), (np.abs(th) - 1.7) * R_ARM)
    mix(A, ramp(form + 0.18, WHITE), ins(d_f))
    mix(A, hexv("#8f8b9c"), ins(d_f + 0.001) * (1 - sstep(strands, 0.10, 0.22)) * 0.75)       # between the strands
    mix(A, hexv("#3a0a10"), ins(np.abs(d_f) - 0.0009) * 0.6)
    d_p = np.maximum(S - rim, wrap)
    mix(A, ramp(metal(form + 0.05), SILVER), ins(d_p))
    mix(A, ramp(form + 0.05, GOLD), ins(np.abs(d_p + 0.0045) - 0.0045))
    for off, wdt in ((0.0, 0.0013), (0.0092, 0.0009)):
        mix(A, hexv("#1b1a20"), ins(np.abs(d_p + off) - wdt))
    lame = np.maximum(S - (rim - 0.045), wrap)                                                   # the upper lame's edge
    mix(A, hexv("#1b1a20"), ins(np.abs(lame) - 0.0011) * ins(d_p + 0.010))
    mix(A, ramp(np.full(Y.shape, 0.95), SILVER), ins(np.abs(lame - 0.003) - 0.0012) * ins(d_p + 0.010) * 0.8)

    # ----- the straps across the waist: black leather, the reference's fasteners; the chest crest: the dark studded jabot
    for k in ("straps", "crest"):
        mix(I[k], ramp(tone(L, I[k] & (gold_k < 0.3)) * 0.8, BLACK), 1 - gold_k)
        mix(I[k], ramp(tone(L, I[k] & (gold_k > 0.7)), GOLD), gold_k)

    C = I["crest"]                                                                              # the jabot's studs
    for z0 in (1.195, 1.170, 1.145):
        mix(C, hexv("#d5d8e2"), ins(np.hypot(Y - 0.011, Z - z0) - 0.0042))

    # ----- gloves: black, the fingers plated
    hands = I["hand1"] | I["hand2"] | I["hand3"] | I["hand4"]
    mix(hands, ramp(tone(L, hands), BLACK))
    fingers = np.isin(M.bone, [i for i, b in enumerate(M.bones) if b[:-3] in ("Index", "Middle") or b.startswith("Thumb2")])
    mix(hands & fingers, ramp(metal(tone(L, hands)), SILVER))

    # ----- skin and fur: the face and neck fair, the ears and tail the hair's blonde
    head = I["head"]
    mix(head, ramp(tone(L, head), SKIN))
    mix(I["inner"], ramp(np.full(Y.shape, 0.36), SKIN))        # the head's side under the hair (dark fur before)
    # the choker's band (z up to 1.287): the suit's white standing collar, one clean dark line along its top
    # (re-toning the choker's own paint left dotted bits of its outline under the chin)
    mix(head, ramp(form + 0.12, WHITE), ins(Z - 1.287))
    mix(head, hexv("#1b1a20"), ins(np.abs(Z - 1.2835) - 0.0035))                    # its black trim band
    mix(head, ramp(form, GOLD), ins(np.abs(Z - 1.2775) - 0.0011) * ins(Z - 1.287))  # a gold line under the trim
    front = sstep(X, 0.030, 0.040)
    mix(head, hexv("#1b1a20"), ins(Y - (0.0025 + 0.20 * (Z - 1.243))) * ins(Z - 1.287) * front)   # the opening
    mix(head, hexv("#d5d8e2"), ins(np.hypot(Y - 0.019, Z - 1.262) - 0.0036) * front)
    mix(head, hexv("#1b1a20"), ins(np.abs(np.hypot(Y - 0.019, Z - 1.262) - 0.0042) - 0.0007) * front)
    for k in ("ears", "tail", "tip"):
        mix(I[k], ramp(tone(L, I[k]), BLOND))
    return np.dstack([np.clip(out, 0, 255), alpha]).astype(np.uint8)


def hair(K=HI):
    """The Cat's hair is not on the outfit's sheet: it is her head piece (accessory "default", Cat_default.png, 128 px;
    the page puts it on whenever no hat is worn). Its own shading, in the reference's blonde (user 2026-11-12: "you are
    granted permission to try change the hair color too")."""
    im = Image.open(DATA / "props" / "tex" / "Cat_default.png").convert("RGBA")
    im = im.resize((im.width * K, im.height * K), Image.LANCZOS)
    a = np.asarray(im).astype(float)
    L = ndimage.gaussian_filter(a[..., :3] @ [0.299, 0.587, 0.114] / 255, 0.6 * K)
    return np.dstack([np.clip(ramp(tone(L, np.ones(L.shape, bool), lo=1), BLOND), 0, 255), a[..., 3]]).astype(np.uint8)


def paint_main(debug):
    """The skin, its checks, the hero from four sides, and original | new | reference side by side (--ref <picture>:
    the user's reference, copied beside the shots; it is theirs, so it stays out of git)."""
    d = OUT / "knight"
    d.mkdir(parents=True, exist_ok=True)
    skin = knight(debug)
    ow, oh = Image.open(DATA / "cat" / "tex" / "champion1.webp").size
    assert skin.shape[:2] == (oh * HI, ow * HI), "a skin is the original's size or 2x / 4x / 8x of it (the page's skinDims)"
    hidden = skin[..., 3] != 255
    assert hidden.mean() < 0.06 and (skin[..., 3][hidden] == 0).all(), "only the shield's texels lose their alpha"
    Image.fromarray(skin, "RGBA").save(d / "champion.png", optimize=True)
    print(f"{skin.shape[1]}x{skin.shape[0]} px, {(d / 'champion.png').stat().st_size / 1e6:.1f} MB")
    views = ((0, "front"), (90, "left"), (180, "back"), (270, "right"))
    asyncio.run(shots("cat", "champion", [("orig", {}, {})], OUT, yaws=views[:1], size=1000, dpr=2))
    Image.fromarray(hair(), "RGBA").save(d / "Cat_default.png")
    skins = {"cat|outfits|champion|": d / "champion.png", "cat|accessories|default|Cat_default.png": d / "Cat_default.png"}
    asyncio.run(shots("cat", "champion", [("knight", skins, {})], OUT, yaws=views, size=1000, dpr=2, face=38))
    panels = [Image.open(OUT / "shots" / "orig_front.png"), Image.open(OUT / "shots" / "knight_front.png")]
    if "--ref" in sys.argv:
        Image.open(sys.argv[sys.argv.index("--ref") + 1]).convert("RGB").save(OUT / "reference.png")
    if (OUT / "reference.png").exists():
        ref = Image.open(OUT / "reference.png")
        panels.append(ref.resize((round(ref.width * 1000 / ref.height), 1000), Image.LANCZOS))
    sheet = Image.new("RGB", (sum(p.width for p in panels), 1000), (230, 225, 216))
    x = 0
    for p in panels:
        sheet.paste(p, (x, 0)); x += p.width
    sheet.save(OUT / "knight_compare.png")
    imgs = "".join(f"<img src=shots/knight_{s}.png>" for _, s in views)
    (OUT / "knight.html").write_text(f"""<!doctype html><meta charset=utf-8><title>Cat: knight</title>
<style>body{{font-family:system-ui,sans-serif;background:#f4f1ea;margin:16px}}figure{{margin:0 0 16px;background:#fff;border-radius:10px;padding:8px}}
figure img{{width:24%;min-width:200px}}.cmp img{{width:100%;min-width:0}}figcaption{{font-weight:600;margin:4px}}</style>
<h1>แมว · ชุด Champion เป็นอัศวินตามภาพอ้างอิง</h1>
<figure class=cmp><img src=knight_compare.png><figcaption>ของเดิม · ของใหม่บนโมเดล 3D (หน้าแบบที่ 38) · ภาพอ้างอิง</figcaption></figure>
<figure>{imgs}<figcaption>ของใหม่ · หน้า ซ้าย หลัง ขวา</figcaption></figure>
<figure><img src=knight/champion.png style="width:48%"><img src=knight/Cat_default.png style="width:24%"><figcaption>ลายชุด ({skin.shape[1]} × {skin.shape[0]}) · ลายผม (ชิ้นหัว default)</figcaption></figure>""", encoding="utf-8")
    print("painted", d / "champion.png")
    print("preview:", (OUT / "knight.html").as_uri())


if __name__ == "__main__":
    paint_main("--debug" in sys.argv) if "--paint" in sys.argv else main()
