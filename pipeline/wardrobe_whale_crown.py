r"""The Whale as the reference's crowned figure (2026-11-13; user: a reference picture, "Whale skin, pick the best equipment
set for this ref image and build the texture"; the reskin-from-image skill: only what the picture shows). The picture:
big purple curls under a small red and gold crown, a wide toothy grin with dark purple lips, teal eyeshadow and spiked
lashes, tan skin, a crimson leotard cut to a deep V with a high collar, a dark skull-and-crossed-bars mark on the bare
chest, a pearl necklace, magenta gloves and boots, a white net cape, net stockings with black garters.
The base (wardrobe_outfit_sheet.py showed all 22 outfits and the head pieces): **superStar**: its open coat is the cape,
its fur collar and lapels the high collar, its necklace of banknotes the pearls, its shirt panel the bare chest and the
leotard's V. Head piece **fanKingHat** (a red and gold crown as it is); the curls are painted on the Whale's own dome.
Painted on the 3D surface (wardrobe_repaint.texel_maps: bone, bind-pose position, normal, UV island per texel).
  uv run --no-project --with pillow --with numpy --with scipy --with playwright python -I pipeline/wardrobe_whale_crown.py --paint [--debug] [--noshots]
Outputs plans/reskins/whale/: crown/superStar.png (2048 px), crown/Wolf_fanKingHat.png (the crown, its gems white),
crown/Wolf_afro.png (the afro in the hair's purple: the alternative head piece), shots/, crown_compare.png, crown.html.
`--darkmouth` keeps the mouth's inside dark instead of painting more teeth there. Nothing is transparent (the game draws
outfits as RGB24 + Diffuse): unwanted parts are painted (`paint_under`), and main() asserts it."""
import asyncio, sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.spatial import cKDTree
sys.path.insert(0, str(Path(__file__).resolve().parent))      # python -I leaves the script's folder off the path
from wardrobe_repaint import ROOT, DATA, cached_maps, sstep, ramp, tone, shots, hsv, paint_under
from wardrobe_bat_robe import vnoise, folds

CLS, OUTFIT, HEAD = "whale", "superStar", "fanKingHat"
OUT = ROOT / "plans" / "reskins" / "whale"
HI = 4                                           # the skin's scale: 2048 px
FACE = 13                                        # BB's face 13: white almond eyes with a pupil (the lashes and shadow are painted round them)
AA = 0.0018                                      # about a texel at 2048 px, in body units (the Whale is 2.5 tall)

# Colours: sampled from the reference picture (k-means of its pixels), each a shadow / base / light ramp
SKIN = ("#a5806c", "#e3c4a1", "#f6e2c6")
HAIR = ("#3b2e88", "#6b59cd", "#9a8cea")
CURL = "#3f3290"
LIP = ("#261d5c", "#44378f", "#7466c9")
CRIMSON = ("#56072a", "#9f0f48", "#d43f74")      # the leotard and its collar
MAGENTA = ("#560b3a", "#95165e", "#cf4f9a")      # gloves and boots
NETFILL = ("#55525a", "#868388", "#b4b0b8")      # between the cape's lines
STOCK = ("#5e4d4c", "#93807a", "#bca8a0")        # between the stockings' lines: the leg seen through
NETLINE = "#dcdae0"
TEAL = "#7fc6d2"
INK = "#2b1714"                                  # the reference's dark brown line
BLACK = "#0d0b0a"
PEARL = ("#8f8a99", "#e8eaed", "#ffffff")

# Sheet seeds (x, y on the game's 512 px sheet) of the UV islands; body coordinates: x front, y left, z up (bind pose):
# the dome z 1.63-2.42 (its rim over the mouth z 2.05 at the middle, 1.69 at the corners), eyes at |y| 0.6, z 2.0, the
# lower jaw 1.32-1.82, the shirt panel z 0.43-1.44 (|y| < 0.54), the coat 0.32-1.55, arms out to |y| 1.6, legs 0.09-0.46
SEEDS = dict(domeF=(154, 58), fin=(17, 19), domeB=(405, 70), jaw=(152, 207), collar=(391, 188), coat=(369, 310),
             handA=(32, 232), handB=(31, 272), sleeve=(165, 307), mouth=(58, 379), pants=(238, 437), chain=(305, 390),
             panel=(447, 454), fluke=(114, 478), sole=(374, 487), foot=(276, 495), note=(335, 145), coin=(478, 142))
