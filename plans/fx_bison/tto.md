# Bison effects + sounds research: the three TTO Lv 100 skills (Unchained Fury, Titan Drop, Magma Quake)

Scope: the TTO clips `unchainedFury` (1.8 s), `titanDrop` (2.0 s) and `magmaQuakeAxe` (2.2 s), all `tto: true` in
`wardrobe/data/bison/clips.json`, group `skill`. No BB code plays them. **All three are in the released list**
(`["magmaQuakeAxe","titanDrop","unchainedFury"]`, also in `wardrobe/tto_released.json`), so all three get cues.
Research only: this file is the only file written, plus the probes in `checks/fx_bison_research/tto/` (git-ignored).

Sources:
- TTO's pseudo-C `D:\12tails\DecompiledSource_TTO_2026-11-02\pseudo\Bison.c` and `CharacterControl.c`, cited as
  `TTO1102:Method@RVA` plus `Bison.c:<line>` (the pseudo-C line numbers change when the export is redone; the RVAs don't);
- capstone over `client\GameAssembly.dll` for the floats Ghidra drops (`dis.py`), the string literals a method's machine
  code loads (`strings_in.py`, through the Bible's `tools/usages.py`), call sites (`callers.py`), and a unicorn run of
  the two trig helpers (`trig.py`);
- BB's `DecompiledSource\CharacterControl.cs` / `AudioControl.cs` for the shared status look and the sound envelope
  (TTO's apply step is BB's, the Bible's `bison-skill-reference.md` "TTO Lv 100 skills", lines 718-833);
- TTO's 2026-11-04 bundles on this PC (`D:\12tails-video\tto_assets\2026-11-04`) through
  `wardrobe_fx_tto.py bison --probe` (`probe.json`, `probe_unchained.json`; summaries `compact.txt`, `compact2.txt`,
  `scripts.txt`) and BB's rip through `wardrobe_fx.py bison --probe` (`probe_bb.json`, `bbsum.py`).

Times are seconds from the start of the clip the cue is keyed by. Unlike the Penguin, most Bison waits are
**`Waits.Get(t)` = wait t seconds** (relative; the coroutine state's time is the sum), checked against `dump.cs`'s
named constants (`MagmaRamAt 0.43`, `MagmaImpactAt 0.9`, `MagmaEndAt 2.2`, `UnchainedBreakAt 0.62`, `UnchainedRoarAt
0.95`, `UnchainedPlantAt 1.45`, `UnchainedLength 1.8`). Titan Drop alone uses **`Bison::Until(start + t)`** (absolute),
whose float Ghidra drops: read with capstone (0.4 at `0x1B79A62`, 2.0 at `0x1B79292`; the rings read
`TitanDropRingAt` = [1.5, 1.9, 2.3] from the `.cctor`). All three skills have one rank, so max rank changes nothing;
Rage Control (a passive, on at max rank) only raises Unchained Fury's Berserker Rush level 4 -> 5 (no other look).

## Read this first

1. **Every effect the three skills spawn is probed.** 17 TTO-only prefabs (`unchainedFury_chains`, `_break`, `_roar`,
   `_plant`; `titanDrop_takeoff`, `_mark`, `_charge`, `_dive`, `_slam1..3`; `magmaQuake_magmaTick`, `_quakeTick`,
   `_magmaField`, `_quakeField`, `_magmaSlam`, `_quakeSlam`) plus the status look `unchained`, and four BB prefabs the
   code reuses (`calamityHammer_ring`, `earthSmasher_ring` by Row6Spawn; `berserkerRush`, `berserkerRush_ring` through
   the Berserker Rush status). No arcana style (the catalog has no `heroes/bison/arcana/`).
2. **Two status looks the Bible doesn't mention** (both in my cues):
   - `unchained` (the 3 s status Unchained Fury puts on at the press): `CharacterControl::AddUnchainedFx@0x24AEB60`
     (`CharacterControl.c:5541-5643`, called from `<addStatus>d__481::MoveNext` at `0x24FD6A6`, removed by
     `RemoveUnchainedFx@0x24C2920` from `removeStatus` at `0x24E8CDB`): the prefab `effects/unchained` at the hero,
     parented to it, world scale 1 (a spinning sigil, six orbiting chain links, two looping energy arcs).
   - **Berserker Rush's own look** at 0.62 s: TTO's `addStatus` loads BB's literals (`effects/berserkerRush_ring` at
     `0x24EDA65`, `effects/berserkerRush` at `0x24ED4E9`, the names `berserkerRush1Fx` / `berserkerRush2Fx`, the bones
     `HandMount_L` / `HandMount_R`: `strings_in.py`), i.e. BB's `CharacterControl.cs:34752-34942`: `berserkerRush_ring`
     at the hero (identity, InitEffectControl) and a `berserkerRush` on each hand mount, kept while the status lasts
     (removed `:15477-15510`). 12 s x CHA, cut at 10 s by the standing rule.
3. **Voices and sounds.** Only Magma Quake has hero sounds: `Row6Voice@0x1B467B0` (`voices/`, 50 % pick between its two
   names) at the press (axe `calamityHammer`; hammer `earthSmasher1|earthSmasher2`) and, axe only, `sounds/`
   `magmaClutter1|magmaClutter2` at the impact (PlayOneShot volume 1.2). Unchained Fury and Titan Drop play **no voice
   and no hero sound**: every other sound is a prefab's own AudioSource. All hero clips are in BB's rip. None of the three
   coroutines rolls a proc.
4. **Magma Quake follows the weapon** (`isHammer@0x1B4EF30`, 24 codes; the flag travels as `tID`): one clip
   (`magmaQuakeAxe`) for both, but different voice, ring, tick look, slam, field and tick count (12 / 10). In the
   wardrobe the 24 codes are 20 weapon props (`wardrobe/data/item_map.json`, the BB-corrected map; section 2.3), with
   no axe prop sharing them. My cues pick the branch by the worn weapon (a new cue-option form, part B7; question 2).
5. **Magma Quake's ticks draw the game's own spots.** 12 tick looks per tick at uniform random points of a 30 m disc
   around the centre, from `System.Random` seeded with the cast position (`Bison.c:7813`). For a Bison at the origin the
   seed is 0, so the game itself would draw exactly the 144 (axe) / 120 (hammer) spots of the cue block (`calc.py`
   reproduces .NET's seeded Random; its first draws 0.72624327, 0.81732536 are .NET's own `new Random(0)` values).
   `FUN_180308640` is cosf and `FUN_180308bd0` sinf (`trig.py`: 0 -> 1 / 0), so spot = centre + (cos a, 0, sin a) x r.
6. **Titan Drop flies 3 m up in the game, and the clip doesn't.** The `titanDrop` clip's Root holds a mid-air pose at the
   standing height from 0.6 to 1.4 s (`clips.json` Root track: z 0.96 throughout); the code moves the transform along
   `TitanDropPath@0x1B47610` (height keys 0 / 2.8 / 3.0 / 0 at 0.4 / 0.85 / 1.2 / 1.5 s; along keys 0 / 0.38 / 0.55 / 1).
   The block keeps the Penguin's decision 8 (in place, no mover), so the Bison would hang in its leap pose on the ground
   for about a second; question 1 recommends a vertical lift part (B8).
7. **Missing parts** (section 4): `Bison_row6Fx`, `Bison_c6Arc` + its shader `TTO/Bison/EnergyArc`,
   `TTO/Bison/MoltenCrust`, `AudioControl`, `GroundConformParticles` (a no-op on the page's flat floor, so only a
   registration), the cue option `worn` / `notWorn` with an item set, and optionally the Titan Drop lift.
   `titanDrop_mark`, and the four BB prefabs, need nothing new; `titanDrop_charge` and `titanDrop_dive` need only
   AudioControl.
8. **No `followState` on any TTO prefab except `unchainedFury_chains`** (life 0.62 + 0.05, so its cut at Row6End 1.8 never
   bites). The two BB rings (`calamityHammer_ring` 3 + 1, `earthSmasher_ring` 1 + 3) are followState: cut at Row6End
   2.2. The code destroys only the Titan Drop mark early (kill 1.1, at the landing).
9. **Effects that run past their clip** (they play in the idle tail, as Grand Codex / Emperors March): Titan Drop's third
   ring (2.3 > 2.0), Magma Quake's ticks (to 6.9 s) and field (to 8.4 s), the Berserker Rush hands (to 10.62 s). With
   the loop toggle on they are cut at the clip's end.
10. **SEQ:** nothing to change. None of the three has a cast bar (Bible: "No cast bar ... none of the three calls
    `DisplayCastBar`"), each is one clip, and the page has no Bison SEQ entry for them (only Normal / Charge Attack).
11. **Code vs bundles.** The decompile is TTO1102; this PC's bundles are 2026-11-04; there is no newer decompile here. The
    one later code change the Bible records (`TTO1106:Bison::TitanDropSpot`, the wall ray) moves no effect.

---

## 1. Shared machinery (`TTO1102:Bison`)

- **`Row6Begin(command, mPos, tDir, clip, wrap)@0x1B45C70`** (`Bison.c:28325`): `actionState "attack"`, `myCommand` = the
  skill, the hero put at mPos, `LookAt(mPos + vFlat(tDir))`, `PlayAnimation(clip, 0.1)`, wrapMode Once, moveSpeed 0.
- **`Row6End(command)@0x1B46060`** (`:28425`): `standby`, only while the action is still this command (every
  `followState` cut below is this moment).
- **`Row6Spawn(name, pos, rot, owned)@0x1B464E0`** (`:28094`): loads `GameAssets/characters/heroes/bison/effects/<name>`
  (`Row6Prefab`, logs "Cannot find <name> effect"); owned -> `CharacterControl.createEffect` (InitEffectControl: an
  owned prefab's followPosition / followState work), else a bare `Instantiate`.
- **`Row6Voice(a, b)@0x1B467B0`** (`:28258`): `voices/<a or b>` (b null or `Random.Range(0, 2) == 0` -> a), PlayOneShot
  volume 1 on the owner (0.75 others), only with the `pvoice` preference on and (for others) in team modes.
- **`Row6Sound(name, vol)@0x1B46420`** (`:28571`): `sounds/<name>` (unused by these three; Magma Quake plays its impact
  sound inline, same path).
- **`MagmaQuakeAt(local)@0x1B41160`** (`:28635`) = hero + right x local.x + flat-forward x local.z, y = the ground
  (`GroundHugEmitter.Ground`). Statics (`Bison::.cctor@0x1B48BD0`, `:30656`): `MagmaButt` (0.8, 0, 1.3),
  `MagmaCenter` (-0.45, 0, 0) (the dump names the fields, `dump.cs` Bison constants).
- **`MagmaQuakeShake` / `QuakeRumbling` / `TitanDropZoomBack`**: camera only (left out, as every class's shakes).
- Status looks: `unchained` (`AddUnchainedFx`, above) and `berserkerRush` (BB's apply, above). No `AddBisonRow6Fx`
  exists (the class list in `methods.tsv` has the Row6Fx helpers of Bat, Cat, Chameleon, Monkey, Penguin, Rabbit,
  Sheep, Whale only).

## 2. Per skill

### 2.1 Unchained Fury (`unchainedFury`, 1.8 s; cell 452)

At the press, before the coroutine, `UnchainedCleanse@0x1B48570` (caster's client) pays the HP, cleanses, breaks free,
and `RPC_AddStatus(213 unchained, 1, 3)` (Bible :731-735). No prefab there except through the status look.

Coroutine `TTO1102:Bison.<RPC_unchainedFury>d__278::MoveNext@0x1B7BFC0` (`Bison.c:17596-17876`):
- **0.00**: status `unchained` look: `unchained` at the hero, hero rotation, parented, world scale 1, kept for the
  status's 3 s (no EffectControl in the prefab: it lives until `RemoveUnchainedFx`) -> cue `kill 3`.
  Row6Begin, clip `unchainedFury` (`:17652`); cooldown; `unchainedFury_chains` **owned** at the hero, hero rotation
  (`:17673`). Its EffectControl: life 0.62, afterLife 0.05, followPosition, followState (cut 1.8, never reached).
- Waits 0.62 (`:17677`) -> **0.62** (state 1, if still doing the skill): `unchainedFury_break` at the hero, hero
  rotation, not owned (`:17706`); `MagmaQuakeShake(pos, 3, 14)`; owner: `RPC_AddStatus(203 berserkerRush,
  max(current, getRageControlLv() + 4), chaAdjust(12))` (`:17735`; level 5 with Rage Control on) -> the status look:
  `berserkerRush_ring` at the hero, identity rotation, InitEffectControl (its EffectControl: 1.0 + 0, followPosition)
  and `berserkerRush` (no EffectControl) on `HandMount_L` and on `HandMount_R`, localPosition 0, kept for the status
  (12 s x CHA) -> cues `bone`, `kill 10` (the 10 s rule).
- Waits 0.33 (`:17743`) -> **0.95**: `unchainedFury_roar` **owned** at the hero, hero rotation (`:17770`; 1.0 + 1.2,
  followPosition; its own `Sound_enrage` = BB's `sounds/enrage`); shake (4, 18).
- Waits 0.5000001 (`:17785`) -> **1.45**: `unchainedFury_plant` at the hero + 2.6 x flat-forward + 2.45 x right
  (`UnchainedPlantAhead` / `UnchainedPlantRight`, `:17838`), hero rotation, not owned (`:17848`): the weapon's
  ground-strike cracks at the axe head; shake (2, 10).
- Waits 0.3499999 (`:17859`) -> **1.8**: Row6End (`:17870`).
- No voice, no sound call. Spawn heights are the hero's (no ground snap).
- Passives / rolls: the HP payment is a hit (`ApplyDamage`), so it can roll the **Berserker Rush passive** on the
  payment frame (`getBerserkerRush`, BB `4 x level`% x LCK) and give the same look 0.62 s early; Blood Rage gives SP only
  (no look). Left out (question 5).

### 2.2 Titan Drop (`titanDrop`, 2.0 s; cell 453)

The target is an enemy within 18 m (`TitanDropTargetInReach@0x1B48260`); `toSpot` is the flat vector to the target's
spot. By the standing rule the target is 10 m ahead.

Coroutine `TTO1102:Bison.<RPC_titanDrop>d__281::MoveNext@0x1B78BD0` (`Bison.c:15885-16338`):
- **0.00** (state 0): `dir` = flat(toSpot) (else the hero's forward), `faceRot` = LookRotation(dir); `land` = mPos +
  dir x max(dist - 3.9, 0) - right x 0.26 (`:16024-16025`: `TitanDropHeadAhead 3.9`, `TitanDropHeadRight 0.26`),
  `slamAt` = land + right x 0.26 + dir x 3.9 (each snapped to the ground by `Math.getSpawnPos`): for the 10 m target,
  land 6.1 m ahead and 0.26 m left, slamAt exactly on the target. Row6Begin, clip `titanDrop` (`:16080`); cooldown;
  camera AutoZoom (left out); `Until(start + 0.4)` (`:16137`; capstone `0x1B79A62`: 0.4).
- **0.40** (state 1): `titanDrop_takeoff` at mPos (the start spot), faceRot, not owned (`:16155`); `titanDrop_mark` at
  slamAt, faceRot, not owned (`:16160`), kept as `mark`; `TitanDropCharge(faceRot)@0x1B46C50` (`:16166`):
  `titanDrop_charge` at `HandMount_R`'s position and rotation, not owned, then `RideWeapon@0x1B45710`: parented to the
  mount, localPosition 0, localRotation identity, localScale 1 / the mount's lossyScale (`:30113-30147`); never
  destroyed by the code on a normal landing (its own 1.1 + 0.45 life ends it). Then every frame: the hero's position =
  `TitanDropPath(now - start, mPos, land)`.
- **first frame at or after 1.20** (`:16245`, `1.2 <= now - start`, once): `titanDrop_dive` **owned** at the hero's
  current (airborne) position, rotation LookRotation(land - pos) (`:16275`). At 1.2 s the path is at height key 3.0,
  along key 0.55 (keys are exact values; SmoothTangents only bends between them): pos = 3.355 m ahead, 0.143 m left,
  3.0 m up; land - pos = (2.745 ahead, 0.117 left, 3.0 down) -> **47.5 deg down, 2.4 deg left** (`calc.py`). The dive is
  0.2 + 1.2 s, followPosition: it rides the hero down.
- **1.50**: the hero set on `land`; `mark` destroyed (`:16204`; its own life 1.1 + 0.1 ends at the same 1.5-1.6 s);
  `TitanDropRings(start, slamAt, faceRot)` started (`:16210`): `<TitanDropRings>d__289::MoveNext@0x1BA91D0`
  (`:18540-18664`) waits `Until(start + TitanDropRingAt[i])` (`:18646`) = **1.5 / 1.9 / 2.3** and spawns
  `"titanDrop_slam" + (i + 1)` (`:18584`) = `titanDrop_slam1` / `_slam2` / `_slam3` at slamAt, faceRot, not owned
  (`:18593`), a shake each, and the owner's ring hit. `Until(start + 2.0)` (`:16215`; capstone `0x1B79292`: 2).
- **2.00**: Row6End (`:16329`). Ring 3 at 2.3 s plays in the idle tail.
- Interrupted in the air (`TitanDropDoing` false): mark and charge destroyed, `TitanDropFall` (no prefab), no rings. Not
  on the page.
- No voice, no sound call: the prefabs carry them (`titanDrop_takeoff`: trample1, overSwing at +0.05 s;
  `titanDrop_charge` holdCharge_ring; `titanDrop_dive` instantRush; `titanDrop_slam1` titanQuake_hit + hammer_hit2;
  `_slam2` earthSmasher + earthSmasher_ring at +0.2 s; `_slam3` titanQuake_hit + gadina_planetBreaker).
- **On the page, in place** (the Penguin's decision 8 / the Wolf's Feral Strike convention, no hero mover): land = the
  hero, so the takeoff at the hero, the mark and the three rings **3.9 m ahead, 0.26 m right** (land + 0.26 right + 3.9
  ahead, the geometry kept relative to the landing, as Frost Field's burst 1.5 m ahead), the dive at the hero with its
  game rotation `rot [47.5, -2.4, 0]`. The rings' own radii (the slams' shock discs 9.2 / 14.9 / 20.7 m) are drawn
  around that spot. Question 1 has the lift option.

### 2.3 Magma Quake (`magmaQuakeAxe`, 2.2 s; cell 454)

The branch: `hammer = tID & 1` (`Bison.c` state 0), set by `DoRow6Skill` from `isHammer@0x1B4EF30` at the press (24
codes: w_bsn5, 15, 19, 22, 24, 25, 32, 34, 35, 40, 41, 42, 45, 46, 49, 50, 51, 52, 59, 60, 61, 62, 68, 69). Through
`wardrobe/data/item_map.json` (the BB-corrected map; `item_map_tto.json`'s trace is the shifted one, NOTES 2026-11-05)
they are the **20 weapon props** `stoneClub, toyHammer, bdWeapon, defenderHammer, defenderHammerR, barbell,
warlordHammer, warlordHammerR, hallowLance, havocHammer, havocHammerR, havocHammerV, superStarBass, mummyMace,
goldenHammer, royalHammer, royalHammerR, specialHammer, legendHammer, timeHammer` (w_bsn62 maps to `legendHammerR`,
which is no prop; w_bsn68 has no prop). No axe code maps to one of them, so the worn prop decides exactly. The other 27
Bison props (the axes, lances, scythe, hoe, `studentWeapon`) are the axe branch.

Coroutine `TTO1102:Bison.<RPC_magmaQuake>d__234::MoveNext@0x1B69E50` (`Bison.c:7634-7843`):
- **0.00**: Row6Begin, clip `magmaQuakeAxe` for both weapons (`:7688`); cooldown; `Row6Voice` (`:7702`): axe
  `calamityHammer` (one name), hammer `earthSmasher1|earthSmasher2`; owned at the hero, hero rotation (`:7720`): axe
  **`calamityHammer_ring`**, hammer **`earthSmasher_ring`** (BB's prefabs, both followPosition + followState: cut 2.2).
  `Waits 0.43` (`:7724`).
- **0.43**: the tick look (axe `magmaQuake_magmaTick`, hammer `magmaQuake_quakeTick`) at `MagmaQuakeAt(MagmaButt)` = the
  hero + **0.8 right, 1.3 ahead**, on the ground, identity, not owned (`:7746-7759`): the weapon butt / head striking
  the ground; shake (1.5, 12). `Waits 0.47` (`:7770`).
- **0.90**: centre = `MagmaQuakeAt(MagmaCenter)` = **0.45 m left**, on the ground, fixed (`:7787`).
  `MagmaQuakeImpact@0x1B41710` (`:7792`, `:28734-28870`): axe `magmaQuake_magmaSlam` at the centre, identity, not owned
  (`:28777`) + `sounds/magmaClutter1|magmaClutter2` (`Random.Range(0, 2) == 0` -> 1, `:28778`) PlayOneShot at **1.2**
  (`:28797`); hammer `magmaQuake_quakeSlam` at the centre (`:28815`), no sound call; camera shake 3 / 6 (left out).
  The field at the centre, identity (`:7807`): axe **`magmaQuake_magmaField`** (EffectControl 6 + 1.5: to 8.4 s),
  hammer **`magmaQuake_quakeField`** (5 + 2: to 7.9 s); both under 10 s, no cut. `System.Random(seed)` (`:7813`),
  `MagmaQuakeTicks` started (`:7816`), hammer also `QuakeRumbling` (camera, 5 s). `Waits 1.3` (`:7827`).
- **2.20**: Row6End (`:7837`).
- **Ticks** (`<MagmaQuakeTicks>d__239::MoveNext@0x1B5C3A0`, `Bison.c:1-139`): radius 30 (`0x41f00000`, `:38`), ticks
  `RoundToInt(2 x life)` = 12 (axe, life 6) / 10 (hammer, 5), 12 bursts a tick (`:45`); the first `Waits 0.5`
  (`:133`) comes before the first tick, so ticks at **0.9 + 0.5 k = 1.4, 1.9 ... 6.9** (axe) / **... 5.9** (hammer). Each
  tick: 12 x { u1 = rng, r = sqrt(u1) x 30 (`:81`); u2 = rng, a = u2 x 2 pi; spot = centre + (cos a x r, 0, sin a x r)
  (`:87-90`), on the ground (`GroundHugEmitter.Ground`); Row6Spawn(tickFx, spot, identity, not owned) (`:113`) }; then
  the owner's hit (`:121`, no prefab). The seed = `RoundToInt(z x 50) x 0x127409f ^ RoundToInt(x x 50) x 0x466f45d` of
  the cast position: 0 at the origin. The spots are world axes; on the page the hero faces +z, so x = right, z = ahead
  (the page turns cues by the hero's facing, which keeps the pattern). Only 13 of the 144 axe spots (9 %) and 9 of the 120 hammer spots lie within 10 m of the hero (the
  radius is 30 m; the field's own pool is 30 m too).
- The weapon-butt look at 0.43 and the 0.9 impact are the Bible's "0.43 s weapon-butt FX" and "0.9 s impact"; the Bible
  calls `MagmaQuakeImpact` camera / FX only, but on the axe it also plays the magmaClutter sound.

## 3. What is left out, all three

- The camera: `MagmaQuakeShake` (every state), `QuakeRumbling`, Titan Drop's AutoZoom / ZoomBack.
- The hits: `TitanDropHit`, `MagmaQuakeHit`, the KO waves: no prefab, nothing to draw.
- The Berserker Rush passive roll on Unchained Fury's HP payment (question 5).
- Titan Drop's fall when interrupted.

## 4. Parts the page lacks (effect: part)

Per effect (probe, `compact2.txt`); "ready" = every component is one the page builds (EffectControl, GroundHugEmitter
discs, ImageEmitter, Shuriken incl. UVModule / mesh particles / stretched mode / local simulation, TrailRendererModern
(tto_sheep.js), StaticMesh, the legacy emitters):

| Effect | Needs |
|---|---|
| `tto/unchained` | B1 Bison_row6Fx, B2 Bison_c6Arc, B3 EnergyArc |
| `tto/unchainedFury_chains` | B1, B2, B3, B5 AudioControl |
| `tto/unchainedFury_break`, `_roar`, `_plant` | B2, B3, B5 |
| `tto/titanDrop_takeoff`, `_slam1`, `_slam2`, `_slam3` | B2, B3, B5 |
| `tto/titanDrop_mark` | ready |
| `tto/titanDrop_charge`, `_dive` | B5 |
| `tto/magmaQuake_magmaTick`, `_quakeTick` | B6 GroundConformParticles (a no-op here) |
| `tto/magmaQuake_magmaSlam` | B2, B3, B6 |
| `tto/magmaQuake_quakeSlam`, `_quakeField` | B2, B3, B5, B6 |
| `tto/magmaQuake_magmaField` | B4 MoltenCrust, B5, B6 |
| `berserkerRush`, `berserkerRush_ring`, `calamityHammer_ring`, `earthSmasher_ring` (BB's rip) | ready (legacy emitters, ImageEmitter, RingEmitter, LineEmitter, EmitterControl, the inventory's "ready" kinds) |

The parts (one agent each, `plans/fx_wolf/build_rules.md`; a new `wardrobe/fxparts/tto_bison.js` for B1, B2, B6):
- **B1 `Bison_row6Fx`** (`TTO1102:Bison_row6Fx::Awake@0x1B9CDE0`, `OnEnable@0x1B9CE90`, `Update@0x1B9CEB0`,
  `Bison.c:31628-31834`; fields spin, tightenFrom, tightenTime, tremble, pulse, strainTime, bob, bobRate). Awake keeps the
  node's localScale / localPosition / localRotation and `seed = Random.value x 100`; t = now - OnEnable time;
  k = 1 - (1 - clamp01(t / tightenTime))^2, s = clamp01(t / strainTime)^2;
  localScale = base x (1 + sin(47 t + seed) x s x pulse) x lerp(tightenFrom, 1, k);
  localRotation = baseRot x Euler(0, spin x t, 0) x Euler(sin(61 t + seed) x s x tremble, 0, sin(53 t + 2 seed) x s x
  tremble) (the products read off the pseudo-C: P = baseRot x Q(spin), then P x Q(tremble));
  localPosition = base + up x bob x sin(bobRate x t + seed) (bob 0: base). Used by the chain rings (tighten from 1.7-2.0
  to 1 in 0.1-0.16 s, tremble 7 deg, pulse 5 %, spin +-30 deg/s), the sigils (spin -40 / 50) and the unchained orbit
  (spin 120, bob 0.08 at 3).
- **B2 `Bison_c6Arc`** (`Awake@0x1B9B7C0`, `Drape@0x1B9B9A0`, `OnEnable@0x1B9BDB0`, `Update@0x1B9BDF0`,
  `Bison.c:30754-31165`; fields delay, duration, diameter, angle, spin, repeat, color, hug, lift): the renderer hidden
  until `delay`, and after `duration` unless `repeat` (then t mod duration); u = t / duration;
  localScale = diameter x (0.65 + 0.4 x (1 - (1 - u)^2)); localRotation = Euler(0, angle + spin x t, 0); the
  material's `_TintColor` (a property block) = 0.5 x (lerp(color.rgb, (1, 0.38, 0.08), clamp01(0.45 u)), alpha =
  color.a x ss(clamp01(u / 0.08)) x (1 - ss(u) - 0.25 (1 - ss(u)))), ss(x) = 3x^2 - 2x^3, ss(u) on clamp01(u) (`Bison.c:31058-31121`
  ); `hug`: every frame each mesh vertex is moved to the ground under it +
  `lift` (0.25) in world space (Drape: on the page's flat floor, the arc lies flat 0.25 m up wherever the node is).
  Every arc is a pair (angle 25 / 205: two opposite sweeps), diameters 3.1-60 m.
- **B3 the shader `TTO/Bison/EnergyArc`** (`tto_c6_energyArc`: no texture, `_TintColor`, `_InvFade`): read its
  programs from the bundle as the Penguin's cel shader was (`plans/fx_penguin/tto.md` "Built", P3: DXBC from the
  shader asset), and give it to the page through `api.shader("shader:TTO/Bison/EnergyArc", make)`. Until then it draws
  as plain alpha (index.html's fallback), i.e. a solid band.
- **B4 the shader `TTO/Bison/MoltenCrust`** (`tto_c6_moltenCrust`, the lava pool `tto_mq_lavaPool`, `_TintColor`
  white): the same way. Only `magmaQuake_magmaField` uses it.
- **B5 `AudioControl`** (TTO1102 `AudioControl::Start@0x2298D00` / `Update@0x2298E70`; the same script as BB's
  `DecompiledSource/AudioControl.cs`: minVolume, maxVolume, delay, fadein, middle, fadeout): with delay > 0 the source
  is stopped at Start and played at `delay`; volume min until delay, min -> max over fadein, max for middle, max -> min
  over fadeout, then min (a loop stays playing, silent). Every TTO prefab here carries one: most one-shots are cut to
  middle + fadeout (holdCharge_ring 0.62 s on the chains, 1.1 s on the charge; titanQuake_hit 1.8 s ...), `overSwing`
  starts at +0.05 s, `earthSmasher_ring` at +0.2 s, and the two **looping** beds fade: `MagmaPit` 0.4 in, 4.6 held, 1.0
  out (the magma field's 6 s), `titanQuake_ring` 0.1 / 4.1 / 0.8 (the quake field's 5 s). Without it the loops play at
  full volume until the effect is destroyed (7.5 / 7 s) and the one-shots run to their clip's end. Page: a part on the
  node's AudioSource through `Sound.play`'s handle (`setVolume`, index.html "Interfaces") plus a start delay.
- **B6 `GroundConformParticles`** (TTO1102 `Sample@0x2260BF0`, `GroundAt@0x2260680`, `LateUpdate@0x2260850`;
  radius, spacing, maxStep; `gcp_*.asm`): LateUpdate moves each particle of the systems below it up by
  `GroundAt(x, z) - origin.y` when that is 0.01 or more (`0x2260ADF-0x2260B3B`), from a height grid sampled at Start.
  On the page's flat floor that is always 0: register an empty part so the inventory reads it as built; no drawing
  change.
- **B7 cue option `worn` / `notWorn` with an item set** (index.html `fxStart` / `cueOf`; today `notWorn` is
  `[slot, item]`, one item, decision 18): `"worn": ["R", "bisonHammer"]` plays the cue only while one of the set's items
  is worn in that slot, `"notWorn": [...]` the reverse; a set name resolves through a table `ITEM_SETS = { bisonHammer:
  [the 20 props of 2.3] }` (`TTO1102:Bison::isHammer@0x1B4EF30` through item_map.json). Accepting a plain list too
  keeps it general.
- **B8 (optional, question 1) Titan Drop's lift**: a hero part that raises the hero by `TitanDropPath`'s height curve
  from 0.4 to 1.5 s (keys (0.4, 0, out 13.68889), (0.85, 2.8, 0.5142857 / 0.5142857), (1.2, 3, 0 / 0), (1.5, 0, in -20);
  `Bison.c:29824-30082`), in place horizontally; owned followPosition effects then ride the lifted hero (the dive),
  and the dive cue's spawn is at the hero's lifted position.

Shared changes asked (files I do not own): `FX_PART_FILES` gains `"tto_bison"`; B7 in index.html. Optional:
`SKILL_FX["bison"]` in `wardrobe_fx_tto.py` (not needed: `cue_tto` builds every `tto/` name the cue file holds).

## 5. Probed on this PC (2026-11-13, TTO's 2026-11-04 bundles; BB's rip)

- `wardrobe_fx_tto.py bison --probe <21 names>` -> `probe.json` (17 TTO prefabs + TTO's copies of the 4 BB ones),
  `--probe unchained` -> `probe_unchained.json`; 32 materials, 21 textures, 16 effect sounds. EffectControl (life +
  afterLife; fP = followPosition, fS = followState): chains 0.62 + 0.05 fP fS; break 0.3 + 1.6; roar 1.0 + 1.2 fP; plant
  0.3 + 1.6; takeoff 0.3 + 1.4; mark 1.1 + 0.1; charge 1.1 + 0.45; dive 0.2 + 1.2 fP; slam1-3 1.2 + 1.6; magmaTick 0.4 +
  1.8; quakeTick 0.3 + 1.6; magmaField 6.0 + 1.5; quakeField 5.0 + 2.0; magmaSlam 1.5 + 1.3; quakeSlam 2.0 + 1.5;
  `unchained` none (lives until removed).
- Scripts: `Bison_row6Fx` x 4 (chains) + 2 (unchained); `Bison_c6Arc` in 13 prefabs (`scripts.txt`); `GroundConformParticles`
  on the six magmaQuake roots (radius 3 / 31 / 12 / 14, spacing 0.75-1.5, maxStep 6); `AudioControl` on all 18 sound
  nodes; GroundHugEmitter all Disc (shape 0), no motes, no resample (`groundhug.js` covers them).
- Shuriken: render modes 0 (38), 1 stretched (16), 4 mesh (17, inline meshes); shapes 0, 4, 10; two local-space systems
  (the charge's Rocks, the unchained Embers); one UVModule (magmaTick Pop, magmaField Bubbles). All supported by
  `shuriken.js`.
- Materials needing a shader: `tto_c6_energyArc` (TTO/Bison/EnergyArc, 12 prefabs), `tto_c6_moltenCrust`
  (TTO/Bison/MoltenCrust); `tto_Bomb2` is `Legacy Shaders/Particles/Multiply (Double)` (only in TTO's copy of
  calamityHammer_ring, which the cues don't use; if it were used, `SHADER_BLEND` would need the line mapping it to the
  page's `multiply2`). Opaque: `tto_c6_chainCopper` (untextured, colour (0.3, 0.16, 0.07)), `tto_mq_rock` (Plain_Rock).
- `wardrobe_fx.py bison --probe berserkerRush,berserkerRush_ring,calamityHammer_ring,earthSmasher_ring` ->
  `probe_bb.json`: berserkerRush (ImageEmitter + Ellipsoid legacy particles, no EffectControl), berserkerRush_ring (1.0 + 0,
  fP; RingEmitter + legacy), calamityHammer_ring (3 + 1, fP fS; its sound calamityHammer_ring), earthSmasher_ring (1 + 3, fP
  fS; its sound earthSmasher). All built kinds.
- Strings and calls: `strings_in.py 24ec270` (TTO's addStatus literals, `addStatus_all.txt`), `callers.py` (AddUnchainedFx /
  RemoveUnchainedFx call sites), `dis.py` (the Until floats, `titanDrop_movenext.asm`; GroundConformParticles), `trig.py`
  (cosf / sinf), `calc.py` (`calc.txt`, `bursts.json`), `cues.py` (`cues.json`, `cues_block.txt`: the block below, parsed;
  every `tto/` effect it names is in the probes).

## 6. Sounds and voices

| Cue | Kind | File | In BB's rip |
|---|---|---|---|
| Magma Quake axe, 0 s | voice | `voices/calamityHammer` | yes |
| Magma Quake hammer, 0 s | voice | `voices/earthSmasher1` / `2` (50 %) | yes |
| Magma Quake axe, 0.9 s | sound | `sounds/magmaClutter1` / `2` (50 %), volume 1.2 | yes |

Effect AudioSources (come with their effects): BB's recordings for holdCharge_ring, enrage, hammer_hit1 / 2, trample1,
overSwing, instantRush, earthSmasher, calamityHammer_ring (Bison `sounds/`) and armorBreak (BB has it as
`wolf/sounds/armorBreak`, which `rip_wav`'s "anywhere" search finds; TTO's default clips are BB's recordings, the
Penguin's finding); TTO's own (not in BB's rip, the exporter decodes them from the bundle): `break`, `MagmaPit` (loop),
`titanQuake_hit`, `titanQuake_ring` (loop), `gadina_planetBreaker`, `earthSmasher_ring`. No TTO-only **hero** sound,
so `SKILL_SOUNDS` needs no Bison entry.

## 7. The cue entries (ready to paste into `wardrobe/fx_cues/bison.json`)

Keys are the clip names (single tiles, no SEQ). `tto/` names are TTO prefabs (built by `wardrobe_fx_tto.py bison`),
plain names BB's (built by `wardrobe_fx.py bison`: berserkerRush, berserkerRush_ring, calamityHammer_ring,
earthSmasher_ring, the three voices, the two sounds). The `worn` / `notWorn` options with the set name `bisonHammer`
need B7: until then the page's `notWorn` check compares the slot's item with the string "bisonHammer" (never equal), so
the axe cues always play and the hammer cues' `worn` is ignored (both branches would play at once): **paste
`magmaQuakeAxe` after B7**, or paste the axe half alone (drop every cue with `worn`). Titan Drop is the in-place variant
(question 1). The block was generated and parsed by `checks/fx_bison_research/tto/cues.py` (the tick spots from
`calc.py`, metres, rounded to 1 cm).

```json
{
  "unchainedFury": {
    "why": "TTO1102:Bison.<RPC_unchainedFury>d__278::MoveNext@0x1B7BFC0 (pseudo/Bison.c:17596-17876; plans/fx_bison/tto.md 2.1): at the press TTO1102:Bison::UnchainedCleanse@0x1B48570 adds the 3 s status unchained (RPC_AddStatus 213, 1, 3), whose look is CharacterControl::AddUnchainedFx@0x24AEB60 (CharacterControl.c:5541-5643, called from <addStatus>d__481::MoveNext at 0x24FD6A6): the prefab unchained at the hero, parented, world scale 1, removed with the status (RemoveUnchainedFx@0x24C2920 from removeStatus at 0x24E8CDB; kill 3); 0: Row6Begin clip unchainedFury (:17652), unchainedFury_chains owned at the hero, hero rotation (:17673; EffectControl 0.62 + 0.05, followState: cut at Row6End 1.8); Waits 0.62 (:17677): unchainedFury_break at the hero, hero rotation, not owned (:17706), camera shake (left out), RPC_AddStatus(203 berserkerRush, max(level, Rage Control + 4) = 5 at max rank, chaAdjust(12)) (:17735): the status look as BB's CharacterControl.cs:34752-34942 (TTO's addStatus loads the same literals: effects/berserkerRush_ring at 0x24EDA65, effects/berserkerRush at 0x24ED4E9, berserkerRush1Fx / 2Fx on HandMount_L / HandMount_R): berserkerRush_ring at the hero, identity, InitEffectControl (:34876), and berserkerRush on each hand mount, localPosition 0 (:34888-34942), removed with the status (:15477-15510): 12 s x CHA, cut at 10 s (kill 10); Waits 0.33 = 0.95: unchainedFury_roar owned at the hero (:17770; its own sounds enrage); Waits 0.5 = 1.45: unchainedFury_plant at the hero + 2.6 flat-forward + 2.45 right, hero rotation, not owned (:17838-17848); Waits 0.35 = 1.8: Row6End (:17870); no Row6Voice / Row6Sound (every sound is a prefab's own AudioSource); one rank, nothing rolled; left out: the camera shakes (MagmaQuakeShake). Parts: Bison_row6Fx, Bison_c6Arc + TTO/Bison/EnergyArc, AudioControl (plans/fx_bison/tto.md section 4).",
    "cues": [
    [0, "fx", "tto/unchained", {"kill": 3}],
    [0, "fx", "tto/unchainedFury_chains", {"cut": 1.8}],
    [0.62, "fx", "tto/unchainedFury_break"],
    [0.62, "fx", "berserkerRush_ring"],
    [0.62, "fx", "berserkerRush", {"bone": "HandMount_L", "kill": 10}],
    [0.62, "fx", "berserkerRush", {"bone": "HandMount_R", "kill": 10}],
    [0.95, "fx", "tto/unchainedFury_roar"],
    [1.45, "fx", "tto/unchainedFury_plant", {"x": 2.45, "d": 2.6}]
    ]
  },
  "titanDrop": {
    "why": "TTO1102:Bison.<RPC_titanDrop>d__281::MoveNext@0x1B78BD0 (pseudo/Bison.c:15885-16338; plans/fx_bison/tto.md 2.2), the target point 10 m ahead, in place (the Penguin's decision 8 / the Wolf's Feral Strike: the page's hero does not travel): land = 0.26 m left of the line, 3.9 m short of the target (TitanDropHeadAhead / HeadRight :16024-16025), slamAt = land + 0.26 right + 3.9 ahead, so on the page the slam is 3.9 ahead, 0.26 right; 0: Row6Begin clip titanDrop (:16080); Until(start + 0.4) (capstone 0x1B79A62: f=0.4): titanDrop_takeoff at the start spot, faceRot (:16155), titanDrop_mark at slamAt, faceRot (:16160; Destroy at the landing :16204: kill 1.1), TitanDropCharge@0x1B46C50: titanDrop_charge at HandMount_R, ridden (RideWeapon@0x1B45710: parent, localPosition 0, localRotation identity, world scale 1; :30113-30147); first frame >= 1.2 s (:16245): titanDrop_dive owned at the airborne hero, LookRotation(land - pos) (:16275) = 47.5 deg down, 2.4 deg left at TitanDropPath@0x1B47610's 1.2 s (height key 3.0, along key 0.55; checks/fx_bison_research/tto/calc.py); 1.5: the hero set on land, the mark destroyed, TitanDropRings@0x1B47C60 (:16210): <TitanDropRings>d__289::MoveNext@0x1BA91D0 (:18540-18664) spawns \"titanDrop_slam\" + (i + 1) at slamAt, faceRot (:18584-18593) at Until(start + TitanDropRingAt[i]) = 1.5 / 1.9 / 2.3 (.cctor :30656: [1.5, 1.9, 2.3]); Until(start + 2.0) (capstone 0x1B79292: f=2): Row6End (:16329); the cues after 2.0 s run on in the idle tail; no Row6Voice / Row6Sound (the prefabs' own AudioSources); the hits and KO waves land on foes (no prefab); left out: the camera zoom and shakes. Parts: Bison_c6Arc + TTO/Bison/EnergyArc, AudioControl; optional the hero's lift (tto.md question 1).",
    "cues": [
    [0.4, "fx", "tto/titanDrop_takeoff"],
    [0.4, "fx", "tto/titanDrop_mark", {"x": 0.26, "d": 3.9, "kill": 1.1}],
    [0.4, "fx", "tto/titanDrop_charge", {"bone": "HandMount_R"}],
    [1.2, "fx", "tto/titanDrop_dive", {"rot": [47.5, -2.4, 0]}],
    [1.5, "fx", "tto/titanDrop_slam1", {"x": 0.26, "d": 3.9}],
    [1.9, "fx", "tto/titanDrop_slam2", {"x": 0.26, "d": 3.9}],
    [2.3, "fx", "tto/titanDrop_slam3", {"x": 0.26, "d": 3.9}]
    ]
  },
  "magmaQuakeAxe": {
    "why": "TTO1102:Bison.<RPC_magmaQuake>d__234::MoveNext@0x1B69E50 (pseudo/Bison.c:7634-7843; plans/fx_bison/tto.md 2.3); the weapon picks the branch: hammer = TTO1102:Bison::isHammer@0x1B4EF30's 24 codes (the item set bisonHammer: wardrobe/data/item_map.json's props for them), else the axe; 0: Row6Begin clip magmaQuakeAxe for both (:7688), Row6Voice@0x1B467B0 (:7702; voices/): axe calamityHammer, hammer earthSmasher1|earthSmasher2 (Random.Range(0, 2)), Row6Spawn owned at the hero, hero rotation (:7720): axe calamityHammer_ring, hammer earthSmasher_ring (BB's prefabs; followState: cut at Row6End 2.2); Waits 0.43 (:7724): the tick look (axe magmaQuake_magmaTick, hammer magmaQuake_quakeTick) at MagmaQuakeAt(MagmaButt) = the hero + 0.8 right + 1.3 flat-forward, on the ground (.cctor :30656: (0.8, 0, 1.3); MagmaQuakeAt@0x1B41160), identity (:7746-7759); Waits 0.47 = 0.9 (:7770): centre = MagmaQuakeAt(MagmaCenter (-0.45, 0, 0)) = 0.45 left (:7787), MagmaQuakeImpact@0x1B41710 (:7792): axe magmaQuake_magmaSlam at the centre, identity (:28777) + sounds/ magmaClutter1|magmaClutter2 (Random.Range(0, 2) == 0 = 1, :28778) at PlayOneShot volume 1.2 (:28797), hammer magmaQuake_quakeSlam at the centre (:28815); the field at the centre, identity (:7807): axe magmaQuake_magmaField (EffectControl 6 + 1.5), hammer magmaQuake_quakeField (5 + 2); MagmaQuakeTicks@0x1B41CB0 (:7816) = <MagmaQuakeTicks>d__239::MoveNext@0x1B5C3A0 (:1-139): Waits 0.5 before each tick, RoundToInt(2 x life) = 12 (axe) / 10 (hammer) ticks at 1.4 ... 6.9 / 5.9 s, each 12 tick looks at the ground at centre + (cos a, 0, sin a) x sqrt(u1) x 30, a = u2 x 2 pi (:38-113; FUN_180308640 = cosf, FUN_180308bd0 = sinf, checks/fx_bison_research/tto/trig.py) from System.Random(RoundToInt(z x 50) x 0x127409f ^ RoundToInt(x x 50) x 0x466f45d) of the cast position (:7813) = Random(0) for a Bison at the origin (calc.py: the game's own spots for that cast); Waits 1.3 = 2.2: Row6End (:7837); the cues after 2.2 s run on in the idle tail; left out: the camera shakes (MagmaQuakeShake, QuakeRumbling@0x1B42370: 1 every 0.1 s for 5 s), the hits (MagmaQuakeHit: no prefab). Parts: GroundConformParticles (a no-op on a flat floor), Bison_c6Arc + TTO/Bison/EnergyArc, TTO/Bison/MoltenCrust, AudioControl (the two looping beds MagmaPit / titanQuake_ring fade out), cue option worn / notWorn with an item set (tto.md section 4).",
    "cues": [
    [0, "voice", "calamityHammer", {"notWorn": ["R", "bisonHammer"]}],
    [0, "fx", "calamityHammer_ring", {"cut": 2.2, "notWorn": ["R", "bisonHammer"]}],
    [0.43, "fx", "tto/magmaQuake_magmaTick", {"x": 0.8, "d": 1.3, "notWorn": ["R", "bisonHammer"]}],
    [0.9, "fx", "tto/magmaQuake_magmaSlam", {"x": -0.45, "notWorn": ["R", "bisonHammer"]}],
    [0.9, "sound", "magmaClutter1|magmaClutter2", {"vol": 1.2, "notWorn": ["R", "bisonHammer"]}],
    [0.9, "fx", "tto/magmaQuake_magmaField", {"x": -0.45, "notWorn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_magmaTick", {"x": 10.05, "d": -23.31, "notWorn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_magmaTick", {"x": -25.01, "d": -9.4, "notWorn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_magmaTick", {"x": -13.15, "d": -4.92, "notWorn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_magmaTick", {"x": -27.14, "d": 10.15, "notWorn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_magmaTick", {"x": -4.85, "d": 29.33, "notWorn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_magmaTick", {"x": -16.32, "d": 3.31, "notWorn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_magmaTick", {"x": -23.88, "d": 4.54, "notWorn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_magmaTick", {"x": 28.74, "d": 5.64, "notWorn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_magmaTick", {"x": 27.4, "d": -0.81, "notWorn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_magmaTick", {"x": -10.2, "d": 22.68, "notWorn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_magmaTick", {"x": 15.22, "d": -22.13, "notWorn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_magmaTick", {"x": 28.8, "d": 6.08, "notWorn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_magmaTick", {"x": -25.21, "d": -4.13, "notWorn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_magmaTick", {"x": -11.53, "d": -26.79, "notWorn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_magmaTick", {"x": 18.92, "d": 10.82, "notWorn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_magmaTick", {"x": -12.87, "d": 3.75, "notWorn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_magmaTick", {"x": 15.86, "d": -1.18, "notWorn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_magmaTick", {"x": 1.51, "d": -23.97, "notWorn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_magmaTick", {"x": -4.29, "d": 3.56, "notWorn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_magmaTick", {"x": 16.5, "d": -4.64, "notWorn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_magmaTick", {"x": -4.97, "d": -20.84, "notWorn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_magmaTick", {"x": -1.97, "d": 10.23, "notWorn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_magmaTick", {"x": 7.48, "d": -27.45, "notWorn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_magmaTick", {"x": -17.24, "d": 4.63, "notWorn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_magmaTick", {"x": 1.61, "d": 11.31, "notWorn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_magmaTick", {"x": -4.2, "d": -18.84, "notWorn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_magmaTick", {"x": -24.0, "d": 1.78, "notWorn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_magmaTick", {"x": 9.1, "d": -9.18, "notWorn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_magmaTick", {"x": -2.95, "d": -27.14, "notWorn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_magmaTick", {"x": -12.32, "d": -25.13, "notWorn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_magmaTick", {"x": 4.23, "d": 23.25, "notWorn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_magmaTick", {"x": 22.14, "d": -17.2, "notWorn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_magmaTick", {"x": 4.21, "d": -7.5, "notWorn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_magmaTick", {"x": -8.09, "d": -9.74, "notWorn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_magmaTick", {"x": 4.8, "d": 26.77, "notWorn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_magmaTick", {"x": -30.24, "d": 3.5, "notWorn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_magmaTick", {"x": -5.03, "d": -23.79, "notWorn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_magmaTick", {"x": 21.29, "d": 15.99, "notWorn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_magmaTick", {"x": -5.49, "d": -25.11, "notWorn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_magmaTick", {"x": 8.35, "d": -5.96, "notWorn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_magmaTick", {"x": -13.36, "d": 1.89, "notWorn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_magmaTick", {"x": -10.53, "d": 19.63, "notWorn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_magmaTick", {"x": -24.54, "d": 4.85, "notWorn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_magmaTick", {"x": 9.5, "d": -25.52, "notWorn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_magmaTick", {"x": 1.98, "d": -26.61, "notWorn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_magmaTick", {"x": -8.55, "d": 27.89, "notWorn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_magmaTick", {"x": -11.68, "d": -18.56, "notWorn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_magmaTick", {"x": -4.41, "d": 16.84, "notWorn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_magmaTick", {"x": 4.22, "d": 26.77, "notWorn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_magmaTick", {"x": 11.34, "d": 5.41, "notWorn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_magmaTick", {"x": -8.75, "d": -22.21, "notWorn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_magmaTick", {"x": 20.95, "d": -10.46, "notWorn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_magmaTick", {"x": 12.27, "d": -6.11, "notWorn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_magmaTick", {"x": 5.81, "d": -4.54, "notWorn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_magmaTick", {"x": 20.08, "d": 13.76, "notWorn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_magmaTick", {"x": 8.61, "d": 7.21, "notWorn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_magmaTick", {"x": 21.97, "d": -6.81, "notWorn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_magmaTick", {"x": 12.11, "d": 16.85, "notWorn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_magmaTick", {"x": -22.8, "d": -10.5, "notWorn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_magmaTick", {"x": -10.94, "d": -9.63, "notWorn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_magmaTick", {"x": -1.82, "d": 1.64, "notWorn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_magmaTick", {"x": 25.12, "d": 10.56, "notWorn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_magmaTick", {"x": -4.89, "d": -15.29, "notWorn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_magmaTick", {"x": 28.85, "d": -2.06, "notWorn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_magmaTick", {"x": -18.93, "d": -2.66, "notWorn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_magmaTick", {"x": -16.32, "d": -0.66, "notWorn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_magmaTick", {"x": 20.03, "d": 7.67, "notWorn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_magmaTick", {"x": -16.34, "d": 0.39, "notWorn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_magmaTick", {"x": -21.36, "d": -18.01, "notWorn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_magmaTick", {"x": -0.92, "d": -9.67, "notWorn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_magmaTick", {"x": 16.93, "d": -7.73, "notWorn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_magmaTick", {"x": -3.82, "d": -10.31, "notWorn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_magmaTick", {"x": 10.96, "d": -20.58, "notWorn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_magmaTick", {"x": -22.94, "d": -10.54, "notWorn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_magmaTick", {"x": 4.54, "d": 11.43, "notWorn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_magmaTick", {"x": -0.56, "d": 23.41, "notWorn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_magmaTick", {"x": -27.66, "d": -12.53, "notWorn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_magmaTick", {"x": -1.1, "d": 7.53, "notWorn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_magmaTick", {"x": -25.51, "d": -11.42, "notWorn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_magmaTick", {"x": -24.43, "d": -2.48, "notWorn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_magmaTick", {"x": 25.65, "d": 13.86, "notWorn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_magmaTick", {"x": 11.54, "d": 17.83, "notWorn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_magmaTick", {"x": -17.37, "d": -21.12, "notWorn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_magmaTick", {"x": -21.96, "d": -7.42, "notWorn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_magmaTick", {"x": 24.14, "d": -0.84, "notWorn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_magmaTick", {"x": 14.69, "d": 6.49, "notWorn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_magmaTick", {"x": -20.81, "d": 2.17, "notWorn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_magmaTick", {"x": 12.11, "d": 6.07, "notWorn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_magmaTick", {"x": 7.95, "d": 11.69, "notWorn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_magmaTick", {"x": -19.57, "d": 6.07, "notWorn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_magmaTick", {"x": -3.69, "d": 2.72, "notWorn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_magmaTick", {"x": 7.5, "d": 25.91, "notWorn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_magmaTick", {"x": 27.73, "d": 5.3, "notWorn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_magmaTick", {"x": 20.38, "d": -4.95, "notWorn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_magmaTick", {"x": 29.29, "d": 3.16, "notWorn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_magmaTick", {"x": -4.74, "d": 23.87, "notWorn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_magmaTick", {"x": -25.58, "d": -15.46, "notWorn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_magmaTick", {"x": -12.3, "d": 23.55, "notWorn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_magmaTick", {"x": 18.76, "d": -3.05, "notWorn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_magmaTick", {"x": 27.38, "d": -4.79, "notWorn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_magmaTick", {"x": 9.77, "d": 11.19, "notWorn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_magmaTick", {"x": 11.94, "d": 25.58, "notWorn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_magmaTick", {"x": -27.54, "d": -7.81, "notWorn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_magmaTick", {"x": -26.93, "d": -2.34, "notWorn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_magmaTick", {"x": 17.33, "d": -0.92, "notWorn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_magmaTick", {"x": -2.41, "d": -5.12, "notWorn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_magmaTick", {"x": 3.09, "d": 9.82, "notWorn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_magmaTick", {"x": -18.89, "d": -10.33, "notWorn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_magmaTick", {"x": -6.13, "d": 14.26, "notWorn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_magmaTick", {"x": 2.69, "d": -14.43, "notWorn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_magmaTick", {"x": -8.77, "d": -7.11, "notWorn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_magmaTick", {"x": -12.99, "d": -18.61, "notWorn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_magmaTick", {"x": 16.88, "d": 2.56, "notWorn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_magmaTick", {"x": 6.29, "d": -6.49, "notWorn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_magmaTick", {"x": 19.25, "d": -15.86, "notWorn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_magmaTick", {"x": -1.26, "d": 24.2, "notWorn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_magmaTick", {"x": -15.68, "d": 2.51, "notWorn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_magmaTick", {"x": 9.65, "d": -8.62, "notWorn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_magmaTick", {"x": -14.08, "d": -16.02, "notWorn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_magmaTick", {"x": -11.98, "d": 12.44, "notWorn": ["R", "bisonHammer"]}],
    [6.4, "fx", "tto/magmaQuake_magmaTick", {"x": 14.38, "d": -0.43, "notWorn": ["R", "bisonHammer"]}],
    [6.4, "fx", "tto/magmaQuake_magmaTick", {"x": 22.99, "d": 0.27, "notWorn": ["R", "bisonHammer"]}],
    [6.4, "fx", "tto/magmaQuake_magmaTick", {"x": 28.45, "d": -7.07, "notWorn": ["R", "bisonHammer"]}],
    [6.4, "fx", "tto/magmaQuake_magmaTick", {"x": 1.21, "d": -11.78, "notWorn": ["R", "bisonHammer"]}],
    [6.4, "fx", "tto/magmaQuake_magmaTick", {"x": 2.84, "d": 8.45, "notWorn": ["R", "bisonHammer"]}],
    [6.4, "fx", "tto/magmaQuake_magmaTick", {"x": 5.33, "d": 4.78, "notWorn": ["R", "bisonHammer"]}],
    [6.4, "fx", "tto/magmaQuake_magmaTick", {"x": 20.14, "d": 15.34, "notWorn": ["R", "bisonHammer"]}],
    [6.4, "fx", "tto/magmaQuake_magmaTick", {"x": -17.62, "d": -21.47, "notWorn": ["R", "bisonHammer"]}],
    [6.4, "fx", "tto/magmaQuake_magmaTick", {"x": 0.74, "d": 22.68, "notWorn": ["R", "bisonHammer"]}],
    [6.4, "fx", "tto/magmaQuake_magmaTick", {"x": 16.99, "d": -21.2, "notWorn": ["R", "bisonHammer"]}],
    [6.4, "fx", "tto/magmaQuake_magmaTick", {"x": 16.3, "d": -11.06, "notWorn": ["R", "bisonHammer"]}],
    [6.4, "fx", "tto/magmaQuake_magmaTick", {"x": -26.5, "d": 6.65, "notWorn": ["R", "bisonHammer"]}],
    [6.9, "fx", "tto/magmaQuake_magmaTick", {"x": 2.63, "d": -17.23, "notWorn": ["R", "bisonHammer"]}],
    [6.9, "fx", "tto/magmaQuake_magmaTick", {"x": -12.25, "d": -15.65, "notWorn": ["R", "bisonHammer"]}],
    [6.9, "fx", "tto/magmaQuake_magmaTick", {"x": -23.68, "d": -18.96, "notWorn": ["R", "bisonHammer"]}],
    [6.9, "fx", "tto/magmaQuake_magmaTick", {"x": -6.85, "d": -6.31, "notWorn": ["R", "bisonHammer"]}],
    [6.9, "fx", "tto/magmaQuake_magmaTick", {"x": 20.42, "d": -21.36, "notWorn": ["R", "bisonHammer"]}],
    [6.9, "fx", "tto/magmaQuake_magmaTick", {"x": 13.85, "d": 16.77, "notWorn": ["R", "bisonHammer"]}],
    [6.9, "fx", "tto/magmaQuake_magmaTick", {"x": -1.7, "d": -0.47, "notWorn": ["R", "bisonHammer"]}],
    [6.9, "fx", "tto/magmaQuake_magmaTick", {"x": -18.3, "d": 16.92, "notWorn": ["R", "bisonHammer"]}],
    [6.9, "fx", "tto/magmaQuake_magmaTick", {"x": -13.13, "d": 24.87, "notWorn": ["R", "bisonHammer"]}],
    [6.9, "fx", "tto/magmaQuake_magmaTick", {"x": -26.85, "d": -3.33, "notWorn": ["R", "bisonHammer"]}],
    [6.9, "fx", "tto/magmaQuake_magmaTick", {"x": -26.86, "d": -7.0, "notWorn": ["R", "bisonHammer"]}],
    [6.9, "fx", "tto/magmaQuake_magmaTick", {"x": 10.83, "d": 18.52, "notWorn": ["R", "bisonHammer"]}],
    [0, "voice", "earthSmasher1|earthSmasher2", {"worn": ["R", "bisonHammer"]}],
    [0, "fx", "earthSmasher_ring", {"cut": 2.2, "worn": ["R", "bisonHammer"]}],
    [0.43, "fx", "tto/magmaQuake_quakeTick", {"x": 0.8, "d": 1.3, "worn": ["R", "bisonHammer"]}],
    [0.9, "fx", "tto/magmaQuake_quakeSlam", {"x": -0.45, "worn": ["R", "bisonHammer"]}],
    [0.9, "fx", "tto/magmaQuake_quakeField", {"x": -0.45, "worn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_quakeTick", {"x": 10.05, "d": -23.31, "worn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_quakeTick", {"x": -25.01, "d": -9.4, "worn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_quakeTick", {"x": -13.15, "d": -4.92, "worn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_quakeTick", {"x": -27.14, "d": 10.15, "worn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_quakeTick", {"x": -4.85, "d": 29.33, "worn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_quakeTick", {"x": -16.32, "d": 3.31, "worn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_quakeTick", {"x": -23.88, "d": 4.54, "worn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_quakeTick", {"x": 28.74, "d": 5.64, "worn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_quakeTick", {"x": 27.4, "d": -0.81, "worn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_quakeTick", {"x": -10.2, "d": 22.68, "worn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_quakeTick", {"x": 15.22, "d": -22.13, "worn": ["R", "bisonHammer"]}],
    [1.4, "fx", "tto/magmaQuake_quakeTick", {"x": 28.8, "d": 6.08, "worn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_quakeTick", {"x": -25.21, "d": -4.13, "worn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_quakeTick", {"x": -11.53, "d": -26.79, "worn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_quakeTick", {"x": 18.92, "d": 10.82, "worn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_quakeTick", {"x": -12.87, "d": 3.75, "worn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_quakeTick", {"x": 15.86, "d": -1.18, "worn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_quakeTick", {"x": 1.51, "d": -23.97, "worn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_quakeTick", {"x": -4.29, "d": 3.56, "worn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_quakeTick", {"x": 16.5, "d": -4.64, "worn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_quakeTick", {"x": -4.97, "d": -20.84, "worn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_quakeTick", {"x": -1.97, "d": 10.23, "worn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_quakeTick", {"x": 7.48, "d": -27.45, "worn": ["R", "bisonHammer"]}],
    [1.9, "fx", "tto/magmaQuake_quakeTick", {"x": -17.24, "d": 4.63, "worn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_quakeTick", {"x": 1.61, "d": 11.31, "worn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_quakeTick", {"x": -4.2, "d": -18.84, "worn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_quakeTick", {"x": -24.0, "d": 1.78, "worn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_quakeTick", {"x": 9.1, "d": -9.18, "worn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_quakeTick", {"x": -2.95, "d": -27.14, "worn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_quakeTick", {"x": -12.32, "d": -25.13, "worn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_quakeTick", {"x": 4.23, "d": 23.25, "worn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_quakeTick", {"x": 22.14, "d": -17.2, "worn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_quakeTick", {"x": 4.21, "d": -7.5, "worn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_quakeTick", {"x": -8.09, "d": -9.74, "worn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_quakeTick", {"x": 4.8, "d": 26.77, "worn": ["R", "bisonHammer"]}],
    [2.4, "fx", "tto/magmaQuake_quakeTick", {"x": -30.24, "d": 3.5, "worn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_quakeTick", {"x": -5.03, "d": -23.79, "worn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_quakeTick", {"x": 21.29, "d": 15.99, "worn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_quakeTick", {"x": -5.49, "d": -25.11, "worn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_quakeTick", {"x": 8.35, "d": -5.96, "worn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_quakeTick", {"x": -13.36, "d": 1.89, "worn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_quakeTick", {"x": -10.53, "d": 19.63, "worn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_quakeTick", {"x": -24.54, "d": 4.85, "worn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_quakeTick", {"x": 9.5, "d": -25.52, "worn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_quakeTick", {"x": 1.98, "d": -26.61, "worn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_quakeTick", {"x": -8.55, "d": 27.89, "worn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_quakeTick", {"x": -11.68, "d": -18.56, "worn": ["R", "bisonHammer"]}],
    [2.9, "fx", "tto/magmaQuake_quakeTick", {"x": -4.41, "d": 16.84, "worn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_quakeTick", {"x": 4.22, "d": 26.77, "worn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_quakeTick", {"x": 11.34, "d": 5.41, "worn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_quakeTick", {"x": -8.75, "d": -22.21, "worn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_quakeTick", {"x": 20.95, "d": -10.46, "worn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_quakeTick", {"x": 12.27, "d": -6.11, "worn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_quakeTick", {"x": 5.81, "d": -4.54, "worn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_quakeTick", {"x": 20.08, "d": 13.76, "worn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_quakeTick", {"x": 8.61, "d": 7.21, "worn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_quakeTick", {"x": 21.97, "d": -6.81, "worn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_quakeTick", {"x": 12.11, "d": 16.85, "worn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_quakeTick", {"x": -22.8, "d": -10.5, "worn": ["R", "bisonHammer"]}],
    [3.4, "fx", "tto/magmaQuake_quakeTick", {"x": -10.94, "d": -9.63, "worn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_quakeTick", {"x": -1.82, "d": 1.64, "worn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_quakeTick", {"x": 25.12, "d": 10.56, "worn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_quakeTick", {"x": -4.89, "d": -15.29, "worn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_quakeTick", {"x": 28.85, "d": -2.06, "worn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_quakeTick", {"x": -18.93, "d": -2.66, "worn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_quakeTick", {"x": -16.32, "d": -0.66, "worn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_quakeTick", {"x": 20.03, "d": 7.67, "worn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_quakeTick", {"x": -16.34, "d": 0.39, "worn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_quakeTick", {"x": -21.36, "d": -18.01, "worn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_quakeTick", {"x": -0.92, "d": -9.67, "worn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_quakeTick", {"x": 16.93, "d": -7.73, "worn": ["R", "bisonHammer"]}],
    [3.9, "fx", "tto/magmaQuake_quakeTick", {"x": -3.82, "d": -10.31, "worn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_quakeTick", {"x": 10.96, "d": -20.58, "worn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_quakeTick", {"x": -22.94, "d": -10.54, "worn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_quakeTick", {"x": 4.54, "d": 11.43, "worn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_quakeTick", {"x": -0.56, "d": 23.41, "worn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_quakeTick", {"x": -27.66, "d": -12.53, "worn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_quakeTick", {"x": -1.1, "d": 7.53, "worn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_quakeTick", {"x": -25.51, "d": -11.42, "worn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_quakeTick", {"x": -24.43, "d": -2.48, "worn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_quakeTick", {"x": 25.65, "d": 13.86, "worn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_quakeTick", {"x": 11.54, "d": 17.83, "worn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_quakeTick", {"x": -17.37, "d": -21.12, "worn": ["R", "bisonHammer"]}],
    [4.4, "fx", "tto/magmaQuake_quakeTick", {"x": -21.96, "d": -7.42, "worn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_quakeTick", {"x": 24.14, "d": -0.84, "worn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_quakeTick", {"x": 14.69, "d": 6.49, "worn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_quakeTick", {"x": -20.81, "d": 2.17, "worn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_quakeTick", {"x": 12.11, "d": 6.07, "worn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_quakeTick", {"x": 7.95, "d": 11.69, "worn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_quakeTick", {"x": -19.57, "d": 6.07, "worn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_quakeTick", {"x": -3.69, "d": 2.72, "worn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_quakeTick", {"x": 7.5, "d": 25.91, "worn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_quakeTick", {"x": 27.73, "d": 5.3, "worn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_quakeTick", {"x": 20.38, "d": -4.95, "worn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_quakeTick", {"x": 29.29, "d": 3.16, "worn": ["R", "bisonHammer"]}],
    [4.9, "fx", "tto/magmaQuake_quakeTick", {"x": -4.74, "d": 23.87, "worn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_quakeTick", {"x": -25.58, "d": -15.46, "worn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_quakeTick", {"x": -12.3, "d": 23.55, "worn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_quakeTick", {"x": 18.76, "d": -3.05, "worn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_quakeTick", {"x": 27.38, "d": -4.79, "worn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_quakeTick", {"x": 9.77, "d": 11.19, "worn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_quakeTick", {"x": 11.94, "d": 25.58, "worn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_quakeTick", {"x": -27.54, "d": -7.81, "worn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_quakeTick", {"x": -26.93, "d": -2.34, "worn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_quakeTick", {"x": 17.33, "d": -0.92, "worn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_quakeTick", {"x": -2.41, "d": -5.12, "worn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_quakeTick", {"x": 3.09, "d": 9.82, "worn": ["R", "bisonHammer"]}],
    [5.4, "fx", "tto/magmaQuake_quakeTick", {"x": -18.89, "d": -10.33, "worn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_quakeTick", {"x": -6.13, "d": 14.26, "worn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_quakeTick", {"x": 2.69, "d": -14.43, "worn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_quakeTick", {"x": -8.77, "d": -7.11, "worn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_quakeTick", {"x": -12.99, "d": -18.61, "worn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_quakeTick", {"x": 16.88, "d": 2.56, "worn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_quakeTick", {"x": 6.29, "d": -6.49, "worn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_quakeTick", {"x": 19.25, "d": -15.86, "worn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_quakeTick", {"x": -1.26, "d": 24.2, "worn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_quakeTick", {"x": -15.68, "d": 2.51, "worn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_quakeTick", {"x": 9.65, "d": -8.62, "worn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_quakeTick", {"x": -14.08, "d": -16.02, "worn": ["R", "bisonHammer"]}],
    [5.9, "fx", "tto/magmaQuake_quakeTick", {"x": -11.98, "d": 12.44, "worn": ["R", "bisonHammer"]}]
    ]
  }
}
```

Notes on the block:
- `tto/unchained` is the status look (3 s); `berserkerRush` / `berserkerRush_ring` the Berserker Rush status look (BB's
  prefabs, as the Sheep's TTO skills use BB's `returnCast`). `bone` parents to the Bison rig's `HandMount_L` /
  `HandMount_R` (both in `wardrobe/data/bison/rig.json`).
- `titanDrop_charge` on `HandMount_R`: RideWeapon also sets localScale 1 / the mount's lossyScale (world scale 1); the
  page's `bone` option sets localPosition 0 and localRotation identity only. `HandMount_R`'s local scale is 1 in
  `rig.json`; its parents decide the lossy scale: check the flame's size by eye (QA).
- The two BB rings keep `cut 2.2` (followState, Row6End); `calamityHammer_ring`'s 3 s life is cut there as in the game.
- Every tick spot cue has its weapon option; the 0.43 s butt look uses the tick prefab of its branch.

## 8. Open questions (each with my recommended answer)

1. **Titan Drop's flight.** The game lifts the Bison 3 m along `TitanDropPath` (0.4-1.5 s) and moves it 6.1 m forward;
   the clip has no lift (Read this first 6). Options: (A) in place, no mover (the block as written; the Bison hangs in
   its leap pose on the ground for ~1 s); (B) the full path, forward travel included (the hero ends 6.1 m ahead, then
   snaps back when the tile ends); (C) the height only, in place (part B8). **Recommend C**: the leap is the skill's
   look, and C keeps decision 8's "no travel" (the slam stays 3.9 m ahead, the dive rides the hero down). If C is
   built, the block needs no change except the dive keeps its rotation and spawns at the lifted hero.
2. **Magma Quake's weapon.** The game picks axe / hammer by the held weapon. **Recommend: follow the worn weapon**
   (B7, the `bisonHammer` set), as the Penguin's Staff of Time (decision 18); one tile, its look changing with the
   weapon. Alternative: two tiles (axe, hammer) — against "one tile per skill".
3. **Magma Quake's tick spots.** **Recommend the game's own spots for a Bison at the origin** (seed 0, fixed: the block),
   which is what the game draws for that cast; the pattern is the same on every play, as it is in the game for one
   spot. Alternative: a fresh pattern each play (a new cue option, e.g. `disc: 30` = a uniform point of a 30 m disc
   drawn when the clip starts, with the game's sqrt / angle formula), closer to "the game varies it" but not to any one
   cast.
4. **Magma Quake's far spots.** 91 % of the tick looks fall farther than 10 m (radius 30). **Recommend: keep all**
   (they are the skill's reach; the field's own pool is 30 m); flag the cost for QA (144 tick effects x 5 Shuriken
   systems over 6 s, plus the field's 11 ground discs of 30 m).
5. **The Berserker Rush passive on the HP payment** (Unchained Fury pays HP through `ApplyDamage`, which can roll the
   passive's `4 x level` % x LCK on that frame and show the berserkerRush look at 0 s). **Recommend: leave out**: the
   skill's own grant 0.62 s later shows the same look, and a 16 % chance to see it 0.62 s earlier is not worth a roll.
6. **BB's or TTO's copy of the four BB prefabs** (TTO ships its own conversions: Shuriken instead of legacy emitters,
   and `calamityHammer_ring` with a `Multiply (Double)` material). **Recommend BB's** (the rip, "ready", the precedent of
   every class so far); TTO's copies are TTO's port of the same effects.
7. **AudioControl** (B5). **Recommend: build it**: it is what cuts TTO's one-shots to their effects and fades the two
   looping beds; without it MagmaPit and titanQuake_ring play at full volume until the field is destroyed.

## 9. For the Bible (offer to the user; that repo's own rules)

- **Unchained Fury's looks** (`bison-skill-reference.md` "Unchained Fury"): the `unchained` status has its own look,
  `CharacterControl::AddUnchainedFx@0x24AEB60` (the prefab `effects/unchained` on the Bison for the status's 3 s,
  removed by `RemoveUnchainedFx@0x24C2920`); the timeline's effects: chains at 0 s (`unchainedFury_chains`), the break
  at 0.62 s (`unchainedFury_break`, with the Berserker Rush ring and hand fires), the roar at 0.95 s, the plant 2.6 m
  ahead and 2.45 m right at 1.45 s. Neither Unchained Fury nor Titan Drop plays a voice or a hero sound.
- **Titan Drop's effects**: takeoff at the start spot and the mark on the hit centre at 0.4 s, the charge flame riding
  `HandMount_R` from 0.4 s, the dive streak at 1.2 s (aimed at the landing), the three slam looks `titanDrop_slam1..3`
  with the rings at 1.5 / 1.9 / 2.3 s; the mark is removed at the landing.
- **Magma Quake**: the 0.43 s weapon-butt FX is the tick look at `MagmaButt` (0.8 m right, 1.3 m ahead); the axe's
  impact also plays `magmaClutter1|2` at volume 1.2 (the Bible lists MagmaQuakeImpact as camera / FX only); voices at the
  press (axe `calamityHammer`, hammer `earthSmasher1|2`); each tick draws 12 looks at uniform random points of the
  30 m disc (radius sqrt(u) x 30), seeded with the cast position, so one cast spot always gives the same pattern.

## Verification

Read-only check, 2026-11-13 (home PC): TTO1102 pseudo-C, `dump.cs` and capstone over `GameAssembly.dll`; BB
`DecompiledSource`; the probes in `checks/fx_bison_research/tto/`; the page (`wardrobe/index.html`). My own probes are in
`checks/fx_bison_research/verify_tto_parts/`. **Result: every time, name, random pick, position, owned flag and option in
the paste-ready block is correct. The block stays as it is.** The corrections below are to the prose only (sections 2.2,
4, 5, 6 and the notes in 7).

**Confirmed against the source**
- Unchained Fury (`<RPC_unchainedFury>d__278::MoveNext@0x1B7BFC0`): the waits are `Waits.Get` 0.62 / 0.33 / 0.5000001 /
  0.3499999, giving 0 / 0.62 / 0.95 / 1.45 / 1.8. Row6Spawn's 5th argument is 1 for the chains and the roar (owned) and 0
  for the break and the plant. The plant sits at pos + 2.6 x vFlat(forward) + 2.45 x right, matching `dump.cs`
  `UnchainedPlantAhead` / `UnchainedPlantRight`. `RPC_AddStatus(0xcb, max(level, getRageControlLv() + 4),
  chaAdjust(12))` runs only on the owner's client (`mChar+0x182`). The `unchained` status is `RPC_AddStatus(0xd5, 1, 3)` in
  `UnchainedCleanse@0x1B48570`. `AddUnchainedFx@0x24AEB60` instantiates at the hero's position and rotation, then
  SetParent (world position kept) and localScale 1 / lossyScale.
- Berserker Rush look, BB `CharacterControl.cs`: the ring at `:34876` (world identity, InitEffectControl); both
  `berserkerRush` copies at `:34888-34932` (parent `HandMount_L` / `HandMount_R` at `:34907` / `:34932`, localPosition 0,
  localScale one).
- Titan Drop (`<RPC_titanDrop>d__281::MoveNext@0x1B78BD0`):
  - `start` is read with `Time.time` right after Row6Begin. `titanDrop_movenext.asm` shows the `Until` floats 0.4
    (`0x1B79A62`) and 2.0 (`0x1B79292`).
  - right = Cross(up, dir), so land = mPos + dir x max(dist - 3.9, 0) - 0.26 right and slamAt = land + 0.26 right +
    3.9 dir, which is exactly the target.
  - The takeoff and the mark are not owned. The charge comes from `TitanDropCharge@0x1B46C50` at HandMount_R, not owned;
    `RideWeapon` sets the parent, localPosition 0, localRotation identity and localScale 1 / lossy.
  - The dive is spawned once, owned, at `1.2 <= now - start`, with LookRotation(land - pos).
  - The landing at start + 1.5 destroys only the mark.
  - The rings are `"titanDrop_slam" + (i + 1)` at `Until(start + TitanDropRingAt[i])`, and the `.cctor@0x1B48BD0` array
    gives 1.5 / 1.9 / 2.3.
  - `TitanDropPath@0x1B47610` keys: height (0.4, 0, out 13.68889), (0.85, 2.8), (1.2, 3), (1.5, 0, in -20); along (0.4, 0),
    (0.85, 0.38), (1.2, 0.55), (1.5, 1).
  - Recomputed dive rotation: pitch atan2(3, 2.7475) = 47.52 deg, yaw atan2(-0.117, 2.745) = -2.44 deg. So
    `rot [47.5, -2.4, 0]` holds.
- Magma Quake (`<RPC_magmaQuake>d__234::MoveNext@0x1B69E50`):
  - `hammer = tID & 1`. The voice is `Row6Voice(earthSmasher1, earthSmasher2)` for the hammer and `(calamityHammer,
    null)` for the axe. The ring is owned.
  - The waits are 0.43 / 0.47 / 1.3.
  - `MagmaButt` (0.8, 0, 1.3) and `MagmaCenter` (-0.45, 0, 0) come from the `.cctor`'s raw words 0x3f4ccccd / 0x3fa66666 /
    0xbee66666.
  - `MagmaQuakeImpact@0x1B41710`: the axe branch picks `Random.Range(0, 2)` from the `sounds/` folder and plays it with
    PlayOneShot at 1.2; the hammer branch has no sound. The field is not owned and has identity rotation.
  - The seed is `RoundToInt(z x 50) x 0x127409f ^ RoundToInt(x x 50) x 0x466f45d`, taken from the RPC's mPos.
  - `<MagmaQuakeTicks>d__239`: radius 0x41f00000 = 30, `RoundToInt(2 x life)` = 12 / 10 ticks, 12 bursts each, and
    `Waits.Get(0.5)` before each tick.
- `isHammer@0x1B4EF30` makes 24 `String.Equals` calls (exact matches, not Contains) on the same 24 codes. Through
  `item_map.json` `bison.weapon` they give exactly the 20 props listed: w_bsn50 / 51 are both royalHammer, w_bsn60 / 61
  both legendHammer, w_bsn62 = legendHammerR (not a prop), and w_bsn68 is unmapped. No other code maps to one of those 20.
  The remaining 27 props take the axe branch.
- **The tick spots, recomputed independently** (`verify_tto_parts/ticks.py`, a from-scratch .NET `System.Random`, Knuth
  subtractive). Its first draws are 0.7262432699679598 and 0.8173253595909687. All 144 axe and 120 hammer spots match the
  block to 1 cm, at the same times (1.4 ... 6.9 / 1.4 ... 5.9), and 13 / 9 of them lie within 10 m.
- Probes (`compact2.txt`, `scripts.txt`, `probe_unchained.json`): the lives, fP and fS are as listed. There are 18
  AudioControl nodes, and GroundConformParticles is on all 6 magmaQuake roots. In `clips.json` the clips are 1.8 / 2.0 /
  2.2 s, tto, group skill. The titanDrop Root track sits at z 0.965 from 0.6 to 1.3 s.
- The rip: `voices/calamityHammer`, `earthSmasher1` / `2` and `sounds/magmaClutter1` / `2` exist. MagmaPit,
  titanQuake_ring, titanQuake_hit, break, gadina_planetBreaker and earthSmasher_ring are not under `Resources`.
- The page: `cueOf` (index.html:4329-4346) takes d / x / y / rot / vol / cut / kill / bone, and `"sound"` is a cue kind.
  `notWorn` compares one string (`:4462`), so B7 is needed as the report says. The block parses as JSON.

**Corrections**
1. **AudioControl's delay (section 4 B5, 2.2, 6).** The report says `overSwing` "starts at +0.05 s" and
   `earthSmasher_ring` "at +0.2 s". That is wrong: in the game those two never sound.
   - `TTO1102:AudioControl::Start@0x2298D00` stops any source whose delay is above 0 (`set_playOnAwake(false)`, then
     `Stop`, at `0x2298E08-0x2298E18`).
   - `Update@0x2298E70` calls `Play` only inside the fade-in branch (`0x2298EA7-0x2298F62`: fadein > 0 and now < start +
     delay + fadein). With fadein 0 it jumps to the middle branch (`0x2298F69`), which only sets the volume. BB's
     `AudioControl.cs` Update does the same once its opaque predicates are worked out.
   - `Sound_overSwing` (titanDrop_takeoff) has delay 0.05 and fadein 0; `Sound_earthSmasher_ring` (titanDrop_slam2) has
     delay 0.2 and fadein 0 (`scripts.txt`).
   - So B5 gets one rule: **a source with a delay starts only inside its fade-in; delay > 0 with fadein 0 stays silent.**
   - The prose changes: in 2.2 the takeoff carries "trample1" (overSwing is silent) and `_slam2` carries "earthSmasher"
     (earthSmasher_ring is silent). Section 6's list of TTO-only sounds loses earthSmasher_ring, since it is never heard.
   - The disassembly is in `verify_tto_parts/audiocontrol_start.asm`, `audiocontrol_update.asm` and
     `audiocontrol_update2.asm`.
   - Also, "Every TTO prefab here carries one" is wrong: 13 of the 18 TTO prefabs do. titanDrop_mark, both tick looks,
     magmaQuake_magmaSlam and `unchained` have no sound node.
2. **Section 5:** the report says "`Bison_c6Arc` in 13 prefabs (`scripts.txt`)". `scripts.txt` has 11 such prefabs, with
   42 arcs: chains 2, break 4, roar 8, plant 2, takeoff 2, slam1-3 4 each, quakeField 6, magmaSlam 2, quakeSlam 4.
   `unchained` adds 2 more (`probe_unchained.json`), which makes **12** prefabs, the same as the material line's 12.
3. **B2, `repeat`:** `unchained`'s two Sweeps are **repeat true** (duration 0.9, diameter 3.6, colour (0.85, 0.09, 0.045,
   0.65), hug). Update@0x1B9BDF0 calls fmod (`FUN_18030c190`) when repeat is on. The rotation keeps the unwrapped t
   (angle + spin x t). Every other instance is repeat false.
4. **Section 7 note on titanDrop_charge:** no check by eye is needed. The page's `bone` keeps the world scale the effect
   was spawned with (index.html:3988), which matches RideWeapon's world scale 1. HandMount_R's lossy scale is 1 in
   `rig.json` anyway, since every parent has scale 1.
5. **Minor, rotations (no cue change).** BB instantiates the two `berserkerRush` copies at world identity and then sets
   `transform.parent`, which keeps the world rotation. Their local rotation is therefore the inverse of the mount's at that
   frame, not identity as the page's `bone` gives. `berserkerRush_ring` and every Magma Quake tick, slam and field are
   world identity in the game, while the page turns them by the hero's facing. These are round particle effects, so
   nothing visible changes.
6. **Minor:** the last tick looks end at 6.9 + 2.2 = 9.1 s (magmaTick 0.4 + 1.8), not at 6.9 s (section 9 of "Read this
   first").

**Open point for the decision (not a correction):** in place, the mark and the rings sit 3.9 m ahead, kept relative to
the landing by analogy with decision 8. In the game `slamAt` is exactly the target. The standing rule "effects on an enemy
go to the target point 10 m ahead" would put them at `d` 10 (and `x` 0) instead. Question 1's option B (the full path)
gives both at once: land 6.1 m ahead, slam at 10 m.

**Paste-ready block:** unchanged. Correction 1 changes the AudioControl part, not the cues.
