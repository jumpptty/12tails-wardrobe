# Panda effects: the parts the page cannot draw yet (or draws wrongly)

Research 13/11/2026, office PC (one of the Panda fx researchers; scope: every page part the Panda's effects need: the
inventory's 71, the 8 Panda prefabs it does not list, the components `wardrobe_fx.effect()` drops, the shaders, the hero
code acting on its effects, summons, and the released TTO skills' prefabs: Nine Dragons, Tempest Dance (+ End), Yin Yang
Fist; Clap and Wai have no effect prefabs). Models: `plans/fx_mole/parts.md`, `plans/fx_chameleon/parts.md`. Read only:
nothing in `wardrobe/data` was written; `wardrobe_fx.py` / `wardrobe_fx_tto.py` ran with `--probe` only (or were imported
read only, in memory); no browser. `Panda.cs`, `CharacterControl.cs`, `ImageEmitter.cs` lines are
`C:\Users\Jump\Desktop\12tails\DecompiledSource\<file>` (= the home PC's `D:\12tails\...`; opaque predicates evaluated by
`annotate.py`, every `if (a - b ==/!= c)` replaced by TRUE / FALSE, line numbers kept, then read by hand); TTO is
`TTO1102:` = `DecompiledSource_TTO_2026-11-02` (`dump.cs`, `methods.tsv`, `pseudo/Panda.c`, `pseudo/CharacterControl.c`,
the client's `GameAssembly.dll` disassembled at the RVAs `methods.tsv` gives).

Probes (read only, outputs beside them) in `checks/fx_panda_research/parts/` (git-ignored; this PC's, re-probed):
- `probe.py` -> `probe.txt`, `probe.json`: all **79** prefabs in `heroes/panda/effects` through `wardrobe_fx.effect()`,
  a raw walk listing every component (what `effect()` drops), an unknown script's field bytes, every material's blend.
  Last lines: `blends: addsoft 123, alpha 4, add 14, multiply 5, shader:Particles/AdditiveOffset 8, opaque 1`; `dropped:
  ParticleSystem 1, ParticleSystemRenderer 1`; `UNKNOWN scripts:` (none). `per_effect.txt`: the components per effect.
- `fx_probe_all.json`: `wardrobe_fx.py panda --probe <all 79>`: every one builds (no error entry).
- `enabled_probe.py` -> `enabled_probe.txt`: every renderer / emitter switched off in a prefab (only threeStep's three
  TrailRenderers, and fuujinKen_ring2's emitter that its EmitterControl starts).
- `probe_ps.py` -> `probe_ps.json`: raijinKen_hit's Unity 3.5 ParticleSystem + renderer (full type trees, BB material);
  `tto_bbcopies.json`: `wardrobe_fx_tto.py panda --probe` of TTO's copies (raijinKen_hit, threeStep, windCloud, the
  status looks); `graft_try.py` -> `graft_try.txt`: the raijinKen_hit graft run in memory with the one table line.
- `cc_probe.py`: the Panda hero prefab's CharacterController (height 0.8, radius 0.2, centre (0, 0.49, 0)).
- `uses.py` -> `uses.txt`: every Instantiate in Panda.cs with each later use of the object (the hero code acting on it).
- `src/*.txt`: `annotate.py` of Panda.cs, CharacterControl.cs, EffectControl.cs.
- `catalog_keys.py` -> `catalog_keys.txt`: TTO's catalog under `heroes/panda/` (94 effects).
- `tto_probe.json` (`wardrobe_fx_tto.py panda --probe <the 15 released prefabs>`), `tto_summary.py` -> `tto_summary.txt`,
  `tto_compact.txt` (one line per node: components, Shuriken modules, EffectControl, AudioSource);
  `tto_mat_probe.py` -> `tto_mat_probe.json` (the new shaders' texture slots and parsed pass state).
- `disasm.py` (capstone, calls named from `methods.tsv` / `names.tsv`, RIP-relative constants shown) ->
  `disasm_HelixRibbon.txt` (HelixRibbonEmitter's Awake, LateUpdate, Ends, Rebuild, .ctor), `disasm_NineKing.txt`.

## Read this first

1. **BB: every Panda effect builds; nothing has a script without a layout; every shader is built.** Two BB effects are
   spoiled, and three status looks plus one hero look are missing from the inventory:
   | effect | what spoils it | today |
   |---|---|---|
   | `threeStep` (Three Steps, the whole visual) | its three `TrailRenderer`s are off in the prefab (`m_Enabled` false, `enabled_probe.txt`); the hero's code switches them on and off during the dash (`Panda.cs:20873-21277`) | `trail.js:100` returns null for a disabled trail: **draws nothing** (the root has only an Animation and its sound) |
   | `raijinKen_hit` (Raijin Ken's strike) | Unity 3.5's ParticleSystem (node `ParticleSystem`, Cloud1 addsoft), dropped by `effect()` | builds without its burst of 32 puffs at 0.4 s |
   | the hero under `ashura` (Ashura 2) | `setColor(1, 0, 0)` on every renderer of the character (`CharacterControl.cs:35484-35496`), back to 0.86 at the end (`:15830-15840`) | not drawn: the Panda looks normal |
2. **No LAYOUTS to paste.** The Panda has no `Panda_<x>` scripts: its 79 prefabs use RingEmitter 72, EffectControl 68,
   ImageEmitter 51, LineEmitter 31, AlphaTimer 16, EmblemEmitter 6, BoltEmitter 2, VortexEmitter 1, EmitterControl 1,
   AudioControl 1 (all with layouts and page parts). One extractor line only: `SHURIKEN_FROM_TTO["panda"] =
   ["raijinKen_hit"]` (the Chameleon's route, no `SHURIKEN_MAT` entry); run in memory it grafts TTO node 1 onto BB node 3
   with BB's own `Cloud1` (`graft_try.txt`).
3. **The inventory misses 8 prefabs; none blocks.** Status looks `CharacterControl.cs` loads: `delayQi` (`:35342`, on
   the Panda, parented, localPosition 0), `drunken` (`:35396`, on the Panda, at `bounds.center + 0.5 x height` up,
   parented), `paralysis` (`:35443`, on the target, at its collider centre, not parented), `ashura` (`:35500`, on the
   Panda's `Root` bone, local identity), `drunk` (`:35535`, on the target, as `drunken`). Three dead prefabs no code
   loads, in BB or TTO (grep over all `DecompiledSource` and TTO1102's `pseudo/` + `pseudo_all.raw.c`):
   `drunkenFist_hit`, `qiStrike_emblem`, `windcloud_hit` (built parts only; nothing to do). Tool gap (as every class's):
   `wardrobe_fx_inventory.py` sees no status looks and no disabled renderers.
4. **The hero's code acting on BB effects** (`uses.txt`; everything else is spawned and left alone):
   - `threeStep`: the trails `fxNode1` on 0.1-0.5 s, `fxNode2` on 0.4-0.8 s, `fxNode3` on from 1.2 s (part 1).
   - `heavenPalm` (the Heaven Palm hit): `localScale = 1.5` at sLv 2 (`Panda.cs:9539-9548`): the max rank's hit is 1.5x
     (the cue's `scale`, built).
   - `spTransfer`: its BoltEmitter has no TargetNode; each frame the code moves it to hero + TransformDirection(0, 0.4,
     0.5) and sets `TargetPosition` = the target's collider centre (`Panda.cs:36432-36441`): the built "no TargetNode
     aims at the cue's `to`" (the Bat's), nothing to build.
   - `raijinKen_hit`: `transform.Find("Camera/effectCamera")` -> `PlayerCameraControl.setSpecialTarget` (`Panda.cs:
     42506-42553`), a cinematic camera cut; and every `CameraEffect` (shakes, `whiteRamp`): left out (camera effects:
     Bison decision 35, Cat 43, Chameleon 52, Mole 51).
5. **Summons: none** (BB or TTO). The ogres (`pummel_ogre`, `towerRush_ogre`) and the dragons are effects.
6. **TTO's released skills (15 prefabs, `tto_compact.txt`) need one new script, two code movers, one bone hook and three
   shaders; two Shuriken modules are missing for them too.**
   | what | prefabs | part |
   |---|---|---|
   | `HelixRibbonEmitter` (TTO.Game TypeDefIndex 411, new) | tempestDance_aura (2), _end (2), _pulse, yinYang, yinYangFist_charge, _seal (2): 9 instances | T1 |
   | the dragons' flight (code, not a script): `Panda.NineDragon`, `Panda.NineKing` | nineDragons_dragon (x8), nineDragons_king | T2 (CODE_MOVERS) |
   | `TempestTrails`: each child of the prefab parented to the hero's bone of its name | tempestDance_trails (Hand_R, Hand_L, Foot_R, Foot_L) | T3 |
   | shaders `ERB/Particles/Add_CenterGlow`, `ERB/Particles/Blend_CenterGlow`, `Particles/Standard Surface` | yinYangFist_burst (7 systems) | T4 |
   | Shuriken `NoiseModule` (8 systems), `LightsModule` (5) | nineDragons_bite / _fall / _kingRise, yinYangFist_burst | T5 (shared with the Monkey's T3) |
   Already built and used as they are: ChameleonLightning (25 bolts in yinYangFist_burst, all `autoBolt`: no hero call),
   GroundHugEmitter (17), TrailRendererModern (6), LineRenderer, SkinnedMeshRenderer + legacy Animation (the dragons;
   TTO's clips are exported now: `pandaRow6_dragonSwim`, `root`), Light (the five templates are `m_Enabled` 0), the
   Shuriken modules Shape / Size / Color / Velocity / InheritVelocity / Force / ClampVelocity / UV / Rotation /
   World Collision, mesh particles (CenterPlate, Bamboo, the Quad), `Particles/Standard Unlit`, legacy add / addsoft /
   alpha / multiply.
7. **Game quirks (offer to the user for the Bible; none changes a cue).**
   - Three Steps' three blade trails are off in the prefab and switched by the coroutine: fxNode1 0.1-0.5 s, fxNode2
     0.4-0.8 s, fxNode3 from 1.2 s until the effect ends with the move at 1.4 s (`Panda.cs:20873`, `:20900`, `:21063`,
     `:21250`, `:21277`; the waits `:21771-21803`).
   - Heaven Palm 2's hit effect is drawn at 1.5x (`Panda.cs:9548`); rank 1's at 1x.
   - Three prefabs ship but no code loads them: `drunkenFist_hit`, `qiStrike_emblem`, `windcloud_hit` (BB and TTO).
   - Nine Dragons: the eight dragons alternate hands (k even: `Hand_R`, odd: `Hand_L`, `TTO1102:Panda.<RPC_nineDragons>
     d__331::MoveNext@0x1d899a0`, Row6Hand(~k & 1)), each on a cubic Bezier that bows out to its own side
     (`<NineDragon>d__336`, part T2); the King weaves (0.9 (1 - u) sin 2 pi u to the side, 0.6 sin pi u up) on its 0.4 s
     flight (`<NineKing>d__339`, `disasm_NineKing.txt` 0x1d7086d-0x1d70921).

## The Panda's spoiled / missing set

"Where" is where the game spawns it; the times and tiles are the skills researchers' (`attacks_emotes.md`,
`skills_*.md`, `tto.md`), so treat the cue shapes here as the parts' contract.

| effect | skill (spawn) | missing part(s) | where |
|---|---|---|---|
| `threeStep` | Three Steps `RPC_threeStep` (createEffect `Panda.cs:21728`, rotation x Euler(270, 90, 0)) | trail.js: a disabled TrailRenderer built hidden + the cue's `enable` (part 1) | hero, followPosition / followState (cut at the standby, 1.4 s, `:21458`) |
| `raijinKen_hit` | Raijin Ken `RPC_raijinKen_hit` (createEffect `:42525`, LookRotation(-hitDir)) | the Shuriken graft (part 2) | hitPos (the 10 m point), facing back at the hero |
| hero look `ashura` (+ the `ashura` effect) | Ashura `RPC_ashura` status (`:30572`, `chaAdjust(24)`) | HERO_SKINS `"ashura"` (part 3); the effect: built (cue `bone`) | the hero; the effect on `Root` |
| `drunken` | Drunken Fist's self status with Drunken Plus (`:32591`, `chaAdjust(12)`) | none (cue `y`, `kill`) | hero, y 0.89 (0.49 + 0.5 x 0.8, `cc_probe.py`) |
| `drunk` | Drunken Fist's hits with Drunken Spin #403 (`:31817` getDebuff(12), `:32039`-`:32362` getDebuff(6)) | none | the target, y 1.1 (0.6 + 0.5 x 1) at d 10 |
| `delayQi` | Delay Qi's self status (`:24255`, `chaAdjust(3) + 3 x QiBurstLv` = 6 s with Qi Burst #412) | none (cue `kill`) | hero, local 0 |
| `paralysis` | Stasis Blow's status on the target (`:34394`) | none (its LineEmitter ends itself) | the target's collider centre (0, 0.6, 10) |
| TTO: tempestDance_aura / _end / _pulse, yinYang, yinYangFist_charge / _seal | Tempest Dance, Yin Yang Fist | HelixRibbonEmitter (T1) | tto.md's |
| TTO: nineDragons_dragon, nineDragons_king | Nine Dragons | Panda.NineDragon, Panda.NineKing (T2) + api.boneMatrix (Interfaces 1) | tto.md's |
| TTO: tempestDance_trails | Tempest Dance (`TempestTrails@0x1d5f010`) | fx:tto/tempestDance_trails (T3) + api.boneMatrix + TrailRendererModern `emitOff` | the hero's hands and feet |
| TTO: yinYangFist_burst | Yin Yang Fist (`<YinYangSeal>d__358`) | ERB shaders + noiseTex, Standard Surface (T4); Noise, Lights (T5) | the seal's spot |
| TTO: nineDragons_bite, _fall, _kingRise | Nine Dragons | Shuriken Noise (T5) | tto.md's |

## LAYOUTS (`pipeline/wardrobe_fx.py`)

None: no Panda prefab has a script without a layout (`probe.txt`'s last line is empty). Extractor lines (lead):
- `wardrobe_fx.py`: `SHURIKEN_FROM_TTO["panda"] = ["raijinKen_hit"]` and **no** `SHURIKEN_MAT` entry (the Chameleon's
  route, `wardrobe_fx.py:494`): BB node 3 `ParticleSystem` (renderer material `Cloud1`, addsoft) <- TTO node 1
  `ParticleSystem` (`tto_Cloud1`), unique name and material. The systems match field for field (`probe_ps.json` vs
  `tto_bbcopies.json`): one shot of 5 s, local space (BB `moveWithTransform` true = TTO 0), hemisphere (type 2) r 1,
  angle 25, one burst of 32 at 0.4 s, life 1-2 s, speed 3-5, size 0.2-0.4, rotation 0-2 pi, colour over life on, every
  other module off; renderer billboard, max size 0.5.
- `wardrobe_fx_tto.py`:
  ```python
  SKILL_FX["panda"] = [
      # Nine Dragons: TTO1102:Panda.<RPC_nineDragons>d__331::MoveNext@0x1d899a0, <NineDragon>d__336@0x1d6f860,
      # <NineKing>d__339@0x1d701c0
      "nineDragons_cast", "nineDragons_dragon", "nineDragons_bite", "nineDragons_king", "nineDragons_kingRise",
      "nineDragons_fall",
      # Tempest Dance (+ End): <RPC_tempestDance>d__346@0x1d9b1b0, TempestTrails@0x1d5f010, RPC_tempestCounter@0x1d59f30,
      # <RPC_tempestDanceEnd>d__355@0x1d9ad20
      "tempestDance_aura", "tempestDance_trails", "tempestDance_pulse", "tempestDance_counter", "tempestDance_end",
      # Yin Yang Fist: <RPC_yinYangFist>d__357@0x1dcdc50, <YinYangSeal>d__358@0x1dce740; the status look
      # CharacterControl::AddYinYangFx@0x24af630
      "yinYangFist_charge", "yinYangFist_seal", "yinYangFist_burst", "yinYang",
  ]
  CODE_MOVERS.update({
      # TTO1102:Panda.<NineDragon>d__336::MoveNext@0x1d6f860 (pseudo/Panda.c:75-387): a cubic Bezier from the hand to the
      # prey + 0.6 up in clamp(1.6 d / 22, 0.35, 0.7) s, NineFly@0x1d53f80 (turned along its motion), NineVanish@0x1d55070
      # at the end (wardrobe/fxparts/tto_panda.js; plans/fx_panda/parts.md T2)
      "nineDragons_dragon": "Panda.NineDragon",
      # <NineKing>d__339::MoveNext@0x1d701c0 (:405-766, disasm_NineKing.txt): 0.4 s from the spawn to the landing point
      # + 0.8 up, weaving, NineVanish at the end
      "nineDragons_king": "Panda.NineKing",
  })
  ```
  and in `material()`: also save `_Noise` (the ERB shaders' second texture) as `"noiseTex"` with `"noiseScale"` /
  `"noiseOffset"` (exported like `_MainTex`, as `_ScaleTex` is): `tto_Add_noise` -> `Gradient4` (`tto_mat_probe.json`;
  the other ERB materials leave `_Noise` empty: white).

## Each part

Page parts plug in as the comment above `FX_PART_FILES` says (`wardrobe/index.html:3940-4041`, as read on 13/11/2026
with the Mole's build editing the file): `wardrobe/fxparts/<file>.js` default-exports `register(api)` and calls
`api.part(type, build)`; `build(fx, node, comp, mat, nodeDef, data)` returns `{ node, update(dt, cam) ("destroy"
removes the node), stop?(), dispose?() }` or null; `"fx:<effect>"` = the hero's code acting on that effect (built once on
its root, comp null); `api.spawn(name, at, opts)`; the cue's options reach a part as `fx.at` (cueOf passes them all).
Space: every root hangs in the effect's mirror group (Unity's world, the hero's feet at the origin, +z her facing, y 0
the floor). The standard target body (Bat decision 4): centre (0, 0.6, 10), CharacterController h 1, r 0.3.

### 1. Three Steps' trails: a disabled TrailRenderer and the cue's `enable` (`fxparts/trail.js`)

**What BB does (`RPC_threeStep`, `Panda.cs:20721-21830`, the predicates evaluated).** At 0 (case 0 -> `:21510-21748`):
`actionState = attack`, `PlayAnimation("threeSteps", 0.2)` (`:21528`), the voice (`:21575-21697`), `createEffect
(threeStep, hero position, hero rotation x Euler(270, 90, 0))` (`:21728`), the three `TrailRenderer`s found by name
(`:21742-21748`), `Yield(2, 0.1)` (`:21801`). Then, each case a wait later (`:21771-21803`):
| clip time | case | line | does |
|---|---|---|---|
| 0.1 | 2 | `:20873` | moveSpeed 4, `fxNode1.enabled = true`; Yield 0.3 |
| 0.4 | 3 | `:20900` | `fxNode2.enabled = true`, hit 1; Yield 0.1 |
| 0.5 | 4 | `:21063` | `fxNode1.enabled = false`; Yield 0.2 |
| 0.7 | 5 | - | hit 2; Yield 0.1 |
| 0.8 | 6 | `:21250` | `fxNode2.enabled = false`; Yield 0.4 |
| 1.2 | 7 | `:21277` | `fxNode3.enabled = true`; Yield 0.1 |
| 1.3 | 8 | - | hit 3; Yield 0.1 |
| 1.4 | 9 | `:21458` | `actionState = standby` (the effect's followState ends it) |
Each case first checks `actionState == attack && myCommand == threeSteps` (else it ends). The prefab (`probe.txt`):
root at (0.396, 2.62, -2.66) turned (0.5, -0.5, -0.5, -0.5), its Animation `root` 1.4 s moves the three nodes (the
fists' and the kick's arcs); TrailRenderer `m_Time` 0.2, width 0.7 -> 0, material `threeStepFx` (addsoft Ray1).

**The page (trail.js, about 10 lines).** `c.m_Enabled === false` no longer returns null: the trail is built with its
mesh hidden (`m.visible = false`, which already drops its points, `trail.js:107`). The cue's `enable` (Interfaces 2):
`[[t, nodeName, on], ...]`, seconds after the spawn; each frame the part compares its own clock with the list entries
for `nodeDef.name` and sets `m.visible` to the newest due one. APPROX: Unity's TrailRenderer, re-enabled, may keep
points from before it was switched off; here none of the three is switched on twice, so it does not matter.

### 2. raijinKen_hit's ParticleSystem (`wardrobe_fx.py` graft, lead; shuriken.js unchanged)

The one table line of "LAYOUTS" above; `graft_try.txt` shows the result (BB node 3 carries `ParticleSystem` +
`ParticleSystemRenderer`, `mats ["Cloud1"]`). The modules it uses (Initial, Shape hemisphere, Emission burst, Color)
are drawn by shuriken.js today. After the build, the inventory still lists it as needing ParticleSystem (the grafted
ones are noted as drawn, the Chameleon's comment in `wardrobe_fx_inventory.py`).

### 3. The Ashura look: HERO_SKINS `"ashura"` (`index.html`, lead)

`CharacterControl.cs:35484-35510` (the `ashura` status case, predicates TRUE): `mColor = (1, 0, 0)`, `setColor(mColor)`
(every renderer under the character, props too: `:21702-21800`), then `ashura` (one LineEmitter `Ray3`, addsoft,
repeatForever, `probe.txt`) instantiated, named `ashuraFx`, parented to `findChildObject(transform, "Root")`, local
position 0, local rotation Euler(0, 0, 0), scale 1. At the status's end (`:15830-15845`): `mColor = (0.86, 0.86, 0.86)`,
`setColor`, the `ashuraFx` child destroyed. Duration `chaAdjust(24)` = 24 s (`Panda.cs:30572`): cut at 10.
**The page:** a body look beside the Bison's (`index.html:4877-4883`): `"ashura": () => ({ tint: [1 / 0.86, 0, 0] })`
(the page's hero colour stands for the game's 0.86, as the Bison's tints): the Panda and her gauntlets turn red. Cues:
`[t, "skin", "ashura", {"kill": 10}]` and `[t, "fx", "ashura", {"bone": "Root", "kill": 10}]` (the page's `bone`:
parented, local 0, identity: exactly the game's). The page rig has `Root` (`clips.json` tracks).

### 4. The other status looks (no page code)

- `drunken` (self): `bounds.center + 0.5 x height x up` of the Panda's own CharacterController = 0.49 + 0.4 = **y 0.89**
  (`cc_probe.py`; APPROX: Unity's controller bounds may add the skin width), parented to her (`CharacterControl.cs:
  35396-35411`); a looping legacy emitter (`drunken`, 2-4 a second, energy 1-1.5): cue `{"y": 0.89, "kill": 10}`
  (`chaAdjust(12)` cut at 10).
- `drunk` (the target): the same rule on the standard body: 0.6 + 0.5 = **y 1.1** at d 10 (`:35535-35547`); `kill` =
  the status (getDebuff(12) for the first hit, 6 for the others, `Panda.cs:31817-32362`), cut at 10.
- `delayQi` (self): at her feet, parented, localPosition 0, scale 1 (`:35342-35376`); its EffectControl life 12 but the
  status ends it (`:15753`): cue `{"kill": 6}` (`chaAdjust(3) + 3 x 1`, Qi Burst #412 on, `Panda.cs:24255`).
- `paralysis` (the target): at its collider centre, identity, not parented (`:35443`): `{"y": 0.6, "d": 10}`; its
  LineEmitter (Life 0.1, Delay 0.1, EmissionTime 0.2, not repeatForever) destroys itself (`LineEmitter.cs:204`).

## TTO parts (the released skills: Nine Dragons, Tempest Dance, Yin Yang Fist)

All in `fxparts/tto_panda.js` (new). Field values are the prefabs' (`tto_probe.json`); the methods TTO1102's.

### T1. HelixRibbonEmitter (TTO.Game TypeDefIndex 411): 9 instances

**Fields** (`dump.cs:11764-11810`; `.ctor`@0x2265660 defaults in brackets): `ribbons` (3), `turns` (1), `height` (2),
`radiusBottom` (0.6), `radiusTop` (1.2), `widthBottom` (0.2), `widthTop` (0.4), `segments` (40), `spin` (-360 deg/s),
`scroll` (1), `uvTile` (2), `wobble` (0), `wobbleSpeed` (3), `Life` (1), `Delay` (0), `fadeIn` (0.2), `fadeOut` (0.3),
`repeatForever`, `radiusScaleStart` (1), `radiusScaleEnd` (1), `colorBottom` / `colorTop` (white), `endFade` (0.2);
private `mesh`, `meshRenderer`, `verts`, `uvs`, `cols`, `startTime`, `phaseOffset`.

**Methods** (`disasm_HelixRibbon.txt`, every constant and call read; sin = `0x308bd0`, cos = `0x308640`, identified by
their uses in `pseudo/Bat.c:19250-19300`; the static at TypeInfo 0x3811de8 + 0x18 is `Vector3.upVector`):
- Awake@0x2264a90: `meshRenderer` = its MeshRenderer; a new dynamic Mesh; `verts`, `uvs`, `cols` of `ribbons x
  (segments + 1) x 2`; triangles `ribbons x segments x 6`: for ribbon r, base `b = r (2 segments + 2)`, segment s, `i =
  b + 2 s`: (i, i + 2, i + 1), (i + 1, i + 2, i + 3); the mesh on its MeshFilter; `startTime = Time.time`;
  `phaseOffset = Random.Range(0, 360)`; `Rebuild(0, 0)`.
- LateUpdate@0x2264ef0: `t = time - startTime - Delay`; `t < 0`, or (`!repeatForever` and `t > Life`): renderer off,
  nothing else (the EffectControl destroys it); else renderer on, `a = fadeIn > 0 ? clamp01(t / fadeIn) : 1`, and when
  `!repeatForever && fadeOut > 0`: `a *= clamp01((Life - t) / fadeOut)`; `Rebuild(t, a)`.
- Ends(s, f)@0x2264e00: `f <= 0` -> 1; else `smooth(clamp01(s / f)) x smooth(clamp01((1 - s) / f))`, smooth(x) = 3x^2
  - 2x^3: each ribbon fades in at its bottom and out at its top over `endFade` of its length.
- Rebuild(t, a)@0x2265090:
  - `k = (!repeatForever && Life > 0) ? clamp01(t / Life) : 0`; `rs = lerp(radiusScaleStart, radiusScaleEnd, k)`;
    `M = (1 + wobble x sin(t x wobbleSpeed)) x rs`; `flat = height <= 0.001`; `phase = t x spin + phaseOffset`
    (degrees); `uShift = t x scroll`.
  - ribbon r (0 .. ribbons - 1): `a0 = (360 r / ribbons + phase)` degrees; point s (0 .. segments, inclusive): `u =
    s / segments`, `th = turns x 2 pi x u + a0 (rad)`, `R = lerp(radiusBottom, radiusTop, u) x M`, `W =
    lerp(widthBottom, widthTop, u)`, centre `p = (R cos th, u x height, R sin th)` (local space), side = flat ? `(cos th,
    0, sin th)` (radial, in the floor's plane) : `(0, 1, 0)` (upright); `v0 = p - side x W / 2`, `v1 = p + side x W / 2`;
    uv `(u x uvTile - uShift, 0)` / `(.., 1)`; colour `lerp(colorBottom, colorTop, u)` with alpha `x Ends(u, endFade)
    x a`, the same on both vertices.
  - vertices, uvs, colours set; RecalculateBounds.
**The page (about 50 lines; the GroundHugEmitter's pattern, groundhug.js:65-).** `api.fxMesh(node, mat)` on the node
(the mesh is in the node's space, so the node's own transform and the effect's followPosition carry it), positions /
colours / uvs rebuilt each frame through `api.setMesh` with the triangle list once, colours made linear as the page's
vertex colours are (trail.js's `lin`), the mesh hidden before Delay and after Life (not repeatForever), the material the
node's (`tto_pandaRow6_windRibbon`, `tto_pandaRow6_inkStroke`: addsoft; their textures wrap: fxMaterial sets
RepeatWrapping, `index.html:4076`). Its clock is the effect's (Time.time - startTime = the node's age).

### T2. The dragons' flights: Panda.NineDragon, Panda.NineKing (code movers)

**NineDragon** (`<NineDragon>d__336::MoveNext@0x1d6f860`, `pseudo/Panda.c:75-387`; its launcher
`<RPC_nineDragons>d__331` `:13461-13688`: dragon k = 0..7 at `start + 0.4 + 0.11 k`, from `Row6Hand(~k & 1)`'s position:
k even `Hand_R`, odd `Hand_L`, `Row6Hand@0x1d5be80`). At its first step:
- `fwd = Row6Fwd()` (the hero's flat forward, `@0x1d5bcd0`); `side = Cross(up, fwd) x (k odd ? -1 : 1)` (k even: her
  right); `end = NineAim(prey, fallback)` (`@0x1d52a30`: the prey's position + 0.6 up while it lives, else the
  fallback); `flight = clamp(1.6 |from - end| / 22, 0.35, 0.7)`;
- `c1 = from + 1.4 fwd + (1.3 + 0.15 (k mod 4)) side + (2.2 + 0.2 (k mod 3)) up`;
- spawned at `from`, `LookRotation(c1 - from)` (Row6Spawn).
Each frame while `time < t0 + flight`: `end` again (homing), `c2 = end + 0.6 side + 2.4 up`, `p = Bezier(from, c1, c2,
end, (time - t0) / flight)` (`Bezier@0x1d51f00`: the cubic), `NineFly(d, last, p)` (`@0x1d53f80`: position p, rotation
`LookRotation(p - last)` when it moved). At the end: `NineFly` to `end`, **NineVanish** (`@0x1d55070`: its children
`Body`, `HeadGlow`, `HeadHalo` SetActive(false), every ParticleSystem under it `Stop(StopEmitting)`, Destroy 0.5 s
later: the trail fades out), `nineDragons_bite` at `end` (identity), `punch1` (k even) / `punch2` (odd) at 0.9 (at most
one per 0.06 s), the bite's hit.
**NineKing** (`<NineKing>d__339::MoveNext@0x1d701c0`, `:405-766`; started at `start + 1.6`): `from = hero + 0.7 up + 0.4
fwd`; `end = NineMark(mark)` (the clicked target's ground position); `aim = end + 0.8 up`; `dir = vFlat(aim - from)`
normalised (fwd when < 0.01); `side = Cross(up, dir)`; spawned at `from`, `LookRotation(dir)`. For 0.4 s, `u = (time -
t0) / 0.4`: `p = lerp(from, aim, clamp01(u)) + 0.9 (1 - u) sin(2 pi u) side + 0.6 sin(pi u) up` (`disasm_NineKing.txt`
0x1d7086d-0x1d70921: the second sin's argument is `u x pi`, which Ghidra dropped), `NineFly`. Then `NineFly(aim)`,
NineVanish, `nineDragons_kingRise` at `end`, `LookRotation(dir)`, a shake (left out), the dash / lock; eight strikes 0.15 s
apart; `nineDragons_fall` at `end` after them.
**The page (one part per code mover, `api.part("Panda.NineDragon")` / `("Panda.NineKing")` on the root, about 35 lines
together).** Its options (`fx.at`, Interfaces 3): `k`, `to` ([x, y, d]: the dragon's `end` = the prey point + 0.6 up,
(0, 0.6, 10) for the standard target; the King's `end` = the ground point (0, 0, 10)), `fromBone` (the dragon's hand:
the start is that bone's position at the spawn, `api.boneMatrix`, else the cue's spot). It drives the root's position
and rotation each frame as above (the root's own Animation, `pandaRow6_dragonSwim` loop / the King's, plays under it),
then vanishes: the three named nodes hidden, `stop?.()` on every emitter under the root (Shuriken's StopEmitting; the
trail keeps fading), `"destroy"` 0.5 s later. The bites / kingRise / fall are cues (their times follow from the fixed
target: part list below), not spawns of the part: one owner per spawn, as the Chameleon's arrow hits are cued.

### T3. fx:tto/tempestDance_trails (`TempestTrails@0x1d5f010`, `pseudo/Panda.c:43467-43706`)

`TempestTrails(true)`: for each child of the prefab (`Hand_R`, `Hand_L`, `Foot_R`, `Foot_L`, all at local 0, identity,
`tto_probe.json`), `Instantiate(child, findChildObject(hero, child.name))`, localPosition 0, localRotation identity,
`TrailRenderer.Clear()`; `TempestTrails(false)`: every such trail `emitting = false` and `Destroy(it, trail.time +
0.05)` (m_Time 0.3 hands, 0.38 feet). **The page (about 15 lines):** the hook on the root, each frame: for each child
node, its local matrix = root^-1 x `api.boneMatrix(child.name, fx)` (Interfaces 1); the cue's `off` (seconds after the
spawn, Interfaces 4): each of its TrailRendererModern emitters' `emitOff()` (Interfaces 5); the cue's `kill` = `off` +
0.43. The root has no EffectControl (it lives until the kill).

### T4. Three shaders (`api.shader` in tto_panda.js)

Pass state from the parsed shader form (`tto_mat_probe.json`, the bundles' `m_ParsedForm`); the programs are not
decoded (APPROX: the fragment from the property set, as the Monkey's `Eric/URP` shaders, plans/fx_monkey/parts.md T2).
- `ERB/Particles/Add_CenterGlow` (tto_Add_noise, tto_Mask13, tto_Circle42): `Blend One One`, ZWrite off, Cull
  `_CullMode` (0: Off). Live properties (the parsed form's list): `_MainTex`, `_Noise`, `_Flow`, `_Mask`,
  `_SpeedMainTexUVNoiseZW`, `_DistortionSpeedXYPowerZ`, `_Emission`, `_Color`, `_Usecenterglow`, `_Usedepth`,
  `_Depthpower`, `_CullMode`. Every material here: `_Usecenterglow` 0 and `_Usedepth` 0 (the mask and soft depth unused),
  `_SpeedMainTexUVNoiseZW` (0, 0, 0, 0) (no scroll; `_MainTexUspeed` / `_SpeedMainTexUVNoiseUV` are stale saved values
  the shader does not declare), `_Flow` empty. So `rgb = main x noise x _Color x vertex colour x _Emission x alpha`, alpha
  = `main.a x noise.a x _Color.a x vertex alpha`, added. `_Emission` 3 / 2 / 2; tto_Add_noise's main texture tiled
  (4, 0.5), its `_Noise` Gradient4 (the extractor's `noiseTex`).
- `ERB/Particles/Blend_CenterGlow` (tto_YinYang): `Blend SrcAlpha OneMinusSrcAlpha`, ZWrite off, Cull Off; the same
  colour with `_Emission` 2.5 and alpha `x _Opacity` (1), clamped.
- `Particles/Standard Surface` (tto_pandaRow6_bamboo, _bambooLeaf: `_Mode` 1 Cutout, `_Cutoff` 0.124 / 0.5, ZWrite on,
  `_EmissionEnabled` 1 with `_EmissionMap` = the albedo x `_EmissionColor` 0.12 / 0.15; _smokePuff, _smokeWisp: `_Mode` 2
  Fade, `_SrcBlend` 5 / `_DstBlend` 10, ZWrite off, no emission; all `_LightingEnabled` 1, `_Cull` 0): Unity's lit
  particle Standard shader. On the page: a lit material (as tto_sheep.js's `Standard`, `tto_sheep.js:138-152`, double
  sided with the face sign turned) with `vertexColors`, `color = _Color`, `map`, Cutout -> `alphaTest = _Cutoff`, Fade ->
  transparent with the blend factors (tto_sheep.js's `BF` table), `emissive = _EmissionColor` with `emissiveMap = map`
  when `_EmissionEnabled`. APPROX: the bamboo's `_BumpMap` normal map is not drawn (not exported).

### T5. Shuriken NoiseModule and LightsModule (`fxparts/shuriken.js`; the Monkey's T3, one owner)

Not drawn today (`shuriken.js:287-290` lists them in `P.skipped`). If the Monkey's build has landed them, nothing here;
else the Panda's values:
- **NoiseModule** (8 systems): `strength` 1 (bites' / fall's / kingRise's Sparks), 0.5 (DustRing), 0.35 (Ink / Cream
  Plume), 1.4 (LeafBurst / LeafFall); `frequency` 0.5 / 0.35 / 0.5 / 0.6; `scrollSpeed` 1 / 0.4 / 0.6; `damping` on for
  the Sparks only; octaves 1, positionAmount 1, rotation / size amount 0, one axis (no separateAxes). APPROX (as the
  Monkey's question 9): a smooth value-noise field in [-1, 1]^3 sampled at `p x frequency + (0, scroll x t, 0)`, added
  to each particle's position as a velocity of `strength` m/s (Unity's curl noise not reproduced; `damping` noted).
- **LightsModule** (yinYangFist_burst's five `Flash` systems): `ratio` 1, `maxLights` 1, `light` = the child node's
  Light (Point, range 8.909, colour (0.75, 0.85, 1), intensity 1, itself off), `intensity` on with `intensityCurve` 5,
  `range` / `color` off: one light at the system's first live particle, intensity 1 x 5 x the particle's alpha, range
  8.909, through `api.pointLight()` (two pooled: a strike that finds none goes unlit), `api.releaseLight` when the
  particle dies or the effect goes.

## Interfaces (fixed up front, so the builders run in parallel)

1. **`api.boneMatrix(name, fx)`** (lead, index.html): a Matrix4 = the Unity transform, in `fx`'s mirror group, of the
   hero's bone `name` (`C.byName[name]`): `fx.mirror.matrixWorld^-1 x bone.matrixWorld x MIRROR_X`, exactly the cue
   `bone` code's (`index.html:4348-4361`); null when the hero or the bone is missing. Used by Panda.NineDragon
   (`fromBone`) and fx:tto/tempestDance_trails.
2. **The cue's `enable`** (trail.js reads `fx.at.enable`): `[[t, nodeName, on], ...]`, seconds after the spawn; a
   TrailRenderer whose node matches is shown from the newest due `on: true` until a later `on: false` (part 1). A
   disabled TrailRenderer is built hidden, not dropped.
3. **Panda.NineDragon / Panda.NineKing's options** (`fx.at`): `k` (0-7), `to` ([x, y, d], the hero-relative point a cue's
   spot uses), `fromBone` ("Hand_R" / "Hand_L"). The CODE_MOVERS component is the root's first (`{"type":
   "Panda.NineDragon"}`), as every TTO mover.
4. **fx:tto/tempestDance_trails' `off`** (seconds after the spawn).
5. **TrailRendererModern `emitOff()`** (`fxparts/tto_sheep.js:227-243`, one method on its emitter): from then on no new
   point (`TrailRenderer.emitting = false`); the old ones run out their `m_Time`. Not `stop()`: the page calls `stop?.()`
   on every emitter at an EffectControl's life end, and TTO's EffectControl stops only ParticleSystems
   (`TTO1102:EffectControl::Update@0x1A233A0`), so a `stop` would change every TTO trail already cued.
6. **HERO_SKINS `"ashura"`** (lead): `{ tint: [1 / 0.86, 0, 0] }`.
7. **Extractors** (lead): `SHURIKEN_FROM_TTO.panda`; TTO `SKILL_FX.panda`, `CODE_MOVERS` (2), `_Noise` -> `noiseTex` /
   `noiseScale` / `noiseOffset`.
8. **New cue options for `wardrobe_fx_check.py`'s `OPTS`** (lead; `:176-181`): `enable`, `k`, `fromBone`, `off` (the
   existing `hand` is the Cat's banner hand and `from` the Chameleon's bolt start: not reused), and the same words in the
   cue-format comment (`index.html:4720-4768`). `FX_PART_FILES += "tto_panda"`.
9. **Unchanged, used:** the cue's `bone`, `scale`, `kill`, `cut`, `rot`, `to`; HeroSkin's body look; tto_chameleon.js's
   ChameleonLightning (any class's prefab); api.pointLight / releaseLight; light.js (a disabled Light builds nothing).

## Rank by value (effects made right / effort)

| rank | part | Panda effects | other classes | work |
|---|---|---|---|---|
| 1 | trail.js disabled trail + `enable` | Three Steps (its only visual) | none in the data today | ~10 lines |
| 2 | HelixRibbonEmitter | Tempest Dance's aura, pulses, end; Yin Yang Fist's charge, seal, the yinYang mark | 0 | ~50 lines |
| 3 | Panda.NineDragon / NineKing + api.boneMatrix | Nine Dragons' eight dragons and King | (boneMatrix: any part) | ~35 + ~5 lines |
| 4 | HERO_SKINS ashura | Ashura's red Panda (24 s, cut 10) | 0 | 1 line |
| 5 | ERB shaders + Standard Surface + noiseTex | Yin Yang Fist's burst (taiji, bamboo, smoke, leaves, glow) | Monkey (the same Hovl family) | ~40 lines + 3 extractor lines |
| 6 | Shuriken Noise + Lights | the sparks' wander, the strikes' flashes of light | Monkey's T3 (one build) | ~40 lines |
| 7 | fx:tto/tempestDance_trails + emitOff | Tempest Dance's limb trails | 0 | ~15 + 2 lines |
| 8 | raijinKen_hit graft | Raijin Ken's burst | 0 | 1 line |

## Who builds what (never two owners for one file; as `plans/fx_wolf/build_rules.md`)

| agent | owns | builds |
|---|---|---|
| A: tto_panda | `wardrobe/fxparts/tto_panda.js` (new), `wardrobe/fxparts/tto_sheep.js` (only `emitOff`, Interfaces 5) | T1 HelixRibbonEmitter, T2 Panda.NineDragon + Panda.NineKing, T3 fx:tto/tempestDance_trails, T4 the three shaders |
| B: shuriken | `wardrobe/fxparts/shuriken.js` | T5 NoiseModule, LightsModule (first check whether the Monkey's build added them: `P.skipped` at `:289`; if so, only the Panda's values above to check against) |
| C: page_pipeline | `wardrobe/index.html`, `wardrobe/fxparts/trail.js`, `pipeline/wardrobe_fx.py`, `pipeline/wardrobe_fx_tto.py`, `pipeline/wardrobe_fx_check.py` | Interfaces 1, 2 (with part 1), 6, 7, 8; part 2's table line |
| lead / editor | `wardrobe/fx_cues/panda.json`, data | the rebuild (`wardrobe_fx_tto.py panda`, then `wardrobe_fx.py panda`) and the cues |

Rules as the Chameleon's: `node --check` on each part file, no browser for the builders, never `wardrobe_fx.py panda` /
`wardrobe_fx_tto.py panda` without `--probe` (the lead rebuilds once); after editing `wardrobe/index.html`, `grep -c
$'\r$' wardrobe/index.html` must print 0. `wardrobe_fx_inventory.py`'s `BUILT` needs nothing new (no BB script added).

## Paste-ready cue fragments (the parts' shapes; times from the sources cited, the clip researchers' entries win)

Keys as the other classes' files (`"<clip>": {"why", "cues"[, "builds"]}`); valid JSON fragments.

```json
  "threeSteps": {
    "why": "RPC_threeStep (Panda.cs:20721-21830, predicates evaluated; parts.md part 1): PlayAnimation(threeSteps, 0.2) at 0 (:21528); threeStep created at the hero, rotation x Euler(270, 90, 0) (:21728), followState: the standby at 1.4 s ends it (:21458); its three trails, off in the prefab, switched by the coroutine: fxNode1 on 0.1 (:20873) off 0.5 (:21063), fxNode2 on 0.4 (:20900) off 0.8 (:21250), fxNode3 on 1.2 (:21277) (waits :21771-21803); voices and hits: the attacks report's",
    "cues": [
    [0, "fx", "threeStep", {"rot": [270, 90, 0], "cut": 1.4, "enable": [[0.1, "fxNode1", true], [0.4, "fxNode2", true], [0.5, "fxNode1", false], [0.8, "fxNode2", false], [1.2, "fxNode3", true]]}]
    ]
  },
  "ashura": {
    "why": "RPC_ashura (Panda.cs:30346-30810): PlayAnimation(ashura, 0.2) at 0 (:30668); 0.4 s: ashuraRing at the hero, her rotation (:30510); 0.8 s: the ashura status (:30572, chaAdjust(24) = 24 s, cut at 10): the Panda tinted (1, 0, 0) (CharacterControl.cs:35484-35496; HERO_SKINS ashura, parts.md part 3) and ashuraFx on her Root bone, local identity (:35500-35510); the waits :30785-30806 (the skills report confirms)",
    "cues": [
    [0.4, "fx", "ashuraRing"],
    [0.8, "skin", "ashura", {"kill": 10}],
    [0.8, "fx", "ashura", {"bone": "Root", "kill": 10}]
    ]
  },
  "nineDragons": {
    "why": "TTO1102:Panda.<RPC_nineDragons>d__331::MoveNext@0x1d899a0 (pseudo/Panda.c:13461-13688; Bible panda-skill-reference.md Nine Dragons; the lone target 10 m ahead): nineDragons_cast at the hero at 0; dragon k = 0-7 at 0.4 + 0.11 k from Hand_R (k even) / Hand_L (Row6Hand(~k & 1)), flying the NineDragon curve (<NineDragon>d__336@0x1d6f860; parts.md T2) to the prey + 0.6 up in clamp(1.6 d / 22, 0.35, 0.7) = 0.7 s, then nineDragons_bite there (identity) and punch1 / punch2; the King at 1.6 from hero + 0.7 up + 0.4 forward (<NineKing>d__339@0x1d701c0), 0.4 s to the landing point + 0.8 up; nineDragons_kingRise at the landing point at 2.0, nineDragons_fall at 3.35 (Until(rise + 1.05 + 0.3)); the strikes, voices, the hits and their sounds: tto.md's",
    "cues": [
    [0, "fx", "tto/nineDragons_cast"],
    [0.4, "fx", "tto/nineDragons_dragon", {"k": 0, "fromBone": "Hand_R", "to": [0, 0.6, 10]}],
    [0.51, "fx", "tto/nineDragons_dragon", {"k": 1, "fromBone": "Hand_L", "to": [0, 0.6, 10]}],
    [0.62, "fx", "tto/nineDragons_dragon", {"k": 2, "fromBone": "Hand_R", "to": [0, 0.6, 10]}],
    [0.73, "fx", "tto/nineDragons_dragon", {"k": 3, "fromBone": "Hand_L", "to": [0, 0.6, 10]}],
    [0.84, "fx", "tto/nineDragons_dragon", {"k": 4, "fromBone": "Hand_R", "to": [0, 0.6, 10]}],
    [0.95, "fx", "tto/nineDragons_dragon", {"k": 5, "fromBone": "Hand_L", "to": [0, 0.6, 10]}],
    [1.06, "fx", "tto/nineDragons_dragon", {"k": 6, "fromBone": "Hand_R", "to": [0, 0.6, 10]}],
    [1.17, "fx", "tto/nineDragons_dragon", {"k": 7, "fromBone": "Hand_L", "to": [0, 0.6, 10]}],
    [1.1, "fx", "tto/nineDragons_bite", {"y": 0.6, "d": 10}],
    [1.21, "fx", "tto/nineDragons_bite", {"y": 0.6, "d": 10}],
    [1.32, "fx", "tto/nineDragons_bite", {"y": 0.6, "d": 10}],
    [1.43, "fx", "tto/nineDragons_bite", {"y": 0.6, "d": 10}],
    [1.54, "fx", "tto/nineDragons_bite", {"y": 0.6, "d": 10}],
    [1.65, "fx", "tto/nineDragons_bite", {"y": 0.6, "d": 10}],
    [1.76, "fx", "tto/nineDragons_bite", {"y": 0.6, "d": 10}],
    [1.87, "fx", "tto/nineDragons_bite", {"y": 0.6, "d": 10}],
    [1.6, "fx", "tto/nineDragons_king", {"y": 0.7, "d": 0.4, "to": [0, 0, 10]}],
    [2.0, "fx", "tto/nineDragons_kingRise", {"d": 10}],
    [3.35, "fx", "tto/nineDragons_fall", {"d": 10}]
    ]
  }
```

(The bite times are the launch + 0.7: the hand is about 9.7 m from (0, 0.6, 10), so `1.6 x 9.7 / 22` = 0.705 is
clamped to 0.7; the mover computes its own flight, so a hand nearer than 9.625 m would land up to 0.01 s sooner.) The
other part-carrying cues, shapes only:
- Drunken Fist's self look: `[0, "fx", "drunken", {"y": 0.89, "kill": 10}]`; on the target: `[t, "fx", "drunk", {"y":
  1.1, "d": 10, "kill": K}]` (K = the status, cut at 10).
- Delay Qi: `[t, "fx", "delayQi", {"kill": 6}]`. Stasis Blow's target: `[t, "fx", "paralysis", {"y": 0.6, "d": 10}]`.
- Heaven Palm's hits (`RPC_heavenPalm_hit`, sLv 2): `[t, "fx", "heavenPalm", {"d": 10, "scale": 1.5}]`.
- Raijin Ken's strike: `[t, "fx", "raijinKen_hit", {"d": 10, "rot": [0, 180, 0]}]` (LookRotation(-hitDir); the
  camera cut not drawn).
- Tempest Dance: `[0, "fx", "tto/tempestDance_aura"]`, `[0, "fx", "tto/tempestDance_trails", {"off": T, "kill": T +
  0.43}]` (T = the dance's end, tto.md's), the pulses `[t, "fx", "tto/tempestDance_pulse"]`; Tempest Dance End
  `[t, "fx", "tto/tempestDance_end"]`.
- Yin Yang Fist: `[0, "fx", "tto/yinYangFist_charge"]`, `[0.55, "fx", "tto/yinYangFist_seal"]`, `[1.75, "fx",
  "tto/yinYangFist_burst"]` (the Bible's times), the mark on the target from the first Yin pulse: `[0.55, "fx",
  "tto/yinYang", {"d": 10, "kill": 2.8}]` (scale `clamp(2 r, 1, 5)` = 1 on the standard body, AddYinYangFx@0x24af630;
  the 2 s status refreshed at 0.95 and 1.35 ends at 3.35).

## Per-effect status (`plans/fx_inventory.md` "### panda", plus what this research found)

BB, 79 prefabs: **ready, nothing to do (73):** ashuraFist, ashuraRing, auraBlast, auraField_ring, cAttack_ring,
climbingCliff_hit, climbingCliff_ring, comboLink_ring, crushingMonolith, crushingMonolith_hit, deadEffect, deathBlow,
deathBlow_ring, delayQi_fire, delayQi_ring, drunkenFist, drunkenSpin, fuujinKen_hit, fuujinKen_ring1, fuujinKen_ring2,
fuujinKen_ring3, heavenPalm (cue `scale` 1.5), heavenPalm_ring, lotusPalm, lotusPalm_ring, mysticSage_hit, nAttack_hit1,
nAttack_hit2, nAttack_punch, nAttack_wheel, psalmOfEnergy_ring, pummel_dust, pummel_hit, pummel_ogre, pummel_ogreArm1,
pummel_ogreArm2, qiBurst, qiStrike, qiStrike_hit, qiStrike_ring, raijinKen_ring1, raijinKen_ring2, rainStorm,
risingDragon, risingDragon_hit, risingDragon_ring, risingVortex, risingVortex_hit, rollAround_ring, rushingFalcon,
rushingFalcon_hit, safeGuard_hit, spTransfer (cue `to`), stasisBlow, stasisBlow_endDust, stasisBlow_ring, threeStep_hit,
tigerPounce_hit, tigerToss, timeAndTideCrane, timeAndTideMonkey, towerRush_hit, towerRush_ogre, towerRush_ring,
waterCrane, waterCrane_hit, waterMonkey, waterMonkey_hit, windCloud, and the status looks delayQi, drunken, drunk,
paralysis (not in the inventory). **Need a part (3):** `threeStep` (part 1), `raijinKen_hit` (part 2), `ashura` (the
effect is ready; the hero tint is part 3). **Dead (3, not cued):** drunkenFist_hit, qiStrike_emblem, windcloud_hit.

TTO, 15 prefabs: **ready:** tempestDance_counter, nineDragons_cast (GroundHug + Shuriken, all built); **need:**
nineDragons_bite (Noise), nineDragons_dragon (T2), nineDragons_fall (Noise), nineDragons_king (T2),
nineDragons_kingRise (Noise), tempestDance_aura / _end / _pulse (T1), tempestDance_trails (T3), yinYang (T1),
yinYangFist_burst (T4, T5), yinYangFist_charge (T1), yinYangFist_seal (T1).

## How sure I am

| item | sure | why |
|---|---|---|
| No BB layout needed; 79 build | high | `wardrobe_fx.py panda --probe` over all 79 and the raw walk (no unknown script, only the one ParticleSystem dropped) |
| Three Steps' trail times | high | the state machine worked through with every predicate evaluated (`src/Panda.txt`), the waits read at their labels |
| raijinKen_hit's graft | high | run in memory with the table line (`graft_try.txt`), the two systems compared field for field |
| Ashura's tint and Root bone | high | plain lines, predicates TRUE (`CharacterControl.cs:35484-35510`, `:15830`) |
| drunken / drunk heights | medium | the controller's bounds read as centre +- height / 2 (skin width not added) |
| HelixRibbonEmitter | high | every instruction of the five methods read; the up vector and sin / cos identified by their other uses |
| NineDragon / NineKing paths | high / medium-high | the pseudo-C read whole; the King's second sin argument from the instructions (0x1d7088f) |
| TempestTrails | high | the method read whole (bones by the children's names, Clear, emitting off, Destroy time + 0.05) |
| ERB shaders' colour | medium | the pass state is the bundle's parsed form; the fragment is inferred from the declared properties (programs compressed) |
| Standard Surface | medium | Unity's own shader; lighting through the page's scene lights is an approximation |
| Noise / Lights | low-medium | Unity's native modules, no source; values exact, the noise field approximated |

## Open questions (each with my recommended answer)

1. **Three Steps' trails.** Recommend building the `enable` option (without it the skill shows nothing but its sound).
2. **Ashura's red Panda.** Recommend the body look (the Bison's Enrage / Titan Form precedent, Bison decision 31): the
   whole hero red from the status for 10 s, with the `ashura` line emitter on her Root.
3. **Nine Dragons' bites: cue or the mover's spawn?** Recommend cues at the computed times (above): one owner per spawn,
   the times fixed by the fixed target; the mover only flies and vanishes.
4. **Noise / Lights (shared with the Monkey).** Recommend the value-noise drift and the pooled lights (the Monkey's
   question 9 answer, whichever class builds first; the other reuses it).
5. **ERB noise texture.** Recommend exporting `_Noise` (`noiseTex`) and multiplying it in (the Hovl family's shader
   does); only tto_Add_noise has one.
6. **Standard Surface's normal map.** Recommend leaving the bamboo's `_BumpMap` out (APPROX): small particles, and the
   extractor would need a second texture slot for one material.
7. **Tempest Dance's counters** (`tempestDance_counter`, spawned on an evaded attack at the attacker,
   `RPC_tempestCounter@0x1d59f30`). Recommend tto.md's call; the part is built either way (no new part).
8. **The hero's moves while dancing** (TempestSteer: the player steers; TempestGlide: a network re-sync of the remote
   copy). Recommend nothing: the owner's view of an unsteered dance stays in place.

## Offers for the Bible (never written there)

- Three Steps' trail switching (Read this first 7): a visual detail the Three Steps entry lacks.
- Heaven Palm 2's hit drawn at 1.5x (`Panda.cs:9548`).
- The three dead prefabs (drunkenFist_hit, qiStrike_emblem, windcloud_hit).
- Nine Dragons: the hand order, the dragons' Bezier and the King's weave (T2), the 0.5 s vanish.
- TTO's HelixRibbonEmitter (a TTO-only emitter script, T1) for the TTO notes.

## Verification (13/11/2026, checker; wins over the body above)

Re-derived on the office PC; probes in `checks/fx_panda_research/verify/` (git-ignored): `tto_probe.json` (the 15 TTO
prefabs, `wardrobe_fx_tto.py panda --probe`, no error), `bb_probe.json` (`wardrobe_fx.py panda --probe` of risingDragon_hit,
ashura, ashuraRing, threeStep, heavenPalm, drunken, drunk, delayQi, paralysis, raijinKen_hit), `dis.py` ->
`helix_small.asm`, `helix_rebuild.asm`, `cues_check.py`, `fk_check.py`, `cues_fixed.json` (see tto.md's Verification).

**Confirmed as written:** 79 BB prefabs in `heroes/panda/effects`; threeStep's three TrailRenderers `m_Enabled` false
(`bb_probe.json`) and `trail.js:100` dropping them; the coroutine's switches (`Panda.cs:20873`, `:20900`, `:21063`,
`:21250`, `:21277`, standby `:21458`; Yields `:21771-21803`: 0.1 / 0.4 / 0.5 / 0.8 / 1.2, standby 1.4), and the same
`enable` list in skills_b.md's `threeSteps`; raijinKen_hit's node `ParticleSystem` with no component (dropped) and
`SHURIKEN_FROM_TTO` with no `SHURIKEN_MAT` entry being the Chameleon's route (`wardrobe_fx.py:270`, `:540`); Heaven Palm's
1.5x at sLv 2 (`Panda.cs:9539-9548`; the card's maxRank 2); Delay Qi `chaAdjust(3) + 3 x QiBurstLv` (`Panda.cs:24255`;
Qi Burst maxRank 1: 6 s); `ashura` `chaAdjust(24)` (`Panda.cs:30572`) and the body look's shape (`index.html:4874-4882`,
the Bison's); the three dead prefabs (no reference in BB's `DecompiledSource` or TTO's `Panda.c`); the 15 TTO prefabs'
components: HelixRibbonEmitter 9 instances (aura 2, end 2, pulse 1, charge 1, seal 2, yinYang 1), NoiseModule 8 systems
(bite, kingRise, fall, burst), LightsModule 5 (burst), the four new-shader materials only on yinYangFist_burst,
tempestDance_trails' four children Hand_R / Hand_L (m_Time 0.3) / Foot_R / Foot_L (0.38) at local identity;
HelixRibbonEmitter's fields (`dump.cs:11767-11796`) and a spot-check of its code (`helix_small.asm`: Ends = the
smoothstep, constants -2 and 3; `helix_rebuild.asm`: `sin(t x wobbleSpeed) x wobble + 1`, the `height <= 0.001` flat
test at 0x2265160, `360 / ribbons` and the degree-to-radian factor, `turns x 2 pi`, cos then sin, the side = (cos, 0,
sin) when flat else `Vector3.up` (0x22652cf-0x226530e), `W x 0.5`, `Ends` called per point). The one CollisionModule
(nineDragons_fall's Sparks, type 1 World) is drawn today (`shuriken.js:262-268`): "World Collision" in Read this first 6 is
right.

1. **Nine Dragons' bites are on the ground, not 0.6 m up.** The bite spawns at `getSpawnPos(end)` (`Panda.c:316-361`),
   and getSpawnPos is the ground under the point (BB `Math.cs:1090-1110`: a ray from 2 m above, 4 m down): (0, 0, 10).
   The fragment's `{"y": 0.6, "d": 10}` is wrong; tto.md's `10` (d 10, y 0) is right. The whole `nineDragons`
   fragment is superseded by tto.md's corrected block (its Verification), which also has the voice, the punches and the
   eight `risingDragon_hit` strikes this fragment leaves out.
2. **T2 / Interfaces 1 and 3: no `fromBone`, the spawn spot cued.** By the Sheep's cued hand / mouth spots and the
   Sheep / Cat movers' `to` (tto.md Verification 2): the dragon cue is `{x, y, d, rot, k, to, kill}` (the hands from
   tto.md's fk table, reproduced exactly with the page's own sampling, `fk_check.py`), the King's `{y: 0.7, d: 0.4, to:
   [0, 0, 10], kill: 0.9}`. `Panda.NineDragon` takes its start from its own spawn spot (not a bone), side and c1 from `k`,
   c2 = to + 0.6 side + 2.4 up, flight from the distance (as T2 says); `Panda.NineKing` aims at `to` + 0.8 up. `api.boneMatrix`
   (Interfaces 1) stays, for T3 only.
3. **Interfaces 8, the new cue words, are `enable`, `k`, `off`** (no `fromBone`), in `wardrobe_fx_check.py:176` `OPTS`
   and the cue-format comment.
4. **The Yin mark on the target is not cued.** `[0.55, "fx", "tto/yinYang", {"d": 10, "kill": 2.8}]` is wrong twice:
   the Yin pulses reach 7 m (`SealYin`, Bible `panda-skill-reference.md:1168`; `rangeMod` 1, Mechanics reference :829),
   so a foe 10 m away never gets `yinYang` (tto.md 2.3, its question 6); and a status look on a foe is left out by the
   earlier classes (Cat decision 44, `plans/fx_cat/decisions.md:140-142`, after Sheep 4, Bat 13 / 44, Penguin 10).
   `yinYang` is built (SKILL_FX) and not cued.
5. **`drunk` and `paralysis` on the target are not cued either** (the same Cat decision 44, which names paralysis): both
   built, neither cued. `drunken` and `delayQi` (the Panda's own) stay as written (`{"y": 0.89, "kill": 10}`,
   `{"kill": 6}`).
6. **The BB fragments are the skills reports'.** `threeSteps`: skills_b.md:277-283 (adds the voice nineStep1 /
   nineStep2, Nine Steps on); `ashura`: skills_a.md:438-446 (adds the voice ashuraGate1 / ashuraGate2 and `single` on the
   Root-bone line); the values here agree with both. Paste theirs, not these.
7. **Tempest Dance's trails:** T = 5.75 (tto.md 2.2: `TempestTrails(false)` 0.75 s into the end, `Panda.c:23442`), so
   `[0, "fx", "tto/tempestDance_trails", {"off": 5.75, "kill": 6.18}]` in the `tempestDance` key; the effect outlives
   its 5 s step on the page (only the cue list changes at a step, `fxStart`). tto.md's `childBones` / `stop` are dropped
   for T3 / Interfaces 5 (its Verification 1).
8. **Minor:** the cue-format comment Interfaces 8 cites is `index.html:4690-4780` today (the Mole's build moved it); the
   part loader's comment is `:3937-4019`, `FX_PART_FILES` at `:4020`. No value changes.

Nothing missed: no summons; every TTO prefab the coroutines load is in the SKILL_FX snippet (13 cued + the counter +
`yinYang`); `clap` / `wai` have no prefabs. Calls made here (the user unavailable): items 2, 4, 5, each by the earlier
classes' decisions named.
