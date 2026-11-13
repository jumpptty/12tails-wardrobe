Summary: all nine clips are traced, with file:line, through the opaque predicates and the timed waits. One shared channel (`RPC_cast`) feeds 13 BB skills. With the passives on (Damage Cast #102/#103) it plays **damageCast1 / damageCast2**, not cast1 / cast2, and releases on cast3. That gives a 10-member cast3 pool plus four sequences of their own: Lavu (hold), Volcanic Eruption (the 10 s field), Summon Gaos (its 8 s bar) and Fire Keep (cast3 with no channel). Blazing Arrow, Flash Fire and Titanic Earth Pulse (`earthPulse`) are plain entries. damageCast3 is never played. In all: 11 cue keys, 17 skills, 75 cues. Eight missing parts (P1-P8), the biggest being the five elemental summons. 12 open questions, each with a recommended answer.

# Monkey effects + sounds research: skills_a (the cast channel and its pool, Blazing Arrow, Flash Fire, Earth Pulse)

Researcher `skills_a`, 2026-11-13 (office PC).
- **Scope:** the clips blazingArrow, cast1, cast2, cast3, damageCast1, damageCast2, damageCast3, earthPulse and flashFire, and every skill that plays them.
- **Method:** research only (recipe steps 1-3).
- **Line numbers:** `C:\Users\Jump\Desktop\12tails\DecompiledSource\Monkey.cs` unless another file is named. The home PC has the same files under `D:\12tails\`. "TTO1102:" means `DecompiledSource_TTO_2026-11-02` (method + RVA).
- **Units:** times are seconds from the start of the clip the cue is keyed by. d = metres ahead, x = metres right, y = metres up.

## Read-only probes

Everything is in `C:\work\12tails-wardrobe\checks\fx_monkey_research\skills_a\` (git-ignored). Nothing there writes outside that folder.

- **Coroutine reads:**
  - `clean.py <file> <from> <to>` works out the opaque predicates. A false `if (a - b op c)` block is dropped; a true one is marked `!!TRUE` and its body kept.
  - `mn.sh <RPC> [file]` prints a coroutine's MoveNext that way; `fn.sh <method> [file]` does the same for a plain method.
  - Outputs: `mn_RPC_*.txt` (RPC_cast, the 14 release coroutines, blazingArrow / blazingArrow_fire, flashFire, earthPulse / earthPulse_hit, groundLock_hit, stoneHammer_fire), `mn_<Elemental>_summon.txt`, `fn_RPC_*_create.txt`, `fn_RPC_fireBall_fire.txt`, `fn_RPC_earthPulse_fire.txt`, `fn_RPC_lavu_summon.txt`.
  - `brief_RPC_*.txt` keeps only the event lines. `flow_RPC_*.txt` is clip_flow.js output and `clip_calls.txt` is clip_calls.js output.
- **`probe\probe.json` + `probe\summary.txt` (from `summ.py`):** `wardrobe_fx.py monkey --probe` of 26 effects. fireBall4 fails ("no layout for Monkey_fireBall"), and volcanicSoul_ring is not in BB's data (KeyError).
  - `probe\probe2.json`: the fireKeep status flash.
  - `probe\probe_tto.err`: volcanicSoul_ring is not in TTO's catalog either.
  - `probe\probe_tto_ve.json`: TTO's copy of volcanicEruption, which reads whole with three ParticleSystems.
  - `probe\cat_keys.py` -> `cat_keys.txt`: TTO catalog addresses under heroes/monkey (voices/blazingarrow is there).
- **`cues.json` + `check.py`:** the paste-ready block below, checked as JSON against wardrobe_fx_check.py's KINDS / OPTS with every time list in order. The only option it does not know yet is `alt` (P8).

## Max rank and passives on

- **The channel skills at top rank:** Fireball 4, Phoenix 4, Ja 4, World Ignition 2, Ground Lock 4, Gadina 4, Stone Hammer 4, Buiten Hou Hou 4, Lavu 2, Flash Fire 4. The rest have one rank: Blazing Arrow, Titanic Earth Pulse, Fire Avatar, Earth Form, Volcanic Eruption, Summon Gaos.
- **Passives that change a look:**
  - Damage Cast #102/#103 swaps the channel clips.
  - Auto Instant #431 gives a 12 % instant cast, with the instantCast flash, and lets the four gated C skills use it.
  - Fire Soul #422 adds fireSoul_ring at the Phoenix create (and a missing volcanicSoul_ring at the Gaos create).
  - Earth Soul #423 adds earthSoul_ring at the Gadina create.
  - Second Stone #403 adds Ground Lock's second stone at 3.4 s.
  - Fire Keep #402 gives its own release tile.
- **Passives that change only numbers:** Rapid Fire, Intense Fire, Aegis of Earth, Stone Sentinel #443, Blazing Fire #442, Instant Blaze #412 and Earth Guard #413 (both only added to the summon's skill list).
- **Rank and the prefab:** the summon and fireball prefabs are picked by sLv (Phoenix4, Ja4, Gadina4, Buiten4, fireBall4). No other rank picks a different effect.
- **Random rolls:** lckAdjust at the stat-free LCK 1 (CharacterControl.cs:20658-20670): `floor(100·n·1.01 / (n·1.01 − n + 100))`. That gives 12 → 12 % and 24 → 24 % (the Bison's 55 → 56 % precedent).

---

## Read this first

### 1. Who plays these clips

| clip | BB | TTO |
|---|---|---|
| cast1 / cast2 | RPC_cast :25486 / :24859, only when getDamageCastLv() == 0 (:25472, :24845) | same (TTO1102:Monkey.<RPC_cast>d__178::MoveNext@0x1CE8830) |
| damageCast1 / damageCast2 | RPC_cast :25478 / :24851, with Damage Cast learned | same |
| damageCast3 | **none**: no BB file names it, nor TTO1102 / 1106 / 1109 | none |
| cast3 | the 13 RPC_<skill>_cast releases started by RPC_cast (:25700-26194), plus RPC_fireKeep_cast (:37182) | the same 14; TTO's RPC_cast also releases buitenBastion, jaAscension and runeGolem (their own clips: the tto report) |
| blazingArrow | RPC_blazingArrow :27881 | same (TTO1102:Monkey.<RPC_blazingArrow>d__188@0x1CE4340) |
| flashFire | RPC_flashFire :28747 | same (d__190@0x1CEE680) |
| earthPulse | RPC_earthPulse :32391 (Titanic Earth Pulse) | same (d__208@0x1CEBC40) |

- With the passives on, cast1 / cast2 are never played. Today's page has both a "Cast" tile (cast1 cast2) and a "Damage Cast" tile (damageCast1 damageCast2). Both end in cast3.
- **Recommendation:** one Cast host, `"Cast: damageCast1 damageCast2*~@0 cast3~"`, with cast1 / cast2 in LOWER_RANK (open question 1).
- TTO's copies of these coroutines load the same names and constants. The one difference is in Blazing Arrow: TTO only unsummons a Phoenix4 (`Monkey__ConsumeSummonOfExactType(…, "Phoenix4")`) where BB unsummons any summon. No summon is out on the tile, so no look changes.

### 2. The channel (RPC_cast, $RPC_cast$24449 :24676-26292)

| time | what happens | source |
|---|---|---|
| 0 | the cast time and cooldown per sType | :25112-25429 |
| 0 | magAdjust | :25430 |
| 0 | actionState attack, myCommand cast | :25435-25445 |
| 0 | damageCast1 (0.2 s fade, Once) | :25478, :25492 |
| 0 | voice `cast` | :25537, :26217 |
| 0.7 | Yield(2, 0.7) | :26208 |
| 0.7 | damageCast2 (0.2 s fade) looped | :24851, :24865 |
| 0.7 | the castRing field at the hero (EC 999, followPosition, followState, its looping castRing sound) | :24882, :24892 |
| 0.7 | castTime = now + bar | :24989 |
| 0.7 | Auto Instant's 12 % roll: castTime 0 and `instantCast` at the hero | :25008-25048 |
| each frame | Damage Cast hits (2 m, every 0.4 s: nothing drawn) | :25599-25681 |
| bar's end | the skill's release coroutine; its myCommand ends the ring's followState | :25692-26194; EffectControl.cs:110-150, :190-215 |

The bars at the highest MAG (magAdjust = clamp(t − 16, 0.1, 600)):
- Every member is at the 0.1 s floor, except **Summon Gaos**: 24 − 16 = **8 s**. That is the War Capital precedent, so it gets its own tile.
- The page's convention is no cast bar (index.html:1160), hence `damageCast2*~@0`.

### 3. The release template (13 of the 14 coroutines)

| time | what happens |
|---|---|
| 0 | cast3 (0.2 s fade, Once) and the skill's voice |
| 0.3 | `castEffect_fire` at hero + TransformDirection(0, 1, 1) |
| 0.4 | the payload |
| 0.8 | standby |

Exceptions:
- **Fire Avatar / Earth Form:** the payload at 0.7, standby at 1.5 / 1.2.
- **Lavu:** standby at 2.4.
- **Volcanic Eruption:** no castEffect_fire; the payload at 0.3; standby at 12.0.
- **Fire Keep:** no voice.
- **Summon Gaos:** no voice.

### 4. Summons are ActionEvent-only

- Phoenix, Ja, Gadina, Buiten and Gaos are created only through `ActionEvent("RPC_<x>_create4")`. That event is sent only when `PhotonClient.IsInitialized()`.
- The receiver's negative create codes are not gated by isMine (Monkey.cs:5182-5195), so the caster gets its own create back.
- Online they appear, which is the game look, so they are cued. Lavu calls `RPC_lavu_summon` directly.

### 5. Missing in both games' data

- **`Effects/volcanicSoul_ring`** (Summon Gaos with Fire Soul, :14387): it is in neither BB's data nor TTO's catalog, so nothing is drawn.
- **Voice `blazingArrow`** (:27917): not in BB's rip (`voices/` has no blazingArrow.wav), but TTO's catalog has `voices/blazingarrow`. Cued as TTO's recording (Sheep decision 10, Chameleon skills_a item 3); P7 brings it in.

### 6. Page changes needed

All in `wardrobe/index.html` unless noted.

- **`SEQ.monkey`:**
  - Replace `"Cast: cast1 cast2*~@0 cast3~"` and `"Damage Cast: damageCast1 damageCast2*~@0 cast3~"` with **`"Cast: damageCast1 damageCast2*~@0 cast3~"`**.
  - Add `"Lavu: damageCast1 damageCast2*~@0 cast3~@2.4"`.
  - Add `"Volcanic Eruption: damageCast1 damageCast2*~@0 cast3~@10.3"`.
  - Add `"Summon Gaos: damageCast1 damageCast2*~@8%88|damageCast2*~@0 cast3~"`.
  - Add `"Fire Keep: cast3"`.
- **Other tables:**
  - `LOWER_RANK.monkey = ["cast1", "cast2"]`: passives-off clips (comment: Damage Cast #102/#103 learned, Monkey.cs:25472, :24845).
  - `NEVER_PLAYED.monkey = ["damageCast3"]`.
  - `SEQ_SKILL.monkey = { "@Lavu": "lavu", "@VolcanicEruption": "volcanicEruption", "@SummonGaos": "summonGaos", "@FireKeep": "fireKeep" }`.
- **`pipeline/wardrobe_skill_icons.py`:**
  - `CLIP_SKILLS["monkey"] = {"earthPulse": ["titanicEarthPulse"]}`.
  - `OWN_TILE["monkey"] = {"lavu": ["cast3"], "volcanicEruption": ["cast3"], "summonGaos": ["damageCast2", "cast3"], "fireKeep": ["cast3"]}`.
  - The Bible icon keys exist for every member: `monkey_fireBall4`, `phoenix4`, `ja4`, `worldIgnition2`, `groundLock4`, `gadina4`, `stoneHammer4`, `buitenHouHou4`, `fireAvatar5`, `earthForm5`, `lavu2`, `volcanicEruption5`, `summonGaos5`, `fireKeep5`, `blazingArrow1`, `flashFire4`, `titanicEarthPulse1`.
- **The pool's members:** Lavu, Volcanic Eruption and Summon Gaos are kept out of `cast3.skills`. Their tiles are their own sequences, the War Capital precedent: a member whose tile id is taken would get a random member's cues.

### 7. What is ready

- **Effects** (inventory + probe): blazingArrow, flashFire, flashFire_ring, earthPulse_ring, earthPulse_hit, instantCast, fireBall_hit, fireSoul_ring, earthSoul_ring, groundLock_hit, secondStone, stoneHammer, lavu_ring, phoenixArmor, phoenixArmor_create, gadinaArmor, gadinaArmor_create, volcanicEruption_ring.
  - castRing and castEffect_fire are the hero prefab's fields, loaded by their Resources names. Neither is in the inventory; the probe reads both whole (open question 12).
- **Voices** (all in BB's rip except blazingArrow): cast, fireBall, phoenix, ja, worldIgnition, groundLock, gadina, stoneHammer, buiten, lavu, sAttack3, volcanicEruption, flashFire, earthPulse, unsummon.
- **Effect sounds** (`monkey/sounds`): blazingArrow, castEffect, castRing, earthPulse_fire, earthPulse_hit, earthSoul, earthform_create, fireAvatar_create, fireBall, fireSoul, fireball_hit, flashFire, groundLock, instantCast, secondStone, stoneHammer, volcanicEruption.
  - lavu_summon is in `elementals/lavu/sounds` (P6).

---

## damageCast1 / damageCast2: the channel (plain entries)

Covered in Read this first 2.

**damageCast1:**
- Voice `cast` at 0.

**damageCast2:**
- `castRing` at 0, `cut` 0.05. The step lasts 0 s on the page, and fxStart cuts a followState effect whose cut lies past its step at the step change.
- `instantCast` at 0 with `p` 0.12 (Auto Instant).

Not cued:
- The motion blur of the instant cast (:25078).
- The Damage Cast hits: within 2 m of the hero, nothing (the target stands 10 m ahead).

## cast3: the Cast pool (`skills`), 10 members

| member | voice | 0.3 | payload | source |
|---|---|---|---|---|
| fireBall | fireBall | castEffect_fire | 0.4 fireBall4 from (0, 1, 1) toward the 10 m target 0.6 m up (2.54° down, 30 m/s); 0.69 fireBall_hit at the body (d 9.7, y 0.61) | :26315-26750; :11092-11318; Monkey_fireBall.cs:13-200 |
| phoenix | phoenix | castEffect_fire | 0.4 fireSoul_ring at the hero; Phoenix4 2 m ahead (summon, then root), cut at 10 s | :26755-27110; :11345-11759; Phoenix.cs:4564-5072 |
| ja | ja | castEffect_fire | 0.4 Ja4 2 m ahead, cut at 10 s | :28920-29275; :12049-12207; Ja.cs:1702-2049 |
| worldIgnition | worldIgnition | castEffect_fire | the ignite status on the foe only (left out) | :29700-30080 |
| groundLock | groundLock | castEffect_fire | 0.4 groundLock_hit at the target; 3.4 secondStone at the target (#403) | :30402-30820; :30960-31170 |
| gadina | gadina | castEffect_fire | 0.4 earthSoul_ring at the hero; Gadina4 2 m ahead (standby 1.5 s), cut at 10 s | :31217-31570; :12580-12960; Gadina.cs:5944-6505 |
| stoneHammer | stoneHammer | castEffect_fire | 0.4 stoneHammer at the target | :32896-33280; :33400-33560 |
| buitenHouHou | buiten | castEffect_fire | 0.4 Buiten4 2 m ahead (create clip, its summon sound and effect), cut at 10 s | :33609-33960; :13327-13460; Buiten.cs:557-816 |
| fireAvatar | sAttack3 | castEffect_fire | 0.7 the hero hidden, phoenixArmor on him (summon, then root at 1.5 s), phoenixArmor_create ×2; cut at 10 s | :38208-38700; CharacterControl.cs status 'fireAvatar' |
| earthForm | sAttack3 | castEffect_fire | 0.7 gadinaArmor on him (summon, then root at 1.2 s), gadinaArmor_create; the hero stays visible; cut at 10 s | :40508-40972; status 'earthForm' |

- Ground Lock's second stone comes in the idle tail (index.html play(): the skill's cues run on after its last step).
- **Fire Avatar's form:**
  - The status turns every renderer under the hero off and the armor's renderers on (CharacterControl.cs, status add 'fireAvatar').
  - That is the page's whole-hero `hideProp` for 10 s.
  - The armor's create effect is made twice by the game (:38461 inside the armor branch, :38503 after it): both are cued.
- Earth Form's status changes only stats and race, so the hero is not hidden.

## Lavu (`@Lavu:cast3`)

- **0:** voice lavu.
- **0.3:** castEffect_fire. The summon would be unsummoned; there is none.
- **0.4:**
  - `lavu` 3 m ahead, 2 m under the floor, rotated Euler(−90, 0, 0) (Monkey_lavu, P3).
  - `lavu_ring` 3 m ahead.
  - Sound `lavu_summon` (P6).
- **2.4:** the 60 s lavu status ends here on the tile (it draws nothing); the cut is at 10 s.
- **Standby:** at 2.4 s, after ten 0.2 s waits with shakes. That is why the tile has its own sequence: `cast3~@2.4` holds the clip's last frame.

## Volcanic Eruption (`@VolcanicEruption:cast3`)

- **0:** voice.
- **0.3:**
  - `volcanicEruption_ring` at the hero (life 12, followState).
  - `volcanicEruption` at the target, 10 m ahead (life 12 + 3; its looping sound under AudioControl; three Shuriken systems in TTO's copy, P5).
- **Then:** 22 ticks of 0.5 s (hits only), and standby at 12.0 s.
- **On the page:** the field is cut at 10 s (`kill` 10 from 0.3, the ring's `cut` 10.25), and `cast3~@10.3` keeps the hero in the cast pose. The game destroys the volcano if he leaves it (:43665-43673).

## Summon Gaos (`@SummonGaos:damageCast2`, `@SummonGaos:cast3`)

**The channel:**
- An 8 s bar (88 %), or Auto Instant's 0 s with the instantCast flash (12 %).
- `"damageCast2*~@8%88|damageCast2*~@0"`. Each cue carries `alt` (P8): the ring cut 7.95 in alternative 0, cut 0.05 plus instantCast in alternative 1.

**The release:**
- 0.3: castEffect_fire.
- 0.4: Gaos 9 m ahead (summon, root at 2.7 s), cut at 10 s.
- The Fire Soul ring is missing (Read this first 5). No voice.

## Fire Keep (`@FireKeep:cast3`, SEQ "Fire Keep: cast3")

- The stored ball's release on the next normal attack (:10020-10024), at level 4.
- cast3, castEffect_fire, then fireBall4 and its hit exactly as the Fireball tile's.
- No voice.
- The 1 s `fireKeep` flash belongs to the store, an earlier untargeted Fireball, so it is not on this tile.

## Blazing Arrow (`blazingArrow`, 4.0 s)

| time | what happens | source |
|---|---|---|
| 0 | clip (0.2 s fade) | :27881 |
| 0 | voice blazingArrow (TTO's recording) | :27917-27933 |
| 0 | the current summon unsummoned (none) | :27942-27954 |
| 1.0 | `blazingArrow` at the hero (life 4, the arrow mesh's 4 s clip, its own sound) | :27697-27715 |
| 3.0 | blazingArrow_fire: 12 hits 0.15 s apart (damage and the foe's burn: left out) | :27777; :28015-28355 |
| 3.8 | standby | :27825 |
| 4.8 | with no summon out, a 24 % roll: Phoenix4 2 m behind the hero, facing forward, with the Fire Soul ring | :28265-28288 |

- The Phoenix is cued with `p` 0.24 and one roll for both cues, cut at 10 s.
- The 4.8 s cues come in the idle tail.

## Flash Fire (`flashFire`, 3.2 s)

| time | what happens | source |
|---|---|---|
| 0 | voice | — |
| 0 | `flashFire_ring` (followState) | :28808-28824 |
| 0.6, 0.9, … 2.7 | eight `flashFire` bursts at the hero (i < sLv × 2) | :28550-28568, :28716, :28854 |
| 2.9 | standby: the ring's cut | :28652-28674 |

## Titanic Earth Pulse (`earthPulse`, 8.0 s)

| time | what happens | source |
|---|---|---|
| 0 | voice unsummon | :32430 |
| 0 | the Gadina4 spent (not on the page, open question 7) | :32455-32492 |
| 0 | noForce 7 s | :32403 |
| 0 | `earthPulse_ring` at the hero (life 7 + 1, followState; the earth beam with the Gadina's shield and sword) | :32495-32511 |
| 4.0 | voice earthPulse | :32222 |
| 5.0 | `earthPulse` from (0, 1, 5), 15 m/s flat (Monkey_earthPulse, P2) | :32272-32277; :13090-13115 |
| 5.31 | `earthPulse_hit` at the target's front, Euler(270, 90, 0) | Monkey_earthPulse.cs:91-194; :32806-32818 |
| 7.5 | standby: the ring's cut | :32335 |

## cast1 / cast2 / damageCast3: no entries

- cast1 / cast2 are played only without Damage Cast, which passives-on excludes. They go in LOWER_RANK, so they get no tile and no cue key; the check would fail on a key with no tile.
- damageCast3 is never played: NEVER_PLAYED, as the Wolf's cast1-3, the Bison's volcanicRam, the Cat's shikifujin and the Chameleon's focusFire.

---

## Paste-ready cue entries for wardrobe/fx_cues/monkey.json

Checked in `C:\work\12tails-wardrobe\checks\fx_monkey_research\skills_a\cues.json` (`check.py`: 11 keys, 75 cues, every time list in order; only `alt` is new). Merge these keys with the other reports' keys into the one object.

```json
{
  "damageCast1": {
    "why": "Monkey.cs RPC_cast ($RPC_cast$24449 :24676-26292), the cast channel of Fireball, Phoenix, Ja, World Ignition, Ground Lock, Gadina, Stone Hammer, Buiten Hou Hou, Lavu, Fire Avatar, Earth Form, Volcanic Eruption and Summon Gaos (the sType switch :25142-25429, the release switch :25700-26194); with Damage Cast #102/#103 learned (passives on: getDamageCastLv() > 0, Monkey.cs:10820-10823, read at :25122) the channel plays damageCast1 / damageCast2 in place of cast1 / cast2 (:25472-25491, :24845-24864): at 0 actionState attack, myCommand cast (:25435-25445), clip damageCast1 (0.2 fade, Once, :25478, :25492), voice cast (one file, Voices/cast :25537, PlayOneShot :26217); Yield(2, 0.7) (:26208): damageCast2",
    "cues": [
      [0, "voice", "cast"]
    ]
  },
  "damageCast2": {
    "why": "Monkey.cs RPC_cast case 2 at 0.7 s (:24826-25101): damageCast2 (0.2 fade, :24851) looped (:24865), the prefab field castRing (= Resources monkey/effects/castRing; probe: EffectControl life 999, followPosition, followState, its own looping Sounds/castRing) Instantiated at the hero, hero rotation (:24882, InitEffectControl :24892); castTime = now + magAdjust(cast time) (:24989, :25430: the 0.1 s floor at high MAG for every member but Summon Gaos, CharacterControl.cs:20584-20588; the page: no cast bar, the SEQ's damageCast2*~@0); Auto Instant #431 (passives on): Random.Range(0, 100) < lckAdjust(12) = 12 % at the stat-free LCK 1 (:25008-25016, CharacterControl.cs:20658-20670) sets castTime 0 and createEffect(instantCast) at the hero, hero rotation (:25025-25048; probe: life 1, followPosition, its own Sounds/instantCast; the motion blur :25078 left out); the instantCast status (Instant Cast, an active buff) is not on; then each frame (YieldDefault(3) :26204) the Damage Cast hits (every 0.4 s, FindAreaTarget 2 m around the hero :25599-25681: nothing within 2 m of a hero whose target stands 10 m ahead, nothing drawn) and, once Time >= castTime (:25692), the skill's RPC_<skill>_cast (:25700-26194), which sets myCommand to the skill: the ring's followState ends there (EffectControl.cs:110-150 records actionState and myCommand, :190-215 ends the effect when either changes), on the page at the step change (cut 0.05, written past the 0 s step: fxStart cuts it at the change)",
    "cues": [
      [0, "fx", "castRing", {"cut": 0.05}],
      [0, "fx", "instantCast", {"p": 0.12}]
    ]
  },
  "cast3": {
    "why": "cast3 is the release clip of the RPC_cast channel's skills (one RPC_<skill>_cast each, started by the release switch Monkey.cs:25700-26194; TTO1102 has the same 14 players, the <RPC_*_cast> coroutines' cast3 strings); each member below is its own tile (poolChains, with the Cast sequence's steps); Lavu, Volcanic Eruption and Summon Gaos have their own sequences (their hold / bar), Fire Keep plays cast3 from the normal attack with no channel (:10020-10024): their keys @<Skill>:cast3",
    "skills": {
      "fireBall": {
        "why": "Monkey.cs RPC_fireBall_cast (:26315-26750), Fireball rank 4, a target locked (tID != 0: Fire Keep #402's store only for an untargeted cast, :25705-25770): at 0 clip cast3 (0.2 fade, Once, :26633-26636), voice fireBall (Voices/fireBall :26663, PlayOneShot :26707); Yield 0.3 (:26696): the prefab field castEffect_fire (= Resources monkey/effects/castEffect_fire; probe: life 2, its own Sounds/castEffect) Instantiated at the hero + TransformDirection(0, 1, 1), hero rotation (:26461); Yield 0.1 (:26703): RPC_fireBall_fire (:26507-26529, Monkey.cs:11092-11291) from position + (0, 1, 1) toward the target's bounds centre (the 10 m target 0.6 m up: LookRotation(0, -0.4, 9), 2.54 degrees down), Effects/fireBall4 (sLv 4, :11236-11248), ProjectileControl life 2 x rangeMod (:11278); Monkey_fireBall flies 30 m/s along its rotation (Monkey_fireBall.cs:13-51); at the target body (front 9.7 m ahead, 8.71 m of flight = 0.29 s) OnTriggerEnter (Monkey_fireBall.cs:91-200) RPC_fireBall_hit: Effects/fireBall_hit at the contact, hero rotation (:11308-11318; life 2, its own Sounds/fireball_hit); the burn status on the foe left out; Yield 0.4 (:26705): FireRune(), standby at 0.8 s (:26569-26574)",
        "cues": [
          [0, "voice", "fireBall"],
          [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}],
          [0.4, "fx", "fireBall4", {"d": 1, "y": 1, "rot": [2.54, 0, 0], "to": [0, 0.6, 10]}],
          [0.69, "fx", "fireBall_hit", {"d": 9.7, "y": 0.61}]
        ]
      },
      "phoenix": {
        "why": "Monkey.cs RPC_phoenix_cast (:26755-27110), Phoenix rank 4: at 0 clip cast3 (0.2 fade, Once, :27025-27028), voice phoenix (:27055, :27098); Yield 0.3 (:27104): castEffect_fire at the hero + (0, 1, 1), hero rotation (:26879); Yield 0.1 (:27094): at 0.4 s RPC_phoenix_create4 (ActionEvent :26939: online the sender's own create runs too, the create codes -211 ... -214 are not gated by isMine, Monkey.cs:5182-5195) at getSpawnPos(position + 2 x forward) (:26914), LookRotation(forward) (Monkey.cs:11345-11759): Fire Soul #422 (passives on): Effects/fireSoul_ring at the hero (:11365-11389; life 1, followPosition, its own Sounds/fireSoul); the previous summon unsummoned (none); Characters/Elementals/Phoenix/Phoenix4 (:11541-11559), Phoenix.summon (:11740; Phoenix.cs:4564-5072: Play(summon) Once, its summon_ring field at its feet, Quaternion.identity, Yield 1, standby: root); no despawn timer (the Bible's infinity chip): cut at 10 s; its AI (Phoenix_AI.cs) left out (open question 4); Yield 0.4 (:27092): standby at 0.8 s (:26966)",
        "cues": [
          [0, "voice", "phoenix"],
          [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}],
          [0.4, "fx", "fireSoul_ring"],
          [0.4, "fx", "Phoenix4", {"d": 2, "kill": 10}]
        ]
      },
      "ja": {
        "why": "Monkey.cs RPC_ja_cast (:28920-29275), Ja rank 4: at 0 clip cast3 (0.2 fade, Once, :29190-29193), voice ja (:29220, :29264); Yield 0.3 (:29262): castEffect_fire at the hero + (0, 1, 1) (:29044); Yield 0.1 (:29270): at 0.4 s RPC_ja_create4 (ActionEvent :29104) at getSpawnPos(position + 2 x forward) (:29079), LookRotation(forward): Characters/Elementals/Ja/Ja4 (Monkey.cs:12049-12061), Ja.summon (:12207; Ja.cs:1702-2049: Play(summon) Once, summon_ring at its feet, Yield 1, standby: root); no despawn timer: cut at 10 s; its AI left out; Yield 0.4 (:29268): standby at 0.8 s (:29131); TTO's Ja Ascension #452 (released) swaps this release for RPC_jaAscension_cast when learned (TTO1102:Monkey.<RPC_cast>d__178::MoveNext@0x1CE8830): open question 9",
        "cues": [
          [0, "voice", "ja"],
          [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}],
          [0.4, "fx", "Ja4", {"d": 2, "kill": 10}]
        ]
      },
      "worldIgnition": {
        "why": "Monkey.cs RPC_worldIgnition_cast (:29700-30080), World Ignition rank 2: at 0 clip cast3 (0.2 fade, Once, :29993-29996), voice worldIgnition (:30023, :30072); Yield 0.3 (:30065): castEffect_fire at the hero + (0, 1, 1) (:29835); Yield 0.1 (:30061): at 0.4 s the ignite status on the target (getDebuff(60), its explosion after 800 / 1200 damage, :29902-29907): a status on a foe, left out (Chameleon decision 53), and its Effects/worldIgnition explosion (:30309) needs that damage, not in a single play; Yield 0.4 (:30067): standby at 0.8 s (:29934)",
        "cues": [
          [0, "voice", "worldIgnition"],
          [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}]
        ]
      },
      "groundLock": {
        "why": "Monkey.cs RPC_groundLock_cast (:30402-30820), Ground Lock rank 4, Second Stone #403 and Aegis of Earth 3 on (passives on): at 0 clip cast3 (0.2 fade, Once, :30736-30739), voice groundLock (:30766, :30801); Yield 0.3 (:30816): castEffect_fire at the hero + (0, 1, 1) (:30537); Yield 0.1 (:30808): at 0.4 s the target locked (groundLock status, getDebuff(3 + 3) :30608-30619, a foe's status: left out), hit (:30625), RPC_groundLock_hit at the target's position (:30633; Monkey.cs:30960-31170): Effects/groundLock_hit there, Quaternion.identity (:31127-31139; life 1, its own Sounds/groundLock); with #403 Yield 3 (:31153-31168): Effects/secondStone at the still-locked target (:31014-31046; life 1, the stone mesh, its own Sounds/secondStone) at 3.4 s, its 0.5 m hit (:31073-31096) draws nothing; Yield 0.4 (:30818): standby at 0.8 s (:30677); the second stone comes in the idle tail",
        "cues": [
          [0, "voice", "groundLock"],
          [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}],
          [0.4, "fx", "groundLock_hit", {"d": 10}],
          [3.4, "fx", "secondStone", {"d": 10}]
        ]
      },
      "gadina": {
        "why": "Monkey.cs RPC_gadina_cast (:31217-31570), Gadina rank 4: at 0 clip cast3 (0.2 fade, Once, :31487-31490), voice gadina (:31517, :31555); Yield 0.3 (:31551): castEffect_fire at the hero + (0, 1, 1) (:31341); Yield 0.1 (:31563): at 0.4 s RPC_gadina_create4 (ActionEvent :31401) at getSpawnPos(position + 2 x forward) (:31376), LookRotation(forward) (Monkey.cs:12580-12960): Earth Soul #423 (passives on): Effects/earthSoul_ring at the hero (:12588-12612; life 1, followPosition, its own Sounds/earthSoul); Characters/Elementals/Gadina/Gadina4 (:12770-12782), Gadina.summon (:12957; Gadina.cs:5944-6505: Play(summon) Once, its summonEffect at its feet, Quaternion.identity (:6269), a 4 x 4 + 8 = 24 m hit (:6344-6367, nothing drawn), Gadina4's Yield 1.5 (:6427-6436, :6502), standby: root); no despawn timer: cut at 10 s; its AI left out; Yield 0.4 (:31568): standby at 0.8 s (:31428)",
        "cues": [
          [0, "voice", "gadina"],
          [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}],
          [0.4, "fx", "earthSoul_ring"],
          [0.4, "fx", "Gadina4", {"d": 2, "kill": 10}]
        ]
      },
      "stoneHammer": {
        "why": "Monkey.cs RPC_stoneHammer_cast (:32896-33280), Stone Hammer rank 4, Stone Sentinel #443 on (damage and KO only): at 0 clip cast3 (0.2 fade, Once, :33192-33195), voice stoneHammer (:33225, :33265); Yield 0.3 (:33271): castEffect_fire at the hero + (0, 1, 1) (:33031); Yield 0.1 (:33261): at 0.4 s RPC_stoneHammer_fire at the target's position (:33093; Monkey.cs:33400-33560): Effects/stoneHammer there, Quaternion.identity (:33523-33533; life 3, the hammer mesh with its root clip, its own Sounds/stoneHammer), Yield 1 (:33554): the camera shake (:33436) and the hit (:33458-33463) at 1.4 s draw nothing; Yield 0.4 (:33278): standby at 0.8 s (:33133)",
        "cues": [
          [0, "voice", "stoneHammer"],
          [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}],
          [0.4, "fx", "stoneHammer", {"d": 10}]
        ]
      },
      "buitenHouHou": {
        "why": "Monkey.cs RPC_buiten_cast (:33609-33960; sType buiten, the card Buiten Hou Hou, icon monkey_buitenHouHou4), rank 4: at 0 clip cast3 (0.2 fade, Once, :33879-33882), voice buiten (:33909, :33954); Yield 0.3 (:33956): castEffect_fire at the hero + (0, 1, 1) (:33733); Yield 0.1 (:33948): at 0.4 s RPC_buiten_create4 (ActionEvent :33793) at getSpawnPos(position + 2 x forward) (:33768), LookRotation(forward): Characters/Elementals/Buiten/Buiten4 (Monkey.cs:13327-13339), Buiten.summon (:13460; Buiten.cs:557-816: Play(create) Once, PlayOneShot(buiten_summonFX) (:779), its summonEffect at its feet, its rotation (:791), Yield 1, standby: root); no despawn timer: cut at 10 s; Yield 0.4 (:33942): standby at 0.8 s (:33820); TTO's Buiten Bastion (released) on the same branch: the tto report",
        "cues": [
          [0, "voice", "buiten"],
          [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}],
          [0.4, "fx", "Buiten4", {"d": 2, "kill": 10}]
        ]
      },
      "fireAvatar": {
        "why": "Monkey.cs RPC_phoenixArmor_cast (:38208-38700; sType fireAvatar :26057-26063), Fire Avatar (one rank; cast bar 9 s, magAdjust's 0.1 s floor, instant allowed by Auto Instant #431, :25314-25342): at 0 clip cast3 (0.2 fade, Once, :38621), voice sAttack3 (:38651, :38696); Yield 0.3 (:38684): castEffect_fire at the hero + (0, 1, 1) (:38321), the summon unsummoned (none, :38326-38338); Yield 0.4 (:38688): at 0.7 s the fireAvatar status (5, chaAdjust(120), :38371): the hero becomes Elementals and every renderer under him off, the armor's on (CharacterControl.cs status add 'fireAvatar': the page's whole-hero hideProp), Effects/phoenixArmor parented to the hero, local 0 / identity, Play(summon) (:38383-38438; its Animation root / run / nAttack / blazingForm1 / blazingForm2 / summon), phoenixArmor_create at the hero, created twice (:38461 inside the armor branch, :38503 after it; life 1, its own Sounds/fireAvatar_create); Yield 0.8 (:38686): standby at 1.5 s (:38562), from which Monkey.Update crossfades the armor to root looped (:471-523; anims 0.8 s after its spawn); the 120 s form cut at 10 s (the armor and the hide); the motion blur (:38530) left out",
        "cues": [
          [0, "voice", "sAttack3"],
          [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}],
          [0.7, "hideProp", "hero", {"kill": 10}],
          [0.7, "fx", "phoenixArmor", {"kill": 10, "anims": [[0, "summon"], [0.8, "root"]]}],
          [0.7, "fx", "phoenixArmor_create"],
          [0.7, "fx", "phoenixArmor_create"]
        ]
      },
      "earthForm": {
        "why": "Monkey.cs RPC_gadinaArmor_cast (:40508-40972; sType earthForm :26083-26089), Earth Form (one rank; 9 s bar, the 0.1 s floor, instant allowed by #431, :25343-25371): at 0 clip cast3 (0.2 fade, Once, :40881), voice sAttack3 (:40911, :40952); Yield 0.3 (:40950): castEffect_fire at the hero + (0, 1, 1) (:40621), the summon unsummoned (none, :40632); Yield 0.4 (:40964): at 0.7 s the earthForm status (5, chaAdjust(120), :40671: Race Elementals, ATK / DEF + 100, no renderer change, CharacterControl.cs status add 'earthForm': the hero stays visible), the camera shake (:40683) left out, Effects/gadinaArmor parented to the hero, local 0 / identity, Play(summon) (:40695-40747; its Animation root / run / summon / nAttack1-3 / cAttack0-2), gadinaArmor_create at the hero (:40758-40770; life 1, followPosition, its own Sounds/earthform_create); Yield 0.5 (:40944): standby at 1.2 s (:40822), from which Monkey.Update crossfades the armor to root looped (:573-587; anims 0.5 s after its spawn); the 120 s form cut at 10 s",
        "cues": [
          [0, "voice", "sAttack3"],
          [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}],
          [0.7, "fx", "gadinaArmor", {"kill": 10, "anims": [[0, "summon"], [0.5, "root"]]}],
          [0.7, "fx", "gadinaArmor_create"]
        ]
      }
    }
  },
  "@Lavu:cast3": {
    "why": "Monkey.cs RPC_lavu_cast (:34386-34870), Lavu rank 2 (cast bar 9 + 3 x 2 = 15 s, magAdjust's 0.1 s floor, :25297-25313): at 0 clip cast3 (0.2 fade, Once, :34785-34788), voice lavu (:34815, PlayOneShot :34864); Yield 0.3 (:34862): castEffect_fire at the hero + (0, 1, 1) (:34510), the summon unsummoned (none, :34515-34523; the Lavu's sacrifice is ToT's, the Bible's line 1033); Yield 0.1 (:34858): at 0.4 s RPC_lavu_summon at position + TransformDirection(0, -2, 3) (3 m ahead, 2 m under the floor, :34550-34561; Monkey.cs:13876-13920): Effects/lavu, LookRotation(forward) x Euler(-90, 0, 0) (:13889-13899), Monkey_lavu.summon (:13915; Monkey_lavu.cs:151-467: the serpent's body chain rising, its head and segments, rotationControl; part P3); the lavu status chaAdjust(60) (:34579-34590: no look, CharacterControl.cs status add 'lavu' is empty) cut at 10 s; Effects/lavu_ring 3 m ahead, Quaternion.identity (:34606-34624; life 2.4); the hero's PlayOneShot of Characters/Elementals/Lavu/Sounds/lavu_summon (:34638-34656: a sound cue, SOUND_ALIASES); then ten 0.2 s waits (case 4 :34677-34683, Yield(4, 0.2) :34848) with a camera shake each (left out): standby at 2.4 s (:34691-34740): the SEQ's cast3~@2.4 holds the clip's last frame",
    "cues": [
      [0, "voice", "lavu"],
      [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}],
      [0.4, "fx", "lavu", {"d": 3, "y": -2, "rot": [-90, 0, 0], "kill": 10}],
      [0.4, "fx", "lavu_ring", {"d": 3}],
      [0.4, "sound", "lavu_summon"]
    ]
  },
  "@VolcanicEruption:cast3": {
    "why": "Monkey.cs RPC_volcanicEruption_cast (:43326-43870), Volcanic Eruption (one rank; 15 s bar, the 0.1 s floor, instant allowed by #431, :25372-25400); its spot dQs7x5UeNh = the target's position (RPC_cast case 2 :24942-24978; 20 m ahead only without a target): at 0 clip cast3 (0.2 fade, Once, :43766-43771), voice volcanicEruption (:43811, :43863), no castEffect_fire; Yield 0.3 (:43855): Effects/volcanicEruption_ring at the hero, hero rotation (createEffect :43451-43469; life 12, followPosition, followState) and Effects/volcanicEruption at the target, Quaternion.identity (createEffect :43488-43506; probe: life 12 + afterLife 3, its root clip, its looping Sounds/volcanicEruption under AudioControl fade-in 0.5 / middle 11 / fade-out 0.5; a Shuriken system: part P5); the red colour ramp and the shakes (:43531, :43548, :43651) left out; then 22 ticks 0.5 s apart (Yield(3, 0.5) :43861, i < 22 :43836), each a 12 m / 6 m hit (:43584-43633, nothing drawn), the volcano destroyed if the hero leaves the attack (:43665-43673); Yield 0.7 (:43853): standby at 12.0 s (:43698): the field cut at 10 s (kill 10 from 0.3, the ring's followState cut 10.25 inside the SEQ's cast3~@10.3 hold)",
    "cues": [
      [0, "voice", "volcanicEruption"],
      [0.3, "fx", "volcanicEruption_ring", {"cut": 10.25}],
      [0.3, "fx", "volcanicEruption", {"d": 10, "kill": 10}]
    ]
  },
  "@SummonGaos:damageCast2": {
    "why": "Monkey.cs RPC_cast case 2 for Summon Gaos (as damageCast2's entry, :24826-25101): the castRing at the hero (:24882) and the bar magAdjust(24) (:25401-25430) = 24 - 512 / 32 = 8 s at the highest MAG (CharacterControl.cs:20584-20588), the SEQ's first alternative damageCast2*~@8 (88 %): the ring's followState cut 7.95; with Auto Instant #431 (canInstantCast kept, :25417-25428) the 12 % roll (lckAdjust(12) at LCK 1, :25008-25016) skips the bar: the second alternative damageCast2*~@0 with instantCast at the hero (:25025-25048) and the ring cut at the step change; each cue plays only in its alternative (the new cue option alt, part P8)",
    "cues": [
      [0, "fx", "castRing", {"cut": 7.95, "alt": 0}],
      [0, "fx", "castRing", {"cut": 0.05, "alt": 1}],
      [0, "fx", "instantCast", {"alt": 1}]
    ]
  },
  "@SummonGaos:cast3": {
    "why": "Monkey.cs RPC_summonGaos_cast (:43919-44210), Summon Gaos (one rank): at 0 clip cast3 (0.2 fade, Once, :44178-44181), no voice (none is loaded); Yield 0.3 (:44197): castEffect_fire at the hero + (0, 1, 1) (:44032); Yield 0.1 (:44199): at 0.4 s RPC_summonGaos_create (ActionEvent :44092) at getSpawnPos(position + 9 x forward) (:44067), LookRotation(forward) (Monkey.cs:14370-14600): Fire Soul #422 (passives on) asks Effects/volcanicSoul_ring at the hero (:14375-14399), which is in neither BB's data nor TTO's catalog (probe: KeyError / not in TTO's catalog): 'Cannot find' and nothing drawn; Characters/Elementals/Gaos/Gaos (:14432-14444), Gaos.summon (:14595; Gaos.cs:4690-4926: Play(summon) Once, createEffect(summon_ring) at its feet, its rotation (:4885), Yield 0.8 (a 3 shake, left out), Yield 0.7 (a motion blur, left out), Yield 1.2, standby at 2.7 s: root); no despawn timer: cut at 10 s; Yield 0.4 (:44195): standby at 0.8 s (:44119)",
    "cues": [
      [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}],
      [0.4, "fx", "Gaos", {"d": 9, "kill": 10}]
    ]
  },
  "@FireKeep:cast3": {
    "why": "Fire Keep #402 (passive, Bible 4.x 'fireKeep'): an untargeted Fireball stores a ball (the fireKeep status, Monkey.cs:25705-25748, its 1 s Effects/fireKeep flash at the store, CharacterControl.cs status add 'fireKeep', not on this tile), and the next normal attack releases it in place of the Combo (:10020-10024): Monkey.cs RPC_fireKeep_cast (:36855-37225) at the stored level 4: at 0 LookAt the target, clip cast3 (0.2 fade, Once, :37179-37185), no voice; Yield 0.3 (:37220): castEffect_fire at the hero + (0, 1, 1) (:37012); Yield 0.1 (:37209): RPC_fireBall_fire from position + (0, 1, 1) toward the target's bounds centre (:37047-37087): fireBall4 and its hit as the Fireball tile's; Yield 0.4 (:37216): standby at 0.8 s (:37132); the status decrement (:10039-10055) draws nothing",
    "cues": [
      [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}],
      [0.4, "fx", "fireBall4", {"d": 1, "y": 1, "rot": [2.54, 0, 0], "to": [0, 0.6, 10]}],
      [0.69, "fx", "fireBall_hit", {"d": 9.7, "y": 0.61}]
    ]
  },
  "blazingArrow": {
    "why": "Monkey.cs RPC_blazingArrow (:27560-27985), Blazing Arrow #234 (one rank): at 0 actionState attack (:27860-27869), clip blazingArrow (0.2 fade, Once, :27881-27884), voice blazingArrow (Voices/blazingArrow :27917, PlayOneShot :27929): not in BB's data (voices/ has no blazingArrow.wav: 'Cannot find blazingArrow voice', :27933); TTO loads the same address (TTO1102:Monkey.<RPC_blazingArrow>d__188::MoveNext@0x1CE4340) and its catalog has gameassets/characters/heroes/monkey/voices/blazingarrow (checks/fx_monkey_research/skills_a/probe/cat_keys.txt): TTO's recording, as the Sheep's decision 10 (part P7); the current summon unsummoned (none, :27942-27954); Yield 1 (:27976): Effects/blazingArrow at the hero, hero rotation (Instantiate :27697-27715; probe: life 4, the arrow mesh's 4 s root clip, AlphaTimer, trail, its own Sounds/blazingArrow), the zoom blur (:27750) left out; Yield 2 (:27972): at 3.0 s blazingArrow_fire (:27777; Monkey.cs:28015-28355): 12 hits 0.15 s apart, 3.5 m circles at 3 i + 2 m ahead (:28133-28215, Yield 0.15 :28305; damage and the foe's burn only); after the 12th, at 3.0 + 12 x 0.15 = 4.8 s, with no summon out: Random.Range(0, 100) < lckAdjust(24) = 24 % at LCK 1 (:28265-28271, CharacterControl.cs:20658-20670): RPC_phoenix_create4 at getSpawnPos(position - 2 x forward), LookRotation(forward) (:28277-28288; the create as the Phoenix tile's: Fire Soul's fireSoul_ring at the hero, Phoenix4), cut at 10 s: in the idle tail; Yield 0.8 (:27974): standby at 3.8 s (:27825)",
    "cues": [
      [0, "voice", "blazingArrow"],
      [1, "fx", "blazingArrow"],
      [4.8, "fx", "fireSoul_ring", {"p": 0.24, "roll": "blazingPhoenix"}],
      [4.8, "fx", "Phoenix4", {"d": -2, "kill": 10, "p": 0.24, "roll": "blazingPhoenix"}]
    ]
  },
  "flashFire": {
    "why": "Monkey.cs RPC_flashFire (:28360-28915), Flash Fire rank 4: at 0 actionState attack (:28726-28735), clip flashFire (0.2 fade, Once, :28747-28750), voice flashFire (:28783, :28795) and Effects/flashFire_ring at the hero, hero rotation (createEffect :28808-28824; probe: life 4, followPosition, followState, its own Sounds/flashFire); Yield 0.3 (:28859): the motion blur (:28518) left out; then while i < sLv x 2 = 8 (:28716), Yield 0.3 (:28854) and a burst: Effects/flashFire at the hero, hero rotation (createEffect :28550-28568; life 1), its 5 m hit (:28593-28632, nothing drawn): at 0.6, 0.9, ... 2.7 s; Yield 0.2 (:28856): standby at 2.9 s (:28652-28674): the ring's followState cut 2.9 (inside the 3.2 s clip)",
    "cues": [
      [0, "voice", "flashFire"],
      [0, "fx", "flashFire_ring", {"cut": 2.9}],
      [0.6, "fx", "flashFire"],
      [0.9, "fx", "flashFire"],
      [1.2, "fx", "flashFire"],
      [1.5, "fx", "flashFire"],
      [1.8, "fx", "flashFire"],
      [2.1, "fx", "flashFire"],
      [2.4, "fx", "flashFire"],
      [2.7, "fx", "flashFire"]
    ]
  },
  "earthPulse": {
    "why": "Monkey.cs RPC_earthPulse (:32100-32593), Titanic Earth Pulse #334 (one rank; needs a Gadina4 and spends it, the Bible's 2.3): at 0 actionState attack, myCommand earthPulse (:32370-32379), clip earthPulse (0.2 fade, Once, :32391-32394), noForce 7 s (:32403, nothing drawn), voice unsummon (:32430, :32442), the Gadina unsummoned (its HP kept for the damage, :32455-32492; not on the page: open question 7), Effects/earthPulse_ring at the hero, hero rotation (createEffect :32495-32511; probe: life 7 + afterLife 1, followPosition, followState, the earth beam mesh with the Gadina shield / sword, its own Sounds/earthPulse_fire); Yield 4 (:32558): at 4.0 s voice earthPulse (:32222, :32553); Yield 1 (:32545): at 5.0 s RPC_earthPulse_fire from position + TransformDirection(0, 1, 5), LookRotation(forward) (:32272-32277; Monkey.cs:13090-13115: Effects/earthPulse, ProjectileControl life 3), Monkey_earthPulse flies 15 m/s along it (Monkey_earthPulse.cs:13-63), at the target body (front 9.7 m ahead: 4.7 m = 0.31 s) OnTriggerEnter (:91-194) RPC_earthPulse_hit at the contact (Monkey.cs:32598-32855): Effects/earthPulse_hit there, Euler(270, 90, 0) (:32806-32818; life 3, its own Sounds/earthPulse_hit), five growing hits 0.2 s apart (:32704-32762, nothing drawn), shakes and the motion blur (:32308, :32847) left out; Yield 2.5 (:32556): standby at 7.5 s (:32335): the ring's followState cut 7.5",
    "cues": [
      [0, "voice", "unsummon"],
      [0, "fx", "earthPulse_ring", {"cut": 7.5}],
      [4, "voice", "earthPulse"],
      [5, "fx", "earthPulse", {"d": 5, "y": 1, "to": [0, 1, 9.7]}],
      [5.31, "fx", "earthPulse_hit", {"d": 9.7, "y": 1, "rot": [270, 90, 0]}]
    ]
  }
}
```

## Parts summary

| part | what | for |
|---|---|---|
| P1 the elemental summons | Extractor: `EXTRA_FOLDERS["monkey"]` = Characters/Elementals (Phoenix4, Ja4, Gadina4, Buiten4, Gaos), data-only layouts for Phoenix / Ja / Gadina / Buiten / Gaos and their _AI scripts, their summon_ring / summonEffect fields, Buiten's buiten_summonFX clip. Page (a `fxparts/monkey.js`, as robots.js): summon (Buiten: create) Once with the field effect at its feet, then the standby branch's root looped. Standby after 1 s (Phoenix, Ja, Buiten), 1.5 s (Gadina4) or 2.7 s (Gaos). No AI. Shared with skills_b's summon commands | Phoenix, Ja, Gadina, Buiten Hou Hou, Summon Gaos, Blazing Arrow's Phoenix |
| P2 the projectiles | `Monkey_fireBall` (layout `mLv` i, Monkey_fireBall.cs:327; 30 m/s along the spawn rotation, ProjectileControl life 2; ends at `to`'s body) and `Monkey_earthPulse` (no fields; 15 m/s, life 3; ends at `to`). The hits are their own cues | Fireball, Fire Keep, Titanic Earth Pulse |
| P3 Monkey_lavu + rotationControl | The inventory's "needs". Monkey_lavu.summon (Monkey_lavu.cs:151-467): the body's segment chain behind its head, rising over its first 2 s (:436). Its layout and motion need the parts stage's full read | Lavu |
| P4 the armor clip schedule | phoenixArmor / gadinaArmor play `summon`, then `root` looped at the cue's `anims` ages (Monkey.cs:471-587). Either a monkey.js part as cat.js's fx:grandCasinoArcade, or `anims` made general in mesh.js | Fire Avatar, Earth Form |
| P5 volcanicEruption's Shuriken | `SHURIKEN_FROM_TTO["monkey"] = ["volcanicEruption"]` (TTO's copy reads whole: 3 ParticleSystems, probe_tto_ve.json), as the Mole's warCapital | Volcanic Eruption |
| P6 a sound alias | `SOUND_ALIASES["monkey"]["lavu_summon"] = "characters/elementals/lavu/sounds/lavu_summon"` | Lavu |
| P7 a TTO voice | voices/blazingarrow from TTO's bundle -> sfx/v_blazingArrow.mp3 (wardrobe_fx_tto.py, beside SKILL_SOUNDS: a voices/ list) | Blazing Arrow |
| P8 cue option `alt` | `alt: k`: the cue plays only when its step's drawn alternative is k (C.seq.alt; fxStart's filter, beside `worn`); add to wardrobe_fx_check.py OPTS | Summon Gaos |

Inventory: add Monkey_fireBall, Monkey_earthPulse and Monkey_lavu to BUILT once P2 / P3 exist. The elementals load through EXTRA_FOLDERS.

## Left out (with reasons)

- **Statuses on a foe** (Chameleon decision 53): World Ignition's ignite, and its worldIgnition explosion, which needs 800+ damage; Ground Lock's lock; Blazing Arrow's and Fireball's burn.
- **Damage-only hits:** Damage Cast's 2 m ticks, Blazing Arrow's 12 circles, Flash Fire's 5 m ticks, Stone Hammer's 1 s blow, Volcanic Eruption's 22 ticks, Earth Pulse's five rings, the Gadina's summon hit.
- **Camera effects** (Bison 35, Cat 43, Chameleon 52): motion blurs, the red ramp, the shakes.
- **Others:** the noForce and lavu statuses (no look); the 1 s fireKeep store flash (belongs to an earlier cast); the elementals' AI (open question 4).
- **The hero does not travel or turn:** the casts face the target already.

## Bible findings to offer the user

- `volcanicSoul_ring` (Summon Gaos with Fire Soul #422, Monkey.cs:14375-14399) is loaded by BB and TTO but exists in neither game's data, so the game logs "Cannot find" and shows no ring.
- BB asks for `Voices/blazingArrow` (:27917), which BB's data lacks, so BB's Blazing Arrow is silent. TTO's catalog has the recording.
- Blazing Arrow's Phoenix: 4.8 s after the press (after the 12th hit), with no summon out, a `lckAdjust(24)` chance (24 % at LCK 1) of a Phoenix4 2 m behind the Monkey (:28265-28288). In TTO, only a Phoenix4 is consumed at the cast, not any summon (`ConsumeSummonOfExactType("Phoenix4")`).
- Fire Avatar's create effect is spawned twice (:38461 and :38503).
- The channel's ring appears only when the bar starts (0.7 s), not with cast1. Every release follows 0.3 / 0.4 / 0.8 s, except Fire Avatar 0.7 / 1.5, Earth Form 0.7 / 1.2, Lavu standby 2.4 and Volcanic Eruption 0.3 / 12.0.
- Summon Gaos's bar can never go below 8 s without Auto Instant: magAdjust removes at most 16 s.

## Open questions (recommended answers)

1. **The Cast host with Damage Cast on:**
   - Recommended: one `"Cast: damageCast1 damageCast2*~@0 cast3~"` tile host, the "Damage Cast" line removed, cast1 / cast2 in LOWER_RANK.
   - Damage Cast (a passive) gets no tile of its own. Its look (the clip swap) is on every cast tile, and its hits need an enemy within 2 m (the Bison's Power Hammer precedent, decision 10).
   - The alternative is keeping both tiles, which leaves a passives-off Cast tile.
2. **The castRing on a 0 s bar:** cue it with `cut` 0.05, so it flashes for one frame as in the game at the 0.1 s floor? Recommended: yes, the Chameleon decision 7 convention.
3. **Auto Instant's 12 % flash** on every channel tile (`p` 0.12)? Recommended: yes (random picks as the game makes them). On Summon Gaos it also skips the 8 s bar, hence the alternatives and P8.
4. **The elementals' AI** (the Phoenix shoots, the Gadina fights, the Ja's aura, the Gaos's attacks)? Recommended: keep them standing (summon, then root) for 10 s, the Barrel Bot precedent (Mole decision 32). Offer the AI as a separate job. P1 is shared with skills_b.
5. **Lavu and Volcanic Eruption as own sequences** for their holds (2.4 s, 10.3 s)? Recommended: yes, the Chameleon Tent / Mole War Capital precedents.
6. **Summon Gaos:** an 8 s bar with a 12 % instant alternative? Recommended: yes (the War Capital 8 s precedent, plus the game's roll).
7. **Titanic Earth Pulse's Gadina4** (needed and spent at 0)? Recommended: not shown. It is gone at 0 s, and its unsummon look belongs to skills_b's Unsummon / Summon Release parts. The Detonate precedent (Mole decision on the nuke) differs: there the nuke stands until the blast.
8. **Fire Avatar's hide and double create:** recommended: hide the whole hero for the form's 10 s (the status turns every renderer off), and cue phoenixArmor_create twice, as the code does.
9. **TTO's Ja Ascension #452** (released) swaps the Ja release for a boosted summon when learned (TTO1102:Monkey.<RPC_cast>d__178, the Bible line 917). Recommended: keep BB's release on the Ja tile and let the tto report's Ja Ascension tile show the boosted one (one tile per skill). Buiten Bastion's branch: the same, the tto report.
10. **Blazing Arrow's voice from TTO** (BB has none)? Recommended: yes (P7, the Sheep's decision 10).
11. **The pool member name for Buiten:** `buitenHouHou` (the card's name and icon; the sType is `buiten`)? Recommended: yes.
12. **castRing / castEffect_fire:** these are the hero prefab's fields, read by their Resources names (monkey/effects/castRing, castEffect_fire, both in BB's container and TTO's catalog). Recommended: the parts stage confirms the field PPtrs, as the Penguin's castRing was confirmed. The projectiles' collider radius was not read: the hit times assume the target body's front at 9.7 m (the Penguin's convention). The parts stage checks it.

## Notes for the tto report

- TTO's RPC_cast also releases `buitenBastion`, `jaAscension` and `runeGolem` (the golemCall clip), with their own cast times (0x40400000 = 3, 0x3fc00000 = 1.5, 0x40c00000 = 6 among the mCastTime writes of TTO1102:Monkey.<RPC_cast>d__178::MoveNext@0x1CE8830; which is which is the tto report's).
- Their channel steps can reuse this report's `damageCast1` / `damageCast2` entries: `"<Skill>: damageCast1 damageCast2*~@0 <clip>"`.

## Verification (2026-11-13)

A read-only re-trace by the checker on the office PC. My scripts and outputs are in `checks\fx_monkey_research\verify\`:
- `clean.py`: prints a .cs range with the opaque predicates worked out.
- `blocks.py`: parses both reports' blocks. This one has 11 keys and 75 cues, is valid JSON, and every time list is in order.
- `cont.py` -> `cont.txt`: BB's Resources container (the Monkey's voices, effects and the elementals).
- `voiceclip.py`: decodes BB's own AudioClips.
- `ripgap.py` -> `ripgap.txt`: every class's voices / sounds that the rip lacks.
- `probe.txt` + `psum.py`: `wardrobe_fx.py monkey --probe` of 37 effects.
- `fix.py` -> `a_fixed.json`: this report's whole block with the corrections below, re-parsed. `a_changed.txt` holds the changed keys, pasted under item 8.

The Verification wins over the report body.

**Checked and confirmed** (clip_flow.js over each coroutine, the waits added up):
- **The channel.** damageCast1 or cast1 is picked by `mDamageCastLv > 0` (:25472-25491).
  - The cast times (:25112-25429):

    | skill | cast time (s) |
    |---|---|
    | Fireball | 4 + sLv - RF |
    | Phoenix, Gadina, Buiten | 3 + 2 sLv |
    | Ja | 1 + 2 sLv |
    | World Ignition | 3 + 3 sLv |
    | Ground Lock | 2 + 0.5 sLv |
    | Stone Hammer | 2 + sLv |
    | Lavu | 9 + 3 sLv |
    | Fire Avatar, Earth Form | 9 |
    | Volcanic Eruption | 15 |
    | Summon Gaos | 24 |

    The last four are instant only with #431.
  - magAdjust is clamp(t - MAG'/32, 0.1, 600) (CharacterControl.cs:20584-20588). So every member is at 0.1 s, and Summon Gaos at 8 s.
  - lckAdjust at LCK 1 (CharacterControl.cs:20658-20670): 12 -> floor(1212 / 100.12) = 12 %; 24 -> floor(2424 / 100.24) = 24 %.
- **The releases:**
  - Fire Avatar: 0.3 / 0.7 (+ 0.4) / 1.5 (+ 0.8).
  - Earth Form: 0.3 / 0.7 / 1.2 (+ 0.5).
  - Lavu: 0.3 / 0.4, then ten Yield(4, 0.2). Standby at 0.4 + 10 x 0.2 = 2.4 s (:34677-34740).
  - Volcanic Eruption: 0.3, then 22 x 0.5, then + 0.7 = 12.0 s.
  - Summon Gaos: 0.3 / 0.4 / 0.8. The Gaos is at getSpawnPos(position + 9 forward) (:44067). No voice.
  - Fire Keep: 0.3 / 0.4 / 0.8 (ActionEvent RPC_fireBall_fire + sLv, :37100).
- **Blazing Arrow:** Yield 1 / 2 / 0.8 gives 1.0, 3.0 and standby at 3.8.
  - blazingArrow_fire's 12 hits come at 3.15 ... 4.8 (i < 12, Yield 0.15, :28259, :28305).
  - Then comes the `lckAdjust(24)` roll with no summon out: Phoenix4 at mPos - 2 tDir (:28265-28288), at 4.8 s.
- **Flash Fire:** the ring at 0, bursts at 0.6 ... 2.7 (i < sLv x 2, :28716), standby at 2.9.
- **Titanic Earth Pulse:** voice at 4.0, shot at 5.0, standby at 7.5. The shot flies 15 m/s from (0, 1, 5), so it reaches the body's front 4.7 m on, at 5.31 s.
- **Geometry and looks:**
  - The fireball flies 2.545 deg down (atan 0.4 / 9). It covers 8.709 m to the body's front in 0.29 s, at y 0.613.
  - The Fire Avatar status turns every renderer under the hero off (CharacterControl.cs:38328-38409).
  - Monkey.Update crossfades the armours to root (0.2) looped once he stands by (Monkey.cs:503-523, :567-587).
- **Effects.** Every effect the block names is in BB's container (`cont.txt`) or comes from EXTRA_FOLDERS. Phoenix4, Ja4, Gadina4, Buiten4 and Gaos are all in `gameassets/characters/elementals/...`.
- **The probe** (`probe.txt`) matches the report:
  - castRing: EC 999, followState, with its looping castRing sound.
  - flashFire_ring: life 4, followState.
  - earthPulse_ring: 7 + 1, followState (root 8.0).
  - volcanicEruption: 12 + 3, with AudioControl and its looping sound.
  - volcanicEruption_ring: 12 + 1, followState.
  - lavu_ring: 2.4. secondStone: 1 + 1.
  - fireBall4: "no layout for Monkey_fireBall (4 field bytes)".
  - volcanicSoul_ring: KeyError (it is in neither game).
- **Icons and TTO.** Every Bible icon key named in "Page changes" exists in `12t_projects/bible/assets.js`. The TTO released rule holds: no TTO cue here.

**Findings:**

1. **Voices: `buiten` is missing from the rip, and `blazingArrow` is in BB's own data.** Read this first 5 / 7, the Blazing Arrow `why`, P7, Q10 and Bible offer 2 are wrong.
   - **Evidence:**
     - The rip's `characters/heroes/monkey/voices/` has `buiten.wav.meta` but no `buiten.wav`, and nothing for blazingArrow.
     - BB's Resources container has both `voices/buiten` and `voices/blazingarrow` (`cont.txt`). Both decode as AudioClips: buiten is 67,676 bytes, blazingArrow 245,554 bytes (`voiceclip.py`).
     - Across every class, these two are the only container voices / sounds the rip lacks (`ripgap.txt`).
   - So BB's Blazing Arrow is **not** silent. The cue `[0, "voice", "blazingArrow"]` stays, as BB's own recording, not TTO's. Withdraw Bible offer 2.
   - **Corrected P7** (replaces "a TTO voice"): `pipeline/wardrobe_fx.py`'s voice job falls back to BB's own AudioClip in the Resources container when `rip_wav(cls, name, "voices")` finds no file.
     - The clip's address is `gameassets/characters/heroes/<cls>/voices/<name>`. Read it with UnityPy `AudioClip.samples`, as FIELD_SOUNDS writes its clips.
     - Without it, `v_buiten.mp3` and `v_blazingArrow.mp3` are never made. The Buiten Hou Hou tile is silent, and `wardrobe_fx_check.py` reports both as missing (`file_errors`, :198-201).
2. **The Gadina4 cue has no sword or shield.** cast3 > gadina's `[0.4, "fx", "Gadina4", ...]` lacks `attach`.
   - parts.md Interfaces 3 / part 9 and skills_b's Gadina4 cues give `"attach": [["gadina_sword4", "mount_Hand_R"], ["gadina_shield4", "mount_Hand_L"]]`. At max rank, Titan Sword 3 / Aegis of Earth 3 give sword4 / shield4.
   - Without it, the Gadina tile shows the Gadina empty-handed. Corrected in item 8.
3. **The summon cues name no `builds`.** The summon part (parts.md part 9) spawns each summon's ring at the spawn from the entry's `builds`. The extractor builds only what the cues and `builds` name (`wardrobe_fx.py` cue_names, :834-849). Add:
   - phoenix and blazingArrow: `phoenix_summon_ring` (Phoenix.cs:4986).
   - ja: `ja_summon_ring` (Ja.cs:2013).
   - gadina: `gadina_summonEffect` (Gadina.cs:6269), `gadina_sword4`, `gadina_shield4`.
   - buitenHouHou: `buiten_summonEffect` (Buiten.cs:791) and its summon sound `sound:buiten_buiten_summon`.
     - The sound is PlayOneShot(buiten_summonFX) (:779), with `SOUND_REFS += "Buiten"`.
     - The name follows `wardrobe_fx.py`:237-244: the script with a lower-case first letter, then the AudioClip's name.
     - The rip's only candidate is `Assets/AudioClip/buiten_summon.wav`, so the builder confirms the name.
   - Gaos: `gaos_summon_ring` (Gaos.cs:4885), in `@SummonGaos:cast3`'s `builds`. It is in the container as `elementals/gaos/effects/summon_ring`, so it needs an ALIASES line.
4. **Two owners for the projectile hits.** parts.md part 1 has the mover spawn `fireBall_hit` / `earthPulse_hit` at the contact (`hit` in its SHOT table, `"builds"`; its fragments :540-541). This report also cues them at 0.69 / 5.31, so each hit would appear twice.
   - **Decision: the part spawns them.** That follows parts.md Interfaces and skills_b's `phoenix_fireBall` (part-spawned `phoenix_fireBall_hit`). effect_only's Fire Avatar - Fireball reuses the same mover.
   - Drop the `fireBall_hit` cue from cast3 > fireBall and from `@FireKeep:cast3`, and the `earthPulse_hit` cue from earthPulse. Add `"builds"` instead.
   - **The hit rotations:**
     - earthPulse_hit: the world `Quaternion.Euler(270, 90, 0)` (Monkey.cs:32818). With the hero facing +z, that is the page's `[270, 90, 0]`. It is **not** parts.md's `"fwd"` / lookEuler(vel).
     - fireBall_hit: the hero's rotation (:11318), so `[0, 0, 0]`.
5. **`anims` -> `clips`.** The page's `anims` is only fxparts/cat.js's fx:grandCasinoArcade option. The armours' timeline is parts.md part 8's `clips: [[age, clip, fade, wrap]]`, the name skills_b uses for the same armour.
   - phoenixArmor: `[[0, "summon", 0, 1], [0.8, "root", 0.2, 2]]`.
   - gadinaArmor: `[[0, "summon", 0, 1], [0.5, "root", 0.2, 2]]`.
   - Both from CrossFade("root", 0.2) + Loop (Monkey.cs:509 / :523, :573 / :587).
   - P4 becomes parts.md part 8.
6. **The castRing `cut` 0.05: the explanation is reversed, but the value stands.**
   - At a step change, fxStart cuts only the followState effects whose cut is *not* past the step (index.html:5311-5315, `f.cutAt <= end`).
   - On the 0 s `damageCast2*~@0` step, a 0.05 cut is past the step, so it counts in the next step's clock. It fires 0.05 s into cast3.
   - That is near enough to the game's release: myCommand changes at cast3's start, and the game's ring lives the 0.1 s floor.
   - Keep 0.05, and correct the `why` / Read this first wording.
   - The same holds for alternative 1 of `@SummonGaos:damageCast2`. Alternative 0's 7.95 is cut at the 8 s step change.
7. **Fire Keep's tile leaves out the store.** Fire Keep #402 is a passive whose whole look has two parts, the store and the release.
   - **The store:**
     - An untargeted Fireball at the bar's end adds the fireKeep status (:25705-25750, RPC_AddStatus :25735 / :25743) and calls RPC_cast0 (:11056-11075: standby, no clip).
     - The status add creates `Effects/fireKeep` at the hero (CharacterControl.cs:38118-38131; probe: EC life 1, followPosition, AudioSource `instantCast`).
   - **The release:** the next normal attack.
   - The `fireKeep` effect is drawn on no other tile.
   - **Decision: show both on the one tile.** Precedents: the Cat's Nine Lives (ko -> getUp), and Mole decision 37 (the precondition shown).
   - **Corrected SEQ** (replaces `"Fire Keep: cast3"`): `"Fire Keep: damageCast1 damageCast2*~@0 root~@1 cast3"`.
     - The channel takes the plain damageCast1 / damageCast2 entries.
     - The new key `@FireKeep:root` is in item 8.
     - `OWN_TILE["monkey"]["fireKeep"]` becomes `["damageCast2", "root", "cast3"]`.
8. **Corrected paste-ready entries.** These replace the same keys of the block; every other key stands as written. The whole corrected block is in `checks\fx_monkey_research\verify\a_fixed.json`.

```json
{
  "cast3": {
    "why": "cast3 is the release clip of the RPC_cast channel's skills (one RPC_<skill>_cast each, started by the release switch Monkey.cs:25700-26194; TTO1102 has the same 14 players, the <RPC_*_cast> coroutines' cast3 strings); each member below is its own tile (poolChains, with the Cast sequence's steps); Lavu, Volcanic Eruption and Summon Gaos have their own sequences (their hold / bar), Fire Keep plays cast3 from the normal attack with no channel (:10020-10024): their keys @<Skill>:cast3",
    "skills": {
      "fireBall": {
        "why": "Monkey.cs RPC_fireBall_cast (:26315-26750), Fireball rank 4, a target locked (tID != 0: Fire Keep #402's store only for an untargeted cast, :25705-25770): at 0 clip cast3 (0.2 fade, Once, :26633-26636), voice fireBall (Voices/fireBall :26663, PlayOneShot :26707); Yield 0.3 (:26696): the prefab field castEffect_fire (= Resources monkey/effects/castEffect_fire; probe: life 2, its own Sounds/castEffect) Instantiated at the hero + TransformDirection(0, 1, 1), hero rotation (:26461); Yield 0.1 (:26703): RPC_fireBall_fire (:26507-26529, Monkey.cs:11092-11291) from position + (0, 1, 1) toward the target's bounds centre (the 10 m target 0.6 m up: LookRotation(0, -0.4, 9), 2.54 degrees down), Effects/fireBall4 (sLv 4, :11236-11248), ProjectileControl life 2 x rangeMod (:11278); Monkey_fireBall flies 30 m/s along its rotation (Monkey_fireBall.cs:13-51); at the target body (front 9.7 m ahead, 8.71 m of flight = 0.29 s) OnTriggerEnter (Monkey_fireBall.cs:91-200) RPC_fireBall_hit: Effects/fireBall_hit at the contact, hero rotation (:11308-11318; life 2, its own Sounds/fireball_hit); the burn status on the foe left out; Yield 0.4 (:26705): FireRune(), standby at 0.8 s (:26569-26574); verification 4: the Monkey_fireBall part (parts.md part 1) spawns fireBall_hit at the contact with the hero's rotation (Monkey.cs:11318), so it is a build, not a cue",
        "cues": [
          [0, "voice", "fireBall"],
          [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}],
          [0.4, "fx", "fireBall4", {"d": 1, "y": 1, "rot": [ 2.54, 0, 0 ], "to": [ 0, 0.6, 10 ]}]
        ],
        "builds": ["fireBall_hit"]
      },
      "phoenix": {
        "why": "Monkey.cs RPC_phoenix_cast (:26755-27110), Phoenix rank 4: at 0 clip cast3 (0.2 fade, Once, :27025-27028), voice phoenix (:27055, :27098); Yield 0.3 (:27104): castEffect_fire at the hero + (0, 1, 1), hero rotation (:26879); Yield 0.1 (:27094): at 0.4 s RPC_phoenix_create4 (ActionEvent :26939: online the sender's own create runs too, the create codes -211 ... -214 are not gated by isMine, Monkey.cs:5182-5195) at getSpawnPos(position + 2 x forward) (:26914), LookRotation(forward) (Monkey.cs:11345-11759): Fire Soul #422 (passives on): Effects/fireSoul_ring at the hero (:11365-11389; life 1, followPosition, its own Sounds/fireSoul); the previous summon unsummoned (none); Characters/Elementals/Phoenix/Phoenix4 (:11541-11559), Phoenix.summon (:11740; Phoenix.cs:4564-5072: Play(summon) Once, its summon_ring field at its feet, Quaternion.identity, Yield 1, standby: root); no despawn timer (the Bible's infinity chip): cut at 10 s; its AI (Phoenix_AI.cs) left out (open question 4); Yield 0.4 (:27092): standby at 0.8 s (:26966); verification 3: the summon part spawns the Phoenix's summon_ring (Phoenix.cs:4986, parts.md Interfaces 4): a build",
        "cues": [[0, "voice", "phoenix"], [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}], [0.4, "fx", "fireSoul_ring"], [0.4, "fx", "Phoenix4", {"d": 2, "kill": 10}]],
        "builds": ["phoenix_summon_ring"]
      },
      "ja": {
        "why": "Monkey.cs RPC_ja_cast (:28920-29275), Ja rank 4: at 0 clip cast3 (0.2 fade, Once, :29190-29193), voice ja (:29220, :29264); Yield 0.3 (:29262): castEffect_fire at the hero + (0, 1, 1) (:29044); Yield 0.1 (:29270): at 0.4 s RPC_ja_create4 (ActionEvent :29104) at getSpawnPos(position + 2 x forward) (:29079), LookRotation(forward): Characters/Elementals/Ja/Ja4 (Monkey.cs:12049-12061), Ja.summon (:12207; Ja.cs:1702-2049: Play(summon) Once, summon_ring at its feet, Yield 1, standby: root); no despawn timer: cut at 10 s; its AI left out; Yield 0.4 (:29268): standby at 0.8 s (:29131); TTO's Ja Ascension #452 (released) swaps this release for RPC_jaAscension_cast when learned (TTO1102:Monkey.<RPC_cast>d__178::MoveNext@0x1CE8830): open question 9; verification 3: the summon part spawns Ja's summon_ring (Ja.cs:2013): a build",
        "cues": [[0, "voice", "ja"], [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}], [0.4, "fx", "Ja4", {"d": 2, "kill": 10}]],
        "builds": ["ja_summon_ring"]
      },
      "worldIgnition": {
        "why": "Monkey.cs RPC_worldIgnition_cast (:29700-30080), World Ignition rank 2: at 0 clip cast3 (0.2 fade, Once, :29993-29996), voice worldIgnition (:30023, :30072); Yield 0.3 (:30065): castEffect_fire at the hero + (0, 1, 1) (:29835); Yield 0.1 (:30061): at 0.4 s the ignite status on the target (getDebuff(60), its explosion after 800 / 1200 damage, :29902-29907): a status on a foe, left out (Chameleon decision 53), and its Effects/worldIgnition explosion (:30309) needs that damage, not in a single play; Yield 0.4 (:30067): standby at 0.8 s (:29934)",
        "cues": [[0, "voice", "worldIgnition"], [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}]]
      },
      "groundLock": {
        "why": "Monkey.cs RPC_groundLock_cast (:30402-30820), Ground Lock rank 4, Second Stone #403 and Aegis of Earth 3 on (passives on): at 0 clip cast3 (0.2 fade, Once, :30736-30739), voice groundLock (:30766, :30801); Yield 0.3 (:30816): castEffect_fire at the hero + (0, 1, 1) (:30537); Yield 0.1 (:30808): at 0.4 s the target locked (groundLock status, getDebuff(3 + 3) :30608-30619, a foe's status: left out), hit (:30625), RPC_groundLock_hit at the target's position (:30633; Monkey.cs:30960-31170): Effects/groundLock_hit there, Quaternion.identity (:31127-31139; life 1, its own Sounds/groundLock); with #403 Yield 3 (:31153-31168): Effects/secondStone at the still-locked target (:31014-31046; life 1, the stone mesh, its own Sounds/secondStone) at 3.4 s, its 0.5 m hit (:31073-31096) draws nothing; Yield 0.4 (:30818): standby at 0.8 s (:30677); the second stone comes in the idle tail",
        "cues": [[0, "voice", "groundLock"], [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}], [0.4, "fx", "groundLock_hit", {"d": 10}], [3.4, "fx", "secondStone", {"d": 10}]]
      },
      "gadina": {
        "why": "Monkey.cs RPC_gadina_cast (:31217-31570), Gadina rank 4: at 0 clip cast3 (0.2 fade, Once, :31487-31490), voice gadina (:31517, :31555); Yield 0.3 (:31551): castEffect_fire at the hero + (0, 1, 1) (:31341); Yield 0.1 (:31563): at 0.4 s RPC_gadina_create4 (ActionEvent :31401) at getSpawnPos(position + 2 x forward) (:31376), LookRotation(forward) (Monkey.cs:12580-12960): Earth Soul #423 (passives on): Effects/earthSoul_ring at the hero (:12588-12612; life 1, followPosition, its own Sounds/earthSoul); Characters/Elementals/Gadina/Gadina4 (:12770-12782), Gadina.summon (:12957; Gadina.cs:5944-6505: Play(summon) Once, its summonEffect at its feet, Quaternion.identity (:6269), a 4 x 4 + 8 = 24 m hit (:6344-6367, nothing drawn), Gadina4's Yield 1.5 (:6427-6436, :6502), standby: root); no despawn timer: cut at 10 s; its AI left out; Yield 0.4 (:31568): standby at 0.8 s (:31428); verification 2-3: Titan Sword 3 / Aegis of Earth 3 give the Gadina4 sword4 / shield4 on mount_Hand_R / _L (option attach, parts.md Interfaces 3, as skills_b's Gadina4 cues); its summonEffect (Gadina.cs:6269): builds",
        "cues": [
          [0, "voice", "gadina"],
          [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}],
          [0.4, "fx", "earthSoul_ring"],
          [0.4, "fx", "Gadina4", {"d": 2, "kill": 10, "attach": [ [ "gadina_sword4", "mount_Hand_R" ], [ "gadina_shield4", "mount_Hand_L" ] ]}]
        ],
        "builds": ["gadina_summonEffect", "gadina_sword4", "gadina_shield4"]
      },
      "stoneHammer": {
        "why": "Monkey.cs RPC_stoneHammer_cast (:32896-33280), Stone Hammer rank 4, Stone Sentinel #443 on (damage and KO only): at 0 clip cast3 (0.2 fade, Once, :33192-33195), voice stoneHammer (:33225, :33265); Yield 0.3 (:33271): castEffect_fire at the hero + (0, 1, 1) (:33031); Yield 0.1 (:33261): at 0.4 s RPC_stoneHammer_fire at the target's position (:33093; Monkey.cs:33400-33560): Effects/stoneHammer there, Quaternion.identity (:33523-33533; life 3, the hammer mesh with its root clip, its own Sounds/stoneHammer), Yield 1 (:33554): the camera shake (:33436) and the hit (:33458-33463) at 1.4 s draw nothing; Yield 0.4 (:33278): standby at 0.8 s (:33133)",
        "cues": [[0, "voice", "stoneHammer"], [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}], [0.4, "fx", "stoneHammer", {"d": 10}]]
      },
      "buitenHouHou": {
        "why": "Monkey.cs RPC_buiten_cast (:33609-33960; sType buiten, the card Buiten Hou Hou, icon monkey_buitenHouHou4), rank 4: at 0 clip cast3 (0.2 fade, Once, :33879-33882), voice buiten (:33909, :33954); Yield 0.3 (:33956): castEffect_fire at the hero + (0, 1, 1) (:33733); Yield 0.1 (:33948): at 0.4 s RPC_buiten_create4 (ActionEvent :33793) at getSpawnPos(position + 2 x forward) (:33768), LookRotation(forward): Characters/Elementals/Buiten/Buiten4 (Monkey.cs:13327-13339), Buiten.summon (:13460; Buiten.cs:557-816: Play(create) Once, PlayOneShot(buiten_summonFX) (:779), its summonEffect at its feet, its rotation (:791), Yield 1, standby: root); no despawn timer: cut at 10 s; Yield 0.4 (:33942): standby at 0.8 s (:33820); TTO's Buiten Bastion (released) on the same branch: the tto report; verification 3: Buiten.summon's summonEffect (Buiten.cs:791) and its PlayOneShot(buiten_summonFX) (:779; SOUND_REFS += Buiten, the sound named buiten_<AudioClip name>, the rip's only candidate Assets/AudioClip/buiten_summon.wav: the builder confirms the name): builds; the voice buiten is BB's own AudioClip (verification 1)",
        "cues": [[0, "voice", "buiten"], [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}], [0.4, "fx", "Buiten4", {"d": 2, "kill": 10}]],
        "builds": ["buiten_summonEffect", "sound:buiten_buiten_summon"]
      },
      "fireAvatar": {
        "why": "Monkey.cs RPC_phoenixArmor_cast (:38208-38700; sType fireAvatar :26057-26063), Fire Avatar (one rank; cast bar 9 s, magAdjust's 0.1 s floor, instant allowed by Auto Instant #431, :25314-25342): at 0 clip cast3 (0.2 fade, Once, :38621), voice sAttack3 (:38651, :38696); Yield 0.3 (:38684): castEffect_fire at the hero + (0, 1, 1) (:38321), the summon unsummoned (none, :38326-38338); Yield 0.4 (:38688): at 0.7 s the fireAvatar status (5, chaAdjust(120), :38371): the hero becomes Elementals and every renderer under him off, the armor's on (CharacterControl.cs status add 'fireAvatar': the page's whole-hero hideProp), Effects/phoenixArmor parented to the hero, local 0 / identity, Play(summon) (:38383-38438; its Animation root / run / nAttack / blazingForm1 / blazingForm2 / summon), phoenixArmor_create at the hero, created twice (:38461 inside the armor branch, :38503 after it; life 1, its own Sounds/fireAvatar_create); Yield 0.8 (:38686): standby at 1.5 s (:38562), from which Monkey.Update crossfades the armor to root looped (:471-523; anims 0.8 s after its spawn); the 120 s form cut at 10 s (the armor and the hide); the motion blur (:38530) left out; verification 5: the armour's clip timeline is parts.md part 8's option clips [[age, clip, fade, wrap]] (Update's CrossFade(root, 0.2) + Loop, Monkey.cs:509, :523)",
        "cues": [
          [0, "voice", "sAttack3"],
          [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}],
          [0.7, "hideProp", "hero", {"kill": 10}],
          [0.7, "fx", "phoenixArmor", {"kill": 10, "clips": [ [ 0, "summon", 0, 1 ], [ 0.8, "root", 0.2, 2 ] ]}],
          [0.7, "fx", "phoenixArmor_create"],
          [0.7, "fx", "phoenixArmor_create"]
        ]
      },
      "earthForm": {
        "why": "Monkey.cs RPC_gadinaArmor_cast (:40508-40972; sType earthForm :26083-26089), Earth Form (one rank; 9 s bar, the 0.1 s floor, instant allowed by #431, :25343-25371): at 0 clip cast3 (0.2 fade, Once, :40881), voice sAttack3 (:40911, :40952); Yield 0.3 (:40950): castEffect_fire at the hero + (0, 1, 1) (:40621), the summon unsummoned (none, :40632); Yield 0.4 (:40964): at 0.7 s the earthForm status (5, chaAdjust(120), :40671: Race Elementals, ATK / DEF + 100, no renderer change, CharacterControl.cs status add 'earthForm': the hero stays visible), the camera shake (:40683) left out, Effects/gadinaArmor parented to the hero, local 0 / identity, Play(summon) (:40695-40747; its Animation root / run / summon / nAttack1-3 / cAttack0-2), gadinaArmor_create at the hero (:40758-40770; life 1, followPosition, its own Sounds/earthform_create); Yield 0.5 (:40944): standby at 1.2 s (:40822), from which Monkey.Update crossfades the armor to root looped (:573-587; anims 0.5 s after its spawn); the 120 s form cut at 10 s; verification 5: option clips (CrossFade(root, 0.2) + Loop, Monkey.cs:573, :587)",
        "cues": [
          [0, "voice", "sAttack3"],
          [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}],
          [0.7, "fx", "gadinaArmor", {"kill": 10, "clips": [ [ 0, "summon", 0, 1 ], [ 0.5, "root", 0.2, 2 ] ]}],
          [0.7, "fx", "gadinaArmor_create"]
        ]
      }
    }
  },
  "@FireKeep:root": {
    "why": "Fire Keep #402's store (verification 7): an untargeted Fireball at the bar's end (RPC_cast's release switch, Monkey.cs:25705-25750: hasSkill(402), tID 0) adds the fireKeep status (RPC_AddStatus :25735 / :25743) and calls RPC_cast0 (:11056-11075: standby, no clip: the page's root~), the status add creating Effects/fireKeep at the hero, identity (CharacterControl.cs:38118-38131; probe: EffectControl life 1, followPosition, its own AudioSource instantCast); the tile's 1 s root step is the flash's life, then the next normal attack's release (@FireKeep:cast3)",
    "cues": [[0, "fx", "fireKeep"]]
  },
  "@FireKeep:cast3": {
    "why": "Fire Keep #402 (passive, Bible 4.x 'fireKeep'): an untargeted Fireball stores a ball (the fireKeep status, Monkey.cs:25705-25748, its 1 s Effects/fireKeep flash at the store, CharacterControl.cs status add 'fireKeep', not on this tile), and the next normal attack releases it in place of the Combo (:10020-10024): Monkey.cs RPC_fireKeep_cast (:36855-37225) at the stored level 4: at 0 LookAt the target, clip cast3 (0.2 fade, Once, :37179-37185), no voice; Yield 0.3 (:37220): castEffect_fire at the hero + (0, 1, 1) (:37012); Yield 0.1 (:37209): RPC_fireBall_fire from position + (0, 1, 1) toward the target's bounds centre (:37047-37087): fireBall4 and its hit as the Fireball tile's; Yield 0.4 (:37216): standby at 0.8 s (:37132); the status decrement (:10039-10055) draws nothing; verification 4: fireBall_hit is the part's (a build); verification 7: the store comes first on this tile (@FireKeep:root)",
    "cues": [
      [0.3, "fx", "castEffect_fire", {"d": 1, "y": 1}],
      [0.4, "fx", "fireBall4", {"d": 1, "y": 1, "rot": [ 2.54, 0, 0 ], "to": [ 0, 0.6, 10 ]}]
    ],
    "builds": ["fireBall_hit"]
  },
  "blazingArrow": {
    "why": "Monkey.cs RPC_blazingArrow (:27560-27985), Blazing Arrow #234 (one rank): at 0 actionState attack (:27860-27869), clip blazingArrow (0.2 fade, Once, :27881-27884), voice blazingArrow (Voices/blazingArrow :27917, PlayOneShot :27929): in BB's own data (the Resources container's voices/blazingarrow AudioClip, 245,554-byte WAV; only the rip lacks the file: checks/fx_monkey_research/verify/voiceclip.py, ripgap.txt): BB's recording (verification 1); the current summon unsummoned (none, :27942-27954); Yield 1 (:27976): Effects/blazingArrow at the hero, hero rotation (Instantiate :27697-27715; probe: life 4, the arrow mesh's 4 s root clip, AlphaTimer, trail, its own Sounds/blazingArrow), the zoom blur (:27750) left out; Yield 2 (:27972): at 3.0 s blazingArrow_fire (:27777; Monkey.cs:28015-28355): 12 hits 0.15 s apart, 3.5 m circles at 3 i + 2 m ahead (:28133-28215, Yield 0.15 :28305; damage and the foe's burn only); after the 12th, at 3.0 + 12 x 0.15 = 4.8 s, with no summon out: Random.Range(0, 100) < lckAdjust(24) = 24 % at LCK 1 (:28265-28271, CharacterControl.cs:20658-20670): RPC_phoenix_create4 at getSpawnPos(position - 2 x forward), LookRotation(forward) (:28277-28288; the create as the Phoenix tile's: Fire Soul's fireSoul_ring at the hero, Phoenix4), cut at 10 s: in the idle tail; Yield 0.8 (:27974): standby at 3.8 s (:27825); the Phoenix's summon_ring is the summon part's (a build, verification 3)",
    "cues": [[0, "voice", "blazingArrow"], [1, "fx", "blazingArrow"], [4.8, "fx", "fireSoul_ring", {"p": 0.24, "roll": "blazingPhoenix"}], [4.8, "fx", "Phoenix4", {"d": -2, "kill": 10, "p": 0.24, "roll": "blazingPhoenix"}]],
    "builds": ["phoenix_summon_ring"]
  },
  "earthPulse": {
    "why": "Monkey.cs RPC_earthPulse (:32100-32593), Titanic Earth Pulse #334 (one rank; needs a Gadina4 and spends it, the Bible's 2.3): at 0 actionState attack, myCommand earthPulse (:32370-32379), clip earthPulse (0.2 fade, Once, :32391-32394), noForce 7 s (:32403, nothing drawn), voice unsummon (:32430, :32442), the Gadina unsummoned (its HP kept for the damage, :32455-32492; not on the page: open question 7), Effects/earthPulse_ring at the hero, hero rotation (createEffect :32495-32511; probe: life 7 + afterLife 1, followPosition, followState, the earth beam mesh with the Gadina shield / sword, its own Sounds/earthPulse_fire); Yield 4 (:32558): at 4.0 s voice earthPulse (:32222, :32553); Yield 1 (:32545): at 5.0 s RPC_earthPulse_fire from position + TransformDirection(0, 1, 5), LookRotation(forward) (:32272-32277; Monkey.cs:13090-13115: Effects/earthPulse, ProjectileControl life 3), Monkey_earthPulse flies 15 m/s along it (Monkey_earthPulse.cs:13-63), at the target body (front 9.7 m ahead: 4.7 m = 0.31 s) OnTriggerEnter (:91-194) RPC_earthPulse_hit at the contact (Monkey.cs:32598-32855): Effects/earthPulse_hit there, Euler(270, 90, 0) (:32806-32818; life 3, its own Sounds/earthPulse_hit), five growing hits 0.2 s apart (:32704-32762, nothing drawn), shakes and the motion blur (:32308, :32847) left out; Yield 2.5 (:32556): standby at 7.5 s (:32335): the ring's followState cut 7.5; verification 4: the Monkey_earthPulse part (parts.md part 1) spawns earthPulse_hit at the contact (about 5.31 s) with the world rotation Euler(270, 90, 0) (Monkey.cs:32818; not lookEuler(vel)): a build",
    "cues": [
      [0, "voice", "unsummon"],
      [0, "fx", "earthPulse_ring", {"cut": 7.5}],
      [4, "voice", "earthPulse"],
      [5, "fx", "earthPulse", {"d": 5, "y": 1, "to": [ 0, 1, 9.7 ]}]
    ],
    "builds": ["earthPulse_hit"]
  }
}
```

9. **Missed: six Bible cards for the summons' own moves have no tile in any Monkey report.**
   - **The cards** (`12t_projects/bible/index.html`, the `id:` list):

     | card | icon |
     |---|---|
     | `monkey_phoenix_fireBall` | phoenix4 |
     | `monkey_gadina_nAttack` | gadina4 |
     | `monkey_ja_detonate` | ja4 |
     | `monkey_gaos_fire`, `monkey_gaos_rampage`, `monkey_gaos_tailSpin` | summonGaos5 |

   - **Why they need tiles:** the standing rule is one tile per skill, with its Bible icon.
   - Q4's "keep them standing" still holds for the summon tiles themselves (the Barrel Bot precedent, Mole decision 32). But Mole decision 32 also showed the Auto Gyro Gun's AI shots, so a summon's move is not out of scope.
   - **Decision:** each card gets an effect-only tile on the idle stance (`"<Name>: root@<t>"`, SEQ_SKILL to the card's skill). The summon stands 2 m ahead (`ring: false`, skills_b's option), plays that move once at the 10 m target, and is cut at 10 s.
   - **Phoenix - Fireball** reuses skills_b's traced shot. In Phoenix.cs RPC_nAttack: CrossFade nAttack + cry, the shot at actionTime + 0.5 (:2354), standby 0.3 later. The Bible gives about 1.85 s between shots with Rapid Fire 3.
   - **The rest is a follow-up research job.** No report traces Gadina's nAttack4, Ja's suicideRun / Detonate, or Gaos's gaosFire / rampage / tailSpin.
     - To read: Gadina.cs, Ja.cs, Gaos.cs, and their _AI ranges.
     - Their field prefabs are already in parts.md's LAYOUTS: `tailSpin_ring`, `gaosFire`, `ja_suicideBomb`, `gadina_nAttack_hit4`.
10. **P8 `alt` needs the check changed too.**
    - `wardrobe_fx_check.py` forces each alternative in turn (seq_plays, `window.__seqAlt`).
    - Its `expected()` (:145-153) would expect alternative 1's `instantCast` (no `p`) in alternative 0's play. `expected()` / `entry_for` must drop the cues of the alternatives not forced.
    - The page side: fxStart's filter compares `c.alt` with `C.seq.alt[step]` (index.html:1401, stepAt's pick), beside `worn`.
11. **Minor.**
    - Read this first 7 lists `buiten` among the voices "in BB's rip". It is not (item 1).
    - The parts summary P1 should name the five ring builds and Buiten's sound (item 3).
    - P2's "the hits are their own cues" is reversed by item 4.
    - Q12: I did not re-read the field PPtrs of castRing / castEffect_fire. Their Resources names exist, and the probe reads both whole.

**Not re-checked here:**
- TTO's catalog keys (the home PC's `cat_keys.txt`).
- The summon waits beyond the summon coroutines' own Yields: Phoenix / Ja / Buiten 1 s, Gaos 0.7 / 0.8 / 1.2, Gadina's per-rank chain (:6498-6504).
- The Phoenix_AI follow-up.
