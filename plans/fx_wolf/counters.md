# Wolf effects + sounds research: Counter, Mirror Blade, Dark Edge, Dual Brand, Crusader, Art Breaker, Art Cancel

Scope: clips counter1, counter2, mirrorCounter1, mirrorCounter2, darkEdge, dualBrand, crusader, artBreaker, artCancel.
Research only (recipe steps 1-3). All line numbers are `D:\12tails\DecompiledSource\Wolf.cs` unless named. Times are seconds
from the start of the clip the cue is keyed by. Distance 0 = at the hero, the same as the pilot: the wardrobe hero
stands still, so a skill's dash is not added (Feral Strike's 4.8 m dash has cue distance 0 too).

Prefab facts below come from a read-only in-memory probe (`wardrobe_fx.Game` / `effect`; scripts in
`checks\fx_wolf_research\counters\probe*.py`, nothing written to the data).

---

## counter1 (Counter's stance): no entry

- Coroutine `RPC_counter1` (`:27912-28290`). At 0: `PlayAnimation("counter1", 0)` (`:28099`), `moveSpeed -1`, `mTempHp = hp`
  (`:28119`); wait 0.2 s (`:28245`); at 0.2 `moveSpeed 0` (`:28052`), then it checks **every frame** (`YieldDefault(3)`,
  `:28249`) until `actionTime + 0.8` (`:28126`, standby `:28142`).
- No `createEffect`, `Instantiate` or `PlayOneShot` in the coroutine. The stance is silent and draws nothing.
- **What triggers the strike:** the first frame (from 0.2 s on) where `hp < mTempHp`. Then `mCounterDmg = mTempHp - hp` and
  it starts `RPC_counter2` (`:28211-28229`). With no HP lost, the stance ends at 0.8 s with no strike.
- **What the wardrobe shows:** the SEQ `Counter: counter1@0.8 counter2` already plays it as "hit at the end of the window"
  (stance 0.8 s, then the strike). That is a fair stand-in with no attacker. The earliest possible strike is at 0.2 s.
- Proposed: no cue entry for counter1.

## counter2 (Counter's strike)

- Coroutine `RPC_counter2` (`:28286-28883`), started by `RPC_counter1` as described above (Impulse #333/#334 starts the
  same strike, per the reference).
- At 0: `addTimeOut` (`:28686`), `PlayAnimation("counter2", 0)` (`:28701`), `moveSpeed -1` (`:28710`), voice
  `Random.Range(0, 2) == 0` ? counter1 : counter2 (`:28742-28797`). Wait 0.1 s (`:28878`). At 0.1: `moveSpeed 9` (`:28431`).
  Wait 0.2 s (`:28876`). At 0.3: the box hit, `RPC_AddEffectDamage` on each enemy (`:28506`) and `RPC_counter_hit` at
  that enemy's collider (`:28511-28526`). Wait 0.1 s (`:28880`). At 0.4: `moveSpeed 0` (`:28551`). Wait 0.3 s (`:28882`).
  At 0.7: standby (`:28619`).
- Left out: `counter_hit`. It spawns at the struck enemy (`ClosestPointOnBounds`, `:28511`; `Instantiate(this.counter_hit, ...)`
  `:8795`), so it is target-side. It is also an inspector field (`public GameObject counter_hit`, `:14520`), not a Resources
  prefab: there is no `wolf/effects/counter_hit` in the ResourceManager, so `wardrobe_fx.py` could not build it anyway.
  Not in the inventory.

```json
  "counter2": {
    "why": "Wolf.cs RPC_counter2, started by RPC_counter1 the frame the hero's HP drops (:28211-28229; the wardrobe plays it after the full 0.8 s stance): clip and voice counter1 / 2 at 0 (:28701-28797); step back 0.1 s, the 9 m/s lunge, the hit at 0.3 s (:28431, :28506), standby 0.7 s (:28619); left out: counter_hit, at the struck enemy (:28511-28526, :8795)",
    "cues": [
    [0, "voice", "counter1|counter2"]
    ]
  }
```

Sure: high. The voice names `counter1` / `counter2` exist only under `voices/`, so no file-name clash (see the clash below).

## mirrorCounter1 (Mirror Blade)

