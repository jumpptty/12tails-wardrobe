# Wolf effects: the parts the page cannot draw yet

Research 2026-11-09 (one of six Wolf fx researchers; scope: the missing parts). Read-only: the probes are in
`checks/fx_wolf_research/parts/` (`probe.py` every node and component of the 21 effects, `probe2.py` clips, `probe3.py`
meshes and materials, `probe4.py` the mirror's shader, `scan_all.py` the new layouts across every class). Their output
is in the `.txt` files next to them. Nothing in `wardrobe/data` was written.

## Why the page can't draw them yet (the short answer)

None of the 21 is out of reach. The parts just haven't been built yet, and each one is missing in two places:

1. **The extractor** (`pipeline/wardrobe_fx.py`). The game's own scripts (VortexEmitter, EmblemEmitter, TrailEmitter,
   EmitterControl, ShatterMesh) store their settings as raw bytes, and `LAYOUTS` has no entry for them yet, so
   `effect()` raises on them ("no layout for VortexEmitter (164 field bytes)"). The Unity built-ins (Animation,
   SkinnedMeshRenderer, a MeshFilter mesh, TrailRenderer, Light) are skipped without a word: `effect()` only reads
   Transform, MeshRenderer / ParticleRenderer materials, the legacy particles and AudioSource.
2. **The page** (`wardrobe/index.html`, `class Fx`). The page only draws `ringEmitter`, `imageEmitter`, `lineEmitter`
   and `legacyParticles`. It reads only the root's EffectControl (`n.parent < 0`, index.html:2966), and nothing on the
   page plays an effect's own animation or draws a mesh.

This research proves all five script layouts below on the real bytes: every instance in every class decodes and uses up
exactly its bytes (VortexEmitter 31, EmblemEmitter 24, EmitterControl 32, ShatterMesh 5, TrailEmitter 22; no failures).
The built-ins are read through the type tree (no byte work), and the repo already has the code to convert meshes and
clips (`wardrobe_data.py` `mesh_block` / `clip_dict`; on the page `hermite()`, `finishProp` skin binding).

## The Wolf's set (from `plans/fx_inventory.md`, checked against the prefabs)

The Wolf needs **no BoltEmitter**. Spawn sites are `Wolf.cs` lines. "Target" means the game spawns the effect on the
enemy or ally that was hit. The pilot's rule leaves those out (the wardrobe has no target).

| effect | skill (RPC) | missing parts | spawned |
|---|---|---|---|
| `artbreaker_ring` | Art Breaker (`RPC_artBreaker`, :34303) | EmitterControl | hero |
| `cattack2` | Charge Attack (`RPC_cAttack2`, :19415, Instantiate) | EffectControl(child) | hero |
| `skyslasher` | Sky Slasher (`RPC_skySlasher`, :31709, Instantiate) | EffectControl(child) | hero |
| `darkedge_ring` | Dark Edge (`RPC_darkEdge`, :30743) | VortexEmitter | hero |
| `dualbrand_slash3` | Dual Brand (`RPC_dualBrand`, :36274) | VortexEmitter, EffectControl(child) | hero |
| `dualbrand_slash1` / `2` / `4` | Dual Brand (:35959 / :36119 / :36424) | Animation, TrailEmitter | hero |
| `holysword_ring` | Holy Sword (`RPC_holySword`, :33218) | EmblemEmitter | hero |
| `holyarmor_ring` | Holy Armor (`RPC_holyArmor`, :33733) | EmblemEmitter | hero |
| `resurrection_ring` | Mass Resurrection (`RPC_massResurrection`, :25400) | EmblemEmitter | hero |
| `resurrection_hit` | Mass Resurrection (:25126) | EmblemEmitter | **target** (each revived ally) |
| `bladefang_underslash` / `upperslash` | Blade Fang (`RPC_bladeFang`, :25670 / :25883, again :26124) | Animation, SkinnedMeshRenderer | hero, rotation × Euler(270, 90, 0) |
| `bloodfang_underslash` / `upperslash` | Blade Fang with the Blood Fang passive (`hasSkill(403)`, :25707 / :25918 / :26159) | Animation, SkinnedMeshRenderer | hero, × Euler(270, 90, 0) |
| `crusader` | Crusader (`RPC_crusader`, :21097) | Animation, TrailRenderer | hero, × Euler(270, 90, 0) |
| `lawbringer` | Crusader with the Law Bringer passive (`getLawBringerLv() > 0`, :21060) | Animation, TrailRenderer | hero, × Euler(270, 90, 0) |
| `crusader_hit` / `lawbringer_hit` | Crusader's hit (`RPC_crusader_hit`, :8440-8510, `Instantiate(.., hitPos, ..)`) | Light | **target** |
| `mirrorblade_mirror` | Mirror Blade (`RPC_mirrorBlade`, :34574) | ShatterMesh, StaticMesh | hero |

