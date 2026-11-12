# Mole effects: the parts the page cannot draw yet (or draws wrongly)

Research 13/11/2026, home PC (one of the Mole fx researchers; scope: every part the Mole's effects need: the inventory's
78, the 13 Mole prefabs it does not list, the components `wardrobe_fx.effect()` drops, the shaders, the hero code acting
on its effects, the summons the Mole's skills make, and the released TTO skills' prefabs). Models:
`plans/fx_penguin/parts.md`, `plans/fx_sheep/parts.md`, `plans/fx_cat/parts.md`, `plans/fx_bison/parts.md`. Read only:
nothing in `wardrobe/data` was written; `wardrobe_fx.py` / `wardrobe_fx_tto.py` ran with `--probe` only; no browser.
`Mole.cs`, `Mole_<x>.cs`, `rotationControl.cs`, `Math.cs`, `ProjectileControl.cs`, `AutoGyroGun.cs`, `BarrelBot.cs`,
`KingKaiser.cs` lines are `D:\12tails\DecompiledSource\<file>` (opaque predicates worked by `annotate.py`, every one
evaluated, then read by hand); TTO is `TTO1102:` = `D:\12tails\DecompiledSource_TTO_2026-11-02` (`dump.cs`, `methods.tsv`,
`pseudo/Mole.c`).

Probes (read only, outputs beside them) in `checks/fx_mole_research/parts/` (git-ignored):
- `probe.py` -> `probe.txt` (+ `mats.py` -> `mats.txt`, `show.py`): all 91 prefabs in `heroes/mole/effects` through
  `wardrobe_fx.effect()` with an unknown script's field bytes and raw words, every material's blend, and the components
  `effect()` drops. Last line: `UNKNOWN scripts: Mole_bazooka [0], Mole_cartBomb [0], Mole_flameCarnival [0],
  rotationControl [16], Mole_grenadeCluster [0], Mole_mine [4 x4], Mole_missile [8], Mole_mortarShot [0], Mole_napalm [0],
  Mole_nAttack [0], Mole_stunGrenade [4], Mole_stunMine [4 x2], Mole_timeNuke [16 x2], CharacterControl [684],
  Mole_warCapital [0], Mole_warMissile [8]`.
- `fx_probe_all.json` (+ `allsum.py`): `wardrobe_fx.py mole --probe <all 91>`: **12 effects raise today** (no layout):
  flameCarnival_fire, mine1-4, missile_fire, stunGrenade, stunMine1-2, timeNuke1-2, warMissile. `fx_probe.json` +
  `fxsum.py` -> `fx_probe_sum.txt`: node transforms of the ones the parts touch.
- `probe_ps.py` -> `probe_ps.txt`, `ps_sum.py` -> `ps_sum.txt`: the three Unity 3.5 ParticleSystems' full type trees
  (bazooka_ring, napalm_ring, warCapital) and the PhysicsManager (gravity -9.8); `ps_mats.py` -> `ps_mats.txt`: their BB
  materials through `wardrobe_fx.bb_material`.
- `tto_bbcopies.json` + `tto_sum.py` -> `tto_sum.txt`: TTO's copies of 17 Mole prefabs (`wardrobe_fx_tto.py mole --probe`):
  the scripts' field names, the systems re-serialised.
- `catalog_keys.py` -> `catalog_keys.txt`; `tto_released.json` + `tto_rel_sum.py` -> `tto_rel_sum.txt` (21 prefabs of the
  released TTO skills).
- `robots.py` -> `robots.txt`, `probe_robots.py` -> `probe_robots.txt`, `probe_robots_kk.txt`: the summons.
- `src/*.txt` / `src/*.s.txt`: `annotate.py` (each `if (a - b ==/!= c)` replaced by TRUE / FALSE, line numbers kept) and
  `squeeze.py` (dead branches dropped) of every script above. Read the `.txt` when nesting matters.

## Read this first

1. **Sixteen Mole scripts block or spoil 24 effects; every shader is already built.** 12 effects do not extract (a script
   with field bytes and no layout); 9 more extract but stand still or never end; 3 lose their Shuriken.

   | effect | what blocks it | today |
   |---|---|---|
   | `nAttack_fire`, `mortarShot_fire`, `stunGrenade`, `grenadeCluster_fire`, `napalm`, `bazooka_fire` | `Mole_nAttack` / `_mortarShot` / `_stunGrenade` (4 bytes) / `_grenadeCluster` / `_napalm` / `_bazooka`: the shell's flight (gravity, life, LookAt), its hit on contact | stunGrenade **not buildable**; the other five build and **hang in the air** at the muzzle |
   | `missile_fire`, `warMissile` | `Mole_missile` / `Mole_warMissile` (8 bytes, `mTarget`): a homing missile | **not buildable** |
   | `cartBomb_fire` | `Mole_cartBomb` (0 bytes): the 3 s fuse; the hero's code drives it at 6 m/s | builds, stands still, never explodes |
   | `mine1-4`, `stunMine1-2` | `Mole_mine` / `Mole_stunMine` (4 bytes, `mLv`): data only on the owner's screen | **not buildable** |
   | `flameCarnival` | `Mole_flameCarnival` (0 bytes): a trap, data only on the owner's screen | builds (fine; lives forever: the cue's `kill`) |
   | `flameCarnival_fire` | `rotationControl` (16 bytes: spin 180 deg/s about y) | **not buildable** |
   | `timeNuke1-2` | `Mole_timeNuke` (16 bytes): the 60 s countdown label (OnGUI), detonate / explode | **not buildable** |
   | `warCapital` | `Mole_warCapital` (0 bytes): `open` then `root` (loop); `CharacterControl` (NOT_DRAWN) | builds; plays `open` once and freezes |
   | `bazooka_ring`, `napalm_ring`, `warCapital` | Unity 3.5's ParticleSystem (Shuriken), dropped by `effect()` | build without their smoke / fire puffs |
   | `chopper` | its AudioSource has `playOnAwake` off: the hero's code starts it (`Mole.cs:33663`) | silent |

2. **Shaders: nothing to build.** The Mole's materials (`mats.txt`): addsoft 116, opaque 48, multiply2 13, alpha 4, add 2,
   multiply 1, premul 1, `shader:Particles/AdditiveOffset` 3 (megaDrill_hit / megaPunch_hit rings: `particles.js`, built),
   `shader:Transparent/AdditiveAlpha` 3 (the shells `nAttack` on nAttack_fire / mortarShot_fire, `napalm` on napalm:
   `additivealpha.js`, built with the Cat; `material()` saves `cut`, `wardrobe_fx.py:335-338`). The napalm canister's
   `_Color` is pure red (1, 0, 0) and `_AdditiveRange` 0.9104 (rip `Material/napalm.mat`): its lit pass is red-lit, as the
   game draws it. The AlphaTimers (bazooka_hit, bombardment_hit) drive `add` materials: `alphatimer.js` handles them.
3. **The three Shuriken systems match TTO's copies field for field** (`ps_sum.txt` against `tto_sum.txt`: life, speed,
   size, burst times / counts, cone / hemisphere shapes, the space). The graft (`SHURIKEN_FROM_TTO`) covers them; their
   three materials (Cloud1, Bomb1_a, Smoke1, all BB `addsoft`) rule out the one-per-class `SHURIKEN_MAT` (`wardrobe_fx.py:197`).
   `shuriken.js` already has every module they use
   (Initial, Shape hemisphere / cone, Emission bursts, Size, Color, Force, ClampVelocity). The Chameleon's graft route
   (now in `wardrobe_fx.py`: BB's own materials, matched by name and material) handles this: one table line.
4. **Summons outside the Effects folder.** Auto Gyro Gun, Barrel Bot and King Kaiser (three skills) instantiate whole robot
   characters from `Resources/GameAssets/Characters/Robots/` (`Mole.cs:11902-12031`, `:12472-12601`, `:35720-35794`), as
   the Penguin's Mana Vortex (`EXTRA_FOLDERS`). Their scripts (`AutoGyroGun` 36 bytes, `BarrelBot` 208, `BarrelBotAI` 8,
   `KingKaiser`) have no layout, and **King Kaiser does not extract at all**: `clip run: compressed / float curves / events
   are not read yet` (`probe_robots_kk.txt`), a gap in `wardrobe_fx.py`'s clip reader. Part 11; a planner's decision
   (question 6).