- Coroutine `RPC_mirrorBlade` (`:34410-35021`). At 0: `PlayAnimation("mirrorCounter1", 0)` (`:34839`), `moveSpeed 0`
  (`:34854`), voice `Random.Range(0, 2) == 0` ? mirrorBlade1 : mirrorBlade2 (`:34888-34943`), `mirrorBlade_ring`
  createEffect at the hero (`:34974`). Wait 0.2 s (`:35012`). At 0.2: `mirrorBlade_mirror` createEffect at the hero
  (`:34574`), `mMirrorHp = hp` (`:34588`). Wait 0.8 s (`:35003`). At 1.0: `PlayAnimation("mirrorCounter2", 0)` (`:34615`)
  and, for the local player only, a camera white flash (`CameraEffect.AddColorRamp("whiteRamp", ...)`, `:34633-34638`).
  Wait 0.4 s (`:35020`). At 1.4: `RPC_AddEffectDamage(433, clamp(mMirrorHp - hp, 0, 1999))` to the locked target
  (`:34673-34710`) and `RPC_mirrorBlade_hit` at the target's collider (`:34715-34725`). Wait 0.4 s (`:35007`). At 1.8: standby (`:34746`).
- **What triggers each part:** nothing reacts to a hit. Every part always plays: the ring, the mirror, the clip change at
  1.0 s, and the strike at 1.4 s. Only the damage depends on the HP lost between 0.2 and 1.4 s. With no damage taken, it
  still swings for 0. So the wardrobe should play all of it as it is.
- Effects:
  - `mirrorBlade_ring`: **ready**. EffectControl life 3, followState false, so no 5th value. It plays its own sound
    (`sounds/mirrorBlade_ring`).
  - `mirrorBlade_mirror`: **needs ShatterMesh, StaticMesh**, so it is left out for now. EffectControl life 1.2, afterLife 0.6,
    followState false. Future cue: `[0.2, "fx", "mirrorBlade_mirror"]`.
  - `mirrorBlade_hit`: **ready**, but left out because it is at the target (see mirrorCounter2).
- **Timing mismatch with the page:** the SEQ is `mirrorCounter1@1.2 mirrorCounter2`. The game switches clips at **1.0 s**
  (0.2 + 0.8). The clip `mirrorCounter1` is 1.0 s long (`data/wolf/clips.json`), so the page holds its last frame for
  0.2 s. 1.2 s is the HP window (0.2 to 1.4), not the clip switch. This is a separate fix in index.html (not a cue job).
  None of the cues below depend on it.

```json
  "mirrorCounter1": {
    "why": "Wolf.cs RPC_mirrorBlade: clip, voice mirrorBlade1 / 2 and mirrorBlade_ring at once (:34839-34974); left out: mirrorBlade_mirror at the hero at 0.2 s (:34574) needs ShatterMesh, StaticMesh; mirrorCounter2 at 1.0 s (:34615), the returned damage and mirrorBlade_hit at the locked target at 1.4 s (:34673-34725, at the target), standby 1.8 s (:34746). Nothing in it reacts to a hit: only the damage depends on the HP lost 0.2-1.4 s",
    "cues": [
    [0, "voice", "mirrorBlade1|mirrorBlade2"],
    [0, "fx", "mirrorBlade_ring"]
    ]
  }
```

Sure: high.

## mirrorCounter2: no entry (optional target cue)

- It starts at 1.0 s in the game (1.2 on the page). The only effect after it starts is `mirrorBlade_hit`, 0.4 s in, at
  the locked target: left out under the target rule.
