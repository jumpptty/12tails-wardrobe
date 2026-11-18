r"""Tests for wardrobe_pets.py's pure rules: BB's code -> prefab and code -> name parses, the rest point, the size
(GetPetSize x PetScales.Multiplier), the idle clip (FindClip), the level and the loop (plans/wardrobe_pets_tto_rules.md
sections 1-4, 7; TTO1118 = the 2026-11-18 client, patch 1.7.0).

  cd /d D:\12tails-wardrobe && py -3 -m unittest pipeline.test_wardrobe_pets -v

Only pure functions are imported (no UnityPy, no Pillow): the bundle reading sits in wardrobe_pets.main().
"""
import unittest

from pipeline.wardrobe_pets import (bb_pet_codes, bb_pet_names, game_name, idle_clip, idle_loops, pet_level,
                                    pet_scale, rest_point, rest_size)

# SheepEquipment.cs:4770-4793 (BB's EquipPet, the family switch), as the decompile writes it
SHEEP_EXCERPT = """
									else if (a == "p_slb")
									{
										if (174517 - 543052 != -368535)
										{
											continue;
										}
										gameObject = (GameObject)Resources.Load("GameAssets/Characters/Pet/smallLeafBug", typeof(GameObject));
										if (86175 - 307981 == -221805)
										{
											continue;
										}
									}
									else if (a == "p_stb")
									{
										if (19474 - 45637 != -26163)
										{
											continue;
										}
										gameObject = (GameObject)Resources.Load("GameAssets/Characters/Pet/smallFatBug", typeof(GameObject));
										if (228551 - 79862 != 148689)
										{
											continue;
										}
									}
"""

# PetData.cs:57-63 (a whole code) and :290-296 (a family code, the level appended)
PETDATA_EXCERPT = """
													if (nCommand == "p_all1")
													{
														if (149232 - 250030 == -100797)
														{
															continue;
														}
														itemClass.name = "Bigbug Balloon";
															if (a == "p_lcr")
															{
																if (85356 - 53614 != 31742)
																{
																	continue;
																}
																itemClass.name = "L. Carron " + lastDigit;
"""

# Config/PetScale as today's resources.assets holds it (2026-11-18 21:23 install; rules section 3), cut to the rows used
PET_SCALE = {
    "heroes": [{"hero": h, "scale": 1.0, "entries": []} for h in ("Bat", "Cat", "Sheep", "Wolf")]
    + [{"hero": "Bison", "scale": 1.0, "entries": [{"code": "p_all85", "scale": 1.5}, {"code": "p_all86", "scale": 1.5}]},
       {"hero": "Whale", "scale": 1.0, "entries": [{"code": "p_all85", "scale": 2.0}, {"code": "p_all86", "scale": 2.0}]}],
    "pets": [{"code": c, "scale": 0.5} for c in ("p_all88", "p_all87", "p_all89", "p_all81", "p_all76", "p_all75")]
    + [{"code": "p_allhlw", "scale": 1.5}],
}


class BBCodes(unittest.TestCase):
    def test_bb_pet_codes_pairs_each_code_with_its_load(self):
        self.assertEqual(bb_pet_codes(SHEEP_EXCERPT), {"p_slb": "smallLeafBug", "p_stb": "smallFatBug"})

    def test_bb_pet_names_reads_the_name_and_whether_the_level_is_appended(self):
        self.assertEqual(bb_pet_names(PETDATA_EXCERPT), {"p_all1": ("Bigbug Balloon", False),
                                                         "p_lcr": ("L. Carron ", True)})


class RestPoint(unittest.TestCase):
    def test_run_follow_rests_follow_distance_behind(self):
        self.assertEqual(rest_point({"type": 3, "dist": 1.5}, "wolf"), [0, 0, -1.5])

    def test_float_behind_adds_the_class_offset_mirrored(self):
        self.assertEqual(rest_point({"type": 0, "dist": 1, "offset": {"cat": [0.2, 0.8, 0]}}, "cat"), [-0.2, 0.8, -1])

    def test_parent_position_is_the_offset_only(self):
        self.assertEqual(rest_point({"type": 4, "dist": 1, "offset": {"bison": [0, 1.2, 0]}}, "bison"), [0, 1.2, 0])


class Scale(unittest.TestCase):
    def test_level_scale_without_a_table(self):
        self.assertAlmostEqual(pet_scale("p_lcr", 9, "sheep", {}), 1.8)

    def test_per_class_entry_is_returned_alone(self):
        self.assertAlmostEqual(pet_scale("p_all85", 1, "whale", PET_SCALE), 2.0)
        self.assertAlmostEqual(pet_scale("p_all85", 1, "bison", PET_SCALE), 1.5)
        self.assertAlmostEqual(pet_scale("p_all85", 1, "cat", PET_SCALE), 1.0)

    def test_per_pet_scale_times_hero_scale(self):
        self.assertAlmostEqual(pet_scale("p_all88", 1, "cat", PET_SCALE), 0.5)

    def test_cute_cats_are_a_flat_four(self):
        self.assertAlmostEqual(pet_scale("p_all31", 1, "cat", PET_SCALE), 4.0)
        self.assertAlmostEqual(pet_scale("p_all35", 9, "whale", PET_SCALE), 4.0)

    def test_valkornoct_grows_by_a_hundredth(self):
        self.assertAlmostEqual(pet_scale("p_svk", 9, "wolf", PET_SCALE), 0.19)

    def test_p_all_codes_have_no_level(self):
        self.assertAlmostEqual(pet_scale("p_all1", 9, "cat", PET_SCALE), 1.0)


