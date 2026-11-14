# Search and the Bible's nicknames in the pickers: implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** a ค้นหา box in the ชุด and ชุดเซ็ต pickers, every picker's search matching the tile name, the game's name and
the players' nickname, nicknamed tiles first with the nickname shown in the Bible's way.

**Architecture:** `pipeline/wardrobe_nicknames.py` copies the Bible's GEAR_NICKNAMES / GEAR_LV / GEAR_DATA into
`wardrobe/data/nicknames.json`, resolved to the wardrobe's tiles through icons.json (same shape as icons.json); the
publish keeps the published tiles' rows; `wardrobe/index.html` loads it beside icons.json and uses it to order, label
and search the pickers.

**Tech Stack:** Python 3 (stdlib, unittest), the page's plain JS (three.js page, no build step), Playwright for the check.

**Spec:** `plans/wardrobe_nicknames_design.md`

## Global Constraints

- Every on-screen word Thai, numbers digits; Thai text centred by eye on the measured ink (NOTES.md "Thai text: centring
  by eye"), the marks above (่ ้ ๊ ๋ ิ ี ึ ื ั ็ ์) and below (ุ ู) never clipped.
- The Bible (`D:\12tails` / `C:\Users\Jump\Desktop\12tails`) and the video folder are read only.
- The look = the user's pick "swap": the nickname in gold where the name was, the name small under it, the tile's border a
  little gold, the tooltip keeps the name (mock: `pipeline/wardrobe_nick_mocks.py`, `checks/nick_mocks/swap_*.png`).
- Order of nicknamed tiles = the Bible's classGuideGearSortKey on `lv`: no level first, then rank-gated (lv < 0, lower lv
  = higher rank first), then level highest first; ties keep the wardrobe's order; un-nicknamed tiles after, as today.
- Search: lower-case, every whitespace removed, on both the query and the text.
- No commits until the user asks; `wardrobe/index.html` carries the skin sessions' uncommitted SKINS.cut / SKINS.face
  hunk, so a commit takes this work's hunks only (NOTES.md "one weapon topic", `git merge-file`).
- The video repo reads `wardrobe/data`: add files only, rename nothing.

## Review Focus

1. A search that finds nothing: the outfit / set picker shows `ไม่พบที่ค้นหา` (not an empty panel); the weapon / hat /
   back picker keeps its ไม่ใส่ tile plus the same note. (Task 3, Task 4 checks.)
2. A redraw of the open picker (same topic re-opened: a skin upload, an edition switch) keeps the typed query and its
   filtered list. (Task 3 check.)
3. Online: a TTO piece that is not released must not appear in the published nicknames.json (its key is the model's
   name). (Task 2 test.)
4. A nickname whose Thai marks sit above the line (วุธแชมป์, หมวกดันน้ำ) in the gold label: not clipped by the label's
   `overflow: hidden`, on desktop and on a 390 px phone; long ones end in an ellipsis. (Task 3 screenshots.)
5. ← / → in the piece viewer and the worn tile scrolled into view (F8) follow the new order. (Task 5 check.)

---

### Task 1: The nickname data

**Files:**
- Create: `pipeline/wardrobe_nicknames.py`, `pipeline/test_wardrobe_nicknames.py`
- Create (built): `wardrobe/data/nicknames.json`
- Modify: `CLAUDE.md` (the Tests line and the Data list name the new script and test)

