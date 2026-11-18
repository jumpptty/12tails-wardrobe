r"""Tests for wardrobe_placements.py's named override (final review I2, 2026-11-19): an entry listed in OVERRIDES as
KEEP stays as the wardrobe had it (the previous placements.json), whatever the client's table says now; every other
entry is the table's.

  cd /d D:\12tails-wardrobe && py -3 -m unittest pipeline.test_wardrobe_placements -v

Only pure functions are imported (no UnityPy): reading the installed client sits in wardrobe_placements.main().
"""
import json
import unittest
from pathlib import Path

from pipeline.wardrobe_placements import KEEP, OVERRIDES, apply_overrides, conv

ROOT = Path(__file__).resolve().parent.parent


def P(bone, x=0.0):
    return {"bone": bone, "p": [x, 0.5, 0.0], "q": [0, 0, 0, 1], "s": 1.0, "kwr": False, "kps": False}


def table(**cat):
    return {"trinkets": {"cat": {"fallback": P("Spine1"), "entries": dict(cat)}}}


class Overrides(unittest.TestCase):
    def test_the_cats_reaper_trinket_is_kept(self):
        # the live BB item and the video repo's Cat skits keep the old place until the user picks (HANDOFF)
        self.assertEqual(OVERRIDES.get(("trinkets", "cat", "t_allhlw5")), KEEP)

    def test_a_kept_entry_is_the_previous_one(self):
        new = table(t_allhlw5=P("Spine1", -0.36), t_new=P("Root"))
        prev = table(t_allhlw5=P("Spine2", -0.19))
        notes = apply_overrides(new, prev, {("trinkets", "cat", "t_allhlw5"): KEEP})
        self.assertEqual(new["trinkets"]["cat"]["entries"]["t_allhlw5"], P("Spine2", -0.19))
        self.assertEqual(new["trinkets"]["cat"]["entries"]["t_new"], P("Root"))       # the rest: the table's
        self.assertEqual(len(notes), 1)

    def test_the_kept_entry_keeps_its_place_in_the_order(self):
        new = table(a=P("A"), t_allhlw5=P("Spine1"), b=P("B"))
        apply_overrides(new, table(t_allhlw5=P("Spine2")), {("trinkets", "cat", "t_allhlw5"): KEEP})
        self.assertEqual(list(new["trinkets"]["cat"]["entries"]), ["a", "t_allhlw5", "b"])

    def test_the_kept_entry_is_written_byte_for_byte(self):
        old = {"bone": "Spine2", "p": [-0.19271332025527954, 0.5011118054389954, -0.03435853123664856],
               "q": [0.33236, 0.375986, -0.801887, 0.324267], "s": 0.7912837266921997, "kwr": False, "kps": False}
        new = table(t_allhlw5=P("Spine1"))
        apply_overrides(new, json.loads(json.dumps(table(t_allhlw5=old))), {("trinkets", "cat", "t_allhlw5"): KEEP})
        dump = lambda e: json.dumps(e, separators=(",", ":"))
        self.assertEqual(dump(new["trinkets"]["cat"]["entries"]["t_allhlw5"]), dump(old))

    def test_no_previous_entry_takes_the_tables(self):
        new = table(t_allhlw5=P("Spine1"))
        notes = apply_overrides(new, {}, {("trinkets", "cat", "t_allhlw5"): KEEP})
        self.assertEqual(new["trinkets"]["cat"]["entries"]["t_allhlw5"], P("Spine1"))
        self.assertTrue(notes and "no previous" in notes[0])

    def test_an_entry_gone_from_the_table_comes_back_when_kept(self):
        new = table()
        apply_overrides(new, table(t_allhlw5=P("Spine2")), {("trinkets", "cat", "t_allhlw5"): KEEP})
        self.assertEqual(new["trinkets"]["cat"]["entries"]["t_allhlw5"], P("Spine2"))

    def test_the_input_previous_is_not_shared(self):
        prev = table(t_allhlw5=P("Spine2"))
        new = table(t_allhlw5=P("Spine1"))
        apply_overrides(new, prev, {("trinkets", "cat", "t_allhlw5"): KEEP})
        new["trinkets"]["cat"]["entries"]["t_allhlw5"]["p"][0] = 9
        self.assertEqual(prev["trinkets"]["cat"]["entries"]["t_allhlw5"]["p"][0], 0.0)

    def test_an_unknown_override_value_stops(self):
        with self.assertRaises(ValueError):
            apply_overrides(table(t_allhlw5=P("Spine1")), table(t_allhlw5=P("Spine2")), {("trinkets", "cat", "t_allhlw5"): "move"})


class Data(unittest.TestCase):
    def test_the_data_holds_the_kept_entry(self):
        # wardrobe/data/placements.json as committed: the Cat's ReaperTrinket where the wardrobe had it before 1.7.0
        pl = json.loads((ROOT / "wardrobe" / "data" / "placements.json").read_text(encoding="utf-8"))
        e = pl["trinkets"]["cat"]["entries"]["t_allhlw5"]
        self.assertEqual(e["bone"], "Spine2")
        self.assertEqual(e["p"], [-0.19271332025527954, 0.5011118054389954, -0.03435853123664856])


class Conv(unittest.TestCase):
    def test_unity_to_three(self):
        e = conv({"bone": "Spine2", "pos": {"x": 0.25, "y": 0.5, "z": -0.1}, "euler": {"x": 0, "y": 0, "z": 0}, "scale": 0.8})
        self.assertEqual(e, {"bone": "Spine2", "p": [-0.25, 0.5, -0.1], "q": [0.0, 0.0, 0.0, 1.0], "s": 0.8, "kwr": False, "kps": False})


if __name__ == "__main__":
    unittest.main()
