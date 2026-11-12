# Cat effects + sounds research: Normal Attack, Charge Attack, emotes, basic moves, KO

Scope: clips nAttack1, nAttack2, nAttack3, nAttack4 (RPC_nAttack1-4 and the dispatcher `doNormalAttack`), cAttack1, cAttack2
(RPC_cAttack1, the release RPC_cAttack0, `doBeginCharge`, `doReleaseCharge`), any MP / SP transfer style skill on an attack
clip (the Cat has none, below), RPC_activateIcon1, the emotes (RPC_emotion), basic moves, KO (RPC_ko, RPC_dead) and, because
it plays the getUp clip with a voice, RPC_revive. Research only (recipe steps 1-3). Line numbers are
`D:\12tails\DecompiledSource\Cat.cs` unless another file is named. Times are seconds from the start of the clip the cue is
keyed by. Distance 0 = at the hero. Every opaque predicate (`if (a - b != c) continue;`) on the paths below was worked by hand
(the subtraction done for each one on the clip, voice, sound, effect and wait lines); each one goes the normal way.

Probe and helper files, all under `checks\fx_cat_research\attacks_emotes\`:
- `RPC_*.txt`: `clip_flow.js` dumps of RPC_nAttack1-4, RPC_cAttack1, RPC_cAttack0, RPC_emotion, RPC_ko, RPC_dead,
  RPC_activateIcon1, RPC_revive (the extra regex `Effects/|Voices/|Sounds/|createEffect|Instantiate|PlayOneShot`);
- `probe.txt` + `probe_summary.txt` (`summarize.py`): `wardrobe_fx.py cat --probe nAttack_dust,damagePlus,damagePlus_ring,
  deadEffect,nAttack_hit,hiddenBlade_hit` (read only, nothing written);
- `probe_fields.txt` (`probe_fields.py`, the Bat's script pointed at the Cat): the Cat MonoBehaviour's GameObject fields are
  `luckyCard_hit`, `forwardLunge_dust`, `TestRay`, `deadEffect`; RPC_dead's `deadEffect` is the prefab of that name
  (`heroes/cat/effects/deadEffect`, material `cat_dead`);
- `rip_audio.txt`: the rip's `heroes/cat/voices/` and `sounds/` listings.

TTO: `DecompiledSource_TTO_2026-11-02\pseudo\Cat.c` keeps the same strings in the same coroutines (below); its waits are
opaque `Waits__Get()` calls, so the BB times stand.

---

## Read this first

1. **The Normal Attack SEQ's step times are wrong** (index.html work, not a cue job). The game starts nAttack2 **0.6 s** after
   stage 1, nAttack3 at **1.2 s** and nAttack4 at **1.7 s** (the dispatcher section). The page's
   `"Normal Attack: nAttack1 nAttack2^ nAttack3 nAttack4"` plays whole clips (nAttack1 0.8 s, nAttack2 0.8333 s, nAttack3
   0.9 s, `data/cat/clips.json`), so stage 2 starts 0.2 s late, stage 3 at 1.633 s (0.433 s late) and stage 4 at 2.533 s
   (0.833 s late). Proposed: **`"Normal Attack: nAttack1@0.6 nAttack2^@0.6 nAttack3@0.5 nAttack4"`**. The fades are right
   as written: nAttack1 is a cut (`PlayAnimation("nAttack1", 0)` :16857; the page's first-step fade stays, as the Sheep's,
   Penguin's and Bat's, Bat decision 28), nAttack2 fades 0.1 s (`^`, :17076), nAttack3 is a cut (:17791), nAttack4 is
   `animation.Play` (a cut, :18730). The Bible already has these starts (`cat-skill-reference.md:497-504`).
2. **The Charge Attack SEQ is off too.** cAttack1 gives way to the looped cAttack2 after **0.5 s** (`Yield(2, 0.5)` :20121,
   then `PlayAnimation("cAttack2", 0)` looped :19711-19716, a cut), not after its whole 0.6 s clip. The charge ticks at 1.0,
   2.0 and 3.0 s after the press (:19728, :19963-19971); with Double Focus #411 on (passives rule) each tick adds 2 stacks and
   the charge is full (6 / 6 at damagePlus5) on the **third** tick, 3.0 s after the press = 2.5 s into cAttack2. Today's
   `"cAttack1 cAttack2*@3.4"` (0.6 + 3.4 = 4.0 s) looks like the full charge **without** Double Focus (4 ticks, max 4
   stacks at rank 3). Proposed: **`"Charge Attack: cAttack1@0.5 cAttack2*@2.6"`** (the third tick at 2.5 s inside the
   step, as the Wolf's `@5.1` holds its 5 s tick). Question 1.
3. **Melee hits draw nothing here.** Every combo hit is a `FindRecTarget` box 3 m long from 1 m behind the Cat, 2 m wide (4 m
   on stage 4) (:16520, :17318, :18001, :18244, :18972, :19213; Bible `:468`), so the 10 m target point is never hit:
   `nAttack_hit` (RPC_nAttack_hit :8253-8282, at the enemy's bounds centre + 1 up), `hiddenBlade_hit` (RPC_hiddenBlade_hit
   :10059-10089, Hidden Blade #331-334 / Jagged Knife #433 on, only on a hit from behind), the "HiddenBlade!" text and
   `onNormalAttackHit`'s gear procs (:15560) are left out, as the Wolf's and the Bison's melee attacks (plans/fx_bison/
   attacks_emotes.md "Read this first" 5).
4. **The charge's look.** On every tick (missions / arena only, `mGameType > 4` :19955, kept as the Sheep / Penguin / Wolf
   precedent): `damagePlus_ring` at the hero (createEffect :19998; it plays its own `sounds/cAttack_ring`) and, on the first
   tick while none exists (`if (aXHRRIdoYe) skip` :20045), the **`damagePlus`** glow Instantiated at the hero and parented
   to `mount_Hand_R` (:20053-20082) with a `StatusControl` that destroys it when the damagePlus status ends
   (StatusControl.cs:66-110: every 0.5 s, `getStatusLv(status) > 0` or Destroy). The status lasts `chaAdjust(12)` = 12 s at
   the page's CHA 1 (CharacterControl.cs:20593-20618) and is not spent here (no hits), so: `kill` 10 (the long-buff rule).
   The `count <= lv + 1` test before the ring (:19981) is always true, because the count was clamped to `lv + 1` the line
   before (:19976): the ring and the "DamagePlus5: 6/6" text come on every tick, also after the charge is full.
5. **One new page part and one inventory line** (Parts needed):
   - `StatusControl` (the only effect in the whole inventory that needs it, `damagePlus`) draws nothing: it is the effect's
     life, which the cue's `kill` gives. Add it to `BUILT` in `pipeline/wardrobe_fx_inventory.py` as data-only (as
     `Sheep_seal`).
   - A cue option **`"single": true`**: skip the spawn while a copy of the same effect from an earlier play still lives (the
     game's guard :20045). Without it the 3.1 s tile loop would stack up to four 10 s hand glows. Fallback: `kill` 2.1 (the
     glow ends with the loop). Question 2.
6. **No MP / SP transfer style skill plays an attack clip.** The only callers of the nAttack / cAttack clips are the combo
   and the charge (:16857, :17076, :17791, :18730, :19711, :19807; the rest of the grep hits are the animation loader
   :1167-1227 and `myCommand` tests). So no `@<Skill>:nAttack1` style entry, unlike the Penguin's MP Transfer.
7. **activateIcon1 plays the `battle` clip** (looped, 0.2 s fade, :48622-48627), the battle emote's clip: the mission's
   "activate the icon" interaction, voice `activate1` at 0 (:48677-48689), a cast bar (:48769), `activate2` in
   RPC_activateIcon2 (:15291). No tile (Penguin decision 19); the battle tile keeps the emote's voice.
8. **Name collisions** (the cue kind picks the folder; voices are saved as `v_<name>`):
   - `nAttack1-4` are clip names, `voices/` files (the shouts) and `sounds/` files (the swings): two cues each, kinds
     `"voice"` and `"sound"` (the Wolf's shape);
   - `cAttack1` / `cAttack2` are clip names and `voices/` files;
   - `cAttack_ring` (`sounds/`) is damagePlus_ring's own AudioSource clip: it comes with the effect, no cue.
9. **The Cat has KO voices** (`voices/` ko1, ko2, dead1, dead2): the KO entry is the Wolf's / Penguin's (decision 11).
10. **getUp has a voice in RPC_revive** (`Voices/revive` at 0, then `animation.Play("getUp")`, :49764-49844). RPC_ko's getUp
    (3 s into KO) is silent. Every class has the same RPC_revive voice (`Voices/revive"` in Wolf, Sheep, Penguin, Bat,
    Bison.cs; 7 classes' rips have `voices/revive.wav`), and no class cues it yet. Question 3.