- Optional, if the editor or the user counts a locked-target strike under the "needs a target point" exception (I don't
  think it does: the skill already shows on the hero through the ring and, once built, the mirror):
  `[0.4, "fx", "mirrorBlade_hit", 10]`. It is ready: EffectControl life 1, followState false, and it plays its own
  `sounds/mirrorBlade_hit`. The game puts it at the target's collider, about 1-1.5 m up (`ClosestPointOnBounds(hero +
  1.5 up)`). At cue distance 10 it would sit at the hero's ground height.

## darkEdge (Dark Edge)

- Coroutine `RPC_darkEdge` (`:30579-31048`). At 0: `addTimeOut` (`:30893`), `PlayAnimation("darkEdge", 0.2f)` (`:30908`),
  `moveSpeed 0`, voice `Random.Range(0, 2) == 0` ? darkEdge1 : darkEdge2 (`:30949-31036`). Wait 0.2 s (`:31029`). At 0.2:
  `darkEdge_ring` createEffect at the hero (`:30743`). Wait 0.2 s (`:31031`). At 0.4: `RPC_AddStatus("darkEdge", sLv,
  chaAdjust(2 x sLv))` on itself (`:30805`; rank 4 = 8 s before CHA). Wait 0.2 s (`:31045`). At 0.6: standby (`:30826`).
- Effects:
  - `darkEdge_ring`: **needs VortexEmitter**, so it is left out. EffectControl life 1, followPosition true, followState
    false. It plays its own `sounds/darkEdge_ring`. Future cue: `[0.2, "fx", "darkEdge_ring"]`.
  - The status's own effect is not in the inventory, which lists only `Wolf.cs` loads. When `darkEdge` is added,
    `CharacterControl.cs:34159-34210` loads `Effects/darkEdge` and instantiates it twice, once parented to each hand bone
    (`mount_Hand_L`, `mount_Hand_R`; local position (0, 0, 0.2), rotation Euler(90, 0, 0)). It is a single ImageEmitter
    with no EffectControl. It stays until the status ends (`CharacterControl.cs:15105-15124` destroys `darkEdge1Fx` /
    `darkEdge2Fx`). This is a buff on the hero, so it would stay under the rules, but the cue format can't attach an
    effect to a bone or hold it for the status duration. Left out: it needs a "bone attach + duration" cue part. If it is
    built, put it at 0.4 s, on both hands.
- **The darkEdge clip is shared:** Holy Armor plays the same clip (`RPC_holyArmor`, `:33598`). Cues are keyed by clip, so
  the `darkEdge` tile can carry only one skill's cues. Whoever researches Holy Armor needs to agree on this with the editor.
- The Dark Edge normal-attack swings (`darkEdge1` / `darkEdge2`, `:15091`, `:17682`) belong to the nAttack clips, not to
  this clip (another researcher's scope).

```json
  "darkEdge": {
    "why": "Wolf.cs RPC_darkEdge: clip and voice darkEdge1 / 2 at 0 (:30908-31036); left out: darkEdge_ring at the hero at 0.2 s (:30743) needs VortexEmitter; the darkEdge status at 0.4 s (:30805) puts Effects/darkEdge on both hand bones until it ends (CharacterControl.cs:34159-34210; needs a bone-attached, held cue); standby 0.6 s (:30826). The clip is Holy Armor's too (:33598)",
    "cues": [
    [0, "voice", "darkEdge1|darkEdge2"]
    ]
  }
