# Monkey effects + sounds research: Combo (nAttack1-2), Mike Blink, HP Transfer (cAttack1-2), emotes, basic moves, KO

Short summary: The Monkey's Normal Attack (Combo) is two stages: nAttack1, then nAttack2 cut in with the game's 0.2 s
crossfade at **0.5 s** (not after the whole 1.43 s clip). Mike, the worn weapon (slot R), flies out about 5 m in the
clip itself; the hit boxes reach 7 / 7.5 m, so nothing is drawn at the 10 m target. The Combo has hero-played sounds and
voices only. Mike Blink #401 (a passive) replaces the Combo on a far target: Mike teleports onto the `mikeBlink` effect
at the target and strikes twice. That needs one new page part (a copy of the R piece on the effect's `mount_Summon`
node). The Charge Attack is **HP Transfer**: a heal beam (`hpTransfer`, a BoltEmitter, the Bat's Drain Life shape) to
an ally, plus Mike Circle's `mikeCircle` on that ally. Emotes: only hi / wave have a voice (`hi`). KO uses single
`ko` / `dead` voices with `deadEffect`. The run plays `step_normal1` on both feet. 8 cue entries, 23 cues.

Scope: the clips nAttack1, nAttack2 (RPC_nAttack1, RPC_nAttack2, their dispatcher `doNormalAttack`, and the passive
Mike Blink's RPC_mikeBlink1 / RPC_mikeBlink2 on the same clips), cAttack1, cAttack2 (RPC_cAttack1 = HP Transfer,
`doBeginCharge`, `doReleaseCharge`, the release RPC_cAttack0), the emotes (RPC_emotion), the basic moves (run, falling,
getUp, root, battle), KO (RPC_ko, RPC_dead, RPC_revive), and the TTO-only emote clips. Research only (recipe steps 1-3),
office PC, 2026-11-13. Line numbers are `C:\Users\Jump\Desktop\12tails\DecompiledSource\Monkey.cs` (the home PC's
`D:\12tails\...`) unless another file is named. Times are seconds from the start of the clip the cue is keyed by.
Distance 0 = at the hero. Every opaque predicate on the paths below was evaluated by
`checks\fx_monkey_research\attacks_emotes\preds.py`, which tags each `if (a - b ==/!= c)` line T / F; each one goes the
normal way.

Probes (read only, nothing written outside `checks\`), all in `checks\fx_monkey_research\attacks_emotes\`:
- `probe.txt`: `wardrobe_fx.py monkey --probe hpTransfer,mikeCircle,nAttack_hit,deadEffect,mikeBlink`;
- `probe_firerune.txt`: `--probe fireRune_hit`;
- `probe_fields.py` / `probe_fields.txt`: the Monkey MonoBehaviour's PPtr fields on the hero prefab, and the
  AnimationEvents on the prefab's own clips;
- `rip_events.txt`: every `animations/*.prefab` of the Monkey mapped by guid to its rip `.anim`, with its events;
- `tto_audio.txt`: TTO's catalog addresses under `heroes/monkey/voices|sounds` (`tto_assets/2026-11-09`);
- `clip_calls.txt` (`node pipeline/clip_calls.js <Bible>/DecompiledSource wardrobe/data monkey`), the `clip_flow.js` dumps
  `RPC_nAttack1.txt` ... `RPC_activateIcon1.txt`, and the predicate dumps `*_pred.txt`, `doNormalAttack.txt`,
  `charge_dispatch.txt`;
- `cues.json`: every paste-ready entry below (parses as JSON).

TTO: `DecompiledSource_TTO_2026-11-02\pseudo\Monkey.c` (TTO1102) has the same coroutines with the same literals:
- `<RPC_nAttack1>d__165` :12500, `<RPC_nAttack2>d__166` :13015 (sounds / voices nAttack1 / nAttack2, the boxes 7 and
  3.5 / 4, `w_mnk59`);
- `<RPC_cAttack1>d__170` :1475 (mikeCircle, 0.88, 0.15, `hasSkill(0x19b)` = #411, "Target is too far");
- `<RPC_cAttack0>d__171` :1347 (root 0.35);
- `<RPC_mikeBlink1>d__227` :11343 and `<RPC_mikeBlink2>d__228` :12041 (mikeBlink, mount_Summon, voices/mikeBlink).

TTO moved the emotes and KO into BaseHero (`pseudo/BaseHero.c` :1900, :2391, :1217, :3940). The Monkey overrides only
the voice names: `Monkey::EmotionVoiceClip` returns `hi` for emo_hi / emo_wave and nothing else (:41199-41221),
`KoVoiceName` returns `ko` (:41239) and `DeadVoiceName` returns `dead` (:41252). TTO's waits are opaque, so the BB times
stand. Nothing in this scope is TTO-only, so the released-list rule does not come in. The TTO-only emote clips stay
silent, `clap` and `wai` included (both released).

---

## Read this first

1. **The Normal Attack SEQ (index.html work, not a cue job).** Today: `"Normal Attack: nAttack1 nAttack2~"`, which plays
   the whole 1.43 s nAttack1 first.
   - Stage 2 is pressed while stage 1 attacks, before stage 1 + 0.5 s, with #101 (`doNormalAttack` :9912-9958).
   - RPC_nAttack2 then waits `Yield(2, actionTime - Time.time + 0.5)` (:20770). actionTime is stage 1's (:20142), so the
     clip comes at **0.5 s**.
   - The clip uses `PlayAnimation("nAttack2", 0.2f)` (:20412), a 0.2 s crossfade (PlayAnimation :1133-1160).
   - **Proposed: `"Normal Attack: nAttack1@0.5 nAttack2~"`.** The first step keeps the page's fade, which is also the
     game's (`PlayAnimation("nAttack1", 0.2f)` :20157).
   - The clips fit each other: Mike is 5.26 m out at 0.53 s of nAttack1 and starts nAttack2 at 5.02 m
     (`mount_Summon` in data/monkey/clips.json).
2. **Mike Blink #401 gets its own tile on the same clips** (one tile per skill; the Chameleon's Critical Plus / Clear
   Arrow precedent, decisions 12-13).
   - Passives are on, but the game picks Mike Blink only for a locked enemy **more than 12 m** away, in a mission
     (`sqrMagnitude > 144` :10076-10142). The tile's 10 m target therefore gets the Combo, and Mike Blink shows on its own
     tile at the same 10 m point (question 1).
   - **Proposed: `"Mike Blink: nAttack1@0.5 nAttack2~"`** (RPC_mikeBlink2's clip also comes at stage 1 + 0.5 s, :36798;
     its fade is 0.2 s, :36486).
   - Keys: `@MikeBlink:nAttack1`, `@MikeBlink:nAttack2`. Add `SEQ_SKILL.monkey["@MikeBlink"] = "mikeBlink"` (the icon
     `icons/skills/monkey/mikeblink5.webp` exists).
3. **Mike Blink moves the worn weapon itself** (part P1 below).
   - At 0.3 s the game instantiates `mikeBlink` at the target's feet (`mPos + tDir` :35907; `tDir` = target - hero
     :10111) with `LookRotation(flat tDir) * Euler(270, 90, 0)`.
   - It then re-parents `mWep1` (Mike: the page's slot **R**, whose placement is the `mount_Summon` bone,
     data/placements.json `weapons.monkey.fallback`) onto the effect's `mount_Summon` node, at localPosition 0 and
     localRotation identity (:35920-35943).
   - `mikeBlink` (probe) is an Animation-only prefab: the 1.1 s clip `root` flies that node. With nothing parented to it,
     the page would draw nothing.
   - `resetMikeBlink` (:14015-14058) puts Mike back on the hero's `mount_Summon` and destroys the effect. That happens at
     stage 2's 0.5 s (:36707), or at stage 1's 0.7 s when no stage 2 was pressed (:36101-36117).
4. **HP Transfer is the Charge Attack, and the tile needs a hold.** Today: `"Charge Attack: cAttack1 cAttack2*"`, a 1.5 s
   hold.
   - cAttack1 is cut in and changes to cAttack2 at **0.7 s** (`Yield(2, 0.7)` :21594; that is also the clip's own
     length), then cAttack2 is cut in and looped (:20969-20974).
   - The channel runs until the player lets go (`doReleaseCharge` :10650-10673), the ally is fully healed, or it moves
     more than 30 m away (:21198-21219). By the SEQ rule ("three hits, at least 3 s"), three 1 s ticks give a **3.2 s**
     hold (the Bat's Drain Life alternative, plans/fx_bat/attacks_emotes.md "3.2 s hold").
   - **Proposed: `"HP Transfer: cAttack1 cAttack2*@3.2"`** (renamed as the Bat's "Drain Life", question 4). The release
     (RPC_cAttack0: `PlayAnimation("root", 0.35f)` :21851, standby 0.35 s later) draws nothing, so the tile's own fade back
     to the start covers it (as the Bat's).
5. **HP Transfer's target is an ally at the 10 m target point.**
   - Sheep decision 1 shows ally skills as self-casts because the game lets the Sheep target herself. HP Transfer refuses
     that ("Cannot use hpTransfer on self" :10445-10452; enemies are refused too, :10456-10463).
   - So the ally stands at the 10 m point, as Revive's ally does (Sheep decisions 1 and 4). Its body is the Bat
     decision 4 one: centre 0.6 m up, radius 0.3, height 1.
   - The beam ends at `bounds.center - forward x 2 x bounds.extents.x` (:20996, :21184) = **(0, 0.6, 9.4)**.
   - Mike Circle's `mikeCircle` sits at `bounds.center - 0.15 up` (:21067) = **d 10, y 0.45**.
6. **Mike Circle #411 is on (passives rule).** At cAttack2's start it puts `mikeCircle` on the ally (:21037-21067). That
   is its only look, so it also gets its own tile (question 5): `"Mike Circle: cAttack1 cAttack2*@3.2"`, with
   `SEQ_SKILL.monkey["@MikeCircle"] = "mikeCircle"` (icon `mikecircle5.webp`). It needs no cue key of its own: the
   `cAttack2` entry is the fallback.
7. **Hero-played sounds (`"sound"` cues: the hero's `audio.PlayOneShot`, no effect carries them).**
   - Combo: `Sounds/nAttack1` at 0.2 s (:19895-19907) and `Sounds/nAttack2` at 0.1 s of stage 2 (:20509-20521).
   - Mike Blink: `Sounds/nAttack1` at 0.3 s (:35862-35874), `Sounds/nAttack2` at 0.1 s (:36531-36543), and on each strike
     `Sounds/nAttack_hit` (RPC_nAttack_hit :10773-10798, with a 0.1 s gate). The `nAttack_hit` prefab has no AudioSource.
   - Run: the AnimationEvents `playLeftFootEvent` at 0.1 s and `playRightFootEvent` at 0.4 s (rip `run.anim`; the only
     events on any Monkey clip, `rip_events.txt`). They play the fields `footStep_left` / `footStep_right` (:101-155,
     :19249, :19252). **Both** fields are `step_normal1` (probe_fields.txt offsets 24 / 32), which lives in
     `Resources/sound/fx/` and is reached by `hero_sound_wav`'s fallback.
   - The effects that bring their own sound: `hpTransfer` (`hpTransfer`, looped) and `fireRune_hit` (`fireRune`).
8. **Voices are few.** The rip's `heroes/monkey/voices/` has nAttack1, nAttack2, mikeBlink, hi, ko and dead among the
   ones this scope asks for. TTO's catalog has the same set and no revive (`tto_audio.txt`).
   - RPC_emotion loads only `Voices/hi`, for emo_hi and emo_wave (:46080-46113). Every other emote is silent.
   - RPC_ko loads `Voices/ko` and RPC_dead `Voices/dead`: one file each, no random pick (:51870, :52202).
   - RPC_revive loads no voice in BB (`RPC_revive.txt`). TTO's BaseHero asks for `Voices/revive`, which neither game has,
     so getUp is silent.
9. **Mission gates (kept shown, Chameleon decision 42 / Cat decision 38).** These play only in a mission or arena, for
   the own team (`mGameType > 4`, `mTeam`): every voice here (nAttack1 :20175, nAttack2 :20430, mikeBlink :36235, ko
   :51852, dead :52184), and `hpTransfer` / `mikeCircle` (:21021). The footsteps and the Combo / blink sounds play for
   the own hero anywhere.
10. **No MP / SP transfer style skill plays an attack clip.** Only RPC_nAttack1 / RPC_mikeBlink1 play nAttack1 (:20157,
    :36205), and only RPC_nAttack2 / RPC_mikeBlink2 play nAttack2 (:20412, :36486). Only RPC_cAttack1 plays cAttack1 /
    cAttack2 on the hero, plus RPC_activateIcon1's mission channel (cAttack2 with a 0.5 s fade :51520; no tile, Penguin
    decision 19). Earth Form's `mGadinaArmor.animation.Play("nAttack1" / "nAttack2" / "cAttack1" / "cAttack2")` (:41444,
    :41836, :42918, :42786) runs on the armour's own Animation, not the hero (other reports' scope).
11. **Other skills that take over the normal attack** (not cued here; for the reports that own them):
    - Fire Keep's stored ball replaces it from standby / run (`RPC_fireKeep_cast` on cast3, :10020-10058);
    - in Fire Avatar it becomes `RPC_phoenixArmor_nAttack` (:9689-9741), in Earth Form `RPC_gadinaArmor_nAttack1-3`
      (:9749-9888);
    - with a Lavu summon out, the charge becomes Upheaval (:10364-10411); in a form it becomes Blazing Form / Sentinel
      Guard (:10208-10351).
12. **Name collisions** (the cue kind picks the folder; voices are saved as `v_<name>`):
    - `nAttack1` and `nAttack2` are clips, `voices/` files and `sounds/` files;
    - `mikeBlink` is an effect and a voice;
    - `hpTransfer` and `fireRune` are sounds their effects play themselves (`hpTransfer` is also the effect);
    - `nAttack_hit` is an effect and a `sounds/` file (the hero plays the sound);
    - `ko` is a clip and a voice; `dead` is a voice and the KO roll's name;
    - `step_normal1` lives in `Resources/sound/fx/` only.

---

## The dispatchers

- **`doNormalAttack`** (:9603-10180): own hero (:9610), and not game code 967 (`useItem("f_wtb1")` :9617-9633, an event
  mode).
  - The aim is `vector2 = flat(a - position).normalized` (:9644-9647).
  - Form branches: Fire Avatar :9689, Earth Form :9749.
  - Combo stage 2 needs attack + myCommand nAttack1 + #101 + `Time.time < actionTime + 0.5` (:9912-9958).
  - Mike Blink stage 2 has the same window after mikeBlink1 (:9964-10014).
  - Fire Keep (:10020-10058). Then, if the `nAttack` timeout is free (:10067), Mike Blink takes over when #401 is
    learned, a locked target exists, it is a mission (`mGameType > 4`), the target is an enemy (another layer) and more
    than 12 m away (:10076-10119). Mike Blink's `vector2` is the raw `target.position - position` (:10111), so the blink
    lands at the target's feet. Otherwise it is Combo stage 1 (:10150).
- **`doBeginCharge`** (:10183-10553): forms and Lavu first (above). HP Transfer then needs:
  - standby or run (:10414-10422);
  - a target that is not herself, not an enemy, a CharacterControl with ActorNr != 0 and `recieveHeal` (:10429-10507);
  - HP above 1, #111 learned, more than 1 s since the last action, and the `cAttack` timeout free (:10486-10521).
  Then RPC_cAttack1 (:10525).
- **`doReleaseCharge`** (:10557-10716): while attacking with cAttack1, RPC_cAttack0 (:10650-10673).
- **RPC_cAttack0** (:21693-21866): attack / cAttack0 (:21836-21842), `PlayAnimation("root", 0.35f)` (:21851), standby
  0.35 s later (`Yield(2, 0.35)` :21865, :21811). No voice, no effect: no tile, no cue.

---

## nAttack1 (Combo stage 1)

Coroutine `RPC_nAttack1` (`$RPC_nAttack1$24334` :19746, MoveNext :19850-20247).

| t (s) | what | source |
|---|---|---|
| 0 | attack, actionTime, myCommand nAttack1, `addTimeOut("nAttack", 1.5)`, LookAt, **`PlayAnimation("nAttack1", 0.2f)`**, Once, moveSpeed 0; voice **`Voices/nAttack1`** (pvoice, mission / arena, own team; volume 1 for the own hero); wait 0.2 | :20139-20166, voice :20169-20213 / PlayOneShot :20243, `Yield(2, 0.2)` :20233 |
| 0.2 | still attack (:19864): own hero, or anyone in a mission (:19874-19888): **`Sounds/nAttack1`** (load :19895, PlayOneShot :19907); wait 0.2 | `Yield(3, 0.2)` :20241 |
| 0.4 | own hero in a mission / arena (:19936-19950): `FindRecTarget(position, forward, 1, 1, 7, 2)` (:19957), a box from the hero to 7 m; per hit `hit(99, ...)` with `(0.5 + 0.1 #401) x ATK` (:19962), KO 1 (+1 #433, +2 `w_mnk59` :19967-19999), RPC_nAttack_hit, onNormalAttackHit, SP + 1, FireRune (:20019-20060); wait 0.8 | `Yield(4, 0.8)` :20229 |
| 1.2 | still attack with nAttack1: standby | :20075-20097 |

- **The hit draws nothing at 10 m.** FindRecTarget keeps a body when its nearest point toward the far end lies inside
  the box (Damage.cs:1416-1625). The 10 m body's nearest point is 9.7 m, past the box's 7 m. So `nAttack_hit` (:10734),
  Fire Rune and the gear procs, which come only on a hit, stay out (the Wolf's / Cat's melee convention).
- Mike (slot R on `mount_Summon`) flies out and back in the clip itself: `mount_Summon` is at x 5.26 at 0.53 s, back by
  1.23 s (data/monkey/clips.json). No effect is spawned for the swing. ("Cannot find nAttack1_fx" :19916 names the sound.)

## nAttack2 (Combo stage 2)

Coroutine `RPC_nAttack2` (`$RPC_nAttack2$24348` :20296, MoveNext :20380-20785).

| t (s) | what | source |
|---|---|---|
| press | attack, myCommand nAttack2; wait to stage 1 + 0.5 s | :20753-20756, `Yield(2, actionTime - Time.time + 0.5)` :20770 |
| 0 | still attack (:20392): moveSpeed 0, `addTimeOut("nAttack", 1.5)`, **`PlayAnimation("nAttack2", 0.2f)`**, Once; voice **`Voices/nAttack2`** (same gates); wait 0.1 | :20402-20417, voice :20422-20452 / PlayOneShot :20775, `Yield(3, 0.1)` :20764 |
| 0.1 | own hero or anyone in a mission: **`Sounds/nAttack2`**; wait 0.2 | :20488-20521, `Yield(4, 0.2)` :20780 |
| 0.3 | own hero in a mission: `FindRecTarget(position + 3.5 forward, forward, 1.5, 1.5, 4, 2)` (:20571): 3.5-7.5 m, the 10 m body is missed; wait 0.8 | `Yield(5, 0.8)` :20773 |
| 1.1 | standby | :20689-20711 |

```json
  "nAttack1": {
    "why": "Monkey.cs RPC_nAttack1 (:19746-20290), Combo stage 1 (doNormalAttack :10150, no Mike Blink target, no fireKeep status, no form): at 0 the clip with a 0.2 s fade (PlayAnimation(nAttack1, 0.2) :20157; PlayAnimation = CrossFade for a fade > 0, :1133-1160) and the voice nAttack1 (mission / arena, own team: pvoice :20169, mGameType > 4 :20175, mTeam :20181; load :20193, PlayOneShot :20243; then Yield(2, 0.2) :20233); 0.2 s, still attacking (:19864): the hero's PlayOneShot of Sounds/nAttack1 (own hero, or anyone in a mission: :19874-19888; load :19895, PlayOneShot :19907; then Yield(3, 0.2) :20241); 0.4 s the hit, FindRecTarget(position, forward, 1, 1, 7, 2) (:19957): a box 0-7 m ahead, so the 10 m body (nearest point 9.7 m) is not hit and nAttack_hit / Fire Rune / onNormalAttackHit (:20025-20060, only on a hit) draw nothing; Mike (the worn R piece on mount_Summon) flies out about 5 m and back by the clip itself; standby 1.2 s (Yield(4, 0.8) :20229, :20087) unless stage 2 was pressed (its clip at 0.5 s: RPC_nAttack2's Yield(2, actionTime - now + 0.5) :20770, the press window doNormalAttack :9912-9958)",
    "cues": [
      [0, "voice", "nAttack1"],
      [0.2, "sound", "nAttack1"]
    ]
  },
  "nAttack2": {
    "why": "Monkey.cs RPC_nAttack2 (:20296-20784), Combo stage 2 (doNormalAttack :9942, pressed while attacking with myCommand nAttack1, #101 learned, before stage 1 + 0.5 s :9912-9938): the entry sets attack / nAttack2 (:20753-20756) and waits to stage 1 + 0.5 s (Yield(2, actionTime - Time.time + 0.5) :20770; actionTime is stage 1's); at 0 moveSpeed 0, the clip with a 0.2 s fade (PlayAnimation(nAttack2, 0.2) :20412) and the voice nAttack2 (mission / arena, own team: :20422-20444, load :20452, PlayOneShot :20775; then Yield(3, 0.1) :20764); 0.1 s: the hero's PlayOneShot of Sounds/nAttack2 (own hero, or anyone in a mission: :20488-20500, load :20509, PlayOneShot :20521; then Yield(4, 0.2) :20780); 0.3 s the hit, FindRecTarget(position + 3.5 forward, forward, 1.5, 1.5, 4, 2) (:20571): 3.5-7.5 m ahead, so the 10 m body is not hit (nAttack_hit / Fire Rune only on a hit, :20639-20674); standby 1.1 s (Yield(5, 0.8) :20773, :20701)",
    "cues": [
      [0, "voice", "nAttack2"],
      [0.1, "sound", "nAttack2"]
    ]
  },
```

Sure: high on the trace and the times. The voices need a mission (shown, item 9).

---

## Mike Blink (#401) on nAttack1 / nAttack2

Coroutine `RPC_mikeBlink1` (`$RPC_mikeBlink1$24707` :35713, MoveNext :35821-36314).

| t (s) | what | source |
|---|---|---|
| 0 | attack, actionTime, myCommand mikeBlink1, timeout 1.5, LookAt, **`PlayAnimation("nAttack1", 0.2f)`**, moveSpeed 0; an old mikeBlink destroyed; voice **`Voices/mikeBlink`** (pvoice, mission, own team); wait 0.3 | :36187-36224, voice :36229-36253 / PlayOneShot :36288, `Yield(2, 0.3)` :36304 |
| 0.3 | still attack (:35831): own hero or anyone in a mission: **`Sounds/nAttack1`**; **`Effects/mikeBlink`** at `mPos + tDir` (the target's feet), `LookRotation(flat tDir) * Euler(270, 90, 0)`; `mWep1` (Mike, slot R) parented to its `mount_Summon`, local 0 / identity; wait 0.2 | :35841-35874, :35889-35943, `Yield(3, 0.2)` :36299 |
| 0.5 | own hero (:35977): `FindRecTarget(target - 3 hitDir, tDir, 1, 1, 4, 2)` (:35995): 7-11 m, **the 10 m body is hit**; RPC_nAttack_hit at `ClosestPointOnBounds(hero + TransformDirection(0, 0.9, 5))` (:36051, :36061); onNormalAttackHit; SP + 1; **FireRune** (:36086); wait 0.2 | `Yield(4, 0.2)` :36310 |
| 0.7 | still attack with myCommand mikeBlink2: Mike stays; else `resetMikeBlink()` | :36101-36117 |
| 1.2 | standby (if still mikeBlink1) | `Yield(5, 0.5)` :36291, :36123-36145 |

Coroutine `RPC_mikeBlink2` (`$RPC_mikeBlink2$24723` :36370, MoveNext :36456-36811), started at a press within 0.5 s:

| t (s) | what | source |
|---|---|---|
| press | attack, myCommand mikeBlink2; wait to stage 1 + 0.5 s | :36778-36781, `Yield(2, ...)` :36798 |
| 0 | moveSpeed 0, timeout 1.5, **`PlayAnimation("nAttack2", 0.2f)`**; no voice; wait 0.1 | :36476-36496, `Yield(3, 0.1)` :36803 |
| 0.1 | **`Sounds/nAttack2`**; wait 0.2 | :36510-36543, `Yield(4, 0.2)` :36789 |
| 0.3 | own hero in a mission, the effect alive: `FindAreaTarget(mikeBlink.position, 1, 3)` (:36601): the body is hit; nAttack_hit at `ClosestPointOnBounds(mikeBlink + TransformDirection(0, 0.9, 5))` (:36657); FireRune (:36692); wait 0.2 | `Yield(5, 0.2)` :36807 |
| 0.5 | **`resetMikeBlink()`**: Mike back on the hero's `mount_Summon` (localScale 1), the effect destroyed; wait 0.6 | :36707, :14015-14058, `Yield(6, 0.6)` :36809 |
| 1.1 | standby | :36714-36736 |

- **Where things land** (the target's body, Bat decision 4: centre 0.6 up, radius 0.3, height 1, box x +-0.3, y 0.1-1.1,
  z 9.7-10.3):
  - `mikeBlink`: d 10, y 0, rot [270, 90, 0]. It lives from 0.3 s of stage 1 to stage 2's 0.5 s (1.0 s): **kill 0.7**.
  - Strike 1's `nAttack_hit`: ClosestPointOnBounds of (0, 0.9, 5) = **d 9.7, y 0.9**, the hero's rotation
    (`Instantiate(nAttack_hit, hitPos, transform.rotation)` :10759).
  - Strike 2's: ClosestPointOnBounds of (0, 0.9, 15) = **d 10.3, y 0.9**.
- **`nAttack_hit`** (probe): EffectControl life 1, two ImageEmitters (Life 0.3, 1 -> 2.4 m, green-yellow). Ready.
- **`mikeBlink`** (probe): Animation (`root`, 1.1 s, a track on `mount_Summon`, which starts at (3.77, 0.57, 0.95)) and
  no EffectControl, so only the reset ends it (the cue's kill). It needs part P1.
- **Fire Rune 3** (#261-263, passives rule; `FireRune` :12273-12318):
  - own hero only, a 1 s lockout (:12282, :12303);
  - `Random.Range(0, 100) < lckAdjust(12)` (:12297), which is 12 % at LCK 1 (the Cat's lckAdjust convention, decision 40);
  - `RPC_AddHeal(260 + lv, 0, 4 lv MP, 4 lv SP)` (numbers only), and `RPC_fireRune` → `fireRune_hit` at the hero,
    identity (:12357). The probe: EffectControl life 1, followPosition, AudioSource `fireRune`, and `magicRune` (a
    StaticMesh + AlphaTimer). Ready.
  - Both strikes roll on their own (p 0.12 each). The game's lockout forbids a second proc 0.3 s after the first; the
    page shows both on 1.4 % of plays (question 6).
- Left out: onNormalAttackHit's gear procs (happy / charm / needlePrison / heavy / plague / drains on the enemy, heal1 /
  revert on the hero by the worn piece, :52561-53105), as the Chameleon decision 53 status looks on a foe. Damage numbers.

```json
  "@MikeBlink:nAttack1": {
    "why": "Monkey.cs RPC_mikeBlink1 (:35713-36314), Mike Blink #401 (passive): doNormalAttack runs it in place of Combo stage 1 on a locked enemy more than 12 m away in a mission (sqrMagnitude > 144, :10076-10142; shown at the 10 m target point, attacks_emotes Q1); at 0 the clip nAttack1 with a 0.2 s fade (:36205), an old mikeBlink destroyed (:36217-36223), the voice mikeBlink (mission / arena, own team: :36229-36245, load :36253, PlayOneShot :36288; then Yield(2, 0.3) :36304); 0.3 s, still attacking (:35831): the hero's Sounds/nAttack1 (:35841-35874), Effects/mikeBlink at the target's position (mPos + tDir :35907, tDir = target - hero :10111: its feet 10 m ahead) with LookRotation(flat tDir) x Euler(270, 90, 0) (:35907), and the worn Mike (mWep1, the page's R) moved onto its mount_Summon node, localPosition 0, localRotation identity (:35920-35943): the part's copy of R there, the hand's R hidden with its particles; the effect's Animation (root, 1.1 s) flies it; then Yield(3, 0.2) :36299; 0.5 s the strike, FindRecTarget(target - 3 forward, forward, 1, 1, 4, 2) (:35995: 7-11 m, the 10 m body is hit): RPC_nAttack_hit (:36061) = nAttack_hit at ClosestPointOnBounds(hero + TransformDirection(0, 0.9, 5)) = the body's front, d 9.7, y 0.9, with the hero's rotation (:36051, :10759), and the hero's Sounds/nAttack_hit (0.1 s gate, :10773-10798); FireRune (:36086) with Fire Rune 3 on (passives rule): Random.Range(0, 100) < lckAdjust(12) = 12 % at LCK 1 (:12297), 1 s lockout (:12303), fireRune_hit at the hero, identity (RPC_fireRune :12357; plays its own Sounds/fireRune); onNormalAttackHit's gear procs left out; Yield(4, 0.2) :36310; 0.7 s: stage 2 pressed (myCommand mikeBlink2) keeps Mike at the target (:36101-36109), so the reset comes in stage 2 at 0.5 s (1.0 s from here): kill 0.7 after the 0.3 s spawn; standby 1.2 s (Yield(5, 0.5) :36291, :36135)",
    "cues": [
      [0, "voice", "mikeBlink"],
      [0.3, "sound", "nAttack1"],
      [0.3, "fx", "mikeBlink", {"d": 10, "rot": [270, 90, 0], "kill": 0.7, "slot": "R"}],
      [0.3, "hideProp", "R", {"kill": 0.7, "all": true}],
      [0.5, "fx", "nAttack_hit", {"d": 9.7, "y": 0.9}],
      [0.5, "sound", "nAttack_hit"],
      [0.5, "fx", "fireRune_hit", {"p": 0.12}]
    ]
  },
  "@MikeBlink:nAttack2": {
    "why": "Monkey.cs RPC_mikeBlink2 (:36370-36811), Mike Blink's second strike (doNormalAttack :9964-10014: pressed while attacking with myCommand mikeBlink1, #101, before stage 1 + 0.5 s): its clip at stage 1 + 0.5 s (Yield(2, actionTime - Time.time + 0.5) :36798); at 0 moveSpeed 0, nAttack2 with a 0.2 s fade (:36486), no voice; 0.1 s (Yield(3, 0.1) :36803) the hero's Sounds/nAttack2 (:36510-36543); 0.3 s (Yield(4, 0.2) :36789) the strike, FindAreaTarget(the mikeBlink effect's position, 1, 3) (:36601: 1 m round the target's feet, the body is hit): nAttack_hit at ClosestPointOnBounds(mikeBlink + TransformDirection(0, 0.9, 5)) = the body's back face, d 10.3, y 0.9, the hero's rotation (:36657, :36667, :10759), the hero's Sounds/nAttack_hit (:10773-10798); FireRune (:36692): 12 % again (lckAdjust(12) :12297; the game's 1 s lockout after a stage 1 proc 0.3 s earlier is not modelled: both show on 1.4 % of plays); 0.5 s (Yield(5, 0.2) :36807) resetMikeBlink (:36707; :14015-14058: Mike back on the hero's mount_Summon, the effect destroyed: stage 1's kill); standby 1.1 s (Yield(6, 0.6) :36809, :36726)",
    "cues": [
      [0.1, "sound", "nAttack2"],
      [0.3, "fx", "nAttack_hit", {"d": 10.3, "y": 0.9}],
      [0.3, "sound", "nAttack_hit"],
      [0.3, "fx", "fireRune_hit", {"p": 0.12}]
    ]
  },
```

Sure: high on the trace and the times. Medium on how Mike looks on the effect: it is the copy at the node's pose, and the
hero's own `mount_Summon` motion in nAttack1 / nAttack2 is no longer Mike's (the game moved the real piece).

---

## cAttack1 (HP Transfer: the start)

Coroutine `RPC_cAttack1` (`$RPC_cAttack1$24358` :20828, MoveNext :20942-21598), entry IL_122A (:21505):

| t (s) | what | source |
|---|---|---|
| 0 | the target from `ActorNrList[tID]`: none (or no CharacterControl) = the coroutine ends (:21507-21531); LookAt it (flat); attack, actionTime, myCommand cAttack1, moveSpeed 0; **`PlayAnimation("cAttack1", 0)`** (cut), Once; wait 0.7 | :21536-21566, `Yield(2, 0.7)` :21594 |
| 0.7 | case 2: the change to cAttack2 (next section) | :20956 |

No voice, no `Sounds/` load and no effect in this part (`RPC_cAttack1.txt`), so cAttack1 gets **no entry**.

## cAttack2 (HP Transfer: the beam)

Same coroutine, case 2 at 0.7 s, then every frame (`YieldDefault(3)` :21596). Times below are from cAttack2's start.

- **0** (case 2, still attack / cAttack1, :20957-20963):
  - `PlayAnimation("cAttack2", 0)` looped (:20969-20974); `hpTransferTimer = now + 1` (:20981); Damage Cast level
    (:20986), its timer now + 0.2 (:20991); `targetOffset = 2 x bounds.extents.x` (:20996); Mike Circle timer now + 0.5
    (:21016);
  - in a mission / arena (:21021): **`Monkey_hpTransfer`** at `position + TransformDirection(0, 0.82, 0.88)`, identity
    (:21027). This is the prefab field at offset 40 = `effects/hpTransfer` (probe_fields.txt); its BoltEmitter is taken
    at :21032;
  - with #411 and a target (:21037-21043): **`mikeCircle`** by the target's own `createEffect` (:21067) at
    `bounds.center - 0.15 up`, `rotation * Euler(270, 90, 0)`;
  - charge level 5 with #411 (`getChargeAttackLv` :10827-10884), so the cost is `2 x 5 - 1` = 9 HP and the heal is
    `floor((1 + 0.02 ATK) x 10)` (:21084-21094).
- **Every frame** while attack / cAttack1 and the target lives (:21109-21156):
  - LookAt the target (:21158-21168);
  - hpTransfer kept at `TransformDirection(0, 0.82, 0.88)` (:21179), its bolt to `bounds.center - forward x targetOffset`
    (:21184);
  - more than 30 m = "Target is too far" and RPC_cAttack0 (:21198-21219).
  - In a mission (:21225):
    - every 1 s, when HP > 9 and the ally is below max: the cost on the Monkey (`RPC_AddEffectDamage` :21256) and the
      heal on the ally (doubled on the Monkey's own summon, :21261-21275). Numbers only (CharacterControl.cs:6058,
      :7130: no effect);
    - Damage Cast every 0.4 s: `FindAreaTarget(Monkey, 2, 2)` (:21299-21373), no enemy;
    - Mike Circle every 0.5 s: `FindAreaTarget(target, 3, 2)` (:21383-21464), no enemy near the ally.
- **The release** (myCommand changes, RPC_cAttack0 :10662): `Destroy(hpTransfer)`, `Destroy(mikeCircle)` (:21475-21493).
- `hpTransfer` (probe): BoltEmitter (3 bolts, Height 0.2, widths 0.1 / 0.08-0.05, rndZigg 0.05, green -> yellow -> red,
  TargetNode -1, the stale TargetPosition (250, 54, 150)), AudioSource `hpTransfer` (loop, playOnAwake), a Point light
  ((0.60, 1, 0.54), intensity 1, range 1). Material `Line_DoubleEdge1`. No EffectControl. **Ready**: the Bat's
  `drainLife` shape (BoltEmitter `to`, fxparts/light.js).
- `mikeCircle` (probe): Animation `root` 1.333 s, Loop (two Mikes, geoMike and pyroMike, circling on `mikeCircle_ctrl`),
  EffectControl life 99 with followPosition (owner = the ally, who stands), two TrailEmitters (`earthRay`). Ready (the
  inventory).
- Both have no end of their own, so: **kill 3.15** in the 3.2 s step (the Bat's hold - 0.05).
- TTO1102 `<RPC_cAttack1>d__170` (pseudo/Monkey.c:1475-2417): the same strings and `hasSkill(0x19b)` (:1680, :2253),
  0.88, 0.15, 900.

```json
  "cAttack2": {
    "why": "Monkey.cs RPC_cAttack1 (:20828-21598), HP Transfer (Charge Attack #111-114; doBeginCharge :10414-10537 needs a friendly target, never the Monkey herself :10445-10452: the ally at the 10 m target point, its body 0.6 m up, radius 0.3, Bat decision 4): cAttack1 cut in at 0 (PlayAnimation(cAttack1, 0) :21563), no voice, no sound, no effect, then Yield(2, 0.7) :21594; case 2 at 0.7 s (times from this clip): cAttack2 cut in, looped (:20969-20974); mission / arena (mGameType > 4 :21021, kept as the Sheep / Penguin / Chameleon precedent): the prefab field Monkey_hpTransfer (= effects/hpTransfer, checks/fx_monkey_research/attacks_emotes/probe_fields.txt offset 40: BoltEmitter, Point light, its own looping Sounds/hpTransfer) at position + TransformDirection(0, 0.82, 0.88), identity (:21027), kept there every frame (:21179), its bolt's TargetPosition = the target's collider.bounds.center - forward x 2 x bounds.extents.x (:20996, :21184) = (0, 0.6, 9.4): to; Mike Circle #411 on (passives rule): mikeCircle created by the target (createEffect :21067, CharacterControl.cs:24191-24214) at its bounds.center - 0.15 up = d 10, y 0.45, the hero's rotation x Euler(270, 90, 0) (EffectControl life 99, followPosition on the standing target; its Animation circles the two Mikes, TrailEmitters); neither has an end of its own: Object.Destroy the frame after the release (:21475-21493): kill 3.15 in the 3.2 s step; the ticks every 1 s (hpTransferTimer :20981, :21233-21275: the HP cost and the heal, numbers only, CharacterControl.cs:6058, :7130), Damage Cast's hits every 0.4 s within 2 m of the Monkey (:21299-21373) and Mike Circle's every 0.5 s within 3 m of the ally (:21383-21464) reach no enemy: nothing drawn; the release RPC_cAttack0 (doReleaseCharge :10650-10673; :21836-21865: CrossFade(root, 0.35), standby 0.35 s later) draws nothing",
    "cues": [
      [0, "fx", "hpTransfer", {"y": 0.82, "d": 0.88, "to": [0, 0.6, 9.4], "kill": 3.15}],
      [0, "fx", "mikeCircle", {"d": 10, "y": 0.45, "rot": [270, 90, 0], "kill": 3.15}]
    ]
  },
```

Sure: high on the trace. The kills follow the proposed 3.2 s hold. With another hold, both kills are the hold - 0.05.

---

## Emotes and basic moves

`RPC_emotion` (`$RPC_emotion$24928` :45848, MoveNext :45962-46684):

- The voice comes at 0, **before** the clip (:46033-46113). Its gates: the voice option (:46033), more than 2 s since the
  last action (`Time.time > actionTime + 2` :46039), and the own hero, game code 31 or a mission teammate (:46045-46071).
- Only emo_hi and emo_wave have one: `Voices/hi` (:46080-46113). Unlike the Chameleon / Mole, there is no
  `Voices/<name>` for the others and no chat pick.
- Then `actionState "emotion"`, `addTimeOut(eType, 0.3)` (:46126-46141) and the clip with a 0.2 s fade. No effect and no
  `Sounds/` load anywhere in RPC_emotion.

| emote | clip | voice | source |
|---|---|---|---|
| emo_hi, emo_wave | wave | hi | :46171, :46179 -> :46621 |
| emo_ty, emo_bow | bow | none | :46189, :46196 -> :46607 |
| emo_laugh | laugh | none | :46203-46209 |
| emo_sit | sit | none | :46223-46229 |
| emo_sleep | sleep | none | :46235-46241 |
| emo_cheer | cheer | none | :46247-46253 |
| emo_beg | beg | none | :46259-46265 |
| emo_cry | cry | none | :46271-46277 |
| emo_talk, emo_chat | talk | none | :46285, :46292 -> :46585 |
| emo_pose | pose5 / 15 / 25 / 35 / 45 / 58 / 65 / 46 / 66 by the worn set, else pose | none | :46299-46545 |
| emo_battle | battle | none | :46561 |
| emo_dance | dance | none | :46578 |

- The TTO-only emote clips (clap, cooking, fishingMonkey, mining, planting, pose37, wai) stay silent. TTO's
  `Monkey::EmotionVoiceClip` gives no voice for emo_clap / emo_wai (Bat decision 36, Chameleon decision 20).
- **KO:**
  - `RPC_ko` (`$RPC_ko$25096` :51626): `actionState "ko"`, `PlayAnimation("ko", 0)` (:51825-51843), voice **`ko`**
    (pvoice, mission, own team :51846-51858; load :51870, PlayOneShot :51882), Fire Avatar / Earth Form removed
    (:51895-51916), getUp after 3 s (`Yield(2, 3)` :51938 -> :51742, cut in), standby 1 s later (`Yield(3, 1)` :51935 ->
    :51766). No effect.
  - `RPC_dead` (`$RPC_dead$25103` :51975): Rewind and `PlayAnimation("ko", 0)` (:52169-52172), voice **`dead`** (same
    gates :52178-52193; load :52202, PlayOneShot :52214), then **always** `Instantiate(deadEffect, hero position, hero
    rotation)` (:52227-52246). That block is outside the voice block, and its predicate `72529 - 362265 != -289735` holds.
  - `deadEffect` (probe): EffectControl life 3, no follow; the ImageEmitter `monkey_dead` 0.8 m up (Delay 0.6, Life 1.2,
    rising 1 m/s) and two `Dust1` LineEmitters (Delay 0.5). Ready.
  - Sheep decision 11: one of the two at random, even chance; the roll carries each one's voice (as mole.json).
- **getUp**: both RPC_ko's (:51742) and RPC_revive's (`animation.Play("getUp")` :52506) are silent. BB's RPC_revive loads
  no voice, and TTO's `Voices/revive` exists in neither game (item 8). **falling, root, battle**: nothing (the battle
  clip's other callers, :49966 and :50301, are RPC_useMount and RPC_useCoin, which add no sound). **run**: the footsteps
  (item 7).

```json
  "wave": {
    "why": "Monkey.cs RPC_emotion (:45848-46684): the voice at 0, before the clip, only for emo_hi and emo_wave: Voices/hi (gates pvoice, more than 2 s since the last action, own hero / game code 31 / mission teammate :46033-46071; emo_hi / emo_wave test :46080-46092, load :46101, PlayOneShot :46113); both play the wave clip with a 0.2 s fade (:46171-46185 -> :46621); every other emote is silent (no other Voices/ load in RPC_emotion; the rip's monkey voices/ has no wave, ty, bow, laugh, cheer, cry, sleep, chat, pose, battle; TTO1102 Monkey::EmotionVoiceClip returns hi for emo_hi / emo_wave only, pseudo/Monkey.c:41199-41221)",
    "cues": [
      [0, "voice", "hi"]
    ]
  },
  "run": {
    "why": "the run clip's AnimationEvents playLeftFootEvent at 0.1 s and playRightFootEvent at 0.4 s (rip AnimationClip/run.anim m_Events, the Monkey prefab's own run, checks/fx_monkey_research/attacks_emotes/probe_fields.txt; the only events on any Monkey clip, rip_events.txt) -> Monkey.cs :101-155: the hero's audio.PlayOneShot(footStep_left) / (footStep_right), own hero or anyone in a mission (:108-118, :137-147); both fields (:19249, :19252) are the AudioClip step_normal1 (probe_fields.txt offsets 24 / 32; Resources/sound/fx/step_normal1.wav, hero_sound_wav's fallback); every cycle (everyCycle, as the Bat's wing flap and the Chameleon's steps)",
    "everyCycle": true,
    "cues": [
      [0.1, "sound", "step_normal1"],
      [0.4, "sound", "step_normal1"]
    ]
  },
  "ko": {
    "why": "Monkey.cs RPC_ko (:51626-51943): the ko clip cut in (PlayAnimation(ko, 0) :51840) and the voice ko (one file, no random; mission / arena, own team: :51846-51858, load :51870, PlayOneShot :51882), getUp after 3 s (Yield(2, 3) :51938, :51742), standby 1 s later (:51935, :51766), no effect; RPC_dead (:51975-52280): Rewind and the same clip (:52169-52172), the voice dead (same gates :52178-52193, load :52202, PlayOneShot :52214), then always Effects/deadEffect at the hero's position and rotation (:52227-52246, outside the voice block; EffectControl life 3, monkey_dead 0.8 m up and two dust lines after 0.5-0.6 s): one of the two at random, even chance (Sheep decision 11, as mole.json: roll dead, its voice with it; '!dead' = RPC_ko's); TTO1102 the same names (Monkey::KoVoiceName ko, DeadVoiceName dead, pseudo/Monkey.c:41239-41262)",
    "cues": [
      [0, "voice", "ko", {"p": 0.5, "roll": "!dead"}],
      [0, "voice", "dead", {"p": 0.5, "roll": "dead"}],
      [0, "fx", "deadEffect", {"p": 0.5, "roll": "dead"}]
    ]
  }
```

No entry for cAttack1, bow, laugh, sit, sleep, cheer, beg, cry, talk, the pose clips, battle, dance, getUp, root, falling,
or the TTO emote clips (all silent, nothing drawn).

---

## Parts needed (build stage)

1. **P1 `mikeBlink` carries Mike** (a page part on the `mikeBlink` effect, for example in a new `fxparts/monkey.js`; the
   game does it in Monkey.cs, not in a script on the prefab):
   - on spawn, `api.propModel(fx.at.slot || "R")` (index.html `propModel`, built for the Chameleon) is parented under the
     effect's node `mount_Summon` at localPosition 0, localRotation identity and the prop's own scale (:35933-35943; the
     reset sets localScale 1, :14043). The copy's `weapon_fx` particles come with it, as the game moves the whole piece;
   - it is disposed with the effect (the cue's kill 0.7 = `resetMikeBlink`'s Destroy, :14055);
   - nothing worn in R: nothing (question 7);
   - the effect's own Animation (`root`, 1.1 s, wrap 0) already drives `mount_Summon` (probe; the inventory has
     `mikeBlink` ready). The copy only needs to ride that node.
   The hand's Mike is hidden by the cue `[0.3, "hideProp", "R", {"kill": 0.7, "all": true}]` (an existing kind and option;
   `inProp` stops at the hero's root, so the copy under the effect stays drawn).
2. **Inventory:** `hpTransfer` is a hero-prefab field (`Monkey_hpTransfer`, offset 40), not a `Resources.Load` path, so
   `plans/fx_inventory.md` "### monkey" misses it. Add it to `pipeline/wardrobe_fx_inventory.py` as the Penguin's
   `nAttack_fire` (it is ready: BoltEmitter, Light, AudioSource). The inventory also cannot see the AudioClip fields
   (`step_normal1` x 2) or the hero-played `Sounds/` (nAttack1, nAttack2, nAttack_hit).
3. **index.html** (the lead's):
   - SEQ `monkey`: `"Normal Attack: nAttack1@0.5 nAttack2~"`, `"Mike Blink: nAttack1@0.5 nAttack2~"`,
     `"HP Transfer: cAttack1 cAttack2*@3.2"` (in place of `"Charge Attack: cAttack1 cAttack2*"`),
     `"Mike Circle: cAttack1 cAttack2*@3.2"`;
   - `SEQ_SKILL.monkey`: `{ "@MikeBlink": "mikeBlink", "@MikeCircle": "mikeCircle" }`.
4. Already built and used here: the `"sound"` cue with its `Resources/sound/fx/` fallback (`hero_sound_wav`),
   `everyCycle`, `hideProp` with `all`, the BoltEmitter `to` and Point light (the Bat's drainLife), `p` / `roll` with
   `"!name"`, `api.propModel`. Everything else cued is ready by the probe and the inventory: nAttack_hit, mikeCircle,
   fireRune_hit (AlphaTimer), deadEffect.

## Left out

- The Combo's hits (0-7 m and 3.5-7.5 m boxes, :19957, :20571), so no nAttack_hit, Fire Rune or gear procs on the Combo
  tile: they miss the 10 m body.
- onNormalAttackHit's gear procs on Mike Blink's hits (statuses on the foe, heal1 / revert on the hero by the worn
  piece, :52561-53105): Chameleon decision 53.
- HP Transfer's heal and cost numbers, Damage Cast's 2 m hits and Mike Circle's 3 m hits (no enemy there), and the
  "Target is too far" text.
- RPC_cAttack0 (the release, nothing drawn) and RPC_activateIcon1 (the mission channel, Penguin decision 19).
- The skills that take over the normal attack or the charge (Fire Keep, Fire Avatar, Earth Form, Lavu's Upheaval,
  Blazing Form, Sentinel Guard): their own reports.
- Game code 967's `useItem("f_wtb1")` normal attack (:9617-9633): an event mode.

## Open questions (each with the recommended answer)

1. **Mike Blink's target distance.** The game blinks only beyond 12 m (:10105). **Recommended: its own tile at the 10 m
   target point** (the standing rule, like every other target effect; Clear Arrow showed its precondition the same way).
   The alternative is 13 m: change d 10 / 9.7 / 10.3 to 13 / 12.7 / 13.3.
2. **The HP Transfer hold.** **Recommended: 3.2 s** (three 1 s ticks, the SEQ rule's "at least 3 s"). The ticks draw
   nothing, so a longer hold only lengthens the beam.
3. **HP Transfer's ally.** **Recommended: an ally at the 10 m target point**, the beam to (0, 0.6, 9.4) and the Mikes at
   (0, 0.45, 10). The skill refuses a self-target, so Sheep decision 1's self-cast does not apply (Sheep decision 4's
   revived ally is the analogue).
4. **The tile name.** **Recommended: "HP Transfer"** in place of "Charge Attack" (as the Bat's "Drain Life"; the Bible's
   name, `monkey-skill-reference.md` §1). Its icon stays the cAttack one either way.
5. **A Mike Circle tile.** **Recommended: yes**, `"Mike Circle: cAttack1 cAttack2*@3.2"`. It reuses the cAttack2 entry,
   so it looks the same as HP Transfer's: Mike Circle's only look lives there (one tile per skill; Chameleon decision
   12's shape).
6. **Fire Rune on the two blink strikes.** **Recommended: p 0.12 each, independent.** The game's 1 s lockout makes two
   procs impossible; the page shows them on 1.4 % of plays. An exact model would need a cue option "only if roll x
   failed, with its own p".
7. **Mike Blink with nothing in R.** **Recommended: nothing drawn**, since the hand shows no Mike either.
   Chameleon decision 50 drew the starter arrow; the Monkey's starter would be `noviceMike` through `PROP_STARTER`, if the
   lead prefers that.
8. **Mission-only voices and the beam.** **Recommended: shown** (Chameleon decision 42, Cat decision 38).
9. **TTO-only emote clips (clap, wai released; cooking, fishingMonkey, mining, planting, pose37).** **Recommended:
   silent**, no entries (Bat decision 36). TTO's own code gives the Monkey no voice for them.

## Offer for the Bible

New for `12t_reference/monkey-skill-reference.md` (its §1 Combo / HP Transfer rows and §4.12 Mike Blink, §4.13 Mike
Circle), offered, not written:
- Combo timing:
  - stage 2 must be pressed within 0.5 s of stage 1, and its clip starts at 0.5 s (`actionTime + 0.5`, :20770);
  - the hits come at 0.4 s (a box 0-7 m ahead, 2 m wide) and 0.8 s (3.5-7.5 m, 3 m wide);
  - standby comes 1.2 s after stage 1, or 1.6 s after it with stage 2;
  - the swing sounds come at 0.2 s and 0.6 s; the voices play only in missions.
- Mike Blink:
  - Mike leaves the hand and appears on the target at 0.3 s;
  - strike 1 at 0.5 s (a 4 m box from 3 m before the target);
  - strike 2 at 0.8 s (1 m round the target), only if pressed within 0.5 s;
  - Mike returns at 1.0 s with stage 2, at 0.7 s without;
  - the `mikeBlink` voice comes on strike 1 only.
- HP Transfer:
  - cAttack1 for 0.7 s, then the beam;
  - the first heal tick comes 1.7 s after the press and then every 1 s;
  - with Mike Circle the two Mikes circle the ally and hit enemies within 3 m of it every 0.5 s;
  - the beam and the Mikes show only in missions / arenas.
- KO: one `ko` and one `dead` voice (no random variant), only in missions. BB's revive plays no voice.
- Footsteps: `step_normal1` on both feet.

## Verification (2026-11-13)

Checker, office PC, read only (probes in `checks/fx_monkey_research/verify/`: `probe_ae_eo.json` = `wardrobe_fx.py monkey
--probe` of every effect named in this report and effect_only.md, summed by `summ.py`; `cues_check.py` parses every json
block of both reports as one object and checks the keys against `wardrobe/data/monkey/clips.json` / the proposed SEQ ids
and the options against `wardrobe_fx_check.py` OPTS; `corrected_ae.json` = the corrected blocks below, `json.load`
clean). The Verification wins over the body.

**Checked and holding** (re-derived from `Monkey.cs`, the rip and the page):
- Every wait in the five tables: `Yield` :20233 0.2, :20241 0.2, :20229 0.8; :20770 `actionTime - Time.time + 0.5`,
  :20764 0.1, :20780 0.2, :20773 0.8; :21594 0.7; :36304 0.3, :36299 0.2, :36310 0.2, :36291 0.5; :36798 + 0.5, :36803
  0.1, :36789 0.2, :36807 0.2, :36809 0.6. So the Combo's and Mike Blink's stage 2 start at 0.5 s and cAttack2 at 0.7 s.
- The fades: `PlayAnimation(..., 0.2f)` :20157, :20412, :36205, :36486; the cuts :21563, :20969.
- The >12 m gate (`sqrMagnitude > 144` :10105, the raw `tDir` :10111); mikeBlink's spawn and the `mWep1` reparent
  (:35907-35943) and the reset (:14015-14058).
- hpTransfer at `TransformDirection(0, 0.82, 0.88)`, identity (:21027), its bolt to `bounds.center - forward x 2
  extents.x` (:20996, :21184) = (0, 0.6, 9.4); mikeCircle at `bounds.center - 0.15 up`, `rotation x Euler(270, 90, 0)`
  (:21067).
- The strike points d 9.7 / d 10.3, y 0.9 (:36051, :36657; the hero's rotation :10759).
- The only `Voices/` loads of RPC_emotion / RPC_ko / RPC_dead: `hi` :46101, `ko` :51870, `dead` :52202; `deadEffect`
  :52233-52243; RPC_revive only `animation.Play("getUp")` :52506.
- The run's events at 0.1 / 0.4 s (rip `AnimationClip/run.anim`; the clip is 0.6 s, clips.json); TTO1102
  `Monkey::EmotionVoiceClip` / `KoVoiceName` / `DeadVoiceName` (pseudo/Monkey.c:41199-41262).
- Every name exists: voices nAttack1, nAttack2, mikeBlink, hi, ko, dead (rip `characters/heroes/monkey/voices/`);
  sounds nAttack1, nAttack2, nAttack_hit (`.../sounds/`), step_normal1 (`Resources/sound/fx/step_normal1.wav`); effects
  hpTransfer, mikeCircle, nAttack_hit, deadEffect, mikeBlink, fireRune_hit (the probe builds all six).
- All 8 entries parse; every key is a Monkey clip or a proposed `@Seq:clip`; every option is in OPTS. Nothing here is
  TTO-only (released: buitenBastion, clap, golemCall, jaAscension, solarCall, wai; clap / wai stay silent, Bat decision
  36). 23 cues, also after finding 1 (the same cues, moved).

1. **Mike Blink's first strike would never fire on the page (the most important).** The three cues at 0.5 s of
   `@MikeBlink:nAttack1` sit at the very end of a 0.5 s step (`nAttack1@0.5`). The page ends a step in `seqTick`,
   before `fxTick` runs (index.html:5493-5494): `S.t >= S.dur` (:1532), then `fxDue(S.dur, false)` (:1535), which skips
   any cue with `c.at >= t` (:5403), then `startStep` swaps `FX.cues` for the next step's (:1524, fxStart). So the
   d 9.7 `nAttack_hit`, its sound and the Fire Rune roll are lost on every play. **Corrected:** they move to
   `@MikeBlink:nAttack2` at 0 (stage 2's clip starts exactly at stage 1 + 0.5 s, :36798: the same moment). Both entries
   in full:

```json
  "@MikeBlink:nAttack1": {
    "why": "Monkey.cs RPC_mikeBlink1 (:35713-36314), Mike Blink #401 (passive): doNormalAttack runs it in place of Combo stage 1 on a locked enemy more than 12 m away in a mission (sqrMagnitude > 144, :10076-10142; shown at the 10 m target point, attacks_emotes Q1); at 0 the clip nAttack1 with a 0.2 s fade (:36205), an old mikeBlink destroyed (:36217-36223), the voice mikeBlink (mission / arena, own team: :36229-36245, load :36253, PlayOneShot :36288; then Yield(2, 0.3) :36304); 0.3 s, still attacking (:35831): the hero's Sounds/nAttack1 (:35841-35874), Effects/mikeBlink at the target's feet (mPos + tDir :35907, tDir = target - hero :10111) with LookRotation(flat tDir) x Euler(270, 90, 0) (:35907), and the worn Mike (mWep1, the page's R; nothing worn: the starter noviceMike, Chameleon decision 50) moved onto its mount_Summon node, localPosition 0, localRotation identity (:35920-35943): fx:mikeBlink's copy of R there, the hand's R hidden with its particles; the effect's Animation (root, 1.1 s) flies it; it lives to stage 2's resetMikeBlink at 0.5 s (:36707, :14015-14058): kill 0.7; then Yield(3, 0.2) :36299. The strike at 0.5 s (FindRecTarget :35995, nAttack_hit d 9.7 y 0.9, Sounds/nAttack_hit, FireRune 12 %) is cued in @MikeBlink:nAttack2 at 0: this step ends at 0.5 (SEQ nAttack1@0.5) and a cue at a step's very end never fires (index.html seqTick :1535 fxDue(S.dur, false), fxDue :5403 skips c.at >= t; attacks_emotes Verification 1)",
    "cues": [
      [0, "voice", "mikeBlink"],
      [0.3, "sound", "nAttack1"],
      [0.3, "fx", "mikeBlink", {"d": 10, "rot": [270, 90, 0], "kill": 0.7, "slot": "R"}],
      [0.3, "hideProp", "R", {"kill": 0.7, "all": true}]
    ]
  },
  "@MikeBlink:nAttack2": {
    "why": "at 0 (= stage 1's 0.5 s, RPC_mikeBlink2's clip at actionTime + 0.5, :36798): stage 1's strike, RPC_mikeBlink1 (:35977-36086): FindRecTarget(target - 3 forward, forward, 1, 1, 4, 2) (:35995: 7-11 m, the 10 m body is hit): RPC_nAttack_hit (:36061) = nAttack_hit at ClosestPointOnBounds(hero + TransformDirection(0, 0.9, 5)) = d 9.7, y 0.9, the hero's rotation (:36051, :10759), the hero's Sounds/nAttack_hit (0.1 s gate, :10773-10798), FireRune (:36086): Fire Rune 3 on, Random.Range(0, 100) < lckAdjust(12) = 12 % at LCK 1 (:12297), fireRune_hit at the hero, identity (:12357); onNormalAttackHit's gear procs left out (cued here, not at 0.5 of nAttack1: a cue at a step's end never fires, Verification 1). Then Monkey.cs RPC_mikeBlink2 (:36370-36811), Mike Blink's second strike (doNormalAttack :9964-10014: pressed while attacking with myCommand mikeBlink1, #101, before stage 1 + 0.5 s): nAttack2 with a 0.2 s fade (:36486), no voice; 0.1 s (Yield(3, 0.1) :36803) the hero's Sounds/nAttack2 (:36510-36543); 0.3 s (Yield(4, 0.2) :36789) the strike, FindAreaTarget(the mikeBlink effect's position, 1, 3) (:36601): nAttack_hit at ClosestPointOnBounds(mikeBlink + TransformDirection(0, 0.9, 5)) = d 10.3, y 0.9 (:36657, :36667, :10759), Sounds/nAttack_hit; FireRune (:36692) 12 % again (the game's 1 s lockout after a proc 0.3 s earlier not modelled: both on 1.4 % of plays, Q6); 0.5 s (Yield(5, 0.2) :36807) resetMikeBlink (:36707; :14015-14058: Mike back on the hero's mount_Summon, the effect destroyed: stage 1's kill); standby 1.1 s (Yield(6, 0.6) :36809, :36726)",
    "cues": [
      [0, "fx", "nAttack_hit", {"d": 9.7, "y": 0.9}],
      [0, "sound", "nAttack_hit"],
      [0, "fx", "fireRune_hit", {"p": 0.12}],
      [0.1, "sound", "nAttack2"],
      [0.3, "fx", "nAttack_hit", {"d": 10.3, "y": 0.9}],
      [0.3, "sound", "nAttack_hit"],
      [0.3, "fx", "fireRune_hit", {"p": 0.12}]
    ]
  },
```
   No other cue in this report sits at or past its step's end (the Combo's at 0 / 0.2 / 0.1, cAttack2's at 0 of a 3.2 s
   step, the run's inside its 0.6 s cycle).

2. **Q7 / P1, Mike Blink with nothing in R: the starter flies, not nothing.** Chameleon decision 50
   (plans/fx_chameleon/decisions.md:168-170): with nothing worn the flying copy is the class's starter piece and the hand
   stays empty, because the game always holds one. By analogy the blink carries `noviceMike` (w_mnk1; it exists in
   `wardrobe/data/monkey/props_weapons.json` and `item_map.json`). **Corrected P1:** `api.propModel("R", true)` with
   `PROP_STARTER.monkey = { R: "noviceMike" }` (index.html:5163 holds only the Chameleon's today). The hand's
   `hideProp "R"` then does nothing (no prop worn, index.html:5439), as the Chameleon's. This part is parts.md part 6
   (`fx:mikeBlink`, plans/fx_monkey/parts.md:311-325, which already says so): **build one `fx:mikeBlink`, parts.md's**.
   The cue's `slot` option stays (in OPTS; that part does not read it, harmless).

3. **The Mike Blink and Mike Circle tiles need their Bible icons in `wardrobe_skill_icons.py` (missed).** With only
   `SEQ_SKILL`, `moveSkillIcons` finds no `HDI.monkey.mikeBlink` / `mikeCircle` (data/icons/hd/index.json has neither)
   and falls back to the small `icons/skills/monkey/mikeblink5.webp` (index.html:3411-3415), unlike every earlier class's
   own-tile skills. The Bible has `monkey_mikeBlink5` and `monkey_mikeCircle5` (assets.js; cards index.html:18722,
   :18734). **Add** to `OWN_TILE` (pipeline/wardrobe_skill_icons.py:67-73), merged with skills_a.md's monkey entries (its
   line 125: lavu, volcanicEruption, summonGaos, fireKeep), as the Chameleon's Critical Plus / Clear Arrow:
```python
            # the Monkey's Mike Blink on the Normal Attack's clips, Mike Circle on HP Transfer's (2026-11-13,
            # plans/fx_monkey/attacks_emotes.md Verification 3)
            "monkey": {"mikeBlink": ["nAttack1", "nAttack2"], "mikeCircle": ["cAttack1", "cAttack2"]}}
```
   This is safe for the Normal Attack and HP Transfer tiles: SEQ_SKILL's values are in `pooled`, so those two icons stay
   off them (index.html:3420). HP Transfer keeps `HDI.monkey.cAttack` = `monkey_cAttack4` (the Bible card's icon) by its
   clips.

4. **Merge with effect_only.md.** Its SEQ block repeats the old `"Normal Attack: nAttack1 nAttack2~"` and
   `"Charge Attack: cAttack1 cAttack2*"`. This report's four lines win; effect_only Verification 4 has the merged monkey
   SEQ and SEQ_SKILL lines.

5. **Small, no change:** the hit sound's 0.1 s gate (:10775-10786) lets both strikes sound (0.3 s apart), as cued.

**Calls made here (the user is away):** strike 1 cued at stage 2's 0 (finding 1, the page's step rule); the starter Mike
when R is empty (finding 2, Chameleon decision 50); own-tile icons (finding 3, the Chameleon's OWN_TILE, decision 14).
Q1-Q6, Q8 and Q9 stand as the report recommends.
