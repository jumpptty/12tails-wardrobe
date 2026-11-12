<!-- Saved by the lead from the researcher's returned text (2026-11-13): its Write was refused. -->

Summary: all 11 clips are traced, with file:line, through the opaque predicates and the timed waits. There are two pools: assemble1 / assemble2, shared by Auto Gyro Gun, Barrel Bot and War Capital, plus TTO's released Barrel Railgun. dig1 belongs to King Kaiser alone. dig2 is never played. Two prefabs the code loads are missing from both BB's and TTO's data: advanceRepair_ring and barrelCannon_ring. Five missing parts (P1-P5) are needed, and there are 12 open questions, each with a recommended answer.

# Mole effects + sounds research: skills_a (eleven skill clips)

Researcher `skills_a`, 2026-11-13 (home PC).
- **Scope:** the clips advanceRepair, assemble1, assemble2, barrelCannon, bunker, chopper, detonate, dig1, dig2, flameTurret1 and flameTurret2, and every skill that plays them.
- **Method:** research only (recipe steps 1-3).
- **Line numbers:** `D:\12tails\DecompiledSource\Mole.cs` unless another file is named. "TTO" means `D:\12tails\DecompiledSource_TTO_2026-11-02\pseudo\Mole.c`.
- **Units:** times are seconds from the start of the clip the cue is keyed by. d = metres ahead, x = metres right, y = metres up.

## Read-only probes