```

Sure: high on the trace. The hand aura's look is not checked.

## dualBrand (Dual Brand)

- Coroutine `RPC_dualBrand` (`:35778-36905`). The waits and states, traced case by case:

| t (s) | state | what | source |
|---|---|---|---|
| 0 | 0 | clip `dualBrand` (`PlayAnimation(.., 0)`), `moveSpeed 0`, voice dualBrand1 / 2 (`Random.Range(0, 2)`), `dualBrand_ring` at the hero; wait 0.2 | `:36692-36817`, `:36893` |
| 0.2 | 2 | `moveSpeed 4`; wait 0.1 | `:35914`, `:36867` |
| 0.3 | 3 | `dualBrand_slash1` at the hero; wait 0.2 | `:35959`, `:36887` |
| 0.5 | 4 | hit 1 (r 5 circle), `dualBrand_hit` at each enemy; wait 0.1 | `:36058`, `:36879` |
| 0.6 | 5 | `dualBrand_slash2` at the hero; wait 0.2 | `:36119`, `:36873` |
| 0.8 | 6 | `moveSpeed 5`, hit 2; wait 0.1 | `:36156`, `:36208`, `:36885` |
| 0.9 | 7 | `moveSpeed 9`, `dualBrand_slash3` at the hero; wait 0.1 | `:36251`, `:36274`, `:36843` |
| 1.0 | 8 | hit 3 (box); wait 0.1 | `:36358`, `:36901` |
| 1.1 | 9 | `moveSpeed 2`, `dualBrand_slash4` at the hero; wait 0.1 | `:36401`, `:36424`, `:36856` |
| 1.2 | 10 | `moveSpeed 1`; wait 0.1 | `:36461`, `:36861` |
| 1.3 | 11 | hit 4; wait 0.1 | `:36535`, `:36863` |
| 1.4 | 12 | `moveSpeed 0`; wait 0.2 | `:36578`, `:36871` |
| 1.6 | 13 | standby | `:36604` |

  These match the reference's movement table: its t is counted from the first speed set (0.2 s), so its hits at 0.3, 0.6,
  0.8 and 1.1 are 0.5, 0.8, 1.0 and 1.3 here.
- Effects:
  - `dualBrand_ring`: **ready**. EffectControl life 1, afterLife 1, followPosition + **followState** true, so the 5th
    value is 1.6. Its life ends first, so the cut never shows, but it is the game's rule. It plays its own
    `sounds/dualBrand_ring`.
  - `dualBrand_slash1`, `_slash2`, `_slash4`: **need Animation, TrailEmitter**. `dualBrand_slash3`: **needs EffectControl(child),
    VortexEmitter**. All four are left out. Each has followState true and plays `sounds/dualBrand_slash`. Future cues:
    `[0.3, "fx", "dualBrand_slash1", 0, 1.6]`, `[0.6, "fx", "dualBrand_slash2", 0, 1.6]`,
    `[0.9, "fx", "dualBrand_slash3", 0, 1.6]`, `[1.1, "fx", "dualBrand_slash4", 0, 1.6]`.
    With all four left out, the wardrobe loses the slash whoosh too: the sound belongs to the prefab, not to a voice.
  - `dualBrand_hit` (ready) is left out: it is at each enemy (`hitPos` = the enemy's centre, `:36048`).
  - In the game, the slashes spawn where the dashing hero is at that moment: 0.4, 1.6, 2.9 and 4.7 m from the start.
    The wardrobe convention is 0.

```json
  "dualBrand": {
    "why": "Wolf.cs RPC_dualBrand: clip, voice dualBrand1 / 2 and dualBrand_ring at once (:36692-36817); left out: dualBrand_slash1 / 2 / 3 / 4 at the hero at 0.3 / 0.6 / 0.9 / 1.1 s (:35959, :36119, :36274, :36424; 1, 2, 4 need Animation, TrailEmitter, 3 needs EffectControl(child), VortexEmitter) and dualBrand_hit at each enemy at 0.5 / 0.8 / 1.0 / 1.3 s (at the target); standby at 1.6 s (:36604), which ends dualBrand_ring (followState)",
    "cues": [
    [0, "voice", "dualBrand1|dualBrand2"],
    [0, "fx", "dualBrand_ring", 0, 1.6]
    ]
  }
```

Sure: high. Each wait was read case by case, not from the flow's order alone.

## crusader (Crusader; Law Bringer changes it)

- Coroutine `RPC_crusader` (`:20891-21690`). At 0: `addTimeOut` (`:21350`), `PlayAnimation("crusader", 0.2f)` (`:21365`),
  `moveSpeed 0`, then a branch on `getLawBringerLv() > 0` (Law Bringer #412, a Class-C passive, learned):
  - not learned: `crusader_ring` createEffect at the hero (`:21528`), voice `Random.Range(0, 2) == 0` ? crusader1 :
    crusader2 (`:21571-21685`);
  - learned: `lawBringer_ring` (`:21399`), voice lawBringer1 / lawBringer2 (`:21442-21688`).

  Wait 0.6 s (`:21675`). At 0.6: the slash, `crusader` (or `lawBringer` with the passive), created at the hero with
  rotation `hero.rotation * Euler(270, 90, 0)` (`:21097` / `:21060`). Wait 0.4 s (`:21679`). At 1.0: `moveSpeed 7`
  (`:21134`). Wait 0.4 s (`:21652`). At 1.4: `moveSpeed 0`, the box hit (`:21161-21262`; `crusader_hit` / `lawBringer_hit`
  at each enemy via `RPC_crusader_hit`, `:8457`, `:8492`), and the self-heal only when something was hit. Wait 0.4 s
  (`:21654`). At 1.8: standby (`:21283`).
- Effects:
  - `crusader_ring`: **ready**. EffectControl life 3, followPosition + **followState** true, so the 5th value is 1.8. It
    plays its own `sounds/crusader1`.
  - `crusader` (the slash): **needs Animation, TrailRenderer**, so it is left out. EffectControl life 1.5, followState
    true. It plays `sounds/crusader2`. **The cue format has no rotation**, and the game turns this one Euler(270, 90, 0), so
    it needs a rotation cue value when it is built. Future cue: `[0.6, "fx", "crusader", 0, 1.8]` plus that rotation.
  - `crusader_hit` (needs Light) and `lawBringer_hit` (needs Light): at the target, left out.
  - Law Bringer variant: `lawBringer_ring` is **ready** (same layout as crusader_ring, life 3, followState, plays
    `sounds/crusader1`). `lawBringer` **needs Animation, TrailRenderer** (followState, plays `sounds/crusader2`).
- **Decision for the user:** "max rank" doesn't say whether a separate passive that reshapes a skill counts. The
  precedent is Added Fire, which was put in only when the user said "want it". The entry below is plain Crusader (rank 4,
  no Law Bringer). The Law Bringer alternative:
  `[[0, "voice", "lawBringer1|lawBringer2"], [0, "fx", "lawBringer_ring", 0, 1.8]]` (+ `lawBringer` at 0.6 when built).

```json
  "crusader": {
    "why": "Wolf.cs RPC_crusader, without Law Bringer #412 (getLawBringerLv() branches :21377 and :21036): clip, crusader_ring and voice crusader1 / 2 at once (:21365-21685); left out: the crusader slash at the hero at 0.6 s turned Euler(270, 90, 0) (:21097) needs Animation, TrailRenderer; the 7 m/s dash 1.0-1.4 s and the hit at 1.4 s (crusader_hit at each enemy, at the target); standby at 1.8 s (:21283), which ends crusader_ring (followState)",
    "cues": [
    [0, "voice", "crusader1|crusader2"],
    [0, "fx", "crusader_ring", 0, 1.8]
    ]
  }
