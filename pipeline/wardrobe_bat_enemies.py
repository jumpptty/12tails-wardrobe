r"""Two Bat skins after two in-game enemies built on the Bat's body (2026-11-13; user: "3D model reference this time ... find
the best Bat Equipment set to copy the skins from in-game enemy Lady Noir and Bat Cult, 2 skins ... you may use the whole
set or just some part"; bases limited to royal / legend / summer / hallow / butterfly). The references: the enemies' own
meshes and textures (wardrobe_enemy_ref.py -> plans/reskins/bat/ref/).
  eyes  the helmeted one in a dark purple armoured dress with eye emblems, striped sleeves and stockings, pink hair,
        eye-marked wings            -> outfit **royal** (a long dress-coat, wide sleeves, boots), head butterflyHood, face 11
  rose  the white-haired one in a black top, a long dark flowered skirt on one hip, lace and striped stockings, red
        wings, a rose in her hair   -> outfit **summer** (a bikini top and a hip cloth on the bare body), no head piece (her rose is painted on the
        hair; a first pass wore hallowCrown for it), face 21
Painted part by part (user: "consider repainting yourself while borrowing textures from the existing ones"; a whole-model
projection was dropped). Three ways, each part named here:
  same   the part has the enemy's own layout at the same sheet place (wardrobe_borrow.same_uv: face, ears, hands, tail,
         the second one's hair and wings): the enemy's paint, texel for texel
  own    the outfit's own paint in the enemy's colours (its shapes differ: the coat, the hair of another cut, the face
         under the face preset)
  borrow the part takes the paint of the enemy's parts named beside it, nearest on the body (skin-tight parts on the
         same body: torso, arms, legs, feet; flat wings); the distances are printed
Nothing is transparent (the game ignores alpha: asserted).
  uv run --no-project --with pillow --with numpy --with scipy --with playwright python -I pipeline/wardrobe_bat_enemies.py eyes|rose|both|arms|backs|belts [--noshots]
Outputs plans/reskins/bat/<eyes|rose>/: look/<outfit>.png (1024 px), shots/ (eight sides), sheet.png, compare.png."""
import asyncio, sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wardrobe_repaint import ROOT, DATA, cached_maps, hsv, hd, sstep, tone, shots
from scipy.spatial import cKDTree
from wardrobe_borrow import ref_maps, borrow, isl, load_obj, fine, bilinear

CLS, K = "bat", 2
LASH_FROM, LASH_W = 0.26, 1.45                                  # the first upper lash's place along the lid (0 = the inner corner), the lashes' thickness
LASHES, LASH_LEN, SHADOW = 7, 2.2, 0.42                         # eye make-up (eye_makeup): upper lashes per eye, their length (1 = up to 27 % of the eye's width at the outer corner), the plum shadow's strength
SIGIL_HIP, TAB_UPPER = False, False
CUTS_DEBUG = "--cuts" in sys.argv                               # strokes(): also write _cache/cuts_<name>.png, the strokes' cut ends marked
SIGIL, SIGIL_Z, SIGIL_H, SIGIL_AT = (350, 144, 420, 254), 0.80, 0.25, 0.135      # her panel's eye pattern: its box on her sheet (x0, y0, x1, y1); on the coat: its middle's height (its foot stays over the belt, z 0.64), its height, its middle's distance from the body's middle on the front piece (|y|)
COAT_BACK, PANEL_WIDE, PANEL_TO = "panel", 0.68, 0.645         # the coat's back: panel (her own back panel, copied whole: that wide against hers, its point at that height: the belt's top) | "ref" (her skirt read at its own place: a stray strip) | plain | eye | wing | spine | hem (coat_back)
BELT = "contour"                                                # royal's own belt (island 33, round the coat's back): none | tooled | braid | studs | scales | weave | eyes | chain | stripes | contour | lattice (belt)
MID_LINE, MID_SIDE = 0.15, 0.12                                 # the belly's centre line and its sides' shade
MIDRIFF = 1.0                                                   # how much of the summer belly's light and shade (its own is ~5 %: 0.6 did not show; faint: user)
FOLD = (1.172, 14.0)                                            # the fold under each breast: its lowest height (at |y| 4.5 cm), how fast it rises to the middle
TAB_TOP, HER_LOW, PANEL_RIM = 1.0, 0.56, 2.6                    # the front piece's pattern starts under here; her tabard is read down to HER_LOW; its border, texels
DISC = (0.985, 0.040, 0.029)                                    # the waist sigil: its middle's height, half-width, half-height
NECK, NECK_W, NECK_H, NECK_P = 1.035, 0.050, 0.080, 3.5         # the neckline, a U (user: "U instead of V"; a V, and a shallow one, before): its bottom's height (just over the sigil), then up NECK_H by |y| = NECK_W, as the NECK_P-th power: a round bottom, upright sides
neck_z = lambda y: NECK + NECK_H * (y / NECK_W) ** NECK_P
neck_n = lambda y: np.hypot(1, NECK_H * NECK_P / NECK_W * (y / NECK_W) ** (NECK_P - 1))      # to measure across the neckline, not in height
LINE2 = 8.2                                                     # the border's second, thinner line: sheet texels in from the coat's edge
LINING = 3.9                                                    # the coat's silver lining, texels of the 512 px sheet
COAT_SIDE = 0.03                                                # the coat's sides take her side panels' paint within this far, seen from the side
SLEEVE_FOLDS, LEG_CREASES = 1.0, 1.0                            # the sleeves' folds and the stockings' creases (cloth_shade): 0 = none
HAIR_TEX, HAIR_PIC_W = 0.0, 0.28                                # the user's hair picture over the hair (hair_picture): its strength (0 = none), its width on the hair (body units)
HAIR_K, BAND_ROUND = 1.25, 95                                   # the hair's contrast over royal's own strand painting; the helmet band runs this far round the head from the front's middle (degrees)
BAND_TOP, BAND_DROP = 1.635, 0.012                              # the first one's helmet band: its top on her head; how much lower the Bat wears it
STRAP_TO = 0.90                                                 # the straps run down to here: under the hip cloth's top (0.98 at her left hip, lower in front)
HIP_INSET, HAIR_GAMMA = 3, 0.40                                # the skirt's edge left unread (sheet texels); the hair's lift (1 = her texture as it is)
ROSE_AT, ROSE_R = np.array([0.080, 0.105, 1.612]), 0.050        # her rose on the Bat's head (the enemy's piece: 0.042, 0.109, 1.622), its radius
BASE = ROOT / "plans" / "reskins" / "bat"
LUM = np.array([0.299, 0.587, 0.114])
hexv = lambda c: np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], float)


def palette(rgb, mask, q=(12, 55, 94), w=4):
    """Three colours of a part of the reference: its texels sorted by luminance, the mean round each percentile."""
    c = rgb[mask]
    o = np.argsort(c @ LUM)
    n = len(o)
    return [c[o[int(n * max(p - w, 0) / 100): int(n * min(p + w, 100) / 100) + 1]].mean(0) for p in q]


def ramp3(t, cols):
    """t 0..1 -> shadow, base (0.5), light; cols: three colours (arrays)."""
    c0, c1, c2 = cols
    t = np.clip(t, 0, 1)[..., None]
    return np.where(t < 0.5, c0 + (c1 - c0) * t * 2, c1 + (c2 - c1) * (t * 2 - 1))


class Job:
    def __init__(self, name, outfit, ref, sub=None):
        self.name, self.outfit, self.out = name, outfit, BASE / name
        im = Image.open(DATA / CLS / "tex" / f"{outfit}1.webp").convert("RGB")
        self.src = np.asarray(im.resize((im.width * K, im.height * K), Image.LANCZOS)).astype(float)
        self.M = cached_maps(CLS, outfit, K, self.out / "_cache")
        self.obj, self.sub = BASE / "ref" / f"{ref}_tri.obj", sub
        self.R = ref_maps(self.obj, BASE / "ref" / f"{ref}.png", K, self.out / "_cache", sub, CLS)
        self.L = ndimage.gaussian_filter(self.src @ LUM / 255, 0.8 * K)
        self.o = self.src.copy()
        self.extra = {}                                           # prop skins: skin key -> file
        M = self.M
        self.form = ndimage.gaussian_filter(0.5 + 0.22 * M.nrm[..., 2] + 0.06 * M.nrm[..., 0] - 0.08 * np.abs(M.nrm[..., 1]), 1.2 * K)

    m = lambda self, *seeds: np.logical_or.reduce([isl(self.M, K, x, y) for x, y in seeds])      # the outfit's islands
    r = lambda self, *seeds: np.logical_or.reduce([isl(self.R, K, x, y) for x, y in seeds])      # the reference's

    def same(self, dst):
        self.o[dst] = self.R.rgb[dst]

    def own(self, dst, cols, k=1.0, ref=None, lo=3, hi=99.5):
        """The outfit's own shading (luminance, its median = the base colour), in three colours."""
        self.o[dst] = ramp3(0.5 + (tone(self.L, dst & self.M.covered if ref is None else ref, lo, hi) - 0.5) * k, cols)[dst]

    def take(self, dst, src, name, absy=False, inset=1.5, flip=False, view=0, within=None, shift=(0, 0, 0), axis=0, scale=(1, 1, 1)):
        return borrow(self.o, self.M, dst, self.R, src, absy=absy, inset=inset * K, name=name, flip=flip, view=view, within=within, shift=shift, axis=axis, scale=scale)

    def lay(self, dst, box, name, side=1, reach=0.0035, to_z=None, ends=0.035):
        """A piece of the reference that stands off the body (a strap), painted on the body under it: the outfit
        texels `dst` that lie behind it seen from the front (side 1) or the back (-1) take its colour. box: the piece's
        place on the reference's sheet (x0, y0, x1, y1); several pieces may share it (a strap in front and one behind):
        its triangles are read from the mesh, the ones on that side of the body kept. to_z: the piece is made
        longer downward to that height (the Bat's hip cloth sits lower than the enemy's belt: the strap "ended abruptly",
        user 2026-11-13): its two ends (`ends` tall: the buckles) keep their shape, the band between them stretches."""
        P, T, N, F = load_obj(self.obj, self.sub)
        P = P @ self.R.A.T + self.R.t
        px = np.stack([T[:, 0] * 512, (1 - T[:, 1]) * 512], 1)
        c = px[F].mean(1)
        F = F[(c[:, 0] > box[0]) & (c[:, 0] < box[2]) & (c[:, 1] > box[1]) & (c[:, 1] < box[3])]
        F = F[P[F][:, :, 0].mean(1) * side > 0.02]
        rng = np.random.default_rng(2)
        f, u, v = rng.integers(0, len(F), 60000), rng.random(60000), rng.random(60000)
        flip = u + v > 1
        u[flip], v[flip] = 1 - u[flip], 1 - v[flip]
        w = np.stack([1 - u - v, u, v], 1)[:, :, None]
        pos, uv = (w * P[F[f]]).sum(1), (w * px[F[f]]).sum(1)
        col = self.R.rgb[np.clip((uv[:, 1] * K).astype(int), 0, self.R.rgb.shape[0] - 1), np.clip((uv[:, 0] * K).astype(int), 0, self.R.rgb.shape[1] - 1)]
        dst = dst & (self.M.nrm[..., 0] * side > 0.2)
        q = self.M.pos[dst][:, 1:].copy()
        if to_z is not None:                                      # the body's height -> the piece's own
            z0, z1 = pos[:, 2].min(), pos[:, 2].max()
            q[:, 1] = np.interp(q[:, 1], [to_z - 1, to_z, to_z + ends, z1 - ends, z1, z1 + 1], [z0 - 1, z0, z0 + ends, z1 - ends, z1, z1 + 1])
        d, j = cKDTree(pos[:, 1:]).query(q)
        hit = d < reach
        ys, xs = np.where(dst)
        self.o[ys[hit], xs[hit]] = col[j[hit]]
        print(f"lay    {name:14s} {int(hit.sum()):8d} texels; the piece: y {pos[:, 1].min():.3f}..{pos[:, 1].max():.3f} z {pos[:, 2].min():.3f}..{pos[:, 2].max():.3f}")

    def mix(self, m, col, k):
        k = np.broadcast_to(np.asarray(k, float), m.shape)[..., None]
        self.o[m] = (self.o * (1 - k) + col * k)[m]

    def save(self):
        d = self.out / "look"
        d.mkdir(parents=True, exist_ok=True)
        skin = np.dstack([np.clip(self.o, 0, 255), np.full(self.o.shape[:2], 255.0)]).astype(np.uint8)
        assert (skin[..., 3] == 255).all(), "an outfit skin is opaque: the game ignores alpha (paint a part, never hide it)"
        Image.fromarray(skin, "RGBA").save(d / f"{self.outfit}.png", optimize=True)
        return d / f"{self.outfit}.png"


def face_marks(J, head, eyes=((37, 47), (90, 47)), shadow="#cdb3d6"):
    """A soft lilac shade over each eye (both enemies have it); the face preset draws the eyes themselves."""
    yy, xx = np.mgrid[:J.o.shape[0], :J.o.shape[1]] / K
    for ex, ey in eyes:
        J.mix(head, hexv(shadow), np.exp(-((xx - ex) / 13.0) ** 2 - ((yy - ey + 5.5) / 3.6) ** 2) * 0.55)
    return xx, yy


