Short summary: The Whale's Normal Attack is three clips. Each one is cut in at a fixed time after stage 1: nAttack2 at 0.8 s and nAttack3 at 1.8 s. Each stage has a voice, one or two hero-played swing sounds (`sounds/nAttack1-3`) and, with the Entended Wave passive (#401, passives on), an `extendedWave1-3` burst at the hero. Every swing hit lands inside a 4 m (7 m) box, so nothing reaches the 10 m target. The Charge Attack is the shield stance: cAttack1 for 0.7 s, then cAttack2 looped. It ends in one of three releases: RPC_cAttack0 under 1 s, the plain RPC_cAttack2 (a crossfade to root) from 1 to 3 s, and from 3 s, with the Shield Bash passive (#114), RPC_shieldBash on the shieldBash clip with `shieldBash_ring` at 0.2 s. Knight of the Deep (#273, a passive) adds the Round Table to the charge, but only while the 12th Kingdom Knight's knights are out. It brings a sound, a voice, `roundTable_ring` cut at the release, and the knights turning on guard. I give it its own tile, which needs the knights from the skills report's part. Emotes follow the usual pattern with the Whale's own voices (beg, bow and battle are voiced; laugh, sit, talk, pose and dance are not). KO is the Wolf's entry, getUp is the Cat's, and run has two `step_heavy1` footsteps. There are 18 cue entries with 30 cues, and no new effect part: every cued effect is ready.

=====================================================================
# Whale effects + sounds research: Normal Attack, Charge Attack (and its releases), emotes, basic moves, KO