Three things follow from this table:

- **Light is needed only by the two Crusader hits, which spawn on the target.** Under the pilot's rule they are left out
  anyway. Light can be skipped for the Wolf.
- **A cue needs a spawn rotation** for the six `× Euler(270, 90, 0)` effects (`createEffect(fx, pos, rotation *
  Quaternion.Euler(270, 90, 0))`). Today a cue carries only a distance, and `Fx` gives the root the hero's rotation and
  nothing more. That is a 6th cue value (Unity Euler degrees, built as `THREE.Euler(x, y, z, "YXZ")` in radians, the
  same order `lineEmitter` already uses).
- **Max rank:** Blood Fang and Law Bringer are Class C passives on top of Blade Fang 3 and Crusader 4 (Bible
  `wolf-skill-reference.md:302`, :357). The cue writer picks which version the tile shows. Both versions use the same
  parts.

## Each part

Layouts are written the way `LAYOUTS` expects: f float, i int (and enums), b bool (1 byte, then padded to 4), v3, c
(Color, 16 bytes), r (a PPtr, 8 bytes). Sizes are the field bytes after the MonoBehaviour header.

### EmitterControl: `artbreaker_ring`

What it does (`EmitterControl.cs`). It switches the same node's legacy ParticleEmitter on and off:
- At Start (:38-87): when `Delay > 0`, `emit = false`.
- Every LateUpdate (:91-154), it adds `deltaTime` to a timer:
  - at `timer >= Delay + Life + AfterLife`, it destroys the node;
  - at `>= Delay + Life`, `emit = false`;
  - after `Delay`, `emit = true`.

In `artbreaker_ring` the `ParticleEmitter` node is saved with `emit = False`, oneShot, `Delay 1, Life 3, AfterLife 0`.
The root EffectControl (life 2) removes the whole effect first, so the dust bursts at 1.0 s and is gone at 2.0 s.

```python
"EmitterControl": [("Delay", "f"), ("Life", "f"), ("AfterLife", "f")],          # EmitterControl.cs:175-181, 12 bytes
```

Page: a timer beside `legacyParticles`, plus a `setEmit(on)` next to its existing `stop()`. About 15 lines, 30 min.
`artbreaker_ring` needs nothing else.

### EffectControl(child): `cattack2`, `skyslasher`, `dualbrand_slash3`

The page keeps only the root's EffectControl. A child's EffectControl runs with **no owner**:
`CharacterControl.createEffect` calls `InitEffectControl` on the root's component only (CharacterControl.cs:24211), and
`cAttack2` / `skySlasher` are plain `Instantiate`s anyway.

What a child EffectControl does (`EffectControl.cs`):
- Awake (:69-75) turns `velocity` into a world direction once, and Update moves the node by it each frame (:167-178).
- At `timer >= life + afterLife` it destroys the node (:179-189).
- If `followState` is set and there is no owner, it jumps the timer straight to `life` on the first frame (:194-210).
- In the after-life it stops its own and its children's legacy emitters and ImageEmitters (:419-512).

What that means for the three effects:
- `cAttack2_dust` and skySlasher's `DustEmitter` are `life 60, afterLife 0, followState true`. Frame 1 sets the timer to
  60, and frame 2 destroys the node with its one-shot burst. **In the game these dust puffs live about two frames:
  effectively never seen.** Built faithfully, this part makes the two effects ready, and their dust stays invisible.
- `dualbrand_slash3`'s VortexEmitter node has `velocity (0, 12, 0)`: the vortex rises 12 m/s. The root's life
  0.5 + 0.3 ends it first.

The layout is the existing EffectControl one (32 bytes). Nothing new to decode.

