# Search and the Bible's nicknames in the pickers: design (2026-11-14)

## Intent

The user: "in the set selection and each piece selections, some pieces or sets are rarely of audience interest 1. add
search box by name 2. nickname should work in search box 3. see nicknamed items from the class guide in the bible hub,
not all will be in the wardrobe, but sort them first at the top for the wardrobe". Players look for the popular pieces
(the ones the community has nicknames for: 70 ดล, วุธแชมป์ ...); the long lists bury them.

## Goals

- A ค้นหา box in the ชุด (outfit) and ชุดเซ็ต (set) pickers; the hat / weapon / back pickers keep theirs.
- The search matches the tile's name, the game's own English name (the Bible's GEAR_DATA) and the nickname, ignoring
  case and spaces ("70ดล" finds "70 ดล").
- Nicknamed tiles first in every picker that lists items (outfits with their R / V tiles, weapons, hats, back items,
  sets), in the Bible's class-guide order (classGuideGearSortKey: no level, rank-gated (highest rank first), then level
  highest first; ties: the wardrobe's own order); the rest in the wardrobe's present order.
- The look (the user's pick, 2026-11-14, of four mocks: "swap"): a nicknamed tile shows the nickname in gold where the
  name was, the name small under it, the tile's border a little gold; the tooltip keeps the name.

## Non-goals

- No game names on the tiles (they are only searchable); no search in the class, colour, face or move pickers.
- Nothing hidden or removed: the rare pieces stay, below.
- No edits to the Bible (read only): its nickname table stays the one source.

## Approaches

1. **(picked) A build script copies the Bible's table into the data, resolved to the wardrobe's tiles**:
   `pipeline/wardrobe_nicknames.py` reads GEAR_NICKNAMES, GEAR_LV and GEAR_DATA from the Bible's index.html (either PC)
   and icons.json, writes `wardrobe/data/nicknames.json`; the page stays simple; the publish keeps the published items'
   rows only. Rerun when the Bible's nicknames change.
2. The page reads the Bible's code table and maps codes itself: the edition codes would have to be guessed from icon
   paths in the page, and the publish could not filter by item.
3. Nicknames typed into the wardrobe by hand: two lists to keep in step.

## Data

`nicknames.json` = `{cls: {kind: {item: {nick, lv, game}}}}`, kind = outfits / weapons / accessories / trinkets, item = the
tile's name; an outfit edition is `<name>|<R|V>`. `nick` = the Bible's nickname of the tile's codes (an outfit's plain
tile: its codes minus the edition codes; an edition tile: the edition's code, from its icon), `lv` = the Bible's GEAR_LV of
that code (absent when the Bible has none), `game` = the game names of all the tile's codes (search only). Shared items
(`all`) resolve per class like the rest. The script prints the nicknames with no tile (boots, pets, rings, codes the
wardrobe lacks).

## Sets

A set's nickname = its outfit's (in the set's edition), else the first of its pieces' (weapon, hat, back) that has one;
sets with a nickname first, in the same order; the search covers the set's name, nickname and each piece's name, game
name and nickname.

## Left to the builder

The Thai text in the gold label centred by eye (NOTES.md "Thai text: centring by eye"); a headless check script; the
publish's filter; NOTES.md / HANDOFF.md (the other PC: pull; a rebuild needs the Bible).
