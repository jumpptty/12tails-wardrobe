# Chameleon effects + sounds research: the three TTO Lv 100 skills (Venom Phantom, Apex Hunt, Chain Lightning)

Scope: the TTO-only clips `venomPhantom1` (0.4 s), `venomPhantom2` (0.233 s), `venomPhantom3` (1.2 s), `apexHunt` (3.1 s)
and `chainLightning` (0.9 s), all `tto: true`, group `skill` in `wardrobe/data/chameleon/clips.json`. No BB code plays them.
**All five are in the released list** (`wardrobe/tto_released.json`, chameleon clips: apexHunt, chainLightning, clap,
venomPhantom1-3, wai), so all three skills get cues. Research only: this file is the only file written in `plans/`, plus
the probes in `checks/fx_chameleon_research/tto/` (git-ignored). Home PC, 2026-11-13.

Sources:
- TTO's pseudo-C `D:\12tails\DecompiledSource_TTO_2026-11-02\pseudo\Chameleon.c` (and `CharacterControl.c`), cited as
  `TTO1102:Method@RVA` plus `Chameleon.c:<line>` (`:<line>` alone = Chameleon.c). The RVA is the stable cite.
- capstone over `client\GameAssembly.dll` for the floats Ghidra drops: `dis.py` (the Wolf's / Bat's) -> `vp_movenext.asm`
  (RPC_venomPhantom), `apex_movenext.asm`, `addstatus.asm` (`<addStatus>d__481`), `cl_*.asm` (ChameleonLightning),
  `ai_*.asm` (ChameleonAfterimage); `callers.py` (call sites of an RVA, il2cpp section); `strs.py` (string literals by
  address, through the Bible's `tools/usages.py`, run with `-B`: no .pyc written there).
- The Bible: `12t_reference/chameleon-skill-reference.md` "TTO Lv 100 skills" (:739-808; Venom Phantom :743-760, Apex
  Hunt :762-780, Chain Lightning :782-797) and the cards `chameleon_venomPhantom` etc. in `12t_projects/bible/index.html`
  (:17760).
- TTO's bundles of 2026-11-04 (`D:\12tails-video\tto_assets\2026-11-04`, the home PC's `wardrobe_fx_tto.py` ASSETS):
  `wardrobe_fx_tto.py chameleon --probe <the 31 TTO-only prefabs>` -> `probe.json`, summarised by `compact.py` ->
  `compact.txt`. `catalog.py` -> `catalog.txt` (TTO's chameleon effects / sounds vs BB's rip, the sound lengths), `cc.py`
  -> `cc.txt` (the Chameleon's CharacterController), `bones.py` (a bone's spot in the hero's space from rig.json +
  clips.json, the page's own hermite), `calc.py` -> `calc.txt` (the numbers below), `cues.py` -> `cues.json` /
  `cues_block.txt` (section 7, parsed and checked against probe.json and the rip's `sounds/`).

Times are seconds from the start of the clip the cue is keyed by. Every wait is `Chameleon::Until(t)`
(`TTO1102:Chameleon::Until@0x1BD95E0`, `:39866`), the absolute-time wait every TTO class uses, and every one here is
`Until(start + t)` (start = `Time.time` at the coroutine's first state), so a wait is a time from the start, not a step
to add. `Later(delay, act)` (`@0x1BD0AE0`, `:38899`) runs `act` `delay` s after it is started. All three skills have one
rank (`chm_venomPhantom5`, `chm_apexHunt5`, `chm_chainLightning5`, DoRow6Skill `:34788-34799`): max rank changes nothing.

## Read this first

1. **Venom Phantom is three clips in one sequence; the other two are one clip each. No cast bar** (all three start in
   `Chameleon::DoRow6Skill@0x1BCF640` at the key press).
   - Venom Phantom plays `venomPhantom1` at 0 (Row6Begin's `PlayAnimation(clip, 0.1)`), **`venomPhantom2` five times**,
     one per shot at 0.3 + 0.22 i (`PlayAnimation(venomPhantom2, 0.05)`, `PhantomShot` `:35954`), then `venomPhantom3`
     at 1.4 (`PlayAnimation(venomPhantom3, 0.1)`, `:12707`), free at 2.6 = 1.4 + 1.2, venomPhantom3's own length.
   - **The page's SEQ is wrong**: `"Venom Phantom: venomPhantom1 venomPhantom2 venomPhantom3"` (index.html:1190) plays
     each clip once, at its own length. It should be
     `"Venom Phantom: venomPhantom1@0.3 venomPhantom2^@0.22 venomPhantom2^@0.22 venomPhantom2^@0.22 venomPhantom2^@0.22 venomPhantom2^@0.22 venomPhantom3^"`
     (0.3 + 5 x 0.22 = 1.4; `^` = 0.1 s, APPROXIMATED: the game's shot crossfade is 0.05 s, the page has no token for
     it, question 1). Cue keys are the plain clip names (`venomPhantom1` / `2` / `3`: no other tile plays them), and
     the `venomPhantom2` entry fires on each of the five steps.
   - `apexHunt` 3.1 s = `Until(start + 3.1)` then Row6End (`:3387`, capstone 0x1BF9A75). `chainLightning` 0.9 s, but
     Row6End comes at **0.5** (`:7002-7013`); the page plays the clip to its 0.9 s end (its last frames are the idle
     pose again), and the later cues run in the idle tail.
2. **31 TTO-only prefabs, all on this PC, no arcana style** (`catalog.txt`: TTO's chameleon/effects has 102 names, 31
   not in BB's rip; no `heroes/chameleon/arcana/`). Every one is probed (section 5). Two of them,
   `venomPhantom_ghostFire` and `venomPhantom_ghostShatter`, are spawned only by the ghost's own script (its `fireFx`
   / `shatterFx`): `wardrobe_fx_tto.py` warns they are "written by name only", so they must be built by name
   (`SKILL_FX["chameleon"]` or the entry's `"builds"`).
3. **No voices, no rolls, no prefab sounds.** Every sound is `Row6Sound` = `PlayOneShot` of
   `GameAssets/characters/heroes/chameleon/sounds/<name>`, volume 1 for the owner (`Row6Sound@0x1BD76F0`, `:39402`).
   So every cue is kind **`"sound"`**. All 16 used are BB's own `chameleon/sounds/` recordings, the same length in TTO
   (`catalog.txt`); the only TTO-only sound, `stormHit`, belongs to the storm arrows (not cued, item 8). **No prefab has
   an AudioSource** (`probe.json` "sounds": []). No `Row6Voice`, no proc roll, no passive adds an effect.
4. **Name collisions** (the cue kind keeps them apart): the sounds `blend`, `massShot`, `poisonVolley`, `allSlain_hit`,
   `markOfSlayer_hit` are also BB Chameleon effects; `thunderDragon_ring2` is a BB effect (inventory: "needs
   ParticleSystem") and here only the sound. `preyFx` is both the lock reticle (`apexLockFx`, lockOnly) and the Prey
   status look (`preyFx`): one prefab, two names on the foe.
5. **Where things go (the standing rules).** The lone target stands 10 m ahead; its "chest" (`Row6Chest@0x1BD69E0`,
   `:39735` = the collider's bounds centre) is the standard target body, **0.6 m up** (Bat decisions 3-4); its ground
   (`Row6Ground@0x1BD72A0`: a raycast down from 2 m above) is y 0. The hero's own chest is her CharacterController
   centre, **0.98 m up** (`cc.txt`: m_Center y 0.98, height 1.8, radius 0.3).
6. **The hero stays in place** (Penguin decision 8, Bat decision 10). Apex Hunt lifts the Chameleon's transform 4.5 m
   by code (the clip itself has no lift: its Root moves 0.36 m at most); this report cues it on the ground, with the
   lift's numbers kept for question 3.
7. **followState** (EffectControl `followState`: ends when the owner's `actionState` or `myCommand` changes,
   `DecompiledSource/EffectControl.cs:122-145`, `:206-240`; destroyed at life + afterLife, `:179-183`):
   - `venomPhantom_coil`: myCommand becomes `venomPhantomShot` at the first shot (`PhantomShot` `:35920`): **cut 0.3**.
     The page reads `cut` against the step's own clock (`FX.t`, index.html Fx.update), which restarts at 0 when
     `venomPhantom2` begins at 0.3, so this cut is never reached (part P8; the coil's own life ends 0.1 s later anyway).
   - `chainLightning_draw`: Row6End at 0.5: **cut 0.5**.
   - `apexHunt_hang`: myCommand stays `apexHunt` until 3.1; no cut. It is **respawned** whenever none lives during the
     hover (life 0.6 + 0.3 = 0.9 s): 0.55, 1.45, 2.35; the code destroys the third at 2.75 (`kill 0.4`).
8. **Chain Lightning's arrows are not in the tile.** The fork / chain bolts (`StormArrow@0x1BD8290`,
   `StormArrowHit@0x1BD8120`, `StaticChain@0x1C5B310`, `HopFx@0x1BD0370`: chainLightning_arrow / _zap / _bolt /
   _boltHot, sound `stormHit`) come with every Combo, Clear Arrow and Left Stride arrow while `stormCharge` lasts.
   The Chain Lightning cast shoots none, and the other tiles play without the buff: not cued (question 7).
9. **Status looks** (`<addStatus>d__481::MoveNext` dispatch, `addstatus.asm` 0x24EE99C-0x24EE9FE, `strs.py`):
   `phantomVenom`, `stormCharge`, `staticDrain` -> `AddChameleonRow6Fx(status, false)`, `prey` ->
   `AddChameleonRow6Fx("prey", true)` (`CharacterControl.c:5927`): `<status>Fx` parented to the character at its
   collider centre, scale `clamp(2 x radius x lossy, 1, 4) / lossy` (`SpawnChameleonRow6Fx@0x24C50F0`), removed with
   the status (`RemoveChameleonRow6Fx@0x24C2190`). On the Chameleon herself (stormCharge 8 s, staticDrain 4 s) they are
   cued (a buff on the hero stays, recipe step 4); on the foe (phantomVenom, prey, BB's poison) they are left out
   (Sheep decision 4).
10. **Camera shakes** (`Row6Shake`: 0.25 Requiem, 0.2 + 0.04 n volley, 0.4 impact, 0.35 overload, 0.6 storm form) stay
    out (Bison decision 35).
11. **Missing parts** (section 6): P1-P9. The TTO scripts `ChameleonLightning`, `ChameleonAfterimage` (+ the
    `TTO/ChameleonSpirit` shader) and `ChameleonPreyReticle`; a code mover for the Apex arrow; the storm's hero
    darkening (a `skin`); a `stop` cue option; the followState cut across a step change. Per the rule every effect is
    cued anyway, with its part named.

---

## 1. Shared machinery (`TTO1102:Chameleon`)

- **`Row6Begin(command, mPos, tDir, clip)@0x1BD6450`** (`:39498`): actionState `attack`, actionTime now, myCommand =
  command; the hero at mPos, `LookAt(mPos + vFlat(tDir))`; `PlayAnimation(clip ?? command, 0.1)`, wrapMode Once,
  moveSpeed 0.
- **`Row6End(command)@0x1BD7100`** (`:39607`): `standby`, myCommand `none`, only while still doing that command.
- **`Row6Spawn(name, pos, rot, owned)@0x1BD77C0`** (`:39344`): `Row6Prefab` loads
  `GameAssets/characters/heroes/chameleon/effects/<name>` (cached, `Cannot find <name> effect`); owned ->
  `CharacterControl.createEffect`, else `Object.Instantiate`. Owned: `venomPhantom_coil`, `apexHunt_hang`,
  `chainLightning_draw` (and the kill's `apexHunt_trophy`).
- **`Row6Sound(name)@0x1BD76F0`** (`:39402`): `sounds/<name>`, PlayOneShot, volume 1 owner / 0.75 others.
- **`Row6Chest(cc)`** = `Collider.bounds.center` (no collider: position + up); **`Row6Ground(p)`** = the ground under p
  (raycast from p + 2 up, 8 m down); **`Row6Bone(name)`** = `Math.findChildObject`.
- Statics (`Chameleon..cctor@0x1BD9650`, `:39953`; `dump.cs:105273-105284`): `GhostSlots` = (1.5, 0, -0.3),
  (-1.5, 0, -0.3), (2.8, 0, -1.1), (-2.8, 0, -1.1), (0, 0, 1.6) (hero-local, x right, z forward); `StormBlack` =
  (0.07, 0.07, 0.09, 1).
- **Bone spots on the page** (`bones.py`; rig.json is the page's right-handed space, its +x = her left, so cue x =
  -rig x): mount_Hand_L at venomPhantom2 0.06 s = (x -0.585, y 1.109, d 0.39); at apexHunt 2.35 s = (-0.229, 0.95,
  0.745).

## 2. Per skill

### 2.1 Venom Phantom (`venomPhantom1` -> `venomPhantom2` x 5 -> `venomPhantom3`; cell 452)

Cast (`DoRow6Skill`, `:34960-35040`; Bible :747): needs an enemy within 16 + 2 x Far Reach, cooldown agiAdjust(75), then
the coroutine and `RPC_venomPhantom` to the others.

Coroutine `TTO1102:Chameleon.<RPC_venomPhantom>d__294::MoveNext@0x1C581A0` (`:21679-22040`):
- **0.00** (state 0): `Row6Begin("venomPhantom", clip "venomPhantom1")` (`:21737`); mPhantomStep += 1; `ClearGhosts(false)`
  (`:21741`); `venomPhantom_coil` **owned** at the hero, hero rotation (`:21754`); `Row6Sound("blend")` (`:21755`);
  `Until(start + 0.3)` (`:21759`, capstone 0x1C58C3F `addss xmm6, [0x30043A4] = 0.3`).
- **0.30** (state 1): `PhantomPack(target)` (`:21804`): the target plus up to 3 foes within 8 m, by poison level then
  distance (Bible :748); i = 0; `Until(start + 0.3 + 0.22 i)` (`:22018`, capstone 0x1C589DC-0x1C589ED).
- **Shots** (state 2) at **0.30, 0.52, 0.74, 0.96, 1.18**: foe = pack[i mod n] (the 5th always the selected target while
  it lives); the facing turned to it; `PhantomShot(face, foeId)` (`:21975`), `RPC_phantomShot` to the others,
  `Later(0.06, ShotHit)` (`:21998`).
- **1.40** (state 3, after the 5th: `Until(start + 0.3 + 1.1)`, `:22032`, capstone 0x1C58A6B-0x1C58A75):
  `PhantomFinale(step, hero position, flat direction to the target)` (`:21888`) -> `RPC_phantomRequiem` here and on the
  others.

**`PhantomShot(face, foeId)@0x1BD21D0`** (`:35882-35979`), each shot:
- myCommand `venomPhantomShot`, actionState `attack`, actionTime now (`:35920`); the hero turned to `face`;
  `PlayAnimation("venomPhantom2", 0.05)`, wrapMode Once (`:35954`); `Row6Sound("rightStride_fire1")` (`:35957`).
- `Later(0.55)` -> `<PhantomShot>b__0@0x1BF57E0` (`:125`): Row6End if still `venomPhantomShot` 0.44 s after the last
  shot. The finale's Row6Begin at 1.4 changes the command first, so it never fires in a full cast.
- `Later(0.06)` -> **`<PhantomShot>b__1@0x1BF5870`** (`:160-484`), so the look comes **0.06 s after each shot**:
  - from = `mount_Hand_L` (`:213`; with none: chest + 0.4 forward); to = `Row6Chest(foe)` (`:263`; dead foe: from + 8
    forward);
  - `venomPhantom_shot` at from, `LookRotation(to - from)` (`:288`), its `RabbitTracer.Set(from, to)` (`:309`);
  - `venomPhantom_hit` at to, identity (`:324`); `Row6Sound("bow_hit2")` (`:326`);
  - `venomPhantom_ghost` at the hero, hero rotation (`:341`), `ChameleonAfterimage.Bake(hero, from)` (`:364`): a frozen
    copy of every visible renderer of the hero (skinned meshes baked in their current pose), drawn with its `spirit`
    material; then `SlideTo(Row6Ground(hero.TransformPoint(GhostSlots[ghosts % 5])), LookRotation(vFlat(to - spot)),
    0.18)` (`:385-423`), added to mGhosts / mGhostFoes.
- `ShotHit` (`@0x1BD7C60`) at +0.06 deals the hit and `AddPoison`: no prefab.

**`<RPC_phantomRequiem>d__301::MoveNext@0x1C1B140`** (`:12606-12957`), times from 1.4 (venomPhantom3's 0):
- **0.00**: `Row6Begin("venomPhantom", spot, face, clip "venomPhantom3")` (`:12707`); `Until(start + 0.55)` (`:12713`).
- **0.55** (1.95 from the cast; interrupted -> `ClearGhosts(true)` and stop, `:12725`):
  - `venomPhantom_requiem` at the hero, hero rotation, not owned (`:12741`); `Row6Sound("venomShock_ring")`
    (`:12743`); Row6Shake 0.25;
  - per ghost k (shot order): from = its `BowPoint` (`:12774`) = its transform x the bow's spot baked at the shot; to =
    its foe's chest (dead: 4 m along the ghost's forward); `ChameleonAfterimage.Fire()` (`:12802`: its `fireFx`
    `venomPhantom_ghostFire` at the bow point, `ai_fire.asm`); `venomPhantom_beam` at from, `LookRotation(to - from)`,
    `RabbitTracer.Set(from, to)` (`:12824-12846`); the foe added to `struck` once;
  - `Row6Sound("poisonVolley")` (`:12753`); `Until(start + 0.55 + 0.12)` (`:12758`).
- **0.67** (2.07): per struck foe still alive: `venomPhantom_rupture` at its chest, identity (`:12910`), `Rupture` (owner,
  `:12917`; hit, burst, `phantomVenom` 8 s: no prefab of its own); `Row6Sound("venomShock")` if any struck (`:12925`);
  `ClearGhosts(true)` (`:12927`): each ghost's `Shatter()` (its `shatterFx` `venomPhantom_ghostShatter` 0.9 x its height
  up, then gone after `shatterTime` 0.35, `ai_shatter.asm`); `Until(start + 1.2)` (`:12932`).
- **1.20** (2.6): `Row6End("venomPhantom")` (`:12947`). venomPhantom3 is 1.2 s ✓. Sums: Bible :749 (shots 0.30 ... 1.18,
  finale 1.40, beams 1.95, Rupture 2.07, end 2.60) ✓.

**The tile (the lone target 10 m ahead, the standing rule).** All five shots go to it; its ghosts still fan out over the
five slots (the slot is the ghost count, not the foe). From `calc.txt`:

| shot | look at | ghost slot (x, d) | turn | bow point at the finale (x, y, d) | beam rot |
|---|---|---|---|---|---|
| 0 | 0.36 | 1.5, -0.3 | -8.29 | 0.865, 1.109, 0.002 | [2.91, -4.95, 0] |
| 1 | 0.58 | -1.5, -0.3 | 8.29 | -2.022, 1.109, 0.17 | [2.91, 11.63, 0] |
| 2 | 0.80 | 2.8, -1.1 | -14.16 | 2.138, 1.109, -0.865 | [2.63, -11.13, 0] |
| 3 | 1.02 | -2.8, -1.1 | 14.16 | -3.272, 1.109, -0.579 | [2.63, 17.18, 0] |
| 4 | 1.24 | 0, 1.6 | 0 | -0.585, 1.109, 1.99 | [3.63, 4.18, 0] |

- The shot: from (-0.585, 1.109, 0.39) to (0, 0.6, 10), 9.64 m, `rot [3.03, 3.48, 0]`.
- With 2-4 foes (question 2) the shots split 3 + 2 / 3 + 1 + 1 / 2 + 1 + 1 + 1, each ghost facing its own foe, a beam and
  a Rupture per foe.

### 2.2 Apex Hunt (`apexHunt`, 3.1 s; cell 453)

Cast (`DoRow6Skill`, `:34900-34955`; Bible :767): an enemy within 24 + 4 x Far Reach, cooldown agiAdjust(120), the
coroutine and `RPC_apexHunt`.

Coroutine `TTO1102:Chameleon.<RPC_apexHunt>d__304::MoveNext@0x1BF8FB0` (`:3204-3645`; floats from `apex_movenext.asm`):
- **0.00**: `Row6Begin("apexHunt", clip "apexHunt")` (`:3265`); step += 1; `ClearApexLocks` (`:3269`); ground = mPos,
  top = ground + 4.5 up (`:3287-3290`); reach = 24 + 4 x Far Reach; `apexHunt_crouch` at ground, hero rotation
  (`:3303`); `Row6Sound("slayerCharge")` (`:3304`); `Until(start + 0.22)` (`:3308`, capstone 0x1BF9C6E).
- **0.22**: `apexHunt_takeoff` at ground, hero rotation (`:3330`); `Row6Sound("massShot")` (`:3331`); nextLock = start +
  0.55; then every frame (state 2) until 2.75:
  - lift, t < 0.55: u = clamp01((t - 0.22) / 0.33), y = 4.5 (1 - (1 - u)^2) (`:3425`);
  - hover, 0.55 <= t < 2.45: top + 0.08 sin(5 (t - 0.55)) up (`:3489`; FUN_180308BD0 = sinf, as Penguin.c:1083), and
    `apexHunt_hang` **owned** at the hero whenever none lives (`:3517`) -> **0.55, 1.45, 2.35**;
  - fall, t >= 2.45: y = 4.5 (1 - ((t - 2.45) / 0.3)^2);
  - locks while t < 2.25, one try at nextLock, then nextLock += 0.3 (**0.55**, 0.85, 1.15, 1.45, 1.75, 2.05;
    `:3525-3545`): the first = the target, later ones `NextLock` (the nearest unlocked living foe to the ground spot);
  - turned toward `ApexFacing` (the selected target while it lives);
  - once at t >= 2.35 (`:3618`): `ApexVolley(ground, tID)` (`:3622`).
- **2.75** (`:3344`): Destroy(hang) (`:3355`); the hero back on the ground; `apexHunt_land` at ground, hero rotation
  (`:3381`); `Until(start + 3.1)` (`:3387`).
- **3.10**: `Row6End("apexHunt")` (`:3633`). The clip is 3.1 s ✓. Bible :768-771 (take-off 0.22, 4.5 m by 0.55, fall
  from 2.45, down 2.75; locks 0.55 + 0.3 k; volley 2.35, hits 2.47 + 0.04 i) ✓.

**`ApexLock(id)@0x1BCE270`** (`:36531-36665`): at most 6, living, not dead: `CharacterControl::AddApexLockFx@0x24AB5A0`
(`CharacterControl.c:6140`) = `preyFx` named `apexLockFx` on the foe, `lockOnly = true`, at its collider centre, scale 1
for the 0.3 m body; `Row6Sound("markOfSlayer_hit")` per lock (`:36628`).

**`ApexVolley(ground, tID)@0x1BCE570`** (`:36853-37188`): from = `mount_Hand_L` (`:36928`; none: hero + 1.2 up); the living
locks; `apexHunt_loose` at from, `LookRotation(first lock's chest - from)` (`:37119`; no lock: 10 m ahead on the ground,
`:37066`); `Row6Sound("slayerFire")` (`:37121`); one `ApexArrow(from, body, chest, primary, 0.04 i)` per lock
(`:37157`); `ClearApexLocks` (`:37147`) = every reticle's `Release()` (fadeOut 0.25).

**`<ApexArrow>d__312::MoveNext@0x1BEC9D0`** (`:485-715`): after its delay, `apexHunt_arrow` at from, `LookRotation(to -
from)` (`:565`); each frame lerped from -> the foe's chest (read live) over **0.12 s**, turned along it (`:584-591`); then
`Destroy(arrow, 0.3)` (`:660`); owner: `ImpactFx(Row6Ground(chest))` (`:675-680`, `@0x1BD05B0`: `apexHunt_impact`,
identity + `Row6Sound("allSlain_hit")`), `ApexHit` (`:701`; hits, Prey 12 s, TTO1106's TrophyWatch: no prefab).

**Kill reward** (TTO1106, Bible :766, :772): `TrophyFx@0x1BD9270` (`:37774`): `apexHunt_trophy` owned + `Row6Sound("allSlain_ring")`.
Only on a kill (question 5): left out.

**The tile (in place, the lone target).** crouch 0, takeoff 0.22, the lock reticle at the target body 0.55 (released at
2.35 = 1.8 s later, gone 2.6), hang 0.55 / 1.45 / 2.35, loose + arrow from the hand (-0.229, 0.95, 0.745) at 2.35,
`rot [2.17, 1.42, 0]`, the arrow at the chest (0, 0.6, 10) at 2.47, the impact on the ground 10 m ahead at 2.47, land 2.75.
- Lift variant (question 3): the hero's y = 3.375 at 0.385, 4.5 at 0.55, 4.422 at 1.45, 4.533 at 2.35, back to 0 at
  2.75 (`calc.txt`); the loose / arrow from (-0.229, 5.483, 0.745), `rot [27.81, 1.42, 0]`.

### 2.3 Chain Lightning (`chainLightning`, 0.9 s, free at 0.5; cell 454)

Cast (`DoRow6Skill`, `:34817-34890`): refused while staticDrain (`0x269`) or stormCharge; cooldown agiAdjust(45)
(`:34826`); the coroutine (`:34849`) and `RPC_chainLightning`; mStormShots = 0; `RPC_AddStatus(stormCharge 0x268, 1, 8)`
on the Chameleon (`:34875`); `StormWatch` (`:34882`).

Coroutine `TTO1102:Chameleon.<RPC_chainLightning>d__317::MoveNext@0x1BFF820` (`:6895-7022`):
- **0.00**: `Row6Begin("chainLightning")` (`:6935`); `chainLightning_draw` **owned** at the hero, hero rotation
  (`:6954`); `Row6Sound("cAttack_bow")` (`:6955`); `Until(start + 0.3)` (`:6960`).
  - The status: `stormChargeFx` on her (section "Read this first" 9), at her collider centre (0.98 up), scale 1,
    removed at 8 s.
- **0.30**: `OverloadFx(Row6Ground(hero))` (`:6980-6983`; `@0x1BD18B0`, `:38755`): `chainLightning_overload`, identity +
  `Row6Sound("thunderDragon_ring2")`; `chainLightning_zapHot` at `Row6Chest(hero)`, identity (`:6997`);
  `StormDragonForm()` (`:7000`); `Until(start + 0.5)` (`:7002`).
- **0.50**: `Row6End("chainLightning")` (`:7013`). Bible :786 ("stands 0.5 s") ✓.

**`<StormDragonForm>d__328::MoveNext@0x1C5B820`** (`:23687-24081`), from 0.3:
- end = now + 8 (`:23767`), grace 1 s; every renderer of hers except ParticleSystem- / Line- / TrailRenderers, with its
  `_Color` (or `_BaseColor`) remembered;
- `chainLightning_stormDragon` **parented** to her, at her position and rotation (`:23896`); `chainLightning_muzzle` at
  her chest, identity (`:23917`);
- each frame while now < end, the cast current, alive, and (now < grace or stormCharge on):
  `StormDarken(k = clamp01(4 (now - 0.3)))` (`:23959`; `@0x1BD8C90`, `:38224`): every remembered colour -> lerp(colour,
  StormBlack, k), alpha kept, through a MaterialPropertyBlock: **near-black by 0.55 s**;
- the loop ends when stormCharge goes (8.0): `chainLightning_zapHot` at her chest (`:23990`); the aura's particle
  systems `Stop(true, StopEmitting)` (`:24010`), `Destroy(aura, 1)` (`:24017`); the darkening undone over 0.6 s
  (k = 1 - (now - fadeFrom) / 0.6), then the original blocks back.

**`<StormWatch>d__333::MoveNext@0x1C5C3C0`** (`:24098-24185`): `Until(now + 0.2)` (`:24173`), then while stormCharge is
on `Until(now + 0.1)` (`:24136`); the first check that finds it gone (expiry at 8.0; the check 8.0-8.1, the 0.1 s steps
drift by frames: cued **8.05**): `RPC_AddStatus(staticDrain 0x269, 1, 4)` (`:24156`; `staticDrainFx` on her chest, 4 s)
and `Row6Sound("rightStride_fire2")` (`:24159`). Bible :793 ✓.

The tile's cues after 0.9 s run on in the idle tail, to 12.05 s (question 6); with the วนซ้ำ toggle on, the clip
restarts at 0.9 s and the 8 s storm restarts with it.

## 3. What is left out (only "on an enemy" / "needs a kill" / camera)

- Status looks on foes (Sheep decision 4): the poison look (every shot's `AddPoison`), `phantomVenomFx` (the
  Rupture's phantomVenom, 8 s), the Prey look (`preyFx` as the `prey` status, 12 s, every Apex arrow target).
- The hits draw nothing of their own (`ShotHit@0x1BD7C60`, `Rupture@0x1BD78F0`, `ApexHit@0x1BCD7F0`: hits and statuses
  only).
- Apex Hunt's kill reward (`apexHunt_trophy`, `allSlain_ring`): needs a kill (question 5).
- The storm arrows' fork / chain looks (item 8, question 7). Venom Shock's spread line `venomPhantom_echo`
  (`EchoFx@0x1BCFE00`, from `PhantomEcho` inside TTO's `RPC_venomShock`): a BB skill's TTO add-on, only on foes that
  carry phantomVenom; not in these clips.
- Camera shakes (Bison decision 35).
- **Cued, on the foe**: the skill's own spawns at the target point (the shot's hit, the beams' ends, the Rupture, the
  arrow and its impact) and the lock reticle (`apexLockFx`: the skill's marker, not a status; as the Penguin's
  constellation marks and the Bat's servant ring; question 4).

## 4. Sounds and voices

All `"sound"` (`chameleon/sounds/`, BB's rip, `catalog.txt` lengths; TTO's copies are the same length):
blend 0.577, rightStride_fire1 0.221, bow_hit2 0.282, venomShock_ring 0.996, poisonVolley 0.939, venomShock 1.188,
slayerCharge 1.12, massShot 0.928, markOfSlayer_hit 1.12, slayerFire 0.951, allSlain_hit 2.538, cAttack_bow 0.282,
thunderDragon_ring2 0.498, rightStride_fire2 0.229 (and allSlain_ring 3.19, stormHit 0.48 TTO-only: not cued).
`wardrobe_fx.py chameleon` builds them from the rip (no P8-style TTO sound needed). No voices.

## 5. Probed 2026-11-13 (home PC, TTO's 2026-11-04 bundles)

`uv run --no-project --with UnityPy --with pillow --with imageio-ffmpeg python -I pipeline/wardrobe_fx_tto.py chameleon --probe <31 names>`
-> `checks/fx_chameleon_research/tto/probe.json`; `compact.txt` summarises it. EffectControl = life + afterLife.

| Prefab | EffectControl | Parts (node: type) | cued |
|---|---|---|---|
| venomPhantom_coil | 0.4 + 0.3, followPosition + followState | GroundHug (ring), PS pull | yes |
| venomPhantom_shot | none | **LineRenderer + RabbitTracer** (venom line), ImageEmitter muzzle | yes |
| venomPhantom_hit | 0.2 + 0.5 | ImageEmitter splash, PS drops | yes |
| venomPhantom_ghost | none | **ChameleonAfterimage** (spirit `tto_chmRow6_phantomSpirit` = **TTO/ChameleonSpirit**; fadeIn 0.12, shatterTime 0.35, life 4, rim, flare; fireFx / shatterFx by name), PS wisps (loop) | yes |
| venomPhantom_ghostFire | 0.15 + 0.35 | ImageEmitter flash | by the ghost |
| venomPhantom_ghostShatter | 0.2 + 0.9 | PS motes, PS smoke | by the ghost |
| venomPhantom_requiem | 0.9 + 0.6 | 2 GroundHugs (venomSigil, ring), ImageEmitter flash | yes |
| venomPhantom_beam | none | **LineRenderer + RabbitTracer**, head: PS glow | yes |
| venomPhantom_rupture | 0.3 + 1.0 | ImageEmitter splash, PS drops, PS smoke | yes |
| venomPhantom_echo | none | **LineRenderer + ChameleonLightning** (bolt) | no (Venom Shock) |
| phantomVenomFx | none | PS wisps, GroundHug (feet) | no (foe status) |
| apexHunt_crouch | 0.2 + 0.5 | GroundHug ring | yes |
| apexHunt_takeoff | 0.3 + 0.8 | GroundHug wave, PS dust, PS streaks (cone) | yes |
| apexHunt_hang | 0.6 + 0.3, followPosition + followState | ImageEmitter halo (1 m up), PS glitter | yes |
| apexHunt_loose | 0.2 + 0.6 | 2 ImageEmitters, PS sparks | yes |
| apexHunt_arrow | none (code) | StaticMesh `Arrow` (37 v) with goldSpirit = **TTO/ChameleonSpirit**, 2 line quads (StaticMesh), TrailRendererModern, PS head | yes |
| apexHunt_impact | 0.5 + 1.3 | 2 ImageEmitters (flash 0.9 up, pillar 3.5 up), 2 GroundHugs (wave, cracks), PS rocks (`tto_Stone`, Particles/Standard Unlit) | yes |
| apexHunt_land | 0.2 + 0.6 | GroundHug ring, PS dust | yes |
| apexHunt_trophy | 1.0 + 0.6, followPosition + followState | PS rise, 2 ImageEmitters | no (kill) |
| preyFx | none | **ChameleonPreyReticle** (lockIn 0.35, fadeOut 0.25, spin 40, gold / dim / race colours), ring + crosshair = built-in Quad (StaticMesh) | yes (the lock) |
| chainLightning_draw | 0.36 + 0.3, followPosition + followState | PS pull, **ChameleonLightning** (aura) | yes |
| chainLightning_overload | 0.5 + 1.1 | **9 ChameleonLightning** (2 autoBolts 6 m down, 7 ground arcs 4 m out), GroundHug cracks, 2 ImageEmitters, PS sparks | yes |
| chainLightning_zapHot | 0.25 + 0.5 | 2 ImageEmitters, **ChameleonLightning** (cling aura), PS sparks | yes |
| chainLightning_muzzle | 0.2 + 0.5 | 2 ImageEmitters, PS sparks | yes |
| chainLightning_stormDragon | none | PS Aura (box, 64/s, loop, `tto_thunderDragon_particle`) at (-0.1, 1.05, -0.2) | yes |
| stormChargeFx | none | **2 ChameleonLightning** (aura), PS sparks (loop), GroundHug (feet) | yes |
| staticDrainFx | none | PS dying, **ChameleonLightning** (flicker), PS smoke | yes |
| chainLightning_arrow / _zap / _bolt / _boltHot | none / 0.15 + 0.4 / none / none | arrow quads + trail + ChameleonLightning crackle / ImageEmitter + PS / ChameleonLightning bolts | no (storm arrows) |

- Shuriken modules: Initial, Shape (sphere 0, hemisphere 2, cone 4, box 5, circle 10), Emission, Color only: all in
  shuriken.js. No mesh particles, no TrailModule, no followState except the five named.
- Materials (18): add / addsoft / alpha on 11 `tto_chmRow6_*` textures + `tto_thunderDragon_particle`; `tto_Stone`
  (Particles/Standard Unlit, colour x 4.75); **two `shader:TTO/ChameleonSpirit`** (`tto_chmRow6_phantomSpirit`,
  `tto_chmRow6_goldSpirit`; props _Fade, _InnerGlow, _MaxGlow, _RimEdge, _RimPower, _ScaleSize / Speed, _Wisp, _WispScale
  / Speed, _CoreColor, _RimColor, _ScaleColor).
- `ChameleonLightning` values (per node): `probe.json` (aura, segments, jag, maxJag, flicker, life, radius, height,
  gap, autoBolt, localFrom / localTo, delay).

## 6. Parts the page lacks (effect: part)

| # | Part | Effects | What it does (source) |
|---|---|---|---|
| P1 | **ChameleonLightning** (TTO script, `dump.cs` `class ChameleonLightning`, token 0x2000d96) on a LineRenderer | chainLightning_draw, _overload, _zapHot, stormChargeFx, staticDrainFx (+ the uncued arrow / bolt / boltHot / echo) | A jagged lightning line of `segments` points. Aura mode: a new random arc on a cylinder (radius, height) around the node every `gap` s (`NewArc@0x1C4E250`: its constants 6.283, 2.2, 0.8, 0.5, 0.05 read as a random angle and a 0.8-2.2 span: UNVERIFIED), re-jagged every `flicker` s (`Jag@0x1C4DD90`: offsets up to jag / maxJag, a sin(pi u) envelope), faded over `life` (`Fade@0x1C4DCE0`); bolt mode: `Set(from, to)@0x1C4E3C0` in world space, `autoBolt` from localFrom / localTo at Start (`@0x1C4E550`); `Update@0x1C4E690`. The parts stage reads these methods (`cl_*.asm`). |
| P2 | **ChameleonAfterimage** (on HeroClone's copy, a frozen pose) + P3 | venomPhantom_ghost (spawns venomPhantom_ghostFire / _ghostShatter with `api.spawn`) | `Bake@0x1C4C190`: every visible renderer of the hero (Skip@0x1C4CFA0), skinned ones baked in the pose of that frame, drawn with `spirit`; bowLocal = the bow's spot in its frame; `SlideTo(pos, rot, 0.18)@0x1C4D2E0`; `Update@0x1C4D3C0` (fade in 0.12, the slide with Slerp, life 4 -> shatter; its other constants 7, 0.15, 0.85, 0.08, 0.3, 0.9 (`ai_update.asm`) look like a glow pulse 0.85 + 0.15 sin(7 t) and the 0.08 s flare after Fire: UNVERIFIED, the parts stage reads them); `Fire@0x1C4CA80` (fireFx at the bow point, the flare); `Shatter@0x1C4CD90` (shatterFx 0.9 x height up, shrink, gone after 0.35); `Apply@0x1C4BEF0` sets _Fade / the rim colour per renderer. Cue options: `bow`, `face`, `slide`, `slots` (the slot = live ghosts of this play % 5); `ghost: k` on a beam cue = ghost k's Fire(); `shatterGhosts` on the rupture cue = ClearGhosts(true). |
| P3 | **TTO/ChameleonSpirit** shader | venomPhantom_ghost (phantomSpirit), apexHunt_arrow's ghost mesh (goldSpirit) | A rim-lit, wispy ghost shader with a scale pattern (its props, section 5); compiled in the bundle: read it as the Bison's / Sheep's TTO shaders were. |
| P4 | **ChameleonPreyReticle** | preyFx (the lock) | Ring (Quad x 2.4, flat) and crosshair (Quad x 0.7, 1.6 up) on the foe's body, locking in over 0.35 s, spinning 40 deg/s, gold for lockOnly (`Start@0x1C4EA70`, `Update@0x1C4EF10`, `Paint@0x1C4E920`); `Release@0x1C4EA60` fades out over 0.25 s. Cue options `lockOnly`, `release` (s after the spawn); the target body: feet 0, centre 0.6. |
| P5 | `Chameleon.ApexArrow` code mover (CODE_MOVERS) | apexHunt_arrow | From the spawn to `to` in 0.12 s, a straight lerp, turned along it (`<ApexArrow>d__312@0x1BEC9D0`, `:565-591`); `kill 0.42` = Destroy(arrow, 0.3) after the arrival. |
| P6 | Hero skin `Chameleon.StormDarken` (HERO_SKINS) | the storm (chainLightning) | Every hero renderer's colour lerped to StormBlack (0.07, 0.07, 0.09) by k = clamp01(4 t) from the cue, held, and back over 0.6 s ending at `kill` (`:23959`, `:24020-24060`, StormDarken@0x1BD8C90). Props too (the game darkens every renderer under her). |
| P7 | Cue option `stop` (seconds after the spawn: every Shuriken system stops emitting, live particles finish) | chainLightning_stormDragon (`stop 7.7`, then `kill 8.7`) | `ParticleSystem.Stop(true, StopEmitting)` + `Destroy(aura, 1)` (`:24010-24017`). Without it, `kill 7.7` is the approximation. |
| P8 | page: a followState `cut` at or after the step's end applies at the step change | venomPhantom_coil (`cut 0.3` at venomPhantom1's end) | Fx.update compares `cutAt` with `FX.t`, which fxStart resets at the next step. |
| P9 | (optional, question 1) a 0.05 s crossfade token in SEQ | venomPhantom2 | `PlayAnimation(venomPhantom2, 0.05)` (`:35954`). |
| (P10) | (optional, question 3) a hero lift | apexHunt | The Chameleon's own 4.5 m lift, hover and fall (`:3425-3489`). |

Parts that already exist and are used here: EffectControl, ImageEmitter, GroundHugEmitter (groundhug.js), Shuriken,
LineRenderer + RabbitTracer + TrailRendererModern (tto_sheep.js; RabbitTracer reads `to`), StaticMesh (mesh.js; the
built-in Quad via BUILTIN_MESH), `Particles/Standard Unlit` (tto_sheep.js).

Build notes: add `SKILL_FX["chameleon"]` to `wardrobe_fx_tto.py` (the 31 names, so ghostFire / ghostShatter and the
uncued ones are built too) and `"Chameleon.ApexArrow"` to CODE_MOVERS for `apexHunt_arrow`; then
`wardrobe_fx_tto.py chameleon` and `wardrobe_fx.py chameleon` (the sounds).

## 7. The cue entries (ready to paste into `wardrobe/fx_cues/chameleon.json`)

Checked by `cues.py` (valid JSON, every `tto/` name in probe.json, every sound in the rip's `chameleon/sounds/`). The
options `bow`, `face`, `slide`, `slots`, `ghost`, `shatterGhosts`, `lockOnly`, `release`, `stop` are new: today's
`cueOf` passes them on to the parts (index.html:4410-4413), harmless until P2 / P4 / P7 exist. The `skin`
`Chameleon.StormDarken` reports missing (`FX.missing`) until P6. With the SEQ fix of "Read this first" 1.

```json
  "venomPhantom1": {
    "why": "TTO1102:Chameleon.<RPC_venomPhantom>d__294::MoveNext@0x1C581A0 (pseudo/Chameleon.c:21679-22040; plans/fx_chameleon/tto.md 2.1; the lone target 10 m ahead): 0: Row6Begin(venomPhantom, clip venomPhantom1) = PlayAnimation(venomPhantom1, 0.1) facing it (:21737; Row6Begin@0x1BD6450 :39498-39580), ClearGhosts (:21741), venomPhantom_coil owned at the hero, hero rotation (:21754; EffectControl 0.4 + 0.3, followPosition + followState: myCommand becomes venomPhantomShot at the first shot, PhantomShot@0x1BD21D0 :35920, so cut 0.3), Row6Sound blend (sounds/, Row6Sound@0x1BD76F0 :39402-39440; :21755); Until(start + 0.3) (:21759, capstone 0x1C58C3F), then the shots (venomPhantom2); no voice, no roll",
    "cues": [
    [0, "fx", "tto/venomPhantom_coil", {"cut": 0.3}],
    [0, "sound", "blend"]
    ]
  },
  "venomPhantom2": {
    "why": "one shot, played five times at 0.3 + 0.22 i (Until :22018; the SEQ steps): PhantomShot@0x1BD21D0 (:35882-35979): myCommand venomPhantomShot, the hero turned to the foe, PlayAnimation(venomPhantom2, 0.05) (:35954), Row6Sound rightStride_fire1 (:35957); Later(0.06) (:35965) = <PhantomShot>b__1@0x1BF5870 (:160-484): from = mount_Hand_L (:213; venomPhantom2 at 0.06 s: 0.585 m left, 1.109 up, 0.39 ahead, checks/fx_chameleon_research/tto/bones.py), to = Row6Chest(foe) = its collider centre, the target body 0.6 m up 10 m ahead (:263; Row6Chest@0x1BD69E0 :39735; Bat decisions 3-4), venomPhantom_shot at from, LookRotation(to - from) (:288) + RabbitTracer.Set(from, to) (:309), venomPhantom_hit at to, identity (:324), Row6Sound bow_hit2 (:326), venomPhantom_ghost at the hero, hero rotation (:341), ChameleonAfterimage.Bake(hero, from) (:364), SlideTo(Row6Ground(hero.TransformPoint(GhostSlots[ghosts % 5])), LookRotation(vFlat(to - spot)), 0.18) (:385-423; GhostSlots from the .cctor@0x1BD9650 :39953: (1.5, 0, -0.3), (-1.5, 0, -0.3), (2.8, 0, -1.1), (-2.8, 0, -1.1), (0, 0, 1.6), hero-local x right / z forward); ShotHit at +0.06 (:21998) draws nothing; left out: the poison look on the foe (a status look on its body, Sheep decision 4)",
    "cues": [
    [0, "sound", "rightStride_fire1"],
    [0.06, "fx", "tto/venomPhantom_shot", {"x": -0.585, "y": 1.109, "d": 0.39, "rot": [3.03, 3.48, 0], "to": [0, 0.6, 10]}],
    [0.06, "fx", "tto/venomPhantom_hit", {"y": 0.6, "d": 10}],
    [0.06, "sound", "bow_hit2"],
    [0.06, "fx", "tto/venomPhantom_ghost", {"bow": [-0.585, 1.109, 0.39], "face": [0, 0.6, 10], "slide": 0.18, "slots": [[1.5, 0, -0.3], [-1.5, 0, -0.3], [2.8, 0, -1.1], [-2.8, 0, -1.1], [0, 0, 1.6]]}]
    ]
  },
  "venomPhantom3": {
    "why": "the finale: at 0.3 + 1.1 = 1.4 (Until :22032, capstone 0x1C58A6B-0x1C58A75) PhantomFinale@0x1BD1E90 starts TTO1102:Chameleon.<RPC_phantomRequiem>d__301::MoveNext@0x1C1B140 (:12606-12957): Row6Begin(venomPhantom, clip venomPhantom3) = PlayAnimation(venomPhantom3, 0.1) (:12707); Until(+0.55) = 1.95 (:12713): venomPhantom_requiem at the hero, hero rotation (:12741), Row6Sound venomShock_ring (:12743), per afterimage k (5, in shot order) Fire() (:12802; its fireFx venomPhantom_ghostFire at its bow point) and venomPhantom_beam from its BowPoint (:12774; the slot + its turn x the bow's local spot, calc.txt) to its foe's chest, LookRotation + RabbitTracer.Set (:12824-12846), then Row6Sound poisonVolley (:12753); Until(+0.67) = 2.07 (:12758): venomPhantom_rupture at each struck foe's chest, identity (:12910; the target 0.6 m up 10 m ahead), Row6Sound venomShock (:12925, struck > 0), ClearGhosts(shatter) (:12927; each afterimage's Shatter(): venomPhantom_ghostShatter, gone after shatterTime 0.35); Until(+1.2) = 2.6: Row6End (:12932-12947), the clip is 1.2 s; Row6Shake 0.25 left out (Bison decision 35); left out: the phantomVenom look on the foe and the poison burst (status / Effect Damage on its body, Sheep decision 4)",
    "cues": [
    [0.55, "fx", "tto/venomPhantom_requiem"],
    [0.55, "sound", "venomShock_ring"],
    [0.55, "fx", "tto/venomPhantom_beam", {"x": 0.865, "y": 1.109, "d": 0.002, "rot": [2.91, -4.95, 0], "to": [0, 0.6, 10], "ghost": 0}],
    [0.55, "fx", "tto/venomPhantom_beam", {"x": -2.022, "y": 1.109, "d": 0.17, "rot": [2.91, 11.63, 0], "to": [0, 0.6, 10], "ghost": 1}],
    [0.55, "fx", "tto/venomPhantom_beam", {"x": 2.138, "y": 1.109, "d": -0.865, "rot": [2.63, -11.13, 0], "to": [0, 0.6, 10], "ghost": 2}],
    [0.55, "fx", "tto/venomPhantom_beam", {"x": -3.272, "y": 1.109, "d": -0.579, "rot": [2.63, 17.18, 0], "to": [0, 0.6, 10], "ghost": 3}],
    [0.55, "fx", "tto/venomPhantom_beam", {"x": -0.585, "y": 1.109, "d": 1.99, "rot": [3.63, 4.18, 0], "to": [0, 0.6, 10], "ghost": 4}],
    [0.55, "sound", "poisonVolley"],
    [0.67, "fx", "tto/venomPhantom_rupture", {"y": 0.6, "d": 10, "shatterGhosts": true}],
    [0.67, "sound", "venomShock"]
    ],
    "builds": ["tto/venomPhantom_ghostFire", "tto/venomPhantom_ghostShatter"]
  },
  "apexHunt": {
    "why": "TTO1102:Chameleon.<RPC_apexHunt>d__304::MoveNext@0x1BF8FB0 (pseudo/Chameleon.c:3204-3645; plans/fx_chameleon/tto.md 2.2; in place, no hero lift: Penguin decision 8 / Bat decision 10; the lone target 10 m ahead): 0: Row6Begin(apexHunt) = PlayAnimation(apexHunt, 0.1) (:3265), ClearApexLocks (:3269), apexHunt_crouch at the cast spot, hero rotation (:3303), Row6Sound slayerCharge (:3304); Until 0.22 (:3308, capstone 0x1BF9C6E): apexHunt_takeoff there (:3330), Row6Sound massShot (:3331), the lift to 4.5 m by 0.55 (:3287-3290, :3425: u = (t - 0.22) / 0.33, 1 - (1 - u)^2; the page's hero stays); hover 0.55-2.45 (+ 0.08 sin(5 (t - 0.55)) up, :3489) with apexHunt_hang owned at the hero whenever none lives (:3517; EffectControl 0.6 + 0.3, followPosition + followState, myCommand unchanged: respawned at 0.55, 1.45, 2.35); 0.55: ApexLock(target) (:3531; ApexLock@0x1BCE270 :36531-36665): CharacterControl::AddApexLockFx@0x24AB5A0 (CharacterControl.c:6140) = preyFx, lockOnly, at the foe's collider centre (the target body 0.6 m up), scale clamp(2 x 0.3, 1, 4) = 1 (SpawnChameleonRow6Fx@0x24C50F0), Row6Sound markOfSlayer_hit (:36628); the lock tries at 0.85 ... 2.05 find no other foe (:3525-3545); 2.35 (:3618): ApexVolley@0x1BCE570 (:36853-37188): from = mount_Hand_L (:36928; apexHunt at 2.35 s: 0.229 m left, 0.95 up, 0.745 ahead), apexHunt_loose there, LookRotation(chest - from) (:37119), Row6Sound slayerFire (:37121), ClearApexLocks = the reticle's Release (:37147; fadeOut 0.25), ApexArrow with delay 0.04 x 0 (:37157): <ApexArrow>d__312@0x1BEC9D0 (:485-715): apexHunt_arrow at from, lerped to the chest over 0.12 s (:565-591), Destroy(arrow, 0.3) (:660): kill 0.42; 2.47: ImpactFx@0x1BD05B0 at Row6Ground(chest) = the ground 10 m ahead (:675-680): apexHunt_impact, identity, Row6Sound allSlain_hit; 2.75: Destroy(hang) (:3355), apexHunt_land at the cast spot (:3381); Until 3.1 (:3387, capstone 0x1BF9A75): Row6End (:3633), the clip is 3.1 s; Row6Shake left out (Bison decision 35); left out: the Prey look on the hit foe (a status look, Sheep decision 4) and the kill's apexHunt_trophy + allSlain_ring (TrophyFx@0x1BD9270: needs a kill, TTO1106)",
    "cues": [
    [0, "fx", "tto/apexHunt_crouch"],
    [0, "sound", "slayerCharge"],
    [0.22, "fx", "tto/apexHunt_takeoff"],
    [0.22, "sound", "massShot"],
    [0.55, "fx", "tto/preyFx", {"y": 0.6, "d": 10, "lockOnly": true, "release": 1.8, "kill": 2.05}],
    [0.55, "sound", "markOfSlayer_hit"],
    [0.55, "fx", "tto/apexHunt_hang"],
    [1.45, "fx", "tto/apexHunt_hang"],
    [2.35, "fx", "tto/apexHunt_hang", {"kill": 0.4}],
    [2.35, "fx", "tto/apexHunt_loose", {"x": -0.229, "y": 0.95, "d": 0.745, "rot": [2.17, 1.42, 0]}],
    [2.35, "sound", "slayerFire"],
    [2.35, "fx", "tto/apexHunt_arrow", {"x": -0.229, "y": 0.95, "d": 0.745, "rot": [2.17, 1.42, 0], "to": [0, 0.6, 10], "kill": 0.42}],
    [2.47, "fx", "tto/apexHunt_impact", {"d": 10}],
    [2.47, "sound", "allSlain_hit"],
    [2.75, "fx", "tto/apexHunt_land"]
    ]
  },
  "chainLightning": {
    "why": "TTO1102:Chameleon::DoRow6Skill@0x1BCF640 (pseudo/Chameleon.c:34817-34890): the coroutine, then RPC_AddStatus(stormCharge 0x268, 1, 8 s) on the Chameleon (:34875) and StormWatch; TTO1102:Chameleon.<RPC_chainLightning>d__317::MoveNext@0x1BFF820 (:6895-7022; plans/fx_chameleon/tto.md 2.3): 0: Row6Begin(chainLightning) = PlayAnimation(chainLightning, 0.1) (:6935), chainLightning_draw owned at the hero, hero rotation (:6954; EffectControl 0.36 + 0.3, followPosition + followState: cut at Row6End 0.5), Row6Sound cAttack_bow (:6955); the stormCharge look on her (<addStatus>d__481 0x24EE9B9 -> AddChameleonRow6Fx@0x24AC040: stormChargeFx at her collider centre, 0.98 m up (CharacterController m_Center, TTO bundle), scale 1, removed with the status at 8 s); Until 0.3 (:6960): OverloadFx@0x1BD18B0 at Row6Ground(hero) (:6980-6983; chainLightning_overload, identity, Row6Sound thunderDragon_ring2, :38799-38801), chainLightning_zapHot at Row6Chest(hero), identity (:6997), StormDragonForm (:7000; <StormDragonForm>d__328@0x1C5B820 :23687-24081): chainLightning_stormDragon parented to her (:23896), chainLightning_muzzle at her chest (:23917), every renderer of hers darkened toward StormBlack (0.07, 0.07, 0.09) over 0.25 s (:23959; StormDarken@0x1BD8C90, .cctor :39953) while stormCharge lasts; Until 0.5 (:7002): Row6End (:7013); 8.0 (stormCharge gone): zapHot at her chest (:23990), the aura's particles stopped and Destroy(aura, 1) (:24010-24017), the darkening undone over 0.6 s; StormWatch@0x1C5C3C0 (:24098-24185; a check 0.2 s after the cast, then every 0.1 s): the first check after 8.0 s (8.0-8.1, cued 8.05) puts staticDrain (0x269, 4 s) on her (:24156; staticDrainFx at her chest, AddChameleonRow6Fx) and Row6Sound rightStride_fire2 (:24159); the cues after the 0.9 s clip run on in the idle tail; Row6Shake left out (Bison decision 35); not cued: the storm arrows' fork and chain (StormArrow@0x1BD8290, HopFx@0x1BD0370: they come with Combo / Clear Arrow / Left Stride arrows while the buff lasts, none in this tile)",
    "cues": [
    [0, "fx", "tto/chainLightning_draw", {"cut": 0.5}],
    [0, "sound", "cAttack_bow"],
    [0, "fx", "tto/stormChargeFx", {"y": 0.98, "kill": 8}],
    [0.3, "fx", "tto/chainLightning_overload"],
    [0.3, "sound", "thunderDragon_ring2"],
    [0.3, "fx", "tto/chainLightning_zapHot", {"y": 0.98}],
    [0.3, "fx", "tto/chainLightning_stormDragon", {"stop": 7.7, "kill": 8.7}],
    [0.3, "skin", "Chameleon.StormDarken", {"kill": 8.3}],
    [0.3, "fx", "tto/chainLightning_muzzle", {"y": 0.98}],
    [8.0, "fx", "tto/chainLightning_zapHot", {"y": 0.98}],
    [8.05, "fx", "tto/staticDrainFx", {"y": 0.98, "kill": 4}],
    [8.05, "sound", "rightStride_fire2"]
    ]
  }
```

Notes on the entries:
- `to` (existing option) = the RabbitTracer's / the arrow's end: the target body's centre.
- `rot` = Unity Euler [pitch down, yaw right, 0] of `LookRotation(to - from)` (calc.py).
- The ghosts' kill: none in the cue (each ghost's own end is the part's: Shatter at the rupture cue, else its `life` 4).
- The status looks on her (`stormChargeFx`, `staticDrainFx`) are not parented on the page: she does not move, and their
  rotation is world identity in the game (SpawnChameleonRow6Fx), which the cue's hero-relative turn does not change for
  these round looks.

## 8. Open questions (each with my recommended answer)

1. **Venom Phantom's shot crossfade (0.05 s).** The SEQ has 0.1 (`^`), 0.2 (`~`) or a cut. Recommend **`^` now**
   (venomPhantom2's first and last poses differ, a cut snaps), and a 0.05 token only if a browser look says the 0.1 s
   fade blurs the five shots (P9).
2. **Venom Phantom: how many foes?** Recommend **the lone target** (the standing rule): the five ghosts and beams look the
   same with one foe (the slot is the ghost count). The 4-foe pack (2 + 1 + 1 + 1, foes within 8 m of the target) would
   add only hits and Ruptures at other spots.
3. **Apex Hunt: lift the hero?** Recommend **in place** (Penguin decision 8, Bat decision 10; the Frost Field leap's 2.5 m
   arc was kept in place too). The hang aura and the volley then come from her standing body. If the user wants the
   4.5 m jump (the skill's look, and the clip has no lift of its own), P10 lifts the hero 0.22-2.75 s with the curve in
   2.2 and the loose / arrow move up (calc.txt: from y 5.483, `rot [27.81, 1.42, 0]`).
4. **Apex Hunt's lock reticle on the target.** Recommend **cued** at the target body (it is the skill's own lock marker,
   `AddApexLockFx`, not a status; as the Penguin's constellation marks and the Bat's servant ring), lockOnly, released
   at 2.35. The Prey status look (the same prefab, 12 s, on every arrow target) stays out.
5. **Apex Hunt's kill reward** (`apexHunt_trophy` + `allSlain_ring`, TTO1106). Recommend **out**: it needs a kill, and
   the 10 m target is a standing dummy (as no other tile kills its target). If wanted: `[2.47, "fx",
   "tto/apexHunt_trophy"]` + `[2.47, "sound", "allSlain_ring"]` (owned at the hero, followState: cut 3.1).
6. **Chain Lightning's tail to 12.05 s** (staticDrain's 4 s from 8.05). Recommend **keep it whole**: each status is under
   the 10 s cut (stormCharge 8 s, staticDrain 4 s), and the -60 % slow's look is what ends the skill.
7. **The storm arrows** (the fork / chain look on Combo, Clear Arrow and Left Stride while the buff lasts). Recommend
   **not cued**: the Chain Lightning cast shoots none, and those tiles play without the buff (a passive would be on; this
   is an active buff). A "storm" variant of the Combo tile would be a new tile, not this research's scope.
8. **The storm's darkening** (P6). Recommend **build it** (the hero-look precedent: Penguin decision 16); it is the
   skill's main look for 8 s with the aura.

## 9. For the Bible (offer to the user; that repo's own rules)

- Venom Phantom: the afterimages stand at fixed spots around the Chameleon, filled in shot order: 1.5 m right and left
  0.3 m back, 2.8 m right and left 1.1 m back, 1.6 m ahead (`GhostSlots`), sliding there in 0.18 s; each shot's look
  comes 0.06 s after the shot; the shot clip restarts on every shot (0.05 s crossfade).
- Apex Hunt: the hovering aura is respawned every 0.9 s while she hangs; the lock reticle is the Prey reticle in its
  lock-only form; the impact lands on the ground under the target.
- Chain Lightning: the storm darkens the Chameleon to near-black (0.07, 0.07, 0.09) over 0.25 s from 0.3 s, held while
  stormCharge lasts, lifted over 0.6 s; staticDrain lands 0-0.1 s after stormCharge ends (the watch's 0.1 s checks).

## Verification

Checker pass 2026-11-13, home PC, read only (no build, no browser). Re-read against the source: every string literal of
the five coroutines and their helpers resolved again with `checks/fx_chameleon_research/tto/strs.py` (Row6Begin /
Row6Spawn / Row6Sound / PlayAnimation arguments in `pseudo/Chameleon.c` :21679-22040, :160-484, :12606-12957,
:3204-3645, :36531-36665, :36853-37188, :485-715, :37299-37345 (ImpactFx), :6895-7022, :23687-24081, :24098-24185,
:35882-35979, :38740-38810); the floats in `vp_movenext.asm` (0.3, 0.22, 1.1, 0.06), `apex_movenext.asm` (0.22, 0.33,
0.55, 0.3, 0.08, 5, 2.25, 2.35, 2.45, 2.75, 3.1, 4.5, 24, 4), the pseudo-C's own annotations (Until 0.3 / 0.5 in
chainLightning, 0.55 / +0.12 / 1.2 in phantomRequiem, Later 0.55 / 0.06 in PhantomShot, 0.12 and Destroy 0.3 in
ApexArrow); the `.cctor` (:39950-39990: GhostSlots 1.5 / -0.3, -1.5 / -0.3, 2.8 / -1.1, -2.8 / -1.1, 0 / 1.6;
StormBlack 0.07, 0.07, 0.09) and `dump.cs:105270-105284` (GhostSlide 0.18, StormInTime 0.25, StormFadeTime 0.6); the
status dispatch in `addstatus.asm` (0x24EE99C-0x24EE9FE: phantomVenom / stormCharge / staticDrain -> AddChameleonRow6Fx
false, prey -> true); `probe.json` (31 prefabs, no AudioSource; the EffectControl life / afterLife / followState of
coil 0.4 + 0.3, hang 0.6 + 0.3, draw 0.36 + 0.3, trophy 1.0 + 0.6, hit 0.2 + 0.5); `cc.txt` (Chameleon centre 0.98);
`bones.py` re-run (mount_Hand_L venomPhantom2 0.06 s = -0.585 / 1.109 / 0.39; apexHunt 2.35 s = -0.229 / 0.95 / 0.745;
the rig's scales along the chain are all 1); every `rot` and bow point of the table in 2.1 recomputed by hand (the
yaw / pitch of LookRotation and the slot + turned bowLocal: all five rows match to the third decimal); the released
list (`wardrobe/tto_released.json`: all five clips) and the clip lengths (`clips.json`: 0.4, 0.2333, 1.2, 3.1, 0.9);
the page's SEQ grammar (`SEQ_ALT`, index.html:1285: `venomPhantom2^@0.22` parses as fade 0.1, step 0.22; a repeated
clip takes its twin action, `startStep` :1416-1421) and that each step re-runs its clip's cues (`fxStart` from
`startStep`, `FX.t = 0`, live effects kept).

**Everything in the report holds** (times, names, positions, picks, the one rank, the cue block's JSON) except:

1. **`"builds"` does not build TTO prefabs** (Read this first 2, section 7's `venomPhantom3` entry). `wardrobe_fx_tto.py`'s
   `cue_tto` (pipeline/wardrobe_fx_tto.py:592-605) reads only the entries' cue lists, never `builds`, and
   `wardrobe_fx.py`'s `cue_names` skips every `tto/` name, `builds` included (pipeline/wardrobe_fx.py:513-515). So
   `venomPhantom_ghostFire` / `_ghostShatter` reach the data only through `SKILL_FX["chameleon"]` (the report's
   section 6 build note, which is therefore required, not an alternative). The `builds` line stays harmless as a record;
   the SKILL_FX entry to paste (exact-case names from `probe.json`) is below.
2. **P10 is not a new part, and question 3 misses the newest precedent.** The page already has the `"lift"` cue kind
   (`LIFTS` / `HeroLift`, index.html:4652-4688; cue doc :4478-4479), made for the Bison's Titan Drop, and Bison
   decision 22 lifted that leap in place "because the leap is the skill's whole look". Apex Hunt's 4.5 m jump is the
   same case, so by analogy the lift is the closer answer (the planner's call; both blocks below). The report's lift
   variant numbers are also wrong for the page: an effect's group is put at the hero root's world position when it
   spawns (`Fx` constructor, index.html:4006: `C.root.getWorldPosition(this.group.position)`), so under a lift a cue's
   `y` and `to` are relative to the **lifted** hero: the loose / arrow keep `y 0.95` (not 5.483) with `rot [27.81, 1.42,
   0]`, and the ground / target spots get the lift subtracted (target body at 0.55 s: 0.6 - 4.5 = -3.9; arrow end at
   2.35 s: 0.6 - 4.533 = -3.933; impact at 2.47 s: 0 - 4.48 = -4.48, the fall's 4.5 (1 - (0.02 / 0.3)^2)).
3. Minor: `<PhantomShot>b__0` is `Later(0.55)` (:35961, `DAT_183004d54 = 0.55`): Row6End 0.55 s after a shot (1.73 s
   after the 5th), not "0.44 s after the last shot" (section 2.1). Nothing cued changes.
4. P1's `NewArc` constants are verified, no longer UNVERIFIED: `checks/fx_chameleon_research/parts/disasm_ChameleonLightning.txt`
   :372-400 reads `nextArc = time + gap + Random.Range(0, gap)`, `th1 = Range(0, 6.28319)`, span `Range(0.8, 2.2)`, sign
   `Random.value < 0.5 ? -1 : 1`, heights `Range(0.05, height)` (as `parts.md` T1).
5. **The ghost's cue options disagree with `parts.md` T2**, which proposes `{"slide": [[t, x, y, d, yaw, 0.18]], "fire":
   [t], "shatter": t}` on the ghost cue. That shape cannot work: the one `venomPhantom2` entry plays five times with the
   same cues, so per-ghost slot / fire / shatter times cannot be written into it. This report's shape (`bow`, `face`,
   `slide`, `slots` on the ghost, the slot = live ghosts of this play % 5; `ghost: k` on each beam = ghost k's Fire();
   `shatterGhosts` on the rupture = ClearGhosts(true)) is the one the part must read (noted in parts.md's Verification).
6. Line drift only (index.html is being edited by another build while this was checked; numbers as of this pass): the SEQ line is now index.html:1211 (was :1190); `cueOf` is :4491
   (was :4410-4413).

Not checked here (another checker's): `effect_only.md`'s RPC_ listing.

### Corrected paste-ready blocks

`pipeline/wardrobe_fx_tto.py`, inside `SKILL_FX` (required, item 1):

```python
    # plans/fx_chameleon/tto.md section 5: all 31 Chameleon TTO-only prefabs (no arcana style); the ghost's own
    # venomPhantom_ghostFire / _ghostShatter (ChameleonAfterimage fireFx / shatterFx, named only by the part), the foe
    # status looks, the kill reward and the storm arrows (not cued) are built too
    "chameleon": [
        # Venom Phantom: TTO1102:Chameleon.<RPC_venomPhantom>d__294::MoveNext@0x1C581A0, <PhantomShot>b__1@0x1BF5870,
        # <RPC_phantomRequiem>d__301::MoveNext@0x1C1B140, EchoFx@0x1BCFE00; AddChameleonRow6Fx (phantomVenom)
        "venomPhantom_coil", "venomPhantom_shot", "venomPhantom_hit", "venomPhantom_ghost", "venomPhantom_ghostFire",
        "venomPhantom_ghostShatter", "venomPhantom_requiem", "venomPhantom_beam", "venomPhantom_rupture",
        "venomPhantom_echo", "phantomVenomFx",
        # Apex Hunt: <RPC_apexHunt>d__304::MoveNext@0x1BF8FB0, ApexVolley@0x1BCE570, <ApexArrow>d__312@0x1BEC9D0,
        # ImpactFx@0x1BD05B0, TrophyFx@0x1BD9270, CharacterControl::AddApexLockFx@0x24AB5A0 (preyFx)
        "apexHunt_crouch", "apexHunt_takeoff", "apexHunt_hang", "apexHunt_loose", "apexHunt_arrow", "apexHunt_impact",
        "apexHunt_land", "apexHunt_trophy", "preyFx",
        # Chain Lightning: <RPC_chainLightning>d__317::MoveNext@0x1BFF820, OverloadFx@0x1BD18B0,
        # <StormDragonForm>d__328@0x1C5B820, StormArrow@0x1BD8290, StormArrowHit@0x1BD8120, HopFx@0x1BD0370;
        # AddChameleonRow6Fx (stormCharge, staticDrain)
        "chainLightning_draw", "chainLightning_overload", "chainLightning_zapHot", "chainLightning_stormDragon",
        "chainLightning_muzzle", "stormChargeFx", "staticDrainFx", "chainLightning_arrow", "chainLightning_zap",
        "chainLightning_bolt", "chainLightning_boltHot",
    ],
```

The section 7 entries stand as written for the in-place answer. For the lift answer (item 2), `index.html`'s `LIFTS`
gains (times from the cue at 0.22 s; [t, height, in-tangent, out-tangent], `liftAt`'s hermite: the lift's quadratic
1 - (1 - u)^2 is exact with these tangents (4.5 x 2 / 0.33 = 27.27 m/s), the hover `0.08 sin(5 (t - 0.55))` keyed at its
peaks and zeros (0.4 m/s there), the fall 4.5 (1 - s^2) exact (end slope -30 m/s); the game's 6 mm step at 2.45 s left
out):

```js
  apexHunt: [[0, 0, 0, 27.2727], [0.33, 4.5, 0, 0.4], [0.6442, 4.58, 0, 0], [0.9584, 4.5, -0.4, -0.4], [1.2726, 4.42, 0, 0],
    [1.5867, 4.5, 0.4, 0.4], [1.9009, 4.58, 0, 0], [2.23, 4.494, -0.399, 0], [2.53, 0, -30, 0]],
```

and the `apexHunt` entry's cues become (the why as written, with "the page's hero stays" replaced by "the lift, LIFTS
apexHunt, from 0.22 s; cue spots relative to the lifted hero (Fx, index.html:4006)"):

```json
    "cues": [
    [0, "fx", "tto/apexHunt_crouch"],
    [0, "sound", "slayerCharge"],
    [0.22, "lift", "apexHunt"],
    [0.22, "fx", "tto/apexHunt_takeoff"],
    [0.22, "sound", "massShot"],
    [0.55, "fx", "tto/preyFx", {"y": -3.9, "d": 10, "lockOnly": true, "release": 1.8, "kill": 2.05}],
    [0.55, "sound", "markOfSlayer_hit"],
    [0.55, "fx", "tto/apexHunt_hang"],
    [1.45, "fx", "tto/apexHunt_hang"],
    [2.35, "fx", "tto/apexHunt_hang", {"kill": 0.4}],
    [2.35, "fx", "tto/apexHunt_loose", {"x": -0.229, "y": 0.95, "d": 0.745, "rot": [27.81, 1.42, 0]}],
    [2.35, "sound", "slayerFire"],
    [2.35, "fx", "tto/apexHunt_arrow", {"x": -0.229, "y": 0.95, "d": 0.745, "rot": [27.81, 1.42, 0], "to": [0, -3.933, 10], "kill": 0.42}],
    [2.47, "fx", "tto/apexHunt_impact", {"y": -4.48, "d": 10}],
    [2.47, "sound", "allSlain_hit"],
    [2.75, "fx", "tto/apexHunt_land"]
    ]
```

(The crouch, take-off and land stand where the lift is 0; the hangs are followPosition and ride the lift. P5's mover
must take `to` as hero-relative at the spawn, as RabbitTracer's `to` is.)
