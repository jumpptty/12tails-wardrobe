r"""BB's own copies of the rip's broken pictures, so the office PC can publish (2026-11-09; user: "deploy from office made
possible please"). The office's copy of the Bible rip has 52 zero-filled Monkey PNGs (armour colours and editions,
.fbm textures, the face overlays 0-22): the publish would drop the Theurgist and Superstar outfits and Monkey's BB faces.
The Bible repo is never written, so each broken file is exported again from BB's game data (12TailsOnline_Data, read
with wardrobe_fx.Game: mainData's ResourceManager for Resources paths, else the Texture2D of that name) into
wardrobe/data/bb_rip_fix/<its path under Assets>, which wardrobe_publish.py uses only when the rip's file can't be
read. Self-check first: intact rip PNGs exported the same way must match the rip pixel for pixel (orientation, alpha).

  uv run --no-project --with UnityPy --with pillow python -I pipeline/bb_rip_fix.py
"""
import os
import sys
from pathlib import Path

from PIL import Image, ImageChops

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wardrobe_fx  # noqa: E402  (its Game: BB's data files, read with UnityPy)

ASSETS = Path(wardrobe_fx.RIP).parent.parent                  # ...\ExportedProject\Assets
OUT = Path(wardrobe_fx.DATA) / "bb_rip_fix"
SCAN = [ASSETS / "Resources" / "gameassets" / "characters" / "heroes", ASSETS / "Resources" / "gamegui" / "icons", ASSETS / "Texture2D"]


def readable(p):
    try:
        with Image.open(p) as im:
            im.verify()
        return True
    except OSError:
        return False


class Textures:
    def __init__(self):
        self.game = wardrobe_fx.Game()
        self.by_name = None

    def find(self, png):
        """BB's Texture2D for a rip PNG: by its Resources path, else by name (resources.assets, then sharedassets)."""
        try:
            rel = png.relative_to(ASSETS / "Resources").with_suffix("").as_posix().lower()
        except ValueError:
            rel = None
        if rel and rel in self.game.container:
            o = self.game.obj(self.game.container[rel], self.game.files["mainData"])
            if o is not None and o.type.name == "Texture2D":
                return o
        if self.by_name is None:                   # every Texture2D by name: resources.assets, then the sharedassets
            import UnityPy
            for name in sorted(os.listdir(wardrobe_fx.GAME)):
                if name.startswith("sharedassets") and name.endswith(".assets") and name not in self.game.files:
                    env = UnityPy.load(os.path.join(wardrobe_fx.GAME, name))
                    self.game.files.update({os.path.basename(k): f for k, f in env.files.items()})
            self.by_name = {}
            order = ["resources.assets"] + sorted(k for k in self.game.files if k.startswith("sharedassets"))
            for fname in order:
                for o in self.game.files[fname].objects.values():
                    if o.type.name == "Texture2D":
                        self.by_name.setdefault(o.read().m_Name, o)
        return self.by_name.get(png.stem)

    def image(self, png):
        o = self.find(png)
        return o.read().image if o is not None else None


def main():
    pngs = [p for base in SCAN if base.is_dir() for p in base.rglob("*.png")]
    broken = [p for p in pngs if not readable(p)]
    print(f"{len(broken)} unreadable of {len(pngs)} rip PNGs")
    if not broken:
        return
    tex = Textures()
    # self-check: intact PNGs from the broken files' folders, exported the same way, must equal the rip's
    folders = sorted({p.parent for p in broken})
    probes = [q for f in folders for q in sorted(f.glob("*.png")) if q not in broken and readable(q)][:6]
    for q in probes:
        mine = tex.image(q)
        if mine is None:
            continue
        with Image.open(q) as ref:
            diff = ImageChops.difference(ref.convert("RGBA"), mine.convert("RGBA")).getbbox() if ref.size == mine.size else "size"
        if diff:
            sys.exit(f"self-check failed: {q.name} exported from BB's data differs from the rip's ({diff}); nothing written")
    print(f"self-check: {len(probes)} intact PNGs match the rip pixel for pixel")
    done, missing = 0, []
    for p in broken:
        im = tex.image(p)
        if im is None:
            missing.append(p.relative_to(ASSETS).as_posix()); continue
        dst = OUT / p.relative_to(ASSETS)
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.save(dst, "PNG")
        done += 1
    print(f"exported {done} to {OUT}" + (f"; not in BB's data: {missing}" if missing else ""))


if __name__ == "__main__":
    main()
