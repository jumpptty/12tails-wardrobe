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
from wardrobe_borrow import ref_maps, borrow, isl, load_obj

CLS, K = "bat", 2
SIGIL, SIGIL_Z, SIGIL_H = (350, 144, 420, 254), 0.66, 0.26      # her panel's eye pattern: its box on her sheet (x0, y0, x1, y1); its middle's height on the coat, its height
COAT_BACK = "ref"                                               # the coat's back: "ref" (her skirt read: a forced band) | plain | eye | contour | spine | hem (coat_back)
BELT, BELT_AT = "none", (0.840, 0.028)                          # a belt round the coat: none | weave | braid | plates (belt); its middle's height and half-height (royal's own belt flaps sit there)
MID_LINE, MID_SIDE = 0.15, 0.12                                 # the belly's centre line and its sides' shade
MIDRIFF = 1.0                                                   # how much of the summer belly's light and shade (its own is ~5 %: 0.6 did not show; faint: user)
FOLD = (1.172, 14.0)                                            # the fold under each breast: its lowest height (at |y| 4.5 cm), how fast it rises to the middle
TAB_TOP, HER_LOW, PANEL_RIM = 0.935, 0.56, 2.6                  # the front piece's pattern starts under here; her tabard is read down to HER_LOW; its border, texels
DISC = (0.985, 0.040, 0.029)                                    # the waist sigil: its middle's height, half-width, half-height
NECK, NECK_W, NECK_H, NECK_P = 1.035, 0.050, 0.080, 3.5         # the neckline, a U (user: "U instead of V"; a V, and a shallow one, before): its bottom's height (just over the sigil), then up NECK_H by |y| = NECK_W, as the NECK_P-th power: a round bottom, upright sides
neck_z = lambda y: NECK + NECK_H * (y / NECK_W) ** NECK_P
neck_n = lambda y: np.hypot(1, NECK_H * NECK_P / NECK_W * (y / NECK_W) ** (NECK_P - 1))      # to measure across the neckline, not in height
LINING = 3.9                                                    # the coat's silver lining, texels of the 512 px sheet
COAT_SIDE = 0.03                                                # the coat's sides take her side panels' paint within this far, seen from the side
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
    J.own(hair, palette(R.rgb, E["hairB"], (10, 55, 95)), lo=1)
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
    ccols = np.array([dress[0] * 0.8, dress[1], dress[2], dress[2] * 1.18])
    cloth = np.stack([np.interp(J.L, [0.0, 0.10, 0.22, 0.60], ccols[:, i]) for i in range(3)], -1)
    J.o[coat] = cloth[coat]
    # its back and its sides: her skirt's panels as seen from behind and from the side, where she has them (the big
    # white eye sits on her side panels: user "texture of the side coat could use some white eye sigils from the ref coat")
    DB = (E["bodice"] | E["backp"] | E["side"]) & rb
    if COAT_BACK == "ref":
        J.take(coat & mb, DB, "coat back", absy=True, view=-1, within=0.015)
    else:
        coat_back(J, coat, dress, R, E)
    ms, rs = np.abs(M.nrm[..., 1]) > 0.45, np.abs(R.nrm[..., 1]) > 0.45
    J.take(coat & ms, (E["bodice"] | E["front"] | E["backp"] | E["side"]) & rs, "coat side", view=1, axis=1, within=COAT_SIDE)
    # its two front pieces: her panel's own pattern, whole (user: "the coat front piece, please try a better job at trying
    # to use reference image patterns"; reading her skirt there by place left fragments: the pieces hang elsewhere).
    # The eye in its diamond frame with the four leaves, from her sheet (SIGIL box), laid upright on the middle of each
    # piece, only its drawn lines (what differs from the box's own cloth colour), so no box shows
    fp = coat & mf & M.covered & (Z > SIGIL_Z - 0.10) & (Z < SIGIL_Z + 0.10)
    y0, y1 = np.percentile(Y[fp], [4, 96])
    hh = min(SIGIL_H, (y1 - y0) * 0.92 * (SIGIL[3] - SIGIL[1]) / (SIGIL[2] - SIGIL[0]))
    ww = hh * (SIGIL[2] - SIGIL[0]) / (SIGIL[3] - SIGIL[1])
    u, vv = (Y - (y0 + y1) / 2) / ww + 0.5, (SIGIL_Z + hh / 2 - Z) / hh
    inb = coat & (u > 0) & (u < 1) & (vv > 0) & (vv < 1)
    px = np.clip(((SIGIL[0] + u * (SIGIL[2] - SIGIL[0])) * K).astype(int), 0, R.rgb.shape[1] - 1)
    py = np.clip(((SIGIL[1] + vv * (SIGIL[3] - SIGIL[1])) * K).astype(int), 0, R.rgb.shape[0] - 1)
    patch = R.rgb[py, px]
    box = R.rgb[SIGIL[1] * K:SIGIL[3] * K, SIGIL[0] * K:SIGIL[2] * K].reshape(-1, 3)
    drawn = sstep(np.abs(patch - np.median(box, 0)).max(-1), 14, 44)
    J.mix(inb, patch, drawn * sstep(nx, 0.2, 0.45))
    print(f"sigil on the coat's front pieces: |y| {y0:.3f}..{y1:.3f}, {ww * 100:.1f} x {hh * 100:.1f} cm at z {SIGIL_Z}, {int((inb & M.covered).sum())} texels")
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
    seam = (Y < 0.005) & (nx < -0.1)
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
    J.mix(hem, band, 1 - sstep(t, LINING, LINING + 0.5))
    J.mix(hem, dress[0] * 0.40, 1 - sstep(t, 0.25, 0.55))
    if BELT != "none":
        belt(J, outer, m((473, 10)), silver, dress)
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
    tsrc = E["front"] & rf & R.covered & (R.edge >= 1.5 * K) & (R.pos[..., 1] > -0.003)
    tp, tc = R.pos[tsrc], R.rgb[tsrc]
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
    d_, j_ = cKDTree(tp[:, 1:]).query(np.stack([yq[main], zq[main]], 1))
    # (at the piece's middle her tabard has no texel to give: its own middle is the island's edge, left unread. Those
    # spots fell back to plain cloth: a stripe down the middle, "fix the seam", user 2026-11-13. Near the middle the
    # nearest texel of hers is taken from further away)
    got = ((d_ < 0.006) | ((u_[main] < 0.25) & (d_ < 0.02))) & (u_[main] < 0.84)
    cloth = np.median(tc[j_[got]], 0)
    J.o[low] = (cloth * (0.86 + 0.28 * J.form)[..., None])[low]
    ys_, xs_ = np.where(main)
    fade = sstep(TAB_TOP - Z[ys_[got], xs_[got]], -0.002, 0.010)[:, None]
    J.o[ys_[got], xs_[got]] = J.o[ys_[got], xs_[got]] * (1 - fade) + tc[j_[got]] * fade
    # above the waist the piece carries her bodice's own lines the same way (user: "the part above the horizontal cut
    # earlier looks bad, not textured and no patterns compared to below"): her dress's front at the same height, laid
    # across the piece's own width (u = |y| / the piece's edge there), in the tabard's cloth colour so the two join
    bsrc = E["bodice"] & rf & R.covered & (R.edge >= 1.5 * K)
    bp, bc = np.stack([np.abs(R.pos[..., 1][bsrc]), R.pos[..., 2][bsrc]], 1), R.rgb[bsrc]
    bb = np.arange(TAB_TOP - 0.03, 1.17, 0.005)
    bi = np.digitize(bp[:, 1], bb)
    bw = np.array([np.percentile(bp[bi == i][:, 0], 98) if (bi == i).sum() > 20 else np.nan for i in range(1, len(bb) + 1)])
    okb = ~np.isnan(bw)
    bw = ndimage.gaussian_filter1d(np.interp(bb, bb[okb], bw[okb]), 1.5)
    upper = low & (Z >= TAB_TOP - 0.012)
    yq2 = Y / np.maximum(np.interp(Z, zc, yo_f), 1e-3) * np.interp(Z, bb + 0.0025, bw)
    d2, j2 = cKDTree(bp).query(np.stack([yq2[upper], Z[upper]], 1))
    g2 = (d2 < 0.006) & ((Y / np.maximum(np.interp(Z, zc, yo_f), 1e-3))[upper] < 0.86)
    col2 = bc[j2[g2]] * (cloth / np.maximum(np.median(bc[j2[g2]], 0), 1))          # her bodice's cloth -> the tabard's
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
    band = (E["helmet"] | E["brow"]) & rf & (R.pos[..., 2] < BAND_TOP)
    J.take((hair | head) & mf & (Z > 1.50), band, "helmet band", absy=True, view=1, within=0.010, shift=(0, 0, BAND_DROP))
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
    J.o[sleeves] = (prof[np.clip(np.digitize(Y, bins) - 1, 0, len(bins) - 1)] * (0.80 + 0.40 * J.form)[..., None])[sleeves]
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
    if COAT_BACK == "eye":                                      # A: one large eye on the back, as on her wings
        eye(0.68 if BELT == "none" else 0.62, 0.24, 0.13)
    elif COAT_BACK == "contour":                                 # B: her wings' flowing contour lines, round a small eye
        r = np.hypot(Y / 1.5, Z - 0.70)
        wav = r + 0.014 * np.sin(Y * 45 + Z * 20)
        lines = ins(np.abs(((wav / 0.036) % 1) - 0.5) * 0.036 - 0.0040, 0.0015) * sstep(wav, 0.085, 0.10)
        J.mix(back, mag, lines * w * 0.75)
        eye(0.70, 0.13, 0.075, 0.9)
    elif COAT_BACK == "spine":                                   # C: a silver scroll down the middle, leaves, a diamond
        J.mix(back, dark, ins(Y - 0.012) * sstep(Z, 0.40, 0.44) * (Z < 0.98) * w * 0.8)
        J.mix(back, silver, ins(Y - 0.0065) * sstep(Z, 0.40, 0.44) * (Z < 0.98) * w)
        for cy in (0.90, 0.76, 0.62):
            curl = np.abs(np.hypot(Y - 0.050, Z - cy) - 0.040) - 0.0050
            J.mix(back, silver, ins(curl) * (Z > cy - 0.006) * (Y < 0.090) * w)
            leaf = np.hypot((Y - 0.105) / 0.020, (Z - cy + 0.006) / 0.034) - 1
            J.mix(back, dark, ins(leaf * 0.02 - 0.003) * w * 0.7)
            J.mix(back, white, ins(leaf * 0.02) * w)
        dia = Y / 0.050 + np.abs(Z - 0.50) / 0.075 - 1
        J.mix(back, silver, ins(np.abs(dia) * 0.03 - 0.0050) * w)
        J.mix(back, white, ins(np.hypot(Y, Z - 0.50) - 0.016) * w)
    elif COAT_BACK == "hem":                                     # D: a row of small ring sigils above the hem, a scroll band
        for cy, cz in ((0.0, 0.58), (0.15, 0.61), (0.29, 0.66)):
            r = np.hypot(Y - cy, Z - cz)
            J.mix(back, dark, ins(r - 0.052) * w * 0.75)
            J.mix(back, white, ins(np.abs(r - 0.042) - 0.0050) * w)
            J.mix(back, white, ins(np.abs(r - 0.024) - 0.0040) * w)
            J.mix(back, white, ins(r - 0.009) * w)
        band = Z - (0.70 + 0.30 * Y ** 2)
        J.mix(back, silver, ins(np.abs(band) - 0.0045) * w * (Y < 0.36))
        J.mix(back, mag * 1.25, ins(np.abs(band - 0.022 + 0.014 * np.sin(Y * 70)) - 0.0030) * w * (Y < 0.36))
    print(f"coat back: design {COAT_BACK}, {int((back & M.covered).sum())} texels")


