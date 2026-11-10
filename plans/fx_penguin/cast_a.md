# Penguin effects + sounds research: the Cast tile (cast1, cast2, cast3), first 8 cast3 skills

Researcher `cast_a`, 2026-11-10 (office PC). Scope: `RPC_cast1` (the cast channel) and the cast3 pool members for Mana
Missile, Mana Burn, Falling Comets, Mana Vortex, Meteora, Frozen Blast, Arctic Wind, Ice Shield. `cast_b` writes the
other members of the cast3 pool (Ice Block, Snow Man, Tornado, Typhoon, Absolute Zero, Blizzard, Snow Ball, Cosmic Rift;
Cosmic Friday has its own tile). Research only (recipe steps 1-3). Line numbers are
`C:\Users\Jump\Desktop\12tails\DecompiledSource\Penguin.cs` unless another file is named. Times are seconds from the
start of the clip the cue is keyed by. Distance 0 = at the hero.

Read-only probes, in `checks\fx_penguin_research\cast_a\` (nothing they run writes outside that folder):
- `cond.sh` gives a condensed view of a line range, with the opaque predicates removed.
- `probe.py` lists each effect's parts, EffectControl, AudioSource and Animation clips through `wardrobe_fx.effect()` in
  memory (output: `probe.txt`).
- `probe_fields.py` reads the Penguin hero MonoBehaviour's serialized fields; `probe_collider.py` its CharacterController;
  `probe_vortex.py` the Mana Vortex summon prefab.
- `missile_sim.py` flies Mana Missile's 7 missiles to the ground at the 10 m point (times, landing points, spawn rots).
- `entries.py` builds and JSON-checks the entries below (output: `entries.txt`).

Max rank and passives on: Mana Missile 4 + More Missile #402 (7 missiles), Mana Burn 2 + Mana Surge #432, Falling Comets
2 + Giant Star #442 (8 comets), Mana Vortex 3, Meteora 2, Frozen Blast 4 + Frozen Break #403, Arctic Wind 3 + Deadly
Frost #413, Ice Shield 4, Double Spell #431 (`12t_reference/penguin-skill-reference.md` :12-25, :578-608).
`lckAdjust(12)` at the page's stats = 12 % (own_skills.md, its header: 12 x 1.01 = 12.12; 1212 / 100.12 = 12.1 -> 12).

---

## Read this first

1. **Missing part not in the inventory: `manaMissile_fire` needs `Penguin_manaMissile`.** `castRing`, `castEffect`,
   `manaMissile_fire`, `manaMissile_hit` and the sound `manaMissile_fire` are inspector fields of the hero prefab
   (`probe_fields.py`: fields 5-9 point at `penguin/effects/castEffect`, `castRing`, `manaMissile_fire`,
   `sounds/manaMissile_fire`, `effects/manaMissile_hit`), never `Resources.Load`ed, so `plans/fx_inventory.md` doesn't
   list them. `wardrobe_fx.py penguin` finds them by name. Their parts (probe):
   - `castRing`: Animation (create 0.47 s, root, destroy), SkinnedMeshRenderer, EffectControl (life 60, afterLife 0.5,
     followPosition, followState), AudioSource `cast` (looped, playOnAwake). **Ready.**
   - `castEffect`: EffectControl (life 1, afterLife 1), ImageEmitter, AudioSource `castEffect`. **Ready.**
   - `manaMissile_hit`: EffectControl (life 1), ImageEmitter, AudioSource `manaMissile_hit`. **Ready.**
   - `manaMissile_fire`: ProjectileControl (built for the Sheep), **Penguin_manaMissile** (not built), TrailRenderer,
     legacy particles. Penguin_manaMissile is the homing mover: 12 m/s (`Penguin_manaMissile.cs:26`), every 0.1 s
     `RotateTowards(forward, target - pos, 0.15 rad)` (`:125-128`), destroyed on any trigger that is not its own layer or
     layer 1 / 2 (`:193-211`), so on the floor too; it reports the hit at `ClosestPointOnBounds` (`:223-238`). The part
     reads the cue's `to` as the target (as the Sheep's movers do, NOTES.md "the Sheep's effects: built and cued").
   This is a 7th Penguin part for the parts stage (the inventory names six).
2. **Missing part: the Mana Vortex summon.** Mana Vortex spawns a summon, not an effect:
   `Resources.Load("GameAssets/Characters/Elementals/ManaVortex/ManaVortex")` (:10421). Its prefab (`probe_vortex.py`):
   CharacterController, CharacterControl, ManaVortex, Animation (`root`, `create`, `destroy`), AudioSource `manaVortex`
   (looped), children BoltEmitter (**not built**: in `EMITTERS` but not in `BUILT`, `pipeline/wardrobe_fx_inventory.py:23-32`),
   LineEmitter, RingEmitter, SkinnedMeshRenderer `manaVortex_tri`. Needs: `wardrobe_fx.py` to find it under
   `characters/elementals/manavortex/` (the same fallback own_skills.md asks for `novaFlare`, its item 1), the BoltEmitter
   part, and its clip switch (`create` at spawn, `root` looped after 1 s, ManaVortex.cs:1048-1073, :973-978; `destroy`
   when it goes, :763). Cued as `"fx", "manaVortex"`.
3. **Missing part (page cue option): `spread` for the comets.** Each Giant Star comet lands at the target point +
   `(Random.Range(-10, 10), 0, Random.Range(-10, 10))` (:26288), whole metres -10 to +9 on each axis. The cue options
   have no random offset (`cueOf`, `index.html:3467-3471`), so the cues carry `"spread": [-10, 9]` (a whole-metre
   offset, drawn per cue at `fxStart`, on x and d separately). Until the page reads it, every comet lands on the 10 m
   point (unknown options are ignored, nothing breaks). Each comet also faces `LookRotation(flat(spot - hero))` (:26305,
   :37625): the same part can turn it.
4. **Double Spell is the Penguin's Free Cast, but only on 5 of these 8.** `RPC_cast1` rolls it once when the bar ends
   (`hasSkill(431)`, `isDoubleSpell`, no `multiCast` yet, `Random.Range(0, 100) < lckAdjust(12)`, :20100-20144): the
   `multiCast` flash at the hero (:20138) and the status `multiCast` Lv 1 for 3 s (:20144). `isDoubleSpell` is set for
   Mana Missile, Mana Burn, Falling Comets, Frozen Blast, Arctic Wind (:19546, :19568, :19590, :19646, :19668) and Ice
   Block (cast_b), never for Mana Vortex, Meteora, Ice Shield (reset :19520). The skill's own coroutine then spends it at
   its multiCast check and **reruns itself once** (no second bar, no second roll: the rerun starts the coroutine
   directly, e.g. :10018-10021), saying `multiCast` (its voice timer is still running). Cued as own_skills.md did for
   Blink / Falling Stars: roll `doubleSpell` p 0.12, the rerun's voice and effects on the same roll, **the clip not
   restarted** (the game Rewinds and replays cast3: own_skills.md question 1) and no purple tint (its question 3).
   The `multiCast` effect is a field loaded only by `RPC_multiCast` (:9832-9838): BB draws nothing on a proc until a
   Double / Triple Cast was cast once. Cued anyway (passives on), as own_skills.md did.
5. **Name collisions** (voices/ vs sounds/ vs effects/):
   - `cast`: `voices/cast.wav` is cast1's voice; `sounds/cast.wav` is castRing's own looping sound. Different recordings;
     the cue is `"voice"` (file `v_cast`), the ring's sound comes with the effect.
   - `manaMissile_fire`: an effect prefab and `sounds/manaMissile_fire.wav` (the field `manaMissile_Fx`, played by
     `RPC_manaMissile_fire` itself, :10258). Cued as both kinds, `"fx"` and `"sound"`.
   - `multiCast`: an effect (its own sound is `sounds/trippleCast`) and `voices/multiCast.wav` (the rerun's line); voices/
     also has `multiCast1-3` (Double / Triple Cast's, not these).
   - Effects whose own sound has another name: `manaSurge` plays `sounds/manaBurn`, `frozenBreak` plays
     `sounds/frozenBlast`, `deadlyFrost` plays `sounds/arcticWind`, `giantComet` plays `sounds/fallingComet`. No cue
     names those sounds. Every `"voice"` cue below is in `voices/`, and every voice file exists (no TTO fix needed).
6. **SEQ: no step-time error.** `"Cast: cast1 cast2*@0 cast3"` matches the code: cast1 (0.7 s clip,
   `data/penguin/clips.json`) is replaced by cast2 at 0.2 + 0.5 = 0.7 s (:20902, :20907, :19446), cast2 starts with a cut
   (`PlayAnimation("cast2", 0)` :19446, no `~`), and all eight skills cut into cast3 (`Rewind()` + `PlayAnimation("cast3",
   0)`, e.g. :21338-21341, so no `~`; the Sheep's is `cast3~` because hers fades 0.2). The first step's 0.2 fade is the
   game's `PlayAnimation("cast1", 0.2f)` (:19884).
7. **Late cues and the loop toggle.** cast3 is 1.03 s long, but Meteora (1.4, 2.6 s), the comets (to 3.05 s) and the
   missile hits (to 2.32 s) come later. By default a skill tile plays once and the cues run on in the idle tail
   (`play(idleName(), true)`, `index.html:1167`). With the skill tab's วนซ้ำ on, the next round's `fxDue` fires the cues
   not yet reached at the step end (`index.html:1168`), so they bunch at 1.03 s. That is page behaviour shared with every
   class, not a cue problem.
8. **Ice Shield's size (verified 2026-11-10).** The shield is scaled `Clamp(mChar.radius + 0.4, 0.5, 2)`
   (CharacterControl.cs:38626). `mChar` is the hero's Unity `CharacterController` (`public CharacterController mChar;`,
   CharacterControl.cs:29789), so `radius` is the prefab's serialized `m_Radius: 0.3` (Penguin.prefab:684): 0.3 + 0.4 =
   0.7.
9. **Mana Vortex is spawned by the server's echo.** `RPC_manaVortex_cast` sends `RPC_manaVortex_create` only as an
   ActionEvent (:27162-27170), with no local call, so the vortex appears a network delay after 0.4 s. Cued at 0.4.
10. **TTO1102 matches BB on every name in scope**: `TTO1102:Penguin.<RPC_cast1>d__170::MoveNext@0x1de4d00`
    (pseudo/Penguin.c:5481-6763: `cast1` 0.2 fade, voice `cast`, `cast2`, `root`, the same skill list plus TTO's
    `iceBreaker`, for cast_b); `<RPC_manaMissile_cast>d__173@0x1df7a40`, `<RPC_manaBurn_cast>d__183@0x1df61c0`,
    `<RPC_fallingComets_cast>d__190@0x1deb860`, `<RPC_manaVortex_cast>d__193@0x1df8b00`, `<RPC_meteora_cast>d__197@0x1df9750`,
    `<RPC_frozenBlast_cast>d__199@0x1df0660`, `<RPC_arcticWind_cast>d__202@0x1dc57f0`, `<RPC_iceShield_cast>d__207@0x1df4a30`:
    the same voices (manaSurge / manaBurn, frozenBreak / frozenBlast, deadlyFrost / arcticWind, multiCast) and clip
    `cast3`. Only string literals and the annotated float constants were compared: TTO's Falling Comets shows 0.2 / 0.5 /
    12 but no 0.15 / 0.4 among its annotated constants (they may be unannotated). BB is the authority; not followed further.
11. **No game bug in scope.** One oddity, it changes no cue: Mana Missile's and Mana Burn's "say multiCast instead"
    timer is 3 s (:21382-21386, :24291-24295), the other three's 12 s (:26470-26474, :29036-29040, :30159-30163); a
    fresh cast always says its own line (the cooldowns are longer), so only the rerun says `multiCast`.

---

## cast1: RPC_cast1, the cast channel

- **Coroutine:** `$RPC_cast1$26057`, :19251-20930. Started with the skill's name (`sType`) for 17 BB skills; it
  dispatches each one's `RPC_<skill>_cast` at :20158-20869 (the 8 here: :20170, :20225, :20285, :20334, :20366, :20415,
  :20441, :20473).
- **Timeline:**

| t (s) | state | what | source |
|---|---|---|---|
| 0 | 0 | cast time / cooldown per skill (:19505-19869), `actionState attack`, `myCommand cast` | :19495-19505 |
| 0 | 0 | `PlayAnimation("cast1", 0.2f)`, Once | :19884-19889 |
| 0 | 0 | voice `Voices/cast` (one file, PlayOneShot 1 for the local player) | :19939-19951 |
| 0 | 0 | Meteora only: its point = the target's position now (no target: 20 m ahead) | :20008-20046 |
| 0 -> 0.2 | | `Yield(2, 0.2)` | :20902 |
| 0.2 | 2 | `castRing` at the hero, hero position and rotation (`createEffect`) | :19419 |
| 0.2 -> 0.7 | | `Yield(3, 0.5)` | :20907 |
| 0.7 | 3 | `cast2` looped (cut); the ring's `root` looped; `castTime = now + mCastTime`, the cast bar | :19446-19475 |
| 0.7+ | 4 | every frame: face the target; when the bar ends: the Double Spell roll (above), then `RPC_<skill>_cast` | :20052-20869, :20899 |

- Sums: 0.2 + 0.5 = 0.7 (= cast1's 0.7 s clip).
- **The handover:** the `_cast` coroutine sets `myCommand = "<skill>"` (e.g. :21329), so the followState castRing goes to
  its after-life (0.5 s) at cast3's start (EffectControl.cs:122-247; the page plays its `destroy` clip there, NOTES.md
  "the Sheep's effects: built and cued"). On the page that is the step edge 0.7 s. Cued `cut: 0.65` for the reason the
  Sheep's is 0.55 (plans/fx_sheep/cast_a.md, Read this first 2: the page restarts FX.t at each step).
- No `rot`: the Penguin's ring spawns with the hero's rotation (the Sheep's had Euler(270, 90, 0)).
- Nothing left out: no other effect is spawned in the channel.

## cast2: no entry

The loop of the cast bar (the page holds it 0 s). Nothing spawns in it: facing the target and the bar only.

## cast3: the shared pool (`skills`), 8 members here

Common skeleton (each member's lines are in its `why`):
- At 0: `actionState attack`, `myCommand <skill>`, `animation.Rewind()` + `PlayAnimation("cast3", 0)` (cut, Once), the
  voice `<voice>1|<voice>2` (`Random.Range(0, 2)`, voices/), and, for the 5 Double Spell skills, the `multiCast` flash
  rolled at the bar's end (the same frame).
- `Yield(2, 0.4)`; at 0.4: `castEffect` at `position + TransformDirection(0, 1, 1)`, hero rotation (= `d 1, y 1`) and
  the skill's fire.
- Then the multiCast check (Double Spell skills) and standby.

Per skill, max rank:

| Skill | Coroutine | Waits after 0.4 | Check / standby (s) | Its own effect | Wardrobe |
|---|---|---|---|---|---|
| Mana Missile 4 + #402 | :20980-21534 | 0.1 (:21530), 0.3 (:21506) | 0.5 / 0.8 (:21235, :21288) | 7 homing missiles from 1 m up 1 m ahead (:21169), `Sounds/manaMissile_fire` (:10258), hits where they land | missiles flown to the ground at the 10 m point (decision 3 by analogy) |
| Mana Burn 2 + #432 | :24017-24520 | 0.1 (:24512), 0.3 (:24509) | 0.5 / 0.8 (:24137, :24197) | `manaSurge` at the target (:24758-24770) | 10 m |
| Falling Comets 2 + #442 | :26065-26615 | 0.15 x 8 (:26589) | 1.6 / 1.6 (:26164, :26221) | 8 `giantComet` at the target + spread (:26288, :37615-37625) | 10 m + spread |
| Mana Vortex 3 | :27088-27383 | 0.3 (:27376) | - / 0.7 (:27197) | the summon 5 m ahead (:27133, :10421) | 5 m |
| Meteora 2 | :27917-28189 | 0.4 (:28177) | - / 0.8 (:28002) | ring at once, meteor +1.0, hit +2.2 (:28533, :28360, :28424; waits :28574, :28567) | 10 m |
| Frozen Blast 4 + #403 | :28754-29258 | 0.1 (:29221), 0.3 (:29253) | 0.5 / 0.8 (:28882, :28942) | `frozenBreak` x 1.8 at the target (:29641-29650) | 10 m |
| Arctic Wind 3 + #413 | :29912-30385 | 0.2 (:30349), 0.2 (:30363) | 0.6 / 0.8 (:30005, :30065) | `deadlyFrost` at `TransformDirection(0, 1, 1.2)`, once (:30751) | 1.2 m ahead, 1 m up |
| Ice Shield 4 | :31038-31382 | 0.4 (:31360) | - / 0.8 (:31173) | the iceShield status's look on the receiver (CharacterControl.cs:38619-38638) | self-cast (decision 1 by analogy) |

Sums (cast3 clock):
- Mana Missile: 0.4 + 0.1 = 0.5 (check), + 0.3 = 0.8 (standby). Rerun from 0.5: voice 0.5, fire 0.5 + 0.4 = 0.9,
  standby 0.5 + 0.8 = 1.3. Mana Burn and Frozen Blast the same (check 0.5, standby 0.8; rerun fire 0.9).
- Falling Comets: comets at 0.4 + 0.15 k, k = 0..7 = 0.4, 0.55, 0.7, 0.85, 1.0, 1.15, 1.3, 1.45; the 8th wait ends at
  1.45 + 0.15 = 1.6 (check, else standby). Rerun from 1.6: voice 1.6, castEffect 1.6 + 0.4 = 2.0, comets 2.0 ... 3.05.
- Arctic Wind: 0.4 + 0.2 = 0.6 (check), + 0.2 = 0.8 (standby). Rerun from 0.6: fire 0.6 + 0.4 = 1.0.
- Mana Vortex: 0.4 + 0.3 = 0.7 (standby).
- Meteora: ring 0.4, meteor 0.4 + 1.0 = 1.4, hit 1.4 + 1.2 = 2.6, damage 2.6 + 0.4 = 3.0; standby 0.4 + 0.4 = 0.8.
- Ice Shield: 0.4 + 0.4 = 0.8 (standby).

**Mana Missile's volley** (`RPC_manaMissile_fire` :10087-10258): 4 + 1 + 2 = 7 missiles (:10087, :10099), yaw
-72 + 24 i (:10199-10215), each `LookRotation(fireDir) x Euler(-0.2 |yaw|, yaw, 0)` (:10220), life 3 s (:10235).
`fireDir` aims at the target's collider centre (:21174); at the 10 m ground point it pitches 6.34 deg down from the
fire point. `missile_sim.py` (FixedUpdate 0.02 s) gives each missile's spawn `rot` and where its 0.3 m sphere meets the
floor: yaw 0 at 0.54 s after the fire, 7.44 m ahead; +-24 at 0.58 s, (+-0.23, 7.84); +-48 at 0.90 s, (+-1.61, 10.93);
+-72 at 1.42 s, (+-3.01, 15.06). `manaMissile_hit` at each contact, hero rotation (:10281-10286). Hit cue times = 0.4 +
those (0.94, 0.98, 1.3, 1.82), rerun 0.9 + those (1.44, 1.48, 1.8, 2.32).

**Mana Vortex's spot:** `getSpawnVector(hero + 2 up, 5 forward - 2 up)` (:27133): the 4 m ray (Math.cs:1224) covers
3.71 m forward and ends 0.51 m above flat ground with no hit, so `getSpawnPos(hero + 5 forward)` (Math.cs:1237) = 5 m
ahead on the floor; `getExpandPos` keeps a free spot (:27144). Scale 0.4 + 0.2 x 3 = 1.0 (ManaVortex.cs:1045), identity
(:10431), life `chaAdjust(60)` (:10513).

**Ice Shield's look:** `Instantiate(Effects/iceShield)` at `collider.bounds.center` (the CharacterController centre y
0.6), parented to the hero, scale 0.7 (Read this first 8) (CharacterControl.cs:38623-38638). It has no EffectControl; it
goes when the status ends (`Find("iceShieldFx")` + Destroy, CharacterControl.cs:17417-17430), after `chaAdjust(30)` =
30 s (:31124). Its Animation `root` loops (probe: wrap 2).

### What is left out, per skill (only "on an enemy" / "needs an attacker")
- Mana Burn: the `manaBurn` status, on the enemy (it draws nothing anyway: MP and damage, CharacterControl.cs:38572-38590).
- Falling Comets: the hits 0.6 s after each comet (:37531-37596), on enemies. (The player's motion blur, :26430-26435, is
  a camera effect, not an effect prefab.)
- Meteora: the damage at 3.0 s, on enemies. (The camera shake and white ramp, :28391-28401, :28442, are camera effects.)
- Frozen Blast: the `ice` status and `Sounds/iceBreak` on an already iced enemy (:29506-29582), on an enemy.
- Arctic Wind: `frost` / `ice` and `Sounds/iceBreak` (:30603-30677), on an enemy.
- Mana Missile, Mana Vortex, Ice Shield: nothing.

### The entries (cast1 and the cast3 pool's 8 members; the editor merges cast_b's members into `skills`)

Generated and JSON-checked by `checks/fx_penguin_research/cast_a/entries.py` (sheep.json layout, one cue per line).

```json
  "cast1": {
    "why": "Penguin.cs RPC_cast1 (:19251-20930), the cast channel the dispatcher starts for every cast-time skill (17 BB skills, :20158-20869, Cosmic Friday among them in its own tile): at 0: clip cast1 (0.2 fade, :19884) and voice cast (Voices/cast, one file, :19939-19951; voices/cast.wav, not sounds/cast.wav); Yield 0.2 (:20902): castRing at the hero, hero position and rotation (:19419; the prefab field castRing = Resources penguin/effects/castRing; EffectControl life 60 + afterLife 0.5, followState; plays its own looping Sounds/cast); Yield 0.5 (:20907): cast2 looped and the ring's root clip at 0.7 s (:19446-19461), then the cast bar (:19466-19475; the page: none) and the skill's RPC_<skill>_cast, which sets myCommand: the ring's followState cut at the step edge 0.7 s (EffectControl.cs:122-247), cued 0.65 because the page restarts FX.t at each step (as the Sheep's 0.55)",
    "cues": [
    [0, "voice", "cast"],
    [0.2, "fx", "castRing", {"cut": 0.65}]
    ]
  },
  "cast3": {
    "why": "The cast3 clip after the RPC_cast1 channel: 16 Penguin skills (Penguin.cs :21341 ... :38888), one per play, even chance, picked anew on every play; Cosmic Friday plays cast3 after the channel too, in its own tile (:39555)",
    "skills": {
      "manaMissile": {
        "why": "Penguin.cs RPC_manaMissile_cast (:21108-21534, enemy target: the 10 m target point): Double Spell #431 on (passives on): RPC_cast1 rolls Random.Range(0, 100) < lckAdjust(12) = 12 % when the bar ends (:20100-20144; lckAdjust CharacterControl.cs:20658-20670, LCK 1), draws multiCast at the hero (:20138; the field is loaded only by RPC_multiCast :9838, so BB and TTO show it only after a Double / Triple Cast) and adds multiCast Lv 1 for 3 s (:20144; its purple tint, CharacterControl.cs:38470-38475, left out: own_skills.md question 3); one roll per play, shared by the repeat's cues: roll doubleSpell; the repeat restarts cast3 in the game (Rewind + PlayAnimation), not on the page (own_skills.md question 1); at 0: clip cast3 cut (Rewind + PlayAnimation(cast3, 0), :21338-21341), voice manaMissile1 / manaMissile2 (Random.Range(0, 2), :21389-21448, PlayOneShot :21501 / :21527; Voices/multiCast instead within 3 s of the last, :21382-21386, :21463); Yield 0.4 (:21514): castEffect at TransformDirection(0, 1, 1), hero rotation (:21137; the prefab field castEffect, plays its own Sounds/castEffect) and RPC_manaMissile_fire from 1 m up 1 m ahead at the target (:21169-21179): rank 4 + More Missile #402 = 7 missiles (:10087-10099), yaw -72 + 24 i, each LookRotation(fireDir) x Euler(-0.2|yaw|, yaw, 0) (:10105-10220; fireDir to the ground point pitches 6.34 deg down; checks/fx_penguin_research/cast_a/missile_sim.py gives each rot), Sounds/manaMissile_fire (the field manaMissile_Fx, :10258); Penguin_manaMissile flies 12 m/s and turns 0.15 rad per 0.1 s toward to (Penguin_manaMissile.cs ctor, FixedUpdate; life 3 s, :10235) and dies on the floor, manaMissile_hit at the contact, hero rotation (OnTriggerEnter -> RPC_manaMissile_hit :10281-10286): sim times 0.54 / 0.58 / 0.90 / 1.42 s after the fire; Yield 0.1 (:21530): the multiCast check at 0.5 s (:21235-21248): the repeat RPC_manaMissile_multiCast starts the coroutine again (:10018-10021: clip, voice multiCast, the volley at 0.9) and this one ends with no standby; else Yield 0.3 (:21506): standby 0.8 s (:21288)",
        "cues": [
        [0, "fx", "multiCast", {"p": 0.12, "roll": "doubleSpell"}],
        [0, "voice", "manaMissile1|manaMissile2"],
        [0.4, "fx", "castEffect", {"d": 1, "y": 1}],
        [0.4, "sound", "manaMissile_fire"],
        [0.4, "fx", "manaMissile_fire", {"d": 1, "y": 1, "rot": [-12.36, -70.57, -6.17], "to": [0, 0, 10]}],
        [0.4, "fx", "manaMissile_fire", {"d": 1, "y": 1, "rot": [-5.33, -47.38, -4.73], "to": [0, 0, 10]}],
        [0.4, "fx", "manaMissile_fire", {"d": 1, "y": 1, "rot": [0.99, -23.91, -2.57], "to": [0, 0, 10]}],
        [0.4, "fx", "manaMissile_fire", {"d": 1, "y": 1, "rot": [6.34, 0.0, 0.0], "to": [0, 0, 10]}],
        [0.4, "fx", "manaMissile_fire", {"d": 1, "y": 1, "rot": [0.99, 23.91, 2.57], "to": [0, 0, 10]}],
        [0.4, "fx", "manaMissile_fire", {"d": 1, "y": 1, "rot": [-5.33, 47.38, 4.73], "to": [0, 0, 10]}],
        [0.4, "fx", "manaMissile_fire", {"d": 1, "y": 1, "rot": [-12.36, 70.57, 6.17], "to": [0, 0, 10]}],
        [0.5, "voice", "multiCast", {"p": 0.12, "roll": "doubleSpell"}],
        [0.9, "fx", "castEffect", {"d": 1, "y": 1, "p": 0.12, "roll": "doubleSpell"}],
        [0.9, "sound", "manaMissile_fire", {"p": 0.12, "roll": "doubleSpell"}],
        [0.9, "fx", "manaMissile_fire", {"d": 1, "y": 1, "rot": [-12.36, -70.57, -6.17], "to": [0, 0, 10], "p": 0.12, "roll": "doubleSpell"}],
        [0.9, "fx", "manaMissile_fire", {"d": 1, "y": 1, "rot": [-5.33, -47.38, -4.73], "to": [0, 0, 10], "p": 0.12, "roll": "doubleSpell"}],
        [0.9, "fx", "manaMissile_fire", {"d": 1, "y": 1, "rot": [0.99, -23.91, -2.57], "to": [0, 0, 10], "p": 0.12, "roll": "doubleSpell"}],
        [0.9, "fx", "manaMissile_fire", {"d": 1, "y": 1, "rot": [6.34, 0.0, 0.0], "to": [0, 0, 10], "p": 0.12, "roll": "doubleSpell"}],
        [0.9, "fx", "manaMissile_fire", {"d": 1, "y": 1, "rot": [0.99, 23.91, 2.57], "to": [0, 0, 10], "p": 0.12, "roll": "doubleSpell"}],
        [0.9, "fx", "manaMissile_fire", {"d": 1, "y": 1, "rot": [-5.33, 47.38, 4.73], "to": [0, 0, 10], "p": 0.12, "roll": "doubleSpell"}],
        [0.9, "fx", "manaMissile_fire", {"d": 1, "y": 1, "rot": [-12.36, 70.57, 6.17], "to": [0, 0, 10], "p": 0.12, "roll": "doubleSpell"}],
        [0.94, "fx", "manaMissile_hit", {"d": 7.44}],
        [0.98, "fx", "manaMissile_hit", {"d": 7.84, "x": -0.23}],
        [0.98, "fx", "manaMissile_hit", {"d": 7.84, "x": 0.23}],
        [1.3, "fx", "manaMissile_hit", {"d": 10.93, "x": -1.61}],
        [1.3, "fx", "manaMissile_hit", {"d": 10.93, "x": 1.61}],
        [1.44, "fx", "manaMissile_hit", {"d": 7.44, "p": 0.12, "roll": "doubleSpell"}],
        [1.48, "fx", "manaMissile_hit", {"d": 7.84, "x": -0.23, "p": 0.12, "roll": "doubleSpell"}],
        [1.48, "fx", "manaMissile_hit", {"d": 7.84, "x": 0.23, "p": 0.12, "roll": "doubleSpell"}],
        [1.8, "fx", "manaMissile_hit", {"d": 10.93, "x": -1.61, "p": 0.12, "roll": "doubleSpell"}],
        [1.8, "fx", "manaMissile_hit", {"d": 10.93, "x": 1.61, "p": 0.12, "roll": "doubleSpell"}],
        [1.82, "fx", "manaMissile_hit", {"d": 15.06, "x": -3.01}],
        [1.82, "fx", "manaMissile_hit", {"d": 15.06, "x": 3.01}],
        [2.32, "fx", "manaMissile_hit", {"d": 15.06, "x": -3.01, "p": 0.12, "roll": "doubleSpell"}],
        [2.32, "fx", "manaMissile_hit", {"d": 15.06, "x": 3.01, "p": 0.12, "roll": "doubleSpell"}]
        ]
      },
      "manaBurn": {
        "why": "Penguin.cs RPC_manaBurn_cast (:24017-24520, enemy target: the 10 m target point): Double Spell #431 on (passives on): RPC_cast1 rolls Random.Range(0, 100) < lckAdjust(12) = 12 % when the bar ends (:20100-20144; lckAdjust CharacterControl.cs:20658-20670, LCK 1), draws multiCast at the hero (:20138; the field is loaded only by RPC_multiCast :9838, so BB and TTO show it only after a Double / Triple Cast) and adds multiCast Lv 1 for 3 s (:20144; its purple tint, CharacterControl.cs:38470-38475, left out: own_skills.md question 3); one roll per play, shared by the repeat's cues: roll doubleSpell; the repeat restarts cast3 in the game (Rewind + PlayAnimation), not on the page (own_skills.md question 1); at 0: clip cast3 cut (:24247-24250), Mana Surge #432 on: voice manaSurge1 / manaSurge2 (:24298-24361; else manaBurn1 / manaBurn2 :24367-24426; Voices/multiCast within 3 s, :24291-24295, :24441); Yield 0.4 (:24500): castEffect at TransformDirection(0, 1, 1) (:24049) and RPC_manaBurn_fire at the target (:24081): with #432 manaSurge at the target's position (tChar.createEffect, :24746-24770; else manaBurn :24789-24807; plays its own Sounds/manaBurn), at the target point, drawn in the hero's facing (the target's rotation, APPROXIMATED); the manaBurn status 0.3 s later (:24705) draws nothing (CharacterControl.cs:38572-38590); Yield 0.1 (:24512): the multiCast check at 0.5 s (:24137-24157): the repeat (:10340-10343) restarts it; else Yield 0.3 (:24509): standby 0.8 s (:24197)",
        "cues": [
        [0, "fx", "multiCast", {"p": 0.12, "roll": "doubleSpell"}],
        [0, "voice", "manaSurge1|manaSurge2"],
        [0.4, "fx", "castEffect", {"d": 1, "y": 1}],
        [0.4, "fx", "manaSurge", {"d": 10}],
        [0.5, "voice", "multiCast", {"p": 0.12, "roll": "doubleSpell"}],
        [0.9, "fx", "castEffect", {"d": 1, "y": 1, "p": 0.12, "roll": "doubleSpell"}],
        [0.9, "fx", "manaSurge", {"d": 10, "p": 0.12, "roll": "doubleSpell"}]
        ]
      },
      "fallingComets": {
        "why": "Penguin.cs RPC_fallingComets_cast (:26065-26615, enemy target: the 10 m target point): Double Spell #431 on (passives on): RPC_cast1 rolls Random.Range(0, 100) < lckAdjust(12) = 12 % when the bar ends (:20100-20144; lckAdjust CharacterControl.cs:20658-20670, LCK 1), draws multiCast at the hero (:20138; the field is loaded only by RPC_multiCast :9838, so BB and TTO show it only after a Double / Triple Cast) and adds multiCast Lv 1 for 3 s (:20144; its purple tint, CharacterControl.cs:38470-38475, left out: own_skills.md question 3); one roll per play, shared by the repeat's cues: roll doubleSpell; the repeat restarts cast3 in the game (Rewind + PlayAnimation), not on the page (own_skills.md question 1); at 0: clip cast3 cut (:26391-26394), voice fallingComet1 / fallingComet2 (:26477-26524; Voices/multiCast within 12 s, :26470-26474, :26551); Yield 0.4 (:26602): castEffect at TransformDirection(0, 1, 1) (:26097), then 2 + 3 x 2 = 8 comets (:26134), one every 0.15 s (Yield :26589) at 0.4, 0.55 ... 1.45 s: Giant Star #442 on: RPC_giantComets_fire (:26282-26310) puts giantComet at the target's position + (Random.Range(-10, 10), 0, Random.Range(-10, 10)), whole metres -10 to +9 on each axis, on the floor (getSpawnPos), LookRotation(flat hero-to-spot) (:37609-37625; it falls from 16 m up, 6 m off along its own facing; plays its own Sounds/fallingComet); hits 0.6 s later draw nothing (:37531-37596); after the 8th Yield 0.15: the multiCast check at 1.6 s (:26164-26182): the repeat (:10375-10378) restarts it, else standby 1.6 s (:26221); the player's motion blur (:26430-26435) is a camera effect",
        "cues": [
        [0, "fx", "multiCast", {"p": 0.12, "roll": "doubleSpell"}],
        [0, "voice", "fallingComet1|fallingComet2"],
        [0.4, "fx", "castEffect", {"d": 1, "y": 1}],
        [0.4, "fx", "giantComet", {"d": 10, "spread": [-10, 9]}],
        [0.55, "fx", "giantComet", {"d": 10, "spread": [-10, 9]}],
        [0.7, "fx", "giantComet", {"d": 10, "spread": [-10, 9]}],
        [0.85, "fx", "giantComet", {"d": 10, "spread": [-10, 9]}],
        [1.0, "fx", "giantComet", {"d": 10, "spread": [-10, 9]}],
        [1.15, "fx", "giantComet", {"d": 10, "spread": [-10, 9]}],
        [1.3, "fx", "giantComet", {"d": 10, "spread": [-10, 9]}],
        [1.45, "fx", "giantComet", {"d": 10, "spread": [-10, 9]}],
        [1.6, "voice", "multiCast", {"p": 0.12, "roll": "doubleSpell"}],
        [2.0, "fx", "castEffect", {"d": 1, "y": 1, "p": 0.12, "roll": "doubleSpell"}],
        [2.0, "fx", "giantComet", {"d": 10, "spread": [-10, 9], "p": 0.12, "roll": "doubleSpell"}],
        [2.15, "fx", "giantComet", {"d": 10, "spread": [-10, 9], "p": 0.12, "roll": "doubleSpell"}],
        [2.3, "fx", "giantComet", {"d": 10, "spread": [-10, 9], "p": 0.12, "roll": "doubleSpell"}],
        [2.45, "fx", "giantComet", {"d": 10, "spread": [-10, 9], "p": 0.12, "roll": "doubleSpell"}],
        [2.6, "fx", "giantComet", {"d": 10, "spread": [-10, 9], "p": 0.12, "roll": "doubleSpell"}],
        [2.75, "fx", "giantComet", {"d": 10, "spread": [-10, 9], "p": 0.12, "roll": "doubleSpell"}],
        [2.9, "fx", "giantComet", {"d": 10, "spread": [-10, 9], "p": 0.12, "roll": "doubleSpell"}],
        [3.05, "fx", "giantComet", {"d": 10, "spread": [-10, 9], "p": 0.12, "roll": "doubleSpell"}]
        ]
      },
      "manaVortex": {
        "why": "Penguin.cs RPC_manaVortex_cast (:27088-27383, no target): no Double Spell roll (isDoubleSpell = false :19520, never set in its branch :19596-19612); at 0: clip cast3 cut (:27247-27250), voice manaVortex1 / manaVortex2 (:27291-27372); Yield 0.4 (:27370): castEffect at TransformDirection(0, 1, 1) (:27120); the spot: getSpawnVector(hero + 2 up, 5 forward - 2 up) (:27133): its 4 m ray ends 0.51 m above flat ground, so getSpawnPos(hero + 5 forward) = 5 m ahead on the floor (Math.cs:1210-1230), getExpandPos keeps a free spot (:27144); RPC_manaVortex_create goes out only as an ActionEvent (:27162-27170; no local call: the server's echo spawns it, a network delay later): RPC_manaVortex_create (:10396-10520) Instantiates the summon Resources Elementals/ManaVortex/ManaVortex (:10421) at the spot, identity (:10431), scale 0.4 + 0.2 x 3 = 1.0, its create clip then root looped after 1 s (ManaVortex.cs:1045-1073, :973), life chaAdjust(60) = 60 s (:10513), cut at 10 s like the Seals (decision 19 by analogy); the summon is not an effect: needs the part ManaVortex summon (wardrobe_fx.py finding it under elementals/manavortex/, its create clip then root looped, its BoltEmitter child); Yield 0.3 (:27376): standby 0.7 s (:27197)",
        "cues": [
        [0, "voice", "manaVortex1|manaVortex2"],
        [0.4, "fx", "castEffect", {"d": 1, "y": 1}],
        [0.4, "fx", "manaVortex", {"d": 5, "kill": 10}]
        ]
      },
      "meteora": {
        "why": "Penguin.cs RPC_meteora_cast (:27917-28189, enemy target: the 10 m target point; the channel stores the target's position at the bar's start, :20008-20046; with no target it would be 20 m ahead, :20040): no Double Spell roll (isDoubleSpell = false :19520, never set in its branch :19613-19629); at 0: clip cast3 cut (:28052-28055), voice meteora1 / meteora2 (:28096-28181); Yield 0.4 (:28172): castEffect at TransformDirection(0, 1, 1) (:27949) and RPC_meteora_fire at the point (:27962): meteora_ring there, identity (:28515-28533; plays its own Sounds/meteora); Yield 1.0 (:28574): meteora at 1.4 s, identity, scale 1.25 at rank 2 (:28342-28373); Yield 1.2 (:28567): meteora_hit at 2.6 s (:28406-28424), with the camera shake and white ramp (:28391-28401, camera effects); Yield 0.4 (:28572): the damage at 3.0 s draws nothing (:28442-28502); case 3 of the cast: Yield 0.4 (:28177): standby 0.8 s (:28002); drawn in the hero's facing (identity, APPROXIMATED)",
        "cues": [
        [0, "voice", "meteora1|meteora2"],
        [0.4, "fx", "castEffect", {"d": 1, "y": 1}],
        [0.4, "fx", "meteora_ring", {"d": 10}],
        [1.4, "fx", "meteora", {"d": 10, "scale": 1.25}],
        [2.6, "fx", "meteora_hit", {"d": 10}]
        ]
      },
      "frozenBlast": {
        "why": "Penguin.cs RPC_frozenBlast_cast (:28754-29258, enemy target: the 10 m target point): Double Spell #431 on (passives on): RPC_cast1 rolls Random.Range(0, 100) < lckAdjust(12) = 12 % when the bar ends (:20100-20144; lckAdjust CharacterControl.cs:20658-20670, LCK 1), draws multiCast at the hero (:20138; the field is loaded only by RPC_multiCast :9838, so BB and TTO show it only after a Double / Triple Cast) and adds multiCast Lv 1 for 3 s (:20144; its purple tint, CharacterControl.cs:38470-38475, left out: own_skills.md question 3); one roll per play, shared by the repeat's cues: roll doubleSpell; the repeat restarts cast3 in the game (Rewind + PlayAnimation), not on the page (own_skills.md question 1); at 0: clip cast3 cut (:28992-28995), Frozen Break #403 on: voice frozenBreak1 / frozenBreak2 (:29043-29106; else frozenBlast1 / frozenBlast2 :29112-29171; Voices/multiCast within 12 s, :29036-29040, :29186); Yield 0.4 (:29245): castEffect at TransformDirection(0, 1, 1) (:28786) and RPC_frozenBlast_fire at the target's position (:28826): with #403 frozenBreak, identity, scale 4 x 0.4 + 0.2 = 1.8 (:29621-29650; else frozenBlast :29671-29696; plays its own Sounds/frozenBlast); the hit 1 s later (:29716, :29431-29608): ice on the enemies hit and Sounds/iceBreak only on an already iced one (:29553-29582), on enemies; Yield 0.1 (:29221): the multiCast check at 0.5 s (:28882-28902): the repeat (:10613-10616) restarts it; else Yield 0.3 (:29253): standby 0.8 s (:28942)",
        "cues": [
        [0, "fx", "multiCast", {"p": 0.12, "roll": "doubleSpell"}],
        [0, "voice", "frozenBreak1|frozenBreak2"],
        [0.4, "fx", "castEffect", {"d": 1, "y": 1}],
        [0.4, "fx", "frozenBreak", {"d": 10, "scale": 1.8}],
        [0.5, "voice", "multiCast", {"p": 0.12, "roll": "doubleSpell"}],
        [0.9, "fx", "castEffect", {"d": 1, "y": 1, "p": 0.12, "roll": "doubleSpell"}],
        [0.9, "fx", "frozenBreak", {"d": 10, "scale": 1.8, "p": 0.12, "roll": "doubleSpell"}]
        ]
      },
      "arcticWind": {
        "why": "Penguin.cs RPC_arcticWind_cast (:29912-30385, no target: a cone ahead): Double Spell #431 on (passives on): RPC_cast1 rolls Random.Range(0, 100) < lckAdjust(12) = 12 % when the bar ends (:20100-20144; lckAdjust CharacterControl.cs:20658-20670, LCK 1), draws multiCast at the hero (:20138; the field is loaded only by RPC_multiCast :9838, so BB and TTO show it only after a Double / Triple Cast) and adds multiCast Lv 1 for 3 s (:20144; its purple tint, CharacterControl.cs:38470-38475, left out: own_skills.md question 3); one roll per play, shared by the repeat's cues: roll doubleSpell; the repeat restarts cast3 in the game (Rewind + PlayAnimation), not on the page (own_skills.md question 1); at 0: clip cast3 cut (:30115-30118), Deadly Frost #413 on: voice deadlyFrost1 / deadlyFrost2 (:30166-30229; else arcticWind1 / arcticWind2 :30235-30294; Voices/multiCast within 12 s, :30159-30163, :30309); Yield 0.4 (:30357): castEffect at TransformDirection(0, 1, 1) (:29944) and RPC_arcticWind_fire at the hero (:29957): with #413 deadlyFrost at TransformDirection(0, 1, 1.2), hero rotation (:30727-30751; else arcticWind :30760-30778; plays its own Sounds/arcticWind); its 8 pulses 0.2 s apart (:30831, :30846) hit enemies only (ice / Arctic Frost #314's frost, Deadly Frost's iceBreak, :30549-30708); Yield 0.2 (:30349): the multiCast check at 0.6 s (:30005-30025): the repeat (:10634-10637) restarts it; else Yield 0.2 (:30363): standby 0.8 s (:30065)",
        "cues": [
        [0, "fx", "multiCast", {"p": 0.12, "roll": "doubleSpell"}],
        [0, "voice", "deadlyFrost1|deadlyFrost2"],
        [0.4, "fx", "castEffect", {"d": 1, "y": 1}],
        [0.4, "fx", "deadlyFrost", {"d": 1.2, "y": 1}],
        [0.6, "voice", "multiCast", {"p": 0.12, "roll": "doubleSpell"}],
        [1.0, "fx", "castEffect", {"d": 1, "y": 1, "p": 0.12, "roll": "doubleSpell"}],
        [1.0, "fx", "deadlyFrost", {"d": 1.2, "y": 1, "p": 0.12, "roll": "doubleSpell"}]
        ]
      },
      "iceShield": {
        "why": "Penguin.cs RPC_iceShield_cast (:31038-31382, ally target: shown as a self-cast, decision 1 by analogy: eSkillTarget.ally, PenguinSkill.cs:1737-1742, and the ally check takes the caster, GameGui.cs:37900-37904): no Double Spell roll (isDoubleSpell = false :19520, never set in its branch :19674-19690); at 0: clip cast3 cut (:31238-31241), voice iceShield1 / iceShield2 (:31282-31371); Yield 0.4 (:31377): castEffect at TransformDirection(0, 1, 1) (:31070) and the iceShield status on the target for chaAdjust(30) = 30 s (:31124-31146), whose apply puts Effects/iceShield at the receiver's collider centre (the Penguin's CharacterController centre y 0.6), parented, scale Clamp(radius 0.3 + 0.4, 0.5, 2) = 0.7 (CharacterControl.cs:38619-38627; mChar is the CharacterController, CharacterControl.cs:29789, m_Radius 0.3, Penguin.prefab:684; plays its own Sounds/iceShield; no EffectControl: it goes when the status ends, CharacterControl.cs:17417-17430: cut at 10 s like the Seals, decision 19 by analogy; the game's 30 s is open question 1); Yield 0.4 (:31360): standby 0.8 s (:31173)",
        "cues": [
        [0, "voice", "iceShield1|iceShield2"],
        [0.4, "fx", "castEffect", {"d": 1, "y": 1}],
        [0.4, "fx", "iceShield", {"y": 0.6, "scale": 0.7, "kill": 10}]
        ]
      }
    }
  }