---

## The dispatcher: Normal Attack stage times (SEQ check)

`doNormalAttack` (:7945-8222):

- **Stage 1** from standby or run when `isTimeOut("nAttack") == 0` (:8192-8198): RPC_nAttack1.
- **Stage 2:** while `myCommand == "nAttack1"`, with Combo #101 (:8022-8028), only when `actionTime + 0.3 < now < actionTime + 0.6`
  (:8038 breaks at `<= +0.3`, :8046 at `>= +0.6`): RPC_nAttack2 (:8054).
- **Stage 3:** while `myCommand == "nAttack2"`, with #102 (:8082-8088), when `actionTime + 0.9 < now < actionTime + 1.2`
  (:8098, :8106): RPC_nAttack3 (:8114).
- **Stage 4:** while `myCommand == "nAttack3"`, with #103 (:8144-8152), once `now > actionTime + 1.7` (:8162): RPC_nAttack4 (:8170).
  The window closes at stage 3's standby, stage 1 + 1.9 s (below).
- **actionTime is set only by stage 1** (:16839-16848 sets actionState, actionTime, myCommand). Stages 2-4 set only
  `actionState` and `myCommand` (:17592-17595, :18523-18526, :19490-19493), and each waits for a fixed time after stage 1:
  - RPC_nAttack2: `Yield(2, actionTime - now + 0.6)` (:17609): the press is before 0.6 s, so **nAttack2 starts at 0.6 s**;
  - RPC_nAttack3: `Yield(2, actionTime - now + 1.2)` (:18538): the press is before 1.2 s, so **nAttack3 starts at 1.2 s**;
  - RPC_nAttack4: `Yield(2, actionTime - now + 1.7)` (:19511): the press is after 1.7 s (a negative wait = the next frame), so
    **nAttack4 starts at 1.7 s** at the earliest.
- The standbys are skipped once the next stage is pressed: stage 1's at 0.6 s tests `myCommand == "nAttack1"` (:16781), stage
  2's at 0.6 s into its clip `"nAttack2"` (:17534), stage 3's at 0.7 s into its clip `"nAttack3"` (:18465).