**Interfaces:**
- Produces: `read_bible_tables(html: str) -> tuple[dict, dict, dict]` (nicknames {code: str}, lv {code: int},
  game {code: str} flattened from GEAR_DATA's six lists); `build(icons: dict, nick: dict, lv: dict, game: dict) ->
  tuple[dict, list[str]]` (the nicknames.json object, the nickname codes no tile carries, sorted);
  `nicknames.json` = `{cls_or_all: {kind: {item: {"nick": str, "lv": int (omitted when none), "game": [str]}}}}`, kind =
  outfits / weapons / accessories / trinkets, an outfit edition tile keyed `<name>|<R|V>`. An item with game names but no
  nickname is kept with `game` only (search).
- Command line (docstring): `py -3 pipeline\wardrobe_nicknames.py` (finds the Bible like bb_item_codes.py's `BIBLE`,
  writes the file, prints the counts per class and the unmatched codes).

- [ ] **Step 1: Write the failing tests** (`unittest`, small hand-made icons / tables):
  - `test_reads_the_three_tables`: an html string with `const GEAR_DATA = {...};`, `const GEAR_LV = {...};`,
    `const GEAR_NICKNAMES = {...};` on their own lines (and other code around) -> the three dicts; a missing table
    raises `ValueError` naming it.
  - `test_plain_outfit_takes_its_non_edition_code`: outfit legend codes a_rab60, a_rab61, a_rab62, editions
    {"R": "icons/armor/rab62.webp"}, nick {a_rab61: "70 ดล", a_rab62: "70 ดด"}, lv {a_rab61: 72, a_rab62: 74} ->
    `out["rabbit"]["outfits"]["legend"]["nick"] == "70 ดล"`, `["legend|R"]["nick"] == "70 ดด"`, lv 72 / 74.
  - `test_one_tile_two_codes`: weapon legendGun codes w_rab60, w_rab61, nick only w_rab61 -> "70 ดล"; game names of
    both codes in `game`.
  - `test_shared_table_resolves_too`: `icons["all"]["accessories"]["poseidonhelmet"]` codes c_all66 -> nicknamed.
  - `test_unmatched_codes_listed`: b_all32 and p_lbd in nick, no tile -> in the second return value.
  - `test_conflicting_nicknames_take_the_first_code_s`: a tile whose two codes carry different nicknames -> the first
    code's (icons.json order), and the script prints the conflict.
- [ ] **Step 2:** `py -3 -m unittest pipeline.test_wardrobe_nicknames` -> fails (no module).
- [ ] **Step 3: Implement** the module: tables read with one regex per name (`^const NAME = (\{.*\});\s*$`, multiline)
  and `json.loads`; an edition's code = the slot letter (outfits a, weapons w, accessories c, trinkets t) + `_` + the
  edition icon's file stem.
- [ ] **Step 4:** the tests pass; run `py -3 pipeline\wardrobe_nicknames.py`; expect 41-61 tiles per class and the 55
  unmatched codes listed in NOTES.md's session section.
- [ ] **Step 5:** add the test module to CLAUDE.md's Tests line and the script to its Data list.

### Task 2: The publish carries the published tiles' nicknames

**Files:**
- Modify: `pipeline/wardrobe_publish.py` (`ROOT_JSON`; new `publish_nicknames(run, icons)`, called after
  `publish_icons`), `pipeline/test_wardrobe_publish.py`

**Interfaces:**
- Consumes: Task 1's file shape; `publish_icons`' return value (the published icons.json object).
- Produces: `<data>/nicknames.json` online = the source's rows whose `cls / kind / item` (an edition key by its name
  before `|`) is in the published icons.json; `{}` when the source has no file.

- [ ] **Step 1: Write the failing test** `test_nicknames_follow_published_items` (World: one published BB weapon with a
  nickname, one TTO weapon not released with a nickname, an outfit edition key) -> the BB weapon and the edition kept,
  the TTO one gone, `wp.check(w.out) == []`; and `test_nicknames_json_written_when_the_data_has_none`.
- [ ] **Step 2:** `py -3 -m unittest pipeline.test_wardrobe_publish` -> the two fail.
- [ ] **Step 3: Implement** `publish_nicknames` and add `"nicknames.json"` to ROOT_JSON.
- [ ] **Step 4:** the full test list in CLAUDE.md passes.

### Task 3: The page: load, label, order, search (outfit and piece pickers)

**Files:**
- Modify: `wardrobe/index.html` (the data load at ~5977, beside `iconOf` ~1657, `item()` ~3757, CSS ~323, `openPicker`'s
  outfit branch ~3818 and prop branch ~3864)

**Interfaces:**
- Produces (page globals, used by Task 4 and the check): `let NICK = {}` (nicknames.json, `getJSON(...).catch(() =>
  ({}))`); `nickOf(kind, name, ed = "") -> {nick, lv, game} | undefined` (looked up the way `iconOf` is: class table by
  name / name without `_L` / `_R`, then `NICK.all[kind][name.toLowerCase()]`; an edition by `name|ed`);
  `nickSort(list, keyFn)` (stable: nicknamed first in the Bible order, the rest unchanged); `findText(...parts) ->
  string` and `matches(q, text) -> bool` (the normalisation in Global Constraints); `item()`'s option `o.nick` (a
  string) draws the swap label: `.lbl.nk-main` = the nickname, `.nk-sub` = the old label, `.pk-item.is-nick`.
- The outfit picker gets the same search box as the prop pickers (`aria-label="ค้นหาชุด"`); its search covers the
  outfit name, each edition tile's name with its letter, nickOf's nick and game names.
- The prop pickers' `find` adds the nick and game names (a weapon's other piece's too).
- A redraw of the same topic keeps the query (read the old input's value before `tools.innerHTML = ""`).
- Empty result: `<p class="pk-note">ไม่พบที่ค้นหา</p>` after any ไม่ใส่ tile.

- [ ] **Step 1:** implement the globals, the label (CSS from the mock's `swap` look: gold 600 13 px main line, a 10.5 px
  muted sub line, ellipsis on both; padding / line-height so Thai upper marks are not clipped) and the two branches.
- [ ] **Step 2: Verify by eye** with an isolated Playwright context (the mock script's pattern), Rabbit and Wolf, weapon
  and outfit pickers, 1366x768 and 390x844: the first tiles are 70 ดล, 70 ดด, ... in order; วุธแชมป์'s ์ whole; search
  `70ดล`, `fenrir` (Wolf: royalSword), `แชมป์`, `zzz` (the note); the query survives a redraw.

### Task 4: The page: sets

**Files:**
- Modify: `wardrobe/index.html` (`buildSets`' end ~1800, the set branch of `openPicker` ~3806, `setNameHTML` users)

**Interfaces:**
- Consumes: Task 3's `nickOf`, `nickSort`, `findText`, `matches`, `item()`'s swap label.
- Produces: `setNick(s) -> {nick, lv} | undefined` = the outfit's nickOf in the set's edition (`setEd(s)`), else the
  first of R (or L), Head, Back that has one; the set list ordered by `nickSort(sets, setNick)` once in `buildSets`
  (so the panel's teaser shows nicknamed sets' outfits too); the set picker's search box (`aria-label="ค้นหาชุดเซ็ต"`)
  beside the count note, matching the set's name, setNick, and each piece's name, nick and game names; the set tile's
  label in the swap look when setNick exists; ถอดทั้งหมด always first, never filtered out.

- [ ] **Step 1:** implement.
- [ ] **Step 2: Verify:** `uv run --no-project --with playwright==1.65.1 python -I pipeline/wardrobe_sets_check.py ...`
  (its docstring's command) exits 0; by eye: the Rabbit's sets open with legend (70 ดล), legend R (70 ดด), royal ...;
  search `60ดด` finds royal R.

### Task 5: The headless check and the notes

**Files:**
- Create: `pipeline/wardrobe_nick_check.py` (Playwright, the menu check's server pattern; exit 1 on a failure)
- Modify: `CLAUDE.md` (browser checks list), `NOTES.md` (the session section), `HANDOFF.md` (the other PC: pull;
  a rebuild of nicknames.json needs the Bible and runs on either PC)
- Delete: `pipeline/wardrobe_nick_mocks.py` stays (it is the mock the user picked from; NOTES names it)

- [ ] **Step 1: Write the check**, for every class: the outfit, weapon, hat, back and set pickers' first tiles = the
  nicknamed ones in nicknames.json's order worked out apart from the page (the same key in Python); every nicknamed
  tile's `.nk-main` text = its nick and `.nk-sub` its name; search `70ดล` leaves only tiles whose nick is "70 ดล" (plus
  ไม่ใส่); a nonsense query shows `ไม่พบที่ค้นหา`; the query survives `openPicker(t)` again; ← / → in the viewer step in
  the picker's order; no page / console errors.
- [ ] **Step 2:** run it: exit 0. Run `wardrobe_menu_check.py`, `wardrobe_weapon_slot_check.py`, `wardrobe_moves_check.py`
  (docstring commands): exit 0. Run the unit tests and node tests from CLAUDE.md.
- [ ] **Step 3:** NOTES.md / HANDOFF.md / CLAUDE.md updated; report to the user; commit only when asked.