def belt(J, outer, tabs, silver, dress):
    """A belt round the coat, dark red, textured (user 2026-11-13, on the band across the coat's back: "I think textured
    belt with dark red as the main color can be quite a good contrast for the lower body"). Original, in her colours:
    the red of her wings' edges (her sheet: 115,20,41 .. 222,60,82) as a shadow / base / light ramp, her silver for its
    piping. At BELT_AT, where royal's own belt flaps are (they take the belt's red). Drawn round the body (s = the way
    round from the front's middle, in body units; both halves of the coat share their texels, so it is symmetric):
      weave   a diagonal lattice: dark lines, each diamond lit at its middle
      braid   two strands crossing over and under, and an eye plate at the back's middle (her sigil as a buckle)
      plates  short plates with a bevel, a dark seam between them, a silver stud on each"""
    M = J.M
    X, Y, Z = M.pos[..., 0], np.abs(M.pos[..., 1]), M.pos[..., 2]
    zc, hw = BELT_AT
    ring = outer & M.covered & (np.abs(Z - zc) < hw)
    xc = (X[ring].min() + X[ring].max()) / 2
    rad = float(np.median(np.hypot(X[ring] - xc, Y[ring])))
    a = np.arctan2(Y, X - xc)
    sa, sb, dz = a * rad, (np.pi - a) * rad, Z - zc             # round from the front's middle, from the back's middle
    v = dz / hw
    red = [np.array(c) for c in ((58.0, 9, 22), (124.0, 22, 44), (186.0, 58, 78))]
    dark, white = red[0] * 0.55, np.array([232.0, 222, 240])
    ins = lambda d, aa=0.0012: 1 - sstep(d, -aa, aa)
    on = ins(np.abs(dz) - hw)
    tone_ = 0.46 + 0.9 * (J.form - 0.5) + 0.14 * v              # a rounded band: lighter toward its top
    J.mix(outer, dress[0] * 0.45, ins(np.abs(dz + hw + 0.006) - 0.008, 0.006) * 0.55)       # its shade on the coat under it
    if BELT == "weave":
        c = 0.019
        pq = [(sa + dz) / c, (sa - dz) / c]
        lat = np.minimum(*[np.abs(x - np.round(x)) for x in pq])                            # 0 on a line .. 0.5 in a diamond
        J.mix(outer, ramp3(tone_ + 0.34 * (lat * 2 - 0.45), red), on)
        J.mix(outer, dark, ins(lat * c - 0.0016, 0.0010) * on * 0.9)
    elif BELT == "braid":
        J.mix(outer, ramp3(tone_ - 0.12, red), on)
        ph = sa / 0.019
        for k, sg in ((0, 1), (1, -1)):
            w_ = v * 0.86 - sg * 0.52 * np.sin(ph)
            over = (np.cos(ph) * sg > 0)                                                    # which strand lies on top here
            strand = ins((np.abs(w_) - 0.30) * hw, 0.0010) * on
            J.mix(outer, dark, ins((np.abs(w_) - 0.40) * hw, 0.0010) * on * np.where(over, 1.0, 0.0))
            J.mix(outer, ramp3(tone_ + 0.30 - 0.9 * np.abs(w_), red), strand * np.where(over, 1.0, 0.0))
        for k, sg in ((0, 1), (1, -1)):                                                     # the strand underneath, where it is not covered
            w_ = v * 0.86 - sg * 0.52 * np.sin(ph)
            under = (np.cos(ph) * sg <= 0)
            other = np.abs(v * 0.86 + sg * 0.52 * np.sin(ph)) > 0.40
            J.mix(outer, ramp3(tone_ + 0.12 - 0.9 * np.abs(w_), red), ins((np.abs(w_) - 0.30) * hw, 0.0010) * on * under * other)
        plate = np.hypot(sb / 0.050, dz / 0.036)                                            # the eye plate behind
        r = np.hypot(sb, dz)
        J.mix(outer, dark, ins((plate - 1.10) * 0.036))
        J.mix(outer, ramp3(np.full(Y.shape, 0.75), silver), ins((plate - 1.0) * 0.036))
        J.mix(outer, red[0], ins((plate - 0.80) * 0.036))
        J.mix(outer, white, ins(np.abs(r - 0.017) - 0.0030))
        J.mix(outer, white, ins(r - 0.0065))
    elif BELT == "plates":
        L_ = 0.052
        f = sa / L_ - np.floor(sa / L_)
        cen = np.abs(f - 0.5) * L_                                                           # from the plate's middle
        bev = np.minimum(np.minimum(f, 1 - f) * L_, hw - np.abs(dz))                          # from the plate's rim
        J.mix(outer, ramp3(tone_ + 0.22 * sstep(bev, 0.0, 0.006) - 0.06, red), on)
        J.mix(outer, dark, ins(np.minimum(f, 1 - f) * L_ - 0.0022) * on)
        stud = np.hypot(cen, dz)
        J.mix(outer, dark, ins(stud - 0.0095) * on * 0.8)
        J.mix(outer, ramp3(np.clip(0.95 - stud / 0.012, 0, 1), silver), ins(stud - 0.0075) * on)
    # silver piping along both edges, a dark line outside it
    pipe = np.abs(np.abs(dz) - (hw - 0.0050))
    J.mix(outer, ramp3(0.55 + 0.45 * (1 - pipe / 0.0030).clip(0, 1), silver), ins(pipe - 0.0030) * (np.abs(dz) < hw + 0.002))
    J.mix(outer, dark, ins(np.abs(np.abs(dz) - hw) - 0.0013))
    if BELT == "braid":                                                                      # the plate lies over the piping
        J.mix(outer, ramp3(np.full(Y.shape, 0.75), silver), ins(np.abs(plate - 0.92) * 0.036 - 0.0030))
        J.mix(outer, dark, ins(np.abs(plate - 1.04) * 0.036 - 0.0012))
    J.own(tabs, red, k=0.9)
    print(f"belt: {BELT} at z {zc} +- {hw}, {rad * 100:.1f} cm from the coat's middle there, {int((ring).sum())} texels")


