# Sheep effects + sounds research: Normal Attack, Charge Attack, emotes, basic moves

Scope: clips nAttack1, nAttack2, nAttack3, cAttack1, cAttack0, cAttack2 (RPC_nAttack1-3, RPC_cAttack1 / 2 / 0 and the
dispatchers `doNormalAttack`, `doBeginCharge`, `doReleaseCharge`), then the emotes (RPC_emotion) and ko (RPC_ko, RPC_dead).
Research only (recipe steps 1-3). Line numbers are `C:\Users\Jump\Desktop\12tails\DecompiledSource\Sheep.cs` unless
another file is named. Times are seconds from the start of the clip the cue is keyed by. Distance 0 = at the hero.

Prefab facts come from a read-only probe (`wardrobe_fx.py sheep --probe cAttack_charge,cAttack_ring,deadEffect,nAttack,cAttack,homingLight`;
nothing written to the data). Voice / sound files were checked in the rip
(`RippedAssets\...\heroes\sheep\{voices,sounds,effects}`) and in BB's ResourceManager (`12TailsOnline_Data\mainData`).

---

## Read this first

1. **SEQ is wrong for Normal Attack.** The game starts nAttack2 at **0.7 s** after stage 1, not 0.8. It starts nAttack3 at
   **1.5 s**; the page plays it at 1.8 s (0.8 + nAttack2's full 1.0 s clip). The fix is in index.html (not a cue job):
   `"Normal Attack: nAttack1@0.7 nAttack2^@0.8 nAttack3"`. Details are in the dispatcher section below. Charge Attack's
   `cAttack1@0.8 cAttack0*~@4 cAttack2` is right: 0.8 and the crossfades match the code. 4 s is a held time the code allows.
2. **The Sheep has no KO or dead voices in BB.** `RPC_ko` / `RPC_dead` load `Voices/ko1`, `ko2`, `dead1`, `dead2`
   (:46478, :46509, :46841, :46872). None of them is in the rip's `voices/` or in mainData's ResourceManager (the
   `heroes/sheep/voices/*` paths it lists have no ko / dead). So the game logs "Cannot find ko1 voice" and stays silent.
   Don't cue them: `wardrobe_fx.py` would report them missing. The only KO cue is `deadEffect` (question 3).
3. **cAttack2's voice is always cAttack1 in BB.** Both branches of `Random.Range(0, 2)` load `Voices/cAttack1` (:19322-19378).
   `voices/cAttack2.wav` exists but BB never plays it. TTO fixed this: TTO1102:Sheep.<RPC_cAttack2>d__155::MoveNext@0x1E7F3B0
   loads cAttack1 or cAttack2 at random (question 2).
4. **Name collisions (the cue kind picks the folder):**
   - `sleep`: `voices/sleep.wav` is the emote. `sounds/sleep.wav` is the Sleep skill's sound. `voices/sleep1` / `sleep2` are
     the Sleep skill's voices. The sleep emote cue is `"voice"` (file `v_sleep`).
   - `cAttack_ring` is both an effect (the ring at the feet, no AudioSource) and a sound. The sound is played by the
     **cAttack_charge** prefab's own AudioSource (play-on-awake, clip `cAttack_ring`), so it comes with that effect and needs no cue.
   - `nAttack`: the effect is the ball (left out), and `sounds/nAttack` is the shot sound the hero's code plays (cued as `"sound"`).
     The voices `nAttack1-3` are in `voices/` only.
   - `cAttack`: the effect is the charged ball (left out), and `sounds/cAttack` is the release sound (cued). The voice
     `cAttack1` is in `voices/` only.
5. **Charge effects are mission / arena only.** The game draws `cAttack_charge` and `cAttack_ring` only when `Game.mGameType > 4`
   (:18686). The Wolf's charge rings had the same gate and were kept, so they are kept here too.
6. **The charge ball's size comes from ATK.** Every 0.1 s the game rewrites the ball's emitter `minSize` / `maxSize` from the
   hero's ATK and Benediction rank (:18952-18957). The page has no cue option for an emitter's size over time (question 4).
7. **deadEffect is left out on the Wolf too.** `RPC_dead` spawns `deadEffect` at the hero (Sheep :46903-46913; Wolf.cs:46037),
   and the Wolf's `ko` entry has no effect. If the user wants it for the Sheep, the Wolf should match.
8. Nothing in this scope sits at the hero except voices, two sounds and the charge's two effects. Every projectile and hit
   is left out: the balls need ProjectileControl (not built), and the hits are on the target.

---

## The dispatcher: Normal Attack stage times (SEQ check)

`doNormalAttack` (:9016-9280):

- **Stage 2:** accepted while `myCommand == "nAttack1"`, with Combo #101, and only when
  `actionTime + 0.3 < Time.time < actionTime + 0.7` (`:9154` breaks if `<= +0.3`, `:9162` breaks if `>= +0.7`). It then starts
  `RPC_nAttack2` (:9170).
- **Stage 3:** accepted while `myCommand == "nAttack2"`, with #102, once `Time.time > actionTime + 1` (:9218). It then starts
  `RPC_nAttack3` (:9226). The window closes at nAttack2's standby, 1.5 s (:17986).
- Neither stage resets `actionTime`: case 0 of RPC_nAttack2 / 3 sets only `actionState` and `myCommand` (:18038-18041,
  :18483-18486). So `actionTime` stays stage 1's start, and each stage waits until a fixed time after it:
  - RPC_nAttack2: `Yield(2, actionTime - Time.time + 0.7)` (:18060). The press always comes before 0.7, so **the nAttack2
    clip always starts at 0.7 s**.
  - RPC_nAttack3: `Yield(2, actionTime - Time.time + 1.5)` (:18496). The press comes between 1.0 and 1.5, so **the nAttack3
    clip always starts at 1.5 s**.
- Stage 1's own standby at 0.8 s (:17445-17457) checks `myCommand == "nAttack1"`, so it is skipped once stage 2 is pressed.
  Stage 2's standby (:17974-17986) checks `"nAttack2"`, so it is skipped once stage 3 is pressed.

Step lengths: nAttack1 runs 0 to 0.7 (0.7 s), nAttack2 runs 0.7 to 1.5 (0.8 s), and nAttack3 plays to its standby at 0.8 s
(its clip is 1.0 s, `data/sheep/clips.json`). The fades match the SEQ: nAttack1 `animation.Play` is a cut (:17530),
nAttack2 `PlayAnimation(.., 0.1f)` is `^` (:17814), and nAttack3 `PlayAnimation(.., 0)` is a cut (:18259).

**Proposed SEQ:** `"Normal Attack: nAttack1@0.7 nAttack2^@0.8 nAttack3"`. Today's `@0.8` came from the skill details.
nAttack2 has no `@`, so the page plays its whole 1.0 s clip and nAttack3 starts 0.3 s late. None of the cues below depend
on this: each one is timed from its own clip.

## The dispatcher: Charge Attack (SEQ check)

- `doBeginCharge` (:9440-9522): from standby or run, with #111, it starts `RPC_cAttack1` (:9510).
- `doReleaseCharge` (:9539-9677): while `myCommand == "cAttack1"`:
  - if `actionTime + 2 <= Time.time` (:9585), it starts `RPC_cAttack2` (:9623 / :9644);
  - otherwise it starts `RPC_cAttack0` (:9665), a fizzle: no clip change, standby 1 s later (:19596-19622).
- `cAttack1@0.8` is right: `Yield(2, 0.8)` (:18970), then `PlayAnimation("cAttack0", 0.2f)` looped (:18676-18681). The 0.2 s
  fade is SEQ's `~`. `cAttack2` is a cut (`PlayAnimation("cAttack2", 0)`, :19287), as in SEQ.
- `@4` on cAttack0: the code has no fixed "full charge". With the SEQ's numbers:
  - held time = 0.8 + 4 = 4.8 s, which passes the 2 s minimum;
  - charge count = `floor(Time.time − actionTime − 1.3)` at the shot (:9807); the shot is 0.5 s after the release, so
    floor(4.8 + 0.5 − 1.3) = floor(4.0) = **4**;
  - the damage cap at rank 4 is 100 × 4 = 400 (:9810). It is reached when (1 + 0.2 × 3) × 4 × ATK ≥ 400, i.e. ATK ≥ 62.5
    (Benediction rank 3).

  So 4 s is a full charge for any real max-level Sheep. Keep it.

---

## nAttack1 (Normal Attack, stage 1)

- Coroutine `RPC_nAttack1` (`$RPC_nAttack1$27685`, :17230-17620).

| t (s) | what | source |
|---|---|---|
| 0 | clip nAttack1 (cut), `addTimeOut("nAttack", 2)`, voice `Voices/nAttack1` (1.0 own hero, 0.75 others); wait 0.5 | :17521-17606, `Yield(2, 0.5)` :17612 |
| 0.5 | the shot, own client only (`isMine`, :17368) and out of town (`mGameType > 3`, :17376); fire point 1 m up and 0.3 m ahead (`TransformDirection(0, 1, 0.3)`, :17384). With Homing Light #401: `RPC_homingLight_fire` (:17394-17400), else `RPC_nAttack_fire` (:17422). Others see it through `ActionEvent`. Both play `Sounds/nAttack` at volume 0.7 (homingLight :11534-11544; nAttack :9363-9373); wait 0.3 | `Yield(3, 0.3)` :17610 |
| 0.8 | standby, only if no stage 2 was pressed | :17445-17457 |

- Sums: shot at 0 + 0.5 = 0.5 s; standby at 0.5 + 0.3 = 0.8 s.
- Passive: Homing Light #401 changes the ball (the user's passives rule: on). It doesn't change the timing or the sound.
- Left out:
  - `homingLight` (or `nAttack` without the passive): needs ProjectileControl, Sheep_homingLight (nAttack: ProjectileControl,
    Sheep_nAttack). The game spawns it at the hero (1 m up, 0.3 m ahead). It flies 12 m/s for 1.7 s, about 20.4 m (the
    reference). Future cue: `[0.5, "fx", "homingLight", {"d": 0.3, "y": 1}]`, aimed at the 10 m target point. The game aims it
    at `tDir − (0, 1, 0.3)`, slightly down toward a ground target.
  - `nAttack_hit` and a second `Sounds/nAttack` (0.7) when the ball lands. Both are at the target (`RPC_nAttack_hit`,
    :9393-9419, called from `Sheep_nAttack.cs:201` / `Sheep_homingLight.cs:239`).

```json
  "nAttack1": {
    "why": "Sheep.cs RPC_nAttack1: clip (animation.Play, :17530) and voice nAttack1 at 0 (:17571, :17606); 0.5 s (Yield(2, 0.5) :17612) the shot, Homing Light #401 on (the passives rule): RPC_homingLight_fire (:17394-17400; RPC_nAttack_fire without it, :17422), both play Sounds/nAttack at 0.7 (:11534-11544, :9363-9373), out of town only (mGameType > 3, :17376); standby 0.8 s (Yield(3, 0.3) :17610, :17457) unless stage 2 is pressed; left out: homingLight 1 m up 0.3 m ahead (:17384, :11445) needs ProjectileControl, Sheep_homingLight (nAttack: ProjectileControl, Sheep_nAttack); nAttack_hit and the hit's Sounds/nAttack at the target (:9393-9419)",
    "cues": [
    [0, "voice", "nAttack1"],
    [0.5, "sound", "nAttack", {"vol": 0.7}]
    ]
  },
```

Sure: high.

## nAttack2 (stage 2)

- Coroutine `RPC_nAttack2` (`$RPC_nAttack2$27696`, :17656-18063). It is started by a press 0.3-0.7 s into stage 1, and its clip
  starts at stage 1 + 0.7 s (`Yield(2, actionTime − now + 0.7)`, :18060).

| t (s, from its clip) | what | source |
|---|---|---|
| 0 | clip nAttack2 (`PlayAnimation(.., 0.1f)`), voice `Voices/nAttack2`; wait 0.5 | :17809-17861, PlayOneShot :18057, `Yield(3, 0.5)` :18055 |
| 0.5 | the shot, as in stage 1 (:17897-17964: isMine, `mGameType > 3`, #401 → homingLight); `Sounds/nAttack` 0.7; wait 0.3 | `Yield(4, 0.3)` :18051 |
| 0.8 | standby, unless stage 3 is pressed | :17974-17996 |

- Sums: shot at 0.5 s (stage 1 + 1.2 s); standby at 0.8 s (stage 1 + 1.5 s).

```json
  "nAttack2": {
    "why": "Sheep.cs RPC_nAttack2 (its clip 0.7 s after stage 1: Yield(2, actionTime - now + 0.7) :18060; the press window 0.3-0.7 s, doNormalAttack :9154-9170): clip (0.1 s fade, :17814) and voice nAttack2 at 0 (:17861, :18057); 0.5 s (Yield(3, 0.5) :18055) the shot, Homing Light on (:17923-17929), Sounds/nAttack at 0.7 (:11544); standby 0.8 s (Yield(4, 0.3) :18051, :17986) unless stage 3 is pressed; left out: homingLight 1 m up 0.3 m ahead (:17913) needs ProjectileControl, Sheep_homingLight; nAttack_hit at the target",
    "cues": [
    [0, "voice", "nAttack2"],
    [0.5, "sound", "nAttack", {"vol": 0.7}]
    ]
  },
```

## nAttack3 (stage 3)

- Coroutine `RPC_nAttack3` (`$RPC_nAttack3$27707`, :18101-18509). It is started by a press 1.0-1.5 s into stage 1, and its clip
  starts at stage 1 + 1.5 s (:18496).

| t (s, from its clip) | what | source |
|---|---|---|
| 0 | clip nAttack3 (cut), voice `Voices/nAttack3`; wait 0.5 | :18254-18306, PlayOneShot :18500, `Yield(3, 0.5)` :18502 |
| 0.5 | the shot (:18342-18409, #401 → homingLight :18374), `Sounds/nAttack` 0.7; wait 0.3 | `Yield(4, 0.3)` :18507 |
| 0.8 | standby | :18418-18441 |

- Sums: shot at 0.5 s (stage 1 + 2.0 s); standby at 0.8 s (stage 1 + 2.3 s).

```json
  "nAttack3": {
    "why": "Sheep.cs RPC_nAttack3 (its clip 1.5 s after stage 1: Yield(2, actionTime - now + 1.5) :18496; the press from 1.0 s, doNormalAttack :9218-9226): clip (cut, :18259) and voice nAttack3 at 0 (:18306, :18500); 0.5 s (Yield(3, 0.5) :18502) the shot, Homing Light on (:18368-18374), Sounds/nAttack at 0.7 (:11544); standby 0.8 s (Yield(4, 0.3) :18507, :18431); left out: homingLight 1 m up 0.3 m ahead (:18358) needs ProjectileControl, Sheep_homingLight; nAttack_hit at the target",
    "cues": [
    [0, "voice", "nAttack3"],
    [0.5, "sound", "nAttack", {"vol": 0.7}]
    ]
  },
```

---

## cAttack1 (Charge Attack: the wind-up)

- Coroutine `RPC_cAttack1` (`$RPC_cAttack1$27718`, :18547-18984).
- At 0: `actionTime = now`, `myCommand "cAttack1"`, `addTimeOut("cAttack", 1)` (:18792-18812), clip cAttack1 with a 0.2 s fade
  (:18827). The voice is `Random.Range(0, 2) == 0` ? `Voices/charge1` : `Voices/charge2` (:18868-18912, PlayOneShot :18981 /
  :18974). It plays for the own hero, or a teammate in missions (:18837-18861). Then it waits 0.8 s (`Yield(2, 0.8)`, :18970).
- At 0.8: it cuts to cAttack0 (below). No effect in cAttack1 itself.

```json
  "cAttack1": {
    "why": "Sheep.cs RPC_cAttack1: clip (0.2 s fade, :18827) and voice charge1 / charge2 (Random.Range(0, 2), :18868-18981) at 0; at 0.8 s (Yield(2, 0.8) :18970) it changes to the looped cAttack0 (:18676), whose cues hold the charge",
    "cues": [
    [0, "voice", "charge1|charge2"]
    ]
  },
```

Sure: high.

## cAttack0 (Charge Attack: the held charge)

- Same coroutine, case 2 (:18663-18780). It plays at cAttack1 + 0.8 s, and only while `actionState "attack"` and
  `myCommand "cAttack1"` (:18664-18670).
- At 0 (its own clip): `PlayAnimation("cAttack0", 0.2f)`, loop (:18676-18681). Then, **only when `mGameType > 4`** (:18686):
  - `cAttack_charge` created 2.7 m above the hero (`position + 2.7f * Vector3.up`, :18698-18710);
  - `cAttack_ring` created at the hero (:18730-18742).

  Out of missions there is no ball (`mChargeAttack` null), so the coroutine ends (:18759-18763).
- From 0 on, every 0.1 s (`Yield(3, 0.1)`, :18972) while the charge holds, the game rewrites the ball's emitter sizes
  (:18952-18957). t is counted from cAttack1's start. ATK is the hero's attack, B the Benediction rank, L the Charge Attack
  rank:
  - `minSize = clamp((t − 0.7) × k, 0, 0.4 L (1 + 0.2 O) − 0.3)`
  - `maxSize = clamp((t − 0.4) × k, 0.3, 0.4 L (1 + 0.2 O))`
  - `k = ATK × 0.25 × (0.01 + 0.0015 B)`
  - O = `hasSkill(462)` (:18779), which BB never has (Bible `sheep-skill-reference.md:291`), so O = 0.

  At L 4 and B 3: k = 0.003625 × ATK, so the full size is 1.3-1.6. That is reached by the page's release at t = 4.8 when
  (4.8 − 0.4) × k ≥ 1.6, i.e. ATK ≥ 101 (1.6 / (4.4 × 0.003625) = 100.3). The prefab's own size is 0.3-0.5 (probe).
- Prefabs (probe):
  - `cAttack_charge`: **ready**. EllipsoidParticleEmitter + child emitter, EffectControl life 60, afterLife 0.7,
    followPosition, **followState**. Its AudioSource plays `Sounds/cAttack_ring` on awake, looped (the clip is 4.0 s;
    the page plays an effect's sound once, which about fills the page's 4 s hold).
  - `cAttack_ring`: **ready**. EffectControl life 180, afterLife 1, followPosition, **followState**; one ImageEmitter image,
    Life 1.
- **The followState cut:** EffectControl ends the effect when `actionState` **or** `myCommand` changes (EffectControl.cs:194-232).
  The release changes `myCommand` to `"cAttack3"` (RPC_cAttack2, :19275), or to `"cAttack0"` on a fizzle (:19602). So both
  effects end at the release, the end of this step: 4 s on the page. Following the Blade Surge precedent in wolf.json
  (`cut` 2.55 because the page's step ends there and `FX.t` restarts with the next step), the cut is **3.95**.

```json
  "cAttack0": {
    "why": "Sheep.cs RPC_cAttack1 case 2 (the change to cAttack0, looped, 0.8 s in: :18676-18681): cAttack_charge 2.7 m above the hero (position + 2.7 up, :18698-18710; plays its own Sounds/cAttack_ring) and cAttack_ring at the hero (:18730-18742), mission / arena only (mGameType > 4, :18686); both followState (EffectControl.cs:194-232): they end at the release, when RPC_cAttack2 sets myCommand cAttack3 (:19275): cut 3.95, the page's step ends at 4 s; the game regrows the ball's particles from ATK every 0.1 s (:18952-18957, full size 1.3-1.6 at rank 4), the page keeps the prefab's 0.3-0.5",
    "cues": [
    [0, "fx", "cAttack_charge", {"y": 2.7, "cut": 3.95}],
    [0, "fx", "cAttack_ring", {"cut": 3.95}]
    ]
  },
```

Sure: high on the trace and the cut. The ball's size on the page is unchecked (question 4).

## cAttack2 (Charge Attack: the release)

- Coroutine `RPC_cAttack2` (`$RPC_cAttack2$27729`, :19025-19409), started by `doReleaseCharge` after a hold of at least 2 s (:9585).

| t (s) | what | source |
|---|---|---|
| 0 | `myCommand "cAttack3"` (ends the charge's followState effects), clip cAttack2 (cut); voice `Voices/cAttack1` (both random branches load cAttack1); wait 0.5 | :19272-19287, :19322-19404, `Yield(2, 0.5)` :19399 |
| 0.5 | `Sounds/cAttack` at 1.0 (always, before the isMine check); own client: `RPC_cAttack` at `mPos + 3 up` (others by `ActionEvent`); wait 0.5 | :19163-19181, :19195-19226, `Yield(3, 0.5)` :19395 |
| 1.0 | standby | :19235-19252 |

- Sums: shot at 0 + 0.5 = 0.5 s; standby at 0.5 + 0.5 = 1.0 s (the clip is 2.0 s and plays on to its end on the page).
- `RPC_cAttack` (:9780-9890): damage from the held time (:9807-9810), then `Instantiate(cAttack, firePos, LookRotation(dir))`
  with ProjectileControl life 5 × rangeMod, homing on the clicked target (:9829-9872). It plays no sound of its own.
- Passive: White Burst #411 changes only the impact (+100 damage and a 6 m splash, `Sheep_cAttack.cs:268-330`), at the target.
- Left out:
  - `cAttack`: needs ProjectileControl, Sheep_cAttack. It spawns 3 m above the hero, then flies 8 m/s toward the target.
    Future cue: `[0.5, "fx", "cAttack", {"y": 3}]`.
  - `cAttack_hit` (`RPC_cAttack_hit`, :9902-9937) and `whiteBurst_hit` (:11564): both at the target.

```json
  "cAttack2": {
    "why": "Sheep.cs RPC_cAttack2 (doReleaseCharge after at least 2 s held, :9585): clip (cut, :19287) and voice cAttack1 at 0 (both Random.Range(0, 2) branches load Voices/cAttack1, :19322-19404; TTO1102 picks cAttack1 / cAttack2); 0.5 s (Yield(2, 0.5) :19399) Sounds/cAttack at full volume (:19169-19181) and the shot 3 m up (RPC_cAttack :19203-19213); standby 1.0 s (Yield(3, 0.5) :19395, :19247); left out: cAttack (Instantiate :9829) needs ProjectileControl, Sheep_cAttack; cAttack_hit and White Burst's whiteBurst_hit at the target (:9902-9937, :11564)",
    "cues": [
    [0, "voice", "cAttack1"],
    [0.5, "sound", "cAttack"]
    ]
  },
```

Sure: high.

---

## Emotes and basic moves

`RPC_emotion` (`$RPC_emotion$28246`, :40348-41200). It works exactly as the Wolf's:

- The voice plays at 0, **before** the clip (:40579-40658). The gates: voice option on (:40580); more than 2 s since the last
  action (`Time.time > actionTime + 2`, :40586); the own hero, or a teammate in missions (:40592-40615).
  - `emo_chat` → `Voices/chat` + `Random.Range(1, 6)`, i.e. chat1-5 (:40638).
  - Every other `emo_<name>` → `Voices/<name>` (`Substring(4)`, :40646), and `PlayOneShot` (:40658) only if the file loads.
- Then the clip, with a 0.2 s fade. No effect and no Sounds/ anywhere in RPC_emotion.

| emote | clip | voice file (voices/) | source |
|---|---|---|---|
| emo_hi, emo_wave | wave | hi / wave | :40694, :40702 → :41144 |
| emo_ty, emo_bow | bow | ty / bow | :40712, :40719 → :41130 |
| emo_laugh | laugh | laugh | :40726-40732 |
| emo_sit | sit | none (silent) | :40746-40752 |
| emo_sleep | sleep | sleep (not `sounds/sleep`, not `sleep1/2`) | :40758-40764 |
| emo_cheer | cheer | cheer | :40770-40776 |
| emo_beg | beg | beg | :40782-40788 |
| emo_cry | cry | cry | :40794-40800 |
| emo_talk, emo_chat | talk | talk: none; chat: chat1-5 | :40808, :40815 → :41108 |
| emo_pose | pose5 / 15 / 25 / 35 / 45 / 58 / 65 / 46 / 66 by the worn set, else pose | none (silent) | :40822-41068 |
| emo_battle | battle | battle | :41078-41084 |
| emo_dance | dance | none (silent) | :41093-41101 |

- In the rip's `voices/`: hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle and chat1-5 all exist. There is no sit,
  talk, pose or dance.
- The TTO-only emote clips (clap, cooking, fishingSheep, mining, planting, pose37, wai) are not in BB's switch: silent.
- The other emote-looking voices (beware, bye, come, follow, giveup, go, paper, rock, scissor, sorry, this, what) belong to
  no tile here. `emo_rock` / `emo_paper` / `emo_scissors` exist in GameGui (:2750-2774), but RPC_emotion's switch gives them
  no clip. Not traced further.
- `RPC_ko` (`$RPC_ko$28415`, :46219-46565): clip ko (:46433), voice ko1 / ko2 (:46468-46562; **the files don't exist**), then
  getUp after 3 s (`Yield(2, 3)` :46546, :46335).
- `RPC_dead` (`$RPC_dead$28422`, :46597-46947): clip ko (:46794), voice dead1 / dead2 (:46829-46888; **the files don't exist**),
  then **always** `deadEffect` at the hero position and rotation (:46896-46913). The voice gate jumps to IL_1A, which is still
  the effect. `deadEffect`: **ready**; EffectControl life 3, no followState; an image 0.8 m up and a ring, both after 0.5 s
  (probe).
- getUp, walk, run, falling, root: nothing (no RPC of theirs plays a voice or an effect in this scope).

The common `why` prefix, as in wolf.json:

```json
  "wave": {
    "why": "Sheep.cs RPC_emotion (:40348): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:40646, PlayOneShot :40658; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_hi (:40694) and emo_wave (:40702) both play the wave clip (:41144): voice hi or wave",
    "cues": [
    [0, "voice", "hi|wave"]
    ]
  },
  "bow": {
    "why": "Sheep.cs RPC_emotion (:40348): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:40646, PlayOneShot :40658; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_ty (:40712) and emo_bow (:40719) both play the bow clip (:41130): voice ty or bow",
    "cues": [
    [0, "voice", "ty|bow"]
    ]
  },
  "laugh": {
    "why": "Sheep.cs RPC_emotion (:40348): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:40646, PlayOneShot :40658; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_laugh (:40726-40732)",
    "cues": [
    [0, "voice", "laugh"]
    ]
  },
  "sleep": {
    "why": "Sheep.cs RPC_emotion (:40348): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:40646, PlayOneShot :40658; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_sleep (:40758-40764): voices/sleep (not sounds/sleep, the Sleep skill's sound, nor its voices sleep1 / sleep2)",
    "cues": [
    [0, "voice", "sleep"]
    ]
  },
  "cheer": {
    "why": "Sheep.cs RPC_emotion (:40348): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:40646, PlayOneShot :40658; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_cheer (:40770-40776)",
    "cues": [
    [0, "voice", "cheer"]
    ]
  },
  "beg": {
    "why": "Sheep.cs RPC_emotion (:40348): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:40646, PlayOneShot :40658; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_beg (:40782-40788)",
    "cues": [
    [0, "voice", "beg"]
    ]
  },
  "cry": {
    "why": "Sheep.cs RPC_emotion (:40348): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:40646, PlayOneShot :40658; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_cry (:40794-40800)",
    "cues": [
    [0, "voice", "cry"]
    ]
  },
  "talk": {
    "why": "Sheep.cs RPC_emotion (:40348): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:40646, PlayOneShot :40658; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_chat (:40815) plays the talk clip (:41108) with chat1-5 at random (Random.Range(1, 6), :40638); emo_talk (:40808) plays it silent (no Voices/talk): the tile takes the chat's voice",
    "cues": [
    [0, "voice", "chat1|chat2|chat3|chat4|chat5"]
    ]
  },
  "battle": {
    "why": "Sheep.cs RPC_emotion (:40348): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:40646, PlayOneShot :40658; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_battle (:41078-41084): voice battle; the battle stance in a fight plays the clip silent: the tile takes the emote's voice",
    "cues": [
    [0, "voice", "battle"]
    ]
  },
  "ko": {
    "why": "Sheep.cs RPC_ko (:46219) and RPC_dead (:46597) both play the ko clip (:46433, :46794); their voices ko1 / ko2 / dead1 / dead2 (:46478-46509, :46841-46872) are not in BB's data (rip voices/ and mainData have none: silent in the game); RPC_dead always puts deadEffect at the hero (:46896-46913; EffectControl life 3), RPC_ko nothing (getUp after 3 s, :46546): one of the two at random, even chance",
    "cues": [
    [0, "fx", "deadEffect", {"p": 0.5}]
    ]
  }
```

The `ko` entry depends on question 3. If it is answered "no effect", drop the entry: the Sheep has nothing to cue on KO.

---

## Left out, needing a part

- `homingLight`: needs ProjectileControl, Sheep_homingLight (all three nAttack stages, Homing Light on; the plain `nAttack`
  needs ProjectileControl, Sheep_nAttack).
- `cAttack`: needs ProjectileControl, Sheep_cAttack (cAttack2).
- The `cAttack_charge` growth: needs a cue part that sets an emitter's min / max size over time (cAttack0). See question 4.

Left out as target-side (no part would bring them in): `nAttack_hit` + its `Sounds/nAttack`, `cAttack_hit`, `whiteBurst_hit`.

## Open questions for the user

1. **Normal Attack SEQ:** change it to `nAttack1@0.7 nAttack2^@0.8 nAttack3`, as the code has it (stage 2 at 0.7 s, stage 3 at
   1.5 s)? Today the page plays stage 2 at 0.8 s and stage 3 at 1.8 s.
2. **Charge release voice:** BB always says cAttack1 (both random branches load the same file: a copy slip). TTO picks cAttack1
   or cAttack2. Keep BB's (`"cAttack1"`) or use the fixed pick (`"cAttack1|cAttack2"`)?
3. **The KO tile:** the Sheep has no KO voices in BB. Add `deadEffect` (RPC_dead's effect at the hero) on half the plays,
   since the ko clip is shared by KO and death? Or leave KO with nothing? The Wolf has the same `deadEffect` (Wolf.cs:46037)
   and its `ko` entry leaves it out. Whatever is chosen should apply to both.
4. **The charge ball's size:** the game grows it from ATK to its full size (particles 1.3-1.6 at rank 4), reached at
   t = 0.4 + 1.6 / k s after cAttack1 starts (k = 0.003625 × ATK): 4.8 s at ATK 101, 2.6 s at ATK 200, 1.9 s at ATK 300.
   The page would draw the prefab's 0.3-0.5. Accept the smaller ball for now (a "needs part" note), or try the cue's
   `scale` option (about ×3.2)? Whether `scale` changes legacy particle sizes on the page has not been checked.

## Offer for the Bible

The reference's Combo section says only "a timed press". The press windows (stage 2 at 0.3-0.7 s, stage 3 from 1.0 s), the
fixed clip starts at 0.7 / 1.5 s, and the shots at 0.5 / 1.2 / 2.0 s (:9154-9226, :18060, :18496) are new findings. So are the
missing KO / dead voices and the cAttack1-only release voice. Offer them to the user for `sheep-skill-reference.md`.

## Verification (2026-11-10)

A second checker re-traced every claim a cue depends on, from the decompile, the rip and a fresh read-only probe
(`wardrobe_fx.py sheep --probe ...`, output in `checks\fx_sheep_research\verify\probe.json` and `probe_summary.txt`).

**Checked and holding:**
- **Normal Attack times.** These come from `clip_flow.js` on RPC_nAttack1/2/3 plus the opaque predicates worked by hand.
  - nAttack1: clip at 0 (:17530), voice (:17606), `Yield(2, 0.5)` (:17612), the shot in case 2 (:17384-17435), `Yield(3, 0.3)` (:17610), standby only if `myCommand == "nAttack1"` (:17444-17457). So 0 / 0.5 / 0.8.
  - nAttack2 / 3: entry sets only `actionState` and `myCommand`, then `Yield(2, actionTime − now + 0.7 / 1.5)` (:18060, :18496; the nAttack3 predicates at :18484-18488 go the normal way). Then the clip, voice, `Yield(3, 0.5)` (:18055 / :18502), the shot, `Yield(4, 0.3)` (:18051 / :18507) and standby (:17986 / :18431).
  - The press windows are `> +0.3`, `< +0.7` (:9154, :9162) and `> +1` (:9218).
  - The page today is `nAttack1@0.8 nAttack2^ nAttack3` (`wardrobe/index.html:1023`), so stage 2 is 0.1 s late and stage 3 is 0.3 s late. The proposed `nAttack1@0.7 nAttack2^@0.8 nAttack3` parses under the SEQ token regex (`index.html:1052`).
- **The shot's sound.** `Sounds/nAttack` at 0.7 in both RPC_nAttack_fire (:9363-9373) and RPC_homingLight_fire (:11534-11544), with the predicates worked out. Homing Light #401 changes only the projectile.
- **Charge Attack.**
  - cAttack1: `Yield(2, 0.8)` (:18970), then `PlayAnimation("cAttack0", 0.2f)` looped (:18676-18681).
  - The two charge effects are `mGameType > 4` only (:18686): cAttack_charge at `position + 2.7 up` with identity rotation (:18710), and cAttack_ring at the hero (:18742).
  - The release needs `actionTime + 2 <= now` (:9585). It sets `myCommand "cAttack3"` (:19275) with a cut clip (:19287). Then the voice, `Yield(2, 0.5)` (:19399), and `Sounds/cAttack` at 1.0 before the isMine check (:19152-19195). Standby comes after `Yield(3, 0.5)` (:19395, :19247).
  - Both random branches load `Voices/cAttack1` (:19332, :19363). TTO1102 `<RPC_cAttack2>d__155` loads voices/cAttack1 or voices/cAttack2 on `Random.Range(0, 2)` (pseudo/Sheep.c:4363-4434).
  - Charge count `floor(t − 1.3)` (:9807), so floor(5.3 − 1.3) = 4. The cap is `100 × (L + O × L)` (:9810), and with B 3 it is reached at ATK ≥ 400 / (1.6 × 4) = 62.5.
- **The followState cut.** EffectControl ends the effect on an `actionState` or `myCommand` change (EffectControl.cs:186-232). The page cuts on `FX.t >= cut` with FX.t reset at each step (`index.html:3160`, `:3417`, and fxStart called once per step, `:1139`), so cut 3.95 is inside the 4 s hold.
- **Rip folders.**
  - voices/ has nAttack1-3, charge1-2, cAttack1-2, hi, wave, ty, bow, laugh, sleep, sleep1-2, cheer, beg, cry, battle and chat1-5.
  - voices/ has no ko1, ko2, dead1, dead2, sit, talk, pose or dance.
  - sounds/ has nAttack (0.59 s), cAttack (1.03 s), cAttack_ring (4.0 s) and sleep.
- **Emotes.** RPC_emotion plays the voice at 0, before the clip (:40580-40658: pvoice, `> actionTime + 2`, own hero or a mission teammate). emo_chat plays chat1-5 (:40638), the rest `Substring(4)` (:40646). Clip lines: :40732-41144. These match the Wolf's entries in wolf.json.
- **ko.**
  - RPC_ko: ko clip (:46433), ko1 / ko2 (:46478, :46509), getUp after 3 s (:46546, :46335), no effect.
  - RPC_dead: dead1 / dead2 (:46841, :46872). The voice gates jump to IL_1A (:46814, :46822), and IL_1A always Instantiates deadEffect at the hero's position and rotation (:46896-46913; the predicate `216627 − 425462 == −208835` holds).
  - deadEffect (probe): EffectControl life 3, no followState; ImageEmitter 0.8 m up and RingEmitter, both Delay 0.5.
  - The Wolf's `ko` entry has no deadEffect (wolf.json), and Wolf.cs:46037 loads it.
- **Prefabs (probe).**
  - cAttack_charge: EC life 60, afterLife 0.7, followState, followPosition.
  - cAttack_ring: EC life 180, afterLife 1, followState; one ImageEmitter, Life 1.
  - Inventory: cattack_charge, cattack_ring and deadeffect are ready. hominglight, nattack and cattack need ProjectileControl (`plans/fx_inventory.md` "sheep").
- **Other.** `RPC_cAttack` life `5 × rangeMod` (:9831). FindRecTarget and the hit functions are target-side, as stated.

**Corrections:**
1. Full ball size at the page's release: "ATK ≥ 100" -> "ATK ≥ 101 (100.3)". (4.8 − 0.4) × 0.003625 × 100 = 1.595 < 1.6 (formula :18957).
2. Question 4: "within about 1-2 s" -> "at t = 0.4 + 1.6 / k: 4.8 s at ATK 101, 2.6 s at ATK 200, 1.9 s at ATK 300". The time depends on ATK, from `maxSize = clamp((t − 0.4) × k, 0.3, 1.6)` (:18957).
3. The size formulas left out the Over Limit term: `0.4 × (L + 0.2 × L × O)` with `O = hasSkill(462)` (:18952, :18957, :18779). BB never has #462 (Bible :291), so the numbers don't change.
4. cAttack_charge's AudioSource is `loop: true` (probe). Added that the clip is 4.0 s and the page plays it once.

None of the 16 cue entries changes.
