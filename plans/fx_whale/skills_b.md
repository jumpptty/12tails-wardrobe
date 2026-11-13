SUMMARY: 8 skills across 10 clips: Shield Bash, Sweep, Javelin, Shield Rush, Swallow, Peninsula Impale, Peninsula Round, Grand Tide, plus Whale Wave / Mal Storm (they play the `malStorm` clip only without Diving Press). 9 paste-ready entries with 99 cues.
- `malStorm` is a lower-rank clip: with Diving Press #443 (passives on) Whale Wave plays `divingWave` and Mal Storm plays `divingStorm` (Whale.cs:32111-32125, :32775-32789). Recommended `LOWER_RANK.whale = ["malStorm"]`; their cues belong on skills_a's diving clips.
- No SEQ change: the one sequence in scope, `"Grand Tide: grandTide1 grandTide2*@3 grandTide0"`, matches the code (grandTide2 cut in at 2.0 s).
- Only Peninsula Impale reaches the 10 m target (the 12 m Asunder box): 10 stabs 0.3 s apart, each hit a 40 % Wall Puncture roll (wallPuncture_hit, else nAttack_hit).
- Four page parts are needed:
  - `Whale_javelin`: the thrown lance, a copy of the worn slot-R piece on a 24 m/s ballistic path that sticks in the ground.
  - `fx:grandTide`: the hero's code playing the wave's create / root / destroy clips across three steps.
  - The Shuriken graft for `grandTide`'s two BB ParticleSystems (`SHURIKEN_FROM_TTO["whale"]`).
  - A cue option `boneAt`, a spawn at a bone's world pose that is not parented, plus a rot element `[lo, hi]` drawn per play: Peninsula Round's 28 slash rings.
- One timing for the Bible: Peninsula Impale's stabs are 0.3 s apart, not 0.2 s.

=====================================================================

# Whale effects + sounds research: Shield Bash, Sweep, Javelin, Shield Rush, Swallow, Peninsula Impale, Peninsula Round, Grand Tide, Mal Storm / Whale Wave (skills_b)

Researcher `skills_b`, 2026-11-13 (office PC).

**Scope.** The clips `grandTide1`, `grandTide2`, `javelin`, `malStorm`, `peninsulaImpale`, `peninsulaRound`, `shieldBash`, `shieldRush`, `swallow` and `sweep`, and every skill that plays them. This is research only (recipe steps 1-3).

**Conventions.**
- Line numbers are `C:\Users\Jump\Desktop\12tails\DecompiledSource\Whale.cs` (home: `D:\12tails\...`) unless another file is named.
- Times are seconds from the start of the clip the entry is keyed by.
- Distance 0 = at the hero.
- Max rank, passives on (the Wolf's / Sheep's / Penguin's / Bat's decisions; every skill learned, the Chameleon's Double Strider and the Monkey's Damage Cast by analogy):
  - Sweep 2 + Tide Cutter #402
  - Javelin 2
  - Shield Rush 2
  - Swallow 2 + Gobble Up #233 (the catch needs it) + Wonder Belly #432
  - Peninsula Impale 2 and Peninsula Round 2 + Peninsula Asunder #442
  - Wall Puncture 4
  - Shield Bash #114
  - Whale Wave / Mal Storm + Diving Press #443
  - Grand Tide (single rank)
