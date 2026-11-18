r"""Tests for wardrobe_convert.py: the Unity -> three.js conversion of meshes and clips shared by wardrobe_data.py and the
pet extractor (x mirrored, quaternions (x, -y, -z, w), triangle winding chosen to agree with the normals).

  cd /d D:\12tails-wardrobe && py -3 -m unittest pipeline.test_wardrobe_convert -v
"""
import os
import tempfile
import unittest
from unittest import mock

from pipeline import wardrobe_convert
from pipeline.wardrobe_convert import ADDITIVE_ALPHA, clip_dict, game_shader, mirror_rows, prop_mats, prop_mesh


class PropMesh(unittest.TestCase):
    def test_prop_mesh_mirrors_x_and_keeps_winding_with_normals(self):
        # one triangle in Unity space, counter-clockwise seen from +z; the normals point +z
        M = {"pos": [[0, 0, 0], [1, 0, 0], [0, 1, 0]], "nrm": [[0, 0, 1]] * 3,
             "uv0": [[0, 0], [1, 0], [0, 1]], "subs": [[[0, 1, 2]]]}
        out = prop_mesh(M, 1)
        self.assertEqual(out["pos"], [0, 0, 0, -1, 0, 0, 0, 1, 0])      # x negated (-0.0 == 0)
        self.assertEqual(out["nrm"], [0, 0, 1] * 3)
        # mirroring x reverses the winding, so the order that agrees with +z normals is (0, 2, 1)
        self.assertEqual(out["idx"], [0, 2, 1])
        self.assertEqual(out["groups"], [[0, 3, 0]])
        self.assertEqual(out["uv"], [0, 0, 1, 0, 0, 1])


class MirrorRows(unittest.TestCase):
    def test_mirror_rows_negates_q_y_z_and_p_x(self):
        row = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.assertEqual(mirror_rows([row], "q"), [[0, 1, -2, -3, 4, 5, -6, -7, 8, 9, -10, -11, 12]])
        self.assertEqual(mirror_rows([row], "p"), [[0, -1, 2, 3, -4, 5, 6, -7, 8, 9, 10, 11, 12]])
        self.assertEqual(mirror_rows([row], "s"), [row])


class ClipDict(unittest.TestCase):
    def test_clip_dict_reads_legacy_curves(self):
        def key(t, v, i, o):
            return {"time": t, "value": dict(zip("xyzw", v)), "inSlope": dict(zip("xyzw", i)),
                    "outSlope": dict(zip("xyzw", o))}
        tt = {"m_SampleRate": 30.0, "m_WrapMode": 2,
              "m_RotationCurves": [{"path": "Root/Head", "curve": {"m_Curve": [
                  key(0.0, (0.1, 0.2, 0.3, 0.9), (1, 2, 3, 4), (5, 6, 7, 8)),
                  key(0.5, (0.0, 0.0, 0.0, 1.0), (0, 0, 0, 0), (0, 0, 0, 0))]}}],
              "m_PositionCurves": [], "m_ScaleCurves": []}
        out = clip_dict(tt)
        self.assertEqual(list(out["tracks"]), ["Head"])
        self.assertEqual(out["tracks"]["Head"]["q"][0],
                         [0.0, 0.1, -0.2, -0.3, 0.9, 1, -2, -3, 4, 5, -6, -7, 8])
        self.assertEqual(out["len"], 0.5)
        self.assertEqual(out["rate"], 30.0)
        self.assertTrue(out["loop"])
        tt["m_WrapMode"] = 1
        self.assertFalse(clip_dict(tt)["loop"])


class GameShader(unittest.TestCase):
    """BB's material of the texture's name in the Bible's rip (Assets/Material/<tex>.mat) -> the page's shader hint."""

    def mats(self, files):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        for name, text in files.items():
            with open(os.path.join(d.name, name), "w", encoding="utf-8") as f:
                f.write(text)
        return mock.patch.object(wardrobe_convert, "BIBLE_MATS", d.name)

    def test_builtin_diffuse_is_opaque(self):
        with self.mats({"littleCarron.mat": "  m_Shader: {fileID: 7, guid: 0000000000000000e000000000000000, type: 0}\n"}):
            self.assertEqual(game_shader("littleCarron.png"), {"shader": "opaque"})

    def test_additive_alpha_takes_its_range_as_the_cut(self):
        mat = (f"  m_Shader: {{fileID: 4800000, guid: {ADDITIVE_ALPHA}, type: 3}}\n"
               "    - first:\n        name: _AdditiveRange\n      second: 0.8\n")
        with self.mats({"champ.mat": mat}):
            self.assertEqual(game_shader("champ.png"), {"shader": "addAlpha", "cut": 0.8})

    def test_no_material_and_tto_items_get_no_hint(self):
        with self.mats({}):
            self.assertEqual(game_shader("nothing.png"), {})
            self.assertEqual(game_shader(None), {})
            self.assertEqual(prop_mats([{"tex": "nothing.png", "color": [1, 0.5, 0.25, 1]}], True),
                             [{"tex": "nothing.png", "color": [1, 0.5, 0.25, 1]}])


if __name__ == "__main__":
    unittest.main()
