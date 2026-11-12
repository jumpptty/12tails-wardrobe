# Bison effects + sounds research: Normal Attack, Charge Attack (and Hold Charge), emotes, basic moves, KO

Scope: clips nAttack1-5 (RPC_nAttack1-5 and the dispatcher `doNormalAttack`), cAttack1-6 (RPC_cAttack1, the release
`doReleaseCharge` with RPC_cAttack0 / RPC_cAttack2, `doBeginCharge`), the Hold Charge passive (#113) that changes the
release, the emotes (RPC_emotion), basic moves (run's AnimationEvents) and KO (RPC_ko, RPC_dead). Research only (recipe
steps 1-3). Line numbers are `D:\12tails\DecompiledSource\Bison.cs` unless another file is named; TTO is
`DecompiledSource_TTO_2026-11-02\pseudo\Bison.c`. Times are seconds from the start of the clip the cue is keyed by.
Distance 0 = at the hero. Model: `plans/fx_penguin/attacks_emotes.md`.

Every opaque predicate on the paths below was resolved by a script, not by eye: `checks\fx_bison_research\attacks_emotes\resolve.py`
prints a line range with each `if (a - b != c)` replaced by TRUE / FALSE (the waits are then read off the labels).
Other probes in that folder (all read-only):
- `RPC_*.txt`: `clip_flow.js` dumps; `clip_calls.txt`: every Bison clip call;
- `probe.txt` / `summarize.py`: `wardrobe_fx.py bison --probe cAttack1_dust,solidCharge_ring,cAttack2_dust,spinHack_ring,holdCharge_fire,holdCharge,holdCharge_ring,deadEffect,nAttack_hit`;
- `probe_fields.py` -> `probe_fields.txt`: the Bison hero prefab's fields;
- `probe_events.py` -> `probe_events.txt`: AnimationEvents on the Bison's clips;
- `rip_list.py` -> `rip_list.txt`: the Bison's voices/ and sounds/ in the game's resource container;
- `find_res.py` -> `find_res.txt`: where step_heavy1/2, axe_hit1, hammer_hit1 live.

---

## Read this first

1. **No other skill plays an attack clip.** `clip_calls.txt`: nAttack1-5 are played only by RPC_nAttack1-5 (:15128,
   :15383, :16175, :16983, :18991) and cAttack1-6 only by RPC_cAttack1 / RPC_cAttack2 (:19284, :19419, :20322-20358).
   The Bison has no MP / SP transfer skill and no mission clip on an attack (its RPC_activateIcon1 plays `battle`,
   :40354, item 9). Over Swing (#273) is started from `doBeginCharge` while Over Power is on (:5203-5280) but plays its
   own `overSwing` clip (:25464): another report's skill.
2. **The page's Normal Attack sequence is wrong in two ways** (index.html work).
   - It plays **both** nAttack3 and nAttack4. The game plays **one of them**: after stage 2, with Combo 3 / 4
     (#103 / #104), `Random.Range(0, 100) <= lckAdjust(25 + 5 x ImprovedSwingLv + 15)` starts the spin RPC_nAttack4,
     else RPC_nAttack3 (:4947-5017). At max rank (Improved Swing 3) that is `lckAdjust(55)` = 55 at the page's LCK 1
     (CharacterControl.cs:20667-20668: 55.55 x 100 / 100.55 = 55.25), and `<=` counts 0..55: **56 % spin, 44 % stage 3**.
   - The stage times: stage 2 at 0.7 s, stage 3 / the spin at 1.4 s, Added Swing at **2.2 s after stage 3 but 2.7 s
     after the spin** (RPC_nAttack5's two waits, `actionTime - now + 2.2` / `+ 2.7`, :19016 / :19022; actionTime is set
     only by stage 1). Today's `nAttack3@0.8 nAttack4@0.8` starts nAttack5 at 3.0 s.
   - nAttack5 fades in over **0.3 s** (`PlayAnimation("nAttack5", 0.3f)` :18991); the SEQ has only 0.2 / 0.1 fades, and
     today's step is a cut.
   - Proposed (two small page parts, "Parts needed"): **`"Normal Attack: nAttack1@0.7 nAttack2@0.7 nAttack4@1.3%56|nAttack3@0.8 nAttack5~0.3"`**.
3. **The page's Charge Attack sequence is a little off, and Hold Charge (#113, a passive, so ON) changes the release.**
   - cAttack1 gives way to the looped cAttack2 after **0.8 s** (`Yield(2, 0.8)` :19608), not the clip's 1.0 s; the full
     charge is 8 s (rank 2: `clamp(t, 2, 4 + 4)` :5378), so cAttack2 holds **7.2 s**.
   - The spin (Improved Swing 3: cAttack6, :20352-20358) ends at **1.816 s**: 8 hits, each two waits of
     `0.2 - 0.033 x 3` = 0.101 s (:20464, :20468), then `Yield(4, 0.2)` (:20466) before standby (:19822-19850). Today: 1.6.
   - **With Hold Charge learned, a release after 2 s never spins.** `doReleaseCharge` stores the charge as the
     `holdCharge` status (sValue = the hit count, 8) and plays RPC_cAttack0 (root, 0.2 s crossfade) instead
     (:5388-5411); the spin comes on the **next attack press**, from standby (`doNormalAttack`'s holdCharge branch,
     :5089-5120), and that spin draws `holdCharge_fire` as it spends the status (:20263-20292). The status itself draws
     `holdCharge_ring` (a burst with its own sound) and the `holdCharge` glow on the hero until the spin (CharacterControl.cs:34666-34708,
     removed :15390-15403). Hold Charge also changes the charge's voice: `holdCharge1|holdCharge2`, not `cAttack1|cAttack2` (:19457-19613).
   - Proposed (passives ON, the press right at standby): **`"Charge Attack: cAttack1@0.8 cAttack2*~@7.2 root~@0.2 cAttack6*@1.816"`**,
     the release's cues under `"@ChargeAttack:root"`. Without Hold Charge it would be `"cAttack1@0.8 cAttack2*~@7.2 cAttack6*@1.816"`
     (question 1; both cue sets are below).
4. **Every effect named here is buildable today** (all their parts are built: EffectControl, Ellipsoid / Ring / Vortex /
   Image / Line emitters, ParticleAnimator / Renderer, AudioSource; `probe.txt`). Two of them are missing from
   `plans/fx_inventory.md` because `CharacterControl.cs` loads them, not `Bison.cs`: `holdCharge` and `holdCharge_ring`
   (CharacterControl.cs:34670, :34673); both are in `heroes/bison/effects/` and extract (probe).
5. **Hits draw nothing here.** The Bison's attacks are melee (5-6 m reach, :14801, :15607, :16418, :17216, :17506,
   :18313, :18603, :20016-20021), so an enemy at the 10 m target point is not hit: no `nAttack_hit` (at the target, +1.2 /
   +1.5 m up, :14850, :15673, :16484, :17272, :17562, :18369, :18659, :20060), no `axe_hit1` / `hammer_hit1` (played by
   RPC_nAttack_hit :7112-7138 and after the spin's / Added Swing's second hit only when something was hit, :17615-17778,
   :18860-18875), no Over Pride voice (`onOverPride` :8615-8736 runs only after a stage hit something, :14907 etc.),
   no onNormalAttackHit gear procs. As the Wolf's melee attacks (plans/fx_wolf/attacks.md:64). Question 3.
6. **Sounds the hero's code plays itself (`"sound"` cues):** the spin's `Sounds/cAttack2` twice per hit, 16 times
   (:19786-19798, :19917-19929); the run's footsteps `step_heavy1` / `step_heavy2` (AnimationEvents, item 8). Every
   other sound comes with its effect: `cAttack1_dust` plays `sounds/cAttack1` **looped** for the whole charge,
   `holdCharge_fire` and `holdCharge_ring` their own one-shots (probe).
7. **Name collisions** (the cue kind picks the folder; voices are saved as `v_<name>`): `cAttack1` / `cAttack2` are clips,
   `voices/` files and `sounds/` files (sounds/cAttack1 = the charge loop on cAttack1_dust, sounds/cAttack2 = the spin
   swish); `nAttack1-5` are clips and voices; `holdCharge_fire` / `holdCharge_ring` are effects and sounds (their own).
8. **The run clip has footsteps.** `run` carries `playLeftFootEvent` at 0.1 s and `playRightFootEvent` at 0.6 s
   (`probe_events.txt`), which play the hero fields `footStep_left` / `footStep_right` (:124-178) = `step_heavy1` /
   `step_heavy2` (`probe_fields.txt`), files only in `Resources/sound/fx/` (`find_res.txt`). This is the Bat's run case
   (plans/fx_bat/attacks_emotes.md "Read this first" 8 and its verification): the same two small jobs (a `"sound"`
   fallback to `sound/fx` in the build, and `everyCycle`).
9. **Emotes as the other classes', except laugh is silent.** The Bison's rip has no `voices/laugh` (`rip_list.txt`), so
   `emo_laugh` loads nothing (:34805-34817) and the laugh clip gets no entry. Voices that exist: hi, wave, ty, bow,
   sleep, cheer, beg, cry, battle, chat1-5, ko1/2, dead1/2. RPC_activateIcon1 plays `battle` (:40354) with
   `activate1` / `activate2` (:40401, :13748), neither in the rip: no tile (Penguin decision 19).
10. **KO: the death puff sits 1 m behind the Bison.** RPC_dead instantiates `deadEffect` at `position - forward`
    (:41213), not at the hero (the Penguin's and the Bat's are at the hero). Resting Glory (#261) heals teammates on
    death (:41233-41248, RPC_restingGlory :7841-7902): numbers on others, nothing drawn on the Bison.

---

## The dispatcher: Normal Attack stage times (SEQ check)

`doNormalAttack` (:4781-5150):

- **Stage 2:** `myCommand == "nAttack1"`, Combo #101 (:4864), press when `actionTime + 0.3 < now < actionTime + 0.7`
  (:4874, :4882): RPC_nAttack2 (:4890).
- **Stage 3 or the spin:** `myCommand == "nAttack2"`, #102 (:4924), press after `actionTime + 1` (:4934). With #103 the
  roll `num = 25 + 5 x getImprovedSwingLv()` (:4947-4953), +15 with #104 (:4959); `Random.Range(0, 100) <= lckAdjust(num)`
  (:4977) starts RPC_nAttack4 (:4983), else RPC_nAttack3 (:5004). Max rank: 55, so 56 % (Read this first 2).
- **Added Swing (#401, a passive, so ON):** `myCommand` nAttack3 or nAttack4 (:5034, :5040), #401 (:5049), press after
  `actionTime + 2` (:5059): RPC_nAttack5 (:5067), no roll.
- **A stored Hold Charge** replaces stage 1: from standby or run, `holdCharge` with sValue >= 2 starts RPC_cAttack2
  with that count (:5089-5120).
- **actionTime is set only by stage 1** (its entry :15113; the later stages' entries set actionState / myCommand only:
  :15933-15936, :16744-16747, :17852-17855, :18949-18974). So each clip starts at a fixed time after stage 1:
  - RPC_nAttack2: `Yield(2, actionTime - now + 0.7)` (:15947): **0.7 s**;
  - RPC_nAttack3 / RPC_nAttack4: `Yield(2, actionTime - now + 1.4)` (:16761, :17871): **1.4 s**;
  - RPC_nAttack5: `+ 2.2` when it follows nAttack3 (:18949 -> :19016), `+ 2.7` when it follows nAttack4 (:18967 -> :19022).
- The press windows close at each stage's standby (only while `myCommand` is still that stage's): stage 1 at 0.7
  (:15045-15068), stage 2 at 0.7 + 0.8 = 1.5 (:15868-15891), stage 3 at 1.4 + 0.9 = 2.3 (:16679-16702), the spin at
  1.4 + 1.5 = 2.9 (:17787-17810). So every press lands before its clip time and the clip times above hold.
- TTO1102 is the same dispatcher: 0.3 / 0.7 (`Bison::doNormalAttack` pseudo/Bison.c:21837, :21842), #101-104 and
  Improved Swing 232-234 with `lckAdjust` (:21831-21932), Added Swing #401 after +2 (:22031-22037). The TTO pseudo-C
  drops the float arguments of the stages' `Waits__Get` calls, but each stage has the same number of waits as BB's
  (nAttack1 3, nAttack2 4, nAttack3 5, nAttack4 6, nAttack5 6; :7862-12041) and the same voice loads (:7957, :8655, :9358, :10088, :11119).

Step lengths: nAttack1 0 -> 0.7, nAttack2 0.7 -> 1.4, then **nAttack4 1.4 -> 2.7 (56 %) or nAttack3 1.4 -> 2.2 (44 %)**,
then nAttack5 played to its clip's end (1.8 s; standby comes at 1.3, :18884-18907). Fades: nAttack1 0.2 s (:15128: the
page's first-step fade is the game's here), nAttack2 / 3 / 4 cut (:15383, :16175, :16983), nAttack5 0.3 s (:18991).

**Proposed SEQ:** `"Normal Attack: nAttack1@0.7 nAttack2@0.7 nAttack4@1.3%56|nAttack3@0.8 nAttack5~0.3"` (needs P1
and P2 of "Parts needed"). The cue entries are per clip, so they follow whichever stage the roll picks.

## The dispatcher: Charge Attack (SEQ check)

- `doBeginCharge` (:5169-5304): from standby or run (:5203-5209); with Over Power on and Over Swing #273 it starts
  Over Swing instead (:5227-5280, another report); else Charge Attack #111 (:5282), not within 0.1 s of the last action
  (:5288): RPC_cAttack1 (:5294).
- `doReleaseCharge` (:5323-5467): while `actionState "attack"` and `myCommand "cAttack1"` (:5354-5360), in a mission or
  arena (`mGameType > 4` :5366), after 2 s (:5372): `num = floor(clamp(t, 2, 4 + (#112 ? 4 : 0)))` (:5378), 8 at a full
  charge. Then:
  - with Hold Charge #113 (:5388): `RPC_AddStatus("holdCharge", 1, chaAdjust(3 + ControlledSwingLv) + floor(clamp(t - 8, 0, 12)) x SolidHoldLv, num)`
    (:5400-5405) and RPC_cAttack0 (:5411);
  - without it: RPC_cAttack2(num) (:5433);
  - released before 2 s: RPC_cAttack0 (:5455).
- RPC_cAttack0 (`$RPC_cAttack0$21115`, :20554-20733): `myCommand "cAttack0"` (:20708), `CrossFade("root", 0.2)` (:20717),
  `Yield(2, 0.2)` (:20731) -> standby (:20672). No voice, no effect.
- TTO1102 the same: `<RPC_cAttack1>d__131::MoveNext` waits 0.8 (pseudo/Bison.c:949) and 1.2 (:610), cAttack2 with 0.2
  fade (:601), cAttack1 cut (:775), `hasSkill(0x71 = 113)` for the voice (:796); `doReleaseCharge` checks 0x71 too
  (:22519); `<RPC_cAttack0>d__133` root crossfade 0.2 (:488), wait 0.2 (:493); `<RPC_cAttack2>d__132` per-hit wait
  `0.2 - 0.033 x lv` (:1124), the final 0.2 (:1569), voices by 0xe8 / 0xe7 (:1252-1255), Spin Hack 0x1b0 (:1516), the
  same effect and sound strings (:1047-1070, :561-576).

**Proposed SEQ** (Hold Charge on, question 1): `"Charge Attack: cAttack1@0.8 cAttack2*~@7.2 root~@0.2 cAttack6*@1.816"`.
- cAttack1 is a cut in the game (`PlayAnimation("cAttack1", 0)` :19419); the page fades a first step 0.2 s unless it is
  written `cAttack1!@0.8` (the Sheep, Penguin and Bat kept the fade: question 6).
- cAttack2's `~` = `PlayAnimation("cAttack2", 0.2f)` (:19284); `root~@0.2` = RPC_cAttack0's crossfade and standby;
  cAttack6 cut in (:20358), looped (:20364).
- `@7.2`: the full 8 s charge from cAttack1's start (rank 2 = 8 hits; the page's NOTES "Bison 8 s then 8 hits").
- `@1.816`: 0.202 x 8 + 0.2. It parses (`[\d.]+`, index.html:1229).

---

## nAttack1 (Normal Attack, stage 1)

Coroutine `RPC_nAttack1` (`$RPC_nAttack1$20924`, :14466-15265).

| t (s) | what | source |
|---|---|---|
| 0 | `actionState "attack"`, `actionTime`, `myCommand "nAttack1"`, `addTimeOut("nAttack", 1.5)`, clip nAttack1 (0.2 s fade), moveSpeed 1; wait 0.3 | :15110-15137, `Yield(2, 0.3)` :15152 |
| 0.3 | voice `Voices/nAttack1` (own hero or a mission teammate, :14594-14620; 1.0 own, 0.75 others); with `w_bsn59` (Vacuum Hammer) the 6 m pull, nothing drawn (:14661-14712); wait 0.2 | load :14629, PlayOneShot :14641, `Yield(3, 0.2)` :15163 |
| 0.5 | the hit: `FindAngleTarget(pos - 0.5 fwd, fwd, 5, 35 deg, 2)` (:14801); on a hit, `nAttack_hit` at the enemy (:14850) and the axe / hammer hit sound (:7112-7138), Over Pride's voice (:14907): none at the 10 m target point; wait 0.2 | `Yield(4, 0.2)` :15157 |
| 0.7 | standby, unless stage 2 was pressed (`myCommand == "nAttack1"`) | :15045-15068 |

```json
  "nAttack1": {
    "why": "Bison.cs RPC_nAttack1 (:14466-15265): clip at 0 (0.2 s fade, :15128); 0.3 s (Yield(2, 0.3) :15152) voice nAttack1 (load :14629, PlayOneShot :14641); the hit at 0.5 s (Yield(3, 0.2) :15163) is melee, 5 m (FindAngleTarget :14801): nothing at the 10 m target point (nAttack_hit at the enemy :14850, the axe / hammer hit sound :7112-7138 and Over Pride's voice :14907 only on a hit, left out as the Wolf's); standby 0.7 s (Yield(4, 0.2) :15157, :15045-15068) unless stage 2 is pressed (its clip starts at 0.7 s: :15947)",
    "cues": [
    [0.3, "voice", "nAttack1"]
    ]
  },
```

## nAttack2 (stage 2)

Coroutine `RPC_nAttack2` (`$RPC_nAttack2$20955`, :15266-15960); its clip starts 0.7 s after stage 1 (:15947).

| t (s, from its clip) | what | source |
|---|---|---|
| 0 | clip nAttack2 (cut), LookAt, moveSpeed 2, `addTimeOut("nAttack", 1.5)`; wait 0.3 | :15383-15408, `Yield(3, 0.3)` :15951 |
| 0.3 | voice `Voices/nAttack2` (:15427-15474); the w_bsn59 pull (:15494-15546); wait 0.2 | load :15462, PlayOneShot :15474, `Yield(4, 0.2)` :15953 |
| 0.5 | the hit: `FindRecTarget(..., 1, 2, 5, 2)` (:15607); nothing at 10 m (:15673, :15730); wait 0.3 | `Yield(5, 0.3)` :15945 |
| 0.8 | standby, unless stage 3 was pressed | :15868-15891 |

```json
  "nAttack2": {
    "why": "Bison.cs RPC_nAttack2 (:15266-15960; its clip 0.7 s after stage 1: Yield(2, actionTime - now + 0.7) :15947, the press window 0.3-0.7 s, doNormalAttack :4874-4890): clip at 0 (cut, :15383); 0.3 s (Yield(3, 0.3) :15951) voice nAttack2 (load :15462, PlayOneShot :15474); the hit at 0.5 s (Yield(4, 0.2) :15953) is melee, 5 m (FindRecTarget :15607): nothing at the 10 m target point (nAttack_hit :15673 and Over Pride :15730 only on a hit); standby 0.8 s (Yield(5, 0.3) :15945, :15868-15891) unless stage 3 / the spin is pressed (from 1.0 s after stage 1, :4934)",
    "cues": [
    [0.3, "voice", "nAttack2"]
    ]
  },
```

## nAttack3 (stage 3, 44 % at max rank)

Coroutine `RPC_nAttack3` (`$RPC_nAttack3$20984`, :16058-16779); its clip starts 1.4 s after stage 1 (:16761).

| t (s, from its clip) | what | source |
|---|---|---|
| 0 | clip nAttack3 (cut), LookAt, moveSpeed 0, `addTimeOut`; wait 0.1 | :16175-16200, `Yield(3, 0.1)` :16767 |
| 0.1 | moveSpeed 4, voice `Voices/nAttack3` (:16219-16273); wait 0.3 | load :16261, PlayOneShot :16774, `Yield(4, 0.3)` :16757 |
| 0.4 | the w_bsn59 pull (:16297-16361); wait 0.2 | `Yield(5, 0.2)` :16769 |
| 0.6 | moveSpeed 0, the hit: `FindRecTarget(..., 1, 1.5, 4, 3)` (:16418); nothing at 10 m (:16484, :16541); wait 0.3 | `Yield(6, 0.3)` :16765 |
| 0.9 | standby, unless Added Swing was pressed | :16679-16702 |

```json
  "nAttack3": {
    "why": "Bison.cs RPC_nAttack3 (:16058-16779; its clip 1.4 s after stage 1: Yield(2, actionTime - now + 1.4) :16761; started instead of the spin on 44 % of presses at max rank: Random.Range(0, 100) <= lckAdjust(25 + 5 x 3 + 15) fails, :4947-5004): clip at 0 (cut, :16175); 0.1 s (Yield(3, 0.1) :16767) voice nAttack3 (load :16261, PlayOneShot :16774); the hit at 0.6 s (Yield(4, 0.3) :16757, Yield(5, 0.2) :16769) is melee, 4 m (FindRecTarget :16418): nothing at the 10 m target point (nAttack_hit :16484, Over Pride :16541 only on a hit); standby 0.9 s (Yield(6, 0.3) :16765, :16679-16702) unless Added Swing #401 is pressed (its clip 2.2 s after stage 1, :19016)",
    "cues": [
    [0.1, "voice", "nAttack3"]
    ]
  },
```

## nAttack4 (the spin, 56 % at max rank)

Coroutine `RPC_nAttack4` (`$RPC_nAttack4$21013`, :16850-17894); its clip starts 1.4 s after stage 1 (:17871).

| t (s, from its clip) | what | source |
|---|---|---|
| 0 | clip nAttack4 (cut), `addTimeOut`; wait 0.3 | :16983-16993, `Yield(3, 0.3)` :17867 |
| 0.3 | voice `Voices/nAttack4` (:17012-17061); wait 0.2 | load :17049, PlayOneShot :17873, `Yield(4, 0.2)` :17880 |
| 0.5 | the w_bsn59 pull (:17085-17147); wait 0.2 | `Yield(5, 0.2)` :17891 |
| 0.7 | moveSpeed 5, hit 1: `FindAreaTarget(pos, 5, 3)` (:17216); nothing at 10 m (:17272, :17339); wait 0.3 | `Yield(6, 0.3)` :17886 |
| 1.0 | moveSpeed 0, hit 2: `FindAreaTarget(pos, 6, 3)` (:17506); on a hit only (:17615), Over Pride (:17629) and `hammer_hit1` / `axe_hit1` by `isHammer()` (:17763-17778); wait 0.5 | `Yield(7, 0.5)` :17863 |
| 1.5 | standby, unless Added Swing was pressed | :17787-17810 |

```json
  "nAttack4": {
    "why": "Bison.cs RPC_nAttack4 (:16850-17894; the spin, started in place of stage 3 on 56 % of presses at max rank: Combo #103 / #104 with Improved Swing 3, Random.Range(0, 100) <= lckAdjust(55) = 55 at LCK 1, :4947-4983, CharacterControl.cs:20658-20670; its clip 1.4 s after stage 1: Yield(2, actionTime - now + 1.4) :17871): clip at 0 (cut, :16983); 0.3 s (Yield(3, 0.3) :17867) voice nAttack4 (load :17049, PlayOneShot :17873); hits at 0.7 s and 1.0 s (Yield(4, 0.2) :17880, Yield(5, 0.2) :17891, Yield(6, 0.3) :17886) are 5 / 6 m circles (FindAreaTarget :17216, :17506): nothing at the 10 m target point (nAttack_hit at the enemy + 1.5 up :17272 / :17562, Over Pride :17339 / :17629 and the hammer_hit1 / axe_hit1 sound :17763-17778 only on a hit); standby 1.5 s (Yield(7, 0.5) :17863, :17787-17810) unless Added Swing #401 is pressed (its clip 2.7 s after stage 1, :19022)",
    "cues": [
    [0.3, "voice", "nAttack4"]
    ]
  },
```

## nAttack5 (Added Swing #401)

Coroutine `RPC_nAttack5` (`$RPC_nAttack5$21048`, :18017-19032).

| t (s, from its clip) | what | source |
|---|---|---|
| 0 | clip nAttack5 (**0.3 s fade**), `addTimeOut`; wait 0.3 | IL_54F :18981-18998, `Yield(4, 0.3)` :19028 |
| 0.3 | voice `Voices/nAttack5` (:18123-18174); the w_bsn59 pull (:18182-18244); wait 0.2 | load :18158, PlayOneShot :18170, `Yield(5, 0.2)` :19030 |
| 0.5 | moveSpeed 5, hit 1: `FindAreaTarget(pos, 5, 3)` (:18313); nothing at 10 m; wait 0.3 | `Yield(6, 0.3)` :19007 |
| 0.8 | moveSpeed 0, hit 2: `FindAreaTarget(pos, 6, 3)` (:18603); on a hit only, the hammer / axe hit sound (:18860-18875); wait 0.5 | `Yield(7, 0.5)` :19014 |
| 1.3 | standby | :18884-18907 |

- Clip start: 2.2 s after stage 1 after nAttack3 (`Yield(2, actionTime - now + 2.2)` :19016), 2.7 s after the spin
  (`Yield(3, ... + 2.7)` :19022); case 2 and 3 both go to IL_54F (:18108-18111).

```json
  "nAttack5": {
    "why": "Bison.cs RPC_nAttack5 (:18017-19032; Added Swing #401, a passive, on; its clip 2.2 s after stage 1 after nAttack3, Yield(2, actionTime - now + 2.2) :19016, 2.7 s after the spin, Yield(3, actionTime - now + 2.7) :19022): clip at 0 (0.3 s fade, :18991); 0.3 s (Yield(4, 0.3) :19028) voice nAttack5 (load :18158, PlayOneShot :18170); hits at 0.5 s and 0.8 s (Yield(5, 0.2) :19030, Yield(6, 0.3) :19007) are 5 / 6 m circles (FindAreaTarget :18313, :18603): nothing at the 10 m target point (nAttack_hit :18369 / :18659, Over Pride :18436 / :18726 and the hammer_hit1 / axe_hit1 sound :18860-18875 only on a hit); standby 1.3 s (Yield(7, 0.5) :19014, :18884-18907)",
    "cues": [
    [0.3, "voice", "nAttack5"]
    ]
  },
```

Sure: high on every time (each wait read off the resolved labels). The 56 % assumes the page's LCK 1 (the Penguin's and
the Bat's convention for lckAdjust).

---

## cAttack1 (Charge Attack: the wind-up)

Coroutine `RPC_cAttack1` (`$RPC_cAttack1$21083`, :19151-19622).

| t (s) | what | source |
|---|---|---|
| 0 | `actionState "attack"`, `actionTime`, `myCommand "cAttack1"`, clip cAttack1 (cut), `removeStatus("holdCharge")`; voice (own hero or a mission teammate :19428-19450): with Hold Charge #113 `holdCharge1` (`Random.Range(0, 2) == 1`) or `holdCharge2`, without it `cAttack1` / `cAttack2` (the same roll); wait 0.8 | :19401-19425; #113 :19457, roll :19461, loads :19471 / :19502, PlayOneShot :19600 / :19613; without :19526-19610; `Yield(2, 0.8)` :19608 |
| 0.8 | still charging: clip cAttack2 (0.2 s fade, looped); wait 1.2 | :19267-19289, `Yield(3, 1.2)` :19617 |
| 2.0 | still charging and `mGameType > 4` (:19308): `cAttack1_dust` at the hero + 0.15 up, hero rotation; Solid Hold #411 (`getSolidChangeLv` :9040-9042): `solidCharge_ring` at the hero | :19314-19332, :19346-19370 |

```json
  "cAttack1": {
    "why": "Bison.cs RPC_cAttack1 (:19151-19622): clip at 0 (cut, :19419) and the voice at 0, Hold Charge #113 on (passives rule): holdCharge1 / holdCharge2 (Random.Range(0, 2) == 1, :19457-19613; without it cAttack1 / cAttack2, :19526-19610; TTO1102 the same, pseudo/Bison.c:796); at 0.8 s (Yield(2, 0.8) :19608) it changes to the looped cAttack2 (0.2 s fade, :19284-19289), whose entry holds the dust and the ring",
    "cues": [
    [0, "voice", "holdCharge1|holdCharge2"]
    ]
  },
```

## cAttack2 (Charge Attack: the held charge)

Same coroutine, case 2 / 3, cAttack2 from 0.8 s after cAttack1.

- At 1.2 s into cAttack2 (2.0 s into the charge): `cAttack1_dust` and `solidCharge_ring` (table above).
- `cAttack1_dust` (probe): EllipsoidParticleEmitter (one-shot, 20 particles, rndVelocity 5 x 5), EffectControl life 60,
  **followState**, followPosition; its AudioSource plays `sounds/cAttack1` on awake, **looped** (the charge's hum).
- `solidCharge_ring` (probe): EffectControl life 99, **followState**, followPosition; one RingEmitter.
- **The followState cut:** the release changes `myCommand` (RPC_cAttack0 :20708 with Hold Charge, RPC_cAttack2 :20122
  without), and EffectControl ends a followState effect on that change (the Sheep's / Penguin's EffectControl check). The
  step ends at 7.2 s, so the cut is **7.15** (the Penguin's 2.95 under a 3 s hold).

```json
  "cAttack2": {
    "why": "Bison.cs RPC_cAttack1 cases 2-3 (the change to cAttack2, looped, 0.8 s into the charge: :19267-19289; Yield(3, 1.2) :19617): at 1.2 s, still charging, mission / arena only (mGameType > 4, :19308; the Sheep's precedent keeps them): cAttack1_dust at the hero + 0.15 up with the hero's rotation (:19320-19332; plays its own looping Sounds/cAttack1) and, Solid Hold #411 on (passives rule, getSolidChangeLv :9040-9042, :19346), solidCharge_ring at the hero (:19358-19370); both followState: they end at the release after the full 8 s charge (rank 2, clamp(t, 2, 8) :5378), when RPC_cAttack0 sets myCommand cAttack0 (:20708; RPC_cAttack2's cAttack2 without Hold Charge, :20122): cut 7.15, the page's step ends at 7.2 s",
    "cues": [
    [1.2, "fx", "cAttack1_dust", {"y": 0.15, "cut": 7.15}],
    [1.2, "fx", "solidCharge_ring", {"cut": 7.15}]
    ]
  },
```

## @ChargeAttack:root (the release with Hold Charge: RPC_cAttack0 and the stored charge)

- At the release (8 s): `doReleaseCharge` gives the Bison `holdCharge` (sValue 8) and starts RPC_cAttack0 in the same
  frame (:5400-5411). RPC_cAttack0 crossfades to root over 0.2 s and stands by 0.2 s later (:20708-20731).
- The status's look (CharacterControl.cs status apply, `case "holdCharge"` :34666-34708):
  - `holdCharge_ring` Instantiated at the hero's position with `Quaternion.identity` (:34670). Probe: EffectControl life 1,
    no follow; three RingEmitters and a VortexEmitter; it plays its own `sounds/holdCharge_ring`. (Identity = the hero's
    own rotation on the page's unturned hero; the rings are round either way.)
  - `holdCharge` Instantiated and parented to the hero, local position 0, named `holdChargeFx` (:34673-34702). Probe:
    an EllipsoidParticleEmitter, EffectControl life 60, no follow. It goes when the status is removed (CharacterControl.cs:15390-15403),
    i.e. when the next press's RPC_cAttack2 spends it (:20263-20269): `kill` 0.2 (the press at standby).
- Its status time would be `chaAdjust(3 + 1)` + 0 (an 8 s charge adds `floor(clamp(8 - 8, 0, 12))` = 0, :5383, :5400).

```json
  "@ChargeAttack:root": {
    "why": "the release with Hold Charge #113 on (passives rule): Bison.cs doReleaseCharge (:5323-5467): after the full charge (>= 2 s, :5372; 8 hits, :5378) RPC_AddStatus(holdCharge, 1, chaAdjust(3 + ControlledSwingLv) + 0, 8) (:5400-5405) and RPC_cAttack0 (:5411) instead of the spin: myCommand cAttack0 (:20708), CrossFade(root, 0.2) (:20717), standby 0.2 s later (Yield(2, 0.2) :20731, :20672); the status's look (CharacterControl.cs:34666-34708): holdCharge_ring at the hero, Quaternion.identity (:34670; plays its own Sounds/holdCharge_ring) and holdCharge parented to the hero (:34673-34702), removed when the next attack press spends the status (doNormalAttack's holdCharge branch :5089-5120 -> RPC_cAttack2 removeStatus :20263-20269 -> CharacterControl.cs:15390-15403): kill 0.2, the press right at standby",
    "cues": [
    [0, "fx", "holdCharge_ring"],
    [0, "fx", "holdCharge", {"kill": 0.2}]
    ]
  },
```

## cAttack6 (the spin: Improved Swing 3)

Coroutine `RPC_cAttack2` (`$RPC_cAttack2$21090`, :19651-20474), with 8 hits (the stored sValue, or the release's count).

| t (s, from cAttack6) | what | source |
|---|---|---|
| 0 | levels cached (:20107-20116), `myCommand "cAttack2"`, `actionTime` (:20119-20125); voice (own or mission teammate, :20131-20153): Improved Swing #232 -> `improvedSwing` (else #231 `controlledSwing`, else `axelSwing`); with the `holdCharge` status: removed and `holdCharge_fire` at the hero (hero rotation); clip by Improved Swing level: **cAttack6** (cut), looped, moveSpeed 3; `cAttack2_dust` at the hero + 0.15 up; Spin Hack #432: `spinHack_ring` at the hero | voices :20160-20254; :20263-20292; switch :20313-20364, :20370; :20379-20391; :20405-20429 |
| 0, 0.202, ..., 1.414 | hit k (k = 0..7): `Sounds/cAttack2` (:19917-19929), the scan `FindAreaTarget(pos, 5 + 2, 3)` (:20016-20021; nAttack_hit at the enemy + 1.5 up only on a hit, :20060); wait w = 0.2 - 0.033 x 3 = 0.101 | IL_1019 :19892-20104, `Yield(2, w)` :20464 |
| 0.101, ..., 1.515 | `Sounds/cAttack2` again (case 2, :19779-19803); wait w | `Yield(3, w)` :20468; case 3 `i++` :19816 |
| 1.616 | `i >= 8` (:19893): wait 0.2 | `Yield(4, 0.2)` :20466 |
| 1.816 | standby (if still `"cAttack2"`) | :19822-19850 |

- Probe: `holdCharge_fire` EffectControl life 1, followPosition, no followState; a RingEmitter and a VortexEmitter; its
  own `sounds/holdCharge_fire`. `cAttack2_dust` EffectControl life 60, **followState**, followPosition. `spinHack_ring`
  EffectControl life 12, **followState**, followPosition; two RingEmitters (0.05 and 1.5 m up).
- **The followState cut:** standby at 1.816 changes `actionState` and `myCommand` (:19840-19850): cut **1.766** for the
  dust and the ring (the step ends at 1.816).
- `Sounds/cAttack2` is played with PlayOneShot(clip), volume 1 (:19798, :19929): 16 `"sound"` cues 0.101 s apart.

```json
  "cAttack6": {
    "why": "Bison.cs RPC_cAttack2 (:19651-20474), 8 hits (the stored Hold Charge, doNormalAttack :5089-5120, or the release's count :5378-5446): at 0 voice improvedSwing (Improved Swing #232 on, :20160-20184; controlledSwing / axelSwing only without it, :20195-20250), the holdCharge status spent: removeStatus and holdCharge_fire at the hero with its rotation (:20263-20292; plays its own Sounds/holdCharge_fire; only with Hold Charge #113), clip cAttack6 by Improved Swing 3 (cut, looped: :20313-20364), cAttack2_dust at the hero + 0.15 up (:20379-20391) and, Spin Hack #432 on, spinHack_ring at the hero (:20405-20429), both followState: cut 1.766 at the standby 1.816 s (:19822-19850); each hit k = 0..7 at 0.202 k plays Sounds/cAttack2 (IL_1019 :19917-19929), waits w = 0.2 - 0.033 x 3 = 0.101 (:20464), plays it again (case 2 :19786-19798), waits w (:20468): 16 swishes 0.101 s apart; after the 8th, Yield(4, 0.2) (:20466) -> standby 1.816 s; the hits are 7 m circles (FindAreaTarget :20016-20021): nothing at the 10 m target point (nAttack_hit at the enemy + 1.5 up :20060 only on a hit)",
    "cues": [
    [0, "voice", "improvedSwing"],
    [0, "fx", "holdCharge_fire"],
    [0, "fx", "cAttack2_dust", {"y": 0.15, "cut": 1.766}],
    [0, "fx", "spinHack_ring", {"cut": 1.766}],
    [0, "sound", "cAttack2"],
    [0.101, "sound", "cAttack2"],
    [0.202, "sound", "cAttack2"],
    [0.303, "sound", "cAttack2"],
    [0.404, "sound", "cAttack2"],
    [0.505, "sound", "cAttack2"],
    [0.606, "sound", "cAttack2"],
    [0.707, "sound", "cAttack2"],
    [0.808, "sound", "cAttack2"],
    [0.909, "sound", "cAttack2"],
    [1.01, "sound", "cAttack2"],
    [1.111, "sound", "cAttack2"],
    [1.212, "sound", "cAttack2"],
    [1.313, "sound", "cAttack2"],
    [1.414, "sound", "cAttack2"],
    [1.515, "sound", "cAttack2"]
    ]
  },
```

Variant without Hold Charge (question 1, not the recommendation): SEQ `"Charge Attack: cAttack1@0.8 cAttack2*~@7.2 cAttack6*@1.816"`,
no `@ChargeAttack:root` entry, `cAttack1`'s voice `"cAttack1|cAttack2"` (:19526-19610), and `cAttack6` without the
`holdCharge_fire` cue (the status is absent, :20263). Every other cue stays.

cAttack3-5 (lower Improved Swing ranks, `LOWER_RANK`) get no entries: the page never plays them.

Sure: high on the trace and the times; the press right at standby is a choice (the earliest the game allows).

---

## Emotes and basic moves

`RPC_emotion` (`$RPC_emotion$21442`, :34554-35376), as the Wolf's, Sheep's, Penguin's and Bat's:
- The voice at 0, **before** the clip (:34739-34817). Gates: the voice option on (:34739), more than 2 s since the last
  action (:34745), the own hero, a mission teammate, or game code 31 (:34751-34773).
- `emo_chat` -> `Voices/chat` + `Random.Range(1, 6)` = chat1-5 (:34797); every other `emo_<name>` -> `Voices/<name>`
  (`Substring(4)`, :34805), `PlayOneShot` volume 1 (:34817), only if the file loads (:34811).
- Then `actionState "emotion"` and the clip, 0.2 s fade (:34836-35312). No effect, no Sounds/.

| emote | clip | voice file | source |
|---|---|---|---|
| emo_hi, emo_wave | wave | hi / wave | :34871, :34878 -> :35312 |
| emo_ty, emo_bow | bow | ty / bow | :34887, :34894 -> :35305 |
| emo_laugh | laugh | **none: the Bison has no voices/laugh** (`rip_list.txt`) | :34901-34907 |
| emo_sit | sit | none | :34921-34927 |
| emo_sleep | sleep | sleep | :34933-34939 |
| emo_cheer | cheer | cheer | :34945-34951 |
| emo_beg | beg | beg | :34957-34963 |
| emo_cry | cry | cry | :34969-34975 |
| emo_talk, emo_chat | talk | talk: none; chat: chat1-5 | :34983, :34990 -> :35283 |
| emo_pose | pose5 / 15 / 25 / 35 / 45 / 58 / 65 / 46 / 66 by the worn set (w_bsn56 + c_all56: `animation.Stop()`), else pose | none | :34997-35245 |
| emo_battle | battle | battle | :35253-35259 |
| emo_dance | dance | none | :35268-35276 |

- wave / bow / laugh play once (`WrapMode.Once` :35318) and stand by at 1.2 s (`Yield(4, 1.2)` :35372); the rest loop
  until the player moves (:35290, :35324-35358).
- TTO-only emote clips in `clips.json` (clap, wai, cooking, mining, planting, fishingBison, pose37): no BB code plays them.
  TTO voices clap with `cheer` and wai with `ty|bow` (the Bat's finding, BaseHero.c:16190-16224). Left silent (question 5).
- **Basic moves:** `run` steps at 0.1 and 0.6 s of every cycle (Read this first 8). getUp, falling, root: nothing (no
  AnimationEvent: `probe_events.txt` lists only run). The Bison has no walk clip.
- **KO:**
  - `RPC_ko` (`$RPC_ko$21611`, :40519-40863): clip ko (cut, :40733), voice ko1 / ko2 at 0 (`Random.Range(0, 2)` :40768;
    loads :40778 / :40809; PlayOneShot :40849 / :40859); getUp after 3 s (`Yield(2, 3)` :40847 -> :40635), standby 1 s
    later (`Yield(3, 1)` :40854 -> :40659). No effect.
  - `RPC_dead` (`$RPC_dead$21618`, :40895-41281): Rewind + clip ko (:41089-41092); voice dead1 / dead2 at 0
    (:41127-41182); then **always** `Instantiate(deadEffect, position - forward, rotation)` (:41194-41213: the voice gates
    jump to IL_3F4, which is the effect). Then Resting Glory #261 (:41233-41248) heals the teammates (RPC_restingGlory
    :7841-7902, the Bison skipped): nothing drawn on the Bison.
  - `deadEffect` (probe): EffectControl life 3, no follow; an ImageEmitter 1 m up and two LineEmitters 0.1 m up. Ready.
  - Sheep decision 11: one of the two at random, even chance, each with its voices (the Wolf's and the Penguin's entry),
    the effect **1 m behind** (`d: -1`).

```json
  "wave": {
    "why": "Bison.cs RPC_emotion (:34554): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:34805, PlayOneShot :34817; the rip has hi, wave, ty, bow, sleep, cheer, beg, cry, battle, chat1-5, no laugh); no effect, no sound; emo_hi (:34871) and emo_wave (:34878) both play the wave clip (:35312): voice hi or wave",
    "cues": [
    [0, "voice", "hi|wave"]
    ]
  },
  "bow": {
    "why": "Bison.cs RPC_emotion (:34554): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:34805, PlayOneShot :34817; the rip has hi, wave, ty, bow, sleep, cheer, beg, cry, battle, chat1-5, no laugh); no effect, no sound; emo_ty (:34887) and emo_bow (:34894) both play the bow clip (:35305): voice ty or bow",
    "cues": [
    [0, "voice", "ty|bow"]
    ]
  },
  "sleep": {
    "why": "Bison.cs RPC_emotion (:34554): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:34805, PlayOneShot :34817; the rip has hi, wave, ty, bow, sleep, cheer, beg, cry, battle, chat1-5, no laugh); no effect, no sound; emo_sleep (:34933-34939)",
    "cues": [
    [0, "voice", "sleep"]
    ]
  },
  "cheer": {
    "why": "Bison.cs RPC_emotion (:34554): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:34805, PlayOneShot :34817; the rip has hi, wave, ty, bow, sleep, cheer, beg, cry, battle, chat1-5, no laugh); no effect, no sound; emo_cheer (:34945-34951)",
    "cues": [
    [0, "voice", "cheer"]
    ]
  },
  "beg": {
    "why": "Bison.cs RPC_emotion (:34554): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:34805, PlayOneShot :34817; the rip has hi, wave, ty, bow, sleep, cheer, beg, cry, battle, chat1-5, no laugh); no effect, no sound; emo_beg (:34957-34963)",
    "cues": [
    [0, "voice", "beg"]
    ]
  },
  "cry": {
    "why": "Bison.cs RPC_emotion (:34554): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:34805, PlayOneShot :34817; the rip has hi, wave, ty, bow, sleep, cheer, beg, cry, battle, chat1-5, no laugh); no effect, no sound; emo_cry (:34969-34975)",
    "cues": [
    [0, "voice", "cry"]
    ]
  },
  "talk": {
    "why": "Bison.cs RPC_emotion (:34554): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:34805, PlayOneShot :34817; the rip has hi, wave, ty, bow, sleep, cheer, beg, cry, battle, chat1-5, no laugh); no effect, no sound; emo_chat (:34990) plays the talk clip (:35283) with chat1-5 at random (Random.Range(1, 6), :34797); emo_talk (:34983) plays it silent (no Voices/talk): the tile takes the chat's voice",
    "cues": [
    [0, "voice", "chat1|chat2|chat3|chat4|chat5"]
    ]
  },
  "battle": {
    "why": "Bison.cs RPC_emotion (:34554): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:34805, PlayOneShot :34817; the rip has hi, wave, ty, bow, sleep, cheer, beg, cry, battle, chat1-5, no laugh); no effect, no sound; emo_battle (:35253-35259): voice battle; the fight stance and RPC_activateIcon1 (:40354) play the clip without it: the tile takes the emote's voice",
    "cues": [
    [0, "voice", "battle"]
    ]
  },
  "run": {
    "why": "the run clip's AnimationEvents playLeftFootEvent at 0.1 s and playRightFootEvent at 0.6 s (checks/fx_bison_research/attacks_emotes/probe_events.txt) -> Bison.cs playLeftFootEvent / playRightFootEvent (:124-178): the hero's audio.PlayOneShot(footStep_left / footStep_right) = step_heavy1 / step_heavy2 (the prefab's fields, probe_fields.txt; Resources/sound/fx/step_heavy1.wav, step_heavy2.wav), own hero or anyone in a mission (mGameType > 4, :131-139, :160-168); every cycle of the run (the event fires each loop: everyCycle, the Bat's page flag)",
    "everyCycle": true,
    "cues": [
    [0.1, "sound", "step_heavy1"],
    [0.6, "sound", "step_heavy2"]
    ]
  },
  "ko": {
    "why": "Bison.cs RPC_ko (:40519): clip (PlayAnimation :40733) and voice ko1 or ko2 at 0 (Random.Range(0, 2) :40768, :40778-40859), getUp after 3 s (:40847, :40635), no effect; RPC_dead (:40895) plays the same clip (:41092) with dead1 or dead2 at 0 (:41127-41182) and always puts deadEffect 1 m behind the hero with its rotation (Instantiate at position - forward :41213; EffectControl life 3); Resting Glory's heal goes to the teammates only (:41233-41248, :7841-7902): one of the two at random, even chance (the Sheep's decision 11, as wolf.json: roll dead, its voices with it; '!dead' = RPC_ko's)",
    "cues": [
    [0, "voice", "ko1|ko2", {"p": 0.5, "roll": "!dead"}],
    [0, "voice", "dead1|dead2", {"p": 0.5, "roll": "dead"}],
    [0, "fx", "deadEffect", {"d": -1, "p": 0.5, "roll": "dead"}]
    ]
  }
```

---

## Parts needed (build stage)

No effect part: every effect cued here is ready (Read this first 4). Page and build parts:

- **P1. A random step in a sequence** (Normal Attack's third stage). The SEQ token regex (`index.html:1229`) has no
  choice. Proposed syntax: a token with `|` = alternatives, each with its own fades / `@t`; `%p` after the first = its
  chance in percent (else even), drawn when the sequence starts (step 0), kept for the play:
  `nAttack4@1.3%56|nAttack3@0.8`. `chains()` stores the alternatives on the step; `startStep` picks; `moveText` shows
  "nAttack4 / nAttack3". `chains()`' every-clip-exists filter checks every alternative.
- **P2. A crossfade of any length** (nAttack5's 0.3 s, :18991): `~0.3` after the clip name (`~` alone stays 0.2):
  regex `^(\w+)(\*)?(?:([~^!])([\d.]+)?)?(?:@([\d.]+))?$`.
- **P3. The run's footsteps** (the Bat's jobs 5a / 5b, plans/fx_bat/attacks_emotes.md "Verification"): the build's
  `"sound"` lookup falling back to the rest of the rip when the class's `sounds/` has no such file (`rip_wav(cls, n,
  "sounds")`, wardrobe_fx.py:346-348, misses `Resources/sound/fx/step_heavy1.wav`), and `"everyCycle"` (re-arm the
  entry's cues each time the looping action's time wraps). Shared with the Bat; built once.
- **The SEQ lines** (index.html, `SEQ.bison`): the two proposed above, with a comment citing the lines (Normal Attack:
  :15947, :16761, :17871, :19016, :19022, :4977, :18991; Charge Attack: :19608, :5378, :5388-5411, :20717-20731,
  :20464-20468, :20466).
- **Inventory:** add `holdCharge` and `holdCharge_ring` (CharacterControl.cs:34670-34673) for the Bison
  (`wardrobe_fx_inventory.py` scans `Bison.cs` only); both are ready.

## Left out

- Everything at a hit enemy (Read this first 5): `nAttack_hit` (the prefab's field, = `heroes/bison/effects/nAttack_hit`,
  `probe_fields.txt`), `axe_hit1` / `hammer_hit1`, Over Pride's `overPride1|overPride2`, `onNormalAttackHit`'s gear
  procs, Colossal Weapon's splash damage, Berserker Rush's self-heal number.
- The Vacuum Hammer's (`w_bsn59`) pull at 0.3-0.5 s of each stage: damage and a push, nothing drawn.
- `cAttack1|cAttack2` (charge voices) and the Hold-Charge-free spin: replaced by Hold Charge (passives ON), not missing.
- `controlledSwing` / `axelSwing` voices: lower-rank alternatives to `improvedSwing`.
- Resting Glory's heal on teammates.
- Over Swing (doBeginCharge's other branch): its own skill and clip, another report.

## Open questions for the user (only what the decisions don't answer)

1. **Hold Charge on the Charge Attack tile.** With Hold Charge learned (passives ON), the game never spins on release: it
   stores the charge (back to the idle stance with a ring and a glow) and spins on the next attack press.
   - A (recommended, the passives rule): `cAttack1@0.8 cAttack2*~@7.2 root~@0.2 cAttack6*@1.816`, the press at the
     earliest moment (standby, 0.2 s after the release), with the holdCharge voices, ring, glow and holdCharge_fire.
   - B: the spin right at release (Hold Charge off): `cAttack1@0.8 cAttack2*~@7.2 cAttack6*@1.816`, voices cAttack1|cAttack2,
     no holdCharge effects.
   - C: both, as two tiles (Charge Attack without Hold Charge, Hold Charge with it). Recommended: **A**.
2. **The combo's third stage.** Recommended: **the game's roll** (56 % spin nAttack4, else nAttack3; P1), not both
   clips one after the other as today, and not always the spin.
3. **Hits.** Melee hits cannot reach the 10 m target point, so no hit sparks, hit sounds or Over Pride voice.
   Recommended: **leave them out** (the Wolf's attacks). The alternative would be an enemy 1-5 m ahead, against the
   10 m rule.
4. **The death puff 1 m behind the Bison** (`position - forward`, :41213). Recommended: **as the game** (`d: -1`).
5. **TTO-only emote clips** (clap, wai, cooking, mining, planting, fishingBison, pose37). Recommended: **silent**, as the
   Wolf, Sheep, Penguin and Bat (a cross-class follow-up with TTO's voices if wanted).
6. **The first step's fade.** nAttack1 really fades 0.2 s (:15128), so the page is right there. cAttack1 is a cut (:19419):
   recommended **keep the page's 0.2 s fade**, as the Sheep, Penguin and Bat (`cAttack1!@0.8` if the cut is wanted).
7. **The run's footsteps.** Recommended: **yes** (step_heavy1 / step_heavy2 at 0.1 / 0.6 s of every cycle, P3), as the
   Bat's wing flap.
8. **The Bison's silent laugh.** The game has no laugh voice for the Bison. Recommended: **silent, as the game** (no
   borrowed voice).

## Offer for the Bible

New or different against `bison-skill-reference.md` (Combo `:192-211`, Charge Attack `:178-190`, movement table `:491-510`):
- the combo's clip starts at 0.7 / 1.4 / 1.4 s after stage 1, and Added Swing's at **2.2 s after stage 3 but 2.7 s after
  the spin** (:19016, :19022); its hits are at +0.5 / +0.8 s of its own clip (:19028, :19030, :19007), so the table's "starts 2.2 s
  ... circles at +1.0 s and +1.3 s" fits only the spin path (2.7 + 0.5 = 2.2 + 1.0);
- the voices: 0.3 / 0.3 / 0.1 / 0.3 / 0.3 s into stages 1 / 2 / 3 / spin / Added Swing; the hits 0.5 / 0.5 / 0.6 / 0.7 + 1.0 / 0.5 + 0.8;
- the charge: cAttack2 from 0.8 s, the dust and Solid Hold's ring at 2.0 s (missions only), the spin's swish every
  `0.2 - 0.033 x lv` s (twice per hit), standby 0.2 s after the last hit;
- Hold Charge also swaps the charge voice (holdCharge1 / 2) and its release plays cAttack0 with holdCharge_ring and the
  holdCharge glow; the stored spin draws holdCharge_fire;
- RPC_dead puts deadEffect 1 m behind the Bison; the Bison has no laugh voice.

---

## Verification (2026-11-13, by the author while writing)

- Every JSON block above parses and every cued name exists: `checks\fx_bison_research\attacks_emotes\check_report.py`
  (output `check_report.txt`): voices in `heroes\bison\voices\`, effects in the probe, sounds in `heroes\bison\sounds\`
  or `sound\fx\` (step_heavy1/2), times in order.

## Verification (read-only checker, 2026-11-13)

Checked against `Bison.cs`, `CharacterControl.cs`, `EffectControl.cs` and TTO's `pseudo/Bison.c`, every opaque predicate
resolved (`checks\fx_bison_research\skills_a\cond.py`) and every coroutine traced with `pipeline/clip_flow.js`; my probe
`checks\fx_bison_research\verify_a\blocks.py`: all ten JSON blocks parse (19 entries), cue times in order.

**Result: no corrections.** Every time, name, position, random pick, rank and paste-ready block stands as written; no
corrected block set. What was re-derived:

- **Dispatcher:** stage 2 press 0.3-0.7 s (:4874, :4882); stage 3 after +1 (:4934); `25 + 5 x 3` + 15 = 55 (:4953, :4965);
  `Random.Range(0, 100) <= lckAdjust(55)` (:4977); `lckAdjust` (CharacterControl.cs:20658-20670) at LCK 1 =
  floor(5555 / 100.55) = 55, so 56 values of 100: **56 %** spin. Added Swing after +2 (:5059); the holdCharge branch (:5089-5120).
- **Clip starts:** `actionTime` is set at stage 1's entry (:15113) and otherwise only in each stage's standby branch
  (:15063, :15886, :16697, :17805, :18902), which a next press skips: 0.7 (:15947), 1.4 (:16761, :17871); RPC_nAttack5's
  entry branches on `myCommand == "nAttack3"` (:18949) -> Block_110 = +2.2 (:19016), else Block_144 = +2.7 (:19022).
- **Stage waits** (case by case): nAttack1 0.3 / 0.2 / 0.2; nAttack2 0.3 / 0.2 / 0.3; nAttack3 0.1 / 0.3 / 0.2 / 0.3 (its
  voice reaches PlayOneShot through IL_1302 :16774 from case 3, so 0.1 s); nAttack4 0.3 / 0.2 / 0.2 / 0.3 / 0.5; nAttack5
  0.3 fade (:18991), 0.3 / 0.2 / 0.3 / 0.5. Voices 0.3 / 0.3 / 0.1 / 0.3 / 0.3 s: right.
- **Charge:** case 2 = cAttack2 (0.2 fade, Loop) then `Yield(3, 1.2)`; case 3, still `attack` / `cAttack1` and
  `mGameType > 4`: cAttack1_dust at +0.15 up, hero rotation (:19332), `getSolidChangeLv()` = `hasSkill(411)` (:9042) ->
  solidCharge_ring (:19370). Voice under `hasSkill(113)`: holdCharge1 on `Range(0, 2) == 1`, else holdCharge2 (:19457-19502).
- **Release:** >= 2 s (:5372), `clamp(t, 2, 4 + 4)` (:5378), #113 -> AddStatus + RPC_cAttack0 (:5388-5411); cAttack0:
  myCommand (:20708), `CrossFade("root", 0.2)` (:20717), `Yield(2, 0.2)` (:20731). EffectControl ends a followState
  effect when actionState **or** myCommand changes (EffectControl.cs:137-140, :226-232), so the release's myCommand
  change does end the dust and Solid Hold's ring.
- **Hold Charge look:** CharacterControl.cs:34666-34702 and its removal :15390-15403; RPC_cAttack2 `hasStatus` ->
  removeStatus + holdCharge_fire (:20263-20292).
- **Spin:** entry IL_1635 (:20106-20125); voice on `hasSkill(232)` = improvedSwing (:20160-20184); `i = 0; goto IL_1019`
  in the same frame (:20444-20447), so the first swish is at 0; case 2 plays the second; `Yield(2 / 3, 0.2 - 0.033 x 3)`
  (:20464, :20468); after 8 hits `Yield(4, 0.2)` (:20466) -> standby (:19822-19850): 16 swishes 0.101 s apart, standby 1.816.
- **Emotes, KO, run:** :34797, :34805-34817, :34871-35312, :35318, :35372; RPC_ko :40733-40859; RPC_dead's voice gates
  `goto IL_3F4`, the effect, so deadEffect always spawns, at `position - forward` (:41092-41213); footStep_left / right
  are the fields at :13984 / :13987 (probe_fields offsets 32 / 40 = step_heavy1 / 2), played by :124-178. The rip's
  `voices/` has no laugh (rip_list.txt).
- **TTO citations** spot-read (pseudo/Bison.c:949, :610, :601, :775, :796, :22519, :488, :493, :1124, :1569, :21837,
  :21842, :22031): as stated.
- **Formats:** every cue fits index.html's `cueOf` (:4333-4344: positional `[t, kind, name, d, cut]` or options d / y /
  cut / kill / p / roll; `"sound"` kind; `d: -1` works). `"@ChargeAttack:root"` is fxStart's key (`ch.id + ":" + clip`,
  :4447). A cut is compared with the step's clock (`FX.t`, :3954), so 7.15 / 1.766 inside the 7.2 / 1.816 steps is the
  Penguin's 2.95 convention. Not in the page yet, as the report says: `everyCycle` (P3), the `~0.3` fade (P2) and the
  random step (P1) (token regex :1229).

Precisions (no cue change):
1. The `holdCharge` glow is Instantiated at `Vector3.zero` with `Quaternion.identity` and then parented (CharacterControl.cs:34682-34702):
   its world rotation is identity, not the hero's, like the ring's. A round emitter on the unturned page hero: nothing to change.
2. "Read this first" 5: the spin's hits draw through `RPC_nAttack_hit` too (:20060); the prefab's `cAttack_hit` field
   (:14056, probe_fields offset 72 = nAttack_hit) is not used there. Left out either way.
