r"""The helmeted Bat skin's lashes, several strengths side by side for the user's pick (2026-11-14: "you can try more
aggresive lashes"). The skin is painted once (wardrobe_bat_enemies.eyes), the make-up put on a copy per variant.
  uv run --no-project --with pillow --with numpy --with scipy --with playwright python -I pipeline/wardrobe_bat_lashes.py
-> plans/reskins/bat/eyes/_cache/lash_<name>.png (1024 px skins) and eyes/lash_variants.png (the eyes, flat, with the
face preset on, 6 x). The model's close-ups: wardrobe_skin_views.py --at Head --lift 0.11 --zoom 9."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).resolve().parent))
import wardrobe_bat_enemies as W

# name: LASHES, LASH_LEN, LASH_W, LASH_FROM
V = {"A_now": (5, 1.25, 1.0, 0.42), "B_bold": (6, 1.7, 1.25, 0.34), "C_dramatic": (7, 2.2, 1.45, 0.26), "D_extreme": (8, 2.8, 1.6, 0.18)}
real, kept = W.eye_makeup, {}
W.eye_makeup = lambda J, head, face: kept.update(J=J, head=head, face=face)
W.eyes()
J, out = kept["J"], W.BASE / "eyes"
bare = J.o.copy()
face = Image.open(W.DATA / W.CLS / "faces" / f"{kept['face']}.webp").convert("RGBA").resize((512, 512), Image.LANCZOS)
box, rows = (12 * 2, 26 * 2, 116 * 2, 66 * 2), []
for name, (n, ln, w, fr) in V.items():
    W.LASHES, W.LASH_LEN, W.LASH_W, W.LASH_FROM = n, ln, w, fr
    J.o = bare.copy()
    real(J, kept["head"], kept["face"])
    skin = Image.fromarray(np.dstack([np.clip(J.o, 0, 255), np.full(J.o.shape[:2], 255.0)]).astype(np.uint8), "RGBA")
    skin.save(out / "_cache" / f"lash_{name}.png")
    c = skin.crop((0, 0, 512, 512)); c.alpha_composite(face)
    rows.append((name, c.crop(box).resize(((box[2] - box[0]) * 6, (box[3] - box[1]) * 6), Image.LANCZOS).convert("RGB")))
w_, h_ = rows[0][1].size
sheet = Image.new("RGB", (w_, (h_ + 30) * len(rows)), "white")
g = ImageDraw.Draw(sheet)
for i, (name, im) in enumerate(rows):
    sheet.paste(im, (0, i * (h_ + 30) + 30)); g.text((8, i * (h_ + 30) + 8), name, fill="black")
sheet.save(out / "lash_variants.png")
print(out / "lash_variants.png")