def limb(M, mask, along):
    """A sleeve's or a stocking's own coordinates: t = the way along it (along = 1: |y|, an arm held out; 2: z, a leg),
    phi = the angle round its middle line (0 = its front, +x; for an arm pi/2 = its top, for a leg pi/2 = its outer
    side), r = its radius there (the limb's middle per 2 cm of t, smoothed)."""
    P = M.pos * [1, 0, 1] + np.abs(M.pos * [0, 1, 0])
    a, b = [i for i in (0, 1, 2) if i != along]
    t = P[..., along]
    k = mask & M.covered
    bins = np.arange(t[k].min(), t[k].max() + 0.02, 0.02)
    i = np.clip(np.digitize(t[k], bins) - 1, 0, len(bins) - 1)
    cen = np.array([P[k][i == j][:, [a, b]].mean(0) if (i == j).sum() > 20 else [np.nan, np.nan] for j in range(len(bins))])
    ok = ~np.isnan(cen[:, 0])
    ca = ndimage.gaussian_filter1d(np.interp(bins, bins[ok], cen[ok, 0]), 1.5)
    cb = ndimage.gaussian_filter1d(np.interp(bins, bins[ok], cen[ok, 1]), 1.5)
    da, db = P[..., a] - np.interp(t, bins + 0.01, ca), P[..., b] - np.interp(t, bins + 0.01, cb)
    return t, np.arctan2(db, da), np.hypot(da, db)


def cloth_shade(J, sleeves, legs):
    """Cloth on the striped sleeves and stockings (user 2026-11-14: "add a bit more texture to the sleeves and
    pantyhose too (don't add more patterns, please add things like texture, shading, or a bit of cloth wrinkles)").
    Light and shade only, multiplied onto the stripes (their colours and places stay): the limb's roundness (lit from
    the front and above, the far side in shade), folds that hang along a wide sleeve, creases round the elbow and the
    cuff, small creases behind the knee and at the ankle, a soft sheen down the front of the stocking, a fine knit
    grain. Drawn on the limb's own coordinates (limb), so nothing is cut at an island's edge."""
    from wardrobe_bat_robe import folds
    M = J.M
    rng = np.random.default_rng(11)
    grain = ndimage.gaussian_filter(rng.normal(0, 1, M.lab.shape), 0.5 * K)
    bump = lambda x, c, w: np.exp(-((x - c) / w) ** 2)
    # --- sleeves
    t, ph, r = limb(M, sleeves, 1)
    rm = float(np.median(r[sleeves & M.covered]))
    lit = 0.5 + 0.5 * np.cos(ph - np.radians(55))                 # from the front and above
    f = 0.80 + 0.36 * lit ** 1.3
    f *= 1 + SLEEVE_FOLDS * 0.17 * folds(ph * rm, t, 0.030, 11, long=5.0) * sstep(t, 0.16, 0.26)          # hanging folds, from under the capelet out
    f *= 1 + SLEEVE_FOLDS * 0.20 * folds(t, ph * rm, 0.013, 13, long=3.5) * np.maximum(bump(t, 0.37, 0.07), 0.8 * bump(t, t[sleeves & M.covered].max() - 0.03, 0.05))
    f *= 1 + 0.045 * grain + 0.025 * np.sin(t / 0.0042 * 2 * np.pi)                                       # knit rows round the arm
    J.o[sleeves] = (J.o * f[..., None])[sleeves]
    # --- stockings
    t, ph, r = limb(M, legs, 2)
    rm = float(np.median(r[legs & M.covered]))
    lit = 0.5 + 0.5 * np.cos(ph - np.radians(25))
    f = 0.78 + 0.38 * lit ** 1.4
    back = np.clip(-np.cos(ph), 0, 1)
    f *= 1 + LEG_CREASES * 0.22 * folds(t, ph * rm, 0.009, 17, long=3.0) * np.maximum(bump(t, 0.47, 0.045) * back, 0.9 * bump(t, 0.20, 0.035))
    f *= 1 + 0.040 * grain + 0.030 * np.sin(ph * 44)                                                      # fine ribs down the leg
    J.o[legs] = (J.o * f[..., None])[legs]
    sheen = 0.10 * bump(ph, np.radians(25), 0.30) * sstep(t, 0.22, 0.30)                                  # the stocking's sheen down its front
    J.mix(legs, np.minimum(J.o * 1.6 + 30, 255), sheen)
    print(f"cloth: sleeves {int((sleeves & M.covered).sum())} texels (radius {rm * 100:.1f} cm), stockings {int((legs & M.covered).sum())}")


def strokes(J, dst, src, key, name, reach=0.006, inset=5, fade=4, depth=None, k=None, key_src=None):
    """Only what the reference DRAWS (lines, leaves, eyes: what differs from its own cloth colour there), laid over the
    outfit's paint on `dst` (user 2026-11-14, of readings that brought cloth, borders and their cut ends along: "it does
    look sharper, true, but some places are not clean either"). Her texels `src` are matched in the key space (key(p):
    (N, 3) body points -> (N, d): a view, a map round the head), read between texels from the sharp sheet (fine), and
    taken only within `reach`, never from her island's rim (`inset` sheet texels: its border and hem stay out), fading
    over the next `fade` texels: a stroke that runs to her border thins out instead of ending in a cut. depth(p): where
    she has several layers at one place of the key space (a dress under a skirt panel, seen from the side), the one
    with the largest depth is read (without it the layers alternate texel by texel: hatching)."""
    R, M = J.R, J.M
    sm = src & R.covered & (R.edge >= inset * K)
    sy, sx = np.where(sm)
    key_src = key_src or key                                     # (her own map when her part's axis is not the outfit's)
    sp, qk = key_src(R.pos[sm]), key(M.pos[dst])
    if depth is not None:                                        # her outermost layer alone: per 4 mm cell of the key space the
        dp = depth(R.pos[sm])                                    # largest depth, texels more than 1.2 cm under it left out (picking
        cell = np.floor(sp / 0.004).astype(int)                  # the deeper of the nearest few flipped from texel to texel at a
        cell -= cell.min(0)                                      # stroke's edge: ragged)
        buf = np.full(cell.max(0) + 1, -9.0)
        np.maximum.at(buf, (cell[:, 0], cell[:, 1]), dp)
        buf = ndimage.maximum_filter(buf, 3)
        top = dp >= buf[cell[:, 0], cell[:, 1]] - 0.012
        sy, sx, sp = sy[top], sx[top], sp[top]
    d, j = cKDTree(sp).query(qk)
    col = fine(R, sy[j], sx[j], qk - sp[j], key_src)
    drawn = sstep(np.abs(col - np.median(R.rgb[sm], 0)).max(-1), 14, 44)
    lim = dict(reach=1 - sstep(d, reach * 0.5, reach), rim=sstep(R.edge[sy[j], sx[j]], inset * K, (inset + fade) * K), mask=np.ones(len(d)) if k is None else k[dst])
    w = (drawn * lim["reach"] * lim["rim"] * lim["mask"])[:, None]
    # the check against cuts: drawn strokes that one of this reading's own limits ends (its weight between 0 and 1 there).
    # A stroke should end where the reference's design ends, not where a limit does: a large count = look at that spot
    cut = {n_: int(((drawn > 0.5) & (v > 0.03) & (v < 0.97)).sum()) for n_, v in lim.items()}
    if CUTS_DEBUG:                                                # a skin that shows them: red = reach, yellow = her island's rim, green = the mask
        dbg = np.clip(J.o, 0, 255).copy()
        for n_, c_ in (("reach", (255, 0, 0)), ("rim", (255, 220, 0)), ("mask", (0, 255, 0))):
            ys_, xs_ = np.where(dst)
            q_ = (drawn > 0.5) & (lim[n_] > 0.03) & (lim[n_] < 0.97)
            dbg[ys_[q_], xs_[q_]] = c_
        Image.fromarray(dbg.astype(np.uint8)).save(J.out / "_cache" / f"cuts_{name.replace(' ', '_').replace(',', '')}.png")
    full = np.zeros(dst.shape)
    full[dst] = w[:, 0]
    lab_, n_ = ndimage.label(full > 0.25)
    small = np.isin(lab_, np.where(ndimage.sum(full > 0.25, lab_, range(1, n_ + 1)) < 30 * K * K)[0] + 1)      # crumbs: under 30 sheet texels
    w = w * (~ndimage.binary_dilation(small, iterations=K))[dst][:, None]
    J.o[dst] = J.o[dst] * (1 - w) + col * w
    print(f"strokes {name:14s} {int((w[:, 0] > 0.5).sum()):7d} of {int(dst.sum())} texels drawn; apart median {np.median(d) * 100:.1f} cm; strokes ended by a limit (texels): {cut}")


def hair_picture(M, pic, width=HAIR_PIC_W, hx=0.02):
    """The user's picture of hair (flowing locks, dark gaps between them, fine lines along them) laid over the hair
    (user 2026-11-14, of locks drawn by formula: "I don't like your hair texture, can you try overlaying my reference
    picture instead?"). Laid on the body, not on the sheet, so it passes from island to island without a seam: across
    the picture = the way round the head (the angle about its upright axis, plus the distance from the axis so a
    lock's face that points round the head is not one stretched column), down the picture = down the hair. The picture
    is `width` wide on the hair (body units); it does not tile, so it repeats mirrored across and cross-faded down. Returns its light and dark as
    0..1 (0 = the dark gaps), its 2nd / 98th percentiles as the ends."""
    im = Image.open(pic).convert("RGB")
    lum = np.asarray(im).astype(float) @ LUM
    lo, hi = np.percentile(lum, [2, 98])
    lum = np.clip((lum - lo) / (hi - lo), 0, 1)
    ph, pw = lum.shape
    X, Y, Z = M.pos[..., 0], M.pos[..., 1], M.pos[..., 2]
    # the angle is counted from the front's middle on the front half and from the back's middle on the back half, so
    # the picture's middle column lies on each (a parting; the two meet at the sides, under the hood)
    ac = np.arctan2(Y, np.abs(X - hx)) * 0.13 + 0.8 * np.hypot(X - hx, Y) * np.sign(Y)
    per = pw / width                                             # picture pixels per body unit
    lum = ndimage.gaussian_filter(lum, max(per * 0.0017 / K * 0.5, 0.3))       # the picture is finer than the sheet: averaged, not picked
    mirror = lambda t, n: (n - 1) - np.abs((t % (2 * (n - 1))) - (n - 1))
    # down the hair the picture repeats by a cross-fade over its last quarter (a mirror there drew diamonds)
    ov = int(ph * 0.25)
    wv = np.linspace(0, 1, ov)[:, None]
    tile = np.vstack([lum[ov:ph - ov], lum[ph - ov:] * (1 - wv) + lum[:ov] * wv])
    # the hair's halves read the same texels, mirrored at the middle: where the picture's strands slant there, they
    # meet as chevrons down the parting. So the column that lies on the middle is the one where they run straightest
    # down (the picture's own strokes: the slope of its light across a 40 px window, least over the picture's height)
    gy_, gx_ = np.gradient(ndimage.gaussian_filter(lum, 2.0))
    slant = np.abs(ndimage.uniform_filter1d((gx_ * gy_).sum(0), 40)) / np.maximum(ndimage.uniform_filter1d((gx_ ** 2).sum(0), 40), 1e-9)
    mid = int(pw * 0.2 + np.argmin(slant[int(pw * 0.2):int(pw * 0.8)]))
    u, v = mirror(mid + ac * per, pw), ((1.70 - Z) * per) % tile.shape[0]
    return ndimage.map_coordinates(tile, [v, u], order=1, mode="grid-wrap")


