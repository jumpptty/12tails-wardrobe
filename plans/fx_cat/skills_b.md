# Cat effects + sounds research: moonBlade, moonStorm, pillage, pointTarget, reverseThrust, supportFire1 / 2, swiftPace, throw1, throw2, walk (skills_b)

Researcher `skills_b`, 2026-11-13 (home PC). Scope: the clips `moonBlade`, `moonStorm`, `pillage`, `pointTarget`,
`reverseThrust`, `supportFire1`, `supportFire2`, `swiftPace`, `throw1`, `throw2`, `walk` and every skill that plays
them. Research only (recipe steps 1-3). Line numbers are `D:\12tails\DecompiledSource\Cat.cs` unless another file is
named. Times are seconds from the start of the clip the entry is keyed by. Distance 0 = at the hero. Max rank, passives
on (the Wolf's / Sheep's / Penguin's / Bat's decisions): Lucky Card 4 + Joker #402, Lucky Dice 2 + Roll the Dice #432,
Flying Dagger 4 + Three Knives #403, Disarm 2, Bleed 2 (+ Open Wound #443), Two Pair 2, Copycat 2, Reverse Thrust 2
(+ Backstab #413), Moon Blade 2, Moon Storm 2, Swift Pace #431, Pillage Plunge #434, Support Fire #444 (+ Revised
Skill #404). The target body is the standing one (Bat decision 4): centre 0.6 m up at 10 m, height 1, radius 0.3.

Read-only probes and scripts, in `checks\fx_cat_research\skills_b\` (git-ignored):
- `clean.py` / `dump.py` (the Bison's: a coroutine with its opaque `if (a - b == c)` predicates worked out) and
  `clean_RPC_<name>.txt` for the 13 coroutines, `clean_hit_rpcs.txt` (Cat.cs:9128-10540, the `_hit` RPCs),
  `clean_supportFire_rpcs.txt` (:10540-10900). Branch points re-checked by hand in the raw file (Moon Storm's j loop
  :36586-36612, Lucky Card's case 4 :20909-20957, RPC_luckyDice_hit :9389-9432).
- `clip_calls.txt` (`clip_calls.js` for the Cat), `tto_strings.py` -> `tto_strings.txt` (the String literals and
  float constants of TTO's coroutines and `_hit` RPCs for these skills).
- `probe.json` / `probe_summary.txt` (`wardrobe_fx.py cat --probe` on 31 effects), `inspect.py` (Animation / mesh /
  trail details), `probe2.py` / `probe2.txt` (supportFire_fire with Cat_supportFire's layout patched in for that run,
  its Rigidbody / BoxCollider, supportFire_hit's ParticleSystem type tree), `probe3.py` / `probe3.txt` (every native
  component, WorldParticleCollider's fields), `probe_events.py` / `probe_events.txt` (AnimationEvents on the Cat's 63
  clips: none), `probe_fields.py` / `probe_fields.txt` (the Cat prefab's object fields: luckyCard_hit,
  forwardLunge_dust, TestRay, deadEffect).
- `shells.py` -> `shells.txt` (Support Fire's shell flight per aim distance).
- `cues.py` -> `cues.json` / `cues_compact.json` (the entries below, checked: valid JSON, times in order, known kinds
  and options).

## Read this first

1. **Three pools and one sequence.**
   - `pointTarget`: Two Pair (:26177), Copycat (:26732). Pool members `twoPair` / `copycat`.
   - `throw1`: Lucky Card (:21102), Lucky Dice (:24174). Pool members `luckyCard` / `luckyDice`.
   - `throw2`: Flying Dagger (:29762), Disarm (:34357), Bleed (:35189). Pool members `flyingDagger` / `disarm` /
     `bleed`.
   - No SEQ holds these clips, so poolChains gives each member a tile of the clip alone and hides the plain clip
     (`C.poolClips`). Seven tiles; no SEQ_SKILL entry is needed.
   - `supportFire1` / `supportFire2` are the existing SEQ `Support Fire: supportFire1 supportFire2*@3` (index.html
     SEQ cat). Only `supportFire1` gets an entry; the shells hang on its ring (item 4).
   - Single-skill clips: `moonBlade`, `moonStorm`, `pillage` (Pillage Plunge), `reverseThrust`, `swiftPace`.
2. **`walk` is a basic move with nothing to cue.** PlayerControl plays it when the move speed is 5 m/s or less
   (:635, :813, :928; `run` above). No coroutine, no voice, no sound, no AnimationEvent (`probe_events.txt`: no Cat
   clip has one), no effect. The page already lists it under ท่าพื้นฐาน (เดิน) (NOTES.md :99, LOOP_BASE index.html:1251).
   No cue entry.
3. **Icons.** `data/icons/hd/index.json` has moonBlade, moonStorm, reverseThrust, supportFire and swiftPace.
   - The seven pool members get their Bible icons from `wardrobe_skill_icons.py` once the cue file names them
     (cat_twoPair2, cat_copycat2, cat_luckyCard4, cat_luckyDice2, cat_flyingDagger4, cat_disarm2, cat_bleed2 are in
     the Bible's assets.js).
   - **`pillage` has no icon today**: the script looks for a skill named like the clip ("pillage"), and the Bible's
     is `cat_pillagePlunge5`. Fix: `CLIP_SKILLS["cat"] = {"pillage": ["pillagePlunge"]}` in
     `pipeline/wardrobe_skill_icons.py`.
4. **The parts the page still needs** (details in "Parts" below):
   - P1 **Cat_supportFire**, the shell (`supportFire_fire`: the probe fails today, "no layout for Cat_supportFire (12
     field bytes)").
   - P2 **Support Fire's volley**: the game fires a shell from a random cannon every 0.24-0.35 s at a random aim.
     A page part on the ring (cue option `volley`), with the cannons found by their cue option `i`.
   - P3 **AlphaTimerFadeOut**: the cannons fade over 0.5 s when the channel ends (cue option `fadeOut`).
   - P4 **BB's ParticleSystem** (Unity 3.5 Shuriken) for `supportFire_hit`'s explosion. `wardrobe_fx.py`'s walker
     skips the component without a word, so the build "succeeds" and draws only the ring.
   - P5 **WorldParticleCollider**: Lucky Dice's dice bounce on the floor.
   - P6 **`hideProp`**, a new cue kind: the five throws hide the right-hand weapon while it is "thrown".
   - Everything else in scope is built: Ring / Line / Image / Emblem emitters, legacy particles, Animation,
     StaticMesh, SkinnedMeshRenderer, AlphaTimer, TrailRenderer, AudioSource, EffectControl.
5. **Nothing melee reaches the 10 m target** (the Bison's convention, skills_b item 9: no hit is drawn where the target
   is out of reach).
   - Moon Blade's circles: 3 / 4 m. Moon Storm's rings: 2 m around 0-7.5 m. Pillage Plunge's box: 2 m either side of
     her after the dash. Reverse Thrust's box: 3 m behind her (she faces away from the target).
   - Moon Storm's two 12 m blasts (radius 3) do reach the 10 m target, but `hit()` draws nothing.
   - So pillagePlunge_hit, reverseThrust_hit and backStab_hit are not cued.
   - The ray skills do reach it. Lucky Card, Flying Dagger, Disarm and Bleed spawn their hits at the ray's point on
     the body's front, `{"d": 9.7, "y": 0.62}` (item 6). Two Pair and Copycat spawn theirs at the target's feet + 0.5 /
     + 1 m, so `d 10`.
6. **The ray skills' geometry** (Lucky Card :20593-20615, Flying Dagger :29123-29145, Disarm :34022-34044, Bleed
   :34854-34876).
   - Fire point = the cast spot + 1.2 m up. Aim = the target's `collider.bounds.center` (0.6 m up at 10 m).
   - The fire effect's rotation is `FromToRotation(forward, (0, -0.6, 10))` = pitch 3.43 deg down: `rot [3.43, 0, 0]`
     (the Penguin's missile convention).
   - The 20 m ray meets the 0.3 m body's front at z 9.7, y = 1.2 - 0.06 x 9.7 = 0.618: `{"d": 9.7, "y": 0.62}`.
   - Flying Dagger's side rays start 0.6 m to each side and 0.3 m back, parallel to the middle one. They miss the body
     (0.6 > 0.3) and end 2 mm above the floor (1.2 - 0.06 x 19.96), so they hit nothing.
7. **The weapon is hidden while it is thrown.** The coroutine switches off `mChar.mWep1`'s MeshRenderers (the
   right-hand weapon: CatEquipment.cs:949-1025 parents it to Hand_R / Arm_R / mount_Hand_R) and switches them back
   on later, unless the Cat is invisible.
   - Lucky Card: 0.4-0.8 s. Lucky Dice: 0.4-0.8 s. Flying Dagger, Disarm, Bleed: 0.5-0.95 s.
   - The re-enable in case 4 runs only if the skill was broken off. Lucky Card's case 4 (:20909-20957) jumps to the
     wait when the action is still "attack", so the weapon shows again only in case 6, after standby.
   - Cue: `[t, "hideProp", "R", {"kill": seconds}]` (P6).
8. **TTO plays these clips through the same 13 coroutines, with the same literals** (`tto_strings.txt`: pseudo/Cat.c
   :1429 bleed, :2933 copycat, :5722 disarm, :9235 flyingDagger, :13989 luckyCard, :14799 luckyDice, :15516 moonBlade,
   :16179 moonStorm, :20698 pillagePlunge, :22047 reverseThrust, :23990 supportFire, :24677 swiftPace, :25088 twoPair).
   - One difference: **TTO's Lucky Dice plays `rollTheDice1` / `rollTheDice2` instead of `luckyDice1` / `2` when Roll
     the Dice #432 is learned** (`hasSkill(0x1b0)` pseudo/Cat.c:15333-15345, loads at :15420 / :15455). BB's rip has
     both rollTheDice wavs, and BB's code never plays them (question 3).
   - TTO also resets Swift Pace's cooldown on a kill with #431 (`Cat::OnKilledPlayer`, `hasSkill(0x1af)` then
     `removeTimeOut("swiftPace")`): gameplay only.
   - TTO's wait values are not in the pseudo-C (`Waits__Get()` loses its float argument), so BB's times are used.
   - No released TTO skill (anchorYank, crescentEclipse1 / 2, dropAnchor, royalFlush1) plays a clip in this scope.
9. **Left out, with no page part to draw them** (the precedent: the Penguin's Dispell screen warp, NOTES 2026-11-13):
   - The camera motion blur of Moon Blade (:35624-35629) and Moon Storm (:36855-36858).
   - Support Fire's camera shake on every shell (:41261).
   - Open Wound #443's red colour ramp on a hit against a disarmed or bleeding foe (OpenWound :10404-10473).
   - The statuses on the foe (cut, pillage, disarm, bleed, Joker's doom): status looks on a foe stay out (Bat
     decision 44, Sheep decision 4).
10. **Dead code, not cued:** `RPC_luckyDice_hit` (:9389-9432) is never called (no call or "RPC_luckyDice_hit" string
    in Cat.cs), and BB's rip has no `luckyDice_hit` prefab. Lucky Dice's look is the `luckyDice` effect alone.

## Moon Blade (`moonBlade`)

- RPC: `RPC_moonBlade` :35464-36202. Key press :6387 (max rank sLv 2) -> :7146.
- Timeline:
  - 0: `PlayAnimation(moonBlade, 0)`, Once (:35966-35969). moveSpeed 0.5 (:35975).
    - **moonBlade** via createEffect at the hero, hero rotation (:35978-35996). EffectControl life 1 + afterLife 1,
      followPosition, no followState; three RingEmitters (Delay 0-0.3); it plays its own Sounds/moonBlade.
    - Voice moonBlade1 / moonBlade2, `Random.Range(0, 2)` (:36039-36095; PlayOneShot :36138 / :36123).
  - `Yield(2, 0.2)` (:36128). At 0.2: moveSpeed 2 (:35611), the player's motion blur (:35624-35629, left out).
  - `Yield(3, 0.1)` (:36141). At 0.3: `FindAreaTarget(pos, 3 rangeMod, 3)` (:35679), hit + cut status.
  - `Yield(4, 0.1)` (:36119). At 0.4: the 4 m circle (:35781).
  - `Yield(5, 0.1)` (:36115). At 0.5: moveSpeed 0 (:35875).
  - `Yield(6, 0.3)` (:36134). At 0.8: standby (:35896).
- Max rank: only the damage (talAdjust(15 + 10 sLv)) and the cut level change. Random: the voice. Rolls: none.
- Spawn: distance 0, hero rotation. Hits: none drawn (item 5).
- Buildable: ready (inventory, probe).

## Moon Storm (`moonStorm`)

- RPC: `RPC_moonStorm` :36203-36951. Key press :6408 (sLv 2) -> :7126.
- Timeline:
  - 0: `PlayAnimation(moonStorm, 0)`, Once (:36708-36711). moveSpeed 0.5.
    - **moonStorm** via createEffect at the hero, hero rotation (:36720-36738). Life 2, no followState. Its eight
      LineEmitters and 16 RingEmitters stand along z 0-12 m with Delays 0.3-0.95 s: the effect itself draws the
      storm's path. It plays its own Sounds/moonStorm.
    - Voice moonStorm1 / moonStorm2 (:36781-36840; PlayOneShot :36805 / :36836).
    - The motion blur (:36855-36858) is left out.
  - `Yield(2, 0.2)` (:36879). At 0.2: moveSpeed 3 (:36350), i = 0.
  - Rings, `Yield(3, 0.1)` each (:36882): at 0.3, 0.4 ... 0.8, `FindAreaTarget(cast + 1.5 i forward, 2, 2)` (:36415);
    moveSpeed 0 at i = 2 (0.5 s, :36403).
  - Blasts, `Yield(4, 0.1)` each (:36887), `j < 2` (:36609): at 0.9 and 1.0, `FindAreaTarget(cast + 12 forward, 3, 2)`
    (:36521). The opaque test after `j++` (:36595, 43275 - 192560 = -149285) is false, so the loop goes back to IL_1A.
  - At 1.0: standby (:36629).
- Max rank: damage only. Random: the voice. Hits: drawn by nobody (item 5).
- Buildable: ready.

## Pillage Plunge (`pillage`)

- RPC: `RPC_pillagePlunge` :39906-40695. Key press :6621 -> :6655 (aimed at the target if any, else forward; no
  target needed).
- Timeline:
  - 0: `PlayAnimation(pillage, 0)`, Once (:40453-40456). moveSpeed 0.
    - **pillagePlunge_ring1** Instantiated at the hero, hero rotation (:40465-40483). Life 1 + 1, no followState;
      plays its own Sounds/pillage.
    - Voice pillagePlunge1 / pillagePlunge2 (:40526-40585; PlayOneShot :40617 / :40627).
  - `Yield(2, 0.7)` (:40623). At 0.7: the dash, moveSpeed 24 (:40042); the pass-through list (:40052).
    - **pillagePlunge_ring2** via createEffect at the hero, hero rotation (:40104-40122). Animation "Base Stack"
      (0.5 s; its two trails sweep down from 3.2 m), life 0.4, followPosition, **followState**.
  - `Yield(3, 0.1)` (:40612). At 0.8: the hit box `FindRecTarget(pos - 2 forward, forward, 2, 2, 4, 2)` (:40172);
    each hit `RPC_pillagePlunge_hit` at the foe (:40223-40244; :10497-10520). Not drawn (item 5).
  - `Yield(4, 0.1)` (:40602). At 0.9: moveSpeed 0 (:40278).
    - **pillagePlunge_ring3** via createEffect at the hero, hero rotation (:40283-40301). Life 1 + 1.
  - `Yield(5, 0.3)` (:40604). At 1.2: standby (:40383) = ring2's cut (its life ends at 1.1 anyway).
- The dash is 24 m/s from 0.7 to 0.9 s = 4.8 m (the Bible's table gives the leg to the hit, 2.4 m). The hero doesn't
  travel on the page, so ring3 is at the hero (the Bison's Instant Rush, the Penguin's Blink).
- One rank. Random: the voice. Buildable: ring1 / ring2 / ring3 ready.

## Reverse Thrust (`reverseThrust`)

- RPC: `RPC_reverseThrust` :31011-32023. Key press :6324 (sLv 2).
- Timeline:
  - 0: she faces away from the target, `LookAt(mPos + vFlat(-tDir))` (:31902). `PlayAnimation(reverseThrust, 0)`,
    Once (:31905-31908). moveSpeed 0.
  - `Yield(2, 0.1)` (:31935). At 0.1: moveSpeed -10 (:31158).
    - **reverseThrust** via createEffect at the hero, rotation `hero x Euler(270, 90, 0)` (:31163-31181). Animation
      "root" (0.3 s), a StaticMesh blade with a TrailRenderer, life 0.3, followPosition, **followState**; it plays
      its own Sounds/reverseTrust1.
    - Voice reverseThrust1 / reverseThrust2 (:31226-31291; PlayOneShot :31952 / :31939).
  - `Yield(3, 0.2)` (:31937). At 0.3: moveSpeed 0, the box behind her (`-transform.forward`, 1 x 1 x 3, :31353).
  - `Yield(4, 0.4)` (:31946). At 0.7: moveSpeed 1, the box again (:31590).
    - Each hit: Backstab #413 doubles the damage when the two facings differ by more than 135 deg (:31386-31455), then
      `RPC_backStab_hit` or `RPC_reverseThrust_hit` at the foe's closest point (:31475-31527; :10340-10363,
      :9925-9948). Not drawn (item 5).
  - `Yield(5, 0.2)` (:31944). At 0.9: moveSpeed 0. `Yield(6, 0.1)` (:31960). At 1.0: standby (:31835) = the
    effect's cut (its life ends at 0.4 anyway).
- Max rank: damage and KO (5 sLv) only. Random: the voice. Buildable: ready.

## Swift Pace (`swiftPace`)

- RPC: `RPC_swiftPace` :39462-39905. Key press :6528-6600: `mPos = Math.getSpawnPos(target - (extents.x + 0.5) x
  target.forward)` = behind the target, and `tDir = vFlat(target - target)` = zero, so the `LookAt` (:39715) leaves
  her facing as it was.
- Timeline:
  - 0: `PlayAnimation(swiftPace, 0)`, Once (:39718-39721). moveSpeed 0.
    - **swiftPace_ring1** Instantiated at the hero, hero rotation (:39727-39745). Life 1 + 1; plays its own
      Sounds/swiftPace1.
    - Voice swiftPace1 / swiftPace2 (:39788-39847; PlayOneShot :39866 / :39874).
  - `Yield(2, 0.3)` (:39868). At 0.3: she is put at `mPos + 0.1 up` (:39597).
    - **swiftPace_ring2** Instantiated there, her rotation (:39602-39620). Life 1 + 1; plays its own Sounds/swiftPace2.
  - `Yield(3, 0.2)` (:39872). At 0.5: standby (:39651).
- The page's hero doesn't travel: ring2 at the hero, 0.1 m up (the Penguin's Blink; question 2). One rank.
- Buildable: both rings ready.

## Support Fire (`supportFire1`, then `supportFire2` looped)

- RPC: `RPC_supportFire` :40696-41391. Key press :6675 -> :6709. The end: `RPC_supportFire0` :10547-10624. The
  shells: `RPC_supportFire_fire` :10636-10768, `Cat_supportFire.cs`, `RPC_supportFire_hit` :10776-10858.
- Timeline:
  - 0: `PlayAnimation(supportFire1, 0)`, Once (:40894-40899). moveSpeed 0.
    - **supportFire_ring** via createEffect at the hero, hero rotation (:40914-40932). Life 99, followPosition,
      **followState**; an EmblemEmitter 3 m up (Delay 0.2) and a repeatForever ring; it plays its own
      Sounds/supportFire_ring.
    - Voice supportFire1 / supportFire2 (:40975-41034).
    - **Six supportFire_cannon** via createEffect, hero rotation, where a 4 m ray down from `TransformDirection(3i -
      10.5, 2, -2)`, i = 1..6, meets the floor (:41043-41099): x -7.5, -4.5, -1.5, 1.5, 4.5, 7.5, 2 m behind her. Each:
      Animation "fire" (0.5 s recoil, not played at spawn: `play false`), the PirateCannon_tri SkinnedMeshRenderer,
      AlphaTimer fading in to 0.8 over 1 s (FadeMiddle 99), a RingEmitter, life 99 + afterLife 0.5, **followState**.
  - `Yield(2, 1)` (:41332). At 1.0: `PlayAnimation(supportFire2, 0)`, Loop (:40832-40837); `mUpdateTime = Time.time
    + 0.25`, fire count 0 (:40842-40847).
  - Then every FixedUpdate (`Yield(3, WaitForFixedUpdate)` :41334) while the action is "attack":
    - The player moving (:41134-41150) or SP under 6 (:41157) ends it: `RPC_supportFire0` (:41269).
    - Once `Time.time >= mUpdateTime`: the next shot at `+ 0.01 x Random.Range(24, 36)` = 0.24-0.35 s (:41174).
      - A cannon at random, `Random.Range(0, 6)` (:41185).
      - `RPC_supportFire_fire(cannon + cannon.TransformDirection(0, 1, 3), getTrajectoryVector(that point, that
        point + (24 + Random.Range(0, 24)) forward, 30), id)` (:41207-41217).
      - That cannon's `animation.Rewind(); Play("fire")` (:10672-10677).
      - **supportFire_smoke** Instantiated at the fire point, `LookRotation(fireDir)` (:10693-10711). Life 1, a
        legacy one-shot puff; it plays its own Sounds/supportFire_fire.
      - **supportFire_fire** Instantiated there, same rotation, then `Cat_supportFire.Init` (:10725-10753).
      - Every sixth shot costs 12 SP (6 with Revised Skill #404, :41249-41255). A camera shake (:41261, left out).
  - The first shot: 1.25 s after the cast (0.25 s into supportFire2).
  - The end (`RPC_supportFire0`): standby (:10566), then every cannon gets `BroadcastMessage("AlphaTimerFadeOut",
    0.5)` (:10603). The cannons' followState sends them into their 0.5 s afterLife; the ring's followState ends it.
- The shell (`supportFire_fire`, probe2.txt):
  - Root: BoxCollider trigger 0.25 x 0.25 x 0.5, Rigidbody (mass 1, drag 0, useGravity), Cat_supportFire with
    `mVelocity (0, 0, 30)`.
  - Children: a legacy ParticleEmitter (the smoke trail) and PirateCannon_fire (MeshFilter + MeshRenderer).
  - `Init`: layer 1, life 10 s, `rigidbody.velocity = transform.TransformDirection(mVelocity)` = 30 m/s along its
    forward (Cat_supportFire.cs:38-57).
  - FixedUpdate: life -= dt (destroyed at 0), `LookAt(position + velocity)` (:67-93). Gravity -9.8 (BB's
    ProjectSettings DynamicsManager m_Gravity).
  - OnTriggerEnter with anything not on the owner's layer, layer 1 or 2 (:102-209): on the owner's client,
    `RPC_supportFire_hit(collider.ClosestPointOnBounds(the shell's centre), ...)`, then Destroy.
  - **supportFire_hit**: Instantiated at that point, identity (:10784-10802). Life 2; a Shuriken ParticleSystem
    (P4) and a RingEmitter; it plays its own Sounds/supportFire_hit. Damage in 8 m (:10825).
- Where the shells land (`shells.py`, after the Bible's 2026-10-16 trace):
  - getTrajectoryVector with the aim at the fire point's height takes its `y < 0.1` branch (Math.cs:885-965): launch
    elevation 2.99 deg (aim 24 m) to 6.42 deg (aim 47 m). The smoke and the shell are `rot [-elev, 0, 0]`.
  - They start at (x, 1, 1) and touch the floor (the box centre 0.125 m up, 50 Hz steps) 18.98-27.23 m ahead of the
    Cat after 0.60-0.88 s (mean 22.9 m, 0.73 s).
  - The cannon lanes are 1.5 m or more off the centre line, so no shell meets the 10 m target (0.3 m body).
- On the page (the SEQ `supportFire1 supportFire2*@3`):
  - The channel lasts the 3 s hold: about 10 shells (from 1.25 s, mean gap 0.295 s), the last landing after the
    hold ends.
  - The ring's and the cannons' `cut` is **3**, the end of the supportFire2 hold on supportFire2's own clock. FX.t
    restarts at every step and `cutAt` is read against it (index.html:4016; the Bison's note 3). During
    supportFire1 (1.0 s) the clock never reaches 3.
- One rank. Random: the voice, every gap, cannon and aim. Buildable: the ring, the cannons and the smoke are ready;
  the shell needs P1-P2, the cannons' fade P3, the explosion's ParticleSystem P4.

## Two Pair (`pointTarget` pool member `twoPair`)

- RPC: `RPC_twoPair` :25518-26412. Key press :6123 (sLv 2).
- Timeline:
  - 0: `PlayAnimation(pointTarget, 0)`, Once (:26177-26180).
    - **twoPair_ring** via createEffect at the hero, hero rotation (:26189-26207). Life 1, followPosition; plays its
      own Sounds/twoPair.
    - Voice twoPair1 / twoPair2 (:26250-26309; PlayOneShot :26333 / :26339).
  - `Yield(2, 0.4)` (:26331). At 0.4, on the owner's client: the statuses of level <= 2 sLv swapped both ways
    (:25716-26038), then `RPC_twoPair_hit(target bounds centre, ..., target id)` (:26068; :9464-9510):
    - **twoPair_hit** Instantiated at the hero + 0.5 up, identity (:9489).
    - **twoPair_hit** at the target's feet + 0.5 up, identity (:9507): the 10 m target point.
  - `Yield(3, 0.4)` (:26328). At 0.8: standby (:26107).
- Max rank: the swapped statuses' level cap only. Buildable: ready. The statuses she takes over draw nothing here (what
  they are depends on the foe).

## Copycat (`pointTarget` pool member `copycat`)

- RPC: `RPC_copycat` :26413-26939. Key press :6144 (sLv 2).
- Timeline:
  - 0: `PlayAnimation(pointTarget, 0)`, Once (:26732-26735).
    - **copycat_ring** via createEffect at the hero, hero rotation (:26744-26762). Life 1 + 1, followPosition; plays
      its own Sounds/copyCat.
    - Voice copycat1 / copycat2 (:26805-26864; PlayOneShot :26883 / :26891).
  - `Yield(2, 0.4)` (:26897). At 0.4: if the target's `mLastDamage > 0` (:26602), damage (:26608) and
    `RPC_copycat_hit` (:26613; :9528-9574):
    - **copycat_hit** at the hero + 1 up, identity (:9553), and at the target's feet + 1 up, identity (:9571): d 10.
    - Else "Copycat fail: no damage to copy" (:26635) and no effect (question 4).
  - `Yield(3, 0.3)` (:26881). At 0.7: standby (:26662).
- Buildable: ready.

## Lucky Card (`throw1` pool member `luckyCard`)

- RPC: `RPC_luckyCard` :20398-21253. Key press :5933 (sLv 4). Joker #402 on: damage and a doom roll on the foe
  (:20850-20893), nothing drawn.
- Timeline:
  - 0: `animation.Rewind(); PlayAnimation(throw1, 0)`, Once (:21099-21105). moveSpeed 0.
  - `Yield(2, 0.4)` (:21151). At 0.4:
    - The main weapon hidden (:20556-20583).
    - **luckyCard_fire** Instantiated at the fire point, `FromToRotation(forward, fireDir)` (:20593-20638): y 1.2,
      rot [3.43, 0, 0]. Life 1, an ImageEmitter 3.5 m out and a LineEmitter (life 0.1); it plays its own
      Sounds/throw.
    - Voice luckyCard1 / luckyCard2 (:20683-20746; PlayOneShot :21137 / :21129). **This is the Bible's "coin flip
      picks one of two card effect variants (:20683)": it picks the voice. There is one card effect.**
  - `Yield(3, 0.1)` (:21139). At 0.5: the 20 m ray (:20780-20790), `RPC_luckyCard_hit(hit.point, forward)`
    (:20798; :9128-9130): the prefab field **luckyCard_hit** (the Cat prefab's first GameObject field,
    `probe_fields.txt`; the same-named Resources prefab is what the probe read) at the point, hero rotation. A legacy
    one-shot (autodestruct, no EffectControl); it plays its own Sounds/throw_hit. At `{"d": 9.7, "y": 0.62}`.
  - `Yield(4, 0.1)` (:21143). At 0.6: nothing (item 7). `Yield(5, 0.1)` (:21147). At 0.7: standby (:20980).
  - `Yield(6, 0.1)` (:21135). At 0.8: the weapon shown (:21020-21048).
- Max rank: cooldown and damage only. Buildable: luckyCard_fire, luckyCard_hit ready; the hide needs P6.

## Lucky Dice (`throw1` pool member `luckyDice`)

- RPC: `RPC_luckyDice` :23682-24446. Key press :6008 (sLv 2). Roll the Dice #432 on: damage only in BB (:23939).
- Timeline:
  - 0: `animation.Rewind(); PlayAnimation(throw1, 0)`, Once (:24171-24177). moveSpeed 0.
    - **Sounds/luckyDice**, `audio.PlayOneShot(clip)`, volume 1 (:24186-24204): a `"sound"` cue (the hero's code
      plays it). The error text calls it "luckyDice_fx".
    - Voice luckyDice1 / luckyDice2 (:24247-24306; PlayOneShot :24358 / :24327). TTO: rollTheDice1 / 2 with #432
      (item 8, question 3).
  - `Yield(2, 0.4)` (:24349). At 0.4:
    - The main weapon hidden (:23829-23856).
    - **luckyDice** Instantiated at the hero, identity (:23866-23884). Life 2: a LineEmitter burst, a RingEmitter
      and the dice (legacy one-shot particles, 1-1.5 s) with a **WorldParticleCollider** (bounce 0.5, energy loss 0,
      collides with layer bit 1 = Default, no message, min kill velocity 0; probe3.txt): P5. No AudioSource.
  - `Yield(3, 0.1)` (:24339). At 0.5: the 6 m circle (:23934). Nothing drawn (item 10).
  - `Yield(4, 0.1)` (:24351), `Yield(5, 0.1)` (:24356). At 0.7: standby (:24061).
  - `Yield(6, 0.1)` (:24341). At 0.8: the weapon shown (:24101-24129).
- Buildable: luckyDice needs P5 (it would draw without it, the dice falling through the floor); the hide needs P6.

## Flying Dagger (`throw2` pool member `flyingDagger`)

- RPC: `RPC_flyingDagger` :28901-29923. Key press :6207 (sLv 4). Three Knives #403 on (`hasSkill(403)` :29168).
- Timeline:
  - 0: `animation.Rewind(); PlayAnimation(throw2, 0)`, Once (:29759-29765). moveSpeed 2 (:29771).
  - `Yield(2, 0.2)` (:29817). At 0.2: moveSpeed 6 (:29059).
  - `Yield(3, 0.3)` (:29800). At 0.5:
    - The main weapon hidden (:29086-29113).
    - **Three flyingDagger_fire** Instantiated at the fire point and at `TransformDirection(-0.6, 0, -0.3)` /
      `(0.6, 0, -0.3)` from it, all with the middle knife's `FromToRotation` (:29123-29184). Life 1, a LineEmitter
      (life 0.1); each plays its own Sounds/throw.
    - Voice threeKnives1 / threeKnives2 (:29220-29285; PlayOneShot :29821 / :29802).
    - Without #403: one knife and flyingDagger1 / flyingDagger2 (:29291-29390).
  - `Yield(4, 0.1)` (:29804). At 0.6: moveSpeed 0; three parallel 20 m rays (:29455, :29509, :29555).
    - The middle one meets the body: `RPC_flyingDagger_hit(hit.point)` (:29461; :9825-9848) = **flyingDagger_hit**
      at the point, hero rotation. A LineEmitter burst; it plays its own Sounds/throw_hit. At `{"d": 9.7, "y": 0.62}`.
    - The side rays hit nothing (item 6).
  - `Yield(5, 0.2)` (:29791). At 0.8: standby (:29628). `Yield(6, 0.15)` (:29833). At 0.95: the weapon shown
    (:29668-29696).
- Buildable: both effects ready; the hide needs P6. The hero doesn't travel (2.2 m by 0.6 s in the game).

## Disarm (`throw2` pool member `disarm`)

- RPC: `RPC_disarm` :33800-34631. Key press :6345 (sLv 2).
- Timeline:
  - 0: `animation.Rewind(); PlayAnimation(throw2, 0)`, Once (:34354-34360). moveSpeed 2.
    - **disarm_ring** via createEffect at the hero, identity (:34369-34387). Life 1, followPosition; plays its own
      Sounds/aura1.
    - Voice disarm1 / disarm2 (:34430-34489; PlayOneShot :34518 / :34532).
  - `Yield(2, 0.2)` (:34527). At 0.2: moveSpeed 6.
  - `Yield(3, 0.3)` (:34512). At 0.5: the weapon hidden (:33985-34012); **disarm** Instantiated at the fire point,
    `FromToRotation` (:34022-34067). Life 1, a LineEmitter; plays its own Sounds/throw.
  - `Yield(4, 0.1)` (:34523). At 0.6: moveSpeed 0; the ray (:34127): `RPC_disarm_hit(hit.point)` (:34135;
    :10219-10242) = **disarm_hit** there, identity; plays its own Sounds/disarm_hit. Then (on a real hit) the disarm
    status on the foe (:34183-34188), nothing drawn.
  - `Yield(5, 0.2)` (:34538). At 0.8: standby (:34223). `Yield(6, 0.15)` (:34536). At 0.95: the weapon shown.
- Buildable: ready; the hide needs P6.

## Bleed (`throw2` pool member `bleed`)

- RPC: `RPC_bleed` :34632-35463. Key press :6366 (sLv 2). The same shape as Disarm:
  - 0: `animation.Rewind(); PlayAnimation(throw2, 0)` (:35186-35189), moveSpeed 2; **bleed_ring** via createEffect at
    the hero, identity (:35201-35219; life 1, followPosition, Sounds/aura1); voice bleed1 / bleed2 (:35262-35321;
    PlayOneShot :35352 / :35341).
  - 0.2 (`Yield 0.2` :35362): moveSpeed 6.
  - 0.5 (`Yield 0.3` :35350): the weapon hidden (:34817-34839); **bleed_fire** at the fire point, `FromToRotation`
    (:34854-34899; life 1, Sounds/throw).
  - 0.6 (`Yield 0.1` :35370): the ray (:34959), `RPC_bleed_hit(hit.point)` (:34967; :10269-10292) = **bleed_hit**
    there, identity (a LineEmitter and legacy blood drops; Sounds/bleed_hit). The bleed status draws nothing here.
  - 0.8 (`Yield 0.2` :35364): standby (:35055). 0.95 (`Yield 0.15` :35348): the weapon shown (:35095-35118).
- Buildable: ready; the hide needs P6.

## Parts

P1. **Cat_supportFire** (the shell).
- `wardrobe_fx.py` LAYOUTS: `"Cat_supportFire": [("mVelocity", "v3")]` (12 bytes; Cat_supportFire.cs:240). With it
  patched in, `probe2.py` reads supportFire_fire clean: mVelocity (0, 0, 30).
- Page: velocity = the spawn rotation x mVelocity; gravity -9.8 per 50 Hz step (v += g dt, then p += v dt); the root
  turned to look along the velocity each step; destroyed at 10 s.
- When the 0.25 x 0.25 x 0.5 box meets the floor (y 0): spawn **supportFire_hit** at the floor point under the
  shell's centre, identity (`api.spawn`), and destroy the shell. Nothing else stops it on the page: the lanes miss
  the 10 m target.
- Its children draw with built parts (the legacy smoke trail, the PirateCannon_fire mesh).

P2. **The volley** (on `supportFire_ring`, cue option `volley`; the Bat's guardian pattern: a part spawns with
`api.spawn`, the entry's `"builds"` names what it spawns).
- From `first` = 1.25 s after the ring's spawn, then every `every` = [0.24, 0.35] s, drawn as
  `0.01 x randInt(24, 35)` (Random.Range's int top left out). A shot falls on the next 50 Hz step, as the game.
- Each shot:
  - Take one of the six cannons at random: they carry cue option `i` 0-5, so the part keeps them by `i` for this play.
  - Play that cannon's "fire" clip from the start: `root.userData.fxAnim.play("fire")`, rewound.
  - The fire point = that cannon + its rotation x `from` (0, 1, 3).
  - aim = 24 + randInt(0, 23) m. The elevation is getTrajectoryVector's (shells.py: atan((v^2 + sqrt(v^4 - g^2
    aim^2)) / (g aim)), then - 0.1 aim / v, as a pitch from the vertical).
  - Spawn **supportFire_smoke** and **supportFire_fire** there, with `rot [-elev, 0, 0]` after the hero's facing.
- It stops when the ring goes: the ring's cut 3 ends it, as the channel's end does.
- Shells already in flight fly on.

P3. **AlphaTimerFadeOut** (AlphaTimer.cs:328-357).
- The call zeroes the delay / ease-in / middle phases and starts the ease-out now, over `nFadeEaseOut`: MaxAlpha to
  MinAlpha (0.8 to 0 for the cannons).
- On the page: a cue option `fadeOut` (seconds). When the effect's cut fires, the AlphaTimer part (alphatimer.js)
  restarts its clock that way. Its EffectControl afterLife 0.5 then removes the cannon as it ends.

P4. **BB's ParticleSystem** (supportFire_hit's node "ParticleSystem": ParticleSystem + ParticleSystemRenderer).
- `wardrobe_fx.py`'s walker has no branch for these two types and skips them silently. The inventory lists the effect
  as "needs ParticleSystem, ParticleSystemRenderer".
- The 3.5 type tree (probe2.txt) has the module names shuriken.js reads for TTO: lengthInSec, startDelay, speed,
  looping, prewarm, playOnAwake, moveWithTransform (a bool here), InitialModule, ShapeModule, EmissionModule,
  SizeModule, RotationModule, ColorModule, UVModule, VelocityModule, ForceModule, ClampVelocityModule,
  SizeBySpeedModule, RotationBySpeedModule, ColorBySpeedModule, CollisionModule, SubModule.
- What would be built: export them (renderer + material) and feed fxparts/shuriken.js, checking each 3.5 field
  against its 2019 reading.
- supportFire_hit: lengthInSec 1, not looping, startLifetime 0.6-1, startSpeed 0-5, startSize 0.5-2, random rotation.

P5. **WorldParticleCollider** (luckyDice's ParticleEmitter node). Legacy particles bounce off the floor.
- Fields: velocity x bounceFactor 0.5 on contact, energy loss 0, collides with layer bit 1 (Default: the page's
  floor), no message, min kill velocity 0.
- The Chameleon's tormentRain_fire and the Rabbit's millionaire1 / 2 need the same part.

P6. **`hideProp`**, a new cue kind: `[t, "hideProp", "R", {"kill": s}]`.
- What it does: the worn right-hand weapon's meshes are taken off the camera layers from t for s seconds. The game
  disables mWep1's MeshRenderers only, so the weapon's own particle effects (weapon_fx.json) keep drawing.
- With no weapon worn, nothing happens.
- Two page spots must know the kind:
  - fxStart's sound preload (index.html:4636: `c.kind !== "fx" && c.kind !== "skin"` would fetch an "R" sound).
  - fxDue (:4701: every other kind goes to Sound.play).
  - Without that, the fx check fails on the failed request.

Also (not a part): `pipeline/wardrobe_skill_icons.py` `CLIP_SKILLS["cat"] = {"pillage": ["pillagePlunge"]}`, then
run it (item 3).

## Paste-ready cue entries for `wardrobe/fx_cues/cat.json`

Nine entries, 13 tiles (checks/fx_cat_research/skills_b/cues.json, valid JSON). The keys are the clips; the pools use
the Wolf's / Sheep's / Penguin's `{why, skills: {member: {why, cues}}}` shape. `hideProp` (P6), `volley` / `i` /
`fadeOut` (P2, P3) are new; every other option is one the page reads today.

```json
 "moonBlade": {
  "why": "Cat.cs RPC_moonBlade (:35464-36202), max rank sLv 2 (dispatch :6387; the effect does not change by rank): clip cut in (PlayAnimation(moonBlade, 0) :35966), Effects/moonBlade created at the hero, hero rotation (createEffect :35984-35996; EffectControl life 1 + afterLife 1, followPosition, no followState; plays its own Sounds/moonBlade) and voice moonBlade1 / moonBlade2 (Random.Range(0, 2) :36039-36095, PlayOneShot :36138 / :36123) at 0; Yield 0.2 (:36128): moveSpeed 2 and the player's motion blur (:35611-35629, screen only); Yield 0.1 (:36141): at 0.3 s the 3 m circle (:35679), Yield 0.1 (:36119): at 0.4 s the 4 m circle (:35781): hit() and the cut status draw nothing, and the 10 m target is out of reach; Yield 0.1 (:36115): moveSpeed 0 (:35875); Yield 0.3 (:36134): standby at 0.8 s (:35896); the hero doesn't travel (0.1 + 0.2 + 0.1 m in the game)",
  "cues": [
   [0, "fx", "moonBlade"],
   [0, "voice", "moonBlade1|moonBlade2"]
  ]
 },
 "moonStorm": {
  "why": "Cat.cs RPC_moonStorm (:36203-36951), max rank sLv 2 (dispatch :6408): clip cut in (PlayAnimation(moonStorm, 0) :36708), Effects/moonStorm created at the hero, hero rotation (createEffect :36720-36738; EffectControl life 2, no followState; its own Line / Ring emitters draw the 12 m path, delays 0.3-0.95 s; plays its own Sounds/moonStorm) and voice moonStorm1 / moonStorm2 (Random.Range(0, 2) :36781-36840, PlayOneShot :36805 / :36836) at 0; the motion blur (:36855-36858) is screen only; Yield 0.2 (:36879): moveSpeed 3 (:36350); six rings of 2 m at cast + 1.5 i m, i = 0..5, 0.3-0.8 s (Yield 0.1 :36882, :36415; moveSpeed 0 at i = 2, :36403), then two blasts of 3 m at cast + 12 m at 0.9 and 1.0 s (Yield 0.1 :36887, :36521, j < 2 :36609): hit() and the cut status draw nothing at the 10 m target; standby at 1.0 s (:36629)",
  "cues": [
   [0, "fx", "moonStorm"],
   [0, "voice", "moonStorm1|moonStorm2"]
  ]
 },
 "pillage": {
  "why": "Cat.cs RPC_pillagePlunge (:39906-40695), Pillage Plunge #434, one rank (dispatch :6621): clip cut in (PlayAnimation(pillage, 0) :40453), Effects/pillagePlunge_ring1 Instantiated at the hero, hero rotation (:40465-40483; EffectControl life 1 + afterLife 1; plays its own Sounds/pillage) and voice pillagePlunge1 / pillagePlunge2 (Random.Range(0, 2) :40526-40585, PlayOneShot :40617 / :40627) at 0; Yield 0.7 (:40623): the dash, moveSpeed 24 (:40042; the hero doesn't travel, 4.8 m by 0.9 s in the game), and pillagePlunge_ring2 created at the hero (:40104-40122; Animation Base Stack, life 0.4, followPosition, followState: the action changes at standby, 1.2 s); Yield 0.1 (:40612): at 0.8 s the hit box 2 m behind to 2 m ahead of her (:40172): pillagePlunge_hit at the foe (:40233, :10497-10520) is out of reach of the 10 m target, none; Yield 0.1 (:40602): moveSpeed 0 and pillagePlunge_ring3 created at the hero (:40278-40301; life 1 + afterLife 1); Yield 0.3 (:40604): standby at 1.2 s (:40383)",
  "cues": [
   [0, "fx", "pillagePlunge_ring1"],
   [0, "voice", "pillagePlunge1|pillagePlunge2"],
   [0.7, "fx", "pillagePlunge_ring2", { "cut": 1.2 }],
   [0.9, "fx", "pillagePlunge_ring3"]
  ]
 },
 "reverseThrust": {
  "why": "Cat.cs RPC_reverseThrust (:31011-32023), max rank sLv 2 (dispatch :6324): she turns her back on the target (LookAt(mPos + vFlat(-tDir)) :31902) and the clip cuts in (PlayAnimation(reverseThrust, 0) :31905); Yield 0.1 (:31935): moveSpeed -10 (backwards, :31158), Effects/reverseThrust created at the hero, hero rotation x Euler(270, 90, 0) (:31163-31181; Animation root, life 0.3, followPosition, followState: the action changes at standby, 1.0 s; plays its own Sounds/reverseTrust1) and voice reverseThrust1 / reverseThrust2 (Random.Range(0, 2) :31226-31291, PlayOneShot :31952 / :31939) at 0.1 s; Yield 0.2 (:31937): at 0.3 s moveSpeed 0 and the 3 m box behind her (:31353), Yield 0.4 (:31946): at 0.7 s moveSpeed 1 and the box again (:31590): each hit a reverseThrust_hit (or, with Backstab #413 on a foe facing away, :31386-31455, a backStab_hit) at the foe (:31475-31527, :9925-9948, :10340-10363): the target 10 m off is out of reach, none; Yield 0.2 (:31944): moveSpeed 0; Yield 0.1 (:31960): standby at 1.0 s (:31835)",
  "cues": [
   [0.1, "fx", "reverseThrust", { "rot": [ 270, 90, 0 ], "cut": 1.0 }],
   [0.1, "voice", "reverseThrust1|reverseThrust2"]
  ]
 },
 "swiftPace": {
  "why": "Cat.cs RPC_swiftPace (:39462-39905), Swift Pace #431, one rank (dispatch :6528-6600: mPos = Math.getSpawnPos(target - (extents.x + 0.5) x target.forward), behind the target, tDir = vFlat(target - target) = zero, so the LookAt :39715 leaves her facing): clip cut in (PlayAnimation(swiftPace, 0) :39718), Effects/swiftPace_ring1 Instantiated at the hero, hero rotation (:39727-39745; life 1 + afterLife 1; plays its own Sounds/swiftPace1) and voice swiftPace1 / swiftPace2 (Random.Range(0, 2) :39788-39847, PlayOneShot :39866 / :39874) at 0; Yield 0.3 (:39868): she is put at mPos + 0.1 up (:39597) and swiftPace_ring2 Instantiated there, her rotation (:39602-39620; life 1 + afterLife 1; plays its own Sounds/swiftPace2): at the hero, 0.1 m up (the hero doesn't travel: the Penguin's Blink); Yield 0.2 (:39872): standby at 0.5 s (:39651)",
  "cues": [
   [0, "fx", "swiftPace_ring1"],
   [0, "voice", "swiftPace1|swiftPace2"],
   [0.3, "fx", "swiftPace_ring2", { "y": 0.1 }]
  ]
 },
 "supportFire1": {
  "why": "Cat.cs RPC_supportFire (:40696-41391), Support Fire #444, one rank (dispatch :6675), the SEQ Support Fire's first step: clip cut in (PlayAnimation(supportFire1, 0) :40894), Effects/supportFire_ring created at the hero, hero rotation (:40914-40932; life 99, followPosition, followState: ends when the channel does; its emblem and looping ring; plays its own Sounds/supportFire_ring) and voice supportFire1 / supportFire2 (Random.Range(0, 2) :40975-41034) at 0; six supportFire_cannon created where a 4 m ray down from TransformDirection(3i - 10.5, 2, -2), i = 1..6, meets the floor, hero rotation (:41043-41099: x -7.5 ... 7.5, 2 m behind; life 99 + afterLife 0.5, followState; AlphaTimer fades each in to 0.8 over 1 s); Yield 1 (:41332): supportFire2 looped from 1.0 s (:40832); the channel ends when the player moves (RPC_supportFire0 :10547-10624: standby, then every cannon's AlphaTimerFadeOut(0.5) :10603): cut 3 = the SEQ's supportFire2*@3 hold, read on supportFire2's own clock (FX.t restarts each step); the shells: the ring's volley (a part to build, report Parts 1-2): from 1.25 s after the ring (mUpdateTime = Time.time + 0.25 at supportFire2's start :40842), every 0.01 x Random.Range(24, 36) = 0.24-0.35 s (:41174), a cannon at random (Random.Range(0, 6) :41185) plays its fire clip (Rewind + Play :10672-10677), supportFire_smoke and supportFire_fire are Instantiated at that cannon + TransformDirection(0, 1, 3), LookRotation(getTrajectoryVector(that point, 24 + Random.Range(0, 24) m ahead, 30)) (:41207-41217, :10693-10753); Cat_supportFire flies at 30 m/s with gravity 9.8 and lands 19-27 m ahead after 0.60-0.88 s (checks/fx_cat_research/skills_b/shells.txt), supportFire_hit at the floor, identity (Cat_supportFire.cs:163-190, Cat.cs:10776-10802); the shake (:41261) is screen only",
  "builds": [
   "supportFire_fire",
   "supportFire_smoke",
   "supportFire_hit"
  ],
  "cues": [
   [0, "fx", "supportFire_ring", { "cut": 3, "volley": { "first": 1.25, "every": [ 0.24, 0.35 ], "aim": [ 24, 47 ], "speed": 30, "from": [ 0, 1, 3 ] } }],
   [0, "voice", "supportFire1|supportFire2"],
   [0, "fx", "supportFire_cannon", { "x": -7.5, "d": -2, "cut": 3, "i": 0, "fadeOut": 0.5 }],
   [0, "fx", "supportFire_cannon", { "x": -4.5, "d": -2, "cut": 3, "i": 1, "fadeOut": 0.5 }],
   [0, "fx", "supportFire_cannon", { "x": -1.5, "d": -2, "cut": 3, "i": 2, "fadeOut": 0.5 }],
   [0, "fx", "supportFire_cannon", { "x": 1.5, "d": -2, "cut": 3, "i": 3, "fadeOut": 0.5 }],
   [0, "fx", "supportFire_cannon", { "x": 4.5, "d": -2, "cut": 3, "i": 4, "fadeOut": 0.5 }],
   [0, "fx", "supportFire_cannon", { "x": 7.5, "d": -2, "cut": 3, "i": 5, "fadeOut": 0.5 }]
  ]
 },
 "pointTarget": {
  "why": "The pointTarget clip is played by two skills: Two Pair (RPC_twoPair, Cat.cs:26177) and Copycat (RPC_copycat, :26732); one tile each (poolChains)",
  "skills": {
   "twoPair": {
    "why": "Cat.cs RPC_twoPair (:25518-26412), max rank sLv 2 (dispatch :6123): clip cut in (PlayAnimation(pointTarget, 0) :26177), Effects/twoPair_ring created at the hero, hero rotation (:26189-26207; life 1, followPosition; plays its own Sounds/twoPair) and voice twoPair1 / twoPair2 (Random.Range(0, 2) :26250-26309, PlayOneShot :26333 / :26339) at 0; Yield 0.4 (:26331): the statuses swapped (:25716-26038) and RPC_twoPair_hit (:26068, :9464-9510): twoPair_hit Instantiated at the hero + 0.5 up and at the target's feet + 0.5 up, identity (:9489, :9507): the 10 m target point; Yield 0.4 (:26328): standby at 0.8 s (:26107)",
    "cues": [
     [0, "fx", "twoPair_ring"],
     [0, "voice", "twoPair1|twoPair2"],
     [0.4, "fx", "twoPair_hit", { "y": 0.5 }],
     [0.4, "fx", "twoPair_hit", { "d": 10, "y": 0.5 }]
    ]
   },
   "copycat": {
    "why": "Cat.cs RPC_copycat (:26413-26939), max rank sLv 2 (dispatch :6144): clip cut in (PlayAnimation(pointTarget, 0) :26732), Effects/copycat_ring created at the hero, hero rotation (:26744-26762; life 1 + afterLife 1, followPosition; plays its own Sounds/copyCat) and voice copycat1 / copycat2 (Random.Range(0, 2) :26805-26864, PlayOneShot :26883 / :26891) at 0; Yield 0.4 (:26897): with the target hurt before (mLastDamage > 0, :26602; else 'Copycat fail', no effect :26635) RPC_copycat_hit (:26613, :9528-9574): copycat_hit Instantiated at the hero + 1 up and at the target's feet + 1 up, identity (:9553, :9571): the 10 m target point; Yield 0.3 (:26881): standby at 0.7 s (:26662)",
    "cues": [
     [0, "fx", "copycat_ring"],
     [0, "voice", "copycat1|copycat2"],
     [0.4, "fx", "copycat_hit", { "y": 1 }],
     [0.4, "fx", "copycat_hit", { "d": 10, "y": 1 }]
    ]
   }
  }
 },
 "throw1": {
  "why": "The throw1 clip is played by two skills: Lucky Card (RPC_luckyCard, Cat.cs:21102) and Lucky Dice (RPC_luckyDice, :24174); one tile each (poolChains)",
  "skills": {
   "luckyCard": {
    "why": "Cat.cs RPC_luckyCard (:20398-21253), max rank sLv 4 (dispatch :5933), Joker #402 on (passives on: damage and a 6 % Doom roll on the foe, :20850-20893, nothing drawn): clip restarted (Rewind, PlayAnimation(throw1, 0) :21099-21102); Yield 0.4 (:21151): the main weapon's renderers off (mWep1 = the right-hand weapon, CatEquipment.cs:949-1025; :20556-20583) until 0.8 s (case 6 :21020-21048 after standby; the 0.6 s branch :20909-20955 only runs if the skill was broken off), Effects/luckyCard_fire Instantiated at the cast spot + 1.2 up, FromToRotation(forward, the target's collider centre - that point) (:20593-20638): 3.43 deg down to the 0.6 m body centre at 10 m (life 1; plays its own Sounds/throw), voice luckyCard1 / luckyCard2 (Random.Range(0, 2) :20683-20746, PlayOneShot :21137 / :21129; the Bible's 'two card effect variants' at :20683 is this voice pick); Yield 0.1 (:21139): at 0.5 s the 20 m ray (:20790) and RPC_luckyCard_hit at its point (:20798, :9128-9130): the prefab field luckyCard_hit (the Cat prefab, checks/fx_cat_research/skills_b/probe_fields.txt) Instantiated there, hero rotation: the ray meets the 0.3 m body's front, 9.7 m ahead, 0.62 m up (legacy one-shot, autodestruct; plays its own Sounds/throw_hit); standby at 0.7 s (:20980)",
    "cues": [
     [0.4, "hideProp", "R", { "kill": 0.4 }],
     [0.4, "fx", "luckyCard_fire", { "y": 1.2, "rot": [ 3.43, 0, 0 ] }],
     [0.4, "voice", "luckyCard1|luckyCard2"],
     [0.5, "fx", "luckyCard_hit", { "d": 9.7, "y": 0.62 }]
    ]
   },
   "luckyDice": {
    "why": "Cat.cs RPC_luckyDice (:23682-24446), max rank sLv 2 (dispatch :6008), Roll the Dice #432 on (damage only in BB, :23939; TTO1102 plays rollTheDice1 / 2 instead of the voice with it, pseudo/Cat.c:15333-15345, report question 3): clip restarted (Rewind, PlayAnimation(throw1, 0) :24171-24174), Sounds/luckyDice (PlayOneShot :24186-24204, volume 1) and voice luckyDice1 / luckyDice2 (Random.Range(0, 2) :24247-24306, PlayOneShot :24358 / :24327) at 0; Yield 0.4 (:24349): the main weapon's renderers off (:23829-23856) until 0.8 s (:24101-24129), Effects/luckyDice Instantiated at the hero, identity (:23866-23884; life 2; its dice bounce on the floor: WorldParticleCollider, a part to build); Yield 0.1 (:24339): at 0.5 s the 6 m circle (:23934): hit() draws nothing (RPC_luckyDice_hit :9389 is never called); standby at 0.7 s (:24061)",
    "cues": [
     [0, "sound", "luckyDice"],
     [0, "voice", "luckyDice1|luckyDice2"],
     [0.4, "hideProp", "R", { "kill": 0.4 }],
     [0.4, "fx", "luckyDice"]
    ]
   }
  }
 },
 "throw2": {
  "why": "The throw2 clip is played by three skills: Flying Dagger (RPC_flyingDagger, Cat.cs:29762), Disarm (RPC_disarm, :34357) and Bleed (RPC_bleed, :35189); one tile each (poolChains)",
  "skills": {
   "flyingDagger": {
    "why": "Cat.cs RPC_flyingDagger (:28901-29923), max rank sLv 4 (dispatch :6207), Three Knives #403 on (passives on, hasSkill(403) :29168): clip restarted (Rewind, PlayAnimation(throw2, 0) :29759-29762), moveSpeed 2; Yield 0.2 (:29817): moveSpeed 6; Yield 0.3 (:29800): at 0.5 s the main weapon's renderers off (:29086-29113) until 0.95 s (:29668-29696 after Yield 0.15 :29833), three Effects/flyingDagger_fire Instantiated at the cast spot + 1.2 up and at TransformDirection(-+0.6, 0, -0.3) from it, each FromToRotation(forward, the target's collider centre - the middle point) (:29123-29184): 3.43 deg down (life 1; each plays its own Sounds/throw), voice threeKnives1 / threeKnives2 (Random.Range(0, 2) :29220-29285, PlayOneShot :29821 / :29802; without #403 one knife and flyingDagger1 / 2, :29291-29390); Yield 0.1 (:29804): at 0.6 s moveSpeed 0 and three parallel 20 m rays (:29455-29555): the middle one meets the 0.3 m body's front, flyingDagger_hit there, hero rotation (:29461, :9825-9848; plays its own Sounds/throw_hit); the side rays pass 0.6 m off the body and end 2 mm above the floor (1.2 - 0.06 x 19.96), no hit; standby at 0.8 s (:29628); the hero doesn't travel (2.2 m in the game)",
    "cues": [
     [0.5, "hideProp", "R", { "kill": 0.45 }],
     [0.5, "fx", "flyingDagger_fire", { "y": 1.2, "rot": [ 3.43, 0, 0 ] }],
     [0.5, "fx", "flyingDagger_fire", { "x": -0.6, "d": -0.3, "y": 1.2, "rot": [ 3.43, 0, 0 ] }],
     [0.5, "fx", "flyingDagger_fire", { "x": 0.6, "d": -0.3, "y": 1.2, "rot": [ 3.43, 0, 0 ] }],
     [0.5, "voice", "threeKnives1|threeKnives2"],
     [0.6, "fx", "flyingDagger_hit", { "d": 9.7, "y": 0.62 }]
    ]
   },
   "disarm": {
    "why": "Cat.cs RPC_disarm (:33800-34631), max rank sLv 2 (dispatch :6345): clip restarted (Rewind, PlayAnimation(throw2, 0) :34354-34357), moveSpeed 2, Effects/disarm_ring created at the hero, identity (:34369-34387; life 1, followPosition; plays its own Sounds/aura1) and voice disarm1 / disarm2 (Random.Range(0, 2) :34430-34489, PlayOneShot :34518 / :34532) at 0; Yield 0.2 (:34527): moveSpeed 6; Yield 0.3 (:34512): at 0.5 s the main weapon's renderers off (:33985-34012) until 0.95 s (:34263-34291 after Yield 0.15 :34536), Effects/disarm Instantiated at the cast spot + 1.2 up, FromToRotation(forward, the target's collider centre - that point) (:34022-34067): 3.43 deg down (life 1; plays its own Sounds/throw); Yield 0.1 (:34523): at 0.6 s the 20 m ray (:34127): RPC_disarm_hit at its point (:34135, :10219-10242): disarm_hit there, identity, on the 0.3 m body's front (plays its own Sounds/disarm_hit); the disarm status on the foe draws nothing here; standby at 0.8 s (:34223)",
    "cues": [
     [0, "fx", "disarm_ring"],
     [0, "voice", "disarm1|disarm2"],
     [0.5, "hideProp", "R", { "kill": 0.45 }],
     [0.5, "fx", "disarm", { "y": 1.2, "rot": [ 3.43, 0, 0 ] }],
     [0.6, "fx", "disarm_hit", { "d": 9.7, "y": 0.62 }]
    ]
   },
   "bleed": {
    "why": "Cat.cs RPC_bleed (:34632-35463), max rank sLv 2 (dispatch :6366): clip restarted (Rewind, PlayAnimation(throw2, 0) :35186-35189), moveSpeed 2, Effects/bleed_ring created at the hero, identity (:35201-35219; life 1, followPosition; plays its own Sounds/aura1) and voice bleed1 / bleed2 (Random.Range(0, 2) :35262-35321, PlayOneShot :35352 / :35341) at 0; Yield 0.2 (:35362): moveSpeed 6; Yield 0.3 (:35350): at 0.5 s the main weapon's renderers off (:34817-34839) until 0.95 s (:35095-35118 after Yield 0.15 :35348), Effects/bleed_fire Instantiated at the cast spot + 1.2 up, FromToRotation(forward, the target's collider centre - that point) (:34854-34899): 3.43 deg down (life 1; plays its own Sounds/throw); Yield 0.1 (:35370): at 0.6 s the 20 m ray (:34959): RPC_bleed_hit at its point (:34967, :10269-10292): bleed_hit there, identity, on the 0.3 m body's front (plays its own Sounds/bleed_hit); the bleed status on the foe draws nothing here; standby at 0.8 s (:35055)",
    "cues": [
     [0, "fx", "bleed_ring"],
     [0, "voice", "bleed1|bleed2"],
     [0.5, "hideProp", "R", { "kill": 0.45 }],
     [0.5, "fx", "bleed_fire", { "y": 1.2, "rot": [ 3.43, 0, 0 ] }],
     [0.6, "fx", "bleed_hit", { "d": 9.7, "y": 0.62 }]
    ]
   }
  }
 }
```

Build line for these alone (after the parts):
`uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py cat` (the
cue file names every effect, voice and sound; `"builds"` adds the shell, smoke and explosion). Every voice above is in
BB's rip (`heroes/cat/voices/`), and Sounds/luckyDice is in `heroes/cat/sounds/`.

## Offered to the user for the Bible (not written there)

- Lucky Card: the `Random.Range(0, 2)` at :20683 picks the voice (luckyCard1 / 2). There is one card effect, not
  "two card effect variants".
- Moon Storm: two 12 m blasts, at 0.9 and 1.0 s (`j < 2`), not one. The rings fall at 0.3-0.8 s. Moon Blade's
  circles fall at 0.3 and 0.4 s.
- Pillage Plunge: the dash runs 0.7-0.9 s at 24 m/s = 4.8 m (the hit at 0.8 s, 2.4 m in); standby 1.2 s.
- The five throws (Lucky Card, Lucky Dice, Flying Dagger, Disarm, Bleed) hide the main weapon while it is thrown
  (0.4-0.8 / 0.5-0.95 s).
- Swift Pace: the direction it passes is `vFlat(target - target)` = zero, so the Cat keeps her facing after the blink
  behind the target.
- Support Fire: the first shell 1.25 s after the cast; the cannons fade out over 0.5 s at the end.
- `RPC_luckyDice_hit` is dead code (never called, no prefab). BB's rip has rollTheDice1 / 2 and jokerCard1 / 2, and
  BB never plays them. TTO plays rollTheDice1 / 2 on Lucky Dice with Roll the Dice #432.

## Open questions (each with my recommendation)

1. **Melee hits with the target out of reach** (Moon Blade, Moon Storm, Pillage Plunge, Reverse Thrust): no hit
   effect, or the hit drawn where the game's box would be?
   *Recommended: no hit*, as the Bison's Over Swing / Slam (nothing reaches the 10 m target, and Moon Storm's blast
   that does draws nothing in the game).
2. **Swift Pace's landing ring**: at the hero (the page's hero doesn't travel), or at the landing spot behind the 10 m
   target (about 10.8 m)?
   *Recommended: at the hero, 0.1 m up* (the Penguin's Blink, the Bat's Switch: each effect with its owner).
3. **Lucky Dice's voice with Roll the Dice #432** (passives on): BB's luckyDice1 / 2, or TTO's rollTheDice1 / 2?
   *Recommended: BB's*. Sheep decision 10 takes TTO's voice only where BB's file is missing, and BB's files exist and
   play. If the user wants TTO's, the cue is `"rollTheDice1|rollTheDice2"`, and both wavs are in BB's rip.
4. **Copycat's hit needs a target hurt before** (`mLastDamage > 0`): show the success every play?
   *Recommended: yes*, the skill's look. The failure only prints a message.
5. **Support Fire's shells: random as the game** (a part, P2) **or a fixed list of cues?**
   *Recommended: the part*. Random picks are kept as the game makes them; fixed cues can't draw the cannon or the
   aim per shot. A fallback, if the part slips: ten fixed shells at 1.25 + 0.295 k s, cannons in turn, aim 35 m.
6. **Support Fire's hold**: keep `supportFire2*@3` (about 10 shells, the last landing after the hold)?
   *Recommended: keep 3 s*, the SEQ rule for a channel the player ends. Shells in flight finish on their own.
7. **The weapon hidden in the five throws** (P6): build `hideProp`?
   *Recommended: yes*, cheap and as the game. Without it the dagger / card stays in her hand while its copy flies.
8. **luckyDice's bounce (P5) and supportFire_hit's Shuriken (P4)**: build both before the Cat's cues are checked?
   *Recommended: yes* (missing parts are always built). P4 is the bigger job: it opens BB's ParticleSystem for every
   class (the inventory counts it in bison, cat, chameleon, mole, monkey, panda, rabbit, whale).
9. **Hits on the body's front `{"d": 9.7, "y": 0.62}` vs the target point `d 10`** for the four ray skills?
   *Recommended: 9.7 / 0.62*, the ray's point on the standard body (Bat decision 4, the Penguin's missile hits).
