r"""The players' nicknames for popular items, from the Bible's class guide, for the wardrobe's pickers (2026-11-14; user:
"nickname should work in search box", "see nicknamed items from the class guide in the bible hub, not all will be in
the wardrobe, but sort them first at the top for the wardrobe"; design plans/wardrobe_nicknames_design.md).

The Bible's 12t_projects/bible/index.html keeps, one line each: GEAR_NICKNAMES {item code: nickname} (70 ดล, วุธแชมป์ ...),
GEAR_LV {code: level, negative = a rank} (the class guide's picker order) and GEAR_DATA {slot: [[code, game name]]}.
They are resolved to the wardrobe's tiles through icons.json's codes: an outfit's plain tile takes its codes minus its
edition codes, an edition tile (R / V) the edition's own code (its icon is named by it: armor/rab62 -> a_rab62). The
Bible is read only: when its nicknames change, run this again.

  py -3 pipeline\wardrobe_nicknames.py
  -> wardrobe/data/nicknames.json = {cls | "all": {kind: {item | "item|R": {"nick", "lv", "game": [names]}}}} (shaped like
     icons.json, so the page looks a tile up the way it looks up its icon); prints the tiles per class and the nicknames
     with no tile (boots, pets, the armlet rings, codes the wardrobe lacks)
"""
import json
import os
import re
import sys
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BIBLE = next((p for p in (r"D:\12tails", r"C:\Users\Jump\Desktop\12tails")
              if os.path.isfile(os.path.join(p, "12t_projects", "bible", "index.html"))), r"D:\12tails")
PAGE = os.path.join(BIBLE, "12t_projects", "bible", "index.html")
DATA = os.path.join(ROOT, "wardrobe", "data")
LETTER = {"outfits": "a", "weapons": "w", "accessories": "c", "trinkets": "t"}


def read_bible_tables(html):
    """(nicknames {code: str}, levels {code: int}, game names {code: str}) from the Bible page's three table lines."""
    def table(name):
        m = re.search(r"^const " + name + r" = (\{.*\});\s*$", html, re.M)
        if not m:
            raise ValueError(f"the Bible page has no `const {name} = {{...}};` line")
        return json.loads(m.group(1))
    data = table("GEAR_DATA")
    game = {code: name for rows in data.values() for code, name in rows}
    return table("GEAR_NICKNAMES"), table("GEAR_LV"), game


def edition_codes(kind, entry):
    """{edition letter: code} of an outfit's R / V tiles, from their icons' file names."""
    out = {}
    for ed, icon in (entry.get("editions") or {}).items():
        m = re.search(r"/([a-z]+\d+[a-z0-9_]*)\.\w+$", icon or "")
        if m:
            out[ed] = f"{LETTER[kind]}_{m.group(1)}"
    return out


def tile_row(name, codes, nick, lv, game):
    """One tile's row ({} when it has neither a nickname nor a game name): the first nicknamed code's nickname and
    level, every code's game name."""
    row, named = {}, [c for c in codes if c in nick]
    if named:
        row["nick"] = nick[named[0]]
        if named[0] in lv:
            row["lv"] = lv[named[0]]
        others = sorted({nick[c] for c in named} - {row["nick"]})
        if others:
            print(f"  {name}: two nicknames, kept {row['nick']!r} over {others}")
    names = [game[c] for c in codes if c in game]
    if names:
        row["game"] = list(dict.fromkeys(names))
    return row


def build(icons, nick, lv, game, items=None):
    """(nicknames.json, the nickname codes no tile carries, sorted). items (page_items): rows go under the page's
    spelling of the item, and an icons.json entry with no page item gives no row (its nicknames count as unmatched)."""
    out, used = {}, set()
    for cls, kinds in icons.items():
        for kind, entries in kinds.items():
            for name, e in entries.items():
                if items is not None:            # the page's own spelling (icons.json's case can differ), else no tile
                    mine = items.get(cls, {}).get(kind, set())
                    name = name if name in mine else next((n for n in sorted(mine) if n.lower() == name.lower()), None)
                    if name is None:
                        continue
                eds = edition_codes(kind, e) if kind == "outfits" else {}
                plain = [c for c in e.get("codes", []) if c not in eds.values()]
                tiles = [(name, plain)] + [(f"{name}|{ed}", [code]) for ed, code in sorted(eds.items())]
                for key, codes in tiles:
                    row = tile_row(f"{cls} {kind} {key}", codes, nick, lv, game)
                    if row:
                        out.setdefault(cls, {}).setdefault(kind, {})[key] = row
                    used.update(c for c in codes if c in nick)
    return out, sorted(set(nick) - used)


def page_items(data):
    """{cls | "all": {kind: names}}: the items the page has, as it looks them up (nickOf / iconOf): a class's outfits
    and props by name and by name without _L / _R; the shared table by lower-case name, any class's prop included."""
    data = Path(data)
    load = lambda rel: json.loads((data / rel).read_text(encoding="utf-8")) if (data / rel).is_file() else []
    out, shared = {}, {k: set() for k in LETTER}
    classes = [c["cls"] for c in json.loads((data / "meta.json").read_text(encoding="utf-8"))["classes"]]
    for cls in classes + ["all"]:
        mine = {"outfits": {o["name"] for o in load(f"{cls}/outfits.json")}} if cls != "all" else {}
        for kind in ("weapons", "accessories", "trinkets"):
            names = {p["name"] for p in load(f"{cls}/props_{kind}.json")}
            mine[kind] = names | {re.sub(r"_[LRlr]$", "", n) for n in names}
            shared[kind].update(n.lower() for n in names)
        if cls != "all":
            out[cls] = mine
    out["all"] = shared
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    with open(PAGE, encoding="utf-8") as f:
        nick, lv, game = read_bible_tables(f.read())
    with open(os.path.join(DATA, "icons.json"), encoding="utf-8") as f:
        icons = json.load(f)
    out, unmatched = build(icons, nick, lv, game, page_items(DATA))
    with open(os.path.join(DATA, "nicknames.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    print(f"{len(nick)} nicknames in the Bible ({PAGE})")
    for cls, kinds in sorted(out.items()):
        n = sum(1 for k in kinds.values() for r in k.values() if "nick" in r)
        print(f"  {cls}: {n} nicknamed tiles")
    print(f"{len(unmatched)} with no tile: {' '.join(unmatched)}")


if __name__ == "__main__":
    main()