def eye_makeup(J, head, face):
    """Lashes and eye shadow round the face preset's eyes (user 2026-11-14, with a drawing of an eye with bold tapered
    lashes: "be a professional makeup artist, paint directly on the model to be precise, current bat eyes need a bit
    more cosmetic to looks more stunning, anime eyelashes"). The page draws the preset's eyes over the skin (the face
    block: the sheet's top-left 256 x 256 texels, composeTexture), so the make-up is painted on the skin round them,
    placed from the preset's own picture: per eye its dark upper lid's top edge and its lower edge, column by column.
      lashes  LASHES tapered, curved spikes rooted on the lid's top edge, from the eye's middle to its outer corner:
              longer and leaning further out toward the corner, the tips curling up; three short ones under the outer
              third of the lower lid. The lid's own near-black. Drawn at 6 x and averaged down: clean edges.
      shadow  a smoky plum close over the lid, deepest at the outer corner, under the lilac shade (face_marks)
    Each eye mirrored about the face's middle: the outer corner is the one away from it."""
    from PIL import ImageDraw
    ov = np.asarray(Image.open(DATA / CLS / "faces" / f"{face}.webp").convert("RGBA")).astype(float)
    dark = (ov[..., 3] > 150) & (ov[..., :3] @ LUM < 75)
    solid = ov[..., 3] > 150
    lab, n = ndimage.label(ndimage.binary_dilation(solid, iterations=2))
    boxes = [b for b in ndimage.find_objects(lab) if (b[1].stop - b[1].start) > 18 and b[0].start < 70]      # the two eyes (not the mouth, the brows)
    boxes = sorted(boxes, key=lambda b: -(b[1].stop - b[1].start) * (b[0].stop - b[0].start))[:2]
    mid = float(np.mean([(b[1].start + b[1].stop) / 2 for b in boxes]))
    ink = ov[..., :3][dark].mean(0) * 0.8
    S, N = 6, 128                                                # supersampling; the face's part of the block, sheet texels
    cv = Image.new("L", (N * K * S, N * K * S), 0)
    g = ImageDraw.Draw(cv)
    sh = np.zeros((N * K, N * K))
    yy, xx = np.mgrid[:N * K, :N * K] / K
    def spike(p0, ang, length, width, s, curl=18, via=None):
        d = lambda a: np.array([s * np.sin(np.radians(a)), -np.cos(np.radians(a))])
        p1, p2 = p0 + d(ang + curl) * length * 0.55, p0 + d(ang - curl * 0.4) * length
        if via is not None:                                      # through a given point instead: p2 = via + the direction ang, that far
            p1, p2 = via, via + d(ang) * length
        t = np.linspace(0, 1, 32)[:, None]
        c = (1 - t) ** 2 * p0 + 2 * t * (1 - t) * p1 + t ** 2 * p2
        tan = np.gradient(c, axis=0); nrm = np.stack([-tan[:, 1], tan[:, 0]], 1) / np.maximum(np.linalg.norm(tan, axis=1, keepdims=True), 1e-9)
        w = width / 2 * (1 - t) ** 1.15
        poly = np.vstack([c + nrm * w, (c - nrm * w)[::-1]]) * K * S
        g.polygon([tuple(q) for q in poly], fill=255)
        return c
    for b in boxes:
        ys, xs = b
        # Every lash is rooted IN the eye's own dark line (user 2026-11-14: "make sure each eyelashes root reach the eye
        # edge, don't make it looks float in solitude on the face"): the line = the largest connected dark piece of the
        # preset's eye (not its crease line over the lid, not a stray mark); an upper lash starts 1.6 texels inside its
        # top edge, a lower lash on its lowest texel, and only where the line really is the eye's lower edge there
        dl, dn = ndimage.label(dark[ys, xs])
        line = dl == (1 + int(np.argmax(ndimage.sum(dark[ys, xs], dl, range(1, dn + 1)))))
        cols = [x for x in range(xs.start, xs.stop) if line[:, x - xs.start].any()]
        top = {x: ys.start + int(np.argmax(line[:, x - xs.start])) for x in cols}
        low = {x: ys.start + int(np.max(np.where(line[:, x - xs.start])[0])) for x in cols}
        edge = {x: ys.start + int(np.max(np.where(solid[ys, x])[0])) for x in cols}
        bot = {x: low[x] for x in cols if edge[x] - low[x] <= 2}
        x0, x1 = min(cols), max(cols)
        s = 1 if (x0 + x1) / 2 > mid else -1                      # outward: away from the face's middle
        inner, outer = (x0, x1) if s > 0 else (x1, x0)
        at = lambda u: int(round(inner + (outer - inner) * u))
        wd = x1 - x0
        for u in np.linspace(LASH_FROM, 0.93, LASHES):
            x = at(u)
            spike(np.array([x + 0.5, top[x] + 1.6]), 8 + 52 * u ** 1.6, wd * (0.10 + 0.17 * u ** 1.3) * LASH_LEN, wd * (0.060 + 0.035 * u) * LASH_W, s)
        # the outer corner: the lid's line carried on as ONE arc, out and up (user 2026-11-14, an arrow at a notch under
        # the outer lashes: "the far away eye lashes should extend its root, forming a pretty arc from the eyes"). Before:
        # two wings from the same spot, a notch between them. The arc starts inside the lid's line, as thick as the
        # line is there, and tapers to a point; the outermost lashes grow from the arc itself, each shorter than the last
        # (it leaves the lid along the lid's own direction there, the slope of its middle over the outer third, then
        # turns up: a flick, not a wedge. A pass through the preset's lowest corner tip filled a heavy triangle)
        xo = at(0.80)
        thick = max(low[xo] - top[xo] + 1.0, wd * 0.07)
        xs_ = np.array(sorted(x for x in cols if 0.62 <= (x - inner) / (outer - inner) <= 0.90), float)
        slope = np.polyfit(xs_, [(top[int(x)] + low[int(x)]) / 2 for x in xs_], 1)[0]
        tang = np.array([s, slope * s]) / np.hypot(1, slope)
        p0 = np.array([xo + 0.5, (top[xo] + low[xo]) / 2 + 0.5])
        arc = spike(p0, 38, wd * 0.125 * LASH_LEN, thick * 1.05, s, via=p0 + tang * wd * 0.105 * LASH_LEN)
        for t_, len_ in ((0.30, 0.19), (0.50, 0.145), (0.68, 0.10)):
            i_ = int(t_ * (len(arc) - 1))
            spike(arc[i_], 36 + 14 * t_, wd * len_ * LASH_LEN, wd * 0.080 * LASH_W * (1.1 - 0.6 * t_), s, curl=14)
        for u in (0.52, 0.66, 0.80, 0.93)[0 if LASH_W > 1.2 else 1:]:
            x = at(u)
            if x in bot:
                spike(np.array([x + 0.5, bot[x] - 0.4]), 180 - (30 + 32 * u), wd * 0.085 * LASH_LEN * (0.7 + 0.5 * u), wd * 0.038 * LASH_W, s, curl=-10)
        # the shadow: by the distance above the lid's top edge, deepest toward the outer corner
        tx = np.array([top[x] for x in cols], float)
        lid = np.interp(xx, np.array(cols) + 0.5, ndimage.gaussian_filter1d(tx, 1.0), left=np.nan, right=np.nan)
        u_ = np.clip((xx - inner) / (outer - inner), 0, 1)
        up = lid - yy
        sh = np.maximum(sh, np.where(np.isnan(lid), 0, np.exp(-(np.clip(up, 0, None) / (wd * 0.11)) ** 2) * (up > -1.5) * (0.35 + 0.65 * u_) * np.sin(np.pi * np.clip((xx - x0 + 2) / (wd + 4), 0, 1)) ** 0.5))
    lash = np.asarray(cv.resize((N * K, N * K), Image.LANCZOS)).astype(float) / 255
    blk = (slice(0, N * K), slice(0, N * K))
    hm = head[blk]
    o = J.o[blk]
    o[hm] = (o * (1 - SHADOW * ndimage.gaussian_filter(sh, 0.6 * K)[..., None]) + np.array([112.0, 62, 104]) * SHADOW * ndimage.gaussian_filter(sh, 0.6 * K)[..., None])[hm]
    o[hm] = (o * (1 - lash[..., None]) + ink * lash[..., None])[hm]
    # the check: with the preset laid on, every dark piece round the eyes must be part of an eye (nothing floats)
    kk = K * 256
    comp = J.o[:kk, :kk].copy()
    big = np.asarray(Image.fromarray(ov.astype(np.uint8), "RGBA").resize((kk, kk), Image.LANCZOS)).astype(float)
    comp = comp * (1 - big[..., 3:] / 255) + big[..., :3] * big[..., 3:] / 255
    dk = (comp @ LUM < 90)
    zone = np.zeros_like(dk)
    for b in boxes:
        zone[max(b[0].start - 14, 0) * K:(b[0].stop + 8) * K, max(b[1].start - 12, 0) * K:(b[1].stop + 12) * K] = True
    cl, cn = ndimage.label(dk & zone)
    sizes = ndimage.sum(dk & zone, cl, range(1, cn + 1))
    lk = np.zeros((kk, kk), bool); lk[:N * K, :N * K] = lash > 0.3
    eyes2 = set((np.argsort(sizes)[-2:] + 1).tolist())
    loose = [int(sizes[i - 1]) for i in range(1, cn + 1) if i not in eyes2 and sizes[i - 1] >= 6 and lk[cl == i].any()]      # (pieces of lash only; a tip's last faint texels do not count)
    if loose:                                                    # show them: red on the composite, 4 x
        keep = np.argsort(sizes)[-2:] + 1
        mark = comp.copy(); mark[(cl > 0) & ~np.isin(cl, keep)] = [255, 0, 0]
        Image.fromarray(np.clip(mark, 0, 255).astype(np.uint8)).crop((0, 30 * K, 128 * K, 80 * K)).resize((128 * K * 4, 50 * K * 4), Image.NEAREST).save(J.out / "_cache" / "lash_loose.png")
    assert not loose, f"eye make-up: dark pieces not joined to an eye (texels each): {loose}"
    print(f"eye make-up: {len(boxes)} eyes of face {face}, {LASHES} + 3 lashes each, {int((lash > 0.5).sum())} texels of lash; lid ink {np.round(ink).astype(int).tolist()}")


