r"""Upscale the wardrobe's icons (user 2026-11-13: "check all icons in the wardrobe app for any unupscaled ones, and
upscale them"; "you may check 12 tails bible hub, some might be there already").

The data builds (wardrobe_icons.py, wardrobe_ui_assets.py) write every icon at the game's own size: 64 px (BB's art),
51 px (TTO's own art), 75 px (the class portraits). This replaces each, in place and under the same name, with a 2x
picture (128 px; the portraits 150 px):

  1. the 12 Tails Bible's own 128 px upscale when it has one under the same name (12t_projects\bible\assets.js:
     GEAR_ICONS a_ / w_ / c_ / t_<code> for icons/armor / weapon / accessory / trinket, SKILL_ICONS <class>_<skill><rank>
     and sup_<skill> for icons/skills/<class> and /support, compared without case) and its picture, shrunk back, is the
     icon's (mean difference over black <= BIBLE_MAX_DIFF per channel): the Bible's WebP bytes as they are;
  2. else the project's icon recipe (D:\12tails-assets-archive\tto-c6-skill-icons-2026-11-03\tools: Real-ESRGAN x4 as
     plain torch modules, RGB = 0.6 x RealESRGAN_x4plus_anime_6B + 0.4 x RealESRGAN_x4plus, alpha Lanczos, Lanczos down
     to the 2x size, WebP q90). Needs torch with CUDA and the models in D:\sd_backup\models\RealESRGAN: the home PC.

icons/upscaled.json keeps, per icon, the hash of the game-size picture it was made from and where it came from
("bible:<key>" or "esrgan"). The data builds ask keep() before writing an icon: an upscale made from the very picture
they are about to write stays, so a rebuild only puts new or changed icons back at game size, and the next run here
upscales just those. icons/hd/ (the Bible's skill icons for the ท่าสกิล rings, wardrobe_skill_icons.py) is not touched.

  py -3.10 pipeline\wardrobe_icons_upscale.py            upscale every icon still at game size
  py -3 pipeline\wardrobe_icons_upscale.py --check       list them only (exit 1 when there are any); needs Pillow only
  ... --sheet <png>                                      also a contact sheet: game size (nearest x2) beside the upscale

The publish takes an upscaled icon only when it proves to be BB's (wardrobe_publish.py Run.icon).
"""
import base64
import hashlib
import io
import json
import os
import re
import sys

from PIL import Image, ImageChops, ImageStat

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = os.path.join(ROOT, "wardrobe", "data", "icons")
MANIFEST = "upscaled.json"
SKIP = ("hd/",)                      # the Bible's skill icons, 128 px already
GAME_SIZES = (51, 64, 75)            # an icon whose longer side is under UPSCALED is at game size
UPSCALED = 128
BIBLE_MAX_DIFF = 10                  # the Bible's same-name upscales measure 0.3 - 8.6 against the game's icon (2026-11-13)
MODELS = "D:/sd_backup/models/RealESRGAN/"
BIBLE = next((p for p in (r"D:\12tails", r"C:\Users\Jump\Desktop\12tails") if os.path.isfile(p + r"\12t_projects\bible\assets.js")), r"D:\12tails")
GEAR_PREFIX = {"armor": "a_", "weapon": "w_", "accessory": "c_", "trinket": "t_"}   # not "acessory": TTO's own folder, other items


def pixel_hash(im):
    """The hash of a picture's pixels (its size and RGBA bytes), whatever file it was read from."""
    im = im.convert("RGBA")
    return hashlib.sha1(f"{im.size[0]}x{im.size[1]}:".encode() + im.tobytes()).hexdigest()


def target_size(size):
    """2x; TTO's 51 px art goes to 128 like the 64 px art (the Bible's convention)."""
    w, h = size
    return (UPSCALED, UPSCALED) if max(w, h) <= 64 else (2 * w, 2 * h)


def is_game_size(size):
    return max(size) < UPSCALED


def load_manifest(icons=ICONS):
    p = os.path.join(icons, MANIFEST)
    if not os.path.isfile(p):
        return {}
    with open(p, encoding="utf-8") as f:
        return json.load(f)


_manifests = {}


def keep(path, image, icons=ICONS):
    """For the data builds: True when the file at path is the upscale of this very game-size picture (so the build
    must not write over it)."""
    icons = os.path.abspath(icons)
    if icons not in _manifests:
        _manifests[icons] = load_manifest(icons)
    rel = os.path.relpath(os.path.abspath(path), icons).replace(os.sep, "/")
    e = _manifests[icons].get(rel)
    if not e or e.get("src") != pixel_hash(image) or not os.path.isfile(path):
        return False
    try:
        with Image.open(path) as im:
            return not is_game_size(im.size)
    except OSError:
        return False


def over_black(im):
    base = Image.new("RGBA", im.size, (0, 0, 0, 255))
    base.alpha_composite(im.convert("RGBA"))
    return base.convert("RGB")


