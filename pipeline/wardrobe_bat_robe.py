r"""The Bat as the reference's robed student (2026-11-12; user: two reference pictures, a long black robe lined green over a
grey V-neck sweater with green trim, a white shirt, a green and silver striped tie, a grey pleated skirt, black tights,
black loafers, long platinum hair, green eyes; "try this reference character for Bat, you may pick the best models").
The base is the Bat's **student** outfit (wardrobe_outfit_sheet.py showed all 22): its open long coat is the robe, it
has the shirt, the tie (its own mesh piece), a skirt, bare legs for the tights, pumps, and the hair on the same sheet.
Painted on the 3D surface as wardrobe_knight.py does (texel_maps: bone, bind-pose position, normal, UV island).
  uv run --no-project --with pillow --with numpy --with scipy --with playwright python -I pipeline/wardrobe_bat_robe.py --islands
  uv run --no-project --with pillow --with numpy --with scipy --with playwright python -I pipeline/wardrobe_bat_robe.py --paint [--debug]
Outputs plans/reskins/bat/: islands.png (+ a printed table), robe/student.png, shots/, robe_compare.png, robe.html."""
import asyncio, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from scipy.spatial import cKDTree
sys.path.insert(0, str(Path(__file__).resolve().parent))      # python -I leaves the script's folder off the path
from wardrobe_repaint import ROOT, DATA, texel_maps, hsv, hd, sstep, ramp, tone, shots

CLS, OUTFIT = "bat", "student"
OUT = ROOT / "plans" / "reskins" / "bat"


def islands():
    """Every UV island numbered on the sheet, and a table: where it is on the sheet and on the body, its main bones."""
    im = Image.open(DATA / CLS / "tex" / f"{OUTFIT}1.webp").convert("RGBA")
    M = texel_maps(CLS, OUTFIT, im.size)
    lab = np.where(M.covered, M.lab, 0)
    rng = np.random.default_rng(3)
    pal = rng.integers(60, 255, (lab.max() + 1, 3)); pal[0] = 255
    pic = Image.fromarray((np.asarray(im.convert("RGB")) * 0.45 + pal[lab] * 0.55).astype(np.uint8))
    d = ImageDraw.Draw(pic)
    for i in range(1, lab.max() + 1):
        m = lab == i
        if m.sum() < 60:
            continue
        ys, xs = np.where(m)
        p = M.pos[m]
        bones, n = np.unique(M.bone[m], return_counts=True)
        top = " ".join(f"{M.bones[b]}:{c * 100 // m.sum()}" for b, c in sorted(zip(bones, n), key=lambda t: -t[1])[:4])
        cy, cx = ndimage.center_of_mass(m)
        if not m[int(cy), int(cx)]:
            k = np.argmin((ys - cy) ** 2 + (xs - cx) ** 2); cy, cx = ys[k], xs[k]
        d.text((cx - 6, cy - 5), str(i), fill="black", stroke_width=2, stroke_fill="white")
        print(f"{i:3d} px={m.sum():6d} seed=({int(cx)},{int(cy)}) sheet x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()} | "
              f"X {p[:, 0].min():.2f}..{p[:, 0].max():.2f} Y {p[:, 1].min():.2f}..{p[:, 1].max():.2f} Z {p[:, 2].min():.2f}..{p[:, 2].max():.2f} | "
              f"nx {M.nrm[m][:, 0].mean():+.2f} | {top}")
    OUT.mkdir(parents=True, exist_ok=True)
    pic.save(OUT / "islands.png")
    print(OUT / "islands.png")


# ---------- the paint ----------
# Body coordinates (x front, y left, z up; the bind pose): neck z 1.33-1.41, the coat's chest 1.11-1.36, the waist 1.05,
# the skirt 0.60-1.05, the legs 0.11-0.73, the arms out to |y| 0.61, the hands beyond. The face preset is drawn at 2x
# over the sheet's top left (eyes z 1.475-1.53, |y| 0.02-0.08; the mouth z 1.43; the cheeks under the eyes z 1.45).
ROBE = ("#09090c", "#1c1c21", "#474752")
GREEN = ("#0a2c1a", "#1a6339", "#49a56e")
GREY = ("#484a51", "#81848c", "#b9bcc3")        # the sweater
SKIRT = ("#1b1c20", "#3d3f45", "#696b73")
WHITE = ("#9d9cab", "#eeeef3", "#ffffff")
TIGHT = ("#1d1516", "#4d3b39", "#8a6a61")       # sheer black tights: the skin shows through (user: "too dark to look like stockings")
SHOE = ("#050506", "#16161a", "#7b7b88")
BLOND = ("#a89059", "#e9dca8", "#fffbe8")       # platinum
SKIN = ("#c99882", "#f6d6c2", "#fff0e4")
NAIL = ("#0c4024", "#1f8a4f", "#63cf94")        # the nails: the house's green, glossy
SILVER = "#cdd0d6"
INK = "#101013"
SEEDS = dict(chest=(866, 136), face=(125, 125), sleeve=(964, 120), pony=(527, 92), hairB=(359, 162), torsoF=(684, 217),
             lapel=(804, 181), side1=(477, 226), coat=(901, 491), side2=(47, 339), cuffIn=(973, 291), fringe=(181, 350),
             torsoB=(484, 353), loop1=(792, 430), cap19=(745, 422), loop2=(777, 430), skirt=(563, 503), earF=(42, 507),
             earB=(133, 506), cap24=(745, 463), leg=(298, 638), hem26=(759, 514), buckle=(763, 583), arm=(540, 643),
             hand1=(127, 658), wingF=(804, 845), tie=(981, 827), lining=(896, 734), hand2=(41, 772), wingB=(494, 820),
             tieEdge=(1010, 756), neck=(136, 761), shoe=(174, 897), sole=(36, 893), heel=(76, 933), tail=(274, 996))
