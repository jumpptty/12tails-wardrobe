# Sheep effects: the parts the page cannot draw yet

Research 10/11/2026 (one of the Sheep fx researchers; scope: the missing parts). Model: `plans/fx_wolf/parts.md`.
Read only. The probes are in `checks/fx_sheep_research/parts/`; each one's output is in the `.txt` next to it:
- `probe.py`: every node and component of the 13 effects (physics too), with the candidate layouts.
- `probe2.py`: what `wardrobe_fx.effect()` gives with the layouts patched in (materials, the comps the page gets).
- `probe3.py`: the projectiles' particle flags.
- `probe4.py`: which node each Animation clip moves.
- `probe5.py`: the sounds the effects play themselves.
- `scan_alphatimer.py`: every AlphaTimer and ProjectileControl in all 12 classes.

Nothing in `wardrobe/data` was written, and `wardrobe_fx.py` was never run without `--probe`. Note: on this PC
`wardrobe_fx.py`'s `BIBLE` picks `D:\12tails` (it has `12TailsOnline_Data` here too), so the probes read the game data
from there. `DecompiledSource` was read from `C:\Users\Jump\Desktop\12tails`. TTO was not consulted: these are BB
scripts.

## Read this first

1. **Hidden blocker: the game's own shader `FX/Phoenix`.** 6 of the Sheep's 9 AlphaTimer nodes use it:
   - `divinitySpear`, `divinitySword`;
   - the 4 weapons of `soulOfArms`.

   The inventory doesn't see shaders. Today the page draws these as a particle material, with a console warning
   (`mesh.js:55`). The extractor also drops the material's `_Emission`, and Phoenix needs it (below). The fix is a
   Phoenix material in `mesh.js` and one line in `wardrobe_fx.py`. 30 materials in the rip use this shader (mostly mobs
   and pets, plus Penguin `absoluteZero` and Cat `GrandCasinoArcade1`).
2. **Divinity Spear, Divinity Sword and Divinity Axe land on the enemy.** All three are placed at
   `tObject.transform.position`:
   - Divinity Spear: `Sheep.cs:31749`, then `:31759`;
   - Divinity Sword: `:30613`;
   - Divinity Axe: `:36148`.

   Under the Wolf rule ("effects on an enemy are left out") they stay out even once AlphaTimer is built. They are those
   skills' main visual, so this is a real decision (Questions, 1).
