# Penguin effects + sounds research: cast3, second half (cast_b)

Scope: the cast3 skills from Ice Block on: iceBlock, snowMan, tornado (tornado3), typhoon (typhoon3), absoluteZero,
blizzard, snowBall, cosmicRift (one "skills" pool member each, cue key `cast3`), and Cosmic Friday (its own sequence:
`@CosmicFriday:cast3` + `cosmicFriday`). Research only (recipe steps 1-3). Line numbers are
`C:\Users\Jump\Desktop\12tails\DecompiledSource\Penguin.cs` unless another file is named. Times are seconds from the start
of the clip the entry is keyed by. Distance 0 = at the hero. Max rank (Ice Block 2, Snow Man 2, Tornado / Typhoon 3,
Absolute Zero 2, Blizzard 2), passives on: Double Spell #431, Typhoon #344, Ice Twister #443, Revised Magic #414.
Page stats (CHA / LCK ignored): `chaAdjust(n)` = n, `getDebuff(n, ..)` = n, `lckAdjust(12)` = 12 % (worked out in
plans/fx_penguin/own_skills.md).

Read-only probes, in `checks\fx_penguin_research\cast_b\`: `probe.json` / `probe_summary.txt` (`wardrobe_fx.py penguin
--probe` on every effect here), `probe_fields.py` (the hero prefab's GameObject fields), `flow.sh` (Penguin.cs lines with
the junk predicates and lone braces dropped), `storm_sim.py` (the storms' slide), `tto_strings.py` (string literals per
TTO coroutine), `pool.py` -> `pool.json` / `pool_pretty.txt` (the entries below; it checks valid JSON, cue times in
order, kinds fx / voice / sound only). An earlier cast_b run (stopped by the usage guard before it wrote this report)
had left these probes and a draft `pool.py`. I re-traced every coroutine and re-read every cited line, and changed the
draft where it was wrong or against the decisions: typhoon's hit sparks out, the hero-skin cues out of the paste-ready
JSON, the multiCast tint out, typhoon's why rewritten.

## Read this first

1. **SEQ step-time error: Cosmic Friday's cast3 lasts 0.4 s, not the whole clip.** `"Cosmic Friday: cast1@0.7 cast2*@0
   cast3 cosmicFriday*@6"` plays cast3 to its end (1.033 s, `wardrobe/data/penguin/clips.json`). The game cuts to the
   looped cosmicFriday clip 0.4 s in: `PlayAnimation("cast3", 0)` (:39555), `Yield(2, WaitForSeconds(0.4))` (:39691),
   then case 2 `PlayAnimation("cosmicFriday", 0)` + `WrapMode.Loop` (:39203-39208). It should be **`cast3@0.4`**. The
   order is cast3 first, then the cosmicFriday loop (the channel). `cast1@0.7` is right: RPC_cast1's `Yield(2, 0.2)`
   (:20902) + `Yield(3, 0.5)` (:20907) = 0.7 to cast2. `@6` for the channel follows the page's "three hits" rule (ticks
   at 0, 2, 4 s, below).
