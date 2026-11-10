# Penguin effects + sounds research: Blink, Parallel Shift, Falling Stars, Nova Flare, Arctic Emperor, Focus Intellect

Scope: clips `blink`, `cast4`, `arcticEmperor`, `focusIntellect`. Research only (recipe steps 1-3). All line numbers are
`C:\Users\Jump\Desktop\12tails\DecompiledSource\Penguin.cs` unless named. Times are seconds from the start of the
clip the cue is keyed by. Distance 0 = at the hero. Prefab facts come from the read-only probe (`wardrobe_fx.py penguin
--probe ...`, plus `checks\fx_penguin_research\own_skills\probe_extra.py` for the two prefabs the stock probe can't
read; output and a summariser in that folder). The decompile's `if (a - b != c) continue;` lines are opaque predicates:
I worked out every one on the paths below, and each goes the normal way. `lckAdjust(12)` at the page's stats (LCK 1, as
the Wolf's Double Art 24 % and the Sheep's Free Cast 24 %): X = 12 x 1.01 = 12.12; 100 x 12.12 / (12.12 - 12 + 100) =
1212 / 100.12 = 12.1 -> floor = **12 %** (formula: `12t_reference/12Tails-Mechanics-Reference.md` §2.4,
CharacterControl.cs:20658).

## Read this first

1. **Blocker (build tool): `novaFlare` isn't in the Penguin's folder.** Nova Flare's blast is the Mana Vortex's prefab
   field (`public GameObject novaFlare`, ManaVortex.cs:540), Resources path
   `gameassets/characters/elementals/manavortex/effects/novaFlare`. `wardrobe_fx.py`'s `effect()` only looks in
   `gameassets/characters/heroes/<cls>/effects/` (`pipeline/wardrobe_fx.py:214`), so the build will fail on this cue.
   With the path patched in memory (my probe script), it builds with no error: every part is one the page has
   (EffectControl life 4, afterLife 0, no follow; LineEmitter, 5 RingEmitters, legacy particles, EmitterControl;
   plays its own sound `novarFlare`, the game's spelling). So it needs a tool fix (a fallback folder), not a page part.
2. **Blocker (part): `arcticEmperor` needs Penguin_arcticEmperor**, as the inventory says. It is an alpha / emission
   fade script (Penguin_arcticEmperor.cs:74-200, no gameplay). `wardrobe_fx.py` also needs a LAYOUTS entry for it: 8
   floats in this order, MinAlpha, MaxAlpha, MinEmission, MaxEmission, FadeDelay, FadeEaseIn, FadeMiddle, FadeEaseOut
   (Penguin_arcticEmperor.cs:225-246). With that layout in memory the decode uses exactly its 32 bytes (the self-check
   passes): 0, 0.25, 0, 0.035, 0, 0.3, 7.7, 1.0. The rest of the prefab is ready: EffectControl life 9, afterLife 2,
   no follow; StaticMesh, ShatterMesh, RingEmitter, VortexEmitter, legacy particles; its own `Sounds/arcticEmperor`.
   Fade-in 0.3 + middle 7.7 + fade-out 1.0 = 9.0 s, the same as its life.
3. **Two shared clips, so two "skills" pools** (the shared-clip rule): `blink` = Blink and Parallel Shift
   (`PlayAnimation("blink", 0)` :23016, :36836); `cast4` = Falling Stars and Nova Flare (:25342, :27619). Nothing else
   plays these clips (grep of `PlayAnimation(` in Penguin*.cs and CharacterControl.cs; `clip_calls.js` agrees).
4. **SEQ: nothing to fix.** The `penguin:` SEQ line has no entry for these six skills, and none is needed: all six are
   instant (no cast bar, no channel) and play one clip. Every clip is longer than the skill's time to standby (blink
   0.83 s vs 0.6 s; cast4 0.8 s vs 0.6 / 0.4 s; arcticEmperor 1.2 s vs 1.0 s; focusIntellect 1.0 s vs 1.0 s). One small
   difference: all six cut in (`PlayAnimation(x, 0)`), but the page fades a single tile in over 0.2 s
   (`index.html` `play()`, `startStep(0, steps[0].cut ? 0 : 0.2)`). Every class's single tiles do this, so I left it.
   A one-step "!" sequence like the Sheep's Seal would cut in, if the user wants it.