```

Sure: high for every time, name and distance traced above, Ice Shield's scale too (Read this first 8); medium for the
missile landing points (a simulation of `Penguin_manaMissile`, ground at y 0.3 = its sphere's radius; see Verification).

## Parts the page lacks (effect: part)

- `manaMissile_fire`: **Penguin_manaMissile** (the homing mover: 12 m/s, 0.15 rad toward `to` every 0.1 s, gone when it
  meets the floor; with the built ProjectileControl, TrailRenderer and legacy particles).
- `manaVortex`: **the ManaVortex summon** (`wardrobe_fx.py` reading `characters/elementals/manavortex/ManaVortex`, its
  `create` clip then `root` looped after 1 s, `destroy` at the end) and **BoltEmitter** (its child).
- `giantComet`: **the cue option `spread`** (page: a whole-metre random offset per cue on x and d, and the comet turned
  to face away from the hero, `LookRotation(flat(spot - hero))`).
- Ready as they are: castRing, castEffect, multiCast, manaMissile_hit, manaSurge, giantComet (its own parts),
  meteora_ring, meteora, meteora_hit, frozenBreak, deadlyFrost, iceShield (`probe.txt`).

## What the editor needs, in one list

- Two keys: `cast1`, and `cast3` (a `skills` pool: these 8 + cast_b's). No SEQ change.
- Effects to build: castRing, castEffect, multiCast, manaMissile_fire (Penguin_manaMissile), manaMissile_hit, manaSurge,
  giantComet, manaVortex (summon + BoltEmitter + the elementals folder), meteora_ring, meteora, meteora_hit, frozenBreak,
  deadlyFrost, iceShield.
- Voices (voices/): cast, multiCast, manaMissile1, manaMissile2, manaSurge1, manaSurge2, fallingComet1, fallingComet2,
  manaVortex1, manaVortex2, meteora1, meteora2, frozenBreak1, frozenBreak2, deadlyFrost1, deadlyFrost2, iceShield1,
  iceShield2. Sound (sounds/): manaMissile_fire.
- Roll name `doubleSpell` (12 %), shared with own_skills.md's Blink / Falling Stars (FX.rolls reset per play).

## Questions (only what the Sheep / Wolf decisions don't answer)

1. **Ice Shield's 30 s and Mana Vortex's 60 s.** Both outlast a tile's play by far. Recommended default: cut both at
   10 s (`kill: 10`), as decision 19 cut the Seal fields (60 s+) at 10 s; Ice Shield's look has no EffectControl, so
   without a `kill` it would never go. Other choice: their real 30 s / 60 s, as Lucent Barrier kept its 3 s and Eden
   Sanctuary its 13 s.

## Verification (2026-11-10)

A skeptical re-trace on the office PC (Penguin.cs = `C:\Users\Jump\Desktop\12tails\DecompiledSource\Penguin.cs`).
Probe scripts: `checks/fx_penguin_research/verify/` (`missile_rot.py`, `missile_hits.py`, `tto_probe_cast.json`).

What was checked, independently (and found right):
- **cast1:** `clip_flow.js ... RPC_cast1`. `PlayAnimation("cast1", 0.2f)` :19884, voice `Voices/cast` :19939/:19951,
  `Yield(2, 0.2)` :20902, castRing via createEffect at the hero (position + rotation) :19419, `Yield(3, 0.5)` :20907,
  `PlayAnimation("cast2", 0)` :19446 + the ring's `root` loop :19456-19461. 0.2 + 0.5 = 0.7 = cast1's clip length (0.7 s,
  `wardrobe/data/penguin/clips.json`). EffectControl followState watches both actionState and myCommand
  (EffectControl.cs:137-140, :226-232), so the ring is cut at the skill's start. `cut 0.65` follows the Sheep's rule.
- **Double Spell:** the roll is at :20108-20144 (hasSkill(431), isDoubleSpell, no multiCast status, `Random.Range(0, 100)
  < lckAdjust(12)`), the flash is `sMRLT35VVC` = `Effects/multiCast`, loaded only at :9838. isDoubleSpell = true only for
  manaMissile :19546, manaBurn :19568, fallingComets :19590, frozenBlast :19646, arcticWind :19668, iceBlock :19707
  (checked against each `$switch == "<skill>"` line).
- **The reruns:** each multiCast check starts the coroutine again in the same frame
  (`RPC_manaMissile_multiCast` -> `StartCoroutine(RPC_manaMissile_cast)` :10018-10021; Mana Burn :10340-10343). The old
  coroutine ends (Block_17 -> `return false`). The voice timers are 3 s (:21386, :24295) and 12 s (:26474, :29040,
  :30163), so the rerun says multiCast.
- **Every wait, re-added from the yields:**
  - Mana Missile: Yield 0.4 :21514, 0.1 :21530, 0.3 :21506.
  - Mana Burn: 0.4 :24500, 0.1 :24512, 0.3 :24509.
  - Falling Comets: 0.4 :26602, 0.15 :26589, `i >= 2 + 3 sLv` = 8 :26134.
  - Mana Vortex: 0.4 :27370, 0.3 :27376.
  - Meteora: 0.4 :28172, 0.4 :28177. Its fire: ring, then 1.0 :28574, meteora (x1.25 at sLv 2), then 1.2 :28567,
    meteora_hit, then 0.4 :28572.
  - Frozen Blast: 0.4 :29245, 0.1 :29221, 0.3 :29253. Its scale is sLv x 0.4 + 0.2 = 1.8.
  - Arctic Wind: 0.4 :30357, 0.2 :30349, 0.2 :30363. deadlyFrost at mPos + TransformDirection(0, 1, 1.2) :30751, and
    4 + 4 pulses :30831.
  - Ice Shield: 0.4 :31377, 0.4 :31360.
- **The volley:** 4 + 1 + 2 = 7 missiles and yaw -72 + 24 i (:10036-10258 condensed), life 3 x rangeMod. The seven spawn
  rots were re-derived with my own Unity-convention quaternion code (`verify/missile_rot.py`), and all seven match the
  report's values exactly.
- **Penguin_manaMissile:** 12 m/s :26, the turn `RotateTowards(.., 0.15, 1)` every 0.1 s :125-128.
- **Mana Vortex's spot:** `getSpawnVector` (Math.cs:1210-1237) uses a 4 m ray. The direction (0, -2, 5) gives
  (0, -1.49, 3.71), so the ray ends 0.51 m up with no hit, then getSpawnPos(hero + 5 forward) = 5 m.
  - It goes out only as an ActionEvent (:27170).
  - The prefab is `characters/elementals/manavortex/ManaVortex.prefab` (it exists in the rip).
  - Scale 0.4 + 0.2 nLv (ManaVortex.cs:1041), `create`, then `root` looped after 1 s (ManaVortex.cs:970-978).
  - BoltEmitter is in EMITTERS but not in BUILT (pipeline/wardrobe_fx_inventory.py).
- **Hero prefab fields:** I re-ran `cast_a/probe_fields.py` (read only). Fields 5-9 = castEffect, castRing,
  manaMissile_fire (GameObject), manaMissile_fire (AudioClip), manaMissile_hit. None of them is in
  `plans/fx_inventory.md`'s penguin list, which names six scripts.
- **Targets** (PenguinSkill.cs mode / target):
  - manaMissile, manaBurn, fallingComets, meteora, frozenBlast: target/enemy.
  - arcticWind, manaVortex: instant/enemy (both fire from the hero, so placement is unchanged).
  - iceShield: target/**ally** :1732-1742, applied to tChar :31146. A self-cast by decision 1.
- **Names:** every voice, effect and the `manaMissile_fire` sound exists in the rip.
- **SEQ** `Cast: cast1 cast2*@0 cast3` (index.html:1027): all eight cut into cast3 (`PlayAnimation("cast3", 0)`), so
  no `~` and no step-time error.
- **The idle tail / loop:** index.html:1163-1171 (`seqTick`: the last step in `back` mode goes to idle, otherwise
  `fxDue(S.dur)` fires the cues not reached).
- **TTO:** the coroutine names and RVAs, and Falling Comets' annotated constants (0.01, 0.2, 0.5, 0.75, 1, 12; no 0.15 /
  0.4), are confirmed in `C:\Users\Jump\Desktop\12tails\DecompiledSource_TTO_2026-11-02\pseudo\Penguin.c` (that is the
  file "pseudo/Penguin.c" means). `wardrobe_fx_tto.py penguin --probe castEffect,castRing,multiCast,cosmicFriday`: all
  four exist in TTO's bundles (`verify/tto_probe_cast.json`).

Corrections (old -> new):
1. Read this first 8, Ice Shield's size. **Old:** "Unverified ... I could not find where `CharacterControl.radius` is
   set". **New:** verified. `mChar` is the hero's Unity `CharacterController` (CharacterControl.cs:29789 `public
   CharacterController mChar;`), so its radius is the serialized `m_Radius: 0.3` (Penguin.prefab:684), and the scale
   0.7 stands. The "Sure" line and the iceShield `why` were updated to match.
2. The iceShield `why`. **Old:** "the game's 30 s is open question 2". **New:** "open question 1". The report has only one
   question. (The same text is still in `checks/fx_penguin_research/cast_a/entries.py` and `entries.txt`, which this check
   did not edit. Paste from this report.)

No timing, name, distance or SEQ error was found.

Unresolved (not disproved, not fixed):
- **Where the missiles aim.** The game aims each missile at the target's `collider.bounds.center` (:21174;
  Penguin_manaMissile.cs:128). For a Penguin-sized target that point is 0.6 m up (the CharacterController centre). This
  report aims at the floor point (0, 0, 10), so the middle missiles land short (7.4-7.8 m). With the aim at 0.6 m up,
  they would reach the 10 m target. My rough re-sim (`verify/missile_hits.py`) does not reproduce `missile_sim.py`'s
  landing points exactly either: it gives 0.56 / 0.64 / 0.98 / 1.44 s against 0.54 / 0.58 / 0.90 / 1.42 s. The editor
  should decide between "the floor at 10 m" (decision 3 by analogy) and "the target, 0.6 m up", and the parts stage
  should check the simulation.
- **Mana Burn's manaSurge rotation.** manaSurge is drawn with the target's rotation (:24770), and this report uses the
  hero's facing. cast_b.md uses `rot [0, 180, 0]` (a target facing the hero) for the same case (snowMan_ring,
  snowBall_cast). Pick one convention for both.
