# Panda: the skills with no body animation (effect-only tiles)

Research only (2026-11-13, office PC). I worked read-only: I wrote this report and files under
`checks/fx_panda_research/effect_only/` (git-ignored) and nothing else.

**What was run:**
- The probe, with `--probe` only (exit 0 both times): `uv run --no-project --with UnityPy python -I pipeline/wardrobe_fx.py
  panda --probe sacredSage_ring,heavenBreath_ring,mysticSage_hit,safeGuard_hit,delayQi_ring,delayQi,delayQi_fire`
  (`probe.json`) and `... --probe cAttack_ring,auraField_ring,qiStrike_ring` (`probe2.json`). `sacredSage_ring` and
  `heavenBreath_ring` came back `KeyError`: not in the BB rip.
- `wardrobe_fx_tto.py panda --probe sacredSage_ring,heavenBreath_ring,...` (exit 1: "not in TTO's catalog under
  gameassets/characters/heroes/panda/effects/: ['heavenBreath_ring', 'sacredSage_ring']"; `tto_probe.err`).
- `node pipeline/clip_calls.js C:/Users/Jump/Desktop/12tails/DecompiledSource wardrobe/data panda`, and
  `pipeline/clip_flow.js` on RPC_windCloud, RPC_rainStorm, RPC_delayQi, RPC_cAttack1, RPC_qiStrike1, RPC_qiStrike2
  (`flow_*.txt`).
- Helpers: `loads.py` -> `loads.txt` (all 160 `Heroes/Panda/(Effects|Voices|Sounds)` loads in Panda.cs, each with the
  method or coroutine class that holds it); `pred.py` (each junk predicate in a line range, evaluated T/F); `bb_rpc.txt`,
  `tto_rpc.txt`, `groups.txt` (the RPC accounting, diffed against the listing: the same 84); `cues.json` (the cue
  entries below, checked with `json.load`); the rip's wav lengths, measured with Python's `wave`.

**Sources:** `C:\Users\Jump\Desktop\12tails\DecompiledSource\Panda.cs` (cited as `:line`), `CharacterControl.cs`,
`EffectControl.cs`; the TTO `DecompiledSource_TTO_2026-11-02\methods.tsv` and `pseudo\Panda.c`; the Bible's
`12t_reference/panda-skill-reference.md` and the skill cards in `12t_projects/bible/index.html` (:19219-19324) and
`assets.js`; `plans/fx_inventory.md` ("### panda"); `wardrobe/data/panda/clips.json`. The templates were the Mole's and
the Chameleon's effect_only.md.

## Read this first

1. **No Panda active is effect-only.** The dispatcher (`doSkill`, :5585-8165) starts a coroutine for every `pnd_*`
   active (:6151-7486), and every one of them plays a body clip. `clip_calls.js` finds 40 of them. It misses two
   because their names contain `&`: `RPC_windCloud` plays `PlayAnimation("wind&cloud", 0.2)` (:37811) and
   `RPC_rainStorm` plays `PlayAnimation("rain&storm", 0.2)` (:38839).
2. **Four skills draw their look from an RPC that plays no skill clip of its own.** All four are passives:

   | Tile (Bible name) | Bible icon | Code | What it shows | Tile shape |
   |---|---|---|---|---|
   | **Mystic Sage** | `panda_mysticSage2` | `RPC_mysticSage_hit` :9570, called from AddDamage (CharacterControl.cs:32115) | `mysticSage_hit` (the double) + voice `mysticSage` | effect-only, `root*@1` |
   | **Safe Guard** | `panda_safeGuard5` | `RPC_safeGuard_hit` :9721, through ActionEvent from RPC_AddStatus (CharacterControl.cs:13503) | `safeGuard_hit` | effect-only, `root*@1` |
   | **Sacred Sage Technique** | `panda_sacredSageTechnique2` | `RPC_sacredSage` :9211, called from the Charge Attack's tick (:19236) | voice `sacredSage1|2` only (its ring is missing from the game data, item 5) | its own tile on the charge's clips |
   | **Delay Qi** | `panda_delayQi1` | `RPC_delayQi` :8549 (coroutine :23981), started from Qi Strike's charge end (:23042) | `delayQi_ring`, the `delayQi` status glow, `delayQi_fire` at the release | its own tile: `qiStrike1`, then **`root`** (its own CrossFade, :24246), then `qiStrike2` |

   Mystic Sage and Safe Guard follow the Penguin's Frost Spike shape: a proc set off by being hit, shown on the idle
   stance on every play. Sacred Sage follows the Chameleon's Critical Plus shape: a passive with its own RPC, riding
   another skill's clip, gets a tile on that clip. Delay Qi's middle step *is* the idle clip (the game cross-fades to
   `root`), so it gets an `@DelayQi:root` cue entry like any effect-only tile, between Qi Strike's two clips.
3. **Every effect these tiles need is already buildable** (probe; inventory "ready" for mysticSage_hit, safeGuard_hit,
   delayQi_ring, delayQi_fire, qiBurst, cAttack_ring, auraField_ring, qiStrike_ring). The status glow `delayQi`
   (loaded from CharacterControl.cs:35342, so it is not in the inventory) is one LineEmitter, a part the page has. **No
   page part is missing.**
4. **A data gap, not mine to fix (flagged for the lead / the clip researchers): the Wind & Cloud and Rain & Storm clips
   are not on the page.** `wardrobe/data/panda/clips.json` has no `wind&cloud` or `rain&storm`, although the rip has
   both (`.../heroes/panda/animations/wind&cloud.prefab`, `rain&storm.prefab`). The cause is the clip filter in
   `pipeline/wardrobe_data.py:210`, `re.fullmatch(rf".*heroes/{cls}/animations/[a-z0-9_]+", x)`, which drops any name
   with `&`. Those two skills cannot get tiles until the data build admits `&` (and the page's clip / file names are
   checked with it). That build reads the game rips, so it runs at the home PC. Neither skill is effect-only.
5. **Sacred Sage's ring is missing from the game itself.** `RPC_sacredSage` loads `Effects/sacredSage_ring` (:9397) or,
   with Heaven Breath, `Effects/heavenBreath_ring` (:9345). Neither prefab is in the BB rip or TTO's catalog, so the
   game logs "Cannot find ... effect" (:9365, :9417) and goes on to the heal. TTO's code is the same
   (`pseudo/Panda.c:38901-38936`, both strings). The tile therefore has the voice only (open question 2).
6. **TTO:** TTO adds `RPC_nineDragons`, `RPC_tempestDance`, `RPC_tempestDanceEnd`, `RPC_yinYangFist` (all with clips,
   all in `tto_released.json`) and `RPC_tempestCounter`: Tempest Dance's counter on an evade (Bible :1154; action code
   `tempestCounter`, `pseudo/Panda.c:30419`). That counter is a phase of a clip skill and needs an attacker, so it
   belongs to the TTO researcher. No TTO skill is effect-only.
7. `wardrobe/fx_cues/panda.json` is `{}` today, so no key here collides with an existing one.

## Accounting: every RPC_* in Panda.cs (84 definitions)

I listed them with `grep -nE "^\s*(public|private|protected|internal)[^(]*\bRPC_\w+\(" Panda.cs`, which gives 84.
`groups.txt` puts each one in one group, and a diff against the listing gives the same 84: 6 + 3 + 29 + 18 + 4 + 13 +
11 = **84**. "Clip" is the body clip the RPC (or the coroutine it starts) plays (clip_calls.js, plus the two `&`
names). "Covered by" names the report that owns it: **attacks** (attacks_emotes), **skills** (skills_a / skills_b, the
clip researchers), **tto**, or **this report**.