def back_variants(which="backs"):
    """Designs side by side for the user to pick: "backs" = the coat's back (eyes/back_variants.png), "belts" = the dark
    red belt, three textures, and one with the back's eye under it (eyes/belt_variants.png: back, back three-quarter, front)."""
    global COAT_BACK, BELT
    out, vs = BASE / "eyes", []
    sets = {"backs": (("eye", "A  one large eye", "eye", "none"), ("contour", "B  wing contour lines + small eye", "contour", "none"),
                      ("spine", "C  silver scroll spine", "spine", "none"), ("hem", "D  ring sigils along the hem", "hem", "none")),
            "belts": (("weave", "E  belt: woven lattice", "plain", "weave"), ("braid", "F  belt: braid + eye plate behind", "plain", "braid"),
                      ("plates", "G  belt: plates + silver studs", "plain", "plates"), ("weave_eye", "H  belt E + the large eye (A)", "eye", "weave"))}[which]
    views = ("180", "150") if which == "backs" else ("180", "150", "000")
    keep = COAT_BACK, BELT
    for key, _, cb, bl in sets:
        COAT_BACK, BELT = cb, bl
        J, look = eyes()
        f = out / "look" / f"royal_{which[:-1]}_{key}.png"
        Image.fromarray(np.dstack([np.clip(J.o, 0, 255), np.full(J.o.shape[:2], 255.0)]).astype(np.uint8), "RGBA").save(f)
        vs.append((f"{which[:-1]}_{key}", {f"{CLS}|outfits|royal|": f, **J.extra}, {"Head": look["head"]}))
    COAT_BACK, BELT = keep
    asyncio.run(shots(CLS, "royal", vs, out, yaws=tuple((int(y), y) for y in views), size=800, face=11))
    from PIL import ImageDraw
    sheet = Image.new("RGB", (480 * 4, 520 * len(views) + 40), (230, 225, 216))
    d = ImageDraw.Draw(sheet)
    for i, ((n, _, _), (_, label, _, _)) in enumerate(zip(vs, sets)):
        for j, y in enumerate(views):
            sheet.paste(Image.open(out / "shots" / f"{n}_{y}.png").crop((160, 250, 640, 770)), (480 * i, 40 + 520 * j))
        d.text((480 * i + 20, 12), label, fill="black")
    sheet.save(out / f"{which[:-1]}_variants.png")
    print(out / f"{which[:-1]}_variants.png")


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
