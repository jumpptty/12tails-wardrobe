# Penguin effects + sounds research: Normal Attack, Charge Attack, MP Transfer, activateIcon, emotes, basic moves, KO

Scope: clips nAttack1, nAttack2, nAttack3 (RPC_nAttack1-3 and the dispatcher `doNormalAttack`), cAttack1, cAttack2
(RPC_cAttack1, the release RPC_cAttack0, `doBeginCharge`, `doReleaseCharge`), MP Transfer (RPC_mpTransfer, plays nAttack1),
RPC_activateIcon1 (plays cAttack2), then the emotes (RPC_emotion) and KO (RPC_ko, RPC_dead). Research only (recipe steps 1-3).
Line numbers are `C:\Users\Jump\Desktop\12tails\DecompiledSource\Penguin.cs` unless another file is named. Times are seconds
from the start of the clip the cue is keyed by. Distance 0 = at the hero. Every opaque predicate (`if (a - b != c) continue;`)
on the paths below was worked by hand; each one goes the normal way.

Prefab facts come from a read-only probe (`wardrobe_fx.py penguin --probe nAttack_fire,nAttack_hit,spreadShot_fire,cAttack_ring,
manaField_ring,deadEffect,mpTransfer,mpTransfer_ring,castEffect,castRing`; nothing written). The ball geometry is
`checks\fx_penguin_research\attacks_emotes\geom.py` (output `geom.txt`). The hero prefab's fields are read by
`probe_fields.py` (output `probe_fields.txt`): `nAttack_fire`, `nAttack_hit` and `deadEffect` are the prefabs of those names in
`heroes/penguin/effects/`. The rip folders were listed by `voices.py` (output `voices.txt`). TTO: `DecompiledSource_TTO_2026-11-02\pseudo\Penguin.c`.

---

## Read this first

1. **Two SEQ step-time errors** (index.html work, not a cue job):
   - **Normal Attack.** The game starts nAttack2 **0.5 s** after stage 1 and nAttack3 at **1.0 s** (the dispatcher section below).
     The page's `nAttack1 nAttack2~ nAttack3~` plays the whole clips, nAttack1 0.9 s and nAttack2 0.8 s (`data/penguin/clips.json`).
     So stage 2 starts 0.4 s late and stage 3 at 1.7 s, 0.7 s late. Proposed: **`"Normal Attack: nAttack1@0.5 nAttack2~@0.5 nAttack3~"`**.
     The fades: in the game nAttack1 is a cut and nAttack2 / 3 fade 0.2 s. The page fades a sequence's first step in over
     0.2 s unless it is written with `!` (`startStep(0, steps[0].cut ? 0 : 0.2)`, `index.html:1142`), so a true cut is
     `"nAttack1!@0.5"` (the Sheep's SEQ left its own cut first step as a fade; the user's pick). (Verification 2026-11-10.)
   - **Charge Attack.** cAttack1 gives way to the looped cAttack2 after **0.7 s** (`Yield(2, 0.7)` :19002). The page's
     `cAttack1 cAttack2*~@3` plays cAttack1's whole 1.9 s clip, 1.2 s late. Proposed: **`"Charge Attack: cAttack1@0.7 cAttack2*~@3"`**.
2. **Mana Field #411 (a passive, so ON) replaces the charge's look and voice**, in BB and TTO:
   - the ring is `manaField_ring`, not `cAttack_ring` (:18546-18618);
   - the voice is `manaField1|manaField2`, not `cAttack1|cAttack2` (:18720-18794; TTO1102 `hasSkill(0x19b)`, pseudo/Penguin.c:5028, :5210).

   So `cAttack_ring` and the voices `cAttack1` / `cAttack2` are not cued. They play only without Mana Field.
3. **MP Transfer has no tile today.** It plays nAttack1 (:23633). The page hides a clip that any sequence uses (`index.html:2783`),
   and nAttack1 is Normal Attack's first step. Proposal (the Sheep's Lullaby precedent, decision 13):
   - a one-step sequence **`"MP Transfer: nAttack1!"`** (a cut-in: `PlayAnimation("nAttack1", 0)` :23633), with its Thai name and icon;
   - its cues under **`"@MPTransfer:nAttack1"`**, tried first;
   - the bare `"nAttack1"` entry stays Normal Attack's stage 1.

   A `skills` pool on `nAttack1` would not work: it would draw MP Transfer half the time inside the combo, and there is no
   single nAttack1 tile to carry it.
4. **activateIcon1 is not a skill.** It is the mission "activate the icon" interaction, and every class has one. Missions call it
   with `Game.mPlayer.SendMessage("activateIcon", nID)` (M303_SnowPass.cs:936, M205_CrossingPlainLagoon2.cs:396 and 13 more), which
   goes through `activateIcon` (:16082-16091) to RPC_activateIcon1. It plays cAttack2 looped with a 0.5 s fade (:47071-47076) for
   `magAdjust(12)` s with a cast bar (:47150-47188), then RPC_activateIcon2 (:16120-16213) sets standby. Voices: `activate1` at
   the start (:47126-47138), `activate2` at the end (:16186-16213). Recommendation: **no tile** (question 2). An optional entry
   is given below.
