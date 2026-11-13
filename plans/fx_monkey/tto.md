# Monkey effects + sounds research: the TTO Lv 100 clips (Ja Ascension, Buiten Bastion, Rune Golem)

Scope: the five TTO clips of `wardrobe/data/monkey/clips.json` (`tto: true`, group `skill`): `jaAscension` (1.133 s),
`solarCall` (1.3 s), `buitenBastion` (1.267 s), `sanctumRaise` (1.5 s), `golemCall` (1.467 s). No BB code plays them.
Research only: this file is the only repo file written, plus the probes in `checks/fx_monkey_research/tto/`
(git-ignored). Office PC, 13/11/2026.

**Released list** (`wardrobe/tto_released.json`, monkey clips: buitenBastion, clap, golemCall, jaAscension, solarCall,
wai): four of the five get cues. **`sanctumRaise` (Buiten Bastion's active, "Earthen Offering") is not released**
(the file's `_about`: "not Buiten Offering's sanctumRaise"): researched below (2.4) but no cue, no sequence, no part.

Sources:
- TTO's pseudo-C `C:\Users\Jump\Desktop\12tails\DecompiledSource_TTO_2026-11-02\pseudo\Monkey.c` (cited `Monkey.c:<line>`,
  with the stable `TTO1102:Method@RVA`) and `pseudo\CharacterControl.c`; `pseudo_c6_extra\monkey\{Ja, Buiten, RuneGolem,
  SunCrownFx, BastionWardFx, SunburnFx, MonkeyBuitenOffering}.c` (cited `Ja.c:`, `Buiten.c:`, `RuneGolem.c:`);
  `dump.cs` for fields and constants. The later builds: `DecompiledSource_TTO_2026-11-06\research\patch_1106\` (the
  method diff and `pseudo\Monkey.c`, cited `TTO1106:` / `1106 Monkey.c:<line>`) and `DecompiledSource_TTO_2026-11-09\
  research\patch_1109\` (`method_diff_all.txt`, `semdiff_all.txt`).
- capstone over `client\GameAssembly.dll` for the one body never decompiled (`SunCrownFx::LateUpdate@0x1D6DED0`):
  `dis.py` -> `suncrown_late.asm`.
- The Bible: `12t_reference\monkey-skill-reference.md` "TTO Lv 100 skills" (:892-969: Ja Ascension :896-922, Buiten
  Bastion :924-940, Rune Golem :942-961) and the cards `monkey_ja` (`12t_projects\bible\index.html:18275`),
  `monkey_buiten` (:18628), `monkey_jaAscension` / `monkey_buitenBastion` / `monkey_runeGolem` (:19210-19212).
- TTO's bundles (this repo's `tto_assets\2026-11-09`, found by `wardrobe_fx_tto.py`):
  `wardrobe_fx_tto.py monkey --probe <24 names>` -> `probe.json` (`compact.py` -> `compact.txt`); the summons' own
  folders, which that tool cannot reach (it only reads `heroes/<cls>/effects/`), through `probe_elem.py` (the tool's own
  exporter with another catalog folder) -> `probe_ja.json`, `probe_buiten.json`, `probe_golem.json`,
  `probe_golembody.json` (+ `.txt`); `catalog.py` -> `catalog.txt` (every TTO address under `heroes/monkey/` and
  `elementals/ja|buiten|runegolem`, marked against BB's rip); `animator.py` (the FX_Magic_Circle AnimatorController and
  its clip); `voice.py` (TTO's voices/buiten, ja, summon, upheaval); BB's `castEffect_fire` through
  `wardrobe_fx.py monkey --probe castEffect_fire` -> `probe_bb.json`.
- `cues_paste.json`: section 7's block, parsed (6 keys, 22 cues).

Times are seconds from the start of the clip (or sequence step) the cue is keyed by. Every TTO Monkey wait is
`Waits.Get(t)` (a cached WaitForSeconds: a step to add), except the comet's and the collapse's per-frame clocks
against `Time.time`. Max rank: the passives boost the **rank 4** Ja / Buiten (sLv 4 -> level 6); the three Lv 100
skills have one rank. The camera shakes (`Monkey::ShakeNear@0x1CD40F0`, Monkey.c:43449-43486, `SendMessage
AddCamereShake` within 30 m; `RuneGolem::Shake`) are the player's screen: left out everywhere.

## Read this first

1. **Four released tiles, all after the shared cast bar.** Every one of them is a release of `RPC_cast`
   (`TTO1102:Monkey.<RPC_cast>d__178::MoveNext@0x1CE8830`, Monkey.c:2434-3866: cast1 (0.2 fade), the bar with cast2
   looped (0.2 fade, :2590-2600), then the release by command): the BB Ja / Buiten casts swap their release for the
   TTO coroutine when 452 / 453 is learned (`hasSkill(0x1c4)`, :3260-3300; :3660-3700), and the commands
   `jaAscension` / `buitenBastion` go to `ReleaseRow6Active` (:3433-3439), `runeGolem` to `RPC_runeGolem_cast`. So the
   tiles are sequences (shared change S1, section 7): `cast1 cast2*~@0.1 <clip>~0.15 root*~@<hold>` (the 0.1 s bar =
   magAdjust's floor, Mole decision 6; every TTO clip starts with `PlayAnimation(clip, 0.15)`; the root hold keeps
   the tile until the summon or the crown's end is shown).
2. **Two clips are the passives on BB summons, two are actives.**
   - `jaAscension` = **Ja Hou Hou IV with Ja Ascension learned** (the boosted summon: Ja level 6 with its aura); its
     own tile, as the Mole's `missilePad` (Missile with Twin Warhead) beside BB's `missile`. BB's Ja tile stays BB's.
   - `buitenBastion` = **Buiten Hou Hou IV with Buiten Bastion learned** (the statue at level 6, x 1.2, with its aura).
   - `solarCall` = **Ja Ascension's active** ("Sun Avatar" in the code): the Ja becomes a comet, the crown, and at
     its end the Solar Collapse.
   - `golemCall` = **Rune Golem**: the golem's summon; the golem itself (TTO-only character, its own AI) is part P9.
   - `sanctumRaise` = Buiten Bastion's active (Earthen Offering): **not released**, no cue.
3. **The summons are shown and cut at 10 s** (Mole decision 32, Bat decision 25): the boosted Ja / Buiten are BB's
   `elementals/ja/Ja4` / `elementals/buiten/Buiten4` (in BB's rip; the BB research's summon part) plus TTO's boost
   (part P8: level 6, the aura prefab, the Buiten's x 1.2); the Rune Golem is TTO's
   `elementals/runeGolem/RuneGolem` (model and clips in TTO's bundles only; part P9). The cue names `Ja4` / `Buiten4`
   are the BB summon part's to fix (question 2).
4. **Sun Avatar needs a Ja**: the tile shows the boosted Ja already standing 2 m ahead from the tile's start (as the
   Mole's King Kaiser already standing, decision 37), hidden and gone at the bar's end (`@SunAvatar:cast1`, which
   must also carry the BB research's cast1 cues: a `@seq:clip` key replaces the plain one).
5. **The crown is cut at 10 s and its end is shown** (Mole Q1's reasoning: the recast ends it early in the game). In
   TTO's current clients (1106, 1109: the bundles' build) a recast with an enemy selected within 30 m flat sends the
   sun onto that enemy: the collapse lands on the 10 m target (question 1; the 1102 / time-up version lands on the
   Monkey).
6. **Voices: four, one not in BB's rip.** `Row6Voice` (`Monkey::Row6Voice@0x1CD3510`, Monkey.c:43213-43288) plays
   `heroes/monkey/voices/<name>` at volume 1 for the owner (0.75 others), only in game types > 4 (quests, PvP,
   arenas) and for the own team: `ja` (jaAscension, solarCall), `buiten` (buitenBastion), `summon` and `upheaval`
   (golemCall). **`buiten`: BB's rip has only `voices/buiten.wav.meta`** (no audio; BB's own `RPC_buiten_cast` loads it,
   Monkey.cs:33909): TTO's clip (0.767 s, 22050 Hz mono, `voice.py`) is part P10 (Sheep decision 10: TTO's fixed
   files where BB's are missing). No hero `sounds/` clip is played; the only other sounds are prefab AudioSources
   (`jaAscension_supernova`: gaosFire_hit 1.0 + explosion1 0.5; `jaAscension_flare`, `sunAvatar_sunburst`,
   `runeGolem_riseBurst` the same pair), which come with their effects.
7. **New page parts** (section 6): the "Eric/URP Particles/Additive" and "Alpha Blended" shaders (46 materials; no
   class had them), an Animator with an AnimatorController (FX_Magic_Circle: the sigils' texture scroll), the Ja model's
   own Animation clip inside two effects, three code movers (the comet, the crown, the collapse), the boosted summons,
   the Rune Golem with its AI, TTO's voice, and the exporter reaching `elementals/<x>/effects`.

---

## 1. Shared machinery (`TTO1102:Monkey`)

- **`PlayRow6Fx(name, at, rot)@0x1CC8EC0`** (Monkey.c:43130-43210): loads `GameAssets/characters/heroes/monkey/
  effects/<name>` (cached in `mRow6Fx`, `Cannot find <name> Effect`), a bare `Instantiate` (no owner, no createEffect).
  None of the in-scope roots has followState (section 5), so the bare Instantiate changes nothing here.
- **`SummonSpot(ahead)@0x1CD52D0`** (:43385-43446): `Math.getSpawnPos(position + ahead x forward)` (the ground point),
  the hero's position if that comes back zero. On the page's floor: `ahead` m straight ahead, y 0.
- **`Row6Voice(name)@0x1CD3510`**: above (Read this first 6).
- **`Still(command)@0x1CD5160`** (:43291-43315): attack and myCommand == command; each later state returns when not
  (an interrupted pose spawns nothing more). **`EndRow6Action(command)@0x1CC65D0`** (:43318-43382): standby, command
  none.
- **`SendBoostedCreate(code, pos, dir, boost)@0x1CD3CA0`** (:43489-43765): the owner's Photon event 0x4a with the
  code (-250 - sLv: Ja; -350 - sLv: Buiten), the position x 50, the direction x 200, and the boost 2;
  `OnRow6ActionEvent@0x1CC7EF0` (:41462) sets `mSummonBoost` and calls `RPC_ja_create` / `RPC_buiten_create`, which
  read it after the Instantiate (:37518-37528, :39194-39204).
- **Status looks** (`CharacterControl::AddMonkeyRow6Status@0x24ADB60`, CharacterControl.c:16854-16882 ->
  `AddMonkeyRow6Fx@0x24AD6A0`, :17181-17345): `<status>` from `heroes/monkey/effects/` (`stoneAegis` and `runeFracture`
  from `elementals/runeGolem/effects/`) at the holder's position, identity, named `<status>Fx`, parented (world pose
  kept), localScale = clamp(2 x CharacterController radius x lossyScale, 1, 4) / lossyScale (the Monkey: radius 0.2 ->
  **1**), then `BastionWardFx.Bind` / `SunCrownFx.Bind` / `SunburnFx.Bind`; one per status (an existing `<status>Fx` is
  kept). Removed with the status (`RemoveMonkeyRow6Status@0x24C2260`, :16883ff).
- **`HeadHeight()@0x24B4A00`** (CharacterControl.c:17371ff): max(0.8, collider bounds top - position y) (+ 1.2 with
  status 0x394). The Monkey's CharacterController (BB `heroes/monkey/Monkey.prefab`: height 1.3, radius 0.2, centre
  y 0.7): **1.35**.

## 2. Per skill

### 2.1 Ja Hou Hou IV with Ja Ascension (`jaAscension`, 1.133 s; the passive of cell 452) - released

Coroutine `TTO1102:Monkey.<RPC_jaAscension_cast>d__315::MoveNext@0x1D084F0` (Monkey.c:10252-10460), started at the
bar's end in place of BB's `RPC_ja_cast` (Monkey.cs:28920-29271: cast3, castEffect_fire at 0.3, the create at 0.4):

| t (s) | what | where | cite |
|---|---|---|---|
| 0 | attack, command `ja`; `PlayAnimation(jaAscension, 0.15)` Once; voice **ja** | | :10304-10319 |
| 0 | spot = SummonSpot(**2**) | 2 m ahead, ground | :10320 |
| 0.25 | **castEffect_fire** (the hero prefab's field +0x2a0, `dump.cs:111686`; BB's own `heroes/monkey/effects/castEffect_fire`) | position + TransformDirection(0, 1, 1): **1 up, 1 ahead**, the hero's rotation | :10347-10370 |
| 0.45 | **jaAscension_pillar** | the spot, identity | :10389-10399 |
| 0.5 | owner: SendBoostedCreate(-254, spot, forward, 2) -> `RPC_ja_create@0x1CCD070`: `elementals/ja/Ja4` at the spot, LookRotation(forward), then **`Ja.Ascend(2)`** | the spot | :10422-10434; :37216-37530 |
| 1.15 | EndRow6Action: standby (the clip ends at 1.133) | | :10439, :10453 |

`TTO1102:Ja::Ascend@0x1D3D0B0` (Ja.c:2728-2819): level = clamp(4 + 2, 1, 6) = **6**, HP 600 (no look),
followDistance = 0.5 x 6 + 2 = **5** (:2763), and from level 5 **`elementals/ja/effects/jaAscension_aura`** at the Ja,
its rotation, named `jaAscensionFx`, parented with the world pose kept (:2768-2805). The aura has no EffectControl: it
lives as long as the Ja. The summon's own look (its `summon` clip, BB's summon ring, its `[ja]` aura status on the
Monkey every 3 s) is BB's (`Ja.<summon>d__23@0x1D4E600`, Ja.c:474-790): the BB summon part. Cut at 10 s: the unsummon
(`Ja.<unsummon>d__26@0x1D4F890`, Ja.c:791-910: the `ko` clip, Destroy 1 s later) at 10.5, gone at 11.5.

### 2.2 Ja Ascension, the active (`solarCall`, 1.3 s; "Sun Avatar", cell 452) - released

The bar (1.5 s x magAdjust; 0.1 s at the floor) ends in `ReleaseRow6Active('jaAscension')` -> **`Monkey::
ReleaseSunAvatar@0x1CD2840`** (Monkey.c:44330-44415): `PickJa` (a living Ja of this Monkey within 30 m, the highest
level first; none: "Sun Avatar needs a summoned Ja", MP / SP back), then the coroutine with from = the Ja's position,
offset = Monkey - Ja, jaNr (:44370-44399), the RPC to the others, `SpendJa` (:44401: the Ja killed). Coroutine
`TTO1102:Monkey.<RPC_sunAvatar_cast>d__352::MoveNext@0x1D20100` (Monkey.c:20405-20846; TTO1106 d__357@0x1D28970 has the
same strings, waits and constants, `1106 Monkey.c:1005-1452`; only the crown's length became `chaAdjust(6)`):

| t (s) | what | where | cite |
|---|---|---|---|
| 0 | jaLv = the Ja's mSummonLv (6; 4 if none); the Ja **hidden** (`Monkey::HideBody@0x1CC6F90`) | | :20485-20550 |
| 0 | **jaAscension_launch** | the Ja (2 m ahead), identity | :20552-20566 |
| 0 | **sunAvatar_comet** (the Ja's model rides inside: its `Ja` node, 0.55 scale) | start = the Ja + **1.2 up** = (0, 1.2, 2), identity | :20570-20598 |
| 0 | posing (attack + cast): command sunAvatar, the hero turned to the Ja (flat; it is straight ahead: no turn), `PlayAnimation(solarCall, 0.15)` Once, voice **ja** | | :20600-20671 |
| 0 | **jaAscension_callFx** | the hero, its rotation | :20672-20687 |
| 0-0.9 | the comet each frame on Monkey::Bezier(start, mid + up x rise, end, s), mid = (start + end) / 2, **rise = 4 + 0.12 x \|flat offset\| = 4.24**, end = the hero + up x (HeadHeight + 0.6) = **(0, 1.95, 0)**, s = (3 - 2u) u^2, u = t / 0.9 (peak 3.7 m up at s 0.5) | | :20689-20826; Bezier :44450-44475 |
| 0.9 | the comet destroyed; **sunAvatar_ignite** at the hero, its rotation; owner and alive: the Sunburn marks cleared, `RPC_AddStatus(solarCrown 921, jaLv 6, jaLv + 10 = 16 s)` (TTO1106: `chaAdjust(6)` s), `mSunActive` | the hero | :20699-20748 |
| 0.9 | -> the status look **solarCrown** (section 1), with `SunCrownFx` | the hero | CharacterControl.c:17181-17345 |
| 1.3 | Waits 0.4: EndRow6Action (standby) = the clip's 1.3 s | | :20754, :20837 |

`mPhoenixArmor` (+0x528, `dump.cs:111768`) plays its own `nAttack` clip (:20658-20670): only in Fire Avatar, left out.

**The crown, `SunCrownFx::LateUpdate@0x1D6DED0`** (never decompiled; `suncrown_late.asm`, the calls named through
`methods.tsv`): each frame `halo.position = holder.position + up x (HeadHeight + 0.35) - holder.forward x 0.25`
(0x1D6DFC6-0x1D6E07F: **1.70 up, 0.25 behind**), `halo.rotation = holder.rotation` (0x1D6E0B4); `ring` (null in this
prefab) `localRotation = Euler(0, 0, t x ringSpeed)`; `orbit.localPosition = (orbitRadius cos a, 0.25 sin 2a,
orbitRadius sin a)`, a = Time.time x orbitSpeed x Deg2Rad (0x1D6E16B-0x1D6E1E4), orbitRadius **0.75**, orbitSpeed
**140**, ringSpeed 40 (`probe.json`); then renderers switched by `hasStatus` x 3 (the holder's hiding statuses, not on
the page). The prefab: `Halo` (0, 1.95, -0.25 in the prefab, moved each frame) with Corona / Core / Ring ImageEmitters
and the flame Crown (Shuriken), `Sun` (the orbit) carrying a 0.26-scale Ja model and its own Corona / Core.

**The crown's end and the Solar Collapse.** The frame `solarCrown` is gone (time up, recast, removed),
`Monkey::SunAvatarTick` starts the collapse (Bible :914). The crown (16 s, or chaAdjust(6) = 15 s at CHA 100) is cut at
10 s (the rule), so it ends at 10.9 s. With the recast (question 1), TTO1106's `TryRecast@0x1CDE5C0` stores the selected
enemy (the 10 m target, flat 10 <= 30 m: `CollapseFoe@0x1CCCCE0`), and
`TTO1106:Monkey.<RPC_solarCollapse>d__369::MoveNext@0x1D1E000` (`1106 Monkey.c:1-428`):
- **sunAvatar_dive** at the Monkey + up x (HeadHeight + 0.6) = **1.95 up**, identity (:117-138);
- 0.5 s rising to that + **5 up** (6.95), k = clamp01(1 - (1 - 2t)^2) (:148-151, :380-400);
- the dive to `Landing` (`g__Landing|369_0@0x1CDE800`: the target's current position) + **0.5 up**, over **0.3 +
  0.015 x flat distance = 0.45 s**, k = clamp01(u^2) (:160-173, :340-370);
- the sun destroyed, **jaAscension_supernova** at the landing (the target's feet, 10 m ahead), identity (:197-210); the
  hits (r 6, no look), the marks cleared.
TTO1102 (`Monkey.<RPC_solarCollapse>d__363@0x1D15280`, Monkey.c:17382-17739) and a crown that runs out: the same from
the Monkey's head, the dive 0.3 s to the Monkey + 0.5 up, the supernova at the Monkey (:17441-17534, :17650-17718).

Timeline (solarCall-relative): 0 launch, comet, callFx, voice; 0.9 ignite, crown; 1.3 standby; **10.9** crown gone,
dive spawned; 11.4 the sun at 6.95 m; **11.85** supernova at 10 m (TTO1102: 11.7 at the Monkey); its life 1.8 + 0.7.

### 2.3 Buiten Hou Hou IV with Buiten Bastion (`buitenBastion`, 1.267 s; the passive of cell 453) - released

Coroutine `TTO1102:Monkey.<RPC_buitenBastion_cast>d__317::MoveNext@0x1CE4F60` (Monkey.c:418-604), in place of BB's
`RPC_buiten_cast` (Monkey.cs:33609-33990: cast3, castEffect_fire, the create; **the TTO one has no castEffect_fire**):

| t (s) | what | where | cite |
|---|---|---|---|
| 0 | attack, command `buiten`; `PlayAnimation(buitenBastion, 0.15)` Once; voice **buiten** (TTO's clip, P10) | | :471-486 |
| 0 | spot = SummonSpot(**2**) | 2 m ahead | :487-490 |
| 0.5 | **buitenBastion_slam** | position + **0.35** x forward, the hero's rotation | :494, :513-532 |
| 0.5 | **buitenBastion_rise** | the spot, the hero's rotation | :534-543 |
| 0.55 | owner: SendBoostedCreate(-354, spot, forward, 2) -> `RPC_buiten_create@0x1CC9440`: `elementals/buiten/Buiten4`, LookRotation(forward), **`Buiten.Bastion(2)`** | the spot | :550, :576-588; :38886-39250 |
| 1.25 | EndRow6Action (standby; the clip ends at 1.267) | | :593, :563-566 |

`TTO1102:Buiten::Bastion@0x1D273E0` (Buiten.c:1136-1265): level 4 + 2 = **6**, HP and max HP x 6 / 4 (Math.Ceiling, no
look), and from level 5 the statue's **localScale x 1.2** (:1205-1216) and **`elementals/buiten/effects/
buitenBastion_aura`** at it, identity, named `buitenBastionFx`, parented (world pose kept: the aura is not scaled with
the statue) (:1218-1253). The aura has no EffectControl (its Runes GroundHug repeats forever): it lives with the statue.
The statue's own look (its `create` clip, its `[buiten]` DEF aura every 4 s, `Buiten.<summon>d__19`, Buiten.c:194-469)
is BB's. Cut at 10 s: the unsummon (`Buiten.<unsummon>d__20@0x1D3BC20`, Buiten.c:470-619: the `unSummon` clip,
Destroy 1 s later) at 10.55, gone at 11.55. (TTO1109 changed `Buiten::summon` / `unsummon` by compiler noise only:
`patch_1109\semdiff_all.txt:2698-2712`, a constructor call swapped.)

### 2.4 Buiten Bastion, the active (`sanctumRaise`, 1.5 s; Earthen Offering, cell 453) - NOT released

For the record (no cue): `TTO1102:Monkey.<RPC_buitenOffering_cast>d__319::MoveNext@0x1CE54D0` (Monkey.c:624-983):
at 0 `buitenBastion_offering` at the Buiten, LookRotation(flat offset) (:789-841), `MonkeyBuitenOffering.Init`
(the statue hidden, the six plates to the recipient, `MonkeyBuitenOffering.<Run>d__30`, the Bible :932), the hero
turned to the statue, `PlayAnimation(sanctumRaise, 0.15)` Once, voice **buiten** (:929-968); Waits 0.7:
`buitenBastion_slam` at position + 0.35 forward (:686-712); Waits 0.8: standby at 1.5 (:716, :733). Its prefabs
(probed): `buitenBastion_offering` (32 nodes: an `Idol` with Animation clips root / create / destroy / unSummon by
name, an Animator FX_Magic_Circle, field-only `buitenBastion_awaken` / `_burst` / `_lock`), `bastionWard` (+ `_break`,
`_chip`, `_hit`; `BastionWardFx`). Parts it would need if released: MonkeyBuitenOffering (P-a), BastionWardFx (P-b),
the Idol's clips (P4). Mole decision 15's rule (not released: no cue); the local tile stays the plain clip (question 6).

### 2.5 Rune Golem (`golemCall`, 1.467 s; cell 454) - released

The bar (6 s x magAdjust; 0.1 s at the floor) ends in `RPC_runeGolem_cast` (RPC_cast, the `runeGolem` branch).
Coroutine `TTO1102:Monkey.<RPC_runeGolem_cast>d__320::MoveNext@0x1D132B0` (Monkey.c:16230-16405):

| t (s) | what | where | cite |
|---|---|---|---|
| 0 | attack, command `runeGolem`; `PlayAnimation(golemCall, 0.15)` Once; voice **summon** | | :16277-16292 |
| 0 | spot = SummonSpot(**4.5**); **runeGolem_circle** | the spot, the hero's rotation | :16293-16306 |
| 0.55 | **runeGolem_stomp**; voice **upheaval** | the hero, its rotation | :16310, :16330-16342 |
| 0.6 | owner: RPC_runeGolem_create(spot, forward) -> `Monkey::RPC_runeGolem_create@0x1CCF990`: `elementals/runeGolem/RuneGolem` at the spot, LookRotation(flat forward), its layer, TrackSummon type 7, `RuneGolem.Init` | the spot | :16351, :16376-16389; :43926-44195 (:44060-44091, :44179) |
| 1.45 | EndRow6Action (standby; the clip ends at 1.467) | | :16394, :16366 |

**The golem** (`RuneGolem`, `dump.cs:113918-114070`; pseudo_c6_extra RuneGolem.c; TTO1106 split Think into
`Engage@0x1D6F800` with the same numbers, `1106 RuneGolem.c:265-543`). Its effects load from
`GameAssets/characters/elementals/runeGolem/effects/` (`FxPath`), at the golem (its position, its rotation) unless said.
Golem time g from the create (tile time = 0.6 + g); `Init@0x1D6AAA0` (:1073-1182): mBorn = now, aura at 0.7, quake at
4, pound at 2.9 + 3 = 5.9, then `Rise`:
- **Rise** (`<Rise>d__83@0x1D7C000`, :667-972): attack / summon; `Once("summon")`; **runeGolem_rise**; mFlareUntil =
  g 2.9; the model (`Model` child) from -ModelHeight up over 0.7 s, y = -h (1 - u)^3 (:878-901); g **0.7**:
  model at 0, **runeGolem_riseBurst**, Shake 3, the rise hit (r 6, no look) (:903-958); g **2.05**: **runeGolem_roar** at
  TransformPoint(RoarAt3 = (0.12, 3.22, 0.52)) (:768-798); g **2.9**: standby (the AI starts) (:804-860).
- **Aura** (`Update@0x1D6D170` :1299-1385, `Aura@0x1D69950` :3118-3224): from g 0.7 every **1.5 s** (to the cut: 0.7,
  2.2 ... 9.7): **runeGolem_auraPulse** at the golem, and every player of its side within r 8 h 4 (the Monkey, 4.5 m)
  gets Stone Aegis (918) for 3 s: the status look **stoneAegis** on the hero (section 1; kept while renewed: one FX from
  g 0.7 to 3 s after the last pulse, g 12.7).
- **AI** (`Think@0x1D6CA90`, :1388-1612; called each frame when not busy and not ending): the 10 m target is 5.5 m from
  the golem (PickTarget: within 14 m). In order: **quake** when now >= mNextQuake and a foe within 7 m (findEnemies 7):
  mNextQuake = now + 12, Face, `Quake`; else if the target is farther than 3.4 + its collider's min(x, z) extent (0.3:
  **3.7 m**) **walk** toward it (`MoveToward@0x1D6B030` :1755-1925: the `run` clip looped, **4 m/s**, turning 360 deg/s;
  `Footfall@0x1D6A590` :1926-2010: a 1.2 s cycle, **runeGolem_step** at TransformPoint(StepL (-0.99, 0, 0.22) / StepR
  (0.99, 0, 0.22)) at phases 0 and 0.5 (`Step` :2011-2056)); else **pound** when now >= mNextPound (mNextPound = now + 7,
  mNextFist = max(mNextFist, now + 1.35), step 2); else **fist** when now >= mNextFist (mFistSide toggles 0 / 1,
  mNextFist = now + 1.6), else idle facing the target.
- **Fist / Pound** (`<Fist>d__84@0x1D6EF50`, :130-442; `.cctor@0x1D6D760` :3914-3974: FistHitAt [0.42, 0.42, 0.62],
  FistLength [1.0, 1.0, 1.35]): `Once("attack<step + 1>")`; at its hit time **runeGolem_fistHit** at
  TransformPoint(FistHitR (0.88, 1.63, 3.11) on step 0 / FistHitL (-0.87, 1.61, 3.11) on step 1), the golem's rotation;
  step 2 (attack3): **runeGolem_pound** at TransformPoint(PoundAt (0, 0, 2.05)) + Shake 2; done at the length.
- **Quake** (`<Quake>d__85@0x1D70C70`, :445-585): `Once("quake", 0.15)`, mFlareUntil = now + 1.6, **runeGolem_quakeCharge**
  at the golem; at 0.78 **runeGolem_quake** at TransformPoint(QuakeAt (0, 0, 2.02)) + Shake 4 (Rune Fracture on the
  foe: a status on the foe, no look, Sheep decision 4); done at 1.6.
- **Glow** (`LateUpdate@0x1D6ACF0`, :1203-1280): the body's `_TintColor` = GlowColor (1, 0.55, 0.25, 1) x 0.85 while
  flaring (now < mFlareUntil), else about 0.28 + 0.1 sin(2.4 t) (the constants 0.85, 2.4, 0.1, 0.28, 0.6 at :1239-1246;
  the exact sum is for the part to read).
- **End**: no time limit in the game; cut at 10 s = `unsummon` -> `Crumble(false)` (:3894-3913, :2656-2709) ->
  `<CrumbleAway>d__87@0x1D6EBD0` (:1-128): `Once("collapse", 0.15)`, **runeGolem_crumble**; at 0.9 **runeGolem_dust** and
  the model sinks y = -h ((t - 0.9) / 1.5)^2 to 2.4; Destroy at 2.4.

Projected golem timeline (the part runs the code; these are what it should produce on the page's target): g 0 summon
and rise; 0.7 burst, first aura; 2.05 roar; 2.9 walk 1.8 m (0.45 s, steps at 2.9 / 3.5 ...); ~3.35 fist 0, hit 3.77;
4.35 quake (charge), hit 5.13; 5.95 pound, hit 6.57; 7.3 fist 1, hit 7.72; 8.9 fist 0, hit 9.32; **10.0 crumble**
(dust 10.9, gone 12.4 = tile 13.0).

## 3. What is left out (only the camera / "on an enemy" / "needs a hit" / another form)

- Every ShakeNear / Shake (the player's screen).
- Sun Avatar: Solar Echo's flares, Sunburn marks and Sunbursts (they need fire-skill hits during the crown: no fire skill
  in this tile); the Fire Avatar armour's nAttack clip (only in that form); the cooldown x 0.7 (no look).
- Rune Golem: its hits' damage, Rune Fracture on the target (status on a foe, Sheep decision 4).
- The boosted Ja's / Buiten's `[ja]` / `[buiten]` statuses on the Monkey (BB looks: the BB summon part's).
- Earthen Offering (`sanctumRaise`): not released.

## 4. Sounds and voices

| t (s, in the cue's key) | kind | name | where | file |
|---|---|---|---|---|
| jaAscension 0 | voice | ja | Row6Voice (:10319) | BB `voices/ja.wav` |
| buitenBastion 0 | voice | **buiten** | Row6Voice (:486) | TTO only (BB's rip: `.meta` only): P10 |
| golemCall 0 / 0.55 | voice | summon / upheaval | Row6Voice (:16292, :16342) | BB `voices/` |
| solarCall 0 | voice | ja | Row6Voice (:20671) | BB |
| own | AudioSource | gaosFire_hit 1.0, explosion1 0.5 | jaAscension_supernova, runeGolem_riseBurst (and unreleased flare / sunburst) | `probe.json` sounds: BB rip WAVs by name |
| own | AudioSource | (castEffect_fire's own) | BB's prefab | BB |

## 5. Probed (office PC, TTO's 2026-11-09 bundles)

All in-scope prefabs export (`probe.err`: only names written by name: AnimationClips of the Ja / Idol / golem models,
the AnimatorController FX_Magic_Circle, `buitenBastion_offering`'s and `bastionWard`'s GameObject fields). Materials (78
over every probe): **Eric/URP Particles/Additive 44, Eric/URP Particles/Alpha Blended 2** (new), Particles/Standard
Unlit 15 (built, tto_sheep.js), add 6, premul 3, addsoft 3, alpha 1, multiply2 1, FlexibleCelShader/Cel No Outline 3
(built, tto_penguin.js: the Ja `tto_ja`, the golem `tto_runeGolem` / `_glow`).

| prefab | root (life + after) | parts | needs |
|---|---|---|---|
| jaAscension_pillar | EffectControl 1.8 + 0.6 | Pillar: 9 Shuriken (Eric Additive / Alpha Blended), Runes GroundHug (runeCircle 0.4 -> 1.6), Embers Shuriken | P2 |
| jaAscension_launch | 1.2 + 0.5 | Flash ImageEmitter 0.9 up, Shock GroundHug ring 0.3 -> 2.6, Runes GroundHug, Embers | - |
| jaAscension_callFx | 1.3 + 0.5 | Sigil (Shuriken + **Animator FX_Magic_Circle**, 0.45) with 4 Shuriken, Motes | P3 |
| sunAvatar_comet | 1.6 + 0.5 (the code destroys it at 0.9) | **Ja** model (SkinnedMesh Ja_tri 526 v, tto_ja cel, Animation `root` by name), Core / Corona ImageEmitters, Wake Shuriken (Flame1_h addsoft) | P4, P5 |
| sunAvatar_ignite | 0.9 + 0.5 | Flash 1.8 up, Shock ring 0.3 -> 3.6, Runes, Embers | - |
| solarCrown | none (the status) | `SunCrownFx` (halo, orbit, 0.75, 140, 40); Halo: Corona / Core / Ring ImageEmitters, Crown Shuriken; Sun: a 0.26 Ja model + Corona / Core | P4, P6 |
| sunAvatar_dive | 1.4 + 0.5 (the code destroys it at 0.8 / 0.95) | Core / Corona / Ring ImageEmitters, Wake Shuriken | P7 |
| jaAscension_supernova | 1.8 + 0.7 | Core: BB-style ParticleEmitter + LineEmitter + RingEmitter (FireRay2, Bomb2, FireRing4) and 2 AudioSources; WhiteOut 1.8 up; Shock ring 0.8 -> 7.0; Sparks; Flames | - |
| buitenBastion_rise | 2.0 + 0.6 | Crystals (10 Shuriken incl. Collision, Sub, Lights (its Light disabled), CustomData), Beam (11 Shuriken, Eric), Runes GroundHug 0.5 -> 2.2, Dust | P2 |
| buitenBastion_slam | 1.0 + 0.5 | Beam (11 Shuriken, 0.7), Wave ring 0.2 -> 2.2, Dust | P2 |
| runeGolem_circle | 2.4 + 0.6 | Sigil (Animator FX_Magic_Circle, 1.8) + 4 Shuriken, Runes 0.4 -> 3.4, Cracks (delay 0.5) 2.6 -> 3.6 | P2, P3 |
| runeGolem_stomp | 0.8 + 0.4 | Beam (0.5) 11 Shuriken, Wave ring 0.2 -> 1.6, Dust | P2 |
| jaAscension_aura (ja/effects) | none (parented to the Ja) | Crown Shuriken 1.15 up, Corona 0.8 up, Embers, Sigil (Animator) | P1, P3 |
| buitenBastion_aura (buiten/effects) | none (parented) | Circle 6 Shuriken (Eric), Runes GroundHug repeatForever 2.0, Motes (runeTeal) | P1, P2 |
| RuneGolem (runegolem/) | Animation (root, run, attack1-3, summon, quake, collapse by name), CharacterController | golem_mnk SkinnedMesh (2487 v; tto_runeGolem + tto_runeGolem_glow, cel), 22 bones (Model child) | P1, P9 |
| runeGolem_rise / riseBurst / roar / auraPulse / step / dust / fistHit / pound / quakeCharge / quake / crumble, stoneAegis (runegolem/effects) | EffectControl 2.2 / 1.4 / 1.0 / 1.3 / 0.8 / 1.0 / 0.9 / 1.4 / 0.9 / 2.6 / 2.0; stoneAegis none (the status) | Shuriken, GroundHug, ImageEmitters (`probe_golem.txt`) | P1, P2, P9 |
| castEffect_fire (BB) | ImageEmitter 0.4, EffectControl, AudioSource | ready (BB parts) | - |

**FX_Magic_Circle** (`animator.py`): the controller's one clip (2.0 s, not legacy) animates the Sigil's
ParticleSystemRenderer material vector `_MainTex_ST` (binding typeID 199, customType 22; the attribute hash's low 28
bits = CRC32("_MainTex_ST"), its top 4 bits the component): x, y, z constant (1, 1, 0), **w (the V offset) 0 -> -1 over
2 s** (a streamed curve, keys at 0 and 2): the sigil's texture scrolls one repeat in 2 s.

## 6. Parts the page lacks (effect: part)

Home: a new `wardrobe/fxparts/tto_monkey.js` (P2-P7, P9) and the exporter (P1, P3, P4, P10). Every part is cued anyway.

| # | Part | Effects | What it does (source) |
|---|---|---|---|
| P1 | Exporter: the summons' folders (`wardrobe_fx_tto.py`, a TTO_EXTRA_FOLDERS beside `Tto`'s `heroes/<cls>/effects/` base) + `SKILL_FX["monkey"]` | jaAscension_aura, buitenBastion_aura, RuneGolem and its 12 effects | `gameassets/characters/elementals/ja/effects`, `.../buiten/effects`, `.../runegolem/effects`, `.../runegolem` (`probe_elem.py` is the shape); SKILL_FX: the 12 heroes/monkey prefabs of section 5 + those. |
| P2 | Shaders `Eric/URP Particles/Additive` and `Alpha Blended` (46 materials) | most Shuriken here | Additive: tex x _TintColor x vertex colour x `_Emission` (1-3), blend per `_SrcBlend` / `_DstBlend` when set (5/1 additive, 1/0 opaque-ish with ZWrite, 5/10 alpha), else additive; Alpha Blended: alpha x `_Opacity`, `_Emission` 4; `_SpeedMainTexUVNoiseZW` UV scroll (Trail_01_1: v -0.8/s); `_Usedepth`, `_Usecenterglow`, `_Usecustomrandom` are 0 in every material (no soft particles, no custom data needed). APPROX: the shader source is not in the bundles. |
| P3 | Animator + AnimatorController (FX_Magic_Circle) | jaAscension_callFx, runeGolem_circle, jaAscension_aura (and buitenBastion_offering) | The exporter writes the controller's clip (today: by name only); the page scrolls the Sigil renderer's `_MainTex_ST.w` 0 -> -1 over 2 s, looping (section 5). |
| P4 | An effect's own Animation clips (TTO; the Mole's P7) | sunAvatar_comet, solarCrown (the Ja model, clip `root`) | The Ja's `root` from TTO's dependency bundle (or BB's Ja rig, the same bones root / body / head / hip / legs). |
| P5 | `Monkey.SunComet` (code mover on sunAvatar_comet) | sunAvatar_comet | From the cue's spot, the quadratic Bezier over mid + up x `rise` to `to`, s = (3 - 2u) u^2 over 0.9 s (u = age / 0.9), the end re-read each frame (the hero's head) (Monkey.c:20760-20821). |
| P6 | `SunCrownFx` | solarCrown | halo at the hero + up x (`head` + 0.35) - forward x 0.25 with the hero's rotation; orbit (0.75 cos a, 0.25 sin 2a, 0.75 sin a), a = 140 deg/s x the clock; ring Euler(0, 0, 40 t) (none here) (`suncrown_late.asm`). |
| P7 | `Monkey.SolarCollapse` (code mover on sunAvatar_dive) | sunAvatar_dive | From the spot up to `top` over 0.5 s (k = 1 - (1 - 2t)^2), then to `to` over `dive` s (k = u^2) (1106 Monkey.c:340-400). |
| P8 | The boosted summons (BB's Ja4 / Buiten4 summon part + TTO's boost) | Ja4, Buiten4 (+ jaAscension_aura, buitenBastion_aura) | Option `boost` 2: the Ja at level 6 (followDistance 5) with `tto/jaAscension_aura` parented at its root; the Buiten x 1.2 with `tto/buitenBastion_aura` parented (unscaled); option `standing` (Sun Avatar's): spawned already summoned in its idle (no summon clip, no ring), gone at `kill` with no unsummon (HideBody + SpendJa). `end`: the unsummon (Ja `ko`, Buiten `unSummon`, gone 1 s later). |
| P9 | `RuneGolem` (the summon, its clips, AI and glow) | RuneGolem + its 12 effects | Section 2.5: the model and its legacy clips from TTO's bundle (summon, root, run, attack1-3, quake, collapse); Rise; the aura pulses with `tto/stoneAegis` on the hero; Think / Fist / Quake / Footfall / MoveToward on `to` (the 10 m target, radius 0.3); the glow; at `end` CrumbleAway. Its spawns are `builds`. |
| P10 | TTO's hero voices (`voices/<name>` from TTO's bundle when BB's rip has no audio) | voice buiten | `tto_clips` reads `heroes/<cls>/sounds/` only: add `voices/` (-> `v_buiten.mp3`); BB's Buiten Hou Hou tile needs it too (BB's code loads the missing file). |
| P11 | Page lines (shared changes S1-S3, section 7) | the four tiles | SEQ lines, CLIP_SKILLS icons. |

## 7. The cue entries (ready to paste into `wardrobe/fx_cues/monkey.json`)

`checks/fx_monkey_research/tto/cues_paste.json`: 6 keys, 22 cues, parsed. Options beyond the page's own: `boost`,
`standing`, `end` (P8, P9), `to`, `rise` (P5), `head` (P6), `top`, `dive` (P7): `fx.at`'s, passed through by cueOf.
`Ja4` / `Buiten4` are the BB summon part's names (question 2); until that part exists, those three cues would fail the
check's "named effect missing" (add them with it, or keep the block whole once the BB research's summon part lands).

```json
{
  "jaAscension": {
    "why": "Ja Hou Hou IV with Ja Ascension's passive (cell 452 learned, passives on): RPC_cast's release swaps RPC_ja_cast for RPC_jaAscension_cast when hasSkill(0x1c4 = 452) (TTO1102:Monkey.<RPC_cast>d__178::MoveNext@0x1CE8830, pseudo/Monkey.c:3260-3300). TTO1102:Monkey.<RPC_jaAscension_cast>d__315::MoveNext@0x1D084F0 (Monkey.c:10252-10460): at 0 attack / command ja, PlayAnimation(jaAscension, 0.15) Once (:10316-10318), Row6Voice('ja') (:10319; Monkey::Row6Voice@0x1CD3510 :43213-43288: voices/ja, volume 1 for the owner), spot = SummonSpot(2) = the ground 2 m ahead (:10320; Monkey::SummonSpot@0x1CD52D0 :43385-43446); Waits 0.25 (:10327): castEffect_fire (the hero prefab's field +0x2a0, dump.cs:111686; BB's heroes/monkey/effects/castEffect_fire, the same Instantiate as BB's RPC_ja_cast Monkey.cs:29044) at position + TransformDirection(0, 1, 1), the hero's rotation (:10347-10370); Waits 0.2 (:10374): PlayRow6Fx jaAscension_pillar at the spot, identity (:10395-10399; Monkey::PlayRow6Fx@0x1CC8EC0 :43130-43210, a bare Instantiate from heroes/monkey/effects/), ShakeNear(spot, 1) (the camera: left out); Waits 0.05 (:10406): SendBoostedCreate(-250 - sLv, spot, forward, boost 2) (:10434) -> RPC_ja_create@0x1CCD070: GameAssets/characters/elementals/ja/Ja4 at the spot, LookRotation(forward), then Ja.Ascend(mSummonBoost 2) (:37216-37530, the boost read at :37518-37528): TTO1102:Ja::Ascend@0x1D3D0B0 (pseudo_c6_extra/monkey/Ja.c:2728-2819) level min(4 + 2, 6) = 6, followDistance 0.5 x 6 + 2 = 5, and from level 5 elementals/ja/effects/jaAscension_aura at the Ja, its rotation, named jaAscensionFx, parented (worldPositionStays) (:2768-2805; part P8, builds); Waits 0.65 (:10439): EndRow6Action standby at 1.15 (:10453). The summon cut at 10 s (the standing rule): its unsummon (Ja.<unsummon>d__26@0x1D4F890, Ja.c:791-910: the ko clip, Destroy 1 s later) at end 10",
    "builds": ["tto/jaAscension_aura"],
    "cues": [
    [0, "voice", "ja"],
    [0.25, "fx", "castEffect_fire", {"y": 1, "d": 1}],
    [0.45, "fx", "tto/jaAscension_pillar", 2],
    [0.5, "fx", "Ja4", {"d": 2, "boost": 2, "end": 10}]
    ]
  },
  "buitenBastion": {
    "why": "Buiten Hou Hou IV with Buiten Bastion's passive (cell 453 learned, passives on): RPC_cast's release swaps RPC_buiten_cast for RPC_buitenBastion_cast when 453 is learned (TTO1102:Monkey.<RPC_cast>d__178::MoveNext@0x1CE8830, Monkey.c:3660-3700). TTO1102:Monkey.<RPC_buitenBastion_cast>d__317::MoveNext@0x1CE4F60 (Monkey.c:418-604): at 0 attack / command buiten, PlayAnimation(buitenBastion, 0.15) Once (:483-485), Row6Voice('buiten') (:486: voices/buiten; BB's rip has only buiten.wav.meta, no audio: TTO's clip, 0.767 s, part P10), spot = SummonSpot(2) (:487); Waits 0.5 (:494): PlayRow6Fx buitenBastion_slam at position + 0.35 x forward, the hero's rotation (:515-532) and buitenBastion_rise at the spot, the hero's rotation (:534-543), ShakeNear(spot, 2) (the camera: left out); Waits 0.05 (:550): SendBoostedCreate(-350 - sLv, spot, forward, boost 2) (:588) -> RPC_buiten_create@0x1CC9440: elementals/buiten/Buiten4 at the spot, LookRotation(forward), then Buiten.Bastion(2) (:38886-39250, :39194-39204): TTO1102:Buiten::Bastion@0x1D273E0 (Buiten.c:1136-1265) level min(4 + 2, 6) = 6, HP x 6 / 4, and from level 5 the statue's localScale x 1.2 and elementals/buiten/effects/buitenBastion_aura at it, identity, named buitenBastionFx, parented (worldPositionStays) (:1205-1253; part P8, builds); Waits 0.7 (:593): EndRow6Action standby at 1.25 (:566). The summon cut at 10 s: its unsummon (Buiten.<unsummon>d__20@0x1D3BC20, Buiten.c:470-619: the unSummon clip, Destroy 1 s later) at end 10",
    "builds": ["tto/buitenBastion_aura"],
    "cues": [
    [0, "voice", "buiten"],
    [0.5, "fx", "tto/buitenBastion_slam", 0.35],
    [0.5, "fx", "tto/buitenBastion_rise", 2],
    [0.55, "fx", "Buiten4", {"d": 2, "boost": 2, "end": 10}]
    ]
  },
  "golemCall": {
    "why": "Rune Golem (cell 454): the bar's release starts TTO1102:Monkey.<RPC_runeGolem_cast>d__320::MoveNext@0x1D132B0 (Monkey.c:16230-16405): at 0 attack / command runeGolem, PlayAnimation(golemCall, 0.15) Once (:16289-16291), Row6Voice('summon') (:16292), spot = SummonSpot(4.5) (:16293), PlayRow6Fx runeGolem_circle at the spot, the hero's rotation (:16298-16306); Waits 0.55 (:16310): runeGolem_stomp at the hero, its rotation (:16330-16341), Row6Voice('upheaval') (:16342), ShakeNear (camera: left out); Waits 0.05 (:16351): the owner sends RPC_runeGolem_create(spot, forward) (:16376-16389) -> Monkey::RPC_runeGolem_create@0x1CCF990 (:43926-44195): elementals/runeGolem/RuneGolem at the spot, LookRotation(flat forward) (:44060-44091), RuneGolem.Init (:44179; RuneGolem::Init@0x1D6AAA0, pseudo_c6_extra/monkey/RuneGolem.c:1073-1182: aura from 0.7 s, quake from 4 s, pound from 5.9 s, the Rise coroutine) -- the golem's own clock is part P9 (rise, roar, AI on the 10 m target, aura pulses with Stone Aegis on the hero, its glow, the crumble at end); Waits 0.85 (:16394): EndRow6Action standby at 1.45 (:16366). No time limit in the game: cut at 10 s (end 10: Crumble, RuneGolem.c:2656-2710, CrumbleAway :1-128)",
    "builds": ["tto/runeGolem_rise", "tto/runeGolem_riseBurst", "tto/runeGolem_roar", "tto/runeGolem_auraPulse", "tto/stoneAegis", "tto/runeGolem_step", "tto/runeGolem_fistHit", "tto/runeGolem_pound", "tto/runeGolem_quakeCharge", "tto/runeGolem_quake", "tto/runeGolem_crumble", "tto/runeGolem_dust"],
    "cues": [
    [0, "voice", "summon"],
    [0, "fx", "tto/runeGolem_circle", 4.5],
    [0.55, "fx", "tto/runeGolem_stomp"],
    [0.55, "voice", "upheaval"],
    [0.6, "fx", "tto/RuneGolem", {"d": 4.5, "end": 10, "to": [0, 0, 10]}]
    ]
  },
  "@SunAvatar:cast1": {
    "why": "Ja Ascension's active (Sun Avatar, cell 452) needs a living Ja of the Monkey within 30 m, the highest level first (TTO1102:Monkey::PickJa@0x1CC8AD0 via ::ReleaseSunAvatar@0x1CD2840, Monkey.c:44330-44415): the tile shows the boosted Ja (level 6, the passive's, with its jaAscension_aura) already standing at its summon spot 2 m ahead (SummonSpot(2) of the jaAscension tile; a level-6 Ja's followDistance 5 keeps it there), from the tile's start; at the bar's end the coroutine hides it (Monkey::HideBody@0x1CC6F90 :20550) and SpendJa kills it (:44401): kill 0.8 = cast1 (0.7 s) + the 0.1 s bar. MERGE: this key replaces the plain cast1 entry for this sequence, so the BB research's cast1 cues (the cast voice, castRing ...) go in here too",
    "builds": ["tto/jaAscension_aura"],
    "cues": [
    [0, "fx", "Ja4", {"d": 2, "boost": 2, "standing": true, "kill": 0.8}]
    ]
  },
  "solarCall": {
    "why": "Sun Avatar's release: Monkey::ReleaseSunAvatar@0x1CD2840 (Monkey.c:44330-44415) starts TTO1102:Monkey.<RPC_sunAvatar_cast>d__352::MoveNext@0x1D20100 (Monkey.c:20405-20846; TTO1106 d__357@0x1D28970 has the same times, only the crown's length changed to chaAdjust(6)) with from = the Ja's position and offset = Monkey - Ja: at 0 jaLv = the Ja's level (6) (:20532-20534), Ja hidden (:20550); PlayRow6Fx jaAscension_launch at the Ja, identity (:20566), ShakeNear (camera: left out); start = Ja + 1.2 up (:20576-20582); sunAvatar_comet there, identity (:20596); posing (attack + cast): command sunAvatar, the hero turned to face the Ja (flat; straight ahead: no turn, :20625-20654), PlayAnimation(solarCall, 0.15) Once (:20655-20657), Row6Voice('ja') (:20671), jaAscension_callFx at the hero, its rotation (:20687); rise = 0.12 x |flat offset| + 4 = 4.24 (:20690-20697); every frame to 0.9 s (:20699-20701) the comet on the quadratic Bezier (Monkey::Bezier@0x1CC2D50 :44450-44475) from start over (mid(start, end) + rise up) to end = the hero + up x (HeadHeight + 0.6) (= 1.95: the Monkey's CharacterController top 0.7 + 1.3 / 2, CharacterControl::HeadHeight@0x24B4A00 CharacterControl.c:17371ff), s = (3 - 2u) u^2, u = t / 0.9 (:20772-20821; part P5); at 0.9 the comet destroyed (:20712), sunAvatar_ignite at the hero, its rotation (:20729), ShakeNear 3 (left out), RPC_AddStatus(solarCrown 0x399, jaLv, jaLv + 10) (:20744-20747) -> CharacterControl::AddMonkeyRow6Fx@0x24AD6A0 (CharacterControl.c:17181-17345): heroes/monkey/effects/solarCrown at the hero, identity, parented, scale clamp(2 x 0.2 x 1, 1, 4) = 1, SunCrownFx.Bind (part P6: the halo at the head + 0.35 up, 0.25 behind, the orbiting sun); the 16 s crown (TTO1106: chaAdjust(6)) cut at 10 s: kill 10 (its end starts the collapse: @SunAvatar:root); Waits 0.4 (:20754): EndRow6Action standby at 1.3 (:20837), the clip's length. The Fire Avatar armour's nAttack clip (mPhoenixArmor +0x528, :20658-20670) plays only in Fire Avatar: left out",
    "cues": [
    [0, "fx", "tto/jaAscension_launch", 2],
    [0, "fx", "tto/sunAvatar_comet", {"y": 1.2, "d": 2, "to": [0, 1.95, 0], "rise": 4.24, "kill": 0.9}],
    [0, "voice", "ja"],
    [0, "fx", "tto/jaAscension_callFx"],
    [0.9, "fx", "tto/sunAvatar_ignite"],
    [0.9, "fx", "tto/solarCrown", {"head": 1.35, "kill": 10}]
    ]
  },
  "@SunAvatar:root": {
    "why": "The crown's end (the 10 s cut at solarCall 10.9 s = this step's 9.6 s; root starts at solarCall's 1.3 s end) is the recast's (TTO1106:Monkey::TryRecast@0x1CDE5C0 with the enemy selected: the 10 m target, flat 10 <= 30 m) -> Monkey::SunAvatarTick@0x1CDE140 -> TTO1106:Monkey.<RPC_solarCollapse>d__369::MoveNext@0x1D1E000 (DecompiledSource_TTO_2026-11-06/research/patch_1106/pseudo/Monkey.c:1-428): sunAvatar_dive at the Monkey + up x (HeadHeight + 0.6) = 1.95, identity (:117-138); 0.5 s rising to + 5 up (k = 1 - (1 - 2t)^2, :148-151, :340-400); then the dive to Landing (the target's position, g__Landing|369_0@0x1CDE800) + 0.5 up over 0.3 + 0.015 x flat distance = 0.45 s (k = u^2, :160-173, :340-370; part P7); then the sun destroyed, jaAscension_supernova at the landing, identity (:197-210), ShakeNear 5 (left out), the hits (no look). TTO1102's (and a crown that runs out): at the Monkey, dive 0.3 s (Monkey.c:17382-17739): question 1",
    "cues": [
    [9.6, "fx", "tto/sunAvatar_dive", {"y": 1.95, "top": 6.95, "to": [0, 0.5, 10], "dive": 0.45, "kill": 0.95}],
    [10.55, "fx", "tto/jaAscension_supernova", 10]
    ]
  }
}
```

**Shared change S1 (`index.html` SEQ, monkey; appended to the Monkey's line):**

```
"Ascended Ja: cast1 cast2*~@0.1 jaAscension~0.15 root*~@10.4",
"Sun Avatar: cast1 cast2*~@0.1 solarCall~0.15 root*~@13.1",
"Bastion Buiten: cast1 cast2*~@0.1 buitenBastion~0.15 root*~@10.3",
"Rune Golem: cast1 cast2*~@0.1 golemCall~0.15 root*~@11.9"
```

Holds: Ja created at jaAscension 0.5, unsummoned at 10.5, gone 11.5 -> root from 1.133 for 10.4; Sun Avatar: the
supernova at root 10.55 + its 2.5 s -> 13.1 (TTO1102's at the Monkey: 10.4 + 2.5 -> 12.9); Buiten: 0.55 + 10 + 1 =
11.55 - 1.267 -> 10.3; Rune Golem: Stone Aegis to tile 13.3 (golem gone 13.0) - 1.467 -> 11.9. The SEQ names are
working names: the tiles show their icons (S2) and Thai names from the page's own table.

**S2 (`pipeline/wardrobe_skill_icons.py` CLIP_SKILLS):** `"monkey": {"jaAscension": ["ja", "jaAscension"],
"buitenBastion": ["buiten", "buitenBastion"], "solarCall": ["jaAscension"], "golemCall": ["runeGolem"],
"sanctumRaise": ["buitenBastion"]}` (the Bible's `monkey_ja4`, `monkey_buiten4`, `monkey_jaAscension5`,
`monkey_buitenBastion5`, `monkey_runeGolem5`; today solarCall, golemCall and sanctumRaise have no icon,
`wardrobe/data/icons/hd/index.json`).

**S3 (`index.html` SEQ_SKILL, optional):** `"@SunAvatar": "jaAscension", "@RuneGolem": "runeGolem"` if the cast
clips' Cast icons would otherwise join the tile (the Sheep's Gleaming Breath sequence shows that they do not; the two
boosted-summon tiles keep CLIP_SKILLS' two icons, which SEQ_SKILL's one skill would hide).

## 8. Open questions (each with my recommended answer)

1. **Sun Avatar's end at the 10 s cut: where does the sun fall?** Recommend **on the 10 m target** (TTO1106+'s recast with
   the enemy selected, the bundles' build; the cut stands for the recast, Mole Q1; every other skill takes the 10 m
   target as the selected enemy): dive 0.45 s, the supernova 10 m ahead (block as written). B: at the Monkey (TTO1102,
   or a crown that runs out): `@SunAvatar:root` becomes `[9.6, "fx", "tto/sunAvatar_dive", {"y": 1.95, "top": 6.95,
   "to": [0, 0.5, 0], "dive": 0.3, "kill": 0.8}]`, `[10.4, "fx", "tto/jaAscension_supernova"]`, hold `root*~@12.9`.
2. **The boosted summons' names and the BB summon part.** Recommend: the BB research's Ja / Buiten summon part (BB's
   `elementals/ja/Ja4`, `elementals/buiten/Buiten4`, EXTRA_FOLDERS as the Mole's robots) with P8's `boost` / `standing`
   on top; the cue names follow that part (`Ja4` / `Buiten4` here).
3. **Separate tiles for the boosted summons?** Recommend **yes** (the Mole's missilePad beside BB's missile): BB's Ja /
   Buiten tiles stay BB's; "Ascended Ja" and "Bastion Buiten" show the passive's look, with both icons (S2).
4. **The pre-placed Ja for Sun Avatar** (the skill fizzles without one): recommend the boosted level-6 Ja standing 2 m
   ahead (its jaAscension spot) from the tile's start, hidden at the bar's end (Mole decision 37's King Kaiser).
5. **The cast bar**: recommend 0.1 s (magAdjust's floor, Mole decision 6) for all four; the page's Monkey Cast line uses
   `@0`: whichever the BB research settles for the Monkey's casts, these four follow.
6. **`sanctumRaise`** (not released): recommend **no cue, no sequence, no part**; its plain clip tile stays local only
   (the publish already drops it). If the user releases it later, P-a / P-b (section 2.4) and P3 / P4 apply.
7. **The Rune Golem's AI**: recommend **run as the code** on the 10 m target (Bat decision 24, Mole decision 32): walk,
   fist, quake, pound, the aura with Stone Aegis on the hero; its hits as projected in 2.5 come from the part, not cues.
8. **The golem's 10 s**: no time limit in the game; recommend the rule's cut with its own `unsummon` (the crumble),
   as Bat decision 25.

## 9. For the Bible (offer to the user; that repo's own rules)

- **Sun Avatar's look:** the Ja leaves its spot as a comet that rises 4 + 0.12 x the Ja's distance m above the midpoint
  and lands on the Monkey's head in 0.9 s; the crown's sun circles 0.75 m round a halo 0.35 m above the head (140 deg/s).
  The collapse sun rises 5 m in 0.5 s before diving.
- **Boosted summons:** the Ja appears 0.5 s after the bar 2 m ahead, the Buiten 0.55 s (the Bible has these), and the
  TTO release drops BB's cast3 / castEffect_fire for the Buiten (the Ja keeps castEffect_fire, at 0.25 s).
- **Rune Golem:** rises out of the ground in 0.7 s, roars at 2.05 s, walks at 4 m/s; a quake is tried before a fist or a
  pound; the first quake comes once the golem has finished its first fist (4.35 s after the summon on a target 10 m from
  the Monkey), the first pound right after it (5.95 s); it crumbles over 2.4 s.
- **Buiten Hou Hou's voice:** BB's data has no `voices/buiten` audio (only its .meta); TTO ships the file.

## Verification (the researcher's own checks)

- Every wait is a labelled DAT constant in the pseudo-C (0.15 fades; 0.25 / 0.2 / 0.05 / 0.65; 0.5 / 0.05 / 0.7;
  0.55 / 0.05 / 0.85; 0.9 / 0.4; 0.7 / 0.8 (sanctumRaise); the collapse 0.5 / 0.3 / 0.015; the golem's 0.7 / 2.05 /
  2.9 / 1.5 / 1.6 / 7 / 12 / 0.78 / 0.9 / 1.5 / 2.4; FistHitAt / FistLength from the InitializeArray labels; the vectors
  decoded from the .cctor's hex).
- SunCrownFx's LateUpdate read from the instructions (`suncrown_late.asm`; cos / sin as Unity's Mathf thunks at
  0x180308640 / 0x180308bd0, the order x = cos, z = sin assumed from their use: medium sure).
- `cues_paste.json` parses (22 cues); every `tto/` name is in a probe (`probe.json`, `probe_ja.json`, `probe_buiten.json`,
  `probe_golem.json`, `probe_golembody.json`); castEffect_fire probes in BB's rip; the voices ja / summon / upheaval are
  BB rip WAVs, buiten TTO's only.
- 1106 / 1109: the method diffs list `RPC_sunAvatar_cast`, `RPC_solarCollapse`, `SunAvatarTick`, `TryRecast`,
  `RuneGolem::Think` (1106) and `Buiten::summon` / `unsummon` (1109, noise); the coroutines of jaAscension,
  buitenBastion, runeGolem_cast and RuneGolem's Rise / Fist / Quake are unchanged (not in either list).
- Not done: a browser check (read-only researcher); the golem's projected timeline is mine (P9 decides); HeadHeight 1.35
  assumes the Monkey at scale 1.

## Verification (2026-11-13, checker)

Read-only re-derivation on the office PC from the sources (TTO1102 `pseudo/Monkey.c`, TTO1106 `patch_1106/pseudo/Monkey.c`,
BB `DecompiledSource/*.cs`, the Bible's `monkey-skill-reference.md` :892-969, BB's rip, TTO's 2026-11-09 bundles through
the tool's own exporter). Probes in `checks/fx_monkey_research/verify/` (git-ignored): `catalog_check.py` -> `catalog.txt`
(every TTO address under `heroes/monkey/` and `elementals/ja|buiten|runegolem`), `probe_v.py` -> `probe_v.json` (all 28
in-scope prefabs through `wardrobe_fx_tto.effect()` with the catalog base swapped), `clips_v.py`, `golem_audio.py`,
`mats_v.py`, `mats_v2.py` -> `mats_v2.txt`, `shader_v.py`. This section wins over the body.

**Confirmed** (no change): every wait of the four coroutines (jaAscension 0.25 / 0.2 / 0.05 / 0.65 = 1.15; buitenBastion
0.5 / 0.05 / 0.7 = 1.25; golemCall 0.55 / 0.05 / 0.85 = 1.45; solarCall 0.9 / 0.4 = 1.3; every clip opened with
`PlayAnimation(clip, 0.15)`, the 0.15 at `DAT_183004e94`) and the strings they use (Monkey.c:10252-10460, :418-604,
:16230-16405, :20405-20846: Row6Voice `ja`, `buiten`, `summon` then `upheaval`, the PlayRow6Fx names, SummonSpot 2 / 2 /
4.5, SendBoostedCreate -0xfa - sLv / -0x15e - sLv, the slam at 0.35 forward); `RPC_ja_create` loads `.../ja/Ja4` then
calls `Ascend` with `mSummonBoost` (:37216-37530); castEffect_fire is the hero's field +0x2a0 (Monkey.c:10347) and neither
the Buiten nor the Golem coroutine instantiates anything else (no `Instantiate` in :418-604, :16230-16405); the clip
lengths (`wardrobe/data/monkey/clips.json`: jaAscension 1.1333, solarCall 1.3, buitenBastion 1.2667, sanctumRaise 1.5,
golemCall 1.4667, all `tto: true`); the released list (`wardrobe/tto_released.json` monkey clips: buitenBastion, clap,
golemCall, jaAscension, solarCall, wai: sanctumRaise not); every effect name exists (`catalog.txt`: the 12
`heroes/monkey/effects` prefabs, `elementals/ja/effects/jaascension_aura`, `elementals/buiten/effects/buitenbastion_aura`,
the 13 `elementals/runegolem/effects/*` and `elementals/runegolem/runegolem`; castEffect_fire in BB's rip and TTO's); the
voices (BB rip `heroes/monkey/voices/`: ja.wav, summon.wav, upheaval.wav; buiten: `buiten.wav.meta` only; TTO's catalog
has `heroes/monkey/voices/buiten` and `voices/blazingarrow` only, so P10 reads the right file); the block is valid JSON
(6 keys, 22 cues) in the page's cue format (cueOf passes every option through as `fx.at`, index.html:4788-4797; `end`,
`to`, `kill` are existing options, :4692-4713); the S1 tokens parse with `SEQ_ALT` (index.html:1376); the holds'
arithmetic; the comet's peak (B(0.5).y = 0.25 x 1.2 + 0.5 x 5.815 + 0.25 x 1.95 = 3.695); the golem's projected timeline
(walk 5.5 - 3.7 = 1.8 m at 4 m/s = 0.45 s; fist 3.35 / hit 3.77; quake 4.35 / 5.13; pound 5.95 / 6.57; fists 7.3 / 7.72,
8.9 / 9.32); the 0.1 s bar (magAdjust = clamp(t - floor(n / 32), 0.1, 600): 1.5 s and 6 s both reach 0.1, Mechanics
reference :255-258; Mole decision 6).

1. **Question 1 decided B: the collapse falls on the Monkey (TTO1102's code).** What is wrong: the body recommends
   TTO1106's aimed recast. Every earlier class took **TTO1102's code** (Bat decision 44, Cat decision 42, Chameleon
   decision 44, Mole decision 57), and TTO1102 always drops the sun on the Monkey (Monkey.c:17382-17739: rise 0.5 s, dive
   0.3 s, `jaAscension_supernova` at the Monkey; the recast only ends the crown, Bible :914). The reason "the cut stands
   for the recast" does not save A either: in TTO1106+ the crown is `chaAdjust(6)` (Bible :900), which at the page's CHA 1
   (Chameleon decision 41) is floor(6 x 1.015) = **6 s**, under the 10 s cut, and a crown that runs out also lands on the
   Monkey (Bible :901). So the root step takes the body's option B: dive 0.3 s, kill 0.8, the supernova at the Monkey at
   root 10.4, hold 10.4 + 1.8 + 0.7 = **12.9**. The 1106+ aimed variant (the body's block, 13.1 s) is offered to the user,
   as Cat decision 42 offered TTO1109's.
2. **The tile's name shows on screen as written; "Sun Avatar" becomes "Ja Ascension".** What is wrong: S1's note says "the
   SEQ names are working names ... Thai names from the page's own table". The page has no such table for sequences: a
   tile's name is its SEQ name (`moveName = n => chainOf(n)?.name || label(n)`, index.html:1542; `chains()` :1405-1408).
   Every earlier TTO tile carries the skill's own name (Crescent Eclipse, Drop Anchor, Venom Phantom, Barrel Railgun,
   Gleaming Breath, Lucent Barrier: index.html:1258, :1277, :1294, :1331); "Sun Avatar" is only the code's name for Ja
   Ascension's active. Decided: **"Ja Ascension"** for the solarCall tile, so its keys become `@JaAscension:cast1` /
   `@JaAscension:root`; "Ascended Ja" and "Bastion Buiten" stay (the passive's look on another skill's summon, as the
   Mole's Missile Pad beside Missile, Mole decision 14); "Rune Golem" stays.
3. **S3: do not add `"@JaAscension": "jaAscension"` to SEQ_SKILL.** A SEQ_SKILL value is dropped from every other tile's
   icons (`pooled`, index.html:3420), so the Ascended Ja tile would lose its Ja Ascension icon. S2's CLIP_SKILLS alone
   gives the four tiles their icons (cast1 / cast2 / root belong to no Monkey skill in `wardrobe/data/icons/hd/index.json`;
   the Bible has `monkey_ja4`, `monkey_buiten4`, `monkey_jaAscension5`, `monkey_buitenBastion5`, `monkey_runeGolem5`).
   Risk for the lead's browser pass: if the BB research makes `ja` / `buiten` members of the cast3 pool, the same filter
   drops the Ja / Buiten icon from the two boosted tiles (they then show only the TTO skill's icon).
4. **P2's shader reading is wrong; parts.md T2's is right.** What is wrong: "blend per `_SrcBlend` / `_DstBlend` when set
   (5/1 additive, 1/0 opaque-ish with ZWrite, 5/10 alpha)". The shader objects' pass state (`shader_v.py`): Additive
   `rtBlend0` src 1 (One), dst `[_Blend2]`, ZWrite 0, Cull `[_CullMode]`, ColorMask 14 (RGB); Alpha Blended src 5 / dst 10
   (SrcAlpha OneMinusSrcAlpha), ZWrite 0. Neither shader declares `_SrcBlend`, `_DstBlend` or `_ZWrite` (their property
   lists: `_MainTex, _Noise, _Flow, _Mask, _SpeedMainTexUVNoiseZW, _DistortionSpeedXYPowerZ, _Emission, _Color, (_Opacity),
   _Usecenterglow, _Usedepth, (_Usecustomrandom), _Depthpower, _CullMode, (_Blend2), _texcoord`): the 18 materials that save
   them (`mats_v.py`) carry stale values from another shader. Every Additive material saves `_Blend2` 1: **One One, no
   depth write, never opaque**. Counts over the 28 prefabs: 39 Additive + 2 Alpha Blended materials. The UV scroll stands:
   `tto_Trail_01_1_h7s10` / `_h11s10` `_SpeedMainTexUVNoiseZW` (0, -0.8, 0, 0) (`mats_v2.txt`), the only nonzero speeds;
   `_Usecenterglow` / `_Usedepth` / `_Usecustomrandom` 0 everywhere.
5. **P4 is already built.** The working tree's `pipeline/wardrobe_fx_tto.py` (`animation()`, :707-753, the Mole build's
   TTO clip export, Mole decision 56) writes TTO's legacy clips: `clips_v.py` gives the comet's and the crown's `Ja` node
   root 1.2 (Loop) / run / ko / summon / unsummon / suicideRun, and RuneGolem's root 5.3, run 1.2, attack1 1.0, attack2
   1.0, attack3 1.3333, summon 2.9, quake 1.6, collapse 2.0, no lost paths; the only export warnings left are the three
   `FX_Magic_Circle` AnimatorController ones (section 5's "AnimationClips ... written by name only" is outdated). P4 is
   done; P1 (the elementals' folders) is still needed. The RuneGolem root exports as it is (24 nodes; its AudioSource has
   no clip, `golem_audio.py`).
6. **Missed part: `MonkeyRow6Rise` on `runeGolem_quake`.** The quake prefab carries 6 `MonkeyRow6Rise` scripts on 6
   StaticMesh spikes (`probe_v.json`), not in section 5's table or P9. Add it to P9 (tto_monkey.js): fields delay
   0.03-0.05, depth 1.13-1.66, riseTime 0.13, hold 0.7, sinkTime 0.5, overshoot 0.15, tilt 25.6-32.3 (`dump.cs:112319`;
   values and the RVAs Awake 0x1d16800, Update 0x1d16c70, Place 0x1d16880 in parts.md T5; the bodies to disassemble as
   SunCrownFx's was). Also the `Light` components of `buitenBastion_rise` (disabled), `runeGolem_rise`, `_pound`, `_quake`,
   `_crumble` (`probe_v.json`): `fxparts/light.js` draws the component; the Shuriken LightsModule is parts.md T3's.
7. **`runeFracture` has a look and is built, not cued.** Section 2.5's "Rune Fracture on the foe: a status on the foe, no
   look" contradicts section 1 (the status looks): `elementals/runegolem/effects/runefracture` is a GroundHug ring + 2
   Shuriken (`probe_v.json`). On a foe it stays out (Cat decision 44, Chameleon 53, Mole 52, Sheep 4) but is "still
   built": P1's SKILL_FX list gains `runeFracture` (13 golem effects, as parts.md counts).
8. **Builds: the BB summon part's rings.** The boosted summons spawn BB's own summon looks through the part: the Ja's
   `summon_ring` (Ja.cs:1997-2013), the Buiten's `summonEffect` at its create and again at its unsummon (Buiten.cs:761-812;
   :974-1016: `unSummon`, `summonEffect` at its position, identity, Destroy 1 s later). With parts.md Interfaces 4's names,
   `jaAscension`'s builds + `ja_summon_ring`, `buitenBastion`'s + `buiten_summonEffect`.
9. Smaller: `tto/RuneGolem` is the name both reports use from here on (parts.md Interfaces 4 wrote `tto/runeGolem`; the
   catalog address is lower case either way, `Tto` compares `n.lower()`, wardrobe_fx_tto.py:327); `cue_tto` reads cues
   only, never `builds` (wardrobe_fx_tto.py:756-769), so every `tto/` name in a `builds` list must also be in SKILL_FX
   (P1), as the Mole's and the Chameleon's are.

Corrected block (replaces section 7's; the plain-key entries keep their `why`, with item 8's builds):

```json
{
  "jaAscension": {
    "why": "as section 7's jaAscension entry (unchanged), plus: the BB summon part spawns the Ja's summon_ring at the create (Ja.cs:1997-2013; Verification 8)",
    "builds": ["tto/jaAscension_aura", "ja_summon_ring"],
    "cues": [
    [0, "voice", "ja"],
    [0.25, "fx", "castEffect_fire", {"y": 1, "d": 1}],
    [0.45, "fx", "tto/jaAscension_pillar", 2],
    [0.5, "fx", "Ja4", {"d": 2, "boost": 2, "end": 10}]
    ]
  },
  "buitenBastion": {
    "why": "as section 7's buitenBastion entry (unchanged), plus: the BB summon part spawns the Buiten's summonEffect at its create and at its unsummon (Buiten.cs:761-812, :974-1016; Verification 8)",
    "builds": ["tto/buitenBastion_aura", "buiten_summonEffect"],
    "cues": [
    [0, "voice", "buiten"],
    [0.5, "fx", "tto/buitenBastion_slam", 0.35],
    [0.5, "fx", "tto/buitenBastion_rise", 2],
    [0.55, "fx", "Buiten4", {"d": 2, "boost": 2, "end": 10}]
    ]
  },
  "golemCall": {
    "why": "as section 7's golemCall entry (unchanged); runeFracture (the quake's status look on the foe) is built through SKILL_FX, never cued (Verification 7); runeGolem_quake's spikes are MonkeyRow6Rise (Verification 6)",
    "builds": ["tto/runeGolem_rise", "tto/runeGolem_riseBurst", "tto/runeGolem_roar", "tto/runeGolem_auraPulse", "tto/stoneAegis", "tto/runeGolem_step", "tto/runeGolem_fistHit", "tto/runeGolem_pound", "tto/runeGolem_quakeCharge", "tto/runeGolem_quake", "tto/runeGolem_crumble", "tto/runeGolem_dust"],
    "cues": [
    [0, "voice", "summon"],
    [0, "fx", "tto/runeGolem_circle", 4.5],
    [0.55, "fx", "tto/runeGolem_stomp"],
    [0.55, "voice", "upheaval"],
    [0.6, "fx", "tto/RuneGolem", {"d": 4.5, "end": 10, "to": [0, 0, 10]}]
    ]
  },
  "@JaAscension:cast1": {
    "why": "Ja Ascension's active (Sun Avatar in the code, cell 452; the tile is named for the skill: Verification 2) needs a living Ja of the Monkey within 30 m, the highest level first (TTO1102:Monkey::PickJa@0x1CC8AD0 via ::ReleaseSunAvatar@0x1CD2840, Monkey.c:44330-44415): the tile shows the boosted Ja (level 6, the passive's, with its jaAscension_aura) already standing at its summon spot 2 m ahead (SummonSpot(2) of the jaAscension tile; a level-6 Ja's followDistance 5 keeps it there), from the tile's start; at the bar's end the coroutine hides it (Monkey::HideBody@0x1CC6F90 :20550) and SpendJa kills it (:44401): kill 0.8 = cast1 (0.7 s) + the 0.1 s bar. MERGE: this key replaces the plain cast1 entry for this sequence, so the BB research's cast1 cues (the cast voice, castRing ...) go in here too",
    "builds": ["tto/jaAscension_aura"],
    "cues": [
    [0, "fx", "Ja4", {"d": 2, "boost": 2, "standing": true, "kill": 0.8}]
    ]
  },
  "solarCall": {
    "why": "as section 7's solarCall entry (unchanged; TTO1102's crown, jaLv + 10 = 16 s, cut at 10 s: kill 10; its end starts the collapse: @JaAscension:root)",
    "cues": [
    [0, "fx", "tto/jaAscension_launch", 2],
    [0, "fx", "tto/sunAvatar_comet", {"y": 1.2, "d": 2, "to": [0, 1.95, 0], "rise": 4.24, "kill": 0.9}],
    [0, "voice", "ja"],
    [0, "fx", "tto/jaAscension_callFx"],
    [0.9, "fx", "tto/sunAvatar_ignite"],
    [0.9, "fx", "tto/solarCrown", {"head": 1.35, "kill": 10}]
    ]
  },
  "@JaAscension:root": {
    "why": "The crown's end (the 10 s cut at solarCall 10.9 s = this step's 9.6 s; root starts at solarCall's 1.3 s end) starts the Solar Collapse (TTO1102:Monkey::OnExtendedUpdate@0x1CC7C30, Bible :914): TTO1102:Monkey.<RPC_solarCollapse>d__363::MoveNext@0x1D15280 (pseudo/Monkey.c:17382-17739): sunAvatar_dive at the Monkey + up x (HeadHeight + 0.6) = 1.95, identity; 0.5 s rising to + 5 up (6.95); the dive 0.3 s to the Monkey + 0.5 up (part P7); then the sun destroyed and jaAscension_supernova at the Monkey, identity, ShakeNear (left out), the hits r 6 (no look). TTO1102's code as every class (Bat decision 44, Cat 42, Chameleon 44, Mole 57; Verification 1); TTO1106+'s aimed recast (the dive 0.3 + 0.015 x distance onto a selected enemy) is offered to the user, not shown",
    "cues": [
    [9.6, "fx", "tto/sunAvatar_dive", {"y": 1.95, "top": 6.95, "to": [0, 0.5, 0], "dive": 0.3, "kill": 0.8}],
    [10.4, "fx", "tto/jaAscension_supernova"]
    ]
  }
}
```

Corrected S1 (replaces section 7's):

```
"Ascended Ja: cast1 cast2*~@0.1 jaAscension~0.15 root*~@10.4",
"Ja Ascension: cast1 cast2*~@0.1 solarCall~0.15 root*~@12.9",
"Bastion Buiten: cast1 cast2*~@0.1 buitenBastion~0.15 root*~@10.3",
"Rune Golem: cast1 cast2*~@0.1 golemCall~0.15 root*~@11.9"
```

S2 unchanged; S3 dropped (item 3). Section 8: Q1 = B (item 1); Q2-Q8 as recommended (Q7: the golem's AI runs as the code,
with the aura pulses, Stone Aegis on the hero, the glow and MonkeyRow6Rise, item 6; Bat decision 24, Mole decision 32's
Auto Gyro Gun). P1's SKILL_FX gains `runeFracture` (item 7). Not re-checked: SunCrownFx's disassembly
(`suncrown_late.asm` is the researcher's scratch; the fields 0.75 / 140 / 40 are in the prefab, `probe_v.json`), the
FX_Magic_Circle clip decode (`animator.py`, not re-run), the golem's Think order beyond the Bible's (:952-955).
