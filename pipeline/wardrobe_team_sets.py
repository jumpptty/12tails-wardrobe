r"""The team's own looks in the ลายผู้เล่น gallery (2026-11-12; user: "please add our Rabbit and Cat creation in it too"):
the repaints built by wardrobe_repaint.py (the Rabbit's summer set as a school uniform, A and B) and wardrobe_knight.py
(the Cat's champion as the reference's knight, with her hair), credited ทีมงาน. They live in wardrobe/data/team_sets.json
(+ data/team/<cls>/<id>_<n>.webp, <id>_p.webp), apart from community.json: the Discord import mirrors that file from the
channel and would drop anything not posted there. The page shows both; the publish carries both (its TTO / published
rules apply to each piece). Run after rebuilding the repaints:
  uv run --no-project --with pillow --with numpy --with scipy --with playwright python -I pipeline/wardrobe_repaint.py --preview
  uv run --no-project --with pillow --with numpy --with scipy --with playwright python -I pipeline/wardrobe_knight.py --paint
  uv run --no-project --with pillow --with numpy --with scipy --with playwright python -I pipeline/wardrobe_team_sets.py
(a friend's set needs its files: DeetaeZ's are in the home PC's archive; elsewhere it is left out with a line saying so)"""
import asyncio, io, json, shutil, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DATA, R = ROOT / "wardrobe" / "data", ROOT / "plans" / "reskins"
sys.stdout.reconfigure(encoding="utf-8")
CREDIT = "ทีมงาน"
AT = "2026-11-12T12:00:00Z"
# the user's friend DeetaeZ's Whale legend set (user 2026-11-12: "if you have DeetaeZ skin (my friend Whale legend) also
# put that set in there too"; DeetaeZ agreed to be named, the trailer credits them, video NOTES.md): their ToT uploads,
# archived on the home PC only (D:\12tails-assets-archive). The weapon texture is the lance + shield atlas: both pieces.
# Left out (with a line saying so) where the archive is missing; its picture is shot from the local page
ARCHIVE = Path(r"D:\12tails-assets-archive\tot-skins-2026-11-07")
FRIENDS = [  # id, class, credit, face, [(slot, kind, item, {texture name: file})]
    ("friend-whale-legend-deetaez", "whale", "DeetaeZ", None,
     [("outfit", "outfits", "legend", {"": ARCHIVE / "Armor" / "[DeetaeZ]1783268358_777.png"}),
      ("Head", "accessories", "legendHelmet", {"Whale_legendHelmet.png": ARCHIVE / "Accessory" / "[DeetaeZ]1783268338_829.png"}),
      ("R", "weapons", "legendLance", {"Whale_legendWeapon.png": ARCHIVE / "Weapon" / "[DeetaeZ]1783268376_830.png"}),
      ("L", "weapons", "legendShield", {"Whale_legendWeapon.png": ARCHIVE / "Weapon" / "[DeetaeZ]1783268376_830.png"})]),
]
SETS = [  # id, class, face, the picture (a shot from the front), [(slot, kind, item, {texture name: file})]
    # face 23 (purple eyes): the knight's renders use 38, a TTO face the public copy does not carry
    ("team-cat-knight", "cat", 23, R / "cat" / "shots" / "knight_front.png",
     [("outfit", "outfits", "champion", {"": R / "cat" / "knight" / "champion.png"}),
      ("Head", "accessories", "default", {"Cat_default.png": R / "cat" / "knight" / "Cat_default.png"})]),
    ("team-rabbit-uniform-a", "rabbit", None, R / "rabbit" / "shots" / "uniform_A_hat_front.png",
     [("outfit", "outfits", "summer", {"": R / "rabbit" / "summer_uniform_A" / "summer.png"}),
      ("Head", "accessories", "summerHat", {"Rabbit_summerHat.png": R / "rabbit" / "summer_uniform_A" / "Rabbit_summerHat.png"})]),
    ("team-rabbit-uniform-b", "rabbit", None, R / "rabbit" / "shots" / "uniform_B_hat_front.png",
     [("outfit", "outfits", "summer", {"": R / "rabbit" / "summer_uniform_B" / "summer.png"}),
      ("Head", "accessories", "summerHat", {"Rabbit_summerHat.png": R / "rabbit" / "summer_uniform_B" / "Rabbit_summerHat.png"})]),
]