**Scope.**
- Clips nAttack1, nAttack2 and nAttack3: RPC_nAttack1-3 and the dispatcher doNormalAttack.
- The Charge Attack:
  - RPC_cAttack1 on cAttack1 / cAttack2, with doBeginCharge and doReleaseCharge;
  - the releases RPC_cAttack0, RPC_cAttack2 and (Shield Bash #114) RPC_shieldBash on the shieldBash clip;
  - Knight of the Deep #273's RPC_roundTable inside the charge.
- MP / SP transfer skills on an attack clip: the Whale has none.
- RPC_emotion, the basic moves, RPC_ko, RPC_dead, RPC_revive, RPC_activateIcon1 and the run footsteps.
- The TTO-only emote clips.

**Method.** Research only (recipe steps 1-3), office PC, 2026-11-13.
- Line numbers are C:\Users\Jump\Desktop\12tails\DecompiledSource\Whale.cs (= D:\12tails\... at home) unless another file is named.
- Times are seconds from the start of the clip the cue is keyed by. Distance 0 means at the hero.
- Every opaque predicate on these paths was evaluated by script: `pred.py` prints a line range with each `if (a - b op c)` replaced by PRED[T] / PRED[F]. I then read each path by hand, and each one goes the normal way. A PRED[F] guards a junk `continue`, and a PRED[T] guards the real goto.

**Files** (all in checks\fx_whale_research\attacks_emotes\, git-ignored):
- `RPC_*.txt`: clip_flow.js dumps of RPC_nAttack1-3, RPC_cAttack1, RPC_cAttack2, RPC_cAttack0, RPC_shieldBash, RPC_roundTable, RPC_emotion, RPC_ko, RPC_dead, RPC_revive and RPC_activateIcon1.
- `n1_body.txt`, `c1.txt`, `sb.txt`, `rt.txt`, `emo.txt`: the predicate-annotated bodies.
- `clip_calls.txt`: `node pipeline/clip_calls.js .../DecompiledSource wardrobe/data whale`.
- `probe.txt`, `probe_summary.txt`: `wardrobe_fx.py whale --probe extendedWave1,extendedWave2,extendedWave3,shieldBash_ring,roundTable_ring,deadEffect,nAttack_hit,shieldBash_hit,wallPuncture_hit,shield` (read only), plus summ.py.
- `probe_fields.py` / `probe_fields.txt`: the Whale MonoBehaviour's serialized fields on the hero prefab. `footStep_left` and `footStep_right` are both the AudioClip `step_heavy1`, and `Whale_shield_hit` is the effect `shield`.
- `probe_events.py` / `probe_events.txt`: AnimationEvents on all 51 Whale clips. Only `run` has any: playLeftFootEvent at 0.1 s and playRightFootEvent at 0.6 s.
- `container_audio.py` / `container_audio.txt`: BB's ResourceManager keys under heroes/whale/voices/ (114) and sounds/ (40), and `sound/fx/step_heavy1`.
- `cues.json`: every entry below, as one JSON object.

**TTO.** TTO1102 `pseudo/Whale.c` keeps the same strings in the same coroutines:
- `<RPC_nAttack1>d__153` :12261, `<RPC_nAttack2>d__154` :13041 and `<RPC_nAttack3>d__155` :14155 (extendedWave1-3, sounds/ and voices/nAttack1-3);
- `<RPC_cAttack1>d__159` :2932 (roundTable voice and sound, cAttack1 voice);
- `<RPC_cAttack2>d__160` :3349, `<RPC_cAttack0>d__161` :2793;
- `<RPC_shieldBash>d__162` :18325 (shieldBash_ring, shieldBash1 / 2);
- `<RPC_roundTable>d__192` :17500.

Its waits are opaque, so the BB times stand (as the Mole's). One TTO difference: TTO's Round Table loads **sounds/**roundTable1 / roundTable2 where BB loads the missing Voices/ ones (Question 3). TTO moved the emotes and KO into BaseHero (pseudo/BaseHero.c `<RPC_emotion>` :1900, `<RPC_ko>` :2391, `<RPC_dead>` :1217, `<RPC_revive>` :3940). Its emotion adds emo_clap / emo_wai and the like, with the voice `GameAssets/Characters/Heroes/<cls>/Voices/<name>`. The Whale has no clap or wai voice in any data I can read. In this scope, only the emote clips are TTO-only.

---
## Read this first

**1. Normal Attack's SEQ needs its times (index.html work).**
- Today index.html:1369 has `"Normal Attack: nAttack1 nAttack2 nAttack3"`, which plays three whole clips (1.0 + 1.0 + 0.9 s).
- In the game, only stage 1 sets actionTime (:16509). Stage 2 waits `Yield(2, actionTime - Time.time + 0.8)` (:17775) and stage 3 waits `+ 1.8` (:18589). Stage 1's standby (:16471-16476) is the only other actionTime write, and it is skipped once myCommand has moved on (:16461), as is stage 2's (:17715).
- The clips therefore start at **0.8 s** and **1.8 s**. That matches the Bible's own combo table (whale-skill-reference.md "Normal attack combo": stage 2 at 0.8, stage 3 at 1.8).
- Every stage cuts in: PlayAnimation(x, 0) at :16524, :16808, :18007. The first step keeps the page's 0.2 s fade (Bat decision 28 and the Sheep / Penguin / Mole).
- **Proposed: `"Normal Attack: nAttack1@0.8 nAttack2@1.0 nAttack3"`** (2.7 s). nAttack2's @1.0 equals its own clip length, written out for clarity.

**2. The Charge Attack has three releases; I propose two tiles plus Knight of the Deep's (Question 1, Question 2).**
- doReleaseCharge (:8486-8643), while attack / cAttack1:
  - before 1 s: RPC_cAttack0 (:8618);
  - from 1 s: RPC_cAttack2 (:8597);
  - from 3 s (`actionTime + 3 <= Time.time` :8557), with Shield Bash #114 (:8545) and mGameType > 4 (:8569): RPC_shieldBash(…, 1) (:8575).
- Both RPC_cAttack0 and RPC_cAttack2 are a CrossFade to root with standby 0.2 s later, and neither draws anything.
- Today: `"Charge Attack: cAttack1 cAttack2*"` (cAttack2 shown for about 1.5 s, a plain lowering).
- Proposed, mirroring the Mole's decisions 2-3 (Charge Attack at 3.0 s plain, Sky Drill at 3.01 s). Here the test is `<=`, so the boundary sits on the other side:
  - `"Charge Attack: cAttack1 cAttack2*@2.29 root~@0.2"`: released at 2.99 s, the plain RPC_cAttack2 (root 0.2 crossfade :19416, standby 0.2 s later :19425);
  - `"Shield Bash: cAttack1 cAttack2*@2.3 shieldBash~"`: released at 3.0 s, the passive's own tile (Shield Bash #114 has its Bible card and icon, `icons/hd/whale/shieldBash.webp`; one tile per skill). Its clip fades in over 0.2 s (:20040) and lasts 0.8 s, with standby at 0.6 s;
  - `"Knight of the Deep: cAttack1 cAttack2*@2.3 shieldBash~"`: the same hold with the knights out (item 3).
- cAttack1 → cAttack2 at 0.7 s (Yield(2, 0.7) :19214, PlayAnimation(cAttack2, 0) :18827, a cut). This is the clip's own 0.7 s, so cAttack1 carries no @.
- The shieldBash single tile disappears, since a clip used by a visible sequence leaves the list. Its cues stay keyed `shieldBash`.

**3. Knight of the Deep (#273) acts only inside the charge, and only with the knights out.**
- With the kingdomKnight status on (12th Kingdom Knight rank 2: six kingdomKnight2, Whale.cs:28414-28511), a charge does three things:
  - at 0: Sounds/roundTable1 (:19024), and **Voices/roundTable** in place of cAttack1 / cAttack2 (:19199);
  - at 0.7 s: RPC_roundTable (:18855). It puts `roundTable_ring` at the hero (:29263): followPosition / followState, life 999, its own looping Sounds/roundTable2. Then a 4 m pulse every 0.5 s, enemies only (:29412).
  - The knights guard from the press (whale_kingdomKnight.cs:202-220, knightGuard :550-760): every 0.5 s a random flat facing (:682), their own `cAttack` clip looped (:687), and back to `root` at the release (:700-710).
- The tile needs the knights standing, which is the skills report's whale_kingdomKnight part (the inventory's "kingdomKnight2: needs whale_kingdomKnight"). The cues below hold what this scope can fix; the knights' cue is drafted in "Parts needed" 2 against that part.
- This follows the Chameleon's Clear Arrow (decision 13): a passive with a precondition gets its own tile, with the precondition's look.

**4. Hero-played sounds (`"sound"` cues), from audio.PlayOneShot in the hero's own code.**
- The swings: sounds/nAttack1 at 0.5 s (:16117), sounds/nAttack2 at 0.2 and 0.5 s (:16914, :17376), sounds/nAttack3 at 0.3 s (:18169). They play on every client in every mode, at volume 1 with no volume argument.
- Knight of the Deep: sounds/roundTable1 (:19024).
- run: footStep_left and footStep_right are **both** `step_heavy1` (probe_fields.txt; Resources/sound/fx/, which the Bison already builds from).
- The effects that bring their own sound are `shieldBash_ring` (shieldBash_ring) and `roundTable_ring` (roundTable2, looped).
- Name collisions (the cue kind picks the folder; voices are saved as v_<name>): nAttack1-3, cAttack1 and cAttack2 are both voices/ files and clip names (nAttack1-3 are sounds/ files too); `roundTable` is a voice while `roundTable1` / `roundTable2` are sounds only; `shield` is a voice, a sound and an effect.

**5. Emote voices** (container_audio.txt).
- BB's Whale has hi, wave, ty, bow, beg, cheer, cry, sleep, battle, chat1-5, ko1-2, dead1-2 and revive.
- It has no laugh, sit, talk, pose or dance voice, so those tiles and every pose<n> stay silent.
- chat draws Random.Range(1, 6) = chat1-5 (:40133), all present.

**6. Mission-only gates are kept** (the Sheep / Penguin / Wolf / Mole precedent):
- gated: extendedWave1-3 (mGameType > 4 :16542, :16836, :18033) and Shield Bash (:8569);
- not gated: the swing sounds, the voices (own hero or a mission teammate), shieldBash_ring once the bash runs, the footsteps (own hero), and the Round Table ring.

**7. No MP / SP transfer style skill plays an attack clip.** clip_calls.txt: nAttack1-3 only in RPC_nAttack1-3 (:16524, :16808, :18007); cAttack1 / cAttack2 only in RPC_cAttack1 (:18988, :18827); shieldBash only in RPC_shieldBash (:20040).

---
## The dispatchers

**doNormalAttack** (:8017-8265, own hero):
- Game code 967 swaps the attack for useItem("f_wtb1") (:8031-8049), an event mode outside the scope.
- The aim is flat: vFlat(target - position).normalized (:8058-8061). The hero turns to it, and there is no projectile.
- Stage 1: from standby or run, when the nAttack timeout is free (:8234), RPC_nAttack1 (:8240).
- Later stages, while attacking:

| myCommand | needs | press window (from stage 1) | starts | lines |
|---|---|---|---|---|
| "nAttack1" | #101 | after 0.3, before 0.8 | RPC_nAttack2 at 0.8 | :8124-8156 |
| "nAttack2" | #102 | after 1.0 (no upper bound; stage 2's standby at 1.6 ends it) | RPC_nAttack3 at 1.8 | :8186-8212 |

**doBeginCharge** (:8376-8482) starts RPC_cAttack1 (:8457) when:
- the hero is in standby or run (:8410-8419);
- #111 is learned (:8425);
- there is no `noShield` status (:8432, "Whale has no shield!");
- the cAttack timeout is free (:8445);
- **at least 1 s** has passed since the last action (:8451).

**doReleaseCharge** (:8486-8643): Read this first 2.

## nAttack1 (stage 1): coroutine $RPC_nAttack1$28459 (:15863-16690)

| t (s) | what happens | lines |
|---|---|---|
| 0 | attack, actionTime, myCommand nAttack1, addTimeOut(nAttack, 1.5), turn to aim, clip cut in, Once, moveSpeed 0 | :16506-16533 |
| 0 | #401 + mission: extendedWave1 at the hero's position and rotation | :16536-16564 |
| 0.2 | if still attacking: voice nAttack1 (own hero or a mission teammate) | :15991-16061, :16606; Yield(2, 0.2) :16616 |
| 0.3 | moveSpeed 4 | :16075; Yield(3, 0.1) :16597 |
| 0.5 | moveSpeed 0; Sounds/nAttack1 (all clients); own hero: Star Spear test, box FindRecTarget(1.5, 1.5, 4 + 3, 2), wall-puncture roll or hit(99) → RPC_nAttack_hit / RPC_wallPuncture_hit at the enemy | :16094-16444; Yield(4, 0.2) :16604 |
| 0.7 | standby, unless stage 2 was pressed | :16452-16491; Yield(5, 0.2) :16613 |

## nAttack2 (stage 2, two swings): coroutine $RPC_nAttack2$28481 (:16691-17813)

| t (s) | what happens | lines |
|---|---|---|
| press | attack, myCommand nAttack2; waits until stage 1 + 0.8 | :17760-17775 |
| 0 | if attacking: clip cut in, Once, moveSpeed 0, addTimeOut; #401 + mission: extendedWave2 | :16797-16878 |
| 0.2 | moveSpeed 4; Sounds/nAttack2; voice nAttack2 | :16880-16988, :17797; Yield(3, 0.2) :17803 |
| 0.4 | moveSpeed 0; swing 1's hit (own hero) | :16990-17339; Yield(4, 0.2) :17777 |
| 0.5 | moveSpeed 4; Sounds/nAttack2 | :17342-17391; Yield(5, 0.1) :17781 |
| 0.7 | moveSpeed 0; swing 2's hit | :17394-17703; Yield(6, 0.2) :17785 |
| 0.8 | standby, unless stage 3 was pressed | :17706-17750; Yield(7, 0.1) :17811 |

## nAttack3 (stage 3): coroutine $RPC_nAttack3$28503 (:17890-18603)

| t (s) | what happens | lines |
|---|---|---|
| press | attack, myCommand nAttack3; waits until stage 1 + 1.8 | :18571-18589 |
| 0 | clip cut in, Once, moveSpeed 0, addTimeOut; #401 + mission: extendedWave3; voice nAttack3 | :17996-18133, :18584 |
| 0.3 | moveSpeed 4; Sounds/nAttack3 | :18135-18185; Yield(3, 0.3) :18596 |
| 0.5 | moveSpeed 0; the hit (half-width 2) | :18187-18514; Yield(4, 0.2) :18598 |
| 0.7 | standby | :18517-18561; Yield(5, 0.2) :18594 |

**Prefabs** (probe_summary.txt), all ready by the inventory:
- extendedWave1: EffectControl life 1, no follow. A RingEmitter (Line_vertMultilines5) at (0.6, 0.7, 4) and two Dust1 LineEmitters at (-0.4 / 1.0, 0.2, 4), each after Delay 0.5.
- extendedWave2: two RingEmitters at (0.3, 0.6 / 0.5, 4), after Delay 0.3 and 0.5.
- extendedWave3: a tideCutter LineEmitter at (0, 1, 3) after Delay 0.4, and two dust LineEmitters after 0.5.

Their delays fall on the stage's hits (0.5; 0.4 / 0.7; 0.5), with the burst at the far end of the 7 m box. The game spawns each one where the hero stands after the earlier stages' steps (0.8 m each). The page has no hero mover, so every one spawns at the start point (Penguin decision 8).

## Charge Attack: cAttack1, cAttack2 (the shield stance)

Coroutine $RPC_cAttack1$28521 (:18669-19247), from its entry IL_CE9 (:18966):

| t (s) | what happens | lines |
|---|---|---|
| 0 | attack, actionTime, myCommand cAttack1, vMovement 0, addTimeOut(cAttack, 1), turn to aim, cAttack1 cut in, Once | :18967-18991 |
| 0 | kingdomKnight status + #273: Sounds/roundTable1 (all clients) | :18994-19037 |
| 0 | voice (own hero or a mission teammate, at most once a second): with kingdomKnight + #273 Voices/roundTable, else cAttack1 or cAttack2 at random | :19040-19212 |
| 0.7 | sLv = 1 + #112 + #113 = 3; still attack / cAttack1: cAttack2 cut in, Loop; own hero: RPC_AddStatus(shield, 3, 1200); #273: RPC_roundTable; SP timer | case 2 :18785-18868; Yield(2, 0.7) :19214 |
| every frame | SP - 1 each second; at SP 0 the own hero releases with RPC_cAttack2 | :18878-18946, YieldDefault(3) :19204 |
| release | once myCommand is not cAttack1: RemoveStatus(shield), end | :18884, :18948-18960 |

**The `shield` status draws nothing.** CharacterControl.cs names it only at :4415 (the Auto Shield skip), :12289 (Whale-only) and :30855 (the damage cut). There is no look branch for it.

**Releases:**
- **RPC_cAttack0** (:19450-19626; under 1 s): myCommand cAttack0 (:19604), PlayAnimation("root", 0.2) (:19613), standby 0.2 s later (:19624, :19568). No tile, no cue.
- **RPC_cAttack2** (:19248-19447; 1-3 s, or the SP-0 auto release): myCommand cAttack2 (:19410), PlayAnimation("root", 0.2) (:19416), standby after 0.2 s (:19425, :19355). This is the Charge Attack tile's `root~@0.2` step, and it needs no cue.
- **RPC_shieldBash** (:19653-20180; 3 s or more with #114, mission):

| t (s) | what happens | lines |
|---|---|---|
| 0 | attack, actionTime, myCommand shieldBash, turn, shieldBash with a 0.2 s fade, Once, moveSpeed 0 | :20025-20050 |
| 0 | voice shieldBash1 or shieldBash2 | :20052-20171 |
| 0.2 | moveSpeed 2; shieldBash_ring at the hero's position and rotation; own hero: FindAreaTarget(3, 3), hit(221, DEF, KO 10), RPC_shieldBash_hit on each enemy hit | :19781-19932; Yield(2, 0.2) :20176 |
| 0.4 | moveSpeed 0 | :19933-19958; Yield(3, 0.2) :20174 |
| 0.6 | standby | :19960-20017; Yield(4, 0.2) :20161 |

- shieldBash_ring (probe): EffectControl life 1, an AudioSource playing shieldBash_ring, a Smoke1 ellipsoid and a Dust5 RingEmitter 0.2 m up. Ready.

**RPC_roundTable** ($RPC_roundTable$28794 :29121-29480), started at the charge's 0.7 s with #273:
- If the knights list is empty or null, nothing happens (:29227-29242).
- Otherwise roundTable_ring at the hero (:29251-29263).
- Then the voice: Random.Range(0, 2) (:29308) picks Voices/roundTable1 or roundTable2 (:29320, :29352). Neither is in BB's data ("Cannot find roundTable1 voice" :29336), so the voice is silent.
- Then Yield(2, 0.5) (:29474). While attack / cAttack1, each 0.5 s comes the pulse FindAreaTarget(pos, 4, 3) (:29412) with hit(276) (:29434) and SP - 1 (:29450), then Yield(3, 0.5) (:29478).
- roundTable_ring (probe): life 999, afterLife 1, followPosition, followState, a repeating WaterWave2 RingEmitter, and an AudioSource looping roundTable2. Ready.
  - followState ends it when the action changes (EffectControl.cs:226-232, per the Chameleon verification), so at the release, 2.3 s into cAttack2: `cut 2.3`.

---
## Emotes and basic moves

**RPC_emotion** ($RPC_emotion$29040, :39843-40665):
- The voice plays at 0, **before** the clip (IL_6C4 :40074-40153). Its gates:
  - the voice option (:40075);
  - more than 2 s since the last action (:40081);
  - own hero, game code 31 or a mission teammate (:40087-40109).
- emo_chat loads `Voices/chat` + Random.Range(1, 6) (:40133). Every other emo_<name> loads `Voices/<name>` (:40141), played only if it loads (:40147-40153).
- Then actionState "emotion" (:40168) and the clip with a 0.2 s fade. There are no effects and no Sounds/.
- wave, bow and laugh play Once with standby at 1.2 s (IL_D66 :40636, Yield(4, 1.2) :40660). The rest loop (IL_DD4 :40608) until the player moves (:40046-40072).

| emote | clip | voice | lines |
|---|---|---|---|
| hi, wave | wave | hi / wave | :40189, :40196 → :40630 |
| ty, bow | bow | ty / bow | :40205, :40212 → :40623 |
| laugh | laugh | (none) | :40219-40225 |
| sit | sit | (none) | :40239-40245 |
| sleep | sleep | sleep | :40251-40257 |
| cheer | cheer | cheer | :40263-40269 |
| beg | beg | beg | :40275-40281 |
| cry | cry | cry | :40287-40293 |
| talk, chat | talk | (none) / chat1-5 | :40301, :40308 → :40601 |
| pose | by worn set | (none) | :40315-40561 |
| battle | battle | battle | :40571-40577 |
| dance | dance | (none) | :40586-40594 |

emo_pose picks the clip by the worn set:
- pose5: w_whl5 + a_whl5 + c_whl5;
- pose15: a_whl15 + c_whl15, with **a 0.5 s fade** (:40358);
- pose25 / 35 / 45 / 65: the full w + a + c set;
- pose58: w_whl58 + a_all58 + c_all58;
- pose46: w_whl46 + c_all46;
- a frozen pose (animation.Stop :40533): w_whl56 + c_all56;
- pose66: w_whl66 + c_all66;
- else pose (:40561).

All of them are silent. pose15's 0.5 s fade is a move-table matter (the emote tab), not a cue.

**TTO-only emote clips** (clap, cooking, fishingWhale, mining, planting, pose37, wai) stay silent (Bat decision 36). TTO's BaseHero emotion would load Voices/clap or Voices/wai, and the Whale has neither. Only clap and wai are released for the whale.

**Basic moves:**
- run: the footsteps (Read this first 4; Whale.cs:113-167, own hero or anyone in a mission).
- falling and root: nothing (PlayerControl plays them silently, and no other clip has an AnimationEvent).
- battle: the emote's voice.

**RPC_activateIcon1** (:45525-45739): the mission channel. It loops `battle` (:45613) with Voices/activate1 (:45660-45672). No tile (Penguin decision 19).

**KO:**
- RPC_ko ($RPC_ko$29209 :45778-46154): PlayAnimation(ko, 0.2) (:45992) and ko1 or ko2 (:46027-46119). getUp comes after 3 s (:46115, :45894), then standby 1 s later.
- RPC_dead ($RPC_dead$29216 :46155-46510): Rewind + ko cut in (:46349-46352), and dead1 or dead2 (:46387-46442). It **always** puts deadEffect at the hero's position and rotation (IL_7B4 :46454-46471): a Resources.Load, not a prefab field, reached by the voice-off and town paths too.
- deadEffect (probe): life 3, the `whale_dead` ImageEmitter 2.4 m up after Delay 0.4. Ready.

**getUp:**
- RPC_revive (:46540-46812) plays getUp (:46734) with Voices/revive (:46775, :46808), which BB's data has.
- RPC_ko's getUp is silent.
- So the entry is the Cat's: revive on half the plays.

---
## Paste-ready cue entries for wardrobe/fx_cues/whale.json (identical to checks\fx_whale_research\attacks_emotes\cues.json)

The file is `{}` today. 18 entries, 30 cues: 6 fx, 7 sound, 17 voice.

```json
  "nAttack1": {
    "why": "Whale.cs RPC_nAttack1 (:15863-16690), Combo stage 1 (doNormalAttack :8234-8240): at 0 actionState attack, actionTime, myCommand nAttack1, the clip cut in (PlayAnimation(nAttack1, 0) :16524), Once; Entended Wave #401 learned (passives rule, :16536) and a mission / arena (mGameType > 4 :16542, kept as the Sheep / Penguin precedent): extendedWave1 at the hero's position and rotation (load :16554, Instantiate :16564; EffectControl life 1, its RingEmitter and two dust LineEmitters 4 m ahead after Delay 0.5, the 7 m reach's impact); Yield(2, 0.2) (:16616); 0.2 s, still attacking (case 2 :15991-15999): the voice nAttack1 (own hero or a mission teammate :16002-16031, load :16039, PlayOneShot :16606); Yield(3, 0.1) (:16597); 0.3 s: moveSpeed 4 (:16075; the step forward, no hero mover: Penguin decision 8); Yield(4, 0.2) (:16604); 0.5 s: moveSpeed 0, the hero's PlayOneShot of Sounds/nAttack1 on every client in every mode (load :16105, PlayOneShot :16117), then own hero only the hit box FindRecTarget(1.5, 1.5, 4 + 3, 2) (:16444) whose RPC_nAttack_hit / wall puncture land on enemies hit (:16238-16434): none at the 10 m target (Cat decision 19); Yield(5, 0.2) (:16613); standby at 0.7 s (case 5 :16452-16491) unless stage 2 was pressed",
    "cues": [
      [0, "fx", "extendedWave1"],
      [0.2, "voice", "nAttack1"],
      [0.5, "sound", "nAttack1"]
    ]
  },
  "nAttack2": {
    "why": "Whale.cs RPC_nAttack2 (:16691-17813), Combo stage 2 (#101, pressed after stage 1 + 0.3 and before + 0.8, doNormalAttack :8130-8156): the entry sets only actionState and myCommand (:17760-17763), so the clip starts at stage 1 + 0.8 s (Yield(2, actionTime - Time.time + 0.8) :17775; stage 1's standby, the only other actionTime write, is skipped once myCommand is nAttack2, :16461): at 0 the clip cut in (PlayAnimation(nAttack2, 0) :16808), Once; #401 + mission: extendedWave2 at the hero's position and rotation (:16828-16862; life 1, two RingEmitters 4 m ahead after Delay 0.3 and 0.5); Yield(3, 0.2) (:17803); 0.2 s: moveSpeed 4 (:16891), Sounds/nAttack2 on every client (load :16902, PlayOneShot :16914), the voice nAttack2 (own hero or a mission teammate :16928-16958, load :16965, PlayOneShot :17797); Yield(4, 0.2) (:17777); 0.4 s: moveSpeed 0, swing 1's hit (:17001-17334); Yield(5, 0.1) (:17781); 0.5 s: moveSpeed 4 (:17353), Sounds/nAttack2 again (:17364, :17376); Yield(6, 0.2) (:17785); 0.7 s: swing 2's hit (:17405-17698); Yield(7, 0.1) (:17811); standby at 0.8 s (case 7 :17706-17750) unless stage 3 was pressed; the hits reach no target at 10 m",
    "cues": [
      [0, "fx", "extendedWave2"],
      [0.2, "sound", "nAttack2"],
      [0.2, "voice", "nAttack2"],
      [0.5, "sound", "nAttack2"]
    ]
  },
  "nAttack3": {
    "why": "Whale.cs RPC_nAttack3 (:17890-18603), Combo stage 3 (#102, pressed while myCommand is nAttack2 and after stage 1 + 1.0, doNormalAttack :8186-8212): the clip at stage 1 + 1.8 s (Yield(2, actionTime - Time.time + 1.8) :18589; the entry sets only actionState / myCommand :18571-18574): at 0 the clip cut in (PlayAnimation(nAttack3, 0) :18007), Once; #401 + mission: extendedWave3 at the hero's position and rotation (:18027-18057; life 1, the tideCutter LineEmitter 3 m ahead after Delay 0.4, two dust LineEmitters 4 m ahead after 0.5); the voice nAttack3 at 0 (:18073-18131, load :18110, PlayOneShot :18584); Yield(3, 0.3) (:18596); 0.3 s: moveSpeed 4 (:18146), Sounds/nAttack3 on every client (load :18157, PlayOneShot :18169); Yield(4, 0.2) (:18598); 0.5 s: moveSpeed 0, the hit (:18198-18509; no target at 10 m); Yield(5, 0.2) (:18594); standby at 0.7 s (case 5 :18517-18561)",
    "cues": [
      [0, "fx", "extendedWave3"],
      [0, "voice", "nAttack3"],
      [0.3, "sound", "nAttack3"]
    ]
  },
  "cAttack1": {
    "why": "Whale.cs RPC_cAttack1 (:18669-19247; doBeginCharge :8376-8482: standby or run, #111, no noShield, the cAttack timeout free, 1 s since the last action :8451, RPC_cAttack1 :8457): at 0 (IL_CE9 :18966-18991) actionState attack, actionTime, myCommand cAttack1, the clip cut in (PlayAnimation(cAttack1, 0) :18988), Once; the voice (own hero or a mission teammate :19040-19068, at most once a second :19069-19075): with no kingdomKnight status (the plain charge) Random.Range(0, 2) (:19121): Voices/cAttack1 (:19131, PlayOneShot :19209) or Voices/cAttack2 (:19162, PlayOneShot :19212); Yield(2, 0.7) (:19214): the change to the looped cAttack2 at 0.7 s (case 2 :18785-18868: PlayAnimation(cAttack2, 0) :18827, the shield status :18843, which draws nothing: CharacterControl.cs has no look for it, only :4415, :12289, :30855)",
    "cues": [
      [0, "voice", "cAttack1|cAttack2"]
    ]
  },
  "shieldBash": {
    "why": "Whale.cs doReleaseCharge (:8486-8643): released while attack / cAttack1 (:8526-8532), at least 1 s (:8538) and at least 3 s after the press (actionTime + 3 <= Time.time :8557), Shield Bash #114 learned (:8545; passives rule), a mission / arena (mGameType > 4 :8569, kept): RPC_shieldBash(..., 1) (:8575) instead of the plain RPC_cAttack2 (:8597); RPC_shieldBash (:19653-20180): at 0 actionState attack, myCommand shieldBash (ends the charge loop and its shield status, :18884, :18948-18954), PlayAnimation(shieldBash, 0.2) (:20040), Once; the voice (own hero or a mission teammate :20052-20079) Random.Range(0, 2) (:20081): shieldBash1 (:20091, PlayOneShot :20171) or shieldBash2 (:20122, PlayOneShot :20158); Yield(2, 0.2) (:20176); 0.2 s: moveSpeed 2 (:19800), shieldBash_ring created at the hero's position and rotation (load :19811, createEffect :19823; EffectControl life 1, plays its own Sounds/shieldBash_ring, a Smoke1 puff and a Dust5 ring 0.2 m up), then own hero the 3 m FindAreaTarget (:19850) whose shieldBash_hit lands on enemies hit (:19893-19909): none at the 10 m target (Cat decision 19); Yield(3, 0.2) (:20174); 0.4 s moveSpeed 0 (:19952); Yield(4, 0.2) (:20161); standby at 0.6 s (case 4 :19960-20017)",
    "cues": [
      [0, "voice", "shieldBash1|shieldBash2"],
      [0.2, "fx", "shieldBash_ring"]
    ]
  },
  "@KnightoftheDeep:cAttack1": {
    "why": "Whale.cs RPC_cAttack1 (:18669-19247) with Knight of the Deep #273 (passive; WhaleSkill.cs:2748-2752) and the kingdomKnight status on (the 12th Kingdom Knight's knights out, rank 2: 2 + 2 x 2 = 6 kingdomKnight2, Whale.cs:28414-28511): at 0 the hero's PlayOneShot of Sounds/roundTable1 on every client (kingdomKnight :18994, #273 :19000, load :19012, PlayOneShot :19024) and, in place of cAttack1 / cAttack2, Voices/roundTable (:19078-19106, load :19096, PlayOneShot :19199; own hero or a mission teammate, the 1 s gate :19069); the clip as the plain charge's (PlayAnimation(cAttack1, 0) :18988, Yield(2, 0.7) :19214); the knights guard from 0: each knight in its standby sees its owner attack / cAttack1 with #273 (whale_kingdomKnight.cs:202-220) and starts knightGuard (:260, coroutine :550-760): every 0.5 s (Yield(3, 0.5) :756) a random flat facing (LookRotation(vFlat(Random.onUnitSphere)) :682) and its cAttack clip looped (:687-692), back to root at the release (:700-710)",
    "cues": [
      [0, "sound", "roundTable1"],
      [0, "voice", "roundTable"]
    ]
  },
  "@KnightoftheDeep:cAttack2": {
    "why": "Whale.cs RPC_cAttack1 case 2 (0.7 s in, :18785-18868): the looped cAttack2 cut in (:18827-18832), the shield status (:18843), and with #273 RPC_roundTable (:18849-18855; coroutine :29121-29480): with knights out (zcKmUWwWZx non-empty :29227-29242) roundTable_ring at the hero's position and rotation (load :29251, createEffect :29263; EffectControl life 999, afterLife 1, followPosition, followState; its repeating WaterWave2 RingEmitter; it loops its own Sounds/roundTable2 from its AudioSource): followState ends it at the release (myCommand shieldBash, 2.3 s into this step: cut 2.3); the coroutine's own voice Voices/roundTable1 | roundTable2 (Random.Range(0, 2) :29308, loads :29320 / :29352) is not in BB's data (they are Sounds/, checks/fx_whale_research/attacks_emotes/container_audio.txt: 'Cannot find roundTable1 voice' :29336): silent; then every 0.5 s (Yield(2, 0.5) :29474, Yield(3, 0.5) :29478) the 4 m pulse (FindAreaTarget(pos, 4, 3) :29412, hit :29434) on enemies only, nothing drawn",
    "cues": [
      [0, "fx", "roundTable_ring", {"cut": 2.3}]
    ]
  },
  "wave": {
    "why": "Whale.cs RPC_emotion (:39843-40665): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (Substring(4) :40141, PlayOneShot :40153, only if it loads :40147; gates: the voice option :40075, more than 2 s since the last action :40081, own hero, game code 31 or a mission teammate :40087-40109); no effect, no Sounds/; BB's Whale voices have hi, wave, ty, bow, beg, cheer, cry, sleep, battle, chat1-5 and no laugh, sit, talk, pose, dance (checks/fx_whale_research/attacks_emotes/container_audio.txt); emo_hi (:40189) and emo_wave (:40196) both play the wave clip (:40630): voice hi or wave",
    "cues": [
      [0, "voice", "hi|wave"]
    ]
  },
  "bow": {
    "why": "Whale.cs RPC_emotion (:39843): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:40141, PlayOneShot :40153); emo_ty (:40205) and emo_bow (:40212) both play the bow clip (:40623), and both voices are in BB's data: voice ty or bow",
    "cues": [
      [0, "voice", "ty|bow"]
    ]
  },
  "sleep": {
    "why": "Whale.cs RPC_emotion (:39843): voice at 0, emo_<name> = Voices/<name> (:40141, PlayOneShot :40153); emo_sleep (:40251-40257)",
    "cues": [
      [0, "voice", "sleep"]
    ]
  },
  "cheer": {
    "why": "Whale.cs RPC_emotion (:39843): voice at 0, emo_<name> = Voices/<name> (:40141, PlayOneShot :40153); emo_cheer (:40263-40269)",
    "cues": [
      [0, "voice", "cheer"]
    ]
  },
  "beg": {
    "why": "Whale.cs RPC_emotion (:39843): voice at 0, emo_<name> = Voices/<name> (:40141, PlayOneShot :40153); emo_beg (:40275-40281); the Whale's data has Voices/beg (unlike the Mole's and the Chameleon's)",
    "cues": [
      [0, "voice", "beg"]
    ]
  },
  "cry": {
    "why": "Whale.cs RPC_emotion (:39843): voice at 0, emo_<name> = Voices/<name> (:40141, PlayOneShot :40153); emo_cry (:40287-40293)",
    "cues": [
      [0, "voice", "cry"]
    ]
  },
  "talk": {
    "why": "Whale.cs RPC_emotion (:39843): emo_chat (:40308) plays the talk clip (:40601) with Voices/chat + Random.Range(1, 6) = chat1-5 (:40127-40133, PlayOneShot :40153; all five in BB's data); emo_talk (:40301) plays it silent (no Voices/talk): the tile takes the chat's voice",
    "cues": [
      [0, "voice", "chat1|chat2|chat3|chat4|chat5"]
    ]
  },
  "battle": {
    "why": "Whale.cs RPC_emotion (:39843): emo_battle (:40571-40577): voice battle (:40141, PlayOneShot :40153); RPC_activateIcon1 (the mission channel) plays the clip with activate1 instead (:45613, :45660-45672; no tile, Penguin decision 19): the tile takes the emote's voice",
    "cues": [
      [0, "voice", "battle"]
    ]
  },
  "run": {
    "why": "the run clip's AnimationEvents playLeftFootEvent at 0.1 s and playRightFootEvent at 0.6 s (checks/fx_whale_research/attacks_emotes/probe_events.txt; the only events on any Whale clip) -> Whale.cs playLeftFootEvent / playRightFootEvent (:113-167): the hero's audio.PlayOneShot(footStep_left / footStep_right) (:135, :164), both = step_heavy1 (the prefab's fields, :15300-15303, probe_fields.txt; Resources/sound/fx/step_heavy1.wav, as the Bison's), own hero or anyone in a mission (mGameType > 4, :120-129, :149-158); every cycle of the run (everyCycle, the Bat's page flag)",
    "everyCycle": true,
    "cues": [
      [0.1, "sound", "step_heavy1"],
      [0.6, "sound", "step_heavy1"]
    ]
  },
  "ko": {
    "why": "Whale.cs RPC_ko (:45778-46154): PlayAnimation(ko, 0.2) (:45992), voice ko1 or ko2 at 0 (Random.Range(0, 2) :46027, loads :46037 / :46068, PlayOneShot :46119 / :46109), getUp after 3 s (Yield(2, 3) :46115, :45894), standby 1 s later (:46117, :45918), no effect; RPC_dead (:46155-46510): Rewind + PlayAnimation(ko, 0) (:46349-46352), dead1 or dead2 at 0 (Random.Range(0, 2) :46387, :46399 / :46411, :46430 / :46442), and always deadEffect at the hero's position and rotation (Resources.Load :46461, Instantiate :46471; IL_7B4 :46454, reached by every voice path, the voice-off and town paths too :46358-46380; EffectControl life 3, the whale_dead ImageEmitter 2.4 m up after Delay 0.4): one of the two at random, even chance (the Sheep's decision 11, as wolf.json / cat.json / the Mole's: roll dead, its voices with it; '!dead' = RPC_ko's)",
    "cues": [
      [0, "voice", "ko1|ko2", {"p": 0.5, "roll": "!dead"}],
      [0, "voice", "dead1|dead2", {"p": 0.5, "roll": "dead"}],
      [0, "fx", "deadEffect", {"p": 0.5, "roll": "dead"}]
    ]
  },
  "getUp": {
    "why": "Whale.cs RPC_revive (:46540-46812): animation.Play(getUp) (:46734) and voice revive at 0 (own hero or a mission teammate :46746-46770, load :46775, PlayOneShot :46808; in BB's data), standby after 1 s (Yield(2, 1) :46810, :46656), no effect; RPC_ko's getUp 3 s into a KO (:45894) is silent: one of the two at random, even chance (decision 11's shape, as cat.json's getUp)",
    "cues": [
      [0, "voice", "revive", {"p": 0.5}]
    ]
  }
```

There is deliberately no `cAttack2` entry: the plain stance draws and says nothing. There is no `root` / `@ChargeAttack:root` entry either, since RPC_cAttack2's release draws nothing.

---
## Parts needed (build stage)

**1. index.html** (every effect cued above is ready by the inventory and the probe; no new effect part):
- SEQ.whale (index.html:1369) replaces its first two entries with:
  `"Normal Attack: nAttack1@0.8 nAttack2@1.0 nAttack3"`,
  `"Charge Attack: cAttack1 cAttack2*@2.29 root~@0.2"`,
  `"Shield Bash: cAttack1 cAttack2*@2.3 shieldBash~"`,
  `"Knight of the Deep: cAttack1 cAttack2*@2.3 shieldBash~"`,
  each with the comment's sources (Read this first 1-3).
- SEQ_SKILL.whale: `{ "@ShieldBash": "shieldBash", "@KnightoftheDeep": "knightOfTheDeep" }` (icons: `icons/hd/whale/shieldBash.webp` exists; knightofthedeep*.webp is in data/icons/skills/whale, for wardrobe_skill_icons.py's rerun).
  - Check that the Charge Attack tile keeps the cAttack icon and that the two passive tiles show only their own (moveSkillIcons, the Chameleon's rule).
- The Thai tile names come from the Bible's cards (the editor's usual source).

**2. Knight of the Deep's knights (depends on the skills report's whale_kingdomKnight part, inventory "kingdomKnight2: needs whale_kingdomKnight"):**
- The tile needs the six rank-2 knights **already standing** at their slots: Init(owner, 2, i), i = 0-5, Whale.cs:28414-28511.
- It uses the part's `standing` option (in OPTS since the Monkey) and one new option, `guard: [from, to]` (seconds after the spawn):
  - every 0.5 s from `from`: a random flat facing (whale_kingdomKnight.cs:682);
  - the knight's own `cAttack` clip looped (:687-692);
  - at `to`: back to `root` (:700-710).
- Draft cues, to align with the knight part's own spawn options, added to `@KnightoftheDeep:cAttack1` (the tile is 0.7 + 2.3 + 0.8 = 3.8 s long; the release at 3.0 s):
  ```json
      [0, "fx", "kingdomKnight2", {"i": 0, "standing": true, "guard": [0, 3.0], "kill": 3.8}],
      ...  (the same for i 1-5)
  ```
- Add `guard` to wardrobe_fx_check.py's OPTS, or the check fails these cues as "bad cue".

**3. Nothing else.**
- extendedWave1-3, shieldBash_ring, roundTable_ring and deadEffect are ready (inventory "### whale", probe_summary.txt).
- The `"sound"` cues use the built path, including Resources/sound/fx/ for step_heavy1 (the Bison's).
- `everyCycle`, `p` / `roll` and `cut` are built.
- The inventory needs no change. The only hero-prefab effect field, `Whale_shield_hit` (= `shield`), is the hit-side block effect, left out below.

## Left out

- **Hits on an enemy.** None of them reaches the 10 m target (Cat decision 19):
  - nAttack_hit (:8290-8303);
  - wallPuncture_hit (:9234-9247) and its own-player camera blur (:16367);
  - shieldBash_hit (:8675-8688);
  - Round Table's pulse;
  - onNormalAttackHit's procs, and Star Spear's single-target rule (w_whl59, :16169-16229), which draws nothing.
- **The receive side.** The wardrobe has no attacker: `shield` toward the attacker (Auto Shield, CharacterControl.cs:4595), `shield` / `shieldReflect` 1 m up and 0.7 m ahead while the stance takes a hit (:30920, :30989).
- **The steps forward.** moveSpeed 4 during each swing, 2 during the bash: no hero mover (Penguin decision 8).
- **RPC_cAttack0** (a release under 1 s): a root crossfade, no tile.
- **The SP-0 auto release**, and SP / timeout / voice-gate bookkeeping (Cat decision 35).
- **RPC_activateIcon1**: no tile (Penguin decision 19). Game code 967's useItem("f_wtb1") attack.
- **The knights' 3 s auto-attacks** (KingdomKnight(), Whale.cs:9650-9720): skipped while the Whale acts and resumed up to 3 s after the last Round Table tick, so they fall outside the tile.
- **Silent clips** (no voice in BB's data): laugh, sit, dance, every pose<n>, pose37 and the TTO emote clips (Bat decision 36).

## Open questions (each with my recommended answer)

1. **Charge Attack tiles.** The code's boundary is `actionTime + 3 <= Time.time`, so a 3.0 s hold with passives on is Shield Bash.
   - **Recommendation: two tiles.** "Charge Attack" released at 2.99 s (`cAttack2*@2.29 root~@0.2`, the plain lowering) and "Shield Bash" at 3.0 s (its own skill and icon). This is the Mole's decisions 2-3 mirrored: there the test was `>`, here it is `<=`.
   - Alternative: one "Charge Attack" tile at 3.0 s ending in shieldBash (passives on), with Shield Bash folded in as the Bison's Hold Charge was. The plain lowering would then never show, and Shield Bash would have no tile of its own.
2. **Knight of the Deep's tile.**
   - **Recommendation: yes, its own tile** with the six knights standing and guarding (Parts 2), the roundTable sound / voice and the ring. This follows the Chameleon's Clear Arrow, a passive shown with its precondition.
   - It waits on the knight part. If that part is not built, the tile still plays the sound, the voice and the ring, but no knights, which misreads the skill. In that case the editor should hold the tile rather than ship it without knights.
3. **Round Table's own voice.** BB asks for Voices/roundTable1 / 2, which do not exist (silent). TTO1102 loads sounds/roundTable1 / 2 instead (pseudo/Whale.c :17500-17818).
   - **Recommendation: BB's, silent** (as Bat decision 36 keeps BB's voices). The ring already loops roundTable2.
   - Alternative: `[0, "sound", "roundTable1|roundTable2"]` in `@KnightoftheDeep:cAttack2`, as TTO plays it.
4. **Mission-only looks** (extendedWave1-3, Shield Bash).
   - **Recommendation: show them**, following the precedent (Mole decision 39).
5. **Stage 1's cut.** The game cuts nAttack1 in (PlayAnimation(x, 0) :16524).
   - **Recommendation: the page's 0.2 s first-step fade**, as every class since the Sheep.
6. **Voice timing in nAttack1.** The voice comes at 0.2 s, not at 0. This is not a choice, just a flag for the editor: nAttack3's voice is at 0, nAttack2's at 0.2.

## Offer for the Bible (whale-skill-reference.md; the user decides, nothing written there)

- **Combo:**
  - the voices at 0.2 / 0.2 / 0 s and the swing sounds at 0.5 / 0.2 + 0.5 / 0.3 s of each stage;
  - stage 3's press window opens at stage 1 + 1.0 (:8204) and has no upper bound but stage 2's own standby at 1.6;
  - the "Normal attack combo" table's own rows give stage 3 at 1.8 (:18589), while its line "Chained start offsets: stage 2 at 0.8, stage 3 at 2.4" reads otherwise;
  - Entended Wave draws extendedWave1-3 (4 m ahead, on the hit times; mission only).
- **Charge Attack:**
  - a release under 1 s is RPC_cAttack0, which lowers the shield (root crossfade, standby 0.2 s later). It is not "nothing happens" (§4.1);
  - a new charge needs 1 s since the last action (:8451);
  - cAttack2 loops from 0.7 s.
- **Shield Bash:** shieldBash with a 0.2 s fade, voice shieldBash1 / 2, the ring and the hit at 0.2 s, a 2 m/s step from 0.2 to 0.4 s, standby at 0.6 s.
- **Round Table:**
  - the ring (and the voice, which BB lacks: Voices/roundTable1 / 2 are missing, TTO loads them from sounds/) comes at the charge's 0.7 s, and the first pulse 0.5 s after that;
  - the ring loops sounds/roundTable2 until the release;
  - the charge's own voice becomes `roundTable` while the knights are out;
  - the knights face a random direction every 0.5 s with their cAttack clip while the Whale charges.
- **Basics:**
  - both footsteps are step_heavy1 (0.1 / 0.6 s of run);
  - BB's Whale has beg / bow / battle / revive voices but no laugh / sit / talk / pose / dance;
  - emo_pose's pose15 fades in over 0.5 s (:40358).

## Verification (2026-11-13)

Checked on the office PC, read only. Probes are in `checks/fx_whale_research/verify/` (git-ignored; the `ae_` files are
this check's): `ae_probe.txt` (`wardrobe_fx.py whale --probe extendedWave1,extendedWave2,extendedWave3,shieldBash_ring,
roundTable_ring,deadEffect,shield,shieldReflect,overPresence`, exit 0), `ae_audio.txt` (BB's Resources container and the
rip for every voice / sound named), `ae_tto_cat.txt` (TTO's catalog, whale voices / sounds), `ae_fields.txt` (the hero
prefab's AudioClip fields), `ae_events.txt` (AnimationEvents), `ae_clip_calls.txt`, `ae_eo_blocks.py` (the cue blocks
parsed and checked against wardrobe_fx_check.py's OPTS / KINDS and `wardrobe/data/whale/clips.json`). **The
Verification wins over the report body.**

**Confirmed (no change):**
- Every coroutine timeline, re-traced from the case labels and Yields: nAttack1 (voice 0.2, sound 0.5, standby 0.7:
  Yield(2, 0.2) :16616, (3, 0.1) :16597, (4, 0.2) :16604, (5, 0.2) :16613), nAttack2 (sound + voice 0.2, hits 0.4 / 0.7,
  sound 0.5, standby 0.8: :17803, :17777, :17781, :17785, :17811), nAttack3 (voice 0, sound 0.3, hit 0.5, standby 0.7:
  :18596, :18598, :18594), shieldBash (voice 0, ring + hit 0.2, standby 0.6: :20176, :20174, :20161), RPC_roundTable
  (ring at its 0, then Yield(2, 0.5) :29474), cAttack1 -> cAttack2 at 0.7 (:19214, :18827).
- The combo's clip starts 0.8 / 1.8 s: only stage 1 writes actionTime on the way (:16509; :16476 / :17730 / :18541 are
  the standbys); press windows :8124-8212 as tabled. So `"Normal Attack: nAttack1@0.8 nAttack2@1.0 nAttack3"` (2.7 s)
  stands; the Bible's own row for stage 3 is 1.8 and its line 609 "stage 3 at 2.4" is the slip the offer names.
- doReleaseCharge, every junk predicate worked by hand (:8486-8643): under 1 s RPC_cAttack0, from 1 s RPC_cAttack2, at
  `actionTime + 3 <= Time.time` with #114 and mGameType > 4 RPC_shieldBash. The 2.99 s / 3.0 s split is the Mole's
  decisions 2-3 mirrored (there `> 3`, here `<=`): **kept**, as the call for the user's review.
- Hit boxes: FindRecTarget(1.5 x rangeMod, 1.5 x rangeMod, 4 + 3 (Entended Wave), 2) (:16444, :17334; nAttack3 width 2,
  :18509); shieldBash FindAreaTarget 3 m (:19850); Round Table 4 m (:29412): none reaches the 10 m point from the start
  spot (the game's own steps, 3.2 m by stage 3's hit, are left out by the no-hero-mover rule, Penguin decision 8).
- Every effect is in BB's Resources and probes as the report says (extendedWave1 ring at (0.6, 0.7, 4) + dust at
  (-0.4 / 1.0, 0.2, 4), Delay 0.5; extendedWave2 rings at (0.3, 0.6 / 0.5, 4), Delay 0.3 / 0.5; extendedWave3 tideCutter
  at (0, 1, 3) Delay 0.4; shieldBash_ring life 1 + its AudioSource shieldBash_ring; roundTable_ring life 999, afterLife 1,
  followPosition, followState, AudioSource roundTable2 looped, its WaterWave2 ring repeatForever; deadEffect life 3,
  whale_dead 2.4 m up, Delay 0.4). deadEffect is Instantiated at the hero's position and rotation (:46454-46471, the
  predicate before the Instantiate true).
- Every voice is in BB's container and the rip: nAttack1-3, cAttack1-2, shieldBash1-2, roundTable, hi, wave, ty, bow,
  sleep, cheer, beg, cry, chat1-5, battle, ko1-2, dead1-2, revive, activate1; none for laugh / sit / talk / pose / dance /
  clap / wai / roundTable1 / roundTable2, in BB or in TTO's catalog (`ae_tto_cat.txt`: the same 114 voices; no clap or
  wai voice under any class). The sounds nAttack1-3, roundTable1-2 are the class's sounds/; step_heavy1 is
  Resources/sound/fx/. Both footstep fields of the hero prefab's script are `step_heavy1` (`ae_fields.txt`), and run's
  events are playLeftFootEvent 0.1 / playRightFootEvent 0.6 (`ae_events.txt`).
- The block parses: 18 entries, 30 cues (6 fx, 7 sound, 17 voice); every kind and option is the page's; every key is a
  clip of `clips.json` or `@KnightoftheDeep:cAttack1/2` (the SEQ name without spaces, index.html:1445, fxStart :5387).
  The ko / getUp / wave / bow / talk entries are the Cat's / Wolf's shapes exactly.
- The TTO line citations (pseudo/Whale.c :12261, :13041, :14155, :2932, :3349, :2793, :18325, :17500; BaseHero.c :1900,
  :2391, :1217) are right; of the emote clips only clap and wai are released (`tto_released.json` whale: clap,
  leviathanCall, wai) and both stay silent.

**Findings:**

1. **Round Table's voice: use TTO's fix, not silence (Q3 reversed).** BB's RPC_roundTable loads Voices/roundTable1 /
   roundTable2 (Whale.cs:29320, :29352), which BB lacks (`ae_audio.txt`); TTO1102 loads
   `GameAssets/characters/heroes/whale/sounds/roundTable1` / `roundTable2` in that slot (pseudo/Whale.c:17541-17544).
   Sheep decision 10 ("use TTO's fixed voices where BB asks for files that don't exist") and Mole decision 47 are the
   precedent; Bat decision 36, cited by Q3, is about the TTO-only emote clips, not a failed BB load. Both files are BB's
   own sounds/ (no TTO content online), so the cue is the `"sound"` kind, at RPC_roundTable's 0 = the cAttack2 step's 0.
   Corrected entry in full:
   ```json
     "@KnightoftheDeep:cAttack2": {
       "why": "Whale.cs RPC_cAttack1 case 2 (0.7 s in, :18785-18868): the looped cAttack2 cut in (:18827-18832), the shield status (:18843), and with #273 RPC_roundTable (:18849-18855; coroutine :29121-29480): with knights out (zcKmUWwWZx non-empty :29227-29242) roundTable_ring at the hero's position and rotation (load :29251, createEffect :29263; EffectControl life 999, afterLife 1, followPosition, followState; its repeating WaterWave2 RingEmitter; it loops its own Sounds/roundTable2 from its AudioSource): followState ends it at the release (myCommand shieldBash, 2.3 s into this step: cut 2.3); then the coroutine's voice, Random.Range(0, 2) (:29308): BB loads Voices/roundTable1 | roundTable2 (:29320 / :29352), missing from BB's data ('Cannot find roundTable1 voice' :29336), so TTO's fix is played (Sheep decision 10, Mole decision 47): TTO1102 loads sounds/roundTable1 | roundTable2 there (pseudo/Whale.c:17541-17544), both in BB's own sounds/ (a 'sound' cue, the hero's PlayOneShot); then every 0.5 s (Yield(2, 0.5) :29474, Yield(3, 0.5) :29478) the 4 m pulse (FindAreaTarget(pos, 4, 3) :29412, hit :29434) on enemies only, nothing drawn",
       "cues": [
         [0, "fx", "roundTable_ring", {"cut": 2.3}],
         [0, "sound", "roundTable1|roundTable2"]
       ]
     },
   ```
   (The block's count becomes 18 entries, 31 cues: 6 fx, 8 sound, 17 voice; finding 2 adds the six knights.)

2. **The knights' draft cues use the wrong slot option and miss the guard's per-slot ticks.** parts.md's whale.js
   interface (parts.md:216-225, :296-299) takes `slot` (0-5, required), not `i` (`i` is the Penguin's, already in OPTS;
   the knight part never reads it, so all six would have no slot). And knightGuard (whale_kingdomKnight.cs:631-763)
   first waits `0.1 x slot` (:761), then every 0.5 s (:756) checks the owner: still attack / cAttack1 -> a random flat
   facing (:682) and `cAttack` looped (:687-692); else standby and `root` looped (:700-710). So each knight goes back to
   root at its first tick at or after the 3.0 s release: slot 0 at 3.0, 1 at 3.1, 2 at 3.2, 3 at 3.3, 4 at 3.4, 5 at 3.0
   (0.5 + 0.5 x 5). The guard is started from the knight's standby when the owner is attack / cAttack1 with #273
   (whale_kingdomKnight.cs:202-220), i.e. at the press. `kill 3.8` (the tile's length, so the next play's standing knights
   replace them in place) stays. Corrected entry in full (the knights joined to the cues; `guard` must be added to
   wardrobe_fx_check.py's OPTS, with parts.md's `attack`):
   ```json
     "@KnightoftheDeep:cAttack1": {
       "why": "Whale.cs RPC_cAttack1 (:18669-19247) with Knight of the Deep #273 (passive; WhaleSkill.cs:2748-2752) and the kingdomKnight status on (the 12th Kingdom Knight's knights out, rank 2: 2 + 2 x 2 = 6 kingdomKnight2, Whale.cs:28414-28511): at 0 the hero's PlayOneShot of Sounds/roundTable1 on every client (kingdomKnight :18994, #273 :19000, load :19012, PlayOneShot :19024) and, in place of cAttack1 / cAttack2, Voices/roundTable (:19078-19106, load :19096, PlayOneShot :19199; own hero or a mission teammate, the 1 s gate :19069); the clip as the plain charge's (PlayAnimation(cAttack1, 0) :18988, Yield(2, 0.7) :19214); the six knights already standing at their slots (the precondition shown: Chameleon decision 13; whale.js 'standing': no rise, no kingdomKnight_ring2), each guarding from the press: its standby sees the owner attack / cAttack1 with #273 (whale_kingdomKnight.cs:202-220) and starts knightGuard (:260, coroutine :631-763): a first wait of 0.1 x slot (:761), then every 0.5 s (:756) a random flat facing (LookRotation(vFlat(Random.onUnitSphere)) :682) with its cAttack clip looped (:687-692), until the first tick at or after the release at 3.0 s (Shield Bash, passives on), which sends it back to root looped (:700-710): 3.0 / 3.1 / 3.2 / 3.3 / 3.4 / 3.0 s for slots 0-5; each knight killed at 3.8 s, the tile's end (0.7 + 2.3 + 0.8), so the next play's standing knights take their place",
       "cues": [
         [0, "sound", "roundTable1"],
         [0, "voice", "roundTable"],
         [0, "fx", "kingdomKnight2", {"slot": 0, "standing": true, "guard": [0, 3.0], "kill": 3.8}],
         [0, "fx", "kingdomKnight2", {"slot": 1, "standing": true, "guard": [0, 3.1], "kill": 3.8}],
         [0, "fx", "kingdomKnight2", {"slot": 2, "standing": true, "guard": [0, 3.2], "kill": 3.8}],
         [0, "fx", "kingdomKnight2", {"slot": 3, "standing": true, "guard": [0, 3.3], "kill": 3.8}],
         [0, "fx", "kingdomKnight2", {"slot": 4, "standing": true, "guard": [0, 3.4], "kill": 3.8}],
         [0, "fx", "kingdomKnight2", {"slot": 5, "standing": true, "guard": [0, 3.0], "kill": 3.8}]
       ]
     },
   ```
   Decision (Q2): the tile ships with the knight part built (missing parts are always built), so "hold the tile" does
   not arise. For the part's builder: `guard`'s `to` is the root return itself (the cue already puts it on the slot's
   tick).

3. **Knight of the Deep's tile needs its HD icon entry.** `SEQ_SKILL` alone makes moveSkillIcons look up
   `HDI.whale.knightOfTheDeep`, which wardrobe_skill_icons.py writes only for a clip's skill, a pool member, EFFECT_ONLY or
   OWN_TILE (pipeline/wardrobe_skill_icons.py:115-145); without it the tile falls back to the low-resolution rank icon
   (index.html:3460-3461). As the Chameleon's Critical Plus / Clear Arrow and the Monkey's Mike Circle, add to `OWN_TILE`:
   ```python
               # the Whale's Knight of the Deep and Shield Reflect on the Charge Attack's clips, Wall Puncture on Peninsula
               # Impale's (2026-11-13, plans/fx_whale/attacks_emotes.md Verification 3-5)
               "whale": {"knightOfTheDeep": ["cAttack1", "cAttack2", "shieldBash"], "shieldReflect": ["cAttack1", "cAttack2", "root"],
                         "wallPuncture": ["peninsulaImpale"]}}
   ```
   (after the `"monkey": {...}` entry, whose closing `}` becomes `,`). The Bible has `whale_knightOfTheDeep1`,
   `whale_shieldReflect5` and `whale_wallPuncture4` in assets.js. Then rerun `py -3 pipeline\wardrobe_skill_icons.py`.

4. **Missed skill: Shield Reflect (#411, Bible card `whale_shieldReflect`, icon `whale_shieldReflect5`) has no tile.**
   Its only look comes when a direct hit lands while the Whale holds the charge's `shield` status: with #411 on the own
   hero, the damage is reflected to the attacker as Effect Damage 411 and `Effects/shieldReflect` is Instantiated at
   `position + TransformDirection(0, 1, 0.7)` with the hero's rotation (CharacterControl.cs:30869-30920); without #411
   (or on another client) `Effects/shield` at the same spot (:30989). effect_only.md Q3 handed it to this report and this
   report left it under "the receive side", so it fell between the two. By the standing rule (one tile per skill) and
   effect_only's own Auto Shield call (a passive started by a hit gets a tile that procs on every play: the Penguin's
   Frost Spike, Bison decision 6, Cat decision 35), it gets its own tile on the charge, the precondition shown (Chameleon
   decision 13), in the Charge Attack's shape: `"Shield Reflect: cAttack1 cAttack2*@2.29 root~@0.2"`, the hit at the
   cAttack2 step's 0 (the shield status starts there, Whale.cs:18843: the earliest block). Passives on, so always the
   reflect look. The probe: shieldReflect = EffectControl life 1, no follow; AudioSource `shieldReflect` (BB
   sounds/shieldreflect); a LineEmitter (wallPuncture material) and a RingEmitter (Line_DoubleLine1) 1 m on: every part
   built, ready (a CharacterControl load, so not in plans/fx_inventory.md, as `shield`). New entry:
   ```json
     "@ShieldReflect:cAttack2": {
       "why": "Shield Reflect #411 (passive, passives on; Bible card whale_shieldReflect) has no clip of its own: it acts when a direct hit lands while the Whale holds the Charge Attack's shield status (RPC_cAttack1 case 2 :18843, from 0.7 s): in AddDamage's status loop (CharacterControl.cs:30855) the own hero with #411 (:30869) reflects min(damage, floor(10 + 10 x sLv + 0.25 x Lv)) to the attacker as Effect Damage 411 (nothing drawn there) and Instantiates Effects/shieldReflect at position + TransformDirection(0, 1, 0.7), the hero's rotation (:30920; without #411 Effects/shield at the same spot :30989); the hit shown at this step's 0, the first moment the stance blocks (a hit-started passive's tile procs on every play: effect_only.md's Auto Shield, the Penguin's Frost Spike); shieldReflect: EffectControl life 1, no follow, its AudioSource plays sounds/shieldReflect, a LineEmitter and a RingEmitter 1 m on in its own frame; the release as the Charge Attack tile's (2.29 s into this step, RPC_cAttack2's root crossfade)",
       "cues": [
         [0, "fx", "shieldReflect", {"d": 0.7, "y": 1}]
       ]
     },
   ```
   Its SEQ line and SEQ_SKILL id: item 6.

5. **Missed tile: Wall Puncture (#251-254, card `whale_wallPuncture`, icon `whale_wallPuncture4`).** It is a proc on the
   hits of nAttack1-3, Sweep, Peninsula Impale and Javelin (getWallPuncture :9196, lckAdjust(40) = 40 % at rank 4), and
   effect_only.md Q4 recommends the Chameleon's Critical Plus shape (decision 12: its own tile, plus the roll in the
   hosts) on nAttack1. But no Normal Attack hit reaches the 10 m point (7 m box, :16444), so a tile on nAttack1 would show
   nothing; the only host that reaches it is Peninsula Impale's 12 m box (skills_b.md, its rolls `impaleWp1-10`). So the
   own tile goes on that clip, every stab's hit a proc: `"Wall Puncture: peninsulaImpale"`, key
   `@WallPuncture:peninsulaImpale`, skills_b's peninsulaImpale cues with each hit's roll pair replaced by the
   unconditional wallPuncture_hit + its sound (follow skills_b's Verification if it moves a time). Because a clip a SEQ
   plays leaves the single-clip list (index.html:3700), Peninsula Impale's own tile must become a one-step sequence too,
   `"Peninsula Impale: peninsulaImpale"` (its cues stay on the plain `peninsulaImpale` key, the fallback at :5388; the
   Sheep's `"Seal of Attack: cast3!"` is one step). New entry (from skills_b.md's block, times 0.8 + 0.3 k / 1.0 + 0.3 k):
   ```json
     "@WallPuncture:peninsulaImpale": {
       "why": "Wall Puncture 4 (#251-254, passive, top rank, passives on; Bible card whale_wallPuncture) has no clip: getWallPuncture() (Whale.cs:9196, lckAdjust(10 x 4) = 40 % at LCK 1) rolls on the hits of nAttack1-3, Sweep, Javelin and Peninsula Impale, and only Peninsula Impale's 12 m box (FindRecTarget(hero, forward, 1.5, 1.5, 12, 3) :26830, Peninsula Asunder #442 on) reaches the 10 m target point; its own tile shows the proc on every stab (the Chameleon's Critical Plus, decision 12): Peninsula Impale as skills_b.md's entry (RPC_peninsulaImpale :26574-27523: voice peninsulaImpale1 | peninsulaImpale2 and peninsulaImpale_ring at 0, asunderImpale at 0.8 + 0.3 k), each of the 10 hits (1.0 + 0.3 k, k = 0 ... 9) RPC_wallPuncture_hit at the target's flat centre 1 m up, LookRotation(the flat direction) = the hero's facing (:26899-26919): Effects/wallPuncture_hit + the hero's PlayOneShot of Sounds/wallPuncture_hit (:9247-9288), in place of the nAttack_hit pair; the camera's WallPuncture blur left out (:26962)",
       "cues": [
         [0, "voice", "peninsulaImpale1|peninsulaImpale2"],
         [0, "fx", "peninsulaImpale_ring"],
         [0.8, "fx", "asunderImpale"],
         [1.0, "fx", "wallPuncture_hit", {"d": 10, "y": 1}],
         [1.0, "sound", "wallPuncture_hit"],
         [1.1, "fx", "asunderImpale"],
         [1.3, "fx", "wallPuncture_hit", {"d": 10, "y": 1}],
         [1.3, "sound", "wallPuncture_hit"],
         [1.4, "fx", "asunderImpale"],
         [1.6, "fx", "wallPuncture_hit", {"d": 10, "y": 1}],
         [1.6, "sound", "wallPuncture_hit"],
         [1.7, "fx", "asunderImpale"],
         [1.9, "fx", "wallPuncture_hit", {"d": 10, "y": 1}],
         [1.9, "sound", "wallPuncture_hit"],
         [2.0, "fx", "asunderImpale"],
         [2.2, "fx", "wallPuncture_hit", {"d": 10, "y": 1}],
         [2.2, "sound", "wallPuncture_hit"],
         [2.3, "fx", "asunderImpale"],
         [2.5, "fx", "wallPuncture_hit", {"d": 10, "y": 1}],
         [2.5, "sound", "wallPuncture_hit"],
         [2.6, "fx", "asunderImpale"],
         [2.8, "fx", "wallPuncture_hit", {"d": 10, "y": 1}],
         [2.8, "sound", "wallPuncture_hit"],
         [2.9, "fx", "asunderImpale"],
         [3.1, "fx", "wallPuncture_hit", {"d": 10, "y": 1}],
         [3.1, "sound", "wallPuncture_hit"],
         [3.2, "fx", "asunderImpale"],
         [3.4, "fx", "wallPuncture_hit", {"d": 10, "y": 1}],
         [3.4, "sound", "wallPuncture_hit"],
         [3.5, "fx", "asunderImpale"],
         [3.7, "fx", "wallPuncture_hit", {"d": 10, "y": 1}],
         [3.7, "sound", "wallPuncture_hit"]
       ]
     },
   ```

6. **The page lines, merged with effect_only.md's (they replace "Parts needed" 1).** SEQ.whale (index.html:1369-1370 at
   this check; anchor on the text; skills_b / tto may add or change their own lines: keep theirs):
   ```js
     whale: ["Normal Attack: nAttack1@0.8 nAttack2@1.0 nAttack3", "Charge Attack: cAttack1 cAttack2*@2.29 root~@0.2",
       "Shield Bash: cAttack1 cAttack2*@2.3 shieldBash~", "Knight of the Deep: cAttack1 cAttack2*@2.3 shieldBash~",
       "Shield Reflect: cAttack1 cAttack2*@2.29 root~@0.2",
       "Cast: cast1 cast2*@0 cast3~", "Bowling Whale: bowlingWhale1@1 bowlingWhale2*@6", "Grand Tide: grandTide1 grandTide2*@3 grandTide0",
       "Peninsula Impale: peninsulaImpale", "Wall Puncture: peninsulaImpale",
       "Auto Shield: root*@1"],
   ```
   (with the comment sources of Read this first 1-3, findings 4-5 here and effect_only.md block 1). SEQ_SKILL:
   `whale: { "@ShieldBash": "shieldBash", "@KnightoftheDeep": "knightOfTheDeep", "@ShieldReflect": "shieldReflect",
   "@WallPuncture": "wallPuncture", "@AutoShield": "autoShield" }` (merged with any other whale ids). Every SEQ_SKILL value
   is left out of every other tile's icons (moveSkillIcons' `pooled`, index.html:3466), so the Charge Attack tile keeps
   only `cAttack` and the Peninsula Impale tile only `peninsulaImpale`.

7. **Shield Bash: this report's tile wins over skills_b.md Q7's single `shieldBash` tile.** Decision: the hold that
   triggers it is shown, as the Mole's Sky Drill (decision 3, `superDig@0.7 dig2*@2.31 skyDrill`: a passive that replaces
   the charge's release). The `shieldBash` entry here and skills_b.md's carry the same two cues; paste one of them (either
   why).

8. **Calls written down (no change to the body):** Entended Wave #401 gets no tile of its own: it always changes the
   Normal Attack (passives on), with no roll, and rides it, as the Mole's Super Dig (decision 2) and skills_b's Tide
   Cutter; the mission-only looks are shown (Mole decision 39, Q4); the first step keeps the page's 0.2 s fade (Q5); the
   plain Charge Attack is released at 2.99 s (Q1, "Confirmed" above).

9. **Line-number nits:** the knights' guard coroutine is `$knightGuard$28453.MoveNext` :631-763 (the class starts at
   :550; the body's ":550-760" is the class span); the check that starts it is :202-220, its #273 test at :214.
