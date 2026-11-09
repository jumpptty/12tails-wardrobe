# 12 Tails Wardrobe: notes

Read this first and append to it during the session, not at the end: findings, conventions, lessons, the session
log.

Split from `jumpptty/12tails-video` on 2026-11-09 (the user: "make a separate repo for the wardrobe, independent of
the video works, so there's a clear line between them"). The sections below moved from that repo's NOTES.md, their
text unchanged except paths. Older mixed history (the TTO extraction of faces / outfits / animations / props, lessons
shared with the skits, the office PC setup) stays in `D:\12tails-video\NOTES.md`: read it when needed, never edit it
from here. The split's design and plan: `plans\wardrobe_split_design.md`, `plans\wardrobe_split_plan.md`.

## Layout

- `wardrobe\index.html` (the page, three.js r160), its icons and `wardrobe\ui\`; `wardrobe\data\` (untracked,
  ~300 MB) built by `pipeline\wardrobe_*.py`, prop textures in `wardrobe\data\props\tex\` (`wardrobe_props_tex.py`).
- Read only, from the sibling `12tails-video` folder: `outfits\`, `tex\faces_tto\`, `props\json\`, `props\tex\`,
  `tto_assets\`, `tot_assets\`; from the Bible repo (`D:\12tails`, office `C:\Users\Jump\Desktop\12tails`): the BB
  rip and the decompiles.
- `wardrobe_dist\` (untracked) = the published copy (`pipeline\wardrobe_publish.py`). The video repo's trailer films
  it and its skits read `wardrobe\data` (placements, the office's prop / face fallbacks): renaming either breaks them.
- `tto_config\` (untracked): `wardrobe_placements.py`'s copies of TTO's placement tables.
- `wardrobe\fx_cues\<cls>.json` (tracked): each class's skill effect / sound cues (`plans\fx_recipe.md`); the built
  effects are in `wardrobe\data\<cls>\fx.json`, `sfx\`, `data\fx\tex\`.

## Wardrobe app (2026-11-04)

`wardrobe.cmd` (this repo's root) serves the folder on http://127.0.0.1:8771 (Python http.server) and opens
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
