r"""Borrowing a reference model's own paint, part by part (2026-11-13; user: two in-game enemies built on the Bat's body as
3D references; a first whole-model projection (every texel takes the nearest point of the reference) was dropped:
"it opens up for a lot of mistake ... consider repainting yourself while borrowing textures from the existing ones": it
put hair on the face, a skirt on the legs, and mirrored the model left to right). Here nothing is automatic: the painter
names a part of the outfit and the part of the reference it takes its paint from.

  ref_maps(obj, tex, K, cache, sub)   the reference's sheet rasterised like wardrobe_repaint.texel_maps: per texel its
                                      place on the body IN THE OUTFIT'S FRAME (fit: turn + shift + scale; NOT mirrored: the
                                      layouts both models share (face, ears, tail, hands) only coincide unmirrored), normal, UV
                                      island (lab), and the texture enlarged K x (rgb)
  borrow(out, M, dst, R, src, ...)    the outfit texels `dst` take the colour of the nearest texel, on the body, of the
                                      reference's texels `src` (both masks chosen by the painter) -> the distances, to print
  same_uv(M, R)                       per outfit island: how much of it has the reference's texel at the SAME sheet place
                                      and the same place on the body (then a plain copy is exact)
  uv run --no-project --with pillow --with numpy --with scipy python -I pipeline/wardrobe_borrow.py <cls> <outfit> <ref.obj> <ref.png> <out dir> [--sub N] [--K 2]
prints the reference's islands (numbered picture: <out>/ref_islands.png) and the same_uv table."""
import itertools, sys
from pathlib import Path
from types import SimpleNamespace
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from scipy.spatial import cKDTree
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wardrobe_repaint import DATA, cached_maps, sstep


def load_obj(path, sub=None):
    """-> pos, uv, normals (per vertex), tris of the submesh `sub` (the export's group <name>_<sub>; None = all)."""
    P, T, N, F, on = [], [], [], [], sub is None
    for line in Path(path).read_text("utf-8").splitlines():
        a = line.split()
        if not a:
            continue
        if a[0] == "v":
            P.append([float(x) for x in a[1:4]])
        elif a[0] == "vt":
            T.append([float(x) for x in a[1:3]])
        elif a[0] == "vn":
            N.append([float(x) for x in a[1:4]])
        elif a[0] == "g" and sub is not None:
            on = a[1].endswith(f"_{sub}")
        elif a[0] == "f" and on:
            F.append([int(c.split("/")[0]) - 1 for c in a[1:4]])
    return np.array(P), np.array(T), np.array(N), np.array(F)


def fit(src, dst, mirror=False, iters=30, keep=0.7):
    """src laid on dst: the best of the 24 axis turns (mirrored ones when `mirror`), each refined (ICP on the closest
    `keep` of the pairs, a scale) -> (A, t, error): a point p of src goes to A @ p + t (A = scale x turn)."""
    tree = cKDTree(dst)
    best = None
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            R = np.zeros((3, 3))
            for i, (p, s) in enumerate(zip(perm, signs)):
                R[i, p] = s
            if (np.linalg.det(R) < 0) != mirror:
                continue
            q = src @ R.T
            s, t = 1.0, np.array([np.median(dst[:, 0]) - np.median(q[:, 0]), np.median(dst[:, 1]) - np.median(q[:, 1]),
                                  np.percentile(dst[:, 2], 1) - np.percentile(q[:, 2], 1)])
            for _ in range(iters):
                d, j = tree.query(s * src @ R.T + t)
                m = d <= np.quantile(d, keep)
                a, b = src[m], dst[j[m]]
                ma, mb = a.mean(0), b.mean(0)
                U, S, Vt = np.linalg.svd((b - mb).T @ (a - ma) / len(a))
                D = np.diag([1, 1, np.sign(np.linalg.det(U @ Vt)) * (-1 if mirror else 1)])
                R = U @ D @ Vt
                s = float(np.clip((S * np.diag(D)).sum() / ((a - ma) ** 2).sum(1).mean(), 0.8, 1.25))
                t = mb - s * R @ ma
            d = tree.query(s * src @ R.T + t)[0]
            err = float(np.sort(d)[: int(len(d) * keep)].mean())
            if best is None or err < best[2]:
                best = (s * R, t, err)
    return best


