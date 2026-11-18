import unittest

from pipeline.wardrobe_tto_fetch import bundles_for

ROWS = [
    ["gameassets/characters/pet/smallanubi", "UnityEngine.GameObject", "x", "a.bundle b.bundle"],
    ["gameassets/characters/heroes/bat/weapons/x", "UnityEngine.GameObject", "x", "c.bundle"],
]


class BundlesForTest(unittest.TestCase):
    def test_bundles_for_takes_every_listed_bundle_of_matching_rows(self):
        self.assertEqual(bundles_for(ROWS, "characters/pets?/"), {"a.bundle", "b.bundle"})

    def test_bundles_for_no_match_is_empty(self):
        self.assertEqual(bundles_for(ROWS, "nothing/here"), set())


if __name__ == "__main__":
    unittest.main()
