"""Tests for pipeline/wardrobe_community.py (community skins: approved Discord submissions -> wardrobe/data).
  cd /d D:\\12tails-wardrobe && py -3 -m unittest pipeline.test_wardrobe_community -v"""
import io
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from pipeline import wardrobe_community as wc


def png(w, h, color=(200, 30, 30, 255), fmt="PNG"):
    b = io.BytesIO()
    Image.new("RGBA", (w, h), color).save(b, fmt)
    return b.getvalue()


class Community(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = self.d = Path(self.tmp.name)
        (d / "sheep" / "tex").mkdir(parents=True)
        (d / "props" / "tex").mkdir(parents=True)
        (d / "all").mkdir()
        (d / "sheep" / "outfits.json").write_text(json.dumps([{"name": "standard", "colors": [1, 2]}, {"name": "nude", "colors": []}]))
        Image.new("RGB", (16, 16)).save(d / "sheep" / "tex" / "standard1.webp")
        (d / "sheep" / "props_weapons.json").write_text(json.dumps([{"name": "halloweenLantern", "nodes": [{"mats": [{"tex": "Lantern.png"}]}]},
                                                                    {"name": "ttoStaff", "tto": True, "nodes": [{"mats": [{"tex": "Lantern.png"}]}]}]))
        (d / "all" / "props_trinkets.json").write_text(json.dumps([{"name": "Azure_Wing", "nodes": [{"mats": [{"tex": "Wing.png"}, {"tex": "Wing2.png"}]}]}]))
        for n, s in (("Lantern.png", 8), ("Wing.png", 8), ("Wing2.png", 4)):
            Image.new("RGBA", (s, s)).save(d / "props" / "tex" / n)

    def tearDown(self):
        self.tmp.cleanup()

    def sub(self, mid, cls="sheep", kind="weapons", item="halloweenLantern", tex=(("Lantern.png", 8),), name="นักวาด", link="", at="2026-11-11T10:00:00Z"):
        meta = {"v": 1, "cls": cls, "kind": kind, "item": item, "name": name, "link": link, "at": at,
                "textures": [{"tex": t, "file": f"skin{i}.png", "w": s, "h": s} for i, (t, s) in enumerate(tex)]}
        return mid, meta, {f"skin{i}.png": png(s, s) for i, (t, s) in enumerate(tex)}, at

    def test_adds_writes_webp_and_mirrors_removals(self):
        added, removed, refused = wc.apply(self.d, [self.sub("111"), self.sub("222", kind="outfits", item="standard", tex=(("", 16),), link="https://x.example/a")])
        self.assertEqual((added, removed, refused), (["111", "222"], [], []))
        j = json.loads((self.d / "community.json").read_text(encoding="utf-8"))["sets"]
        self.assertEqual([s["id"] for s in j], ["111", "222"])
        self.assertEqual(j[0]["pieces"], [{"slot": "R", "kind": "weapons", "item": "halloweenLantern", "owner": "sheep", "tex": {"Lantern.png": "community/sheep/111_0.webp"}}])
        self.assertEqual((j[0]["face"], j[0]["thumb"]), (None, None))              # the first format: no face, no preview
        self.assertEqual(j[1]["link"], "https://x.example/a")
        with Image.open(self.d / "community/sheep/111_0.webp") as im:
            self.assertEqual((im.format, im.size), ("WEBP", (8, 8)))
        added, removed, refused = wc.apply(self.d, [self.sub("222", kind="outfits", item="standard", tex=(("", 16),))])
        self.assertEqual((added, removed), ([], ["111"]))
        self.assertFalse((self.d / "community/sheep/111_0.webp").exists())
        self.assertTrue((self.d / "community/sheep/222_0.webp").exists())
        self.assertEqual(wc.old_ids(self.d), {"222"})

    def test_shared_piece_keeps_its_owner_and_both_textures(self):
        wc.apply(self.d, [self.sub("333", kind="trinkets", item="Azure_Wing", tex=(("Wing.png", 8), ("Wing2.png", 4)))])
        s = json.loads((self.d / "community.json").read_text(encoding="utf-8"))["sets"][0]
        self.assertEqual(s["cls"], "sheep")
        self.assertEqual(s["pieces"][0]["owner"], "all")
        self.assertEqual(s["pieces"][0]["tex"], {"Wing.png": "community/sheep/333_0.webp", "Wing2.png": "community/sheep/333_1.webp"})

    def look(self, mid, pieces, preview=True, face=38, at="2026-11-12T10:00:00Z"):
        """a whole look (meta v2): pieces = [(slot, kind, item, [(tex, size)])]"""
        n, defs, files = 0, [], {}
        for slot, kind, item, texs in pieces:
            ts = []
            for t, s in texs:
                files[f"skin{n}.png"] = png(s, s)
                ts.append({"tex": t, "file": f"skin{n}.png", "w": s, "h": s})
                n += 1
            defs.append({"slot": slot, "kind": kind, "item": item, "textures": ts})
        if preview:
            b = io.BytesIO()
            Image.new("RGB", (30, 40), (200, 200, 190)).save(b, "JPEG")
            files["preview.jpg"] = b.getvalue()
        return mid, {"v": 2, "cls": "sheep", "name": "ผู้ส่งชุด", "link": "", "face": face, "at": at, "pieces": defs}, files, at

    def test_a_whole_look_is_one_set_with_its_face_and_thumbnail(self):
        added, _, refused = wc.apply(self.d, [self.look("500", [("outfit", "outfits", "standard", [("", 16)]), ("R", "weapons", "halloweenLantern", [("Lantern.png", 8)])])])
        self.assertEqual((added, refused), (["500"], []))
        s = json.loads((self.d / "community.json").read_text(encoding="utf-8"))["sets"][0]
        self.assertEqual((s["face"], s["thumb"]), (38, "community/sheep/500_p.webp"))
        self.assertEqual([(p["slot"], p["item"], list(p["tex"].values())) for p in s["pieces"]],
                         [("outfit", "standard", ["community/sheep/500_0.webp"]), ("R", "halloweenLantern", ["community/sheep/500_1.webp"])])
        with Image.open(self.d / s["thumb"]) as im:
            self.assertEqual(im.format, "WEBP")

    def test_a_look_drops_a_piece_it_cannot_carry_and_is_refused_when_none_is_left(self):
        added, _, refused = wc.apply(self.d, [self.look("501", [("outfit", "outfits", "standard", [("", 16)]), ("R", "weapons", "ttoStaff", [("Lantern.png", 8)])], preview=False)])
        s = json.loads((self.d / "community.json").read_text(encoding="utf-8"))["sets"][0]
        self.assertEqual((added, refused, [p["item"] for p in s["pieces"]], s["thumb"]), (["501"], [], ["standard"], None))   # the TTO staff is left out
        _, _, refused = wc.apply(self.d, [self.look("502", [("R", "weapons", "ttoStaff", [("Lantern.png", 8)])])])
        self.assertEqual([i for i, _ in refused], ["502"])

    def test_refusals(self):
        bad = [self.sub("1", item="nothing"), self.sub("2", tex=(("Lantern.png", 12),)), self.sub("3", kind="outfits", item="nude", tex=(("", 16),)),
               self.sub("4", name="  "), self.sub("5", link="http://plain.example"), self.sub("6", tex=(("Other.png", 8),)),
               self.sub("7", kind="hats"), self.sub("9", item="ttoStaff")]
        m, meta, files, at = self.sub("8")
        files = {"skin0.png": png(8, 8, fmt="BMP")}
        bad.append((m, meta, files, at))
        added, removed, refused = wc.apply(self.d, bad)
        self.assertEqual(added, [])
        self.assertEqual(sorted(i for i, _ in refused), [str(i) for i in range(1, 10)])
        self.assertIn("TTO", dict(refused)["9"])
        self.assertIn("12x12, the original 8x8", dict(refused)["2"])
        self.assertIn("not a PNG", dict(refused)["8"])

    def test_a_high_res_skin_is_kept(self):
        # exactly 2x of the original (8 -> 16): in, at its own size (the page's skinDims; user 2026-11-12)
        added, _, refused = wc.apply(self.d, [self.sub("1", tex=(("Lantern.png", 16),))])
        self.assertEqual((added, refused), (["1"], []))
        with Image.open(self.d / "community/sheep/1_0.webp") as im:
            self.assertEqual(im.size, (16, 16))

    def test_files_of_finds_the_embed_picture(self):
        # Discord's real shape: the embed's image is not listed in attachments (2026-11-12, the first live send)
        m = {"attachments": [{"filename": "meta.json", "url": "https://cdn.discordapp.com/attachments/1/2/meta.json?ex=a"}],
             "embeds": [{"image": {"url": "https://cdn.discordapp.com/attachments/1/3/skin0.png?ex=b&is=c"}}]}
        self.assertEqual(wc.files_of(m), {"meta.json": "https://cdn.discordapp.com/attachments/1/2/meta.json?ex=a",
                                          "skin0.png": "https://cdn.discordapp.com/attachments/1/3/skin0.png?ex=b&is=c"})

    def test_dry_run_writes_nothing(self):
        added, _, _ = wc.apply(self.d, [self.sub("9")], dry=True)
        self.assertEqual(added, ["9"])
        self.assertFalse((self.d / "community.json").exists())
        self.assertFalse((self.d / "community").exists())


if __name__ == "__main__":
    unittest.main()