```

Sure: high on the trace. **Blocked by a sound file-name clash** (below): as things stand, the voice cue would play the
wrong file.

## artBreaker (Art Breaker)

- Coroutine `RPC_artBreaker` (`:33808-34385`). At 0: the cooldown (`:34146-34161`), `PlayAnimation("artBreaker", 0.1f)`
  (`:34176`), `moveSpeed 0`, voice `Random.Range(0, 2) == 0` ? artBreaker1 : artBreaker2 (`:34217-34272`), `artBreaker_ring`
  createEffect at the hero (`:34303`), and for the local player a motion blur (`CameraEffect.AddMotionBlur`, `:34332-34335`).
  Wait 1.0 s (`:34355`). At 1.0: if the locked target is within 30 m (`:33988`), the hit, `artBreaker_hit` at the target's
  bounds centre (`:34016-34026`) and the `artCancel` status on it (`:34036`). Wait 0.3 s (`:34364`). At 1.3: standby (`:34058`).
- Effects:
  - `artBreaker_ring`: **needs EmitterControl**, so it is left out. EffectControl life 2, followState false. It plays its own
    `sounds/artBreaker_ring`. Future cue: `[0, "fx", "artBreaker_ring"]`.
  - `artBreaker_hit`: **ready**. EffectControl life 1, afterLife 1, followState false. It plays `sounds/artCancel_hit`.
    Left out because it is at the target.
- **Judgement call, the target exception:** Art Breaker's strike exists only at the distant locked target. With the ring
  unbuilt, the wardrobe shows nothing but the voice. If the exception ("needs a target point to exist at all") is read to
  cover a ranged single-target strike, add `[1.0, "fx", "artBreaker_hit", 10]`. The game puts it at the target's body
  centre, about 1 m up, but the cue puts it at ground level. My reading is that `_hit` effects stay out: the exception is
  for effects placed at a target point (a ground mark, a landing), and this is a hit spark. Sure: medium. Ask the user if
  the skill looks empty.

```json
  "artBreaker": {
    "why": "Wolf.cs RPC_artBreaker: clip (0.1 s fade) and voice artBreaker1 / 2 at 0 (:34176-34272); left out: artBreaker_ring at the hero at 0 (:34303) needs EmitterControl; artBreaker_hit at the locked target (within 30 m) at 1.0 s (:33988-34026, at the target); standby 1.3 s (:34058)",
    "cues": [
    [0, "voice", "artBreaker1|artBreaker2"]
    ]
  }
