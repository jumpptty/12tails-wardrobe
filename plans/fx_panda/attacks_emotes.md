Short summary: The Panda's Normal Attack is five clips from five coroutines, one per Combo stage, each started at a fixed time after stage 1: 0.6, 1.5, 2.4 and 3.0 s (the page plays the five whole clips back to back today). Its effects are small and all at the hero: two flying `nAttack_punch` fists in stages 1 and 2, the spinning `nAttack_wheel` in stage 3 and, with the Aura Blast passive, the `auraBlast` burst with its own voices in stage 5. The hero's code plays two punch sounds itself (the prefab's AudioClip fields `punch1Fx` / `punch2Fx` = Sounds/punch1 / punch2). The Charge Attack is cAttack1 for 0.7 s, then the looped cAttack2 with two followState effects (`cAttack_ring` and, with Aura Field, `auraField_ring`) that the release ends; the release (RPC_cAttack0) is only a crossfade to root. The emotes follow the usual pattern with the Panda's own voice set (chat1-5; no voice for wave, sit, beg, talk, pose, dance). KO is the Wolf's shape. The run has two footstep sounds (step_light1 / step_light3). Nothing needs building: every effect is ready and every cue kind and option exists. The page work is two SEQ lines. The Charge Attack cues are keyed by the sequence (`@ChargeAttack:...`) because Raijin Ken plays the same two clips with other voices and rings.

=====================================================================
# Panda effects + sounds research: Normal Attack (nAttack1-5), Charge Attack (cAttack1-2) and its release, emotes, basic moves, KO

**Scope.**
- The Combo: RPC_nAttack1 ... RPC_nAttack5 (clips nAttack1-5) and the dispatcher doNormalAttack, with the passives that change them (Combo #101-104, Aura Blast #401).
- The Charge Attack: doBeginCharge, RPC_cAttack1 (clips cAttack1, cAttack2), doReleaseCharge and its one release RPC_cAttack0, with Aura Field #411 (and Sacred Sage #343-344, which draws nothing here).
- MP / SP transfer style skills on an attack clip: none (below).
- RPC_emotion, the basic moves (run, root, falling, getUp, battle), RPC_ko, RPC_dead, RPC_revive, RPC_activateIcon1, the run's footsteps, and the TTO-only emote clips (clap, cooking, fishingPanda, mining, planting, pose37, wai).

**Method.** Research only (recipe steps 1-3), office PC, 2026-11-13. Line numbers are `C:\Users\Jump\Desktop\12tails\DecompiledSource\Panda.cs` (the home PC's `D:\12tails\...`) unless another file is named. Times are seconds from the start of the clip the cue is keyed by. Distance 0 means at the hero. Every opaque predicate on these paths was evaluated by script: `pred.py` gives each `if (a - b op c)` its truth value and flags any TRUE one that guards `continue` or any FALSE one that guards a real statement. It found none in any range cited here (`pred.txt`). The flows were read through `ann.py`, which prints the same lines with each predicate replaced by TRUE / FALSE. Each one goes the normal way.

**Files** (all in `checks\fx_panda_research\attacks_emotes\`, git-ignored, made on this PC):
- `clip_calls.txt`: `node pipeline/clip_calls.js .../DecompiledSource wardrobe/data panda`.
- `RPC_*.txt`: clip_flow.js dumps of RPC_nAttack1-5, RPC_cAttack1, RPC_cAttack0, RPC_emotion, RPC_ko, RPC_dead, RPC_revive, RPC_activateIcon1.
- `ann.py` / `rd.sh` (annotated reads), `pred.py` / `pred.txt` (the predicate check over every range cited here).
- `probe.txt` / `probe_summary.txt` (`summ.py`): `wardrobe_fx.py panda --probe nAttack_punch,nAttack_wheel,auraBlast,cAttack_ring,auraField_ring,nAttack_hit1,nAttack_hit2,deadEffect` (read only).
- `probe_fields.py` / `probe_fields.txt`: the Panda hero prefab (`gameassets/characters/heroes/panda/panda`: the GameObject entry, since the same key also names the MonoScript) and its Panda MonoBehaviour. That is 72 bytes, a 24-byte header plus 6 references: mChar, footStep_left, footStep_right, punch1Fx, punch2Fx and rollAround_ring (empty). The file also lists the AnimationEvents of the prefab's Animation clips.
- `field_keys.py` / `field_keys.txt`: the fields' AudioClips, matched by file + pathID. footStep_left = `sound/fx/step_light1`, footStep_right = `sound/fx/step_light3`, punch1Fx = `heroes/panda/sounds/punch1`, punch2Fx = `heroes/panda/sounds/punch2` (all in sharedassets3).
- `cues.json`: every entry below (identical to the block).

**TTO.** `DecompiledSource_TTO_2026-11-02\pseudo\Panda.c` (TTO1102) keeps the same strings in the same coroutines:
- `<RPC_nAttack1>d__160` :9569, `<RPC_nAttack2>d__161` :10381, `<RPC_nAttack3>d__162` :11208, `<RPC_nAttack4>d__163` :12159, `<RPC_nAttack5>d__164` :12656: nAttack_punch, nAttack_wheel, auraBlast, the voices nAttack1-5 / auraBlast1-2, w_pnd59, and Euler(270, 90, 0) written as 4.712389 / 1.5707964 radians.
- `<RPC_cAttack1>d__167` :1947: cAttack_ring, auraField_ring, the cAttack1 / cAttack2 voices.
- `<RPC_cAttack0>d__168` :1805: root.
- `Panda::doNormalAttack` :35401: the windows 0.3 / 0.8 / 1.44 / 1.7 / 2.6.

The waits cannot be read as literals, so the BB times stand. TTO moved the emotes and KO into BaseHero (`pseudo\BaseHero.c`: `<RPC_emotion>d__146` :1900, `<RPC_dead>d__158` :1217, `<RPC_ko>d__157` :2391, `<RPC_revive>d__159` :3940). Nothing in this scope is a TTO skill. The TTO-only emote clips clap and wai are in `wardrobe/tto_released.json` (panda) but stay silent (below).

---
## Read this first

**1. Normal Attack: five stages at fixed times (index.html work, SEQ panda).**
- Combo 4 (#101-#104, max rank) gives five stages, each its own coroutine.
- Stage k > 1 starts with `Yield(2, actionTime - Time.time + X)`, and actionTime is stage 1's, since the later entries never set it. X = 0.6 (:16621), 1.5 (:17501), 2.4 (:18064), 3.0 (:18802). The Bible's mechanics reference §4.8 has the same anchors.
- Every later stage cuts in (`PlayAnimation(nAttack<k>, 0)` :16015, :16798, :17685, :18216). Stage 1 fades in over 0.2 s (`PlayAnimation(nAttack1, 0.2f)` :15742), which is the page's own first-step fade.
- Today's line `"Normal Attack: nAttack1 nAttack2 nAttack3 nAttack4 nAttack5"` plays the whole clips (0.8 + 1.2 + 1.2 + 0.9 + 0.8 s).
- **Proposed:** `"Normal Attack: nAttack1@0.6 nAttack2@0.9 nAttack3@0.9 nAttack4@0.6 nAttack5"` (3.8 s; stage 5 goes to standby 0.8 s after it starts, :18813 + :18827 + :18817).
  - Step times: 0.6 - 0 = 0.6, 1.5 - 0.6 = 0.9, 2.4 - 1.5 = 0.9, 3.0 - 2.4 = 0.6. Each clip is at least that long (0.8, 1.2, 1.2, 0.9).
  - Each stage's own standby falls exactly on the next stage's start: stage 1 at 0.1 + 0.2 + 0.2 + 0.1 = 0.6, stage 2 at 0.6 + 0.9, stage 3 at 1.5 + 0.9. Stage 4's would come at 2.4 + 0.7 = 3.1, but stage 5 has already taken over at 3.0: stage 4's standby test sees myCommand nAttack5 (:17987).

**2. Every Combo effect is at the hero, and the hero is played in place.**
- The punches are `Instantiate(nAttack_punch, position + TransformDirection(...), rotation)` (:15283, :15488, :16154, :16359). The prefab's EffectControl has life 0.2 and velocity (0, 0, 8), so each fist flies 1.6 m ahead and is gone (probe_summary.txt).
- The wheel and the burst are `createEffect` at the hero (:16939; :18462 at 0.5 m up), each with rotation x `Euler(270, 90, 0)`.
- The game moves the Panda during the combo (the Bible's movement table):
  - stage 1 at 5 m/s from 0.1 to 0.5 s;
  - stage 2 at 4 m/s, then -2;
  - stage 3 at 5 m/s;
  - stage 4 at 10 m/s;
  - stage 5 at -4 m/s.
- The page keeps the hero in place (Penguin decision 8, Cat decision 20), so every effect sits at the standing hero.

**3. The melee hits draw nothing.**
- Every hit is a 2-3 m box or a 2 m circle round the Panda (the Bible's "Boxes"), so none reaches the 10 m target point.
- So there is no `nAttack_hit1` / `nAttack_hit2`. They come from RPC_nAttack1_hit (:7994-8067) and RPC_nAttack2_hit (:8080-8153), only on a landed hit, each with its own Sounds/nAttack_hit1 / 2.
- There are no Shadow Fist, Combo Plus, Spirit Fist or gear procs either.
- Reason: Bison decision 16 (the Wolf's attacks), Cat decision 19.

**4. Hero-played sounds (`"sound"` cues).**
- The hero's code calls `audio.PlayOneShot(punch1Fx)` / `(punch2Fx)` on the own client in a mission / arena (inside the `mGameType > 4` blocks):
  - stage 1 at 0.1 / 0.3 s (:15303, :15508);
  - stage 2 at 0.2 / 0.4 s (:16174, :16379);
  - stage 4: punch2 at 0.3 s (:17816);
  - stage 5: punch1 at 0.3 s (:18408).
- The fields are the prefab's AudioClips `Sounds/punch1` and `Sounds/punch2`. They are the same objects as the Resources paths (probe_fields.txt, field_keys.txt), so `hero_sound_wav` finds `heroes/panda/sounds/punch1.wav` / `punch2.wav`.
- These effects bring their own sound: `nAttack_wheel` (wheel), `auraBlast` (auraBlast), `cAttack_ring` (cAttack_ring, looped).

**5. Aura Blast changes stage 5 (passives on).** With #401, in a mission / arena:
- the voice is `auraBlast1` or `auraBlast2` (Random.Range(0, 2), :18267-18342) instead of `nAttack5`;
- `auraBlast` appears at 0.3 s, 0.5 m up (:18430-18462);
- the hit becomes a 2 m circle at 0.5 s (:18629).

The clip and its 0.8 s length stay the same.

**6. Charge Attack: two clips, two followState effects, a release with no cue.**
- RPC_cAttack1 cuts cAttack1 in at 0 with the voice `cAttack1|cAttack2`.
- At 0.7 s it puts `cAttack_ring` and (Aura Field #411) `auraField_ring` at the hero, then cuts cAttack2 in and loops it (:19006-19105).
- Both effects have followState (probe), so they end when myCommand changes at the release. EffectControl.cs:226-232 compares actionState and myCommand, and RPC_cAttack0 sets myCommand cAttack0 (:19676).
- The only release is RPC_cAttack0 (doReleaseCharge :8325-8337): `CrossFade("root", 0.2)` (:19685), then standby 0.2 s later (:19699). It has no effect and no voice. There is no full charge and no other release.
- Today's line `"Charge Attack: cAttack1 cAttack2*@3"` plays all of cAttack1 (0.9 s).
- **Proposed:** `"Charge Attack: cAttack1@0.7 cAttack2*@3 root~@0.2"`: the game's 0.7 s, the 3 s hold kept, then the release's root crossfade and standby (Question 3).

**7. The Charge Attack cues are keyed by the sequence.**
- Raijin Ken (#444, `"Raijin Ken: cAttack1 cAttack2* raijinKen1 raijinKen2"`) plays the same clips from RPC_raijinKen (:42066, :41688, :42119-42181). It has its own voices (raijinKen1 / raijinKen2) and rings (raijinKen_ring1 / 2).
- fxStart tries `@<sequence id>:<clip>` first, then the plain clip (index.html:5323). Plain `cAttack1` / `cAttack2` entries would therefore also play in the Raijin Ken tile.
- So this report's entries are `@ChargeAttack:cAttack1` and `@ChargeAttack:cAttack2`.

**8. No MP / SP transfer style skill plays an attack clip** (clip_calls.txt):
- nAttack1-5 are played only by RPC_nAttack1-5 (:15742, :16015, :16798, :17685, :18216).
- cAttack1 / cAttack2 are played only by RPC_cAttack1 (:19351, :19100) and RPC_raijinKen (:42066, :41688).
- Sp Transfer plays its own spTransfer clip (:36168).

**9. The emote voices differ from the other classes'** (the rip's `heroes/panda/voices/`).
- Present: hi, ty, bow, laugh, sleep, cheer, cry, battle, chat1-5. Missing: wave, sit, beg, talk, pose, dance.
- chat is `"chat" + Random.Range(1, 6)`, so chat1-5 (:44508).
- The wave tile takes emo_hi's `hi`, since emo_wave is silent. The bow tile takes `ty|bow`, since both are voiced. The talk tile takes the chat voices.
- pose (every set variant), sit, beg and dance stay silent, with no entry.

**10. getUp is silent in BB.**
- BB's RPC_revive (:50800-51015) loads no voice at all, although the rip has `voices/revive.wav`.
- RPC_ko's getUp after 3 s is silent too.
- TTO's BaseHero RPC_revive does play `/Voices/revive` (BaseHero.c :3940). That is a Bible offer, not a cue (Question 6).

**11. Mission-only gates are kept** (the Sheep / Penguin / Wolf / Mole precedent):
- Gated: every nAttack_punch and the punch sounds (:15259, :15464, :16130, :16335, :17808, :18402), the wheel (:16913), Aura Blast's voice and burst (:18273, :18436), and the charge's two rings (:19022).
- Not gated: the voices nAttack1-4 and cAttack1-2 (own hero or a mission teammate), the emote voices, KO, deadEffect and the footsteps.

---
## The dispatcher: doNormalAttack (:7585-7942)

- Own hero only (:7592). Game code 967 swaps the attack for `useItem("f_wtb1")` (:7599-7615): an event mode, out of scope.
- The aim is `vector = vFlat(targetArray[0] - position)`, normalized (:7623-7629). It sets only the facing; the Panda never aims at a point.
- **Stage 1** comes from standby, run or Roll Around's attack (:7641-7665 -> IL_4AE :7896). With the `delayQi` status the press fires RPC_qiStrike2 instead (:7897-7913, Qi Strike's report). Otherwise it fires RPC_nAttack1 once the nAttack timeout is free (:7924-7930).
- **Later stages**, while attacking:

| myCommand | needs | press window (after stage 1) | starts (anchor) | lines |
|---|---|---|---|---|
| nAttack1 | #101 | 0.3 < t < 0.8 | 0.6 (:16621) | :7674-7706 |
| nAttack2 | #102 | 1.0 < t < 1.44 | 1.5 (:17501) | :7734-7766 |
| nAttack3 | #103 | t > 1.7 (no upper bound) | 2.4 (:18064) | :7794-7818 |
| nAttack4 | #104 | t > 2.6 (no upper bound) | 3.0 (:18802) | :7840-7874 |

- Each stage's standby resets actionTime (:15691, :16562, :17432) and runs only while myCommand is still that stage's own.
- So a stage-2 press after stage 1's standby at 0.6 s finds the Panda in standby, with the 1.5 s nAttack timeout still running, and does nothing. In effect the stage-2 window closes at 0.6 s, not at 0.8 (offer).
- The other windows close at 1.44 (before stage 2's standby at 1.5), 2.4 (stage 3's standby) and 3.1 (stage 4's).

## nAttack1 (stage 1): $RPC_nAttack1$25129 (:15126-15845)

| t (s) | what happens | lines |
|---|---|---|
| 0 | attack, actionTime, myCommand nAttack1, addTimeOut(nAttack, 1.5); turn to the aim; clip with a 0.2 s fade; moveSpeed 0 | :15721-15751 |
| 0 | voice nAttack1 (own hero or a mission teammate) | :15754-15823 |
| 0.1 | moveSpeed 5; mission: nAttack_punch at TD(0, 0.5, -0.1), hero rotation; own: punch1 | :15254-15303 |
| 0.1 | the 2 x 2 m box; a landed hit: nAttack_hit1, Combo Plus, Shadow Fist, SP + 1 (left out) | :15330-15439 |
| 0.3 | mission: nAttack_punch at TD(-0.1, 0.45, 0); own: punch2; the second box (no crit, :15528) | :15464-15634 |
| 0.5 | moveSpeed 0 | :15659 |
| 0.6 | standby unless stage 2 was pressed | :15676-15696 |

Waits: Yield(2, 0.1) :15837, Yield(3, 0.2) :15829, Yield(4, 0.2) :15841, Yield(5, 0.1) :15835.

## nAttack2 (stage 2): $RPC_nAttack2$25144 (:15898-16631)

| t (s) | what happens | lines |
|---|---|---|
| press | attack, myCommand nAttack2, then Yield(2, actionTime - now + 0.6) | :16592-16621 |
| 0 | clip cut in, moveSpeed 4, addTimeOut, turn; voice nAttack2 | :16015-16115, :16608 |
| 0.2 | mission: nAttack_punch at TD(0, 0.5, -0.1); own: punch1; box | :16130-16305 |
| 0.4 | mission: nAttack_punch at TD(0, 0.5, -0.1); own: punch2; box | :16335-16495 |
| 0.6 | moveSpeed -2 | :16525 |
| 0.9 | standby unless stage 3 was pressed | :16542-16567 |

Waits: Yield(3, 0.2) :16617, Yield(4, 0.2) :16613, Yield(5, 0.2) :16603, Yield(6, 0.3) :16627.

## nAttack3 (stage 3): $RPC_nAttack3$25157 (:16681-17511)

| t (s) | what happens | lines |
|---|---|---|
| press | attack, myCommand nAttack3, Yield(2, actionTime - now + 1.5) | :17462-17501 |
| 0 | clip cut in, moveSpeed 0, addTimeOut, turn; voice nAttack3 | :16798-16893, :17475 |
| 0.1 | moveSpeed 5; mission: nAttack_wheel by createEffect at the hero, rotation x Euler(270, 90, 0) | :16908-16951 |
| 0.2, 0.4, 0.6 | the three 3 x 3 m box hits (no effect, no sound) | cases 4-6 :16957-17384 |
| 0.8 | moveSpeed 0 | :17400 |
| 0.9 | standby unless stage 4 was pressed | :17417-17437 |

Waits: Yield(3, 0.1) :17484, Yield(4, 0.1) :17507, Yield(5, 0.2) :17478, Yield(6, 0.2) :17497, Yield(7, 0.2) :17491, Yield(8, 0.1) :17489.

`nAttack_wheel` (probe_summary.txt): EffectControl life 0.7 with followPosition; its Animation spins the wheel mesh 0.8 m out; AudioSource `wheel`.

## nAttack4 (stage 4): $RPC_nAttack4$25172 (:17568-18066)

| t (s) | what happens | lines |
|---|---|---|
| press | attack, myCommand nAttack4, Yield(2, actionTime - now + 2.4) | :18032-18064 |
| 0 | clip cut in, moveSpeed 0; voice nAttack4 | :17685-17778, :18059 |
| 0.3 | moveSpeed 10; own client in a mission: punch2 (no effect) | :17795-17816 |
| 0.5 | moveSpeed 0; the 2 x 2 m box | :17835-17959 |
| 0.7 | standby unless stage 5 was pressed | :17987-18007 |

Waits: Yield(3, 0.3) :18053, Yield(4, 0.2) :18048, Yield(5, 0.2) :18057.

## nAttack5 (stage 5): $RPC_nAttack5$25183 (:18110-18831)

| t (s) | what happens | lines |
|---|---|---|
| press | attack, myCommand nAttack5, Yield(2, actionTime - now + 3) | :18781-18802 |
| 0 | clip cut in, moveSpeed 0, addTimeOut; voice auraBlast1 / auraBlast2 (Aura Blast, mission) else nAttack5 | :18216-18374, :18798, :18806, :18829 |
| 0.3 | moveSpeed -4; own client in a mission: punch1; Aura Blast in a mission: auraBlast at the hero + 0.5 up, rotation x Euler(270, 90, 0) | :18391-18465 |
| 0.5 | moveSpeed 0; Aura Blast's 2 m circle (without it: the 3 m box at 0.3 s, :18508) | :18605-18629 |
| 0.8 | standby | :18717-18739 |

Waits: Yield(3, 0.3) :18813; then Yield(4, 0.2) :18827 with Aura Blast, or Yield(5, 0.2) :18821 without it; then Yield(6, 0.3) :18817.

`auraBlast` (probe): life 1, two AlphaTimer layers and a RingEmitter (0.3 -> 2 m), AudioSource `auraBlast`.

## Charge Attack: $RPC_cAttack1$25194 (:18879-19478), the release $RPC_cAttack0$25207 (:19522-19701)

**doBeginCharge** (:8166-8275) starts RPC_cAttack1 (:8263) when all of these hold:
- the Panda is in standby or run;
- it has no `ashura` status (with one it starts RPC_ashuraFist instead, :8215-8222, Ashura's report);
- the cAttack timeout is free (:8242);
- #111 is learned (:8248);
- 0.1 s have passed since the last action (:8257).

| t (s) | what happens | lines |
|---|---|---|
| 0 | attack, actionTime, myCommand cAttack1, vMovement 0, addTimeOut(cAttack, 1), turn; cAttack1 cut in | :19330-19354 |
| 0 | voice cAttack1 or cAttack2 (Random.Range(0, 2)) | :19357-19469 |
| 0.7 | still charging: mission: cAttack_ring at the hero; Aura Field: auraField_ring at the hero | :19007-19098 |
| 0.7 | cAttack2 cut in, looped; tTime = now | :19100-19110 |
| 1.7, 2.7, ... | in a mission, once a second: SP gain; Sacred Sage only with SP > 100 and HP below max; Aura Field's SP to an ally within 8 m | :19125-19323 |
| release | RPC_cAttack0: attack, myCommand cAttack0 (ends both rings), CrossFade(root, 0.2) | :19670-19685 |
| release + 0.2 | standby | :19628-19657, Yield(2, 0.2) :19699 |

Waits: Yield(2, 0.7) :19467; the hold loop is `Yield(3, WaitForFixedUpdate)` :19472.

**doReleaseCharge** (:8294-8349): while attack / cAttack1, it always calls RPC_cAttack0 (:8337).

**Prefabs** (probe_summary.txt), both ready:
- `cAttack_ring`: life 600, followPosition, followState; an ImageEmitter 0.6 m up and a RingEmitter (r 0.4); a looped AudioSource `cAttack_ring`.
- `auraField_ring`: life 99, followPosition, followState; one 3 x 3 m ImageEmitter 0.1 m up.

---
## Emotes and basic moves

**RPC_emotion** ($RPC_emotion$25775, :44265-45090):
- The voice plays at 0, before the clip (:44450-44528).
- It is gated by the voice option, by `Time.time > actionTime + 2` (:44456), and by the player being the own hero, game code 31 or a mission teammate (:44462-44482).
- emo_chat loads `chat + Random.Range(1, 6)` (:44508). Every other emo_<name> loads `Voices/<name>` (:44516) and plays only if the file loads (:44522-44528).
- Then the clip plays with a 0.2 s fade. There are no effects and no Sounds/ loads.

| emote | clip | voice | lines |
|---|---|---|---|
| hi, wave | wave | hi / (none) | :44582, :44590 -> :45032 |
| ty, bow | bow | ty / bow | :44600, :44607 -> :45018 |
| laugh | laugh | laugh | :44614-44620 |
| sit | sit | (none) | :44634-44640 |
| sleep | sleep | sleep | :44646-44652 |
| cheer | cheer | cheer | :44658-44664 |
| beg | beg | (none) | :44670-44676 |
| cry | cry | cry | :44682-44688 |
| talk, chat | talk | (none) / chat1-5 | :44696, :44703 -> :44996 |
| pose | by worn set | (none) | :44710-44956 |
| battle | battle | battle | :44966-44972 |
| dance | dance | (none) | :44981-44989 |

emo_pose picks pose5 / 15 / 25 / 35 / 45 / 58 / 65 / 46 / 66 by the worn set (:44714-44948). With w_pnd56 + c_all56 it freezes the pose (animation.Stop :44916-44928); otherwise it plays pose (:44956).

**Basic moves:**
- **run:** the prefab's Animation has three clips, and only run carries AnimationEvents: `playLeftFootEvent` at 0.1 s and `playRightFootEvent` at 0.4 s (probe_fields.txt).
  - Panda.cs:101-117 plays `footStep_left` = step_light1 and `footStep_right` = step_light3, with no player or mode test.
  - Both wavs are in `Resources/sound/fx/`, which `hero_sound_wav`'s fallback already searches (as for the Chameleon's step_light2 / 3).
  - The entry takes `"everyCycle": true`.
- **root, falling:** nothing (no events, no code sound).
- **battle:** the emote's voice (above). RPC_activateIcon1 loops battle with no voice (:49915-49933); it gets no tile (Penguin decision 19).
- **getUp:** silent (Read this first 10).

**KO**
- RPC_ko ($RPC_ko$25944, :50036-50380): `PlayAnimation(ko, 0)` (:50250), ko1 or ko2 at 0 (:50285-50377), getUp after 3 s (:50371, :50152), standby 1 s later (:50375, :50176).
- RPC_dead ($RPC_dead$25951, :50413-50768): Rewind + `PlayAnimation(ko, 0)` (:50607-50610), then dead1 or dead2 (:50645-50704).
  - It always puts `deadEffect` at the hero's position and rotation (IL_3ED :50712-50729).
  - Every path reaches it: both voice paths, the other-team path, and the path with voices off.
- deadEffect: life 3, an ImageEmitter 0.6 m up and a RingEmitter (probe); ready.

No entry for:
- sit, beg, dance, pose (every variant), getUp, root, falling;
- pose37 and the TTO emote clips (clap, cooking, fishingPanda, mining, planting, wai). TTO's BaseHero would ask for `Voices/clap` and the like, which BB's data lacks. They stay silent, following Bat decision 36 and the Cat, Chameleon and Mole.

---
## Paste-ready cue entries for wardrobe/fx_cues/panda.json (identical to checks\fx_panda_research\attacks_emotes\cues.json)

The file is `{}` today: this block goes between its braces. Other reports' entries are added after a comma.

```json
  "nAttack1": {
    "why": "Panda.cs RPC_nAttack1 (:15126-15845), Combo stage 1 (doNormalAttack :7924-7930): at 0 attack / myCommand nAttack1 / addTimeOut(nAttack, 1.5) (:15721-15730), PlayAnimation(nAttack1, 0.2) (:15742), moveSpeed 0, the voice nAttack1 (own hero or a mission teammate :15754-15776, load :15789, PlayOneShot :15823), Yield(2, 0.1) (:15837); 0.1 s (case 2 :15243): moveSpeed 5 (:15254); mission / arena only (mGameType > 4 :15259, kept: the Sheep / Penguin precedent): Effects/nAttack_punch (:15271) Instantiated at position + TransformDirection(0, 0.5, -0.1) with the hero's rotation (:15283; EffectControl life 0.2, velocity (0, 0, 8): it flies 1.6 m ahead), own hero: PlayOneShot(punch1Fx) (:15297-15303; the prefab field punch1Fx = Sounds/punch1, checks/fx_panda_research/attacks_emotes/probe_fields.txt, field_keys.txt); the hit box (1, 1, 2, 1) at the hero (:15357) reaches 2 m, not the 10 m target: no nAttack_hit1 (RPC_nAttack1_hit :15412, on a landed hit only), no Shadow Fist / Combo Plus / gear procs (:15397-15439); Yield(3, 0.2) (:15829); 0.3 s (case 3 :15453): nAttack_punch at TransformDirection(-0.1, 0.45, 0) (:15488) and PlayOneShot(punch2Fx) = Sounds/punch2 (:15502-15508), same mission gate (:15464); Yield(4, 0.2) (:15841); 0.5 s: moveSpeed 0 (:15659), Yield(5, 0.1) (:15835); 0.6 s: standby unless stage 2 was pressed (:15676-15696); the hero's 2 m run forward (5 m/s from 0.1 to 0.5 s) is played in place (Penguin decision 8, Cat decision 20)",
    "cues": [
      [0, "voice", "nAttack1"],
      [0.1, "fx", "nAttack_punch", {"y": 0.5, "d": -0.1}],
      [0.1, "sound", "punch1"],
      [0.3, "fx", "nAttack_punch", {"x": -0.1, "y": 0.45}],
      [0.3, "sound", "punch2"]
    ]
  },
  "nAttack2": {
    "why": "Panda.cs RPC_nAttack2 (:15898-16631), Combo stage 2 (Combo #101, pressed 0.3-0.8 s after stage 1, doNormalAttack :7674-7706): the entry sets attack / myCommand nAttack2 (:16592-16595) and waits Yield(2, actionTime - Time.time + 0.6) (:16621; actionTime is stage 1's): the clip 0.6 s after stage 1; at 0 PlayAnimation(nAttack2, 0) cut in (:16015), moveSpeed 4 (:16025), addTimeOut (:16030), the voice nAttack2 (load :16094, PlayOneShot :16608), Yield(3, 0.2) (:16617); 0.2 s (case 3 :16119): mission only (:16130) nAttack_punch at TransformDirection(0, 0.5, -0.1), hero's rotation (:16154), own hero PlayOneShot(punch1Fx) = Sounds/punch1 (:16168-16174); Yield(4, 0.2) (:16613); 0.4 s (case 4 :16324): nAttack_punch at the same offset (:16359) and PlayOneShot(punch2Fx) = Sounds/punch2 (:16373-16379); the 2 m boxes' hits (:16209-16305, :16399-16495) never reach the 10 m target; Yield(5, 0.2) (:16603); 0.6 s: moveSpeed -2 (:16525), Yield(6, 0.3) (:16627); 0.9 s: standby unless stage 3 was pressed (:16542-16567)",
    "cues": [
      [0, "voice", "nAttack2"],
      [0.2, "fx", "nAttack_punch", {"y": 0.5, "d": -0.1}],
      [0.2, "sound", "punch1"],
      [0.4, "fx", "nAttack_punch", {"y": 0.5, "d": -0.1}],
      [0.4, "sound", "punch2"]
    ]
  },
  "nAttack3": {
    "why": "Panda.cs RPC_nAttack3 (:16681-17511), Combo stage 3 (Combo #102, pressed 1.0-1.44 s after stage 1, doNormalAttack :7734-7766): entry attack / myCommand nAttack3 (:17462-17465), Yield(2, actionTime - Time.time + 1.5) (:17501): the clip 1.5 s after stage 1; at 0 PlayAnimation(nAttack3, 0) cut in (:16798), moveSpeed 0, addTimeOut, the voice nAttack3 (load :16872, PlayOneShot :17475), Yield(3, 0.1) (:17484); 0.1 s (case 3 :16897): moveSpeed 5 (:16908); mission only (mGameType <= 4 skips it, :16913): Effects/nAttack_wheel (:16927) by createEffect at the hero's position with rotation x Euler(270, 90, 0) (:16939; EffectControl life 0.7, followPosition, plays its own Sounds/wheel); Yield(4, 0.1) (:17507); hits at 0.2, 0.4, 0.6 s (cases 4-6, Yield 0.2 each :17478, :17497, :17491; 3 x 3 m box, no effect, no sound) that never reach the 10 m target; 0.8 s moveSpeed 0 (:17400), Yield(8, 0.1) (:17489); 0.9 s standby unless stage 4 was pressed (:17417-17437)",
    "cues": [
      [0, "voice", "nAttack3"],
      [0.1, "fx", "nAttack_wheel", {"rot": [270, 90, 0]}]
    ]
  },
  "nAttack4": {
    "why": "Panda.cs RPC_nAttack4 (:17568-18066), Combo stage 4 (Combo #103, pressed after 1.7 s, doNormalAttack :7794-7818): entry attack / myCommand nAttack4 (:18032-18035), Yield(2, actionTime - Time.time + 2.4) (:18064): the clip 2.4 s after stage 1; at 0 PlayAnimation(nAttack4, 0) cut in (:17685), moveSpeed 0, the voice nAttack4 (load :17759, PlayOneShot :18059), Yield(3, 0.3) (:18053); 0.3 s (case 3 :17784): moveSpeed 10 (:17795), own hero in a mission / arena (isMine :17800, mGameType > 4 :17808; kept): PlayOneShot(punch2Fx) = Sounds/punch2 (:17816); no effect in this stage; Yield(4, 0.2) (:18048); 0.5 s: moveSpeed 0 (:17835), the 2 x 2 m box hit (:17858-17959; never the 10 m target), Yield(5, 0.2) (:18057); 0.7 s standby unless stage 5 was pressed (:17987-18007)",
    "cues": [
      [0, "voice", "nAttack4"],
      [0.3, "sound", "punch2"]
    ]
  },
  "nAttack5": {
    "why": "Panda.cs RPC_nAttack5 (:18110-18831), Combo stage 5 (Combo #104, pressed after 2.6 s, doNormalAttack :7840-7874), Aura Blast #401 on (passives rule; getAuraBlastLv = hasSkill(401) :9681): entry attack / myCommand nAttack5 (:18781-18784), Yield(2, actionTime - Time.time + 3) (:18802): the clip 3.0 s after stage 1; at 0 PlayAnimation(nAttack5, 0) cut in (:18216), moveSpeed 0, addTimeOut; the voice: with Aura Blast in a mission / arena (:18267-18273, kept) auraBlast1 or auraBlast2 (Random.Range(0, 2) :18279, loads :18291 / :18323, PlayOneShot :18798 / :18806), else nAttack5 (:18355, :18829); Yield(3, 0.3) (:18813); 0.3 s (case 3 :18380): moveSpeed -4 (:18391), own hero in a mission (:18396-18402): PlayOneShot(punch1Fx) = Sounds/punch1 (:18408); Aura Blast in a mission (:18430-18436): Effects/auraBlast (:18450) by createEffect at position + 0.5 up with rotation x Euler(270, 90, 0) (:18462; EffectControl life 1, plays its own Sounds/auraBlast), then Yield(4, 0.2) (Block_6 -> IL_1267 :18827); 0.5 s (case 4 :18605): moveSpeed 0, FindAreaTarget(hero, 2, 3) (:18629: a 2 m circle round the hero, never the 10 m target), Yield(6, 0.3) (:18817); 0.8 s standby (:18717-18739); without Aura Blast (not shown) the 3 m box at 0.3 s (:18508) and the same 0.8 s",
    "cues": [
      [0, "voice", "auraBlast1|auraBlast2"],
      [0.3, "sound", "punch1"],
      [0.3, "fx", "auraBlast", {"y": 0.5, "rot": [270, 90, 0]}]
    ]
  },
  "@ChargeAttack:cAttack1": {
    "why": "Panda.cs RPC_cAttack1 (:18879-19478; doBeginCharge :8242-8263: standby or run, cAttack off timeout, #111, 0.1 s after the last action; no ashura status, else Ashura Fist :8215-8222), the Charge Attack tile's first step (keyed by the sequence: Raijin Ken also plays cAttack1 / cAttack2, with its own voices and rings, RPC_raijinKen :42066, :41688): at 0 attack / actionTime / myCommand cAttack1 / addTimeOut(cAttack, 1) (:19330-19342), PlayAnimation(cAttack1, 0) cut (:19351), the voice cAttack1 or cAttack2 (Random.Range(0, 2) :19386, loads :19396 / :19427, PlayOneShot :19469 / :19465; own hero or a mission teammate :19357-19379), Yield(2, 0.7) (:19467): cAttack2 at 0.7 s (the step @0.7)",
    "cues": [
      [0, "voice", "cAttack1|cAttack2"]
    ]
  },
  "@ChargeAttack:cAttack2": {
    "why": "Panda.cs RPC_cAttack1 case 2 (:19006-19115), 0.7 s after the press, still attack / cAttack1: mission / arena only (mGameType > 4 :19022, kept): Effects/cAttack_ring by createEffect at the hero with its rotation (:19034-19046; EffectControl life 600, followPosition, followState; its looping Sounds/cAttack_ring), with Aura Field #411 on (passives rule; getAuraFieldLv :9688) Effects/auraField_ring there too (:19060-19084; life 99, followPosition, followState; its 3 m ImageEmitter field); then PlayAnimation(cAttack2, 0) cut in, wrapMode Loop (:19100-19105); the hold loop every fixed update (:19125-19323): each 1 s in a mission the SP gain (:19148-19190), Sacred Sage (#343 / #344) only when SP > 100 and HP below max (:19195-19247: nothing at full HP, the Mole's Super Dig heal precedent), Aura Field's SP to an ally within 8 m (:19257-19315: no ally, nothing drawn); held 3 s (the SEQ's @3, the SEQ rule's 3 s for a hold the player ends): doReleaseCharge (:8325-8337) -> RPC_cAttack0 sets myCommand cAttack0 (:19676), which ends both followState effects (EffectControl.cs:226-232 compares actionState and myCommand): cut 3",
    "cues": [
      [0, "fx", "cAttack_ring", {"cut": 3}],
      [0, "fx", "auraField_ring", {"cut": 3}]
    ]
  },
  "wave": {
    "why": "Panda.cs RPC_emotion (:44265-45090): every emote's voice at 0, before its clip (:44450-44528; the voice option on, more than 2 s since the last action :44456, own hero / game code 31 / a mission teammate :44462-44482), emo_<name> = Voices/<name> (Substring(4) :44516, PlayOneShot :44528, only if the file loads :44522); no effect, no Sounds/; the rip's Panda voices have hi, ty, bow, laugh, sleep, cheer, cry, battle, chat1-5 and no wave, sit, beg, talk, pose, dance; emo_hi (:44582) and emo_wave (:44590) both play the wave clip (IL_133B :45032): emo_hi's voice hi, emo_wave silent (no Voices/wave): the tile takes the voiced one",
    "cues": [
      [0, "voice", "hi"]
    ]
  },
  "bow": {
    "why": "Panda.cs RPC_emotion (:44265): emo_ty (:44600) and emo_bow (:44607) both play the bow clip (:45018); both voices are in the rip (Voices/ty, Voices/bow; :44516, PlayOneShot :44528): one of the two, even chance",
    "cues": [
      [0, "voice", "ty|bow"]
    ]
  },
  "laugh": {
    "why": "Panda.cs RPC_emotion (:44265): voice at 0, Voices/<name> (:44516, PlayOneShot :44528); emo_laugh (:44614-44620)",
    "cues": [
      [0, "voice", "laugh"]
    ]
  },
  "sleep": {
    "why": "Panda.cs RPC_emotion (:44265): voice at 0, Voices/<name> (:44516, PlayOneShot :44528); emo_sleep (:44646-44652)",
    "cues": [
      [0, "voice", "sleep"]
    ]
  },
  "cheer": {
    "why": "Panda.cs RPC_emotion (:44265): voice at 0, Voices/<name> (:44516, PlayOneShot :44528); emo_cheer (:44658-44664)",
    "cues": [
      [0, "voice", "cheer"]
    ]
  },
  "cry": {
    "why": "Panda.cs RPC_emotion (:44265): voice at 0, Voices/<name> (:44516, PlayOneShot :44528); emo_cry (:44682-44688)",
    "cues": [
      [0, "voice", "cry"]
    ]
  },
  "talk": {
    "why": "Panda.cs RPC_emotion (:44265): emo_chat (:44703) plays the talk clip (:44996) with Voices/chat + Random.Range(1, 6) = chat1-5 (:44502-44508, PlayOneShot :44528; all five in the rip); emo_talk (:44696) plays it silent (no Voices/talk): the tile takes the chat's voice",
    "cues": [
      [0, "voice", "chat1|chat2|chat3|chat4|chat5"]
    ]
  },
  "battle": {
    "why": "Panda.cs RPC_emotion (:44265): emo_battle (:44966-44972): voice battle (:44516, PlayOneShot :44528); the mission's RPC_activateIcon1 loops the clip with no voice (:49930; no tile, Penguin decision 19): the tile takes the emote's voice",
    "cues": [
      [0, "voice", "battle"]
    ]
  },
  "run": {
    "why": "the run clip's AnimationEvents playLeftFootEvent at 0.1 s and playRightFootEvent at 0.4 s (the Panda prefab's Animation, checks/fx_panda_research/attacks_emotes/probe_fields.txt; the only events on its clips) -> Panda.cs:101-117: the hero's audio.PlayOneShot(footStep_left) = step_light1 / (footStep_right) = step_light3 (the fields :14554 / :14557, probe_fields.txt, field_keys.txt: Resources/sound/fx/), no player or mode test; every cycle of the run (everyCycle, as the Bat's and the Chameleon's)",
    "everyCycle": true,
    "cues": [
      [0.1, "sound", "step_light1"],
      [0.4, "sound", "step_light3"]
    ]
  },
  "ko": {
    "why": "Panda.cs RPC_ko (:50036-50380): PlayAnimation(ko, 0) (:50250) and the voice ko1 or ko2 at 0 (Random.Range(0, 2) :50285, loads :50295 / :50326, PlayOneShot :50368 / :50377), getUp after 3 s (Yield(2, 3) :50371, PlayAnimation(getUp, 0) :50152, silent), standby 1 s later (:50375, :50176), no effect; RPC_dead (:50413-50768) plays the same clip (Rewind + PlayAnimation(ko, 0) :50607-50610) with dead1 or dead2 at 0 (Random.Range(0, 2) :50645, :50657-50700) and always Effects/deadEffect at the hero's position and rotation (IL_3ED :50712-50729, reached by every voice path and with voices off; EffectControl life 3): one of the two at random, even chance (the Sheep's decision 11, as wolf.json / cat.json / mole's: roll dead, its voices with it; '!dead' = RPC_ko's)",
    "cues": [
      [0, "voice", "ko1|ko2", {"p": 0.5, "roll": "!dead"}],
      [0, "voice", "dead1|dead2", {"p": 0.5, "roll": "dead"}],
      [0, "fx", "deadEffect", {"p": 0.5, "roll": "dead"}]
    ]
  }
```

17 entries, 33 cues (9 fx, 8 sound, 16 voice). Checked by script against the data (checks\fx_panda_research\attacks_emotes\cues.json):
- every key is a Panda clip, or `@ChargeAttack:<clip>`;
- every cue list is in time order;
- every kind and option is in wardrobe_fx_check.py's KINDS / OPTS;
- every voice is in the rip's `heroes/panda/voices/`;
- every sound is in `heroes/panda/sounds/` (punch1, punch2) or `Resources/sound/fx/` (step_light1, step_light3);
- every effect is "ready" in plans/fx_inventory.md "### panda".

---
## Parts needed (build stage)

**None.**
- Every cued effect is ready: nAttack_punch, nAttack_wheel, auraBlast, cAttack_ring, auraField_ring and deadEffect are Resources.Load paths, all "ready" in plans/fx_inventory.md, and the probe shows only built components.
- The root EffectControl's velocity (the punch's 8 m/s) is applied by Fx (index.html:4243-4246). followPosition and followState are handled, and a followState cut at the step end comes at the step change (fxStart, index.html:5315-5319).
- Every cue kind (fx, voice, sound), option (x, y, d, rot, cut, p, roll) and entry key (everyCycle) already exists.

**index.html (the editor's):**
- SEQ panda: `"Normal Attack: nAttack1@0.6 nAttack2@0.9 nAttack3@0.9 nAttack4@0.6 nAttack5"` and `"Charge Attack: cAttack1@0.7 cAttack2*@3 root~@0.2"`, with a comment citing Read this first 1 and 6.
- The other four lines (Raijin Ken, Fuujin Ken, Qi Strike, Tempest Dance) belong to the skills / TTO reports.
- Nothing for NEVER_PLAYED or LOOPS.
- No SEQ_SKILL entry is needed for these two tiles. data/icons/hd/index.json already has panda `nAttack` and `cAttack`, the Bible's Combo and Charge Attack icons.

**wardrobe_fx.py:** nothing. `hero_sound_wav` finds punch1 / punch2 in the class's sounds/ and step_light1 / step_light3 under Resources/sound/fx (its fallback).

## Left out

- **The hits on an enemy:** nAttack_hit1 / nAttack_hit2 and their Sounds/nAttack_hit1 / 2 (RPC_nAttack1_hit / 2_hit), Shadow Fist, Combo Plus, Spirit Fist, onNormalAttackHit's gear procs, and SP + 1. The boxes and circles reach 2-3 m, never the 10 m target (Bison decision 16, Cat decision 19).
  - Whether any of those passives (Shadow Fist #331-334, Combo Plus #241-244, Spirit Fist #433, Combo Link #442) gets an effect-only tile of its own is the effect_only report's call. ShadowFist (:35669-35861) loads no effect.
- **The hero's travel** during the combo: in place (Penguin decision 8, Cat decision 20).
- **Variants replaced by passives on:**
  - stage 5 without Aura Blast (the nAttack5 voice and the 3 m box);
  - the charge without Aura Field (no auraField_ring).
- **Things that draw nothing in the wardrobe:**
  - the charge's SP ticks;
  - Sacred Sage (needs SP > 100 and HP below max; its voices sacredSage1 / 2 are in RPC_sacredSage :9211-9290, for whichever report gives Sacred Sage a tile);
  - Aura Field's ally SP;
  - Force Gauntlet (w_pnd59), which only changes the hit search (:15338-15349 and the matching sites).
- **The Delay Qi release** from the attack key (RPC_qiStrike2, Qi Strike's report) and **Ashura Fist** in place of the charge (Ashura's report).
- **The 2 s emote voice gate and the timeouts** (Cat decision 35).
- **activateIcon1** (no tile, Penguin decision 19), and the event mode's `f_wtb1` (game code 967).

## Open questions (each with my recommended answer)

1. **Normal Attack step times.**
   - **Recommendation: `nAttack1@0.6 nAttack2@0.9 nAttack3@0.9 nAttack4@0.6 nAttack5`**: the game's anchors at the earliest presses (the Wolf / Sheep / Penguin / Bat / Mole precedent).
   - Today's whole clips run 4.9 s instead of 3.8 s and put every later cue late.
2. **Keep the hero in place?**
   - **Recommendation: yes** (Penguin decision 8, Cat decision 20). The fists, wheel and burst sit at the standing hero.
   - The game would have carried the hero about 2 m forward by stage 1's end and about 0.8 m back during stage 5.
3. **Charge Attack tile.**
   - **Recommendation: `cAttack1@0.7 cAttack2*@3 root~@0.2`.** The 0.7 s is the game's own (Yield 0.7 :19467). The 3 s is the SEQ rule's hold, since the Panda's charge has no full charge. root~@0.2 is the release's CrossFade(root, 0.2) and standby 0.2 s later (the Mole's burrow tile ends the same way).
   - Alternative: `cAttack1@0.7 cAttack2*@3`. The release crossfade is then replaced by the page's 0.2 s loop fade back into cAttack1. The cues do not change.
4. **Key the charge cues `@ChargeAttack:cAttack1` / `@ChargeAttack:cAttack2`?**
   - **Recommendation: yes.** Plain keys would also fire in the Raijin Ken tile, which plays the same clips with raijinKen1 / raijinKen2 and its own rings.
   - If the skills report keys its Raijin Ken entries `@RaijinKen:cAttack1` / `@RaijinKen:cAttack2`, plain keys would also work. The sequence keys are safe either way.
5. **Show the mission-only effects and sounds** (every punch, the wheel, Aura Blast's voice and burst, the charge's rings)?
   - **Recommendation: yes** (the Sheep / Penguin / Wolf / Mole precedent).
   - In town the game shows only the voices.
6. **getUp's voice.**
   - **Recommendation: silent, no entry.** BB's Panda.cs RPC_revive plays no voice, although `voices/revive.wav` is in BB's data. TTO's BaseHero plays `/Voices/revive` for every hero.
   - The emotes and basic moves are BB content (Bat decision 36: chat voices stay BB's). A cross-class follow-up with TTO's revive is an offer, not this job.
7. **Wave tile.**
   - **Recommendation: `hi` on every play.** emo_wave has no voice file, so the only voiced way into the clip is emo_hi.
   - The alternative, `hi` on half the plays (emo_wave's silence on the other half, Cat getUp's p 0.5 shape), is not worth a roll.

## Offers for the Bible (panda-skill-reference.md / mechanics §4.8; the user decides, nothing written there)

- **Combo windows in effect:**
  - Stage 2's press window is 0.3 < t < 0.8 in the dispatcher (:7690-7698), but stage 1 goes to standby at 0.6 s when stage 2 has not been pressed (:15676-15696, actionTime reset :15691). The nAttack timeout (1.5 s, :15730) then blocks a new stage 1, so a press between 0.6 and 0.8 s does nothing: the window is in effect 0.3-0.6 s.
  - Likewise stage 4's has no upper bound in code but closes at 2.4 s (stage 3's standby), and stage 5's at 3.1 s (stage 4's).
- **The Combo's look and sounds by stage** (the reference lists hits and boxes, not effects):
  - stage 1: punches at 0.1 / 0.3 s;
  - stage 2: punches at 0.2 / 0.4 s;
  - stage 3: the wheel at 0.1 s, then hits at 0.2 / 0.4 / 0.6 s;
  - stage 4: only the punch2 sound, at 0.3 s;
  - stage 5: the punch1 sound and the Aura Blast burst at 0.3 s, the hit at 0.5 s.

  All of them only in missions / arenas.
- **Aura Blast's voice:** stage 5's voice becomes auraBlast1 / auraBlast2, but only in missions / arenas (:18267-18273). In town it stays nAttack5 even with #401.
- **Charge Attack's rings:** cAttack_ring and auraField_ring come at 0.7 s, mission only (:19022), and they last until the release, which is always the plain RPC_cAttack0 crossfade (no charged release).
- **Voices:**
  - the Panda's chat draws chat1-5 (Random.Range(1, 6), :44508);
  - emo_wave, emo_sit, emo_beg, emo_talk, emo_pose and emo_dance name voices the Panda's data lacks;
  - BB's RPC_revive plays no voice, while TTO's BaseHero plays Voices/revive.
- **The run's footsteps:** step_light1 / step_light3 at 0.1 / 0.4 s of each run cycle, for every player in every mode (:101-117: no isMine or mode test, unlike the Chameleon's).

## Verification (2026-11-13)

Checker's re-trace, office PC; probes in `checks/fx_panda_research/verify/ae_eo/` (git-ignored): `probe.json` /
`probe_summary.txt` (`wardrobe_fx.py panda --probe` on the 15 effects of this report and effect_only, exit 0),
`check_cues.py` (keys, order, kinds, options and every name against the rip). This section wins over the body.

1. **Timings: confirmed, no change.** Each coroutine's waits re-added from the Yield lines (one Yield per state, so the
   chain is 2, 3, 4, ...):
   - stage 1: 0.1 (:15837) + 0.2 (:15829) + 0.2 (:15841) + 0.1 (:15835) = 0.6 s to its standby;
   - stage 2: starts at actionTime + 0.6 (:16621), then 0.2 + 0.2 + 0.2 + 0.3 (:16617, :16613, :16603, :16627) = 0.9 s;
   - stage 3: + 1.5 (:17501), then 0.1 + 0.1 + 0.2 + 0.2 + 0.2 + 0.1 (:17484, :17507, :17478, :17497, :17491, :17489) = 0.9 s;
   - stage 4: + 2.4 (:18064), then 0.3 + 0.2 + 0.2 (:18053, :18048, :18057) = 0.7 s;
   - stage 5: + 3 (:18802), then 0.3 + 0.2 + 0.3 (:18813, :18827, :18817) = 0.8 s.
   - Starts 0 / 0.6 / 1.5 / 2.4 / 3.0, so the steps are 0.6 - 0 = 0.6, 1.5 - 0.6 = 0.9, 2.4 - 1.5 = 0.9, 3.0 - 2.4 =
     0.6, then nAttack5's whole 0.8 s clip: 3.0 + 0.8 = 3.8 s. Stages 2-5 are cuts (PlayAnimation(x, 0) :16015,
     :16798, :17685, :18216), stage 1 the 0.2 fade (:15742). The proposed line stands:
     `"Normal Attack: nAttack1@0.6 nAttack2@0.9 nAttack3@0.9 nAttack4@0.6 nAttack5"`.
   - The dispatcher's windows (:7690 / :7698 0.3-0.8, :7750 / :7758 1.0-1.44, :7810 > 1.7, :7866 > 2.6) are as written.
   - Charge Attack: Yield(2, 0.7) (:19467), cAttack2 cut in and looped (:19100-19105), the release's
     CrossFade("root", 0.2) (:19685) and Yield(2, 0.2) (:19699). `"Charge Attack: cAttack1@0.7 cAttack2*@3 root~@0.2"`
     stands. The first step keeps the page's fade although RPC_cAttack1 cuts cAttack1 in (:19351): Bison decision 4,
     Cat decision 2.
2. **Names: confirmed.**
   - The six effects are in the rip's `heroes/panda/effects/` and the probe matches the body: nAttack_punch life 0.2,
     velocity (0, 0, 8); nAttack_wheel 0.7, followPosition, AudioSource wheel; auraBlast 1, AudioSource auraBlast;
     cAttack_ring 600, followPosition + followState, looped cAttack_ring; auraField_ring 99, followPosition +
     followState; deadEffect 3.
   - Every voice (nAttack1-5, auraBlast1-2, cAttack1-2, hi, ty, bow, laugh, sleep, cheer, cry, chat1-5, battle, ko1-2,
     dead1-2) is in `voices/`. punch1 / punch2 are in `sounds/`, step_light1 / step_light3 in `Resources/sound/fx/`.
   - The run's events (0.1 / 0.4 s) and the four AudioClip fields match `attacks_emotes/probe_fields.txt` and
     Panda.cs:101-117.
   - The TTO-only emote clips: TTO's catalog (`tto_assets/2026-11-09/catalog.bin`, `heroes/panda/voices/`) has no clap,
     wai or cooking voice either, so silence is right for the released clap / wai too (Bat decision 36).
3. **Positions: confirmed.**
   - TransformDirection(0, 0.5, -0.1) at :15283, :16154 and :16359, and (-0.1, 0.45, 0) at :15488, become
     `{"y": 0.5, "d": -0.1}` and `{"x": -0.1, "y": 0.45}`.
   - The wheel: hero rotation x Euler(270, 90, 0) (:16939). The burst: + 0.5 up, the same rotation (:18462).
   - deadEffect: the hero's position and rotation (:50729). It has no `d`, unlike the Bison's.
4. **The cue block: valid, no change.** It parses and equals `attacks_emotes/cues.json`: 17 entries, 33 cues (9 fx,
   8 sound, 16 voice; recounted). Every key is a clip in `wardrobe/data/panda/clips.json`, or `@ChargeAttack:<clip>`,
   which is the id of the SEQ name "Charge Attack" (index.html:1410). Every kind and option is in
   wardrobe_fx_check.py KINDS / OPTS (:176-186). The ko / wave / bow / talk shapes match cat.json and bison.json.
5. **Q4 settled.** skills_b keys its Raijin Ken entries `@RaijinKen:cAttack1` / `@RaijinKen:cAttack2`
   (plans/fx_panda/skills_b.md:367-376). Plain keys would therefore also have been safe. Keep `@ChargeAttack:` anyway:
   effect_only's Sacred Sage tile plays the same clips under its own keys.
6. **Open questions 1-7: decided as recommended.** The precedents cited hold: Wolf / Sheep / Penguin / Bat / Mole
   stage anchors; Penguin decision 8 and Cat decision 20 (in place); the Mole's burrow release shape; Sheep / Penguin /
   Mole mission gates kept; getUp silent, because Panda.cs loads no `Voices/revive` anywhere (grep), though the rip has
   the file (Mole decision 16, Chameleon decision 19); `hi` for the wave tile, as no `wave.wav` exists.
7. **Missed, outside this report's clips (the effect_only Verification item 3 has the full fix): Wind & Cloud and Rain &
   Storm are cued by no Panda report.** Both are BB skills with Bible cards (bible/index.html:19286-19287). Their clips
   `wind&cloud` (3.6 s) and `rain&storm` (3.0 s) are missing from clips.json because of the `[a-z0-9_]+` clip filter
   (pipeline/wardrobe_data.py:49 and :210). Nothing in this report's own scope (Combo, Charge Attack, emotes, basic
   moves, KO) is missed.
8. **Coordination with effect_only:** the Sacred Sage Technique tile must take this report's Charge Attack steps,
   `root~@0.2` included (effect_only Verification item 2).
