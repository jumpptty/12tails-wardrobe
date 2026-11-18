# Pets in the wardrobe: design (2026-11-18)

## Intent

The user: "Add Pet section, standing behind the hero how it would work in game. Bring their models together with their
texture and animations", then "When I say pet animations, I meant pet idle animation only". A new สัตว์เลี้ยง topic: a
player picks any pet and sees it with their dressed hero, placed where the game places it, in its idle loop. The
wardrobe is about seeing a whole look; in the game the pet is part of it.

## Goals

- A สัตว์เลี้ยง topic in the left panel and its picker: one tile per pet prefab (colour variants are their own tiles, as
  the game spawns them: littleCarron / _p / _s, SmallRabby W / G / S / B), the game's icon by pet code, the game's name,
  the picker's ค้นหา box (name, game name, the Bible's nickname), nicknamed pets first (the nicknames rule,
  `plans/wardrobe_nicknames_design.md`), and a "none" choice to take the pet off.
- Every pet the game spawns: BB's (about 60, `gameassets/characters/pet/`) and TTO's own (about 25,
  `gameassets/characters/pets/`: Dino sharks, Mini / Small Rabby, Cute Cat, Tianlong, Apo, Violeta, the allNN ...).
- Each pet: its prefab's meshes and materials with their textures, and its idle clip looping. Nothing else moves.
- **Placement = the game's at rest** (`PetControl.cs` Init and LateUpdate, BB; the same fields in TTO's bundles):
  - The hero's equipment spawns the pet at hero.position - hero.forward with the hero's rotation
    (`SheepEquipment.cs:~4990`, the same in every class), then `Init` puts it at hero.position - followDistance x
    hero.forward. With the hero standing still nothing moves it again (the follow trail is filled with that point), so
    it stands **followDistance behind the hero, facing the same way**, playing `root`. This holds for RunFollow (3, most
    pets), RunBehind (2), FloatFollow (1).
  - FloatBehind (0): the same point plus the class offset (`offset_<class>`), rotation the hero's.
  - ParentPosition (4: the kites, Ninja Kites, Tianlong) / ParentAll (5): at hero.position plus the class offset turned
    by the pet's rotation (the kites' offsets are heights: Bison / Whale 1.2, Wolf 1.0, Cat / Sheep / Bat 0.8,
    Chameleon 0.7, Rabbit / Monkey 0.6, Panda / Mole / Penguin 0.5), rotation the hero's.
  - Values per prefab from its PetControl (`followType`, `followDistance`, `offset_<class>`), read from TTO's bundles
    (they keep the type trees; BB's YAML rip left the script's fields empty). Seen so far: followDistance 1 for most,
    1.4 littleMadCocon, 1.5 smallFlowerBug, 2 miniMokBug, 0 the Ninja Kites.