```

## artCancel (Art Cancel)

- Coroutine `RPC_artCancel` (`:27300-27875`). At 0: the cooldown (`:27617-27623`), `PlayAnimation("artCancel", 0.2f)`
  (`:27638`), `removeLockStatus` (`:27647`), `moveSpeed 10` (`:27650`), voice `Random.Range(0, 2) == 0` ? artCancel1 :
  artCancel2 (`:27682-27737`). Then three spawns at the hero: `Instantiate(dust_forward)` (`:27750`), `artCancel_slide`
  createEffect (`:27771`) and `Instantiate(artCancel_ring)` (`:27803`). The local player also gets a motion blur
  (`:27823-27826`). Wait 0.6 s (`:27853`). At 0.6: `moveSpeed 0` (`:27447`), the box hit, `artCancel_hit` at each enemy
  (`:27494-27509`, an inspector prefab `this.artCancel_hit`), and the `artCancel` status on each enemy. Wait 0.4 s
  (`:27857`). At 1.0: standby (`:27556`).
- Effects:
  - `artCancel_slide`: **ready**. EffectControl life 1, followPosition + **followState** true, so the 5th value is 1.0. It
    plays its own `sounds/artCancel1`.
  - `artCancel_ring`: **ready**. It is instantiated, so no EffectControl owner, the same as feralStrike_ring.
    EffectControl life 3, followState false.
  - `dust_forward`: **not in the inventory**, because it is an inspector field (`public GameObject dust_forward`, `:14247`),
    not a `Resources.Load`. A Resources prefab of the same name exists (`gameassets/characters/heroes/wolf/effects/dust_forward`).
    Its parts are EffectControl (life 0.5, followState false) and 2 LineEmitters, both built, and `wardrobe_fx.effect()`
    reads it with no error. So it is effectively **ready**, and `wardrobe_fx.py` can build it by that name. Sure (that the
    inspector field is this prefab): medium-high. The names match and it sits in the Wolf effects folder, but I couldn't
    find the hero prefab's Wolf component to compare the reference. The same `dust_forward` is also instantiated by nAttack1
    (`:14985`) and Blade Fang (`:25641`, `:25854`, `:26073`), so the editor should keep it consistent with those researchers.
  - `artCancel_hit`: at the target, left out.

```json
  "artCancel": {
    "why": "Wolf.cs RPC_artCancel: clip, the 10 m/s dash, voice artCancel1 / 2, dust_forward, artCancel_slide and artCancel_ring at the hero at once (:27638-27803; dust_forward is the Wolf's inspector field, built from Resources wolf/effects/dust_forward); the hit at 0.6 s (artCancel_hit at each enemy, at the target); standby at 1.0 s (:27556), which ends artCancel_slide (followState)",
    "cues": [
    [0, "voice", "artCancel1|artCancel2"],
    [0, "fx", "dust_forward"],
    [0, "fx", "artCancel_slide", 0, 1.0],
    [0, "fx", "artCancel_ring"]
    ]
  }