def eyes():
    """The helmeted one, on royal."""
    J = Job("eyes", "royal", "LadyNoir", sub=0)
    M, R, r, m = J.M, J.R, J.r, J.m
    Y, Z, nx = np.abs(M.pos[..., 1]), M.pos[..., 2], M.nrm[..., 0]
    front, back = R.nrm[..., 0] > 0.15, R.nrm[..., 0] < -0.15
    e = dict(face=(62, 62), hairB=(170, 100), brow=(306, 97), puff=(480, 63), bodice=(386, 163), front=(426, 295), backp=(458, 326),
             side=(372, 442), legs=(148, 327), sleeve=(279, 314), hips=(150, 219), boot=(301, 236), foot=(78, 441), sole=(10, 449),
             bootcuff=(176, 473), wing=(253, 403), cowl=(225, 247), cowl2=(476, 457), helmet=(255, 168))
    E = {k: r(v) for k, v in e.items()}
    # --- same layout: the enemy's own paint
    for seeds in ((419, 15), (21, 253), (66, 253), (63, 328), (20, 386), (136, 497), (314, 491)):      # neck, ears, hand, palm, tail, its tip
        J.same(m(seeds))
    # --- own paint, the enemy's colours: the face (under the face preset's eyes), the hair (another cut), the coat
    head = m((62, 61))
    J.own(head, palette(R.rgb, E["face"], (6, 62, 96)), k=0.9)
    face_marks(J, head)
    hair = m((179, 80), (263, 45), (238, 112), (23, 169), (90, 174))
    # (user 2026-11-14, looking up at the head: "the texture missed some hair": the hair was near flat, one soft ramp
    # over the smoothed luminance. Now royal's own strand painting at full sharpness, each island on its own median,
    # through her hair's shade / base / light: HAIR_K sets the contrast)
    hp = palette(R.rgb, E["hairB"], (3, 50, 97), w=3)
    print("hair palette:", [np.round(c).astype(int).tolist() for c in hp])
    Ls = J.src @ LUM / 255
    pic = hair_picture(M, BASE / "hair_ref.png") if HAIR_TEX else np.full(M.lab.shape, 0.62)      # (off 2026-11-14: "remove the hair texture for now, it looks too much")
    for seed in ((179, 80), (263, 45), (238, 112), (23, 169), (90, 174)):
        hi_ = m(seed)
        t_ = 0.5 + (tone(Ls, hi_ & M.covered, 1, 99.5) - 0.5) * HAIR_K
        J.o[hi_] = ramp3(0.5 + (t_ - 0.5) * (0.7 if HAIR_TEX else 1.0) + HAIR_TEX * 0.75 * (pic - 0.62), hp)[hi_]
        J.mix(hi_, hp[0] * [0.70, 0.64, 0.72], HAIR_TEX * 0.55 * (1 - sstep(pic, 0.05, 0.40)))      # the picture's dark gaps, deeper than her hair's own shade
    dress = palette(R.rgb, E["bodice"] | E["side"], (6, 38, 66))
    trim = palette(R.rgb, E["brow"], (20, 60, 95))
    coat = m((441, 190), (452, 337), (499, 424), (473, 10))
    strip = m((300, 162))                                        # the inner dress's front, between the coat's edges
    cape = m((240, 216), (399, 45))
    collar, collar_in = m((322, 290), (332, 19), (363, 27)), m((78, 386))
    jabot = m((346, 465), (236, 286))
    h, s, v = hsv(J.src)
    gold = sstep(s, 0.25, 0.45) * (hd(h, 45) < 25) * sstep(v, 0.35, 0.55)
    mf, mb, rf, rb = nx > 0.3, nx < -0.3, R.nrm[..., 0] > 0.3, R.nrm[..., 0] < -0.3
    # --- royal's own forms in her colours: the chest (capelet, collar, the throat ornament) and the inner dress's
    # front. Two passes read her bodice onto them (bare chest, eye cups, waist disc): user 2026-11-13, with both
    # boxed: "it is too forced to match the reference on uneven texture meant for an entirely different things, in
    # this case, don't force it, just use other designs that respect the model there". So: the model's own cloth,
    # trims and ornaments, her purple for the cloth, her silver for what royal draws light, the gold zigzag faint
    stops = [0.0, 0.10, 0.22, 0.40, 0.58, 0.85]
    cols = np.array([dress[0] * 0.8, dress[1], dress[2], trim[0], trim[1], trim[2]])
    recol = np.stack([np.interp(J.L, stops, cols[:, i]) for i in range(3)], -1)
    for part in (cape, collar):
        J.o[part] = recol[part]
        J.mix(part, dress[2] * 1.12, gold * 0.9)
    J.own(collar_in, palette(R.rgb, E["cowl"] | E["cowl2"], (10, 62, 97)))         # the collar's other face: her cowl's black and red
    J.own(jabot, trim)
    # --- the coat: plain cloth first (royal's own grey edging and zigzag are replaced by her border, below)
    # ONE clean cloth for the whole coat (user 2026-11-14, boxing the coat's side under the belt: "some places are not
    # clean"): the body's form and soft drape folds, as on its back, not royal's own paint through a ramp (its light
    # hem trim came out as a flat grey skirt beside the dark back; its edging as stray tones)
    from wardrobe_bat_robe import folds
    drape = folds(Y, Z, 0.045, 7, long=7.0) * sstep(1.02 - Z, 0.0, 0.25)
    cloth = dress[1] * (0.82 + 0.30 * J.form + 0.17 * drape)[..., None]
    J.o[coat] = cloth[coat]
    J.o[m((452, 337))] = (cloth * 0.82)[m((452, 337))]                # its inside face, a shade darker
    # its back and its sides: her skirt's panels as seen from behind and from the side, where she has them (the big
    # white eye sits on her side panels: user "texture of the side coat could use some white eye sigils from the ref coat")
    DB = (E["bodice"] | E["backp"] | E["side"]) & rb
    if COAT_BACK == "ref":
        J.take(coat & mb, DB, "coat back", absy=True, view=-1, within=0.015)
    else:
        coat_back(J, coat, dress, R, E)
    # Her eye sigil (the eye in its diamond frame with the four leaves: SIGIL, its box on her sheet) once on each hip,
    # whole: wrapped round the coat (across = the way round the body from the front's middle, so it does not stretch
    # where the coat turns from front to side), wholly over the belt, read between her texels from the sharp sheet,
    # only its drawn lines on the clean cloth. (Before: the same eye twice and in parts: a reading of her panels from
    # the side, with their cloth, borders and hem: ragged bands and thorns under the belt, scribbles by the chest, user
    # 2026-11-14 "some places are not clean"; and this box laid flat from the front across the belt, its stem's tip
    # showing under the belt as a lone thorn.)
    # (user, of that pass: "you are starting to lose way too much details on the robe": the big eye of her side panels
    # is back on the coat's sides, over the belt: seen from the side, the outermost of her layers, only its drawn
    # lines, read from the sharp sheet. SIGIL_HIP: the small sigil instead / as well; off, it is the same motif)
    # (user, with arrows at the eye's top and its rear leaf: "you have to make sure each UV islands connects cleanly
    # when it assemble in the model too ... the pattern got cut awkwardly for no reason". The coat's side is ONE island:
    # the cuts were this reading's own limits, a hard test on the coat's normals (side-facing only), the same test on
    # hers, and a fade under z 1.02. Now the whole outside of the coat over the belt may take it, from all of her dress
    # island, her outermost layer; it ends where HER design ends. Only the coat's front and back middles stay out,
    # softly: they carry the lining and her back panel)
    # (and, on the next close-up, the eye's stem still cut on a straight line where the coat turns from its side to its
    # front: "explain why your own painting can cause such an unclean cut when the UV map is not even the problem?".
    # A reading from ONE VIEW (here: from the side, the key = x, z) is only valid where the surface faces that view;
    # where it turns away the picture smears, so the reading needs a limit there, and a limit across a motif is a cut.
    # So: no view. Both surfaces are unrolled round the body instead (the angle about each one's own upright axis x a
    # fixed 17 cm, and the height): her skirt round her, the coat round the Bat. A motif keeps its shape all the way
    # round, and the only limits left are the coat's own other designs: its front lining and her back panel.)
    def unroll(pos, xc):
        return np.stack([np.arctan2(np.abs(pos[:, 1]), pos[:, 0] - xc) * 0.17, pos[:, 2]], 1)
    hipM, hipR = m((441, 190)) & M.covered & (np.abs(Z - 0.80) < 0.05), E["bodice"] & R.covered & (np.abs(R.pos[..., 2] - 0.80) < 0.05)
    xcM, xcR = [float((q.min() + q.max()) / 2) for q in (M.pos[..., 0][hipM], R.pos[..., 0][hipR])]
    side_dst = m((441, 190)) & M.covered & (Z > 0.58) & (Z < 1.12)
    ang_ = np.degrees(np.arctan2(Y, M.pos[..., 0] - xcM))
    strokes(J, side_dst, E["bodice"], lambda q: unroll(q, xcM), "coat side", reach=0.008, inset=2, fade=14,
            depth=lambda q: np.hypot(q[:, 0] - xcR, q[:, 1]), key_src=lambda q: unroll(q, xcR),
            k=sstep(Z, 0.585, 0.595) * (1 - sstep(Z, 1.025, 1.06)) * sstep(ang_, 22, 32) * (1 - sstep(ang_, 138, 150)))      # (its lower end: behind the belt, which covers z 0.58-0.60 all the way round: no fade in view)
    print(f"coat side: unrolled round x {xcM:.3f} (the coat) / {xcR:.3f} (her dress)")
    outer_c = m((441, 190))
    ringc = outer_c & M.covered & (np.abs(Z - SIGIL_Z) < 0.04)
    xc_ = float((M.pos[..., 0][ringc].min() + M.pos[..., 0][ringc].max()) / 2)
    th_ = np.arctan2(Y, M.pos[..., 0] - xc_)
    rad_c = float(np.median(np.hypot(M.pos[..., 0][ringc] - xc_, Y[ringc])))
    at_ = ringc & (nx > 0.3) & (np.abs(Y - SIGIL_AT) < 0.012)       # its middle: on the front piece's face, SIGIL_AT from the body's middle
    th0 = float(np.median(th_[at_]))
    hh = SIGIL_H
    ww = hh * (SIGIL[2] - SIGIL[0]) / (SIGIL[3] - SIGIL[1])
    u, vv = (th_ - th0) * rad_c / ww + 0.5, (SIGIL_Z + hh / 2 - Z) / hh
    inb = outer_c & (u > 0) & (u < 1) & (vv > 0) & (vv < 1)
    px = np.clip(((SIGIL[0] + u * (SIGIL[2] - SIGIL[0])) * K).astype(int), 0, R.rgb.shape[1] - 1)
    py = np.clip(((SIGIL[1] + vv * (SIGIL[3] - SIGIL[1])) * K).astype(int), 0, R.rgb.shape[0] - 1)
    patch = R.rgb[py, px] if R.hi is None else bilinear(R.hi, (SIGIL[0] + u * (SIGIL[2] - SIGIL[0])).clip(0, 511.99) * (R.hi.shape[1] / 512) - 0.5,
                                                         (SIGIL[1] + vv * (SIGIL[3] - SIGIL[1])).clip(0, 511.99) * (R.hi.shape[0] / 512) - 0.5)
    box = R.rgb[SIGIL[1] * K:SIGIL[3] * K, SIGIL[0] * K:SIGIL[2] * K].reshape(-1, 3)
    drawn = sstep(np.abs(patch - np.median(box, 0)).max(-1), 14, 44)
    # only the sigil itself: her panel's border strokes cut through the box's corners (they showed as lone thorns on the
    # coat). A rounded diamond about the sigil's middle on her sheet (384, 199), 28 x 57 texels to its rim
    sx_, sy_ = SIGIL[0] + u * (SIGIL[2] - SIGIL[0]), SIGIL[1] + vv * (SIGIL[3] - SIGIL[1])
    own = 1 - sstep((np.abs(sx_ - 384) / 28) ** 2.5 + (np.abs(sy_ - 199) / 57) ** 2.5, 0.85, 1.0)
    if SIGIL_HIP:
        J.mix(inb, patch, drawn * own)
    print(f"sigil on each hip: {ww * 100:.1f} x {hh * 100:.1f} cm at z {SIGIL_Z}, its middle {SIGIL_AT * 100:.0f} cm from the body's middle ({np.degrees(th0):.0f} deg round; the coat {rad_c * 100:.0f} cm from its axis there), {int((inb & M.covered).sum())} texels")
    # her silver border along every edge of the coat (user, tracing the coat's front edge down to the hem's point:
    # "I want you to add reference image silver lining border along the edges of the coat too"): the border's own
    # colours from her sheet (the stroke beside the sigil), a band following the coat island's edge: a dark line, the
    # silver with its light middle, a dark line, a lilac glow inside, as hers
    st = R.rgb[150 * K:228 * K, 430 * K:446 * K].reshape(-1, 3)
    st = st[(st.max(1) - st.min(1)) / np.maximum(st.max(1), 1) < 0.16]
    silver = [np.percentile(st, 55, axis=0), np.minimum(np.percentile(st, 94, axis=0) * 1.12, 255), np.array([242.0, 245, 247])]
    # The coat's outside (441,190) and its inside (452,337) are two islands. Both halves of each read the same texels
    # (measured: 99.5 % of the texels have a triangle on her left and one on her right), so left and right cannot differ
    # by the paint. But the idle pose swings her left flap open and shows its INSIDE, and the inside island's own
    # sheet border is not the cloth's edge: the lining drawn along it ran astray there (user: "the right robe piece,
    # the silver lining didn't align nicely along the edge of the coat like the left side, is it a mirrored skin
    # problem?"). The inside takes its lining from the outside's edge instead: by the distance, on the body, to the
    # outside island's border, in the same width
    outer, inner = m((441, 190)), m((452, 337))
    hem = outer | inner
    t = M.edge / K                                               # texels of the game's sheet in from the island's edge
    # (the back's middle, where the two mirrored halves meet, is an island edge but not the cloth's: no lining there)
    seam = (Y < 0.008) & (nx < -0.1)                               # (0.005 left texels of the seam at z 0.41-0.50, |y| to 0.0058, as "edge": a pale drop of lining low on the back)
    rim_o = outer & M.covered & (M.edge < 1.6 * K) & ~seam
    t[outer] = (ndimage.distance_transform_edt(~rim_o) / K)[outer]
    Pa = M.pos * [1, 0, 1] + np.abs(M.pos * [0, 1, 0])
    ob = outer & M.covered & (M.edge < 1.6 * K)
    otree = cKDTree(Pa[ob])
    ring = outer & M.covered & (np.abs(t - LINING) < 0.4)
    per_texel = float(np.median(otree.query(Pa[ring])[0])) / LINING          # body units per sheet texel on the coat
    t[inner] = otree.query(Pa[inner])[0] / per_texel
    print(f"coat lining: {per_texel * 1000:.1f} mm per sheet texel; the inside face within the lining's width: {100 * (t[inner & M.covered] < LINING).mean():.0f} % of it")
    # (user: "I want thicker silver lining with brighter tone to contrast, now it just blends in": LINING texels wide
    # (3.5 before), from her border's mid grey up to near white, a darker line each side)
    band = ramp3(0.25 + 0.75 * (1 - np.abs(t - 0.45 - LINING / 2) / (LINING / 2)).clip(0, 1), silver)
    J.mix(hem, dress[2] * 1.3, (1 - sstep(t, LINING + 1.0, LINING + 3.2)) * 0.40)
    J.mix(hem, dress[0] * 0.40, 1 - sstep(t, LINING + 0.5, LINING + 1.2))
    # her border's second line (on her panels a thinner grey stroke runs inside the silver one), LINE2 texels in, with a
    # dark line each side: detail along every edge and spike of the hem that follows the coat's own outline
    t2 = np.abs(t - LINE2)
    J.mix(hem, dress[0] * 0.45, (1 - sstep(t2, 1.0, 1.5)) * 0.8)
    J.mix(hem, silver[0] * 0.92, 1 - sstep(t2, 0.55, 0.95))
    J.mix(hem, band, 1 - sstep(t, LINING, LINING + 0.5))
    J.mix(hem, dress[0] * 0.40, 1 - sstep(t, 0.8, 1.3))          # (0.25-0.55 before: thinner than a texel, it broke into teeth along the lapels)
    if BELT != "none":
        sl = R.rgb[E["sleeve"] & R.covered]
        sh, ss, sv = hsv(sl)
        wg = R.rgb[E["wing"] & R.covered]
        wh, ws, wv = hsv(wg)
        mag = wg[(wh > 295) & (wh < 345) & (ws > 0.35) & (wv > 0.25)]
        pal = dict(dress=dress, white=np.array([232.0, 222, 240]),
                   stripe_dark=sl[sl @ LUM < np.percentile(sl @ LUM, 30)].mean(0),
                   stripe_blue=sl[(sh > 195) & (sh < 260) & (ss > 0.15)].mean(0) if ((sh > 195) & (sh < 260) & (ss > 0.15)).sum() > 50 else np.array([67.0, 79, 99]),
                   mag=mag.mean(0) * 1.15 if len(mag) > 50 else np.array([120.0, 40, 90]))
        print("belt palette:", {k: np.round(v).astype(int).tolist() for k, v in pal.items() if k != "dress"})
        belt(J, m((499, 425)), silver, pal)
    # --- the front piece, fitted to ITS shape (user, tracing its outline: "you copied the pattern with no extra thoughts
    # that the actual shape of the front piece is like this [it ends in two tails, hers in one point], please optimize
    # the pattern to fit well with that model in mind"). Below the waist: (1) her tabard's inside (the V, the curls
    # with their leaves, the diamond) laid across the piece's own width at every height (u = |y| / the piece's edge
    # there -> the same share of her tabard's width), her top to HER_LOW onto the piece's top to where it splits;
    # (2) plain cloth on the two tails; (3) the silver border drawn along the piece's real outline, round both tails
    # (by the distance to the island's edge; the mirror seam at y = 0 is not an edge)
    cv = strip & M.covered
    zb = np.arange(0.30, 1.17, 0.005)
    ib = np.digitize(Z[cv], zb)
    yo = np.array([Y[cv][ib == i].max() if (ib == i).any() else np.nan for i in range(1, len(zb))])
    yi = np.array([Y[cv][ib == i].min() if (ib == i).any() else np.nan for i in range(1, len(zb))])
    zc = zb[:-1] + 0.0025
    ok = ~np.isnan(yo)
    yo_f = ndimage.gaussian_filter1d(np.interp(zc, zc[ok], yo[ok]), 2)
    z_split = float(zc[ok & (yi > 0.010) & (zc < 0.8)].max())
    # (her tabard's top, above z 0.9, lies on the other side of her sheet's mirror line (y < 0): with only y >= 0 read,
    # that part found nothing near and took her border's grey and its dark outline from far off by turns: a comb of
    # teeth down the V. Both sides are read now, as |y|)
    tsrc = E["front"] & rf & R.covered & (R.edge >= 1.5 * K)
    tp, tc = R.pos[tsrc] * [1, 0, 1] + np.abs(R.pos[tsrc] * [0, 1, 0]), R.rgb[tsrc]
    hb = np.arange(tp[:, 2].min(), tp[:, 2].max(), 0.005)
    hi_ = np.digitize(tp[:, 2], hb)
    hw = np.array([tp[hi_ == i][:, 1].max() if (hi_ == i).any() else 0 for i in range(1, len(hb) + 1)])
    her_top = min(TAB_TOP, float(tp[:, 2].max()) - 0.01)
    # ONE cloth and ONE border for the whole piece under the neckline (user 2026-11-13, an arrow at the waist: "the seams
    # here is not connecting cleanly, it looks like a sudden crop even though there's no 3D shift there": above TAB_TOP
    # the piece had kept an earlier reading of her bodice, in another purple, and the border began at TAB_TOP). The
    # motif fades in under the waist sigil instead of starting at a cut
    low = strip & (Z < neck_z(Y) - 0.013 * neck_n(Y))    # (the neckline's edge is measured across it, not in height)
    main = low & (Z > z_split) & (Z < TAB_TOP)
    v_ = (TAB_TOP - Z) / (TAB_TOP - z_split)
    zq = her_top - v_ * (her_top - HER_LOW)
    u_ = Y / np.maximum(np.interp(Z, zc, yo_f), 1e-3)
    yq = u_ * np.interp(zq, hb + 0.0025, ndimage.gaussian_filter1d(hw, 1.5))
    qk_ = np.stack([yq[main], zq[main]], 1)
    d_, j_ = cKDTree(tp[:, 1:]).query(qk_)
    ty_, tx_ = np.where(tsrc)
    tcf = fine(R, ty_[j_], tx_[j_], qk_ - tp[j_][:, 1:], lambda q: np.stack([np.abs(q[:, 1]), q[:, 2]], 1))      # her tabard between its texels (the sharp sheet)
    # (at the piece's middle her tabard has no texel to give: its own middle is the island's edge, left unread. Those
    # spots fell back to plain cloth: a stripe down the middle, "fix the seam", user 2026-11-13. Near the middle the
    # nearest texel of hers is taken from further away)
    # (0.02 before: inside the V notch at her tabard's top, where she has no cloth at all, rows took her border's grey or
    # its dark outline from up to 2 cm away by turns: a comb of teeth down the V's inner edge, plain to see once the
    # lines were sharp. 0.008 still bridges the unread middle)
    got = ((d_ < 0.006) | ((u_[main] < 0.25) & (d_ < 0.008))) & (u_[main] < 0.84)
    cloth = np.median(tc[j_[got]], 0)
    J.o[low] = (cloth * (0.86 + 0.28 * J.form)[..., None])[low]
    ys_, xs_ = np.where(main)
    fade = sstep(TAB_TOP - Z[ys_[got], xs_[got]], -0.002, 0.010)[:, None]
    J.o[ys_[got], xs_[got]] = J.o[ys_[got], xs_[got]] * (1 - fade) + tcf[got] * fade
    # above the waist the piece carries her bodice's own lines the same way (user: "the part above the horizontal cut
    # earlier looks bad, not textured and no patterns compared to below"): her dress's front at the same height, laid
    # across the piece's own width (u = |y| / the piece's edge there), in the tabard's cloth colour so the two join
    # (TAB_TOP 0.935 + a second reading of her bodice above it, until 2026-11-14: user, boxing the piece: "these two parts
    # are the same piece, yet the pattern got cut awkwardly for no reason". Her tabard alone now, from under the waist
    # sigil down to the split, one motif; TAB_UPPER brings the old upper reading back)
    if TAB_UPPER:
        bsrc = E["bodice"] & rf & R.covered & (R.edge >= 1.5 * K)
        bp, bc = np.stack([np.abs(R.pos[..., 1][bsrc]), R.pos[..., 2][bsrc]], 1), R.rgb[bsrc]
        bb = np.arange(TAB_TOP - 0.03, 1.17, 0.005)
        bi = np.digitize(bp[:, 1], bb)
        bw = np.array([np.percentile(bp[bi == i][:, 0], 98) if (bi == i).sum() > 20 else np.nan for i in range(1, len(bb) + 1)])
        okb = ~np.isnan(bw)
        bw = ndimage.gaussian_filter1d(np.interp(bb, bb[okb], bw[okb]), 1.5)
        upper = low & (Z >= TAB_TOP - 0.012)
        yq2 = Y / np.maximum(np.interp(Z, zc, yo_f), 1e-3) * np.interp(Z, bb + 0.0025, bw)
        qk2 = np.stack([yq2[upper], Z[upper]], 1)
        d2, j2 = cKDTree(bp).query(qk2)
        by2, bx2 = np.where(bsrc)
        bcf = fine(R, by2[j2], bx2[j2], qk2 - bp[j2], lambda q: np.stack([np.abs(q[:, 1]), q[:, 2]], 1))
        g2 = (d2 < 0.006) & ((Y / np.maximum(np.interp(Z, zc, yo_f), 1e-3))[upper] < 0.86)
        col2 = bcf[g2] * (cloth / np.maximum(np.median(bc[j2[g2]], 0), 1))          # her bodice's cloth -> the tabard's
        yu, xu = np.where(upper)
        f2 = sstep(Z[yu[g2], xu[g2]] - TAB_TOP, -0.012, 0.010)[:, None]
        J.o[yu[g2], xu[g2]] = J.o[yu[g2], xu[g2]] * (1 - f2) + np.clip(col2, 0, 255) * f2
        print(f"front piece, above the waist: her bodice's half-width {bw.min() * 100:.1f}..{bw.max() * 100:.1f} cm, lines on {int(g2.sum())} of {int(upper.sum())} texels")
    rim = cv & (M.edge < 1.6 * K) & (Y > 0.006)
    tb = ndimage.distance_transform_edt(~rim) / K
    pb = ramp3(0.25 + 0.75 * (1 - np.abs(tb - 0.4 - PANEL_RIM / 2) / (PANEL_RIM / 2)).clip(0, 1), silver)
    J.mix(low, dress[0] * 0.40, 1 - sstep(tb, PANEL_RIM + 0.4, PANEL_RIM + 1.0))
    J.mix(low, pb, 1 - sstep(tb, PANEL_RIM, PANEL_RIM + 0.4))
    print(f"front piece: splits at z {z_split:.3f}; its half-width {np.nanmin(yo_f) * 100:.1f}..{np.nanmax(yo_f) * 100:.1f} cm; her tabard z {tp[:, 2].min():.2f}..{tp[:, 2].max():.2f}, motif on {int(got.sum())} texels")
    # her round waist sigil on the piece (user, boxing the spot: "add circle sigil from the ref image here too"): drawn,
    # from her rings: silver rim, dark ring, silver ring, dark middle (her own piece of it is half a disc standing off
    # the body: a reading by place brought only its outline)
    rr = np.hypot(Y / DISC[1], (Z - DISC[0]) / DISC[2])
    J.mix(strip, dress[0] * 0.40, 1 - sstep(rr, 1.04, 1.12))
    J.mix(strip, ramp3(0.45 + 0.5 * (1 - np.abs(rr - 0.84) / 0.16).clip(0, 1), silver), 1 - sstep(rr, 0.98, 1.04))
    J.mix(strip, dress[0] * 0.55, 1 - sstep(rr, 0.64, 0.70))
    J.mix(strip, ramp3(0.45 + 0.5 * (1 - np.abs(rr - 0.47) / 0.11).clip(0, 1), silver), 1 - sstep(rr, 0.54, 0.60))
    J.mix(strip, dress[1], 1 - sstep(rr, 0.32, 0.38))
    # skin under the throat ornament (user: "show some skin under the complex 3d shapes above, no need to match the ref
    # exactly"): the piece's top above a neckline that rises to the sides, with her silver edge. Royal's hanging tab,
    # the trinket, keeps its own paint ("it should be underneath the trinket, the trinket itself shouldn't get
    # recolored"; its front face is the capelet island's middle, z < 1.21, x > 0.11, its back the island at 236,286).
    # The cleavage is DRAWN on the chest, as her own sheet draws hers (two shade strokes running down to the middle):
    # the trinket hangs over the middle 3 cm each side, so a shade in the middle alone never showed ("I checked
    # visually, there's no cleavage at all": two passes had put the summer texture's soft shade there, grey and
    # hidden). Each breast's upper line runs from the middle (CLEAVE[0]) up and out, crossing the chest that shows
    # beside the trinket: a dark line, a soft shade on the sternum's side, a light on the breast's; and the line
    # between the breasts below their meeting point, for the view from the side
    # What shows there is the UNDERSIDE of the breasts, not the upper cleavage (user 2026-11-13, after the summer
    # texture's cleavage was copied there and did not show: "the position should be the underboob, not the upper
    # cleavage, so there's a little of manual repositioning and improvisation left for you"). The mesh says where:
    # above z ~1.175 the piece comes forward and faces down (nz -0.35..-0.6: the breast's underside), below it is the
    # near-upright ribs (nz -0.17). So, improvised on that shape, all soft (blurred), warm: the fold under each breast
    # (FOLD: a round, lowest at |y| 4.5 cm, rising to the middle where the breasts meet), the underside in shade above
    # it (deepest at the fold), the breast's cast shade on the ribs below it, fading down
    sk = np.median(R.rgb[36 * K:60 * K, 335 * K:352 * K].reshape(-1, 3), 0)
    zn = neck_z(Y)
    bare = 1 - sstep(Z - zn, -0.002, 0.002)                      # 0 above the neckline
    chest = strip & (bare < 0.5)
    dn = Z - (FOLD[0] + FOLD[1] * (Y - 0.045) ** 2)             # > 0: on the breast's underside
    sh_ = np.where(dn > 0, 0.34 * np.exp(-dn / 0.030), 0.46 * np.exp(dn / 0.017)) + 0.22 * np.exp(-(dn / 0.004) ** 2)
    sh_ = sh_ + 0.25 * np.exp(-(Y / 0.006) ** 2) * (dn > 0)      # the line between the breasts, above where they meet
    sh_ = ndimage.gaussian_filter(np.where(chest, sh_, 0.0), 1.2 * K) / np.maximum(ndimage.gaussian_filter(chest.astype(float), 1.2 * K), 0.05)
    lr = 1 - np.clip(sh_, 0, 0.8)
    J.mix(strip, sk[None, None, :] * np.stack([lr ** 0.80, lr ** 1.06, lr ** 1.02], -1), 1 - bare)
    # a faint midriff (user: "add a bit of midriff texture on the bare skin part? just a faint texture"): the Bat's own
    # summer texture paints a bare belly on the same body (the sternum's line, the ribs' soft shade, the navel's dip);
    # its light and shade below the breasts' fold, AT THE SAME PLACE. No navel: on every Bat outfit that shows one
    # (summer, nude, warlock, illusionist) it sits at z 1.00-1.01, under the U's bottom (1.035) and its silver edge.
    # A first pass read the belly 5.2 cm higher to bring the navel into the U: too high (user: "how sure are you that
    # belly button is supposed to be there? ... if not use different shading of midriff that's not belly button").
    # Instead: a soft, wide shade down the middle (the belly's centre line) and the belly's roundness (a little
    # darker toward the U's sides), both faint
    S = cached_maps(CLS, "summer", K, J.out / "_cache")
    sim = Image.open(DATA / CLS / "tex" / "summer1.webp").convert("RGB")
    srgb = np.asarray(sim.resize((sim.width * K, sim.height * K), Image.LANCZOS)).astype(float)
    sh2, ss2, sv2 = hsv(srgb)
    sskin = isl(S, K, 360, 102) & S.covered & (S.edge >= 2 * K) & (S.nrm[..., 0] > 0.3) & (hd(sh2, 20) < 18) & (ss2 > 0.09) & (ss2 < 0.45) & (sv2 > 0.70)
    slum = srgb[sskin] @ LUM
    _, jm = cKDTree(np.stack([np.abs(S.pos[..., 1][sskin]), S.pos[..., 2][sskin]], 1)).query(np.stack([Y[chest], Z[chest]], 1))
    mr = np.ones(Y.shape)
    mr[chest] = slum[jm] / np.median(slum)
    mr = ndimage.gaussian_filter(mr, 0.8 * K)
    below = sstep(-dn, 0.0, 0.02)                                # under the fold only: the breasts keep theirs
    # (user, of 7 % / 6 % with wide falloffs: "too faint and diffused": stronger and tighter now)
    mid = (np.clip(1 + (mr - 1) * MIDRIFF * below, 0.6, 1.1) - MID_LINE * np.exp(-(Y / 0.0055) ** 2) * below * sstep(Z, NECK + 0.008, NECK + 0.022)
           - MID_SIDE * sstep(Y, 0.010, 0.046) * sstep(-dn, -0.03, 0.03))
    # (the side shade began at a hard step, |y| 2.2-3 cm, and at the fold: "the 2 shades there didn't blend nicely".
    # Now a wide ramp that runs on into the breasts' underside; the whole factor smoothed on the body)
    mid_f = np.where(chest, mid, 0.0)
    wt = ndimage.gaussian_filter(chest.astype(float), 1.5 * K)
    mid = np.where(chest, ndimage.gaussian_filter(mid_f, 1.5 * K) / np.maximum(wt, 0.05), 1.0)
    J.o[chest] = (J.o * np.stack([mid ** 0.85, mid ** 1.05, mid ** 1.05], -1))[chest]
    print(f"midriff: {int((chest & (below > 0.5)).sum())} texels, shade {mid[chest].min():.2f}..{mid[chest].max():.2f}")
    print(f"chest: {int((chest & M.covered).sum())} texels; shade {sh_[chest].min():.2f}..{sh_[chest].max():.2f}")
    J.mix(strip, ramp3(np.full(Y.shape, 0.8), silver), (1 - sstep(np.abs((Z - zn) / neck_n(Y) + 0.006), 0.004, 0.006)))
    J.mix(strip, dress[0] * 0.40, (1 - sstep(np.abs((Z - zn) / neck_n(Y) + 0.0125), 0.0010, 0.0022)))
    # her helmet's band with the eye disc, whole, across the forehead: on the hair AND on the bare forehead between
    # its strands (user: "why only half? bring the full headband texture (on the hair itself ...)"). Half was missing
    # because her helmet is a mirrored part (its texels hold y >= 0 only): read with absy. Only the band and the disc
    # (her helmet below BAND_TOP), worn BAND_DROP lower than hers so the hood's edge does not cover the disc
    # Painted on the hair as a band worn round the head, not laid on from the front (user 2026-11-14, looking up at it:
    # "the silver metallic part bled into Bat's forehead and hair, it's almost like a cheap attempt at projection, can
    # you fix this as if you are an 3D model artist drawing directly on the 3D model?"). The front reading had also
    # painted the forehead's skin behind the fringe (hidden from the front above z 1.53, in full view from below) and
    # left out hair that faces sideways. Now: (1) the skin carries no metal at all; (2) every fringe texel
    # takes her helmet's paint at the same place ROUND the head (the angle from the front's middle and the height),
    # not at the same place seen from the front
    hx = 0.02                                                    # the head's upright axis (x; y = 0)
    cyl = lambda q: np.stack([np.arctan2(np.abs(q[:, 1]), q[:, 0] - hx) * 0.14, q[:, 2]], 1)
    outw = lambda P, N: ((P[..., 0] - hx) * N[..., 0] + P[..., 1] * N[..., 1]) / np.maximum(np.hypot(P[..., 0] - hx, P[..., 1]), 1e-6)
    bsrc = (E["helmet"] | E["brow"]) & R.covered & (R.edge >= 1.5 * K) & (R.pos[..., 2] < BAND_TOP) & (outw(R.pos, R.nrm) > 0.1)
    # (user, on that pass: "the metal part still bled into the hair left and right [the side locks beside the eyes], but
    # the almond shape I redded [two strand faces crossing the band] should get the silver metal texture continued from
    # the eye sigil on her forehead that is no longer hair (illusion)". So the band is on the fringe alone (island
    # 90,174: not the side locks, not the back hair), and on EVERY face of it there, whichever way it points: the
    # strands' side and under faces carry the band on, so it reads as one piece of metal, not hair with paint on it)
    bdst = m((90, 174)) & M.covered & (Z > 1.47)
    # her outermost layer alone, per 4 mm cell of the map round the head (picking the outermost of the nearest few
    # flipped from texel to texel where her helmet and its brow piece overlap: dark specks round the disc's ring)
    sp_, q_ = R.pos[bsrc], M.pos[bdst] + [0, 0, BAND_DROP]
    by_, bx_ = np.where(bsrc)
    cs_, rad_ = cyl(sp_), np.hypot(sp_[:, 0] - hx, sp_[:, 1])
    cell = np.floor(cs_ / 0.004).astype(int); cell -= cell.min(0)
    buf = np.full(cell.max(0) + 1, -9.0)
    np.maximum.at(buf, (cell[:, 0], cell[:, 1]), rad_)
    top_ = rad_ >= ndimage.maximum_filter(buf, 3)[cell[:, 0], cell[:, 1]] - 0.008
    sp_, by_, bx_ = sp_[top_], by_[top_], bx_[top_]
    d_, j_ = cKDTree(cyl(sp_)).query(cyl(q_))
    ang = np.degrees(np.arctan2(np.abs(q_[:, 1]), q_[:, 0] - hx))
    wb = ((1 - sstep(d_, 0.005, 0.010)) * (1 - sstep(ang, BAND_ROUND - 12, BAND_ROUND)))[:, None]
    J.o[bdst] = J.o[bdst] * (1 - wb) + fine(R, by_[j_], bx_[j_], cyl(q_) - cyl(sp_[j_]), cyl) * wb
    on_ = wb[:, 0] > 0.5
    print(f"helmet band on the fringe: {int(on_.sum())} of {int(bdst.sum())} texels, z {q_[on_][:, 2].min():.3f}..{q_[on_][:, 2].max():.3f}, to {ang[on_].max():.0f} deg round; apart median {np.median(d_[on_]) * 100:.1f} cm")
    # --- borrowed, part from part (skin-tight on the same body, and the flat wings)
    J.take(m((149, 320)), E["legs"] | E["boot"] | E["bootcuff"] | E["hips"], "legs", absy=True)
    J.take(m((99, 457), (18, 446), (67, 421), (52, 444), (148, 470), (189, 478)), E["foot"] | E["sole"] | E["boot"], "feet", absy=True)
    J.take(m((402, 422), (246, 409)), E["wing"], "wings", absy=True)
    # --- the sleeves: the enemy's rings, read along the arm (its sleeve's median colour per 2 mm of |y|)
    sl = E["sleeve"] & R.covered & (R.edge > 2)
    ry = np.abs(R.pos[..., 1][sl])
    bins = np.arange(ry.min(), ry.max(), 0.002)
    idx = np.clip(np.digitize(ry, bins) - 1, 0, len(bins) - 1)
    prof = np.array([np.median(R.rgb[sl][idx == i], 0) if (idx == i).any() else [0, 0, 0] for i in range(len(bins))])
    sleeves = m((361, 125), (255, 333), (340, 223), (329, 90))
    ring_ = np.stack([np.interp(Y, bins + 0.001, ndimage.gaussian_filter1d(prof[:, c], 0.6)) for c in range(3)], -1)      # (between the profile's 2 mm steps: they notched the stripes' edges)
    J.o[sleeves] = (ring_ * (0.90 + 0.20 * J.form)[..., None])[sleeves]
    cloth_shade(J, sleeves, J.m((149, 320)) & (Z > 0.19))
    # --- the head piece: the bug set's hood as the helmet: its own paint (wing cells and veins) in the dress's purple,
    # the bright cells the helmet's pale ornaments
    him = Image.open(DATA / "props" / "tex" / "Bat_butterflyHood.png").convert("RGB")
    ha = np.asarray(him.resize((him.width * 4, him.height * 4), Image.LANCZOS)).astype(float)
    hl = ndimage.gaussian_filter(ha @ LUM / 255, 1.0)
    hc = np.array([dress[0] * 0.8, dress[1], dress[2] * 1.15, trim[1], trim[2]])
    hood = np.stack([np.interp(hl, [0.0, 0.12, 0.38, 0.62, 0.9], hc[:, i]) for i in range(3)], -1)
    d = J.out / "look"
    d.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.dstack([np.clip(hood, 0, 255), np.full(hood.shape[:2], 255.0)]).astype(np.uint8), "RGBA").save(d / "Bat_butterflyHood.png")
    J.extra[f"{CLS}|accessories|butterflyHood|Bat_butterflyHood.png"] = d / "Bat_butterflyHood.png"
    eye_makeup(J, head, 11)
    return J, dict(head="butterflyHood", face=11, ref_tile=4)   # face 11 (user: "face 11 looks more like her"; a first pick: 4)