5. **Double Spell #431 (a passive, so ON) repeats the skill.** It rolls 12 % at the start of Blink (:23163-23193) and
   Falling Stars (:25494-25535). On a proc it draws `multiCast` and gives the `multiCast` status, and the skill runs
   **again** from its multiCast check: Blink at 0.4 s, Falling Stars at 0.6 s (`RPC_blink_multiCast` :10312-10315,
   `RPC_fallingStars_multiCast` :10354-10357). The rerun restarts the clip (`animation.Rewind()` + `PlayAnimation`).
   The page can't restart a clip from a cue. In the entries below, the rerun's effects and voice ride the same roll
   ("doubleSpell"), but the clip doesn't restart (question 1). In BB the rerun rolls again, so procs can chain; TTO
   skips the roll on a rerun (`isRepeat`, TTO1102:Penguin.<RPC_blink>d__180::MoveNext@0x1dc72c0, pseudo/Penguin.c:3931;
   <RPC_fallingStars>d__187::MoveNext@0x1ded300, :10634). One rerun is cued; a second would be 1.4 % (0.12 x 0.12).
   Parallel Shift has a multiCast check (:36704) but no Double Spell roll, so only the actives Double Cast / Triple Cast
   (not passives) repeat it. No repeat is cued there.
6. **The hero warps, the wardrobe hero doesn't.** Blink moves her 3 x 2 + 2 = 8 m (:22759) and Parallel Shift 10 m
   (:36523), both at 0.3 s. On top of that she walks at moveSpeed 3 from 0.1 to 0.4 s (:22665 / :22866, :36297 /
   :36691). The arrival effect (`blink`, `parallelShift`) goes at the hero, 0 m. This follows the Wolf's Feral Assault
   ("0 m: the wardrobe hero doesn't travel", wolf.json).
7. **Nova Flare does nothing without a Mana Vortex.** If the Penguin has none (`LxAw60aoWG`, set by Mana Vortex
   :10431), the coroutine shows "Cannot use manaPool: no manaVortex in place" and ends: no clip, no voice, no cooldown
   (:27591, :27740-27747). With one, the hero side is only clip + voice. The blast is spawned by the vortex, where the
   vortex is (ManaVortex.cs:773). On the page I put it 5 m ahead, where Mana Vortex places it (`getSpawnVector(pos + 2
   up, 5 forward - 2 up)`, :27133); question 2.
8. **Possible game bugs / Bible differences** (to offer the user for the Bible; none of them changes a cue):
   - Nova Flare's cooldown key is `"novaFLare"` (:27607), but its skill cType is `"novaFlare"` (PenguinSkill.cs:535),
     and `isTimeOut` compares with a case-sensitive `==` (CharacterControl.cs:20031). If the gate reads the cType (the
     Bible: GameGui.cs:37596), BB's Nova Flare cooldown never blocks a cast. I checked only these lines.
   - The Bible's "whiff case: still goes on CD" doesn't match this coroutine: the cooldown is set only inside the
     vortex branch (:27591-27607). The SP spent by the dispatcher is another matter, which I didn't check.
   - The Bible says Nova Flare "destroys the vortex and refunds the vortex's stored MP". The refund (and its
     `manaPool_hit` on the Penguin) comes only from `ManaVortex.RPC_dead` (:1318-1330). Nova Flare marks the vortex
     `dead` at once (ManaVortex.cs:742-745), then 1 s later deals the hits and calls `Destroy` (:712). The HP-0 check
     that would start RPC_dead skips a dead vortex (:399), and so does the lifetime tick (:310). So Nova Flare gives no
     refund, and there's no `manaPool_hit` to cue. Sure: medium-high.
