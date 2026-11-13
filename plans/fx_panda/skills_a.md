Summary: all 15 clips are traced, with file:line, through the opaque predicates and the timed waits (each predicate
evaluated by `cond.py`). Eleven skills play them: Ashura (ashura, then ashuraFist, its charge-press replacement), Tiger
Toss / Climbing Cliff / Crumbling Mountain (all open with `grab`), Combo Link, Drunken Fist, Fuujin Ken (fujinKen1-3),
Heaven Palm, Lotus Palm, Pummel and Qi Strike (qiStrike1, Delay Qi's hold, qiStrike2). No pool: no clip of mine is
played by two skills except `grab`, which opens three sequences and has no cues of its own. No TTO skill plays any of
these clips (TTO1102's copies load the same names). Every effect is ready by the inventory and the probe; three small
missing parts are needed (P1 the Ashura tint, P2 the `atBone` cue option, P3 range-valued offsets), plus the inventory
and icon-script lines. 14 cue entries, 75 cues. 10 open questions, each with a recommended answer.

# Panda effects + sounds research: skills_a (fifteen skill clips)

Researcher `skills_a`, 2026-11-13 (office PC).
- **Scope:** the clips ashura, ashuraFist, climbingCliff, comboLink, crumblingMountain, drunkenFist, fujinKen1, fujinKen2,
  fujinKen3, grab, heavenPalm, lotusPalm, pummel, qiStrike1 and qiStrike2, and every skill that plays them.
- **Method:** research only (recipe steps 1-3).
- **Line numbers:** `C:\Users\Jump\Desktop\12tails\DecompiledSource\Panda.cs` (home: `D:\12tails\...`) unless another
  file is named. "TTO" means `DecompiledSource_TTO_2026-11-02\pseudo\Panda.c`.
- **Units:** times are seconds from the start of the clip the cue is keyed by. d = metres ahead, x = metres right,
  y = metres up.

## Read-only probes

Everything is in `C:\work\12tails-wardrobe\checks\fx_panda_research\skills_a\` (git-ignored). Nothing there writes
outside that folder.

- **Coroutine reads:**
  - `cond.py <file> <from> <to>` prints the lines with every opaque predicate `if (a - b ==/!= c)` evaluated to
    TRUE / FALSE.
  - `f.sh <from> <to> [file]` does the same with the braces and the dead `if (FALSE) continue/goto` pairs dropped
    (default file Panda.cs).
  - Outputs: `flow_RPC_*.txt` (clip_flow.js with the effect / voice / status lines) and `clip_calls.txt`
    (clip_calls.js for the Panda).
- **`probe\probe.json`** with `probe\summary.txt` (from `probe\summ.py`): `wardrobe_fx.py panda --probe` of the 32
  effects named below. All decode; every component type they use is in the page (EffectControl, Ring / Image / Line /
  Emblem emitters, legacy particles, AudioSource, AudioControl, EmitterControl, Animation, SkinnedMeshRenderer,
  StaticMesh, AlphaTimer).
- **`entries.py` -> `cues_whole.json`:** the cue entries (times sorted, kinds known), JSON-checked.

## Max rank and passives on

- Qi Strike 3 with Delay Qi #214 and Qi Burst #412.
- Pummel 2 with Ogre Impact #422.
- Drunken Fist 2 with Drunken Plus 2 (#304) and Drunken Spin #403.
- Ashura 2; Lotus Palm 2; Heaven Palm 2 (with Spirit Fist #433: range only).
- Tiger Toss with Climbing Cliff, Crumbling Mountain and Crushing Monolith #432 (passives).
- Fuujin Ken, Combo Link: one rank each.

Ranks change the look in two places only: Heaven Palm's blast is 1.5x at rank 2 (:9542-9548), and the passives above
swap or add effects (qiBurst for qiStrike, pummel_ogre and its arms, drunkenSpin for drunkenFist, the drunken status,
crushingMonolith and its hits).

---

## Read this first

### 1. Who plays these clips

| clip | BB | TTO |
|---|---|---|
| ashura | RPC_ashura :30668 | same (TTO `<RPC_ashura>d__201`) |
| ashuraFist | RPC_ashuraFist :31281, started by doBeginCharge while the `ashura` status holds (:8215-8231) | same (`d__202`) |
| grab | RPC_grab :26359 (Tiger Toss's cast, dispatch :7174); it starts RPC_tigerToss, RPC_climbingCliff or RPC_crumblingMountain at 0.2 s (:26142, :26245, :26224) | same (`d__183`) |
| climbingCliff | RPC_climbingCliff :27607 | same (`d__188`) |
| crumblingMountain | RPC_crumblingMountain :28392 | same (`d__191`) |
| comboLink | RPC_comboLink :40672 | same (`d__233`) |
| drunkenFist | RPC_drunkenFist :32467 | same (`d__203`) |
| fujinKen1 / 2 / 3 | RPC_fuujinKen :41139 / :40994 / :41300 | same (`d__234`) |
| heavenPalm | RPC_heavenPalm :40176 | same (`d__221`) |
| lotusPalm | RPC_lotusPalm :39337 | same (`d__219`) |
| pummel | RPC_pummel :24910 | same (`d__179`) |
| qiStrike1 | RPC_qiStrike1 :23132 | same (`d__175`) |
| qiStrike2 | RPC_qiStrike2 :23665 (with Delay Qi: the attack press that releases the hold, doNormalAttack :7896-7930) | same (`d__176`) |

- TTO1102 names each clip only in its own coroutine (an awk pass over every `String:'<clip>'` literal of Panda.c by
  enclosing function), so no TTO skill (nineDragons, tempestDance, yinYangFist) plays them, and no released TTO item
  needs a cue here.
- The effect names in TTO's copies are the same (ashuraRing, climbingCliff_ring, crushingMonolith, qiBurst, delayQi_ring
  ... all present in Panda.c).

### 2. The tiles

One tile per skill, each with its Bible icon:

- **Ashura:** the cast, then one Ashura Fist under the red form (open question 1).
- **Tiger Toss / Climbing Cliff / Crumbling Mountain:** three sequences that each open with `grab`. Climbing Cliff and
  Crumbling Mountain each get their own tile, though with the passives on Crumbling Mountain takes over whenever SP ≥ 40
  (:26209-26224; open question 6). The tigerToss clip's cues are skills_b's; this report gives the SEQ line only.
- **Qi Strike:** the charge, then Delay Qi's hold on the idle stance, then the release (open question 2).
- **Combo Link, Drunken Fist, Fuujin Ken, Heaven Palm, Lotus Palm, Pummel:** single clips, or the existing Fuujin Ken
  sequence.

### 3. Missing part P1: the Ashura tint

- The `ashura` status's apply (CharacterControl.cs:35484-35518) does `setColor(1, 0, 0)`: _Color on every renderer under
  the character (CharacterControl.cs:21702-21800).
- New HERO_SKINS body look: `"ashura": () => ({ tint: [1 / 0.86, 0, 0] })`. The tint is read against the page hero's
  0.86 base colour, as the Bison's `enrage` is.
- A tint-only body look is already supported (index.html:4920, `look.grow != null || look.tint`).
- One line in index.html. The check already knows the `skin` kind.

### 4. Missing part P2: the cue option `atBone`

- Climbing Cliff's and Crumbling Mountain's hit flashes are Instantiated, not parented, at the Panda's `Root` bone's
  world position + 0.3 × the hero's forward, LookRotation(the hero's forward) (:27538 -> :8757; :28203 -> :9791).
- The `Root` bone moves through the climb clips, so a fixed `y` is wrong, and `bone` would make the flash ride the bone.
- New option `atBone: "<bone>"`: when the effect spawns, its root goes to that bone's world position at that moment,
  plus the cue's x / y / d along the hero's facing. Its rotation is the hero's facing (+ the cue's rot). After that it
  stays put.
- In index.html, the Fx constructor reads `at.atBone` once, the way the `bone` branch (:4348-4360) reads `C.byName`,
  without keeping it.
- Add `atBone` to wardrobe_fx_check.py's OPTS.
- Fallback if P2 is not built: `{"bone": "Root"}` (the flash rides the hips for its 1 s life).

### 5. Missing part P3: range-valued offsets

- Each Pummel jab with Ogre Impact throws an arm at `position + TransformDirection(Random.Range(0.2, 0.6),
  Random.Range(0.5, 1.5), Random.Range(0.5, 0.7))`, and the other arm at `Random.Range(-0.6, -0.2)` for x (:24565,
  :24601). Unity's float Range includes both ends.
- `spread` draws whole metres only, so it cannot express this.
- New: `x`, `y` and `d` may each be `[lo, hi]`, a float drawn when the clip starts.
- In cueOf (index.html:4794-4797): `const R = v => Array.isArray(v) ? v[0] + Math.random() * (v[1] - v[0]) : v || 0;`
  used for d, x and y. That is one line, and `spread` still adds after it.
- The check's OPTS takes the names already. Any code that reads `c[3].d` as a number should go through cueOf.

### 6. Inventory: four status effects that CharacterControl loads

`ashura`, `drunken`, `drunk` and `delayQi` are loaded by the status apply (CharacterControl.cs:35500, :35396, :35535,
:35342), not by Panda.cs. So `plans/fx_inventory.md` "### panda" does not list them.

The probe reads all four whole:
- ashura: LineEmitter, no EffectControl.
- drunken and drunk: legacy particles, no EffectControl.
- delayQi: EffectControl life 12, LineEmitter.

They belong in `pipeline/wardrobe_fx_inventory.py` as ready status effects (the Mole verification's item 3 precedent).
`drunk` (on a foe) is not cued (Left out).

### 7. Icons: Fuujin Ken has no tile icon today

- The clips fujinKen1-3 strip to `fujinKen`, but the Bible key is `panda_fuujinKen` (two u's), so the index has no
  `fuujinKen` entry (data/icons/hd/index.json).
- Add `CLIP_SKILLS["panda"] = {"fujinKen1": ["fuujinKen"], "fujinKen2": ["fuujinKen"], "fujinKen3": ["fuujinKen"]}` to
  wardrobe_skill_icons.py.
- The script picks rank 5. panda_fuujinKen1 and panda_fuujinKen5 are the same image (same base64, md5 23bf179f), and
  the Bible card uses panda_fuujinKen1 (bible/index.html:19305).
- ashuraFist and grab need no icon: each plays only inside a sequence whose other clip carries one (moveSkillIcons,
  index.html:3415-3427).

### 8. Left out: hits on the foe, statuses on the foe, camera effects

- **Melee boxes that never reach the 10 m target** (Cat decision 19), so no hit is drawn:
  - Pummel's `pummel_hit`: the Ogre box is 4 m wide and 3 m long (:24765, :24818-24828).
  - Qi Strike's `qiStrike_hit`: the box is 1 + 5 m long with Qi Burst (:23503, :23532-23542).
  - Drunken Fist's four 1 m boxes (:31718, :31940, :32115, :32263), and so also the `drunk` status they would put on a
    foe (CharacterControl.cs:35531-35544; the foe-status rule, Cat decision 44).
  - Ashura Fist's 3 m circle (:31197).
  - Fuujin Ken's `fuujinKen_hit`, drawn only on enemies within 2 m (`sqrMagnitude < 4`, :41414-41420). The 12 m pull
    draws nothing.
- **Camera effects:** the motion blurs (Ashura :30532, Combo Link :40725, Fuujin Ken :40967, Qi Strike :23871, Heaven
  Palm :40006), the camera shakes (Ashura Fist :31052, Heaven Palm :39996) and the toasts ("ClimbingCliff!", "Crumbling
  Mountain!", "ComboLink: +n combo").
- **Statuses with no look:** noForce (CharacterControl.cs:2266), atkUp (:33176-33186, deltaAtk only), comboPlus.
- **Without Ogre Impact only:** the `punch1Fx` jab sound (:24778).

### 9. The hero does not travel

The game moves the hero in these skills: Grab's 16 m/s lunge (:26009), Pummel's lunge and step back (:24448, :24637),
Drunken Fist's walk (:32476, :32075, :32102), Ashura Fist's 3.6 m lunge (:30987), Qi Strike's release dash (:23680),
Heaven Palm's backstep (:40185, :39801) and the climbs' step back (:27566, :28351).

In the wardrobe, every effect is relative to the standing hero (Bison decision 17, Mole decision 28).

### What is ready

- **Effects** (inventory + probe): ashuraRing, ashuraFist, climbingCliff_ring, climbingCliff_hit, crushingMonolith,
  crushingMonolith_hit, comboLink_ring, drunkenSpin, fuujinKen_ring1-3, heavenPalm_ring, heavenPalm, lotusPalm_ring,
  lotusPalm, pummel_dust, pummel_ogre, pummel_ogreArm1, pummel_ogreArm2, qiStrike_ring, qiBurst, delayQi_ring and
  delayQi_fire. The probe also covers the status effects ashura, drunken and delayQi (item 6).
- **Voices** (all in BB's rip, `heroes/panda/voices`): ashuraGate1-2, ashuraFist1-2, climbingCliff, crumblingMountain,
  drunkenFist1-2, fuujinken1-2 (the code spells them fuujinKen1-2; the rip lookup is case-free on Windows), heavenPalm1-2,
  lotusPalm1-2, pummel1-2, qiStrike1-3, delayQi.
- **Hero-played sound:** `Sounds/qiStrike` (`heroes/panda/sounds/qiStrike`).
- **Effect sounds** (AudioSources, in `panda/sounds`): ashura_ring, ashuraFist, nAttack_hit1, crushingMonolith_hit,
  comboLink_ring, drunkenFist, fuujinken1-2, heavenPalm_hit, lotusParm_ring (sic), lotusPalm_hit, pummel_ogre, qiStrike1
  (qiStrike_ring's loop), delayQi.

---

## Ashura (`ashura`, 1.4 s), then Ashura Fist (`ashuraFist`, 1.5 s)

Sources: RPC_ashura :30346-30843; RPC_ashuraFist :30843-31420; the status CharacterControl.cs:35484-35518.

| time | what happens | source |
|---|---|---|
| 0 | ashura (0.2 s fade, Once) | :30668 |
| 0 | voice ashuraGate1 or 2, at random | :30709-30792 (predicates :30710, :30722, :30742: the normal way) |
| 0.4 | `ashuraRing` at the hero (EC 1, followPosition, own ashura_ring sound) | Yield(2, 0.4) :30785; :30498-30510 |
| 0.8 | the `ashura` status, chaAdjust(24) = 24 s, own client | Yield(3, 0.4) :30806; :30572 |
| 0.8 | status apply: setColor(1, 0, 0), `Effects/ashura` under the Root bone (localPosition 0, Euler 0, scale 1, named ashuraFx) | CharacterControl.cs:35488-35515 |
| 1.2 | standby | Yield(4, 0.4) :30798; :30598 |
| next charge press | doBeginCharge starts RPC_ashuraFist instead of the charge | :8215-8231 |
| fist 0 | ashuraFist **cut in** (PlayAnimation(ashuraFist, 0), Once) | :31281 |
| fist 0 | voice ashuraFist1 or 2, at random | :31322-31411 |
| fist 0.3 | moveSpeed 6 (the 3.6 m lunge) | Yield(2, 0.3) :31398; :30987 |
| fist 0.9 | stop; `ashuraFist` Instantiated at the hero, Quaternion.identity (EC 1 + 1, own ashuraFist sound) | Yield(3, 0.6) :31416; :31009-31032 |
| fist 0.9, 1.1 | two hits, FindAreaTarget(3, 3) | :31197, :31230; Yield(4, 0.2) :31414 |
| fist 1.3 | sp = 0, standby | :31118-31141 |

- The status lasts 24 s at CHA 1 (chaAdjust). The tint and ashuraFx are cut at 10 s, the same as the Bison's Enrage
  look (Bison decision 31).
- `single` on ashuraFx: in the game, a refreshed status does not apply again, so a looping tile keeps one ashuraFx and
  renews it (Cat decision 37's option).
- **Page lines:**
  - `SEQ.panda`: add "Ashura: ashura@1.2 ashuraFist". The fist cuts in, and a later step's default is a cut
    (index.html:1541).
  - The tile's icon is Ashura's, from the ashura clip.

## Tiger Toss / Climbing Cliff / Crumbling Mountain: the grab (`grab`, 1.0 s)

Source: RPC_grab :25862-26393.

| time | what happens | source |
|---|---|---|
| 0 | grab (0.1 s fade, Once); no voice, no effect | :26359 |
| 0.1 | moveSpeed 16 | Yield(2, 0.1) :26391; :26009 |
| 0.2 | stop; the selected target must be in the 1 m box | Yield(3, 0.1) :26389; :26036-26096 |
| 0.2 | height × scale < 3 and weight < 60 -> RPC_tigerToss | :26113-26142 |
| 0.2 | otherwise, with Climbing Cliff learned: SP ≥ 40 and Crumbling Mountain learned -> RPC_crumblingMountain, else RPC_climbingCliff | :26178-26256 |
| 0.5 | standby, only when nothing was started | Yield(4, 0.3) :26387; :26292 |

- The started coroutine sets myCommand at once, so the grab's own step ends at 0.2 s.
- No cue entry: the grab has no effect and no voice.
- **Page lines:** `SEQ.panda`: add
  - "Tiger Toss: grab@0.2 tigerToss" (PlayAnimation(tigerToss, 0) :26959: a cut);
  - "Climbing Cliff: grab@0.2 climbingCliff";
  - "Crumbling Mountain: grab@0.2 crumblingMountain".
- The icons come from the second clip (tigerToss, climbingCliff, crumblingMountain).

## Climbing Cliff (`climbingCliff`, 2.0 s)

Source: RPC_climbingCliff :27194-27752.

| time | what happens | source |
|---|---|---|
| 0 | climbingCliff **cut in** (PlayAnimation(climbingCliff, 0), Once); noForce 2 s | :27607, :27619 |
| 0 | voice climbingCliff (one file) | :27651-27669 |
| 0 | `climbingCliff_ring` at the hero (EC 3, followPosition, followState) | :27693-27711 |
| 0.1 × i, i = 0-17 | one tick each, Yield(2, 0.1) | :27347, :27750 |
| i = 1, 3, ... 15 (0.1-1.5) | a hit on the selected target (ActorNrList[tID], no range test); on a landed hit, `climbingCliff_hit` at Root.position + 0.3 forward, LookRotation(forward) (EC 1, own nAttack_hit1 sound) | :27442-27538; :8734-8760 |
| 1.2-1.6 | step back at -4 m/s | :27566, :27580 |
| 1.8 | standby | i ≥ 18 :27347-27370 |

- The hits strike the grabbed target wherever it stands (:27500), so they land with the target at 10 m too. The tile
  assumes every hit lands (the skill only runs on a grabbed target; Mole decision on Detonate).
- climbingCliff_ring's followState: cut 1.8.

## Crumbling Mountain (`crumblingMountain`, 3.0 s)

Source: RPC_crumblingMountain :27796-28616.

| time | what happens | source |
|---|---|---|
| 0 | crumblingMountain **cut in**; noForce 3 s | :28392, :28404 |
| 0 | voice climbingCliff | :28436-28454 |
| 0 | `climbingCliff_ring` at the hero | :28478-28496 |
| 0 | Crushing Monolith #432: three `crushingMonolith` (Panda doubles: SkinnedMeshRenderer + Animation, EC 3 + 1, followPosition, followState) at target ∓ (radius + 0.1) × forward / ± right, each facing the target | :28513-28575 |
| 0.1 × i, i = 0-27 | ticks | :27949, :28611 |
| i = 2, 5, 9, 10, 11, 15-22 (13 hits) | #432: hit(432) on the target, then `crushingMonolith_hit` at Root.position + 0.3 forward, LookRotation(forward) (EC 1, own sound) | :28044-28203; :9768-9794 |
| 1.6 (i = 16) | voice crumblingMountain; toast | :28267-28332 |
| 2.4-2.7 | step back | :28351, :28365 |
| 2.8 | standby | i ≥ 28 :27949-27972 |

- **The doubles' spots** (the target at the 10 m point, the standard body radius 0.3, + 0.1; Bat decision 3):
  - d 9.6, rot [0, 180, 0] (LookRotation(-forward));
  - x 0.4, d 10, rot [0, -90, 0] (LookRotation(-right));
  - x -0.4, d 10, rot [0, 90, 0].
  - Their followState and the ring's: cut 2.8.
- Without #432 the hits would be `climbingCliff_hit` (:28223-28245). The passives rule takes the #432 branch.

## Combo Link (`comboLink`, 1.0 s)

Source: RPC_comboLink :40418-40751.

| time | what happens | source |
|---|---|---|
| 0 | comboLink (0.2 s fade, Once); no voice | :40672 |
| 0 | `comboLink_ring` at the hero (EC 1 + 1, followPosition, own sound) | :40684-40702 |
| 0.4 | atkUp (5, chaAdjust(6), +n ATK), own client: nothing drawn | Yield(2, 0.4) :40749; :40570; CharacterControl.cs:33176-33186 |
| 0.8 | standby | Yield(3, 0.4) :40747; :40602 |

- With no team combo, the dispatcher refuses the skill ("ComboLink is not available.", :6187-6208). The tile assumes
  a combo, as Detonate assumes its nuke.

## Drunken Fist (`drunkenFist`, 1.2 s)

Source: RPC_drunkenFist :31474-32638; the status CharacterControl.cs:35389-35405.

| time | what happens | source |
|---|---|---|
| 0 | drunkenFist (0.2 s fade, Once); moveSpeed 3 | :32467, :32476 |
| 0 | voice drunkenFist1 or 2 | :32508-32563 |
| 0 | Drunken Plus 2: `drunken` status chaAdjust(12) on the own client; its apply puts `Effects/drunken` at bounds.center + 0.5 × height up, identity, parented to the hero | :32576-32591; CharacterControl.cs:35396-35405 |
| 0.2 | Drunken Spin: `drunkenSpin` at position + TransformDirection(0, 0.5, 0.5), the hero's rotation (own drunkenFist sound); hit 1 | Yield(2, 0.2) :32619; :31621-31645, :31718 |
| 0.5 | stop; `drunkenSpin` again; hit 2 | Yield(3, 0.3) :32611 (from :31712 / :31831); :31853-31882 |
| 0.57 / 0.7 | speed 7 / speed 9, hit 3 | Yield(4, 0.07) :32615; Yield(5, 0.13) :32623; :32075, :32102 |
| 0.86 | stop, hit 4 | Yield(6, 0.16) :32636; :32250 |
| 1.2 | standby | Yield(7, 0.34) :32625; :32397 |

- **The drunken look's height:** the Panda's CharacterController has m_Center y 0.49 and m_Height 0.8 (rip
  `heroes/panda/Panda.prefab`, lines 709-715), so 0.49 + 0.4 = **0.89 m**.
  - It has no EffectControl and is destroyed with the status (CharacterControl.cs:15786-15793), which lasts 12 s at
    CHA 1: kill 10, `single`.
- Without Drunken Spin the effect is `drunkenFist` at the same spot (:31660-31680).

## Fuujin Ken (`fujinKen1` 1.0 s, `fujinKen2` 0.53 s loop, `fujinKen3` 0.9 s)

Source: RPC_fuujinKen :40786-41483.

| time | what happens | source |
|---|---|---|
| 0 | fujinKen1 (0.2 s fade, Once); noForce 9 s | :41139, :41159 |
| 0 | voice fuujinKen1 or 2 | :41193-41248 |
| 0 | `fuujinKen_ring1` at the hero (EC 1 + 1, own fuujinken1 sound) | :41261-41279 |
| 0.5 | `fuujinKen_ring2`, the tornado (EC 8 + 1, followPosition, followState; its own loop fuujinken2, AudioControl, EmitterControl, Animation) | Yield(2, 0.5) :41465; :40922-40940 |
| 1.0 | fujinKen2 cut in, Loop | Yield(3, 0.5) :41475; :40994-40999 |
| 1.0 + 0.4 i, i = 0-19 | FindAreaTarget(12, 9): pull; fuujinKen_hit only within 2 m | :41352-41420; Yield(4, 0.4) :41463 |
| 9.0 | fujinKen3 cut in; `fuujinKen_ring3` at the hero (EC 2) | :41296-41322 |
| 9.7 | standby | Yield(5, 0.7) :41461; :41057 |

- The ring2 tornado ends by its own life: 0.5 + 8 = 8.5 s, then 1 s of after-life, before the 9.7 s standby. So it
  needs no cut. A followState cut written on fujinKen3's clock would come wrong at the step change (index.html:5315-5318).
- **Page line:** "Fuujin Ken: fujinKen1 fujinKen2*@8 fujinKen3" stands as written. The icon line is item 7.

## Heaven Palm (`heavenPalm`, 4.0 s)

Source: RPC_heavenPalm :39643-40353; RPC_heavenPalm_hit :9516-9551.

| time | what happens | source |
|---|---|---|
| 0 | heavenPalm (0.2 s fade, Once); moveSpeed -2; noForce 4 s | :40176, :40185, :40188 |
| 0 | voice heavenPalm1 or 2 | :40220-40275 |
| 0 | `heavenPalm_ring` at the hero (EC 3.6, followState; the heavenPalm_shadow mesh plays root) | :40288-40304 |
| 0.7 | moveSpeed -1; hitTime 1.2 | Yield(2, 0.7) :40336; :39801, :39821 |
| every frame to 2.8 | faces the target; a pulse on the first frame after actionTime + hitTime (1.2 -> 1.8 -> 2.2 -> 2.6), own client | YieldDefault(3) :40339; :39928-40054 |
| each pulse | `heavenPalm` at the target's position, Quaternion.identity, localScale 1.5 at rank 2 (EC 2, own heavenPalm_hit sound); the (2 sLv + 2 + SF) m area hit | :40060; :9539-9548; :40077 |
| 3.3 / 3.7 | stop / standby | Yield(4, 0.5) :40341; Yield(5, 0.4) :40348; :39876 |

- **"First frame after"** (`Time.time <= actionTime + hitTime` skips, :39982): at 60 fps that is 1/60 s late, so 1.22,
  1.82, 2.22, 2.62 (the Mole's dig_dust 0.117 precedent).
- The blasts are at the target point's feet, `d 10`.
- heavenPalm_ring's life of 3.6 ends before the standby (3.7), so it needs no cut.
- Without a target (tID == 0) the skill does nothing (:40131). It is target-mode, so the tile assumes the target.

## Lotus Palm (`lotusPalm`, 2.0 s)

Source: RPC_lotusPalm :39066-39599; RPC_lotusPalm_hit :9466-9489.

| time | what happens | source |
|---|---|---|
| 0 | lotusPalm (0.2 s fade, Once); noForce 2 s | :39337, :39357 |
| 0 | voice lotusPalm1 or 2 | :39391-39446 |
| 0 | `lotusPalm_ring` at the hero (EC 2, followState; the lotusPalm_shadow mesh; own lotusParm_ring sound) | :39459-39477 |
| to 1.4 | faces the target every frame | :39573-39579, YieldDefault(2) :39597 |
| 1.4 | `lotusPalm` at target.collider.ClosestPointOnBounds(mPos + up), LookRotation(the hero's forward) (EC 1, own lotusPalm_hit sound), before the hit roll, so it is drawn even on a dodge | Time ≥ actionTime + 1.4 :39494; :39510-39513; :9489 |
| 1.8 | standby | Yield(3, 0.4) :39593; :39224 |

- **The contact:** with the standard target body (centre 0.6 m up, height 1, radius 0.3, at 10 m; Bat decision 4), the
  bounds' closest point to (0, 1, 0) is **(0, 1, 9.7)**. That is the guardian's hit spot.
- lotusPalm_ring: cut 1.8.

## Pummel (`pummel`, 1.5 s)

Source: RPC_pummel :24301-25119.

| time | what happens | source |
|---|---|---|
| 0 | pummel (0.1 s fade, Once) | :24910 |
| 0 | voice pummel1 or 2 | :24959-25014 |
| 0 | `pummel_dust` at the hero, its rotation (EC 0.5) | :25027-25045 |
| 0.1 | moveSpeed 16 | Yield(2, 0.1) :25111; :24448 |
| 0.2 | stop; Ogre Impact: `pummel_ogre` at the hero (EC 1, followState; StaticMesh + AlphaTimer; own pummel_ogre sound) | Yield(3, 0.1) :25115; :24475-24504 |
| 0.2 + 0.1 k, k = 0-4 | jab k: the Ogre box (2, 2, 3, 3), no sound with #422 | IL_B0 :24743-24862 |
| 0.25 + 0.1 k | `pummel_ogreArm1` at position + TransformDirection(R(0.2, 0.6), R(0.5, 1.5), R(0.5, 0.7)), the hero's rotation (EC 0.5, velocity 0, 0, 2) | Yield(4, 0.05) :25117; :24547-24565 |
| 0.3 + 0.1 k | `pummel_ogreArm2` at TransformDirection(R(-0.6, -0.2), R(0.5, 1.5), R(0.5, 0.7)) | Yield(5, 0.05) :25087; :24583-24601; i++ :25077 |
| 0.8 / 1.0 / 1.2 | step back at -6 / stop / standby | Yield(7, 0.1) :25096; Yield(8, 0.2) :25092; Yield(9, 0.2) :25106; :24690 |

- The arms' velocity is turned by the spawned rotation, so they fly ahead at 2 m/s (index.html:4246).
- pummel_ogre's life (0.2 + 1) ends at the standby, so it needs no cut.
- The random offsets need P3.

## Qi Strike (`qiStrike1` 2.97 s, Delay Qi's hold on `root`, `qiStrike2` 0.77 s)

Sources: RPC_qiStrike1 :22845-23290; RPC_delayQi :23981-24272; RPC_qiStrike2 :23328-23931; the status
CharacterControl.cs:35338-35371.

| time | what happens | source |
|---|---|---|
| 0 | qiStrike1 (0.2 s fade, Once) | :23132 |
| 0 | voice qiStrike1 or qiStrike2, at random | :23173-23228 |
| 0 | `qiStrike_ring` at the hero (EC 6, followPosition, followState; its own looping qiStrike1 sound) | :23241-23259 |
| to 4.0 | faces the target every frame until actionTime + 1 + sLv = 4 s | :22993-23028 |
| 4.0 | Delay Qi #214: RPC_delayQi | :23036-23042 |
| hold 0 | myCommand delayQi, so qiStrike_ring's followState ends it (EffectControl.cs:226-232 compares actionState **and** myCommand) | :24146 |
| hold 0 | voice delayQi | :24181-24199 |
| hold 0 | `delayQi_ring` at the hero (EC 1, own delayQi sound) | :24211-24229 |
| hold 0 | CrossFade(root, 0.2) | :24246 |
| hold 0 | the delayQi status, chaAdjust(3) + 3 = 6 s: `Effects/delayQi` (EC 12, LineEmitter) parented to the hero, localPosition 0 | :24255; CharacterControl.cs:35342-35371 |
| hold 0.2 | standby (the hold is idle) | Yield(2, 0.2) :24269; :24110 |
| the next attack press | RPC_qiStrike2 at the status level | doNormalAttack :7896-7930 |
| release 0 | qiStrike2 (0.2 s fade); moveSpeed 16 | :23665, :23680 |
| release 0 | voice qiStrike3 | :23712-23730 |
| release 0 | the status removed (delayQiFx destroyed, CharacterControl.cs:15753-15757) | :23742-23748 |
| release 0 | `delayQi_fire` at the hero | :23753-23771 |
| release 0 | Qi Burst: `qiBurst` at the hero (EC 2, followState; StaticMesh fist, Animation root) | :23786-23810 |
| release 0 | Sounds/qiStrike | :23877-23893 |
| release 0.2 | stop; the 6 m box | Yield(2, 0.2) :23929; :23475-23503 |
| release 0.6 | standby | Yield(3, 0.4) :23927; :23604 |

- **The hold** runs until the player presses attack, at most 6 s. The SEQ rule gives at least 3 s for a hold that runs
  until the player lets go (Mole decisions header), so it is held **3 s**.
- **Page lines:**
  - `SEQ.panda`: "Qi Strike: qiStrike1@4 root*~@3 qiStrike2~" (was "qiStrike1@4 qiStrike2~").
  - Cue key `@QiStrike:root`.
  - `SEQ_SKILL.panda = { "@QiStrike": "qiStrike" }`. This keeps any effect-only `root` tile's icon off this tile
    (moveSkillIcons, index.html:3415-3426), the Mole's `@ChargeAttack` precedent.
- qiStrike_ring is cut 4 at the step change (fxStart :5315-5318); qiBurst is cut 0.6.
- delayQi has kill 3 (the release).

---

## Paste-ready cue entries for wardrobe/fx_cues/panda.json

Validated in `C:\work\12tails-wardrobe\checks\fx_panda_research\skills_a\cues_whole.json` (times and kinds; the whys
added here).

```json
{
  "ashura": {
    "why": "Panda.cs RPC_ashura (:30346-30843), Ashura 2 (#272; addTimeOut 300 s :30659): clip (0.2 fade, Once, :30668-30671) and voice ashuraGate1 / ashuraGate2 (Random.Range(0, 2) :30709-30792) at 0; Yield(2, 0.4) (:30785): Effects/ashuraRing at the hero, hero rotation (createEffect :30498-30510; EffectControl 1, followPosition; plays its own Sounds/ashura_ring); the local player's motion blur (:30532) left out; Yield(3, 0.4) (:30806): at 0.8 s the ashura status, chaAdjust(24) = 24 s at CHA 1, on the own client (RPC_AddStatus :30572), whose apply does setColor(1, 0, 0) on every renderer under the hero (CharacterControl.cs:35488-35497, :21702-21800: HERO_SKINS ashura, tint 1 / 0.86, 0, 0) and puts Effects/ashura (named ashuraFx; a LineEmitter, no EffectControl) under the Root bone, localPosition 0, Euler(0, 0, 0), scale 1 (CharacterControl.cs:35500-35515), both undone by the removal (:15830-15846): cut at 10 s, single (a refreshed status applies once); the +5 x sLv SP every 0.5 s draws nothing; Yield(4, 0.4) (:30798): standby at 1.2 s (:30598); the next charge press starts RPC_ashuraFist (doBeginCharge :8215-8231): the SEQ's ashura@1.2 ashuraFist",
    "cues": [
      [0, "voice", "ashuraGate1|ashuraGate2"],
      [0.4, "fx", "ashuraRing"],
      [0.8, "skin", "ashura", {"kill": 10}],
      [0.8, "fx", "ashura", {"bone": "Root", "kill": 10, "single": true}]
    ]
  },
  "ashuraFist": {
    "why": "Panda.cs RPC_ashuraFist (:30843-31420), Ashura's charge-press replacement under the ashura status (doBeginCharge :8215-8231, the status level 2): clip cut in (PlayAnimation(ashuraFist, 0), Once, :31281-31284) and voice ashuraFist1 / ashuraFist2 (Random.Range(0, 2) :31322-31411) at 0; Yield(2, 0.3) (:31398): moveSpeed 6 (:30987; the 3.6 m lunge, the hero does not travel); Yield(3, 0.6) (:31416): at 0.9 s stop (:31009) and Effects/ashuraFist Instantiated at the hero's position, Quaternion.identity (:31020-31032; EffectControl 1 + 1; plays its own Sounds/ashuraFist); the local player's camera shake (:31052) left out; two hits 0.2 s apart in a 3 m circle (FindAreaTarget :31197, hit :31230, Yield(4, 0.2) :31414) never reach the 10 m target; at 1.3 s sp = 0 and standby (:31118-31141)",
    "cues": [
      [0, "voice", "ashuraFist1|ashuraFist2"],
      [0.9, "fx", "ashuraFist"]
    ]
  },
  "climbingCliff": {
    "why": "Panda.cs RPC_climbingCliff (:27194-27752), Climbing Cliff (one rank; started by Tiger Toss's grab on a target at least 3 m tall with SP < 40, RPC_grab :26178-26256): clip cut in (PlayAnimation(climbingCliff, 0), Once, :27607-27610), noForce 2 s (:27619, nothing drawn), voice climbingCliff (one file, :27651-27669) and Effects/climbingCliff_ring at the hero, hero rotation (createEffect :27693-27711; EffectControl 3, followPosition, followState) at 0; the toast ClimbingCliff! (:27687) left out; 18 ticks of 0.1 s (i >= 18 :27347, Yield(2, 0.1) :27750): on i = 1, 3, ... 15 a hit on the selected target itself (ActorNrList[tID] :27500, hit :27516, no range test: it lands with the target at 10 m too; every hit assumed landed) and then RPC_climbingCliff_hit at the Root bone's position + 0.3 x forward (mHitPos = Root :27725, :27538) = Effects/climbingCliff_hit Instantiated there, LookRotation(the hero's forward) (:8734-8760; EffectControl 1; plays its own Sounds/nAttack_hit1): atBone Root, d 0.3; the step back at -4 m/s on ticks 12-16 (:27566, :27580) not travelled; standby at 1.8 s (:27370): the ring's followState cut 1.8",
    "cues": [
      [0, "voice", "climbingCliff"],
      [0, "fx", "climbingCliff_ring", {"cut": 1.8}],
      [0.1, "fx", "climbingCliff_hit", {"atBone": "Root", "d": 0.3}],
      [0.3, "fx", "climbingCliff_hit", {"atBone": "Root", "d": 0.3}],
      [0.5, "fx", "climbingCliff_hit", {"atBone": "Root", "d": 0.3}],
      [0.7, "fx", "climbingCliff_hit", {"atBone": "Root", "d": 0.3}],
      [0.9, "fx", "climbingCliff_hit", {"atBone": "Root", "d": 0.3}],
      [1.1, "fx", "climbingCliff_hit", {"atBone": "Root", "d": 0.3}],
      [1.3, "fx", "climbingCliff_hit", {"atBone": "Root", "d": 0.3}],
      [1.5, "fx", "climbingCliff_hit", {"atBone": "Root", "d": 0.3}]
    ]
  },
  "crumblingMountain": {
    "why": "Panda.cs RPC_crumblingMountain (:27796-28616), Crumbling Mountain with Crushing Monolith #432 on (passives rule; started by the grab on a tall target with SP >= 40, RPC_grab :26209-26224): clip cut in (PlayAnimation(crumblingMountain, 0), Once, :28392-28395), noForce 3 s (:28404), voice climbingCliff (:28436-28454) and climbingCliff_ring at the hero (createEffect :28478-28496; EffectControl 3, followPosition, followState) at 0; #432 (:28513): three Effects/crushingMonolith (the Panda doubles: SkinnedMeshRenderer, Animation, AlphaTimer; EffectControl 3 + 1, followPosition, followState) at the target's position - (radius + 0.1) x forward with LookRotation(-forward), + (radius + 0.1) x right with LookRotation(-right), - (radius + 0.1) x right with LookRotation(right) (createEffect :28565-28575): the target at the 10 m point with the standard body radius 0.3 (plans/fx_bat/decisions.md 3) = d 9.6 rot [0, 180, 0], x 0.4 d 10 rot [0, -90, 0], x -0.4 d 10 rot [0, 90, 0]; 28 ticks of 0.1 s (i >= 28 :27949, Yield(2, 0.1) :28611): on i = 2, 5, 9, 10, 11, 15-22 (13 hits, :28044-28116) hit(432) on the selected target (:28181; no range test, assumed landed) and RPC_crushingMonolith_hit at Root.position + 0.3 x forward (:28203) = Effects/crushingMonolith_hit there, LookRotation(forward) (:9768-9794; EffectControl 1; plays its own Sounds/crushingMonolith_hit): atBone Root, d 0.3 (without #432 climbingCliff_hit, :28223-28245); at i = 16 (1.6 s) voice crumblingMountain (:28267-28332; the toast left out); the step back on ticks 24-27 (:28351, :28365) not travelled; standby at 2.8 s (:27972): the ring's and the doubles' followState cut 2.8",
    "cues": [
      [0, "voice", "climbingCliff"],
      [0, "fx", "climbingCliff_ring", {"cut": 2.8}],
      [0, "fx", "crushingMonolith", {"d": 9.6, "rot": [0, 180, 0], "cut": 2.8}],
      [0, "fx", "crushingMonolith", {"x": 0.4, "d": 10, "rot": [0, -90, 0], "cut": 2.8}],
      [0, "fx", "crushingMonolith", {"x": -0.4, "d": 10, "rot": [0, 90, 0], "cut": 2.8}],
      [0.2, "fx", "crushingMonolith_hit", {"atBone": "Root", "d": 0.3}],
      [0.5, "fx", "crushingMonolith_hit", {"atBone": "Root", "d": 0.3}],
      [0.9, "fx", "crushingMonolith_hit", {"atBone": "Root", "d": 0.3}],
      [1.0, "fx", "crushingMonolith_hit", {"atBone": "Root", "d": 0.3}],
      [1.1, "fx", "crushingMonolith_hit", {"atBone": "Root", "d": 0.3}],
      [1.5, "fx", "crushingMonolith_hit", {"atBone": "Root", "d": 0.3}],
      [1.6, "fx", "crushingMonolith_hit", {"atBone": "Root", "d": 0.3}],
      [1.6, "voice", "crumblingMountain"],
      [1.7, "fx", "crushingMonolith_hit", {"atBone": "Root", "d": 0.3}],
      [1.8, "fx", "crushingMonolith_hit", {"atBone": "Root", "d": 0.3}],
      [1.9, "fx", "crushingMonolith_hit", {"atBone": "Root", "d": 0.3}],
      [2.0, "fx", "crushingMonolith_hit", {"atBone": "Root", "d": 0.3}],
      [2.1, "fx", "crushingMonolith_hit", {"atBone": "Root", "d": 0.3}],
      [2.2, "fx", "crushingMonolith_hit", {"atBone": "Root", "d": 0.3}]
    ]
  },
  "comboLink": {
    "why": "Panda.cs RPC_comboLink (:40418-40751), Combo Link #442 (one rank; the dispatcher refuses it with no team combo, :6187-6208: the tile assumes one, as Detonate assumes its nuke): clip (0.2 fade, Once, :40672-40675) and Effects/comboLink_ring at the hero, hero rotation (createEffect :40684-40702; EffectControl 1 + 1, followPosition; plays its own Sounds/comboLink_ring) at 0, no voice; the local player's motion blur (:40725) left out; Yield(2, 0.4) (:40749): atkUp (5, chaAdjust(6), +n ATK) on the own client (:40570; CharacterControl.cs:33176-33186, deltaAtk only) and the toast (:40576), nothing drawn; Yield(3, 0.4) (:40747): standby at 0.8 s (:40602)",
    "cues": [
      [0, "fx", "comboLink_ring"]
    ]
  },
  "drunkenFist": {
    "why": "Panda.cs RPC_drunkenFist (:31474-32638), Drunken Fist 2 with Drunken Plus 2 (#304) and Drunken Spin #403 (passives rule): clip (0.2 fade, Once, :32467-32470), moveSpeed 3 (:32476) and voice drunkenFist1 / drunkenFist2 (Random.Range(0, 2) :32508-32563) at 0; the drunken status at level 2 for chaAdjust(12) = 12 s on the own client (:32576-32591), whose apply puts Effects/drunken (named drunkenFx; legacy particles, no EffectControl) at the CharacterController's bounds centre + 0.5 x height up = 0.49 + 0.4 = 0.89 m (rip Panda.prefab m_Center y 0.49, m_Height 0.8, lines 709-715), Quaternion.identity, parented to the hero (CharacterControl.cs:35396-35405), destroyed with the status (:15786-15793): kill 10 (the 10 s cut), single; Yield(2, 0.2) (:32619): at 0.2 s Drunken Spin (getDrunkenSpinLv :31621) Effects/drunkenSpin at position + TransformDirection(0, 0.5, 0.5), the hero's rotation (Instantiate :31633-31645; plays its own Sounds/drunkenFist; drunkenFist without #403, :31660-31680) and hit 1; Yield(3, 0.3) (:32611): at 0.5 s stop (:31853), drunkenSpin again (:31858-31882), hit 2; Yield(4, 0.07) / Yield(5, 0.13) / Yield(6, 0.16) (:32615, :32623, :32636): speed 7 at 0.57, speed 9 and hit 3 at 0.7, stop and hit 4 at 0.86 (:32075, :32102, :32250); the four 1 m boxes (:31718, :31940, :32115, :32263) never reach the 10 m target, so no drunk status on a foe; Yield(7, 0.34) (:32625): standby at 1.2 s (:32397)",
    "cues": [
      [0, "voice", "drunkenFist1|drunkenFist2"],
      [0, "fx", "drunken", {"y": 0.89, "kill": 10, "single": true}],
      [0.2, "fx", "drunkenSpin", {"y": 0.5, "d": 0.5}],
      [0.5, "fx", "drunkenSpin", {"y": 0.5, "d": 0.5}]
    ]
  },
  "fujinKen1": {
    "why": "Panda.cs RPC_fuujinKen (:40786-41483), Fuujin Ken #434 (one rank; addTimeOut 240 s :41124): clip (0.2 fade, Once, :41139-41144), noForce 9 s (:41159), voice fuujinKen1 / fuujinKen2 (Random.Range(0, 2) :41193-41248; the rip spells them fuujinken1 / 2) and Effects/fuujinKen_ring1 at the hero, hero rotation (createEffect :41261-41279; EffectControl 1 + 1, followPosition; plays its own Sounds/fuujinken1) at 0; Yield(2, 0.5) (:41465): at 0.5 s Effects/fuujinKen_ring2, the tornado, at the hero (createEffect :40922-40940; EffectControl 8 + 1, followPosition, followState: its life ends at 8.5 s, before the 9.7 s standby, so no cut; Animation, AudioControl, EmitterControl; its own looping Sounds/fuujinken2); the local player's motion blur (:40967) left out; Yield(3, 0.5) (:41475): fujinKen2 at 1.0 s (the SEQ's next step)",
    "cues": [
      [0, "voice", "fuujinKen1|fuujinKen2"],
      [0, "fx", "fuujinKen_ring1"],
      [0.5, "fx", "fuujinKen_ring2"]
    ]
  },
  "fujinKen3": {
    "why": "Panda.cs RPC_fuujinKen after the 20th tick (i >= 20 :41296; fujinKen2 cut in and looped at 1.0 s :40994-40999, ticks Yield(4, 0.4) :41463: the SEQ's fujinKen2*@8; each tick's 12 m pull, FindAreaTarget :41352, draws nothing, fuujinKen_hit only on enemies within 2 m :41414-41420, never the 10 m target): at 9.0 s fujinKen3 cut in (PlayAnimation(fujinKen3, 0), Once, :41300-41303) and Effects/fuujinKen_ring3 at the hero, hero rotation (createEffect :41306-41322; EffectControl 2); Yield(5, 0.7) (:41461): standby at 9.7 s (:41057)",
    "cues": [
      [0, "fx", "fuujinKen_ring3"]
    ]
  },
  "heavenPalm": {
    "why": "Panda.cs RPC_heavenPalm (:39643-40353), Heaven Palm 2 (#364; a target skill, tID == 0 does nothing :40131: the target at the 10 m point): clip (0.2 fade, Once, :40176-40179), moveSpeed -2 (:40185), noForce 4 s (:40188), voice heavenPalm1 / heavenPalm2 (Random.Range(0, 2) :40220-40275) and Effects/heavenPalm_ring at the hero, hero rotation (createEffect :40288-40304; EffectControl 3.6, followPosition, followState: its life ends before the 3.7 s standby, no cut; the heavenPalm_shadow mesh plays root) at 0; Yield(2, 0.7) (:40336): moveSpeed -1 and hitTime 1.2 (:39801, :39821); every frame (YieldDefault(3) :40339) until actionTime + 2.8 (:39928) the hero faces the target (:39969), and on the own client the first frame after actionTime + hitTime (Time.time <= ... skips, :39982; 1/60 s late at 60 fps: 1.22, 1.82, 2.22, 2.62) hitTime steps 1.2 -> 1.8 -> 2.2 -> 2.6 -> 99 (:40012-40054) and RPC_heavenPalm_hit(the target's position, :39964, :40060) = Effects/heavenPalm Instantiated there, Quaternion.identity, localScale 1.5 at sLv 2 (:9539-9548; EffectControl 2; plays its own Sounds/heavenPalm_hit): the target's feet, d 10, scale 1.5; the camera shake and blur (:39996, :40006) left out; the (2 sLv + 2 + SF) m area hit (:40077) draws nothing more; Yield(4, 0.5) (:40341): stop at 3.3 s (:39850); Yield(5, 0.4) (:40348): standby at 3.7 s (:39876)",
    "cues": [
      [0, "voice", "heavenPalm1|heavenPalm2"],
      [0, "fx", "heavenPalm_ring"],
      [1.22, "fx", "heavenPalm", {"d": 10, "scale": 1.5}],
      [1.82, "fx", "heavenPalm", {"d": 10, "scale": 1.5}],
      [2.22, "fx", "heavenPalm", {"d": 10, "scale": 1.5}],
      [2.62, "fx", "heavenPalm", {"d": 10, "scale": 1.5}]
    ]
  },
  "lotusPalm": {
    "why": "Panda.cs RPC_lotusPalm (:39066-39599), Lotus Palm 2 (#362; a target skill, tID == 0 does nothing :39276: the target at the 10 m point): clip (0.2 fade, Once, :39337-39342), noForce 2 s (:39357), voice lotusPalm1 / lotusPalm2 (Random.Range(0, 2) :39391-39446) and Effects/lotusPalm_ring at the hero, hero rotation (createEffect :39459-39477; EffectControl 2, followPosition, followState; the lotusPalm_shadow mesh plays root; plays its own Sounds/lotusParm_ring) at 0; every frame (YieldDefault(2) :39597) the hero faces the target (:39573-39579) until Time.time >= actionTime + 1.4 (:39494): RPC_lotusPalm_hit at target.collider.ClosestPointOnBounds(mPos + up) (:39510-39513), before the hit roll (:39528), so drawn on a dodge too = Effects/lotusPalm there, LookRotation(the hero's forward) (:9466-9489; EffectControl 1; plays its own Sounds/lotusPalm_hit): the standard target body's (plans/fx_bat/decisions.md 4) closest point to (0, 1, 0) is (0, 1, 9.7); Yield(3, 0.4) (:39593): standby at 1.8 s (:39224): the ring's followState cut 1.8",
    "cues": [
      [0, "voice", "lotusPalm1|lotusPalm2"],
      [0, "fx", "lotusPalm_ring", {"cut": 1.8}],
      [1.4, "fx", "lotusPalm", {"y": 1, "d": 9.7}]
    ]
  },
  "pummel": {
    "why": "Panda.cs RPC_pummel (:24301-25119), Pummel 2 (#223) with Ogre Impact #422 (passives rule): clip (0.1 fade, Once, :24910-24915), voice pummel1 / pummel2 (Random.Range(0, 2) :24959-25014) and Effects/pummel_dust Instantiated at the hero, hero rotation (:25027-25045; EffectControl 0.5) at 0; Yield(2, 0.1) (:25111): moveSpeed 16 (:24448; the 1.6 m lunge, not travelled); Yield(3, 0.1) (:25115): at 0.2 s stop (:24475) and #422 Effects/pummel_ogre at the hero (createEffect :24480-24504; EffectControl 1, followPosition, followState; StaticMesh + AlphaTimer; plays its own Sounds/pummel_ogre; its life ends at the 1.2 s standby, no cut); five jabs (i < 5 :24743) at 0.2 + 0.1 k: the Ogre box FindRecTarget(2, 2, 3, 3) (:24765; no punch1Fx with #422, :24778) never reaches the 10 m target (no pummel_hit, :24818-24828); after each jab Yield(4, 0.05) (:25117): Effects/pummel_ogreArm1 at position + TransformDirection(Random.Range(0.2, 0.6), Random.Range(0.5, 1.5), Random.Range(0.5, 0.7)), the hero's rotation (:24547-24565; EffectControl 0.5, velocity (0, 0, 2) turned by the rotation, StaticMesh + AlphaTimer), Yield(5, 0.05) (:25087): Effects/pummel_ogreArm2 at TransformDirection(Random.Range(-0.6, -0.2), Random.Range(0.5, 1.5), Random.Range(0.5, 0.7)) (:24583-24601), i++ and the next jab at once (:25077): arms at 0.25 + 0.1 k and 0.3 + 0.1 k (x / y / d ranges: part P3); Yield(7, 0.1) (:25096): moveSpeed -6 at 0.8 (:24637); Yield(8, 0.2) (:25092): stop at 1.0 (:24664); Yield(9, 0.2) (:25106): standby at 1.2 s (:24690)",
    "cues": [
      [0, "voice", "pummel1|pummel2"],
      [0, "fx", "pummel_dust"],
      [0.2, "fx", "pummel_ogre"],
      [0.25, "fx", "pummel_ogreArm1", {"x": [0.2, 0.6], "y": [0.5, 1.5], "d": [0.5, 0.7]}],
      [0.3, "fx", "pummel_ogreArm2", {"x": [-0.6, -0.2], "y": [0.5, 1.5], "d": [0.5, 0.7]}],
      [0.35, "fx", "pummel_ogreArm1", {"x": [0.2, 0.6], "y": [0.5, 1.5], "d": [0.5, 0.7]}],
      [0.4, "fx", "pummel_ogreArm2", {"x": [-0.6, -0.2], "y": [0.5, 1.5], "d": [0.5, 0.7]}],
      [0.45, "fx", "pummel_ogreArm1", {"x": [0.2, 0.6], "y": [0.5, 1.5], "d": [0.5, 0.7]}],
      [0.5, "fx", "pummel_ogreArm2", {"x": [-0.6, -0.2], "y": [0.5, 1.5], "d": [0.5, 0.7]}],
      [0.55, "fx", "pummel_ogreArm1", {"x": [0.2, 0.6], "y": [0.5, 1.5], "d": [0.5, 0.7]}],
      [0.6, "fx", "pummel_ogreArm2", {"x": [-0.6, -0.2], "y": [0.5, 1.5], "d": [0.5, 0.7]}],
      [0.65, "fx", "pummel_ogreArm1", {"x": [0.2, 0.6], "y": [0.5, 1.5], "d": [0.5, 0.7]}],
      [0.7, "fx", "pummel_ogreArm2", {"x": [-0.6, -0.2], "y": [0.5, 1.5], "d": [0.5, 0.7]}]
    ]
  },
  "qiStrike1": {
    "why": "Panda.cs RPC_qiStrike1 (:22845-23290), Qi Strike 3 (#213) with Delay Qi #214 and Qi Burst #412 (passives rule): clip (0.2 fade, Once, :23132-23135), voice qiStrike1 / qiStrike2 (Random.Range(0, 2) :23173-23228) and Effects/qiStrike_ring at the hero, hero rotation (createEffect :23241-23259; EffectControl 6, followPosition, followState; plays its own looping Sounds/qiStrike1) at 0; every frame (YieldDefault(2) :23287) the hero faces the target (:23014) until actionTime + 1 + sLv = 4 s (:23028; the SEQ's qiStrike1@4): #214 starts RPC_delayQi (:23036-23042), which sets myCommand delayQi (:24146): the ring's followState ends it (EffectControl.cs:226-232 compares actionState and myCommand): cut 4, at the step change (index.html fxStart)",
    "cues": [
      [0, "voice", "qiStrike1|qiStrike2"],
      [0, "fx", "qiStrike_ring", {"cut": 4}]
    ]
  },
  "@QiStrike:root": {
    "why": "Panda.cs RPC_delayQi (:23981-24272), Delay Qi #214 at the end of Qi Strike's charge (:23036-23042): myCommand delayQi (:24146), voice delayQi (one file, :24181-24199), Effects/delayQi_ring at the hero, hero rotation (createEffect :24211-24229; EffectControl 1; plays its own Sounds/delayQi), CrossFade(root, 0.2) (:24246: the SEQ's root*~) and the delayQi status at sLv 3 for chaAdjust(3) + 3 x getQiBurstLv() = 6 s (:24255), whose apply puts Effects/delayQi (named delayQiFx; EffectControl 12, a LineEmitter) under the hero, localPosition 0, scale 1 (CharacterControl.cs:35342-35371), all at 0; Yield(2, 0.2) (:24269): standby (:24110); the hold lasts until the next attack press releases RPC_qiStrike2 at the status level (doNormalAttack :7896-7930), at most 6 s: held 3 s (the SEQ rule's at least 3 s for a hold the player ends), the release removing the status and its delayQiFx (:23742-23748; CharacterControl.cs:15753-15757): kill 3",
    "cues": [
      [0, "voice", "delayQi"],
      [0, "fx", "delayQi_ring"],
      [0, "fx", "delayQi", {"kill": 3}]
    ]
  },
  "qiStrike2": {
    "why": "Panda.cs RPC_qiStrike2 (:23328-23931), Delay Qi's release at sLv 3: clip (0.2 fade, Once, :23665-23668), moveSpeed 16 (:23680; the 3.2 m dash, not travelled), voice qiStrike3 (one file, :23712-23730), the delayQi status removed (:23742-23748) and Effects/delayQi_fire Instantiated at the hero, hero rotation (:23753-23771; EffectControl 1; plays its own Sounds/delayQi), Qi Burst #412 (getQiBurstLv :23786): Effects/qiBurst at the hero, hero rotation (createEffect :23792-23810; EffectControl 2, followPosition, followState; the StaticMesh fist with Animation root; qiStrike without #412, :23827-23845), the local player's motion blur (:23871) left out, and Sounds/qiStrike (PlayOneShot :23877-23893) at 0; Yield(2, 0.2) (:23929): stop (:23475) and the 1 + 5 m box (:23503) never reaches the 10 m target (no qiStrike_hit, :23532-23542); Yield(3, 0.4) (:23927): standby at 0.6 s (:23604): qiBurst's followState cut 0.6",
    "cues": [
      [0, "voice", "qiStrike3"],
      [0, "sound", "qiStrike"],
      [0, "fx", "delayQi_fire"],
      [0, "fx", "qiBurst", {"cut": 0.6}]
    ]
  }
}
```

## Page and script lines

| where | line |
|---|---|
| index.html `SEQ.panda` | add "Ashura: ashura@1.2 ashuraFist", "Tiger Toss: grab@0.2 tigerToss", "Climbing Cliff: grab@0.2 climbingCliff", "Crumbling Mountain: grab@0.2 crumblingMountain"; change "Qi Strike: qiStrike1@4 qiStrike2~" to "Qi Strike: qiStrike1@4 root*~@3 qiStrike2~"; "Fuujin Ken: fujinKen1 fujinKen2*@8 fujinKen3" stands |
| index.html `SEQ_SKILL` | `panda: { "@QiStrike": "qiStrike" }` |
| index.html `HERO_SKINS` | `"ashura": () => ({ tint: [1 / 0.86, 0, 0] })` (P1) |
| index.html Fx / cueOf | `atBone` (P2); range-valued x / y / d (P3) |
| wardrobe_fx_check.py OPTS | add `atBone` |
| wardrobe_skill_icons.py `CLIP_SKILLS` | `"panda": {"fujinKen1": ["fuujinKen"], "fujinKen2": ["fuujinKen"], "fujinKen3": ["fuujinKen"]}` |
| wardrobe_fx_inventory.py | the status effects ashura, drunken, drunk, delayQi (CharacterControl-loaded), ready |

No NEVER_PLAYED: every clip of mine is played by its coroutine.

## Parts summary

| part | what | for |
|---|---|---|
| P1 Ashura tint | HERO_SKINS body look `ashura`, tint (1/0.86, 0, 0) | Ashura |
| P2 `atBone` | cue option: spawn at a hero bone's world position (+ x / y / d along the facing), hero's facing, not parented | Climbing Cliff, Crumbling Mountain |
| P3 range offsets | cueOf: x / y / d as `[lo, hi]` floats drawn at the clip start | Pummel |

All three are small, page-only parts, with no new extractor work. The data needs `wardrobe_fx.py panda` once the cues
are in.

## Bible findings to offer the user

- **Ashura's status comes 0.8 s after the cast.** ashuraRing is at 0.4 s and the status (tint, SP gain) at 0.8 s
  (:30785, :30806, :30572). A cast cut short before then gives no Ashura.
- **The climbs' hit flashes are drawn in two different places.** On the own client they are at the Panda's Root +
  0.3 m; other clients get Root + 1 m (ActionEvent passes `forward` unscaled: :27538 vs :27549, :28203 vs :28214).
  The climbs' hits also never test range: once grabbed, the target is hit wherever it goes (:27500, :28137).
- **Pummel with Ogre Impact plays no jab sound:** punch1Fx is only in the non-Ogre branch (:24778).
- **Heaven Palm's blast is 1.5x at rank 2** (:9548), and its pulses come on the first frame after 1.2 / 1.8 / 2.2 /
  2.6 s, not at them (:39982).
- **Lotus Palm's flash is drawn before the hit roll** (:39513 before :39528), so a dodged Lotus Palm still shows it.
- **Combo Link plays no voice.**
- **Crushing Monolith's three doubles** stand at the target's front and both sides (radius + 0.1 m) for the 2.8 s climb
  (:28565-28575).

## Open questions (recommended answers)

1. **Ashura Fist: in the Ashura tile, or a tile of its own?** Recommended: in the Ashura tile, "Ashura: ashura@1.2
   ashuraFist". It is Ashura's own sub-state with no icon or roster entry (the Bible's note), and it only exists under
   the red form, which the tile then shows (Chameleon's Tent precedent: cast and sleep in one tile).
2. **Qi Strike with Delay Qi:** the charge 4 s, the idle hold 3 s, then the release? Recommended: yes, "qiStrike1@4
   root*~@3 qiStrike2~". Passives on means Delay Qi always diverts the punch (:23036). The 3 s is the SEQ rule's hold.
   A separate Delay Qi tile would be identical, so it gets none.
3. **The climb hit flashes:** build `atBone` (P2), or let them ride the Root bone? Recommended: build atBone. The game
   leaves them where they spawned, and the climb moves the hips. Riding is the fallback if P2 slips.
4. **Crushing Monolith's doubles at the 10 m target** (standard radius 0.3), though the grab needs the target in contact
   and at least 3 m tall? Recommended: the 10 m rule as written (the enemy-at-target rule, Bat decision 3's body). The
   climb's own flashes stay on the hero's body. Alternative for the user: move the target to the grab's 1 m contact for
   the grab family only.
5. **Pummel's random arm offsets:** build P3? Recommended: yes. Whole-metre `spread` cannot draw 0.2-0.6 m, and fixed
   midpoints would lose the game's scatter.
6. **Climbing Cliff's own tile**, though with the passives on Crumbling Mountain replaces it at SP ≥ 40? Recommended:
   keep both, one tile per skill. Climbing Cliff is still what the game plays below 40 SP (:26209).
7. **Tiger Toss's sequence:** "grab@0.2 tigerToss". Recommended: yes. The tigerToss cues are skills_b's; this report
   only supplies the opening step.
8. **Heaven Palm's frame-late pulses** (1.22 / 1.82 / 2.22 / 2.62) or the round 1.2 / 1.8 / 2.2 / 2.6? Recommended:
   1.22 etc., the Mole's dig_dust precedent (a strict > on the frame loop at 60 fps).
9. **Combo Link and the palms with no target / combo** (the game refuses them): assume the condition? Recommended: yes,
   as Detonate assumes its nuke (Mole decision). The palms are target skills: the target at 10 m.
10. **The status looks' cut** (Ashura's tint and ashuraFx, Drunken Plus's drunkenFx: 24 s and 12 s): 10 s with
    `single`? Recommended: yes. That is the 10 s rule, and `single` keeps one copy when the tile loops (a refreshed
    status in the game applies once).

## Verification

Not yet run: this is the researcher's report, for a checker's re-trace.

## Verification (13/11/2026)

Checker, office PC. Re-derived from `C:\Users\Jump\Desktop\12tails\DecompiledSource\Panda.cs` and `CharacterControl.cs`,
the probe (`wardrobe_fx.py panda --probe` of every effect named here: all decode), the rip's `heroes/panda/voices` /
`sounds` and `Panda.prefab`, `wardrobe/index.html`, `pipeline/wardrobe_fx_check.py`, `pipeline/wardrobe_skill_icons.py`
and the Bible's assets.js. Probes: `checks\fx_panda_research\verify\` (`co.sh`, `ymap.py`, `blocks.py`, `probe.json`).
The Verification wins over the report body.

**Confirmed** (no change):
- **Timelines:** every clip time and wait sum matches the code:
  - Ashura: 0.4 / 0.8 / 1.2; Ashura Fist 0.3 / 0.9 / 1.1.
  - The grab: 0.1 / 0.2 / 0.5, and its branches (height × scale < 3 and weight < 60 -> toss; SP ≥ 40 -> Crumbling
    Mountain, :26100-26256).
  - Climbing Cliff: i++ before each test, so i = 1 is at 0.1 s, the hits at 0.1 ... 1.5 and the standby at 1.8.
  - Crumbling Mountain: its 13 hit ticks, the voice at i = 16, the doubles' three spots and LookRotations
    (:28565-28575).
  - Combo Link: 0.4 / 0.8, no voice.
  - Drunken Fist: 0.2 + 0.3 + 0.07 + 0.13 + 0.16 + 0.34 = 1.2.
  - Fuujin Ken: i = 0 at 1.0, fujinKen3 at i = 20 = 9.0, standby 9.7.
  - Heaven Palm: hitTime 1.2 -> 1.8 -> 2.2 -> 2.6, scale 1.5, 3.3 / 3.7.
  - Lotus Palm: 1.4, ClosestPointOnBounds(mPos + up).
  - Pummel: five jabs 0.1 s apart from 0.2, the arms at +0.05 / +0.1, 0.8 / 1.0 / 1.2.
  - Qi Strike: actionTime + 1 + sLv = 4 at sLv 3, hasSkill(214) -> RPC_delayQi, CrossFade(root, 0.2),
    chaAdjust(3) + 3 × QiBurst; qiStrike2 0.2 / 0.6.
- **Status looks:** they are as cited (CharacterControl.cs:35335-35545: delayQi parented at local 0; drunken at
  bounds.center + 0.5 × height, with Panda.prefab m_Center y 0.49 and m_Height 0.8 = 0.89 m; ashura setColor(1, 0, 0) and
  ashuraFx under the `Root` bone, which the page rig has).
- **EffectControls:** they match the probe (qiStrike_ring 6 followState, qiBurst 2 followState, climbingCliff_ring 3
  followState, crushingMonolith 3 + 1, fuujinKen_ring2 8 + 1, heavenPalm_ring 3.6, lotusPalm_ring 2, pummel_ogre 1,
  pummel_ogreArm1 / 2 0.5 with velocity (0, 0, 2)).
- **Files:** every voice and sound file exists.
- **The block:** valid JSON, 14 keys / 75 cues, times sorted, kinds known. Its keys are Panda clips or the new
  "@QiStrike" SEQ's root. `atBone` and the range-valued x / y / d are the only new things.
- **TTO:** no released TTO item plays these clips.
- **The Fuujin Ken icon line:** the Bible has panda_fuujinKen1 / 5 only.

1. **Delay Qi gets its own tile.** Question 2's "a separate Delay Qi tile would be identical, so it gets none" goes
   against the standing rule (one tile per skill, with its Bible icon) and against effect_only.md.
   - **Evidence:** Delay Qi is a skill with its own RPC and Bible icon (`panda_delayQi1`; effect_only.md:40, :85). A
     passive with its own RPC riding another skill's clips gets a tile of its own (Chameleon decisions 12-13: Critical
     Plus; Mole decision 3: Sky Drill). effect_only.md's SEQ line is `"Delay Qi: qiStrike1@4 root*~@3 qiStrike2~"`.
   - **Correction:**
     - Keep this report's Qi Strike line `"Qi Strike: qiStrike1@4 root*~@3 qiStrike2~"` (passives on: the charge always
       diverts, :23036) and its `@QiStrike:root` entry.
     - Add effect_only's Delay Qi tile with the same steps.
     - Key its middle step `"@DelayQi:root"` with the same three cues as `@QiStrike:root` (`[0, "voice", "delayQi"]`,
       `[0, "fx", "delayQi_ring"]`, `[0, "fx", "delayQi", {"kill": 3}]`).
     - Drop effect_only's `@DelayQi:qiStrike1` / `@DelayQi:qiStrike2`. This report's plain `qiStrike1` / `qiStrike2`
       keys serve both tiles, because fxStart falls back to `tab[clip]` (index.html:5333). effect_only's qiStrike2 copy
       also lacks qiBurst's `cut 0.6` (followState, standby at 0.6 s :23604), which this report has right.
     - `SEQ_SKILL "@QiStrike": "qiStrike"` stays (with "@DelayQi": "delayQi" beside it, each tile shows its own icon).

2. **SEQ lines and SEQ_SKILL, merged with skills_b:**
   - **Tiger Toss:** skills_b writes `"Tiger Toss: grab^@0.2 tigerToss!"`, this report `"grab@0.2 tigerToss"`.
     - They play the same. A first step's `^` is not read (play() always fades a first step 0.2 s unless it is `!`,
       index.html:1519, :1551), and a later step with no mark is a cut.
     - Use this report's three grab lines as written.
   - **SEQ_SKILL:** one panda entry for both halves and effect_only.md:
     `panda: { "@QiStrike": "qiStrike", "@RaijinKen": "raijinKen", "@TigerToss": "tigerToss", "@MysticSage": "mysticSage",
     "@SafeGuard": "safeGuard", "@SacredSageTechnique": "sacredSageTechnique", "@DelayQi": "delayQi" }`.
   - **The other page lines here stand:** the Ashura and climb lines, HERO_SKINS ashura, atBone and the ranges (P1-P3),
     the OPTS line and CLIP_SKILLS fujinKen1-3.

3. **Question 4 (Crushing Monolith's doubles at the 10 m target) is confirmed, and it binds skills_b.**
   - skills_b had put the same grabbed target's Tiger Pounce splash 1 m ahead.
   - One target needs one spot, so skills_b's Verification 3 moves that splash to d 10.
   - Nothing here changes.

4. **Missed by both clip reports: Wind & Cloud and Rain & Storm**, BB skills whose clips (`wind&cloud`, `rain&storm`)
   the data build drops because of the `&`.
   - They sort into skills_b's half. Their timelines, cue entries and the three parts (the data filter, the icon
     pattern, and SEQ_ALT if needed) are in skills_b.md's Verification 1.
   - Nothing in this report's scope is otherwise missing: every Panda RPC is accounted for in effect_only.md's table,
     and statuses with a look are cued (ashura, drunken, delayQi; `hide` is Raijin Ken's, skills_b Verification 2).

No other correction: the paste-ready block above stands as written.