def rose(arms="lace"):
    """The white-haired one, on summer. arms: both arms read the same texels (checked on the mesh: every arm texel has
    a triangle at +y and one at -y), so her one striped sleeve cannot be on one arm: "sleeve" = the striped sleeve and
    its cuff on both, "mix" = stripes to the elbow, her lace glove below, "lace" = the glove on both (the first pass)."""
    J = Job("rose", "summer", "BatCult")
    M, R, r, m = J.M, J.R, J.r, J.m
    e = dict(face=(62, 62), collar=(474, 15), neck=(419, 15), hairB=(179, 80), torsoF=(340, 114), torsoB=(456, 123), sleeve=(250, 229),
             skirt=(441, 275), stock=(149, 273), arm=(270, 321), legw=(144, 367), strap=(497, 370), rose=(85, 389), foot=(87, 448), sole=(18, 446))
    E = {k: r(v) for k, v in e.items()}
    # --- same layout: the enemy's own paint (hair back and side, ears, hand, palm, wings, tail)
    for seeds in ((263, 45), (179, 78), (21, 253), (66, 252), (63, 328), (20, 385), (402, 422), (246, 409), (136, 497), (314, 491)):
        J.same(m(seeds))
    # --- own paint, the enemy's colours: the face (under face preset 21's eyes), summer's own fringe and side lock
    head = m((62, 62))
    J.own(head, palette(R.rgb, E["face"], (6, 62, 96)), k=0.9)
    xx, yy = face_marks(J, head)
    dm = np.abs(xx - 37.5) / 3.2 + np.abs(yy - 64.5) / 4.6                 # the small diamond under her right eye
    J.mix(head, hexv("#b9529f"), 1 - sstep(dm, 0.8, 1.1))
    J.own(m((135, 173), (61, 170)), palette(R.rgb, E["hairB"], (10, 55, 95)), lo=1)
    # --- borrowed, part from part (the same bare body under both)
    J.take(m((360, 102)), E["torsoF"], "torso front")
    J.take(m((461, 112)), E["torsoB"], "torso back")
    # the strap from the top's middle down to the belt, and the one down the back (user, circling it: "add these
    # details"): pieces standing 1-2 cm off the body, one strip of the sheet for both; the nearest-point borrow never
    # reached them (the skin under them is nearer)
    J.lay(m((360, 102)), (487, 331, 508, 411), "strap front", side=1, to_z=STRAP_TO)
    J.lay(m((461, 112)), (487, 331, 508, 411), "strap back", side=-1, to_z=STRAP_TO)
    J.take(m((490, 15)), E["neck"] | E["collar"], "neck")
    J.take(m((297, 204)), E["collar"], "necklace")
    arm = m((270, 321))
    J.take(arm, E["arm"], "arms", absy=True)
    if arms != "lace":                                          # user 2026-11-13, circling the sleeve on the reference
        J.take(arm & (np.abs(M.pos[..., 1]) < (9 if arms == "sleeve" else 0.40)), E["sleeve"], "sleeve", absy=True)
    J.take(m((227, 216)), E["sleeve"], "bracelet", absy=True)
    J.take(m((148, 327)), E["stock"] | E["legw"] | E["torsoF"] | E["torsoB"], "legs", absy=True)
    # the hip cloth: her skirt's paint read at the mirror place (user 2026-11-13: "you may invert the pattern from the ref
    # left and right and I think the eye sigil from the ref should align nicely there"): her skirt hangs from her left
    # hip, summer's cloth from the right. Read unmirrored, the cloth lay 9-18 cm from the skirt and its paint was scraps
    J.take(m((468, 300)), E["skirt"], "hip cloth", inset=HIP_INSET, flip=True)
    J.take(m((300, 128), (255, 133), (236, 165), (271, 269), (88, 427), (37, 445), (96, 459)), E["foot"] | E["sole"] | E["legw"], "feet", absy=True)
    # --- the flower on the hip: the enemy's rose (its picture laid over the flower's own box)
    for seed in ((380, 282), (411, 234)):
        fl = m(seed) & M.covered
        ys, xs = np.where(fl)
        sy, sx = np.where(E["rose"] & R.covered)
        u, v = (xs - xs.min()) / max(np.ptp(xs), 1), (ys - ys.min()) / max(np.ptp(ys), 1)
        J.o[ys, xs] = R.rgb[(sy.min() + v * np.ptp(sy)).astype(int), (sx.min() + u * np.ptp(sx)).astype(int)]
    for seed in ((388, 225), (484, 442)):
        J.own(m(seed), palette(R.rgb, E["skirt"], (5, 30, 60)))
    # --- whiter hair (user: "bat cult need a brighter whiter hair"): her texture's white reads grey under the page's light
    hairs = m((179, 78), (263, 45), (135, 173), (61, 170))
    J.o[hairs] = (255 * (J.o[hairs] / 255) ** HAIR_GAMMA)
    # --- the rose in her hair (user, circling it; and "remove the headpiece"): her rose is a piece of its own before
    # her left ear; no head piece of the five sets is one, so it is painted flat on the hair there: the rose's
    # picture from the enemy's sheet, on the hair texels within ROSE_R of its place, facing the same way
    c, n = ROSE_AT, np.array([0.05, 0.87, 0.46]) / np.linalg.norm([0.05, 0.87, 0.46])
    t1 = np.cross(n, [0, 0, 1.0]); t1 /= np.linalg.norm(t1)
    t2 = np.cross(t1, n)
    off = M.pos - c
    a, b, dep = off @ t1, off @ t2, off @ n
    rr = np.hypot(a, b) / ROSE_R
    on = hairs & (rr < 1) & (np.abs(dep) < 0.05) & (M.nrm @ n > 0.2) & (M.pos[..., 1] > 0)
    sy, sx = np.where(E["rose"] & R.covered)
    py = (sy.min() + (0.5 - b / (2 * ROSE_R)).clip(0, 1) * np.ptp(sy)).astype(int)
    px = (sx.min() + (0.5 + a / (2 * ROSE_R)).clip(0, 1) * np.ptp(sx)).astype(int)
    J.mix(on, R.rgb[py, px], 1.0)
    J.mix(on, hexv("#3a0b0d"), sstep(rr, 0.86, 0.98) * 0.8)                 # a dark rim: it stands out from the white hair
    print(f"rose on the hair: {int((on & M.covered).sum())} texels")
    return J, dict(head=None, face=21, ref_tile=2)