- The target is the standing 10 m target point, a Penguin-sized body: CharacterController height 1, radius 0.3, centre 0.6 m up (Bat decision 4).
- Random procs at LCK 1 (the Wolf's Double Art convention, Cat decisions 40 / 41): lckAdjust(40) = floor(100 x 40.4 / 100.4) = 40, and `Random.Range(0, 100) < 40` = **p 0.4**.
- The Whale's body as the page draws her: the prefab's `Whale_tri` scale 1, CharacterController height 2.4, radius 0.8, centre 1.3 (body.py). This is the n = 4 size of Game.cs:2795-2825 (`0.8 + 0.05 n`, `centre 1.1 + 0.05 n`). With passives on the game's n is 5 (Super Size 4 + Mega Size); see effect_only.md open question 5.

**Read-only probes and scripts**, all in `checks\fx_whale_research\skills_b\` (git-ignored):
- `clean.py` is the Monkey's / Bat's: it prints a .cs range with the opaque predicates worked out (`!!TRUE` marks a true one; false blocks are dropped). `F.sh` / `brief.sh` filter it.
- `clean_RPC_<name>.txt` holds every coroutine in scope: shieldBash, sweep, javelin, shieldRush, swallow, peninsulaImpale, peninsulaRound, whaleWave, malStorm, grandTide, grandTide0. `classes_all.txt` lists the coroutine classes and their lines.
- `probe.json` + `probe_summary.txt`: `wardrobe_fx.py whale --probe` on 22 effects. probe.err is empty; `javelin_hit` is not in the rip (KeyError). `summarize.py` makes the summary.
- `rb.py`: the javelin prefab's Rigidbody (mass 1, drag 0, **useGravity true**), its BoxCollider (trigger, 0.25 x 0.25 x 3, centre z 0.5), and the PhysicsManager gravity (0, -9.8, 0).
- `body.py`: the Whale prefab's Whale_tri scale and CharacterController.
- `javelin_sim.py` + `javelin_sim.txt`: the javelin's aim (getTrajectoryVector, worked out from Math.cs) and its flight.
- `tto_probe_grandTide.json`: `wardrobe_fx_tto.py whale --probe grandTide`. TTO's copy has both ParticleSystems decoded (tto_Water2 at z 2, tto_Splash3 at z -3.5).
- `tto\<name>.asm`: TTO1102 MoveNext disassembly (the tto researcher's dis.py), read for the `Waits.Get` arguments.
- `cues.py` -> `cues_block.json`; `cues_fmt.json` is the block below, checked as JSON.

## Read this first

### 1. `malStorm` is a lower-rank clip (passives on: Diving Press)

- Two skills play it, and both swap it out when Diving Press #443 is learned:
  - RPC_whaleWave: `if (hasSkill(443)) PlayAnimation("divingWave", 0.2) else PlayAnimation("malStorm", 0.2)` (:32111-32125).
  - RPC_malStorm: the same with `divingStorm` (:32775-32789).
- TTO keeps the swap: `divingStorm` is a string of `Whale.<RPC_malStorm>d__201::MoveNext` (TTO1102 pseudo/Whale.c:10883), and `divingWave` one of RPC_whaleWave's (:21470).
- **Recommended:** `LOWER_RANK.whale = ["malStorm"]` (the Monkey's decision 6, cast1 / cast2 under Damage Cast). No cue entry for `malStorm`. The Whale Wave and Mal Storm tiles are skills_a's `divingWave` / `divingStorm`.
- **Icons:** the hd index has `malStorm` on the `malStorm` clip. The diving clips need `CLIP_SKILLS["whale"] = {"divingWave": ["whaleWave"], "divingStorm": ["malStorm"]}` in wardrobe_skill_icons.py (for skills_a / the lead to confirm).
- For the record, the passive-off timelines:
  - Mal Storm: voice malStorm1|2 at 0. At 0.7 `malStorm` at the hero (life 3) and a hit (:32480-32492, :32686). Then `createMalstormBolt` at 0.8 / 0.9 / 1.0 per round (:32532-32586), four rounds 0.3 s apart (`i < 4` :32663), and standby at 2.0.
  - Whale Wave: `whaleWave` at the hero at 0.7, standby at 1.0 (:31900-31912, :32245-32255).

### 2. Peninsula Impale: 10 stabs 0.3 s apart, and the only reach in scope

- Each stab is `asunderImpale` at the hero, then `Yield(3, 0.2)` (:27433), then the hit, then `Yield(4, 0.1)` (:27447), then `i++`.
- So the stabs are at 0.8 + 0.3 k and the hits at 1.0 + 0.3 k, for k = 0 ... 9 (`i < 2 + 4 x sLv` :27076). Standby is at 3.8.
- The Bible's movement table says "a hit every 0.2 s" (+0.4 m each). The code gives 0.3 s (+0.6 m at 2 m/s). Offered for the Bible.
- With Asunder the hit box is 12 m long (`FindRecTarget(pos, fwd, 1.5, 1.5, 12, 3)` :26830), so every hit lands on the 10 m target. The hit point is `vFlat(target centre) + (0, hero y + 1, 0)`, which is d 10, y 1.
- Each stab makes one Wall Puncture roll (:26844):
  - p 0.4: `wallPuncture_hit` + Sounds/wallPuncture_hit.
  - Otherwise: `nAttack_hit` + Sounds/nAttack_hit.
  - Both sounds are the hero's PlayOneShot (:8303-8354, :9247-9288), so they are `"sound"` cues. Paired rolls `impaleWp<k>` / `!impaleWp<k>` (the KO tile's `!name` convention).

### 3. Javelin is the worn lance, thrown

- `Whale_javelin.Init` instantiates `mChar.mWep2` (the lance: getWeapon(code, 1) on mount_Hand_R, WhaleEquipment.cs:1631-1710) under the projectile at local identity, with every renderer on (Whale_javelin.cs:82-118).
- The lance in hand has its MeshRenderers off from 0.5 to 1.0 (:22985-23017, :23049-23110). This is the Cat's `hideProp` (built), slot R, with no `all`: only MeshRenderers go off.
- The flight:
  - It starts at the cast spot + TransformDirection(1.2, 2.2, 1) (:22919), aimed by `Math.getTrajectoryVector(firePos, target centre, 24)` (Math.cs:885-1006).
  - Velocity is TransformDirection(0, 0, 24) (Whale_javelin.cs:25, :50), with gravity on.
  - The nose follows the velocity (:165).
  - On terrain contact it sticks: gravity off, velocity eased to 0 (:174, :191-198).
  - It is destroyed at life 3 (ProjectileControl.life = 3 x rangeMod :8803; Whale_javelin.cs:150-154).
- javelin_sim.txt:
  - The aim is rot [2.878, -7.595, 0].
  - It passes the target at 0.38 s (y 1.0, inside the body).
  - It sticks at 0.46 s about 11.9 m ahead, 13.4 deg nose down.
  - It rests at (x -0.33, y 0.44, d 12.44).
- It pierces and hits in flight (OnTriggerStay), but **nothing is drawn**:
  - RPC_javelin_hit has no local caller (:4213 is the remote ActionEvent dispatch).
  - `javelin_hit` is not in the rip.
  - Javelin's Wall Puncture proc there only deals damage (Whale_javelin.cs:276-304), so effect_only's "p 0.4 roll beside Javelin" does not apply.
- This needs the **Whale_javelin part** (P1).

### 4. Grand Tide's wave spans three steps

- `grandTide` is made at grandTide1's 1.0 (:37436) and plays `create` (:37449). `root` loops from grandTide2's start (:37509).
- It is ended by EffectControl's followState when myCommand becomes `grandTide0` (RPC_grandTide0 :38176; EffectControl.cs:226-291 plays `destroy` and the 1 s after-life).
- The page's `cut` is read on the playing step's clock, and a cut past a step is left for later steps (index.html fxStart, :5369-5380). So no `cut` value can say "at grandTide0's start" from a grandTide1 cue.
- The Cat's `fx:grandCasinoArcade` solved the same thing: the part plays the cue's `anims` and sets `fx.cutAt = -Infinity` at its own end age. So this needs the **fx:grandTide part** (P2):
  - `anims [[1.0, "root"]]`
  - `end 4.0` = grandTide1's 2.0 - 1.0 + grandTide2's @3
- Its two BB ParticleSystems need the **Shuriken graft** (P3).

### 5. Swallow catches only with Gobble Up, and the catch is 1 m ahead

- Swallow's coroutine:
  - 1 s wind-up, then 9 pulls at 1.0 ... 1.8 (Bible).
  - At 1.9 the catch, only with Gobble Up #233 (`hasSkill(233)` :25705; the Bible says so too).
  - The catch spawns `swallow_hit` at the target's bounds centre (:9030).
- The pulls drag the locked target toward hero + forward (:25885), and the grab box is 2 m (:25726). So the catch happens 0-2 m ahead.
- Cue: `{"d": 1, "y": 0.6}`, marked APPROXIMATED (Open question 2).

### 6. The page parts this scope needs

No cue can do these.

- **P1 `Whale_javelin`** (the inventory's "needs Whale_javelin"; fxparts/whale.js, the Cat_supportFire precedent in fxparts/cat.js):
  - The model: `api.propModel(at.slot || "R")` (the Chameleon's arrow hook) parented at the root, local identity. With nothing worn, the Whale's starter lance (Open question 9).
  - The motion:
    - At the spawn: v = root forward x 24.
    - Each 0.02 s step: v.y -= 9.8 x 0.02, then pos += v x 0.02, and the root faces along v.
  - The stick:
    - The test: the trigger box's lowest corner (z -1 ... 2 along the nose, half height 0.125) at or below the floor y 0.
    - After it: no gravity, no more turning, and v = v x (1 - 0.48) each step (Lerp(v, 0, 24 dt)).
  - Gone at age 3.
  - The part under the floor: clipped as index.html does for moving children (the game's terrain hides it).
  - The data: `LAYOUTS["Whale_javelin"] = []` (no serialized fields; the speed is the ctor's (0, 0, 24)).
  - Without the part, the effect is a lone AudioSource with no mesh.
- **P2 `fx:grandTide`** (fxparts/whale.js, the cat.js GCA pattern):
  - Plays the cue's `anims` on the root Animation as each age passes. `root` is Loop (the data's wrap 2).
  - At `end` it sets `fx.cutAt = -Infinity`. The page's own followState end then plays `destroy` and the 1 s after-life, so the wave is gone at age 5.0, the end of grandTide0's 1 s clip.
  - After an earlier end (`fx.stopped`, a new pick) nothing more plays.
- **P3 the Shuriken graft for `grandTide`**:
  - `SHURIKEN_FROM_TTO["whale"] = ["grandTide"]` in wardrobe_fx.py, by the Chameleon's route.
  - Two nodes named "ParticleSystem", matched by their renderers' first materials. TTO's are tto_Water2 and tto_Splash3, so BB's should be Water2 / Splash3; the parts agent confirms BB's names.
  - Without it the wave's spray and splash are skipped without a word.
- **P4 cue option `boneAt` + a per-play rot element** (index.html, cueOf / Fx):
  - `"boneAt": bone` spawns the effect once at that hero bone's world position and rotation (the `bone` option's mirror math, run once at the spawn), then leaves it in the world: Unity's `Instantiate(prefab, bone.position, bone.rotation x Euler(rot))`. `rot` then counts after the bone's rotation, as `bone` + `rot` does (boneRot).
  - A rot element `[lo, hi]` is a whole number drawn per play (Unity's int Random.Range, top left out): `[0, 0, [-30, 29]]`.
  - Peninsula Round's 28 `asunderRound` rings at mount_Hand_R (:28025) need both.
  - Until it is built, rotOf passes the nested array on as it is, so the placement gets NaN. Do not paste the peninsulaRound entry before P4.
- Already built and used here:
  - `hideProp` (the Cat's P6)
  - `"sound"` cues
  - `p` / `roll` / `!roll`
  - `cut`
  - x / y / d / rot
  - Ring / Line / Image emitters and legacy particles
  - StaticMesh + Animation (the wave's meshes; mesh.js play())
  - EffectControl followPosition / followState

## The skills, at a glance

| Skill (clip) | Voice | Effects | Standby | Needs |
|---|---|---|---|---|
| Shield Bash (shieldBash; passive #114, a charge release after 3 s or more) | shieldBash1/2 at 0 | shieldBash_ring at the hero at 0.2 (the 3 m hits miss the target) | 0.6 | - |
| Sweep (sweep, Tide Cutter on) | tideCutter1/2 at 0 | tideCutter_ring at 0 (cut 1.6); Sounds/sweep at 1.0 (the 6 / 5 m hits miss) | 1.6 | - |
| Javelin (javelin) | javelin1/2 at 0 | the thrown lance at 0.5; the lance in hand hidden 0.5-1.0 | 1.0 | Whale_javelin (P1) |
| Shield Rush (shieldRush) | shieldRush1/2 at 0 | shieldRush_ring at the body centre (y 1.3) at 0.2 (the 2 m box misses) | 0.6 | - |
| Swallow (swallow) | swallow1/2 at 0 | swallow_ring at 0 (cut 2.9); Sounds/swallow at 1.0; swallow_hit at d 1 at 1.9 | 2.9 | - |
| Peninsula Impale (peninsulaImpale, Asunder on) | peninsulaImpale1/2 at 0 | peninsulaImpale_ring at 0; 10 x asunderImpale at 0.8 + 0.3 k; 10 hits at d 10 / y 1: wallPuncture_hit (p 0.4) or nAttack_hit, with their sounds | 3.8 | - |
| Peninsula Round (peninsulaRound, Asunder on) | peninsulaRound1/2 at 0 | peninsulaRound_ring at 0 (cut 4.0); 28 x asunderRound at mount_Hand_R, 1.0 ... 3.7 (the 4 m hits miss) | 4.0 | boneAt + rot range (P4) |
| Grand Tide (grandTide1 > grandTide2* > grandTide0) | grandTide1/2 at 0 | grandTide_ring at 0; the wave at 1.0 (create, root from 2.0, destroy at grandTide0) | grandTide0's 0.8 | fx:grandTide (P2), Shuriken (P3) |
| Whale Wave / Mal Storm (malStorm) | - | not played with Diving Press (item 1) | - | LOWER_RANK |

## Per clip: the timelines

Every coroutine here has the same frame. `default` (time 0):
- sets actionState attack, myCommand and the cooldown
- sets the hero's spot and facing
- plays the clip and sets moveSpeed
- plays the voice `Random.Range(0, 2)`: only with the pvoice setting on, for others only in the same team, at 0.75 volume
- spawns the first effect

The camera effects (motion blur, shakes, WallPuncture screen message) are left out, as the Wolf's and the Penguin's were. They are at Sweep :21887 / :22136, Peninsula Impale :26962, Peninsula Round :27713 and Mal Storm :32468.

None of these hops or dashes is on the page: there is no hero mover (Penguin decision 8). The Bible's movement table gives the game's distances.

### Shield Bash (RPC_shieldBash :19653-20229)

- **The trigger** (doReleaseCharge :8486-8570): the Charge Attack (#111) released 3 s or more after its press (`actionTime + 3 <= Time.time` :8557), with #114 and `Game.mGameType > 4` (combat maps).
- **0:** `PlayAnimation("shieldBash", 0.2)` (:20040), moveSpeed 0, voice shieldBash1|shieldBash2 (:20081-20171).
- **0.2** (`Yield(2, 0.2)` :20176):
  - moveSpeed 2 (:19800).
  - shieldBash_ring createEffect at the hero, hero rotation (:19811-19823): life 1, no follow, its own Sounds/shieldBash_ring.
  - The hits: FindAreaTarget(hero, 3, 3) (:19850), each with RPC_shieldBash_hit at the foe (:19909; Instantiate at the hit point :8698). Out of reach.
- **0.4** (`Yield(3, 0.2)` :20174): moveSpeed 0.
- **0.6** (`Yield(4, 0.2)` :20161): standby (:19973).

### Sweep (RPC_sweep :21464-22728)

- **0:**
  - `PlayAnimation("sweep", 0.2)` (:22287), moveSpeed -0.5 (:22296).
  - With Tide Cutter #402: tideCutter_ring createEffect at the hero (:22299-22321): life 2, followPosition, followState. Voice tideCutter1|tideCutter2 (:22364-22405).
  - Without it: sweep_ring and sweep1|sweep2 (:22432-22534).
- **0.2** (`Yield(2, 0.2)` :22621): moveSpeed -0.3.
- **0.5** (`Yield(3, 0.3)` :22601): moveSpeed 0.
- **1.0** (`Yield(4, 0.5)` :22572): moveSpeed 9; Sounds/sweep PlayOneShot (:21676-21688).
- **1.1** (`Yield(5, 0.1)` :22599): moveSpeed 6. Hit 1: FindAreaTarget(hero, 6, 3) (:21743), one Wall Puncture roll (:21763): wallPuncture_hit (:21839) or nAttack_hit (:21930). Out of reach.
- **1.4** (`Yield(6, 0.3)` :22580): moveSpeed 0. Hit 2: FindAreaTarget(hero, 5, 3) (:21992), the same pair (:22088, :22179). Out of reach.
- **1.6** (`Yield(7, 0.2)` :22615): standby (:22217). This is tideCutter_ring's cut.

### Javelin (RPC_javelin :22728-23422; RPC_javelin_fire :8768-8831; Whale_javelin.cs)

- **0:** `animation.Rewind()`, `PlayAnimation("javelin", 0.2)` (:23197-23200), moveSpeed 0, voice javelin1|javelin2 (:23241-23336).
- **0.4** (`Yield(2, 0.4)` :23318): moveSpeed 2 (:22886).
- **0.5** (`Yield(3, 0.1)` :23324):
  - firePos and fireDir as in item 3 (:22919-22966). With no target it aims at cast spot + 20 x forward (:22961); the tile uses the target point.
  - RPC_javelin_fire (:22967) Instantiates `javelin` with `LookRotation(fireDir)` (:8791-8794). It sets life = 3 x rangeMod (:8803) and calls `Whale_javelin.Init(owner, sLv)` (:8809).
  - The lance in hand: `mWep2.GetComponentsInChildren(MeshRenderer)` off (:22985-23017).
- **0.6** (`Yield(4, 0.1)` :23322): moveSpeed 0.
- **1.0** (`Yield(5, 0.4)` :23328): the lance's MeshRenderers on again (:23083-23110); standby (:23127).
- The projectile:
  - Its AudioSource `javelin` plays on awake.
  - Its flight, stick and life are in item 3.
  - Its root has no EffectControl (ProjectileControl + Whale_javelin + AudioSource; Rigidbody and a trigger BoxCollider, rb.py).

### Shield Rush (RPC_shieldRush :24032-24642)

- **0:** `PlayAnimation("shieldRush", 0.2)` (:24445), moveSpeed 0, voice shieldRush1|shieldRush2 (:24486-24579).
- **0.2** (`Yield(2, 0.2)` :24572):
  - moveSpeed 6 x sLv = 12 (:24179).
  - shieldRush_ring createEffect at `collider.bounds.center`, hero rotation (:24190-24202): life 1, followPosition, its own Sounds/shieldRush. Its ring sits 1 m ahead of that centre (its node at z 1).
  - y 1.3 is the page body's centre (Open question 6).
- **0.3** (`Yield(3, 0.1)` :24562): the hit box FindRecTarget(hero, fwd, 1, 1, 2, 3) (:24252), each with RPC_shieldRush_hit at the foe (:24311). Out of reach.
- **0.4** (`Yield(4, 0.1)` :24585): moveSpeed 0.
- **0.6** (`Yield(5, 0.2)` :24583): standby (:24375).

### Swallow (RPC_swallow :25218-26006)

- **0:**
  - `PlayAnimation("swallow", 0.2)` (:25543), moveSpeed 0, voice swallow1|swallow2 (:25592-25647).
  - swallow_ring createEffect at the hero (:25666-25678): life 3, followPosition, followState.
- **1.0** (`Yield(2, 1)` :25931):
  - Sounds/swallow PlayOneShot (:25382-25394).
  - The locked target (:25408-25414).
  - The first pull: `RPC_AddDamage(230 + sLv, -1, 0, 0, force)` with force = hero + forward - target, as (sLv + Wonder Belly) = 3 x unit when farther than 1 m (:25885-25912).
- **1.1 ... 1.8**: the next 8 pulls (`Yield(3, 0.1)` :25935, i++ :25451, `i >= 9` :25695). Nothing is drawn.
- **1.9:** the catch (Gobble Up #233 :25705):
  - The target must be inside FindRecTarget(hero, fwd, 1, 1, 2, 3) on its layer (:25726).
  - The Whale's collider must be taller than the target's (:25766-25776).
  - Then RPC_swallow_hit(target position, hero forward) (:25791): `swallow_hit` Instantiated at the target's `collider.bounds.center`, `LookRotation(hero forward)` (:9020-9030). Life 1, no AudioSource.
  - Then `swallow` on the target, `gobble` on the Whale, 15 s at equal CHA with Wonder Belly (:25811-25839).
  - The swallowed target's renderers go off (CharacterControl.cs:35573-35660). Not drawn: the page has no target body.
- **2.9** (`Yield(4, 1)` :25927): standby (:25478). This is swallow_ring's cut; the 2.8 s clip ends first, and the ring's own life 3 is 0.1 s later.

### Peninsula Impale (RPC_peninsulaImpale :26574-27523)

- **0:**
  - `PlayAnimation("peninsulaImpale", 0.2)` (:27274), moveSpeed 0, voice peninsulaImpale1|peninsulaImpale2 (:27315-27370).
  - peninsulaImpale_ring createEffect at the hero (:27389-27399): life 2, followPosition + followState. The standby at 3.8 comes after its life, so no cut. Its own Sounds/peninsular.
- **0.8** (`Yield(2, 0.8)` :27435):
  - moveSpeed 3 (:26732).
  - With #442, the locked target is read (:26762-26785). i = 0.
  - The first stab (IL_F28 :27076): with #442 `asunderImpale` Instantiated at the hero, hero rotation (:27157-27169): life 1, no follow, its own Sounds/impale. Without #442 it is `peninsulaImpale` (:27219-27231).
  - Then LookAt the target on the flat (:27199).
- **+0.2** (`Yield(3, 0.2)` :27433): moveSpeed 2, the hit with its Wall Puncture roll (item 2; :26813-27031).
- **+0.3** (`Yield(4, 0.1)` :27447): i++ (:27249), the next stab.
- Stabs at 0.8, 1.1 ... 3.5; hits at 1.0, 1.3 ... 3.7.
- **3.8:** i = 10: moveSpeed 0, standby (:27082-27099).

### Peninsula Round (RPC_peninsulaRound :27523-28262)

- **0:**
  - `PlayAnimation("peninsulaRound", 0.2)` (:27834), moveSpeed 0, voice peninsulaRound1|peninsulaRound2 (:27883-27938).
  - peninsulaRound_ring createEffect at the hero (:27957-27969): life 4, followPosition + followState, a looped Sounds/peninsularRound.
- **0.8** (`Yield(2, 0.8)` :28191): moveSpeed 3 (:27670).
- **1.0** (`Yield(3, 0.2)` :28189): moveSpeed 0; mHandMount = `mount_Hand_R` (:27719); i = 0.
- **Every 0.1 s** from 1.0 while i < 28 (:27986, `Yield(4, 0.1)` :28201, i++ :27733):
  - With #442 `asunderRound` Instantiated at the hand mount's world position, `rotation x Euler(0, 0, Random.Range(-30, 30))` (:28013-28025): life 1, no AudioSource, not parented. Without #442 it is `peninsulaRound` (:28048-28060).
  - On `i % 4 == 0` the hits: FindRecTarget(hero - fwd, fwd, 3, 3, 5, 3) (:28099), with RPC_nAttack_hit (:28155). Out of reach. That is 7 hits, at 1.0, 1.4 ... 3.4 (the Bible).
- **3.8:** i = 28: `Yield(5, 0.2)` (:28193).
- **4.0:** standby (:27752). This is peninsulaRound_ring's cut, and also its life.

### Grand Tide (RPC_grandTide :37257-38002, RPC_grandTide0 :38002-38233; grandTide1 > grandTide2 held > grandTide0)

- **grandTide1, 0:**
  - `PlayAnimation("grandTide1", 0.2)` (:37781), moveSpeed 0, voice grandTide1|grandTide2 (:37822-37877).
  - grandTide_ring createEffect at the hero (:37896-37906): life 3 + 1, followPosition + followState, its own Sounds/grandTide_ring. myCommand stays grandTide past its life, so no cut.
- **grandTide1, 1.0** (`Yield(2, 1)` :37936):
  - moveSpeed 2; collisions with everyone within 400 m ignored (:37398-37408, the Bible's "not a hit area").
  - `grandTide` createEffect at the hero (:37424-37436), with `animation.Play("create")` Once (:37449-37454):
    - life 99 + 1, followPosition, followState
    - a looped Sounds/grandTide
    - five `grandTide_tri` StaticMeshes 4.8 m down that the create clip raises
    - two BB ParticleSystems
- **grandTide2, 0 = 2.0** (`Yield(3, 1)` :37939):
  - `PlayAnimation("grandTide2", 0)` cut, Loop (:37488-37493); moveSpeed 3 (:37498).
  - The wave: `animation.Play("root")` Loop (:37509-37514).
  - Then every FixedUpdate (`Yield(4, WaitForFixedUpdate)` :37933) until the player moves or MP < 10 / SP < 20 (:37566-37601):
    - once a second (:37604-37612) SP -10 (Revised Skill #404), MP -8 (Revised Magic #414)
    - `hit(444)` on FindRecTarget(hero - 4 fwd, fwd, 8, 8, 7, 4) (:37632-37655), 4 m behind to 3 m ahead
    - hit() draws nothing, and the target is out of reach anyway
  - The SEQ's `grandTide2*@3` is the three-hit rule for a channel the player ends.
- **grandTide0, 0 = 5.0:**
  - RPC_grandTide0 (:37674): myCommand grandTide0, `PlayAnimation("grandTide0", 0)` cut, moveSpeed 2 (:38170-38188).
  - Back in RPC_grandTide: the wave plays `destroy` (:37706). EffectControl's followState end does the same and starts the 1 s after-life (EffectControl.cs:226-291).
  - At grandTide0's 0.8 (`Yield(2, 0.8)` :38204): standby (:38115). grandTide0's cues are not in this scope.

## Buildability (inventory + probe)

| Effect | Loaded at | Probe | Status |
|---|---|---|---|
| shieldBash_ring | :19811 | EC 1, legacy particles (Smoke1) + Ring (Dust5), own sound | ready |
| tideCutter_ring | :22309 | EC 2 fPos fState, 2 Line + Ring | ready |
| sweep_ring (without #402) | :22438 | EC 2 fPos fState, Ring | ready (not cued) |
| javelin | :8781 | ProjectileControl, Whale_javelin, AudioSource; Rigidbody (gravity), BoxCollider trigger (rb.py); no mesh of its own | needs Whale_javelin (P1) |
| shieldRush_ring | :24190 | EC 1 fPos, Ring at z 1, own sound | ready |
| swallow_ring | :25666 | EC 3 fPos fState, 2 Line (Smoke1_small) | ready |
| swallow_hit | :9020 | EC 1, Image + legacy particles | ready |
| peninsulaImpale_ring | :27389 | EC 2 fPos fState, Image / Line / Ring, own sound | ready |
| asunderImpale | :27157 | EC 1, Ring + 2 Line, own sound (impale) | ready |
| peninsulaImpale (without #442) | :27219 | the same nodes as asunderImpale | ready (not cued) |
| nAttack_hit | :8303 | EC 0.5 + 0.5, 2 Line | ready |
| wallPuncture_hit | :9247 | EC 1, Ring + Line at z -0.5 | ready |
| peninsulaRound_ring | :27957 | EC 4 fPos fState, 2 Line + Ring, looped sound | ready |
| asunderRound | :28013 | EC 1, 2 Ring (Line_DoubleLine1) | ready; its spawn needs boneAt + the rot range (P4) |
| grandTide_ring | :37896 | EC 3 + 1 fPos fState, Ring / Image / Ring, own sound | ready |
| grandTide | :37424 | Animation (create 1.0 Once, root 2.033 Loop, destroy 1.0 Once), EC 99 + 1 fPos fState, looped sound, 5 StaticMesh; 2 ParticleSystems skipped | needs the Shuriken graft (P3) and fx:grandTide (P2) |
| malStorm, whaleWave | :32480, :31900 | EC 3 / EC 1 + 1 | ready (not cued: item 1) |
| shieldBash_hit, shieldRush_hit | :8688, :8905 | EC 1, Line + Ring | ready (never reaches the target: not cued) |
| javelin_hit | :8848 | not in the rip (KeyError) | never spawned locally: not cued |

**Sounds, voices and AudioSource clips** (all checked against the rip, `RippedAssets/.../heroes/whale/sounds`, `/voices`):
- `"sound"` cues: sweep, swallow, nAttack_hit, wallPuncture_hit. All are in whale/sounds.
- Voices: shieldBash1/2, tideCutter1/2, javelin1/2, shieldRush1/2, swallow1/2, peninsulaImpale1/2, peninsulaRound1/2, grandTide1/2. All are in whale/voices.
- The effects' own AudioSource clips are in whale/sounds: shieldBash_ring, javelin, shieldRush, peninsular, impale, peninsularRound, grandTide_ring, grandTide.
- In the rip with no code (left out): `peninsulaAsunder1/2`, `penninsulaImpale1/2` (0 loads in BB's Whale.cs and TTO1102's Whale.c; effect_only.md agrees).

## TTO in this scope

- Every TTO coroutine here loads the same asset names as BB: RPC_sweep d__166, RPC_javelin d__167, RPC_shieldBash d__162, RPC_shieldRush d__171, RPC_swallow d__175, RPC_peninsulaImpale d__180, RPC_peninsulaRound d__181, RPC_grandTide d__217 (pseudo/Whale.c string lists).
- The waits Ghidra or the disassembly shows match BB's:
  - javelin: 0.4 / 0.1 / 0.1 / 0.4
  - shieldBash: 0.2 x 3
  - grandTide: 1 / 1
  - sweep: 0.3, 0.5, 0.1, 0.3, 0.2
  - shieldRush: 0.2, 0.1, 0.1
  - swallow: 0.1
  - peninsulaRound: 0.8, 0.1, 0.2
  - peninsulaImpale: 0.8
- The rest are passed in registers and were not resolved: marked unverified, not a known difference.
- No TTO-only skill plays these clips. The TTO references are effects only:
  - RPC_leviathanBreach d__303 loads `shieldBash_hit`.
  - RPC_leviathanCast d__302 loads `grandTide_ring`.
  - Both are the tto report's (leviathanCall).
- The Bible's TTO note "Aim option" (Shield Rush, Javelin, Sweep, the Peninsulas aim at the command point only when another target is selected) does not change the tiles: the target is straight ahead.

## Page changes (index.html, wardrobe_skill_icons.py, wardrobe_fx.py), besides the parts

- **LOWER_RANK:** `whale: ["malStorm"]` (item 1), with its comment: "the Whale's malStorm: Whale Wave / Mal Storm play divingWave / divingStorm with Diving Press #443, Whale.cs:32111-32125, :32775-32789; plans/fx_whale/skills_b.md item 1".
- **SEQ whale:** no change. `"Grand Tide: grandTide1 grandTide2*@3 grandTide0"` matches the code:
  - grandTide1 for its whole 2.0 s
  - grandTide2 cut in, held
  - grandTide0 cut in
- **wardrobe_skill_icons.py:** nothing for this scope (every clip here has its icon in data/icons/hd/index.json). The diving clips' map is in item 1.
- **wardrobe_fx.py:** `SHURIKEN_FROM_TTO["whale"] = ["grandTide"]` (P3) and `LAYOUTS["Whale_javelin"] = []` (P1).

## Paste-ready cues for wardrobe/fx_cues/whale.json

- 9 entries, 99 cues, in `C:\work\12tails-wardrobe\checks\fx_whale_research\skills_b\cues_fmt.json` (valid JSON, the same as cues_block.json).
- Keys are the clips.
- New options:
  - `slot` on `javelin` (P1)
  - `anims` / `end` on `grandTide` (P2)
  - `boneAt` and the `[lo, hi]` rot element on `asunderRound` (P4)
- Every other option is one the page reads today.
- `grandTide2`'s empty entry only documents the clip and can be left out.

```json
{
  "shieldBash": {
    "why": "RPC_shieldBash :19653-20229 (Shield Bash #114, passive: doReleaseCharge :8486-8570 starts it when the Charge Attack (needs #111) is released after a hold of 3 s or more, with #114 and Game.mGameType > 4): PlayAnimation(shieldBash, 0.2) (:20040), voice shieldBash1 / shieldBash2 (Random.Range(0, 2) :20081-20122, played :20158 / :20171) at 0; Yield 0.2 (:20176): at 0.2 moveSpeed 2 (:19800), Effects/shieldBash_ring createEffect at the hero, hero rotation (:19811-19823; life 1, no follow; plays its own Sounds/shieldBash_ring), the hits FindAreaTarget(hero, 3 x rangeMod, 3 x rangeMod) (:19850) with RPC_shieldBash_hit at the struck foe (:19909; shieldBash_hit Instantiated at the hit point :8698): the 10 m target point (a Penguin-sized body: bounds centre 0.6 m up, height 1, radius 0.3) is out of the 3 m reach, so nothing is drawn (the Bison's convention); Yield 0.2 (:20174): moveSpeed 0 at 0.4 (:19952); Yield 0.2 (:20161): standby 0.6 (:19973)",
    "cues": [
      [0, "voice", "shieldBash1|shieldBash2"],
      [0.2, "fx", "shieldBash_ring"]
    ]
  },
  "sweep": {
    "why": "RPC_sweep :21464-22728 (rank 2, Tide Cutter #402 on: passives on): PlayAnimation(sweep, 0.2) (:22287), moveSpeed -0.5 (:22296); with #402 Effects/tideCutter_ring createEffect at the hero, hero rotation (:22299-22321; life 2, followPosition, followState: cut at the standby 1.6) and voice tideCutter1 / tideCutter2 (Random.Range(0, 2) :22364-22405, played :22610 / :22619), in place of sweep_ring and sweep1 / sweep2 (:22432-22534, without #402), at 0; Yield 0.2 (:22621): moveSpeed -0.3 (:21611); Yield 0.3 (:22601): moveSpeed 0 at 0.5 (:21638); Yield 0.5 (:22572): at 1.0 moveSpeed 9 and Sounds/sweep on the hero's AudioSource (:21665-21688, a 'sound' cue); Yield 0.1 (:22599): at 1.1 moveSpeed 6, hit 1 FindAreaTarget(hero, 4 + 2 (Tide Cutter), 3) (:21743); Yield 0.3 (:22580): at 1.4 moveSpeed 0, hit 2 FindAreaTarget(hero, 5, 3) (:21992); each hit is RPC_nAttack_hit at the foe or, on a Wall Puncture proc (lckAdjust(40) = 40 % at LCK 1, :9196-9215), RPC_wallPuncture_hit (:21839, :21930, :22088, :22179): the 10 m target point (a Penguin-sized body: bounds centre 0.6 m up, height 1, radius 0.3) is out of the 6 / 5 m reach (the game's dash brings her 0.71 / 2.51 m closer, the Bible's movement table; the page has no hero mover), so nothing is drawn; the camera's WallPuncture blur left out (:21887); Yield 0.2 (:22615): standby 1.6 (:22217)",
    "cues": [
      [0, "voice", "tideCutter1|tideCutter2"],
      [0, "fx", "tideCutter_ring", {"cut": 1.6}],
      [1.0, "sound", "sweep"]
    ]
  },
  "javelin": {
    "why": "RPC_javelin :22728-23422 (rank 2): animation.Rewind, PlayAnimation(javelin, 0.2) (:23197-23200), voice javelin1 / javelin2 (Random.Range(0, 2) :23241-23282, played :23336 / :23333) at 0; Yield 0.4 (:23318): moveSpeed 2 at 0.4 (:22886); Yield 0.1 (:23324): at 0.5 RPC_javelin_fire(firePos = cast spot + TransformDirection(1.2, 2.2, 1), fireDir = Math.getTrajectoryVector(firePos, target collider.bounds.center, 24)) (:22919-22967; Math.cs:885-1006) = Effects/javelin Instantiated at firePos, LookRotation(fireDir) (:8781-8794): rot [2.878, -7.595, 0] at the 10 m target point (a Penguin-sized body: bounds centre 0.6 m up, height 1, radius 0.3) (checks/fx_whale_research/skills_b/javelin_sim.txt), its ProjectileControl.life = 3 x rangeMod = 3 (:8803) and Whale_javelin.Init (:8809): a copy of the worn lance (mWep2 = getWeapon(code, 1) on mount_Hand_R, WhaleEquipment.cs:1631-1710: the page's slot R) parented at local identity, every renderer on (Whale_javelin.cs:82-118); it flies at 24 m/s (velocity = TransformDirection(0, 0, 24), :25, :50) under gravity -9.8 (Rigidbody useGravity, PhysicsManager: checks/fx_whale_research/skills_b/rb.py), nose along its velocity (:165), sticks in the ground on its trigger box's terrain contact (BoxCollider 0.25 x 0.25 x 3, centre z 0.5: gravity off, velocity eased to 0, :174, :191-198), destroyed at 3 s (:150-154); plays its own Sounds/javelin (AudioSource); its piercing hits on the target (OnTriggerStay :210-328, Wall Puncture's proc there too) draw nothing (no javelin_hit: RPC_javelin_hit has no local caller, Whale.cs:4213 is the remote dispatch, and the prefab is not in the rip); the lance in hand: its MeshRenderers off (:22985-23017) from 0.5 to 1.0 (:23049-23110; its weapon_fx particles keep drawing); Yield 0.1 (:23322): moveSpeed 0 at 0.6 (:23041); Yield 0.4 (:23328): standby 1.0 (:23127)",
    "cues": [
      [0, "voice", "javelin1|javelin2"],
      [0.5, "fx", "javelin", {"x": 1.2, "y": 2.2, "d": 1, "rot": [2.878, -7.595, 0], "slot": "R"}],
      [0.5, "hideProp", "R", {"kill": 0.5}]
    ]
  },
  "shieldRush": {
    "why": "RPC_shieldRush :24032-24642 (rank 2): PlayAnimation(shieldRush, 0.2) (:24445), voice shieldRush1 / shieldRush2 (Random.Range(0, 2) :24486-24527, played :24579 / :24574) at 0; Yield 0.2 (:24572): at 0.2 moveSpeed 6 x sLv = 12 (:24179) and Effects/shieldRush_ring createEffect at the hero's collider.bounds.center, hero rotation (:24190-24202; life 1, followPosition; plays its own Sounds/shieldRush): y 1.3 = the Whale prefab's CharacterController centre (checks/fx_whale_research/skills_b/body.py: height 2.4, radius 0.8, centre 1.3, Whale_tri scale 1, as the page draws her; 1.35 with Super Size 4 + Mega Size, Game.cs:2795-2825); Yield 0.1 (:24562): at 0.3 the hit box FindRecTarget(hero, forward, 1, 1, 2, 3) (:24252) with RPC_shieldRush_hit at the struck foe (:24311): the 10 m target point (a Penguin-sized body: bounds centre 0.6 m up, height 1, radius 0.3) is out of reach (2.4 m of dash in the game; no hero mover on the page), so nothing is drawn; Yield 0.1 (:24585): moveSpeed 0 at 0.4 (:24354); Yield 0.2 (:24583): standby 0.6 (:24375)",
    "cues": [
      [0, "voice", "shieldRush1|shieldRush2"],
      [0.2, "fx", "shieldRush_ring", {"y": 1.3}]
    ]
  },
  "swallow": {
    "why": "RPC_swallow :25218-26006 (rank 2, Gobble Up #233 learned, Wonder Belly #432 on): PlayAnimation(swallow, 0.2) (:25543), moveSpeed 0, voice swallow1 / swallow2 (Random.Range(0, 2) :25592-25647) and Effects/swallow_ring createEffect at the hero, hero rotation (:25666-25678; life 3, followPosition, followState: cut at the standby 2.9) at 0; Yield 1 (:25931): at 1.0 Sounds/swallow on the hero's AudioSource (:25382-25394, a 'sound' cue), then 9 pulls 0.1 s apart (i < 9 :25695, Yield 0.1 :25935) at 1.0 ... 1.8: RPC_AddDamage(230 + sLv, -1, ..., (sLv + 1) x unit toward hero + forward) on the locked target (:25885-25912; the Bible's 9 pulls), drawing nothing; at 1.9 the catch, only with Gobble Up (hasSkill(233) :25705): the target inside FindRecTarget(hero, forward, 1, 1, 2, 3) (:25726), the Whale's collider taller than its own (2.4 m against 1 m, :25766-25776) -> RPC_swallow_hit (:25791) = Effects/swallow_hit Instantiated at the target's collider.bounds.center, LookRotation(hero forward) (:9020-9030; life 1): drawn at d 1, y 0.6, the pull's goal hero + forward (:25885) inside the 2 m grab box, where the target is when it is caught (APPROXIMATED: the page's target does not move), then the swallow / gobble statuses (:25811-25839; the swallowed target's renderers go off, CharacterControl.cs:35573-35660); Yield 1 (:25927): standby 2.9 (:25478)",
    "cues": [
      [0, "voice", "swallow1|swallow2"],
      [0, "fx", "swallow_ring", {"cut": 2.9}],
      [1.0, "sound", "swallow"],
      [1.9, "fx", "swallow_hit", {"d": 1, "y": 0.6}]
    ]
  },
  "peninsulaImpale": {
    "why": "RPC_peninsulaImpale :26574-27523 (rank 2, Peninsula Asunder #442 on, Wall Puncture 4 on): PlayAnimation(peninsulaImpale, 0.2) (:27274), voice peninsulaImpale1 / peninsulaImpale2 (Random.Range(0, 2) :27315-27370) and Effects/peninsulaImpale_ring createEffect at the hero, hero rotation (:27389-27399; life 2, followPosition, followState: its life ends before the standby 3.8, so no cut; plays its own Sounds/peninsular) at 0; Yield 0.8 (:27435): at 0.8 moveSpeed 3 and the locked target (#442, :26762-26785), i = 0 (:26787); each stab (while i < 2 + 4 x sLv = 10, :27076): with #442 Effects/asunderImpale Instantiated at the hero, hero rotation (:27151-27169; life 1, its own Sounds/impale; in place of peninsulaImpale :27213-27231) and LookAt the target (:27199, straight ahead here), Yield 0.2 (:27433); the hit: moveSpeed 2 (:26813), one getWallPuncture() roll (:26844; lckAdjust(10 x 4) = 40 % at LCK 1: p 0.4, one roll per stab) over FindRecTarget(hero, forward, 1.5, 1.5, 12, 3) (:26830): the 12 m box reaches the 10 m target point (a Penguin-sized body: bounds centre 0.6 m up, height 1, radius 0.3): a proc -> RPC_wallPuncture_hit(vFlat(target centre) + (0, hero y + 1, 0), vFlat(target - hero)) (:26899-26919) = wallPuncture_hit, LookRotation(hitDir), + Sounds/wallPuncture_hit (:9247-9288); else RPC_nAttack_hit(the same point, hero forward) (:27006-27016) = nAttack_hit, hero rotation, + Sounds/nAttack_hit (:8303-8354): both at d 10, y 1, the sounds 'sound' cues (the hero's PlayOneShot); then Yield 0.1 (:27447) and i++ (:27249): stabs at 0.8 + 0.3 k, hits at 1.0 + 0.3 k (k = 0 ... 9: 1.0 ... 3.7); at i = 10 moveSpeed 0 and standby 3.8 (:27082-27099); left out: the camera's WallPuncture blur (:26962)",
    "cues": [
      [0, "voice", "peninsulaImpale1|peninsulaImpale2"],
      [0, "fx", "peninsulaImpale_ring"],
      [0.8, "fx", "asunderImpale"],
      [1.0, "fx", "wallPuncture_hit", {"d": 10, "y": 1, "p": 0.4, "roll": "impaleWp1"}],
      [1.0, "sound", "wallPuncture_hit", {"p": 0.4, "roll": "impaleWp1"}],
      [1.0, "fx", "nAttack_hit", {"d": 10, "y": 1, "p": 0.4, "roll": "!impaleWp1"}],
      [1.0, "sound", "nAttack_hit", {"p": 0.4, "roll": "!impaleWp1"}],
      [1.1, "fx", "asunderImpale"],
      [1.3, "fx", "wallPuncture_hit", {"d": 10, "y": 1, "p": 0.4, "roll": "impaleWp2"}],
      [1.3, "sound", "wallPuncture_hit", {"p": 0.4, "roll": "impaleWp2"}],
      [1.3, "fx", "nAttack_hit", {"d": 10, "y": 1, "p": 0.4, "roll": "!impaleWp2"}],
      [1.3, "sound", "nAttack_hit", {"p": 0.4, "roll": "!impaleWp2"}],
      [1.4, "fx", "asunderImpale"],
      [1.6, "fx", "wallPuncture_hit", {"d": 10, "y": 1, "p": 0.4, "roll": "impaleWp3"}],
      [1.6, "sound", "wallPuncture_hit", {"p": 0.4, "roll": "impaleWp3"}],
      [1.6, "fx", "nAttack_hit", {"d": 10, "y": 1, "p": 0.4, "roll": "!impaleWp3"}],
      [1.6, "sound", "nAttack_hit", {"p": 0.4, "roll": "!impaleWp3"}],
      [1.7, "fx", "asunderImpale"],
      [1.9, "fx", "wallPuncture_hit", {"d": 10, "y": 1, "p": 0.4, "roll": "impaleWp4"}],
      [1.9, "sound", "wallPuncture_hit", {"p": 0.4, "roll": "impaleWp4"}],
      [1.9, "fx", "nAttack_hit", {"d": 10, "y": 1, "p": 0.4, "roll": "!impaleWp4"}],
      [1.9, "sound", "nAttack_hit", {"p": 0.4, "roll": "!impaleWp4"}],
      [2.0, "fx", "asunderImpale"],
      [2.2, "fx", "wallPuncture_hit", {"d": 10, "y": 1, "p": 0.4, "roll": "impaleWp5"}],
      [2.2, "sound", "wallPuncture_hit", {"p": 0.4, "roll": "impaleWp5"}],
      [2.2, "fx", "nAttack_hit", {"d": 10, "y": 1, "p": 0.4, "roll": "!impaleWp5"}],
      [2.2, "sound", "nAttack_hit", {"p": 0.4, "roll": "!impaleWp5"}],
      [2.3, "fx", "asunderImpale"],
      [2.5, "fx", "wallPuncture_hit", {"d": 10, "y": 1, "p": 0.4, "roll": "impaleWp6"}],
      [2.5, "sound", "wallPuncture_hit", {"p": 0.4, "roll": "impaleWp6"}],
      [2.5, "fx", "nAttack_hit", {"d": 10, "y": 1, "p": 0.4, "roll": "!impaleWp6"}],
      [2.5, "sound", "nAttack_hit", {"p": 0.4, "roll": "!impaleWp6"}],
      [2.6, "fx", "asunderImpale"],
      [2.8, "fx", "wallPuncture_hit", {"d": 10, "y": 1, "p": 0.4, "roll": "impaleWp7"}],
      [2.8, "sound", "wallPuncture_hit", {"p": 0.4, "roll": "impaleWp7"}],
      [2.8, "fx", "nAttack_hit", {"d": 10, "y": 1, "p": 0.4, "roll": "!impaleWp7"}],
      [2.8, "sound", "nAttack_hit", {"p": 0.4, "roll": "!impaleWp7"}],
      [2.9, "fx", "asunderImpale"],
      [3.1, "fx", "wallPuncture_hit", {"d": 10, "y": 1, "p": 0.4, "roll": "impaleWp8"}],
      [3.1, "sound", "wallPuncture_hit", {"p": 0.4, "roll": "impaleWp8"}],
      [3.1, "fx", "nAttack_hit", {"d": 10, "y": 1, "p": 0.4, "roll": "!impaleWp8"}],
      [3.1, "sound", "nAttack_hit", {"p": 0.4, "roll": "!impaleWp8"}],
      [3.2, "fx", "asunderImpale"],
      [3.4, "fx", "wallPuncture_hit", {"d": 10, "y": 1, "p": 0.4, "roll": "impaleWp9"}],
      [3.4, "sound", "wallPuncture_hit", {"p": 0.4, "roll": "impaleWp9"}],
      [3.4, "fx", "nAttack_hit", {"d": 10, "y": 1, "p": 0.4, "roll": "!impaleWp9"}],
      [3.4, "sound", "nAttack_hit", {"p": 0.4, "roll": "!impaleWp9"}],
      [3.5, "fx", "asunderImpale"],
      [3.7, "fx", "wallPuncture_hit", {"d": 10, "y": 1, "p": 0.4, "roll": "impaleWp10"}],
      [3.7, "sound", "wallPuncture_hit", {"p": 0.4, "roll": "impaleWp10"}],
      [3.7, "fx", "nAttack_hit", {"d": 10, "y": 1, "p": 0.4, "roll": "!impaleWp10"}],
      [3.7, "sound", "nAttack_hit", {"p": 0.4, "roll": "!impaleWp10"}]
    ]
  },
  "peninsulaRound": {
    "why": "RPC_peninsulaRound :27523-28262 (rank 2, Peninsula Asunder #442 on): PlayAnimation(peninsulaRound, 0.2) (:27834), voice peninsulaRound1 / peninsulaRound2 (Random.Range(0, 2) :27883-27938) and Effects/peninsulaRound_ring createEffect at the hero, hero rotation (:27957-27969; life 4, followPosition, followState: cut at the standby 4.0; its looped Sounds/peninsularRound) at 0; Yield 0.8 (:28191): moveSpeed 3 at 0.8 (:27670); Yield 0.2 (:28189): at 1.0 moveSpeed 0, mHandMount = mount_Hand_R (:27719), i = 0; every 0.1 s (Yield 0.1 :28201, i++ :27733) while i < 12 + 8 x sLv = 28 (:27986): with #442 Effects/asunderRound Instantiated at mount_Hand_R's world position, its rotation x Euler(0, 0, Random.Range(-30, 30)) (int: -30 ... 29), not parented (:28007-28025; life 1, no follow; in place of peninsulaRound :28042-28060): 28 slash rings at 1.0 ... 3.7 left where the lance hand was; on i % 4 == 0 the hits FindRecTarget(hero - forward, forward, 3, 3, 5, 3) (:28081-28099): the 10 m target point (a Penguin-sized body: bounds centre 0.6 m up, height 1, radius 0.3) is out of the 4 m reach, so nothing is drawn; the redirect of damage taken (CharacterControl.cs:4299-4350) needs an attacker; at i = 28 Yield 0.2 (:28193): standby 4.0 (:27752); left out: the camera blur (:27713)",
    "cues": [
      [0, "voice", "peninsulaRound1|peninsulaRound2"],
      [0, "fx", "peninsulaRound_ring", {"cut": 4.0}],
      [1.0, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [1.1, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [1.2, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [1.3, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [1.4, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [1.5, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [1.6, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [1.7, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [1.8, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [1.9, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [2.0, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [2.1, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [2.2, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [2.3, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [2.4, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [2.5, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [2.6, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [2.7, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [2.8, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [2.9, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [3.0, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [3.1, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [3.2, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [3.3, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [3.4, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [3.5, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [3.6, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}],
      [3.7, "fx", "asunderRound", {"boneAt": "mount_Hand_R", "rot": [0, 0, [-30, 29]]}]
    ]
  },
  "grandTide1": {
    "why": "RPC_grandTide :37257-38002 (whl_grandTide5, single rank; Revised Skill #404 / Revised Magic #414 only lower its costs): PlayAnimation(grandTide1, 0.2) (:37781), moveSpeed 0, voice grandTide1 / grandTide2 (Random.Range(0, 2) :37822-37877) and Effects/grandTide_ring createEffect at the hero, hero rotation (:37896-37906; life 3 + 1, followPosition, followState: myCommand stays grandTide past its life, so no cut; its own Sounds/grandTide_ring) at 0; Yield 1 (:37936): at 1.0 moveSpeed 2, collisions ignored (:37398-37408), Effects/grandTide createEffect at the hero, hero rotation (:37424-37436; life 99 + 1, followPosition, followState, its looped Sounds/grandTide; five wave meshes + two BB ParticleSystems) and its Animation Play(create) Once (:37449-37454); Yield 1 (:37939): grandTide2 at 2.0 (the SEQ's grandTide1 step, 2.0 s); the wave: Play(root) Loop at grandTide2's start (:37509-37514) = age 1.0; its followState end when myCommand becomes grandTide0 (RPC_grandTide0 :38176; EffectControl.cs:226-291 plays its destroy clip, then the 1 s after-life; the coroutine's own Play(destroy) :37706 in the same frame) at grandTide0's start = age 4.0 with the SEQ's grandTide2*@3: anims and end are the fx:grandTide part's options",
    "cues": [
      [0, "voice", "grandTide1|grandTide2"],
      [0, "fx", "grandTide_ring"],
      [1.0, "fx", "grandTide", {"anims": [[1.0, "root"]], "end": 4.0}]
    ]
  },
  "grandTide2": {
    "why": "RPC_grandTide case 3 (:37472-37525): PlayAnimation(grandTide2, 0) cut, Loop (:37488-37493), moveSpeed 3 (:37498) at 2.0 s of the skill; every FixedUpdate (Yield WaitForFixedUpdate :37933) until the player moves or MP < 10 / SP < 20 (:37566-37601, then RPC_grandTide0 :37674): once a second (mUpdateTime :37604-37612) SP -10 (Revised Skill), MP -8 (Revised Magic) and hit(444) on FindRecTarget(hero - 4 x forward, forward, 8, 8, 7, 4) (:37617-37655), 4 m behind to 3 m ahead: the 10 m target point is out of reach and hit() draws nothing; the SEQ's grandTide2*@3 (a channel that runs until the player moves: three hits, at 0, 1, 2); the wave's root clip is played by the fx:grandTide part (the grandTide1 cue's anims)",
    "cues": []
  }
}
```

## Left out (with reasons)

- **Hits on the target that cannot reach it** (the Bison's convention; Mole decision 29):
  - Shield Bash (3 m)
  - Sweep (6 / 5 m)
  - Shield Rush (a 2 m box)
  - Peninsula Round (4 m)
  - Grand Tide (3 m ahead; hit() draws nothing anyway)
  - Their hit effects (shieldBash_hit, shieldRush_hit, nAttack_hit, wallPuncture_hit) would show only on a foe in reach.
- **Javelin's hits:** the game draws nothing (item 3).
- **The hero's hops and dashes:** no hero mover (Penguin decision 8).
- **Camera effects:** motion blur, shake, the WallPuncture message.
- **The swallowed target's disappearance:** the page draws no target body.
- **Lower-rank or passive-off variants:**
  - sweep_ring + sweep1/2 (without Tide Cutter)
  - peninsulaImpale / peninsulaRound (without Asunder)
  - `malStorm` / `whaleWave` on the malStorm clip (without Diving Press)
- **Voices with no code:** peninsulaAsunder1/2, penninsulaImpale1/2.

## Open questions (each with my recommended answer)

1. **`malStorm` as LOWER_RANK?**
   - **Recommended yes** (passives on; the Monkey's decision 6). No `malStorm` entry; the Whale Wave / Mal Storm tiles are `divingWave` / `divingStorm` (skills_a), with the CLIP_SKILLS map in item 1.
   - Alternative: keep a passive-off malStorm tile. That breaks the passives-on rule.
2. **Swallow's catch spot.**
   - **Recommended d 1, y 0.6.** The pull's goal is hero + forward, inside the 2 m grab box: where the game catches the target.
   - Alternative: d 10 (the standing target point). But there the catch cannot happen, since the box is 2 m.
3. **Swallow's catch at all** (it needs Gobble Up #233):
   - **Recommended yes.** Every skill is learned at max rank. The Bible documents the dependency.
4. **Peninsula Impale's Wall Puncture roll:**
   - **Recommended p 0.4 per stab** (lckAdjust(40) at LCK 1), with the paired `!roll` nAttack_hit. This matches effect_only.md open question 4.
5. **The wave's end age** (`end 4.0`) is tied to the SEQ's `grandTide2*@3`:
   - **Recommended keep** (the Cat's GCA_END precedent).
   - If the lead changes that @ (or grandTide1's 2.0), `end` = 1.0 + the grandTide2 step's length.
   - The other route is a page option "cut at step k's start": more general, but nothing else needs it yet.
6. **Shield Rush ring height:**
   - **Recommended y 1.3**, the centre of the body the page draws (prefab scale 1).
   - Use 1.35 if the lead scales the body to the passives-on 1.05 (effect_only.md open question 5).
7. **Shield Bash's tile:**
   - **Recommended the single `shieldBash` tile** (the clip after the release). The charge stays on the Charge Attack tile (attacks_emotes), as the Chameleon's Silent Walk (a passive inside the Charge Attack) kept its own clip tile (plans/fx_chameleon/skills_b.md, silentWalk).
   - Alternative: `"Shield Bash: cAttack1 cAttack2*@3 shieldBash~"` (hold at least 3 s, the 0.2 s fade :20040). That is the attacks_emotes owner's call, since it reuses their charge timings.
8. **Peninsula Round's rings: `boneAt` (frozen where the hand was) or `bone` (riding the hand)?**
   - **Recommended `boneAt`.** The game Instantiates at the hand's pose and never parents (:28025), so the 28 rings trace the lance's swing.
9. **Javelin with nothing in slot R:**
   - **Recommended the Whale's starter lance** (the Chameleon's starter-arrow decision 50). The parts agent names the item from WhaleEquipment's default code.
   - In the game an empty mWep2 cannot happen (a hero always holds a weapon).
10. **The javelin's ground contact:**
    - **Recommended the trigger box's lowest corner at y 0**, on Unity's 0.02 s FixedUpdate (assumed, the Cat_supportFire precedent).
    - It sticks about 11.9 m ahead. APPROXIMATED: the exact frame depends on the physics step.
11. **The empty `grandTide2` entry:**
    - **Recommended keep** for its `why`. Drop it if the editor's check objects to an entry with no cues.

## Offered to the user for the Bible (not written there)

- **Peninsula Impale's timing:**
  - Stabs are 0.3 s apart, not 0.2 s: `Yield 0.2` before each hit, then `Yield 0.1` (:27433, :27447).
  - Stab effects at 0.8 + 0.3 k, hits at 1.0 + 0.3 k (k = 0 ... 9 at rank 2), standby at 3.8.
  - So the movement table's distances are +0.6 m per hit, not +0.4.
- **Javelin:**
  - The projectile is a copy of the worn lance (Whale_javelin.cs:82-118); the lance in hand is hidden 0.5-1.0 s.
  - It is aimed by getTrajectoryVector at 24 m/s under gravity -9.8 and lives 3 x rangeMod s.
  - It sticks where its 3 m trigger box meets the ground.
  - It draws no hit effect: javelin_hit is never spawned locally and the prefab is not in the client.
  - Its Wall Puncture proc deals the purple damage with no effect.
- **Peninsula Round:**
  - The Asunder slash rings are spawned at the lance hand (mount_Hand_R) every 0.1 s, each rolled ±30 deg, not parented.
  - Standby at 4.0.
- **Grand Tide:**
  - The wave appears at 1.0 s (create clip), loops from 2.0 s, and is destroyed when the end move starts (EffectControl's followState).
  - The end move's standby is 0.8 s after it starts.
- **Shield Rush's ring** is centred on the Whale's body centre, not her feet.
- **Swallow's standby** is at 2.9 s (the catch at 1.9 s, then 1 s).
- **Unused voices in the client:** peninsulaAsunder1/2, penninsulaImpale1/2 (no code plays them).

## Verification (2026-11-13)

A read-only re-trace by the checker (office PC). My dumps and probes are in `checks\fx_whale_research\verify\`:
- `RPC_<name>.txt` for shieldBash, sweep, javelin, shieldRush, swallow, peninsulaImpale, peninsulaRound, grandTide, grandTide0, whaleWave and malStorm (`pipeline\clip_flow.js`, with the Effects / Sounds / Voices / moveSpeed lines kept).
- `probe.json` + `summary.txt`: `wardrobe_fx.py whale --probe` on the 14 cued effects, run here. `summ.py` reads its concatenated objects; probe.err is empty.
- `parse_blocks.py`: every json block of a report checked against `wardrobe_fx_check.py`'s KINDS / OPTS / entry keys, `data/whale/clips.json` and the page's whale SEQ names.

**Checked and confirmed.**
- **The waits, case by case** (each Yield's state number followed to its case):
  - **Shield Bash:** 0.2 + 0.2 + 0.2. The ring comes at 0.2 and standby at 0.6 (:20176, :20174, :20161).
    - The trigger: #111, `actionTime + 3 <= Time.time`, #114 and `Game.mGameType > 4` (:8517-8575).
  - **Sweep:** 0.2 + 0.3 + 0.5 + 0.1 + 0.3 + 0.2. Sounds/sweep plays at 1.0, the hits come at 1.1 and 1.4, standby at 1.6.
    - Tide Cutter's ring and voices are the `hasSkill(402)` branch (:22299-22405); sweep_ring and sweep1-2 are the else branch (:22432-22534).
    - The dash numbers (0.71 / 2.51 m closer) add up from the moveSpeeds.
  - **Javelin:** 0.4 + 0.1 + 0.1 + 0.4.
    - The renderers go off in case 3, after RPC_javelin_fire (:22975-22990).
    - Case 4's loop turns them back on only on the abort path (the action is no longer javelin).
    - Case 5 turns them on at 1.0.
  - **Shield Rush:** 0.2 + 0.1 + 0.1 + 0.2. The ring is at `collider.bounds.center` (:24202), and moveSpeed is `sLv x 6` (:24179).
  - **Swallow:** Yield 1, then 9 pulls (`i >= 9` :25695, Yield 0.1 :25935), then Yield 1 (:25927), so standby is at 2.9.
    - The catch comes at 1.9, behind `hasSkill(233)` (:25705).
    - It Instantiates at the target's bounds centre with LookRotation(hero forward) (:9020-9031).
    - No other sound or effect plays at the catch. Voices/gobbleUp (:26431) belongs to Gobble Up.
  - **Peninsula Impale:** case 2 sets i = 0 and goes to IL_F28 (the stab). The loop then runs:
    - IL_66C -> IL_C4F `Yield(3, 0.2)`;
    - case 3: the hit, then `Yield(4, 0.1)` (IL_1823);
    - case 4 -> IL_3DD `i++` -> IL_F28.
    - So the stabs are 0.3 s apart, at 0.8 + 0.3 k, and the hits at 1.0 + 0.3 k. Standby is at 3.8 (:27075-27099).
    - The hit point is `vFlat(bounds centre) + (0, hero y + 1, 0)` for both hits (:26896, :27003).
    - Both hit sounds have a 0.1 s throttle (:8329, :9264), shorter than the 0.3 s spacing.
  - **Peninsula Round:** `Random.Range(-30, 30)` is the int overload (both arguments are int literals, :28025 / :28060), so -30 ... 29.
    - The loop bound is `12 + 8 sLv` = 28 (:27986).
    - The rings come at 1.0 ... 3.7; at i = 28 Yield 0.2, so standby is at 4.0.
    - The hits come on `i % 4 == 0`: 7 of them, at 1.0 ... 3.4.
  - **Grand Tide:** Yield 1, then Yield 1.
    - The wave is made at 1.0, with Play(create) Once (:37436-37454).
    - At 2.0 grandTide2 is cut in and looped, and the wave plays root Loop (:37488-37514).
    - The release plays destroy (:37706).
    - RPC_grandTide0: myCommand grandTide0, the clip cut in, Yield 0.8, standby (:38170-38204).
- **Diving Press swap:** `hasSkill(443)` picks divingWave / divingStorm, else malStorm (:32111-32125, :32775-32789). `LOWER_RANK.whale = ["malStorm"]` stands (Monkey decision 6).
- **Javelin's aim:** I worked out every opaque predicate in `Math.getTrajectoryVector` (Math.cs:885-1006) by hand. Each one takes the path javelin_sim.py codes: the `y <= 0` root and the `y < 0.1` correction.
  - Fired from `mPos + TransformDirection(1.2, 2.2, 1)` (:22919) at the bounds centre (:22952), it gives rot [2.878, -7.595, 0].
  - parts.md's `javelin_aim.txt` gets the same rot on its own.
  - Whale_javelin.cs matches item 3:
    - the ctor sets (0, 0, 24), and Awake turns it by TransformDirection;
    - Init copies `mWep2` at local zero / identity, with every Renderer on;
    - FixedUpdate checks the life, then LookAt(position + velocity) until stuck, then Lerp(v, 0, 24 dt);
    - OnTriggerEnter on layer 0 sticks it and turns gravity off;
    - OnTriggerStay deals damage only.
- **Names:** all are in the BB rip (`gameassets/characters/heroes/whale/`).
  - effects/: shieldBash_ring, tideCutter_ring, javelin, shieldRush_ring, swallow_ring, swallow_hit, peninsulaImpale_ring, asunderImpale, nAttack_hit, wallPuncture_hit, peninsulaRound_ring, asunderRound, grandTide_ring, grandTide.
  - sounds/: sweep, swallow, nAttack_hit, wallPuncture_hit.
  - voices/: every cued pair.
  - `javelin_hit` is not there.
  - peninsulaAsunder1/2 and penninsulaImpale1/2 have no loads: 0 hits in BB's Whale.cs and in TTO1102's pseudo/Whale.c.
- **Probe (mine):**
  - Every EffectControl life, followPosition and followState in the Buildability table is right. For example:
    - tideCutter_ring: 2, fPos, fState;
    - shieldRush_ring: 1, fPos, ring node at z 1;
    - swallow_ring: 3, fPos, fState;
    - peninsulaRound_ring: 4, fPos, fState, the looped peninsularRound;
    - grandTide_ring: 3 + 1;
    - nAttack_hit: 0.5 + 0.5.
  - grandTide's root:
    - Animation: create 1.0 wrap 1, root 2.0333 wrap 2, destroy 1.0 wrap 1. Create plays on awake.
    - EffectControl 99 + 1, fPos, fState.
    - AudioSource grandTide, looped.
    - Under it: five grandTide_tri StaticMeshes at y -4.775, and two empty ParticleSystem nodes at z 2 and z -3.5.
  - javelin's root: ProjectileControl + Whale_javelin + AudioSource javelin. It has no EffectControl.
- **Reach calls:** every "out of reach" under Left out holds for the 10 m point (3 m, 6 / 5 m, the 2 m box, 4 m, 3 m ahead).
- **The block:** it parses, with 9 entries and 99 cues.
  - Every key is a clip in clips.json, and the times are in order.
  - The only option the check does not know is `boneAt` (Finding 2). `slot`, `anims` and `end` are known words.
- **Ranks:**
  - Sweep, Javelin, Shield Rush, Swallow, Peninsula Impale and Peninsula Round are all max rank 2 (whale-skill-reference.md:12-21).
  - Wall Puncture is rank 4: `lckAdjust(10 x 4)`, so p 0.4 at LCK 1, one roll per stab (whale-skill-reference.md:332, Whale.cs:26844).
- **Not re-derived:** the TTO wait list (from Ghidra and the disassembly). I take it as the report states it; it changes no cue.

**Findings.**

1. **The Grand Tide wave's cue options do not match the part's fixed interface.**
   - parts.md fixes `fx:grandTide` up front (Interfaces 1, `parts.md:296-297`; section 6, `:232-240`):
     - the part plays `root` Loop at age 1.0 by itself;
     - at the cue option `release` (an age) it calls `fx.cutNow()`;
     - its block has `[1, "fx", "grandTide", {"release": 4}]` (`parts.md:401`).
   - This report's cue uses `anims [[1.0, "root"]]` and `end 4.0` (the Cat's GCA pattern) instead.
   - **Decided: parts.md's interface.**
     - It belongs to the builder, and it was fixed first so the builders can run in parallel.
     - There is one fixed clip at a fixed age. The Cat's GCA needed `anims` for its varying clip list.
     - `cutNow()` ends the wave the same way `cutAt = -Infinity` does: the destroy clip, then the 1 s after-life, gone at age 5.0.
   - The age does not change: release 4 = grandTide1's 2.0 - 1.0 + grandTide2's @3.
   - Open question 5 now reads `release` where it says `end`.
   - The corrected entry is below.
2. **P4 (`boneAt` and the `[lo, hi]` rot element) is in no builder's list.**
   - parts.md never names asunderRound, Peninsula Round or `boneAt`.
   - Its page_pipeline row (`parts.md:336`) lists only LAYOUTS, the Shuriken line, PROP_STARTER, FX_PART_FILES and `OPTS += guard, attack`.
   - Every missing page part is built (the rule), so the lead gives P4 to page_pipeline:
     - `wardrobe/index.html` cueOf / Fx: `boneAt` takes the bone's pose once, at the spawn. That is `bone`'s own matrix math (`:4401-4407`) run in the constructor, with `boneRot` after it.
     - `rotOf` (`:4849`): each `[lo, hi]` element becomes a whole number drawn per play. It is one line: `Array.isArray(r) ? r.map(v => Array.isArray(v) ? randInt(v[0], v[1]) : v) : ...`. `randInt` includes `hi`, so `[-30, 29]` is Unity's `Range(-30, 30)`.
     - The cue-format comment gets a dated line for each.
     - `pipeline/wardrobe_fx_check.py:215`: `OPTS += "boneAt"`. Without it the check reports the peninsulaRound cues as "bad cue".
   - Until P4 is built, the peninsulaRound entry stays out of whale.json, as the report says.
3. **Javelin's `slot: "R"` is not in parts.md's interface.**
   - Interfaces 1 says "javelin / flyingShield take none", and its build calls `api.propModel("R", true)`.
   - It is not a wrong cue: `slot` is already a known OPTS word (the Chameleon's arrow), and it names which prop is copied.
   - **Decided: keep the cue as written.** The builder may read `fx.at.slot || "R"`, as the Chameleon's arrow does.
   - Either way the Whale's lance is in slot R (index.html SWAP_HANDS `:1082-1086`, parts.md `:60-62`).
4. **No `grandTide0` entry is needed.**
   - The report leaves grandTide0 "not in this scope", and no other report's block has it either.
   - RPC_grandTide0 (:38002-38233) loads nothing. Its only lines are myCommand, the clip, moveSpeed and standby (verify\RPC_grandTide0.txt).
   - The wave's destroy at grandTide0's start belongs to the grandTide1 cue (Finding 1).
5. **Swallow's cut 2.9 is past the end of the 2.8 s clip.**
   - In play-once mode the cut comes in the idle tail (Chameleon decision 11).
   - With the loop toggle on, the round restarts at 2.8 s, so the cut never comes. The ring then ends on its own life (3.0), 0.2 s into the next round. Against the game's 2.9 standby, it ends 0.1 s late.
   - **No change.** The same holds for Javelin: its part lives 3 s, past the 1.3 s clip, so it plays out in the idle tail.
6. **Swallow's catch spot, a note on Open question 2.**
   - The pull's goal, `hero + forward` (1 m ahead), is inside the Whale's capsule: radius 0.8 at the drawn size, plus the target's 0.3.
   - So if the push moves the target through its CharacterController, a pulled target stops near d 1.1.
   - **Keep d 1** (marked APPROXIMATED, as written). The 0.1 m is within the approximation.
   - The catch needs the target inside the 0-2 m box. The pulls bring a 10 m target there: 9 pulls of 3 units each, the tooltip's 9 / 18 m/s.

**Corrected paste-ready entry.** Only `grandTide1` changes: its last cue and the end of its why. Every other entry in the block above stands as written. `peninsulaRound` goes in once P4 is built (Finding 2).

```json
  "grandTide1": {
    "why": "RPC_grandTide :37257-38002 (whl_grandTide5, single rank; Revised Skill #404 / Revised Magic #414 only lower its costs): PlayAnimation(grandTide1, 0.2) (:37781), moveSpeed 0, voice grandTide1 / grandTide2 (Random.Range(0, 2) :37822-37877) and Effects/grandTide_ring createEffect at the hero, hero rotation (:37896-37906; life 3 + 1, followPosition, followState: myCommand stays grandTide past its life, so no cut; its own Sounds/grandTide_ring) at 0; Yield 1 (:37936): at 1.0 moveSpeed 2, collisions ignored (:37398-37408), Effects/grandTide createEffect at the hero, hero rotation (:37424-37436; life 99 + 1, followPosition, followState, its looped Sounds/grandTide; five wave meshes + two BB ParticleSystems, the Shuriken graft) and its Animation Play(create) Once (:37449-37454; also its play-on-awake clip); Yield 1 (:37939): grandTide2 at 2.0 (the SEQ's grandTide1 step, 2.0 s); the wave: Play(root) Loop at grandTide2's start (:37509-37514) = age 1.0, played by the fx:grandTide part (plans/fx_whale/parts.md 6); its followState end when myCommand becomes grandTide0 (RPC_grandTide0 :38176; EffectControl.cs:226-291 plays its destroy clip, then the 1 s after-life; the coroutine's own Play(destroy) :37706 in the same frame) at grandTide0's start = age 4.0 with the SEQ's grandTide2*@3: the part's release option (fx.cutNow(): the step edge a cue's cut cannot cross; skills_b.md Verification 1)",
    "cues": [
      [0, "voice", "grandTide1|grandTide2"],
      [0, "fx", "grandTide_ring"],
      [1.0, "fx", "grandTide", {"release": 4}]
    ]
  },
```

**For the Bible (confirmed, still only offered):**
- Peninsula Impale's 0.3 s spacing. So the movement table's distances at the hits are 0.6 + 0.6 k m, not +0.4 each: moveSpeed 3 from 0.8 to 1.0, then 2 until 3.8.
- Javelin's copied lance, Peninsula Round's hand rings and Grand Tide's clip timeline are as the report writes them.
