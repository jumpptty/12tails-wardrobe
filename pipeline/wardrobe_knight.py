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
SILVER = ("#6c717e", "#c6c9d4", "#ffffff")
WHITE = ("#b9b6c2", "#f3f2f6", "#ffffff")
BLACK = ("#101014", "#25242b", "#4b4954")
OUT = ROOT / "plans" / "reskins" / "cat"


def load(outfit):
    im = Image.open(DATA / "cat" / "tex" / f"{outfit}1.webp").convert("RGBA")
    src = np.asarray(im).astype(float)
    M = texel_maps("cat", outfit, im.size)
    h, s, v = hsv(src[..., :3])
    L = ndimage.gaussian_filter(src[..., :3] @ [0.299, 0.587, 0.114] / 255, 1.0)
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
# is the Cat's own pale blonde, the eyes are the face preset's (38: purple, calm).
GOLD = ("#74460e", "#d9a22c", "#ffe690")
SKIN = ("#b97a5e", "#efc5a9", "#fcdfca")
BLOND = ("#8d8260", "#d8cfa9", "#f7f2da")       # the Cat's own hair, for her ears and tail
SEEDS = dict(torsoF=(290, 100), torsoB=(430, 100), arms=(170, 360), thighs=(450, 340), skirt=(270, 300), skirt2=(67, 319),
             sash=(430, 222), sash2=(364, 100), sash3=(500, 127), belt=(326, 217), belt2=(355, 34), straps=(200, 219),
             crest=(118, 357), wing=(212, 42), pauldronR=(235, 415), gauntR=(374, 435), gauntR2=(100, 430), gauntR3=(312, 391),
             gauntR4=(220, 355), bracerL=(300, 438), bandL=(455, 263), greave=(460, 450), rim=(175, 197), boot=(335, 348),
             boot2=(20, 392), boot3=(44, 360), boot4=(154, 436), head=(72, 90), ears=(64, 192), inner=(160, 50),
             hand1=(95, 249), hand2=(36, 247), hand3=(20, 292), hand4=(64, 296), tail=(238, 482), tip=(46, 450),
             shield=(180, 135), shield2=(497, 30))
AA = 0.0014                                      # about a texel, in body units


def inside(d, aa=AA):                            # a signed distance (negative inside) -> a soft mask
    return 1 - sstep(d, -aa, aa)


