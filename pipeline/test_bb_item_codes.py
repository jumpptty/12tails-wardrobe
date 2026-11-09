r"""Tests for bb_item_codes.parse: item code -> model read by the braces of BB's obfuscated <Class>Equipment.cs (2026-11-09:
the old "load after the last compare" rule gave Chameleon w_chm61 = standardBow + legendArrow; the game loads
legendBow + legendArrow for w_chm60 and w_chm61).

  cd /d D:\12tails-wardrobe && py -3 -m unittest pipeline.test_bb_item_codes -v
"""
import os
import tempfile
import unittest

from pipeline.bb_item_codes import parse

L = 'result = (GameObject)Resources.Load("GameAssets/Characters/Heroes/Chameleon/Weapons/{}", typeof(GameObject));'
# the Chameleon's legend / royal nest, junk predicates and all (ChameleonEquipment.cs:1300-1600, shortened)
SRC = """
if (!(nWeapon == "w_chm50"))
{
  if (!(nWeapon == "w_chm60"))
  {
    if (97219 - 254130 != -156911) { continue; }
    if (nWeapon == "w_chm61")
    {
      if (31401 - 585668 != -554267) { continue; }
    }
    else if (nWeapon == "w_chm62")
    {
      if (nHand == 1) { %s } else { %s }
    }
    else if (nWeapon == "w_chm82")
    {
      if (nHand == 1) { %s } else { %s }
    }
    else if (nHand == 1) { %s }
    else { %s }
  }
  if (nHand == 1) { %s } else { %s }
}
if (nHand == 1) { %s } else { %s }
""" % tuple(L.format(n) for n in ["legendBowR", "legendArrowR", "flamingArch", "flamingShot", "standardBow", "standardBow",
                                   "legendBow", "legendArrow", "royalBow", "royalArrow"])


class Parse(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".cs")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(SRC)
        self.w = parse(self.path, "chameleon")[0]["weapon"]

    def tearDown(self):
        os.remove(self.path)

    def test_own_block(self):                  # a code's loads are inside its block, the default branch is no code's
        self.assertEqual(self.w["w_chm62"], ["legendBowR", "legendArrowR"])
        self.assertEqual(self.w["w_chm82"], ["flamingArch", "flamingShot"])

    def test_negated_body_after_block(self):   # !(x == c) { ... } then c's loads, up to the parent block's end
        self.assertEqual(self.w["w_chm60"], ["legendBow", "legendArrow"])
        self.assertEqual(self.w["w_chm50"], ["royalBow", "royalArrow"])

    def test_empty_branch_falls_through(self):  # an empty branch takes the enclosing negated code's loads
        self.assertEqual(self.w["w_chm61"], ["legendBow", "legendArrow"])


if __name__ == "__main__":
    unittest.main()