def difference(small, big):
    """Mean absolute difference per channel (the largest of R, G, B) between a game-size picture and a bigger one
    shrunk to its size, both over black."""
    a = over_black(small)
    b = over_black(big.convert("RGBA").resize(small.size, Image.LANCZOS))
    return max(ImageStat.Stat(ImageChops.difference(a, b)).mean)


def game_size_icons(icons=ICONS):
    out = []
    for d, _, files in os.walk(icons):
        for f in sorted(files):
            rel = os.path.relpath(os.path.join(d, f), icons).replace(os.sep, "/")
            if not f.endswith(".webp") or rel.startswith(SKIP):
                continue
            with Image.open(os.path.join(d, f)) as im:
                if is_game_size(im.size):
                    out.append(rel)
    return sorted(out)


def bible_icons():
    """{key in lower case: (key, WebP bytes)} of the Bible's 128 px gear and skill icons."""
    path = os.path.join(BIBLE, "12t_projects", "bible", "assets.js")
    if not os.path.isfile(path):
        return {}
    s = open(path, encoding="utf-8").read()
    heads = [(m.start(), m.group(1)) for m in re.finditer(r"(?m)^BIBLE_ASSETS\.([A-Z_0-9]+)\s*=", s)] + [(len(s), None)]
    out = {}
    for (a, name), (b, _) in zip(heads, heads[1:]):
        if name not in ("GEAR_ICONS", "SKILL_ICONS"):
            continue
        for key, data in re.findall(r'"([^"\n]{1,80})"\s*:\s*"data:image/webp;base64,([^"]+)"', s[a:b]):
            raw = base64.b64decode(data)
            with Image.open(io.BytesIO(raw)) as im:
                if im.size == (UPSCALED, UPSCALED):
                    out[key.lower()] = (key, raw)
    return out


def bible_key(rel):
    parts = rel[:-len(".webp")].split("/")
    if len(parts) == 2 and parts[0] in GEAR_PREFIX:
        return GEAR_PREFIX[parts[0]] + parts[1]
    if len(parts) == 3 and parts[0] == "skills" and parts[1] != "emotion":
        return ("sup" if parts[1] == "support" else parts[1]) + "_" + parts[2]
    return None


# ---- Real-ESRGAN (basicsr's RRDBNet) as plain torch modules: the archive's esr.py
def esrgan():
    import numpy as np
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    class RDB(nn.Module):
        def __init__(self, nf=64, gc=32):
            super().__init__()
            self.conv1 = nn.Conv2d(nf, gc, 3, 1, 1)
            self.conv2 = nn.Conv2d(nf + gc, gc, 3, 1, 1)
            self.conv3 = nn.Conv2d(nf + 2 * gc, gc, 3, 1, 1)
            self.conv4 = nn.Conv2d(nf + 3 * gc, gc, 3, 1, 1)
            self.conv5 = nn.Conv2d(nf + 4 * gc, nf, 3, 1, 1)
            self.lrelu = nn.LeakyReLU(0.2, True)

        def forward(self, x):
            x1 = self.lrelu(self.conv1(x))
            x2 = self.lrelu(self.conv2(torch.cat((x, x1), 1)))
            x3 = self.lrelu(self.conv3(torch.cat((x, x1, x2), 1)))
            x4 = self.lrelu(self.conv4(torch.cat((x, x1, x2, x3), 1)))
            return self.conv5(torch.cat((x, x1, x2, x3, x4), 1)) * 0.2 + x

    class RRDB(nn.Module):
        def __init__(self, nf, gc=32):
            super().__init__()
            self.rdb1, self.rdb2, self.rdb3 = RDB(nf, gc), RDB(nf, gc), RDB(nf, gc)

        def forward(self, x):
            return self.rdb3(self.rdb2(self.rdb1(x))) * 0.2 + x

    class RRDBNet(nn.Module):
        def __init__(self, nb, nf=64, gc=32):
            super().__init__()
            self.conv_first = nn.Conv2d(3, nf, 3, 1, 1)
            self.body = nn.Sequential(*[RRDB(nf, gc) for _ in range(nb)])
            self.conv_body = nn.Conv2d(nf, nf, 3, 1, 1)
            self.conv_up1 = nn.Conv2d(nf, nf, 3, 1, 1)
            self.conv_up2 = nn.Conv2d(nf, nf, 3, 1, 1)
            self.conv_hr = nn.Conv2d(nf, nf, 3, 1, 1)
            self.conv_last = nn.Conv2d(nf, 3, 3, 1, 1)
            self.lrelu = nn.LeakyReLU(0.2, True)

        def forward(self, x):
            feat = self.conv_first(x)
            feat = feat + self.conv_body(self.body(feat))
            feat = self.lrelu(self.conv_up1(F.interpolate(feat, scale_factor=2, mode="nearest")))
            feat = self.lrelu(self.conv_up2(F.interpolate(feat, scale_factor=2, mode="nearest")))
            return self.conv_last(self.lrelu(self.conv_hr(feat)))

    nets = {}
    for kind, nb, f in (("anime", 6, "RealESRGAN_x4plus_anime_6B.pth"), ("general", 23, "RealESRGAN_x4plus.pth")):
        m = RRDBNet(nb)
        m.load_state_dict(torch.load(MODELS + f, map_location="cpu", weights_only=True)["params_ema"])
        nets[kind] = m.eval().cuda()

    @torch.no_grad()
    def upscale(im):
        """A game-size RGBA picture -> its 2x picture (the recipe in the docstring)."""
        src = np.asarray(im.convert("RGBA"), dtype=np.float32) / 255.0
        h, w = src.shape[:2]
        t = torch.from_numpy(src[..., :3].transpose(2, 0, 1)).unsqueeze(0).cuda()
        up = (0.6 * nets["anime"](t).clamp(0, 1) + 0.4 * nets["general"](t).clamp(0, 1)).squeeze(0).cpu().numpy().transpose(1, 2, 0)
        u8 = lambda a: (np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)
        alpha = np.asarray(Image.fromarray(u8(src[..., 3])).resize((4 * w, 4 * h), Image.LANCZOS))
        return Image.fromarray(np.dstack([u8(up), alpha]), "RGBA").resize(target_size((w, h)), Image.LANCZOS)
    return upscale