| RPC (line) | Skill | Clip | Covered by |
|---|---|---|---|
| nAttack1-5 (:7959-7987) | Normal Attack (combo stages) | nAttack1-5 | attacks |
| nAttack1_hit :7994, nAttack2_hit :8080 | its hits | none (phase) | attacks |
| cAttack1 :8364 | Charge Attack (and Aura Field, Sacred Sage's tick inside it) | cAttack1, cAttack2 loop | attacks (Sacred Sage's own tile: this report) |
| cAttack0 :8371 | the charge's release / cancel | none (standby) | attacks |
| roll :8378 | Roll | roll | skills |
| rollAround :8385 | Roll Around | rollAround | skills |
| threeStep :8392 (+ _hit :8399) | Three Steps (Nine Steps inside) | threeSteps | skills |
| rushingFalcon :8442 (+ _hit :8449) | Rushing Falcon | rushingFalcon | skills |
| qiStrike1 :8492, qiStrike2 :8499 (+ qiStrike_hit :8506) | Qi Strike (Qi Burst inside) | qiStrike1, qiStrike2 | skills (Delay Qi's tile reuses them: this report) |
| **delayQi :8549** | **Delay Qi** | **root** (CrossFade, :24246) | **this report** |
| pummel :8556 (+ _hit :8563) | Pummel (Ogre Impact inside) | pummel | skills |
| towerRush :8606 (+ _hit :8613) | Tower Rush (Ogre Impact inside) | towerRush | skills |
| grab :8656 | Tiger Toss's grapple | grab | skills |
| tigerToss :8663 (+ tigerPounce_hit :8677) | Tiger Toss, Tiger Pounce | tigerToss | skills |
| climbingCliff :8727 (+ _hit :8734) | Climbing Cliff | climbingCliff | skills |
| crumblingMountain :8784 (+ crushingMonolith_hit :9768, called :28203 / :28214) | Crumbling Mountain, Crushing Monolith | crumblingMountain | skills |
| risingVortex :8862 (+ _hit :8869) | Rising Vortex | risingVortex | skills |
| risingDragons :8912 (+ risingDragon_hit :8919) | Rising Dragons | risingDragons | skills |
| ashura :8990 | Ashura | ashura | skills |
| ashuraFist :8997 | Ashura Fist (the charge under ashura) | ashuraFist | skills |
| drunkenFist :9004 | Drunken Fist (Drunken Plus / Spin inside) | drunkenFist | skills |
| waterMonkey :9018 (+ _hit :9025) | Water Monkey (Time and Tide inside) | waterMonkey | skills |
| waterCrane :9068 (+ _hit :9075) | Water Crane (Time and Tide inside) | waterCrane | skills |
| stasisBlow :9118 (+ _hit :9125) | Stasis Blow | stasisBlow | skills |
| deathBlow :9131 (+ _hit :9138) | Death Blow | stasisBlow (:35430) | skills |
| spTransfer :9204 | Sp Transfer | spTransfer | skills |
| **sacredSage :9211** | **Sacred Sage Technique** (Heaven Breath inside) | none (inside the charge's cAttack2) | **this report** |
| windCloud :9445 | Wind & Cloud | `wind&cloud` (:37811), **not in clips.json** | skills (item 4) |
| rainStorm :9452 | Rain & Storm | `rain&storm` (:38839), **not in clips.json** | skills (item 4) |
| lotusPalm :9459 (+ _hit :9466) | Lotus Palm | lotusPalm | skills |
| heavenPalm :9509 (+ _hit :9516) | Heaven Palm | heavenPalm | skills |
| **mysticSage_hit :9570** | **Mystic Sage** | **none** | **this report** |
| **safeGuard_hit :9721** | **Safe Guard** | **none** | **this report** |
| comboLink :9811 | Combo Link | comboLink | skills |
| fuujinKen :9818 (+ _hit :9825) | Fuujin Ken | fujinKen1-3 | skills |
| raijinKen :9868 (+ _hit :9875) | Raijin Ken | cAttack1, cAttack2, raijinKen1-2 | skills |
| obsidianFang :9939 / _hit :9946, stunningGround :9989, psalmOfEnergy :10229, seaAegis :10399, assassinate :10586, zephyrLore :10593, mineWalker :10687, replenishment :10694, elementalBound :10823, divineChannel :10969, astralShift :10976, bloodCarnage :11167 (13) | the shared support skills (`sup_*`, dispatched :6292-6578) | none | none: left out (the Bible leaves them out of the Panda's roster, reference "Notes on judgment calls"; the Penguin's / Mole's reports) |
| emotion :11514, emotion0 :11521 | emotes | the emote clips | attacks |
| useItem :11961, useMount :12018, useCoin :12071, petEffect :14265 | items, mount, coin, pet | (shared) | none (every class's) |
| activateIcon1 :14303, activateIcon2 :14310 | the mission | cast2 loop / standby | none (Penguin decision 19) |
| ko :14350, dead :14357, revive :14364 | KO / death | ko, dead, getUp | attacks |

Group counts: attacks 6 (nAttack1-5, cAttack1), their phases 3, skills 29 (with qiStrike2), skill phases 18, this
report 4, supports 13, shared 11.

**Cross-check by loads (`loads.txt`).** Every literal Panda Effects / Voices / Sounds load in Panda.cs sits inside one
of the RPCs above, or `onSupport` (:9909, `Voices/support`). None sits in `Update` (:121) or the dispatcher. Update calls
only the shared gear updates (:156-192), the items' `blackServant` / `autoLife` (:251-329) and the KO / death checks
(:349, :413). CharacterControl.cs loads five more Panda effects, all statuses: `delayQi` :35342 (this report), `drunken`
:35396 (Drunken Plus, in Drunken Fist), `paralysis` :35443 (Stasis Blow's target), `ashura` :35500 (Ashura), `drunk`
:35535 (Drunken Spin's target).

## The passives, each one checked

| Passive (Bible card) | Where it runs | Draws on the Panda? | Tile? |
|---|---|---|---|
| **Mystic Sage** #371/372 | AddDamage, on a hit of more than 100 at full SP (CharacterControl.cs:31986-32133) | `mysticSage_hit` + voice | **yes, effect-only** |
| **Safe Guard** #431 | RPC_AddStatus, on a debuff (CharacterControl.cs:13465-13505) | `safeGuard_hit` | **yes, effect-only** |
| **Sacred Sage Technique** #343/344 | the Charge Attack's 1 s tick (:19140-19250) | voice (the ring is missing in the game data) | **yes, on the charge's clips** |
| **Delay Qi** #214 | Qi Strike's charge end (:23036) | delayQi_ring, the status glow, delayQi_fire | **yes, its own sequence** |
| Heaven Breath #443 | inside Sacred Sage (:9335-9380) and Sp Transfer (:36329) | only the missing `heavenBreath_ring` and bigger heals | no: on inside those two (as the Cat's Lady Luck, the Bison's Rage Control) |
| Aura Field #411 | the charge's case 2 (:19084) and tick (:19257-19318) | `auraField_ring` | no (the Charge Attack's; also on in the Sacred Sage tile) |
| Aura Blast #401 | nAttack5 (:18291-18450) | `auraBlast` + voices | no (attacks) |
| Qi Burst #412 | qiStrike2 (:23786-23810), the hold +3 s | `qiBurst` | no (Qi Strike's; on in Delay Qi's tile) |
| Ogre Impact #422, Nine Steps #402, Drunken Plus #303/304, Drunken Spin #403, Time and Tide #413, Wind Walker #423, Tiger Pounce #232, Crushing Monolith #432, Spirit Fist #433 | inside skills with clips (loads.txt: pummel_ogre, towerRush_ogre, nineStep voices, the `drunken` status, drunkenSpin, timeAndTide*, tigerPounce_hit, crushingMonolith / _hit, radii) | in those skills' cues | no (skills) |
| Combo Plus #241-244 | `RPC_AddStatus("comboPlus")` on every landed hit (:8820-8848) | nothing (no effect load anywhere for comboPlus) | no |
| Shadow Fist #331-334 | `ShadowFist(target)`, effect damage (:9144-9192) | nothing (no effect load in it) | no |
| Resistance #131-134 | RPC_AddStatus (CharacterControl.cs:13512) | only the −83 damage-number popup (`RPC_AddDamage(-83, ...)`) | no: the page draws no numbers |
| Focused Spirit / Art, Stat Plus, Super Stat Plus, Revised Skill / Magic / Art, Charge Attack ranks | numbers only | no | no |

The Bible's Reborn-only cards (Resonant Fist, Dragon Typhoon, Wind And Storm, Hundred Fists, Formless Path, Spirit
Overflow, Five Heaven Palms, Asura Trinity; index.html:19307-19317) have no BB or TTO code: out of scope.

## How each reads (junk predicates worked out with pred.py)

### Mystic Sage (max rank 2)
- **Trigger** (CharacterControl.cs, the direct-damage `AddDamage` coroutine): on the Panda's own client, with #371
  (`mMysticSageLv = 1`, :32051; `= 2` with #372, :32056-32064), no `mysticSage` lockout, no sleep / snowMan / petrify /
  paralysis (:32043), `hp > 0` (:32068), `sp >= msp` (:32076) and `nDamage > 100` (:32084). Then the message "Mystic
  Sage!" (:32091), `addTimeOut("mysticSage", 18 - 6 x 2)` = 6 s flat (:32096), and
  `RPC_mysticSage_hit(mTransform.position, forward, 0)` (:32115; ActionEvent :32128). Every guard on the path is false
  (:32047-32129), so the code goes straight through.
- **RPC_mysticSage_hit** (:9570-9668): `Effects/mysticSage_hit` (:9583), then `Instantiate(..., xouZty6Gud.position,
  xouZty6Gud.rotation)` (:9595; `xouZty6Gud = this.transform`, :57). This is the hero's own spot and rotation. The `hitPos`
  argument is not used. Then the voice: pvoice on, the owner skips the team gate, the voice loads at :9644,
  `222524 - 7742 != 214783` is true (break), and PlayOneShot runs at :9667.
- **The heal:** 1 s later `RPC_AddHeal(370 + 2, ceil(0.5 x damage))` (CharacterControl.cs:32219, :30304). It shows a
  number only. The page has no numbers, so it is left out.
- **Prefab** (probe): EffectControl life 1, afterLife 0, no followPosition or followState. It holds an ImageEmitter
  (`Ring2`, 2 images in 0.2 s, life 0.3, 0.4 -> 1.6 m, 0.4 m up) and the double, `mysticSage_tri`: a StaticMesh
  (material `mysticSage`) with a 0.43 s Animation and an AlphaTimer. Every part is ready. The voice `mysticSage.wav`
  lasts 0.339 s.
- **TTO** (`pseudo/Panda.c:30001`, :32785): the same effect name and call.

### Safe Guard (max rank 1)
- **Trigger** (CharacterControl.cs:13465-13505, in the Panda block of RPC_AddStatus, after the Roll Around refusal and
  before Resistance): with `hasSkill(431)`, `isTimeOut("safeGuard") == 0` and `isDebuffStatus(sType)`, the code runs
  `addTimeOut("safeGuard", agiAdjust(180))` and `ActionEvent("RPC_safeGuard_hit", transform.position, forward, 0)`
  (:13503). Then `4603 - 324875 != -320271` is true (break), and the status is not applied.
- **Receive** (Panda.cs:5214-5218, action code −431): `141698 - 493432 == -351734` is true, so it calls
  `RPC_safeGuard_hit`. There is no isMine gate (Mystic Sage's receive, :5182-5188, has one), so the owner draws it from
  the ActionEvent too.
- **RPC_safeGuard_hit** (:9721-9764): `addTimeOut` again (:9728), `Effects/safeGuard_hit` (:9737), then `createEffect(...,
  xouZty6Gud.position, xouZty6Gud.rotation)` (:9747; `140214 - 213937 == -73723` is true). No voice or sound.
- **Prefab** (probe): EffectControl life 1, followPosition. An ImageEmitter (`safeGuard`, 1 image, life 1, 0.6 m up)
  and a RingEmitter on the ground (`Line_fadeBottom`, life 0.4). Ready.
- **TTO** (`pseudo/Panda.c:29954`, :32810): the same.

### Sacred Sage Technique (max rank 2, Heaven Breath on)
- **The charge** (`$RPC_cAttack1$25194`, :18879-19480):
  - At 0 s (:19330-19355): attack / cAttack1, `PlayAnimation("cAttack1", 0)`, wrap Once.
  - The voice: `Random.Range(0, 2) == 0` (:19386). Either `cAttack1` (:19396, Block_41 PlayOneShot) or `cAttack2`
    (:19427, IL_183). The predicates are worked out as listed in `pred.py 19329 19470`.
  - Then `Yield 0.7 s` (:19467).
- **case 2 at 0.7 s** (:19006-19112, all guards false):
  - In real game modes (:19022), `cAttack_ring` is created at the hero's position and rotation (:19046). Its probe:
    life 600, followState, a looped `cAttack_ring` sound.
  - With Aura Field, `auraField_ring` is created there too (:19084; life 99, followState).
  - `PlayAnimation("cAttack2", 0)` looped (:19100), and `tTime = now` (:19110).
- **The tick** (:19140-19250): it runs when `tTime + 1 <= Time.time` (:19148), so at 1.7, 2.7, ... s. Each tick:
  - SP gain `clamp(ceil(0.02 x chargeLv x ATK), 2 x chargeLv, 4 x chargeLv)`, where chargeLv = 3 at max rank
    (:19161-19190): 6-12 SP a second.
  - If then `sp > 100` and `hp < mhp`, with #343 (level 2 with #344), the owner calls `RPC_sacredSage` (:19236;
    ActionEvent :19247).
  - All guards are false (`pred.py 19116 19260`).
- **RPC_sacredSage** (:9211-9441):
  - The voice: `Random.Range(0, 2) == 0` (:9247). Either `sacredSage1` (:9259, PlayOneShot :9271) or `sacredSage2`
    (:9290, :9302).
  - `sp = 0` (50 with Revised Skill #404, :9315-9334).
  - With Heaven Breath (`3629 - 413899 == -410270` is true, :9337): `heavenBreath_ring` (:9345). It is missing, so the
    else branch logs at :9365 and no continue follows. Then the heal `50 + 50 x 2 + 2 x Lv` HP and `floor(0.1 x Lv)` MP,
    and "Heaven Breath Technique!" (:9375-9381).
  - Without Heaven Breath: `sacredSage_ring` (:9397, missing as well), the heal 150 HP and "Sacred Sage Technique!"
    (:9427-9433).
- **Voices:** sacredSage1 0.953 s, sacredSage2 0.841 s.
- **Times on the tile:** voice cAttack1|2 at 0; at 0.7 cAttack2, cAttack_ring and auraField_ring; at 1.7 (1.0 into
  cAttack2) the voice sacredSage1|2. The first tick is shown, so the Panda is taken to be just under 100 SP and hurt.
  The charge is held 3 s, as the Charge Attack tile holds it.

### Delay Qi (max rank 1, Qi Strike 3, Qi Burst on)
- **Qi Strike's charge** (`$RPC_qiStrike1$25279`): `PlayAnimation("qiStrike1", 0.2)` (:23132). The voice: either
  `qiStrike1` (:23185) or `qiStrike2` (:23216), by `Random.Range(0, 2)` (:23173). `qiStrike_ring` is created at the
  hero (:23259; life 6, followState, a looped sound). All guards on this path are false.
- **The charge end:** the charge holds while `Time.time < actionTime + 1 + sLv` (:23028), so 4 s at rank 3. Then
  `hasSkill(214)` (:23036) starts `RPC_delayQi(position, forward, 0, sLv)` (:23042) instead of RPC_qiStrike2 (:23064).
  The command turns `delayQi`, so qiStrike_ring's followState ends it there (EffectControl.cs:122-140 keeps the
  `actionState` and `myCommand` it was made with).
- **RPC_delayQi** (:23981-24275), at 4.0 s:
  - attack / `myCommand = "delayQi"` (:24140-24146; the guards at :24141-24150 are true, :24154-24238 false).
  - The voice `delayQi` (:24187, PlayOneShot :24199; 0.118 s).
  - `delayQi_ring` at the hero's position and rotation (:24226).
  - `animation.CrossFade("root", 0.2)` (:24246, inside the true `98145 - 244319 != -146173`).
  - The owner adds the `delayQi` status at Lv 3 for `chaAdjust(3) + 3 x getQiBurstLv()` = 6 s (:24255).
  - `Yield 0.2` (:24269), then case 2: `actionState = "standby"` (:24110). From then on the Panda stands or runs,
    holding the punch.
- **The status's look** (CharacterControl.cs:35338-35375, the `delayQi` case, all guards false): `Effects/delayQi`
  Instantiated, named `delayQiFx`, parented to the hero at local 0 and scale 1. It is destroyed by `removeStatus`
  (:15753-15757). Probe: EffectControl life 12 and one LineEmitter (`Ray4`, 180 rays over 9 s, repeating, 0.3 m up).
- **The release:** an attack press from standby or run with the status starts `RPC_qiStrike2` at the status level
  (:7895-7913). At 0 (`$RPC_qiStrike2$25291`, :23656-23903, guards worked):
  - `PlayAnimation("qiStrike2", 0.2)`, `moveSpeed 16` (the lunge), voice `qiStrike3` (:23730).
  - The status is on, so `removeStatus("delayQi")` (:23748) and `delayQi_fire` Instantiated at the hero (:23771).
  - With Qi Burst, `qiBurst` createEffect (:23810) instead of `qiStrike` (:23845).
  - Sounds/qiStrike (:23893), then Yield 0.2 (:23929) and the hit (the Qi Strike owner's).
- **Prefabs** (probe): `delayQi_ring` and `delayQi_fire` both have EffectControl life 1 and their own AudioSource
  `delayQi` (sounds/delayQi.wav, 1.318 s). delayQi_ring has a Ring2 image pair and a burst of 32 Ray4 lines; delayQi_fire
  has a Ring2 image pair. All ready.
- **Hold length:** the game holds until the player presses attack, at most 6 s. After 6 s the status is gone and a
  press is a plain nAttack1. The tile holds 3 s, the tooltip's "max 3 sec" (PandaSkill_eng.cs:301) (open question 1).
- **TTO** (`pseudo/Panda.c:5239`, :15197): the same delayQi_ring. TTO's Qi Strike charge is `min(sLv, 2)` s (Bible
  :1116), not ours: BB's code is the content.

## Choices made here (rule by rule)
- **Max rank, passives on:**
  - Mystic Sage 2 (no visual difference from rank 1).
  - Safe Guard 1.
  - Sacred Sage 2, with Heaven Breath, Charge Attack 3 and Aura Field on.
  - Delay Qi on Qi Strike 3, with Qi Burst on: qiBurst at the release and the 6 s limit.
- **Procs with no host clip** (Mystic Sage, Safe Guard): an idle-stance tile, played on every play with no roll and no
  enemy. The Penguin's Frost Spike, the Bison's Berserker Rush, Cat decision 10.
- **A passive with its own RPC on another skill's clip** (Sacred Sage): a tile on that clip. The Chameleon's Critical
  Plus (decision 12), the Cat's Even Odds (decision 11).
- **Positions:** all four look at the hero's own position and rotation, so the cues carry no `d` or `rot`. Nothing is
  drawn at the 10 m target point (no enemy-side effect here).
- **Followers and cuts:** qiStrike_ring is cut 4 (the command change). cAttack_ring and auraField_ring are cut 3 (the
  charge step's end). The delayQi glow is killed at 3 s (its status removed at the release). Nothing runs past 10 s.
- **Step lengths:** the longest effect or voice, held (`root*`, Cat decision 9) because the Panda's idle `root` is
  0.8 s:
  - Mystic Sage 1 s (the effect's life).
  - Safe Guard 1 s.
  - Delay Qi's hold 3 s.
  - Sacred Sage: cAttack1 0.7 s (the game's switch at :19467; the clip is 0.9 s), cAttack2 held 3 s (the Charge Attack
    tile's).

## Missing page parts

None. Every prefab above probes as built only from parts the page has: EffectControl, ImageEmitter, RingEmitter,
LineEmitter, StaticMesh, Animation, AlphaTimer, AudioSource. Two game assets are missing from the game itself:
`sacredSage_ring` and `heavenBreath_ring`, absent from the BB rip and from TTO. They are not page parts, and nothing is
drawn for them (open question 2).

## PASTE-READY

### 1. `wardrobe/index.html` SEQ: the panda line gains four tiles (append; keep whatever the other researchers write)

```js
    // the Panda's passives with their own RPC (2026-11-13, plans/fx_panda/effect_only.md): Mystic Sage and Safe Guard play
    // no clip (RPC_mysticSage_hit Panda.cs:9570 from AddDamage, RPC_safeGuard_hit :9721 from RPC_AddStatus): their effect
    // on the idle stance, held 1 s; Sacred Sage Technique on the Charge Attack's clips (its tick 1 s into cAttack2,
    // :19148-19236); Delay Qi = Qi Strike's charge, then RPC_delayQi's own CrossFade to root (:24246), held 3 s (the
    // tooltip's max 3 sec), then the release
    "Mystic Sage: root*@1", "Safe Guard: root*@1", "Sacred Sage Technique: cAttack1@0.7 cAttack2*@3",
    "Delay Qi: qiStrike1@4 root*~@3 qiStrike2~"],
```

### 2. `wardrobe/index.html` SEQ_SKILL: add a panda entry (merge with any other panda ids)

```js
  // the Panda (2026-11-13, plans/fx_panda/effect_only.md): Mystic Sage and Safe Guard on the idle stance, Sacred Sage
  // Technique on the charge's clips, Delay Qi between Qi Strike's
  panda: { "@MysticSage": "mysticSage", "@SafeGuard": "safeGuard", "@SacredSageTechnique": "sacredSageTechnique",
    "@DelayQi": "delayQi" },
```

### 3. `wardrobe/fx_cues/panda.json`: seven entries, 16 cues

The same text, checked with `json.load`, is in `checks/fx_panda_research/effect_only/cues.json`; copy that file's
entries in. The cues are:

```json
  "@MysticSage:root": { "why": "...", "cues": [
    [0, "fx", "mysticSage_hit"],
    [0, "voice", "mysticSage"] ] },
  "@SafeGuard:root": { "why": "...", "cues": [
    [0, "fx", "safeGuard_hit"] ] },
  "@SacredSageTechnique:cAttack1": { "why": "...", "cues": [
    [0, "voice", "cAttack1|cAttack2"] ] },
  "@SacredSageTechnique:cAttack2": { "why": "...", "cues": [
    [0, "fx", "cAttack_ring", {"cut": 3}],
    [0, "fx", "auraField_ring", {"cut": 3}],
    [1, "voice", "sacredSage1|sacredSage2"] ] },
  "@DelayQi:qiStrike1": { "why": "...", "cues": [
    [0, "voice", "qiStrike1|qiStrike2"],
    [0, "fx", "qiStrike_ring", {"cut": 4}] ] },
  "@DelayQi:root": { "why": "...", "cues": [
    [0, "voice", "delayQi"],
    [0, "fx", "delayQi_ring"],
    [0, "fx", "delayQi", {"kill": 3}] ] },
  "@DelayQi:qiStrike2": { "why": "...", "cues": [
    [0, "voice", "qiStrike3"],
    [0, "fx", "delayQi_fire"],
    [0, "fx", "qiBurst"],
    [0, "sound", "qiStrike"] ] }
```

The full `why` texts with every citation are in cues.json.

**Coordination:**
- `@SacredSageTechnique:cAttack1` / `:cAttack2` must match the Charge Attack tile's cAttack1 / cAttack2 entries (the
  attacks researcher), plus the sacredSage voice.
- `@DelayQi:qiStrike1` / `:qiStrike2` must match the Qi Strike tile's entries (the skills researcher). For qiStrike2
  that means copying their hit and lunge cues and keeping `delayQi_fire`.
- My cues above are the parts I derived from the code. Where the owners' entries differ, theirs win, except for
  `delayQi_fire` and the hold.
- Every option used (`cut`, `kill`) is in `wardrobe_fx_check.py` OPTS (:176).
- Check with `py -3 -c "import json; json.load(open('wardrobe/fx_cues/panda.json', encoding='utf-8'))"`.

### 4. `pipeline/wardrobe_skill_icons.py`

```python
# EFFECT_ONLY (:57-64): add
               # the Panda's Mystic Sage and Safe Guard (2026-11-13, plans/fx_panda/effect_only.md)
               "panda": ["mysticSage", "safeGuard"],
# OWN_TILE (:67-77): add
            # the Panda's Sacred Sage Technique on the charge's clips, Delay Qi on Qi Strike's and the idle (2026-11-13,
            # plans/fx_panda/effect_only.md)
            "panda": {"sacredSageTechnique": ["cAttack1", "cAttack2"], "delayQi": ["qiStrike1", "root", "qiStrike2"]},
```

The Bible has `panda_mysticSage2`, `panda_safeGuard5`, `panda_sacredSageTechnique2` and `panda_delayQi1` (assets.js;
cards index.html:19290, :19294, :19285, :19244), so `best` finds them. Then `py -3 pipeline\wardrobe_skill_icons.py`.

### 5. Build and check (the lead's, after the cue file is in)

```
uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py panda --fx mysticSage_hit,safeGuard_hit,cAttack_ring,auraField_ring,qiStrike_ring,delayQi_ring,delayQi,delayQi_fire,qiBurst --voices mysticSage,cAttack1,cAttack2,sacredSage1,sacredSage2,qiStrike1,qiStrike2,delayQi,qiStrike3 --sounds qiStrike
py -3 pipeline\wardrobe_skill_icons.py
uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py C:/work/12tails-wardrobe checks/fx_panda dark --cls panda
```

A plain `wardrobe_fx.py panda` picks these up from the cue file once every Panda cue is in (`cue_names`).

## Left out (with reasons)
- **The Sacred Sage / Heaven Breath ring:** missing from BB's and TTO's data. The game draws nothing (item 5).
- **Messages** ("Mystic Sage!", "Sacred Sage Technique!" / "Heaven Breath Technique!"), **heals**, **Resistance's −83
  popup**, **Combo Plus's atk stacks**, **Shadow Fist's effect damage:** text and numbers only. No earlier class shows
  them.
- **Heaven Breath as a tile:** a modifier passive. Its only look would be the missing ring (Cat's Lady Luck, Bison's
  Rage Control).
- **Sacred Sage in the plain Charge Attack tile:** it needs SP over 100 and HP below max, a precondition the plain
  charge does not show (the Chameleon's Clear Arrow and its invisible). The attacks researcher's call (open question 3).
- **Tempest Dance's counter (`RPC_tempestCounter`):** a TTO phase that needs an attacker. The TTO researcher's.
- **The 13 support skills:** as every class.

## Open questions (each with my recommended answer)
1. **Delay Qi's hold, and the Qi Strike tile.**
   - The hold lasts until the press, at most 6 s. I recommend **3 s** (the tooltip's "max 3 sec"). Alternatives: 1.5 s
     (the page's default `*`), or 5.9 s (the longest that still releases).
   - With passives on, the game's Qi Strike always goes through Delay Qi (`hasSkill(214)`, :23036). I recommend that
     **the Qi Strike tile keep the direct punch** (`qiStrike1@4 qiStrike2~`) and the hold get its own Delay Qi tile:
     one tile per skill, and both looks shown, as the Chameleon's Normal Attack / Clear Arrow pair. The alternative is
     one Qi Strike tile with the hold and both icons.
2. **Sacred Sage's tile has the voice only.** I recommend **keeping the tile**: one tile per skill, it has its own RPC,
   card and icon, and the game itself shows no ring. A made-up ring would be our invention. The alternative is no tile
   (Sacred Sage left as a passive with no look).
3. **Sacred Sage in the plain Charge Attack tile:** I recommend **not** (HP is full there). The attacks researcher
   decides that tile.
4. **Mystic Sage / Safe Guard with no attacker shown:** I recommend **the proc alone on the idle stance**, as Frost Spike
   (Penguin) and Berserker Rush (Bison). The hit or debuff that sets them off belongs to another hero.
5. **Wind & Cloud and Rain & Storm** (item 4): I recommend fixing `pipeline/wardrobe_data.py:210` to admit `&`
   (`[a-z0-9_&]+`) at the home PC, rebuilding the Panda's data, and checking the `&` through the page's clip names and
   URLs (`encodeURIComponent` wherever a clip name becomes a path). The skills researchers then cue them. Until then
   neither skill can have a tile. Neither is effect-only.

## Offers for the Bible (not written there)
- `sacredSage_ring` and `heavenBreath_ring` exist in neither BB's nor TTO's data. Sacred Sage / Heaven Breath show no
  ring in game, only the voice and the message (Panda.cs:9345 / :9397 load nothing; TTO the same).
- Safe Guard's `safeGuard_hit` reaches the owner only through the ActionEvent (no local call; the −431 receive has no
  isMine gate, Panda.cs:5214-5218), unlike Mystic Sage (local call + an isMine-gated receive).
- Delay Qi's hold: after 0.2 s the Panda is back in `standby` (:24110) with the status and its glow (`delayQiFx`,
  parented to the hero). The release plays `delayQi_fire` (:23771) beside the normal Qi Strike / Qi Burst effect.
- The charge tick starts 1 s after cAttack2 begins: the first Sacred Sage / SP tick lands 1.7 s after the press
  (:19110, :19148).
- Mystic Sage's double appears at the hero's own spot, not at the hit point (`RPC_mysticSage_hit` ignores `hitPos`,
  :9595).

## Verification (2026-11-13)

Checker's re-trace, office PC. Probes are in `checks/fx_panda_research/verify/ae_eo/` (git-ignored):
- `probe_summary.txt` and `probe_wc_rs_summary.txt`: `wardrobe_fx.py panda --probe`, exit 0.
- `check_cues.py`: keys, order, kinds, options and names against the rip.
- `make_block.py`: builds the corrected block below (`effect_only_cues.json`) and parses it.

This section wins over the body.

1. **Delay Qi: the Qi Strike tile includes the hold (skills_a wins), and the Delay Qi tile keeps only `@DelayQi:root`.**
   - The body's open question 1 has Qi Strike show the direct punch. With passives on, that never happens in the game:
     `hasSkill(214)` always turns the charge's end into RPC_delayQi (:23036-23042).
   - The Chameleon's Normal Attack / Clear Arrow pair is not a match. Clear Arrow needs a state, invisibility, so both
     of its looks can happen.
   - The call for Qi Strike: plans/fx_panda/skills_a.md's `"Qi Strike: qiStrike1@4 root*~@3 qiStrike2~"`, with its
     plain `qiStrike1` / `qiStrike2` entries and `@QiStrike:root` (skills_a.md:422, :559-583).
   - The call for Delay Qi: a tile of its own with its Bible icon, by the one-tile-per-skill rule (Chameleon decision
     12: Critical Plus has its own tile although its host shows it too).
     - It has the same steps as the Qi Strike tile.
     - Its only own key is `@DelayQi:root`, with the same cues as `@QiStrike:root`.
     - Its qiStrike1 / qiStrike2 steps fall back to the plain entries: fxStart tries `@<id>:<clip>`, then `<clip>`
       (index.html:5323).
   - **Drop `@DelayQi:qiStrike1` and `@DelayQi:qiStrike2`.** They would copy skills_a's entries and drift from them.
     The body's copy already lacks qiBurst's `{"cut": 0.6}`: qiBurst is followState (probe: life 2), and the release
     goes to standby at 0.6 s (skills_a.md:416-417).
   - Not taken: no Delay Qi tile at all (skills_a Q2: "identical"). The rule needs Delay Qi's icon on a tile.
2. **Sacred Sage Technique takes the Charge Attack tile's steps:**
   `"Sacred Sage Technique: cAttack1@0.7 cAttack2*@3 root~@0.2"`.
   - The body leaves out the release. attacks_emotes.md Read this first 6 has it: RPC_cAttack0's
     CrossFade("root", 0.2) (:19685), then standby 0.2 s later (:19699).
   - The cues do not change.
3. **Missed: Wind & Cloud and Rain & Storm need tiles, and their missing parts are built, not left out.**
   - No Panda report cues either skill. A grep over plans/fx_panda finds no windCloud1 / 2 at all; rainStorm1 / 2 appear
     only as Tempest Dance's, in tto.md.
   - The body's item 4 found the cause but left the build undone.
   - **Data.**
     - Both clips are GameObjects in TTO's catalog. `aa_catalog.py tto_assets/2026-11-09/catalog.bin --grep
       heroes/panda/animations/` lists `wind&cloud` and `rain&storm` as `UnityEngine.GameObject`. So `tto` is false:
       they are BB content, online too.
     - The BB rip has `AnimationClip/wind&cloud.anim` (last key 3.6 s) and `rain&storm.anim` (3.0 s).
     - Only the regex drops them, in two places, not one: pipeline/wardrobe_data.py:49 (the catalog grep) and :210 (the
       clip filter). In both, change `animations/[a-z0-9_]+` to `animations/[a-z0-9_&]+`.
     - Then rebuild the Panda's data at the home PC, since it reads TTO's bundles:
       `uv run --no-project --with UnityPy --with pillow python wardrobe_data.py --only panda`. Commit and push
       `wardrobe/data/panda/` and `meta.json`.
   - **Icons.**
     - The Bible's icons are `panda_wind&cloud2` and `panda_rain&storm2` (bible/index.html:19286-19287).
     - In pipeline/wardrobe_skill_icons.py `main`, change `re.fullmatch(rf"{cls}_([A-Za-z]+?)(\d*)", k)` to
       `rf"{cls}_([A-Za-z&]+?)(\d*)"`.
     - The clip lookup (`base.lower() in lower`) then finds both, with no CLIP_SKILLS line.
   - **Page.**
     - No SEQ line: they are single clips. SEQ_ALT's `\w+` (index.html:1381) would reject `&`, so they must stay out of
       SEQ.
     - The lead's browser pass checks the two tiles, their icons (`icons/hd/panda/wind&cloud.webp`) and the cues.
   - **Cues.** I derived them with the annotated reader; each state has one Yield, so the chain runs in order.
     - **Wind & Cloud:**
       - at 0: the voice `windCloud1|windCloud2` and Sounds/windCloud;
       - ten `windCloud` rings: 0.3 and 0.6 s (+0.5 forward), 0.9 (at the hero), 1.2 and 1.5 (-0.3 right), 1.7 (at the
         hero), 2.1 (+0.3 right), 2.5 (+0.5 right), 2.9 and 3.0 (+0.4 forward);
       - `punch1` with each ring from 0.6 s on;
       - the waits: 0.3 x 5 + 0.2 + 0.4 x 2 + 0.3 + 0.1 x 2 + 0.2 + 0.1 = 3.3 s to the standby.
     - **Rain & Storm:**
       - at 0: the voice `rainStorm1|rainStorm2`;
       - five `rainStorm` bursts at 0.2, 0.7, 1.3, 1.9 and 2.2 s (waits 0.2 + 0.5 + 0.6 + 0.6 + 0.3);
       - the bursts are followState, so each is cut at the standby: 2.2 + 0.2 + 0.4 = 2.8 s.
     - Neither skill's hits reach the 10 m target (4 m and 6 m circles round the hero), and neither skill has a mode
       gate.
     - Both prefabs are ready. windCloud is one RingEmitter (life 2). rainStorm is a RingEmitter with its own
       AudioSource.
     - Verdict: PLAUSIBLE. The clip researcher reads them again when they are cued.
   - **HANDOFF item** (the lead writes it):
     - At the home PC: apply the two regex changes, rebuild the Panda's data, run `wardrobe_skill_icons.py`, and add
       the two entries below to `wardrobe/fx_cues/panda.json`.
     - Then build: `wardrobe_fx.py panda --fx windCloud,rainStorm --voices windCloud1,windCloud2,rainStorm1,rainStorm2
       --sounds windCloud,punch1`. Commit and push.
     - The two cue keys are not clips until the data rebuild lands, so add them with the rebuild.
4. **Confirmed, no change:**
   - **Mystic Sage:**
     - `Effects/mysticSage_hit` is Instantiated at the hero's position and rotation (:9583, :9595).
     - The voice is mysticSage (:9644, :9667).
     - The prefab has life 1 and no follow.
   - **Safe Guard:**
     - `safeGuard_hit` is a createEffect at the hero (:9737, :9747).
     - The prefab has followPosition and life 1. There is no voice.
   - **Sacred Sage:**
     - The voices are sacredSage1 / 2 (:9247-9302).
     - `heavenBreath_ring` (:9345) and `sacredSage_ring` (:9397) are in neither the BB rip's effects nor TTO's
       catalog. The game draws nothing there, and neither is a page part.
     - The charge's tick waits for tTime + 1, so the first tick is 1.0 s into cAttack2: the voice cue at 1.
   - **Delay Qi:**
     - delayQi_ring at the hero; the voice delayQi (:24187, :24199); CrossFade("root", 0.2) (:24246).
     - The status lasts chaAdjust(3) + 3 = 6 s, so the 3 s hold (the tooltip's "max 3 sec", PandaSkill_eng.cs:301)
       fits inside it.
     - The `delayQi` glow has life 12 and one LineEmitter, so `kill 3` is right.
     - qiStrike_ring is followState with life 6, so `cut 4` is right.
   - **Counts:** Panda.cs has 84 RPC_ definitions (grep).
   - **Icons:** all four are in the Bible's assets.js: panda_mysticSage2, panda_safeGuard5, panda_sacredSageTechnique2
     and panda_delayQi1.
   - **The cue file:**
     - The body's cues.json parses.
     - Its keys are real clips under the proposed sequence ids (`@MysticSage`, `@SafeGuard`, `@SacredSageTechnique`,
       `@DelayQi`: each SEQ name without its spaces, index.html:1410).
     - Every name is in the rip.
   - **Block 3 is not paste-ready:** its `why` texts read `"..."`, and the full texts sit in a git-ignored file the home
     PC does not have. The full block is below.
5. **Corrected paste-ready blocks** (these replace PASTE-READY 1-5):

   **SEQ.panda: add** beside attacks_emotes' and skills_a's lines, keeping the body's comment with Delay Qi's part
   reworded as item 1 says:
   ```js
       "Mystic Sage: root*@1", "Safe Guard: root*@1", "Sacred Sage Technique: cAttack1@0.7 cAttack2*@3 root~@0.2",
       "Delay Qi: qiStrike1@4 root*~@3 qiStrike2~"
   ```
   Qi Strike's own line is skills_a's: `"Qi Strike: qiStrike1@4 root*~@3 qiStrike2~"`.

   **SEQ_SKILL, merged with skills_a's:**
   ```js
     // the Panda (2026-11-13, plans/fx_panda/effect_only.md Verification, skills_a.md): Qi Strike (with Delay Qi's hold),
     // Mystic Sage and Safe Guard on the idle stance, Sacred Sage Technique on the charge's clips, Delay Qi's own tile
     panda: { "@QiStrike": "qiStrike", "@MysticSage": "mysticSage", "@SafeGuard": "safeGuard",
       "@SacredSageTechnique": "sacredSageTechnique", "@DelayQi": "delayQi" },
   ```

   **pipeline/wardrobe_skill_icons.py:**
   - The body's lines stand: EFFECT_ONLY `"panda": ["mysticSage", "safeGuard"]` and OWN_TILE
     `"panda": {"sacredSageTechnique": ["cAttack1", "cAttack2"], "delayQi": ["qiStrike1", "root", "qiStrike2"]}`.
   - Add the `[A-Za-z&]+?` change from item 3.

   **wardrobe/fx_cues/panda.json: seven entries, 37 cues.**
   - The first five go in now.
   - `wind&cloud` and `rain&storm` go in with the home PC's data rebuild (item 3).
   - Qi Strike's three entries are skills_a's.

   ```json
     "@MysticSage:root": {
       "why": "Mystic Sage 2 (#372, passives on), a proc with no clip: on the Panda's own client, in the direct-damage AddDamage coroutine (CharacterControl.cs:31986-32133), with #371 / #372 (mMysticSageLv 2, :32051-32064), no mysticSage lockout, none of sleep / snowMan / petrify / paralysis, hp > 0 (:32068), sp >= msp (:32076) and a hit of more than 100 (:32084): the message Mystic Sage! (:32091), addTimeOut(mysticSage, 18 - 6 x 2 = 6 s, flat) (:32096) and RPC_mysticSage_hit at the hero (:32115, ActionEvent :32128; the junk guards on the path all false, worked by hand). RPC_mysticSage_hit (Panda.cs:9570-9668): Effects/mysticSage_hit (:9583) Instantiated at the hero's own transform, position and rotation (xouZty6Gud = this.transform, :57; :9595; EffectControl life 1, no followPosition / followState: the double, a StaticMesh with its 0.43 s Animation and AlphaTimer, and a Ring2 image burst), then voice mysticSage (:9644, PlayOneShot :9667; the owner passes the team gate). Nothing plays a clip: the tile shows it on the idle stance, on every play (no hit to wait for: the Penguin's Frost Spike, the Bison's Berserker Rush). The heal (ceil(0.5 x damage) HP 1 s later, CharacterControl.cs:32219, :30304) and the message draw nothing the page shows (plans/fx_panda/effect_only.md)",
       "cues": [
         [0, "fx", "mysticSage_hit"],
         [0, "voice", "mysticSage"]
       ]
     },
     "@SafeGuard:root": {
       "why": "Safe Guard (#431, passives on), a proc with no clip: in the Panda block of RPC_AddStatus (CharacterControl.cs:13465-13505), with #431, no safeGuard cooldown (:13471) and a debuff status on its way (StatusData.isDebuffStatus, :13477): addTimeOut(safeGuard, agiAdjust(180)) (:13483), ActionEvent RPC_safeGuard_hit (:13503; the receive, Panda.cs:5214-5218 (code -431), has no isMine gate, so the owner draws it too), then break: the status is not applied. RPC_safeGuard_hit (Panda.cs:9721-9764): addTimeOut again (:9728), Effects/safeGuard_hit (:9737) createEffect at the hero's position and rotation (:9747; EffectControl life 1, followPosition: one safeGuard image 0.6 m up for 1 s and a ground RingEmitter 0.4 s); no voice, no sound. Nothing plays a clip: the tile shows it on the idle stance, on every play (no debuff to wait for: the Penguin's Frost Spike) (plans/fx_panda/effect_only.md)",
       "cues": [
         [0, "fx", "safeGuard_hit"]
       ]
     },
     "@SacredSageTechnique:cAttack1": {
       "why": "Sacred Sage Technique rides the Charge Attack (RPC_cAttack1 -> $RPC_cAttack1$25194, Panda.cs:18879-19480): the charge start as the Charge Attack's (actionState attack, myCommand cAttack1, PlayAnimation(cAttack1, 0) :19351, voice cAttack1 / cAttack2 by Random.Range(0, 2) :19386, :19396 / :19427, PlayOneShot Block_41 / IL_183; Yield 0.7 s :19467). Copy the Charge Attack tile's cAttack1 cues here if its owner adds any (plans/fx_panda/effect_only.md)",
       "cues": [
         [0, "voice", "cAttack1|cAttack2"]
       ]
     },
     "@SacredSageTechnique:cAttack2": {
       "why": "Sacred Sage Technique 2 (#344, passives on; Heaven Breath #443 on): at 0.7 s the charge's case 2 (Panda.cs:19006-19112, real game modes, :19022): cAttack_ring at the hero's position and rotation (:19046; EffectControl life 600, followState: it ends when the charge does, cut 3, the step's end), with Aura Field #411 auraField_ring there too (:19084; life 99, followState), PlayAnimation(cAttack2, 0) looped (:19100), tTime = now (:19110). The tick (:19140-19250) runs once a second from tTime + 1 (:19148): SP + clamp(ceil(0.02 x 3 x ATK), 6, 12) with Charge Attack 3 (#112, #113: chargeLv 3, :19161-19190); when SP is then above 100 and HP below max (:19195-19201) with #343 / #344 (level 2, :19207-19222) the owner calls RPC_sacredSage (:19236, ActionEvent :19247). The tile shows the first tick, 1.0 s into cAttack2 (the Panda close to 100 SP, hurt). RPC_sacredSage (Panda.cs:9211-9441): voice sacredSage1 / sacredSage2 by Random.Range(0, 2) (:9247; :9259 / :9290, PlayOneShot :9271 / :9302), SP to 0 (50 with Revised Skill #404, :9315-9334), then with Heaven Breath the heavenBreath_ring createEffect (:9345-9357) and the heal 50 + 50 x 2 + 2 x Lv HP, Lv / 10 MP with the message Heaven Breath Technique! (:9377-9380) (without it sacredSage_ring, :9397-9409, and Sacred Sage Technique!, :9429-9432). Neither ring is in the game's data (the BB rip: KeyError; TTO's catalog: not there either), so the game logs Cannot find ... and draws no ring: the voice is the skill's only look (plans/fx_panda/effect_only.md, open question 2)",
       "cues": [
         [0, "fx", "cAttack_ring", {"cut": 3}],
         [0, "fx", "auraField_ring", {"cut": 3}],
         [1, "voice", "sacredSage1|sacredSage2"]
       ]
     },
     "@DelayQi:root": {
       "why": "RPC_delayQi (Panda.cs:8549 -> $RPC_delayQi$25306 :23981-24275) plays no skill clip of its own: myCommand delayQi (:24146), voice delayQi (:24187, PlayOneShot :24199), delayQi_ring at the hero's position and rotation (:24217-24226; EffectControl life 1, its own AudioSource delayQi), animation.CrossFade(root, 0.2) (:24246: the idle stance, the step's ~), the delayQi status at the Qi Strike rank 3 for chaAdjust(3) + 3 x Qi Burst (#412 on) = 6 s (:24255); after 0.2 s actionState standby (:24110). The status's apply (CharacterControl.cs:35338-35375) Instantiates Effects/delayQi parented to the hero at local 0 (delayQiFx; EffectControl life 12, a repeating Ray4 LineEmitter); it goes with the status (removeStatus, :15753-15757), here at the release 3 s on (kill 3). The hold is 3 s, the tooltip's max 3 sec (PandaSkill_eng.cs:301; 6 s is the limit with Qi Burst: a release after it is a plain nAttack1) (plans/fx_panda/effect_only.md, open question 1); the Delay Qi tile's only own key (Verification 2026-11-13 item 1): its qiStrike1 / qiStrike2 steps take the plain qiStrike1 / qiStrike2 entries of plans/fx_panda/skills_a.md (fxStart's fallback, index.html:5323), and these cues are the same as skills_a's @QiStrike:root",
       "cues": [
         [0, "voice", "delayQi"],
         [0, "fx", "delayQi_ring"],
         [0, "fx", "delayQi", {"kill": 3}]
       ]
     },
     "wind&cloud": {
       "why": "Panda.cs RPC_windCloud ($RPC_windCloud$25591 :36529-38050; checker-derived 2026-11-13, plans/fx_panda/effect_only.md Verification item 3): at 0 attack / myCommand windCloud / addTimeOut(wind&cloud, agiAdjust(120)) (:37793-37802), PlayAnimation(wind&cloud, 0.2) Once (:37811-37814), the voice windCloud1 or windCloud2 (Random.Range(0, 2) :37852, loads :37864 / :37895, PlayOneShot :37876 / :37907; pvoice, own hero or a mission teammate :37823-37845), Sounds/windCloud (IL_E97 :37919-37938, every path), Spirit Fist #433 on (:38003), Yield(2, 0.3) (:38004); the 13 states chain 2 -> 14, each Yield(k) once (:37977-38047): 0.3 (case 2 :36657) windCloud Instantiated at position + 0.5 forward, Quaternion.identity (:36699; a RingEmitter on the ground, EffectControl life 2, no follow: the identity rotation changes nothing on a ring), no punch (Block_225 -> Yield(3, 0.3) :38027-38028, :38017); 0.6 (case 3) the same + 0.5 forward (:36742) and own hero PlayOneShot(punch1Fx) = Sounds/punch1 (:36748-36754); 0.9 (case 4) at the hero (:36851) + punch1 (:36863); 1.2 (case 5) - 0.3 right (:36960) + punch1 (:36974); 1.5 (case 6) - 0.3 right (:37012) + punch1 (:37024); 1.7 (case 7) at the hero (:37116) + punch1 (:37128); 2.1 (case 8) + 0.3 right (:37220) + punch1 (:37232); 2.5 (case 9) + 0.5 right (:37324) + punch1 (:37336); 2.8 (case 10) moveSpeed 2 (:37422); 2.9 / 3.0 (cases 11, 12) + 0.4 forward (:37455, :37559) + punch1 (:37467, :37571); 3.2 (case 13) moveSpeed 0 and the last hit (:37657-37670); 3.3 (case 14) standby (:37741); no mGameType gate on any of it (none in :36650-37722); every hit is FindAreaTarget(hero, (3 + 1) x rangeMod, 2) (:36768 ...): 4 m, never the 10 m target, no hit look (windcloud_hit is loaded by no code, parts.md); the clip is 3.6 s (AnimationClip/wind&cloud.anim); the hero's walk (moveSpeed 3, 1, 2) played in place (Penguin decision 8, Cat decision 20)",
       "cues": [
         [0, "voice", "windCloud1|windCloud2"],
         [0, "sound", "windCloud"],
         [0.3, "fx", "windCloud", {"d": 0.5}],
         [0.6, "fx", "windCloud", {"d": 0.5}],
         [0.6, "sound", "punch1"],
         [0.9, "fx", "windCloud"],
         [0.9, "sound", "punch1"],
         [1.2, "fx", "windCloud", {"x": -0.3}],
         [1.2, "sound", "punch1"],
         [1.5, "fx", "windCloud", {"x": -0.3}],
         [1.5, "sound", "punch1"],
         [1.7, "fx", "windCloud"],
         [1.7, "sound", "punch1"],
         [2.1, "fx", "windCloud", {"x": 0.3}],
         [2.1, "sound", "punch1"],
         [2.5, "fx", "windCloud", {"x": 0.5}],
         [2.5, "sound", "punch1"],
         [2.9, "fx", "windCloud", {"d": 0.4}],
         [2.9, "sound", "punch1"],
         [3.0, "fx", "windCloud", {"d": 0.4}],
         [3.0, "sound", "punch1"]
       ]
     },
     "rain&storm": {
       "why": "Panda.cs RPC_rainStorm ($RPC_rainStorm$25622 :38147-38998; checker-derived 2026-11-13, plans/fx_panda/effect_only.md Verification item 3): at 0 attack / myCommand rainStorm / addTimeOut(rain&storm, agiAdjust(180)) (:38821-38830), PlayAnimation(rain&storm, 0.2) Once (:38839-38842), the voice rainStorm1 or rainStorm2 (Random.Range(0, 2) :38880, loads :38890 / :38921, PlayOneShot Block_133 :38987 / Block_102 :38972; pvoice, own hero or a mission teammate :38851-38873), Yield(2, 0.2) (:38979); then Yield(3, 0.5) :38970, (4, 0.6) :38994, (5, 0.6) :38962, (6, 0.3) :38964, (7, 0.2) :38960, (8, 0.4) :38977: Effects/rainStorm createEffect at the hero, Quaternion.identity, at 0.2 (case 2 :38317), 0.7 (:38360), 1.3 (:38468), 1.9 (:38565), 2.2 (:38657), no mode gate; each EffectControl life 2 + afterLife 1, followPosition, followState, its own Sounds/rainStorm (probe, checks/fx_panda_research/verify/ae_eo/probe_wc_rs_summary.txt): the action changes at the standby, 2.8 s (case 8 :38769-38779): cut 2.8; hits at 0.7-2.2 are FindAreaTarget(hero, (5 + 1) x rangeMod, 2) (:38390 ...): 6 m with Spirit Fist #433, never the 10 m target; the clip is 3.0 s (AnimationClip/rain&storm.anim); moveSpeed 3 / 4 played in place",
       "cues": [
         [0, "voice", "rainStorm1|rainStorm2"],
         [0.2, "fx", "rainStorm", {"cut": 2.8}],
         [0.7, "fx", "rainStorm", {"cut": 2.8}],
         [1.3, "fx", "rainStorm", {"cut": 2.8}],
         [1.9, "fx", "rainStorm", {"cut": 2.8}],
         [2.2, "fx", "rainStorm", {"cut": 2.8}]
       ]
     }
   ```

   **Build** (the lead's, once the cue file is in):
   ```
   uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py panda --fx mysticSage_hit,safeGuard_hit,cAttack_ring,auraField_ring,delayQi_ring,delayQi --voices mysticSage,cAttack1,cAttack2,sacredSage1,sacredSage2,delayQi
   ```
   Qi Strike's names come with skills_a's entries. Once every Panda cue is in, a plain `wardrobe_fx.py panda` takes
   them all from the cue file.
6. **Open questions, decided:**
   - Q1: as item 1. The 3 s hold stands.
   - Q2: keep the voice-only Sacred Sage tile, as recommended.
   - Q3: no Sacred Sage in the plain Charge Attack tile, as recommended.
   - Q4: the proc alone on the idle stance, as recommended (the Penguin's Frost Spike).
   - Q5: replaced by item 3: built with two regex changes at the home PC.
