r"""Tests for wardrobe_props_tex.py: the prop textures the wardrobe's props JSON names are copied into its own data.

  cd /d D:\12tails-wardrobe && py -3 -m unittest pipeline.test_wardrobe_props_tex -v
"""
import json
import tempfile
import unittest
from pathlib import Path

from pipeline.wardrobe_props_tex import copy_prop_textures


def props(*texes):
    """One props_<kind>.json list: a prop with one node per texture name."""
    return [{"name": "p", "tto": False, "mount": None,
             "nodes": [{"name": f"n{i}", "mats": [{"tex": t, "color": [1, 1, 1, 1]}]} for i, t in enumerate(texes)]}]


class CopyPropTextures(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.data, self.src = root / "data", root / "src"
        (self.data / "cat").mkdir(parents=True)
        self.src.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def write_props(self, cls, kind, *texes):
        (self.data / cls).mkdir(exist_ok=True)
        (self.data / cls / f"props_{kind}.json").write_text(json.dumps(props(*texes)), encoding="utf-8")

    def test_copies_referenced_only(self):
        self.write_props("cat", "weapons", "a.png", "b.png")
        for n in ("a.png", "b.png", "c.png"):
            (self.src / n).write_bytes(n.encode())
        self.assertEqual(copy_prop_textures(self.data, self.src), (2, []))
        self.assertEqual(sorted(p.name for p in (self.data / "props" / "tex").iterdir()), ["a.png", "b.png"])
        self.assertEqual((self.data / "props" / "tex" / "a.png").read_bytes(), b"a.png")

    def test_missing_texture_reported(self):
        self.write_props("cat", "weapons", "x.png")
        self.assertEqual(copy_prop_textures(self.data, self.src), (0, ["x.png"]))

    def test_existing_copy_kept(self):
        self.write_props("cat", "weapons", "a.png")
        (self.src / "a.png").write_bytes(b"new")
        (self.data / "props" / "tex").mkdir(parents=True)
        (self.data / "props" / "tex" / "a.png").write_bytes(b"mine")
        self.assertEqual(copy_prop_textures(self.data, self.src), (0, []))
        self.assertEqual((self.data / "props" / "tex" / "a.png").read_bytes(), b"mine")

    def test_shared_all_folder_and_mats_without_tex(self):
        self.write_props("all", "accessories", "s.png")
        (self.data / "cat" / "props_trinkets.json").write_text(json.dumps(
            [{"name": "q", "nodes": [{"name": "n", "mats": [{"color": [1, 1, 1, 1]}]}, {"name": "m"}]}]), encoding="utf-8")
        (self.src / "s.png").write_bytes(b"s")
        self.assertEqual(copy_prop_textures(self.data, self.src), (1, []))


if __name__ == "__main__":
    unittest.main()
