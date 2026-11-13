# Whale effects + sounds research: the TTO Lv 100 skill (Leviathan Breach)

Scope: the TTO skill clip `leviathanCall` (2.4 s, `tto: true`, group `skill` in `wardrobe/data/whale/clips.json`), the
clip of Leviathan Breach (cell 454). No BB code plays it. **It is in the released list** (`wardrobe/tto_released.json:314-332`,
whale clips: clap, leviathanCall, wai), so it gets cues. `clap` and `wai` are emotes (the attacks_emotes report's); the
Whale's other TTO clips (cooking, fishingWhale, mining, planting, pose37) are emotes too and not released. Research only
(office PC, 13/11/2026): this file is the only repo file written; probes and outputs are in
`checks/fx_whale_research/tto/` (git-ignored). Sources:
- TTO's pseudo-C `C:\Users\Jump\Desktop\12tails\DecompiledSource_TTO_2026-11-02\pseudo\Whale.c`, cited `TTO1102:Method@RVA`
  plus `:<line>` (= Whale.c) ; `fn.py` (the Panda's noise-dropping printer) -> `dorow6.txt`, `cast_movenext.txt`,
  `breach_movenext.txt`, `damage_movenext.txt`, `helpers1.txt`, `helpers2.txt`, `row6.txt`, `until_cctor.txt`, `strike.txt`;
- **a Ghidra run** for the types `pseudo/` leaves out (BUILD.md :51: `tools\run_ghidra.bat targets.tsv out.c`, read-only on
  the 11-02 project, then `tools\annotate.py` run with `-B` into this folder; nothing written in the Bible's tree, `git
  status` there unchanged): `WhaleDolphin` (11 methods), `WhaleLeviathan` (11), `Whale.<DolphinLeap>d__308::MoveNext`
  -> `annot\WhaleDolphin.c`, `annot\WhaleLeviathan.c`, `annot\Whale.c` (filtered: `dolphin.txt`, `leviathan.txt`);
- capstone over `client\GameAssembly.dll` (`dis.py`) for the floats Ghidra drops: `breach_movenext.asm` (the two Untils),
  `dol_pose.asm`, `dol_point.asm`, `lev_pose.asm`, `lev_flex.asm`, `lev_fade.asm`;
- the Bible: `12t_reference\whale-skill-reference.md` "Leviathan Breach" (:773-812) and the card `whale_leviathanBreach`
  (icon `whale_leviathanBreach5`, `12t_projects\bible\index.html:19630`);
- TTO's bundles on this PC (`tto_assets/2026-11-09`, found by `wardrobe_fx_tto.py` itself): `wardrobe_fx_tto.py whale
  --probe leviathanBreach_warn,leviathanCall_raise,leviathanCall_slam,leviathanBreach_dolphin,leviathanBreach` ->
  `probe.json` (`compact.py` -> `compact.txt`); `catalog.py` -> `catalog.txt` (every catalog address under
  `heroes/whale/` against BB's rip); BB's `castRing` through `wardrobe_fx.py whale --probe castRing` -> `probe_bb.json`;
- `paths.py` -> `paths.txt` (the hop count, the lanes, the dives and the Leviathan's keys at the 10 m target, asserted);
- `cues.py` -> `cues_paste.json`: section 7's block, built from the numbers above, parsed and name-checked.

Times are seconds from the start of the sequence step the cue is keyed by. The Whale's TTO waits are `Whale::Until(t)`
(`@0x1EC24D0`, `:35821`: an absolute time, `start + x`, `start` = `Time.time` at the coroutine's first state). Leviathan
Breach has one rank (`whl_leviathanBreach5`); passives on: Reduced Cast (#373) halves its cast bar (it ends at magAdjust's
0.1 s floor either way); Sovereign Impaler / Oceans Resilience change only numbers here (section 3).

## Read this first

1. **Two coroutines, three clips: the SEQ line to add is**
   `"Leviathan Breach: cast1@0.1 cast2*^@0 leviathanCall^"` (shared change S1).
   - `RPC_leviathanCast` plays BB's `cast1` (0.2 fade) for the cast bar, `cast2` (0.1 fade, looped) at min(0.6, bar), and
     at the bar's end the owner starts `RPC_leviathanBreach` in the same frame (2.1). The bar is 1.5 s, x 0.5 with
     Reduced Cast, then magAdjust: **0.1 s** at high INT (Mole decision 6, Monkey decision 5), so `cast2` shows for one
     frame (`@0`, as the Whale's own Cast line's `cast2*@0`).
   - `RPC_leviathanBreach` plays `leviathanCall` through `Row6Begin` = `PlayAnimation(clip, 0.1)` (`^`) and ends the action
     at **0.75** (`Row6End`, `CallLength` = `DolphinAt[2]`); the clip is 2.4 s. The page plays the clip to its end
     (Chameleon decision 11) and the later cues (to 4.15 s, the effects living to 9.95 s) run in the idle tail (question 1).
2. **Cue keys.** `@LeviathanBreach:cast1` (the ring, the warning circle, a sound: the TTO cast has **no voice**, so the
   plain `cast1` entry's BB voice must not play), an empty `@LeviathanBreach:cast2` (keeps the plain `cast2` cues off),
   and the plain `leviathanCall` (no other tile plays it). Plus `SEQ_SKILL.whale = {"@LeviathanBreach": "leviathanBreach"}`
   and `CLIP_SKILLS.whale = {"leviathanCall": ["leviathanBreach"]}` for the tile's icon (S2, S3).
3. **The page's target gives 3 hops.** `LeviathanHops` = 2 + (|flat(spot - whale - 2.5 dir)| >= 7): at 10 m, 7.5 -> **3**.
   So the Leviathan rises at **1.95**, breaches at 2.55, crashes (the tsunami) at **4.15**; the pool lasts to 9.15; the
   dolphins dive at the Bible's 0.99 ... 2.19 (`paths.txt`; Bible :785-788 "2.05 / 2.55, 3.65 / 4.15" for 2 / 3 hops ✓).
4. **Five TTO-only prefabs, all probed, all on this PC; one BB prefab (`castRing`).** `catalog.txt`: TTO's `whale/effects`
   has 11 TTO-only names; Leviathan Breach uses five (`leviathanBreach_warn`, `leviathanCall_raise`, `leviathanCall_slam`,
   `leviathanBreach_dolphin`, `leviathanBreach`); the other six (`armorShatter`, `impaler`, `oceanResilience`,
   `tidalPressure`, `sovereignImpale`, `sovereignImpale_rise`) are the two TTO passives' looks (not cued, 3). No arcana
   style. **No prefab has an AudioSource** (`probe.json` sounds: []).
5. **Two scripted movers to build** (section 6): `WhaleDolphin` (each dolphin's hops along its lane, splashes, trail, tail
   and fins) and `WhaleLeviathan` (the Leviathan's keyed rise, breach and dive, its geyser / crash / pool children, tail
   flex, fade). Both are TTO scripts on the prefab roots, not decompiled in `pseudo/`: this report decompiled them (Ghidra
   + capstone) and gives their numbers.
6. **Every sound is the Whale's own `sounds/` clip from BB's rip** (grandTide_ring, shieldBash_hit, whaleWave, grandTide,
   bowlingWhale): `Row6Sound@0x1EC1420` (`:35240-35316`), volume 1 for the owner. All cues are kind `"sound"`; no voice.
7. **Left out:** the owner's screen colour ramp `iceRamp` and the two `Row6Shake`s (the player's camera, Bison decision 35);
   the hits and `wet` on the foe (no effect, Sheep decision 4); the whirlpool's pull (no look).

---

## 1. Shared machinery (`TTO1102:Whale`)

- **`DoRow6Skill(skill, aim, target)@0x1EB8D80`** (`:33095-33251`): only for `whl_leviathanBreach5`; the target must be a
  living enemy on another layer (`Row6Alive`, layer mask `0xfffdff00`), else "Leviathan Breach needs an enemy target." and
  MP / SP back (`:33249-33250`); the aim = `Row6Ground(target position)` at the press (`:33176`); cooldown
  `agiAdjust(120)` (`:33181-33182`); starts `<RPC_leviathanCast>d__302` with `off` = aim - Whale (`:33186-33209`).
- **`Row6Begin(command, mPos, tDir, clip)@0x1EC0670`** (`:35382-35450`): actionState `attack`, myCommand = command, the
  Whale at mPos, `LookAt(mPos + vFlat(tDir))`, `PlayAnimation(clip ?? command, 0.1)` (`DAT_1830031e0` = 0.1), wrapMode
  Once. **`Row6End(command)@0x1EC0D40`** (`:35490-35560`): standby, myCommand `none`, only while still doing it.
  **`Row6Doing(command)@0x1EC0CB0`**: attack and that command.
- **`Row6Spawn(name, pos, rot, owned, loop)@0x1EC1660`** (`:35105-35236`): `Row6Prefab` loads
  `GameAssets/characters/heroes/whale/effects/<name>` (cached, "Cannot find <name> effect"); owned -> `createEffect`, else
  `Instantiate`; with `loop` set, the effect's `Animation` plays that clip, wrapMode Loop (`:35214-35231`). Owned here:
  `castRing` (loop `root`) and `leviathanCall_raise`.
- **`Row6Sound(name)@0x1EC1420`** (`:35240-35316`): `GameAssets/characters/heroes/whale/sounds/<name>`, PlayOneShot, volume
  1 for the owner (`mChar + 0x182`), 0.75 others.
- **Statics** (`Whale::.cctor@0x1EC27F0`, `:35880-35907`; `dump.cs:124125-124164`): `DolphinAt` = [0.55, 0.65, 0.75]
  (`InitializeArray` 1057803469 / 1059481190 / 1061158912), `DolphinSide` = [0, -1, 1]; `SlamAt` 0.6, `CastWindUp` 0.6,
  `LeviathanCast` 1.5, `DolphinLaneGap` 2.2, `DolphinWidth` 1.6.
- **Clocks** (`:32960-33062`): `CallLength` = DolphinAt[last] = **0.75**; `LeviathanAt(hops)` = 0.5 hops + 0.75 - 0.3;
  `BreachAt` = LeviathanAt + 0.6; `CrashAt` = LeviathanAt + 2.2; `DiveAt(i, j)` = DolphinAt[i] + 0.5 (j + 1) - 0.06
  (`@0x1EB8CE0`, `:34599-34627`).
- **`LeviathanDir(off)@0x1EBB2A0`** (`:34323-34371`): flat, normalised (forward when tiny). **`DolphinLane(whale, spot, dir,
  i, hops)@0x1EB91B0`** (`:34375-34490`): right = cross(up, dir) (the hero's right); from = whale + 1.5 dir + right x 1.43
  DolphinSide[i], to = spot - dir + right x 2.2 DolphinSide[i]; `WhaleDolphin::Lane(from, to, hops)@0x1EF5B10` = hops + 1
  points lerped from -> to; each put on the ground (`Row6Ground`, y 0 on the page).

## 2. Leviathan Breach (`cast1` > `cast2` > `leviathanCall`; cell 454) - released

### 2.1 The cast: `TTO1102:Whale.<RPC_leviathanCast>d__302::MoveNext@0x1EDFFB0` (`:10488-10823`)

State 0, at the press (0):
- `mLeviathanStep + 1` (`:10539-10541`); `castTime` = 1.5 (`0x3fc00000`, `:10542`), x 0.5 if `hasSkill(0x175 = 373)`
  (Reduced Cast, `:10544-10547`), `magAdjust` (`:10549`) -> **0.1** (high INT, the floor).
- actionState `attack`, myCommand `cast` (`:10553-10561`); the Whale at mPos, `LookAt` the spot (`:10566-10578`).
- **`PlayAnimation('cast1', 0.2)`**, Once (`:10581-10583`). No voice.
- The owner's `DisplayCastBar(castTime)` (`:10616`).
- **`castRing`** through `Row6Spawn` at the Whale, `Quaternion.Euler` rad (4.71239, 1.5708, 0) = **(270, 90, 0)**, owned,
  loop **`root`** (`:10620-10634`). BB's castRing (`probe_bb.json`): EffectControl life 60, afterLife 0, followPosition +
  followState; its default Animation clip is `create` (a 0.47 s grow from scale 0.18), which `root` replaces here.
  followState ends it when myCommand changes: `Row6Begin('leviathanCall')` at 0.1 -> **cut 0.1**.
- An older warn destroyed (`:10635-10646`); **`leviathanBreach_warn`** at mPos + off (**the 10 m target point**),
  `LookRotation(vFlat(off))` = the Whale's facing, **not owned** (`:10647-10682`), kept as `mLeviathanWarn` (0x680).
- `Row6Sound('grandTide_ring')` (`:10684`).

Each frame after (state 1, `:10694-10817`), while still `attack` / `cast` and this step:
- at `start + min(0.6, castTime)` = 0.1: **`PlayAnimation('cast2', 0.1)`**, wrapMode Loop (`:10718-10730`);
- at `start + castTime` = 0.1 on the owner's client (`mChar + 0x182`): `StartCoroutine(RPC_leviathanBreach(Whale, spot -
  Whale, tID))` (`:10760-10781`) and the RPC to the others (`:10789-10811`): the same frame as `cast2`. (A remote copy waits
  up to 1.5 s more for that RPC, else `RPC_cast0`, `:10740-10756`.)
- Interrupted (another action, a stun): the warn is destroyed (`:10694-10710`).

### 2.2 The call: `TTO1102:Whale.<RPC_leviathanBreach>d__303::MoveNext@0x1EDF630` (`:10155-10467`)

Times from its start (= cast + 0.1):
- **0** (state 0): step + 1 (`:10213`); dir, **hops 3** (`:10227-10235`); the warn `Destroy(warn, CrashAt(3) = 4.15)`
  (`:10236-10254`: it lives cast 0 -> 4.25, never its own 8 + 0.3); **`Row6Begin('leviathanCall', ...)`** (`:10260`):
  `PlayAnimation('leviathanCall', 0.1)`, Once; **`leviathanCall_raise`** at the Whale, the Whale's rotation, **owned**
  (`:10276-10291`; EffectControl 2.0 + 0.6, followPosition + followState -> **cut 0.75** at Row6End);
  `LeviathanRise(spot, dir, 3)` started (`:10297-10298`); for i = 0, 1, 2 `DolphinLeap(start + DolphinAt[i],
  DolphinLane(mPos, spot, dir, i, 3))` (`:10362-10380`); the player's own `CameraEffect.AddColorRamp('iceRamp', 'none', 0,
  0.2)` (`:10316-10336`: the screen, left out); the owner's `LeviathanDamage(mPos, spot, dir, 3)` (`:10339-10349`: hits
  only, 3); **`Until(start + 0.6)`** (`SlamAt`; capstone `0x1EDFF33` addss 0.6, `breach_movenext.asm`).
- **0.6** (state 1, `:10394-10438`), still doing `leviathanCall`: **`leviathanCall_slam`** at the Whale + **0.9 forward -
  0.75 right**, the Whale's rotation, not owned (`:10400-10426`); `Row6Sound('shieldBash_hit')` (`:10427`);
  `Until(start + DolphinAt[0])` = 0.55 (capstone `0x1EDF9C7` addss [array + 0x20]): already past.
- **0.6** (state 2, `:10451-10465`): `Row6Sound('whaleWave')` (`:10453`); `Until(start + CallLength = 0.75)`.
- **0.75** (state 3): `Row6End('leviathanCall')` (`:10442-10447`): standby. The clip runs on to 2.4.

**The dolphins** (`<DolphinLeap>d__308::MoveNext@0x1ECD580`, `annot\Whale.c:1-88`): `Until(at)`, then
**`leviathanBreach_dolphin`** at lane[0], `Quaternion.identity`, not owned, and `WhaleDolphin.Play(lane)` (P1). On the page
(x right, d ahead; `paths.txt`):

| dolphin | spawn | from (x, d) | to (x, d) | splashes (scale 1 / 0.8 / 0.8 / 1) | gone |
|---|---|---|---|---|---|
| 0 middle | 0.55 | (0, 1.5) | (0, 9) | 0.61, 0.99, 1.49, 1.99 | 4.55 |
| 1 left | 0.65 | (-1.43, 1.5) | (-2.2, 9) | 0.71, 1.09, 1.59, 2.09 | 4.65 |
| 2 right | 0.75 | (1.43, 1.5) | (2.2, 9) | 0.81, 1.19, 1.69, 2.19 | 4.75 |

Each hop is 2.5 m long and peaks 1.8 m up (arc = clamp(0.45 x 2.5, 1.8, 3.4)), from 1.4 m under the ground.

**The Leviathan** (`<LeviathanRise>d__304::MoveNext@0x1ECEEC0`, `:912-1050`; `start` = the call's start):
- `Until(start + LeviathanAt(3) = 1.95)`: **`leviathanBreach`** at **the spot** (d 10), `LookRotation(dir)` (the Whale's
  facing), not owned (`:986`); `WhaleLeviathan.Play(spot, dir)` (`:1005`; P2: geyser and trail at +0.5 = 2.45, crash and
  pool at +2.2 = 4.15, trail off, the body hidden after 3.3 = 5.25, the pool off at +7.2 = 9.15, destroyed at +8 = 9.95).
- `Until(start + BreachAt = 2.55)`: `Row6Sound('grandTide')` (`:1036`); `Row6Shake(spot, 0.4)` (`:1042`, left out).
- `Until(start + CrashAt = 4.15)`: `Row6Sound('whaleWave')`, `Row6Sound('bowlingWhale')` (`:1023-1024`); `Row6Shake(spot,
  0.9)` (`:1030`, left out).

**Timeline** (sequence-relative; the call starts at 0.1):

| s (call) | what |
|---|---|
| cast 0 | cast1, castRing (cut at 0.1), the warn at the target (to 4.25), grandTide_ring |
| cast 0.1 = call 0 | cast2 for a frame; leviathanCall; leviathanCall_raise (cut 0.75) |
| 0.55 / 0.65 / 0.75 | the three dolphins leave (P1) |
| 0.6 | leviathanCall_slam 0.75 m left, 0.9 m ahead; shieldBash_hit; whaleWave |
| 0.75 | Row6End (standby) |
| 0.99 ... 2.19 | the nine dives (P1's splashes) |
| 1.95 | leviathanBreach at the target (P2) |
| 2.4 | the clip ends (idle tail after) |
| 2.45 | its geyser (P2) |
| 2.55 | grandTide (the breach hits) |
| 4.15 | the crash and the pool (P2); whaleWave + bowlingWhale (the tsunami hits); the warn gone |
| 5.25 / 9.15 / 9.95 | the Leviathan's body hidden / the pool off / the prefab destroyed |

## 3. What is left out (only "on an enemy" / the player's screen / not released)

- The owner's `iceRamp` colour ramp (`:10335`) and the two `Row6Shake`s (0.4, 0.9): the player's screen (Bison decision 35).
- `LeviathanDamage@0x1EBB1F0` (`<LeviathanDamage>d__309::MoveNext@0x1ECD7C0`, `:171-880`) and `DolphinStrike@0x1EB9540`
  (`:34634-35040`): `hit`s, the knock-up and push, `wet` (`RPC_AddStatus`, `:620`, `:741`) and the whirlpool's pull: no
  prefab, no sound; `wet`'s look is on the foe (Sheep decision 4).
- **The TTO passives' looks** (Sovereign Impaler #452: `impaler` on the Whale, `armorShatter` and the
  `sovereignImpale` / `sovereignImpale_rise` spear on the foe; Oceans Resilience #453: `oceanResilience` on the Whale,
  `tidalPressure` on the foes; catalog names, their spawn code not traced here). Not cued: neither has a clip in the
  released list (the rule), the foe looks are on an enemy, and neither fires in any tile (Impaler needs Wall Puncture's
  three stacks; Oceans needs Harden Skin stacks from damage taken). Their numbers on Leviathan Breach (the tsunami x 1.25
  on `armorShatter`, the 20-stack DEF term) have no look.

## 4. Sounds and voices

| t (in the cue's key) | kind | name | where | in BB's rip |
|---|---|---|---|---|
| @LeviathanBreach:cast1 0 | sound | grandTide_ring | Row6Sound `:10684` | whale/sounds/ |
| leviathanCall 0.6 | sound | shieldBash_hit | Row6Sound `:10427` | whale/sounds/ |
| leviathanCall 0.6 | sound | whaleWave | Row6Sound `:10453` | whale/sounds/ |
| leviathanCall 2.55 | sound | grandTide | LeviathanRise `:1036` | whale/sounds/ |
| leviathanCall 4.15 | sound | whaleWave, bowlingWhale | LeviathanRise `:1023-1024` | whale/sounds/ |

No voice (no `Row6Voice` in either coroutine), no roll, no AudioSource in any prefab. The names collide with BB clips /
effects (`grandTide`, `bowlingWhale`): the kind keeps them apart.

## 5. Probed 2026-11-13 (office PC, TTO's 2026-11-09 bundles; `probe.json`, `compact.txt`)

All five export with no warning (`probe.err` empty). Materials (19): addsoft 11, alpha 7 (the skins and the water waves),
add 2 (eye, foam); textures 16 (`tto_whlRow6_*`, `tto_Water*`, `tto_Splash3`, `tto_Ring_Water`, `tto_grandTide`,
`tto_Line_vertMultilines4`). ParticleSystems use only the Initial / Shape / Emission / Color / Velocity modules, billboard
render mode (all in `shuriken.js`).

| prefab | EffectControl (life + after) | parts | needs |
|---|---|---|---|
| leviathanBreach_warn | 8.0 + 0.3 (destroyed at 4.25 by the code) | 3 GroundHug discs `repeatForever` (whirl r 7.6-8 alpha, glint r 7.8-7.6, edge r 8-8.2: the tsunami's 8 m), bubbles PS | - |
| leviathanCall_raise | 2.0 + 0.6, followPosition + followState | rise PS (velocity), ground GroundHug (r 0.8-3.2), beam / tip / star ImageEmitters (the raised hand, 4.9-6 m up, 0.35-0.4 s) | - (cut 0.75) |
| leviathanCall_slam | 0.8 + 0.8 | crack / ripple GroundHugs, splash PS, flash ImageEmitter | - |
| leviathanBreach_dolphin | none (`WhaleDolphin`) | `body` > model (yaw 180) > Dolphin SkinnedMeshRenderer (dolphinSkin alpha + eye) on DolphinRig (root, fin_L / fin_R, head, tail1-5), Dolphin_foam (UVScroll -0.9); `core` ImageEmitter; `trail` (3 TrailRendererModern: flukes 0.45 s, finL / finR 0.3 s; spray / mist / glints PS); `splash` (crown / rim bands, ripple / foam discs, jet / drops / sparkle PS) | **P1** |
| leviathanBreach | none (`WhaleLeviathan`) | `body` > model (0, 0, -7), yaw 180 > LeviathanBody SkinnedMeshRenderer on LeviathanRig (root 8.5 up, fins, head, tail1-5), foam (UVScroll -0.35); `trail` (3 trails 0.7 / 0.5 / 0.5 s, glints / spray / mist PS, core); `geyser` (skirt / column / crown bands, ripple / ring / crack discs, jet / drops / climb PS, flash, rays); `crash` at (0, 0, 1.5) (tsunami / tsunami2 / backwash bands r 2-13, flash / foam / shock / crack discs r to 15, splash / spray / rain / mist PS, flash); `pool` (vortex / foam / rim discs r 5.8-6.4, life 4.9; orbit > churn PS 4.4 s) | **P2** |

`castRing` (BB, `probe_bb.json`): Animation `create` (default) and `root`; EffectControl 60 + 0, followPosition +
followState.

## 6. Parts the page lacks (effect: part)

Home `wardrobe/fxparts/tto_whale.js` (new). The rest is built: GroundHugEmitter (`groundhug.js`, `repeatForever` too),
ImageEmitter, TrailRendererModern (`tto_sheep.js`), ParticleSystem (`shuriken.js`), SkinnedMeshRenderer on the effect's
own nodes (`mesh.js`), UVScroll (`uvscroll.js`). Every effect is cued anyway (the rule).

| # | Part | Effects | What it does (source) |
|---|---|---|---|
| P1 | `WhaleDolphin` (the prefab's own script) | leviathanBreach_dolphin | **Awake** (`@0x1EF5410`): `body` hidden; `splash`, `trail` children deactivated (`Child@0x1EF5870`). **Play(lane)** (`@0x1EF5C90`): the lane = the cue's spot (from) -> `to`, `hops` + 1 points (y 0); the root at lane[0], `LookRotation(flat(last - first))`; start; body shown; Pose(0). **Update** (`@0x1EF6F00`), h = 2 (t - start): splash k (0 ... hops) when h >= k - 0.12 + (k == 0 ? 0.24 : 0): a copy of `splash` at point k, the dolphin's rotation, scale 1 (first, last) / 0.8, active, destroyed 3.5 s later (`Fire@0x1EF5930`); `trail` active while h < hops - 0.1 and 0.1 < frac(h) < 0.9; body hidden once h > hops + 0.05, else Pose(min(h, hops)); destroyed at t - start >= 0.5 hops + 2.5. **Point(h)** (`@0x1EF5F80`): segment s = clamp(floor h, 0, hops - 1), u = clamp01(h - s); lerp(P[s], P[s+1], u) - 1.4 up + up x (arc + 1.4) x 4u(1 - u), arc = clamp(0.45 x segment length, 1.8, 3.4). **Pose(h)** (`@0x1EF6430`, `dol_pose.asm`): body at Point(h); forward = Point(h + 0.03) - Point(h - 0.03) (the 0.03 at `0x1EF6502`), rotation LookRotation(forward, up) x Euler(0, 0, 20 sin(pi u)); tail i (tail1-5): rest, then AngleAxis(18 (i + 1) / 5 sin(16 t - 0.9 i), body.right) x it; fin_L / fin_R: rest, then AngleAxis(+-12 sin(9 t), body.forward) x it. |
| P2 | `WhaleLeviathan` (the prefab's own script) | leviathanBreach | **Awake** (`@0x1EF7450`): `body` hidden; `geyser`, `trail`, `crash`, `pool` deactivated; the renderers under body kept. **Play(spot, dir)** (`@0x1EF8B50`): root at the spot, LookRotation(flat dir); start; body shown; Pose(0). **Update** (`@0x1EF95D0`), t = time - start: at 0.5 geyser and trail on; at 2.2 crash moved to CrashPoint (0, 0, 1.5) and on, pool on, trail off; pool off at 7.2; body hidden once t > KeyT[last] + 0.1 = 3.3, else Pose(t); destroyed at 8. **Pose(t)** (`@0x1EF8DE0`): KeyT [0.4, 0.6, 1.3, 1.75, 2.2, 2.7, 3.2], KeyPos (0, -9, 0), (0, -5, 0), (0, 7.5, 0.6), (0, 9, 2), (0, 1.2, 3), (0, -2.6, 3.6), (0, -6.5, 4), KeyPitch [-90, -88, -76, -22, 10, 20, 30], KeyRoll [0, 0, 70, 145, 180, 190, 200] (`.cctor@0x1EF9990`); segment i (the last with t > KeyT[i + 1] stops at len - 2), u = clamp01 over it; body.localPosition = Catmull-Rom(K[i - 1], K[i], K[i + 1], K[i + 2], u) (ends clamped; `CatmullRom@0x1EF7B30`); s = (3 - 2u) u^2; body.localRotation = Euler(lerp pitch, 0, 0) x Euler(0, 0, lerp roll); then Flex, Fade. **Flex(t)** (`@0x1EF8190`, `lev_flex.asm`): amp = 1 before 1.75, 0.45 after; bend = sin(pi (t - 1.9) / 0.6) on 1.9-2.5, else 0; tail i: rest, then AngleAxis((9 amp sin(7t - 0.8 i) - 10 bend) (i + 1) / 5, body.right); head: rest, then AngleAxis(3 sin(3.5 t) - 12 bend, body.right); fins: rest, then AngleAxis(+-18 sin(4 t), body.forward). **Fade(t)** (`@0x1EF7D70`): a = clamp01((t - 0.4) / 0.3) x (1 - clamp01((t - 2.5) / 0.7)), each body renderer's material colour (`_TintColor`, else `_BaseColor`, else `_Color`) with alpha x a, through a MaterialPropertyBlock. |
| P3 | `castRing`'s loop clip (Row6Spawn's `loop`) | castRing | A cue option (`"animLoop": "root"` in section 7) playing that Animation clip looped from the spawn instead of the default `create` (`Whale::Row6Spawn@0x1EC1660` `:35214-35231`). For a 0.1 s ring the difference is its size (full instead of growing from 0.18): question 4. |
| P4 | `SKILL_FX["whale"]` in `wardrobe_fx_tto.py` | all | The five prefabs (`leviathanBreach_warn`, `leviathanCall_raise`, `leviathanCall_slam`, `leviathanBreach_dolphin`, `leviathanBreach`), with the cue names `tto/<prefab>` (the build also takes them from the cues). |

A note for P1 / P2: the children the scripts switch on (`trail`, `geyser`, `crash`, `pool`) must start their emitters'
clocks when switched on (as `tto_cat.js` holds back the anchor's inactive Leash node), and each dolphin splash is a fresh
copy of the `splash` subtree with its own clock.

## 7. The cue entries (ready to paste into `wardrobe/fx_cues/whale.json`)

`checks/fx_whale_research/tto/cues_paste.json` (made and checked by `cues.py`): 3 keys, 14 cues; every `tto/` name is in
`probe.json`, `castRing` in BB's rip, every sound in BB's `whale/sounds/`. The dolphin's `to` / `hops` and `animLoop` are
the parts' (`fx.at`; cueOf passes unknown options on). `whale.json` is `{}` today, so the block is the whole file until the
BB reports' entries join it (`@LeviathanBreach:cast1` / `:cast2` leave the plain `cast1` / `cast2` keys to them).

```json
{
  "@LeviathanBreach:cast1": {
    "why": "TTO1102:Whale::DoRow6Skill@0x1EB8D80 (pseudo/Whale.c:33095-33251: whl_leviathanBreach5, a living enemy target, the aim = Row6Ground under it at the press, cooldown agiAdjust(120)) -> RPC_leviathanCast(mPos, off = spot - whale, tID); TTO1102:Whale.<RPC_leviathanCast>d__302::MoveNext@0x1EDFFB0 (:10488-10823; plans/fx_whale/tto.md 2.1): castTime 1.5, x 0.5 with Reduced Cast 0x175 = 373 (passives on), magAdjust (:10542-10550; high INT: magAdjust's 0.1 s floor, Mole decision 6); actionState attack, myCommand cast (:10553-10561); the Whale at mPos, LookAt the spot (:10566-10578); PlayAnimation(cast1, 0.2), Once (:10581-10583); no voice (no Row6Voice: the plain cast1 entry's BB cast voice is not played); the owner's DisplayCastBar(castTime) (:10616); castRing via Row6Spawn at the Whale, Euler rad (4.71239, 1.5708, 0) = (270, 90, 0), owned, its Animation 'root' played looped (Row6Spawn's loop argument, :10621-10634, Whale::Row6Spawn@0x1EC1660 :35214-35231; castRing: EffectControl life 60 + 0, followPosition + followState: cut when RPC_leviathanBreach's Row6Begin sets myCommand leviathanCall at 0.1, the step change); an older warn destroyed (:10635-10646); leviathanBreach_warn at mPos + off = the 10 m target point, LookRotation(flat off) = the hero's facing, not owned (:10647-10682), kept as mLeviathanWarn and destroyed by RPC_leviathanBreach at its start + CrashAt(3 hops) = 4.15 (:10236-10250, Whale::CrashAt@0x1EB8C90 :33047-33062): 0.1 + 4.15 = kill 4.25 (its own life 8 + 0.3 never reached); Row6Sound grandTide_ring (:10684; Whale::Row6Sound@0x1EC1420: sounds/, volume 1 for the owner). Each frame (state 1, :10694-10817): at min(0.6, castTime) cast2 (0.1 fade, looped, :10718-10730); at castTime the owner starts RPC_leviathanBreach (:10760-10781) in the same frame. The owner's iceRamp screen ramp and Row6Shake are the player's screen: left out (Bison decision 35)",
    "cues": [
      [0, "fx", "castRing", {"rot": [270, 90, 0], "cut": 0.1, "animLoop": "root"}],
      [0, "fx", "tto/leviathanBreach_warn", {"d": 10, "kill": 4.25}],
      [0, "sound", "grandTide_ring"]
    ]
  },
  "@LeviathanBreach:cast2": {
    "why": "TTO1102:Whale.<RPC_leviathanCast>d__302::MoveNext@0x1EDFFB0 (:10718-10730): cast2 at min(0.6, castTime) = 0.1, 0.1 fade, looped, and RPC_leviathanBreach starts in the same frame (castTime 0.1 reached): no cue of its own; this empty entry keeps the plain cast2 entry's BB cues off the Leviathan Breach tile",
    "cues": []
  },
  "leviathanCall": {
    "why": "TTO1102:Whale.<RPC_leviathanBreach>d__303::MoveNext@0x1EDF630 (:10155-10467; plans/fx_whale/tto.md 2.2), 0 = its start (cast + 0.1): state 0: mLeviathanStep + 1; dir = LeviathanDir(off) (@0x1EBB2A0 :34323-34371: flat, normalised); hops = LeviathanHops(mPos, spot, dir)@0x1EBB3F0 (:34496-34530) = WhaleDolphin::Hops(|flat(spot - whale - 2.5 dir)|)@0x1EF5AF0 = 2 + (len >= 7): 10 - 2.5 = 7.5 -> 3 hops; Row6Begin('leviathanCall', mPos, off) (@0x1EC0670 :35382-35450: attack, myCommand leviathanCall, LookAt, PlayAnimation(leviathanCall, 0.1), Once) (:10260); leviathanCall_raise via Row6Spawn at the Whale, the Whale's rotation, owned (:10276-10291; EffectControl 2.0 + 0.6, followPosition + followState: cut at Row6End 0.75); LeviathanRise(spot, dir, 3) started (:10297-10298, <LeviathanRise>d__304::MoveNext@0x1ECEEC0 :912-1050); the three DolphinLeap(start + DolphinAt[i], DolphinLane(mPos, spot, dir, i, 3)) (:10362-10380; DolphinAt [0.55, 0.65, 0.75], DolphinSide [0, -1, 1], Whale::.cctor@0x1EC27F0 :35880-35907): <DolphinLeap>d__308::MoveNext@0x1ECD580 (Ghidra run, checks/fx_whale_research/tto/annot/Whale.c:1-88): Until(at), leviathanBreach_dolphin via Row6Spawn at lane[0], identity, not owned, WhaleDolphin.Play(lane); DolphinLane@0x1EB91B0 (:34375-34490): from = whale + 1.5 dir + right x 1.43 side, to = spot - dir + right x 2.2 side (right = cross(up, dir)), WhaleDolphin::Lane@0x1EF5B10 (hops + 1 points, lerped), each on the ground (Row6Ground): middle (0, 1.5) -> (0, 9), left (-1.43, 1.5) -> (-2.2, 9), right (1.43, 1.5) -> (2.2, 9) (x right, d ahead; part P1 flies them: splashes 0.06 / 0.5 k - 0.06 after the spawn = the Bible's dives 0.99 ... 2.19, gone at 0.5 x 3 + 2.5 = 4.0 after it); the owner's LeviathanDamage(mPos, spot, dir, 3) (:10339-10349: hits only); Until(start + SlamAt 0.6) (capstone 0x1EDFF33, breach_movenext.asm). State 1 (0.6), still doing leviathanCall: leviathanCall_slam via Row6Spawn at the Whale + 0.9 forward - 0.75 right, the Whale's rotation, not owned (:10397-10426), Row6Sound shieldBash_hit (:10427); Until(start + DolphinAt[0] = 0.55) (capstone 0x1EDF9C7): already past, so state 2 runs at once: Row6Sound whaleWave (:10453) at 0.6; Until(start + CallLength = DolphinAt[2] = 0.75) (Whale::get_CallLength@0x1EC8720 :32960-32986); state 3 (0.75): Row6End (standby, :10446). The page plays the 2.4 s clip to its end (Chameleon decision 11); the later cues run in the idle tail. LeviathanRise: Until(start + LeviathanAt(3) = 0.5 x 3 + 0.75 - 0.3 = 1.95) (@0x1EBB160 :32993-33016): leviathanBreach via Row6Spawn at the spot, LookRotation(dir), not owned, WhaleLeviathan.Play(spot, dir) (:959-1005; part P2: geyser at +0.5, crash and pool at +2.2, pool off +7.2, gone +8 = 9.95); Until(start + BreachAt = 1.95 + 0.6 = 2.55) (@0x1EB8C40): Row6Sound grandTide (:1036), Row6Shake(spot, 0.4) left out; Until(start + CrashAt = 1.95 + 2.2 = 4.15): Row6Sound whaleWave and bowlingWhale (:1023-1024), Row6Shake 0.9 left out. Left out: the owner's CameraEffect.AddColorRamp('iceRamp') at 0 (:10316-10336, the player's screen), the dolphin / breach / tsunami / whirlpool hits and wet on the foe (LeviathanDamage, DolphinStrike@0x1EB9540: no effect; Sheep decision 4)",
    "cues": [
      [0, "fx", "tto/leviathanCall_raise", {"cut": 0.75}],
      [0.55, "fx", "tto/leviathanBreach_dolphin", {"d": 1.5, "to": [0, 0, 9], "hops": 3}],
      [0.6, "fx", "tto/leviathanCall_slam", {"x": -0.75, "d": 0.9}],
      [0.6, "sound", "shieldBash_hit"],
      [0.6, "sound", "whaleWave"],
      [0.65, "fx", "tto/leviathanBreach_dolphin", {"x": -1.43, "d": 1.5, "to": [-2.2, 0, 9], "hops": 3}],
      [0.75, "fx", "tto/leviathanBreach_dolphin", {"x": 1.43, "d": 1.5, "to": [2.2, 0, 9], "hops": 3}],
      [1.95, "fx", "tto/leviathanBreach", {"d": 10}],
      [2.55, "sound", "grandTide"],
      [4.15, "sound", "whaleWave"],
      [4.15, "sound", "bowlingWhale"]
    ]
  }
}
```

**Shared changes (the lead's, in `index.html` / the pipeline):**
- **S1** `SEQ.whale`: add `"Leviathan Breach: cast1@0.1 cast2*^@0 leviathanCall^"` (first step's 0.2 s fade = the game's
  `PlayAnimation(cast1, 0.2)`; `^` = the 0.1 s fades of cast2 and Row6Begin).
- **S2** `SEQ_SKILL.whale = { "@LeviathanBreach": "leviathanBreach" }` (the tile shows Leviathan Breach's icon, not the
  Cast pool's: the sequence opens with BB's cast1 / cast2, as the Mole's `@BarrelRailgun` opens with Assemble's clips).
- **S3** `wardrobe_skill_icons.py` `CLIP_SKILLS["whale"] = {"leviathanCall": ["leviathanBreach"]}` (the Bible's
  `whale_leviathanBreach5`; the clip is not named like the skill), then rebuild the HD index.
- **S4** P3's `animLoop` (or drop the option from the castRing cue: question 4).

## 8. Open questions (each with my recommended answer)

1. **The clip after Row6End**: the game frees the Whale at 0.75 s, the clip is 2.4 s. Recommend **play it whole** (the
   game's standby does not cut a Once clip that is still playing, as the Chameleon's Chain Lightning, decision 11); the
   cues to 4.15 s run in the idle tail. Alternative: cut the step at 0.75 (`leviathanCall^@0.75`), which ends on the idle.
2. **Hops**: recommend **3**, the 10 m target's count (the rule). The 2-hop timings (target under 9.5 m) are in section 1.
3. **whaleWave at 0.6 with the slam**: the coroutine's second wait (0.55) is already past when the first (0.6) ends, so the
   sound comes in the same or the next frame. Recommend **0.6** (one frame is below the page's resolution).
4. **castRing's `root` loop** (P3): recommend **build the option** (one line in the Animation part: play the named clip,
   loop); the ring lives 0.1 s here. Alternative: leave the default `create` (the ring shows small for its 0.1 s).
5. **The warn's own 8.3 s life vs the code's Destroy at 4.25**: recommend **kill 4.25** (the code's), as cued.
6. **The TTO passives' looks** (section 3): recommend **left out** (not released; not triggered in any tile). If the user
   wants them, they belong to Wall Puncture's and Harden Skin's tiles, as `tto/impaler` etc., and need their spawn code
   traced (`AddWhaleRow6Status`, `SovereignLance@0x1EC1AC0`, `OceanUpdate@0x1EBB580`).
7. **The iceRamp screen ramp**: recommend **left out** (the player's own camera, as every class's shakes). It is a
   `CameraEffect.AddColorRamp('iceRamp', 'none', 0, 0.2)` for the local player at the call's start.
8. **The Leviathan's flex / fade amplitudes** (P2) are read from the machine code's constants (`lev_flex.asm`,
   `lev_fade.asm`); the builder should check them against the decompile before drawing (they are marked with RVAs).

## 9. For the Bible (offer to the user; that repo's own rules)

- **Leviathan Breach's look and sound timeline** (the reference has the hits' times only): at the press the cast bar plays
  `cast1` (no voice) with the cast ring, a warning circle 8 m wide on the target (gone when the tsunami hits) and the
  `grandTide_ring` sound; at the call the Whale raises its hand (`leviathanCall_raise`), slams the ground 0.6 s later
  0.75 m to its left (`leviathanCall_slam`, `shieldBash_hit` + `whaleWave`), and is free at 0.75 s while the 2.4 s
  animation plays on; the dolphins leave at 0.55 / 0.65 / 0.75 s, each hop 2.5 m long and 1.8 m high (arc =
  clamp(0.45 x hop length, 1.8, 3.4) m), splashing at every landing; the Leviathan rises out of the ground at the target
  (`LeviathanAt`), breaches 9 m high, rolls 200 degrees over and dives 4 m beyond the target, the tsunami ring
  (`crash`, 1.5 m beyond the target) and the 6 m whirlpool (5 s) at `CrashAt`; sounds `grandTide` at the breach and
  `whaleWave` + `bowlingWhale` at the tsunami; camera shakes 0.4 and 0.9 and an `iceRamp` screen tint for the caster.
- **The cast with Reduced Cast** reaches magAdjust's 0.1 s floor at high INT (the card already models 0.75 before
  magAdjust).

## Verification (the researcher's own checks)

- Every wait Ghidra dropped was read from the instructions: the state 0 `Until(start + 0.6)` (`0x1EDFF33`), the state 1
  `Until(start + DolphinAt[0])` (`0x1EDF9C7`, `[rcx + 0x20]` = element 0 of the static at `Whale + 0`); the other clocks are
  labelled DAT constants (0.5, 0.75 via the array, 0.3, 0.6, 2.2, 0.06, 7, 1.43, 2.2, 1.5).
- `DolphinAt` / `DolphinSide` / `KeyT` / `KeyPitch` / `KeyRoll` are the annotator's `InitializeArray` labels; `KeyPos` and
  `CrashPoint` are the `.cctor`'s hex stores (0xc1100000 = -9, 0xc0a00000 = -5, 0x40f00000 = 7.5, 0x3f19999a = 0.6,
  0x41100000 = 9, 0x40000000 = 2, 0x3f99999a = 1.2, 0x40400000 = 3, 0xc0266666 = -2.6, 0x40666666 = 3.6, 0xc0d00000 = -6.5,
  0x40800000 = 4; CrashPoint (0, 0, 0x3fc00000 = 1.5), the prefab's `crash` node position too).
- `paths.py` asserts 3 hops, 1.95 / 2.55 / 4.15, the 1.8 m peaks; its dive times equal the Bible's (:787).
- `cues.py`: 14 cues parse; every name checked (`tto/` in `probe.json`, `castRing` in BB's rip, the five sounds in BB's
  `whale/sounds/`).
- Not done: a browser check (read-only researcher); the TTO 11-06 / 11-09 builds were not re-read (the Bible: 11-06
  changed only the description text).

## Verification (13/11/2026, checker)

Read-only re-derivation on the office PC: TTO1102 `pseudo/Whale.c` (the cast :10488-10823, the call :10155-10467,
LeviathanRise :912-1053, the clocks :32960-33062, DolphinLane :34375-34490, LeviathanHops :34496-34530, Row6Spawn
:35105-35236), this report's own Ghidra / capstone outputs (`checks/fx_whale_research/tto/annot/*.c`, `*.asm`), TTO's
11-09 bundles through the tool's exporter, BB's rip, the Bible (`whale-skill-reference.md` :773-812). Probes in
`checks/fx_whale_research/verify/`: `tto_castring.json` (`wardrobe_fx_tto.py whale --probe castRing`), `blocks.py` ->
`blocks.txt` (both reports' blocks parsed and checked against `OPTS` / `KINDS` / `ENTRY_KEYS` of `wardrobe_fx_check.py`,
the clips, the page's SEQ ids and every name), `sizes.py` (method sizes in the three TTO builds). This section wins over
the body.

**Confirmed** (no change): every wait and its sum (cast bar 1.5 x 0.5, then magAdjust's 0.1 floor; cast2 at
min(0.6, bar), :10718-10730; the call's `Until(start + 0.6)` (asm `0x1EDFF33` addss 0.6), `Until(start + DolphinAt[0])`
(`0x1EDF9C7`, element 0 = 0.55, already past), `Until(start + CallLength 0.75)`; LeviathanRise's three Untils (:954,
:1013, :1045) with LeviathanAt = 0.5 x 3 + DolphinAt[2] 0.75 - 0.3 = 1.95, BreachAt = 1.95 + 0.6 = 2.55, CrashAt =
1.95 + 2.2 = 4.15); Hops = 2 + (|flat(spot - dir - (whale + 1.5 dir))| >= 7) (:34496-34530, `annot/WhaleDolphin.c:221-225`):
10 - 2.5 = 7.5 -> 3; the lanes (`right` = cross(up, dir) = (dz, 0, -dx) = +x, so side -1 is the hero's left,
:34433-34460); the slam at + 0.9 forward - 0.75 right, the Whale's rotation, not owned (:10400-10426); the raise owned at
the Whale (:10276-10291); the warn at mPos + off, LookRotation(flat off), not owned, then `Destroy(warn, CrashAt(hops))`
(:10236-10254); castRing at Euler rad (4.71239, 1.5708, 0), owned, loop `root` (:10620-10634; Row6Spawn plays the named
clip and sets Loop, :35214-35231); EffectControl's followState compares both actionState and myCommand (BB
`EffectControl.cs:226-232`), so the ring ends when Row6Begin sets `leviathanCall`; no voice in either coroutine (their
string tables hold no Row6Voice / Voices path); LeviathanDamage and DolphinStrike load no prefab and play no sound (no
string but `dead`; `wet` is status id 0x2329 through RPC_AddStatus, :620); the dolphin's Update (splash at
h >= k - 0.12, + 0.24 for k = 0, scale 1 / 0.8; the trail window; hidden after hops + 0.05; destroyed at 0.5 hops + 2.5:
`annot/WhaleDolphin.c:445-540`), so the splashes 0.61 / 0.99 / 1.49 / 1.99 (+ 0.1, + 0.2) and the Bible's dives (:787);
KeyT [0.4, 0.6, 1.3, 1.75, 2.2, 2.7, 3.2], KeyPitch [-90, -88, -76, -22, 10, 20, 30], KeyRoll [0, 0, 70, 145, 180, 190,
200] are the `.cctor`'s `InitializeArray` field labels (`annot/WhaleLeviathan.c:1307-1309`); the P1 / P2 constants are in
the instructions (`dol_pose.asm`: 0.03, 18, 16, 0.9, 12, 9, 20; `dol_point.asm`: 1.4, 1.8, 3.4, 0.45, 4; `lev_fade.asm` /
`lev_flex.asm`: 0.4, 0.3, 2.5, 0.7, 0.45, 1.75, 1.9, 0.6, 7, 0.8, 9, 10, 3.5, 3, 12, 18, 4); the five prefabs'
EffectControls (warn 8 + 0.3, raise 2 + 0.6 followPosition / followState, slam 0.8 + 0.8; dolphin and Leviathan none) and
nodes (`crash` at (0, 0, 1.5), `model` at (0, 0, -7)); no node is saved inactive in any of the five, so P1 / P2's Awake
must switch the children off (as written); every ParticleSystem module used (Initial, Shape, Emission, Color, Velocity;
billboard) is read by `shuriken.js` (:256); the clip `leviathanCall` (2.4 s, `tto: true`) and cast1 / cast2 (0.6 s) in
`wardrobe/data/whale/clips.json`; the released list (`wardrobe/tto_released.json` whale clips: clap, leviathanCall, wai);
the S1 tokens parse with `SEQ_ALT` (index.html:1413) and the id is `@LeviathanBreach` (`chains()`, :1445); the plain
`leviathanCall` tile is hidden once the chain uses it (:3700); cues after the 2.4 s clip run in the idle tail
(`play(idleName(), true)`, :1571); a `cut` at its step's end (castRing's 0.1) comes at the step change (the cue-format
comment, the Chameleon's venomPhantom_coil); the Bible icon `whale_leviathanBreach5` exists (`assets.js`); every `tto/`
name is in `probe.json`, every sound in BB's `whale/sounds/` (grandTide_ring, shieldBash_hit, whaleWave, grandTide,
bowlingWhale .wav), and TTO's catalog has no TTO-only Whale sound; the block is valid JSON, 3 keys, 14 cues, its keys real
(`blocks.txt`). TTO 11-06 / 11-09: the 57 methods of this skill (the five coroutines, the Row6 helpers, the clocks,
WhaleDolphin, WhaleLeviathan) have the same byte size in all three builds (`sizes.py`): no change found.

1. **castRing is TTO's own copy; BB's stands for it (decided).** What is wrong: "one BB prefab (`castRing`)" (Read this
   first 4) and "BB's castRing (`probe_bb.json`)" (2.1). `Row6Spawn` loads the catalog address
   `gameassets/characters/heroes/whale/effects/castring` from TTO's bundles. Probed (`verify/tto_castring.json`): the same
   root (Animation `create` 0.467 s default, `root` 2 s Loop, plus a `destroy` 0.5 s; EffectControl 60 + 0,
   followPosition + followState; AudioSource `cast1`, looped, playOnAwake), the same `castRing` mesh node (scale 0.1, rot
   (0, 0, 0.707, 0.707), `tto_Ring_Water` addsoft = BB's Ring_Water), plus one node `ImageEmitter` at y 0.2 that holds
   only a MeshRenderer (`tto_Ring_Frozen`): no MeshFilter and no emitter script, so it draws nothing; the `destroy` clip is
   never seen (afterLife 0: gone in the frame followState ends). The cue keeps BB's `castRing` (no `tto/`), as the
   Monkey's castEffect_fire; `SKILL_FX["whale"]` holds the five TTO prefabs only (P4 as written).
2. **A missed sound: castRing's own `cast1`.** What is wrong: section 4 ("no AudioSource in any prefab") and section 9
   ("cast1 (no voice)") leave out that the ring carries a looped, playOnAwake AudioSource `cast1` (BB's copy and TTO's):
   the cast sound plays from the press until the ring goes at 0.1. No cue is needed (the effect plays it; `wardrobe_fx.py`
   builds `cast1.mp3` with castRing). Section 4's table gains the row
   `@LeviathanBreach:cast1 0 | (effect) | cast1, looped, to 0.1 | castRing's AudioSource | whale/sounds/cast1.wav`.
3. **Two cue options are missing from the checker's list.** What is wrong: `animLoop` (the castRing cue) and `hops` (the
   three dolphin cues) are not in `OPTS` (`pipeline/wardrobe_fx_check.py:215-221`), so the gate rejects the entries
   (`blocks.txt`). Corrected (page_pipeline): `OPTS += "animLoop", "hops"`, and the cue-format comment (index.html, after
   :4763) gains "animLoop (the effect's own Animation clip played looped from the spawn, Row6Spawn's `loop`:
   TTO1102:Whale::Row6Spawn@0x1EC1660; Leviathan Breach's castRing, fxparts/bat.js), hops (a Leviathan Breach dolphin's hop
   count, the hero's LeviathanHops; fxparts/tto_whale.js)". The block itself is unchanged.
4. **P3 / question 4 decided: built, in bat.js's `fx:castRing`.** The rule (every missing part built), and the ring shows
   full-sized and turning instead of growing from 0.18 for its 0.1 s. Home: `fx:castRing` (`fxparts/bat.js:442-453`, agent
   A's, whose gate already lets `"whale"` through by parts.md part 7): when the cue gives `animLoop`, its first update plays
   it with `play(name, 0, LOOP)` and the 0.5 s restart is skipped. No new file.
5. **The dolphin's cue shape is this report's, not parts.md's Interfaces 6.** parts.md fixes `from` / `to` options and the
   part computing `Hops(|to - from|)`. Decided: this block stands: the cue's own spot (`x`, `d`) is lane[0], `to`
   ([x, y, d]) the lane's end, `hops` given (3). Reason: the game counts hops from the spot (`|spot - whale - 2.5 dir|` =
   7.5), not from a lane's length (7.54 for the side lanes: the same count here, not the game's formula). Builder B reads
   `fx.at.to` and `fx.at.hops` and makes `Lane(from, to, hops)` (hops + 1 points lerped, y 0).
6. **Questions 1-3 and 5-8 decided as recommended**: the clip plays whole (Chameleon decision 11); 3 hops (the 10 m rule);
   whaleWave at 0.6; the warn's kill 4.25 (the code's Destroy); the TTO passives' looks left out (not released, Mole
   decision 15; looks on the foe, Sheep decision 4 as the Bat's tto Q6); iceRamp and the shakes left out (Bison decision
   35); question 8 is closed by the constants above (the instructions hold every number P1 / P2 use).
7. **S2 and S3 are both needed (against the Monkey's verification 3).** `wardrobe_skill_icons.py` maps a clip to a skill
   only by its name or by CLIP_SKILLS (:120), so without S3 the HD index has no `leviathanBreach` and the tile no icon;
   with S2 the tile shows that icon alone (`moveSkillIcons`, index.html:3457-3461) instead of the cast skills', and
   dropping `leviathanBreach` from other tiles' icons costs nothing (only this chain plays `leviathanCall`). The Mole's
   `@BarrelRailgun` precedent (a chain opening with shared clips) holds; the Monkey's call was for tiles whose skill also
   shows on another tile.
8. **Section 9 (the Bible offer) wording.** "a warning circle 8 m wide" -> **8 m in radius** (the warn's edge disc r
   8-8.2, the tsunami's r 8, Bible :793); "breaches 9 m high" -> "its body's pivot rises to 9 m" (KeyPos (0, 9, 2) is the
   `body` node; the model hangs from it at (0, 0, -7) with its rig root 8.5 m up, so the creature's own height differs);
   add "the cast ring plays the cast sound `cast1`" (item 2).
