r"""Tests for wardrobe_fx.py's texture files (2026-11-13, the Whale's build): every class's effect textures share one
folder, data/fx/tex, and two different textures of one name must never replace one another (TEX_FILES, save_texture).

  cd /d D:\12tails-wardrobe && py -3 -m unittest pipeline.test_wardrobe_fx_textures -v
"""
import sys
import tempfile
import types
import unittest
from pathlib import Path

from PIL import Image

sys.modules.setdefault("UnityPy", types.ModuleType("UnityPy"))   # the module only needs it to read the game's files
from pipeline import wardrobe_fx as W  # noqa: E402


def picture(seed, size=(64, 64)):
    """A picture with large shapes (so its WebP stays close to it): different seeds, different pictures."""
    im = Image.new("RGBA", size, (0, 0, 0, 0))
    for i in range(size[0]):
        for j in range(size[1]):
            on = ((i // 16 + j // 16 + seed) % 2) == 0
            im.putpixel((i, j), ((40 * seed) % 256, 200 if on else 30, (90 * seed) % 256, 255 if on else 60))
    return im


def size(path):
    with Image.open(path) as im:
        return im.size


class Obj:
    """A stand-in for a UnityPy texture object: its file, its pathID, its name."""

    def __init__(self, file, path_id, name):
        self.assets_file = types.SimpleNamespace(name=file)
        self.path_id = path_id
        self._name = name

    def read(self):
        return types.SimpleNamespace(m_Name=self._name)


class TextureFiles(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_new_texture_is_written(self):
        self.assertTrue(W.save_texture(str(self.dir), "ring", picture(1)))
        self.assertEqual(size(self.dir / "ring.webp"), (64, 64))

    def test_the_same_picture_keeps_the_file_as_it_is(self):
        W.save_texture(str(self.dir), "ring", picture(1))
        before = (self.dir / "ring.webp").read_bytes()
        self.assertFalse(W.save_texture(str(self.dir), "ring", picture(1)))
        self.assertEqual((self.dir / "ring.webp").read_bytes(), before)

    def test_another_picture_under_the_same_name_stops_the_build(self):
        W.save_texture(str(self.dir), "nAttack_hit1", picture(1))
        before = (self.dir / "nAttack_hit1.webp").read_bytes()
        with self.assertRaises(SystemExit) as e:
            W.save_texture(str(self.dir), "nAttack_hit1", picture(2))
        self.assertIn("TEX_FILES", str(e.exception))
        self.assertEqual((self.dir / "nAttack_hit1.webp").read_bytes(), before)

    def test_another_size_under_the_same_name_stops_the_build(self):
        W.save_texture(str(self.dir), "castRing", picture(1, (64, 64)))
        with self.assertRaises(SystemExit):
            W.save_texture(str(self.dir), "castRing", picture(1, (32, 32)))

    def test_a_name_that_differs_only_in_case_stops_the_build(self):
        W.save_texture(str(self.dir), "ShadowRay", picture(1))
        with self.assertRaises(SystemExit) as e:
            W.save_texture(str(self.dir), "shadowRay", picture(1))
        self.assertIn("case", str(e.exception))
        self.assertEqual(sorted(p.name for p in self.dir.iterdir()), ["ShadowRay.webp"])

    def test_retex_writes_over_a_changed_picture(self):
        W.save_texture(str(self.dir), "tto_RuneGolem", picture(1))
        self.assertTrue(W.save_texture(str(self.dir), "tto_RuneGolem", picture(2, (32, 32)), replace=True))
        self.assertEqual(size(self.dir / "tto_RuneGolem.webp"), (32, 32))

    def test_a_clashing_texture_takes_its_own_file_name(self):
        self.assertEqual(W.tex_name(Obj("sharedassets4.assets", 48, "nAttack_hit1")), "whale_nAttack_hit1")
        self.assertEqual(W.tex_name(Obj("sharedassets11.assets", 62, "castRing")), "sheep_castRing")
        self.assertEqual(W.tex_name(Obj("sharedassets12.assets", 55, "shadowRay")), "bat_shadowRay")
        # every other texture keeps its own name: the Cat's nAttack_hit1, the Penguin's castRing, the shared ShadowRay
        self.assertEqual(W.tex_name(Obj("sharedassets5.assets", 43, "nAttack_hit1")), "nAttack_hit1")
        self.assertEqual(W.tex_name(Obj("sharedassets10.assets", 38, "castRing")), "castRing")
        self.assertEqual(W.tex_name(Obj("sharedassets1.assets", 79, "ShadowRay")), "ShadowRay")

    def test_no_two_clashing_textures_share_a_file_name(self):
        names = list(W.TEX_FILES.values())
        self.assertEqual(len(names), len({n.lower() for n in names}))


if __name__ == "__main__":
    unittest.main()
