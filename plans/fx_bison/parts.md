# Bison effects: the parts the page cannot draw yet (or draws wrongly)

Research 13/11/2026, home PC (one of the Bison fx researchers; scope: every part the Bison's effects need: the
inventory's 46, the 18 Bison prefabs it does not list, and the released TTO skills' 17 prefabs). Models:
`plans/fx_penguin/parts.md`, `plans/fx_sheep/parts.md`, `plans/fx_bat/parts.md` (the Bat's parts are researched, not
built yet: where the Bison needs one of them it says so and does not respecify it). Read only: nothing in `wardrobe/data`
was written, `wardrobe_fx.py` / `wardrobe_fx_tto.py` ran with `--probe` only, no browser. BB lines are
`D:\12tails\DecompiledSource\<file>:<line>`; TTO is `TTO1102:` + method + RVA (`BUILD.md`'s rule: never pseudo-C lines).

Probes (read only, outputs beside them) in `checks/fx_bison_research/parts/`:
- `probe.py` -> `probe.txt`, `probe_short.txt` (bone-only nodes dropped), `summarize.py` -> `summary.txt`: all 64
  prefabs in `heroes/bison/effects` through `wardrobe_fx.effect()` (a copy of the Bat's probe: unknown scripts' field
  bytes and raw words, every material's blend, the components `effect()` skips).
- `probe2.py` -> `probe2.txt`: every Animation clip (name, length, wrap) and AudioSource; the Bison hero prefab's
  `Bison` component references resolved (`nAttack_hit`, `cAttack_hit`, `overLord`).
- `shader_text.py` -> `shader_text.txt`, `shader_fp.py` -> `shader_fp.txt`: the compiled text BB keeps for the game's
  `Velvet` (sharedassets2, path 90; the rip's `velvet.shader` is AssetRipper's dummy) and `Particles/AdditiveOffset`.
- `tto_probe.json` (+ `tto_summary.py` -> `tto_summary.txt`, `tto_scripts.txt`), `tto_probe_slam.json`
  (`tto_summary_slam.txt`): `wardrobe_fx_tto.py bison --probe` of the 17 TTO prefabs and of TTO's copy of
  `magmaClutter_ring2`; `catalog_keys.py` -> `catalog_keys.txt` (TTO catalog addresses: `titanDrop_slam` is
  `titanDrop_slam1-3`).
- `shader_dxbc.py` -> `dxbc_EnergyArc.txt`, `dxbc_MoltenCrust.txt`: TTO/Bison/* pass state and D3D11 programs.
- `disasm.py` -> `disasm.txt`: `TTO1102:GroundConformParticles::GroundAt@0x2260680`, `::LateUpdate@0x2260850`,
  `::Sample@0x2260bf0` (capstone, call targets named from `names.tsv`).

## Read this first

1. **Three Bison scripts have no layout; one of them blocks the build.** `probe.txt`'s last line: `UVScroll` 8 bytes x3,
   `Bison_earthRupture` 0, `Bison_overLord` 0. `wardrobe_fx.py` raises on UVScroll's 8 bytes, so `aspect_slam` and
   `aspect_trample` (Slam's and Trample's horde ghosts) **cannot be built today**. UVScroll is shared (Cat `deltaStrike`,
   Whale `bowlingWhale`: inventory).
2. **The inventory sees 46 of 64 prefabs.** The other 18 come from:
   - status looks `CharacterControl.cs` loads in `addStatus` (`$addStatus$35621`): holdCharge_ring :34670 + holdCharge
     :34673 (parented to the hero :34692); berserkerRush_ring :34876 + berserkerRush x2 on `HandMount_L` / `HandMount_R`
     :34907 / :34932; furyTrance1-3 on `Neck` :34963 / :34982; overPower_horn1-2 on `Head` with **localRotation
     Euler(-90, 0, 0)** :35010 / :35016 / :35022 and overPower_ring on the hero :35028 / :35034; ironShield :35064,
     diamondShield :35095, perfectShield :35129, perfectArmor :35164, titanForm :35243 / :35262 (all on the hero,
     localScale one);
   - the hero prefab's fields (`probe2.txt`): `nAttack_hit` (offset 24) and `cAttack_hit` (offset 48) are **the same
     prefab** (`nAttack_hit`, path 274); `overLord` (path 273), made at Start (`Bison.cs:96` -> `createOverLord`
     :8480-8517, parented to the hero).
   Of these, only overPower_horn needs something the page lacks (a bone with a local rotation, Interfaces 1).
   `perfectShield` / `perfectArmor` are statuses **no code adds** (no `"perfectShield"` / `"perfectArmor"` AddStatus in
   BB's sources or TTO's pseudo-C; only the voices `perfectShield1-2` exist, played by Iron / Diamond Shield,
   `Bison.cs:27480`, :28067): nothing cues them.
3. **Shaders the page draws wrongly** (the inventory does not see shaders):
   | material (effects) | shader | today | needed |
   |---|---|---|---|
   | `earthsmasher` (earthSmasher, massStun: the rock) | game's `Transparent/Opaque1`, faded by its **AlphaTimer** (on `_Color`) | mesh.js draws it, but `alphatimer.js` knows no Opaque1 (`OPACITY`, `alphatimer.js:27`): it warns and the rock **never fades**: it stays solid from 1.0 s (earthSmasher: 0.8 s hold + 0.2 s fade) / 0.8 s (massStun: 0.5 + 0.3) to the effect's end at 2.0 s | AlphaTimer on Opaque1, both passes (part 2) |
   | `nAttack_hit1`, `nAttack_hit2` (nAttack_hit: every Combo / Charge Attack hit), `nAttack_hit1` (knockDown_hit) | game's `Particles/AdditiveOffset` | fxMaterial's alpha-blend fallback | the Bat's `particles.js` item (its part 9), unchanged |
   | `Bomb2` (calamityHammer_fire / _ring, magmaClutter_ring1) | built-in 206 | `multiply2`, built | - |
   | `bison_dead` (deadEffect) | built-in 207 | `premul`, built | - |
   | `perfectArmor` (perfectArmor) | game's `Velvet` (rim light) | fxMaterial alpha fallback, warned | rim-lit Lambert (part 7); **no code reaches it** (2 above) |
4. **The hero's own body changes in two statuses** (not prefabs): Enrage scales the Bison by `+0.05 x sLv` and tints
   him with `setColor(0.8 + 0.05 sLv, 0.8 - 0.05 sLv, 0.8 - 0.05 sLv)` (`CharacterControl.cs:34717-34724`; back to
   0.86 grey at the end, :15412-15422); Titan Form scales him by `+(0.3 sLv + 0.2)` = **1.8x at rank 2** and tints him
   `(0.6, 0.7, 1)` (:35219-35223; back at :15675-15681). `setColor` writes `_Color.rgb` on **every renderer under the
   character** (`CharacterControl.cs:21702-21745`), effects parented to him included; the normal colour is 0.86
   (`mColor` reset to `(0.86, 0.86, 0.86)` everywhere, e.g. :15153). The Bison prefab's root scale is 1
   (`Bison.prefab:1038`). The page has no such hero look (Interfaces 2, question 1).
5. **One BB prefab has Unity 3.5's Shuriken.** `magmaClutter_ring2`'s swinging `TrailEmitter` node also holds a
   ParticleSystem + ParticleSystemRenderer (`probe.txt`: skipped comps); `wardrobe_fx.py` does not decode BB's
   ParticleSystem (`wardrobe_weapon_fx.py:14-18`), so the puffs it leaves along the Magma Clutter swing are missing.
   TTO's copy (`tto/magmaClutter_ring2` in `tto_probe.json`) has the system decoded (rate 128/s, life 0.6 s, size curve
   0 -> 1 -> 0, world space, colour white -> (0.99, 0.42, 0.37, 0.44) -> grey 0, material `tto_Bomb2` = Multiply
   (Double)) **but loses the swing**: its Animation clip `cleave` "is written by name only, not exported"
   (`tto_probe.err`). So: BB's effect plus TTO's two components grafted onto the node (part 5).
6. **TTO's released skills need two Bison scripts and two Bison shaders** (`tto_summary.txt`): `Bison_c6Arc` (the
   ground / air crescents in 13 of the 17 prefabs), `Bison_row6Fx` (Unchained Fury's chains), `TTO/Bison/EnergyArc` (the
   crescents' material) and `TTO/Bison/MoltenCrust` (Magma Quake's lava pool). Also `AudioControl` on every TTO sound
   node (15; the Bat's `audiocontrol.js`), and `GroundConformParticles` (5 roots), which is a **no-op on the page's flat
   floor** (part 10). Everything else in them (GroundHugEmitter, ImageEmitter, ParticleSystem with Shape types 0 / 4 /
   10, render modes 0 / 1 / 4, TrailRendererModern, StaticMesh) is built (`shuriken.js`, `groundhug.js`,
   `tto_sheep.js`, `mesh.js`).
7. **Sounds the effects play themselves (`probe2.txt`): no trap.** Every BB effect clip is in `bison/sounds/` except
   `lavu_upheaval` (stunningGround_ring: `elementals/lavu/sounds/`, found by `rip_wav`'s walk). `cAttack1`, `trample1`,
   `trample2` are in both `sounds/` and `voices/`: `rip_wav` (`wardrobe_fx.py:343-359`) takes `sounds/` first for an
   effect's own source, and voices are asked with their folder, so the kinds stay apart. Looping sources: cAttack1_dust
   (`cAttack1`), the four shields (`shield`), magmaQuake_magmaField (`MagmaPit`), magmaQuake_quakeField
   (`titanQuake_ring`): the page loops them until the effect goes.
8. **Blood Carnage (the shared support skill) loads the Bat's files** (`Bison.cs:10552` `Heroes/Bat/Effects/
   bloodCarnage_ring`, :10619 `Heroes/Bat/Voices/bloodCarnage1`, and `...2`): the Bison's folder has neither. If a
   Bison tile plays it (the skill reports' call), `wardrobe_fx.py` needs `EXTRA_FOLDERS["bison"] =
   ["gameassets/characters/heroes/bat/effects"]` (tried after the Bison's own folder, so the Bison's `nAttack_hit`,
   `castEffect` ... still win) and the voice folder alias the Bat's Interfaces 6 proposes (`SOUND_ALIASES`).

## The Bison's blocked set

"Where" is where BB spawns it (the standing rules move enemy spots to the 10 m target point).

| effect | skill (spawn) | missing part(s) | where |
|---|---|---|---|
| `aspect_slam` | Slam (`Bison.cs:21449`) | UVScroll layout + part; AlphaTimer / UVScroll sharing one material copy | hero (followPosition, followState) |
| `aspect_trample` | Trample (`Bison.cs:22536`) | the same (two skinned hordes, 2.5 m left / right) | hero |
| `earthRupture` (x3 at max rank) | Earth Rupture (`RPC_earthRupture_fire2`, `Bison.cs:8829-8929`) | Bison_earthRupture mover (0 bytes) | hero + (0, 0.2, 0.4), yaw -25 / 0 / +25 |
| `earthSmasher`, `massStun` | Earth Smasher (`:29132`), Mass Stun (`:9096`) | AlphaTimer on Opaque1 (both passes) | earthSmasher at the hero (`:29132-29140`), massStun at `RPC_massStun_fire`'s `tPos`, `LookRotation(tDir)` (`:9082-9103`) |
| `nAttack_hit`, `knockDown_hit` | every Combo / Charge Attack hit (`Bison.cs:7097`), Knock Down (`:7511-7520`) | AdditiveOffset (the Bat's particles.js) | target (10 m) |
| `magmaClutter_ring2` | Magma Clutter (`:31506`) | the Shuriken graft from TTO's copy; shuriken.js taking the renderer's own material | hero |
| `overPower_horn2` | Over Power status (`CharacterControl.cs:35010-35022`) | a cue `bone` with a local rotation | the `Head` bone, Euler(-90, 0, 0) |
| Enrage / Titan Form body | the statuses (`CharacterControl.cs:34713-34724`, :35209-35223) | a hero look: grow + tint (question 1) | the hero |
| `perfectArmor` | (no code adds the status) | Velvet | hero |
| TTO: 13 prefabs with crescents | Magma Quake, Titan Drop, Unchained Fury | Bison_c6Arc + EnergyArc | the prefabs' own |
| TTO `unchainedFury_chains` | Unchained Fury | Bison_row6Fx | the hero |
| TTO `magmaQuake_magmaField` | Magma Quake | MoltenCrust (on its GroundHugEmitter pools) | the field |
| TTO, 15 sound nodes | all three | AudioControl (the Bat's audiocontrol.js) | - |

Ready today and only needing cues: everything else (the rings, dusts and hits: RingEmitter / LineEmitter /
ImageEmitter / legacy particles / EmitterControl / EmblemEmitter / VortexEmitter; trample1-2, trample_dust, slam_dust,
instantRush_ring with AlphaTimer on built-in 200 `add`; powerCleave / powerHammer / magmaClutter_ring2's swing
(Animation + TrailEmitter / TrailRenderer); the four shields (Animation + SkinnedMesh `opaque` + TrailEmitter
`alwaysUp`, `TrailEmitterMode` 1); holdCharge, berserkerRush, furyTrance1-3, titanForm, overPower_ring (no
EffectControl: they live until the status ends, so the cue's `kill`, 10 s cap); deadEffect (premul)). `overLord` draws
nothing (part 4).

## LAYOUTS (paste into `pipeline/wardrobe_fx.py`, after the Bat's block)

```python
# the Bison's parts (plans/fx_bison/parts.md, 2026-11-13; checks/fx_bison_research/parts/probe.txt: UVScroll's three
# instances are its two floats exactly, (0.2, -0.2); Bison_earthRupture / Bison_overLord keep every field private)
LAYOUTS.update({
    "UVScroll": [("scroll_x", "f"), ("scroll_y", "f")],   # UVScroll.cs:67, :70 (8 bytes; Bison 2, Cat 1, Whale 1)
    "Bison_earthRupture": [],                             # Bison_earthRupture.cs:218-228: all private (the mover, part 3)
    "Bison_overLord": [],                                 # Bison_overLord.cs:206-215: all private (an aura trigger, part 4)
})
```

Values: aspect_slam's and both aspect_trample hordes' `scroll_x` 0.2, `scroll_y` -0.2 (`probe.txt`; the constructor's
default is 0.1 / 0.1, `UVScroll.cs:26`, :29).

And in `material()` (`wardrobe_fx.py:250-252`, beside `_Ambient`): save `"rim": colors["_RimColor"]` when the material
has it (Velvet's `_RimColor`, RGB colour + power in A; `perfectArmor.mat`: (0.384, 0.594, 1.0, 1.0)). Only part 7
reads it.

## Each part

Page parts plug in as the comment above `FX_PART_FILES` says (`index.html:3723-3745`): `wardrobe/fxparts/<file>.js`
default-exports `register(api)` and calls `api.part(type, build)`; `build(fx, node, comp, mat, nodeDef, data)` returns
`{ node, update(dt, cam) ("destroy" removes the node), stop?(), dispose?() }` or null; `api.shader(blend, make)` owns a
data blend. Clocks: as `alphatimer.js`, `t += dt` from the first update (the spawn frame).

### 1. UVScroll: `aspect_slam`, `aspect_trample` (also Cat `deltaStrike`, Whale `bowlingWhale`)

**What it does in BB (`UVScroll.cs`).** Fields `scroll_x`, `scroll_y` (:67, :70; defaults 0.1, :26, :29). Update
(:42-46): `offset = (Repeat(Time.time x scroll_x, 100), Repeat(Time.time x scroll_y, 100))`, then
`renderer.material.SetTextureOffset("_MainTex", offset)` (:45): the renderer's own material copy, its main texture's
offset **replaced** (the saved offset is lost), from the game's absolute clock (so every UVScroll in the scene scrolls in
step: the two Trample hordes move together).

**The effects.** aspect_slam: a StaticMesh (3,700 verts) with UVScroll and AlphaTimer (0 -> 0.3 over 0.2 s, held 0.1 s,
out 0.1 s), EffectControl life 1 followState. aspect_trample: two skinned hordes (2,824 verts each, 2.5 m left and
right, Animation `root` 0.667 s loop), each with AlphaTimer (0 -> 0.3 in 0.2 s, held 5 s) and UVScroll, life 3
followState. Material `aspectOfTheHorde`: built-in 200 `add`, tint (0.5, 0.5, 0.5, **0**): invisible until the
AlphaTimer raises it, as the game ships it. Comps order differs: aspect_slam StaticMesh, UVScroll, AlphaTimer;
aspect_trample SkinnedMeshRenderer, AlphaTimer, UVScroll.

**The page part (`fxparts/uvscroll.js`, new, about 25 lines, generic).**
- First update: the node's mesh (`node.children.find(x => x.isMesh)`), its per-renderer material copy by the shared
  convention (Interfaces 3: reuse it when another part made it, else clone and write it back), and a clone of that
  copy's `map` (three keeps the offset on the Texture object, shared by every material of that texture: clone it, the
  image source stays shared), `map.repeat` kept from the data's scale.
- Each frame: `T` = the page's absolute clock (`performance.now() / 1000`, as `tto_sheep.js`'s `time`), `map.offset.set(
  (T x sx) mod 100, (T x sy) mod 100)` (Unity's Repeat = a positive modulo). Unity's and three's uv offsets have the same
  sense (`fxMaterial` sets `t.offset` from the data's `_MainTex` offset as is, `index.html:3775+`), so no sign change.
- `dispose()`: free the map clone (and the material copy if this part made it).
- APPROXIMATED: the phase (the game's Time.time since the client started) is the page's clock's.

### 2. AlphaTimer on Opaque1 / Opaque2, and one per-renderer copy shared by parts (`fxparts/alphatimer.js`)

**What the game does.** AlphaTimer drives `_Color` when the shader has it (mode 1, `AlphaTimer.cs:63`), and Opaque1 has
`_Color` (its `Material { Diffuse [_Color] }`, `Opaque1.shader:10-18`; `mesh.js:103-126`): alpha = `_Color.a x
texture.a` in both passes. earthSmasher's and massStun's rock (`earthsmasher`, saved `_Color` (0.78, 0.78, 0.78,
**1.0**)) get both passes from mesh.js (`opaque1`, `mesh.js:127-134`: pass 1 ZWrite Off, AlphaTest GEqual 0.95; pass 2
ZWrite On, alpha blend). Timers: earthSmasher Min 0, Max 1, delay 0, in 0, middle 0.8, out 0.2; massStun middle 0.5,
out 0.3 (`probe.txt`): solid, then faded to 0 by 1.0 s / 0.8 s; EffectControl life 2 (no after-life). While the alpha
is under 0.95 pass 1 draws nothing (its test fails), pass 2 blends: the game's own fade.

**Today.** `OPACITY` (`alphatimer.js:27`) has `add`, `alpha`, `shader:FX/Phoenix` only: `own()` (`:31-41`) warns "no
_Color / _TintColor known" and the timer is off. And `own()` clones only `mesh.material[0]`: with a two-pass material
`withMaterials` puts **both passes** in the list (`mesh.js:200-210`), so even with an entry the second pass would keep
alpha 1.

**The change (alphatimer.js, about 10 lines).**
- `OPACITY["shader:Transparent/Opaque1"] = OPACITY["shader:Transparent/Opaque2"] = a => a` (alpha = `_Color.a`, not
  doubled: the alpha part of their combine has no "double", `mesh.js:106-107`).
- The first material's passes: `mesh.material[0]` and, when its `userData.fxPass === 0`, the entry after it whose
  `fxPass === 1` (mesh.js tags them). Clone each (keep `onBeforeCompile`, as now), write them back, set the opacity on
  all of them each frame. Unity's `renderer.material` is one copy driving every pass.
- Honour the shared copy (Interfaces 3): when `mesh.userData.fxOwn` is set, use the materials there as they are.
- Matches the Bat's Interfaces 5 (mesh.js builds both Opaque1 passes always): with both passes at any saved alpha this
  code is the same.

### 3. Bison_earthRupture (+ ProjectileControl): `earthRupture`

**What it does in BB (`Bison_earthRupture.cs`).**
- Awake (:20-84): layer 1 (:28), `ProjectileControl` of its own node (:31), ignores collisions with every other
  "Projectile" (:34-66). Init(owner) (:88-92): the owner and its CharacterControl.
- FixedUpdate (:96-127): clock `+= Time.deltaTime` (:103); at `ProjectileControl.life` Destroy (:106-110); else
  `rigidbody.velocity = transform.TransformDirection(ProjectileControl.velocity)` (:119) every step: the prefab's
  **(0, 0, 12)** along its spawn rotation (rotation frozen, `m_Constraints 112`, no gravity: `probe.txt` skipped comps).
- OnCollisionEnter (:131-198): a Player / Enemy collider is ignored from then on (:156) and hit (`hit(203, ...)`,
  :186); **it is not destroyed**: the rupture runs through every foe. (Walls stop it physically: none on the page.)
- The hero's code sets `life = 2` (`Bison.cs:8797` fire1, :8892 fire2): **2 s, 24 m**.
- Max rank (Earth Rupture 2, Bible table): `RPC_earthRupture_fire2` (`Bison.cs:8829-8929`): `lhs = LookRotation(fireDir)`
  with its z euler set to 0 (:8862), three ruptures at `lhs x Euler(0, 25 i, 0)`, i = -1, 0, 1 (:8877), from `firePos
  = hero + TransformDirection(0, 0.2, 0.4)` (:28634).

**Draws anything?** No: it moves the root. The three skinned "teeth" (Animation `root` 1.2 s loop, `addsoft`) and the
two legacy emitters (dust, smoke) are built.

**The page part (`fxparts/bison.js`, new, about 15 lines; the shape of `sheep.js`'s `mover`).** Velocity
`(0, 0, 12)` (the node's `ProjectileControl.velocity`, `nodeDef.comps`) turned by `fx.uQuat(node)` at the spawn (the
cue's rot is on the root); `node.position += vel x dt`; `"destroy"` at t >= 2 (the hero code's life). No floor end (it
travels 0.2 m up, level) and no target end (it pierces).

### 4. Bison_overLord: `overLord` (draws nothing)

`Bison_overLord.cs`: Init(nLv, ownerID) (:21-50) finds the owner; OnTriggerEnter / Exit (:56-123, :126-190) give or
take an ally Tails the `overLord` status (`addStatus("overLord", lv, 999, ceil(0.05 x def x lv))`, :110; removed :173)
inside its 10 m trigger sphere (`probe.txt`). The prefab has nothing else: no part, no cue. Its `[]` layout (above) and
a place in `BUILT` (as `Sheep_seal`, "draws nothing") are all it needs. (Bible quirk already recorded: Enrage's body
scale widens the sphere, `bison-skill-reference.md:270`.)

### 5. magmaClutter_ring2's Shuriken, read from TTO's copy (`pipeline/wardrobe_fx.py`, lead; `fxparts/shuriken.js`)

**The effect (BB, `probe.txt`, `probe2.txt`).** Root scale 0.7, EffectControl life 1 + 0.5 followState, AudioSource
`magmaClutter2`; node 1 `magmaClutter_cleave` (Animation `cleave` 0.4 s, wrap 0: the swing); node 2 `TrailEmitter` at
(1.99, 1.54, 2.38) under it, with the game's TrailEmitter (`ExplosionRay`, `addsoft`, MeshRenderer) **and** a Shuriken
system + renderer the BB read skips.

**The graft (about 25 lines in `wardrobe_fx.py`, the lead's).** A table `SHURIKEN_FROM_TTO = {"bison":
["magmaClutter_ring2"]}`. After `effect()` builds BB's version, read TTO's copy with `wardrobe_fx_tto`'s `Tto` /
`Build` / `effect` (as `wardrobe_weapon_fx.tto_weapons` does, `wardrobe_weapon_fx.py:77-97`), and for each BB node whose
name path matches a TTO node carrying a `ParticleSystem`, append that node's `ParticleSystem` and
`ParticleSystemRenderer` dicts to the BB node's comps (after its own); keep the BB node's `mats` (`["ExplosionRay"]`:
the TrailEmitter's). Merge the renderer's material: `tto_Bomb2` (`m_Materials: ["tto_Bomb2"]`; shader `Legacy
Shaders/Particles/Multiply (Double)`, texture `tto_Bomb2_0`) as `multiply2` (one line in `wardrobe_fx_tto.SHADER_BLEND`,
`wardrobe_fx_tto.py:132`: `"Legacy Shaders/Particles/Multiply (Double)": "multiply2"`), or point the renderer at BB's
own `Bomb2` (the same shader, built-in 206, already in `fx.json` for calamityHammer) and skip the TTO texture.

**shuriken.js (2 lines, `shuriken.js:299-303`).** Today the system takes `mat` = the node's `mats[0]` and reads the
renderer's own list only when that is missing. Prefer the renderer's own first material when it names one the data has:
`const own = rd.m_Materials?.[0]; if (typeof own === "string" && data.materials?.[own]) mat = api.fxMaterial(fx.cls,
own, data.materials[own]);`. In every TTO-read node the two are the same name (wardrobe_fx_tto writes the renderer's
first materials into `mats`), so nothing else changes; here the puffs get Bomb2 and the trail keeps ExplosionRay.

### 6. Hero looks: a bone with a local rotation; the body's growth and tint (`index.html`, lead)

- **overPower_horn2 on `Head`, localRotation Euler(-90, 0, 0)** (`CharacterControl.cs:35016-35022`; max rank 2 picks
  `overPower_horn2`, :35010 `"overPower_horn" + sLv`). The cue's `bone` holds an effect at the bone with localRotation
  identity (`index.html:3985-3991`: the root's quaternion is replaced by the bone's each frame, so the cue's `rot` is
  lost). Change: when the cue has both, keep `rot`'s quaternion at construction (the root already gets it,
  `index.html:3904`) and multiply it on after the bone's (`this.root.quaternion.multiply(this.boneRot)`): Unity's
  `localRotation` under the bone. The rig has `Head`, `Neck`, `HandMount_L` / `_R` (`wardrobe/data/bison/rig.json`).
- **Enrage / Titan Form body** (question 1). A `"look"` cue kind beside `"skin"` (`HERO_SKINS`, `index.html:4379`; its
  `HeroSkin` life rules, kill and a new pick ending it): `{ "grow": g, "tint": [r, g, b] }` scales the hero's root by
  `g` (Unity's `localScale + n x one` on a scale-1 root) and multiplies every hero mesh material's colour by `tint` =
  `mColor / 0.86` (the page draws the normal look; the game's normal `_Color` is 0.86), restored on dispose. Values at
  max rank: Enrage 4 (+ Rage Control #402, sLv 5, `Bison.cs:20968-20973`): grow 1.25, colour (1.05, 0.55, 0.55) -> tint
  (1.22, 0.64, 0.64); without Rage Control grow 1.2, tint (1.16, 0.70, 0.70). Titan Form 2: grow **1.8**, colour (0.6,
  0.7, 1) -> tint (0.70, 0.81, 1.16). Effects the game parents to him with localScale one (titanForm's ring, the
  shields) grow with him: give their cues `scale` the same factor inside that tile.

### 7. Velvet: `perfectArmor` (no code adds its status: build last, or not)

**The shader** (BB's compiled text, `shader_fp.txt`; the rip's `velvet.shader:7` is a dummy): a Lambert surface shader,
ForwardBase (+ ForwardAdd, PrePass), opaque, ZWrite on, Cull Back. Its fragment program: `albedo = tex.rgb x _Color.rgb`;
`rgb = 2 x albedo x _LightColor0 x max(0, N.L) + albedo x SH ambient + _RimColor.rgb x (1 - saturate(dot(normalize(
viewDir), N)))^_RimColor.a`; alpha 0. perfectArmor: `_Color` white, `_RimColor` (0.384, 0.594, 1.0, power 1), texture
`perfectArmor`.

**The page (mesh.js `material()`, about 15 lines).** `"shader:Velvet"` -> as mesh.js's `opaque` (a Lambert with `map`,
`color` = `_Color`; the page's convention for the built-in Diffuse beside it, perfectShield) plus the rim as emissive:
`onBeforeCompile` adding after `#include <emissivemap_fragment>`: `totalEmissiveRadiance += fxRim.rgb * pow(1.0 -
clamp(dot(normalize(vViewPosition), normal), 0.0, 1.0), fxRim.a);` (three 0.160's Lambert has both in its fragment),
`fxRim` from the data's `rim` (LAYOUTS paragraph; default white, power 1). FrontSide. APPROXIMATED: the game's lights.

### 8. Bison_c6Arc + TTO/Bison/EnergyArc: 13 TTO prefabs (`fxparts/tto_bison.js`, new)

**Fields** (`dump.cs` `Bison_c6Arc`, `tto_scripts.txt`): delay, duration, diameter, angle, spin, repeat, color, hug, lift.
Every instance: angle 25 (Sweep0) / 205 (Sweep1), spin 140, repeat false, lift 0.25; hug true except unchainedFury_roar's
three air spirals (RoarSpiral0-2's Sweeps, hug false); diameter = the node's saved scale (4 ... 60).

**What it does in TTO.**
- `Awake@0x1B9B7C0`: its MeshRenderer, a MaterialPropertyBlock; with `hug`, its own copy of the mesh (`Instantiate<Mesh>`)
  and the flat vertices kept.
- `OnEnable@0x1B9BDB0`: `started = Time.time`; renderer **off**.
- `Update@0x1B9BDF0`: `t = Time.time - started - delay`, `d = max(0.01, duration)`. `t < 0`, or `t >= d` (repeat false):
  renderer off, done. Else `k = t / d` (repeat: `(t mod d) / d`):
  - `localScale = diameter x (0.65 + 0.4 x (1 - (1 - k)^2)) x one` (eased out, overriding the saved scale);
  - `localRotation = Euler(0, angle + spin x t, 0)`;
  - `_TintColor` (property block) = 0.5 x `(lerp(c.r, 1, f), lerp(c.g, 0.38, f), lerp(c.b, 0.08, f), 0.75 x (1 -
    S(k)) x S(k / 0.08) x c.a)`, `f = clamp01(0.45 k)`, `S` = smoothstep `x^2 (3 - 2x)` on a clamped x: it warms toward
    orange, fades in over the first 8 %, out along the rest;
  - with hug: `Drape@0x1B9B9A0`: every vertex to world, `y = GroundHugEmitter.Ground(world, transform.position.y) +
    lift`, back to local (`InverseTransformPoint`), the mesh's vertices replaced: the crescent lies 0.25 m above the
    ground whatever its parent's tilt;
  - renderer on.
- `.cctor@0x1B9C280`: the property is `_TintColor`.

**EnergyArc** (`dxbc_EnergyArc.txt`): Blend SrcAlpha One (additive), ZWrite Off, Cull Off, Queue Transparent; vertex
colour `2 x _TintColor x vcol` (vs `add o1 = r0 + r0`); fragment `alpha = S(u / 0.1) x (1 - S((u - 0.9) / 0.1)) x v x
vcol.a`, `rgb = vcol.rgb` (u, v = uv0; no texture read). The mesh `c6_crescent` (82 verts) has uv.x along the arc and
uv.y across, vertex alpha 0 on its inner edge.

**The page part.**
- `api.shader("shader:TTO/Bison/EnergyArc", d => ...)`: a `ShaderMaterial` as `tto_sheep.js`'s `additive()` (its VERT
  already does `color x uTint`, with `uTint = 2 x tint`), fragment as above with `ADD_OUT`.
- `api.part("Bison_c6Arc", ...)`: first update: the node's StaticMesh (`node.userData.fxStatic`, `mesh.js`), its own
  material clone (the property block: one per renderer), and with hug its geometry's flat positions kept (mesh.js builds
  one geometry per spawn, so it may be rewritten in place). Each frame as Update: `mesh.visible`, `node.scale`,
  `node.quaternion` (Unity's Euler y: inside the mirror Unity's numbers apply as they are), the clone's `uTint` (the
  0.5-scaled colour; the shader doubles it), and for hug the drape: `fx.uMatrix(node)` to the Unity world, `y = 0 +
  0.25` (the page's `Ground`: `groundhug.js:62-63`, the floor y 0 when within the 12 m up / 24 m down span, else the
  reference height), back through its inverse; `position.needsUpdate`.
- `dispose()`: the clone.

### 9. Bison_row6Fx: `unchainedFury_chains` (`fxparts/tto_bison.js`)

**Fields** (`dump.cs` `Bison_row6Fx`): spin, tightenFrom, tightenTime, tremble, pulse, strainTime, bob, bobRate.
Instances (`tto_scripts.txt`): Ring0 / Ring1 / Ring2 (spin 30 / -30 / 30, tightenFrom 1.7 / 1.85 / 2.0, tightenTime 0.1 /
0.13 / 0.16, tremble 7, pulse 0.05, strainTime 0.62, bob 0) and Mark (spin -40, tightenFrom 1, tightenTime 0.12, no
tremble or pulse, strainTime 0.6). The chains (`bisonRow6_chain` StaticMesh, `tto_c6_chainCopper` opaque +
`tto_bsnRow6_chainGlow` add) and the sigil quads hang under them.

**What it does in TTO.** `Awake@0x1B9CDE0`: base scale, position, rotation kept; `seed = Random.value x 100`.
`OnEnable@0x1B9CE90`: `t0 = Time.time`. `Update@0x1B9CEB0`, `t = Time.time - t0`:
- `e = 1 - (1 - clamp01(t / tightenTime))^2` (1 when tightenTime <= 0); `s = clamp01(t / strainTime)^2` (0 when
  strainTime <= 0);
- `localScale = baseScale x (1 + sin(47 t + seed) x s x pulse) x lerp(tightenFrom, 1, e)`: the ring closes in from
  1.7-2x and starts to throb as the strain builds;
- `localRotation = baseRot x Euler(0, spin x t, 0) x Euler(sin(61 t + seed) x s x tremble, 0, sin(53 t + 2 seed) x s x
  tremble)` (the products' order read from the quaternion arithmetic);
- `localPosition = basePos + (bob != 0 ? sin(bobRate x t + seed) x bob x up : 0)`.

**The page part (about 20 lines).** The same on the node (Unity's numbers inside the mirror), own clock, `seed` drawn at
build.

### 10. TTO/Bison/MoltenCrust, GroundConformParticles, SKILL_FX (`tto_bison.js`, `wardrobe_fx_tto.py`)

- **MoltenCrust** (`dxbc_MoltenCrust.txt`; Magma Quake's PoolPop / PoolHold / PoolFade, material `tto_c6_moltenCrust`,
  texture `tto_mq_lavaPool`, `_TintColor` (1, 1, 1, 1)): Blend SrcAlpha OneMinusSrcAlpha, ZWrite Off, Cull Off. Vertex:
  `vcol x _TintColor` (not doubled), uv0, the world position. Fragment, `T = _Time.y`, `n(p)` = value noise with
  `hash(p) = fract(sin(dot(p, (127.1, 311.7))) x 43758.5453)` and smoothstep blending:
  `n1 = n(3.1 x world.xz - (0.16 T, 0))`, `n2 = n(0.7 x world.xz + (0.28 T, -0.15 T))`; `m = 0.7 n2 + 0.3 n1`;
  `base = m x (0.55, 0.32, 0.026) + (0.45, 0.04, 0.009)`; `glow = clamp01(1.65 n1 n2)^3`; `tex` = the texture;
  `crust = S(clamp01((tex.r - 1.25 max(tex.g, tex.b) - 0.07) x 2.857143))`; `hot = S(clamp01((tex.r - 0.38) x
  2.380952)) x crust`; `lava = hot x (0.7, 0.42, 0.13) x glow + base`; `rgb = mix(tex.rgb x (0.7, 0.78, 0.87), lava,
  crust) x vcol.rgb`; the ragged rim: `e = 0.91 + 0.035 n(36 uv)`, `r = |2 uv - 1|`, `alpha = tex.a x vcol.a x (1 -
  S(clamp01((r - e) / (0.995 - e))))`. Page: `api.shader("shader:TTO/Bison/MoltenCrust", ...)`, a ShaderMaterial with
  `vertexColors`, normal blending, the world position from `modelMatrix` in Unity's space (the mirror flips x: use
  `fx`-independent world xz, the noise only needs a stable field), `uTime` as `tto_sheep.js`'s `time`.
- **GroundConformParticles** (radius / spacing / maxStep; 5 roots): `Sample@0x2260bf0` keeps `origin =
  transform.position` and an n x n grid of `GroundHugEmitter.Ground` heights around it; `LateUpdate@0x2260850`, for
  every World-space system under it (`simulationSpace == 1`), adds `GroundAt(x, z) - origin.y` (`GroundAt@0x2260680`:
  the grid bilinear, origin.y outside it) to each **newborn** particle's y (age under one frame; every particle on the
  first frame), when the difference is over 0.01. On the page's flat floor `Ground` is 0 everywhere, so with the effect
  spawned on the floor (y 0) the shift is 0: **no part needed**. (Spawned above the floor, it would drop new particles
  to y 0: a 10-line part if a cue ever does that.)
- **`SKILL_FX["bison"]`** (`wardrobe_fx_tto.py:76`, its owner): `magmaQuake_magmaField`, `_quakeField`, `_magmaTick`,
  `_quakeTick`, `_magmaSlam`, `_quakeSlam` (`TTO1102:Bison.<RPC_magmaQuake>d__234::MoveNext@0x1B69E50`,
  `<MagmaQuakeTicks>d__239::MoveNext@0x1B5C3A0`, `Bison::MagmaQuakeImpact`); `titanDrop_takeoff`, `_dive`, `_mark`,
  `_charge` (on `HandMount_R`, `Bison::TitanDropCharge`), `_slam1`, `_slam2`, `_slam3` (`<RPC_titanDrop>d__281::MoveNext
  @0x1B78BD0`, `<TitanDropRings>d__289`: `"titanDrop_slam"` + a number; the bare name is not in the catalog,
  `catalog_keys.txt`); `unchainedFury_break`, `_chains`, `_plant`, `_roar` (`<RPC_unchainedFury>d__278::MoveNext`).
  `magmaQuake`, `magmaQuakeAxe`, `titanDrop`, `unchainedFury` are **clips** (`heroes/bison/animations/`), not effects.
  Their sounds: `MagmaPit`, `titanQuake_ring`, `titanQuake_hit`, `break`, `gadina_planetBreaker` are not under the rip's
  `Resources` (only `Assets/AudioClip/`), so the TTO bundle's own clip is used (the tool's fallback); the rest are BB's.
- **AudioControl** on every TTO sound node: the Bat's `audiocontrol.js` (its part 5; TTO has BB's six floats, e.g.
  `Sound_MagmaPit` 0 / 1 / delay 0 / in 0.4 / middle 4.6 / out 1.0), needs no Bison change.

## Interfaces (fixed up front, so the builders run in parallel)

1. **Cue `bone` + `rot`** (lead, `index.html:3926`, :3985): with both, `rot` is the localRotation under the bone (part 6).
2. **A `"look"` cue kind** (lead, beside `"skin"`, `index.html:4513`): `{ grow, tint }` on the hero, cut by the cue's
   `kill`, ended by a new pick (part 6, question 1). Only if the user says yes.
3. **One per-renderer material copy, shared by the parts on a node** (alphatimer.js, uvscroll.js, and any later part that
   needs `renderer.material`): the first part to need it clones `mesh.material[0]` with its other passes (part 2), writes
   them back and sets `mesh.userData.fxOwn = true`; a part that finds the flag uses the materials there. The clone that
   made it frees it when its effect is gone (alphatimer's `owned` list). UVScroll additionally clones the copy's `map`
   (once: `mesh.userData.fxOwnMap`).
4. **shuriken.js takes the renderer's own first material** when the data has it (part 5).
5. **The Bat's, unchanged:** `particles.js` (AdditiveOffset for `nAttack_hit` / `knockDown_hit`), `audiocontrol.js` +
   `fx.sounds` (TTO's 15 sound nodes), mesh.js Opaque1 both passes. If the Bison is built before the Bat, these come
   first; nothing in the Bison changes their spec.
6. **Extractors** (lead): LAYOUTS and the `rim` colour (above), `SHURIKEN_FROM_TTO` (part 5), `EXTRA_FOLDERS["bison"]`
   and the Blood Carnage voice alias only if a tile plays it; `wardrobe_fx_tto.py`'s owner: `SKILL_FX["bison"]`,
   `SHADER_BLEND` Multiply (Double).

## Rank by value (effects made right / effort)

| rank | part | Bison effects | other classes | work |
|---|---|---|---|---|
| 1 | AdditiveOffset (the Bat's particles.js) | `nAttack_hit`: every Combo and Charge Attack hit; `knockDown_hit` | Wolf bladeFang_hit ..., Penguin nAttack_hit (33 materials) | the Bat's ~10 lines |
| 2 | UVScroll layout + part + shared copy | aspect_slam, aspect_trample (unbuildable today) | Cat deltaStrike, Whale bowlingWhale | 3 + ~25 + ~5 lines |
| 3 | Bison_earthRupture | earthRupture (x3) | 0 | ~15 lines |
| 4 | AlphaTimer on Opaque1 (both passes) | earthSmasher, massStun | Bat guardian wings (if driven), Cat supportFire_cannon | ~10 lines |
| 5 | Bison_c6Arc + EnergyArc | 13 TTO prefabs (every released TTO skill) | 0 | ~45 lines |
| 6 | AudioControl (the Bat's) | 15 TTO sound nodes | Bat, Mole, Monkey, Panda, Whale | the Bat's ~25 lines |
| 7 | bone + rot | overPower_horn2 | 0 | ~3 lines |
| 8 | MoltenCrust | magmaQuake_magmaField's pool | 0 | ~40 lines |
| 9 | Bison_row6Fx | unchainedFury_chains | 0 | ~20 lines |
| 10 | Shuriken graft + shuriken.js material | magmaClutter_ring2's puffs | 0 | ~25 + 2 lines |
| 11 | hero look (grow + tint) | Enrage, Titan Form | Wolf Lunar Eclipse's black tint, Penguin multiCast (left out, decision 10) | ~40 lines |
| 12 | Velvet | perfectArmor (never cued) | Shade1-5 and sea creatures' materials (not heroes) | ~15 lines |

After all: `BUILT` in `pipeline/wardrobe_fx_inventory.py` += `UVScroll`, `Bison_earthRupture`, `Bison_overLord`,
`ParticleSystem` / `ParticleSystemRenderer` only if the graft is made generic (else the inventory keeps magmaClutter_ring2
"needing" them: say so in its comment); run it again (the recipe's rule).

## Who builds what (never two owners for one file; as `plans/fx_wolf/build_rules.md`)

| agent | owns | builds |
|---|---|---|
| A: bison | `wardrobe/fxparts/bison.js` (new), `wardrobe/fxparts/uvscroll.js` (new) | Bison_earthRupture; UVScroll (Interfaces 3) |
| B: timer | `wardrobe/fxparts/alphatimer.js` | Opaque1 / Opaque2, both passes, the shared copy (Interfaces 3) |
| C: tto | `wardrobe/fxparts/tto_bison.js` (new), `pipeline/wardrobe_fx_tto.py`, `wardrobe/fxparts/shuriken.js` | Bison_c6Arc, Bison_row6Fx, EnergyArc, MoltenCrust; SKILL_FX / SHADER_BLEND; Interfaces 4 |
| D: mesh | `wardrobe/fxparts/mesh.js` | Velvet (only if question 6 says build it; the Bat's Opaque1 change is the same owner's) |
| lead | `wardrobe/index.html`, `pipeline/wardrobe_fx.py`, `pipeline/wardrobe_fx_inventory.py`, `wardrobe/fx_cues/bison.json` | Interfaces 1, 2, 6; `FX_PART_FILES += "bison", "uvscroll", "tto_bison"` (and the Bat's if not there yet); `BUILT`; the rebuild and the cues |

Rules as the Penguin's: `node --check`, no browser for the builders, never `wardrobe_fx.py bison` /
`wardrobe_fx_tto.py bison` without `--probe` (the lead rebuilds once). If the Bat's builders run at the same time,
`shuriken.js`, `mesh.js` and `wardrobe_fx_tto.py` must keep one owner across both classes.

## Paste-ready cue fragments (for the skill reports' entries; times from the sources cited)

Each is the part-dependent shape; the skill reports own the full timelines (voices, rings, `cut`), and their numbers win
where they traced further.

```json
  "earthRupture": {
    "why": "RPC_earthRupture: clip at 0 (Bison.cs:28739), voice earthRupture1 / 2 by Random.Range(0, 2) (:28780-28835), earthRupture_ring at the hero (:28854-28864, followState), Yield 0.8 (:28899); case 2: RPC_earthRupture_fire2 (max rank 2) from hero + TransformDirection(0, 0.2, 0.4) (:28634), three ruptures at LookRotation x Euler(0, 25 i, 0), i = -1..1 (:8877), life 2 (:8892), 12 m/s straight (Bison_earthRupture.cs:119, fxparts/bison.js); Yield 0.7 (:28891), standby at 1.5 s (:28669)",
    "cues": [
    [0, "voice", "earthRupture1|earthRupture2"],
    [0, "fx", "earthRupture_ring", {"cut": 1.5}],
    [0.8, "fx", "earthRupture", {"d": 0.4, "y": 0.2, "rot": [0, -25, 0]}],
    [0.8, "fx", "earthRupture", {"d": 0.4, "y": 0.2}],
    [0.8, "fx", "earthRupture", {"d": 0.4, "y": 0.2, "rot": [0, 25, 0]}]
    ]
  }
```

Status looks (their spawn time = the skill's `RPC_AddStatus`, the skill reports'):
- Over Power (rank 2, `chaAdjust(9)` = 9 s, Bible `bison-skill-reference.md:118`): `[t, "fx", "overPower_horn2", {"bone":
  "Head", "rot": [-90, 0, 0], "kill": 9}]` (`CharacterControl.cs:35010-35022`), `[t, "fx", "overPower_ring", {"kill":
  9}]` (:35028-35034).
- Fury Trance 3 (`chaAdjust(12)`, cut at 10): `[t, "fx", "furyTrance3", {"bone": "Neck", "kill": 10}]` (:34963-34982).
- Berserker Rush (rank 4 + Rage Control: `chaAdjust(6)` = 6 s, `Bison.cs:7821-7824`): `[t, "fx", "berserkerRush_ring"]`
  (:34876, EffectControl life 1 + 0), `[t, "fx", "berserkerRush", {"bone": "HandMount_L", "kill": 6}]`, `[t, "fx",
  "berserkerRush", {"bone": "HandMount_R", "kill": 6}]` (:34888-34932).
- Iron / Diamond Shield (`chaAdjust(6)`): `[t, "fx", "ironShield", {"kill": 6}]` / `"diamondShield"` (:35064, :35095).
- Titan Form (rank 2, 60 s, cut at 10): `[t, "fx", "titanForm", {"kill": 10, "scale": 1.8}]` (:35243-35262; the scale
  only with the hero look, question 1), and with a yes `[t, "look", "titanForm", {"grow": 1.8, "tint": [0.70, 0.81,
  1.16], "kill": 10}]`.
- Enrage (with a yes): `[t, "look", "enrage", {"grow": 1.25, "tint": [1.22, 0.64, 0.64], "kill": 10}]` (sLv 5 with Rage
  Control; question 2).
- Hold Charge (`CharacterControl.cs:34666-34692`): `[t, "fx", "holdCharge_ring"]`, `[t, "fx", "holdCharge", {"kill":
  <the status time>}]` (EffectControl life 60).

## How sure I am

| item | sure | why |
|---|---|---|
| UVScroll layout and behaviour | high | two public floats, 8 bytes on all three; Update is two lines |
| AlphaTimer misses Opaque1, and the second pass | high | `OPACITY` and `own()` read directly; `withMaterials` flattens the passes |
| Bison_earthRupture: straight 12 m/s, 2 s, pierces | high | FixedUpdate / OnCollisionEnter read in full; life 2 at both fire sites |
| The status looks' bones, rotation, scales, tints | high | bare literals in `addStatus` / `removeStatus` |
| No code adds perfectShield / perfectArmor | high | grep of all BB sources and TTO's pseudo-C |
| Bison_c6Arc / Bison_row6Fx formulas | medium-high | annotated pseudo-C, constants resolved; the quaternion product order derived by hand |
| EnergyArc / MoltenCrust | medium-high | D3D11 disassembly read by hand; fog variants ignored |
| GroundConformParticles a no-op on the page | medium-high | disassembly: newborn particles shifted by ground - origin.y; the page's floor is flat |
| The Shuriken graft draws the game's puffs | medium | TTO's copy is BB's prefab re-imported (as the time weapons); not compared with BB's 3.5 bytes |
| Velvet's maths | high | the compiled ARB fragment program |

## Open questions (with my recommended answer)

1. **Enrage's and Titan Form's body**: the game grows the Bison (1.2-1.25x, Titan Form **1.8x**) and tints him (red /
   blue). The Penguin's Double Spell tint was left out (its decision 10), but here the growth is the skill's whole look
   (Titan Form's prefab is one ground ring). Recommended: **build the `"look"` cue (grow + tint), cut at 10 s**, and check
   the 1.8x Bison against the camera's framing by screenshot.
2. **Rage Control (#402) on Enrage**: the passive adds a level (sLv 5: +0.25 scale, colour (1.05, 0.55, 0.55)) and
   Berserker Rush's (+1, 6 s). Recommended: **on** (max ranks with every passive learned, as the Sheep's Benediction in
   its decision 8).
3. **magmaClutter_ring2's puffs**: graft TTO's decoded Shuriken onto BB's effect (part 5), or leave the puffs out.
   Recommended: **graft** (the same source the time weapons already use).
4. **UVScroll's phase**: the game scrolls by its absolute clock. Recommended: **the page's absolute clock** (the two
   Trample hordes in step, as in the game).
5. **Blood Carnage on the Bison**: only if a skill report gives it a tile; then `EXTRA_FOLDERS` + the Bat voice alias.
   Recommended: **follow the Bat's decision on the shared skill** (one tile per class that has it, same files).
6. **Velvet / perfectArmor**: no game code ever shows it. Recommended: **don't build it now** (rank 12); note it in the
   inventory as unreachable.
7. **Effects parented to a grown hero** (titanForm's ring under a 1.8x Bison): recommended the cue's `scale` in that tile
   only (Titan Form's own), not a general follow-the-hero's-scale rule.

## Verification

Read-only check, 2026-11-13 (home PC), against BB `DecompiledSource`, TTO1102 (pseudo-C, `dump.cs`, capstone), the
probes in `checks/fx_bison_research/parts/` and `.../tto/`, and the page code. My own probes are in
`checks/fx_bison_research/verify_tto_parts/`. The LAYOUTS block, the Earth Rupture block and the status-look fragments are
correct. The corrections are counts, one missing prefab, and one AudioControl rule.

**Confirmed against the source**
- UVScroll:
  - Source: `UVScroll.cs:26` / `:29` set the defaults 0.1 / 0.1, `:42-46` is Update (Repeat(Time.time x s, 100) ->
    `renderer.material.SetTextureOffset`), and `:67` / `:70` declare the two floats.
  - Probe: every instance is 8 bytes, with the words (0.2, -0.2).
  - Build: `wardrobe_fx.py:293-294` raises "no layout" whenever a script has field bytes. So `aspect_slam` and
    `aspect_trample` cannot be built today.
  - `Bison_earthRupture` and `Bison_overLord` have 0 bytes. They do not raise; their `[]` layouts only serve the
    inventory. The LAYOUTS format matches the file's.
- The inventory has 46 Bison entries.
- Status looks in BB `CharacterControl.cs`: holdCharge `:34670` / `:34673` / `:34692`; berserkerRush `:34876`, `:34888`,
  `:34907` (HandMount_L), `:34932` (HandMount_R); furyTrance `:34963` / `:34982` (Neck); overPower_horn `:35010` (+ sLv),
  `:35016` (Head), `:35022` (Euler(-90, 0, 0)); overPower_ring `:35028` / `:35034`; ironShield `:35064`; diamondShield
  `:35095`; perfectShield `:35129`; perfectArmor `:35164`; titanForm `:35209`, `:35219`, `:35243`, `:35262`; mColor 0.86
  at `:15153`.
- Recomputed grow and tint: Enrage 5 gives 1.25 and (1.05, 0.55, 0.55) / 0.86 = (1.22, 0.64, 0.64); Titan Form 2 gives
  1.8 and (0.70, 0.81, 1.16).
- No `AddStatus("perfectShield")` or `AddStatus("perfectArmor")` call exists in BB.
- The page:
  - `index.html:3985-3990`: `bone` replaces the root's quaternion, so the cue's `rot` is lost.
  - `alphatimer.js:27`: `OPACITY` holds add / alpha / Phoenix only.
  - `own()` clones `material[0]` only.
  - `shuriken.js:300-302` reads `rd.mats || rd.materials`, while TTO renderer dicts carry `m_Materials`. So the 2-line
    change is needed as written.
- Earth Rupture:
  - Every line cited checks out: clip `:28739`; `Random.Range(0, 2)` at `:28780`, voices `:28792` / `:28804` and
    `:28823` / `:28835`; ring `createEffect` at `:28864`.
  - The ring is `earthRupture_ring`, EffectControl 2 + 2, followPosition and followState (`summary.txt`).
  - Yield 0.8 (`:28899`) leads to case 2, `fire2` (`:28634`). Yield 0.7 (`:28891`) leads to standby (`:28669`) at 1.5 s.
  - `fire2` is at `:8829`: z euler 0 at `:8862`, `Euler(0, 25 i, 0)` for i = -1..1 at `:8877`, life 2 at `:8892`.
  - `Bison_earthRupture.cs` sets velocity = TransformDirection(velocity) every FixedUpdate and Destroys at life.
    OnCollisionEnter ignores the collider and hits, with no Destroy. The probe's velocity is (0, 0, 12).
  - The block's format is valid.
- Status durations: Berserker Rush 4 + 1 with `chaAdjust(3 + 3)` = 6 s (Bible `:276`, `Bison.cs:7821-7824`); Over Power
  9 s; Fury Trance `chaAdjust(12)`; Iron / Diamond Shield 6 s; Titan Form 60 s.
- `Bison_c6Arc::Update@0x1B9BDF0`: the scale, the rotation Euler(0, angle + spin x t) with t not wrapped, the tint lerp
  toward (1, 0.38, 0.08) by clamp01(0.45 k), alpha 0.75 (1 - S(k)) S(k / 0.08) c.a, and the 0.5 factor all match.
- `Bison_row6Fx::Update@0x1B9CEB0` matches; the quaternion arithmetic gives the product order base x spin x tremble.
- EnergyArc `ps_4_0`: alpha = S(10 u) (1 - S(10 (u - 0.9))) v vcol.a, and rgb = vcol.rgb.
- Not re-derived beyond the cited lines: AlphaTimer on Opaque1, Velvet, MoltenCrust, the Shuriken graft. I also checked
  `mesh.js:127-134` and `:200-210`.

**Corrections**
1. **Counts.** These affect "Read this first" 6, the blocked set, parts 8 and 10, rank rows 5 / 6, and Interfaces 5.
   - **AudioControl is on 18 TTO sound nodes in 13 prefabs**, not 15. Per prefab: chains 1, break 2, roar 1, plant 1,
     takeoff 2, charge 1, dive 1, slam1-3 2 each, magmaField 1, quakeField 1, quakeSlam 1 (`tto/scripts.txt`).
   - **GroundConformParticles is on 6 roots**, not 5: all six magmaQuake prefabs (magmaTick, quakeTick, magmaField,
     quakeField, magmaSlam, quakeSlam).
   - **Bison_c6Arc is in 11 of the 17 skill prefabs** (42 arcs), not 13. With the status look `unchained` it is 12.
2. **A missing prefab: `tto/unchained`.** This is Unchained Fury's 3 s status look, made by
   `CharacterControl::AddUnchainedFx@0x24AEB60` (see tto.md, "Read this first" 2). It appears nowhere in this report.
   - It has 2 `Bison_row6Fx`: node 1 has spin 50, tightenTime 0.12, strainTime 0.6; node 5, the orbit, has spin 120,
     **bob 0.08, bobRate 3**.
   - It has 2 `Bison_c6Arc`: duration 0.9, diameter 3.6, **repeat true**, colour (0.85, 0.09, 0.045, 0.65), hug.
   - It has no EffectControl and no sound (`tto/probe_unchained.json`).
   - It belongs in the blocked set, needing Bison_row6Fx + Bison_c6Arc + EnergyArc.
   - Part 9 must cover it. The bob term is used here: localPosition = base + up x 0.08 x sin(3 t + seed).
   - It belongs in rank rows 5 and 9.
   - It belongs in `SKILL_FX["bison"]`, as the Wolf's list carries its status look `windBound`
     (`wardrobe_fx_tto.py:77-86`).
3. **Part 8:** "Every instance: ... repeat false" is wrong, because `unchained`'s two arcs are repeat true. The diameters
   run 3.1 (the roar spirals) to 60, not 4 to 60.
4. **AudioControl (part 10, Interfaces 5).** "needs no Bison change" is wrong; it needs one rule.
   - `TTO1102:AudioControl::Start@0x2298D00` stops a source with delay > 0. `Update@0x2298E70` calls `Play` only inside
     the fade-in branch (fadein > 0, `0x2298EA7-0x2298F62`); with fadein 0 it jumps to `0x2298F69`, which only sets the
     volume. BB's `AudioControl.cs` Update matches once its predicates are worked out.
   - So `Sound_overSwing` (titanDrop_takeoff, delay 0.05, fadein 0) and `Sound_earthSmasher_ring` (titanDrop_slam2, delay
     0.2, fadein 0) are **silent in the game**.
   - The Bat's part ("at t >= delay start a new one", `plans/fx_bat/parts.md` part 5) would play them. It should start a
     delayed source only when fadein > 0, inside its fade-in window.
   - The Bat's own nefariousWhip_hit has fadein 0.5, so it is unaffected.
5. **Part 10, sounds not under the rip's `Resources`:** add `earthSmasher_ring` (titanDrop_slam2's). That makes six:
   MagmaPit, titanQuake_ring, titanQuake_hit, break, gadina_planetBreaker, earthSmasher_ring. After correction 4 it is
   never heard anyway.
6. **LAYOUTS placement:** "after the Bat's block" doesn't work yet, because `pipeline/wardrobe_fx.py` has no Bat block.
   The last block is the Mana Vortex one (`:124-129`). Put it after whichever block is last.

**Corrected paste-ready pieces.** The LAYOUTS block, the `earthRupture` entry and the status-look fragments are
unchanged. The `SKILL_FX["bison"]` list (part 10) becomes:

```python
    "bison": [
        # Magma Quake: TTO1102:Bison.<RPC_magmaQuake>d__234::MoveNext@0x1B69E50, <MagmaQuakeTicks>d__239@0x1B5C3A0,
        # Bison::MagmaQuakeImpact@0x1B41710
        "magmaQuake_magmaField", "magmaQuake_quakeField", "magmaQuake_magmaTick", "magmaQuake_quakeTick",
        "magmaQuake_magmaSlam", "magmaQuake_quakeSlam",
        # Titan Drop: <RPC_titanDrop>d__281::MoveNext@0x1B78BD0, Bison::TitanDropCharge@0x1B46C50, <TitanDropRings>d__289@0x1BA91D0
        "titanDrop_takeoff", "titanDrop_mark", "titanDrop_charge", "titanDrop_dive",
        "titanDrop_slam1", "titanDrop_slam2", "titanDrop_slam3",
        # Unchained Fury: <RPC_unchainedFury>d__278::MoveNext@0x1B7BFC0 (+ CharacterControl::AddUnchainedFx@0x24AEB60, the status look)
        "unchainedFury_chains", "unchainedFury_break", "unchainedFury_roar", "unchainedFury_plant", "unchained",
    ],
```

The blocked-set rows become:

| effect | skill (spawn) | missing part(s) | where |
|---|---|---|---|
| TTO: 12 prefabs with crescents (11 skill prefabs + `unchained`) | Magma Quake, Titan Drop, Unchained Fury | Bison_c6Arc (incl. `repeat`) + EnergyArc | the prefabs' own |
| TTO `unchainedFury_chains`, `unchained` | Unchained Fury | Bison_row6Fx (incl. `bob`) | the hero |
| TTO, 18 sound nodes (13 prefabs) | all three | AudioControl (delayed start only inside a fade-in) | - |