10. **`pillage`'s icon**: add `CLIP_SKILLS["cat"] = {"pillage": ["pillagePlunge"]}`?
    *Recommended: yes* (the tile has no icon otherwise).

## Verification

Checker, 2026-11-13 (read only; scripts in `checks/fx_cat_research/verify/`: `keys.py` dumps a Cat.cs range's effect /
voice / yield / clip / ray lines, `blocks.py` parses the paste-ready block and runs every cue through
`wardrobe_fx_check.py`'s KINDS / OPTS). Every coroutine in scope was re-read for its case order, yields, spawns, voices
and rotations.

**Confirmed** (no change): dispatch lines :5933 (luckyCard4), :6008, :6123, :6144, :6207 (flyingDagger4), :6324, :6345,
:6366, :6387, :6408, :6528 (+ getSpawnPos / `vFlat(target - target)` :6557-6562), :6621 -> :6655, :6675 -> :6709,
:7126, :7146. Moon Blade 0 / 0.2 / 0.3 / 0.4 / 0.5 / 0.8 (:35966-36141; 3 m and 4 m circles :35679 / :35781). Moon Storm:
rings i = 0..5 at 0.3-0.8 (`i < 6` -> IL_83D Yield(3, 0.1), :36675-36676, :36882), blasts at 0.9 and 1.0: the `break`
after `j++` (:36600) leaves the switch, which closes at :36607, and falls into IL_1A `j < 2` (:36608-36611), so two
blasts, standby at 1.0 (:36629). Pillage Plunge 0 / 0.7 / 0.8 / 0.9 / 1.2 (:40453-40627; ring1 Instantiate, ring2 /
ring3 createEffect, hero rotation). Reverse Thrust LookAt(-tDir) :31902, effect at 0.1 with `rotation x Euler(270, 90,
0)` :31181, boxes along `-transform.forward` :31353 / :31590, standby 1.0. Swift Pace :39597-39745. Support Fire: cannons
`Raycast(position + TransformDirection(3i - 10.5, 2, -2), down, 4, mask 5)` i = 1..6 (:41048-41084), supportFire2 looped
at 1.0 with `mUpdateTime = Time.time + 0.25` (:40832-40842), gap `0.01 x Random.Range(24, 36)` :41174, cannon
`Random.Range(0, length)` :41185, fire point + aim :41207-41212, SP :41255 (#404), shake :41261, end :41269 /
:10566 / :10603; RPC_supportFire_fire :10672-10753 (LookRotation(fireDir)), _hit :10802 identity, 8 m :10825;
Cat_supportFire.cs: the only public field is `Vector3 mVelocity` :240 (12 bytes), Init sets layer 1 and the velocity,
FixedUpdate looks along the velocity. getTrajectoryVector (Math.cs:885-965) re-derived: the `+` root, the `y < 0.1`
branch gives `num - 0.1 aim / v`, then `sin(num) x vFlat(mPos - mTarget).normalized + cos(num) x up` = 2.99-6.42 deg up:
shells.txt holds. Two Pair / Copycat :26177-26339 / :26602-26897 (hits at hero + 0.5 / + 1 and at the target's
`transform.position` + 0.5 / + 1, identity, :9489 / :9507, :9553 / :9571). Lucky Card: fire point `mPos + 1.2 up`,
fireDir = the target's `collider.bounds.center - mPos - 1.2 up` (:20593-20615), the hide :20556-20578 at 0.4, case 4's
re-enable skipped while still "attack" / "luckyCard" (:20909-20915 -> IL_FE6), case 6 at 0.8 (:21019-21043), ray
:20790, hit :20798 -> `Instantiate(luckyCard_hit, hitPos, hero rotation)` :9130, Joker lckAdjust(6) :20882. Lucky Dice
:24171-24358 (Sounds/luckyDice PlayOneShot, volume 1, :24204), effect identity :23884, 6 m circle :23934, re-enable
:24023 / :24124; RPC_luckyDice_hit :9389 has no caller and no ActionEvent string, and the rip has no
luckyDice_hit.prefab. Flying Dagger :29059-29833 (three knives :29174-29184 with the middle one's rotation, side rays
:29509 / :29555, hit :9848 hero rotation, threeKnives voice at 0.5). Disarm / Bleed :34354-34538 / :35186-35370 (rings
identity :34387 / :35219, hits identity :10242 / :10292). TTO's rollTheDice1 / 2 switch on 0x1b0 = 432 (pseudo/Cat.c
strings :14841-14857, test :15334). walk: `num2 > 5` -> `animation.Play("run")`, else `PlayAnimation("walk", 0.2)`
(:630-635). Every cued prefab exists in the rip; the probes' life / followState / AudioSource values match the report;
the inventory lines for luckyDice, supportFire_fire, supportFire_hit match P1, P4, P5. Icons: assets.js has every pool
member's key and cat_pillagePlunge5; `CLIP_SKILLS["cat"] = {"pillage": ["pillagePlunge"]}` is needed (hd/index.json's
cat block has no pillage today). The ray geometry (3.434 deg, `{"d": 9.7, "y": 0.62}`, side rays 0.6 m off and ending
2 mm up) and the rot sign (`rot [+x]` = pitch down, as the Bat's `[8.219, 0, 0]` and the Penguin's `[4.514, 0, 0]`)
hold. The page: poolChains gives the seven members their own tiles and hides the three clips (index.html:1274-1292);
cueOf passes unknown options through (`{...o}`, :4410-4412).