```

Sure: high on the trace. **Blocked by the same sound file-name clash** as Crusader.

---

## Blocking problem: voice and sound files with the same name

`wolf/voices/` and `wolf/sounds/` both hold **crusader1, crusader2, artCancel1, artCancel2**, and they are different
recordings (md5 differ; e.g. `sounds/crusader1.wav` is 45,910 B, `voices/crusader1.wav` is 33,098 B). The effects use the
sounds/ ones: `crusader_ring` -> `sounds/crusader1`, `crusader` / `lawBringer` -> `sounds/crusader2`, `artCancel_slide` ->
`sounds/artcancel1` (checked by resolving each AudioSource's clip against the ResourceManager paths).

`wardrobe_fx.py` exports both kinds to one `data/wolf/sfx/<name>.mp3`. `rip_wav()` looks in `sounds/` first, so the
voice cues `crusader1|crusader2` and `artCancel1|artCancel2` would play the effect sounds (slash whooshes), not the
Wolf's voice, and the page can't tell the two apart either (`Sound.play(cls, name)`). Before the Crusader and Art Cancel
voice cues go in, the pipeline and page need separate names for voices and sounds (e.g. `sfx/voice_<name>.mp3`, or a
voices/ subfolder). That is a pipeline change, not a cue change. The pilot's voices (armorBreak1/2, crossBreak1/2,
grandCross1/2, feralStrike1/2) don't clash: they were checked against the sounds/ listing.

## Bible findings (to offer the user; not written there)

- Counter's stance checks HP **every frame** from 0.2 s to 0.8 s (`YieldDefault(3)`, `:28249`), not "every 0.2 s"
  (`wolf-skill-reference.md` wlf_counter1-2). HP lost between 0 and 0.2 s is caught at 0.2 s, because `mTempHp` is
  recorded at 0. Sure: high.
- Mirror Blade switches to `mirrorCounter2` at 1.0 s (`:34615`, after waits of 0.2 + 0.8 s). The strike comes 0.4 s later
  at 1.4 s. The reference has it right. The wardrobe's SEQ `mirrorCounter1@1.2` is the page's own mismatch.
- The Dark Edge status puts an `Effects/darkEdge` aura on both hand bones for its duration (`CharacterControl.cs:34159-34210`).
  This is a visual fact, probably not something the Bible needs.

## Cross-cutting point the editor should decide once for the class

- **Double Art** (#131-134; max rank 4): nearly every Wolf skill calls `getDoubleArt()` at its start. In this scope that
  is crusader `:21344`, artCancel `:27617`, counter2 `:28680`, darkEdge `:30887`, artBreaker `:34146`, mirrorBlade `:34807`
  and dualBrand `:36665`. The call rolls `Random.Range(0, 100) < lckAdjust(4 x 6)` (24% plus luck, `Wolf.cs:8235-8300`).
  On a proc, `RPC_doubleArt` instantiates `doubleArt` (ready) at the hero, plus `sublimeArt_ring` (ready) when Sublime Art
  #431 is learned (`:18411-18459`). It is a weighted random proc, which "a|b" can't express: it needs a chance value, or a
  "nothing" alternative. The pilot's cues leave it out. I left it out here too, for consistency.

## Recipe problems I hit

1. **Voice and sound names can clash** (above). Nothing in the recipe or in `wardrobe_fx.py` warns about it. Recipe step 3
   should say: check that a voice name doesn't also exist under `sounds/`.
2. **The inventory misses prefabs that aren't `Resources.Load` lines in `<Class>.cs`.** It misses inspector fields
   (`dust_forward`, `counter_hit`, `artCancel_hit`) and status effects spawned by `CharacterControl.cs` (the Dark Edge
   hand aura). The recipe should say to grep `Instantiate(this.<field>` too and to look up the status's add handler in
   `CharacterControl.cs` for a self-buff.
3. **The cue format can't express several things the game does:** a spawn rotation (Crusader / Law Bringer:
   `rotation * Euler(270, 90, 0)`), a bone attachment held for a status duration (Dark Edge), a weighted random proc
   (Double Art), and camera effects (Art Cancel and Art Breaker motion blur, the Mirror Blade white flash). The recipe
   should say how to record these: "left out: needs <cue feature>"?
4. **`YieldDefault(n)` isn't explained.** It means wait one frame (a per-frame poll loop, as in Counter's stance). The
   recipe explains only `Yield(n, WaitForSeconds(x))`.
5. **Other passives that change a skill** (Law Bringer for Crusader; Sublime Art adds `sublimeArt_ring` to Double Art):
   "max rank" covers a skill's own rank but doesn't say whether other passives are assumed learned.
6. **The "needs a target point" exception is unclear** for ranged single-target strikes (Art Breaker, Mirror Blade), whose
   only strike visual is the `_hit` at the target.
7. **The dash is ignored without the recipe saying so.** Effects spawned at the hero mid-dash (Dual Brand's slashes,
   Crusader) get distance 0 because the wardrobe hero stands still. That is the pilot's convention (Feral Strike), but the
   recipe doesn't state it.
8. **Sequence tiles reset the cue clock.** `fxStart` sets `FX.t = 0` and replaces `FX.cues` at every step
   (`index.html:3223-3226`). So a first-clip cue timed after the step switch is dropped silently, and a first-clip
   followState effect's cut (`cutAt`) is compared against the next clip's clock. Nothing in this scope hits it today: the
   counter1 / mirrorCounter1 cues are all at or before 0.2 s and not followState. It could matter for future cues on
   multi-clip tiles, and the recipe's "cues belong to the clip they start with" doesn't warn about it.
9. **One clip, two skills:** `darkEdge` is also Holy Armor's clip. Cues keyed by clip can't hold both, and the recipe
   doesn't say what to do.
