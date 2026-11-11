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
        j = json.loads((self.d / "community.json").read_text(encoding="utf-8"))["skins"]
        self.assertEqual([s["id"] for s in j], ["111", "222"])
        self.assertEqual(j[0]["tex"], {"Lantern.png": "community/sheep/111_0.webp"})
        self.assertEqual(j[1]["link"], "https://x.example/a")
        with Image.open(self.d / "community/sheep/111_0.webp") as im:
            self.assertEqual((im.format, im.size), ("WEBP", (8, 8)))
        added, removed, refused = wc.apply(self.d, [self.sub("222", kind="outfits", item="standard", tex=(("", 16),))])
        self.assertEqual((added, removed), ([], ["111"]))
        self.assertFalse((self.d / "community/sheep/111_0.webp").exists())
        self.assertTrue((self.d / "community/sheep/222_0.webp").exists())

    def test_shared_piece_goes_under_all_with_both_textures(self):
        wc.apply(self.d, [self.sub("333", kind="trinkets", item="Azure_Wing", tex=(("Wing.png", 8), ("Wing2.png", 4)))])
        s = json.loads((self.d / "community.json").read_text(encoding="utf-8"))["skins"][0]
        self.assertEqual(s["cls"], "all")
        self.assertEqual(s["tex"], {"Wing.png": "community/all/333_0.webp", "Wing2.png": "community/all/333_1.webp"})

    def test_refusals(self):
        bad = [self.sub("1", item="nothing"), self.sub("2", tex=(("Lantern.png", 16),)), self.sub("3", kind="outfits", item="nude", tex=(("", 16),)),
               self.sub("4", name="  "), self.sub("5", link="http://plain.example"), self.sub("6", tex=(("Other.png", 8),)),
               self.sub("7", kind="hats"), self.sub("9", item="ttoStaff")]
        m, meta, files, at = self.sub("8")
        files = {"skin0.png": png(8, 8, fmt="BMP")}
        bad.append((m, meta, files, at))
        added, removed, refused = wc.apply(self.d, bad)
        self.assertEqual(added, [])
        self.assertEqual(sorted(i for i, _ in refused), [str(i) for i in range(1, 10)])
        self.assertIn("TTO", dict(refused)["9"])
        self.assertIn("16x16, the original 8x8", dict(refused)["2"])
        self.assertIn("not a PNG", dict(refused)["8"])

    def test_dry_run_writes_nothing(self):
        added, _, _ = wc.apply(self.d, [self.sub("9")], dry=True)
        self.assertEqual(added, ["9"])
        self.assertFalse((self.d / "community.json").exists())
        self.assertFalse((self.d / "community").exists())


if __name__ == "__main__":
    unittest.main()
