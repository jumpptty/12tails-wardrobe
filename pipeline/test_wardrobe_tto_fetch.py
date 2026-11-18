import unittest

from pipeline.wardrobe_tto_fetch import bundles_for, require_bundles

ROWS = [
    ["gameassets/characters/pet/smallanubi", "UnityEngine.GameObject", "x", "a.bundle b.bundle"],
    ["gameassets/characters/heroes/bat/weapons/x", "UnityEngine.GameObject", "x", "c.bundle"],
]


class BundlesForTest(unittest.TestCase):
    def test_bundles_for_takes_every_listed_bundle_of_matching_rows(self):
        self.assertEqual(bundles_for(ROWS, "characters/pets?/"), {"a.bundle", "b.bundle"})

    def test_bundles_for_no_match_is_empty(self):
        self.assertEqual(bundles_for(ROWS, "nothing/here"), set())

    def test_require_bundles_returns_the_bundles_of_a_matching_pattern(self):
        self.assertEqual(require_bundles(ROWS, "characters/pets?/"), {"a.bundle", "b.bundle"})

    def test_require_bundles_exits_when_a_pattern_matches_nothing(self):
        with self.assertRaises(SystemExit) as cm:
            require_bundles(ROWS, "characters/petz/")
        self.assertIn("characters/petz/", str(cm.exception.code))


if __name__ == "__main__":
    unittest.main()