5. **Inventory gaps.**
   - `nAttack_fire` is missing from `plans/fx_inventory.md`: it is a hero-prefab field (`Instantiate(this.nAttack_fire, ...)` :9672),
     not a `Resources.Load` path. It needs exactly what `spreadShot_fire` needs (ProjectileControl + **Penguin_nAttack**): the
     probe shows the same components, two EllipsoidParticleEmitters and an AudioSource `nAttack`.
   - `nAttack_hit` (:9711) and `deadEffect` (:47977) are fields too. Both are ready by the probe (EffectControl + ImageEmitter /
     RingEmitter, the Sheep's `deadEffect` shape).
6. **The game's own no-target shot does not reach 10 m.** With nothing targeted, the click aims at `position + 10 forward`
   (GameGui.cs:1659), and `doNormalAttack` then lowers the aim by 0.25 m because the target object is null (:9300-9306).
   (Corrected in the verification, 2026-11-10.) With an enemy targeted, the click aims at the enemy's
   **`collider.bounds.center`** (GameGui.cs:1626), not its feet, so a real enemy at 10 m is hit by a nearly flat ball, not
   by one meeting the ground. And the ball is a trigger sphere of **radius 0.35** (`m_Radius: 0.35`, no gravity,
   nAttack_fire.prefab / spreadShot_fire.prefab), so on flat ground it fires `OnTriggerEnter` when its centre is 0.35 m up:
   - aimed at the 10 m ground point (the cues below): it touches the ground at **5.57 m after 0.363 s**, not 10 m after 0.6807 s;
   - the no-target click: **4.30 m after 0.273 s** (its centre path alone would reach the ground at 7.625 m after 0.5117 s);
   - the numbers: `checks\fx_penguin_research\verify\ball_radius.py`.

   The cues below keep the decision-3 convention (the ball ends at the 10 m target point after the centre path, 0.6807 s),
   as the Sheep's homingLight did (its radius 0.3 was not counted either). That is a picture of "hits the enemy at 10 m",
   not what a ground-aimed ball does. This is question 1.
7. **The Staff of Time (`w_pgn59`) changes the shot,** and it is a wardrobe item (`data/item_map.json`). Held, it slows the ball
   to 0.01 m/s for 12 s, with a 3 m radius (Penguin_nAttack.cs:115-145; Bible `penguin-skill-reference.md:206`). This is question 3.
8. **Name collisions.** The cue kind picks the folder, and voices are saved as `v_<name>`.
   - `nAttack1-3`, `cAttack1`, `cAttack2` are both clip names and `voices/` files.
   - `cAttack` (sounds/) is the loop that `manaField_ring` / `cAttack_ring` play themselves. The voices `cAttack1` / `cAttack2` are another thing.
   - `mpTransfer` is an effect and a `sounds/` file (the effect plays it). The voices are `mpTransfer1` / `mpTransfer2`.
   - `multiCast` is an effect and a voice (`voices/multiCast`, plus `multiCast1-3`).
   - `cast` is in both `voices/` and `sounds/` (castRing's loop; not in this scope).
   - `sleep` is only in `voices/` (the Penguin has no `sounds/sleep`).
   - No cue in this scope is kind `"sound"`: none of these coroutines loads a `Sounds/` clip. Every sound comes with its effect:
     - `nAttack_fire` → sounds/nAttack (vol 1);
     - `spreadShot_fire` → sounds/nAttack (vol 0.5 each);
     - `nAttack_hit` → sounds/nAttack_hit;
     - `manaField_ring` → sounds/cAttack (looped);
     - `mpTransfer` → sounds/mpTransfer.
9. **Unlike the Sheep, the Penguin has KO voices.** `voices/` has ko1, ko2, dead1, dead2, so the KO entry is the Wolf's (voices + deadEffect, rolled).
10. **Spread Shot #401 (a passive, so ON) is rolled.** BB's `Random.Range(0, 100) <= lckAdjust(20)` = 21 % on stages 1-2 and
    `<= lckAdjust(40)` = 41 % on stage 3. At the page's stats (LCK 1, CharacterControl.cs:20667-20668):
    - stages 1-2: lckAdjust(20) = floor(100 × 20.2 / 100.2) = floor(20.16) = 20, and `<=` counts 0..20 = 21 values;
    - stage 3: lckAdjust(40) = floor(100 × 40.4 / 100.4) = floor(40.24) = 40, so 41 values.

    TTO1102 is the same: it skips only when `lck < rand` (pseudo/Penguin.c:18749-18750, :19496-19497). The Bible already has the
    `<=` note (`:683`). A proc fires 3 pellets **instead of** the one ball (:17254-17281), so the single ball takes the `!` roll.
11. **Possible game bug (low impact, no cue change).** RPC_cAttack1's case 2 (:18505-18518) ends only when `actionState != "attack"`
    **and** `myCommand != "cAttack1"`. A release 0.35-0.7 s in leaves `actionState "attack"` (RPC_cAttack0's standby comes 0.35 s
    later, :19223), so the cAttack2 loop and the ring still start after the release. Not traced further. The GUI's charge needs a
    0.3 s hold first (GameGui.cs:1668).

---

## The dispatcher: Normal Attack stage times (SEQ check)

`doNormalAttack` (:9235-9471):

- **Stage 2:** while `myCommand == "nAttack1"`, with Combo #101 (:9339), only when `actionTime + 0.3 < now < actionTime + 0.5`
  (`:9349` breaks at `<= +0.3`, `:9357` breaks at `>= +0.5`). It then starts RPC_nAttack2 (:9365).
- **Stage 3:** while `myCommand == "nAttack2"`, with #102 (:9403), once `now > actionTime + 0.8` (:9413). It then starts
  RPC_nAttack3 (:9421). The window closes at stage 2's standby, stage 1 + 1.0 s (below).
- **actionTime is never reset by stages 2 / 3.** Their entry sets only `actionState` and `myCommand` (:17857-17860, :18319-18322).
  So each stage waits for a fixed time after stage 1:
  - RPC_nAttack2: `Yield(2, actionTime - now + 0.5)` (:17877). The press is always before 0.5 s, so **the nAttack2 clip starts at 0.5 s**.
  - RPC_nAttack3: `Yield(2, actionTime - now + 1)` (:18332). The press comes between 0.8 and 1.0 s, so **the nAttack3 clip starts at 1.0 s**.
- Stage 1's standby at 0.5 s checks `myCommand == "nAttack1"` (:17309), so it is skipped once stage 2 is pressed. Stage 2's
  standby at 0.5 s into its clip (stage 1 + 1.0) checks `"nAttack2"` (:17799), so it is skipped once stage 3 is pressed.
- TTO1102 is the same: `Waits__Get(actionTime - now + 0.5)` in `<RPC_nAttack2>d__163::MoveNext@0x1dfc630` (pseudo/Penguin.c:19060).

Step lengths: nAttack1 runs 0 to 0.5, nAttack2 runs 0.5 to 1.0, and nAttack3 runs to its standby at 0.5 s. Its clip is
1.5 s; the page plays it to the end, which holds every landing below. The fades:
- nAttack1 is a cut (`PlayAnimation("nAttack1", 0)` :17385);
- nAttack2 fades 0.2 s, `~` (:17605);
- nAttack3 fades 0.2 s, `~` (:18067).

**Proposed SEQ:** `"Normal Attack: nAttack1@0.5 nAttack2~@0.5 nAttack3~"`. It parses under the token regex (`index.html:1071`).
The ball landings below are placed across the steps with these times. With today's SEQ they would land at the wrong moments
(they are not wrong per clip, but stage 1's ball would land in nAttack1's own tail).

## The dispatcher: Charge Attack (SEQ check)

- `doBeginCharge` (:9475-9570): from standby or run, with #111 (:9524), not within 1 s of the last action (:9539). It starts
  RPC_cAttack1 (:9545).
- `doReleaseCharge` (:9574-9640): while `actionState "attack"` and `myCommand "cAttack1"`, it starts **RPC_cAttack0** (:9617).
  - There is no RPC_cAttack2 and no minimum hold, damage or shot. The Bible: "No direct damage on release ever", `:209`.
  - RPC_cAttack0 (:19193-19223) sets `myCommand "cAttack0"` (:19199), crossfades to root over 0.35 s (:19208-19211), and goes
    to standby 0.35 s later (`Yield(2, 0.35)` :19223, :19163). No voice and no effect.
- `cAttack1@0.7`: the clip cuts in at 0 (`PlayAnimation("cAttack1", 0)` :18666). Then `Yield(2, 0.7)` (:19002), then
  `PlayAnimation("cAttack2", 0.2f)` with Loop (:18520-18525). The 0.2 s fade is SEQ's `~`. The page fades the first step
  in over 0.2 s (`index.html:1142`); the game's cut would be `cAttack1!@0.7` (verification 2026-11-10).
- `@3` on cAttack2: no length is fixed. The hold gives MP every 1 s (:18879-18903, Charge Attack rank 4 = getChargeAttackLv 4
  :9723-9760), so 3 s is three ticks. Keep it.

**Proposed SEQ:** `"Charge Attack: cAttack1@0.7 cAttack2*~@3"`.

---

## nAttack1 (Normal Attack, stage 1)

- Coroutine `RPC_nAttack1` (`$RPC_nAttack1$26014`, :17012-17430).

| t (s) | what | source |
|---|---|---|
| 0 | `actionState "attack"`, `actionTime`, `myCommand "nAttack1"`, `addTimeOut("nAttack", 1.5)`, clip nAttack1 (cut); wait 0.1 | :17367-17397, `Yield(2, 0.1)` :17421 |
| 0.1 | voice `Voices/nAttack1` (1.0 own, 0.75 others); wait 0.2 | :17144-17203, PlayOneShot :17425, `Yield(3, 0.2)` :17419 |
| 0.3 | the shot, own client (`isMine` :17222) and `mGameType >= 5` (:17230); fire point 0.75 m up, 0.5 m ahead (`TransformDirection(0, 0.75, 0.5)` :17238), aim `tDir − (0, 0.75, 0.5)` (:17243). With #401 and a 21 % roll: `RPC_spreadShot_fire` (:17248-17273), else `RPC_nAttack_fire` (:17281). Wait 0.2 | `Yield(4, 0.2)` :17410 |
| 0.5 | standby, unless stage 2 was pressed | :17303-17325 |

- Sums: voice 0 + 0.1 = 0.1; shot 0.1 + 0.2 = 0.3; standby 0.3 + 0.2 = 0.5.
- **The ball.** `RPC_nAttack_fire` (:9665-9705): `Instantiate(nAttack_fire, firePos, FromToRotation(forward, fireDir))`, ProjectileControl life
  `1.4 × rangeMod` (:9681), `Penguin_nAttack.Init` (:9693).
  - Penguin_nAttack moves it at 14 m/s forward (Penguin_nAttack.cs:103) and ends it after 1.4 s (:25, :44-53).
  - On any collider that is not the owner's layer and not layer 1 / 2, it destroys itself (:211-229) and calls RPC_nAttack_hit
    at the contact point (`ClosestPointOnBounds`, :238). That call comes **before** the Player / Enemy test (:261 vs :279-294),
    so the ground counts.
  - RPC_nAttack_hit (:9709-9712): `Instantiate(nAttack_hit, hitPos, hero rotation)`. nAttack_hit plays its own sounds/nAttack_hit.
- **Geometry** (decision 3: aimed at the 10 m ground point, `geom.txt`; the centre path, the 0.35 m trigger radius not
  counted, Read this first 6):
  - aim (0, −0.75, 9.5): pitch atan(0.75 / 9.5) = **4.514°** down;
  - path √(9.5² + 0.75²) = √90.8125 = 9.5296 m, so 9.5296 / 14 = **0.6807 s**;
  - it lands at 0.3 + 0.6807 = 0.9807 s after stage 1, which is **0.4807 s into nAttack2** (0.9807 − 0.5).
- **Spread Shot.** `RPC_spreadShot_fire` (:11472-11586): `spreadShot_fire` three times, i = −1, 0, 1, at `firePos + 0.3 i × right`, rotation
  `lhs × Euler(0, 15 i, 0)` with lhs's roll zeroed (:11496-11520). Each gets the same ProjectileControl and Penguin_nAttack (:11525-11551).
  - In Unity Euler, the side pellets are (4.36, ±15.045, ±1.171) (`geom.txt`).
  - The side pellets travel 9.8657 m (0.7047 s) and meet the ground at x = ±2.853, d = 10.0.
  - Landings: centre 0.9807 s after stage 1 (as the single ball), sides 1.0047 s. Stage 2 runs 0.5 to 1.0, so the side hits fall
    0.0047 s into nAttack3 and are cued there.
- TTO1102 `<RPC_nAttack1>d__162::MoveNext@0x1dfbb50`: the same waits (0.1 `:18679`, 0.2 `:18562`), `lckAdjust(0x14)` (:18749), cut clip (:18662).
- Left out: Frost Bite's frost / ice (Penguin_nAttack.cs:321-350) and `onNormalAttackHit`'s gear procs (:48447-48871). Both act
  only on an enemy actually hit: they come after the Player / Enemy test (Penguin_nAttack.cs:279-306), on an enemy with no
  target-point analogue.

```json
  "nAttack1": {
    "why": "Penguin.cs RPC_nAttack1 (:17012-17430): clip at 0 (cut, :17385); 0.1 s (Yield(2, 0.1) :17421) voice nAttack1 (PlayOneShot :17425); 0.3 s (Yield(3, 0.2) :17419) the shot, mGameType >= 5 (:17230): fire point 0.75 m up 0.5 m ahead (TransformDirection(0, 0.75, 0.5) :17238), aim tDir - (0, 0.75, 0.5) (:17243), at the 10 m target point on the ground (decision 3, as the Sheep's; a real enemy is aimed at its collider.bounds.center, GameGui.cs:1626, the no-target click 0.25 lower, GameGui.cs:1659, :9306; the ball's 0.35 m trigger radius is not counted): pitch atan(0.75 / 9.5) = 4.514 deg; Spread Shot #401 on (passives rule), Random.Range(0, 100) <= lckAdjust(20) = 21 % (:17254, CharacterControl.cs:20667): RPC_spreadShot_fire's 3 pellets at firePos + 0.3 i right, lhs x Euler(0, 15 i, 0) (:11496-11520; Unity Euler (4.36, +-15.045, +-1.171), checks/fx_penguin_research/attacks_emotes/geom.txt) instead of RPC_nAttack_fire's one ball (:9672, :17281); Penguin_nAttack flies them 14 m/s (Penguin_nAttack.cs:103) and ends them on the ground (:211-229); each plays its own Sounds/nAttack (ball 1.0, pellets 0.5); standby 0.5 s (Yield(4, 0.2) :17410, :17315) unless stage 2 is pressed (stage 2 starts at 0.5 s: its entry carries this shot's landing at 0.3 + 0.6807 - 0.5 = 0.4807 s, nAttack3's the side pellets' at 0.3 + 0.7047 - 1.0 = 0.0047 s)",
    "cues": [
    [0.1, "voice", "nAttack1"],
    [0.3, "fx", "nAttack_fire", {"d": 0.5, "y": 0.75, "rot": [4.514, 0, 0], "p": 0.21, "roll": "!spread1"}],
    [0.3, "fx", "spreadShot_fire", {"d": 0.5, "x": -0.3, "y": 0.75, "rot": [4.36, -15.045, -1.171], "p": 0.21, "roll": "spread1"}],
    [0.3, "fx", "spreadShot_fire", {"d": 0.5, "y": 0.75, "rot": [4.514, 0, 0], "p": 0.21, "roll": "spread1"}],
    [0.3, "fx", "spreadShot_fire", {"d": 0.5, "x": 0.3, "y": 0.75, "rot": [4.36, 15.045, 1.171], "p": 0.21, "roll": "spread1"}]
    ]
  },
```

The roll names are per stage (`spread1` / `spread2` / `spread3`): rolls last for the whole play of a sequence (`fxStart`
resets `FX.rolls` only at step 0, `index.html:3484`). So the later steps' landing cues share their own stage's roll.
Sure: high on times and geometry. The landing moment assumes an enemy exactly at 10 m (question 1).

## nAttack2 (stage 2)

- Coroutine `RPC_nAttack2` (`$RPC_nAttack2$26023`, :17463-17891). It is started by a press 0.3-0.5 s into stage 1; its clip starts at
  stage 1 + 0.5 s (:17877).

| t (s, from its clip) | what | source |
|---|---|---|
| 0 | LookAt, `addTimeOut("nAttack", 1.5)`, clip nAttack2 (0.2 s fade); wait 0.2 | :17590-17613, `Yield(3, 0.2)` :17879 |
| 0.2 | voice `Voices/nAttack2`; wait 0.1 | :17629-17693, PlayOneShot :17870, `Yield(4, 0.1)` :17885 |
| 0.3 | the shot, as in stage 1 (:17707-17784; #401 with a 21 % roll, `lckAdjust(20)` :17744); wait 0.2 | `Yield(5, 0.2)` :17875 |
| 0.5 | standby, unless stage 3 is pressed | :17793-17815 |

- Sums: voice 0 + 0.2 = 0.2; shot 0.2 + 0.1 = 0.3 (stage 1 + 0.8); standby 0.3 + 0.2 = 0.5 (stage 1 + 1.0).
- Landings in this step: stage 1's centre ball (or Spread Shot's middle pellet, the same path) at 0.3 + 0.6807 − 0.5 =
  **0.4807 s**. It lands whatever the roll, so the hit is unrolled. This stage's own landings fall in nAttack3.
- TTO1102 `<RPC_nAttack2>d__163::MoveNext@0x1dfc630`: 0.2 fade (:18892), waits 0.1 (:18975) and `actionTime - now + 0.5` (:19060), lckAdjust(0x14) (:19123).

```json
  "nAttack2": {
    "why": "Penguin.cs RPC_nAttack2 (:17463-17891; its clip 0.5 s after stage 1: Yield(2, actionTime - now + 0.5) :17877, the press window 0.3-0.5 s, doNormalAttack :9349-9365): clip (0.2 s fade, :17605); 0.2 s (Yield(3, 0.2) :17879) voice nAttack2 (PlayOneShot :17870); 0.3 s (Yield(4, 0.1) :17885) the shot as in nAttack1 (:17728-17784), Spread Shot 21 % (lckAdjust(20) :17744); standby 0.5 s (Yield(5, 0.2) :17875, :17805) unless stage 3 is pressed; at 0.4807 s stage 1's ball (or its middle pellet) meets the ground at the 10 m point (0.3 + 9.5296 m / 14 m/s - 0.5): Penguin_nAttack calls RPC_nAttack_hit at the contact point before any Player / Enemy test (Penguin_nAttack.cs:211-261), nAttack_hit there with the hero's rotation (:9711; plays its own Sounds/nAttack_hit)",
    "cues": [
    [0.2, "voice", "nAttack2"],
    [0.3, "fx", "nAttack_fire", {"d": 0.5, "y": 0.75, "rot": [4.514, 0, 0], "p": 0.21, "roll": "!spread2"}],
    [0.3, "fx", "spreadShot_fire", {"d": 0.5, "x": -0.3, "y": 0.75, "rot": [4.36, -15.045, -1.171], "p": 0.21, "roll": "spread2"}],
    [0.3, "fx", "spreadShot_fire", {"d": 0.5, "y": 0.75, "rot": [4.514, 0, 0], "p": 0.21, "roll": "spread2"}],
    [0.3, "fx", "spreadShot_fire", {"d": 0.5, "x": 0.3, "y": 0.75, "rot": [4.36, 15.045, 1.171], "p": 0.21, "roll": "spread2"}],
    [0.4807, "fx", "nAttack_hit", {"d": 10}]
    ]
  },
```

## nAttack3 (stage 3)

- Coroutine `RPC_nAttack3` (`$RPC_nAttack3$26032`, :17925-18353). It is started by a press after 0.8 s; its clip starts at
  stage 1 + 1.0 s (:18332).

| t (s, from its clip) | what | source |
|---|---|---|
| 0 | LookAt, `addTimeOut("nAttack", 1.5)`, clip nAttack3 (0.2 s fade); wait 0.1 | :18052-18076, `Yield(3, 0.1)` :18347 |
| 0.1 | `moveSpeed -0.5`, voice `Voices/nAttack3`; wait 0.2 | :18091-18155, PlayOneShot :18340, `Yield(4, 0.2)` :18349 |
| 0.3 | the shot (:18169-18246); #401 with a **41 %** roll (`lckAdjust(40)` :18206); wait 0.2 | `Yield(5, 0.2)` :18351 |
| 0.5 | standby | :18255-18277 |

- Sums: voice 0 + 0.1 = 0.1; shot 0.1 + 0.2 = 0.3 (stage 1 + 1.3); standby 0.3 + 0.2 = 0.5.
- Landings in this step (times from stage 1, minus 1.0):
  - stage 1's side pellets: 1.0047 → **0.0047**;
  - stage 2's centre: 0.8 + 0.6807 = 1.4807 → **0.4807**;
  - stage 2's sides: 0.8 + 0.7047 = 1.5047 → **0.5047**;
  - stage 3's centre: 1.3 + 0.6807 = 1.9807 → **0.9807**;
  - stage 3's sides: 1.3 + 0.7047 = 2.0047 → **1.0047**.

  All of these fall inside the 1.5 s clip the page plays.
- TTO1102 `<RPC_nAttack3>d__164::MoveNext@0x1dfd160`: 0.2 fade (:19265), wait 0.1 (:19272), lckAdjust(0x28) (:19496).

```json
  "nAttack3": {
    "why": "Penguin.cs RPC_nAttack3 (:17925-18353; its clip 1.0 s after stage 1: Yield(2, actionTime - now + 1) :18332, the press from 0.8 s, doNormalAttack :9413-9421): clip (0.2 s fade, :18067); 0.1 s (Yield(3, 0.1) :18347) voice nAttack3 (PlayOneShot :18340); 0.3 s (Yield(4, 0.2) :18349) the shot as in nAttack1 (:18190-18246), Spread Shot 41 % (Random.Range(0, 100) <= lckAdjust(40) = 40, :18206); standby 0.5 s (Yield(5, 0.2) :18351, :18267); the landings at the 10 m line (Penguin_nAttack.cs:211-261, nAttack_hit with the hero's rotation :9711, its own Sounds/nAttack_hit; checks/fx_penguin_research/attacks_emotes/geom.txt): stage 1's side pellets 0.3 + 0.7047 - 1.0 = 0.0047 s (x +-2.853), stage 2's ball 0.8 + 0.6807 - 1.0 = 0.4807 s and its sides 0.5047 s, this stage's ball 0.9807 s and its sides 1.0047 s",
    "cues": [
    [0.0047, "fx", "nAttack_hit", {"d": 10, "x": -2.853, "p": 0.21, "roll": "spread1"}],
    [0.0047, "fx", "nAttack_hit", {"d": 10, "x": 2.853, "p": 0.21, "roll": "spread1"}],
    [0.1, "voice", "nAttack3"],
    [0.3, "fx", "nAttack_fire", {"d": 0.5, "y": 0.75, "rot": [4.514, 0, 0], "p": 0.41, "roll": "!spread3"}],
    [0.3, "fx", "spreadShot_fire", {"d": 0.5, "x": -0.3, "y": 0.75, "rot": [4.36, -15.045, -1.171], "p": 0.41, "roll": "spread3"}],
    [0.3, "fx", "spreadShot_fire", {"d": 0.5, "y": 0.75, "rot": [4.514, 0, 0], "p": 0.41, "roll": "spread3"}],
    [0.3, "fx", "spreadShot_fire", {"d": 0.5, "x": 0.3, "y": 0.75, "rot": [4.36, 15.045, 1.171], "p": 0.41, "roll": "spread3"}],
    [0.4807, "fx", "nAttack_hit", {"d": 10}],
    [0.5047, "fx", "nAttack_hit", {"d": 10, "x": -2.853, "p": 0.21, "roll": "spread2"}],
    [0.5047, "fx", "nAttack_hit", {"d": 10, "x": 2.853, "p": 0.21, "roll": "spread2"}],
    [0.9807, "fx", "nAttack_hit", {"d": 10}],
    [1.0047, "fx", "nAttack_hit", {"d": 10, "x": -2.853, "p": 0.41, "roll": "spread3"}],
    [1.0047, "fx", "nAttack_hit", {"d": 10, "x": 2.853, "p": 0.41, "roll": "spread3"}]
    ]
  },
```

Sure: high on the trace. The 0.0047 s cue depends on the proposed SEQ (stage 2's step ending at exactly 0.5 s).

---

## cAttack1 (Charge Attack: the wind-up)

- Coroutine `RPC_cAttack1` (`$RPC_cAttack1$26041`, :18388-19005).
- At 0: `actionState "attack"`, `actionTime`, `myCommand "cAttack1"`, `addTimeOut("cAttack", 1)`, then clip cAttack1 as a cut
  (:18631-18671).
- The voice also plays at 0 (own hero or a mission teammate, :18684-18706), at most once every 2 s (:18707-18715):
  - with Mana Field #411 (ON): `manaField1|manaField2` (Random.Range(0, 2), :18720-18793; PlayOneShot :18996 / :18988);
  - without it: `cAttack1|cAttack2` (:18795-18862).
- Then `Yield(2, 0.7)` (:19002).
- TTO1102 `<RPC_cAttack1>d__168::MoveNext@0x1de3bd0`: the same strings (pseudo/Penguin.c:4932-4945), the 2 s voice gate (:5026),
  `hasSkill(0x19b)` (:5028).

```json
  "cAttack1": {
    "why": "Penguin.cs RPC_cAttack1 (:18388-19005): clip at 0 (cut, :18666) and the voice at 0, Mana Field #411 on (passives rule): manaField1 / manaField2 (Random.Range(0, 2), :18720-18793, PlayOneShot :18996 / :18988; without it cAttack1 / cAttack2, :18795-18862); at 0.7 s (Yield(2, 0.7) :19002) it changes to the looped cAttack2 (:18520-18525), whose cue holds the ring",
    "cues": [
    [0, "voice", "manaField1|manaField2"]
    ]
  },
```

## cAttack2 (Charge Attack: the held charge)

- Same coroutine, case 2 (:18504-18621), at cAttack1 + 0.7 s.
- At 0 (its own clip): `PlayAnimation("cAttack2", 0.2f)` looped (:18520-18525). Then, **only when `mGameType > 4`** (:18540; the
  Sheep's precedent keeps mission-only effects):
  - with #411: `manaField_ring` created at the hero's position and rotation (:18546-18575);
  - without it: `cAttack_ring` (:18587-18610).
- Every FixedUpdate (`Yield(3, WaitForFixedUpdate)` :19000) while `myCommand "cAttack1"`: an MP tick every 1 s (:18879-18903), and
  with #411 an MP share to the own player within 8 m (:18909-18967). Neither draws anything.
- `manaField_ring` (probe): EffectControl life 300, afterLife 0.3, **followState**, followPosition; an ImageEmitter 0.05 m up,
  a LineEmitter and a RingEmitter; its AudioSource plays `sounds/cAttack` on awake, **looped**. Ready (inventory).
- **The followState cut:** the release (RPC_cAttack0) sets `myCommand "cAttack0"` (:19199), and EffectControl ends the ring on a
  `myCommand` / `actionState` change (EffectControl.cs:194-232, the Sheep's check). The page's step ends at 3 s, so the cut is
  **2.95** (the Sheep's 3.95 under a 4 s hold).

```json
  "cAttack2": {
    "why": "Penguin.cs RPC_cAttack1 case 2 (the change to cAttack2, looped, 0.7 s in: :18520-18525): Mana Field #411 on (passives rule): manaField_ring at the hero's position and rotation (:18546-18575; without it cAttack_ring, :18587-18610), mission / arena only (mGameType > 4, :18540); it plays its own looping Sounds/cAttack; followState (EffectControl.cs:194-232): it ends at the release, when RPC_cAttack0 sets myCommand cAttack0 (:19199; root crossfade 0.35 s, :19208-19211): cut 2.95, the page's step ends at 3 s; the MP ticks every 1 s (:18879-18967) draw nothing",
    "cues": [
    [0, "fx", "manaField_ring", {"cut": 2.95}]
    ]
  },
```

Sure: high.

---

## MP Transfer (RPC_mpTransfer, clip nAttack1): its own sequence

- Coroutine `RPC_mpTransfer` (`$RPC_mpTransfer$26140`, :23291-23852). It is an ally-targeted skill, so it shows as a self-cast
  on the hero (decision 1 analogue).

| t (s) | what | source |
|---|---|---|
| 0 | target from `tID` (:23588-23606), `actionState "attack"`, `myCommand "mpTransfer"`, cooldown `agiAdjust(30)`, clip nAttack1 (cut); `mpTransfer_ring` at the hero's position and rotation; voice `mpTransfer1|mpTransfer2` (Random.Range(0, 2)) if 3 s have passed since the last one, else `Voices/multiCast` (a Double / Triple Cast repeat); wait 0.3 | :23615-23663, voice :23706-23842, `Yield(2, 0.3)` :23844 |
| 0.3 | own client: `RPC_AddHeal` MP to the target (:23477), `mpTransfer` created **at the target's** position and rotation (:23482-23505); wait 0.2 | `Yield(3, 0.2)` :23846 |
| 0.5 | standby | :23519-23546 |

- Sums: effect 0 + 0.3 = 0.3; standby 0.3 + 0.2 = 0.5.
- Prefabs (probe):
  - `mpTransfer_ring`: EffectControl life 1, afterLife 1, **followState**, followPosition; an ImageEmitter at 0.75 up, 0.5 ahead,
    Delay 0.3. It ends at the standby, 0.5 s (cut 0.5).
  - `mpTransfer`: EffectControl life 1, afterLife 1, followPosition; Emblem, Image and Line emitters; it plays `sounds/mpTransfer` itself.
- The `multiCast` voice: the page's tile replays every 0.9 s, but each play stands for a fresh cast (the 30 s cooldown,
  :23624), so the cue keeps `mpTransfer1|mpTransfer2`.
- TTO1102 `<RPC_mpTransfer>d__182::MoveNext@0x1dfabe0`: the same strings (pseudo/Penguin.c:17919-17928), cut clip (:18221), 3 s voice gate (:18294), waits 0.1 / 0.5 in the heal calc (:17984-17990, unrelated).

**Page change (index.html):** add `"MP Transfer: nAttack1!"` to the `penguin:` SEQ, with the tile's Thai name and icon. The entry
below is keyed for that sequence.

```json
  "@MPTransfer:nAttack1": {
    "why": "Penguin.cs RPC_mpTransfer (:23291-23852), its own one-step sequence because Normal Attack uses nAttack1 (cut, :23633): at 0 mpTransfer_ring at the hero's position and rotation (:23651-23663; followState, ends at the standby 0.5 s: Yield(2, 0.3) :23844 + Yield(3, 0.2) :23846, :23536) and voice mpTransfer1 / mpTransfer2 (Random.Range(0, 2), :23713-23842; multiCast only on a repeat within 3 s, :23706, :23787); at 0.3 s mpTransfer on the ally (:23500), here the hero (decision 1: ally skills as self-casts; plays its own Sounds/mpTransfer)",
    "cues": [
    [0, "voice", "mpTransfer1|mpTransfer2"],
    [0, "fx", "mpTransfer_ring", {"cut": 0.5}],
    [0.3, "fx", "mpTransfer"]
    ]
  },
```

Sure: high.

## activateIcon1 (clip cAttack2): optional, recommended out

The trace is in "Read this first" 4. If the user wants a tile (question 2), it would be a sequence `"Activate: cAttack2*@12"`. Its
fade is 0.5 s; the SEQ has only 0.1 / 0.2. The cast time is `magAdjust(12)`, or `tID / 100` when the mission passes `300 + n`
(M404_SandOasis.cs:502, so 3 s). The entry:

```json
  "@Activate:cAttack2": {
    "why": "Penguin.cs RPC_activateIcon1 (:46910-47256; a mission's activateIcon, M303_SnowPass.cs:936): cAttack2 looped, 0.5 s fade (:47071-47076), voice activate1 at 0 (:47126-47138), the cast bar magAdjust(12) s (:47150-47188); RPC_activateIcon2 at the end: standby and voice activate2 (:16127-16213), cued just inside the 12 s step",
    "cues": [
    [0, "voice", "activate1"],
    [11.95, "voice", "activate2"]
    ]
  },
```

Not counted among the entries to paste.

---

## Emotes and basic moves

`RPC_emotion` (`$RPC_emotion$26623`, :41355-42180). It works exactly as the Wolf's and the Sheep's:

- The voice plays at 0, **before** the clip (:41540-41618). The gates:
  - the voice option is on (:41540);
  - more than 2 s since the last action (`Time.time > actionTime + 2`, :41546);
  - the own hero, a mission teammate, or anyone in game code 31 (:41552-41580).
- `emo_chat` → `Voices/chat` + `Random.Range(1, 6)`, i.e. chat1-5 (:41598).
- Every other `emo_<name>` → `Voices/<name>` (`Substring(4)`, :41606), played by `PlayOneShot` (:41618, volume 1) only if the file loads.
- Then `actionState "emotion"` and the clip, with a 0.2 s fade (:41637-42122). No effect and no Sounds/ anywhere in RPC_emotion.

| emote | clip | voice file (voices/) | source |
|---|---|---|---|
| emo_hi, emo_wave | wave | hi / wave | :41672, :41680 → :42122 |
| emo_ty, emo_bow | bow | ty / bow | :41690, :41697 → :42108 |
| emo_laugh | laugh | laugh | :41704-41710 |
| emo_sit | sit | none (silent) | :41724-41730 |
| emo_sleep | sleep | sleep | :41736-41742 |
| emo_cheer | cheer | cheer | :41748-41754 |
| emo_beg | beg | beg | :41760-41766 |
| emo_cry | cry | cry | :41772-41778 |
| emo_talk, emo_chat | talk | talk: none; chat: chat1-5 | :41786, :41793 → :42086 |
| emo_pose | pose5 / 15 / 25 / 35 / 45 / 58 / 65 / 46 / 66 by the worn set, else pose | none (silent) | :41800-42046 |
| emo_battle | battle | battle | :42056-42062 |
| emo_dance | dance | none (silent) | :42071-42079 |

- In the rip's `voices/`: hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle and chat1-5 all exist. There is no sit,
  talk, pose or dance (`voices.txt`).
- The other emote-looking voices belong to no tile here: beware, bye, come, follow, giveup, go, paper, rock, scissor, sorry,
  this, what, support, change, return1/2, revive.
- **KO:**
  - `RPC_ko` (`$RPC_ko$26792`, :47293-47640): `animation.Play("ko")` (:47507). Voice ko1 / ko2 at 0 (Random.Range(0, 2) :47542;
    loads :47552 / :47583; PlayOneShot :47628 / :47635). getUp after 3 s (`Yield(2, 3)` :47624 → :47409), standby 1 s later
    (`Yield(3, 1)` :47622 → :47433). No effect.
  - `RPC_dead` (`$RPC_dead$26799`, :47671-48005): Rewind + `animation.Play("ko")` (:47865-47868). Voice dead1 / dead2 at 0
    (:47903-47958). Then **always** `Instantiate(deadEffect, hero position, hero rotation)` (:47970-47977): the voice gates jump
    to IL_93 (:47888, :47896), which is still the effect, and the predicate `88132 − 343220 == −255088` holds.
  - `deadEffect` (probe): EffectControl life 3, no followState; an ImageEmitter 0.8 m up (Life 1.2) and a RingEmitter (Life 0.4),
    both after Delay 0.5. Ready.
  - Decision 11: one of the two at random, even chance, with each one's voices. This is the Wolf's entry.
- getUp, walk, run, falling, root: nothing. RPC_ko's getUp has no voice; no other RPC of theirs plays a voice or an effect.

```json
  "wave": {
    "why": "Penguin.cs RPC_emotion (:41355): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:41606, PlayOneShot :41618; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_hi (:41672) and emo_wave (:41680) both play the wave clip (:42122): voice hi or wave",
    "cues": [
    [0, "voice", "hi|wave"]
    ]
  },
  "bow": {
    "why": "Penguin.cs RPC_emotion (:41355): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:41606, PlayOneShot :41618; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_ty (:41690) and emo_bow (:41697) both play the bow clip (:42108): voice ty or bow",
    "cues": [
    [0, "voice", "ty|bow"]
    ]
  },
  "laugh": {
    "why": "Penguin.cs RPC_emotion (:41355): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:41606, PlayOneShot :41618; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_laugh (:41704-41710)",
    "cues": [
    [0, "voice", "laugh"]
    ]
  },
  "sleep": {
    "why": "Penguin.cs RPC_emotion (:41355): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:41606, PlayOneShot :41618; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_sleep (:41736-41742): voices/sleep (the Penguin has no sounds/sleep)",
    "cues": [
    [0, "voice", "sleep"]
    ]
  },
  "cheer": {
    "why": "Penguin.cs RPC_emotion (:41355): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:41606, PlayOneShot :41618; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_cheer (:41748-41754)",
    "cues": [
    [0, "voice", "cheer"]
    ]
  },
  "beg": {
    "why": "Penguin.cs RPC_emotion (:41355): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:41606, PlayOneShot :41618; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_beg (:41760-41766)",
    "cues": [
    [0, "voice", "beg"]
    ]
  },
  "cry": {
    "why": "Penguin.cs RPC_emotion (:41355): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:41606, PlayOneShot :41618; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_cry (:41772-41778)",
    "cues": [
    [0, "voice", "cry"]
    ]
  },
  "talk": {
    "why": "Penguin.cs RPC_emotion (:41355): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:41606, PlayOneShot :41618; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_chat (:41793) plays the talk clip (:42086) with chat1-5 at random (Random.Range(1, 6), :41598); emo_talk (:41786) plays it silent (no Voices/talk): the tile takes the chat's voice",
    "cues": [
    [0, "voice", "chat1|chat2|chat3|chat4|chat5"]
    ]
  },
  "battle": {
    "why": "Penguin.cs RPC_emotion (:41355): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:41606, PlayOneShot :41618; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_battle (:42056-42062): voice battle; the battle stance in a fight plays the clip silent: the tile takes the emote's voice",
    "cues": [
    [0, "voice", "battle"]
    ]
  },
  "ko": {
    "why": "Penguin.cs RPC_ko (:47293): clip (animation.Play :47507) and voice ko1 or ko2 at 0 (Random.Range(0, 2) :47542, :47552-47635), getUp after 3 s (:47624, :47409), no effect; RPC_dead (:47671) plays the same clip (:47868) with dead1 or dead2 at 0 (:47903-47958) and always puts deadEffect at the hero's position and rotation (:47970-47977; EffectControl life 3): one of the two at random, even chance (the Sheep's decision 11, as wolf.json: roll dead, its voices with it; '!dead' = RPC_ko's)",
    "cues": [
    [0, "voice", "ko1|ko2", {"p": 0.5, "roll": "!dead"}],
    [0, "voice", "dead1|dead2", {"p": 0.5, "roll": "dead"}],
    [0, "fx", "deadEffect", {"p": 0.5, "roll": "dead"}]
    ]
  }
```

---

## Parts needed (build stage)

- `nAttack_fire` (nAttack1-3): ProjectileControl (built) + **Penguin_nAttack**.
  - The motion: 14 m/s along its forward from Init (Penguin_nAttack.cs:103); `life 1.4` (:25, :44-53; ProjectileControl life
    `1.4 × rangeMod`, :9681).
  - The end: on the first collider not the owner's (:211-229), so the floor at the 10 m line.
  - Its children: two EllipsoidParticleEmitters (ice 0.4-0.6, snowflake 0.1).
  - Add the effect to the inventory: it is a field, missed by the `Resources.Load` scan.
- `spreadShot_fire` (nAttack1-3, on a Spread Shot proc): the same part (`plans/fx_inventory.md` already lists it).
- The `w_pgn59` branch of Penguin_nAttack (0.01 m/s, 12 s, radius 3) only if question 3 says yes.

Everything else cued here is ready: nAttack_hit, manaField_ring, mpTransfer_ring, mpTransfer, deadEffect.

## Left out

- Frost Bite's frost / ice and `onNormalAttackHit`'s gear procs (charm, happy, heal1, revert ...; :48447-48871). They follow
  only a hit on an actual enemy (Penguin_nAttack.cs:279-306), on an enemy with no target-point analogue: the wardrobe's balls meet the ground.
- `cAttack_ring` and the voices `cAttack1` / `cAttack2`: replaced by Mana Field (passives ON), not missing.
- The MP-share heal on allies in 8 m (:18909-18967): a number, nothing drawn.

## Open questions for the user (only what the decisions don't answer)

1. **Normal Attack's aim point.** (Corrected in the verification, 2026-11-10: the ball's 0.35 m trigger radius and the
   enemy aim point were not counted.)
   - The game's own no-target shot aims 10 m ahead but 0.25 m low (GameGui.cs:1659, :9306); its 0.35 m trigger sphere
     touches flat ground at 4.30 m after 0.27 s.
   - An enemy at 10 m is aimed at its body centre (`collider.bounds.center`, GameGui.cs:1626): a nearly flat ball that ends on
     the enemy's collider, a little short of 10 m, after about 0.6 s.
   - The cues above: a ball pitched 4.514 deg at the 10 m ground point that ends there after 0.6807 s (the centre path; the
     decision-3 convention, as the Sheep). A ground-aimed ball really touches down at 5.57 m after 0.363 s.
   - Recommended default: **keep the 10 m picture** (the decision's target point; the cues above), or say if the game-true
     5.57 m / 0.363 s landing (or a flat ball at an enemy's body height) is wanted; the same question holds for the Sheep.
2. **activateIcon1** (a mission's "activate" channel on the cAttack2 clip, every class has one): recommended default **no tile**.
   The optional `"@Activate:cAttack2"` entry is above.
3. **The Staff of Time (`w_pgn59`)** slows the normal-attack ball to 0.01 m/s for 12 s: with it held, should the tile show the
   crawling ball? Recommended default: **no**, the normal 14 m/s ball whatever the weapon.

## Offer for the Bible

These look new; the reference's Combo section `:203-206` and Charge Attack section `:208-213` have no timings. Offer them to the
user for `penguin-skill-reference.md`:
- the press windows: stage 2 at 0.3-0.5 s, stage 3 after 0.8 s (:9349-9413);
- the fixed clip starts at 0.5 / 1.0 s (:17877, :18332), the shots at 0.3 / 0.8 / 1.3 s, and the voices at 0.1 / 0.2 / 0.1 s;
- the charge loop at 0.7 s;
- MP Transfer's effect at 0.3 s on the target;
- the no-target landing: about 4.3 m after 0.27 s (the ball's 0.35 m trigger sphere; its centre path alone would reach
  7.6 m; corrected in the verification), and that a targeted shot aims at the enemy's body centre (GameGui.cs:1626);
- the 0.35-0.7 s release quirk (Read this first 11).

## Verification (2026-11-10)

A skeptical re-trace, read-only. Probe scripts: `checks\fx_penguin_research\verify\` (`ball_radius.py`, `parse_entries.py`,
`ec_fields.py`, and the `clip_flow.js` dumps `nAttack1.txt`, `nAttack23.txt`, `cAttack1.txt`, `mpTransfer.txt`).

**Checked and confirmed** (re-added the waits along each flattened state machine from its PlayAnimation):
- nAttack1: clip cut :17385, Yield 0.1 :17421 → voice :17425 (0.1), Yield 0.2 :17419 → the shot (0.3), Yield 0.2 :17410 → standby (0.5), its `myCommand == "nAttack1"` test :17309.
- nAttack2: clip 0.2 fade :17605 after `Yield(2, actionTime - now + 0.5)` :17877; Yield 0.2 :17879 → voice :17870 (0.2); Yield 0.1 :17885 → shot (0.3); Yield 0.2 :17875 → standby (0.5). Entry sets only actionState / myCommand (:17857-17860).
- nAttack3: `Yield(2, actionTime - now + 1)` :18332; clip 0.2 fade :18067; Yield 0.1 :18347 → voice :18340 (0.1); Yield 0.2 :18349 → shot (0.3); Yield 0.2 :18351 → standby (0.5).
- doNormalAttack windows: stage 2 `> +0.3` and `< +0.5` with #101, stage 3 `> +0.8` with #102 (:9339-9421).
- Spread Shot: `<= lckAdjust(20)` :17254 / :17744, `<= lckAdjust(40)` :18206; lckAdjust (CharacterControl.cs:20658-20669) at LCK 1: 20.2 → 2020 / 100.2 = 20.16 → 20 (21 values, 21 %); 40.4 → 4040 / 100.4 = 40.24 → 40 (41 %). TTO1102 `if (lck < rand) skip` (pseudo/Penguin.c:18749-18750, :19496-19497).
- RPC_spreadShot_fire (:11472-11586): i = −1..1, `firePos + 0.3 i right`, `lhs * Euler(0, 15 i, 0)`, lhs's z zeroed; geom.py's quaternion maths re-read, its output stands for the centre path.
- Penguin_nAttack.cs: 14 m/s set once in Init (:103), life 1.4 (:25), the w_pgn59 branch (:115-139), the hit at ClosestPointOnBounds (:238) and RPC_nAttack_hit (:261) before the Player / Enemy test (:279). Prefabs: no gravity (`m_UseGravity: 0`).
- cAttack1: cut :18666, voice gate (pvoice; own, or a mission teammate; 2 s timer :18707-18715), #411 → manaField1 / 2 (:18738, :18770), Yield 0.7 :19002; case 2 → cAttack2 0.2 fade looped (:18520-18525), the ring only when `mGameType > 4` (:18540), #411 → manaField_ring (:18558-18570). The case-2 exit needs `actionState != "attack"` **and** `myCommand != "cAttack1"` (:18505-18515): the 0.35-0.7 s release quirk holds.
- RPC_cAttack0: myCommand cAttack0 :19199, root crossfade 0.35 :19208-19211, Yield 0.35 :19223 → standby :19163. EffectControl's followState end on an actionState / myCommand change (EffectControl.cs:188-201).
- MP Transfer: clip nAttack1 cut :23633, mpTransfer_ring at the hero :23663, voice mpTransfer1 / 2 with the 3 s timer (:23706-23710), multiCast otherwise (:23787); Yield 0.3 :23844 → RPC_AddHeal on the target :23477 and mpTransfer at the target's transform (:23500); Yield 0.2 :23846 → standby :23536. Only clip callers of nAttack1: :17385 and :23633.
- Probe EffectControl fields (ec_fields.py): manaField_ring 300 / 0.3 followState; mpTransfer_ring 1 / 1 followState (cut 0.5 right); mpTransfer 1 / 1; nAttack_hit 2; deadEffect 3, no follow.
- Prefab fields nAttack_fire / nAttack_hit / deadEffect (probe_fields.txt), and absent from `plans/fx_inventory.md` "penguin": confirmed.
- KO: RPC_ko clip :47507, ko1 / ko2 :47552 / :47583, getUp after 3 s; RPC_dead Rewind + ko :47865-47868, dead1 / dead2, deadEffect always (IL_93 :47970-47977). Emote lines (:41546, :41598, :41606, :41618, :41672-42122) re-read.
- Every cued name is a file: all voices in `heroes\penguin\voices\`, all effects in `heroes\penguin\effects\` (parse_entries.py; all 17 entries parse, times in order). No `Sounds/` load in any coroutine of this scope.
- `index.html`: the sequence clip hiding (:2783), the token regex (`nAttack1!@0.5` also parses), `FX.rolls` reset only at step 0, `"@MPTransfer:nAttack1"` matches `ch.id` (fxStart).
- TTO1102 lines (pseudo/Penguin.c): nAttack1 :18562 / :18662 / :18679 / :18749, nAttack2 :18892 / :18975 / :19060 / :19123, nAttack3 :19265 / :19272 / :19496, cAttack1 :5026 / :5028 / :5210, mpTransfer :18221 / :18294: all as written. (No TTO prefab claim in this report, so the TTO prefab probe was not re-run.)

**Corrections made:**
1. Read this first 6, the nAttack1 why and Geometry, question 1, the Bible offer. Old: "an enemy at the 10 m target point (no −0.25), so the ball meets the ground at 10 m after 0.6807 s"; "the 7.625 m no-target landing after 0.5117 s". New: a targeted enemy is aimed at its `collider.bounds.center` (GameGui.cs:1626), not its feet; the ball is a 0.35 m trigger sphere (`m_Radius: 0.35`, nAttack_fire.prefab / spreadShot_fire.prefab), so a ground-aimed ball touches flat ground at 5.57 m after 0.363 s and the no-target click at 4.30 m after 0.273 s (`verify\ball_radius.py`). The cues keep the decision-3 convention (as the Sheep's homingLight, radius 0.3, also not counted); question 1 now says so.
2. Read this first 1 and the Charge Attack SEQ section. Old: "The fades are right: nAttack1 is a cut". New: the page fades a sequence's first step 0.2 s unless it has `!` (`index.html:1142`), so the game's cuts would be `nAttack1!@0.5` and `cAttack1!@0.7`; the Sheep kept the fade, so this is the user's pick.

**Not disproved, left as written:** the ground collider sits at the hero's foot level (the radius numbers assume flat ground at y = 0); the MP-transfer self-cast reading (decision 1 analogue).