3. **Homing Light (#401) replaces the normal-attack ball.** Every stage fires `homingLight` instead of `nAttack`
   (`Sheep.cs:17394-17435`, and the same in stages 2 and 3; Bible `sheep-skill-reference.md:279`). With the
   passives-ON rule, `nAttack` is never cued. The two prefabs look the same: same material, same emitter values
   (`probe.txt` lines 1-11 vs 28-38). Without a target, homing does nothing (`Sheep_homingLight.cs:92-94`).
4. **A projectile's life is set by the hero's code, not by the prefab.** `ProjectileControl.life` is
   `1.7 × rangeMod` for `nAttack` / `homingLight` (`Sheep.cs:9343`, `:11472`; prefab 0) and `5 × rangeMod` for `cAttack`
   (`:9838`; prefab 10). `rangeMod` is 1 by default (`CharacterControl.cs:154`). So reading `life` from the data is wrong.
5. **Two effects have no EffectControl at all: the seal combos and Eden Sanctuary.** The code destroys them:
   - **Combo seal:** destroyed when a new combo forms (`Sheep.cs:10800-10802`), or when one of its 3 placed seals (each
     lives `chaAdjust(60)`, `:32284`) or the owner is gone (`Sheep_seal.cs:170-320`).
   - **Eden Sanctuary:** destroyed at 13 s (`Sheep_edenSanctuary.cs:73`, `:129-135`, `:423`).

   On the page, a combo seal would live until the next pick (repeatForever rings, a looping clip). In a looping tile
   each loop would stack another one (Questions, 5).
6. **The Charge Attack ball grows with its damage.** `Sheep_cAttack.Init` adds `clamp(0.004 × cDmg, 0, 2.5)` to the
   main glow's particle size (`Sheep_cAttack.cs:76-79`). On BB at max rank and full charge that is **+1.6 m**. The page
   needs a per-spawn size hook in `legacyParticles` (one small change in `index.html`, below).
7. **Three effects loop their own sound, and the page plays it once:**
   - `divinityAxe` (`divinityAxe.wav`);
   - `edenSanctuary` (`edenSanctuary.wav`, a 1.2 s clip looped through the effect's 13 s);
   - `lullaby_ring` (`lullaby.wav`, until the cut).

   The extractor already stores `loop: true` (`probe5.txt`). Looping it is the lead's change in `index.html` (line 3135
   plus a stop in `dispose`). It is not one of the 7 parts.
8. **No name collisions.** Every sound these 13 effects play is only in `sounds/`, none in `voices/`: `divinityAxe`,
   `divinitySpear`, `divinitySword`, `edenSanctuary`, `lullaby`, `soulOfArms`, `seal` (`probe5.txt`).
9. **Every layout is proved on the real bytes.** All 56 AlphaTimer, 20 ProjectileControl and 4 Sheep_seal instances in
   the 12 classes decode and use up exactly their bytes (AlphaTimer and ProjectileControl: `scan_alphatimer.txt`, last
   line; the 4 Sheep_seal: `probe.txt` lines 318, 341, 364, 387). Sheep_nAttack, Sheep_cAttack,
   Sheep_homingLight and Sheep_edenSanctuary have **0 field bytes**: all their fields are private. They already extract
   today (`wardrobe_fx.py:226-228` raises only when bytes are left over).

## The Sheep's set (from `plans/fx_inventory.md`, checked against the prefabs)

"Where" is where the game spawns the effect. "Enemy" means it is left out under the Wolf rule.

| effect | skill (spawn) | missing parts | where |
|---|---|---|---|
| `homingLight` | Normal Attack with Homing Light #401 (`RPC_homingLight_fire`, Instantiate `Sheep.cs:11457`) | ProjectileControl, Sheep_homingLight | hero: `firePos = mPos + (0, 1, 0.3)` local, `LookRotation(fireDir)` (`:17384-17400`) |
| `nAttack` | Normal Attack without #401 (`RPC_nAttack_fire`, `:9328`) | ProjectileControl, Sheep_nAttack | hero, same `firePos` (`:17422`) |
| `cAttack` | Charge Attack release (`RPC_cAttack`, `:9829`; called from `RPC_cAttack2` with `pos + 3·up`, Bible `:290`) | ProjectileControl, Sheep_cAttack | hero, 3 m up |
| `lullaby_ring` | Lullaby (`RPC_lullaby`, createEffect `:35708` at the hero, `Quaternion.identity`) | AlphaTimer | hero |
| `soulOfArms` | Soul of Arms (`RPC_soulOfArms_cast`, createEffect `:34118` at `tObject.collider.bounds.center`) | AlphaTimer (+ Phoenix material) | the buffed ally (the Sheep when she buffs herself) |
| `edenSanctuary` | Eden Sanctuary (`:37133` at the combo seal's position and rotation; `InitEdenSanctuary` `:37142`) | AlphaTimer, Sheep_edenSanctuary | the combo seal = the centroid of the 3 placed seals (`:32397`); seals are placed at the hero (`:8189`), so the hero |
| `sealOfAttack` / `Defense` / `Earth` / `Heaven` | the seal combo (`RPC_seal_create`, Instantiate `:10834` / `:10970` / `:11112` / `:11255`, `Quaternion.identity`) | Sheep_seal | the centroid of the 3 seals (`:32397`): the hero |
| `divinitySpear` | Divinity Spear (`RPC_divinitySpear_fire`, `:10762`) | AlphaTimer (+ Phoenix) | **enemy** (`:31749`) |
| `divinitySword` | Divinity Sword (`RPC_divinitySword_fire`, `:31117`) | AlphaTimer (+ Phoenix) | **enemy** (`:30613`) |
| `divinityAxe` | Divinity Axe (`RPC_divinityAxe_fire`, `:36700`) | AlphaTimer | **enemy** (`:36148`) |

All 13 drawn means Sheep goes from 38 of 51 to 51 of 51 ready. Under the target rule, 10 of them reach the hero's cues
(9 if `nAttack` stays unused).

## Each part

Layouts are written as `LAYOUTS` expects them (`wardrobe_fx.py:39-40`): f float, i int, b bool (4 bytes with padding),
v3. Page parts are wired as the comment above `FX_PART_FILES` says (`index.html:3039-3049`): a module
`wardrobe/fxparts/<file>.js` with `register(api)` calls `api.part(type, build)`. `build(fx, node, comp, mat, nodeDef,
data)` returns `{ node, update(dt, cam), stop?() }` or null. An unknown type is skipped without a word
(`index.html:3136`).

### AlphaTimer: `lullaby_ring`, `soulOfArms`, `edenSanctuary` (with the next part); `divinity*` (on the enemy)

**What it does in BB (`AlphaTimer.cs`).** It fades **its own node's renderer material** and draws nothing itself. It
never touches the children: `this.renderer` is used at :63, :283-312, and the child renderers are read only for
shadows, :60, :222-275.
- **Start (:38-100).**
  - Sets the times `d = FadeDelay`, `i = d + FadeEaseIn`, `m = i + FadeMiddle`, `o = m + FadeEaseOut`, from the first
    frame.
  - Picks the colour it drives:
    - `_Color`, if the shader has one (mode 1, :63-72);
    - else `_TintColor` (mode 2, :74-83);
    - else it **disables itself** (:85-87).
- **Update, each frame (:112-221), with t = time since Start:**

  | when | alpha |
  |---|---|
  | t < d | MinAlpha |
  | t < i | lerp Min → Max |
  | t < m | MaxAlpha |
  | t < o | lerp Max → Min |
  | t > o, `repeat` | restart the times (:169-199) |
  | t > o, `endDestroy` | Destroy the node (:201-207) |
  | t > o, neither | MinAlpha (:215) |

  All tests are strict `>` on the end times, so a 0-length phase is skipped and nothing divides by zero.
- **Then it writes `color.a = alpha`** into `_Color` or `_TintColor` (:276-321). `renderer.material` is Unity's
  per-renderer copy.
- `eraseShadow` switches shadows only (:222-275). It is false in every Sheep instance.
- `AlphaTimerFadeOut(n)` (:328-357) is called only by Cat (`Cat.cs:10603`), not by the Sheep.

```python
# AlphaTimer.cs:378-402 (36 bytes; all 56 instances in 10 classes decode)
"AlphaTimer": [("MinAlpha", "f"), ("MaxAlpha", "f"), ("FadeDelay", "f"), ("FadeEaseIn", "f"), ("FadeMiddle", "f"),
               ("FadeEaseOut", "f"), ("eraseShadow", "b"), ("repeat", "b"), ("endDestroy", "b")],
```

**The Sheep's 9 instances (`probe.txt`).** Shader kinds from `probe2.txt`; none has `repeat` or `endDestroy`.

| effect / node | renderer | shader → mode | Min / Max | delay / in / hold / out (s) | visible |
|---|---|---|---|---|---|
| `lullaby_ring` / `lullaby_sheep_tri` | Skinned | Additive (`add`) → `_TintColor` | 0 / 0.5 | 0 / 1 / 99 / 0 | fades in over 1 s; gone at the cut (EC life 99, followState) |
| `soulOfArms` / 4 × `Sheep_soulOfArms_tri [axe / spear / sword / trident]` | StaticMesh | FX/Phoenix → `_Color` | 0 / 1 | 0 / 0.5 / 9.2 / 0.3 | 0-10 s (EC 10 + 2) |
| `edenSanctuary` / `edenSanctuary_tri` | StaticMesh (3,744 verts) | Additive → `_TintColor` | 0 / 0.5 | 0 / 1 / 11 / 1 | 0-13 s |
| `divinityAxe` / `axe` | Skinned | Additive → `_TintColor` | 0 / 0.2 | 0 / 0.2 / 2 / 0.2 | 0-2.4 s (enemy) |
| `divinitySpear` / `root` | Skinned | FX/Phoenix → `_Color` | 0 / 0.5 | 0 / 0 / 0.5 / 0.2 | 0-0.7 s (enemy) |
| `divinitySword` / `Sheep_divinitySword` | Skinned | FX/Phoenix → `_Color` | 0 / 0.5 | 0.3 / 0.4 / 0.6 / 0.2 | 0.3-1.5 s (enemy) |

Sums, checked: lullaby 0 + 1 + 99 + 0 = 100. Soul of Arms 0 + 0.5 + 9.2 + 0.3 = 10.0. Eden 0 + 1 + 11 + 1 = 13.
Axe 0 + 0.2 + 2 + 0.2 = 2.4. Spear 0 + 0 + 0.5 + 0.2 = 0.7. Sword 0.3 + 0.4 + 0.6 + 0.2 = 1.5.

Every one of these materials is saved with alpha 0 (tint or colour .a = 0; Spear 0.502), so **without AlphaTimer they
are invisible**. That is why the game ships them faded out.

**Draws anything?** No. It only fades the mesh that StaticMesh or SkinnedMeshRenderer (`mesh.js`) already draws.

**How it plugs in: `wardrobe/fxparts/alphatimer.js`, about 35 lines.**
1. **Find the mesh lazily, on the first update**, so the component order doesn't matter: `node.children.find(o =>
   o.isMesh)`. No AlphaTimer node in any class also carries an emitter (`scan_alphatimer.txt`, "others on node":
   Animation, ShatterMesh or UVScroll only), so the first mesh child is the renderer's.
2. **Clone its material(s) once**, the way Unity's `renderer.material` copies them. Both `mesh.js`'s `mats` and
   `FX.mats` share one material per class and name, so writing to the shared one would fade every other spawn and
   effect that uses it. That was the same kind of bug as ImageEmitter's shared `repeatForever` (`index.html:3226-3227`).
   **Check:** in three r160 `Material.copy()` does not carry `onBeforeCompile`, which `fxMaterial`'s additive alpha fix
   lives in (`index.html:3084-3085`). Copy it across: `c.onBeforeCompile = m.onBeforeCompile`.
3. **Each frame, apply the alpha by the material's `blend`** (`data.materials[nodeDef.mats[0]].blend`; a
   SkinnedMeshRenderer's is in `comp.mats`):
   - `add` / `alpha` (the particle shaders' `_TintColor`): `opacity = min(1, 2 × alpha)`. This is the same rule
     `fxMaterial` uses for a saved tint (`index.html:3080`).
   - `shader:FX/Phoenix` (`_Color`): `opacity = alpha`.
   - `addsoft` and anything with neither colour: do nothing (AlphaTimer.cs:85-87).
   - `opaque` (Diffuse has `_Color`, but alpha is not drawn): do nothing.
   - Any other shader: warn.
4. **Return** `"destroy"` only for `endDestroy` (one instance in other classes).

**The Phoenix material it needs (in `mesh.js` `material()`, about 15 lines).**
- What the shader does: `Phoenix.shader` (rip `Assets/Resources/gameassets/shader/Phoenix.shader:1-23`) is
  fixed-function lit: `Ambient` / `Diffuse [_Color]`, `Emission [_Emission]`. It computes `texture × lit colour ×
  2`, with alpha `texture.a × _Color.a`, then `Blend SrcAlpha OneMinusSrcAlpha`, `AlphaTest Greater 0`, and ZWrite on
  (not switched off).
- Page version: a `MeshLambertMaterial` with:
  - `map`, plus `emissiveMap = map`;
  - `color = 2 × _Color.rgb` and `emissive = 2 × _Emission.rgb`, both gamma (`SRGBColorSpace`);
  - `transparent`, `opacity = _Color.a`, `alphaTest ≈ 1/255`, both sides;
  - `depthWrite` as the game has it (on).
- The extractor must keep `_Emission`. In `wardrobe_fx.py` `material()` (:192-194) add `"emission":
  colors.get("_Emission")`. The Sheep's values: Spear and Sword 0.502, Soul of Arms 0.251. Doubled, the texture is half
  to fully self-lit, so the page's lights matter little.
- **Approximated:** the game's ambient and light colours are not known, and "double" clamps at 1 in the game.

**Other classes (`plans/fx_inventory.md` "Per missing part", recounted from `fx_inventory.json`).** AlphaTimer alone
blocks **34 more effects in 8 classes**: bat 2, bison 7, cat 2, mole 2, monkey 6, panda 10, penguin 2, rabbit 3. 40 of
other classes' effects need it in all (bison 9, cat 3, panda 12 and whale 1 also need something else).

Their shader kinds (`scan_alphatimer.txt`), to check when those classes come:
- most are `add` / `alpha` (fine);
- `Transparent/Opaque1` ×3: bison `earthSmasher`, `massStun`; cat `supportFire_cannon`;
- built-in 30 ×2: rabbit `millionaire_peppon`, whale `bowlingWhale`;
- built-in 34 ×1: monkey `stoneHammer`;
- Phoenix ×1: penguin `absoluteZero`;
- `opaque` ×1: panda `raijinKen_hit`;
- monkey `blazingArrow`'s node has two renderers (a SkinnedMeshRenderer `add` and a TrailRenderer); Unity's
  `this.renderer` is the first one.

### Sheep_seal: `sealOfAttack`, `sealOfDefense`, `sealOfEarth`, `sealOfHeaven`

**What it does in BB (`Sheep_seal.cs`).** Game logic only: **it draws nothing.**
- **`Init(owner, seal1, seal2, seal3)` (:40-149):** called right after the Instantiate (`Sheep.cs:11392-11395`). It
  stores the owner and the 3 placed seals, and sets the buff radius to `max(6, ceil(flat distance to each seal))`,
  capped at 30 (:65-125).
- **Update (:153-325):**
  - Before Init it does nothing (:161-166).
  - Every 5 s it gives allies in that radius the status named by `mSealType` (`RPC_AddStatus(<seal>, 1, 6, ...)`,
    :197-307; owner side only, :205).
  - When the owner or any of the 3 seals is gone, it destroys its node (:170-195, :320).

```python
# Sheep_seal.cs:348 (4 bytes; all 4 instances decode: mSealType 0 attack, 1 defense, 2 earth, 3 heaven)
"Sheep_seal": [("mSealType", "i")],
```

**How it plugs in.** Only the `LAYOUTS` line; the page needs **no code** (an unknown type is skipped). Everything a
combo seal shows is already built: two RingEmitters (one repeatForever), a SkinnedMeshRenderer on a looping 2 s clip,
and its `seal` sound.

**Lifetime.** There is no EffectControl. On the page it lives until the next pick unless a cue's `kill` ends it
(Questions, 5). It unblocks all 4 combo effects.

### ProjectileControl + Sheep_nAttack / Sheep_homingLight / Sheep_cAttack: `homingLight`, `nAttack`, `cAttack`

**ProjectileControl (`ProjectileControl.cs`) is data only.**
- `Init(owner)` sets `isInitialized` and `OwnerID` (:21-51).
- It has no Update: it neither moves nor draws.
- In every class the projectile's own script reads it.

```python
# ProjectileControl.cs:72-87 (32 bytes; all 20 instances in 8 classes decode). life is overwritten by the hero's code
"ProjectileControl": [("life", "f"), ("dmg", "f"), ("velocity", "v3"), ("OwnerID", "i"), ("isInitialized", "b"),
                      ("isDestroyed", "b")],
```

The Sheep's values: velocity (0, 0, 12) for `nAttack` / `homingLight` and (0, 0, 8) for `cAttack`; life 0 / 0 / 10
(`probe.txt` lines 10, 37, 21).

**The three movers (0 field bytes each) do the same thing.**
1. **Awake:** set the Rigidbody's velocity to `transform.TransformDirection(v)`.
   - `Sheep_nAttack` uses `ProjectileControl.velocity` (`Sheep_nAttack.cs:48-51`).
   - `Sheep_homingLight` uses its own `(0, 0, 12)` (`Sheep_homingLight.cs:26`, :51).
   - `Sheep_cAttack` uses its own `(0, 0, 8)` (`Sheep_cAttack.cs:28`, :57).

   All three equal the prefab's ProjectileControl velocity.
2. **FixedUpdate:** destroy the node at `life` (`Sheep_nAttack.cs:70-80`, `Sheep_homingLight.cs:77-86`,
   `Sheep_cAttack.cs:112-121`).
3. **Homing:** every 0.1 s, turn toward the target by 0.15 rad (homingLight, :92-113) or 0.1 rad (cAttack, :127-148).
   This needs a target GameObject (`InitTarget` / `Init(tObject)`, `Sheep.cs:11500-11511`, :9869-9872). There is none
   here, so the ball flies straight.

The Rigidbody has no gravity, drag 0 and its rotation frozen (`m_Constraints 112`, `probe.txt:5`), so the speed is
constant. A hit on any collider that isn't the owner's layer or layer 1 / 2 destroys the ball
(`Sheep_nAttack.cs:223-241`, `Sheep_cAttack.cs:223-388`). That includes the ground, and the hit effect lands on the
target (out).

**`Sheep_cAttack.Init(tObject, cDmg)` (:69-101): the growing ball.** It adds `clamp(0.004 × cDmg, 0, 2.5)` to the
root emitter's `minSize` and `maxSize`. Step by step, at max rank:
1. `cDmg = clamp((1 + 0.2 × Benediction) × n × ATK, ATK, 100 × (Lv + OverLimit × Lv))` (`Sheep.cs:9787-9810`).
   OverLimit #462 is never on BB (Bible `:291`), so the cap is 100 × 4 = 400 at Charge Attack 4.
2. The tile holds 0.8 + 4 = 4.8 s, so `n = floor(4.8 − 0.8) = 4`.
3. 4 × ATK ≥ 400 for any ATK ≥ 100, so cDmg = 400.
4. Size added = 0.004 × 400 = **1.6 m**.
5. The main glow goes from 0.3-0.5 to 1.9-2.1 m; the child sparks are unchanged.

**What the particles look like.** The ball is a legacy emitter:
- `nAttack` / `homingLight`: **world-space** particles, 15/s, 0.4 s each, so a comet tail behind the moving ball
  (`probe3.txt`).
- `cAttack`: local glow plus world-space sparks.
- `legacyParticles` already draws both (`index.html:3328-3392`).
- Their `emitterVelocityScale` (0.05: the tail inherits 0.6 m/s) is not modelled. That is minor.

**How it plugs in: `wardrobe/fxparts/sheep.js`, about 20 lines.**
- One builder registered for the three types.
- Velocity: `vA(v).applyQuaternion(fx.uQuat(node))`, taken at spawn (the cue's `rot` is already on the root,
  `index.html:3121-3124`).
- Each frame: `node.position.addScaledVector(vel, dt)`.
- Its own timer returns `"destroy"` at the code's life: **1.7 / 1.7 / 5 s** (`Sheep.cs:9343`, `:11472`, `:9838`).
  That is 20.4 m / 20.4 m / 40 m.
- For `Sheep_cAttack`, add 1.6 m to the node's glow: `fx.emitters.find(e => e.node === node && e.addSize)?.addSize(1.6)`.
- `ProjectileControl` itself needs no page code.

The size hook is a lead's change in `index.html` `legacyParticles`. It must not mutate the shared `em`:
- :3330 add `sizeAdd = 0` to the `let`;
- :3345 `size: rnd(em.minSize, em.maxSize) + sizeAdd`;
- :3349 add `addSize(a) { sizeAdd += a; },` to the returned object.

**Cue options these effects need (the times come from the attacks report).**
- `homingLight` / `nAttack`: `{"d": 0.3, "y": 1, "rot": [<pitch>, 0, 0]}` (`firePos`, `Sheep.cs:17384-17389`).
  - `fireDir = tDir − (0, 1, 0.3)`, where `tDir = target − hero` (`doNormalAttack`, `:9016-9060`).
  - With the target on the ground 10 m ahead: pitch = atan(1 / 9.7) = **5.89°** down (Unity Euler x +5.89).
  - The ball then meets the ground at the target after √(9.7² + 1²) = 9.75 m, that is 9.75 / 12 = **0.81 s**. Its
    0.3 m sphere touches about 0.57 s in.
  - Pass `kill` for that ending, or none for a full 1.7 s miss (Questions, 3).
- `cAttack`: `{"y": 3}` plus a `rot` from its `dir`. The attacks report traces `RPC_cAttack2`.

### Sheep_edenSanctuary: `edenSanctuary` (with AlphaTimer)

**What it does in BB (`Sheep_edenSanctuary.cs`).**
1. **`InitEdenSanctuary(owner)` (:25-88):** reached by `SendMessage` in the spawn frame (`Sheep.cs:37142`). It plays
   `create` once (:64-67) and sets the end time to now + **12 s** (:73) and the first heal tick to +0.5 s (:76).
2. **Update (:92-226):** owner side only, every 2 s, gives every character within 18 m the `sanctuary` status (:144-208).
   After 12 s, or with the owner gone, it starts `DestroySanctuary` (:129-135, :219).
3. **`DestroySanctuary` (:358-425):** `CrossFade("destroy", 0.2)` (:409), waits 1 s (:423), then destroys the effect
   (:372). Total **13 s**.

**The clips (`probe4.txt`).**
- `create` lifts `edenSanctuary_tri` from y −10 to 0 in 1 s.
- `destroy` sinks it from 0 back to −10 in 1 s.
- The cross-fade joins two equal poses (0 to 0), so a plain switch is exact.

This matches the AlphaTimer's 1 s fade-in, 11 s hold and 1 s fade-out (0-13 s). The page's Animation part already plays
`create` on its own (default clip, `play` true: `probe2.txt`).

**Draws anything?** No. It times the clip switch and the end. 0 field bytes: nothing to decode.

**How it plugs in: `wardrobe/fxparts/sheep.js`, about 10 lines.**
- At 12 s, call `fx.emitters.find(e => e.node === node && e.play)?.play("destroy")`.
- At 13 s, return `"destroy"`. The root goes, so the effect is disposed, repeatForever rings and vortex included.

This needs a `play(name)` on `mesh.js`'s Animation emitter, about 6 lines in `mesh.js:121-144`: make `clip` / `tracks`
/ `len` / `wrap` lets set by a `use(name)`, and `play(name) { use(name); t = 0; }`. The data already carries both clips
(`c.clips`).

## Rank by value (effects unblocked / effort)

| rank | part | Sheep effects ready (on the hero) | other classes | work |
|---|---|---|---|---|
| 1 | Sheep_seal | 4 (all on the hero) | 0 | 1 `LAYOUTS` line + `BUILT`; no page code |
| 2 | AlphaTimer (+ Phoenix material, `_Emission`) | 5 alone: `lullaby_ring`, `soulOfArms` (self?), plus the 3 `divinity*` on the enemy | **34 alone, 40 in all** | about 35 lines (`alphatimer.js`) + 15 (`mesh.js` Phoenix) + 2 lines in `wardrobe_fx.py`; 2-3 h |
| 3 | ProjectileControl + the 3 movers | 3 (`homingLight`, `cAttack`; `nAttack` unused with #401) | ProjectileControl alone unblocks none (each class has its own mover) | about 20 lines (`sheep.js`) + 3 (`index.html` `addSize`) + 1 `LAYOUTS` line; 1 h |
| 4 | Sheep_edenSanctuary | 1 (`edenSanctuary`, needs rank 2) | 0 | about 10 lines (`sheep.js`) + 6 (`mesh.js` `play`); 1 h |

After all four, add to `BUILT` in `pipeline/wardrobe_fx_inventory.py`: `AlphaTimer`, `ProjectileControl`, `Sheep_seal`,
`Sheep_nAttack`, `Sheep_homingLight`, `Sheep_cAttack`, `Sheep_edenSanctuary`. Then run it again (the recipe's rule).

## Who builds what (never two owners for one file; as `plans/fx_wolf/build_rules.md`)

| agent | owns | builds |
|---|---|---|
| A: alpha | `wardrobe/fxparts/alphatimer.js` (new), `wardrobe/fxparts/mesh.js` | AlphaTimer; the FX/Phoenix material in `material()`; the Animation emitter's `play(name)` |
| B: sheep | `wardrobe/fxparts/sheep.js` (new) | the Sheep_nAttack / Sheep_homingLight / Sheep_cAttack movers; Sheep_edenSanctuary |
| lead | `pipeline/wardrobe_fx.py`, `wardrobe/index.html`, `pipeline/wardrobe_fx_inventory.py`, `wardrobe/fx_cues/sheep.json` | `LAYOUTS` ×3 and `material()` `"emission"`; `FX_PART_FILES` += `"alphatimer"`, `"sheep"`; `legacyParticles` `addSize`; looping AudioSource (optional); `BUILT`; the rebuild and the cues |

The interfaces are fixed up front, so A and B run in parallel:
- the Animation emitter gets `.play(name)` (A);
- `legacyParticles` gets `.addSize(metres)` (lead);
- the data's materials get `emission` (lead).

The whole job is about 100 lines, so one agent doing A then B is just as fine. Rules as in the Wolf's: `node --check`,
no browser, never `wardrobe_fx.py sheep` without `--probe` (the lead rebuilds once).

## How sure I am

| item | sure | why |
|---|---|---|
| The 3 layouts | high | Every instance in every class uses up exactly its bytes (56 / 20 / 4), and the values make sense (fades 0..1, speeds 8 / 12, seal types 0-3). |
| AlphaTimer picks `_TintColor` on the particle Additive shader | medium-high | Unity's `HasProperty` asks the shader, and Particles/Additive has no `_Color`. These materials keep a stale `_Color` but are saved with tint alpha 0, which only makes sense if the timer drives the tint. |
| Phoenix as Lambert + emissive | medium | The shader source is clear, but the game's light colours aren't known. |
| Projectile lives and the 1.6 m size | high | Bare code lines; the cap reasoning follows the Bible's own decode (`:291`). |
| The ball ends at the ground | medium | Any non-owner collider destroys it (`Sheep_nAttack.cs:223-241`); that the terrain counts is inferred. |
| Eden's 12 + 1 s and the clip switch | certain | Bare literals; the two clips' poses come from `probe4.txt`. |

## Questions for the user

1. **Divinity Spear / Sword / Axe.** The game puts them on the enemy. Leave them out (as the Wolf's hits), or show
   them at the target point 10 m ahead (the Wolf's cast-target rule)?
2. **Soul of Arms.** It goes on the buffed ally. Show it on the Sheep herself, as a self-buff?
3. **The Normal Attack ball (`homingLight` with Homing Light on; it looks the same as `nAttack`).** Let it fly the full
   1.7 s (20.4 m, a miss), or end it where it meets the ground at the 10 m target (about 0.8 s)? The same choice for the
   Charge Attack ball (5 s, 40 m).
4. **The Charge Attack ball's size.** Show BB's max (+1.6 m on the glow: Charge Attack 4, full charge)?
5. **The seal combo (`sealOf*`, 60 s or more in the game) and Eden Sanctuary (13 s).** In a looping tile they would
   pile up. End each at the loop's end with `kill`, or keep one standing (the game replaces the old combo when a new one
   forms, `Sheep.cs:10800-10802`)?

## Verification (2026-11-10)

An independent re-trace of every file:line, serialized field and number above. The sources were BB `DecompiledSource\*.cs`
(office: `C:\Users\Jump\Desktop\12tails`), the probe outputs in `checks/fx_sheep_research/parts/`, the rip's `Phoenix.shader`
and `.mat` files, and the repo's `index.html`, `fxparts/mesh.js`, `wardrobe_fx.py` and `fx_inventory.json`. The numbers are
re-derived by `checks/fx_sheep_research/verify/tto_parts_numbers.py`, which exits OK.

**Checked and holding:**
- Enemy placement:
  - Divinity Spear `Sheep.cs:31749` (`tPos = tObject.transform.position`), then `:31759`.
  - Divinity Sword `:30613` and Axe `:36148` (both `tObject.transform.position`).
  - The fire functions instantiate at that position: `:10762`, `:31117`, `:36700`.
- Homing Light: `:17394` `hasSkill(401)` leads to `RPC_homingLight_fire` (`:17400`), else `RPC_nAttack_fire` (`:17422`).
  `firePos` / `fireDir` are set at `:17384` / `:17389`. Bible `:279` agrees.
- Projectile lives: `:9343` and `:11472` are `1.7f * rangeMod`; `:9838` is `5 * rangeMod`; `CharacterControl.cs:154` sets
  `rangeMod = 1f`.
- The seal combo is destroyed at `:10802`; the placed seal's life is `chaAdjust(60)` at `:32284`.
- `Sheep_seal.cs`:
  - Init at `:40`; the radius is `max(6, ceil(flat distance))` capped at 30 (`:119`).
  - Update at `:153`; the owner check at `:205`; every 5 s (`:213`); `RPC_AddStatus(<seal>, 1, 6, 0, owner)` at `:268-304`.
  - Destroy at `:320`; `mSealType` at `:348`. The enum order is attack, defense, earth, heaven.
- `Sheep_edenSanctuary.cs`:
  - `Play("create")` `:64`; `+12` `:73`; `+0.5` `:76`.
  - The end check `:129-135` runs on every client; the heal tick is owner-only (`:152`), every 2 s, 18 m (`:160-205`).
  - `CrossFade("destroy", 0.2)` `:409`; `WaitForSeconds(1)` `:423`; Destroy `:372`.
- `AlphaTimer.cs`:
  - Start `:38`; `HasProperty("_Color")` `:63`; `_TintColor` `:74`; `enabled = false` `:87`.
  - The strict `>` phase tests, then `repeat` `:169` / `endDestroy` `:201-207` / `MinAlpha` `:215`.
  - The colour writes `:283-312`; fields `:378-402`; `AlphaTimerFadeOut` `:328`, called only by `Cat.cs:10603`.
- `ProjectileControl.cs` fields `:72-87`. The three movers' Awake velocities, FixedUpdate destroys and homing steps match
  their lines. All their fields are private.
- `Sheep_cAttack.cs:76` / `:79` (`Clamp(0.004 × cDmg, 0, 2.5)` on `maxSize` / `minSize`).
- cDmg at `Sheep.cs:9807-9810` is `n = floor(Time − actionTime − 1.3)`, and `RPC_cAttack` runs 0.5 s after the release
  (Bible `:290`). With the SEQ's `cAttack1@0.8 cAttack0*~@4` hold that is `floor(4.8 + 0.5 − 1.3) = 4`, the report's
  `floor(4.8 − 0.8)`. So cDmg = 400 and the glow grows 1.6 m.
- `index.html`:
  - The parts comment `:3040-3049`; the tint opacity `:3080`; `onBeforeCompile` `:3084-3085`; the cue's root
    placement and `rot` (Unity YXZ) `:3121-3124`.
  - The AudioSource is played once `:3135`; an unknown type is skipped `:3136`; the per-spawn `repeatForever` `:3226-3227`.
  - `legacyParticles` `:3328`, with its `let` `:3330`, `size:` `:3345` and `return` `:3349`.
- `mesh.js:55` (the warning) and `:121-144` (the Animation part, a single fixed clip).
- `wardrobe_fx.py:39-40` (LAYOUTS), `:192-194` (`material()` keeps only `_TintColor` / `_Color`), `:226-228`.
- `Phoenix.shader:1-23` reads as described. Exactly 30 `.mat` files use its GUID (`bad00689...`), `absoluteZero` and
  `GrandCasinoArcade1` among them.
- `probe.txt`:
  - AlphaTimer values at lines 55 / 83 / 128 / 143 / 168 / 244-279.
  - The EffectControl lives: lullaby 99 with followState; soulOfArms 10 + 2; none on Eden or the seals.
  - Rigidbody `m_Constraints 112` (line 5); SphereCollider radius 0.3 (0.5 for cAttack).
- `probe3.txt`: 15/s, 0.4 s, world space, `emitterVelocityScale` 0.05.
- `probe4.txt`: Eden's clips move y from −10 to 0 and back.
- `probe5.txt`: the loop flags. No voice name equals one of these sounds.
- Counts recounted from `fx_inventory.json` with the inventory's `BUILT`:
  - AlphaTimer alone blocks 34 effects in 8 classes, and 40 need it, per class as stated.
  - The Sheep has 38 of 51 effects ready, and the 13 blocked ones are exactly the table's.
  - The shader kinds in `scan_alphatimer.txt` (Phoenix 7 = the Sheep's 6 + Penguin's 1) match.
- The cue numbers: pitch atan(1 / 9.7) = 5.89°; 9.75 m / 12 = 0.81 s; the sphere touches at 0.57 s; 20.4 / 40 m; tail 0.6 m/s.

**Corrections made in the text above (old -> new, with the proof):**
1. Read this first 7: `edenSanctuary.wav, 13 s` -> `a 1.2 s clip looped through the effect's 13 s`. The rip's
   `sounds\edenSanctuary.wav` is 1.199 s long; 13 s is the effect's life (`Sheep_edenSanctuary.cs:73`, `:423`).
2. Read this first 9: the 4 Sheep_seal instances are cited from `scan_alphatimer.txt`'s last line, which reads only
   `{'AlphaTimer ok': 56, 'ProjectileControl ok': 20}`. New source: `probe.txt` lines 318 / 341 / 364 / 387
   (`mSealType` 0 / 1 / 2 / 3).
3. The table's `homingLight` row: `firePos ... (:17394-17400)` -> `(:17384-17400)`. `firePos` is set at `Sheep.cs:17384`
   and `fireDir` at `:17389`; `:17394-17400` is only the `hasSkill(401)` branch.
4. ProjectileControl values: `life 0 / 0 / 10 (probe.txt lines 10, 21, 37)` -> `lines 10, 37, 21`. The values are in the
   order nAttack / homingLight / cAttack, but line 21 is cAttack's (life 10) and line 37 is homingLight's (life 0).

**Notes (not errors):**
- `Sheep_nAttack.cs:166-172` also destroys the ball on a same-layer character other than the owner (Holy Orb's ally heal).
  With no allies on the page this changes nothing.
- The `AlphaTimer.cs` "Update (:112-221)" range starts inside the method (declared at `:104`). The cited lines are right.

**Unresolved (not disproved, not proved here):**
- That the terrain counts as a collider that ends the ball (the report's own "medium").
- That the Additive particle shader has no `_Color` property, so AlphaTimer drives `_TintColor`. The materials keep a stale
  `_Color`, and the shader's property list was not read here.
- The Phoenix look (Lambert + emissive) against the game's lights: not checkable offline.