5. **The inventory misses 13 Mole prefabs** (hero prefab fields and `RPC_*_hit` loads): `chopper`, `chopper_forwardDust`,
   `chopper_hit`, `chopper_startDust` (`Mole.cs:19763-19781`), `missileBase`, `missile_fire`, `missile_hit`
   (`:19784-19802`), `nAttack_fire`, `nAttack_hit` (`:19436-19439`), `deadEffect` (`:20084`), `synchroMole`,
   `synchroMole_ring`, `timeNuke_explosion` (`Mole_timeNuke.cs:350`, the nuke's own field). Of them `missile_fire` (Mole_missile)
   and `nAttack_fire` (Mole_nAttack) need parts; the rest use built parts (`allsum.py`). `chopper` also needs the sound
   start (part 9). Inventory gaps for `wardrobe_fx_inventory.py` (later): it does not see playOnAwake-off sources, nor the
   Shuriken material count, nor hero code moving an effect (the cart).
6. **Game quirks (offer to the user for the Bible; none changes a cue).**
   - Mines, Stun Mines, Flame Carnival and Time Nukes are invisible **only to enemies** (`Game.mPlayer.layer !=
     owner.layer` -> every Renderer off: `Mole_mine.cs:69-97`, `Mole_stunMine.cs:69-97`, `Mole_flameCarnival.cs:65-98`,
     `Mole_timeNuke.cs:80-111`). The owner sees them: the page shows them (the owner's view).
   - Flame Carnival's trigger turns the **Mole's** renderers on, not the trap's (`Mole.cs:39204-39218`:
     `this.$self_.gameObject.GetComponentsInChildren(Renderer)`): an enemy who sets it off still sees no trap, only the fire.
   - King Kaiser's colour is `Skin / 100` (r g b k w) with the else branch `KingKaiser_p` (`Mole.cs:35709-35776`), and BB has
     no `kingkaiser_p` (`robots.txt`): a sixth colour would summon nothing.
   - `warCapital_dead` is loaded by name (`Mole_warCapital.cs:599`) and does not exist in BB (`names.txt`): "Cannot find
     warCapital_dead effect" (`:618`) on every War Capital death.
   - The Stun Grenade's blast is the **normal attack's** `nAttack_hit` (`Mole_stunGrenade.cs:193`), though BB has an
     `RPC_stunGrenade_hit` loading `stunGrenade_hit` (`Mole.cs:11359`), a prefab BB does not hold.
   - `missile_hit` is drawn with the **hero's** rotation, wherever the missile lands (`Mole.cs:13208`).
   - A Mole_missile / Mole_warMissile that meets nothing explodes at the end of its life (`Mole_missile.cs:64-139`,
     `Mole_warMissile.cs:64-120`): `RPC_missile_hit` at its own position.
   - Stun Mine's life is `talAdjust(60)` (`Mole_stunMine.cs:60`; the Bible already notes it as a BB bug).

## The Mole's blocked set

"Where" is where BB spawns it. Cue shapes below use the Wolf / Sheep / Penguin / Bat / Cat keys; the clip times and
which tile plays them are the skills researchers' (`skills_a.md`, `skills_b.md`, `attacks_emotes.md`, `effect_only.md`),
so treat the cues here as the parts' contract.

| effect | skill (spawn) | missing part(s) | where |
|---|---|---|---|
| `nAttack_fire` (+ `nAttack_hit`) | Normal Attack (`RPC_nAttack_fire` `Mole.cs:10070-10092`) | Mole_nAttack mover | firePos, `LookRotation(getTrajectoryVector(firePos, firePos + fireDir, 15))`, life 10 |
| `mortarShot_fire` (+ `mortarShot_hit`) | Mortar Shot (`:10745-10783`) | Mole_mortarShot mover | firePos, `LookRotation(getMortarVector(.., 20))`, life 5 |
| `stunGrenade` (+ `nAttack_hit`) | Stun Grenade (`:11272-11319`) | Mole_stunGrenade layout + mover | firePos, `LookRotation(getTrajectoryVector(.., 15))`, life 3 |
| `grenadeCluster_fire` (+ `grenadeCluster_hit`) | Grenade Cluster (`:13787-13822`) | Mole_grenadeCluster mover | firePos + 0.5 fireDir, `LookRotation(fireDir)`, life 5 |
| `napalm` (+ `napalm_hit`) | Napalm (`:13714-13752`, hit coroutine `:37769`) | Mole_napalm mover | firePos, `LookRotation(getMortarVector(.., 20))`, life 5 |
| `bazooka_fire` (+ `bazooka_hit`) x3 | War Factory 2, Bazooka (`$RPC_bazooka$23990` `:41336-41361`) | Mole_bazooka mover | hero + `TransformDirection(-0.25, 1, 1)`, hero forward, life 2 |
| `missile_fire` (+ `missile_hit`) | Missile (`:13133-13192`) | Mole_missile layout + homing mover | firePos + fireDir, `LookRotation(fireDir)`, life 5, target |
| `warMissile` (+ `warMissile_hit`) | War Capital's volleys (`RPC_warMissile_fire` `:14494-14566`) | Mole_warMissile layout + homing mover | target + flat 2 m random - 6 fireDir + 6 up, `LookRotation(fireDir - up)`, life 12 |
| `cartBomb_fire` (+ `cartBomb_hit`) | War Factory 5, Cart Bomb (`$RPC_cartBomb$24030` `:43088-43376`) | Mole_cartBomb fuse; the hero's drive (`fx:cartBomb_fire`) | `getSpawnPos(hero + 0.5 forward)`, hero rotation |
| `mine1-4`, `stunMine1-2` | Landmine, Stun Mine (`:24281-24398`, `:27067-27106`) | Mole_mine / Mole_stunMine layouts (data only) | the mine spot, `Euler(270, 90, 0)` |
| `flameCarnival` (+ `flameCarnival_fire`) | Flame Carnival (`:38518`, fire `:38980`) | (data only); `rotationControl`; the trap's clips (`fx:flameCarnival`) | hero + tDir, identity |
| `timeNuke1-2` (+ `timeNuke_explosion`) | Time Nuke (`RPC_timeNuke_create` `:11612-11730`), Detonate (`:31102-31171`) | Mole_timeNuke layout + countdown label + detonate | mPos, identity |
| `warCapital` | War Capital (`RPC_warCapital_create` `:14239-14463`) | Mole_warCapital (clip switch); Shuriken graft | tPos, `LookRotation(tDir)` |
| `bazooka_ring`, `napalm_ring` | Bazooka (`:41168`), Napalm (`:37146`) | Shuriken graft (per-effect material) | hero (bazooka: `egpdC7u0CW`, hero rotation) |
| `chopper` | Chopper (`$RPC_chopper$23799` `:33589-33604`) | the sound start (`fx:chopper`) | bone `mount_Cannon`, local identity |
| (hero) | Charge Attack's burrow (`$RPC_cAttack1$23473` `:22031-22053`, `:21583`, `:21951`) | the hero hidden while under (a cue kind) | - |
| AutoGyroGun1-4, BarrelBot1-4, KingKaiser_r/g/b/k/w | Auto Gyro Gun, Barrel Bot, King Kaiser | summons: folders, layouts, clip switches; King Kaiser's compressed clips | the summon spot |

## LAYOUTS (paste into `pipeline/wardrobe_fx.py`, after the Cat's block)

```python
# the Mole's parts (plans/fx_mole/parts.md, 2026-11-13; checks/fx_mole_research/parts/probe.txt: each instance's bytes are
# the listed fields exactly; TTO's re-serialised copies name the same fields, checks/fx_mole_research/parts/tto_sum.txt);
# the other Mole scripts keep every field private (0 field bytes)
LAYOUTS.update({
    "Mole_mine": [("mLv", "i")],                     # Mole_mine.cs:239 (4 bytes; mine1-4 = 1-4: the damage rank only)
    "Mole_stunMine": [("mLv", "i")],                 # Mole_stunMine.cs:239 (4; stunMine1-2 = 1-2)
    "Mole_stunGrenade": [("mLv", "i")],              # Mole_stunGrenade.cs:355 (4; 1; RPC_stunGrenade_fire sets it, Mole.cs:11319)
    # Mole_timeNuke.cs:341, :344, :350 (16 bytes: 1 / 2, true, the timeNuke_explosion prefab [24, 386])
    "Mole_timeNuke": [("mLv", "i"), ("isVisible", "b"), ("timeNuke_explosion", "r")],
    "Mole_missile": [("mTarget", "r")],              # Mole_missile.cs:433 (8; [0, 0]: the hero's code sets it, Mole.cs:13189)
    "Mole_warMissile": [("mTarget", "r")],           # Mole_warMissile.cs:345 (8; [0, 0]; Mole.cs:14563)
    # rotationControl.cs:75-84 (16 bytes; flameCarnival_fire/fire_ctrl (0, 180, 0), false; also the Monkey's lavu)
    "rotationControl": [("mRotation_x", "f"), ("mRotation_y", "f"), ("mRotation_z", "f"), ("useWorldRotation", "b")],
    "Mole_bazooka": [], "Mole_cartBomb": [], "Mole_flameCarnival": [], "Mole_grenadeCluster": [], "Mole_mortarShot": [],
    "Mole_napalm": [], "Mole_nAttack": [], "Mole_warCapital": [],
})
```

Two more extractor lines (lead, `wardrobe_fx.py`):
- `SHURIKEN_FROM_TTO["mole"] = ["bazooka_ring", "napalm_ring", "warCapital"]` and **no** `SHURIKEN_MAT` entry (part 8):
  the Chameleon's route, in the working tree since this research began (`wardrobe_fx.py:186-194` comment, `:494`: a class
  with no SHURIKEN_MAT entry keeps each BB ParticleSystemRenderer's own materials and matches the TTO node of the same name
  whose renderer's first material is `"tto_" + BB's mats[0]`). The Mole's three match one to one: BB `Cloud1` / `Bomb1_a` /
  `Smoke1` -> TTO `tto_Cloud1` / `tto_Bomb1_a` / `tto_Smoke1` (`tto_sum.txt`), one system per effect, unique names. (Had
  that route not landed: `SHURIKEN_MAT` is one material per class, `:197`, and the Mole's three systems have three.)
- The summons, if built (part 11, question 6): `EXTRA_FOLDERS["mole"] = ["gameassets/characters/robots/autogyrogun",
  "gameassets/characters/robots/barrelbot", "gameassets/characters/robots/kingkaiser"]`; `NOT_DRAWN |= {"AutoGyroGun",
  "BarrelBot", "BarrelBotAI", "KingKaiser", "KingKaiserAI"}` (or their layouts, below); the clip reader's compressed /
  float curves for King Kaiser.

## Each part

Page parts plug in as the comment above `FX_PART_FILES` says (`wardrobe/index.html:3845-3888`):
`wardrobe/fxparts/<file>.js` default-exports `register(api)` and calls `api.part(type, build)`; `build(fx, node, comp, mat,
nodeDef, data)` returns `{ node, update(dt, cam) ("destroy" removes the node), stop?(), dispose?() }` or null;
`"fx:<effect>"` = the hero's code acting on that effect, built once on its root (comp null); `api.spawn(name, at, opts)`
makes an effect a script instantiates (the entry's `"builds"` puts it in `fx.json`); `fx.cutAt` is the cue's `cut` in
clip time, compared with `api.FX.t`. Space: every root hangs in the effect's mirror group (Unity's world, the hero's feet
at the origin, +z her facing, y 0 the floor). The target body (Bat decision 4, every class): a cylinder at (0, 0.6, 10),
height 1, radius 0.3; `ClosestPointOnBounds` = the point clamped into its box x +-0.3, y 0.1..1.1, z 9.7..10.3.

### 1. The Mole's shells: Mole_nAttack, Mole_mortarShot, Mole_stunGrenade, Mole_grenadeCluster, Mole_napalm, Mole_bazooka (`fxparts/mole.js`, new)

**What they do in BB.** All six are one pattern on the prefab's root (the Rigidbody's node; probe.txt: each root has
ProjectileControl + the script + a trigger BoxCollider + Rigidbody):
- ctor: a private local velocity (`Mole_nAttack.cs:28` (0, 0, 15); `Mole_mortarShot.cs:26` (0, 0, 20);
  `Mole_stunGrenade.cs:28` (0, 0, 15); `Mole_grenadeCluster.cs:28` (0, 0, 6); `Mole_napalm.cs:26` (0, 0, 20);
  `Mole_bazooka.cs:28` (0, 0, 24)). Private: not in the prefab bytes (0 bytes; stunGrenade's 4 are `mLv`).
- Awake: layer 1, `rigidbody.velocity = transform.TransformDirection(v)` (`Mole_nAttack.cs:47-53`, the others' :45-57):
  along the spawn rotation, once.
- FixedUpdate: `clock += dt`; at `ProjectileControl.life` Destroy; else `transform.LookAt(position + velocity)`
  (`Mole_nAttack.cs:72-88`; mortarShot :70-86, stunGrenade :76-92, grenadeCluster :72-88, napalm :70-86). **Mole_bazooka
  has no LookAt** (`Mole_bazooka.cs:72-81`: life only; it has no gravity, so its heading never changes anyway).
- The life is the hero's code's, not the prefab's 0 / 10: nAttack `10 x rangeMod` (`Mole.cs:10089`), mortarShot 5
  (`:10780`), stunGrenade 3 (`:11307`), grenadeCluster 5 (`:13819`), napalm 5 (`:13749`), bazooka 2 (`:41361`);
  rangeMod 1.
- Physics (probe.txt skipped comps): Rigidbody mass 1, drag 0, **gravity on** for nAttack, mortarShot, stunGrenade,
  grenadeCluster, napalm; **off** for bazooka. Trigger boxes: 0.25 x 0.25 x 0.5 (nAttack, mortarShot, napalm, bazooka),
  0.25 cube (stunGrenade, grenadeCluster). Gravity -9.8 (`probe_ps.txt`: the PhysicsManager).
- OnTriggerEnter: skips the owner's layer, layer 1, layer 2 (`Mole_nAttack.cs:132-146`, the same block in each); on the
  owner's client `vector = mCollider.ClosestPointOnBounds(collider.bounds.center)` (`:156`) and the hit RPC, then
  `Destroy(gameObject)` (`:317`), the legacy smoke trail on the root or a child with it.

| script | hit RPC (file:line) | hit effect, rotation (Mole.cs) |
|---|---|---|
| Mole_nAttack | `RPC_nAttack_hit(vector, zero)` `Mole_nAttack.cs:201` | `nAttack_hit`, identity `:10105` |
| Mole_mortarShot | `RPC_mortarShot_hit(vector, zero)` `Mole_mortarShot.cs:171` | `mortarShot_hit`, identity `:10830` |
| Mole_stunGrenade | `RPC_nAttack_hit(vector, zero)` `Mole_stunGrenade.cs:193` | `nAttack_hit`, identity `:10105` |
| Mole_grenadeCluster | `RPC_grenadeCluster_hit(vector, zero)` `Mole_grenadeCluster.cs:184` | `grenadeCluster_hit`, `LookRotation(zero)` = identity `:13865` |
| Mole_napalm | `RPC_napalm_hit(vector, vFlat(forward).normalized)` `Mole_napalm.cs:158-179` | `napalm_hit`, `LookRotation(hitDir)` `:37769` |
| Mole_bazooka | `RPC_bazooka_hit(vector, vFlat(forward).normalized)` `Mole_bazooka.cs:159-182` | `bazooka_hit`, `LookRotation(hitDir)` `:14036` |

**The spawn rotations** (the skills researchers' cues carry them as `rot`): nAttack and stunGrenade use
`Math.getTrajectoryVector(firePos, firePos + fireDir, 15)` (`Math.cs:885-1006`, the Cat's `trajectoryVector`, exported by
`cat.js`); mortarShot and napalm use `Math.getMortarVector(.., 20)` (`Math.cs:1011-1085`): `d = |vFlat(pos - target)|`,
`f = 0.5 asin(d g / v^2)` when `d < v^2 / |g| - 1` (`:1043-1049`), else `-0.5` (`:1057`), direction `sin(f) vFlat(pos -
target).normalized + cos(f) up` (`:1063-1069`): the **high lob**, its angle from vertical `|f|`; at d 10, v 20: f = -0.1237
rad, elevation 82.9 deg, flight about 4.05 s, range 10.0 m (height difference ignored). grenadeCluster and bazooka fly
along `fireDir` / the hero's forward.

**The page part (mole.js, about 70 lines), one builder for the six:**
- A table `SHELL = { Mole_nAttack: { v: 15, g: true, life: 10, look: true, half: [0.125, 0.125, 0.25], hit: "nAttack_hit",
  rot: "id" }, Mole_mortarShot: { v: 20, g: true, life: 5, ..., hit: "mortarShot_hit", rot: "id" }, Mole_stunGrenade: { v:
  15, g: true, life: 3, half: [0.125, 0.125, 0.125], hit: "nAttack_hit", rot: "id" }, Mole_grenadeCluster: { v: 6, g: true,
  life: 5, half: 0.125 cube, hit: "grenadeCluster_hit", rot: "id" }, Mole_napalm: { v: 20, g: true, life: 5, ..., hit:
  "napalm_hit", rot: "flat" }, Mole_bazooka: { v: 24, g: false, life: 2, look: false, hit: "bazooka_hit", rot: "flat" } }`
  (the lines above in a comment per row).
- Build: `vel = (0, 0, v)` x `fx.uQuat(node)` (TransformDirection at the spawn: the cue's rot is on the root).
- Each fixed step 0.02 s (cat.js's / bat.js's `STEP`): `vel.y -= 9.8 x 0.02` when `g`; `p += vel x 0.02`; `++k x 0.02 >=
  life` -> `"destroy"`; then the contact test, in this order:
  1. **the target body** (Bat decision 4): the box's centre within `0.3 + max(half)` of the axis (x 0, z 10) in xz and its
     y in `[0.1 - half.y, 1.1 + half.y]` -> hit point = `p` clamped into the body's box (`ClosestPointOnBounds`);
  2. **the floor**: the box's lowest corner (`y - (half.y cos p + half.z |sin p|)`, p the pitch; cat.js's test) `<= 0` ->
     hit point = `(p.x, 0, p.z)`.
  On contact: `api.spawn(hit, { x, y, d: z, rot })` with `rot = [0, 0, 0]` for "id" (Quaternion.identity: the page's
  default facing, the hero's) or `[0, yaw(vel), 0]` for "flat" (`LookRotation(vFlat(forward))`: cat.js's `lookEuler` with
  the pitch dropped), and `"destroy"`.
- Between steps the node is drawn at `p + vel x acc`, its quaternion `LookRotation(vel)` when `look` (bazooka keeps its
  spawn rotation), `node.updateMatrixWorld(true)` so the trail emitter after it sees the move (cat.js's line).
- The hits must be in `fx.json`: each projectile cue's entry carries `"builds": [<hit>]` (nAttack_hit for both Normal
  Attack and Stun Grenade).
- APPROXIMATED: the page has only the floor and the target body as colliders; a shot that misses both flies its life out.

**Cue shapes** (the skills researchers' times; `fireDir` aimed at the target point, so the lobs land on it):
`[t, "fx", "nAttack_fire", {"x": X, "y": Y, "d": D, "rot": [-elev, 0, 0]}]` and the entry's `"builds": ["nAttack_hit"]`;
the same for `mortarShot_fire` / `napalm` (elevation 82.9 deg at 10 m from the getMortarVector above), `stunGrenade`,
`grenadeCluster_fire`, `bazooka_fire` (three, rot 0, from `(-0.25, 1, 1)`, `Mole.cs:41336-41341`).

### 2. Homing missiles: Mole_missile, Mole_warMissile (`fxparts/mole.js`)

**What they do in BB (`Mole_missile.cs`; `Mole_warMissile.cs` is the same code, line for line).**
- Field `public GameObject mTarget` (`:433`; warMissile `:345`); privates: clock, next-turn time, the ProjectileControl.
- Awake (`:21-37`): layer 1; `rigidbody.velocity = TransformDirection(ProjectileControl.velocity)` (`:34`): the prefab's
  (0, 0, 8) (missile_fire) / (0, 0, 12) (warMissile) (`probe.txt`).
- Update (not FixedUpdate; `:46-179`), only while `ProjectileControl.isInitialized` (`:51`; `Init(ownerID)` sets it,
  `ProjectileControl.cs:21-45`, called in the spawn frame: `Mole.cs:13146`, `:14523`) and not `isDestroyed` (`:55`):
  `clock += dt` (`:64`); at `life` (missile `5 x rangeMod`, `Mole.cs:13149`; warMissile the prefab's 12: the hero's code
  sets none, `:14520-14523`) the owner's client calls `RPC_missile_hit(position, forward)` (`:118`) / `RPC_warMissile_hit`
  (`Mole_warMissile.cs:101`), and Destroy (`:139`, `:120`): **it explodes where it is**. Else, with a target, every 0.2 s
  (`:151-157`): `forward = RotateTowards(forward, mTarget.collider.bounds.center - position, 0.3 rad, 1)` (`:162`),
  `rotation = LookRotation(forward)` (`:167`), `velocity = TransformDirection(ProjectileControl.velocity)` (`:172`).
  The first turn comes on the first frame (the next-turn time starts at 0).
- OnTriggerEnter (`:188-301`): any collider not on the owner's layer, 1 or 2 (`:235-247`) -> Destroy, `isDestroyed`
  (`:253-258`), the owner's client `RPC_missile_hit(ClosestPointOnBounds, forward)` (`:269-290`).
- Physics: no gravity, rotation frozen (m_Constraints 112), trigger box 0.2 x 0.2 x 0.5 centred 0.25 ahead.
- Hits: `missile_hit` at hitPos with **the hero's** rotation (`Mole.cs:13208`); `warMissile_hit` with
  `LookRotation(hitDir)` = the missile's forward (`:14615`).
- Spawns: missile_fire at `firePos + fireDir`, `LookRotation(fireDir)`, `mTarget` = the target character (`:13140`,
  `:13189`); warMissile at `firePos - 6 fireDir + 6 up`, `LookRotation(fireDir - up)` (45 deg down), firePos = a random
  target + `vFlat(2 x insideUnitSphere)` (`:14517`, `:43760-43801`), `mTarget` the same target (`:14563`).

**The page part (mole.js, about 40 lines), one builder for the two:**
- Speed `|ProjectileControl.velocity|` from the node's comps (8 / 12), life 5 / 12 (a table, cited).
- Target: the target body's centre `(0, 0.6, 10)` (Penguin decision 3: homing aims 0.6 m up), or the cue's `to` when
  given (index.html's cue option, as the bolts'). No target (`"to": null` in the cue): straight on.
- Per frame (Update, the page's dt): clock; at life -> spawn the hit at the node's position and `"destroy"`; every 0.2 s
  `RotateTowards` by 0.3 rad (three: the angle between forward and the aim, `min(0.3, angle)` about their cross axis;
  magnitude kept 1), velocity = forward x speed; `p += vel x dt`; the contact test of part 1 (body, then floor: half 0.1 /
  0.1 / 0.25, the box 0.25 ahead of the node); hit -> `api.spawn("missile_hit", { x, y, d, rot: [0, 0, 0] })` (the hero's
  rotation = the page's default facing) / `api.spawn("warMissile_hit", { ..., rot: lookEuler(forward) })`, `"destroy"`.
- `"builds": ["missile_hit"]` / `["warMissile_hit"]` on the entries.

### 3. Mole_cartBomb and the hero's drive: `cartBomb_fire` (`fxparts/mole.js`)

**What the script does (`Mole_cartBomb.cs`).** No fields. `Init(owner)` (`:27-40`, called in the spawn frame,
`Mole.cs:43132`): owner, its CharacterControl, started. Update (`:52-157`): `t += dt` (`:83`); while `t <= 3` (`:88`) and
the owner's `actionState == "attack"` (`:94`) and `myCommand == "cartBomb"` (`:100`): nothing; else, on the owner's
client, `RPC_cartBomb_hit(position, forward)` (`:127`) and Destroy (`:146`). (The predicates on the path: `:84`, `:128`
read `!=` against their own difference: FALSE, so dead.)

**The hero's drive (`Mole.cs`, coroutine `$RPC_cartBomb$24030`).** The cart is spawned at `getSpawnPos(hero + 0.5
forward)` (the floor under that point, `:43088`; `Math.cs:1090-1137`), the hero's rotation (`:43106`), direction = the
hero's forward (`:43093`); then every FixedUpdate (`Yield(4, WaitForFixedUpdate)`, `:43538`) while the cart lives: the
direction from the move keys (`:43267-43285`; none on the page: forward stays), `rotation = LookRotation(dir)`
(`:43291`), `rigidbody.velocity = 6 x dir` (`:43296`): flat, 6 m/s, the fall velocity reset every step (it stays on the
floor). When the cart is gone the hero goes to standby (`:43248-43254` -> case 5 `:43178-43235`).
Physics: a **non-trigger** CapsuleCollider (radius 0.5, centre y 0.55) and a Rigidbody with frozen rotation (probe.txt):
the cart is **stopped** by the target body (Unity's solver), it does not pass through.
`cartBomb_hit` at the cart's position, `LookRotation(hitDir)` = the cart's forward (`Mole.cs:14154`).

**The page part `Mole_cartBomb` (mole.js, about 25 lines)** (the script and the hero's drive in one, the cart is only
ever driven by this coroutine): from the spawn, every 0.02 s step, `p.z += 6 x 0.02` along the root's forward (the cue's
rot), capped at the target body: the cart's centre stops at `10 - 0.3 - 0.5 = 9.2` m along +z (APPROXIMATED: Unity's
contact solver, medium sure); at `t > 3` -> `api.spawn("cartBomb_hit", { x, y: 0, d: z, rot })` (rot = the cart's), and
`"destroy"`. The looping `cartBomb` AudioSource goes with it (Fx.dispose). `"builds": ["cartBomb_hit"]`.
Timeline in the game: cart at clip 0.3 (`Yield(2, 0.3)`, `:43540`), driving from 0.5 (`Yield(3, 0.2)`, `:43544`), at the
body about 1.95, boom at 3.3 (the fuse counts from Init); the skills researcher's times win.

### 4. Mole_mine, Mole_stunMine, Mole_flameCarnival: data only on the owner's screen; Flame Carnival's trigger (`fxparts/mole.js`)

**What they do.** Each `Init` (`Mole_mine.cs:31-114`, `Mole_stunMine.cs:31-114`, `Mole_flameCarnival.cs:21-110`): the ID,
the owner, the life `chaAdjust(60)` / `talAdjust(60)` / `chaAdjust(90)` s (`:60`, `:60`, `:53`), every renderer off for
an enemy's screen (Read this first 6), started. Update: Destroy when the life ends untriggered, or the owner is gone /
dead (`Mole_mine.cs:146-196`). OnTriggerEnter (4 m SphereCollider, `probe.txt`): an enemy (tag Player / Enemy, another
layer, layer > 2) -> triggered; mines wait 0.5 s (`Mole_mine.cs:540`, `Mole_stunMine.cs:542`) then `RPC_mine_hit` /
`RPC_stunMine_hit` at the mine (`:379`; + `RPC_smartShell_hit` with Smart Shell lv 1, `:396-413`) and Destroy (`:530`);
Flame Carnival starts `RPC_flameCarnival_fire(position)` (`Mole_flameCarnival.cs:280`) and stays.
`mLv` is the damage rank only (`Mole.cs:10609`, `:10642`).

**The page.** On the owner's screen the three draw nothing of their own: no part (as `Sheep_seal`). The cue's `kill`
is their end (the 10 s rule: 60 / 90 s -> 10). Add `"Mole_mine", "Mole_stunMine", "Mole_flameCarnival"` to `BUILT` in
`wardrobe_fx_inventory.py` ("data only: the owner sees them; the cue's kill"). Nothing at the 10 m target triggers
them: the trap sits 1 m ahead (`Mole.cs:38518`: `mPos + tDir`), its 4 m sphere does not reach the body at 10 m.

**Flame Carnival's fire, if a tile triggers it** (question 3): the hero's coroutine `$RPC_flameCarnival_fire$23930`
(`Mole.cs:38844-39256`): at its start the trap's `animation.Play("open")` + `audio.Play()` (`:39198-39201`; clips `open` /
`close` 0.5 s Once, the default `close` plays on spawn, `fx_probe_sum.txt`), `Yield(2, 0.3)` (`:39252`), then
`flameCarnival_fire` at the trap, identity (`:38980`), then 20 pulses `Yield(3, 0.3)` (`:39033`, `:39244`: 6 s, the damage
only), the trap's `Play("close")` (`:39047`), `Yield(4, 0.5)` (`:39248`), Destroy the trap (`:39014`). Page part
`fx:flameCarnival` (mole.js, about 15 lines): when the cue's option `"trigger": T` (age) is set, at T `fxAnim.play("open")`
and restart its AudioSource (`api.Sound.play`, the entry's h replaced, as audiocontrol.js), at T + 0.3
`api.spawn("flameCarnival_fire", { x, y, d })`, at T + 6.3 `play("close")`, at T + 6.8 `"destroy"`. flameCarnival_fire's
own EmitterControls (life 6) and AudioControl (0.5 in, 6, 0.5 out; `tto_sum.txt`, BB's the same) are built.

### 5. rotationControl: `flameCarnival_fire` (`fxparts/rotationcontrol.js`, new, generic; also the Monkey's `lavu`)

**What it does (`rotationControl.cs`).** Fields `mRotation_x`, `mRotation_y`, `mRotation_z` (float), `useWorldRotation`
(bool) (`:75-84`). Start (`:20-22`): keeps its world rotation. Update (`:27-50`): `useWorldRotation` -> `rotation = start x
Euler(dt x (x, y, z))` (`:38`: a one-frame offset from the start each frame, a jitter, not a spin: kept as written);
else `transform.Rotate(dt x (x, y, z))` (`:47`: Space.Self, degrees, accumulating).

**The Mole's use.** `flameCarnival_fire/fire_ctrl` (node 1): (0, 180, 0), false: the three flame jets (its children,
`ParticleEmitter`s with EmitterControl life 6) spin **half a turn a second** about the node's own y.

**The page part (about 15 lines).** `api.part("rotationControl", (fx, node, c) => ...)`: `useWorldRotation` false ->
each update `node.quaternion.multiply(Euler(dt x x, dt x y, dt x z, "YXZ" in radians))` (Unity's Rotate in self space:
`rotation = rotation x Euler(..)`; Unity Euler applies z, x, y = three's "YXZ"); true -> `node.quaternion = start x
Euler(dt x v)` with `start` the node's quaternion at build. Inside the mirror group the numbers are Unity's (no
conversion). Add `"rotationControl"` to `BUILT`.

### 6. Mole_timeNuke: the countdown label, detonate, explode (`fxparts/mole.js`; one extractor addition)

**What it does in BB (`Mole_timeNuke.cs`).**
- Fields (public, serialized): `mLv` (`:341`; 1 / 2 by prefab), `isVisible` (`:344`, ctor true `:30`), `timeNuke_explosion`
  (`:350`, the prefab, path id 386).
- `Init(owner)` (`:42-119`, `Mole.cs:11711`): the owner, the clock `start = Time.time` (`:56`), state 1 (`:59`), a GUIStyle:
  font `GameGui/Fonts/GMO24` (`:65`), text colour **(0.8, 0.3, 0.3, 1)** (`:68`), centred (`:71`); for an enemy:
  `isVisible = false`, every renderer off (`:80-111`).
- OnGUI (`:142-178`), while state 1 and `isVisible`: `v = Camera.main.WorldToScreenPoint(position + (0.2 mLv + 0.6) up)`
  (`:157`: 0.8 m / 1.0 m up), drawn only when `0 < v.z < 30` (`:160-168`: in front of the camera and nearer than 30 m),
  `GUI.depth 3`, `GUI.Label(Rect(v.x - 15, Screen.height - v.y - 15, 30, 30), floor(start + 60 - Time.time))` (`:175`): the
  seconds left, 60 for the first instant then 59, 58 ... in a 30 x 30 px box centred on that point.
- Update (`:191-287`): owner gone / dead -> Destroy; `start + 60 <= now + 1` -> state 2 (`:241-247`: the label goes at 59 s);
  `start + 60 <= now` -> state 3, `doExplode` (`:263-276`).
- `detonate()` (by `SendMessage("detonate")` from the Detonate skill, `Mole.cs:31102`, `:31148`; `:436-524`): when state 1:
  the seconds waited kept (`:478`), state 3 (`:481`), every renderer on (`:496-498`), `Yield(2, 0.5)` (`:523`), `doExplode`
  (`:451`).
- `doExplode()` (`:644-921`): `Instantiate(timeNuke_explosion, position, rotation)` (`:796`), its renderers off (`:801-828`),
  four damage waves 0.1 s apart (`:673`, `:921`), Destroy (`:911`): the nuke goes 0.4 s after the blast.
- The Detonate skill also puts `detonate` at each nuke (`Mole.cs:31125`, `:31171`, identity) at clip 0.6 (`Yield(2, 0.6)`,
  `:31458`), and refuses to start without a nuke ("Cannot find TimeNuke to detonate", `Mole.cs:6762`).

**The font.** GMO24 is a Unity bitmap font (rip `Resources/gamegui/fonts/GMO24.asset`: 16 x 16 grid, ascent 19, line 26.1;
its texture `Font Texture`, the glyph '0' 8 x 9 px of a 9 px advance). Extractor (lead, `wardrobe_fx.py`, about 25
lines): when a cued effect carries `Mole_timeNuke`, read the Font `GameGui/Fonts/GMO24` from the game data (mainData's
ResourceManager, as the prefabs), save its texture as `data/fx/tex/GMO24.webp` and the digits' `m_CharacterRects` ('0'-'9':
uv, vert, width) into `fx.json` as `"fonts": {"GMO24": {"tex": "GMO24", "ascent": 19, "chars": {...}}}`.

**The page part `Mole_timeNuke` (mole.js, about 45 lines).**
- Build: `mLv` from the comp; a `THREE.Sprite` (its own `CanvasTexture`, `sizeAttenuation: false`, `depthTest: false`,
  `renderOrder` high: the GUI is drawn over the scene) under the effect root at local `(0, 0.2 mLv + 0.6, 0)`, scaled to 30
  x 30 screen pixels each frame (the page's canvas height and camera fov); the canvas redrawn only when the number
  changes: the digits of `floor(60 - age)` blitted from GMO24 (data `fonts`) tinted (0.8, 0.3, 0.3); fallback (no font
  data) a bold sans 18 px in the same colour. **Centred by the measured ink**, not the box (CLAUDE.md "Thai text: centring
  by eye", NOTES.md: digits only here, no Thai marks, but the same rule: centre the glyphs' measured bounds in the 30 x 30
  box, as GUI's MiddleCenter puts the glyph box; check with a screenshot).
- Shown while `age < 59` and the camera's view depth of the point is in `(0, 30)`; hidden after `detonate()`.
- `detonate()` on the emitter (for `fx:detonate`, below): label off, meshes kept on, after 0.5 s explode.
- Explode (age 60, beyond the 10 s cut, or detonate + 0.5): `api.spawn("timeNuke_explosion", { x, y, d, rot })` at the
  nuke, its meshes hidden, `"destroy"` 0.4 s later. `"builds": ["timeNuke_explosion"]` on the Time Nuke / Detonate entries.
- `fx:detonate` (the Detonate skill's hero code): the `detonate` effect is spawned at each nuke (`Mole.cs:31125`), so the
  hook sits on that effect's root: `api.part("fx:detonate", fx => ...)`, at build, the living `timeNuke1` / `timeNuke2` Fx
  in `api.FX.live` nearest its root (within 0.5 m) gets `emitter.detonate()`; the cue puts `detonate` at the nuke's spot at
  clip 0.6 (`Yield(2, 0.6)`, `:31458`; the skills researcher places it).
- Add `"Mole_timeNuke"` to `BUILT`.

### 7. Mole_warCapital: `warCapital`'s clips (`fxparts/mole.js`); CharacterControl

**What it does (`Mole_warCapital.cs`).** No fields. Awake (`:24-55`): its own CharacterControl to standby. `InitWarCapital`
(SendMessage in the spawn frame, `Mole.cs:14451`; coroutine `:313-382`): layer = the owner's (`:363`), `animation.Play("open")`
Once (`:366-369`; the default clip, plays on spawn anyway), `Yield(2, 1)` (`:381`), then `Play("root")`, wrapMode Loop
(`:327-332`), operational (`:337`), the on-screen message "WarCapital is now operational." (`:342`: English, a game
message: left out). Update (`:75-169`): hp 0 -> `RPC_dead` (`close` Once, the missing `warCapital_dead`, `Yield 1`,
Destroy: `:545-646`). No EffectControl: it stands until it dies (the cue's `kill`, 10).
Clips (`fx_probe_sum.txt`): `open` 1.0 s Once, `root` 1.033 s Loop, `close` 1.0 s Once, on nodes 4-7 (the model's root,
base, launcher, flag).

**The page part `Mole_warCapital` (about 10 lines).** At age 1.0 `node.userData.fxAnim.play("root")` (mesh.js's
Animation on the root; the clip's own wrap 2 loops). `CharacterControl` stays NOT_DRAWN (`wardrobe_fx.py:201`); add
`"CharacterControl"` (NOT_DRAWN: "a summon's stats, nothing drawn") and `"Mole_warCapital"` to `BUILT`.
The volleys (`$OnWarCapital$24042`, `Mole.cs:43591-43930`: every 3 s, targets within 36 m, `RPC_warCapital_fire` (the
launch, `warCapital_fire` x N 0.15 s apart, `:44248`, `:44267`), 6 s later the `warMissile`s on random targets,
`:43760-43801`, `:43919-43927`) are cues on the War Capital tile, or a part if the planner wants them random: the skills
researcher's call; the missiles' flight is part 2.

### 8. Unity 3.5's ParticleSystem: `bazooka_ring`, `napalm_ring`, `warCapital` (`wardrobe_fx.py` graft, lead; `fxparts/shuriken.js` unchanged)

| system (node, BB transform) | what it is (`ps_sum.txt`; TTO's copy `tto_sum.txt` the same) | BB material (`ps_mats.txt`) |
|---|---|---|
| bazooka_ring `Particle System` (7) at (-0.25, 1, 1), identity: the muzzle | loop 5 s, **world** (BB `moveWithTransform` false = TTO 1), hemisphere radius 0.01, life 0.5-1, speed 3-4, size 0.5-1, rotation 0-2 pi, rate 0, **3 bursts of 12 at 0.9, 1.4, 1.7 s**, size 0.48 -> 1, colour fade, force (0, 1, 0) local, ClampVelocity magnitude 1 dampen 0.1 | `Cloud1` addsoft |
| napalm_ring `ParticleSystem` (1) at 0, -80 deg about x (rot (0.6428, 0, 0, -0.766)) | loop 5 s, local, cone 45 deg radius 0.2, life 0.5-1, speed 2-4, size 0.5-1, **one burst of 16 at 0**, size 0.47 -> 1, colour white -> red -> dark, force (0, -1, 0) world | `Bomb1_a` addsoft (texture Bomb1) |
| warCapital `ParticleSystem` (2) at (0, 0.2, 0), -90 deg about x | one shot 1 s, local, cone 81 deg radius 1.5, life 1, speed 0.5-1, size 1-1.5, **one burst of 32 at 0**: the dust ring as it lands | `Smoke1` addsoft (tint (0.56, 0.87, 1, 1): Additive (Soft) reads none) |

Why the graft and not BB's own: the Cat's part 6 (Unity 3.5's two-constant minimum as `minCurve` x `scalar`, `cnt0..3` /
`time0..3` bursts, the inverted `moveWithTransform`). Every module here is one `shuriken.js` reads (Initial, Shape types
2 and 4, Emission bursts, Size, Color, Force with `inWorldSpace`, ClampVelocity: `shuriken.js:243-258`, `:402`). The
Chameleon's route (`graft_shuriken`, `wardrobe_fx.py:470-557`, the branch at `:494`) puts TTO's two components on the BB
node itself with BB's material, so BB's node transforms above hold (the TTO copies' transforms are the same:
`tto_bbcopies.json`). After it: the inventory's NOTES gain the three lines the Bison / Cat / Chameleon have ("grafted from
TTO's copy ... drawn").

### 9. The chopper's engine sound (`fx:chopper`, `fxparts/mole.js`)

**What the hero's code does (`Mole.cs`, coroutine `$RPC_chopper$23799`).** At case 2 (clip 0.3, `Yield(2, 0.3)` `:34172`)
the chopper is made, parented to `Mole_tri/root/UpperBody1/UpperBody2/mount_Cannon`, local zero / identity
(`:33589-33604`); case 3 (0.5) `chopper_startDust` (`:33631`); case 4 (0.7) `moveSpeed 3` and
`mChopper.audio.Play()` (`:33658-33663`); case 5 (1.3) speed `5 + sLv`, Chopper Cannon's ring with #443 (`:33690-33719`);
ten 0.4 s steps of `chopper_forwardDust` and hits (`:33794-33946`, `Yield(6, 0.4)` `:34160`); then `audio.Stop()`
(`:33806`) and standby (5.3). The chopper's AudioSource: clip `chopper`, **playOnAwake off**, loop (`probe.txt`), so the
page (which starts only playOnAwake sources, `index.html:4073`) never plays it. EffectControl life 5.5, followState.

**The page part (about 12 lines).** `api.part("fx:chopper", fx => ...)`: at age 0.4 (clip 0.7 - 0.3) start the root's
AudioSource as audiocontrol.js does (`api.Sound.play(fx.cls, src.clip, src.volume, true)`, the handle put into a new
`fx.sounds` / `fx.loops` entry so Fx.dispose stops it), stop it at age 5.0 (clip 5.3) or at the cut. The cue: `[0.3, "fx",
"chopper", {"bone": "mount_Cannon", "cut": 5.3}]` (the skills researcher's times; `mount_Cannon` is in `data/mole/rig.json`).
The hero's flight (moveSpeed 3, then 5 + sLv) is the hero's, not an effect's (in place, the Wolf's Feral Strike rule).

### 10. The burrow hides the hero (a cue kind, `wardrobe/index.html`, lead)

`$RPC_cAttack1$23473` turns every Renderer under the Mole off while she is under ground (`Mole.cs:22031-22053`) and on
again when she surfaces (`:21583`, `:21951`). The page has `api.heroHide(key, on)` (index.html:4574) and the `hideProp`
cue kind (`HeroPropHide`, `:4761`, `:4980`) but no cue that hides the whole hero. Spec (about 12 lines, beside
`HeroPropHide`): a `"hideHero"` cue kind, `[t, "hideHero", "", {"kill": seconds}]`, a live object that calls
`heroHide(this, true)` at its start and `heroHide(this, false)` at its end / dispose (so a new pick never leaves her hidden,
the comment at `:4912`); `wardrobe_fx_check.py` OPTS learns the kind. Whether the Charge Attack tile shows the hidden
stretch is the attacks researcher's (`attacks_emotes.md`); the times are theirs.

### 11. The summons: Auto Gyro Gun, Barrel Bot, King Kaiser (question 6)

| summon | prefab (Mole.cs) | scripts (bytes) | clips the code plays | blocks |
|---|---|---|---|---|
| Auto Gyro Gun | `Robots/AutoGyroGun/AutoGyroGun1-4` by rank (`:11902-12031`; top 4), tPos, `LookRotation(tDir)`; life `chaAdjust(120)` (`:12235`) | `AutoGyroGun` 36 = `mChar` r, `mLv` i, `autoGyroGun_fire` r, `nAttack_fx` r, `create_fx` r (`AutoGyroGun.cs:1056-1089`); CharacterControl 684 | `create` (0.8 s) + create_fx, `Yield 0.8`, `root` Loop (`AutoGyroGun.cs:1710-1738`, `:1670-1675`); firing: `fire` Loop + `autoGyroGun_fire` every 0.1 s (`:1350-1477`) | layout; the fire prefab is only a field reference (no Resources path) |
| Barrel Bot | `Robots/BarrelBot/BarrelBot1-4` (`:12472-12601`; top 4) | `BarrelBot` 208 = `mChar`, 7 ints (`BarrelBotLv` ... `DrillLv`), `nAttack_fx`, 17 effect refs, `isCreate` b, `mCreator`, `mCreatorChar`, `create_fx` (`BarrelBot.cs:1958-2045`); `BarrelBotAI` 8 (`AI_state` string: needs an "s" type); CharacterControl | `root` / `run` cross-fades by its AI (`BarrelBot.cs:500-638`), attacks punch / hammer / chopper / missile / cannon / drill | layouts (a string reader) |
| King Kaiser | `Robots/KingKaiser/KingKaiser_<colour>` by `Skin / 100` (`:35709-35776`), tPos, `LookRotation(tDir)` (`:35794`); the Mole hidden inside ("hide" status, `:36135`) for `chaAdjust(240)` | `KingKaiser`, `KingKaiserAI`, CharacterControl | `run` / `root` (`KingKaiser.cs:369-507`), `punch`, `missile` ... | **its clips do not extract** (compressed / float curves, `probe_robots_kk.txt`); the hero hidden; the colour pick (effect_only.md P1) |

The Penguin built its Mana Vortex summon as a standing model with its own clips (`EXTRA_FOLDERS`, the ManaVortex part);
by analogy the first two are a folder line, layouts (or NOT_DRAWN), and a part each that plays `create` then `root`
(Auto Gyro Gun) / `root` (Barrel Bot), cut at 10 s. King Kaiser needs the clip reader first (the Unity 3.5 compressed /
float-curve AnimationClip format, a pipeline job of its own) and is the Mole's form change (the hero hidden, a mech the
player drives), closer to a hero skin than an effect.

### 12. Shaders and the rest: nothing to build

Read this first 2. Also checked (`allsum.py`): every Animation in the Mole's effects plays by itself (no `play` off);
effectRotationMode 1 (flameTurret, flameTurret_fire) without an owner does nothing (control.js, as the game); child
EffectControls with a velocity (warCapital_fire's rising missiles, (0, 0, -12)) are control.js's; `bunker_hole` / `dig_hole`
MeshColliders draw nothing. The worn cannon's own clips (`mWep1.animation.Play("fire")` / `"root"` / `"pose45"`,
`Mole.cs:505`, `:20243`, `:20520`, `:24666-24957`) are the weapon prop's, not an effect's (question 7).

## TTO: the released skills' parts (for the TTO researcher's `tto.md`; listed here so nothing is missed)

The released Mole TTO skills (`barrelRailgun1-4`, `kaiserArsenal`, `missilePad`) spawn 21 prefabs (`catalog_keys.txt`,
`tto_rel_sum.txt`). TTO's own Mole scripts (fields `TTO1102:dump.cs`, RVAs `methods.tsv`); the hero's code in
`pseudo/Mole.c` (`<RPC_barrelRailgun>d__418` :2754, `_fire` d__424 :3657, `_overload` d__429 :3955, `_end` d__430 :3403;
`SpawnMissilePad` :38266, `MissilePadLock` :38384, `DropMissilePad` :38478). **Kaiser Arsenal is the King Kaiser's skill**:
`KingKaiser.RPC_kaiserArsenal` @0x1cb1010, `_fire` @0x1cb0a60, `_hit` @0x1cb0ca0, `RollArsenal`, `ArsenalShot`,
`ArsenalWatch`, `NearestPod` (`dump.cs:110087-110101`); KingKaiser's code is not in `pseudo/` (no pseudo file for it):
it needs the King Kaiser summon on the page first (part 11).

| part | prefab(s) | what it is (`dump.cs` line, fields; RVAs) | build home |
|---|---|---|---|
| `MoleRailgun` | barrelRailgun (root), barrelRailgun_turret/Gun | `:108360`: glows[], coils[], channel, orb, muzzle, arcPrefab, glowColor, size; DrainTime 0.6; tier, orb scale, MaterialPropertyBlock tint; Awake@0x1c87120 SetTier@0x1c87850 Fire@0x1c87220 Grow@0x1c87250 Update@0x1c87890 Paint@0x1c87320 Arc@0x1c86e70 | `fxparts/tto_mole.js` |
| `MoleRailTurret` | barrelRailgun_turret | `:108447`: head, cradle, seat, gun, OnLock; KickBack 0.22, KickNod 7, KickTime 0.45, Timeline 6, Steps[] (part, from, to, offset, axis, spin, clank), BootCharge 5.62, BootFlash 5.85, CheckYaw 12; Assemble@0x1c84a40 Finish@0x1c859f0 Grow@0x1c85d40 Kick@0x1c85e60 LateUpdate@0x1c85e80 Yaw@0x1c86dc0/0x1c86e00 Muzzle@0x1c86bf0 | `tto_mole.js` + the hero's coroutine (`pseudo/Mole.c:2904-3019`) |
| `MoleRailBeam` | barrelRailgun_beam | `:108321`: core, glow, slug, arcPrefab, coreColor, glowColor, life, slugSpeed; Width[]; Shoot(a, b, tier)@0x1c83c10 Update@0x1c83ed0 Draw@0x1c83730 Place@0x1c83a80 | `tto_mole.js` |
| `MoleRailArc` | barrelRailgun_arc (a LineRenderer) | `:108285`: segments, jag, maxJag, flicker, life; Set@0x1c832b0 Follow@0x1c82cd0 Update@0x1c83430 Jag@0x1c82dc0 | `tto_mole.js` (LineRenderer: `tto_sheep.js`, built) |
| `MoleRailShock` | barrelRailgun_hit / _lock / _shock | arcPrefab, arcs, reachMin, reachMax, secondWave, pull; Start@0x1c84700 Update@0x1c849d0 Burst@0x1c84340 | `tto_mole.js` |
| `MoleLaunchPad` | missilePad | `:108217`: body, hatches[], rack, muzzles[]; RiseTime 0.45, Depth 0.8, OpenAt 0.42-0.6, HatchOpen 115, RackAt 0.52-0.72, RackLift 0.22, SinkTime 0.55, MaxLife 4, Locks[,]; Begin@0x1c81dc0 Sink@0x1c823d0 SinkIn@0x1c82390 NextMuzzle@0x1c81e10 Kick@0x1c81df0 Update@0x1c82450 Sample@0x1c81e50 | `tto_mole.js` + `SpawnMissilePad` / `DropMissilePad` |
| `MoleLockReticle` | missile_lock | `:108270`: pull; LateUpdate@0x1c82870 | `tto_mole.js` |
| `KaiserArsenalPod` | kaiserArsenalPod | `:109601`: ring, petals[], rack, fins[], muzzles[]; UnfoldTime 1.05, FoldTime 0.7, PetalOpen 42, RackSlide 0.75, RackTwist 60, FinFold 90, Locks[,]; Wear@0x1cad8c0 Unfold@0x1cad650 Fold@0x1cac920 Kick@0x1cac950 Update@0x1cad680 Pose@0x1cacb60 LockPoint@0x1cac9d0 | `tto_mole.js` (needs King Kaiser) |
| `KaiserWarhead` | kaiserWarhead (ProjectileControl + homing) | `:109657`: mTarget, arsenal; RelockRange 8, TurnEvery 0.15, TurnStep 0.4; Update@0x1cae4a0 OnTriggerEnter@0x1cae060 Land@0x1cadc40 NearestEnemy@0x1cadd80 | `tto_mole.js` (part 2's mover with its own numbers) |
| Shuriken (modes 0 / 1), GroundHugEmitter, LineRenderer, FlexibleCelShader/Cel No Outline, AdditiveAlpha | rail hit / lock / shock Sparks, recoil / launch Puffs, kaiserWarhead smoke; the blast / line / trench / overload rings; tto_BarrelBot, tto_KingKaiser_k, tto_warhead ... | built (`shuriken.js`, `groundhug.js`, `tto_sheep.js`, `tto_penguin.js`, `additivealpha.js`) | - |
| `barrelRailgun_rip`'s Animation (clip name only) | the drill rip | `wardrobe_fx_tto.py` warns "a MonoBehaviour reference () is written by name only" for several rail prefabs (`tto_released.err`): the arcPrefab references, to resolve to `barrelRailgun_arc` | `wardrobe_fx_tto.py` |
Blends (`tto_rel_sum.txt`): add 6 (`tto_rail*_add`, `tto_missileLock_add`), addsoft 13, alpha 1, multiply2 1, cel 5,
AdditiveAlpha 1: all drawn today.

## Interfaces (fixed up front, so the builders run in parallel)

1. **mole.js's movers** (parts 1-3) use only what exists: `fx.uQuat(node)`, `api.spawn(name, at)` + the entries' `builds`,
   `node.updateMatrixWorld(true)`; the target body is a constant in mole.js (Bat decision 4); `cat.js` exports
   `trajectoryVector` / `lookEuler` (import them: `import { lookEuler } from "./cat.js"`, or a shared `ballistics.js` if
   the lead prefers; one source).
2. **`fx:detonate` -> a living nuke's `emitter.detonate()`** (part 6): the nuke's Mole_timeNuke emitter exposes
   `detonate()`; the `detonate` effect's part finds the `timeNuke1` / `timeNuke2` Fx at its spot in `api.FX.live`.
3. **`"fonts"` in fx.json** (part 6): `{ <name>: { tex, ascent, chars: { "<char>": { uv: [x, y, w, h], vert: [x, y, w, h],
   width } } } }`, the texture in `data/fx/tex/`.
4. **`"hideHero"` cue kind** (part 10, lead, index.html): `[t, "hideHero", "", {"kill": s}]`.
5. **`SHURIKEN_FROM_TTO["mole"]`** (part 8, lead, `wardrobe_fx.py`; the Chameleon's no-SHURIKEN_MAT route).
6. **Existing, used as they are:** mesh.js's `fxAnim.play()` (warCapital, flameCarnival), audiocontrol.js's pattern for
   starting a playOnAwake-off source (chopper, flameCarnival), `fx.cutAt` / `api.FX.t`, the cue's `bone` / `rot` / `kill` /
   `cut` / `to`.

## Rank by value (effects unblocked / effort)

| rank | part | Mole effects it makes right | other classes | work |
|---|---|---|---|---|
| 1 | LAYOUTS (8 lines) | mine1-4, stunMine1-2, stunGrenade, missile_fire, warMissile, timeNuke1-2, flameCarnival_fire extract | Monkey (rotationControl) | 1 block |
| 2 | shell movers (part 1) | nAttack_fire, mortarShot_fire, stunGrenade, grenadeCluster_fire, napalm, bazooka_fire + their hits | 0 | ~70 lines |
| 3 | homing (part 2) | missile_fire, warMissile + hits | 0 (TTO's kaiserWarhead later) | ~40 lines |
| 4 | Shuriken graft entry (the Chameleon's route) | bazooka_ring, napalm_ring, warCapital puffs | - | 1 line |
| 5 | rotationControl | flameCarnival_fire | Monkey's lavu | ~15 lines |
| 6 | Mole_warCapital + fx:chopper | warCapital's idle loop, the chopper's engine | 0 | ~10 + ~12 lines |
| 7 | Mole_cartBomb | cartBomb_fire, cartBomb_hit | 0 | ~25 lines |
| 8 | Mole_timeNuke (+ font export, fx:detonate) | timeNuke1-2's countdown, Detonate | 0 | ~45 + ~25 + ~10 lines |
| 9 | hideHero cue kind | the burrow | any class that hides | ~12 lines |
| 10 | fx:flameCarnival (only if triggered) | the trap's open / close and its fire | 0 | ~15 lines |
| 11 | summons (Auto Gyro Gun, Barrel Bot; King Kaiser after the clip reader) | three skills' robots | Penguin-style | large |

After all: `BUILT` in `pipeline/wardrobe_fx_inventory.py` += `Mole_nAttack`, `Mole_mortarShot`, `Mole_stunGrenade`,
`Mole_grenadeCluster`, `Mole_napalm`, `Mole_bazooka`, `Mole_missile`, `Mole_warMissile`, `Mole_cartBomb`, `Mole_mine`,
`Mole_stunMine`, `Mole_flameCarnival`, `Mole_timeNuke`, `Mole_warCapital`, `rotationControl`, `CharacterControl`
(NOT_DRAWN); NOTES for the three grafted systems; run it again (the recipe's rule).

## Who builds what (never two owners for one file; as `plans/fx_wolf/build_rules.md`)

| agent | owns | builds |
|---|---|---|
| A: mole | `wardrobe/fxparts/mole.js` (new) | parts 1, 2, 3, 6 (page side), 7, 9, `fx:flameCarnival`, `fx:detonate` |
| B: generic | `wardrobe/fxparts/rotationcontrol.js` (new) | rotationControl |
| C: TTO (with the TTO researcher's report) | `wardrobe/fxparts/tto_mole.js` (new) | the TTO table |
| lead | `pipeline/wardrobe_fx.py`, `pipeline/wardrobe_fx_tto.py`, `wardrobe/index.html`, `pipeline/wardrobe_fx_inventory.py`, `pipeline/wardrobe_fx_check.py`, `wardrobe/fx_cues/mole.json` | LAYOUTS; `SHURIKEN_FROM_TTO["mole"]`; the GMO24 font export; the `hideHero` cue kind; `FX_PART_FILES += "mole", "rotationcontrol", "tto_mole"`; `BUILT` / NOTES; the summons' folders if decided; the rebuild and the cues |

A codes against Interfaces 1-3, so A, B and the lead run in parallel. Rules as before: `node --check`, no browser for the
builders, never `wardrobe_fx.py mole` without `--probe` (the lead rebuilds once).

## PASTE-READY (the parts' contract; the skills researchers' entries win where they differ)

Only the clip whose whole timeline this research walked (Chopper); the other part-bearing skills' entries are the skills
researchers', in the cue shapes of parts 1-7. For `wardrobe/fx_cues/mole.json` (today `{}`), checked JSON:

```json
  "chopper": {
    "why": "Mole.cs $RPC_chopper$23799 (:33450-34190), max rank sLv 3: at 0 the clip chopper Once (:34028-34031) and voice chopper1 | chopper2 (Random.Range(0, 2) :34069; :34079 / :34110, PlayOneShot :34169 / :34162); Yield(2, 0.3) (:34172); 0.3 the chopper (hero prefab field Mole_chopper, :19763) parented to mount_Cannon, local zero / identity (:33589-33604), its AudioSource chopper (playOnAwake off, loop) started at 0.7 by fx:chopper (:33663), EffectControl life 5.5 followState; Yield(3, 0.2) (:34167); 0.5 chopper_startDust at the hero, identity (:33631); Yield(4, 0.2) (:34157); 0.7 the sound; Yield(5, 0.6) (:34151); 1.3 choppperCannon_ring at the hero, hero rotation, Chopper Cannon #443 on (passives on; :33695-33719); then ten steps 0.4 s apart (Yield(6, 0.4) :34160): chopper_forwardDust at the hero, hero rotation (:33877) at 1.3 + 0.4 k, k 0-9; the hits (chopper_hit) are on enemies (:33929), left out; at 5.3 audio.Stop (:33806) and standby (:33829): the chopper's followState cut. The hero's own flight (moveSpeed 3 / 5 + sLv, :33658, :33690) is not drawn (in place)",
    "builds": [],
    "cues": [
    [0, "voice", "chopper1|chopper2"],
    [0.3, "fx", "chopper", {"bone": "mount_Cannon", "cut": 5.3}],
    [0.5, "fx", "chopper_startDust"],
    [1.3, "fx", "choppperCannon_ring"],
    [1.3, "fx", "chopper_forwardDust"], [1.7, "fx", "chopper_forwardDust"], [2.1, "fx", "chopper_forwardDust"],
    [2.5, "fx", "chopper_forwardDust"], [2.9, "fx", "chopper_forwardDust"], [3.3, "fx", "chopper_forwardDust"],
    [3.7, "fx", "chopper_forwardDust"], [4.1, "fx", "chopper_forwardDust"], [4.5, "fx", "chopper_forwardDust"],
    [4.9, "fx", "chopper_forwardDust"]
    ]
  }
```

(The `"cut"` is the cue option the Cat's / Bat's entries use for a followState end; the 5th-value form of the recipe
works the same. The chopper clip is 5.2 s; the coroutine's standby at 5.3 is after it.)

## How sure I am

| item | sure | why |
|---|---|---|
| The eight byte layouts | high | public fields in declaration order; 4 / 4 / 4 / 16 / 8 / 8 / 16 bytes decoded; TTO's copies name the same fields with the same values (`tto_sum.txt`; TTO's Mole_missile adds scatter / twin / pair, BB's 8 bytes hold only mTarget) |
| The shells' speeds, gravity, lives, hits | high | literals at the cited lines; Rigidbody flags from the prefab |
| The hit at the target body vs the floor | medium-high | Bat decision 4's body; Unity's trigger moment approximated by the box-overlap test |
| getMortarVector's lob (82.9 deg at 10 m) | high | `Math.cs:1011-1085`, guards worked; height difference ignored by the game itself |
| Homing (0.2 s, 0.3 rad, explode at life end) | high | literals; Update clock (frame-based, as the page) |
| Cart Bomb stops at 9.2 m | medium | Unity's solver between a Rigidbody capsule and a CharacterController; the 3 s fuse is certain |
| Time Nuke label (place, colour, 59 s, 30 m) | high | `Mole_timeNuke.cs:157-175`, `:241`; the pixel look of GMO24 needs the export |
| The three systems = TTO's copies | high | every field compared (`ps_sum.txt` / `tto_sum.txt`) |
| Chopper sound at clip 0.7, stop 5.3 | medium-high | the case numbers; the IL label -> Yield mapping (Block_43 / Block_32) read by order |
| The summons' layouts | medium | byte sums match (36, 208); BarrelBotAI's 8-byte string not decoded |

## Open questions (each with my recommended answer)

1. **The shells' hits: part-spawned or cued?** Recommended: **part-spawned** (`api.spawn` on contact, the entry's `builds`),
   as the Cat's Support Fire: the lob's 4 s flight and the trajectory shots stay in step with their blasts whatever pitch
   the cue gives.
2. **Mortar Shot and Napalm lob 83 deg up and fall for about 4 s at 10 m.** Keep the game's lob? Recommended: **yes** (the
   game's getMortarVector at the 10 m target point; the camera's fit takes the 30 m apex if it must: the Wolf's long skills
   pull back).
3. **Flame Carnival never fires on the page** (the 10 m target is outside its 4 m trigger). Show only the trap, or have the
   target step in? Recommended: **the trap only**, cut at 10 s (the game: nothing walks on it), with `fx:flameCarnival`
   built anyway for a later "trigger" option; the skills researcher may propose a SEQ that shows the fire (the effect-only
   rule) if the user wants the flames seen.
4. **Time Nuke's countdown label.** Draw it (60 ... 51 in the 10 s cut, the game's red-orange GMO24 digits over the nuke)?
   Recommended: **yes**, with the font exported (top quality); the Detonate tile shows a nuke first (the game refuses
   Detonate without one, `Mole.cs:6762`): a SEQ "timeNuke > detonate" the skills researcher shapes.
5. **Cart Bomb against the target.** Stop at the body (9.2 m) and wait for the 3 s fuse, as Unity's physics would?
   Recommended: **yes**.
6. **The summons (Auto Gyro Gun, Barrel Bot, King Kaiser).** Build them as standing robots (the Penguin's Mana Vortex rule)?
   Recommended: **Auto Gyro Gun and Barrel Bot yes** (create -> root, cut 10 s, no AI: no fire without the AI's target
   logic, or Auto Gyro Gun firing at the 10 m target if the skills researcher wants it); **King Kaiser as its own job** (the
   clip reader's compressed curves first, then a hero-hidden mech tile with the colour pick, effect_only.md P1, whose else
   branch summons nothing in BB: use `_r` for an unknown colour, as Fire Barrage's planes).
7. **The worn cannon's recoil clips** (`mWep1.animation.Play("fire")` on every shot). Out of the effects' scope?
   Recommended: **yes, out** here; offer it to the weapons work (the props' own Animation) as a separate item.
8. **Kaiser Arsenal** (released TTO) is King Kaiser's skill: wait for question 6's King Kaiser? Recommended: **yes**; the
   TTO researcher lists its parts, the build waits for the mech.
9. **War Capital's volleys.** Cue them at fixed times (every 3 s check, 6 s launch-to-impact) or a part with the game's
   random target offsets? Recommended: **cues** (one target, deterministic times), the warMissiles' `x` / `d` spread by the
   game's `vFlat(2 x insideUnitSphere)` written as a fixed pick per missile, flown by part 2.

## Verification

Checker, 13/11/2026, home PC, read only (`D:\12tails\DecompiledSource`, `DecompiledSource_TTO_2026-11-02`, this repo's
`pipeline/wardrobe_fx.py`, `wardrobe/index.html`, `wardrobe/fxparts/`, the researchers' probe outputs; my scripts and
outputs in `checks/fx_mole_research/verify_tp/`). Re-read and **confirmed**: the LAYOUTS block (every field public, in
declaration order, with the cited lines and types: `Mole_mine.cs:239`, `Mole_stunMine.cs:239`, `Mole_stunGrenade.cs:355`,
`Mole_timeNuke.cs:341 / 344 / 350` (the private `:347` between them is not serialized), `Mole_missile.cs:433`,
`Mole_warMissile.cs:345`, `rotationControl.cs:75-84`; the "b" type is 4 bytes in `wardrobe_fx.py`'s reader, so 16 / 16
bytes add up); the six shells' speeds (`Mole_nAttack.cs:28` 15, `Mole_mortarShot.cs:26` 20, `Mole_stunGrenade.cs:28` 15,
`Mole_grenadeCluster.cs:28` 6, `Mole_napalm.cs:26` 20, `Mole_bazooka.cs:28` 24), LookAt on all but the bazooka, the lives
(`Mole.cs:10089`, `:10780`, `:11307`, `:13749`, `:13819`, `:41361`, each x rangeMod), the hit RPCs and their rotations
(`:10105`, `:10830`, `:13865`, `:14036`, `:37769`; `Mole_stunGrenade.cs:193` is `RPC_nAttack_hit`), the Rigidbody gravity
flags and trigger boxes (`parts/probe.txt`); getMortarVector (`Math.cs:1011-1085`: g = Physics.gravity.y < 0, so f < 0,
82.9 deg, 4.05 s, 10.0 m at d 10, v 20); the homing missiles (`Mole_missile.cs:51-162`: 0.2 s, 0.3 rad, explode at life
`:118` / `:139`; `Mole_warMissile.cs:101`, `:143`; spawns `Mole.cs:13140`, `:13189`, `:14517`, `:14563`; hits `:13208`
the hero's rotation, `:14615`; prefab speeds 8 / 12 and warMissile's life 12, `probe.txt`); the cart (`Mole.cs:43088`,
`:43106`, `:43132`, `:43291`, `:43296`, `:43538-43544`; `Mole_cartBomb.cs:88-127`); the Time Nuke label (`Mole_timeNuke.cs:56`,
`:65-71`, `:157-175`, `:241`, `:263`, `:478-523`, `:673`, `:796`, `:911`); the Chopper paste block (`Mole.cs:33589-34172`:
every Yield, the voice pick, choppperCannon_ring with #443, the ten forward dusts, `audio.Stop` and standby; the prefab's
EffectControl 5.5 followState and its playOnAwake-off loop, `probe.txt:242-247`; the clip is 5.2 s, `data/mole/clips.json`;
`mount_Cannon` is in `rig.json`; the block parses); `SHURIKEN_FROM_TTO` / `SHURIKEN_MAT` / `graft_by_material` /
`NOT_DRAWN` / `EXTRA_FOLDERS` as described (`wardrobe_fx.py:186-205`, `:393`, `:494`, `:523-559`); the exporter keeps a
playOnAwake-off clip in `sounds` (`:419-424`), so `fx:chopper` has its file; `cat.js` exports `trajectoryVector` /
`lookEuler` (`fxparts/cat.js:29`, `:44`), `STEP = 0.02` in cat.js / bat.js; the inventory's `### mole` names none of the 13
prefabs of Read this first 5; every RVA and `dump.cs` line of the TTO table (`methods.tsv`).

**Corrections**

1. **Part 10 is built already: no `hideHero` cue kind.** Since the Chameleon (decision 49), the `hideProp` kind's slot
   `"hero"` hides the whole hero, her props and their weapon_fx particles, through `heroHide`, until its `kill`
   (`index.html:4600-4608`, `HeroPropHide` `:4885-4898`; used `fx_cues/chameleon.json:592`; `wardrobe_fx_check.py:22-24`
   knows it). The burrow's cue is `[t, "hideProp", "hero", {"kill": s}]`. Drop the new kind from part 10, Interfaces 4, Rank
   row 9 and the lead's list in "Who builds what".
2. **The TTO table misses Missile with Twin Warhead** (the released `missilePad` clip): its 21 prefabs (`tto_rel_sum.txt`)
   leave out `missileBot_fire`, `missileBot_fire_bot`, `missileBot_hit` and `twinImpact`, and include the never-spawned gun
   `barrelRailgun`: **24 prefabs** to build (`tto.md` section 5). Add the row **TTO's `Mole_missile`** (`dump.cs:108651`:
   mTarget, scatter, twin, pair; Awake / Update / OnTriggerEnter / TargetAlive / NearestEnemy `pseudo/Mole.c:43953-44610`,
   RVAs 0x1c9f960 / 0x1ca0660 / 0x1c9fdc0 / 0x1ca0560 / 0x1c9fa60; the relock within 8 m, the egg's split, `WarheadHit`;
   home `tto_mole.js`, `tto.md` P9), and the dump line of `MoleRailShock` (`:108406`). The blends line grows with them
   (`tto.md` section 5: multiply2 2, cel 6).
