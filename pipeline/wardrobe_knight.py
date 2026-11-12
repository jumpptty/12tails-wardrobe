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


if __name__ == "__main__":
    main()