**Corrections:**

1. **P5 / Lucky Dice "collides with layer bit 1 = Default"**: the field is `m_CollidesWith.m_Bits: 1`, i.e. bit **0** =
   layer 0, Default (luckyDice.prefab:240-252, as treasureHunt.prefab:176-187). The page part is unchanged (the floor).
2. **The new cue kind and options fail today's check.** `pipeline/wardrobe_fx_check.py` accepts only
   `KINDS = ("fx", "voice", "sound", "skin", "clone")` (:127) and the option set OPTS (:125-126), so `hideProp` (five
   cues) and `volley` / `fadeOut` (seven cues) are reported as "bad cue" (blocks.py output). P2 / P3 / P6 must also add
   `"hideProp"` to KINDS and `"volley", "fadeOut"` to OPTS (beside the two index.html spots P6 names, :4636 and :4701).
   `"i"` is **not** new: it is already in OPTS and passed through by cueOf (the Penguin's TTO parts read it).
3. **Support Fire's `cut 3` (the ring and the six cannons) -> 2.95.** `seqTick` runs before `fxTick`
   (index.html:4741-4742), and `cut` is tested as `FX.t >= cutAt` (:4016). With the skill tab's วนซ้ำ on, the 3 s
   supportFire2 step ends (and the next round's fxStart resets FX.t to 0) on the frame FX.t would reach 3, so the cut
   never fires and the life-99 ring and cannons pile up each round (in the default once mode the idle tail keeps FX.t
   running, so 3 works there). 2.95 is the Penguin's precedent for a cut at a 3 s step's end (penguin.json cAttack2
   `manaField_ring`: "cut 2.95, the page's step ends at 3 s"). P2's "the ring's cut ends the volley" then stops it at
   2.95 (about ten shells still).
4. Not re-derived (no claim found wrong): item 8's other TTO line numbers and "`Waits__Get()` loses its float argument".

Everything else (every time, name, position, random pick, rank and buildability claim) checked out.

### Corrected paste-ready entry (only `supportFire1` changes; the other eight entries stand as written)

```json
 "supportFire1": {
  "why": "Cat.cs RPC_supportFire (:40696-41391), Support Fire #444, one rank (dispatch :6675), the SEQ Support Fire's first step: clip cut in (PlayAnimation(supportFire1, 0) :40894), Effects/supportFire_ring created at the hero, hero rotation (:40914-40932; life 99, followPosition, followState: ends when the channel does; its emblem and looping ring; plays its own Sounds/supportFire_ring) and voice supportFire1 / supportFire2 (Random.Range(0, 2) :40975-41034) at 0; six supportFire_cannon created where a 4 m ray down from TransformDirection(3i - 10.5, 2, -2), i = 1..6, meets the floor, hero rotation (:41043-41099: x -7.5 ... 7.5, 2 m behind; life 99 + afterLife 0.5, followState; AlphaTimer fades each in to 0.8 over 1 s); Yield 1 (:41332): supportFire2 looped from 1.0 s (:40832); the channel ends when the player moves (RPC_supportFire0 :10547-10624: standby, then every cannon's AlphaTimerFadeOut(0.5) :10603): cut 2.95, just inside the SEQ's supportFire2*@3 hold, read on supportFire2's own clock (FX.t restarts each step; seqTick runs before fxTick, so a cut of exactly 3 never fires when the tile loops; the Penguin's manaField_ring precedent); the shells: the ring's volley (a part to build, report Parts 1-2): from 1.25 s after the ring (mUpdateTime = Time.time + 0.25 at supportFire2's start :40842), every 0.01 x Random.Range(24, 36) = 0.24-0.35 s (:41174), a cannon at random (Random.Range(0, 6) :41185) plays its fire clip (Rewind + Play :10672-10677), supportFire_smoke and supportFire_fire are Instantiated at that cannon + TransformDirection(0, 1, 3), LookRotation(getTrajectoryVector(that point, 24 + Random.Range(0, 24) m ahead, 30)) (:41207-41217, :10693-10753); Cat_supportFire flies at 30 m/s with gravity 9.8 and lands 19-27 m ahead after 0.60-0.88 s (checks/fx_cat_research/skills_b/shells.txt), supportFire_hit at the floor, identity (Cat_supportFire.cs:163-190, Cat.cs:10776-10802); the shake (:41261) is screen only",
  "builds": [
   "supportFire_fire",
   "supportFire_smoke",
   "supportFire_hit"
  ],
  "cues": [
   [0, "fx", "supportFire_ring", { "cut": 2.95, "volley": { "first": 1.25, "every": [ 0.24, 0.35 ], "aim": [ 24, 47 ], "speed": 30, "from": [ 0, 1, 3 ] } }],
   [0, "voice", "supportFire1|supportFire2"],
   [0, "fx", "supportFire_cannon", { "x": -7.5, "d": -2, "cut": 2.95, "i": 0, "fadeOut": 0.5 }],
   [0, "fx", "supportFire_cannon", { "x": -4.5, "d": -2, "cut": 2.95, "i": 1, "fadeOut": 0.5 }],
   [0, "fx", "supportFire_cannon", { "x": -1.5, "d": -2, "cut": 2.95, "i": 2, "fadeOut": 0.5 }],
   [0, "fx", "supportFire_cannon", { "x": 1.5, "d": -2, "cut": 2.95, "i": 3, "fadeOut": 0.5 }],
   [0, "fx", "supportFire_cannon", { "x": 4.5, "d": -2, "cut": 2.95, "i": 4, "fadeOut": 0.5 }],
   [0, "fx", "supportFire_cannon", { "x": 7.5, "d": -2, "cut": 2.95, "i": 5, "fadeOut": 0.5 }]
  ]
 },
```

And in `pipeline/wardrobe_fx_check.py` (with P2 / P3 / P6):

```python
OPTS = {"d", "x", "y", "rot", "vol", "cut", "p", "roll", "scale", "kill", "to", "bone", "spread", "i", "n", "ignite", "hideHero", "notWorn",
        "worn", "end", "volley", "fadeOut"}
KINDS = ("fx", "voice", "sound", "skin", "clone", "hideProp")
```