3. **KingKaiser's code is decompiled** ("TTO: the released skills' parts", `:469`): `pseudo_c6_extra/mole/KingKaiser.c`
   (7703 lines: `<RPC_kaiserArsenal>d__72` `:206-656`, SpawnPods `:7202-7377`, PodLock `:7381`, ArsenalShot `:7028-7071`), as
   `tto.md` Read this first 6 says; only `KaiserArsenalPod` and `MoleLockReticle` have no pseudo-C.
4. **Questions 6 and 8 go against the standing rules.** "Missing page parts are always built" and `kaiserArsenal` is in the
   released list (cues required): the recommended answers are to **build** the King Kaiser (the clip reader's compressed /
   float curves, then the summon) and Kaiser Arsenal's parts, not to wait; `tto.md` section 7 already writes the
   kaiserArsenal cues, which play on the Mole until the Kaiser stands (its question 4).
5. **Part 3, the cart's drive starts 0.2 s after the spawn**, not "from the spawn": the cart is made at clip 0.3 and the
   coroutine's `Yield(3, 0.2)` (`Mole.cs:43544`) comes before the FixedUpdate loop (`:43538`) that sets `velocity = 6 x dir`
   (`:43296`), as the part's own timeline says ("driving from 0.5"). The page part: still for age < 0.2, then 6 m/s; the
   boom at age 3 (the fuse counts from Init, the spawn frame) stays; at the body (9.2 m) about clip 1.95.