def ref_maps(obj, tex, K, cache, sub=None, cls="bat", body="summer", mirror=False):
    """The reference's sheet, per texel (see the module's docstring); laid on `cls`'s `body` outfit (a bare one fits best).
    Kept in <cache>/ref_<name>_<K>.npz."""
    obj, f = Path(obj), Path(cache) / f"ref_{Path(obj).stem}_{K}{'_m' if mirror else ''}.npz"
    im = Image.open(tex).convert("RGB")
    W, H = im.width * K, im.height * K
    if not f.exists():
        P, T, N, F = load_obj(obj, sub)
        used = np.unique(F)
        B = cached_maps(cls, body, 2, cache)
        rng = np.random.default_rng(1)
        dst = B.pos[B.covered]
        A, t, err = fit(P[used], dst[rng.choice(len(dst), 40000, replace=False)], mirror)
        P, N = P @ A.T + t, N @ (A / np.cbrt(abs(np.linalg.det(A)))).T
        pos, nrm, cov = np.zeros((H, W, 3)), np.zeros((H, W, 3)), np.zeros((H, W), bool)
        px = np.stack([T[:, 0] * W, (1 - T[:, 1]) * H], 1)
        for tri in F:
            a, b, c = px[tri]
            x0, x1 = max(int(min(a[0], b[0], c[0])), 0), min(int(np.ceil(max(a[0], b[0], c[0]))), W - 1)
            y0, y1 = max(int(min(a[1], b[1], c[1])), 0), min(int(np.ceil(max(a[1], b[1], c[1]))), H - 1)
            den = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
            if x1 < x0 or y1 < y0 or abs(den) < 1e-9:
                continue
            xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            l0 = ((b[1] - c[1]) * (xs - c[0]) + (c[0] - b[0]) * (ys - c[1])) / den
            l1 = ((c[1] - a[1]) * (xs - c[0]) + (a[0] - c[0]) * (ys - c[1])) / den
            ins = (l0 >= -0.02) & (l1 >= -0.02) & (1 - l0 - l1 >= -0.02)
            yy, xx = np.where(ins)
            L = np.stack([l0[ins], l1[ins], 1 - l0[ins] - l1[ins]], 1)
            pos[yy + y0, xx + x0], nrm[yy + y0, xx + x0], cov[yy + y0, xx + x0] = L @ P[tri], L @ N[tri], True
        f.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(f, pos=pos.astype(np.float32), nrm=nrm.astype(np.float32), covered=cov, A=A, t=t, err=err)
    d = np.load(f)
    cov = d["covered"]
    return SimpleNamespace(pos=d["pos"].astype(float), nrm=d["nrm"].astype(float), covered=cov, lab=ndimage.label(cov)[0],
                           edge=ndimage.distance_transform_edt(cov), rgb=np.asarray(im.resize((W, H), Image.LANCZOS)).astype(float),
                           err=float(d["err"]), A=d["A"], t=d["t"])


