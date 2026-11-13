"""wardrobe_icons_upscale.py: the parts that need no GPU (the names, the sizes, the data builds' keep()).

  py -3 -m unittest pipeline.test_wardrobe_icons_upscale
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wardrobe_icons_upscale as up  # noqa: E402


def gradient(size=64, shift=0):
    im = Image.new("RGBA", (size, size))
    im.putdata([((40 + 3 * x + shift) % 256, 20 + 2 * y, 120, 0 if x < 6 and y < 6 else 255) for y in range(size) for x in range(size)])
    return im


class UpscaleTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.icons = Path(self.tmp.name) / "icons"
        (self.icons / "weapon").mkdir(parents=True)
        (self.icons / "hd" / "cat").mkdir(parents=True)
        up._manifests.clear()

    def tearDown(self):
        self.tmp.cleanup()

    def test_sizes(self):
        self.assertEqual(up.target_size((64, 64)), (128, 128))
        self.assertEqual(up.target_size((51, 51)), (128, 128))       # TTO's own art, as the Bible does
        self.assertEqual(up.target_size((75, 75)), (150, 150))       # the class portraits
        self.assertTrue(up.is_game_size((75, 75)))
        self.assertFalse(up.is_game_size((128, 128)))

    def test_bible_keys(self):
        self.assertEqual(up.bible_key("armor/bat5.webp"), "a_bat5")
        self.assertEqual(up.bible_key("weapon/wlf40.webp"), "w_wlf40")
        self.assertEqual(up.bible_key("accessory/rab52.webp"), "c_rab52")
        self.assertEqual(up.bible_key("trinket/all20.webp"), "t_all20")
        self.assertEqual(up.bible_key("skills/wolf/cattack1.webp"), "wolf_cattack1")
        self.assertEqual(up.bible_key("skills/support/seaaegis.webp"), "sup_seaaegis")
        for rel in ("acessory/all5.webp", "skills/emotion/wai.webp", "heroes/bat1.webp"):
            self.assertIsNone(up.bible_key(rel), rel)                # TTO's own folder, emotes, portraits: not in the Bible

    def test_game_size_icons_listed_without_hd(self):
        gradient().save(self.icons / "weapon" / "a.webp", "WEBP", lossless=True)
        gradient(128).save(self.icons / "weapon" / "b.webp", "WEBP", quality=90)
        gradient().save(self.icons / "hd" / "cat" / "c.webp", "WEBP", lossless=True)
        self.assertEqual(up.game_size_icons(self.icons), ["weapon/a.webp"])

    def test_keep_only_the_upscale_of_the_same_picture(self):
        """A data build must not write over an upscale made from the picture it holds; a changed or new picture, or a
        file still at game size, is written."""
        game, path = gradient(), self.icons / "weapon" / "a.webp"
        self.assertFalse(up.keep(path, game, self.icons))                         # no manifest, no file
        game.resize((128, 128), Image.LANCZOS).save(path, "WEBP", quality=90)
        (self.icons / up.MANIFEST).write_text(json.dumps({"weapon/a.webp": {"src": up.pixel_hash(game), "from": "esrgan"}}))
        up._manifests.clear()
        self.assertTrue(up.keep(path, game, self.icons))
        self.assertFalse(up.keep(path, gradient(shift=9), self.icons))            # the game's picture changed
        self.assertFalse(up.keep(self.icons / "weapon" / "new.webp", game, self.icons))
        game.save(path, "WEBP", lossless=True)                                    # the file is back at game size
        self.assertFalse(up.keep(path, game, self.icons))

    def test_difference(self):
        game = gradient()
        self.assertLess(up.difference(game, game.resize((128, 128), Image.LANCZOS)), 3)
        self.assertGreater(up.difference(game, Image.new("RGBA", (128, 128), (220, 120, 160, 255))), 20)


if __name__ == "__main__":
    unittest.main()