6. **Line refs moved** (today's `index.html`): `api.heroHide` is in the api at `:3886` / `:3958` (not `:4574`),
   `HeroPropHide` `:4885` (not `:4761`), the playOnAwake start `:4127` (not `:4073`), the parts' comment above
   `FX_PART_FILES` ends at `:3939` (not `:3845-3888`).

**Notes (no cue changes)**
- The Chopper's `cut` 5.3 is after the 5.2 s clip: with the page's default (skill once, then the idle tail, `skillLoop`
  off, `index.html:1438`) FX.t runs on and the cut comes; with the loop toggle on, the clip restarts at 5.2 and the cut is
  never reached (the EffectControl's 5.5 s ends it at clip 5.8, over the next round's chopper). Fine as written; a
  `"Chopper: chopper@5.3"` SEQ would make the loop match too.
- Part 1's cue shapes: `RPC_nAttack_fire` aims `getTrajectoryVector(firePos, firePos + fireDir, 15)` (`Mole.cs:10070-10089`)
  at the point `fireDir` reaches, `fireDir = tDir - fireOffset` (`:20423`): whether the shell lands on the 10 m point is
  the skills researchers' (their `rot`).

**Corrected paste-ready block set.** The LAYOUTS block, the two extractor lines and the Chopper entry are unchanged. Part
10's cue shape becomes `[t, "hideProp", "hero", {"kill": seconds}]` (no index.html change).
