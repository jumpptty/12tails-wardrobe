<!-- Saved by the lead from the researcher's returned text (2026-11-13): its Write was refused. -->

Short summary: The Mole's Normal Attack is five shells. Stage 1 is nAttack1, and stages 2-5 are nAttack2 four times. Each clip starts at a fixed time after stage 1: 0.7, 1.2, 1.7 and 2.2 s. The shell is a lob that falls under gravity, so it needs a new part, Mole_nAttack, shaped like the Cat's Cat_supportFire: 15 m/s, nAttack_hit spawned where it lands. The Charge Attack is a burrow on the superDig clip, with the hero hidden from 0.6 s. It is released either as the plain surfacing or, with the Sky Drill passive, as the skyDrill clip. Emotes follow the usual pattern, with Mole-specific voices. KO is the Wolf's entry. The build stage needs four small new page features (`tune`, `hideHero`, `rot: "randomYaw"`, the Mole_nAttack options `firePoint` / `to`), plus an optional `propAnim`. Three hero-prefab fields are missing from the inventory.

=====================================================================
# Mole effects + sounds research: Normal Attack, Charge Attack (and its Sky Drill release), emotes, basic moves, KO

**Scope.**
- Clips nAttack1 and nAttack2: RPC_nAttack1, RPC_nAttack2 with repeat 2-5, and the dispatcher doNormalAttack.
- The Charge Attack: RPC_cAttack1 on superDig / dig1, doBeginCharge, doReleaseCharge, the release RPC_cAttack0 and, with the Sky Drill passive, the release RPC_skyDrill on the skyDrill clip.
- MP / SP transfer skills on an attack clip: the Mole has none.
- RPC_activateIcon1, the emotes (RPC_emotion), basic moves, KO (RPC_ko, RPC_dead) and RPC_revive.

**Method.** Research only (recipe steps 1-3), home PC, 2026-11-13. Line numbers are D:\12tails\DecompiledSource\Mole.cs unless another file is named. Times are seconds from the start of the clip the cue is keyed by. Distance 0 means at the hero. Every opaque predicate on these paths was evaluated by script (pred.py prints each `if (a - b op c)` with its truth value) and read by hand; each one goes the normal way.

**Files** (all in checks\fx_mole_research\attacks_emotes\):
- nAttack1.txt, RPC_*.txt: clip_flow.js dumps of RPC_nAttack1, RPC_nAttack2, RPC_cAttack1, RPC_cAttack0, RPC_skyDrill, RPC_emotion, RPC_ko, RPC_dead, RPC_revive and RPC_activateIcon1. pred.py is the predicate checker.
- probe.txt and probe_summary.txt: `wardrobe_fx.py mole --probe nAttack_fire,nAttack_hit,deadEffect,dig_dirt,dig_dust,dig_hole,superDig_dust,skyDrill` (read only).
- probe_parts.py: the Cat's parts probe pointed at the Mole, so it also shows the Rigidbody and colliders. Outputs probe_parts.txt and probe_parts2.txt (skyDrill, skyShaker_ring, skyDrill_ring).
- probe_fields2.txt: the Mole MonoBehaviour's fields. They are the AudioClip nAttack_fire (= nAttack_fireFx), the GameObjects nAttack_fire and nAttack_hit, the chopper / missile / kaiser objects, and deadEffect.
- field_keys.txt: those fields are the container's heroes/mole/sounds/nattack_fire (#229), effects/nattack_fire (#363), effects/nattack_hit (#364) and effects/deadeffect (#371), all in sharedassets8.
- probe_events.txt: none of the 95 Mole clips read has an AnimationEvent.
- rip_audio.txt: the rip's heroes/mole/voices (94 files) and sounds (46 files).
- geom.py and geom.txt: the shell's aim (Math.getTrajectoryVector) and its flight.
- cues.json: every entry below.

**TTO.** pseudo/Mole.c keeps the same strings in the same coroutines:
- `<RPC_nAttack1>d__203` :16954, with the trumpet notes and RPC_nAttack_fire;
- `<RPC_nAttack2>d__204` :17536;
- `<RPC_cAttack1>d__208` :6605;
- `<RPC_cAttack0>d__209` :6373;
- `<RPC_skyDrill>d__253` :20147.

Its waits are opaque, so the BB times stand. TTO moved the emotes and KO into BaseHero (pseudo/BaseHero.c :1900, :2391, :1217). Nothing in this scope is TTO-only.

---
## Read this first

