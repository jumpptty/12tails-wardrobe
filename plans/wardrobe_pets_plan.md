# Pets in the wardrobe (and Bloom Pulse): implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A สัตว์เลี้ยง topic: every game pet with its model, texture and idle loop, standing where the game puts it
behind the hero; downloadable like other pieces; plus Bloom Pulse's lv9 meshes as a back trinket.

**Architecture:** `pipeline/wardrobe_pets.py` reads TTO's decrypted client and writes the pets in the props' existing
format (three.js space) as a small index plus one file per pet; the page wears a pet through the props' `buildProp` /
`finishProp` path, parented to the hero's root at the game's rest point instead of a bone. Bloom Pulse goes into
`all/props_trinkets.json` the way `wardrobe_tot.py` merges its entries.

**Tech Stack:** Python 3 (UnityPy, Pillow; `uv run --no-project --with ...`), `node` for TTO's bundle decrypt,
three.js r160 in `wardrobe/index.html`, Playwright headless checks, `unittest`.

**Spec:** `plans/wardrobe_pets_design.md` (read it with this plan).

## Global Constraints

- Every on-screen word Thai, numbers digits; Thai in a box centred by eye on the measured ink (NOTES.md "Thai text:
  centring by eye").
- Topic name: `สัตว์เลี้ยง`. Menu labels as the other pieces': `ดาวน์โหลดลาย (PNG)`, `ดาวน์โหลดโมเดล 3D (GLB)`,
  `ถอดสัตว์เลี้ยงออก`, `เปลี่ยนสัตว์เลี้ยง`.
- Never write or commit in `12tails-video` or the Bible (`D:\12tails`); read only.
- Every script in `pipeline/`, its docstring with its exact command line; Python as `uv run --no-project --with <pkgs>
  python -I ...` or `py -3`.
- TTO data: today's client decrypted into this repo's git-ignored `tto_assets/2026-11-18/`.
- Online: BB pets published and downloadable; TTO-only pets and Bloom Pulse dropped unless in
  `wardrobe/tto_released.json`, and preview only (`ttoLocked`) when listed. ToT never.
- Browser checks headless (Playwright), one after another, on a free port; never the user's browser window.
- Commit only this work's files (other sessions' skin work sits uncommitted in the tree: `git add` paths, never `-A`).
- A look being picked (camera angle, the topic's place) = side-by-side mocks for the user first.

## Review Focus

1. A saved loadout names a pet the data no longer has (the online copy drops TTO pets): the class loads without a pet,
   no error toast, no console error. (Task 5)
2. Picking pets quickly (A then B before A's file arrives): only B ends on stage, one undo step per pick. (Task 5)
3. Changing class with a pet out: the pet comes back with the new class's offset and scale (p_all85 beside the Whale
   at 2.0x, a kite at the new class's height). (Task 5)
4. ชมชิ้นส่วน (Showcase) opened on another piece hides the pet with the character and shows it again on exit. (Task 5)
5. `?ttolock` (the online rule) on a TTO-only pet: its menu has no download items; a BB pet's has both. (Task 8)

---

### Task 1: TTO's pet rules, read from 1.7.0

**Files:**
- Create: `plans/wardrobe_pets_tto_rules.md`
- Modify: `NOTES.md` (the "pets: the design" section)

**Interfaces:**
- Produces: the exact formulas Task 4 encodes: `rest_point`, `pet_scale`, `idle_clip`, the TTO code -> prefab table,
  the TTO-only names, the upgradable BB codes.

- [ ] **Step 1: Read TTO1118's pet code** in `D:\12tails\DecompiledSource_TTO_2026-11-18` (`dump.cs` for RVAs; the
  disassembly of `GameAssembly.dll` with the Bible's tools or capstone as `wardrobe_icons.py` does): `EquipPet`
  (0x1adac10), `GetPetSize` (0x1adcff0), `IsStaticLargePet` (0x1add410) and its `StaticLargePetScale`,
  `PetControl.Init` / `LateUpdate` / `FindClip` / `SetAnimPrefixes` (dump.cs ~96568), `PetScales.Multiplier`.
- [ ] **Step 2: Write `plans/wardrobe_pets_tto_rules.md`**: for each of spawn point, rotation, level scale, the
  multiplier, the idle clip choice: TTO's rule with its RVA, BB's rule (design doc), "same" or the difference. Also:
  TTO's code -> prefab map for the pets BB lacks (EquipPet's address strings, `gameassets/characters/Pets/...`), their
  game names (TTO's locale table, as `EmotionSkill` is read for emotes) and which BB codes the pet shop upgrades to
  Lv 9 (`PetShopData.cs`, the Bible's `12Tails-Mechanics-Reference.md` "Pet level N"). Anything not settled: say so.
- [ ] **Step 3: NOTES.md**: one bullet per finding, with the RVAs.
- [ ] **Step 4: Commit** `git add plans/wardrobe_pets_tto_rules.md NOTES.md && git commit -m "wardrobe pets: TTO's pet rules read from 1.7.0"`

### Task 2: Today's TTO client, decrypted for the wardrobe

**Files:**
- Create: `pipeline/wardrobe_tto_fetch.py`, `pipeline/test_wardrobe_tto_fetch.py`

**Interfaces:**
- Produces: `tto_assets/2026-11-18/{catalog.bin, dec/<bundle>}` holding every bundle (with dependencies) of the
  addresses matching the given patterns; `bundles_for(rows: list[list[str]], pattern: str) -> set[str]`.

- [ ] **Step 1: Failing test** `test_bundles_for_takes_every_listed_bundle_of_matching_rows`: rows
  `[["gameassets/characters/pet/smallanubi", "UnityEngine.GameObject", "x", "a.bundle b.bundle"],
  ["gameassets/characters/heroes/bat/weapons/x", "UnityEngine.GameObject", "x", "c.bundle"]]`, pattern
  `characters/pets?/` -> `{"a.bundle", "b.bundle"}`; `test_bundles_for_no_match_is_empty`.
- [ ] **Step 2: Run** `py -3 -m unittest pipeline.test_wardrobe_tto_fetch` -> FAIL (no module).
- [ ] **Step 3: Implement** `bundles_for` and the CLI `py -3 pipeline/wardrobe_tto_fetch.py --out tto_assets/2026-11-18
  --grep "<regex>" [--grep ...]`: rows from `aa_catalog.py` (`DecompiledSource_TTO_2026-11-14/tools`) on the live
  `...\StreamingAssets\aa\catalog.bin`, copy that catalog, run `bundle_decrypt.js` for each bundle not yet in `dec/`.
- [ ] **Step 4: Run** the test -> PASS; then the fetch with `--grep "characters/pets?/" --grep
  "heroes/all/trinkets/aura_bloompulse" --grep "icons/items/(pet|trinket)/" --grep "animations/sixseven$" --grep
  "icons/skills/emotion/sixseven$"` -> prints the bundle count, `dec/` holds them.
- [ ] **Step 5: Commit** `git add pipeline/wardrobe_tto_fetch.py pipeline/test_wardrobe_tto_fetch.py && git commit -m "wardrobe: fetch and decrypt TTO bundles by address"`

### Task 3: The props' conversion as a shared module

**Files:**
- Create: `pipeline/wardrobe_convert.py`, `pipeline/test_wardrobe_convert.py`
- Modify: `pipeline/wardrobe_data.py:62-66` (the helpers `r5`, `mp`, `mq`), `:111-129` (`clip_dict`), `:237-265`
  (`prop_mesh`, `mirror_rows`): moved out, imported back

**Interfaces:**
- Produces: `r5(x)`, `mp(p)`, `mq(q)`, `clip_dict(tt) -> {len, rate, loop, tracks}` (tracks by node name),
  `prop_mesh(M, nmats) -> {pos, nrm, uv, idx, groups}`, `mirror_rows(rows, slot)`; bodies unchanged.

- [ ] **Step 1: Failing tests**: `test_prop_mesh_mirrors_x_and_keeps_winding_with_normals` (one triangle, normals
  +z: pos x negated, idx flipped to agree with the normals); `test_mirror_rows_negates_q_y_z_and_p_x` (row
  `[0, 1,2,3,4, 5,6,7,8, 9,10,11,12]` slot q -> y, z and their slopes negated); `test_clip_dict_reads_legacy_curves`
  (a minimal typetree dict, one rotation curve on path `Root/Head`: track `Head`, `q` mirrored, `loop` from
  `m_WrapMode == 2`).
- [ ] **Step 2: Run** `py -3 -m unittest pipeline.test_wardrobe_convert` -> FAIL.
- [ ] **Step 3: Move** the five helpers into `wardrobe_convert.py` (no UnityPy import there); `wardrobe_data.py`
  imports them.
- [ ] **Step 4: Run** the new tests -> PASS; `py -3 -m py_compile pipeline/wardrobe_data.py`; `git diff
  pipeline/wardrobe_data.py` shows the five bodies removed and one import added, nothing else. (No data rebuild:
  `--props-only` would rewrite `props_*.json` without `wardrobe_tot.py`'s merged entries.)
- [ ] **Step 5: Commit** `git add pipeline/wardrobe_convert.py pipeline/test_wardrobe_convert.py pipeline/wardrobe_data.py && git commit -m "wardrobe: the props' conversion helpers in their own module"`

### Task 4: `wardrobe_pets.py`: the pets' data

**Files:**
- Create: `pipeline/wardrobe_pets.py`, `pipeline/test_wardrobe_pets.py`
- Output: `wardrobe/data/pets/index.json`, `wardrobe/data/pets/<name>.json`, `wardrobe/data/props/tex/<tex>.png`,
  `wardrobe/data/icons/pet/<code>.webp`, `tto_config/PetScale.json`

**Interfaces:**
- Consumes: Task 1's rules; Task 2's `tto_assets/2026-11-18`; Task 3's helpers.
- Produces (pure, tested): `bb_pet_codes(cs_text: str) -> dict[str, str]` (code -> prefab, from an Equipment file's
  `a == "p_xxx"` ... `Resources.Load("GameAssets/Characters/Pet/<name>")` pairs); `rest_point(follow: dict, cls: str)
  -> [x, y, z]` (three.js space, hero at the origin facing +z); `pet_scale(code: str, level: int, cls: str, table:
  dict) -> float`; `idle_clip(clip_names: list[str], default: str | None) -> str | None`.
- Produces (data): index row `{name, file, code, level, game, icon, tto, follow: {type, dist, offset: {cls: [x,y,z]}},
  scale: {cls: s}, size: [w, h, d]}`; a pet file = a props entry `{name, tto, nodes, anim: {default, clips: {<idle>}}}`
  (one clip only), its skins on its own bones (the props' "live" skin), materials by `prop_mats`.

- [ ] **Step 1: Failing tests** with the spec's values: `bb_pet_codes` on a two-branch excerpt of
  `SheepEquipment.cs` -> `{"p_slb": "smallLeafBug", "p_stb": "smallFatBug"}`; `rest_point({"type": 3, "dist": 1.5},
  "wolf") == [0, 0, -1.5]`; FloatBehind `{"type": 0, "dist": 1, "offset": {"cat": [0.2, 0.8, 0]}}` for cat ->
  `[-0.2, 0.8, -1]`; ParentPosition kiteChula `{"type": 4, "dist": 1, "offset": {"bison": [0, 1.2, 0]}}` for bison ->
  `[0, 1.2, 0]`; `pet_scale("p_lcr", 9, "sheep", {}) == 1.8`; `pet_scale("p_all85", 1, "whale", <PetScale.json>) ==
  2.0`; `pet_scale("p_all88", 1, "cat", <PetScale.json>) == 0.5`; `idle_clip(["root", "run"], "run") == "root"`;
  `idle_clip(["chibiDog_alert", "chibiDog_hi"], "chibiDog_alert") == "chibiDog_alert"`; `idle_clip([], None) is None`.
  (Adjust any expected value Task 1 shows TTO computes differently, and say so in the commit.)
- [ ] **Step 2: Run** `py -3 -m unittest pipeline.test_wardrobe_pets` -> FAIL.
- [ ] **Step 3: Implement** the four functions, then the CLI `uv run --no-project --with UnityPy --with pillow python
  -I pipeline/wardrobe_pets.py [--assets tto_assets/2026-11-18] [--only <name,...>]`: every catalog GameObject under
  `characters/pets?/` (not `effects/`) carrying a PetControl -> its tree (TRS, MeshFilter / SkinnedMeshRenderer, bind
  poses, `_MainTex` / `_Color`), the idle clip's curves resolved to node indices (as `wardrobe_data.py:326-386` does),
  the PetControl values, codes (BB: `bb_pet_codes` over the 12 `DecompiledSource\<Class>Equipment.cs`; TTO: Task 1's
  table), level (upgradable -> 9, else the code's own), the icon by code (`gamegui/icons/items/pet/<code>`, lossless
  WebP), `Config/PetScale` copied from `resources.assets`; `tto` = no prefab of that name in BB's
  `characters/pet/`. A texture name already in `props/tex` with other bytes: stop with its name. Print the pets with
  particles, with no clip, and any it skipped with why.
- [ ] **Step 4: Run** the tests -> PASS; the CLI -> 100+ pets in `index.json`, no stop.
- [ ] **Step 5: Commit** `git add pipeline/wardrobe_pets.py pipeline/test_wardrobe_pets.py wardrobe/data/pets wardrobe/data/props/tex wardrobe/data/icons/pet && git commit -m "wardrobe pets: the data (models, textures, idle clips, the game's follow values)"`

### Task 5: The pet on stage

**Files:**
- Modify: `wardrobe/index.html` (`SLOTS` :602, `loadClass` :734-786, `setProp` :1135, the render loop :6041,
  `applyState` :1896, the คัดลอกให้ Claude line, `Showcase`)
- Create: `pipeline/wardrobe_pet_check.py`

**Interfaces:**
- Consumes: Task 4's index row and pet file.
- Produces: `C.state.Pet` (pet name | null, saved per class like `Back`), `C.props.Pet` (the built pet's root),
  `petIndex()` -> Promise of the index rows (fetched once, shared by all classes), `setPet(name)` (async, the one way
  a pet goes on or off; `null` = off), `wardrobe` check hooks as the other checks use.

- [ ] **Step 1: Failing check** `py -3 pipeline/wardrobe_pet_check.py` (headless, a free port): for 4 classes x
  {smallAnubi, miniMokBug, kiteChula, smallKumo, one TTO pet}: the pet's root world position equals
  `rest_point` x the row's values within 1e-3 and its scale the row's `scale[cls]`; its mixer advances (a node's
  quaternion changes over 0.5 s) unless it has no clip; Review Focus 1-4 as cases (a saved loadout with
  `Pet: "noSuchPet"`; two picks 50 ms apart; class switch to whale with p_all85's pet; Showcase on the outfit hides
  it); no page errors. Run -> FAIL (no Pet slot).
- [ ] **Step 2: Implement**: `setPet` builds with `buildProp` / `finishProp`, adds to `C.root` at `rest_point`
  (the row's follow, this class) with the hero's rotation and `scale[cls]`; a newer pick wins (a request counter);
  `setPet` joins `tracked()` undo, `persist`, `applyState`, loadClass's restore (a missing name = no pet, quietly),
  the copy line (`สัตว์เลี้ยง <name>`); the render loop already updates `C.props` mixers.
- [ ] **Step 3: Run** the check -> PASS, then the existing `wardrobe_menu_check.py`, `wardrobe_sets_check.py`,
  `wardrobe_moves_check.py` one after another -> unchanged results.
- [ ] **Step 4: Commit** `git add wardrobe/index.html pipeline/wardrobe_pet_check.py && git commit -m "wardrobe pets: a pet stands where the game puts it"`

### Task 6: Mocks for the user: the camera turn and the topic's place

**Files:**
- Create: `pipeline/wardrobe_pet_mocks.py` -> `checks/pet_mocks/index.html` (git-ignored)

- [ ] **Step 1: Render** with the real page (a `?petcam=<deg>,<rise>` test hook, local only): the Sheep in standard
  with smallAnubi, miniMokBug, kiteChula and a Lv 9 pet, at turns 30 / 40 / 55 deg and rises 0.1 / 0.25; and 3 panel
  layouts for the สัตว์เลี้ยง block (beside ประดับ, beside ท่าทาง, its own row), desktop and phone width; one page, side
  by side, labels in Thai.
- [ ] **Step 2: Open it for the user** (full path on its own line) and ask which angle and which layout. Wait for the
  answer; write it into the design doc's camera goal and NOTES.md.

### Task 7: The topic, the picker and the camera (the user's pick)

**Files:**
- Modify: `wardrobe/index.html` (`TOPICS` :1688, `currentIcon` :3696, `openPicker` :3829 / `pickerProps` :3257,
  `heroFitPose` :4007, `FIT_DIR` :4006)
- Modify: `pipeline/wardrobe_pet_check.py`

**Interfaces:**
- Consumes: `setPet`, `petIndex`, Task 6's picks.
- Produces: `FIT_DIR_PET` (the picked turn and rise); the topic `["Pet", "สัตว์เลี้ยง"]`.

- [ ] **Step 1: Extend the check (failing)**: the topic opens a picker with a "none" tile plus one tile per row, the
  ค้นหา box finds a pet by its game name ("Anubi") and by a nickname, nicknamed pets first; with a pet out
  `heroFitPose()` uses `FIT_DIR_PET` and its box holds the pet's bounds (all 8 corners on screen); with none, `FIT_DIR`.
- [ ] **Step 2: Implement** with the existing picker parts (`pickerProps`' tile, `nickSort`, `findText`, the icon from
  the row); the tile's name = the row's `game`; Thai label centred by eye.
- [ ] **Step 3: Run** the check -> PASS; screenshot the panel and the picker (desktop, 390x700 phone) and look at
  the Thai marks.
- [ ] **Step 4: Commit** `git add wardrobe/index.html pipeline/wardrobe_pet_check.py && git commit -m "wardrobe pets: the สัตว์เลี้ยง topic, picker and camera"`

### Task 8: Downloads

**Files:**
- Modify: `wardrobe/index.html` (`VIEW_SLOTS` :3189, `pmList` :2929, `kindOf` :1926, `recOf` / `ttoLocked`,
  `texsOf`, `makePiece` :2505, `pieceFile` :2644, `dlName` :2039, `SLOT_TH`)
- Modify: `pipeline/wardrobe_pet_check.py`

**Interfaces:**
- Consumes: the Pet slot (kind `pets`, records from `petIndex` + the pet file).
- Produces: the pet's piece menu: wear / change / remove, `ดาวน์โหลดลาย (PNG)` per texture, `ดาวน์โหลดโมเดล 3D (GLB)`;
  no view-alone, no upload, no community items.

- [ ] **Step 1: Extend the check (failing)**: on a BB pet the menu lists exactly those items and each download
  produces a file named `12tails_<class in Thai>_<pet>.png` / `.glb`; the GLB loads back in GLTFLoader with its
  bones and the embedded PNG byte-equal to the data's; with `?ttolock` a TTO pet's menu has no download item (Review
  Focus 5).
- [ ] **Step 2: Implement** through the existing paths (`makePiece` with the pet's own bones, as a skinned prop).
- [ ] **Step 3: Run** the check -> PASS; `wardrobe_menu_check.py` -> unchanged.
- [ ] **Step 4: Commit** `git add wardrobe/index.html pipeline/wardrobe_pet_check.py && git commit -m "wardrobe pets: model and texture downloads"`

### Task 9: Icons at 2x and the Bible's pet nicknames

**Files:**
- Modify: `pipeline/wardrobe_nicknames.py`, `pipeline/test_wardrobe_nicknames.py`; output `wardrobe/data/nicknames.json`,
  `wardrobe/data/icons/pet/*.webp`

- [ ] **Step 1: Failing test** `test_pet_nicknames_resolve_to_pet_tiles`: a GEAR_NICKNAMES fixture with a pet code
  (`p_sab9` or the Bible's form) and a pets index fixture -> `nicknames.json["all"]["pets"]["smallanubi"] == {nick,
  game, ...}`; the script no longer lists that code as "no tile".
- [ ] **Step 2: Run** `py -3 -m unittest pipeline.test_wardrobe_nicknames` -> FAIL; **implement**; run -> PASS.
- [ ] **Step 3: Rebuild** `py -3 pipeline/wardrobe_nicknames.py`; `py -3.10 pipeline/wardrobe_icons_upscale.py` (home
  PC), then `--check` -> no pet icon left at game size.
- [ ] **Step 4: Commit** `git add pipeline/wardrobe_nicknames.py pipeline/test_wardrobe_nicknames.py wardrobe/data/nicknames.json wardrobe/data/icons/pet && git commit -m "wardrobe pets: 2x icons, the Bible's pet nicknames"`

### Task 10: Bloom Pulse, lv9's meshes

**Files:**
- Create: `pipeline/wardrobe_tto_trinkets.py`, `pipeline/test_wardrobe_tto_trinkets.py`
- Output: `wardrobe/data/all/props_trinkets.json` (one entry merged), `wardrobe/data/props/tex/*`, `tto_config/*Placement.json` and `wardrobe/data/placements.json` (refreshed from today's client)

**Interfaces:**
- Consumes: Task 2's decrypt, Task 3's helpers.
- Produces: entry `{name: "aura_bloompulse", tto: true, mount, nodes}` = the meshes of prefab `aura_bloompulse_lv9`
  only (Moat, Ribbon, Flower1 / 3 / 4 + Inner / Heart / Pulse, Twin0, Twin1, Ring) with their parents' transforms;
  `merge(entries: list, new: list) -> list` (replace by name, keep the rest in order).

- [ ] **Step 1: Failing tests**: `merge` replaces an existing `aura_bloompulse` and keeps the other entries' order;
  `meshes_only(nodes)` keeps a mesh node and its ancestors, drops particle-only branches (`Bloom`, `Pollen`).
- [ ] **Step 2: Run** `py -3 -m unittest pipeline.test_wardrobe_tto_trinkets` -> FAIL; **implement** (CLI
  `uv run --no-project --with UnityPy --with pillow python -I pipeline/wardrobe_tto_trinkets.py`; docstring: run again
  after `wardrobe_data.py`); run -> PASS.
- [ ] **Step 3: Build**: the script, then `uv run --no-project --with UnityPy python pipeline/wardrobe_placements.py`
  (today's client; `git diff wardrobe/data/placements.json`: any other item whose placement moved goes in NOTES.md);
  the icon by its code where the client has one (else the page's no-icon tile, noted).
- [ ] **Step 4: Look**: the Sheep wearing it (a headless screenshot from 3 angles) -> 18 meshes present, flowers
  around the feet; show the user.
- [ ] **Step 5: Commit** `git add pipeline/wardrobe_tto_trinkets.py pipeline/test_wardrobe_tto_trinkets.py wardrobe/data/all/props_trinkets.json wardrobe/data/props/tex wardrobe/data/placements.json && git commit -m "wardrobe: Bloom Pulse's lv9 meshes"`

### Task 11: The publish

**Files:**
- Modify: `pipeline/wardrobe_publish.py` (`BB.compare_prop` :508 / `prop_prefab` :499, a new `publish_pets`, `stage_data`
  :1157, `ITEM_ICON_FOLDERS`), `pipeline/test_wardrobe_publish.py`

**Interfaces:**
- Produces: `publish_pets(run) -> list` (the index rows kept), `pets/index.json` and the kept `pets/<name>.json` staged.

- [ ] **Step 1: Failing tests** (the file's fixtures style): a BB pet whose mesh and idle clip equal the fixture rip's
  `characters/pet/<name>.prefab` is kept with its texture and `icons/pet/<code>.webp` re-taken from BB; a pet with
  `tto: true` not in the released list is dropped with "TTO's own item"; a released TTO pet is kept with `tto: true`;
  a BB pet whose mesh differs is dropped with the reason.
- [ ] **Step 2: Run** `py -3 -m unittest pipeline.test_wardrobe_publish` -> FAIL; **implement** (`compare_prop`'s
  mesh and clip comparison on the pet prefab; `prop_texture`; `run.icon`); run -> PASS.
- [ ] **Step 3: Dry publish** `py -3 pipeline/wardrobe_publish.py --out <scratch folder>` -> the report lists the TTO
  pets and Bloom Pulse as dropped, the BB pets kept; `wardrobe_dist_check.py` on it passes. No deploy.
- [ ] **Step 4: Commit** `git add pipeline/wardrobe_publish.py pipeline/test_wardrobe_publish.py && git commit -m "wardrobe pets: the publish keeps BB's pets"`

### Task 12: Notes, hand-off, the full test run, push

**Files:**
- Modify: `NOTES.md`, `HANDOFF.md`, `CLAUDE.md` (the test command list and the browser checks list)

- [ ] **Step 1: Run every test** in CLAUDE.md's list plus the new modules (`pipeline.test_wardrobe_tto_fetch`,
  `pipeline.test_wardrobe_convert`, `pipeline.test_wardrobe_pets`, `pipeline.test_wardrobe_tto_trinkets`), `node --test
  pipeline/test_site_worker.mjs`, `test_adopt_from_video.ps1`, then the browser checks one by one -> all pass.
- [ ] **Step 2: Docs**: NOTES.md (what was built, the commands, the user's picks); HANDOFF.md (office: pull; a pet or
  Bloom Pulse rebuild needs a decrypted TTO 1.7.0, so it runs at home or after the office decrypts one; the deploy
  waits for the user); CLAUDE.md: the new tests and `wardrobe_pet_check.py`.
- [ ] **Step 3: Commit and push** `git add NOTES.md HANDOFF.md CLAUDE.md && git commit -m "wardrobe pets: notes and hand-off" && git push`
