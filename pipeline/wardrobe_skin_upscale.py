r"""A painted skin at twice its size, through the project's icon recipe (user 2026-11-14, of the Bat's royal skin: "is
there a way to make the patterns looks more high res? can you try upscaling if it helps?"). The recipe is
wardrobe_icons_upscale.py's (Real-ESRGAN x4: 0.6 anime_6B + 0.4 x4plus, Lanczos down to 2x); a skin is too big for one
pass on the GPU, so it goes through in tiles with a margin (the margin's picture is thrown away: no tile seams). The
skin stays opaque (an outfit cannot hide anything). Needs torch with CUDA and the models: the home PC.

  py -3.10 pipeline\wardrobe_skin_upscale.py <in.png> <out.png> [--tile 192] [--pad 24] [--bits 7]
The wardrobe wears a skin of any size (composeTexture scales the face overlay by skin width / base width); the send
route takes files up to 4 MB (site_worker.mjs LIMITS.fileBytes): the size is printed."""
import argparse
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wardrobe_icons_upscale import esrgan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--tile", type=int, default=192); ap.add_argument("--pad", type=int, default=24)
    ap.add_argument("--bits", type=int, default=7, help="colour depth per channel of the file (7: off by 1 level at most, a quarter smaller; 8: as upscaled)")
    a = ap.parse_args()
    im = Image.open(a.src).convert("RGB")
    W, H = im.size
    px = np.asarray(im)
    padded = Image.fromarray(np.pad(px, ((a.pad, a.pad), (a.pad, a.pad), (0, 0)), mode="reflect"))
    up = esrgan()
    out = np.zeros((2 * H, 2 * W, 3), np.uint8)
    n = 0
    for y in range(0, H, a.tile):
        for x in range(0, W, a.tile):
            w, h = min(a.tile, W - x), min(a.tile, H - y)
            t = up(padded.crop((x, y, x + w + 2 * a.pad, y + h + 2 * a.pad)))      # 2x, the margins with it
            out[2 * y:2 * (y + h), 2 * x:2 * (x + w)] = np.asarray(t.convert("RGB"))[2 * a.pad:2 * (a.pad + h), 2 * a.pad:2 * (a.pad + w)]
            n += 1
    q = 256 >> a.bits
    if q > 1:                                                    # (a 2048 px skin is ~5 MB as upscaled: over the send route's 4 MB)
        out = ((out.astype(int) + q // 2) // q * q).clip(0, 255).astype(np.uint8)
    Image.fromarray(np.dstack([out, np.full(out.shape[:2], 255, np.uint8)]), "RGBA").save(a.dst, optimize=True)
    print(f"{a.src} {W}x{H} -> {a.dst} {2 * W}x{2 * H}, {n} tiles, {os.path.getsize(a.dst) / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
