# Bat effects + sounds research: Normal Attack, Drain Life (charge), activateIcon, emotes, basic moves, KO

Scope: clips nAttack1, nAttack2, nAttack3 (RPC_nAttack1-3, the dispatcher `doNormalAttack`, RPC_nAttack_fire1 / fire2,
RPC_nAttack_hit), cAttack1, cAttack2 (Drain Life: RPC_cAttack1, the release RPC_cAttack0, `doBeginCharge`,
`doReleaseCharge`, RPC_cAttack_hit, Dream Burst's RPC_dreamBurst_hit), RPC_activateIcon1 (plays cAttack2), the emotes
(RPC_emotion), the basic moves and KO (RPC_ko, RPC_dead). Research only (recipe steps 1-3). No MP / SP transfer style
skill of the Bat plays an attack clip: `clip_calls.js` lists only the three combo stages, RPC_cAttack1 and
RPC_activateIcon1 on nAttack* / cAttack* (`checks/fx_bat_research/attacks_emotes/clip_calls.txt`); Hate Transfer
plays cast3 (the cast reports' scope).

Line numbers are `D:\12tails\DecompiledSource\Bat.cs` unless another file is named. Times are seconds from the start of
the clip the cue is keyed by. Distance 0 = at the hero. Every opaque predicate (`if (a - b != c) continue;`) on the paths
below was worked by hand; each goes the normal way (the notable ones are named).

Probes (read only, nothing written outside `checks/fx_bat_research/attacks_emotes/`):
- `wardrobe_fx.py bat --probe nAttack,nAttack_hit,drainLife,drainLife_charge,drainLife_hit,deadEffect,dreamBurst_hit` -> `probe.txt`;
- `probe_fields.py` (the Bat hero prefab's `Bat` MonoBehaviour, its GameObject PPtrs in field order) -> `probe_fields.txt`;
- `probe_events.py` (AnimationEvents on every class's clips) -> `probe_events.txt`, `probe_events_all.txt`;
- `geom.py` (the bolt geometry) -> `geom.txt`; `homing.py` (the Homing Wand path) -> `homing.txt`;
- the `clip_flow.js` dumps `RPC_nAttack1.txt` ... `RPC_activateIcon1.txt`.
TTO: `DecompiledSource_TTO_2026-11-02\pseudo\Bat.c` (constants only; the cues are BB's).

---

## Read this first

1. **Two SEQ step-time errors** (index.html work, not a cue job). Today: `"Normal Attack: nAttack1 nAttack2 nAttack3"`,
   `"Drain Life: cAttack1 cAttack2*"`.
   - **Normal Attack.** The game starts nAttack2 **0.6 s** after stage 1 and nAttack3 at **1.2 s** (the dispatcher
     section). The page plays the whole clips (nAttack1 0.8 s, nAttack2 0.8 s, `data/bat/clips.json`), so stage 2 starts
     0.2 s late and stage 3 at 1.6 s, 0.4 s late. Both later stages cut in (`PlayAnimation(x, 0)` :20664, :21079): no
     `~`. Proposed: **`"Normal Attack: nAttack1@0.6 nAttack2@0.6 nAttack3"`** (the first step keeps the page's 0.2 s fade,
     as the Sheep's and the Penguin's; the game's cut would be `nAttack1!@0.6`).
   - **Drain Life.** cAttack1 lasts 0.2 + 0.2 + 0.3 = 0.7 s (its clip's own length: no `@` needed), then cAttack2 cuts in
     looped (`PlayAnimation("cAttack2", 0)` :21762-21767). The hold has no fixed length (the channel runs until the
     release). Proposed: **`"Drain Life: cAttack1 cAttack2*@6.2"`**: five drain ticks (1-5 s) and Dream Burst's first
     burst at 6.0 s (passives on, Dream Burst 3, question 3); the plain three-tick hold would be `cAttack2*@3.2`.
2. **Drain Life needs a target.** With none, RPC_cAttack1 ends at once, before its clip (`!tObject` -> Block_63 ->
   `return false`, :22355-22362), and `doBeginCharge` will not even start it (:10369-10373; an ally or NPC is refused
   too, :10417-10437). So the tile is a picture of a drain on the 10 m target (the standing rule), as the Penguin's
   charge ring is: the bolt runs to the target 0.6 m up (decision 3), the drain ticks every 1 s.
3. **A BB (and TTO) bug in the drain tick's hit flash.** The Bat's own client spawns `drainLife_hit` at **her own
   position** (`RPC_cAttack_hit(this.position, ...)` :22182), while the network message sends **the target's**
   `collider.bounds.center` (:22193), and a Shadow Illusion clone uses the target's centre both ways
   (`Bat_illusion.cs:4685`, :4698). TTO1102 keeps the split (pseudo/Bat.c:3386-3405). The cues below put it at the
   target point 0.6 m up (question 2); offer the bug to the user for the Bible.
4. **Hero-played sounds (`"sound"` cues).** Unlike the Penguin's, the Bat's bolt has no AudioSource: the hero's code plays
   `Sounds/nAttack` itself, once per shot (three bolts, one sound: RPC_nAttack_fire2 :10933-10943), and Dream Burst's
   `Sounds/dreamBurst_hit` (RPC_dreamBurst_hit :13952 ff.). Both are `"sound"` cues. The effects that bring their own
   sound: `nAttack_hit` (AudioSource nAttack_hit), `drainLife` (AudioSource drainLife, **looped**, until the release).
5. **Inventory gaps.** Five of the effects here are hero-prefab fields, not `Resources.Load` paths, so
   `plans/fx_inventory.md` "### bat" misses them (`probe_fields.txt`: the Bat MonoBehaviour's PPtrs in field order,
   matched to the field declarations :19572-19614):

   | field (Bat.cs) | prefab | parts (probe) | state |
   |---|---|---|---|
   | `nAttack_fire` :19587 | `nAttack` | Bat_nAttack, ProjectileControl, 2 ImageEmitter, VortexEmitter, TrailRenderer | needs **Bat_nAttack** |
   | `nAttack_hit` :19593 | `nAttack_hit` | EffectControl (life 1), AudioSource nAttack_hit, 2 RingEmitter, LineEmitter | ready |
   | `Bat_drainLife` :19596 | `drainLife` | **BoltEmitter**, AudioSource drainLife (loop), **Light** (point), ImageEmitter | needs **Light** + the BoltEmitter target (below) |
   | `Bat_drainLife_charge` :19599 | `drainLife_charge` | LineEmitter, EffectControl (life 999, followState, followPosition) | ready |
   | `cAttack_hit` :19608 | `drainLife_hit` | ImageEmitter, EffectControl (life 1) | ready |

   (`wingFlap` :19572 is the AudioClip `step_fly1`; `castEffect` / `castRing` are the cast reports'.) `deadEffect`
   (Resources.Load :53740) and `dreamBurst_hit` (:13989) are in the inventory, ready.
6. **The bolt's no-target aim is the 10 m ground point exactly.** GameGui aims a click with no target at
   `position + 10 forward` (GameGui.cs:1659) and a targeted one at the enemy's `collider.bounds.center`
   (:1626); the Bat's dispatcher passes it on unchanged (no Penguin-style 0.25 m drop): `tDir = a - position`, except
   within 3 m, where it becomes `4 flat(dir) + up` (:9886-9895). So decision 1's picture (the bolt ends on the ground at
   the 10 m point) is here also the game's own untargeted shot, centre path. The 0.4 m trigger sphere (nAttack.prefab
   `m_Radius: 0.4`, trigger, no gravity) would really touch flat ground at 7.23 m after 0.42 s (`geom.txt`), not
   counted, as the Sheep's and the Penguin's (question 1).
7. **Stage 3's landings come after its 1.0 s clip** (1.1062 / 1.1276 s). Played once (the default), the page keeps a
   skill's later cues running in the idle tail (index.html `play(idleName(), true)`, "its effects and later cues run
   on"), so they come at their times. With วนซ้ำ on, `fxDue` fires them at the step's end (1.0 s), 0.1 s early. An
   `nAttack3@1.2` step would hold the clip's last frame 0.2 s instead; not proposed.
8. **The run clip has a sound.** `run` carries an AnimationEvent `playWingFlapEvent` at 0.1 s (`probe_events.txt`), which
   plays `wingFlap` = `step_fly1` (Bat.cs:101-140; own hero, or anyone in a mission: `mGameType > 4`), every cycle of the
   run. The Wolf, Sheep and Penguin clips carry no events (`probe_events_all.txt`: only the Bat's wing flap and the
   Bison / Chameleon / Monkey / Panda / Whale footsteps on `run`), so the earlier classes' "run: nothing" holds. Two
   small jobs to make it play (question 5): `step_fly1.wav` is in `Resources/sound/fx/`, which `wardrobe_fx.py`'s
   `--sounds` path does not search (`rip_wav(cls, n, "sounds")` looks only in the class's `sounds/`), and the page says
   a basic move's cues once per pick (`!S.round`, index.html startStep), not on each loop of the run.
9. **No rolls here.** Combo 3 (#103) is a rank: at max rank stage 3 always fires three bolts (:21227). There is no
   Spread-Shot-like proc on the Bat's combo, and no voice gate on the charge (the Penguin's 2 s gate has no Bat twin).
10. **Name collisions.** The cue kind picks the folder (voices are `v_<name>`):
    - `nAttack1`-`nAttack3`, `cAttack1`, `cAttack2` are clip names and `voices/` files; `nAttack4` is a voice only.
    - `nAttack` is an effect (the bolt, no sound of its own) and a `sounds/` file (the hero's shot sound).
    - `nAttack_hit`, `drainLife`, `dreamBurst_hit` are effects and `sounds/` files; the first two play theirs themselves,
      `dreamBurst_hit` (no AudioSource) is played by the hero's code: a `"sound"` cue.

---

## The dispatcher: Normal Attack stage times (SEQ check)

`doNormalAttack` (:9834-10320; own client; not in game code 967, :9848):
- **Stage 1** when standby / run and the `nAttack` lock is free (:10010-10022, :10239): RPC_nAttack1 (:10245).
- **Stage 2:** while `myCommand == "nAttack1"`, with Combo #101 (:10037), only when `actionTime + 0.3 < now <
  actionTime + 0.6` (:10047 breaks at `<= +0.3`, :10055 at `>= +0.6`): RPC_nAttack2 (:10063).
- **Stage 3:** while `myCommand == "nAttack2"`, with #102 (:10150), once `now > actionTime + 0.9` (:10160): RPC_nAttack3
  (:10168). The window closes at stage 2's standby, stage 1 + 1.2 s.
- **actionTime is not reset by stages 2 / 3** (their entry sets only `actionState` and `myCommand`, :20859-20862,
  :21342-21345), so each stage waits a fixed time after stage 1:
  - RPC_nAttack2: `Yield(2, actionTime - now + 0.6)` (:20881): **the nAttack2 clip starts at 0.6 s**;
  - RPC_nAttack3: `Yield(2, actionTime - now + 1.2)` (:21360): **the nAttack3 clip starts at 1.2 s**.
- Stage 1's standby at 0.6 s checks `myCommand == "nAttack1"` (:20300), stage 2's at its 0.6 s checks `"nAttack2"`
  (:20801): each is skipped once the next stage is pressed.
- The Bible matches the windows (`bat-skill-reference.md:289`: "pressed 0.3-0.6 s after stage 1", "after 0.9 s"); the
  fixed clip starts are not in it (offer below).
- Shadow Illusion clones repeat each stage from their own spot (:10080-10125, :10185-10230, :10260-10305): no clones in
  the wardrobe (they are Shadow Illusion's summons), left out.
- TTO1102: the same constants (`<RPC_nAttack1>d__145` pseudo/Bat.c:16233: 0.3, 1.5; `d__146` :16562: 0.3, 0.6, 1.5;
  `d__147` :16898: 0.5, 0.2, 1.2, 2, `Range(0, 2)`).

Steps: nAttack1 0 to 0.6, nAttack2 0.6 to 1.2, nAttack3 from 1.2 to its clip's end (1.0 s; its standby at 0.7 s).
**Proposed SEQ:** `"Normal Attack: nAttack1@0.6 nAttack2@0.6 nAttack3"`.

## The dispatcher: Drain Life (SEQ check)

- `doBeginCharge` (:10324-10585): a target is required, not the Bat, within `16 + 12 x Dark Intention` m (16, or 28 with
  #411: :10385-10406), not an ally or NPC (:10417-10437), standby or run (:10460-10474), #111 (:10475), not within 1 s
  of the last action (:10490); then RPC_cAttack1 with the target's ActorNr (:10496).
- `doReleaseCharge` (:10588-10720): while `actionState "attack"` and `myCommand "cAttack1"`: **RPC_cAttack0** (:10642).
  RPC_cAttack0 (:22646-22816): `myCommand "cAttack0"` (:22795), `CrossFade("root", 0.35)` (:22804), standby 0.35 s later
  (`Yield(2, 0.35)` :22815, :22764). No voice, no effect.
- The loop (case 5, every frame) ends on the next frame after the release: `myCommand != "cAttack1"` skips the drain
  block and the coroutine destroys the bolt and the charge lines at once (`Object.Destroy`, :22270-22293).

**Proposed SEQ:** `"Drain Life: cAttack1 cAttack2*@6.2"` (question 3 for the hold).

---

## nAttack1 (Normal Attack, stage 1)

Coroutine `$RPC_nAttack1$19844` (:20108-20500).

| t (s) | what | source |
|---|---|---|
| 0 | `actionState "attack"`, `actionTime`, `myCommand "nAttack1"`, `addTimeOut("nAttack", 1.5)`, LookAt, clip nAttack1 (cut), voice `Voices/nAttack1` (1.0 own, 0.75 others); wait 0.3 | :20358-20376, load :20423, PlayOneShot :20461, `Yield(2, 0.3)` :20457 |
| 0.3 | own client, `mGameType > 3` (:20254): fire point `mPos + TransformDirection(0, 1.3, 1)` (:20262), aim `tDir - TransformDirection(0, 1.3, 1)` (:20267), RPC_nAttack_fire1 (:20272); wait 0.3 | `Yield(3, 0.3)` :20464 |
| 0.6 | standby, unless stage 2 was pressed | :20294-20316 |

- **RPC_nAttack_fire1** (:10746-10832): `Instantiate(nAttack_fire, firePos, FromToRotation(forward, fireDir))` (:10753),
  ProjectileControl life `1.25 x rangeMod` (:10762); with the Homing Wand (`weapon == "w_bat59"`) and a target,
  `Bat_nAttack.InitHoming(tID)` (:10765-10788); the hero's `audio.PlayOneShot(Sounds/nAttack)` (:10802-10812).
- **The bolt** (`Bat_nAttack.cs`): Awake sets `rigidbody.velocity = TransformDirection(ProjectileControl.velocity)` (:51)
  = the prefab's (0, 0, 15) = **15 m/s** (probe); FixedUpdate destroys it at its life (:86-95); homing only with a target
  set (:101-122). OnTriggerEnter (:138 ff.): on any collider not on the owner's layer and not layer 1 / 2 (:181-197) it
  destroys itself (:199) and, on the owner's client, calls `RPC_nAttack_hit` at `ClosestPointOnBounds` (:208, :243)
  **before** the Player / Enemy test (:261), so the floor counts. RPC_nAttack_hit (:10972-10975):
  `Instantiate(nAttack_hit, hitPos, hero rotation)`; nAttack_hit plays its own Sounds/nAttack_hit.
- **Geometry** (`geom.txt`; aimed at the 10 m ground point, the centre path): aim (0, -1.3, 9), pitch atan(1.3 / 9) =
  **8.219 deg** down; path sqrt(81 + 1.69) = 9.0934 m, 9.0934 / 15 = **0.6062 s**; it lands 0.3 + 0.6062 = 0.9062 s
  after stage 1 = **0.3062 s into nAttack2**. (Life 1.25 s = 18.75 m: never the limit here.)
- Left out: `onNormalAttackHit`'s weapon procs, the SP gain and Amplify Damage (Bat_nAttack.cs:276-363): only on an enemy
  actually hit, nothing drawn by the Bat.

```json
  "nAttack1": {
    "why": "Bat.cs RPC_nAttack1 (:20108-20500): clip at 0 (cut, :20376) with voice nAttack1 (load :20423, PlayOneShot :20461); 0.3 s (Yield(2, 0.3) :20457) the shot, own client, mGameType > 3 (:20254): RPC_nAttack_fire1 (:20272) Instantiate(nAttack_fire = the prefab nAttack, firePos, FromToRotation(forward, fireDir)) (:10753; field order checks/fx_bat_research/attacks_emotes/probe_fields.txt) from TransformDirection(0, 1.3, 1) (:20262), aimed tDir - (0, 1.3, 1) (:20267) at the 10 m target point on the ground (decision 1; the game's own untargeted click, position + 10 forward, GameGui.cs:1659, passed on unchanged :9886): pitch atan(1.3 / 9) = 8.219 deg; Bat_nAttack flies it 15 m/s (ProjectileControl.velocity (0, 0, 15), Bat_nAttack.cs:51) and ends it on the ground (:181-199; the 0.4 m trigger not counted); the hero's code plays Sounds/nAttack (:10802-10812; the bolt has no AudioSource); to = the target 0.6 m up, used only by the Homing Wand (w_bat59 = specialWand, :10765-10788); standby 0.6 s (Yield(3, 0.3) :20464, :20306) unless stage 2 is pressed (stage 2 starts at 0.6 s: its entry carries this bolt's landing at 0.3 + 0.6062 - 0.6 = 0.3062 s)",
    "cues": [
    [0, "voice", "nAttack1"],
    [0.3, "fx", "nAttack", {"d": 1, "y": 1.3, "rot": [8.219, 0, 0], "to": [0, 0.6, 10]}],
    [0.3, "sound", "nAttack"]
    ]
  },
```

Sure: high on the trace and the times; the landing is the decision-1 picture.

## nAttack2 (stage 2)

Coroutine `$RPC_nAttack2$19855` (:20506-20900). Started by a press 0.3-0.6 s into stage 1; its clip starts at stage 1 +
0.6 s (`Yield(2, actionTime - now + 0.6)` :20881).

| t (s, from its clip) | what | source |
|---|---|---|
| 0 | position, LookAt, `addTimeOut("nAttack", 1.5)`, clip nAttack2 (**cut**), voice `Voices/nAttack2`; wait 0.3 | :20644-20669, load :20711, PlayOneShot :20877, `Yield(3, 0.3)` :20875 |
| 0.3 | the shot as stage 1 (`mGameType >= 5`, :20755; :20763-20773); wait 0.3 | `Yield(4, 0.3)` :20870 |
| 0.6 | standby, unless stage 3 is pressed | :20795-20817 |

- Sums: voice 0; shot 0.3 (stage 1 + 0.9); standby 0.6 (stage 1 + 1.2).
- In this step: stage 1's bolt lands at **0.3062 s**. This stage's own lands at 0.9 + 0.6062 - 1.2 = 0.3062 s into nAttack3.

```json
  "nAttack2": {
    "why": "Bat.cs RPC_nAttack2 (:20506-20900; its clip 0.6 s after stage 1: Yield(2, actionTime - now + 0.6) :20881, the press window 0.3-0.6 s, doNormalAttack :10047-10063): clip at 0 (cut, :20664) with voice nAttack2 (load :20711, PlayOneShot :20877); 0.3 s (Yield(3, 0.3) :20875) the shot as in nAttack1 (:20763-20773; RPC_nAttack_fire1 :10753, Sounds/nAttack :10812); standby 0.6 s (Yield(4, 0.3) :20870, :20807) unless stage 3 is pressed; at 0.3062 s stage 1's bolt meets the ground at the 10 m point (0.3 + 9.0934 m / 15 m/s - 0.6; checks/fx_bat_research/attacks_emotes/geom.txt): Bat_nAttack calls RPC_nAttack_hit at the contact point before any Player / Enemy test (Bat_nAttack.cs:208-261), nAttack_hit there with the hero's rotation (:10974; plays its own Sounds/nAttack_hit); with the Homing Wand worn the bolt homes on the target instead (question 4)",
    "cues": [
    [0, "voice", "nAttack2"],
    [0.3, "fx", "nAttack", {"d": 1, "y": 1.3, "rot": [8.219, 0, 0], "to": [0, 0.6, 10]}],
    [0.3, "sound", "nAttack"],
    [0.3062, "fx", "nAttack_hit", {"d": 10}]
    ]
  },
```

## nAttack3 (stage 3)

Coroutine `$RPC_nAttack3$19866` (:20921-21372). Started by a press after 0.9 s; its clip starts at stage 1 + 1.2 s
(`Yield(2, actionTime - now + 1.2)` :21360).

| t (s, from its clip) | what | source |
|---|---|---|
| 0 | position, LookAt, `addTimeOut("nAttack", 2)`, clip nAttack3 (**cut**); voice `nAttack3` or `nAttack4` (`Random.Range(0, 2) == 0`); wait 0.5 | :21059-21084, :21120, loads :21132 / :21164, PlayOneShot :21353 / :21362, `Yield(3, 0.5)` :21369 |
| 0.5 | the shot (`mGameType >= 5`, :21209; :21217-21222): with Combo 3 #103 (max rank: on) **RPC_nAttack_fire2** (:21227-21233); wait 0.2 | `Yield(4, 0.2)` :21356 |
| 0.7 | standby | :21278-21300 |

- **RPC_nAttack_fire2** (:10836-10968): `lhs = FromToRotation(forward, fireDir)` with its roll zeroed (:10844-10858);
  for i = -1, 0, 1: `Instantiate(nAttack_fire, firePos + i x transform.right, lhs x Euler(0, 15 i, 0))` (:10868), each
  with life 1.25 and the wand's homing (:10883-10916); **one** Sounds/nAttack after the loop (:10927-10943).
- Geometry (`geom.txt`): the side bolts start 1 m to the side, Unity Euler **(7.937, +-15.149, +-2.141)**, and meet the
  ground after 9.4142 m = **0.6276 s** at x +-3.4366, d 10.0; the centre one as before, 0.6062 s.
- Landings in this step: stage 2's bolt at **0.3062**; this stage's centre at 0.5 + 0.6062 = **1.1062**, its sides at
  0.5 + 0.6276 = **1.1276** (after the 1.0 s clip: Read this first 7).

```json
  "nAttack3": {
    "why": "Bat.cs RPC_nAttack3 (:20921-21372; its clip 1.2 s after stage 1: Yield(2, actionTime - now + 1.2) :21360, the press from 0.9 s, doNormalAttack :10160-10168): clip at 0 (cut, :21079) with voice nAttack3 or nAttack4 (Random.Range(0, 2) :21120, loads :21132 / :21164, PlayOneShot :21353 / :21362); 0.5 s (Yield(3, 0.5) :21369) Combo 3 #103 on (max rank, :21227): RPC_nAttack_fire2's three bolts (:21233) at firePos + i x right, lhs x Euler(0, 15 i, 0) with lhs's roll zeroed (:10844-10868; Unity Euler (7.937, +-15.149, +-2.141), checks/fx_bat_research/attacks_emotes/geom.txt) and one Sounds/nAttack (:10933-10943); standby 0.7 s (Yield(4, 0.2) :21356, :21290); the landings at the 10 m line (Bat_nAttack.cs:208-261, nAttack_hit with the hero's rotation :10974, its own Sounds/nAttack_hit): stage 2's bolt 0.9 + 0.6062 - 1.2 = 0.3062 s, this stage's centre 0.5 + 0.6062 = 1.1062 s and its sides 0.5 + 9.4142 / 15 = 1.1276 s at x +-3.4366 (after the 1.0 s clip: they run on in the idle tail)",
    "cues": [
    [0, "voice", "nAttack3|nAttack4"],
    [0.3062, "fx", "nAttack_hit", {"d": 10}],
    [0.5, "fx", "nAttack", {"d": 1, "x": -1, "y": 1.3, "rot": [7.937, -15.149, -2.141], "to": [0, 0.6, 10]}],
    [0.5, "fx", "nAttack", {"d": 1, "y": 1.3, "rot": [8.219, 0, 0], "to": [0, 0.6, 10]}],
    [0.5, "fx", "nAttack", {"d": 1, "x": 1, "y": 1.3, "rot": [7.937, 15.149, 2.141], "to": [0, 0.6, 10]}],
    [0.5, "sound", "nAttack"],
    [1.1062, "fx", "nAttack_hit", {"d": 10}],
    [1.1276, "fx", "nAttack_hit", {"d": 10, "x": -3.4366}],
    [1.1276, "fx", "nAttack_hit", {"d": 10, "x": 3.4366}]
    ]
  },
```

Sure: high on the trace. The 0.3062 s cues depend on the proposed SEQ (steps of exactly 0.6 s).

### The Homing Wand variant (question 4; only if the user says yes)

With `w_bat59` (the wardrobe's `specialWand`, `data/item_map.json`) and a target, each bolt turns 0.1 rad towards the
target's `collider.bounds.center` every 0.1 s and flies 16 m/s after the first turn (Bat_nAttack.cs:101-122, the 16 from
the constructor :26). Simulated at 50 FixedUpdates / s (`homing.txt`): the centre bolt passes the target centre (10 m,
0.6 up) at **0.56 s** (0.07 m off), the side bolts at **0.58 s** (x +-0.32, d 10.09): they hit the enemy, not the floor.
That needs a `worn [slot, item]` cue option (the mirror of `notWorn`, index.html fxStart) and the wand's homing in the
Bat_nAttack part (it reads the cue's `to`). The ground hits above get `"notWorn": ["R", "specialWand"]`, and these are
added (times from the clip each lands in):

```json
    [0.26, "fx", "nAttack_hit", {"d": 10, "y": 0.6, "worn": ["R", "specialWand"]}],
```
in nAttack2 (stage 1's bolt: 0.3 + 0.56 - 0.6), and in nAttack3:
```json
    [0.26, "fx", "nAttack_hit", {"d": 10, "y": 0.6, "worn": ["R", "specialWand"]}],
    [1.06, "fx", "nAttack_hit", {"d": 10, "y": 0.6, "worn": ["R", "specialWand"]}],
    [1.08, "fx", "nAttack_hit", {"d": 10.09, "x": -0.32, "y": 0.54, "worn": ["R", "specialWand"]}],
    [1.08, "fx", "nAttack_hit", {"d": 10.09, "x": 0.32, "y": 0.54, "worn": ["R", "specialWand"]}]
```
(The hit point is really where the 0.4 m sphere first meets the enemy's collider, a little earlier and nearer: an
approximation, as every target-point cue is.)

---

## cAttack1 (Drain Life: the wind-up)

Coroutine `$RPC_cAttack1$19877` (:21410-22552), start at IL_1123 (:22348).

| t (s) | what | source |
|---|---|---|
| 0 | the target from tID; none = the coroutine ends (:22355-22362); position, LookAt the target (flat), `actionState "attack"`, `actionTime`, `myCommand "cAttack1"`, clip cAttack1 (cut, Once); voice `cAttack1` or `cAttack2` (`Random.Range(0, 2) == 0`), no time gate; wait 0.2 | :22379-22409, :22441-22548 (loads :22451 / :22482, PlayOneShot :22548 / :22541), `Yield(2, 0.2)` :22535 |
| 0.2 | `moveSpeed -0.5` (a small step back: no hero mover in the wardrobe, Penguin decision 8); wait 0.2 | case 2 :21553, `Yield(3, 0.2)` :22524 |
| 0.4 | `moveSpeed 0`; **drainLife_charge** at `position + 1.2 up`, `Quaternion.identity` (:21580), `InitEffectControl(hero)` (:21590); wait 0.3 | case 3, `Yield(4, 0.3)` :22522 |
| 0.7 | case 4: cAttack2 (the next entry) | :21596-21844 |

- `drainLife_charge` (probe): LineEmitter (repeatForever) + EffectControl life 999, **followState**, followPosition. It
  goes at the release: the loop's `Object.Destroy` (:22282-22288) on the first frame after RPC_cAttack0 sets
  `myCommand "cAttack0"` (:22795). Its rotation is the world's identity: the page's hero faces +z at the origin
  (fxparts/penguin.js header: "Unity's world, the hero's feet at the origin, +z her facing"), so no `rot`.
- **Its end, `kill` not `cut`:** the page's `cut` compares the cue with `FX.t`, which restarts at each step (fxStart),
  and the release comes in the next step. The game's end is a Destroy, so `kill` (seconds after the spawn) fits:
  0.3 s left of cAttack1 + the 6.2 s hold - 0.05 (just inside the step, as the Penguin's 2.95) = **6.45** (with a 3.2 s
  hold: 3.45).
- TTO1102 `<RPC_cAttack1>d__151` (pseudo/Bat.c:2253-3620): the same constants (1.2, 0.82, 0.88, 0.1, 1.25, 0.65, 8,
  `Range(0, 2)`).

```json
  "cAttack1": {
    "why": "Bat.cs RPC_cAttack1 (:21410-22552), a drain on the 10 m target (with none the coroutine ends before its clip, :22355-22362; doBeginCharge needs an enemy within 16 / 28 m, :10369-10406): clip at 0 (cut, :22406) with voice cAttack1 or cAttack2 (Random.Range(0, 2) :22441, loads :22451 / :22482, PlayOneShot :22548 / :22541; no time gate); 0.2 s (Yield(2, 0.2) :22535) moveSpeed -0.5 (no hero mover); 0.4 s (Yield(3, 0.2) :22524) drainLife_charge (the field Bat_drainLife_charge) at position + 1.2 up, Quaternion.identity (:21580), EffectControl followState (life 999): destroyed by the loop the frame after the release (:22282-22288, RPC_cAttack0 sets myCommand cAttack0 :22795): kill 0.3 + the 6.2 s cAttack2 hold - 0.05 = 6.45 (FX.t restarts with the cAttack2 step, so a cut cannot reach it); at 0.7 s (Yield(4, 0.3) :22522) the looped cAttack2, whose entry holds the drain",
    "cues": [
    [0, "voice", "cAttack1|cAttack2"],
    [0.4, "fx", "drainLife_charge", {"y": 1.2, "kill": 6.45}]
    ]
  },
```

## cAttack2 (Drain Life: the drain)

Same coroutine, case 4 at cAttack1 + 0.7 s, then case 5 every frame (`YieldDefault(5)` :22531).

| t (s, from cAttack2) | what | source |
|---|---|---|
| 0 | range check (`(16 + 12 DarkIntention)^2`, :21612; too far = release, :21684-21711); clip **cAttack2 (cut, Loop)**; **drainLife** at `position + TransformDirection(0, 0.82, 0.88)`, identity (:21772); `drainLifeTimer = now + 1` (:21782); levels: Drain Life, Drain Mana, Merciless Drain, Dream Burst, Amplify Damage (:21787-21839); `dreamBurstTimer = drainLifeTimer + 8 - DreamBurstLv` (:21833) | :21596-21844 |
| 0 (same frame), every frame | while `attack` / `cAttack1` with a target: LookAt the target (flat), **drainLife moved to `position + TransformDirection(0.1, 1.25, 0.65)`** (:21967), its `BoltEmitter.TargetPosition = target.collider.bounds.center` (:21972); range check again (:21983-22064) | :21854-21976 |
| 1, 2, 3, 4, 5 | the tick (`drainLifeTimer < now`, :22066-22074): hpDrain / mpDrain / spDrain statuses on the target (:22146-22181), **RPC_cAttack_hit** (:22182; the network copy at the target's bounds centre :22193), SP + 1 (:22199), Amplify Damage (:22204-22231), Merciless Drain's 66 (:22233-22267) | :22066-22267 |
| 6 | Dream Burst 3 (#363, max rank; passives on): `dreamBurstTimer` 0.7 + 1 + 8 - 3 = 6.7 from cAttack1 = **6.0 here** is passed at the sixth tick: `hit(363, target, ...)` (:22112) and **RPC_dreamBurst_hit** (:22117), and that second's drain is skipped (Block_89 -> IL_D23, :22131-22133); the next burst would come 6 s later | :22087-22135, getDreamBurstLv :13908 |
| release | the frame after RPC_cAttack0: `Object.Destroy(drainLife)` and the charge lines (:22270-22293) | |

- **drainLife** (probe): a BoltEmitter (3 bolts, Height 0.2, widths 0.05-0.1, violet, TargetNode -1: it draws to
  `TargetPosition`, which the code sets each frame), a Point light (colour (1, 0.53, 1), intensity 1, range 2), an
  ImageEmitter (repeatForever) and its AudioSource `drainLife`, **looped**. No EffectControl: only the coroutine's Destroy
  ends it, so **kill 6.15** (the 6.2 s hold - 0.05). The spawn point (0, 0.82, 0.88) is overwritten in the same frame
  (case 4 breaks out of the switch into the per-frame block, :21844 -> :21854), so the cue uses (0.1, 1.25, 0.65).
  The target: `collider.bounds.center` = 10 m ahead, 0.6 m up (decision 3): `"to": [0, 0.6, 10]`.
- **drainLife_hit** (probe): EffectControl life 1, one ImageEmitter growing 1 -> 2.4 m over 0.2 s. At the target's
  centre (question 2; the Bat's own client draws it at her feet).
- **RPC_dreamBurst_hit** (:13952-14030): `createEffect(dreamBurst_hit, target.collider.bounds.center - 0.4 x hitDir,
  hero rotation)` with `hitDir` = the Bat's forward (:22117): **9.6 m ahead, 0.6 up**; then the hero's
  `audio.PlayOneShot(Sounds/dreamBurst_hit)` (the prefab has no AudioSource: Animation + EffectControl life 1 / afterLife
  1, followPosition; dreamBurst_tri StaticMesh + AlphaTimer; a LineEmitter: ready).
- Nothing drawn: the drain statuses (CharacterControl.cs:33488-33610: damage numbers, `RPC_AddHeal(66, ...)` on the Bat,
  no effect, :7130-7390), Amplify Damage, Merciless Drain's 66 and its "Merciless Drain!" text.
- Drain Mana #121-123 and Merciless Drain #421 only add statuses (max rank: on; nothing drawn). Dark Intention #411 only
  raises levels and the range.

```json
  "cAttack2": {
    "why": "Bat.cs RPC_cAttack1 case 4 (the change to cAttack2, cut and looped, 0.7 s in: :21762-21767), its loop every frame (case 5, :21854-22267) on the 10 m target: drainLife (the field Bat_drainLife: BoltEmitter, Point light, its own looping Sounds/drainLife) spawned at TransformDirection(0, 0.82, 0.88) (:21772) and moved the same frame, and every frame, to position + TransformDirection(0.1, 1.25, 0.65) (:21967), the bolt's TargetPosition = the target's collider.bounds.center (:21972; 0.6 m up, decision 3: to); no EffectControl: Object.Destroy the frame after the release (:22270-22281): kill 6.15 in the 6.2 s step; the tick every 1 s (drainLifeTimer = now + 1, :21782, :22066-22074): RPC_cAttack_hit, drainLife_hit (the field cAttack_hit) with the hero's rotation (:10995) at the target point 0.6 m up, where the network copy and the clones draw it (:22193; Bat_illusion.cs:4685) (the Bat's own client draws it at her feet, :22182, a BB and TTO bug); Dream Burst 3 on (#363, passives rule, getDreamBurstLv :13908): dreamBurstTimer = 0.7 + 1 + 8 - 3 (:21833) passed at the sixth tick, 6.0 s here: RPC_dreamBurst_hit (:22117) createEffect(dreamBurst_hit, target centre - 0.4 x the Bat's forward, the Bat's rotation) (:13952 ff.: 9.6 m ahead, 0.6 up) and the hero's Sounds/dreamBurst_hit, that second's drain skipped (:22131-22133); the statuses, the heal and Merciless Drain's 66 draw nothing (CharacterControl.cs:33488-33610)",
    "cues": [
    [0, "fx", "drainLife", {"d": 0.65, "x": 0.1, "y": 1.25, "to": [0, 0.6, 10], "kill": 6.15}],
    [1, "fx", "drainLife_hit", {"d": 10, "y": 0.6}],
    [2, "fx", "drainLife_hit", {"d": 10, "y": 0.6}],
    [3, "fx", "drainLife_hit", {"d": 10, "y": 0.6}],
    [4, "fx", "drainLife_hit", {"d": 10, "y": 0.6}],
    [5, "fx", "drainLife_hit", {"d": 10, "y": 0.6}],
    [6, "fx", "dreamBurst_hit", {"d": 9.6, "y": 0.6}],
    [6, "sound", "dreamBurst_hit"]
    ]
  },
```

With the 3.2 s hold instead (question 3): keep the first four cues with `kill` 3.15 (and 3.45 on drainLife_charge), drop
the 4 / 5 / 6 s ones. Sure: high on the trace; the tick moments are frame-quantised in the game (the first frame after
each whole second).

---

## activateIcon1 (clip cAttack2): no tile (Penguin decision 19)

The mission "activate the icon" channel every class has: RPC_activateIcon1 (`$RPC_activateIcon1$20692`, :52681-53020)
plays cAttack2 looped with a 0.5 s fade (:52892-52895), voice `activate1` at the start (:52939-52951), a cast bar
(`castTime`, :52841); RPC_activateIcon2 (:19270) ends it with `activate2`. As the Penguin's: no tile, no entry.

---

## Emotes and basic moves

`RPC_emotion` (`$RPC_emotion$20534`, :47093-47960) works as the other classes':
- The voice plays at 0, **before** the clip (:47278-47363), when the voice option is on (:47278), more than 2 s after
  the last action (:47284), and the hero is the player's own, a mission teammate or anyone in game code 31
  (:47290-47318).
- `emo_chat` -> `Voices/chat` + `Random.Range(1, 4)` = **chat1-3 only** (:47336; the rip has chat1-5, and TTO plays 1-5:
  `BaseHero::EmotionVoiceClip`, pseudo/BaseHero.c:16170-16230, with `get_ChatVoiceCount` = 5 :16102, the Bat not
  overriding it); every other `emo_<name>` -> `Voices/<name>` (`Substring(4)`, :47344), `PlayOneShot` volume 1 (:47356).
- Then `actionState "emotion"` and the clip with a 0.2 s fade. No effect and no Sounds/ anywhere in RPC_emotion.

| emote | clip | voice (voices/) | source |
|---|---|---|---|
| emo_hi, emo_wave | wave | hi / wave | :47410, :47418 -> :47899 |
| emo_ty, emo_bow | bow | ty / bow | :47428, :47435 -> :47885 |
| emo_laugh | laugh | laugh | :47442-47448 |
| emo_sit | sit | none | :47462-47468 |
| emo_sleep | sleep | sleep | :47474-47480 |
| emo_cheer | cheer | cheer | :47486-47492 |
| emo_beg | beg | beg | :47498-47504 |
| emo_cry | cry | cry | :47510-47516 |
| emo_talk, emo_chat | talk | talk: none; chat: chat1-3 | :47524, :47531 -> :47863 |
| emo_pose | pose5 / 15 / 25 / 35 / 45 / 58 / 65 / 46 / 66 by the worn set (w_bat56 + c_all56: `animation.Stop()`), else pose | none | :47538-47786 |
| emo_battle | battle; with `w_bat65` (the wardrobe's `japanWagasa`) the weapon's own clip toggles `open` / `close` | battle | :47794-47842 |
| emo_dance | dance | none | :47848-47856 |

- wave / bow / laugh play once and go to standby at 1.2 s (`Yield(4, 1.2)` :47949 -> :47243); the rest loop until the
  player moves (:47870, :47921-47936).
- In the rip's `voices/`: hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5; no sit, talk, pose, dance.
- TTO-only emote clips in `clips.json` (clap, wai, cooking, mining, planting, fishingBat, pose37): no BB code plays them;
  TTO gives `emo_clap` the voice `cheer` and `emo_wai` `ty|bow` (BaseHero.c:16190-16224; the "staff" emotes cook / mine
  / plant none). The earlier classes left them silent (NOTES.md 2026-11-10, the Wolf's emote voices): question 6.
- **KO:**
  - `RPC_ko` (`$RPC_ko$20703`, :53058-53432): clip ko (cut, :53272), voice ko1 / ko2 at 0 (`Random.Range(0, 2)` :53307;
    loads :53317 / :53348; PlayOneShot :53397 / :53393); getUp after 3 s (`Yield(2, 3)` :53400 -> :53174), standby 1 s
    later (`Yield(3, 1)` :53391 -> :53198). No effect.
  - `RPC_dead` (`$RPC_dead$20710`, :53434-53790): Rewind + clip ko (:53628-53631); voice dead1 / dead2 at 0
    (:53666-53721); then **always** `Instantiate(deadEffect, hero position, hero rotation)` (:53733-53750; the voice gates
    fall through to IL_1E0, and `79294 - 293003 == -213709` holds at :53748).
  - `deadEffect` (probe): EffectControl life 3, no followState; an ImageEmitter 1 m up (Life 1.2) and two LineEmitters
    0.1 m up (Life 0.4), all after Delay 0.6. Ready.
  - Sheep decision 11: one of the two at random, with each one's voices (the Wolf's and the Penguin's entry).
- **Basic moves:** `run` plays the wing flap at 0.1 s of every cycle (Read this first 8; question 5). getUp, falling,
  root: nothing (no AnimationEvent, no RPC voice). The Bat has no walk clip.

```json
  "wave": {
    "why": "Bat.cs RPC_emotion (:47093): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:47344, PlayOneShot :47356; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_hi (:47410) and emo_wave (:47418) both play the wave clip (:47899): voice hi or wave",
    "cues": [
    [0, "voice", "hi|wave"]
    ]
  },
  "bow": {
    "why": "Bat.cs RPC_emotion (:47093): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:47344, PlayOneShot :47356); no effect, no sound; emo_ty (:47428) and emo_bow (:47435) both play the bow clip (:47885): voice ty or bow",
    "cues": [
    [0, "voice", "ty|bow"]
    ]
  },
  "laugh": {
    "why": "Bat.cs RPC_emotion (:47093): the voice at 0, before the clip, emo_laugh = Voices/laugh (:47344, PlayOneShot :47356); clip laugh (:47448); no effect, no sound",
    "cues": [
    [0, "voice", "laugh"]
    ]
  },
  "sleep": {
    "why": "Bat.cs RPC_emotion (:47093): the voice at 0, before the clip, emo_sleep = Voices/sleep (:47344, PlayOneShot :47356; the Bat has no sounds/sleep); clip sleep (:47480); no effect, no sound",
    "cues": [
    [0, "voice", "sleep"]
    ]
  },
  "cheer": {
    "why": "Bat.cs RPC_emotion (:47093): the voice at 0, before the clip, emo_cheer = Voices/cheer (:47344, PlayOneShot :47356); clip cheer (:47492); no effect, no sound",
    "cues": [
    [0, "voice", "cheer"]
    ]
  },
  "beg": {
    "why": "Bat.cs RPC_emotion (:47093): the voice at 0, before the clip, emo_beg = Voices/beg (:47344, PlayOneShot :47356); clip beg (:47504); no effect, no sound",
    "cues": [
    [0, "voice", "beg"]
    ]
  },
  "cry": {
    "why": "Bat.cs RPC_emotion (:47093): the voice at 0, before the clip, emo_cry = Voices/cry (:47344, PlayOneShot :47356); clip cry (:47516); no effect, no sound",
    "cues": [
    [0, "voice", "cry"]
    ]
  },
  "talk": {
    "why": "Bat.cs RPC_emotion (:47093): every emote's voice at 0, before its clip; emo_chat (:47531) plays the talk clip (:47863) with chat1-3 at random (Random.Range(1, 4), :47336: the Bat's BB code never reaches the rip's chat4 / chat5; TTO plays 1-5); emo_talk (:47524) plays it silent (no Voices/talk): the tile takes the chat's voice; no effect, no sound",
    "cues": [
    [0, "voice", "chat1|chat2|chat3"]
    ]
  },
  "battle": {
    "why": "Bat.cs RPC_emotion (:47093): the voice at 0, before the clip, emo_battle = Voices/battle (:47344, PlayOneShot :47356); clip battle (:47800; with w_bat65, the japanWagasa, the weapon's own open / close clip toggles, :47803-47835: a prop clip, no effect); the battle stance in a fight plays the clip silent: the tile takes the emote's voice",
    "cues": [
    [0, "voice", "battle"]
    ]
  },
  "ko": {
    "why": "Bat.cs RPC_ko (:53058): clip (PlayAnimation(ko, 0) :53272) and voice ko1 or ko2 at 0 (Random.Range(0, 2) :53307, loads :53317 / :53348, PlayOneShot :53397 / :53393), getUp after 3 s (:53400, :53174), no effect; RPC_dead (:53434) plays the same clip (Rewind + ko :53628-53631) with dead1 or dead2 at 0 (:53666-53721) and always puts deadEffect at the hero's position and rotation (:53733-53750; EffectControl life 3): one of the two at random, even chance (the Sheep's decision 11, as wolf.json / penguin.json: roll dead, its voices with it; '!dead' = RPC_ko's)",
    "cues": [
    [0, "voice", "ko1|ko2", {"p": 0.5, "roll": "!dead"}],
    [0, "voice", "dead1|dead2", {"p": 0.5, "roll": "dead"}],
    [0, "fx", "deadEffect", {"p": 0.5, "roll": "dead"}]
    ]
  }
```

Only if question 5 is a yes (it needs the two small jobs in "Parts needed" first, or the check fails on a missing sound):

```json
  "run": {
    "why": "the run clip's AnimationEvent playWingFlapEvent at 0.1 s (checks/fx_bat_research/attacks_emotes/probe_events.txt) -> Bat.cs playWingFlapEvent (:101-140): the hero's audio.PlayOneShot(wingFlap) = step_fly1 (the field :19572, probe_fields.txt; Resources/sound/fx/step_fly1.wav), own hero or anyone in a mission (mGameType > 4, :107-121); every cycle of the run (the event fires each loop)",
    "cues": [
    [0.1, "sound", "step_fly1"]
    ]
  }
```

---

## Parts needed (build stage)

1. **Bat_nAttack** (a new `wardrobe/fxparts/bat.js`, the `nAttack` bolt; the pattern of sheep.js's movers and
   penguin.js's Penguin_nAttack):
   - velocity = TransformDirection(ProjectileControl.velocity) at the spawn (Bat_nAttack.cs:51; the prefab's (0, 0, 15));
     no gravity (prefab `m_UseGravity: 0`); Destroy at ProjectileControl.life, which the hero's code sets to
     1.25 x rangeMod = 1.25 s (Bat.cs:10762, :10883; the prefab's own 2 is overwritten);
   - the end on the ground (decision 1): the bolt goes when its centre reaches y 0 (the 0.4 m trigger not counted);
   - only if question 4 is a yes: with the Homing Wand worn (`api.hero().state.R === "specialWand"`, read at the spawn
     as Bat.cs:10765 reads `weapon == "w_bat59"`), every 0.1 s (first at once) RotateTowards(forward, to - pos, 0.1 rad)
     and velocity = forward x 16 (Bat_nAttack.cs:101-122, :26), the target = the cue's `to`; it ends at the target (when
     its centre comes within the 0.4 m trigger of it).
   - Its children (2 ImageEmitter, VortexEmitter, TrailRenderer) are built parts.
2. **BoltEmitter's target from the cue** (index.html `boltEmitter`, a few lines): with no TargetNode, take
   `fx.at.to` (hero space: right / up / ahead, the cue option RabbitTracer and Penguin.EmperorShot already read) instead
   of the prefab's `TargetPosition` (drainLife's is a stale world point, (250, 54, 150), which draws nothing: `mag >= 50`).
3. **Light** (drainLife's Point light: colour (1, 0.529, 1), intensity 1, range 2, `m_Type 2`): a THREE.PointLight on its
   node, distance = range. The inventory already lists Light for `mindControl_ring` (the cast reports' scope), so one
   part serves both.
4. Only if question 4 is a yes: a `worn [slot, item]` cue option (index.html fxStart, beside `notWorn`).
5. Only if question 5 is a yes: (a) `wardrobe_fx.py`: a `"sound"` cue not in the class's `sounds/` falls back to the rest
   of the rip (`rip_wav`'s anywhere search), for `step_fly1`; (b) the page: an entry flag that replays a basic move's
   cues on every round (the run's loop), e.g. `"everyRound": true` in the entry, read where startStep tests `!S.round`.
6. Add the five hero-prefab fields to the inventory (Read this first 5), as the Penguin's `nAttack_fire`.

Ready as they are: nAttack_hit, drainLife_charge, drainLife_hit, dreamBurst_hit, deadEffect.

## Left out

- Shadow Illusion's clones repeating the combo and the drain (Bat.cs:10080-10305, :21627-21650): no clones on the stage
  (they are another skill's summons).
- The drain's statuses on the target, the heal on the Bat, Amplify Damage, Merciless Drain's 66: numbers and texts only.
- The weapon procs and SP gain on a landed bolt (Bat_nAttack.cs:276-363): only on an enemy actually hit.
- cAttack1's `moveSpeed -0.5` step back (0.2-0.4 s): no hero mover (Penguin decision 8).
- The japanWagasa's open / close on the battle emote (:47803-47835): a prop clip, not an effect (question 8).
- activateIcon1: no tile (Penguin decision 19).

## Open questions (each with the recommended answer)

1. **Where the bolts land.** The cues: the centre path at the 10 m ground point, 0.6062 s (side bolts 0.6276 s at
   x +-3.44), the decision-1 picture, which here is also the game's own untargeted shot. The game's 0.4 m trigger really
   touches the floor at 7.23 m after 0.42 s; a real enemy is aimed at its body centre and hit by a flatter bolt.
   **Recommended: keep the 10 m picture** (as the Sheep and the Penguin).
2. **drainLife_hit's place.** The Bat's own client draws it at her own feet (:22182), everyone else and the clones at the
   target's centre (:22193, Bat_illusion.cs:4685), in BB and TTO. **Recommended: the target point 0.6 m up** (the cues
   above), and offer the bug to the user for the Bible. The other way: `[t, "fx", "drainLife_hit"]` at the hero.
3. **Drain Life's hold.** **Recommended: `cAttack2*@6.2`**, so the tile shows Dream Burst 3's first burst at 6.0 s (the
   passives-on rule) after five drain ticks; the plain channel rule ("three hits, at least 3 s") would be `@3.2`, with
   no burst.
4. **The Homing Wand (`specialWand`, w_bat59).** Worn, the bolts home on the target 0.6 m up and hit it at 0.56-0.58 s
   instead of the floor. **Recommended: yes, as the game** (the Penguin's decision 18 for the Staff of Time): Bat_nAttack's
   homing, a `worn` cue option and the variant cues above.
5. **The run's wing flap.** **Recommended: yes** (`run` entry, step_fly1 at 0.1 s of each cycle), with the two small jobs
   (build fallback, a per-round replay flag). The footsteps of the Bison, Chameleon, Monkey, Panda and Whale runs are the
   same kind of event (`probe_events_all.txt`): those classes' researchers should use the same entry shape.
6. **TTO-only emote clips** (clap, wai, cooking, mining, planting, fishingBat, pose37). TTO voices clap with `cheer` and
   wai with `ty|bow`; BB has no code for them. **Recommended: leave them silent now** (as the Wolf, Sheep and Penguin),
   and offer the user a cross-class follow-up with TTO's voices. Likewise the chat voices stay BB's chat1-3 (TTO 1-5).
7. **activateIcon1.** **Recommended: no tile** (Penguin decision 19).
8. **The japanWagasa on the battle emote** (each battle emote opens or closes the parasol). **Recommended: no change in
   this job**; it is a prop-clip feature for the page (NOTES.md has the wagasa's clips), offered separately.
9. **The first step's fade** (`nAttack1`, `cAttack1` cut in the game). **Recommended: keep the page's 0.2 s fade**, as the
   Sheep and the Penguin (`!` if the user wants the cut).

## Offer for the Bible

New against `bat-skill-reference.md` (Combo `:287-296`, Drain Life `:298-309`), for the user to add there:
- the combo's fixed clip starts at 0.6 / 1.2 s after stage 1 (:20881, :21360), the shots at 0.3 / 0.9 / 1.7 s, the
  voices at each stage's start (stage 3 nAttack3 or nAttack4), the bolt's 15 m/s (16 m/s while homing);
- Drain Life's timeline: the charge lines at 0.4 s, the bolt and the looped cAttack2 at 0.7 s, the first tick 1 s
  later; with no target nothing at all happens (:22355-22362);
- the BB / TTO bug: the Bat's own client draws the drain's hit flash at her own feet, not on the target (:22182 vs :22193);
- BB's Bat emote chat voices are chat1-3 only (:47336), though chat4 / chat5 exist;
- the run's wing-flap sound (an AnimationEvent at 0.1 s).

## Verification

Checker, 2026-11-13 (home PC), read only against `D:\12tails\DecompiledSource` (Bat.cs, Bat_nAttack.cs,
Bat_illusion.cs, GameGui.cs, CharacterControl.cs), the TTO pseudo-C, the rip (`RippedAssets/.../gameassets/characters/
heroes/bat/{voices,sounds,effects}`), `wardrobe/data/bat/clips.json` and `wardrobe/index.html`. Every opaque predicate
on the traced paths was re-worked.

**Confirmed as written** (times, names, positions, picks, ranks): the dispatcher windows and the fixed clip starts
(Bat.cs:10047-10063, :10160-10168; `Yield(2, actionTime - now + 0.6)` :20881 / `+ 1.2` :21360); every stage's cut, voice,
shot and standby time (:20376 / :20457 / :20464; :20664 / :20881 / IL_51B `Yield(3, 0.3)` / IL_1A `Yield(4, 0.3)`;
:21079 / `Yield(3, 0.5)` / `Yield(4, 0.2)`); stage 3's `Random.Range(0, 2)` nAttack3 | nAttack4; the no-target aim
(GameGui.cs:1659, the 3 m clause Bat.cs:9886-9895); `RPC_nAttack_fire1` / `fire2` (:10753, :10868: `firePos + i x
transform.right`, `lhs x Euler(0, 15 i, 0)`, roll zeroed, one Sounds/nAttack after the loop) and the geometry (recomputed:
pitch 8.2192, side bolts Unity Euler (7.9373, 15.1486, 2.1410), landings 0.6062 / 0.6276 s at x 3.4366, d 10.0); 15 m/s,
16 m/s homing, 0.1 rad / 0.1 s (Bat_nAttack.cs:26, :51, :101-122); the floor hit before the Player / Enemy test
(Bat_nAttack.cs:181-261); `RPC_nAttack_hit` with the hero's rotation (:10974). Drain Life: no target = nothing
(:22355-22362), the doBeginCharge checks (:10369-10490), cAttack1 0 / 0.2 / 0.4 / 0.7 (Block_10 `Yield(3, 0.2)`, Block_6
`Yield(4, 0.3)`), drainLife_charge at +1.2 up, identity (:21580), drainLife spawned (:21772) and moved every frame to
TransformDirection(0.1, 1.25, 0.65) with the bolt's TargetPosition = the target's bounds centre (:21967-21972), the tick
every 1 s, the own-client hit flash at her feet vs the network copy at the target (:22182 vs :22193; the clone at the
target both ways, Bat_illusion.cs:4685 / :4698, its `RPC_cAttack_hit` :2188-2190), Dream Burst 3 (getDreamBurstLv :13908
returns 3 with #363; timer `drainLifeTimer + 8 - 3` :21833 = 6.0 s into cAttack2, that second's drain skipped via
Block_89 -> IL_D23 `YieldDefault(5)`), dreamBurst_hit at `bounds.center - 0.4 x hitDir` with the hero's PlayOneShot
(:13952-14030; the Bible's "every 9 - level s", bat-skill-reference.md:378). Emotes: chat1-3 only (`Random.Range(1, 4)`
:47336; Wolf / Sheep / Penguin use `Range(1, 6)`: Wolf.cs:39628, Sheep.cs:40638, Penguin.cs:41598), the other voices
`Substring(4)`; every voice file named is in the rip's `voices/` (hi, wave, ty, bow, laugh, sleep, cheer, beg, cry,
battle, chat1-3, ko1/2, dead1/2, nAttack1-4, cAttack1/2) and every sound in `sounds/` (nAttack, nAttack_hit, drainLife,
dreamBurst_hit). KO: RPC_ko no effect; RPC_dead always deadEffect (`79294 - 293003 == -213709` holds, :53748). The run's
AnimationEvent (probe_events.txt) and `playWingFlapEvent` (Bat.cs:101-140, the field `wingFlap` :19572 = step_fly1, which
is only in `Resources/sound/fx/`). The five hero-prefab fields and their order (Bat.cs:19572-19614 against
probe_fields.txt). Every paste-ready block parses; its option names are the page's (the cue comment above cueOf, index.html:4295-4330).

**Corrections**

1. `plans/fx_bat/attacks_emotes.md:80-82` (Read this first 8), `:495` (Parts needed 5b) and `:525-526` (question 5): the
   reason a basic move's cue plays only once is not the `!S.round` test. `run` plays in mode `"loop"` (LOOP_BASE
   index.html:1221, playMode :1270-1275), and startStep gives a loop-mode step `S.dur = Infinity` (index.html:1345-1346), so seqTick never
   starts a next step (index.html:1351) and startStep runs once per pick: the clip's cycles are three.js's own
   `LoopRepeat` (index.html:1336). An `"everyRound"` flag read beside `!S.round` would never be reached. Corrected job 5b:
   **in fxTick (index.html:4528 ff.), for an entry flagged `"everyCycle": true`, re-arm its cues (clear `c.done`) each time
   the playing action's time wraps (`C.action.time` smaller than on the last frame), and fire them against that action's
   time instead of FX.t**. Job 5a (the `"sound"` fallback to the rest of the rip for step_fly1, wardrobe_fx.py:424 calls
   `rip_wav(cls, n, "sounds")`, which looks only in the class's `sounds/`, :346-348) stands.

No time, name, position, pick or rank in the report was wrong; no paste-ready cue changes. The `run` entry only changes its
flag:

```json
  "run": {
    "why": "the run clip's AnimationEvent playWingFlapEvent at 0.1 s (checks/fx_bat_research/attacks_emotes/probe_events.txt) -> Bat.cs playWingFlapEvent (:101-140): the hero's audio.PlayOneShot(wingFlap) = step_fly1 (the field :19572, probe_fields.txt; Resources/sound/fx/step_fly1.wav), own hero or anyone in a mission (mGameType > 4, :107-121); every cycle of the run (the event fires each loop: everyCycle, a page flag to build)",
    "everyCycle": true,
    "cues": [
    [0.1, "sound", "step_fly1"]
    ]
  }
```

Small notes (no change needed): `kill` counts from the spawn, not the step clock, so drainLife's and drainLife_charge's
0.05 margins (6.15, 6.45) are not needed (6.2, 6.5 are the game's ends), but they are harmless; the release's
`CrossFade("root", 0.35)` (:22804) is played by the page's way back to idle with its own 0.2 s fade.