**1. Normal Attack is five shells, not two clips (index.html work).**
- Combo 4 (#101-#104, max rank) gives five stages. The game plays nAttack1 once, then nAttack2 four times, all from one coroutine, RPC_nAttack2(repeat 2..5) (:9625, :9677, :9729, :9785).
- Only stage 1 sets actionTime. Each stage waits `Yield(2, actionTime - now + repeat × 0.5 - 0.3)` (:21352), so the clips start at 0.7, 1.2, 1.7 and 2.2 s.
- The page's current "Normal Attack: nAttack1 nAttack2" plays two whole 0.9 s clips.
- Proposed: "Normal Attack: nAttack1@0.7 nAttack2@0.5 nAttack2@0.5 nAttack2@0.5 nAttack2" (3.1 s).
  - Stages 2-5 cut in: Rewind + PlayAnimation(nAttack2, 0) at :20906-20911.
  - The first step keeps the page's fade. The game's is also a 0.2 s fade (:20611).
- The editor should check that a SEQ can repeat a clip: each step must restart the clip and call fxStart again. The four steps share the one nAttack2 entry, which is right because they are the same coroutine.

**2. The shell is a lob with gravity and needs a part (the Cat_supportFire shape).**
- RPC_nAttack_fire (:10070-10099) turns the shell along LookRotation(Math.getTrajectoryVector(firePos, target, 15)) (:10077).
- Mole_nAttack sets 15 m/s (ctor :28, Awake :53). The Rigidbody has gravity on (probe_parts.txt). Each FixedUpdate it turns along its velocity (:88).
- OnTriggerEnter (Mole_nAttack.cs:100-320) fires on any collider not on the owner's layer or layers 1 / 2, so the ground counts. It then spawns nAttack_hit at ClosestPointOnBounds with identity rotation (:156, :201, Mole.cs:10105).
- From the default fire point the shell rises 6.753 deg and lands 9.833 m ahead after 0.62 s (geom.txt).
- Every landing falls inside the next stage. The four nAttack2 steps would each need different landing cues, which the page cannot express. So the part must spawn the hit itself, with "builds": ["nAttack_hit"].
- nAttack_fire, nAttack_hit and deadEffect are not in plans/fx_inventory.md "### mole". All three are hero-prefab fields, not Resources.Load paths.

**3. The fire point follows the worn cannon.**
- fireOffset = TransformDirection(0.2, 1, 0.6), replaced by the weapon's "firePoint" node when it has one (:20396-20417, :21158-21174).
- 28 of the 44 BB Mole weapons have one (12tails-video props\json\mole_weapons.json).
- The aim always ends at the target point (fireDir = tDir - fireOffset, :20423), so the pitch changes with the fire point.
- The cues give the default (x 0.2, y 1, d 0.6, rot [-6.753, -1.219, 0]) plus two new part options: "firePoint": "R" and "to": [0, 0, 10]. See Question 2.

**4. Two weapons change the shot** (both are wardrobe items).
- **Double Cannon** (w_mol59 = specialCannon, no firePoint): fires two shells, from firePos ∓ 0.3 right, along rotateH(fireDir, ±9) (:20428-20439; Math.cs:838-843, where +9 turns left).
  - Left shell: rot [-6.753, -10.219, 0], lands x -1.738, d 9.689.
  - Right shell: rot [-6.753, 7.781, 0], lands x 1.750, d 9.750.
- **Trumpet** (w_mol25 = trumpet): each shot plays the next note of a 26-note tune, Mary Had a Little Lamb in do / re / me.
  - The tune is v6HdwFeOMZ (:32); the notes are loaded and played at :20251-20353.
  - The counter is a Mole field, pre-incremented with Mathf.Repeat(i + 1, 26) (:20293), so a fresh hero starts on the 2nd note.
  - With the Trumpet, stage 1 drops the cannon sound (weapon != "w_mol25", :20383). Stages 2-5 have no such test and play both (:21146-21152), a BB quirk.

**5. A cannon sound from the hero's own code.**
- audio.PlayOneShot(nAttack_fireFx, 1) on every shot, on the own client in a mission / arena only, as the shot itself (:20361-20389).
- nAttack_fireFx is the prefab's AudioClip field "nAttack_fire" = sounds/nattack_fire, so it is a "sound" cue.
- The effect nAttack_fire has no AudioSource. nAttack_hit plays its own sounds/nattack_hit.

**6. The Charge Attack is the burrow, played on superDig, and the Mole has no charge SEQ yet.**
- With Super Dig #411 on (passives rule), superDig plays (dig1 without it, :22290-22304).
- At 0.6 s (dig-in = 1 - 0.2 × Speed Drill 2, :21609), every renderer of the hero is switched off (:22031-22053) until the release. Underground, a dig_dirt mound appears every 0.2 s.
- The release (doReleaseCharge :9938) is one of two:
  - RPC_cAttack0: three dust puffs and a root crossfade;
  - RPC_skyDrill on the skyDrill clip: when Sky Drill is learned, more than 3 s have passed since the press, and it is a mission (:9987-10023).
- The 12 s auto-surfacing (4 × Charge Attack 3, :21553, :21716-21750) is always the plain one, never Sky Drill.
- dig2 is never played by BB or TTO; only the PlayAnimation table loads it (:709).
- Proposed (Question 3):
  - "Charge Attack: superDig@0.7 dig2*@2.3 root~@0.2": released at 3.0 s, plain surfacing. At exactly 3 s the `> 3` test is false. This follows the SEQ rule's "at least 3 s" for a hold that runs until the player lets go.
  - "Sky Drill: superDig@0.7 dig2*@2.31 skyDrill": the same burrow released at 3.01 s, with Sky Drill 2 and Sky Shaker #413 (passives on). It gets its own tile under one-tile-per-skill: Sky Drill #313-314 is a passive with its own clip.
- dig2 serves as the hidden underground step. This gives the release's cues a key of their own, "@ChargeAttack:root".
- The parallel effect_only report lists Sky Drill as someone else's (plans/fx_mole/effect_only.body.md:53). If a skills report also cues skyDrill, keep one entry.
- dig1 stays a tile for King Kaiser (PlayAnimation("dig1", 0.2) :35389), which another report covers.

**7. No MP / SP transfer style skill plays an attack clip.** Only RPC_nAttack1 (:20611) and RPC_nAttack2 (:20911) play nAttack1 / nAttack2. I checked every PlayAnimation, animation.Play and CrossFade in Mole.cs.

**8. Emote voices differ from the other classes'** (rip_audio.txt, :46201-46227).
- The rip has no bow, beg, sit, talk or dance voice. emo_bow and emo_beg are silent. The bow tile takes emo_ty's "ty", as the talk tile takes chat's voice.
- chat is "chat" + Random.Range(1, 4) = chat1-3 (:46207), although the rip has chat1-5.
- emo_pose has a voice, "pose", played before the clip is chosen from the worn set. Every pose clip BB plays gets it: pose, pose5, 15, 25, 35, 45, 46, 58, 65 and 66.
- pose37 and the TTO emote clips (clap, cooking, fishingMole, mining, planting, wai) stay silent (Cat decision 16).

**9. getUp is silent.** RPC_revive asks for Voices/revive (:52973), which the Mole's rip lacks, and it plays only if the file loads (:52985). So the Mole gets no counterpart to the Cat's getUp entry. KO is the Wolf's shape.

**10. Mission-only gates are kept**, following the Sheep / Penguin / Wolf precedent:
- gated: the shell and the cannon sound (mGameType > 4, :20369, :21138), superDig_dust (:21637), Sky Drill (:9999);
- not gated: the trumpet note, the voices, dig_hole, dig_dirt and dig_dust.

---
## The dispatcher: doNormalAttack (:9515-9835)

- **Aim:** vector = targetArray[0] - position (:9555-9557). Within 3 m it becomes 4 × vFlat(vector).normalized + up (:9559-9563). There is no lowering when no target object is passed (unlike the Penguin's -0.25).
- **Stage 1:** from standby / run, when nAttack is off timeout (:9806-9813).
- **Later stages, while attacking:**

| myCommand | needs | press before (stage 1 +) | starts | lines |
|---|---|---|---|---|
| "nAttack1" | #101 | 0.5 s | repeat 2 | :9607, :9617, :9625 |
| "nAttack2" | #102 | 0.8 s | repeat 3 | :9659-9677 |
| "nAttack3" | #103 | 1.1 s | repeat 4 | :9711-9729 |
| "nAttack4" | #104 | 1.4 s | repeat 5 | :9767-9785 |

- There is no lower bound on any press window.
- RPC_nAttack2's entry sets only actionState and myCommand (:21333-21336), never actionTime. The clips therefore start at 0.7, 1.2, 1.7 and 2.2 s (:21352).
- Each stage's standby (stage 1 at 0.7 :20535-20551; later stages at 0.5 :21297-21313) checks its own myCommand, so it is skipped once the next stage has been pressed.

## The shell (geom.txt)

- **Aim from the default point:** from (0.2, 1, 0.6) to (0, 0, 10), so d = 9.402 and y = -1.
  - First angle: num = atan((225 + sqrt(15⁴ - 9.8² d²)) / (-9.8 d)) = -1.3599.
  - The y < 0.1 correction (f = 2 atan(y / d) = -0.2120) gives num = -1.4530.
  - Result: Unity Euler [-6.753, -1.219, 0].
- **Flight:** 0.02 s steps, g = -9.8, ground test on the 0.25 × 0.25 × 0.5 trigger box (as the Cat's). Apex 1.14 m. Lands at x 0.004, d 9.833 after 0.62 s.
- **Aimed 0.6 m up instead** (an enemy's bounds centre): rot [-8.214, -1.219, 0], lands d 10.69 after 0.68 s.
- **Landing times from stage 1:** 0.92, 1.52, 2.02, 2.52, 3.02 s. In step time that is 0.22 s into stage 2 for stage 1's shell, 0.32 s into stage k+1 for stage k's, and 0.82 s into the last clip for stage 5's. The part spawns the hits, so no landing cues are needed.

## nAttack1 (stage 1) — coroutine $RPC_nAttack1$23447 (:20098-20710)

**At 0 s**
- Sets actionState "attack", actionTime, myCommand "nAttack1" and addTimeOut("nAttack", 1.5); turns to the aim; plays the clip with a 0.2 s fade; moveSpeed 0 (:20593-20620).
- Voice nAttack1 (:20658, PlayOneShot :20704).
- Waits 0.3 s (Yield 2 :20696).

**At 0.3 s, if still attacking (:20215)**
- The weapon's Animation plays "fire" (:20243).
- The Trumpet plays its next note (:20251-20353).
- On the own client in a mission only: Sounds/nAttack_fire at volume 1, unless the Trumpet is held (:20361-20389).
- The shell or shells (:20396-20473).
- Waits 0.4 s (Yield 3 :20700).

**At 0.7 s**
- The weapon plays "root" if it has that clip (:20514-20520).
- Standby, unless stage 2 was pressed (:20529-20551).

With no weapon at all, :20401 would throw on mWep1.transform before the shot. The wardrobe's bare-handed Mole simply fires from the default point.

## nAttack2 (stages 2-5) — coroutine $RPC_nAttack2$23459 (:20753-21364)

**At the press**
- Sets attack and myCommand "nAttack"+repeat, then waits (:21333-21352).

**At 0 s**
- If still attacking: turns to the aim, moveSpeed 0, addTimeOut, Rewind, clip cut in (:20891-20916).
- Voice nAttack2 (:20958, :21359).
- Waits 0.2 s (:21346).

**At 0.2 s**
- Weapon "fire" (:21012).
- Trumpet note (:21020-21122).
- On the own client in a mission: Sounds/nAttack_fire, with no Trumpet test (:21130-21152).
- The shell or shells (:21158-21235).
- Waits 0.3 s (:21355).

**At 0.5 s**
- Weapon "root"; standby unless the next stage was pressed (:21257-21313).

## Charge Attack: superDig, the burrow (dig2), the release

**doBeginCharge** (:9839-9925) starts RPC_cAttack1 (:9909) when:
- the hero is in standby or run;
- cAttack is off timeout;
- #111 is learned;
- at least 0.1 s have passed since the last action.

**Ranks** (passives on, max): Charge Attack 3 (getChargeAttackLv returns 3), Speed Drill 2, Super Dig #411, Sky Drill 2 (#314), Sky Shaker #413.

**RPC_cAttack1** ($RPC_cAttack1$23473, :21411-22513), from its entry IL_1BD8 (:22271):

| t (s) | what happens | lines |
|---|---|---|
| 0 | attack, actionTime, myCommand "cAttack1", addTimeOut(cAttack, 1), turn to aim | :22272-22466 |
| 0 | superDig cut in (dig1 without #411) | :22290-22304 |
| 0 | voice superDig (cAttack without #411), at most every 2 s | :22348-22414 |
| 0 | dig_hole at position + 0.05 up, hero rotation | :22446 |
| 0 | dustTimer = now + 0.1 | :22466 |
| 0.1, 0.3, 0.5 | superDig_dust at the hero, every 0.2 s, mission only | :21608-21690 |
| 0.6 | every renderer off, CharacterController shrunk; then waits 0.1 | IL_858 :22030-22182; Yield 4 :22503 |
| 0.7 | case 4: digTime, digTimeOut 12; the underground loop every frame | :21533-21561 |
| 0.9, 1.1, … | dig_dirt at the hero, Euler(0, Random.Range(0, 360), 0), every 0.2 s | :21758-21792 |
| (underground) | also removeLockStatus(5), the mouse movement, the Super Dig heal (below max HP only) | :21694-21880 |
| 12.0 | auto-surfacing with RPC_cAttack0, never Sky Drill | :21716-21750 |
| release | renderers back on | :21888-21951 |

Without Super Dig (passives off, not shown): the clip is dig1, the voice is "cAttack", the dig-in lasts 0.9 s, and dig_dust comes every 0.1 s (IL_132B :22185-22267).

**doReleaseCharge** (:9938-10040), while attacking with cAttack1:
- If Sky Drill is learned, Time.time - actionTime > 3, and mGameType > 4: RPC_skyDrill(expandPos, vector, 0, 2) (:9987-10018).
- Otherwise: RPC_cAttack0 (:10027).
- expandPos = getExpandPos(position, 1, 0.4) (:9954). On open ground that is the hero's own spot (Math.cs:1242).

**RPC_cAttack0** ($RPC_cAttack0$23515, :22647-22879):
- attack, myCommand "cAttack0";
- three dig_dust at the hero with its rotation (:22810-22838);
- turns to the aim, moveSpeed 0, CrossFade("root", 0.2) (:22864);
- standby 0.2 s later (:22877, :22776).

**Prefabs** (probe_parts.txt); all ready:
- dig_hole: life 5, an Animation on the hole. Its child digSound has its own EffectControl (life 2) and plays the looping sounds/dig; index.html already handles a child's EffectControl (:4068, :4135).
- dig_dirt: life 2, an Animation on the mound.
- superDig_dust and dig_dust: life 1, a one-shot Smoke1 ellipsoid.

### Sky Drill (the charge's release with the passive) — $RPC_skyDrill$23747 (:31496-32186)

**At 0 s**
- totalDigTime (:31795); attack, actionTime, myCommand "skyDrill"; turn to aim; clip cut in; moveSpeed 0 (:31800-31840).
- Voice skyDrill1 or skyDrill2 (:31874-31933).
- skyDrill created at the hero with rotation × Euler(270, 90, 0) (createEffect :31960).
- With Sky Shaker #413: skyShaker_ring at the hero (:31998), in place of skyDrill_ring (:32033).
- Left out: the camera blur (:32059) and shake (:32153), and Sky Shaker's 5 m hit (:32085-32128).

**At 0.1 and 0.2 s:** the two drill rings (Yield 2 0.1 :32184; FindAreaTarget 1 / 2 m :31649; skyDrill_hit only on an enemy hit, :31688).

**At 1.0 s:** standby (Yield 3 0.8 :32180, :31743).

**Prefabs** (probe_parts2.txt); both ready:
- skyDrill: life 0.55, followPosition, followState, an Animation on two skinned drills.
- skyShaker_ring: life 1 + 1, plays sounds/skyDrill.

---
## Emotes and basic moves

**RPC_emotion** ($RPC_emotion$24108, :45917-46738):
- The voice plays at 0 s, before the clip (:46149-46227).
- It is gated by the voice option, Time.time > actionTime + 2, and the player being the own hero, game code 31 or a mission teammate.
- emo_chat loads chat + Random.Range(1, 4). Every other emo_<name> loads Voices/<name> and plays only if the file loads.
- Then the clip with a 0.2 s fade. There are no effects and no Sounds/ loads.

| emote | clip | voice | lines |
|---|---|---|---|
| hi, wave | wave | hi / wave | :46263, :46270 → :46704 |
| ty, bow | bow | ty / (none) | :46279, :46286 → :46697 |
| laugh | laugh | laugh | :46293 |
| sit | sit | (none) | :46313 |
| sleep | sleep | sleep | :46325 |
| cheer | cheer | cheer | :46337 |
| beg | beg | (none) | :46349 |
| cry | cry | cry | :46361 |
| talk, chat | talk | (none) / chat1-3 | :46375, :46382 → :46675 |
| pose | by worn set | pose | :46389-46635 |
| battle | battle | battle | :46645 |
| dance | dance | (none) | :46660 |

emo_pose picks pose5 / 15 / 25 / 35 / 45 / 58 / 65 / 46 / 66 by the worn set, a frozen pose with w_mol56 + c_all56 (animation.Stop :46595-46610), else pose.

**Basic moves:** nothing. PlayerControl (:9041-9476) plays run / root / falling with no sound, and no Mole clip has an AnimationEvent.

**RPC_activateIcon1:** loops "pose" (:51782) with activate1 / activate2 (:51837, :19176). No tile (Penguin decision 19).

**KO**
- RPC_ko ($RPC_ko$24281, :52008-52354): ko clip (:52222), ko1 or ko2 at 0 s, getUp after 3 s (:52347, :52124).
- RPC_dead ($RPC_dead$24288, :52387-52712): Rewind + ko (:52581-52584), dead1 or dead2, and always deadEffect at the hero's position and rotation. IL_408 (:52687) is reached by every voice path.
- deadEffect: life 3, an ImageEmitter (mole_dead) 0.8 m up and two Dust1 LineEmitters; ready.

**RPC_revive** (:52744-53017): Voices/revive is missing from the rip, so it is silent.

No entry for sit, beg, dance, getUp, root, run, falling, pose37 or the TTO emote clips.

---
## Paste-ready cue entries for wardrobe/fx_cues/mole.json (identical to checks\fx_mole_research\attacks_emotes\cues.json)

```json
  "nAttack1": {
    "why": "Mole.cs RPC_nAttack1 (:20098-20710), Combo stage 1 (doNormalAttack :9813): clip at 0 with a 0.2 s fade (PlayAnimation(nAttack1, 0.2) :20611) and the voice nAttack1 at 0 (load :20658, PlayOneShot :20704, then Yield(2, 0.3) :20696); 0.3 s, still attacking (:20215): the worn weapon's Animation plays fire (:20243); the Trumpet (w_mol25 = trumpet, :20251) plays the next note of its 26-note tune (trumpet_do / re / me by v6HdwFeOMZ = [3,2,1,2,3,3,3,2,2,2,3,3,3,3,2,1,2,3,3,3,1,2,2,3,2,1] :32, index pre-incremented by Mathf.Repeat(i + 1, 26) :20293, PlayOneShot :20315 / :20334 / :20353; all clients, all modes); own client in a mission / arena only (isMine :20361, mGameType > 4 :20369, the Sheep / Penguin precedent keeps it): Sounds/nAttack_fire (the prefab's nAttack_fireFx field, AudioClip sharedassets8 #229 = heroes/mole/sounds/nattack_fire, checks/fx_mole_research/attacks_emotes/field_keys.txt) at volume 1 unless the Trumpet is held (:20383-20389); the shell from firePos = position + TransformDirection(0.2, 1, 0.6), or the worn weapon's firePoint node (:20396-20418; 28 of the 44 BB cannons have one), aimed at the target point (fireDir = tDir - fireOffset :20423, firePos + fireDir = the 10 m ground point, decision 1 of the Penguin): RPC_nAttack_fire (:20473) = Instantiate(nAttack_fire, firePos, LookRotation(Math.getTrajectoryVector(firePos, target, 15))) (:10077-10080): pitch up 6.753 deg, yaw -1.219 deg (checks/fx_mole_research/attacks_emotes/geom.txt); Double Cannon (w_mol59 = specialCannon, no firePoint) fires two instead, from firePos -+ 0.3 right along rotateH(fireDir, +-9) (:20428-20439): yaw -10.219 / 7.781; Mole_nAttack flies it at 15 m/s with gravity (Mole_nAttack.cs:28, :53, :88; Rigidbody gravity on, box trigger 0.25 x 0.25 x 0.5, probe_parts.txt) and on the ground calls RPC_nAttack_hit at the contact point (Mole_nAttack.cs:156, :201) = nAttack_hit with Quaternion.identity (:10105; plays its own Sounds/nAttack_hit): it lands 9.83 m ahead after 0.62 s (part-spawned: builds); standby at 0.7 s (Yield(3, 0.4) :20700, :20541) unless stage 2 is pressed",
    "builds": ["nAttack_hit"],
    "cues": [
      [0, "voice", "nAttack1"],
      [0.3, "sound", "trumpet_do|trumpet_re|trumpet_me", {"worn": ["R", "trumpet"], "tune": ["trumpet_re", "trumpet_do", "trumpet_re", "trumpet_me", "trumpet_me", "trumpet_me", "trumpet_re", "trumpet_re", "trumpet_re", "trumpet_me", "trumpet_me", "trumpet_me", "trumpet_me", "trumpet_re", "trumpet_do", "trumpet_re", "trumpet_me", "trumpet_me", "trumpet_me", "trumpet_do", "trumpet_re", "trumpet_re", "trumpet_me", "trumpet_re", "trumpet_do", "trumpet_me"]}],
      [0.3, "sound", "nAttack_fire", {"notWorn": ["R", "trumpet"]}],
      [0.3, "fx", "nAttack_fire", {"x": 0.2, "y": 1, "d": 0.6, "rot": [-6.753, -1.219, 0], "to": [0, 0, 10], "firePoint": "R", "notWorn": ["R", "specialCannon"]}],
      [0.3, "fx", "nAttack_fire", {"x": -0.1, "y": 1, "d": 0.6, "rot": [-6.753, -10.219, 0], "worn": ["R", "specialCannon"]}],
      [0.3, "fx", "nAttack_fire", {"x": 0.5, "y": 1, "d": 0.6, "rot": [-6.753, 7.781, 0], "worn": ["R", "specialCannon"]}]
    ]
  },
  "nAttack2": {
    "why": "Mole.cs RPC_nAttack2 (:20753-21364), Combo stages 2-5 (one coroutine, repeat 2-5: doNormalAttack :9625, :9677, :9729, :9785, presses before stage 1 + 0.5 / 0.8 / 1.1 / 1.4 s with #101-#104 :9607-9777): its clip at stage 1 + 0.5 x repeat - 0.3 = 0.7 / 1.2 / 1.7 / 2.2 s (Yield(2, actionTime - now + repeat x 0.5 - 0.3) :21352; actionTime is set by stage 1 only, the entry sets actionState / myCommand :21333-21336): Rewind and the clip cut in (PlayAnimation(nAttack2, 0) :20906-20911), the voice nAttack2 at 0 (load :20958, PlayOneShot :21359, then Yield(3, 0.2) :21346); 0.2 s: the weapon's fire clip (:21012), the Trumpet's next note (:21020-21122, the same counter as stage 1), Sounds/nAttack_fire on the own client in a mission / arena (:21130-21152; unlike stage 1, played with the Trumpet too: no w_mol25 test), the shell as in stage 1 (:21158-21235; Double Cannon :21190-21201); standby 0.5 s (Yield(4, 0.3) :21355, :21303) unless the next stage is pressed; each shell lands 0.62 s after its shot (part-spawned nAttack_hit: stage k's in stage k + 1 at 0.32 s, the last one at 0.82 s of this 0.9 s clip)",
    "builds": ["nAttack_hit"],
    "cues": [
      [0, "voice", "nAttack2"],
      [0.2, "sound", "trumpet_do|trumpet_re|trumpet_me", {"worn": ["R", "trumpet"], "tune": ["trumpet_re", "trumpet_do", "trumpet_re", "trumpet_me", "trumpet_me", "trumpet_me", "trumpet_re", "trumpet_re", "trumpet_re", "trumpet_me", "trumpet_me", "trumpet_me", "trumpet_me", "trumpet_re", "trumpet_do", "trumpet_re", "trumpet_me", "trumpet_me", "trumpet_me", "trumpet_do", "trumpet_re", "trumpet_re", "trumpet_me", "trumpet_re", "trumpet_do", "trumpet_me"]}],
      [0.2, "sound", "nAttack_fire"],
      [0.2, "fx", "nAttack_fire", {"x": 0.2, "y": 1, "d": 0.6, "rot": [-6.753, -1.219, 0], "to": [0, 0, 10], "firePoint": "R", "notWorn": ["R", "specialCannon"]}],
      [0.2, "fx", "nAttack_fire", {"x": -0.1, "y": 1, "d": 0.6, "rot": [-6.753, -10.219, 0], "worn": ["R", "specialCannon"]}],
      [0.2, "fx", "nAttack_fire", {"x": 0.5, "y": 1, "d": 0.6, "rot": [-6.753, 7.781, 0], "worn": ["R", "specialCannon"]}]
    ]
  },
  "superDig": {
    "why": "Mole.cs RPC_cAttack1 (:21411-22513), Charge Attack 3 (#113, digTimeOut 4 x 3 = 12 s :21553), Speed Drill 2 (#312), Super Dig #411 on (passives rule): at 0 the clip superDig cut in (PlayAnimation(superDig, 0) :22290-22296; dig1 without #411 :22304), the voice superDig (#411 :22359-22383; cAttack without it :22402-22414; at most every 2 s :22348), dig_hole 0.05 m up with the hero's rotation (:22446; EffectControl life 5, its digSound child plays the looping Sounds/dig for 2 s); the dig-in (IL_26 :21608-21690) until actionTime + 1 - 0.2 x 2 = 0.6 s (:21609): superDig_dust at the hero with its rotation every 0.2 s from 0.1 s (dustTimer :22466, :21645-21676; mission / arena only, mGameType > 4 :21637, kept as the Sheep / Penguin precedent) = 0.1, 0.3, 0.5 s; at 0.6 s every renderer of the hero off (IL_858 :22031-22053) until the release, when the loop sees myCommand change (:21934-21951): hidden 0.6 to 3.0 s (the release at 3.0 s in the Charge Attack tile, 3.01 s in Sky Drill's); then Yield(4, 0.1) (:22503) to the underground loop at 0.7 s (case 4 :21533-21561), the dig2 step",
    "cues": [
      [0, "voice", "superDig"],
      [0, "fx", "dig_hole", {"y": 0.05}],
      [0.1, "fx", "superDig_dust"],
      [0.3, "fx", "superDig_dust"],
      [0.5, "fx", "superDig_dust"],
      [0.6, "hideHero", "dig", {"kill": 2.4}]
    ]
  },
  "dig2": {
    "why": "Mole.cs RPC_cAttack1's underground loop (IL_1535 :21694-21880, every frame from 0.7 s while myCommand is cAttack1): dig_dirt at the hero's position with a random yaw (Quaternion.Euler(0, Random.Range(0, 360), 0) :21792; EffectControl life 2, its Animation raises the mound) whenever 0.2 s have passed since the last (digTime :21548, :21758-21764): 0.9, 1.1, ... s = 0.2, 0.4, ... s into this step, the last at 2.9 s before the 3.0 s release; not mission-gated; the hero moves underground in the game (:21813-21818), here in place (Penguin decision 8); the Super Dig heal every 2 s (:21823-21860) needs HP below max and draws nothing at full HP; the auto-surfacing at 12 s (:21716-21750) is not reached; dig2 itself is never played by BB or TTO code (only loaded, :709): the hidden hero's step",
    "cues": [
      [0.2, "fx", "dig_dirt", {"rot": "randomYaw"}],
      [0.4, "fx", "dig_dirt", {"rot": "randomYaw"}],
      [0.6, "fx", "dig_dirt", {"rot": "randomYaw"}],
      [0.8, "fx", "dig_dirt", {"rot": "randomYaw"}],
      [1.0, "fx", "dig_dirt", {"rot": "randomYaw"}],
      [1.2, "fx", "dig_dirt", {"rot": "randomYaw"}],
      [1.4, "fx", "dig_dirt", {"rot": "randomYaw"}],
      [1.6, "fx", "dig_dirt", {"rot": "randomYaw"}],
      [1.8, "fx", "dig_dirt", {"rot": "randomYaw"}],
      [2.0, "fx", "dig_dirt", {"rot": "randomYaw"}],
      [2.2, "fx", "dig_dirt", {"rot": "randomYaw"}]
    ]
  },
  "@ChargeAttack:root": {
    "why": "Mole.cs doReleaseCharge (:9938-10040): released after 3 s or less underground (Time.time - actionTime > 3 is false, :9993; Sky Drill's tile shows the later release) -> RPC_cAttack0 (:10027, coroutine :22647-22879) at getExpandPos(position, 1, 0.4) (:9954, the hero's own spot on open ground): dig_dust three times at the hero with its rotation (:22828-22838; EffectControl life 1, not mission-gated), the hero shown again (RPC_cAttack1 :21934-21951), CrossFade(root, 0.2) (:22864), standby 0.2 s later (Yield(2, 0.2) :22877, :22776)",
    "cues": [
      [0, "fx", "dig_dust"],
      [0, "fx", "dig_dust"],
      [0, "fx", "dig_dust"]
    ]
  },
  "skyDrill": {
    "why": "Mole.cs doReleaseCharge (:9972-10023): Sky Drill 2 (#314, passives rule) learned, more than 3 s since the press (:9993), mission / arena (mGameType > 4 :9999, kept): RPC_skyDrill (:12265, coroutine :31496-32186) instead of the plain surfacing: at 0 the clip cut in (PlayAnimation(skyDrill, 0) :31825), the hero shown again (myCommand skyDrill :31810 ends RPC_cAttack1's loop), voice skyDrill1 or skyDrill2 (Random.Range(0, 2) :31874, PlayOneShot :31898 / :31929), skyDrill created at the hero with rotation x Euler(270, 90, 0) (createEffect :31960; EffectControl life 0.55, followPosition, followState; its drills' Animation), Sky Shaker #413 on: skyShaker_ring at the hero (:31974-31998; plays its own Sounds/skyDrill) in place of skyDrill_ring (:32021-32033); the Sky Shaker 5 m hit and the two drill rings at 0.1 and 0.2 s (Yield(2, 0.1) :32184, :31649; 1 and 2 m) reach no target at 10 m: nothing drawn (Cat decision 19); camera blur and shake (:32059, :32153) left out; standby 1.0 s (Yield(3, 0.8) :32180, :31743)",
    "cues": [
      [0, "voice", "skyDrill1|skyDrill2"],
      [0, "fx", "skyDrill", {"rot": [270, 90, 0]}],
      [0, "fx", "skyShaker_ring"]
    ]
  },
  "wave": {
    "why": "Mole.cs RPC_emotion (:45917-46738): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (Substring(4) :46215, PlayOneShot :46227, only if the file loads :46221; the gates :46149-46183); no effect, no sound; the rip's Mole voices have hi, wave, ty, laugh, sleep, cheer, cry, battle, pose, chat1-5 and no bow, beg, sit, talk, dance (checks/fx_mole_research/attacks_emotes/rip_audio.txt); emo_hi (:46263) and emo_wave (:46270) both play the wave clip (:46704): voice hi or wave",
    "cues": [
      [0, "voice", "hi|wave"]
    ]
  },
  "bow": {
    "why": "Mole.cs RPC_emotion (:45917): emo_ty (:46279) and emo_bow (:46286) both play the bow clip (:46697); emo_ty's voice ty is in the rip, emo_bow's Voices/bow is not (rip_audio.txt), so emo_bow is silent: the tile takes the voiced emote's ty (as talk takes chat's)",
    "cues": [
      [0, "voice", "ty"]
    ]
  },
  "laugh": {
    "why": "Mole.cs RPC_emotion (:45917): voice at 0, emo_<name> = Voices/<name> (:46215, PlayOneShot :46227); emo_laugh (:46293-46299)",
    "cues": [
      [0, "voice", "laugh"]
    ]
  },
  "sleep": {
    "why": "Mole.cs RPC_emotion (:45917): voice at 0, emo_<name> = Voices/<name> (:46215, PlayOneShot :46227); emo_sleep (:46325-46331)",
    "cues": [
      [0, "voice", "sleep"]
    ]
  },
  "cheer": {
    "why": "Mole.cs RPC_emotion (:45917): voice at 0, emo_<name> = Voices/<name> (:46215, PlayOneShot :46227); emo_cheer (:46337-46343)",
    "cues": [
      [0, "voice", "cheer"]
    ]
  },
  "cry": {
    "why": "Mole.cs RPC_emotion (:45917): voice at 0, emo_<name> = Voices/<name> (:46215, PlayOneShot :46227); emo_cry (:46361-46367)",
    "cues": [
      [0, "voice", "cry"]
    ]
  },
  "talk": {
    "why": "Mole.cs RPC_emotion (:45917): emo_chat (:46382) plays the talk clip (:46675) with Voices/chat + Random.Range(1, 4) = chat1-3 (:46201-46207; the Mole picks from three, though the rip has chat1-5); emo_talk (:46375) plays it silent (no Voices/talk): the tile takes the chat's voice",
    "cues": [
      [0, "voice", "chat1|chat2|chat3"]
    ]
  },
  "battle": {
    "why": "Mole.cs RPC_emotion (:45917): emo_battle (:46645-46651): voice battle (:46215, PlayOneShot :46227); RPC_useMount and RPC_useCoin play the clip without it (:50260, :50590): the tile takes the emote's voice",
    "cues": [
      [0, "voice", "battle"]
    ]
  },
  "pose": {
    "why": "Mole.cs RPC_emotion (:45917): emo_pose's voice Voices/pose (:46215, PlayOneShot :46227; in the rip) at 0, before the clip is chosen by the worn set (:46389-46635): pose with no full set (:46635); the mission's RPC_activateIcon1 loops this clip with activate1 instead (:51782, :51837; no tile, Penguin decision 19)",
    "cues": [
      [0, "voice", "pose"]
    ]
  },
  "pose5": {
    "why": "Mole.cs RPC_emotion (:45917): emo_pose's voice pose at 0 (:46215, PlayOneShot :46227), then pose5 with w_mol5 + a_mol5 + c_mol5 worn (:46393-46411)",
    "cues": [
      [0, "voice", "pose"]
    ]
  },
  "pose15": {
    "why": "Mole.cs RPC_emotion (:45917): emo_pose's voice pose at 0 (:46215, PlayOneShot :46227), then pose15 with a_mol15 + c_mol15 worn (no weapon test, :46420-46432)",
    "cues": [
      [0, "voice", "pose"]
    ]
  },
  "pose25": {
    "why": "Mole.cs RPC_emotion (:45917): emo_pose's voice pose at 0 (:46215, PlayOneShot :46227), then pose25 with w_mol25 + a_mol25 + c_mol25 (:46440-46458)",
    "cues": [
      [0, "voice", "pose"]
    ]
  },
  "pose35": {
    "why": "Mole.cs RPC_emotion (:45917): emo_pose's voice pose at 0 (:46215, PlayOneShot :46227), then pose35 with the 35 set (:46467-46485)",
    "cues": [
      [0, "voice", "pose"]
    ]
  },
  "pose45": {
    "why": "Mole.cs RPC_emotion (:45917): emo_pose's voice pose at 0 (:46215, PlayOneShot :46227), then pose45 with the 45 set (:46494-46512)",
    "cues": [
      [0, "voice", "pose"]
    ]
  },
  "pose46": {
    "why": "Mole.cs RPC_emotion (:45917): emo_pose's voice pose at 0 (:46215, PlayOneShot :46227), then pose46 with w_mol46 + c_all46 (:46575-46587)",
    "cues": [
      [0, "voice", "pose"]
    ]
  },
  "pose58": {
    "why": "Mole.cs RPC_emotion (:45917): emo_pose's voice pose at 0 (:46215, PlayOneShot :46227), then pose58 with w_mol58 + a_all58 + c_all58 (:46521-46539)",
    "cues": [
      [0, "voice", "pose"]
    ]
  },
  "pose65": {
    "why": "Mole.cs RPC_emotion (:45917): emo_pose's voice pose at 0 (:46215, PlayOneShot :46227), then pose65 with the 65 set (:46548-46566)",
    "cues": [
      [0, "voice", "pose"]
    ]
  },
  "pose66": {
    "why": "Mole.cs RPC_emotion (:45917): emo_pose's voice pose at 0 (:46215, PlayOneShot :46227), then pose66 with w_mol66 + c_all66 (:46615-46627)",
    "cues": [
      [0, "voice", "pose"]
    ]
  },
  "ko": {
    "why": "Mole.cs RPC_ko (:52008): clip (animation.Play :52222) and voice ko1 or ko2 at 0 (Random.Range(0, 2) :52257, loads :52267 / :52298, PlayOneShot :52337 / :52340), getUp after 3 s (Yield(2, 3) :52347, :52124), standby 1 s later, no effect; RPC_dead (:52387) plays the same clip (Rewind + Play :52581-52584) with dead1 or dead2 at 0 (Random.Range(0, 2) :52619, :52631-52674) and always puts deadEffect at the hero's position and rotation (IL_408 :52687, reached by every voice path; the Mole prefab's deadEffect field = heroes/mole/effects/deadEffect, sharedassets8 #371, field_keys.txt; EffectControl life 3): one of the two at random, even chance (the Sheep's decision 11, as wolf.json / penguin.json / cat.json: roll dead, its voices with it; '!dead' = RPC_ko's)",
    "cues": [
      [0, "voice", "ko1|ko2", {"p": 0.5, "roll": "!dead"}],
      [0, "voice", "dead1|dead2", {"p": 0.5, "roll": "dead"}],
      [0, "fx", "deadEffect", {"p": 0.5, "roll": "dead"}]
    ]
  }
```

---
## Parts needed (build stage)

**1. Mole_nAttack**, on nAttack_fire's root (0 serialized bytes). This is Cat_supportFire with 15 m/s and nAttack_hit; one shared ballistic helper could serve both.
- Velocity = TransformDirection(0, 0, 15) at spawn (ctor :28, Awake :53).
- Each 0.02 s step: v.y -= 9.8 × 0.02, then p += v × 0.02; the root turns along v (:88).
- Destroyed when elapsed ≥ life, where life = 10 × rangeMod (:10089; FixedUpdate :72-79).
- When the trigger box's lowest corner reaches y 0: `api.spawn("nAttack_hit", {x, y: 0, d})` with identity rotation (:10105), then "destroy" (:317). The shell's world-space Smoke ellipsoid goes with it.
- Option `firePoint: "R"`: start at the worn main-hand prop's "firePoint" node world position, when the prop has one (:20401-20417).
- Option `to: [x, y, d]`: re-aim from that start with `trajectoryVector(start, to, 15)` (exported from cat.js).
- The cue's x / y / d / rot remain the fallback.

**2. `tune` (a cue option).** Plays the listed names in order, one per firing of any cue that carries the same list.
- The counter is per class and per tune, kept across plays and tiles. In the game it is the Mole field NJLdLhWCB0 (:19418), reset only for a new hero; reset it on a class change.
- The cue's name lists all three notes so the build makes them.

**3. `hideHero` (a cue kind):** `[t, "hideHero", key, {"kill": s}]`.
- Takes every hero mesh off the camera's layers from t for s seconds, via heroHide (as HeroPropHide does).
- Shows it again at the end, on a new pick, on a class change, or when VFX is turned off.
- The game uses GetComponentsInChildren(Renderer) (:22031), which also hides the weapon's own particles. So the page's WFX weapon effects should hide with the hero.

**4. `rot: "randomYaw"`:** [0, a random integer 0-359, 0], drawn when the clip starts (dig_dirt, :21792).

**5. Optional (Q4): `propAnim`:** `[t, "propAnim", "R", {"clip": "fire"}]`.
- Plays the clip once on the worn prop's Animation, if it has that clip: "fire" at the shot (:20243, :21012).
- "root" at the standby, only if the prop has a root clip (:20514-20520).
- Not used in the entries above.

**6. Inventory:** add the hero-prefab fields to pipeline/wardrobe_fx_inventory.py.
- nAttack_fire needs ProjectileControl (built) and Mole_nAttack.
- nAttack_hit and deadEffect are ready.

**7. index.html**
- The Normal Attack SEQ (Read this first, point 1).
- The Charge Attack and Sky Drill SEQs, with their Thai names and icons (SEQ_SKILL / CLIP_SKILLS).
- If Q3 drops dig2, add `NEVER_PLAYED.mole = ["dig2"]`.

All other cued effects are ready by the inventory and the probe.

## Left out

- Hits on an enemy: the shell's damage and gear procs (Mole_nAttack.cs:282-294), Sky Drill's 1-2 m rings and skyDrill_hit, and Sky Shaker's 5 m hit. None of them reaches the 10 m target (Cat decision 19).
- Camera effects: Sky Drill's blur and shake (Cat decision 43).
- Things that draw nothing in the wardrobe:
  - the Super Dig heal (nothing at full HP);
  - removeLockStatus;
  - the collider and collision changes;
  - the underground movement (the hero stays in place, Penguin decision 8).
- Variants replaced by passives on:
  - the no-Super-Dig variant;
  - skyDrill_ring, replaced by skyShaker_ring.
- The 2 s voice gates and the timeouts (Cat decision 35).

## Open questions (each with my recommended answer)

1. **Where does the shell aim?** With no target the game aims at the 10 m ground point (no lowering, :9555). With an enemy it aims at the enemy's collider.bounds.center (GameGui.cs:1626).
   - **Recommendation: the ground point** (Penguin decision 1, Sheep decision 3). The shell lands 9.83 m ahead after 0.62 s.
   - Aiming 0.6 m up would give rot [-8.214, -1.219, 0] and a landing at 10.69 m, unless an enemy's body stops it first.
2. **Use the worn cannon's firePoint?**
   - **Recommendation: yes, build the `firePoint` / `to` options.** 28 of the 44 cannons move the muzzle.
   - Without them, every shot starts from the code's default point (0.2, 1, 0.6).
3. **Which Charge Attack tiles?**
   - **Recommendation: two tiles**: "Charge Attack: superDig@0.7 dig2*@2.3 root~@0.2" and "Sky Drill: superDig@0.7 dig2*@2.31 skyDrill", with dig2 as the hidden underground step.
   - Alternative A: the full 12 s burrow ending in the auto-surfacing (dig2*@11.3, 56 dig_dirt cues; mostly empty).
   - Alternative B: root* underground. The release's cues would then need another clip, and NEVER_PLAYED gets dig2.
4. **Play the weapon's fire / root clips (`propAnim`)?**
   - **Recommendation: yes, low priority.** It is the game's 0.2 s recoil on every shot.
   - Today the page loops a prop's default clip on its own (index.html:999-1030).
5. **Build the Trumpet's `tune`?**
   - **Recommendation: yes.** Without it the fallback is a random pick of the three notes, and the melody is lost.
6. **Show the mission-only shots?** In town the game fires no shell and plays no cannon sound (:20369).
   - **Recommendation: yes, show them**, following the precedent.

## Offer for the Bible (mole-skill-reference.md; the user decides)

- **Combo timings.**
  - The press windows close at stage 1 + 0.5 / 0.8 / 1.1 / 1.4 s, with no lower bound.
  - The clips start at 0.7 / 1.2 / 1.7 / 2.2 s.
  - The shot comes at 0.3 s in stage 1 and at 0.2 s in later stages.
- **The shell's lob:** getTrajectoryVector at 15 m/s with gravity, about 6.75 deg up from the default muzzle, landing about 9.8 m ahead after 0.62 s.
- **The Trumpet:** it plays Mary Had a Little Lamb one note per shot, starting from the 2nd note. With it, stage 1 drops the cannon sound but stages 2-5 keep it (:20383 vs :21146).
- **The burrow.**
  - The hero is hidden from 0.6 s.
  - The 12 s auto-surfacing never becomes Sky Drill (:21739).
  - Sky Drill's rings come at 0.1 and 0.2 s, with standby at 1.0 s. The reference's "0.8 s / 0.1 s apart" reads otherwise.
  - The reference's dig-in citations :21609 and :22186 are swapped against their formulas.
- **Voices.**
  - The chat voice picks only chat1-3 (:46207).
  - emo_bow, emo_beg and RPC_revive name voices that the Mole's data lacks.
- **dig2** is never played, in BB or TTO.


## Verification (2026-11-13)

A read-only re-trace by the checker. The probes and dumps are in `checks\fx_mole_research\verify\`: the `RPC_*.txt` clip_flow.js dumps, `list_fx.py` -> `list_fx.txt` (the BB container's heroes/mole/effects and the robot prefabs) and `parse_blocks.py` (it parses both reports' blocks against wardrobe_fx_check.py's KINDS / OPTS).

**Checked and confirmed.** I re-added the waits along each flattened state machine and evaluated the opaque predicates on these paths by hand. Each one goes the normal way.
- **Dispatcher:** doNormalAttack windows 0.5 / 0.8 / 1.1 / 1.4 with #101-#104, and RPC_nAttack2(repeat 2-5) (:9601-9798). The stage-1 start is at :9807-9813. The within-3 m aim is :9559-9565. There is no target lowering.
- **Stage 1** (RPC_nAttack1):
  - The clip is a 0.2 s fade (:20611) with voice nAttack1 (:20658, :20704), then Yield 0.3 (:20696).
  - Case 2 (:20214-20486): weapon "fire", then the Trumpet note. The note is played on every client in every mode. The note mapping is 1 do, 2 re, 3 me (:20299-20353). The tune array has 26 entries (:32-58, behind a true predicate). The counter is pre-incremented (:20293), so the report's tune list (starting on re) is right.
  - Next, the cannon sound and the shell, gated by isMine and mGameType > 4 (:20361-20389). The cannon sound is skipped with w_mol25.
  - The shell: fireOffset (0.2, 1, 0.6) or firePoint (:20396-20418), fireDir = tDir - fireOffset (:20423). With w_mol59: ∓0.3 right, rotateH ±9 (:20428-20439; Math.cs:838-843, where +9 turns left).
  - Then Yield 0.4, and standby at 0.7 only while myCommand is nAttack1 (:20529-20551).
- **Stages 2-5** (RPC_nAttack2):
  - The entry sets only actionState and myCommand (:21333-21336), then waits Yield(actionTime - now + 0.5 × repeat - 0.3) (:21352). The clips start at 0.7 / 1.2 / 1.7 / 2.2 s.
  - Rewind plus a cut-in (:20906-20911), then voice nAttack2. Yield 0.2 (:21346).
  - The cannon sound has no w_mol25 test (:21130-21152).
  - Then Yield 0.3 (:21355), and standby only while myCommand is "nAttack" + repeat (:21291-21313).
- **The shell:**
  - Math.getTrajectoryVector (Math.cs:885-1006): every predicate evaluated, and geom.py's formula matches the code, including the y < 0.1 correction. I recomputed the first angle by hand: -1.3599, then -1.4530, giving 6.75 deg up and yaw -1.219.
  - Mole_nAttack: ctor (0, 0, 15), Awake velocity, FixedUpdate LookAt(velocity) and the life. OnTriggerEnter skips the owner's layer and layers 1 / 2. It spawns RPC_nAttack_hit at ClosestPointOnBounds, then Destroy. Mole.cs:10103-10106 is nAttack_hit with identity rotation.
  - The landing times are 0.92 / 1.52 / 2.02 / 2.52 / 3.02 s.
- **Weapons and fire points** (`12tails-video\props\json\mole_weapons.json`): 28 of 44 BB weapons have a firePoint. specialCannon (w_mol59) and trumpet (w_mol25) have none (data/item_map.json:2762, :2801). Mole weapons mount on mount_Hand_R, so the slot "R" is right.
- **Charge Attack** (RPC_cAttack1):
  - Entry IL_1BD8 (:22272-22466): superDig cut in with #411 (:22290-22296), voice superDig on the 2 s gate (:22348-22383), dig_hole 0.05 m up (:22446), dustTimer = now + 0.1.
  - IL_26 (:21608-21690): ends at actionTime + 1 - 0.2 × 2 = 0.6 s; superDig_dust is mission-gated.
  - IL_858 (:22030-22053): renderers off, then Yield(4, 0.1) (:22503).
  - Case 4 (:21533-21561) and IL_1535 (:21694-21880): dig_dirt with random yaw (:21792), auto-surfacing after 4 × 3 = 12 s.
  - The reference's :21609 / :22186 citations are indeed swapped.
- **Release** (doReleaseCharge, :9938-10039): Sky Drill when Sky Drill is learned, more than 3 s have passed and mGameType > 4 (:9987-10018), else RPC_cAttack0 (:10027). expandPos = getExpandPos(position, 1, 0.4) (:9954).
- **RPC_cAttack0:** three dig_dust at the hero (:22828-22838), CrossFade root 0.2 (:22864), standby after 0.2 s (:22877).
- **RPC_skyDrill:**
  - Clip cut in (:31825), voice skyDrill1 / skyDrill2 (:31874-31929), skyDrill with rotation × Euler(270, 90, 0) (:31960), skyShaker_ring with #413 (:31974-31998).
  - The rings come at 0.1 / 0.2 s: Yield(2, 0.1) runs twice, then Yield(3, 0.8), so standby is at 1.0 (:32166-32184). The Bible's "0.8 / 0.1 apart" is indeed wrong.
- **Emotes** (RPC_emotion, :46149-46710): every emote, clip and voice in the table and every line cited is right. chat is Random.Range(1, 4) (:46207). The pose sets are at :46393-46635, and w_mol56 + c_all56 is animation.Stop (:46595-46610).
- **Voices in BB's rip** (`attacks_emotes\rip_audio.txt`): the rip has no bow, beg, sit, talk, dance or revive.
- **KO:** RPC_ko (:52222, :52257, :52347, :52124). RPC_dead: Rewind + ko (:52581-52584), dead1 / dead2 (:52619-52674), and deadEffect at IL_408 (:52687), reached by every voice path, the pvoice-off path too (:52590-52612).
- **Other lines:**
  - dig2 is named only by the loader (:709), never by BB's code or TTO's pseudo/Mole.c (0 hits).
  - The TTO coroutine lines :16954 / :17536 / :6605 / :6373 / :20147 are the named MoveNext headers.
  - battle's other players are at :50260 and :50590.
  - activateIcon1 is :51782 / :51837, with activate2 at :19176.
- **Prefabs** (probe_summary.txt): nAttack_fire (ProjectileControl + Mole_nAttack, no AudioSource), nAttack_hit (life 1, sounds/nAttack_hit), deadEffect, dig_hole (its digSound child, EC 2, looping dig), dig_dirt, dig_dust, superDig_dust, skyDrill (life 0.55, followState). nAttack_fire, nAttack_hit and deadEffect are indeed absent from plans/fx_inventory.md "### mole".
- **The block:** it parses. Every time list is in order, and every key is a Mole clip in data/mole/clips.json (or a sequence key).

**Corrections:**
1. **superDig's hiding cue uses a kind the page and the check do not have.** `[0.6, "hideHero", "dig", {"kill": 2.4}]` fails wardrobe_fx_check.py (KINDS, pipeline/wardrobe_fx_check.py:179, "bad cue"). The page already hides the whole hero with `[t, "hideProp", "hero", {"kill": s}]`:
   - index.html:5186 (fxDue) and HeroPropHide :4885-4898 (`slot === "hero"` -> heroHide);
   - `wfxHidden` (:4901-4906) also hides the worn weapon's weapon_fx particles, as the game's GetComponentsInChildren(Renderer) does (:22031);
   - the check knows it: HIDE_TARGETS, wardrobe_fx_check.py:181; the Chameleon's Thunder Dragon uses it.

   The cue becomes `[0.6, "hideProp", "hero", {"kill": 2.4}]`, and Parts item 3 (`hideHero`) is dropped: nothing to build. HeroPropHide is not an Fx with a cut, so a step change leaves it alone, and the hero shows at 3.0 s.
2. **Parts: the check's option list.** The new options `tune` (the trumpet cues) and `firePoint` (the shell cues) must be added to wardrobe_fx_check.py's OPTS (:171-174), or the check fails those cues as "bad cue". `rot: "randomYaw"` is a value, not an option, so OPTS needs nothing for it, but cueOf (index.html:4629-4632) must learn it beside "random".
3. **Read this first 1's open check is already answered.** A SEQ may repeat a clip:
   - startStep takes a twin action when the step's clip is the playing one (index.html:1459), and calls fxStart for every step (:1469);
   - the Chameleon's Venom Phantom repeats venomPhantom2 five times (index.html SEQ.chameleon).

   With no fade mark, a later step cuts in (`startStep(n, ... st.fade)`, the fade 0), as the game's Rewind + PlayAnimation(nAttack2, 0) does.
4. **Overlaps with the other Mole reports.** The editor keeps one entry per key:
   - `superDig`: skills_b.md:521-529 has the same voice / dig_hole / dust cues but no hiding. skills_b's own Q5 (:607-609) hands the underground phase to this report. Use this report's entry, with correction 1. Since the Charge Attack and Sky Drill SEQs play superDig, its single tile is hidden (index.html:3593), so skills_b's "keep the hero visible" tile does not arise.
   - `skyDrill`: skills_b.md:513-518 is the same, plus a harmless `"cut": 1.0` (life 0.55). Either entry will do.
   - `dig2`: skills_a.md ("dig2" and Q7) proposes `NEVER_PLAYED.mole = ["dig2"]` and no cues. That fits this report's SEQs: a clip a SEQ plays is hidden anyway (index.html:3593), so the NEVER_PLAYED entry is redundant but harmless. This report's `dig2` entry (the hidden burrow's dig_dirt) stays.
5. **Citations.**
   - "plans/fx_mole/effect_only.body.md:53" does not exist. The line meant is plans/fx_mole/effect_only.md:103 (Sky Drill "on its release ... in those skills' cues").
   - The child-EffectControl handling cited as index.html ":4068, :4135" is at index.html:4199-4200.

**Not a correction, for the editor:** the frame-loop timers fire strictly after their time (`dustTimer >= Time.time` -> wait, :21645; `digTime + 0.2 < Time.time`, :21758).
- At 60 fps, superDig_dust would fall at 0.117 / 0.333 / 0.55 s and dig_dirt every 0.217 s (10 mounds, not 11, before 3.0 s).
- The report uses the nominal 0.1 / 0.3 / 0.5 and 0.2 s. skills_a.md's King Kaiser dust uses the 60 fps model (0.117 s).
- Both depend on the frame rate. Pick one model for the class.

**Corrected paste-ready entries.** Only `superDig` changes. Every other entry in the block above stands as written.

```json
  "superDig": {
    "why": "Mole.cs RPC_cAttack1 (:21411-22513), Charge Attack 3 (#113, digTimeOut 4 x 3 = 12 s :21553), Speed Drill 2 (#312), Super Dig #411 on (passives rule): at 0 the clip superDig cut in (PlayAnimation(superDig, 0) :22290-22296; dig1 without #411 :22304), the voice superDig (#411 :22359-22383; cAttack without it :22402-22414; at most every 2 s :22348), dig_hole 0.05 m up with the hero's rotation (:22446; EffectControl life 5, its digSound child plays the looping Sounds/dig for 2 s); the dig-in (IL_26 :21608-21690) until actionTime + 1 - 0.2 x 2 = 0.6 s (:21609): superDig_dust at the hero with its rotation every 0.2 s from 0.1 s (dustTimer :22466, :21645-21676; mission / arena only, mGameType > 4 :21637, kept as the Sheep / Penguin precedent) = 0.1, 0.3, 0.5 s; at 0.6 s every renderer of the hero off (IL_858 :22031-22053) until the release, when the loop sees myCommand change (:21934-21951): the page's whole-hero hiding (hideProp hero, HeroPropHide: the hero, its props and their weapon_fx particles, as GetComponentsInChildren(Renderer) :22031) from 0.6 to 3.0 s (the release at 3.0 s in the Charge Attack tile, 3.01 s in Sky Drill's); then Yield(4, 0.1) (:22503) to the underground loop at 0.7 s (case 4 :21533-21561), the dig2 step",
    "cues": [
      [0, "voice", "superDig"],
      [0, "fx", "dig_hole", {"y": 0.05}],
      [0.1, "fx", "superDig_dust"],
      [0.3, "fx", "superDig_dust"],
      [0.5, "fx", "superDig_dust"],
      [0.6, "hideProp", "hero", {"kill": 2.4}]
    ]
  },
```

**Parts list after these corrections:** Mole_nAttack (with `firePoint` and `to`), `tune`, `rot: "randomYaw"`, the optional `propAnim`, OPTS += tune and firePoint, and the inventory's three hero-prefab fields. `hideHero` is dropped.
