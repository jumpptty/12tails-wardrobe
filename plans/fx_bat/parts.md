# Bat effects: the parts the page cannot draw yet (or draws wrongly)

Research 13/11/2026, home PC (one of the Bat fx researchers; scope: every part the Bat's effects need, the inventory's
26 plus the 34 Bat prefabs it does not list, the Shade4 prefabs and sounds Guardian of the Night uses, and the TTO
Nightfall Swarm's parts). Models: `plans/fx_penguin/parts.md`, `plans/fx_sheep/parts.md`. Read only: nothing in
`wardrobe/data` was written, `wardrobe_fx.py` / `wardrobe_fx_tto.py` ran with `--probe` only, no browser.
`DecompiledSource` lines are `D:\12tails\DecompiledSource\<file>`; TTO is `TTO1102:` + method + RVA.

Probes (read only, outputs beside them) in `checks/fx_bat_research/parts/`:
- `probe.py` -> `probe.txt`, `summary.txt`: all 60 prefabs in `heroes/bat/effects` through `wardrobe_fx.effect()`, an
  unknown script's field bytes and raw words, every material's blend, and the components `effect()` skips (Rigidbody,
  colliders, Light, CharacterController). `UNKNOWN` line: the field byte count of each script with no layout.
- `probe2.py` -> `probe2.txt`: every Animation clip (name, length, wrap), every AudioSource (clip, volume, loop,
  rolloff), and the references inside Bat_guardianOfTheNight / Bat_illusion, resolved to names.
- `probe3.py` -> `probe3.txt`: the Shade4 prefabs (`elementals/shade4/effects`: nAttack_hit, castEffect, nAttack_blade)
  and which files the guardian's two references live in.
- `calc.py` -> `calc.txt`: the Echoes orbs' homing to the 10 m target, the Homing Wand bolt, the Mirage Orb's fade.
- `tto_probe.json` (+ `.err`): `wardrobe_fx_tto.py bat --probe` of the Nightfall Swarm prefabs.
- `disasm.py` -> `disasm.txt`: TTO's `BatSwarmFlap::Awake` / `Update` disassembled (capstone, read from the Bible's
  `client\GameAssembly.dll`), with the constants they read.

## Read this first

1. **Seven Bat scripts and one shared script have no layout.** `probe.txt`'s last line: Bat_echoes 12 bytes,
   Bat_guardianOfTheNight 16, Bat_illusion 80, Bat_mirageOrb 4, AudioControl 24, Bat_nAttack 0, Bat_illusionFire 0
   (and CharacterControl 668 on `illusion`, already in `NOT_DRAWN`). All five byte-carrying layouts below match their
   public fields in declaration order exactly (the raw words decode to the prefab values). `wardrobe_fx.py` raises on
   the five with bytes today, so `echoes`, `guardian`, `illusion`, `mirageOrb` and `nefariousWhip_hit` cannot even be
   built.
2. **The inventory sees 26 of the Bat's 60 prefabs.** It reads only `Resources.Load` in `Bat.cs`. The rest come from:
   - the hero prefab's fields (`Bat.cs:19587-19782`): `nAttack` (`nAttack_fire`), `nAttack_hit`, `drainLife`,
     `drainLife_charge`, `drainLife_hit` (`cAttack_hit`), `castEffect`, `castRing`, `illusion`, `illusion_ring` (field ->
     prefab inferred from the clone's twin fields, which `probe2.txt` resolves; the hero prefab's own were not resolved);
   - the clone's fields (`Bat_illusion.cs:2918-2945`, resolved in `probe2.txt`): `illusion_fire`, `castEffect_illusion`,
     `castRing_illusion`, `illusion_dust`;
   - the guardian's fields: `guardian_blade` and Shade4's `castEffect` (`probe3.txt`: sharedassets12 path 302 / 310);
   - the status looks `CharacterControl.cs` loads: blind :40581, charm :40668, chiroptophobia :41301, confuse :40626,
     corruption :40113, corruption_hit :9561, curse :40297, darkStalker :40996, doom :40491, doom_hit :44199,
     guardian_ring :40545, mindControl :40735, nightmare :40368, phantomBane :40059, phantomBane_hit :9479,
     shame :40944, blackServant :41379; bloodCarnage :41637 and every class's `bloodCarnage_ring` (a shared skill, not
     the Bat's).
   Of these, the parts that block are only `nAttack` (Bat_nAttack), `illusion` (Bat_illusion), `illusion_fire`
   (Bat_illusionFire), `drainLife` (Light, and the BoltEmitter target) and the five on the Offset / 205 shaders
   (table below). Tool gap for later, as the Penguin's: `wardrobe_fx_inventory.py` misses prefab fields and status looks.