def sheet(pairs, path, cols=12):
    """Contact sheet: per icon the game-size picture (nearest, to the upscale's size) and the upscale, on dark and white."""
    cell, pad = 150, 4
    rows = (len(pairs) + cols - 1) // cols
    out = Image.new("RGBA", (cols * (2 * cell + 3 * pad), rows * (cell + pad) + pad), (30, 26, 24, 255))
    for i, (old, new) in enumerate(pairs):
        r, c = divmod(i, cols)
        x, y = c * (2 * cell + 3 * pad) + pad, r * (cell + pad) + pad
        if (r + c) % 2:
            out.paste((255, 255, 255, 255), (x - 2, y - 2, x + 2 * cell + pad + 2, y + cell + 2))
        out.alpha_composite(old.convert("RGBA").resize(new.size, Image.NEAREST), (x, y))
        out.alpha_composite(new.convert("RGBA"), (x + cell + pad, y))
    out.save(path)


def main(argv):
    todo = game_size_icons()
    if "--check" in argv:
        print(f"{len(todo)} icons at game size" + (":" if todo else " (every icon is upscaled)"))
        for rel in todo:
            print(" ", rel)
        return 1 if todo else 0
    if not todo:
        print("every icon is upscaled already")
        return 0
    manifest, bible, upscale = load_manifest(), bible_icons(), None
    print(f"{len(todo)} icons at game size; the Bible has {len(bible)} 128 px icons", flush=True)
    pairs, counts, refused = [], {"bible": 0, "esrgan": 0}, []
    for n, rel in enumerate(todo):
        path = os.path.join(ICONS, *rel.split("/"))
        with Image.open(path) as f:
            old = f.convert("RGBA")
        hit = bible.get((bible_key(rel) or "").lower()) if target_size(old.size) == (UPSCALED, UPSCALED) else None
        if hit:
            d = difference(old, Image.open(io.BytesIO(hit[1])))
            if d > BIBLE_MAX_DIFF:
                refused.append((rel, hit[0], round(d, 1)))
                hit = None
        if hit:
            with open(path, "wb") as f:
                f.write(hit[1])
            manifest[rel] = {"src": pixel_hash(old), "from": "bible:" + hit[0]}
            counts["bible"] += 1
        else:
            upscale = upscale or esrgan()
            upscale(old).save(path, "WEBP", quality=90)
            manifest[rel] = {"src": pixel_hash(old), "from": "esrgan"}
            counts["esrgan"] += 1
        if "--sheet" in argv:
            pairs.append((old, Image.open(path).convert("RGBA")))
        if (n + 1) % 500 == 0:
            print(f"  {n + 1} / {len(todo)}", flush=True)
    with open(os.path.join(ICONS, MANIFEST), "w", encoding="utf-8", newline="\n") as f:
        json.dump(dict(sorted(manifest.items())), f, separators=(",", ":"))
    print(f"upscaled {len(todo)}: {counts['bible']} from the Bible, {counts['esrgan']} by Real-ESRGAN")
    for rel, key, d in refused:
        print(f"  {rel}: the Bible's {key} is too far from the game's icon (difference {d}, limit {BIBLE_MAX_DIFF}); upscaled here")
    if "--sheet" in argv:
        step = max(1, len(pairs) // 240)
        sheet(pairs[::step], argv[argv.index("--sheet") + 1])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
