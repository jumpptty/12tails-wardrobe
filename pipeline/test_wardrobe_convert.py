r"""Tests for wardrobe_convert.py: the Unity -> three.js conversion of meshes and clips shared by wardrobe_data.py and the
pet extractor (x mirrored, quaternions (x, -y, -z, w), triangle winding chosen to agree with the normals).

  cd /d D:\12tails-wardrobe && py -3 -m unittest pipeline.test_wardrobe_convert -v
"""
import unittest

from pipeline.wardrobe_convert import clip_dict, mirror_rows, prop_mesh


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


if __name__ == "__main__":
    unittest.main()