def isl(X, K, x, y):
    """The island under the sheet point (x, y of the game's sheet) of an outfit's or a reference's maps."""
    return X.lab == X.lab[y * K + K // 2, x * K + K // 2]


def borrow(out, M, dst, R, src, absy=False, inset=1.5, name="", flip=False, view=0, within=None, shift=(0, 0, 0), axis=0, scale=(1, 1, 1)):
    """out[dst] = the reference's colour at the nearest point (on the body) of its texels `src`. absy: a mirrored outfit
    part (both halves read the same texels): |y| on both sides. inset: reference texels this close to their island's edge
    are not read (their colour bleeds from the gutter). flip: the outfit's part is read at its mirror place (y -> -y): a
    piece the outfit wears on the other side (the Bat's hip cloth on her right hip, the enemy's skirt on her left).
    view: 1 / -1 = as seen from the front / the back: nearest in (y, z) only, depth left out, and of the reference's
    layers there the one in front (a dress that hangs differently from the outfit's still shows its own picture at the
    same height and width; give front- or back-facing texels on both sides). within: only where the pair is this
    close (body units), fading out from half of it: the rest of `dst` keeps its paint. shift: the outfit's spot reads
    the reference that far away (x, y, z): a piece worn a little lower than hers (0, 0, +2 cm = hers, 2 cm down).
    scale: the outfit's spot is read at that multiple of its place (1.35 across = her wider panel squeezed into a
    narrower piece), applied before shift.
    **A reference part can itself be mirrored** (her helmet: only y >= 0 is in the maps, the last triangle drawn):
    axis: with view, the direction looked along: 0 = from the front / back, 1 = from the side (nearest in (x, z), the
    outermost layer; give side-facing texels).
    read a mirrored part with absy, or half of the outfit's part finds nothing (the band "only half", user 2026-11-13). Prints how far the pairs were;
    returns the distances."""
    sm = src & R.covered & (R.edge >= inset)
    ky = (lambda p: p * [1, 0, 1] + np.abs(p * [0, 1, 0])) if absy else (lambda p: p)
    key = (lambda p: np.delete(ky(p), axis, 1)) if view else ky
    sp, q = R.pos[sm], M.pos[dst] * ([1, -1, 1] if flip else [1, 1, 1]) * scale + shift
    tree = cKDTree(key(sp))
    if view:
        d, j = tree.query(key(q), k=8)
        depth = np.where(d <= d[:, :1] + 0.003, np.abs(sp[j][:, :, 1]) if axis == 1 else sp[j][:, :, 0] * view, -9.0)
        r, pick = np.arange(len(q)), depth.argmax(1)
        d, j = d[r, pick], j[r, pick]
    else:
        d, j = tree.query(key(q))
    col = R.rgb[sm][j]
    if within is None:
        out[dst] = col
    else:
        w = (1 - sstep(d, within * 0.5, within))[:, None]
        out[dst] = out[dst] * (1 - w) + col * w
    pc = np.percentile(d, [50, 90, 99]) * 100
    took = "" if within is None else f"; taken within {within * 100:.1f} cm: {100 * (d < within).mean():.0f} %"
    print(f"borrow {name:14s} {int(dst.sum()):8d} texels <- {int(sm.sum()):8d}; apart: median {pc[0]:.1f} cm, 90 % {pc[1]:.1f}, 99 % {pc[2]:.1f}{took}")
    return d


def same_uv(M, R, tol=0.03):
    """Per outfit island ((x, y) of a point of it on the maps, texels, share with the reference at the same sheet place
    within tol on the body)."""
    rows = []
    for i in range(1, int(M.lab.max()) + 1):
        m = (M.lab == i) & M.covered
        if m.sum() < 200:
            continue
        ok = R.covered[m] & (np.linalg.norm(R.pos[m] - M.pos[m], axis=-1) < tol)
        ys, xs = np.where(m)
        k = np.argmin((ys - ys.mean()) ** 2 + (xs - xs.mean()) ** 2)
        rows.append(((int(xs[k]), int(ys[k])), int(m.sum()), float(ok.mean())))
    return rows


def main():
    a = sys.argv
    cls, outfit, obj, tex, out = a[1], a[2], Path(a[3]), Path(a[4]), Path(a[5]).resolve()
    K = int(a[a.index("--K") + 1]) if "--K" in a else 2
    sub = int(a[a.index("--sub") + 1]) if "--sub" in a else None
    R = ref_maps(obj, tex, K, out / "_cache", sub, cls, mirror="--mirror" in a)
    M = cached_maps(cls, outfit, K, out / "_cache")
    print(f"fit: {R.err * 100:.1f} cm (the closest 70 %), det {np.linalg.det(R.A):+.3f}")
    rng = np.random.default_rng(3)
    pal = rng.integers(60, 255, (R.lab.max() + 1, 3)); pal[0] = 255
    pic = Image.fromarray((R.rgb * 0.45 + pal[R.lab] * 0.55).astype(np.uint8))
    d = ImageDraw.Draw(pic)
    print("the reference's islands (seed = a point on the game's sheet; X front, Y left, Z up in the outfit's frame):")
    for i in range(1, R.lab.max() + 1):
        m = R.lab == i
        if m.sum() < 60 * K * K:
            continue
        ys, xs = np.where(m)
        p = R.pos[m]
        cy, cx = ndimage.center_of_mass(m)
        if not m[int(cy), int(cx)]:
            k = np.argmin((ys - cy) ** 2 + (xs - cx) ** 2); cy, cx = ys[k], xs[k]
        d.text((cx - 6, cy - 5), str(i), fill="black", stroke_width=2, stroke_fill="white")
        print(f"{i:3d} px={m.sum() // (K * K):6d} seed=({int(cx) // K},{int(cy) // K}) sheet x {xs.min() // K}-{xs.max() // K} y {ys.min() // K}-{ys.max() // K} | "
              f"X {p[:, 0].min():.2f}..{p[:, 0].max():.2f} Y {p[:, 1].min():.2f}..{p[:, 1].max():.2f} Z {p[:, 2].min():.2f}..{p[:, 2].max():.2f} | nx {R.nrm[m][:, 0].mean():+.2f}")
    pic.save(out / "ref_islands.png")
    print("the outfit's islands with the reference at the same sheet place (island, texels, share):")
    print("  " + "  ".join(f"({x // K},{y // K}):{s * 100:.0f}%" for (x, y), n, s in same_uv(M, R) if n > 400 * K * K))


if __name__ == "__main__":
    main()
