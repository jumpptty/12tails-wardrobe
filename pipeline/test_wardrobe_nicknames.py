r"""Tests for wardrobe_nicknames: the Bible's class-guide nicknames (GEAR_NICKNAMES), levels (GEAR_LV) and game names
(GEAR_DATA) resolved to the wardrobe's tiles through icons.json (2026-11-14; user: "nickname should work in search box",
"see nicknamed items from the class guide in the bible hub ... sort them first at the top for the wardrobe").

  cd /d D:\12tails-wardrobe && py -3 -m unittest pipeline.test_wardrobe_nicknames -v
"""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from pipeline.wardrobe_nicknames import build, page_items, read_bible_tables


def page(**tables):
    """A Bible page: each table on its own line, as index.html has them, with other code around."""
    lines = ["<script>", "const GEAR_INDEX = (() => { return {}; })();"]
    lines += [f"const {name} = {json.dumps(t, ensure_ascii=False)};" for name, t in tables.items()]
    lines += ["function classGuideGearSortKey(id){ return [0]; }", "</script>"]
    return "\n".join(lines)


def icons(cls="rabbit", **slots):
    """icons.json for one class (and an empty shared table unless given)."""
    out = {cls: {k: {} for k in ("outfits", "weapons", "accessories", "trinkets")},
           "all": {k: {} for k in ("outfits", "weapons", "accessories", "trinkets")}}
    for key, entries in slots.items():
        c, kind = key.split("__") if "__" in key else (cls, key)
        out[c][kind].update(entries)
    return out


class ReadTablesTest(unittest.TestCase):
    def test_reads_the_three_tables(self):
        html = page(GEAR_DATA={"weapon": [["w_rab61", "Legend Gun V"]], "armor": [["a_rab61", "Legend Armor V"]],
                               "hat": [], "trinket": [], "boot": [["b_all32", "Spike Boots"]], "pet": []},
                    GEAR_LV={"w_rab61": 74, "w_rab58": -68},
                    GEAR_NICKNAMES={"w_rab61": "70 ดล"})
        nick, lv, game = read_bible_tables(html)
        self.assertEqual(nick, {"w_rab61": "70 ดล"})
        self.assertEqual(lv, {"w_rab61": 74, "w_rab58": -68})
        self.assertEqual(game, {"w_rab61": "Legend Gun V", "a_rab61": "Legend Armor V", "b_all32": "Spike Boots"})

    def test_a_missing_table_names_itself(self):
        html = page(GEAR_DATA={"weapon": []}, GEAR_LV={})
        with self.assertRaisesRegex(ValueError, "GEAR_NICKNAMES"):
            read_bible_tables(html)