AA = 0.0014 / 2                                  # about a texel of the game's 1024 px sheet, in body units
HI = 2                                           # the skin's scale: 2048 px
FACE = 16                                        # BB's face 16: green eyes, a stern brow (the second reference)
V_Z, V_K = 1.168, 3.3                            # the sweater's V: its point, and how steeply its edges rise
CREST = (0.066, 1.212)                           # the crest: y (her left), z: half under the robe's lapel


# ---------- cloth and hair: generated detail (user 2026-11-12: "give almost every part more texture, cloth wrinkles,
# hair details") ----------
def _hash(i, j, seed):
    n = (i * 374761393 + j * 668265263 + seed * 1442695041) & 0xFFFFFFFF
    n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFF) / 65535.0


def vnoise(x, y, seed=0):
    """Smooth value noise, 0..1, at any (x, y): a function of the body's coordinates, so it has no seams between islands."""
    xi, yi = np.floor(x).astype(np.int64), np.floor(y).astype(np.int64)
    fx, fy = x - xi, y - yi
    fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a, b, c, d = _hash(xi, yi, seed), _hash(xi + 1, yi, seed), _hash(xi, yi + 1, seed), _hash(xi + 1, yi + 1, seed)
    return a + (b - a) * fx + (c - a) * fy + (a - b - c + d) * fx * fy


def folds(u, w, lam, seed, long=6.0):
    """Folds that run along w, about lam wide across u (body units): the light on them, about -1..1. A height field of
    noise stretched along w (folds start and stop as on cloth, and wander), lit from the side: its slope across u."""
    u = u + 0.45 * lam * (vnoise(w / (lam * 3.0), w * 0 + 0.5, seed + 7) * 2 - 1)
    hgt = lambda uu: vnoise(uu / lam, w / (lam * long), seed) + 0.5 * vnoise(uu / lam * 2.1 + 9, w / (lam * long) * 1.7, seed + 3)
    d = 0.2 * lam
    return np.tanh(4.0 * (hgt(u + d) - hgt(u - d)))


def strands(L, flow, mask, K, n=40, seed=5):
    """Hair, drawn as hair: fields over the hair's texels (mask) that follow its strands -> dict of
    fine, coarse (0..1: strand texture, clumps), relief (-1..1: the clumps lit from one side), dark, light (0..1: single
    strands as thin lines that taper out at both ends). The strands' direction: along the original's own strokes (the
    smoothed structure tensor of its luminance), along the nearest side edge of the lock (so the lines run together
    into a lock's point instead of being cut by it), and where neither says much, down `flow` (z: down the hair)."""
    ys, xs = np.where(mask)
    y0, y1, x0, x1 = max(ys.min() - 8, 0), ys.max() + 8, max(xs.min() - 8, 0), xs.max() + 8
    mb = mask[y0:y1, x0:x1]
    Lb = ndimage.gaussian_filter(L[y0:y1, x0:x1], 1.2 * K)
    gy, gx = np.gradient(Lb)
    J = [ndimage.gaussian_filter(a, 9 * K) for a in (gx * gx, gx * gy, gy * gy)]
    zy, zx = np.gradient(ndimage.gaussian_filter(flow[y0:y1, x0:x1], 4 * K))
    zn = np.maximum(np.hypot(zx, zy), 1e-9)
    dnx, dny = -zx / zn, -zy / zn                               # down the hair, on the sheet
    e = 4.0 * np.median(J[0] + J[2])                            # the fallback: across the strands = that, turned a quarter
    cx, cy = -dny, dnx
    J[0] += e * cx ** 2; J[1] += e * cx * cy; J[2] += e * cy ** 2
    dist = ndimage.distance_transform_edt(mb)                   # the lock's side edges (not its root or its cut end:
    ey, ex = np.gradient(ndimage.gaussian_filter(dist, 1.5 * K))    # those lie across the way down)
    en = np.maximum(np.hypot(ex, ey), 1e-9)
    ex, ey = ex / en, ey / en
    wgt = 12 * e * np.exp(-dist / (7 * K)) * (1 - (ex * dnx + ey * dny) ** 2) ** 2
    J[0] += wgt * ex ** 2; J[1] += wgt * ex * ey; J[2] += wgt * ey ** 2
    J = [ndimage.gaussian_filter(a, 2 * K) for a in J]
    ang = 0.5 * np.arctan2(2 * J[1], J[0] - J[2])               # across the strokes; the strands run at a right angle
    fx, fy = -np.sin(ang), np.cos(ang)
    sgn = np.where(fx * dnx + fy * dny < 0, -1.0, 1.0)          # every strand pointing down the hair
    fx, fy = (fx * sgn).astype(np.float32), (fy * sgn).astype(np.float32)
    rng = np.random.default_rng(seed)
    step, s_line = 0.75 * K, 0.62 * K
    blur = lambda a, s: ndimage.gaussian_filter(a.astype(np.float32), s)
    layers = {"fine": blur(rng.random(mb.shape), 0.55 * K), "coarse": blur(rng.random(mb.shape), 2.1 * K),
              "dark": blur(rng.random(mb.shape) < 0.0013 / K ** 2, s_line), "light": blur(rng.random(mb.shape) < 0.0010 / K ** 2, s_line)}
    py0, px0 = (a.astype(np.float32) for a in np.where(mb))
    acc = {k: a[mb].astype(np.float64) for k, a in layers.items()}
    at = lambda a, py, px: ndimage.map_coordinates(a, [py, px], order=1, mode="nearest")
    for sign in (1, -1):
        px, py, dx, dy = px0.copy(), py0.copy(), fx[mb] * sign, fy[mb] * sign
        for i in range(1, n + 1):
            px += dx * step; py += dy * step
            vx, vy = at(fx, py, px), at(fy, py, px)
            flip = np.where(vx * dx + vy * dy < 0, -1, 1)                # keep going the same way
            nn = np.maximum(np.hypot(vx, vy), 1e-6)
            dx, dy = vx * flip / nn, vy * flip / nn
            w = 0.5 * (1 + np.cos(np.pi * i / (n + 1)))                 # fading out: a strand's ends taper
            for k, a in layers.items():
                acc[k] += w * at(a, py, px)
    out = {}
    for k, a in acc.items():
        whole = np.full(L.shape, 0.0 if k in ("dark", "light") else 0.5)
        if k in ("dark", "light"):
            val = np.clip(a * s_line * np.sqrt(2 * np.pi) * step, 0, 1)      # 1 = a strand's middle
        else:
            lo, hi = np.percentile(a, [2, 98])
            val = np.clip((a - lo) / (hi - lo), 0, 1)
        whole[y0:y1, x0:x1][mb] = val
        out[k] = whole
    cyy, cxx = np.gradient(ndimage.gaussian_filter(out["coarse"], 0.8 * K))
    rel = np.zeros(L.shape)
    rel[y0:y1, x0:x1] = cxx[y0:y1, x0:x1] * -fy + cyy[y0:y1, x0:x1] * fx       # the clumps' slope across the strands
    out["relief"] = np.tanh(rel / (1.3 * rel[mask].std() + 1e-9)) * mask
    return out