def arm_variants():
    """The second skin's arms, side by side for the user to pick: sleeve | mix | lace, front and three-quarter."""
    out, vs = BASE / "rose", []
    for a in ("sleeve", "mix", "lace"):
        J, look = rose(a)
        f = out / "look" / f"summer_{a}.png"
        Image.fromarray(np.dstack([np.clip(J.o, 0, 255), np.full(J.o.shape[:2], 255.0)]).astype(np.uint8), "RGBA").save(f)
        vs.append((f"arms_{a}", {f"{CLS}|outfits|summer|": f}, {}))
    asyncio.run(shots(CLS, "summer", vs, out, yaws=((0, "000"), (315, "315")), size=800, face=look["face"]))
    sheet = Image.new("RGB", (800 * 3, 800 * 2))
    for i, (n, _, _) in enumerate(vs):
        for j, y in enumerate(("000", "315")):
            sheet.paste(Image.open(out / "shots" / f"{n}_{y}.png"), (800 * i, 800 * j))
    sheet.save(out / "arms.png")
    print(out / "arms.png")


def coat_back(J, coat, dress, R, E):
    """The coat's back, an original design in her theme (user 2026-11-13, of a band across it: "I found a forced
    painting ... please design this according to the theme of this character, your own designs and give me several
    mock variants, no forced repaint"). The band was royal's own belt, kept in the coat's re-coloured shading, and her
    skirt read over it. Here the back (back-facing coat texels) gets a clean cloth (shaded by the body's form and soft
    drape folds, not royal's paint), then one of the designs below, drawn in her own colours: her lilac-white for the
    sigils, her silver for lines, a dark magenta for the flowing contour lines of her wings. Both halves of the coat
    share their texels, so every design is mirror-symmetric about the back's middle."""
    M = J.M
    Y, Z, nx = np.abs(M.pos[..., 1]), M.pos[..., 2], M.nrm[..., 0]
    back = coat & (nx < -0.05)
    w = sstep(-nx, 0.05, 0.35)                                   # 1 on the back, fading at the sides
    from wardrobe_bat_robe import folds
    drape = folds(Y, Z, 0.045, 7, long=7.0) * sstep(1.02 - Z, 0.0, 0.25)
    cloth = dress[1] * (0.82 + 0.30 * J.form + 0.10 * drape)[..., None]
    J.mix(back, cloth, w)
    white = np.array([232.0, 222, 240])
    silver = np.array([200.0, 204, 208])
    dark = dress[0] * 0.45
    mag = np.array([120.0, 40, 90])
    ins = lambda d, aa=0.0015: 1 - sstep(d, -aa, aa)
    def eye(cz, hw, hh, wb=1.0):                                 # her wing's eye: an almond outline, a ring iris, a dot
        u, v = Y / hw, (Z - cz) / hh
        alm = np.abs(v) - (1 - np.minimum(u, 1.2) ** 2) * (u < 1)  # < 0 inside the almond
        alm = np.where(u < 1, alm, 1.0)
        r = np.hypot(Y, Z - cz)
        J.mix(back, dark, ins(np.abs(alm) - 0.16 * wb, 0.03) * w * 0.85)
        J.mix(back, white, ins(np.abs(alm) - 0.085 * wb, 0.025) * w)
        J.mix(back, dark, ins(r - hh * 0.80) * (alm < 0) * w * 0.6)
        J.mix(back, white, ins(np.abs(r - hh * 0.60) - hh * 0.12) * w)
        J.mix(back, white, ins(r - hh * 0.26) * w)
    # Placed by the back's own shape (measured 2026-11-14): royal's belt (island 33) lies across it at z 0.55 .. 0.64;
    # above it the back runs up to the hair and the capelet (z ~1.05; 48 cm wide at the belt, 24 at the top), below it
    # the skirt is short at the middle (to z 0.40) and long in its spikes (to 0.27 at |y| 0.15, 0.20 at the outer tails)
    def contours(cz, k=0.75):                                   # her wings' flowing lines, in rings round (0, cz)
        r = np.hypot(Y / 1.5, Z - cz)
        wav = r + 0.014 * np.sin(Y * 45 + Z * 20)
        lines = ins(np.abs(((wav / 0.036) % 1) - 0.5) * 0.036 - 0.0040, 0.0015) * sstep(wav, 0.115, 0.13)
        J.mix(back, mag, lines * w * k)
    if COAT_BACK == "panel":
        # Her own back design, copied whole (user 2026-11-14, of my four designs: "Why do you hesitate to copy the back
        # design from the reference image?"; the "forced painting" of 2026-11-13 was one stray strip of it, read at its
        # own place within 1.5 cm, not the design). Her back panel (the pointed tabard: silver border, the vine with
        # its curls and two pale leaves, the diamond) laid on the middle of the coat's back as one piece, her paint
        # inside its own outline (read between her texels from the sharp sheet: fine), PANEL_WIDE x as wide as hers,
        # from its top at her own height down to PANEL_TO.
        # Outside the outline: the coat's clean cloth, a soft shade along the panel's edge.
        # Above the panel, her dress's own back (the emblem between the shoulders) at its own place.
        src = E["backp"] & R.covered & (R.nrm[..., 0] < -0.3) & (R.edge >= 1.5 * K)
        sp = np.stack([np.abs(R.pos[..., 1][src]), R.pos[..., 2][src]], 1)
        sy_, sx_ = np.where(src)
        kyz = lambda q: np.stack([np.abs(q[:, 1]), q[:, 2]], 1)
        # (user, of the panel's point under the belt, seen from straight behind: "please fix so doesn't look like it is
        # clipping". Under the belt the coat's back is a few large triangles, each half skinned to its own leg (the
        # middle's vertices to both thighs): in the idle pose the halves shear and cross near the middle, so a shape
        # drawn across the middle there is cut on one side. Nothing is drawn there now: the whole panel, smaller,
        # ends with its point on the belt (PANEL_TO), and the skirt under the belt is plain cloth)
        zt, zh, zc = float(sp[:, 1].max()), float(sp[:, 1].min()), PANEL_TO
        zq = zt - (zt - Z) * (zt - zh) / (zt - zc)
        ys_, xs_ = np.where(back)
        qk = np.stack([Y[ys_, xs_] / PANEL_WIDE, zq[ys_, xs_]], 1)
        d, j = cKDTree(sp).query(qk)
        scj = fine(R, sy_[j], sx_[j], qk - sp[j], kyz)
        k_in = (1 - sstep(d, 0.0025, 0.0045))[:, None]
        shade = (1 - sstep(d, 0.004, 0.016))[:, None] * 0.45 * (d[:, None] > 0.0035)
        base = J.o[ys_, xs_] * (1 - shade) + dark * shade
        J.o[ys_, xs_] = base * (1 - k_in) + scj * (0.90 + 0.20 * J.form[ys_, xs_])[:, None] * k_in
        up = back & M.covered & (Z > zt - 0.01)
        strokes(J, up, E["bodice"] & (R.nrm[..., 0] < -0.3), lambda q: np.stack([np.abs(q[:, 1]), q[:, 2]], 1), "coat back, top", inset=3,
                k=1 - sstep(Y, 0.060, 0.085))                    # the emblem between the shoulders alone: beside it her dress's lines came as stray hooks
        print(f"her back panel on the coat: {int((d < 0.003).sum())} texels, her z {zh:.2f}..{zt:.2f} -> {zc:.2f}..{zt:.2f}, {PANEL_WIDE} x her width (half-width {sp[:, 0].max() * PANEL_WIDE * 100:.0f} cm)")
    elif COAT_BACK == "eye":                                    # A: one large eye on the upper back, as on her wings
        eye(0.83, 0.17, 0.095)
    elif COAT_BACK == "wing":                                    # B: the back as a wing: the eye and its flowing lines over the whole back
        contours(0.83)
        eye(0.83, 0.17, 0.095)
    elif COAT_BACK == "spine":                                   # C: a silver scroll up the middle with leaves, a diamond under the belt
        J.mix(back, dark, ins(Y - 0.012) * sstep(Z, 0.66, 0.69) * (Z < 1.03) * w * 0.8)
        J.mix(back, silver, ins(Y - 0.0065) * sstep(Z, 0.66, 0.69) * (Z < 1.03) * w)
        for cy in (0.96, 0.85, 0.74):
            curl = np.abs(np.hypot(Y - 0.050, Z - cy) - 0.040) - 0.0050
            J.mix(back, silver, ins(curl) * (Z > cy - 0.006) * (Y < 0.090) * w)
            leaf = np.hypot((Y - 0.105) / 0.020, (Z - cy + 0.006) / 0.034) - 1
            J.mix(back, dark, ins(leaf * 0.02 - 0.003) * w * 0.7)
            J.mix(back, white, ins(leaf * 0.02) * w)
        dia = Y / 0.040 + np.abs(Z - 0.475) / 0.060 - 1
        J.mix(back, dark, ins(dia * 0.03 - 0.004) * w * 0.8)
        J.mix(back, silver, ins(np.abs(dia) * 0.03 - 0.0045) * w)
        J.mix(back, white, ins(np.hypot(Y, Z - 0.475) - 0.013) * w)
    elif COAT_BACK == "hem":                                     # D: ring sigils on the skirt under the belt, a scroll band over it
        for cy, cz, rr_ in ((0.0, 0.475, 0.042), (0.155, 0.41, 0.052), (0.295, 0.40, 0.052)):
            r = np.hypot(Y - cy, Z - cz) / rr_
            J.mix(back, dark, ins((r - 1.0) * rr_) * w * 0.75)
            J.mix(back, white, ins((np.abs(r - 0.81) - 0.10) * rr_) * w)
            J.mix(back, white, ins((np.abs(r - 0.46) - 0.08) * rr_) * w)
            J.mix(back, white, ins((r - 0.17) * rr_) * w)
        band = Z - (0.74 + 0.30 * Y ** 2)
        J.mix(back, silver, ins(np.abs(band) - 0.0045) * w * (Y < 0.30))
        J.mix(back, mag * 1.25, ins(np.abs(band - 0.022 + 0.014 * np.sin(Y * 70)) - 0.0030) * w * (Y < 0.30))
    print(f"coat back: design {COAT_BACK}, {int((back & M.covered).sum())} texels")


