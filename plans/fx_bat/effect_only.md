# Bat effects: the skills with no body animation (research, 2026-11-13)

Read-only research for the Bat's effect-only tiles (plans/fx_recipe.md steps 1-3; the Sheep's Quick Heal is the
template: SEQ "<Name>: root@1" + SEQ_SKILL + cue key "@<Name>:root" + `wardrobe_skill_icons.py` EFFECT_ONLY). Sources:
`D:\12tails\DecompiledSource\Bat.cs` (BB, every line cited as `:n`), `Bat_illusion.cs`, `CharacterControl.cs`,
`Math.cs`; TTO pseudo-C `DecompiledSource_TTO_2026-11-02\pseudo\Bat.c`; the Bible's `bat-skill-reference.md` and
skill cards. Probes and their outputs: `checks/fx_bat_research/effect_only/` (git-ignored): `probe1.json`,
`probe2.json` (wardrobe_fx.py --probe), `mats.txt` (materials and blends), `shader_ids.txt` (built-in shader ids),
`illusion_field.txt` (the clone prefab's dust field), `cues.json` (the four cue entries below, parsed as JSON),
`icons.png` (the Bible icons). Their small scripts sit beside them (`mats_probe.py`, `shader_ids.py`,
`illusion_field.py`: they import wardrobe_fx.py and only read).

## Read this first

1. **Four Bat skills play no body clip:** Mass Cast, Shadow Gaze, Switch, Shadow Sacrifice. Each is a plain `void`
   RPC with no wait, called straight from the key press. No `PlayAnimation` runs, either in the RPC or in the dispatcher
   (`clip_calls.js` finds no clip for them). Every cue is at 0 s, and each gets an idle-stance tile.
2. **One part is missing: Unity 3.5's `Particles/Multiply` (built-in shader 205).** `shadowSacrifice_ring`'s dark lines
   (`ShadowLine1`, `ShadowRay`) use it. `wardrobe_fx.py`'s `BUILTIN_BLEND` has no 205, so today they would be drawn
   **additive**: bright streaks where the game draws dark shadow lines. The inventory calls the effect "ready" because it
   doesn't check shaders. It needs building (spec in "Parts needed" below). The other effects are all buildable today.
3. **Switch and Shadow Sacrifice act on the Shadow Illusion clones**, and the page has none. Their effects on the clones
   go to the clones' summon spots (two clones at the top rank, 1.5 m left / right and 2.6 m ahead, on the ground). No
   clone bodies are drawn. This follows the "target point" convention. Open question 1 gives the simpler option.
4. **A BB bug, kept by TTO: Shadow Sacrifice is silent on half its plays.** Its first voice branch loads
   `shadowSacrifice1` into the wrong field (Shame's) and plays a field that nothing fills. The cue is therefore
   `shadowSacrifice2` at p 0.5 (open question 2), and the bug is offered for the Bible.
5. Mass Cast's 9 s status tints the Bat purple (`setColor`). It is left out, as the Penguin's multiCast tint was
   (plans/fx_penguin/decisions.md 10). See open question 3.

## Every RPC_* in Bat.cs (89), accounted for

Listed with `grep -oE '(void|IEnumerator) RPC_\w+' Bat.cs` (89 methods). `clip_calls.js` gives the clips each one plays.
The ActionEvent names in the receive switch (`ActionName == "RPC_..."`, `:1800-3600`) add no method: `RPC_blind1/2` and
the rest are the cast-pool skills, which go through `RPC_cast1`.

**Effect-only (this report): 4.** `RPC_massCast` (:11124), `RPC_shadowGaze` (:11281), `RPC_switch` (:13272),
`RPC_shadowSacrifice` (:14100).

**Their clips are covered by other reports, phases included: 61.**
- nAttack1-3: `RPC_nAttack1/2/3`, phases `RPC_nAttack_fire1`, `RPC_nAttack_fire2`, `RPC_nAttack_hit`.
- cAttack1 / cAttack2 (Drain Life): `RPC_cAttack1`. Phases: `RPC_cAttack0` (the release), `RPC_cAttack_hit`, and
  `RPC_dreamBurst_hit` (:13952). Dream Burst is a passive proc in the drain loop (ActionEvent :22130). Its
  `dreamBurst_hit` sits on the drained target, `collider.bounds.center - 0.4 hitDir` (:14001), with `Sounds/dreamBurst_hit`
  (:14021-14033). It belongs in the Drain Life entry.
- cast1 / cast2 (the cast channel): `RPC_cast1`, plus `RPC_cast0`, the cancel when the target is lost (:11007-11033: standby only, no
  effect).
- cast3 (the cast pool): `RPC_phantomBane_cast`, `RPC_dissolute_cast`, `RPC_corruption_cast`, `RPC_curse_cast`,
  `RPC_doom_cast`, `RPC_mirageOrb_cast` (+ `_fire`, `_destroy`), `RPC_shadowIllusion_cast` (+ `RPC_shadowIllusion_create`),
  `RPC_blind_cast`, `RPC_confusion_cast`, `RPC_hateTransfer_cast`, `RPC_swap_cast` (+ `RPC_swap_hit`),
  `RPC_dreamDazzle_cast` (+ `_hit`), `RPC_phantasmBlast_cast` (+ `_hit`), `RPC_charm_cast` (+ `RPC_charm_hit`),
  `RPC_mimic_cast` (+ `RPC_mimic_create`), `RPC_shame_cast`, `RPC_darkStalker_cast`, `RPC_paranoia_cast` (+ `_hit`),
  `RPC_shatteringDream_cast` (+ `_hit`).
- channel + cast3: `RPC_nightmare_cast` (+ `RPC_nightmare0`, the channel's end: it removes the status and stops the clones'
  channel, :12060-12200, no effect) and `RPC_mindControl_cast` (+ `RPC_mindControl0`, the same, :13802-13950).
- echoes: `RPC_echoes` (+ `_fire`, `_hit`). soulEater: `RPC_soulEater` (+ `_hit`).
- bigCast1-3: `RPC_guardianOfTheNight` and `RPC_guardianOfTheNight_cast`, plus the summoned guardian's own AI moves
  `RPC_guardian_attack`, `RPC_guardian_cast`, `RPC_guardian_unsummon` (each starts a coroutine on
  `Bat_guardianOfTheNight`, :12455-12600) and `RPC_guardian_hit` (Elementals/Shade4's `nAttack_hit` at the hit,
  :12619-12629). Also `RPC_nefariousWhip` / `_cast` (+ `_hit`), and `RPC_blackServant` / `_cast`.

**Shared by every class (item / pet / mount / coin / emote / KO): 24.** These are the 12 support skills
`RPC_obsidianFang` (+ `_hit`), `stunningGround`, `psalmOfEnergy`, `seaAegis`, `assassinate`, `zephyrLore`,
`mineWalker`, `replenishment`, `elementalBound`, `divineChannel`, `astralShift` and `bloodCarnage`. They are found in
Wolf, Sheep, Penguin, Bison and Cat too, and the Bible's "Support-skill exclusion" (`SkillData.getSupportSkill`) covers
them. Also: `RPC_emotion`, `RPC_emotion0`, `RPC_useItem`, `RPC_useMount`, `RPC_useCoin`, `RPC_petEffect`,
`RPC_activateIcon1/2`, `RPC_ko`, `RPC_dead`, `RPC_revive`.

4 + 61 + 24 = 89. **TTO:** Crimson Verdict and Evil Twin go through `Bat.<RPC_row6Cast>` (strings `cast1`, `cast2`,
PlayAnimation). Nightfall Swarm has its `nightfallSwarm` clip. None is effect-only; the TTO report covers them. (ToT's C6
skills are not in BB's Bat.cs and never go online.)

---

## Mass Cast (`massCast`, Bible "Mass Cast", icon `bat_massCast2`)

**RPC:** `RPC_massCast(mPos, tDir, tID, sLv)` (:11124-11270). Local call :9735 (the key press), ActionEvent
`RPC_massCast<sLv>` :9744; remote :4356 / :4374. Max rank 2.

| t | what | where | lines |
|---|---|---|---|
| 0 | cooldown agiAdjust(180) | | :11131 |
| 0 | `Effects/massCast` | the hero's position and rotation (createEffect), distance 0 | :11140, :11152 |
| 0 | status massCast sLv 2, chaAdjust(3 + 3 x 2) = 9 s (isMine) | | :11164 |
| 0 | voice massCast1 / massCast2, Random.Range(0, 2) | own team | :11199, :11209, :11240, :11265, :11269 |

- **The effect** (probe1.json): EffectControl life 1, afterLife 0, followPosition, no followState. RingEmitter
  (`Line_Multilines2`, 202 addsoft) and LineEmitter (`IceRay`, 202). Its AudioSource plays `Sounds/massCast`. Every part
  is built: **ready**.
- **The status's look:** `$addStatus` sets `mColor (0.48, 0.29, 0.78)` and `setColor` for the status
  (CharacterControl.cs:40037-40045), and `removeStatus` puts it back to 0.86 grey (:18064-18070): a purple body tint for 9 s.
  It is left out (open question 3).
- No followState cut, no random effect, no passive that adds an effect to Mass Cast itself. Auto Mass #431 rolls in the
  cast channel instead (below, "Notes for the other reports").

## Shadow Gaze (`shadowGaze`, Bible "Shadow Gaze", icon `bat_shadowGaze4`)

**RPC:** `RPC_shadowGaze(mPos, tDir, tID, sLv)` (:11281-11780). Local call :9655, ActionEvent :9668; remote
:4770-4824. Max rank 4. The Bible says "target, enemy; instant".

| t | what | where | lines |
|---|---|---|---|
| 0 | cooldown agiAdjust(20) with Demon Gaze #412 (else 30) | | :11319-11333 |
| 0 | voice shadowGaze1 / shadowGaze2, Random.Range(0, 2) | own team | :11368, :11380, :11411, :11392, :11423 |
| 0 | targets: the target alone without massCast; with it, up to 6 in FindAreaTarget(target, 18, 12) | | :11447-11513 |
| 0 | Demon Gaze #412 on: banner "Demon Gaze", `Effects/demonGaze_hit` at each target's `collider.bounds.center`, `Quaternion.identity` (caster's client only, isMine :11519) | target | :11525-11554 |
| 0 | (without #412: `Effects/shadowGaze_hit` the same way) | | :11576-11594 |
| 0 | hit talAdjust(12 + 12 x 4 + 12) | | :11614 |
| 0 | `Sounds/demonGaze_hit` (without #412 `shadowGaze_hit`) by playAudioAtPoint at the hit target nearest the camera | target | :11630-11646, :11663-11687, :11710-11722 |
| 0 | camera colour ramp `shadowRamp` 10 s, only on the local player's screen when it is hit | | :11737-11761 |

- **Passives on, max rank:** Demon Gaze #412 → `demonGaze_hit` + `Sounds/demonGaze_hit`. `demonGaze_hit` and
  `shadowGaze_hit` are node-for-node the same prefab (probe1.json). Mass Cast is not up on a fresh tile, so there is one
  target.
- **Where:** an enemy goes to the 10 m target point, at its body centre 0.6 m up (Penguin decision 3: collider centre).
  The rotation is world identity, drawn in the hero's facing (APPROXIMATED, as the Sheep's divinityAxe and the Penguin's
  absoluteZero).
- **The effect:** EffectControl life 2, no follow. Two RingEmitters (`nAttack2`, 203 alpha), a LineEmitter (`Ray0`, 202)
  and an EmblemEmitter: **ready**. It has no AudioSource, so the sound is a `"sound"` cue (`--sounds demonGaze_hit`).
- Left out: the "Demon Gaze" text banner (UI) and the camera ramp, which only shows on a hit local player's screen.
- BB oddity (no visible effect): the remote copy of `RPC_shadowGaze4` runs with sLv **3** (:4815-4824). Only the caster's
  client draws the effect and deals the hit (isMine), so the difference never shows.

## Switch (`switch`, Bible "Switch", icon `bat_switch1`)

**RPC:** `RPC_switch(mPos, tDir, tID)` (:13272-13526). Dispatcher `bat_switch1` :7870-7951. It is refused with
"No Illusion to switch place with" (and the cost is refunded) when no clone is out (:7876-7893). Rank 1.

| t | what | where | lines |
|---|---|---|---|
| press | the clone: right one (`omdviAIVKF`) when `Random.Range(0, 2) == 0` or only it exists, else the left (`INmv81bBeH`) | | :7901-7958 |
| 0 | cooldown agiAdjust(12) | | :13279 |
| 0 | the Bat goes to the clone's spot, the clone to the Bat's old spot | | :13300-13309 |
| 0 | locks up to Lv 4 (5 with Paranoia #433) cleared, target released (Bat and both clones); nothing drawn | | :13312-13356 |
| 0 | `Effects/switch_hit` at the Bat (new spot, its rotation), at clone 1 and at clone 2 (their rotation) | Bat + clones | :13368, :13380, :13391, :13403 |
| 0 | voice switch1 / switch2, Random.Range(0, 2) | own team | :13447, :13457, :13488, :13525, :13522 |

- **The clones' spots:** Shadow Illusion at its top rank (4) makes two clones. Clone 1 (`INmv81bBeH`, created with sLv 3
  < 4, :13121-13125) is at `getSpawnVector(pos + up, TransformDirection(-1.5, -1, 2.6))`. Clone 2 (`omdviAIVKF`, :13134)
  is at `(+1.5, -1, 2.6)` (:31511-31559). `Math.getSpawnVector` (Math.cs:1210) casts a 4 m ray down that line and snaps
  to the ground, so on flat ground the clones stand 1.5 m left / right and 2.6 m ahead. In the game they then follow the
  Bat and drift; the summon spots are the stable reading.
- **The page:** the hero can't move, so the cues give the game's picture after the swap, seen from the Bat.
  - If the left clone was swapped (roll `switchLeft`, 0.5): it now stands where the Bat stood, `x +1.5, d -2.6`, and the
    right clone is at `x +3, d 0`.
  - If the right clone was swapped: the mirror, `x -1.5, d -2.6` and `x -3`.
  - Either way, one `switch_hit` at the hero.
- **The effect:** EffectControl life 1, no follow. ImageEmitters (`star8` 200 add, `Ring1` 202) 1.2 m up in the prefab.
  Its AudioSource plays `Sounds/swap` at 0.5 volume, three times as in the game (three instances): **ready**.

## Shadow Sacrifice (`shadowSacrifice`, Bible "Shadow Sacrifice", icon `bat_shadowSacrifice5`)

The highest-rank key; the Bible card names `bat_shadowSacrifice1`, which is the same picture: `checks/.../icons.png`.

**RPC:** `RPC_shadowSacrifice(mPos, tDir, tID)` (:14100-14350). Local call :8195, ActionEvent :8208; remote :6773. It
is refused with "Required shadow illusion" (and the cost is refunded) when no clone is out (:8164-8187). Rank 1 (#413).

| t | what | where | lines |
|---|---|---|---|
| 0 | cooldown agiAdjust(120) | | :14110 |
| 0 | voice: Random.Range(0, 2); branch 2 plays shadowSacrifice2; branch 1 plays nothing (bug, below) | own team | :14142-14201 |
| 0 | each clone: 20 % of its HP added up, then `Bat_illusion.RPC_disappear` → `illusion_dust` at the clone + 1 m up, `Quaternion.identity` | clones | :14213-14288; Bat_illusion.cs:2829-2836 |
| 0 | `Effects/shadowSacrifice_ring` at the hero's position and rotation (createEffect), distance 0 | hero | :14301, :14313 |
| 0 | RPC_AddHeal(413, total) when the total is above 0, nothing drawn | | :14327-14339 |

- **The voice bug** (BB and TTO): branch 1 tests `BJyldV2eoL`. Nothing ever assigns that field (declared :19899, used
  only at :14148-14166). The branch loads `shadowSacrifice1` into `vsHla13joN` (:14154), the field Shame keeps `shame1` in
  (:39894-39980), and then plays the empty field: "Cannot find shadowSacrifice1 voice" (:14170), no sound. TTO1102
  `Bat::RPC_shadowSacrifice@0x1acc0e0` is the same: it tests `audioClip_59` (0x550), loads into `audioClip_61` (0x560),
  which is Shame's shame1 slot (`Bat.<RPC_shame_cast>d__210` reads 0x560 for shame1), and plays 0x550. Side effect in both
  games: after a Shadow Sacrifice that took branch 1, Shame's shame1 branch says `shadowSacrifice1`. So in the game
  Shadow Sacrifice voices `shadowSacrifice2` on half the plays and is silent on the other half.
- **The dust:** `illusion_dust` is the clone prefab's `Bat_illusion` field. The rip loses the field names, but the
  BB data's raw bytes resolve it: the PPtr at byte 96 of the `Bat_illusion` MonoBehaviour on `Effects/illusion` is
  `Effects/illusion_dust` (illusion_field.txt; byte 40 is `illusion_fire`). It is a loaded prefab, not a
  `Resources.Load`, which is why `plans/fx_inventory.md` doesn't list it. Probe (probe2.json): EffectControl life 1, a
  LineEmitter (`Ray3`, 202) and a legacy Ellipsoid particle system (`Smoke4`, 206 multiply2). Its AudioSource plays
  `Sounds/illusionSmoke`. **Ready.** It goes at the two clones' spots (`x -+1.5, d 2.6`) 1 m up.
- **The ring:** EffectControl life 1 + afterLife 1, followPosition. RingEmitters (`ShadowLine1`, `Dust5`) and a
  VortexEmitter (`ShadowRay`). `ShadowLine1` and `ShadowRay` use built-in shader **205**, which has no blend in
  `BUILTIN_BLEND` (shader_ids.txt), so they fall back to "add". **Needs the Particles/Multiply part** (below); the rest
  is ready.

---

## Parts needed

**Particles/Multiply (built-in 205), for `shadowSacrifice_ring` (materials `ShadowLine1`, `ShadowRay`).**
- `wardrobe_fx.py`: `BUILTIN_BLEND[205] = "multiply"`. plans/fx_penguin/parts.md "Read this first" 4 already
  identified 205 as Multiply: its 24 rip materials, `BlackTrail`, `ShadowLine1-4`, `ShadowRay_0` ..., are dark on white.
  parts.md line 119 asked for this line "if a later class needs it". The Bat does.
- `index.html` `fxMaterial`: a `"multiply"` branch beside `"multiply2"`. Unity 3.5's built-in `Particles/Multiply` is:
  - `Blend Zero SrcColor`, `Cull Off`, `Lighting Off`, `ZWrite Off`, no `_TintColor`;
  - texture stage 1 `combine texture * primary`;
  - stage 2 `constantColor (1,1,1,1) combine previous lerp(previous) constant`.

  So colour = lerp(white, texture x vertex colour, that alpha), and the result = what is drawn x colour (only ever
  darkens). This is the 206 branch with lerp toward 1.0 instead of 0.5 and `blendSrc ZeroFactor, blendDst SrcColorFactor`.
  For the empty canvas, use 206's trick (alpha = 1 - luminance of the colour) so the darkening still shows over the
  stage's CSS backdrop.
- How sure: medium-high on the shader (Unity's standard built-in source; the id is 205 by the alphabetical rule
  plans/fx_penguin/parts.md confirms). Check with a screenshot of Shadow Sacrifice after the build: dark rising lines.
- The parts report should grep every other cued Bat effect for 205 materials (Shadow*, BlackTrail, Dust10/11 ...), so
  one builder covers them all.

No other part is missing for these four skills. The parts in play are EffectControl, RingEmitter, LineEmitter,
ImageEmitter, EmblemEmitter, VortexEmitter, legacy particles and AudioSource; every one is in
`wardrobe_fx_inventory.py`'s BUILT.

## Paste-ready page lines

`wardrobe/index.html` SEQ: append to `bat:`, after "Guardian of the Night: bigCast1 bigCast2*@0 bigCast3~":
```js
    // skills the game plays with no animation (plans/fx_bat/effect_only.md: RPC_massCast Bat.cs:11124, RPC_shadowGaze
    // :11281, RPC_switch :13272, RPC_shadowSacrifice :14100 call no PlayAnimation): their effects on the idle stance
    "Mass Cast: root@1", "Shadow Gaze: root@1", "Switch: root@1", "Shadow Sacrifice: root@1"],
```
`SEQ_SKILL`, a new class key:
```js
  bat: { "@MassCast": "massCast", "@ShadowGaze": "shadowGaze", "@Switch": "switch", "@ShadowSacrifice": "shadowSacrifice" },
```
`pipeline/wardrobe_skill_icons.py` EFFECT_ONLY:
```python
EFFECT_ONLY = {"sheep": ["quickHeal"], "penguin": ["manaArc", "dispell", "doubleCast", "tripleCast"],
               "bat": ["massCast", "shadowGaze", "switch", "shadowSacrifice"]}
```
(`bat_massCast2`, `bat_shadowGaze4`, `bat_switch1`, `bat_shadowSacrifice5` exist in the Bible's assets.js; the script takes
each skill's highest rank. Run `py -3 pipeline\wardrobe_skill_icons.py` after the edit.)

What the build needs (the cue file names them; with `--fx` by hand):
`--fx massCast,demonGaze_hit,switch_hit,illusion_dust,shadowSacrifice_ring --voices massCast1,massCast2,shadowGaze1,shadowGaze2,switch1,switch2,shadowSacrifice2 --sounds demonGaze_hit`
(all present in the rip: voices/*.wav, sounds/demonGaze_hit.wav).

## Paste-ready cues (wardrobe/fx_cues/bat.json)

Also saved as `checks/fx_bat_research/effect_only/cues.json`, which parses as JSON. Key shape `"@<SEQ name without
spaces>:root"`, as the Sheep's `"@QuickHeal:root"`.

```json
  "@MassCast:root": {
    "why": "Bat.cs RPC_massCast (:11124-11270, a plain method: no clip, no wait; the dispatcher calls it straight from the key press, :9735, and no PlayAnimation runs: the tile plays it on the idle stance), all at 0: addTimeOut agiAdjust(180) (:11131); Effects/massCast (:11140) at the hero's position and rotation (createEffect :11152; EffectControl life 1, followPosition; plays its own Sounds/massCast); the massCast status at the top rank, sLv 2 for chaAdjust(3 + 3 x 2) = 9 s (:11164), its purple body tint (setColor (0.48, 0.29, 0.78), CharacterControl.cs $addStatus :40037-40045; back to grey 0.86 in removeStatus :18064-18070) left out as the Penguin's multiCast tint (plans/fx_penguin/decisions.md 10); voice massCast1 / massCast2 (Random.Range(0, 2) :11199; :11209 / :11240, PlayOneShot :11265 / :11269; played for the caster's own team)",
    "cues": [
    [0, "fx", "massCast"],
    [0, "voice", "massCast1|massCast2"]
    ]
  },
  "@ShadowGaze:root": {
    "why": "Bat.cs RPC_shadowGaze (:11281-11780, a plain method: no clip, no wait; the dispatcher calls it straight from the key press, :9655, and no PlayAnimation runs: the tile plays it on the idle stance), all at 0: cooldown agiAdjust(20) with Demon Gaze #412 (:11319-11325); voice shadowGaze1 / shadowGaze2 (Random.Range(0, 2) :11368; :11380 / :11411, PlayOneShot :11392 / :11423); no massCast up, so the target alone (getStatusLv(massCast) :11447; with it, up to 6 in FindAreaTarget(target, 18, 12) :11468, :11513); Demon Gaze #412 on (passives on, hasSkill(412) :11525): Effects/demonGaze_hit (:11542; without it shadowGaze_hit, :11582, the same look) Instantiated at the target's collider.bounds.center with Quaternion.identity (:11554; drawn in the hero's facing, APPROXIMATED), on the caster's own client only (isMine :11519): an enemy, so the 10 m target point, 0.6 m up at its body centre (plans/fx_penguin/decisions.md 3); the hit talAdjust(12 + 12 x 4 + 12) (:11614) draws nothing; Sounds/demonGaze_hit (:11663-11675; without #412 shadowGaze_hit, :11710) by playAudioAtPoint at the hit target nearest the camera (:11630-11646, :11687); the 'Demon Gaze' banner (:11531) and the shadowRamp camera tint on a hit local player (:11737-11761) left out",
    "cues": [
    [0, "voice", "shadowGaze1|shadowGaze2"],
    [0, "fx", "demonGaze_hit", {"d": 10, "y": 0.6}],
    [0, "sound", "demonGaze_hit"]
    ]
  },
  "@Switch:root": {
    "why": "Bat.cs RPC_switch (:13272-13526, a plain method: no clip, no wait; the dispatcher calls it straight from the key press, :7870-7951, refused with 'No Illusion to switch place with' when no clone is out, :7876-7888; the tile plays it on the idle stance), all at 0: addTimeOut agiAdjust(12) (:13279); the Bat and the chosen clone trade places (:13300-13309), lock statuses up to Lv 5 with Paranoia #433 cleared and targets released on the Bat and both clones (:13312-13356), drawing nothing; Effects/switch_hit (:13368; plays its own Sounds/swap) at the Bat's new spot with its rotation (:13380) and at each clone with the clone's (:13391, :13403); the clones: two at Shadow Illusion's top rank, summoned on the ground 1.5 m left and right, 2.6 m ahead (TransformDirection(-+1.5, -1, 2.6) from 1 m up, Math.getSpawnVector Math.cs:1210; Bat.cs:31511-31559), the left one INmv81bBeH, the right one omdviAIVKF (RPC_shadowIllusion_create :13121-13134); the clone swapped is picked as the game picks it, Random.Range(0, 2) == 0 the right one, else the left (:7901-7958): roll switchLeft (0.5) = the left clone swapped, which now stands where the Bat stood, 1.5 m right and 2.6 m behind the Bat, and the right clone 3 m to its right; else the mirror; the page's hero stays put, so these are the game's spots after the swap seen from the Bat; no clone bodies are drawn; voice switch1 / switch2 (Random.Range(0, 2) :13447; :13457 / :13488, PlayOneShot :13525 / :13522)",
    "cues": [
    [0, "fx", "switch_hit"],
    [0, "fx", "switch_hit", {"x": 1.5, "d": -2.6, "p": 0.5, "roll": "switchLeft"}],
    [0, "fx", "switch_hit", {"x": 3, "p": 0.5, "roll": "switchLeft"}],
    [0, "fx", "switch_hit", {"x": -1.5, "d": -2.6, "p": 0.5, "roll": "!switchLeft"}],
    [0, "fx", "switch_hit", {"x": -3, "p": 0.5, "roll": "!switchLeft"}],
    [0, "voice", "switch1|switch2"]
    ]
  },
  "@ShadowSacrifice:root": {
    "why": "Bat.cs RPC_shadowSacrifice (:14100-14350, a plain method: no clip, no wait; the dispatcher calls it straight from the key press, :8164-8195, refused with 'Required shadow illusion' when no clone is out, :8170-8182; the tile plays it on the idle stance), all at 0: addTimeOut agiAdjust(120) (:14110); voice Random.Range(0, 2) (:14142): one branch loads and plays shadowSacrifice2 (:14185, :14197); the other loads shadowSacrifice1 into Shame's shame1 field (vsHla13joN, :14154; Shame :39894-39980) and plays a field nothing ever fills (BJyldV2eoL, :14148-14166, declared :19899): no voice, 'Cannot find shadowSacrifice1 voice' (:14170); TTO the same (TTO1102 Bat::RPC_shadowSacrifice@0x1acc0e0 tests audioClip_59, loads audioClip_61): so shadowSacrifice2 on half the plays, as the game; each clone (two at Shadow Illusion's top rank, 1.5 m left and right, 2.6 m ahead, :31511-31559) gives 20 % of its HP (:14230, :14271) and vanishes: Bat_illusion.RPC_disappear (:14247, :14288; Bat_illusion.cs:2829-2836) Instantiates its illusion_dust field (Effects/illusion_dust, the illusion prefab's Bat_illusion field at byte 96: checks/fx_bat_research/effect_only/illusion_field.txt; plays its own Sounds/illusionSmoke) 1 m above the clone, Quaternion.identity (drawn in the hero's facing, APPROXIMATED); no clone bodies are drawn; then Effects/shadowSacrifice_ring (:14301) at the hero's position and rotation (createEffect :14313; EffectControl life 1 + afterLife 1, followPosition); the heal RPC_AddHeal(413) (:14339) draws nothing more",
    "cues": [
    [0, "voice", "shadowSacrifice2", {"p": 0.5}],
    [0, "fx", "illusion_dust", {"x": -1.5, "d": 2.6, "y": 1}],
    [0, "fx", "illusion_dust", {"x": 1.5, "d": 2.6, "y": 1}],
    [0, "fx", "shadowSacrifice_ring"]
    ]
  }
```

The page's rules these cues lean on (index.html cueOf / fxStart): a `"!name"` roll plays when that roll failed, so it
needs its own `p`. Rolled cues (`p`) aren't expected by `wardrobe_fx_check.py` (:226, :238); `switch_hit` at the hero,
`massCast`, `demonGaze_hit`, `illusion_dust` and `shadowSacrifice_ring` are, and each must spawn.

## Notes for the other reports (seen on the way)

- **Auto Mass #431 draws `massCast` too:** in `RPC_cast1`, with no massCast up, `Random.Range(0, 100) < lckAdjust(12)`
  (:23253-23259) runs `createEffect(dYR2KulycG, hero)` (:23354) and massCast Lv 1 for 3 s (:23360). That prefab field is
  loaded only by `RPC_massCast` (:11140), so BB shows the proc's effect only after Mass Cast has been cast once, as the
  Penguin's multiCast. That is for the cast-pool report's rolls (the Penguin cued it in the roll). TTO's
  `Bat::Row6Release` loads `effects/massCast` itself.
- **Dream Burst** (passive on Drain Life): `dreamBurst_hit` on the drained target (:13989-14001), `Sounds/dreamBurst_hit`
  (:14021-14033), every 9 - 3 = 6 s at Dream Burst 3 (the Bible). The clones burst too (`Bat_illusion.cs:2399`). This is
  for the Drain Life entry.
- **Shame's voice** in the game becomes `shadowSacrifice1` after a branch-1 Shadow Sacrifice (above). The tiles play
  independently, so Shame keeps `shame1|shame2`.

## Offer for the Bible (the user's call; never written there from here)

1. Shadow Sacrifice's first voice is never heard. It is loaded into Shame's field (BB :14148-14166, TTO
   `RPC_shadowSacrifice@0x1acc0e0`), so Shame's first voice then says `shadowSacrifice1`. BB and TTO both.
2. The remote copy of Shadow Gaze rank 4 runs as rank 3 (BB :4815-4824). It has no visible effect, because the effect
   and hit are drawn on the caster's client only.
3. Mass Cast's status tints the Bat purple, `(0.48, 0.29, 0.78)` (CharacterControl.cs:40037-40045).
4. Auto Mass's flash only shows after Mass Cast has been cast once that session (BB :23354, field loaded at :11140).

## Open questions

1. **Switch and Shadow Sacrifice: show the clones' effects at their summon spots, without clones?**
   - Recommended: **yes**, as the cues above. It is the game's three `switch_hit`s / two dusts, at the spots
     Shadow Illusion's top rank gives (1.5 m left / right, 2.6 m ahead). For Switch they are seen from the Bat after the
     swap, with the swapped clone picked 50/50 as the game picks it. This matches the "target point" convention, where an
     enemy's effect plays at an empty spot.
   - Simpler alternative: only the hero's own effect (`switch_hit` / `shadowSacrifice_ring` at 0) plus the voice. Then
     drop the four rolled `switch_hit` lines and the two `illusion_dust` lines.
   - If the Shadow Illusion report proposes a clone part (a copy of the hero), these two tiles could summon it first. I
     would not do that: each tile starts fresh, and a clone that pops in only to vanish reads worse than the dust alone.
2. **Shadow Sacrifice's voice: the game's (shadowSacrifice2 on half the plays, else silent) or the intended
   `shadowSacrifice1|shadowSacrifice2`?**
   - Recommended: **the game's**, `[0, "voice", "shadowSacrifice2", {"p": 0.5}]`. Sheep decision 10 took TTO's fix only
     where TTO fixed a BB bug; here TTO keeps it, and the rule is "random picks as the game does them".
   - If the user prefers the intended voice: `[0, "voice", "shadowSacrifice1|shadowSacrifice2"]` and add
     `shadowSacrifice1` to the build's voices.
3. **Mass Cast's purple body tint for 9 s: leave out?**
   - Recommended: **leave out**, as the Penguin's multiCast tint (decision 10). The tile already shows the cast flash and
     the voice. A tint would need a new hero-look cue kind (a colour on every hero material, `setColor`), and the Penguin
     declined one.
   - If wanted, it would be a `"skin"`-like cue with `kill: 9`, a part of its own.
4. **Shadow Gaze: the effect at the target's body centre, 0.6 m up, or on the ground?**
   - Recommended: **0.6 m up** (`{"d": 10, "y": 0.6}`). The game spawns it at `collider.bounds.center`, and Penguin
     decision 3 makes that 0.6 m for every class.
5. **Shadow Gaze's sound: cue `Sounds/demonGaze_hit` as a `"sound"`?**
   - Recommended: **yes**. The hero's code plays it (playAudioAtPoint at the target), not the effect: the
     `demonGaze_hit` prefab has no AudioSource. The page's sounds aren't positional, so it plays at full level.
6. **Tile length `root@1`?**
   - Recommended: **yes**, as Quick Heal. Every cue is at 0, and the longest effect, `demonGaze_hit` (2 s), runs on over
     the idle tail.
7. **The Particles/Multiply part: build it now for Shadow Sacrifice (and any other 205 material the Bat cues)?**
   - Recommended: **yes** (the user's "missing parts are always built"). Without it the ring's shadow lines come out as
     bright additive streaks.

## Verification

Read-only check (2026-11-13, home PC). I re-read the claims against `D:\12tails\DecompiledSource\Bat.cs`,
`Bat_illusion.cs`, `CharacterControl.cs`, `Math.cs`, the TTO pseudo-C (`pseudo/Bat.c`), the Bible
(`bat-skill-reference.md`, `assets.js` icon keys), the rip's WAVs (durations measured), the page (`wardrobe/index.html`
cueOf / fxStart / fxDue / chains / poolChains / SEQ_SKILL), `pipeline/wardrobe_skill_icons.py` and
`pipeline/wardrobe_fx_check.py`. I worked the opaque predicates by hand. My probes and outputs:
`checks/fx_bat_research/verify_b/` (`probe_eo.json` = `wardrobe_fx.py bat --probe massCast,demonGaze_hit,shadowGaze_hit,
switch_hit,illusion_dust,shadowSacrifice_ring`, exit 0; `shader_ids_b.txt`, `mats_b.txt`; `summ.py` summarises a probe).

### What holds
- **The RPC_* listing.** My own `grep -oE '(void|IEnumerator) RPC_\w+' Bat.cs` gives 89 distinct methods (:10725-:19382).
  The report's groups are complete and disjoint: 4 effect-only + 61 with clips or phases (re-counted: 6 + 4 + 2 + 29 +
  4 + 5 + 6 + 3 + 2) + 24 shared (13 support incl. obsidianFang_hit, 11 item / mount / coin / pet / emote / KO).
  `node pipeline/clip_calls.js D:/12tails/DecompiledSource wardrobe/data bat` lists 35 Bat.cs methods that play a skill
  clip; massCast, shadowGaze, switch and shadowSacrifice are not among them. The only Bat.cs effect loads outside an
  RPC or its coroutine are createNightmareRing / createMindControlRing (Nightmare / Mind Control) and the pets' `mini*`
  effects, so no other clip-less Bat skill exists (the passive procs Dream Burst, Auto Mass and Chiroptophobia each ride
  a tile that has a clip: Drain Life, the cast pool, Blind / Confusion).
- **Mass Cast:** :11131 agiAdjust(180), :11140 load, :11152 createEffect (hero position + rotation), :11164
  chaAdjust(3 + 3 sLv) = 9 s at sLv 2, :11199 pick, :11209 / :11240 loads, :11265 / :11269 plays; every predicate as
  stated. Probe: EC life 1, followPosition, AudioSource massCast; RingEmitter Line_Multilines2 (202), LineEmitter IceRay
  (202): ready.
- **Shadow Gaze:** :11319-:11333 cooldown, :11368 pick (:11380 / :11392, :11411 / :11423), :11447 getStatusLv(massCast),
  banner :11531, demonGaze_hit :11542 / :11554 at collider.bounds.center + identity (isMine :11519), hit :11614, sounds
  :11675 / :11687 (shadowGaze_hit :11710 / :11722), shadowRamp :11761. The remote rank-4 branch passes 3 (:4824).
  demonGaze_hit = shadowGaze_hit node for node (EC life 2, two RingEmitters nAttack2 203, LineEmitter Ray0 202,
  EmblemEmitter), no AudioSource: the `"sound"` cue is right.
- **Switch:** the dispatcher :7870-:7958 as stated (no left clone: the right one; else Random.Range(0, 2) == 0: the
  right, else the left; a lone left clone with roll 0 throws in BB, the Bible's :630 note). :13279, :13300 / :13303 (the
  trade), :13368 load, :13380 / :13391 / :13403 the three Instantiates with their owners' rotations, :13447 pick,
  switch1 -> PlayOneShot :13525, switch2 -> :13522. Probe: EC life 1, AudioSource swap at 0.5, ImageEmitters star8 (200)
  + Ring1 (202) 1.2 m up: ready. The clone spots: :31511 / :31541 TransformDirection(-+1.5, -1, 2.6) from hero + up;
  Math.getSpawnVector (Math.cs:1210) casts 4 m along that 3.16 m vector and falls back to pos + dir, so on flat ground
  both give (-+1.5, 0, 2.6); getExpandPos (:31516 / :31546, Math.cs:1242) only pushes off colliders. Clone 1 (create
  sLv max(1, 4 - 1) = 3 < 4) = INmv81bBeH, clone 2 (sLv 4 + 2 = 6) = omdviAIVKF (:13121-:13134).
- **Shadow Sacrifice:** :14110; the voice bug exactly as written (branch 1: :14148 tests BJyldV2eoL, declared :19899
  and never assigned; :14154 loads into vsHla13joN, Shame's shame1 field :39894-:39980; :14170 logs; branch 2 :14185 /
  :14197); TTO the same (`Bat::RPC_shadowSacrifice` pseudo/Bat.c:39366 tests 0x550 and stores 0x560; Shame's MoveNext
  :22999 reads 0x560). Clones :14213-:14288 (20 % of HP each, RPC_disappear), Bat_illusion.RPC_disappear
  (Bat_illusion.cs:2827-:2836: illusion_dust at position + up, identity), ring :14301 / :14313, heal :14339. Offset 96
  fits the clone's serialized fields (Bat_illusion.cs:2897-:2945: Weapon at 32, then 8 PPtrs, illusion_dust the 9th
  field, at 96). Probe: illusion_dust EC life 1, Ray3 (202) + Smoke4 (206 multiply2), AudioSource illusionSmoke: ready;
  shadowSacrifice_ring EC life 1 + afterLife 1, followPosition; ShadowLine1 and ShadowRay are built-in 205 and fall back
  to "add" (wardrobe_fx.py:43, :227): the Particles/Multiply part is needed, as the report says.
- Icons: `bat_massCast2`, `bat_shadowGaze4`, `bat_switch1`, `bat_shadowSacrifice5` are the highest-rank keys in
  assets.js. Every voice and sound named is in the rip (massCast1/2, shadowGaze1/2, switch1/2, shadowSacrifice2;
  demonGaze_hit, swap, illusionSmoke, massCast). The cue block parses as JSON (wrapped in braces). Cue keys resolve:
  "Mass Cast: root@1" gets chain id "@MassCast", so fxStart reads "@MassCast:root" (index.html chains / fxStart).

### Corrections
1. **The `EFFECT_ONLY` paste drops the Penguin's Frost Spike.** `pipeline/wardrobe_skill_icons.py:39` already reads
   `"penguin": ["manaArc", "dispell", "doubleCast", "tripleCast", "frostSpike"]`; the report's line omits
   `"frostSpike"`, which would lose that tile's HD icon. Corrected below.
2. **The SEQ paste cannot be appended as written.** index.html:1152 ends `"Guardian of the Night: ... bigCast3~"],`; the
   block must replace that `]` (and skills_b.md changes the same line: Mind Control added, Nightmare `@8.9`). Merged
   block below. Likewise `SEQ_SKILL` gets one `bat:` key with both reports' entries (skills_b.md adds `@Nightmare`,
   `@MindControl`): two `bat:` keys in one object literal keep only the last.
3. **Step lengths: the Penguin's later rule, not Quick Heal's `@1`.** plans/fx_penguin/effect_only.md:162 (the
   effect-only template this run follows): each step = the effect's EffectControl life (+ afterLife), at least the
   longest voice. So Mass Cast `root@1` (life 1; voices 0.86 / 0.89 s), **Shadow Gaze `root@2`** (demonGaze_hit life
   2; voices 0.83 / 0.99 s), Switch `root@1` (switch_hit life 1; voices 0.49 / 1.0 s), **Shadow Sacrifice `root@2`**
   (ring life 1 + afterLife 1; shadowSacrifice2 is 1.07 s). Open question 6's answer changes accordingly.
4. **Switch: the clones' lock clears run on the Bat, not on the clones (BB).** :13323 and :13345 take
   `(CharacterControl)this.GetComponent(...)`, the Bat's own component, before removeLockStatus(4) / releaseTarget()
   (:13329 / :13334, :13351 / :13356); the Bible says the same (bat-skill-reference.md:630, fixed only in Reborn).
   Nothing is drawn either way; the `why` is corrected below.
5. **Switch's spots: the hero-stays frame the other moved-hero cues use, which needs no roll.** The report places the
   cues in the frame after the swap (the hero standing where the Bat lands), so the swapped clone's hit goes 2.6 m
   *behind* the hero. The other cues of this run keep each effect with its owner as the page shows it: Blink's landing at
   the hero (wardrobe/fx_cues/penguin.json `blink`: "the wardrobe hero doesn't travel, as Feral Assault's"), skills_b's
   Swap (one swap_hit at the hero, one at the 10 m target point), and Shadow Sacrifice's dusts / Shadow Illusion's
   clones at the summon spots. In that frame the three switch_hits are at the hero, (-1.5, 2.6) and (+1.5, 2.6)
   whichever clone the game picks (the pick only decides which clone ends where), so the rolls go and all three spawns
   are checked by wardrobe_fx_check.py (it skips cues with `p`, :225-:226, :237-:238). The report's post-swap cues stay
   the alternative for the decisions stage.
6. **More built-in 205 (Particles/Multiply) materials the Bat cues** (the report asked the parts stage to grep them;
   `checks/fx_bat_research/verify_b/shader_ids_b.txt`): shadowSacrifice_ring (ShadowLine1, ShadowRay), paranoia_hit
   (ShadowLine3, ShadowRay), echoes_ring (ShadowRay), echoes_hit (ShadowRay), darkStalker (darkStalker), nightmare_ring
   (nightmare_bolt); plans/fx_bat/parts.md adds nefariousWhip_hit (Smoke4_multiply). One builder
   (`BUILTIN_BLEND[205] = "multiply"` + the page's branch) covers them all. 205 = Multiply stays medium-high (not
   checkable offline), as the report says.
7. Small: Shadow Gaze's FindAreaTarget is at :11468 (the report's :11513 is the loop's end).

### Corrected paste-ready blocks

`wardrobe/index.html` SEQ, the `bat:` entry (lines 1151-1152 become this; skills_b.md's Mind Control and Nightmare
`@8.9` included; merge with any change the other Bat reports make to the first line):
```js
  bat: ["Normal Attack: nAttack1 nAttack2 nAttack3", "Drain Life: cAttack1 cAttack2*", "Cast: cast1 cast2*@0 cast3~",
    "Nightmare: cast1 cast2*@0 cast3~@0.5 channel*~@8.9", "Mind Control: cast1 cast2*@0 cast3~@0.5 channel*~@9.9",
    "Guardian of the Night: bigCast1 bigCast2*@0 bigCast3~",
    // skills the game plays with no animation (plans/fx_bat/effect_only.md: RPC_massCast Bat.cs:11124, RPC_shadowGaze
    // :11281, RPC_switch :13272, RPC_shadowSacrifice :14100 call no PlayAnimation): their effects on the idle stance,
    // each step one effect's life (+ afterLife), at least its longest voice (plans/fx_penguin/effect_only.md)
    "Mass Cast: root@1", "Shadow Gaze: root@2", "Switch: root@1", "Shadow Sacrifice: root@2"],
```
`SEQ_SKILL`, one new class key (both reports):
```js
  bat: { "@Nightmare": "nightmare", "@MindControl": "mindControl", "@MassCast": "massCast", "@ShadowGaze": "shadowGaze",
    "@Switch": "switch", "@ShadowSacrifice": "shadowSacrifice" },
```
`pipeline/wardrobe_skill_icons.py` EFFECT_ONLY (line 39):
```python
EFFECT_ONLY = {"sheep": ["quickHeal"], "penguin": ["manaArc", "dispell", "doubleCast", "tripleCast", "frostSpike"],
               "bat": ["massCast", "shadowGaze", "switch", "shadowSacrifice"]}
```
Cues: `@MassCast:root`, `@ShadowGaze:root` and `@ShadowSacrifice:root` stay as written above. `@Switch:root` becomes:
```json
  "@Switch:root": {
    "why": "Bat.cs RPC_switch (:13272-13526, a plain method: no clip, no wait; the dispatcher calls it straight from the key press, :7870-7951, refused with 'No Illusion to switch place with' when no clone is out, :7876-7888; the tile plays it on the idle stance), all at 0: addTimeOut agiAdjust(12) (:13279); the Bat and the chosen clone trade places (:13300-13309); the Bat's lock statuses up to Lv 5 with Paranoia #433 cleared and its target released (:13312-13315), and a Lv 4 clear and release once more per clone that exists, run on the Bat's own CharacterControl in BB (this.GetComponent :13323, :13345; bat-skill-reference.md:630), drawing nothing; Effects/switch_hit (:13368; EffectControl life 1; plays its own Sounds/swap at 0.5) at the Bat's new spot with its rotation (:13380) and at each clone with the clone's (:13391, :13403); the clones: two at Shadow Illusion's top rank, summoned on the ground 1.5 m left and right, 2.6 m ahead, facing the hero's forward (TransformDirection(-+1.5, -1, 2.6) from 1 m up, Math.getSpawnVector Math.cs:1210; Bat.cs:31511-31559, :12944), the left one INmv81bBeH, the right one omdviAIVKF (RPC_shadowIllusion_create :13121-13134); the clone swapped is the right one when Random.Range(0, 2) == 0, else the left (:7901-7958); the page's hero stays put and each effect stays with its owner as the page shows it (as Blink and Swap): one switch_hit at the hero and one at each clone's summon spot, the same three spots whichever clone the game picks; no clone bodies are drawn; voice switch1 / switch2 (Random.Range(0, 2) :13447; :13457 / :13488, PlayOneShot :13525 / :13522)",
    "cues": [
    [0, "fx", "switch_hit"],
    [0, "fx", "switch_hit", {"x": -1.5, "d": 2.6}],
    [0, "fx", "switch_hit", {"x": 1.5, "d": 2.6}],
    [0, "voice", "switch1|switch2"]
    ]
  },
```
The build line is unchanged. Open questions 1 (correction 5 as the recommended reading), 2, 3, 4, 5 and 7 stand; 6
becomes `root@1` / `@2` / `@1` / `@2` (correction 3).
