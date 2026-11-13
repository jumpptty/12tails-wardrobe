# Monkey: the skills with no body animation (effect-only tiles)

Research only (2026-11-13, office PC). I worked read-only: I wrote this report and files under
`checks/fx_monkey_research/effect_only/` (git-ignored) and nothing else.

**What was run:**
- Two probes, `--probe` only (exit 0 both): `uv run --no-project --with UnityPy python -I pipeline/wardrobe_fx.py monkey
  --probe instantCast_ring,instantCast,fireRune_hit,earthRune_hit,castRing` (`probe.json`, summary `probe_summary.txt`)
  and `... --probe phoenixArmor,pAttack_ring,blazingForm_fire,blazingForm_ring,blazingForm0_ring,fireBall4,phoenixArmor_destroy`
  (`probe2.json`, `probe2_summary.txt`; `fireBall4` answers "no layout for Monkey_fireBall", the inventory's missing part).
- `node pipeline/clip_calls.js C:/Users/Jump/Desktop/12tails/DecompiledSource wardrobe/data monkey` (`clip_calls.txt`).
- Helpers in `checks/fx_monkey_research/effect_only/`: `pred.py` (every junk predicate in a line range, T / F; outputs
  `pred_*.txt`), `loads.py` -> `loads.txt` (all 154 `Heroes/Monkey/` loads in Monkey.cs with the method holding each),
  `callers.py` -> `callers.txt` (who calls each phase RPC), `bb_rpc.txt` / `tto_rpc.txt` (the RPC lists), `flow_*.txt`
  (readable flows of the Fire Avatar moves), `clip_len.py` -> `clip_len.txt` (AudioClip lengths read from the BB data
  through `wardrobe_fx.Game`: the rip's `sounds/*.wav` on this PC are zero-filled), `summ.py`, `cues.json` (block 3 below,
  checked with `json.load`).

**Sources:** `C:\Users\Jump\Desktop\12tails\DecompiledSource\Monkey.cs` (cited `:line`), `CharacterControl.cs`,
`EffectControl.cs`, `Monkey_fireBall.cs`; the TTO pseudo-C `DecompiledSource_TTO_2026-11-02\pseudo\Monkey.c` and
`methods.tsv`; the Bible's `12t_reference/monkey-skill-reference.md` and its cards / `assets.js` in `12t_projects/bible/`;
`plans/fx_inventory.md` ("### monkey"); `wardrobe/data/monkey/clips.json`. Templates: the Mole's and Chameleon's
`effect_only.md`, the Penguin's Frost Spike / Double Cast, the Bison's Berserker Rush.

## Read this first

1. **One Monkey active is effect-only: Instant Cast** (`RPC_instantCast`, a plain method `doSkill` calls straight,
   :9501). `doSkill` (:7366-9535) holds no PlayAnimation / animation.Play / CrossFade at all; every other active it
   reaches plays a body clip (`clip_calls.js`: summonAttack, summonDefense, summonRelease, cast1 / cast2 / cast3,
   damageCast1 / 2, blazingArrow, flashFire, runicCast, earthPulse, upheaval, ...).
2. **Two passives fire a look on the Monkey with no clip: Fire Rune (#261-263) and Earth Rune (#361-363).** Each gets an
   idle-stance tile with its proc every play, as the Penguin's Frost Spike and the Bison's Berserker Rush (both need a
   hit too). Fire Rune's end-of-action roll also belongs on six other tiles (12 %): a note for their owners below.
3. **Two Fire Avatar moves play no body clip either: Fire Avatar - Fireball (the form's normal attack) and Blazing Fire's
   Blazing Form (the form's charge).** The `fireAvatar` status switches off every renderer under the Monkey
   (CharacterControl.cs:38348-38380) and the armor `Effects/phoenixArmor`, parented to him, plays the moves on its own
   Animation (`mPhoenixArmor.animation.Play("nAttack")` :39224, `"blazingForm1"` :40001, `"blazingForm2"` :39595). They
   are two Bible cards (`monkey_fireAvatar_fireBall`, icon `monkey_fireBall4`; `monkey_blazingFire`, icon
   `monkey_blazingFire5`), so two tiles: the hero hidden, the armor drawn and played. **If the Fire Avatar researcher
   also wrote them, keep one copy** (Open question 1).
4. **Two page parts are missing (built, not left out):** P1 a part playing the hero code's clips and fades on the armor
   and the fire form (`fx:phoenixArmor`, `fx:blazingForm_fire`, cue options `anims` and a new `alpha`); P2 an icon alias
   in `wardrobe_skill_icons.py` (the Fire Avatar - Fireball card borrows `monkey_fireBall4`). Fire Avatar - Fireball also
   needs `Monkey_fireBall` (the fireball projectile, `fx_inventory.md`), which the Fireball skill needs anyway: the
   parts report builds it.
5. **TTO: nothing effect-only.** The nine TTO-only RPCs are Buiten Bastion / Buiten Offering / Ja Ascension (both casts)
   / Rune Golem casts, which play clips, and their phases (`runeGolem_create`, `solarEcho`, `sunburst`,
   `solarCollapse`).
6. **Status tint left out:** Instant Cast's status tints the Monkey (0.78, 0.43, 0.34) for 12 s; left out as the
   Penguin's multiCast tint (Penguin decision 10, Bat 13, Bison 34, Cat 44). Open question 3 has the one-line HERO_SKINS
   body look if the lead wants it.

## Result

| Tile (Bible name) | Bible icon | Code | Effects (max rank) | Voice / sound | Step | Buildable |
|---|---|---|---|---|---|---|
| **Instant Cast** | `monkey_instantCast2` | `RPC_instantCast` :10938 (called :9501) | `instantCast_ring` at the hero | voice `instantCast` (0.850 s); the ring's own sound | `root*@1` | yes (ready) |
| **Fire Rune** | `monkey_fireRune3` | `FireRune` :12273 -> `RPC_fireRune` :12334 | `fireRune_hit` at the hero, identity | the effect's `fireRune` (0.522 s) | `root*@1` | yes (ready) |
| **Earth Rune** | `monkey_earthRune3` | `EarthRune` :13539 -> `RPC_earthRune` :13600 | `earthRune_hit` at the hero, identity | the effect's `fireRune` | `root*@1` | yes (ready) |
| **Fire Avatar - Fireball** | `monkey_fireBall4` (P2) | `doNormalAttack` :9729 -> `$RPC_phoenixArmor_nAttack$24778` :38728 | armor `nAttack`; `fireBall4` from the muzzle to the 10 m point; `pAttack_ring`; Fire Rune 12 % | voice `sAttack3` (0.572 s), sound `nAttack1` (0.118 s) | `root*@1.8` | P1 + `Monkey_fireBall` |
| **Blazing Fire** | `monkey_blazingFire5` | `doBeginCharge` :10253 -> `$RPC_phoenixArmor_blazingForm$24791` :39351; release `doReleaseCharge` :10600 -> `$RPC_phoenixArmor_blazingForm0$24812` :40111 | armor `blazingForm1` / `blazingForm2` / fade; `blazingForm_ring`; `blazingForm_fire` (the fire form); `blazingForm0_ring` | the effects' own (`blazingForm_ring` 1.494 s, `blazingForm_fire` 0.993 s looped, `blazingForm0_ring` 0.599 s) | `root*@3.5` | P1 |

The Monkey's idle `root` is 0.6 s (clips.json); every step is written held (`root*@t`), as the Mole's and the Cat's.

## Accounting: every RPC_* in Monkey.cs (93 definitions)

`grep -nE "^\s*(public|private|protected|internal)[^(]*\bRPC_\w+\(" Monkey.cs` gives 93 (`bb_rpc.txt`). Owner =
the report that cues it: "skills" = the skills reports (skills_a / skills_b, whichever holds the skill), "attacks" =
attacks_emotes, "this" = this report.

| RPC (line) | Skill | Body clip | Owner |
|---|---|---|---|
| nAttack1 :10720, nAttack2 :10727 | Combo | nAttack1, nAttack2 | attacks |
| nAttack_hit :10734 | Combo / Mike Blink / Damage Cast hit (called :20035, :20649, :36061, :36667, :21355, :25660, :35118) | none (phase) | attacks / skills |
| cAttack1 :10889, cAttack0 :10896 | HP Transfer (charge, release) | cAttack2 / cAttack1; release none (phase) | attacks |
| mikeBlink1 :14001, mikeBlink2 :14008 | Mike Blink (#401, the normal attack past 12 m) | nAttack1, nAttack2 | attacks |
| summonAttack :10903, summonDefense :10910, unsummon :10917, summonRelease :10924, summonSoul :10931 | the summon commands, Summon Soul | summonAttack, summonDefense, summonRelease (x3) | skills |
| **instantCast :10938** | **Instant Cast** | **none** | **this** |
| cast :11049, cast0 :11056 | the cast bar (13 spells), its cancel | cast1 / cast2 / damageCast1 / 2; cancel none (phase) | skills |
| fireBall_cast :11085, fireBall_fire :11092, fireBall_hit :11295 | Fireball (fire also serves Fire Keep and Fire Avatar - Fireball) | cast3; fire / hit none (phases) | skills (+ this for Fire Avatar's shot) |
| phoenix_cast :11338, phoenix_create :11345 | Phoenix | cast3; create none (phase, its fireSoul_ring :11377) | skills |
| skyCrimson :11807 | Sky Crimson | summonAttack | skills |
| blazingArrow :11858 | Blazing Arrow | blazingArrow | skills |
| flashFire :11872 | Flash Fire | flashFire | skills |
| ja_cast :11879, ja_create :11886 | Ja | cast3; create none (phase) | skills |
| **fireRune :12334** | **Fire Rune** (passive proc, from FireRune :12312) | **none** | **this** |
| runicFlame :12461, runicFlame_fire :12468 | Runic Flame (segments from RunicFlame :12436) | runicCast; fire none (phase) | skills |
| worldIgnition_cast :12533, worldIgnition_hit :12540 | World Ignition | cast3; hit none (phase) | skills |
| groundLock_cast :12547, groundLock_hit :12554 | Ground Lock (+ Second Stone) | cast3; hit none (phase) | skills |
| gadina_cast :12561, gadina_create :12568 | Gadina | cast3; create none (phase, earthSoul_ring :12600) | skills |
| planetBreaker :13067 | Planet Breaker | summonAttack | skills |
| earthPulse :13074, earthPulse_fire :13081, earthPulse_hit :13136 | Titanic Earth Pulse | earthPulse; fire / hit none (phases) | skills |
| stoneHammer_cast :13143, stoneHammer_fire :13150 | Stone Hammer | cast3; fire none (phase) | skills |
| buiten_cast :13157, buiten_create :13164 | Buiten Hou Hou | cast3; create none (phase) | skills |
| **earthRune :13600** | **Earth Rune** (passive proc, from EarthRune :13578) | **none** | **this** |
| runicSand :13727, runicSand_fire :13734 | Runic Sand | runicCast; fire none (phase) | skills |
| lavu_cast :13799, lavu_summon :13876, upheaval :13949, upheaval0 :13956, lavu_unsummon :13963 | Lavu, its Upheaval | cast3, upheaval; the rest phases (upheaval0 plays root :35674) | skills |
| fireKeep_cast :14066 | Fire Keep's release (from the normal attack) | cast3 | skills / attacks |
| instantBlaze :14073 | Instant Blaze | summonAttack | skills |
| earthGuard :14080 | Earth Guard | summonAttack | skills |
| phoenixArmor_cast :14087 | Fire Avatar | cast3 | skills |
| **phoenixArmor_nAttack :14094** | **Fire Avatar - Fireball** | **none** (the armor's `nAttack`) | **this** |
| **phoenixArmor_blazingForm :14101, phoenixArmor_blazingForm0 :14108** | **Blazing Fire** (the form's charge, release) | **none** (the armor's `blazingForm1` / `2`, `root`) | **this** |
| phoenixArmor_destroy :14115 | Fire Avatar's end (from Update :495) | none (phase) | skills |
| gadinaArmor_cast :14170 | Earth Form | cast3 | skills |
| gadinaArmor_nAttack1 :14177, _nAttack2 :14184, _nAttack3 :14191, gadinaArmor_hit :14198 | Earth Form - Normal Attack (hit = its phase) | summonAttack (+ nAttack1 / 2 on the armor) | skills / attacks |
| gadinaArmor_sentinalGuard :14241, _sentinalGuard0 :14248 | Stone Sentinel's Sentinel Guard | sentinalGuard1 / 2 / 0 (SEQ "Sentinel Guard") | skills |
| gadinaArmor_destroy :14255 | Earth Form's end (Update :559) | none (phase) | skills |
| volcanicEruption_cast :14310 | Volcanic Eruption | cast3 | skills |
| summonGaos_cast :14317, summonGaos_create :14324 | Summon Gaos | cast3; create none (phase, volcanicSoul_ring :14387) | skills |
| obsidianFang :14623, obsidianFang_hit :14630, stunningGround :14673, psalmOfEnergy :14916, seaAegis :15086, assassinate :15273, zephyrLore :15280, mineWalker :15374, replenishment :15381, elementalBound :15510, divineChannel :15656, astralShift :15663, bloodCarnage :15854 | the 13 shared supplements | (shared) | none (out of the Monkey's roster, as every class) |
| emotion :16201, emotion0 :16208 | emotes | the emote clips | attacks |
| useItem :16648, useMount :16705, useCoin :16758, petEffect :18955 | items, mount, coin, pet | (shared) | attacks / none |
| activateIcon1 :18993, activateIcon2 :19000 | the mission | cAttack2 | none (Penguin decision 19) |
| ko :19040, dead :19047, revive :19054 | the KO tile | ko / dead | attacks |

Totals: 41 RPCs that play a body clip (`clip_calls.txt`, activateIcon1 among them) + 6 here with no clip (instantCast,
fireRune, earthRune, phoenixArmor_nAttack, phoenixArmor_blazingForm and its release blazingForm0) + 23 phases of
others' skills + 23 shared = **93** (`groups.txt`, diffed by name against `bb_rpc.txt`: the same 93, none twice). The Bible's 28
cooldown actives (reference table :8-37) all reach a clip except Instant Cast; Fire Avatar - Fireball and Blazing Fire
are the form's moves.

**TTO** (`tto_rpc.txt`, 78 Monkey RPCs; BB-only are the 24 shared): the TTO-only nine are `RPC_buitenBastion_cast`
(clip `buitenBastion`, pseudo/Monkey.c:418-607), `RPC_buitenOffering_cast` (`sanctumRaise`, :624-986; not released),
`RPC_jaAscension_cast` (`jaAscension`, :10252-10463) and `RPC_sunAvatar_cast` (`solarCall`, :20405-20849),
`RPC_runeGolem_cast` (`golemCall`, :16230-16408), and the phases `RPC_runeGolem_create` (:43926), `RPC_solarEcho`
(:17759), `RPC_sunburst` (:45030), `RPC_solarCollapse` (:17382; Ja Ascension's crown flares and closing blast, Bible
reference :912-915). Each phase belongs to its skill's tile (the TTO report). TTO keeps `RPC_instantCast` as BB
(pseudo/Monkey.c:35898-36054: agiAdjust(240), chaAdjust(12), the same ring and voice, the same mode-above-4 voice gate),
`FireRune` / `RPC_fireRune` (:37554, :37667, `fireRune_hit` :37690), `EarthRune` / `RPC_earthRune` (:39236, :39349) and
the Fire Avatar effects (`pAttack_ring` :15112, `blazingForm_ring` / `_fire` / `0_ring` :13583-13953). No TTO cue here.

## The passives, each one checked

| Passive (Bible) | Where it runs | Draws on the Monkey? | Tile? |
|---|---|---|---|
| **Fire Rune** #261-263 | FireRune :12273, 18 call sites (Bible 4.7) | `fireRune_hit` | **yes (here)**; and 12 % on six tiles (below) |
| **Earth Rune** #361-363 | EarthRune :13539 on a hit taken (Update :236-242; CharacterControl.cs:30341, :30435) | `earthRune_hit` | **yes (here)** |
| **Blazing Fire** #442 | the Fire Avatar charge (doBeginCharge :10208-10253); +10 in Flash Fire | the fire form | **yes (here)** |
| Damage Cast #102-103 | inside HP Transfer (:21299-21339), the cast bar (:25644), Upheaval (:35102) | hits only | no (those tiles) |
| Rapid Fire, Intense Fire, Titan Sword, Aegis of Earth | summon stats, Fireball cast time, Ground Lock time | no | no |
| Fire Soul #422, Earth Soul #423 | summon stats; the soul rings at the summon's creation (fireSoul_ring :11377, earthSoul_ring :12600, volcanicSoul_ring :14387) | rings in those tiles | no (Phoenix / Gadina / Summon Gaos owners) |
| Mike Blink #401, Mike Circle #411 | the normal attack past 12 m (:10073-10139); HP Transfer's Mikes on the target (:21383-21435) | in those clips | no (attacks) |
| Auto Instant #431 | RPC_cast :25008-25048: 12 % instant cast, `instantCast` effect at the hero | in the cast tiles | no (cast owners, as Bat decision 12's Auto Mass) |
| Second Stone #403, Stone Sentinel #443 | Ground Lock's second stone; Stone Hammer +30; Sentinel Guard (clip) | in those tiles | no |
| Stat Plus, Super Stat Plus, Revised Skill / Magic / Art | stats / costs | no | no |

Monkey.Update (:159-1130) runs only the shared gear / pet updates, EarthRune on a hit (:242), the RunicFlame /
RunicSand / Lavu skill updates (:254-278), PlayerControl, the KO / death checks and the Fire Avatar / Earth Form armor
sync (:470-560): no passive look of its own.

## How each reads (junk predicates worked by hand: `pred_*.txt`)

### Instant Cast (max rank 2)
- **Dispatch:** `mnk_instantCast2` does num2++ (:7683-7690; the guards :7685 / :7690 false), so sLv 2; `doSkill` calls
  `RPC_instantCast(position, vector2, num, num2)` directly (:9501) and sends `"RPC_instantCast" + num2` (:9510); the
  remote copies arrive through :2136-2148 -> :4553 / :4571. No clip, no actionState change.
- **Body** (:10938-11045, a `for (;;)` with junk `continue`s): `addTimeOut("instantCast", agiAdjust(240))` (:10945);
  `:10946` `19509 - 32367 != -12857` true -> for the owner `RPC_AddStatus("instantCast", sLv 2, chaAdjust(12), 0, ActorNr)`
  (:10954; `:10950` / `:10955` false). chaAdjust (CharacterControl.cs:20593-20612) at CHA 1, LCK 1:
  `Random.Range(0, CeilToInt(0.2 x 1))` = `Range(0, 1)` = 0, num = 1, `(int)(12 x 1.015)` = 12 s.
  - `Effects/instantCast_ring` (:10966; `:10962` / `:10967` false) and `createEffect(ring, transform.position,
    transform.rotation)` (:10978; `:10974` / `:10979` false).
  - Voice: `pvoice` on (:10992); `:10996` `129740 - 533583 == -403843` true -> `Game.mGameType <= 4` breaks (:10998),
    then the own-team test (:11004); `Voices/instantCast` (:11016); `:11024` true -> Block_9 PlayOneShot, volume 1 for
    the owner (:11044). BB voices it only in modes above 4; shown (Cat decision 38, Chameleon 42, Mole 39).
- **The status:** apply CharacterControl.cs:37821-37835 (`162087 - 51138 == 110949` and `81937 - 175912 == -93975`
  true): `setColor(0.78, 0.43, 0.34)`; removal :17075-17085 `setColor(0.86, 0.86, 0.86)`. Each spell cast instant
  spends one level (RPC_cast :25002-25062). Tint left out (Read this first 6).
- **Prefab `instantCast_ring`** (probe): EffectControl life 1, afterLife 0, followPosition, no followState; AudioSource
  `instantCast` (0.771 s) on awake; a RingEmitter 2.0 -> 0 m (2 per 0.2 s, life 0.25, `FireTrail1`) 0.1 m up and a
  LineEmitter burst of 24 (life 0.3, `FireRay`) 0.8 m up: a fiery ring closing on the Monkey. (`instantCast`, the cast
  routine's one, is the same with an image and the ring opening: the cast owners'.)
- **Step 1 s** (the ring's life; voice 0.85 s, sound 0.77 s).

### Fire Rune (max rank 3, passives on)
- **The proc** (FireRune :12273-12330; every predicate on the path true, `pred_instantCast_fireRune.txt`): owner only
  (:12278); not within 1 s of the last success (:12282); `getFireRuneLv()` 3 with #263 (:12229-12270); `Random.Range(0,
  100) >= lckAdjust(12)` breaks (:12297). lckAdjust (CharacterControl.cs:20658-20670) at LCK 1: num = 12 x 1.01 =
  12.12, `FloorToInt(100 x 12.12 / (12.12 - 12 + 100))` = `FloorToInt(12.105)` = 12, so 12 %. On success: lockout 1 s
  (:12303), `RPC_AddHeal(263, 0, 12, 12, ...)` (:12306), "FireRune!" (:12309), `RPC_fireRune(position, forward, 0)`
  (:12312) + ActionEvent (:12315).
- **RPC_fireRune** (:12334-12373): `Effects/fireRune_hit` (:12347; `:12343` / `:12348` false), `createEffect(..., 
  transform.position, Quaternion.identity)` (:12357; `:12355` true).
- **Prefab `fireRune_hit`** (probe): EffectControl life 1, followPosition; AudioSource `fireRune` (0.522 s); one
  `magicRune_tri` StaticMesh (`fireRune` material) faded by AlphaTimer (0 -> 0.6 in 0.2 s, out 0.3 s): a rune disc under
  the Monkey.
- **The tile:** the proc every play (Frost Spike / Berserker Rush precedent; the game needs a landed hit or an action's
  end). Step 1 s.
- **On other tiles (their owners):** the end-of-action calls roll whether or not anything was hit, so with the passive
  on each of these tiles gets `[t_end, "fx", "fireRune_hit", {"p": 0.12}]` at its closing state's time: the Fireball cast
  (`$RPC_fireBall_cast` :26569), Fire Keep's release (:37127), Fire Avatar's cast (:38557), Earth Form's cast (:40817) and
  its three attacks (:41299, :42007, :42530). Fire Avatar - Fireball (:38963) has it below. The per-hit calls need an
  enemy hit: no cue (as the Mole's Smart Shell).

### Earth Rune (max rank 3, passives on)
- **The proc** (EarthRune :13539-13584; predicates all true, `pred_earthRune.txt`): owner only; 1 s lockout (:13569);
  `getEarthRuneLv()` 3 (:13495); roll `< lckAdjust(12)` = 12 % (:13563); `RPC_AddHeal(363, 0, 12, 12)` (:13572);
  "EarthRune!" (:13575); `RPC_earthRune` (:13578). Callers: Update when `myDamage == -1` (:236-242),
  CharacterControl.cs:30341 (the Monkey hit), :30435 (his Gadina 1-4 / Buiten 1-4 hit; the look still at the Monkey).
- **RPC_earthRune** (:13600-13660): `Effects/earthRune_hit` (:13613), `createEffect(..., position, identity)` (:13623;
  `:13621` true).
- **Prefab `earthRune_hit`**: as `fireRune_hit` with the `earthRune` material; its AudioSource is also `fireRune`.
- **The tile:** the proc every play (Frost Spike: a hit absorbed; Berserker Rush: a hit taken). Step 1 s.

### Fire Avatar - Fireball (the form's normal attack)
- **Dispatch** (doNormalAttack :9603-9735): in the `fireAvatar` status (:9689), nAttack lock free, standby or run:
  `vector2 = target - position` (3 m or nearer: `3 x flat + up`), StartCoroutine `RPC_phoenixArmor_nAttack(position,
  vector2, tID)` (:9729).
- **The hidden body:** the status's apply (CharacterControl.cs:38328-38380; every guard as worked, the loop's
  `93669 - 119234 != -25565` false) sets isSpecialForm, AGI / TAL + 100, displayOffset + up and **`enabled = false` on
  every Renderer under the Monkey** (`GetComponentsInChildren(Renderer)`, :38348-38370). The armor is made after the
  status (:38371 then :38407), so it shows: `Instantiate(phoenixArmor, position, rotation)`, parent = the Monkey,
  localPosition 0, localRotation identity (:38407-38433), `Play("summon")` (:38438). Update keeps it on `root` / `run`
  outside attacks (:470-525: `CrossFade("root", 0.2)` when moveSpeed < 2, :509) and destroys it with the status (:495).
- **The coroutine** (`$RPC_phoenixArmor_nAttack$24778` :38728-39307; `pred_pAttack.txt`):
  - state 0: level `sLv = 1` (:39003), `+1` for each of `Time.time - actionTime > 3 / 6 / 9` (:39006-39041, `:39004`
    true, the inner guards false) = **4** (the top rank; the tile's hero has stood idle). Voice gate :39042-39058
    (pvoice, mode above 4, own team; shown), the switch (:39060-39183): 1 `sAttack1` (:39077, :39089), 2 and 3
    `sAttack2` (:39162, :39174), **4 `sAttack3`** (:39131, :39143). IL_8F6: actionState attack, actionTime, myCommand
    `pAttack`, `addTimeOut("nAttack", 1)` (:39189-39198), the hero faces the target (:39201-39210), the armor
    `Rewind()` + `Play("nAttack")` + `wrapMode Once` (:39219-39229), `Sounds/nAttack1` (:39256, PlayOneShot :39266: the
    owner always, others only in modes above 4, :39235-39245). Yield 0.4 (:39302).
  - state 2 at **0.4**: still attack / pAttack (:38856-38870); the owner: `firePos = mPos + TransformDirection(0.2, 1.5,
    1.5)` (:38880), `fireDir = tDir - TransformDirection(0.2, 1.5, 1.5)` (:38885), i.e. from the muzzle to the target;
    `RPC_fireBall_fire(firePos, fireDir, tID, 4)` (:38890, ActionEvent :38901) -> `fireBall4` (:11236), Instantiate at
    firePos, `LookRotation(fireDir)` (:11099, :11269), ProjectileControl Init, `life = 2 x rangeMod` (:11273-11278);
    `pAttack_ring` (:38914) `createEffect(ring, position, rotation)` (:38926). Yield 0.4 (IL_D5F -> IL_7B3 :39300).
  - state 3 at **0.8**: `FireRune()` (:38963; 12 %), standby (:38968-38983); then Update's `CrossFade("root", 0.2)`.
- **Geometry:** the target is the 10 m point on the ground, so fireDir = (0, 0, 10) - (0.2, 1.5, 1.5) = (-0.2, -1.5,
  8.5): yaw `atan(0.2 / 8.5)` = 1.35 deg to the left, pitch `atan(1.5 / sqrt(8.5^2 + 0.2^2))` = `atan(1.5 / 8.502)` =
  10.0 deg down: `rot [10.0, -1.35, 0]` at `x 0.2, y 1.5, d 1.5`. At 30 m/s (Monkey_fireBall.cs:26, :51) the 8.63 m
  take 0.29 s: the ball reaches the point at about 0.69 s (what it does on the ground is `Monkey_fireBall`'s part: the
  Fireball report's, Open question 5).
- **Prefabs** (probe): `phoenixArmor` no EffectControl, an Animation (default `root` 1.3 s loop; `run` 1.0, `nAttack`
  1.0, `blazingForm1` 0.8 Once, `blazingForm2` 0.7 Loop, `summon` 1.0), the Phoenix-shaped SkinnedMesh (2347 verts,
  material `phoenixArmor`: FX/Phoenix, `_Color` a 0.706, already drawn by mesh.js), a flame ParticleSystem on Spine1, a
  ground RingEmitter and two TrailEmitters; `pAttack_ring` EffectControl life 1 (no follow), an image ring and a burst at
  the muzzle (0.2, 1.5, 2.0); `fireBall4` needs `Monkey_fireBall`.
- **Step 1.8 s** (Fire Rune's 1 s effect from 0.8; pAttack_ring ends at 1.4).

### Blazing Fire (the form's charge)
- **Dispatch** (doBeginCharge :10183-10274): in `fireAvatar` (:10208), with #442 (:10212, else "Require BlazingFire
  Skill"), `mp >= 6` and `sp >= 6` (:10225-10231), the `blazingForm` lock free (:10238): StartCoroutine (:10253). The
  release: doReleaseCharge with myCommand `blazingForm` (:10594) starts `RPC_phoenixArmor_blazingForm0` (:10600).
- **The coroutine** (`$RPC_phoenixArmor_blazingForm$24791` :39351-40040; `flow_blazingForm.txt`, `pred_blazingForm.txt`):
  - state 0 at **0** (IL_34F :39938-40007, the wrappers true): attack, actionTime, command `blazingForm`,
    `addTimeOut("blazingForm", 6)`, the hero faces the target, moveSpeed 0; `blazingForm_ring` (:39969)
    `createEffect(ring, position, rotation)` (:39981); the armor `Play("blazingForm1")`, Once (:40001-40004). Yield 0.6
    (:40035).
  - state 2 at **0.6**: `blazingForm_fire` (:39493) `oux7JJkiIy = createEffect(fire, position, rotation)` (:39505);
    for the local player `CameraEffect.AddMotionBlur(8, 4, 4, ...)` (:39527-39532; left out). Yield 0.2 (:40026).
  - state 3 at **0.8**: `moveSpeed = 3` (:39559: the Monkey rushes forward at 3 m/s; shown in place), collisions with
    everything within 400 m ignored (:39564-39574), the armor `Play("blazingForm2")` + Loop (:39595-39600), its
    `phoenixArmor_tri/root` SkinnedMeshRenderer found (:39605-39616). Yield FixedUpdate (:40028).
  - state 4, every FixedUpdate while attack / blazingForm: before `actionTime + 1` the renderer's `materials[0].color.a =
    Lerp(0.7, 0, 5 x (t - 0.8))` (:39900-39927): the armor fades out over 0.8-1.0 s; at **1.0** (:39865) the renderer off
    (:39871), `blazingForm_fire.animation.Play("root")` (:39882), on to state 5.
  - state 5 every 0.3 s (Yield :40022) from 1.0: the owner pays 3 SP / 3 MP (2 with #404 / #414, :39744-39749) and hits
    `FindRecTarget(position - forward, forward, 2, 3, 3, 3)` with `hit(442, talAdjust(100))` and burn 4 on a foe
    without burn (:39754-39810): nothing drawn; out of MP or SP it releases itself (:39826).
  - when the state leaves (the release): alpha 0.7, renderer on, collisions back (:39658-39698).
- **The release** (`$RPC_phoenixArmor_blazingForm0$24812` :40111-40470, `flow_blazingForm0.txt`; the wrappers all false
  = the statements run): at **R**: attack, actionTime, command `blazingForm0`, vMovement 0, the 6 s lock
  (:40282-40302); `blazingForm0_ring` (:40318) `createEffect(ring, position, rotation)` (:40330); the armor
  `CrossFade("root", 0.5)` + Loop (:40360-40365), its renderer on (:40392); `blazingForm_fire.animation.Play("destroy")`
  (:40414; its followState also ends here: EffectControl records actionState and myCommand at its start, :122-137, and
  the command changed). Every FixedUpdate until R + 0.2 (:40421): alpha `Lerp(0, 0.7, 5 x (t - R))` (:40436-40447);
  Yield 0.15 (:40464); standby at R + 0.35 (:40247).
- **Hold:** R = 2.5 s: the full fire form from 1.0 s held 1.5 s, the SEQ's default for a held part (index.html, the
  comment over SEQ; the Monkey's own "Sentinel Guard: sentinalGuard1 sentinalGuard2* sentinalGuard0" takes it). Open
  question 4.
- **Prefabs** (probe): `blazingForm_ring` EffectControl life 1 + afterLife 1, followPosition, AudioSource
  `blazingForm_ring` (1.494 s), an image ring (delay 0.5); `blazingForm_fire` EffectControl life 99 + afterLife 0.2,
  followPosition, followState, an Animation (`create` 0.2 Once by itself, `root` 0.6 Loop, `destroy` 0.2), a winged
  SkinnedMesh (`blazingForm`), a ring ImageEmitter, two LineEmitter flame jets and a flame ParticleSystem, AudioSource
  `blazingForm_fire` looped (0.993 s); `blazingForm0_ring` EffectControl life 1 (no follow), AudioSource
  `blazingForm0_ring` (0.599 s), an image ring. All ready in the inventory.
- **Step 3.5 s** (blazingForm0_ring's life from 2.5).

## Choices made here (rule by rule, the earlier classes' decisions by analogy)
1. **Max rank:** Instant Cast 2 (the status level only: no look changes); Fire Rune 3, Earth Rune 3 (passives on; the
   look does not change with the rank); Fire Avatar - Fireball at level 4 (`fireBall4`, `sAttack3`: the code's top
   level, picked by idle time; the idle tile has stood).
2. **Procs every play** on the Fire Rune / Earth Rune tiles (Penguin Frost Spike, Bison Berserker Rush); the 12 % roll
   (`p: 0.12`, lckAdjust(12) at LCK 1, as Bat decision 12's Auto Mass and Cat decision 40) where the rune comes inside
   another move (Fire Avatar - Fireball here, six tiles of other owners).
3. **Identity = no `rot`** (Mole decision 49, the Bison's identity looks): fireRune_hit, earthRune_hit. The hero's
   rotation = no `rot`: instantCast_ring, pAttack_ring, blazingForm_ring, blazingForm_fire, blazingForm0_ring.
4. **The 10 m target point** on the ground for Fire Avatar's ball: the code aims at the target position, not a homing
   bounds centre (Open question 5 has the 0.6 m variant).
5. **Gated voices / sounds shown:** Instant Cast's and Fire Avatar's voices (modes above 4 only in BB) play (Cat 38,
   Chameleon 42, Mole 39).
6. **Left out:** Instant Cast's status tint (Penguin 10, Bat 13, Bison 34, Cat 44); the FireRune! / EarthRune! messages
   (as the Bison's BerserkerRush!); Blazing Form's camera motion blur (Bison 35); its 3 m/s rush (in place: Cat 77's
   Pillage Plunge, Penguin 8); the per-hit rune calls and Earth Rune on summons (no enemy, no hit).
7. **The hidden body** (`[0, "hideProp", "hero"]`, no kill = until the next pick: the Chameleon's Thunder Dragon,
   decisions 48-49): the status hides every renderer, props and weapon_fx included.
8. **Step lengths:** the longest effect or voice: Instant Cast 1, Fire Rune 1, Earth Rune 1, Fire Avatar - Fireball 1.8,
   Blazing Fire 3.5; all held (`root*@t`, the 0.6 s idle loops; Cat decision 9).

## Missing page parts

### P1. The armor's and the fire form's clips and fades from the hero's code (`fx:phoenixArmor`, `fx:blazingForm_fire`)
- **Why:** the Monkey's code plays the armor's clips (`nAttack`, `blazingForm1`, `blazingForm2`, `root` with crossfades)
  and fades its material (alpha 0.7 -> 0 -> 0.7, the renderer off between), and plays the fire form's `root` at 1.0 s
  (`destroy` comes with the page's followState end). The page plays only an effect's default clip; `anims` exists only
  inside `fx:grandCasinoArcade` (fxparts/cat.js:108-140).
- **Interface:** cue options `anims` (already in OPTS): `[[age, clip, fade?], ...]`, each played once when the
  effect's age passes it, `fxAnim.play(clip, fade)` (mesh.js: Play, or CrossFade over fade s); `alpha` (new):
  `[[age, a], ...]`, the opacity of every skinned material of the effect: untouched before the first key, linear
  between keys, held after the last; `a == 0` hides the material (the renderer off).
- **Who else uses it:** the Fire Avatar tile's owner (the armor's `summon` clip at its creation, :38438, then root), if
  it spawns the armor. Earth Form's `gadinaArmor` is the same kind of armor (its owner's call).
- **Where:** a Monkey part module (the parts report's `wardrobe/fxparts/monkey.js`, with `Monkey_fireBall`; add
  `"monkey"` to FX_PART_FILES, index.html:3940-3955) and `"alpha"` in `pipeline/wardrobe_fx_check.py` OPTS (:171-174).
  Code in PASTE-READY block 5.

### P2. A tile whose Bible card borrows another skill's icon (`ICON_ALIAS`)
- **Why:** the card "Fire Avatar - Fireball" (`monkey_fireAvatar_fireBall`, index.html:18917-18922) uses the icon
  `monkey_fireBall4`; `wardrobe_skill_icons.py` finds icons by `<cls>_<skill><n>` names only (:80-87), and the key
  `fireBall` is the Fireball tile's.
- **Interface:** `ICON_ALIAS = {"monkey": {"fireAvatarFireBall": "fireBall"}}`: the alias gets the source's best icon
  under its own key (`icons/hd/monkey/fireAvatarFireBall.webp`, clips `["root"]`).
- **Where:** `pipeline/wardrobe_skill_icons.py` after `lower = {...}` (:87). Block 4.

### Needed from another report: `Monkey_fireBall`
`fireBall4` (and fireBall1-3) cannot be built without it (`fx_inventory.md`, the probe). Its own skill (Fireball) needs
it, so the parts report builds it; until then the Fire Avatar - Fireball tile draws everything but the ball.

## PASTE-READY

### 1. `wardrobe/index.html` SEQ: the monkey line (index.html:1252-1253) gains a comment and five tiles (keep any other researcher's lines, append these)

```js
  monkey: ["Normal Attack: nAttack1 nAttack2~", "Charge Attack: cAttack1 cAttack2*", "Cast: cast1 cast2*~@0 cast3~",
    "Damage Cast: damageCast1 damageCast2*~@0 cast3~", "Sentinel Guard: sentinalGuard1 sentinalGuard2* sentinalGuard0",
    // Instant Cast plays no animation (doSkill calls RPC_instantCast straight, Monkey.cs:9501; doSkill :7366-9535 calls
    // no PlayAnimation); Fire Rune and Earth Rune (passives) are procs at the Monkey (FireRune :12273, EarthRune :13539);
    // in Fire Avatar the body is hidden (CharacterControl.cs:38348-38380) and the armor plays the form's normal attack
    // and Blazing Fire's charge (:39224, :40001, :39595): their effects on the idle stance, the hero hidden in the two
    // form tiles, held (the 0.6 s idle loops) as long as the last effect: Instant Cast / the runes 1 s, Fire Avatar -
    // Fireball 1.8 s (Fire Rune's roll at 0.8 + 1), Blazing Fire 3.5 s (released at 2.5, its ring's 1 s)
    // (2026-11-13, plans/fx_monkey/effect_only.md)
    "Instant Cast: root*@1", "Fire Rune: root*@1", "Earth Rune: root*@1", "Fire Avatar - Fireball: root*@1.8",
    "Blazing Fire: root*@3.5"],
```

### 2. `wardrobe/index.html` SEQ_SKILL (index.html:3338-3350): add a monkey entry (merge with any other monkey ids)

```js
  monkey: { "@InstantCast": "instantCast", "@FireRune": "fireRune", "@EarthRune": "earthRune",
    "@FireAvatar-Fireball": "fireAvatarFireBall", "@BlazingFire": "blazingFire" },
```
(The chain id is the SEQ name with its spaces dropped, `chains()` index.html:1358: "Fire Avatar - Fireball" ->
`@FireAvatar-Fireball`; wardrobe_fx_check.py `split_key` drops spaces the same way.)

### 3. `wardrobe/fx_cues/monkey.json`: five entries (the file is `{}` today; the same text, checked with json.load, is `checks/fx_monkey_research/effect_only/cues.json`)

```json
  "@InstantCast:root": {
    "why": "Monkey.cs RPC_instantCast (:10938-11045), a plain method doSkill calls straight (mnk_instantCast2 num2++ :7683-7690, call :9501, ActionEvent RPC_instantCast + sLv :9510; doSkill :7366-9535 calls no PlayAnimation / animation.Play / CrossFade), so the Monkey goes on with what he was doing; the tile plays it on the idle stance. At max rank (Instant Cast 2): addTimeOut instantCast agiAdjust(240) (:10945), for the owner the instantCast status Lv 2 for chaAdjust(12) = 12 s at CHA 1 (:10954; its two instant casts are the cast tiles' business, RPC_cast :25002-25062), Effects/instantCast_ring (:10966) createEffect at the hero's position and rotation (:10978; EffectControl life 1, followPosition, no followState; its own AudioSource Sounds/instantCast 0.771 s), Voices/instantCast (0.850 s; :11016, PlayOneShot :11044 through :11024's Block_9; BB plays it only in modes above 4 to the own team, :10996-11008, shown as Cat decision 38). Predicates worked in checks/fx_monkey_research/effect_only/pred_instantCast_fireRune.txt. Left out: the status's tint setColor(0.78, 0.43, 0.34) (CharacterControl.cs:37821-37835, back to 0.86 at :17075-17085), as the Penguin's multiCast tint (Penguin decision 10, Bison 34, Cat 44)",
    "cues": [
    [0, "fx", "instantCast_ring"],
    [0, "voice", "instantCast"]
    ]
  },
  "@FireRune:root": {
    "why": "Monkey.cs FireRune (:12273-12330), Fire Rune #261-263's proc (no clip; the tile plays it on the idle stance, the proc every play, as the Penguin's Frost Spike and the Bison's Berserker Rush): for the owner (:12278), once per 1 s (:12282, set :12303), at Fire Rune 3 (getFireRuneLv :12229-12270, passives on) a roll Random.Range(0, 100) < lckAdjust(12) = 12 % at LCK 1 (:12297; CharacterControl.cs:20658-20670) heals 12 MP / 12 SP (RPC_AddHeal(263, 0, 12, 12) :12306; no look), the FireRune! message (:12309; left out), RPC_fireRune (:12312 -> :12334-12373): Effects/fireRune_hit (:12347) createEffect at the hero's position, Quaternion.identity (:12357; no rot, as Mole decision 49's identity looks; EffectControl life 1, followPosition; its AudioSource Sounds/fireRune 0.522 s; a magicRune StaticMesh faded by AlphaTimer 0.2 in / 0.3 out). BB calls FireRune per landed hit (Combo, Mike Blink, Damage Cast, Blazing Arrow, Flash Fire, both Fireballs) and once at the end of the Fireball cast, Fire Keep's release, Fire Avatar's cast and attack, Earth Form's cast and attacks (18 sites, Bible monkey-skill-reference.md 4.7)",
    "cues": [
    [0, "fx", "fireRune_hit"]
    ]
  },
  "@EarthRune:root": {
    "why": "Monkey.cs EarthRune (:13539-13584), Earth Rune #361-363's proc (no clip; the tile plays it on the idle stance, the proc every play, as the Penguin's Frost Spike): run when the Monkey takes a hit (Update's myDamage == -1 :236-242, CharacterControl.cs AddDamage :30341) or his Gadina / Buiten does (:30435); for the owner, once per 1 s (:13569), at Earth Rune 3 (getEarthRuneLv :13495, passives on) a roll < lckAdjust(12) = 12 % (:13563) heals 12 MP / 12 SP (RPC_AddHeal(363, 0, 12, 12) :13572), the EarthRune! message (:13575; left out), RPC_earthRune (:13578 -> :13600): Effects/earthRune_hit (:13613) createEffect at the Monkey's position, Quaternion.identity (:13623; EffectControl life 1, followPosition; the fireRune_hit layout with the earthRune material, its AudioSource the same Sounds/fireRune 0.522 s)",
    "cues": [
    [0, "fx", "earthRune_hit"]
    ]
  },
  "@FireAvatar-Fireball:root": {
    "why": "Monkey.cs doNormalAttack (:9603) in the fireAvatar status (:9689) starts $RPC_phoenixArmor_nAttack$24778 (:9729 -> :38728-39307), which plays no body clip: the status hid every renderer under the Monkey at its start (CharacterControl.cs:38348-38380) and the armor Effects/phoenixArmor parented to him (:38407-38433) plays the attack (hideProp hero, the armor at the hero with the anims). At 0: level 1 + 1 each past 3 / 6 / 9 s since the last action (:39003-39041) = 4, the top rank (the idle tile has stood; fireBall4); voice sAttack3 for level 4 (:39117-39143; levels 2-3 sAttack2 :39156-39174, 1 sAttack1 :39065-39089; BB plays them in modes above 4 to the own team, :39042-39058, shown); the attack state, nAttack lock 1 s, the hero faces the target (:39189-39210); the armor Rewind + Play(nAttack) + Once (:39219-39229); Sounds/nAttack1 (0.118 s; :39256-39266, the owner always). Yield 0.4 (:39302): at 0.4 for the owner firePos = hero + TransformDirection(0.2, 1.5, 1.5) (:38880), fireDir = (target - hero) - that offset (:38885) = from the muzzle to the 10 m target point on the ground: LookRotation((-0.2, -1.5, 8.5)) = pitch 10.0 deg down, yaw 1.35 deg left; RPC_fireBall_fire(firePos, fireDir, tID, 4) (:38890 -> :11092-11290: fireBall4 :11236, Instantiate at firePos, LookRotation(fireDir) :11099 / :11269, ProjectileControl life 2 x rangeMod :11278; Monkey_fireBall 30 m/s, the Fireball report's part); pAttack_ring at the hero's position and rotation (:38914-38926; EffectControl life 1, its emitters at the muzzle 0.2, 1.5, 2.0). Yield 0.4 (:39300): at 0.8 FireRune() (:38963: Fire Rune 3, 12 %, fireRune_hit at the hero, identity) and standby (:38968); Update then CrossFades the armor to root over 0.2 s (:509, the state no longer attack, moveSpeed < 2)",
    "cues": [
    [0, "hideProp", "hero"],
    [0, "fx", "phoenixArmor", {"kill": 1.8, "anims": [[0, "nAttack"], [0.8, "root", 0.2]]}],
    [0, "voice", "sAttack3"],
    [0, "sound", "nAttack1"],
    [0.4, "fx", "fireBall4", {"x": 0.2, "y": 1.5, "d": 1.5, "rot": [10.0, -1.35, 0]}],
    [0.4, "fx", "pAttack_ring"],
    [0.8, "fx", "fireRune_hit", {"p": 0.12}]
    ]
  },
  "@BlazingFire:root": {
    "why": "Monkey.cs doBeginCharge (:10183) in the fireAvatar status with Blazing Fire #442, 6 MP / 6 SP and no blazingForm lock (:10208-10238) starts $RPC_phoenixArmor_blazingForm$24791 (:10253 -> :39351-40040), no body clip (the Monkey hidden by the status, CharacterControl.cs:38348-38380; hideProp hero). At 0 (:39938-40007): attack state, command blazingForm, blazingForm lock 6 s, the hero faces the target, moveSpeed 0; Effects/blazingForm_ring at the hero's position and rotation (:39969-39981; EffectControl life 1 + afterLife 1, followPosition, its AudioSource Sounds/blazingForm_ring 1.494 s); the armor Play(blazingForm1) + Once (:40001-40004). Yield 0.6 (:40035): at 0.6 Effects/blazingForm_fire at the hero's position and rotation (:39493-39505; EffectControl life 99 + afterLife 0.2, followPosition, followState: ends when the release changes the command; its Animation create 0.2 s plays by itself; its looped Sounds/blazingForm_fire 0.993 s) and the camera motion blur (:39527-39532; left out, Bison decision 35). Yield 0.2 (:40026): at 0.8 moveSpeed 3 (:39559; the dash shown in place, as Cat decision 77's Pillage Plunge), the armor Play(blazingForm2) + Loop (:39595-39600); every FixedUpdate the armor's materials[0] alpha Lerp(0.7, 0, 5 (t - 0.8)) (:39900-39927), at 1.0 s its renderer off (:39865-39871) and blazingForm_fire Play(root) (:39882); from 1.0 every 0.3 s (Yield :40022) MP / SP - 3 (:39744-39749) and a FindRecTarget hit with burn 4 on foes (:39759-39810; nothing drawn). Held 1.5 s of full form (the SEQ's held-part default): release at 2.5 (doReleaseCharge :10594-10600 -> $RPC_phoenixArmor_blazingForm0$24812 :40111-40470): command blazingForm0 (:40282-40302; blazingForm_fire's followState end: cut 2.5, and Play(destroy) :40414), Effects/blazingForm0_ring at the hero's position and rotation (:40318-40330; EffectControl life 1, its AudioSource Sounds/blazingForm0_ring 0.599 s), the armor CrossFade(root, 0.5) + Loop (:40360-40365), its renderer on (:40392) and alpha Lerp(0, 0.7, 5 (t - 2.5)) to 2.7 (:40421-40447); Yield 0.15 (:40464): standby at 2.85 (:40247)",
    "cues": [
    [0, "hideProp", "hero"],
    [0, "fx", "phoenixArmor", {"kill": 3.5, "anims": [[0, "blazingForm1"], [0.8, "blazingForm2"], [2.5, "root", 0.5]], "alpha": [[0.8, 0.7], [1.0, 0], [2.5, 0], [2.7, 0.7]]}],
    [0, "fx", "blazingForm_ring"],
    [0.6, "fx", "blazingForm_fire", {"cut": 2.5, "anims": [[0.4, "root"]]}],
    [2.5, "fx", "blazingForm0_ring"]
    ]
  }
```
(The comma after the last `}` only if another entry follows. `alpha` is not in `wardrobe_fx_check.py`'s OPTS yet: the
check fails on `@BlazingFire:root` until P1 adds it; the other options are there.) Check with
`py -3 -c "import json; json.load(open('wardrobe/fx_cues/monkey.json', encoding='utf-8'))"`.

### 4. `pipeline/wardrobe_skill_icons.py`: EFFECT_ONLY (:49-53) gains the monkey list; P2's alias

```python
               "cat": ["awareness", "damageRoulette", "treasureHunt"],
               # the Monkey's Instant Cast, Fire Rune, Earth Rune and the two Fire Avatar moves (2026-11-13,
               # plans/fx_monkey/effect_only.md)
               "monkey": ["instantCast", "fireRune", "earthRune", "fireAvatarFireBall", "blazingFire"]}
# a tile whose Bible card borrows another skill's icon (2026-11-13, plans/fx_monkey/effect_only.md P2: the card
# Fire Avatar - Fireball, monkey_fireAvatar_fireBall, shows monkey_fireBall4)
ICON_ALIAS = {"monkey": {"fireAvatarFireBall": "fireBall"}}
```
```python
        lower = {s.lower(): s for s in best}
        for a, src in ICON_ALIAS.get(cls, {}).items():   # P2: the alias takes the source skill's best icon
            if src in best:
                best[a] = best[src]; lower[a.lower()] = a
```
The Bible has `monkey_instantCast2`, `monkey_fireRune3`, `monkey_earthRune3`, `monkey_fireBall4`,
`monkey_blazingFire5` (assets.js; cards index.html:18029, :18328, :18647, :18917-18922, :18944-18948). Then
`py -3 pipeline\wardrobe_skill_icons.py`.

### 5. P1, the part (in the Monkey part module, `wardrobe/fxparts/monkey.js`, inside its `register(api)`)

```js
  // ---------------------------------------------------------------- fx:phoenixArmor, fx:blazingForm_fire (the hero's code)
  // Monkey.cs (2026-11-13, plans/fx_monkey/effect_only.md P1): the Fire Avatar armor Effects/phoenixArmor (parented to
  // the hero, :38407-38433; Animation root 1.3 s loop, run, nAttack 1.0, blazingForm1 0.8 Once, blazingForm2 0.7 Loop,
  // summon 1.0) is played by the hero's code: the form's attack Rewind + Play("nAttack") (:39219-39229), Update's
  // CrossFade("root", 0.2) after it (:509), Blazing Form's Play("blazingForm1") (:40001), Play("blazingForm2") + Loop
  // (:39595-39600), the release's CrossFade("root", 0.5) (:40360); its SkinnedMeshRenderer's materials[0].color.a
  // (FX/Phoenix: the opacity) lerped 0.7 -> 0 over 0.8-1.0 s, the renderer off at 1.0 (:39871, :39900-39927), on again
  // and 0 -> 0.7 over 0.2 s at the release (:40392, :40436-40447). The fire form blazingForm_fire: Play("root") at 1.0 s
  // (:39882; its "destroy" at the release comes with the page's followState end, as :40414). The cue gives the ages:
  // anims [[age, clip, fade?], ...] (fxAnim.play: Play, or CrossFade over fade s), alpha [[age, a], ...] (every skinned
  // material's opacity: untouched before the first key, linear between keys, held after; 0 = off)
  const scheduled = fx => {
    if (fx.cls !== "monkey") return null;
    const anims = (Array.isArray(fx.at?.anims) ? fx.at.anims : []).slice().sort((a, b) => a[0] - b[0]);
    const keys = Array.isArray(fx.at?.alpha) ? fx.at.alpha : [];
    const anim = fx.nodes.find(o => o?.userData?.fxAnim)?.userData.fxAnim, mats = [];
    fx.root.traverse(o => { if (o.isSkinnedMesh) mats.push(...[].concat(o.material)); });
    let t = 0, k = 0;
    return { node: fx.root, update(dt) {
      t += dt;
      while (k < anims.length && t >= anims[k][0]) { const [, clip, fade] = anims[k++]; anim?.play(clip, fade); }
      if (!keys.length || t < keys[0][0]) return;
      const i = keys.findIndex(q => q[0] > t);
      const a = i < 0 ? keys[keys.length - 1][1] : keys[i - 1][1] + (keys[i][1] - keys[i - 1][1]) * (t - keys[i - 1][0]) / (keys[i][0] - keys[i - 1][0]);
      for (const m of mats) { m.opacity = a; m.visible = a > 0; }
    } };
  };
  api.part("fx:phoenixArmor", scheduled);
  api.part("fx:blazingForm_fire", scheduled);
```
```python
# pipeline/wardrobe_fx_check.py OPTS (:171-174): add "alpha" (fxparts/monkey.js fx:phoenixArmor, plans/fx_monkey/effect_only.md P1)
```
```js
// wardrobe/index.html FX_PART_FILES (:3940-3955): add "monkey" (if the parts report has not already)
```
`fxAnim.play(name, fade)` is mesh.js's Animation (mesh.js:270-298); `play(name)` with fade undefined is a cut, as
`Play`. Check by screenshot that the FX/Phoenix material takes the opacity (mesh.js `phoenix()` makes it
`transparent: true`, opacity = `_Color.a`).

### 6. Build and check

```
uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py monkey --fx instantCast_ring,fireRune_hit,earthRune_hit,phoenixArmor,pAttack_ring,fireBall4,blazingForm_ring,blazingForm_fire,blazingForm0_ring --voices instantCast,sAttack3 --sounds nAttack1
py -3 pipeline\wardrobe_skill_icons.py
uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py C:/work/12tails-wardrobe checks/fx_monkey dark --cls monkey
```
A plain `wardrobe_fx.py monkey` builds them from the cue file once every Monkey cue is in. `fireBall4` builds only after
`Monkey_fireBall` exists.

## Left out (with reasons)
- Instant Cast's status tint (0.78, 0.43, 0.34) for 12 s: status tints stay out (Penguin 10, Bat 13, Bison 34, Cat 44).
- FireRune! / EarthRune! on-screen messages; the MP / SP heals (numbers, no effect: RPC_AddHeal CharacterControl.cs
  :7130-7393 loads none).
- Blazing Form's motion blur (Bison 35), its 3 m/s rush (in place), its hits / burn on foes (no enemy).
- Fire Rune's per-hit calls and Earth Rune's summon-hit calls (no enemy, no hit: as the Mole's Smart Shell).
- The 13 shared supplements (out of every class's roster), the mission icons (Penguin 19).

## Open questions (each with my recommended answer)
1. **Who owns the Fire Avatar moves.** They play no body clip, so they fell here; the Fire Avatar researcher may also
   have written them. *Recommend this report's two tiles* (one tile per Bible card), merged with whatever that report
   gives for the armor's `summon` and the form's end (`phoenixArmor_destroy`); keep one copy of each.
2. **Fire Avatar - Fireball's level.** BB picks 1-4 by idle time (3 / 6 / 9 s). *Recommend level 4* (top rank;
   `fireBall4`, `sAttack3`). Alternative: level 1 (`fireBall1`, `sAttack1`), what a fast repeat gives.
3. **Instant Cast's tint.** *Recommend leaving it out* (precedent). If wanted: HERO_SKINS
   `"instantCast": () => ({ tint: [0.78 / 0.86, 0.43 / 0.86, 0.34 / 0.86] })` (a body look, as `enrage`) and
   `[0, "skin", "instantCast", {"kill": 10}]` (12 s cut at 10), the step then `root*@10`.
4. **Blazing Form's hold.** BB holds while the key is held and MP / SP last. *Recommend release at 2.5 s* (1.5 s of full
   form, the SEQ default). Alternative: longer, e.g. 4 s, to show the 0.3 s drain rhythm (which draws nothing).
5. **Fire Avatar's ball aim and landing.** *Recommend the 10 m point on the ground* (`rot [10.0, -1.35, 0]`), the
   target position BB aims at; the homing-style 0.6 m up would be `rot [6.04, -1.35, 0]`. What the ball does on the
   ground (a `fireBall_hit` or flying on to its 2 s life) is `Monkey_fireBall`'s, decided by the Fireball report; this
   tile follows it.
6. **Fire Rune on other tiles.** *Recommend the six end-of-action rolls* (`p: 0.12`) on the Fireball, Fire Keep, Fire
   Avatar and Earth Form tiles (their owners), as Bat decision 12's Auto Mass; the Fire Rune tile shows the look sure.
7. **The hidden hero.** *Recommend `hideProp hero` with no kill* (until the next pick). If the loop's next round should
   show the Monkey for a frame, give `kill` = the step instead.
8. **Bible offers (not written there):** Fire Avatar hides every renderer of the Monkey (CharacterControl.cs:38348-38370)
   and the form's moves are the armor's own clips (no body clip); the form attack's level by idle time picks the voice
   (1 sAttack1, 2-3 sAttack2, 4 sAttack3) besides the fireball; the ball leaves from 0.2 right, 1.5 up, 1.5 ahead and
   flies straight at the target position; Blazing Form's timeline (the armor fades out 0.8-1.0 s, the fire form from
   0.6 s, the rush at 3 m/s from 0.8 s, collisions off, the first drain tick at 1.0 s, the release fade-in 0.2 s and
   standby 0.35 s after); Instant Cast's status tint (0.78, 0.43, 0.34); Instant Cast's and the Fire Avatar attack's
   voices only in modes above 4 (to the own team); Earth Rune's and Fire Rune's looks at the Monkey with world
   identity rotation, the Earth Rune effect sounding Fire Rune's sound.

## Verification (2026-11-13)

Checker, office PC, read only (probes in `checks/fx_monkey_research/verify/`: `probe_ae_eo.json` = `wardrobe_fx.py monkey
--probe` of every effect named here and in attacks_emotes.md; `cues_check.py` parses block 3 and checks its keys and
options). The Verification wins over the body.

**Checked and holding:**
- Instant Cast: `RPC_instantCast` called straight (:9501); `addTimeOut` :10945, `RPC_AddStatus("instantCast", sLv,
  chaAdjust(12))` :10954, `Effects/instantCast_ring` :10966 at the hero's position and rotation :10978,
  `Voices/instantCast` :11016. Bible card maxRank 2, icon `monkey_instantCast2` (bible index.html:18026-18031).
- Fire Rune / Earth Rune: `fireRune_hit` :12347 and `earthRune_hit` :13613, both `Quaternion.identity` (:12357,
  :13623); probe: EffectControl life 1, followPosition, both AudioSources `fireRune`. Bible lckProc 12 (BB; the 45 / 60 /
  75 % is TTO's later change, not this page's).
- Fire Avatar - Fireball: level 1 + 1 per 3 / 6 / 9 s idle (Monkey.cs:39003-39037; Bible reference 4.17), level 4 =
  `sAttack3` (:39131), `Effects/fireBall4` (:11236), `firePos` / `fireDir` (:38880, :38885), `pAttack_ring` (:38914-38926),
  `FireRune()` at 0.8 (:38963); Yields 0.4 / 0.4 (:39302, :39300). The aim: (0, 0, 10) - (0.2, 1.5, 1.5) = (-0.2, -1.5,
  8.5): pitch atan(1.5 / 8.502) = 10.0 deg, yaw atan(0.2 / 8.5) = 1.35 deg left: `rot [10.0, -1.35, 0]` holds; the 0.6 m
  variant atan(0.9 / 8.502) = 6.04 deg holds too.
- Blazing Fire: Yields 0.6 / 0.2 (:40035, :40026), `moveSpeed = 3` :39559, `Play("blazingForm2")` :39595, the fade
  `Lerp(0.7, 0, 5 (t - actionTime - 0.8))` :39900-39927, `actionTime + 1` :39865, `blazingForm_fire.Play("root")`
  :39882; the release `blazingForm0_ring` :40318, `CrossFade("root", 0.5)` :40360, `Play("destroy")` :40414, `+ 0.2`
  :40421, `Yield 0.15` :40464.
- Every effect builds by the probe (instantCast_ring, fireRune_hit, earthRune_hit, phoenixArmor, pAttack_ring,
  blazingForm_ring, blazingForm_fire, blazingForm0_ring) except `fireBall4` ("no layout for Monkey_fireBall", parts.md
  part 1, as the report says). Voices `instantCast`, `sAttack3` and the sound `nAttack1` are in the rip. The armor's clips
  (root 1.3 Loop, run, nAttack 1.0, blazingForm1 0.8 Once, blazingForm2 0.7 Loop, summon 1.0) and the fire form's (create
  0.2 Once, root 0.6 Loop, destroy 0.2 Once; EffectControl life 99 + 0.2, followPosition, followState) match the probe.
- Block 3: the five entries parse, the keys are the proposed SEQ ids (`@FireAvatar-Fireball` = the name with its spaces
  dropped, index.html chains(); wardrobe_fx_check.py `split_key` :96-101), every option is in OPTS except `alpha` (as the
  report says). No step's cue sits at or past its step's end. Nothing TTO here.
- Monkey.cs has 16 `FireRune()` calls plus Monkey_fireBall.cs:261 (the Bible's 18 sites count the Fireball's twice).

1. **P1 collides with parts.md part 8 (the most important).** parts.md:336-348 registers the same `fx:phoenixArmor`
   (and `fx:gadinaArmor`) in `fxparts/elementals.js`, with a cue option `clips` and a default `summon` then `root`.
   The page keeps one part per name (`FXPARTS["fx:" + name]`, index.html:4235), so the second module to load would
   silently replace the first, and one report's cues would lose their clips. **Decision:** one part, registered once,
   in the file the parts build puts part 8 in (it serves the Fire Avatar tile's `summon` and Earth Form's armor too).
   It reads the existing option **`anims`** (already in OPTS, wardrobe_fx_check.py:177, and in the cue-format comment
   for fx:grandCasinoArcade), each item `[age, clip, fade?, wrap?]`, with parts.md's default timeline when a cue gives
   none, plus this report's new **`alpha`**. parts.md's `clips` name is dropped. The full code is in finding 2.

2. **P1's alpha would fade every copy of the armor at once.** `mesh.js` keeps one material per effect material name
   (`mats[k]`, k = cls/name, wardrobe/fxparts/mesh.js:180-184), so `m.opacity = a; m.visible = a > 0` on it fades and
   hides every live phoenixArmor: the loop's next round, the Fire Avatar tile's armor. `alphatimer.js` clones per
   renderer for this reason (wardrobe/fxparts/alphatimer.js:52-63). **Corrected block 5** (in place of the report's,
   merged with parts.md part 8; register it once):
```js
  // ------------------------------------------------- fx:phoenixArmor, fx:gadinaArmor, fx:blazingForm_fire (the hero's code)
  // Monkey.cs (2026-11-13, plans/fx_monkey/effect_only.md P1 + Verification 1-2, parts.md part 8): the Fire Avatar armor
  // Effects/phoenixArmor and the Earth Form armor gadinaArmor (parented to the hero, :38407-38433, :40732-40747) and the
  // fire form blazingForm_fire are played by the hero's code: Play("summon") at creation, then Update's CrossFade("root",
  // 0.2) + Loop (:509, :523; :573, :587); the form's attack Rewind + Play("nAttack") (:39219-39229); Blazing Form's
  // Play("blazingForm1") (:40001), Play("blazingForm2") + Loop (:39595-39600), the release's CrossFade("root", 0.5)
  // (:40360); the armor's materials[0].color.a lerped 0.7 -> 0 over 0.8-1.0 s, the renderer off at 1.0 (:39871,
  // :39900-39927), on again and 0 -> 0.7 over 0.2 s at the release (:40392, :40436-40447); the fire form's Play("root") at
  // 1.0 s (:39882). The cue gives the ages: anims [[age, clip, fade?, wrap?], ...] (fxAnim.play(clip, fade, wrap): Play,
  // or CrossFade over fade s; none given: summon, then root), alpha [[age, a], ...] (the opacity of this effect's own
  // copies of its skinned materials, mesh.js sharing one per name: untouched before the first key, linear between keys,
  // held after; 0 = the renderer off)
  const scheduled = dflt => fx => {
    if (fx.cls !== "monkey") return null;
    const given = Array.isArray(fx.at?.anims) ? fx.at.anims.filter(a => Array.isArray(a) && a.length >= 2) : [];
    const anims = (given.length ? given : dflt).slice().sort((a, b) => a[0] - b[0]);
    const keys = Array.isArray(fx.at?.alpha) ? fx.at.alpha.slice().sort((a, b) => a[0] - b[0]) : [];
    const anim = fx.nodes.find(o => o?.userData?.fxAnim)?.userData.fxAnim;
    const meshes = [], own = [];
    if (keys.length) fx.root.traverse(o => {
      if (!o.isSkinnedMesh) return;
      const list = [].concat(o.material).map(m => {
        const c = m.clone(); c.onBeforeCompile = m.onBeforeCompile; c.customProgramCacheKey = m.customProgramCacheKey;
        own.push(c); return c;
      });
      o.material = Array.isArray(o.material) ? list : list[0];
      meshes.push([o, list]);
    });
    let t = 0, k = 0;
    return { node: fx.root, update(dt) {
      t += dt;
      while (k < anims.length && t >= anims[k][0]) { const [, clip, fade, wrap] = anims[k++]; anim?.play(clip, fade, wrap); }
      if (!keys.length || t < keys[0][0]) return;
      const i = keys.findIndex(q => q[0] > t);
      const a = i < 0 ? keys[keys.length - 1][1]
        : keys[i - 1][1] + (keys[i][1] - keys[i - 1][1]) * (t - keys[i - 1][0]) / (keys[i][0] - keys[i - 1][0]);
      for (const [o, list] of meshes) { o.visible = a > 0; for (const m of list) m.opacity = a; }
    }, dispose() { for (const m of own) m.dispose(); } };
  };
  api.part("fx:phoenixArmor", scheduled([[0, "summon"], [1.0, "root", 0.2, 2]]));
  api.part("fx:gadinaArmor", scheduled([[0, "summon"], [0.8, "root", 0.2, 2]]));
  api.part("fx:blazingForm_fire", scheduled([]));
```
   (Fx.dispose calls each part's dispose, index.html:4382.) Also add `"alpha"` to wardrobe_fx_check.py OPTS (:176-181)
   and write `alpha` and the anims items' fade / wrap into index.html's cue-format comment (the Cat block, index.html:4716-4718,
   says `[[seconds after the spawn, clip], ...]`). Block 3's cues stay as they are (their anims items fit the wider
   form).

3. **P2 is not needed: point SEQ_SKILL at `fireBall`.** `moveSkillIcons` takes the tile's skill from SEQ_SKILL, then
   `HDI[cls][skill]`, else the class's top-rank small icon of that skill (index.html:3411-3415). With
   `"@FireAvatar-Fireball": "fireBall"` the tile shows the Fireball's icon, which is the Bible card's (`monkey_fireBall4`,
   bible index.html:18922): the HD one once the Fireball's own tile puts `fireBall` in `icons/hd/index.json`, else
   `icons/skills/monkey/fireball4.webp`. No ICON_ALIAS, no new key. `fireBall` in `pooled` (:3420) only keeps it off
   tiles that are not the Fireball's, which one tile per skill wants anyway. "fireAvatarFireBall" leaves EFFECT_ONLY too
   (its `lower.get` finds no such Bible key and prints "no icon", wardrobe_skill_icons.py:128). **Corrected block 4:**
```python
               "cat": ["awareness", "damageRoulette", "treasureHunt"],
               # the Monkey's Instant Cast, Fire Rune, Earth Rune and Blazing Fire (2026-11-13, plans/fx_monkey/effect_only.md;
               # Fire Avatar - Fireball takes the Fireball's icon through SEQ_SKILL, Verification 3)
               "monkey": ["instantCast", "fireRune", "earthRune", "blazingFire"]}
```
   (and nothing after `lower = {...}`.)

4. **Block 1 and block 2 must merge with attacks_emotes.md; their line numbers moved.** Block 1 re-lists the old
   `"Normal Attack: nAttack1 nAttack2~"` and `"Charge Attack: cAttack1 cAttack2*"`, which attacks_emotes.md replaces.
   The SEQ monkey line is now index.html:1296-1297 (not 1252-1253), SEQ_SKILL :3393-3409 (not 3338-3350), FX_PART_FILES
   :4014 (not 3940-3955). **Corrected block 1** (keep any skills / TTO report lines too, and the report's comment over
   the five effect-only tiles):
```js
  monkey: ["Normal Attack: nAttack1@0.5 nAttack2~", "Mike Blink: nAttack1@0.5 nAttack2~", "HP Transfer: cAttack1 cAttack2*@3.2",
    "Mike Circle: cAttack1 cAttack2*@3.2", "Cast: cast1 cast2*~@0 cast3~",
    "Damage Cast: damageCast1 damageCast2*~@0 cast3~", "Sentinel Guard: sentinalGuard1 sentinalGuard2* sentinalGuard0",
    "Instant Cast: root*@1", "Fire Rune: root*@1", "Earth Rune: root*@1", "Fire Avatar - Fireball: root*@1.8",
    "Blazing Fire: root*@3.5"],
```
   **Corrected block 2:**
```js
  monkey: { "@MikeBlink": "mikeBlink", "@MikeCircle": "mikeCircle", "@InstantCast": "instantCast", "@FireRune": "fireRune",
    "@EarthRune": "earthRune", "@FireAvatar-Fireball": "fireBall", "@BlazingFire": "blazingFire" },
```

5. **Small: the Fire Rune note for other owners.** "Six tiles" lists 7 end-of-action calls on 5 tiles: the Fireball
   cast (:26569), Fire Keep's release (:37127), Fire Avatar's cast (:38557), Earth Form's cast (:40817) and the Earth
   Form - Normal Attack tile's three attacks (:41299, :42007, :42530). Each still gets
   `[t_end, "fx", "fireRune_hit", {"p": 0.12}]`.

**Calls made here (the user is away):** one armor part on the existing `anims` option (finding 1: the Cat's option name,
no second name for the same thing); per-effect material copies (finding 2, the alphatimer pattern); the Fireball's icon
through SEQ_SKILL instead of a new alias (finding 3). Open questions 1-8 stand as the report recommends.
