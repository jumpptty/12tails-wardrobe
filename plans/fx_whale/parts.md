# Whale effects: the parts the page cannot draw yet (or draws wrongly)

Research 13/11/2026, office PC (one of the Whale fx researchers; scope: every part the Whale's effects need: all 61
prefabs in `heroes/whale/effects`, the components `wardrobe_fx.effect()` drops, the shaders, the hero code acting on its
effects, the summons, and the released TTO skill's prefabs). Models: `plans/fx_mole/parts.md`,
`plans/fx_chameleon/parts.md`. Read only: nothing in `wardrobe/data` was written; `wardrobe_fx.py` / `wardrobe_fx_tto.py`
ran with `--probe` only; no browser. BB lines are `C:\Users\Jump\Desktop\12tails\DecompiledSource\<file>` (the home PC's
`D:\12tails\...`); every opaque predicate worked by `annotate.py` (TRUE / FALSE, line numbers kept) and read by hand.
TTO is `TTO1102:` = `DecompiledSource_TTO_2026-11-02` (`dump.cs`, `methods.tsv`, `pseudo/Whale.c`, capstone of
`client/GameAssembly.dll`).

Probes (read only, outputs beside them) in `checks/fx_whale_research/parts/` (git-ignored, this PC only):
- `probe.py` -> `probe.txt`, `probe.json`: the 61 prefabs (66 Resources keys; 5 are the scripts' MonoScripts) through
  `wardrobe_fx.effect()`, a raw walk with every component, unknown scripts' field bytes, materials' blends. Last lines:
  `blends: addsoft 91, alpha 14, add 2, premul 1, opaque 1, shader:Particles/AdditiveOffset 1, multiply2 1,
  shader:FX/Phoenix 1`; `dropped: SphereCollider 3, Rigidbody 3, ParticleSystem 2, ParticleSystemRenderer 2, BoxCollider
  1`; `UNKNOWN scripts: Whale_flyingShield [0], Whale_homingShield [0], Whale_javelin [0], whale_kingdomKnight [8, 8],
  Whale_overPresence [0]`. **59 extract, 2 raise** (kingdomKnight1 / kingdomKnight2).
- `probe2.py` -> `probe2.json`: the blocked six with the LAYOUTS below in memory (the knights' clips, the flying shield's
  clip keys). `mats2.py`: the knights' materials. `fs_path.py` -> `fs_path.txt`: the Flying Shield's path against the
  target body. `javelin_aim.mjs` -> `javelin_aim.txt`: the Javelin's aim and flight (cat.js's `trajectoryVector`).
- `probe_ps.py` -> `probe_ps.json` (+ the stdout line): grandTide's two Unity 3.5 ParticleSystems, their BB materials, and
  what `whale_kingdomKnight.kingdomKnight_ring2` [16, 295] names. `graft_try.py` -> `graft_try.txt`: grandTide through
  `graft_shuriken` with `SHURIKEN_FROM_TTO["whale"]` set in memory.
- `tto_bbcopies.json` (+ `.err`): TTO's copies of flyingShield, homingShield, javelin, kingdomKnight2, overPresence,
  divingStorm (`wardrobe_fx_tto.py whale --probe`). `tto_probe.json` + `tto_summary.py` -> `tto_summary.txt`: the released
  skill's TTO prefabs and TTO's grandTide. `catalog_keys.py` -> `catalog_keys.txt` (706 whale keys).
  `disasm.py` -> `disasm_leviathan.txt`: capstone of WhaleLeviathan's and WhaleDolphin's methods. `blobscan.py`: a
  heuristic search of the metadata for WhaleLeviathan.KeyT.
- `src/*.txt`: the annotated sources (Whale, CharacterControl, the five Whale scripts, ProjectileControl, Math).

## Read this first

1. **Five Whale scripts; four need page code, one is data only; no shader to build.** The Whale is a small set:

   | effect | what blocks it | today |
   |---|---|---|
   | `kingdomKnight1`, `kingdomKnight2` (12th Kingdom Knight) | `whale_kingdomKnight` (8 bytes, `kingdomKnight_ring2`): a summoned shrimp knight in one of six slots round the Whale, rising from 1 m under the floor, its own clips (root, nAttack, cAttack, unsummon) | **not buildable** |
   | `javelin` (Javelin) | `Whale_javelin` (0 bytes): a copy of the worn lance thrown at 24 m/s under gravity, stuck in the floor | builds, **empty** (the lance copy is the script's) and stands still |
   | `flyingShield` (Flying Shield) | `Whale_flyingShield` (0 bytes): a copy of the worn shield on the clip-driven node; its 1 m trigger | builds, the 1 s loop flies **an empty node** |
   | `homingShield` (Homing Shield) | `Whale_homingShield` (0 bytes): a copy of the worn shield, spinning, homing 12 m/s on the target, a hit each pass | builds, **empty**, never moves, never ends (no EffectControl) |
   | `grandTide` (Grand Tide) | Unity 3.5's ParticleSystem x 2 (dropped); the hero's code plays its clips create -> root -> destroy | builds without its spray; stops on `create`'s last pose |
   | `castRing` (the cast channel) | the hero's code restarts its `root` clip 0.5 s after the spawn (`Whale.cs:20474-20479`); `fx:castRing` (bat.js) is gated to the Bat and the Chameleon | builds; `create` plays once and the ring freezes |
   | `overPresence` (Over Presence, passive) | `Whale_overPresence` (0 bytes): a 6 m trigger handing enemies a status; no renderer | builds; nothing to draw (data only) |

2. **Shaders: nothing to build.** BB: addsoft 91, alpha 14, add 2, premul 1 (`whale_dead`), opaque 1 (+ the knights'
   `shrimpKnight1/2`), multiply2 1 (`Smoke4` in seaAegis_ring), `shader:Particles/AdditiveOffset` 1 (nAttack_hit:
   `particles.js`), `shader:FX/Phoenix` 1 (seaAegis: `mesh.js`). TTO (the released Leviathan Breach + TTO's grandTide):
   alpha, add, addsoft only (`tto_summary.txt` "materials"). Every other component in the 61 is built (AlphaTimer + UVScroll
   on bowlingWhale_tri, VortexEmitter, EmblemEmitter on honor_cast, BoltEmitter on malstorm_bolt, AudioControl on
   bowlingWhale, TrailRenderer on the knights' lances, Animation / SkinnedMeshRenderer everywhere). No AudioSource has
   playOnAwake off; every Animation plays by itself.
3. **grandTide's two systems match TTO's copy field for field** (life 0.5 / 1, speed 2 / 6 with TTO's two-constant
   minimum 1 / 3, size 1 / 3 (min 0.5 / 2), rate 128 / 64, shape 5 = Box with TTO's scale (16, 3, 1) and angle 25, loop 5 s,
   world space (BB `moveWithTransform` false = TTO 1), force (0, -6, 0) world, Size and Color on; `probe_ps.json` against
   `tto_probe.json`). Both BB nodes are named `ParticleSystem`, but their materials differ (Water2, Splash3), so the
   Chameleon's by-material route matches them one to one: **one table line**, proved in memory (`graft_try.txt`: "grafted
   from TTO node 1 (material Water2)", "from TTO node 7 (material Splash3)"). `shuriken.js` reads shape 5 (`:200`).
4. **Three effects carry a copy of the worn weapon**, as the Chameleon's arrow (decision 50): Javelin copies `mWep2` (the
   lance), Flying Shield and Homing Shield copy `mWep1` (the shield). BB's `WhaleEquipment.cs:1640-1677`: mWep1 = the
   piece on `mount_Hand_L` (the shield), mWep2 = `mount_Hand_R` (the lance); the page's whale sets put the lance in slot
   **R** and the shield in slot **L** (`index.html:1647-1662`, item_map pairs [lance, shield]). `api.propModel(slot, true)`
   needs `PROP_STARTER.whale = { R: "noviceLance", L: "noviceShield" }` (`index.html:5230`: today only the Chameleon and the
   Monkey).
5. **The inventory misses 10 Whale prefabs** (loaded by CharacterControl or held in fields): `bubbleShield`, `salvation`,
   `heavy`, `honor_cast`, `shield`, `shieldReflect`, `rejuvenate_hit` (status looks and hit reactions,
   `CharacterControl.cs:35561-36040`, `:30920`, `:30989`, `:4595`, `:8910`), `kingdomKnight_ring2` (the knight's field),
   `overPresence` (the Whale prefab's field, `Whale.cs:15579`, made at Start `:92`), and `divingStorm` (**never loaded in
   BB**: only the hero clip `Animations/divingStorm`, `Whale.cs:1445`, `:32781`). All of them extract and use built parts
   (`probe.txt`); none needs a part. Two names the code loads have **no BB prefab**: `javelin_hit` (`Whale.cs:8835-8848`,
   and `RPC_javelin_hit` is never called) and `bowlingWhale_hit` (`:10499-10527`, at the enemy anyway).
6. **The released TTO skill (Leviathan Breach, clip `leviathanCall`) needs two TTO parts:** `WhaleLeviathan`
   (`tto/leviathanBreach`: a 55-node leviathan whose body, tail and fins the code poses along a key path, no clip) and
   `WhaleDolphin` (`tto/leviathanBreach_dolphin`: dolphins hopping along a lane). Everything else in those prefabs is built
   (GroundHugEmitter 26, ImageEmitter 9, Shuriken 22, TrailRendererModern 6, UVScroll 2, SkinnedMeshRenderer 4). `clap`
   and `wai` are BaseHero emotes (`pseudo/BaseHero.c:1945-1948`): no effect, no part.
7. **Game quirks (offer to the user for the Bible; none changes a cue).** Listed in "Offers for the Bible".

## The Whale's blocked set

"Where" is where BB spawns it (the cue's shape). The clip times and tiles are the skills researchers'; the paste-ready
block below has the four whole timelines this research walked.

| effect | skill (spawn) | missing part(s) | where |
|---|---|---|---|
| `javelin` | Javelin (`$RPC_javelin$28609` `Whale.cs:22728-23360`; `RPC_javelin_fire` `:8760-8800`) | Whale_javelin: the lance copy, the throw, the stick | hero + TransformDirection(1.2, 2.2, 1), `LookRotation(getTrajectoryVector(.., target centre, 24))`, life 3 |
| `flyingShield` (+ `flyingShield_hit`) | Flying Shield (`$RPC_flyingShield$28671` `:24642-25190`) | Whale_flyingShield: the shield copy, the trigger | hero, hero rotation x `Euler(270, 90, 0)` (`:24807`) |
| `homingShield` (+ `flyingShield_hit`) | Homing Shield (`$RPC_homingShield$28927` `:35040-35440`; `RPC_homingShield_fire` `:10371-10431`) | Whale_homingShield: the copy, the homing flight, the passes, the life | hero + TransformDirection(0, 1, 1), hero forward, target, life chaAdjust(3) |
| `kingdomKnight2` x 6 (+ `kingdomKnight_ring2`) | 12th Kingdom Knight (`$RPC_kingdomKnight$28772` `:28262-28850`) | LAYOUTS; whale_kingdomKnight: slot, rise, follow, clips, unsummon; Round Table's guard; the volley (unused) | hero + TransformDirection(slot) - up |
| `grandTide` | Grand Tide (`$RPC_grandTide$28979` `:37257-37990`) | Shuriken graft (one line); `fx:grandTide` (root at 1 s, the release) | hero, hero rotation, followState |
| `castRing` | every cast-time skill (`$RPC_cast1` `:20380-21385`) | `fx:castRing` for the Whale (bat.js, one word) | hero, `Euler(270, 90, 0)` world-absolute (`:20421`) |
| `overPresence` | Over Presence #313 (Start `:86-92`, `createOverPresence` `:9903-9952`) | none (data only: BUILT) | parented to the hero |
| `tto/leviathanBreach`, `tto/leviathanBreach_dolphin` | Leviathan Breach (TTO) | WhaleLeviathan, WhaleDolphin | the TTO researcher's (`tto.md`) |

## LAYOUTS (paste into `pipeline/wardrobe_fx.py`, after the Monkey's block)

```python
# the Whale's parts (plans/fx_whale/parts.md, 2026-11-13; checks/fx_whale_research/parts/probe.txt: each instance's bytes are
# the listed fields exactly; TTO's re-serialised copies name the same one field, checks/fx_whale_research/parts/
# tto_bbcopies.json); the other four Whale scripts keep every field private (0 field bytes)
LAYOUTS.update({
    # whale_kingdomKnight.cs:312 (8 bytes: [16, 295] = sharedassets4's kingdomKnight_ring2, the Resources prefab itself,
    # probe_ps.py; Init spawns it at the knight's slot, :126-132): kingdomKnight1 / kingdomKnight2
    "whale_kingdomKnight": [("kingdomKnight_ring2", "r")],
    # Whale_flyingShield.cs:244-256, Whale_homingShield.cs:491-518, Whale_javelin.cs:349-373, Whale_overPresence.cs:208-217
    "Whale_flyingShield": [], "Whale_homingShield": [], "Whale_javelin": [], "Whale_overPresence": [],
})
```

One more extractor line (page_pipeline, `wardrobe_fx.py:333`): `"whale": ["grandTide"]` in `SHURIKEN_FROM_TTO`, with the
comment "the Whale's (2026-11-13, plans/fx_whale/parts.md Read this first 3): BB Water2 / Splash3 -> TTO tto_Water2 /
tto_Splash3 on the two "ParticleSystem" nodes, one match each by material, the Chameleon's route", and **no**
`SHURIKEN_MAT` entry. (At home only: the office has TTO's bundles too, `graft_try.txt` ran here.)

## Each part

Page parts plug in as the comment above `FX_PART_FILES` says (`wardrobe/index.html:3979-4060`):
`wardrobe/fxparts/<file>.js` default-exports `register(api)` and calls `api.part(type, build)`; `build(fx, node, comp, mat,
nodeDef, data)` returns `{ node, update(dt, cam) ("destroy" removes the node), stop?(), dispose?() }` or null;
`"fx:<effect>"` is built once on the effect's root (comp null); `api.spawn(name, at)` makes an effect a script
instantiates (the entry's `"builds"` puts it in fx.json); `api.propModel(slot, fallback)` a fresh copy of a worn prop
(Unity space, root at 0 / identity, null while loading: ask again next frame); `fx.cutNow()` is followState's end (the
`destroy` clip, the after-life; `index.html:4315`). Space: the effect's mirror group = Unity's world, the hero's feet at
the origin, +z her facing, +x her right, y 0 the floor. The target body (Bat decision 4): a cylinder at (0, 0.6, 10),
height 1, radius 0.3 (box x +-0.3, y 0.1..1.1, z 9.7..10.3). `STEP = 0.02`, gravity -9.8, `lookEuler` from `cat.js`.

### 1. Whale_javelin: `javelin` (`fxparts/whale.js`, new)

**What it does in BB (`Whale_javelin.cs`).**
- ctor: a private local velocity (0, 0, 24) (`:25`). Awake (`:37-55`): layer 1, ProjectileControl kept,
  `rigidbody.velocity = TransformDirection(v)` (`:50`) along the spawn rotation.
- Init(owner, lv) (`:62-122`, called in the spawn frame, `Whale.cs:8781-8800`): `Instantiate(owner.mWep2, zero,
  identity)`, parented to the javelin, local zero / identity (`:82-91`), every Renderer under it on (`:94-108`).
- FixedUpdate (`:140-180`): `clock += dt` (`:147`); at `ProjectileControl.life` Destroy (`:150-154`; life `3 x rangeMod`,
  `Whale.cs:8796`); not stuck: `LookAt(position + velocity)` (`:165`); stuck: `velocity = Lerp(velocity, 0, 24 dt)`
  (`:174`: x 0.52 a step, about 4 % of a step's travel further in all, ~1 m at 24 m/s).
- OnTriggerEnter (`:186-205`): a collider on **layer 0** (the terrain) -> stuck, `useGravity = false`. OnTriggerStay
  (`:210-325`): damage only, every 0.1 s, while not stuck (it pierces; no effect, no destroy).
- Physics (`probe.txt:167`): Rigidbody gravity **on**, rotation frozen (112); trigger box 0.25 x 0.25 x **3**, centre z 0.5
  (from 1 m behind the node to 2 m ahead). AudioSource `javelin`, playOnAwake (built).

**The page part (whale.js, about 45 lines).**
- Build: `vel = (0, 0, 24) x fx.uQuat(node)`; the copy `api.propModel("R", true)` under the node at 0 / identity (retry each
  frame while null); its meshes visible.
- Each 0.02 s step: `t += STEP`; `t >= 3` -> `"destroy"`; not stuck: `vel.y -= 9.8 STEP` then `p += vel STEP`, the node's
  rotation `LookRotation(vel)`; the floor test: the box's lowest point (both ends at -1 / +2 m along the heading, minus
  0.125 x the heading's horizontal part) `<= 0` -> stuck; stuck: `vel *= 1 - 24 STEP` (Lerp), `p += vel STEP`, rotation
  kept. The target body is a trigger the javelin passes (`OnTriggerStay`, no effect): no test needed.
- On the page (`javelin_aim.txt`): from (1.2, 2.2, 1) with rot [2.88, -7.59, 0] it crosses the body at 0.38 s (y 1.0) and
  meets the floor at 0.46 s, 11.9 m ahead, pitched 13 deg down, then slides ~1 m in, and stands to 3 s.
- Add `"Whale_javelin"` to `BUILT` (`wardrobe_fx_inventory.py`).

### 2. Whale_flyingShield: `flyingShield` (`fxparts/whale.js`)

**What it does in BB.** The root (EffectControl life 1, Animation `flyingShield` 1 s, AudioSource `javelin`) is made with
`hero rotation x Euler(270, 90, 0)` (`Whale.cs:24807`, the prefab root's own (0.5, -0.5, -0.5, -0.5)); its clip moves the
child `flyingShield` (one track, `probe2.json`) on a 1 s loop: from the left hand (-0.76, 1.36, 0.91) out to (0.9, 1.36,
11.85) and back on the right (3.5, 1.36, 6.1), always 1.36 m up (`fs_path.txt`). On that child (`probe.txt:107`):
`Whale_flyingShield` + a trigger SphereCollider radius **1** + a Rigidbody (no gravity).
- Init(owner, lv) (`Whale_flyingShield.cs:37-110`, `Whale.cs:24840`): `Instantiate(mWep1, position, rotation)`, parented,
  local zero / identity (`:96-105`).
- OnTriggerEnter (`:126-215`): a Player / Enemy of another layer (not 2), on the owner's client:
  `RPC_flyingShield_hit(transform.position, transform.forward)` (`:199`) = `flyingShield_hit` at the shield,
  `LookRotation(forward)` (`Whale.cs:8955`), and the hit (`:210`). No destroy: each entry is a hit.

**The page part (about 25 lines).** Build: the copy `api.propModel("L", true)` under the node, 0 / identity. Each frame:
the node's Unity position (`fx.uMatrix(node)`); the sphere (r 1) against the target body's box (closest point within 1 m);
on the frame it enters: `api.spawn("flyingShield_hit", { x, y, d, rot: lookEuler(the node's forward) })`. **On the page it
never enters** (closest 1.48 m at 0.45 s, `fs_path.txt`): built for the rule, as the game's no-hit at this target. Add
`"Whale_flyingShield"` to `BUILT`.

### 3. Whale_homingShield: `homingShield` (`fxparts/whale.js`)

**What it does in BB (`Whale_homingShield.cs`).**
- Init(life, owner, target) (`:20-180`, `Whale.cs:10431`): end = now + life (`chaAdjust(3)` = 3 at CHA 1), the aim =
  the target's `collider.bounds.center` (`:55`, again each frame `:272`); `Instantiate(mWep1)` with every MeshRenderer on,
  parented at local 0, **local Euler(0, 0, 90)** (`:86-135`).
- Update (frame time, `:183-335`): past the end -> `RPC_homingShield_destroy` (draws nothing) and Destroy (`:231-249`);
  `a = RotateTowards(forward, aim - position, 4 dt, 1)` (`:278`); `rotation = LookRotation(Scale(a, (1, 0.2, 1)))` (`:281`:
  the climb flattened); `Translate(12 dt forward)` (`:284`); the copy `Rotate(1200 dt, 0, 0)` (self, `:324`).
- OnTriggerEnter (`:340-430`, root: SphereCollider r **0.5**, Rigidbody no gravity, `probe.txt:153`): a Player / Enemy of
  another layer: the hit, and when it lands (`hit() == 0`: CharacterControl.hit returns 0 on its paths,
  `CharacterControl.cs:3631-3670`) `RPC_flyingShield_hit(position, forward)` (`:409-418`). **It goes on**: it turns
  back (a 3 m turn radius at 12 m/s, 4 rad/s) and hits again on each pass.

**The page part (about 40 lines).** Aim: the cue's `to`, else the body's centre (0, 0.6, 10) (Penguin decision 3). On the
0.02 s step (the Mole editor's lesson: frame-time turns fly straight through a long first frame; at 50 fps the same
flight): life 3 -> `"destroy"`; RotateTowards by `4 STEP` rad (the angle between forward and the aim, `min(4 STEP, angle)`
about their cross axis), y x 0.2, renormalised, LookRotation; `p += 12 STEP forward`; the copy turns `1200 STEP` deg about
its local x. The sphere (r 0.5) against the body's box: on entry `api.spawn("flyingShield_hit", { x, y, d, rot:
lookEuler(forward) })`. `"builds": ["flyingShield_hit"]`. Add `"Whale_homingShield"` to `BUILT`.

### 4. whale_kingdomKnight: `kingdomKnight1`, `kingdomKnight2` (`fxparts/whale.js`)

**What it does in BB (`whale_kingdomKnight.cs`).** The root: Animation (`root` 1.0 s Loop, the default, plays by itself;
`nAttack` 1.2 s, `cAttack` 0.5 s, `unsummon` 1.0 s; `probe2.json`) + the script; `Shrimp_tri` (SkinnedMeshRenderer,
`shrimpKnight1` / `shrimpKnight2` opaque), `lance` (TrailRenderer, Line_Flat addsoft). No EffectControl.
- Init(owner, lv, slot) (`:23-150`, `Whale.cs:28506`): the slot offset (`:45-117`): 0 (1.6, 0, 1.6), 1 (-1.6, 0, 1.6), 2
  (1.6, 0, -1.6), 3 (-1.6, 0, -1.6), 4 (2.2, 0, 0), 5 (-2.2, 0, 0); `position = owner + TransformDirection(offset) - up`
  (`:120`: **1 m under the floor**), `rotation = owner's` (`:123`); `Instantiate(kingdomKnight_ring2, position + up,
  rotation)` (`:126-132`: on the floor at the slot); state standby (`:144`).
- Update (`:163-245`): owner gone -> Destroy (`:242`); standby: `position = Lerp(position, owner + TransformDirection
  (offset), 4 dt)`, `rotation = Lerp(rotation, owner's, 4 dt)` (`:229-234`: **it rises** to its slot and follows); with
  Round Table (#273) and the owner in `attack` / `cAttack1`: `knightGuard()` (`:202-220`).
- knightGuard (`:631-763`): wait `0.1 x slot` (`:761`); while the owner charges: `rotation = LookRotation(vFlat(
  Random.onUnitSphere))` (`:682`), `Play("cAttack")` Loop (`:687-692`), wait 0.5 (`:756`), again; then standby, `root`
  Loop (`:700-710`). No lerp while guarding.
- knightAttack(target) (`:409-524`, from `Whale.KingdomKnight()` every 3 s on `FindClosestTarget(the Whale, 8)`,
  `Whale.cs:9650-9729`, the volley RPC `:29062`): face the target flat (`:498`), `nAttack` Once (`:504`), 0.5 s, the hit
  (`:439`), 0.5 s, `root` Loop (`:454-469`). **Never on the page**: the target is 10 m from the Whale.
- unsummon (`:867-915`; `RPC_kingdomKnight_unsummon` `Whale.cs:9827-9868`, at the status's end and at a recast): `Play(
  "unsummon")` Once (`:902`), 1 s (`:913`), Destroy (`:881`). The status is `chaAdjust(60)` (`Whale.cs:28533`): cut at 10 s.
- Rank: `sLv == 1` -> kingdomKnight1, else kingdomKnight2 (`Whale.cs:28414-28480`); 2 + 2 sLv knights: the top rank is
  **six kingdomKnight2**.

**The page part (about 50 lines).** Options (fx.at): `slot` (0-5, required), `end` (age: the unsummon; the Monkey's word,
decision 30), `standing` (true: already out, at its slot on the floor from the start, no ring2: the Monkey's word,
decision 34), `guard` ([from, to] ages: Round Table's guard), `attack` ([ages]: knightAttack at the body; built, never
cued: Mole decision 26's unused `trigger`). Build: root local position `(ox, standing ? 0 : -1, oz)`, identity; not
standing: `api.spawn("kingdomKnight_ring2", { x: ox, y: 0, d: oz })`. Each frame in standby: `p.lerp(target, min(1, 4 dt))`
(Unity's frame lerp, as the game), the quaternion slerped to identity at the same rate. `guard`: from `from + 0.1 slot`
every 0.5 s a random flat yaw (uniform 0-360) and `fxAnim.play("cAttack", 0, 2)` (Animation.Play restarts it after a
rewind: `fxAnim.rewind()` first, the Cat's call), at `to` `play("root", 0, 2)`, standby again. `attack` at age a: yaw to the
body, `rewind(); play("nAttack", 0, 1)`, at a + 1.0 `play("root", 0, 2)`. `end`: `play("unsummon", 0, 1)`, `"destroy"` 1 s
later. `"builds": ["kingdomKnight_ring2"]`. Add `"whale_kingdomKnight"` to `BUILT`.

### 5. Unity 3.5's ParticleSystem: `grandTide` (`wardrobe_fx.py` graft, page_pipeline; `shuriken.js` unchanged)

Read this first 3. After it: the inventory's `NOTES` gain "grandTide: two ParticleSystems grafted from TTO's copy
(Water2, Splash3), drawn", as the Bison / Cat / Chameleon / Mole lines.

### 6. `fx:grandTide`: the hero's clips on the effect (`fxparts/whale.js`)

The hero's code: `Play("create")` Once at the spawn (`Whale.cs:37449-37454`; also the default clip), `Play("root")` Loop
1 s later (`:37509-37514`, after `Yield(3, 1)` `:37939`), `Play("destroy")` Once at the release (`:37706-37711`), when
myCommand leaves `grandTide` (the SEQ's grandTide0) and the followState after-life (1 s) begins. The page's cue `cut`
cannot cross the step edge (the effect is made in grandTide1, released after grandTide2's 3 s). **Part (about 12 lines):**
at age 1.0 `fxAnim.play("root", 0, 2)`; at age `release` (the cue option, seconds after the spawn) `fx.cutNow()` (the
`destroy` clip and the after-life: the game's end exactly); not after a cut or a stop. `release` is already an OPTS word
(the Chameleon's reticle), read per part.

### 7. `fx:castRing` for the Whale (`fxparts/bat.js:443`, one word)

`$RPC_cast1` makes castRing at 0.1 s (`Whale.cs:20409-20421`, after `Yield(2, 0.1)`), then `Yield(3, 0.5)` and
`Play("root")` Loop (`:20474-20479`): the same 0.5 s restart bat.js's hook makes for the Bat and the Chameleon. Change
`if (fx.cls !== "bat" && fx.cls !== "chameleon") return null;` to let `"whale"` through, and the comment above it
(`:439-441`) to name the Whale (`Whale.cs:20421`, `:20474-20479`).

### 8. Whale_overPresence: `overPresence` (data only)

`Whale_overPresence.cs`: Init(lv, owner) (`:21-50`); OnTriggerEnter / Exit (`:56-185`, its 6 m sphere): an enemy gets /
loses `overPresence` (`moveMod -0.1 x lv`, `CharacterControl.cs:35952-35957`; no look). No renderer: nothing to draw, no
cue. Add `"Whale_overPresence"` to `BUILT` ("data only: an aura's trigger").

### 9. Hero code acting on the Whale's effects (no new part; the cue options exist)

| effect | the code | the cue |
|---|---|---|
| flyingShield | worn shield's MeshRenderers off 0.5 -> 1.5 s (`Whale.cs:24857-24915`) | `hideProp L` kill 1 |
| javelin | worn lance's off 0.5 -> 1.0 s (`:22985-23100`) | `hideProp R` kill 0.5 |
| homingShield | `noShield` chaAdjust(3) hides the worn shield (`CharacterControl.cs:36060-36075`, removal `:16152-16180`) | `hideProp L` kill 3 |
| bubbleShield, salvation (status looks) | made at `collider.bounds.center`, parented to the hero, `localScale = Clamp(mChar.radius + 0.4, 0.5, 1.5)` (`CharacterControl.cs:35973-36040`); destroyed with the status (`:16085-16151`) | `y`, `scale`, `kill` (the skills researchers') |
| heavy | `InitEffectControl(the target)` (`:35928-35936`): rides the holder | at the holder |
| honor_cast | `position + 2 up`, identity (`:35561-35564`) | `y: 2` |
| megalodon | at the target, identity, `localScale 1.5` (`Whale.cs:34802-34813`) | `d: 10, scale: 1.5` |
| shield, shieldReflect | a hit taken in the charge: `+ TransformDirection(0, 1, 0.7)`, hero rotation (`CharacterControl.cs:30920`, `:30989`, `:4595`) | none on the page (no hit taken) |
| bowlingWhale | follows the hero (followPosition, followState, life 7; AlphaTimer / UVScroll / AudioControl built); the hero is not hidden (`$RPC_bowlingWhale$28962` has no Renderer line) | `kill` across the step edge |

## TTO: the released skill's parts (for the TTO researcher's `tto.md`; listed so nothing is missed)

Leviathan Breach (`whl_leviathanBreach5`, skill 454; clip `leviathanCall` 2.4 s, `data/whale/clips.json`): the cast
`<RPC_leviathanCast>d__302` @0x1edffb0 (`pseudo/Whale.c:10488-10825`: cast1, castRing with "root", grandTide_ring's
sound, `leviathanBreach_warn`), the breach `<RPC_leviathanBreach>d__303` @0x1edf630 (`:10155-10470`: Row6Begin
leviathanCall `:10260`, `leviathanCall_raise` `:10291`, LeviathanRise `:10297`, the color ramp iceRamp (camera, left out)
`:10335`, DolphinLeap `:10377-10378`, `leviathanCall_slam` `:10425`, sounds shieldBash_hit / whaleWave), `<LeviathanRise>
d__304` @0x1eceec0 (`:912-1053`: `WhaleLeviathan.Play(spot, dir)` `:1005`), `<DolphinLeap>d__308` @0x1ecd580 (`:43-135`),
`<LeviathanDamage>d__309` (`:171-879`, hits only). Prefabs (`catalog_keys.txt`, `tto_summary.txt`):
`leviathanBreach_warn` (EffectControl 8 + 0.3, GroundHug x 3, Shuriken), `leviathanCall_raise` (EffectControl 2,
followPosition / followState), `leviathanCall_slam` (0.8), `leviathanBreach` (55 nodes), `leviathanBreach_dolphin` (31),
and TTO's own `castRing` (Row6Spawn reads `Row6FxPath` + name, `dump.cs:124104`).

| part | prefab | what it is (`dump.cs` line, constants; RVAs) | build home |
|---|---|---|---|
| `WhaleLeviathan` | tto/leviathanBreach | `:124464`: BreachGeyserAt 0.5, CrashAt 2.2, PoolLife 5, Life 8; statics CrashPoint **(0, 0, 1.5)**, KeyPos **(0, -9, 0), (0, -5, 0), (0, 7.5, 0.6), (0, 9, 2), (0, 1.2, 3), (0, -2.6, 3.6), (0, -6.5, 4)** (both read from the `.cctor`'s element stores, `disasm_leviathan.txt:2-197`), KeyT / KeyPitch / KeyRoll (7 floats each, `RuntimeHelpers.InitializeArray` blobs: field handles 0x3809788 / 0x38044e0 / 0x3800000), TailBones; bones mBody, mModel, mHead, mTail[], mFinL/R + rests; children mGeyser / mTrail / mCrash / mPool (nodes 23 `geyser`, 15 `trail`, 36 `crash`, 49 `pool`) toggled; Renderer fade by MaterialPropertyBlock. Awake@0x1ef7450 Find@0x1ef8100 Child@0x1ef7cb0 Play(spot, dir)@0x1ef8b50 Update@0x1ef95d0 Pose(t)@0x1ef8de0 Flex(t)@0x1ef8190 Fade(t)@0x1ef7d70 CatmullRom@0x1ef7b30 | `fxparts/tto_whale.js` |
| `WhaleDolphin` | tto/leviathanBreach_dolphin | `:124415`: Hop 0.5, Sink 1.4, AfterLife 2.5, ArcMin 1.8, ArcMax 3.4, ArcPerMetre 0.45; mBody, mTail[], fins, mSplash, mTrail, mPoints, mSplashed. `Hops(len) = len >= 7 ? 3 : 2` (@0x1ef5af0, read); Lane(from, to, hops)@0x1ef5b10 Play(points)@0x1ef5c90 Update@0x1ef6f00 Fire(at, scale)@0x1ef5930 Pose(h)@0x1ef6430 Point(h)@0x1ef5f80 Awake@0x1ef5410 .cctor@0x1ef7270 (TailBones). The hero's statics: DolphinAt[], DolphinSide[] (Whale's `.cctor`), DolphinLaneGap 2.2, DolphinWidth 1.6 (`dump.cs:124125-124128`) | `fxparts/tto_whale.js` |
| GroundHugEmitter, ImageEmitter, Shuriken (sim 0 / 1), TrailRendererModern, UVScroll, SkinnedMeshRenderer, EffectControl | all five prefabs | built (`groundhug.js`, `shuriken.js`, `tto_sheep.js`, `uvscroll.js`, `mesh.js`, `control.js`) | - |
| `SKILL_FX["whale"]` | the five + TTO's castRing, the sounds grandTide_ring / shieldBash_hit / whaleWave if BB's rip lacks them | `wardrobe_fx_tto.py:76` | page_pipeline |

KeyT, a heuristic (`blobscan.py`, unverified): the metadata holds `[0, 0.4, 0.6, 1.3, 1.75, 2.2, 2.7]` at 0x63e9b4, which fits
KeyPos (y crosses 0 between 0.4 and 0.6 = BreachGeyserAt 0.5; between 1.75 and 2.2 = CrashAt 2.2). The builder (or the
TTO researcher) confirms it and finds KeyPitch / KeyRoll through the field-RVA table (`tools/defaults.py` reads the
metadata's default-value blobs) or from Pose@0x1ef8de0's use of them.

## Interfaces (fixed up front, so the builders run in parallel)

1. **whale.js's cue options (fx.at):** knights `slot` (0-5), `end` (age), `standing` (true), `guard` ([from, to] ages),
   `attack` ([ages]); grandTide `release` (age); homingShield `to` ([x, y, d], default the body's centre (0, 0.6, 10)).
   javelin / flyingShield take none (their spot and rot are the cue's). New OPTS words for `wardrobe_fx_check.py:215`:
   **`guard`, `attack`** (`slot`, `end`, `standing`, `release`, `to` are there already).
2. **`api.propModel("R" | "L", true)`** with `PROP_STARTER.whale = { R: "noviceLance", L: "noviceShield" }`
   (`index.html:5230`, page_pipeline): the lance for the javelin, the shield for both shields; the copy's weapon_fx come
   along (as the game's Instantiate of the worn piece).
3. **`api.spawn`** of `flyingShield_hit` (homingShield's entry builds it; flyingShield's does not: it never spawns there)
   and `kingdomKnight_ring2` (the 12th Kingdom Knight entry builds it).
4. **Constants in whale.js:** the target body (Bat decision 4), `STEP 0.02`, gravity -9.8; `import { lookEuler } from
   "./cat.js"` (one source, as mole.js).
5. **Existing, used as they are:** `fxAnim.play(name, fade, wrap)` / `rewind()` (mesh.js), `fx.cutNow()`, `fx.uQuat` /
   `fx.uMatrix`, the `hideProp` kind with slot R / L, bat.js's `fx:castRing` (one gate word).
6. **TTO:** `tto/leviathanBreach` spawned at the spot with `rot` = the breach direction (`Play(spot, dir)` = the cue's
   placement); `tto/leviathanBreach_dolphin` with options `from` / `to` ([x, y, d], the lane's ends), the part computing
   `Hops(|to - from|)` and `Lane(from, to, hops)` as the game (both OPTS words exist). The TTO researcher's tto.md fixes the
   times and spots; tto_whale.js reads only fx.at and its own comps.

## Rank by value (effects made right / effort)

| rank | part | Whale effects it makes right | work |
|---|---|---|---|
| 1 | LAYOUTS (2 lines) + graft (1 line) + bat.js gate (1 word) | kingdomKnight1-2 extract; grandTide's spray; castRing's root | 3 lines |
| 2 | whale_kingdomKnight | 12th Kingdom Knight's six knights (and Round Table's guard) | ~50 lines |
| 3 | Whale_homingShield | Homing Shield (+ its hits) | ~40 lines |
| 4 | Whale_javelin | Javelin | ~45 lines |
| 5 | Whale_flyingShield | Flying Shield's shield | ~25 lines |
| 6 | fx:grandTide | Grand Tide's root loop and its end | ~12 lines |
| 7 | WhaleLeviathan, WhaleDolphin | Leviathan Breach (TTO, released) | large (the key path from the disassembly) |

After all: `BUILT` in `pipeline/wardrobe_fx_inventory.py:23` += `Whale_flyingShield`, `Whale_homingShield`, `Whale_javelin`,
`whale_kingdomKnight`, `Whale_overPresence`; `NOTES` += grandTide's graft; run it again (the recipe's rule): the Whale
should read 50 / 51 ready (grandTide's grafted systems counted apart, as the Mole's three).

## Who builds what (never two owners for one file; as `plans/fx_wolf/build_rules.md`)

| agent | owns | builds |
|---|---|---|
| A: whale | `wardrobe/fxparts/whale.js` (new); `wardrobe/fxparts/bat.js` (the one gate word of part 7, nothing else) | parts 1-4, 6, 7 |
| B: tto_whale (with the TTO researcher's tto.md) | `wardrobe/fxparts/tto_whale.js` (new) | WhaleLeviathan, WhaleDolphin |
| page_pipeline | `wardrobe/index.html`, `pipeline/wardrobe_fx.py`, `pipeline/wardrobe_fx_tto.py`, `pipeline/wardrobe_fx_inventory.py`, `pipeline/wardrobe_fx_check.py` | LAYOUTS; `SHURIKEN_FROM_TTO["whale"]`; `PROP_STARTER.whale`; `FX_PART_FILES += "whale", "tto_whale"` (and its comment: the Whale's parts); the cue-format comment for `slot` / `end` / `standing` / `guard` / `attack` / `release` (kingdomKnight, grandTide); `SKILL_FX["whale"]`; `BUILT` / `NOTES`; OPTS += guard, attack |
| lead / editor | `wardrobe/fx_cues/whale.json` | the cues (the reports' corrected blocks), the rebuild, the gate |

A and B code against Interfaces 1-6, so all three run in parallel. Rules as before: `node --check`, no browser for the
builders, never `wardrobe_fx.py whale` / `wardrobe_fx_tto.py whale` without `--probe` (the lead rebuilds once), and
`grep -c $'\r$' wardrobe/index.html` = 0 after any edit of it. If another class's build runs at the same time, bat.js,
index.html and the pipeline files keep one owner across the classes.

## Paste-ready cue entries (the parts' contract; the skills researchers' entries win where they differ)

The four clips whose whole timelines this research walked, in the page's current format (`index.html:4738-4838`), for
`wardrobe/fx_cues/whale.json` (today `{}`); checked JSON (`checks/fx_whale_research/parts/paste.json`). The 12th Kingdom
Knight's key is a placeholder: it plays `cast3`, the Cast sequence's last clip too, so the skills researcher keys it (a
`cast3` pool member, or `@<its SEQ id>:cast3`).

```json
  "javelin": {
    "why": "Whale.cs $RPC_javelin$28609 (:22728-23360), max rank sLv 2: at 0 the clip javelin (0.2 fade, :23200) and voice javelin1 | javelin2 (Random.Range(0, 2) :23241; Voices/javelin1 :23251, javelin2 :23282; PlayOneShot :23336 / :23333); Yield(2, 0.4) (:23318), Yield(3, 0.1) (:23324): at 0.5 RPC_javelin_fire (:22967; :8781-8800: javelin Instantiated at firePos, LookRotation(fireDir), ProjectileControl life 3 x rangeMod, Whale_javelin.Init copies the worn lance mWep2, Whale_javelin.cs:82-108) at firePos = hero + TransformDirection(1.2, 2.2, 1) (:22919), fireDir = getTrajectoryVector(firePos, the target's collider centre, 24) (:22952) = the standard body's centre (0, 0.6, 10): rot [2.88, -7.59, 0] (checks/fx_whale_research/parts/javelin_aim.txt), and the worn lance's MeshRenderers off (:22985-23007); Yield(4, 0.1) (:23322), Yield(5, 0.4) (:23328): at 1.0 back on (:23088-23100) and standby (:23127). Whale_javelin (fxparts/whale.js) flies it: 24 m/s, gravity, through the body at 0.38 s (it pierces: OnTriggerStay damage only, no effect), into the floor at 0.46 s about 11.9 m ahead, stuck there to its 3 s life; javelin_hit (RPC_javelin_hit :8835) is never called and BB has no such prefab: left out",
    "cues": [
    [0, "voice", "javelin1|javelin2"],
    [0.5, "fx", "javelin", {"x": 1.2, "y": 2.2, "d": 1, "rot": [2.88, -7.59, 0]}],
    [0.5, "hideProp", "R", {"kill": 0.5}]
    ]
  },
  "flyingShield": {
    "why": "the clip flyingShield is Flying Shield's and Homing Shield's (Whale.cs:25014, :35302): one tile each (pool members)",
    "skills": {
      "flyingShield": {
        "why": "Whale.cs $RPC_flyingShield$28671 (:24642-25190), max rank sLv 2: at 0 the clip flyingShield (0.2 fade, :25014), voice flyingShield1 | flyingShield2 (Random.Range(0, 2) :25055; Voices/flyingShield1 :25065, flyingShield2 :25096; PlayOneShot :25138 / :25133); Yield(2, 0.5) (:25143): at 0.5 flyingShield by createEffect at the hero, hero rotation x Euler(270, 90, 0) (:24807; CharacterControl.cs:24191-24210), Whale_flyingShield.Init on its child flyingShield (:24820-24840: the worn shield mWep1 copied onto it, Whale_flyingShield.cs:96-105), the worn shield's MeshRenderers off (:24857-24879); EffectControl life 1 = its clip: a 1 s loop 1.36 m up from the left hand out to 11.85 m ahead and back on the right (checks/fx_whale_research/parts/fs_path.txt); Yield(3, 1) (:25145): at 1.5 back on (:24903-24915); Yield(4, 0.2) (:25131): 1.7 standby (:24944). Its 1 m trigger passes 1.48 m from the standard target body (0.45 s), so no flyingShield_hit (Whale_flyingShield.cs:199, Whale.cs:8955); the part would spawn one on contact",
        "cues": [
        [0, "voice", "flyingShield1|flyingShield2"],
        [0.5, "fx", "flyingShield", {"rot": [270, 90, 0]}],
        [0.5, "hideProp", "L", {"kill": 1}]
        ]
      },
      "homingShield": {
        "why": "Whale.cs $RPC_homingShield$28927 (:35040-35440), one rank: at 0 the clip flyingShield (0.2 fade, :35302), voice homingShield1 | homingShield2 (Random.Range(0, 2) :35343; Voices/homingShield1 :35353, homingShield2 :35384; PlayOneShot :35425 / :35418); Yield(2, 0.5) (:35428): at 0.5 RPC_homingShield_fire at hero + TransformDirection(0, 1, 1), hero forward, the target (:35194; :10380-10431: Instantiate, LookRotation(tDir), Whale_homingShield.Init(chaAdjust(3) = 3 s at CHA 1, owner, target): the worn shield copied at local Euler(0, 0, 90), Whale_homingShield.cs:82-135) and noShield for chaAdjust(3) (:35211; its apply turns the worn shield's MeshRenderers off, CharacterControl.cs:36060-36075, its removal on, :16152-16180); Yield(3, 0.7) (:35430): 1.2 standby (:35232). Whale_homingShield (fxparts/whale.js): 12 m/s, turning 4 rad/s to the body's centre (Penguin decision 3), its y flattened x 0.2, the copy spinning 1200 deg/s; every pass through the body: flyingShield_hit at it, LookRotation(its forward) (Whale_homingShield.cs:409-418, Whale.cs:8955); gone at 3 s (RPC_homingShield_destroy draws nothing)",
        "builds": ["flyingShield_hit"],
        "cues": [
        [0, "voice", "homingShield1|homingShield2"],
        [0.5, "fx", "homingShield", {"y": 1, "d": 1}],
        [0.5, "hideProp", "L", {"kill": 3}]
        ]
      }
    }
  },
  "@KingdomKnight:cast3": {
    "why": "Whale.cs $RPC_kingdomKnight$28772 (:28262-28850), max rank sLv 2: at 0 the clip cast3 (0.2 fade, :28640), voice kingdomKnight1 | kingdomKnight2 (Random.Range(0, 2) :28681; :28693 / :28724; PlayOneShot :28705 / :28736), kingdomKnight_ring1 by createEffect at the hero, hero rotation (:28755-28767), the old knights unsummoned (:28799); Yield(2, 0.5) (:28816): at 0.5 2 + 2 sLv = 6 knights (:28414), kingdomKnight2 for sLv 2 (:28468-28480), Init(owner, sLv, slot i) (:28506): each at hero + TransformDirection(slot) - up, slot 0-5 = (1.6, 0, 1.6), (-1.6, 0, 1.6), (1.6, 0, -1.6), (-1.6, 0, -1.6), (2.2, 0, 0), (-2.2, 0, 0) (whale_kingdomKnight.cs:45-120), kingdomKnight_ring2 at its slot on the floor (:126-132), rising to the slot (Lerp 4 / s, :229); the kingdomKnight status chaAdjust(60) (:28533-28538), cut at 10 s: end 10 = unsummon(), its clip unsummon then Destroy 1 s later (whale_kingdomKnight.cs:867-913, Whale.cs:9827-9868); Yield(3, 0.5) (:28820): 1.0 standby (:28570). No volley: KingdomKnight() picks FindClosestTarget(the Whale, 8) (Whale.cs:9729; the volley RPC :29062), the target is 10 m away",
    "builds": ["kingdomKnight_ring2"],
    "cues": [
    [0, "voice", "kingdomKnight1|kingdomKnight2"],
    [0, "fx", "kingdomKnight_ring1"],
    [0.5, "fx", "kingdomKnight2", {"slot": 0, "end": 10}],
    [0.5, "fx", "kingdomKnight2", {"slot": 1, "end": 10}],
    [0.5, "fx", "kingdomKnight2", {"slot": 2, "end": 10}],
    [0.5, "fx", "kingdomKnight2", {"slot": 3, "end": 10}],
    [0.5, "fx", "kingdomKnight2", {"slot": 4, "end": 10}],
    [0.5, "fx", "kingdomKnight2", {"slot": 5, "end": 10}]
    ]
  },
  "grandTide1": {
    "why": "Whale.cs $RPC_grandTide$28979 (:37257-37990), one rank: at 0 the clip grandTide1 (0.2 fade, :37781), voice grandTide1 | grandTide2 (Random.Range(0, 2) :37822; Voices/grandTide1 :37834, grandTide2 :37865; PlayOneShot :37846 / :37877), grandTide_ring by createEffect at the hero, hero rotation (:37896-37906); Yield(2, 1) (:37936): at 1.0 grandTide by createEffect at the hero, hero rotation (:37424-37436; EffectControl life 99, afterLife 1, followPosition, followState; its own looping AudioSource grandTide) and its Animation create, Once (:37449-37454); Yield(3, 1) (:37939): at 2.0 the clip grandTide2 looped (:37488-37493, the SEQ's next step) and the effect's root, looped (:37509-37514: fx:grandTide at age 1); then each FixedUpdate while myCommand is grandTide and MP >= 10, SP >= 20 (:37589-37622); the release (the SEQ's grandTide0 at 2 + 3 = 5 s) plays destroy (:37706-37711) and the followState after-life (1 s): release 4 (age) = fx.cutNow(); ParticleSystem x 2 grafted from TTO's copy (Water2, Splash3)",
    "cues": [
    [0, "voice", "grandTide1|grandTide2"],
    [0, "fx", "grandTide_ring"],
    [1, "fx", "grandTide", {"release": 4}]
    ]
  }
```

Cue shapes for the others the parts touch: Round Table on a Charge Attack tile (question 3): `[0, "fx", "kingdomKnight2",
{"slot": k, "standing": true, "guard": [0, T], "kill": T + 0.5}]` k 0-5, T the charge's end. The cast channel's castRing
keeps the Bat's / Chameleon's shape (`{"rot": [270, 90, 0], "cut": <the step edge - 0.05>}`, spawn 0.1).

## How sure I am

| item | sure | why |
|---|---|---|
| The LAYOUTS | high | 8 / 0 / 0 / 0 / 0 bytes decoded; [16, 295] resolves to the Resources kingdomKnight_ring2 (`probe_ps.py`); TTO's copies name the one field (`tto_bbcopies.json`) |
| The graft | high | proved in memory (`graft_try.txt`); fields compared |
| Javelin's flight | high (the throw), medium (the stick) | literals at the cited lines; the 1 m slide after the stick is the Lerp's sum; where Unity's trigger first meets the floor is approximated by the box's lowest point |
| Flying Shield's loop and its miss | high | the clip's own Hermite keys, the root's Euler(270, 90, 0) (`:24807`) = the prefab's rotation; the 1.48 m gap |
| Homing Shield's passes | high (the numbers), medium (the hit moments) | literals; the step clock instead of frame time (a judgement, Mole editor) |
| The knights (slots, rise, follow, clips, unsummon, guard) | high | the script read whole; the clips from the prefab |
| No knight volley at 10 m | high | `FindClosestTarget(.., 8)` at `Whale.cs:9729` |
| fx:grandTide / castRing times | high | case order traced (`Yield(2, 1)`, `Yield(3, 1)`; `Yield(2, 0.1)`, `Yield(3, 0.5)`) |
| TTO's KeyPos / CrashPoint / Hops | high | read from the disassembly |
| TTO's KeyT | low | a metadata pattern match only |

## Open questions (each with my recommended answer)

1. **Flying Shield never hits the 10 m target** (its loop passes 1.48 m from the body). Show it as the game, or move the
   hit? Recommended: **as the game** (no hit at this target; the part's trigger stays for the rule), as the Mole's Flame
   Carnival (parts Q3, decision 26).
2. **The knights' volley** (`KingdomKnight()`, every 3 s on the nearest enemy within 8 m of the Whale) never fires at 10 m.
   Recommended: **no volley cued**; `attack` built and unused (Mole decision 26).
3. **Round Table** (#273, passives on) shows only with knights out. Show six standing knights guarding on the Charge Attack
   tile? Recommended: **yes, on the tile that shows Round Table** (the precondition shown: Mole decision 27, Monkey
   decision 34), with `standing` + `guard` over the charge; the attacks researcher places it.
4. **Grand Tide's end crosses the step edge.** Recommended: the part option `release` (age) calling `fx.cutNow()`, so the
   `destroy` clip and the 1 s after-life play as in the game (a `kill` would cut them off).
5. **Nothing worn in a hand**: the copies use the starter piece (`noviceLance` / `noviceShield`, Chameleon decision 50).
   Recommended: **yes** (the game always holds a weapon).
6. **Homing Shield on the 0.02 s step** rather than frame time. Recommended: **the step** (the Mole editor's fix for
   Mole_missile / KaiserWarhead: the same flight at 50 fps, safe on long frames).
7. **TTO's KeyT / KeyPitch / KeyRoll** are metadata blobs. Recommended: the TTO researcher or builder B decodes them
   (field-RVA table, or Pose's disassembly) before building WhaleLeviathan; the KeyT candidate above is a starting point,
   not a source.
8. **bubbleShield / salvation's size** (`Clamp(mChar.radius + 0.4, 0.5, 1.5)`): `mChar.radius` is CharacterControl's own
   field, not the prefab's CharacterController (radius 0.8, rip `Whale.prefab:640-655`). Recommended: the skills researcher reads
   the Whale's `radius` from the hero data (or `Game.cs:2805`'s `0.6 + 0.05 n` if that is the one) before cueing `scale`.

## Offers for the Bible (never written there; the user decides)

- **Flying Shield's path** (the reference: "no code in the class (prefab/animation)"): a 1 s loop 1.36 m up, from the left
  hand out to 11.85 m ahead and back on the right side, about 7 m wide (the root turned `Euler(270, 90, 0)`, `Whale.cs:24807`,
  the clip's keys); its trigger is a 1 m sphere, so an enemy standing inside the loop (for example 10 m ahead, at the
  centre of the line) is missed; one hit per entry, outward or back.
- **Homing Shield keeps flying after a hit**: no destroy on contact; it turns back at 4 rad/s (a 3 m turn at 12 m/s), its
  climb flattened to a fifth, and hits again each pass until its `chaAdjust(3)` life (`Whale_homingShield.cs:278-284`,
  `:409-418`); the flying copy spins 1200 deg/s; the worn shield is hidden for `noShield`'s duration.
- **Javelin sticks in the ground**: touching the terrain stops its gravity and brakes it to rest in a few frames; it stays
  to its 3 s life, harmless once stuck (`Whale_javelin.cs:174`, `:186-205`, `:219`). The thrown javelin is a copy of the
  worn lance (the hand's lance is hidden 0.5 s).
- **12th Kingdom Knight's knights** rise from 1 m under the ground to slots (+-1.6, +-1.6) and (+-2.2, 0) round the Whale
  (`whale_kingdomKnight.cs:45-120`, `:229`); rank 1 summons the kingdomKnight1 look, rank 2 kingdomKnight2; under Round
  Table each knight waits 0.1 s x its slot, then spins to a random facing every 0.5 s (`:682-761`).
- **Missing prefabs in BB**: `javelin_hit` (and `RPC_javelin_hit` is never called) and `bowlingWhale_hit` ("Cannot find
  bowlingWhale_hit Effect" on every hit); the `divingStorm` effect prefab is never loaded (only its clip is), and the hero
  field `Whale_shield_hit` is never read (`Whale.cs:15342`).

## Verification (13/11/2026, checker)

Read-only re-derivation on the office PC: BB `DecompiledSource/Whale.cs` (the coroutines' Yields, loads and spawns),
`Whale_javelin.cs`, `Whale_homingShield.cs`, `whale_kingdomKnight.cs`, `WhaleEquipment.cs`, `CharacterControl.cs`,
`EffectControl.cs`, `Math.cs`; TTO1102 `pseudo/Whale.c` and the TTO researcher's Ghidra output
(`checks/fx_whale_research/tto/annot/`); BB's rip; this report's own probes. New probes in
`checks/fx_whale_research/verify/`: `blocks.py` -> `blocks.txt`, `tto_castring.json`. This section wins over the body.

**Confirmed** (no change): Javelin `$RPC_javelin$28609`: clip at 0 (0.2 fade, :23200), voice javelin1 | javelin2
(Random.Range(0, 2), :23241-23282), Yield(2, 0.4) + Yield(3, 0.1) = 0.5 fire at hero + TransformDirection(1.2, 2.2, 1)
(:22919) toward the target's `collider.bounds.center` at 24 m/s (:22952), the lance's renderers off (:23007), Yield(4,
0.1) + Yield(5, 0.4) = 1.0 on (:23100): hideProp R kill 0.5; the aim rot [2.88, -7.59, 0] is cat.js's
`trajectoryVector` port of `Math.getTrajectoryVector` (Math.cs:885); Whale_javelin's velocity, LookAt, the Lerp(24 dt)
brake, the layer-0 stick (`Whale_javelin.cs:50, 165, 174, 191-198`). Flying Shield: rot hero x Euler(270, 90, 0)
(:24807), Yield(2, 0.5) / (3, 1) / (4, 0.2) = 0.5 / 1.5 / 1.7, voices :25065 / :25096. Homing Shield: fire at hero +
TransformDirection(0, 1, 1), hero forward (:35194), noShield chaAdjust(3) (:35211) = 3 s at CHA 1, Yield 0.5 / 0.7;
`Whale_homingShield.cs:55, 135, 272-284, 324` (the aim, Euler(0, 0, 90), RotateTowards 4 dt, the 0.2 flattening, 12 m/s
Translate, the 1200 deg/s spin). 12th Kingdom Knight: `2 + 2 sLv` knights (:28414), kingdomKnight1 for sLv 1 else 2
(:28433, :28468), chaAdjust(60) (:28527), ring1 at 0 (:28755-28767), Yield 0.5 / 0.5; the six slots, `- up`, ring2 at
`+ up`, the 4 dt lerps, the guard and unsummon clips (`whale_kingdomKnight.cs:54-132, 229-234, 682-761, 902-913`).
Grand Tide: clip and voices at 0, grandTide_ring at 0 (:37896-37906), Yield(2, 1): grandTide + `create` (:37424-37454),
Yield(3, 1): grandTide2 cut-in and `root` Loop (:37488-37514), `destroy` at the release (:37706); with the page's
`grandTide1 grandTide2*@3 grandTide0` (index.html:1370) the release is at 5.0 = age 4. BB's cast: castRing at 0.1
(Yield(2, 0.1) :21357, spawn :20421, world Euler(270, 90, 0)) and `root` Loop at 0.6 (Yield(3, 0.5) :21381, :20474-20479):
bat.js's 0.5 s hook fits the Whale. `mWep1` = the `mount_Hand_L` piece, `mWep2` = `mount_Hand_R` (`WhaleEquipment.cs:1645,
1677, 1707-1710`); the page's starters `noviceLance` / `noviceShield` exist (`data/whale/props_weapons.json`). Every
effect, voice and `builds` name in the block is in BB's rip; the block parses (wrapped in braces) with 4 keys and 20 cues,
every option in `OPTS` (`blocks.txt`); `PROP_STARTER` (index.html:5230), `fx.cutNow` (:4315), `uMatrix` / `uQuat`
(:4318-4319), mesh.js's `play(name, fade, wrap)` / `rewind()`, cat.js's exported `trajectoryVector` / `lookEuler`,
`SHURIKEN_FROM_TTO` (wardrobe_fx.py:333), `BUILT` (wardrobe_fx_inventory.py:23) and the bat.js gate (:443) are where
cited; `guard` / `attack` are indeed new to `OPTS`; `graft_try.txt` shows the two systems matched by material. The
TTO table's WhaleLeviathan / WhaleDolphin facts agree with tto.md. Not re-run: the inventory's "50 / 51 ready" (the
lead's run after the build).

1. **The 12th Kingdom Knight's key: its own tile, `@12thKingdomKnight:cast3` (decided).** What is wrong: `@KingdomKnight:cast3`
   is no sequence (the Whale's SEQ, index.html:1369-1370, has none; `blocks.txt`), and no skills_a report is on this PC to
   key it. The skill has **no cast bar**: the dispatcher starts `RPC_kingdomKnight` directly (Whale.cs:7482), where
   Heavy Weight and Bubble Shield go through `RPC_cast1` (:7415, :7447). So it is a one-step tile on cast3, as the Sheep's
   Eden Sanctuary and the Chameleon's Immunity (Chameleon decision 6), named as the Bible names it (`12thKingdomKnight`,
   whale-skill-reference.md:22). Page changes (page_pipeline): SEQ.whale += `"12th Kingdom Knight: cast3"` (play()'s 0.2 s
   fade = `PlayAnimation(cast3, 0.2)`, :28640); `SEQ_SKILL.whale["@12thKingdomKnight"] = "12thKingdomKnight"`;
   `wardrobe_skill_icons.py`: `OWN_TILE["whale"] = {"12thKingdomKnight": ["cast3"]}` and, because the Bible key starts
   with a digit, which the icon regex `{cls}_([A-Za-z]+?)(\d*)` (:109) cannot read, `RANK_ICONS["whale"] =
   {"12thKingdomKnight": "whale_12thKingdomKnight2"}` (the top rank; `assets.js` has `whale_12thKingdomKnight1` / `2`), then
   the HD rebuild. The corrected entry (the cues unchanged):

```json
  "@12thKingdomKnight:cast3": {
    "why": "Whale.cs $RPC_kingdomKnight$28772 (:28262-28850), max rank sLv 2 (12thKingdomKnight1 / 2, whale-skill-reference.md:22), started by the dispatcher with no cast bar (:7482; Heavy Weight / Bubble Shield go through RPC_cast1, :7415, :7447): at 0 the clip cast3 (0.2 fade, :28640), voice kingdomKnight1 | kingdomKnight2 (Random.Range(0, 2) :28681; :28693 / :28724; PlayOneShot :28705 / :28736), kingdomKnight_ring1 by createEffect at the hero, hero rotation (:28755-28767), the old knights unsummoned (:28799); Yield(2, 0.5) (:28816): at 0.5 2 + 2 sLv = 6 knights (:28414), kingdomKnight2 for sLv 2 (:28468-28480), Init(owner, sLv, slot i) (:28506): each at hero + TransformDirection(slot) - up, slot 0-5 = (1.6, 0, 1.6), (-1.6, 0, 1.6), (1.6, 0, -1.6), (-1.6, 0, -1.6), (2.2, 0, 0), (-2.2, 0, 0) (whale_kingdomKnight.cs:54-120), kingdomKnight_ring2 at its slot on the floor (:126-132), rising to the slot (Lerp 4 / s, :229); the kingdomKnight status chaAdjust(60) (:28527-28538), cut at 10 s after the summon (Bat decision 25): end 10 = unsummon(), its clip unsummon then Destroy 1 s later (whale_kingdomKnight.cs:867-913, Whale.cs:9827-9868); Yield(3, 0.5) (:28820): 1.0 standby (:28570). No volley: KingdomKnight() picks FindClosestTarget(the Whale, 8) (Whale.cs:9729; the volley RPC :29062), the target is 10 m away",
    "builds": ["kingdomKnight_ring2"],
    "cues": [
      [0, "voice", "kingdomKnight1|kingdomKnight2"],
      [0, "fx", "kingdomKnight_ring1"],
      [0.5, "fx", "kingdomKnight2", {"slot": 0, "end": 10}],
      [0.5, "fx", "kingdomKnight2", {"slot": 1, "end": 10}],
      [0.5, "fx", "kingdomKnight2", {"slot": 2, "end": 10}],
      [0.5, "fx", "kingdomKnight2", {"slot": 3, "end": 10}],
      [0.5, "fx", "kingdomKnight2", {"slot": 4, "end": 10}],
      [0.5, "fx", "kingdomKnight2", {"slot": 5, "end": 10}]
    ]
  }
```

2. **KeyT is decoded, and the heuristic is wrong.** What is wrong: "KeyT, a heuristic ... `[0, 0.4, 0.6, 1.3, 1.75, 2.2,
   2.7]`" (:289-292), question 7 and the "TTO's KeyT: low" row. The `.cctor`'s `InitializeArray` labels for the three field
   handles this report names (0x3809788 / 0x38044e0 / 0x3800000) read KeyT **[0.4, 0.6, 1.3, 1.75, 2.2, 2.7, 3.2]**,
   KeyPitch **[-90, -88, -76, -22, 10, 20, 30]**, KeyRoll **[0, 0, 70, 145, 180, 190, 200]**
   (`checks/fx_whale_research/tto/annot/WhaleLeviathan.c:1307-1309`; tto.md P2). The 0x63e9b4 blob is not KeyT. Question
   7 is closed; the row reads high.
3. **Interfaces 6 is superseded by tto.md's block.** The dolphin cue is the lane's start at the cue's own spot (`x`, `d`),
   `to` ([x, y, d]) its end and **`hops`** given (3, the hero's LeviathanHops on the spot), not `from` / `to` with the part
   computing the hops from the lane's length (tto.md Verification 5). New `OPTS` words for page_pipeline: `guard`,
   `attack` (this report) and `hops`, `animLoop` (tto.md Verification 3).
4. **Agent A also builds tto.md's P3 in bat.js.** The castRing of Leviathan Breach's cast plays `root` looped from its spawn
   (TTO1102 Row6Spawn's `loop`): `fx:castRing` reads the cue's `animLoop` on its first update and then skips the 0.5 s
   restart (tto.md Verification 4). Part 7 and the "Who builds what" row for A gain it (still bat.js only).
5. **`SKILL_FX["whale"]` is the five TTO prefabs only.** What is wrong: the TTO table's last row adds "TTO's castRing" and
   the three sounds. The game loads TTO's own castRing, but it draws as BB's (the same root and mesh; its extra
   `ImageEmitter` node has a MeshRenderer and nothing to draw; its `destroy` clip is never seen with afterLife 0:
   `verify/tto_castring.json`, tto.md Verification 1), so the cue uses BB's `castRing`; the sounds are BB rip WAVs
   (grandTide_ring, shieldBash_hit, whaleWave, grandTide, bowlingWhale in `whale/sounds/`), built by `wardrobe_fx.py`.
6. **Question 8 resolved: bubbleShield / salvation scale 1.2, at y 1.3.** What is wrong: "`mChar.radius` is CharacterControl's
   own field, not the prefab's CharacterController". `CharacterControl.mChar` **is** the hero's CharacterController
   (`public CharacterController mChar;`, CharacterControl.cs:29789; the Penguin's Ice Shield, plans/fx_penguin/cast_a.md
   8); the Whale prefab's is `m_Radius 0.8`, `m_Center (0, 1.3, 0)`, `m_Height 2.4` (rip `heroes/whale/Whale.prefab:643-656`).
   So `Clamp(0.8 + 0.4, 0.5, 1.5)` = **1.2** (CharacterControl.cs:35999, :36036), and `collider.bounds.center` is 1.3 m
   up (the hero at scale 1): the skills researcher's cues take `{"y": 1.3, "scale": 1.2}`.
7. **One word for each option across the Whale's reports (decided: this report's interface).** attacks_emotes.md:402
   gives the Round Table knights `"i": k`; the part reads **`slot`** (Interfaces 1), so that cue becomes
   `{"slot": k, "standing": true, "guard": [0, T], "kill": T + 0.5}` (this report's shape, :406-407). skills_b.md:509
   gives Grand Tide `{"anims": [[1.0, "root"]], "end": 4.0}`; no Whale part reads `anims` (only cat.js's
   `fx:grandCasinoArcade`, :124, and elementals.js) or `end` on grandTide, so that cue becomes this block's
   `[1, "fx", "grandTide", {"release": 4}]` (`fx:grandTide` plays `root` at age 1.0 itself, part 6).
8. **The target body: use the Bat's capsule.** Parts 2-3 test against a box (x +-0.3, y 0.1-1.1). The page's other parts
   use the Bat decision 4 capsule (axis (0, 0.4-0.8, 10), radius 0.3; `fxparts/bat.js:30`). Same result here: Flying
   Shield's closest pass (-0.91, 1.36, 11.62) is 1.64 m from the capsule (1.48 from the box), outside its 1 m sphere, so
   still no hit; Homing Shield's passes are tested with the capsule too (one body for every Whale part).
