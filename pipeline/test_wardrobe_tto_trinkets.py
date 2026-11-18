r"""Tests for wardrobe_tto_trinkets.py's pure rules: `merge` (replace an entry by name, keep the others' order) and
`meshes_only` (keep a mesh node and its ancestors, drop particle-only branches).

  cd /d D:\12tails-wardrobe-pets && py -3 -m unittest pipeline.test_wardrobe_tto_trinkets -v

Only pure functions are imported (no UnityPy, no Pillow): the bundle reading sits in wardrobe_tto_trinkets.main().
"""
import unittest

from pipeline.wardrobe_tto_trinkets import meshes_only, merge


def node(name, parent, mesh=False):
    n = {"name": name, "parent": parent, "p": [0, 0, 0], "q": [0, 0, 0, 1], "s": [1, 1, 1], "on": True}
    if mesh:
        n["mesh"] = {"pos": [], "nrm": None, "uv": None, "idx": [], "groups": []}
    return n


class Merge(unittest.TestCase):
    def test_replaces_by_name_and_keeps_the_order(self):
        entries = [{"name": "a"}, {"name": "aura_bloompulse", "old": True}, {"name": "b"}]
        out = merge(entries, [{"name": "aura_bloompulse", "new": True}])
        self.assertEqual([e["name"] for e in out], ["a", "aura_bloompulse", "b"])
        self.assertTrue(out[1].get("new"))
        self.assertFalse(out[1].get("old"))

    def test_appends_when_absent_and_does_not_touch_the_input(self):
        entries = [{"name": "a"}]
        out = merge(entries, [{"name": "aura_bloompulse"}])
        self.assertEqual([e["name"] for e in out], ["a", "aura_bloompulse"])
        self.assertEqual(len(entries), 1)

    def test_a_second_run_changes_nothing(self):
        new = [{"name": "aura_bloompulse", "v": 1}]
        once = merge([{"name": "a"}], new)
        self.assertEqual(merge(once, new), once)


class MeshesOnly(unittest.TestCase):
    def test_keeps_a_mesh_and_its_ancestors_and_drops_particle_branches(self):
        nodes = [node("root", -1),
                 node("Moat", 0, mesh=True),
                 node("Bloom", 0),                  # particles only
                 node("BloomSub", 2),               # particles only
                 node("Flower1", 0),                # no mesh itself, a mesh below
                 node("Inner", 4, mesh=True),
                 node("Pollen", 0)]
        out = meshes_only(nodes)
        self.assertEqual([n["name"] for n in out], ["root", "Moat", "Flower1", "Inner"])
        # parents are re-indexed into the kept list
        self.assertEqual([n["parent"] for n in out], [-1, 0, 0, 2])

    def test_does_not_touch_the_input(self):
        nodes = [node("root", -1), node("Bloom", 0), node("Moat", 0, mesh=True)]
        meshes_only(nodes)
        self.assertEqual(nodes[2]["parent"], 0)
        self.assertEqual(len(nodes), 3)

    def test_no_mesh_gives_nothing(self):
        self.assertEqual(meshes_only([node("root", -1), node("Bloom", 0)]), [])


if __name__ == "__main__":
    unittest.main()
