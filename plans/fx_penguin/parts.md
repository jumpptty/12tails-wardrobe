# Penguin effects: the parts the page cannot draw yet

Research 10/11/2026 (one of the Penguin fx researchers; scope: the missing parts, plus anything the Penguin's prefabs use
that the page draws wrongly). Model: `plans/fx_sheep/parts.md`. Read only. BB `DecompiledSource` and the rip were read
from `C:\Users\Jump\Desktop\12tails`; `wardrobe_fx.py` reads the game data from `D:\12tails` on this PC (its `BIBLE`).
Probes (read only, outputs next to them) in `checks/fx_penguin_research/parts/`:
- `probe.py` -> `probe.txt`: every node, component and material (with its shader: built-in id or the game's shader name)
  of the 48 Penguin effects in `plans/fx_inventory.json`, with the candidate LAYOUTS patched in memory.
- `probe.py <names>` -> `probe3.txt` (the 14 Penguin prefabs the inventory doesn't list), `probe_extra.txt`
  (`nAttack_fire`, `manaMissile_fire`, `absoluteZero`, `meteora`).
- `probe2.py` -> `probe2.txt`, `probe2b.txt`: Rigidbody / Collider / AudioSource fields and every Animation clip (length,
  wrap, what it moves).
- `calc.py` -> `calc.txt`: the tornado's glide, the typhoon's homing, `chaAdjust(6)`, the fade sums.

Nothing in `wardrobe/data` was written; `wardrobe_fx.py` / `wardrobe_fx_tto.py` were never run without `--probe`.
All `Penguin.cs` lines are `C:\Users\Jump\Desktop\12tails\DecompiledSource\Penguin.cs`.

## Read this first

1. **Every layout is proved on the real bytes.** With the LAYOUTS below patched in, all 10 blocked prefabs decode and
   use up exactly their bytes (`probe.txt`; the stock probe's own errors name the sizes: Penguin_tornado / _typhoon 28,
   _arcticEmperor 32, _iceBlock 8). Penguin_cosmicFriday, Penguin_nAttack, Penguin_manaMissile and Penguin_snowMan have
   **0 field bytes** (all their fields are private), so they already extract, but the page draws nothing of what they do.
2. **The inventory misses three effects that need a Penguin script, because they are not `Resources.Load`ed.**
   - `nAttack_fire` (the Normal Attack ball): a prefab field (`public GameObject nAttack_fire`, `Penguin.cs:16437`),
     instantiated by `RPC_nAttack_fire` (`:9672`). It carries **Penguin_nAttack**, like `spreadShot_fire`.
   - `manaMissile_fire` (Mana Missile): a prefab field (`:16500`), instantiated at `:10220`. It carries
     **Penguin_manaMissile** (the mover; not in the inventory at all).
   - `snowMan` (the Snow Man status look): loaded by `CharacterControl.cs:38705`, not by `Penguin.cs`. It carries
     **Penguin_snowMan**, and the code **hides the hero's renderers** while it stands (`CharacterControl.cs:38690-38700`).
   The other prefab-field / status prefabs (`castEffect`, `castRing`, `deadEffect`, `manaMissile_hit`, `nAttack_hit`,
   `cosmicRift`, `focusIntellect`, `frost`, `iceShield`, `snowBall`, `snowBall_break`) use only built parts
   (`probe3.txt`). Tool gap, for later: `wardrobe_fx_inventory.py` only sees `Resources.Load` paths in `<Class>.cs`.
3. **Shaders the page draws wrongly today (the inventory doesn't see shaders).** Penguin materials (`probe.txt`,
   `probe3.txt`):
   | material (effect) | shader | today on the page | needed |
   |---|---|---|---|
   | `arcticEmperor` (arcticEmperor) | game's `Transparent/AdditiveSaturate`, **two passes** | mesh.js warns, fxMaterial alpha-blend at tint alpha 0: invisible | 2-pass material + Penguin_arcticEmperor |
   | `cosmicFriday` (cosmicFriday) | game's `Transparent/Opaque1` | warn, unlit, opacity 2 x tint.a = 0.26 | lit Lambert, `_Color` x 2, opacity `_Color.a` 0.46 |
   | `iceblock` (iceBlock) | game's `Transparent/Opaque2` | warn, unlit, opacity 2 x tint.a = **0.10** | lit Lambert, `_Color` x 2, opacity 0.75, both sides |
   | `snowman` (snowMan) | game's `DiffuseAmbient` | warn, unlit, no depth write | opaque lit Lambert x 2 |
   | `fallingComet1`, `giantComet` (fallingComet, giantComet: the comet bodies) | built-in **206** | `BUILTIN_BLEND` has no 206: silently `add` | Particles/Multiply (Double) (medium sure, below) |
   | `penguin_dead` (deadEffect: the KO tile) | built-in **207** | silently `add` | Particles/Alpha Blended Premultiply (medium) |
   | `nAttack_hit` | game's `Particles/AdditiveOffset` | warn | not needed: the hit lands on the enemy (left out) |

   **207 is every class's `<cls>_dead`** (all 12 `*_dead.mat` in the rip, plus `netherBane` and `fireWall`: 13 materials on 207): the Wolf's and the Sheep's deadEffect,
   already built, are drawn as additive too. Over the white stage that matters (premultiplied darkens by alpha).
   `absoluteZero` (FX/Phoenix + AlphaTimer) and `meteora` (Diffuse) are drawn right already.
4. **How sure the 206 / 207 names are.** Unity 3.5's "unity default resources" ids are not in the game files. The
   extractor's rule (the Particle shader files in alphabetical order from 200) is confirmed one more step by **205**:
   its 24 materials in the rip are `BlackTrail`, `ShadowLine1-4`, `ShadowRay_0`, `ShadowRing1`, `Dust10/11` ..., and
   `BlackTrail.png` is a dark trail on a white, opaque background: only a multiply makes sense, and "Particle Multiply"
   is the 6th file (Add, AddMultiply, AddSmooth, Alpha Blend, Blend, **Multiply**, MultiplyDouble, Premultiply Blend,
   VertexLit Blended). So 206 = **Multiply (Double)**, 207 = **Alpha Blended Premultiply**. Counter-evidence: 3 of the 15
   materials on 206 (`Bomb1_m`, `Bomb4`, `Smoke4`) keep an `_EmisColor` (VertexLit Blended's property), but Unity 3.5
   keeps old properties when a shader is switched. Medium; check with a screenshot of `fallingComet` after the build.
5. **Two looping sounds start at volume 0 and the page leaves them there.** `tornado1-3` and `typhoon1-3` play
   `sounds/cyclone` with `m_Volume 0`, loop on (`probe2.txt`); the scripts raise it in FixedUpdate (below). Without a
   volume hook the page plays the loop silent. Needs `Sound.play`'s handle to take a new volume (lead, `index.html`).
6. **Spawned at the world's rotation, moved along the hero's.** tornado / typhoon are instantiated with
   `Quaternion.identity` (`:10909`, `:10948`, `:10987`; `:11182`, `:11221`, `:11260`) but pushed along
   `owner.transform.forward` (`Penguin_tornado.cs:98`, `Penguin_typhoon.cs:848`). The funnel is round, so the spawn
   rotation is invisible; the parts use the hero's forward (the mirror group's +z), whatever the cue's `rot`.
7. **Game quirks (offer to the user for the Bible; none changes a cue).**
   - The typhoon's first push is `rotateH(5 x forward, (tID - 1) x 120)` (`Penguin_typhoon.cs:848`): its starting
     swerve depends on the **target's Photon actor number** (0, 120 or 240 degrees). Question 2.
   - `RPC_cosmicFriday`'s load failure says "Cannot find cosmicFriday_ring Effect" for the `cosmicFriday` prefab too
     (`Penguin.cs:39288`, a copy-paste).
   - Staff of Time (`w_pgn59`) turns the Normal Attack ball (and Spread Shot's) into a 0.01 m/s, 12 s, 3 m mine
     (`Penguin_nAttack.cs:115-145`); the Bible has it (`penguin-skill-reference.md:206`). Question 1.
8. **Name collisions: none that bites.** Every sound these effects play is in `sounds/` only: `cyclone`,
   `arcticEmperor`, `cosmicFriday`, `iceBlock`, `nAttack`, `snowMan` (the snowMan prefab's own AudioSource; `voices/` has `snowman1-2`) (`probe2.txt`; the rip's `penguin/sounds/`). `voices/` has
   `arcticEmperor1-2`, `cosmicFriday1-2`, `iceBlock1-2`, `nAttack1-3`, `tornado1-2`, `typhoon1-2`, `spreadShot1-2`:
   different names, so the kinds stay apart. Watch: the **effects** `tornado1` / `tornado2` / `typhoon1` / `typhoon2`
   share their names with the **voices** `tornado1` / `tornado2` / `typhoon1` / `typhoon2`. Cue kinds keep them apart
   (`"fx"` reads `fx.json`, `"voice"` reads `v_<name>.mp3`).
9. **SEQ: nothing in my scope.** The Penguin SEQ (`index.html:1027-1028`) has no tornado / typhoon / iceBlock entry;
   their clips are the cast ones (`cast_b.md`'s scope). The parts below take their end from the cue (`cut`), so they fit
   whatever the cast_b report decides.

## The Penguin's blocked set (inventory + the three it misses)

"Where" is where BB spawns it; "Enemy" is left out by the decisions.

| effect | skill (spawn) | missing part(s) | where |
|---|---|---|---|
| `tornado3` (`tornado1`, `tornado2` lower ranks) | Tornado, max rank sLv 3 (`RPC_tornado_fire` `:10832`, Instantiate `:10987`, Init `:11032`) | Penguin_tornado | `getSpawnPos(hero + (1 + sLv) x forward)` = **4 m ahead** at sLv 3 (`:32804`) |
| `typhoon3` (`typhoon1`, `typhoon2`) | Typhoon (`RPC_typhoon_fire` `:11137`, Instantiate `:11260`, Init `:11311`) | Penguin_typhoon | **4 m ahead** (`:33353`); then homes on the target (10 m point) |
| `arcticEmperor` | Arctic Emperor (Instantiate `:35054` at the hero, hero rotation) | Penguin_arcticEmperor + AdditiveSaturate | hero |
| `cosmicFriday` | Cosmic Friday (Instantiate `:39268` at the hero, hero rotation; `SendMessage("InitCosmicFriday")` `:39279`) | Penguin_cosmicFriday + Opaque1 | hero (follows her) |
| `iceBlock` | Ice Block (`RPC_iceBlock_fire`, Instantiate `:10726` at `mPos`, `LookRotation(tDir)`; Init `:10744`) | Penguin_iceBlock + Opaque2 | `mPos` (cast_b's) |
| `spreadShot_fire` (x3) | Spread Shot (`RPC_spreadShot_fire` `:11472`; 3 balls at `firePos + 0.3 i x right`, yaw `15 i`, i = -1..1, `:11518-11520`) | Penguin_nAttack | hero (`firePos`) |
| `nAttack_fire` | Normal Attack (`RPC_nAttack_fire` `:9665`, Instantiate `:9672`) | Penguin_nAttack | hero (`firePos`) |
| `manaMissile_fire` (xN) | Mana Missile (Instantiate `:10220`, `lhs x Euler(-0.2 abs(a), a, 0)`, Init `:10245`) | Penguin_manaMissile | hero (`firePos`), homing on the target |
| `snowMan` | Snow Man status (`CharacterControl.cs:38705`, at the snowmanned character, `Quaternion.identity`; Init `:38711`) | Penguin_snowMan + DiffuseAmbient + hide the hero | the snowmanned one (self-cast: the hero) |
| `fallingComet`, `giantComet` | Falling Comets (`:26881`, `:37615`) | (ready; material 206) | cast_a's |
| `deadEffect` | KO tile (decision 11) | (ready; material 207) | hero |

## LAYOUTS (paste into `pipeline/wardrobe_fx.py`, after the Sheep's block)

```python
# the Penguin's parts (plans/fx_penguin/parts.md, 2026-11-10): every Penguin_tornado / _typhoon (3 each), the
# arcticEmperor and the iceBlock decode and use up exactly their bytes; the other Penguin scripts keep every field
# private (0 field bytes)
LAYOUTS.update({
    # Penguin_tornado.cs:605, :635, :638 / Penguin_typhoon.cs:515, :557, :560 (28 bytes): mLv = the hit radius (m) and
    # the steering force 11 - mLv; nPosition / nVelocity = the owner's network copy (0 in the prefab)
    "Penguin_tornado": [("mLv", "i"), ("nPosition", "v3"), ("nVelocity", "v3")],
    "Penguin_typhoon": [("mLv", "i"), ("nPosition", "v3"), ("nVelocity", "v3")],
    # Penguin_arcticEmperor.cs:225-246 (32 bytes): AlphaTimer's fade on _TintColor.a plus a second one on _Emission.a
    "Penguin_arcticEmperor": [("MinAlpha", "f"), ("MaxAlpha", "f"), ("MinEmission", "f"), ("MaxEmission", "f"),
                              ("FadeDelay", "f"), ("FadeEaseIn", "f"), ("FadeMiddle", "f"), ("FadeEaseOut", "f")],
    "Penguin_iceBlock": [("mLife", "i"), ("mLv", "i")],     # Penguin_iceBlock.cs:264, :267 (8 bytes); Init overwrites both
    "Penguin_cosmicFriday": [], "Penguin_nAttack": [], "Penguin_manaMissile": [], "Penguin_snowMan": [],
})
```

And one line in `BUILTIN_BLEND` (`wardrobe_fx.py:37`), with the comment's evidence (Read this first 4):
`206: "multiply2", 207: "premul"` (205 `"multiply"` too if a later class needs it; no Penguin material uses it).

Values (`probe.txt`): tornado1 / 2 / 3 `mLv` 1 / 2 / 3; typhoon1 / 2 / 3 `mLv` 1 / 2 / 3; `nPosition` / `nVelocity` 0
everywhere; iceBlock `mLife` 12, `mLv` 1; arcticEmperor 0, 0.25, 0, 0.035, 0, 0.3, 7.7, 1.0.

## Each part

Page parts plug in as the comment above `FX_PART_FILES` says (`index.html:3050-3065`): `wardrobe/fxparts/<file>.js`
default-exports `register(api)` and calls `api.part(type, build)`; `build(fx, node, comp, mat, nodeDef, data)` returns
`{ node, update(dt, cam) (return "destroy" to remove the node), stop?() }` or null. The model is `fxparts/sheep.js`.
`node.userData.fxAnim.play(name, fade)` switches a clip (`mesh.js:145-190`); `fx.cutAt` is the cue's `cut` in clip
time, compared with `api.FX.t` (Interfaces 4); `fx.at.to` is the cue's target point (`tto_sheep.js:24`).

### 1. Penguin_tornado: `tornado1` / `tornado2` / `tornado3`

**What it does in BB (`Penguin_tornado.cs`).**
- `Init(owner, dmg, ice)` (:42-187), called in the spawn frame (`Penguin.cs:11032`; `ice = hasSkill(443)`, :11029,
  passive ON: only the speed cap and a frost roll change, nothing drawn):
  - `rigidbody.velocity = 5 x owner.transform.forward` (:98), `rigidbody.drag = 2` (:103);
  - ignores every Player / Enemy / NPC collider (:108-145); locks the owner's camera on it (:152-168, not on the page);
  - starts `onCreate` (:174) and sets itself active (:179).
- `onCreate` (:724-778): `animation.Play("create")`, `wrapMode = Once` (:768-771), `Yield(2, 0.4)` (:778), then
  `Play("root")`, `wrapMode = Loop` (:744-749) unless already dying.
- Update (:199-397): while active, ends itself (`onDestroy`, :391) once the owner's `actionState != "attack"` or
  `myCommand != "tornado"` (:225-231); else every 0.35 s (:248-256) hits everything within `mLv` m (:266-311, the
  `tornado_hit` effects land on the enemies: out).
- FixedUpdate (:409-560):
  - volume `+= Time.deltaTime`, clamped 0..1, while alive (:428); `-= Time.deltaTime` while dying (:442);
  - the owner steers it with the movement keys, `AddForce((11 - mLv) x input)` (:460-472), speed capped 40 (ice) / 30
    (:478-515), pulled back past 30 m (:522-531). **No input on the page: no force**, so it glides and stops.
- `onDestroy` (:884-940): `Play("destroy")`, `wrapMode = Once` (:925-931), `Yield(2, 0.4)` (:940), `Destroy` (:898).
- Also ended from outside: a new Tornado destroys the old at once (`Penguin.cs:10839-10845`); `RPC_tornado_destroy`
  starts `onDestroy` (`:11072-11106`).

**Physics (`probe2.txt`).** Rigidbody mass 1, drag 0 in the prefab (Init sets 2), gravity on, rotation frozen
(`m_Constraints 112`); CapsuleCollider r 1, h 3, centre y 1.5: its bottom is at the root, so on flat ground gravity does
nothing. Glide (`calc.txt`, step by step, 50 steps/s, `v *= 1 - 2 x 0.02 = 0.96` each step):
1. v(t) = 5 x 0.96^(50 t) m/s;
2. x(t) = 0.1 x 0.96 / 0.04 x (1 - 0.96^(50 t)) = **2.4 x (1 - 0.96^(50 t)) m**;
3. 1.34 m at 0.4 s, 2.09 m at 1 s, 2.36 m at 2 s; the limit is **2.4 m** (exp form: 5 / 2 = 2.5 m, 4 % off).

**The clips (`probe2.txt`), on the skinned funnel (nodes 4-6).** `create` 0.4 s: the funnel grows from scale 0.2 to 1;
`root` 0.833 s: the spin; `destroy` 0.4 s: it shoots up (z 0.05 -> 6 in its own frame) and squashes to (0.1, 2, 2).
The Animation component's default clip is `root`, wrap 2 (Loop), playing by itself; clips' own wrap 0, so the
component's wrap decides (`mesh.js:159`). Unity's script sets `wrapMode = Once` right after `Play("create")`.

**Draws anything?** No: it moves the root and switches clips. Everything drawn (SkinnedMeshRenderer, two legacy emitters,
a RingEmitter, all `addsoft`) is built.

**The page part (in `fxparts/penguin.js`, about 35 lines).**
- First update: `node.userData.fxAnim.play("create", 0, 1)` (needs the `wrap` argument, Interfaces), look up the loop:
  `fx.loops.find(l => l.node === node)?.h` (the AudioSource comp comes after this one in `comps`, so not at build time).
- Each frame, own clock `t`: velocity `v *= (1 - 2 dt)` (or `0.96^(50 dt)`), `node.position.z += v dt` (mirror space +z
  = the hero's forward); volume `min(1, t)` via the handle's `setVolume`.
- At `t >= 0.4`: `fxAnim.play("root", 0, 2)`.
- At the cut (`fx.cutAt`, Interfaces; none = never, as the game with the key held): `play("destroy", 0, 1)`, volume
  falls 1/s; 0.4 s later return `"destroy"` (the root goes: the effect is disposed, its loop stopped).
- The cue (cast_b's): `[t, "fx", "tornado3", {"d": 4, "cut": <clip time the channel ends>}]`.

### 2. Penguin_typhoon: `typhoon1` / `typhoon2` / `typhoon3`

**What it does in BB (`Penguin_typhoon.cs`).**
- `Init(owner, dmg, hp, life, tID, ice)` is a coroutine (:712-927), started in the spawn frame (`Penguin.cs:11311`):
  - `life = chaAdjust(6)` (`:11305`) = **6 s** at the page's CHA 1 / LCK 1 (`calc.txt`: `CharacterControl.cs:20593`,
    `num = clamp(1 + Random.Range(0, ceil(0.2)), 1, 512) = 1`, `(int)(6 x 1.015) = 6`); end time = now + 6 (:772);
  - `hp = talAdjust(300)` = 306 (`:11302`, TAL 1), lowered by the damage it deals (:205);
  - the target: `PhotonClient.ActorNrList[tID]` (:830-837), the cast's target;
  - `velocity = rotateH(5 x owner.forward, (tID - 1) x 120)` (:848), `drag = 2` (:853);
  - `Play("create")`, `wrapMode = Once` (:902-907), `Yield(2, 0.4)` (:927); case 2: `Play("root")`, `wrapMode = Loop`
    (:733-738), active (:744).
- FixedUpdate (:307-475), from the spawn (before active too): `AddForce((11 - mLv) x flat direction to the target)`
  (:356-372) = **8 N on 1 kg** at mLv 3; caps 40 / 30 (:379-416); pulled back past 30 m (:423-436). Volume `+= dt`
  clamped **0..0.6** while active (:330), `-= dt` while dying (:472).
- Update (:49-295), while active: hits within `mLv` m every 0.35 s (:110-245, on the enemy: out); destroys itself
  (`RPC_typhoon_destroy` -> `onDestroy`, :270-287, `Penguin.cs:11360-11378`) when the target is gone, the 6 s are up
  (`end >= Time.time`, :81), the owner is down (:87) or its hp < 0 (:93).
- `onDestroy` (:1067-1126): `Play("destroy")` Once, `Yield(2, 0.4)`, `Destroy` (:1081).

**Motion with the 10 m target point (`calc.txt`).** Start 4 m ahead; force 8 m/s^2 toward the point; drag 2:
terminal speed 0.96 x 8 x 0.02 / 0.04 = **3.84 m/s**. Straight start (0 degrees): within 3 m of the point at 0.68 s;
120 / 240 degrees: it swings out and is within 3 m at 1.64 s. All three settle on the point and sit there until 6 s.
- End: 6 s, then the 0.4 s `destroy` clip: gone at **6.4 s**. Its hp would end it sooner against a real foe
  (306 / 30 per hit = 11 hits, 3.85 s of contact); that needs an attacker's defence, so the page keeps the 6 s.

**Same prefab parts as the tornado** minus the two particle emitters (`probe.txt`): skinned funnel, RingEmitter, loop.

**The page part (in `fxparts/penguin.js`, about 40 lines, sharing the tornado's clip / volume code).**
- Start velocity: `(-5 sin a, 0, 5 cos a)` for `a` = `(tID - 1) x 120` degrees (`Math.cs:840-841`: rotateH turns the
  other way from Unity's yaw); `a` from question 2 (default: one of 0 / 120 / 240 at random per spawn).
- Each frame: `v += 8 x flat(target - pos).normalize() x dt`, then `v *= (1 - 2 dt)`, `pos += v dt`. Target =
  `fx.at.to` (Unity space, `tto_sheep.js:24`) or (0, 0, 10) when the cue has none.
- Volume: 0 until 0.4 s, then `min(0.6, t - 0.4)`; while dying `-1/s`.
- `t >= 0.4`: `play("root", 0, 2)`; `t >= 6` (or the cue's `cut`, if earlier: Typhoon has no channel check, so normally
  none): `play("destroy", 0, 1)`, `"destroy"` 0.4 s later.
- The cue (cast_b's): `[t, "fx", "typhoon3", {"d": 4, "to": [0, 0, 10]}]`.

### 3. Penguin_arcticEmperor + the AdditiveSaturate material: `arcticEmperor`

**What it does in BB (`Penguin_arcticEmperor.cs`).**
- Start (:41-62): the phase ends from the spawn: `d = FadeDelay` (:51), `i = d + FadeEaseIn` (:54), `m = i +
  FadeMiddle` (:57), `o = m + FadeEaseOut` (:60).
- Update (:74-200), the AlphaTimer pattern twice: `d > t` Min (:87-98); `i > t` lerp Min -> Max (:104-115); `m > t` Max
  (:121-132); `o > t` lerp Max -> Min (:138-149); `t > o` Min (:155-166). Then `renderer.material`'s `_TintColor.a = a`
  (:175-181) and `_Emission.a = a2` (:184-190). Strict tests, no repeat, no destroy.
- Its values: alpha 0 -> **0.25**, emission 0 -> **0.035**; phases 0 / 0.3 / 8.0 / 9.0 s (0 + 0.3 = 0.3; 0.3 + 7.7 =
  8.0; 8.0 + 1.0 = 9.0). EffectControl life 9 + afterLife 2; ShatterMesh breaks the statue at 8 s over 1 s
  (`probe.txt`): the fade-out and the shatter run together.

**The shader (`Assets/Resources/gameassets/shader/AdditiveSaturate.shader:1-45`).** Two passes, both ZWrite Off, Cull Off,
AlphaTest Greater 0.01, ColorMask RGB:
- Pass 1 (:9-26), `Blend SrcAlpha OneMinusSrcAlpha`: `constant(_TintColor) x vertex colour`, then `x texture double`
  (:24-25): colour = 2 x tint.rgb x vcol x tex, alpha = tint.a x vcol.a x tex.a, doubled too by the page's convention
  for its particle shaders (`fxMaterial`'s `2 x tint`, `index.html:3104-3113`).
- Pass 2 (:27-43), `Blend SrcAlpha One` (additive): `constant(_Emission) x previous double` (:42), and in a pass's first
  stage `previous` is the vertex colour: **no texture**, the whole statue's shape glows by 2 x emission.rgb x vcol, at
  alpha 2 x emission.a.
- Saved (`probe.txt`): tint (0.32, 0.39, 0.58, **0**), emission (0.43, 0.61, 0.75, 0.035), vertex colours present
  (1,225 verts). So without the part the statue is invisible (tint alpha 0), as the game ships it.
- Also used by Wolf `Wolf_heartRing` and `ShadowPortal_0` (the rip's `.mat` files by the shader's GUID): none cued.

**The page.**
- mesh.js `material()`: `"shader:Transparent/AdditiveSaturate"` -> two `MeshBasicMaterial`s, both `vertexColors`,
  `transparent`, `depthWrite: false`, `DoubleSide`, `alphaTest 0.01`:
  - pass 1: `map`, `color = 2 x tint.rgb` (sRGB), `opacity = min(1, 2 x tint.a)`, normal blending;
  - pass 2: no map, `color = 2 x emission.rgb`, `opacity = min(1, 2 x emission.a)`, `CustomBlending` SrcAlpha / One
    (plus the canvas-alpha line `fxMaterial` uses for its additive ones, `index.html:3110-3111`).
  Return both (a list), and `withMaterials` gives each its own group over the **same** index range, pass 1 first.
  ShatterMesh (`mesh.js:237`) keeps only `material[0]` after the shatter: keep both groups there
  (`g.addGroup(0, n, 0); g.addGroup(0, n, 1)`).
- Part `Penguin_arcticEmperor` (penguin.js, about 25 lines): first update, find `node.children` mesh, clone both
  materials (Unity's `renderer.material` is one per-renderer copy driving both passes; copy `onBeforeCompile` as
  `alphatimer.js` does), then each frame pass 1 `opacity = min(1, 2a)`, pass 2 `opacity = min(1, 2 a2)`.
- APPROXIMATED: whether "double" doubles alpha too (the page's particle convention says yes); fog off.

### 4. Penguin_cosmicFriday + Opaque1: `cosmicFriday`

**What it does in BB (`Penguin_cosmicFriday.cs`).**
- `InitCosmicFriday(ownerID)` (a coroutine; `SendMessage` starts it in the spawn frame, `Penguin.cs:39279`):
  owner from the id (:358-385), `Play("create")`, `wrapMode Once` (:391-394), `Yield(2, 0.5)` (:406); case 2:
  `Play("root")`, `wrapMode Loop` (:330-335), active (:340).
- Update (:31-93), active only: `transform.position = owner.position` each frame (:60: it follows her), and once her
  `actionState != "attack"` or `myCommand != "cosmicFriday"` (:72-78) -> `DestroyCosmicFriday` (:87).
- `DestroyCosmicFriday` (:515-580): `CrossFade("destroy", 0.2)`, `wrapMode Once` (:566-569), `Yield(2, 0.5)` (:580),
  `Destroy` (:529). The hero's coroutine also sends it (`Penguin.cs:39464-39470`).
- OnTriggerEnter (:99-170): an ally entering its 3 m trigger gets the `cosmicFriday` status (logic only).
- No EffectControl: it lives until destroyed. Its AudioSource `cosmicFriday` loops (vol 1): the page already loops it
  until the effect is disposed (`index.html:3163-3165`).

**The clips (`probe2.txt`).** `create` 0.5 s (wrap 1): the disc grows 1 -> 6 and turns 45 degrees; `root` 9.03 s (wrap
2): the slow turn at scale 6; `destroy` 0.5 s (wrap 1): back to 1. Default clip `create`, playing by itself: right from
the spawn.

**The page part (penguin.js, about 15 lines).** `t >= 0.5`: `fxAnim.play("root")`; at the cut: `fxAnim.play("destroy",
0.2)` and `"destroy"` 0.5 s later. Following: the hero doesn't move, nothing to do. The cue's `cut` = the clip time she
leaves `attack` (cast_b's; the SEQ's `cosmicFriday*@6` hold).

**Opaque1 (`shader/Opaque1.shader:1-32`).** Lit (`Ambient` / `Diffuse [_Color]`), `combine primary x texture double,
primary alpha x texture alpha` (:18, :28). Pass 1 (:9-19): ZWrite Off, `AlphaTest GEqual 0.95`; pass 2 (:20-29): ZWrite on,
Cull Back (defaults), alpha blend. `_Color.a` = 0.46 here, so pass 1 never passes: only pass 2 draws. Page: as mesh.js's
`phoenix()` without emission: `MeshLambertMaterial`, `color = 2 x _Color.rgb`, `map`, `transparent`, `opacity =
_Color.a`, `depthWrite` true, `FrontSide`. (Also Bison `earthSmasher`, `massStun`, Cat `supportFire_cannon` with an
AlphaTimer on `_Color`: `alphatimer.js` will need `"shader:Transparent/Opaque1": a => a` then, not now.)

### 5. Penguin_iceBlock + Opaque2: `iceBlock`

**What it does in BB (`Penguin_iceBlock.cs`).**
- `Init(life, lv, owner)` (:44-97), in the spawn frame (`Penguin.cs:10744`): `mLife = (int)(life + Time.time)` (:51)
  with `life = chaAdjust(6) + 6` = **12 s** (`Penguin.cs:10744`, `calc.txt`); the first ice tick 1.1-1.9 s later (:84).
- Update (:101-230): destroys the block once `mLife < Time.time` (:116-120), the owner is gone (:127-131) or down
  (:138-142); else every 1 s gives foes within `6 + 3 lv` m the `ice` status (:157-211, logic only).
- Note `mLife` is an **int** of the absolute time, so the block lives 12 s minus the fraction of `Time.time`: 11-12 s.
  The page uses 12 (the spawn at a whole second).
- No EffectControl. Its clip `root` (0.6 s, Once): the block drops from 4 m to 0.5 m (`probe2.txt`). MeshCollider: a wall
  (logic only).

**The page part (penguin.js, 3 lines).** Own clock; return `"destroy"` when `t > 12`.

**Opaque2 (`shader/Opaque2.shader:1-34`).** Same lit combine as Opaque1. Pass 1 (:8-18): ZWrite on, `AlphaTest GEqual
0.95`; pass 2 (:19-31): ZWrite Off, **Cull Off**, `AlphaTest Less 0.95`. `_Color.a` = 0.75, so only pass 2 draws. Page:
Lambert, `color = 2 x (0.56, 0.98, 1.0)`, `map`, `opacity 0.75`, `depthWrite: false`, `DoubleSide`.

### 6. Penguin_nAttack: `nAttack_fire`, `spreadShot_fire`

**What it does in BB (`Penguin_nAttack.cs`).**
- Constructor: its own life `1.4` s (:25). (The hero's code also sets `ProjectileControl.life = 1.4 x rangeMod`,
  `Penguin.cs:9681`, `:11535`; Penguin_nAttack counts its own: FixedUpdate `life -= dt`, Destroy at 0, :44-53.)
- `Init(owner, ownerID)` (:65-145): damage 0.5 x ATK (:97), layer 1 (:100), `velocity = TransformDirection(0, 0, 14)`
  (:103): **14 m/s** along its spawn rotation. With **Staff of Time** (`weapon == "w_pgn59"`, :115): damage x 0.75 (:121),
  life **12 s** (:124), velocity **0.01** m/s (:127), trigger radius 3 (:139), a mine flag (:145).
- OnTriggerEnter (:168-381): a hit on a foe destroys it and asks for `RPC_nAttack_hit` at the contact (:229-272, on the
  enemy: out); the mine flag changes which layers count (:196-202).
- Physics (`probe2b.txt`): no gravity, drag 0, rotation frozen, trigger sphere r 0.35.

**The page part (penguin.js, about 15 lines, or reuse `sheep.js`'s `mover` shape).** Velocity `(0, 0, 14)` turned by
`fx.uQuat(node)` at the spawn; life 1.4 s; ends when the centre reaches the floor going down (the Sheep's decision 3
analogue: the ball meets the ground at the 10 m target point). Staff of Time (question 1): `(0, 0, 0.01)`, life 12 s,
no floor end. The worn weapon is `api.hero().state.R === "specialScepter"` (`item_map.json` penguin/weapon/w_pgn59 =
`specialScepter`, the only code with that model).

### 7. Penguin_manaMissile: `manaMissile_fire`

**What it does in BB (`Penguin_manaMissile.cs`).** Its own speed `(0, 0, 12)` (:26). Awake: layer 1, `velocity =
TransformDirection(0, 0, 12)` (:45-51). `Init(target, dmg)` (:63-79). FixedUpdate (:91-134): clock `+= dt`, Destroy at
`ProjectileControl.life` (:98-107) = `3 x rangeMod` = **3 s** (`Penguin.cs:10235`); with a target, every 0.1 s
(:119-125) `forward = RotateTowards(forward, target.collider.bounds.center - pos, 0.15 rad, 1)` (:128), turn to it,
velocity = forward x 12 (:131-134). A trigger hit on a foe destroys it (:211) and asks for `manaMissile_hit` there (out).
Physics: no gravity, trigger sphere r 0.3 (`probe2b.txt`).

**The page part (penguin.js, about 20 lines).** As Sheep_homingLight, but **homing on the target point** (the decisions
give the target a place, 10 m ahead): `fx.at.to` or (0, 1, 10) = the target's bounds centre (the Penguin-size body:
CharacterController h 1, centre y 0.6 in `Penguin.prefab:677-689`; use the cue's `to`). Every 0.1 s rotate the velocity
toward it by at most 0.15 rad; end when within 0.3 m + the target's radius (0.3) of it, or at 3 s. The fan
(`Euler(-0.2 |a|, a, 0)`, `Penguin.cs:10220`) is the cue's `rot` per missile (cast_a's).

### 8. Penguin_snowMan + DiffuseAmbient + hiding the hero: `snowMan`

**What it does in BB.** `CharacterControl.cs:38690-38711`: on the `snowMan` status the character's renderers are all
switched off (:38692), `snowMan` is instantiated at its position, `Quaternion.identity`, and `Init(owner)`.
`Penguin_snowMan.cs`: Init (:20-79) turns it to the owner's rotation (:45) and, when the owner's collider is taller than
1 m, scales it by that height (:48-63; the Penguin's CharacterController is h 1, so scale 1); Update (:82-135) follows the
owner (:116) while her `actionState == "snowMan"` (:110), else destroys itself (:124-129). Its clip `root` (1 s, loop)
wobbles the snowman (`probe2b.txt`).

**The page part (penguin.js, about 15 lines).** Hide the hero's meshes (`api.hero().root`, its outfit and props) from the
spawn; at the cut return `"destroy"` and show them again; also show them again in `dispose()` (Interfaces: the page must
call it), so a new pick never leaves the hero hidden. Question 3.

**DiffuseAmbient (`shader/diffuseambient.shader:1-19`).** Opaque, lit (`Ambient [_Ambient]`, `Diffuse [_Color]`),
`primary x texture double`. Page: like `opaque` in mesh.js but `color = 2 x _Color` (white here); `_Ambient` isn't
extracted (default white). APPROXIMATED: the game's own lights.

### 9. Built-in 206 / 207 (the lead's, in `fxMaterial`: both mesh.js and the emitters route there)

- **206 Multiply (Double)** (Unity's `Particle MultiplyDouble.shader`): `Blend DstColor SrcColor` (= 2 x src x dst),
  colour = lerp(0.5, texture x vertex colour, texture alpha); ZWrite Off, Cull Off. On the transparent canvas the plain
  multiply has nothing to multiply (empty canvas = 0): use mesh.js glass's trick (`mesh.js:27-39`, multiply rgb, alpha
  from the luminance), APPROXIMATED the same way. Used by `fallingComet1` (SkinnedMesh comet in `fallingComet`) and
  `giantComet`.
- **207 Alpha Blended Premultiply**: `Blend One OneMinusSrcAlpha`, colour = texture x vertex colour x vertex alpha.
  Page: `premultipliedAlpha` on, normal blending. Used by every class's deadEffect (`penguin_dead` here).
- Medium sure (Read this first 4): check `fallingComet` and the KO tile by eye after the rebuild.

## Interfaces (fixed up front, so the builders run in parallel)

1. **`mesh.js` Animation `play(name, fade = 0, wrap)`**: a third argument overrides the wrap mode (Unity's
   `animation.wrapMode = ...` right after `Play`, as every Penguin script does). Needed by the tornado / typhoon, whose
   clips carry wrap 0 under a Loop component: without it `create` would loop for a frame past 0.4 s and pop.
2. **`Sound.play` handle `setVolume(v)`** (lead, `index.html:3033-3043`): keep `h.vol`, set the gain at start from it,
   and `setVolume` writes `g.gain.value` once started. Parts reach it as `fx.loops.find(l => l.node === node)?.h`.
3. **`Fx.dispose` calls `e.dispose?.()` on every emitter** (lead, `index.html:3227`): the snowman's "show the hero
   again", and the arcticEmperor / AlphaTimer clones could use it.
4. **The cue's `cut` for a part**: `fx.cutAt` is in clip time (set at `index.html:3526`). A part compares
   `api.FX.t >= fx.cutAt` (`FX` is already in the api, `index.html:3070-3071`), as EffectControl's followState does
   (`index.html:3199`). No page change.
5. Materials: mesh.js `material()` may return a list for one name (AdditiveSaturate's two passes); `withMaterials`
   and ShatterMesh take a list.

## Rank by value (effects unblocked / effort)

| rank | part | Penguin effects it makes right | other classes | work |
|---|---|---|---|---|
| 1 | Penguin_nAttack | `nAttack_fire` (every Normal Attack), `spreadShot_fire` | 0 | ~15 lines |
| 2 | Penguin_tornado + Penguin_typhoon (+ `play` wrap, `setVolume`) | 6 (tornado1-3, typhoon1-3) | 0 | ~60 lines + 2 + 4 |
| 3 | Penguin_arcticEmperor + AdditiveSaturate | `arcticEmperor` | (Wolf heartRing, not cued) | ~25 + ~25 lines |
| 4 | Opaque1 / Opaque2 + Penguin_cosmicFriday / Penguin_iceBlock | `cosmicFriday`, `iceBlock` | Opaque1: bison 2, cat 1; Opaque2: rabbit pots | ~20 + ~20 lines |
| 5 | Penguin_manaMissile | `manaMissile_fire` | 0 | ~20 lines |
| 6 | 206 / 207 in `fxMaterial` + `BUILTIN_BLEND` | `fallingComet`, `giantComet`, `deadEffect` | **every class's deadEffect**, 13 more 206 materials | ~20 lines |
| 7 | Penguin_snowMan + DiffuseAmbient + `dispose` | `snowMan` | 0 | ~15 + ~8 lines |

After all, add to `BUILT` in `pipeline/wardrobe_fx_inventory.py`: `Penguin_tornado`, `Penguin_typhoon`,
`Penguin_arcticEmperor`, `Penguin_cosmicFriday`, `Penguin_iceBlock`, `Penguin_nAttack`, `Penguin_manaMissile`,
`Penguin_snowMan`; run it again (the recipe's rule).

## Who builds what (never two owners for one file; as `plans/fx_wolf/build_rules.md`)

| agent | owns | builds |
|---|---|---|
| A: shaders | `wardrobe/fxparts/mesh.js` | AdditiveSaturate (2 passes, a material list, `withMaterials` + ShatterMesh keeping both), Opaque1, Opaque2, DiffuseAmbient in `material()`; Animation `play(name, fade, wrap)` |
| B: penguin | `wardrobe/fxparts/penguin.js` (new) | Penguin_tornado, Penguin_typhoon, Penguin_arcticEmperor, Penguin_cosmicFriday, Penguin_iceBlock, Penguin_nAttack, Penguin_manaMissile, Penguin_snowMan |
| lead | `pipeline/wardrobe_fx.py`, `wardrobe/index.html`, `pipeline/wardrobe_fx_inventory.py`, `wardrobe/fx_cues/penguin.json` | LAYOUTS block; `BUILTIN_BLEND` 206 / 207 and their `fxMaterial` cases; `FX_PART_FILES += "penguin"`; `Sound.play` `setVolume`; `Fx.dispose` -> `e.dispose?.()`; `BUILT`; the rebuild and the cues |

B codes against the interfaces above, so A and B run in parallel. The TTO parts (`plans/fx_penguin/tto.md` section 6,
P1-P8) are a separate builder set and touch other files (`tto_sheep.js`-style module, `shuriken.js`,
`wardrobe_fx_tto.py`); `shuriken.js` and `wardrobe_fx_tto.py` must not get a second owner. Rules as the Sheep's:
`node --check`, no browser, never `wardrobe_fx.py penguin` without `--probe` (the lead rebuilds once).

## How sure I am

| item | sure | why |
|---|---|---|
| The 4 byte layouts | high | exact byte use on all 8 instances; values make sense (mLv 1-3, fades, 12 s) |
| Tornado / typhoon clocks (0.4 s create, 0.4 s destroy, 6 s typhoon) | high | bare literals; `chaAdjust` at CHA 1 |
| The glide 2.4 m and the typhoon's homing | medium | Unity 3.5's exact drag formula assumed (`v *= 1 - drag dt`); exp form within 4 % |
| AdditiveSaturate two passes | medium-high | the shader source is plain; alpha doubling follows the page's convention |
| Opaque1 / 2 only pass 2 drawing | high | `_Color.a` below the 0.95 test |
| 206 / 207 names | medium | the alphabetical rule fits 200, 202, 203, 205; not checkable offline |
| snowMan hides the hero | high | `renderer.enabled = false` loop right before the Instantiate |

## Questions for the user (only what the Sheep / Wolf decisions don't answer)

1. **Staff of Time.** With `w_pgn59` (the wardrobe's `specialScepter`) in hand, the game's Normal Attack and Spread Shot
   balls barely move (0.01 m/s) and last 12 s, a mine. Follow the weapon worn on the page? Default: **yes** (the game's
   behaviour, one check in the part).
2. **Typhoon's first swerve** depends on the target's network number: 0, 120 or 240 degrees. Default: **one of the
   three at random each play** (all three end on the 10 m point by about 1.6 s).
3. **Snow Man hides the hero** (the game switches her renderers off and shows a snowman). Default: **hide her** for the
   snowman's time, back at its end or on the next pick.

## Verification (2026-11-10)

A skeptical re-trace by a checker agent (office PC); no builder run, no browser.

**What I checked:**
- Every `Penguin.cs` line cited (9665, 9672, 9681, 10220, 10235, 10245, 10726, 10744, 10832, 10839, 10909 / 10948 /
  10987 by sLv 1 / 2 / 3, 11029, 11032, 11072, 11137, 11182 / 11221 / 11260, 11302-11311, 11360, 11472, 11518-11520,
  11535, 16437, 16500, 26881, 32804, 33353, 35054, 37615, 39268, 39279, 39288, 39464): each says what the report says.
  Tornado's max rank is 3 (Bible `penguin-skill-reference.md:28`), so `tornado3` / `typhoon3` 4 m ahead holds.
- The scripts: `Penguin_tornado.cs` (42, 98, 103, 174, 179, 225-231, 248-256, 391, 428, 442, 472, 515, 531, 605 /
  635 / 638, 744-778, 898-940), `Penguin_typhoon.cs` (81-93, 205, 287, 330, 356-372, 416, 436, 472, 515 / 557 / 560,
  733-772, 819-853: the angle is `(tID − 1) × 120` with tID the actor number, 902-927, 1081, 1126),
  `Penguin_arcticEmperor.cs`, `Penguin_cosmicFriday.cs` (60, 72-87, 330-406, 529-580), `Penguin_iceBlock.cs` (44, 51, 84,
  116-138, 157, 211), `Penguin_nAttack.cs` (25, 44-53, 97-145, 196, 229, 272), `Penguin_manaMissile.cs` (26, 45-51,
  98-107 against `ProjectileControl.life`, 119-134, 211), `Penguin_snowMan.cs` (Init: owner rotation, the > 1 m
  scale test; follows while `actionState == "snowMan"`), `CharacterControl.cs` 20593 (chaAdjust: `Random.Range(0, 1)`
  is 0, so 6 × 1.015 → 6) and 38692 / 38705 / 38711 (renderers off, then the snowMan spawn and Init).
- LAYOUTS: the public fields of all 8 scripts, in order, are exactly the listed ones (no `[SerializeField]` anywhere):
  tornado / typhoon int + 2 × Vector3 = 28 bytes, arcticEmperor 8 floats = 32, iceBlock 2 ints = 8, the other four
  none. The values in `probe.txt` match.
- Shaders: `AdditiveSaturate.shader` (2 passes, :9-26 / :27-43, pass 2 `constant * previous double` with no texture),
  `Opaque1.shader` (pass 1 ZWrite Off AlphaTest GEqual 0.95, pass 2 alpha blend), `Opaque2.shader` (pass 2 :19-31 ZWrite
  Off, Cull Off, AlphaTest Less 0.95), `diffuseambient.shader` (lit, `primary * texture double`). The materials using them
  by GUID: AdditiveSaturate = arcticEmperor, ShadowPortal_0, Wolf_heartRing (as said). Built-in ids in the rip's .mat
  files: 206 = 15 (fallingComet1 and giantComet among them, as said), 207 = 13, 205 = 24.
- Page lines: `index.html` 1027-1028 (Penguin SEQ: no tornado / typhoon / iceBlock), 3035-3042 (Sound.play has no
  volume handle), 3050-3071, 3104-3113 (fxMaterial 2 × tint), 3163-3165, 3199, 3227, 3526; `wardrobe_fx.py:37`
  (BUILTIN_BLEND has no 205-207); `tto_sheep.js:24`; `shuriken.js:258` (TrailModule skipped).
- Physics and clips (`probe2.txt`): mass 1, drag 0 (Init sets 2), constraints 112 (rotation frozen), capsule r 1 h 3,
  the loops `cyclone` at volume 0; create / destroy 0.4 s, root 0.833 s; cosmicFriday 0.5 / 9.033 / 0.5 s.
- The others: the inventory (48 / 38 / 10; `nAttack_fire`, `manaMissile_fire`, `snowMan` absent), `item_map.json`
  w_pgn59 = `specialScepter` (the only one), `Penguin.prefab:683-688` (CharacterController h 1, r 0.3, centre y 0.6),
  `Math.cs:840-841` (rotateH), Bible :206 (Staff of Time), `D:\12tails` holding `12TailsOnline_Data` on this PC too
  (so `wardrobe_fx.py`'s BIBLE is D: here, as said).
- The glide (2.4 m limit) and the typhoon's terminal speed (0.96 × 0.16 / 0.04 = 3.84 m/s) re-derived by hand.

**Corrections made in this file:**
1. arcticEmperor Start: "(:50) ... (:53) ... (:56) ... (:59)" -> ":51 / :54 / :57 / :60". Proof:
   `Penguin_arcticEmperor.cs:51` `this.s0HfRiD47E = this.m09fpK1X6E + this.FadeDelay;`, :54, :57, :60 the next three
   (the cited lines are the guards' `{`).
2. "component's wrap decides (`mesh.js:157`)" -> `:159`. Proof: `mesh.js:159` `wrap = clip.wrap || c.wrap || 1`
   (:157 is `const use = name => {`).
3. "ShatterMesh (`mesh.js:236`) keeps only `material[0]`" -> `:237`. Proof: `mesh.js:237`
   `if (Array.isArray(m.material)) m.material = m.material[0];`.
4. Built-in 205: "its 12 materials" -> "its 24 materials in the rip". Proof: 24 `.mat` files with
   `m_Shader: {fileID: 205, ...}` (BlackTrail, Dust10/11, ShadowLine1-4, ..., and two named `Smoke4_multiply`, which
   backs 205 = Multiply).
5. 207 is not only the `_dead` materials: + `netherBane` and `fireWall` (13 in all). Proof: the same grep for 207.
6. Item 8 left out one sound: the `snowMan` prefab's own AudioSource plays `sounds/snowMan` (probe.txt), beside the
   voices `snowman1-2`; added (different file names, no collision).

**Unresolved (not disproved):** the exact-byte decode of every instance (I checked the field lists, not re-ran
`probe.py` with the patch); the 206 / 207 shader names (the alphabetical rule fits; not checkable offline: the
report's own "medium"); whether typhoon's FixedUpdate force runs before `active` (the guard at `:309-318` jumps to
`IL_461`, not traced); the tornado's comps order (AudioSource after the script); the typhoon's 0.68 s / 1.64 s
settle times (`sim_typhoon.py` not re-run); Cosmic Friday's Opaque1 "also Bison `massStun`" (no `massStun` material
uses Opaque1 by name; it may share `earthsmasher.mat`).