- Max rank: Combo 3 (#101-103) reaches stage 4 (Bible `:258`).

Step lengths: nAttack1 0 → 0.6, nAttack2 0.6 → 1.2, nAttack3 1.2 → 1.7, nAttack4 to its standby 0.9 s in (`Yield(6, 0.4)`
:19513; the page plays its 1.8 s clip to the end, as the Penguin's last stage).

**Proposed SEQ:** `"Normal Attack: nAttack1@0.6 nAttack2^@0.6 nAttack3@0.5 nAttack4"` (parses as the Sheep's
`nAttack2^@0.8`).

## The dispatcher: Charge Attack (SEQ check)

- `doBeginCharge` (:8339-8433): from standby or run, `isTimeOut("cAttack") == 0`, Charge Attack #111, not within 0.1 s of the
  last action (`actionTime + 0.1 > now` breaks, :8388-8400): RPC_cAttack1 (:8406).
- `doReleaseCharge` (:8435-8500): while `actionState "attack"` and `myCommand "cAttack1"`: **RPC_cAttack0** (:8478). There is no
  release attack: RPC_cAttack0 (:20286-20368) sets `myCommand "cAttack0"` (:20339), crossfades to root over 0.2 s (:20348)
  and goes to standby 0.2 s later (`Yield(2, 0.2)` :20367, :20303). No voice, no effect, no damage (Bible `:279-282`: the
  charge only gives damagePlus stacks to later hits).
- `cAttack1@0.5`: clip cAttack1 cut in at 0 (:19807), `Yield(2, 0.5)` (:20121), then cAttack2 cut in, looped (:19711-19716).
  So no `~` on cAttack2.
- The ticks: `mChargeTimer = actionTime + 1` (:19728); each FixedUpdate (`Yield(3, WaitForFixedUpdate)` :20123) while
  `actionState "attack"` and `myCommand "cAttack1"` (:19940-19946), when `mChargeTimer < now` (:19963): `mChargeTimer = now + 1`
  (:19971). Ticks at 1.0, 2.0, 3.0 ... s after the press (to the next physics step, 0.02 s), = **0.5, 1.5, 2.5** s into cAttack2.
- Max rank, passives on: `getChargeLv()` = 3 (#113, :8505-8544) + 2 with Double Focus #411 (:19733) = damagePlus **5**; each tick
  adds 2 stacks (`1 + 1` :19976, :20031), clamped to `lv + 1` = 6: 2 / 4 / 6, full on the third tick.

**Proposed SEQ:** `"Charge Attack: cAttack1@0.5 cAttack2*@2.6"`.

---

## nAttack1 (Normal Attack, stage 1)

- Coroutine `RPC_nAttack1` (`$RPC_nAttack1$21644`, :16186-16955).

| t (s) | what | source |
|---|---|---|
| 0 | `actionState "attack"`, `actionTime`, `myCommand "nAttack1"`, `addTimeOut("nAttack", 1.5)`, LookAt, clip nAttack1 (cut), moveSpeed 3; wait 0.1 | :16839-16872, `Yield(2, 0.1)` :16903 |
| 0.1 | `nAttack_dust` at `position + TransformDirection(-0.1, 0, -0.25)`, hero rotation; wait 0.1 | :16320-16332, `Yield(3, 0.1)` :16888 |
| 0.2 | moveSpeed 9; `Sounds/nAttack1` (`PlayOneShot(clip)`, volume 1; own hero, or `mGameType > 4`); voice `Voices/nAttack1` (pvoice on; own hero, or a mission teammate; 1.0 own, 0.75 others); wait 0.2 | :16350-16399, :16413-16451, PlayOneShot :16900, `Yield(4, 0.2)` :16884 |
| 0.4 | moveSpeed 0, the hit (`FindRecTarget(pos - fwd, fwd, 1, 1, 3, 2)` :16520): melee, nothing at the 10 m point; wait 0.2 | :16486-16770, `Yield(5, 0.2)` :16882 |
| 0.6 | standby, unless stage 2 was pressed | :16774-16820 |

- Sums: dust 0 + 0.1 = 0.1; sound and voice 0.1 + 0.1 = 0.2; hit 0.2 + 0.2 = 0.4; standby 0.4 + 0.2 = 0.6 (the Bible's hit at
  0.4, `:501`).
- `nAttack_dust` (probe): EffectControl life 1, no follow; one ImageEmitter (Life 0.3, `Dust7`, tilted 30 deg, world velocity
  (0, 0.2, 0.2)). Ready.
- In place: the game moves her 2.4 m forward over the stage (Bible `:501`); the page's hero never moves (index.html Fx.update
  "the hero never moves here"), so the dust sits at its offset from where she stands.
- TTO `<RPC_nAttack1>d__172` (pseudo/Cat.c:16797): the same strings, `effects/nAttack_dust`, `sounds/nAttack1`, `voices/nAttack1`
  (:16905-16916), clip cut (:17416).

```json
  "nAttack1": {
    "why": "Cat.cs RPC_nAttack1 (:16186-16955): clip at 0 (cut, PlayAnimation(nAttack1, 0) :16857), moveSpeed 3; 0.1 s (Yield(2, 0.1) :16903) nAttack_dust at position + TransformDirection(-0.1, 0, -0.25) with the hero's rotation (:16320-16332; EffectControl life 1); 0.2 s (Yield(3, 0.1) :16888) the swing Sounds/nAttack1 at full volume (PlayOneShot(clip) :16399) and the voice nAttack1 (:16451, PlayOneShot :16900); the hit at 0.4 s (Yield(4, 0.2) :16884) is melee, a 3 m box from 1 m behind (FindRecTarget :16520): nothing at the 10 m target point (nAttack_hit :8253-8282, Hidden Blade's hiddenBlade_hit :10059-10089 and onNormalAttackHit :15560 only on a hit, left out as the Wolf's / Bison's); standby 0.6 s (Yield(5, 0.2) :16882, :16787) unless stage 2 is pressed (its clip at 0.6 s: Yield(2, actionTime - now + 0.6) :17609); the hero stays in place (the game's 2.4 m lunge is not moved)",
    "cues": [
    [0.1, "fx", "nAttack_dust", {"d": -0.25, "x": -0.1}],
    [0.2, "sound", "nAttack1"],
    [0.2, "voice", "nAttack1"]
    ]
  },
```

Sure: high.

## nAttack2 (stage 2)

- Coroutine `RPC_nAttack2` (`$RPC_nAttack2$21659`, :16959-17670), started by a press 0.3-0.6 s into stage 1; its clip at stage 1 + 0.6 s.

| t (s, from its clip) | what | source |
|---|---|---|
| 0 | clip nAttack2 (0.1 s fade), moveSpeed 0, `addTimeOut("nAttack", 1.5)`, LookAt; voice `Voices/nAttack2`; wait 0.1 | :17065-17150, PlayOneShot :17621, `Yield(3, 0.1)` :17613 |
| 0.1 | moveSpeed 7; `nAttack_dust` at `position + TransformDirection(-0.4, 0, 0)`, hero rotation; `Sounds/nAttack2`; wait 0.3 | :17175-17256, `Yield(4, 0.3)` :17611 |
| 0.4 | moveSpeed 0, the hit (`FindRecTarget` :17318): melee; wait 0.2 | :17274-17525, `Yield(5, 0.2)` :17605 |
| 0.6 | standby, unless stage 3 is pressed | :17527-17579 |

- Sums: dust and sound 0 + 0.1 = 0.1; hit 0.1 + 0.3 = 0.4 (stage 1 + 1.0, Bible `:502`); standby 0.4 + 0.2 = 0.6 (stage 1 + 1.2).
- TTO `<RPC_nAttack2>d__173` (pseudo/Cat.c:17578): the same strings (:17676-17691), the 0.1 s fade (:18210).

```json
  "nAttack2": {
    "why": "Cat.cs RPC_nAttack2 (:16959-17670; its clip 0.6 s after stage 1: Yield(2, actionTime - now + 0.6) :17609, the press window 0.3-0.6 s, doNormalAttack :8038-8054): clip (0.1 s fade, :17076), moveSpeed 0, the voice nAttack2 at 0 (:17150, PlayOneShot :17621); 0.1 s (Yield(3, 0.1) :17613) moveSpeed 7, nAttack_dust at position + TransformDirection(-0.4, 0, 0) with the hero's rotation (:17197-17209) and the swing Sounds/nAttack2 at full volume (:17244-17256); the hit at 0.4 s (Yield(4, 0.3) :17611) is melee (FindRecTarget :17318): nothing at the 10 m target point (nAttack_hit / hiddenBlade_hit only on a hit); standby 0.6 s (Yield(5, 0.2) :17605, :17540) unless stage 3 is pressed (its clip at stage 1 + 1.2 s, :18538)",
    "cues": [
    [0, "voice", "nAttack2"],
    [0.1, "fx", "nAttack_dust", {"x": -0.4}],
    [0.1, "sound", "nAttack2"]
    ]
  },
```

Sure: high.

## nAttack3 (stage 3)

- Coroutine `RPC_nAttack3` (`$RPC_nAttack3$21672`, :17674-18609), started by a press 0.9-1.2 s after stage 1; its clip at stage 1 + 1.2 s.

| t (s, from its clip) | what | source |
|---|---|---|
| 0 | clip nAttack3 (cut), `addTimeOut("nAttack", 1.5)`, LookAt; voice `Voices/nAttack3`; wait 0.1 | :17780-17860, PlayOneShot :18544, `Yield(3, 0.1)` :18534 |
| 0.1 | moveSpeed 4; `Sounds/nAttack3`; wait 0.2 | :17885-17934, `Yield(4, 0.2)` :18554 |
| 0.3 | hit 1 (`FindRecTarget` :18001); wait 0.2 | :17952-18213, `Yield(5, 0.2)` :18549 |
| 0.5 | moveSpeed 0, hit 2 (:18244); wait 0.2 | :18215-18456, `Yield(6, 0.2)` :18536 |
| 0.7 | standby, unless stage 4 is pressed | :18458-18510 |

- Sums: sound 0.1; hits 0.1 + 0.2 = 0.3 and 0.5 (stage 1 + 1.5 / 1.7, Bible `:503`); standby 0.7 (stage 1 + 1.9). No dust here.
- TTO `<RPC_nAttack3>d__174` (pseudo/Cat.c:18331): the same strings (:18427-18440), clip cut (:18470).

```json
  "nAttack3": {
    "why": "Cat.cs RPC_nAttack3 (:17674-18609; its clip 1.2 s after stage 1: Yield(2, actionTime - now + 1.2) :18538, the press window 0.9-1.2 s, doNormalAttack :8098-8114): clip (cut, :17791) and the voice nAttack3 at 0 (:17860, PlayOneShot :18544); 0.1 s (Yield(3, 0.1) :18534) moveSpeed 4 and the swing Sounds/nAttack3 at full volume (:17922-17934); hits at 0.3 s and 0.5 s (Yield(4, 0.2) :18554, Yield(5, 0.2) :18549) are melee (FindRecTarget :18001, :18244): nothing at the 10 m target point; no dust in this stage; standby 0.7 s (Yield(6, 0.2) :18536, :18471) unless stage 4 is pressed (from 1.7 s after stage 1, :8162)",
    "cues": [
    [0, "voice", "nAttack3"],
    [0.1, "sound", "nAttack3"]
    ]
  },
```

Sure: high.

## nAttack4 (stage 4)

- Coroutine `RPC_nAttack4` (`$RPC_nAttack4$21687`, :18613-19578), started by a press after 1.7 s; its clip at stage 1 + 1.7 s at the earliest.

| t (s, from its clip) | what | source |
|---|---|---|
| 0 | `animation.Play("nAttack4")` (a cut), `addTimeOut("nAttack", 1.5)`, LookAt; `nAttack_dust` **at the hero** (position, rotation); voice `Voices/nAttack4`; wait 0.1 | :18719-18831, Instantiate :18780, PlayOneShot :19520, `Yield(3, 0.1)` :19507 |
| 0.1 | moveSpeed 6; `Sounds/nAttack4`; wait 0.2 | :18856-18905, `Yield(4, 0.2)` :19516 |
| 0.3 | hit 1 (`FindRecTarget(..., 2, 2, 3, 2)` :18972, 4 m wide); wait 0.2 | :18923-19182, `Yield(5, 0.2)` :19523 |
| 0.5 | hit 2 (:19213); wait 0.4 | :19184-19423, `Yield(6, 0.4)` :19513 |
| 0.9 | standby | :19425-19477 |

- Sums: sound 0.1; hits 0.3 and 0.5 (stage 1 + 2.0 / 2.2, Bible `:504`); standby 0.9.
- TTO `<RPC_nAttack4>d__175` (pseudo/Cat.c:19286): the same strings (:19385-19400).

```json
  "nAttack4": {
    "why": "Cat.cs RPC_nAttack4 (:18613-19578; its clip 1.7 s after stage 1 at the earliest: Yield(2, actionTime - now + 1.7) :19511, the press from 1.7 s, doNormalAttack :8162-8170): clip (animation.Play, a cut, :18730), nAttack_dust at the hero's position and rotation (:18768-18780) and the voice nAttack4 at 0 (:18831, PlayOneShot :19520); 0.1 s (Yield(3, 0.1) :19507) moveSpeed 6 and the swing Sounds/nAttack4 at full volume (:18893-18905); hits at 0.3 s and 0.5 s (Yield(4, 0.2) :19516, Yield(5, 0.2) :19523) are melee, a 4 m wide box (FindRecTarget :18972, :19213): nothing at the 10 m target point; standby 0.9 s (Yield(6, 0.4) :19513, :19438)",
    "cues": [
    [0, "fx", "nAttack_dust"],
    [0, "voice", "nAttack4"],
    [0.1, "sound", "nAttack4"]
    ]
  },
```

Sure: high.

---

## cAttack1 (Charge Attack: the wind-up)

- Coroutine `RPC_cAttack1` (`$RPC_cAttack1$21702`, :19582-20170).
- At 0: `actionState "attack"`, `actionTime`, `myCommand "cAttack1"`, `addTimeOut("cAttack", 1)`, LookAt, clip cAttack1 cut, moveSpeed 0
  (:19777-19822).
- The voice at 0 (pvoice on; own hero or a mission teammate, :19827-19856), at most once every 2 s (:19858-19866):
  `cAttack1|cAttack2` (`Random.Range(0, 2)` :19871; loads :19883 / :19915; PlayOneShot :20111 / :20119). Both files exist.
- Then `Yield(2, 0.5)` (:20121).
- The tile replays every 3.1 s (proposed SEQ), so the 2 s gate never thins it.
- TTO `<RPC_cAttack1>d__178` (pseudo/Cat.c:2411): the same strings, `voices/cAttack1` / `cAttack2`, `effects/damagePlus`,
  `effects/damagePlus_ring`, `mount_Hand_R` (:2458-2475), `Random.Range(0, 2)` (:2607), cAttack1 cut (:2575), cAttack2 (:2505).

```json
  "cAttack1": {
    "why": "Cat.cs RPC_cAttack1 (:19582-20170): clip at 0 (cut, PlayAnimation(cAttack1, 0) :19807) and the voice at 0: cAttack1 or cAttack2 (Random.Range(0, 2) :19871, loads :19883 / :19915, PlayOneShot :20111 / :20119; at most every 2 s, :19858-19866); at 0.5 s (Yield(2, 0.5) :20121) it cuts to the looped cAttack2 (:19711-19716), whose cue holds the charge",
    "cues": [
    [0, "voice", "cAttack1|cAttack2"]
    ]
  },
```

## cAttack2 (Charge Attack: the held charge)

- Same coroutine, case 2 and IL_BEA (:19698-19735, :19939-20104), from cAttack1 + 0.5 s.
- At 0 (its own clip): `PlayAnimation("cAttack2", 0)` looped (:19711-19716); `mDuration = chaAdjust(12)` (12 at CHA 1), `mChargeTimer =
  actionTime + 1` (:19728), `mChargeLv = getChargeLv() + 2` (Double Focus #411, :19733).
- Each FixedUpdate (:20123) while `actionState "attack"` and `myCommand "cAttack1"` (:19940-19946), **only when `mGameType > 4`**
  (:19955; kept, the Sheep / Penguin / Wolf precedent), on a tick (0.5, 1.5, 2.5 s, the dispatcher section):
  - `damagePlus_ring` at the hero's position and rotation (createEffect :19987-19998); the probe: EffectControl life 1, no
    follow, an Ellipsoid one-shot (`Smoke1`), two RingEmitters (`Line_vertMultilines2`, `Dust3_h`), and its AudioSource
    plays `sounds/cAttack_ring` on awake. Ready;
  - the "DamagePlus5: n/6" text (:20018) and `RPC_AddStatus("damagePlus", 5, 12, 2)` (:20031): nothing drawn;
  - while no glow exists (:20045): `damagePlus` Instantiated at the hero with `Quaternion.identity` (:20053), parented to
    `mount_Hand_R`, `localPosition = 0` (:20077-20082), `StatusControl.Init(mChar, "damagePlus")` (:20087). The probe: root
    StatusControl only (no EffectControl), one legacy Ellipsoid (energy 0.5-0.8, 12-24 a second, local space, `damagePlus`
    material) + ParticleAnimator + ParticleRenderer. It lives as long as the status (StatusControl.cs:66-110): 12 s after the
    last tick here (no hit spends the stacks), cut at **10 s** (`kill` 10).
- The release (RPC_cAttack0, `myCommand "cAttack0"` :20339) ends the loop (:19946); the ring has no followState, so no cut.
- The rig has `mount_Hand_R` (`data/cat/rig.json`).
- Small difference: the game parents with the world pose kept (Unity's `transform.parent =`), so the glow keeps world identity
  at that moment; the page's `bone` option sets `localRotation` identity. The emitter is a point with symmetric random
  velocity and a 0.1 m/s local drift, so the difference is about 8 cm of drift direction.

```json
  "cAttack2": {
    "why": "Cat.cs RPC_cAttack1 case 2 (the cut to the looped cAttack2 0.5 s in, :19711-19716): Charge Attack 3 + Double Focus #411 on (passives rule): damagePlus 5 (getChargeLv 3 + 2, :19733, :8505-8544); a charge tick 1.0 s after the press and every 1 s after (mChargeTimer :19728, :19963-19971, FixedUpdate :20123) = 0.5, 1.5, 2.5 s into this clip, mission / arena only (mGameType > 4, :19955): each tick damagePlus_ring at the hero's position and rotation (createEffect :19987-19998; EffectControl life 1, plays its own Sounds/cAttack_ring; every tick, the count <= lv + 1 test :19981 is always true after the clamp :19976), +2 stacks (RPC_AddStatus :20031, full 6 / 6 on the third tick); on the first tick, while none exists (:20045), the damagePlus glow on mount_Hand_R (Instantiate :20053, parent and localPosition 0 :20077-20082) whose StatusControl keeps it while the status lasts (StatusControl.cs:66-110; chaAdjust(12) = 12 s, CharacterControl.cs:20593-20618; no hit spends it here): kill 10 (the long-buff rule), single (one glow at a time, the game's guard :20045); the release RPC_cAttack0 (myCommand cAttack0 :20339, root crossfade 0.2 s :20348, standby 0.2 s later :20367) plays nothing",
    "cues": [
    [0.5, "fx", "damagePlus_ring"],
    [0.5, "fx", "damagePlus", {"bone": "mount_Hand_R", "kill": 10, "single": true}],
    [1.5, "fx", "damagePlus_ring"],
    [2.5, "fx", "damagePlus_ring"]
    ]
  },
```

Sure: high on the trace; the glow's handling is question 2.

---

## Emotes and basic moves

`RPC_emotion` (`$RPC_emotion$22282`, :43007-43835). It works exactly as the Wolf's, Sheep's and Penguin's:

- The voice plays at 0, **before** the clip (IL_12AE :43238-43320). The gates:
  - the voice option is on (`pvoice`, :43239);
  - more than 2 s since the last action (`Time.time > actionTime + 2`, :43245);
  - the own hero, anyone in game code 31, or a mission teammate (:43250-43285, game code :43257).
- `emo_chat` → `Voices/chat` + `Random.Range(1, 6)`, i.e. chat1-5 (:43297).
- Every other `emo_<name>` → `Voices/<name>` (`Substring(4)`, :43305), `PlayOneShot` (volume 1, :43317) only if the file loads.
- Then `actionState "emotion"` and the clip with a 0.2 s fade (:43325-43803). No effect and no Sounds/ anywhere in RPC_emotion.

| emote | clip | voice file (voices/) | source |
|---|---|---|---|
| emo_hi, emo_wave | wave | hi / wave | :43353, :43361 → :43803 |
| emo_ty, emo_bow | bow | ty / bow | :43371, :43378 → :43789 |
| emo_laugh | laugh | laugh | :43385-43391 |
| emo_sit | sit | none (silent) | :43405-43411 |
| emo_sleep | sleep | sleep | :43417-43423 |
| emo_cheer | cheer | cheer | :43429-43435 |
| emo_beg | beg | beg | :43441-43447 |
| emo_cry | cry | cry | :43453-43459 |
| emo_talk, emo_chat | talk | talk: none; chat: chat1-5 | :43467, :43474 → :43767 |
| emo_pose | pose5 / 15 / 25 / 35 / 45 / 58 / 65 / 46 / 66 by the worn set (w_cat56 + c_all56 stops the animation), else pose | none (silent) | :43481-43729 |
| emo_battle | battle | battle | :43737-43743 |
| emo_dance | dance | none (silent) | :43752-43760 |

- In the rip's `voices/`: hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle and chat1-5 all exist; no sit, talk, pose or
  dance (`rip_audio.txt`).
- The other emote-looking voices belong to no tile here: beware, bye, come, follow, giveup, go, paper, rock, scissor, sorry,
  support, what, change, return1 / 2, mount1 / 2, disMount1 / 2, transform1 / 2.
- The TTO emote clips in the emote tab (wai, clap, cooking, mining, planting, fishingCat, pose37; `tto: true` in clips.json) have no
  BB code and no BB voice: silent, as for the other classes.
- **KO:**
  - `RPC_ko` (`$RPC_ko$22451`, :48844-49214): `animation.Play("ko")` (:49058). Voice ko1 / ko2 at 0 (Random.Range(0, 2) :49093;
    loads :49103 / :49134; PlayOneShot :49173 / :49183). getUp after 3 s (`Yield(2, 3)` :49176 → :48960), standby 1 s later
    (`Yield(3, 1)` :49180 → :48984). No effect.
  - `RPC_dead` (`$RPC_dead$22458`, :49218-49584): Rewind + `PlayAnimation("ko", 0)` (:49415). Voice dead1 / dead2 at 0
    (Random.Range(0, 2) :49450; :49462-49505). Then **always** (IL_542, which both voice gates jump to) Rewind,
    `animation.Play("ko")` and `Instantiate(deadEffect, hero position, hero rotation)` (:49517-49527); the predicate on the way,
    `141446 − 286209 != −144762`, holds.
  - `deadEffect` (probe): EffectControl life 3, no follow; an ImageEmitter 0.8 m up (`cat_dead`, Life 1.2, Delay 0.4) and two
    LineEmitters 0.1 m up (`Dust1`, Life 0.4, Delay 0.3). Ready (not in the inventory: a prefab field, not a `Resources.Load` path).
  - Decision 11: one of the two at random, even chance, with each one's voices: the Wolf's / Penguin's entry.
- **getUp:** RPC_ko's getUp has no voice. `RPC_revive` (`$RPC_revive$22465`, :49588-49870) plays `Voices/revive` at 0 (pvoice,
  own hero or a mission teammate; load :49817, PlayOneShot :49829), then `animation.Play("getUp")` (:49841), standby after 1 s
  (`Yield(2, 1)` :49863 → :49704). No effect (its 1 s `noDamage` status draws no prefab). Question 3; the entry is below,
  not counted among the entries to paste.
- walk, run, falling, root: nothing (Cat.cs loads no other Sounds/ than nAttack1-4, nAttack_hit, backflip, grandCasino2,
  luckyDice; no step / fly sound field on the Cat prefab, `probe_fields.txt`).

```json
  "wave": {
    "why": "Cat.cs RPC_emotion (:43007): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:43305, PlayOneShot :43317; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_hi (:43353) and emo_wave (:43361) both play the wave clip (:43803): voice hi or wave",
    "cues": [
    [0, "voice", "hi|wave"]
    ]
  },
  "bow": {
    "why": "Cat.cs RPC_emotion (:43007): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:43305, PlayOneShot :43317; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_ty (:43371) and emo_bow (:43378) both play the bow clip (:43789): voice ty or bow",
    "cues": [
    [0, "voice", "ty|bow"]
    ]
  },
  "laugh": {
    "why": "Cat.cs RPC_emotion (:43007): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:43305, PlayOneShot :43317; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_laugh (:43385-43391)",
    "cues": [
    [0, "voice", "laugh"]
    ]
  },
  "sleep": {
    "why": "Cat.cs RPC_emotion (:43007): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:43305, PlayOneShot :43317; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_sleep (:43417-43423)",
    "cues": [
    [0, "voice", "sleep"]
    ]
  },
  "cheer": {
    "why": "Cat.cs RPC_emotion (:43007): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:43305, PlayOneShot :43317; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_cheer (:43429-43435)",
    "cues": [
    [0, "voice", "cheer"]
    ]
  },
  "beg": {
    "why": "Cat.cs RPC_emotion (:43007): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:43305, PlayOneShot :43317; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_beg (:43441-43447)",
    "cues": [
    [0, "voice", "beg"]
    ]
  },
  "cry": {
    "why": "Cat.cs RPC_emotion (:43007): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:43305, PlayOneShot :43317; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_cry (:43453-43459)",
    "cues": [
    [0, "voice", "cry"]
    ]
  },
  "talk": {
    "why": "Cat.cs RPC_emotion (:43007): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:43305, PlayOneShot :43317; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_chat (:43474) plays the talk clip (:43767) with chat1-5 at random (Random.Range(1, 6), :43297); emo_talk (:43467) plays it silent (no Voices/talk): the tile takes the chat's voice",
    "cues": [
    [0, "voice", "chat1|chat2|chat3|chat4|chat5"]
    ]
  },
  "battle": {
    "why": "Cat.cs RPC_emotion (:43007): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:43305, PlayOneShot :43317; the rip has hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, chat1-5); no effect, no sound; emo_battle (:43737-43743): voice battle; the mission's RPC_activateIcon1 also loops this clip (:48622, voice activate1 :48677; no tile, Penguin decision 19): the tile takes the emote's voice",
    "cues": [
    [0, "voice", "battle"]
    ]
  },
  "ko": {
    "why": "Cat.cs RPC_ko (:48844): clip (animation.Play :49058) and voice ko1 or ko2 at 0 (Random.Range(0, 2) :49093, :49103-49183), getUp after 3 s (:49176, :48960), no effect; RPC_dead (:49218) plays the same clip (:49415, :49521) with dead1 or dead2 at 0 (:49450-49505) and always puts deadEffect at the hero's position and rotation (:49527; the Cat prefab's deadEffect field, EffectControl life 3): one of the two at random, even chance (the Sheep's decision 11, as wolf.json / penguin.json: roll dead, its voices with it; '!dead' = RPC_ko's)",
    "cues": [
    [0, "voice", "ko1|ko2", {"p": 0.5, "roll": "!dead"}],
    [0, "voice", "dead1|dead2", {"p": 0.5, "roll": "dead"}],
    [0, "fx", "deadEffect", {"p": 0.5, "roll": "dead"}]
    ]
  }
```

Optional (question 3; not counted above):

```json
  "getUp": {
    "why": "Cat.cs RPC_revive (:49588-49870): voice revive at 0 (load :49817, PlayOneShot :49829), then the getUp clip (animation.Play :49841), standby after 1 s (:49863, :49704), no effect; RPC_ko's getUp 3 s into a KO (:48960) is silent: one of the two at random, even chance (decision 11's shape)",
    "cues": [
    [0, "voice", "revive", {"p": 0.5}]
    ]
  }
```

---

## Parts needed (build stage)

1. **`StatusControl`** (`damagePlus`, the only effect in the inventory that needs it: `plans/fx_inventory.md` "Parts" line 47):
   - What it does (StatusControl.cs:37-110): `Init` stores the character and the status name; every 0.5 s `Update` destroys the
     object once the character is gone or `getStatusLv(status) == 0`. It draws nothing and moves nothing.
   - Build: data-only. Add `"StatusControl"` to `BUILT` in `pipeline/wardrobe_fx_inventory.py` with a comment (the effect's life
     is the status's: the cue's `kill`), then rerun the inventory. The page needs nothing for the component itself: an effect
     with no EffectControl lives until its `kill` (index.html Fx.update: `killAt`, no `ec`).
   - Check `wardrobe_fx.py`'s extraction keeps the root's child emitter with a root that has no EffectControl (the probe reads it
     fine).
2. **The cue option `single`** (index.html, the cue dispatch next to `f.killAt = c.kill`, ~:4705): when `c.single` and
   `FX.live` already holds a live Fx of the same effect name, skip this spawn. Document it in the cue-format comment
   (~:4366-4395) with the source (Cat.cs:20045, `if (aXHRRIdoYe) skip`). Question 2 has the fallback.

Everything else cued here is ready: nAttack_dust, damagePlus_ring, deadEffect (and the `bone` option already exists:
Soul of Arms' trail on mount_Hand_R).

## Left out

- Everything at a hit enemy (Read this first 3): `nAttack_hit`, `hiddenBlade_hit` (+ its own `sounds/nAttack_hit`), the
  HiddenBlade! text, Open Wound, onNormalAttackHit's gear procs. Melee boxes reach about 2 m.
- The combo's lunge (moveSpeed 3 / 9 / 7 / 4 / 6): the page's hero stays in place.
- The DamagePlus text (:20018) and the damagePlus status icon: no prefab.
- activateIcon1 / 2 (Read this first 7).
- RPC_revive's `noDamage` status: no prefab.

## Open questions (each with the recommended answer)

1. **Charge Attack's hold.** The proposed `cAttack1@0.5 cAttack2*@2.6` shows the full charge with Double Focus on (three ticks,
   6 / 6 stacks at damagePlus 5). Today's `@3.4` after the whole cAttack1 (4.0 s) matches a full charge without Double Focus
   (four ticks). Recommended: **`@2.6`** (passives on: Double Focus is a passive). If a fourth ring is wanted in view,
   `cAttack2*@3.6` (0.5 + 3.6 = 4.1 s, the 4.0 s tick inside).
2. **The hand glow over a looping tile.** In the game one glow stays from the first tick until the status ends (12 s, or until
   the next hits spend the 6 stacks), and a new charge within that time does not add a second one (:20045). Recommended:
   **`kill` 10 + the new `single` option** (one glow at a time, gone 10 s after it first came). Fallback without the page
   part: `kill` 2.1 (the glow ends with the 3.1 s loop and comes again 0.5 s into the next cAttack2).
3. **getUp's voice.** RPC_revive plays `revive` at 0 with the getUp clip; RPC_ko's getUp is silent. Recommended: **yes, the
   optional `getUp` entry, `revive` at p 0.5** (decision 11's shape for the KO tile), and the same entry for every class that
   has `voices/revive` (Wolf, Sheep, Penguin, Bat, Bison and the rest: each class's RPC_revive has the same line; a cross-class
   change for the editor of each, so the user may prefer to keep getUp silent everywhere as today).
4. **Normal Attack's first-step fade.** nAttack1 cuts in the game (:16857); the page fades a sequence's first step 0.2 s unless
   it has `!`. Recommended: **keep the fade** (`nAttack1@0.6`), as the Sheep, Penguin and Bat (Bat decision 28).

## Offer for the Bible

These look new; `cat-skill-reference.md` has the stage starts and hit times (`:497-504`) and the charge ranks (`:279-282`), but not:
- the voice and swing-sound times per stage: voice at 0.2 / 0 / 0 / 0 s and swing at 0.2 / 0.1 / 0.1 / 0.1 s into stages 1-4,
  the dust at 0.1 / 0.1 / (none) / 0 s (:16320-17256, :17860-17934, :18768-18905);
- the press windows: stage 2 at 0.3-0.6 s, stage 3 at 0.9-1.2 s, stage 4 from 1.7 s, open until 1.9 s (:8038-8162);
- the charge loop at 0.5 s and the ticks at 1, 2, 3 s after the press (:20121, :19728, :19963-19971), full at the third tick with
  Double Focus; the ticks, rings and the hand glow only in missions / arena (`mGameType > 4`, :19955);
- that the `count <= lv + 1` test (:19981) is always true after the clamp (:19976), so the ring and the "DamagePlus" text come
  on every tick, also when full (a harmless leftover);
- that the hand glow (`damagePlus`, on mount_Hand_R) lasts as long as the status (StatusControl), not the charge;
- that the mission's activateIcon1 loops the battle clip (:48622).

## Verification

Checker `verify_a`, 2026-11-13 (home PC), read only. Re-traced with `clip_flow.js` (every RPC in this report:
RPC_nAttack1-4, RPC_cAttack1, RPC_ko, RPC_dead, RPC_revive, RPC_activateIcon1, RPC_emotion), the dispatcher
`doNormalAttack` (Cat.cs:8022-8198), the opaque predicates on the effect / voice / wait paths worked by hand, and a fresh
read-only probe of every cued effect (`checks/fx_cat_research/verify_a/probe.json`). Checked: every time, wait, clip fade,
position, offset, random pick, rank and gate in the tables, the "why" texts and the paste-ready cues; the clip lengths
(`data/cat/clips.json`); the rip's voice / sound files; the Bible rows cited (cat-skill-reference.md:279-281, :468,
:501-504); the TTO function lines (pseudo/Cat.c:2411, :16797, :17578, :18331, :19286); chaAdjust(12) = 12 at CHA 1 / LCK 1
(CharacterControl.cs:20592-20610); StatusControl's 0.5 s status poll (StatusControl.cs:50, :82-110); `mount_Hand_R` in
`data/cat/rig.json`. All of it holds: no time, name, position, pick or rank is wrong, and the paste-ready blocks are valid
JSON with every key a Cat clip (battle, ko, getUp are base-tab clips; the others emote / skill).

Confirmed in particular: the stage starts 0.6 / 1.2 / 1.7 s (Yield(2, actionTime - now + 0.6 / 1.2 / 1.7) :17609, :18538,
:19511; press windows :8038-8046, :8098-8106, :8162); the dust offsets TransformDirection(-0.1, 0, -0.25) (:16332) and
(-0.4, 0, 0) (:17209), at the hero on stage 4 (:18780); the charge ticks at press + 1, 2, 3 s, mission / arena only
(:19728, :19955-19971), the ring on every tick (the `<= lv + 1` test after the clamp, :19976-19981), the glow once
(`if (aXHRRIdoYe) goto` :20045-20053) on mount_Hand_R (:20077-20087); deadEffect always in RPC_dead (IL_542 :49517-49527,
predicates 92492 - 473760 = -381268, 298532 - 514853 = -216321, 141446 - 286209 = -144763 != -144762); chat1-5
(`Random.Range(1, 6)` :43297; the rip has chat1-5, unlike the Bat's chat1-3).

Corrections (no paste-ready block changes):

1. **When the hand glow stacks** (Read this first 5, Parts needed 2, Open question 2). A skill tile plays once and then the
   idle stance with its effects running on (index.html:1339-1357 `play`, `mode = "back"`); the 3.1 s loop that would stack
   four `kill` 10 glows happens only with the skill tab's วนซ้ำ toggle on (`skillLoop`, index.html:1343, :1350-1353). Without
   the toggle a single play shows one glow for 10 s and the stacking question does not arise.
2. **`single` should renew the live glow, not only skip.** Each tick re-adds damagePlus (RPC_AddStatus :20031) and a re-add
   keeps the longer of the remaining and the new duration (`sTime = Mathf.Max(FloorToInt(statusClass.sTime - Time.time),
   sTime)`, CharacterControl.cs:14035), so while the Cat keeps charging the status, and the StatusControl'd glow
   (StatusControl.cs:104-110), never lapse. As specified ("skip this spawn while a copy lives"), the looped tile would show a
   gap: glow spawned 1.0 s into the tile, killed at 11.0 s, the ticks at 4.1 / 7.2 / 10.3 s skipped, the next glow only at
   13.4 s (2.4 s without one every fourth loop). Recommended spec for the part: with `single`, a cue whose effect already
   lives does not spawn a second copy and **resets that copy's kill** (its `killAt` = its age + the cue's `kill`): the game's
   one glow, kept alive by every charge, gone 10 s after the last one. The paste-ready `cAttack2` cue stays as written.

Not changed (checked, judgement calls already flagged as questions): the 10 m target point is out of every combo box
(3 m long from 1 m behind, :16520, :18972), so no hit effects; the `mGameType > 4` precedent; getUp's `revive` at p 0.5
(question 3).