class IdleClip(unittest.TestCase):
    def test_root_found_by_its_prefix(self):
        self.assertEqual(idle_clip(["root", "run"], "run", "root", 3, True), "root")

    def test_chibi_dog_prefix(self):
        self.assertEqual(idle_clip(["chibiDog_alert", "chibiDog_hi"], "chibiDog_alert", "chibiDog_alert", 3, True),
                         "chibiDog_alert")

    def test_no_clips(self):
        self.assertIsNone(idle_clip([], None, "root", 3, True))

    def test_koalia_idles_on_battle_not_its_default(self):
        self.assertEqual(idle_clip(["run", "battle", "root"], "root", "battle", 3, True), "battle")

    def test_parent_position_plays_the_default_only_when_automatic(self):
        self.assertEqual(idle_clip(["root"], "root", "root", 4, True), "root")
        self.assertIsNone(idle_clip(["root"], "root", "root", 4, False))

    def test_prefix_without_an_underscore_match_takes_the_first_starting_with_it(self):
        self.assertEqual(idle_clip(["rootX", "root_Cute"], None, "root", 3, False), "root_Cute")
        self.assertEqual(idle_clip(["walk", "Root2"], None, "root", 1, False), "Root2")


class Loop(unittest.TestCase):
    def test_playidle_restarts_a_once_clip(self):
        self.assertTrue(idle_loops(True, 0, 0))
        self.assertTrue(idle_loops(True, 1, 0))

    def test_clamp_forever_holds_even_under_playidle(self):
        self.assertFalse(idle_loops(True, 8, 0))

    def test_default_clip_loops_only_by_wrap_mode(self):
        self.assertTrue(idle_loops(False, 2, 0))
        self.assertFalse(idle_loops(False, 0, 0))
        self.assertTrue(idle_loops(False, 0, 2))          # the clip's Default takes the Animation's wrap mode


class RestSize(unittest.TestCase):
    def test_bounds_at_the_idle_clips_first_frame_and_only_what_shows(self):
        I = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        entry = {"nodes": [
            {"name": "root", "parent": -1, "p": [0, 0, 0], "q": [0, 0, 0, 1], "s": [1, 1, 1], "on": True},
            {"name": "bone", "parent": 0, "p": [0, 0, 0], "q": [0, 0, 0, 1], "s": [1, 1, 1], "on": True},
            {"name": "body", "parent": 0, "p": [0, 0, 0], "q": [0, 0, 0, 1], "s": [1, 1, 1], "on": True,
             "skin": {"pos": [0, 0, 0, 1, 0, 0], "w": [1, 0, 0, 0] * 2, "j": [0, 0, 0, 0] * 2, "bones": [1], "ibm": I}},
            {"name": "hidden", "parent": 0, "p": [5, 5, 5], "q": [0, 0, 0, 1], "s": [1, 1, 1], "on": False,
             "mesh": {"pos": [0, 0, 0, 1, 1, 1]}}],
            # the idle's first key turns the bone 90 deg about z: the vertex (1, 0, 0) stands at (0, 1, 0)
            "anim": {"default": "idle", "clips": {"idle": {"tracks": {"1": {"q": [[0, 0, 0, 0.7071068, 0.7071068] + [0] * 8]}}}}}}
        self.assertEqual(rest_size(entry), [0, 1, 0])
        del entry["anim"]
        self.assertEqual(rest_size(entry), [1, 0, 0])                 # no clip: the prefab pose


class LevelAndName(unittest.TestCase):
    def test_levels(self):
        self.assertEqual(pet_level("p_lcr"), (9, False))
        self.assertEqual(pet_level("p_srp"), (1, False))
        self.assertEqual(pet_level("p_all85"), (1, False))
        self.assertEqual(pet_level("p_mrd"), (9, True))

    def test_game_names(self):
        names = {"p_all1": ("Bigbug Balloon", False), "p_lcr": ("L. Carron ", True)}
        self.assertEqual(game_name("p_lcr", 9, names), "L. Carron 9")
        self.assertEqual(game_name("p_all1", 1, names), "Bigbug Balloon")
        self.assertEqual(game_name("p_svk", 9, names), "S.ValkorNoct 9")     # spaced like BB's "L. Carron 9"
        self.assertIsNone(game_name("p_all85", 1, names))


if __name__ == "__main__":
    unittest.main()