3. **Three bolts point at nothing.** `drainLife`, `mindControl_ring` and `nightmare_ring` carry a BoltEmitter whose target
   the hero's code sets: `TargetPosition = target.collider.bounds.center` every tick (`Bat.cs:21972`) or `TargetCollider
   = hitObject.collider` (`:12033`, `:13775`; BoltEmitter.cs:155-173 reads the collider first, then the object). The
   page's `boltEmitter` (`index.html:4156`) uses `TargetNode` or the prefab's `TargetPosition` (250, 54, 150), a world
   point 290 m off, which its 50 m test drops: **all three draw no bolt today**. Fix: the cue's `to` as the target
   (Interfaces 1).
4. **Shaders the page draws wrongly (the inventory does not see shaders).**
   | material (effects) | shader | today | needed |
   |---|---|---|---|
   | `blind`, `corruption`, `Shadow1` (blind, corruption, corruption_hit, phantomBane, soulEater_hit, soulEater_ring) | game's `Particles/MultiplyOffset` | normal alpha blend of the texture (fxMaterial's fallback): a dark smudge painted on, not a multiply | multiply (Blend Zero SrcColor), colour lerp(white, tex x vcol, alpha), Offset 0, -1 |
   | `Smoke4_multiply` (nefariousWhip_hit's ground ring) | built-in **205** Particles/Multiply | `BUILTIN_BLEND` has no 205: drawn **additive**, white smoke instead of dark | the same multiply (205 = "multiply", Penguin report "Read this first" 4) |
   | `nefariousWhip4` (nefariousWhip_hit's rising wisps) | game's `Particles/AlphaOffset` | normal alpha blend, depth-tested | rgb x alpha, then SrcAlpha blend (a^2 edges), ColorMask RGB, Offset 0, -20000 (drawn in front) |
   | `guardian2` (the guardian's wings) | game's `Transparent/Opaque1` with `_Color.a` 0 in the prefab, faded to 1 by the script | mesh.js builds pass 2 only when the saved alpha is below 0.95 | both passes once a part drives alpha up to 1 (mesh.js) |
   | `guardian1` (the guardian's body) | `FX/Phoenix`, `_Color.a` 0 | invisible until driven (correct) | the guardian part drives it 0 -> 0.8 |
   Cross-class, not the Bat's (worth the same builder): MultiplyOffset is also Wolf `darkEdge_hit` and
   `vitalityStrike_hit` (no BB class code loads it); **AlphaOffset is 21 materials, among them `doubleArt` (the Wolf's Double Art banner, cued 81
   times in wolf.json), `retuunCast` (the Sheep's returnCast, 68 cues) / `freeCast` / `instantCast` and the status words (miss, resist, immune,
   evade, reflect ...)**, already cued and drawn as plain alpha today; AdditiveOffset is 33 (Wolf `bladeFang_hit`,
   `bloodFang_hit`, Penguin `nAttack_hit` ...). Counts: the rip's `.mat` files by the shader's GUID (this session).
5. **Two hero-side looks.** Shadow Illusion's clones are **copies of the Bat as she is dressed** (`Bat_illusion.summon`,
   `Bat_illusion.cs:157-351`: her weapon, accessory and trinket instantiated on the clone's bones, her body's
   `sharedMesh` and `material` copied) **tinted** `setColor(0.3, 0.2, 0.5)` for her own side (`:377-382`; 0.86 grey for
   foes), not the prefab's student-uniform mesh. That needs the page's hero, not effect data: a `"clone"` cue kind beside
   `"skin"` (part 6). Mimic (`Bat.cs:38941`, Instantiate(the target, the Bat's spot), and `hide` on the Bat, `:39312`;
   `CharacterControl.cs:32818-32840`: every renderer off) needs a target model the page has not: question 5.
6. **Guardian of the Night is a small AI with its own effects, sound and a sword trail**, and its hit effect and swing
   sound live in **Shade4's** folder under names the Bat's folder also has (`nAttack_hit`, `nAttack`, `castEffect`):
   `wardrobe_fx.py` would load the Bat's own. It needs aliases (Interfaces 6) and a way for a part to spawn an effect
   (Interfaces 4).
7. **Sounds the effects play themselves (`probe2.txt`): nothing new collides by kind.** Looping AudioSources:
   bigCast_ring, bloodCarnage, castRing (`cast_ring`), drainLife / mindControl_ring / nightmare_ring (all `drainLife`),
   guardian (`guardian_ring`, Shade4's), nightmare (`nightMare`), nefariousWhip_hit (`nefariousWhip`, under AudioControl):
   the page already loops them until the effect goes. Two by-name traps for the extractor's `rip_wav` lookup: Shade4's
   `nAttack.wav` (the guardian's swing, `Bat_guardianOfTheNight.cs:1047`) vs the Bat's own `sounds/nAttack.wav`, and
   `explosion1` (Shade4 `nAttack_hit`'s AudioSource: found in `Resources/sound/fx`, fine). Voices (`voices/`) are
   different names: echoes1-2, guardianOftheNight1-2, mirageOrb1-2, nefariousWhip1-2, shadowIllusion1, ShadowIllusion2
   (capital S in the rip).

## The Bat's blocked set

"Where" is where BB spawns it (the standing rules move enemy spots to the 10 m target point, facing the hero).

| effect | skill (spawn) | missing part(s) | where |
|---|---|---|---|
| `echoes` (x3) | Echoes (`RPC_echoes` case 3, `Bat.cs:28088-28098`; `RPC_echoes_fire` :11812-11900) | Bat_echoes layout + part | hero + 2 m up, yaw 0 / -120 / +120 |
| `nAttack` (x1, x3 at stage 3) | Normal Attack (`RPC_nAttack_fire1` :10746, `_fire2` :10836) | Bat_nAttack (0 bytes) part | `firePos` (1.3 m up, 1 m ahead) |
| `illusion_fire` | the clones' Normal Attack (`Bat_illusion.cs:2003-2093`) | Bat_illusionFire (0 bytes) part | each clone's firePos |
| `mirageOrb` | Mirage Orb (`RPC_mirageOrb_fire` :12656-12800, Instantiate :12679, `Init` :12799) | Bat_mirageOrb layout + part | 1 m up 1 m ahead; **at the target's feet with Distant Orb #403** (`Bat.cs:9279-9301`, :31235-31258) |
| `guardian` | Guardian of the Night (`RPC_guardianOfTheNight_cast`, Instantiate :30561, Init :30586) | Bat_guardianOfTheNight layout + part; Opaque1 both passes; spawn api; Shade4 aliases | hero - 4 m (behind), hero rotation |
| `illusion` | Shadow Illusion (`RPC_shadowIllusion_create` :12924-13125) | Bat_illusion layout; hero clone (`"clone"` cue) | (-1.5, 0, 2.6) and (1.5, 0, 2.6) (`:31511`, `:31541`) |
| `nefariousWhip_hit` | Nefarious Whip (`Bat.cs:44025`, at the target, hero rotation) | AudioControl layout + part; 205 multiply; AlphaOffset | target (10 m) |
| `drainLife` | Drain Life (cAttack channel, `Bat.cs:21772-21972`) | Light; BoltEmitter `to` | hand (0.1, 1.25, 0.65), bolt to the target |
| `mindControl_ring` | Mind Control (`Bat.cs:13738-13775`) | Light; BoltEmitter `to` | hero (bolt node at (-0.2, 1.25, 1.0)) |
| `nightmare_ring` | Nightmare (`Bat.cs:11996-12033`) | BoltEmitter `to` | hero |
| `blind`, `corruption`, `corruption_hit`, `phantomBane`, `soulEater_hit`, `soulEater_ring` | Blind, Corruption, Phantom Bane statuses / hits; Soul Eater | MultiplyOffset | target |
| `guardian_hit` (Shade4 `nAttack_hit`) | the guardian's two hits (`Bat.cs:12606-12619`, Quaternion.identity) | the alias (name clash) | target's near side |
| `guardian_blade` | the guardian's swing (`Bat_guardianOfTheNight.cs:1079-1095`) | spawned by the guardian part, parented to its `sword` bone | the guardian |

Ready today and only needing cues: everything else (castEffect / castRing and their `_illusion` twins, drainLife_charge,
drainLife_hit, dreamBurst_hit (AlphaTimer, built), shatteringDream_hit (ShatterMesh + AlphaTimer, built), nightmare
(multiply2 + opaque meshes), deadEffect (premul), the other status looks). Status prefabs with no EffectControl (blind,
charm, chiroptophobia, confuse, curse, darkStalker, doom, mindControl, nightmare, shame, guardian_ring, blackServant)
live until the code removes the status: the cue's `kill` (10 s cap), not a part.

## LAYOUTS (paste into `pipeline/wardrobe_fx.py`, after the Mana Vortex block)

```python
# the Bat's parts (plans/fx_bat/parts.md, 2026-11-13; checks/fx_bat_research/parts/probe.txt: each instance's bytes are
# the listed fields exactly; Bat_nAttack / Bat_illusionFire keep every field private)
LAYOUTS.update({
    "Bat_echoes": [("mTarget", "r"), ("mEchoesLv", "i")],                       # Bat_echoes.cs:577, :580 (12 bytes)
    "Bat_mirageOrb": [("isVisible", "b")],                                       # Bat_mirageOrb.cs:408 (4; Init sets it)
    "Bat_guardianOfTheNight": [("guardianBlade", "r"), ("castEffect", "r")],     # Bat_guardianOfTheNight.cs:169, :175 (16)
    # Bat_illusion.cs:2894-2945 (80 bytes): references only (the clone copies the hero, part 6)
    "Bat_illusion": [("mChar", "r"), ("Weapon", "r"), ("nAttack_fire", "r"), ("nAttack_hit", "r"), ("Bat_drainLife", "r"),
                     ("Bat_drainLife_charge", "r"), ("cAttack_hit", "r"), ("castEffect_illusion", "r"),
                     ("castRing_illusion", "r"), ("illusion_dust", "r")],
    "Bat_nAttack": [], "Bat_illusionFire": [],
    # AudioControl.cs:233-248 (24 bytes; Bat nefariousWhip_hit, and one effect each of Mole, Monkey, Panda, Whale)
    "AudioControl": [("minVolume", "f"), ("maxVolume", "f"), ("delay", "f"), ("fadein", "f"), ("middle", "f"),
                     ("fadeout", "f")],
})
```

And `BUILTIN_BLEND[205] = "multiply"` (`wardrobe_fx.py:43`; the comment there already names it; 24 materials in the rip,
the Bat's `Smoke4_multiply` the first cued one).

Values (`probe.txt`): echoes `mTarget` (0, 0), `mEchoesLv` 0 (`RPC_echoes_fire` sets both, `Bat.cs:11884-11887`);
mirageOrb `isVisible` true; guardian refs (5, 302) = `heroes/bat/effects/guardian_blade`, (5, 310) =
`elementals/shade4/effects/castEffect` (`probe3.txt`); nefariousWhip_hit AudioControl min 0, max 1, delay 0.5, fadein
0.5, middle 4, fadeout 0.2.

## Each part

Page parts plug in as the comment above `FX_PART_FILES` says (`index.html:3718-3737`): `wardrobe/fxparts/<file>.js`
default-exports `register(api)` and calls `api.part(type, build)`; `build(fx, node, comp, mat, nodeDef, data)` returns
`{ node, update(dt, cam) ("destroy" removes the node), stop?(), dispose?() }`. Helpers to reuse from
`fxparts/penguin.js`: `stepper` (50 Hz physics with an exact drawn path), `rotateTowards`, `lookRot`, `target(fx, dflt)`
(the cue's `to`), `play(fx, node, name, fade, wrap)`, `loopOf`, `setVol`. A shared `fxparts/bat.js` holds parts 1-6; the
generic ones get modules of their own (7, 8, 9).

### 1. Bat_echoes: `echoes` (Echoes' three orbs)

**What it does in BB (`Bat_echoes.cs`).**
- Awake (:23-46): layer 1; `velocity = TransformDirection(ProjectileControl.velocity)` (:36) = (0, 0, 4): **4 m/s**
  along the spawn rotation (`RPC_echoes_fire` instantiates with `LookRotation(fireDir)`, `Bat.cs:11835`).
- `RPC_echoes_fire` (`Bat.cs:11812-11900`): `ProjectileControl.life = 5 x rangeMod` = 5 s (:11844), `mTarget` = the
  target picked for this orb, `mEchoesLv = sLv` (2 at max rank).
- Update (:48-188), per frame: clock += dt; at `life` it calls `RPC_echoes_hit` **at its own position** (:120) and is
  destroyed (:141); with a target, every 0.1 s (:153-159) `forward = RotateTowards(forward, mTarget.collider.bounds.center
  - position, 0.5 rad, 1)` (:164), rotation = LookRotation (:169), velocity re-set to 4 m/s along it (:174).
- OnTriggerEnter (:190-555): on a foe's collider (other layer, not 1 / 2, tag Player / Enemy; a collider that is not its
  target is ignored from then on, :279) it is destroyed (:287) and calls `RPC_echoes_hit(ClosestPointOnBounds, forward,
  lv)` (:308-324: `echoes_hit` there with the HERO's rotation, `Bat.cs:11928-11935`), hits (:357) and, with `lv > 0`,
  re-fires from the hit point at the nearest OTHER foe within 30 m (:369-530). One target on the page: no bounce.
- Physics (`probe.txt`): Rigidbody no gravity, rotation frozen; BoxCollider 0.3 m trigger.

**The page part (`fxparts/bat.js`, about 25 lines, as `Penguin_manaMissile`).** Velocity 4 m/s along `fx.uQuat(node)`
at the spawn; every 0.1 s of its own clock (the first at the spawn) `rotateTowards(fwd, to - pos, 0.5)` with `to` =
`target(fx, V(0, 0.6, 10))` (decision: homing aims 0.6 m up); end when the centre comes within 0.45 m (box half 0.15 +
body 0.3) of the body's axis, centre +- 0.2 m (penguin.js `BODY_HALF`); at 5 s, else. Ends with `"destroy"`; the hit
effect is the cue's.
- `calc.txt`: fired at clip 0.6 s, orb 0 meets the 10 m body at **2.42 s after its spawn** (clip 3.02 s) at (0, 0.658,
  9.587); orbs 1 and 2 turn round and meet it at **2.60 s** (clip 3.20 s) at (-+0.048, 0.657, 9.563); the same at 30 /
  60 / 144 fps.
- `Math.rotateH(forward, 120 i)` (`Bat.cs:28093`) = (-sin a, 0, cos a) (`Math.cs:838-843`, the Penguin's finding):
  Unity yaw atan2(x, z) = 0, **-120, +120**.
- Cue shape: `[0.6, "fx", "echoes", {"y": 2, "rot": [0, -120, 0], "to": [0, 0.6, 10]}]` (and 0 / +120), the hits
  `[3.02, "fx", "echoes_hit", {"d": 9.587, "y": 0.658}]`, `[3.2, "fx", "echoes_hit", {"x": -0.048, "d": 9.563, "y":
  0.657}]`, `[3.2, ..., {"x": 0.048, ...}]` (full entry at the end).

### 2. Bat_nAttack and Bat_illusionFire: `nAttack`, `illusion_fire` (the bolts)

**What they do in BB.** The same code twice (`Bat_nAttack.cs`, `Bat_illusionFire.cs`):
- ctor: a homing speed (0, 0, 16) (`Bat_nAttack.cs:26`, `Bat_illusionFire.cs:26`); Awake: layer 1, `velocity =
  TransformDirection(ProjectileControl.velocity)` = (0, 0, 15) (prefab, `probe.txt`) (:51 in both): **15 m/s**.
- The hero sets `life = 1.25 x rangeMod` (`Bat.cs:10762`, :10883); `InitHoming(tID)` only with the **Homing Wand**
  `weapon == "w_bat59"` and a target (`Bat.cs:10765-10788`); for the clone bolt `InitHoming` also needs Illusion Effect
  #401 (`Bat_illusionFire.cs:103-124`; passives on: yes).
- FixedUpdate (`Bat_nAttack.cs:79-125`): clock += dt, Destroy at `life` (:89); with a homing target, every 0.1 s
  `RotateTowards(forward, target.collider.bounds.center - position, 0.1 rad, 1)` (:116) and the velocity becomes
  TransformDirection((0, 0, **16**)) (:122): 16 m/s from the first turn.
- OnTriggerEnter (:138-366): any collider not on the owner's layer nor 1 / 2 (the floor too) destroys it and calls
  `RPC_nAttack_hit(ClosestPointOnBounds, forward)` (:243) before the Player / Enemy test: the cue's hit, as the Penguin.
- Rigidbody: no gravity, rotation frozen; SphereCollider 0.4 m. The prefab's TrailRenderer (`Line_Flat_alpha`) is built
  (trail.js) and follows the node.

**The page part (`fxparts/bat.js`, about 25 lines, one builder for both types).** At build: `homing = api.worn("R") ===
"specialWand"` (`item_map.json` bat/weapon/w_bat59 = `specialWand`, the only code with it). Not homing: straight 15 m/s
along the spawn rotation, ends when the centre reaches y 0 (the Normal Attack rule: on the ground at the 10 m target
point) or at 1.25 s. Homing: the stepper at 50 Hz, the first turn at the spawn, then every 0.1 s, toward `target(fx,
V(0, 0.6, 10))`, 16 m/s after the first turn; ends within 0.4 + 0.3 m of the body's axis (centre +- 0.2), on the floor,
or at 1.25 s. `calc.txt`: from (0, 1.3, 1) the homing bolt meets the body at **0.54 s**; stage 3's side bolts (+-1 m
right, yaw +-15) also come back and meet it at 0.54 s.
- Cue options it reads: `rot` (the aim), `to`. The cues differ by the weapon: the hit times need `notWorn` /
  a new `worn` filter (question 2).

### 3. Bat_mirageOrb: `mirageOrb`

**What it does in BB (`Bat_mirageOrb.cs`).**
- ctor: its colour `(0.5, 0.5, 0.5, 0.5)` (:26). Init (:45-130, `Bat.cs:12799`): level `L = sLv + (Distant Orb ? 2 :
  0)` = **6** at max with the passive; end time `nLife + now` (:58), `nLife = chaAdjust(30)` (`Bat.cs:31265`);
  `isVisible = true` when the viewer is on the owner's layer (:96; the page: true).
- Update (:134-258): destroyed at the end time, when the owner is gone or down, or once its damage total
  `> 60 L - 10` (:185, :208); else every frame `a = Lerp(a, isVisible ? 0.05 : 0, 5 dt)` (:230 / :238) and
  `renderer.material.SetColor("_TintColor", (0.5, 0.5, 0.5, a))` (:244).
- OnTriggerStay (:263-360): a foe inside its 1 m sphere, at most every 0.5 s (:316): `a = 0.4` (:319, a flash) and
  `RPC_AddEffectDamage(300 + L, 6 L - 1)` (:346), the total += `6 L - 1`.
- So (`calc.txt`): from 0.5 it fades to 0.05 (0.17 at 0.25 s, 0.08 at 0.5 s, 0.05 by 1.5 s; the same within 2 % at 30-144
  fps); **with the target inside** (Distant Orb puts it at the target's feet, `Bat.cs:9279-9301`, :31241-31258): a flash
  to 0.4 at 0, 0.5, ... 5.0 s (11 ticks x 35 = 385 > 350) and it is **gone at 5.0 s**; without a target, 30 s (cut at
  10 s by the rule).
- Its own: Animation `root` 1.2 s (clip wrap 0 under the component's Loop: loops), a SkinnedMeshRenderer (395 verts,
  vertex colours) with `mirageOrb` (additive, tint alpha 0.043 in the prefab, which the script overwrites at once), its
  sound `mirageOrb` once.

**The page part (`fxparts/bat.js`, about 25 lines).** First update: clone the mesh's material (as alphatimer.js `own()`:
`renderer.material` is the renderer's own copy; keep `onBeforeCompile`), `a = 0.5`. Each frame `a += (0.05 - a) x
min(1, 5 dt)`, opacity `min(1, 2 a)` (fxMaterial's rule for a saved tint). Inside test: the cue's `to` (default the
10 m point's feet (0, 0, 10)) within 1 + 0.3 m of the orb horizontally and the body's height (0..1 m) overlapping the
sphere: then a tick at the first frame and every 0.5 s after: `a = 0.4`, count; after the 11th tick (`L` = 6:
`ceil((60 L - 10) / (6 L - 1)) + ...` = 11), `"destroy"` on the next update. A cue's `kill` (10 s) covers the no-target
case. `dispose` frees the clone.
- Cue shape (Distant Orb on, passives rule): `[t, "fx", "mirageOrb", {"d": 10}]` (Instantiate with
  Quaternion.identity, `Bat.cs:12679`: no rot); off: `{"d": 1, "y": 1, "kill": 10}`.

### 4. Bat_guardianOfTheNight: `guardian` (+ `guardian_blade`, Shade4 `nAttack_hit`, Shade4 `nAttack` sound)

**What it does in BB.** The summon (`Bat.cs:30549-30609`): `Instantiate(guardian, hero - 4 x forward, hero rotation)`
(:30561), `StartCoroutine(Init(bat, sLv))` (:30586); the Bat's timer `xMnv4YLKcX = now + chaAdjust(30 sLv)` (60 s, `:30592-30609`).
Its fields: `guardianBlade`, `castEffect`. State `init` (enum `eGuardianOfTheNightState`: init 0, standby, attack,
castSpell, unsummon) and **one shared clock `t0`** (`a4pGjxUjoI`) for every coroutine.
- **Init** (WaitForFixedUpdate coroutine, `Bat_guardianOfTheNight.cs:283-445`): `t0 = now`, `Play("walk")` Loop
  (:436-439); each fixed step until `t0 + 1 <= now` (:323): position = Lerp(owner - 4 fwd, owner - 2 fwd, now - t0)
  (:338), body `materials[0].color.a = Lerp(0, 0.8, now - t0)` (:351-378), wings `materials[1].color.a = Lerp(0, 1,
  ...)` (:383-406); then `state = standby`, `t0 = now` (:306-311).
- **Update** (:32-105), standby only: farther than 3 m from the owner (`sqrMagnitude > 9`, :57): CrossFade("walk",
  0.1) Loop, position = Lerp(position, owner + 2 x dir, dt), rotation = Lerp(rotation, LookRotation(-dir), 2 dt)
  (:63-80); else CrossFade("root", 0.2) Loop (:86-91). After Init it stands 2 m behind her: `root`.
- **The Bat's AI** (`Bat.GuardianOfTheNight`, `Bat.cs:12275-12442`, from her Update): while the timer runs and she
  lives, a scan every 2.5 s, the first in the frame after the summon (:12321, the timer starts at 0): a random
  living foe within `FindAreaTarget(Bat, 32, 12)`; closer than 16 m (`sqrMagnitude < 256`, :12394) ->
  `RPC_guardian_attack(foe.position, foe.forward)` (:12400); else 50 %: `RPC_guardian_cast` (:12414-12422). Timer out:
  `RPC_RemoveStatus` + `RPC_guardian_unsummon` (:12436-12439).
- **attack(mPos, tDir)** (WaitForFixedUpdate, :622-1420), `tDir` = the FOE's forward. Runs only from `standby`
  (:1375-1381): `state = attack`, `t0 = now`, CrossFade("root", 0.2). Five phases, each ending at the first fixed step
  with `t0 + 0.5 <= now`:
  | phase | each step | at its end |
  |---|---|---|
  | A (:1111-1179, :1014-1103) | body a = Lerp(0.8, 0, 2 dt0), wings Lerp(1, 0, ...): fade out where it stands | position = mPos - 6 tDir, rotation = LookRotation(tDir) (:1021-1026), **Play("nAttack") Once** (:1031-1036), PlayOneShot Shade4 `Sounds/nAttack` (:1047-1059), **guardian_blade** instantiated on the `sword` bone, localPosition (-1.1, 0, 0), localRotation Euler(0, 180, 90) (:1079-1095) |
  | B (:927-1012, :808-918) | position = Lerp(mPos - 8 tDir, mPos - 2 tDir, 2 dt0), fade in (0 -> 0.8 / 1) | hit everything within FindAreaTarget(guardian, 4, 3) (:848-871): `RPC_guardian_hit(foe.collider.ClosestPointOnBounds(guardian + up))` (:877, :893) |
  | C (:1367, :1275-1361) | position = Slerp(mPos - 2 tDir, mPos + tDir, 2 dt0) | the second hit, the same way (:1288-1333) |
  | D (:729-806, :693-725) | position = Slerp(mPos + tDir, mPos + 4 tDir, ...), fade out | Play("root") Loop, position = owner - 2 owner.forward (:700-710) |
  | E (:1217-1271, :1183-1205) | fade in, `(now - t0) / 0.5` | `state = standby` (:1190), done |
  Every resume first checks `state == attack` (:637-677): an unsummon aborts it.
- **castSpell** (:1646-1870): `castEffect` (Shade4) at the guardian + TransformDirection(0, 2.75, 1.2) (:1670),
  CrossFade("cast") ... only for a foe beyond 16 m: never with the 10 m target.
- **unsummon** (:1998-2119): `state = unsummon`, `Play("ko")` Once (:2033-2036), both alphas set full (0.8 / 1,
  :2045-2090), `WaitForSeconds(2)`, Destroy (:2012).
- `RPC_guardian_hit` (`Bat.cs:12606-12619`): Shade4 `Effects/nAttack_hit` at the point, `Quaternion.identity`.
- Clips (`probe2.txt`): root 1.6 s (Loop), run 1.0, walk 2.0 (Loop), nAttack 1.8, cast 1.7, ko 2.0. Materials:
  `guardian1` FX/Phoenix (`Shade4`, `_Color` 0.784 grey, `_Emission` (0.196, 0.203, 0.294)), `guardian2` Opaque1
  (`Shade4_wing`), both alpha 0 in the prefab; `Shade4_tri` scale 1.2; two repeatForever rings at the feet; a legacy
  emitter on `Spine1`; its loop `guardian_ring` (Shade4's sound).

**On the page, with the target 10 m ahead facing the hero (tDir = (0, 0, -1)).** Spawned at (0, 0, -4); Init walks it
to (0, 0, -2) over 1 s while fading in; the scan at ~0 s is refused (state `init`); **attacks start at 2.5 s and 7.5 s**
(the scan at 5.0 s finds the first attack in its last fixed step or later: each phase lasts 25-26 fixed steps because
`t0 + 0.5` rarely equals a step's float time, so the attack takes 2.50-2.60 s; at 7.5 s it is standby again).
Each attack, from its start: 0-0.5 s fades out behind the Bat; at 0.5 s it reappears **behind the target** at z 16 facing
the hero, plays `nAttack`, swings with the blade trail and the Shade4 swing sound; 0.5-1.0 s dashes z 18 -> 12 fading
in; **hit 1 at 1.0 s** (guardian_hit at the target's near side, (0, 1, 10.3) for a 1 m body); 1.0-1.5 s cuts through
z 12 -> 9; **hit 2 at 1.5 s** ((0, 1, 9.7)); 1.5-2.0 s on to z 6 fading out; at 2.0 s back to (0, 0, -2) (`owner - 2
forward`, still facing -z), `root`; 2.0-2.5 s fades in. (`Vector3.Slerp` of two world positions: in the game's world,
far from the origin, it is a straight lerp to within mm; the page uses lerp.) At the cut (10 s by the rule): unsummon:
the second attack is aborted at its next step (it is in phase E, 2.5 s in, or done), `ko` once, fully visible, gone at
12 s.

**The page part (`fxparts/bat.js`, about 110 lines).** A 50 Hz state machine that runs the coroutines as written: the
shared `t0`, the phase tests `t0 + 0.5 <= now` on the step clock (`k x 0.02`, as `float` sums: `Math.fround`), Init and
attack both stepping in the same fixed step (Init first: it was started first), Update's standby follow per frame, the
AI scan every 2.5 s from the spawn (the Bat's, on the page's frame clock), the target from `target(fx, V(0, 0, 10))` and
its forward `(0, 0, -1)` (the rot [0, 180, 0] rule). It:
- drives `node.position` / `quaternion` (the root, Unity space), the Animation (`play(name, fade, wrap)`: walk 0.1
  Loop, root 0.2 Loop, nAttack Once, ko Once), the two alphas: Phoenix opacity = a (alphatimer's rule), Opaque1 pass
  opacities = a (both passes, Interfaces 5), on per-spawn clones of the mesh's materials (Unity's `renderer.materials`);
- at each phase A end: `api.Sound.play(cls, "guardian_nAttack")` and `api.spawn("guardian_blade", ...)` following the
  `sword` node with localPosition (-1.1, 0, 0), localRotation Euler(0, 180, 90) (Interfaces 4);
- at each hit: `api.spawn("guardian_hit", {x, y, d})` at ClosestPointOnBounds(guardian + up) of the target's box
  (centre x / z of `to`, half width 0.3, height 0..1: question 4) with Quaternion.identity;
- the unsummon at the cue's `end` (seconds after the spawn; 10 by the rule): `ko` Once, alphas full, `"destroy"` 2 s
  later (the loop `guardian_ring` goes with it).
- Cue shape: `[t, "fx", "guardian", {"d": -4, "end": 10, "to": [0, 0, 10]}]` and the entry's `"builds":
  ["guardian_blade", "guardian_hit"]` (Interfaces 6).

### 5. AudioControl: `nefariousWhip_hit` (and Mole / Monkey / Panda / Whale, one effect each)

**What it does in BB (`AudioControl.cs`).** Start (:38-110): with `delay > 0` the AudioSource is stopped
(`playOnAwake = false`, `Stop()`); volume = `minVolume` when `fadein > 0`, else `maxVolume`. Update (:112-215), from
Start's time: before `delay` volume = min; then during `fadein` volume = Lerp(min, max, (t - delay) / fadein) and
`Play()` if not playing (the sound starts **from its beginning** at `delay`); during `middle` max; during `fadeout`
Lerp(max, min, ...); after, min. Fields as LAYOUTS. Opaque predicates checked by hand (all `continue`s dead, the
`break`s live).

**nefariousWhip_hit's values:** silent 0-0.5 s, the `nefariousWhip` loop starts at 0.5 s and fades in to 1 by 1.0 s,
holds to 5.0 s, fades out to 0 by 5.2 s, then plays silently until the effect is destroyed (EffectControl life 5 +
afterLife 5 = 10 s).

**The page part (`fxparts/audiocontrol.js`, about 25 lines, generic).** At build, the node's AudioSource handle
(`fx.sounds`, Interfaces 2): with `delay > 0` stop it; at `t >= delay` start a new one (`api.Sound.play(fx.cls, clip,
0, loop)`) and put it in the handle's place (so `Fx.dispose` stops it); each frame `setVolume(v)` per the phases. Loop
or not, the same.

### 6. Bat_illusion: the clones (`illusion`), a `"clone"` cue

**What it does in BB.** `RPC_shadowIllusion_create` (`Bat.cs:12924-13125`): `Instantiate(illusion, mPos,
LookRotation(tDir))` (:12944, tDir = the Bat's forward), `illusion_ring` at mPos, identity (:13064),
`summon(bat, damageMod, hitMod, chaAdjust(60))` (:13115). The spots: `getSpawnVector(Bat + up, TransformDirection(-+1.5,
-1, 2.6))` (`:31511`, `:31541`; a 4 m ray down to the floor, `Math.cs:1210-1237`: on flat ground **(-+1.5, 0, 2.6)**),
the second clone from rank 2. `summon` (`Bat_illusion.cs:60-410`): copies her stats, instantiates her weapon on
`mount_Hand_L`, accessory on `Head` (Euler(0, -90, 90)), trinket on Head / Spine1 / Spine2 by item (:157-330), copies
the body's `sharedMesh` and `material` (:339-351), and `setColor(0.3, 0.2, 0.5)` for her side (:377-382; `setColor`
writes the rgb of `_Color` on every renderer that has one, `CharacterControl.cs:21702-21800`; the normal hero colour is
0.86 grey, `:139`, `:15153`). It then plays its own `root` and repeats her Combo stages, Drain Life channel, emotes and
KO (Bat.cs calls on `bat_illusion*`; the Bible). `RPC_disappear` (`Bat_illusion.cs:2829-2850`): `illusion_dust` at its
position + 1 m up, identity, and Destroy; the Bat's recast dismisses old clones that way (`Bat.cs:31789-31848`).

**Why not the prefab.** The `illusion` prefab draws the default student body (`Bat_standard1`, 2,004 verts) and carries
25 clips over 55 bones (`probe2.txt`); in the game that mesh and material are replaced at once. Built as an effect it
would be the wrong look and a heavy `fx.json` entry.

**The page (lead, `index.html`, beside `HeroSkin`; about 60 lines).** A cue kind `"clone"`: `[t, "clone", "root",
{"x": -1.5, "d": 2.6, "kill": 10}]` (name = the hero clip it plays: the illusion's default `root`). `HeroClone`: a
`SkeletonUtils.clone` of `C.root` taken at spawn time (every mesh shown now: outfit, worn props, a skin cue's look),
each material cloned with its colour multiplied by (0.3, 0.2, 0.5) / 0.86 in gamma (= (0.349, 0.233, 0.581) as sRGB: the
page's hero stands for _Color 0.86), its own `AnimationMixer` on the hero's loaded clips (bound by bone names), placed at
the hero's world position + her facing x (x, 0, d) (Unity x is the hero's right: the mirror), her rotation; not under
an effect's mirror group. Listed in `FX.live` (a new pick or class change ends it), kill = `RPC_disappear`: the cue file
puts `illusion_dust` at the kill time `{"x": -1.5, "d": 2.6, "y": 1}`. Raycasts off (the piece menu ignores it).

### 7. Light (Unity built-in): `drainLife`, `mindControl_ring` (and Wolf `crusader_hit`, `lawbringer_hit`)

**What it is.** A point light (`m_Type` 2), colour (1, 0.53, 1) on drainLife, (0.085, 0.92, 1) on mindControl_ring,
intensity 1, range 2, render mode 2 (ForceVertex: "not important", per vertex), no shadows, no cookie (`probe.txt`).
The extractor already stores it ("as stored", `wardrobe_fx.py:308`). In Unity 3.5 it lights the lit materials within 2
m: the Bat herself (her hand casts the bolt) and lit effect meshes (Phoenix / Opaque / Lambert); the particle shaders
are unlit. Unity's vertex-light falloff: 1 / (1 + 25 (d / range)^2), nothing past the range.

**The page part (`fxparts/light.js`, about 25 lines).** `api.part("Light", ...)`: a `THREE.PointLight` under the node,
colour from `m_Color` as sRGB, `distance = m_Range`, intensity `2 x pi x m_Intensity` (Unity 3.5's lit shaders double
the light, three's Lambert divides by pi), removed with the node. Two page details for the lead:
- the falloff: patch `THREE.ShaderChunk.lights_pars_begin`'s `getDistanceAttenuation` once at load to Unity's
  `1 / (1 + 25 (d / cutoff)^2)` inside the cutoff (the page has no other point or spot light, so nothing else changes);
- adding / removing a light makes three recompile every lit material (the number of lights is in the program): keep
  one PointLight in the scene from the start at intensity 0, and let the part borrow it (one at a time; a second
  concurrent Light reuses a second pooled one), so Drain Life never stutters.
APPROXIMATED: the game's per-vertex lighting vs three's per-pixel; the intensity scale (check by eye on the dark stage).

### 8. BoltEmitter's target from the cue (`index.html`, lead): `drainLife`, `mindControl_ring`, `nightmare_ring`

`boltEmitter(fx, node, e, mat)`: when `e.TargetNode < 0` and the cue has `to`, the target point is `V(...fx.at.to)`
(the mirror group's space, as penguin.js's `target()`); else as today. `to` = the target's `collider.bounds.center`:
[0, 0.6, 10] (decision: 0.6 m up). Without it the three bolts draw nothing (Read this first 3). drainLife's root moves to
the hand each tick (`Bat.cs:21967`: hero + TransformDirection(0.1, 1.25, 0.65); spawned at (0, 0.82, 0.88), :21772):
the cue puts it at the hand. All three have no EffectControl or a 60 s followState one: the channel's end is the cue's
`cut` / `kill`.

### 9. The particle shaders with an Offset, and built-in 205 (`fxparts/particles.js`, new, through `api.shader`)

`api.shader(blend, make)` (`index.html:3730`) lets a module own a data blend; FXSHADERS is consulted first in
fxMaterial, and mesh.js routes unknown `shader:` blends there too. All from the rip's `shader/*.shader` (stubs with
their fixed-function text intact):
- **`shader:Particles/MultiplyOffset`** (`MultiplyOffset.shader:1-27`) and **`multiply`** (built-in 205, Unity 3.5's
  `Particle Multiply`, the same combine without the Offset): stage 1 `texture x primary`, stage 2 `previous
  lerp(previous) constant (1, 1, 1, 1)`: colour = lerp(white, tex x vcol, tex.a x vcol.a); `Blend Zero SrcColor`
  (dst x colour), ZWrite Off, Cull Off, Fog white, `Offset 0, -1` (MultiplyOffset only). Page: as mesh.js's `glass` /
  fxMaterial's `multiply2`: `blendSrc Zero, blendDst SrcColor, blendSrcAlpha One, blendDstAlpha One`, the fragment
  `rgb = mix(vec3(1), rgb, a)`, `a = 1 - luminance(rgb)` (the darkening carried by alpha over the empty canvas: stage x
  luminance); `polygonOffset` (0, -1) for the Offset one; no `_TintColor` (the saved one is a leftover). APPROXIMATED as
  multiply2: over empty canvas the multiply is grey, not coloured.
- **`shader:Particles/AlphaOffset`** (`AlphaOffset.shader:1-27`): stage 1 `texture x primary`, stage 2 `previous x
  previous alpha, previous alpha`: rgb = tex x vcol x a, alpha = a (a = tex.a x vcol.a); `Blend SrcAlpha
  OneMinusSrcAlpha` (so rgb x a^2 over), ZWrite Off, Cull Off, ColorMask RGB, `Offset 0, -20000`. Page: normal blending,
  vertex colours, `gl_FragColor.rgb *= gl_FragColor.a` in the fragment, `polygonOffset: true, polygonOffsetFactor 0,
  polygonOffsetUnits -20000` (the same GL mechanism: in front of the hero by about half a metre at the page's depth
  range), no tint doubling (no `_TintColor` in the shader).
- **`shader:Particles/AdditiveOffset`** (`AdditiveOffset.shader`; not the Bat's: Wolf bladeFang_hit / bloodFang_hit,
  Penguin nAttack_hit and 30 more): stage 2 `previous x previous alpha`, `Blend One OneMinusSrcColor` (fxMaterial's
  `addsoft` with rgb x alpha first), ColorMask RGB, Offset 0, -20000. Same module, if the lead wants it now.

### 10. Opaque1 with an animated alpha (`fxparts/mesh.js`)

`opaque1()` (`mesh.js:127-134`) builds pass 1 (ZWrite Off, AlphaTest GEqual 0.95) only when the SAVED `_Color.a` is
>= 0.95, and says "a part that animates _Color.a across 0.95 would need pass 1 too: none does yet". The guardian's wings
go 0 -> 1. Build both passes always (pass 1 discards every texel below 0.95 x its opacity, so at the saved 0 it draws
nothing: no change for cosmicFriday's 0.46 except one more material in the list), `userData.fxPass` 0 / 1 as now; the
guardian part sets both passes' opacity.

## TTO: Nightfall Swarm's parts (the released one; the timeline is `plans/fx_bat/tto.md`'s)

`wardrobe_fx_tto.py bat --probe` (`tto_probe.json`): `nightfallSwarm_reform`, `_hit`, `_bat`, `_wrap`, `_burst` exist in
TTO's catalog; `nightfallSwarm`, `_flap`, `_screech` do not (they are sounds: `Bat::Row6Sound@0x1AD00B0` loads from
`heroes/bat/sounds/` / `voices/`). Components: EffectControl, ImageEmitter, ParticleSystem (+ Renderer), GroundHugEmitter,
MeshFilter / StaticMesh, TrailRendererModern: all built (shuriken.js, groundhug.js, mesh.js, tto_sheep.js). Material
`tto_batRow6_batSolid` is `FlexibleCelShader/Cel No Outline` (built by tto_penguin.js's api.shader). Missing:
- **BatSwarmFlap** (on `nightfallSwarm_bat`'s root; fields `wingL` -> node 4 (named WingR), `wingR` -> node 3 (WingL),
  `beatsPerSecond` 9, `amplitude` 55, `lift` 10; `dump.cs:98919-98938`). Disassembled (`disasm.txt`):
  `TTO1102:BatSwarmFlap::Awake@0x1B1AEB0`: restL = wingL.localRotation, restR = wingR.localRotation; `phase =
  Random.Range(0, 6.28319)`; `beatsPerSecond *= Random.Range(0.85, 1.15)`. `TTO1102:BatSwarmFlap::Update@0x1B1AFC0`:
  `angle = sin(Time.time x beatsPerSecond x 2 pi + phase) x amplitude + lift`; `wingL.localRotation = restL x
  AngleAxis(angle, Vector3.up)`; `wingR.localRotation = restR x AngleAxis(-angle, Vector3.up)` (the whole angle, lift
  included, negated). Page part (`fxparts/tto_bat.js`, about 20 lines): the same, `Time.time` = the page's clock; the
  quaternions are Unity's numbers inside the mirror group (no conversion).
- The swarm's flight is moved by code (`Bat::SwarmPath@0x1AD2D30`, `Bat::SwarmLanding@0x1AD2500`,
  `Bat.<Regather>d__337::MoveNext@0x1B25130`, `Bat::Row6Body@0x1ACED20`): a CODE_MOVER in `wardrobe_fx_tto.py` and a
  part, as the Sheep's BreathFly, and probably the hero hidden while she is the swarm (`api.heroHide`). Their spec is
  the TTO report's; not traced here.
- `SKILL_FX["bat"]` (the five prefabs) and `SKILL_SOUNDS["bat"]` (`nightfallSwarm`, `nightfallSwarm_flap`,
  `nightfallSwarm_screech`, if BB's rip lacks them: it does, no such WAV in `heroes/bat/sounds`) in `wardrobe_fx_tto.py`.

## Interfaces (fixed up front, so the builders run in parallel)

1. **`boltEmitter` target from `fx.at.to`** when `TargetNode < 0` (part 8).
2. **`fx.sounds`**: the Fx constructor keeps every AudioSource's handle, `{ node, comp, h }` (loop or not), beside
   `fx.loops`; `Fx.dispose` stops them all (a one-shot's stop is harmless). A part may replace `entry.h`.
3. **`api.worn(slot)`** exists (`index.html:3744`); Bat parts read `"R"` (the main weapon).
4. **`api.spawn(name, at, opts)`** (lead): builds `new Fx(C.cls, name, data, at)` from the class's loaded `fx.json`,
   pushes it to `FX.live` (a new pick clears it) and returns it, or null when the data lacks it (counted in
   `FX.missing`, so the check fails). `opts.followNode = node` (a node of another Fx): each frame the new root's Unity
   transform = the other Fx's `uMatrix(node)` (no MIRROR_X: both are inside a mirror group), times `opts.local`
   (`{pos, rot}` in Unity numbers, the localPosition / localRotation the script sets). Used by the guardian (blade,
   hits); `at` takes the cue options (x, y, d, rot).
5. **mesh.js Opaque1: both passes always** (part 10); parts find a material's passes by `userData.fxBlend` /
   `fxPass`.
6. **Extractor (`wardrobe_fx.py`), lead:** `LAYOUTS` and `BUILTIN_BLEND[205]` above; `ALIASES = {"bat": {"guardian_hit":
   "gameassets/characters/elementals/shade4/effects/nattack_hit"}}` (an effect name -> its container path, tried before
   the class folder: the Bat's own `nAttack_hit` has the same name); `SOUND_ALIASES = {"bat": {"guardian_nAttack":
   "characters/elementals/shade4/sounds/nAttack"}}` for `rip_wav` (the Bat's `sounds/nAttack.wav` would win); and an
   entry key `"builds"` (effects / sounds a part spawns that no cue names) read by `cue_names()`.
7. **A `"clone"` cue kind** (part 6), lead, `index.html`.
8. **`fx.cutAt` / `api.FX.t`** as the Penguin's (no change); the guardian reads its own `end` option.

## Rank by value (effects unblocked / effort)

| rank | part | Bat effects it makes right | other classes | work |
|---|---|---|---|---|
| 1 | Bat_nAttack (+ Bat_illusionFire) | `nAttack`: every Normal Attack (x1, x3), the clones' bolts | 0 | ~25 lines |
| 2 | BoltEmitter `to` | drainLife (every Charge Attack), mindControl_ring, nightmare_ring | (Penguin's Mana Vortex unchanged) | ~3 lines |
| 3 | particles.js: MultiplyOffset, 205, AlphaOffset (+ AdditiveOffset) | blind, corruption, corruption_hit, phantomBane, soulEater_hit / _ring, nefariousWhip_hit | Wolf doubleArt, darkEdge_hit, bladeFang_hit ...; Sheep returnCast banners; Penguin nAttack_hit; the status words | ~45 lines |
| 4 | Bat_echoes | echoes (x3) | 0 | ~25 lines |
| 5 | Bat_mirageOrb | mirageOrb | 0 | ~25 lines |
| 6 | AudioControl + `fx.sounds` | nefariousWhip_hit's sound | Mole, Monkey, Panda, Whale (1 each) | ~25 + 5 lines |
| 7 | Light + the pooled light / falloff | drainLife, mindControl_ring | Wolf crusader_hit, lawbringer_hit | ~25 + 10 lines |
| 8 | the `"clone"` cue | Shadow Illusion (and the tiles that need clones: Switch, Shadow Sacrifice) | 0 | ~60 lines |
| 9 | Bat_guardianOfTheNight + `api.spawn` + aliases + Opaque1 | guardian, guardian_blade, guardian_hit | 0 | ~110 + 25 + 15 + 3 lines |
| 10 | BatSwarmFlap (TTO) | nightfallSwarm_bat | 0 | ~20 lines |

After all: `BUILT` in `pipeline/wardrobe_fx_inventory.py` += Bat_echoes, Bat_guardianOfTheNight, Bat_illusion,
Bat_illusionFire, Bat_mirageOrb, Bat_nAttack, AudioControl, Light; run it again (the recipe's rule).

## Who builds what (never two owners for one file; as `plans/fx_wolf/build_rules.md`)

| agent | owns | builds |
|---|---|---|
| A: bat | `wardrobe/fxparts/bat.js` (new) | Bat_echoes, Bat_nAttack + Bat_illusionFire, Bat_mirageOrb, Bat_guardianOfTheNight (against Interfaces 2, 4, 5) |
| B: shared parts | `wardrobe/fxparts/particles.js`, `audiocontrol.js`, `light.js` (new) | MultiplyOffset / 205 / AlphaOffset / AdditiveOffset; AudioControl; Light |
| C: mesh | `wardrobe/fxparts/mesh.js` | Opaque1 both passes |
| D: tto | `wardrobe/fxparts/tto_bat.js` (new) + `pipeline/wardrobe_fx_tto.py` | BatSwarmFlap, the swarm mover, SKILL_FX / SKILL_SOUNDS bat (with the TTO report) |
| lead | `wardrobe/index.html`, `pipeline/wardrobe_fx.py`, `pipeline/wardrobe_fx_inventory.py`, `wardrobe/fx_cues/bat.json` | Interfaces 1, 2, 4, 6, 7; the light pool and falloff patch; `FX_PART_FILES += "bat", "particles", "audiocontrol", "light", "tto_bat"`; `BUILT`; the rebuild and the cues |

Rules as the Penguin's: `node --check`, no browser for the builders, never `wardrobe_fx.py bat` without `--probe` (the
lead rebuilds once).

## Paste-ready cue fragments (for the skill reports' entries; times from the sources cited)

```json
  "echoes": {
    "why": "Bat.cs RPC_echoes (:27814-28220): clip echoes (:28211, wrapMode Once :28214) at 0; voice echoes1 / echoes2 (Random.Range(0, 2) :28252, Voices/echoes1 :28262, echoes2 :28293, PlayOneShot :28332 / :28348) at 0; Yield(2, 0.1) (:28330): echoes_ring at the hero (createEffect :27979; followState, cut at the standby 0.8 s: Yield(3, 0.5) :28336 + Yield(4, 0.2) :28351, :28141); at 0.6 s three orbs from the hero + 2 m up (:28088), Math.rotateH(forward, 120 i) (:28093) = yaw 0 / -120 / +120 (Math.cs:838-843), each homing on the target (Bat_echoes.cs:153-174: 0.5 rad every 0.1 s, 4 m/s; the target 10 m ahead, 0.6 m up); they meet it 2.42 s / 2.60 s later (checks/fx_bat_research/parts/calc.txt): echoes_hit at the contact with the hero's rotation (Bat_echoes.cs:308-324, Bat.cs:11928-11935); one target, no bounce (Bat_echoes.cs:369-530 needs another foe)",
    "cues": [
    [0, "voice", "echoes1|echoes2"],
    [0.1, "fx", "echoes_ring", {"cut": 0.8}],
    [0.6, "fx", "echoes", {"y": 2, "to": [0, 0.6, 10]}],
    [0.6, "fx", "echoes", {"y": 2, "rot": [0, -120, 0], "to": [0, 0.6, 10]}],
    [0.6, "fx", "echoes", {"y": 2, "rot": [0, 120, 0], "to": [0, 0.6, 10]}],
    [3.02, "fx", "echoes_hit", {"d": 9.587, "y": 0.658}],
    [3.2, "fx", "echoes_hit", {"x": -0.048, "d": 9.563, "y": 0.657}],
    [3.2, "fx", "echoes_hit", {"x": 0.048, "d": 9.563, "y": 0.657}]
    ]
  }
```

The `echoes` clip is its own tile (it has its own animation, `Bat.cs:1370`). The other fragments, for the skill
reports to place at their own clip times:
- Shadow Illusion (cast3, `RPC_shadowIllusion_cast` :31357-31890: clip :31672, castEffect :31690, voice
  shadowIllusion1 | ShadowIllusion2 :31722-31777 at 0; Yield(2, 0.4) :31882; the clones at **0.4 s**):
  `[0.4, "fx", "illusion_ring", {"x": -1.5, "d": 2.6}]`, `[0.4, "clone", "root", {"x": -1.5, "d": 2.6, "kill": 10}]`,
  the same at x 1.5 (rank 2+), and `[10.4, "fx", "illusion_dust", {"x": -1.5, "d": 2.6, "y": 1}]` x 2 (the kill =
  RPC_disappear).
- Guardian of the Night, at the summon time `t` (the end of its cast bar): `[t, "fx", "guardian", {"d": -4, "end": 10,
  "to": [0, 0, 10]}]`, entry `"builds": ["guardian_blade", "guardian_hit"]`, sound `guardian_nAttack` built via
  `"builds"` too (the part plays it).
- Mirage Orb (Distant Orb on): `[t, "fx", "mirageOrb", {"d": 10}]`.
- Nefarious Whip's hit: `[t, "fx", "nefariousWhip_hit", {"d": 10}]` (at the target, the hero's rotation, `Bat.cs:44025`).
- Drain Life: `[t, "fx", "drainLife", {"x": 0.1, "y": 1.25, "d": 0.65, "to": [0, 0.6, 10], "kill": <the channel's
  end>}]`; Mind Control / Nightmare rings: `{"to": [0, 0.6, 10], "cut": <standby>}`.

## How sure I am

| item | sure | why |
|---|---|---|
| The 7 layouts | high | public fields in order = the byte counts exactly; the raw words read as the prefab values (refs resolve to the named prefabs) |
| BoltEmitter draws nothing today | high | the prefab's TargetPosition is world (250, 54, 150), the page's 50 m test (`index.html:4171`) |
| MultiplyOffset / AlphaOffset / 205 combines | high | the rip's shader text; 205 = Multiply as the Penguin report (medium on the id, high on Smoke4_multiply being dark smoke) |
| Echoes' and the Homing Wand's arrival times | medium-high | the scripts' numbers; the contact radius is the decisions' body (0.3 m), not a real foe's |
| Mirage Orb 11 ticks / 5.0 s with Distant Orb | high | `60 L - 10`, `6 L - 1`, 0.5 s, the strict `>` |
| The guardian's attacks at 2.5 s and 7.5 s | medium | the 5.0 s scan race depends on float time; the shared `t0` is in the code (one field) |
| The clone copies the dressed hero, tinted | high | `Bat_illusion.cs:157-382` |
| Light's intensity on the page | low-medium | the scale between Unity's lights and the page's is by eye |
| BatSwarmFlap | high | disassembled; constants 2 pi, 0.85, 1.15 read from the instructions |

## Open questions (with my recommended answer)

1. **The guardian's AI on the page.** Run the scan / attack machine as written (attacks at 2.5 s and 7.5 s, unsummon at
   10 s, gone at 12 s), or a simpler one attack? Recommended: **as written** (it is the game's look: behind-the-target
   backstab, two hits, return), with the 10 s cut.
2. **The Homing Wand (`specialWand`, w_bat59) changes the Normal Attack**: the bolts home on the target (and stage 3's
   side bolts come back to it) and hit at 0.54 s instead of landing on the floor. Follow the worn weapon, as the
   Penguin's decision 18? Recommended: **yes**; the cue file needs a `worn` filter (the opposite of `notWorn`) for the
   homing hits.
3. **Guardian hits: part-spawned or cued?** The game's code spawns them from the guardian's own coroutine. Recommended:
   **the part spawns them** (`api.spawn`), since their times follow the part's state machine.
4. **The target's body for contact / ClosestPointOnBounds**: the decisions fix its centre at 0.6 m up; recommended a 1 m
   tall, 0.3 m radius body (the Penguin's), giving the guardian's hit points (0, 1, 10.3) / (0, 1, 9.7).
5. **Mimic** (a copy of the TARGET at the Bat's spot, the Bat hidden): the page has no target model. Recommended: a
   **self-mimic** (the game lets her pick an ally; her own copy over her hidden self looks like her), so no part: the
   tile plays the cast and its effects only.
6. **Clones in other tiles** (Combo, Drain Life, emotes repeat on live clones): recommended **no**; the clones appear only
   in Shadow Illusion, Switch and Shadow Sacrifice (where the skill needs them), via the `"clone"` cue.
7. **AlphaOffset / AdditiveOffset fix reaches already-published Wolf / Sheep / Penguin banners and hits** (doubleArt,
   returnCast, bladeFang_hit ...): recommended **yes, in the same build**, and say so in NOTES.md (their look changes).
8. **Light**: worth it for a 2 m pink / cyan glow on her hand side? Recommended **yes** (the rule: build every part),
   with the pooled light so there is no stutter.

## Verification

Checker, 2026-11-13 (home PC), read only, against `D:\12tails\DecompiledSource` (Bat.cs, Bat_echoes.cs,
Bat_mirageOrb.cs, Bat_guardianOfTheNight.cs, Bat_illusion.cs, Bat_illusionFire.cs, Bat_nAttack.cs, AudioControl.cs,
Math.cs, CharacterControl.cs), the TTO pseudo-C (`pseudo/Bat.c`, `dump.cs`), the rip's shaders and `.mat` files, this
report's probes (`probe.txt`, `calc.txt`, `disasm.txt`) and the page (`wardrobe/index.html`, `fxparts/mesh.js`,
`pipeline/wardrobe_fx.py`, `wardrobe_fx_tto.py`).

**Confirmed (no change):**
- LAYOUTS: every public field, in order, is the listed one and no other (`Bat_echoes.cs:577, :580`;
  `Bat_mirageOrb.cs:408`; `Bat_guardianOfTheNight.cs:169, :175`, the `AudioClip` between them, :172, is private, so not
  serialized: 16 bytes; `Bat_illusion.cs:2894-2945`, 10 refs = 80; `AudioControl.cs:233-248`, 6 floats = 24); with `r` =
  8 bytes the sizes match `probe.txt`'s UNKNOWN line. `Bat_nAttack` / `Bat_illusionFire` have no public field.
  `BUILTIN_BLEND[205]`: `Smoke4_multiply.mat` is `{fileID: 205, guid: 0000000000000000e000000000000000}`, 24 such `.mat`.
- Shaders (rip `gameassets/shader/*.shader`): MultiplyOffset `Blend Zero SrcColor`, `Offset 0, -1`, stage 2 `previous
  lerp(previous) constant` (= lerp(white, prev, prev.a)); AlphaOffset `Blend SrcAlpha OneMinusSrcAlpha`, `ColorMask
  RGB`, `Offset 0, -20000`, stage 2 `previous * previous alpha, previous alpha`; AdditiveOffset `Blend One
  OneMinusSrcColor`, the same stage 2. Counts by GUID: AlphaOffset 21 (doubleArt, retuunCast, freeCast, instantCast,
  nefariousWhip4 among them), MultiplyOffset 5 (blind, corruption, Shadow1, darkEdge_hit, vitalityStrike_hit),
  AdditiveOffset 33. guardian1 = FX/Phoenix, guardian2 = Transparent/Opaque1 (`mesh.js` `opaque1` builds pass 1 only at
  saved alpha >= 0.95, as said).
- The 18 status-look line numbers in `CharacterControl.cs` (each line loads the named prefab).
- BoltEmitter: `Bat.cs:12033`, `:13775` (`TargetCollider = hitObject.collider`), `:21972` (`TargetPosition =
  collider.bounds.center`); the page's `boltEmitter` uses `TargetNode` or `TargetPosition` and draws nothing at >= 50 m.
  Drain Life's spawn (0, 0.82, 0.88) identity (:21772) and hand (0.1, 1.25, 0.65) (:21967).
- Echoes: clip and voice at 0 (`Random.Range(0, 2)` :28252, echoes1 / echoes2 both exist in `voices/`), Yield 0.1 ->
  echoes_ring (createEffect :27979; EffectControl followPosition + followState, probe), Yield 0.5 -> three orbs at
  0.6 s from the hero + 2 up (:28088) at `rotateH(forward, 120 i)` (`Math.cs:838-843`: yaw 0 / -120 / +120), Yield 0.2 ->
  standby 0.8 s; orb target = a random foe within `FindAreaTarget(hero, 20, 10)` (:28053: the one 10 m target here);
  `Instantiate(echoes, firePos, LookRotation(fireDir))` (:11835), life 5 x rangeMod (:11844), prefab velocity (0, 0, 4).
- Normal Attack bolt: `FromToRotation(forward, fireDir)`, life 1.25 x rangeMod, `InitHoming` only with
  `weapon == "w_bat59"` (`item_map.json` bat weapon w_bat59 = specialWand) and a target (:10765-10788); homing 0.1 rad per
  0.1 s, then (0, 0, 16) (`Bat_nAttack.cs:26, :116, :122`). Clone bolts need the clone's copied weapon w_bat59
  (`Bat_illusion.cs:2022, :2113`) and #401 (`Bat_illusionFire.cs:109`).
- Mirage Orb: `Init(sLv + (hasSkill(403) ? 2 : 0), chaAdjust(30), ...)` (:12799, :31265; the life is passed in the `tID`
  slot); max rank 4 (the Bible card) -> L 6; `total > 60 L - 10` (`Bat_mirageOrb.cs:185`), `+= 6 L - 1` (:343), tick
  0.5 s / a = 0.4 (:316-319), `Lerp(a, 0.05, 5 dt)` (:230), `_TintColor` (:244): 11 ticks, gone at 5.0 s. Distant Orb
  spot = the target's `transform.position` (:9279-9301, :31258); without it `mPos + TransformDirection(0, 1, 1)`.
- Guardian: summon at hero - 4 forward, hero rotation (:30561), `Init` (:30586), `chaAdjust(30 sLv)` (60 s at rank 2);
  AI `sqrMagnitude < 256` -> `RPC_guardian_attack(foe.position, foe.forward)` else a 50 % cast (:12394-12422); phases:
  Init lerp -4 -> -2 over 1 s (:338), A end teleport `mPos - 6 tDir` (:1021), nAttack, Shade4 `Sounds/nAttack` (:1047),
  blade on `sword` at (-1.1, 0, 0), Euler(0, 180, 90) (:1084-1094); B `Lerp(mPos - 8 tDir, mPos - 2 tDir)` (:927) and
  hit 1 `ClosestPointOnBounds(guardian + up)` within `FindAreaTarget(guardian, 4, 3)` (:848, :877); C `Slerp(mPos -
  2 tDir, mPos + tDir)` (:1367), hit 2 (:1288, :1317); D to `mPos + 4 tDir` then back to owner - 2 forward (:729, :710);
  E fade in (:1217-1245). Hit prefab `Elementals/Shade4/Effects/nAttack_hit` (`Bat.cs:12619`). The hit points (0, 1,
  10.3) / (0, 1, 9.7) follow for the body box.
- Shadow Illusion: cast3 with 0.2 fade (:31672), castEffect at TransformDirection(0, 1.3, 1) (:31690), voice
  shadowIllusion1 | shadowIllusion2 (`Random.Range(0, 2)`, :31722-31766; the rip's file is `ShadowIllusion2.wav`),
  Yield 0.4 -> the clones (state 2, :31511 / :31541; the second only when sLv > 1), the clone `Instantiate(illusion,
  mPos, LookRotation(tDir))` (:12944), `illusion_ring` createEffect at mPos, identity (:13064; followPosition only);
  tint `setColor(0.3, 0.2, 0.5)` (`Bat_illusion.cs:377`). Nefarious Whip's hit: createEffect on the target at its
  position with the hero's rotation (`Bat.cs:44037`).
- TTO: BatSwarmFlap (`dump.cs:98919`, Awake / Update constants as `disasm.txt`), the five prefabs in the catalog.

**Corrections:**
1. **Echoes' hit point** (section 1 "Cue shape", lines 172-174, and the paste-ready block): `Bat_echoes.cs:308` calls
   `RPC_echoes_hit(mCollider.ClosestPointOnBounds(this.collider.bounds.center), ...)`, the point on the target's box
   nearest the orb, not the orb's centre. With the decisions' body (centre 0.6 m up, radius 0.3: box z 9.7-10.3), the
   three contacts (orb centres z 9.587 / 9.563) land on its front face: **d 9.7**, x and y unchanged (inside the box).
   The Penguin's Mana Missile hit (the same `ClosestPointOnBounds`) was cued at 9.7 the same way. Times unchanged.
2. **TTO section, `SKILL_SOUNDS["bat"]`** (lines 422-423): `nightfallSwarm` is not a sound. It is the clip / command
   name (`DAT_183869fb0`: `Row6Begin` `Bat.c:18769`, the cooldown `addTimeOut` in `DoRow6Skill`, `Row6End` :19490). The
   sounds are `nightfallSwarm_screech` and `nightfallSwarm_flap` only (with BB's `bloodCarnage_ring`, `drainLife`), and
   `Row6Sound@0x1AD00B0` loads only `GameAssets/characters/heroes/bat/sounds/` (`Bat.c:45157-45190`); `voices/` is
   `Row6Voice@0x1AD02B0`'s, which this skill never calls. So lines 405-407 ("`nightfallSwarm`, `_flap`, `_screech` ...
   they are sounds ... `sounds/` / `voices/`") read: `_flap` and `_screech` are `sounds/` clips, `nightfallSwarm` the
   clip. `SKILL_SOUNDS` itself is optional: `wardrobe_fx_tto.py:602` already fetches every `"sound"` cue BB's rip lacks.
3. **TTO section, the mover's sources** (lines 418-419): `Bat::Row6Body@0x1ACED20` plays no part in the swarm (it is
   called neither from `<RPC_nightfallSwarm>d__336::MoveNext`, `Bat.c:18584-19497`, nor from `DoRow6Skill`'s Nightfall
   branch; its callers are other Row6 code, `Bat.c:136, 192, 377, 8475, 12045, 22189, 41963, 42615`). The bats' chest
   spot is `Row6Chest@0x1ACEE60`. And "probably the hero hidden" is certain: `HideBody@0x1AC44A0` at 0.4 s (:18898),
   `ShowBody@0x1AD0500` at 0.9 s (:19420), as `plans/fx_bat/tto.md` P1 (a).
4. **Shadow Illusion's spots** (part 6, lines 322-323): `Math.getSpawnVector` (`Math.cs:1210-1237`) is not "a 4 m ray
   down": it casts 4 m from hero + 1 m up **along** `TransformDirection(-+1.5, -1, 2.6)` (layer mask 5) and falls back
   to `mPos + mDir`, then `getSpawnPos`. On flat ground both give (-+1.5, 0, 2.6): the cue positions stand.
5. **Interfaces 7, the `"clone"` cue kind**: the page treats every cue kind other than `"fx"` / `"skin"` as a sound,
   in both places: `fxStart`'s prefetch (`index.html:4464`, `c.kind !== "fx" && c.kind !== "skin"` -> `Sound.get`) and
   `fxDue` (`:4513-4519`, `else if (c.kind !== "fx") Sound.play(...)`). A `"clone"` cue would request
   `data/bat/sfx/root.mp3` and play nothing. The lead adds `"clone"` beside `"skin"` in both (`wardrobe_fx.py`
   `cue_names` already skips unknown kinds, `:375`).
6. Line cites that moved in the edited `index.html` (no content change): the part-plugin comment is `:3722-3744`,
   `api.worn` `:3751`, `boltEmitter` `:4163`, its 50 m test `:4171`.

**Corrected paste-ready block** (only the three `echoes_hit` cues and the end of the `why` change):

```json
  "echoes": {
    "why": "Bat.cs RPC_echoes (:27814-28220): clip echoes (:28211, wrapMode Once :28214) at 0; voice echoes1 / echoes2 (Random.Range(0, 2) :28252, Voices/echoes1 :28262, echoes2 :28293, PlayOneShot :28332 / :28348) at 0; Yield(2, 0.1) (:28330): echoes_ring at the hero (createEffect :27979; followState, cut at the standby 0.8 s: Yield(3, 0.5) :28336 + Yield(4, 0.2) :28351, :28141); at 0.6 s three orbs from the hero + 2 m up (:28088), Math.rotateH(forward, 120 i) (:28093) = yaw 0 / -120 / +120 (Math.cs:838-843), each homing on the target (Bat_echoes.cs:153-174: 0.5 rad every 0.1 s, 4 m/s; the target 10 m ahead, 0.6 m up); they meet it 2.42 s / 2.60 s later (checks/fx_bat_research/parts/calc.txt): echoes_hit at mCollider.ClosestPointOnBounds(the orb's centre) (Bat_echoes.cs:308), the front of the target's box at 9.7 m, with the hero's rotation (Bat_echoes.cs:308-324, Bat.cs:11928-11935); one target, no bounce (Bat_echoes.cs:369-530 needs another foe)",
    "cues": [
    [0, "voice", "echoes1|echoes2"],
    [0.1, "fx", "echoes_ring", {"cut": 0.8}],
    [0.6, "fx", "echoes", {"y": 2, "to": [0, 0.6, 10]}],
    [0.6, "fx", "echoes", {"y": 2, "rot": [0, -120, 0], "to": [0, 0.6, 10]}],
    [0.6, "fx", "echoes", {"y": 2, "rot": [0, 120, 0], "to": [0, 0.6, 10]}],
    [3.02, "fx", "echoes_hit", {"d": 9.7, "y": 0.658}],
    [3.2, "fx", "echoes_hit", {"x": -0.048, "d": 9.7, "y": 0.657}],
    [3.2, "fx", "echoes_hit", {"x": 0.048, "d": 9.7, "y": 0.657}]
    ]
  }
```

And the TTO line for `pipeline/wardrobe_fx_tto.py` (optional, as `plans/fx_bat/tto.md` P3):

```python
SKILL_SOUNDS["bat"] = ["nightfallSwarm_screech", "nightfallSwarm_flap"]   # TTO1102:Bat::Row6Sound@0x1AD00B0 (sounds/ only), Bat.c:18896-18897
```
