Summary: 14 clips, 16 coroutines read, 14 tiles, 16 cue keys (39 cues).
- **Pools:** `stasisBlow`: Stasis Blow, Death Blow (one tile each).
- **Sequences:** Raijin Ken is 7.5 s, not the page's ~3.7 s nor the Bible's ~2.4 s: the charge holds cAttack2 until 5 s after the cast (BB and TTO agree). New: Tiger Toss (`grab` then `tigerToss`), Roll Around (6 s).
- **Parts to build:** a new cue option `enable` for TrailRenderers the hero's code switches on and off (Three Steps' three fist trails; fxparts/trail.js drops a disabled TrailRenderer today, so they never draw). `SHURIKEN_FROM_TTO["panda"] = ["raijinKen_hit"]` (data only; proved in memory by probe2).
- **Everything else is ready:** 20 of the 22 cued effects.
- **No hits drawn:** every hit in scope lands within 1-5 m, so none reaches the 10 m target. Stasis Blow's and Death Blow's hit RPCs are empty in both games.
- **Possible Bible findings:**
  - Raijin Ken's timeline.
  - Water Monkey / Water Crane hits are 0.2 s apart, not 0.7 s.
  - Stasis / Death Blow have no hit look.
  - Nine Steps swaps Three Steps' voices.

---

# Panda effects + sounds research: skill clips, second half (skills_b)

Scope: the clips raijinKen1, raijinKen2, risingDragons, risingVortex, roll, rollAround, rushingFalcon, spTransfer, stasisBlow, threeSteps, tigerToss, towerRush, waterCrane and waterMonkey, and every skill that plays them (`pipeline/clip_calls.js`). Research only (recipe steps 1-3).