2. **Double Spell is 12 %, not 24 %, and only Ice Block rolls it here.** RPC_cast1 rolls it as the bar completes, right
   before it starts the skill's coroutine (the same frame as cast3's 0): `hasSkill(431)`, `isDoubleSpell`, no multiCast
   status, `Random.Range(0, 100) < lckAdjust(12)` (:20108-20126), then `multiCast` at the hero (createEffect
   :20132-20138) and `RPC_AddStatus("multiCast", 1, 3, ..)` (:20144). `isDoubleSpell` is true for iceBlock (:19707) and
   false for the rest: the default (:19520) for snowMan, tornado, typhoon, absoluteZero and blizzard, set false for
   snowBall (:19814), cosmicRift (:19836) and cosmicFriday (:19858). So the other seven have no proc flash at all. Ice
   Block doesn't recast on a proc. It spends the status and places 9 blocks instead of 5 (`mBlockCount = sLv + sLv x
   multiCastLv`, :31594-31618), so the four extra blocks share the flash's roll (`"roll": "doubleSpell"`).
3. **Tornado and Typhoon are one key press.** With Typhoon #344 learned (passives on), RPC_cast1 turns "tornado" into
   RPC_typhoon_cast when an enemy on another layer is locked (:20597-20626; getTyphoonLv :11123-11126). With no lock it
   runs RPC_tornado_cast (:20648). I made them two pool members (question 1).
4. **The cast flash is the hero prefab's `castEffect` field** (field 5 = Resources `penguin/effects/castEffect`,
   `probe_fields.py`; declared :16464). It is **ready**: EffectControl life 1 + afterLife 1, one ImageEmitter, and it
   plays its own `sounds/castEffect`. All nine coroutines spawn it 0.4 s in, at `position + TransformDirection(0, 1, 1)`
   = `{"d": 1, "y": 1}` (:31589, :32252, :32788, :33340, :33802, :34380, :38210, :38725, :39198). Each skill's own
   effect comes at that same 0.4 s.
5. **Parts.**
   - Cued now, with the part still to build:
     - `iceBlock` needs Penguin_iceBlock. It has 8 field bytes and no layout, and the script is gameplay only: a
       lifetime and the slow (Penguin_iceBlock.cs:44-145).
     - `tornado3` needs Penguin_tornado (28 bytes).
     - `typhoon3` needs Penguin_typhoon (28 bytes).
     - `cosmicFriday` needs Penguin_cosmicFriday.
   - Ready now:
     - `absoluteZero` (AlphaTimer + ShatterMesh, FX/Phoenix).
     - `snowMan`, the status's snowman, probes without error: its Penguin_snowMan has no serialized fields and draws
       nothing (it turns, scales and follows the target, and destroys itself when the status ends: the cue's `rot` and
       `kill` cover that). CharacterControl.cs:38705 loads it, so the inventory doesn't list it. It is not in
       `BUILT` (`pipeline/wardrobe_fx_inventory.py`), so the parts stage registers it as a data-only part, as
       `Sheep_seal` was (verification 2026-11-10).
   - Not cued at all: the hero-skin look of Cosmic Rift / Cosmic Friday. It is a material swap with no prefab
     (question 2).
6. **The page's Cast tile cuts into cast3, but Blizzard fades** (`PlayAnimation("cast3", 0.2f)`, :34675; the other eight
   use 0). One shared step can't do both, so I left it: the cost is 0.2 s of blend.
7. **Long channels on a short clip.** Tornado and Blizzard each hold the hero in the attack state for 6 s, but play cast3
   only once (WrapMode.Once).
   - Tornado: the channel starts with the 0.4 s spawn (channelTime = now + chaAdjust(6) :32839) and ends with the
     destroy at :33046-33052.
   - Blizzard: six 1 s ticks, standby at 6.4 s (:34499).

   The page goes back to idle after cast3 and keeps the cues and effects running (the tail), so every cue below still
   fires. Only the hero's held pose differs. Nothing to change.
8. **Name collisions.**
   - `snowman1` / `snowman2` (`voices/`): BB loads `Voices/snowMan1` / `snowMan2` (:32496, :32527), but the rip has
     `snowman1.wav` / `snowman2.wav`. The names differ only in case, so BB plays them. TTO loads the lower-case spelling
     (`pseudo/Penguin.c:21195-21196`). The cues use the rip's spelling, like the Sheep's `sealofAttack1`.
   - `multiCast` is an effect and also `voices/multiCast.wav`. The cue here is the effect: Ice Block's proc says
     nothing.
   - These effect names are also `sounds/` files: `absoluteZero`, `blizzard`, `iceBlock`, `cosmicRift`,
     `cosmicRift_ring`, `cosmicFriday`, `cosmicFriday_ring`, `snowBall`. Each sound is that effect's own AudioSource, and
     no cue plays it. `sounds/snowBall` is the exception: the snowBall prefab is a StaticMesh only and doesn't use it.
   - No cue here is kind `"sound"`.
9. **Surprises and possible game findings.** None of these changes a cue. Offer them to the user for the Bible.
   - **Typhoon's launch angle.** The launch is `rotateH(5 x owner forward, (tID - 1) x 120 deg)` (Penguin_typhoon.cs:848),
     and tID is the **target's actor number** (:819-837). So the storm leaves at 0, 120 or 240 deg off the Penguin's
     facing, depending on the target's number mod 3. It then curves onto the target (force 11 - sLv, :372). This looks
     like code meant for several storms. The cue takes tID 1, straight ahead.
   - **Typhoon's HP pool.** Its HP (`talAdjust(100 x sLv)`, :11302) drains by the damage it deals (`PIDfzmxJ88 -= num`,
     Penguin_typhoon.cs:205), and it ends when the HP goes below 0 (:93). Against a 0-DEF target that is 11 hits. The
     Bible already says this.
   - **Snow Ball's shield time** is the snowman's time left, truncated to an int (`(int)getStatusTime("snowMan")`,
     :38298).
   - **Ice Block's life** is `(int)(nLife + Time.time)` (Penguin_iceBlock.cs:51). The truncation makes each block live
     between 11 and 12 s, not exactly 12.
10. **TTO1102 matches BB on every effect and voice name** in these coroutines (string literals, `tto_strings.py`):
    - `TTO1102:Penguin.<RPC_iceBlock_cast>d__208::MoveNext@0x1df2f30`
    - `<RPC_snowMan_cast>d__211@0x1e00a00`
    - `<RPC_tornado_cast>d__212@0x1e016c0`
    - `<RPC_typhoon_cast>d__218@0x1e02450`
    - `<RPC_absoluteZero_cast>d__223@0x1dc3ea0`
    - `<RPC_blizzard_cast>d__224@0x1de2440`. TTO moves Blizzard's effect and ticks into a separate
      `<RPC_blizzard_fire>d__225@0x1de2fe0`, which carries a 6.5 constant.
    - `<RPC_snowBall_cast>d__237@0x1dffd70`
    - `<RPC_cosmicRift_cast>d__238@0x1de8e40`
    - `<RPC_cosmicFriday_cast>d__239@0x1de7ce0`

    I did not reconcile TTO's waits, because not all of its 0.4 constants are printed inline. BB is the authority. No BB
    file is missing, so no TTO voice fix applies.

## Who is targeted, and where each effect appears

| Skill | Target (Bible) | Kept, at the hero | Kept, at the target point 10 m ahead / elsewhere | Left out |
|---|---|---|---|---|
| Ice Block | none (instant/self) | castEffect, multiCast (12 %) | 5 blocks (9 on a proc) on the ground 1.5 m ahead | the ice slow on enemies (no look) |
| Snow Man | enemy | castEffect | snowMan_ring, the snowman (10 s) | the hidden enemy body (nothing to hide) |
| Tornado | none locked | castEffect | tornado_ring + tornado3 4 m ahead | tornado_hit / frost on enemies it meets |
| Typhoon | locked enemy | castEffect | typhoon3 from 4 m ahead, seeking the 10 m point | tornado_hit / frost on the struck enemy |
| Absolute Zero | enemy | castEffect | absoluteZero | the ice tint on the enemy; the camera iceRamp |
| Blizzard | enemy (the storm's centre) | castEffect | blizzard (6 s) | the hits on enemies near it; the camera blur |
| Snow Ball | an enemy that is a snowman | castEffect | the snowman (to 0.4 s), snowBall_cast, snowBall, snowBall_break | the shield's burst (needs an attacker) |
| Cosmic Rift | self | castEffect, cosmicRift_ring, cosmicRift (twice) | | the hero-skin look (question 2) |
| Cosmic Friday | self + allies within 3 m | castEffect, cosmicFriday_ring, cosmicFriday | | the hero-skin look (question 2); the status on allies (none) |

Targets, from `12t_reference/penguin-skill-reference.md`:
- Ice Block instant/self (:382)
- Snow Man target/enemy (:390)
- Tornado instant/enemy (:398), and the Typhoon reroute (:403-404, :409-416)
- Absolute Zero target/enemy (:423)
- Blizzard target/all, the locked target as the storm's centre (:432-437)
- Snow Ball target/enemy (:506)
- Cosmic Rift instant/self (:511)
- Cosmic Friday instant/self, the 3 m pulse on allies (:540-546)

Effects on an enemy go to the target point 10 m ahead (plans/fx_wolf/decisions.md, plans/fx_sheep/decisions.md 2), the
same as the Sheep's divinitySpear_ring. Hit sparks on a struck enemy stay out, the same as the Sheep's divinityAxe_hit
and the Wolf's nAttack_hit.

## Per skill: the timeline

All nine run the same way. RPC_cast1's bar ends and starts `RPC_<skill>_cast` in the same frame (cast3's 0).

- **Case 0:** `actionState = "attack"`, `myCommand = <skill>`, `animation.Rewind()`, `PlayAnimation("cast3", 0)` (a
  cut; Blizzard 0.2), `WrapMode.Once`. Then the voice: `Random.Range(0, 2) == 0` plays `<skill>1`, otherwise
  `<skill>2`. Both are in `voices/`, gated by pvoice. Then `Yield(2, 0.4)`.
- **Case 2, at 0.4:** castEffect `{"d": 1, "y": 1}` and the skill's own effect.
- **Case 3, after another `Yield(3, 0.4)`:** standby at 0.8 s, unless noted.

The `if (a - b != c) continue;` lines are opaque predicates. I worked out every one on these paths, and each takes the
normal branch. For example, in iceBlock `283391 - 409596 != -126204` is true, so it goes to IL_38F, and
`250619 - 1245 != 249375` is true, so it goes to the ActionEvent.

### iceBlock (Ice Block): `$RPC_iceBlock_cast$26362`, `:31432-32090`
| t | what | source |
|---|---|---|
| 0 | Double Spell roll in RPC_cast1 (12 %): `multiCast` at the hero (ready: life 1, followPosition, RingEmitter + LineEmitter, its own `sounds/trippleCast`) | `:20108-20144` |
| 0 | cast3 cut, voice iceBlock1 / iceBlock2 | `:31779`, `:31830-31874`, `:32036-32039` |
| 0 -> 0.4 | `Yield(2, 0.4)` | `:32034` |
| 0.4 | castEffect; the multiCast level is read and the status removed; mBlockCount = 2 (4 on a proc); i = 0: the centre block, raycast down from 9 m up, 1.5 m ahead. `RPC_iceBlock_fire` places `iceBlock` with `LookRotation(hero forward)` and `Init(chaAdjust(6) + 6 = 12, sLv, ..)` | `:31589-31618`, `:31958`, `:10716-10744` |
| 0.4 -> 0.5 | `Yield(3, 0.1)` | `:32017` |
| 0.5 | i = 1: the right block, +1.5 m (`+ i x 1.5 x right`) | `:31985` |
| 0.5 -> 0.55 | `Yield(4, 0.05)` | `:32023` |
| 0.55 | case 4: the left block, -1.5 m (`- i x 1.5 x right`) | `:31668` |
| 0.55 -> 0.6 | `Yield(5, 0.05)` | `:32032` |
| 0.6 / 0.65 | i = 2: right +3 m, left -3 m (the same two waits) | as above |
| 0.7 | i = 3 >= mBlockCount + 1: standby | `:31899-31918` |
| (proc) 0.7 / 0.75, 0.8 / 0.85 | i = 3 and 4: +-4.5 m, +-6 m; standby at 0.9 | as above |

Sums, step by step: 0.4 + 0.1 = 0.5; + 0.05 = 0.55; + 0.05 = 0.6; + 0.05 = 0.65; + 0.05 = 0.7 (standby, or i = 3 on a
proc); then 0.75, 0.8, 0.85, 0.9.

- Each block plays its own `sounds/iceBlock`. It is destroyed with no fade when its life ends
  (Penguin_iceBlock.cs:116-120), 12 s after it is placed (11-12 s, Read this first 9).
- Left out: the blocks' ice slow on enemies (Penguin_iceBlock.cs:160-215), which has no look.
- Also left out: the multiCast purple tint while the status lasts (0 to 0.4 s, CharacterControl.cs:38470-38477). This
  matches Blink (own_skills question 3, default out).

### snowMan (Snow Man): `$RPC_snowMan_cast$26377`, `:32095-32630`
| t | what | source |
|---|---|---|
| 0 | cast3 cut, voice snowman1 / snowman2 | `:32445`, `:32486-32576` |
| 0 -> 0.4 | `Yield(2, 0.4)` | `:32574` |
| 0.4 | castEffect, and `snowMan_ring` on the target at its position and rotation (tChar.createEffect; ready: life 1 + 1, its own `sounds/snowMan`) | `:32252`, `:32313-32331` |
| 0.4 | status snowMan Lv 2 for getDebuff(2 + 4 x 2) = 10 s. The target's renderers are hidden and `Effects/snowMan` is placed at its feet, identity. Penguin_snowMan then turns it to the target's rotation, keeps scale 1 for a target 1 m tall or less, follows the target, and destroys itself when the target's actionState leaves "snowMan" | `:32345-32350`; CharacterControl.cs:38650-38711; Penguin_snowMan.cs:36-63, :82-129 |
| 0.4 -> 0.8 | `Yield(3, 0.4)` | `:32585` |
| 0.8 | standby | `:32377` |

The target is taken as a Penguin-sized enemy facing the hero (`rot [0, 180, 0]`). Penguin.prefab's CharacterController
is `m_Height 1`, `m_Radius 0.3` (:683-684), so the snowman keeps scale 1. The snowman ends with its status at
0.4 + 10 = 10.4 s (`kill 10`).

### tornado (Tornado, rank 3): `$RPC_tornado_cast$26391`, `:32631-33182`
| t | what | source |
|---|---|---|
| 0 | cast3 cut, voice tornado1 / tornado2 | `:32904`, `:32955-32999`, `:33126-33129` |
| 0 -> 0.4 | `Yield(2, 0.4)` | `:33122` |
| 0.4 | castEffect; the spot is `getSpawnPos(position + (1 + 3) x forward)` = 4 m ahead | `:32788`, `:32804` |
| 0.4 | `RPC_tornado_fire`: `tornado_ring` at the spot, identity (ready: life 3 + 1, LineEmitter, its own `sounds/cyclone_create`), and `tornado3` (sLv 3), identity, `Init(owner, talAdjust(30), Ice Twister on)` | `:32821`, `:10851-10869`, `:10963-10987`, `:11026-11032` |
| 0.4 | channelTime = now + chaAdjust(6) | `:32839` |
| 0.4 -> 6.4 | the channel: the hero turns to the storm every frame | `:33024-33120` |
| 6.4 | `RPC_tornado_destroy`: standby, and the storm's onDestroy (`destroy` clip, `Yield 0.4`, Destroy). Penguin_tornado also starts onDestroy itself when the owner leaves "attack" / "tornado" (Penguin_tornado.cs:199-240) | `:33046-33063`, `:11072-11106`; Penguin_tornado.cs:803-940 |
| 6.8 | the storm is gone | Penguin_tornado.cs:898, :940 |

Penguin_tornado (to build):
- `Init` sets velocity 5 x owner forward and drag 2 (Penguin_tornado.cs:98-103).
- onCreate plays `create`, then `root` looped 0.4 s later (:744-778).
- Unsteered, it slides about 2.4 m, to about 6.4 m ahead (`storm_sim.py`; with no friction, 5 / 2 = 2.5 m).
- It plays its own looping `sounds/cyclone`.

Left out: `tornado_hit` and Ice Twister's frost on enemies the storm meets (Penguin_tornado.cs:266-361). These are on an
enemy, and with no enemy locked there is no target point.

### typhoon (Typhoon: Tornado with an enemy locked, rank 3): `$RPC_typhoon_cast$26405`, `:33183-33644`
| t | what | source |
|---|---|---|
| 0 | cast3 cut, voice typhoon1 / typhoon2 | `:33466`, `:33507-33548`, `:33598-33601` |
| 0 -> 0.4 | `Yield(2, 0.4)` | `:33587` |
| 0.4 | castEffect; the spot is 4 m ahead (`getSpawnPos(.. (1 + sLv) x forward)`) | `:33340`, `:33353` |
| 0.4 | `RPC_typhoon_fire`: `typhoon3` at the spot, identity, `Init(owner, talAdjust(30), HP talAdjust(300), life chaAdjust(6) = 6, tID, Ice Twister)`. Init sets the life end to now + 6 (Penguin_typhoon.cs:772) and the launch to rotateH(5 x forward, (tID - 1) x 120) with drag 2; from then on a force of 8 pushes it at the target | `:33358`, `:11236-11311`; Penguin_typhoon.cs:757-853, :356-372 |
| 0.4 -> 0.8 | `Yield(3, 0.4)` | `:33596` |
| 0.8 | standby (the storm runs on) | `:33398` |
| 6.4 | the storm's life ends: Update starts onDestroy (`destroy` clip, `Yield 0.4`, Destroy) | Penguin_typhoon.cs:81, :270-287, :1111-1126; Penguin.cs:11360-11378 |
| 6.8 | gone | |

- `"to": [0, 0, 10]` gives the part the point it seeks.
- `cut 6.4` is the storm's life end, not an action change: the typhoon doesn't watch the hero. `kill 6.4`, counted from
  its 0.4 s spawn, ends it at 6.8.
- Its sound `sounds/cyclone` loops and fades in to 0.6 (Penguin_typhoon.cs:330, :472).
- Left out: every 0.35 s (:110-118), `tornado_hit` at each struck enemy's collider centre (:168-183,
  Penguin.cs:10789-10812) and Ice Twister's 9 % frost on that enemy (:210-238, CharacterControl.cs:38733-38757). Both
  are on the struck enemy.
- The HP pool's early end is not modelled (Read this first 9).

### absoluteZero (Absolute Zero, rank 2): `$RPC_absoluteZero_cast$26417`, `:33645-34221`
| t | what | source |
|---|---|---|
| 0 | cast3 cut, voice absoluteZero1 / absoluteZero2 | `:34019`, `:34060-34115` |
| 0 -> 0.4 | `Yield(2, 0.4)` | `:34164` |
| 0.4 | castEffect, and `absoluteZero` at the target's position, `Quaternion.identity`. It is ready now: EC life 1 + 1, followPosition; StaticMesh + AlphaTimer + ShatterMesh (Delay 0.4), LineEmitter, legacy particles, RingEmitter, VortexEmitter; its own `sounds/absoluteZero` | `:33802`, `:33838-33856` |
| 0.4 | status ice Lv 4 for getDebuff(12), on the target | `:33903` |
| 0.4 -> 0.8 | `Yield(3, 0.4)` | `:34168` |
| 0.8 | standby | `:33951` |

Identity is drawn in the hero's facing (APPROXIMATED, as for the Sheep's divinityAxe).

Left out:
- The ice status's tint of the enemy's body: it is on an enemy, and there is no body at the target point.
- The player's camera colour ramp `iceRamp` (:33919-33924): a camera effect, left out like the Wolf's.

### blizzard (Blizzard, rank 2): `$RPC_blizzard_cast$26433`, `:34222-34893`
| t | what | source |
|---|---|---|
| 0 | cast3 with a 0.2 s fade, voice blizzard1 / blizzard2 | `:34675`, `:34716-34771` |
| 0 -> 0.4 | `Yield(2, 0.4)` | `:34820` |
| 0.4 | castEffect, and the camera motion blur (player only) | `:34380`, `:34385-34396` |
| 0.4 | `blizzard` at the target's position, the hero's rotation (tChar.createEffect). Ready: EC life 6 + afterLife 1, followPosition; 3 RingEmitters / an ImageEmitter (Life 7, repeating), SnowEmitter particles; its own looping `sounds/blizzard` | `:34424-34447` |
| 0.4 | i = 0: tick 1 | `:34526-34621` |
| 0.4 ... 5.4 | six ticks 1 s apart: everyone within 6 + 3 x 2 = 12 m of the target is hit, except the target itself (no look) | `:34527`, `:34566-34605`, `:34815`, `:34467` |
| 6.4 | i = 6: standby. The blizzard ends on its own life (6 s from 0.4) and fades out over its afterLife | `:34480-34519` |

Sum: 0.4 + 6 x 1 = 6.4. The blizzard is destroyed early only when the channel is broken (:34625-34631).

Left out: the hits, which have no look of their own and land on enemies near the target, and the camera blur.

### snowBall (Snow Ball): `$RPC_snowBall_cast$26547`, `:38064-38589`
| t | what | source |
|---|---|---|
| 0 | the target must already be a snowman ("Can only cast on snowman" otherwise, :38307), so the snowman stands at the target point. This is the same idea as the Sheep's seal fields showing the seals they need | `:38287-38310` |
| 0 | cast3 cut, voice snowBall1 / snowBall2 | `:38403`, `:38444-38541` |
| 0 -> 0.4 | `Yield(2, 0.4)` | `:38535` |
| 0.4 | castEffect, and `snowBall_cast` on the target at its position and rotation (tChar.createEffect; ready: ImageEmitter, particles, EmitterControl, VortexEmitter; no sound) | `:38210`, `:38247-38265` |
| 0.4 | status snowBall at the snowman's level, for `(int)` its time left. snowMan is removed (its snowman destroys itself, Penguin_snowMan.cs:110-129), actionState becomes "snowBall", the target's renderers are hidden, and `snowBall` is placed at its feet: identity, parented, scale height + 0.2 = 1.2 | `:38287-38298`; CharacterControl.cs:38843-38916 |
| 0.4 -> 0.8 | `Yield(3, 0.4)` | `:38547` |
| 0.8 | standby | `:38335` |
| 8.4 | the status ends: snowBallFx is destroyed, and `snowBall_break` is placed at the target's feet, identity (ready: EC life 1 + 1, particles) | CharacterControl.cs:17558-17580 |

The time left is APPROXIMATED as the quickest chain, Snow Man then Snow Ball with no cast bar:
1. The snowman starts with 10 s.
2. Elapsed before Snow Ball's status: 0.4 (Snow Man's standby at 0.8, less its status at 0.4) + 0.7 (Snow Ball's cast1
   to cast2) + 0 (the bar) + 0.4 = 1.5 s.
3. Time left: 10 - 1.5 = 8.5, and `(int)` makes it 8.
4. It ends at 0.4 + 8 = 8.4 s.

Scale: `mChar.height` is 1 for a Penguin-sized target, + 0.2 = 1.2.

Left out: the shield's burst when damage breaks it, which needs an attacker.

### cosmicRift (Cosmic Rift, self): `$RPC_cosmicRift_cast$26559`, `:38590-39061`
| t | what | source |
|---|---|---|
| 0 | cast3 cut, voice cosmicRift1 / cosmicRift2 | `:38888`, `:38929-38970`, `:39016-39024` |
| 0 -> 0.4 | `Yield(2, 0.4)` | `:39022` |
| 0.4 | castEffect, and `cosmicRift_ring` at the hero (createEffect; ready: EC life 1 + 1, followState + followPosition, its own `sounds/cosmicRift_ring`) | `:38725-38748` |
| 0.4 -> 0.6 | `Yield(3, 0.2)` | `:39031` |
| 0.6 | status cosmicRift (5, chaAdjust(12) = 12 s): every Diffuse renderer of the hero gets an `FX/CosmicRift` material with its own texture, and every other renderer is hidden | `:38793`; CharacterControl.cs:38946-39006 |
| 0.6 | `cosmicRift` at the hero, identity (createEffect; ready: EC life 1 + 1, followState, its own `sounds/cosmicRift`) | CharacterControl.cs:39011-39020 |
| 0.6 -> 0.8 | `Yield(4, 0.2)` | `:39014` |
| 0.8 | standby: both followState effects get their cut | `:38820` |
| 12.6 | the status ends: the renderers go back to Diffuse and are shown, and `cosmicRift` appears at the hero again. No action change follows, so it plays its full life | CharacterControl.cs:17605-17683 |

Sums: 0.4 + 0.2 = 0.6; 0.6 + 0.2 = 0.8; 0.6 + 12 = 12.6.

### Cosmic Friday: `$RPC_cosmicFriday_cast$26566`, `:39062-39700` (its own tile)
The sequence is cast1 (0.7 s) > cast2 (the bar, 0) > cast3 (0.4 s, Read this first 1) > cosmicFriday looped (the channel,
6 s). RPC_cast1 starts it when the bar ends (:20859-20869; isDoubleSpell false, :19858).

| clip | t | what | source |
|---|---|---|---|
| cast3 | 0 | cast3 cut, voice cosmicFriday1 / cosmicFriday2 | `:39555`, `:39596-39680` |
| cast3 | 0 -> 0.4 | `Yield(2, 0.4)` | `:39691` |
| cosmicFriday | 0 (= 0.4) | castEffect, and `PlayAnimation("cosmicFriday", 0)` looped | `:39198-39208` |
| cosmicFriday | 0 | `cosmicFriday_ring` at the hero (ready: EC life 1 + 1, followState; its own `sounds/cosmicFriday_ring`) | `:39213-39231` |
| cosmicFriday | 0 | `cosmicFriday` at the hero, the hero's rotation, `InitCosmicFriday`. To build: `create` for 0.5 s, then `root` looped, following the owner every frame; its own looping `sounds/cosmicFriday` | `:39250-39279`; Penguin_cosmicFriday.cs:24-60, :283-406 |
| cosmicFriday | 0, 2, 4 | the channel, one `WaitForFixedUpdate` per frame (:39678). While she doesn't move and MP >= 25, every 2 s (mUpdateTime + 2): MP - 20 (Revised Magic #414), and status cosmicFriday (5, 3 s) on everyone of her layer within 3 m, herself included. The status gives the same FX/CosmicRift look | `:39310-39452`; CharacterControl.cs:39047-39114 |
| cosmicFriday | 6 | the page's channel end (in the game, a move or running out of MP: RPC_cosmicFriday_cancel sets standby, :11653-11683). `DestroyCosmicFriday` (`destroy` clip, `Yield 0.5`, Destroy) and standby | `:39356-39375`, `:39464-39514`; Penguin_cosmicFriday.cs:434-580 |
| cosmicFriday | 6.5 | the field is gone | |

The ring's life (1 + 1 s) ends before the 6 s cut. Her own status, refreshed at 4 s, would hold the look until 7 s.

## The cue entries (ready to paste)

The editor merges `cast3.skills` with cast_a's members: one pool, one member per play at even chance. The Cosmic Friday
entries are separate keys. Same as `checks\fx_penguin_research\cast_b\pool_pretty.txt` (valid JSON, checked by
`pool.py`).

```json
{
  "cast3": {
    "why": "(the editor's merge line: cast_a's members + these 8, one per play at even chance; Cosmic Friday has its own tile)",
    "skills": {
      "iceBlock": {
        "why": "Penguin.cs RPC_iceBlock_cast (:31432-32090; RPC_cast1 starts it when the bar ends, :20516-20522; isDoubleSpell :19707): Double Spell #431 on (passives on; one roll per play: roll doubleSpell): RPC_cast1 rolls Random.Range(0, 100) < lckAdjust(12) = 12 % as the bar completes (:20108-20126; luck ignored), a proc draws multiCast at the hero (createEffect :20132-20138; plays its own Sounds/trippleCast) and adds multiCast Lv 1 (:20144), which tints the hero (0.48, 0.29, 0.78) (CharacterControl.cs:38470-38477) until Ice Block spends it at 0.4 s (:31594-31611; the tint is left out, as Blink's: plans/fx_penguin/own_skills.md question 3); clip cast3 cut (PlayAnimation(cast3, 0) :31779) and voice iceBlock1 / iceBlock2 (Random.Range(0, 2) :31830-31874, PlayOneShot :32036-32039) at 0; Yield 0.4 (:32034): castEffect (the Penguin prefab's castEffect field = Resources penguin/effects/castEffect) 1 m ahead 1 m up (TransformDirection(0, 1, 1) :31589; plays its own Sounds/castEffect); mBlockCount = sLv + sLv x multiCastLv = 2, 4 on a proc (:31618); each block raycast down to the ground 1.5 m ahead (:31958, :31985, :31668), RPC_iceBlock_fire: iceBlock, LookRotation(hero forward) (:10716-10744; NEEDS Penguin_iceBlock), life chaAdjust(6) + 6 = 12 s (:10744, Penguin_iceBlock.cs:51; destroyed with no fade :116-120; CHA ignored): the centre at 0.4, then Yield 0.1 (:32017) and per i = 1..mBlockCount the right block +1.5 i m, Yield 0.05 (:32023), the left one -1.5 i m, Yield 0.05 (:32032): 0.5 / 0.55, 0.6 / 0.65, on a proc also 0.7 / 0.75, 0.8 / 0.85; standby when i = mBlockCount + 1 (:31899-31918): 0.7 s (0.9 on a proc); each block plays its own Sounds/iceBlock; the blocks' ice slow on enemies (Penguin_iceBlock.cs:169) draws nothing",
        "cues": [
        [0, "fx", "multiCast", {"p": 0.12, "roll": "doubleSpell"}],
        [0, "voice", "iceBlock1|iceBlock2"],
        [0.4, "fx", "castEffect", {"d": 1, "y": 1}],
        [0.4, "fx", "iceBlock", {"d": 1.5, "kill": 12}],
        [0.5, "fx", "iceBlock", {"d": 1.5, "x": 1.5, "kill": 12}],
        [0.55, "fx", "iceBlock", {"d": 1.5, "x": -1.5, "kill": 12}],
        [0.6, "fx", "iceBlock", {"d": 1.5, "x": 3.0, "kill": 12}],
        [0.65, "fx", "iceBlock", {"d": 1.5, "x": -3.0, "kill": 12}],
        [0.7, "fx", "iceBlock", {"d": 1.5, "x": 4.5, "kill": 12, "p": 0.12, "roll": "doubleSpell"}],
        [0.75, "fx", "iceBlock", {"d": 1.5, "x": -4.5, "kill": 12, "p": 0.12, "roll": "doubleSpell"}],
        [0.8, "fx", "iceBlock", {"d": 1.5, "x": 6.0, "kill": 12, "p": 0.12, "roll": "doubleSpell"}],
        [0.85, "fx", "iceBlock", {"d": 1.5, "x": -6.0, "kill": 12, "p": 0.12, "roll": "doubleSpell"}]
        ]
      },
      "snowMan": {
        "why": "Penguin.cs RPC_snowMan_cast (:32095-32630, enemy target; the target point 10 m ahead): clip cast3 cut (:32445) and voice snowman1 / snowman2 at 0 (Random.Range(0, 2) :32486; BB loads Voices/snowMan1 / snowMan2 :32496, :32527, the rip's files are voices/snowman1 / snowman2, the spelling TTO loads, pseudo/Penguin.c:21195-21196; PlayOneShot :32563, :32576); Yield 0.4 (:32574): castEffect 1 m ahead 1 m up (:32252; plays Sounds/castEffect); snowMan_ring on the target at its feet, the target's rotation (tChar.createEffect :32313-32331; plays its own Sounds/snowMan); the snowMan status, Lv 2, getDebuff(2 + 4 x 2 = 10 s, CHA vs CHA; CHA ignored) (:32345-32350): the target's renderers hidden and Effects/snowMan at its feet (CharacterControl.cs:38650-38711); Penguin_snowMan turns it to the target's rotation, keeps scale 1 for a target 1 m tall or less (Penguin_snowMan.cs:45-63), follows it and destroys itself when the status ends (:110-129; it has no fields and draws nothing); the target taken as a Penguin-sized enemy facing the hero (rot 180); Yield 0.4 (:32585): standby 0.8 s (:32377)",
        "cues": [
        [0, "voice", "snowman1|snowman2"],
        [0.4, "fx", "castEffect", {"d": 1, "y": 1}],
        [0.4, "fx", "snowMan_ring", {"d": 10, "rot": [0, 180, 0]}],
        [0.4, "fx", "snowMan", {"d": 10, "rot": [0, 180, 0], "kill": 10}]
        ]
      },
      "tornado": {
        "why": "Penguin.cs RPC_tornado_cast (:32631-33182; with Typhoon #344 learned it is cast only with no enemy locked: RPC_cast1 :20597-20648, getTyphoonLv :11123-11126): clip cast3 cut (:32904) and voice tornado1 / tornado2 (Random.Range(0, 2) :32955-32999, PlayOneShot :33126, :33129) at 0; Yield 0.4 (:33122): castEffect 1 m ahead 1 m up (:32788; plays Sounds/castEffect); the spot getSpawnPos(position + (1 + sLv) x forward) = 4 m ahead at sLv 3 (:32804); RPC_tornado_fire (:32821): tornado_ring there, identity (:10851-10869; EffectControl life 3, plays its own Sounds/cyclone_create) and tornado3 (sLv 3, :10963-10987; NEEDS Penguin_tornado: Init velocity 5 x hero forward, drag 2, Penguin_tornado.cs:98-103, unsteered it slides about 2.4 m, to 6.4 m ahead, checks/fx_penguin_research/cast_b/storm_sim.py; its own looping Sounds/cyclone), Ice Twister #443 on (:11029); channel chaAdjust(6) = 6 s (:32839): the hero holds the attack state, turning to the storm every frame (:33093-33120), and at 0.4 + 6 = 6.4 s RPC_tornado_destroy (:33046-33052): standby (:11079) and the storm's onDestroy: destroy clip, Yield 0.4, Destroy (:11106; Penguin_tornado.cs:928-940, :898): cut 6.4, gone at 6.8 (kill 6.4 after its spawn); left out: tornado_hit and Ice Twister's frost on enemies the storm meets (Penguin_tornado.cs:266-361), on an enemy with no target-point analogue (no enemy is locked, or the cast would be Typhoon)",
        "cues": [
        [0, "voice", "tornado1|tornado2"],
        [0.4, "fx", "castEffect", {"d": 1, "y": 1}],
        [0.4, "fx", "tornado_ring", {"d": 4}],
        [0.4, "fx", "tornado3", {"d": 4, "cut": 6.4, "kill": 6.4}]
        ]
      },
      "typhoon": {
        "why": "Penguin.cs RPC_typhoon_cast (:33183-33644; Tornado cast with an enemy locked and Typhoon #344 learned, passives on: RPC_cast1 :20597-20626): clip cast3 cut (:33466) and voice typhoon1 / typhoon2 (Random.Range(0, 2) :33507-33548, PlayOneShot :33598, :33601) at 0; Yield 0.4 (:33587): castEffect 1 m ahead 1 m up (:33340; plays Sounds/castEffect); getSpawnPos(position + (1 + sLv) x forward) = 4 m ahead at sLv 3 (:33353), RPC_typhoon_fire (:33358): typhoon3 there, identity (:11236-11260; NEEDS Penguin_typhoon; its own looping Sounds/cyclone, fading in to 0.6, Penguin_typhoon.cs:330, :472), Init(owner, damage, HP talAdjust(300), life chaAdjust(6) = 6, the target, Ice Twister #443) (:11299-11311): launched rotateH(5 x owner forward, (tID - 1) x 120 deg) with drag 2 (Penguin_typhoon.cs:848-853; tID is the target's actor number, APPROXIMATED as 1: straight ahead), pushed with force 11 - 3 = 8 at the target, the 10 m point: to (:356-372); its life is set at Init (:772), so at 0.4 + 6 = 6.4 s Update starts onDestroy (:81, :270-287): destroy clip, Yield 0.4, Destroy (:1111-1126; Penguin.cs:11360-11378): cut 6.4 here is that life end (the hero went to standby at 0.8 s and the typhoon does not watch her), gone at 6.8 (kill 6.4 after its spawn); its HP pool talAdjust(300), drained by the damage it deals (:205, :93), is not modelled (APPROXIMATED: it depends on the enemy's DEF; on a 0-DEF target it would end after 11 hits); Yield 0.4 (:33596): standby 0.8 s (:33398); left out: every 0.35 s (:110-118) tornado_hit at each struck enemy's collider centre (:168-183, Penguin.cs:10789-10812) and Ice Twister's 9 % frost on it (:210-238, CharacterControl.cs:38733-38757): on the struck enemy, as the Sheep's divinityAxe_hit",
        "cues": [
        [0, "voice", "typhoon1|typhoon2"],
        [0.4, "fx", "castEffect", {"d": 1, "y": 1}],
        [0.4, "fx", "typhoon3", {"d": 4, "to": [0, 0, 10], "cut": 6.4, "kill": 6.4}]
        ]
      },
      "absoluteZero": {
        "why": "Penguin.cs RPC_absoluteZero_cast (:33645-34221, enemy target; the target point 10 m ahead): clip cast3 cut (:34019) and voice absoluteZero1 / absoluteZero2 (Random.Range(0, 2) :34060-34115) at 0; Yield 0.4 (:34164): castEffect 1 m ahead 1 m up (:33802; plays Sounds/castEffect); absoluteZero at the target's feet, Quaternion.identity (:33838-33856; drawn in the hero's facing, APPROXIMATED; AlphaTimer + ShatterMesh, FX/Phoenix; plays its own Sounds/absoluteZero); Yield 0.4 (:34168): standby 0.8 s (:33951); left out: the ice status's blue tint of the target's body (Lv 4, getDebuff(12), :33903; CharacterControl.cs:38600-38610), on an enemy with no target-point analogue (no body there); the player's camera colour ramp iceRamp (:33919-33924), a camera effect as the Wolf's were",
        "cues": [
        [0, "voice", "absoluteZero1|absoluteZero2"],
        [0.4, "fx", "castEffect", {"d": 1, "y": 1}],
        [0.4, "fx", "absoluteZero", {"d": 10}]
        ]
      },
      "blizzard": {
        "why": "Penguin.cs RPC_blizzard_cast (:34222-34893, enemy target; the target point 10 m ahead): clip cast3 with a 0.2 s fade (PlayAnimation(cast3, 0.2) :34675; the Cast tile's step is a cut) and voice blizzard1 / blizzard2 (Random.Range(0, 2) :34716-34771) at 0; Yield 0.4 (:34820): castEffect 1 m ahead 1 m up (:34380; plays Sounds/castEffect); blizzard on the target at its feet, the hero's rotation (tChar.createEffect :34424-34442; EffectControl life 6 + afterLife 1, followPosition, its own looping Sounds/blizzard); six 1 s ticks (i < 6 :34527, Yield 1 :34815, i++ :34467) at 0.4 ... 5.4 s hit every enemy within 12 m but the target (:34566-34605); at i = 6, 0.4 + 6 x 1 = 6.4 s: standby (:34499), the blizzard left to end on its own 6 s life (it is destroyed only when the channel is cut short, :34625-34631); left out: the hits (no visual of their own), on enemies near the target with no target-point analogue; the player's camera motion blur (:34385-34396), a camera effect as the Wolf's were",
        "cues": [
        [0, "voice", "blizzard1|blizzard2"],
        [0.4, "fx", "castEffect", {"d": 1, "y": 1}],
        [0.4, "fx", "blizzard", {"d": 10}]
        ]
      },
      "snowBall": {
        "why": "Penguin.cs RPC_snowBall_cast (:38064-38589, an enemy target that must be a snowman: 'Can only cast on snowman' :38307; the target point 10 m ahead): the snowman a Snow Man left there stands at 0 (as the Sheep's seal fields show the seals they need) and goes when the snowBall status removes snowMan at 0.4 s (CharacterControl.cs:38847; Penguin_snowMan.cs:110-129); clip cast3 cut (:38403) and voice snowBall1 / snowBall2 (Random.Range(0, 2) :38444-38485, PlayOneShot :38523, :38541) at 0; Yield 0.4 (:38535): castEffect 1 m ahead 1 m up (:38210; plays Sounds/castEffect); snowBall_cast on the target at its feet, its rotation (tChar.createEffect :38247-38265; no sound); the snowBall status with the snowman's level and time left (:38287-38298; getStatusTime = the time left, CharacterControl.cs:19278): the snowman's 10 s less the 1.5 s from its status (Snow Man's 0.4 s) to this one (Snow Man's standby 0.8 s + Snow Ball's cast1 0.7 s + 0.4 s) = 8.5, cut to 8 by the int; snowBall at the target's feet, identity, parented, scale height + 0.2 = 1.2 for a Penguin-sized target (CharacterControl.cs:38886-38916; StaticMesh); the status ends at 0.4 + 8 = 8.4 s: snowBallFx destroyed and snowBall_break at the target's feet, identity (CharacterControl.cs:17558-17580); Yield 0.4 (:38547): standby 0.8 s (:38335); left out: the shield's burst when damage breaks it, needs an attacker",
        "cues": [
        [0, "fx", "snowMan", {"d": 10, "rot": [0, 180, 0], "kill": 0.4}],
        [0, "voice", "snowBall1|snowBall2"],
        [0.4, "fx", "castEffect", {"d": 1, "y": 1}],
        [0.4, "fx", "snowBall_cast", {"d": 10, "rot": [0, 180, 0]}],
        [0.4, "fx", "snowBall", {"d": 10, "scale": 1.2, "kill": 8}],
        [8.4, "fx", "snowBall_break", {"d": 10}]
        ]
      },
      "cosmicRift": {
        "why": "Penguin.cs RPC_cosmicRift_cast (:38590-39061, a self-buff): clip cast3 cut (:38888) and voice cosmicRift1 / cosmicRift2 (Random.Range(0, 2) :38929-38970, PlayOneShot :39016, :39024) at 0; Yield 0.4 (:39022): castEffect 1 m ahead 1 m up (:38725; plays Sounds/castEffect) and cosmicRift_ring at the hero (createEffect :38730-38748; followState: cut at the 0.8 s standby; plays its own Sounds/cosmicRift_ring); Yield 0.2 (:39031): at 0.6 s RPC_AddStatus(cosmicRift, 5, chaAdjust(12) = 12 s; CHA ignored) (:38793): every Diffuse renderer of the hero gets FX/CosmicRift with its own texture, every other renderer hidden (CharacterControl.cs:38952-39006; NOT cued: a hero material swap, no effect prefab; plans/fx_penguin/cast_b.md question 2), and cosmicRift at the hero, identity (:39011-39020; followState: cut at 0.8; plays its own Sounds/cosmicRift); Yield 0.2 (:39014): standby 0.8 s (:38820); the status ends at 0.6 + 12 = 12.6 s: the hero's renderers back to Diffuse (colour 0.86) and shown (CharacterControl.cs:17605-17671) and cosmicRift again at the hero (:17676-17683)",
        "cues": [
        [0, "voice", "cosmicRift1|cosmicRift2"],
        [0.4, "fx", "castEffect", {"d": 1, "y": 1}],
        [0.4, "fx", "cosmicRift_ring", {"cut": 0.8}],
        [0.6, "fx", "cosmicRift", {"cut": 0.8}],
        [12.6, "fx", "cosmicRift"]
        ]
      }
    }
  },
  "@CosmicFriday:cast3": {
    "why": "Penguin.cs RPC_cosmicFriday_cast (:39062-39700; RPC_cast1 starts it when the bar ends, :20859-20869): clip cast3 cut (PlayAnimation(cast3, 0) :39555) and voice cosmicFriday1 / cosmicFriday2 (Random.Range(0, 2) :39596-39637, PlayOneShot :39673, :39680) at 0; Yield 0.4 (:39691): the cosmicFriday clip cuts in (:39203), its entry has the rest",
    "cues": [
    [0, "voice", "cosmicFriday1|cosmicFriday2"]
    ]
  },
  "cosmicFriday": {
    "why": "Penguin.cs RPC_cosmicFriday_cast case 2, 0.4 s into cast3 (Yield 0.4 :39691), times from this clip: PlayAnimation(cosmicFriday, 0) looped (:39203-39208); castEffect 1 m ahead 1 m up (:39198; plays Sounds/castEffect); cosmicFriday_ring at the hero (createEffect :39213-39231; followState, ends on its life 1 + 1 s first; plays its own Sounds/cosmicFriday_ring); cosmicFriday at the hero, InitCosmicFriday (:39250-39279; NEEDS Penguin_cosmicFriday: create clip, Yield 0.5, root looped, following the hero, Penguin_cosmicFriday.cs:60, :330-406; its own looping Sounds/cosmicFriday); the channel (Yield WaitForFixedUpdate :39678) runs until the player moves or MP < 25 (:39341-39381), the tile's 6 s: three ticks at 0, 2, 4 s (mUpdateTime + 2 :39387-39395; MP 20 with Revised Magic #414 :39400) each put cosmicFriday (5, 3 s) on everyone of her layer within 3 m, herself included (FindAreaTarget(her position, 3, 3, 1 << her layer) :39405-39449, no self-exclusion), whose look is Cosmic Rift's FX/CosmicRift skin (CharacterControl.cs:39047-39114; NOT cued: a hero material swap, question 2), refreshed until 4 + 3 = 7 s; at 6 s the channel ends: DestroyCosmicFriday (:39464-39470: destroy clip, Yield 0.5, Destroy, Penguin_cosmicFriday.cs:529-580; cut 6, gone at 6.5) and standby (:39494); left out: the cosmicFriday status on allies (no allies)",
    "cues": [
    [0, "fx", "castEffect", {"d": 1, "y": 1}],
    [0, "fx", "cosmicFriday_ring"],
    [0, "fx", "cosmicFriday", {"cut": 6, "kill": 6.5}]
    ]
  }
}
```

## Hero-skin cues, for when that part exists (not in the JSON above)

These need a new cue kind (say `"skin"`) and a page part: swap every Diffuse renderer of the hero to an `FX/CosmicRift`
material with its own texture, hide every other renderer, and restore them on `kill` (CharacterControl.cs:38946-39006,
:39047-39114, :17605-17671). Today the page would treat an unknown kind as a sound: `fxDue` plays every non-"fx" cue
through `Sound.play` (`wardrobe/index.html`, `fxDue`). That is why these stay out of the paste-ready JSON.
- Cosmic Rift (`cast3` -> `cosmicRift`): `[0.6, "skin", "FX/CosmicRift", {"kill": 12}]` (0.6 to 12.6 s).
- Cosmic Friday (`cosmicFriday`): `[0, "skin", "FX/CosmicRift", {"kill": 7}]` (the pulse at 0 s puts it on her, and
  the last pulse at 4 s holds it to 7 s).

## Left out, and why

On an enemy with no target-point analogue, or needing an attacker:
- Snow Man / Snow Ball: the hidden enemy body (there is no body to hide).
- Absolute Zero: the ice tint on the enemy's body.
- Blizzard: the six ticks' hits on enemies near the target (no look of their own).
- Tornado: `tornado_hit` and frost on enemies it meets (no enemy is locked, so no target point).
- Typhoon: `tornado_hit` and frost on the struck enemy, the same as the Sheep's divinityAxe_hit.
- Snow Ball: the shield's burst when damage breaks it (needs an attacker).

Camera effects, as the Wolf's: Absolute Zero's `iceRamp` and Blizzard's motion blur.

Not an effect prefab:
- The multiCast purple tint (own_skills question 3).
- The FX/CosmicRift hero skin (question 2).

## New questions (only what the Sheep / Wolf decisions don't answer)

1. **Tornado and Typhoon: two pool members, or Typhoon only?** In the game, one press gives Typhoon when an enemy is
   locked (Typhoon #344, a passive, is on), and Tornado otherwise (Read this first 3). "Passives on" plus the 10 m target
   point would make every play a Typhoon. **Recommended: two members**, as the Sheep's Seal of Attack / Defense: both are
   what a max-rank Penguin casts.
2. **Build the hero-skin look (a `"skin"` cue kind and an FX/CosmicRift material part) for Cosmic Rift and Cosmic
   Friday?** It is the main thing these two skills show on the hero. Without it, Cosmic Rift is two ring flashes, and
   Cosmic Friday is its field. The decisions cover missing effect parts, not a hero material swap, and own_skills left
   the multiCast tint out on the same grounds. **Recommended: yes for these two**, with the lines in "Hero-skin cues"
   above; keep the multiCast tint out.

## Verification (2026-11-10)

A skeptical re-trace on the office PC (Penguin.cs = `C:\Users\Jump\Desktop\12tails\DecompiledSource\Penguin.cs`).
Probe outputs: `checks/fx_penguin_research/verify/`.

What was checked, independently (and found right):
- **The SEQ error (Read this first 1) is real.** In `RPC_cosmicFriday_cast`:
  - `PlayAnimation("cast3", 0)` :39555, `Yield(2, 0.4)` :39691.
  - Case 2: castEffect :39198, `PlayAnimation("cosmicFriday", 0)` + `WrapMode.Loop` :39203-39208.
  - cast3's clip is 1.0333 s (`clips.json`), and the SEQ step `cast3` (index.html:1028) has no `@`, so it plays to 1.03.
    **`cast3@0.4` is right.**
  - `cast1@0.7` = 0.2 (:20902) + 0.5 (:20907), and cast1's clip is 0.7 s.
  - The `@CosmicFriday:cast3` key is the form `fxStart` looks up (index.html:1074, :3476).
- **Double Spell:** the roll at :20108-20144 is 12 %. isDoubleSpell is true only for iceBlock :19707 here; it is false
  by default (:19520) for snowMan, tornado, typhoon, absoluteZero and blizzard, and set false at :19814, :19836, :19858.
- **Ice Block:** a proc gives no recast. `mBlockCount = sLv + sLv x multiCastLv` (2 -> 4), and the loop runs i = 0 ..
  mBlockCount, so there are 1 + 2 x 2 = 5 blocks, or 9 on a proc.
  - Each block is placed by a raycast down from 9 m, 1.5 m ahead, +- i x 1.5 x right, the right one first (the case-3
    path), then the left (case 4).
  - Waits: 0.4 :32034, 0.1 :32017, 0.05 :32023, 0.05 :32032, so the blocks land at 0.4, 0.5, 0.55, 0.6, 0.65, and
    standby is at 0.7.
  - Life: `Init(chaAdjust(6) + 6)`, with `mLife = (int)(nLife + Time.time)` (Penguin_iceBlock.cs:51).
- **Snow Man:** snowMan_ring via tChar.createEffect at the target :32331. The status lasts getDebuff(2 + 4 sLv) = 10 s
  :32345. Waits 0.4 :32574 and 0.4 :32585. The BB voices are `snowMan1/2` :32496/:32527; the rip's files are
  `snowman1/2.wav`, and TTO's pseudo :21195-21196 uses the lower case.
- **Tornado:**
  - The reroute is at :20591-20626 (an enemy on another layer + getTyphoonLv). The spot is getSpawnPos(1 + sLv
    forward) :32804.
  - RPC_tornado_fire: tornado_ring + tornado3 (sLv == 3) :10857-10987.
  - channelTime = now + chaAdjust(6) :32839; RPC_tornado_destroy runs at the channel end :33046.
  - Penguin_tornado: velocity 5 x forward, drag 2 (:98-103). WASD steering applies only with input (:463-472); the 30 m
    leash pulls back only beyond 30 m (raw :523-531, `<= 900 -> break`), so "unsteered" holds.
- **Typhoon:**
  - The launch is `rotateH(5 forward, (nID - 1) x 120)`; nID is the tID passed in, the target's actor number
    (Penguin_typhoon.cs:757-853).
  - The force is 11 - mLv toward the target (:350-372).
  - Init: talAdjust(sLv x 10) damage, talAdjust(sLv x 100) HP, chaAdjust(6) life (Penguin.cs:11299-11311).
  - Only typhoon3 is spawned: no ring (`VNrw0Yg6aF` = tornado_ring is used only by RPC_tornado_fire).
- **Absolute Zero:** Instantiate at the target's position, identity, :33856. Ice Lv sLv x 2 = 4, getDebuff(12) :33903.
  Waits 0.4 / 0.4.
- **Blizzard:** cast3 with a 0.2 fade :34675. The effect via tChar.createEffect at the target, with the hero's rotation
  :34442. `i < 6` ticks with `Yield(3, 1)` :34815, so standby comes at 0.4 + 6 = 6.4.
- **Snow Ball:** `(int)getStatusTime("snowMan")` :38298, and getStatusTime returns `sTime - Time.time`
  (CharacterControl.cs:19278).
  - The status removes snowMan and sets actionState "snowBall" (CharacterControl.cs:38847-38850).
  - The `snowBall` effect: identity, parented, scale `mChar.height + 0.2`, where mChar is the CharacterController
    (CharacterControl.cs:29789) and m_Height is 1 (Penguin.prefab:683).
- **Cosmic Rift:** waits 0.4 :39022, 0.2 :39031, 0.2 :39014. The status is set at :38793. The `cosmicRift` effect via
  createEffect at the hero, identity (CharacterControl.cs:39011-39020), and again at the status end (:17676).
- **Cosmic Friday's status:** the apply (CharacterControl.cs:39047-39114) and the end (:17707) load no effect prefab, so
  only the material swap is missed (question 2).
- **Names:** every voice, effect and sound named exists in the rip (case-insensitively for snowman). No coroutine in
  scope loads a `Sounds/` file of its own except iceBreak (on enemies, left out).
- **Targets** (PenguinSkill.cs):
  - iceBlock: instant/self.
  - snowMan, absoluteZero, snowBall: target/enemy.
  - tornado: instant/enemy.
  - blizzard: target/all.
  - cosmicRift, cosmicFriday: instant/self.
- **TTO:** `<RPC_iceBlock_cast>d__208@0x1df2f30` and `<RPC_cosmicFriday_cast>d__239@0x1de7ce0` are confirmed, and so is
  `<RPC_blizzard_fire>d__225` with `+ 6.5` (pseudo :4400-4725), all in
  `C:\Users\Jump\Desktop\12tails\DecompiledSource_TTO_2026-11-02\pseudo\Penguin.c`. The cosmicFriday prefab exists in
  TTO's bundles (`wardrobe_fx_tto.py penguin --probe`, `verify/tto_probe_cast.json`).

Corrections (old -> new):
1. Read this first 5, "Ready now: snowMan". **Old:** ready, with its Penguin_snowMan "has no fields and draws nothing".
   **New:** that is true, but Penguin_snowMan is not in `BUILT` (pipeline/wardrobe_fx_inventory.py:22-29). By the
   recipe it is a part to register, as a data-only part like `Sheep_seal`. Nothing to draw: the cue's `rot` / `kill`
   cover its turn, follow and end (Penguin_snowMan.cs:36-63 sets the rotation and the scale from the target's collider
   height).

No timing, name, distance or target error was found. The SEQ fix `cast3@0.4` stands.

Unresolved (not disproved, not fixed):
- **Rotation convention.** For effects drawn with the target's rotation (snowMan_ring, snowBall_cast, snowMan) this
  report uses `rot [0, 180, 0]` (the target facing the hero). cast_a.md draws Mana Burn's manaSurge, also in the target's
  rotation (:24770), in the hero's facing. One convention for both.
- **TTO's waits** were not reconciled (as the report says).
- **Blizzard's tick victims.** "Every enemy within 12 m but the target" is not confirmed: the `hitObject != tObject`
  branch at :34590 sits behind opaque predicates I did not resolve. No cue depends on it (the hits are left out).