9. **Name collisions: none exact.** Voices (voices/): `blink1-2`, `parallelShift1-2`, `multiCast`, `fallingStar1-2`,
   `novaFlare1-2`, `arcticEmperor1-2`, `focusIntellect1-2`. The effects' own sounds (sounds/): `blink`, `parallelShift`,
   `trippleCast` (multiCast's), `fallingStar_ring`, `fallingStar_hit` (giantStar's), `novarFlare`, `arcticEmperor`,
   `focusIntellect_ring`, `focusIntellect`. Watch-outs: `multiCast` is an effect and a voice (different kinds, both
   used below), and voices/ also has `multiCast1-3` (Double / Triple Cast's lines, not these). No cue here is
   `"sound"`: every sound in scope belongs to an effect.
10. **A 12 s voice timer.** Falling Stars and Parallel Shift say `multiCast` instead of their own line when they are
    recast within 12 s (`p0ULydF8cA` :25383-25389 / :25463-25481; `abSUOYOYsq` :36909-36913 / :36984-37038). Their
    cooldowns (agiAdjust(30) x 0.88 = 26.4 s) are longer, so a fresh cast always says its own line. Only a Double Spell
    rerun says `multiCast` (Falling Stars at 0.6 s, below). Blink has no such timer: its rerun says blink1 / blink2.
11. **TTO1102 matches BB** on every effect and voice name and on the clip for all six (string literals in
    <RPC_blink>d__180@0x1dc72c0, <RPC_parallelShift>d__232@0x1dfe4b0, <RPC_fallingStars>d__187@0x1ded300,
    <RPC_giantStars_fire>d__234@0x1df2a50, <RPC_novaFlare>d__195@0x1dfdc90, <RPC_arcticEmperor>d__228@0x1dc4de0,
    <RPC_focusIntellect>d__231@0x1deecf0). BB asks for no missing file, so no TTO voice fix applies.

---

## blink (Blink, Parallel Shift): one pool

### Blink

- Coroutine `RPC_blink` (`$RPC_blink$26122` :22507-23236, MoveNext :22632-23236). Max rank sLv 2 (pgn_blink2, #224).

| t (s) | state | what | source |
|---|---|---|---|
| 0 | 0 | `actionState attack`, cooldown `blink` agiAdjust(12); clip `blink` (cut, Once) | `:22995-23019` |
| 0 | 0 | `blink_ring` Instantiated at the hero (position, rotation) | `:23034-23046` |
| 0 | 0 | voice `blink1` or `blink2` (`Random.Range(0, 2)`, pvoice-gated) | `:23060-23144` |
| 0 | 0 | Double Spell #431: no `multiCast` and `Random.Range(0, 100) < lckAdjust(12)` (12 %) → `multiCast` createEffect at the hero, status multiCast Lv 1 for 3 s | `:23157-23193` |
| 0 → 0.1 | | `Yield(2, 0.1)` | `:23233` |
| 0.1 | 2 | moveSpeed 3, `removeLockStatus(4)` | `:22665-22670` |
| 0.1 → 0.3 | | `Yield(3, 0.2)` (via `Block_92`) | `:22671-22673`, `:23229` |
| 0.3 | 3 | collisions ignored in a 3/3/6/2 box, `Move(8 m forward)`, collisions back; `blink` Instantiated where she lands | `:22697-22829` |
| 0.3 → 0.4 | | `Yield(4, 0.1)` (via `IL_AB8` → `IL_D58`) | `:22834`, `:23220-23227` |
| 0.4 | 4 | moveSpeed 0; with multiCast: `reduceStatusLv` (Lv 1 → 0, status removed), `RPC_blink_multiCast` = this coroutine again from its state 0, and this one ends (`IL_73A` → `return false`) | `:22866-22922`, `:23216-23217`, `:10312-10315` |
| 0.4 → 0.6 | | else `Yield(5, 0.2)` | `:23219` |
| 0.6 | 5 | `standby`, myCommand none | `:22926-22953` |

- Sums: 0.1 + 0.2 = 0.3; + 0.1 = 0.4; + 0.2 = 0.6. With a rerun: its state 0 at 0.4, its warp at 0.4 + 0.3 = 0.7, its
  standby at 0.4 + 0.6 = 1.0.
- Effects (probe):
  - `blink_ring`: **ready**. EffectControl life 1, afterLife 1, no follow; 2 ImageEmitters; plays its own
    `sounds/blink` (once).
  - `blink`: **ready**. EffectControl life 1, afterLife 0; 2 ImageEmitters; no sound.
  - `multiCast`: **ready**. EffectControl life 1, afterLife 0, followPosition; RingEmitter, LineEmitter; plays its own
    `sounds/trippleCast`. It is the Penguin's field `sMRLT35VVC` (:16476), loaded from `Effects/multiCast` by
    `RPC_multiCast` (:9832-9838). Blink only uses the field if it is already loaded (`if (sMRLT35VVC)` :23181). On a
    fresh login without a Double / Triple Cast cast first, the proc gives the status but draws nothing. That's a BB
    quirk; I cue the flash, as the passives-on rule intends.
- Left out: the purple tint while the status lasts (question 3), and the camera does nothing here.

### Parallel Shift

- Coroutine `RPC_parallelShift` (`$RPC_parallelShift$26489` :36150-37069, MoveNext from :36265). One rank (#422).

| t (s) | state | what | source |
|---|---|---|---|
| 0 | 0 | `actionState attack`, cooldown `blink` agiAdjust(30); clip `blink` (cut, Once) | `:36815-36839` |
| 0 | 0 | `parallelShift_ring` Instantiated at the cast position `mPos`, hero rotation | `:36848-36866` |
| 0 | 0 | voice `parallelShift1` / `parallelShift2` (`Random.Range(0, 2)`), or `multiCast` within 12 s of the last one (not on a fresh cast, Read this first 10) | `:36880-37045` |
| 0 → 0.1 | | `Yield(2, 0.1)` | `:37052` |
| 0.1 | 2 | moveSpeed 3, `removeLockStatus(5)` | `:36297-36302` |
| 0.1 → 0.3 | | `Yield(3, 0.2)` | `:36307`, `:37026` |
| 0.3 | 3 | everyone of her own layer within 6 m (her included, `FindAreaTarget(mPos, 6, 3)` :36344): lock 5 removed; each one's own client moves them 10 m along her facing (`Move(10 x tDir)` :36523); `blink` at each **other** player, before and after the move (`hitObject != self`, :36411-36435, :36586-36610); then `parallelShift` Instantiated at the hero (where she lands) | `:36329-36654` |
| 0.3 → 0.4 | | `Yield(4, 0.1)` | `:36659`, `:37063-37065`, `:37028` |
| 0.4 | 4 | moveSpeed 0; a multiCast check (Double / Triple Cast only) | `:36691-36742` |
| 0.4 → 0.6 | | `Yield(5, 0.2)` | `:37056` |
| 0.6 | 5 | `standby` | `:36746-36773` |

- Sums: 0.1 + 0.2 = 0.3; + 0.1 = 0.4; + 0.2 = 0.6.
- Effects (probe): `parallelShift_ring` **ready** (life 1, afterLife 1; 3 ImageEmitters; plays its own
  `sounds/parallelShift`); `parallelShift` **ready** (life 1; 3 ImageEmitters; no sound).
- Left out: the `blink` flashes on the **other** players warped with her. The code skips the caster herself
  (:36388, :36411, :36586), so a self-cast (Sheep decision 1) gives her `parallelShift` and no `blink`. Same reading as
  the Sheep's All Feather ("the wings on the other allies have no ally to sit on"). This isn't one of the two reasons
  the brief allows, so the editor should know.

### The entry

```json
  "blink": {
    "why": "Penguin.cs: Blink (RPC_blink :22507-23236) and Parallel Shift (RPC_parallelShift :36150-37069) both play the blink clip, cut in (PlayAnimation(\"blink\", 0) :23016, :36836); one skill per play",
    "skills": {
      "blink": {
        "why": "Penguin.cs RPC_blink at max rank (sLv 2): clip (cut, :23016), blink_ring Instantiated at the hero (:23046; EffectControl life 1 + afterLife 1, plays its own Sounds/blink) and voice blink1 / blink2 (Random.Range(0, 2), :23089-23144) at 0; Double Spell #431 on (passives on): Random.Range(0, 100) < lckAdjust(12) = 12 % (:23163-23175) draws multiCast at the hero (createEffect :23187; plays its own Sounds/trippleCast) and gives multiCast Lv 1 for 3 s (:23193); Yield 0.1 (:23233): moveSpeed 3 (:22665); Yield 0.2 (:23229): at 0.3 s the warp, Move(3 x 2 + 2 = 8 m forward) (:22759), and blink Instantiated where she lands (:22829; 0 m: the wardrobe hero doesn't travel, as Feral Assault's); Yield 0.1 (:23227): at 0.4 s, with the rolled multiCast, the status is spent and RPC_blink_multiCast reruns the skill (:22884-22904, :10312-10315): its blink_ring and voice at 0.4, its blink at 0.4 + 0.3 = 0.7, on the same roll (the clip's restart at 0.4, :23013-23016, isn't played on the page; the rerun's own roll isn't chained, as TTO1102 <RPC_blink>d__180::MoveNext@0x1dc72c0 skips it, pseudo/Penguin.c:3931); else Yield 0.2 (:23219): standby at 0.6 s (:22943)",
        "cues": [
        [0, "fx", "blink_ring"],
        [0, "voice", "blink1|blink2"],
        [0, "fx", "multiCast", {"p": 0.12, "roll": "doubleSpell"}],
        [0.3, "fx", "blink"],
        [0.4, "fx", "blink_ring", {"p": 0.12, "roll": "doubleSpell"}],
        [0.4, "voice", "blink1|blink2", {"p": 0.12, "roll": "doubleSpell"}],
        [0.7, "fx", "blink", {"p": 0.12, "roll": "doubleSpell"}]
        ]
      },
      "parallelShift": {
        "why": "Penguin.cs RPC_parallelShift: clip blink (cut, :36836), parallelShift_ring Instantiated at the cast position, hero rotation (:36866; EffectControl life 1 + afterLife 1, plays its own Sounds/parallelShift) and voice parallelShift1 / parallelShift2 (Random.Range(0, 2), :36916-37045; Voices/multiCast only when recast within 12 s, :36909-36913, never on a fresh cast: its cooldown is agiAdjust(30), :36824) at 0; Yield 0.1 (:37052): moveSpeed 3 (:36297); Yield 0.2 (:37026): at 0.3 s every player of her side within 6 m, she included (FindAreaTarget :36344), moved 10 m along her facing (Move :36523), and parallelShift Instantiated where she lands (:36654; 0 m: the wardrobe hero doesn't travel); left out: blink on each other player warped with her (:36435, :36610; the code skips the caster, :36411, so the self-cast shows none); Yield 0.1 (:37028), Yield 0.2 (:37056): standby at 0.6 s (:36763); no Double Spell roll (only Double / Triple Cast's multiCast repeats it, :36704-36724)",
        "cues": [
        [0, "fx", "parallelShift_ring"],
        [0, "voice", "parallelShift1|parallelShift2"],
        [0.3, "fx", "parallelShift"]
        ]
      }
    }
  },
```

Sure: high on the traces and times; medium on how the rerun cues read without the clip restarting.

---

## cast4 (Falling Stars, Nova Flare): one pool

### Falling Stars

- Coroutine `RPC_fallingStars` (`$RPC_fallingStars$26175` :24878-25679, MoveNext :25003-25623). Max rank sLv 2
  (#242). Giant Star #442 is a passive that changes the skill, so it is ON: the stars are `RPC_giantStars_fire`
  (`$RPC_giantStars_fire$26510` :37136-37360) and `giantStar`, not `fallingStar`.

| t (s) | state | what | source |
|---|---|---|---|
| 0 | 0 | `actionState attack`, cooldown agiAdjust(30); clip `cast4` (cut, Once) | `:25321-25345` |
| 0 | 0 | voice `fallingStar1` / `fallingStar2` (`Random.Range(0, 2)`), or `multiCast` within 12 s | `:25354-25491` |
| 0 | 0 | Double Spell #431, 12 %: `multiCast` createEffect at the hero, status multiCast Lv 1, 3 s | `:25494-25535` |
| 0 | 0 | Focus Intellect read and removed; damage `talAdjust(15 + 15 x 2)` | `:25539-25554` |
| 0 | 0 | `fallingStar_ring` createEffect at the hero (position, rotation) | `:25557-25573` |
| 0 → 0.4 | | `Yield(2, 0.4)` (via `Block_133` → `IL_945`) | `:25576`, `:25618-25619`, `:25607` |
| 0.4 | 2 | camera motion blur (local player); enemies within `FloorToInt(1.5) x (8 + 4 x 2)` = 16 m, height 6, up to 10 with Giant Star: `RPC_giantStars_fire(enemy position)` each | `:25036-25190` |
| 0.4 | (fire 0) | `giantStar` Instantiated at the enemy's position, `Quaternion.identity` | `:37322-37338` |
| 0.4 → 1.0 | (fire) | `Yield(2, 0.6)`, then the hit within 3 m, x 1.25 | `:37355`, `:37254-37293` |
| 0.4 → 0.6 | | `Yield(3, 0.2)` (via `Block_120` → `IL_6EB`) | `:25196-25198`, `:25614-25615`, `:25605` |
| 0.6 | 3 | with multiCast: spent, `RPC_fallingStars_multiCast` reruns the skill from state 0, this one ends (`IL_5AC`) | `:25222-25264`, `:10354-10357` |
| 0.6 | 3 | else `standby` | `:25285-25305` |

- Sums: 0.4 + 0.2 = 0.6 to standby; the star at 0.4 (fire's state 0, same frame), its hit at 0.4 + 0.6 = 1.0. Rerun:
  its state 0 at 0.6 (voice `multiCast`, since the first cast set the 12 s timer at :25389; ring), its star at
  0.6 + 0.4 = 1.0, its standby at 0.6 + 0.6 = 1.2.
- Target point: the stars fall on enemies the skill finds by itself (no lock). An enemy at the 10 m point is inside the
  16 m reach, so one star at 10 m (Sheep decision 2: summoned at the enemy → the 10 m target point).
- Effects (probe):
  - `fallingStar_ring`: **ready**. EffectControl life 2, afterLife 0, followPosition; Line, Image and Ring emitters;
    plays its own `sounds/fallingStar_ring`.
  - `giantStar`: **ready**. EffectControl life 1.4, afterLife 1; Animation `Base Stack` 0.8 s (the falling mesh),
    SkinnedMeshRenderer, 3 RingEmitters, legacy particles; plays its own `sounds/fallingStar_hit`. Spawned with
    identity rotation in world space. The page turns it with the hero's facing, which is the same thing while she faces
    world forward.
  - `multiCast`: as in Blink.
- Left out: the camera motion blur (`AddMotionBlur(4, 2, 2, ...)` :25047, the local player's camera). The Wolf's Feral
  Assault left out its camera blur too. Again not one of the brief's two reasons, so the editor should know.

### Nova Flare

- Coroutine `RPC_novaFlare` (`$RPC_novaFlare$26250` :27421-27787, MoveNext :27524-27764). One rank (#254). The blast
  is the vortex's own coroutine (ManaVortex.cs `$RPC_novaFlare$18623` :554-844), started by
  `LxAw60aoWG.SendMessage("RPC_novaFlare")` (:27595).

| t (s) | state | what | source |
|---|---|---|---|
| 0 | 0 | with a vortex (`if (LxAw60aoWG)` :27591): the vortex told to blow (:27595); `actionState attack`, cooldown `novaFLare` agiAdjust(120); clip `cast4` (cut, Once) | `:27591-27622` |
| 0 | 0 | voice `novaFlare1` / `novaFlare2` (`Random.Range(0, 2)`) | `:27631-27756` |
| 0 | (vortex) | its damage = 0.5 x HP + MP; hp 0, `dead`; its `destroy` animation; `novaFlare` Instantiated at the vortex, `Quaternion.identity` | ManaVortex.cs:739-773 |
| 0 → 0.4 | | `Yield(2, 0.4)` | `:27750` |
| 0.4 | 2 | `standby` | `:27538-27576` |
| 0 → 1.0 | (vortex) | `Yield(2, 1)`; then every enemy within 12 + 4 x vortexLv (24 m at Mana Vortex 3) hit, vortex destroyed | ManaVortex.cs:804, :673-712 |

- Sums: standby at 0.4; the blast at 0 (the vortex's coroutine starts in the same frame), its hits at 0 + 1 = 1.0.
- No Double Spell roll and no Focus Intellect read on the hero side (the burst damage doesn't read Focus Intellect).
- Where: the vortex. Mana Vortex spawns it at `getSpawnVector(hero + 2 up, 5 forward - 2 up)` (:27133), the ground 5 m
  ahead, so `d 5` (question 2).
- Effect (probe, path patched in memory): `novaFlare` ready (Read this first 1). EffectControl life 4.
- Left out: the vortex itself and its `destroy` animation (ManaVortex.cs:763), a summon (ManaVortex.prefab) and not an
  effect (question 2). No `manaPool_hit` refund flash (Read this first 8).

### The entry

```json
  "cast4": {
    "why": "Penguin.cs: Falling Stars (RPC_fallingStars :24878-25679) and Nova Flare (RPC_novaFlare :27421-27787) both play cast4, cut in (PlayAnimation(\"cast4\", 0) :25342, :27619); one skill per play",
    "skills": {
      "fallingStars": {
        "why": "Penguin.cs RPC_fallingStars at max rank (sLv 2), Giant Star #442 on (passives on): clip (cut, :25342), voice fallingStar1 / fallingStar2 (Random.Range(0, 2), :25394-25449; Voices/multiCast only within 12 s of the last cast, :25383-25389) at 0; Double Spell #431: Random.Range(0, 100) < lckAdjust(12) = 12 % (:25500-25512) draws multiCast at the hero (createEffect :25524; plays its own Sounds/trippleCast) and gives multiCast Lv 1 for 3 s (:25530); fallingStar_ring at the hero (createEffect :25573; life 2, followPosition; plays its own Sounds/fallingStar_ring) at 0; Yield 0.4 (:25607): every enemy within 16 m (:25066-25071), up to 10, gets RPC_giantStars_fire at its feet (:25134), which Instantiates giantStar there at once, identity (:37338; plays its own Sounds/fallingStar_hit), the hit 0.6 s later (:37355, :37293): the enemy at the 10 m target point (Sheep decision 2); Yield 0.2 (:25605): at 0.6 s, with the rolled multiCast, RPC_fallingStars_multiCast reruns the skill (:25228-25246, :10354-10357) on the same roll: voice multiCast (the 12 s timer was set at 0, :25389, :25469-25481), its ring at 0.6, its star at 0.6 + 0.4 = 1.0 (the clip's restart at 0.6, :25339-25342, isn't played on the page; its own roll isn't chained, as TTO1102 <RPC_fallingStars>d__187::MoveNext@0x1ded300 skips it, pseudo/Penguin.c:10634); else standby at 0.6 s (:25285); left out: the camera motion blur at 0.4 s (:25047), as Feral Assault's",
        "cues": [
        [0, "voice", "fallingStar1|fallingStar2"],
        [0, "fx", "multiCast", {"p": 0.12, "roll": "doubleSpell"}],
        [0, "fx", "fallingStar_ring"],
        [0.4, "fx", "giantStar", {"d": 10}],
        [0.6, "voice", "multiCast", {"p": 0.12, "roll": "doubleSpell"}],
        [0.6, "fx", "fallingStar_ring", {"p": 0.12, "roll": "doubleSpell"}],
        [1.0, "fx", "giantStar", {"d": 10, "p": 0.12, "roll": "doubleSpell"}]
        ]
      },
      "novaFlare": {
        "why": "Penguin.cs RPC_novaFlare, with the Penguin's Mana Vortex in place (:27591; without one nothing plays, :27740): the vortex told to blow (SendMessage :27595), clip (cut, :27619) and voice novaFlare1 / novaFlare2 (Random.Range(0, 2), :27660-27756) at 0; the vortex's RPC_novaFlare Instantiates its novaFlare field (ManaVortex.cs:540; Resources characters/elementals/manavortex/effects/novaFlare; life 4, plays its own Sounds/novarFlare) at the vortex, identity, at once (ManaVortex.cs:773), its hits 1 s later (:804, :673-712): the vortex 5 m ahead, where Mana Vortex places it (getSpawnVector(pos + 2 up, 5 forward - 2 up), Penguin.cs:27133); Yield 0.4 (:27750): standby at 0.4 s (:27556); left out: the vortex itself (a summon, ManaVortex.prefab) and its destroy animation (ManaVortex.cs:763); no refund flash (manaPool_hit comes only from ManaVortex.RPC_dead, :1318-1330, which a vortex marked dead at :745 never runs, :399)",
        "cues": [
        [0, "voice", "novaFlare1|novaFlare2"],
        [0, "fx", "novaFlare", {"d": 5}]
        ]
      }
    }
  },
```

Sure: high on the traces and times; medium on `d 5` (question 2).

---

## arcticEmperor (Arctic Emperor)

- Coroutine `RPC_arcticEmperor` (`$RPC_arcticEmperor$26455` :34890-35323, MoveNext :35004-35297), max rank sLv 2
  (#372); the ticks in `arcticEmperor_hit` (`$arcticEmperor_hit$26464` :35328-35700).

| t (s) | state | what | source |
|---|---|---|---|
| 0 | 0 | `actionState attack`, cooldown agiAdjust(600); clip `arcticEmperor` (cut, Once) | `:35138-35162` |
| 0 | 0 | voice `arcticEmperor1` / `arcticEmperor2` (`Random.Range(0, 2)`) | `:35171-35291` |
| 0 → 0.3 | | `Yield(2, 0.3)` | `:35281` |
| 0.3 | 2 | `arcticEmperor` Instantiated at the hero (position, rotation); `arcticEmperor_hit(hero position, 2)` started | `:35036-35076` |
| 0.3 → 1.0 | | `Yield(3, 0.7)` | `:35277` |
| 1.0 | 3 | `standby` | `:35103-35123` |
| 0.3 + 0 ... 7 | (hit) | every 1 s (`Yield(2, 1)` :35644): `frost` on every enemy within 8 m (:35547-35586) | `:35431-35646` |
| 0.3 + 8 = 8.3 | (hit) | the burst `talAdjust(60 + 60 x 2)` within 8 m, frost removed | `:35459-35510` |

- Sums: 0.3 + 0.7 = 1.0 to standby; the castle at 0.3; the burst at 0.3 + 8 x 1 = 8.3 (the Bible's 8.3 s).
- Effect: `arcticEmperor`, **needs Penguin_arcticEmperor** (Read this first 2). Its life is 9 s from 0.3 s, so it ends
  at 9.3 s, plus 2 s of afterLife. It plays its own `sounds/arcticEmperor`.
- Left out: the `frost` status look on each enemy (`Effects/frost`, CharacterControl.cs:38733-38763). That is on an
  enemy with no target-point analogue: an enemy at the 10 m point is outside the 8 m reach (:35466).

```json
  "arcticEmperor": {
    "why": "Penguin.cs RPC_arcticEmperor at max rank (sLv 2): clip (cut, :35159) and voice arcticEmperor1 / arcticEmperor2 (Random.Range(0, 2), :35200-35291) at 0; Yield 0.3 (:35281): the castle, arcticEmperor Instantiated at the hero (:35054; EffectControl life 9 + afterLife 2, Penguin_arcticEmperor's fade 0.3 in / 7.7 / 1.0 out; plays its own Sounds/arcticEmperor) and arcticEmperor_hit started (:35076: frost every 1 s, the burst at 0.3 + 8 = 8.3 s, :35431-35646); Yield 0.7 (:35277): standby at 1.0 s (:35103); left out: the frost look on each enemy (CharacterControl.cs:38733-38763), on an enemy within 8 m (:35466), and the 10 m target point is outside that",
    "cues": [
    [0, "voice", "arcticEmperor1|arcticEmperor2"],
    [0.3, "fx", "arcticEmperor"]
    ]
  },
```

Sure: high.

---

## focusIntellect (Focus Intellect)

- Coroutine `RPC_focusIntellect` (`$RPC_focusIntellect$26482` :35709-36129, MoveNext :35811-36122). One rank (#421).

| t (s) | state | what | source |
|---|---|---|---|
| 0 | 0 | `actionState attack`, cooldown agiAdjust(120); clip `focusIntellect` (cut, Once) | `:35930-35954` |
| 0 | 0 | `focusIntellect_ring` createEffect at the hero (position, rotation) | `:35963-35981` |
| 0 | 0 | voice `focusIntellect1` / `focusIntellect2` (`Random.Range(0, 2)`; the opaque `break` at :36044 leads to :36100) | `:35995-36114` |
| 0 → 0.8 | | `Yield(2, 0.8)` | `:36118` |
| 0.8 | 2 | INT > 100 (the page assumes high INT, the cast-bar rule): status `focusIntellect` Lv 5, `chaAdjust(6)` s, value INT - 100 (else "This penguin is too stupid!") | `:35852-35867` |
| 0.8 | (addStatus) | `Effects/focusIntellect` Instantiated at the hero, `Quaternion.identity`, parented to her, scale 1, named `focusIntellectFx`; no wait before it (`addStatus` case 0 → the switch) | CharacterControl.cs:38790-38825, :32489-32815 |
| 0.8 → 1.0 | | `Yield(3, 0.2)` | `:35872`, `:36104` |
| 1.0 | 3 | `standby` | `:35895-35915` |
| 0.8 + 6 = 6.8 | | the status ends: `focusIntellectFx` destroyed (or sooner, at the next damage spell, which removes the status) | CharacterControl.cs:17490-17500 |

- Sums: 0.8 + 0.2 = 1.0 to standby; the aura at 0.8, gone at 0.8 + 6 = 6.8 (chaAdjust(6) = 6 s at CHA 1, the base the
  Sheep used for chaAdjust(12) = 12 s).
- Effects (probe): `focusIntellect_ring` **ready** (life 1, afterLife 1, followPosition; Image and Ring emitters; plays
  its own `sounds/focusIntellect_ring`). `focusIntellect` **ready** (life 30, no follow; 2 RingEmitters; plays its own
  `sounds/focusIntellect`). The inventory lacks it because it is loaded in CharacterControl.cs, so it needs
  `kill 6`, since its life of 30 s outlasts the status.

```json
  "focusIntellect": {
    "why": "Penguin.cs RPC_focusIntellect: clip (cut, :35951), focusIntellect_ring at the hero (createEffect :35981; life 1 + afterLife 1, followPosition, plays its own Sounds/focusIntellect_ring) and voice focusIntellect1 / focusIntellect2 (Random.Range(0, 2), :36024-36114) at 0; Yield 0.8 (:36118): the focusIntellect status, Lv 5, chaAdjust(6) = 6 s (:35867; INT > 100, :35852, high INT as the cast-bar rule), whose add draws Effects/focusIntellect on the hero at once, identity, parented (CharacterControl.cs:38790-38825; life 30, plays its own Sounds/focusIntellect), destroyed when the status ends (CharacterControl.cs:17490-17500): kill 6; Yield 0.2 (:36104): standby at 1.0 s (:35895)",
    "cues": [
    [0, "fx", "focusIntellect_ring"],
    [0, "voice", "focusIntellect1|focusIntellect2"],
    [0.8, "fx", "focusIntellect", {"kill": 6}]
    ]
  }
```

Sure: high.

---

## What the editor needs, in one list

- Four entries: `blink` (pool: blink, parallelShift), `cast4` (pool: fallingStars, novaFlare), `arcticEmperor`,
  `focusIntellect`. No SEQ change.
- Effects to build: blink_ring, blink, multiCast, parallelShift_ring, parallelShift, fallingStar_ring, giantStar,
  focusIntellect_ring, focusIntellect (all ready); arcticEmperor (Penguin_arcticEmperor + its LAYOUTS entry);
  novaFlare (ready, but `wardrobe_fx.py` must find it under `characters/elementals/manavortex/effects/`).
- Voices (voices/): blink1, blink2, parallelShift1, parallelShift2, multiCast, fallingStar1, fallingStar2, novaFlare1,
  novaFlare2, arcticEmperor1, arcticEmperor2, focusIntellect1, focusIntellect2.
- Roll name `doubleSpell` (12 %), used in Blink and Falling Stars. FX.rolls reset per play, so each tile rolls its own.

## Questions (only what the Sheep / Wolf decisions don't answer)

1. **Double Spell reruns the skill and restarts its clip** (Blink at 0.4 s, Falling Stars at 0.6 s). The decisions
   cover the roll, not a rerun. Recommended default: what I wrote above. The rerun's effects and voice play on the
   same 12 % roll, but the clip doesn't restart: the page has no cue that restarts a clip. One rerun only, as TTO does.
   If the user wants the clip to replay too, that is a small page feature for later (a cue kind that restarts the
   current clip). The other choice is the flash only, with no rerun cues.
2. **Nova Flare's blast point and the vortex.** Not an enemy, so the 10 m rule doesn't settle it. Recommended
   default: the blast at the vortex 5 m ahead, where Mana Vortex places it (:27133), and no vortex model (it is a
   summon, ManaVortex.prefab, and the Mana Vortex tile would need it first). Other choices: 10 m, or show the vortex
   and its `destroy` animation.
3. **The multiCast tint.** While the Double Spell status lasts (0.4 s in Blink, 0.6 s in Falling Stars), the game
   tints the Penguin purple (`setColor(0.48, 0.29, 0.78)`, CharacterControl.cs:38470-38477; reset on removal,
   :17354-17360). Recommended default: leave it out (the page doesn't tint heroes; it is not an effect prefab).
