# 12 Tails Wardrobe: notes

Read this first and append to it during the session, not at the end: findings, conventions, lessons, the session
log.

Split from `jumpptty/12tails-video` on 2026-11-09 (the user: "make a separate repo for the wardrobe, independent of
the video works, so there's a clear line between them"). The sections below moved from that repo's NOTES.md, their
text unchanged except paths. Older mixed history (the TTO extraction of faces / outfits / animations / props, lessons
shared with the skits, the office PC setup) stays in `D:\12tails-video\NOTES.md`: read it when needed, never edit it
from here. The split's design and plan: `plans\wardrobe_split_design.md`, `plans\wardrobe_split_plan.md`.

## Layout

- `wardrobe\index.html` (the page, three.js r160), its icons and `wardrobe\ui\`; `wardrobe\data\` (~370 MB, tracked
  in git since 2026-11-10, byte for byte; untracked before) built by `pipeline\wardrobe_*.py`, prop textures in
  `wardrobe\data\props\tex\` (`wardrobe_props_tex.py`). A rebuild ends with committing and pushing the changed data.
- Read only, from the sibling `12tails-video` folder: `outfits\`, `tex\faces_tto\`, `props\json\`, `props\tex\`,
  `tto_assets\`, `tot_assets\`; from the Bible repo (`D:\12tails`, office `C:\Users\Jump\Desktop\12tails`): the BB
  rip and the decompiles.
- `wardrobe_dist\` (untracked) = the published copy (`pipeline\wardrobe_publish.py`); nothing outside reads it since the
  trailer was retired (2026-11-10). The video repo's skits read `wardrobe\data` (placements, the office's prop / face
  fallbacks): renaming that breaks them.
- `tto_config\` (untracked): `wardrobe_placements.py`'s copies of TTO's placement tables.
- `wardrobe\fx_cues\<cls>.json` (tracked): each class's skill effect / sound cues (`plans\fx_recipe.md`); the built
  effects are in `wardrobe\data\<cls>\fx.json`, `sfx\`, `data\fx\tex\`.

## Wardrobe app (2026-11-04)

`wardrobe.cmd` (this repo's root) serves the folder on http://127.0.0.1:8771 (`pipeline/wardrobe_serve.py`, Python's
http.server that closes itself about 10-15 s after the last wardrobe page closes, 2026-11-10) and opens
`wardrobe/index.html`: three.js r160 (jsdelivr importmap), one class at a time in its game idle (`root`), every outfit
(BB + TTO) in every colour, any face (composed on the texture in a canvas with skins.py's face-block rule), right /
left hand weapons, headpiece, back trinket (BB's mounts and rotations above), emotes with Thai labels (TTO's clap /
wai / cooking / mining / planting / fishing / pose37 tagged), base moves and skill moves; the game's 0.2 s crossfade,
one-shot moves return to idle. Loadout per class in localStorage; "บันทึกภาพ" saves a PNG, "คัดลอกให้ Claude"
copies the loadout line. CSS `saturate(1.15)` on the canvas = the V07 saturation.
- Data: `pipeline/wardrobe_data.py` -> `wardrobe/data/` (224 MB): everything converted to three.js space (= the
  mirrored space: x -> -x, quaternion (x, -y, -z, w), bind poses S B S, winding by the normals); outfits as binary
  (`o_<armor>.bin`: positions, normals, uv, weights, joints, indices) + `outfits.json`; textures and faces as WebP;
  clips as the game's Hermite keys (mirrored; infinite slope = +-1e30 = a step), sampled at 30 fps in the page.
- Skinning: three.js world = bone.world x boneInverse x bindMatrix x v; Unity = bone.world x bindpose x v, so
  boneInverse = mirrored bindpose x inverse(mesh world at bind); each outfit mesh gets its own Skeleton over the shared
  bones (Monkey / Panda bind poses differ from the rest pose, so the rest pose can't be used for the inverses).
- The view re-fits with a ResizeObserver on the stage (a window resize alone left a stale aspect: stretched view).
- **Item icons** (user: "really hard to use without the in-game icons"): `pipeline/wardrobe_icons.py`. Icons are
  `gamegui/icons/items/<weapon|armor|accessory|acessory|trinket>/<code>` (1597, one bundle `27165fa0…`), named by
  item code (`a_shp24` -> `armor/shp24`); TTO has no item table in its bundles, so code -> model comes from each
  `<Class>Equipment`'s compiled string switches (`WeaponAsset` / `BowAsset` / `ArrowAsset` / `LanceAsset` /
  `ShieldAsset`, `ArmorMeshAsset`, `AccessoryAsset`, `TrinketAsset`; TTO1102 DLL), read with capstone + the
  decompile's `usages.py`: the switch is a hash tree, so each code compare is followed to its "equal" branch and the
  first name literal there is the model (checked on BB's code: `w_shp1` -> `noviceBook`, `a_all1` -> `Sheep_scout`).
  One code can give two pieces (bow + arrow, lance + shield); Panda's gloves are props `<name>_L` / `_R` (the game adds
  the hand), so the page strips the suffix to find the icon. Coverage: nearly every outfit, weapon and headpiece;
  missing = items with no code in the TTO1102 DLL (nude, divineGoddess) and fx-only trinkets. `item_map.json` keeps
  every class's code -> [models]. The page shows icon tiles (name under, pink dot = TTO, codes in the tooltip).
- **Textures repeat** (user: "100% sure the Day-Night wing texture is right in game"): Unity's default wrap is
  Repeat, three.js's is clamp. Day-Night wing's UVs run v -1..0, so clamped it showed one edge row stretched.
  `propMaterials` sets `RepeatWrapping` on every prop texture.
- **UI (user 2026-11-04)**: the left panel is one block per topic (อาชีพ, ชุด, หน้า, อาวุธหลัก, อาวุธที่ 2, หมวก,
  ของประดับหลัง, ท่าทาง), each only the name on top + the current choice's icon in a big ring; the blocks share the
  panel's full height (flex 1, min 112 px, then the panel scrolls) and the ring fills its block (CSS container units:
  `min(100cqw, 100cqh - title)`; 100 px at a 1266 px tall window; phone: 4 blocks per row); a click opens the picker,
  a full-height side panel twice the left panel's width (`--side` x 2) beside it, the 3D view still visible and
  draggable; picking does not close it (user: "swap easily"; ✕ / Esc / clicking the row again closes it). Tiles fill
  their grid cell: 3 per row (items ~113 px), faces 2 per row (~184 px, user: "big faces"). Outfit colours sit in the picker's top
  bar, props get a search box, moves have three tabs. Icons: class portraits `gamegui/icons/heroes/<cls>1`, emotes
  from `gamegui/icons/skills/emotion/` (talk -> chat, cooking -> cook, sleep -> zzz, pose* -> pose ...), skill moves
  from the class's skill icons; `pipeline/wardrobe_ui_assets.py` extracts them (2144) to `data/icons/heroes/` and
  `data/icons/skills/` and writes `data/ui.json`. Faces (user: "use the face overlay itself, not the texture UV"): the
  overlay webp `data/<cls>/faces/<n>.webp` on a skin-tone disc, cropped with CSS `object-view-box` to `faceBox`, the
  square around where 96 % of that class's face pixels fall (2nd-98th percentile; the outer edge of all faces together
  is set by a few tears / blushes and left the eyes tiny: Sheep 224 px wide against 90 px for the features).
  `wardrobe_ui_assets.py --faces-only` recomputes faceBox alone.
- **Moves (2026-11-09; user: "emote infinite loop should extend to ท่าพื้นฐาน", "ล้ม should stay on the floor", "ท่าสกิล
  ... connect them instead of separating them", "ท่าสกิล also should loop indefinitely until further input"):** every move
  plays until the next pick. `play()` runs a list of steps (`C.seq`, moved on by `seqTick` in the render loop; the mixer's
  finished event is no longer used): วิ่ง / ร่วง / ยืนพัก / ตั้งท่าสู้ / เดิน, clips with the data's loop flag and the
  singles the BB code sets to `WrapMode.Loop` (`LOOPS`: Over Swing, Roll Around, Upheaval ...) loop seamlessly; ล้ม plays
  once and lies there; ลุกขึ้น plays once, then idle; anything else plays once and starts again with the game's 0.2 s
  crossfade (a clone of the clip is the second action, so it blends from its own last frame instead of snapping).
  - ท่าสกิล: `SEQ` = per class, the skills whose clips the BB code plays as one sequence, one tile each (the skill's icon
    by its name, else its first clip's), listed first. The pattern in the code: the skill's coroutine plays a start clip
    (`Once`), then the part it holds as `WrapMode.Loop` (charge held, cast bar, channel), then the release, often in its own
    RPC (cast-time skills: `RPC_cast1` plays cast1 then cast2 looped, `RPC_<skill>_cast` plays cast3). Held parts show for
    about 1.5 s (`HOLD_SECS`) unless the step has a time (Timings below). Examples: Sheep Charge Attack cAttack1 → (0.8 s) cAttack0 loop → cAttack2 on release
    (`Sheep.cs:18827`, `:18676`, `:19287`); Holy Light holyLight1 → holyLight2 loop through the cast bar (`magAdjust(6)`) →
    holyLight3 at cast end + 0.6 s → holyLight4 loop while the beam hits (`:28265`, `:27584`, `:28028`, `:27652`); Lullaby
    the same start, then lullaby looped (`:35643`); Heart Ripper / Finishing Blow start their second RPC themselves
    (`Cat.cs:5051`, `:5393`); Counter → counter2 when hit (`Wolf.cs:28220`); Bounce → bounce0 (`Rabbit.cs:21114`); Bat
    Nightmare / Mind Control end in a channel loop; the Chameleon's volley loops cAttack3 and ends on cAttack4
    (`Chameleon.cs:17200`); Raijin Ken = cAttack1 → cAttack2 loop → raijinKen1 → raijinKen2.
  - **Look-alike names that are not sequences stay single tiles:** Book Bash 1-3 is a random pick (`Random.Range(0, 3)`,
    `Sheep.cs:37523`), Monkey damageCast1/2 replace cast1/2 when its damage-cast passive
    is learned (the release is cast3 either way; damageCast3 is never played by BB), Whale Wave divingWave / malStorm,
    Medical Shot gilShot / medicalShot and the Mole's superDig / dig1 by a learned skill.
  - Normal-attack combos (nAttack1 → 2 → ...) are one tile, each stage cut where the next press can come when its clip
    runs long (Sheep nAttack1 at 0.8 s of its 5 s clip, Wolf nAttack1 0.8 s, nAttack2 0.96 s). TTO-only sequences (Crescent
    Eclipse, Venom Phantom, Barrel Railgun, Tempest Dance) are by name (Focus Fire, once listed here, is BB data that no BB
    or TTO code plays: hidden since 2026-11-13, NEVER_PLAYED, plans/fx_chameleon/decisions.md 16); a sequence shows only when all its clips
    are in the copy, so the online copy (no TTO clips) loses nothing. The Cat's and Wolf's `walk` moved to ท่าพื้นฐาน (เดิน).
  - **Timings (2026-11-09; user: "look at their timings referring to skill-details tool", "Blade song 1-4 merge them
    all", "castbar is lessened by INT, don't touch them, assume high INT, no cast bar"):** a step's `@t` comes from the
    Bible's skill details at max rank, checked against the coroutine waits. Every cast bar the stats shorten is 0 (the
    cast bars of `RPC_cast1` / `RPC_cast` (cast2, mix2, damageCast2), Nightmare, Guardian of the Night, Holy Light,
    Lullaby, Cosmic Friday, Slayer, All Slayer, the Mole's Assemble): its loop shows for one frame, as the game's at zero
    cast time (cast2 starts after cast1's 0.7 s, `Penguin.cs:20907`, `:19466`). Barrel Railgun's fixed 6 s stays.
    Channels = their duration (Nightmare's channel 9 s, `Bat.cs:28612`; Thunder Dragon 3, Fuujin Ken 20 × 0.4 = 8, Bowling
    Whale 6, Tempest Dance 5, Grand Casino Arcade 5 rolls × 2.7 = 13.5), or three hits (at least 3 s) when the game runs
    them until the player moves (Holy Light's beam, Lullaby, Cosmic Friday 6 s, Support Fire, Flame Turret, Grand Tide,
    the Panda's and Penguin's charge ticks). Charges = full charge (Sheep 0.8 + 4 s at rank 4, Chameleon 9 s then 18 shots
    × 0.2, Wolf 5.8 s for the third wave, Cat 4 stacks, Bison 8 s then 8 hits × 0.202 on cAttack6); Qi Strike 4 s, Counter's stance
    0.8 s, Mirror Blade's 1.2 s, Trample's two phases 0.9 / 2.6 s (`Bison.cs:22696`, `:22515`), the Bison's combo stages
    at the range preview's 0 / 0.7 / 1.4 / 2.2 s. Skills the skill details give no timing for keep their clip lengths.
  - **Max rank everywhere (2026-11-09; user: "for all animations, assume max rank, eg. Blade Song currently runs thru all
    ranks and is very weird. Blade Fang why stuck at Rank 2 with wrong timing"):** Blade Song was songs 1 → 2 → 3 → 4
    (the user's earlier "merge them all"); the game plays `bladeSong<rank>` (switch at `Wolf.cs:30332`), so now
    bladeSong3 cut at 0.9 + 0.2 × 11 = 3.1 s, then bladeSong4 (0.2 s fade). Blade Fang was bladeFang1-3 at full clip
    length = rank 2's three slashes; rank 3 slashes four times, 1 → 2 → 3 → 2, the clip changing right after each hit:
    0 / 0.2 / 0.5 / 0.8 s (hits 0.2 / 0.4 / 0.7 / 1.0, end 1.2; `:26402`, `:26640`, `:26063`, the `bladeFang_count >= sLv`
    checks `:26055`, `:26627`, waits `:26652-26694`). Bison Charge Attack was cAttack3 × 4 hits = rank 1 without Improved
    Swing; now rank 2's full 8 s charge (cAttack1 1 s + cAttack2 7 s) and Improved Swing 3's cAttack6 (`Bison.cs:20318`)
    for 8 × 0.202 = 1.6 s. Quick Fire had no times: rank 4 = quickFire1 0.4 s, quickFire2 0.9 s (opening shot + 8 shots
    0.1 s apart), quickFire3 (`Chameleon.cs:19660`, `:20061`, `:19787`); with Added Fire #402 (Lv 55 passive; user: "want
    it") the loop is 4 × 4 = 16 shots, so quickFire2 runs 1.7 s. Lower-rank clips (`LOWER_RANK`: bladeSong1-2, the Bison's cAttack3-5) are left out of the move
    list. How found: every skill coroutine whose flow branches on `sLv` (`clip_flow.js` with `sLv` as the extra pattern:
    46 do), kept only where rank picks the clip or the length of a held / looped part; Trample (2.6 s), Grand Casino
    Arcade (5 rolls), the Chameleon's Charge Attack (9 s, 18 swings), Qi Strike (4 s) were already at max rank; the
    Rabbit's, Monkey's and Whale's charges have no charge-time clamp. Checked: `wardrobe_moves_check.py` traces (Blade
    Song 3 → 4 at 3.1, Blade Fang 0.2 / 0.5 / 0.9, Bison 1.0 / 8.0, Quick Fire 0.5 / 1.4 at swiftshader's ~0.1 s lag),
    the lower-rank clips not listed, no page errors.
  - Tools: `pipeline/clip_calls.js` (every class's skill clips per coroutine, with fades and wrap modes),
    `pipeline/clip_flow.js` (one coroutine's flow: the order and the waits), `pipeline/wardrobe_moves_check.py` (headless:
    all tiles, every class's parsed sequences with their step times in `chains.json`, timed traces of the Sheep's
    sequences, Blade Song and Counter, ko holding, run looping, getUp back to idle; checked 2026-11-09, no page errors;
    the swiftshader traces slow down on the heavier models, so read their times on the Sheep).

## ToT student outfits in the LOCAL wardrobe (2026-11-07)

User: "add ToT exclusive outfits models to the 3D LOCAL wardrobe only first". ToT's armor list equals TTO's minus
Halloween and the two goddess outfits, so the only ToT-only outfit is the **student set**, one per class
(`heroes/<cls>/student/`): body `<Cls>_Student` (colours `_Student_1..5`, 1024 px), hat `_Student_accessories`, weapon
`_Student_weapons` (Chameleon `_bow` + `_arrow`, Whale `_lance` + `_shield`; ToT's TTOLegacyArmor / Accessory / Weapon
ResourceMap name exactly these). How ToT's bundles were opened (TTOENC01, AES-CBC, key = TTOBundleCipher.ClientKey):
`D:\12tails-assets-archive\tot-skins-2026-11-07\_tools\README.md`; the student bundles, decrypted, are in
`tot_assets/2026-11-07/dec/` (216 with dependencies) + `student_resources.json` (catalog rows).
- `pipeline/wardrobe_tot.py` (py -3.10, UnityPy) adds per class: outfit `student` (`o_student.bin`, `tex/student<c>.webp`,
  `"face": "quarter"`), headpiece `studentHat`, weapon(s) `studentWeapon` / `studentBow` ...; prop textures
  `wardrobe/data/props/tex/tot_*.png` (the video folder's `props/tex` until the 2026-11-09 split). Every entry has `"tot": true`; a re-run replaces them. **Run it again after `wardrobe_data.py`**,
  which rewrites outfits.json / props_*.json. `wardrobe_publish.py` drops them (no BB prefab), so they stay local.
- **Face**: ToT's `TryBlendLegacySkinOverlay` (ToT GameAssembly 0x181389a30) puts the 256 overlay on a 512 sheet's
  top-left quarter and stretches it over the top-left quarter (w/2 x h/2) of any other size; the page's usual block
  (256 wide) would be half-width on the 1024 student sheets. Checked: Cat / Wolf / Sheep faces sit exactly as on
  `standard`.
- **Hats are skinned to the hero's skeleton** (all but Bat and Mole, whose hats are rigid and use the Head mount):
  prop field `heroSkin` {pos, nrm, uv, idx, groups, w, j, bones (names), ibm}; the page's `buildHeroSkin()` binds it in
  the tri space like an outfit mesh. Monkey's mic is skinned to its own bones: baked into its prefab pose.
- Page: blue dot (`--tot`) on ToT tiles, `badge()`. Checked headless (Playwright + the ms-playwright chromium-1234,
  swiftshader): all 12 classes dressed, hats and weapons on, no page errors.
- Until 2026-11-09 another session worked on the page in the `comic-skit-wardrobe-online` / `-wasd` worktrees (served
  on 8773 / 8775 over main's data; merged and removed). A parallel session may do the same again: check
  `git worktree list` and use a free port for checks.

## Online copy (2026-11-07 / 08)

The wardrobe is public at https://12tails-wardrobe.jumpthai.workers.dev (Cloudflare Worker with static assets, the user's
account; linked from the 12 Tails Bible's ห้องแต่งตัว tile). Plan and full decision log: `plans\wardrobe_online_plan.md`
and `.superpowers\sdd\2026-11-07-wardrobe-online\progress.md` (untracked), both moved here from the Bible repo on
2026-11-09 (the wardrobe's home is this repo; only the hub mirror art, `art\` with its `HOW.md`, stays in the Bible's
copy of that folder).
- **Content rule, updated 2026-11-09: BB plus released TTO** (session log "TTO online"): the TTO items in
  `wardrobe\tto_released.json` go online too, preview only. The rule below held until then.
- **Content rule (user):** "BB 3D models only". From TTO only face paints: all of them for Bison, Chameleon, Mole,
  Monkey, Penguin, Whale (released), the first half by number for the other six (`TTO_FACES_ALL_RELEASED`). ToT's local
  student outfits never go online. `pipeline/wardrobe_publish.py` enforces it: it keeps only items whose meshes / clips /
  props equal BB's client (the files were extracted through TTO's bundles), re-takes every picture from the BB rip, proves
  the upscaled Recolor Drug icons (`wardrobe/ui/recolor1-5.webp`) against BB's `field/rsc1-5.png`, drops everything else
  into `wardrobe_dist_report.json` (`dropped`, with reasons), writes the data under a content-hashed `data-<hash>/` folder
  with a year-long cache (`_headers`) and checks Cloudflare's limits (20,000 files, 25 MiB each) and case-sensitive paths.
- **Update:** `py -3 pipeline/wardrobe_publish.py --out wardrobe_dist` (about 5 min; `--src` / `--data` when the page
  and data live apart), read the printed count changes and the report, scan `wardrobe_dist` for anything non-BB, then the
  USER uploads from an EMPTY folder (never from the 12tails-video folder: its git-ignored `wrangler.jsonc` makes wrangler upload
  `review/` instead, which once published the private review notes for a few minutes):
  `npx wrangler deploy --assets D:\12tails-wardrobe\wardrobe_dist --name 12tails-wardrobe --compatibility-date 2026-11-07`.
  **Since community skins (2026-11-11) the deploy names the Worker script too**, or the send route is lost:
  `npx wrangler deploy D:/12tails-wardrobe/pipeline/site_worker.mjs --assets D:/12tails-wardrobe/wardrobe_dist --name
  12tails-wardrobe --compatibility-date 2026-11-07` (office: the C:/work/12tails-wardrobe paths). The Worker runs only
  where no file matches (POST /api/submit); its secrets DISCORD_WEBHOOK / TURNSTILE_SECRET live in Cloudflare.
  Office PC (2026-11-09): the same with `--assets C:\work\12tails-wardrobe\wardrobe_dist` (first time there: `npx wrangler
  login`). Claude cannot run the upload (the auto-mode classifier blocks publishing). Only changed files are sent; the page is
  served no-cache, so visitors get a new page at once and keep the data cache when the data folder name is unchanged.
- **Round 2 features (2026-11-08):** the Bible's Ledger palette, a pure white stage, a phone layout (bottom-sheet picker,
  no keyboard pop, no page scroll at headed-Chrome sizes 390x700 / 360x620), the left panel rows (class + face box,
  colour picked in place with the Recolor Drug icons, a full-width gilded gear-set row, hat + outfit, weapons, back +
  moves), R / V through the set tab (switches the whole worn set), per-item skin download / upload with Ctrl+V onto the
  tile or the model piece under the pointer (kept in the browser only, undoable), and WASD (W / S pan up / down, A / D
  strafe).
- **Live preview of a branch without a junction:** a tiny server that serves main's data and takes `wardrobe/*` from a
  worktree (the session's `devserve.py`); never put a junction to `wardrobe/data` inside a worktree or a scratch folder:
  `git worktree remove` / `git clean` / a recursive delete empties the target.
- **Round 3 (premium pass, 2026-11-08):** from the critical UI review (`.superpowers\sdd\2026-11-07-wardrobe-online\
  task-14a-review.md`, fixes in `task-14b-report.md`).
  - Look: the Bible's BB tokens and Ledger material (6 px corners, hairline edges, the harlequin weave), fonts from the
    Bible's Google Fonts sheet (no self-hosted TTFs; numbers in JetBrains Mono), one toolbar with the gold บันทึกภาพ, the
    Bible mark in the panel lockup (the publish makes it a new-tab link), Ledger toasts, the gold tab icon.
  - Desktop picker = 42 % of the stage (440 px min) and a camera view offset keeps the hero visible beside it.
  - Names: classes in Thai, items through `humanize()` (no Thai item names yet: the user may supply a NAME_TH table).
  - First visit to a class (no saved loadout) starts in its standard outfit (task 17b, R70; it wore the first set before);
    a nameplate on the stage (class, set, pieces) with the loading / error line and toasts.
  - Camera limits (distance, never under the floor, look-at near the hero); screenshots bake in saturate(1.15) at 2x
    and are named `12tails_<class in Thai>_<set or outfit>.png`.
  - `wardrobe/ui/recolor1-5.webp` are cropped to the potions (BB box 4,7-56,59, 104 px); the publish proves that box
    (`UI_CROP`) and moves them to a hashed `ui-<hash>/` folder with a year-long cache rule beside the data's.
  - Phone: four tiles a row, a grabber with swipe-down to close, 44 px class / face targets, the Bible mark on the stage.
  - Task 17b (the final review's fixes, 2026-11-08: `task-17a-review.md`, `task-17b-report.md` in the sdd folder):
    - First visit = the standard outfit, colour 1, the default face, nothing else; no prop list delays the first picture
      (the Cat's hood goes on when its list arrives; a saved loadout's lists load with the rig).
    - Camera: fit to the posed bounds of what is worn (headgear may rise .65 of the outfit's height, weapons and wings
      .4 to the side), pulled back until the box clears the toolbar (64 px) and the foot (12 px); after a pick it glides
      to the new fit unless the visitor has moved the camera.
    - ชมชิ้นส่วน is one name everywhere; the open viewer is the mode: the toolbar button opens it on the open picker's
      worn piece (or the outfit) and closes it, a tile click while it is open shows that piece (never wears it), the
      shown tile is marked and the picker header says so.
    - Card: buttons in fixed places (worn = ใส่อยู่, disabled; ‹ i / n › on the first line; two textures = one
      ดาวน์โหลดลาย that turns into ลาย 1 / ลาย 2 in place), a slot / set / colour line, centred under the piece;
      phones add "ปัดซ้ายหรือขวาเพื่อดูชิ้นอื่น".
    - Fit: the piece's outline over a whole turn fills 94 % of the band between the toolbar and the card; it turns
      about the centre of its footprint's smallest circle; WASD stays near it.
    - Motion: the character fades into the white stage (colour to white, nothing see-through), then the piece fades and
      scales in; a step fades the old piece out first; leaving fades the piece, eases the camera back, fades the
      character in.
    - The viewer's screenshot is cut to the piece plus 6 % (still transparent), `12tails_<class>_<slot>_<item>.png`.
    - Phone pickers with tile tools go three abreast; คืนลายเดิม is the "ลายของคุณ ✕" badge (three tools on every tile).
    - Downloads: `12tails_<class>_<item>` + `_สี<n>` (an outfit's colour) / `_ลาย<n>` (one of two textures) /
      `_ลายของคุณ`, then `.png` or `.glb`.
    - GLB props keep the turn they have when worn on their root (a hat opens upright in Blender); outfits unchanged.
    - The turntable: the finger left down when a pinch ends no longer counts as a drag.
- **3D model download (task 15, 2026-11-08; user: "allow the download of 3D models of each component too"):** a cube tool
  on every tile with the skin buttons (outfit, hat, both weapons, back) saves that piece, worn or not, as binary glTF
  `12tails_<class in Thai>_<item>.glb` (three's GLTFExporter, a dynamic import through the importmap's jsDelivr
  three@0.160.0 on the first click only; nothing is equipped, no undo step; Thai toasts). A file holds the mesh(es) with
  normals and UVs in the bind pose, page units, Y up; skinned pieces their bones (outfits and ToT's hero-skinned hats: the
  class's whole rig under "Armature", posed by the inverse bind matrices, so Monkey / Panda come out in their bind pose,
  not their rest pose; props with their own skin: the prop's bones), props their node tree at the origin (no mount
  offset) with the turn they have when worn (task 17b); the texture ดาวน์โหลดลาย saves (colour / edition worn or the visitor's skin; an outfit with the face drawn
  on, as the page shows it) embedded byte for byte (a small exporter plugin hands GLTFExporter that PNG instead of a
  canvas re-encode), V flipped; a plain standard material (metalness 0, roughness 1 = the page's lit Lambert look),
  alphaTest 0.5 -> MASK, the page's sides. **Not mirrored:** three.js space and glTF are both right-handed Y up, so the
  file is the page's model; checked by rendering each file with GLTFLoader from the page's camera (mean pixel difference
  <= 0.003 / 255 on outfits, 13-17 for a mirrored copy; the Chinese lantern's printed character reads the right way
  round) and by Blender's importer landing every vertex on (x, -z, y), the mapping build_rabbit.py uses. Sizes: outfits
  0.6-0.75 MB, props 20-120 KB.
- **Panel header (2026-11-08; user: "use the brand icon and the tool name in a single row"):** the Bible's own logo (its
  `.brand` CSS and SVG copied from the Bible's index.html, gradient id renamed `wdBrandGold`), a hairline, then ห้องแต่งตัว,
  one row; on a phone the logo alone is the 44 px chip level with the toolbar. The local copy has the logo as an `<a>`
  with no href; the publish adds the Bible's href, `target="_blank"` and `rel="noopener"` to its opening tag.
- **ชมชิ้นส่วน (task 16, 2026-11-08; user: "view and appreciate each piece of the model separately from the character
  too, like a floating item"):** an inspect mode on the same stage. `makePiece(slot, item, {pose})` builds a detached
  copy of one piece from the data with the texture it wears now (pose "idle" for the viewer: an outfit on a fresh copy of
  the class's skeleton in the idle clip's first frame, a prop turned the way it sits on the hero (`placementOf`, shared
  with setProp) with its own clip looping; pose "bind" for the 3D file, which is now written from it by `pieceFile`; the
  files came out identical to task 15's). The character fades out; the piece floats in the free part of the stage (the
  desktop picker's view offset, and above its card), fit as task 17b describes (Round 3 above); turntable 20 deg/s, bob
  3 % of its size every 3 s, a contact shadow that shrinks and fades as it rises. Only a left-button / one-finger drag
  orbits and pauses the turntable (it resumes 3 s after the drag); zoom / orbit limits scale with the piece, no pan,
  WASD within reach of the piece. The card (the nameplate's place; a phone's bottom area): name, ‹ i / n ›, slot, sets,
  colour or ลายของคุณ, ใส่ชิ้นนี้ / ใส่อยู่ (one undo step), ดาวน์โหลดโมเดล 3D (the .glb), ดาวน์โหลดลาย, ✕ กลับ.
  - **Superseded 2026-11-09 by the piece menu** (session log "the piece menu"): the tile tools, the toolbar button and the
    card's two download buttons are gone; the way in is the menu's ดูชิ้นนี้อย่างเดียว or a double-click on a piece.
    Until then: ways in: the cube on every tile (`title` ชมชิ้นส่วน; tiles keep ดาวน์โหลดลาย / อัปโหลดลาย / the cube); the toolbar
    button ชมชิ้นส่วน (`aria-pressed` = the viewer open; while open a tile click shows its piece instead of wearing
    it); a double-click on a piece of the character (the Ctrl+V ray).
  - Keys: Esc closes the viewer first, ← / → step through the open picker's list (else the slot's whole list), Enter on
    a focused tile in the mode shows it; a phone swipes left / right on the stage. Esc / ✕ / the toggle off restore the
    camera, its limits, the character and the picker exactly. บันทึกภาพ in the viewer saves the floating piece alone.
    Viewing never adds an undo step; renderer.info.memory stays flat over 30 steps (8 geometries / 10 textures).

## Thai text: centring by eye (user 2026-11-09)

User: "when attempting to align Thai text to the middle of the text box height almost assume and measure all the
วรรณยุกต์ and สระ like สระ ุ that make the text not look centered by eye even though it is middle aligned by the code
convention".

- **Why code centring looks wrong:** flexbox `align-items: center`, `line-height`, `vertical-align: middle` and a
  canvas's `textBaseline = "middle"` centre the font's line box (its ascent + descent), not the letters you see. A Thai
  font's line box keeps room for the marks above (วรรณยุกต์ ่ ้ ๊ ๋; สระบน ิ ี ึ ื; ั ็ ์, and stacks of two, as in
  ที่ ปั้ ชื่อ) and below (สระล่าง ุ ู, ฺ, the tails of ฎ ฏ ญ ฐ), and the Thai and Latin metrics of one font differ.
  So a word without marks sits off-centre in its box, and a word with many marks reads crowded at one edge.
- **Measure the ink, not the box:** the text's real height, marks included. In a page, a canvas with the same font
  and size: `ctx.font = getComputedStyle(el).font; const m = ctx.measureText(text);` then `m.actualBoundingBoxAscent`
  (above the baseline) and `m.actualBoundingBoxDescent` (below). The ink's middle is
  `(actualBoundingBoxAscent - actualBoundingBoxDescent) / 2` above the baseline; move the text (`transform:
  translateY(...)`, or uneven padding) until that middle is the box's middle. Wait for the web font first
  (`document.fonts.ready`), or the fallback font gets measured.
- **Assume the marks when the text can change** (a label that swaps, a name from data, หยุดท่า / เล่นต่อ): measure a
  reference that holds the tallest upper stack and the deepest lower vowel the box may show (for example `ปั้ญู`), so
  the text stays put when it changes; for fixed text, measure that exact string.
- **Check by eye, then by pixels:** screenshot the box, find the first and last rows that have text ink; the gap above
  and the gap below should match within about 1 px (at 2x, 2 px). Digits stay in JetBrains Mono, whose metrics differ
  again: measure a mixed run (Thai + digits) as it renders.
- Everywhere Thai text sits in a box: buttons, tiles, chips and badges (`.sk-badge`), the toolbar, the key hints'
  `<kbd>` row, toasts, the piece menu, the nameplate, 3D labels drawn on canvases.

## Session log

Entries moved from 12tails-video's NOTES.md (2026-11-05 to 2026-11-09), then this repo's own.

- **2026-11-05 (wardrobe on the office screen)**: the office PC is 2560 x 1080 at 100 % (the page gets ~900 px of
  height); user: "not scaled to my smaller work PC". The eight topic blocks (112 px minimum each) overflowed into a
  scrollbar. `wardrobe/index.html` now has a short-screen layout (`max-height: 1000px` and `min-width: 900px`):
  blocks two abreast filling the height, a 340 px side panel, the picker 40 % of the stage wide (the hero stands
  mid-stage: wider covered her) with auto-fill columns (136 px items, 190 px faces). Taller screens unchanged.
  Checked in Playwright at 2560 x 900 and 2560 x 1300; Chrome caches the page: Ctrl+F5 after an edit.
- **2026-11-05 (wardrobe: equip a set in one press + undo / redo)**: user: "an equip set button that equips all
  related equipment in a single press, only sets with 2 or more complementary components". New topic ชุดเซ็ต
  (`buildSets` in `wardrobe/index.html`). Grouping by item code alone was too noisy (a number is shared by
  unrelated shared items: hat 15 = santa and summer; Rabbit 23 = standard + nurseGunR), so: (1) by name: a piece
  joins the outfit its name starts with at a word boundary (hallowFlower -> hallow, not halloween), else its name
  minus the last word (holyHat -> holy; outfit holyRobe -> holy); a trailing capital is a recolour variant set
  (mothLaternR + mothHatR = moth R), digits pick the first (championFlag1); (2) by code, only for strays: a piece
  joins an outfit that lacks its slot and whose name-matched pieces carry its class-tag code number
  (starMicrophone w_shp45 -> superStar), or a costume outfit with no name-matched piece carrying the number itself
  (fur a_shp5 + sheepDoll + sheepHat); shared tags all* / fem / mal never count (t_allhlw5 ReaperTrinket).
  Sets with no outfit need a common code number (party hat 7 + whistle 7). Weapons: item_map two-piece codes =
  first piece in the main hand, second in the other (the game's pairs cross names: Chameleon w_chm61 = standardBow
  + legendArrow), Panda / Wolf `_L` / `_R` (case-insensitive) to their hands, the Wolf's one-piece sword in both.
  Listed only with 2+ pieces (outfit / weapon / head / back); slots the set lacks keep what they have. Undo /
  redo (buttons + Ctrl+Z / Ctrl+Y) over outfit, colour, face and the four slots, per class. Checked in Playwright
  on 8 classes (35-38 sets each) and a press + undo + redo.
- **2026-11-05 (wardrobe: R / V outfit editions; icons fixed from BB's code table)**: user: "the R and V variants
  didn't get the texture colour change, only the hat" and "wrong icons all over the wardrobe, but correct model
  application". (1) BB ships each outfit's recolour editions `<Class>_<armor><c>R / V.png` (Sheep holyRobe R + V,
  standard R + V, moth R ...); wardrobe_data.py had packed only colours 1-5. `pipeline/wardrobe_editions.py` packs
  them from the BB rip (649 textures, 12 classes; Monkey theurgist R / V and spider 4R are broken in the office PC's
  copy of the rip only: the home PC's are intact, 660 there)
  as `outfits.json` "editions": {R: [colours]}; wardrobe_data.py packs them too from now on (untested: no TTO
  bundles on the office PC). The page's outfit state has an edition ("" / R / V): a set R / V switches it, the outfit
  picker has แบบ buttons, undo covers it. (2) wardrobe_icons.py had traced code -> model out of TTO's compiled
  switches and ~27 codes per class came out shifted (Rabbit a_rab10 -> superStar; BB: a_rab10 / 11 / 12 =
  standard with textures standard<c> / <c>R / <c>V). Models were right (by name), icons (by code) were not.
  `pipeline/bb_item_codes.py` reads BB's readable DecompiledSource/<Class>Equipment.cs (a `nArmor == "code"` compare
  -> the next Resources.Load; armor textures give the edition; negated compares skipped; two pieces per weapon code
  only where most codes load two = Chameleon bow + arrow, Whale weapon + shield, else the second load is the
  switch's default branch), keeps TTO's trace for codes BB lacks, and rebuilds `icons.json` (+ per-outfit edition
  icons) from the icons already extracted; the old files kept as `item_map_tto.json` / `icons_tto.json`. The page's
  JSON fetches use `cache: "no-cache"` (a rebuilt outfits.json was served stale). Trap: `wardrobe.setOutfit` (the
  scripted-check helper) dropped the edition argument and made a correct page look broken: check helpers too.
  User: "move character colour selection out from outfit to set equipment": the สีตัวละคร 1-5 buttons are in the
  ชุดเซ็ต picker's header now (a set keeps the colour when it changes the outfit); the outfit picker keeps แบบ.
  User: "add a first option in set: remove everything; cat head: remove the none option and use default as
  default": ถอดทั้งหมด = the standard outfit, no edition, no weapons / headpiece / back item (colour and face
  stay). `BASE_HEAD = {cat: "default"}` (the only class with a base headpiece, `Cat_default.png`): the Cat starts
  with it, its หมวก list has no ไม่ใส่ and lists it first, and setProp turns an empty Head into it (so undo and
  ถอดทั้งหมด respect it). Also: the picker body is emptied when a picker opens (the set / prop lists load async,
  and a quick click could hit the previous picker's tiles: a Cat set got applied to the Sheep in a scripted check).
  User: "series equipments flickering like crazy, e.g. Sheep moth and Bat butterfly head piece": **z-fighting**. The
  game culls back faces and models a two-sided sheet as two faces back to back (same corners, opposite winding);
  the page drew every mesh double-sided, so each pair fought. Found in 21 outfit meshes (Sheep moth 26 pairs, Bat
  butterfly 78, the pvpArmors, Sheep legend ...) and 8 props (mothHat, butterflyHood, mummyHead, pvpHelmet,
  starMicrophone ...). `stacked(pos, idx)` in the page finds such pairs; those meshes (outfit, prop, skinned prop)
  are drawn FrontSide, the rest stay DoubleSide (the outfit keeps a front-sided clone of its material, updated
  with colour / face changes). Checked from front and back: no holes.
- **2026-11-09, the wardrobe's home is this repo** (the user asked whether it belongs in the Bible repo; the cons:
  that repo is public while this one is private, the Bible's single-file and no-browser-check rules don't fit a served
  3D app, and the wardrobe and the video pipeline read each other's folders; the user: "let's make the wardrobe based on
  12tails-video repo then"). CLAUDE.md says so; the plan (`plans\wardrobe_online_plan.md`) and the decision log
  (`.superpowers\sdd\2026-11-07-wardrobe-online\`, minus the Bible's mirror art) were moved here from the Bible repo
  (checked identical, then deleted there; the Bible's `art\` stays, its `index.html` cites `art\HOW.md`), and the Bible's
  `bible-hub-tools` skill now points here (it still named `D:\12tails-video\comic-skit` and `wrangler pages deploy`).
  The worktrees `comic-skit-wardrobe-online` / `-wasd` here and `D:\12tails-wardrobe-online` (Bible), fully merged and
  clean, no junctions inside, were removed (`git worktree remove`; their branches kept). The Bible one's empty folder
  stayed: another process held it ("being used by another process"); delete it once that window is closed.
- **2026-11-09, the wardrobe moved to its own repo** (the user: "make a separate repo for the wardrobe, independent of
  the video works, so there's a clear line between them", after a day of wardrobe, trailer and fight commits meeting in
  one repo and one NOTES.md). `jumpptty/12tails-wardrobe` at `D:\12tails-wardrobe` (office `C:\work\12tails-wardrobe`),
  made with `git filter-repo` from this repo: its 23 files keep their history, this repo's history is unchanged. Its
  untracked data (`wardrobe\data`, `wardrobe_dist` + reports, the online copy's decision log) moved by its
  `pipeline\adopt_from_video.ps1`; the page's prop textures are now its own (`wardrobe\data\props\tex`). The readers
  there point at the sibling folder: `skitlib.WARDROBE` (tto_placement, _wardrobe_prop), `skins.py` WARDROBE_FACES,
  `extract_tto_props.py` (item_map.json), `trailer_common.WARDROBE_DIST`. This NOTES.md took the wardrobe sections and
  four wardrobe-only log entries (2026-11-05: the office screen, equip a set, R / V editions; 2026-11-09: the
  wardrobe's home); mixed entries stay there. The video's `transfer_to_drive.ps1` lost `-WardrobeOnly` and its
  `wardrobe\data` entry (this repo has its own transfer). Design and plan: `plans\wardrobe_split_*.md`.
- **2026-11-09, the switchover on the home PC** (plan Task 5): the peer session `12tails-video-18` held its builds;
  `adopt_from_video.ps1` moved `wardrobe\data`, `wardrobe_dist` + its two reports and
  `.superpowers\sdd\2026-11-07-wardrobe-online` (renames, ~1 s), copied 1,131 prop textures (0 missing) and repointed
  the Desktop shortcut. Checks: 37 unit tests; `wardrobe_moves_check.py` over every class, `errors: []`; a page load
  dressing Cat (knife, hat) and Wolf (sword, Angel Wing) fetched 4 `data/props/tex/` textures, all 200; the video's 53
  trailer tests against the moved `wardrobe_dist`; `skitlib.tto_placement` / `_wardrobe_prop` in background Blender.
  **Trap: a fresh clone checks the page out CRLF** (global `core.autocrlf true`) while the old folder's copy was LF;
  the publish copies the page's bytes, so the rebuilt `index.html` differed from the live one in line endings only
  (data byte-identical, 6,896 files). `.gitattributes` now pins `wardrobe/index.html` to LF.
- **Moving data between PCs: Google Drive, no flash drive** (user 2026-11-09: "No flashdrive, google drive only"):
  `pipeline\transfer_to_drive.ps1 -Dest C:\Users\Jump\Desktop\12tails-wardrobe-transfer` (1 s), the user uploads that
  folder to Google Drive (Drive for desktop is installed here but wasn't running: `C:\Program Files\Google\Drive File
  Stream\<version>\GoogleDriveFS.exe`) and downloads it at the office. Drive's web download of a file this size asks
  to confirm it can't virus-scan it.
  Flash-drive form, if one is ever used: `pipeline\transfer_to_drive.ps1 -Drive <letter>` writes
  `<drive>:\12tails-wardrobe-transfer\` = `wardrobe_data.tar` (0.35 GB, 7,668 files, prop textures included, 6 s),
  `12tails-wardrobe.bundle`, `README.txt` (restore: clone, `tar -xf ... -C C:\work\12tails-wardrobe`, then once
  `adopt_from_video.ps1 -SetAside`, which renames the office's older `<video>\wardrobe\data` to `wardrobe_data_old`).
- **2026-11-09, the switchover on the office PC**: the video's `move_project.ps1` ran from this session with VS Code
  open on this folder (its dry run found 0 holders: only a window on `comic-skit` itself blocks it): 48 items up into
  `C:\work\12tails-video`, origin -> `jumpptty/12tails-video`. Then `adopt_from_video.ps1 -SetAside`: the office's
  04/11 data is `C:\work\12tails-video\wardrobe_data_old` (delete when happy), 0 prop textures missing, the empty
  `<video>\wardrobe` removed. The move left two Desktop shortcuts stale, fixed by hand: `wd.lnk` (pointed at the
  video's gone `wardrobe.cmd`, now this folder's) and `comic-skit.lnk` (its target was the old folder itself, which
  the move only matches for paths inside it; now `C:\work\12tails-video`). `subst D: C:\work` drops at every sign-out,
  so the office's Startup folder has `map_D.cmd` (`if not exist D:\ if exist C:\work\ subst D: C:\work`; tested by
  unmapping and running it). `wardrobe_data_old` deleted (user's go, 6,455 files, 277 MB). Checks: 42 unit tests, the adopt test, `wardrobe_moves_check.py` `errors: []` (Playwright's headless
  Chromium had to be installed here first: `uv run --no-project --with playwright playwright install chromium`).
- **2026-11-09, two bug reports traced (no fix yet)**: (1) "Chameleon Legend set doesn't have legend bow": the set wears
  standardBow + legendArrow. Cause: `item_map.json` from `bb_item_codes.py`, whose rule "each load belongs to the compare
  just before it" fails on the obfuscated nesting in `<Class>Equipment.cs`: `if (!(nWeapon == "w_chm60")) { if w_chm61
  {empty} else if w_chm62 {legendBowR/ArrowR} else if w_chm82 {...} else {standardBow} }` then legendBow / legendArrow
  AFTER the block (the w_chm60 body; w_chm61's empty branch falls through to it: its decoy `31401 - 585668 != -554267`
  is false). So w_chm60 is skipped (negated), w_chm61 keeps the TTO trace (standardBow + legendArrow, wrong), and the
  weapon `cur` never resets, so w_chm82 collects 7 loads. buildSets then reads legendArrow as w_chm61's second piece
  and puts its first, standardBow, in the main hand; legendBow is in no two-piece code, so it is never a first piece.
  Same cause, second symptom: legendBow's only code is w_chm82, so its icon is Flaming Arch's (`chm82.webp`).
  Scale: the three shapes (negated-only 34, empty branch 19, glued 2) occur in every class's source, but mostly the
  TTO trace happened to be right. Wrong and visible: only Chameleon legend (set + icon). Wrong, not visible: Whale
  w_whl51 = standard (game: royal), w_whl61 = ladybug R (game: legend), w_whl79 glued 8 loads (the royal / legend
  sets get their pairs from w_whl50 / 60, right by luck). `pipeline/wardrobe_sets_check.py` (new, headless) over 12
  classes / 454 sets: one set with another set's weapon, Chameleon legend (Penguin box + paperCup is the beggar
  costume joined by code 5, not flagged). (2) "Panda doesn't have Worm R in the armor selection, but the set has it":
  by design since 2026-11-07 (editions picked in the set tab): the ชุด picker lists each outfit once
  (`C.outfits.map`), so all 132 R / V editions (11 per class) are missing from it, not only Worm R; the check finds
  every one reachable through some set (0 unreached).
- **2026-11-09, bug 1 fixed: `bb_item_codes.py` reads the braces** (user: "yes" to the parser fix). `parse()` now takes
  each compare's own `{}` block: a positive code's loads are inside it; a negated code `if (!(n == "c")) {...}` owns the
  loads after its block up to the parent block's end; an empty branch falls through to the enclosing negated code's
  loads; a default `else` is no code's. `item_map.json` changed in 14 codes, all to the game's pattern (60 / 61 plain,
  62 R): Chameleon w_chm60 / 61 legendBow + legendArrow (was missing / standardBow + legendArrow), w_chm82 flaming only
  (was 7 pieces), w_chm51 royal (was royal R); Whale w_whl51 royal, w_whl61 legend, w_whl79 eclipse only; Cat t_cat61
  legendTrinketR (was sandTopaz, which is t_all51; the icon cat61 is the starred legend trinket); t_*62 legendTrinketR
  added for Bat, Chameleon, Mole, Panda, Whale, Wolf. Effect: the Chameleon legend set wears legendBow (the only set that
  changed, all 12 classes diffed), legendBow's icon is chm61 (was Flaming Arch's chm82); `wardrobe_sets_check.py`
  passes. The script's run is under `main()` now (importing it no longer rewrites the data) and its kinds are sorted
  (two runs gave the same JSON in a different key order); `pipeline/test_bb_item_codes.py` tests the four shapes on
  the Chameleon's real nest. **Home PC: after `git pull`, run `py -3 -I pipeline\bb_item_codes.py` once** (it needs the
  Bible's DecompiledSource, both PCs have it), or the next data tar from home carries the old map back. The video
  repo's `extract_tto_props.py` reads `item_map.json`: those 14 codes now map as above.
- **2026-11-09, R / V editions in the ชุด picker** (user: "yes" to bug 2; reverses part of 2026-11-07's "editions in the
  set tab"): every edition is a tile of its own right after its outfit (Worm, Worm R; icon = the edition's own from
  icons.json "editions"), `wearOutfit(name, e)`: the same outfit changes only the texture (`setColorOrFace`), another
  loads it (`setOutfit`); the plain tile now means ปกติ (before, an outfit pick kept the worn edition); a colour the
  edition lacks moves to its first colour. Edition tiles carry no skin tools (one skin covers every edition) and are
  `data-ed` cells, skipped by `syncTiles` and the viewer's list. Pressed = outfit and edition. Undo covers it (`pick` ->
  `tracked`). Checked: `wardrobe_sets_check.py` (now also: every class's 11 editions have a tile; Panda Worm R picked ->
  worn + pressed, undo -> standard, plain Worm -> no edition, Worm R again; screenshot), `wardrobe_moves_check.py`
  (Quick Fire with Added Fire: quickFire2 0.4 -> quickFire3 2.1 s). One run logged a transient
  `ERR_CONNECTION_REFUSED` that two reruns didn't repeat; the moves check now prints a console error's URL.
- **2026-11-09, skill sounds online: feasibility** (user: "analyze whether it is feasible for the cloudflare server to
  hold all skills sfx to play along character animations"; analysis only, nothing built). Hosting: easy. The BB rip has
  1,627 hero WAVs (+36 that Python's `wave` can't read, likely not plain PCM; ffmpeg should) under
  `Resources/gameassets/characters/heroes/<cls>/{sounds,voices}`: 32 min in all, mostly mono 22 kHz, median 1.0 s,
  longest Sheep lullaby 17.8 s. At 48 kbps mono AAC that is 1,920 s × 6 KB/s ≈ 11.5 MB; the files would take the
  online copy from ~6,900 to ~8,500 of Cloudflare's 20,000. Where each sound plays is readable: the skill coroutine
  loads it by path and plays it (`Resources.Load(".../Wolf/Voices/bladeFang1")` then `audio.PlayOneShot`,
  `Wolf.cs:26536-26548`; random picks like armorBreak1 / 2, `:22904-22947`; Blood Fang swaps bloodFang1 / 2,
  `:26451-26512`), and the effects it spawns carry their own play-on-awake sound (`createEffect(armorBreak_ring)`,
  `:22966-22976`; about 550 hero effect prefabs have an AudioSource, clip by GUID via the WAVs' `.meta`). Animation
  events are only footsteps / wing flaps (155 of 2,933 clips: playRunStepEvent, playWalkStepEvent ...). The work is the
  cue timing in the flattened coroutines (done by hand for Blade Fang's clips), not the hosting.
- **2026-11-09, skill VFX too: feasibility** (user: "not just sfx, the vfx too"; analysis only). BB is Unity 3.5.7f6.
  1,668 effect prefabs (hero ones 60-96 per class). What they are made of (prefabs containing): the game's own scripts
  `EffectControl` 1,339 and mesh emitters `RingEmitter` 717, `ImageEmitter` 490, `LineEmitter` 417, `VortexEmitter` 88,
  `EmblemEmitter` 33, `BoltEmitter` 30, `TrailEmitter` 25 (+ `ProjectileControl` 67, `AlphaTimer` 62, `UVScroll` 6;
  128 scripts in all, most one-offs); Unity's legacy particles (Ellipsoid emitter + animator + renderer) 552; Shuriken
  `ParticleSystem` only 46; legacy `Animation` 272; `SkinnedMeshRenderer` 170. 663 materials, ~92% on Unity's built-in
  particle shaders (fileID 200-207 + 7: blend modes), a few custom (Additive / Alpha / MultiplyOffset, Opaque1/2,
  Phoenix); 608 textures, 23.6 MB as PNG. **Trap: the rip has no emitter settings** (every script's MonoBehaviour is
  just `m_Script`; the video repo's skits rebuilt effects from textures for that reason). They are in BB's
  `12TailsOnline_Data/resources.assets` (type tree on, but MonoBehaviour's tree is only the 24-36-byte header; the
  fields follow as raw bytes in declaration order): 1,284 objects of 212 bytes = 24 + RingEmitter's 188 (13 floats,
  2 Vector3, 5 Color, Vector3, float, int, float, bool padded to 4, int), decoded with UnityPy's `get_raw_data()` +
  `struct` (`<13f6f20f3ffifbxxxi`): Life 0.3, Emission 2 / 0.1 s, radius 0 -> 2, width 0.3 -> 0, ringTri 24. Legacy
  particle settings did survive in the rip YAML (`EllipsoidParticleEmitter` minSize / minEnergy / minEmission /
  worldVelocity, `ParticleAnimator` colorAnimation[0-4], sizeGrow). Effects are spawned by the same coroutines
  (`createEffect(prefab, pos, rot)`), many at the target, which the wardrobe has none of.
- **2026-11-09, skill effects + sounds pilot: Wolf Armor Break, Cross Break, Grand Cross** (user: "let's try wolf cross
  break, armor break, and grand cross"). Local only so far (the publish doesn't copy the effect data).
  - Data: `pipeline/wardrobe_fx.py wolf --fx ... --voices ...` -> `data/wolf/fx.json` (effects: node tree, transforms in
    Unity space, components; materials), `data/fx/tex/*.webp`, `data/wolf/sfx/*.mp3` (64 kbps mono). It reads BB's own
    files, not the rip: `mainData`'s ResourceManager (16,645 Resources paths) -> the prefab in `resources.assets`;
    materials, textures and AudioClips sit in `sharedassets1.assets` (a PPtr's fileID is read against the externals of
    the file holding the reference; each file numbers its own). MonoBehaviour fields decoded from raw bytes with
    `LAYOUTS` (EffectControl 32, RingEmitter 188, ImageEmitter 188, LineEmitter 180; every decode must use all bytes),
    script names from the MonoScripts in `sharedassets0.assets`. Unity 3.5 traps: `m_Component` = (classID, PPtr) pairs;
    material property keys are `{name: ...}`. Built-in shaders by id = the Particle shader files alphabetically from 200:
    200 Additive, 202 Additive (Soft), 203 Alpha Blended (borne out by 1,200 materials' tints and texture alpha).
  - Page: FX section (`FX_CUES`, `Fx`, `ringEmitter` / `imageEmitter` / `lineEmitter` / `legacyParticles`, `Sound`):
    each effect is built in Unity's space inside a group scaled (-1, 1, 1). Behaviour from four read-only agent specs of
    the decompiled scripts (cited in the code comments) and Unity 3.5's legacy particle docs: emitters make all their
    elements at once and stagger them; colour through 5 keys (LineEmitter's burst mode uses 2.5, a game quirk kept);
    ImageEmitter angles are radians; ParticleRenderMode 0 / 2 billboard, 3 stretched, 4 horizontal, 5 vertical;
    sizeGrow = x (1 + g) a second, damping = x d a second; EffectControl stops legacy emitters and ImageEmitters after
    `life`, destroys at `life + afterLife`. Cues traced from the coroutines (Armor Break: voice + ring at 0, slash by
    rank = armorBreak2 at 0.7 s; Cross Break: voice at 0, ring 0.1 s, cross 0.6 m ahead at 1.2 s; Grand Cross: voice +
    ring at 0, wave at the mark 0.6 m ahead at 0.6 s). Sound: Web Audio, unlocked by the first click / key, เสียงท่าทาง
    toolbar button (on by default, localStorage).
  - **Trap, additive light on a transparent canvas:** the stage is a transparent canvas over a white CSS background, and
    a browser drops colour where the canvas alpha is 0, so plain additive effects showed only over the hero (and written
    alpha made grey squares). The additive materials now write premultiplied colour with alpha = the brightest channel
    (`onBeforeCompile`): over dark that is the game's added light, over white the coloured parts stay.
  - Backdrop, the user's pick pending: `?fxbg=dark` (default: the stage darkens while a move with effects plays),
    `spot` (a dark glow behind the hero), `white`. `pipeline/wardrobe_fx_check.py` shoots all three into
    `<out>/compare.html`, samples the live effects, and fails on page / console errors or failed requests.
  - Open: Cross Break's stretched slashes come out huge at the wardrobe's close camera (lengthScale -1 / velocityScale
    -1 read as size + speed, up to ~8 m; the anchor and sign are the spec's open points); sizeGrow's formula; no game
    footage compared yet.
- **2026-11-09, Feral Strike added to the effects pilot, timed** (user: "try adding feral strike and time"). Coroutine
  `RPC_feralStrike` (`Wolf.cs:28952-29704`): clip (cut in) + voice feralStrike1 / 2 + `feralStrike_ring` (Instantiate,
  so no EffectControl owner) at 0; `feralStrike` with the dash at 0.3 s; standby at 1.0 s. `feralStrike`'s
  EffectControl has followState, so the game ends it when the hero's action changes: a 5th cue value (the clip time
  of that change) does that now. Both effects use only component types already built, so the work was: trace the
  coroutine, probe the prefabs, extract, one cue line. Check fix found on the way: the intermittent
  ERR_CONNECTION_REFUSED in the headless checks was the stdlib test server's 5-connection queue (the page loads dozens
  of icons at once); all three checks now set `request_queue_size = 128`. `wardrobe_fx_check.py` also shoots each
  skill's busiest frame (`_peak`), since short-lived parts fall between swiftshader's slow frames.
- **2026-11-09, office publishing** (user: "hide the pilot in public copy and deploy from office made possible";
  "check RippedAsset from all servers"). Page: the effects pilot hangs on `const FX_ON = true;`, the publish sets it
  false and hides the sound button. `wardrobe_publish.py`: the rip found under either PC's Bible. The office rip has 177
  zero-filled files, all under heroes\monkey (armour textures, face overlays, .fbm, 24 trinket prefabs, effect
  prefabs, sounds). Textures: `pipeline/bb_rip_fix.py` exports them again from BB's game data into data/bb_rip_fix
  (self-check: re-exported intact PNGs equal the rip's pixel for pixel), used only when the rip's file can't be read.
  Props: when BB's prefab is missing or zero-filled, `compare_prop` compares with the Reborn rip beside it
  (`RippedAssets_Reborn`, all 24 intact); `read_mesh_shape` reads Reborn's newer mesh layout (channels, topology 1 =
  strip); 11 Wolf meshes readable in both rips are identical. Office build: 6,896 files (= home's count); 4 Monkey back
  items still dropped (their Reborn meshes are multi-stream / skinned). Tested (fallback test in test_wardrobe_publish).
- **2026-11-09, home PC catches up on HANDOFF**: `bb_item_codes.py` rebuilt `item_map.json` / `icons.json` (exactly the
  14 codes listed above changed; `wardrobe_sets_check.py` exit 0, 0 foreign weapons). `wardrobe_fx.py wolf` built the
  pilot's data (8 effects, 13 materials, 13 textures, 13 sounds; `wardrobe_fx_check.py` exit 0, all 13 sounds loaded,
  `errors: []`). `wardrobe_publish.py --out wardrobe_dist`: 6,899 files (+3 on the last report), 270.1 MB,
  `data-7e0350ddb2`, `FX_ON = false`, no fx / sfx files, check: no problems; 6.5 min. 46 unit tests pass. Not deployed
  (the user's step, HANDOFF). The Bible commit `0704e0f6` is still not on GitHub (office to push).
- **2026-11-09, effects for every class, step 1 (prep) done** (HANDOFF "Next up", the plan agreed at the office).
  - Cues moved out of `index.html` into `wardrobe/fx_cues/<cls>.json`, tracked, one per class (11 are `{}`), each clip
    `{why: the source lines, cues: [...]}` (JSON has no comments, so the citations moved into `why`). The page reads the
    class's file when it shows the class (`fxData`: cues, then `data/<cls>/fx.json` if any); with `FX_ON` false (the
    publish) it fetches nothing; the publish copies only named files, so `fx_cues/` stays local. `FX.spawned` /
    `FX.missing` tally what cues spawned (a cue whose effect isn't in the data used to be skipped silently).
  - `wardrobe_fx.py <cls>` with no `--fx` builds what the cue file names (same lists as the HANDOFF's typed ones for
    Wolf). `Game.script_name` now reads a script reference against the component's own file (Mole `megapunch_hit`'s is
    not in resources.assets: it raised).
  - `wardrobe_fx_check.py`: classes from the cue files (`--cls` to pick), each cued clip's tile (the sequence holding it),
    a shot 0.15 s after each effect first appears (no typed times), fails on a cued effect or voice missing from the data
    or never spawned (tested with a bogus cue: exit 1, both messages).
  - `plans/fx_recipe.md`: the per-skill recipe (trace with `clip_flow.js` and an extra pattern, the flattened state
    machine's `Yield(n, wait)`, max rank, distance, followState, target-spawned effects left out, build, check).
  - `pipeline/wardrobe_fx_inventory.py` -> `plans/fx_inventory.md` / `.json`: every effect a class's `<Class>.cs` loads
    from its own Effects folder (699; the code also loads 12 pet effects and other classes' buffs / potions, ~28 per class,
    counted apart), its parts, and whether ready (built parts only, and `wardrobe_fx.effect()` extracts it in memory).
    **403 of 699 (58%) are ready today**; Mole is the worst off (25 of 78: bombs and missiles are meshes). Greedy build
    order: VortexEmitter +23, EmblemEmitter +19, EmitterControl +18, StaticMesh +10, AlphaTimer +9, Animation +18,
    SkinnedMeshRenderer +52 (the mesh parts unlock effects together: 80 for the three), TrailRenderer +14,
    Rabbit_potion +13, EffectControl(child) +12, TrailEmitter +10, BoltEmitter +9; then one-offs (the classes' own
    scripts). Physics parts (colliders, Rigidbody) don't count: they draw nothing.
  - Checks: Wolf's four skills pass the new check on all three backdrops (13 sounds), moves check `errors: []`, 46 unit
    tests, the adopt test; the publish's page rewrite still applies to the edited page. `wardrobe_dist` was built before
    this (no public difference: the pilot is off there).
- **2026-11-09, the piece menu: hover and click a piece on the model** (user: "instead of viewing individual object,
  downloading 2D and 3D and uploading buttons scattered all around the place, I want the user to be able to hover and
  click at each individual item in the model directly, with mild hover effect, clicking at each piece will then show
  basic info of that item and dropdown list of actions download upload, view this item only, etc.").
  - Hover: the piece under the mouse (`pieceAt`, about ten rays a second in the render loop, mouse / pen only) lights up
    and the cursor turns to a pointer; never in the viewer, while dragging, or in a screenshot (`hoverClear` first). Three
    looks mocked side by side (`?hover=gold` default / `lift` / `dim`, `checks/piece_menu/hover_close.png`, the
    user's pick pending): gold = diffuse colour x (1.18, 1.08, 0.92) + emissive 0.07 x gold. **Trap: an added glow lifts
    dark colours most** (the first try, emissive + 0.2 x gold, turned the Wolf's dark-blue outfit sepia); a factor keeps
    the darks, but a full red can't brighten (the red weapon showed nothing), hence the trace of added gold. Lift (x 1.22)
    is close to invisible, dim (the rest x 0.6) barely shows.
  - Click (no drag over 5 px, under 0.7 s, one finger): the menu `#pmenu` beside the pointer, kept in the window (moved to
    `body`: inside the stage a phone's panel drew over it). Head: icon, name, slot · ใส่อยู่ / ยังไม่ได้ใส่ · colour or
    ลายของคุณ · first set (+n) · ของจาก TTO / ToT. Actions: ดูชิ้นนี้อย่างเดียว (the viewer), ใส่ชิ้นนี้ (not worn),
    เปลี่ยน<slot> (opens its picker), ถอด<slot>ออก (props; not the Cat's base head), ดาวน์โหลดลาย (PNG) and
    อัปโหลดลายของคุณ (one per texture when a piece has two), ดาวน์โหลดโมเดล 3D (GLB), คืนลายเดิม (when skinned); wear /
    take off are one undo step. The menu's piece stays lit while it is open.
  - Other ways to the same menu: right-click / long press on a picker tile (pieces not worn: ใส่ชิ้นนี้ instead of
    เปลี่ยน) or a topic ring; the viewer card's ตัวเลือก (no "view"); Ctrl+V on a two-texture piece opens it with วางรูปเป็นลาย
    1 / 2 (the picture kept); a menu item with a texture is a Ctrl+V target too.
  - Keyboard: the menu key / Shift+F10 on a tile or ring opens it under the element with the first action focused (Chrome
    gives a key-opened context menu a point inside the element, so the key press itself is noted: `ctxKeyAt`); a pointer
    opens it with the menu focused (no action looks chosen); ↑ ↓ Home End move, Esc / Tab close and give the focus back;
    the page's keys (Esc closing the picker, ← → in the viewer, WASD) wait while it has the focus.
  - Removed: the three tools on every tile (the ลายของคุณ badge stays as a label), the toolbar's ชมชิ้นส่วน (`#vmode`),
    the card's ดาวน์โหลดโมเดล 3D / ดาวน์โหลดลาย (and its two-texture choice). Phone pickers for items go four abreast like
    the rest (three only made room for the tools). The WASD hint says คลิกที่ชิ้นบนตัวละครเพื่อดูเมนู.
  - **The video repo's trailer breaks on the next publish**: `trailer_features.py` clicks `#vmode` ("inspect", "download")
    and a tile's `.sk[data-sk="up"]`; it films `wardrobe_dist`, which still has them until it is rebuilt.
  - Check: `pipeline/wardrobe_menu_check.py` (31 checks: hover per piece, a menu per piece inside the window, a drag opens
    none, PNG and GLB downloads, upload through the file chooser then reset, take off + Ctrl+Z, the viewer's ตัวเลือก and
    Esc order, the double-click, right-click a tile + wear, Shift+F10 + arrows + focus back, a phone tap; no errors).
    Also: sets, moves and effects checks `errors: []`, 46 unit tests, the publish's page rewrite. Heredoc trap seen
    twice this session: a `\n` inside a Python heredoc came out as a real line break in the written file (a toast string
    split in two, a PNG signature turned into raw bytes); edit such lines with the Edit tool.
- **2026-11-09, the piece menu published (built, not deployed)** (user: "rebuild it to publish"): `wardrobe_dist` 6,899
  files, `data-7e0350ddb2` (unchanged: only the page changed, +10 KB, so visitors keep the cached data), check: no
  problems, `FX_ON = false`, no `#vmode` / clipboard code. Smoke test of the built copy served on its own (hover on the
  outfit, its menu: view / change / png / glb / up, no errors). The user deploys; the trailer fix waits in HANDOFF
  "Video repo".
- **2026-11-09, hover look picked: pulsing rim** (user: "suggest a few more hover effect mocks", then "we will go with
  pulsing rim", "stronger rim strenght please"). Mocked side by side (`pipeline/wardrobe_hover_mocks.py`, the idle
  paused, animated looks at three moments; `D:\12tails-wardrobe\checks\hover_mocks\compare.html`): gold, pulse, outline,
  rim, sweep, then rimpulse. The overlay looks draw a copy of the piece (same geometry and skeleton, never hit by the ray)
  with the original's texture for the cut-outs. Rim = fresnel `pow(1 - |n.v|, 1.4)`, gold x 1.6, alpha x 1.8, **added**
  light (blended, it went muddy brown fading into the black afro); rimpulse breathes between half and full every 1.4 s.
  The others stay as `?hover=gold|lift|dim|pulse|outline|rim|sweep`.
- **2026-11-09, TTO online** (user: "Also add TTO stuff to the public deployement, I've got the green light, BUT 1.
  Change the pink dot to TTO small logo instead. 2. TTO shouldn't be downloadable nor uploadable, it's preview only 3.
  only include released assets, I will mark them from html picker").
  - `wardrobe_publish.py`: `wardrobe\tto_released.json` ({cls: {kind: [names]}}) names the TTO-sourced items to publish
    (TTO-sourced = what the BB rule drops for being TTO's: tto flag, or BB's file can't be matched); they are copied from
    the local data (mesh, textures, icons, prop textures, the skill / emotion icons a released clip shows: the page's
    `EMO` table is read from index.html) and marked `"tto": true`. Every candidate goes into `wardrobe_dist_tto.json`
    (beside the report) for the picker. No released file = the old face rule, nothing else of TTO (byte-identical data).
    ToT's own items (`tot`, hero-skinned hats) never go online.
  - Page: TTO's mark = `wardrobe\ui\tto.webp` (64 px from the Bible's `TTO_icon.png`) on TTO tiles and in the menu head
    (the publish allows it in the ui folder beside the proven Recolor Drug icons). `TTO_LOCK` (the publish sets it;
    locally `?ttolock`): a TTO piece's menu has no download / upload / reset (the user: no note needed), the skin / model
    functions and Ctrl+V refuse it, and a BB outfit's 3D file swaps a worn TTO face for the class's first BB face.
  - Picker: `wardrobe\tto_picker.html` (local only; http://127.0.0.1:8771/wardrobe/tto_picker.html), class tabs,
    click to mark, saves `tto_released.json`. The user preferred rules in chat instead; the file was written from them:
    every class's Halloween outfit, weapon(s), hat; Bat Dream Band V / Dream Wand V; Clap and Wai; every TTO skill motion
    the Bible documents (clip -> skill through TTO's pseudo-C: golemCall = Rune Golem, solarCall = Sun Avatar,
    leviathanCall = Leviathan Breach, magmaQuakeAxe = Magma Quake, emperorPenguin = Emperor's March, missilePad = the
    Mole's Missile; left out: sanctumRaise = Buiten Offering, not in the Bible, and Cat shikifujin, which TTO never plays);
    the 10 TTO faces per class already online; no Quotation Flag; every shared item except Aura Bloodmoon / Undead Queen,
    Champion Wing, Moonlight Rabbit, Pumpkon Headband, White Wing, Witchy Wing. Dream Band V checked TTO-only: BB has
    dreamBand / dreamBandR only (prefabs, `BatEquipment.cs:2659`, `:2681`).
  - BB items that only looked TTO-sourced: the 12 Chinese Lanterns, Mole Legend Trinket, Penguin Hallow Lattern were
    dropped because the extractor baked their skinned meshes into a pose; now a baked node is BB's when BB's prefab has
    the skinned mesh of that name with the same vertex and triangle counts (all 14 pass), so they publish as BB. Whale
    `talk`: 75 of 76 channels equal BB's `talk_7.anim`; Foot_R's rotation lost BB's 360-degree twist at 1.30-1.73 s
    (`py -3 D:\12tails-wardrobe\pipeline\clip_diff.py whale talk`); a BB clip whose copy differs now goes online with
    BB's own keys (the user: "yes you should do that"). The local page still plays TTO's copy.
  - Checks: `pipeline/wardrobe_tto_check.py` (picker toggles and saved JSON, the TTO mark, the lock on a TTO outfit and
    not on a BB one), 38 publish tests (released items, unknown kind, baked props, BB keys for a differing clip).
- **2026-11-09, deployed by Claude** (user: "please change that Claude.md setting then deploy"; CLAUDE.md now lets Claude
  deploy when asked). `npx wrangler deploy --assets D:/12tails-wardrobe/wardrobe_dist --name 12tails-wardrobe
  --compatibility-date 2026-11-07` from an empty scratch folder (wrangler was logged in): 271 files uploaded, 6,826
  already there, version `5de09acb-20e5-4379-90a2-356c40544e24`. The live page has `data-a6cc4a90e6`, `TTO_LOCK = true`,
  `FX_ON = false`; the Wolf's Halloween outfit and the TTO mark answer 200. The auto-mode classifier did not block it
  this time. The live page has one unused CSS rule (`.pm-lock`) the repo's page no longer has: built just before it was
  removed; it goes with the next publish.
- **2026-11-09, Space and R** (user: "add space bar to stop the animation control, hint near the asdw", "R to reset the
  pose to idle stance"). Space pauses / resumes: the render loop gives the mixer, the sequence, the props' clips and the
  skill effects dt 0 (camera, hover, the viewer's turntable keep going); a new move resumes (`play()`). Space is left to a
  focused button while the visitor navigates by keyboard (`lastInput === "key"`) and to text fields; after a mouse click
  on a tile it pauses instead of pressing the tile again. R plays the idle (`idleName()`), like picking ยืนพัก. The hint
  row: คลิกที่ชิ้น... | WASD เลื่อนกล้อง | Space หยุดท่า (เล่นต่อ while paused) | R ท่ายืน. Checked in
  `wardrobe_menu_check.py` (pause holds the mixer, resume, a new move resumes, R from an emote to root); moves check
  `errors: []`. Not deployed yet.
- **2026-11-09, the key-hint row centred by eye** (user: "try fixing the hint container first", then "then deploy").
  `pipeline/thai_center_check.py <url> <selector>` (2x screenshot; per text run and per child box, the ink's gap above
  and below inside the box) measured: the keys' letters 0.8 px high (the key box was centred, its 2 px bottom edge
  lifts the letter's middle), the Thai runs 0.5 px high counted with their marks (ที่ ชิ้น เลื่อน above, ดู หยุด below).
  Fixed: kbd line-height 15 px + 1.5 px padding on top (same box, letter +0.75 px, now within 0.2 px); the Thai runs in
  `.kh-t` moved down by `transform: translateY(.5px)` (`top: .5px` snapped to a whole pixel and overshot to 0.5 px low).
  The run with marks both ways (คลิกที่ชิ้น...ดูเมนู) is now 6.5 / 6.5 px; the others share its baseline (the rule: as
  if they had the marks). Space reads lower than the capitals because of its p (a descender), as it should. Rebuilt
  (data unchanged, `data-a6cc4a90e6`), `wardrobe_dist_check.py` passed, deployed from a fresh empty folder (the last
  deploy's folder holds wrangler's `.wrangler` cache now): version `c1753290-953d-4a5c-a23d-f7b8968b9d9c`, Space / R and
  the hint live. Same deploy carries Space / R (555e6b0) and drops the stale `.pm-lock` rule.
- **2026-11-09, the Wolf's effects and sounds, the parallel way** (user: "let's start doing a single class, Wolf first";
  then "send more agents to research Wolf, each with is own reports only ... delegate only one agent capable of editting
  the file", "don't use playwright test, I will help you test"). Six read-only researchers wrote
  `plans/fx_wolf/{attacks,counters,misc,cast,tto,parts}.md`; the user's decisions are `plans/fx_wolf/decisions.md`
  (passives on, no Cast tile, instantCast one skill per play at even chance, Double Art rolled at 24 %, enemy hits out,
  a cast needing a target 10 m ahead). Groundwork (commit 439c7b1): the cue options / sound kind / skills map / rolls
  (comment above `cueOf` in index.html), voices as `sfx/v_<name>.mp3` apart from sounds (Wolf voices and sounds share
  names: crusader1, artCancel1, nAttack1-3, cAttack1-2, bladeFang1-2 are different recordings), `wardrobe_fx.py --probe`
  (read only), `wardrobe_fx_check.py --files-only`. Step times fixed after checking each claim in Wolf.cs by hand:
  nAttack2 0.64 (stage 3 from 1.44 s), cAttack1 0.8 + cAttack2 5.1 (full-charge ring 5.0 s in), bladeFang1 0.7 (a 0.5 s
  wind-up, the first hit at 0.7), bladeSong3 2.9 (bladeSong4 right after the 11th slash when skill 354 is learned),
  mirrorCounter1 1.0. The Bible lacks the Blade Fang wind-up and the Blade Song 2.9: offered to the user.
  - The one editor wrote `wardrobe/fx_cues/wolf.json`: 31 clips; Double Art (doubleArt + sublimeArt_ring, one roll) on
    the 24 skills whose code calls getDoubleArt (not the normal attacks, Charge Attack, Sky Slasher); the TTO skills as
    sounds only (their effects need a TTO reader and GroundHugEmitter / ArcRibbonEmitter / Shuriken). Build: 33 effects,
    88 sounds (`rip_wav` now also searches Resources\, for `sound/fx/aura1.wav`, the Blade Fang ring's); files check:
    no problems. Not tested in a browser (the user tests).
  - Known limits: a cue at exactly a step's end never fires (the step switches first), so the 11th Blade Song slash is
    bladeSong4's cue at 0; Twin Resonance's fire sound plays once (loops in the game); effects that outlive their clip
    restart with each replay; TTO sounds from other classes' folders (shatteringDream_hit, iceBreak) can't be cued;
    luck's bonus to Double Art ignored; old pilot voice files without `v_` are left in `data/wolf/sfx`.
- **2026-11-09, the Whale's lance and shield were in the wrong hands** (user: "Whale weapon left and right seems to be
  swapped"). BB's WhaleEquipment puts `getWeapon(code, 1)` = the lance on `mount_Hand_R` and `getWeapon(code, 0)` = the
  shield on `mount_Hand_L` (`WhaleEquipment.cs:416-445`, `:1645`, `:1677`). The page's main slot (อาวุธหลัก) holds the
  code's first piece, the lance (item_map order), but TTO's placement table numbers the Whale's slots the shield's way
  ("whale" = mount_Hand_L), so the lance went left. `SWAP_HANDS` (index.html, above `placementOf`) uses the "#2" entry
  for the Whale's main slot and the plain one for its second. The Chameleon (bow first, on the left) matches its table
  and is unchanged. Not deployed yet; the user tests.
- **2026-11-09, ของประดับหลัง -> ประดับ** (user: "rename ของประดับหลัง to ประดับ since some times they comes in a form of
  glasses, so let's use generic word"): the topic name (TOPICS), ถอดทั้งหมด's tooltip, the TTO picker's kind. The menu's
  เปลี่ยน / ถอด...ออก lines follow (เปลี่ยนประดับ, ถอดประดับออก). The video repo mentions the old label only in
  `plans/wardrobe_trailer_design.md` and two old `.playwright-mcp` dumps, no code.
- **2026-11-09, every drawable Wolf effect, built and cued** (user: "make the effects we can't draw work including TTO
  skills effects" / "every missing effect from Wolf hero"). Groundwork 9184194 (plug-in loader `FX_PART_FILES`, the five
  proven layouts, `wardrobe_fx_mesh.py` hook, cue options scale / kill; `plans/fx_wolf/build_rules.md` = who owns which
  file); seven agents in parallel, one file set each (2c3408b): vortex, emblem, trail, control, mesh (+ wardrobe_fx_mesh.py),
  the TTO reader `pipeline/wardrobe_fx_tto.py` (TTO's bundles via the Bible's aa_catalog, default style, `tto/<prefab>`,
  home only: it reads the video folder's tto_assets), groundhug / arcribbon / groundfollower (TTO's scripts from its
  machine code, the Bible's run_ghidra.bat), shuriken (Unity's ParticleSystem). Inventory: 67 of the Wolf's 69 own
  effects drawable. Then one editor (`plans/fx_wolf/parts_built.md`) cued them: Blood Fang's slashes (rot 270 / 90 / 0),
  the Mirror Blade pane, Dark Edge's vortex, the emblems, Dual Brand's four slashes, Law Bringer's slash, Art Breaker,
  cAttack2, and TTO's three skills (Blade Surge 68 cues: its random line cage is one fixed draw, seed 32, written in the
  entry's why; Resonance Claw; Wind Bound Domain). Build: 48 BB effects, 93 sounds; 18 TTO effects; files check clean.
  Found on the way: imageEmitter's stop() wrote into the shared data (fixed); legacy particles take setEmit.
  - Open (page): a cue at or after a step's end never fires (Wind Bound Domain's pulses at 2.8 / 4.8 / 6.8 s after its
    1.7 s clip; Blade Surge's aura cut set to 2.55 instead of 2.6 for the same reason); hand-bone auras for a buff's
    length (Dark Edge, Holy Sword) and Lunar Eclipse's tint can't be cued; the TrailRenderer and DistortGlass are
    approximations; Crusader / Law Bringer trail colours may be swapped (user to check); vortex speed 80 vs 60 fps
    (`?vortexfps=60`) is the user's pick.
- **2026-11-09, ท่าสกิล play once** (user: "for ท่าสกิล let's not loop unless it's my override"; reverses the morning's
  "ท่าสกิล also should loop indefinitely until further input" by default). A skill move (a sequence tile, or a clip in
  the skill group: `isSkillMove`) plays once and goes back to the idle stance (mode "back"); one the game loops (a
  channel, `LOOPS`) plays its loop for the held time (HOLD_SECS) first. The override: the skill tab's วนซ้ำ toggle
  (`.pk-loop`, localStorage `wardrobe.skillLoop`), the old endless loop; switching it replays the skill playing now.
  Emotes and base moves unchanged. Going back to idle passes `tail`: no fxClear, no new cues, FX.t runs on, so an effect
  outliving its clip stays and cues after the clip's end fire (Wind Bound Domain's pulses at 2.8 / 4.8 / 6.8 s, a cut
  equal to the clip length); when the last cue has fired and the last effect is gone the cue list empties (the dark
  backdrop goes). `wardrobe_moves_check.py`'s looping expectations for skills are out of date (the user tests by hand).
- **2026-11-09, effect directions: Cross Break / Grand Cross / Resonance Claw** (user: Cross Break "should form a cross
  pattern on the ground briefly before disappearing, however the app vfx direction is all over the place, i suspect
  this issue extends to Grand Cross too"; Resonance Claw "should go 3 directions, but now it only go one direction,
  maybe there's a link"). The link: a velocity in the wrong frame, twice.
  - Legacy particles added `rndVelocity` in world axes. Cross Break = four emitters 1 m out (0.2 m up) turned 0 / 90 /
    180 / -90, each shooting stretched streaks along its local x through the centre, with rndVelocity (3, 0, 0) as big as
    its speed: only along the arm if it turns with the emitter, so the prefab's own design says local (world axes splayed
    the turned arms by up to 45 degrees). Grand Cross's emitters (turned 90 about z) have rndVelocity mostly on local x
    too. Now (localVelocity + rnd) x the emitter's rotation + worldVelocity. (No Unity 3.5 engine source to cite: the
    reading is from the prefabs.)
  - `Fx` moved a root by its EffectControl velocity in the hero's frame only; EffectControl's Awake turns it by the
    spawned rotation (TransformDirection), so the cue's rot must turn it: Resonance Claw's three waves all have velocity
    (0, 0, 36) and differ only by the cue's rot 0 / -45 / +45, so all three flew straight ahead. Now velocity x the root's
    spawn rotation. (fxparts/control.js's child EffectControl already did this.)
- **2026-11-09, ท่าสกิล in the class guide's ring format, with the Bible's upscaled icons** (user: "for Wolf animations
  that might come from various skills, display all their skill icons, i want all skills to use circle frame too like our
  class guide format. Resurrection is Mass Ressurection icon, please borrow upscaled skill icon from the bible too").
  `pipeline/wardrobe_skill_icons.py` copies each skill's highest-rank 128 px icon from the Bible's
  `12t_projects/bible/assets.js` (BIBLE_ASSETS.SKILL_ICONS, `<cls>_<skill><rank>`) to `data/icons/hd/<cls>/<skill>.webp`
  and writes `data/icons/hd/index.json` ({cls: {skill: {icon, clips}}}): a clip belongs to the skill named like it, or
  to CLIP_SKILLS' list (the Wolf: instantCast = Brave Spirit, Second Wind, Lunar Eclipse, Holy Sword; darkEdge = Dark
  Edge, Holy Armor; resurrection = Mass Resurrection; mirrorCounter1-2 = Mirror Blade). 189 icons, the Wolf's 41 skill
  clips all covered (other classes partly: names that differ fall back to the game's icon). Page: skill tiles show every
  skill of their clips in the Bible's cover-ring layout (`RING_SPOTS` = CLASS_GUIDE_COVER_SPOTS; `.rc-ring` =
  `.cg-cover-ring`: gold ring, dark gap, faint ring, glow, blurred copy behind, art at 130 % with a round mask); the
  ท่าทาง ring shows a skill's first Bible icon. Publish: `publish_hd_icons` carries only the skills whose clips are online.
- **2026-11-09, deployed** (user: "when you are done, fell free to commit push and deploy"): `wardrobe_dist` 7,288 files,
  `data-913bb811c8`, check: no problems; the online icons/hd index holds only skills whose clips are online (189, every
  file present). From a fresh empty folder (each deploy leaves a `.wrangler` cache in its folder): 191 uploaded, version
  `2c062f90-9a2d-4a2c-86a2-ad7f9528d815`. **Trap:** a request right after the deploy can get Cloudflare's edge copy of
  the old page (CF-Cache-Status: HIT, the old data folder) although the page is served no-cache; a fresh request (a
  query string) shows the new one. This deploy carries everything since the last: the piece menu's hover = pulsing rim,
  TTO, Space / R, the key-hint centring, zoom 40 x, drop a picture on a piece, the Whale's hands, ประดับ, skills once
  (วนซ้ำ), the skill rings. Online the effects stay off (FX_ON false). Not browser-checked (the user tests).
- **2026-11-09, Space didn't pause mid skill** (user: "why spacebar doesn't work mid skill animations"). After a click on
  a skill tile the tile keeps the focus; the capture-phase keydown that sets `lastInput` (the Ctrl+V target's keyboard
  mode) counted Space as navigation and ran first, so the Space handler saw "keyboard navigation on a button" and let
  Space press the tile: the skill restarted. Now only Tab / arrows count as navigation, and the key-up of a Space taken
  for pause is swallowed too (a focused button is pressed on key-up). Not deployed yet.
- **2026-11-09, the effects online, and the hand-over to the office** (user: "life the restriction on sfx and vfx on
  the public deploy, we have finished Wolf", "deploy when done", "after deployment make sure I can pull from work PC and
  continue working on the wardrobe"). The publish keeps FX_ON and the sound button, copies `fx_cues/` and `fxparts/`
  beside the page (`_headers`: no-cache, their names never change) and each class's `fx.json`, the textures its materials
  and emblems name and its `sfx/` into the data folder (`publish_fx`); 39 publish tests. Built: 7,480 files,
  `data-1669a2addd`; a no-browser check of the copy: all 241 Wolf cues have their effect / voice / sound files, every
  cue key is an online clip. Deployed from a fresh empty folder: 174 uploaded, version
  `00f769bf-f6ad-4766-b829-10800f0307d4`; live: FX_ON true, `fx_cues/wolf.json` / `fxparts/*.js` (text/javascript) /
  the Wolf's fx.json and sounds 200. Space mid-skill fix (06dec0e) went with it. Office: `transfer_to_drive.ps1 -Dest
  C:\Users\Jump\Desktop\12tails-wardrobe-transfer` (362 MB tar, 8,107 files, checked for the effects, sounds, TTO
  textures and icons/hd); HANDOFF "Office PC" has the pull + restore steps.
- **2026-11-10, `wardrobe\data` in git** (user: "can't the data folder push to github private?", then "one repo for
  now"; separate data repo offered for smaller history later). 372 MB, 8,029 files, largest 8.4 MB (GitHub refuses
  over 100 MB). `.gitignore`: `/wardrobe/data*/` then `!/wardrobe/data/` (copies set aside stay out) and
  `/wardrobe/data/bb_rip_fix/` (the office's rip repair); `.gitattributes`: `wardrobe/data/** -text` (no CRLF on
  checkout: core.autocrlf is true here, and the publish hashes the data's bytes); `test_repo_rules` checks both.
  History grows with every data rebuild: if the repo gets heavy, split the data into its own repo then. The office's
  first pull needs its untracked data moved aside (HANDOFF "Office PC").
- **2026-11-10, the office's first pull with the data in git**: a plain `git pull` (b98e03e..1bb66aa) went through with
  the office's old `wardrobe\data` still in place, no Move-Item needed: it was ignored before the pull, and git
  overwrites ignored files without asking. `git status` clean; 8,029 tracked data files plus the 52 of `bb_rip_fix`
  (still there, still ignored); `wardrobe_fx_check.py --cls wolf --files-only`: no problems.
- **2026-11-10, the Wolf's emote and basic-move voices; the server closes with the page** (user: "there's no sfx / vfx
  if any, for other emotes other than the skill animations, Wolf first"; "closing the Wardrobe viewport browser closes
  the server instance together with it too"). What the game does: `RPC_emotion` (Wolf.cs :39385) only plays a voice,
  at 0 before the clip: `emo_<name>` = `Voices/<name>` (:39636), `emo_chat` = chat1-5 at random (:39628). No effect,
  no Sounds/ (the `doEmoticon` bubbles in CharacterControl are statuses: tent zzz, panic, heart; not the emotes). The
  rip has voices for hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5; none for sit, dance, talk, pose*,
  clap, wai, cooking, mining, planting, fishingWolf (silent in the game too). Shared clips: wave (emo_hi, emo_wave) =
  `hi|wave`, bow (emo_ty, emo_bow) = `ty|bow`, talk (emo_chat; emo_talk is silent) = chat1-5, battle (emo_battle; the
  fight stance silent) = battle, ko = `ko1|ko2|dead1|dead2` (RPC_ko :45604-45695 and RPC_dead :45975-46006 share the
  clip). getUp, walk, run, falling, root: nothing. Cues in `fx_cues/wolf.json` (10 entries), the 19 `v_*.mp3` built
  by `wardrobe_fx.py wolf`; its rebuilt `fx.json` differed only in four `mMeshFilter` path IDs (the office's game data
  numbers its assets differently), so the home build's fx.json was kept (`git checkout`). Page: an emote or basic move
  replayed (mode "again") says its line once per pick (`C.seq.round`; cry's 0.8 s clip said it on every replay);
  skills unchanged. `wardrobe_fx_check.py` opens the clip's own picker tab (อีโมต / ท่าพื้นฐาน keys failed as "no
  ท่าสกิล tile"); dark check exit 0, no errors. Server: `pipeline/wardrobe_serve.py` (ThreadingHTTPServer, queue 128);
  the page and tto_picker.html hold `/__alive` (an EventSource, only when `location.port === "8771"`, so the checks'
  servers and the public copy never ask); 10 s after the last one closes it exits (measured: survives a reload, gone
  15 s after the tab closed). Caveat: a browser that discards idle tabs (Chrome's Memory Saver) drops the stream too:
  run `wardrobe.cmd` again. Online: the emote voices go with the next publish (from home).
- **2026-11-10, the office publishes in full** (user: "I thought we have made it so that both PCs can deploy"; "shouldn't
  the 4 Monkey items be in the data you pulled?"). They were in the data; the publish dropped them because it proves
  each item is BB's against a rip, and the office's BB prefabs are zero-filled, so it compares with Reborn's copy, which
  a later Unity (2021.3) wrote in a newer layout: meshes with streams 1-2 (UVs, bone weights) and clips whose keys open
  with `- serializedVersion: 3` (time on the next line). `read_mesh_shape` now reads several streams (stream 0's stride
  from its channels, Unity 2019+ VertexFormat sizes, each stream 16-byte aligned; the sizes must add up to the data, or
  it refuses); `read_clip` reads both key forms. legendTrinket, legendTrinketR, partyWhistle, poseidonTrinket now
  equal Reborn's mesh and clip: office build 7,499 files (= home's 7,480 deployed + the 19 Wolf voices),
  `data-d24944ba10`, check no problems, `wardrobe_dist_check.py` errors []. Two tests (multi-stream mesh, new key
  form); 52 tests pass. Deploy waits for `npx wrangler login` on this PC (not logged in).
- **2026-11-10, deployed from the office** (user: "commit push and deploy"). Wrangler login: a `wrangler login` run by
  Claude timed out (the browser's callback can't reach the sandboxed listener); the user ran it in VS Code's terminal,
  and the token (`%APPDATA%\xdg.config\.wrangler\config\default.toml`) works for Claude's deploys after that. From a
  fresh empty folder: 30 uploaded, 7,468 already there, version `56977780-5fe4-4940-a76d-de27b148ecd3`. Live:
  `data-d24944ba10`, the Wolf's `v_cry` / `v_hi` 200, `fx_cues/wolf.json` with the emote cues, Monkey's legendTrinket /
  legendTrinketR / partyWhistle / poseidonTrinket in props_trinkets.json. Either PC can now publish and deploy.
- **2026-11-10, SFX / VFX toggles** (user: "make toggle SFX and VFX, SFX replacing the current audio icon"; style A of
  four mocked, "SFX/VFX style A is the best"). Toolbar: text buttons SFX (was the speaker icon, `#sound`) and VFX
  (`#vfx`), gold when on, grey + struck through when off (`.tb.fxt`), each remembered (`wardrobe.sound`,
  `wardrobe.vfx`); Thai tooltips / toasts เสียงประกอบ, เอฟเฟกต์. VFX off clears the live effects and spawns none, but
  an effect's own play-on-awake sounds still play (`fxSounds`; Cross Break with VFX off: voice + crossBreak sound, no
  effect). The wider bar ran under the Bible logo on phones (at 360 px it covered ย้อนกลับ): at <= 400 px the gold
  บันทึกภาพ keeps its camera alone (gaps 19 / 24 / 7 px at 430 / 390 / 360).
- **2026-11-10, TTO guarded against casual copying** (user: "analyze whether it is hard to rip undownloadable assets
  (TTO stuff) from my public deploys"; then "Go with your recc, I just want to stop casual copying, those who can
  reverse engineer the page can already get the files they need from the offline game copy"). Found: the TTO lock only
  hid buttons; every TTO texture was a plain public URL at full size, and `window.wardrobe.debug()` handed out the scene
  (with GLTFExporter on the page: a .glb in a few console lines). Now: (1) the publish writes `if (navigator.webdriver)
  window.wardrobe = {`, so only automation (Playwright: the checks) gets the hook; a visitor's browser has none (checked
  with webdriver forced false: `typeof window.wardrobe` undefined, no errors). (2) `scramble()` in wardrobe_publish.py:
  "TTOx" + bytes XOR a repeating key, for a released TTO item's own files: outfit `.bin` + colour textures, prop
  textures (local copies), TTO faces; icons stay plain (tiles show them). The page's `dataBytes()` undoes any file with
  the mark (SCR_MARK / SCR_KEY = SCRAMBLE_MARK / SCRAMBLE_KEY, a test holds them equal); `loadImage` now goes through it
  for data pictures (object URLs, `BLOBS` for `<img>` tiles), `loadTex` replaces TextureLoader for prop textures, the
  two `o_<name>.bin` fetches use it; TTO faces are decoded before their tiles draw (TTO_LOCK only). Tile right-click
  already opens the piece menu, so the browser's "save image" never shows there. Left plain: prop meshes (inline in
  props JSON), clips, effects, icons. Build: 7,499 files, +3.9 KB; Halloween outfit / sword / hat render from the
  scrambled files, 43 / 43 face tiles; dist check and fx check errors []. Tests: scramble round trip + key match, the
  released-TTO test checks the scrambled files. The trailer is retired (user: "the trailer video is already published,
  you may delete everything related to it"): CLAUDE.md / NOTES no longer promise it `wardrobe_dist` or the hook; its
  files in the video repo: HANDOFF.
- **2026-11-10, deployed** (user: "deploy"): SFX / VFX, the TTO guard, the phone toolbar. From a fresh empty folder:
  234 uploaded (the scrambled TTO files and the page), 7,264 already there, version
  `3d998061-2f7e-4fe2-8c79-393accb8b06e`. Live: `data-086254db3e`, the gated hook, `#vfx`; wolf/o_halloween.bin,
  tex/halloween1.webp, faces/23.webp start with "TTOx", BB's standard1.webp is plain RIFF; the previous data folders
  (data-d24944ba10, data-5b9c3cebb9) 404, so no plain TTO copy is left at an old address.
- **2026-11-10, TTO bundles at the office** (user: "TTO skill effects build is here in work PC too no? If not you can
  just rip it like always"). The office has TTO installed (`%LOCALAPPDATA%\TailsTopia\game\TailsTopia\
  TailsTopiaOnline_Data\StreamingAssets\aa`, patch of 2026-11-09: 538 bundles, 1.7 GB). Decrypted all with the Bible's
  `DecompiledSource_TTO_2026-11-02\tools\bundle_decrypt.js` (key fingerprint unchanged) into `tto_assets\2026-11-09\dec`
  + `catalog.bin` in this repo (top-level, so git-ignored by the whitelist; never in the video folder).
  `wardrobe_fx_tto.py`'s ASSETS: the video folder's 2026-11-04 if present, else the newest `tto_assets\<date>` here.
  Probe of the Wolf's 18 TTO effects from it: all identical to the home build. After a TTO patch: decrypt into a new date.
- **2026-11-10, the Sheep's effects: research done** (user: "now's let use workflows to complete Sheep class next!").
  Workflow 1 (9 agents, 31 min): six read-only researchers wrote `plans/fx_sheep/{attacks_emotes,own_skills,cast_a,
  cast_b,tto,parts}.md`, three checkers re-traced ~424 claims and corrected 15 in place (each report's "Verification"
  section). cast3 is shared by 23 Sheep skills (one pool); the Normal Attack's stages run at 0.7 / 1.5 s (SEQ had 0.8 /
  1.8); BB asks for voices that don't exist (All Cleanse, Seal of Defense; the charge release always cAttack1): TTO
  fixed them (Bible findings to offer). The user took all 20 recommendations: `plans/fx_sheep/decisions.md`, and set
  the rule that missing parts are always built (memory + plans/fx_recipe.md). Workflow 2 (build) started: AlphaTimer +
  Phoenix material, the Sheep's projectiles / Eden, page + pipeline changes, the TTO side; one editor; one QA pass.
- **2026-11-10, the Sheep's effects: built and cued** (workflow 2: four builders, then one editor). Parts:
  `fxparts/alphatimer.js` (AlphaTimer), the FX/Phoenix material and `fxAnim.play(name, fade)` in `mesh.js`,
  `fxparts/sheep.js` (the three projectile movers, Sheep_edenSanctuary, and two "fx:<effect>" hooks: the held charge
  ball's growth, Sheep.cs:18952-18957, ATK 101 taken; Holy Light's ring root clip at 0.5 s, :27700), `fxparts/tto_sheep.js`
  (TTO's three Sheep shaders, Standard, LineRenderer, TrailRendererModern, RabbitTracer, BreathFly, CodexOpen); shuriken
  reads the simulation space the right way round now (the Wolf's 12 TTO systems simulate in world space: re-check its
  TTO skills). index.html: `FX_PART_FILES` += alphatimer, sheep, tto_sheep; `api.shader` / FXSHADERS; a part named
  `fx:<effect>` = the hero's code on that effect; the legacy emitter's `addSize` / `setSize`; cue options `to` and
  `bone` (Soul of Arms' trail on mount_Hand_R), a roll `"!name"` (plays when that roll failed: the KO tiles); a
  followState cut plays the effect's `destroy` clip (EffectControl.cs:252-291, castRing's shrink); a step's cues it
  never reached fire when the step ends (a long frame dropped cast1's castRing in the check); looping AudioSources play
  until their effect goes; VFX off runs effects hidden; cue keys `@<sequence id>:<clip>`; SEQ `!` = a cut first step;
  Normal Attack 0.7 / 1.5 s; tiles Soul of Arms, Seal of Attack, Seal of Defense (two skills, decision 18; each a pool
  of the three fields its seal can complete), Eden Sanctuary, Gleaming Breath, Lucent Barrier. `wardrobe/fx_cues/
  sheep.json`: 34 keys, the Cast tile's cast3 pool of 21 skills (decisions 1-20: self-casts with their status looks,
  Divinity Sword / Spear / Axe and Revive at 10 m, the balls ending on the floor at 10 m with their ground hits,
  Return Cast `roll returnCast`, TTO's voice fixes). Wolf: `ko` shows deadEffect on half the plays with RPC_dead's
  voices (`!dead` = RPC_ko's), `wardrobe/data/wolf/fx.json` gained only deadEffect + material wolf_dead (written back
  in its committed indent-1 CRLF form). Data built at the office: `wardrobe_fx.py sheep` (47 BB effects, 117 sounds),
  then `wardrobe_fx_tto.py sheep` (24 TTO effects): 71 effects, nothing missing. Checks: files-only and the dark
  browser check exit 0, errors []; the Wolf's dark check too; unit tests OK. Not yet looked at by the user.
- **2026-11-10, the Sheep's effects: QA pass** (workflow 2's last step). Checks: `wardrobe_fx_check.py ... checks/
  fx_sheep_qa dark --cls sheep` and `... checks/fx_wolf_qa dark --cls wolf` exit 0, errors [] (both run again after the
  fixes); `--files-only` no problems (sheep, wolf); `wardrobe_moves_check.py` errors [] (after the fix below);
  `wardrobe_menu_check.py` errors []; unit tests 52 OK; `test_adopt_from_video.ps1` fails 0. The check's screenshots
  miss most of the 10 m effects (the default camera faces the hero, so "ahead" is behind it) and come late under
  swiftshader: `pipeline/wardrobe_fx_probe.py` (camera views side / back / book..., per-effect world boxes, a pool forced
  to one skill, props worn) and `pipeline/wardrobe_fx_trace.py` (per-frame age / position / vertices / opacity) are the tools for that;
  the "back" view (behind the hero, looking ahead) shows the 10 m point. Fixed: (1) World Encarta's status look drew
  nothing: the prefab is an Animation and eight empty nodes, the status code hangs eight copies of the caster's mWep1
  on them (CharacterControl.cs:39912-39975): `fxparts/sheep.js` `fx:worldEncarta` copies the worn อาวุธหลัก (none worn:
  nothing, as the game); (2) `wardrobe_moves_check.py` still clicked the retired `soulOfArms` tile (now `@SoulofArms`,
  plus `@SealofAttack` for the `!` cut); (3) with VFX off the hidden effects kept the dark backdrop up for their whole
  life (13 s for Eden): `fx-on` now needs VFX on; (4) HANDOFF: the office-built data travels in git (it is tracked),
  not by Drive. Open: decision 1 lists Soul of Arms as ally-targeted, but its hits damage the target (Bible
  sheep-skill-reference.md:444, `hit(370 + sLv, target, ...)`): the arms may belong at the 10 m point (decision 2's
  rule) - asked the user. The Sheep's `fx.json` online carries TTO's Grand Codex book mesh (13,046 vertices) as plain
  JSON (the Wolf's TTO effects had no models): a policy question for the user, since TTO models are otherwise scrambled.
- **2026-11-10, after the Sheep build: free camera, background toggle, TTO effects scrambled, Soul of Arms at 10 m**
  (user: "unlock ASWD 100% free movement"; "remove the black screen dim too" -> "just make it a manual toggle for
  background color deafult to white"; "deploy automatically after all work is done"). Camera: `clampTarget` (the
  look-at point held in a box around the hero, WASD and right-drag pan alike) and `scClamp` (the viewer's, around the
  piece) are gone with their `fitBox` state; WASD / pan go anywhere, the reset button comes back (checked: D then W
  carried the target from (0, 0.77, 0) to (5.0, 4.1, 0)). Background: the พื้นหลัง button (`#bg`, half-filled circle,
  next to VFX) = white by default, dark (#211c27 -> #2d2634) when pressed, remembered (`wardrobe.bg`); the automatic
  dark backdrop while effects played (`fx-on`, FXBG) is gone; on the dark stage only the nameplate turns light (the
  WASD hint keeps its pale chip); `?fxbg=dark` still starts dark (unsaved) for the headless checks / probes. Phones:
  the bar's buttons go 36 -> 32 px wide under 760 px (gaps to the logo 5 / 22 / 30 px at 360 / 390 / 430). TTO: the
  publish now also scrambles `tto_*` effect textures and any `<cls>/fx.json` with tto/ effects (the Sheep's holds the
  Grand Codex book, a 13,046-vertex model); the page reads fx.json through `dataBytes` and every effect texture through
  `texLoader = { load: loadTex }` (also the parts' api.texLoader). Soul of Arms: decision 1 had listed it as an ally
  buff, but the arms hit the target (Sheep.cs:34100-34118, QA), so its cue is at the 10 m point (decision 2). Checks
  (one at a time): unit tests OK, files no problems (sheep, wolf), fx check sheep / wolf dark exit 0 errors [], moves
  check errors [], menu check errors [], adopt test fails 0.
- **2026-11-10, deployed: the Sheep** (user: "deploy automatically after all work is done"). The first publish stopped
  on its own guard ("'no-cache' is still in the published page": the new fx.json read); the publish now strips it like
  getJSON's ("no-cache effects" edit, in the test page too). Build: 7,685 files (+186), 331.7 MB (+5.4 MB);
  sheep/fx.json, wolf/fx.json and tto_* textures scrambled ("TTOx"), BB's wolf_dead.webp plain; check no problems;
  `wardrobe_dist_check.py` errors []. Deployed from a fresh empty folder: version
  `c58df635-d5d5-47a0-be6f-9e3b36481bf2`, live `data-f8b8ebe61a`, the bg / vfx buttons, fxparts alphatimer / sheep /
  tto_sheep and fx_cues/sheep.json 200, the old data folder 404.
- **2026-11-10, the Penguin's research stopped at 98 % of the weekly limit** (user: "use workflows to do the next
  class, Penguin"; the usage guard, CLAUDE.md, stopped it). Workflow `penguin-fx-research` (six researchers, then three
  checkers; same prompts as the Sheep's, with the Sheep / Wolf decisions applied by analogy and only new questions
  raised): **finished**: own_skills (`plans/fx_penguin/own_skills.md`, not yet verified); **written but its agent never
  returned**: tto (`plans/fx_penguin/tto.md`, maybe incomplete, not verified); **not started writing**: attacks_emotes,
  cast_a, cast_b, parts; no checker ran. The workflow's script is in this session's folder only; HANDOFF has the
  continuation (re-run the four, check tto.md, then the three checkers).
- **2026-11-10 (17:08-17:43), the Penguin's research finished** (user: "continue your penguin research ... the handoff
  commit push to home PC is done before 18.00"). The stopped workflow resumed in the same session (own_skills from
  cache), 35 min: all six reports in `plans/fx_penguin/` written and checked (374 claims re-traced, each report's
  "Verification" section). The researchers raised 17 new questions (beyond the Sheep / Wolf decisions), each with a
  recommended default, in the reports' question sections: Double Spell reruns, Nova Flare at the vortex 5 m ahead,
  Constellation's star count, Emperor's March stopping, Frost Field's leap, long statuses cut at 10 s, the Normal
  Attack's aim point (a 0.35 m ball radius the Sheep's cues ignored too), Tornado / Typhoon as two pool members, Cosmic
  Rift / Friday's hero-skin look, Snow Man hiding the hero, the Staff of Time's slow ball. Next: the user answers them
  (or takes the defaults), then the build workflow (HANDOFF).
- **2026-11-10 (evening, home PC), pulled and checked** (user: "git pull and continue Penguin work"): 1bb66aa..47ead9a.
  The office-built Sheep data came with the pull (`wardrobe_fx_check.py ... --cls sheep --files-only`: no problems);
  the usage guard runs here without a prompt (`--once`: weekly 2.0 %). The Penguin's 17 questions plus the checkers' two
  conventions (missile aim: floor at 10 m or the target 0.6 m up; effects drawn with the target's rotation: the hero's
  facing or `rot [0, 180, 0]`) put to the user; attacks_emotes Q3 and parts Q1 give opposite defaults for the Staff of
  Time (no / yes).
- **2026-11-10 (evening, home), the Penguin's decisions; the build workflow started** (user: "go with your recc"): all 20
  in `plans/fx_penguin/decisions.md`. Two of them are new rules for every class: homing missiles aim at the target
  0.6 m up, and effects drawn with the target's rotation use `rot [0, 180, 0]` (the target faces the hero). Workflow
  `penguin-fx-build` (`pipeline/workflows/penguin-fx-build.js`, run wf_c0c24a49-de0): builders shaders (mesh.js),
  penguin (`fxparts/penguin.js`), page_pipeline, tto (`fxparts/tto_penguin.js`, shuriken.js's Trail module, the TTO
  skinned mesh + cel shader), then one editor (`fx_cues/penguin.json`, the data build), then QA over Penguin, Sheep and
  Wolf. Usage guard on (`usage_watch.py 98 60`).
- **2026-11-10 (evening, home), the Penguin's effects: built and cued** (workflow `penguin-fx-build`: four builders, then
  one editor; user: "go with your recc"). Builders: **shaders** (`fxparts/mesh.js`: Transparent/AdditiveSaturate as two
  passes, Opaque1 / Opaque2 lit at their real alpha, DiffuseAmbient with its `ambient`, `fxAnim.play(name, fade, wrap)`;
  node probe `checks/fx_penguin_build/shaders/probe.mjs`, its 1.27 MB `three160.js` copy stays in the ignored checks/);
  **penguin** (`fxparts/penguin.js`: Penguin_tornado / _typhoon / _arcticEmperor / _cosmicFriday / _iceBlock / _nAttack
  (+ the Staff of Time mine) / _manaMissile (aimed 0.6 m up) / _snowMan); **page_pipeline** (`wardrobe_fx.py` Penguin
  LAYOUTS, built-ins 206 = multiply2 and 207 = premul (every class's `<cls>_dead`: the Wolf's and Sheep's KO stay additive
  until their data is rebuilt), EXTRA_FOLDERS for novaFlare and the Mana Vortex summon, BoltEmitter / ManaVortex; page:
  SEQ Normal Attack 0.5 / 0.5, Charge Attack cAttack1@0.7, Cosmic Friday cast3@0.4, the MP Transfer tile, the "skin" cue
  kind + HERO_SKINS FX/CosmicRift, api.heroHide / api.worn, Sound handle setVolume, Fx.dispose -> e.dispose?.(), cue
  scale [x, y, z], spread, every option passed to fx.at); **tto** (`fxparts/tto_penguin.js` StarLines / EmperorShot /
  FlockRise + the cel shader, shuriken.js's TrailModule, TTO SkinnedMeshRenderer export, Unity's built-in Quad, TTO's own
  sounds). Editor: the snowman now hides the hero through `api.heroHide` (one hiding mechanism, by layers; was its own
  visible = false walk) and a cue's `hideHero: false` leaves her shown (Snow Ball's leftover snowman: decision 17 is
  Snow Man's own, she would blink out for 0.4 s); new cue option `notWorn: [slot, item]` (index.html fxStart: the Normal
  Attack's ground hits left out while the Staff of Time is in the main hand, decision 18); the check's OPTS += n,
  hideHero, notWorn. `wardrobe/fx_cues/penguin.json`: 27 keys, the Cast tile's cast3 pool of 16 (Tornado and Typhoon two
  members), assembled from the reports' paste-ready blocks by `checks/fx_penguin_build/editor/cues_build.py` (ignored
  folder, re-runnable) with the decisions applied: missiles at the target 0.6 m up (new rots; the middle three hit it at
  1.12 s, yaw +-48 / +-72 pass it to the floor at 15.8 / 19.1 m), manaSurge rot [0, 180, 0], Typhoon's random swerve and no
  cut, Cosmic Rift / Friday skin cues (kill 12 / 7), Ice Shield / Mana Vortex kill 10, Nova Flare 5 m, five Constellation
  stars, Emperor's March's full run, Frost Field in place, no activateIcon1 entry. Data: `wardrobe_fx.py penguin` (46
  effects, 61 materials, 58 textures, 110 sounds; "missing" only TTO's own emperorPenguin_flock / _whistle, written by the
  TTO build), then `wardrobe_fx_tto.py penguin` (28 TTO effects): 74 effects, every cued effect and sound present; the
  Wolf's and Sheep's data untouched. Playwright: uv now resolves a version wanting chromium_headless_shell-1254, installed
  with `uv run --no-project --with playwright playwright install chromium`. Checks: files-only no problems; dark check
  exit 0, errors []; unit tests 52 OK. Probes (`wardrobe_fx_probe.py`, `checks/fx_penguin_build/editor/probe*`): Mana
  Missile, Tornado (glide ahead), Typhoon (homing on 10 m), Snow Man (snowman at 10 m, hero hidden), Snow Ball (hero
  shown), Cosmic Friday's skin, the Arctic Emperor statue, Falling Stars / Nova Flare all draw as intended. The dark
  check's cast4 samples were empty once (a pool tile has no expected effect, so it settles early; the first sample after a
  click lands about 1.7 s in under swiftshader); `checks/fx_penguin_build/editor/repro.py` replays its click order and
  both members spawn. Open: decision 17 differs from the game (BB hides the snowmanned target, never the caster;
  penguin.js HIDE_ONLY_ON_HERO switches to the game's rule); not yet looked at by the user; the QA pass is next.

- **2026-11-10 (evening, home), the Penguin's effects: QA pass** (workflow `penguin-fx-build`'s last step; cut off that
  night, **finished 2026-11-13** by the overnight run's `penguin-fx-finish` QA step, below). New tool `pipeline/wardrobe_fx_shots.py`: the probe's views, boxes and forced pools,
  but on a virtual clock (the page's one THREE.Clock replaced by a fixed 1/30 s step), so every shot is at exactly the clip
  time asked however slowly swiftshader draws (the probe's real-time samples landed up to 10 s late on the Arctic
  Emperor); forced rolls (`ko!dead`, `cast3!doubleSpell`, several joined by `+`), `BG=white` for the white stage, the hero's
  drawn / hidden meshes per sample, and a stalled render loop reported with the page error's stack. Found and fixed:
  (1) **Arctic Wind froze the whole page**: deadlyFrost's legacy particleEmitter has no material (`mats [null]`), the page
  built a mesh with a null material and three's renderer threw every frame, which stops `setAnimationLoop` for good (1 Cast
  play in 16; the dark check plays one random pool member, so it never met it): `legacyParticles` builds no mesh without a
  material, and `fxMesh` hides any null-material mesh; (2) **the KO ghost (premul, built-in 207) drew as a dim dark-teal
  smudge on the dark stage**: the canvas read back (0, 84, 101) over alpha 29, colour above alpha, which the browser's
  premultiplied compositing clamps to the alpha; the premul shader now writes alpha >= its brightest channel (the 'add'
  convention): dark stage (23, 105, 128) vs the game's (33, 111, 139).
  **Finished 2026-11-13 (overnight, home)**, after the one-tile-per-skill pages and the five effect-only tiles:
  - Tools: `wardrobe_fx_shots.py` gained `--jobs <jobs.json>` (many tiles in one browser, a fresh context per job: the page
    keeps the worn look in localStorage, so a reload carried the Staff of Time into every later tile), several views per
    sample (`back,side`), a `behind` camera (behind and above: the 10 m target and +-10 m around it), `SEED=<n>`
    (Math.random seeded), `PARTS=1` (each drawn part of the live effects: node, material, vertices, box, indices behind
    the camera / off screen / NaN) and `HIDE=<regex>` (hide parts before the shot); its emote tab was looked up as
    "emotion" (the picker's is `emote`: emote tiles were never found; also fixed in `wardrobe_fx_probe.py`). New
    `pipeline/wardrobe_fx_sheet.py`: contact sheets (one row per tile / forced roll / backdrop, `index.html`).
  - Shot (virtual clock): 44 jobs on the dark and the white stage (161 samples each) plus 13 `behind` views: Normal
    Attack (as rolled, Spread Shot forced on all three stages, the Staff of Time worn), Charge Attack, MP Transfer, all 16
    cast3 tiles (Double Spell forced on Mana Missile, Mana Burn, Frozen Blast, Arctic Wind, Ice Block, Falling Comets),
    Cosmic Friday, Blink (+ Double Spell), Parallel Shift, Falling Stars (+ Double Spell), Nova Flare, Arctic Emperor,
    Focus Intellect, Constellation, Frost Field, Emperor's March, Mana Arc, Dispell, Double Cast, Triple Cast, Frost
    Spike, KO (dead forced and as rolled), wave / talk. Sheets: `checks/fx_penguin_qa/sheets_dark`, `sheets_white`,
    `sheets_behind` (git-ignored; the shots under `run/`, logs `run/*.log`).
  - Everything lands as the reports and decisions.md say (boxes in the hero's frame; tile time = clip time + 0.7 s on the
    cast3 tiles): the Normal Attack balls end at the 10 m point at 0.98 / 1.48 / 1.98 s, Spread Shot's side hits at
    x +-2.85; the three middle missiles hit (0, 0.62, 9.7) at 1.82 s, the outer pairs pass to the floor at 15.8 / 19.1 m;
    manaSurge, Meteora's ring and blast, Frozen Break, Blizzard, Absolute Zero, Snow Man / Snow Ball at 10 m; Mana Vortex
    and Nova Flare at 5 m; the comets in +-10 m around 10 m; Constellation's pentagon 10-15.4 m and the giant star at 13 m;
    Emperor's March's frost line to the Goal at 22.45 m at 1.636 s; Frost Field at the hero; the effect-only tiles at the
    hero (Mana Arc's cage 0.5 m up, turned anew each play). Endings: Ice Shield, Mana Vortex and Snow Man at 11.1 s (kill
    10), Ice Block 13.1, Tornado / Typhoon 7.5, Focus Intellect 6.8, Cosmic Rift's skin 13.3, Cosmic Friday 8.1; the hero
    is hidden for the snowman and shown again at its end, and a new pick mid-effect (after Snow Man, Cosmic Rift, Cosmic
    Friday, Ice Shield) shows her again, drops the skin copies and the effects. Staff of Time: the balls hover (0.01 m/s)
    and the ground hits stay out. No page error and no stalled render loop in any job.
  - **No new bug found** in the page, the cues or the data (the two fixes of 2026-11-10 hold). Looked into, not bugs:
    Nova Flare's hard-edged "square" wedges at 0.5-0.8 s are its RingEmitters running from a negative radius (-3..-6 to
    5..6 m) with a height: mid-life a ring is a cone, whose straight silhouettes read as a square; RingEmitter.cs lerps
    the radius the same way, no clamp (:419-424), and fresh GPU buffers draw the same frame identically (the kept-buffer
    setMesh is not involved). snowMan's first-frame box reaching 50 m up / 64 m out: its ParticleEmitter child sits at
    (0, 50.2, -64) in the prefab (a one-shot puff out of sight), as in the game. castRing's age 60.x after its cut = the
    cut jumping to its life's end for the afterLife.
  - Gates: `wardrobe_fx_check.py ... dark --cls penguin` exit 0, errors [] (all tiles); unit tests 65 OK, node 8 pass,
    `test_adopt_from_video.ps1` fails 0; `wardrobe_weapon_fx_check.py` OK (needs `--with pillow`, as its docstring says).
    No page or fxparts code changed, so the Sheep / Wolf runs were not needed.
  - For the user's eye: on the white stage the white parts (the snowman, Meteora's smoke, Ice Shield's and Frost Field's
    crystals) melt into the backdrop and the additive glows are faint (the game has no white backdrop; the dark stage is
    the reference); Nova Flare's cone wedges (above, faithful but odd-looking); decision 17 (the game hides the
    snowmanned target, never the caster); effect_only.md's open points 1-4 (Mana Arc's random cage, the multiCast tint on
    Double / Triple Cast, Frost Spike with or without the shield, Dispell's screen warp).
- **2026-11-10 (19:40, home), the usage guard was blind** (user: "is the work flowing?"): the workflow was (the four
  builders and the editor done, QA running), but every one of the guard's 42 checks since 18:08 got HTTP 429 from the
  usage endpoint (`Retry-After: 0`; `--once` worked just before). `usage_watch.py` now checks every 5 min by default,
  doubles the wait after a failure (up to 15 min), prints each success with the time, and prints `BLIND` after 30 min
  without one; CLAUDE.md's command is `98 300`. Restarted.
- **2026-11-10 (night, home), the TTO skills' lag fixed: effect meshes kept their GPU buffers** (user: "please fix TTO
  skills lag ... something might be unoptimized? common issues ... redrawing everything again every frame"). Cause:
  `setMesh` (index.html, called every frame by every emitter: shuriken.js's systems, the legacy particles, groundhug,
  trail, vortex, the TTO line renderers) made new BufferAttributes each frame, so three created a new WebGL buffer per
  attribute per mesh per frame (189-322 a frame on a TTO skill) and never deleted the replaced ones (only the last set,
  at the effect's dispose): a GPU memory leak that made every play in the same page slower. Now each mesh keeps one set
  of DynamicDraw buffers written in place (counts = the frame's, only that range uploaded), grown x2 when a frame needs
  more (the old buffers freed by geometry.dispose); Shuriken's mesh particles pass their normals through it (they added
  a new normal buffer each frame too). New tool `pipeline/wardrobe_fx_perf.py` (virtual clock or `--real`, `--gpu` =
  this PC's RTX 4070 SUPER through ANGLE D3D11, `--baseline` = the page served with the old setMesh, `--profile`).
  Real time on the GPU, the repeat play, before -> after: Wolf Blade Surge 54 fps with 26 stalls over 50 ms (worst
  614 ms) -> 2,128 fps, none; Wind Bound Domain 46 fps / 41 stalls -> 773 fps / 0; Resonance Claw 176 / 27 -> 1,570 / 0;
  Sheep Grand Codex 186 / 5 -> 509 / 0; Penguin Emperor's March 385 / 13 -> 597 / 0; Constellation 222 -> 396; Frost
  Field 49 / 30 -> 132 / 2. GL buffers created in a 5 s play: 30,000-112,000 -> 84-1,300. What is left heaviest: the
  mesh particles (Frost Field's rings, Emperor's March's goal spikes: 3,000-8,000 vertices a system rebuilt in JS each
  frame, renderMesh); GPU instancing would cut that, but every TTO shader would need the instancing chunks.
  Sequence tiles are `@<Name>` in the perf tool (`@GleamingBreath`).
- **2026-11-10 (night, home), skills without an animation, and the pooled tiles** (user: "there's much less skills than
  I thought, like where is the simple mana arc? ... so you didn't do the vfx too?"). Two causes. (1) Tiles follow clips,
  and most skills share one: the Penguin's Cast tile (cast3) is a pool of 16 skills picked at random per play, cast4
  holds Falling Stars / Nova Flare, blink Blink / Parallel Shift; their effects were built, hidden behind three tiles.
  (2) The research listed skills by their clips (clip_calls.js), so skills whose RPC plays no clip were never looked at:
  Penguin Mana Arc (`$RPC_manaArc$26093`, Penguin.cs:21578: no animation call, `manaArc` / `penguinOfArc` effect at the
  hero + 0.5 m up, a self AoE), Dispell, Frost Spike (Ice Shield's). Found by listing every `RPC_*` in Penguin.cs against
  the cues and the reports (the others missing are shared item / pet / mount / coin RPCs). The user: one tile per skill,
  effect-only tiles on the idle stance, "but redo Wolf and Sheep first" (HANDOFF "Either PC").
- **2026-11-10, the Penguin's build committed as is** (QA cut off; checks after the lag fix: fx check dark penguin /
  sheep / wolf exit 0, errors []; unit tests 52 OK).
- **2026-11-10 (night, home), one tile per skill; Quick Heal; Wolf and Sheep first** (user: "Yes to both, but redo Wolf
  and Sheep first"). Page: `chains()` adds `poolChains`: every member of a plain-clip pool in the cue file
  ({skills: {...}}) gets its own sequence tile (`pick` = the member, name from its id: "@IceShield"), with the steps of the
  tile that played the pool (the sequence holding the clip with no cue key of its own for it, "Cast" first; else the clip
  alone); that host is not listed (`hidden`, `C.poolClips`); `fxStart` plays the pick's cues only; the icon is the
  member's own (`moveSkillIcons` via `chainOf(name).skill`). "@<sequence>:<clip>" pools stay random (the Sheep's seal
  fields are one skill's outcomes). chains() is not cached until the cue file has loaded. Wolf: Dark Edge, Holy Armor,
  Brave Spirit, Second Wind, Lunar Eclipse, Holy Sword (were 2 tiles); Sheep: the 21 Cast skills (was 1). Skills with no
  animation, found per class as the class's own RPC_* that call no clip (clip_calls.js), phases (_hit, _fire, _multiCast,
  _move ...) and the shared item / pet / mount RPCs left aside: Wolf none (grandMark = Cross Break's mark, nAttack5 the
  combo's restart, doubleArt the roll, all cued); Sheep Quick Heal (Free Cast is the returnCast roll, cast0 / holyLight0
  / lullaby0 the cancels): SEQ "Quick Heal: root@1" + SEQ_SKILL, cue key "@QuickHeal:root" (voice quickHeal1|2, koHeal
  with KO Heal #422 on, returnCast 24 %; Sheep.cs:10201-10420), built with `wardrobe_fx.py sheep --fx koHeal,quickHeal
  --voices quickHeal1,quickHeal2` (merges). `wardrobe_skill_icons.py`: every pool member (its pool's clip) and
  EFFECT_ONLY skill (root) gets its Bible icon, so the publish keeps them. `wardrobe_fx_check.py` plays each member's
  tile expecting its own cues, and skips the hidden hosts. Checks: files-only sheep / wolf no problems; dark wolf exit 0,
  errors [].
  Then: dark sheep exit 0 errors [] (all 21 Cast skills and Quick Heal played); moves check errors []; menu check errors [] (a first run's failed emote-icon requests did not repeat); unit tests 52 OK. New pipeline/wardrobe_picker_shot.py (screenshots of a class's picker tab).
- **2026-11-10 (night, home), deployed** (user: "1." = everything, the Penguin as it is): the TTO lag fix, one tile per
  skill (Wolf, Sheep, and the Penguin's pools), Quick Heal, the Penguin's effects (QA cut off, its effect-only skills not
  yet in, not hand-checked). Publish: 7,906 files (+426), 337 MB, check no problems; `wardrobe_dist_check.py` errors [];
  penguin / sheep / wolf fx.json and the 41 tto_* textures start with "TTOx". From a fresh empty folder: 230 uploaded,
  7,675 already there, version `9d49453e-6890-4ae7-8783-3c7b64d1f2b5`. Live: `data-f37b6da64e`, poolChains and the
  kept buffers in the page, fxparts penguin / tto_penguin, fx_cues/penguin.json, the Quick Heal icon 200; the old data
  folder 404.
- **2026-11-11, deployed: Devil Wing off, the disclaimer** (user: "remove the Devil Wing from the Wardrobe Online
  version, that piece has not been released yet, then deploy, also red warning text at top left in white area"):
  `devilWing` out of `tto_released.json` (all.trinkets; the publish drops it: "not in the released list"); a red
  `.disclaimer` on the stage's top left "โปรเจกต์ส่วนตัว ไม่มีส่วนเกี่ยวข้องกับเซิร์ฟเวอร์ใด ๆ" (#c62828, #ff8a80 on the dark
  backdrop; follows `--inset` beside the picker; phone: under the logo chip), local and online. Publish 7,905 files (-1),
  check no problems; unit tests 52 OK; `wardrobe_dist_check.py` errors [] (a first run's Halloween tile click didn't wear
  it in time; the rerun passed). From a fresh empty folder: 2 uploaded, version `e5957791-636d-4877-be20-89df43b1c514`,
  live `data-16e5161a08`, the old data folder 404.
- **2026-11-11, the TTO Halloween weapons drawn as the game draws them** (user: "players report holding a pumpkin
  instead of the lantern ... also Bat weapon is too long, abnormal size"). Cause: Unity draws submesh i with material i
  and leaves a submesh with no material undrawn; three TTO prefabs have 2 submeshes and 1 material (the only ones of
  1,590 prop meshes; everywhere else group i = material i): Sheep halloweenLantern (submesh 0 = 36 triangles from the
  texture's orange octagon, top left: the "pumpkin", the same shape as TTO's item icon shp37_0; the 796-triangle
  lantern with its bow is submesh 1, never drawn in the game), Bat halloweenWand (submesh 1 = a 24-triangle purple
  crystal past the spider head, z 0.84-1.14: the wand drew 1.41 long, the game's is 1.27), Rabbit halloweenRifle (a
  48-triangle piece). The extractor wrote such a submesh with material 0, so the page drew it. Fix in the page:
  `propGeometry(m, nMats)` keeps only the first nMats submeshes in the index (the 3D file copies the index, so it
  matches). Checked against the TTO patch of 2026-11-07 (installed here; 106 bundles decrypted into the session's
  scratch): both prefabs unchanged (same meshes, scale 1, same material); WeaponPlacement has no Bat entry (fallback,
  keepPrefabScale, scale 1), so nothing in the game shrinks the wand further; that patch's placements add only Panda
  t_all182 (placements.json left as is). The Sheep's lantern also sits mostly inside her sleeve. New:
  `pipeline/tto_prefab_probe.py` (a TTO prefab's nodes, meshes, textures from decrypted bundles),
  `pipeline/wardrobe_weapon_shot.py` (a class holding each weapon: shots, close-ups, size against the hero).
  Publish: data folder unchanged (data-16e5161a08), page only, check no problems; unit tests 52 OK; dist check errors []
  (again its first run's Halloween click failed, the rerun passed: that check step is timing-flaky).
- **2026-11-11, reverted: the extra submeshes stay drawn** (user: "no, I don't think those are intended, please don't
  lose the extra pieces"). The page is back to drawing every submesh (the full Sheep lantern, the Bat wand's crystal,
  the Rabbit rifle's piece): the user reads the game's single material as TTO's mistake, not the design. The fix's
  deploy, stopped mid-run by the user, had gone live (version from the stopped run); redeployed the reverted page:
  version `8846e8c2-11e8-4004-bc28-73b125da201a`, data folder unchanged (data-16e5161a08), live page without the
  submesh filter. The cause above stays true; don't "fix" it again without asking. The two scripts stay.
- **2026-11-11, community skins: decided** (user: "recommend the best workflow to receive skin textures from audiences
  and upload to the wardrobe website"; "upload = no limit to any pieces"): a Google Form (Thai; the PNG as downloaded
  with ดาวน์โหลดลาย, so its name gives class + item; credit name + optional link; consent) -> files in the user's Drive,
  an อนุมัติ column the user ticks -> an import script validates (name, size = the original's, PNG) and writes webp +
  a creators list into wardrobe/data -> a "ลายจากผู้เล่น" section per piece; publish + deploy as usual. Any piece, TTO
  included: approved skins show on TTO pieces online too; the visitor's own อัปโหลดลาย and every download stay locked
  on TTO pieces (TTO_LOCK unchanged). Credit = name + link (the user checks links when approving).
- **2026-11-11, community skins: Discord instead of the form** (user: "instead of Forms, can we go the cloudflare worker
  route that send stuff to discord?"; then "(b) Allow preview upload", "Discord bot"). The page's piece menu sends the
  visitor's own skin (name, optional link, consent, Turnstile) to `POST /api/submit` on the site's own Worker, which
  checks it and posts it to a private Discord channel through a webhook (secrets in Cloudflare, never in the repo);
  the user reacts ✅; `pipeline/wardrobe_community.py` reads the channel with a bot token kept only on the PCs and
  writes the approved skins into wardrobe/data; publish + deploy. TTO rule loosened by the user: online, a visitor may
  put their own skin on a TTO piece (preview, and to send it); every TTO download (texture, 3D) stays locked.
- **2026-11-11, community skins built** (not deployed: waits for the user's setup, HANDOFF "community skins"). Two
  uploads, kept apart (user: "there's 2 upload pipelines, upload for just local testing and upload that intend to be
  public"): อัปโหลดลายของคุณ stays in the browser as before; ส่งลายนี้ให้ทีมงาน (the piece menu, only when the visitor's own
  skin is on and SUBMIT_KEY is set) opens a dialog (name <= 40, optional https link, consent, Turnstile) and posts that
  one skin. Pieces:
  - `pipeline/site_worker.mjs`: the site's Worker (assets first; it runs only for POST /api/submit): origin check,
    Turnstile siteverify, fields and PNG checks (<= 2 files, 4 MB, 4096 px), a rough per-IP limit in the colo cache,
    then the webhook (`?wait=true`, `allowed_mentions: {parse: []}`, the PNGs + meta.json). 503 without its secrets.
    Tests: `node --test pipeline/test_site_worker.mjs` (stubs); `py -3 -I pipeline/site_worker_check.py` (wrangler dev,
    Cloudflare's test secret, a stand-in webhook).
  - Page: COMMUNITY from data/community.json; a worn community skin is a SKINS entry with `by` (ownSkin / skinBy):
    menu list "ลายจากผู้เล่น" (wear = one undo step; a link button opens the creator's link), the nameplate's "ลายโดย",
    badge ลายผู้เล่น, download names `_ลายโดย<name>`, beforeunload only for own skins. TTO lock: downloads only (upload,
    reset, Ctrl+V allowed on TTO pieces). `SUBMIT_KEY` = ?submitkey= locally (test key 1x00000000000000000000AA), the
    publish writes `wardrobe/community_config.json`'s site key. The disclaimer goes to top 66 px while the desktop
    picker is open (`main.inset`; it ran under the toolbar at 1366 px: live since this morning's deploy).
  - `pipeline/wardrobe_community.py`: the bot reads the channel (webhook messages with a person's ✅), checks each
    skin against the data (the piece, its textures, the original's size, a real PNG, https link), writes
    data/community/<cls|all>/<message id>_<n>.webp (q92) + community.json, mirrored (✅ taken away = gone). Tests:
    `pipeline.test_wardrobe_community`.
  - Publish: `publish_community` keeps a skin when its piece is published, scrambled for a TTO piece; community.json is
    always written. Tests: 3 new in test_wardrobe_publish.
  - Checks: `pipeline/wardrobe_community_check.py` (the browser flow with a stand-in community.json and api/submit);
    `wardrobe_tto_check.py` and `wardrobe_dist_check.py` now expect upload kept on TTO pieces. All green: unit 59 OK,
    node 4/4, community check, worker check, menu check, TTO check, dist check (twice).
- **2026-11-11, community skins reworked** (user: "ลายจากผู้เล่น implementation is bad, it should be an option for
  another pop-up box, user can choose to download it or wear it in the wardrobe"; then "TTO upload should work only on
  private version, there should be no TTO skins from other players to try to begin with since we have to use the 2D
  texture as the thumbnail"). (1) The piece menu has one entry "ลายจากผู้เล่น <n>" opening `Gallery`: a card per skin
  (the 2D texture as its picture, "ลายโดย", the link or ไม่มีลิงก์, ใส่ในห้องแต่งตัว = one undo step and the pop-up closes,
  ดาวน์โหลด = `communityDownload`, PNG `12tails_<class>_<item>[_ลาย<n>]_ลายโดย<name>.png`), Esc / ✕ / the backdrop close;
  buttons stacked (ใส่ในห้องแต่งตัว did not fit beside ดาวน์โหลด). (2) The TTO loosening is undone: online a TTO piece is
  preview only again (no upload, paste, reset, send); `communityOf` ignores a TTO piece; the import refuses one ("is
  TTO's"), the publish drops one (no scrambled copy any more). Checks rewritten on the BB mothLatern + standard outfit;
  `wardrobe.debug()` also hands out Send / Gallery. The check trap: the pop-up reuses `.send-back`, so a selector for the
  send dialog must say `:not(.gal-back)`; Cloudflare's test widget always returns the same dummy token. All green: unit
  59, node 4/4, community check (twice), menu, TTO, dist check (twice), publish no problems.

- **2026-11-12, community skins: setup done** (office, user: "Let's do the one-time setup", then "can you use browser
  access to do it?"). Claude drove the user's Chrome; Claude Code's safety check blocks Claude from creating webhooks,
  bots and other account integrations, so the user clicked those (Create Webhook, Authorize, the bot's channel
  permission, Reset Token + MFA, the intent toggle, Turnstile Create). Discord: private `#wardrobe-submissions`
  (id 1570242267397230764) in the user's server "Jump" (12tails category); webhook "Captain Hook"; app "12 Tails Skins"
  (id 1570241807726547034; Message Content Intent on, flags 524288; View Channels + Read Message History, invite
  permissions=66560). The token went from the clipboard into `%APPDATA%\12tails-wardrobe\discord.json` (never printed);
  a read-only check: the bot sees the channel and reads its history. Turnstile widget "12tails-wardrobe" (Managed,
  hostname 12tails-wardrobe.jumpthai.workers.dev), site key in `wardrobe/community_config.json`. Worker secrets
  TURNSTILE_SECRET and DISCORD_WEBHOOK set by piping the clipboard into `npx wrangler secret put` from an empty scratch
  folder (`wrangler secret list` shows both; the live site still 200). Not deployed yet (HANDOFF).
- **2026-11-12, community skins: deployed and the first live send** (user: "GO"). Deploy 1 (de938b86) also put the
  Penguin's effects online (they came with the pull; their QA is still open, HANDOFF). The first live sends failed
  silently; three bugs, all fixed (deploy d1380e15): (1) the stored DISCORD_WEBHOOK began with a BOM (U+FEFF): Windows
  PowerShell adds one when piping text into a program (`$u | npx wrangler secret put ...`), and `fetch` threw "Invalid
  URL" (wrangler tail showed it). The Worker now trims both secrets (trim() removes U+FEFF); test in
  test_site_worker.mjs. When setting a secret from Windows: Git Bash `printf %s ... |` or type it at wrangler's prompt.
  (2) The page wiped every refusal: after a refused send it resets Turnstile, the real widget re-passes within a second,
  and its callback ran say(""). Now the callback clears only SEND_ERR.wait; wardrobe_community_check.py asserts the
  refusal stays. (3) The import would refuse every skin: Discord takes an embed's picture (skin0.png) out of the
  message's attachments; `files_of` adds the embed image (test in test_wardrobe_community). Also: the Worker's 5-per-10-
  minute limit counts before the Discord post, so failed posts used it up (429 `rate` after five tries). The public page
  exposes wardrobe.debug() only under navigator.webdriver, so in a normal Chrome the send was tested through the UI (a
  PNG pasted with Ctrl+V on the tile) and `pipeline/wardrobe_send_live_probe.py` (headless, reads Send's state). The
  channel holds two test messages: "ทดสอบรูปแบบข้อความ (จากเครื่อง ไม่ผ่านเว็บ)" (the Worker's message format posted
  from the PC with node) and "ทดสอบระบบ" (the real send from the site, a recoloured mothLatern 128x128).
- **2026-11-12, community skins live from Discord** (user: "can you make it so that I can upload player skin data thru
  phone after I approved in discord? that flow is much smoother"). The Worker's `GET /api/community` lists the channel's
  webhook messages with a ✅ (meta.json read once per message, the list cached 60 s per data centre) and
  `/api/community/<id>/<n>.png` serves a skin only while it is approved; no KV, no cron. No data-side re-check: the
  Worker checked each skin when it was sent, and the page skips missing / TTO pieces and draws a skin at the original's
  size (wearCommunity). Page: `LIVE_COMMUNITY` (false locally, the publish sets true) asks api/community first, else
  the data's community.json; `communitySrc` maps "api/..." pictures. The dist check's server stands in for the route.
  Tests: node 6/6 (the route), unit 60, community check, dist check. Deployed 6e9c7831; the route answers 503 "closed"
  until the Worker has DISCORD_BOT_TOKEN and DISCORD_CHANNEL: Claude Code's safety check refuses Claude's secret writes
  now ("Secret-Store Writes"), so the user sets them (HANDOFF). After that the PC import is only the fallback.
- **2026-11-12, the disclaimer reworded** (user picked from six takes: "let's go with เว็บแฟนเมด ไม่ใช่ของ Official";
  "Official" in English is the user's choice, an exception to the all-Thai rule). Deployed 32507daf; checked live: the
  marks on ไม่ใช่ render clean, top left of the stage.  Later the same day (user: "approve settin the bot secrets"): Claude set DISCORD_BOT_TOKEN (from discord.json, Git
  Bash pipe, never printed) and DISCORD_CHANNEL. /api/community lists the test skin, its picture 200 image/png; a
  headless run of the live page loads both from the route and the pop-up card shows it. Phone approval is live.
- **2026-11-12, the live list's call ceiling lifted** (user: "fix that now"). The free plan allows 50 outgoing calls per
  request; the list made 1 per 100 messages + 1 meta.json download per approved skin (cached a day per data centre),
  so a cold rebuild failed at about 40-45 skins. The Worker now also writes the meta into the embed's footer
  ("meta {json}", <= 2048 chars) and the list reads it from the message: 1 call per 100 messages. Messages from before
  (the two tests) still use their meta.json. meta.json stays (the PC import reads it). node 6/6; deployed c4362bde;
  the live list lists both test messages (the user had ✅'d the format test too). Keep the channel tidy: every message
  costs a little (1 call per 100), so delete rejected submissions now and then.
- **2026-11-12, Rabbit set reskins** (user: "reskin the textures, 3 varaints each for Rabbit, legend, summer set, royal
  and Ant"; then "Whole set", "Themed recolours", "Preview page first"). `pipeline/wardrobe_reskin.py rabbit --preview`:
  per set 3 named themes (legend เพลิงนิล / อเมทิสต์ / มรกต; summer ซันเซ็ต / พาสเทล / ราตรี; royal ไพลิน / มรกตทอง /
  ทับทิมดำ; ant แตนทอง / ด้วงเขียว / โคบอลต์), outfit colour 1 + every set piece, hue bands moved (split by value for
  a dark base vs a glowing trim; a neutral rule tints whites). The outfit's body is kept: equal to the median of the
  Rabbit's 21 outfits, or changed by a colour option (those recolour the fur; 68 % of legend1 vs legend2's differences
  are body). Royal's purple band had to reach hue ~285 (the gun's background). Outputs plans/reskins/rabbit/<set>_<n>/
  (not committed until the user picks) + shots (the local page headless, the canvas only, cropped) + preview.html.
  Known: ant's red emblem on the boots' back stays red (shared with other outfits, so counted as body). Community skins
  of an outfit replace the whole texture, so a reskin fixes the fur at colour 1 (pink) whatever colour the visitor picked.
- **2026-11-12, the Rabbit's summer set as a school uniform, painted on the 3D surface** (user: recolours are "too
  normal"; then a reference picture (black dress, white collar, red ribbon, white cuffs, black knee socks, white
  shoes): "try using this reference for rabbit summer set, make sure it looks good in 3D", "don't bake in the eyes to
  the 2D texture since that part get overlaid by the game face preset anyway"). `pipeline/wardrobe_repaint.py
  [--preview]`: the outfit's mesh (o_summer.bin: pos, uv, bone weights) is drawn into UV space, so every texel has its
  bone, its bind-pose position (x front, y left, z up; the Rabbit is 1.8 tall, knee z 0.39, wrist |y| 0.40) and its UV
  island; gutters take the nearest island's values, so paint reaches them too (no seams). No Blender needed. The design
  paints by part and height and keeps the painted shading (luminance -> a shadow / base / light ramp): dress white ->
  black (navy trim falls to the ramp's shadow, the striped inset plain, buttons dark metal), collar navy -> white,
  sleeves on the arms to |y| 0.30 then a white cuff (the right wrist's band geometry is the cuff), socks to z 0.37 with
  a ribbed top, feet in socks, shoe trim and soles charcoal, the ear's ribbon red. A = that on the pink Rabbit; B =
  also black hair (every Head / Neck texel but the face island), black outer ears, dusty-rose inner ears, the fur left
  showing (thigh, chest) as the face's cream skin. The cap: black crown, white band. Lessons: (1) white cloth turned
  near black shows the webp's 8x8 blocks: luminance is blurred (sigma 2.5) where flat and kept sharp near edges, the
  edge mask as wide as the blur (a narrower one grew dark halos around small marks); (2) tone spans get a floor (0.12)
  or a flat area is stretched into noise; (3) the face presets' pixels span x 24-114, y 18-87 of the sheet and are
  mostly transparent (3.7 %): only eyes and mouth are overlaid, the rest of the head is the skin's; the script asserts
  nothing is painted in y 30-88 there, and that size and alpha equal the original's. Outputs
  plans/reskins/rabbit/summer_uniform_<A|B>/ + shots + uniform.html (not committed until the user picks).  Later (user: "at the shoulder, it is still rabbit skin color, you should fix it black right?"): yes. The summer dress
  is sleeveless: the bare shoulder tops (|y| 0.04-0.09, z 0.83-0.90) are fur on two islands (the pink "V" at the dress
  island's top edge is the shoulders, not a neckline; and the strip at sheet x 330-391, y 244-261). Both black now in A
  and B (B had them as skin); B's skin is the thighs only. Checked front, side, back.
- **2026-11-12, the Cat as the reference's knight: picking the base** (user: a reference picture, a red bodysuit, silver
  armour with gold trim, a white tabard with a gold border; "find the best cat outfit that can best represent this
  reference image", "I don't want a simple recolor, I need the outlines to have a high matching percentage against the
  reference image too. This is a detailed work"). `pipeline/wardrobe_outfit_sheet.py cat <png> [names]` shoots every
  outfit front and back (22 for the Cat). Shortlist by parts: champion, legend, pvpArmor, royal; then champion vs
  legend close up and `pipeline/wardrobe_knight.py --blockout` (both roughly in the reference's colours, plans/reskins/
  cat/blockout.html). Pick: **champion**: white plate with gold trim (pauldron, gauntlets, greaves with pointed knees),
  a white hip cloth with a gold border (the tabard), crossed waist straps (black, they read as the reference's frog
  fasteners), and its torso and thighs are the bare body mesh (islands 3 front / 4 back, thighs 23), a free canvas for
  the red suit's lines. Its shield (left arm; islands at sheet 180,135 and 497,30) hides cleanly with alpha 0 (the
  material's alphaTest 0.5); the arm under it has its own bracer. Legend (symmetric, fully covered, side tassets, dark
  gloves, pointed sabatons) lost: no white cloth, no plate, and its tassets read as wide red hips. The user's question
  "does the original texture matter": so far yes (the uniform reused the original's shading and colour classes, so its
  trims carried over); the knight is to be painted from the mesh (bone, position, island), the original's paint
  optional. `wardrobe_repaint.shots(cls, outfit, variants, out, yaws, size, dpr)` is general now (skins must sit under
  the repo: the page fetches them). Next: the detailed paint on champion, waiting for the user's go.
- **2026-11-12, the Cat's knight: the detailed paint on champion** (user: "You may go ahead, note that you can also change
  the skin color to match, you may also edit the faces your self"; then "if done I want a original vs new 3D vs ref").
  `pipeline/wardrobe_knight.py --paint [--ref <picture>] [--debug]` -> plans/reskins/cat/knight/champion.png, shots,
  knight_compare.png (original | new | reference) and knight.html. What the outfit texture does NOT hold (an island-id
  render showed it: each island a flat colour, numbers on the model): the **hair** (it kept its colour; the Cat's own
  pale blonde stays) and the **eyes** (the face preset's overlay; preset 38 = purple, calm, the closest of the 43; the
  render sets `C.state.face`, a visitor picks it in the page). Painted from the mesh alone (bone, position, normal,
  island; the original's paint not read): the red suit on the bare torso / thighs / arms (islands 3, 4, 23, 24) with
  form shading from the normals (lighter facing up, darker at the sides and island edges), princess seams, a black
  placket with a silver zip, three frog fasteners with studs (z 1.075 / 1.040 / 1.005, |y| < 0.04), a white collar
  close to the neck; red sleeves to the elbow (|y| 0.30) and a painted vambrace below; gold knee emblems with a black
  hexagon (z 0.368, |y| 0.09, front-facing texels); black gloves with plated fingers; fair skin on the head island and
  the head's side under the hair (island 5, dark fur before); ears and tail the hair's blonde. From the original's
  paint, re-toned (its gold trims follow the modelled edges): the plate (silver / the reference's gold), the hip cloth
  (white, its filigree blurred away, thin gold ornaments removed by a binary opening, a soft dark contour beside the
  gold border), the crossed straps and the chest crest (black, gold edges; studs on the crest). The shield: alpha 0.
  Tried and dropped: a painted shoulder cap + fringe (read as a bare white shoulder), a white cape yoke on the back
  (beside fair skin it read as a bare back), a dilated-ring line on the cloth (jagged), black for the choker's gold
  (a dotted line under the chin). `texel_maps` now also gives `nrm` and `edge` (texels to the island's edge); `shots`
  takes `face`. The script asserts the size and that only the shield's texels lose alpha. The reference picture is the
  user's: copied to plans/reskins/cat/reference.png for the comparison, not committed.
- **2026-11-12, the knight polished, and high-res skins** (user: "can you polish a bit more? like the boots shouldn't
  have any gold, and the black outline looks cheap"; then "you are allowed to ignore game logic and apply high-res
  texture"). (1) **The page keeps a skin larger than the game's texture**: `skinDims(uw, uh, w, h)` = the skin's own
  size when it is exactly 2x / 4x / 8x of the original and at most 4096 px, else the original's (as before);
  `composeTexture` sizes its canvas by the skin and scales the face block with it; `skinUpload` and `wearCommunity`
  use it; the import (`wardrobe_community.check`) accepts the same multiples (test: 8 -> 16 kept; 12 refused). Local
  only until a publish + deploy. Send limit: the Worker's 4 MB per file (the knight's 2048 px PNG is 2.4 MB). (2) The
  painter: `HI = 4` (2048 px): the original is enlarged (LANCZOS) for the re-toned parts, the texel maps are drawn at
  that size, seeds / pixel radii / AA scale with K; the drawn lines (frogs, zip, studs, knee hexagons, collar line) are
  sharp. (3) Polish: no dark line on the cloth; the cloth's gold kept per connected piece (a piece with a thick part is
  a border; the per-texel test bit notches into the borders' tips); greaves and boots have no gold (their trims a
  darker steel, faint gold too), only the knee emblems; the collar is the choker's band painted white with one clean
  dark line on top (z 1.287). Checks: unit 61 OK, community check all ok, the Rabbit build still passes.
- **2026-11-12, the knight's hair** (user: "you are granted permission to try change the hair color too btw, I didn't
  restrict you"). The Cat's hair is not on the outfit's sheet (the island-id render had shown that): it is her **head
  piece**, accessory `default` (`BASE_HEAD.cat`; texture props/tex/Cat_default.png, 128 px; `setProp("Head", null)` puts
  it back on), so its skin is a second texture, key `cat|accessories|default|Cat_default.png`. `hair()` re-tones its
  own shading to the reference's blonde at 4x (512 px); ears and tail use the same ramp (BLOND #b0843f / #ecd087 /
  #fdf1c4; a first, more orange ramp read darker than the reference). The set is now two files:
  plans/reskins/cat/knight/champion.png + Cat_default.png. A set of community skins = one submission per piece.
- **2026-11-12, the knight: sleeves, collar, shiny steel, shoulders** (user: "I want more details along her red arm
  cloths, like a black stripe", "add details at her collar", "make the armor looks more silver shiny, now it looks too
  white", "add a fake texture at her right shoulder too, some white furs both left and right"). (1) **The arm's own
  frame**: it hangs 39 degrees off the y axis (axis by SVD of the arm island's positions: 0.05, 0.78, -0.63; length
  0.43, elbow s 0.31, the left band s 0.165-0.29), so rings at constant |y| cut it obliquely; now S = along the arm from
  the shoulder, th = round it from the normals (mirrored for the right arm's texels; 0 = the outer side). A black
  stripe |th| < 0.42 rad with gold piping down the sleeve; the vambrace from s_el. (2) **Shoulders**: a painted
  pauldron (S < 0.10 curving to 0.07 at the sides, |th| < 1.9; gold rim, dark edges, an upper lame line) and under it
  the reference's white fringe (12 strands by |sin(12 th)|, grey between them), on the shared arm texels so both arms
  have it; with real edges it reads as plate (the plain cap of pass 1 read as a bare shoulder). (3) **Collar**: the
  neck band gets a black trim band (z 1.2835), a gold line under it, the front opening (a black V), a ringed stud
  each side; the lapels on the chest a second trim line and a dark knot with a stud. (4) **Steel**: SILVER is a mid
  grey-blue ramp (#3f4553 / #949baf / #f8fafd) and the plate's tone = 0.40 paint + 0.50 env(nz) capped at 0.84 + a
  narrow glint on up-facing texels, env = bright sky, a dark horizon band at nz ~ 0, a dim ground glow; the hip cloth
  stays white, so cloth and plate now differ. Gold takes a quarter of env.  Later (user, with a close-up of the chest crest: "collar has more black in the ref and the image attached should be
  white instead of gold"): the crest's border is the WHITE ramp (the straps keep gold); the collar's black is broader:
  the trim band z 1.2815 +- 0.0055, a black foot under z 1.2475, the front opening a wide V of black lining
  (|y| < 0.006 + 0.42 (z - 1.243)), the studs moved out to |y| 0.026; on the chest a 0.005 black lapel edge, a heavier
  second trim line, a wider knot.
- **2026-11-12, community skins as whole looks** (user: "ease of use for the users is very important ... the user have to
  click too many clicks ... I want more well-thought out batch approach. Skin from community one-click change the whole
  sets and texture"; then "ok build it", "continue"). A submission is now a **set** (a whole look). Format:
  community.json / the Worker's list = `{"sets": [{id, cls, name, link, at, face, thumb, pieces: [{slot, kind, item,
  owner, tex}]}]}`; the first format (`{"skins": [...]}`, Discord meta v1) reads as sets of one everywhere (page,
  Worker, import, publish), so the live test skin keeps working. (1) **Page**: the toolbar's **ลายผู้เล่น** (a count of
  this class's sets) opens `SetGallery`: a card per set (the character's picture, credit, link), **ลองทั้งชุด** = every
  piece on with its textures + the set's face, one undo step (`wearSet`, `equipPieces`); ดาวน์โหลด saves every texture.
  A set none of whose pieces this copy can wear (TTO's, not published) is left out once the prop lists load. The piece
  menu's ลายจากผู้เล่น still lists each piece of a set on its own (COMMUNITY is derived, ids "<set>#<n>"). **ส่งลุคนี้**
  (toolbar, shown only with SUBMIT_KEY and an own skin worn) sends every worn piece wearing the visitor's own skin, each
  can be unticked, with the character's picture (`capturePreview`: the fitted front camera, 360x480 JPEG ~30 KB) and the
  face: one message, one ✅. **Several files dropped at once** (or one beside the character) go to the piece their name
  says, the names this page gives downloads (`12tails_<class>_<item>[_สี n][_ลาย n][_ลายโดย..]`, `(1)` copies too), a
  piece not worn is put on, one undo step (`dropMany`). Toolbar: icons only while the desktop picker is open (with the
  two new buttons it slid under the picker at 1366 px and hid undo; the check caught it). (2) **Worker**: the `pieces`
  form field [{slot, kind, item, textures: [{tex, field}]}], up to 6 pieces / 8 files / 9 MB together, `preview`
  (JPEG/PNG <= 400 KB) and `face`; Discord meta v2 (`pieces`, `face`), the embed's picture is the preview; the list
  serves `/api/community/<id>/<n>.png` (numbered over the whole set) and `/api/community/<id>/preview`. Unverified:
  Discord's per-message limit (believed 10 MB; too much shows as "upstream"). (3) **Import** writes sets,
  `<id>_p.webp` thumbnails (<= 640 px), drops a piece it can't carry (TTO's, missing) and refuses a set with none left.
  (4) **Publish** keeps a set's published pieces and thumbnail. Checks: unit 63, node 8/8, community check all ok
  (new: gallery, ลองทั้งชุด + undo, drop many + undo, ส่งลุคนี้ one request with both pieces + preview + face), menu
  check 35/35. Not deployed (HANDOFF).
- **2026-11-12, ลายผู้เล่น as a picture card, the team's looks, deployed** (user: a mark-up "ลายผู้เล่น here is better" =
  a square under the disclaimer; "awkward crop, please prioritize head"; "please add our Rabbit and Cat creation in it
  too"; "if you have DeetaeZ skin (my friend Whale legend) also put that set in there too please then deploy"). (1) The
  toolbar button became `.cm-card` under the disclaimer (116 px; phone 84 px under the disclaimer; beside an open picker
  top 96 px): the newest set's picture, anchored at the top (background-position 50% 4%; the gallery's thumbnails
  object-position top) so the head shows, and the count. (2) **team_sets.json** (+ data/team/<cls>/): the team's own
  looks, apart from community.json (the Discord import mirrors that one and would drop them); the page merges both
  (sorted by date), the publish carries both with the same per-piece rules. `pipeline/wardrobe_team_sets.py` builds it
  from plans/reskins: the Cat knight (champion 2048 px + the hair piece, face **23**: the renders' 38 is a TTO face the
  public copy lacks, the page fell back to face 0), the Rabbit uniforms A and B (outfit + cap), credited ทีมงาน, their
  pictures cropped 3:4 from the front shots. (3) **DeetaeZ's Whale legend** (outfit, legendHelmet, the lance + shield
  atlas on legendLance and legendShield; video NOTES.md: archived as a match for Whale_legend, they agreed to be named)
  is in the script's FRIENDS but its files are only in the home PC's D:\12tails-assets-archive (not at the office): there
  it is shot from the local page and added (HANDOFF). Checks: unit 64, node 8/8, community check all ok, dist check ok.
  Deployed 065f1bf4 (page + Worker together): live, /api/community (the Discord sets) and team_sets.json load, the
  card counts Cat 1 / Rabbit 2 / Sheep 2, ลองทั้งชุด on the knight gives champion + default + face 23, no errors.  Later the same day (the user pasted DeetaeZ's three textures: "outfit, weapon, headpiece", "Deetaez"): 512 / 256 / 256
  px, exactly Whale legend / Whale_legendWeapon / Whale_legendHelmet, opaque like the originals; kept in
  plans/friends/deetaez/ (tracked, so either PC rebuilds) and wardrobe_team_sets.py reads them there (no archive
  needed). The set: outfit legend, legendHelmet, the weapon atlas on legendLance (R) and legendShield (L), credited
  DeetaeZ, its picture shot from the local page. Deployed 7d3ce552; live: the Whale's card counts 1, ลองทั้งชุด puts all
  four pieces on, the nameplate "Legend ลายโดย DeetaeZ", no errors.
- **2026-11-12, one place to send; the camera an icon** (user: "บันทึกภาพ only icon is enough, and let's change the send
  skin to ทีมงาน place of usage, the new logic will be a button near the camera, what it does is it check all skin the
  preset is wearing if it's not from the default nor the community skins, those skins are filtered to send to
  discord"). บันทึกภาพ: its icon only (aria-label / title keep the name). **ส่งลายให้ทีมงาน** beside it is the only way to
  send: always shown online (SUBMIT_KEY), it collects every worn piece wearing the visitor's own skin (ownPieces: not the
  game's texture, not a community skin, never TTO's) into one submission; with none it says how to put one on. Gone: the
  piece menu's ส่งลายนี้ให้ทีมงาน and the gallery's ส่งลายของคุณ. Phone (<= 480 px): tighter toolbar buttons so the bar
  clears the logo chip (measured: 360 / 390 / 430 px all clear). Checks: community all ok, menu 35 ok.  Deployed cde7de25. Then (user, with the Whale card saying ใส่อยู่ after a part was changed: "you should detect whether
  the user changed any part that replaced the community skins, if yes the try this skin set should be available
  again"): a skin stays in SKINS on a piece taken off, so its presence alone said ใส่อยู่. Now `setWorn2`: worn = every
  piece this copy can wear is on in its slot and all its textures wear this set's skin; the piece pop-up's ใส่อยู่ also
  needs the piece on. Check: wear the look, swap the weapon, the card says ลองทั้งชุด again.- **2026-11-12 (home), the Bat as a robed house student** (user: two reference pictures, a long black robe lined green,
  a grey V-neck sweater with green trim, white shirt, green and silver striped tie, grey pleated skirt, black tights,
  black loafers, long platinum hair, green eyes; "try this reference character for Bat, you may pick the best models").
  `pipeline/wardrobe_bat_robe.py --islands | --paint [--debug]` -> plans/reskins/bat/ (robe/student.png 2048 px, shots,
  robe_compare.png, robe.html; not committed until the user picks). Base: **student** (of the Bat's 22, sheet.png): an
  open knee-length coat (the robe), shirt, a tie that is its own mesh piece, skirt, bare legs, pumps; teacher has no
  coat, royal's coat is closed with a high collar and armour boots, bathRobe is short and belted. The Bat's hair, ears,
  wings and tail are all on the outfit's sheet (1024 px; no head piece as the Cat has), so one texture is the whole
  look. Face 16 (BB's, so online too): green eyes, a stern brow. What was learned: (1) the coat, legs and shoes are
  **mirrored** (both halves read the same texels: an equal count of triangles at y < 0 and y > 0 per island), the torso
  is not: the crest sits on the sweater's left chest (y 0.047, z 1.105), not on the robe. (2) The tie hangs in front
  of the sweater: alpha 0 below z 1.16 tucks it into the V (V point z 1.168); the belt's buckle (island 27 + its inner
  piece, an island of 39 px), and the two loops are alpha 0 too; the skirt island's top (z > 0.95) is the sweater's hem
  (a green stripe at z 0.985, a ribbed band under it). (3) The green facing down the coat's front = the lowest |y| per
  height on the coat's front + 3 cm (read per 1 cm bin it stepped into a row of teeth: interpolate over z). (4) The
  body under the coat pokes through at the shoulder: torso |y| > 0.085 above z 1.22 and the arm to |y| 0.42 are the
  robe's black. (5) Islands under 60 px exist (one shoulder patch reads a single texel at sheet 411,408): paint them by
  seed or they keep the original white. Wings: black backs, green membrane (the robe and its lining); ears black, a
  dark green inside. Not possible on this mesh: the hood, the long loose hair (the Bat's is a ponytail), the flared
  skirt (pleats are painted on the pencil skirt), hoop earrings. The second reference was pasted mid-turn and is not on
  disk (only the first: plans/reskins/bat/reference.png, the user's, not in git).
  Later the same day, the user's review ("give almost every part more texture, cloth wringles, hair details"; "a very
  faint blush"; "fix the necktie, it should start from the collar and goes inside the grey sweater"; "long sleeves
  shirt that is longer than the robe should be white"; "some green part of the robe shouldn't be outside the robe";
  "stockings too dark to look like stockings"; then on the live view: the forehead band "is intended to be hair
  shadow, not the hair color", under the chin the same, the badge "should partially be behind the robe fold", "all 10
  fingernails painted green"). What the painter gained: (1) **Generated detail from body coordinates** (no seams
  between islands): `vnoise` (value noise), `folds(u, w, lam, seed)` = a noise height field stretched along w, lit from
  the side (its slope across u): drape down the coat (stronger to the hem), folds at the elbow and armpit only (all
  along the sleeve they read as stripes), creases at the sweater's waist + a fine knit rib, wandering pleats each a
  little different, rings on the shirt cuff. (2) **Hair strands** (`strands`): noise smeared along a direction field
  (line integral convolution, 28 steps each way): mostly "down the hair" (the sheet-space gradient of z, turned a
  quarter for the tensor: the first try put the gradient itself in and the strands ran in rings), a little of the
  original strokes' own direction; fine + coarse, a shine band broken by them. The painted strokes alone, enlarged
  from 1024 px, gave scribbles. (3) **`ramp` runs on past its light colour for t > 1** (white patches on the shoe,
  blotches in the shine): robe() clips every ramp (`rampc`). (4) **The tie is painted on the shirt** (knot z
  1.299-1.333 under the collar's leaves, the blade widening into the V); the outfit's own tie mesh is alpha 0 (a loose
  one, its knot 6 cm under the collar: it read as a bug). (5) The robe's outside is black only: green = lining, the
  sleeve's inside, the lapel. The coat's chest came through the lapel in black patches seen from below: chest texels
  under the lapel are green (under = the lapel's nearest point lies along the normal, side offset < 2.5 mm; by plain
  distance the green grew a ragged fringe past the lapel's edge; a KD-tree of the lapel's texel positions). (6) **The
  face preset is drawn at 2x** on the Bat's 1024 sheet (eyes z 1.475-1.53, mouth 1.43; the cheeks' blush |y| 0.056,
  z 1.452, 20 %). The face island's dark band under the fringe and under the chin is the hair's SHADOW: skin's shadow
  tone, hair colour only on the island's rim above z 1.5. (7) The crest at y 0.066, z 1.212: the lapel half covers it.
  (8) Tights: a skin-through-black ramp (#1d1516 / #4d3b39 / #8a6a61), lighter where the leg faces front or back and on
  the knee, a shade under the skirt's hem. (9) **Hands**: thumb + index + one block for the other three (bones
  Thumb1-2, Index1-3, Middle1-3), both hands on the same texels; the gloves' holes left edge lines, so the whole hand
  is one skin, the block's fingers drawn apart by two straight lines (the finger's edges fitted as lines along its
  axis), nails on the last joint's outer side (the outer island's mean normal), larger than life (19-21 mm; at 12 mm
  they were specks). The block's last joint has about 20 x 25 px of the 1024 sheet for three nails and curls inward
  in the idle pose: those three are small and seen from the side or behind, not from the front.
  **The live view** (user: "is it possible to see you working on the texture and 3D model in real time?", then
  "please remember the script for this live view, it's really good"): `pipeline/wardrobe_skin_live.html` (the local
  wardrobe in a frame wearing the skin file, put on again whenever the file changes, the flat texture beside it, the
  camera kept): `py -3 pipeline\wardrobe_serve.py 8771`, then
  http://127.0.0.1:8771/pipeline/wardrobe_skin_live.html?cls=bat&outfit=student&face=16&skin=/plans/reskins/bat/robe/student.png
  Open it for the user at the start of any skin painting (CLAUDE.md "Running things"). Outfit textures only so far.

  Then (user: "the darker part is making uneven skin around the bat collar / neck"; "improve the quality of Bat's
  bangs and john details"): the neck island is one even skin (the choker's band had been repainted from its own dark
  tone: a darker patch under the collar), a soft shade up under the chin only. The hair keeps the original's painted
  locks (their shadows cut clean, their glints) under the new detail; `strands()` now works on the hair's texels only
  and gives fine / coarse noise, the clumps' relief (lit across the strands) and single strands as thin lines that taper
  out at both ends; the direction also follows the nearest side edge of each lock, so the lines run together into a
  lock's point instead of being cut by it. The side locks (จอน) are a shade darker under the fringe. Before, the locks
  were washed pale under grainy streaks.

## 2026-11-12 (home), props: the game's shaders (missing textures, glass edges) and the wagasa's loop

User: "Wolf Time Sword and Champion Sword why their textures are missing, champion sword shoe have aqua glass like
blades along the edges of the blade"; "fix Bat Japanese Umbrella non-stop animation loop".
- **Why textures went missing**: the page cut every prop texel under alpha 0.5 (alphaTest), and props/json leaves the
  shader empty. BB's material of the same name (the Bible's `RippedAssets/ExportedProject/Assets/Material/<tex>.mat`)
  says what the alpha is for. Two kinds were wrong: **built-in Diffuse** (fileID 7) ignores alpha: the Time Sword's
  alpha is 96 % under 0.5 (a mask for something else), so it was cut almost away; likewise the Bison Time Hammer, the
  Bat Veggie Hat. **Transparent/AdditiveAlpha** (shader guid 184331bf..., not a file in the rip: known by its materials'
  `_AdditiveColor` / `_AdditiveRange`; the rip's `Shader/AdditiveAlpha.shader` shows the passes): texels with alpha >=
  `_AdditiveRange` (default 0.9; the Bat rapier 0.5178) solid and lit, the rest added as light (texture x alpha, Blend
  SrcAlpha One, Cull Off, ZWrite Off). Every class's champion weapon uses it: their glass edges (alpha ~0.36) were cut.
- `wardrobe_data.py` `game_shader()` writes `"shader": "opaque"` or `"shader": "addAlpha", "cut": r` on BB prop
  materials (1455 opaque, 13 addAlpha); the page: opaque = no alphaTest, addAlpha = alphaTest at the cut + `glowTwin`
  (a copy of the mesh drawing the texels under the cut additively, premultiplied with alpha = the brightest channel, as
  fxMaterial's additive blends; flagged hoverOverlay so hover tints / outlines skip it; shares the texture, so skins
  swap it too). Not touched: built-in fileID 30 (the glasses' lenses: cut as before), fileID 202 (halos), shader
  5eda1254 (Cat luckyStarKnife, Penguin lightScepter: also carry _AdditiveColor, unconfirmed).
- **`--props-only` drops the ToT pieces**: run `py -3.10 pipeline/wardrobe_tot.py` after it (its docstring says so).
  That run also wrote 7 `props/tex/tot_*_Student_Color.png` hat textures the tracked data already named but git never had
  (the office's ToT student hats were untextured).
- **The wagasa**: its default clip "close" (0.4 s) looped for ever (the data marks every clip a loop). The game holds it
  closed and toggles open / close on the battle emote (Bat.cs: `mWep1.animation.CrossFade("open" / "close")` for
  w_bat65 under "emo_battle"). finishProp now plays a clip that ends away from its start (0.1 in position / scale, 14
  degrees) once and holds its end: the wagasa, and the Mole's barrel and legend cannons' "fire" (a handle / a drum
  turned one step; they snapped back every 0.2 s). Every wing and other loop drifts at most 0.04 and still loops.

## 2026-11-12/13 (home), weapons' own effects

User: "Can you add particle effects for weapons too?" `pipeline/wardrobe_weapon_fx.py [cls ...]` -> `data/<cls>/weapon_fx.json`
(a file of its own: wardrobe_fx.py rewrites fx.json's effects and materials only) + `data/fx/tex/`. 310 BB weapons:
61 with Unity 3.5 legacy particles (flaming, mummy, pvp, butterfly, candles, lanterns ...), 230 with the game's
TrailEmitter (no code switches it: it draws whenever the weapon moves, so at rest it barely shows, a skill's swing streaks
it), 5 TrailRenderer, 4 ImageEmitter, 1 BoltEmitter, 15 Shuriken (the time weapons + moroccoLamp, russiaMatryoshka).
- Read with wardrobe_fx.py's own Game / effect (the prefab by its Resources path heroes/<cls>/weapons/<name>), the
  weapon's mesh, material and Animation dropped (the prop draws and plays them). wardrobe_fx.py does not decode BB's
  Shuriken, so those 15 are read whole from **TTO's client copy** (wardrobe_fx_tto.py's Tto now takes folder="weapons";
  its materials / textures tto_*, published scrambled as every TTO texture). Which ones: the rip's prefab has class 198.
- Page: `weaponFx(root, name)` from setProp (weapon slots): an Fx whose root follows the worn prop's root every frame
  (`fx.follow`: mirror^-1 x root.matrixWorld x mirror, scale too), shown while the prop is; its own list `WFX.live`
  (FX.live is cleared by every new pick and a move's end waits on it), disposed once its prop leaves the stage.
- **tangentVelocity was missing from legacyParticles**: the speed outward from the emitter's surface, per axis (added to
  the local velocity, turned with the emitter). All of the flaming weapons' flames' speed is this: they spawned still, and
  a stretched quad with no speed draws nothing (the Sheep's Flaming Book showed no fire). The one skill effect with it is
  the Sheep's lullaby_ring. MEDIUM SURE (Unity's legacy source is not available; the 3.5 manual's "starting speed of
  particles along X, Y, and Z, across the Emitter's surface" and the common use): the user to compare with the game.
- Not done: Sheep mothLatern (its particle material is a null reference in the game files: nothing to draw), Monkey
  spiderMike / R (UVScroll) and Penguin hallowLattern (simplePendulum): scripts with no byte layout in wardrobe_fx.py
  LAYOUTS (not particles; the builder skips the whole weapon); TTO-only weapons.
- Online: wardrobe_publish.py publish_weapon_fx copies weapon_fx.json and its textures. Check:
  `pipeline/wardrobe_weapon_fx_check.py [out.png] [cls:item ...]` (headless; fails on a weapon with particles drawing
  nothing, an effect outliving its weapon, a page error).

## 2026-11-13 (overnight, home), every class's skill effects: the run (plans/goal_fx_all_classes.md)

User, before bed: "finish all classes skill sfx and vfx all skills, commit push and deploy" (usage guard 70 % for this
run; it was at 47 % at the start). Order: Penguin, Bat, Bison, Cat, Chameleon, Mole, Monkey, Panda, Rabbit, Whale.
- Workflows: `penguin-fx-finish` (effect-only tiles: researcher -> checker -> editor -> the Penguin's QA) and, per class,
  `class-fx` with args `{mode: "research"|"build", cls, Cls, skills, tto, released}` (research: six read-only
  researchers in plans/fx_<cls>/ {attacks_emotes, skills_a, skills_b, tto, effect_only, parts}.md + three checkers
  appending "## Verification"; build: a planner writing plans/fx_<cls>/decisions.md ("decided overnight, for the user's
  review") and splitting the missing parts, up to four builders on disjoint files, one editor (cues, tiles, icons, data,
  the dark fx check as the gate), one QA with wardrobe_fx_shots.py). The script is saved in this session's folder; to run
  it in another session, re-create it from this description (the research of one class overlaps the build of the one
  before; builds never overlap, they share index.html).
- Progress: Penguin, Bat, Bison, Cat, Chameleon DONE, committed and deployed (last: 49b0bc5, version d8254611, data-2f9f8dd372). Mole research done + committed (6a166de); its build stopped by the user at 07:05 ("stop here for now, push and deploy all progress") after only its planner (plans/fx_mole/decisions.md, 63 decisions): nothing of the Mole in the page or data. Not started: Monkey, Panda, Rabbit, Whale. Usage 66 % weekly at the stop (47 % at the start). HANDOFF.md says how to continue.
- **Bat build, page_pipeline builder (2026-11-13):** the game's Particles/MultiplyOffset, AlphaOffset and AdditiveOffset
  shaders (fxparts/particles.js) and built-in 205 = Particles/Multiply (`BUILTIN_BLEND[205] = "multiply"`) are now built for
  every class. That changes the look of effects already cued and published: the Wolf's Double Art banner (doubleArt),
  bladeFang_hit / bloodFang_hit, darkEdge_hit, vitalityStrike_hit; the Sheep's returnCast / freeCast / instantCast banners;
  the Penguin's nAttack_hit; the status words (miss, resist, immune, evade, reflect ...). The Offset ones now draw in
  front, with rgb x alpha; the multiply ones darken instead of glowing. This takes effect only after each class's fx.json
  is rebuilt (`wardrobe_fx.py <cls>`), since the blend is written into the data; until then only the new page shaders
  apply to materials already saved as `shader:Particles/*Offset` (decision 41, parts.md Q7). Other page changes: Opaque1
  always builds two passes, so cosmicFriday has one more material that draws nothing; `Fx.dispose` now also stops an
  effect's one-shot AudioSources (Unity's Destroy does too), so a new pick or an effect's end now cuts its own one-shot
  sounds in every class.

## 2026-11-13 (overnight, home), the Penguin's effect-only tiles

From plans/fx_penguin/effect_only.md (its "## Verification" wins: the corrected SEQ comment). Five tiles on the idle
stance, one per skill: **Mana Arc** (root@2), **Dispell** (root@2), **Double Cast** (root@1.5), **Triple Cast** (root@1.5),
**Frost Spike** (root@1).
- Page (wardrobe/index.html): SEQ penguin's five `"<Name>: root@t"` (step = the effect's EffectControl life + afterLife,
  at least the longest voice), SEQ_SKILL `@ManaArc/@Dispell/@DoubleCast/@TripleCast/@FrostSpike`, and one new page part:
  a cue's `"rot": "random"` = Unity's Random.rotation (`randRot`, Shoemake's uniform quaternion as YXZ Euler degrees,
  drawn per play in cueOf), for Mana Arc's ring cage (`createEffect(penguinOfArc, hero + 0.5 up, Random.rotation)`
  Penguin.cs:21798).
- Cues (wardrobe/fx_cues/penguin.json, before "wave"): `@ManaArc:root` penguinOfArc (#412 on: hasSkill(412) :21774;
  max rank sLv 4, pgn_manaArc4 :7430) {y 0.5, rot random} + voice manaArc1|manaArc2 (:21886); `@Dispell:root` dispell
  (:22289-22301) + dispell1|dispell2 (:22355); `@DoubleCast:root` / `@TripleCast:root` multiCast (RPC_multiCast sLv 1 / 2,
  :9819-10007, effect :9838-9850) + multiCast1|multiCast3 / multiCast2|multiCast3 (:9897-10006); `@FrostSpike:root`
  frostSpike_ring (Instantiate identity :37883-37895; proc CharacterControl.cs:31236-31270) + frostSpike1|frostSpike2
  (:37947).
- Icons: wardrobe_skill_icons.py EFFECT_ONLY penguin + frostSpike (Bible penguin_frostSpike5); ran it: only
  data/icons/hd/index.json's frostSpike entry and penguin/frostSpike.webp changed.
- Data: `wardrobe_fx.py penguin --fx penguinOfArc,dispell,multiCast,frostSpike_ring --voices manaArc1,manaArc2,dispell1,
  dispell2,multiCast1,multiCast2,multiCast3,frostSpike1,frostSpike2` (merged: fx.json 77 effects; new sfx dispell.mp3,
  frostSpike.mp3, nine v_*.mp3; data/fx/tex/frost.webp). No TTO effect, so no wardrobe_fx_tto.py.
- Judgement calls (effect_only.md's defaults; the open points stay the user's): Mana Arc plays penguinOfArc, not manaArc
  (passives on); the random rotation built (not the fixed prefab tilts); voices every play (the game's 2 / 6 / 12 s voice
  timers only thin out spamming); Frost Spike's burst alone, every play (no 12 % roll, no Ice Shield around her: the
  variant is in the report); left out: Dispell's camera screen warp (AddScreenWarp ringMask :22433, no page part; Cat /
  Chameleon / Whale use barrierMask / zoomMask / ringMask+burstMask), the multiCast status's purple tint (decision 10's
  analogy; open point for the user on these two tiles, where the tint is the buff).
- Gotcha: the Edit tool rewrote index.html with CRLF on every line (the repo keeps it LF, .gitattributes eol=lf, and the
  publish copies its bytes): converted back to LF; check `grep -c $'\r$' wardrobe/index.html` = 0 after editing it.
- Gate: files-only penguin "no problems"; `wardrobe_fx_check.py ... checks/fx_penguin dark --cls penguin` exit 0,
  errors [], all 44 tiles played, the five new ones each spawning their effect (penguinOfArc 200 v, dispell 84 v,
  multiCast 162 v x2, frostSpike_ring 504 v). Not committed (the run's commit does it).

## 2026-11-13 (overnight, home), the Bat's effects: built and cued

From plans/fx_bat/ (six reports, each with its "## Verification", which wins; decisions.md decided overnight for the
user's review). One editor after four builders (page_pipeline, bat_parts, shared_parts, tto_bat).
- **Parts (new):** fxparts/bat.js (Bat_nAttack / Bat_illusionFire bolts with the Homing Wand's homing, Bat_echoes,
  Bat_mirageOrb, Bat_guardianOfTheNight's AI state machine, the fx:castRing root-loop hook, bat only), particles.js (the
  Offset shaders + 205 multiply), audiocontrol.js (AudioControl's fade, nefariousWhip_hit), light.js (pooled point lights:
  drainLife, mindControl_ring), tto_bat.js (BatSwarmFlap + the Bat.NightfallSwarm mover, the hero hidden 0.4-0.9 s). Page:
  api.spawn (+ followNode), the "clone" cue kind (HeroClone: SkeletonUtils copy of the dressed hero, tinted (0.3, 0.2,
  0.5), its own mixer), fx.sounds (one-shots stopped at dispose), boltEmitter aiming at a cue's `to`, two pooled
  PointLights with a 1/(1+25u^2) falloff, cue option `worn`, entry keys `builds` and `everyCycle`, Opaque1's two passes.
  wardrobe_fx.py: the Bat LAYOUTS, BUILTIN_BLEND[205], ALIASES / SOUND_ALIASES (guardian_hit / guardian_nAttack = Shade4's),
  hero_sound_wav (a "sound" cue outside the class's sounds/, skipping characters/: step_fly1).
- **Fix found by the gate:** Bat_guardianOfTheNight looked its `sword` bone up when the part was built, but a root part is
  built before the later nodes are named (index.html Fx fills them in order), so the blade never spawned; it now looks
  the bone up when the blade is due (fxparts/bat.js). A part that needs another node of its effect must look it up late.
- **Cues** (wardrobe/fx_cues/bat.json, 32 entries, 210 cues; assembled from the reports' corrected blocks by
  checks/fx_bat_research/editor/assemble.py, git-ignored): Normal Attack (nAttack1-3, ground hits `notWorn` the Homing
  Wand, its hits `worn` at 0.24 / 1.04 s, d 9.7: the bolt part's 0.54 s contact, decision 15), Drain Life (cAttack1-2),
  cast1, the cast3 pool's 19 members (Auto Mass 12 % on 11), Nightmare and Mind Control sequences (`@Nightmare:*`,
  `@MindControl:*`), echoes (hits d 9.7), soulEater, bigCast1-2, the bigCast3 pool (Guardian of the Night `{d -4, end 10,
  to [0, 0, 10], kill 12}` + `builds` guardian_blade, guardian_hit, sound:guardian_nAttack; Nefarious Whip; Black
  Servant), nightfallSwarm (TTO, released: 28 bats), the four effect-only tiles (`@MassCast:root`, `@ShadowGaze:root`,
  `@Switch:root` in the hero-stays frame, `@ShadowSacrifice:root`), emotes (wave, bow, laugh, sleep, cheer, beg, cry, talk
  chat1-3, battle), ko (ko | dead with deadEffect), run (`everyCycle`, step_fly1 at 0.1 s).
- **Tiles / icons:** SEQ bat and SEQ_SKILL bat as the merged blocks (Normal Attack @0.6 / @0.6, Drain Life cAttack2*@6.2,
  Nightmare channel @8.9, Mind Control @9.9, Guardian bigCast1@1 bigCast2*@0.1, Mass Cast root@1, Shadow Gaze root@2,
  Switch root@1, Shadow Sacrifice root@2); wardrobe_skill_icons.py OWN_TILE bat {nightmare, mindControl}, EFFECT_ONLY bat;
  rerun with the cue file in place: bat 33 HD icons (28 new webp under data/icons/hd/bat + index.json).
- **Data:** `wardrobe_fx.py bat`: 50 effects, 65 materials, 62 textures, 116 sounds; `wardrobe_fx_tto.py bat`: 5 TTO
  effects, 7 materials, 7 textures, 2 TTO-only sounds (nightfallSwarm_flap / _screech). data/bat/fx.json 55 effects,
  sfx/ 118 files, 46 new textures in data/fx/tex (all tracked: they go in the run's commit; the other PC pulls).
- **Judgement calls (mine):** Hate Transfer has no voice cue: BB and TTO both load voices/hateTransfer1 / 2, which neither
  BB's rip nor TTO's catalog has (the game logs "Cannot find hateTransfer1 voice", Bat.cs:33619), so the game is silent;
  Shadow Illusion's clones are `"clone", "root"` cues (the part tints them itself, no `tint` option) with illusion_dust at
  their end (10.4 s, decision 21); the check no longer expects effects from `worn` cues (wardrobe_fx_check.py expected():
  they need an item the default dress lacks). Clones (d 2.6, x +-1.5) and every target-point effect sit outside the
  default camera's frame, toward the camera, as for the other classes.
- **Gate:** files-only bat "no problems"; `wardrobe_fx_check.py ... checks/fx_bat dark --cls bat` exit 0, errors [], 44
  tiles played, every cued effect spawned (the guardian's blade and both hits included). Not committed.
- **Open:** rebuild wolf / sheep / penguin fx.json for the 205 multiply look (above); the light's 2 pi intensity and the
  Offset shaders' look are by eye, not yet checked by the user; offers for the Bible are listed at the end of
  plans/fx_bat/decisions.md.
- **QA pass (2026-11-13, the run's Bat QA step).** Shot with `wardrobe_fx_shots.py --jobs` (virtual clock; jobs
  checks/fx_bat_qa/jobs.json, 41 jobs, every Bat tile) on the dark and the white stage, side + behind views (front for the
  clones and the near effects): Normal Attack (as rolled, and with the Homing Wand worn), Drain Life, Nightmare, Mind
  Control, Mass Cast, Shadow Gaze, Switch, Shadow Sacrifice, all 19 cast3 members (Auto Mass forced on Dissolute, Charm's
  50 % roll forced), Guardian of the Night to 14.5 s, Nefarious Whip, Black Servant, Echoes, Soul Eater, Nightfall Swarm,
  KO (dead forced, and as rolled), run, wave / talk / battle. Sheets: checks/fx_bat_qa/sheets_dark, sheets_white
  (git-ignored; shots under run/, logs run/*.log). Everything lands where the reports and decisions.md say (boxes in the
  hero's frame; the cast3 tiles' time = clip time + 0.7 s): the combo's bolts end at the 10 m line at 0.906 / 1.506 s, the
  stage-3 side hits at x +-3.44 (2.33 s); with the Homing Wand they meet the body at 9.7 m (0.84 / 1.44 / 2.24 s) and the
  ground hits stay out; the drain beam reaches z 9.83, its ticks at 1.7-5.7 s, Dream Burst at 6.7 s, gone at the 6.87 s
  release; nightmare (scale 3) and mindControl at the target to 10.1 / 11.1 s, their beams cut at the same time; Phantom
  Bane's ticks every 2 s from 2.1 s; Blind / Confusion and Chiroptophobia end at 11.1 s; the Mirage Orb flashes every
  0.5 s and goes after its 11th tick (gone by 6.0 s); the two clones (tinted, idle, at x +-1.5, d 2.6) end at 11.1 s with
  illusion_dust there; Switch's three flashes and Shadow Sacrifice's dust at the summon spots; Dark Stalker at d 9.6-10
  to 11.1 s; the guardian walks in behind her (z -4 -> -2), its first attack at spawn + 4 s (6.1 s: fade, the dash z 18 ->
  12 with the blade, hits at 7.2 / 7.7 s, back, fade in), the scan at 8.6 s finds it still fading in, so the next attack
  is at 11.1 s and the unsummon at 12.1 s aborts it before its first hit: it falls (ko) where the dash left it, near the
  target, gone at 14.1 s; Echoes' orbs home and hit at 3.02 / 3.2 s; Nightfall Swarm hides her 0.4-0.9 s, the 28 bats run
  the 12.5 m road, the hit at 0.73 s, they wait at the road's end and fold into her chest in Regather's last 0.1 s
  (k^2, as TTO), gone at 1.15 s; the run's step_fly1 every 0.8 s cycle at 0.10-0.12 s (checks/fx_bat_qa/run_sound_probe.py,
  real time). No page error, no stalled render loop in any job (the only console lines: swiftshader's glBlitFramebuffer
  feedback warning, in the Penguin's QA logs too).
  - **No bug found; no file changed by the QA.** Looked into, not bugs: nightmare's Particles/Multiply sphere is solid
    black on the dark stage (multiply over the empty canvas is the grey approximation, particles.js; on the white stage its
    texture shows); the cyan glow at her hand during Nightmare / Mind Control (nightmare_ring's ImageEmitter, 2 a second,
    life 0.5) is there in some shots and not others; bigCast_ring's age 99.x = the cut jumping to its life's end; a
    sequence step's cues start one frame early (the render loop runs seqTick, which zeroes FX.t, then fxTick adds that
    frame's dt: Drain Life's cAttack2 at 0.667 s, not 0.7), page-wide and within a frame, left as it is.
  - Gates: `wardrobe_fx_check.py ... dark --cls bat` exit 0, errors [] (44 tiles); the builders changed shared page /
    fxparts code, so also `--cls wolf`, `--cls sheep`, `--cls penguin`: exit 0, errors [] each (no other class has cues);
    unit tests 65 OK, node 8 pass, test_adopt_from_video.ps1 fails 0; `wardrobe_weapon_fx_check.py` OK.
  - For the user's eye: the white stage (the multiply shadows show their texture there, the additive glows are faint or
    show as coloured haze); the guardian's look (body / wing alphas, the large dark wing quads in its nAttack swing, its ko
    fall near the target when the 10 s cut lands mid-attack); the Mirage Orb's brightness (two double-sided additive shells
    at the game's opacity); the light's intensity (drainLife, mindControl_ring); decisions 8, 9, 13, 22, 23 and 44 (what is
    left out).

## 2026-11-13 (overnight, home), the Bison's effects: built and cued

From plans/fx_bison/ (six reports, each with its "## Verification", which wins; decisions.md decided overnight for the
user's review). One editor after three builders (page_pipeline, bison_parts, tto_bison).
- **Parts (new):** page (index.html): SEQ steps with alternatives `a|b` (`%p` = a chance, drawn per round, test hook
  `window.__seqAlt`) and crossfades of any length (`~0.3`); a cue's `bone` + `rot` = Unity's localRotation under the bone
  (Over Power's horn on Head, Euler(-90, 0, 0)); HERO_SKINS body looks `enrage` (x 1.25, tint (1.22, 0.64, 0.64)) and
  `titanForm` (x 1.8, (0.70, 0.81, 1.16)), the hero's own materials tinted in place and restored; the `lift` cue kind
  (LIFTS.titanDrop = TitanDropPath's height keys, Hermite, the hero raised in place; followPosition effects ride it);
  ITEM_SETS.bisonHammer (BB's 22 isHammer codes + timeHammer = 21 names) with `wearing()` for worn / notWorn (an item, a
  list or a set name); NEVER_PLAYED.bison volcanicRam; FX_PART_FILES += bison, uvscroll, tto_bison. fxparts: bison.js
  (Bison_earthRupture mover 12 m/s for 2 s; Bison_overLord null), uvscroll.js (UVScroll by the page's absolute clock, its
  map cloned once the picture is in), alphatimer.js (Opaque1 / Opaque2 on both passes; the per-renderer copy shared via
  mesh.userData.fxOwn), tto_bison.js (Bison_c6Arc with repeat + ground drape, Bison_row6Fx with bob, the EnergyArc and
  MoltenCrust shaders, GroundConformParticles a no-op). wardrobe_fx.py: LAYOUTS UVScroll / Bison_earthRupture /
  Bison_overLord; SHURIKEN_FROM_TTO: magmaClutter_ring2's Shuriken puffs grafted from TTO's decoded copy onto BB's effect
  with BB's Bomb2 material (decision 40: BB content, the `cleave` swing kept). wardrobe_fx_tto.py SKILL_FX bison (17 + the
  status look `unchained`). wardrobe_fx_check.py: alternatives played once each, `lift`. wardrobe_moves_check.py's
  chains.json lists alternatives; mesh.js' Opaque comment updated; wardrobe_fx_inventory.py BUILT / notes, rerun.
- **Cues** (wardrobe/fx_cues/bison.json, 40 keys, 420 cues, 67 effects (18 TTO), assembled from the reports' corrected
  blocks by checks/fx_bison_build/editor/assemble.py, git-ignored, with decisions 22 / 25-26 / 40 applied): Normal Attack
  `nAttack1@0.7 nAttack2@0.7 nAttack4@1.3%56|nAttack3@0.8 nAttack5~0.3` (voices only: melee hits never reach 10 m),
  Charge Attack with Hold Charge (`@ChargeAttack:root`: holdCharge_ring + the holdCharge glow, the stored spin's
  holdCharge_fire, 16 swish sounds), nine skills_a clips (Power Cleave's axe / hammer sets by `["R", "bisonHammer"]`,
  Earth Rupture's three waves, Mass Stun and six Calamity strikes at 10 m, Magma Clutter's TTO-fix start sound), the
  overPower pool (Over Power, Titan Form with its body look and ring scale 1.8) and the warcry pool (Warcry, Iron / Diamond
  Shield 8 s, Onslaught silent), Over Swing wearing the horn and ring for 1.2 s, Pride Crusher silent, Slam, Trample
  (trample2*@2.4, cuts 2.4), effect-only `@BerserkerRush:root` (6 s) and `@FuryTrance:root` (furyTrance3, cut 10), the
  three released TTO skills (Unchained Fury with `tto/unchained`; Titan Drop with `[0, "lift", "titanDrop"]`, the slam
  3.9 m ahead / 0.26 m right; Magma Quake by the worn weapon, the game's 144 / 120 seed-0 tick spots), emotes (laugh
  silent: no voice in the rip), run (step_heavy1 / 2 every cycle), ko (dead: deadEffect 1 m behind, d -1).
- **Tiles / icons:** SEQ / SEQ_SKILL bison as the merged blocks (the page_pipeline builder pasted them); wardrobe_skill_icons.py
  CLIP_SKILLS bison {cleave: powerCleave}, EFFECT_ONLY bison; rerun: bison 25 HD icons (7 new webp: berserkerRush,
  diamondShield, furyTrance, ironShield, onslaught, powerCleave, titanForm; index.json bison only).
- **Data:** `wardrobe_fx.py bison`: 49 effects, 41 materials, 42 textures, 88 sounds (the graft line printed);
  `wardrobe_fx_tto.py bison`: 18 TTO effects, 23 materials, 13 textures, 15 sounds (6 TTO's own: MagmaPit, break,
  earthSmasher_ring, gadina_planetBreaker, titanQuake_hit, titanQuake_ring). data/bison/fx.json 67 effects (4.2 MB), sfx/
  98 files, 35 new textures in data/fx/tex (all to commit with the run; the other PC pulls).
- **Judgement calls (mine):** the hammer branches (powerHammer, Magma Quake's earthSmasher_ring / quakeTick / quakeSlam /
  quakeField) are `worn` cues, which the gate doesn't expect, so checks/fx_bison_build/editor/hammer_probe.py played
  cleave and magmaQuakeAxe with royalHammer worn: all spawned (121 quake ticks), errors []. The Titan Form look at 1.8x
  leaves the default camera frame (head and shoulders off the top; the camera doesn't refit for a skin): left for the QA /
  the user's eye, not changed. Target-point effects (Titan Drop's slams 3.9 m ahead, Mass Stun, the strikes) sit toward
  the camera outside the default frame, as for the other classes.
- **Gate:** files-only (bat, bison, penguin, sheep, wolf) "no problems"; `wardrobe_fx_check.py ... checks/fx_bison dark
  --cls bison` exit 0, errors [], 37 tile plays (Normal Attack twice: nAttack4, then nAttack3), every cued effect spawned
  (lift:titanDrop, skin:enrage / skin:titanForm included); unit tests 65 OK. The builders changed shared page / fxparts
  code, so also `--cls bat,wolf,sheep,penguin` in one run: it found a page bug (below), then exit 0, errors [] (174 tile
  plays); the Bison gate re-run after the fix: exit 0, errors []. Not committed.
- **Fix found by the regression gate:** a class change kept the old move's cues still to come (FX.cues, FX.cycle): the
  Bat's run (everyCycle) re-armed step_fly1 and fired it once the Wolf was in, asking for data/wolf/sfx/step_fly1.mp3
  (404). loadClass now drops them with the old class (index.html, beside its fxClear()); the same held for any pending
  cue (a Calamity strike due at 9.9 s) when the class is switched mid-skill.
- **Open:** the user's review of decisions.md (Titan Drop in place with the lift, Magma Quake's fixed seed-0 spots and its
  far ticks' cost, Hold Charge on the Charge Attack tile, volcanicRam hidden); the Bible offers at the end of
  plans/fx_bison/decisions.md; the QA pass (wardrobe_fx_shots.py) for the looks (EnergyArc / MoltenCrust shaders compiled
  only in the gate's headless run, the 1.8x framing, UVScroll's hordes).
- **QA pass (2026-11-13, the run's Bison QA step).** Shot with `wardrobe_fx_shots.py --jobs` (virtual clock; jobs
  checks/fx_bison_qa/jobs.json, 40 jobs, every Bison tile: Normal Attack, Charge Attack to 10.2 s, the nine skills_a clips
  (Power Cleave also with royalHammer worn), both pools' six members, Over Swing, Pride Crusher, Slam, Trample, the two
  effect-only tiles, the three TTO tiles (Magma Quake also with royalHammer), KO (dead forced, and as rolled), run, the
  emotes with voices, laugh) on the dark and the white stage, side + front / behind / top: 366 shots each. Sheets:
  checks/fx_bison_qa/sheets_dark, sheets_white (git-ignored; shots and logs under run/). Boxes in the hero's frame
  (+x = the hero's left, so the cues' Unity x shows negative) match the reports: farStun_ring centred (-0.42, 0.19)
  (x 0.5, d 0.15); massStun round the 10 m point (z 5.8-16.2); afterShock centred 2 m ahead; Earth Rupture's three
  waves fan out at +-25 deg and their front passes 12 m at 0.97 s; Calamity's strikes at z ~10 at 2.4 / 3.9 ... 9.9 s,
  the last gone by 11.5 s; the Over Power horns on the head (upright, both sides) to 9.5 s, the ring with them; Titan
  Form's growth from 0.3 s, its ring at 1.8x (r 1.47-1.74), both gone at 10.3 s; Enrage x 1.25 and red from 0.5 s to
  10.5 s; the shields orbit from 0.6 s to 8.6 s; Berserker Rush on both hands to 6 s; Fury Trance at the neck to 10 s;
  Hold Charge's glow gone by the spin (0.2 s), spinHack_ring cut at 1.766 s; Trample's trample2 lives from 0.3 s to the
  cut at 3.3 s (trample2's 2.4) and the two hordes run 2.5 m left and right, in step; Unchained Fury's plant centred
  (-2.45, 2.6), its Berserker Rush look to 10.6 s; Titan Drop's mark and three slams centred (-0.26, 3.9) on the floor
  while the hero rises 3 m (the shots' camera rides the hero, so the floor drops away there), the dive from above
  ahead; Magma Quake's ticks 1 + 12 a burst from 1.4 s (the axe's field's pool fades from 6 s by its own PoolFade
  particles, gone by 7 s; the hammer's to 7.9 s); KO's deadEffect 1 m behind. No page error, no stalled render loop,
  no failed job (the only console lines: swiftshader's glBlitFramebuffer feedback warning). checks/fx_bison_qa/
  body_probe.py: Titan Form / Enrage / the lift end cleanly on the next pick, mid-air, with VFX off and on a class
  change (scale 1, y 0, colours back), errors [].
  - **No bug found; no file changed by the QA** (except this paragraph).
  - Gates: `wardrobe_fx_check.py ... checks/fx_bison_qa/gate_bison dark --cls bison` exit 0, errors [] (37 tile plays);
    the builders changed shared page / fxparts code, so also `--cls wolf,sheep,penguin,bat` (every other class with
    cues): exit 0, errors [] (174 tile plays); unit tests 65 OK, node 8 pass, test_adopt_from_video.ps1 fails 0;
    `wardrobe_weapon_fx_check.py` OK.
  - Looked into, not bugs: the magma field's MoltenCrust looks blocky up close (its value noise at 3.1 / m, the TTO
    shader's own arithmetic); cut rings jump to their life's end (prideCrusher_ring age 2.12 at 0.95 s, as the Bat's
    QA).
  - For the user's eye: the default camera (a close fit of the standing hero) shows only Titan Form's legs and loses the
    Bison entirely at the top of Titan Drop's leap (checks/fx_bison_qa/frame/TitanForm.png, titanDrop_top.png; a zoom
    out shows both whole); every target-point effect sits outside that frame too, as for the other classes. Also the
    white stage's faint additive glows, the EnergyArc crescents and the MoltenCrust pool (the shaders draw, their look
    is unjudged), Magma Quake's 144 ticks' cost on a slow PC.

## 2026-11-13 (overnight, home), the Cat's effects: built and cued

From plans/fx_cat/ (six reports, each with its "## Verification", which wins; decisions.md decided overnight for the
user's review). One editor after four builders (cat, generic = worldcollider + additivealpha, tto_cat, page_pipeline).
- **Parts (new):** fxparts/cat.js (Cat_grandCasinoArcade: materials [1] / [2] blink 0.15 sin(4 T) in counter-phase;
  fx:grandCasinoArcade plays the cue's `anims` on the machine node and sets cutAt -Infinity at age 15.5 (the standby);
  Cat_supportFire: 30 m/s along its spawn rotation, gravity on the 0.02 s step, supportFire_hit spawned on the floor;
  fx:supportFire_cannon: the six cannons of one play keyed by FX.gen, the first living one owns the barrage clock, from
  age 1.25 every 0.24-0.35 s a random cannon rewinds + plays `fire` and spawns supportFire_smoke / supportFire_fire at
  getTrajectoryVector's pitch for 24-47 m, at the cut every cannon fadeOut(0.5)); fxparts/worldcollider.js
  (WorldParticleCollider: legacy particles bounce off y 0 with the whole velocity x bounceFactor, via the new
  legacyParticles `collide` hook); fxparts/additivealpha.js (shader Transparent/AdditiveAlpha, two passes, the material's
  `cut` = _AdditiveRange); fxparts/tto_cat.js (Cat_royalCard, Cat_royalHandBanner, Cat_eclipseFx moon + blade with
  HoldWeapon copying the worn R prop, the movers Cat.RoyalSwordFall / Cat.DropAnchorFlight holding the Leash rings back
  to the landing, shaders Unlit/Color, Unlit/Texture). mesh.js: an Animation with play off is built (idle until play()),
  rewind(); alphatimer.js: fadeOut(sec); tto_penguin.js: the cel shader draws _FresnelBrightness / _RimAlpha (other
  classes' cel materials carry 0 / 0, so they look as before). index.html: SEQ cat (13 sequences), SEQ_SKILL cat,
  NEVER_PLAYED.cat shikifujin, FX_PART_FILES += cat, worldcollider, additivealpha, tto_cat; cue option `single` (a live
  copy's kill renewed instead of a second spawn); cue kind `hideProp` [t, "hideProp", "R", {kill}] (the worn prop's
  meshes off the layers, VFX on only; weapon_fx keeps drawing). wardrobe_fx.py: LAYOUTS Cat_grandCasinoArcade /
  Cat_supportFire, WorldParticleCollider stored, AdditiveAlpha's cut, SHURIKEN_FROM_TTO.cat supportFire_hit with BB's
  Bomb2 (new bb_material()), ALIASES.cat.doom = the Bat's doom, BUILTIN_BLEND 205-207 certain. wardrobe_fx_tto.py:
  SKILL_FX.cat (28), CODE_MOVERS, SHADER_BLEND += Multiply / Multiply (Double) / Alpha Blended Premultiply (the Cat's
  weapon_fx moroccoLamp tto_Smoke4 turns multiply2 at the next wardrobe_weapon_fx.py run). wardrobe_fx_check.py: KINDS
  hideProp, 10 new OPTS. wardrobe_fx_inventory.py BUILT += StatusControl, Cat_grandCasinoArcade, Cat_supportFire,
  WorldParticleCollider (rerun: the Cat 66 / 67 ready). Nothing the video repo reads was renamed.
- **Cues** (wardrobe/fx_cues/cat.json, 49 keys, 218 cues (149 fx, 51 voice, 13 sound, 5 hideProp), 87 effect names (24
  TTO), assembled from the reports' corrected blocks by checks/fx_cat_build/editor/assemble.py + fmt.py, git-ignored):
  the combo (dust, swing sounds, voices; melee hits draw nothing), the charge (damagePlus_ring each tick, the damagePlus
  glow on mount_Hand_R, kill 10, single), the instantCast / gamble / pointTarget / throw1 / throw2 pools (one tile per
  member: Fate Draw with Lady Luck, Double Down's eight coin-flip strikes target / Cat, Life / Skill Gamble with Even
  Odds catching a loss, the ray skills' hits at {d 9.7, y 0.62}, the five throws hiding the R prop), Grand Casino Arcade
  (5 spins at LCK 255, 9 : 8 : 6 : 27 hit pick, Casino Doom's doom at y 0.89), Forward Lunge, Backflip, Heart Ripper /
  Finishing Blow (hits at the standing hero; TTO's finisingBlow1|2 voice), Delta Strike, Moon Blade / Storm, Pillage
  Plunge, Reverse Thrust, Swift Pace, Support Fire (ring + six cannons cut 2.95, builds fire / smoke / hit), the
  effect-only tiles @Awareness:root, @DamageRoulette:root, @TreasureHunt:root (coins 1 m ahead), @EvenOdds:gamble (a
  pool of the two hosts), @NineLives:ko / :getUp (ninelife1|2), emotes, ko (dead roll), getUp (revive at p 0.5), and the
  released TTO tiles royalFlush1 (hand 9, one random suit), crescentEclipse1 / 2 (in place; the dive from {d -5, y
  5.447}), dropAnchor + anchorYank (shrapnel p 0.25). Decisions applied on top of the blocks: 48 (Support Fire's cue
  shapes, no volley / i / fadeOut), 26 (doom y 0.89, not 0.6), 50 (anims, no cut on the machine).
- **Tiles / icons:** wardrobe_skill_icons.py rerun: cat 34 HD icons for 45 clips (18 new webp; index.json cat only).
- **Data:** `wardrobe_fx.py cat`: 63 effects, 71 materials, 78 textures, 126 sounds (the supportFire_hit graft line
  printed); `wardrobe_fx_tto.py cat`: 28 TTO effects, 49 materials, 41 textures, 18 sounds. data/cat/fx.json 91 effects
  (1.4 MB), sfx/ 129 files, 87 new textures in data/fx/tex (one named "deltaStrike _shatter.webp", with the rip's space),
  all new files, to commit with the run; the other PC pulls.
- **Judgement calls (mine):** none beyond decisions.md; where a report's first block and its verification differed, the
  verification's block was taken (crescentEclipse2's dive, supportFire1's 2.95).
- **Gate:** files-only cat (and bat, bison, penguin, sheep, wolf) "no problems"; `wardrobe_fx_check.py ... checks/fx_cat
  dark --cls cat` exit 0, errors [], 43 tile plays, every expected effect spawned; the builders changed shared page /
  fxparts code (mesh.js, alphatimer.js, tto_penguin.js's cel shader, legacyParticles), so also `--cls
  wolf,sheep,penguin,bat,bison` in one run (checks/fx_cat_regress): exit 0, errors [], 211 tile plays; unit tests 65 OK,
  node 8 pass. Not committed.
- **For the QA pass:** in the headless run some tiles' first frame stalls (Crescent Eclipse's first sample after 0 s is
  at 2.69 s, so the takeoff, blades, dive and click were never sampled though they spawned; Royal Flush 1.2 s, Support
  Fire 1.1 s): shader / texture first use under swiftshader, to be looked at with wardrobe_fx_shots.py's virtual clock
  (the blades' HoldWeapon copy with and without a worn weapon, the cards' flip, the shells' arcs and the cannons' fade).
  Doom (p 0.0196 a spin) and the shrapnel (p 0.25) are rolled procs the gate does not expect.
- **QA pass (2026-11-13, the run's Cat QA step).** Shot with `wardrobe_fx_shots.py --jobs` (virtual clock; jobs
  checks/fx_cat_qa/jobs.json, 51 jobs, every Cat tile: Normal Attack, Charge Attack to 11.2 s, Grand Casino Arcade to
  16.6 s (and with Casino Doom forced, `grandCasinoArcade2!casino1`), Support Fire to 5.5 s, Heart Ripper, Finishing Blow,
  the five effect-only / passive tiles (Even Odds with each host), all twelve pool members (Double Down with all eight
  strikes forced on the target, and as rolled; Life / Skill Gamble won and as rolled), backflip, Delta Strike, Forward
  Lunge, Moon Blade, Moon Storm, Pillage Plunge, Reverse Thrust, Swift Pace, the three TTO tiles (Crescent Eclipse also
  with royalDagger worn; Drop Anchor with the shrapnel forced), KO (dead forced, and as rolled), getUp and the emotes with
  voices; the throws with royalDagger worn) on the dark and the white stage, side + front / behind / top: 484 shots
  each. Sheets: checks/fx_cat_qa/sheets_dark, sheets_white (git-ignored; shots and logs under run/). The editor's
  headless stalls are not on the virtual clock: every sample landed at its time, the takeoff, blades, dive and click
  included. Boxes in the hero's frame (+x = her left) match the reports: the combo's dust at 0.1 / 0.7 / 1.7 s (each
  step's cues one frame early, the known seqTick order); the charge's rings at 1.0 / 2.0 / 3.0 s and one glow on her
  hand from 1.0 s to 11.0 s (kill 10); the machine rises at 0.4 s with her on its pedestal, a hit over her head 2.0 s
  into each spin (3.7 ... 14.5 s; Doom forced: the Bat's doom on her at 3.7 s), destroy and sinking from 14.9 s, ring2
  (r 13 m) at 15.2 s; Support Fire's six cannons in their row 2 m behind (x +-7.5), the first shell at 1.23 s, shells
  landing 18-33 m ahead (their hit's extent), the ring and cannons cut at 3.95 s and faded by 4.6 s, shells in flight
  flying on; Heart Ripper's sparks at the hero 1 m up (0.6 / 1.0 s); Finishing Blow's three hits at the hero; the Insight
  mark at 2.04-2.34 m for 3 s; the roulette at 0.63-1.15 m to 10.2 s; Treasure Hunt's coins 1 m ahead, bouncing, gone
  at 1 s; the ray skills' hits round (0, 0.62, 9.7); Two Pair / Copycat at both the Cat and the 10 m point; Double Down's
  strikes at the target or at her; the throws hide the worn dagger 0.4-0.8 s / 0.5-0.95 s and give it back; Delta
  Strike's triangle from 0.5 m ahead with its cats at its far corners (+-4.5, 8); Crescent Eclipse's moon rising, the
  eight blades flung to the 5 m ring, planted, recalled to her at 2.0-2.3 s (the prefab's crescent with no weapon, the
  worn dagger's copy with one), the dive from behind and above at 1.1 s, the land, click and burst; Drop Anchor's anchor
  flying to the 10 m point (slam 0.75 s), the Leash rings (r 7 m) from the landing, the heave at 7.0 s and the smash,
  sink and forced shrapnel at 7.45 s, the anchor gone with them; Royal Flush's five cards dealt, flipped (one suit) and
  gathered over the table at 10 m, the banner, bursts, sword and its hit, all gone by 5 s; KO's deadEffect. No page
  error, no stalled render loop, no failed job in either run (the only console lines: swiftshader's glBlitFramebuffer
  feedback warning). checks/fx_cat_qa/state_probe.py: the charge tile plays once and keeps one glow; Support Fire cut
  by another pick at 2.0 s leaves nothing and fires no more shells; Grand Casino Arcade, Drop Anchor and Support Fire cut
  by a class change leave nothing; errors [].
  - **No bug found in the page, the parts, the cues or the data; no page file changed by the QA.** One tool change:
    `wardrobe_fx_shots.py` gains the force `<cue key>%<effect>` (that effect's chance cues, a `p` with no roll, always
    fire: the shrapnel has no roll name for `!`), and a forced name's `/` is kept out of the shot file name.
  - Looked into, not bugs: the machine's and Double Down's skinned meshes report bind-pose boxes (the machine's y -5.4 ..
    -0.1, the green strike 10 m to her left) while they draw in place; Reverse Thrust's trail lives 0.3 s (its
    EffectControl), so its cut 1.0 never acts; the fortune emblem is a GUI picture (not in the boxes; it shows over her
    head in the shots); Royal Flush's and the burst's Shuriken debris falls through the floor (no collision module).
  - Gates: `wardrobe_fx_check.py ... checks/fx_cat_qa/gate_cat dark --cls cat` exit 0, errors [] (43 tile plays); the
    builders changed shared page / fxparts code, so also `--cls wolf,sheep,penguin,bat,bison` (every other class with
    cues; the other cue files are empty): exit 0, errors [] (211 tile plays); unit tests 65 OK, node 8 pass,
    test_adopt_from_video.ps1 fails 0; `wardrobe_weapon_fx_check.py` OK.
  - For the user's eye: the Insight mark floats about 0.6 m over her ears (the game's own height, decision 27: y 1.3 if
    it reads too high); the target-point effects and Support Fire's far landings sit outside the default camera's
    frame, as for the other classes (not shot with the default camera here); the white stage's faint additive glows;
    the Royal Flush cards' left-to-right order as dealt (Q J 10 K A in the shots); decisions.md's overnight calls
    (listed in the editor's paragraph above).

## 2026-11-13 (overnight, home), the Chameleon's effects: built and cued

From plans/fx_chameleon/ (six reports, each with its "## Verification", which wins; decisions.md decided overnight for
the user's review). One editor after four builders (chameleon, shaders = doubletexture + fxinvisible, tto_chameleon,
page_pipeline).
- **Parts (new):** fxparts/chameleon.js (Chameleon_nAttack: 40 m/s along the spawn turn, life 0.8 s, ends on the floor or,
  with `to`, at the trigger box's contact with the target body; the flying arrow is api.propModel's copy of the worn L
  piece (R with snookerBall; nothing worn: noviceArrow) at Euler(0, 270, 270); clearArrow draws the worn arrow's root
  mesh in the node's FX/Invisible material; `fatal` spawns Fatal Strike's blood (built, not cued: decision 43);
  Chameleon_needlePrison: 16 needles 0.05 s apart, 67.5 degrees, r = `r` 0.6; fx:doubleStrider_left / _right: the clone
  faces `to` on the flat and strafes `strafe` m/s along its right on a 0.02 s step), fxparts/doubletexture.js
  (Self-Illumin/DoubleTexture, the texel squared in gamma space: the builder measured three's piecewise sRGB making the
  spec's linear square up to 7.4/255 too dark), fxparts/fxinvisible.js (FX/Invisible on an effect mesh: the 35 % pass +
  api.shellMaterial's blue rim), fxparts/tto_chameleon.js (ChameleonLightning, ChameleonAfterimage + TTO/ChameleonSpirit
  with its depth prepass, the ghost hooks fx:tto/venomPhantom_coil / _beam / _rupture, ChameleonPreyReticle with
  `release`, the Chameleon.ApexArrow mover). index.html (the page_pipeline builder): api.propModel, api.shellMaterial,
  HERO_SKINS FX/Blend, FX/Invisible (ghost drawn first) and Chameleon.StormDarken, hideProp "hero" / `all` / no kill
  (until the next pick), cue `life` and `stop`, the P8 cut at a step change (only effects of the ending step whose cut is
  not past that step: the Bison's trample2, the Cat's supportFire_ring and the Sheep's holylight_ring, whose cuts are
  written in a later step's clock, keep their old timing), LIFTS.apexHunt, SEQ / SEQ_SKILL / NEVER_PLAYED chameleon
  (focusFire1 / 2 hidden), FX_PART_FILES += chameleon, doubletexture, fxinvisible, tto_chameleon; moveSkillIcons: a
  SEQ_SKILL skill shows on its own tile only (as a pool member does), so Critical Plus' and Clear Arrow's icons stay off
  the Normal Attack tile. SEQ chameleon gains "Normal Attack: nAttack1" (a clip used by a visible sequence leaves the
  ท่าสกิล list, so without it the tile would vanish; as a one-step sequence it plays once and repeats with วนซ้ำ; its cue
  key stays the plain nAttack1). bat.js: fx:castRing lets the Chameleon through. wardrobe_fx.py: LAYOUTS
  Chameleon_campFire / _needlePrison / _nAttack; graft_by_material for SHURIKEN_FROM_TTO.chameleon = thunderDragon_ring2,
  zeroShot_ring (matched by node name and BB's first PSR material, BB's materials kept; the Bison's magmaClutter_ring2 and
  the Cat's supportFire_hit probed byte-identical to their committed data, not rebuilt). wardrobe_fx_tto.py: _ScaleTex
  saved as scaleTex, SKILL_FX.chameleon (31), CODE_MOVERS apexHunt_arrow. wardrobe_fx_check.py: hideProp "hero", optional
  kill, `all`, 19 new OPTS. wardrobe_fx_inventory.py BUILT += Chameleon_nAttack / _needlePrison / _campFire (the Chameleon
  55 / 57 ready; the 2 left are the grafted ParticleSystems, noted as drawn). Nothing the video repo reads was renamed.
- **Cues** (wardrobe/fx_cues/chameleon.json, 51 keys, 336 cues: 204 fx, 57 sound, 40 voice, 27 hideProp, 7 skin, 1 lift;
  86 effect names, 24 of them TTO; assembled from the reports' blocks by checks/fx_chameleon_build/editor/make_cues.py,
  git-ignored): the Combo shot (the worn arrow to the 10 m ground point, hit at 0.4281 s, the hand arrow hidden 0.2-1.8 s,
  bow_fire1 / plunger with the Plunger Bow, Critical Plus' 20 % roll), its own tiles @CriticalPlus:nAttack1 (the crit on
  every play) and @ClearArrow:nAttack1 (the FX/Invisible look and the hidden hand arrow until the next pick, clearArrow in
  place of nAttack), Charge Attack (blend + FX/Blend 9 s, rings each second, the full ring at 8 s cut 8.95, 18 volley
  fires, cAttack4 at 3.4 s), Silent Walk (FX/Blend 1.6 s), the cast channel (castRing cut 0.35, the hand arrow hidden until
  the next pick) and its five pool members (True / Mass Invisibility with the FX/Invisible look 0.2 s after the puff,
  Final Entrapment's cage life 7, Camp Fire 2 m ahead kill 10, Mark of Slayer), Tent, Immunity (y 1.16, scale 0.7), Venom
  Shock, Blood Burn, Rusty Decay, Perfect Blend, Needle Prison (kill 5, builds needlePrison_arrow), Mass Shot, Fatal
  Strike (both hands, kill 10), Left Stride (five hero + five clone arrows, hits at the box contact), Quick Fire (18
  shots, hits {d 9.7, y 0.63}), Poison Volley, Torment Rain (the cage it needs from 0, the rain at 2.0 s; TTO's
  tormenrRain1|2 voice), Right Stride (the clone at -5.02 m/s, its shots from skills_b Verification 4's table), Slayer x 4
  and All Slayer x 4 (one tile per member; TTO's unnumbered All Slayer voices), All Slain, Skin Shift, Zero Shot, Thunder
  Dragon (the whole hero hidden 0.6-3.8 s), the emotes, run's footsteps (everyCycle), KO (deadEffect p 0.5); TTO
  (released): Venom Phantom (five ghosts at the GhostSlots, five beams, the rupture shattering them; builds ghostFire /
  ghostShatter), Apex Hunt (lifted along the 4.5 m jump, decision 34), Chain Lightning (StormDarken, the tail to 12.05 s).
  Applied on top of the blocks: every hand-arrow hideProp is "L" with `all: true` (decision 48; skills_b's "R" turned
  round, its whys now say slot L); Needle Prison's `radius` written as `r` (decision 56); Right Stride's why says 5.02 m/s.
- **Tiles / icons:** wardrobe_skill_icons.py rerun: chameleon 41 HD icons for 66 clips (23 new webp; index.json
  chameleon only).
- **Data:** `wardrobe_fx_tto.py chameleon`: 31 TTO effects, 18 materials, 13 textures (two "written by name only"
  warnings for the ghost's fire / shatter references: those come in through SKILL_FX); `wardrobe_fx.py chameleon`: 62
  effects, 74 materials, 70 textures, 112 sounds (five graft lines printed). data/chameleon/fx.json 93 effects (2.6 MB),
  sfx/ 112 files, 54 new textures in data/fx/tex: all new files, to commit with the run; the other PC pulls.
- **Judgement calls (mine):** the tto_chameleon builder's preyFx kill 2.15, not 2.05 (the reticle's 0.1 s hold before
  its 0.25 s fade, ChameleonPreyReticle Update@0x1C4EF10); the thunderDragon2 entry kept with no cues (it records the
  clip's timeline); Clear Arrow's tile with no `invisible` puff (the status is its precondition, not cast there). The
  builders' calls kept: Fatal Strike's blood at maxY 0.8 with no root mesh (Chameleon_nAttack.cs:241), riding the
  projectile root.
- **Gate:** files-only chameleon and every class with cues "no problems"; `wardrobe_fx_check.py ... checks/fx_chameleon
  dark --cls chameleon` exit 0, errors [], 46 tile plays, every expected effect spawned (the sleep emote's voice key is
  routed by the checker to the Tent tile, which plays sleep with @Tent:sleep: the emote's own play is not sampled); unit
  tests 65 OK, node 8 pass, node --check on the four new part files and bat.js. The page code and fxparts changed for every class (P8 cut, hideProp, shellMaterial, bat.js), so also `--cls wolf,sheep,penguin,bat,bison,cat` in one run (checks/fx_chameleon_regress): exit 0, errors [], 254 tile plays. Not committed.
- **For the QA pass:** no screenshot has been looked at yet for the new shaders (DoubleTexture, FX/Invisible on a mesh,
  TTO/ChameleonSpirit, the shells; the gate saw no console error, so they compiled); the arrow copy's turn in flight, the
  needles' fall, the clone's path, the ghosts' slots and the lifted Apex Hunt want wardrobe_fx_shots.py's virtual clock.
  Rolled procs the gate does not expect: Critical Plus' crits (p 0.2), KO's deadEffect (p 0.5).
- **For the Bible (offer, not written):** decisions.md's last section; also, from the builders: with the Snooker set the
  flying copy is the ball while the hand's cue is hidden; Clear Arrow never carries Fatal Strike's blood.
- **QA pass (2026-11-13, the run's Chameleon QA step).** Shot with `wardrobe_fx_shots.py --jobs` (virtual clock; jobs
  checks/fx_chameleon_qa/jobs.json, 57 jobs, every Chameleon tile: Normal Attack (nothing worn: the starter arrow; Cupid,
  Plunger and the Snooker set worn), Critical Plus, Clear Arrow (bare and with Cupid), Charge Attack to 14.5 s, Silent Walk,
  the five cast pool members, Tent, Immunity, Venom Shock, Blood Burn, Rusty Decay, Perfect Blend, Needle Prison, Mass
  Shot, Fatal Strike, Left / Right Stride (side, behind, top), Quick Fire, Poison Volley, Torment Rain, the four Slayer
  and four All Slayer members, All Slain, Skin Shift, Zero Shot, Thunder Dragon (bare and with Cupid), the three TTO
  tiles (Venom Phantom with side, behind and front views, Apex Hunt from the side and far, Chain Lightning to 12.8 s,
  with and without Cupid), KO (dead forced, and as rolled), the six emotes with voices and run) on the dark and the
  white stage: 639 shots each. Sheets: checks/fx_chameleon_qa/sheets_dark, sheets_white (git-ignored; shots and logs
  under run/). No page error, no stalled render loop, no failed job (the only console lines: swiftshader's
  glBlitFramebuffer feedback warning). Boxes in the hero's frame (+x = her left) match the reports: the Combo arrow from
  (0, 1.5, 1) to the 10 m ground point, tip first (the starter noviceArrow, the worn arrow, the Snooker ball, the plunger
  head first), the hand arrow hidden from 0.2 s; nAttack_hit at 0.43 s at (0, 0, 10); Clear Arrow's FX/Invisible hero
  and arrow; the charge's FX/Blend 0.8-9.8 s, a ring each second, the full ring at 8.8 s, the volley fans from 9.8 s and
  cAttack4's at 13.2 s; the castRing cut into its 0.5 s shrink at 0.4 s (the same age-60 jump as the Bat's); the
  invisible puff at 0.8 s and the FX/Invisible look from 1.0 s, kept (props too, the hand arrow hidden); the Final
  Entrapment cage at the 10 m target to 7.8 s (life 7); Camp Fire 2 m ahead to 10.8 s; the Tent at 0.8 s, the heal at 1.3 s;
  Immunity's cross at y 1.16 to 10.2 s; the detonations at the target; the 16 needles falling one every 0.05 s onto
  their ring at the target, standing point down to 5.8 s; Fatal Strike's blood on both hands to 10.3 s; the Double
  Strider clone strafing round the target (Left Stride to her right, Right Stride to her left; gone at the 2.3 s cut),
  every shot at its table spot and flying to the target; Quick Fire's 18 flashes at (0, 0.63, 9.7); the Torment Rain cage
  from 0 and the rain at 2.0 s; Thunder Dragon hiding the hero and her props 0.6-3.8 s; the five Venom Phantom ghosts at
  their slots (x +-1.5 / +-2.8 / 0, her right first), aiming, the five beams from their bow points to the target at 1.95
  s, the rupture and the shatters at 2.07 s; Apex Hunt's crouch, the lift (the takeoff and the reticle stay on the
  ground, the hang rides her), the arrow and the impact at the target at 2.47 s, the land at 2.75 s; Chain Lightning's
  darkened hero to 8.0 s, back by 8.6 s, staticDrainFx 8.05-12.05 s; KO's deadEffect.
  - **Bug found and fixed (index.html, shared Fx code):** a child node's own EffectControl velocity was never applied
    (the page's comment said "Not done"), so the falling bolts of All Slain (allSlain_bolt, -48 m/s), the four All
    Slayer hits (allSlayer_bolt, -24 m/s) and Thunder Dragon's thunderDragon_ring1 (thunderBolt, -48 m/s) hung 12-36 m
    up and never struck (All Slain's and the dragon's out of every default view). Now Fx applies it as the game does
    (EffectControl.cs:71-73: TransformDirection by the child's own world turn at the spawn; :167-173: position +=
    velocity x dt every frame, life and after-life), put back into the parent's space. Those bolts end under the floor,
    which the game's ground hides and the page cannot (the camera may orbit below): every mesh under such a moving child
    gets its own copy of its material (fxMaterial's shader hooks copied: clone() leaves them out) clipped at the hero's
    ground (`renderer.localClippingEnabled = true`, freed with the effect). The only other such child in the data is the
    **Wolf's dualBrand_slash3 vortex** ((0, 12, 0) under a 90-degree turn): it now flies ahead at 12 m/s (about 4 m by
    0.27 s), as the game's code says: **for the user's eye**. Shots: checks/fx_chameleon_qa/bolts_fixed3.png,
    wolf_vortex.png.
  - Looked into, not bugs: the needles' boxes read flat (the box script turns only two corners) while they stand;
    massHouseShot draws nothing until 0.6 s (its rain's own 0.4-0.6 s delay); Skin Shift's decoy is the prefab's static
    chameleon mesh (life 1 + after-life 1); bugSlayer_fire's streaks fly back past her (the prefab's own particles);
    staticDrainFx is faint by design (a 0.08 s arc every 0.5 s, a few sparks and smoke); the long apexHunt_arrow trail
    behind the hand at its spawn; allSlayer_ring cut at 0.65 s (cued so, not the game's 0.8 s: the step edge, as
    castRing's).
  - Gates: `wardrobe_fx_check.py ... checks/fx_chameleon_qa/gate_chameleon2 dark --cls chameleon` exit 0, errors []
    (46 tile plays, on the final code); the page's Fx code changed (and the builders' shared code), so also `--cls
    wolf,sheep,penguin,bat,bison,cat` (every other class with cues; mole, monkey, panda, rabbit, whale are empty):
    exit 0, errors [] (254 tile plays); unit tests 65 OK, node 8 pass, test_adopt_from_video.ps1 fails 0;
    `wardrobe_weapon_fx_check.py` OK. Not committed.
  - For the user's eye: the Wolf vortex above; the dragon skeleton's DoubleTexture reads dark teal inside its green glow
    (checks/fx_chameleon_qa/skeleton_near.png); the Venom Phantom ghosts are pale grey-white with green on the white
    stage; the target-point effects sit outside the default camera's frame, as for the other classes; decisions.md's
    overnight calls and the editor's judgement calls above.
## 2026-11-13 (office), ชื่อผลงาน on the send form

User: "when players are submitting the skins, add another text box field, ชื่อผลงาน" then "queue it and deploy this
feature ASAP". Optional (my call: a required field would refuse looks sent the old way and adds friction; say so if it
should be required), up to 60 characters, one plain line (the Worker's `clean`).
- Page: the form's first field `ชื่อผลงาน (ไม่บังคับ)` (focused on open; not remembered in the browser, unlike the name and
  link), sent as `title`; the consent line names it; the ลายผู้เล่น cards (sets and single pieces) show it above
  "ลายโดย <name>" (`.gal-title`, the credit line then muted).
- Worker (site_worker.mjs): LIMITS.title 60; meta.title (always, "" when empty); the Discord message's field ชื่อผลงาน and
  its embed title "<title> · ..."; the live list carries `title` only when set. Import (wardrobe_community.py): community.json
  sets keep `title` when set. Tests: node 9 pass (one new), unit tests 66 OK (one new).
- Deployed from a clean worktree of 578705e (C:\work\12tails-wardrobe-hotfix, branch title-field), because the Mole
  build was editing index.html in the main folder at the time; the same edits were made there too.
## 2026-11-13 (office), the team's sets taken down (the user re-uploads them)

User: "take down, DeetaeZ, rabbit and cat skins from the public site, I will try uploading them myself using the new
pipeline" then "compile them on desktop". wardrobe/data/team_sets.json now holds no sets and data/team/ is gone (the
Cat knight, Rabbit summer uniforms A and B, DeetaeZ's Whale legend set: every set it had), locally and online. Re-running
`pipeline/wardrobe_team_sets.py` would write them back: don't, unless the user asks. The original PNGs (the sources in the
git-ignored plans/reskins/, checked against the published webp: same sizes, mean difference under 1/255) were copied to
the office PC's Desktop `wardrobe_reupload\<set>\12tails_<class in Thai>_<item>.png`, the names the page's drag-and-drop
reads (dropMany), one folder per look (the Cat knight's folder name carries its face, 23). Published and deployed from a
clean worktree again (the Mole build was editing index.html).

## 2026-11-13 (office), the run resumed: Mole build, then Monkey, Panda, Rabbit, Whale

User: "goal prompt to finish what we started" (plans/goal_fx_all_classes.md, rewritten for either PC: gate from the repo
root, deploy paths `<repo>`, usage guard back at CLAUDE.md's 98 %). The workflow is now in the repo:
`pipeline/workflow_class_fx.js` (run it with the Workflow tool's scriptPath; args `{mode: "research", cls, Cls, released,
skillClips, ttoClips, ttoEmotes}` or `{mode: "build", cls, Cls, released, regress, groups?}`: without `groups` a planner
writes decisions.md and splits the builders; office paths are written into it, change REPO / ENV for the home PC).
- Mole build: the planner skipped (its decisions.md exists); four builders from parts.md "Who builds what" + decisions.md:
  mole (fxparts/mole.js), robots (fxparts/rotationcontrol.js + the summons in a new fxparts/robots.js: my call, parts.md
  gave the summons to no agent), tto_mole (fxparts/tto_mole.js), page_pipeline (index.html, wardrobe_fx.py,
  wardrobe_fx_tto.py); then the editor and the QA. The home PC's research probes (checks/fx_mole_research/) are not
  here: the builders re-probe.
- Monkey research runs beside it (released TTO: buitenBastion, golemCall, jaAscension, solarCall; sanctumRaise is TTO
  but not released: researched, not cued).
- Progress: Monkey research committed (4e8bdb6), Panda research committed (074e4d4; its effect_only found the "&" clip
  filter: HANDOFF, home PC), Rabbit research running; the Mole built, its gates passed (editor + QA sections below),
  committed (48d52d6) and deployed (version 9c8368b1, data-afb354ae09; published from a worktree of 48d52d6 plus the
  other session's live opaque-outfit patch, so its deploy was not undone; the Monkey build was starting in this folder).
  Rabbit research committed (07546c0; skills_b saved from the journal: its Write was refused, "Subagents should return
  findings as text", and its checker, which ran before the file existed, was run again on its own). Whale research
  committed (d7ff8ff; the same for its skills_a). The Monkey built (planner + monkey / elementals / tto_monkey /
  page_pipeline builders, editor, QA): gates passed, committed and deployed (its section below). The other session
  committed its opaque change to main itself (1dd61cc), so the Monkey commit needed no index.html split, only NOTES.md.
- Another session worked in this folder at the same time (reskins; outfits opaque, which touches index.html). Its
  uncommitted files are left to it: the Mole commit stages index.html without its 24 lines (its own worktree's diff
  reversed out of a copy, the copy staged with `git update-index --cacheinfo`) and NOTES.md without its three sections;
  never `git add -A` here while another session has work in the tree.

- **Bug (user: "Check the deployed Monkey, it is missing a lot of faces"):** every publish from a git worktree at the
  office dropped the Monkey's 23 BB faces (0-22; only TTO's 23-32 online) with "check: no problems": the office rip's
  52 Monkey PNGs are zero-filled and the publish repairs them from wardrobe/data/bb_rip_fix/ (BBRip.usable), which is
  git-ignored, so a fresh worktree has none. Since this morning's ชื่อผลงาน / takedown deploys (mine, worktrees) and the
  other session's d4adea35. Fixed: `usable()` now raises BBDataError when a rip file can't be read and the bb_rip_fix
  folder is missing (test: test_unreadable_rip_file_without_bb_rip_fix_stops_the_publish); a worktree publish needs
  `New-Item -ItemType Junction <worktree>\wardrobe\data\bb_rip_fix -Target <main>\wardrobe\data\bb_rip_fix`.
  Also found: the other session's d4adea35 (10:29, built from 074e4d4) had replaced my Mole deploy 9c8368b1 (10:22),
  so the Mole was offline until the Monkey's deploy. Both wardrobe peer sessions were told (SendMessage).
  The Monkey and the Mole went live together in version 59b73956 (data-c4c13d8692, from a worktree of c8ea0e2 with
  bb_rip_fix linked in): every class 33 faces, the Monkey's 23 outfit colours and 2 outfits back too; checked live
  headless (no 404, no page error).
- The Panda built (planner + two builders: tto_panda, page_pipeline; editor; QA, which added the `floor` clip for the
  two dragons under the ground): gates passed, committed and deployed (its section below). Its editor also fixed the
  "&" in wardrobe_data.py's clip filter; the data rebuild is the home PC's (HANDOFF).
  Panda live: version 462c24e7 (data-7360b42ed2; a worktree of a2506ba with bb_rip_fix linked in; every class 33 faces).
- The Rabbit built (planner + rabbit / generic / page_pipeline builders, editor, QA: no bugs found): gates passed,
  committed and deployed (its section below).

## 2026-11-13 (office), the Whale after a reference picture (the `reskin-from-image` skill)

User: "restrict your access to knowledge regarding the reference characters ... just follow what you see in the
reference image" -> the project skill `.claude/skills/reskin-from-image/` (`/reskin-from-image`; .gitignore lets
`.claude/skills/` through, nothing else of `.claude`), a line in CLAUDE.md, a memory. Then: "Whale skin, pick the best
equipment set for this ref image and build the texture" ("any set equipment candidates except student skins from ToT").
The picture as seen: big purple curls under a small red and gold crown, a wide grin (a wall of teeth, dark purple lips),
teal eyeshadow and spiked lashes, tan skin, a crimson leotard cut to a deep V with a high pointed collar, a dark
skull-over-crossed-bars mark on the bare chest, pearls, magenta gloves and boots, a white net cape, net stockings with
black garters. Notes and files describe the picture only, never who it is.
- `pipeline/wardrobe_whale_crown.py --paint [--debug] [--noshots] [--darkmouth]` -> plans/reskins/whale/ (crown/
  superStar.png 2048 px, crown/Wolf_fanKingHat.png, crown/Wolf_afro.png, shots, crown_compare.png, crown.html; not
  committed until the user picks; reference.png is the user's, not for git). `_cache/maps4.npz` = the texel maps kept
  between runs (a pass is ~1 min with it).
- **Base: superStar** (of the Whale's 22; sheet.png): the open coat = the cape, the fur collar + lapels = the high
  collar, the banknote necklace = the pearls (two round pearls per note, alpha 0 round them; the gold chain and coin
  alpha 0), the shirt panel = the bare chest, the mark and the leotard's V. **Head: fanKingHat** (a red and gold crown
  as it is; its blue / green gems painted white) with the curls painted on the Whale's own dome; **afro** in the hair's
  purple is the alternative (one head piece at a time; the Whale wears the Wolf's files: skin keys
  `whale|accessories|fanKingHat|Wolf_fanKingHat.png`, `whale|accessories|afro|Wolf_afro.png`). Face 13 (BB's).
- The Whale's sheet (512 px; body 2.5 tall, x front, y left, z up): the dome is two islands (front, back) + the fin;
  its rim over the mouth z 2.05 (middle) to 1.69 (corners); the **eyes sit at the mouth's corners** (|y| 0.6, z 2.0, on
  the dome's sides), so the face is a band of skin over the mouth and the rest of the dome is hair. Each tooth is its
  own island; the lower jaw (z 1.32-1.82) is one island; the face overlay is the sheet's top-left quarter (only the
  eyes are opaque). Coat, sleeves and legs are mirrored; the panel is not. The coat has **no body under it** and the
  material is front-sided: holes all over the coat showed a hollow Whale from the side and behind, so the net is painted
  over grey (as the reference's cape reads) and real holes (alpha 0, the material's alphaTest) open only from z 0.86
  down to the hem, where the legs are behind.
- What the painter does: curls = cells round ~87 scattered points on the dome in 3D (they cross the seams), looked up
  through a smooth noise (no honeycomb), each a puff with a spiral line; the hairline follows the curls; lips = the 3D
  distance to the mouth's rim (the island's boundary where x > 0.385); eyeshadow and lashes in a frame on the skin at
  each eye (found from the face preset's alpha); the mouth's inside painted as more teeth (off-white, dark lines) so the
  gaps between the Whale's teeth close into the reference's grin.
- Invented (the picture does not show them): the back (curls all over, the net cape, a crimson seat), the Whale's tail
  (skin), the soles. Not possible on this mesh: the hair's width past the dome (the afro adds some), the collar's
  points, long legs for the stockings (they are 0.3 tall here), a single strand of pearls (the notes' side strands hang
  down as pearls too).
- `wardrobe_outfit_sheet.py` gained `--props Head:afro Back:glasses ... [--on <outfit>]` (each prop alone on one outfit);
  `wardrobe_skin_live.html` gained `&head=<piece>`:
  http://127.0.0.1:8771/pipeline/wardrobe_skin_live.html?cls=whale&outfit=superStar&face=13&head=fanKingHat&skin=/plans/reskins/whale/crown/superStar.png
- Next, if the user picks it: add to `wardrobe_team_sets.py` (as the Cat knight), publish, deploy.

## 2026-11-13 (office), the Mole's effects: built and cued

From plans/fx_mole/ (six reports, each with its "## Verification", which wins; decisions.md decided overnight for the
user's review). One editor after four builders (mole, robots, tto_mole, page_pipeline), on the office PC.
- **Parts (new):** fxparts/mole.js (the six shells Mole_nAttack / _mortarShot / _stunGrenade / _grenadeCluster / _napalm /
  _bazooka on the 0.02 s step, their hits part-spawned on the floor or the standard target body, `firePoint` = the worn
  cannon's muzzle re-aimed at `to`, Grenade Cluster's `tilt`; Mole_missile / Mole_warMissile homing, BB and TTO in one
  part, the TTO pairs' twinImpact and the egg's eight-way splits; Mole_cartBomb (still 0.2 s, 6 m/s, stops at 9.2 m, boom
  at 3 s); Mole_timeNuke's countdown (GMO24 digits in a 30 x 30 px sprite 1 m over the nuke, the ink centred) and its
  detonate(); fx:detonate; Mole_warCapital (open, root from 1 s); fx:flameCarnival (`trigger`, never cued); the mines and
  Flame Carnival data only), fxparts/rotationcontrol.js (rotationControl, generic: also the Monkey's lavu),
  fxparts/robots.js (AutoGyroGun's AI shots at `to` 2 / 4 / 6 / 8 s, BarrelBot standing, KingKaiser's create / root and
  the `clip` option, the host of `"host": "KingKaiser"`), fxparts/tto_mole.js (the rail turret, gun, beam, arcs, shocks,
  trench, overload, the launch pad with `launch`, the lock reticle, the arsenal pods, the Kaiser's warheads). index.html
  (page_pipeline): SEQ / SEQ_SKILL / NEVER_PLAYED mole, the SEQ token `>t` (a step's clip from t s in), cycle pools
  (`"order": "cycle"`, member `standby`, FX.counters), member `name`, LIFTS.barrelRailgun (3-axis; effects spawned during
  it placed from her spot before the lift), cue options tune / pick "color" / host + bone / playAudio / clip / rot
  "randomYaw", the propAnim kind, api.fontText / api.propPoint, FX_PART_FILES += mole, rotationcontrol, robots, tto_mole.
  wardrobe_fx.py: the Mole LAYOUTS + the robots' (new string type "s"), EXTRA_FOLDERS (Characters/Robots), field prefabs
  (kaiser_dust, kaiser_box, autoGyroGun_fire) and the robots' AudioClip fields as sounds (SOUND_REFS: autoGyroGun_create,
  kingKaiser_kaiser_create ...), the clip reader's AnimationEvents, HERO_CLIPS (kaiserArsenal added to every
  KingKaiser_<c>'s Animation), the GMO24 font (fx.json `"fonts"`, data/fx/tex/GMO24.webp), sounds found as .ogg and in
  the rip's Assets/AudioClip (every class, only where a name was missing before), SHURIKEN_FROM_TTO bazooka_ring /
  napalm_ring / warCapital. wardrobe_fx_tto.py: SKILL_FX mole (24), arcPrefab references resolved, TTO Animations written
  (barrelRailgun_rip's root; no other class's TTO data has one). Nothing the video repo reads was renamed.
- **Editor fixes (found by the gate):**
  - **A NaN in fx.json:** warCapital's mesh has 18 NaN normals; Python wrote `NaN`, the page's JSON.parse refused the whole
    8 MB file and `fxData` swallowed the error, so every Mole effect read "not in fx.json". wardrobe_fx_mesh.r5 now writes
    0 for a NaN (those vertices' normals are 0: for the QA's eye on War Capital), both builders dump with
    `allow_nan=False`, and index.html's fxData says `console.error("effects data", cls, e)` instead of swallowing it (the
    gate fails on that line from now on). No other class's fx.json had a NaN.
  - **Mole_missile's clock:** the turns ran once per frame, so the headless gate's 3.9 s first frame flew every TTO missile
    straight into the floor and no pair ever blasted (twinImpact never spawned); the clock and the 0.2 s turns now run on
    the 0.02 s physics steps (fxparts/mole.js; the same flight at the page's frame rates, checked with
    wardrobe_fx_shots.py's virtual clock before and after). KaiserWarhead (tto_mole.js) still turns on the frame clock (its
    hits spawned in the gate): for the QA's eye on a slow PC.
  - **robots.js** played `kaiser_create`, but the export names it `kingKaiser_kaiser_create`: the parts now read the comps'
    own fields (create_fx, nAttack_fx, kaiser_createFx), the SFX names the fallback.
- **Cues** (wardrobe/fx_cues/mole.json, 56 keys, 351 cues: 224 fx, 62 voice, 59 sound, 3 hideProp, 2 propAnim, 1 lift;
  103 effect names (cued + builds), 23 of them TTO; assembled by checks/fx_mole_build/editor/assemble.py, git-ignored,
  from the reports' corrected blocks): attacks_emotes' (the Combo's five shells with firePoint / tune / Double Cannon,
  superDig per its Verification, dig2's mounds, the plain surfacing, Sky Drill, the emotes, KO), skills_a's (Advance
  Repair, the Assemble pool, War Capital, Barrel Cannon, Bunker, Chopper with playAudio, Detonate, King Kaiser, Flame
  Turret), skills_b's (the mine, mortarShot, punch and tnt pools, grenade, grenadeCluster, hammer, missile, War Factory),
  effect_only's four, tto's three. Applied on top: decision 43 (propAnim R fire at each Normal Attack shot), 19
  (firePoint + `to` on Mortar Shot, the five Napalm shells with their own aims, Stun Grenade), 12 (TNT 1-4 named "TNT n"),
  13 (War Factory's standby per member), 45 (dig1's dust on the nominal 0.1 ... 1.8 s), 35 / 36 (the Kaiser by colour,
  the hideProp), 32 (the Auto Gyro Gun's builds), 27 (Detonate: timeNuke2 kill 3, the cued explosion dropped, builds
  timeNuke_explosion), 40 (the lift on @BarrelRailgun:assemble1), 22 / 41 (missilePad: the pad's `launch: true` makes the
  launches, the eight missiles (pair 2j / 2j + 1) and the 5 % egg; the cued launch / missile / hit / blast cues gone), 37
  (Kaiser Arsenal: the Kaiser at 0 with `clip`, the hideProp 4.4 s, the pods' `host`), the overload's kill dropped (its
  part ends it), skills_b's five tnt `why` fixes, tto/barrelRailgun_arc in the builds of the three lock entries.
- **Tiles / icons:** wardrobe_skill_icons.py CLIP_SKILLS mole (decision 14, + missilePad = missile + twinWarhead),
  RANK_ICONS (new: tnt1-4 with their own rank icons), EFFECT_ONLY mole, OWN_TILE mole (warCapital; cAttack on superDig for
  the Charge Attack's HD icon), cycle pools skipped; rerun: mole 38 HD icons for 47 clips (index.json mole only).
- **Data:** `wardrobe_fx_tto.py mole`: 24 TTO effects, 30 materials, 27 textures, 4 sounds; `wardrobe_fx.py mole`: 80
  effects, 85 materials, 82 textures, 125 sounds (the three graft lines printed). data/mole/fx.json 104 effects (8.1 MB:
  the robots' meshes and clips; the largest class file), sfx/ 128 files, 76 new textures in data/fx/tex (GMO24.webp
  among them): all new files, to commit with the run; the other PC pulls. wardrobe_fx_inventory.py BUILT += the 20 Mole
  parts + CharacterControl (data only, NOT_DRAWN), NOTES (the three grafts), CLASS_NOTES mole (the field prefabs); rerun:
  the Mole 75 / 78 ready (the 3 left are the grafted ParticleSystems, drawn).
- **Judgement calls (mine):** the missile pad as the tto_mole builder built it (`launch: true`, the egg rolled by the pad)
  rather than the mole builder's cued launches with `pair` (one owner for the launch spots: the pad's real muzzles);
  tto/missileBot_fire_bot left out of the entry's builds (made only on the 5 % egg, so the gate would fail 95 % of plays;
  SKILL_FX builds it, it is in fx.json); the robot sounds in builds by their exported names (`sound:kingKaiser_kaiser_create`
  ...) so the files check sees them; Landmine's tile named "Landmine" (the Bible's card), as TNT's; no icon for Kaiser
  Arsenal (the Bible has none of its own; King Kaiser's is a SEQ_SKILL skill, which moveSkillIcons keeps to its own tile);
  wardrobe_fx_check.py plays a cycle pool's tile once per member, each play expecting that member's cues, KINDS += propAnim,
  OPTS += decision 59's 17 + launch, egg, ENTRY_KEYS += order, SKILL_KEYS += standby, name.
- **Gate:** files-only (every class with cues) "no problems"; `wardrobe_fx_check.py ... checks/fx_mole dark --cls mole`
  exit 0, errors [], 60 tile plays (War Factory five times), every expected effect spawned (the shells' and missiles'
  part-made hits, autoGyroGun_fire, timeNuke_explosion, the four twinImpacts, the arsenal's warheads and hits);
  the page, the fxparts and the builders changed shared code, so also `--cls wolf,sheep,penguin,bat,bison,cat,chameleon` in one run (checks/fx_mole_regress): exit 0, errors [], 300 tile plays; unit tests 66 OK, node 9 pass, test_adopt_from_video.ps1 fails 0; `wardrobe_weapon_fx_check.py` OK. Not committed.
- **For the QA pass:** nothing has been looked at in a screenshot yet: the Time Nuke's countdown (GMO24 digits, ink
  centring, 60 ... 51), the Kaiser in each colour and in Kaiser Arsenal (the pods on its arms, BB's Kaiser material on
  TTO's pod meshes), the rail turret's assembly, ride and lift (the Mole on the seat), the shells from a worn cannon's
  firePoint (and Double Cannon's two), Grenade Cluster's tilts, the cart stopping at 9.2 m, the Auto Gyro Gun's leg1 aim,
  War Capital's zeroed normals, the egg's 64 splits (forced: they land 4-5 m round the target by the builder's physics,
  untested against the game), the Mortar / Napalm lobs landing 4-5 s in (the idle tail), the Trumpet's tune, propAnim on a
  cannon with a fire clip, the 8.1 MB fx.json's load time. Headless first-frame stalls (missilePad's first sample at
  3.95 s) want wardrobe_fx_shots.py's virtual clock (it showed the four twinImpacts at 2.6-3.6 s). Rolled procs the gate
  does not expect: KO's deadEffect, the egg.
- **For the Bible (offer, not written):** decisions.md's last section; also, from the builders: the Auto Gyro Gun fires
  2 s after it stands, then every 2 s (the 2 s nAttack lock); the King Kaiser's footsteps are events on its run clip only;
  the robots' sounds are AudioClips outside Resources; the egg's split missiles mostly miss a 10 m target (a 0.3 rad per
  0.2 s turn at 8 m/s cannot curve back), untested against the game.
- **QA pass (13/11/2026, office).** Shot with `wardrobe_fx_shots.py --jobs` (virtual clock; jobs
  checks/fx_mole_qa/jobs.json, 64 jobs, every Mole tile: Normal Attack bare, with Double Cannon, royalCannon (a firePoint),
  capitalCannon (fire + root clips) and the Trumpet; Charge Attack; Sky Drill; Auto Gyro Gun / Barrel Bot to 10.4 s; War
  Capital to 18.3 s; Bunker; Flame Turret; King Kaiser to 15.3 s and in each of the five colours; Reload, Fire Barrage,
  Bombardment, Synchro Mole; the four mines (Time Nuke close up); Mortar Shot and Napalm (also with royalCannon); Mega
  Punch / Drill; TNT 1-4; Advance Repair, Barrel Cannon, Chopper, Detonate, Grenade (also royalCannon), Grenade Cluster,
  Hammer, Missile (to 5.7 s); War Factory forced to each of its five weapons and once as cycled; Barrel Railgun to 17.6 s;
  Kaiser Arsenal; Missile Pad as rolled and with the egg forced; KO (dead forced, and as rolled), getUp, emotes, run) on
  the dark and the white stage: 719 / 740 shots. Sheets: checks/fx_mole_qa/sheets_dark, sheets_white (git-ignored; shots
  and logs under run/). No page error, no stalled render loop, no failed job (the only console line: swiftshader's
  glBlitFramebuffer feedback warning).
  - What matches (boxes in the hero's frame, +x = her left): the Combo's five shells from (0.2, 1, 0.6) (Unity), hitting
    the body's front at 9.4-9.8 m 0.62 s after each shot (0.95 / 1.45 / 1.95 / 2.45 / 2.95 s); Double Cannon's two shells
    -+0.3 m and +-9 deg, two hits each stage; royalCannon's shell (and Stun Grenade's) leaving its muzzle; the burrow
    (dig_hole, superDig_dust at 0.1 / 0.3 / 0.5 s, the hero hidden 0.6-3.0 s, dig2's mounds every 0.2 s, the surfacing
    dust at 3.0 s); Sky Drill's drill and rings at 3.01 s; the Auto Gyro Gun from 0.63 s 0.7 m ahead, its tracer to the
    target 2 s after it stands, gone at 10.63 s; Barrel Bot standing to 10.6 s; War Capital at 8.53 s 2 m ahead, opened,
    to 18.5 s (its zeroed normals light normally); King Kaiser: dig1's dust, kaiser_dust at 2.4 s, the box at 2.9 s, the
    Kaiser at 4.9 s (r / g / b / k / w by the outfit colour) with the Mole hidden, gone at 14.85 s; the Time Nuke's
    GMO24 digits centred 1 m over the nuke (checks/fx_mole_qa/nuke_digits.png), gone on Detonate (0.6 s), the blast at
    1.1 s (+-20 m) and the nuke gone; Fire Barrage's flare at 9 m, three planes over at 2-3.3 s, the hits at 9 m;
    Bombardment's 3 x 5 grid of bombs and blasts 5.2-6.2 s; mines 0.5 / 1 m ahead to 10.3 s; Mortar Shot's five lobs
    landing on the target 4.3-5.1 s; Napalm's five at (0, 10) and (+-5, 5 / 15); TNT 1-4's blasts at 8 / 16 / 24 / 32 m;
    Grenade Cluster's eight grenades (tilts drawn), eight bursts round her; Missile's four homing missiles, the front
    pair's hits at 1.7 s, the back pair swinging round to hit at 3.4 s; the Chopper on her back 0.3-5.15 s; War Factory's
    saw, bazooka (three shells, three hits at the body), tesla coil, roller and the cart (stopped 9 m ahead, boom at
    3.3 s); Barrel Railgun's 13-part assembly 0.6-6.0 s, the Mole lifted onto the seat behind the grips by 6.55 s, four
    shots (beam, trench, hit, overload at 10 m) at 8.85 / 11.25 / 13.65 / 16.05 s, off the seat and the shrink to 17.45
    s; Kaiser Arsenal's Kaiser at her spot, the pods on its arms in its red from 0.6 s, the warheads from 1.8 s, hits at
    the target, all gone at 4.4 s; Missile Pad 1.35 m behind, eight missiles 0.95-1.3 s, hits at 2.5-3.6 s with the twin
    blasts; the egg forced: 64 splits landing in a ring 4-6 m round the target (the builder's physics).
  - **Bug found and fixed (wardrobe/fx_cues/mole.json):** Napalm's four side shells had `to` [+-5, 0, +-5], the game's
    offsets from the target, but the part reads `to` as the point: with a firePoint cannon worn, four of the five
    shells re-aimed at points beside the Mole (two behind her). Now the points (-5, 0, 5), (-5, 0, 15), (5, 0, 5), (5, 0,
    15); re-shot with royalCannon: they land at (+-5, 5 / 15) as the fallback rot does.
  - **Fixed (wardrobe/fxparts/tto_mole.js, KaiserWarhead):** its clock and 0.15 s turns ran once per frame (the editor's
    flag): a long frame (a stalled first frame, a tab coming back from the background: the page's clock has no cap) flew
    the warhead straight for the whole frame. Now on the 0.02 s steps, as Mole_missile's.
  - Tool: `wardrobe_fx_shots.py` gains the force `<cue key>^<option>=<JSON>` (missilePad^egg=1) and the props key
    `"_color": n` (the outfit colour, for pick "color").
  - Looked into, not bugs: the countdown reads 59 at the nuke's first frame and 50 in its last second (floor(60 - age),
    the game's sum; decision 55's "60 ... 51" is one off: the 10 s kill ends it at 50); the Mole seen under the floor while
    she digs in / surfaces (dig1, the burrow's crossfade back to idle: the page's stage hides nothing below y 0); during
    the Chopper she reads orange-red: chopper_forwardDust's multiply smoke drawn over her (hidden, she is her own
    colour: checks/fx_mole_qa/probe_hide); the Kaiser's shoulder shells stay brown in r / g / b / k (its texture); the
    Kaiser Arsenal tile shows the "KA" letters (no icon, the editor's call); the props data have firePoint on 22 of 45
    Mole weapons (attacks_emotes says 28 of 44 BB cannons: if a cannon's shells start at the default point, the
    extraction may have dropped its firePoint node: the video repo's).
  - Gates: `wardrobe_fx_check.py ... checks/fx_mole_qa/gate dark --cls mole` exit 0, errors [] (60 tile plays; the
    arsenal's warheads land with the step clock under the headless stalls); files-only (every class with cues) "no
    problems"; unit tests 66 OK, node 9 pass, test_adopt_from_video.ps1 fails 0; `wardrobe_weapon_fx_check.py` OK. No
    regression run: the QA changed only Mole files (its cue file, tto_mole.js's KaiserWarhead) and the shots tool.
  - For the user's eye: the egg's 64 splits (untested against the game); the Chopper's orange-red look; the target-point
    effects and the far TNTs outside the default camera; the white stage's faint glows; propAnim's recoil and the
    Trumpet's tune (the gate counts them, a screenshot cannot show them); KaiserWarhead / the 8.1 MB fx.json on a slow PC.

## 2026-11-13 (office), the Cat after a second reference picture; the five allowed sets; mistakes written down

User: "From now on equipment sets are limited to just these 5 unless I add them later": 60 = royal, 70 = legend, summer,
Halloween (Original) = `hallow` (BB's, not TTO's `halloween`), the class's bug set (in the `reskin-from-image` skill file
and a memory). "These classes are female humanoid: Cat, Sheep, Rabbit, and Bat"; for a pick "don't mind" the Rabbit's
long ears or the Bat's wings. The picture as seen: a slim young woman, short dark violet hair (a small bun behind),
green half-lidded eyes, fair skin, a black choker, a white sleeveless collared shirt with a thin black ribbon, charcoal
high-waisted shorts with one button, black thigh-highs, dark brown loafers.
- **Base: the Cat's summer** (plans/reskins/_pick/<cls>.png: the five sets on the four classes): sleeveless top, shorts,
  bare arms and legs, slip-on shoes, a neck scarf. `pipeline/wardrobe_cat_shorts.py [--debug] [--noshots]` ->
  plans/reskins/cat/shorts/ (look/summer.png 2048 px, look/Cat_default.png = the hair, shots, compare.png, look.html;
  not committed until the user picks; reference.png is the user's).
- Painted: fair skin (head, arms, hands, thighs), the top + bare midriff as the white shirt (drape, a gathered foot,
  placket lines, a back yoke), the shorts' **high waist painted on the body** up to z 0.972 (band, button, fly, belt
  loops), the scarf as the collar with the ribbon's bow and its ends down the placket, a choker on the neck (z 1.268),
  charcoal shorts (a median blur takes the rivets out), thigh-highs from z 0.56, loafers (strap, apron seam, sole),
  hair / ears / tail dark violet. Hidden: the wristband, the top's tied knot, the braces' middle (z 0.95-1.085).
- **Eyes on a closed-eye preset** (the user's idea: "it is easy to work on top of a single eye stroke"): face 5 (each
  eye one arched stroke, sheet x 24-55 and 87-118, y 49-59) is the upper lid; the eye is painted under it on the head
  island (sheet space). After the user's close-up ("yours is too generic"): narrow, a heavy lid running past the outer
  corner, a bright green iris cut by both lids with a rim and an inner ring, a small flat pupil, no light dots, lower
  lashes at the outer end, cheek hatching. The user is trying an image generator for the eyes: the face block
  (1024 px, with the overlay) + a prompt are in Desktop\cat_eyes_imagegen (office PC); a returned picture would be
  pasted over the head island's eye area (not built yet).
- **Mistakes** (now checks in the skill file): (1) hiding the braces whole showed a hollow shoulder and a hole in the
  shorts' back: the body has real openings under them; (2) the first "fix" cut "cap sleeves" picked by their pink,
  which were the top's emblem (a hole in the chest), the second painted them skin (blotches): the cause was found only
  by `island_shots` (new in wardrobe_repaint.py: every island its own colour, the cut pieces gone, eight sides); (3) the
  skin's first ramp rendered mauve under the page's light.
- **Alpha hiding is the page's, not the game's**: the page draws outfits with alphaTest 0.5 (index.html setOutfit);
  BB's `<Class>Equipment.cs` builds the hero's material as `new Material(Shader.Find("Diffuse"))` (colour 0.86), which
  ignores alpha, and no cut-out shader is named anywhere in the decompiled code. So in the game a skin's hidden pieces
  would be drawn solid (the knight's shield, the Bat's tie and buckle, the Whale's hem, pearls, chain and coin, the
  Cat's wristband, knot and braces). Not tested in a running game.
- wardrobe_repaint.py also gained `cached_maps` (texel maps kept in <out>/_cache); wardrobe_skin_live.html
  `&extra=<skin key>@<png>` (a prop's skin, the Cat's hair).

## 2026-11-13 (office), outfits drawn as the game draws them: opaque

User: "Players use my wardrobe to plan what the skin will looks like in the game. Fix the wardrobe to use game logic
ASAP". **The game:** every class's `<Class>Equipment.cs` (the outfit's material method) blends the face overlay onto the
outfit texture (`pixels2[i] = a * face + (1 - a) * base` over the top-left 256 x 256), writes the result into
`new Texture2D(512, 512, TextureFormat.RGB24, true)` and draws it with `new Material(Shader.Find("Diffuse"))`, colour
0.86 grey. RGB24 has no alpha channel and Diffuse ignores alpha: **no part of an outfit is see-through in the game**, and
where a skin has alpha 0 its colour under it shows. The Rabbit alone has a second branch: when the game's own texture
is `ARGB32` it keeps ARGB32 and uses `Transparent/Diffuse` (an alpha blend). It never runs for BB: the rip's import
settings give every outfit texture `textureFormat: 10` (DXT1) or `3` (RGB24), none 4 / 5. In the wardrobe's data only
ToT's student sheets have alpha (ToT is another client, local only, its shader unread).
- **index.html:** `outfitCut(o)` = 0 (no alpha test) for BB / TTO outfits, 0.5 for ToT's; used by setOutfit, the look
  cards' render and the 3D file's export (`fileMaterial(..., alphaTest)`, glTF OPAQUE); `composeTexture` makes a skin
  opaque before it enters the canvas (`solidPixels`: a canvas would store alpha-0 texels as black; the game keeps their
  colour); the pick (`pieceAt`) and the hover overlay take the material's own alpha test instead of a fixed 0.5. Props
  unchanged: they already follow each game material's shader (`game_shader()`, 2026-11-12). TTO's outfit shader is not
  read: TTO outfits are treated as BB's (their textures have no alpha, so only a skin on one could differ).
- **Check:** `uv run --no-project --with playwright python -I pipeline/wardrobe_outfit_alpha_check.py` (a skin with a red
  hole at alpha 0 on the Cat's summer: no alpha test, the hole opaque and red; the ToT student keeps 0.5; no page errors).
  Two traps it hit: `wardrobe.show()` can return before the class has loaded, and `wardrobe.debug().C` is the C of that
  moment (a class load replaces it): read `wardrobe.debug().C` fresh each time. Also passed: wardrobe_sets_check and
  wardrobe_menu_check (errors []), unit tests, node 9/9.
- **Skins made by hiding are changed by this** (now shown as in the game): the Whale crown (the hem's holes, the
  pearls' squares, the chain and coin), the Cat shorts (the wristband, the top's knot, the braces' middle), and the
  earlier Cat knight (the shield) and Bat robe (the tie, the buckle). Their painters must paint those parts instead.
- Deployed from a clean worktree of 074e4d4 (C:\work\12tails-wardrobe-hotfix, branch outfit-opaque), as the last two
  deploys, because the Mole build is editing index.html here: the same edits are in this folder's index.html.
- **The two new skins repainted with nothing transparent** (user: "paint it, never make them transparent"):
  `wardrobe_repaint.paint_under(out, M, piece, under)` (new) paints a part as what lies under it (nearest texel, bind
  pose, |y|). Whale: the chain and coin = the chest under them; the cape's hem net painted over grey like the rest (no
  holes); the banknotes (one texture shared by every note, so no single "under") = two large touching pearls with a
  bead-gap shadow. Cat: the wristband = the arm's skin, the top's knot and the braces = the shirt under them. Both
  painters assert the saved skin is fully opaque. Left as the mesh gives it: the Cat's wristband reads as a skin cuff
  at the wrist and the knot as two white flaps at the waist (their shapes stand off the body). The Cat knight
  (wardrobe_knight.py: the shield) and the Bat robe (wardrobe_bat_robe.py: the tie, the buckle and its inner piece)
  still use alpha: not repainted yet.
- **The Cat knight's shield painted** (user: "repaint the Cat skin on the online wardrobe too to have the shield color
  filled in"): the set is live again as a player set (the user re-sent it through the form; Discord message
  1570624627900678296) and, with outfits opaque, its alpha-hidden shield showed in the champion's old white.
  wardrobe_knight.py: the shield's two islands joined the plate (the armour's silver, its rim and swirl in the
  reference's gold; the reference has no shield: invented from its metals); no alpha anywhere, asserted. The new
  champion.png + Cat_default.png are on the office Desktop, `wardrobe_reupload\cat_knight_face23\12tails_แมว_champion.png`
  / `12tails_แมว_default.png` (the names the page's drop reads): the user sends them again (face 23) and takes the old
  message's check mark away; the live list follows Discord within a minute. The Bat robe (tie, buckle) still uses alpha.

## 2026-11-13 (office), two Bat skins after two in-game enemies (3D references)

User: "it will be 3D model reference this time, find the best Bat Equipment set to copy the skins from in-game enemy Lady
Noir and Bat Cult, 2 skins ... you may use the whole set or just some part". Both enemies are in BB's files on the Bat's
own body (meshes `LadyNoir_tri` (submesh 0 the body, 1 the wand), `BatCult_tri`; textures in the rip's Texture2D/).
- **The references:** `pipeline/wardrobe_enemy_ref.py <out> LadyNoir+NoirWand:NoirWand BatCult@x-90` (UnityPy reads the
  mesh from 12TailsOnline_Data, a bare three.js page shoots it unlit from eight sides) -> plans/reskins/bat/ref/
  (<name>_tri.obj, <name>_sheet.png; BatCult's bind pose has z up: `@x-90`). Not for git (game assets).
- **Picks** (the five allowed sets; candidates shot with `wardrobe_outfit_sheet.py`): the helmeted one in the dark
  purple eye-emblem dress -> outfit **royal** (long dress-coat, wide sleeves, boots) + head **butterflyHood** (the bug
  set's hood as the helmet) + face 4 (amber); the white-haired one -> outfit **summer** (bikini top + hip cloth on the
  bare body) + head **hallowCrown** (a small red crown where she has a rose) + face 21 (red). Weapons not skinned.
- **A whole-model projection was built and dropped** (user: "I don't like your projection approach, it opens up for a
  lot of mistake ... consider repainting yourself while borrowing textures from the existing ones"): every texel took
  the nearest point of the enemy's surface: hair on the face, bands down the dress front, a ragged grey hem.
- **`pipeline/wardrobe_borrow.py`** instead, nothing automatic: `ref_maps` (the enemy's sheet per texel: its place on
  the body in the Bat's frame, by a fit of 24 turns + ICP, 0.8-0.9 cm), `same_uv` (which outfit islands have the
  enemy's own layout at the same sheet place), `borrow(dst, src)` (a named outfit part takes the paint of named enemy
  parts, nearest on the body; prints the distances: over ~3 cm = look at it). **Not mirrored:** a first guess that the
  game's meshes and the wardrobe's data differ in handedness was wrong: the shared layouts (face, ears, tail, hands)
  only coincide with a proper turn (same_uv 99-100 %; mirrored 0-12 %).
- **`pipeline/wardrobe_bat_enemies.py eyes|rose|both [--noshots]`** -> plans/reskins/bat/<eyes|rose>/ (look/<outfit>.png
  1024 px opaque, look/Bat_butterflyHood.png, shots of eight sides, sheet.png, compare.png = original | new | enemy).
  Per part, one of three ways: **same** (the enemy's paint texel for texel: neck, ears, hands, tail; the second one's
  hair back / side and wings too), **own** (the outfit's own paint in the enemy's palette, read from its texture by
  percentile: the faces under the preset's eyes, hair of another cut, royal's coat with its trims, the hood),
  **borrow** (torso, arms, legs, feet, wings, capelet, collar, hip cloth). The first one's sleeves: the enemy's ring
  colours read along the arm (median per 2 mm of |y|). The dress's big eye emblem: a patch of the enemy's sheet
  (x 360-408, y 158-236) laid on royal's inner front strip (z 0.93-0.58); borrowing that strip whole gave bands (7 cm
  apart). The hip cloth borrows the skirt's inside only (inset 10: its red edge had spread over the cloth).
- Limits: summer's arms share one set of texels, so the second enemy's single striped sleeve cannot be on one arm:
  both arms wear her lace glove, the bracelet takes the sleeve's cuff colours; the hip cloth is short where her skirt
  is long. Royal is a coat over a dress where the first enemy wears a fitted split dress with bare shoulders; the hood
  keeps its antennae; no veil over the eye. Left for a next pass: the weapons' skins (royalWand / legendWand).

## 2026-11-13 (office), the Monkey's effects: built and cued

From plans/fx_monkey/ (six reports, each with its "## Verification", which wins; decisions.md decided overnight for the
user's review). One editor after four builders (monkey, elementals, tto_monkey, page_pipeline), on the office PC.
- **Parts (new):** fxparts/monkey.js (the four straight shots Monkey_fireBall 30 m/s / Monkey_earthPulse 15 m/s /
  Phoenix_fireBall / Phoenix_skyCrimson_fire 16 m/s on the 0.02 s step, no gravity, their hits part-spawned on contact
  with the standard target body or the floor (Sky Crimson's ball: the floor only); Monkey_lavu: the summon flight, the
  standby circling the head + 4 m, the 0.25 s trail of its six segments, `lavu: "upheaval"` onto the 6 m ring with
  `release`, `unsummon`'s 1 s fade; fx:mikeBlink: the worn R prop's copy (nothing worn: noviceMike) on the effect's
  mount_Summon), rotationcontrol.js + `Rotate` (the runic rings), mesh.js's FX/Lavu line, fxparts/elementals.js (the
  summons Phoenix, Ja, Gadina, Buiten, Gaos: summon clip + ring, root, their cries, `end` = each one's own unsummon
  coroutine; options standing, anims, hide, moves, turn, attach, boost (TTO: level 6, the aura, the Buiten x 1.2);
  the armours fx:phoenixArmor / fx:gadinaArmor / fx:blazingForm_fire with anims and `alpha` on their own material
  copies; fx.onSingle), fxparts/tto_monkey.js (the two Eric/URP Particles shaders, the Animator's Sigil UV scroll,
  SunCrownFx, the movers Monkey.SunComet / Monkey.SolarCollapse, MonkeyRow6Rise's quake spikes, RuneGolem's AI ported
  from RuneGolem.c: rise, roar, walk 3.25 m/s, fist / quake / pound, the aura pulse with tto/stoneAegis on the hero, its
  glow, CrumbleAway at `end`), shuriken.js's SubModule / NoiseModule (APPROX) / LightsModule (APPROX, pooled lights; no
  other class's data enables any of the three). index.html (page_pipeline): SEQ / LOWER_RANK (cast1, cast2) /
  NEVER_PLAYED (damageCast3) / SEQ_SKILL monkey, the step key `@<seq>:<clip>#<step>` (fxStart tries it first), cue
  option `alt`, PROP_STARTER.monkey, FX_PART_FILES += monkey, elementals, tto_monkey, the cue-format comment.
  wardrobe_fx.py: the Monkey LAYOUTS + the summons', Game's repeated container key keeps the GameObject, EXTRA_FOLDERS /
  FIELD_PREFABS (15) / ALIASES (the Gaos rings) / SOUND_REFS (Phoenix, Gadina, Buiten, Gaos) / SOUND_ALIASES
  (lavu_summon, the Gaos rings' sounds), SHURIKEN_FROM_TTO volcanicEruption, the container voice fallback (buiten,
  blazingArrow), prefixed field prefabs' own AudioSource names (phoenix_fireBall ...). wardrobe_fx_tto.py: EXTRA_FOLDERS
  monkey (the elementals' ja / buiten / runegolem folders), SKILL_FX monkey (28), CODE_MOVERS, the Animator's uv curve.
  Nothing the video repo reads was renamed.
- **Editor fixes (found by the build and the gate):**
  - **The rip's Monkey sounds are empty:** all 36 WAVs in `characters/heroes/monkey/sounds/` of BOTH Bible copies
    (D:\12tails and the Desktop one) are zero-filled (no RIFF header; ffmpeg refused blazingArrow.wav and the build
    stopped); every other class has 0. wardrobe_fx.py's sound jobs now check the header (`rip_broken`) and take BB's own
    AudioClip from the Resources container (`container_voice(..., folder)`, sounds/ then voices/), with a printed line
    per file. The Monkey's sfx/ are BB's container clips: for the user's ear.
  - **`own.onSingle?.(c)`** (index.html fxDue's `single` branch): the elementals builder's item for page_pipeline was
    not in the page; without it a reused armour / standing summon kept its first cue's timeline (the form tiles, every
    loop of a command tile).
  - wardrobe_fx_check.py: a sequence's cap now adds the time its earlier steps take (`play_time`: the @t holds, else the
    clip's length): Summon Gaos' 8 s bar put the Gaos' unsummon ring (10 s after the release) past the old cap.
- **Cues** (wardrobe/fx_cues/monkey.json, 42 keys, 193 cues: 130 fx, 45 voice, 14 sound, 4 hideProp; 97 effect names
  (cued + builds), 27 TTO; assembled by checks/fx_monkey_build/editor/assemble.py, git-ignored, from
  attacks_emotes (its blocks with Verification 1's Mike Blink entries), skills_a Verification 8 / skills_b Verification 4
  (verify/a_fixed.json, b_fixed.json), effect_only block 3, parts Verification's @Lavu:cast3, tto Verification's block).
  Applied on top: decision 5 (castRing cut 0.1), 7 (@JaAscension:damageCast1 with damageCast1's voice), 15
  (@Phoenix-Fireball:root new), 30 / 35 (`end` 10 on every skill's own summon: the cast3 pool's Phoenix4 / Ja4 / Gadina4
  / Buiten4, Summon Gaos' Gaos, Blazing Arrow's Phoenix), 31 (clips -> anims, ring: false -> standing: true), 34
  (Titanic Earth Pulse's Gadina4 standing, `end` 0, with sword / shield), 36 (the armours' anims), 37 (the form tiles'
  armour single, kill 10), 38 (Lavu unsummon 10, kill 11), 44 (Fire Rune rolls at the Fireball cast 0.8, Fire Keep 0.8,
  Fire Avatar 1.5, Earth Form 1.2, Earth Form Attack stage 3 0.8); builds: the Gaos rings, the Phoenix / Buiten unsummon
  sounds, the Buiten summon sound on Bastion Buiten, fireBall_hit on Fire Avatar - Fireball.
- **Tiles / icons:** SEQ "Phoenix - Fireball: root*@2.8" (was 2.5: the shot at 0.5 s + about 0.25 s flight + the hit's
  2 s life); wardrobe_skill_icons.py CLIP_SKILLS / EFFECT_ONLY / OWN_TILE monkey (decision 18); rerun: monkey 42 HD icons
  for 56 clips (32 new webp; index.json monkey only).
- **Data:** `wardrobe_fx_tto.py monkey`: 28 TTO effects, 68 materials, 59 textures, 2 sounds; `wardrobe_fx.py monkey`:
  70 effects, 85 materials, 85 textures, 89 sounds (the three volcanicEruption graft lines and the container-clip lines
  printed). data/monkey/fx.json 98 effects (8.6 MB, the summons' meshes and clips: now the largest class file), sfx/ 90
  files, 101 new textures in data/fx/tex: all new files, to commit with the run; the other PC pulls.
  wardrobe_fx_inventory.py BUILT += the Monkey's shots / Lavu / Rotate / summons (+ their AIs, data only), NOTES
  volcanicEruption's graft, CLASS_NOTES monkey (the hero fields, the field prefabs); rerun: the Monkey 50 / 51 ready (the 1 left: volcanicEruption's grafted ParticleSystems, drawn).
- **Judgement calls (mine):** Summon Gaos' instant alternative keeps its castRing cut 0.05 (its step is 0 s, Auto
  Instant's castTime 0, not the 0.1 s floor of decision 5); Blazing Arrow lists no builds (its Phoenix and ring come
  with the 24 % roll; the check expects every build on every play; the Phoenix tile's builds put the ring in fx.json);
  the Phoenix member's builds carry sound:phoenix_pheonix_unsummon and Buiten Hou Hou's sound:buiten_buiten_unsummon
  (their `end` plays them); the Phoenix - Fireball hold 2.8.
- **Gate:** files-only (every class with cues) "no problems"; `wardrobe_fx_check.py ... checks/fx_monkey dark --cls
  monkey` exit 0, errors [], 48 tile plays (Summon Gaos twice: the 8 s bar, the instant one), every expected effect
  spawned (the four shots' part-made hits, the summons' rings, the Gaos' unsummon ring, the golem's 12 spawns and
  tto/stoneAegis, the boosted auras); the page and shared parts changed (index.html's onSingle, shuriken.js, mesh.js, rotationcontrol.js, the check, wardrobe_fx.py's sound jobs), so also `--cls wolf,sheep,penguin,bat,bison,cat,chameleon,mole` in one run (checks/fx_monkey_regress): exit 0, errors [], 360 tile plays; unit tests 66 OK, node 9 pass, test_adopt_from_video.ps1 fails 0;
  `wardrobe_weapon_fx_check.py` OK. Not committed.
- **Left out:** decision 57's five untraced summon-move cards (Gadina - Normal Attack, Ja - Detonate, Gaos - Fire /
  Rampage / Tail Spin) and the BB elementals' AIs (a follow-up job for HANDOFF.md); sanctumRaise (not released);
  volcanicSoul_ring (in neither game); decisions 49-56's camera effects, foe statuses, texts.
- **For the QA pass:** nothing has been looked at in a screenshot yet: Lavu's flight out of the ground and its circling
  4 m over the head (the default camera's fit), Upheaval's 6 m ring, the shots' hit points (the 0.02 s steps put them at
  d 9.97-9.99, not the body's 9.7 front), Sky Crimson's ball from 11.7 m up landing at d 10.2, Instant Blaze's dash to
  12.8 m, the Gaos 9 m ahead, the Gadina's sword / shield on its hands (and gone with it on Titanic Earth Pulse's `end`
  0), Mike Blink's flying Mike (bare: noviceMike), Fire Avatar's hidden hero and armour, Blazing Fire's alpha fade, the
  Eric shaders, the Rune Golem's walk / fists / quake spikes / glow / crumble, Ja Ascension's comet, crown and collapse
  on the Monkey, the boosted Ja / Buiten auras; the container sounds by ear. Headless first-frame stalls (Ja Ascension's
  first sample after 0 s at 3.6 s, Phoenix - Fireball's at 2.6 s) want wardrobe_fx_shots.py's virtual clock. Rolled
  procs the gate does not expect: Fire Rune (12 %), Auto Instant (12 %), Blazing Arrow's Phoenix (24 %), KO's
  deadEffect. The builders' headless harnesses are in this session's scratchpad (monkey: check/check.mjs; elementals:
  test_elementals.mjs; tto_monkey: harness/run.mjs).
- **For the Bible (offer, not written):** decisions.md's last section; also: the rip has no Monkey sounds (zero-filled
  WAVs; BB's container holds them); the Rune Golem walks at 3.25 m/s (CharacterControl's runSpeed, eased at 4 /s: tto.md's
  "4 m/s" is the easing rate); the golem's glow is material 1 (tto_runeGolem_glow, legacy Additive); FX_Magic_Circle's
  scroll binds the Sigil's `glow/line`, whose renderer is off in the game too (no visible scroll).
- **QA pass (13/11/2026, office).** Shot with `wardrobe_fx_shots.py --jobs` (virtual clock; jobs
  checks/fx_monkey_qa/jobs.json from make_jobs.py, 62 jobs, every Monkey tile: Normal Attack; Mike Blink bare (noviceMike),
  with fireMike (Fire Rune forced on both strikes) and geoMike; HP Transfer, Mike Circle; Fireball (and with Auto Instant
  + Fire Rune forced); the ten cast3 members, the summons and armours to their unsummon / end (12.3-13.5 s); Lavu to
  12.4 s (side, front, far); Volcanic Eruption to 11.5 s; Summon Gaos' 8 s bar to 21 s and its instant bar (forced) to
  12.8 s; Fire Keep; Earth Form Attack (and stage 3's Fire Rune forced); Sentinel Guard; Upheaval to 10.5 s (side, top,
  far); Instant Cast, Fire / Earth Rune; Fire Avatar - Fireball, Blazing Fire, Phoenix - Fireball; Runic Flame / Sand;
  the five Summon Attack members, the three Summon Release members, Summon Defense; Blazing Arrow (and its Phoenix forced,
  to 15.9 s); Titanic Earth Pulse; Flash Fire; the four TTO tiles to their end (Ja Ascension to 15 s and Rune Golem to
  14.1 s with a far view); sanctumRaise's bare clip tile; KO (dead forced, and as rolled), getUp, run, wave, clap, wai,
  dance, fishingMonkey, cooking) on the dark and the white stage: 838 shots each. Sheets: checks/fx_monkey_qa/sheets_dark,
  sheets_white (git-ignored; shots and logs under run/). No page error, no stalled render loop, no failed job (no
  console line at all on either stage).
  - What matches (boxes in the hero's frame, +x = her left): Mike Blink's Mike leaving at 0.3 s, at the target by 0.5 s,
    strikes at (0, 0.9, 9.7) at 0.5 s and (0, 0.9, 10.3) at 0.8 s, the worn piece hidden 0.3-1.0 s (the starter noviceMike
    flies when nothing is worn); Fire Rune's ring at the hero's feet; HP Transfer's beam (0, 0.6-0.8, 0.9 -> 9.3) with
    the two Mikes circling the target 0.7-3.85 s; every cast's castRing 0.7-0.8 s, castEffect_fire at 1.1 s, the release
    at 1.2 s; the Fireball's hit 0.3 s later at the target (the 0.02 s steps put it at d about 10, as the game's discrete
    trigger would); the Phoenix4 / Ja4 / Gadina4 / Buiten4 2 m ahead from 1.2 s with their rings, standing to 11.2 s, then
    their own unsummon (the Phoenix's / Ja's ko, the Gadina sinking back into the floor with its sword and shield on its
    hands, the Buiten's effect), all gone by 12.3-13.5 s; Ground Lock's hit at 1.3 s and Second Stone at 4.3 s at the
    target; Fire Avatar's hidden hero 1.5-11.5 s with the armour and its two creates, Earth Form's armour from 1.5 s; Lavu
    bursting up 3 m ahead at 1.2 s, the column climbing to 2 s, its tail out of the floor by 3.3 s; Upheaval's Lavu on the
    6 m ring round the hero 2.0-3.1 s, released into standby; the Volcanic Eruption field at the target 1.1-11.1 s; the Gaos
    9 m ahead at 9.1 s (8 s bar) / 1.1 s (instant), its unsummon ring 10 s later; Fire Keep's store 0.8-1.8 s and the
    shot at 2.2 s; the form tiles' armour already worn (Blazing Fire's fade to 0 over 0.8-1.0 s, back from 2.5 s; Fire
    Avatar - Fireball's ball at 0.4 s, hit 0.7 s); Phoenix - Fireball's shot at 0.5 s, its hit at 0.8 s; Summon Attack's
    shot at 0.8 s, hit 1.15 s; Sky Crimson's Phoenix gone 2.3-5.3 s, the ball from (0, 11.7, 5.4) at 3.3 s, bursting on
    the floor at about (0, 10.2) at 4.2 s; Planet Breaker's two pulses; Instant Blaze's dash from 0.8 s, the Phoenix
    standing at d about 13 from 1.9 s with its ring riding it; Unsummon's ko, gone 1.3 s; Summon Soul's ring and soul;
    Blazing Arrow's arrow and, forced, its Phoenix 2 m behind at 4.8 s, unsummoned at 14.8 s; Titanic Earth Pulse's Gadina
    unsummoned from 0 (gone by 1.5 s), the shot at 5 s and its hit at 5.35 s; Flash Fire's eight bursts; Ascended Ja /
    Bastion Buiten (the boosted Ja with its aura, the Buiten x 1.2 with its slam and rise); Ja Ascension's standing Ja to
    0.8 s, the comet arcing onto the head 0.8-1.7 s, the crown to 11.7 s, its rise and dive onto the Monkey and the
    supernova at 12.5 s; the Rune Golem's circle, rise and burst at 1.4 s, roar, walk to the target, quake spikes, crumble
    11.4-13.8 s; KO's deadEffect.
  - Tool: `wardrobe_fx_shots.py` gains the force `seqAlt:<step>=<k>` (window.__seqAlt: Summon Gaos' instant bar).
  - Looked into, not bugs: the worn Mike seen about 5 m ahead at 1.1 s after Mike Blink is the hero's own piece on its
    mount, which the nAttack clip flies out and back (the probe checks/fx_monkey_qa/probe/orphan.py: C.props.R at d 4.7
    at 0.5 s, 5.1 at 1.1 s, back at 2 s; no stray mesh in the scene), as the game's resetMikeBlink puts mWep1 back on
    its mount; Stone Hammer's box reads 5 m to her right because the box tool takes a skinned mesh's bind-space bounds
    (the drawn hammer falls on the target's centre: its rings at x 0); ja_summon_ring draws nothing (the prefab is an
    AudioSource only); the Gaos and the golem fill the front view (they are that big); Lavu out of the default frame
    3.5-10.8 s: the standby's RotateTowards at 1 rad/s and 8 m/s loops it in the vertical plane up to 28 m and through
    the floor (Monkey_lavu.cs Update, ported line for line; the game's moving hero tilts that plane); the Titanic Earth
    Pulse hit's blue dome is 19 m across (the prefab); every one of the 90 sfx files plays a real sound
    (checks/fx_monkey_qa/probe/loud.py: no silent file, max -0.0 to -12.6 dB, step_normal1 -25 dB as the other classes').
  - Gates: `wardrobe_fx_check.py ... checks/fx_monkey_qa/gate dark --cls monkey` exit 0, errors [] (48 tile plays); unit
    tests 66 OK, node 9 pass, test_adopt_from_video.ps1 fails 0; `wardrobe_weapon_fx_check.py` OK; index.html LF. No
    regression run and no fix: the QA changed only the shots tool. Not committed.
  - For the user's eye: Lavu's vertical loop out of view (and dipping under the floor) for most of its 10 s; the target-
    point effects and the 9 m Gaos outside / filling the default camera; the container-clip sounds by ear (BB's own, never
    listened to); the white stage's faint glows; decisions.md's overnight calls and the editor's judgement calls above.
- **The white-haired one, the user's review** (the rose, the striped sleeve and the midriff strap circled on the
  reference: "apply these fixes, add these details. And remove the headpiece"; then "details here [the hip cloth]
  still looks gibberish ... you may invert the pattern from the ref left and right and I think the eye sigil from the
  ref should align nicely there"; "bat cult need a brighter whiter hair"). (1) **No head piece**: hallowCrown had stood
  in for her rose (the only small red piece on the head among the five sets' head pieces; a crown on the crown of the
  head, never repainted: a weak stand-in). The rose is painted flat on the hair before her left ear instead
  (`ROSE_AT`, `ROSE_R`: the enemy's rose picture laid on the hair texels there; hair islands are not mirrored, the
  ears are, so not on the ear). (2) **The straps** (front, top to belt; one down the back) are pieces standing off
  the body sharing one strip of her sheet (x 489-506, y 333-409): the nearest-point borrow never reached them.
  `Job.lay(dst, box, side)` reads the piece's triangles from the mesh, keeps the front or the back ones, and paints
  the body texels behind them (nearest in y, z within 3.5 mm). (3) **Arms**: every arm texel of summer has a triangle
  at +y and one at -y (checked on the mesh), so one sleeve on one arm is impossible: `rose(arms=)` "sleeve" (stripes
  + cuff on both: the working file), "mix" (stripes to |y| 0.40, lace below), "lace"; `wardrobe_bat_enemies.py arms`
  -> rose/arms.png (the three side by side) for the user's pick. (4) **Hip cloth**: `borrow(flip=True)` reads the
  enemy's skirt at the mirror place (her skirt hangs from her left hip, summer's cloth from the right): 0.7 cm median
  apart (unmirrored: 9-18 cm at the far side, scraps); inset 3 keeps the belt and the red edge. (5) Hair lifted
  (`HAIR_GAMMA` 0.40): her texture's white reads grey under the page's light.
- **The straps lengthened; the arms mocked both ways** (user: "make sure the strap reaches the skirt, it ended abruptly";
  the right arm bare: "forget the right bare arm, it's impossible since it's mirrored ... mock me both bares for
  comparison"). `Job.lay(to_z=STRAP_TO)`: the straps run down to z 0.90, under the hip cloth's top (the Bat's cloth sits
  lower than the enemy's belt), their buckle ends kept, the band between stretched. Measured over whole parts (a raster
  of each side's triangles): summer's arms, hands and legs are 97-99 % shared by both sides, the bracelet is the right
  wrist's only, the hip cloth and torso are not shared. rose/arms_bare_vs_sleeve.png = A the sleeve on both | B bare on
  both (her lace glove on the forearm: look/summer_lace.png); the working file is still A until the user picks.
- The user picked **bare arms** ("bare arms look better"): rose(arms="lace") is the default now (bare upper arms, her lace
  glove on both forearms); look/summer.png, sheet.png and compare.png are that version.
- **The helmeted one, the user's review** (the forehead, the chest, the dress's middle, the coat's two front edges and
  the panel between them circled: "attempt the better job at trying to use reference texture around these parts.
  Also face 11 looks more like her"). `borrow(view=1 | -1, within=)` (new): a part is read **as seen from the front or
  the back**: nearest in (y, z) only, of her layers there the one in front, front-facing texels on both sides, and
  only where she has something within `within` (the rest keeps its paint). Royal's coat and dress hang differently
  from her dress, so nearest-on-the-body had given bands; the view reading gives: the dress front 0.4 cm median (90 %
  taken), the chest ornament (royal's jabot halves = her two eye-disc cups) 0.2 cm, the capelet's front (bare chest,
  shoulder pieces), the coat's front and back where her skirt panels are (55 % / 61 % taken: her trims and scrolls;
  the coat's wider, longer rest keeps its re-coloured paint), the helmet's brow band and eye disc on the fringe's top.
  The hand-placed eye emblem on the centre panel is gone: on her model the big eyes sit on the side panels, the
  centre is the plain pointed tabard under the waist disc. Royal's gold zigzag is now a faint line. Face 11.
- The white-haired one's skin is on the office Desktop for the user's own upload: `wardrobe_reuploadat_cult_face21  12tails_ค้างคาว_summer.png` (1024 px, opaque; outfit summer, face 21, no head piece).
- **The opaque-outfit deploy d4adea35 had two side effects** (found by the effects session, 2026-11-13): built in a fresh
  git worktree of 074e4d4, it lacked the git-ignored `wardrobe/data/bb_rip_fix/` (the office's repair of 52 zero-filled
  Monkey PNGs), so the publish dropped the Monkey's 23 BB faces (live: faces 23-32 only) while printing "check: no
  problems"; and it replaced the effects session's Mole deploy 9c8368b1 of seven minutes earlier, taking the Mole's
  effects offline. The effects session republishes from current main with the folder linked in and makes
  wardrobe_publish.py stop when the folder is missing. Rule for this session's deploys from now on: from the main
  folder at current main (or a worktree with bb_rip_fix linked: New-Item -ItemType Junction), and tell the other
  session first.
- **The helmeted one: the whole headband, the coat's side sigils** (user: "why only half? bring the full headband texture
  (on the hair itself like you did, we don't have an option)"; "texture of the side coat could use some white eye sigils
  from the ref coat"). (1) **Why half:** her helmet is itself a mirrored part: ref_maps holds only its y >= 0 half
  (the last triangle drawn per texel), so the Bat's other half found nothing within reach. `absy=True` reads it for
  both sides. The band + eye disc (her helmet below `BAND_TOP` 1.635, the dome left out) now goes on the hair AND the
  bare forehead between the strands, worn `BAND_DROP` 1.2 cm lower than hers (`borrow(shift=)`) so the hood's edge
  clears the disc; 0.2 cm median, 79 % taken. (2) `borrow(view=1, axis=1)`: a reading **from the side** (nearest in
  (x, z), the outermost layer, side-facing texels on both models): the coat's sides take her side panels with the big
  white eye and its leaves where her skirt reaches (`COAT_SIDE` 3 cm, 61 % taken); the coat's longer hem keeps its
  re-coloured paint.
- **The helmeted one: don't force it; the coat's front pieces and border** (user, with the chest and the inner dress's
  front boxed: "it is too forced to match the reference on uneven texture meant for an entirely different things, in
  this case, don't force it, just use other designs that respect the model there"; "the coat front piece, please try a
  better job at trying to use reference image patterns"; tracing the coat's front edge: "add reference image silver
  lining border along the edges of the coat too"). (1) The capelet, the collar, the throat ornament and the inner
  dress's front are **royal's own forms in her colours** again (cloth = her purple, what royal draws light = her
  silver, the gold zigzag faint; the collar's other face her cowl's black and red): no reading of her bodice there.
  (2) The coat: plain cloth base (royal's own edging and zigzag gone), her back and side readings as before, and on
  each **front piece her panel's own pattern**: the eye in its diamond frame with four leaves, from her sheet
  (`SIGIL` box x 350-420, y 144-254), upright at z 0.66, 16.5 x 26 cm, only its drawn lines (what differs from the
  box's median cloth colour) so no box shows. (3) **Her silver border** along every edge of the coat: its colours from
  her sheet (the stroke beside the sigil, x 430-446, y 150-228), drawn as a band by the distance to the coat island's
  edge (`M.edge`): dark line, silver with a light middle, dark line, a lilac glow inside.
- **The helmeted one: the front piece is the inner dress's centre panel** (user, boxing it beside hers: "front piece
  stills fail to resemble the reference pattern, not even close"; "I want thicker silver lining with brighter tone to
  contrast, now it just blends in"). I had read "the coat front piece" as the coat's two front flaps and put the panel
  back to royal's own ornaments: wrong piece. Now the panel (island at sheet 300,162; its texels hold y <= 0, mirrored)
  is her centre column read from the front with |y|: her bodice (both halves: it is not mirrored) and her tabard
  (island 19, its y >= 0 texels only: the rest are other faces), `borrow(scale=(1, TABARD_FIT 1.35, 1))` so her wider
  tabard's silver border stays inside the narrower panel; a plain dark cloth where she shows nothing (within 0.8 cm,
  65 % taken). Result: the pointed tabard with its border, V and leaf ornament matches; the waist disc comes out as
  its outer ring only (its inner rings are not picked up: open); above the waist the panel is mostly under royal's
  throat ornament. The coat's lining: `LINING` 6.5 texels wide (3.5 before), from her border's grey up to near white,
  a darker line each side.
- **The helmeted one: the front piece fitted to its own shape; the waist sigil; skin at the chest; a thinner lining**
  (user, tracing the piece's outline with its two tails: "you copied the pattern with no extra thoughts that the actual
  shape of the front piece is like this, please optimize the pattern to fit well with that model in mind"; "the prior
  silver lining is now too thick, maybe 60%"; "add circle sigil from the ref image here too"; "show some skin under
  the complex 3d shapes above, no need to match the ref exactly"). The piece (half-width 5.7-9.6 cm, splits into two
  tails at z 0.49; her tabard ends in one point) below `TAB_TOP` 0.935: her tabard's inside (V, curls with leaves,
  diamond) laid across the piece's own width at every height (u = |y| / the piece's edge there = the same share of
  her tabard's width; her top down to `HER_LOW` 0.56 onto the piece's top down to the split), plain cloth on the tails,
  and the silver border along the piece's real outline round both tails (`PANEL_RIM`; distance to the island's edge,
  the mirror seam at y = 0 left out). The waist sigil is drawn (`DISC`: silver rim, dark ring, silver ring, dark
  middle), not read: her own is half a disc standing off the body. Skin above a neckline (`NECK` 1.085, rising to
  the sides, her silver edge) on the piece's top, from her sheet's chest skin; royal's hanging tab stays dark (a
  pendant; island 236,286 painted skin is not the visible tab). `LINING` 3.9 (60 % of 6.5).

## 2026-11-13 (office), the Panda's effects: built and cued

From plans/fx_panda/ (six reports, each with its "## Verification", which wins; decisions.md decided overnight for the
user's review). One editor after two builders (tto_panda, page_pipeline), on the office PC.
- **Parts (new):** fxparts/tto_panda.js (TTO's HelixRibbonEmitter, nine instances: the Tempest Dance aura / end / pulse,
  Yin Yang Fist's charge and seal, yinYang; the code movers Panda.NineDragon (the cued hand spot, the code's cubic Bezier
  bowing to the side of `k`'s parity, to `to` in clamp(1.6 d / 22, 0.35, 0.7) s, NineVanish) and Panda.NineKing
  (0.4 s weave to `to` + 0.8 up, NineVanish: Body / HeadGlow / HeadHalo hidden, the ParticleSystems stopped, "destroy"
  0.5 s later); the hook fx:tto/tempestDance_trails (the four limb trails on the hero's Hand_R / Hand_L / Foot_R / Foot_L
  through api.boneMatrix, placed before the trails sample, `off` = emitOff); the shaders ERB/Particles/Add_CenterGlow,
  ERB/Particles/Blend_CenterGlow (noiseTex loaded by the part, white when absent) and Particles/Standard Surface (lit,
  flatShading, `_BumpMap` left out: APPROX)); fxparts/tto_sheep.js: TrailRendererModern's `emitOff()` (no `stop()`);
  fxparts/trail.js: a TrailRenderer off in the prefab is built hidden and the cue's `enable` ([[t, node, on], ...])
  switches it by node name (Three Steps' fxNode1-3; a trail with no enable list is as before). index.html
  (page_pipeline): SEQ / SEQ_SKILL panda (decisions 1-16), HERO_SKINS `ashura` (tint 1 / 0.86, 0, 0), the cue option
  `atBone` (spawned once at the hero bone's world position + x / y / d along her facing, not parented), range-valued
  x / y / d (`rangeOf` in cueOf and api.spawn: a float per play), api.boneMatrix(name, fx), FX_PART_FILES += tto_panda,
  the cue-format and part-loader comments. wardrobe_fx.py: SHURIKEN_FROM_TTO panda raijinKen_hit (no SHURIKEN_MAT).
  wardrobe_fx_tto.py: SKILL_FX panda (15), CODE_MOVERS nineDragons_dragon / _king, `material()` saves `_Noise` as
  noiseTex / noiseScale / noiseOffset. wardrobe_data.py: the clip filter `animations/[a-z0-9_&]+` at :49 and :210 (not
  run: the Panda's data rebuild is the home PC's, HANDOFF). Nothing the video repo reads was renamed.
- **Cues** (wardrobe/fx_cues/panda.json, 56 keys, 212 cues: 140 fx, 52 voice, 18 sound, 1 skin, 1 hideProp; 69 effect
  names, 13 of them TTO; assembled by checks/fx_panda_build/editor/assemble.py, git-ignored, from attacks_emotes' block (17
  keys), skills_a's (14), skills_b's (16, with its Verification 2's raijinKen1 + the 1 s hideProp hero and Verification
  3's tigerToss splash at d 10), effect_only Verification 5's first five, tto Verification's block (4 keys, 54 cues)).
  Applied on top: decision 24 (Heaven Palm's blasts at the nominal 1.2 / 1.8 / 2.2 / 2.6 s, its why says so); decision 3
  and 9 (the Raijin Ken / Roll Around whys quote the page's SEQ lines, no `!` / `^`); decision 31 (delayQi kill 3, not
  parts Verification 5's 6); decision 52 (`wind&cloud` / `rain&storm` held back for the home rebuild). The empty
  `@RaijinKen:cAttack2` / `raijinKen2` entries stay as records (decision 61; the check accepts an empty list).
- **Tiles / icons:** wardrobe_skill_icons.py CLIP_SKILLS panda fujinKen1-3 -> fuujinKen, EFFECT_ONLY panda mysticSage /
  safeGuard, OWN_TILE panda sacredSageTechnique / delayQi, the Bible-key pattern `([A-Za-z&]+?)` (decision 60); rerun:
  panda 33 HD icons for 46 clips (6 new webp: deathBlow, delayQi, fuujinKen, mysticSage, sacredSageTechnique, safeGuard;
  index.json panda only, no other class changed). No NEVER_PLAYED / LIFTS / LOWER_RANK for the Panda.
- **Check / inventory:** wardrobe_fx_check.py OPTS += enable, atBone, k, off; a cue's x / y / d must be a number or
  [lo, hi] with lo <= hi. wardrobe_fx_inventory.py BUILT += HelixRibbonEmitter (TTO, not scanned), NOTES panda
  (raijinKen_hit's graft, threeStep's switched trails: drawn), CLASS_NOTES panda (the five CharacterControl status looks,
  the three dead prefabs); rerun: the Panda 70 / 71 ready (the 1 left: raijinKen_hit's grafted ParticleSystem, drawn).
- **Data:** `wardrobe_fx_tto.py panda`: 15 TTO effects, 45 materials, 44 textures, 10 sounds; `wardrobe_fx.py panda`: 56
  effects, 65 materials, 61 textures, 118 sounds (the raijinKen_hit graft line printed). data/panda/fx.json 71 effects
  (3.7 MB), sfx/ 120 files, 56 new textures in data/fx/tex: all new files, to commit with the run; the other PC pulls.
- **Judgement calls (mine):** the whys of Heaven Palm, Raijin Ken and Roll Around rewritten only where decisions.md
  changed their numbers or lines; the range test in the check (lo <= hi); the dead prefabs in the inventory's class note
  (the scan lists only code-loaded prefabs, so a per-effect note would never print); wardrobe_skill_icons.py,
  wardrobe_fx_check.py and wardrobe_fx_inventory.py kept LF as they were in this checkout.
- **Gate:** files-only (every class with cues) "no problems"; `wardrobe_fx_check.py ... checks/fx_panda dark --cls panda`
  exit 0, errors [], 43 tile plays, every expected effect spawned (by name: the dragon and the King, risingDragon_hit,
  the limb trails, the seal and burst, threeStep, the ashura skin, the hideProp hero); the page and shared parts changed (index.html's atBone / ranges / boneMatrix, trail.js, tto_sheep.js, the check), so also `--cls wolf,sheep,penguin,bat,bison,cat,chameleon,mole,monkey` in one run (checks/fx_panda_regress): exit 0, errors [], 408 tile plays; unit tests 67 OK, node 9 pass, test_adopt_from_video.ps1 fails 0; `wardrobe_weapon_fx_check.py checks/fx_panda_build/editor/weapon_fx_check.png` OK. index.html LF. Not committed.
- **Left out:** Wind & Cloud and Rain & Storm (their clips are not in clips.json until the home PC's wardrobe_data.py
  rebuild with the `&` filter; then the two cue entries from effect_only Verification 5 and the build line of decision
  52: HANDOFF); tempestDance_counter and yinYang (built, not cued: decision 37); drunk and paralysis on the target
  (decision 38); the three dead prefabs (decision 49); sacredSage_ring / heavenBreath_ring (in neither game, decision 48);
  decisions 46-47 and 50's camera effects, texts, numbers, steering.
- **For the QA pass:** nothing has been looked at in a screenshot yet: the three new shaders (the burst's ERB glows, the
  bamboo / leaves / smoke under Standard Surface's flat shading), the helix ribbons, the dragons' Bezier from the hands
  (the headless first frame stalled: the first sample after 0.03 s is at 2.68 s, so the dragons and the King were seen
  only in the spawn tally) and the King's weave, the limb trails on the hands and feet and their fade from 5.75 s, Three
  Steps' trails switching (sampled only at 0 and 1.24 s), the climbs' flashes at the Root bone + 0.3 m, Pummel's arms
  scattered, the red Ashura Panda, the 1 s hidden Panda under raijinKen_hit's kick, Raijin Ken's grafted puffs,
  Crushing Monolith's three doubles round the 10 m target. These want wardrobe_fx_shots.py's virtual clock. Rolled
  procs the gate does not expect: KO's deadEffect (p 0.5); Stasis / Death Blow are one tile each.
- **For the Bible (offer, not written):** decisions.md's last section.
- **QA pass (13/11/2026, office).** Shot with `wardrobe_fx_shots.py --jobs` (virtual clock; jobs
  checks/fx_panda_qa/jobs.json from make_jobs.py, 52 jobs, every Panda tile: Normal Attack (bare and with the Champion
  gauntlets), Charge Attack, Sacred Sage Technique, Raijin Ken to 8 s (side, front, behind; and gauntlets worn for the
  hide), Fuujin Ken to 9.9 s, Qi Strike and Delay Qi to 8.2 s, Tempest Dance to 6.6 s (side, front, near), Ashura to 11 s
  (bare and with gauntlets), Tiger Toss, Climbing Cliff, Crumbling Mountain (side, behind, far), Roll Around to 6 s, Mystic
  Sage, Safe Guard, Stasis Blow, Death Blow, Combo Link, Drunken Fist to 10.2 s, Heaven / Lotus Palm, Pummel, Roll, Three
  Steps (side, top, near), Rushing Falcon, Tower Rush, Rising Vortex, Rising Dragons, Water Monkey / Crane, Sp Transfer,
  the three TTO tiles (Nine Dragons to 5 s from side, front, behind and far; Tempest Dance; Yin Yang Fist to 3.5 s), KO
  (dead forced, and as rolled), getUp, run, the eight voiced emotes, clap, wai, dance, fishingPanda) on the dark and the
  white stage: 681 shots each. Sheets: checks/fx_panda_qa/sheets_dark, sheets_white (git-ignored; shots and logs under
  run/). No page error, no stalled render loop, no failed job (the only console lines: swiftshader's glBlitFramebuffer
  feedback warning).
  - What matches (boxes in the hero's frame, +x = her left): the Combo's punches at 0.1 / 0.3 and 0.8 / 1.0 s, the wheel
    from 1.6 s, Aura Blast from 3.3 s (each stage one 1/30 s frame off the anchors, the clock's step); the charge's two
    rings 0.7-3.7 s; Raijin Ken's ring1 to 5 s, ring2 at 5.0 (its own second pulse at 7.0 s: the prefab's 2 s Delay
    emitters), the kick from 12-19 m up onto the target from 5.5 s and its splash at the target, the Panda hidden 5.5-6.5 s
    with her gauntlets (hero meshes drawn 0, hidden 3) and back at 6.6 s; Fuujin Ken's ring1, the cyclone and clouds
    (+-13 m) to 9.0 s and ring3 at 9.0; Qi Strike's 4 s ring, Delay Qi's glow at her feet 4.0-7.0 s, delayQi_fire and the
    burst at 7.0 s (Delay Qi's tile the same); Tempest Dance's helix aura, the eight gusts 0.3-4.5 s, the four limb trails
    on hands and feet riding her jumps (to 2.9 m up) and stopping from 5.75 s (gone by 6.1 s), the end's helix from
    5.75 s; Ashura's ring at 0.4 s, the red Panda 0.8-10.8 s (her worn gauntlets red too) and back at 11 s, the Root
    flame on her, Ashura Fist's eruption at 2.1 s; Tiger Toss at 0.8 s and the splash at (0, 0, 10) at 0.9 s; the climbs'
    flashes left where Root + 0.3 m was at each spawn while she climbs to 4 m; Crushing Monolith's three doubles round
    the target (rising to 3 m, landing at 2.8 s, fading); Roll Around's ring each round to 6 s; Mystic Sage's cyan
    double 1 m behind her, Safe Guard's shell; Stasis / Death Blow's ring, blow and end dust; Combo Link's ring at 0.4 s;
    Drunken Fist's spins at 0.2 / 0.5 s and the drunken stars to 10 s; Heaven Palm's four blasts at the target from 1.2 /
    1.8 / 2.2 / 2.6 s (x 1.5); Lotus Palm's flash at (0, 1, 9.7) at 1.4 s; Pummel's dust, ogre and ten arms scattered both
    sides 0.25-0.7 s; Three Steps' trails switched (fxNode1 at 0.2 / 0.45, fxNode2 at 0.6, none at 0.9-1.1, fxNode3 at
    1.25 / 1.35, gone by 1.5 s at the cut); Rushing Falcon, Tower Rush's ogre, Rising Vortex, Water Monkey / Crane's
    clones on her; Sp Transfer's bolt to (0, 0.6, 9.9) 0.5-0.8 s; Nine Dragons' cast, the eight dragons from her hands
    arcing R / L in turn onto the target (0.4-1.9 s), the bites, the King's weave 1.6-2.0 s, kingRise, the eight strikes
    and the fall at 3.35 s; Yin Yang Fist's charge, the seal at her feet from 0.55 s (+-8 m), the burst with its upright
    disc, bamboo, leaves and smoke from 1.75 s (the three new shaders compile and draw); KO's deadEffect.
  - **Bug found and fixed (index.html Fx, wardrobe/fx_cues/panda.json, wardrobe_fx_check.py):** Rising Dragons'
    `risingDragon` and Nine Dragons' `tto/nineDragons_kingRise` carry their dragons with the prefab's own Animation out
    of the ground and down through it at the end (14 m and up to 24 m under the floor), which the game's ground hides;
    the page drew them whole under the floor (the dragon's lower half below the ground ring while it rose, its tail
    hanging under the floor to 4.1 s / 4.2 s). New cue option `floor` (true: every mesh of the effect clipped at the
    hero's ground, the same clip the Chameleon's falling bolts got, now one helper `clipFloor`), set on those two cues
    (their whys say so); OPTS += floor. The helper also takes a material list (the dragons' skins are one: the old code's
    `m0.clone()` would have thrown on it) and the two dispose lines free each material of a list. Shots:
    checks/fx_panda_qa/fix_sheets.
  - Looked into, not bugs: raijinKen_ring2 drawing again at 7.0-7.5 s (two of its emitters have Delay 2.0 in the
    prefab); the cyan Panda double behind her in Heaven Palm / Lotus Palm / Water Monkey / Crane (the rings' own
    mesh); Climbing Cliff's blue figure beside her (climbingCliff_ring's mesh); the Three Steps trails drawn round her,
    not on her hands (the prefab's Animation carries them along the dash she does not make, decision 20); the Tempest
    Dance aura's age jumping to its after-life at 5.0 s (followState's cut, as the Bat's castRing); skinned meshes'
    boxes reading far off (the box tool takes their bind-space bounds: the King's y -7..6); the dragons' boxes living
    to 1.2 s after their 0.7 s flight (NineVanish's 0.5 s with the trail fading); Pummel's arms at opacity 0 for the last
    0.2 s of their 0.5 s life (the prefab's fade).
  - Gates: `wardrobe_fx_check.py ... checks/fx_panda_qa/gate dark --cls panda` exit 0, errors [] (43 tile plays, on the
    final code); files-only every class "no problems"; the page's shared Fx code changed, so also `--cls
    wolf,sheep,penguin,bat,bison,cat,chameleon,mole,monkey` (checks/fx_panda_qa/regress): exit 0, errors [] (408 tile plays); unit tests 67
    OK, node 9 pass, test_adopt_from_video.ps1 fails 0; `wardrobe_weapon_fx_check.py` OK; index.html LF.
    Not committed.
  - For the user's eye: the floor clip on the two dragon effects (the dragons now rise out of the ground; a camera
    orbited under the floor no longer sees them below it); Tempest Dance's pale helix on the white stage; Fuujin Ken's
    clouds 13 m out and the target-point effects outside the default camera's frame, as for the other classes; the
    Yin Yang burst's upright disc filling the near view; decisions.md's overnight calls and the editor's judgement calls
    above.
- **The helmeted one: cleavage at the chest, the front piece's seam** (user: "add some breast cleavage texture, can copy
  form Bat texture we have"; "fix the seam"). (1) The seam was a stripe of plain cloth down the piece's middle: her
  tabard's own middle is its island's edge, left unread (inset), so spots at u ~ 0 found no texel within reach. Inset
  1.5 texels now, and near the middle (u < 0.25) her nearest texel is taken from up to 2 cm. (2) The chest's light and
  shade come from the Bat's **summer** texture: its skin between and above the bikini's cups (skin picked by colour),
  read `CLEAVE_UP` 8 cm higher and `CLEAVE_WIDE` 1.3 x wider, put through her skin's colours. (3) **Royal's hanging
  tab**: its front face is part of the capelet's island (the middle, z < 1.21, x > 0.11), only its back face is the
  island at 236,286. Two passes painted the back face alone and the tab stayed dark; found by listing every island at
  the chest's middle with its position and present colour. Both faces are skin with the cleavage's shade now: the
  tab reads as the chest.
- **The cleavage redone under the trinket** (user: "it should be underneath the trinket, the trinket itself shouldn't get
  recolored to show cleavage"): royal's hanging tab (both faces) keeps its own dark paint again; the cleavage is on the
  chest behind it only: the summer texture's shade (`CLEAVE_WIDE` 1.9, `CLEAVE_K` 4.5) plus each breast's round
  (`BREAST`: a light on top, a soft line under). From the front the trinket covers the middle 3 cm each side, so only
  a sliver of the chest shows beside it: the shading is slight there, more from the side.
- **The cleavage drawn, not shaded** (user, with a close-up: "I checked visually, there's no cleavage at all"). Measured on
  the texture by position: the summer texture's shade was there, but grey (the skin ramp's dark end) and almost all
  within 3 cm of the middle, behind the trinket; beside it the skin was flat. Now drawn as her own sheet draws hers:
  each breast's upper line from the meeting point (`CLEAVE`: z 1.122) up and out to |y| 5.5 cm, so it crosses the
  chest that shows beside the trinket: a warm dark line (her strokes' colour, warmed), a soft shade on the sternum's
  side, a light on the breast's side, and the line between the breasts below the meeting point. The summer-texture
  reading, `CLEAVE_UP / _K / _WIDE` and `BREAST` are gone.
- **The cleavage copied from the Bat's summer texture; the lining on the coat's inside** (user, of the two lines I had
  drawn: "why do you think a straight line is fit to represent a cleavage?"; "the right robe piece, the silver lining
  didn't align nicely along the edge of the coat like the left side, is it a mirrored skin problem?"). (1) The drawn
  lines are gone. The chest takes the summer texture's own painted chest: its skin between and above the bikini's cups
  (picked by colour), seen from the front, read `CLEAVE_UP` 10 cm higher (the cups' meeting point on the neckline)
  and `CLEAVE_WIDE` 1.5 x wider; only its light and shade (luminance as a share of the summer skin's, `CLEAVE_K`),
  warm-tinted, on her skin (its colours carried the bikini's cool edge). plans/reskins/bat/eyes/chest_under_trinket.png
  = that paint from the front with nothing over it: a soft crease with round shades. From the front the trinket
  covers the crease; the sides' soft shade shows. Eight Bat outfits' chests were laid side by side first (summer,
  bathRobe and queen paint a bare chest). (2) **Not a mirror problem**: 99.5 % of the coat's texels have a triangle
  on each side. The idle pose swings her left flap open and shows the coat's INSIDE (its own island, 452,337), whose
  sheet border is not the cloth's edge, so its lining ran astray. The inside now takes the lining by its distance on
  the body to the outside island's border (2.4 mm per sheet texel there; 9 % of the inside lies within the lining).
  Tried and dropped: the mesh's open edges as "the real hem" (`open_edges`): the coat is a closed shell, it has none.
- **The chest is the breasts' underside** (user: "it doesn't show in the model still, because the position should be the
  underboob, not the upper cleavage, so there's a little of manual repositioning and improvisation left for you").
  Read off the mesh (the panel's top, per height): above z ~1.175 it comes forward and faces down (nz -0.35..-0.6),
  below it is the near-upright ribs (nz -0.17). The summer cleavage copy is gone. Painted on that shape, soft and
  warm: the fold under each breast (`FOLD`: lowest z 1.172 at |y| 4.5 cm, rising to the middle), the underside in
  shade above it, the cast shade on the ribs below it fading down. It shows from the front beside the trinket (the
  fold lies at the top of the skin that shows). eyes/chest_under_trinket.png = the paint alone, chest_closeup.png =
  the model from three angles.
- **The helmeted one is done** (user: "Lady Noir looks good now, prepare it on desktop for me to publish"). On the office
  Desktop, `wardrobe_reupload\lady_noir_face11\`: `12tails_ค้างคาว_Royal.png` (outfit royal, 1024 px) and
  `12tails_ค้างคาว_Butterfly_Hood.png` (head butterflyHood, 512 px), both opaque, + preview_front.png. File names =
  12tails_<class in Thai>_<the page's humanize(item) with _ for spaces> ("Butterfly_Hood", not "butterflyHood": dropMany
  matches the humanized name). Tested headless: dropping both on the Bat puts royal + butterflyHood on with both
  skins, no page errors. The user sends it from the page themselves (face 11).

## 2026-11-13 (office), the Rabbit's effects: built and cued

From plans/fx_rabbit/ (six reports, each with its "## Verification", which wins; decisions.md decided overnight for the
user's review). One editor after three builders (rabbit, generic, page_pipeline), on the office PC.
- **Parts (new):** fxparts/rabbit.js (`LightGolem`: Contract's golem plays its own `root` clip looped from the spawn, its
  own LightGolem1 material, no AI; class-guarded); fxparts/tto_rabbit.js (TTO's RabbitSpin, PowerUpRotation (not
  class-guarded: a generic store script, on the uncued bountyHunt_claim), the movers Rabbit.PosterFly (0.25 s arc to `to`,
  spinning 900 deg/s, nothing on arrival), Rabbit.CoinRise (0.35 s ease to the hang spot, the bob from the cue's clip time
  `fx.at.at` + age) and Rabbit.TurretCapsule (0.25 s to `to`, then medicTurret_hit at `to` and `kind` at `ally`, kill 2),
  and RabbitMedicTurret (the Model's 0.45 s grow, beats at 0.75 + 1.5 k s while age < `end`: beat, head snapped to the
  ally, shot and capsule from the Muzzle node, the drop a third each; at `end` the break and a 0.4 s shrink));
  fxparts/control.js: `EffectControl(root)`, the root's faceCamera / faceUp (modes 2 / 3) while age < life, with cue
  option `owner` + followPosition: the root at owner + R x (spawn - owner) (statScan swings round the target), for every
  class (the child part's mode code moved into one `faceTurn`, unchanged); fxparts/sheep.js: `fx:cAttack_charge` returns
  null unless the Sheep (the Rabbit's cAttack_charge shares the name). index.html (page_pipeline): SEQ / SEQ_SKILL rabbit
  (decisions 1-10, 13), ITEM_SETS.rabbitShotgun (isShotgun's 10 props), the cue kind `propCopy` (HeroPropCopy: a copy of
  the worn prop, weapon_fx too, on a hero bone at the worn prop's world scale), cue options `yaw` (FX.yaws, one angle per
  play per name), `sphere`, `replace` and `"random"` inside a rot list (rotOf now returns a fresh array), HERO_SKINS
  rapidTrance, the `EffectControl(root)` call in the Fx constructor, FX_PART_FILES += rabbit, tto_rabbit, the cue-format
  comment. **Mine (index.html Fx.update):** an effect with no EffectControl and nothing left to draw was disposed on its
  first frame even with a cue's kill: the scope (sniperCamera: Transform, script, the playOnAwake-off deadShot AudioSource)
  went before its playAudio 0.1, so the deadShot never played; such an effect now lives to its cue's kill (every other
  cued effect with a kill has an EffectControl or something drawn: no other class changes). wardrobe_fx.py: LAYOUTS
  Rabbit_potion, Rabbit_sniperCamera, the four 0-byte scripts, LightGolem, LightGolemAI; SHURIKEN_FROM_TTO rabbit
  extravagance_ring (no SHURIKEN_MAT); EXTRA_FOLDERS rabbit lightgolem. wardrobe_fx_tto.py: SKILL_FX rabbit (25),
  CODE_MOVERS medicTurret_capsule / bountyHunt_poster / coinRicochet_coin. Nothing the video repo reads was renamed.
- **Cues** (wardrobe/fx_cues/rabbit.json, 53 keys, 282 cues: 206 fx, 62 voice, 9 sound, 3 hideProp, 1 skin, 1 propCopy; 94
  effect names, 17 of them TTO; assembled by checks/fx_rabbit_build/editor/assemble.py, git-ignored): attacks_emotes'
  block with its Verification's nAttack / cAttack3 (its From the Above block dropped); skills_a Verification's whole block
  (no Mall voices); skills_b's block with its Verification's statScan (`owner`), `@Contract:bow`, medicalShot, and its
  tenShot (not parts'); effect_only Verification's `@FromtheAbove:bounce1` / `:bounce2` (empty, a guard); tto section 7's
  bountyHunt / coinRicochet and its Verification 2's medicTurret. Applied on top: decision 39 (cAttack2 = the scope cue
  `sniperCamera` {y 1.05, d 0.15, playAudio 0.1, kill 4.2}, its why rewritten, not attacks_emotes Verification 2's sound
  kill); decisions 31 / 33 / 55 (the turret cue `replace`, medicTurret_deploy's bare 1.8 written {"d": 1.8}).
- **Tiles / icons:** wardrobe_skill_icons.py CLIP_SKILLS rabbit maim -> maimShot, OWN_TILE rabbit customizedShotgun /
  fromTheAbove / contract, RANK_ICONS rabbit (decision 13's 14 card icons + cAttack3 and customizedShotgun2, below); rerun:
  rabbit 34 HD icons for 43 clips (14 new webp: acidicField, boostShot, contract, customizedShotgun, diamondShot,
  fromTheAbove, healingField, heatShot, immuneShot, lifeShot, maimShot, miracleBlend, shake, stickyGum; 11 replaced by the
  card's picture: backpack, cAttack, circleShot, fourShot, gorgonShot, mall, millionaire, rapidTrance, shootingArray,
  statScan, truceTrading); index.json rabbit only, no other class changed. No NEVER_PLAYED / LIFTS for the Rabbit.
- **Check / inventory:** wardrobe_fx_check.py KINDS += propCopy (its slot one of R / L / Head / Back, `bone` a string; not
  expected: it takes hold only with a prop worn), OPTS += yaw, sphere, replace, owner, ally, delay (not kind); names()
  splits a builds name "a|b" (wardrobe_fx.py already built every name of one). wardrobe_fx_inventory.py BUILT += the 14 of
  decision 57, NOTES rabbit extravagance_ring (grafted: drawn), CLASS_NOTES rabbit (castStar / castLight / deadEffect /
  mall1-5 / the drinkers' looks / the golem, and the ten missing prefabs); rerun: the Rabbit 83 / 84 ready (the 1 left:
  extravagance_ring's grafted ParticleSystems, drawn).
- **Data:** `wardrobe_fx_tto.py rabbit`: 25 TTO effects, 61 materials, 55 textures, 11 sounds; `wardrobe_fx.py rabbit`: 77
  effects, 70 materials, 66 textures, 110 sounds (the two extravagance_ring graft lines printed, Gil and star5).
  data/rabbit/fx.json 102 effects (3.0 MB; LightGolem 26 nodes with its root / run / ko / getUp / dead clips), sfx/ 111
  files, 65 new textures in data/fx/tex: all new files, to commit with the run; the other PC pulls.
- **Judgement calls (mine):** RANK_ICONS cAttack -> rabbit_cAttack3 and customizedShotgun -> rabbit_customizedShotgun2
  (decision 13 says to compare nAttack / cAttack with their cards; the cAttack card's picture differs from cAttack4, and
  the Customized Shotgun tile's card differs from customizedShotgun4 the same way; nAttack4 is its card); the turret's
  drops as one builds pick `"lifeShot|boostShot|heatShot"`: written as three names, the check expected all three from 7
  random draws (a ~17 % flaky gate); the Fx disposal fix above; skills_b's harmless ring cuts (medicalShot_ring 1.7,
  shootingArray_ring 1.8) kept as its Verification allows; the turret probe (7 beats, 7 capsules, 7 hits, the break, gone
  by 11.5 s), the scope (live 1.0-5.2 s with its sound) and Ten Shot's copy (timeShotgun worn: the copy on mountHand_L at
  the worn world scale 0.93, gone by 3.2 s) checked headless (checks/fx_rabbit_build/editor/probe.py).
- **Gate:** files-only (every class with cues) "no problems"; `wardrobe_fx_check.py ... checks/fx_rabbit dark --cls
  rabbit` exit 0, errors [], 52 tile plays (Truce Trading once per outcome), every expected effect spawned, 78 sounds
  loaded (on the final code); the page and shared parts changed (index.html's cue options / propCopy / Fx disposal, control.js, sheep.js, the check), so also `--cls wolf,sheep,penguin,bat,bison,cat,chameleon,mole,monkey,panda` in one run (checks/fx_rabbit_regress): exit 0, errors [], 451 tile plays; unit tests 67 OK, node 9 pass, test_adopt_from_video.ps1 fails 0; `wardrobe_weapon_fx_check.py checks/fx_rabbit_build/editor/weapon_fx_check.png` OK.
  index.html LF. Not committed.
- **Left out:** decisions 44-48 (the scope's camera and GUI, the messages, Mall's shop UI, Stat Scan's and Coin Ricochet's
  chat; the status looks on others, the bounty claim; gear procs, numbers, pickups; the missing prefabs snipeShot_hit,
  kneeShot_hit, herbFinder, contract_ring, fourShot_hit, circleShot_hit, tenShot_hit, mall / mall0 / mall6; the plain
  rifle path). Nothing else: every skill decided is cued. Built, not cued: tto/bounty, tto/gilded, tto/bountyHunt_claim,
  autoLife / enlarge / reduce / miracleDrop.
- **For the QA pass:** nothing has been looked at in a screenshot except Ten Shot's second gun (it reads right: the copy in
  her left hand, pointing up like the worn one). To look at: statScan facing the camera and swinging round the target
  (EffectControl(root), the camera behind: about 0.3 m behind the target's centre line), bounce1 / fromTheAbove_ring's
  faceUp; the potions' and stars' ring turned by one `yaw` per play (stars and bottles in line); Millionaire's 18 coins
  within 2 m, each its own yaw; the fields and the gum on loop (`replace`: one of each); the Mall stall by colour (mall3-5
  share one material); the Light Golem 3 m ahead (its root loop, its material); Rapid Trance's purple; the Medic Turret's
  grow, head turn to her, capsules flying back to her chest and the drops at her feet, its shrink at 10.55 s; the poster's
  arc from her left hand to 0.6 m above the chest; the coins' rise and bob meeting the shot tracers; the hired guns'
  muzzles 14 m out and 7 m up (outside the default frame); extravagance_ring's grafted coins and stars; the sniperCamera's
  deadShot (heard 1.1-5.2 s of the Charge Attack tile); the Normal Attack's floor ricochet at 11 m and the shotgun
  variant with a shotgun worn. Rolled procs the gate does not expect: KO's deadEffect (p 0.5), Knee Shot's maimShot_hit
  (p 0.8), Miracle Blend's golden bottle (p 0.05 per bottle).
- **For the Bible (offer, not written):** decisions.md's last section.
- **QA pass (13/11/2026, office).**
  - **What was shot.** `wardrobe_fx_shots.py --jobs` (virtual clock). The jobs file is checks/fx_rabbit_qa/jobs.json,
    written by make_jobs.py: 70 jobs covering every Rabbit tile.
    - Normal Attack: bare, and with traderGun worn (the shotgun path); Customized Shotgun.
    - Charge Attack to 6.2 s; Bounce and From the Above to 10.3 s.
    - Maim Shot, and again with maimShot_hit forced.
    - Gil / Diamond Shot, Gorgon Shot, Backpack (standardGun worn, for the hide), Four Shot (side, top), Circle Shot,
      Extravagance.
    - Mall to 8.2 s, plus outfit colours 2-5.
    - Mix / Shake / Miracle Blend to 11.6 s, and Miracle Blend with two golden bottles forced (mix3!pot1+mix3!pot3).
    - The three fields and the four Medical Shots; Rapid Trance to 11.3 s; Stat Scan (side, front, behind).
    - Truce Trading, both outcomes (seqAlt:1=0 / 1); Contract to 10.3 s.
    - Shooting Array, Millionaire (side, front, top); Ten Shot bare, with timeShotgun and with standardGun.
    - The three TTO tiles: Bounty Hunt (side, front, far), Coin Ricochet (side, front, near), Medic Turret to 11.5 s.
    - KO (dead forced, and as rolled), getUp, run, and 22 emotes (wave ... pose66, clap, wai, dance).
  - Both stages: 826 shots each, dark and white. Sheets: checks/fx_rabbit_qa/sheets_dark and sheets_white (git-ignored;
    shots and logs under run/).
  - Extra checks (checks/fx_rabbit_qa/probe, probe_sheets):
    - A top / near / front set for the gum, the fields and the turret.
    - replace_probe.py, run with the skill tab's วนซ้ำ on.
  - Page health: no page error, no stalled render loop, no failed job. The only console lines are swiftshader's
    glBlitFramebuffer feedback warning.
  - **What matches** (boxes in the hero's frame, +x = her left):
    - **Normal Attack and Charge Attack.** The Bouncing Bullet tracer meets the floor at 11 m at 0.3 s, and the second
      tracer leaves the floor 0.02 s later. With a shotgun worn: shotgun_fire / _hit only. Charge Attack: the charge at
      0 s, the scope drawing nothing 1-5 s, then the release and cAttack_hit at (0, 1.05, 9.83) at 5.0 s.
    - **Bounce and From the Above.** Bounce leaves the frame by 0.7 s. The hero is hidden 0.9-9.5 s and falls back in on
      bounce2. fromTheAbove_ring draws from 9.9 s: its emitters have Delay 1.0, so it shows 1 s after its 8.9 s cue,
      which is the game's 9.9 s step. From the Above's six air shots come down from 12 m onto (0, 0.36, 9.7) at 1.1 ...
      8.6 s.
    - **Shots at the target.** Maim / Gil / Diamond / Gorgon / the Medical Shots hit at the 10 m body at their cued times.
    - **Four Shot** fires forward, back, left and right at 0.4 / 0.7 / 1.0 / 1.3 s (identity rotation, as the code).
    - **Backpack** hides the worn gun 0.2-1.0 s. **Circle Shot**'s three bursts come above her.
    - **Extravagance** draws its grafted coins and stars (0.4-0.8 s).
    - **Mall.** The stall comes in by colour: red, blue, then green for colours 3-5 (mall3-5 share one material).
    - **Potions and stars.** The stars of Mix / Shake / Miracle Blend land on the bottle spots (one `yaw` per play, in
      line). The bottles stay to 11.4 s; the golden winged bottle shows at the forced slots.
    - **Sticky Gum** is centred about 2.4 m ahead, radius about 2.5 m, read off the top view. Its box (z 4.4-10) reads
      wrong because the gum is a skinned mesh.
    - **The fields and the turret** keep one live copy each across loops (`replace`). The potions stack: 5, then 20 by
      8 s.
    - **Rapid Trance**: the potion in her left hand 0.4-1.3 s, the purple tint 1.1-11.1 s, back at 11.3 s.
    - **Stat Scan's** mark sits on the target and faces each camera (side, front, behind).
    - **Truce Trading**: the flag in her left hand, then success or fail.
    - **The Light Golem** stands 3 m ahead from 0.1 s, animating: frames differ between samples. Its own teal
      LightGolem1 material; gone at 10.3 s.
    - **Shooting Array**'s three shots and finalhit land at the target. **Ten Shot**'s volleys go in the code's
      directions, with nAttack_hit x2 at 2.5 s. The worn gun's copy shows 0.2-2.8 s: three hero meshes, two at 2.9 s.
      Nothing is copied when no gun is worn.
    - **Bounty Hunt**: the poster's arc from her left hand to the chest + 0.6 by 0.65 s, then the pin, the flare going
      up, and the three hired guns at their fixed spots at 1.15 / 1.35 / 1.55 s.
    - **Coin Ricochet**: four coins rise and hang. Each is pinged at 0.75 / 0.95 / 1.15 / 1.35 s, in order from her left,
      then ricochets onto the target and cashes out at 1.42 s.
    - **Medic Turret**: it grows from 0.55 s, beats at 1.3, 2.8, ... s, and sends capsules back to her with a drop at her
      feet. It breaks at 10.55 s and is gone by 11.0 s.
    - **KO**: deadEffect when forced.
  - **Bugs found:** none. No file was changed by this pass.
  - **Looked into, not bugs:**
    - **Millionaire's peppers** spawn 4-6 m out. The prefab's Animation rolls each one from +6 m through its root to -6 m
      over 2 s; the root itself is within 2 m (`sphere`).
    - **The Gorgon beam** looks near-white on the dark stage. It is an additive cyan / pink texture with both faces
      drawn; the white stage shows its colours.
    - **The TTO shots' 10 m streak** (coinRicochet_shot, medicTurret_shot). Their Muzzle's LineEmitter (endRadius 10)
      points along the hero's facing, because Row6Tracer spawns at identity. Example: the turret's shot back at her
      streaks forward, away from her.
    - **statScan_dust** draws nothing in the samples: its emitters have Delay 0.3 and Life 0.4, which no sample hit.
    - **Box readings.** The skinned meshes' boxes (the gum, the golem, the bottles) read in bind space.
    - **The miracle bottles** hover 0.3-0.45 m up and spin: that is the prefab's looped root clip.
    - **The floor's contact-shadow disc** stays while the hero is hidden in Bounce. It is the stage's, as for every
      class.
  - **Gates (on the final code, unchanged by this pass).**
    - `wardrobe_fx_check.py ... checks/fx_rabbit_qa/gate dark --cls rabbit`: exit 0, errors [], 52 tile plays.
    - Files-only check for every class: "no problems".
    - Unit tests: 67 OK; node 9 pass; test_adopt_from_video.ps1 fails 0.
    - `wardrobe_weapon_fx_check.py`: OK. index.html is LF.
    - No regression run: no shared code changed in this pass. Not committed.
  - **For the user's eye:**
    - Snipe Mastery's hit and the other missing prefabs draw nothing (decision 17 / 47).
    - The Light Golem's size: about 2.5 times her height.
    - The white sacks on the Mall stall.
    - Millionaire's peppers rolling across 12 m.
    - The TTO shots' forward streak.
    - The hired guns 14 m out and the target-point effects outside the default frame, as for the other classes.
    - Decisions.md's overnight calls and the editor's judgement calls above.
- **The front piece's cut at the waist** (user, after seeing the skin: "the seams here is not connecting cleanly, it
  looks like a sudden crop even though there's no 3D shift there"): above `TAB_TOP` the piece had kept an earlier
  reading of her bodice (another purple, loose lines) and the fitted pattern and its border began at TAB_TOP. Now one
  cloth and one border for the whole piece from the neckline down (the bodice reading and `TABARD_FIT` are gone), the
  waist sigil on it, the tabard's pattern fading in over 3 cm under the sigil. The Desktop files were replaced.
- **The front piece above the waist carries her bodice's lines** (user: "it part above the horizontal cut earlier looks
  bad, not textured and no patterns compared to below"): the plain cloth there now takes her dress's front at the same
  height, laid across the piece's own width as the tabard is (u = |y| / the piece's edge; her bodice's half-width per
  height from its 98th percentile), its cloth colour scaled to the tabard's so the two join, cross-faded over 2 cm at
  `TAB_TOP`; the drawn waist sigil and the piece's border go over it. The Desktop outfit file was replaced again.
- **A deeper neckline** (user, a box just over the waist sigil: "more exposed skin almost reach the circle sigil"):
  `NECK` 1.035 (1.085 before), `NECK_K` 1.6 (0.6): a deep V of skin from the chest down to just over the sigil, its
  sides where they were; the silver edge and its dark line are measured across the neckline now (in height they came
  out thin and jagged on the steep V). The Desktop outfit file was replaced.
- **The neckline is a U** (user: "U instead of V"): `neck_z(y)` = NECK + NECK_H * (|y| / NECK_W) ** NECK_P (1.035, 0.080,
  0.050, 3.5): a round bottom just over the waist sigil, upright sides; `neck_n(y)` measures its silver edge across
  the curve. The Desktop outfit file was replaced.
- **A faint midriff** (user: "add a bit of midriff texture on the bare skin part? just a faint texture"): the Bat's summer
  texture's belly (plain but for its navel, z 1.004, under the U's edge) read `NAVEL_UP` 5.2 cm higher so the navel
  sits inside the U over the sigil, its light and shade at `MIDRIFF` 1.0, plus a soft wide centre shade (5 %%), below
  the breasts' fold only. eyes/midriff_closeup.png. The Desktop outfit file was replaced.
- **No navel: it belongs lower** (user: "how sure are you that belly button is supposed to be there? it is not too high
  right?"). Measured on every Bat outfit with a bare belly (a navel-like dip in the skin down the middle, garment edges
  left out): summer 1.008, nude 1.007, warlock 1.007, illusionist 0.997, i.e. the game puts it at z ~1.00-1.01, under
  the U's bottom (1.035) and its silver edge. The previous pass had moved it 5.2 cm up into the U: wrong. Now the belly
  reading stays at its true place (so no navel shows) and the midriff is a soft wide centre shade (7 %) and the belly's
  roundness toward the U's sides (6 %). `NAVEL_UP` is gone. The Desktop outfit file was replaced.
- The midriff stronger and tighter (user: "too faint and diffused"): `MID_LINE` 0.15 (centre line, 4.5 mm wide), `MID_SIDE`
  0.12 (the sides, a 0.8 cm transition). Desktop outfit file replaced.
- The midriff's shades blended (user: "the 2 shades there didn't blend nicely"): the side shade had a hard step (|y|
  2.2-3 cm) and started at the breasts' fold; now a wide ramp (|y| 1-4.6 cm) running on into the underside, and the whole
  factor smoothed on the body (1.5 texel sigma, normalised at the edges). Desktop outfit file replaced.
- **The coat's back and a belt: original designs, mocked for the user's pick** (user, of a band across the coat's back in
  the 3D view: "I found a forced painting ... please design this according to the theme of this character, your own
  designs and give me several mock variants, no forced repaint"; then "I think textured belt with dark red as the main
  color can be quite a good contrast for the lower body"). The band = her skirt read onto the coat's back (`COAT_BACK`
  "ref") over royal's belt height. `coat_back()` paints the back as clean cloth (form + drape, not royal's paint) with
  an original design: eye | contour | spine | hem | plain; `belt()` draws a dark red belt round the coat at `BELT_AT`
  (z 0.84 +- 0.028, where royal's belt flaps sit; the flaps take its red; her wing-edge red as a ramp, silver piping):
  weave | braid (+ an eye plate behind) | plates (+ silver studs). `wardrobe_bat_enemies.py backs` ->
  eyes/back_variants.png (A-D, no belt), `... belts` -> eyes/belt_variants.png (E-H: back, three-quarter, front).
  The back's mirror seam no longer gets a lining (it is an island edge, not the cloth's). Defaults stay "ref" / "none"
  and look/royal.png + the Desktop file are unchanged until the user picks. Open: a small pale drop on the back's
  middle near z 0.5 (to clean with the pick).
- **The belt mocked was the wrong one** (user: "commit push, we will polish this further at home, you missed mark
  entirely, that is not the correct belt I'm referring to"). The dark red belt of belt_variants.png goes round the coat
  at hip height (z 0.84); which band the user's screenshot shows was never checked against the islands (rule 12 of
  the skill: show back which piece was understood before a full pass). Not applied anywhere: `COAT_BACK` "ref", `BELT`
  "none", look/royal.png = the version on the office Desktop. Continues at home: HANDOFF.md. Committed for that: the
  painters, the skill, the two Bat skins' look files and mock sheets, the Cat knight's two files (not the user's
  reference pictures, not plans/reskins/bat/ref (game files: rebuilt at home), not _cache / shots; the Whale, the Cat
  shorts and the Rabbit folders stay on the office PC, unpicked).

## 2026-11-13 (home), the Panda's Wind & Cloud and Rain & Storm (the HANDOFF item)

- Data: `uv run --no-project --with UnityPy --with pillow python pipeline/wardrobe_data.py --only panda --no-props`
  (TTO 2026-11-04 bundles from the video folder): clips.json gains exactly `wind&cloud` (3.6 s) and `rain&storm`
  (3.0 s), skill, not TTO; nothing else in it changed. **Gotcha:** the run also rewrote 55 Panda outfit textures (WebP
  re-encoded by this uv env's Pillow: same pictures, mean 1 level off, max ~38) and dropped the ToT `student` outfit
  from outfits.json (meta.json's outfits 22 -> 21), which only `wardrobe_tot.py` adds back. Kept only the real change:
  the textures, outfits.json and meta.json restored from git, then meta.json's Panda `clips` set to the new ones
  (same compact JSON; the rest byte for byte). A future `--only <cls>` rebuild: diff before committing, and run
  `wardrobe_tot.py --only <cls>` after it if the outfits are kept.
- Icons: `wardrobe_skill_icons.py` (its `&` pattern was already in): icons/hd/panda/wind&cloud.webp, rain&storm.webp
  and their index.json entries; nothing else changed.
- Cues: the two entries of plans/fx_panda/effect_only.md Verification item 3, verbatim, appended to
  wardrobe/fx_cues/panda.json (21 + 6 cues).
- Effects: `wardrobe_fx.py panda --fx windCloud,rainStorm --voices windCloud1,windCloud2,rainStorm1,rainStorm2
  --sounds windCloud,punch1`: fx.json gains only `windCloud` and `rainStorm`; new sfx v_windCloud1/2, windCloud (the
  rest already there, identical).
- Gate: files-only, every class: "no problems".
- Gate: `wardrobe_fx_check.py D:/12tails-wardrobe checks/fx_panda_amp dark --cls panda`: exit 0, errors [], sound ctx
  running (90 loaded); `wind&cloud` spawns its windCloud rings from 0.29 s, `rain&storm` its rainStorm bursts; the peak
  shots show both, each tile with its Bible icon. No page or shared code changed, so no regression run.
- The usage guard's `--once` read weekly 98.0 % right before the Whale's workflow; the user then: "lift the usage guard
  permanently" (CLAUDE.md and plans/goal_fx_all_classes.md updated: no guard any more). `pipeline/workflow_class_fx.js`
  now takes `pc: "home"` (D:/ paths, the video folder's TTO 2026-11-04 bundles; default stays the office).

## 2026-11-14 (home), the helmeted Bat skin: finding the coat's band

- References rebuilt at home (`wardrobe_enemy_ref.py`, the HANDOFF line) and `wardrobe_bat_enemies.py eyes` run: its
  look/royal.png does **not** match the committed one (72k texels differ, all on the coat's outside island 441,190:
  the silver lining sits further in and the gutter takes the cloth). On the model the two look nearly the same. The
  committed file (= the one on the office Desktop) was made before the mock passes changed the lining code (the back's
  mirror seam), so the painter's defaults no longer reproduce it exactly. The committed png is kept; the rebuild sits in
  eyes/_cache/royal_rebuilt.png (not for git).
- **`pipeline/wardrobe_skin_views.py`** (new): skins on the hero from any yaw:pitch (below too), zoom and aim height;
  `--islands` numbers every UV island where it shows (rays through the page, uv -> island) with a legend (island ->
  sheet point, z range, size). Royal's islands at the back: 9 = the coat's outside (441,190), 26 = its inside
  (452,338), **33 = a zigzag strip round the coat's back at hip height (499,425; bind z 0.54-0.64)**: royal's own
  belt, a separate island, painted as plain coat cloth today. eyes/views_band/sheet.png shows it in red.
- **Belt mocks on island 33** (user: "Yes, it's the zig zag"). `belt(J, strip, silver)` replaces the office's belt round the
  coat at z 0.84 (the wrong piece; its royal_belt_plates / _weave_eye and belt_variants.png removed). Laid out on the
  strip's own shape: s = arc length along it from the back's middle (the strip's end, a mirror seam; 67 cm along the zigzag
  per half on the body), v = across it from its sheet rows (it lies upright in the sheet, sheet x 494-505, y 363-487;
  v flipped so 0 = its top edge). Each design a height field shaded as relief lit from above, in her wings' edge red,
  a fine grain, silver cord piping both edges: I tooled vine, J braid (chevron plait), K studs + an eye clasp at the
  back's middle, L scales, M basket weave. `wardrobe_bat_enemies.py belts` writes look/royal_belt_<key>.png only;
  the sheet: `wardrobe_skin_views.py ... --views 200:-10,150:-25,180:-45 --zoom 6 --aim 0.36` ->
  eyes/views_belts/sheet.png (a row per design, "now" first). `BELT` stays "none" until the user picks.
- **Own designs too, previews from 8 sides full body** (user: "all these variants are from my dark red suggestions, come up
  with your own design too, the preview should be 8 angles view fullbody"). `belt()` gains five in her other colours
  (pal, read in eyes(): her sleeves' stripe tones 35,29,37 / 64,73,90, her wings' magenta 91,48,78 (x2 on the belt to
  show), her eyes' lilac-white): N eyes (small eyes + silver diamonds on dark purple), O chain (silver oval links and
  bars on near-black), P stripes (her sleeves' slanted stripes), Q contour (her wings' magenta lines + an eye at the
  back's middle), R lattice (a pale silver band, a dark purple diamond lattice). `wardrobe_skin_views.py --per-job`
  writes one sheet_<name>.png per skin (4 x 2, one crop for all its sides): eyes/views_belts8/sheet_<key>.png, with
  sheet_now.png for the present skin. Seen: the red ones contrast most with the coat; the purple / grey ones (eyes,
  chain, stripes, lattice) are quieter, the eyes and the chain read best of those.
- **Picked: Q, the wing contour lines** (user: "I like contour"). `BELT = "contour"`; look/royal.png rebuilt (opaque;
  pixel-identical to the mock). It also carries the painter's present coat lining (the rebuild noted above), not the
  office Desktop file's. eyes/views_final/sheet_look.png = the 8 sides. The ten belt mock pngs are removed (their sheets
  in eyes/views_belts8/ stay); `wardrobe_bat_enemies.py belts` writes them again.
- **The head, the hair, the back, cloth, an upscale** (user, with close-ups from the live view; all in
  `wardrobe_bat_enemies.py eyes`, look/royal.png):
  - **The helmet band, painted on the 3D head** ("when I look from below ... the silver metallic part bled into Bat's
    forehead and hair, it's almost like a cheap attempt at projection, can you fix this as if you are an 3D model
    artist drawing directly on the 3D model?"; then "the metal part still bled into the hair left and right, but the
    almond shape I redded should get the silver metal texture continued from the eye sigil ... no longer hair
    (illusion)"). The band was a reading from the front (`take(view=1)`) on hair + head: it also painted the forehead's
    skin behind the fringe (hidden from the front above z 1.53: measured with a front depth map of the hair; in full
    view from below) and her helmet's lower sides onto the side locks. Now: the skin carries no metal; the band is on
    the fringe island alone (90,174), on every face of it whichever way it points (the strands' side and under faces
    carry it on: one piece of metal), read ROUND the head (the angle about the head's axis x 0.02, and the height:
    `cyl`), her helmet's outward faces only. `BAND_ROUND` 95.
  - **The hair = the user's hair picture** ("the texture missed some hair"; then a picture of flowing dark red locks:
    "I want you to add hair texture too, don't have to be this exact texture"; of locks drawn by formula: "I don't
    like your hair texture, can you try overlaying my reference picture instead?"). `hair_picture()`: the picture
    (plans/reskins/bat/hair_ref.png, not for git: the user's; it came mid-turn and was read back out of the session's
    jsonl, `attachment` records) laid on the body: across = the angle round the head (+ 0.8 x the distance from the
    axis, or a lock's face that points round the head is one stretched column), counted from the front's / the back's
    middle; down = down the hair; `HAIR_PIC_W` 0.28 wide, mirrored across, cross-faded down (a mirror drew diamonds).
    Its light and dark through her hair's palette (174,139,149 / 217,178,193 / 243,210,221), the dark gaps deeper.
    **The hair's halves share their texels** (a mirror at the back's middle): slanted strands meet as chevrons there,
    so the picture's column where the strands run straightest lies on the middle (least slope of its light over a
    40 px window). Royal's own strand painting stays under it at 0.7.
  - **The coat's back** ("the back of the robe ... maybe it's from game model mirroring issues, but please fix if you
    can, the back of the robe texture is also a bit bland"). Not mirroring: the dark column down the middle was her
    back panel read onto the coat within 1.5 cm (`COAT_BACK` "ref"). Now `COAT_BACK = "wing"`: clean cloth, her wings'
    eye on the upper back (z 0.83) and their flowing magenta lines over the whole back (the belt's lines). The designs
    were re-placed round the belt (it lies at z 0.55-0.64; the old eye sat behind it): eye | wing | spine | hem |
    plain, `... backs` -> look/royal_back_<key>.png (not for git), sheets eyes/views_backs8/sheet_back_<key>.png.
    **The pale drop low on the back** = the coat's lining drawn on texels of the back's mirror seam at z 0.41-0.50
    whose |y| reached 0.0058 (the seam test was |y| < 0.005: now 0.008).
  - **The front piece "skewed to the Bat's right"**: not the paint. Its two halves are one set of texels mirrored at
    y = 0 (40 triangles each side, the middle's vertices all at sheet x 315, mirror pairs' uv equal to 0.005 texel), so
    a pattern cannot lean. The idle pose turns her hips about 10 degrees: from straight ahead the piece's right half
    is foreshortened and the coat's right flap covers its edge; from yaw 350 it is symmetric. The game's own royal
    paint leans the same way (eyes/views_front/sheet.png: original and look, yaw 0 and 350). Nothing changed.
  - **Cloth on the sleeves and stockings** ("add a bit more texture ... (don't add more patterns, please add things
    like texture, shading, or a bit of cloth wrinkles)"). `cloth_shade()`: light and shade multiplied onto the stripes
    on the limb's own coordinates (`limb()`: the way along, the angle round its middle line): roundness, folds along
    the sleeve (wardrobe_bat_robe.folds), creases at the elbow, the cuff, behind the knee and at the ankle, a sheen
    down the stocking's front, knit rows / ribs and a grain. `SLEEVE_FOLDS`, `LEG_CREASES`.
  - **Twice the size** ("is there a way to make the patterns looks more high res? can you try upscaling if it
    helps?"). It helps: `pipeline/wardrobe_skin_upscale.py` (new; `py -3.10`, home PC: torch + CUDA) puts a skin
    through the icons' Real-ESRGAN recipe in tiles (192 px + a 24 px margin thrown away) -> look/royal_2x.png, 2048 px.
    The ragged edges of nearest-texel readings and the 1024 px stair-steps on drawn lines come out as clean strokes
    (eyes/views_up/). As upscaled 5.0 MB, over the send route's 4 MB (LIMITS.fileBytes): saved at 7 bits a channel
    (off by 1 level at most): 3.7 MB. The page wears any size (composeTexture: skin width / base width). Painting
    at K = 4 instead was not tried (the painter's constants are K-aware only in part: belt relief, grain).
- **`wardrobe_skin_views.py`** grew: `--at <bone> [--lift]` (the page's own camera target sits in front of the hero:
  a view from below aimed with --aim looked at her chest), the shot read in the same task as the render (canvas
  toDataURL: the page's loop and its orbit limits pulled a low camera back before an outside screenshot), `--per-job`.
- **Her back panel copied whole; the hair picture off** (user: "Why do you hesitate to copy the back design from the
  reference image? Also remove the hair texture for now, it looks too much."). The hesitation was a wrong reading of
  2026-11-13's "forced painting ... your own designs" (said of one stray strip) and of the skill's rule 11; the rule's
  own answer was there: "bring the reference's patterns as whole motifs placed on a fitting piece". `COAT_BACK =
  "panel"` (coat_back): her back panel island (458,326: the pointed tabard, silver border, vine, two leaves, diamond),
  her paint texel for texel inside its own outline, on the middle of the coat's back: `PANEL_WIDE` 1.25 x wider
  (half-width 17 cm of the coat's 24 at the belt), its point raised from her z 0.37 to the hem's middle 0.405, a soft
  shade along its edge, the coat's clean cloth outside; above it her dress's back at its own place (the emblem
  between the shoulders). The wing / eye / spine / hem designs stay in the code. `HAIR_TEX = 0.0`: the hair is royal's
  own strand painting in her palette (HAIR_K 1.25); hair_picture() and hair_ref.png are only needed when it is on.
  look/royal.png + royal_2x.png (3.2 MB) rebuilt; eyes/views_final/sheet_look.png = the 2x from 8 sides.
- **Clean and sharp: review rounds on the model** (user, with close-ups: "assume direct camera to the back side of the
  robe, please fix so doesn't look like it is clipping"; "the patterns are beautiful but it is not sharp, some of it
  still looks like water color"; "see the model in 3D and reiterate until everything looks clean"; then "you are
  starting to lose way too much details on the robe"). Each round: paint, upscale, eight sides at two heights
  (eyes/review_low, review_up: `wardrobe_skin_views.py --at Spine1 --lift -0.42 / 0.12 --zoom 3.4 --per-job`).
  - **The back under the belt "clipping":** not the paint's seam. Under the belt the coat's back is a few large
    triangles, each half skinned to its own leg (the middle's vertices to both thighs): in the idle pose the halves
    shear and cross near the middle (a grid skin showed it: `--islands --rays 2` saves hits_<yaw>_<pitch>.npy), so a
    shape drawn across the middle there is cut on one side. Nothing crosses it now: her back panel, smaller
    (`PANEL_WIDE` 0.68, `PANEL_TO` 0.645), ends with its point on the belt; plain cloth under the belt.
  - **Sharp:** her 512 px sheet upscaled twice (`wardrobe_skin_upscale.py`, --bits 8) -> ref/LadyNoir_x4.png (2048 px,
    not for git; without it everything falls back to the small sheet). `ref_maps` loads it as R.hi (its light and
    dark, the small sheet's own colours: the upscaler tinted grey lines green); `wardrobe_borrow.fine()` reads her
    colour BETWEEN her texels (the outfit's point's offset from its matched texel, turned into a step on her sheet by
    least squares over the neighbours' places; steps over 1.5 texels = matched from beyond an edge: none), used by
    borrow(), the fringe band, the back panel, the front piece. Before, many outfit texels shared one of hers: blocks.
  - **Clean:** the coat is ONE cloth now (form + drape folds, as its back was), not royal's paint through a ramp (its
    light hem trim came out as a grey skirt). `strokes()`: only what she DRAWS there (differs from her cloth), never
    from her island's rim, fading toward it; with `depth`, her outermost layer alone (a depth buffer per 4 mm cell;
    picking among the nearest few flipped texel by texel: hatching, ragged edges). Used for the big eye on the coat's
    sides (over the belt only: under it her panel's hem made ragged bands and thorns, the user's boxed spot) and the
    emblem between the shoulders (|y| < 6 cm: beside it, stray hooks). The small sigil box on the front pieces is off
    (`SIGIL_HIP`; it is the same motif as the side eye; wrapped round the body and trimmed to its own diamond if on).
    The front piece: her tabard's top lies on the other side of her sheet's mirror line (y < 0), unread before: a comb
    of teeth down the V; read as |y| now. The lining's outer dark line a full texel wide (a quarter-texel line broke
    into teeth along the lapels). The sleeves' rings read between the profile's 2 mm steps (notched stripe edges).
  - **Detail kept** (the "too much lost" round had only a small sigil per hip): the big side eye back, and her border's
    second thinner line inside the silver lining along every edge and spike (`LINE2` 8.2 texels in).
- **Black dots, connected patterns, lashes; the lessons written down** (user: "what are these? black dots"; "make sure
  each UV islands connects cleanly when it assemble in the model"; "these two parts are the same piece, yet the
  pattern got cut awkwardly"; "explain why your own painting can cause such an unclean cut"; "anime eyelashes";
  "document all relevant lessons from this session").
  - Dots across the side eye: (1) the side reading's target mask was a hard test on the coat's per-texel normals:
    along the coat's own triangle edges (split normals) single texels fell out and kept the cloth colour; (2) her dark
    under-panel island was read with her dress island: single texels found it nearer. The same on the forehead disc
    (her helmet and brow layers flipping): the fringe band reads her outermost layer per 4 mm cell now.
  - **The side eye is unrolled, not viewed** (`unroll`: the angle about each surface's own upright axis x 17 cm, and
    the height; her dress round x -0.001, the coat round -0.032). Before: from the side (key x, z), limited by
    normals: cut where the coat turns to its front (the stem's neck, the rear leaf). Now the whole motif: eye, frame,
    four leaves, the stem up to her waist arc and down behind the belt (its lower limit z 0.585-0.595 is under the
    belt all the way round). Limits left: the front lining (22-32 deg) and her back panel (138-150 deg).
  - **The front piece is one reading**: `TAB_TOP` 1.0 (her tabard from under the waist sigil to the split);
    `TAB_UPPER` (her bodice's lines above 0.935, the old seam) off.
  - `strokes()` prints per limit how many drawn texels it ends; `--cuts` writes eyes/_cache/cuts_<name>.png (red
    reach, yellow her island's rim, green the mask) to render with wardrobe_skin_views.py; fragments under 30 texels
    are dropped; `key_src` for her own map.
  - **`eye_makeup()`**: face 11's eyes located in the preset's picture; `LASHES` 5 tapered curved spikes on the outer
    half of each upper lid (`LASH_LEN` 1.25), a wing past the outer corner, three short lower lashes; a plum shadow
    (mostly hidden under the preset's own half-opaque lid highlight). eyes/review_face/sheet.png.
  - Lessons: the skill's rules 17-24 (.claude/skills/reskin-from-image/SKILL.md) and the memory
    `feedback_skin_polish_standards.md` (the user's standards: copy the reference's designs, clean AND detailed,
    self-review in rounds on the model, 8-angle full-body previews, paint on the surface).
- **Lashes, stronger: four strengths mocked** (user: "you can try more aggresive lashes"). `pipeline/wardrobe_bat_lashes.py`
  (new): the skin painted once, the make-up put on a copy per variant (A now 5 lashes x 1.25 | B bold 6 x 1.7 | C
  dramatic 7 x 2.2 | D extreme 8 x 2.8; `LASH_W` thickness, `LASH_FROM` the first lash's place along the lid; from
  LASH_W 1.2 a second shorter wing and a fourth lower lash) -> eyes/lash_variants.png (flat, the preset on) and
  eyes/views_lashes/sheet.png (the model, four angles). Defaults unchanged (A) until the user picks.
- **Picked: C, with every lash rooted in the eye's line** (user: "C looks good, but make sure each eyelashes root reach the
  eye edge, don't make it looks float in solitude on the face"). Defaults `LASHES` 7, `LASH_LEN` 2.2, `LASH_W` 1.45,
  `LASH_FROM` 0.26. Roots: the eye's line = the largest connected dark piece of the preset's eye (before: any dark
  texel in the eye's box, so the crease line over the lid or a stray mark could be a "lid"); an upper lash starts 1.6
  texels inside its top edge; a lower lash on the line's lowest texel, and only where the line is the eye's lower
  edge there (elsewhere the preset has no dark line to root on: those lower lashes are left out, one per eye stays).
  `eye_makeup` now asserts it: with the preset laid on, no piece of lash may be a dark piece of its own (a failure
  writes eyes/_cache/lash_loose.png, the loose pieces red). look/royal.png + royal_2x.png rebuilt.
- **The outer corner is one arc** (user, an arrow at a notch under the outer lashes: "the far away eye lashes should extend
  its root, forming a pretty arc from the eyes"). Before: two wings from one spot, a notch between them. Now the lid's
  line is carried on as one tapering flick: it starts inside the lid's line at 0.80 of its length, as thick as the line
  there, leaves along the lid's own direction (the slope of the line's middle over its outer third), then turns up
  (`spike(via=)`); the three outermost lashes grow from the arc itself, each shorter than the last. Tried and
  dropped: an arc through the preset's lowest corner tip (a heavy filled wedge). eyes/review_face/sheet.png.
- **512 px for upload** (user: "skin reduce to 512x512 please, that's the max game can render"): look/royal_512.png = the
  2048 px skin shrunk with Lanczos (sharper than painting at 512); on the home Desktop
  `wardrobe_reupload\lady_noir_face11\12tails_ค้างคาว_Royal.png` (the hood was 512 already). look/royal_2x.png stays
  for the wardrobe's own preview.

## 2026-11-13 (home), every icon upscaled

User: "check all icons in the wardrobe app for any unupscaled ones, and upscale them"; then "you may check 12 tails
bible hub, some might be there already".

- **Found:** `wardrobe/data/icons` held 3,741 icons at the game's size: item icons 64 px (51 px for TTO's own art: 70),
  the skill and emote icons 64 px, the 60 class portraits 75 px. Already upscaled: `icons/hd/` (the Bible's 128 px skill
  icons for the ท่าสกิล rings) and `wardrobe/ui/recolor1-5.webp` (104 px = 2x the 52 px potion crop; they measure 1.3-1.4
  from the Real-ESRGAN recipe below against 5.4-6.6 from a plain Lanczos resize, so they were made with it). `ui/tto.webp`
  (61 x 64) is the Bible's 256 px TTO logo made smaller, shown at 20 px: nothing to upscale.
- **`pipeline/wardrobe_icons_upscale.py`** (new) replaces each game-size icon in place, same name, with a 2x picture
  (128 px, TTO's 51 px art to 128 too as the Bible does; the portraits 150 px): the Bible's own 128 px upscale when
  `12t_projects/bible/assets.js` has one under the same name (GEAR_ICONS `a_ / w_ / c_ / t_<code>`, SKILL_ICONS
  `<class>_<skill><rank>` and `sup_<skill>`, without case) and it measures within `BIBLE_MAX_DIFF` 10 of the game's icon
  (its WebP bytes as they are), else the project's icon recipe (the archive's
  `D:\12tails-assets-archive\tto-c6-skill-icons-2026-11-03\tools`: Real-ESRGAN x4 as plain torch modules, RGB = 0.6 x
  anime_6B + 0.4 x x4plus, alpha Lanczos, Lanczos down, WebP q90; `py -3.10` with CUDA, models in
  `D:\sd_backup\models\RealESRGAN`: the home PC only). Run: 1,651 from the Bible, 2,090 by Real-ESRGAN (four Lv 100
  skill icons of the Bible measured 10.2-10.7 and were upscaled here instead). The folder went from 12.7 MB to 26.3 MB.
  - Names only, never the nearest picture: a pixel search matched tier variants to each other (`weapon/bat11` to
    `w_bat12` at 1.9), so the Bible's icon is taken by its name and the pixels only refuse a wrong one.
  - An edge-bleed pass (colour under the transparent pixels filled from the edge before the upscale) made no visible
    difference on white or dark; the plain recipe is kept.
  - `icons/upscaled.json`: per icon the hash of the game-size picture it came from and its source (`bible:<key>` /
    `esrgan`). `wardrobe_icons.py` and `wardrobe_ui_assets.py` ask `keep()` before writing an icon, so a data rebuild
    leaves the upscales alone and writes only new or changed icons at game size; then
    `py -3.10 pipeline\wardrobe_icons_upscale.py` does just those. `--check` (Pillow only, either PC) lists icons still
    at game size, exit 1 when there are any.
- **The publish** (`wardrobe_publish.py` `Run.proven_upscale`, `ICON_MAX_DIFF` 12): an icon of the data that is bigger
  than BB's picture is published as it is once, shrunk to BB's size, it is BB's picture (the Recolor Drug pictures'
  comparison); one that fails is warned about and BB's own picture goes out at game size, as every icon did before. All
  3,508 icons with a BB file measure 0.3-9.5; the other 233 are TTO's (published from the data when released, as before).
  The published `icons.json` / `ui.json` paths are unchanged, and `upscaled.json` is not published.
- **The page** needed no change (no code reads an icon's pixel size; only two CSS comments). The video repo reads
  `icons.json` for the paths only: nothing renamed or moved.
- Checked: unit tests (`test_wardrobe_icons_upscale`, a publish test for the proof), a headless page pass at 2x device
  pixels over every topic's picker (201 icon and ui pictures, none under 128 px but the five potions and the TTO mark, no
  console errors), and a publish into a scratch folder.
- **Deployed** (user: "you may deploy"): published from the main folder at 07b2b9a (check: no problems, no upscale
  refused, the same drop counts as the live copy's), from an empty folder with the Worker script: 2,889 files uploaded,
  6,679 already there, version `9cf1cf7c-bd28-4796-ae8a-0df240c9fb17`, `data-c9333e34e6` (it replaced the office's
  `data-aec559a710`). Compared with the live copy first, every page / JSON / script file: besides the icons, the copy
  differed by the page's three CSS comments, LF for CRLF in fxparts and fx_cues, and the Panda's Wind & Cloud and Rain &
  Storm (5bb4936, committed at home and not yet deployed: meta.json, panda/clips.json, panda/fx.json, fx_cues/panda.json,
  icons/hd/index.json), which went live with it. Live: icons 128 px (portraits 150 px), `icons/hd/panda/wind&cloud.webp`
  200, every class 33 faces, /api/community answering, `upscaled.json` not there.

## 2026-11-13 (home), the Whale's build started

User: "why is Whale skills not in the wardrobe?" (only its research existed: the build was dropped that day on
"delete Whale build"), then "build the Whale". `pipeline/workflow_class_fx.js` (scriptPath) with args `{mode: "build",
cls: "whale", Cls: "Whale", released: ["clap", "leviathanCall", "wai"], regress: the eleven built classes, pc: "home"}`,
run wf_4847b2c5-182: planner (no decisions.md existed), builders, editor, QA. The script's prompts now name all
eleven built classes as models, the new unit test, and the Bat skin session's files as off limits.

## 2026-11-13 (home), the Whale's effects: built and cued

From plans/fx_whale/ (six reports, each with its "## Verification", which wins; decisions.md decided overnight for the
user's review: 67 decisions). One editor after three builders (whale, tto_whale, page_pipeline), on the home PC.
- **Parts (new):** fxparts/whale.js (`Whale_javelin`: a copy of the worn lance, api.propModel slot R, the starter
  noviceLance with nothing worn, thrown at 24 m/s under gravity on the 0.02 s step, nose along its velocity, stuck when
  its box's lowest point meets the floor, gone at 3 s, no hit drawn; `Whale_flyingShield`: a copy of the worn shield on
  the clip-driven node, its 1 m sphere tested against the target body each frame; `Whale_homingShield`: the copy at
  Euler(0, 0, 90) spun 1200 deg/s, 12 m/s, RotateTowards 4 rad/s with the heading's y x 0.2, a flyingShield_hit on every
  entry of its 0.5 m sphere, gone at 3 s; `whale_kingdomKnight`: options `slot`, `end`, `standing`, `guard`, `attack`,
  the rise y = -e^(-4 t), its kingdomKnight_ring2 spawned at the slot, the unsummon clip and gone 1 s later;
  `fx:grandTide`: root looped at age 1.0, fx.cutNow() at the cue's `release`); one target body for all of them, the Bat's
  capsule. fxparts/bat.js, fx:castRing only: the Whale let through its class gate, a cue's `animLoop` played looped from
  the first update with the 0.5 s restart skipped. fxparts/tto_whale.js (TTO's `WhaleDolphin`: the lane from the cue's
  spot to `to` in `hops` hops, the 1.4 m sink and the arc, tail and fins, a fresh splash copy at every landing and a
  fresh trail copy per hop; `WhaleLeviathan`: the keyed rise, breach and dive on a Catmull-Rom path, tail flex, fade,
  the geyser / trail / crash / pool children switched on at their times with fresh clocks). index.html (page_pipeline):
  SEQ.whale (15 lines), SEQ_SKILL.whale (9 ids), LOWER_RANK.whale malStorm, PROP_STARTER.whale, FX_PART_FILES += whale,
  tto_whale, cue options `around: [lo, hi]` (a whole-metre radius at a whole angle, cueOf), a rot element `[lo, hi]`
  (rotOf), `withRot` beside `atBone` (the bone's rotation too, once), `fx.clipFloor(node)` for the parts (clips in place
  what is already the mesh's own material, copies a shared one). wardrobe_fx.py: LAYOUTS whale_kingdomKnight
  (`kingdomKnight_ring2`) and the four field-less Whale scripts, SHURIKEN_FROM_TTO whale grandTide (matched by material,
  no SHURIKEN_MAT). wardrobe_fx_tto.py: SKILL_FX whale (5). No NEVER_PLAYED / LIFTS for the Whale. Nothing the video repo
  reads was renamed.
- **Editor fix, shared data (found by `git status` after the build): textures of one name replaced one another.** Every
  class's effect textures land in data/fx/tex under the texture's own name, and BB has different pictures under one
  name in different classes' files. The Whale's build wrote its nAttack_hit1 / nAttack_hit2 over the Cat's (other
  pictures, mean difference 93 / 29 of 255). An audit of all 471 textures of the twelve classes' cued BB effects
  (checks/fx_whale_build/editor/tex_audit.py, git-ignored) found two older cases, both live since those classes'
  builds: **the Sheep's castRing texture (the pink ring, 128 px) had been replaced by the Penguin's (the blue ring,
  256 px)**, so the Sheep's cast ring, Revert and Revive drew the Penguin's ring; **the Bat's shadowRay (the zigzag ray
  of Phantom Bane, its hit and Soul Eater's hit) differs only in case from the shared ShadowRay (the smoke)**: one file
  on Windows, so the smoke was drawn (and on a case-sensitive host only one of the two names has a file: not looked at
  on the live site). Now wardrobe_fx.py's `TEX_FILES` gives those four
  texture objects (by assets file + pathID) a file name of their own (whale_nAttack_hit1 / 2, sheep_castRing,
  bat_shadowRay; the material's "tex" and an emblem's imageTex follow, `tex_name`), and `save_texture` (both builders
  use it) refuses to replace a file that holds another picture or differs only in case: the build stops and names the
  clash; a file that already holds the same picture is left byte for byte; `--retex` writes over it where the game's
  own picture changed. Data: the Cat's two files restored from git; `wardrobe_fx.py sheep --fx castRing` and
  `wardrobe_fx.py bat --fx phantomBane` (each changes one material's "tex" in that class's fx.json and adds one texture
  file; effects, order and every other material identical to the committed data). Tests: pipeline/
  test_wardrobe_fx_textures.py (8, new). TTO's textures audited too (tex_audit_tto.py: 323 checked, no clash between
  classes; at home the Monkey's tto_RuneGolem is another size and three Monkey textures are missing from the
  2026-11-04 bundles: its TTO data is the office's 2026-11-09 build, so a Monkey TTO rebuild belongs to the office, or
  needs `--retex` here). Not audited: the weapons' own effects (wardrobe_weapon_fx.py writes a texture only when no
  file of that name exists; it reads its names through the same `tex_name` at its next run). **For the user's eye:**
  the Sheep's cast ring is pink again and the Bat's Phantom Bane ray is the zigzag.
- **Cues** (wardrobe/fx_cues/whale.json, 41 keys, 267 cues: 168 fx, 53 sound, 43 voice, 3 hideProp; 54 effect names, 5
  of them TTO; assembled from the reports' blocks by checks/fx_whale_build/editor/assemble.py, git-ignored):
  attacks_emotes' block with its Verification's `@KnightoftheDeep:cAttack1` (the six standing knights, `guard`) and
  `:cAttack2` (the ring + TTO's roundTable1|roundTable2 sound), `@ShieldReflect:cAttack2` and
  `@WallPuncture:peninsulaImpale`; effect_only's `@AutoShield:root`; skills_a's block (cast1, the cast3 pool of eight,
  `@Honor:cast3`, `@BubbleBurst:cast3`, divingWave, divingStorm, gobble, bowlingWhale1) with its Verification's
  `@12thKingdomKnight:cast3` and flyingShield pool; skills_b's block (sweep, javelin, shieldRush, swallow,
  peninsulaImpale, peninsulaRound) with its Verification's grandTide1 and no grandTide2; tto section 7's
  `@LeviathanBreach:cast1`, the empty `:cast2`, leviathanCall. Applied on top: decision 28 (`replace` on the bubble),
  38 (`replace` on the slot-0 knight), 32 (every `boneAt` written `atBone` + `withRot`); each of the three whys says so.
- **Tiles / icons:** wardrobe_skill_icons.py CLIP_SKILLS whale (divingWave -> whaleWave, divingStorm -> malStorm, gobble
  -> gobbleUp, leviathanCall -> leviathanBreach), OWN_TILE whale (honor, 12thKingdomKnight, bubbleBurst on cast3;
  knightOfTheDeep and shieldReflect on the charge's clips; wallPuncture on peninsulaImpale), EFFECT_ONLY whale
  autoShield, RANK_ICONS whale 12thKingdomKnight (its Bible key starts with a digit); rerun: whale 32 HD icons for 43
  clips (19 new webp: 12thKingdomKnight, autoShield, bubbleBurst, bubbleShield, callToArm, gobbleUp, heavyWeight,
  homingShield, honor, hydroBlast, knightOfTheDeep, leviathanBreach, megalodon, rejuvenate, revitalize, salvation,
  shieldReflect, wallPuncture, whaleWave); index.json whale only, no other class changed.
- **Check / inventory:** wardrobe_fx_check.py OPTS += guard, attack, around, withRot, animLoop, hops; a cue's rot is now
  checked (`rot_ok`: three angles, each a number, "random" or a [lo, hi] pair of whole numbers, or the words), around is
  [lo, hi] whole metres, withRot only beside atBone (every class's cues pass). wardrobe_fx_inventory.py BUILT += the
  five Whale scripts and TTO's WhaleDolphin / WhaleLeviathan, NOTES whale grandTide (grafted: drawn), CLASS_NOTES whale
  (the status looks CharacterControl loads, kingdomKnight_ring2, overPresence, the unused divingStorm prefab, the
  missing javelin_hit / bowlingWhale_hit); rerun: the Whale 50 / 51 ready (the 1 left: grandTide's grafted
  ParticleSystems, drawn), 688 / 699 over all classes.
- **Data:** `wardrobe_fx_tto.py whale`: 5 TTO effects, 19 materials, 16 textures, 0 sounds (no warning);
  `wardrobe_fx.py whale`: 49 effects, 45 materials, 46 textures, 115 sounds (the two grandTide graft lines printed:
  Water2, Splash3; heavy's `reduce` found in the Rabbit's sounds by the rip walk). data/whale/fx.json 54 effects
  (2.5 MB), sfx/ 115 files (75 voices, 40 sounds), 35 new textures in data/fx/tex for the Whale (15 tto_) + the two
  fixes' sheep_castRing and bat_shadowRay: all new files, to commit with the run; the office PC pulls.
- **Gotcha (this PC's Git Bash):** `grep -c $'\r$' <file>` prints 0 for a CRLF file (grep reads it as text and drops
  the CR): the page's LF check needs `grep -c -U $'\r$' wardrobe/index.html` or `py -3 -c "print(open('wardrobe/
  index.html','rb').read().count(b'\r\n'))"` (both 0 now). The pipeline's .py files are CRLF in this working tree (git's
  autocrlf; LF in the index): an edit by script must keep that.
- **Judgement calls (mine):** the texture fix above reaches the Sheep's and the Bat's committed data (two materials'
  texture names: a correction, not a rebuild); the check validates rot / around / withRot (decision 66 asked only for
  the words); the three decisions applied on top of the blocks were written into the whys; TEX_FILES names by class
  prefix (`<cls>_<name>`). The builders' calls kept: the Homing Shield's 2e-6 m nudge to a random side (without it the
  shield locks onto its aim's line, passes once and flies off: one hit, not decision 26's hit per pass), the knights'
  guard never rewinding cAttack, the Leviathan's fade by the material's saved tint / colour, a fresh trail copy per
  hop, fx.clipFloor clipping own materials in place.
- **Gate:** files-only (every class with cues) "no problems"; `wardrobe_fx_check.py D:/12tails-wardrobe checks/fx_whale dark
  --cls whale` exit 0, errors [], 43 tile plays, every expected effect spawned, 82 sounds loaded (run again on the
  final code: the same). The page and shared parts changed (index.html's cue options, withRot, fx.clipFloor; bat.js;
  the check; the two builders' texture names), so also the regression over the eleven other classes
  (checks/fx_whale_regress). **In one run the headless page crashed** ("Page crashed") at its 326th tile play, the
  Mole's War Capital, eight classes into one page, at 23:38, with nothing wrong logged before it (not explained: the
  page's memory after eight classes, or the PC's load then, the user finding it "really laggy" and the lead's
  pipeline/throttle_headless.ps1 coming in at 23:50; the same tile passes in a fresh page, and the office ran ten
  classes in one page for the Rabbit). In two runs: `--cls
  wolf,sheep,penguin,bat,bison,cat,chameleon` exit 0, errors [], 300 tile plays; `--cls mole,monkey,panda,rabbit`
  exit 0, errors [], 205 tile plays. Unit tests 73 OK (81 with the new test_wardrobe_fx_textures), node 9 pass,
  test_adopt_from_video.ps1 fails 0; `wardrobe_weapon_fx_check.py checks/fx_whale_build/editor/weapon_fx_check.png`
  OK; a trial `wardrobe_publish.py --out` into a scratch folder (removed after): "check: no problems", the Whale's
  fx.json, 115 sounds, 32 HD icons and the renamed textures in it (its one warning, whale/talk's TTO keys, is about
  the clip, not the effects). index.html LF (0 CR, counted in bytes). The gates ended after midnight (the 14th).
  Not committed.
- **Left out:** decisions 22, 39, 56-58 (hits out of reach, the knights' volley, camera effects, looks that need a foe
  or an attacker, the unreleased TTO passives' looks, the Reborn-only and supplement skills, the unused divingStorm
  prefab and orphan voices, the missing javelin_hit / bowlingWhale_hit). Nothing else: every skill decided is cued.
  Built, not cued: the knights' `attack` option, kingdomKnight1 (rank 1's look: its layout reads, no cue names it),
  overPresence.
- **For the QA pass:** the gate's wall-clock samples and my own probe (checks/fx_whale_build/editor/probe.py, every
  frame recorded in the page) agree with the cues on what spawns, where and for how long: the knights at slots
  (+-1.6, +-1.6), (+-2.2, 0) rising from 1 m under the floor, their rings 1 s, unsummon at 10 s, gone at 11 s; Knight of
  the Deep's six from 0 to 3.8 s with the ring 0.7-4.0 s; the bubble 10 s at y 1.3; heavy, spiralBlast, megalodon_ring
  (7 s) and megalodon (at 4.0 s of cast3) at the 10 m point; the javelin from (1.2 right, 2.2, 1) to rest at (0.33
  left, 0.44, 12.44), 3 s; the Homing Shield's hits at (0, 0.87, 9.4) and (+-0.7, 0.71, 10.29), gone at 3.0 s; the
  Flying Shield spawning no hit; grandTide alive 1.0-6.0 s of the tile; bowlingWhale 0.5-7.95 s; Leviathan Breach's
  warn 0-4.25 s, raise cut at 0.75 s, slam 0.75 m left / 0.9 m ahead, 24 dolphin effects (3 dolphins + 12 splashes + 9
  trails), the Leviathan 8 s from 1.95 s of leviathanCall. A few sanity shots on the virtual clock
  (checks/fx_whale_build/editor/shots/sheet1-4.png) read right; nothing else has been looked at. To look at: the lance
  copy's orientation in flight and stuck (its tip under the floor clipped), the shield copies' orientation and spin,
  the knights' look, rise and guard turns (their floor clip while rising), the 28 asunderRound rings following the
  lance hand's pose (`withRot`), Mal Storm's bolts 12-22 m up (above most frames), grandTide's grafted spray and a pale
  square sheet under her at 1.5 s of the tile (the wave's create clip or the grafted Water2 box: unjudged), honor_cast
  (an emblem, a GUI picture: no mesh, it shows 2 m up over her face from the near camera), the bubble's size, the
  dolphins' hops, splashes and trails, the Leviathan's rise, breach, roll and dive at the 10 m point (pivot to 9.6 m:
  far outside the default frame), its fade and floor clip, the cast ring's `animLoop` in its 0.1 s. In the headless
  real-time runs the first frame after a pick can stall 0.3-0.6 s with dt unclamped, so a t = 0 cue's effect starts
  that late while the step clock runs on (the Normal Attack's stage-2 wave came 0.2 s after stage 1's in one probe
  run): the known headless stall, to be judged on the virtual clock only. Rolled procs the gate does not expect: KO's
  deadEffect (p 0.5), Peninsula Impale's wallPuncture_hit / nAttack_hit pairs (p 0.4 a stab).
- **For the Bible (offer, not written):** decisions.md's last section; from the builders: the Homing Shield hits a 10 m
  target twice (0.70 s and about 2.5 s after its spawn) and which side it returns on is chance; the knights' guard never
  restarts cAttack; the javelin slides about 0.5 m after sticking; the Flying Shield's nearest pass is 1.64 m from the
  body's side; the Leviathan's pivot overshoots to 9.6 m (the Catmull-Rom over key 3's 9 m); the fins' signs; the
  dolphin's clamped heading samples; the fade reaching the trail's renderers.
- **QA pass (2026-11-14, home).** Shot with `wardrobe_fx_shots.py --jobs` (virtual clock; jobs
  checks/fx_whale_qa/jobs.json, 51 jobs, every Whale tile: Normal Attack, Charge Attack, Shield Bash, Knight of the
  Deep, Shield Reflect, Auto Shield, the eight cast pool members, Honor, 12th Kingdom Knight to 12 s, Bubble Burst,
  Whale Wave, Mal Storm, Flying Shield and Homing Shield (nothing worn: the starter shield; and with timeShield +
  poseidonSpear worn), Gobble Up, Bowling Whale to 8.2 s, Sweep, Javelin (nothing worn: the starter lance; with
  poseidonSpear; with starMicrophone), Shield Rush, Swallow, Peninsula Impale, Wall Puncture, Peninsula Round, Grand
  Tide to 6.5 s, Leviathan Breach to 10.6 s (side, behind, far, and near for the cast ring), the eight emotes with
  voices, clap, wai, run, KO (dead forced, and as rolled), getUp) on the dark and the white stage: 883 shots each.
  Sheets: checks/fx_whale_qa/sheets_dark, sheets_white (git-ignored; shots and logs under run/). No page error, no
  stalled render loop, no failed job (the only console line: swiftshader's glBlitFramebuffer feedback warning). Four
  camera views added to the shot and sheet scripts: `tall` (the floor to 23 m up, from far in front: Mal Storm's
  bolts), `wide` (from 50 m on her left: the Leviathan whole), `ground` / `groundfar` (level with the floor at her
  spot / at the 10 m target: whatever draws under the picture's middle line is under the floor).
  Boxes in the hero's frame (+x = her left) match the reports and decisions: extendedWave1-3 4 m ahead from 0 / 0.8 /
  1.8 s; shieldBash_ring at 3.2 s; the six standing knights at (+-1.6, +-1.6), (+-2.2, 0) turning every 0.5 s, back to
  her facing by 3.5 s, gone at 3.8 s, roundTable_ring 0.7-3.0 s; shieldReflect at 0.7 s 0.7 m ahead, shield 1 m ahead;
  castRing 0.1-0.55 s; the bubble 0.9-10.9 s; heavy, spiralBlast, megalodon_ring (to 7.6 s) and megalodon (4.6-7.6 s)
  at the 10 m point; rejuvenate_hit at 2.9 / 6.9 s (Revitalize 3.1 / 7.1 s); callToArm_ring at her and 8 m behind;
  honor_cast 0.4-0.9 s; the knights rising from 1 m under the floor with their rings from 0.5 s, the unsummon at
  10.5 s, gone at 11.5 s; malStorm 0.7 s and 24 bolts falling from 12-22 m up at 35 m/s; the Flying Shield's loop out
  on her left to 11.9 m ahead and back on her right, lying flat, the worn shield hidden 0.5-1.5 s, no hit; the Homing
  Shield through the target at 1.22 s and again at 3.03 s, gone at 3.5 s, the worn shield hidden to 3.5 s; the lance
  copy from (1.2 right, 2.2, 1), tip first, stuck at 11.6-14.1 m ahead from 0.5 s after the throw, gone 3 s after it,
  the worn lance hidden 0.5-1.0 s; bowlingWhale 0.5-7.95 s; Peninsula Impale's spikes every 0.3 s and one hit each at
  (0, 1, 10); the 28 asunderRound rings round the lance hand; grandTide 1.0-6.0 s with the hero riding it; Leviathan
  Breach: the cast ring 0-0.1 s, the warn at the target to 4.25 s, the raise cut at 0.85 s, the slam at 0.7 s, the
  three dolphins' hops with a splash at each landing, the Leviathan from 2.05 s (geyser 2.55 s, breach, roll, dive,
  crash 4.25 s, body gone 5.35 s, pool to 9.25 s, all gone at 10.05 s); KO's deadEffect.
  - **Bug found and fixed: parts under the floor were drawn** (decision 45's rule, "what is under the floor is
    hidden", was applied to the knights, the javelin, the dolphins' and the Leviathan's bodies only). Seen from the
    floor-level views (checks/fx_whale_qa/sheets_ground before, sheets_fix after):
    - **Mal Storm's bolts** fell on through the floor to 5.5 m under it (the prefab's root EffectControl velocity
      (0, -35, 0) over its 0.5 s life; the page clips a moving CHILD by itself, not a moving root). Fixed in
      wardrobe/fx_cues/whale.json: `"floor": true` on the 24 bolt cues (the Panda's option).
    - **Megalodon's shark** showed its body from 9 m under the floor while rising and sinking. Fixed: `"floor":
      ["Megalodon"]` on its cue.
    - **Grand Tide's wave** (five meshes hung 4.8 m under the prefab's root, boxes to 11 m under the floor) drew its
      whole underside, and **grandTide_ring's 24 water sheets** (its ImageEmitter, 3 m tall, centred on the floor)
      drew their buried halves: the editor's "pale square sheet under her at 1.5 s". Fixed: `"floor": true` on
      grandTide, `"floor": ["ImageEmitter"]` on grandTide_ring.
    - **Leviathan Breach's drops** (TTO's ParticleSystems, no Collision module) fell through the floor: the crash's
      `rain` (up at 10-20 m/s under 2.2 g for 1.4-2.2 s) made a blue column to 30 m under the pool, the slam's, the
      geyser's and the dolphin splashes' drops the same on a smaller scale. Fixed: `"floor": ["splash"]` on the slam's
      cue; in wardrobe/fxparts/tto_whale.js `clipDrops` clips every ParticleSystem node of the Leviathan and of a
      dolphin's splash copy at the floor (the ground discs and bands stay whole).
    - For these, **the cue option `floor` now also takes a node's name or a list of names** (wardrobe/index.html, class
      Fx: only those nodes of the effect and what hangs under them; `true` is the whole effect, as before), because a
      flat ring lying exactly on the floor must not be cut along it. pipeline/wardrobe_fx_check.py checks that each
      name is a node of the cued effect.
  - Looked into, not bugs: the knights' lance trails draw long straight zigzags during the guard (each 0.5 s turn
    moves the lance tip at once and the TrailRenderer joins the two places, as Unity's does); honor_cast shows over
    her face (the code puts it 2 m over her feet and she is 2.4 m tall); the Flying Shield draws no hit (decision
    25); megalodon_ring is faint on the white stage (additive on white); megalodon's and the bolts' boxes read under
    the floor in the logs (the box is the geometry's, not the clipped picture); the cast ring cut at 0.55 s with no
    shrink shown between samples; a step can start one frame late on the virtual clock (Normal Attack's stage 2 at
    0.83 s for its 0.8, Leviathan Breach's call at 0.12 s for its 0.1: float sums of the 1/30 s frames); with a weapon worn its own effect (poseidonSpear's purple trail,
    starMicrophone's ribbon) keeps drawing on the hand while the thrown piece is hidden (decision 54: meshes only).
    Left as they are, as for the other classes: rings and bursts centred on her body that dip under the floor by
    less than 2 m (Peninsula Round's rings, rejuvenate_hit, the bubble's underside, flyingShield_hit) and a
    camera-facing flash on the floor (the Leviathan's crash).
  - Gates (on the final code): `wardrobe_fx_check.py D:/12tails-wardrobe checks/fx_whale_qa/gate dark --cls whale` exit 0, errors [] (43 tile
    plays, 82 sounds loaded); files-only over the twelve classes "no problems"; the page's Fx code changed (the `floor`
    option), so also the regression, in two runs as the editor's (one page for all eleven crashed for the editor; not
    tried again): `--cls wolf,sheep,penguin,bat,bison,cat,chameleon` exit 0, errors [] (300 tile plays), `--cls
    mole,monkey,panda,rabbit` exit 0, errors [] (205 tile plays); unit tests 81 OK (the six modules, the new
    test_wardrobe_fx_textures among them), node 9 pass, test_adopt_from_video.ps1 fails 0; `wardrobe_weapon_fx_check.py
    checks/fx_whale_qa/weapon_fx_check.png` OK (it needs `--with pillow` beside playwright); a trial
    `wardrobe_publish.py --out` into a scratch folder (removed after): "check: no problems". index.html LF (0 CR,
    counted in bytes). Not committed.
  - For the user's eye: Megalodon, Mal Storm, Grand Tide and Leviathan Breach now end at the floor (compare
    checks/fx_whale_qa/sheets_ground with sheets_fix); the knights' zigzag lance trails while guarding; Honor's
    emblem over her face; Peninsula Round's rings pass under the floor (not clipped); the target-point effects (Heavy
    Weight, Hydro Blast, Megalodon, the Leviathan) sit outside the default camera's frame, as for the other classes;
    Mal Storm's bolts start 12-22 m up; decisions.md's overnight calls and the editor's judgement calls above (the
    Sheep's cast ring pink again, the Bat's Phantom Bane ray).
- **The lead's pass (2026-11-14, home):** the editor's and the QA's reports read; 81 unit tests, the Worker's 9,
  `wardrobe_icons_upscale.py --check` 0; index.html, whale.js, tto_whale.js, bat.js and whale.json 0 CR by byte count;
  two QA sheets looked at (Leviathan Breach wide after the floor fix, 12th Kingdom Knight). CLAUDE.md's test line and
  the workflow script's now carry `pipeline.test_wardrobe_fx_textures`; the script's weapon check line has
  `--with pillow`. With the Whale the effects run is complete (twelve classes): `plans/goal_fx_all_classes.md` is
  deleted and HANDOFF's "Next up" is narrowed to what is left for the user's eye.
- **`pipeline/throttle_headless.ps1`** (user during the build: "reduce PC power consumption to 30%, everything is really
  laggy"): one chrome-headless-shell (the regression gate: SwiftShader draws on the CPU, at AboveNormal priority) held
  69% of the 20 logical cores; put on the last 6 cores at Idle priority it measured 17%. A workflow's agents cannot be
  messaged mid-run, so it is done from outside: the script repeats it every 3 s for every such process (`-Percent`,
  `-Hours`, `-Once`). The checks run slower under it. The editor's one-page regression crash (23:38) came before it
  (23:50), so it is not the cause.
- **The send dialog: looked into, left as it is** (user: "no one has been able to send me skins because no cloudfare
  pop-up to verify", then "the cloudfare tick didn't appear cuz by PC is too slow that's all, no need for fix"). On the
  live site Turnstile loads and draws its box at 1366x768, 1280x600, 390x844 and 360x640 (headless, and a separate real
  Chrome). Seen and not changed, for a later day if wanted: (1) when Cloudflare wants a click the box shows a checkbox
  while SEND_ERR.wait says to wait for the tick; (2) at about 600 px of height the box starts below the dialog's fold
  (the form is 676 px in 566); (3) the widget's error-callback says nothing. Cloudflare's test key that always asks
  for a click is `3x00000000000000000000FF` (`?submitkey=`). `pipeline/wardrobe_send_live_probe.py` still drives the
  old piece-menu send (the toolbar's #sendlook replaced it).
- **Deployed** (user: "when done please commit push and deploy, then shut down this PC"): published from the main
  folder at b4e05b3 (check: no problems; 9,569 -> 9,743 files, +4.5 MB; one warning, whale/talk's TTO keys differ from
  BB's, BB's published), deployed from an empty folder with the Worker script: version
  `cef73b79-837a-4547-be5d-586607703aa0`, `data-627300df13`. Live: 200, whale/fx.json, fxparts/whale.js and
  tto_whale.js, fx_cues/whale.json, fx/tex/sheep_castRing.webp, /api/community answering, the old data folder 404, no
  tot/. A headless pass on the live page: the Whale's 32 skill tiles; Leviathan Breach, 12th Kingdom Knight and Javelin
  spawn their effects; no page or console errors. The PC was shut down after it, with the Bat skin session's work
  still uncommitted on its disk (HANDOFF "Home PC: the Bat skin session's work is not committed").

## 2026-11-14 (home), one weapon topic

User: "having 2 weapons slot is confusing to the users, merge the 2 slots to one which applies both main and sub weapon",
then "when you are done, commit push deploy this work".
- **The panel:** อาวุธหลัก + อาวุธที่ 2 are one topic, **อาวุธ** (TOPICS "R"). Row 4 = อาวุธ + ประดับ; ท่าทาง spans row 5,
  its ring capped at a half block's size (desktop and short screens; on a phone a topic is ring + name in a row anyway).
- **A pick wears the game's whole weapon** (index.html `weaponOf` / `setWeapon`, above buildSets):
  - a two-piece code (item_map.json: Chameleon bow + arrow, Whale lance + shield): the first piece in R, the second in L
    (the Whale's hands: SWAP_HANDS, unchanged);
  - `<name>_L` / `_R` pieces each in its own hand (Panda's gloves, the Wolf's hallowSaw / specialSword);
  - the Wolf's other swords in both hands: WolfEquipment.getWeapon(code, 1 / 2) loads the same prefab for hand 1
    (mount_Hand_L) and hand 2 (mount_Hand_R), except w_wlf35 / w_wlf59's `_l` / `_r` (DecompiledSource/WolfEquipment.cs
    :594, :805, :940-1010);
  - everything else in R only. PandaEquipment.getWeapon("w_pnd5", isLeft: true) loads nothing (:442): holyThread is
    one-handed, so the sets no longer put it in both hands (`dualSame` did that for any class with a "#2" placement and
    no code pairs: the Panda as well as the Wolf; it is `BOTH_HANDS` = the Wolf now);
  - ToT's student pieces (no code) pair by the coded pairs' word endings: studentBow + studentArrow, studentLance +
    studentShield (the student sets get the arrow / shield too now; local only).
- **Internals unchanged:** C.state.R / L and C.props.R / L, the sets, looks (LOOK_SLOTS), skins, the effects (propModel /
  propCopy "L"), `wardrobe.show`, the community import's slot names, so the video repo and every check script still
  work. The picker lists one tile per weapon (its R piece; the search also finds it by the other piece's name); the
  pressed tile and the ring = `wornIn("R")` (R, else the weapon of what L holds: an old saved or shared look with a free
  left-hand piece still shows something).
- **Every other way a piece goes on wears its whole weapon** (`wearPiece`): the piece menu's ใส่ชิ้นนี้ and ถอดอาวุธออก
  (both hands off), the viewer's ใส่, a skin upload or a community skin on a piece not worn, a dropped file
  (`equipPieces`: a list naming one hand only; a look naming both hands keeps each piece as listed). A weapon piece's
  menu has **อีกชิ้นของอาวุธนี้: <name>** (the other piece's own menu, at the same place): the arrow / shield / left glove
  has no tile of its own any more, so its PNG / GLB download and skin upload are reached from the weapon tile's
  right-click too; a click on it on the model works as before (slot L; SLOT_TH.L = อาวุธ; เปลี่ยนอาวุธ opens the one topic).
- **Check:** `pipeline/wardrobe_weapon_slot_check.py` (headless; every class's tiles and hands against item_map.json
  worked out apart from the page, a pick / ไม่ใส่ / one undo per class, the Chameleon's arrow menu and its other-piece
  link, the panel and its three rings one size at 1920x1200, 1366x768 and 390x844): 97 ok, exit 0. Unit tests 81 OK, node
  9 pass, test_adopt_from_video.ps1 fails 0; `wardrobe_menu_check.py` and `wardrobe_sets_check.py` exit 0 (foreign
  weapons 0); `wardrobe_weapon_fx_check.py` OK (a first run on a cold disk cache
  timed out; HEAD's page also took 58 s to load cold, and warm both show flamingBrand's effect within 2 s). Playwright pinned `==1.65.1` (chromium 1254; the newest wants a browser not installed).
- **Committed alone:** the Bat / Cat skin sessions' uncommitted files stay out, its SKINS.cut / SKINS.face hunk in
  index.html too (the commit's page = HEAD's + this change, built with `git merge-file`; HEAD's + both = the working
  file). The publish takes the page from `git archive` of the commit and the data from the main folder (`--src` /
  `--data`), so the deploy carries no uncommitted work either.