def knight(debug=False):
    src, M, h, s, v, L, grp = load("champion")
    out, alpha = src[..., :3].copy(), src[..., 3].copy()
    I = {k: (M.lab == M.lab[y, x]) for k, (x, y) in SEEDS.items()}
    if debug:
        for k, m in I.items():
            ys, xs = np.where(m & M.covered)
            print(f"{k:10s} covered={bool(M.covered[SEEDS[k][1], SEEDS[k][0]])} px={len(xs):6d} x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()}")
    X, Ys, Z = M.pos[..., 0], M.pos[..., 1], M.pos[..., 2]
    Y = np.abs(Ys)
    nx, ny, nz = M.nrm[..., 0], M.nrm[..., 1], M.nrm[..., 2]

    def mix(m, col, k=1.0):
        k = np.broadcast_to(np.asarray(k, float), m.shape)[..., None]
        out[m] = (out * (1 - k) + col * k)[m]

    # painted light for the new cloth: from above, the sides and the islands' edges a little darker
    form = ndimage.gaussian_filter(0.5 + 0.30 * nz - 0.10 * np.abs(ny) - 0.16 * (1 - sstep(M.edge, 0, 6)) * M.covered, 1.2)
    gold_k = sstep(s, 0.45, 0.65) * (hd(h, 42) < 20) * sstep(v, 0.5, 0.7)
    hexv = lambda c: np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], float)
    hexc_white = hexv(WHITE[1])

    # ----- the plate: the original's forms, silver for its white, the reference's gold for its gold
    plate = np.zeros(Y.shape, bool)
    for k in ("wing", "pauldronR", "gauntR", "gauntR2", "gauntR3", "gauntR4", "bracerL", "bandL", "greave", "rim", "boot", "boot2", "boot3", "boot4"):
        plate |= I[k]
    cloth = I["skirt"] | I["skirt2"] | I["sash"] | I["sash2"] | I["sash3"] | I["belt"] | I["belt2"]
    for area, cols in ((plate, SILVER), (cloth, WHITE)):
        mix(area, ramp(tone(L, area & (gold_k < 0.3) & (s < 0.25)), cols))
        mix(area, ramp(tone(L, area & (gold_k > 0.7)), GOLD), gold_k)
    alpha[I["shield"] | I["shield2"]] = 0

    # the hip cloth: its thin gold ornaments (the wing) gone, a black line inside the gold border, as the reference's tabard
    thick = ndimage.binary_opening(cloth & (gold_k > 0.5), iterations=2)
    near = ndimage.binary_dilation(thick, iterations=2)
    Ls = ndimage.gaussian_filter(L, 3)                         # and its grey filigree: the cloth plain, softly shaded
    mix(cloth, ramp(tone(Ls, cloth & (gold_k < 0.3) & (s < 0.25)), WHITE), (1 - gold_k) + gold_k * ~near)
    g = ndimage.gaussian_filter(thick.astype(float), 1.6)      # a smooth contour beside the border (a dilated ring was jagged)
    mix(cloth & M.covered, hexv("#211e27"), (1 - sstep(np.abs(g - 0.16), 0.03, 0.09)) * 0.6 * (gold_k < 0.3))
    # the knees: the reference's gold emblem, a black hexagon inside it (the greave's front, z 0.37, |y| 0.09)
    G = I["greave"]
    dy, dz = Y - 0.09, Z - 0.368
    hexd = np.maximum(np.abs(dy) * 0.866 + np.abs(dz) * 0.5, np.abs(dz))
    front = sstep(nx, 0.15, 0.4)
    mix(G, hexv("#1b1a20"), inside(hexd - 0.0345) * front)
    mix(G, ramp(form + 0.1, GOLD), inside(hexd - 0.031) * front)
    mix(G, hexv("#1b1a20"), inside(np.abs(hexd - 0.0185) - 0.0022) * front)
    # ----- the suit: the torso
    red = ramp(form, RED)
    for k in ("torsoF", "torsoB", "thighs", "arms"):
        mix(I[k], red)
    F, B = I["torsoF"], I["torsoB"]
    seam = np.abs(Y - (0.028 + 0.062 * np.clip((Z - 0.88) / 0.31, 0, 1) ** 1.2)) - 0.0020      # the princess seams
    mix(F | B, hexv("#4d0a13"), inside(seam) * 0.8)
    mix(F, ramp(form, BLACK), inside(Y - 0.0085) * (Z < 1.2))                                   # the placket and its zip
    mix(F, hexv("#aab0bd"), inside(Y - 0.0015) * (Z < 1.2))
    for z0 in (1.075, 1.040, 1.005):                                                            # the frog fasteners
        bar = np.maximum(np.abs(Z - z0) - 0.0048, Y - 0.040)
        tip = (np.abs(Y - 0.042) / 0.011 + np.abs(Z - z0) / 0.0105 - 1) * 0.008
        mix(F, ramp(form, BLACK), inside(np.minimum(bar, tip)))
        mix(F, hexv("#cfd2dc"), inside(np.hypot(Y - 0.021, Z - z0) - 0.0034))
    col_d = (Z - (1.207 + 0.75 * Y)) / 1.25                                                     # the collar: close to the neck
    mix(F, ramp(form + 0.1, WHITE), inside(-col_d))
    mix(F, hexv("#1b1a20"), inside(np.abs(col_d) - 0.0030))
    mix(B, hexv("#4d0a13"), inside(Y - 0.0016) * 0.8)                                           # the back: a centre seam
    # (a white cape yoke was tried here: beside the fair skin it read as a bare back)
    mix(B, ramp(form + 0.1, WHITE), inside(-col_d))                                             # the collar goes round
    mix(B, hexv("#1b1a20"), inside(np.abs(col_d) - 0.0030))

    # ----- the sleeves: red to the elbow (|y| 0.30), a vambrace from there
    A = I["arms"]
    # (red from the shoulder: the left arm's band and bracer, the right's pauldron and gauntlet are modelled over it;
    # a painted shoulder cap read as a bare white shoulder, pass 1)
    mix(A, ramp(form + 0.05, SILVER), inside(0.300 - Y))
    mix(A, ramp(form, GOLD), inside(np.abs(Y - 0.300) - 0.004))

    # ----- the straps across the waist: black leather, the reference's fasteners; the chest crest: the dark studded jabot
    for k in ("straps", "crest"):
        mix(I[k], ramp(tone(L, I[k] & (gold_k < 0.3)) * 0.8, BLACK), 1 - gold_k)
        mix(I[k], ramp(tone(L, I[k] & (gold_k > 0.7)), GOLD), gold_k)

    C = I["crest"]                                                                              # the jabot's studs
    for z0 in (1.195, 1.170, 1.145):
        mix(C, hexv("#d5d8e2"), inside(np.hypot(Y - 0.011, Z - z0) - 0.0042))

    # ----- gloves: black, the fingers plated
    hands = I["hand1"] | I["hand2"] | I["hand3"] | I["hand4"]
    mix(hands, ramp(tone(L, hands), BLACK))
    fingers = np.isin(M.bone, [i for i, b in enumerate(M.bones) if b[:-3] in ("Index", "Middle") or b.startswith("Thumb2")])
    mix(hands & fingers, ramp(tone(L, hands), SILVER))

    # ----- skin and fur: the face and neck fair, the ears and tail the hair's blonde
    head = I["head"]
    mix(head, ramp(tone(L, head), SKIN))
    mix(I["inner"], ramp(np.full(Y.shape, 0.36), SKIN))        # the head's side under the hair (dark fur before)
    choker = head & (Z < 1.30)                                 # the choker: the suit's white collar, black where it was gold
    mix(choker, ramp(tone(L, choker & (s < 0.2)) * 0.5 + 0.4, WHITE), (1 - sstep(s, 0.15, 0.25)) * (1 - sstep(v, 0.78, 0.86)))
    mix(choker, hexc_white, gold_k)                            # (black here came out as a dotted line under the chin)
    for k in ("ears", "tail", "tip"):
        mix(I[k], ramp(tone(L, I[k]), BLOND))
    return np.dstack([np.clip(out, 0, 255), alpha]).astype(np.uint8)


