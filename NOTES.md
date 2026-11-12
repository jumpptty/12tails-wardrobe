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
    Eclipse, Focus Fire, Venom Phantom, Barrel Railgun, Tempest Dance) are by name; a sequence shows only when all its clips
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
- Progress (updated as it goes): Penguin DONE + deployed; Bat DONE (32 cue keys, 55 effects, 118 sounds; gates bat / wolf / sheep / penguin pass), committed + deployed below; Bison research DONE, its build next; Cat research running. (A deploy needs a NEW empty folder each time: wrangler leaves .wrangler/ behind.)
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