def thumb(shot):
    """the square front shot -> 360 x 480 (the cards' 3:4), the hero centred, the shot's own light ground"""
    im = Image.open(shot).convert("RGB")
    w, h = im.size
    cw = round(h * 3 / 4)
    im = im.crop(((w - cw) // 2, 0, (w - cw) // 2 + cw, h)).resize((360, 480), Image.LANCZOS)
    b = io.BytesIO()
    im.save(b, "WEBP", quality=85, method=6)
    return b.getvalue()


def original_size(kind, cls, item, name):
    return Image.open(DATA / cls / "tex" / f"{item}1.webp").size if kind == "outfits" else Image.open(DATA / "props" / "tex" / name).size


def friend_shots(todo):
    """a front shot of each friend's set on the local page (wardrobe_repaint.shots), under plans/reskins/<cls>/shots"""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from wardrobe_repaint import shots
    for sid, cls, credit, face, pieces in todo:
        tmp = R / cls / "_friend"
        tmp.mkdir(parents=True, exist_ok=True)
        skins, props = {}, {}
        for slot, kind, item, texs in pieces:
            for name, f in texs.items():
                dst = tmp / f"{sid}_{item}.png"
                Image.open(f).convert("RGBA").resize(original_size(kind, cls, item, name), Image.LANCZOS).save(dst)
                skins[f"{cls}|{kind}|{item}|{name}"] = dst
            if slot != "outfit":
                props[slot] = item
        outfit = next(i for s, k, i, t in pieces if s == "outfit")
        asyncio.run(shots(cls, outfit, [(sid, skins, props)], R / cls, yaws=((20, "front"),), size=640, face=face))


def main():
    out = DATA / "team"
    if out.exists():
        shutil.rmtree(out)
    sets = []
    ready = [f for f in FRIENDS if all(p.exists() for *_, texs in f[4] for p in texs.values())]
    for f in FRIENDS:
        if f not in ready:
            print(f"{f[0]}: left out, its files are not on this PC ({ARCHIVE})")
    if ready:
        friend_shots(ready)
    todo = [(sid, cls, CREDIT, face, shot, pieces) for sid, cls, face, shot, pieces in SETS]
    todo += [(sid, cls, credit, face, R / cls / "shots" / f"{sid}_front.png", pieces) for sid, cls, credit, face, pieces in ready]
    for sid, cls, credit, face, shot, pieces in todo:
        d = out / cls
        d.mkdir(parents=True, exist_ok=True)
        n, ps = 0, []
        for slot, kind, item, texs in pieces:
            tex = {}
            for name, f in texs.items():
                rel = f"team/{cls}/{sid}_{n}.webp"
                n += 1
                im = Image.open(f).convert("RGBA")
                w, h = original_size(kind, cls, item, name)          # the original's size or 2x / 4x / 8x of it (skinDims)
                if not any(im.size == (w * k, h * k) for k in (1, 2, 4, 8)):
                    print(f"  {sid}: {f.name} is {im.size[0]}x{im.size[1]}, scaled to {w}x{h}")
                    im = im.resize((w, h), Image.LANCZOS)
                im.save(DATA / rel, "WEBP", quality=92, alpha_quality=100, method=6)
                tex[name] = rel
            ps.append({"slot": slot, "kind": kind, "item": item, "owner": cls, "tex": tex})
        (d / f"{sid}_p.webp").write_bytes(thumb(shot))
        sets.append({"id": sid, "cls": cls, "name": credit, "link": "", "at": AT, "face": face, "thumb": f"team/{cls}/{sid}_p.webp", "pieces": ps})
        print(sid, n, "textures")
    (DATA / "team_sets.json").write_text(json.dumps({"sets": sets}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", DATA / "team_sets.json", sum(p.stat().st_size for p in out.rglob("*")) // 1024, "KB")


if __name__ == "__main__":
    main()