def robe(debug=False, K=HI):
    im = Image.open(DATA / CLS / "tex" / f"{OUTFIT}1.webp").convert("RGBA")
    im = im.resize((im.width * K, im.height * K), Image.LANCZOS)
    src = np.asarray(im).astype(float)
    M = texel_maps(CLS, OUTFIT, im.size)
    h, s, v = hsv(src[..., :3])
    L = ndimage.gaussian_filter(src[..., :3] @ [0.299, 0.587, 0.114] / 255, 1.0 * K)
    out, alpha = src[..., :3].copy(), src[..., 3].copy()
    I = {k: (M.lab == M.lab[y * K + K // 2, x * K + K // 2]) for k, (x, y) in SEEDS.items()}
    ins = lambda d, aa=AA: 1 - sstep(d, -aa, aa)
    hexv = lambda c: np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], float)
    X, Ys, Z = M.pos[..., 0], M.pos[..., 1], M.pos[..., 2]
    Y = np.abs(Ys)
    nx, ny, nz = M.nrm[..., 0], M.nrm[..., 1], M.nrm[..., 2]
    full = lambda x: np.full(Y.shape, float(x))
    rampc = lambda t, cols: ramp(np.clip(t, 0, 1), cols)     # (past 1 a ramp runs on beyond its light colour: white patches)
    if debug:
        for k, m in I.items():
            ys, xs = np.where(m & M.covered)
            print(f"{k:8s} px={len(xs):7d} x {xs.min() // K}-{xs.max() // K} y {ys.min() // K}-{ys.max() // K}")

    def mix(m, col, k=1.0):
        k = np.broadcast_to(np.asarray(k, float), m.shape)[..., None]
        out[m] = (out * (1 - k) + col * k)[m]

    calm = lambda area, ref=None, k=0.6: 0.5 + (tone(L, area if ref is None else ref) - 0.5) * k
    # painted light for the new cloth: from above, the sides and the islands' edges a little darker
    form = ndimage.gaussian_filter(0.5 + 0.28 * nz - 0.10 * np.abs(ny) - 0.14 * (1 - sstep(M.edge, 0, 6 * K)) * M.covered, 1.2 * K)
    theta = np.arctan2(Ys, X)                                    # round the body's axis
    arc = np.arctan2(Y, X) * 0.2                                 # the same on the mirrored coat, in body units (radius ~0.2)
    # the arm: S along it from the shoulder, th round it (0 = its upper side); the coat's sleeve and the arm under it
    Pm = np.stack([X, Y, Z], -1)
    pts = Pm[I["sleeve"] & M.covered]
    ax = np.linalg.svd(pts - pts.mean(0), full_matrices=False)[2][0]
    ax *= np.sign(ax[1])
    S = (Pm - pts.mean(0)) @ ax
    S = S - S[I["sleeve"] & M.covered].min()
    up = np.array([0, 0, 1.0]) - ax[2] * ax
    up /= np.linalg.norm(up)
    Nm = np.stack([nx, ny * np.sign(Ys + 1e-9), nz], -1)
    th = np.arctan2(ndimage.gaussian_filter(Nm @ np.cross(ax, up), K), ndimage.gaussian_filter(Nm @ up, K))
    s_at = lambda y: float(np.median(S[I["sleeve"] & M.covered & (np.abs(Y - y) < 0.008)]))
    s_el = s_at(0.33)
    if debug:
        print("arm axis", ax.round(3), "sleeve length", round(float(S[I["sleeve"] & M.covered].max()), 3), "elbow s", round(s_el, 3))

    # ----- the robe: black, its folds; green only inside (the lining, the sleeve's inside) and on the turned-out lapel
    # (user 2026-11-12, with the front edge circled: "some green part of the robe shouldn't be outside the robe")
    drape = folds(arc, Z, 0.050, 11) * (0.45 + 0.55 * sstep(1.05 - Z, 0.0, 0.5)) + 0.35 * folds(arc, Z, 0.021, 12, long=9)
    elbow = np.exp(-((S - s_el) / 0.05) ** 2) + 0.6 * np.exp(-(S / 0.05) ** 2)
    sleeve = folds(S + 0.9 * th * 0.045, th * 0.045, 0.026, 21, long=1.1) * (0.06 + 0.9 * elbow) + 0.6 * folds(th * 0.045, S, 0.032, 22, long=6)
    bias = folds(0.6 * Z - 0.8 * Y, 0.8 * Z + 0.6 * Y, 0.034, 31, long=4)      # across the chest, from the shoulder
    wr = {"coat": drape, "lining": drape, "sleeve": sleeve, "cuffIn": sleeve, "chest": 0.7 * bias, "lapel": 0.45 * bias}
    for k in ("chest", "sleeve", "coat"):
        mix(I[k], rampc(0.44 + 0.30 * (calm(I[k], k=0.8) - 0.5) + 0.45 * (form - 0.5) + 0.27 * wr[k], ROBE))
    for k in ("lining", "cuffIn", "lapel"):
        mix(I[k], rampc(0.46 + 0.35 * (calm(I[k], k=0.8) - 0.5) + 0.5 * (form - 0.5) + 0.22 * wr[k], GREEN))
    mix(I["coat"], rampc(full(0.92), ROBE), ins(np.abs(M.edge - 2.2 * K) - 0.9 * K, 0.5) * M.covered * 0.35)   # a stitched edge
    # (the coat's chest only: its black came through the lapel in patches, seen from below. Under = the lapel's nearest
    # point lies straight out along the normal; a point beside the lapel's edge is not under it: by plain distance
    # the green grew a ragged fringe past the edge. Smoothed on the sheet, then cut clean)
    lap = cKDTree(Pm[I["lapel"] & M.covered])
    under_lapel = np.zeros(Y.shape)
    Ch = I["chest"]
    dist, j = lap.query(Pm[Ch])
    out_n = ((lap.data[j] - Pm[Ch]) * Nm[Ch]).sum(-1)
    side = np.sqrt(np.maximum(dist ** 2 - out_n ** 2, 0))
    under_lapel[Ch] = (side < 0.0025) & (dist < 0.02) & (out_n > -0.004)
    under_lapel = sstep(ndimage.gaussian_filter(under_lapel, 2.5 * K), 0.5, 0.75)

    # ----- the sweater on the torso, the shirt, its collar and the tie in the V
    F, B = I["torsoF"], I["torsoB"]
    crease = folds(Z + 0.18 * Y, Ys, 0.021, 41, long=3.5) * (0.25 + 0.75 * sstep(1.17 - Z, 0.0, 0.09)) + 0.3 * folds(Ys, Z, 0.03, 42)
    knit = 0.5 + 0.9 * (form - 0.5) + 0.15 * crease + 0.035 * np.sin(Ys * 2 * np.pi / 0.0036)
    for k in ("torsoF", "torsoB", "cap24"):
        mix(I[k], rampc(knit, GREY))
    d_v = (Z - (V_Z + V_K * Y)) / np.hypot(1, V_K)              # > 0 inside the V
    inV = ins(-d_v)
    shirt = 0.56 + 0.8 * (form - 0.5) + 0.10 * folds(Ys, Z, 0.016, 51)
    mix(F, rampc(shirt, WHITE), inV)
    # the tie (user: "it should start from the collar and go inside the grey sweater"): painted on the shirt, from its
    # knot under the collar down into the V's point; the outfit's own tie (a loose one, hanging in front, its knot
    # 6 cm under the collar) is not drawn
    for k in ("tie", "tieEdge"):
        alpha[I[k]] = 0
    KN0, KN1 = 1.299, 1.333                                      # the knot: its foot, its top
    blade = np.maximum(Y - (0.0105 + 0.085 * (KN0 + 0.004 - Z)), Z - (KN0 + 0.004))
    knot = np.maximum(Y - (0.0092 + 0.13 * (Z - KN0)), np.maximum(Z - KN1, KN0 - Z))
    tie = np.minimum(blade, knot)
    mix(F, hexv("#7d7c8c"), ins(tie - 0.0045, 0.0035) * inV * 0.55)                 # its shadow on the shirt
    tsh = 0.50 + 0.9 * (form - 0.5) + 0.10 * folds(Ys, Z, 0.012, 52)
    u1, u2 = ((Z + 0.9 * Ys) / 0.026) % 1.0, ((Z - 0.9 * Ys) / 0.016) % 1.0
    for d, u, per in ((blade, u1, 0.026), (knot, u2, 0.016)):
        mix(F, hexv(INK), ins(d - 0.0011) * inV * 0.85)
        mix(F, rampc(tsh, GREEN), ins(d) * inV)
        mix(F, hexv(SILVER), ins((np.abs(u - 0.5) - 0.15) * per) * ins(d) * inV * 0.95)
        mix(F, hexv("#0a2c1a"), ins((np.abs(np.abs(u - 0.5) - 0.23) - 0.03) * per) * ins(d) * inV * 0.9)
    mix(F, hexv(INK), ins(np.abs(Z - KN0) - 0.0009) * ins(Y - 0.0098) * inV * 0.75)     # under the knot
    mix(F, rampc(tsh - 0.25, GREEN), ins(np.hypot(Y, (Z - (KN0 - 0.006)) * 0.6) - 0.003) * inV * 0.6)   # the dimple
    # the collar's leaves over the knot's shoulders: white, a clean line along their edges, a soft shade under them
    leaf = np.maximum((1.338 - 1.5 * Y) - Z, 0.0088 - Y) / 1.8          # < 0 on a leaf
    mix(F, hexv("#8f8e9e"), ins(leaf - 0.004, 0.004) * ins(-leaf) * inV * 0.45)
    mix(F, rampc(form + 0.16, WHITE), ins(leaf) * inV)
    mix(F, hexv("#77768a"), ins(np.abs(leaf) - 0.0009) * inV)
    for lo, hi, col in ((-0.0150, 0.0, rampc(knit + 0.10, GREY)), (-0.0105, -0.0045, rampc(form + 0.05, GREEN)),
                        (-0.0160, -0.0146, hexv("#3c3e44")), (-0.0008, 0.0008, hexv("#3c3e44"))):
        mix(F, col, ins(np.abs(d_v - (lo + hi) / 2) - (hi - lo) / 2))
    mix(B, rampc(knit + 0.10, GREY), ins(1.325 - Z))                    # the back of the neck: the ribbed band
    mix(B, rampc(form + 0.05, GREEN), ins(np.abs(Z - 1.335) - 0.003))
    # under the robe the body is the robe's black: at the shoulder it pokes through the coat (a grey speck otherwise)
    mix(F | B, rampc(full(0.45), ROBE), ins(0.085 - Y) * ins(1.22 - Z))
    mix(I["chest"], rampc(0.46 + 0.5 * (form - 0.5), GREEN), under_lapel)
    # the house crest on the sweater's left chest (the coat's two halves share their texels, so not on the robe): a
    # green shield, a silver rim, a silver serpent's S
    cy, cz = Ys - CREST[0], Z - CREST[1]
    shield = np.maximum(np.abs(cy) - 0.0165, np.maximum(cz - 0.019, -cz - 0.024 + 1.1 * np.maximum(np.abs(cy) - 0.004, 0)))
    front = sstep(nx, 0.2, 0.5)
    mix(F, hexv(INK), ins(shield - 0.0022) * front)
    mix(F, hexv(SILVER), ins(shield - 0.0010) * front)
    mix(F, rampc(form, GREEN), ins(shield + 0.0022) * front)
    snake = np.abs(cy - 0.0062 * np.sin(cz / 0.0105 * np.pi)) - 0.0021
    mix(F, hexv(SILVER), ins(np.maximum(snake, np.abs(cz + 0.001) - 0.0125)) * front)

    # ----- the shirt's long sleeves, longer than the robe's (user: "should be white, don't forget slight cloth
    # wrinkles too"): white from under the robe's sleeve to the wrist, soft rings of folds, a plain cuff
    A, Hd = I["arm"], I["hand1"] | I["hand2"]
    CUFF0, CUFF1 = 0.578, 0.622
    rnd = np.arctan2(nx, nz) * 0.03                                   # round the forearm
    rings = folds(Y + 0.12 * rnd, rnd, 0.015, 61, long=2.0) * (0.55 + 0.45 * sstep(Y, 0.50, 0.58)) + 0.4 * folds(rnd, Y, 0.02, 62, long=4)
    mix(A, rampc(full(0.45), ROBE))
    mix(A, rampc(0.58 + 0.7 * (form - 0.5) + 0.22 * rings, WHITE), ins(0.44 - Y))
    for area in (A, Hd):
        mix(area, rampc(0.66 + 0.7 * (form - 0.5) + 0.06 * rings, WHITE), ins(CUFF0 - Y) * ins(Y - CUFF1))
        for y0, k in ((CUFF0, 1.0), (CUFF0 + 0.0045, 0.45), (CUFF1 - 0.004, 0.45)):
            mix(area, hexv("#7f7e92"), ins(np.abs(Y - y0) - 0.0008) * ins(Y - CUFF1) * k)
        mix(area, hexv("#6f6e80"), ins(np.abs(Y - CUFF1) - 0.0011))

    # ----- the skirt island: the sweater's hem over its top (a green stripe, a ribbed band), then grey pleats
    Sk = I["skirt"]
    N_PLEAT = 22
    q = theta * N_PLEAT / (2 * np.pi) + 0.10 * (vnoise(Z / 0.06, theta * 3, 71) - 0.5) * sstep(0.95 - Z, 0, 0.3)   # they wander to the hem
    p = q % 1.0
    each = _hash(np.floor(q).astype(np.int64) % N_PLEAT, np.zeros(Y.shape, np.int64), 72)                          # no two pleats alike
    fold = np.minimum(p, 1 - p) * (2 * np.pi * 0.13 / N_PLEAT)        # body units from the fold line (radius ~0.13)
    cloth = 0.22 * folds(theta * 0.13, Z, 0.03, 73, long=7) * sstep(0.9 - Z, 0, 0.25)
    mix(Sk, rampc(0.26 + 0.36 * p + 0.10 * (each - 0.5) + 0.25 * (form - 0.5) + cloth, SKIRT))
    mix(Sk, rampc(full(0.95), SKIRT), ins((np.abs(p - 0.055) - 0.02) * 0.037) * 0.45)      # the fold's lit edge
    mix(Sk, hexv("#111215"), ins(fold - 0.0015) * 0.9)
    mix(Sk, rampc(full(0.2), SKIRT), ins(Z - 0.612) * 0.7)             # the hem's shade
    HEM, RIB = 0.985, 0.950
    mix(Sk, hexv("#141518"), ins(Z - RIB) * ins(RIB - 0.014 - Z, 0.007) * 0.45)          # the band's shade on the pleats
    mix(Sk, rampc(knit, GREY), ins(RIB - Z))
    rib = 0.5 + 0.5 * np.sin(theta * 64)
    mix(Sk, rampc(knit - 0.18 + 0.24 * rib, GREY), ins(RIB - Z) * ins(Z - (HEM - 0.006)))
    mix(Sk, rampc(form + 0.05, GREEN), ins(np.abs(Z - HEM) - 0.0055))
    mix(Sk, hexv("#3c3e44"), ins(np.abs(Z - RIB) - 0.0014))
    mix(Sk, hexv("#3c3e44"), ins(np.abs(Z - (HEM - 0.0062)) - 0.0008) * 0.8)
    for k in ("cap19", "hem26"):
        mix(I[k], rampc(full(0.25), SKIRT))
    for k in ("buckle", "loop1", "loop2"):                             # the belt's buckle and loops: not drawn
        alpha[I[k]] = 0
    alpha[538 * K:610 * K, 712 * K:812 * K] = 0                       # (its inner piece is an island of its own, 39 px)
    # two specks: a shoulder patch whose triangles all read one texel (sheet 411,408), a bit of the lapel (820,207)
    mix(M.lab == M.lab[408 * K + K // 2, 411 * K + K // 2], rampc(full(0.45), ROBE))
    mix(M.lab == M.lab[207 * K + K // 2, 821 * K + K // 2], rampc(full(0.5), GREEN))
    mix(F | B, rampc(full(0.3), SKIRT), ins(Z - 0.93))                  # the hips under the skirt

    # ----- sheer black tights (the skin shows through where the leg faces out and over the knee), loafers
    G = I["leg"]
    knee = np.exp(-((Z - 0.43) / 0.055) ** 2)
    sheer = (0.40 + 0.26 * np.abs(nx) ** 1.5 + 0.20 * knee * sstep(nx, 0.0, 0.7) - 0.12 * knee * sstep(-nx, 0.2, 0.8)
             - 0.22 * sstep(Z, 0.56, 0.63) + 0.05 * (vnoise(Z / 0.03, theta * 2, 81) - 0.5))
    sheer = ndimage.gaussian_filter(sheer, K)
    mix(G, rampc(sheer, TIGHT))
    Sh = I["shoe"]
    skin_k = sstep(v, 0.72, 0.85) * (hd(h, 22) < 22) * (s < 0.45)
    gloss = 0.26 * sstep(ndimage.gaussian_filter(nz, 3 * K), 0.5, 0.95) * sstep(M.edge, 2 * K, 9 * K)
    mix(Sh, rampc(0.14 + 0.5 * tone(ndimage.gaussian_filter(ndimage.median_filter(L, 9 * K), 2 * K), Sh & (skin_k < 0.3)) + gloss, SHOE))
    mix(Sh, rampc(sheer, TIGHT), ndimage.gaussian_filter(skin_k, 0.6 * K))
    for k in ("sole", "heel"):
        mix(I[k], rampc(0.5 * tone(L, I[k]), SHOE))

    # ----- the neck: no choker, the shirt's collar stand at its foot
    Nk = I["neck"]
    dark = sstep(-v, -0.8, -0.6)
    mix(Nk, rampc(0.52 - 0.22 * sstep(Z, 1.372, 1.402), SKIN))      # one even skin (the choker's band, repainted from its own
    # dark tone, left a darker patch: user "the darker part is making uneven skin around the collar / neck"), a soft shade up under the chin
    mix(Nk, rampc(form + 0.12, WHITE), ins(Z - 1.362))
    mix(Nk, hexv("#8d8c9a"), ins(np.abs(Z - 1.362) - 0.0012))

    # ----- the hands: no gloves, one skin all over (the cuff above reaches the wrist), the three fingers of the block
    # drawn apart, and green nails on all ten (user 2026-11-12: "check against the actual 3D models, I want all 10
    # fingernails painted green to be visible and looks good"). The hand is a thumb, an index and one block for the
    # other three (bones Thumb1-2, Index1-3, Middle1-3); both hands share their texels, so five nails make ten. The
    # outer island (hand1) wraps the back and the sides of each finger, the palm's (hand2) its underside: a nail sits
    # on the last joint, on the side the outer island's mean normal faces.
    HB = I["hand1"]
    mix(Hd, rampc(0.54 + 0.6 * (form - 0.5), SKIN), ins(CUFF1 - Y))
    bn = lambda *names: np.isin(M.bone, [i for i, b in enumerate(M.bones) if b[:-2] in names])

    def finger(whole, prev, last, n, nail_len, width):
        Wm = Hd & bn(*whole)
        cv = Wm & M.covered
        a = Pm[cv & bn(last)].mean(0) - Pm[cv & bn(prev)].mean(0)
        a /= np.linalg.norm(a)
        dv = Nm[HB & cv & bn(prev, last)].mean(0)
        dv -= (dv @ a) * a
        dv /= np.linalg.norm(dv)
        s = Pm @ a
        s = s - s[cv & bn(last)].max()                           # 0 at the tip, falling toward the wrist
        w = Pm @ np.cross(a, dv)
        cen = -0.002 - 0.004 * np.arange(30)                     # the finger's middle line and width along it
        lo, hi = np.full(30, np.nan), np.full(30, np.nan)
        for i in range(30):
            m = cv & (np.abs(s - cen[i]) < 0.003)
            if m.sum() > 20:
                lo[i], hi[i] = np.percentile(w[m], [2, 98])
        ok = ~np.isnan(lo)
        lo, hi = (np.polyval(np.polyfit(cen[ok], x[ok], 1), cen) for x in (lo, hi))      # straight edges (smoothed bins wobbled)
        mid = np.interp(-s, -cen, (lo + hi) / 2)
        Ws = np.interp(-s, -cen, hi - lo)
        lat = w - mid
        back = sstep(Nm @ dv, 0.0, 0.3)
        base = s[cv & bn(whole[0])].min() + 0.026                # just past the knuckles
        for i in range(1, n):                                     # the block's fingers, drawn apart
            line = np.abs(lat - (i / n - 0.5) * Ws)
            mix(Wm, hexv("#c08a79"), ins(line - 0.0008) * ins(base - s) * 0.7)
        mix(Wm, hexv("#f2aca6"), sstep(s, -0.022, -0.003) * 0.32)                     # the fingertips, a little pink
        hl = nail_len / 2
        sc = -0.0040 - hl
        Wc = float(np.interp(-sc, -cen, hi - lo))
        if debug:
            print(f"finger {last:8s} axis {a.round(2)} dorsal {dv.round(2)} width at the nail {Wc:.4f} length {-s[cv].min():.3f}")
        for i in range(n):
            hw = width * Wc / n
            r = min(hw, hl) * 0.9
            qx, qy = np.abs(lat - ((i + 0.5) / n - 0.5) * Wc) - hw + r, np.abs(s - sc) - hl + r
            dn = np.hypot(np.maximum(qx, 0), np.maximum(qy, 0)) + np.minimum(np.maximum(qx, qy), 0) - r
            mix(Wm, hexv("#0a3219"), ins(dn - 0.0008) * back * 0.8)
            mix(Wm, rampc(0.5 + 0.6 * (form - 0.5), NAIL), ins(dn) * back)
            gx = lat - ((i + 0.5) / n - 0.5) * Wc + hw * 0.32                             # a streak of gloss down one side
            mix(Wm, hexv("#c8f4d8"), ins((np.hypot(gx / (hw * 0.17), (s - sc - hl * 0.15) / (hl * 0.5)) - 1) * hw * 0.17) * ins(dn + 0.0008) * back * 0.7)

    # (larger than life: at 12 mm, a real nail on this 17 cm hand, they were specks at the ends of the low-poly fingers)
    finger(("Index1", "Index2", "Index3"), "Index2", "Index3", 1, 0.0215, 0.43)
    finger(("Middle1", "Middle2", "Middle3"), "Middle2", "Middle3", 3, 0.0195, 0.40)
    finger(("Thumb1", "Thumb2"), "Thumb1", "Thumb2", 1, 0.0185, 0.42)

    # ----- hair: platinum. The original's painted locks stay (their shadows cut clean, their glints), over them the
    # clumps' soft relief, single strands as thin tapering lines, a band of shine broken by the strands (user
    # 2026-11-12: "improve the quality of Bat's bangs and john [จอน: the side locks] details": the first hair was the
    # locks washed pale under grainy streaks)
    keys = ("pony", "hairB", "side1", "side2", "fringe")
    hair = np.logical_or.reduce([I[k] for k in keys])
    H = strands(L, Z, hair, K)
    for k in keys:
        Hr = I[k]
        tn = tone(L, Hr, lo=1)
        t = 0.54 + 0.42 * (tn - 0.5) - 0.16 * (1 - sstep(tn, 0.20, 0.45))          # the painted locks, their shadows
        t = t + 0.09 * H["relief"] + 0.05 * (H["fine"] - 0.5)
        if k in ("side1", "side2"):
            t = t - 0.13 * sstep(Z, 1.53, 1.575)                                   # under the fringe
        z0 = {"pony": 1.36, "fringe": 1.625}.get(k, 1.605)             # the shine: a band round the head, broken by the strands
        band = np.exp(-((Z - z0 - 0.020 * (H["coarse"] - 0.5) - 0.006 * (H["fine"] - 0.5)) / 0.014) ** 2)
        t = t + 0.20 * band * (0.3 + 0.7 * sstep(H["fine"], 0.25, 0.7))
        t = t + 0.15 * sstep(tn, 0.80, 0.97)                                       # the original's glints on the locks' edges
        t = t - 0.24 * sstep(H["dark"], 0.18, 0.62) + 0.20 * sstep(H["light"], 0.2, 0.65)
        mix(Hr, rampc(np.maximum(t, 0.06), BLOND))
    Fc = I["face"]
    shade = 1 - sstep(v, 0.70, 0.93)
    mix(Fc, rampc(0.10 + 0.22 * tone(L, Fc & (v < 0.8)), SKIN), shade * 0.85)                # a shadow on skin, not hair
    mix(Fc, rampc(0.15 + 0.5 * tone(L, Fc & (v < 0.8)), BLOND), shade * 0.9 * (1 - sstep(M.edge, 1.5 * K, 7 * K)) * sstep(Z, 1.49, 1.52))   # the rim under the hair: forehead and temples only
    mix(Fc & ~M.covered, rampc(full(0.3), BLOND), shade * sstep(Z, 1.49, 1.52))
    # a very faint blush under the eyes (user); the face preset's eyes and mouth are drawn over the sheet, the cheeks are the skin's
    blush = np.exp(-((Y - 0.056) / 0.021) ** 2 - ((Z - 1.452) / 0.0115) ** 2)
    mix(Fc, hexv("#f08a8c"), blush * 0.20 * (1 - shade))

    # ----- the Bat's own: ears, wings and tail in the robe's black, the wings' membrane its green
    grain = 0.12 * (vnoise(X / 0.02 + Z / 0.02 * 0.7, Ys / 0.02 - Z / 0.02 * 0.4, 90) - 0.5)
    mix(I["earB"], rampc(tone(L, I["earB"]), ROBE))
    mix(I["earF"], rampc(0.42 * tone(L, I["earF"]), GREEN))
    mix(I["earF"], rampc(tone(L, I["earF"]), ROBE), 1 - sstep(M.edge, 3 * K, 7 * K))
    mix(I["wingB"], rampc(tone(L, I["wingB"]) + grain, ROBE))
    W = I["wingF"]
    bone_k = ndimage.gaussian_filter(1 - sstep(s, 0.42, 0.6), 0.5 * K)
    mix(W, rampc(0.72 * tone(L, W & (bone_k < 0.3)) + grain, GREEN))
    mix(W, rampc(0.25 + 0.7 * tone(L, W & (bone_k > 0.7)), ROBE), bone_k)
    mix(I["tail"], rampc(tone(L, I["tail"]), ROBE))
    return np.dstack([np.clip(out, 0, 255), alpha]).astype(np.uint8)


def paint_main(debug):
    d = OUT / "robe"
    d.mkdir(parents=True, exist_ok=True)
    skin = robe(debug)
    orig = Image.open(DATA / CLS / "tex" / f"{OUTFIT}1.webp").convert("RGBA")
    assert skin.shape[:2] == (orig.height * HI, orig.width * HI), "a skin is the original's size or 2x / 4x / 8x of it (the page's skinDims)"
    Image.fromarray(skin, "RGBA").save(d / f"{OUTFIT}.png", optimize=True)
    print(f"{skin.shape[1]}x{skin.shape[0]} px, {(d / f'{OUTFIT}.png').stat().st_size / 1e6:.1f} MB")
    views = ((0, "front"), (90, "left"), (180, "back"), (270, "right"), (25, "q"))
    if not (OUT / "shots" / "orig_front.png").exists():
        asyncio.run(shots(CLS, OUTFIT, [("orig", {}, {})], OUT, yaws=views[:1], size=1000, dpr=2))
    skins = {f"{CLS}|outfits|{OUTFIT}|": d / f"{OUTFIT}.png"}
    asyncio.run(shots(CLS, OUTFIT, [("robe", skins, {})], OUT, yaws=views, size=1000, dpr=2, face=FACE))
    panels = [Image.open(OUT / "shots" / "orig_front.png"), Image.open(OUT / "shots" / "robe_front.png")]
    for f in sorted(OUT.glob("reference*.png")):                        # the user's pictures: theirs, not in git
        ref = Image.open(f).convert("RGB")
        panels.append(ref.resize((round(ref.width * 1000 / ref.height), 1000), Image.LANCZOS))
    sheet = Image.new("RGB", (sum(p.width for p in panels), 1000), (230, 225, 216))
    x = 0
    for p in panels:
        sheet.paste(p, (x, 0)); x += p.width
    sheet.save(OUT / "robe_compare.png")
    imgs = "".join(f"<img src=shots/robe_{s}.png>" for _, s in views[:4])
    (OUT / "robe.html").write_text(f"""<!doctype html><meta charset=utf-8><title>Bat: robe</title>
<style>body{{font-family:system-ui,sans-serif;background:#f4f1ea;margin:16px}}figure{{margin:0 0 16px;background:#fff;border-radius:10px;padding:8px}}
figure img{{width:24%;min-width:200px}}.cmp img{{width:100%;min-width:0}}figcaption{{font-weight:600;margin:4px}}</style>
<h1>ค้างคาว · ชุด Student เป็นชุดคลุมนักเรียนตามภาพอ้างอิง</h1>
<figure class=cmp><img src=robe_compare.png><figcaption>ของเดิม · ของใหม่บนโมเดล 3D (หน้าแบบที่ {FACE}) · ภาพอ้างอิง</figcaption></figure>
<figure>{imgs}<figcaption>ของใหม่ · หน้า ซ้าย หลัง ขวา</figcaption></figure>
<figure><img src=robe/{OUTFIT}.png style="width:48%"><figcaption>ลายชุด ({skin.shape[1]} × {skin.shape[0]})</figcaption></figure>""", encoding="utf-8")
    print("preview:", (OUT / "robe.html").as_uri())


if __name__ == "__main__":
    if "--islands" in sys.argv:
        islands()
    else:
        paint_main("--debug" in sys.argv)