def paint_main(debug):
    """The skin, its checks, the hero from four sides, and original | new | reference side by side (--ref <picture>:
    the user's reference, copied beside the shots; it is theirs, so it stays out of git)."""
    d = OUT / "knight"
    d.mkdir(parents=True, exist_ok=True)
    skin = knight(debug)
    orig = np.asarray(Image.open(DATA / "cat" / "tex" / "champion1.webp").convert("RGBA"))
    assert skin.shape == orig.shape, "a skin keeps the original's size"
    hidden = skin[..., 3] != orig[..., 3]
    assert hidden.mean() < 0.06 and (skin[..., 3][hidden] == 0).all(), "only the shield's texels lose their alpha"
    Image.fromarray(skin, "RGBA").save(d / "champion.png")
    views = ((0, "front"), (90, "left"), (180, "back"), (270, "right"))
    asyncio.run(shots("cat", "champion", [("orig", {}, {})], OUT, yaws=views[:1], size=1000, dpr=2))
    asyncio.run(shots("cat", "champion", [("knight", {"cat|outfits|champion|": d / "champion.png"}, {})], OUT, yaws=views, size=1000, dpr=2, face=38))
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
<figure><img src=knight/champion.png style="width:48%"><figcaption>ลาย (512 × 512)</figcaption></figure>""", encoding="utf-8")
    print("painted", d / "champion.png")
    print("preview:", (OUT / "knight.html").as_uri())


if __name__ == "__main__":
    paint_main("--debug" in sys.argv) if "--paint" in sys.argv else main()