hexv = lambda c: np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], float)


def maps(K):
    return cached_maps(CLS, OUTFIT, K, OUT / "_cache")


def face_eyes():
    """The face preset's two eyes on the 512 px sheet: centre (x, y) of each (the overlay is 256 px, drawn 1:1)."""
    a = np.asarray(Image.open(DATA / CLS / "faces" / f"{FACE}.webp").convert("RGBA"))[..., 3] > 40
    lab, n = ndimage.label(ndimage.binary_dilation(a, iterations=3))
    cs = sorted(ndimage.center_of_mass(a, lab, range(1, n + 1)), key=lambda c: c[1])
    return [(c[1], c[0]) for c in (cs[0], cs[-1])]


def paint(debug=False, K=HI):
    im = Image.open(DATA / CLS / "tex" / f"{OUTFIT}1.webp").convert("RGBA")
    im = im.resize((im.width * K, im.height * K), Image.LANCZOS)
    src = np.asarray(im).astype(float)
    M = maps(K)
    L = ndimage.gaussian_filter(src[..., :3] @ [0.299, 0.587, 0.114] / 255, 1.0 * K)
    out = src[..., :3].copy()
    I = {k: (M.lab == M.lab[y * K + K // 2, x * K + K // 2]) for k, (x, y) in SEEDS.items()}
    ins = lambda d, aa=AA: 1 - sstep(d, -aa, aa)                 # 1 where d < 0, a soft edge
    X, Ys, Z = M.pos[..., 0], M.pos[..., 1], M.pos[..., 2]
    Y = np.abs(Ys)
    nx, ny, nz = M.nrm[..., 0], M.nrm[..., 1], M.nrm[..., 2]
    Pm = M.pos
    full = lambda x: np.full(Y.shape, float(x))
    rampc = lambda t, cols: ramp(np.clip(t, 0, 1), cols)
    bn = lambda *names: np.isin(M.bone, [i for i, b in enumerate(M.bones) if b in names or b[:-2] in names])

    def mix(m, col, k=1.0):
        k = np.broadcast_to(np.asarray(k, float), m.shape)[..., None]
        out[m] = (out * (1 - k) + col * k)[m]

    # painted light: from above and a little from the front, the islands' edges a shade darker
    form = ndimage.gaussian_filter(0.5 + 0.24 * nz + 0.06 * nx - 0.08 * np.abs(ny) - 0.10 * (1 - sstep(M.edge, 0, 7 * K)) * M.covered, 1.5 * K)

    # ---------- the dome: purple curls; a band of face over the mouth ----------
    dome = I["domeF"] | I["domeB"] | I["fin"]
    # the mouth's upper rim: the front island's boundary on its front side (its other boundary is the seam to the back)
    rimF = I["domeF"] & M.covered & (M.edge < 1.6) & (X > 0.385)
    d_rim = np.full(Y.shape, 9.0)
    d_rim[I["domeF"]] = cKDTree(Pm[rimF]).query(Pm[I["domeF"]])[0]
    # the hairline: low over the middle of the brow, higher round the eyes, scalloped by the curls; hair again past the eyes
    hairline = 0.140 + 0.17 * sstep(Y, 0.30, 0.56)
    f_face = np.maximum(d_rim - hairline, (0.27 - X) * 0.9)
    # curls: cells round scattered points on the dome (in 3D, so they cross the seams), each a puff with a spiral line
    pts = Pm[dome & M.covered]
    rng = np.random.default_rng(7)
    seeds = []
    for p in pts[rng.permutation(len(pts))[:30000]]:
        if not seeds or np.min(np.linalg.norm(np.array(seeds) - p, axis=1)) > 0.165:
            seeds.append(p)
    S = np.array(seeds)
    Sn = M.nrm[dome & M.covered][cKDTree(pts).query(S)[1]]
    up = np.array([0, 0, 1.0])
    T1 = np.cross(up, Sn); T1[np.linalg.norm(T1, axis=1) < 1e-3] = (1, 0, 0)
    T1 /= np.linalg.norm(T1, axis=1, keepdims=True)
    T2 = np.cross(Sn, T1)
    rot, flip = rng.random(len(S)) * 2 * np.pi, np.where(rng.random(len(S)) < 0.5, -1.0, 1.0)
    # (the points looked up a little off their place, by a smooth noise: the cells' edges wander instead of a honeycomb)
    Pd = Pm[dome]
    warp = np.stack([vnoise(Pd[:, (i + 1) % 3] / 0.09 + 7 * i, Pd[:, (i + 2) % 3] / 0.09, 40 + i) - 0.5 for i in range(3)], 1) * 0.07
    (d1, d2), (i1, _) = (a.T for a in cKDTree(S).query(Pd + warp, k=2))
    size = 0.8 + 0.45 * rng.random(len(S))                     # no two curls the same size
    rel = (Pd + warp - S[i1]) / size[i1][:, None]
    a_, b_ = (rel * T1[i1]).sum(1) * flip[i1], (rel * T2[i1]).sum(1)
    r, phi = np.hypot(a_, b_), np.arctan2(b_, a_) + rot[i1]
    pitch = 0.062
    sp = r / pitch - phi / (2 * np.pi)
    line = np.abs(sp - np.round(sp)) * pitch                    # distance to the spiral's line
    spiral = ins(line - 0.0085) * ins(r - 0.105) * sstep(r, 0.004, 0.02)
    glint = ins(np.abs((sp + 0.33) - np.round(sp + 0.33)) * pitch - 0.006) * ins(r - 0.09) * sstep(r, 0.02, 0.04)
    crease = 1 - sstep(d2 - d1, 0.0, 0.05)                      # between two curls
    t = np.zeros(Y.shape); cr = np.zeros(Y.shape); spl = np.zeros(Y.shape); gl = np.zeros(Y.shape)
    t[dome] = 0.52 + 0.20 * (1 - sstep(d1, 0.0, 0.13)); cr[dome] = crease; spl[dome] = spiral; gl[dome] = glint
    bulge = np.zeros(Y.shape); bulge[dome] = d1
    f_face = f_face - 0.55 * (bulge - 0.075) * I["domeF"]      # the hair's edge follows the curls: each one bulges over the skin
    face = ins(f_face) * I["domeF"]
    if debug:
        print("curls:", len(S))
    mix(dome, rampc(t + 0.85 * (form - 0.5) - 0.36 * cr + 0.10 * gl, HAIR))
    mix(dome, hexv(CURL), spl * 0.85)
    mix(dome, rampc(full(0.12), HAIR), cr * 0.55 * np.where(I["domeF"], sstep(f_face, 0.0, 0.035), 1))    # (no dark notches along the brow)
    # the face: skin, a shade under the hairline, a nose's hint, the creases from the nose to the mouth's corners
    mix(dome, rampc(0.52 + 0.9 * (form - 0.5) - 0.09 * sstep(f_face, -0.035, 0.0), SKIN), face)
    mix(dome, hexv(CURL), ins(np.abs(f_face) - 0.003) * I["domeF"] * 0.4)           # the hair's edge on the skin
    # the lips: a thick dark purple band round the whole grin, a lighter line along its middle
    lipU = ins(d_rim - 0.058) * I["domeF"]
    mix(dome, rampc(0.50 + 0.9 * (form - 0.5), LIP), lipU)
    mix(dome, rampc(full(0.9), LIP), ins(np.abs(d_rim - 0.030) - 0.006, 0.005) * I["domeF"] * 0.45)
    mix(dome, hexv(INK), ins(np.abs(d_rim - 0.058) - 0.0035) * I["domeF"] * 0.8)

    # the eyes' paint (the face preset draws the eye itself): teal shadow sweeping up and out, a black rim, spiked lashes
    for ex, ey in face_eyes():
        E, En = Pm[int(ey * K), int(ex * K)], M.nrm[int(ey * K), int(ex * K)]
        side = np.sign(E[1])
        t1 = np.cross(up, En); t1 /= np.linalg.norm(t1)
        outw = t1 * side                                         # along the skin, away from the nose
        upw = up - (up @ En) * En; upw /= np.linalg.norm(upw)
        near = I["domeF"] & (np.linalg.norm(Pm - E, axis=-1) < 0.4)
        a, b = (Pm - E) @ outw, (Pm - E) @ upw
        if debug:
            print("eye", E.round(3), "normal", En.round(2))
        sh = np.hypot((a - 0.035) / 0.150, (b - 0.045 - 0.25 * np.maximum(a, 0)) / 0.105)
        mix(near, hexv(TEAL), (1 - sstep(sh, 0.72, 1.0)) * face * 0.92)
        mix(near, hexv("#4f9fb0"), ins(np.abs(sh - 0.92) * 0.1 - 0.004, 0.004) * face * 0.5)
        ring = np.hypot(a / 0.066, b / 0.052)
        lash = np.zeros(Y.shape)
        for deg, ln in ((-25, 0.050), (15, 0.070), (50, 0.078), (88, 0.072), (126, 0.066), (165, 0.052), (205, 0.040)):
            c, s_ = np.cos(np.radians(deg)), np.sin(np.radians(deg))
            along, perp = a * c + b * s_, -a * s_ + b * c
            u = (along - 0.050) / ln                             # 0 at the rim, 1 at the spike's tip
            lash = np.maximum(lash, ins(np.abs(perp) - 0.019 * (1 - u)) * (u > -0.3) * (u < 1))
        mix(near, hexv(BLACK), np.maximum(lash, ins(np.abs(ring - 1.0) * 0.055 - 0.011)) * face)

    # ---------- the lower jaw: the chin, the lower lip ----------
    J = I["jaw"]
    rimJ = J & M.covered & (M.edge < 1.6) & (Z > 1.70 - 0.25 * sstep(Y, 0.45, 0.8))
    d_low = np.full(Y.shape, 9.0)
    d_low[J] = cKDTree(Pm[rimJ]).query(Pm[J])[0]
    mix(J, rampc(0.50 + 0.9 * (form - 0.5) - 0.16 * sstep(-d_low, -0.16, -0.06) - 0.20 * sstep(-Z, -1.47, -1.36), SKIN))
    mix(J, rampc(0.50 + 0.9 * (form - 0.5), LIP), ins(d_low - 0.062))
    mix(J, rampc(full(0.9), LIP), ins(np.abs(d_low - 0.030) - 0.006, 0.005) * 0.45)
    mix(J, hexv(INK), ins(np.abs(d_low - 0.062) - 0.0035) * 0.8)
    mix(J, hexv("#956e5e"), ins(np.abs(Z - (1.615 - 2.2 * Ys ** 2)) - 0.0045) * ins(Y - 0.085, 0.02) * 0.7)   # the crease under the lip
    # inside the mouth: the reference's grin is a wall of teeth, the Whale's are blocks with gaps: the mouth's inside is
    # painted as more teeth behind them (off-white, a dark line between the rows and between the teeth), so the gaps close
    Mo = I["mouth"]
    if "--darkmouth" in sys.argv:
        mix(Mo, src[..., :3] * 0.30 + hexv("#1a0d16") * 0.70)
    else:
        mix(Mo, rampc(0.74 + 0.3 * (form - 0.5) - 0.12 * sstep(-X, -0.1, 0.3), ("#8d8b9e", "#dcdce3", "#f6f6fa")))
        mix(Mo, hexv("#2a2140"), ins(np.abs((Y / 0.19 + 0.5) % 1 - 0.5) * 0.19 - 0.006) * 0.8)
        mix(Mo, hexv("#2a2140"), ins(np.abs(Z - 1.925) - 0.007) * 0.85)

    # ---------- the collar and its lapels: crimson ----------
    C = I["collar"]
    mix(C, rampc(0.44 + 0.35 * (tone(ndimage.gaussian_filter(L, 3 * K), C) - 0.5) + 0.9 * (form - 0.5), CRIMSON))
    mix(C, rampc(full(0.95), CRIMSON), ins(np.abs(M.edge - 3.0 * K) - 1.0 * K, 0.6) * M.covered * 0.30)      # a piped edge

    # ---------- the cape: a white net. The coat has no body under it (holes all over it showed a hollow Whale from the
    # side and behind), so the net is painted over grey, as the reference's cape reads; real holes open toward the hem,
    # where the legs are behind it ----------
    Ct = I["coat"]
    arc = np.arctan2(Y, X) * 0.85                                # round the body, in body units
    CELL = 0.105
    u, v = (arc + Z) / CELL, (arc - Z) / CELL
    dl = np.minimum(np.abs(u - np.round(u)), np.abs(v - np.round(v))) * CELL / np.sqrt(2)     # distance to the nearest line
    drape = folds(arc, Z, 0.11, 11) * (0.4 + 0.6 * sstep(1.3 - Z, 0.0, 0.7))
    mix(Ct, rampc(0.42 + 0.9 * (form - 0.5) + 0.20 * drape, NETFILL))
    mix(Ct, hexv("#3d3a42"), ins(dl - 0.0125, 0.004) * 0.35)                                    # a soft shade beside the line
    mix(Ct, hexv(NETLINE) * (0.80 + 0.20 * np.clip(0.5 + form + 0.2 * drape, 0, 1))[..., None], ins(dl - 0.0075))
    # (no real holes: an outfit cannot be see-through in the game, RGB24 + Diffuse. The hem's open mesh of the first
    # passes was alpha 0: the net is painted over the grey down to the hem, as on the rest of the cape)

    # ---------- the arms: bare; magenta gloves with a pointed cuff ----------
    A = I["sleeve"]
    round_arm = np.arctan2(nx, nz)
    cuff = 1.33 + 0.045 * np.abs(np.sin(1.5 * round_arm))
    mix(A, rampc(0.52 + 1.0 * (form - 0.5), SKIN))
    mix(A, rampc(0.50 + 1.0 * (form - 0.5), MAGENTA), ins(cuff - Y))
    mix(A, rampc(full(0.92), MAGENTA), ins(np.abs(Y - cuff - 0.022) - 0.006, 0.004) * 0.5)
    mix(A, hexv("#3d0627"), ins(np.abs(Y - cuff) - 0.004))
    for k in ("handA", "handB"):
        mix(I[k], rampc(0.15 + 0.8 * tone(L, I[k]), MAGENTA))

    # ---------- the chest: bare, the leotard's deep V, the dark mark ----------
    P = I["panel"]
    Vz = 0.58 + 0.75 * Y + 1.3 * Y ** 2                         # the V's edge: skin above it
    d_v = (Z - Vz) / np.hypot(1, 0.75 + 2.6 * Y)
    chest = 0.54 - 0.10 * np.exp(-(Ys / 0.035) ** 2) * sstep(Z, 0.62, 0.8) * (1 - sstep(Z, 1.05, 1.2)) \
        - 0.16 * np.exp(-((Z - (0.985 - 1.1 * (Y - 0.24) ** 2)) / 0.03) ** 2) * sstep(Y, 0.03, 0.10) \
        + 0.08 * np.exp(-((Y - 0.24) / 0.16) ** 2 - ((Z - 1.12) / 0.11) ** 2) - 0.18 * sstep(Z, 1.25, 1.44)
    mix(P, rampc(ndimage.gaussian_filter(chest, 2 * K), SKIN))
    pec = np.abs(Z - (0.985 - 1.1 * (Y - 0.24) ** 2)) - 0.0035
    mix(P, hexv("#956e5e"), ins(pec) * ins(np.abs(Y - 0.235) - 0.165, 0.02) * 0.75)             # under each pec
    mix(P, hexv("#956e5e"), ins(Y - 0.003) * ins(np.abs(Z - 0.69) - 0.07, 0.02) * 0.6)          # the belly's line
    leo = 0.46 + 0.5 * (form - 0.5) + 0.10 * folds(Ys, Z, 0.06, 31) + 0.20 * sstep(d_v, -0.10, -0.01) * 0 - 0.10 * sstep(-Z, -0.62, -0.45)
    mix(P, hexv("#8f6a5c"), ins(d_v - 0.012, 0.010) * 0.45)                                     # its shade on the skin
    mix(P, rampc(leo, CRIMSON), ins(d_v))
    mix(P, rampc(full(0.93), CRIMSON), ins(np.abs(d_v + 0.016) - 0.004, 0.003) * 0.5)
    mix(P, hexv("#3d0420"), ins(np.abs(d_v) - 0.0045))
    # the mark: a skull over two crossed bars with curled ends, in the reference's dark brown
    MK = 1.22                                                    # the mark's size
    Ys_, Y_ = Ys, Y
    Ys, Y, cz = Ys / MK, Y / MK, (Z - 0.865) / MK
    skull = np.minimum(np.hypot(Ys / 0.074, (cz - 0.012) / 0.066) - 1, np.maximum(np.abs(Ys) / 0.045 - 1, np.abs(cz + 0.062) / 0.028 - 1)) * 0.06
    bars = np.full(Y.shape, 9.0)
    for sgn in (1, -1):
        c, s_ = np.cos(np.radians(34)), np.sin(np.radians(34)) * sgn
        along, perp = Ys * c + cz * s_, -Ys * s_ + cz * c
        bars = np.minimum(bars, np.maximum(np.abs(perp) - 0.0115, np.abs(along) - 0.175))
        for e in (1, -1):                                        # each end: a curl (a ring, open toward the bar)
            qy, qz = Ys - e * 0.192 * c + e * 0.022 * s_ * 0, cz - e * 0.192 * s_
            bars = np.minimum(bars, np.abs(np.hypot(qy, qz) - 0.024) - 0.0095)
    tail = np.maximum(np.abs(Ys) - 0.011 - 0.9 * np.maximum(-(cz + 0.150), 0) * 0 + 0.35 * np.maximum(cz + 0.19, 0) * 0, np.abs(cz + 0.135) - 0.045)
    tail = np.minimum(tail, np.hypot(Ys, cz + 0.185) - 0.021)
    mark = np.minimum(np.minimum(skull, bars), tail)
    holes = np.minimum(np.hypot((Y - 0.030) / 0.021, (cz - 0.012) / 0.024) - 1, np.hypot(Ys / 0.009, (cz + 0.022) / 0.013) - 1) * 0.02
    teeth = np.minimum(np.abs(np.abs(Ys) - 0.015) - 0.003, np.abs(Ys) - 0.003)
    teeth = np.maximum(teeth, np.abs(cz + 0.066) - 0.019)
    skin_now = out.copy()
    mix(P, hexv(INK) * 0.5 + hexv("#4c3842") * 0.5, ins(mark) * (d_v > 0.0))
    for cut in (holes, teeth):
        mix(P, skin_now, ins(cut) * ins(skull + 0.004))
    Ys, Y = Ys_, Y_

    # ---------- the necklace: pearls, two to a banknote; the gold chain and its coin painted as the chest under them.
    # (Nothing is hidden with alpha: the game ignores it. The notes' texels are shared by every note of the necklace,
    # each over a different place, so they cannot take "what is under": two large touching pearls fill each note, the
    # corners between them a bead-gap shadow) ----------
    for k in ("chain", "coin"):
        paint_under(out, M, I[k], I["panel"] | I["collar"] | I["coat"])
    Nt = I["note"]
    ys, xs = np.where(Nt & M.covered)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    yy, xx = np.mgrid[:Y.shape[0], :Y.shape[1]]
    rad = min((y1 - y0) / 2, (x1 - x0) / 4)
    mix(Nt, hexv("#3e3946"))                                     # between the beads: shadow
    for cx in (x0 + (x1 - x0) * 0.25, x0 + (x1 - x0) * 0.75):
        cy = (y0 + y1) / 2
        dd = np.hypot(xx - cx, yy - cy) / rad
        ball = Nt & (dd < 1)
        lit = 0.62 - 0.50 * dd ** 2 + 0.55 * np.exp(-(((xx - cx) / rad + 0.32) ** 2 + ((yy - cy) / rad + 0.36) ** 2) / 0.07) \
            + 0.16 * np.exp(-(((xx - cx) / rad - 0.45) ** 2 + ((yy - cy) / rad - 0.5) ** 2) / 0.10)
        mix(ball, rampc(lit, PEARL))
        mix(ball, hexv("#6f6a7c"), sstep(dd, 0.86, 1.0) * 0.55)

    # ---------- below: the leotard's seat, net stockings held by black garters, magenta boots; the Whale's own tail
    # in the body's skin ----------
    G = I["pants"]
    mix(G, rampc(0.46 + 1.0 * (form - 0.5), CRIMSON))
    legtube = G & bn("Thigh", "Leg", "Foot")
    la = np.arctan2(Y - 0.60, X) * 0.21                          # round the leg
    SC = 0.062
    u, v = (la + Z) / SC, (la - Z) / SC
    dl = np.minimum(np.abs(u - np.round(u)), np.abs(v - np.round(v))) * SC / np.sqrt(2)
    GART, BOOT = 0.385, 0.185
    mix(legtube, rampc(0.48 + 1.0 * (form - 0.5), STOCK))
    mix(legtube, hexv(NETLINE), ins(dl - 0.0055) * 0.92)
    mix(legtube, hexv(BLACK), ins(GART - Z) * 0.96)                                             # the garter's band
    mix(legtube, hexv("#55504f"), ins(np.abs(Z - GART - 0.022) - 0.004, 0.003) * 0.5)
    strap = ins(np.abs(Y - 0.60) - 0.030) * sstep(X, 0.05, 0.2) * ins(GART - Z) * ins(Z - 0.56)   # up the thigh's front to the leotard
    mix(G, hexv(BLACK), strap * 0.96)
    mix(legtube, rampc(0.50 + 1.1 * (form - 0.5), MAGENTA), ins(Z - BOOT))
    mix(legtube, rampc(full(0.92), MAGENTA), ins(np.abs(Z - BOOT + 0.02) - 0.006, 0.004) * 0.5)
    mix(legtube, hexv("#3d0627"), ins(np.abs(Z - BOOT) - 0.004))
    mix(I["foot"], rampc(0.2 + 0.7 * tone(L, I["foot"]), MAGENTA))
    mix(I["sole"], rampc(full(0.12), MAGENTA))
    tail_k = ins(X + 0.62, 0.03) * (G & ~legtube)
    mix(G, rampc(0.50 + 1.0 * (form - 0.5), SKIN), tail_k)
    mix(I["fluke"], rampc(0.46 + 1.0 * (form - 0.5), SKIN))
    return np.dstack([np.clip(out, 0, 255), np.full(out.shape[:2], 255.0)]).astype(np.uint8)


def head_pieces(d):
    """The two head pieces' own textures (the Whale wears the Wolf's files): the crown's blue and green gems become the
    reference's white dots; the afro, the alternative to the crown (one head piece at a time), in the hair's purple
    with the same spiral curls (on a grid of the sheet, so the texture still tiles)."""
    im = Image.open(DATA / "props" / "tex" / "Wolf_fanKingHat.png").convert("RGBA")
    a = np.asarray(im).astype(float)
    h, s_, v = hsv(a[..., :3])
    gem = ndimage.gaussian_filter(((h > 90) & (h < 270) & (s_ > 0.28)).astype(float), 0.6)[..., None]
    lum = (a[..., :3] @ [0.299, 0.587, 0.114] / 255)
    a[..., :3] = a[..., :3] * (1 - gem) + ramp(np.clip(0.25 + lum * 1.1, 0, 1), PEARL) * gem
    Image.fromarray(a.astype(np.uint8), "RGBA").save(d / "Wolf_fanKingHat.png")
    K = 4
    im = Image.open(DATA / "props" / "tex" / "Wolf_afro.png").convert("RGBA")
    im = im.resize((im.width * K, im.height * K), Image.LANCZOS)
    a = np.asarray(im).astype(float)
    lum = ndimage.gaussian_filter(a[..., :3] @ [0.299, 0.587, 0.114] / 255, 2 * K, mode="wrap")
    n, N = 6, im.width                                           # 6 x 6 curls, every other row shifted half a cell
    yy, xx = np.mgrid[:N, :N] / (N / n)
    row = np.floor(yy)
    cx = xx + 0.5 * (row % 2)
    ci, cj = np.floor(cx).astype(np.int64) % n, row.astype(np.int64) % n
    hsh = ((ci * 7 + cj * 13 + ci * cj * 5) % 17) / 17.0
    fx, fy = cx - np.floor(cx) - 0.5, yy - row - 0.5
    r, phi = np.hypot(fx, fy), np.arctan2(fy, fx * np.where(hsh > 0.5, 1, -1)) + hsh * 6.283
    pitch = 0.26
    sp = r / pitch - phi / 6.283
    line = np.abs(sp - np.round(sp)) * pitch
    t = 0.50 + 0.9 * (tone(lum, np.ones(lum.shape, bool)) - 0.5) * 0.5 + 0.22 * (1 - sstep(r, 0.0, 0.5)) - 0.30 * sstep(r, 0.38, 0.52)
    col = ramp(np.clip(t, 0, 1), HAIR)
    k = ((1 - sstep(line, 0.028, 0.045)) * (1 - sstep(r, 0.40, 0.46)) * sstep(r, 0.02, 0.07) * 0.85)[..., None]
    a[..., :3] = col * (1 - k) + hexv(CURL) * k
    Image.fromarray(a.astype(np.uint8), "RGBA").save(d / "Wolf_afro.png")


def paint_main(debug, noshots):
    d = OUT / "crown"
    d.mkdir(parents=True, exist_ok=True)
    skin = paint(debug)
    orig = Image.open(DATA / CLS / "tex" / f"{OUTFIT}1.webp")
    assert skin.shape[:2] == (orig.height * HI, orig.width * HI), "a skin is the original's size or 2x / 4x / 8x of it (the page's skinDims)"
    assert (skin[..., 3] == 255).all(), "an outfit skin is opaque: the game ignores alpha (paint a part, never hide it)"
    Image.fromarray(skin, "RGBA").save(d / f"{OUTFIT}.png", optimize=True)
    print(f"{skin.shape[1]}x{skin.shape[0]} px, {(d / f'{OUTFIT}.png').stat().st_size / 1e6:.1f} MB")
    head_pieces(d)
    if noshots:
        return
    views = ((0, "front"), (90, "left"), (180, "back"), (270, "right"), (25, "q"))
    if not (OUT / "shots" / "orig_front.png").exists():
        asyncio.run(shots(CLS, OUTFIT, [("orig", {}, {})], OUT, yaws=views[:1], size=1000, dpr=2))
    skins = {f"{CLS}|outfits|{OUTFIT}|": d / f"{OUTFIT}.png", f"{CLS}|accessories|{HEAD}|Wolf_fanKingHat.png": d / "Wolf_fanKingHat.png",
             f"{CLS}|accessories|afro|Wolf_afro.png": d / "Wolf_afro.png"}
    asyncio.run(shots(CLS, OUTFIT, [("crown", skins, {"Head": HEAD}), ("afro", skins, {"Head": "afro"})], OUT, yaws=views, size=1000, dpr=2, face=FACE))
    panels = [Image.open(OUT / "shots" / f"{n}_front.png") for n in ("orig", "crown", "afro")]
    for f in sorted(OUT.glob("reference*.png")):                        # the user's picture: theirs, not in git
        ref = Image.open(f).convert("RGB")
        panels.append(ref.resize((round(ref.width * 1000 / ref.height), 1000), Image.LANCZOS))
    sheet = Image.new("RGB", (sum(p.width for p in panels), 1000), (230, 225, 216))
    x = 0
    for p in panels:
        sheet.paste(p, (x, 0)); x += p.width
    sheet.save(OUT / "crown_compare.png")
    imgs = "".join(f"<img src=shots/crown_{s}.png>" for _, s in views[:4])
    (OUT / "crown.html").write_text(f"""<!doctype html><meta charset=utf-8><title>Whale: crown</title>
<style>body{{font-family:system-ui,sans-serif;background:#f4f1ea;margin:16px}}figure{{margin:0 0 16px;background:#fff;border-radius:10px;padding:8px}}
figure img{{width:24%;min-width:200px}}.cmp img{{width:100%;min-width:0}}figcaption{{font-weight:600;margin:4px}}</style>
<h1>วาฬ · ชุด Super Star ตามภาพอ้างอิง</h1>
<figure class=cmp><img src=crown_compare.png><figcaption>ของเดิม · ของใหม่ + มงกุฎ (Fan King Hat, หน้าแบบที่ {FACE}) · ของใหม่ + ผมแอฟโฟร (Afro) · ภาพอ้างอิง</figcaption></figure>
<figure>{imgs}<figcaption>มงกุฎ · หน้า ซ้าย หลัง ขวา</figcaption></figure>
<figure>{imgs.replace("crown_", "afro_")}<figcaption>ผมแอฟโฟร · หน้า ซ้าย หลัง ขวา</figcaption></figure>
<figure><img src=crown/{OUTFIT}.png style="width:48%"><figcaption>ลายชุด ({skin.shape[1]} × {skin.shape[0]})</figcaption></figure>""", encoding="utf-8")
    print("preview:", (OUT / "crown.html").as_uri())


if __name__ == "__main__":
    paint_main("--debug" in sys.argv, "--noshots" in sys.argv)
