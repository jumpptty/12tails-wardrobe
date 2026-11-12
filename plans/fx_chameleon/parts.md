# Chameleon effects: the parts the page cannot draw yet (or draws wrongly)

Research 13/11/2026, home PC (one of the Chameleon fx researchers; scope: every part the Chameleon's effects need: the
inventory's 57, the 14 Chameleon prefabs it does not list, the status looks `CharacterControl.cs` loads, the shaders, the
hero looks the statuses put on her, and the released TTO skills' prefabs). Models: `plans/fx_penguin/parts.md`,
`plans/fx_sheep/parts.md`, `plans/fx_bat/parts.md`, `plans/fx_bison/parts.md`, `plans/fx_cat/parts.md`. Read only:
nothing in `wardrobe/data` was written; `wardrobe_fx.py` / `wardrobe_fx_tto.py` ran with `--probe` only (or were
imported read only); no browser. `Chameleon.cs`, `Chameleon_nAttack.cs`, `Chameleon_campFire.cs`,
`Chameleon_needlePrison.cs`, `ChameleonEquipment.cs`, `CharacterControl.cs`, `Math.cs` lines are
`D:\12tails\DecompiledSource\<file>`; TTO is `TTO1102:` = `D:\12tails\DecompiledSource_TTO_2026-11-02` (`dump.cs`,
`methods.tsv`, `pseudo/Chameleon.c`, the client's `GameAssembly.dll` disassembled at the RVAs `dump.cs` gives).

Probes (read only, outputs beside them) in `checks/fx_chameleon_research/parts/` (git-ignored):
- `probe.py` -> `probe.txt`, `summary.txt`: all 71 prefabs in `heroes/chameleon/effects` through `wardrobe_fx.effect()`
  with an unknown script's field bytes and raw words, every material's blend, and the components `effect()` drops. Last
  line: `UNKNOWN scripts: Chameleon_campFire [4, 4], Chameleon_nAttack [0, 0], Chameleon_needlePrison [8]`.
- `probe_ps.py` -> `probe_ps.txt`, `ps_sum.py` -> `ps_sum.txt`: the full type trees of the dropped components
  (thunderDragon_ring2's and zeroShot_ring's five Unity 3.5 ParticleSystems, tormentRain_fire's legacy emitters and
  WorldParticleCollider); `ps_mats.py` -> `ps_mats.txt`: the systems' BB materials through `wardrobe_fx.material()`.
- `mesh_probe.py` -> `mesh_probe.txt`: node rotations, mesh bounds, Animation clips, and the saved floats / colours of
  the materials that matter (`_AdditiveRange`, FX/Invisible's tint ...); `clip_probe.py` -> `clip_probe.txt`
  (needlePrison_arrow's clip keys); `ref_probe.py` -> `ref_probe.txt` (Chameleon_needlePrison's reference).
- `shader_probe.py` -> `shaders.txt`: the compiled text of `FX/Invisible`, `FX/Blend`, `FX/Camaflage`,
  `Self-Illumin/DoubleTexture`, `Transparent/AdditiveAlpha` from BB's data (the rip's `.shader` files of the first three
  are stubs).
- `tto_bbcopies.json`: `wardrobe_fx_tto.py chameleon --probe` of TTO's copies of the blocked BB prefabs;
  `tto_probe.json` + `tto_summary.py` -> `tto_summary.txt`: the 27 prefabs of the released TTO skills (apexHunt_*,
  chainLightning_*, venomPhantom_*); `tto_prey.json` (preyFx); `catalog_keys.py` / `catalog_all.py` -> `catalog_*.txt`;
  `tto_mat_probe.py` -> `tto_mat_probe.txt` (the spirit materials' texture slots).
- `disasm.py` -> `disasm_ChameleonLightning.txt`, `disasm_ChameleonAfterimage.txt`, `disasm_ChameleonPreyReticle.txt`
  (capstone, calls named from `methods.tsv`, float constants shown); `shader_dxbc.py` -> `dxbc_ChameleonSpirit.txt`
  (the TTO shader's pass state and D3D11 programs).
- `calc.py` -> `calc.txt`: the Combo arrow's flight to the standard target body, the Needle Prison ring, the rain.

## Read this first

1. **Three Chameleon scripts and one Unity component block or spoil nine BB effects; two shaders and two hero looks are
   missing.**
   | effect | what blocks it | today |
   |---|---|---|
   | `campFire1`, `campFire2` | `Chameleon_campFire` (4 bytes, no layout) | **not buildable**: `wardrobe_fx.py` raises on the bytes |
   | `needlePrison` | `Chameleon_needlePrison` (8 bytes, no layout); it spawns 16 `needlePrison_arrow` | **not buildable** |
   | `nAttack` (every Combo / Left Stride / Double Strider arrow) | `Chameleon_nAttack` (0 bytes): the prefab has **no mesh**: the arrow drawn is a copy of the hero's worn arrow | builds, draws **nothing**, does not move |
   | `clearArrow` | `Chameleon_nAttack` (the mover, the worn arrow's mesh swap); `FX/Invisible` on its mesh | builds, a still green smudge (fxMaterial's fallback) |
   | `thunderDragon_ring2`, `zeroShot_ring` | Unity 3.5's ParticleSystem (2 + 3 systems), dropped by `effect()` | build without their sparks / lightning dots / zero-shot bursts |
   | `tormentRain_fire` | `WorldParticleCollider` (bounce 0: the arrows stick in the ground), dropped | the arrows fall through the floor |
   | `thunderDragon_ring2` | game's `Self-Illumin/DoubleTexture` on the dragon skeleton mesh | drawn as a particle material (warning) |
   | `needlePrison_arrow` | game's `Transparent/AdditiveAlpha` on its skinned arrow | drawn as a particle material (warning) |
   | the hero under `blend` (Charge Attack's charge, Perfect Blend) / `invisible` (True / Mass Invisibility, Clear Arrow's condition) | `FX/Blend` / `FX/Invisible` on every Diffuse renderer of the character (`CharacterControl.cs:36665-36940`, `:32640-32690`) | not drawn: the hero looks normal |
2. **The inventory misses 14 prefabs; none of the unlisted ones blocks beyond the table above.** They come from
   - the status looks `CharacterControl.cs` loads: `Immunity` (`:36595`), `needlePrison` (`:36629`), `invisible`
     (`:36949`), `venomShock` (`:36991`, on the poisoned target), `fatalStrike` (`:37077`, two, on the hands),
     `rustyDecay` (`:37161`, on the target);
   - a concatenated name: `campFire1` / `campFire2` = `"Effects/campFire" + sLv` (`Chameleon.cs:9430`);
   - `Chameleon_nAttack.cs:205` (`fatalStrike` on a Fatal Strike arrow) and `Chameleon_needlePrison.cs:47`
     (`mPrisonArrow` = `needlePrison_arrow`, `ref_probe.txt`);
   - five dead prefabs no code loads (grep over all of `DecompiledSource`): `cAttack`, `cAttack_effect`, `quickFire_hit`,
     `poisonArrow`, `poisonArrow_ring` (built parts only; nothing to do).
   `Immunity`, `invisible`'s look, `fatalStrike`, `needlePrison`, `needlePrison_arrow`, `campFire1/2` have **no
   EffectControl** (`probe.txt`): they live until the status ends (`CharacterControl.cs:16289`, `:16558`, `:16590`
   destroy them by name) or the script's timer: on the page, the cue's `kill`. Tool gap (as the Penguin's and the
   Bat's): `wardrobe_fx_inventory.py` sees neither status looks, concatenated names nor shaders.
3. **Built since the inventory, nothing to do:** `particles.js` draws `Particles/AdditiveOffset` (`slayerEye`,
   `slayerMark1/2`, `nAttack_hit1`, `skinShift_chameleon` on a StaticMesh: mesh.js hands it to `api.shaders`),
   `Particles/MultiplyOffset` (`vitalityStrike_hit`) and built-in 205 `multiply` (`needlePoison_dust`); `premul` (207)
   draws `chameleon_dead`; built-in 7 `opaque` draws `Camp_Fire`, `Chameleon_tent`, `finalentrapment`. Every
   BoltEmitter (thunderDragon_ring1, the four allXSlayer_hit, allSlain_hit) has its own `TargetNode` in the prefab
   (`probe.txt`: TargetNode 3 / 8), so the Bat's no-target fix doesn't matter here.
4. **The Combo arrow is the hero's own worn arrow, copied.** `Chameleon_nAttack.Init` (`Chameleon_nAttack.cs:74-325`):
   Instantiate `mWep2` (the right-hand piece, `ChameleonEquipment.cs:1712-1715`: `mWep1` = getWeapon(code, 1) on
   `mount_Hand_L`, the bow; `mWep2` = getWeapon(code, 2) on `mount_Hand_R`, the arrow), or `mWep1` with the Snooker
   weapon `w_chm25` (`:114-128`: the ball flies), parented to the projectile at local 0, `Euler(0, 270, 270)` (`:150`),
   its renderers on (`:177`). On the page that is the prop in slot **L** (the Chameleon's second piece; slot R for
   `snookerBall`). Interfaces 1.
5. **Eighteen coroutines hide the hand arrow while a shot is out** (`mWep2`'s renderers off, then on again): nAttack1
   (`:15538` / `:15802`), cAttack2 (`:17399` / `:17113`), cast1 (`:18512`, no re-show in its range), immunity (`:19141` /
   `:18914`), quickFire (`:19420` / `:19975`), needlePrison (`:21653` / `:21793`), massShot (`:22468` / `:22667`),
   poisonVolley (`:23206` / `:23399`), venomShock (`:24253` / `:23994`), tormentRain (`:25482` / `:25550`), leftStride
   (`:26787` / `:26846`), rightStride (`:28001` / `:28060`), bloodBurn (`:30117` / `:29878`), slayer_fire (`:31967` /
   `:31705`), allSlayer_fire (`:32974` / `:33502`), skinShift (`:35142` / `:34883`), rustyDecay (`:35820` / `:35561`),
   zeroShot (`:37366` / `:37249`) (off / on lines; an "on" line above its "off" is an earlier state of the same flattened
   state machine). A cue kind for it: Interfaces 2; the times are the clip researchers'.
6. **The hero looks are the own-team view.** Both statuses switch the character's renderers by the **viewer's** layer
   (`CharacterControl.cs:32494-32520`, `:36665-36700`): another team sees `FX/Camaflage` (a refraction of the screen
   behind, a 3-texel shimmer: `shaders.txt`) or nothing (Erase Senses #412); her own team and the player herself see
   `FX/Blend` / `FX/Invisible`: the texture at 35 % plus a tinted outline. The page shows the player's own hero, so the
   own-team look (question 4).
7. **The ParticleSystems: TTO's copies match BB's field for field** (`tto_bbcopies.json` against `ps_sum.txt`: life,
   speed, size, shape, bursts, renderer modes, materials `tto_zeroShot1/2` = `Legacy Shaders/Particles/Multiply
   (Double)` = BB's `multiply2`, `tto_spark3` ... `addsoft` as BB). The Bison's / Cat's graft (`SHURIKEN_FROM_TTO`)
   covers them, but **node matching by name breaks here**: thunderDragon_ring2 has two nodes named `ParticleSystem`,
   zeroShot_ring three named `Particle System` (two at the same position), and TTO's node order differs from BB's (TTO
   node 1 is a system, BB node 1 a LineEmitter). Match by (node name, the renderer's first material without `tto_`):
   part 7.
8. **TTO's released skills bring three new scripts and a shader** (`tto_summary.txt`): `ChameleonLightning` (7 prefabs:
   chainLightning_arrow / _bolt / _boltHot / _draw / _overload / _zapHot, venomPhantom_echo), `ChameleonAfterimage`
   (venomPhantom_ghost), `ChameleonPreyReticle` (preyFx, Apex Hunt's mark on a prey), and `TTO/ChameleonSpirit`
   (venomPhantom_ghost's body, apexHunt_arrow's ghost mesh). Everything else they use is built (GroundHugEmitter,
   TrailRendererModern, LineRenderer, RabbitTracer, Shuriken, `Particles/Standard Unlit`, add / addsoft / alpha). No
   ParticleSystem in them uses Trail, Sub, Collision, Lights or Noise modules.
9. **Game quirks (offer to the user for the Bible; none changes a cue).**
   - Camp Fire's prefab is cached on the first cast: `if (!BEXYZgTcQN) BEXYZgTcQN = Load("campFire" + sLv)`
     (`Chameleon.cs:9424-9430`), so after learning Camp Fire 2 the old `campFire1` keeps spawning until the hero object
     is rebuilt (a relog / map change).
   - With the Snooker weapon (`w_chm25`) the Combo shot is the ball (`mWep1`, the "bow" hand) while every shot
     coroutine hides `mWep2`, the cue (`Chameleon_nAttack.cs:114-128`; item 5).
   - Clear Arrow never carries Fatal Strike's blood trail: the clear branch (`Chameleon_nAttack.cs:272-318`) skips the
     `fatalStrike` attach the normal branch does (`:199-260`), though `RPC_clearArrow_fire` passes the Fatal Strike level
     and spends its charge (`Chameleon.cs:9036-9060`).
   - TTO dropped Torment Rain's ground stick: TTO's `tormentRain_fire` is Shuriken with its CollisionModule off
     (`tto_bbcopies.json`), so on TTO the arrows fall through the ground; on BB a WorldParticleCollider with bounce 0
     stops each arrow where it lands, standing in the ground until its 2-3 s are up.
   - Needle Prison's 16 needles are not laid round in order: needle i at `rotateH(r forward, 67.5 i)` (`:187`), so they
     fall at 0, 67.5, 135, 202.5 ... degrees, three turns that fill the 16 points 22.5 degrees apart (`calc.txt`).

## The Chameleon's blocked set

"Where" is where BB spawns it; the times and the skill tiles are the skills researchers' (`attacks_emotes.md`,
`skills_*.md`, `tto.md`), so treat the cue shapes here as the parts' contract.

| effect | skill (spawn) | missing part(s) | where |
|---|---|---|---|
| `nAttack` (x1 per shot) | Combo `RPC_nAttack_fire` (`:8447`, Instantiate `:8473` LookRotation(fireDir), life `:8482`, Init `:8497`); also Left / Right Stride and Double Strider's clone (`:26971`, `:27032`) | Chameleon_nAttack + Interfaces 1 | `firePos = hero + (0, 1.5, 0) + forward` (`:15586`), aimed at the target (`:15591`) |
| `clearArrow` | Combo while `invisible` with Clear Arrow #263 (`RPC_clearArrow_fire` `:8983`, Instantiate `:9009`, Init `:9041`) | Chameleon_nAttack (clear branch) + FX/Invisible in mesh.js | as `nAttack` |
| `fatalStrike` (on an arrow) | `Chameleon_nAttack.cs:199-247` while the `fatalStrike` status holds | none of its own (api.spawn, followNode) | the arrow model, 0.1 m behind its tip |
| `needlePrison` (+ 16 `needlePrison_arrow`) | Needle Prison: status on the hit target (`:21750`), look `CharacterControl.cs:36629-36650` | Chameleon_needlePrison layout + part; AdditiveAlpha in mesh.js | the target's feet (10 m point), identity, parented to it |
| `campFire1` / `campFire2` (max rank: 2) | Camp Fire `RPC_campFire_create` (`:9417-9452`, Instantiate `Euler(270, 90, 0)`, `Init(owner, chaAdjust(30))`) | Chameleon_campFire layout (draws nothing) | `mPos` (the cast's spot) |
| `tormentRain_fire` | Torment Rain `RPC_tormentRain_fire` (`:9258`, `:25872-25996`), at the Final Entrapment cage's centre | WorldParticleCollider | the cage (the 10 m point) |
| `thunderDragon_ring2` | Thunder Dragon (`:37992`) | the Shuriken graft; Self-Illumin/DoubleTexture | thunderDragon's spawn |
| `zeroShot_ring` | Zero Shot (`createEffect` `:37647`, hero position and rotation) | the Shuriken graft | hero |
| hero look `FX/Blend` | `blend`: Charge Attack (`:16358`, `blend 4` while charging), Perfect Blend (`:20687`) | HERO_SKINS "FX/Blend" | the hero |
| hero look `FX/Invisible` (+ `invisible` effect) | `invisible`: True Invisibility (`:21155`), Mass Invisibility (`:24575`) | HERO_SKINS "FX/Invisible" | the hero; the look 0.2 s after the status (`CharacterControl.cs:42212`) |
| `castRing` | every cast1 (`:18544`, root loop restarted at 0.5 s `:17939-17944`) | `fx:castRing` hook for the Chameleon (bat.js) | hero, `Euler(270, 90, 0)` |
| `finalEntrapment` | Final Entrapment (`:9142-9167`: `effectControl.life = mDuration`) | cue `life` (Interfaces 4) | hitPos (the 10 m point) |
| TTO: chainLightning_*, venomPhantom_echo | Chain Lightning, Venom Phantom (`pseudo/Chameleon.c:35707`, `:38893` `ChameleonLightning::Set`) | ChameleonLightning | tto.md's |
| TTO: venomPhantom_ghost | Venom Phantom (`pseudo/Chameleon.c:364` Bake, `:423` SlideTo 0.18 s, `:12802` Fire, `:36425` Shatter) | ChameleonAfterimage + TTO/ChameleonSpirit | tto.md's |
| TTO: apexHunt_arrow | Apex Hunt | TTO/ChameleonSpirit (its `ghost` mesh) | tto.md's |
| TTO: preyFx | Apex Hunt's prey marks (`pseudo/Chameleon.c:36548-36631` `mApexMarks`, `:37236` Release) | ChameleonPreyReticle | the prey (10 m point) |

## LAYOUTS (paste into `pipeline/wardrobe_fx.py`, after the Bat's block)

```python
# the Chameleon's parts (plans/fx_chameleon/parts.md, 2026-11-13; checks/fx_chameleon_research/parts/probe.txt: each
# instance's bytes are the listed fields exactly; Chameleon_nAttack keeps every field private, 0 bytes)
LAYOUTS.update({
    "Chameleon_campFire": [("mLv", "i")],              # Chameleon_campFire.cs:219 (4 bytes: campFire1 1, campFire2 2)
    "Chameleon_needlePrison": [("mPrisonArrow", "r")], # Chameleon_needlePrison.cs:47 (8 bytes: -> needlePrison_arrow)
    "Chameleon_nAttack": [],
})
```

Values (`probe.txt`): campFire1 `mLv` 1, campFire2 `mLv` 2 (read by its heal only, `Chameleon_campFire.cs:106`);
needlePrison `mPrisonArrow` [25, 274] = the GameObject `needlePrison_arrow` in sharedassets6 (`ref_probe.txt`).

Four more extractor lines (lead, `wardrobe_fx.py`):
- `WorldParticleCollider` stored as Light / TrailRenderer are (the Cat's line, `plans/fx_cat/parts.md` "LAYOUTS"):
  tormentRain_fire's `m_BounceFactor` 0, `m_CollisionEnergyLoss` 0, `m_CollidesWith` {m_Bits 1}, `m_MinKillVelocity` 0.
- `material()`: `shader:Transparent/AdditiveAlpha` saves `"cut"` = `_AdditiveRange` (the Cat's line): `needleprison`
  0.5189 (`mesh_probe.txt`), `_Color` 0.799.
- `SHURIKEN_FROM_TTO["chameleon"] = ["thunderDragon_ring2", "zeroShot_ring"]` with the matching rule of part 7.
- `wardrobe_fx_tto.py` `material()`: also save `_ScaleTex` as `"scaleTex"` (exported like `_MainTex`) for TTO's own
  shaders: `chmRow6_phantomSpirit` / `chmRow6_goldSpirit` -> `chmRow6_scalesTile` (`tto_mat_probe.txt`), part T2.

## Each part

Page parts plug in as the comment above `FX_PART_FILES` says (`wardrobe/index.html`; its line numbers here are as read on 2026-11-13 while the Bison build was editing the file): `wardrobe/fxparts/<file>.js`
default-exports `register(api)` and calls `api.part(type, build)`; `build(fx, node, comp, mat, nodeDef, data)` returns
`{ node, update(dt, cam) ("destroy" removes the node), stop?(), dispose?() }` or null; `"fx:<effect>"` = the hero's code
acting on that effect; `api.spawn(name, at, opts)` makes an effect a script instantiates (`opts.followNode` +
`opts.local` = a parent); `fx.cutAt` is the cue's `cut` in clip time against `api.FX.t`; `fx.at.to` is the cue's
target point. Space: every root hangs in the effect's mirror group (Unity's world, the hero's feet at the origin, +z her
facing, y 0 the floor). The standard target body (Bat decisions 3-4): centre (0, 0.6, 10), CharacterController h 1,
r 0.3 (AABB x +-0.3, y 0.1..1.1, z 9.7..10.3).

### 1. Chameleon_nAttack: `nAttack`, `clearArrow` (`fxparts/chameleon.js`, new; Interfaces 1)

**What it does in BB (`Chameleon_nAttack.cs`).** All fields private (0 bytes).
- Awake (:21-38): layer 1 (:28), `ProjectileControl` cached (:31), `rigidbody.velocity = TransformDirection(0, 0, 30)`
  (:34): **30 m/s** along its spawn rotation (`LookRotation(fireDir)`, `Chameleon.cs:8473`).
- FixedUpdate (:46-66): clock `+= dt` (:53); Destroy once it reaches `ProjectileControl.life` (:56-62) =
  `(0.4 + 0.1 x Far Reach) x rangeMod` (`Chameleon.cs:8482`, `:9018`) = **0.8 s** at Far Reach 4, rangeMod 1
  (`CharacterControl.cs:154`).
- `Init(owner, nFatalStrikeLv, nClearLv)` (:74-325):
  - Bow Mastery #401: velocity **40 m/s** (:94-100) (passives on: 40);
  - `nClearLv == 0` (`nAttack`, :106): the weapon copy: `Instantiate(w_chm25 ? mWep1 : mWep2)` (:114-128), parent
    the projectile, `localPosition 0`, `localRotation = Euler(0, 270, 270)` (:140-150; that turns the model's +y onto
    the flight's +z: every Chameleon arrow model lies along +y, `props_weapons.json`), every renderer enabled (:155-182);
    then with `nFatalStrikeLv > 0` (:199) `fatalStrike` (:205) parented to the copy at `(0, mesh.bounds.max.y - 0.1, 0)`
    of the copy root's MeshFilter mesh (:215-233), or (0, 0.8, 0) when the root has none (:241), scale 1 (:247);
  - `nClearLv != 0` (`clearArrow`, :272-318): the child `arrow` (:274): for her own team (:283) its MeshFilter's mesh
    = `mWep2`'s root MeshFilter `sharedMesh` (:287-305) when both exist; for another team the child is destroyed
    (:318): enemies see no arrow.
- OnTriggerEnter (:336-850): a foe's collider destroys it (:397) and asks for `RPC_nAttack_hit` at
  `ClosestPointOnBounds(the arrow collider's centre)` (:406-445), Critical Plus' roll (:620-680), poison (:713-783):
  logic and hit cues (the attacks researcher's).
- Physics (`probe.txt`): Rigidbody mass 1, no gravity, rotation frozen; trigger BoxCollider size (0.3, 0.3, 1.5),
  centre (0, 0, 1): it spans local z 0.25 .. 1.75, so it reaches a target 1.75 m before the arrow root does.

**The flight on the page (`calc.txt`).** From `firePos = (0, 1.5, 1)` aimed at the body's centre (0, 0.6, 10), 50 fixed
steps a second: the trigger first overlaps the body in the step at **0.18 s** after the spawn (0.24 s at 30 m/s), root
at (0, 0.78, 8.16); the hit flash's `ClosestPointOnBounds` = **(0, 0.68, 9.7)**. Without a `to` it flies the 0.8 s
(32 m) and goes.

**The page part (chameleon.js, about 60 lines).**
- Model: `api.propModel(fx.at.slot || (api.worn("R") === "snookerBall" ? "R" : "L"))` (Interfaces 1) for `nAttack`;
  added under the effect's root at local 0, quaternion = Unity Euler (0, 270, 270) (the page's "YXZ" conversion, as a
  cue's `rot`); no worn piece: the fallback model (question 1).
- `clearArrow`: the node `arrow` keeps its own mesh unless the worn arrow's prefab root has one
  (`propModel(...).userData.rootMesh`): then that geometry replaces the arrow node's, with the arrow node's own
  FX/Invisible material (part 3) and its own rotation (0.5, -0.5, -0.5, 0.5) (`mesh_probe.txt`, the same +y -> +z turn).
- Each frame: `root += v dt`, v = 40 (`fx.at.speed` overrides; question 6) x the spawn forward (`fx.uQuat(root)`); end
  (`"destroy"`) at 0.8 s, or in the first 0.02 s step whose box overlaps the target body when the cue has `to` (the
  attacks cue puts `nAttack_hit` there: see the fragment). APPROX: the box against the capsule by points along its
  centre line within 0.45 m (0.3 + half the box) of the capsule's axis, as `calc.py`.
- `fx.at.fatal` (the status holds; question 5): `api.spawn("fatalStrike", {}, { followNode: root, local: { pos: [0, 0,
  maxY - 0.1] } })`, maxY from `userData.rootMesh` (0.8 without), never on `clearArrow`; the entry's `"builds":
  ["fatalStrike"]`.
- The hand arrow vanishing while the shot is out is a separate cue (Interfaces 2), not this part.

### 2. Chameleon_needlePrison: `needlePrison` (+ `needlePrison_arrow`) (`fxparts/chameleon.js`)

**What it does in BB.**
- The look (`CharacterControl.cs:36622-36650`, status `needlePrison` on the hit target, `Chameleon.cs:21750`):
  `PositionEvent()`, Instantiate `needlePrison` at the target's position, `Quaternion.identity` (:36629), named
  `needlePrisonFx`, parented to the target, scale 1 (:36632-36638), and starts `Init(Clamp(2 x mChar.radius, 0.5, 2))`
  (:36650): `mChar` is the target's CharacterController, so r = 2 x 0.3 = **0.6 m** on the standard body. Destroyed by
  name when the status ends (`:16558-16570`); duration `getDebuff(1 + sLv, cha, target cha) + 2` with Mass House Lock
  (`Chameleon.cs:21745`, the skills researcher's `kill`, cut at 10).
- `Init(nRadius)` (`Chameleon_needlePrison.cs:23-25`, the state machine :144-213, its predicates worked through): i = 0
  (:205); while i < 16 (:172): `pos = transform.position + rotateH(r x forward, 67.5 i)` (:187; `Math.cs:840-841`:
  x = -r sin a, z = r cos a), `Instantiate(mPrisonArrow, pos, LookRotation(Vector3.up))` (:192), parent the prison
  (:197), `Yield(0.05)` (:211), i++ (:158). So **16 needles, one every 0.05 s from 0 to 0.75 s**, on a 0.6 m ring
  (positions in `calc.txt`), each pointing up (LookRotation(up) = Euler(-90, 0, 0)).
- `needlePrison_arrow` (no EffectControl): Animation `root` 0.5 s, plays itself, wrap 0 = Once (`mesh_probe.txt`): the
  needle falls from 9 m in its own +z (= up) to 0 by 0.27 s, then shakes (`clip_probe.txt`); its SkinnedMeshRenderer is
  `needleprison` (AdditiveAlpha, part 4); an ImageEmitter of `needlePoison_dust` (multiply, built) puffs at 0.3 s. The
  prison's own AudioSource plays `needlePrison` once.

**The page part (chameleon.js, about 20 lines).** On the `needlePrison` root: own clock; at 0.05 i (i = 0..15)
`api.spawn("needlePrison_arrow", {}, { followNode: fx.root, local: { pos: [-0.6 sin(67.5 i), 0, 0.6 cos(67.5 i)], rot:
[-90, 0, 0] } })` (Unity space: rotateH's sign as written; r from `fx.at.r`, default 0.6); they go with the prison
(followNode). The entry's `"builds": ["needlePrison_arrow"]`. Cue: `{"d": 10, "kill": <duration, cut 10>}`.

### 3. FX/Invisible on an effect mesh: `clearArrow` (`fxparts/mesh.js`; the shell shared with Interfaces 3)

**The shader (compiled, `shaders.txt` "FX/Invisible"; the rip's stub has none of it).** Queue Transparent, two passes:
- pass 1: `Blend SrcAlpha OneMinusSrcAlpha`, `ColorMask RGB`, ZWrite on, Cull Back, `SetTexture [_MainTex] {
  ConstantColor (1,1,1,0.35) combine texture, constant alpha }`: the texture unlit at **35 %**;
- pass 2: `Cull Front`, `Blend SrcAlpha SrcColor`, ColorMask RGB, ZWrite on: a shell whose vertex program pushes each
  vertex along its view-space normal in clip space, `xy += (n.x P[0][0], n.y P[1][1]) x clip z x 0.003`, coloured
  constant **(0.3, 0.6, 1, 0.75)**: drawn after pass 1, so only the rim outside the silhouette shows: a blue outline.
  Fallback "Transparent/Diffuse".
- `clearArrow.mat`: no texture (`white`), `_Color` white; its `_TintColor` (0, 1, 0.35, 0.14) and `_Emission` are
  leftovers the shader never reads (`mesh_probe.txt`). The only FX/Invisible material in the rip.

**The page.** mesh.js `material()`: `"shader:FX/Invisible"` -> a list (as AdditiveSaturate's): pass 1
`MeshBasicMaterial({ map (or none: white), transparent, opacity 0.35, depthWrite true, FrontSide })`, pass 2 the
shared shell material (Interfaces 3: colour (0.3, 0.6, 1), alpha 0.75, k 0.003, blend SrcAlpha / SrcColor,
BackSide), drawn after pass 1 (renderOrder +1 or the group order). APPROXIMATED: the canvas alpha of a SrcColor
blend (Interfaces 3).

### 4. Transparent/AdditiveAlpha on an effect mesh: `needlePrison_arrow` (`fxparts/mesh.js`; the Cat's spec)

The Cat's part 3 material (`plans/fx_cat/parts.md` "Its material"), unchanged: pass 1 lit, `color = 2 x _Color`,
`alphaTest = cut`, FrontSide; pass 2 the texels under the cut added as light (`glowTwin`'s, `index.html:915-935`).
Here on a SkinnedMeshRenderer (withMaterials takes the list for an SMR too): `cut` 0.519, `_Color` 0.799. Whoever
builds it first builds it once (Cat `supportFire_fire`, Chameleon `needlePrison_arrow`, Mole `napalm` / `nAttack`).

### 5. Self-Illumin/DoubleTexture: `thunderDragon_ring2`'s skeleton (`fxparts/mesh.js`)

**The shader (`shaders.txt`; the rip's `DoubleTexture.shader:1-11` is the same).** One pass, no blend, no lighting,
ZWrite on, Cull Back: `SetTexture [_MainTex] { combine texture * texture }`: **colour = texture squared**, opaque
(`_Color` 0.784 unused). Fallback "Diffuse". Used by `thunderDragon_skeletons` (a 2,645-vertex dragon skeleton, node
`thunderDragon_skeleton_tri`, turned 180 degrees) and the Rabbit's `rabbit_stickygum` (the rip's `.mat` files by the
shader's GUID).

**The page.** `"shader:Self-Illumin/DoubleTexture"` -> `MeshBasicMaterial({ map })` with `onBeforeCompile` after
`map_fragment`: `diffuseColor.rgb *= sampledDiffuseColor.rgb; diffuseColor.a = 1.0;` (opaque). Squaring the decoded
(linear) texel equals squaring the gamma value (a pure power commutes with the square), so no colour-space fix.

### 6. WorldParticleCollider: `tormentRain_fire` (`fxparts/worldcollider.js`; the Cat's part 5, generic)

The Cat's spec (`plans/fx_cat/parts.md` part 5: the `collide` hook in `legacyParticles`, the floor y 0 as the only
collider) covers it with these values (`ps_sum.txt`): bounce **0**, energy loss 0, layer mask 1, min kill 0. So each
arrow that reaches y 0 gets velocity 0 and is **not** killed (|v| < 0 is false): it stands there for the rest of its
energy. The arrows: node `ParticleEmitter` at (0, 16, 0), local space (`Simulate in Worldspace?` false), one shot of
64-256, ellipsoid (5, 12, 5) (a radius: `index.html:4370`), local velocity (0, -48, 0), energy 2-3 s, size 2-3, vertical
billboards (`m_StretchParticles` 5, built: `index.html:4344`), `rainOfArrow` alpha: they land 0.08-0.58 s after the
spawn (`calc.txt`) and stand 1.4-2.9 s. The dust (`DustEmitter`, world space, its EmitterControl delay 0.1 / life 0.5)
is built. The local-space test goes through `fx.uMatrix(node)` (the Cat's spec). APPROX: the page has no ground mesh
(`index.html:649`: a shadow disc), so the lower half of each standing 2-3 m arrow shows below the floor line, where the
game's ground hides it (question 2).

### 7. Unity 3.5's ParticleSystem: `thunderDragon_ring2`, `zeroShot_ring` (`wardrobe_fx.py` graft, lead; shuriken.js unchanged)

**The systems (`ps_sum.txt`, `ps_mats.txt`; TTO's copies the same, `tto_bbcopies.json`).**
| effect / node (BB index) | what | material |
|---|---|---|
| thunderDragon_ring2 `ParticleSystem` (3), at (0, 1.2, 0) | loop 5 s, local, box 3 x 2 x 3, rate 48, life 0.1-0.3, size 0.5-1.5, speed 0 | `spark3` addsoft |
| thunderDragon_ring2 `ParticleSystem` (4), at (-0.1, 1.05, -0.2) | loop 5 s, **prewarm**, local, box 0.7 x 2.1 x 0.7, rate 64, life 0.5-1, size 0.6-0.9, speed 0-0.3 | `thunderDragon_particle` addsoft |
| zeroShot_ring `Particle System` (4), (0, 1.3, 1.5) | one shot 1 s, start delay 1, world, hemisphere shell r 0.2, burst 12, life 0.3-0.5, speed 0-2, size 1-4, size over life, rotation over life -45 deg/s, force | `zeroShot1` multiply2 |
| zeroShot_ring `Particle System` (5), (0, 1.3, 1.5) | the same shape, delay 1, burst 48, life 0.4-0.6, speed 1-3, size 1-2, rotation +45 deg/s | `zeroShot2` multiply2 |
| zeroShot_ring `Particle System` (6), (0, 1.3, 1.0) | one shot, world, sphere shell r 3, burst 24 at 0.2 s, speed -12..-9 (inward), size 0.1-0.2, clamp velocity, **stretched** x 6 | `zeroShot3` addsoft |

**The graft (the Bison's part 5 / the Cat's part 6), with a matching rule for repeated names.** After `effect()` builds
BB's version, read TTO's copy (`tto/<name>`), and for each BB node carrying a ParticleSystem (BB's walk must note it:
`elif ty == "ParticleSystemRenderer": node["mats"] = [material(...) for m in m_Materials]; node["ps"] = True`, which
also gives the node BB's own materials), take the TTO node with the **same name whose ParticleSystemRenderer's first
material is `"tto_" + node["mats"][0]`**; on a tie, the next unused one in TTO's order. Append that node's
`ParticleSystem` and `ParticleSystemRenderer` dicts to the BB node's comps; keep BB's `mats` (`spark3`,
`thunderDragon_particle`, `zeroShot1/2/3`: their textures come through `material()`). By name alone the two
`Particle System` nodes at (0, 1.3, 1.5) would swap materials, and thunderDragon's two `ParticleSystem` nodes would get
each other's shapes. No other renderer on these nodes, so mats[0] is the system's own (the Bison's shuriken.js change is
not needed for them). The native 3.5 converter (the Cat's question 5) would cover them too; until then the inventory
keeps them "needing" ParticleSystem.

### 8. The `fx:castRing` hook for the Chameleon (`fxparts/bat.js`, one line)

`RPC_cast1` creates `castRing` at 0 (`Chameleon.cs:18544`, `Euler(270, 90, 0)`), waits 0.4 s (case 2, `:17882-17906`:
`cast2` looped), waits 0.1 s (`:18592`), then `mCastRing.animation.Play("root")`, `wrapMode = Loop`
(`:17939-17944`): the Bat's 0.5 s restart exactly. `bat.js:441` `if (fx.cls !== "bat") return null;` ->
`if (fx.cls !== "bat" && fx.cls !== "chameleon") return null;` (and its comment). The prefab is the Chameleon's own
(`castring`: create 0.4667 s, root 2 s loop, `probe.txt`), as the Bat's has.

### 9. Chameleon_campFire: `campFire1`, `campFire2` (layout only, no page code)

`Chameleon_campFire.cs`: `Init(owner, nTimer)` (:23-40): owner, `ivqbdRG8uR = (int)(Time.time + nTimer)` (:36),
active. Update (:52-150): Destroy when the owner is gone (:71) or the time is up (:82); else every 4 s (:97) heals allies
in the `emotion` state within 9 m by `0.01 + 0.02 mLv` of their HP / MP / KO (:106-140): logic only. Draws nothing; no
EffectControl. `nTimer = chaAdjust(30)` = 30 s (`Chameleon.cs:29360`, the Bible's Duration line): the cue's `kill` 10
(fields cut at 10 s). campFire2 (max rank): root scale 1 (campFire1 0.8), the `Camp_Fire` mesh (opaque), a `Flame3`
legacy emitter, the `campFire` loop (until the kill). Add `"Chameleon_campFire"` to `BUILT` ("draws nothing").

### 10. The hero looks FX/Blend and FX/Invisible (`index.html` HERO_SKINS, lead; Interfaces 3)

**What BB does (`CharacterControl.cs`).**
- `blend` (`:36665-36940`): `removeStatus("invisible")`; renderers = the character's (`:36672`); for another team
  (`:36676-36800`, FX/Camaflage `:36770`) or off; for her own team / no player (`:36850-36935`): every material whose shader is
  `Diffuse` -> `new Material(FX/Blend)` with its `mainTexture` (`:36874-36890`, `:36880`), every other renderer `enabled = false`
  (`:36900`). At once (no wait). Back to Diffuse at the status's end (`:16307-16450`).
- `invisible` (`:36942-36955`, `:32494-32690`): `removeStatus("blend")`; Instantiate `Effects/invisible` at her
  position, identity, `InitEffectControl(her)` (`:36949-36955`; EffectControl life 2, followPosition), then
  `Yield(0.2)` (`:42212`) and in case 2 (`:32494`): for her own team (`:32498-32509` -> `IL_B965`, `:32630-32690`, FX/Invisible `:32649`) every
  Diffuse material -> FX/Invisible with its mainTexture, others off. Back at the end (`:16458-...`).
- The shaders (`shaders.txt`), both: pass 1 = the texture unlit at alpha 0.35 (ZWrite on, Cull Back, ColorMask RGB);
  pass 2 = the shell, Cull Front, `Blend SrcAlpha SrcColor`, ColorMask RGB, ZWrite on, pushed out by `k x clip z`
  along the view normal (CosmicRift's vertex program, `index.html:4444-4475`, with its own k), drawn **after** pass 1:
  | look | shell colour (constant) | k |
  |---|---|---|
  | FX/Blend | (0.8, 0.8, 0.3, 0.5): a yellow-green rim | 0.002 |
  | FX/Invisible | (0.3, 0.6, 1, 0.75): a blue rim | 0.003 |
  (FX/CosmicRift, for contrast: shell first, 0.008, One / OneMinusSrcAlpha.)

**The page.** Two HERO_SKINS entries beside `"FX/CosmicRift"`: the same `ghost` (MeshBasic, map, opacity 0.35;
Cull Back here, not CosmicRift's DoubleSide), the shell from the shared helper (Interfaces 3) with the table's colour and
k, and a flag that the ghost draws first (HeroSkin's copies `[shell, ghost]` today: order by renderOrder). Cues:
`[t, "skin", "FX/Blend", {"kill": k}]` at the `blend` status; `[t + 0.2, "skin", "FX/Invisible", {"kill": k}]` plus
`[t, "fx", "invisible"]` at the `invisible` status (durations: skills researchers; Perfect Blend `chaAdjust(2 x 2 + 4)`
= 8 s with Erase Senses, True Invisibility 16 s and Mass Invisibility 12 s cut at 10; `blend` also ends at her next
action, `Chameleon.cs:166-201`). APPROXIMATED as CosmicRift's: every page mesh taken as Diffuse.

## TTO parts (the released skills: Apex Hunt, Chain Lightning, Venom Phantom)

All three in `fxparts/tto_chameleon.js` (new). Field values are the prefabs' (`tto_summary.txt`); the methods are
TTO1102's, disassembled (`disasm_*.txt`; addresses are RVAs from `dump.cs:105570-105700`).

### T1. ChameleonLightning (TTO.Game TypeDefIndex 3477): 7 prefabs

**Fields** (`dump.cs` ChameleonLightning; `.ctor`@0x1C4E8E0 defaults): `aura` (bool), `segments` (9), `jag` (0.18),
`maxJag` (0.45), `flicker` (0.05), `life` (0.25), `radius` (0.55), `height` (1.1), `gap` (0.12), `autoBolt`, `localFrom`,
`localTo`, `delay`; private `line`, `a`, `b`, `born`, `nextJag`, `nextArc`, `wakeAt`, `c0`, `c1`, `set`, `waiting`.

**Methods.**
- Awake@0x1C4DBF0: `line = GetComponent<LineRenderer>()`; `SetVertexCount(segments + 1)`; `c0 = startColor`, `c1 =
  endColor`; `born = time`; if `aura`: `useWorldSpace = false`, `NewArc()`.
- Start@0x1C4E550: if `autoBolt && !set`: with `delay > 0`: `waiting = true`, `wakeAt = time + delay`, line disabled;
  else `Set(TransformPoint(localFrom), TransformPoint(localTo))`.
- Set(from, to)@0x1C4E3C0 (called by the hero's code for the non-auto bolts: `pseudo/Chameleon.c:35707` venomPhantom_echo,
  `:38893` chainLightning_bolt / _boltHot): `useWorldSpace = true`; `a = from`, `b = to`; `set = true`; `born = time`;
  `Jag()`.
- Update@0x1C4E690: `waiting` and `time >= wakeAt` -> enable, `Set(TransformPoint(localFrom), TransformPoint(localTo))`.
  Aura: `time >= nextArc` -> `NewArc()`, else `time >= nextJag` -> `Jag()`; `Fade(clamp01(1 - (time - born) / life))`.
  Bolt: nothing until `set`; `age = time - born`; `age >= life` -> Destroy(gameObject); else `time >= nextJag` -> `Jag()`;
  `Fade(1 - age / life)`.
- NewArc@0x1C4E250 (the aura's crackle, local space): `born = time`; `nextArc = time + gap + Random(0, gap)`;
  `th1 = Random(0, 2 pi)`; `th2 = th1 + Random(0.8, 2.2) x (Random.value < 0.5 ? -1 : 1)`; `a = (r cos th1,
  Random(0.05, height), r sin th1)`, `b = (r cos th2, Random(0.05, height), r sin th2)`; `Jag()`.
- Jag@0x1C4DD90: `nextJag = time + flicker`; `d = b - a`; `side = normalize(cross(d, up))` (`cross(d, right)` when
  |.|^2 < 0.0001); `n2 = cross(normalize(d), side)`; `amp = min(|d| x jag, maxJag)`; for i = 0..segments: `t = i /
  segments`, `p = a + d t`, inner points `+= (side x Random(-1, 1) + n2 x Random(-1, 1)) x sin(pi t) x amp`;
  `SetPosition(i, p)`.
- Fade(k)@0x1C4DCE0: `startColor = (c0.rgb, c0.a k)`, `endColor = (c1.rgb, c1.a k)`.

**The page.** On a node with tto_sheep.js's LineRenderer part: find it (`fx.emitters.find(x => x.node === node &&
x.line)`), set `driven = true`, keep its colour curve x k (as RabbitTracer, `tto_sheep.js:262-298`); write `pts`
(world for a bolt, the node's space for an aura: `world = !aura`) each Jag; `draw(cam)` every frame. A non-auto bolt's
`from` / `to` come from the cue (`fx.at.from` default the node, `fx.at.to` the target's chest); without `to` it draws
nothing, as RabbitTracer. chainLightning_overload's nine auto bolts (sky to ground, 7 ground arcs) need nothing from the
cue.

### T2. ChameleonAfterimage (3476) + the shader TTO/ChameleonSpirit: `venomPhantom_ghost`

**Fields** (`.ctor`@0x1C4DA50): `spirit` (Material), `fireFx`, `shatterFx` (GameObjects: `venomPhantom_ghostFire`,
`venomPhantom_ghostShatter`, written by name, `tto_probe.err`), `fadeIn` (0.12), `shatterTime` (0.35), `life` (4),
`rim`, `flare` (Colors); private `baked`, `parts`, `block`, `born`, `endAt` / `firedAt` / `slideAt` (-1), `slideTime`,
`slideFrom/To`, `turnFrom/To`, `bowLocal`. Prefab: fadeIn 0.12, shatterTime 0.35, life 4, rim (0.5, 1, 0.3, 0.7),
flare (0.9, 1, 0.7, 1), spirit `chmRow6_phantomSpirit`.

**Methods.**
- Bake(body, bowPoint)@0x1C4C190 (`pseudo/Chameleon.c:364`): `bowLocal = InverseTransformPoint(bowPoint)`; for each
  enabled, active renderer of `body` not `Skip`ped (@0x1C4CFA0: by name suffixes / a substring, string literals not
  resolved): a SkinnedMeshRenderer's `BakeMesh` (its pose **frozen**) or a MeshFilter's sharedMesh, in a new child
  GameObject at the renderer's world position / rotation and lossy-scale ratio, every submesh drawn with `spirit`, no
  shadows; then `Apply(0, rim)`.
- SlideTo(pos, rot, time)@0x1C4D2E0 (`:423`, 0.18 s): from the current pose, `slideTime = max(0.01, time)`, `slideAt =
  now`.
- Update@0x1C4D3C0: `age = now - born`; `age > life` and not ending -> Shatter. Slide: `u = clamp01((now - slideAt) /
  slideTime)`, `e = 1 - (1 - u)^2`, position lerp / rotation slerp by e, done at u = 1. Fade = `clamp01(age / fadeIn) x
  (0.85 + 0.15 sin(7 age))`; ending: `k = clamp01((endAt - now) / shatterTime)`, fade x k, scale `1 + 0.08 (1 - k)`,
  Destroy at `now >= endAt`. Colour: `rim`, after Fire `lerp(flare, rim, clamp01((now - firedAt) / 0.3))`.
  `Apply(fade, colour)`.
- Fire@0x1C4CA80 (`:12802`): `firedAt = now`; `fireFx` at `TransformPoint(bowLocal)`, its rotation.
- Shatter@0x1C4CD90 (`:36425`): `endAt = now + shatterTime`; `shatterFx` at its position, its rotation (scale x 0.9).
- Apply(fade, c)@0x1C4BEF0: a MaterialPropertyBlock on every part: one float (`_Fade`) and one colour (`_RimColor`):
  the two names are the IL2CPP literals at 0x37FDD60 / 0x3801228, inferred from the shader's properties (medium).

**TTO/ChameleonSpirit (`dxbc_ChameleonSpirit.txt`).** Queue Transparent+1. Pass 0: ZWrite on, ColorMask 0 (a depth
prepass: only the front-most surface of the body draws). Pass 1: `Blend One OneMinusSrcAlpha` (premultiplied), ZWrite
off, ZTest LEqual, Cull Back. Fragment (world position P, normal N, view V):
- wisp: `q = P x _WispScale + (0, -_WispSpeed x time, 0)`; `n = 0.65 noise(q) + 0.35 noise(2.3 q + 7.1)` (a 3D value
  noise, hash `fract(p x 0.3183099 + 0.1) x 17`, `fract(x y z (x + y + z))`, smoothstep weights); `w = smoothstep(0.25,
  0.85, n)`; `wisp = 1 + _Wisp (w - 1)`;
- rim: `f = 1 - saturate(N.V)`; `pr = f^_RimPower`; `s = smoothstep(_RimEdge, 1, f)`;
- scales: `_ScaleTex`'s alpha, triplanar on `P x _ScaleSize` scrolled by `-_ScaleSpeed x time`, weighted by |N|;
- alpha = `_Fade x saturate(0.35 s + _CoreColor.a (0.55 + 0.45 wisp) + 0.25 pr)`;
- rgb = `_CoreColor.rgb x alpha + _Fade x min(_RimColor.rgb _RimColor.a (pr _InnerGlow wisp + s) + scales x
  _ScaleColor.rgb _ScaleColor.a (1 - s), _MaxGlow)`.
Values: phantomSpirit (core (0.05, 0.2, 0.05, 0.28), rim (0.5, 1, 0.3, 0.6), RimPower 3.4, RimEdge 0.62, InnerGlow 0.35,
scales (0.35, 0.9, 0.2, 0.06), ScaleSize 1.8, ScaleSpeed 0.4, Wisp 0.5, WispScale 2.2, WispSpeed 0.6, MaxGlow 0.9, Fade
1); goldSpirit (apexHunt_arrow's `ghost`): core (0.3, 0.2, 0.05, 0.4), rim (1, 0.85, 0.4, 1), RimPower 2.2, RimEdge 0.45,
InnerGlow 0.25, scales (1, 0.8, 0.3, 0.2), ScaleSize 1.5 (`tto_probe.json` materials).

**The page.**
- `api.shader("shader:TTO/ChameleonSpirit", make)`: a ShaderMaterial (or MeshBasic + onBeforeCompile) with the
  fragment above, `premultipliedAlpha`, One / OneMinusSrcAlpha, depthWrite false, plus a depth-only twin drawn first
  (colorWrite false, depthWrite true) for pass 0; `scaleTex` from the data (extractor line, LAYOUTS section); `_Fade`
  and `_RimColor` as uniforms a part can set.
- Part `ChameleonAfterimage`: bake = a frozen copy of the hero's meshes in the current pose (each SkinnedMesh's
  vertices through `boneTransform` once, or a clone bound to a detached copy of the skeleton), every material the
  spirit (one clone per afterimage for its uniforms); the timeline from cue options the tto researcher fills
  (`{"slide": [[t, x, y, d, yaw, 0.18]], "fire": [t], "shatter": t}`, `fire` / `shatter` spawning
  `tto/venomPhantom_ghostFire` / `tto/venomPhantom_ghostShatter` through `api.spawn`, the entry's `"builds"`); life 4 s
  without a shatter cue. APPROX: Skip()'s name rules (unresolved literals): take every mesh of the dressed hero.

### T3. ChameleonPreyReticle (3478): `preyFx`

**Fields** (`tto_prey.json`): `ring`, `crosshair` (Transforms: its two meshes `tto_chmRow6_reticle_add`,
`tto_chmRow6_cross_add`, both `add`), `tinted` [both renderers], `notches` [], `lockIn` 0.35, `fadeOut` 0.25, `spin` 40,
`preview`, `previewStacks`, `lockOnly`, colours `gold` / `dim` / `bug` / `tail` / `elem` / `mach` (by the prey's race).
**What it does** (Start@0x1C4EA70, Update@0x1C4EF10, Paint@0x1C4E920; read from the call and constant list, medium):
Start reads the prey's feet / head from its renderers' and collider's bounds (head + 2 above the collider's top is a
clamp), keeps the two scales, paints the tint; Update: gone `fadeOut` s after the prey loses its status (alpha
`1 - (t - 0.1) / fadeOut`, then Destroy); the ring follows the feet + 0.06, spins `spin` deg/s, its scale lerps 2.2 -> 1
over `lockIn` (`-1.2 x` + 2.2); the crosshair sits above the head (+ 0.7, bobbing 0.08 x sin(3 t)), faces the camera
(`LookRotation(camera - pos, up)`), scale `1.15 - 0.35 x` ...; Paint sets a property-block colour (x 0.85, alpha 0.5
floor). On the page: on the standard body at the 10 m point (feet y 0, head y 1.1), tint by the race the cue names
(default `gold`). Built only if tto.md cues `preyFx` (question 9).

### T4. Already built for these prefabs

GroundHugEmitter (apexHunt_crouch / _impact / _land / _takeoff, chainLightning_overload, venomPhantom_coil / _requiem),
TrailRendererModern + StaticMesh (apexHunt_arrow, chainLightning_arrow), LineRenderer + RabbitTracer (venomPhantom_beam,
_shot), Shuriken (every `head` / burst system), `Particles/Standard Unlit` (`tto_Stone`, tto_sheep.js:161).

## Interfaces (fixed up front, so the builders run in parallel)

1. **`api.propModel(slot)`** (lead, index.html): a fresh Object3D of the prop worn in that slot (`buildProp(p)` +
   `finishProp` + `skinProp`, so a visitor's skin and the AdditiveAlpha glow twin come along), its root's position
   reset to 0, quaternion identity, scale the prefab's (`p.nodes[0].s`); `userData.rootMesh = { geometry, maxY }` when
   the prefab's root node has a mesh (42 of the 45 Chameleon second pieces; not bdArrow, eclipseArrow, paperArrow), else
   null; null when the slot is empty. Unity space (prop nodes are, `index.html:941-961`), so it hangs inside an
   effect's mirror group as is. Freed with the effect (geometry is the prop data's: share, don't dispose).
2. **A `"hideProp"` cue kind** (lead): `[t, "hideProp", "L", {"kill": d}]` takes `C.props[slot]`'s meshes off the
   camera's layers from t for d seconds (the LOOK mechanism, `index.html:4423-4441`, keyed per cue; ended by a new
   pick too). The 18 coroutines of "Read this first" 5 hide `mWep2` = slot L (also with the Snooker set: the cue).
3. **A shared shell material** (lead, index.html, exposed as `api.shellMaterial({ color, alpha, k, blend })`): the
   CosmicRift shell's vertex patch with its k a uniform / define, colour and alpha constant, `BackSide`; blend
   "srcColor" = CustomBlending SrcAlpha / SrcColor for rgb. Canvas alpha (the page renders over a transparent canvas):
   blendSrcAlpha One, blendDstAlpha OneMinusSrcAlpha with the output alpha = its brightest channel x alpha (fxMaterial's
   additive trick). Used by HERO_SKINS FX/Blend, FX/Invisible (part 10) and mesh.js FX/Invisible (part 3).
4. **A cue `life`** (lead, Fx): when the cue has `life`, the root EffectControl reads `{ ...ec, life }` (Final
   Entrapment: `effectControl.life = mDuration`, `Chameleon.cs:9161-9167`; the prefab's 6 s).
5. **The legacy emitters' `collide` hook** (the Cat's Interfaces, index.html `legacyParticles`), for worldcollider.js.
6. **Extractors** (lead): LAYOUTS, WorldParticleCollider, AdditiveAlpha `cut`, the graft with part 7's matching and
   BB's PSR materials; TTO: `scaleTex`; `SKILL_FX["chameleon"]` is tto.md's.
7. **Unchanged, used:** tto_sheep.js's LineRenderer (`driven`, `pts`, `world`, `color`, `width`, `draw`), api.spawn
   with `followNode` / `local`, the entry's `"builds"`, HERO_SKINS / HeroSkin, `api.worn`.

## Rank by value (effects made right / effort)

| rank | part | Chameleon effects | other classes | work |
|---|---|---|---|---|
| 1 | Chameleon_nAttack + propModel | every Combo arrow (nAttack1, Left / Right Stride, Double Strider), Clear Arrow | 0 | ~60 + ~20 lines |
| 2 | hero looks FX/Blend, FX/Invisible + shell helper | Charge Attack, Perfect Blend, True / Mass Invisibility | (CosmicRift shares the helper) | ~40 lines |
| 3 | hideProp cue kind | 18 shot coroutines | any class whose code hides a hand piece | ~15 lines |
| 4 | Chameleon_needlePrison + AdditiveAlpha | needlePrison (unbuildable today) | AdditiveAlpha: Cat, Mole | ~20 + the Cat's ~25 lines |
| 5 | Shuriken graft (name + material match) | thunderDragon_ring2, zeroShot_ring | Bison, Cat (same graft) | ~25 lines (shared) |
| 6 | ChameleonLightning | 7 TTO prefabs (Chain Lightning, Venom Phantom's echo) | 0 | ~50 lines |
| 7 | WorldParticleCollider | tormentRain_fire | Cat 2, Rabbit 2 | the Cat's ~25 lines |
| 8 | Chameleon_campFire layout | campFire1 / 2 (unbuildable today) | 0 | 1 line |
| 9 | DoubleTexture | the Thunder Dragon skeleton | Rabbit stickyGum | ~8 lines |
| 10 | FX/Invisible on a mesh | clearArrow's look | 0 | ~10 lines (with the helper) |
| 11 | ChameleonAfterimage + TTO/ChameleonSpirit | venomPhantom_ghost, apexHunt_arrow's ghost | 0 | ~60 + ~60 lines |
| 12 | fx:castRing (one line), cue `life` (one line) | castRing in every cast1, finalEntrapment's length | 0 | 2 lines |
| 13 | ChameleonPreyReticle | preyFx (only if cued) | 0 | ~40 lines |

After all, add to `BUILT` in `pipeline/wardrobe_fx_inventory.py`: `Chameleon_nAttack`, `Chameleon_needlePrison`,
`Chameleon_campFire` (draws nothing), `WorldParticleCollider`; `ParticleSystem` / `ParticleSystemRenderer` only if the
graft is made generic (else say in its comment that the grafted ones are drawn); run it again (the recipe's rule).

## Who builds what (never two owners for one file; as `plans/fx_wolf/build_rules.md`)

| agent | owns | builds |
|---|---|---|
| A: chameleon | `wardrobe/fxparts/chameleon.js` (new) | Chameleon_nAttack (both branches, Fatal Strike's spawn), Chameleon_needlePrison |
| B: mesh | `wardrobe/fxparts/mesh.js` | Self-Illumin/DoubleTexture, FX/Invisible (through `api.shellMaterial`), Transparent/AdditiveAlpha (if the Cat's builder has not) |
| C: collider | `wardrobe/fxparts/worldcollider.js` (new, if the Cat's is not in) | WorldParticleCollider |
| D: tto | `wardrobe/fxparts/tto_chameleon.js` (new) | ChameleonLightning, ChameleonAfterimage + TTO/ChameleonSpirit (api.shader), ChameleonPreyReticle |
| bat.js's owner | `wardrobe/fxparts/bat.js` | `fx:castRing` for the Chameleon (one line) |
| lead | `wardrobe/index.html`, `pipeline/wardrobe_fx.py`, `pipeline/wardrobe_fx_tto.py`, `pipeline/wardrobe_fx_inventory.py`, `wardrobe/fx_cues/chameleon.json` | Interfaces 1-6; HERO_SKINS FX/Blend / FX/Invisible; LAYOUTS, graft, `cut`, `scaleTex`; `FX_PART_FILES += "chameleon", "worldcollider", "tto_chameleon"`; `BUILT`; the rebuild and the cues |

Rules as the Penguin's: `node --check`, no browser for the builders, never `wardrobe_fx.py chameleon` /
`wardrobe_fx_tto.py chameleon` without `--probe` (the lead rebuilds once). If the Bison's / Cat's builders run at the
same time, `mesh.js`, `shuriken.js`, `worldcollider.js`, `wardrobe_fx.py` and `wardrobe_fx_tto.py` keep one owner across
the classes (the Bison's build is in the working tree now: `fxparts/bison.js`, `tto_bison.js`, `uvscroll.js`
untracked, `alphatimer.js` and `index.html` modified).

## Paste-ready cue fragments (the parts' shapes; times from the sources cited, the rest the clip researchers')

Keys as the Wolf / Sheep / Penguin / Bat cue files (`"<clip>": {"why", "cues"[, "builds"]}`); valid JSON fragments.

```json
  "nAttack1": {
    "why": "RPC_nAttack1: the shot 0.2 s in (Bible chm_nAttack1-4: waits 0.2 s, one arrow; Chameleon.cs:15586-15643), firePos = hero + (0, 1.5, 0) + forward (:15586) aimed at the target's centre (:15591); RPC_nAttack_fire (:8447-8497): the nAttack arrow (the worn arrow copied, Chameleon_nAttack.cs:114-150; parts.md part 1), 40 m/s with Bow Mastery (:100), life 0.8 s (:8482); its trigger meets the standard body 0.18 s after the spawn and RPC_nAttack_hit puts nAttack_hit at ClosestPointOnBounds (0, 0.68, 9.7), the hero's rotation (:8588; parts/calc.txt); the hand arrow hidden from the shot (:15538) to its re-show (:15802, its time the attacks report's)",
    "cues": [
    [0.2, "hideProp", "L", {"kill": 0.3}],
    [0.2, "fx", "nAttack", {"y": 1.5, "d": 1, "rot": [5.71, 0, 0], "to": [0, 0.6, 10]}],
    [0.38, "fx", "nAttack_hit", {"y": 0.68, "d": 9.7}]
    ]
  },
  "needlePrison": {
    "why": "Needle Prison's status on the hit target (Chameleon.cs:21750) puts needlePrison at its feet, identity, parented (CharacterControl.cs:36629-36638), Init(Clamp(2 x 0.3, 0.5, 2) = 0.6) (:36650): 16 needlePrison_arrow, one per 0.05 s on the 0.6 m ring (Chameleon_needlePrison.cs:158-211; parts.md part 2); it goes when the status ends (:16558), getDebuff(1 + sLv) + 2 s (Chameleon.cs:21745), cut at 10",
    "builds": ["needlePrison_arrow"],
    "cues": [
    [0, "fx", "needlePrison", {"d": 10, "kill": 10}]
    ]
  }
```

(In `nAttack1`, `rot` [5.71, 0, 0] is `LookRotation((0, 0.6, 10) - (0, 1.5, 1))` = pitch atan(0.9 / 9) down, as a cue's
Unity Euler; `kill` 0.3 of the `hideProp` and the hit's 0.38 = 0.2 + 0.18 are placeholders the attacks report replaces
from `:15802` and its own spawn time; `needlePrison`'s 0 is the status time in its tile.) The other part-carrying cues,
shapes only:
- Camp Fire: `[t, "fx", "campFire2", {"d": D, "rot": [270, 90, 0], "kill": 10}]` (`Chameleon.cs:9430-9452`).
- Torment Rain: `[t, "fx", "tormentRain_fire", {"d": 10}]` (the cage's centre, `:25505`, `:25996`).
- Final Entrapment: `[t, "fx", "finalEntrapment", {"d": 10, "life": L}]` (`:9142-9167`; L = mDuration, cut 10).
- Perfect Blend / Charge Attack: `[t, "skin", "FX/Blend", {"kill": K}]`.
- True / Mass Invisibility (self): `[t, "fx", "invisible"]`, `[t + 0.2, "skin", "FX/Invisible", {"kill": K}]`.
- Immunity's look (no EffectControl): `[t, "fx", "Immunity", {"y": 1.16, "scale": 0.7, "kill": K}]`
  (`CharacterControl.cs:36595-36610`: bounds centre 0.98 + 0.1 x 1.8 up, `Clamp(0.3 + 0.4, 0.5, 1.5)`).
- Fatal Strike's look: `[t, "fx", "fatalStrike", {"bone": "mount_Hand_L", "kill": K}]` and the same on
  `mount_Hand_R` (`CharacterControl.cs:37077-37110`).

## How sure I am

| item | sure | why |
|---|---|---|
| The 3 layouts | high | exact byte use (4, 8, 0) and the decoded values (mLv 1 / 2; the reference resolves to needlePrison_arrow) |
| The arrow is the worn mWep2 copy, Euler(0, 270, 270), 40 m/s, 0.8 s | high | plain lines in Chameleon_nAttack.cs and Chameleon.cs; the predicates at :108 worked through (both true) |
| The 0.18 s contact | medium | Unity's 0.02 s fixed step assumed (the game's TimeManager not read); the box against the capsule sampled |
| FX/Blend / FX/Invisible passes and constants | high | the compiled shader text read from BB's data; the pass order from the file |
| Own-team branch = FX/Blend / FX/Invisible | medium-high | the branch on `layer != mPlayer.layer`; the FX/Blend loop's placement in the else read from the flattened code's order |
| Needle Prison 16 x 0.05 s, 67.5 degrees, r 0.6 | high | the state machine worked through; the target body's radius from the Bat decisions |
| The graft's data equal BB's | high | field for field in `tto_bbcopies.json` vs `ps_sum.txt` |
| WorldParticleCollider bounce 0 = stuck | medium | the 3.5 manual's wording (no source); TTO dropped the module, nothing to compare |
| ChameleonLightning | high | small methods, every call and constant named |
| ChameleonAfterimage / ChameleonSpirit | medium | the Update and the shader read whole; Skip's names and Apply's property names not resolved |
| ChameleonPreyReticle | low-medium | only the calls and constants skimmed |

## Open questions (with my recommended answer)

1. **No arrow worn** (the page's bare hero has empty R / L; BB always holds one). Recommend: fall back to the starter
   set's arrow, `noviceArrow` (w_chm1), for the projectile only (the hand stays empty).
2. **Torment Rain's standing arrows show their lower half below the floor** (no ground mesh on the page). Recommend:
   accept (APPROX, noted); if it reads badly, worldcollider.js may clip a stuck particle's quad at y 0 for vertical
   billboards.
3. **ParticleSystem route.** Recommend the TTO graft now (as the Bison and the Cat), with part 7's (name, material)
   matching; the native 3.5 converter later if all 11 BB systems are wanted without TTO's bundles.
4. **Hero looks: own team or enemy view?** Recommend the own-team look (FX/Blend's yellow rim, FX/Invisible's blue rim
   on a 35 % ghost): it is what the player sees of her own Chameleon. The enemy view (a refraction shimmer, or nothing
   with Erase Senses) is not drawn.
5. **Fatal Strike on the Combo arrows.** The blood trail rides only on shots fired while the `fatalStrike` status holds
   (the Fatal Strike skill's charges, `Chameleon.cs:26313`). Recommend: the Combo tile without it; if the skills report
   builds a Fatal Strike sequence that ends in shots, those carry `"fatal": true`.
6. **Bow Mastery's 40 m/s.** Recommend 40 (passives on); `fx.at.speed` lets a tile choose 30.
7. **Clear Arrow.** Recommend the own-team look: the worn arrow's shape in FX/Invisible (35 % white + blue rim). Enemies
   would see no arrow.
8. **The hand arrow hiding** (18 coroutines). Recommend build the `hideProp` cue kind and let each clip report cue it:
   the arrow visibly leaves the hand in every shot.
9. **The prey reticle (TTO preyFx).** Recommend build it only if tto.md cues `preyFx` on the 10 m target (the standing
   rule puts enemy effects there); default tint gold.
10. **The spirit shader.** Recommend a faithful port of the fragment (the noise, the rim, the triplanar scales, the depth
    prepass); a plain rim-only approximation would lose the moving wisps that are the afterimage's look.

## Verification

Checker pass 2026-11-13, home PC, read only (no build, no browser). Re-read against the source: the BB lines this report
cites in `Chameleon.cs` (:8473, :8482, :8497, :8588, :9417-9452, :9424-9430, :15586, :15591, :16358, :17882-17944,
:18544, :18592, :20687, :21155, :21745-21750, :24575, :25505, :25996, :26313, :29360, :37647, :37992),
`Chameleon_nAttack.cs` (:21-66, :94-100, :114-128, :140-150, :177, :199-247, :274-318, :336-400),
`Chameleon_needlePrison.cs` (:23-25, :47, :158-211), `Chameleon_campFire.cs` (:36, :71, :82, :97, :106, :219),
`Math.cs:838-843` (rotateH), `CharacterControl.cs` (:154, :16289, :16558, :16590, :32494, :32649, :36595-36610,
:36629-36650, :36770, :36880, :36949-36960 -> Block_989 :42212-42213 `Yield(2, 0.2)`, :36991, :37077-37110, :37161);
the TTO cites `pseudo/Chameleon.c` :364, :423 (SlideTo 0.18), :12802, :35707, :36425, :36548, :36631, :37236, :38893;
`disasm_ChameleonLightning.txt` NewArc (:372-400); the LAYOUTS format against `wardrobe_fx.py` (`SIZES` "r" = 8,
"i" = 4); the existing graft (`graft_shuriken`, wardrobe_fx.py:393-440); `bat.js`'s hook; the page's slot mapping
(index.html `placementOf`: R = the first piece, the bow; L = the second, the arrow; `item_map.json`: w_chm25 =
snookerBall (R) + snookerCue (L), w_chm1 = noviceBow + noviceArrow); the Bible (`chameleon-skill-reference.md:376-384`,
Needle Prison 2 / 3 s + 2). Times, layouts, the needle ring, the shader passes, the castRing timing, Immunity's
`y 1.16 / scale 0.7`, the Camp Fire / Final Entrapment / Torment Rain shapes and the TTO part specs hold, except:

1. **The `nAttack1` fragment aims at the wrong point, and part 1 has no floor end.** The fragment aims the arrow at the
   body centre (`rot [5.71, 0, 0]`, `to [0, 0.6, 10]`, hit 0.38 s at (0, 0.68, 9.7)). The standing answer for every
   class's Normal Attack is the game's own untargeted shot at the 10 m ground point (Bat decision 1, Penguin 1, Sheep 3),
   and `attacks_emotes.md` (its block, :156-168) cues it so: `fireDir = tDir - (0, 1.5, 0) - forward` (Chameleon.cs:15591,
   with `tDir = aim - hero`, :5984-6048) gives pitch 9.4623 deg; the arrow meets the floor 9.1241 m / 40 m/s = 0.2281 s
   after its 0.2 s spawn: hit 0.4281 s at d 10; the hand arrow is hidden 0.2-1.8 s (`hideProp` kill 1.6). Part 1's
   "without a `to` it flies the 0.8 s (32 m) and goes" would send that arrow through the floor: `OnTriggerEnter` ends the
   arrow on the ground too ("the ground counts", Chameleon_nAttack.cs:336-400; attacks_emotes.md :136-139). The part
   must end the arrow when its root reaches y 0 (or at a cue `end`, as the hit's time), besides the `to` body test.
2. **`needlePrison`'s `kill` is 5, not 10.** At max rank 2 with Mass House Lock (passives on) the status lasts
   `getDebuff(1 + 2, cha, cha) + 2` = 3 + 2 = 5 s (Chameleon.cs:21745; Bible :378: "2 / 3 s contested, +2 s"), well under
   the 10 s cut.
3. **Fatal Strike's look keeps world identity, not its parent's turn.** On the arrow: `Instantiate(fatalStrike,
   Vector3.zero, Quaternion.identity)` (Chameleon_nAttack.cs:205), `transform.parent = copy` keeps that world pose (:212),
   and only `localPosition` is set after (:233 / :241): its rotation is world identity at the spawn (the hero's facing on
   the page), not the arrow's 9.46 deg pitch. Part 1's `api.spawn(... local: { pos: [0, 0, maxY - 0.1] })` with no `rot`
   gives it the arrow's turn: pass `local.rot` = the inverse of the arrow root's spawn rotation (for the 10 m shot,
   `[-9.4623, 0, 0]`). Its position `(0, maxY - 0.1, 0)` is in the copy's local space, so it is scaled by the copy's
   (the prop root's) scale. Likewise the two hand looks (CharacterControl.cs:37077-37110: Instantiate at the bone's
   position with `Quaternion.identity`, then parented) keep world identity, where the page's `bone` option sets
   localRotation identity: APPROX (a small turn of the blood trail) unless `rot` is given.
4. **The graft needs more than a list entry.** Today's `graft_shuriken` (wardrobe_fx.py:393-440) matches by node path
   through a dict (`tto_at = dict(zip(node_paths(tto_nodes), tto_nodes))`, :426: a repeated path keeps only the last
   node, the very collision part 7 describes), puts the systems on a new `_shuriken` child node, and sets every grafted
   renderer's material to the class's one `SHURIKEN_MAT[cls]` (:417). The Chameleon's five systems use four BB
   materials (spark3, thunderDragon_particle, zeroShot1/2 multiply2, zeroShot3), so `SHURIKEN_MAT["chameleon"]` has no
   single value: part 7's (name, first-material) match and "keep BB's mats" are a change to `graft_shuriken` (and BB's
   walk must keep the PSR's materials), not only `SHURIKEN_FROM_TTO["chameleon"] = [...]`.
5. **T2's cue options conflict with `tto.md`, and cannot work.** The `{"slide": [[t, x, y, d, yaw, 0.18]], "fire": [t],
   "shatter": t}` shape would need different times per ghost, but the one `venomPhantom2` entry plays five times with the
   same cues (each step re-runs it, index.html `startStep` -> `fxStart`). The part reads `tto.md` section 7's options
   instead: on the ghost `bow` (the hand spot at the shot, hero-relative), `face` (the foe point it turns to), `slide`
   0.18, `slots` (slot = the live ghosts of this play % 5); on each `venomPhantom_beam` cue `ghost: k` (ghost k's Fire():
   `tto/venomPhantom_ghostFire` at its bow point, the flare); on the rupture cue `shatterGhosts: true` (every ghost's
   Shatter(): `tto/venomPhantom_ghostShatter`). Without a shatter, life 4 s.
6. **T3: build `release`, and take the cue's centre.** `tto.md` cues `preyFx` (Apex Hunt's lock, so the reticle is
   built) with `{"y": 0.6, "d": 10, "lockOnly": true, "release": 1.8, "kill": 2.05}`: `release` (s after the spawn) =
   `Release@0x1C4EA60`, which `ClearApexLocks` calls in the volley (pseudo/Chameleon.c:37236, :37147), then the 0.25 s
   fadeOut. The root sits at the collider centre (AddApexLockFx), so the part takes feet = root y - 0.6 and head = root
   y + 0.5 for the standard body (under a lift, `tto.md` Verification 2, the root is given relative to the lifted hero).
7. **Parts missing from "Who builds what"** (`tto.md` section 6): P5 the `Chameleon.ApexArrow` code mover
   (`CODE_MOVERS` in wardrobe_fx_tto.py + its page part: agent D, `tto_chameleon.js`: from the spawn to `to` in 0.12 s,
   straight, turned along it); P6 HERO_SKINS `"Chameleon.StormDarken"` (lead, index.html: every hero renderer to
   (0.07, 0.07, 0.09) by k = clamp01(4 t), held, back over 0.6 s ending at `kill`); P7 the cue option `stop` (lead, Fx:
   Shuriken stops emitting); P8 the followState `cut` across a sequence step (lead, Fx.update). Add them to the table
   and to "Rank by value".
8. **`hideProp` before its kind exists plays a sound.** `fxDue` sends every kind but fx / skin / lift / clone to
   `Sound.play` (index.html:4894) and `fxStart` preloads it (:4823), so a `hideProp` cue pasted before Interfaces 2 is
   built asks for `sfx/L.mp3`. Build the kind first (and add `"hideProp"` to those two skips).
9. Line drift only (index.html and bat.js are being edited by another build): `bat.js`'s hook is :442 (was :441).

Not checked here (another checker's): `effect_only.md`'s RPC_ listing.

### Corrected paste-ready fragments

`nAttack1` (the attacks report's block, which is the one to paste; shown here with the parts' options it needs):

```json
  "nAttack1": {
    "why": "plans/fx_chameleon/attacks_emotes.md (its why, :158): RPC_nAttack1 (Chameleon.cs:15380-16051): voice nAttack1 at 0; 0.2 s: the hand arrow (mWep2, the page's L) hidden until 1.8 s (:15516-15548, :15761-15813), bow_fire1 (plunger with the plunger bow), the nAttack arrow at mPos + (0, 1.5, 0) + forward (:15586) aimed at the untargeted 10 m ground point (:15591, pitch 9.4623 deg; Bat decision 1), 40 m/s with Bow Mastery (Chameleon_nAttack.cs:100), the worn arrow copied (:114-150; parts.md part 1); it meets the floor 0.2281 s later and RPC_nAttack_hit puts nAttack_hit there with the hero's rotation (:8588)",
    "cues": [
    [0, "voice", "nAttack1"],
    [0.2, "hideProp", "L", {"kill": 1.6}],
    [0.2, "sound", "bow_fire1", {"notWorn": ["R", "plungerBow"]}],
    [0.2, "sound", "plunger", {"worn": ["R", "plungerBow"]}],
    [0.2, "fx", "nAttack", {"d": 1, "y": 1.5, "rot": [9.4623, 0, 0]}],
    [0.4281, "fx", "nAttack_hit", {"d": 10}]
    ]
  },
  "needlePrison": {
    "why": "Needle Prison's status on the hit target (Chameleon.cs:21750) puts needlePrison at its feet, identity, parented (CharacterControl.cs:36629-36638), Init(Clamp(2 x 0.3, 0.5, 2) = 0.6) (:36650): 16 needlePrison_arrow, one per 0.05 s on the 0.6 m ring (Chameleon_needlePrison.cs:158-211; parts.md part 2); it goes when the status ends (:16558): getDebuff(1 + 2) + 2 (Mass House Lock, passives on) = 5 s at max rank 2 (Chameleon.cs:21745; Bible chm_needlePrison1-2)",
    "builds": ["needlePrison_arrow"],
    "cues": [
    [0, "fx", "needlePrison", {"d": 10, "kill": 5}]
    ]
  }
```

(`needlePrison`'s 0 is the status time in its tile, as before.) Part 1's Fatal Strike spawn, corrected:
`api.spawn("fatalStrike", {}, { followNode: root, local: { pos: [0, 0, (maxY - 0.1) * copyScale], rot: <the inverse of
the arrow's spawn turn, [-9.4623, 0, 0] for the 10 m shot> } })`. The shapes-only list: Fatal Strike's hand look
`[t, "fx", "fatalStrike", {"bone": "mount_Hand_L", "kill": K}]` keeps its APPROX turn (item 3).