Everything is in `D:\12tails-wardrobe\checks\fx_mole_research\skills_a\`. Nothing there writes outside that folder.

- **Coroutine reads:**
  - `cond.py <file> <from> <to>` works out the opaque predicates.
  - `f.sh` does the same with the junk lines dropped; `F=<file>` picks another .cs.
  - Outputs: `advanceRepair.txt`, `assemble1.txt`, `barrelCannon.txt`, `bunker.txt`, `chopper.txt`, `detonate.txt`, `kingKaiser.txt`, `kingKaiser_create.txt`, `flameTurret.txt`, `flow_RPC_*.txt` (clip_flow.js) and `clip_calls.txt`.
- **`probe\probe.json`** with `probe\summary.txt` (from `summ.py`): `wardrobe_fx.py mole --probe` of the 19 named effects.
  - `probe\probe_tto.*`: `wardrobe_fx_tto.py --probe advanceRepair_ring,barrelCannon_ring`.
  - `probe\probe_tto_wc.json`: TTO's copy of warCapital.
- **`probe\fields.py` -> `fields.txt`:** the Mole hero prefab's `Mole` MonoBehaviour fields (Mole.cs:19430-20084), resolved:
  - Mole_chopper = effects/chopper.
  - chopper_startDust = effects/chopper_StartDust.
  - chopper_forwardDust = effects/chopper_forwardDust.
  - kaiser_dust and kaiser_box are in sharedassets8.assets (path IDs 387 / 379) and are **not in Resources**.
  - Aside for skills_b: the skyDrill_hit field points to the chopper_hit prefab.
- **`probe\nukefield.py` -> `nukefield.txt`:** Mole_timeNuke's fields on timeNuke1 / timeNuke2: mLv, isVisible, timeNuke_explosion (= effects/timeNuke_explosion).
- **`probe\probe2.py` -> `probe2.json`:** kaiser_dust, kaiser_box, timeNuke_explosion and the robots AutoGyroGun4, BarrelBot4 and KingKaiser_b. ALIASES and the container were patched in memory only.
- **`probe\probe3.py` -> `probe3.json`:** the robots read with stand-in word layouts for their scripts.
- **`entries.py` -> `entries.json` / `cues_whole.json`:** the cue entries, JSON-checked.

## Max rank and passives on

- Auto Gyro Gun 4 (+ Hidden Turret #403, Heavy Built: stats only).
- Barrel Bot 4 (+ Double Bot #423).
- Bunker 2, Flame Turret 3, Chopper 3 (+ Barrel Cannon #443).
- Advance Repair, Barrel Cannon, Detonate (with Time Nuke 2's nuke) and War Capital: one rank each.
- King Kaiser (+ Kaiser Cannon #372 and Kaiser Beam #373).
- Super Dig #411 (Charge Attack).

No rank picks a different effect. Ranks change only damage, speed, cast time and the summon's model number.

---

## Read this first

### 1. Who plays these clips

| clip | BB | TTO |
|---|---|---|
| advanceRepair | RPC_advanceRepair :36725 | same (TTO:1391) |
| assemble1 | RPC_assemble1 :23438 (Auto Gyro Gun, Barrel Bot, War Capital) | RPC_assemble1 (TTO:1845); **RPC_barrelRailgun** through WarAreaBegin (TTO:2840) |
| assemble2 | RPC_assemble1 :23065 | RPC_assemble1 (TTO:1933); RPC_barrelRailgun (TTO:2962) |
| barrelCannon | RPC_barrelCannon :40208 | same (TTO:2613); RPC_warArea through WarAreaBegin (TTO:23620): **not released, no cue** |
| bunker | RPC_bunker :25334 | same (TTO:6191) |
| chopper | RPC_chopper :34028 | same (TTO:8996) |
| detonate | RPC_detonate :31277 | same (TTO:9438) |
| dig1 | RPC_cAttack1 :22304 (only without Super Dig); RPC_kingKaiser :35389 | same (TTO:7236, :12788) |
| dig2 | **none** (only the clip loader names it, :709-715) | none |
| flameTurret1 / 2 | RPC_flameTurret :28234 / :27861 | same (TTO:11509 / :11335) |

- TTO's copies of these coroutines load the same names, with the same constants (string lists TTO:1138-12962). No look changes.
- The assemble clips are two pools.
- With the passives on, Charge Attack plays superDig (:22290-22304), so dig1 is King Kaiser's only.

### 2. Two rings are missing from both games' data

- `Effects/advanceRepair_ring` (:36840) and `Effects/barrelCannon_ring` (:40226) are not in BB's Resources (the probe gives a KeyError).
- They are not in BB's rip folder either, nor in TTO's catalog (`probe_tto.err`).
- The game logs "Cannot find … effect" and draws nothing.
- This is a Bible finding to offer the user.

### 3. Missing part P1: the robot summons

The summons are robot characters, not effects: `Characters/Robots/AutoGyroGun/AutoGyroGun4`, `.../BarrelBot/BarrelBot4` and `.../KingKaiser/KingKaiser_<r g b k w p>`. Each has Animation, SkinnedMeshRenderer, CharacterControl and its own scripts. AutoGyroGun4 has the clips root, create, destroy, fire and hide (`probe3.json`).

The extractor needs:
- ALIASES paths for them.
- Data-only layouts for `AutoGyroGun` (36 bytes: autoGyroGun_fire, nAttack_fx and create_fx, AutoGyroGun.cs:1083-1089), `BarrelBot` (208), `BarrelBotAI` (8) and `KingKaiser`.
- A reader for KingKaiser's clips. Today the probe fails with "clip run: compressed / float curves / events are not read yet".

The page needs a `fxparts/mole.js` summon part:
- **AutoGyroGun:**
  - Spawn (AutoGyroGun.cs:1651-1741): `create` once with `create_fx`, then `root` looped from 0.8 s.
  - AI (:733-990, :1159-1477): the first scan is 2 s after Awake (:58). After that it shoots every 2 s at an enemy within 24 m.
  - Each shot: the gun node turns (:1329), `fire` crossfades in, `nAttack_fx` plays, `autoGyroGun_fire` spawns at the turret (:1440), and `root` returns 0.7 s later.
  - Hidden Turret's hide (:832-861) never happens while it keeps firing.
  - It aims at the cue's `to`. Its 120 s life is cut at 10 s.
- **BarrelBot** (BarrelBot.cs:5940-6103): `getUp` once with `create_fx`, standby 0.8 s later, then `root`. Its AI is left out (open question 3).
- **KingKaiser** (KingKaiser.cs:3821-4048):
  - `create` once with `kaiser_createFx`, standby after 3 s, then `root`.
  - The model follows the outfit colour, Skin / 100: 1 r, 2 g, 3 b, 4 k, 5 w, otherwise p (:35709-35776).
  - The hero is hidden through a `hideHero` option, as penguin.js does for Snow Man.

### 4. Missing part P2: effects held in prefab fields

- `kaiser_dust` and `kaiser_box` are Mole-prefab fields (Mole.cs:19811-19814) with no Resources path. They live in sharedassets8.assets as path IDs 387 / 379.
- Their components are all ready.
- wardrobe_fx.py needs a way to load them by field index, e.g. `FIELD_REFS = {"mole": {"kaiser_dust": ("Mole", 12), "kaiser_box": ("Mole", 13)}}`. That is the PPtr at header + 8 × index, as probe2.py reads it.
- kaiser_box's own sound exists only as `RippedAssets\ExportedProject\Assets\AudioClip\kaiser_box.wav`, outside Resources. It needs a sound alias, or rip_wav's walk has to include that folder.
- The chopper's three effects are also prefab fields, but they are in Resources, so they are ready by name.

### 5. Missing part P3: the cue option `playAudio`

- The chopper's AudioSource (`chopper`, loop, playOnAwake off) is started by `mChopper.audio.Play()` at 0.7 s (:33663) and stopped at 5.3 s (:33806).
- The page only starts playOnAwake sources (index.html:4073).
- New option `playAudio`: seconds after the spawn at which the root AudioSource plays (looped per its `loop`); it stops when the effect ends.
- Add it to wardrobe_fx_check.py's OPTS.

### 6. Missing part P4: Mole_timeNuke

- The inventory already lists it, and skills_b shares it.
- Its 16 field bytes are mLv (i), isVisible (b) and timeNuke_explosion (r), Mole_timeNuke.cs:341-350.
- For Detonate the nuke model only has to stand still until it explodes. Its OnGUI countdown is screen text and is left out.

### 7. Missing part P5: warCapital

- BB's Shuriken system on node 2 is dropped by the extractor. TTO's copy reads whole (ParticleSystem with tto_Smoke1): use `SHURIKEN_FROM_TTO["mole"] = ["warCapital"]`.
- Mole_warCapital (Mole_warCapital.cs:313-381) plays `open` once, then `root` looped after 1 s.
- Its CharacterControl is data only.
- Its missiles never come inside 10 s: the first scan is 12 s after the create (:43912).

### 8. Left out: hits, statuses and camera effects

- Effects that draw nothing: Advance Repair's heal (a number), Flame Turret's damage box, the Chopper's hits and #443's 5 m blasts (damage only), King Kaiser's noForce status.
- Camera effects: the motion blurs, King Kaiser's zoom, shake and colour ramp.

### 9. The hero does not travel

- In the game the Chopper flies at 3 m/s from 0.7 s and at 8 m/s from 1.3 s (:33658, :33690).
- In the wardrobe every effect stays at the standing hero.
- Flame Turret's 45° turns are left out.

### What is ready

- **Effects** (inventory + probe): assemble_box, assemble_dust, bunker, bunker_hole, chopper, chopper_StartDust, chopper_forwardDust, choppperCannon_ring, detonate, detonate_ring, timeNuke_explosion, dig_hole, dig_dust, flameTurret, flameTurret_fire.
- **Voices** (all in BB's rip): advanceRepair1-2, cast, autoGyroGun1-2, barrelBot1-2, bunker1-2, chopper1-2, detonate1-2, flameTurret1-2, kingKaiser1-2, laugh.
- **Effect sounds** (all in `mole/sounds`): assemble, bunker, chopper, chopperCannon_ring, detonate, dig, fireTurret, timeNuke, warCapital. The exception is kaiser_box (item 4).

---

## Advance Repair (`advanceRepair`, 0.4 s loop)

Source: RPC_advanceRepair :36263-36900; RPC_advanceRepair0 :13665.

| time | what happens | source |
|---|---|---|
| 0 | clip (0.2 s fade, Loop) | :36725 |
| 0 | voice advanceRepair1 or 2, at random | :36766-36821 |
| 0 | ring: missing (item 2) | — |
| every 1 s | SP − 1, target +150 HP | :36671-36699 |
| end | a move key, the target past 2 m, or SP < 5 | :36573-36658 |

- The skill needs a Robots / Structure ally within 2 m (doSkill :7048).
- Nothing visible comes of it.
- The page already loops this clip (`LOOPS`), so it needs no SEQ.

## Assemble pool: Auto Gyro Gun and Barrel Bot, plus War Capital

Clips: `assemble1` (0.6 s), `assemble2` (0.5 s loop). Sources: RPC_assemble1 :22908-23596; RPC_assemble0 :10477.

| time | what happens | source |
|---|---|---|
| 0 | `assemble1` (0.2 s fade, Once) | :23438 |
| 0 | voice `cast` | :23479-23533 |
| 0.6 | `assemble2` cut in (Loop) | :23065 |
| 0.6 | `assemble_box` at the hero: EffectControl 999, followState, own looping `assemble` sound | :23086-23098 |
| 0.6 | cast bar magAdjust: Auto Gyro Gun 1 + 4, Barrel Bot 3 + 4, War Capital 24 | :23353-23417 |
| 0.6 + bar | box destroyed, standby, create RPC | :23163-23331 |

The cast bar is `magAdjust(t) = clamp(t − floor(MAG'/32), 0.1, 600)`, with MAG' at most 512 (CharacterControl.cs:20584-20588). At the highest MAG:
- Auto Gyro Gun and Barrel Bot get **0.1 s**, magAdjust's floor (the Bat's bigCast2 precedent).
- War Capital gets **8 s**, so it gets its own tile.

The create RPCs (getSpawnVector puts each summon k m ahead on the floor):
- **Auto Gyro Gun 4** (:11751-12235):
  - assemble_dust 0.7 m ahead.
  - Voice autoGyroGun1 or 2.
  - AutoGyroGun4 0.7 m ahead, LookRotation(forward) (:23199, :12019-12031).
  - Life chaAdjust(120), cut at 10 s.
- **Barrel Bot 4** (:12279-13005):
  - assemble_dust 1 m ahead (:12304).
  - Voice barrelBot1 or 2.
  - BarrelBot4 0.7 m ahead (:23249, :12589).
  - No lifetime of its own, cut at 10 s.
  - Double Bot only keeps a bot from an earlier cast (:12415).
- **War Capital** (:14239-14463):
  - `warCapital` 2 m ahead (:23291) with its own sound.
  - Voice `laugh` (:14328).
  - Open, then root.
  - Cut at 10 s.

War Capital's cues are keyed `@WarCapital:assemble1/2` so that it is not a pool member: a member whose tile id is already taken would get a random member's cues (poolChains / fxStart).

### Page lines

- `SEQ.mole`: "Assemble: assemble1 assemble2*@0.1" (was `@0`).
- `SEQ.mole`: add "War Capital: assemble1 assemble2*@8".
- `SEQ_SKILL.mole["@WarCapital"] = "warCapital"`.
- `wardrobe_skill_icons.py`: `CLIP_SKILLS["mole"]["assemble1"] = ["autoGyroGun", "barrelBot"]`, and the same for `assemble2`.
- `wardrobe_skill_icons.py`: `OWN_TILE["mole"] = {"warCapital": ["assemble1", "assemble2"]}`.
- Data: ALIASES for AutoGyroGun4 and BarrelBot4 (P1); `SHURIKEN_FROM_TTO` (P5).

### TTO Barrel Railgun (released) on the same clips

Source: TTO:2758-3388.
- `WarAreaBegin("barrelRailgun", tDir, "assemble1", 0.2)` (TTO:2840, TTO:41178) plays no voice.
- The rail turret `barrelRailgun_turret` (MoleRailTurret Grow/Assemble over 6 s) stands 1.17 m ahead, with `assemble_dust` there (RailFx) and Sounds/assemble.
- A fixed 6 s cast bar (DisplayCastBar(6), not magAdjust).
- At 0.6 s: `assemble2` cut in (Loop) and `assemble_box` at the hero (TTO:2960-2972).
- At 6 s: the box is destroyed, Finish runs, and `barrelRailgun1` starts from its 0.55 s mark with a 0.1 s fade (TTO:2990-3010).

So the page's "Barrel Railgun: barrelRailgun1 barrelRailgun2*@6 …" starts 6 s late. If the tto report reshapes it to begin "assemble1@0.6 assemble2*@5.4":
- `@BarrelRailgun:assemble1` gets no cues.
- `@BarrelRailgun:assemble2` = `[[0, "fx", "assemble_box", {"kill": 5.35}]]`.
- The dust and the turret go in its own block.

## Barrel Cannon (`barrelCannon`, 1.0 s)

Source: RPC_barrelCannon :39835-40330.

| time | what happens | source |
|---|---|---|
| 0 | clip (0.2 s fade, Once) | :40208 |
| 0 | voice barrelBot2 (one file, no random pick) | :40281-40320 |
| 0 | ring: missing | — |
| 0.3 | RPC_cannonForm sent to each living bot; none here ("BarrelBot is not ready") | :39989-40112 |
| 0.8 | standby | — |

- doSkill casts the skill with no bot check (:7356-7375), so clip plus voice is a real game look.
- With bots, each plays cannonForm1 with its cannonForm_ring, then cannonForm2 and 10 shells 0.5 s apart (BarrelBot.cs:5377-5800). See open question 4.

## Bunker (`bunker`, 0.5 s)

Source: RPC_bunker :25102-25640; RPC_bunker0 :10954.

| time | what happens | source |
|---|---|---|
| 0 | clip **cut in** (`PlayAnimation(bunker, 0)`, Once) | :25334 |
| 0 | voice bunker1 or 2 | :25383-25438 |
| 0 | `bunker_hole` at the hero (EffectControl 1) | :25451-25469 |
| 0.2 | `bunker`: EffectControl 999, followState, sandbag mesh, dust ring, puff, own `bunker` sound | :25248-25266 |
| 0.2 | Race = Structure | :25280 |
| after | held until a move key | :25485-25578 |

- Rank 2's damage reduction changes no look.
- Page line: "Bunker: bunker@3". The clip plays once and holds its last frame; the cut is 2.95.

## Chopper (`chopper`, 5.2 s)

Source: RPC_chopper :33450-34186.

| time | what happens | source |
|---|---|---|
| 0 | clip (0.2 s fade, Once) | :34028 |
| 0 | voice chopper1 or 2 | :34069-34169 |
| 0.3 | the `chopper` under `mount_Cannon` (local 0 / identity; EffectControl 5.5, followState; Animation root; its loop chopper sound, playOnAwake off) | :33589-33604 |
| 0.5 | `chopper_StartDust` at the hero, identity rotation | :33631 |
| 0.7 | moveSpeed 3; the chopper's audio Play() | :33658-33663 |
| 1.3 | moveSpeed 8 | — |
| 1.3 | #443 on: `choppperCannon_ring` (EffectControl 4, followPosition, own loop sound) | :33690-33719 |
| 1.3 + 0.4 k (k = 0-9) | `chopper_forwardDust` at the hero | :33794-34002, Yield 0.4 :34160 |
| 5.3 | sound Stop; standby | :33800-33868 |

- The clip ends at 5.2 s, before the standby, so the chopper is cut at 5.15.
- `chopper_hit` comes only on a hit.

## Detonate (`detonate`, 1.5 s)

Sources: RPC_detonate :30961-31490; Mole_timeNuke.cs :407-523 and :615-921.

| time | what happens | source |
|---|---|---|
| 0 | clip (0.2 s fade) | :31277 |
| 0 | voice detonate1 or 2 | :31318-31373 |
| 0 | `detonate_ring` at the hero (EffectControl 1.5; emitters start at 0.5 s; own sound) | :31386-31404 |
| 0.6 | each nuke gets `detonate`, and the `detonate` effect spawns at it, identity rotation | :31096-31171 |
| 1.1 | doExplode: `timeNuke_explosion` at the nuke (EffectControl 4, own `timeNuke` sound); the nuke's renderers go off and it is destroyed after four 0.1 s rings | :796-911 |
| 1.3 | standby | — |

- Without a nuke the skill is refused ("Cannot find TimeNuke to detonate", :6740-6762).
- The tile assumes `timeNuke2` 1 m ahead with identity rotation, the spot RPC_timeNuke uses (mPos + tDir, :30653; :11663-11687). It stands until 1.1 s (P4).

## King Kaiser (`dig1`, 1.87 s, then the Kaiser)

Sources: RPC_kingKaiser :34990-35530; RPC_kingKaiser_create :35536-36204.

| time | what happens | source |
|---|---|---|
| 0 | dig1 (0.2 s fade, Once) | — |
| 0 | noForce 5 s | — |
| 0 | `dig_hole` at the hero, 0.05 m up (EffectControl 5, hole mesh; looping `dig` for 2 s) | :35426-35444 |
| to 1.9 | `dig_dust` every 0.1 s on the frame loop; strictly after 0.1 s, so 0.117 s at 60 fps | :35293-35364 |
| 2.4 | `kaiser_dust` (four puffs at ±1.5, ±1) | :35127 |
| 2.9 | `kaiser_box` at rotation × Euler(270, 90, 0) (EffectControl 3, box mesh, own sound) | :35186-35192 |
| 4.9 | `kaiser_dust` again | — |
| 4.9 | the Kaiser at the hero's spot (getExpandPos only moves it when blocked) | :35229-35270, :35794 |
| 4.9 | voice kingKaiser1 or 2 | :36057 |
| 4.9 | the Mole hidden for chaAdjust(240) | :36135 |

- The Kaiser plays create (3 s), then root. It is cut at 10 s.
- dig1 holds its last frame until 4.9 s.

Page lines:
- `SEQ.mole`: "King Kaiser: dig1@4.9 root*@10".
- `SEQ_SKILL.mole["@KingKaiser"] = "kingKaiser"`.
- `CLIP_SKILLS["mole"]["dig1"] = ["kingKaiser"]` (the Bible has mole_kingKaiser3).

The KingKaiser part picks the model by outfit colour. If P1's Kaiser is not built, drop the third cue of `@KingKaiser:root` and make the step `root@0.5`.

## dig2 (0.13 s)

- No BB or TTO code plays it: only the loader names it (:709-715), and TTO has no such string.
- `NEVER_PLAYED.mole = ["dig2"]`, as for the Wolf's cast1-3, the Bison's volcanicRam and the Cat's shikifujin.
- No cues.

## Flame Turret (`flameTurret1` 0.5 s, `flameTurret2` 0.5 s loop)

Source: RPC_flameTurret :27714-28415.

| time | what happens | source |
|---|---|---|
| 0 | flameTurret1 **cut in** | :28234 |
| 0 | voice flameTurret1 or 2 | :28275-28330 |
| 0 | `flameTurret`: EffectControl 60, followPosition, followState, followObject; turret model with create / root, puff, dust ring; own `bunker` sound | :28343-28359 |
| 0.5 | flameTurret2 cut in (Loop) | :27861 |
| 1.0 | `flameTurret_fire`: EffectControl 5, followState; flames 1.5 m ahead; loop `fireTurret` sound | :27893-27911 |
| from 1.25 | damage box every 0.25 s | — |
| 5.0 | standby: actionTime + chaAdjust(5) | :27935, :27984-28028 |

- chaAdjust(5) = (int)(5 × (1 + 0.015 × CHA')), which is 5 at CHA 1 (CharacterControl.cs:20593-20619).
- Rank 3 changes only the damage.
- Both effects are cut at 4.45 on flameTurret2's clock.
- Page line: "Flame Turret: flameTurret1 flameTurret2*@4.5" (was @3).

---

## Paste-ready cue entries for wardrobe/fx_cues/mole.json

Validated in `D:\12tails-wardrobe\checks\fx_mole_research\skills_a\cues_whole.json`.

```json
{
  "advanceRepair": {
    "why": "Mole.cs RPC_advanceRepair (:36263-36900), Advance Repair #431 (one rank; doSkill :7048 needs a Robots / Structure ally within 2 m): clip (0.2 fade, looped, :36725-36728) and voice advanceRepair1 / advanceRepair2 (Random.Range(0, 2) :36766-36821) at 0; Effects/advanceRepair_ring at the hero (createEffect :36834-36850) is in neither BB's data (resources.assets) nor TTO's catalog (checks/fx_mole_research/skills_a/probe): the game logs 'Cannot find advanceRepair_ring effect' (:36859) and draws nothing; from 1 s, every 1 s: SP - 1 and the target +150 HP (:36671-36699; the heal number only); the channel ends on a move key, the target past 2 m or SP < 5 (:36573-36658; RPC_advanceRepair0 :13665-13695 standby): the page's loop (LOOPS)",
    "cues": [
      [0, "voice", "advanceRepair1|advanceRepair2"]
    ]
  },
  "assemble1": {
    "why": "The assemble1 clip opens RPC_assemble1 (Mole.cs:22908-23596), the build coroutine of Auto Gyro Gun, Barrel Bot and War Capital (sType :23353-23411); BB's only player, and TTO's RPC_assemble1 the same (pseudo/Mole.c:1735-2297); War Capital has its own tile (its 8 s bar), TTO's Barrel Railgun its own sequence: one tile each (poolChains, with the Assemble sequence's steps)",
    "skills": {
      "autoGyroGun": {
        "why": "Mole.cs RPC_assemble1 with sType autoGyroGun (rank 4, :8285): clip (0.2 fade, Once, :23438-23441) and voice cast (one file, :23479-23533) at 0; Yield 0.6 (:23527): assemble2",
        "cues": [
          [0, "voice", "cast"]
        ]
      },
      "barrelBot": {
        "why": "Mole.cs RPC_assemble1 with sType barrelBot (rank 4, :5130-5170): clip (0.2 fade, Once, :23438-23441) and voice cast (:23479-23533) at 0; Yield 0.6 (:23527): assemble2",
        "cues": [
          [0, "voice", "cast"]
        ]
      }
    }
  },
  "assemble2": {
    "why": "RPC_assemble1's build step (Mole.cs:23065-23125): assemble2 cut in and looped, the assemble box, the cast bar magAdjust(1 + sLv) / magAdjust(3 + sLv) (:23353-23417; 0.1 s, magAdjust's floor, CharacterControl.cs:20584-20588, the SEQ's assemble2*@0.1), then the summon in the same frame (:23163-23331)",
    "skills": {
      "autoGyroGun": {
        "why": "Mole.cs RPC_assemble1 (autoGyroGun, sLv 4): at 0.6 s assemble2 (cut, loop, :23065-23070) and Effects/assemble_box at the hero, hero rotation (createEffect :23086-23098; EffectControl life 999, followPosition, followState; Animation root looped; plays its own looping Sounds/assemble); at the bar's end (magAdjust(5) = 0.1 s, cued 0.05: the step edge less the page's margin) the box Destroyed (:23331), standby (RPC_assemble0 :10477-10504) and RPC_autoGyroGun_create4 (:23199-23236, :11751-12235): assemble_dust 0.7 m ahead, hero rotation (Instantiate :11764-11776; life 1), voice autoGyroGun1 / autoGyroGun2 (Random.Range(0, 2) :11819-11874), the turret Characters/Robots/AutoGyroGun/AutoGyroGun4 where a ray from 1 m up along 0.7 forward - up meets the floor (getSpawnVector :23199: 0.7 m ahead), LookRotation(forward) (:12019-12031); AutoGyroGun.create (AutoGyroGun.cs:1651-1741): clip create and its create_fx, 0.8 s later root looped; life chaAdjust(120) cut at 10 s; its AI (first scan 2 s after Awake, AutoGyroGun.cs:58, then a shot every 2 s at an enemy within 8 + 4 x 4 = 24 m, :755-811, :1159-1477) fires at the 10 m target 0.6 m up (parts: the robot summon)",
        "cues": [
          [0, "fx", "assemble_box", {"kill": 0.05}],
          [0.05, "fx", "assemble_dust", {"d": 0.7}],
          [0.05, "voice", "autoGyroGun1|autoGyroGun2"],
          [0.05, "fx", "AutoGyroGun4", {"d": 0.7, "kill": 10, "to": [0, 0.6, 10]}]
        ]
      },
      "barrelBot": {
        "why": "Mole.cs RPC_assemble1 (barrelBot, sLv 4): at 0.6 s assemble2 and assemble_box as Auto Gyro Gun's (:23065-23098); at the bar's end (magAdjust(7) = 0.1 s, cued 0.05) the box Destroyed (:23331), standby, RPC_barrelBot_create4 (:23249-23274, :12279-13005): assemble_dust 1 m ahead (position + forward), hero rotation (:12292-12304), voice barrelBot1 / barrelBot2 (Random.Range(0, 2) :12347-12402), Characters/Robots/BarrelBot/BarrelBot4 0.7 m ahead on the floor (getSpawnVector :23249), LookRotation(forward) (:12589-12601); BarrelBot.create (BarrelBot.cs:5940-6103): getUp once and its create_fx, standby 0.8 s later, then root; no life (BarrelBot.cs:179-260): cut at 10 s; Double Bot #423 keeps an earlier bot (:12415-12433): none in a single play; its AI (BarrelBotAI.cs) left out (open question 3)",
        "cues": [
          [0, "fx", "assemble_box", {"kill": 0.05}],
          [0.05, "fx", "assemble_dust", {"d": 1}],
          [0.05, "voice", "barrelBot1|barrelBot2"],
          [0.05, "fx", "BarrelBot4", {"d": 0.7, "kill": 10}]
        ]
      }
    }
  },
  "@WarCapital:assemble1": {
    "why": "Mole.cs RPC_assemble1 with sType warCapital (War Capital #444, one rank): clip (0.2 fade, Once, :23438-23441) and voice cast (:23479-23533) at 0; Yield 0.6 (:23527): assemble2",
    "cues": [
      [0, "voice", "cast"]
    ]
  },
  "@WarCapital:assemble2": {
    "why": "Mole.cs RPC_assemble1 (warCapital): at 0.6 s assemble2 (cut, loop, :23065-23070) and assemble_box at the hero (createEffect :23086-23098; life 999, followState; its own looping Sounds/assemble); the bar magAdjust(24) (:23393, :23417), at the highest MAG 24 - 512 / 32 = 8 s (CharacterControl.cs:20586-20587; the SEQ's assemble2*@8, cued 7.95): the box Destroyed (:23331), standby, RPC_warCapital_create (:23291-23316, :14239-14463): any earlier War Capital destroyed (:14252), Effects/warCapital 2 m ahead on the floor (getSpawnVector(position + up, 2 x forward - up) :23291), LookRotation(forward) (:14267-14279; plays its own Sounds/warCapital), voice laugh (:14328-14340), InitWarCapital (:14451; Mole_warCapital.cs:313-381: open once, 1 s later root looped); lives until destroyed (Mole_warCapital.cs:100-170): cut at 10 s; its first enemy scan 12 s after the create (OnWarCapital :43912, then every 6 s :43919): no missiles within the 10 s",
    "cues": [
      [0, "fx", "assemble_box", {"kill": 7.95}],
      [7.95, "fx", "warCapital", {"d": 2, "kill": 10}],
      [7.95, "voice", "laugh"]
    ]
  },
  "barrelCannon": {
    "why": "Mole.cs RPC_barrelCannon (:39835-40330), Barrel Cannon #443 (one rank; doSkill :7356-7375 casts with no bot check): clip (0.2 fade, Once, :40208-40211) and voice barrelBot2 (one file, no pick, :40281-40320) at 0; Effects/barrelCannon_ring at the hero (createEffect :40220-40238) is in neither BB's data nor TTO's catalog (probe): 'Cannot find barrelCannon_ring effect' (:40246), nothing drawn; Yield 0.3 (:40325): each living Barrel Bot (and Double Bot's second, :40053-40104) is sent RPC_cannonForm (BarrelBot.cs:5377-5800), none here ('BarrelBot is not ready', :40046); Yield 0.5 (:40327): standby at 0.8 s (:40133-40177)",
    "cues": [
      [0, "voice", "barrelBot2"]
    ]
  },
  "bunker": {
    "why": "Mole.cs RPC_bunker (:25102-25640), Bunker rank 2 (myCommand bunker2: damage taken x 0.25, CharacterControl.cs:4636-4672; no look change): clip cut in (PlayAnimation(bunker, 0), Once, :25334-25339), voice bunker1 / bunker2 (Random.Range(0, 2) :25383-25438) and Effects/bunker_hole at the hero, hero rotation (createEffect :25451-25469; EffectControl life 1, followPosition) at 0; Yield 0.2 (:25601): Effects/bunker at the hero (createEffect :25248-25266; life 999, followPosition, followState; the sandbag ring mesh Mole_bunker, its dust ring and puff; plays its own Sounds/bunker), Race = Structure (:25280); Yield 0.3 (:25589): held until a move key (:25485-25542; RPC_bunker0 :10954-10993 standby): the SEQ Bunker's 3 s (the run-until-the-player-moves rule), cut 2.95",
    "cues": [
      [0, "voice", "bunker1|bunker2"],
      [0, "fx", "bunker_hole"],
      [0.2, "fx", "bunker", {"cut": 2.95}]
    ]
  },
  "chopper": {
    "why": "Mole.cs RPC_chopper (:33450-34186), Chopper rank 3, Barrel Cannon #443 on (passives on): clip (0.2 fade, Once, :34028-34031) and voice chopper1 / chopper2 (Random.Range(0, 2) :34069-34169) at 0; Yield 0.3 (:34172): the Mole prefab's Mole_chopper field (= Effects/chopper, checks/fx_mole_research/skills_a/probe/fields.txt) created at the origin, parented to Mole_tri/root/UpperBody1/UpperBody2/mount_Cannon, localPosition 0, localRotation identity (:33589-33604; EffectControl life 5.5, followState; Animation root; its AudioSource chopper, loop, playOnAwake off); Yield 0.2 (:34167): chopper_startDust (= Effects/chopper_StartDust) at the hero, Quaternion.identity (:33631); Yield 0.2 (:34157): at 0.7 s moveSpeed 3 and the chopper's AudioSource Play() (:33658-33663: playAudio 0.4 after its spawn); Yield 0.6 (:34151): at 1.3 s moveSpeed 5 + 3 (:33690), hasSkill(443) (:33695): choppperCannon_ring at the hero, hero rotation (createEffect :33701-33719; life 4, followPosition; plays its own looping Sounds/chopperCannon_ring); ten ticks 0.4 s apart from 1.3 s (i >= 10 :33794, Yield 0.4 :34160): chopper_forwardDust (= Effects/chopper_forwardDust) at the hero, hero rotation (:33877); each tick's 3 m box (:33890) and #443's 5 m blast (:33957-33986) hit nothing at the standing hero (the hero does not travel; chopper_hit only on a hit, :33929); at 5.3 s the chopper's sound Stop and standby (:33800-33868): the chopper cut at 5.15, the clip's 5.2 s end less the page's margin",
    "cues": [
      [0, "voice", "chopper1|chopper2"],
      [0.3, "fx", "chopper", {"bone": "mount_Cannon", "cut": 5.15, "playAudio": 0.4}],
      [0.5, "fx", "chopper_StartDust"],
      [1.3, "fx", "choppperCannon_ring"],
      [1.3, "fx", "chopper_forwardDust"],
      [1.7, "fx", "chopper_forwardDust"],
      [2.1, "fx", "chopper_forwardDust"],
      [2.5, "fx", "chopper_forwardDust"],
      [2.9, "fx", "chopper_forwardDust"],
      [3.3, "fx", "chopper_forwardDust"],
      [3.7, "fx", "chopper_forwardDust"],
      [4.1, "fx", "chopper_forwardDust"],
      [4.5, "fx", "chopper_forwardDust"],
      [4.9, "fx", "chopper_forwardDust"]
    ]
  },
  "detonate": {
    "why": "Mole.cs RPC_detonate (:30961-31490), Detonate #273 (one rank; doSkill refuses it with no Time Nuke, :6740-6762: the tile assumes Time Nuke 2's nuke where the Time Nuke tile puts it, mPos + tDir = 1 m ahead, identity, RPC_timeNuke :30653, RPC_timeNuke_create :11663-11730): clip (0.2 fade, Once, :31277-31280), voice detonate1 / detonate2 (Random.Range(0, 2) :31318-31373) and Effects/detonate_ring at the hero, hero rotation (createEffect :31386-31404; life 1.5, followPosition; plays its own Sounds/detonate) at 0; the local player's motion blur (:31430-31433) left out; Yield 0.6 (:31458): each nuke sent detonate (:31096-31148) and Effects/detonate Instantiated at it, identity (:31107-31171; life 1); Mole_timeNuke.detonate (Mole_timeNuke.cs:407-523): renderers on, Yield 0.5, doExplode (:615-921): timeNuke_explosion (the prefab's field = Effects/timeNuke_explosion, probe/nukefield.txt) at the nuke, its rotation (:796; life 4; plays its own Sounds/timeNuke), the nuke's renderers off and Destroyed after four 0.1 s rings (:801-911); Yield 0.7 (:31462): standby at 1.3 s",
    "cues": [
      [0, "voice", "detonate1|detonate2"],
      [0, "fx", "detonate_ring"],
      [0, "fx", "timeNuke2", {"d": 1, "kill": 1.1}],
      [0.6, "fx", "detonate", {"d": 1}],
      [1.1, "fx", "timeNuke_explosion", {"d": 1}]
    ]
  },
  "dig1": {
    "why": "dig1 is King Kaiser's (RPC_kingKaiser :35389; Charge Attack plays superDig instead with Super Dig #411 on, :22290-22304, the passives rule): Mole.cs RPC_kingKaiser (:34990-35530), King Kaiser #371 (one rank; Kaiser Cannon #372 / Kaiser Beam #373 on: Kaiser level 3, the Kaiser's attacks only): clip (0.2 fade, Once, :35389-35392; held on its last frame, the SEQ's dig1@4.9), noForce 5 s (:35401, nothing drawn), the camera zoom (:35420) left out, Effects/dig_hole at the hero 0.05 m up, hero rotation (Instantiate :35426-35444; EffectControl life 5, Animation root; its digSound child plays the looping Sounds/dig for 2 s) at 0; every 0.1 s on the frame loop (dustTimer :35321-35329, 0.117 s at 60 fps) until actionTime + 1.9 (:35293): Effects/dig_dust at the hero, hero rotation (:35334-35352; life 1); Yield 0.5 (:35487): at 2.4 s the Mole prefab's kaiser_dust field (sharedassets8.assets path 387, not in Resources; probe2.json: four smoke puffs at (+-1.5, 0, +-1), life 1 + 1) at the hero, hero rotation (:35127-35133; the camera shake left out); Yield 0.5 (:35496): at 2.9 s the kaiser_box field (path 379; life 3, Animation root, the KaiserBox mesh; plays its own kaiser_box) at the hero, rotation x Euler(270, 90, 0) (:35186-35192); Yield 2 (:35494): at 4.9 s the Kaiser (@KingKaiser:root)",
    "cues": [
      [0, "fx", "dig_hole", {"y": 0.05}],
      [0.12, "fx", "dig_dust"],
      [0.23, "fx", "dig_dust"],
      [0.35, "fx", "dig_dust"],
      [0.47, "fx", "dig_dust"],
      [0.58, "fx", "dig_dust"],
      [0.7, "fx", "dig_dust"],
      [0.82, "fx", "dig_dust"],
      [0.93, "fx", "dig_dust"],
      [1.05, "fx", "dig_dust"],
      [1.17, "fx", "dig_dust"],
      [1.28, "fx", "dig_dust"],
      [1.4, "fx", "dig_dust"],
      [1.52, "fx", "dig_dust"],
      [1.63, "fx", "dig_dust"],
      [1.75, "fx", "dig_dust"],
      [1.87, "fx", "dig_dust"],
      [2.4, "fx", "kaiser_dust"],
      [2.9, "fx", "kaiser_box", {"rot": [270, 90, 0]}]
    ]
  },
  "@KingKaiser:root": {
    "why": "Mole.cs RPC_kingKaiser at 4.9 s (case 5 :35210-35277): kaiser_dust again at the hero (:35229-35235), RPC_kingKaiser_create at getExpandPos(position, 4, 1.2) (:35270; the hero's spot when it is free), LookRotation(forward) (:35536-36204): Characters/Robots/KingKaiser/KingKaiser_<r g b k w p> by the outfit colour (Skin / 100 = 1-5, else p, :35709-35776), KingKaiser.summon (KingKaiser.cs:3821-4048: create once and its kaiser_createFx, 3 s to standby, then root), voice kingKaiser1 / kingKaiser2 (Random.Range(0, 2) :36057-36112), the Mole hidden (addStatus hide, chaAdjust(240) :36135) and carried with the Kaiser for 240 s: cut at 10 s (the Kaiser and the hide, 9.95 inside the step); the colour ramp and motion blur (:36012-36017) left out",
    "cues": [
      [0, "fx", "kaiser_dust"],
      [0, "voice", "kingKaiser1|kingKaiser2"],
      [0, "fx", "KingKaiser", {"kill": 9.95, "hideHero": true}]
    ]
  },
  "flameTurret1": {
    "why": "Mole.cs RPC_flameTurret (:27714-28415), Flame Turret rank 3 (damage only): clip cut in (PlayAnimation(flameTurret1, 0), Once, :28234-28237), voice flameTurret1 / flameTurret2 (Random.Range(0, 2) :28275-28330) and Effects/flameTurret at the hero, hero rotation (createEffect :28343-28359; EffectControl life 60, followPosition, followState, rotation mode followObject; the turret Mole_frameTurret's create / root, a puff, a dust ring; plays its own Sounds/bunker) at 0; Yield 0.5 (:28396): flameTurret2; the channel ends at actionTime + chaAdjust(5) (:27935, :27984: 5 s at the stat-free CHA 1; the SEQ's flameTurret2*@4.5): the turret's followState cut 4.45 on flameTurret2's clock",
    "cues": [
      [0, "voice", "flameTurret1|flameTurret2"],
      [0, "fx", "flameTurret", {"cut": 4.45}]
    ]
  },
  "flameTurret2": {
    "why": "Mole.cs RPC_flameTurret from 0.5 s: flameTurret2 cut in and looped (:27861-27866); Yield 0.5 (:28392): at 1.0 s (0.5 into this step) Effects/flameTurret_fire at the hero, hero rotation (createEffect :27893-27911; life 5, followPosition, followState, followObject; the flames 1.5 m ahead; plays its own looping Sounds/fireTurret), the damage box every 0.25 s from 1.25 s (FindRecTarget 12 m :28144-28200, nothing drawn); turning by the arrow keys (RPC_flameTurret_rotate :28078-28130) left out; standby at 5 s (:27984-28028): cut 4.45 (the step's 4.5 s less the page's margin)",
    "cues": [
      [0.5, "fx", "flameTurret_fire", {"cut": 4.45}]
    ]
  }
}
```

## Parts summary

| part | what | for |
|---|---|---|
| P1 robot summons | Extractor: ALIASES, data layouts for AutoGyroGun / BarrelBot / BarrelBotAI / KingKaiser, and the KingKaiser clips' compressed / float curves. Page (`fxparts/mole.js`): AutoGyroGun (create, root, AI shots at `to` every 2 s from 2 s with autoGyroGun_fire + nAttack_fx), BarrelBot (getUp, root), KingKaiser (outfit colour, create 3 s, root, `hideHero`) | Auto Gyro Gun, Barrel Bot, King Kaiser |
| P2 prefab-field effects | load kaiser_dust / kaiser_box from the Mole prefab's fields; kaiser_box.wav from Assets/AudioClip | King Kaiser |
| P3 `playAudio` | cue option: the root AudioSource's Play() at that age (index.html + OPTS) | Chopper |
| P4 Mole_timeNuke | layout (mLv i, isVisible b, timeNuke_explosion r); shared with skills_b | Detonate |
| P5 warCapital | `SHURIKEN_FROM_TTO["mole"] = ["warCapital"]`; Mole_warCapital: open, then root after 1 s; CharacterControl data only | War Capital |

Inventory: add Mole_timeNuke and Mole_warCapital to BUILT once P4 / P5 exist. The robots load through ALIASES.

## Bible findings to offer the user

- advanceRepair_ring and barrelCannon_ring are loaded by both BB and TTO but exist in neither game's data, so both skills draw no ring (Mole.cs:36840, :40226).
- War Capital's first salvo comes 12 s after it is built (:43912). With no enemy near it rechecks every 6 s (:43919), and after a salvo it waits 24 s (:43887). The reference says only "every 24 s".
- War Capital's assemble time can never drop below 8 s: magAdjust removes at most 16 s.
- Advance Repair's first heal tick is 1 s in (:36459, :36881).
- Chopper: the ticks run 0.4 s apart from 1.3 s; it flies at 3 m/s from 0.7 s and at 5 + sLv m/s from 1.3 s.

## Open questions (recommended answers)

1. **Show the summons?** These are Auto Gyro Gun's turret, Barrel Bot's bot, War Capital's base and King Kaiser's robot. Recommended: yes, build them (P1, P5; the precedent is the Bat's Guardian of the Night, decisions 24-25), each cut at 10 s. Auto Gyro Gun's AI should fire at the 10 m target as the code does: the first shot about 2 s after the create, then every 2 s.
2. **War Capital's cast bar:** 8 s at the highest MAG, on its own tile? Recommended: yes, 8 s. It cannot reach 0, and it is not a long buff, so the 10 s rule does not apply.
3. **Barrel Bot's AI** (it runs to the target and fights with six weapons, BarrelBotAI.cs:945-1215)? Recommended: keep it standing (getUp, then root) for 10 s. Offer the AI to the user as a separate job.
4. **Barrel Cannon without a bot:** clip + voice only, or Double Bot's two bots in cannon form? Recommended: clip + voice now, since that is the game's own no-bot look. The cannon form can come after P1's BarrelBot and its cannon shell (BarrelBot_cannon, cannon_fire / cannon_hit).
5. **Detonate:** assume Time Nuke 2's nuke 1 m ahead? Recommended: yes, because the skill cannot be cast without one. If P4 is late, drop the `timeNuke2` cue and keep the rest.
6. **King Kaiser's robot:** build it (create, root, the outfit colour, the Mole hidden for 10 s)? Recommended: yes (P1; the Penguin's Snow Man precedent, decision 17). The colour comes from the worn outfit's colour number: 1 r, 2 g, 3 b, 4 k, 5 w, otherwise p.
7. **dig2:** hide it with NEVER_PLAYED? Recommended: yes, and tell the user.
8. **Flame Turret's length:** 5 s (flameTurret2*@4.5) instead of the page's 3 s? Recommended: 4.5. Channels use their base duration (the Bat precedent); chaAdjust only lengthens it, up to 43 s at CHA 512.
9. **Bunker:** "Bunker: bunker@3"? Recommended: yes. Bunker and flameTurret1 cut in in the game, but the page's first-step fade stays (Cat decision 2).
10. **Chopper hit:** in the game the flying Mole would hit a target 10 m ahead at the third tick (2.1 s). Recommended: leave it out, since the hero does not travel (the Bison's Instant Rush).
11. **The missing rings:** add a stand-in? Recommended: no. Offer the finding for the Bible.
12. **Barrel Railgun's opening (TTO, released):** the game opens with assemble1 and a 5.4 s assemble2, not with barrelRailgun1. Recommended: the tto report changes the page line to start with `assemble1@0.6 assemble2*@5.4`, using the two `@BarrelRailgun:` cue keys above. This report supplies the data; the tto report owns the sequence.

## Verification (2026-11-13)

A read-only re-trace by the checker. My dumps and probes are in `checks\fx_mole_research\verify\`: `RPC_assemble1.txt`, `RPC_advanceRepair.txt`, `RPC_bunker.txt`, `RPC_chopper.txt`, `RPC_detonate.txt`, `RPC_flameTurret.txt` and `RPC_kingKaiser.txt` (clip_flow.js), `list_fx.py` -> `list_fx.txt` (the BB container's heroes/mole/effects and the robot prefabs) and `parse_blocks.py` (the block against wardrobe_fx_check.py's KINDS / OPTS).

**Checked and confirmed.** I followed every case from its PlayAnimation and summed the waits. The opaque predicates on these paths were evaluated by hand (for example :11888, :12300, Math.cs:1212-1235); each goes the normal way.
- **Advance Repair:** clip 0.2 s fade, Loop (:36725-36728). Voice advanceRepair1 / advanceRepair2 (:36766-36821). Effects/advanceRepair_ring at :36840 and createEffect :36850, with the "Cannot find" log at :36859. The first tick comes after Yield(2, 1) (:36881).
- **Assemble:**
  - assemble1 with a 0.2 s fade (:23438) and voice cast (:23485, :23533), then Yield 0.6 (:23527).
  - Case 2 (:23046-23125): assemble2 cut in and looped, assemble_box at the hero with its rotation (createEffect :23098), assembleTime = now + magAdjust.
  - The casts: autoGyroGun 1 + sLv, barrelBot 3 + sLv, warCapital 24 (IL_225).
  - magAdjust (CharacterControl.cs:20584-20588): clamp(t - floor(MAG'/32), 0.1, 600). At MAG 512 that is 0.1 / 0.1 / 8 s. At MAG 1 it would be the full 5 / 7 / 24 s. The page's cast-bar convention is the floor (Bat decision 29), so these hold.
  - At the bar's end: RPC_assemble0 (standby, :10477-10504) and the create RPC (:23163-23316). The box is Destroyed a frame later (:23331).
  - getSpawnVector (Math.cs:1210-1237): a 4 m ray from 1 m up. It meets the floor at 0.7 m along 0.7 forward - up, and at 2 m along 2 forward - up.
  - autoGyroGun adds getExpandPos(…, 1, 0.3), which is a no-op on open ground.
- **The creates:**
  - Auto Gyro Gun: assemble_dust at position + 0.7 forward (:11776), voice autoGyroGun1 / autoGyroGun2 (:11819-11874), AutoGyroGun4 at tPos with LookRotation(tDir) (:12019-12031).
  - Barrel Bot: assemble_dust at position + forward (:12304), BarrelBot4 (:12589-12601).
  - War Capital: the old one Destroyed, Effects/warCapital at tPos with LookRotation(tDir), voice laugh (:14245-14345). The first scan is now + 12 (:43912) and the post-salvo wait 24 s (:43887), so no missile comes within 10 s.
- **Barrel Cannon:** clip 0.2 s fade (:40208), barrelCannon_ring Load (:40226) with its "Cannot find" log (:40246), voice barrelBot2 (one file, :40287, :40320). Then Yield 0.3 (:40325) and Yield 0.5 (:40327), so standby is at 0.8.
- **Missing rings:** neither ring is in BB's container (list_fx.txt: 105 Mole effects, neither name), nor in TTO's catalog (skills_a\probe\probe_tto.err).
- **Bunker:** clip cut in (:25334), voice bunker1 / bunker2 (:25383-25438), bunker_hole (:25469). Yield 0.2 (:25601), then bunker (:25266) and Race = Structure (:25280). The probe: bunker EC life 999, followPosition, followState, its own bunker sound.
- **Chopper:** I re-ran the case chain:
  - 0.3 s: the chopper on mount_Cannon, local 0 / identity (:33589-33604).
  - 0.5: StartDust with identity rotation (:33631).
  - 0.7: moveSpeed 3 and audio.Play (:33658-33663).
  - 1.3: 5 + 3 and choppperCannon_ring (#443, :33695-33719).
  - Ticks at 1.3 + 0.4k for k = 0-9; at 5.3 audio.Stop and standby (:33794-33868). The labels Block_43 / Block_32 / Block_50 / IL_C11 are at :34135-34172.
  - mount_Cannon is in data/mole/rig.json.
- **Detonate:**
  - Clip 0.2 s fade (:31277), voice detonate1 / detonate2 (:31318-31373), detonate_ring (:31404).
  - Yield 0.6: each nuke gets SendMessage(detonate) and Effects/detonate at it, identity (:31096-31171).
  - Mole_timeNuke.detonate (Mole_timeNuke.cs:407-523): renderers on, then Yield 0.5. doExplode (:615-921) spawns timeNuke_explosion at once with the nuke's rotation (:796), the nuke's renderers off, and Destroy after the 0.1 s rings.
  - Yield 0.7 (:31462): standby at 1.3.
  - Time Nuke's spot: RPC_timeNuke(position, forward) (:8306) -> RPC_timeNuke_create(mPos + tDir), identity (:11655-11730), so 1 m ahead. The owner sees the nuke: Init hides it only from the other side (Mole_timeNuke.cs:42-110).
- **King Kaiser:**
  - dig1 with a 0.2 s fade, noForce 5 s (no look, CharacterControl.cs:2266), the camera zoom, dig_hole 0.05 m up (IL_A46 :35371-35444).
  - dig_dust whenever Time > dustTimer, which is re-armed + 0.1 (IL_6D7 :35292-35364), until actionTime + 1.9. Then Yield 0.5: kaiser_dust (case 3, :35133). Then Yield 0.5: kaiser_box × Euler(270, 90, 0) (case 4, :35192). Then Yield 2: case 5 at 4.9, kaiser_dust and the create (:35210-35277).
  - The colour pick is Math.div(Skin, 100) (:35709-35776). MoleEquipment.cs:1495-1500 confirms that Skin / 100 is the armour colour number.
  - The create at once: the Instantiate (:35794), summon (:35995), voice kingKaiser1 / kingKaiser2 (:36057-36112), the hide status (:36135), which switches every renderer off (CharacterControl.cs:32818-32830).
  - The 60 fps dust list (16 puffs at 0.117 k) is right.
- **Flame Turret:**
  - flameTurret1 cut in, with actionTime set at the start (IL_855 :28215-28237). Voice flameTurret1 / flameTurret2 (:28275-28330) and flameTurret (:28359), then Yield 0.5 (:28396).
  - Case 2: flameTurret2 cut in and looped, then Yield 0.5 (Block_67 :28392).
  - Case 3: flameTurret_fire (:27911) and mDuration = chaAdjust(5) = 5 at CHA 1. Standby at actionTime + 5 (:27984-28028).
  - The turret's `cut` 4.45, written on flameTurret2's clock, works on the page as it is today. fxStart leaves a followState cut that lies past the ending step alone (index.html:5070-5082, "a cut written in a later step's clock ... is left as it was"). Fx.update then cuts it at FX.t >= 4.45 in flameTurret2 (:4188), at 4.95 s on the tile.
- **dig2:** only the loader names it (Mole.cs:709); TTO's pseudo/Mole.c has 0 hits.
- **Probe facts** (skills_a\probe\summary.txt): assemble_box (EC 999, followState, looping assemble), warCapital (Animation open / root / close, its sound), chopper (EC 5.5, followState), choppperCannon_ring (EC 4, its looping sound), detonate_ring (EC 1.5), flameTurret (EC 60, followState, Animation create / root), flameTurret_fire (EC 5, the looping fireTurret).
- **Voices:** every cued voice is in BB's rip (attacks_emotes\rip_audio.txt, lower-cased).
- **The block:** it parses and every time list is in order. The only option the check does not know yet is `playAudio`, as P3 says.

**Corrections:**
1. **KingKaiser_p does not exist in BB's data.** The container has only KingKaiser_b, _g, _k, _r and _w (verify\list_fx.txt; parts.md:83-84 says the same). So the code's else branch (:35776) summons nothing in BB, not a "p" Kaiser. This changes Read this first 3, Q6 and the `@KingKaiser:root` why.
   - Every wardrobe Mole outfit has colours 1-5 (data/mole/outfits.json), so r / g / b / k / w covers them all.
   - The one exception is steamSuit, which has no colour list. The KingKaiser part needs a stated fallback for it, for example the r model or the outfit's default colour. The game would show no Kaiser.
2. **The Kaiser's hiding: use the page's existing whole-hero cue (recommended).** `{"hideHero": true}` on the KingKaiser cue would need code in the new KingKaiser part (as penguin.js does for the Snow Man).
   - `[0, "hideProp", "hero", {"kill": 9.95}]` already does it: index.html fxDue :5186, HeroPropHide :4885-4898, wfxHidden :4901-4906, wardrobe_fx_check.py HIDE_TARGETS :181.
   - It also matches the hide status, which turns off every renderer, the weapon's included.
   - attacks_emotes.md's burrow uses the same cue (its Verification 1).
3. **Inventory.** chopper, chopper_StartDust and chopper_forwardDust (Mole-prefab fields) and timeNuke_explosion (Mole_timeNuke's field) are not in plans/fx_inventory.md "### mole". Like attacks_emotes item 6, they belong in pipeline/wardrobe_fx_inventory.py, as ready field effects: their components are ready by the probe. "What is ready" says "inventory + probe"; for these four it is the probe only.
4. **dig2 versus attacks_emotes.md.** attacks_emotes uses dig2 as the hidden underground step of its Charge Attack and Sky Drill SEQs, with a `dig2` cue entry (dig_dirt). This report's "No cues" yields to that entry.
   - `NEVER_PLAYED.mole = ["dig2"]` is then redundant: a clip a SEQ plays is hidden anyway (index.html:3593). It is harmless and can stay as the record that no code plays it.
   - Tell the user either way (Q7).

**Not re-derived (Bible offer only):** War Capital's "rechecks every 6 s" (:43919). The Yield(4, 6) is there, but I did not trace which branch reaches it. The 12 s first scan and the 24 s post-salvo wait are confirmed. Neither changes a cue.

**For the editor, not a correction:** the chopper's cut 5.15 (the clip's end) rather than the game's 5.3 standby is the safer pick. A looping tile restarts FX.t at 5.2, so a 5.3 cut would come in the next round.

**Corrected paste-ready entry.** Only `@KingKaiser:root` changes: its why, and its hiding as a separate cue. Every other entry in the block above stands as written.

```json
  "@KingKaiser:root": {
    "why": "Mole.cs RPC_kingKaiser at 4.9 s (case 5 :35210-35277): kaiser_dust again at the hero (:35229-35235), RPC_kingKaiser_create at getExpandPos(position, 4, 1.2) (:35270; the hero's spot when it is free), LookRotation(forward) (:35536-36204): Characters/Robots/KingKaiser/KingKaiser_<r g b k w> by the armour colour Skin / 100 = 1-5 (:35709-35776, MoleEquipment.cs:1495-1500; the else branch loads KingKaiser_p, which BB's data does not have: no Kaiser; every wardrobe Mole outfit has colours 1-5, steamSuit none: the part's fallback), KingKaiser.summon (KingKaiser.cs:3821-4048: create once and its kaiser_createFx, 3 s to standby, then root), voice kingKaiser1 / kingKaiser2 (Random.Range(0, 2) :36057-36112), the Mole hidden (addStatus hide, chaAdjust(240) :36135: every renderer off, CharacterControl.cs:32818-32830; the page's whole-hero hideProp) and carried with the Kaiser for 240 s: cut at 10 s (the Kaiser and the hide, 9.95 inside the step); the colour ramp and motion blur (:36012-36017) left out",
    "cues": [
      [0, "fx", "kaiser_dust"],
      [0, "voice", "kingKaiser1|kingKaiser2"],
      [0, "fx", "KingKaiser", {"kill": 9.95}],
      [0, "hideProp", "hero", {"kill": 9.95}]
    ]
  },
```

**P1 after these corrections:** the KingKaiser part no longer hides the hero itself. It picks the r / g / b / k / w model by the outfit colour, with a fallback for an outfit with no colour number.
