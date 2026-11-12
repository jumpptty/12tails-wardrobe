SUMMARY: 9 skills across 14 clips: Quick Fire, Poison Volley, Torment Rain, Right Stride, the 4-member Slayer pool, Skin Shift, Zero Shot, Thunder Dragon, Silent Walk. 14 paste-ready entries with 113 cues.
- Two SEQ fixes the code proves: Quick Fire's first step should be quickFire1@0.6, not 0.4. Slayer should be slayer1@1 slayer2*~@0.1 slayer3~.
- One new tile: Torment Rain: rainOfArrow@2.7. It also needs CLIP_SKILLS chameleon {rainOfArrow: [tormentRain]}, or the tile has no icon.
- One BB bug with a TTO fix: Torment Rain is silent in BB because the voice files are named tormenrRain1/2. TTO loads those names.
- Thunder Dragon has no voice in either game.
- Six parts are needed:
  - hideProp: the Cat's P6. This scope adds "hero" for Thunder Dragon's 3.2 s full hide.
  - The Double Strider ghost mover, cue option strafe. New, and shared with Left Stride.
  - BB ParticleSystem (the Cat's P4).
  - WorldParticleCollider (the Cat's P5).
  - The Self-Illumin/DoubleTexture material.
  - The FX/Invisible hero skin.

=====================================================================

# Chameleon effects + sounds research: Quick Fire, Poison Volley, Torment Rain, Right Stride, Slayer, Skin Shift, Zero Shot, Thunder Dragon, Silent Walk (skills_b)

Researcher `skills_b`, 2026-11-13 (home PC).

**Scope.** The clips `poisonVolley`, `quickFire1-3`, `rainOfArrow`, `rightStride`, `silentWalk`, `skinShift`, `slayer1-3`, `thunderDragon1-2` and `zeroShot`, and every skill that plays them. This is research only (recipe steps 1-3).

**Conventions.**
- Line numbers are `D:\12tails\DecompiledSource\Chameleon.cs` unless another file is named.
- Times are seconds from the start of the clip the entry is keyed by.
- Distance 0 = at the hero.
- Max rank, passives on (the Wolf's / Sheep's / Penguin's / Bat's decisions): Quick Fire 4 + Added Fire #402, Far Reach 4, Poison Volley 2, Right Stride 2 + Double Strider #423, Improved Slayer 4, Silent Walk #411.
- The target is the standing 10 m target point, a Penguin-sized body: CharacterController height 1, radius 0.3, centre 0.6 m up (bounds.center = y 0.6). This is Bat decision 4: one body for every cue.

**Read-only probes and scripts**, all in `checks\fx_chameleon_research\skills_b\`:
- `clean.py` is the Bat's: it prints a .cs range with the opaque predicates worked out. `dump.sh` wraps it.
- `clean_<RPC>.txt` holds every coroutine in scope: quickFire, poisonVolley, tormentRain, tormentRain_fire, rightStride, strideRight, doubleStrideRight, slayer, slayer_fire, skinShift, zeroShot, thunderDragon, cAttack1.
- `flow_RPC_*.txt` is clip_flow.js output. `classes.txt` and `classes_all.txt` list the coroutine classes and their lines.
- `probe.json` + `probe_summary.txt`: `wardrobe_fx.py chameleon --probe` on 24 effects; probe.err is empty. `summarize.py` makes the summary.
- `probe_fields.py` + `probe_fields.txt`: the Chameleon prefab's fields.
  - field 1, footStep_left = sound/fx/step_light2
  - field 2, footStep_right = step_light3
  - field 3, **nAttack_bowFx1 = chameleon/sounds/bow_fire1**
- `probe_events.py` + `probe_events.txt`: the class's AnimationEvents. Only `run` has any (playLeftFootEvent 0.1, playRightFootEvent 0.4). `silentWalk` and every skill clip here have none.
- `stride_sim.py` + `stride_sim.txt`: the Double Strider ghost's path and its five shots.
- `cues.py` -> `cues.json` / `cues_pretty.json`; `fmt.py` -> `cues_block.json` (the block below, checked as JSON).

## Read this first

### 1. Two SEQ steps in index.html are off, and the code is clear

- **Quick Fire:** `quickFire1@0.4` must be **`quickFire1@0.6`**.
  - The opening shot is at 0.4 (case 2) and its ray check at 0.5 (case 3, `Yield(3, 0.1)` :20323).
  - Only then does case 4 play quickFire2 (:19641-19670, `Yield(4, 0.1)` :20313).
  - quickFire2 then runs 0.6 -> 2.3 = 1.7 s: 16 loop shots 0.1 s apart from 0.6, the 16th hit at 2.2, then `Yield(6, 0.1)` :20303. So `quickFire2*@1.7` is right.
  - Both the SEQ comment ("quickFire2 from the opening shot (0.4 s)") and the Bible are 0.2 s early. The Bible says "quickFire2 with the opening shot at 0.4 s ... closing shot at 0.4 + 0.1 x (1 + loop shots)". This is offered for the Bible.
- **Slayer:** `slayer1 slayer2*~@0 slayer3~` must be **`slayer1@1 slayer2*~@0.1 slayer3~`**.
  - slayer2 starts at a fixed 1.0 s (`Time.time >= actionTime + 1` :30367). The slayer1 clip is 1.5 s, so the full clip is too long.
  - The held cast is magAdjust's floor of 0.1 s, not 0 (:30406, CharacterControl.cs:20584-20588; the Bat's Guardian `@0.1`).
  - The eye cue sits at slayer2's 0 and needs the step to last.
- **New: `"Torment Rain: rainOfArrow@2.7"`** (Open question 1). The rain lands at 2.0-2.6 s of a 2.0 s clip. A cue at the clip's very end would be lost to the tile's restart, because fxStart resets FX.t.
- Thunder Dragon's `thunderDragon1@0.8 thunderDragon2*@3` is right: ring2 and the hide at 0.6, thunderDragon2 at 0.8 (:38081), six 0.5 s ticks, standby at 3.8 (:38357).

### 2. Slayer is a pool of four skills over a three-clip sequence

- One coroutine plays all four, and sLv = the skill:
  - Bug Slayer (1)
  - Tail Slayer (2)
  - Elemental Slayer (3)
  - Machine Slayer (4)

  These are #341-344, each with its own cooldown key (:30820).
- Each clip key (`slayer1`, `slayer2`, `slayer3`) gets `skills: {bugSlayer, tailSlayer, elementalSlayer, machineSlayer}`. The voice, the eye and the fire effect differ per member.
- poolChains gives each member its own tile with the Slayer sequence's steps and hides the host. It keeps the pick through the three steps (fxStart: `ch.pick`).
- The member names match the Bible's icons `chameleon_bugSlayer1`, `tailSlayer2`, `elementalSlayer3` and `machineSlayer4`. wardrobe_skill_icons.py picks them up from the cue file, so no OWN_TILE or SEQ_SKILL entry is needed.

### 3. `rainOfArrow` is Torment Rain's clip

- wardrobe_skill_icons.py names a clip's skill after the clip, and there is no `rainOfArrow` skill. So the tile has no icon today: data/icons/hd/index.json has no tormentRain.
- Add `CLIP_SKILLS["chameleon"] = {"rainOfArrow": ["tormentRain"]}` (Bible icon `chameleon_tormentRain1`).

### 4. A BB bug with TTO's fix: Torment Rain is silent in BB

- RPC_tormentRain loads `Voices/tormentRain1` / `tormentRain2` (:25719, :25750).
- The rip has only `voices/tormenrRain1.wav` / `tormenrRain2.wav` (misspelled).
- TTO loads `Voices/tormenrRain1` / `tormenrRain2` (TTO1102 `Chameleon.<RPC_tormentRain>d__170::MoveNext`, pseudo/Chameleon.c:20602-20604).
- Cue: `tormenrRain1|tormenrRain2` (Sheep decision 10). Offered for the Bible.

### 5. Thunder Dragon has no voice

Neither the BB nor the TTO coroutine loads one, and the rip has no thunderDragon voice. Its only sounds are its two rings' AudioSources.

### 6. The page parts this scope needs

No cue can do these. All but two are shared with the Cat's or other reports.

- **P1 `hideProp`** (the Cat's P6, plans/fx_cat/skills_b.md).
  - Every skill here hides the arrow in hand while it shoots, then shows it again at the end unless she is invisible. The arrow is `mChar.mWep2` = the R slot, mount_Hand_R.
  - Cue: `[t, "hideProp", "R", {"kill": s}]`.
  - **New here:** Thunder Dragon hides **the whole hero** from 0.6 to 3.8 s: every Renderer under her (`GetComponentsInChildren(Renderer)` :38018-38052). Cue: `[0.6, "hideProp", "hero", {"kill": 3.2}]`, the page's heroHide for kill seconds.
  - The game's list includes ParticleRenderers, so the worn weapon's own effects (weapon_fx.json) go dark as well.
- **P2 the Double Strider mover** (new; shared with skills_a's Left Stride).
  - The `doubleStrider_right` / `doubleStrider_left` ghost is an effect that the hero's code moves every FixedUpdate.
  - Each step it does LookAt the target on the flat, then `Translate((runSpeed + 1) x right x dt)`. Left Stride uses +, Right Stride uses -1 x (doubleStrideRight :29162-29168, doubleStrideLeft :27769-27775).
  - runSpeed is 5 (CharacterControl.cs:88).
  - Cue options:
    - `strafe`: m/s along the effect's own right; -6 for Right Stride, +6 for Left Stride.
    - `to`: the point it keeps facing, [0, 0, 10].
  - Without the mover, the ghost runs on the spot inside the hero.
- **P3 BB's ParticleSystem** (Unity 3.5 Shuriken; the Cat's P4).
  - `zeroShot_ring` has 3 systems and `thunderDragon_ring2` has 2.
  - wardrobe_fx.py's walker skips them without a word.
- **P4 WorldParticleCollider** (the Cat's P5): `tormentRain_fire`'s arrow rain stops on the floor.
- **P5 the `Self-Illumin/DoubleTexture` material** (new).
  - Used by `thunderDragon_ring2`'s dragon skeleton (StaticMesh `thunderDragon_skeleton_tri`).
  - The shader is one opaque unlit pass, `combine texture * texture` (checks/fx_chameleon_research/parts/shaders.txt:361-373).
  - Without it, mesh.js would warn and draw the skeleton as a particle material.
- **P6 the `FX/Invisible` hero skin** (new; shared with the Charge Attack / Perfect Blend / invisibility reports).
  - This is the blend / invisible look the Chameleon sees on herself. Her Diffuse renderers switch to FX/Invisible and the others turn off (CharacterControl.cs:32625-32684).
  - The shader (parts/shaders.txt:254ff) has FX/CosmicRift's shape: an offset back-face shell in (0.3, 0.6, 1, 0.75) plus the texture at 35 % alpha.
  - It needs a `HERO_SKINS["FX/Invisible"]` entry. In this scope only the Silent Walk tile uses it (Open question 4).
- Everything else in scope is already built: Image / Line / Ring emitters, legacy particles, EmitterControl, StaticMesh, Animation + SkinnedMeshRenderer, BoltEmitter to its own TargetNode (thunderDragon_ring1), Particles/AdditiveOffset (the slayer eyes, nAttack_hit, skinShift_chameleon: fxparts/particles.js) and EffectControl.

### 7. Only Quick Fire draws anything on the 10 m target

- Quick Fire's ray hits draw `nAttack_hit` on the body at `{"d": 9.7, "y": 0.63}`.
- These skills reach the target, but nothing is drawn:
  - Poison Volley's 12 m box, Torment Rain's area, and Right Stride's and Slayer's rays all reach it, but `hit()` draws nothing.
  - `poison` draws nothing on addStatus either (CharacterControl.cs:36965-36969).
- These skills cannot reach the target, so nothing is drawn (the Bison's convention):
  - Zero Shot: a 6 m pull and a 3 m box.
  - Thunder Dragon: 3 m ticks with a 12 % paralysis.

### 8. TTO in this scope

- Every TTO coroutine here loads the same names. Checked per function: RPC_quickFire d__154, RPC_poisonVolley d__162, RPC_rightStride d__178, RPC_skinShift d__194, RPC_slayer d__184, RPC_slayer_fire d__185, RPC_zeroShot d__198, RPC_thunderDragon d__199, RPC_tormentRain_fire.
- The one difference is Torment Rain's voice fix (item 4).
- No TTO-only skill plays these clips.
- The one TTO reference is Venom Phantom's `RPC_phantomRequiem` (d__301), which calls `Row6Sound("poisonVolley")` (pseudo/Chameleon.c:12682, :12753). That is a sound, not the clip, so it belongs to the tto report.

## The skills, at a glance

| Skill (clip) | Voice | Effects | Standby | Needs |
|---|---|---|---|---|
| Quick Fire (quickFire1 > quickFire2* > quickFire3) | quickFire1/2 at 0 | 18 shots: quickFire_fire 1 m ahead, 1.5 m up, + Sounds/quickFire at 0.4, 0.6 ... 2.1, 2.3; nAttack_hit on the body 0.1 s after each | 2.7 | hideProp, SEQ @0.6 |
| Poison Volley (poisonVolley) | poisonVolley1/2 at 0 | poisonVolley at the hero at 0 | 0.7 | hideProp |
| Torment Rain (rainOfArrow) | tormenrRain1/2 (TTO's fix) at 0 | the cage at 10 m (Open question 1); tormentRain_ring at 0.9; tormentRain_fire at the cage at 2.0 | 2.1 | WorldParticleCollider, hideProp, SEQ, icon map |
| Right Stride (rightStride) | rightStride1/2 at 0 | strideShot_dust and the doubleStrider_right ghost at 0; 5 shots at 0.366 + 0.433 i (rightStride_fire from her and from the ghost + Sounds/rightStride_fire1/2) | 2.298 | the mover, hideProp |
| Bug / Tail / Elemental / Machine Slayer (slayer1 > slayer2* > slayer3) | <x>Slayer1/2 at 0 | <x>Slayer_eye on the target at slayer2's 0 (1.0 s); Sounds/bow_fire1 + <x>Slayer_fire 1.5 m up, scale 1.4, at slayer3's 0 (1.1 s) | slayer3 0.7 | hideProp, SEQ fix |
| Skin Shift (skinShift) | skinShift1/2 at 0 | skinShift_ring (the shed skin) at the hero at 0 | 0.7 | hideProp |
| Zero Shot (zeroShot) | zeroShot1/2 at 0 | zeroShot_ring at the hero at 0 (its own shot lines at 1.0 / 1.1) | 1.3 | ParticleSystem, hideProp |
| Thunder Dragon (thunderDragon1 > thunderDragon2*) | none (the game has none) | thunderDragon_ring1 at 0; thunderDragon_ring2 (the dragon skeleton) at 0.6; the hero hidden 0.6-3.8 | 3.8 | ParticleSystem, DoubleTexture, hideProp hero |
| Silent Walk (silentWalk, looped) | none (no AnimationEvent) | the FX/Invisible look | - | FX/Invisible skin |

## Per clip: the timelines

Every coroutine here has the same frame. `default` (time 0):
- sets actionState attack, myCommand and the cooldown
- sets the hero's spot and facing
- plays the clip and sets moveSpeed
- plays the voice `Random.Range(0, 2)`: only with the pvoice setting on, for others only in the same team, at 0.75 volume
- spawns the first effect

The opaque predicates are worked out in `clean_<RPC>.txt`.

The camera effects (motion blur, screen warps) are left out, as the Wolf's and the Penguin's were. They are at Quick Fire :20281, Poison Volley :23234, Slayer :31989, Zero Shot :37134 and Thunder Dragon :37939.

### Quick Fire (RPC_quickFire :19240-20438; quickFire1 > quickFire2 held > quickFire3)

- **0:** `PlayAnimation("quickFire1", 0)` cut (:20163), moveSpeed 0, voice quickFire1|quickFire2 (:20204-20259).
- **0.4** (case 2, `Yield(2, 0.4)` :20329): the arrow (mWep2) is hidden (:19398-19425). The opening shot:
  - firePos = hero + TransformDirection(0, 1.5, 1) (:19435); fireDir = target `bounds.center` - firePos (:19451).
  - quickFire_fire is Instantiated there with `LookRotation(fireDir)` (:19478-19490): pitch atan(0.9 / 9) = 5.711 deg down.
  - quickFire_fire is a 0.3 s ImageEmitter flash (Ring4). The shot itself is a raycast; no arrow flies.
  - Sounds/quickFire plays on the hero's AudioSource (:19504-19522): a `"sound"` cue.
- **0.5** (case 3, `Yield(3, 0.1)` :20323): the ray (36 m, :19467) hits the body.
  - RPC_nAttack_hit(hit.point, hero forward) (:19590) spawns Effects/nAttack_hit at the hit point with the hero's rotation (:8565-8588; it plays its own bow_hit1).
  - From (0, 1.5, 1) toward (0, 0.6, 10), the ray meets the 0.3 m body's side at z 9.7, y 1.5 - 0.1 x 8.7 = 0.63.
- **0.6** (case 4, `Yield(4, 0.1)` :20313): `PlayAnimation("quickFire2", 0)` cut, Loop (:19660-19665).
  - The loop (:20061-20129): while i < 4 x sLv = 16 (Added Fire #402), LookAt the target, fire a shot (fx + sound), then `Yield(5, 0.1)` (:20340).
  - Case 5 (:19677-19761) checks that shot's ray (the hit) and does i++.
  - Shots at 0.6 ... 2.1 (quickFire2 time 0 ... 1.5); hits at 0.7 ... 2.2 (quickFire2 time 0.1 ... 1.6).
- **2.3** (case 6, `Yield(6, 0.1)` :20303): `PlayAnimation("quickFire3", 0)` cut, Once (:19787-19792), and the closing shot (:19797-19834). This is quickFire3 time 0.
- **2.4** (case 7): the closing shot's hit (:19869-19882).
- **2.5** (case 8): CrossFade(root, 0.2) (:19934).
- **2.7** (case 9, `Yield(9, 0.2)` :20336): the arrow is shown again (:19946-19981); standby (:20009).
- Notes:
  - 18 shots = 2 + 4 x sLv, matching the Bible's count.
  - The hide cue goes on quickFire1 at 0.4 with kill 2.3. `kill` runs on the effect's own age, so it spans the steps.

### Poison Volley (RPC_poisonVolley :23037-23758)

- **0:**
  - `PlayAnimation("poisonVolley", 0)` cut (:23503) and voice poisonVolley1|poisonVolley2 (:23544-23599).
  - Effects/poisonVolley createEffect at the hero, hero rotation (:23612-23628): life 1, followPosition, its own Sounds/poisonVolley, and Line emitters delayed 0.3 s.
- **0.3** (`Yield(2, 0.3)` :23666): the arrow is hidden (:23184-23211). The zoomMask screen warp is left out.
- **0.5** (`Yield(3, 0.2)` :23658): CrossFade(root, 0.2) (:23261). The hits on `FindRecTarget(hero, forward, 1, 8, 12, 4)` (:23279-23312) and the poison (:23318-23345) draw nothing.
- **0.7** (`Yield(4, 0.2)` :23670): the arrow is shown again; standby (:23433).
- The page plays the 0.8 s clip to its end. The game's root crossfade at 0.5 is not modelled.

### Torment Rain (RPC_tormentRain :25269-25872, RPC_tormentRain_fire :25872-26159; clip rainOfArrow)

- **The cage it needs.**
  - Torment Rain casts only while the Chameleon's own Final Entrapment cage stands, with her within 40 m (:6686-6703, the Bible).
  - Its spot `tPos` is the cage's position (`OAQYXXtBCn` :25635-25644).
  - The cage was spawned at the target's feet: `RPC_finalEntrapment_hit(tObject.transform.position, ...)` (:25004) -> `Instantiate(finalEntrapment, hitPos, identity)` (:9152).
  - So the rain falls at d 10. The tile shows the cage (Open question 1).
- **0:** `PlayAnimation("rainOfArrow", 0)` cut (:25668) and the voice (item 4: TTO's `tormenrRain1|tormenrRain2`).
- **0.9** (`Yield(2, 0.9)` :25811): tormentRain_ring createEffect at the hero, hero rotation (:25405-25423). It has life 2, followPosition and **followState** (cut at the standby, 2.1), and its own Sounds/tormentRain_ring.
- **1.2** (`Yield(3, 0.3)` :25791): the arrow is hidden (:25460-25487); RPC_tormentRain_fire(tPos, hero forward) starts (:25505 own, :25518 the others).
- **2.0** (tormentRain_fire's `Yield(2, 0.8)` :26105): Effects/tormentRain_fire is Instantiated at the cage spot with `LookRotation(hero forward)` (:25990-26006).
  - It has life 3 and its own Sounds/tormentRain_fire.
  - 64-256 arrows from 16 ± 12 m up fall at 48 m/s and land within about 0.6 s, with a dust burst at the floor (EmitterControl delay 0.1).
  - It needs WorldParticleCollider.
- **2.1** (`Yield(4, 0.9)` :25808): the arrow is shown again; standby (:25583).
- **2.2** (`Yield(3, 0.2)` :26109): the hits, `FindAreaTarget(cage, 8, 10)` (:26044-26067). Nothing is drawn.

### Right Stride (RPC_rightStride :27821-29212; strideRight :28847-29026; doubleStrideRight :29026-29212)

- **0, the hero:** `PlayAnimation("rightStride", 0.2)` (:28480); vMovement = right, moveSpeed = runSpeed + 1 (:28486-28489).
  - strideRight (:28504) keeps her facing the target every FixedUpdate while she runs right (:28977-28982), so she circles the target.
  - On the page she stays put: there is no hero mover (the Wolf's Feral Strike, Penguin decision 8).
- **0, Double Strider #423:**
  - Any earlier ghost is destroyed (:28523).
  - `doubleStrider_right` createEffect at the hero, hero rotation (:28529-28547). It is an animated ghost body: SkinnedMeshRenderer + Animation `root` (2.6 s, a strafe on the spot), EffectControl life 3, **followState** (cut at 2.298).
  - doubleStrideRight (:28573) moves it every FixedUpdate: LookAt the target on the flat, then `Translate((runSpeed + 1) x -1 x right x dt, world)` (:29162-29168). It circles the target the other way (P2).
  - stride_sim.txt: by 2.298 s it reaches (-9.89, 0, 8.03), 78.7 deg round.
- **0, voice and dust:** voice rightStride1|rightStride2 (:28617-28672). strideShot_dust createEffect at the hero (:28685-28703): life 2, followPosition + followState, its own looped Sounds/rightStride_footStep.
- **The five shots:** 0.366, 0.799, 1.232, 1.665, 2.098.
  - Timing: the first at 0.366 (`Yield(2, 0.366)` :28740), then every 0.433 s (`Yield(3, 0.433)` :28742), up to `i >= 2 x sLv + 1` = 5 (:28432).
  - The arrow is hidden at the first shot (:27979-28006).
  - Each shot:
    - Sounds/rightStride_fire1 on even shots, rightStride_fire2 on odd shots (:28145-28212): `"sound"` cues.
    - rightStride_fire at hero + TransformDirection(0.4, 1.2, 1), `LookRotation` to the target's bounds centre (:28219-28259): `{"x": 0.4, "d": 1, "y": 1.2, "rot": [3.81, -2.545, 0]}`.
    - The ghost's shot from its spot + its TransformDirection(-0.38, 1.2, 1), aimed the same way (:28289-28323).
  - The ghost's five spots and aims come from stride_sim.txt: 50 Hz steps, runSpeed 5. They are APPROXIMATED, since gear can add speed.
  - The RaycastAll hits (:28342-28414) draw nothing.
- **2.298** (`Yield(4, 0.2)` :28744): the arrow is shown again; standby (:28093). The ghost's and the dust's followState end here.

### Slayer: Bug / Tail / Elemental / Machine Slayer (RPC_slayer :30217-31274, RPC_slayer_fire :31274-32144)

- **slayer1, 0** (IL_1976 :30810):
  - `PlayAnimation("slayer1", 0.2)` (:30829).
  - Voice by sLv: bugSlayer1|2, tailSlayer1|2, elementalSlayer1|2, machineSlayer1|2 (:30870-31159).
  - Every frame (`YieldDefault(2)` :31197) she faces the target (:30629-30639) until `Time.time >= actionTime + 1` (:30367).
- **slayer2, from 1.0 s:** `PlayAnimation("slayer2", 0.2)`, Loop (:30391-30396).
  - castTime = `magAdjust(2 + 0.5 x 4)` (:30406) = 4 s less INT / 32, with a floor of 0.1. That is **0.1 s** at top INT.
  - In the same frame the eye: `<x>Slayer_eye` is Instantiated at the target's `collider.bounds.center`, identity, with `InitEffectControl(target)` (:30688-30727). It has life 1 + 0.5, followPosition on the target, and its own Sounds/slayerCharge.
  - The eye repeats every 2 s only while `mEffectTimer + 2 < castTimer` (:30696-30712). With a 0.1 s cast it spawns once.
  - Cue: `{"d": 10, "y": 0.6}`.
- **slayer3, from 1.1 s** (`Time.time >= castTimer` :30660 -> RPC_slayer_fire :30784-30795):
  - `PlayAnimation("slayer3", 0.2)` (:31749).
  - `audio.PlayOneShot(nAttack_bowFx1)` (:31761) = Sounds/bow_fire1 (the prefab's field): a `"sound"` cue.
  - fireVector = target bounds centre - hero - 1.5 up, y clamped to ±0.05 (:31764-31770): pitch 2.874 deg.
  - `<x>Slayer_fire` at hero + 1.5 up with `LookRotation(fireVector)` (:31785-31926): life 1, its own Sounds/slayerFire. localScale 1 + 0.1 x Improved Slayer 4 = **1.4** (:31947).
  - The arrow is hidden (:31953-31972) until 0.85 (:31682-31710).
  - At 0.1 (`Yield(2, 0.1)` :32022): the hits, `FindRecTarget(hero + forward, forward, 1.0, 1.0, 36, 10)` (:31455-31610), x2 on the member's race or slayerMark. Nothing is drawn.
  - At 0.7 (`Yield(3, 0.6)` :32028): standby (:31642).
  - At 0.85 (`Yield(4, 0.15)` :32032): the arrow is shown again.

### Skin Shift (RPC_skinShift :34709-35336)

- **0:**
  - `PlayAnimation("skinShift", 0)` cut (:34987). moveSpeed -3: she hops back about 1.8 m in 0.6 s (:34996). The hop is not on the page.
  - Voice skinShift1|skinShift2 (:35028-35083).
  - skinShift_ring is Instantiated at the hero, hero rotation (:35096-35114). It has life 1 + 1: a smoke burst, a ring, and the **shed skin** (StaticMesh `skinShift_chameleon`, a Chameleon-shaped shell in Particles/AdditiveOffset), plus its own Sounds/skinShift.
  - The arrow is hidden (:35128-35147).
  - Every non-system status is removed (:35155-35215), and 10 % of hp is taken (RPC_AddDamage :35229, no effect drawn).
- **0.6** (`Yield(2, 0.6)` :35261): moveSpeed 0.
- **0.7** (`Yield(3, 0.1)` :35257): the arrow is shown again; standby (:34917).

### Zero Shot (RPC_zeroShot :36976-37784)

- **0:**
  - `PlayAnimation("zeroShot", 0)` cut (:37522), moveSpeed -2 (:37531), voice zeroShot1|zeroShot2 (:37563-37618).
  - zeroShot_ring createEffect at the hero, hero rotation (:37631-37647). It has life 1 + 2 and followPosition. It holds:
    - shot lines: Line emitters delayed 1.0 / 1.1 s, 1.3 m up, 1.6 m ahead
    - a ground ring delayed 1.0 s
    - three **BB ParticleSystems**
    - its own Sounds/zeroShot

    The effect itself times the shot's look to 1.0 s.
- **0.5** (`Yield(2, 0.5)` :37689): moveSpeed -1. Then a pull every 0.1 s at 0.5 ... 0.9 (`i < 5` :37338, `Yield(3, 0.1)` :37679; FindAreaTarget(hero + 2 forward, 6) :37441-37490). The target is out of reach, so nothing is drawn.
- **1.0:** the arrow is hidden (:37344-37371); moveSpeed -6; the 4 x 3 x 3 m hit box (:37399-37422) is also out of reach.
- **1.2** (`Yield(4, 0.2)` :37685): the arrow is shown again unless she is invisible (:37218-37255).
- **1.3** (`Yield(5, 0.1)` :37681): standby (:37286).

### Thunder Dragon (RPC_thunderDragon :37784-38604; thunderDragon1 > thunderDragon2 held)

- **0:**
  - `PlayAnimation("thunderDragon1", 0)` cut (:38240). blend and invisible are removed (:38260-38265).
  - thunderDragon_ring1 createEffect at the hero, hero rotation (:38270-38288). It has life 3 + 1, followPosition, followState, and its own Sounds/thunderDragon_ring1. Its thunderBolt node falls from 24 m at 48 m/s, with a BoltEmitter to its own BoltTarget.
  - It needs no cut: actionState stays `attack` until 3.8, after its life ends at 3.0.
  - No voice.
- **0.6** (`Yield(2, 0.3)` :38491, `Yield(3, 0.3)` :38500): myCommand becomes thunderDragon2 (:37981).
  - thunderDragon_ring2 createEffect at the hero, hero rotation (:37986-38004). It has life 3.2 (ending with the standby at 3.8), followPosition and followState. It holds the dragon skeleton StaticMesh (Self-Illumin/DoubleTexture), two BB ParticleSystems and a looped Sounds/thunderDragon_ring2.
  - **Every Renderer under the hero turns off** (:38018-38052): she becomes the dragon until 3.8.
- **0.8** (`Yield(4, 0.2)` :38487): `PlayAnimation("thunderDragon2", 0)` cut, Loop (:38081-38086). This is thunderDragon2 time 0.
- **Ticks** at thunderDragon2 time 0, 0.5 ... 2.5 (`Yield(5, 0.5)` :38485, i++ :38155): FindAreaTarget(hero, 3, 3) damage plus a 12 % paralysis (:38418-38465). The paralysis look is Panda/Effects/paralysis (CharacterControl.cs:35443) on a foe in reach. The 10 m target is out of reach, so nothing is drawn.
- **3.0 of thunderDragon2 = 3.8** (i >= 6, :38305): the hero's renderers turn back on (:38309-38332); standby (:38357).

### Silent Walk (silentWalk, looped; passive #411 in RPC_cAttack1 :16112-16841)

- Only RPC_cAttack1 plays this clip. While the charge is held and the player walks, it calls `PlayAnimation("silentWalk", 0.2)` (:16584; another client's copy :16634). It goes back to cAttack2 when she stops (:16604, :16648). So the tile is the walk inside the Charge Attack's charge.
- By then (0.8 s into the charge) she holds the `blend` status (`RPC_AddStatus("blend", 4, chaAdjust(3 x lv + 3))` :16358). The `blend` flash at 0.6 m up (:16325-16337) belongs to the charge.
- On her own team's screens, hers included, blend draws every Diffuse renderer in FX/Invisible and turns the others off (CharacterControl.cs:32494-32509, :32625-32684).
- The clip has no AnimationEvent (probe_events.txt), so Silent Walk is silent.
- The charge rings (cAttack_ring1 each second, cAttack_ring2 at full charge, :16422-16516) belong to the charge's timer, so they stay on the Charge Attack tile.
- Cue: the FX/Invisible hero skin for the tile (Open question 4).

## Buildability (inventory + probe)

| Effect | Loaded at | Probe | Status |
|---|---|---|---|
| quickFire_fire | :19478 | EC 0.3 + ImageEmitter | ready |
| nAttack_hit | :8578 | EC 1, 3 ImageEmitters (AdditiveOffset, built), bow_hit1 | ready |
| poisonVolley | :23618 | EC 1 fPos, Image / Line, legacy particles, EmitterControl | ready |
| tormentRain_ring | :25411 | EC 2 fPos fState, Line / Ring / Image | ready |
| tormentRain_fire | :25996 | EC 3, legacy particles + EmitterControl; WorldParticleCollider skipped | needs WorldParticleCollider (P4) |
| finalEntrapment (the cage) | :9142 | EC 6 (the game sets 7), Animation + SkinnedMeshRenderer, Rings | ready |
| rightStride_fire | :28247 | EC 1, Image + Line | ready |
| strideShot_dust | :28691 | EC 2 fPos fState, legacy particles, looped footstep | ready |
| doubleStrider_right | :28535 | EC 3 fState, Animation (root 2.6 s) + SkinnedMeshRenderer (57 nodes) | ready as an effect; its motion needs the mover (P2) |
| bugSlayer_eye, tailSlayer_eye, elementalSlayer_eye, machineSlayer_eye | :30450-30567 | EC 1 + 0.5 fPos, ImageEmitter (slayerEye, AdditiveOffset), slayerCharge | ready |
| bugSlayer_fire, tailSlayer_fire, elementalSlayer_fire, machineSlayer_fire | :31797-31914 | EC 1, Line + 2 Rings, slayerFire | ready |
| skinShift_ring | :35102 | EC 1 + 1, legacy particles, Ring, StaticMesh (AdditiveOffset) | ready |
| zeroShot_ring | :37637 | EC 1 + 2 fPos, Line / Ring; 3 ParticleSystems skipped | needs BB ParticleSystem (P3) |
| thunderDragon_ring1 | :38276 | EC 3 + 1 fPos fState, Line / Ring, a child EC with velocity, BoltEmitter to its TargetNode | ready |
| thunderDragon_ring2 | :37992 | EC 3.2 fPos fState, Line / Ring; 2 ParticleSystems skipped; StaticMesh in Self-Illumin/DoubleTexture | needs BB ParticleSystem (P3) + DoubleTexture (P5) |
| (hero look) FX/Invisible | CharacterControl.cs:32649 | shader in parts/shaders.txt | needs a HERO_SKINS entry (P6) |

**Sounds, voices and AudioSource clips** (all checked against the rip):
- `"sound"` cues: quickFire, rightStride_fire1, rightStride_fire2, bow_fire1. All are in the rip's chameleon/sounds.
- Voices: quickFire1/2, poisonVolley1/2, tormenrRain1/2, rightStride1/2, bugSlayer1/2, tailSlayer1/2, elementalSlayer1/2, machineSlayer1/2, skinShift1/2, zeroShot1/2. All are in chameleon/voices.
- Every effect's own AudioSource clip is in chameleon/sounds too: bow_hit1, poisonVolley, tormentRain_ring, tormentRain_fire, finalEntrapment, finalEntrapment_hit, rightStride_footStep, slayerCharge, slayerFire, skinShift, zeroShot, thunderDragon_ring1, thunderDragon_ring2.

## Page changes (index.html, wardrobe_skill_icons.py), besides the parts

- **SEQ chameleon:**
  - `"Quick Fire: quickFire1@0.6 quickFire2*@1.7 quickFire3"` (was @0.4).
  - `"Slayer: slayer1@1 slayer2*~@0.1 slayer3~"` (was `slayer1 slayer2*~@0 slayer3~`).
  - New: `"Torment Rain: rainOfArrow@2.7"`.
  - In the SEQ comment, the Quick Fire sentence becomes: "quickFire2 from 0.6 s (the opening shot at 0.4, its ray at 0.5, Chameleon.cs:20313)".
- **wardrobe_skill_icons.py:** add `CLIP_SKILLS["chameleon"] = {"rainOfArrow": ["tormentRain"]}`, then run it. The Slayer pool's four icons come from the cue file.
- **New cue kinds:** fxStart's sound preload and fxDue must know the `hideProp` kind, and the FX/Invisible `skin` must be in HERO_SKINS. The Cat's P6 note applies: any kind other than fx / skin / clone is fetched and played as a sound.
- **wardrobe_fx.py** builds `tormenrRain1` / `tormenrRain2` by the cue's name. That is the files' own spelling, so no alias is needed.

## Paste-ready cues for wardrobe/fx_cues/chameleon.json

- 14 entries, 113 cues, in `D:\12tails-wardrobe\checks\fx_chameleon_research\skills_b\cues_block.json` (valid JSON, the same as cues.json).
- The keys are the clips. The Slayer pool uses the Wolf's / Sheep's / Penguin's `{why, skills: {member: {why, cues}}}` shape on each of its three clips.
- New cue kinds and options: `hideProp` (P1), `strafe` (P2), and the `"skin"` FX/Invisible (P6). Every other option is one the page reads today.
- `thunderDragon2`'s empty entry only documents the clip and can be left out.

```json
{
  "quickFire1": {
    "why": "RPC_quickFire :19240-20438, rank 4 + Added Fire #402 (passives on): every shot = quickFire_fire Instantiated at firePos = hero + TransformDirection(0, 1.5, 1), LookRotation(fireDir), fireDir = (target bounds centre - firePos) (:19435-19490, :19797-19820, :20092-20115; a 0.3 s ImageEmitter flash, no projectile: the shot is a Physics.Raycast of 20 + 4 x Far Reach 4 = 36 m, :19467) + Sounds/quickFire on the hero's AudioSource (:19510-19522, :19834, :20129; a 'sound' cue); 0.1 s later the ray's hit: RPC_nAttack_hit(hit.point, hero forward) (:19590, :19713, :19882) = Effects/nAttack_hit at the hit point, the hero's rotation (:8565-8588; plays its own Sounds/bow_hit1), on the 10 m target point (a Penguin-sized body: bounds centre 0.6 m up, height 1, radius 0.3): the ray from (0, 1.5, 1) meets the body's side at d 9.7, y 0.63; mChar.hit draws nothing else; this clip: PlayAnimation(quickFire1, 0) cut (:20163) and voice quickFire1 / quickFire2 (Random.Range(0, 2) :20204-20259) at 0; Yield 0.4 (:20329): the arrow in hand (mWep2 = slot R) hidden (:19398-19425) until 2.7 s (:19946-19981), the opening shot (:19435-19522); Yield 0.1 (:20323): its hit at 0.5 (:19577-19590); Yield 0.1 (:20313): quickFire2 at 0.6 (case 4 :19641-19670), so the SEQ step is quickFire1@0.6 (index.html had 0.4); left out: the camera motion blur (:20281)",
    "cues": [
      [0, "voice", "quickFire1|quickFire2"],
      [0.4, "fx", "quickFire_fire", {"d": 1, "y": 1.5, "rot": [5.711, 0, 0]}],
      [0.4, "sound", "quickFire"],
      [0.4, "hideProp", "R", {"kill": 2.3}],
      [0.5, "fx", "nAttack_hit", {"d": 9.7, "y": 0.63}]
    ]
  },
  "quickFire2": {
    "why": "RPC_quickFire :19240-20438, rank 4 + Added Fire #402 (passives on): every shot = quickFire_fire Instantiated at firePos = hero + TransformDirection(0, 1.5, 1), LookRotation(fireDir), fireDir = (target bounds centre - firePos) (:19435-19490, :19797-19820, :20092-20115; a 0.3 s ImageEmitter flash, no projectile: the shot is a Physics.Raycast of 20 + 4 x Far Reach 4 = 36 m, :19467) + Sounds/quickFire on the hero's AudioSource (:19510-19522, :19834, :20129; a 'sound' cue); 0.1 s later the ray's hit: RPC_nAttack_hit(hit.point, hero forward) (:19590, :19713, :19882) = Effects/nAttack_hit at the hit point, the hero's rotation (:8565-8588; plays its own Sounds/bow_hit1), on the 10 m target point (a Penguin-sized body: bounds centre 0.6 m up, height 1, radius 0.3): the ray from (0, 1.5, 1) meets the body's side at d 9.7, y 0.63; mChar.hit draws nothing else; this clip (from 0.6 s of the skill): PlayAnimation(quickFire2, 0) cut, WrapMode.Loop (:19660-19665), i = 0 (:19670); the loop shots while i < 4 x sLv = 16 with Added Fire (:20061): LookAt the target, shot (:20065-20129), Yield 0.1 (:20340), its hit and i++ (case 5 :19677-19761): shots at 0, 0.1 ... 1.5, hits at 0.1 ... 1.6; after the 16th hit Yield 0.1 (:20303): quickFire3 at 1.7 (the SEQ's quickFire2*@1.7)",
    "cues": [
      [0.0, "fx", "quickFire_fire", {"d": 1, "y": 1.5, "rot": [5.711, 0, 0]}],
      [0.0, "sound", "quickFire"],
      [0.1, "fx", "nAttack_hit", {"d": 9.7, "y": 0.63}],
      [0.1, "fx", "quickFire_fire", {"d": 1, "y": 1.5, "rot": [5.711, 0, 0]}],
      [0.1, "sound", "quickFire"],
      [0.2, "fx", "nAttack_hit", {"d": 9.7, "y": 0.63}],
      [0.2, "fx", "quickFire_fire", {"d": 1, "y": 1.5, "rot": [5.711, 0, 0]}],
      [0.2, "sound", "quickFire"],
      [0.3, "fx", "nAttack_hit", {"d": 9.7, "y": 0.63}],
      [0.3, "fx", "quickFire_fire", {"d": 1, "y": 1.5, "rot": [5.711, 0, 0]}],
      [0.3, "sound", "quickFire"],
      [0.4, "fx", "nAttack_hit", {"d": 9.7, "y": 0.63}],
      [0.4, "fx", "quickFire_fire", {"d": 1, "y": 1.5, "rot": [5.711, 0, 0]}],
      [0.4, "sound", "quickFire"],
      [0.5, "fx", "nAttack_hit", {"d": 9.7, "y": 0.63}],
      [0.5, "fx", "quickFire_fire", {"d": 1, "y": 1.5, "rot": [5.711, 0, 0]}],
      [0.5, "sound", "quickFire"],
      [0.6, "fx", "nAttack_hit", {"d": 9.7, "y": 0.63}],
      [0.6, "fx", "quickFire_fire", {"d": 1, "y": 1.5, "rot": [5.711, 0, 0]}],
      [0.6, "sound", "quickFire"],
      [0.7, "fx", "nAttack_hit", {"d": 9.7, "y": 0.63}],
      [0.7, "fx", "quickFire_fire", {"d": 1, "y": 1.5, "rot": [5.711, 0, 0]}],
      [0.7, "sound", "quickFire"],
      [0.8, "fx", "nAttack_hit", {"d": 9.7, "y": 0.63}],
      [0.8, "fx", "quickFire_fire", {"d": 1, "y": 1.5, "rot": [5.711, 0, 0]}],
      [0.8, "sound", "quickFire"],
      [0.9, "fx", "nAttack_hit", {"d": 9.7, "y": 0.63}],
      [0.9, "fx", "quickFire_fire", {"d": 1, "y": 1.5, "rot": [5.711, 0, 0]}],
      [0.9, "sound", "quickFire"],
      [1.0, "fx", "nAttack_hit", {"d": 9.7, "y": 0.63}],
      [1.0, "fx", "quickFire_fire", {"d": 1, "y": 1.5, "rot": [5.711, 0, 0]}],
      [1.0, "sound", "quickFire"],
      [1.1, "fx", "nAttack_hit", {"d": 9.7, "y": 0.63}],
      [1.1, "fx", "quickFire_fire", {"d": 1, "y": 1.5, "rot": [5.711, 0, 0]}],
      [1.1, "sound", "quickFire"],
      [1.2, "fx", "nAttack_hit", {"d": 9.7, "y": 0.63}],
      [1.2, "fx", "quickFire_fire", {"d": 1, "y": 1.5, "rot": [5.711, 0, 0]}],
      [1.2, "sound", "quickFire"],
      [1.3, "fx", "nAttack_hit", {"d": 9.7, "y": 0.63}],
      [1.3, "fx", "quickFire_fire", {"d": 1, "y": 1.5, "rot": [5.711, 0, 0]}],
      [1.3, "sound", "quickFire"],
      [1.4, "fx", "nAttack_hit", {"d": 9.7, "y": 0.63}],
      [1.4, "fx", "quickFire_fire", {"d": 1, "y": 1.5, "rot": [5.711, 0, 0]}],
      [1.4, "sound", "quickFire"],
      [1.5, "fx", "nAttack_hit", {"d": 9.7, "y": 0.63}],
      [1.5, "fx", "quickFire_fire", {"d": 1, "y": 1.5, "rot": [5.711, 0, 0]}],
      [1.5, "sound", "quickFire"],
      [1.6, "fx", "nAttack_hit", {"d": 9.7, "y": 0.63}]
    ]
  },
  "quickFire3": {
    "why": "RPC_quickFire :19240-20438, rank 4 + Added Fire #402 (passives on): every shot = quickFire_fire Instantiated at firePos = hero + TransformDirection(0, 1.5, 1), LookRotation(fireDir), fireDir = (target bounds centre - firePos) (:19435-19490, :19797-19820, :20092-20115; a 0.3 s ImageEmitter flash, no projectile: the shot is a Physics.Raycast of 20 + 4 x Far Reach 4 = 36 m, :19467) + Sounds/quickFire on the hero's AudioSource (:19510-19522, :19834, :20129; a 'sound' cue); 0.1 s later the ray's hit: RPC_nAttack_hit(hit.point, hero forward) (:19590, :19713, :19882) = Effects/nAttack_hit at the hit point, the hero's rotation (:8565-8588; plays its own Sounds/bow_hit1), on the 10 m target point (a Penguin-sized body: bounds centre 0.6 m up, height 1, radius 0.3): the ray from (0, 1.5, 1) meets the body's side at d 9.7, y 0.63; mChar.hit draws nothing else; this clip (from 2.3 s of the skill): PlayAnimation(quickFire3, 0) cut, Once (:19787-19792) and the closing shot (:19797-19834) at 0; Yield 0.1 (:20327): its hit at 0.1 (:19869-19882); Yield 0.1 (:20309): CrossFade(root, 0.2) at 0.2 (:19934); Yield 0.2 (:20336): the arrow shown again, standby at 0.4 (:19946-20019)",
    "cues": [
      [0, "fx", "quickFire_fire", {"d": 1, "y": 1.5, "rot": [5.711, 0, 0]}],
      [0, "sound", "quickFire"],
      [0.1, "fx", "nAttack_hit", {"d": 9.7, "y": 0.63}]
    ]
  },
  "poisonVolley": {
    "why": "RPC_poisonVolley :23037-23758 (rank 2): PlayAnimation(poisonVolley, 0) cut (:23503), voice poisonVolley1 / poisonVolley2 (Random.Range(0, 2) :23544-23599) and Effects/poisonVolley createEffect at the hero, hero rotation (:23612-23628; life 1, followPosition, plays its own Sounds/poisonVolley) at 0; Yield 0.3 (:23666): the arrow (mWep2, slot R) hidden (:23184-23211) until 0.7 (:23370-23405); the camera's zoomMask warp left out (:23234); Yield 0.2 (:23658): CrossFade(root, 0.2) at 0.5 (:23261), the hits FindRecTarget(hero, forward, 1, 8, 12, 4) (:23279-23312) and poison (:23318-23345) draw nothing on the target (CharacterControl addStatus 'poison' draws nothing, CharacterControl.cs:36965-36969); Yield 0.2 (:23670): standby 0.7 (:23433)",
    "cues": [
      [0, "voice", "poisonVolley1|poisonVolley2"],
      [0, "fx", "poisonVolley"],
      [0.3, "hideProp", "R", {"kill": 0.4}]
    ]
  },
  "rainOfArrow": {
    "why": "RPC_tormentRain :25269-25872 (Torment Rain #273, rank 1): cast only while the Chameleon's own Final Entrapment cage stands (:6686-6703); its spot tPos = the cage's position (OAQYXXtBCn :25635-25644) = the target's feet (RPC_finalEntrapment_hit(tObject.transform.position) :25004, Instantiate(finalEntrapment, hitPos, identity) :9152): the cage shown at the 10 m target point (a Penguin-sized body: bounds centre 0.6 m up, height 1, radius 0.3) from 0 to the tile's end, as Snow Ball shows the snowman it needs (penguin.json snowBall); PlayAnimation(rainOfArrow, 0) cut (:25668) at 0 and the voice: BB loads Voices/tormentRain1 / tormentRain2 (:25719, :25750), which the game has no file for (the rip: voices/tormenrRain1.wav, tormenrRain2.wav), so BB plays nothing; TTO loads Voices/tormenrRain1 / tormenrRain2 (TTO1102 Chameleon.<RPC_tormentRain>d__170::MoveNext, pseudo/Chameleon.c:20602-20604): TTO's fix (Sheep decision 10); Yield 0.9 (:25811): tormentRain_ring createEffect at the hero, hero rotation (:25405-25423; life 2, followState: cut at the standby, 2.1; plays its own Sounds/tormentRain_ring); Yield 0.3 (:25791): the arrow (slot R) hidden (:25460-25487) until 2.1 (:25527-25555) and RPC_tormentRain_fire(tPos, hero forward) (:25505, :25518): Yield 0.8 (:26105), then Effects/tormentRain_fire Instantiated at the cage spot, LookRotation(hero forward) (:25990-26006) at 2.0 (life 3, plays its own Sounds/tormentRain_fire; its arrows fall from 16 m at 48 m/s and need WorldParticleCollider); the hits FindAreaTarget(cage, 8, 10) at 2.2 (:26044-26067) draw nothing; Yield 0.9 (:25808): standby 2.1 (:25583)",
    "cues": [
      [0, "voice", "tormenrRain1|tormenrRain2"],
      [0, "fx", "finalEntrapment", {"d": 10, "kill": 2.7}],
      [0.9, "fx", "tormentRain_ring", {"cut": 2.1}],
      [1.2, "hideProp", "R", {"kill": 0.9}],
      [2.0, "fx", "tormentRain_fire", {"d": 10}]
    ]
  },
  "rightStride": {
    "why": "RPC_rightStride :27821-29212 (rank 2: 2 x sLv + 1 = 5 shots, :28432; Double Strider #423 on): PlayAnimation(rightStride, 0.2) (:28480), the hero runs right at runSpeed + 1 circling the target (:28486-28504, strideRight :28977-28982: the page has no hero mover, she stays, as the Wolf's Feral Strike); #423: doubleStrider_right createEffect at the hero, hero rotation (:28529-28547; an animated ghost body, life 3, followState: cut at the standby 2.298), moved by doubleStrideRight every FixedUpdate: LookAt the target on the flat, then Translate(-(runSpeed + 1) x its right x dt, world) (:29162-29168): a page part (cue option strafe -6 m/s, to = the target), runSpeed 5 (CharacterControl.cs:88); voice rightStride1 / rightStride2 (Random.Range(0, 2) :28617-28672) and strideShot_dust at the hero, hero rotation (:28685-28703; life 2, followPosition + followState, its own looped Sounds/rightStride_footStep) at 0; Yield 0.366 (:28740), then a shot every 0.433 s (:28742): 0.366, 0.799, 1.232, 1.665, 2.098; the arrow (slot R) hidden from 0.366 (:27979-28006) to 2.298 (:28037-28065); each shot: Sounds/rightStride_fire1 on even shots, rightStride_fire2 on odd (:28145-28212, 'sound' cues), rightStride_fire Instantiated at hero + TransformDirection(0.4, 1.2, 1), LookRotation to the target's bounds centre (:28219-28259: rot [3.81, -2.545, 0]) and one at the clone + its TransformDirection(-0.38, 1.2, 1) aimed the same way (:28289-28323; the spots from checks/fx_chameleon_research/skills_b/stride_sim.txt, APPROXIMATED with runSpeed 5); the RaycastAll hits (:28342-28414) draw nothing; Yield 0.2 (:28744): standby 2.298 (:28093)",
    "cues": [
      [0, "voice", "rightStride1|rightStride2"],
      [0, "fx", "strideShot_dust", {"cut": 2.298}],
      [0, "fx", "doubleStrider_right", {"cut": 2.298, "strafe": -6, "to": [0, 0, 10]}],
      [0.366, "hideProp", "R", {"kill": 1.932}],
      [0.366, "sound", "rightStride_fire1"],
      [0.366, "fx", "rightStride_fire", {"x": 0.4, "d": 1, "y": 1.2, "rot": [3.81, -2.545, 0]}],
      [0.366, "fx", "rightStride_fire", {"x": -2.406, "d": 1.305, "y": 1.2, "rot": [3.805, 15.468, 0]}],
      [0.799, "sound", "rightStride_fire2"],
      [0.799, "fx", "rightStride_fire", {"x": 0.4, "d": 1, "y": 1.2, "rot": [3.81, -2.545, 0]}],
      [0.799, "fx", "rightStride_fire", {"x": -4.501, "d": 2.164, "y": 1.2, "rot": [3.799, 29.872, 0]}],
      [1.232, "sound", "rightStride_fire1"],
      [1.232, "fx", "rightStride_fire", {"x": 0.4, "d": 1, "y": 1.2, "rot": [3.81, -2.545, 0]}],
      [1.232, "fx", "rightStride_fire", {"x": -6.394, "d": 3.592, "y": 1.2, "rot": [3.792, 44.939, 0]}],
      [1.665, "sound", "rightStride_fire2"],
      [1.665, "fx", "rightStride_fire", {"x": 0.4, "d": 1, "y": 1.2, "rot": [3.81, -2.545, 0]}],
      [1.665, "fx", "rightStride_fire", {"x": -7.852, "d": 5.463, "y": 1.2, "rot": [3.785, 59.982, 0]}],
      [2.098, "sound", "rightStride_fire1"],
      [2.098, "fx", "rightStride_fire", {"x": 0.4, "d": 1, "y": 1.2, "rot": [3.81, -2.545, 0]}],
      [2.098, "fx", "rightStride_fire", {"x": -8.745, "d": 7.545, "y": 1.2, "rot": [3.779, 74.319, 0]}]
    ]
  },
  "slayer1": {
    "why": "RPC_slayer :30217-31274 and RPC_slayer_fire :31274-32144: four skills on one coroutine, sLv = the skill (Bug / Tail / Elemental / Machine Slayer, #341-344, each its own cooldown key slayer + sLv :30820), one per play at random on the Slayer host, each its own tile (poolChains); slayer1 at 0 (:30829)",
    "skills": {
      "bugSlayer": {
        "why": "bugSlayer (sLv 1, x2 on Bugs / Plants): PlayAnimation(slayer1, 0.2) (:30829) and voice bugSlayer1 / bugSlayer2 (the sLv switch, Random.Range(0, 2) :30870-31159) at 0; each frame the hero faces the target until Time.time >= actionTime + 1 (:30367, :30629-30639, YieldDefault :31197): slayer2 at 1.0 (SEQ step slayer1@1; the clip is 1.5 s)",
        "cues": [
          [0, "voice", "bugSlayer1|bugSlayer2"]
        ]
      },
      "tailSlayer": {
        "why": "tailSlayer (sLv 2, x2 on Tails): PlayAnimation(slayer1, 0.2) (:30829) and voice tailSlayer1 / tailSlayer2 (the sLv switch, Random.Range(0, 2) :30870-31159) at 0; each frame the hero faces the target until Time.time >= actionTime + 1 (:30367, :30629-30639, YieldDefault :31197): slayer2 at 1.0 (SEQ step slayer1@1; the clip is 1.5 s)",
        "cues": [
          [0, "voice", "tailSlayer1|tailSlayer2"]
        ]
      },
      "elementalSlayer": {
        "why": "elementalSlayer (sLv 3, x2 on Elementals): PlayAnimation(slayer1, 0.2) (:30829) and voice elementalSlayer1 / elementalSlayer2 (the sLv switch, Random.Range(0, 2) :30870-31159) at 0; each frame the hero faces the target until Time.time >= actionTime + 1 (:30367, :30629-30639, YieldDefault :31197): slayer2 at 1.0 (SEQ step slayer1@1; the clip is 1.5 s)",
        "cues": [
          [0, "voice", "elementalSlayer1|elementalSlayer2"]
        ]
      },
      "machineSlayer": {
        "why": "machineSlayer (sLv 4, x2 on Robots): PlayAnimation(slayer1, 0.2) (:30829) and voice machineSlayer1 / machineSlayer2 (the sLv switch, Random.Range(0, 2) :30870-31159) at 0; each frame the hero faces the target until Time.time >= actionTime + 1 (:30367, :30629-30639, YieldDefault :31197): slayer2 at 1.0 (SEQ step slayer1@1; the clip is 1.5 s)",
        "cues": [
          [0, "voice", "machineSlayer1|machineSlayer2"]
        ]
      }
    }
  },
  "slayer2": {
    "why": "RPC_slayer :30217-31274 and RPC_slayer_fire :31274-32144: four skills on one coroutine, sLv = the skill (Bug / Tail / Elemental / Machine Slayer, #341-344, each its own cooldown key slayer + sLv :30820), one per play at random on the Slayer host, each its own tile (poolChains); slayer2 from 1.0 s (:30367-30396)",
    "skills": {
      "bugSlayer": {
        "why": "bugSlayer: PlayAnimation(slayer2, 0.2), Loop (:30391-30396) at 0; the cast castTime = magAdjust(2 + 0.5 x Improved Slayer 4) = 4 s less INT / 32, floor 0.1 (:30406; CharacterControl.cs:20584-20588): 0.1 s at top INT (the user's no-cast-bar rule; the Bat's Guardian step @0.1); in the same frame bugSlayer_eye (:30428-30587) Instantiated at the target's collider.bounds.center, identity, InitEffectControl(target) (:30688-30727; life 1 + 0.5, followPosition, plays its own Sounds/slayerCharge), again every 2 s only while mEffectTimer + 2 < castTimer (:30696-30712): once at 0.1 s; at castTimer RPC_slayer_fire (:30660, :30784-30795)",
        "cues": [
          [0, "fx", "bugSlayer_eye", {"d": 10, "y": 0.6}]
        ]
      },
      "tailSlayer": {
        "why": "tailSlayer: PlayAnimation(slayer2, 0.2), Loop (:30391-30396) at 0; the cast castTime = magAdjust(2 + 0.5 x Improved Slayer 4) = 4 s less INT / 32, floor 0.1 (:30406; CharacterControl.cs:20584-20588): 0.1 s at top INT (the user's no-cast-bar rule; the Bat's Guardian step @0.1); in the same frame tailSlayer_eye (:30428-30587) Instantiated at the target's collider.bounds.center, identity, InitEffectControl(target) (:30688-30727; life 1 + 0.5, followPosition, plays its own Sounds/slayerCharge), again every 2 s only while mEffectTimer + 2 < castTimer (:30696-30712): once at 0.1 s; at castTimer RPC_slayer_fire (:30660, :30784-30795)",
        "cues": [
          [0, "fx", "tailSlayer_eye", {"d": 10, "y": 0.6}]
        ]
      },
      "elementalSlayer": {
        "why": "elementalSlayer: PlayAnimation(slayer2, 0.2), Loop (:30391-30396) at 0; the cast castTime = magAdjust(2 + 0.5 x Improved Slayer 4) = 4 s less INT / 32, floor 0.1 (:30406; CharacterControl.cs:20584-20588): 0.1 s at top INT (the user's no-cast-bar rule; the Bat's Guardian step @0.1); in the same frame elementalSlayer_eye (:30428-30587) Instantiated at the target's collider.bounds.center, identity, InitEffectControl(target) (:30688-30727; life 1 + 0.5, followPosition, plays its own Sounds/slayerCharge), again every 2 s only while mEffectTimer + 2 < castTimer (:30696-30712): once at 0.1 s; at castTimer RPC_slayer_fire (:30660, :30784-30795)",
        "cues": [
          [0, "fx", "elementalSlayer_eye", {"d": 10, "y": 0.6}]
        ]
      },
      "machineSlayer": {
        "why": "machineSlayer: PlayAnimation(slayer2, 0.2), Loop (:30391-30396) at 0; the cast castTime = magAdjust(2 + 0.5 x Improved Slayer 4) = 4 s less INT / 32, floor 0.1 (:30406; CharacterControl.cs:20584-20588): 0.1 s at top INT (the user's no-cast-bar rule; the Bat's Guardian step @0.1); in the same frame machineSlayer_eye (:30428-30587) Instantiated at the target's collider.bounds.center, identity, InitEffectControl(target) (:30688-30727; life 1 + 0.5, followPosition, plays its own Sounds/slayerCharge), again every 2 s only while mEffectTimer + 2 < castTimer (:30696-30712): once at 0.1 s; at castTimer RPC_slayer_fire (:30660, :30784-30795)",
        "cues": [
          [0, "fx", "machineSlayer_eye", {"d": 10, "y": 0.6}]
        ]
      }
    }
  },
  "slayer3": {
    "why": "RPC_slayer :30217-31274 and RPC_slayer_fire :31274-32144: four skills on one coroutine, sLv = the skill (Bug / Tail / Elemental / Machine Slayer, #341-344, each its own cooldown key slayer + sLv :30820), one per play at random on the Slayer host, each its own tile (poolChains); slayer3 from 1.1 s (the 0.1 s cast, :30660; :31749)",
    "skills": {
      "bugSlayer": {
        "why": "bugSlayer: RPC_slayer_fire's start (:31733-31992): PlayAnimation(slayer3, 0.2) (:31749), audio.PlayOneShot(nAttack_bowFx1) (:31761) = Sounds/bow_fire1 (the Chameleon prefab's field 3, checks/fx_chameleon_research/skills_b/probe_fields.txt; a 'sound' cue), fireVector = target bounds centre - hero - 1.5 up, its y clamped to +-0.05 (:31764-31770: rot [2.874, 0, 0]), bugSlayer_fire Instantiated at hero + 1.5 up, LookRotation(fireVector) (:31785-31926; life 1, plays its own Sounds/slayerFire), localScale 1 + 0.1 x Improved Slayer 4 = 1.4 (:31947), the arrow (slot R) hidden (:31953-31972) until 0.85 (:31682-31710); the camera blur left out (:31989); Yield 0.1 (:32022): the hits FindRecTarget(hero + forward, forward, 1.0, 1.0, 36, 10) (:31455-31610) draw nothing; Yield 0.6 (:32028): standby 0.7 (:31642); Yield 0.15 (:32032)",
        "cues": [
          [0, "sound", "bow_fire1"],
          [0, "fx", "bugSlayer_fire", {"y": 1.5, "rot": [2.874, 0, 0], "scale": 1.4}],
          [0, "hideProp", "R", {"kill": 0.85}]
        ]
      },
      "tailSlayer": {
        "why": "tailSlayer: RPC_slayer_fire's start (:31733-31992): PlayAnimation(slayer3, 0.2) (:31749), audio.PlayOneShot(nAttack_bowFx1) (:31761) = Sounds/bow_fire1 (the Chameleon prefab's field 3, checks/fx_chameleon_research/skills_b/probe_fields.txt; a 'sound' cue), fireVector = target bounds centre - hero - 1.5 up, its y clamped to +-0.05 (:31764-31770: rot [2.874, 0, 0]), tailSlayer_fire Instantiated at hero + 1.5 up, LookRotation(fireVector) (:31785-31926; life 1, plays its own Sounds/slayerFire), localScale 1 + 0.1 x Improved Slayer 4 = 1.4 (:31947), the arrow (slot R) hidden (:31953-31972) until 0.85 (:31682-31710); the camera blur left out (:31989); Yield 0.1 (:32022): the hits FindRecTarget(hero + forward, forward, 1.0, 1.0, 36, 10) (:31455-31610) draw nothing; Yield 0.6 (:32028): standby 0.7 (:31642); Yield 0.15 (:32032)",
        "cues": [
          [0, "sound", "bow_fire1"],
          [0, "fx", "tailSlayer_fire", {"y": 1.5, "rot": [2.874, 0, 0], "scale": 1.4}],
          [0, "hideProp", "R", {"kill": 0.85}]
        ]
      },
      "elementalSlayer": {
        "why": "elementalSlayer: RPC_slayer_fire's start (:31733-31992): PlayAnimation(slayer3, 0.2) (:31749), audio.PlayOneShot(nAttack_bowFx1) (:31761) = Sounds/bow_fire1 (the Chameleon prefab's field 3, checks/fx_chameleon_research/skills_b/probe_fields.txt; a 'sound' cue), fireVector = target bounds centre - hero - 1.5 up, its y clamped to +-0.05 (:31764-31770: rot [2.874, 0, 0]), elementalSlayer_fire Instantiated at hero + 1.5 up, LookRotation(fireVector) (:31785-31926; life 1, plays its own Sounds/slayerFire), localScale 1 + 0.1 x Improved Slayer 4 = 1.4 (:31947), the arrow (slot R) hidden (:31953-31972) until 0.85 (:31682-31710); the camera blur left out (:31989); Yield 0.1 (:32022): the hits FindRecTarget(hero + forward, forward, 1.0, 1.0, 36, 10) (:31455-31610) draw nothing; Yield 0.6 (:32028): standby 0.7 (:31642); Yield 0.15 (:32032)",
        "cues": [
          [0, "sound", "bow_fire1"],
          [0, "fx", "elementalSlayer_fire", {"y": 1.5, "rot": [2.874, 0, 0], "scale": 1.4}],
          [0, "hideProp", "R", {"kill": 0.85}]
        ]
      },
      "machineSlayer": {
        "why": "machineSlayer: RPC_slayer_fire's start (:31733-31992): PlayAnimation(slayer3, 0.2) (:31749), audio.PlayOneShot(nAttack_bowFx1) (:31761) = Sounds/bow_fire1 (the Chameleon prefab's field 3, checks/fx_chameleon_research/skills_b/probe_fields.txt; a 'sound' cue), fireVector = target bounds centre - hero - 1.5 up, its y clamped to +-0.05 (:31764-31770: rot [2.874, 0, 0]), machineSlayer_fire Instantiated at hero + 1.5 up, LookRotation(fireVector) (:31785-31926; life 1, plays its own Sounds/slayerFire), localScale 1 + 0.1 x Improved Slayer 4 = 1.4 (:31947), the arrow (slot R) hidden (:31953-31972) until 0.85 (:31682-31710); the camera blur left out (:31989); Yield 0.1 (:32022): the hits FindRecTarget(hero + forward, forward, 1.0, 1.0, 36, 10) (:31455-31610) draw nothing; Yield 0.6 (:32028): standby 0.7 (:31642); Yield 0.15 (:32032)",
        "cues": [
          [0, "sound", "bow_fire1"],
          [0, "fx", "machineSlayer_fire", {"y": 1.5, "rot": [2.874, 0, 0], "scale": 1.4}],
          [0, "hideProp", "R", {"kill": 0.85}]
        ]
      }
    }
  },
  "skinShift": {
    "why": "RPC_skinShift :34709-35336 (Skin Shift #421): PlayAnimation(skinShift, 0) cut (:34987), moveSpeed -3 (the hop back, :34996; no hero mover on the page), voice skinShift1 / skinShift2 (Random.Range(0, 2) :35028-35083), Effects/skinShift_ring Instantiated at the hero, hero rotation (:35096-35114; life 1 + 1, the shed skin skinShift_chameleon StaticMesh in Particles/AdditiveOffset, plays its own Sounds/skinShift), the arrow (slot R) hidden (:35128-35147) until 0.7 (:34854-34889), every non-system status removed (:35155-35215) and 10 % of hp taken (RPC_AddDamage :35229, no effect) at 0; Yield 0.6 (:35261): moveSpeed 0; Yield 0.1 (:35257): standby 0.7 (:34917)",
    "cues": [
      [0, "voice", "skinShift1|skinShift2"],
      [0, "fx", "skinShift_ring"],
      [0, "hideProp", "R", {"kill": 0.7}]
    ]
  },
  "zeroShot": {
    "why": "RPC_zeroShot :36976-37784 (Zero Shot #434): PlayAnimation(zeroShot, 0) cut (:37522), moveSpeed -2 (:37531), voice zeroShot1 / zeroShot2 (Random.Range(0, 2) :37563-37618) and Effects/zeroShot_ring createEffect at the hero, hero rotation (:37631-37647; life 1 + 2, followPosition, its shot lines and ground ring delayed 1.0 / 1.1 s, three BB ParticleSystems: needs that part; plays its own Sounds/zeroShot) at 0; Yield 0.5 (:37689): moveSpeed -1, the camera blur left out (:37134); the pulls toward hero + 2 x forward (FindAreaTarget 6 m, :37441-37490) at 0.5, 0.6, 0.7, 0.8, 0.9 (Yield 0.1 :37679; i < 5 :37338) draw nothing (the 10 m target point (a Penguin-sized body: bounds centre 0.6 m up, height 1, radius 0.3) is out of the 6 m reach); at 1.0: the arrow (slot R) hidden (:37344-37371) until 1.2 (:37218-37255), moveSpeed -6, the hit box FindRecTarget(hero + 0.5 forward, 2, 2, 3, 3) (:37399-37422) draws nothing; Yield 0.2 (:37685); Yield 0.1 (:37681): standby 1.3 (:37286)",
    "cues": [
      [0, "voice", "zeroShot1|zeroShot2"],
      [0, "fx", "zeroShot_ring"],
      [1.0, "hideProp", "R", {"kill": 0.2}]
    ]
  },
  "thunderDragon1": {
    "why": "RPC_thunderDragon :37784-38604 (Thunder Dragon #444; no voice in BB or TTO: neither loads one, TTO1102 Chameleon.<RPC_thunderDragon>d__199::MoveNext pseudo/Chameleon.c:19812-20546): PlayAnimation(thunderDragon1, 0) cut (:38240), blend / invisible removed (:38260-38265), thunderDragon_ring1 createEffect at the hero, hero rotation (:38270-38288; life 3 + 1, followPosition, followState: the actionState stays attack to 3.8 s, after its life, so no cut; its thunderBolt falls from 24 m at 48 m/s with a BoltEmitter to its own BoltTarget; plays its own Sounds/thunderDragon_ring1) at 0; Yield 0.3 (:38491): the camera blur left out (:37939); Yield 0.3 (:38500): at 0.6 myCommand thunderDragon2 (:37981), thunderDragon_ring2 createEffect at the hero, hero rotation (:37986-38004; life 3.2, ends with the standby at 3.8: the dragon skeleton StaticMesh in Self-Illumin/DoubleTexture, two BB ParticleSystems, its looped Sounds/thunderDragon_ring2) and every Renderer under the hero off (:38018-38052) until 3.8 (:38305-38332): the whole hero hidden for 3.2 s; Yield 0.2 (:38487): thunderDragon2 at 0.8 (the SEQ's thunderDragon1@0.8)",
    "cues": [
      [0, "fx", "thunderDragon_ring1"],
      [0.6, "fx", "thunderDragon_ring2"],
      [0.6, "hideProp", "hero", {"kill": 3.2}]
    ]
  },
  "thunderDragon2": {
    "why": "RPC_thunderDragon case 4 (:38065-38096): PlayAnimation(thunderDragon2, 0) cut, Loop at 0 (0.8 s of the skill); six ticks 0.5 s apart (Yield 0.5 :38485, i++ :38155, i >= 6 :38305) at 0, 0.5 ... 2.5: FindAreaTarget(hero, 3, 3) damage and a 12 % paralysis (:38418-38465) on enemies within 3 m: the 10 m target point (a Penguin-sized body: bounds centre 0.6 m up, height 1, radius 0.3) is out of reach, so nothing is drawn (the Bison's convention; Panda/Effects/paralysis, CharacterControl.cs:35443, would show only on a foe in reach); the hero shown again and standby at 3.0 (:38309-38357), the SEQ's thunderDragon2*@3; the reflect (CharacterControl.cs:4618-4627) needs an attacker",
    "cues": []
  },
  "silentWalk": {
    "why": "Silent Walk #411 (passive): RPC_cAttack1 :16112-16841 plays silentWalk (0.2 fade) while the charge is held and the player walks (:16526-16594; another client's copy :16613-16653), so the tile is the walk inside the Charge Attack's charge: from 0.8 s of the charge the Chameleon holds the blend status (RPC_AddStatus blend :16358), drawn on her own team's screens (hers too) as FX/Invisible on every Diffuse renderer, the other renderers off (CharacterControl.cs:32494-32509, :32625-32684): the hero-skin look FX/Invisible (a 'skin' cue, as the Penguin's FX/CosmicRift); the clip has no AnimationEvent (no footsteps, checks/fx_chameleon_research/skills_b/probe_events.txt: only run calls playLeftFootEvent / playRightFootEvent); left out: the charge rings and their timer (the Charge Attack tile's, :16422-16516)",
    "cues": [
      [0, "skin", "FX/Invisible"]
    ]
  }
}
```

## Open questions (each with my recommended answer)

1. **Torment Rain: show the cage it needs, and how long is the tile?**
   - **Recommended:**
     - The finalEntrapment cage at the target point from 0, `{"d": 10, "kill": 2.7}`.
     - Tile `"Torment Rain: rainOfArrow@2.7"`. The rain spawns at 2.0 and its arrows land by about 2.6.
     - Why: the Snow Ball / seal-field precedent of showing the precondition the skill needs. The rain falls into the cage, as in the game.
   - Costs:
     - The cage's 0.9 s drop animation and its own finalEntrapment_hit sound play at each start of the tile.
     - The clip (2.0 s) holds its last pose for 0.7 s.
   - Alternative: no cage cue, keeping the same @2.7 step.
2. **Double Strider ghost: build the mover (P2)?**
   - **Recommended yes.** The game moves the ghost itself, a quarter circle round the target the opposite way. Its five shots are cued from its real spots. Without the mover, the ghost strafes on the spot inside the hero.
   - The same part serves Left Stride with strafe +6 (coordinate with skills_a).
   - Fallback: drop the strafe option and the five ghost shots (the ghost stays at the hero).
3. **Thunder Dragon: hide the whole hero 0.6-3.8 s (`hideProp "hero"`)?**
   - **Recommended yes.** She turns into the dragon skeleton. Without the hide, she stands inside it.
   - Also hide the worn weapon's own effects for those 3.2 s, as the game's Renderer list does.
4. **Silent Walk tile: the FX/Invisible look?**
   - **Recommended yes:** one `skin` cue for the whole tile. Silent Walk is the walk inside the blend-camouflaged charge.
   - Use the same HERO_SKINS entry the Charge Attack / invisibility reports need.
   - If FX/Invisible is not built, leave the entry's cues empty. The fx check would fail on a missing skin.
5. **Skin Shift's shed skin: at the hero, or 1.8 m ahead (where she hops back from it)?**
   - **Recommended at the hero (d 0)**, as spawned. The page has no hero mover (the Wolf's Feral Strike, Penguin decision 8). The overlap lasts only the effect's 1 + 1 s.
6. **Hide the arrow in hand (`hideProp "R"`) on all eight skills?**
   - **Recommended yes.** It is the Cat's P6 part, one cheap cue each, and the arrow visibly leaves her hand in the game.
7. **Quick Fire's 18 hit flashes on the target body (`nAttack_hit` at d 9.7, y 0.63)?**
   - **Recommended yes.** This is the standing enemy-at-target-point rule, and the hit point is the ray's real contact.
8. **Torment Rain's voice: TTO's fix `tormenrRain1|tormenrRain2`, or silent as in BB?**
   - **Recommended TTO's fix** (Sheep decision 10).
9. **runSpeed for the ghost's path:**
   - **Recommended the base 5** (CharacterControl.cs:88), marked APPROXIMATED. Gear that adds speed would widen the circle.
10. **Slayer's eye:**
    - **Recommended once**, at slayer2's 0 (top INT, a 0.1 s cast). With a slow cast it would repeat every 2 s.
11. **The empty `thunderDragon2` entry:**
    - **Recommended keep** for its `why`. Drop it if the editor's check objects to an entry with no cues.

## Offered to the user for the Bible (not written there)

- Quick Fire's clip timing:
  - quickFire2 starts at 0.6 s, not 0.4 (the opening shot at 0.4, its ray at 0.5).
  - The closing shot and quickFire3 come at 2.3, not 0.4 + 0.1 x (1 + loop shots).
  - Hits land 0.1 s after each shot; standby is at 2.7.
- Torment Rain:
  - Silent in BB: the voice files are named tormenrRain1/2; TTO loads the right names.
  - Timeline: ring at 0.9, rain at 2.0, hits at 2.2, standby at 2.1.
- Thunder Dragon:
  - No voice in BB or TTO.
  - The hero is hidden 0.6-3.8 s, and the skeleton ring at 0.6.
- Slayer:
  - slayer2 starts at a fixed 1.0 s.
  - The eye on the target repeats every 2 s of cast.
  - The fire is at 1.5 m with its pitch clamped to ±0.05.
  - The fire's scale is 1 + 0.1 x Improved Slayer.
- Right Stride's Double Strider ghost:
  - It circles the target the other way at runSpeed + 1, facing it.
  - Its shots fire from TransformDirection(-0.38, 1.2, 1).
- Zero Shot's timeline: pulls at 0.5-0.9 s, the shot at 1.0, standby at 1.3, about 2.6 m of hop back.
- Skin Shift's standby is at 0.7, with the 1.8 m hop back.
- Poison Volley:
  - 0.3 s arrow hide, root crossfade at 0.5, standby at 0.7.
  - poison draws nothing on the target.

## Verification

(Written by the checker against the researcher's draft `checks/fx_chameleon_research/skills_b/cues_block.json` while this file was missing: the researcher's Write was refused and its report came back as text; saved here by the lead, 2026-11-13. The corrections below win.)

**Confirmed against the source:**
- **quickFire:**
  - Shot at 0.4 s, hit at 0.5 s, quickFire2 starting at 0.6 s. index.html says 0.4, so it changes to `quickFire1@0.6`.
  - 16 loop shots at 0–1.5 s with hits at 0.1–1.6 s, then quickFire3 at 1.7 s.
  - The hit at d 9.7 / y 0.63, the pitch of 5.711° and the arrow hidden until 2.7 s.
- **poisonVolley:** the 0.3 / 0.5 / 0.7 s times.
- **rainOfArrow:**
  - Times: the ring at 0.9 s, the hide at 1.2 s, the fire at 2.0 s, standby at 2.1 s.
  - Voice: `tormenrRain1|2` is right. The rip only has the misspelled files and TTO loads them (pseudo/Chameleon.c:20602-20604).
- **rightStride:**
  - Shots at 0.366, 0.799, 1.232, 1.665 and 2.098 s, then standby at 2.298 s.
  - Sounds: fire1 on even shots, fire2 on odd.
  - The hero's arrows at `[3.81,-2.545,0]`.
  - My own simulation reproduces every clone spot at 6 m/s.
- **slayer:**
  - slayer2 at 1.0 s, cast 0.1 s; the eye at d 10 / y 0.6.
  - The fire pitch of 2.874°: the direction is normalized and then its y is clamped to ±0.05 (:31764-31767).
  - Scale 1.4.
- **skinShift and zeroShot:** times confirmed.
- **thunderDragon:**
  - ring1 at 0, ring2 and the whole hero hidden at 0.6 s, thunderDragon2 at 0.8 s.
  - Six ticks; the hero shows again at 3.0 s. No voice exists in BB or TTO.

**Corrections:**
1. **Every `hideProp "R"` must be `"L"`.** That covers quickFire1, poisonVolley, rainOfArrow, rightStride, slayer3 (all 4 members), skinShift and zeroShot. The game hides `mWep2`, which is the arrow: ChameleonEquipment.cs:1646 / 1682 / 1715, `getWeapon(code, 2)`. On the page, R is the bow and L is the arrow (index.html:1512 and 1044-1047; skills_a item 5 and attacks_emotes agree). Paste-ready:
   - `[0.4, "hideProp", "L", {"kill": 2.3}]`
   - `[0.3, "hideProp", "L", {"kill": 0.4}]`
   - `[1.2, "hideProp", "L", {"kill": 0.9}]`
   - `[0.366, "hideProp", "L", {"kill": 1.932}]`
   - `[0, "hideProp", "L", {"kill": 0.85}]` (×4)
   - `[0, "hideProp", "L", {"kill": 0.7}]`
   - `[1.0, "hideProp", "L", {"kill": 0.2}]`
2. **silentWalk: `[0, "skin", "FX/Blend"]`, not FX/Invisible.** The draft cites CharacterControl.cs:32494-32684, but those lines are the `invisible` status. The charge gives `RPC_AddStatus("blend", ...)` (Chameleon.cs:16358). Blend draws FX/Blend on the player's own team's screens (CharacterControl.cs:36665-36880, the material at :36880) and FX/Camaflage for enemies (:36770).
3. **thunderDragon1 needs a part.** `[0.6, "hideProp", "hero", {"kill": 3.2}]` is a format parts.md doesn't have: its hideProp only takes prop slots (parts.md:483). The source is right: every Renderer under the hero goes off (Chameleon.cs:38018-38052, back on at :38305-38332). hideProp needs a `"hero"` target wired to the page's `heroHide` / `LOOK.hides` (index.html:4509).
4. **Clone speed differs from skills_a.** The draft's `strafe -6` uses CharacterControl.cs:88's runSpeed of 5. That value is overwritten on load with `0.01 × (400 + 2·AGI − 4·weight)` (CharacterDataClass.cs:979, CharacterControl.cs:1458), which is 4.02 at the page's stats. skills_a uses 5.02 for Left Stride, so one rule is needed for both.
   - At 5.02, the cue becomes `[0, "fx", "doubleStrider_right", {"cut": 2.298, "strafe": -5.02, "to": [0, 0, 10]}]`.
   - The clone's shots at 5.02 (y 1.2):

     | Time | x | d | rot |
     |---|---|---|---|
     | 0.366 | -2.081 | 1.226 | [3.807, 13.34, 0] |
     | 0.799 | -3.872 | 1.844 | [3.802, 25.399, 0] |
     | 1.232 | -5.567 | 2.879 | [3.798, 38.019, 0] |
     | 1.665 | -6.996 | 4.259 | [3.793, 50.625, 0] |
     | 2.098 | -8.048 | 5.837 | [3.789, 62.645, 0] |

   - The draft's own cues are right at 6 m/s.

Files are in D:/12tails-wardrobe/checks/fx_chameleon_research/verify_b_eo/:
- pred.py
- stride.py
- stride502.py
- probe_crit.json
- flow_RPC_*.txt