class BuildTest(unittest.TestCase):
    def test_plain_outfit_takes_its_non_edition_code(self):
        ic = icons(outfits={"legend": {"icon": "icons/armor/rab60.webp", "codes": ["a_rab60", "a_rab61", "a_rab62"],
                                       "editions": {"R": "icons/armor/rab62.webp"}}})
        out, _ = build(ic, {"a_rab61": "70 ดล", "a_rab62": "70 ดด"}, {"a_rab61": 72, "a_rab62": 74}, {})
        self.assertEqual(out["rabbit"]["outfits"]["legend"]["nick"], "70 ดล")
        self.assertEqual(out["rabbit"]["outfits"]["legend"]["lv"], 72)
        self.assertEqual(out["rabbit"]["outfits"]["legend|R"]["nick"], "70 ดด")
        self.assertEqual(out["rabbit"]["outfits"]["legend|R"]["lv"], 74)

    def test_one_tile_two_codes(self):
        ic = icons(weapons={"legendGun": {"icon": "icons/weapon/rab60.webp", "codes": ["w_rab60", "w_rab61"]}})
        out, _ = build(ic, {"w_rab61": "70 ดล"}, {"w_rab60": 72, "w_rab61": 74},
                       {"w_rab60": "Legend Gun", "w_rab61": "Legend Gun V"})
        e = out["rabbit"]["weapons"]["legendGun"]
        self.assertEqual(e["nick"], "70 ดล")
        self.assertEqual(e["lv"], 74)                        # the nicknamed code's level
        self.assertEqual(e["game"], ["Legend Gun", "Legend Gun V"])

    def test_a_tile_with_no_level_has_no_lv(self):
        ic = icons(accessories={"poseidonHelmet": {"icon": None, "codes": ["c_all66"]}})
        out, _ = build(ic, {"c_all66": "หมวกดันน้ำ"}, {}, {})
        self.assertNotIn("lv", out["rabbit"]["accessories"]["poseidonHelmet"])

    def test_game_name_alone_is_kept_for_the_search(self):
        ic = icons(weapons={"royalSword": {"icon": "icons/weapon/wlf50.webp", "codes": ["w_wlf50"]}})
        out, _ = build(ic, {}, {}, {"w_wlf50": "Fenrir Sword"})
        self.assertEqual(out["rabbit"]["weapons"]["royalSword"], {"game": ["Fenrir Sword"]})

    def test_a_tile_with_nothing_is_left_out(self):
        ic = icons(weapons={"stick": {"icon": None, "codes": ["w_rab3"]}})
        out, _ = build(ic, {}, {}, {})
        self.assertNotIn("stick", out.get("rabbit", {}).get("weapons", {}))

    def test_shared_table_resolves_too(self):
        ic = icons(all__accessories={"poseidonhelmet": {"icon": "icons/accessory/all66.webp", "codes": ["c_all66"]}})
        out, _ = build(ic, {"c_all66": "หมวกดันน้ำ"}, {"c_all66": 61}, {})
        self.assertEqual(out["all"]["accessories"]["poseidonhelmet"]["nick"], "หมวกดันน้ำ")

    def test_unmatched_codes_listed(self):
        ic = icons(weapons={"legendGun": {"icon": None, "codes": ["w_rab61"]}})
        _, unmatched = build(ic, {"w_rab61": "70 ดล", "p_lbd": "ALL 9", "b_all32": "เท้าหนาม"}, {}, {})
        self.assertEqual(unmatched, ["b_all32", "p_lbd"])

    def test_rows_take_the_page_s_spelling(self):
        """icons.json can spell a name in another case than the page's item (the Bison's PoseidonHelmet = the page's
        poseidonHelmet, 2026-11-14 review): the row goes under the page's spelling, or the page never finds it."""
        ic = icons(cls="bison", accessories={"PoseidonHelmet": {"icon": None, "codes": ["c_all66"]}})
        out, unmatched = build(ic, {"c_all66": "หมวกดันน้ำ"}, {}, {}, items={"bison": {"accessories": {"poseidonHelmet"}}})
        self.assertEqual(list(out["bison"]["accessories"]), ["poseidonHelmet"])
        self.assertEqual(unmatched, [])

    def test_an_edition_row_takes_its_outfit_s_page_spelling(self):
        ic = icons(cls="panda", outfits={"shinjitsu": {"icon": None, "codes": ["a_pnd40", "a_pnd42"],
                                                       "editions": {"V": "icons/armor/pnd42.webp"}}})
        out, _ = build(ic, {"a_pnd42": "48 ดด"}, {}, {}, items={"panda": {"outfits": {"shinJitsu"}}})
        self.assertEqual(list(out["panda"]["outfits"]), ["shinJitsu|V"])

    def test_a_row_with_no_page_item_is_unmatched(self):
        ic = icons(weapons={"ghostGun": {"icon": None, "codes": ["w_rab9"]}})
        out, unmatched = build(ic, {"w_rab9": "ปืนผี"}, {}, {"w_rab9": "Ghost Gun"}, items={"rabbit": {"weapons": {"legendGun"}}})
        self.assertNotIn("ghostGun", out.get("rabbit", {}).get("weapons", {}))
        self.assertEqual(unmatched, ["w_rab9"])

    def test_page_items_read_from_the_data(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "meta.json").write_text(json.dumps({"classes": [{"cls": "bison"}]}), encoding="utf-8")
            (d / "bison").mkdir()
            (d / "bison" / "outfits.json").write_text(json.dumps([{"name": "shinJitsu"}]), encoding="utf-8")
            (d / "bison" / "props_accessories.json").write_text(json.dumps([{"name": "poseidonHelmet"}]), encoding="utf-8")
            (d / "bison" / "props_weapons.json").write_text(json.dumps([{"name": "shinGauntlet_L"}]), encoding="utf-8")
            (d / "all").mkdir()
            (d / "all" / "props_trinkets.json").write_text(json.dumps([{"name": "FlowerBand"}]), encoding="utf-8")
            got = page_items(d)
        self.assertEqual(got["bison"]["outfits"], {"shinJitsu"})
        self.assertEqual(got["bison"]["accessories"], {"poseidonHelmet"})
        self.assertEqual(got["bison"]["weapons"], {"shinGauntlet_L", "shinGauntlet"})     # the page also looks up without _L / _R
        self.assertIn("flowerband", got["all"]["trinkets"])                              # the shared table: lower case
        self.assertIn("poseidonhelmet", got["all"]["accessories"])                       # a class prop can use it too

    def test_conflicting_nicknames_take_the_first_code_s(self):
        ic = icons(weapons={"twin": {"icon": None, "codes": ["w_rab70", "w_rab71"]}})
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            out, _ = build(ic, {"w_rab70": "หนึ่ง", "w_rab71": "สอง"}, {}, {})
        self.assertEqual(out["rabbit"]["weapons"]["twin"]["nick"], "หนึ่ง")
        self.assertIn("twin", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