- **The camera (the user's pick B, 2026-11-18):** while a pet is out, the fitted view turns to the side and a little
  higher so the pet shows beside the hero; with no pet, today's front view (`FIT_DIR`). The fit box takes in the pet. The
  turn (about 40 deg as a starting point) and the height are a look: mocked side by side for the user to pick (CLAUDE.md:
  mock variants), on pets of different sizes (a small walker 1 m back, a 2 m one, a kite, a Lv 9 pet at 1.8x, which
  may reach into the hero: shown as the game has it, not moved).
- **Size = the pet at its highest level (my call, from the user's "max rank everywhere", 2026-11-09, and "the meshes
  at max level" for Bloom Pulse, 2026-11-18).** BB scales a pet by the level digit of its code right after the spawn:
  `localScale = (level x 0.1 + 0.9)` (`SheepEquipment.cs:5021`, the same in all 12 Equipment files): Lv 1 = 1.0x,
  Lv 9 = 1.8x. A pet the pet shop upgrades (Bible `12Tails-Mechanics-Reference.md`, "Pet level N") shows at Lv 9;
  one with no upgrade (balloons, kites, balls, the `p_allN` codes and the like) at its own level. Then TTO's per-pet /
  per-class multiplier (below). The tile's name carries the level the game writes ("L. Carron 9").
- **TTO's rules where they differ (my call: the live game, as the wardrobe already takes TTO's placement tables for
  BB's items):** `PetScales.Multiplier(hero, code)` from the client's Resources TextAsset `Config/PetScale`
  (`resources.assets`, read the way `wardrobe_placements.py` reads the placement tables; copy into `tto_config/`):
  today it shrinks p_all75 / 76 / 81 / 87 / 88 / 89 to 0.5, p_allhlw 1.5, and per class only p_all85 / 86 (Bison 1.5,
  Whale 2.0); no BB pet is in it. TTO1118's `PetControl` adds `idlePrefix` / `FindClip`: the builder reads TTO's
  `EquipPet` / `Init` / `FindClip` (disassembly, `DecompiledSource_TTO_2026-11-18`) to confirm the spawn point, the
  level scale and the idle clip, and follows TTO where it differs from BB's (noted in NOTES.md).
- The pet is part of the class's saved loadout (localStorage), the undo steps, the คัดลอกให้ Claude line, บันทึกภาพ;
  hidden with the character in ชมชิ้นส่วน.
- **Downloads (user 2026-11-18: "the model and texture should be downloadable like other assets, Same logic, TTO
  exclusive remains undownloadable"):** the pet's piece menu gives ดาวน์โหลดโมเดล 3D (`.glb`, the same `pieceFile` /
  GLTFExporter path: its own bones, bind pose, the texture embedded byte for byte) and ดาวน์โหลดลาย (the texture PNG;
  `ลาย 1 / ลาย 2` when it has two), named `12tails_<class in Thai>_<pet>` as other pieces. Online: BB pets yes,
  TTO-only pets preview only (no download), the rule other TTO pieces follow; the local copy downloads everything.
- Online: BB's pets go on the public copy (the content rule: BB + `wardrobe/tto_released.json`); TTO-only pets stay
  local unless listed there. The publish proves each published pet against BB's client the way it proves props.

## Non-goals

- No pet movement: no run / walk, no following, no pet skills or their effects (`pet/effects/mini*`); whatever move the
  hero plays, the pet stays at its spot in idle. No level picker (one size per pet, above).
- No particle systems a prefab may carry (a glow, petals): models, textures and the idle clip only. The builder lists
  any pet whose look depends on one, for the user.
- Not in v1 (the user can ask later): pets in gear sets, ส่งลุคนี้ / looks, community skins, uploading a skin onto a
  pet, the piece menu's view-alone (ดูชิ้นนี้อย่างเดียว) for pets.
- No Thai pet names table: tiles show the game's names (as other items, `humanize()`), Thai only through nicknames.
- Nothing written or committed in the video repo or the Bible (read only).

## Approaches

How the data is made:

1. **(my call) `pipeline/wardrobe_pets.py` in this repo reads TTO's decrypted bundles** (BB's pets are in TTO's client
   with their PetControl type trees, as BB's outfits and clips are for `wardrobe_data.py`) and writes page-ready data
   in the existing prop format, converted to three.js space. Precedent: `wardrobe_tot.py` and the effects builds read game
   bundles here. One script, one repo, one session. CLAUDE.md says extraction scripts belong to the video repo; the user
   was told and did not object (2026-11-18), the video repo has no pet extraction to extend.
2. The video repo extracts pets into `props/json`, `wardrobe_data.py` converts them: two repos and two sessions for one
   feature, and `wardrobe_data.py` rewrites everything to add one kind.
3. BB's YAML rip for BB pets: no PetControl values and no TTO pets.

The view (asked; the user picked B):

- A. Front view kept; the visitor orbits to find the pet (mostly hidden behind the hero at first).
- **B. (picked) The game's spot, the camera turned while a pet is out.**
- C. The pet moved sideways into the front view: not where the game puts it.

## Data

- Source: the newest decrypted TTO client. TTO updated today (1.7.0, home install, `%LOCALAPPDATA%\TailsTopia\...\aa\
  StandaloneWindows64`); `tto_assets/2026-11-04` predates 1.6.2.4 and may lack newer pets. My call: decrypt today's
  client's pet bundles (and their dependencies) into this repo's git-ignored `tto_assets/2026-11-18/` (as the office did
  with `tto_assets/2026-11-09`; `D:\12tails\DecompiledSource_TTO_2026-11-14\tools\bundle_decrypt.js`, the address map
  from `aa_catalog.py`), `--assets` to choose another. The same decrypt serves the 6-7 emote (`sixseven`) next.
- Which prefabs are pets: BB = every `Resources.Load("GameAssets/Characters/Pet/<name>")` in the classes' Equipment
  pet switch, with its `p_<code>` (BB's names `PetData.cs`, e.g. p_lcr "L. Carron"); TTO = the catalog's
  `characters/pets?/` GameObjects that carry a PetControl, codes from TTO's DLL the way `wardrobe_icons.py` finds item
  codes, where findable. Effects (`pet/effects/`) are not pets.
- Format: the props' (`all/props_trinkets.json`): `nodes` (the prefab tree, p / q / s), meshes as `skin` (pos, nrm, uv,
  idx, groups, w, j, bones = node indices, ibm) with `mats`, `anim.clips` with tracks per node index in the game's
  Hermite keys; plus `pet`: {code, followType, followDistance, offset: {cls: [x, y, z]}} in three.js space. A small
  index (names, codes, icons, follow values, sizes) loads with the page; one file per pet loads on pick, so the first
  picture never waits for pets. Textures as the props': PNG under `data/props/tex/` by the game's texture name (the
  publish re-takes them from BB's flat `Assets/Texture2D` by that name; a name already there with other bytes stops the
  script). **The idle clip =
  the game's at rest:** `Init` sets "has run" only when the Animation has a `run` clip, and LateUpdate then CrossFades
  `root`; without `run` nothing calls a clip and the Animation's default clip (`m_Animation`, played automatically)
  runs. So: a `run` clip -> `root`; else the default clip (all63 / 65 / 68 chibiDog_root, all64 / 66 / 67 chibiDog_alert,
  halloweenGhost_root, Tianlong's Take 001 ...); no Animation (kiteButterfly / Chula / Pukpao, soccerBall) -> the
  prefab pose, as in the game.
- Census of TTO's 2026-11-04 client (102 prefabs with a PetControl, all with legacy Animation clips; only all66 also
  carries an Animator): follow types 3 RunFollow (most), 1 FloatFollow (littleDeadPeppon, miniGoldenBug, miniSkyBug,
  smallKarazo, smallFlowerDryad, smallSelene, smallStingQueen), 2 RunBehind (littleBDMellon, smallNeonBug), 0
  FloatBehind (the four balloons, smallKumo), 4 ParentPosition (kites, Ninja Kites, Tianlong A / B, smallDragonZ), 5
  ParentAll (soccerBall). Particles ride on CuteCat_R, MotherFlowerBug, koalia (7), all66 (4), halloweenGhost,
  miniGoldenBug, smallKarazo, smallKumo (left out, Non-goals).
- Icons: `gamegui/icons/items/pet/<code>` (132 files in BB's rip) through `wardrobe_icons.py`'s path, then the 2x
  upscale (`wardrobe_icons_upscale.py`, home PC). Nicknames: `wardrobe_nicknames.py` gains the pets kind (it prints
  pets today as "no tile").

## Bloom Pulse (the user, same session)

"You might as well add t_all_tto_bloompulse to the wardrobe too if it has a model for it", then "Do the meshes at max
level for Bloom Pulse". A shared back trinket new in TTO 1.7.0 (today's client; not in `tto_assets/2026-11-04`):
`heroes/all/trinkets/aura_bloompulse` + `_lv1`..`_lv9` (the shared trinkets bundle, bb81e29a60faa85dabae8dbe20ca5179 in
today's catalog, and its dependencies). Its look is mostly particles; meshes come from lv4 on.
- One tile in the ประดับ (Back) picker, `aura_bloompulse`, = **lv9's meshes**: Moat (Lv2_MossGlow_B), Ribbon
  (Lv3_PollenDrift_D), the three flowers Flower1 / 3 / 4 with their Inner, Heart, Pulse (Lv4_BloomPulse_C, at radius
  about 0.7 around the hero), the leaves Twin0 / Twin1 (Lv5_LeafSwirl_D, at x -+0.8), Ring (Lv9_ThornAura_A); each at its
  prefab transform (the parents' 0.5-0.65 scales included).
- Static: the scripts that move them (Lv2_MossGlow_B ... Lv9_ThornAura_A, no clips) and every particle system are left
  out, as for the other two auras (their GroundRing mesh only).
- Materials are TTO's own shaders (M_BloomPulse_C_Flower1 ...; the shader sits in a dependency bundle): the page's prop
  materials draw texture x colour, additive where the shader is additive; how close that comes is for the user's eye.
- Data: the same decrypt as the pets; written into `all/props_trinkets.json` the way `wardrobe_tot.py` merges its
  entries (`"tto": true`; a re-run replaces it; run again after `wardrobe_data.py`); placement from TTO's
  `TrinketPlacement` for its code (refresh `tto_config` from today's client: `wardrobe_placements.py`), else the
  existing auras' rule; its icon by code where the client has one. TTO-only: local, no downloads online, unless the
  user lists it in `tto_released.json`.

## Risks

- (Checked 2026-11-18: every pet's clips are legacy Animation clips, the format the props' path reads.) Pets added
  after 11-04 (today's 1.7.0) may differ: any clip the path can't read leaves that pet in its prefab pose, reported.
- Units: the pet and the hero must share scale (both the game's metres in three.js space); checked on the stage
  against a game screenshot if the sizes look off.

## Left to the builder

The page code (where the pet's group lives: on the hero's root, not a bone; the contact shadow, if any, in the stage's
style); the panel row the สัตว์เลี้ยง block joins (a look: mock it with the camera angles); Thai centring by eye on any
new label (NOTES.md); a headless check script (every pet loads and sits at its spot for every class, idle loops, the
camera shows it, no page errors); unit tests for the code -> prefab parse and the publish's pet rule; NOTES.md and
HANDOFF.md (the other PC: pull; a pet rebuild runs at home or wherever a decrypted TTO client is).