def belt(J, strip, silver, pal):
    """Royal's own belt, island 33 (sheet 499,425): a strip round the coat's back at hip height, zigzagging over the
    coat's folds, from under the front pieces to the back's middle (both halves share its texels: the back's middle is
    its end, a mirror seam). User 2026-11-14, of it: "textured belt with dark red as the main color can be quite a good
    contrast for the lower body" (a first set of mocks, 2026-11-13, went round the coat at z 0.84: the wrong piece).
    Laid out by the strip's own shape: s = the way along it (body units, from the back's middle), v = across it (0 its
    top edge .. 1 its bottom, from its rows in the sheet). Each design is a height field, shaded as relief lit from
    above, in the red of her wings' edges, with silver piping along both edges and a fine leather grain. Original:
      tooled  a running vine with leaves pressed into the leather
      braid   a plait of rounded strands (chevrons)
      studs   plain leather, a row of silver studs, an eye clasp at the back's middle (her wings' eye)
      scales  overlapping round scales, two rows
      weave   a diagonal basket weave
    and Claude's own (user 2026-11-14: "all these variants are from my dark red suggestions, come up with your own design
    too"), in her other colours (pal: her dress's purples, her sleeves' stripe tones, her wings' magenta lines, her
    eyes' lilac-white):
      eyes     dark purple leather, a row of small eyes (silver almond, lilac-white iris) with a silver diamond between
      chain    near-black leather, a silver chain of oval links along its middle
      stripes  slanted stripes in her sleeves' and stockings' tones (a chevron at the back's middle)
      contour  dark purple with her wings' flowing magenta contour lines, a small eye at the back's middle
      lattice  a pale silver-lilac band with a dark purple diamond lattice, a dot in each diamond"""
    M = J.M
    H, W = M.lab.shape
    cov = strip & M.covered
    rows = np.where(cov.any(1))[0]
    c = np.array([M.pos[r][cov[r]].mean(0) for r in rows])
    c[:, 1] = np.abs(c[:, 1])
    s_row = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(c, axis=0), axis=1))])
    if c[-1, 1] < c[0, 1]:
        s_row = s_row[-1] - s_row                                   # 0 at the back's middle (|y| ~ 0)
    lo = np.array([np.where(cov[r])[0].min() for r in rows], float)
    hi = np.array([np.where(cov[r])[0].max() for r in rows], float)
    yy, xx = np.mgrid[0:H, 0:W]
    ri = np.clip(np.searchsorted(rows, yy), 0, len(rows) - 1)
    s = np.where(strip, s_row[ri], 0.0)
    v = np.where(strip, (xx - lo[ri] + 0.5) / (hi[ri] - lo[ri] + 1.0), 0.5)
    flip = np.median(M.pos[..., 2][cov & (v < 0.3)]) < np.median(M.pos[..., 2][cov & (v > 0.7)])
    if flip:
        v = 1 - v                                                   # v = 0 at the top edge
    wd = 0.040                                                      # the belt's width, body units (measured 2.7 .. 5.1 cm)
    u, vi = s / wd, (v - 0.17) / 0.66                               # along in belt widths; across the inner band 0..1
    inner = (vi > 0) & (vi < 1)
    red = [np.array(x) for x in ((50.0, 8, 19), (116.0, 20, 40), (182.0, 56, 76))]
    base, grain_k = red, 0.05                                       # the leather's ramp (shadow, base, light)
    purple = [pal["dress"][0] * 0.55, pal["dress"][0] * 1.05, pal["dress"][1] * 1.25]
    white = pal["white"]
    ins = lambda d, aa=0.04: 1 - sstep(d, -aa, aa)                  # inside a shape (d < 0), soft by aa (in vi / u units)
    def small_eye(cu, hl, hh):                                      # an eye centred at u = cu: almond outline, iris ring, pupil
        du, dv = (u - cu) / hl, (vi - 0.5) / hh
        al = np.where(np.abs(du) < 1, np.abs(dv) - (1 - np.minimum(np.abs(du), 1) ** 2), 1.0)
        rr = np.hypot((u - cu) * 0.66, (vi - 0.5) * 0.66) / (hh * 0.66)
        extra.append((ins(al - 0.30, 0.08) * 0.85, purple[0] * 0.6))
        extra.append((ins(np.abs(al) - 0.14, 0.07), ramp3(np.full((H, W), 0.8), silver)))
        extra.append((ins(rr - 0.62, 0.08) * (al < -0.1), white))
        extra.append((ins(rr - 0.30, 0.08), purple[0] * 0.5))
    h = np.zeros((H, W))
    extra = []                                                      # (weight, colour) laid over the leather
    if BELT == "tooled":
        P = 1.8
        vc = 0.5 + 0.26 * np.sin(2 * np.pi * u / P)
        stem = np.exp(-((vi - vc) / 0.09) ** 2)
        ph = (u / P) % 1
        lf = np.zeros_like(u)
        for p0, side in ((0.25, -1), (0.75, 1)):                    # a leaf at each crest, on its outer side
            du, dv = (ph - p0) * P, vi - (0.5 - side * 0.26) + side * 0.20
            lf = np.maximum(lf, 1 - np.hypot(du / 0.34, dv / 0.15))
        for p0, side in ((0.0, 1), (0.5, -1)):                      # a curl where the vine crosses the middle
            dp = (ph - p0 + 0.5) % 1 - 0.5
            r = np.hypot(dp * P / 0.9, (vi - 0.5 - side * 0.22) / 0.42)
            lf = np.maximum(lf, np.exp(-((r - 0.30) / 0.10) ** 2) * 0.8 * (r < 0.5))
        h = np.maximum(stem, lf.clip(0, 1) ** 0.5)
    elif BELT == "braid":
        w = (u / 0.55 + np.abs(vi - 0.5) * 1.15) % 1
        h = np.sin(np.pi * w) ** 0.7 * (0.85 + 0.15 * np.sign(vi - 0.5))
    elif BELT == "studs":
        h = 0.5 + 0.08 * np.sin(np.pi * vi)
        f = (u / 0.62) % 1
        du = np.minimum(f, 1 - f) * 0.62
        sd = np.hypot(du, (vi - 0.5) * 0.66)
        clasp = u < 0.62
        dome = np.clip(1 - sd / 0.13, 0, 1)
        extra.append((((sd > 0.13) & (sd < 0.17) & ~clasp) * 0.7, red[0] * 0.5))
        extra.append((((sd < 0.13) & ~clasp) * 1.0, ramp3(0.25 + 0.75 * dome ** 0.6, silver)))
        uu, vv = u / 0.50, (vi - 0.5) * 0.66 / 0.30                 # the clasp's almond: half-length 0.5 widths, half-height 0.3
        al = np.where(uu < 1, np.abs(vv) - (1 - np.minimum(uu, 1) ** 2), 1.0)       # < 0 inside
        r = np.hypot(u * wd, (vi - 0.5) * 0.66 * wd)
        extra.append(((al < 0.10) * 1.0, red[0] * 0.45))
        extra.append(((np.abs(al) < 0.07) * 1.0, ramp3(np.full((H, W), 0.85), silver)))
        extra.append((((al < -0.07) & (r < 0.0075)) * 1.0, np.array([232.0, 222, 240])))
        extra.append(((r < 0.0040) * 1.0, red[0] * 0.6))
    elif BELT == "scales":
        hs = 0.42
        best = np.full((H, W), 9.0)
        for row, off in ((0, 0.0), (1, 0.5)):
            cv_ = 0.27 + 0.46 * row
            b0 = np.round(u / hs - off)
            for dk in (-1, 0, 1):
                cu = (b0 + dk + off) * hs
                d = np.hypot((u - cu) / (hs * 0.62), (vi - cv_) / 0.34)
                best = np.where(d < 1, np.minimum(best, d), best)
        h = np.clip(1 - best, 0, 1) ** 0.6
    elif BELT == "weave":
        cw = 0.36
        a_, b_ = (u + vi * 0.66) / cw, (u - vi * 0.66) / cw
        over = (np.floor(a_) + np.floor(b_)) % 2 == 0
        fa, fb = a_ % 1, b_ % 1
        h = np.where(over, np.sin(np.pi * fb) ** 0.5 * 0.9 + 0.1, np.sin(np.pi * fa) ** 0.5 * 0.7)
        h *= 0.55 + 0.45 * np.minimum(np.minimum(fa, 1 - fa), np.minimum(fb, 1 - fb)) * 2
    elif BELT == "eyes":
        base = purple
        h = 0.5 + 0.1 * np.sin(np.pi * vi)
        P = 1.25                                                    # an eye every P widths, one centred on the back's middle
        k = np.round(u / P)
        small_eye(k * P, 0.46, 0.40)
        dd = np.abs(u - (k + 0.5 * np.sign(u - k * P + 1e-9)) * P) / 0.13 + np.abs(vi - 0.5) / 0.20 - 1      # the diamond between
        extra.append((ins(dd, 0.15) * (np.abs(u - k * P) > 0.5), ramp3(np.full((H, W), 0.7), silver)))
    elif BELT == "chain":
        base = [pal["stripe_dark"] * 0.6, pal["stripe_dark"] * 1.0, pal["stripe_dark"] * 1.6]
        h = 0.5 + 0.06 * np.sin(np.pi * vi)
        L_ = 0.70                                                   # one link face-on and one edge-on per L_ widths
        f = u / L_ - np.floor(u / L_)
        du = (f - 0.5) * L_
        ring = np.abs(np.hypot(du / 0.24, (vi - 0.5) / 0.30) - 1) - 0.22
        bar = np.maximum(np.abs((np.minimum(f, 1 - f)) * L_) - 0.13, np.abs(vi - 0.5) - 0.07)
        extra.append((ins(np.minimum(ring, bar / 0.3) - 0.12, 0.10) * 0.8, base[0] * 0.5))          # its shadow
        shine = 0.45 + 0.5 * np.clip(0.5 - (vi - 0.5) * 1.6, 0, 1)
        extra.append((ins(ring, 0.08), ramp3(shine, silver)))
        extra.append((ins(bar / 0.3, 0.08) * (np.abs(du) > 0.22), ramp3(shine + 0.1, silver)))
    elif BELT == "stripes":
        base = [pal["stripe_dark"] * 0.7, pal["stripe_dark"], pal["stripe_dark"] * 1.4]
        q = (u + np.abs(vi - 0.5) * 0.0 + vi * 0.66 * 0.8) / 0.42
        band = np.abs((q % 1) - 0.5) - 0.22                         # < 0 on a light stripe
        h = 0.5 + 0.25 * np.cos(2 * np.pi * q)
        extra.append((ins(band, 0.05), ramp3(0.42 + 0.3 * (0.5 - vi) + 0.4 * (h - 0.5), [pal["stripe_blue"] * 0.7, pal["stripe_blue"], pal["stripe_blue"] * 1.35])))
    elif BELT == "contour":
        base = purple
        h = 0.5 + 0.08 * np.sin(np.pi * vi)
        for i, c0 in enumerate((0.22, 0.5, 0.78)):
            wv = vi - c0 - 0.11 * np.sin(2 * np.pi * u / (1.6 + 0.3 * i) + i * 1.7)
            extra.append((ins(np.abs(wv) - 0.05, 0.03) * sstep(u, 0.55, 0.8), np.minimum(pal["mag"] * 2.0, 255)))
        small_eye(0.0, 0.50, 0.42)
    elif BELT == "lattice":
        base = [silver[0] * 0.55 + pal["white"] * 0.0, silver[0] * 0.75 + pal["white"] * 0.2, pal["white"]]
        cw = 0.56
        a_, b_ = (u + vi * 0.66) / cw, (u - vi * 0.66) / cw
        line = np.minimum(np.abs(a_ - np.round(a_)), np.abs(b_ - np.round(b_)))       # 0 on a lattice line .. 0.5 mid-diamond
        h = 0.5 + 0.5 * np.minimum(line * 2, 1)
        extra.append((ins(line - 0.05, 0.025), purple[0] * 0.9))
        ca, cb = np.floor(a_) + 0.5, np.floor(b_) + 0.5
        dot = np.hypot(a_ - ca, b_ - cb)
        extra.append((ins(dot - 0.11, 0.04), purple[1] * 1.1))
        grain_k = 0.025
    h = np.where(inner, h, 0.0)
    hs_ = ndimage.gaussian_filter(h, 0.6)
    gv = np.gradient(hs_, axis=1) * (-1 if flip else 1)            # along v (v grows with the sheet x unless flipped)
    light = -gv * 2.2 - np.gradient(hs_, axis=0) * 0.5              # lit from the top edge
    rng = np.random.default_rng(7)
    grain = ndimage.gaussian_filter(rng.normal(0, 1, (H, W)), 0.7) * grain_k
    t = 0.40 + 0.20 * hs_ + 1.3 * light + grain + 0.10 * (0.5 - v)
    J.o[strip] = ramp3(t, base)[strip]
    for k, col in extra:
        J.mix(strip, col, k)
    # piping: a silver cord along each edge, a dark line between it and the leather, the very edge in shade
    for e in (v, 1 - v):
        cord = np.clip(1 - np.abs(e - 0.085) / 0.055, 0, 1)
        J.mix(strip, base[0] * 0.45, (np.abs(e - 0.155) < 0.03) * 0.9)
        J.mix(strip, ramp3(0.3 + 0.7 * cord ** 0.7, silver), (cord > 0) * 1.0)
        J.mix(strip, base[0] * 0.4, (e < 0.025) * 0.8)
    print(f"belt: {BELT} on island 33, {s_row.max() * 100:.0f} cm from the back's middle to its end, {int(cov.sum())} texels")