Page: give each node its own `{ec, age}`. Move it by `vel` (Unity world, taken at spawn), stop the emitters under it at
`life`, remove it at `life + afterLife`, and apply the followState-with-no-owner jump. Update the `if (c.type ===
"EffectControl" && n.parent < 0)` branch to match. About 25 lines, 1 h.

### VortexEmitter: `darkedge_ring`, `dualbrand_slash3`

Each frame (`VortexEmitter.cs` LateUpdate :147-753; the mesh is in the node's own space, MeshFilter on the node):
- **Delay:** nothing happens before `Delay` (:155).
- **Pruning:** points older than `Life` are dropped from the old end (:167-189).
- **Spin:** if `Spin` is not zero, the node's world Euler x / y / z is **set** to `57.3 × Time.time × Spin / Life`
  degrees. This uses the absolute clock, not the time since spawn (:190-343). Both Wolf effects have Spin 0.
- **Emission:** while the frame counter is `<= length` (so `length + 1` frames), each frame adds `vortexCount` points
  (:356-429). Point *i* has
  - angle `θ = Rotation × time + i × vortexRadian` (radians);
  - direction `(cos θ − sin θ, 0, sin θ + cos θ)`, which has length √2 (the game's own quirk);
  - a random radius offset `0..rndRadius`;
  - its birth time.
- **End:** once the counter passes `length` and every point has died, the emitter either restarts (`repeatForever`) or
  destroys the node (:430-463).
- **Mesh (:464-735), per point**, with `age = clamp01((now − birth) / Life)`:
  - radius `r = lerp(startRadius, endRadius, age) + rnd`;
  - half-width `hw = 0.5 × lerp(startWidth, endWidth, age)`;
  - drift `b = lerp(0, localVelocity, age)` (the whole drift over life, not a speed);
  - inner vertex `dir × r + b`;
  - outer vertex `dir × (r + hw) + b`, or `dir × r + up × hw + b` with `alwaysUp`;
  - `uv = (age × UVTile, 0 / 1)` (UVTile 0 has a strange `2n / (j + 1)`, not used by the Wolf);
  - colour: the five-key ramp at 0 / .25 / .5 / .75 / 1, the same as the page's `ramp()`;
  - triangles join each point to the one `vortexCount` later, so each arm is a strip (:674-717).
- `VortexEmitterMode` (Stretch / Tile) is saved but never read.

```python
# VortexEmitter.cs:774-837, 164 bytes; VortexEmitterMode (0 Stretch, 1 Tile) is never read; length = frames of emission
"VortexEmitter": [("Life", "f"), ("Delay", "f"), ("startRadius", "f"), ("endRadius", "f"), ("rndRadius", "f"),
                  ("startWidth", "f"), ("endWidth", "f"), ("length", "i"), ("alwaysUp", "b"), ("localVelocity", "v3"),
                  ("Color1", "c"), ("Color2", "c"), ("Color3", "c"), ("Color4", "c"), ("Color5", "c"),
                  ("Rotation", "f"), ("vortexCount", "i"), ("vortexRadian", "f"), ("Spin", "v3"),
                  ("VortexEmitterMode", "i"), ("UVTile", "f"), ("repeatForever", "b")],
```

The Wolf's values:
- `darkEdge_ring`: Life 0.5, radius 0.5 → 1, width 0.5 → 0, length 9, rises 2, Rotation 9, 6 arms 1 rad apart.
- `dualBrand_slash3`: Life 0.3, radius 0, width 0 → 3, length 24, drift −6, Rotation 6, 4 arms 1.5 rad apart.

**One thing the user must pick: the frame rate.** Emission is counted in frames, so the spiral's length and the spacing
of its points depend on the game's fps. BB sets `Application.targetFrameRate = 80` (LoginGui.cs:484), and vSync, if on,
caps that at the monitor's 60. The page should emit on a fixed tick rather than its own frames. Mock 60 and 80 side by
side for the user to pick.

Page: about 60 lines, 2-3 h. It is the biggest part across classes too: 31 effects in 8 classes, 23 of them blocked by
it alone.

### EmblemEmitter: `holysword_ring`, `holyarmor_ring`, `resurrection_ring` (`resurrection_hit`: target)

This is not a 3D emitter. It is a **screen-space GUI picture** (`EmblemEmitter.cs`):
- **Start:** Awake (:82-86) sets `start = now + Delay` and a scale `k = Screen.width / 1024`.
- **Each OnGUI (:90-287), between `start` and `start + Life`:**
  - project the node to the screen, `z` = distance along the camera's view;
  - `alpha` = the five-key ramp of `alpha1..alpha5` at 0 / .25 / .5 / .75 / 1, applied as `GUI.color.a` (white
    otherwise);
  - if `z < 40`, draw `image` centred on the point, `image.width × k × lerp(startWidth, endWidth, u) ×
    clamp(5 / z, 0.2, 1)` pixels wide (height the same with `image.height` and the heights);
  - it draws over everything, the hero included (`GUI.depth 5`).
- **End:** after `start + Life`, it destroys the node (:278).
- `velocity` and `rndScale` are saved but never read.

```python
# EmblemEmitter.cs:308-347, 68 bytes; image = a Texture2D PPtr (resolve with game.obj, export like the materials' textures)
"EmblemEmitter": [("Life", "f"), ("Delay", "f"), ("image", "r"), ("startHeight", "f"), ("endHeight", "f"),
                  ("startWidth", "f"), ("endWidth", "f"), ("rndScale", "f"), ("velocity", "v3"), ("alpha1", "f"),
                  ("alpha2", "f"), ("alpha3", "f"), ("alpha4", "f"), ("alpha5", "f")],
```

The Wolf's images: `holyShield` 256×256, `holySword` 256×256, `resurrection` 454×256 (sizes 0.5 → 0.8, or 0.5 / 0.7 →
0.7 / 1.0; delays 0.2 / 0.4 / 0.9 s).

Extractor: when the script is EmblemEmitter, resolve `image`, add it to `texs` (it goes to `data/fx/tex/`) and store its
name and pixel size. About 8 lines.

Page: a picture laid over the canvas. Either a `THREE.Sprite` with `sizeAttenuation: false`, `depthTest: false` and a
top `renderOrder`, sized from pixels, or an absolutely placed `<img>` over the stage. Use normal alpha blending and the
canvas width in place of `Screen.width`. About 40 lines, 2 h.

### Animation: `bladefang_*` ×2, `bloodfang_*` ×2, `crusader`, `lawbringer`, `dualbrand_slash1` / `2` / `4`

A Unity built-in, read through the type tree. Every Wolf clip is uncompressed (`m_Compressed False`), 30 samples a
second, with Hermite keys (value, inSlope, outSlope) in `m_RotationCurves` / `m_PositionCurves` / `m_ScaleCurves` and no
float curves or events. That is exactly what `wardrobe_data.py clip_dict` already reads.

| effect | clip | animates | span |
|---|---|---|---|
| blade/bloodFang under / upper | `root` | child `root` (rotation, position, scale) and `root/bladeFang1..7` (rotation 6-10 keys, position 2) | 0.3 s |
| crusader, lawBringer | `root` | positions of `crusader_upperSlash` (10 keys), `crusader_sideSlash` (8) | 0.9 s |
| dualBrand_slash1 / 2 / 4 | `root` / `Base Stack` | `SlashN` rotation 15 / 16 / 6, position 13 / 12 / 12, scale 2 | 0.7 / 0.5 / 0.5 s |

The Animation components are `playAutomatically`, with wrap 0 / 1 (Default / Once). The clip plays once from spawn and
the nodes keep their last pose. That matters only for `crusader` (0.9 s clip, life 1.5 s): the trails stop moving and
fade. EffectControl plays a clip named `destroy` at the end of its life (`EffectControl.cs:252-289`), but no Wolf clip
has that name.

Extractor: per Animation, write `{clips: {name: clip_dict(...)}, default, wrap}`:
- keep the keys **unmirrored** (effects stay in Unity space);
- resolve each curve `path` (relative to the Animation's node; Unity's `Find` takes the first child with that name, and
  `dualBrand_slash2` has `Slash2` under `Slash2`) to a node index.

About 40 lines.

Page: sample with the existing `hermite()` into an `AnimationMixer` on the effect's nodes (as `finishProp` does), or set
the poses directly each tick. About 40 lines.

**The whole part, with the cue rotation: 3-4 h.** It unlocks nothing alone. Its value comes with TrailEmitter,
SkinnedMeshRenderer and TrailRenderer below.

### SkinnedMeshRenderer: `bladefang_*` ×2, `bloodfang_*` ×2

What they are: a fan-shaped blade ribbon on the prefab root, skinned to 8 bones (`bladeFang1..7`, `root`), that the clip
opens in 0.3 s.

| mesh | verts | tris | material |
|---|---|---|---|
| `Wolf_bladeFang_tri` | 148 | 128 | `bladeFang_slash`, addsoft |
| `Wolf_bloodFang_tri` | 216 | 272 | `bloodFang_slash`, addsoft, colour 0.78 |

Each has 8 bind poses, normals and UVs. It has **no vertex colours**: the page needs a white colour attribute, since
`fxMaterial` uses vertex colours. `m_RootBone` is null and the AABB is zero.

Extractor: `MeshHandler` reads it as `mesh_block` does: positions, uv, the index list, 4 weights and 4 joints per
vertex, the bind poses. Keep it unmirrored, put the bones as node indices and the materials in `mats`. It is small
enough to inline in fx.json (about 10-15 KB). About 35 lines.

Page: a `THREE.SkinnedMesh` on the node, bound the way `finishProp` binds a prop's skin: `boneInverses = bindpose ×
inverse(mesh world)`, bound at spawn inside the mirror group, double-sided. About 35 lines.

**The whole part: 2-3 h.** With Animation, it unlocks all four.

### TrailEmitter: `dualbrand_slash1` / `2` / `4` (two each: `SlashN` and a child)

The game's own trail (`TrailEmitter.cs`). It draws a ribbon along where its node has been, the node being swung by the
clip.
- **Awake (:83-152):** a quality check (`minQuality`, 0 for the Wolf).
- **Each LateUpdate (:157-761):**
  - **Pruning:** sections older than `life` are dropped (:184-200).
  - **Timer:** with `isTimer`, it emits only from `delay` to `delay + easeIn + easeMiddle` and destroys itself after
    `+ easeOut` (:207-248). The Wolf's are all `false`.
  - **New section:** when the node has moved more than `minDistance` from the newest section (:255-331), it adds one
    with
    - the world position;
    - `upDir` (world up with `alwaysUp`, else the node's own up at that moment);
    - `uv` (its distance along the trail / `uvHeight`);
    - its birth time.
  - **Mesh, built in world space then moved into the node's space (:340-761).** For each section, with `u =
    clamp01(age / life)` (0 for the newest):
    - half-width `hw = 0.5 × lerp(startWidth, endWidth, u)`;
    - vertices `point ∓ upDir × hw + upDir × age × localVelocity + worldUp × age × worldVelocity` (:488-493);
    - `uv = (u × uvHeight, 0 / 1)` in Stretch mode (:498), or `section.uv` in Tile mode (:643);
    - colour: a **four-key** ramp, Color1..4 at 0 / .33 / .66 / 1 (factor 3; :508-534);
    - triangles: one strip (:706-744).
  - Fewer than 2 sections draw nothing.

```python
# TrailEmitter.cs:813-867, 124 bytes; TrailEmitterMode 0 Stretch, 1 Tile
"TrailEmitter": [("startWidth", "f"), ("endWidth", "f"), ("life", "f"), ("alwaysUp", "b"), ("minDistance", "f"),
                 ("Color1", "c"), ("Color2", "c"), ("Color3", "c"), ("Color4", "c"), ("TrailEmitterMode", "i"),
                 ("uvHeight", "f"), ("localVelocity", "f"), ("worldVelocity", "f"), ("isTimer", "b"), ("delay", "f"),
                 ("easeIn", "f"), ("easeMiddle", "f"), ("easeOut", "f"), ("minQuality", "i")],
```

The Wolf's values: width 1 → 3 (2 → 4 on slash4), life 0.4, minDistance 0.01, Stretch, the upDir spread 4 or 6 m/s,
world sink −0.5 (0 on slash4). Materials `dualBrand1` / `dualBrand2`, addsoft.

Page: keep the sections in Unity world space (`fx.uMatrix(node)`, the way `legacyParticles` keeps world particles) and
draw the mesh under `fx.mirror`. About 70 lines, 3 h. With Animation, it unlocks slash1 / 2 / 4. With VortexEmitter
and EffectControl(child) on top, the whole Dual Brand is drawable.

### TrailRenderer: `crusader`, `lawbringer` (on `crusader_upperSlash`, `crusader_sideSlash`)

A Unity built-in (no source; its behaviour is from Unity 3.5's TrailRenderer):
- a new point each time the node moves more than `m_MinVertexDistance`;
- each point lives `m_Time`;
- a ribbon that **faces the camera**, with width going from `m_StartWidth` at the head to `m_EndWidth` at the tail;
- colour through the five `m_Colors` keys along the trail (packed RGBA, as the legacy `colorAnimation` keys the page
  already unpacks);
- the texture stretched along the trail.

The Wolf's values: time 0.3, width 0.4 → 1.0, min distance 0.1, no autodestruct. The materials are `crusader_slash` /
`lawBringer_slash` (addsoft): white fading to gold, or to blue for Law Bringer. Each slash node also carries a looping
legacy "Particle System", which the page already draws.

Extractor: read these six fields and the material (add `TrailRenderer` to the renderers whose `m_Materials` are read).
About 10 lines.

Page: like TrailEmitter, but the width direction is `cross(segment, view)`. About 60 lines.

**The whole part: 2-3 h.** With Animation, it unlocks both, so Crusader is drawable (its hits stay out).

### StaticMesh + ShatterMesh: `mirrorblade_mirror` (node `mirror_tri`)

**StaticMesh** is a MeshFilter mesh drawn by a MeshRenderer with no emitter. Here it is `mirror_tri`: 70 verts, 96
tris, normals and UVs, no colours. It is a pane about 1.3 m wide, 0.2-2.0 m high, 1.25 m in front.

Its material uses the game's own shader **`FX/DistortGlass`**. That shader takes a GrabPass of the screen and multiplies
it by `_MainTex`, shifted by a constant 32 texels. Its fallback SubShader is `Blend DstColor Zero` × texture: a
**multiply**. On the page, a `CustomBlending` with `DstColorFactor` / `ZeroFactor` (or `MultiplyBlending`) matches the
fallback.

**Caveat:** the wardrobe's canvas is transparent over the stage colour. A multiply onto empty canvas gives 0, so the
mirror would only show where it covers the hero. Showing it over the backdrop needs a backdrop to multiply (for
example, the stage colour as a constant). This is worth mocking for the user.

Extractor: MeshFilter → mesh (MeshHandler: pos, uv, normals, idx). About 15 lines. Page: a plain `THREE.Mesh` with that
material. About 25 lines.

**ShatterMesh** (`ShatterMesh.cs`) breaks the pane apart. Each LateUpdate (:53-165):
- **Before `Delay`:** nothing.
- **Then, on the first frame:** `CreateClone` (:169-397) splits the mesh so every triangle has its own 3 vertices. Each
  triangle gets a velocity:
  - its face normal (`normalize(cross(b − a, c − a))`), multiplied axis by axis by `localVelocity`;
  - plus, per axis with `rndVelocity > 0`, `Random.Range(−r, r + 1)` (the +1 bias is the game's);
  - plus `worldVelocity`.
  All of it is in the mesh's local space.
- **Until `Delay + Life`:** each vertex = original + `lerp(0, velocity, clamp01((t − Delay) / Life))` (the whole
  velocity is the total travel).
- **After that:** frozen.
- `rndRotation` is never read.

```python
# ShatterMesh.cs:418-433, 56 bytes; rndRotation is never read
"ShatterMesh": [("Life", "f"), ("Delay", "f"), ("worldVelocity", "v3"), ("localVelocity", "v3"),
                ("rndVelocity", "v3"), ("rndRotation", "v3")],
```

The Wolf's values: Delay 1.2, Life 0.6, local (0, 1, −3), random (3, 3, 6). The root EffectControl (1.2 + 0.6) ends at
the same moment.

Page: about 35 lines, 1-2 h, on top of StaticMesh (1 h). Together they unlock Mirror Blade.

### Light: `crusader_hit`, `lawbringer_hit` (target only)

A point light (`m_Type 2`): white, intensity 1, range 4, render mode 2 (not important, i.e. per vertex), no cookie or
flare, on for the effect's 1 + 1 s.

If ever wanted: extract 4 fields (about 6 lines) and add a `THREE.PointLight(colour, intensity, 4)` under the node,
removed with it (about 10 lines, 30 min). It lights only the hero, which is Lambert; the effects themselves are unlit.
**Not needed for the Wolf**: both effects spawn on the target.

## Build order for the Wolf

Each step lists the effects (and skills) that become fully drawable once the steps above it exist.

| step | part | newly ready | size |
|---|---|---|---|
| 1 | EmitterControl | `artbreaker_ring` (Art Breaker) | 15 lines, 30 min |
| 2 | EffectControl(child) | `cattack2` (Charge Attack), `skyslasher` (Sky Slasher) | 25 lines, 1 h |
| 3 | EmblemEmitter (+ texture export) | `holysword_ring`, `holyarmor_ring`, `resurrection_ring` (Holy Sword, Holy Armor, Mass Resurrection) | 40 + 8 lines, 2 h |
| 4 | VortexEmitter | `darkedge_ring` (Dark Edge), `dualbrand_slash3` (with step 2) | 60 lines, 2-3 h + the fps mock |
| 5 | Animation (+ the cue's spawn rotation) | none alone | 40 page + 40 extractor lines, 3-4 h |
| 6 | TrailEmitter | `dualbrand_slash1` / `2` / `4`: all of Dual Brand | 70 lines, 3 h |
| 7 | SkinnedMeshRenderer | `bladefang_*`, `bloodfang_*` (Blade Fang ± Blood Fang) | 35 + 35 lines, 2-3 h |
| 8 | TrailRenderer | `crusader`, `lawbringer` (Crusader ± Law Bringer) | 60 + 10 lines, 2-3 h |
| 9 | StaticMesh + ShatterMesh | `mirrorblade_mirror` (Mirror Blade) | 25 + 15 + 35 lines, 2-3 h + the multiply mock |
| — | Light | (`crusader_hit`, `lawbringer_hit`: target only, stay out) | skip |

- **Total:** about 450 lines of page code and about 150 in `wardrobe_fx.py`, roughly 3 working days with the browser
  checks. Steps 1-4 (about a day) unlock 8 of the 18 hero-side effects.
- **After each step:** add the part to `BUILT` in `wardrobe_fx_inventory.py` and run it again (the recipe's rule).
- **Cross-class order:** VortexEmitter (23 effects alone) and EmblemEmitter (19) unlock far more than the rest. Steps 3
  and 4 are worth doing first whatever the class.

## How sure I am of each layout

| part | sure | why |
|---|---|---|
| VortexEmitter (164 B) | high | Every one of 31 instances in 8 classes uses up exactly its bytes. The values make sense (length 9 / 24, vortexCount 6 / 4, colours in 0..1, `bool → v3` padding as the existing layouts). Two neighbouring floats swapped would also fit the byte count; the order is the decompile's declaration order. |
| EmblemEmitter (68 B) | high | All 24 decode. The `image` PPtr resolves to real Texture2Ds (holyShield, holySword, resurrection). |
| TrailEmitter (124 B) | high | All 22 decode. The values make sense (life 0.4, minDistance 0.01, mode 0, minQuality 0, the two bools padded). |
| EmitterControl (12 B) | high | All 32 decode (Delay 1 / Life 3 / AfterLife 0 in artBreaker). Its three floats only have to be in the right order. |
| ShatterMesh (56 B) | high | All 5 decode; four v3 after two floats. |
| EffectControl(child) | certain | It is the existing 32-byte layout. What's new is behaviour, not bytes. I am highly sure of the "dust lives two frames" reading (the opaque `if (a − b != c)` guards worked out by hand at EffectControl.cs:192-210). |
| Animation / SkinnedMeshRenderer / MeshFilter / TrailRenderer / Light | certain (type tree) | Read through UnityPy's type tree; no byte layout is involved. The mesh reads through `MeshHandler` (`mesh.m_Vertices` itself is None in this 3.5 file, so `MeshHandler` is required). |

Less sure (behaviour, not bytes):
- the legacy Animation's end-of-clip hold (medium; matters only for `crusader`'s last 0.6 s);
- TrailRenderer's exact width and colour mapping (medium-high; Unity built-in, no source);
- the fps for VortexEmitter (the user's pick);
- DistortGlass as a multiply (high for the fallback, approximate for the grab-pass shift).