- Line numbers are `C:\Users\Jump\Desktop\12tails\DecompiledSource\Panda.cs` (the home PC's `D:\12tails\...`) unless another file is named. `TTO1102:` = `DecompiledSource_TTO_2026-11-02/pseudo/Panda.c`.
- Times are seconds from the start of the clip the entry is keyed by (a SEQ step's own start). Distance 0 = at the hero.
- Max rank, passives on:
  - Roll 2, Three Steps 2 with Nine Steps #402, Rushing Falcon 2, Tower Rush 2 with Ogre Impact #422, Tiger Toss with Tiger Pounce #232.
  - Rising Vortex 2, Rising Dragons 2, Water Monkey 2 / Water Crane 2 with Time and Tide #413 and Spirit Fist #433.
  - Stasis Blow 2 / Death Blow 2 with Wind Walker #423, Sp Transfer 2 with Heaven Breath #443, Roll Around #421, Raijin Ken #444.
  - No effect in scope is picked by `sLv`.

Read-only probes, in `checks\fx_panda_research\skills_b\` (git-ignored):
- `flow.py` prints a coroutine with its junk predicates evaluated (`if (FALSE) {continue;}` dropped, `if (TRUE)` marked). Its outputs are `RPC_<name>.txt`, plus `RPC_grab.txt` for Tiger Toss's dispatch. `clip_calls.txt` is `clip_calls.js panda`.
- `probe.json` / `probe_sum.txt`: `wardrobe_fx.py panda --probe` on 32 effects.
- `tto_probe.json`: `wardrobe_fx_tto.py panda --probe raijinKen_hit`.
- `probe2.py` -> `probe2.txt`: `SHURIKEN_FROM_TTO["panda"] = ["raijinKen_hit"]` added in memory, then the probe's graft. It reports "TTO's ParticleSystem grafted from TTO node 1 (material Cloud1)" onto BB node 3.
- `pool.py` -> `pool.json` / `pool_pretty.txt`: the entries below. It checks valid JSON, cue times in order, kinds fx / voice / sound, and that every key is a Panda clip or `@Seq:clip`.

## Read this first

1. **Pools and tiles (14).**
   - `stasisBlow` is played by Stasis Blow (RPC_stasisBlow :34612) and Death Blow (RPC_deathBlow :35430). It is a pool: one tile per member (poolChains), each with its Bible icon. Death Blow's icon needs a CLIP_SKILLS line (paste below).
   - The other twelve clips have one skill each. roll = Roll, rollAround = Roll Around, threeSteps = Three Steps, rushingFalcon = Rushing Falcon, towerRush = Tower Rush, tigerToss = Tiger Toss, risingVortex = Rising Vortex, risingDragons = Rising Dragons, waterMonkey = Water Monkey, waterCrane = Water Crane, spTransfer = Sp Transfer, and raijinKen1 + raijinKen2 = Raijin Ken.

2. **Raijin Ken is 7.5 s** (question 1).
   - RPC_raijinKen holds the looped cAttack2 until `Time.time >= actionTime + 5`. That is :41896, with actionTime set at the cast (:42051). TTO1102 `<RPC_raijinKen>d__236` has the same `=5`.
   - The timeline:

     | time (s) | what happens |
     |---|---|
     | 0 | cAttack1, cut in |
     | 0.7 | cAttack2, cut in, looped |
     | 5.0 | raijinKen1 |
     | 5.5 | the hit look at the target |
     | 5.9 | the 8 m blast |
     | 6.7 | raijinKen2 |
     | 7.5 | standby |

   - Every clip is cut in (`PlayAnimation(x, 0)`).
   - The page's SEQ today is `cAttack1 cAttack2* raijinKen1 raijinKen2`, which holds cAttack2 for 1.5 s. Replace it with `"Raijin Ken: cAttack1!@0.7 cAttack2*!@4.3 raijinKen1!@1.7 raijinKen2!"`.
   - Its cues are keyed `@RaijinKen:cAttack1` / `@RaijinKen:cAttack2`. The empty cAttack2 entry keeps the Charge Attack's cAttack2 cues off this tile.

3. **New sequences:**
   - **Tiger Toss** `"Tiger Toss: grab^@0.2 tigerToss!"`.
     - RPC_grab plays `grab` with a 0.1 s fade (:26359), dashes at 0.1 s and checks the box at 0.2 s.
     - It then starts RPC_tigerToss (:26142), which cuts in `tigerToss` (:26959).
     - `grab` is skills_a's clip, and so are its Climbing Cliff / Crumbling Mountain branches (:26178-26245). The line must agree with theirs (question 3).
   - **Roll Around** `"Roll Around: rollAround*^@6"`. The roll lasts its 6 s timer (:20650), then each round recasts with a new voice and ring. LOOPS already has `rollAround`.
   - Also SEQ_SKILL `panda: { "@RaijinKen": "raijinKen", "@TigerToss": "tigerToss" }`. Without it, the Raijin Ken tile also shows the Charge Attack's icon, and the Tiger Toss tile shows grab's icons (moveSkillIcons).

4. **Parts to build** (two; everything else is ready):
   - **TrailRenderer `enable`:**
     - `threeStep`'s three TrailRenderers (fxNode1-3) are disabled in the prefab (`m_Enabled` 0, probe). The hero's code switches them: fxNode1 on at 0.1 s, fxNode2 on at 0.4, fxNode1 off at 0.5, fxNode2 off at 0.8, fxNode3 on at 1.2 (:20873, :20900, :21063, :21250, :21277).
     - `fxparts/trail.js` returns null for a disabled TrailRenderer today (:100), so they never draw. The inventory's "threeStep: ready" misses this.
     - The new cue option is `"enable": [[seconds after the spawn, "node name", true | false], ...]`.
     - The page: Fx shows or hides the TrailRenderer of the node with that name at that age.
     - trail.js: builds a disabled TrailRenderer too, hidden until switched on. Its update already forgets the points while the mesh is hidden (:110).
     - The check: OPTS += `"enable"`.
     - stasisBlow's / deathBlow's trails are enabled in the prefab: nothing to do for them.
   - **raijinKen_hit's ParticleSystem:**
     - BB's node 3 decodes nothing. TTO's copy decodes it: 32 particles bursting at 0.4 s, material tto_Cloud1 (tto_probe.json).
     - `SHURIKEN_FROM_TTO["panda"] = ["raijinKen_hit"]`. There is no SHURIKEN_MAT entry, so it goes by the Chameleon's graft_by_material route: node name + BB's material Cloud1, TTO node 1 -> BB node 3 (probe2.txt).
     - The node order differs (TTO 1, BB 3), as the Mole's bazooka_ring.

5. **Where things land** (decisions applied by analogy):
   - The hero does not travel (Bison decision 17), so the following are left out:
     - every dash: Three Steps, Rushing Falcon, Tower Rush's 16 m/s lunge, Stasis / Death Blow's 3 / 10 / 4 m/s;
     - every step back: Tower Rush, Rising Dragons;
     - Roll's roll, Roll Around's steering, Water Monkey's step and Tiger Toss's 3 m/s walk;
     - Wind Walker's warp (question 4).
   - All effects sit at the standing hero.
   - **No hit is drawn** where the reach misses the 10 m target (Mole decision 29):
     - threeStep_hit, rushingFalcon_hit and waterMonkey_hit: 1-2 m boxes;
     - towerRush_hit: Ogre Impact's 4 m circle;
     - risingVortex_hit and risingDragon_hit: 3 m;
     - waterCrane_hit: 5 m.
   - **Stasis Blow and Death Blow have no hit look at all.** RPC_stasisBlow_hit / RPC_deathBlow_hit are empty bodies (:9125, :9138). In TTO both names map to one stub (TTO1102 methods.tsv RVA 0x33b5c0).
   - **Raijin Ken's hit is at the 10 m target**: the dispatch puts it at the target's front, `bounds.center - extents.x x dir` (:41753-41763). That is `{d 9.7, y 0.6}` (the target body: Bat decision 3), facing the hero `rot [0, 180, 0]` (LookRotation(-hitDir) :42525).
   - **Sp Transfer's ally is at the 10 m point:**
     - The skill refuses the Panda herself (:6717-6728), so the Sheep's self-cast rule does not apply. Its exception does: Revive and Gleaming Breath, Sheep decisions 1 and 4.
     - The bolt (BoltEmitter) aims at the ally's bounds centre every frame (:36441), `to [0, 0.6, 10]`, from `{y 0.4, d 0.5}`. It is destroyed 0.3 s later (`kill 0.3`, :36090, :36300).
   - **Tiger Toss assumes the grab held** (question 2):
     - The grab needs a target in its 1 m box (:26073); with none, the game plays grab only.
     - The tile shows the toss, as the Mole's Detonate assumes its nuke (Mole decision 27).
     - Tiger Pounce's splash is drawn at the grabbed target's spot, 1 m ahead on the floor.

6. **Passives swap looks:**
   - Nine Steps -> voices nineStep1|2 instead of threeStep1|2 (:21569).
   - Time and Tide -> `timeAndTideMonkey` / `timeAndTideCrane` (the shadow clones) instead of `waterMonkey` / `waterCrane` (:33227, :33792).
   - Ogre Impact -> `towerRush_ogre` at 0.2 s (:25371).
   - Tiger Pounce -> `tigerPounce_hit` 0.1 s after the throw (:26758-26771).

7. **Roll has no effect:** RPC_roll loads only its voices and Sounds/roll (:20008-20092).

8. **Voice spelling:** Raijin Ken asks for `Voices/raijinKen1|2` (:42119, :42150). The rip has `raijinken1|2.wav` (Resources is case-blind; TTO asks for `raijinken1`). The cue keeps BB's spelling: `rip_wav`'s `os.path.exists` finds it on Windows, which both PCs are.

9. **TTO.**
   - No released TTO skill (nineDragons, tempestDance, tempestDanceEnd, yinYangFist) plays these clips.
   - Every BB coroutine here has a TTO twin playing the same clip (TTO1102 pseudo/Panda.c):

     | coroutine | line |
     |---|---|
     | roll | :19721 |
     | rollAround | :20070 |
     | threeStep | :23504 |
     | rushingFalcon | :20680 |
     | towerRush | :25449 |
     | tigerToss | :24682 |
     | risingVortex | :18930 |
     | risingDragons | :17859 |
     | waterMonkey | :26780 |
     | waterCrane | :26148 |
     | stasisBlow | :22261 |
     | deathBlow | :4271 |
     | spTransfer | :21657 |
     | raijinKen | :15819 |

   - TTO's Raijin Ken has the same waits: 0.7, the 5 s check, 0.5, 1.2, 0.8.
   - BB is the authority for the cues.

## Per clip

Format: the RPC (file:line), then the timeline (fx = effect where / rotation; voice = Voices/; sound = Sounds/ the hero's code plays). Then where it ends (standby), followState cuts, passives and buildability. The "why" of each JSON entry carries every citation.

### roll (Roll 2; clip 1.0 s)
- RPC_roll :19727-20128:
  - 0: voice roll1|roll2 (:20008); sound roll (:20082-20092). No effect.
  - Standby 0.8 (Yield 0.1 :20125 + 0.7 :20123, :19894).
- **Buildable:** nothing to build.

### rollAround (Roll Around #421; clip 0.7 s, looped; SEQ "Roll Around: rollAround*^@6")
- RPC_rollAround :20159-20700:
  - 0: voice rollAround1|rollAround2 (:20550); fx rollAround_ring at the hero (:20636; followPosition + followState, life 6, its own rollAround_ring sound).
  - Standby when the 6 s timer runs out (:20650, :20425-20442), the ring's life too: no cut.
- **Buildable:** ready.

### threeSteps (Three Steps 2 + Nine Steps; clip 1.6 s)
- RPC_threeStep :20721-21805:
  - 0: voice nineStep1|nineStep2 (:21575); fx threeStep at the hero, rot [270, 90, 0] (:21728; followPosition + followState, life 3; its Animation 'root', 1.4 s, swings fxNode1-3 along the fists).
  - The trail switches are in Read this first 4.
  - Hits at 0.4 / 0.7 / 1.3 s (no target in reach); standby 1.4 (:21458) = the cut.
- **Buildable:** needs the `enable` option.

### rushingFalcon (Rushing Falcon 2; clip 1.3 s)
- RPC_rushingFalcon :21885-22776:
  - 0: voice rushingFalcon1|rushingFalcon2 (:22637); fx rushingFalcon at the hero (:22721; followPosition + followState, life 2; its three rings are delayed 0.3 / 0.5 / 0.7 s, the three hits).
  - Standby 1.0 (:22526) = the cut.
- **Buildable:** ready.

### towerRush (Tower Rush 2 + Ogre Impact; clip 1.0 s)
- RPC_towerRush :25172-25811:
  - 0: voice towerRush1|towerRush2 (:25682); fx towerRush_ring at the hero (Instantiate :25766, life 0.5).
  - 0.2: fx towerRush_ogre at the hero (:25395; StaticMesh + AlphaTimer + ring, life 1).
  - Standby 0.8 (:25571).
- **Buildable:** ready.

### tigerToss (Tiger Toss + Tiger Pounce; clip 1.0 s; SEQ "Tiger Toss: grab^@0.2 tigerToss!")
- RPC_tigerToss :26452-27190 (started by RPC_grab :25862, at 0.2 s :26142):
  - 0: voice tigerToss1|tigerToss2 (:27003).
  - 0.6: fx tigerToss at the hero + 1.2 m up (:26633; life 2).
  - 0.7: fx tigerPounce_hit at the thrown target, LookRotation(forward) (:26771, :8690). Here it is placed 1 m ahead on the floor (question 2).
  - Standby 0.8 (:26889).
- **Buildable:** both ready.

### risingVortex (Rising Vortex 2; clip 1.2 s)
- RPC_risingVortex :28672-29351:
  - 0: voice risingVortex1|risingVortex2 (:29177); fx risingVortex at the hero (:29261; followPosition + followState, life 2).
  - Pulls at 0.4 / 0.6 within 3 m; standby 1.0 (:29066) = the cut.
- **Buildable:** ready.

### risingDragons (Rising Dragons 2; clip 2.8 s)
- RPC_risingDragons :29356-30282:
  - 0: voice risingDragon1|risingDragon2 (:30156).
  - 0.1: fx risingDragon_ring at the hero (:29521; followPosition, life 4).
  - 0.4: fx risingDragon at the hero (:29677; followPosition + followState, life 2.4 + 1; the dragon's SkinnedMesh flies 15 m along its Animation in 2 s).
  - Eight uppercuts 0.6-1.65, then at 2.1 fx ashuraFist at the hero, identity (:29782).
  - Standby 2.6 (:29922) = risingDragon's cut.
- **Buildable:** all ready.

### waterMonkey (Water Monkey 2 + Time and Tide; clip 1.0 s)
- RPC_waterMonkey :32706-33330:
  - 0: voice waterMonkey1|waterMonkey2 (:33159); fx timeAndTideMonkey at the hero (:33247; life 2: the shadow clone's SkinnedMesh + AlphaTimer and its Animation, three images 1 / 2 / 3 m ahead at 0.4-0.6 s).
  - Hits at 0.5 / 0.7; standby 0.9 (:32964).
- **Buildable:** ready.

### waterCrane (Water Crane 2 + Time and Tide; clip 2.0 s)
- RPC_waterCrane :33382-33990:
  - 0: voice waterCrane1|waterCrane2 (:33724); fx timeAndTideCrane at the hero (:33816; followPosition + followState, life 3; EmblemEmitter, images, rings and the shadow clone).
  - Pulses at 0.7 / 0.9 within 5 m; standby 1.7 (:33593) = the cut.
- **Buildable:** ready.

### stasisBlow (pool: Stasis Blow 2, Death Blow 2; clip 1.0 s)

| member | 0 s | 0.2 s | 0.6 s | standby |
|---|---|---|---|---|
| stasisBlow (RPC_stasisBlow :34040-34789) | voice stasisBlow1\|2 (:34653); fx stasisBlow_ring at the hero (:34737; followState, cut 0.8) | fx stasisBlow, rot [270, 90, 0] (:34224; followPosition + followState, cut 0.8) | fx stasisBlow_endDust at the hero (:34476) | 0.8 (:34524) |
| deathBlow (RPC_deathBlow :34851-35610) | voice deathBlow1\|2 (:35471); fx deathBlow_ring at the hero (Instantiate :35555) | fx deathBlow, rot [270, 90, 0] (:35039; cut 0.8) | fx stasisBlow_endDust (:35294) | 0.8 (:35342) |

- The hit at 0.5 s draws nothing in either game (Read this first 5).
- Wind Walker's warp is left out (question 4).
- **Buildable:** all ready.

### spTransfer (Sp Transfer 2; clip 1.0 s)
- RPC_spTransfer :35899-36480:
  - 0: voice spTransfer1|spTransfer2 (:36219).
  - 0.5: fx spTransfer, a BoltEmitter, at TransformDirection(0, 0.4, 0.5), identity (:36080), to the ally's bounds centre 10 m ahead; destroyed at 0.8 (:36300).
  - Standby 0.8 (:36354).
- **Buildable:** ready. The page's BoltEmitter takes `to` (index.html boltEmitter, the Bat's).

### raijinKen1 / raijinKen2 (Raijin Ken; SEQ "Raijin Ken: cAttack1!@0.7 cAttack2*!@4.3 raijinKen1!@1.7 raijinKen2!")
- RPC_raijinKen :41542-42250 and RPC_raijinKen_hit :42290-42595:
  - **@RaijinKen:cAttack1**, 0: voice raijinKen1|raijinKen2 (:42107); fx raijinKen_ring1 at the hero (:42191; followPosition + followState, life 5, a looping raijinken1 sound). No cut: it ends at 5.0 s by itself, as in the game.
  - **@RaijinKen:cAttack2** (0.7-5.0 s): nothing new.
  - **raijinKen1** (from 5.0 s):
    - 0: fx raijinKen_ring2 at the hero (:41940; followPosition, life 3); voice nAttack3 (:41991).
    - 0.5: fx raijinKen_hit at {d 9.7, y 0.6}, rot [0, 180, 0] (:42525). Its Animation flies the kicking Panda image from (0, 15, 11) in its own space down to the impact in 0.433 s, and its rings come at 0.4 s.
  - **raijinKen2** (6.7-7.5 s): nothing new.
- **Buildable:** ring1 and ring2 are ready; raijinKen_hit needs the Shuriken graft (Read this first 4). Its Camera / effectCamera nodes draw nothing.

## Effects at a glance

- **Ready:** rollAround_ring, rushingFalcon, towerRush_ring, towerRush_ogre, tigerToss, tigerPounce_hit, risingVortex, risingDragon_ring, risingDragon, ashuraFist, timeAndTideMonkey, timeAndTideCrane, stasisBlow_ring, stasisBlow, stasisBlow_endDust, deathBlow_ring, deathBlow, spTransfer, raijinKen_ring1, raijinKen_ring2.
- **Need a part:**

  | effect | part |
  |---|---|
  | threeStep | the `enable` option (TrailRenderer on / off) |
  | raijinKen_hit | the TTO Shuriken graft (data) |

- **Not cued:**
  - Hits only on a target in 1-5 m: threeStep_hit, rushingFalcon_hit, towerRush_hit, risingVortex_hit, risingDragon_hit, waterMonkey_hit, waterCrane_hit.
  - waterMonkey and waterCrane: Time and Tide replaces them.
  - Stasis / Death Blow hits: none exist.
- **Sounds:**
  - The one "sound" cue: roll. It is in the rip's panda/sounds.
  - Every effect's own AudioSource is in panda/sounds: threeSteps, rushingFalcon, towerRush, towerRush_ogre, tigerToss, tigerPounce, risingVortex, risingDragons, ashuraFist, waterMonkey, waterCrane, stasisBlow, rollAround_ring, raijinken1 / raijinken2 / raijinken_hit.
  - Every voice named is in panda/voices.

## Paste-ready cue entries for wardrobe/fx_cues/panda.json

16 keys, 39 cues (from `checks\fx_panda_research\skills_b\pool_pretty.txt`, checked by `pool.py`).
- New option: `enable` on threeStep (the part, Read this first 4).
- `to` and `kill` on spTransfer.
- The pool's member keys name its tiles ("Stasis Blow", "Death Blow").

```json
{
"roll": {
  "why": "Panda.cs RPC_roll (:19727-20128), Roll 2 (max rank: only moveSpeed and the lock levels change, :19973, :19976): clip, 0.2 s fade (:19964), voice roll1 / roll2 (Random.Range(0, 2) :20008, loads :20020 / :20051, PlayOneShot :20032 / :20063) and Sounds/roll, the hero's (load :20082, PlayOneShot :20092) at 0; no effect is loaded; the roll forward (6 + 4 sLv m/s, then 4 + 3 sLv after Yield 0.1 :20125, :19870) is left out (the hero does not travel, Bison decision 17); Yield 0.7 (:20123): standby 0.8 s (:19894)",
  "cues": [
    [0, "voice", "roll1|roll2"],
    [0, "sound", "roll"]
  ]
},
"rollAround": {
  "why": "Panda.cs RPC_rollAround (:20159-20700), Roll Around #421 (its own tile, SEQ \"Roll Around: rollAround*^@6\"): clip looped, 0.1 s fade (:20506-20509), removeLockStatus(5) (:20518; again every 0.5 s :20292-20303, gameplay), voice rollAround1 / rollAround2 (Random.Range(0, 2) :20550, loads :20562 / :20593, PlayOneShot :20574 / :20605) and rollAround_ring createEffect at the hero, hero rotation (:20624-20636; followPosition + followState, life 6, its own Sounds/rollAround_ring) at 0; the roll lasts mRollTimer = 6 s (:20650, standby :20425-20442 once Time.time passes it, WaitForFixedUpdate :20672): the ring's life ends there too, so no cut; the steering (:20318-20416) is left out (no travel)",
  "cues": [
    [0, "voice", "rollAround1|rollAround2"],
    [0, "fx", "rollAround_ring"]
  ]
},
"threeSteps": {
  "why": "Panda.cs RPC_threeStep (:20721-21805), Three Steps 2 with Nine Steps #402 on (passives on): clip, 0.2 s fade (:21528), voice nineStep1 / nineStep2 in place of threeStep1 / 2 (getNineStepsLv() != 0 :21569; Random.Range(0, 2) :21575, loads :21587 / :21618, PlayOneShot :21599 / :21630; else :21642-21697) and threeStep createEffect at the hero, rotation x Euler(270, 90, 0) (:21716-21728; followPosition + followState, life 3, its Animation 'root' swings fxNode1-3, its own Sounds/threeSteps) at 0; its three TrailRenderers start disabled (rip prefab m_Enabled 0) and the hero's code switches them (:21742-21748): fxNode1 on at 0.1 (Yield 0.1 :21801, :20873), fxNode2 on at 0.4 (Yield 0.3 :21795, :20900), fxNode1 off at 0.5 (Yield 0.1 :21771, :21063), fxNode2 off at 0.8 (Yield 0.2 :21780 + 0.1 :21776, :21250), fxNode3 on at 1.2 (Yield 0.4 :21785, :21277): the new cue option enable (the part to build); the three hits at 0.4 / 0.7 / 1.3 s reach 1-2 m (FindRecTarget :20938, :21108, :21322; threeStep_hit only on a target, :8399-8412) and Nine Steps' whiteRamp on a hit (:21036) is the camera's: left out; Yield 0.1 (:21803): standby 1.4 s (:21458): threeStep's cut",
  "cues": [
    [0, "voice", "nineStep1|nineStep2"],
    [0, "fx", "threeStep", {"rot": [270, 90, 0], "cut": 1.4, "enable": [[0.1, "fxNode1", true], [0.4, "fxNode2", true], [0.5, "fxNode1", false], [0.8, "fxNode2", false], [1.2, "fxNode3", true]]}]
  ]
},
"rushingFalcon": {
  "why": "Panda.cs RPC_rushingFalcon (:21885-22776), Rushing Falcon 2: clip, 0.2 s fade (:22596), voice rushingFalcon1 / rushingFalcon2 (Random.Range(0, 2) :22637, loads :22649 / :22680, PlayOneShot :22661 / :22692) and rushingFalcon createEffect at the hero, hero rotation (:22711-22721; followPosition + followState, life 2, its rings at 0.3 / 0.5 / 0.7 s are the three hits, its own Sounds/rushingFalcon) at 0; the dash (8 / 6 / 8 / 6 m/s from 0.1 s, :22032, :22059, :22227, :22377) is left out (no travel); hits at 0.3 / 0.5 / 0.7 s within 2 m (:22102, :22240, :22390; rushingFalcon_hit only on a target, :8449-8462); Yields 0.1 / 0.2 / 0.2 / 0.2 / 0.3 (:22754, :22763, :22759, :22767, :22775): standby 1.0 s (:22526): the effect's cut",
  "cues": [
    [0, "voice", "rushingFalcon1|rushingFalcon2"],
    [0, "fx", "rushingFalcon", {"cut": 1.0}]
  ]
},
"towerRush": {
  "why": "Panda.cs RPC_towerRush (:25172-25811), Tower Rush 2 with Ogre Impact #422 on: clip, 0.1 s fade (:25641), voice towerRush1 / towerRush2 (Random.Range(0, 2) :25682, loads :25694 / :25725, PlayOneShot :25706 / :25737) and towerRush_ring Instantiated at the hero, hero rotation (:25756-25766; life 0.5, its own Sounds/towerRush) at 0; Yield 0.1 (:25799): the 16 m/s lunge (:25319, left out: no travel); Yield 0.1 (:25803): at 0.2 s moveSpeed 0 (:25346) and, hasSkill(422) (:25371), towerRush_ogre Instantiated at the hero, hero rotation (:25383-25395; life 1, its own Sounds/towerRush_ogre); the hit FindAreaTarget(pos, 4, 6) (:25424) misses the 10 m target (towerRush_hit only on a target, :8613-8626); Yield 0.3 (:25793): the -4 m/s step back (:25545, left out); Yield 0.3 (:25797): standby 0.8 s (:25571)",
  "cues": [
    [0, "voice", "towerRush1|towerRush2"],
    [0, "fx", "towerRush_ring"],
    [0.2, "fx", "towerRush_ogre"]
  ]
},
"tigerToss": {
  "why": "Panda.cs RPC_tigerToss (:26452-27190), Tiger Toss with Tiger Pounce #232 on, started 0.2 s into RPC_grab when the grabbed target is under 3 m and 60 weight (:26113-26142; SEQ \"Tiger Toss: grab^@0.2 tigerToss!\"; the toss assumes the grab held, as the Mole's Detonate assumes its nuke, plans/fx_mole/decisions.md 27): clip cut in (PlayAnimation(\"tigerToss\", 0) :26959), voice tigerToss1 / tigerToss2 (Random.Range(0, 2) :27003, loads :27015 / :27046, PlayOneShot :27027 / :27058) at 0; Yield 0.6 (:27127): tigerToss Instantiated at the hero + 1.2 m up, hero rotation (:26621-26633; life 2, its own Sounds/tigerToss) and the throw (:26675); Yield 0.1 (:27134): at 0.7 s Tiger Pounce's RPC_tigerPounce_hit at the thrown target's position, LookRotation(the hero's forward) (getTigerPounceLv :26758, :26771; Instantiate :8677-8690; its own Sounds/tigerPounce), here the grabbed target's spot 1 m ahead on the floor (the grab box FindRecTarget(pos, forward, 1, 1, 1, 3) :26073; question 2); the 3 m/s walk (:26968) left out; Yield 0.1 (:27132): standby 0.8 s (:26889)",
  "cues": [
    [0, "voice", "tigerToss1|tigerToss2"],
    [0.6, "fx", "tigerToss", {"y": 1.2}],
    [0.7, "fx", "tigerPounce_hit", {"d": 1}]
  ]
},
"risingVortex": {
  "why": "Panda.cs RPC_risingVortex (:28672-29351), Rising Vortex 2: clip, 0.2 s fade (:29136), voice risingVortex1 / risingVortex2 (Random.Range(0, 2) :29177, loads :29189 / :29220, PlayOneShot :29201 / :29232) and risingVortex createEffect at the hero, hero rotation (:29251-29261; followPosition + followState, life 2, its own Sounds/risingVortex) at 0; the pulls at 0.4 / 0.6 s reach 3 m (FindAreaTarget :28832, :28947; Yield 0.4 :29303, 0.2 :29288; risingVortex_hit only on a target :28861, :28976); Yield 0.1 + 0.3 (:29294, :29299): standby 1.0 s (:29066): the effect's cut",
  "cues": [
    [0, "voice", "risingVortex1|risingVortex2"],
    [0, "fx", "risingVortex", {"cut": 1.0}]
  ]
},
"risingDragons": {
  "why": "Panda.cs RPC_risingDragons (:29356-30282), Rising Dragons 2: clip, 0.2 s fade (:30112), noForce 3 s (:30124), voice risingDragon1 / risingDragon2 (Random.Range(0, 2) :30156, loads :30166 / :30197, PlayOneShot :30258 / :30269) at 0; Yield 0.1 (:30240): risingDragon_ring createEffect at the hero, hero rotation (:29509-29521; followPosition, life 4, its own Sounds/risingDragons) and the owner's 10 s deltaRamp (:29548, camera: left out); Yield 0.2 (:30244): the 0.3 s lock within 3 m (:29580-29625, no look); Yield 0.1 (:30242): at 0.4 s risingDragon createEffect at the hero, hero rotation (:29665-29677; followPosition + followState, life 2.4 + 1, the flying dragon's SkinnedMesh and Animation) and a camera shake (:29699, left out); Yield 0.2 (:30256): eight uppercuts every 0.15 s from 0.6 s within 3 m (i < 8 :29974, :30010, Yield 0.15 :30263; risingDragon_hit only on a target :30039); Yield 0.3 (:30277): at 2.1 s the finisher, ashuraFist Instantiated at the hero, Quaternion.identity (:29770-29782; its own Sounds/ashuraFist), within 4 m (:29821), the -4 m/s step back (:29759, left out); Yield 0.4 + 0.1 (:30275, :30248): standby 2.6 s (:29922): risingDragon's cut",
  "cues": [
    [0, "voice", "risingDragon1|risingDragon2"],
    [0.1, "fx", "risingDragon_ring"],
    [0.4, "fx", "risingDragon", {"cut": 2.6}],
    [2.1, "fx", "ashuraFist"]
  ]
},
"waterMonkey": {
  "why": "Panda.cs RPC_waterMonkey (:32706-33330), Water Monkey 2 with Time and Tide #413 on: clip, 0.2 s fade (:33118), voice waterMonkey1 / waterMonkey2 (Random.Range(0, 2) :33159, loads :33171 / :33202, PlayOneShot :33183 / :33214) and, getTimeAndTideLv() > 0 (:33227), timeAndTideMonkey createEffect at the hero, hero rotation (:33237-33247; life 2, the shadow clone's SkinnedMesh + AlphaTimer, its own Sounds/waterMonkey) in place of waterMonkey (:33272-33282) at 0; Yield 0.2 (:33323): the 3 m/s step (:32853, left out); Yield 0.3 (:33315): two hits at 0.5 / 0.7 s 1-2 m ahead (FindRecTarget :33020, Yield 0.2 :33311; waterMonkey_hit only on a target :33059); standby 0.9 s (:32964)",
  "cues": [
    [0, "voice", "waterMonkey1|waterMonkey2"],
    [0, "fx", "timeAndTideMonkey"]
  ]
},
"waterCrane": {
  "why": "Panda.cs RPC_waterCrane (:33382-33990), Water Crane 2 with Time and Tide #413 on: clip, 0.2 s fade (:33675), voice waterCrane1 / waterCrane2 (Random.Range(0, 2) :33724, loads :33736 / :33767, PlayOneShot :33748 / :33779) and, getTimeAndTideLv() > 0 (:33792), timeAndTideCrane createEffect at the hero, hero rotation (:33804-33816; followPosition + followState, life 3, the shadow clone, its own Sounds/waterCrane) in place of waterCrane (:33841-33853) at 0; Yield 0.7 (:33975): two pulses at 0.7 / 0.9 s within 5 m (4 + Spirit Fist #433, FindAreaTarget :33886, Yield 0.2 :33983; waterCrane_hit only on a target :33921); Yield 0.6 (:33985): standby 1.7 s (:33593): the effect's cut",
  "cues": [
    [0, "voice", "waterCrane1|waterCrane2"],
    [0, "fx", "timeAndTideCrane", {"cut": 1.7}]
  ]
},
"stasisBlow": {
  "why": "The stasisBlow clip: Stasis Blow (RPC_stasisBlow, PlayAnimation(\"stasisBlow\", 0.2) Panda.cs:34612) and Death Blow (RPC_deathBlow, the same clip :35430), one per play, even chance, picked anew on every play (one tile each, poolChains); both the same timeline: 3 m/s, Wind Walker #423's warp at 0.2 s when the spot 3 m short of the target is over 6 m away (:34192-34198, :35009-35015; with the 10 m target it is 7 m: left out, the hero does not travel), 10 m/s from 0.3 s, the hit at 0.5 s, 4 m/s from 0.6 s, standby 0.8 s; RPC_stasisBlow_hit and RPC_deathBlow_hit are empty in BB (:9125, :9138) and TTO (one stub, TTO1102 methods.tsv 0x33b5c0): no hit look in either game",
  "skills": {
    "stasisBlow": {
      "why": "Panda.cs RPC_stasisBlow (:34040-34789), Stasis Blow 2: clip, 0.2 s fade (:34612), voice stasisBlow1 / stasisBlow2 (Random.Range(0, 2) :34653, loads :34665 / :34696, PlayOneShot :34677 / :34708) and stasisBlow_ring createEffect at the hero, hero rotation (:34727-34737; followState, life 2, its own Sounds/stasisBlow) at 0; Yield 0.2 (:34770): stasisBlow createEffect at the hero, rotation x Euler(270, 90, 0) (:34212-34224; followPosition + followState, life 1, its two trails swung by its Animation); Yield 0.1 (:34768), Yield 0.2 (:34777): the hit at 0.5 s (FindRecTarget from 2 m behind, 5 m long with Spirit Fist, :34312; paralysis :34361-34394; RPC_stasisBlow_hit :34401, empty); Yield 0.1 (:34784): stasisBlow_endDust Instantiated at the hero, hero rotation (:34464-34476; life 0.5); Yield 0.2 (:34779): standby 0.8 s (:34524): the cut of both followState effects",
      "cues": [
        [0, "voice", "stasisBlow1|stasisBlow2"],
        [0, "fx", "stasisBlow_ring", {"cut": 0.8}],
        [0.2, "fx", "stasisBlow", {"rot": [270, 90, 0], "cut": 0.8}],
        [0.6, "fx", "stasisBlow_endDust"]
      ]
    },
    "deathBlow": {
      "why": "Panda.cs RPC_deathBlow (:34851-35610), Death Blow 2: clip stasisBlow, 0.2 s fade (:35430), voice deathBlow1 / deathBlow2 (Random.Range(0, 2) :35471, loads :35483 / :35514, PlayOneShot :35495 / :35526) and deathBlow_ring Instantiated at the hero, hero rotation (:35545-35555; life 2, its own Sounds/stasisBlow) at 0; Yield 0.2 (:35586): deathBlow createEffect at the hero, rotation x Euler(270, 90, 0) (:35027-35039; followPosition + followState, life 1); Yield 0.1 (:35601), Yield 0.2 (:35592): the hit and the lckAdjust(20 sLv) kill roll at 0.5 s (:35128, :35205; RPC_deathBlow_hit :35219, empty); Yield 0.1 (:35606): stasisBlow_endDust Instantiated at the hero, hero rotation (:35282-35294); Yield 0.2 (:35608): standby 0.8 s (:35342): deathBlow's cut",
      "cues": [
        [0, "voice", "deathBlow1|deathBlow2"],
        [0, "fx", "deathBlow_ring"],
        [0.2, "fx", "deathBlow", {"rot": [270, 90, 0], "cut": 0.8}],
        [0.6, "fx", "stasisBlow_endDust"]
      ]
    }
  }
},
"spTransfer": {
  "why": "Panda.cs RPC_spTransfer (:35899-36480), Sp Transfer 2 (a friendly target, never the Panda herself: :6717-6728, so the ally stands at the 10 m point, as the Sheep's Revive / Gleaming Breath, plans/fx_sheep/decisions.md 1, 4): clip, 0.2 s fade (:36168), voice spTransfer1 / spTransfer2 (Random.Range(0, 2) :36219, loads :36231 / :36263, PlayOneShot :36459 / :36473) at 0; Yield 0.5 (:36457): spTransfer (a BoltEmitter) Instantiated at the hero + TransformDirection(0, 0.4, 0.5), Quaternion.identity (:36062-36080), its TargetPosition the ally's collider.bounds.center every frame (:36441: the 10 m target 0.6 m up, plans/fx_penguin/decisions.md 3: to); mTransferTime 0.3 s later (:36090): Destroy (:36300), the SP heal (:36329), standby 0.8 s (:36354)",
  "cues": [
    [0, "voice", "spTransfer1|spTransfer2"],
    [0.5, "fx", "spTransfer", {"y": 0.4, "d": 0.5, "to": [0, 0.6, 10], "kill": 0.3}]
  ]
},
"@RaijinKen:cAttack1": {
  "why": "Panda.cs RPC_raijinKen (:41542-42250), Raijin Ken #444, its first step (SEQ \"Raijin Ken: cAttack1!@0.7 cAttack2*!@4.3 raijinKen1!@1.7 raijinKen2!\"): cAttack1 cut in (PlayAnimation(\"cAttack1\", 0) :42066), voice raijinKen1 / raijinKen2 (Random.Range(0, 2) :42107, loads :42119 / :42150, PlayOneShot :42131 / :42162; the rip's files are raijinken1 / 2.wav, Resources is case-blind) and raijinKen_ring1 createEffect at the hero, hero rotation (:42181-42191; followPosition + followState, life 5: it ends at 5.0 s, when raijinKen1 starts, its own looping Sounds/raijinken1; no cut, so the step change at 0.7 s keeps it) at 0; Yield 0.7 (:42228): cAttack2",
  "cues": [
    [0, "voice", "raijinKen1|raijinKen2"],
    [0, "fx", "raijinKen_ring1"]
  ]
},
"@RaijinKen:cAttack2": {
  "why": "Panda.cs RPC_raijinKen, its second step: cAttack2 cut in and looped at 0.7 s (:41688-41693), facing the target each frame (:42023, YieldDefault :42224) until Time.time >= actionTime + 5 (:41896; actionTime = the cast, :42051; TTO1102 Panda.<RPC_raijinKen>d__236 the same =5): 4.3 s; nothing new is spawned (this key keeps the Charge Attack's cAttack2 cues off the Raijin Ken tile)",
  "cues": []
},
"raijinKen1": {
  "why": "Panda.cs RPC_raijinKen, at 5.0 s: raijinKen1 cut in (PlayAnimation(\"raijinKen1\", 0) :41912), raijinKen_ring2 createEffect at the hero, hero rotation (:41928-41940; followPosition, life 3, its own Sounds/raijinken2) and voice nAttack3, no pick (load :41991, PlayOneShot :42244) at 0; Yield 0.5 (:42220): at 0.5 s the leap's hide status 1 s (:41732, gameplay) and RPC_raijinKen_hit at fPos = the target's bounds centre - extents.x x the flat direction (:41753-41763): the 10 m target's front, (0, 0.6, 9.7) (centre 0.6 m up, radius 0.3: plans/fx_bat/decisions.md 3), raijinKen_hit createEffect there, LookRotation(-hitDir) = facing the hero (:42515-42525; its Animation flies the kicking Panda image from (0, 15, 11) to its root in 0.433 s; its ParticleSystem from TTO's copy, SHURIKEN_FROM_TTO; its effectCamera (:42546-42553), the whiteRamp (:42464) and the 8 m blast 0.4 s later (:42421) are the camera's and gameplay: left out); Yield 1.2 (:42242): raijinKen2",
  "cues": [
    [0, "fx", "raijinKen_ring2"],
    [0, "voice", "nAttack3"],
    [0.5, "fx", "raijinKen_hit", {"d": 9.7, "y": 0.6, "rot": [0, 180, 0]}]
  ]
},
"raijinKen2": {
  "why": "Panda.cs RPC_raijinKen, at 6.7 s: raijinKen2 cut in (PlayAnimation(\"raijinKen2\", 0) :41813), moveSpeed 0 (:41808); Yield 0.8 (:42218): standby at 7.5 s (:41844); nothing is spawned (the entry records the step)",
  "cues": []
}
}
```

### Paste-ready lines beside the cues

- `wardrobe/index.html` SEQ.panda:
  - Replace `"Raijin Ken: cAttack1 cAttack2* raijinKen1 raijinKen2"` with `"Raijin Ken: cAttack1!@0.7 cAttack2*!@4.3 raijinKen1!@1.7 raijinKen2!"`.
  - Add `"Tiger Toss: grab^@0.2 tigerToss!"` and `"Roll Around: rollAround*^@6"`.
  - Anchor by text: the file is being edited. After any edit, `grep -c $'\r$' wardrobe/index.html` must print 0.
- `wardrobe/index.html` SEQ_SKILL: `panda: { "@RaijinKen": "raijinKen", "@TigerToss": "tigerToss" },`
- `pipeline/wardrobe_skill_icons.py` CLIP_SKILLS:
  ```python
      # the Panda's stasisBlow clip is Stasis Blow and Death Blow (RPC_deathBlow plays it, Panda.cs:35430; plans/fx_panda/skills_b.md)
      "panda": {"stasisBlow": ["stasisBlow", "deathBlow"]},
  ```
  skills_a may add `grab` to the same dict.
- `pipeline/wardrobe_fx.py` SHURIKEN_FROM_TTO: `"panda": ["raijinKen_hit"]`. Graft_by_material route, no SHURIKEN_MAT entry (probe2.txt).
- `pipeline/wardrobe_fx_check.py` OPTS: `+ "enable"` (threeStep's trail switches).

## Decisions taken by analogy (the user is away; for the review)

1. No travel (Bison 17, Mole 28): every dash, step back, roll, steer and warp is left out; effects at the standing hero.
2. Hits drawn only where the reach meets the 10 m target (Bison 16, Mole 29): none in this half except Raijin Ken's, which the game puts at the target.
3. Raijin Ken's hit at the target's front `{d 9.7, y 0.6}`, facing the hero (Bat 3, Penguin 4).
4. Sp Transfer's ally 10 m ahead, the bolt to its bounds centre (Sheep 1 and 4's exception: the skill cannot target the Panda herself; Penguin 3).
5. Tiger Toss shows the successful toss (Mole 27), with the Pounce at the grabbed spot 1 m ahead.
6. Passives on (Nine Steps, Time and Tide, Ogre Impact, Tiger Pounce, Wind Walker, Spirit Fist): their looks replace the base ones.
7. Camera effects left out (Mole 51): Nine Steps' whiteRamp, Rising Dragons' deltaRamp and shakes, Raijin Ken's effectCamera and whiteRamp.
8. Roll Around held 6 s per round, as the game's timer.
9. Raijin Ken's timeline from the code (BB = TTO), not the Bible's prose.

## Open questions (each with my recommendation)

1. **Raijin Ken's length.**
   - The code holds the charge to 5 s, so the tile runs 7.5 s; the Bible says ~2.4 s.
   - Recommended: the code (`cAttack2*!@4.3`). BB :41896 and TTO1102's `=5` agree.
   - Alternative: keep the page's 1.5 s hold. The hit would then come 3.3 s too early against the game.
2. **Tiger Pounce's spot.**
   - Recommended: 1 m ahead on the floor, the grab box's far edge where the grabbed target stands. The 0.1 s of its throw before the splash is not modelled.
   - Alternatives: leave the splash out (no target is ever in reach of the 10 m point, so the game would play grab only), or put it at the 10 m target.
3. **Tiger Toss's tile.**
   - Recommended: `"Tiger Toss: grab^@0.2 tigerToss!"`. It plays the whole cast, the grab clip first, as the game does.
   - skills_a owns `grab`. With the 10 m target taken as small and light, the grab branches to the toss; Climbing Cliff and Crumbling Mountain need a target 3 m tall and are their own tiles from the same grab.
   - Without the line, tigerToss stays a single tile and the cues still fit (they are keyed by tigerToss).
4. **Wind Walker's warp** (Stasis / Death Blow).
   - With the 10 m target the game warps the Panda 7 m forward at 0.2 s, and the blow then lands on the target.
   - Recommended: no warp (no travel). Nothing is lost: the warp has no look, and the hit RPCs draw nothing.
5. **Roll Around.**
   - Recommended: the 6 s SEQ, so each round recasts the voice and ring.
   - Without it, the looped clip plays on with the ring gone after 6 s.
6. **Three Steps' trails.**
   - Recommended: build `enable`. The tile's whole look is the three fist trails, and without the part they never draw.
7. **Sp Transfer's bolt end.**
   - Recommended: the ally's centre (0, 0.6, 10).
   - Alternative: the Panda herself. The bolt would have no length.

## Possible Bible findings (offer to the user; none written there)

1. **Raijin Ken's timeline:**
   - cAttack1 0.7 s, then cAttack2 held until 5 s after the cast (Panda.cs:41896; TTO1102 the same).
   - raijinKen1 at 5.0 with voice nAttack3, the hit look at 5.5, its 8 m blast at 5.9 (RPC_raijinKen_hit's 0.4 s wait, :42587).
   - raijinKen2 at 6.7, standby 7.5.
   - The reference's "Charge-up 2: 0.5 s ... Total ~2.4 s" takes the 0.5 s wait after raijinKen1 for the charge.
2. **Water Monkey's two scans are 0.2 s apart** (0.5 / 0.7 s: Yield 0.2 + 0.3, then 0.2, :33323, :33315, :33311). The reference says "0.7 seconds apart".
3. **Water Crane's two pulses are 0.2 s apart** (0.7 / 0.9 s, :33975, :33983). Its section says "separated by 0.7 seconds"; its own hit-timing section has 0.7 / 0.9.
4. **Stasis Blow and Death Blow draw no hit effect:** RPC_stasisBlow_hit / RPC_deathBlow_hit are empty in BB (:9125, :9138) and TTO.
5. **Nine Steps changes Three Steps' voice** to nineStep1|2 (:21569). Time and Tide changes Water Monkey's / Water Crane's effect to the shadow-clone versions (:33227, :33792).
6. Death Blow plays the stasisBlow clip and Stasis Blow's end dust (:35430, :35282).

## Verification (13/11/2026)

Checker, office PC. Re-derived from `C:\Users\Jump\Desktop\12tails\DecompiledSource\Panda.cs` and `CharacterControl.cs`,
the probe (`wardrobe_fx.py panda --probe` of all 50 effects named by skills_a + skills_b, plus windCloud, rainStorm,
windcloud_hit: all decode, every component is one the page has), the rip's `heroes/panda/voices` and `sounds` folders,
`wardrobe/index.html` (cue format, SEQ grammar, poolChains, fxStart, SEQ_SKILL), `pipeline/wardrobe_fx_check.py` and
`pipeline/wardrobe_skill_icons.py`. Probes: `checks\fx_panda_research\verify\` (`co.sh` = a coroutine's key lines,
`ymap.py` = which Yield each `case` reaches, `blocks.py` = the JSON checks, `probe*.json`, `b_new.json` = the corrected
blocks below, JSON-checked, times sorted). The Verification wins over the report body.

**Confirmed** (no change): every clip time (the coroutines' waits added up: roll 0.8; Roll Around's 6 s timer :20650;
Three Steps 0.1 + 0.3 + 0.1 + 0.2 + 0.1 + 0.4 + 0.1 + 0.1 = 1.4 and its five trail switches :20873-:21277; Rushing
Falcon 1.0; Tower Rush 0.2 / 0.8; Tiger Toss 0.6 / 0.7 / 0.8; Rising Vortex; Rising Dragons; Stasis / Death Blow
0.2 / 0.5 / 0.6 / 0.8; Sp Transfer's bolt and its 0.3 s Destroy :36290-:36300; Raijin Ken 0 / 0.7 / 5.0 (:41896) /
5.5 / 6.7 / 7.5). Every effect's EffectControl is as cited (life, followPosition / followState; threeStep's fxNode1-3
are `m_Enabled` false, stasisBlow's / deathBlow's trails true). Every voice and sound file exists (raijinken1 / 2 in
lower case, found case-free; the mp3 takes the cue's spelling, wardrobe_fx.py:908). The block is valid JSON, 16 keys /
39 cues; its keys are Panda clips or the existing "@RaijinKen" SEQ's; `enable` is the one new option (OPTS lacks it, as
said). Raijin Ken's hit spot (0, 0.6, 9.7) facing the hero is right. No released TTO skill plays these clips.

1. **Missed: two BB skills, Wind & Cloud and Rain & Storm.** Both play a body clip, so they belong to this half
   (between raijinKen and waterMonkey). effect_only.md items 1 and 4 handed them to the clip researchers, and
   clip_calls.js misses them because of the `&`.
   - **Evidence:** RPC_windCloud :36529-38146 plays `PlayAnimation("wind&cloud", 0.2f)` (:37811); RPC_rainStorm
     :38147-39065 plays `"rain&storm"` (:38839). Both are dispatched from doSkill (:6607, :6627) and are in TTO1102 too
     (pseudo/Panda.c has both strings). The Bible has their cards and icons (`panda_wind&cloud2`, `panda_rain&storm2`,
     bible/index.html:19286-19287, assets.js).
   - **Timelines** (each `case k` reaches Yield(k + 1) in order, ymap.py; the start reaches Yield(2, 0.3) :38004 /
     Yield(2, 0.2) IL_115E):
     - **Wind & Cloud:**
       - At 0: the voice and Sounds/windCloud.
       - `windCloud` (life 2, no follow, Instantiate, Quaternion.identity) at 0.3 / 0.6 (d 0.5), 0.9 (at the hero),
         1.2 / 1.5 (x -0.3), 1.7 (at the hero), 2.1 (x 0.3), 2.5 (x 0.5) and 2.9 / 3.0 (d 0.4).
       - Sounds/punch1 (punch1Fx = sounds/punch1, attacks_emotes.md:20) with each of those from 0.6 on.
       - Nine 4 m strikes at 0.6, 0.9, 1.5, 1.7, 2.1, 2.5, 2.9, 3.0 and 3.2. None reaches 10 m, and there is no hit RPC.
       - Standby at 3.3.
     - **Rain & Storm:**
       - At 0: the voice.
       - `rainStorm` (createEffect, followPosition + followState, life 2 + 1, its own sound) at the hero at 0.2, 0.7,
         1.3, 1.9 and 2.2.
       - Four 6 m pulses at 0.7, 1.3, 1.9 and 2.2.
       - Standby at 2.8, which is every ring's cut.
   - **Parts to build** (the rule: built, never left out):
     - `pipeline/wardrobe_data.py:210`:
       - The clip filter `[a-z0-9_]+` drops any `&` name. Make it `[a-z0-9_&]+` and rebuild the Panda's data.
       - That build reads the game rips / TTO's catalog, so it runs at the home PC: a HANDOFF.md item, then commit the
         changed `wardrobe/data/panda/clips.json`.
       - Check there that both clips land. If TTO's catalog spells them differently, follow its spelling and key the
         cues by it.
     - `pipeline/wardrobe_skill_icons.py:95`:
       - The Bible-key pattern `{cls}_([A-Za-z]+?)(\d*)` drops `panda_wind&cloud2` / `panda_rain&storm2`. Make it
         `([A-Za-z&]+?)`; the clip strips to `wind&cloud`, which then matches.
       - The icon file is `icons/hd/panda/wind&cloud.webp`. `&` is a legal URL path character, and in the tile's
         unescaped attributes (`data-m`, the ring's `url()`) `&cloud` / `&storm` are not character references, so it
         renders. Check the tile.
     - **SEQ:**
       - No SEQ line is needed (each is one clip).
       - If the rebuilt clip is shorter than its standby (3.3 s / 2.8 s), the single tile would lose the late cues. Then
         a SEQ line `"Wind & Cloud: wind&cloud@3.3"` / `"Rain & Storm: rain&storm@2.8"` holds it, and SEQ_ALT
         (index.html:1388) must take `([\w&]+)` for the clip.
     - Both effects are ready (probe: one RingEmitter each). No new cue option is needed.
   - **Paste-ready entries** (add them to the block). `rot`: none. The game's Quaternion.identity is the hero's facing
     in the wardrobe, as with Ashura Fist in skills_a.

```json
{
  "wind&cloud": {
    "why": "Panda.cs RPC_windCloud (:36529-38146, dispatch :6627; the Bible's Wind & Cloud #351-352, max rank 2, Spirit Fist #433 on): clip wind&cloud, 0.2 s fade (PlayAnimation :37811, WrapMode.Once :37814), voice windCloud1 / windCloud2 (Random.Range(0, 2) :37852, loads :37864 / :37895) and Sounds/windCloud, the hero's (load :37926, PlayOneShot :37938) at 0; the states run 2 -> 14 in order (each case's goto reaches Yield(k + 1), checked by checks/fx_panda_research/verify/ymap.py): Yield 0.3 (:38004) -> 0.3 s windCloud Instantiated at position + 0.5 x forward, Quaternion.identity (:36687-36699; EffectControl 2, no follow, a RingEmitter) and moveSpeed 3 (not travelled); Yield 0.3 -> 0.6 s windCloud at + 0.5 forward (:36742), Sounds/punch1 (punch1Fx, own client :36754) and strike 1; 0.9 s (Yield 0.3) stop, windCloud at the hero (:36851), punch1 (:36863), strike 2; 1.2 s (Yield 0.3) windCloud at - 0.3 x right (:36960), punch1 (:36974); 1.5 s (Yield 0.3) windCloud at - 0.3 right (:37012), punch1 (:37024), strike 3; 1.7 s (Yield 0.2) windCloud at the hero (:37116), punch1 (:37128), strike 4; 2.1 s (Yield 0.4) windCloud at + 0.3 right (:37220), punch1 (:37232), strike 5; 2.5 s (Yield 0.4) windCloud at + 0.5 right (:37324), punch1 (:37336), strike 6; 2.8 s (Yield 0.3) moveSpeed 2 (:37422); 2.9 s (Yield 0.1) windCloud at + 0.4 forward (:37455), punch1 (:37467), strike 7; 3.0 s (Yield 0.1) windCloud at + 0.4 forward (:37559), punch1 (:37571), strike 8; 3.2 s (Yield 0.2) stop, strike 9 (:37670), no effect; 3.3 s (Yield 0.1) standby (:37741); the nine strikes FindAreaTarget(hero, (3 + 1) m) (:36768 ...) never reach the 10 m target and have no hit look (no hit RPC; windcloud_hit is loaded by no code, plans/fx_panda/parts.md:87); the 30 % evasion (CharacterControl.cs:3170-3203) draws nothing",
    "cues": [
      [
        0,
        "voice",
        "windCloud1|windCloud2"
      ],
      [
        0,
        "sound",
        "windCloud"
      ],
      [
        0.3,
        "fx",
        "windCloud",
        {
          "d": 0.5
        }
      ],
      [
        0.6,
        "fx",
        "windCloud",
        {
          "d": 0.5
        }
      ],
      [
        0.6,
        "sound",
        "punch1"
      ],
      [
        0.9,
        "fx",
        "windCloud"
      ],
      [
        0.9,
        "sound",
        "punch1"
      ],
      [
        1.2,
        "fx",
        "windCloud",
        {
          "x": -0.3
        }
      ],
      [
        1.2,
        "sound",
        "punch1"
      ],
      [
        1.5,
        "fx",
        "windCloud",
        {
          "x": -0.3
        }
      ],
      [
        1.5,
        "sound",
        "punch1"
      ],
      [
        1.7,
        "fx",
        "windCloud"
      ],
      [
        1.7,
        "sound",
        "punch1"
      ],
      [
        2.1,
        "fx",
        "windCloud",
        {
          "x": 0.3
        }
      ],
      [
        2.1,
        "sound",
        "punch1"
      ],
      [
        2.5,
        "fx",
        "windCloud",
        {
          "x": 0.5
        }
      ],
      [
        2.5,
        "sound",
        "punch1"
      ],
      [
        2.9,
        "fx",
        "windCloud",
        {
          "d": 0.4
        }
      ],
      [
        2.9,
        "sound",
        "punch1"
      ],
      [
        3.0,
        "fx",
        "windCloud",
        {
          "d": 0.4
        }
      ],
      [
        3.0,
        "sound",
        "punch1"
      ]
    ]
  },
  "rain&storm": {
    "why": "Panda.cs RPC_rainStorm (:38147-39065, dispatch :6607; the Bible's Rain & Storm #353-354, max rank 2, Spirit Fist #433 on): clip rain&storm, 0.2 s fade (PlayAnimation :38839) and voice rainStorm1 / rainStorm2 (Random.Range(0, 2) :38880, loads :38890 / :38921, PlayOneShot :38972 / :38987) at 0; the states run 2 -> 8 in order (checks/fx_panda_research/verify/ymap.py): Yield 0.2 (IL_115E) -> 0.2 s moveSpeed 3 (:38294, not travelled) and rainStorm createEffect at the hero, Quaternion.identity (:38305-38317; EffectControl 2 + 1, followPosition, followState, a RingEmitter, its own Sounds/rainStorm); Yield 0.5 -> 0.7 s rainStorm (:38360) and pulse 1; Yield 0.6 -> 1.3 s rainStorm (:38468), pulse 2; Yield 0.6 -> 1.9 s moveSpeed 4 (:38554), rainStorm (:38565), pulse 3; Yield 0.3 -> 2.2 s rainStorm (:38657), pulse 4; Yield 0.2 -> 2.4 s stop (:38743); Yield 0.4 -> 2.8 s standby (:38769): every rainStorm's followState cut 2.8; the pulses FindAreaTarget(hero, (5 + 1) m) (:38390 ...) never reach the 10 m target and have no hit look; the 30 % evasion draws nothing",
    "cues": [
      [
        0,
        "voice",
        "rainStorm1|rainStorm2"
      ],
      [
        0.2,
        "fx",
        "rainStorm",
        {
          "cut": 2.8
        }
      ],
      [
        0.7,
        "fx",
        "rainStorm",
        {
          "cut": 2.8
        }
      ],
      [
        1.3,
        "fx",
        "rainStorm",
        {
          "cut": 2.8
        }
      ],
      [
        1.9,
        "fx",
        "rainStorm",
        {
          "cut": 2.8
        }
      ],
      [
        2.2,
        "fx",
        "rainStorm",
        {
          "cut": 2.8
        }
      ]
    ]
  }
}
```

   - **Bible findings to offer:** the reference's timing table (panda-skill-reference.md:944-945) starts both skills'
     hits one wait early.
     - Wind & Cloud's hits come 0.6, 0.9, 1.5, 1.7, 2.1, 2.5, 2.9, 3.0 and 3.2 s after the cast, not 0.3 ... 2.9. The
       table leaves out the 0.3 s wait before the first state (:38004).
     - Rain & Storm's come at 0.7, 1.3, 1.9 and 2.2, not 0.5 ... 2.0 (the 0.2 s wait).

2. **Raijin Ken hides the Panda for 1 s at 5.5 s.** The report left this out as "gameplay".
   - **Evidence:**
     - `addStatus("hide", 1, 1, ...)` at the leap (Panda.cs:41732, the same state as the hit spawn).
     - The status apply disables every Renderer under the hero (CharacterControl.cs:32818-32840), and the removal
       enables them again (:14547-14560).
     - So it is a look: the Panda vanishes while raijinKen_hit's Panda image does the kick.
   - **Correction:** a `hideProp` "hero" cue for 1 s (the Chameleon's Thunder Dragon, its decision 49). The raijinKen1
     entry in full:

```json
{
  "raijinKen1": {
    "why": "Panda.cs RPC_raijinKen, at 5.0 s: raijinKen1 cut in (PlayAnimation(\"raijinKen1\", 0) :41912), raijinKen_ring2 createEffect at the hero, hero rotation (:41928-41940; followPosition, life 3, its own Sounds/raijinken2) and voice nAttack3, no pick (load :41991, PlayOneShot :42244) at 0; Yield 0.5 (:42220): at 0.5 s the leap's hide status for 1 s (addStatus(\"hide\", 1, 1) :41732, while actionState attack and myCommand raijinKen): its apply disables every Renderer under the hero (CharacterControl.cs:32818-32840), its removal enables them again (:14547-14560): the hero hidden 1 s, hideProp hero kill 1 (the Chameleon's Thunder Dragon, plans/fx_chameleon/decisions.md 49); and RPC_raijinKen_hit at fPos = the target's bounds centre - extents.x x the flat direction (:41753-41763): the 10 m target's front, (0, 0.6, 9.7) (centre 0.6 m up, radius 0.3: plans/fx_bat/decisions.md 3, 4), raijinKen_hit createEffect there, LookRotation(-hitDir) = facing the hero (:42515-42525; its Animation flies the kicking Panda image down to its root in 0.433 s while the hero is hidden; its ParticleSystem from TTO's copy, SHURIKEN_FROM_TTO; its effectCamera (:42546-42553), the whiteRamp (:42464) and the 8 m blast 0.4 s later (:42421) are the camera's and gameplay: left out); Yield 1.2 (:42242): raijinKen2",
    "cues": [
      [
        0,
        "fx",
        "raijinKen_ring2"
      ],
      [
        0,
        "voice",
        "nAttack3"
      ],
      [
        0.5,
        "fx",
        "raijinKen_hit",
        {
          "d": 9.7,
          "y": 0.6,
          "rot": [
            0,
            180,
            0
          ]
        }
      ],
      [
        0.5,
        "hideProp",
        "hero",
        {
          "kill": 1
        }
      ]
    ]
  }
}
```

3. **Tiger Pounce's splash goes to the 10 m target point, not 1 m ahead** (question 2, answered the other way).
   - **Why:**
     - The standing rule puts effects on an enemy at the target point 10 m ahead.
     - skills_a puts the very same grabbed target there: its Crushing Monolith doubles stand at d 9.6 / 10 (skills_a
       Q4: "the 10 m rule as written").
     - One grabbed target needs one spot, so both use 10 m.
   - **The spot:** the splash is at the thrown target's position, LookRotation(forward) (:26771, :8690): d 10, no rot.
     The tigerToss entry in full:

```json
{
  "tigerToss": {
    "why": "Panda.cs RPC_tigerToss (:26452-27190), Tiger Toss with Tiger Pounce #232 on, started 0.2 s into RPC_grab when the grabbed target is under 3 m and 60 weight (:26113-26142; SEQ \"Tiger Toss: grab@0.2 tigerToss\"; the toss assumes the grab held, as the Mole's Detonate assumes its nuke, plans/fx_mole/decisions.md 27): clip cut in (PlayAnimation(\"tigerToss\", 0) :26959), voice tigerToss1 / tigerToss2 (Random.Range(0, 2) :27003, loads :27015 / :27046) at 0; Yield 0.6 (:27127): tigerToss Instantiated at the hero + 1.2 m up, hero rotation (:26621-26633; life 2, its own Sounds/tigerToss) and the throw (removeStatus grab); Yield 0.1 (:27134): at 0.7 s Tiger Pounce's RPC_tigerPounce_hit at the thrown target's position, LookRotation(the hero's forward) (getTigerPounceLv :26758; Instantiate :8677-8690; its own Sounds/tigerPounce): an effect on the enemy, so at the 10 m target point (the standing rule; the same grabbed target skills_a's Crushing Monolith doubles stand at), d 10; the 3 m/s walk (:26968) left out; Yield 0.1 (:27132): standby 0.8 s (:26889)",
    "cues": [
      [
        0,
        "voice",
        "tigerToss1|tigerToss2"
      ],
      [
        0.6,
        "fx",
        "tigerToss",
        {
          "y": 1.2
        }
      ],
      [
        0.7,
        "fx",
        "tigerPounce_hit",
        {
          "d": 10
        }
      ]
    ]
  }
}
```

4. **The CLIP_SKILLS line `"panda": {"stasisBlow": ["stasisBlow", "deathBlow"]}` is not needed** (skills_b.md:403).
   - wardrobe_skill_icons.py already gives every member of a cue-file pool its own icon (the `pools` loop, :115-133).
     `deathBlow` is in `best` as panda_deathBlow2.
   - Drop the line. The Penguin's and the Sheep's pools carry no such line either.

5. **SEQ lines and SEQ_SKILL, merged with skills_a:**
   - **Tiger Toss:** skills_a writes `"Tiger Toss: grab@0.2 tigerToss"`, this report `"grab^@0.2 tigerToss!"`.
     - They play the same. A first step always fades in over 0.2 s unless it is marked `!` (index.html:1519, :1551: a
       `^` there is not read), and a later step with no mark is a cut.
     - Use skills_a's form, the same as its Climbing Cliff / Crumbling Mountain lines.
   - **Roll Around:** `"Roll Around: rollAround*^@6"` plays the same as `rollAround*@6` for the same reason; either is
     fine.
   - **SEQ_SKILL:** one panda entry for both halves and effect_only.md:
     `panda: { "@QiStrike": "qiStrike", "@RaijinKen": "raijinKen", "@TigerToss": "tigerToss", "@MysticSage": "mysticSage",
     "@SafeGuard": "safeGuard", "@SacredSageTechnique": "sacredSageTechnique", "@DelayQi": "delayQi" }`.

Corrected totals: 18 keys, 67 cues. That is the block with finding 1's two entries added and the tigerToss / raijinKen1 entries
replaced by those in findings 2 and 3.