def back_variants(which="backs"):
    """Designs side by side for the user to pick: "backs" = the coat's back (eyes/back_variants.png), "belts" = the dark
    red belt, three textures, and one with the back's eye under it (eyes/belt_variants.png: back, back three-quarter, front)."""
    global COAT_BACK, BELT
    out, vs = BASE / "eyes", []
    sets = {"backs": (("panel", "her back panel, copied whole", "panel", BELT), ("plain", "plain cloth", "plain", BELT), ("eye", "A  one large eye", "eye", BELT), ("wing", "B  the back as a wing: eye + flowing lines", "wing", BELT),
                      ("spine", "C  silver scroll spine + diamond", "spine", BELT), ("hem", "D  ring sigils on the skirt, a scroll band", "hem", BELT)),
            "belts": (("tooled", "I  tooled vine", "ref", "tooled"), ("braid", "J  braid", "ref", "braid"),
                      ("studs", "K  studs + eye clasp", "ref", "studs"), ("scales", "L  scales", "ref", "scales"), ("weave", "M  basket weave", "ref", "weave"),
                      ("eyes", "N  eyes + diamonds", "ref", "eyes"), ("chain", "O  silver chain", "ref", "chain"), ("stripes", "P  her stripes", "ref", "stripes"),
                      ("contour", "Q  wing contour lines", "ref", "contour"), ("lattice", "R  silver lattice", "ref", "lattice"))}[which]
    keep = COAT_BACK, BELT
    for key, _, cb, bl in sets:
        COAT_BACK, BELT = cb, bl
        J, look = eyes()
        f = out / "look" / f"royal_{which[:-1]}_{key}.png"
        Image.fromarray(np.dstack([np.clip(J.o, 0, 255), np.full(J.o.shape[:2], 255.0)]).astype(np.uint8), "RGBA").save(f)
        vs.append((f"{which[:-1]}_{key}", {f"{CLS}|outfits|royal|": f, **J.extra}, {"Head": look["head"]}))
    COAT_BACK, BELT = keep
    # the sheets: wardrobe_skin_views.py --per-job (8 sides, full body), a sheet per design
    for _, f_, _ in vs:
        print(list(f_.values())[0])


def run(fn, noshots):
    J, look = fn()
    f = J.save()
    print(J.name, "->", f.relative_to(ROOT), f"{f.stat().st_size / 1e6:.1f} MB")
    if noshots:
        return
    skins = {f"{CLS}|outfits|{J.outfit}|": f, **J.extra}
    yaws = tuple((y, f"{y:03d}") for y in range(0, 360, 45))
    asyncio.run(shots(CLS, J.outfit, [("look", skins, {"Head": look["head"]})], J.out, yaws=yaws, size=800, face=look["face"]))
    if not (J.out / "shots" / "orig_000.png").exists():
        asyncio.run(shots(CLS, J.outfit, [("orig", {}, {})], J.out, yaws=yaws[:1], size=800))
    sheet = Image.new("RGB", (800 * 4, 800 * 2))
    for i, (_, s) in enumerate(yaws):
        sheet.paste(Image.open(J.out / "shots" / f"look_{s}.png"), ((i % 4) * 800, (i // 4) * 800))
    sheet.save(J.out / "sheet.png")
    ref = Image.open(BASE / "ref" / f"{J.R_name if hasattr(J, 'R_name') else ('LadyNoir' if J.name == 'eyes' else 'BatCult')}_sheet.png")
    t = look["ref_tile"]
    tile = ref.crop(((t % 4) * 700, 30 + (t // 4) * 900, (t % 4) * 700 + 700, 30 + (t // 4) * 900 + 900)).resize((622, 800), Image.LANCZOS)
    cmp_ = Image.new("RGB", (800 * 2 + 622, 800), (230, 225, 216))
    cmp_.paste(Image.open(J.out / "shots" / "orig_000.png"), (0, 0)); cmp_.paste(Image.open(J.out / "shots" / "look_000.png"), (800, 0)); cmp_.paste(tile, (1600, 0))
    cmp_.save(J.out / "compare.png")
    print(J.out / "sheet.png")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    for name, fn in (("eyes", eyes), ("rose", rose)):
        if which in (name, "both"):
            run(fn, "--noshots" in sys.argv)
    if which == "arms":
        arm_variants()
    if which in ("backs", "belts"):
        back_variants(which)
