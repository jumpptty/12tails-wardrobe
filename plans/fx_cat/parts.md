# Cat effects: the parts the page cannot draw yet (or draws wrongly)

Research 13/11/2026, home PC (one of the Cat fx researchers; scope: every part the Cat's effects need: the inventory's 67,
the 9 Cat prefabs it does not list, the Unity components `wardrobe_fx.effect()` drops, the shaders, and the released TTO
skills' prefabs). Models: `plans/fx_penguin/parts.md`, `plans/fx_sheep/parts.md`, `plans/fx_bat/parts.md`,
`plans/fx_bison/parts.md`. Read only: nothing in `wardrobe/data` was written; `wardrobe_fx.py` / `wardrobe_fx_tto.py`
ran with `--probe` only; no browser. `Cat.cs`, `UVScroll.cs`, `StatusControl.cs`, `Cat_supportFire.cs`,
`Cat_grandCasinoArcade.cs`, `AlphaTimer.cs`, `Math.cs`, `CharacterControl.cs` lines are `D:\12tails\DecompiledSource\<file>`;
TTO is `TTO1102:` = `D:\12tails\DecompiledSource_TTO_2026-11-02` (`dump.cs`, `methods.tsv`, `pseudo/Cat.c`).

Probes (read only, outputs beside them) in `checks/fx_cat_research/parts/` (git-ignored):
- `probe.py` -> `probe.txt` (+ `mats.py` -> `mats.txt`): all 76 prefabs in `heroes/cat/effects` through `wardrobe_fx.effect()`
  with an unknown script's field bytes and raw words, every material's blend, and the components `effect()` drops.
  Last line: `UNKNOWN scripts: StatusControl [0], UVScroll [8], Cat_grandCasinoArcade [8], Cat_supportFire [12]`.
- `probe_ps.py` -> `probe_ps.txt` (+ `ps_sum.py` -> `ps_sum.txt`): the full type trees of the dropped components
  (supportFire_hit's ParticleSystem + renderer, luckyDice's / treasureHunt's legacy emitters and WorldParticleCollider) and
  the game's PhysicsManager (gravity -9.8).
- `calc.py` -> `calc.txt`: Support Fire's cannonball, `Math.getTrajectoryVector` and the flight to the ground.
- `tto_probe.json` (supportFire_hit), `tto_bbcopies.json` (TTO's copies of the blocked BB prefabs and `deadEffect`),
  `catalog_keys.py` -> `catalog_keys.txt`, `tto_released.json` + `tto_summary.py` -> `tto_summary.txt` (the 26 prefabs of
  the released TTO skills).

## Read this first

1. **Four Cat scripts, one shared script, one Unity component and one Unity 3.5 system block or spoil eight effects.**
   | effect | what blocks it | today |
   |---|---|---|
   | `deltaStrike` | `UVScroll` (8 bytes, no layout) | **not buildable**: `wardrobe_fx.py` raises on the bytes |
   | `grandCasinoArcade` | `Cat_grandCasinoArcade` (8 bytes, no layout); the hero's code switching its clips | **not buildable** |
   | `supportFire_fire` | `Cat_supportFire` (12 bytes, no layout); `Transparent/AdditiveAlpha` on an effect mesh | **not buildable** |
   | `supportFire_hit` | Unity 3.5's ParticleSystem (Shuriken), dropped by `effect()` | builds without its burst |
   | `supportFire_cannon` | "ready" in the inventory, but `Transparent/Opaque1` at `_Color.a` 0 + AlphaTimer (alphatimer.js drives no Opaque1), an Animation with `play` off (mesh.js builds none), the hero's `Rewind(); Play("fire")` and `AlphaTimerFadeOut(0.5)` | **invisible** |
   | `luckyDice`, `treasureHunt` | `WorldParticleCollider` (legacy particles bouncing on the ground), dropped by `effect()` | dice / coins fall through the floor |
   | `damagePlus` | `StatusControl` (0 bytes: extracts) | fine; no EffectControl, so the cue's `kill` is its life (no page code) |
2. **Shared with the Bison (`plans/fx_bison/parts.md`, researched, not built yet):** UVScroll (its part 1, same spec),
   AlphaTimer driving Opaque1 (its part 2: the Cat's cannons), and the Shuriken graft from TTO's copy (its part 5:
   `SHURIKEN_FROM_TTO`). Whichever class is built first builds them once; the Cat adds one table entry and two
   AlphaTimer details (part 4 below).
3. **Built since the inventory (the Bat's build, in the working tree 2026-11-13):** `particles.js` draws the Cat's
   `multiply` (205: deltaStrike `ShadowLine2`, deltaStrike_cat / _ring `ShadowRay`, pillagePlunge rings' `Ray1_m`,
   `Smoke4_multiply`, `Dust10`, `ShadowLine3`), `Particles/AdditiveOffset` (8: nAttack_hit, backStab_hit, hiddenBlade_hit,
   forwardLunge_hit, pillagePlunge_hit, reverseThrust_hit) and `Particles/AlphaOffset` (6: the words on copycat_hit,
   twoPair_hit, lifeGamble / skillGamble heal / hit). mesh.js draws `FX/Phoenix` (GrandCasinoArcade1), built-in 7
   `opaque` (doubleDown1 / 2's cactus) and Opaque1. `premul` (207) draws `cat_dead`. Nothing else to do for them.
4. **New proof for the Penguin's medium-sure built-in shader names.** TTO re-serialised BB's prefabs with Unity's own
   shader names (`tto_bbcopies.json`, `tto_probe.json`): `cat_dead` (built-in 207) = `Legacy Shaders/Particles/Alpha
   Blended Premultiply`; `ShadowLine2` (205) = `Legacy Shaders/Particles/Multiply`; `Bomb2` (206, the material of
   supportFire_hit's system, rip `Material/Bomb2_0.mat` `m_Shader: {fileID: 206}`) = `Legacy Shaders/Particles/Multiply
   (Double)`. So `BUILTIN_BLEND` 205 / 206 / 207 (`wardrobe_fx.py:46`) are now **certain**; worth a line in its comment
   and in `plans/fx_penguin/parts.md`'s "How sure" (it says medium).
5. **The inventory misses nothing that blocks.** The 9 unlisted prefabs (`bleed`, `damageRoulette`, `fortune`, `insight`
   (status looks, `CharacterControl.cs:9156`, :36258, :36239, :36406), `gambleRing`, `luckyCard_hit`,
   `forwardLunge_dust`, `grandCasinoArcade_hit0`, `deadEffect` (hero prefab fields / hit RPCs)) use built parts only
   (`probe.txt`). Of them `damageRoulette`, `fortune`, `insight` have no EffectControl: they live until the status ends
   (the cue's `kill`). `damageRoulette` is parented to the character at its collider centre and scaled
   `clamp(2 x radius + 0.4, 1, 1.5)` (`CharacterControl.cs:36258-36273`): a cue's `y` / `scale`, no part. Inventory gaps
   (for `wardrobe_fx_inventory.py`, later): it does not see shaders (supportFire_fire's AdditiveAlpha, the cannon's
   alpha-0 Opaque1) nor the components `effect()` drops.
6. **Game quirks (offer to the user for the Bible; none changes a cue).**
   - Support Fire's balls never fly at the target: each cannon aims `24 + Random.Range(0, 24)` m straight ahead of the
     Cat (`Cat.cs:41212`), and `getTrajectoryVector`'s correction (`Math.cs`, `num += num - num cos f - 0.1 d / v`) lowers
     the arc to 3-6.4 degrees, so they land **18-26 m ahead of the muzzle** (`calc.txt`), short of the aimed point.
   - Grand Casino Arcade's tint flicker reads `mRenderer` (`Cat_grandCasinoArcade.cs:28-50`); TTO's copy of the prefab
     reads `mRenderer: None` (`tto_bbcopies.json`), so on TTO the third sign material stays invisible (BB: it pulses).
   - TTO dropped the coins' ground bounce: TTO's `treasureHunt` system has its CollisionModule off, `luckyDice` keeps it
     (world, bounce 0.5) (`tto_bbcopies.json`).

## The Cat's blocked set

"Where" is where BB spawns it. Cue shapes below use the Wolf / Sheep / Penguin / Bat keys; the times and the skill
tiles are the skills researchers' (`skills_a.md`, `skills_b.md`), so treat the cues here as the parts' contract.

| effect | skill (spawn) | missing part(s) | where |
|---|---|---|---|
| `deltaStrike` | Delta Strike (`$RPC_deltaStrike$22138`, Instantiate `Cat.cs:37482`) | UVScroll layout + part | hero + 0.5 forward, hero rotation, **scale 1.5 at sLv 2** (`:37495`) |
| `grandCasinoArcade` | Grand Casino Arcade (`$RPC_grandCasinoArcade$21905` case 2, `createEffect` `:27838`, `Find("grandCasinoArcade")` `:27858`) | Cat_grandCasinoArcade layout + part; the hero's `Play("fire")` x5 / `Play("destroy")` (`:28554`, `:28531`) | hero, hero rotation; followState |
| `supportFire_cannon` (x6) | Support Fire (coroutine `$RPC_supportFire$22224`, raycasts `:41060`, `createEffect` `:41084`) | AlphaTimer on Opaque1 (Bison part 2); `AlphaTimerFadeOut`; Animation with `play` off + rewind; the barrage | `(3i - 10.5, 0, -2)` i = 1..6, hero rotation |
| `supportFire_smoke` (xN) | `RPC_supportFire_fire` (`:10711`) | (ready) spawned by the barrage part | muzzle `cannon + (0, 1, 3)`, `LookRotation(fireDir)` |
| `supportFire_fire` (xN) | `RPC_supportFire_fire` (`:10741`, `Init` `:10753`) | Cat_supportFire layout + part; AdditiveAlpha in mesh.js | the muzzle, flying to the ground |
| `supportFire_hit` (xN) | `RPC_supportFire_hit` (`:10802`, Quaternion.identity), from the ball's trigger (`Cat_supportFire.cs:179`) | the Shuriken graft (Bison part 5) | the ground point under the ball, 18-26 m ahead |
| `luckyDice` | Lucky Dice (`$RPC_luckyDice$21797`, Instantiate `:23872-23880`, hero position, identity) | WorldParticleCollider | hero |
| `treasureHunt` | Treasure Hunt (`RPC_treasureHunt` `:9078-9100`, `firePos`, identity) | WorldParticleCollider | `firePos` |
| `damagePlus` | Charge Attack (`$RPC_cAttack1$21702`, Instantiate `:20053`, parent `mount_Hand_R` `:20077`, `Init` `:20087`) | none (StatusControl draws nothing) | `mount_Hand_R`, local (0, 0, 0) |

## LAYOUTS (paste into `pipeline/wardrobe_fx.py`, after the Bison's block; drop the UVScroll line if the Bison's is in)

```python
# the Cat's parts (plans/fx_cat/parts.md, 2026-11-13; checks/fx_cat_research/parts/probe.txt: each instance's bytes are
# the listed fields exactly; StatusControl keeps every field private, 0 bytes, so it needs no entry)
LAYOUTS.update({
    "UVScroll": [("scroll_x", "f"), ("scroll_y", "f")],             # UVScroll.cs:67, :70 (8 bytes; Bison 2, Cat 1, Whale 1)
    "Cat_grandCasinoArcade": [("mRenderer", "r")],                  # Cat_grandCasinoArcade.cs:144 (8 bytes: its own SMR)
    "Cat_supportFire": [("mVelocity", "v3")],                       # Cat_supportFire.cs:240 (12 bytes; (0, 0, 30))
})
```

Values (`probe.txt`): deltaStrike_tri's UVScroll `scroll_x` 1.0, `scroll_y` 1.0 (not the 0.1 defaults); grandCasinoArcade
`mRenderer` [0, 75936] (the SkinnedMeshRenderer on the same node); supportFire_fire `mVelocity` (0, 0, 30).

Three more extractor lines (lead, `wardrobe_fx.py`):
- `WorldParticleCollider` stored as Light / TrailRenderer are (`wardrobe_fx.py:333`: `elif ty in ("TrailRenderer",
  "Light", "WorldParticleCollider")`): its fields as stored (`m_BounceFactor` 0.5, `m_CollisionEnergyLoss` 0,
  `m_CollidesWith` {m_Bits 1} = layer 0 only, `m_SendCollisionMessage` false, `m_MinKillVelocity` 0).
- `material()` (`wardrobe_fx.py:242-276`): for `shader:Transparent/AdditiveAlpha` also save `"cut"` = the material's
  `_AdditiveRange` float (`m_Floats`; shader default 0.9; PirateCannon_Fire 0.9, rip `Material/PirateCannon_Fire.mat`),
  as `wardrobe_data.py:281-297` does for the props.
- `SHURIKEN_FROM_TTO["cat"] = ["supportFire_hit"]` (the Bison's graft, part 6 below).

## Each part

Page parts plug in as the comment above `FX_PART_FILES` says (`wardrobe/index.html:3758-3793`): `wardrobe/fxparts/<file>.js`
default-exports `register(api)` and calls `api.part(type, build)`; `build(fx, node, comp, mat, nodeDef, data)` returns
`{ node, update(dt, cam) ("destroy" removes the node), stop?(), dispose?() }` or null; `"fx:<effect>"` = the hero's code
acting on that effect, built once on its root (comp null); `api.spawn(name, at, opts)` makes an effect a script
instantiates; `fx.cutAt` is the cue's `cut` in clip time, compared with `api.FX.t`. Space: every root hangs in the
effect's mirror group (Unity's world, the hero's feet at the origin, +z her facing, y 0 the floor).

### 1. UVScroll: `deltaStrike` (generic; the Bison's part 1)

**What it does in BB (`UVScroll.cs`).** Fields `scroll_x`, `scroll_y` (:67, :70; defaults 0.1, :26 / :29). Update (:42-46):
`renderer.material.SetTextureOffset("_MainTex", (Repeat(Time.time x scroll_x, 100), Repeat(Time.time x scroll_y, 100)))`:
the renderer's own material copy, its offset replaced, from the absolute clock.

**The Cat's use.** `deltaStrike_tri` (node 2): a 10-vertex SkinnedMeshRenderer (the delta, material `deltastrike`,
built-in 203 `alpha`, tint 0.5, texture `deltaStrike`) swung by node 1's `root` clip (2 s); scroll **(1, 1) per second**
(one texture width a second along both axes). EffectControl life 2. No AlphaTimer on that node (the shatter pane's
AlphaTimer is on node 10), so no shared-copy contention. The cue's `scale` 1.5 doesn't touch the uv.

**The page part.** Exactly the Bison's spec (`plans/fx_bison/parts.md` part 1, `fxparts/uvscroll.js`, about 25 lines:
clone the per-renderer material and its `map`, `map.offset.set((T x sx) mod 100, (T x sy) mod 100)` with `T` the page's
absolute clock, free both in `dispose`). The texture wraps (`fxMaterial`'s `withMap` sets RepeatWrapping,
`index.html` fxMaterial). Nothing Cat-specific.

### 2. Cat_grandCasinoArcade + the hero's clip switches: `grandCasinoArcade` (`fxparts/cat.js`, new)

**What the script does (`Cat_grandCasinoArcade.cs`; opaque predicates worked by hand).**
- Field `public SkinnedMeshRenderer mRenderer` (:144); privates `sQpTrSb8ri`, `NH5TxXGGpM` (:147, :150).
- Awake (:21-83): `mRenderer.materials` (Unity: per-renderer copies of every material) `[1]` -> sQp (:38), `[2]` -> NH5
  (:50); both found -> break (:62-64). (Every guard on the path is dead: :30 `-414407 != -414406`, :34 `-184106` equal,
  :39, :46, :51, :58 all fall through.)
- Update (:87-123), every frame: `num = 0.15 sin(4 Time.time)` (:94); `sQp._TintColor = (0.5, 0.5, 0.5, num)` (:103);
  `NH5._TintColor = (0.5, 0.5, 0.5, 0.15 - num)` (:115); break (:116-118). So material 2 (`GrandCasinoArcade2`) pulses
  alpha -0.15..0.15 and material 3 (`GrandCasinoArcade3`) 0..0.3, in counter-phase, period 2 pi / 4 = **1.571 s**.
- Both are built-in 200 `add` (`probe.txt`: saved tints a 0.502 and **0**: GrandCasinoArcade3 is invisible without the
  script). Particles/Additive clamps a negative alpha to 0.

**The hero's code on the same node (`Cat.cs`, coroutine `$RPC_grandCasinoArcade$21905`).** `mGrandCasinoAnimation =
effect.transform.Find("grandCasinoArcade")` (:27858) = node 1 (its Animation: `create` 1.467 s (default, plays by itself),
`fire` 2.5 s, `destroy` 1.0 s, all wrap 0; `probe.txt`). Then, max rank sLv 2 (Bible `cat-skill-reference.md:23`):
- clip t 0: `grandCasinoArcade1`, ring1, voice; `Yield(2, 0.4)` (:28796); t 0.4: the effect created (:27838);
  `Yield(3, 1.3)` (:28782); t 1.7: case 3, `i = 0` (:27946-27960) -> the loop at `IL_9BB` (:28506);
- each spin while `i < sLv x 2 + 1` (:28508): `mGrandCasinoAnimation.animation.Play("fire")` (:28554) + sound
  `grandCasino2` x2 volume (:28566-28578), `Yield(4, 2)` (:28784); case 4: the roll and hits (:27993-28265); `i < 2 sLv`
  -> `Yield(5, 0.7)` (:28780), else `Yield(6, 0.4)` (:28809); case 5 / 6 -> `i++` (`IL_160E`, :28595) -> `IL_9BB`;
- after the 5th: `grandCasinoArcade3` + `Play("destroy")` (:28513-28531), `Yield(7, 0.3)`, `Yield(8, 0.7)`, standby
  (:28454).
- So in **effect age** (spawned at clip 0.4): `fire` at **1.3, 4.0, 6.7, 9.4, 12.1**; `destroy` at **14.5**; the hero's
  standby (followState cut) at clip 15.9 = age 15.5, EffectControl life 16 + afterLife 1. A break out of `attack`
  (`IL_20BD`) plays no `destroy`: followState alone ends it.

**The page parts (cat.js, about 40 lines).**
- `Cat_grandCasinoArcade` (on node 1): first update, `mesh = node.children.find(x => x.isMesh)`; its material list
  (`withMaterials`, three groups) -> clone `[1]` and `[2]` (copy `onBeforeCompile`, as `alphatimer.js` `own()`), write them
  back; free them with the effect (`dispose`). Each frame: `n = 0.15 sin(4 T)` (`T` the page's absolute clock, as
  UVScroll), `m1.opacity = clamp01(2 n)`, `m2.opacity = clamp01(2 (0.15 - n))` (fxMaterial's `add` rule: opacity =
  min(1, 2 x tint.a), `index.html` fxMaterial).
- `fx:grandCasinoArcade` (the hero's code; `fx.cls === "cat"` only): own clock; at ages 1.3 + 2.7 k (k = 0..4)
  `fx.nodes[1].userData.fxAnim.play("fire")`, at 14.5 `play("destroy")`; nothing at or after `fx.cutAt`
  (`api.FX.t >= fx.cutAt`). Clips wrap 0 -> Once under mesh.js's rule; `fire` (2.5 s) is not playing when the next one
  comes (2.7 s), so `play()` restarts it.
- Cue shape (skills researcher's times): `[0.4, "fx", "grandCasinoArcade", {"cut": <standby clip time>}]`
  (15.9 at sLv 2, or the 10 s rule's cut: question 2).

### 3. Cat_supportFire: `supportFire_fire`, and the ball's hit (`fxparts/cat.js`)

**What it does in BB (`Cat_supportFire.cs`).**
- ctor (:13-34): `mVelocity = (0, 0, 30)` (:26). The prefab keeps it (`probe.txt`).
- `Init(ownerID)` (:38-63), called in the spawn frame (`Cat.cs:10753`): life `u2PTTORycU = 10` (:48), layer 1 (:51),
  `rigidbody.velocity = TransformDirection(mVelocity)` (:54): 30 m/s along its spawn rotation (`LookRotation(fireDir)`,
  `Cat.cs:10741`).
- FixedUpdate (:67-98): `life -= dt` (:74); at 0 `Destroy` (:81); else `transform.LookAt(position + velocity)` (:90): it
  points along its flight.
- OnTriggerEnter (:102-219): skips colliders on the owner's layer (:139), layer 1 (projectiles, :145), layer 2 (:151); on
  the owner's client (:157) `vector = mCollider.ClosestPointOnBounds(collider.bounds.center)` (:163) and
  `cat.RPC_supportFire_hit(vector, 0, 0)` (:179); then `Destroy(gameObject)` (:206).
- Physics (`probe.txt` skipped comps): Rigidbody mass 1, drag 0, **gravity on**, not kinematic; BoxCollider trigger
  0.25 x 0.25 x 0.5. Gravity -9.8 (`probe_ps.txt`: the PhysicsManager in mainData). The ground is layer 0: the cannons'
  own raycast finds it with mask 5 = layers 0 and 2 (`Cat.cs:41060`), so the ball's trigger meets it.
- `RPC_supportFire_hit` (`Cat.cs:10776-10802`): `Instantiate(supportFire_hit, hitPos, Quaternion.identity)` (:10802), then
  the area damage (8 m radius, :10825).

**The flight (`calc.txt`; `Math.getTrajectoryVector`, `Math.cs:885-1000`, guards worked by hand).** Target at the muzzle's
height (`y = 0`), `d = 24 + Random.Range(0, 24)` (int, 24..47) m ahead (`Cat.cs:41212`), speed 30:
`num = atan((v^2 + sqrt(v^4 - g (g d^2))) / (g d))` (the high-arc tangent, used as the angle **from vertical**, which is
the low arc), then the `y < 0.1` branch `num += num - num cos(0) - 0.1 d / v`; direction `sin(num) x flat(pos - target) +
cos(num) x up`. Results: elevation 2.99 deg (d 24) .. 6.41 deg (d 47); from the muzzle 1 m up it lands **17.98-26.23 m**
ahead after **0.60-0.88 s** (apex 1.11-1.54 m). With the cannons' lanes at x = +-1.5 / 4.5 / 7.5 no ball passes within
the standard target body (radius 0.3 at x 0, Bat decision 4): every ball lands on the ground.

**The page part `Cat_supportFire` (cat.js, about 30 lines).**
- Build: velocity `v = fx.uQuat(node) x (0, 0, comp.mVelocity[2])` (the spawn rotation from the cue's `rot`), life 10.
- Each fixed step 0.02 s (bat.js's `STEP`): `v.y -= 9.8 x 0.02`, `node.position += v x 0.02`, `node.quaternion =
  LookRotation(v)` (bat.js's `lookRot`). The ground test as `calc.py`: lowest corner `y - (0.125 cos p + 0.25 |sin p|)`
  (p = the downward pitch) <= 0 -> `api.spawn("supportFire_hit", {x: pos.x, y: 0, d: pos.z})` (Unity x = the cue's x;
  rotation identity = the cue's default facing, the hit is round), return `"destroy"` (the ball and its Cloud1 trail go,
  as Unity's Destroy). Life <= 0 -> `"destroy"`.
- `supportFire_hit` must be in `fx.json`: the Support Fire cue entry's `"builds": ["supportFire_fire", "supportFire_smoke",
  "supportFire_hit"]` (the Bat's `builds` key, `fx_cues/bat.json`).

**Its material: `Transparent/AdditiveAlpha` in mesh.js (the shaders owner).** The ball (`PirateCannon_fire`, a 135-vertex
StaticMesh, material `PirateCannon_Fire`, texture `PirateCannon_fire`: a dark iron top, a flame glow below; `_Color` 0.784,
`_AdditiveRange` 0.9). Shader (`Assets/Resources/gameassets/shader/AdditiveAlpha.shader:1-34`): pass 1 `Lighting On`,
`Material {Ambient/Diffuse [_Color]}`, `AlphaTest GEqual [_AdditiveRange]`, `combine primary x texture double, primary
alpha x texture alpha` (ZWrite on, Cull Back); pass 2 unlit, ZWrite Off, Cull Off, `Blend SrcAlpha One`, `AlphaTest LEqual
[_AdditiveRange]`, `combine texture, texture alpha`. Page: `material()` branch `"shader:Transparent/AdditiveAlpha"` -> a
list: pass 1 = `lit(d, map, {transparent: false, alphaTest: cut, side: FrontSide})` (Lambert, color 2 x _Color as sRGB,
the `opaque1` helper's `lit`), pass 2 = MeshBasic `map`, no colour, CustomBlending One / One with rgb x alpha and alpha =
the brightest channel, discard `a > cut`, `depthWrite: false`, DoubleSide: index.html's `glowTwin` (props,
`index.html:915-935`) as the model. Today the mesh falls to fxMaterial (alpha blended, warning). Also used by the Mole
(`napalm`, `nAttack` materials in the rip): worth the generic branch.

### 4. The Support Fire barrage: `supportFire_cannon` (cat.js `fx:supportFire_cannon`; alphatimer.js; mesh.js)

**What the hero's code does (`Cat.cs`, coroutine `$RPC_supportFire$22224`).**
- Clip t 0 (case 0): `actionState = "attack"` (:40864), `supportFire1` Once (:40894-40899), `supportFire_ring` at the hero
  (:40932), voice supportFire1 | supportFire2 (:40975-41030); six raycasts down from `hero + TransformDirection(3i - 10.5,
  2, -2)`, 4 m, mask 5 (:41060), each hit -> `createEffect(supportFire_cannon, hit.point, transform.rotation)` (:41084):
  on flat ground the cannons stand at **(3i - 10.5, 0, -2)**, i = 1..6, the hero's rotation; `Yield(2, 1 s)` (:41332).
- t 1.0 (case 2): `supportFire2` Loop (:40832-40837), `mUpdateTime = now + 0.25` (:40842) -> every FixedUpdate
  (`Yield(3, WaitForFixedUpdate)`, :41334) the loop `IL_729` (:41110-): while `attack` / `supportFire`, no move input
  (:41140, :41148 -> `RPC_supportFire0`), `sp >= 6`; when `mUpdateTime <= now`: `mUpdateTime = now + 0.01 x
  Random.Range(24, 36)` (:41174: **0.24-0.35 s**, on the next fixed step), a random cannon (:41185), muzzle `cannon +
  TransformDirection(0, 1, 3)` (:41207), `fireDir` (:41212, part 3), `RPC_supportFire_fire` (:41217); every 6th shot
  `sp -= hasSkill(404) ? 6 : 12` (:41255). First shot at about t 1.26.
- `RPC_supportFire_fire` (:10636-10770): the cannon `animation.Rewind(); animation.Play("fire")` (:10672-10677; clip
  `fire` 0.5 s, the recoil and wheels, nodes 3-6; the component's `play` is off, `probe.txt`); `supportFire_smoke` (life 1,
  its own sound `supportFire_fire`) and `supportFire_fire` at the muzzle, `LookRotation(fireDir)` (:10711, :10741).
- End: `RPC_supportFire0` (:10547-10630): `standby` (:10566), then every cannon
  `BroadcastMessage("AlphaTimerFadeOut", 0.5)` (:10603). The cannons' EffectControl (life 99, afterLife 0.5,
  followState) removes them 0.5 s later. `AlphaTimer.AlphaTimerFadeOut` (`AlphaTimer.cs:328-357`): start / delay /
  ease-in ends = 0, middle end = now, out end = now + 0.5: alpha lerps **Max -> Min over 0.5 s** from now.
- The cannon's look: SkinnedMeshRenderer `supportFire_cannon`, game shader `Transparent/Opaque1` with `_Color.a` **0**,
  AlphaTimer 0 -> 0.8 over 1 s, held 99 s (`probe.txt`); 0.8 < 0.95, so only Opaque1's pass 2 draws (a 0.8 see-through
  cannon). Today it is invisible: `alphatimer.js`'s `OPACITY` has no Opaque1 (`alphatimer.js:27`).

**What to build.**
- **alphatimer.js** (its owner): (a) the Bison's part 2 (Opaque1 driven on both passes: `opacity = alpha`); (b) the
  emitter gains `fadeOut(sec)` = `AlphaTimerFadeOut`: `d = i = 0`, `m = t`, `o = t + sec` (the clock unchanged), so the
  next frames lerp MaxAlpha -> MinAlpha (`AlphaTimer.cs:151-157`). Only Cat calls it (`alphatimer.js:15-16` says so).
- **mesh.js** (its owner): the Animation part also for a component with `play` off (today `if (!c.play ...) return null`,
  `mesh.js` Animation part): no pose until a part calls `play()` (Unity: the prefab pose stands); and `rewind()` =
  `Animation.Rewind` (the current clip's time to 0, so a following `play()` of the same clip restarts it: the same cannon
  can be picked twice within the 0.5 s clip). The interface comment above `FX_PART_FILES` gets one line.
- **cat.js `fx:supportFire_cannon`** (about 45 lines): each cannon registers in a module list keyed by `api.FX.gen` (the
  six cues of one play are built the same frame); the first one built owns the barrage clock (`fx.cls === "cat"`):
  - from its age 1.25 (clip 1.25: case 2 at 1.0 + 0.25), on the 0.02 s grid, until `api.FX.t >= fx.cutAt`: pick a
    living cannon at random, `fxAnim.rewind(); fxAnim.play("fire")` on its root (the Animation is on node 0); muzzle =
    its position + its rotation x (0, 1, 3); `dist = 24 + floor(rnd x 24)`; `fireDir` by part 3's formula (pure
    function, 10 lines, in cat.js); `api.spawn("supportFire_smoke", at)` and `api.spawn("supportFire_fire", at)` with
    `at = {x: muzzle.x, y: muzzle.y, d: muzzle.z, rot: [-elevation, 0, 0]}` (Unity Euler: LookRotation of a forward-up
    direction); next shot in `0.01 x (24 + floor(rnd x 12))` s;
  - at the cut: every registered cannon's AlphaTimer emitters `fadeOut(0.5)` (BroadcastMessage reaches every node:
    `for (const e of c.emitters) e.fadeOut?.(0.5)`); stop shooting. Balls in flight fly on (their own Fx).
  - no SP model on the page (question 3).
- Cue shape (skills researcher's times): six `[0, "fx", "supportFire_cannon", {"x": X, "d": -2, "cut": C}]`, X = -7.5,
  -4.5, -1.5, 1.5, 4.5, 7.5, plus the entry's `"builds"` (part 3).

### 5. WorldParticleCollider: `luckyDice`, `treasureHunt` (`fxparts/worldcollider.js`, new, generic; one index.html hook)

**What it does (Unity 3.5's built-in, no game source; the 3.5 manual "World Particle Collider").** On a legacy emitter's
node: each particle moving through a collider on a `Collides With` layer bounces: velocity reflected on the surface
normal and multiplied by **Bounce Factor** ("similar to the Particle Animator's Damping": the whole speed), the particle's
energy (life left) minus **Collision Energy Loss** seconds (killed below 0), killed when its speed after the hit is below
**Min Kill Velocity**; Send Collision Message off. Values (both effects, `probe_ps.txt`): bounce 0.5, loss 0, layer
mask 1 (layer 0: the ground, as above), min kill 0.

**The particles (`probe_ps.txt`).** Both one-shot, world space, ParticleAnimator force (0, -9, 0), damping 0.6,
autodestruct, ParticleRenderer max size 0.25, UV animation 2 x 2 tiles, 6 cycles:
- luckyDice: 12-36 dice at 1 m up, life 1-1.5 s, size 0.1-0.2, local velocity (0, 1, 0) + random (+-20, 0, +-20): they
  burst sideways, fall in about 0.5 s and skid / bounce out; colour animated (`alpha` material `luckyDice`).
- treasureHunt: 12-36 coins at 0.5 m up, life 1-1.5 s, size 0.1, velocity (0, 3, 0) + random (+-4, +-2, +-4): a fountain
  that lands and hops (`alpha` material `Gil`).
Without the collider (today) both fall through the page's floor.

**The page.**
- index.html (lead, `legacyParticles`, `index.html:4287-4345`): after `p.p.addScaledVector(p.v, dt)` call
  `this.collide?.(p, world)`; a false return removes the particle. The emitter object carries `collide` (null by default).
- worldcollider.js (about 25 lines): `api.part("WorldParticleCollider", (fx, node, c) => ...)`: the node's legacy emitter
  is in `fx.emitters` (built before the node's scripts, `index.html:3960-3961`: `e.node === node && e.setEmit`); set
  `e.collide = (p, world) => { ... }` and return null (nothing of its own to update). The test in the effect's Unity world
  (world space: `p.p` as is; local: through `fx.uMatrix(node)`): when `y < 0` and `v.y < 0`: `y = 0` (the hit point, a
  point particle), `v = (v.x, -v.y, v.z) x bounce`, `p.age += loss`, false when `|v| < minKill` (0: never) or the age
  passes the energy; only when `m_CollidesWith.m_Bits & 1` (layer 0 = the floor). shuriken.js's `collide()`
  (`shuriken.js:488-501`) is the model.
- APPROXIMATED: the floor is the page's only collider (the game also has walls / props on layer 0). Medium sure on the
  bounce maths: the 3.5 manual likens Bounce Factor to Damping (whole velocity); TTO's own conversion of luckyDice wrote it
  as Shuriken's `m_Bounce` 0.5 with `m_Dampen` 0 (normal component only, tangential kept) (`tto_bbcopies.json`). The
  difference shows only in how far the dice skid. Question 4.

### 6. Unity 3.5's ParticleSystem: `supportFire_hit` (`wardrobe_fx.py` graft, lead; `fxparts/shuriken.js` unchanged)

**The system (`probe_ps.txt`, `ps_sum.txt`; rip `supportFire_hit.prefab:130-140`).** Node `ParticleSystem` at (0, 0.2, 0),
localRotation (0.7071, 0, 0, -0.7071) = -90 deg about x (its +z points up). lengthInSec 1, no loop, play on awake,
`moveWithTransform` true; Initial: life 0.6-1.0, speed 0-5, size 1-2, rotation 0-2 pi, no gravity, max 1000; Shape cone
(type 4), radius 0.2, angle 25; Emission rate 0, **one burst of 12 at 0** (`cnt0` 12, `time0` 0, `m_BurstCount` 1); Size over
life 0.48 -> 1; Colour over life white -> black, alpha 1 / 1 / 0 at 0 / 0.5 / 1; renderer billboard, max size 0.5,
material `Bomb2` (built-in 206 `multiply2`, texture `Bomb2_0`: an orange explosion puff). So twelve fireball puffs burst
upward in a 25 deg cone and darken as they die.

**Why not read it in BB.** Unity 3.5 serialises it differently from what shuriken.js reads (TTO's newer layout): a
two-constant curve keeps its minimum as `minCurve`'s first key x `scalar` (no `minScalar`: shuriken.js would take 0, life
0-1 and size 0-2), bursts are `cnt0..3` / `time0..3` (shuriken.js reads `m_Bursts`: it would emit nothing),
`moveWithTransform` is a bool with true = local (shuriken.js reads 1 = world: inverted).

**The graft (the Bison's part 5).** TTO holds the same prefab (`tto_probe.json`: `tto/supportFire_hit`) re-serialised by
Unity: `moveWithTransform` 0, life `minScalar` 0.6, size `minScalar` 1.0, `m_Bursts` [{time 0, count 12}], material
`tto_Bomb2` = `Legacy Shaders/Particles/Multiply (Double)`. It matches BB's values field for field. So:
`SHURIKEN_FROM_TTO = {"bison": ["magmaClutter_ring2"], "cat": ["supportFire_hit"]}`; the BB node (`ParticleSystem`, index 1)
gets TTO's `ParticleSystem` + `ParticleSystemRenderer` dicts, and `mats = ["Bomb2"]` (BB's own material through
`material()` on the BB renderer's `m_Materials`, as the Bison recommends: `Bomb2` is already in fx.json shapes as
`multiply2`), or TTO's with `SHADER_BLEND["Legacy Shaders/Particles/Multiply (Double)"] = "multiply2"`
(`wardrobe_fx_tto.py:141`). Unlike the Bison's node, this one has no other renderer, so `mats[0]` is the system's own and
the Bison's shuriken.js change (prefer the renderer's own material) is not needed for it.
The other route, a native Unity 3.5 -> new-layout conversion in `wardrobe_fx.py` (the three differences above), would
cover all 11 BB systems (bison, cat, chameleon 2, mole 3, monkey, panda, rabbit, whale; inventory "Per part") without
needing TTO's bundles at build time; the graft needs TTO's bundles (home PC builds them anyway). Question 5.

### 7. StatusControl: `damagePlus` (no page code)

**What it does (`StatusControl.cs`).** All fields private (0 bytes). `Init(nChar, nStatus)` (:37-62): the character, the
status name, the clock `now + 0.5` (:50), active (:53). Update (:66-121): every 0.5 s, `Destroy(gameObject)` when the
character is gone (:91-95) or its `getStatusLv(status) <= 0` (:104-110). Draws nothing.

**The Cat's use.** `damagePlus` (an addsoft particle burst on the hand) is instantiated at the hero, `Quaternion.identity`
(`Cat.cs:20053`), parented to **`mount_Hand_R`** at local (0, 0, 0) (:20077-20081), `Init(mChar, "damagePlus")` (:20087),
right after `RPC_AddStatus("damagePlus", chargeLv, mDuration, ...)` (:20031); `mDuration = chaAdjust(12)` (:19723) =
**12 s** at the page's CHA 1 (the Penguin's `chaAdjust` sum). Only one at a time (:20045: not when one stands).

**The page.** No part: the cue `{"bone": "mount_Hand_R", "kill": 10}` (12 s cut at 10 by the standing rule; the bone
is in `data/cat/rig.json`). Add `"StatusControl"` to `BUILT` in `wardrobe_fx_inventory.py` with the comment "draws
nothing (data only), the cue's kill" (as `Sheep_seal`).

## TTO: the released skills' parts (for the TTO researcher's `tto.md`; listed here so nothing is missed)

The released Cat TTO skills (`anchorYank`, `crescentEclipse1`, `crescentEclipse2`, `dropAnchor`, `royalFlush1`) spawn 26
prefabs (`catalog_keys.txt`, `tto_summary.txt`). What the page lacks:
| part | prefab(s) | what it is (`TTO1102:dump.cs` declarations; RVAs from `methods.tsv`) | build home |
|---|---|---|---|
| `Cat_eclipseFx` | crescentEclipse_blade (mode 1), crescentEclipse_moon (mode 0) | fields mode, pivot, glow, disc, shadow, corona, bite (ParticleSystem), sound, landSound `disarm_hit`, moonSize 7; Awake@0x1be8070, LateUpdate@0x1be9930, Tint (MaterialPropertyBlock)@0x1be9de0, coroutines Rise@0x1bf3a20, EclipseRun@0x1bede70, Set@0x1bf5230, FlingRun@0x1bee430, RecallRun@0x1bf31e0, IgniteRun@0x1bf0210; called by the hero (Eclipse, Dismiss, HoldWeapon, Fling, Recall, Ignite) | `fxparts/tto_cat.js` |
| `Cat_anchorChain` | dropAnchor_chain | a 10-point LineRenderer (`m_Enabled` false in the prefab) between the holder and the anchor, linkLength 0.42, anchorRingHeight 1.8, maxSag 0.9; Bind@0x1be77b0, LateUpdate@0x1be7920 | `tto_cat.js` (LineRenderer itself: `tto_sheep.js`, built) |
| `Cat_royalCard` | royalFlush_card | Deal / Flip / Flash / Shatter / Gather coroutines, SetCard (the face atlas offset of `tto_royalFlush_face`, 6 x 4), GlowPulse; Awake@0x1beaaa0, DealRun@0x1beaab0, FlipRun@0x1beac30, GatherRun@0x1bead40, Shatter@0x1beb370 | `tto_cat.js` |
| `Cat_royalHandBanner` | royalFlush_hand | `hands` = 10 textures `tto_royalFlush_hand0-9` (exported: `tto_released.json` textures), banner / glow / rays renderers, plate, life 1.7, fadeTime 0.45; Show@0x1bebe80, Apply@0x1beb830, LateUpdate@0x1beb9e0 | `tto_cat.js` |
| the hero's TTO coroutines moving the prefabs | `Cat.<RPC_crescentEclipse>d__345` (`pseudo/Cat.c:3404`), `Cat.<RPC_anchorYank>d__394` (:660), dropAnchor, royalFlush | as the Sheep's / Penguin's `CODE_MOVERS` | `wardrobe_fx_tto.py` + `tto_cat.js` |
| `shader:Unlit/Texture` | royalFlush_card's `tto_royalFlush_face` (atlas scale (1/6, 1/4)), `tto_royalFlush_backMat` | unlit, texture only, opaque | `api.shader` in `tto_cat.js` |
| `shader:Unlit/Color` | `tto_crescentEclipse_m_edge`, `tto_royalFlush_m_edge`, `tto_royalFlush_rim` | unlit flat `_Color`, opaque | `api.shader` in `tto_cat.js` |
| blend names | dropAnchor_smash / royalFlush_swordHit `tto_Bomb2` (Multiply (Double)), dropAnchor_shrapnel `tto_Default-Particle` (Alpha Blended Premultiply) | today fxMaterial's alpha-blend fallback | `wardrobe_fx_tto.py:141` `SHADER_BLEND` += `"Legacy Shaders/Particles/Multiply (Double)": "multiply2"`, `"Legacy Shaders/Particles/Alpha Blended Premultiply": "premul"` (and `"Legacy Shaders/Particles/Multiply": "multiply"`) |
Built already: GroundHugEmitter, EmblemEmitter, ParticleSystem (shuriken.js: render modes 0 / 1, Velocity / Force /
InheritVelocity / Rotation modules), TrailRendererModern and LineRenderer (`tto_sheep.js`), FlexibleCelShader/Cel No
Outline (`tto_penguin.js`, by blend for any class; its fresnel / rim props are not drawn, `tto_penguin.js:125`; the Cat's
cel materials carry `_FresnelBrightness` 0.15-0.4, `_RimAlpha` 0).

## Interfaces (fixed up front, so the builders run in parallel)

1. **mesh.js Animation with `play` off + `rewind()`** (shaders / mesh owner): built idle (no pose) until `play()`;
   `rewind()` sets the current clip's time to 0 (part 4).
2. **alphatimer.js `fadeOut(sec)`** on its emitter (part 4) and Opaque1 in `OPACITY` (Bison part 2).
3. **legacyParticles' `collide` hook** (lead, index.html; part 5): `this.collide?.(p, world)` after the move, false =
   remove.
4. **mesh.js `shader:Transparent/AdditiveAlpha`** (two passes, `d.cut`) and the extractor's `cut` (part 3).
5. **The Bison's**: UVScroll and the per-renderer shared copy (Interfaces 3 there), `SHURIKEN_FROM_TTO` (Interfaces 6).
6. **Existing, used as they are:** `api.spawn` (+ the entry's `builds`), `fx.emitters`, `fx.nodes`, `api.FX.gen`,
   `api.FX.t` / `fx.cutAt`, the cue's `bone` / `scale` / `kill` / `cut`.

## Rank by value (effects unblocked / effort)

| rank | part | Cat effects it makes right | other classes | work |
|---|---|---|---|---|
| 1 | UVScroll layout + part | `deltaStrike` (unbuildable today) | Bison 2, Whale 1 | 1 + ~25 lines (Bison's) |
| 2 | Cat_grandCasinoArcade + `fx:grandCasinoArcade` | `grandCasinoArcade` (unbuildable today) | 0 | 1 + ~40 lines |
| 3 | Support Fire: Cat_supportFire + barrage + AdditiveAlpha + AlphaTimer Opaque1 / fadeOut + Animation play-off / rewind | `supportFire_fire` (unbuildable), `supportFire_cannon` (invisible), smoke / hit placement | AdditiveAlpha: Mole; AlphaTimer Opaque1: Bison 2 | ~30 + ~45 + ~25 + ~15 + ~10 lines |
| 4 | Shuriken graft entry | `supportFire_hit`'s burst | 10 more BB systems if done natively | 1 line (after the Bison's ~25) |
| 5 | WorldParticleCollider + hook | `luckyDice`, `treasureHunt` | Chameleon 1, Rabbit 2 | ~25 + 2 lines |
| 6 | StatusControl in BUILT | `damagePlus` (fine already) | 0 | 1 line |

After all: `BUILT` in `pipeline/wardrobe_fx_inventory.py` += `UVScroll` (if the Bison's isn't in), `StatusControl`,
`Cat_grandCasinoArcade`, `Cat_supportFire`, `WorldParticleCollider`; `ParticleSystem` / `ParticleSystemRenderer` once
the graft (or the native read) covers every BB system; run it again (the recipe's rule).

## Who builds what (never two owners for one file; as `plans/fx_wolf/build_rules.md`)

| agent | owns | builds |
|---|---|---|
| A: shaders + mesh | `wardrobe/fxparts/mesh.js`, `wardrobe/fxparts/alphatimer.js` | AdditiveAlpha (2 passes, `cut`); Animation built with `play` off + `rewind()`; AlphaTimer `fadeOut(sec)` (+ the Bison's Opaque1 drive if not in) |
| B: cat | `wardrobe/fxparts/cat.js` (new) | Cat_grandCasinoArcade, `fx:grandCasinoArcade`, Cat_supportFire (+ `fireDir`), `fx:supportFire_cannon` |
| C: generic | `wardrobe/fxparts/worldcollider.js` (new), `wardrobe/fxparts/uvscroll.js` (new, if the Bison's isn't built) | WorldParticleCollider; UVScroll (the Bison's spec) |
| D: TTO (with the TTO researcher's report) | `wardrobe/fxparts/tto_cat.js` (new) | the TTO table above |
| lead | `pipeline/wardrobe_fx.py`, `pipeline/wardrobe_fx_tto.py`, `wardrobe/index.html`, `pipeline/wardrobe_fx_inventory.py`, `wardrobe/fx_cues/cat.json` | LAYOUTS; WorldParticleCollider stored; AdditiveAlpha `cut`; `SHURIKEN_FROM_TTO["cat"]`; `SHADER_BLEND` lines; legacyParticles' `collide` hook; `FX_PART_FILES += "cat", "worldcollider", "tto_cat"` (+ `"uvscroll"`); `BUILT`; the rebuild and the cues |

B codes against Interfaces 1-3, so A, B and C run in parallel. Rules as before: `node --check`, no browser for the
builders, never `wardrobe_fx.py cat` without `--probe` (the lead rebuilds once).

## How sure I am

| item | sure | why |
|---|---|---|
| The three byte layouts | high | public fields in declaration order; 8 / 8 / 12 bytes as decoded; values sensible (1, 1; a ref to its own SMR; 30 m/s) |
| Grand Casino's flicker and schedule (fires at age 1.3 + 2.7 k, destroy 14.5) | high | literals; every guard worked by hand; sLv 2 = Bible rank 2; EffectControl life 16 fits the 15.9 s end |
| The cannonball's flight (lands 18-26 m out) | medium-high | Unity's semi-implicit step assumed (`v += g dt; p += v dt`); `getTrajectoryVector`'s guards worked by hand; flat ground at the cannons' height |
| Support Fire's barrage (0.24-0.35 s, random cannon, fade 0.5 s) | high | literals at :41174, :41185, :10603; `AlphaTimer.cs:328-357` |
| 205 / 206 / 207 names | **certain now** | TTO's re-serialised copies name the shaders (Read this first 4) |
| The ParticleSystem's meaning (local, 0.6-1 s, 12 at 0) | high | BB's 3.5 fields and TTO's upgraded copy agree |
| WorldParticleCollider's bounce maths | medium | no game source; the 3.5 manual's wording vs TTO's converter (part 5) |
| damagePlus: 12 s, `mount_Hand_R` | high | `:19723`, `:20077`; chaAdjust at CHA 1 as the Penguin's sum |

## Open questions (each with my recommended answer)

1. **Support Fire's balls land 18-26 m ahead**, outside the page's usual framing. Keep the game's distances? Recommended:
   **yes** (the barrage is the skill; the cannons and muzzle flashes stand at the hero, the explosions are where the game
   puts them; the tile's camera can pull back as the Wolf's long skills do, if the editor finds it empty).
2. **Grand Casino Arcade lasts 15.9 s at max rank** (five spins). The 10 s rule is for long buffs / fields; this is a
   channel of the hero's own clip. Recommended: **play all five spins** (cut at 15.9, the clip's standby), as the game; if
   the editor keeps the 10 s cap, the part plays the spins before the cut and the followState end does the rest.
3. **Support Fire's end.** The game ends it on a move key or when SP < 6 (12 SP per 6 shots, 6 with #404 on: from 100 SP
   that is 96 shots, about 30 s). Recommended: **cut at 10 s** (the standing rule), the cannons then fading 0.5 s.
4. **WorldParticleCollider's bounce**: the whole velocity x 0.5 (the 3.5 manual) or only the bounce off the floor (TTO's
   conversion)? Recommended: **the whole velocity** (the BB component's own semantics; the page draws BB).
5. **BB's Shuriken: TTO graft or a native 3.5 read?** Recommended: **the graft now** (the Bison's design, one table entry,
   proven field-for-field here), and a native read later if a class's BB system has no TTO copy.
6. **damagePlus' life**: 12 s status, cut at 10 by the standing rule. Recommended: **10** (the rule), on `mount_Hand_R`.

## Verification

Checked 2026-11-13 (home PC, read only) against `D:\12tails\DecompiledSource\` (`UVScroll.cs`, `Cat_grandCasinoArcade.cs`,
`Cat_supportFire.cs`, `AlphaTimer.cs`, `Math.cs`, `Cat.cs`, `CharacterControl.cs`), TTO1102's `methods.tsv`, this
report's probe outputs (`probe.txt`, `probe_ps.txt`, `ps_sum.txt`, `tto_probe.json`, `calc.txt`) and the page
(`wardrobe/index.html`, `wardrobe/fxparts/`). My own scripts: `checks/fx_cat_research/verify_tto_parts/traj.py`
(getTrajectoryVector's predicates and the flight).

Confirmed as written:
- **LAYOUTS** (the paste-ready python block): `UVScroll` scroll_x / scroll_y (UVScroll.cs:67, :70; defaults 0.1 :26, :29;
  Update :42-46), `Cat_grandCasinoArcade.mRenderer` (:144; the two other fields private), `Cat_supportFire.mVelocity`
  (:240; the other two private); the probe's bytes and words (probe.txt:147 [1.0, 1.0], :380 [0, 75936], :778 [0, 0, 30],
  :866). The block is correct as it stands.
- Cat_grandCasinoArcade: every opaque predicate re-worked (Awake :30 / :34 / :39 / :46 / :51 / :58 / :62; Update :95 true,
  :99 false, :104 false, :113 true, :116 true): materials [1] and [2], `0.15 sin(4 Time.time)` and `0.15 - num`.
- Grand Casino Arcade's schedule (Cat.cs): effect at 0.4 (Yield 2 :28796, createEffect :27838, Find :27858), case 3 at 1.7
  (Yield 3 :28782), spins while `i < 2 sLv + 1` (:28507) with Play("fire") (:28554) and grandCasino2 at volume 2
  (:28566-28578), Yield 4 = 2 s (:28784), then `i >= 2 sLv` -> Yield 6 = 0.4 (:28303, :28809) else Yield 5 = 0.7 (:28780);
  after the 5th: grandCasinoArcade3 + Play("destroy") (:28513-28531), Yield 7 0.3, Yield 8 0.7, standby. Effect ages:
  fire 1.3 + 2.7 k, destroy 14.5, standby 15.5 (clip 15.9). mesh.js's play() restarts `fire` (2.5 s) at the next spin
  (t >= len, mesh.js:325).
- Support Fire (Cat.cs): six raycasts from `TransformDirection(3i - 10.5, 2, -2)`, i = 1..6 (:41048-41099, :41060),
  cannons `createEffect` at the hit, hero rotation (:41084); `now + 0.25` (:40842), `0.01 x Random.Range(24, 36)`
  (:41174), random cannon (:41185), muzzle `cannon + TransformDirection(0, 1, 3)` (:41207), `getTrajectoryVector(muzzle,
  muzzle + (24 + Range(0, 24)) forward, 30)` (:41212); SP (:41255); Rewind + Play("fire") (:10672-10677); smoke and ball
  at LookRotation(fireDir) (:10711, :10741), Init (:10753); the hit at identity (:10802), 8 m area (:10825); standby
  (:10566) and `BroadcastMessage("AlphaTimerFadeOut", 0.5)` (:10603); AlphaTimerFadeOut's predicates
  (AlphaTimer.cs:337-352: all three zeroed, start now, end now + 0.5). Cat_supportFire's ctor / Init / FixedUpdate
  predicates as described.
- The flight: getTrajectoryVector's 20 predicates take the high-arc tangent and the `y < 0.1` branch as written; my
  recompute gives elevation 2.99 deg (d 24) to 6.41 deg (d 47), as calc.txt. A point from the 1 m muzzle lands 19.2-26.8 m
  out after 0.64-0.90 s; with the box's lowest corner (calc.py) 17.98-26.23 m: "18-26 m ahead of the muzzle" holds.
- WorldParticleCollider's stored fields (probe.txt:566, :848), the PhysicsManager's gravity -9.8 (probe_ps.txt:1501); the
  Shuriken graft's values (ps_sum.txt: startLifetime min key 0.6 x 1, startSize 0.5 x 2 = 1-2, cone type 4 r 0.2 / 25
  deg, cnt0 12 at time0 0, m_BurstCount 1; tto_probe.json: moveWithTransform 0, minScalar 0.6 / 1.0, m_Bursts [{0, 12}],
  `tto_Bomb2` = `shader:Legacy Shaders/Particles/Multiply (Double)`); `SHADER_BLEND` maps only Additive, Additive (Soft),
  Alpha Blended and Diffuse today (wardrobe_fx_tto.py:141-142); `BUILTIN_BLEND` 205 / 206 / 207 (wardrobe_fx.py:46).
- damagePlus: Instantiate at the hero, identity (Cat.cs:20053), parent `mount_Hand_R` (:20077), Init (:20087), one at a
  time (:20045), `chaAdjust(12)` (:19723); damageRoulette's parent and scale (CharacterControl.cs:36258-36273); the
  status-look loads (:9156, :36239, :36406). Delta Strike: hero + 0.5 forward (:37482), scale 1.5 at sLv 2 (:37495).
- Page hooks as cited: mesh.js's Animation `if (!c.play ...) return null` (mesh.js:287), alphatimer.js's OPACITY with no
  Opaque1 (alphatimer.js:27), legacyParticles' move (index.html:4326), the legacy emitter pushed before the node's
  scripts (index.html:3960-3961), shuriken.js's collide (shuriken.js:489), the api.spawn contract (index.html:3783-3790).

Corrections:
1. **Grand Casino Arcade's cue cannot carry a `cut` in "clip time"** (part 2's cue shape `[0.4, "fx",
   "grandCasinoArcade", {"cut": <standby clip time>}]`, 15.9 or the 10 s cut). A cue's cut is compared with `FX.t`
   (index.html:4016, penguin.js:28, bat.js:447), and fxStart sets `FX.t = 0` at every step of a sequence
   (index.html:4605, called by startStep :1374). The effect is spawned in grandCasinoArcade1's step, so its cut is read
   against whichever step is playing: 15.9 is reached only 15.9 s into grandCasinoArcade3's step (its idle tail;
   EffectControl's life 16 has ended it long before), and 10 fires 10 s into grandCasinoArcade2's step (11.7 s,
   mid-spin). Corrected: the cue has no `cut`, and the part ends the effect itself on its own age clock, as it already
   plays `fire` / `destroy`: at age 15.5 (the standby, clip 15.9 - 0.4) set `fx.cutAt = -Infinity`, so the page's
   followState end runs (index.html:4016: age = life, then the 1 s afterLife). The part's "nothing at or after
   `fx.cutAt`" becomes "nothing at or after age 15.5". The schedule needs the SEQ's grandCasinoArcade2 held 13.2 s, not
   today's 13.5 (skills_a.md:29-31), so grandCasinoArcade3 starts at 14.9 = the destroy's age 14.5. skills_a.md:539
   writes the same schedule as a cue key `anims` ([[1.3, "fire"] ... [14.5, "destroy"]]): the lead takes one of the two
   (the part's fixed ages, or `anims` read by the part), not both.
2. **Support Fire's cannon `cut` is in supportFire2's clock**, for the same reason: the cannons are spawned at 0 of
   supportFire1 (1.0 s), and the barrage's "until `api.FX.t >= fx.cutAt`" and the followState end then read
   supportFire2's step time, so C = that step's hold: 3 with today's `supportFire2*@3` (skills_b.md:495-500 has 3), 9 if
   question 3's 10 s cut is taken (`supportFire2*@9`). C must stay above supportFire1's 1.0 s, or the cannons are cut in
   the first step.
3. RVAs in the TTO table: the Cat_eclipseFx coroutines listed are their MoveNext bodies (methods.tsv), but
   Cat_royalCard's `DealRun@0x1beaab0`, `FlipRun@0x1beac30`, `GatherRun@0x1bead40` are the iterator stubs; the bodies are
   `<DealRun>d__27::MoveNext@0x1bed260`, `<FlipRun>d__29@0x1bef0c0`, `<GatherRun>d__34@0x1bef6f0` (and
   `<Pulse>d__31@0x1bf07d0`).
4. The TTO table misses one page gap (tto.md Verification 3): `dropAnchor_anchor`'s `Leash` is the only inactive node,
   its Edge / Pull RingEmitters carry no flag, and `ringEmitter` (index.html:3965, :4086) never reads `active`, so they
   draw from the spawn. The `Cat.DropAnchorFlight` mover holds them back until the landing.
5. Minor: glowTwin is index.html:920-948 (not 915-935); every other line cited checks out.

### Corrected cue shapes (part 2 and part 4; the LAYOUTS block above is unchanged)

```json
[0.4, "fx", "grandCasinoArcade"]
```
(fx:grandCasinoArcade: `fire` at ages 1.3 + 2.7 k, k = 0..4, `destroy` at 14.5, `fx.cutAt = -Infinity` at 15.5; SEQ
`"Grand Casino Arcade: grandCasinoArcade1 grandCasinoArcade2*@13.2 grandCasinoArcade3"`.)

```json
[0, "fx", "supportFire_cannon", {"x": -7.5, "d": -2, "cut": 3}],
[0, "fx", "supportFire_cannon", {"x": -4.5, "d": -2, "cut": 3}],
[0, "fx", "supportFire_cannon", {"x": -1.5, "d": -2, "cut": 3}],
[0, "fx", "supportFire_cannon", {"x": 1.5, "d": -2, "cut": 3}],
[0, "fx", "supportFire_cannon", {"x": 4.5, "d": -2, "cut": 3}],
[0, "fx", "supportFire_cannon", {"x": 7.5, "d": -2, "cut": 3}]
```
(cut = the supportFire2 hold of the SEQ `"Support Fire: supportFire1 supportFire2*@3"`; 9 with `supportFire2*@9` for the
10 s rule; the entry keeps `"builds": ["supportFire_fire", "supportFire_smoke", "supportFire_hit"]`.)
