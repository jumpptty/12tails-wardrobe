# Mole effects + sounds research: the TTO-only clips (Barrel Railgun, Missile Pad, Kaiser Arsenal)

Scope: the six TTO clips of `wardrobe/data/mole/clips.json` (`tto: true`, group `skill`): `barrelRailgun1` (1.2 s),
`barrelRailgun2` (0.6 s, loop), `barrelRailgun3` (0.5 s), `barrelRailgun4` (0.5 s), `missilePad` (1.3 s), `kaiserArsenal`
(4.4 s). No BB code plays them. Research only: this file is the only file written in the repo, plus the probe scripts and
outputs in `checks/fx_mole_research/tto/` (git-ignored). Sources:
- TTO's pseudo-C `D:\12tails\DecompiledSource_TTO_2026-11-02\pseudo\Mole.c` and `pseudo_c6_extra\mole\{KingKaiser,
  MoleRailTurret, MoleRailgun, MoleRailBeam, MoleRailArc, MoleRailShock, MoleLaunchPad, KaiserWarhead}.c`, cited as
  `TTO1102:Method@RVA` plus `Mole.c:<line>` (or `KingKaiser.c:<line>`);
- capstone over `client\GameAssembly.dll` for the floats Ghidra drops (`dis.py`; `missile_movenext.asm`, `reticle.asm`);
  the Bible's `tools/usages.py`, imported read-only (`podlocks.py`, run with `-B`), for the one table no decompile has
  (KaiserArsenalPod's Locks);
- `fn.py` (a function printer, noise lines dropped) -> `rail_movenext.txt`, `rail_fire.txt`, `rail_end.txt`, `rail_hit.txt`,
  `rail_overload.txt`, `rail_helpers.txt`, `missile_movenext.txt`, `missile_fns.txt`, `missile_hit.txt`, `mole_missile.txt`,
  `locks.txt`, `arsenal_movenext.txt`, `arsenal_fns.txt`, `turret_fns.txt`, `turret_cctor.txt`, `Mole*.txt`, `KaiserWarhead.txt`;
- `steps.py` -> `steps.txt` (MoleRailTurret.Steps, the turret's 13-part assembly, decoded from the .cctor + the DLL);
- `missile_sim.py` -> `missile_sim.txt` (the 8 Missile flights to the 10 m target);
- the Bible's `12t_reference\mole-skill-reference.md` "TTO Lv 100 skills" (lines 712-773: War Area :718, Twin Warhead
  :734, Barrel Railgun :751);
- TTO's 2026-11-04 bundles (`D:\12tails-video\tto_assets\2026-11-04`) through
  `wardrobe_fx_tto.py mole --probe <26 names>` -> `probe.json` (`compact.py` -> `compact.txt`); `catalog.py` ->
  `catalog.txt` (every catalog address under `heroes/mole/` against BB's rip); `kaiser_tto.py` -> `kaiser_tto.txt` (the
  KingKaiser_b prefab's clip fields); BB's three reused prefabs through `wardrobe_fx.py mole --probe` -> `probe_bb.json`;
- `cues.py` (+ `why.py`) -> `cues_paste.json`: the paste-ready block of section 7, built from the numbers above and parsed.

Times are seconds from the start of the step (sequence) or clip the cue is keyed by. The Mole's TTO waits are
`Waits.Get(t)` (a cached WaitForSeconds: a step to add) and per-frame clocks against `Time.time` (the cast, the ride, the
turret): no `Until`. Max rank: Missile 4 with Twin Warhead (the only skill here with ranks); Barrel Railgun and Kaiser
Arsenal have one rank.

**Released list:** all six clips (`barrelRailgun1`, `barrelRailgun2`, `barrelRailgun3`, `barrelRailgun4`, `kaiserArsenal`,
`missilePad`) are in it (`wardrobe/tto_released.json:145-151`), so all get cues.

## Read this first

1. **Barrel Railgun's sequence is wrong in `index.html`.** Today's SEQ line (`index.html` SEQ.mole, line 1250 on 2026-11-13) is `barrelRailgun1
   barrelRailgun2*@6 barrelRailgun3@0.65 barrelRailgun4` (from the clip names). The code plays (section 2.1):
   - `assemble1` (fade 0.2) through `WarAreaBegin('barrelRailgun', dir, 'assemble1', 0.2)` (`Mole.c:2840`), then at 0.6 s
     `assemble2` looped, a cut (`:2960-2964`), through the fixed 6 s cast bar (`DisplayCastBar(6)`, `:2944`): **BB's
     Assemble clips**, while the turret builds itself in front of the Mole;
   - at 6.0 s `barrelRailgun1` (fade 0.1) **started at its 0.55 s** (`AnimationState.time = 0.55`, `:3020-3026`), the hop
     onto the seat, to its 1.2 s end (`:3100`): 0.65 s;
   - the ride: `barrelRailgun2` looped (fade 0.1, `:3142-3144`); each shot `barrelRailgun3` (fade 0.05) for 0.5 s, then
     `barrelRailgun2` again (fade 0.1) (`RPC_barrelRailgun_fire`, `:3919-3925`, `:3719`); shots at ride 2.2 + 2.4 k;
   - the end: `barrelRailgun4` (fade 0.05) (`RPC_barrelRailgun_end`, `:3490`), standby 0.5 s later (`:3596-3598`).

   The corrected SEQ line (section 7, shared change S1) needs one new page feature: a step that starts its clip at a time
   (`barrelRailgun1` from 0.55 s). The 0.05 s fades are today's syntax (`^0.05`, `SEQ_ALT` in `index.html`).
2. **Cue keys.** Barrel Railgun's cues sit on the sequence's own keys (Sheep decision 13): `@BarrelRailgun:assemble1`,
   `@BarrelRailgun:assemble2` (BB's Assemble tile keeps the plain `assemble1` / `assemble2`), and
   `@BarrelRailgun:barrelRailgun3` (played again on every shot step). A step's pending cues are dropped when the next step
   starts (`fxStart` replaces `FX.cues`, `index.html` fxStart), so whatever runs across steps (the turret's assembly and ride
   clock, the ground line, the charge tiers, the overload's three shocks 0.7-2.1 s after a 0.5 s shot step, the trench's
   2.4 s of sparks) belongs to the effect that lives across them: parts (section 6), as the Penguin's StarLines.
   `missilePad` and `kaiserArsenal` are single clips: plain keys.
3. **No voices except the Missile's.** `MissileVoice` (missile1 / missile2, `Random.Range(0, 2)`, voices/) is the only voice.
   Every other sound is the hero's `sounds/` clip through `Mole::RailSound@0x1C3C8E0` (`Mole.c:40503`, volume x 1 for the
   owner, 0.75 others) or `KingKaiser::TwinSound@0x1CB26A0` (the same folder), or a prefab's own AudioSource. All are in BB's
   rip (`sounds/`: assemble, teslaCoil, bazooka_fire, superTNT_hit, nAttack_hit, megaPunch_hit, missile_base, missile_fire)
   except two that live outside it (part P15): the lock `beep` (`Resources/sound/gui/beep.ogg`, an .ogg) and `kaiser_open`
   (the KingKaiser prefab's `kaiser_openFx`, `Assets/AudioClip/kaiser_open.wav`, outside Resources).
4. **TTO-only prefabs: 34 in the catalog, 25 in scope, all probed.** `catalog.txt`: 125 Mole effects, 34 not in BB's rip:
   15 `barrelRailgun*`, 6 `missile*` / `missilePad*`, `twinImpact`, 4 `kaiser*`, `barrelBot_warhead` (Barrel Bot's), 6
   `warArea_*` (War Area: no clip of its own, not in scope), 2 `warCapital_*warhead` (War Capital's). No arcana style. Three
   BB prefabs are reused: `assemble_box`, `assemble_dust`, `chopper_forwardDust`: cued as BB's rip copies (Bison decision
   43). `barrelRailgun` (the gun alone) is never spawned (the turret carries its own gun).
5. **Two unowned followState roots.** `barrelRailgun_blast` and `barrelRailgun_rip` (followPosition + followState) are bare
   `Instantiate`s (`Mole::RailFx@0x1C3B5D0`, `Mole.c:40348`: no `createEffect`, no owner), and EffectControl with
   followState and no owner jumps straight to its after-life on the first Update (`EffectControl.cs:194-210`; control.js's
   own comment for child nodes). The page treats every root as owned, so their cues carry `"cut"` = their own spawn time
   (question 6).
6. **Kaiser Arsenal is the King Kaiser's move**, not the Mole's: `KingKaiser.<RPC_kaiserArsenal>d__72` plays the TTO clip
   `GameAssets/characters/heroes/mole/animations/kaiserArsenal` (`KingKaiser.c:249`, `:313-319`) on the Kaiser's own rig
   (the clip's tracks: Root, Body, Lid, Chest_L / _R, Stomach, root_Ctrl ..., `clips.json`), and the pods hang on the Kaiser's
   Arm_R / Arm_L. The page plays the clip on the Mole. Question 4 (and `parts.md` question 8, part 11: the King Kaiser
   summon). Correction to `parts.md:469`: KingKaiser's code is decompiled, in `pseudo_c6_extra\mole\KingKaiser.c`
   (BUILD.md "pseudo_c6_extra"); only `KaiserArsenalPod` and `MoleLockReticle` were never decompiled (their RVAs are in
   `methods.tsv`; this report read their numbers with capstone and usages.py).
7. **Missile with Twin Warhead.** `missilePad` plays only when Twin Warhead (#453) is learned (`get_HasMissileBot`;
   otherwise `OldMissile` and BB's clip `missile`, `Mole.c:16067-16077`), so this tile is Missile 4 with the passive: 8
   missiles in 4 pairs, the pad, the lock, the gold blasts. Its 5 % "egg" (every missile a splitting MissileBot) is rolled as
   the game does (question 3). BB's `missile` tile is the BB research's.
8. **Flight times are now known** (the Bible says "Not computable from code: missile and warhead speeds",
   `mole-skill-reference.md:745`): TTO's bundles give `missileBot_fire`'s ProjectileControl velocity (0, 0, 8) and
   `kaiserWarhead`'s (0, 0, 12) (`probe.json`). With the steering (0.3 rad every 0.2 s, `Mole_missile::Update@0x1CA0660`)
   the 8 missiles reach a 10 m target 2.56-3.53 s after the cast (`missile_sim.txt`). Section 8.
9. **No camera effects.** MissilePadLock's `AddCamereShake` (`Mole.c:38443-38466`) is the player's screen: left out.

---

## 1. Shared machinery (`TTO1102:Mole`, `TTO1102:KingKaiser`)

- **`WarAreaBegin(command, tDir, clip, fade)@0x1C3DE70`** (`Mole.c:41176`): actionState `attack`, the command, the hero
  turned to `pos + vFlat(tDir)`, `PlayAnimation(clip, fade)`, wrapMode Once, moveSpeed 0. `WarAreaDoing(command)@0x1C3E410`:
  still attack + this command; `WarAreaEnd@0x1C3E4A0`: standby.
- **`WarAreaPrefab(name)@0x1C3F0C0`** (`:40933`): loads `GameAssets/characters/heroes/mole/effects/<name>` (cached; logs
  `Cannot find <name> effect`). `WarAreaSpawn(name, pos, rot, owned)@0x1C3F420` (`:40994`): owned -> `createEffect`, else
  `Instantiate`. `RailFx(name, pos, rot)@0x1C3B5D0` (`:40348`): always a bare `Instantiate`. Owned here: only `assemble_box`.
- **`RailSound(name, volume)@0x1C3C8E0`** (`:40503`): `sounds/<name>`, `PlayOneShot` on the hero at volume x (1 owner,
  0.75 others). KingKaiser's `TwinSound@0x1CB26A0` (`KingKaiser.c:6405`) is the same on the Kaiser.
- **`RailLock(at, clank)@0x1C3BF90`** (`:40390`), the turret's OnLock: `barrelRailgun_lock` at `at`, identity, localScale x
  (0.6 + 0.8 clank); clank >= 0.9: `assemble_dust` at `mRailSpot` with the hero's rotation; RailSound `nAttack_hit`
  (`megaPunch_hit` when clank >= 0.7) at 0.25 + 0.35 clank (`:40420-40494`).
- **`MissilePadLock(at, clank)@0x1C2E7C0`** (`:38384`), the pad's OnLock: RailSound nAttack_hit / megaPunch_hit (>= 0.7) at
  0.25 + 0.35 clank; clank >= 0.9: `chopper_forwardDust` at `at` with the hero's rotation, and the owner's camera shake.
- **`KingKaiser::PodLock(at, clank)@0x1CB08B0`** (`KingKaiser.c:7381`), the pods' OnLock: `TwinFx('barrelRailgun_lock', at,
  identity, scale 1.2 + 1.2 clank)`, TwinSound nAttack_hit / megaPunch_hit (>= 0.7) at 0.3 + 0.4 clank.
- **`RailFlat(dir)@0x1C3B480`** (`:40277`): vFlat(dir) normalised, else the hero's forward; `RailYaw` its yaw. With the
  target 10 m ahead every Barrel Railgun direction is the hero's facing.
- **Targets.** Barrel Railgun's beam `FindRecTarget(turret spot, dir, 1.6, 1.6, 45.5, 3)` (`:39868-39870`); the Missile's
  `PickLocks(count)@0x1C2F710` (the nearest foes within 32 m, height 10, `:38552`); Kaiser Arsenal's
  `FindAreaTarget(Kaiser, 32, 10)` (`KingKaiser.c:395-396`). With the one 10 m target every lock, pair and random pick is
  it. Every effect on it goes to the target point 10 m ahead: its bounds centre 0.6 m up (Penguin decision 3), its feet 0.

## 2. Per skill

### 2.1 Barrel Railgun (`assemble1` > `assemble2` > `barrelRailgun1` > `barrelRailgun2` / `barrelRailgun3` > `barrelRailgun4`; cell 454) - released

Start: `Mole::DoRailgunSkill@0x1C2A780` (`Mole.c:38816`; the skill string `mol_barrelRailgun5`) starts
`<RPC_barrelRailgun>d__418` with the aim direction (`aim - hero` when not tiny, else the hero's forward). Coroutine
`TTO1102:Mole.<RPC_barrelRailgun>d__418::MoveNext@0x1C606D0` (`Mole.c:2754-3382`):

**Cast, 0-6.0 s (state 0 and its loop, `:2829-2993`):**
- `RailClear` (`:2831`); `WarAreaBegin('barrelRailgun', RailFlat(tDir), 'assemble1', 0.2)` (`:2840`); cooldown
  `agiAdjust(150)` (`:2845-2846`).
- `mRailSpot` = start + 1.17 x dir (`:2857-2865`); yaw = RailYaw(dir) (`:2871-2873`).
- **`barrelRailgun_turret`** (`WarAreaPrefab`, bare `Instantiate` at mRailSpot, identity, `:2875-2896`), `set_Yaw(yaw)`,
  `Grow(1)`, OnLock = RailLock, `Assemble(0, 6)` (`:2898-2914`). Its parts fly in (MoleRailTurret.Steps, `steps.txt`; position
  = rest + offset x (1 - BackOut(k)), rotation = AngleAxis((1 - k)^3 x spin, axis) x rest, k over [from, to],
  `MoleRailTurret::Assemble@0x1C84A40`, `MoleRailTurret.c:445-712`; BackOut(k) = 1 + 2.7 (k - 1)^3 + 1.7 (k - 1)^2):

  | part | from - to (s) | offset | axis, spin | clank | lock at |
  |---|---|---|---|---|---|
  | Plate | 0.2 - 0.7 | (0, -0.35, 0) | up, 0 | 0.6 | 0.7 |
  | Pedestal | 0.75 - 1.35 | (0, 2.6, 0) | up, 0 | 1.0 | 1.35 (+ assemble_dust) |
  | Cap | 1.4 - 1.85 | (0, 0.9, 0) | up, 360 | 0.5 | 1.85 |
  | Ring | 1.9 - 2.3 | (0, 0.7, 0) | up, -180 | 0.4 | 2.3 |
  | Yoke | 2.3 - 2.85 | (0, 1.8, 0) | right, 40 | 0.7 | 2.85 |
  | Seat | 2.85 - 3.35 | (0, 0.35, -1.4) | right, -70 | 0.5 | 3.35 |
  | Grips | 3.35 - 3.75 | (0, 0.45, -0.25) | right, 50 | 0.35 | 3.75 |
  | Drum | 3.8 - 4.35 | (0, 1.3, -1.5) | forward, 180 | 0.8 | 4.35 |
  | Breech | 4.2 - 4.65 | (0, 1.2, 0) | up, 90 | 0.6 | 4.65 |
  | Rails | 4.6 - 5.05 | (0, 0, -1.25) | forward, 0 | 0.6 | 5.05 |
  | Coil1 / 2 / 3 | 5.0 - 5.25 / 5.18 - 5.43 / 5.36 - 5.61 | (0, 0.8, 0) | forward, 270 / -270 / 270 | 0.35 / 0.35 / 0.45 | 5.25 / 5.43 / 5.61 |

  Then the boot at 5.62 (the gun's tier 3, its `tierAt`), the flash at 5.85 (`firedAt`, tier 0), the head's 12-degree check
  wobble 5.62-6.0 (sin(2 pi f) x 12 x (1 - f), f over 0.38 s) and `Finish()` at 6.0 (`MoleRailTurret.c:526-571`). Each lock
  is RailLock at the part's transform (the pivots, `probe.json`: Plate / Pedestal / Cap at the turret root; Ring / Yoke /
  Seat / Grips at Head (0, 0.6, 0); Drum / Breech / Rails / Coil1-3 at the gun, Head + Cradle (0, 0.45, 0.45)).
- `RailFx('assemble_dust', mRailSpot, hero rotation)` and `RailSound('assemble', 1)` (`:2925-2926`).
- The owner's cast bar `DisplayCastBar(6)` (`:2944`): fixed, no magAdjust (NOTES.md: "Barrel Railgun's fixed 6 s stays").
- The cast loop (state 1, `:2953-2993`), every frame while `elapsed < 6`: at 0.6 s once, `PlayAnimation('assemble2', 0)`,
  wrapMode Loop (`:2960-2964`), and **`assemble_box` owned** at the hero, hero rotation (`WarAreaSpawn(..., owned 1)`,
  `:2966-2977`); `Assemble(elapsed, 6)` (`:2986`).
- At 6.0: `Destroy(box)` (`:2995-3005`); `Finish()`; `PlayAnimation('barrelRailgun1', 0.1)`, `time = 0.55`, wrapMode Once
  (`:3019-3026`).

**The hop, 6.0-6.65 s (state 2, `:3029-3104`):** clip time ct = 0.55 + t; from ct 0.85 gravity off and the Mole moved from
its start to the turret's seat (SeatAnchor = Head + (0, 0.03, -0.62): **0.63 m up, 0.55 m ahead** of the start) along
`lerp(start, seat, s) + up x 0.5 sin(pi s)`, s = SmoothStep(clamp01((ct - 0.85) x 4)) (done at ct 1.1), facing the
turret's yaw; to ct 1.2 (`:3100`). No effect, no sound.

**The ride, from 6.65 s (`:3119-3367`):** `mRailRiding`, `rideAt` = now (`:3119-3121`); the owner's 20 s bar
(`DisplayCastBar(20)`, `:3139`); `PlayAnimation('barrelRailgun2', 0.1)` looped (`:3142-3144`); **`barrelRailgun_line`**
(RailFx at mRailSpot, the head's rotation) parented to the turret's Head, its GroundHugEmitters' startWidth / endWidth set
to 3.2 (`0x404ccccd` at +0x40 / +0x44, `:3154-3174`; GroundHugEmitter fields, `dump.cs:11676-11677`): a 3.2 m x 45 m lane
(the hit's width), life 120, destroyed at the end. Then every frame (state 3, `:3198-3367`):
- the turret's yaw: the owner steers it (`RailSteer`, left / right keys), others lerp to the owner's; on the page nobody
  steers: it stays the hero's facing; `RailSeat` keeps the Mole on the seat (`Mole::RailSeat@0x1C3C3D0`).
- cycle k = floor(ride / 2.4), c = ride - 2.4 k. A new cycle: `SetTier(0)` (`:3253-3265`). Tier 1 / 2 / 3 at c >= 0.6 /
  1.3 / 2.0 (`RailTierAt` = [0, 0.6, 1.3, 2.0], `Mole::.cctor@0x1C404E0`), shown once each while the cycle's shot time
  (cycle start + 2.2) <= 20.01: `SetTier(t)` and `RailSound('teslaCoil', 0.4 + 0.15 t)` (0.55 / 0.70 / 0.85) (`:3280-3325`).
- **the shot** at c >= 2.2 once per cycle while ride <= 20 (`:3330-3356`): `RPC_barrelRailgun_fire(mRailSpot, the head's
  forward, k + 1)`. **8 shots** at ride 2.2, 4.6 ... 19.0 (cast + 8.85 ... 25.65).
- ride >= 20 (`:3359-3360`): `RailSendEnd` -> `RPC_barrelRailgun_end`. Pressing the skill again ends the ride early
  (`Mole::TryRecast@0x1C3DA10`, Bible :757); KO / death too.

**Each shot: `TTO1102:Mole.<RPC_barrelRailgun_fire>d__424::MoveNext@0x1C62250` (`Mole.c:3657-3932`)**, at the shot's time:
- the turret's yaw set to the shot's direction, `MoleRailgun.Fire()`, `MoleRailTurret.Kick()` (`:3784-3803`); the muzzle =
  the gun's `muzzle` transform (Head 0.6 + Cradle (0, 0.45, 0.45) + Muzzle (0, 0, 1.42) under the turret: **1.05 m up,
  3.04 m ahead** of the start; the kick's recoil shows next LateUpdate, after the read).
- **`barrelRailgun_beam`** at the muzzle, LookRotation(dir), `MoleRailBeam.Shoot(muzzle, muzzle + 45 dir, 3)`
  (`:3825-3855`); **`barrelRailgun_muzzle`** at the muzzle, LookRotation(dir) (`:3861`); **`barrelRailgun_recoil`** and
  **`barrelRailgun_blast`** at mRailSpot, LookRotation(dir) (`:3867`, `:3872`).
- `RailSound('bazooka_fire', 1)`, `RailSound('superTNT_hit', 0.6)` (`:3873-3874`).
- `RailRip(mRailSpot, dir)` (`<RailRip>d__428::MoveNext@0x1C93700`, `Mole.c:24361-24455`): **`barrelRailgun_rip`** at
  mRailSpot + s dir, LookRotation(dir), s = 2, 5, 8 ... 44 (15 rips, while s <= 45), one every `Waits.Get(0.01875)`: 3 m
  per 0.01875 s = 160 m/s, the beam slug's speed (`slugSpeed` 160, `probe.json`).
- **`barrelRailgun_trench`** at mRailSpot + dir, LookRotation(dir) (`:3881-3885`), and `RailTrenchSparks(mRailSpot, dir)`
  (`<RailTrenchSparks>d__427::MoveNext@0x1C93C70`, `:24736-24882`): for 2.4 s, every Random.Range(0.05, 0.11) s, one
  **`barrelRailgun_arc`** with `life` = Random.Range(0.08, 0.18) and `Set(a, b)`, a = mRailSpot + dir x U(1.5, 43) + 0.15 up,
  b = a + (Euler(0, U(-35, 35), 0) dir) x U(1, 2.5) + 0.25 up.
- the owner's hits (`:3898-3910`): `RailHit(mRailSpot, dir)@0x1C3B780` (`:39789-40057`): for every foe in the lane (no
  insight), the hit; the 12 % paralysis (`:39919-39931`, a status on the foe: no look, Sheep decision 4); **`barrelRailgun_hit`**
  at the foe's collider bounds centre, LookRotation(dir) (`:39935-39983`); then `RPC_barrelRailgun_overload` on the
  damaged foe nearest along the lane (`:40001-40033`). `RailTrench` (`<RailTrench>d__426@0x1C941B0`): 5 ticks of hits,
  no effect.
- `PlayAnimation('barrelRailgun3', 0.05)`, wrapMode Once (`:3919-3921`); `Waits.Get(0.5)` (`:3925`); then, still riding,
  `PlayAnimation('barrelRailgun2', 0.1)` looped (`:3716-3721`).

**The overload: `<RPC_barrelRailgun_overload>d__429::MoveNext@0x1C62C00` (`Mole.c:3955-4295`):** **`barrelRailgun_overload`**
at the foe's position (its feet), identity, parented to it (`:4065-4094`); 3 times `Waits.Get(0.7)`, each:
**`barrelRailgun_shock`** at the foe + 1 up, identity (`:4128-4154`; the prefab's own sound nAttack_hit_2 0.8), the shock
hit, and an arc (`barrelRailgun_arc`, life 0.25, from the foe + up to each other foe within 4 m + up) plus a shock on each
of those (`:4175-4264`); after the third (2.1 s) the aura is destroyed (`:4270-4295`). One target: 3 shocks, no arcs.

**The end: `<RPC_barrelRailgun_end>d__430::MoveNext@0x1C61B20` (`Mole.c:3403-3636`):** riding off, the line destroyed,
`SetTier(0)` (`:3444-3486`); `PlayAnimation('barrelRailgun4', 0.05)`, Once (`:3490-3492`); the hop off: from the seat to
`land` = mRailSpot - 0.8 x the turret's right - 0.2 x its forward (**0.8 m left, 0.97 m ahead** of the start, on the
ground), `lerp + up x 0.4 sin(pi s)`, s = SmoothStep(clamp01((t - 0.08) / 0.32)) to t 0.42 (`:3533-3575`); gravity back
after 0.4 (`:3577`); the turret shrinks `Grow(1 - clamp01(2 (t - 0.3)))` (`:3586-3594`); `WarAreaEnd` (standby) at 0.5
(`:3596-3598`); the turret destroyed at 0.8 (`:3605-3621`). No effect, no sound.

**Timeline with question 1's 10 s ride** (cast-relative; the full 20 s ride in brackets):

| s | what |
|---|---|
| 0 | assemble1, turret, assemble_dust, sound assemble |
| 0.6 | assemble2 loop, assemble_box (owned) |
| 0.7 ... 5.61 | the 13 locks (table above) |
| 5.62 / 5.85 / 6.0 | gun boot / flash / Finish; box destroyed |
| 6.0 - 6.65 | barrelRailgun1 from 0.55: the hop |
| 6.65 | ride: barrelRailgun2, the line |
| 7.25, 7.95, 8.65 | teslaCoil 0.55 / 0.70 / 0.85 (tiers 1-3); again 2.4 s later each cycle |
| 8.85, 11.25, 13.65, 16.05 [... 25.65] | the shots (barrelRailgun3 0.5 s each) |
| 16.65 [26.65] | the end (barrelRailgun4), the line gone |
| 17.15 [27.15] | standby |
| 17.45 [27.45] | the turret gone |

### 2.2 Missile with Twin Warhead (`missilePad`, 1.3 s; Missile + cell 453) - released

Coroutine `TTO1102:Mole.<RPC_missile>d__344::MoveNext@0x1C78270` (`Mole.c:15978-16471`); waits from capstone
(`missile_movenext.asm`):
- **0.00** (state 0, `:16064-16157`): Twin Warhead learned, so no `OldMissile`; attack, command `missile`, cooldown
  `agiAdjust(60)`; `sLv` = `MissileBotLevel(mPos, 4)` = **8** (2 x rank, `Mole::MissileBotLevel@0x1C2DFD0`, which also rolls
  the egg: a System.Random seeded from the cast position, `< 0.05` -> `missileBotEgg`); the hero at mPos facing the target;
  `PlayAnimation('missilePad', 0.05)`, Once (`:16116-16125`); **`MissileVoice`** (`Mole::MissileVoice@0x1C2EA40`:
  `voices/missile1` or `missile2`, `Random.Range(0, 2)`, volume 1); **`SpawnMissilePad(mPos - 1.35 forward)`**
  (`:16143-16149`; `Mole::SpawnMissilePad@0x1C3D4D0`, `:38266-38372`): `missilePad` (bare Instantiate, **1.35 m behind** the
  hero, the hero's rotation), OnLock = MissilePadLock, `Begin()`; **`assemble_dust`** there, the hero's rotation; sound
  **`missile_base`** (volume 1). `Waits.Get(0.3)` (0x1C7871E).
- **The pad** (`MoleLaunchPad`, `MoleLaunchPad.c`): rises from 0.8 m under the ground over 0.45 s, hatches open 0.42-0.6 s
  to 115 degrees, the rack lifts 0.22 at 0.52-0.72 s; its Locks table [3, 2] = (0.45, 1.0), (0.6, 0.5), (0.72, 0.6)
  (`MoleLaunchPad::.cctor@0x1C82740`, `MoleLaunchPad.c:490`) -> MissilePadLock: **0.45** megaPunch_hit 0.6 + `chopper_forwardDust`
  at the pad (the hero's rotation; clank 1.0) + the camera shake (left out); **0.60** nAttack_hit 0.425; **0.72** nAttack_hit
  0.46. Each `Kick()` (a launch) jolts the rack for 0.12 s; `SinkIn(s)` sinks it over 0.55 s, then Destroy; it sinks by
  itself at age 4 (`MaxLife`, `MoleLaunchPad.c:144-167`).
- **0.30** (state 2, `:16175-16204`): `PickLocks((8 + 1) / 2)` = up to 4 nearest foes: the target; `LockSequence(locks)`
  (`<LockSequence>d__353@0x1C55670`: one `RPC_missile_lock` per lock, 0.07 s apart): **`missile_lock`** at the target's
  bounds centre, identity, parented to it, scale = clamp(0.7 x 2 x max(extent x, y), 1, 4) / its lossy scale = 1 for a
  hero-sized foe (`Mole.c:38686-38775`), and **`sound/gui/beep`** at 0.6 (owner; 0.35 others) (`:38778-38806`).
  `Waits.Get(0.65)` (0x1C788FA).
- **0.95** (state 3, `:16209-16369`): **`missile_fire`** sound (`PlayMissileFireSound@0x1C2F9A0`, volume 1); then missile
  i = 0 ... 7, `Waits.Get(0.05)` between (0x1C78D98): **0.95, 1.00 ... 1.30**. Missile i: pair = `NextTwinPair()` on even
  i (missiles 2j and 2j + 1 share pair j); the firing point = the pad's `NextMuzzle()` (Muzzle0-3 in turn: rack (+-0.15,
  0.53, +-0.15), the pad scaled 0.85, the rack raised 0.22: (+-0.13, 0.64, -1.35 +- 0.13) from the hero); fire dir =
  normalize(rotateH(forward, 360 / 8 x i) x 0.45 + up x 1.4) (`:16316-16333`; `Math.rotateH` turns to the left,
  `DecompiledSource/Math.cs:838-843`): 72.2 degrees up, fanned 45 degrees apart. `RPC_missile_fire@0x1C34DE0`
  (`:33952-34068`): `MoleLaunchPad.Kick()`, **`missilePad_launch`** at the muzzle, LookRotation(dir); `FireMissile@0x1C2B3C0`
  (`:34072-34205`): **`missileBot_fire`** (or the egg **`missileBot_fire_bot`**) at muzzle + dir, LookRotation(dir), its
  ProjectileControl life 10 x rangeMod (Twin Warhead; 5 without), `Mole_missile.twin` = true, `pair`, the target.
- **1.30**: `LinkedSalvo(locks)` (every own Auto Gyro Gun within 20 m fires a pair: none here); the wait `0.35 - 0.05 x 7`
  = 0 is skipped (`:16371-16393`); `SinkIn(0.45)` (0x1C78ED1): the pad sinks at 1.75 and is **destroyed at 2.30**; standby
  (`:16401-16466`). The clip is 1.3 s.
- **The flights** (`Mole_missile::Update@0x1CA0660`, `mole_missile.txt`; the same as BB's `Mole_missile.cs:157-172`): every
  0.2 s, forward = RotateTowards(forward, the target's bounds centre - pos, 0.3 rad, 1), velocity = forward x 8 m/s (the
  prefab's (0, 0, 8)). `missile_sim.py` (a 0.5 m contact radius about the target's axis) gives, by missile 0-7: hits at
  **2.558, 2.675, 2.992, 3.333, 3.525, 3.433, 3.200, 2.975 s**, climbing 4.7-8.1 m. A hit (`Mole_missile::OnTriggerEnter
  @0x1C9FDC0`): the damage, then `RPC_missile_hit@0x1C35100`: **`missileBot_hit`** at the hit point (`ClosestPointOnBounds`:
  the top of the target, 1.2 m) with **the hero's** rotation (`:34260-34278`); then `Mole::WarheadHit@0x1C3FFE0`: the
  pair's second hit within 0.5 s of the first on the same foe -> `TwinImpact` (the gold blast's hits) -> `RPC_twinImpact
  @0x1C39D90`: **`twinImpact`** at that point, LookRotation(vFlat(dir)) (`:37519-37588`). Pairs (0, 1), (2, 3), (4, 5),
  (6, 7): second hits at **2.675, 3.333, 3.525, 3.200** (gaps 0.12 / 0.34 / 0.09 / 0.23 s: all four blast).
- **The egg** (5 %, question 3): every missile is `missileBot_fire_bot` (a MissileBot riding the missile), and a hit
  calls `MissileBotScatter(at)@0x1C2E1E0` instead of the twin blast: 8 `missileBot_fire` from the hit point + 1 up, fanned
  45 degrees, each at a random foe within 32 m (the target again); they hit as above (no twin, no second split; Bible :741).
  64 more missiles: part P9 spawns them.

### 2.3 Kaiser Arsenal (`kaiserArsenal`, 4.4 s; King Kaiser, Twin Warhead) - released

The King Kaiser's normal attack picks it at 50 % with Kaiser level 2+ and a target farther than 10 m
(`KingKaiser::doNormalAttack@0x1CB36E0`, `RollArsenal@0x1CB1970`; Bible :743). Coroutine
`TTO1102:KingKaiser.<RPC_kaiserArsenal>d__72::MoveNext@0x1CB7460` (`KingKaiser.c:206-656`):
- **0.00**: attack, command `kaiserArsenal`, the 6 s `nAttack` lock; the Kaiser at mPos facing the target; the clip `arsenal`
  added from `GameAssets/characters/heroes/mole/animations/kaiserArsenal` (`TwinAsset`, `:310-319`), `CrossFade(arsenal, 0.2)`,
  Once (`:328-329`). No voice. `Waits.Get(0.6)` (`:335`).
- **0.60** (state 1): `SpawnPods()` (`KingKaiser::SpawnPods@0x1CB19A0`, `KingKaiser.c:7202-7377`): `DropPods`, then
  **`kaiserArsenalPod`** instantiated under the Kaiser's **Arm_R** and **Arm_L** bones (`FindBone`), localPosition 0,
  localRotation `LookRotation(left, forward)` (= Euler (0, -90, -90)), named `arsenalPod_<bone>`, `Wear(the Kaiser's skinned
  material)` (the pods take the Kaiser's colour), OnLock = PodLock, `unfoldAt` = now (`:7256-7353`); **`assemble_dust`** at
  the Kaiser, its rotation, scale 1.6 (`TwinFx`, `:7354-7366`); then `PlayOneShot(kaiser_openFx)` = the clip
  **`kaiser_open`** (the KingKaiser_b prefab's field, `kaiser_tto.txt`; `KingKaiser.c:357-366`). `Waits.Get(1.2)` (`:371`).
- **The pods** (`KaiserArsenalPod`, not decompiled: fields `dump.cs:109601-109641`, RVAs `methods.tsv`): UnfoldTime 1.05,
  FoldTime 0.7, PetalOpen 42, RackSlide 0.75, RackTwist 60, FinFold 90; Locks [4, 3] = (0.38, 0.6, 0), (0.68, 1.0, 1),
  (0.85, 0.45, 2), (0.98, 0.5, 3) (time after Unfold, clank, lock point; `KaiserArsenalPod::.cctor@0x1CAD990`, resolved by
  `podlocks.py`) -> PodLock on each pod: **`barrelRailgun_lock`** at `LockPoint(i)`, scale 1.92 / 2.4 / 1.74 / 1.8, and
  nAttack_hit 0.54 / megaPunch_hit 0.7 / nAttack_hit 0.48 / nAttack_hit 0.5, at **0.98, 1.28, 1.45, 1.58 s** (twice: two pods).
- **1.80** (state 2): targets = `FindAreaTarget(Kaiser, 32, 10)` (the owner's). **16 shots**, `Waits.Get(0.1)` apart:
  **1.8, 1.9 ... 3.3** (`:484-603`). Shot k: on even k a random target (`pairTarget`); pod `k % 2` (Arm_R on even, Arm_L on
  odd) `Kick()` -> its next muzzle (Muzzle0-6, the rack 1.32 m out); dir = normalize(muzzle.forward + 0.35 up);
  `ArsenalShot@0x1CAF000` (`KingKaiser.c:7028-7071`): **`kaiserArsenal_muzzle`** at the muzzle, LookRotation(dir);
  TwinSound **`missile_fire` 0.55**; `FireWarhead(muzzle, dir, target, arsenal, 3.5)@0x1CAF780`: **`kaiserWarhead`** at the
  muzzle, LookRotation(dir) (`:6706-6735`).
- **The warheads** (`KaiserWarhead.c`): 12 m/s (the prefab's ProjectileControl (0, 0, 12)), `RotateTowards(forward, the
  target's bounds centre - pos, 0.4 rad, 1)` every 0.15 s (`:232`, `:271-272`), life 3.5; on contact or at the end of life
  `Land(at)@0x1CADC40` -> `KingKaiser::WarheadLanded@0x1CB2E70` -> `RPC_kaiserArsenal_hit@0x1CB0CA0` (`KingKaiser.c:7075`):
  **`kaiserArsenal_hit`** at `at` with the **Kaiser's** rotation (its own sound explosion1 0.6), then the hits (r 2.5).
  The launch points ride the Kaiser's animated arms, so the flights and hit times are the part's (P11 / P12).
- **3.40** (after the 16th shot's wait): `Waits.Get(3.5 - elapsed)` = 0.1 (`:607-618`); **3.50**: every pod `foldAt` = now
  (Fold) and TwinSound **`nAttack_hit` 0.5** (`:620-645`); `Waits.Get(0.7)` (`:649`).
- **4.20** (state 5): `DropPods(false)`: the pods destroyed, no poof (`:412-413`, `KingKaiser.c:7487-7560`); `Waits.Get(4.4 -
  elapsed)` = 0.2; **4.40**: standby (`:427-474`). The clip is 4.4 s.

## 3. What is left out (only "on an enemy's body" / "needs a foe" / the player's screen)

- Barrel Railgun: the paralysis status (12 %; no look on the foe, Sheep decision 4); the overload's arcs and shocks to
  other foes within 4 m (none); the trench's hits (no effect); the owner's two cast bars (GUI).
- Missile: the Auto Gyro Guns' linked salvo (none on the page; part 11's summons would not stand within 20 m either); the
  camera shake.
- Kaiser Arsenal: SP + 1 per target hit (no look).
Everything else is cued: the hits on the target go to the 10 m target point (the rule).

## 4. Sounds and voices

| t (s, in the cue's key) | kind | name | where | in BB's rip |
|---|---|---|---|---|
| assemble1 0 | sound | assemble | RailSound 1 (`Mole.c:2926`) | sounds/ |
| assemble2 0.1 ... 5.01 | sound | nAttack_hit / megaPunch_hit | RailLock 0.25 + 0.35 clank | sounds/ |
| ride (part) | sound | teslaCoil 0.55 / 0.70 / 0.85 | the tiers (`:3325`) | sounds/ |
| barrelRailgun3 0 | sound | bazooka_fire 1, superTNT_hit 0.6 | `:3873-3874` | sounds/ |
| own | AudioSource | nAttack_hit (muzzle, hit 1.0), nAttack_hit_2 (shock 0.8) | prefabs | Assets/AudioClip (nAttack_hit_2: the exporter's fallback, TTO's clip) |
| missilePad 0 | voice | missile1 \| missile2 | MissileVoice | voices/ |
| missilePad 0 | sound | missile_base | SpawnMissilePad | sounds/ |
| missilePad 0.3 | sound | **beep** 0.6 | RPC_missile_lock | `Resources/sound/gui/beep.ogg` (P15) |
| missilePad 0.45 / 0.6 / 0.72 | sound | megaPunch_hit 0.6 / nAttack_hit 0.425 / 0.46 | MissilePadLock | sounds/ |
| missilePad 0.95 | sound | missile_fire | PlayMissileFireSound | sounds/ |
| own | AudioSource | missile_hit (missileBot_hit, twinImpact 1.0) | prefabs | Assets/AudioClip (fallback) |
| kaiserArsenal 0.6 | sound | **kaiser_open** | PlayOneShot(kaiser_openFx) | `Assets/AudioClip/kaiser_open.wav` (P15) |
| kaiserArsenal 0.98-1.58 (part) | sound | nAttack_hit / megaPunch_hit x 2 | PodLock | sounds/ |
| kaiserArsenal 1.8 ... 3.3 | sound | missile_fire 0.55 x 16 | TwinSound | sounds/ |
| kaiserArsenal 3.5 | sound | nAttack_hit 0.5 | TwinSound | sounds/ |
| own | AudioSource | explosion1 0.6 (kaiserArsenal_hit) | prefab | Assets/AudioClip (fallback; built before as explosion1.mp3) |

## 5. Probed (home PC, TTO's 2026-11-04 bundles; `probe.json`, `compact.txt`)

All 25 in-scope TTO prefabs export; the warnings are the unresolved `arcPrefab` references ("a MonoBehaviour reference
() is written by name only": `barrelRailgun_turret`, `_beam`, `_hit`, `_shock`, `_lock`) and `barrelRailgun_rip`'s
AnimationClip `root` (`probe.err`). Materials (29): blends add 6, addsoft 13, alpha 1, multiply2 2, `FlexibleCelShader/Cel
No Outline` 6 (built: `tto_penguin.js`), `Transparent/AdditiveAlpha` 1 (built: `additivealpha.js`).

| prefab | EffectControl (life + after) | parts | own sound | needs |
|---|---|---|---|---|
| barrelRailgun_turret | none (the code destroys it) | MoleRailTurret (head, cradle, seat, gun); the gun's MoleRailgun (3 glows, 3 coils, channel, orb, muzzle, glowColor (0.45, 0.85, 1)); 20 StaticMesh (tto_BarrelBot cel, tto_railGlow_add), Ball (ImageEmitter, KingKaiser_beam) | - | P1, P2 |
| barrelRailgun_line | none (Destroy at the end) | GroundHug strip (shape 2) 1.5 wide (the code: 3.2), 45 long, life 120, lift 0.06 | - | P2 (spawn, width) |
| barrelRailgun_beam | none (MoleRailBeam life 0.55) | MoleRailBeam (core, glow, slug, slugSpeed 160, Width [0.4, 0.55, 0.85, 1.3]); Glow / Core StaticMesh tto_railBeam_add; Slug's Shell StaticMesh tto_nAttack (AdditiveAlpha) | - | P3 |
| barrelRailgun_muzzle | 1.0 + 0, scale 0.7 | LineEmitter, 2 ImageEmitters, 3 RingEmitters | nAttack_hit 1.0 | - |
| barrelRailgun_recoil | 0.6 + 1.0 (Puff 0.5 + 1.0, Skid 0.5 + 0) | Shuriken Smoke1, 2 LineEmitters | - | - |
| barrelRailgun_blast | 0.8 + 1.0, followPosition, **followState**, scale 1.3 | 2 GroundHugs (Line_vertMultilines4, Dust3_h) | - | cut (unowned) |
| barrelRailgun_trench | 2.4 + 0.6 | 2 GroundHug strips 44 m (2.2 -> 2.8 / 0.7 wide), tto_railTrench_add | - | P5 (sparks) |
| barrelRailgun_rip | 0.8 + 0.2, followPosition, **followState**, scale 0.8 | Animation (clip `root`, name only), 2 LineEmitters, SkinnedMeshRenderer `Mole_megaDrill_tri` (tto_megaDrill cel, 3 bones) | - | P7, cut (unowned) |
| barrelRailgun_arc | none (MoleRailArc life 0.2; the code sets 0.08-0.25) | LineRenderer (0.07 wide, tto_railBeam_add), MoleRailArc (segments 7, jag 0.16, maxJag 0.6, flicker 0.04) | - | P4 |
| barrelRailgun_hit | 1.0 + 0, scale 0.8 | LineEmitter, RingEmitter, ImageEmitter, Shock: MoleRailShock (3 arcs, reach 0.7-1.4, secondWave 0.1, pull 0.6) + 4 ImageEmitters + Shuriken Sparks (stretched) | nAttack_hit 1.0 | P4 |
| barrelRailgun_overload | 2.4 + 0.3 | LineEmitter Crackle (0.9 up), GroundHug ring | - | P6 |
| barrelRailgun_shock | 0.45 + 0.3 | MoleRailShock (5 arcs) + 4 ImageEmitters + Sparks | nAttack_hit_2 0.8 | P4 |
| barrelRailgun_lock | 0.4 + 0.2 | MoleRailShock (2 arcs, scale 0.45, pull 0) + 4 ImageEmitters + Sparks | - | P4 |
| missilePad | none (MaxLife 4; the code sinks it) scale 0.85 | MoleLaunchPad (body, 2 hatches, rack, 4 muzzles); 5 StaticMesh tto_BarrelBot | - | P8 |
| missilePad_launch | 1.0 + 0, scale 0.45 | LineEmitter, RingEmitter, ImageEmitter, Puff (Shuriken Smoke1) | - | - |
| missileBot_fire | ProjectileControl life 10, velocity (0, 0, 8) | Mole_missile (mTarget, scatter, twin, pair), Shuriken smoke trail (multiply2, loop, 20/s), 2 StaticMesh (missile, warhead) | - | P9 |
| missileBot_fire_bot | the same | + MissileBot SkinnedMeshRenderer (the robot, 4 missiles on mounts; MissilleBot_missile and Warhead inactive) | - | P9 |
| missileBot_hit | 1.0 + 0 | Shuriken Bomb2 (multiply2, 8 burst), ImageEmitter missile_hit | missile_hit 1.0 | - |
| missile_lock | 2.4 + 0.2 | MoleLockReticle (pull 1.2), 3 ImageEmitters (missileLock_add, KingKaiser_beam) | - | P10 |
| twinImpact | 1.0 + 0 | Shuriken Bomb2, ImageEmitters (missile_hit, GoldFlash, GoldRing), RingEmitter | missile_hit 1.0 | - |
| kaiserArsenalPod | none (DropPods) | KaiserArsenalPod (ring, 4 petals, rack, 2 fins, 7 muzzles); 8 StaticMesh tto_KingKaiser_k (cel; Wear swaps it) | - | P11 |
| kaiserArsenal_muzzle | 1.0 + 0 | LineEmitter, RingEmitter, 2 ImageEmitters | - | - |
| kaiserWarhead | ProjectileControl life 10 (the code 3.5), (0, 0, 12), scale 1.8 | KaiserWarhead (mTarget, arsenal), Shuriken smoke, 2 StaticMesh | - | P12 |
| kaiserArsenal_hit | 2.0 + 0 | 2 LineEmitters, 3 ImageEmitters, RingEmitter | explosion1 0.6 | - |
| barrelRailgun | (the gun alone, 17 nodes) | never spawned | - | - |

BB's copies (`probe_bb.json`): `assemble_box` 999 + 0, followPosition + followState (owned; the code destroys it at 6.0),
`assemble_dust` 1.0 + 0, `chopper_forwardDust` 0.5 + 0: all "ready" BB effects.

## 6. Parts the page lacks (effect: part)

Home `wardrobe/fxparts/tto_mole.js` (`parts.md`'s TTO table, which lists the same scripts); numbers above. Every part is
cued anyway (the rule).

| # | Part | Effects | What it does (source) |
|---|---|---|---|
| P1 | `MoleRailTurret` (+ the gun's `MoleRailgun`) | barrelRailgun_turret | The 13-part assembly over 6 s (Steps table 2.1; renderers shown from each step's `from`), the boot (tier 3) at 5.62, the flash at 5.85, the check wobble, Finish at 6 (`finish`); Kick (0.45 s: cradle 0.22 back, 7-degree nod); Grow; the end's shrink from `rideEnd` + 0.3 to + 0.8 (`MoleRailTurret.c`, `Mole.c:3586-3621`). MoleRailgun: SetTier (orb OrbSize [0, 0.6, 1.0, 1.5], arcs between ArcTop1-3 every ArcGap [0, 0.35, 0.18, 0.08] s), Fire (the glow drains over DrainTime 0.6), Paint (`_TintColor`, glowColor) (`MoleRailgun.c`). |
| P2 | `Mole.RailRide` (code mover on the turret: the coroutine's ride) | barrelRailgun_turret (+ barrelRailgun_line, sound teslaCoil) | From `ride`: spawn `tto/barrelRailgun_line` parented to Head, its GroundHugs 3.2 wide (`Mole.c:3154-3174`); each cycle 2.4 s: SetTier(0), tiers 1-3 at 0.6 / 1.3 / 2.0 with teslaCoil 0.4 + 0.15 t (only while the cycle's shot <= 20.01 s of ride); at each of `shots`: Fire + Kick; at `rideEnd`: SetTier(0), the line destroyed. |
| P3 | `MoleRailBeam` | barrelRailgun_beam | Core and glow quads stretched from the cue's spot to `to`, width Width[tier] (tier 3: 1.3), fading over life 0.55; the slug flying at 160 m/s; arcs every 0.03 s while age < 0.7 life, Random 0.06-0.14 s, 1.5-3.5 m out (`MoleRailBeam.c:149-252`, Draw / Place). |
| P4 | `MoleRailArc` + `MoleRailShock`, and `arcPrefab` -> `tto/barrelRailgun_arc` | barrelRailgun_arc, _hit, _shock, _lock (+ the beam's and gun's arcs) | Arc: a jagged LineRenderer bolt from a to b (7 segments, jag 0.16, max 0.6, re-jagged every 0.04 s), fading over `life`; Follow(ta, tb, s). Shock: at Start `arcs` bolts from the node out 0.7-1.4 m (random yaw 0-360, pitch -50 to 25), a second wave at 0.1 s, `pull` toward the camera (`MoleRailShock.c`). The exporter writes `arcPrefab` as `{"asset": "MonoBehaviour", "name": ""}` (probe.err): resolve it to the arc prefab. |
| P5 | `Mole.RailTrenchSparks` (code mover on the trench) | barrelRailgun_trench (+ barrelRailgun_arc) | 2.4 s of arcs every U(0.05, 0.11) s along the lane from the cue's `from` (2.1; `Mole.c:24736-24882`). |
| P6 | `Mole.RailOverload` (code mover on the aura) | barrelRailgun_overload (+ barrelRailgun_shock) | 3 shocks at the aura + 1 up, 0.7 s apart (`Mole.c:4110-4295`); the cue's kill 2.1 ends it. |
| P7 | An effect's own Animation clips (TTO) | barrelRailgun_rip | The drill's `root` clip on its 3 bones (today written by name only); the SkinnedMeshRenderer export exists (Penguin P3). The rip lives only its 0.2 s after-life (unowned followState). |
| P8 | `MoleLaunchPad` | missilePad | Rise 0.45 s from 0.8 m down (Back easing), hatches 0.42-0.6 s to 115 degrees, rack +0.22 at 0.52-0.72 s, a 0.12 s kick at each of `kicks`, sink at `sink` over 0.55 s (`MoleLaunchPad.c:98-443`). The locks' sounds and dust are cued. |
| P9 | `Mole_missile` (homing mover; BB's Missile needs the same, `parts.md`) | missileBot_fire, missileBot_fire_bot | 8 m/s along forward, every 0.2 s RotateTowards the cue's `to` by 0.3 rad; gone at `kill` (the cued hit). The egg (`missileBot_fire_bot`): at `kill` spawn 8 `tto/missileBot_fire` from the hit + 1 up, fanned 45 degrees, steering to `to`, and their `tto/missileBot_hit` on arrival (`MissileBotScatter@0x1C2E1E0`; builds). |
| P10 | `MoleLockReticle` | missile_lock | Keeps its spot in the parent's space and is pulled toward the camera by min(pull 1.2, distance / 2) (`MoleLockReticle::LateUpdate@0x1C82870`, `reticle.asm`). |
| P11 | `KaiserArsenalPod` + the arsenal's shots | kaiserArsenalPod (+ kaiserArsenal_muzzle, kaiserWarhead, barrelRailgun_lock, sounds) | Unfold 1.05 s (petals 42, rack slide 0.75 + twist 60, fins 90), the 4 locks (2.3), a kick at each of `kicks` spawning `tto/kaiserArsenal_muzzle` + `tto/kaiserWarhead` at the next of 7 muzzles, dir = forward + 0.35 up, homing to `to`; Fold 0.7 s at `fold`; Wear (the worn colour). Needs its methods decompiled or read with capstone (`methods.tsv` 0x1CAC8A0-0x1CADAE0). |
| P12 | `KaiserWarhead` (mover) | kaiserWarhead | 12 m/s, RotateTowards 0.4 rad every 0.15 s, life 3.5; on reaching the target or at 3.5 s spawn `tto/kaiserArsenal_hit` there with the hero's rotation (builds). |
| P13 | SEQ: a step's clip start time | the Barrel Railgun tile | `barrelRailgun1` from 0.55 s (`Mole.c:3024`); and the corrected line (S1). |
| P14 | A hero mover for the ride (a 3-axis `lift`) | the Barrel Railgun tile | The hop onto the seat (0.63 up, 0.55 ahead) in barrelRailgun1, seated through the ride, the hop off to (-0.8, 0, 0.97) in barrelRailgun4 (2.1). Today's `lift` is height only (HeroLift, `index.html` LIFTS). Its cue, added with the part (not in section 7's block: an unknown lift name would not play): `[0, "lift", "barrelRailgun"]` on `@BarrelRailgun:assemble1`, the curve timed from the cast (seat reached 6.55 s, held to 16.65, landed 17.07). Question 2. |
| P15 | Hero sounds outside the class's sounds/ | beep, kaiser_open | `hero_sound_wav` (`wardrobe_fx.py:522`) walks Resources for `<name>.wav` only: beep is an .ogg (`Resources/sound/gui/beep.ogg`), kaiser_open is in `Assets/AudioClip/` (outside Resources). A SOUND_ALIASES line each won't do (aliases are .wav under gameassets): widen the lookup to .ogg and to Assets/AudioClip. |
| P16 | `SKILL_FX["mole"]` in `wardrobe_fx_tto.py` | all | The 25 prefabs of section 5 (barrelRailgun minus the unused gun), so the parts' spawns build too. |
| P17 | (question 4) the King Kaiser on the page | kaiserArsenal | `parts.md` part 11's summon, playing the TTO clip, the pods on its own Arm_R / Arm_L. |

## 7. The cue entries (ready to paste into `wardrobe/fx_cues/mole.json`)

`checks/fx_mole_research/tto/cues_paste.json` (parsed by `cues.py`): 5 keys, 131 cues. The part options (`finish`, `ride`,
`shots`, `rideEnd`, `tier`, `from`, `sink`, `kicks`, `fold`) are `fx.at`'s for P1-P11 (cueOf passes unknown keys through,
the cue format comment above `cueOf` in `index.html`: "every other option is passed on as it is, for the parts"); `cut` on the unowned followState roots; `p` / `roll` `egg` / `!egg` share one 5 % roll per play.
The missile hits and blasts are cued at `missile_sim.txt`'s times (P9 removes each missile at its `kill`, so no target
collider is needed; re-time them if P9's flights differ). Nothing is keyed on `barrelRailgun1`, `barrelRailgun2` or
`barrelRailgun4`: their steps carry no cue of their own (2.1; P2 / P14 run across them).

```json
{
  "@BarrelRailgun:assemble1": {
    "why": "TTO1102:Mole.<RPC_barrelRailgun>d__418::MoveNext@0x1C606D0 (pseudo/Mole.c:2754-3382; plans/fx_mole/tto.md 2.1): WarAreaBegin('barrelRailgun', dir, clip assemble1, fade 0.2) (:2840); the turret barrelRailgun_turret at mRailSpot = start + 1.17 x flat dir (:2857-2865), identity then set_Yaw(the aim's yaw) = the hero's facing, Grow(1), Assemble(0, 6) (:2875-2914; its 13 parts fly in to 5.61 s, boot 5.62, flash 5.85, Finish at 6.0: MoleRailTurret::Assemble@0x1C84A40, MoleRailTurret::.cctor@0x1C86030 Steps); RailFx assemble_dust at mRailSpot with the hero's rotation (:2925) and RailSound('assemble', 1) (:2926; sounds/); the 6 s cast bar (:2944) is the owner's GUI. The turret lives to the end's shrink (<RPC_barrelRailgun_end>d__430@0x1C61B20: Grow(1 - clamp01(2 (t - 0.3))), Destroy at 0.8 s, Mole.c:3586-3621): with the ride cut at 10 s (question 1) the end starts at 6.65 + 10 = 16.65 s, so kill 17.45; finish / ride / shots / rideEnd are the turret part's clock (parts P1, P2: the ground line, the charge tiers with teslaCoil, Fire and Kick at each shot, the shrink)",
    "builds": ["tto/barrelRailgun_line", "sound:teslaCoil"],
    "cues": [
    [0, "fx", "tto/barrelRailgun_turret", {"d": 1.17, "kill": 17.45, "finish": 6.0, "ride": 6.65, "shots": [8.85, 11.25, 13.65, 16.05], "rideEnd": 16.65}],
    [0, "fx", "assemble_dust", 1.17],
    [0, "sound", "assemble"]
    ]
  },
  "@BarrelRailgun:assemble2": {
    "why": "RPC_barrelRailgun d__418 (Mole.c:2953-2993): at 0.6 s PlayAnimation(assemble2, 0) looped (:2962-2964) and WarAreaSpawn assemble_box owned at the hero with the hero's rotation (:2975), destroyed when the 6 s cast ends (:2995-3005: kill 5.4); each turret part's lock (MoleRailTurret::Assemble, OnLock = Mole::RailLock@0x1C3BF90, when its step reaches 1, at the step's 'to': checks/fx_mole_research/tto/steps.txt) spawns barrelRailgun_lock at the part, identity, scale x (0.6 + 0.8 clank) (Mole.c:40428-40457), RailSound nAttack_hit (megaPunch_hit when clank >= 0.7) at 0.25 + 0.35 clank (:40489-40494), and assemble_dust at mRailSpot with the hero's rotation when clank >= 0.9 (the Pedestal, :40459-40486); times are the steps' 'to' - 0.6; the parts' pivots (probe.json): Plate / Pedestal / Cap at the turret root, Ring / Yoke / Seat / Grips at Head (0.6 up), Drum / Breech / Rails / Coil1-3 at the gun (Head + Cradle (0, 0.45, 0.45))",
    "cues": [
    [0, "fx", "assemble_box", {"kill": 5.4}],
    [0.1, "fx", "tto/barrelRailgun_lock", {"d": 1.17, "scale": 1.08}],
    [0.1, "sound", "nAttack_hit", {"vol": 0.46}],
    [0.75, "fx", "tto/barrelRailgun_lock", {"d": 1.17, "scale": 1.4}],
    [0.75, "sound", "megaPunch_hit", {"vol": 0.6}],
    [0.75, "fx", "assemble_dust", 1.17],
    [1.25, "fx", "tto/barrelRailgun_lock", {"d": 1.17, "scale": 1.0}],
    [1.25, "sound", "nAttack_hit", {"vol": 0.425}],
    [1.7, "fx", "tto/barrelRailgun_lock", {"y": 0.6, "d": 1.17, "scale": 0.92}],
    [1.7, "sound", "nAttack_hit", {"vol": 0.39}],
    [2.25, "fx", "tto/barrelRailgun_lock", {"y": 0.6, "d": 1.17, "scale": 1.16}],
    [2.25, "sound", "megaPunch_hit", {"vol": 0.495}],
    [2.75, "fx", "tto/barrelRailgun_lock", {"y": 0.6, "d": 1.17, "scale": 1.0}],
    [2.75, "sound", "nAttack_hit", {"vol": 0.425}],
    [3.15, "fx", "tto/barrelRailgun_lock", {"y": 0.6, "d": 1.17, "scale": 0.88}],
    [3.15, "sound", "nAttack_hit", {"vol": 0.3725}],
    [3.75, "fx", "tto/barrelRailgun_lock", {"y": 1.05, "d": 1.62, "scale": 1.24}],
    [3.75, "sound", "megaPunch_hit", {"vol": 0.53}],
    [4.05, "fx", "tto/barrelRailgun_lock", {"y": 1.05, "d": 1.62, "scale": 1.08}],
    [4.05, "sound", "nAttack_hit", {"vol": 0.46}],
    [4.45, "fx", "tto/barrelRailgun_lock", {"y": 1.05, "d": 1.62, "scale": 1.08}],
    [4.45, "sound", "nAttack_hit", {"vol": 0.46}],
    [4.65, "fx", "tto/barrelRailgun_lock", {"y": 1.05, "d": 1.62, "scale": 0.88}],
    [4.65, "sound", "nAttack_hit", {"vol": 0.3725}],
    [4.83, "fx", "tto/barrelRailgun_lock", {"y": 1.05, "d": 1.62, "scale": 0.88}],
    [4.83, "sound", "nAttack_hit", {"vol": 0.3725}],
    [5.01, "fx", "tto/barrelRailgun_lock", {"y": 1.05, "d": 1.62, "scale": 0.96}],
    [5.01, "sound", "nAttack_hit", {"vol": 0.4075}]
    ]
  },
  "@BarrelRailgun:barrelRailgun3": {
    "why": "Each shot: TTO1102:Mole.<RPC_barrelRailgun_fire>d__424::MoveNext@0x1C62250 (Mole.c:3657-3932), started at ride 2.2 + 2.4 k (d__418 :3310-3343; RailTierAt 0.6 / 1.3 / 2.0, Mole::.cctor@0x1C404E0): MoleRailgun.Fire and MoleRailTurret.Kick (:3800-3803, the turret part's clock); barrelRailgun_beam at the gun's muzzle (Head 0.6 + Cradle (0, 0.45, 0.45) + Muzzle (0, 0, 1.42): 1.05 up, 3.04 ahead), LookRotation(dir), MoleRailBeam.Shoot(muzzle, muzzle + 45 dir, tier 3) (:3836-3855; part P3); barrelRailgun_muzzle at the muzzle (:3861); barrelRailgun_recoil and barrelRailgun_blast at mRailSpot (:3867, :3872; the blast is followState with no owner, a bare Instantiate (Mole::RailFx@0x1C3B5D0), so EffectControl sends it to its after-life at once (EffectControl.cs:194-210): cut at its spawn); RailSound bazooka_fire 1 and superTNT_hit 0.6 (:3873-3874); RailRip (<RailRip>d__428@0x1C93700, Mole.c:24361-24455): barrelRailgun_rip at mRailSpot + s dir, s = 2, 5 ... 44, every 0.01875 s (the slug's 160 m/s), LookRotation(dir), also unowned followState (cut at spawn); barrelRailgun_trench at mRailSpot + dir, LookRotation(dir) (:3885) and RailTrenchSparks (<RailTrenchSparks>d__427@0x1C93C70: an arc every 0.05-0.11 s for 2.4 s; part P5 on the trench, from = mRailSpot); RailHit@0x1C3B780: barrelRailgun_hit at the struck foe's bounds centre (the 10 m target, 0.6 m up), LookRotation(dir) (Mole.c:39935-39983), then RPC_barrelRailgun_overload on the nearest damaged foe (:40014-40033): <RPC_barrelRailgun_overload>d__429@0x1C62C00 puts barrelRailgun_overload on its feet, identity, parented to it (:4065-4094), 3 shocks (barrelRailgun_shock at the foe + 1 up, identity) 0.7 s apart, the aura destroyed after the third at 2.1 s (:4110-4295; part P6 spawns the shocks). Then barrelRailgun3 (fade 0.05) for Waits 0.5 and barrelRailgun2 again (fade 0.1) (:3919-3925, :3719). The 12 % paralysis (:39919-39931) is a status on the foe: no look here (Sheep decision 4)",
    "builds": ["tto/barrelRailgun_arc", "tto/barrelRailgun_shock"],
    "cues": [
    [0, "fx", "tto/barrelRailgun_beam", {"y": 1.05, "d": 3.04, "to": [0, 1.05, 48.04], "tier": 3}],
    [0, "fx", "tto/barrelRailgun_muzzle", {"y": 1.05, "d": 3.04}],
    [0, "fx", "tto/barrelRailgun_recoil", 1.17],
    [0, "fx", "tto/barrelRailgun_blast", {"d": 1.17, "cut": 0}],
    [0, "sound", "bazooka_fire"],
    [0, "sound", "superTNT_hit", {"vol": 0.6}],
    [0.0, "fx", "tto/barrelRailgun_rip", {"d": 3.17, "cut": 0.0}],
    [0.01875, "fx", "tto/barrelRailgun_rip", {"d": 6.17, "cut": 0.01875}],
    [0.0375, "fx", "tto/barrelRailgun_rip", {"d": 9.17, "cut": 0.0375}],
    [0.05625, "fx", "tto/barrelRailgun_rip", {"d": 12.17, "cut": 0.05625}],
    [0.075, "fx", "tto/barrelRailgun_rip", {"d": 15.17, "cut": 0.075}],
    [0.09375, "fx", "tto/barrelRailgun_rip", {"d": 18.17, "cut": 0.09375}],
    [0.1125, "fx", "tto/barrelRailgun_rip", {"d": 21.17, "cut": 0.1125}],
    [0.13125, "fx", "tto/barrelRailgun_rip", {"d": 24.17, "cut": 0.13125}],
    [0.15, "fx", "tto/barrelRailgun_rip", {"d": 27.17, "cut": 0.15}],
    [0.16875, "fx", "tto/barrelRailgun_rip", {"d": 30.17, "cut": 0.16875}],
    [0.1875, "fx", "tto/barrelRailgun_rip", {"d": 33.17, "cut": 0.1875}],
    [0.20625, "fx", "tto/barrelRailgun_rip", {"d": 36.17, "cut": 0.20625}],
    [0.225, "fx", "tto/barrelRailgun_rip", {"d": 39.17, "cut": 0.225}],
    [0.24375, "fx", "tto/barrelRailgun_rip", {"d": 42.17, "cut": 0.24375}],
    [0.2625, "fx", "tto/barrelRailgun_rip", {"d": 45.17, "cut": 0.2625}],
    [0, "fx", "tto/barrelRailgun_trench", {"d": 2.17, "from": [0, 0, 1.17]}],
    [0, "fx", "tto/barrelRailgun_hit", {"y": 0.6, "d": 10}],
    [0, "fx", "tto/barrelRailgun_overload", {"d": 10, "kill": 2.1}]
    ]
  },
  "missilePad": {
    "why": "TTO1102:Mole.<RPC_missile>d__344::MoveNext@0x1C78270 (pseudo/Mole.c:15978-16471; plans/fx_mole/tto.md 2.2), Twin Warhead learned (passives on; without it OldMissile plays BB's missile clip): Missile rank 4 -> 8 missiles (Mole::MissileBotLevel@0x1C2DFD0); the clip, fade 0.05 (:16116-16125); Mole::MissileVoice@0x1C2EA40: missile1 / missile2, Random.Range(0, 2) (voices/); Mole::SpawnMissilePad@0x1C3D4D0 at mPos - 1.35 forward, the hero's rotation (:16143-16149): missilePad + assemble_dust there + sounds/missile_base; the pad's locks (MoleLaunchPad.Locks (0.45, 1.0), (0.6, 0.5), (0.72, 0.6), MoleLaunchPad::.cctor@0x1C82740) -> Mole::MissilePadLock@0x1C2E7C0: nAttack_hit / megaPunch_hit at 0.25 + 0.35 clank, and for clank >= 0.9 chopper_forwardDust at the pad with the hero's rotation (the camera shake is the player's screen: left out); Waits 0.3 (capstone 0x1C7871E): PickLocks((8 + 1) / 2) = the one target, LockSequence -> RPC_missile_lock@0x1C352E0: missile_lock at its bounds centre, identity, parented to it, scale 1 for a hero-sized foe, and sound/gui/beep at 0.6 (Mole.c:38686-38806); Waits 0.65 (0x1C788FA): sounds/missile_fire, then missile i every 0.05 s (0x1C78D98), fire dir = normalize(rotateH(forward, 45 i) x 0.45 + up x 1.4) (:16316-16333; Math.rotateH turns to the left, DecompiledSource/Math.cs:838-843), from the pad's next muzzle (NextMuzzle cycles Muzzle0-3; the pad scaled 0.85, the rack raised 0.22: 0.64 m up): RPC_missile_fire@0x1C34DE0: MoleLaunchPad.Kick, missilePad_launch at the muzzle, LookRotation(dir); FireMissile@0x1C2B3C0: missileBot_fire (the egg missileBot_fire_bot when the cast's 5 % roll hit, MissileBotLevel) at muzzle + dir, LookRotation(dir); Mole_missile turns 0.3 rad toward the target's bounds centre every 0.2 s at 8 m/s (Mole_missile::Update@0x1CA0660; checks/fx_mole_research/tto/missile_sim.py: hits 2.56-3.53 s on the 10 m target); RPC_missile_hit@0x1C35100: missileBot_hit at the hit point (ClosestPointOnBounds: the top of the target), the hero's rotation; Mole::WarheadHit@0x1C3FFE0: a pair's second hit within 0.5 s -> TwinImpact -> RPC_twinImpact@0x1C39D90: twinImpact there, LookRotation(flat dir), 4 pairs; eggs split instead (Mole::MissileBotScatter@0x1C2E1E0, part P9); SinkIn(0.45) at 1.30 (0x1C78ED1): the pad sinks over 0.55 s and is destroyed at 2.30 (MoleLaunchPad::Update@0x1C82450). LinkedSalvo (Auto Gyro Guns within 20 m) has nothing to fire here",
    "cues": [
    [0, "voice", "missile1|missile2"],
    [0, "fx", "tto/missilePad", {"d": -1.35, "sink": 1.75, "kill": 2.3, "kicks": [0.95, 1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3]}],
    [0, "fx", "assemble_dust", -1.35],
    [0, "sound", "missile_base"],
    [0.3, "fx", "tto/missile_lock", {"y": 0.6, "d": 10}],
    [0.3, "sound", "beep", {"vol": 0.6}],
    [0.45, "sound", "megaPunch_hit", {"vol": 0.6}],
    [0.45, "fx", "chopper_forwardDust", -1.35],
    [0.6, "sound", "nAttack_hit", {"vol": 0.425}],
    [0.72, "sound", "nAttack_hit", {"vol": 0.46}],
    [0.95, "sound", "missile_fire"],
    [0.95, "fx", "tto/missileBot_fire", {"x": -0.13, "y": 1.59, "d": -1.17, "rot": [-72.2, 0, 0], "to": [0, 0.6, 10], "kill": 1.608, "p": 0.05, "roll": "!egg"}],
    [0.95, "fx", "tto/missilePad_launch", {"x": -0.128, "y": 0.64, "d": -1.478, "rot": [-72.2, 0, 0]}],
    [0.95, "fx", "tto/missileBot_fire_bot", {"x": -0.13, "y": 1.59, "d": -1.17, "rot": [-72.2, 0, 0], "to": [0, 0.6, 10], "kill": 1.608, "p": 0.05, "roll": "egg"}],
    [1.0, "fx", "tto/missileBot_fire", {"x": -0.34, "y": 1.59, "d": -1.01, "rot": [-72.2, -45, 0], "to": [0, 0.6, 10], "kill": 1.675, "p": 0.05, "roll": "!egg"}],
    [1.0, "fx", "tto/missilePad_launch", {"x": -0.128, "y": 0.64, "d": -1.223, "rot": [-72.2, -45, 0]}],
    [1.0, "fx", "tto/missileBot_fire_bot", {"x": -0.34, "y": 1.59, "d": -1.01, "rot": [-72.2, -45, 0], "to": [0, 0.6, 10], "kill": 1.675, "p": 0.05, "roll": "egg"}],
    [1.05, "fx", "tto/missileBot_fire", {"x": -0.18, "y": 1.59, "d": -1.48, "rot": [-72.2, -90, 0], "to": [0, 0.6, 10], "kill": 1.942, "p": 0.05, "roll": "!egg"}],
    [1.05, "fx", "tto/missilePad_launch", {"x": 0.128, "y": 0.64, "d": -1.478, "rot": [-72.2, -90, 0]}],
    [1.05, "fx", "tto/missileBot_fire_bot", {"x": -0.18, "y": 1.59, "d": -1.48, "rot": [-72.2, -90, 0], "to": [0, 0.6, 10], "kill": 1.942, "p": 0.05, "roll": "egg"}],
    [1.1, "fx", "tto/missileBot_fire", {"x": -0.09, "y": 1.59, "d": -1.44, "rot": [-72.2, -135, 0], "to": [0, 0.6, 10], "kill": 2.233, "p": 0.05, "roll": "!egg"}],
    [1.1, "fx", "tto/missilePad_launch", {"x": 0.128, "y": 0.64, "d": -1.223, "rot": [-72.2, -135, 0]}],
    [1.1, "fx", "tto/missileBot_fire_bot", {"x": -0.09, "y": 1.59, "d": -1.44, "rot": [-72.2, -135, 0], "to": [0, 0.6, 10], "kill": 2.233, "p": 0.05, "roll": "egg"}],
    [1.15, "fx", "tto/missileBot_fire", {"x": -0.13, "y": 1.59, "d": -1.78, "rot": [-72.2, -180, 0], "to": [0, 0.6, 10], "kill": 2.375, "p": 0.05, "roll": "!egg"}],
    [1.15, "fx", "tto/missilePad_launch", {"x": -0.128, "y": 0.64, "d": -1.478, "rot": [-72.2, -180, 0]}],
    [1.15, "fx", "tto/missileBot_fire_bot", {"x": -0.13, "y": 1.59, "d": -1.78, "rot": [-72.2, -180, 0], "to": [0, 0.6, 10], "kill": 2.375, "p": 0.05, "roll": "egg"}],
    [1.2, "fx", "tto/missileBot_fire", {"x": 0.09, "y": 1.59, "d": -1.44, "rot": [-72.2, -225, 0], "to": [0, 0.6, 10], "kill": 2.233, "p": 0.05, "roll": "!egg"}],
    [1.2, "fx", "tto/missilePad_launch", {"x": -0.128, "y": 0.64, "d": -1.223, "rot": [-72.2, -225, 0]}],
    [1.2, "fx", "tto/missileBot_fire_bot", {"x": 0.09, "y": 1.59, "d": -1.44, "rot": [-72.2, -225, 0], "to": [0, 0.6, 10], "kill": 2.233, "p": 0.05, "roll": "egg"}],
    [1.25, "fx", "tto/missileBot_fire", {"x": 0.43, "y": 1.59, "d": -1.48, "rot": [-72.2, -270, 0], "to": [0, 0.6, 10], "kill": 1.95, "p": 0.05, "roll": "!egg"}],
    [1.25, "fx", "tto/missilePad_launch", {"x": 0.128, "y": 0.64, "d": -1.478, "rot": [-72.2, -270, 0]}],
    [1.25, "fx", "tto/missileBot_fire_bot", {"x": 0.43, "y": 1.59, "d": -1.48, "rot": [-72.2, -270, 0], "to": [0, 0.6, 10], "kill": 1.95, "p": 0.05, "roll": "egg"}],
    [1.3, "fx", "tto/missileBot_fire", {"x": 0.34, "y": 1.59, "d": -1.01, "rot": [-72.2, -315, 0], "to": [0, 0.6, 10], "kill": 1.675, "p": 0.05, "roll": "!egg"}],
    [1.3, "fx", "tto/missilePad_launch", {"x": 0.128, "y": 0.64, "d": -1.223, "rot": [-72.2, -315, 0]}],
    [1.3, "fx", "tto/missileBot_fire_bot", {"x": 0.34, "y": 1.59, "d": -1.01, "rot": [-72.2, -315, 0], "to": [0, 0.6, 10], "kill": 1.675, "p": 0.05, "roll": "egg"}],
    [2.558, "fx", "tto/missileBot_hit", {"x": -0.01, "y": 1.13, "d": 9.5, "p": 0.05, "roll": "!egg"}],
    [2.558, "fx", "tto/missileBot_hit", {"x": -0.01, "y": 1.13, "d": 9.5, "p": 0.05, "roll": "egg"}],
    [2.675, "fx", "tto/missileBot_hit", {"x": -0.18, "y": 1.2, "d": 9.55, "p": 0.05, "roll": "!egg"}],
    [2.675, "fx", "tto/missileBot_hit", {"x": -0.18, "y": 1.2, "d": 9.55, "p": 0.05, "roll": "egg"}],
    [2.675, "fx", "tto/twinImpact", {"x": -0.18, "y": 1.2, "d": 9.55, "p": 0.05, "roll": "!egg"}],
    [2.975, "fx", "tto/missileBot_hit", {"x": 0.18, "y": 1.2, "d": 9.55, "p": 0.05, "roll": "!egg"}],
    [2.975, "fx", "tto/missileBot_hit", {"x": 0.18, "y": 1.2, "d": 9.55, "p": 0.05, "roll": "egg"}],
    [2.992, "fx", "tto/missileBot_hit", {"x": -0.31, "y": 1.2, "d": 9.64, "p": 0.05, "roll": "!egg"}],
    [2.992, "fx", "tto/missileBot_hit", {"x": -0.31, "y": 1.2, "d": 9.64, "p": 0.05, "roll": "egg"}],
    [3.2, "fx", "tto/missileBot_hit", {"x": 0.32, "y": 1.2, "d": 9.65, "p": 0.05, "roll": "!egg"}],
    [3.2, "fx", "tto/missileBot_hit", {"x": 0.32, "y": 1.2, "d": 9.65, "p": 0.05, "roll": "egg"}],
    [3.2, "fx", "tto/twinImpact", {"x": 0.32, "y": 1.2, "d": 9.65, "p": 0.05, "roll": "!egg"}],
    [3.333, "fx", "tto/missileBot_hit", {"x": -0.24, "y": 1.2, "d": 9.82, "p": 0.05, "roll": "!egg"}],
    [3.333, "fx", "tto/missileBot_hit", {"x": -0.24, "y": 1.2, "d": 9.82, "p": 0.05, "roll": "egg"}],
    [3.333, "fx", "tto/twinImpact", {"x": -0.24, "y": 1.2, "d": 9.82, "p": 0.05, "roll": "!egg"}],
    [3.433, "fx", "tto/missileBot_hit", {"x": 0.24, "y": 1.2, "d": 9.82, "p": 0.05, "roll": "!egg"}],
    [3.433, "fx", "tto/missileBot_hit", {"x": 0.24, "y": 1.2, "d": 9.82, "p": 0.05, "roll": "egg"}],
    [3.525, "fx", "tto/missileBot_hit", {"x": 0.0, "y": 1.2, "d": 9.72, "p": 0.05, "roll": "!egg"}],
    [3.525, "fx", "tto/missileBot_hit", {"x": 0.0, "y": 1.2, "d": 9.72, "p": 0.05, "roll": "egg"}],
    [3.525, "fx", "tto/twinImpact", {"x": 0.0, "y": 1.2, "d": 9.72, "p": 0.05, "roll": "!egg"}]
    ]
  },
  "kaiserArsenal": {
    "why": "TTO1102:KingKaiser.<RPC_kaiserArsenal>d__72::MoveNext@0x1CB7460 (pseudo_c6_extra/mole/KingKaiser.c:206-656; plans/fx_mole/tto.md 2.3), the King Kaiser's move (question 4: the page plays the clip on the Mole): CrossFade(arsenal = mole/animations/kaiserArsenal, 0.2) (:308-329); Waits 0.6: KingKaiser::SpawnPods@0x1CB19A0: kaiserArsenalPod on the Kaiser's Arm_R and Arm_L bones, localPosition 0, localRotation LookRotation(left, forward) (KingKaiser.c:7256-7320), Wear(the Kaiser's material), and assemble_dust at the Kaiser with its rotation, scale 1.6 (:7354-7366), then PlayOneShot(kaiser_openFx = clip kaiser_open) (:357-366); the pods' locks (KaiserArsenalPod.Locks (0.38, 0.6), (0.68, 1.0), (0.85, 0.45), (0.98, 0.5) after Unfold; KaiserArsenalPod::.cctor@0x1CAD990, resolved with the Bible's tools/usages.py) -> KingKaiser::PodLock@0x1CB08B0: barrelRailgun_lock at the pod's lock point, scale 1.2 + 1.2 clank, nAttack_hit / megaPunch_hit at 0.3 + 0.4 clank (part P11); Waits 1.2: 16 shots 0.1 s apart from 1.8 s, shot k on pod k % 2 (:484-603): KaiserArsenalPod.Kick -> its muzzle, dir = normalize(muzzle.forward + 0.35 up), KingKaiser::ArsenalShot@0x1CAF000: kaiserArsenal_muzzle at the muzzle, LookRotation(dir), TwinSound missile_fire 0.55, FireWarhead(arsenal, life 3.5): kaiserWarhead at the muzzle, LookRotation(dir) (KaiserWarhead::Update@0x1CAE4A0: 12 m/s, 0.4 rad toward the target every 0.15 s; Land@0x1CADC40 on contact or at 3.5 s -> KingKaiser::WarheadLanded@0x1CB2E70 -> RPC_kaiserArsenal_hit@0x1CB0CA0: kaiserArsenal_hit there with the Kaiser's rotation): the pod part spawns the flashes, warheads and hits (builds); at 3.5 s the pods fold and TwinSound nAttack_hit 0.5 (:620-653); Waits 0.7: DropPods(false) at 4.2 (kill 3.6 after the 0.6 s spawn); standby at 4.4, the clip's length",
    "builds": ["tto/kaiserArsenal_muzzle", "tto/kaiserWarhead", "tto/kaiserArsenal_hit", "tto/barrelRailgun_lock", "sound:nAttack_hit", "sound:megaPunch_hit"],
    "cues": [
    [0.6, "fx", "tto/kaiserArsenalPod", {"bone": "Arm_R", "rot": [0, -90, -90], "kill": 3.6, "fold": 2.9, "kicks": [1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6], "to": [0, 0.6, 10]}],
    [0.6, "fx", "tto/kaiserArsenalPod", {"bone": "Arm_L", "rot": [0, -90, -90], "kill": 3.6, "fold": 2.9, "kicks": [1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5, 2.7], "to": [0, 0.6, 10]}],
    [0.6, "fx", "assemble_dust", {"scale": 1.6}],
    [0.6, "sound", "kaiser_open"],
    [1.8, "sound", "missile_fire", {"vol": 0.55}],
    [1.9, "sound", "missile_fire", {"vol": 0.55}],
    [2.0, "sound", "missile_fire", {"vol": 0.55}],
    [2.1, "sound", "missile_fire", {"vol": 0.55}],
    [2.2, "sound", "missile_fire", {"vol": 0.55}],
    [2.3, "sound", "missile_fire", {"vol": 0.55}],
    [2.4, "sound", "missile_fire", {"vol": 0.55}],
    [2.5, "sound", "missile_fire", {"vol": 0.55}],
    [2.6, "sound", "missile_fire", {"vol": 0.55}],
    [2.7, "sound", "missile_fire", {"vol": 0.55}],
    [2.8, "sound", "missile_fire", {"vol": 0.55}],
    [2.9, "sound", "missile_fire", {"vol": 0.55}],
    [3.0, "sound", "missile_fire", {"vol": 0.55}],
    [3.1, "sound", "missile_fire", {"vol": 0.55}],
    [3.2, "sound", "missile_fire", {"vol": 0.55}],
    [3.3, "sound", "missile_fire", {"vol": 0.55}],
    [3.5, "sound", "nAttack_hit", {"vol": 0.5}]
    ]
  }
}
```

**Shared change S1 (`index.html` SEQ, mole; needs P13's start time, written here as `>0.55`):**

```
"Barrel Railgun: assemble1@0.6 assemble2*@5.4 barrelRailgun1>0.55^@0.65 barrelRailgun2*^@2.2 barrelRailgun3^0.05@0.5 barrelRailgun2*^@1.9 barrelRailgun3^0.05@0.5 barrelRailgun2*^@1.9 barrelRailgun3^0.05@0.5 barrelRailgun2*^@1.9 barrelRailgun3^0.05@0.5 barrelRailgun2*^@0.1 barrelRailgun4^0.05@0.5"
```

0.6 + 5.4 + 0.65 + 2.2 + 4 x 0.5 + 3 x 1.9 + 0.1 + 0.5 = 17.15 s = standby (2.1). The first step keeps the page's 0.2 s
fade (= the game's assemble1 fade); assemble2 cuts in (the game's `PlayAnimation(assemble2, 0)`). With the full ride
(question 1, option B): four more `barrelRailgun3^0.05@0.5 barrelRailgun2*^@1.9` pairs, the last `barrelRailgun2*^@1.0`
(ride 19.5 -> 20.0), and the turret's `kill` 27.45, `shots` to 25.65, `rideEnd` 26.65.

## 8. Open questions (each with my recommended answer)

1. **Barrel Railgun's ride: 10 s or the game's fixed 20 s?** Recommend **10 s** (4 shots), the rule's cut for long fields
   (Sheep decision 19, Bat's Mind Control at 10 s), and a real game path: the player presses the skill again to get off
   (`TryRecast`, Bible :757). B: the full 20 s, 8 shots, a 27.45 s tile.
2. **The Mole on the turret** (the hop onto the seat 0.63 m up, the hop off to 0.8 m left): recommend **build P14** (a
   3-axis lift); without it the Mole stands inside the turret's back for 10 s, its feet 0.63 m under the seat. (Penguin
   decision 8 kept Frost Field's leap in place, but there the hero only moved along the ground.)
3. **The 5 % egg**: recommend **as the game** (the rule "random picks as the game does them"): one roll per play, all 8
   missiles MissileBots that split into 8 each (P9). Alternative: never the egg.
4. **Kaiser Arsenal on the page**: the clip is the King Kaiser's (its rig), the pods hang on its arms, and its 16 warheads
   leave from them. Recommend **the King Kaiser for this tile** (P17 = `parts.md` part 11, which its question 8 also
   recommends), the cues as written (bones Arm_R / Arm_L are the Kaiser's). Until then the tile plays the Kaiser's clip on
   the Mole (the shared bone names Arm_L / Arm_R / Head ... take the Kaiser's poses), and the cues as written put the pods
   on the Mole's arms at the Kaiser's scale (their rack reaches 1.32 m).
5. **The missile hits: cued or part-made?** Recommend **cued** at the simulated times (section 7; the same as the
   Penguin's computed ball), P9 removing each missile at its `kill`. Alternative: P9 detects arrival at `to` and spawns the
   hit and the pair's blast itself (builds), exact to its own flight.
6. **Unowned followState roots** (`barrelRailgun_blast`, `barrelRailgun_rip`): recommend **`cut` at the spawn**, as the
   game's no-owner after-life (EffectControl.cs:194-210). A general fix (a cue option `owned: false`, or the exporter
   marking bare-Instantiate roots) would cover other classes too; the `cut` needs no page change.
7. **The pad's and the turret's lock points**: the turret's 13 locks are cued at the parts' pivots (root / Head / gun);
   recommend keeping them cued (fixed times, `steps.txt`) rather than P1 spawning them, so the BB-style sounds stay
   visible in the cue file. (The pods' locks stay P11's: their points ride the Kaiser's arms.)

## 9. For the Bible (offer to the user; that repo's own rules)

- **Barrel Railgun:** the 6 s cast plays Assemble's two clips while the turret builds itself in 13 timed steps (0.2-5.61 s,
  `MoleRailTurret.Steps`); the hop is `barrelRailgun1` from 0.55 s; the Mole rides 0.63 m up on a seat 0.55 m ahead; each
  shot plays `barrelRailgun3` for 0.5 s; the charge sound (teslaCoil) rises 0.6 / 1.3 / 2.0 s into each 2.4 s cycle; at
  the end the Mole hops off to the turret's left and the turret shrinks away over 0.3-0.8 s; the trench crackles with
  sparks for 2.4 s; the beam's slug flies 160 m/s.
- **Missile with Twin Warhead:** the launch pad stands 1.35 m **behind** the Mole and sinks 0.45 s after the last launch
  (gone at 2.3 s); the missiles fly at **8 m/s**, climbing at 72 degrees, turning at most 0.3 rad every 0.2 s: on a 10 m
  target they land 2.6-3.5 s after the cast (Bible :745 "not computable": now from TTO's bundles). The lock beeps once
  per target (`sound/gui/beep`).
- **Kaiser Arsenal:** the warheads fly at **12 m/s**, turning 0.4 rad every 0.15 s; the pods unfold at 0.6 s on both arms
  (locks at 0.98-1.58 s), the shots alternate arms, the pods fold at 3.5 s and go at 4.2 s.

## Verification (the researcher's own checks)

- Every wait Ghidra dropped was read from the instructions (`missile_movenext.asm`: 0.3, 0.65, 0.05, the 0.35 - 0.05 x 7
  wait, SinkIn 0.45) or is a labelled DAT constant in the pseudo-C (Barrel Railgun 0.6 / 6 / 0.55 / 0.85 / 1.2 / 2.4 / 2.2
  / 20; the overload 0.7; the end 0.08 / 0.32 / 0.42 / 0.3 / 0.5 / 0.8; Kaiser Arsenal 0.6 / 1.2 / 0.1 / 3.5 / 0.7 / 4.4).
- Steps (`steps.txt`): the parts' names come from the `local_* = String` lines, the 16-byte (from, to, offset.x,
  offset.y) pairs from the DLL at the `uVar4 = _DAT_` addresses (the Seat's through its `s_..._183005490` alias), the axis
  from the last `Vector3.<axis>Vector` before each element; array stride 0x30 (MoleRailTurret.Step, `dump.cs:108430-108444`).
- Tables: RailTierAt [0, 0.6, 1.3, 2.0], MoleLaunchPad.Locks, MoleRailBeam.Width, MoleRailgun OrbSize / ArcGap are the
  annotator's `InitializeArray` labels; KaiserArsenalPod.Locks is usages.py's resolution of the field slot 0x183809600 its
  .cctor loads (0x1CAD9B7).
- `kaiser_open`: the KingKaiser MonoBehaviour's `kaiser_openFx` in TTO's KingKaiser_b bundle (`kaiser_tto.txt`), present in
  BB's rip as `Assets/AudioClip/kaiser_open.wav`. BB's resources.assets MonoBehaviours have no type tree
  (`kaiser_clips.txt` empty).
- `cues_paste.json` parses (`cues.py` json.loads), 131 cues; every fx name is in `probe.json` (tto/) or BB's rip
  (assemble_box, assemble_dust, chopper_forwardDust); every sound in BB's `sounds/` or voices/ except beep and kaiser_open
  (P15).
- Not done: a browser check (read-only researcher); the missile simulation's contact radius (0.5 m) and the target's
  1.2 m bounds are assumptions (P9 decides); KaiserArsenalPod's and MoleLockReticle's code beyond the numbers above.

## Verification

Checker, 13/11/2026, home PC, read only (`TTO1102:pseudo/Mole.c`, `pseudo_c6_extra/mole/*.c`, `dump.cs`, `methods.tsv`,
the DLL's constants read again with `checks/fx_mole_research/verify_tp/rd.py`, `wardrobe/index.html`; probes and outputs in
`checks/fx_mole_research/verify_tp/`). Re-derived and **confirmed**: every Barrel Railgun time, fade and wait
(`Mole.c:2840`, `:2944`, `:2960-2977` (assemble2 fade 0, the box owned), `:3005`, `:3019-3029` (fade 0.1, time 0.55, the
clock `now - 0.55`), `:3100` (1.2), `:3139-3144`, `:3170-3171` (0x404ccccd = 3.2), `:3242-3360` (2.4 / 0.6 / 1.3 / 2.0 /
2.2 / 20.01 / 20, teslaCoil 0.4 + 0.15 t)); the 13 Steps' from / to / offset y (DLL 0x183005550 ... 0x1830054e0,
`rd.py`); the lock at the part's world position when k reaches 1 (`MoleRailTurret.c:695-704`), BackOut and the spin law
(`:650-690`); the pivots, SeatAnchor (0, 0.03, -0.62) and Muzzle (0, 0, 1.42) (`compact.txt`); RailLock scale 0.6 + 0.8 c,
dust >= 0.9 at mRailSpot, megaPunch >= 0.7, volume 0.25 + 0.35 c (`Mole.c:40428-40494`), so all 13 lock cues (times,
scales, volumes, spots); the shot (`:3784-3925`: tier 3, the beam / muzzle / recoil / blast spots, bazooka_fire 1,
superTNT_hit 0.6, the 0.5 wait, barrelRailgun3 fade 0.05), RailRip (s = 2 ... 44 step 3, the first at 0,
`Waits.Get(0.01875)`, `:24361-24455`), RailTrenchSparks' ranges (`:24798-24878`), the overload's three 0.7 s shocks and the
aura's end after the third (`:4100-4295`); the S1 SEQ line sums to 17.15 s and every token but the new `>0.55` matches
`SEQ_ALT` (`index.html:1325`); the Missile's HasMissileBot = hasSkill(0x1c5 = 453), 2 x rank, the 0.05 egg (a double at
0x183005378), PickLocks((8 + 1) / 2), the waits 0.3 / 0.65 / 0.05 (DLL 0x1830043a4 / 0x1830043b4 / 0x182f3ff30, the
rip-relative targets recomputed), the fire direction's 0.45 / 1.4 (the pairs at 0x183005240 / 0x1830053e0), rotateH's sign
(`Math.cs:838-843`), all eight muzzle, launch and spawn spots and rotations (worked by hand), the pad's Locks table
(`MoleLaunchPad.c:480`: 0.45 / 1.0, 0.6 / 0.5, 0.72 / 0.6), lock 0 at the pad's own position (`:187-198`), SinkIn, the
0.55 s sink and the destroy (`:41-55`, `:150-166`), sound/gui/beep 0.6 (an AddressableLoader clip in TTO; BB's rip has
`Resources/sound/gui/beep.ogg`) and kaiser_open (`RippedAssets/ExportedProject/Assets/AudioClip/kaiser_open.wav`); Kaiser
Arsenal's waits 0.6 / 1.2 / 0.1 x 16 / 3.5 / 0.7 / 4.4 and the fold sound (`KingKaiser.c:279-652`), pods[0] = Arm_R,
pods[1] = Arm_L, shot k on pod k % 2 (`:7266-7270`, `:493-540`), LookRotation(left, forward) = Euler (0, -90, -90)
(worked by hand), assemble_dust x 1.6 (`:7366`); every RVA in sections 1-2 and `parts.md`'s TTO table (`methods.tsv`); the
pod fields (`dump.cs:109601-109623`). Every cued sound is in BB's rip, every `tto/` name is in `probe.json`, the bones
Arm_R / Arm_L / mount_Cannon are in `data/mole/rig.json`, and the block parses (131 cues, the same as `cues_paste.json`).

**Corrections**

1. **The missile hits are timed on a non-standard target** (section 2.2 "The flights", section 7 `missilePad`, section 9's
   Bible line; `missile_sim.py`: contact within 0.5 m of the axis and up to y 1.7, the hit points clamped to y 1.2). Every
   class uses one body (Bat decision 4, `plans/fx_bat/decisions.md:18`; Penguin decision 3): radius 0.3, y 0.1-1.1,
   ClosestPointOnBounds clamped into x +-0.3, y 0.1..1.1, z 9.7..10.3; `parts.md` "Each part" uses it too. TTO's missile
   trigger is 0.2 x 0.2 x 0.5 centred 0.25 ahead (`probe.json`, missileBot_fire's BoxCollider) and the hit point is the
   body's ClosestPointOnBounds of that collider's bounds centre (`Mole.c:44427-44437`). Re-run on that body
   (`checks/fx_mole_research/verify_tp/missile_sim2.py` -> `missile_sim2.txt`): hits at **2.550, 2.683, 3.025, 3.375, 3.567,
   3.475, 3.233, 2.983 s** (missiles 0-7), all at y **1.1**, d 9.70-9.87; the pairs' second hits **2.683, 3.375, 3.567,
   3.233** (gaps 0.13 / 0.35 / 0.09 / 0.25: all four still blast). The missiles' `kill` change with them. Section 9: "land
   2.55-3.57 s after the cast".
2. **The egg keeps the gold blasts** (Read this first 7, section 2.2 "The egg", section 7: `twinImpact` cued only on
   `!egg`). `Mole::FireMissile` sets `twin = hasSkill(453)` and `pair = pendingTwinPair` whatever the prefab, the egg's too
   (`Mole.c:34137-34143`), and `Mole_missile::OnTriggerEnter` calls `RPC_missile_hit`, then `MissileBotScatter` when
   `scatter`, then (the target damaged, `twin` set) `WarheadHit` (`:44453-44537`): an egg pair hitting within 0.5 s makes
   the gold blast as well as splitting. The four `twinImpact` cues lose their `p` / `roll`; the two `missileBot_hit` cues
   per missile (`egg` and `!egg`, the same spot) become one plain cue each.
3. **The split missiles can make gold blasts too** (P9; the Bible's :741 says "no gold blast"): `MissileBotScatter` fires
   through the same `FireMissile` (`Mole.c:37069`) and never resets `pendingTwinPair` (no write to 0x7f4 in
   `:36919-37112`), so all 64 carry the last pair's id with `twin` true; on one target, the second of every two hits within
   0.5 s goes through `WarheadHit`'s TryGetValue / Remove into `TwinImpact` (`:37276-37367`). P9 should keep a
   `twinFirstHit` map for its splits (medium sure: read from the pseudo-C, not run). Their direction is
   `normalize(rotateH(the hero's forward + 0.3 up, 45 i))` from the hit + 1 up (`:36986-37064`): the hero's forward, not
   the missile's (add to P9). A Bible item to offer the user.
4. **Counts** (Read this first 4, P16): the catalog's TTO-only effects are 1 barrelBot_warhead + **14** barrelRailgun*
   (not 15) + 4 kaiser* + 6 missile* / missilePad* + twinImpact + 6 warArea_* + 2 warCapital_* = 34 (`catalog.txt:24`);
   **24** prefabs to build (25 probed with the unused gun; P16: 24).
5. **S1, option B** (section 7, under the SEQ line): after the 8th shot (ride 19.0) comes barrelRailgun3 for 0.5 s, then
   **`barrelRailgun2*^@0.5`** (ride 19.5 -> 20.0), not `@1.0`: the 4th shot's `barrelRailgun2*^@0.1` becomes `@1.9`, then
   four `barrelRailgun3^0.05@0.5 barrelRailgun2*^@1.9` pairs whose last `barrelRailgun2` is `@0.5`; the tile is 27.15 s.
6. **Line refs:** P15's `hero_sound_wav` is `pipeline/wardrobe_fx.py:583` today (not :522).

**Notes (no cue changes)**
- The egg's roll is seeded from the cast position (`System.Random(round(50 z) x 0x127409f ^ round(50 x) x 0x466f45d)`,
  `Mole.c:36818-36823`): at one spot the game always gives the same answer; the page's 5 % per play is the game's odds
  over spots (question 3's recommendation stands).
- With the page's loop toggle on (`skillLoop`, `index.html:1438`), a single clip restarts at its end and its unreached cues
  are dropped (`seqTick`, `fxStart`): `missilePad` (1.3 s) would lose every hit at 2.55-3.57 s. Off (the default), the idle
  tail keeps them. If they must survive the loop, a one-step SEQ `"Missile Pad: missilePad@3.6"` holds the tile (as the
  Chameleon's `rainOfArrow@2.7`, `index.html:1246`); the plain `missilePad` key still matches.
- `RailLock`, `MissilePadLock` and `SpawnPods` load `assemble_dust` / `chopper_forwardDust` from TTO's
  `heroes/mole/effects` (`WarAreaPrefab`, `Mole.c:40474`, `:38428`); cueing BB's rip copies stands (Bison decision 43).

**Corrected paste-ready block set.** `@BarrelRailgun:assemble1`, `@BarrelRailgun:assemble2`,
`@BarrelRailgun:barrelRailgun3` and `kaiserArsenal` are unchanged; this `missilePad` replaces section 7's (47 cues; the
file then holds 123). Checked: it parses (`json.loads`), the names as before.

```json
  "missilePad": {
    "why": "TTO1102:Mole.<RPC_missile>d__344::MoveNext@0x1C78270 (pseudo/Mole.c:15978-16471; plans/fx_mole/tto.md 2.2), Twin Warhead learned (passives on; without it OldMissile plays BB's missile clip): Missile rank 4 -> 8 missiles (Mole::MissileBotLevel@0x1C2DFD0); the clip, fade 0.05 (:16116-16125); Mole::MissileVoice@0x1C2EA40: missile1 / missile2, Random.Range(0, 2) (voices/); Mole::SpawnMissilePad@0x1C3D4D0 at mPos - 1.35 forward, the hero's rotation (:16143-16149): missilePad + assemble_dust there + sounds/missile_base; the pad's locks (MoleLaunchPad.Locks (0.45, 1.0), (0.6, 0.5), (0.72, 0.6), MoleLaunchPad::.cctor@0x1C82740) -> Mole::MissilePadLock@0x1C2E7C0: nAttack_hit / megaPunch_hit at 0.25 + 0.35 clank, and for clank >= 0.9 chopper_forwardDust at the pad with the hero's rotation (the camera shake is the player's screen: left out); Waits 0.3 (capstone 0x1C7871E): PickLocks((8 + 1) / 2) = the one target, LockSequence -> RPC_missile_lock@0x1C352E0: missile_lock at its bounds centre, identity, parented to it, scale 1 for a hero-sized foe, and sound/gui/beep at 0.6 (Mole.c:38686-38806); Waits 0.65 (0x1C788FA): sounds/missile_fire, then missile i every 0.05 s (0x1C78D98), fire dir = normalize(rotateH(forward, 45 i) x 0.45 + up x 1.4) (:16316-16333; Math.rotateH turns to the left, DecompiledSource/Math.cs:838-843), from the pad's next muzzle (NextMuzzle cycles Muzzle0-3; the pad scaled 0.85, the rack raised 0.22: 0.64 m up): RPC_missile_fire@0x1C34DE0: MoleLaunchPad.Kick, missilePad_launch at the muzzle, LookRotation(dir); FireMissile@0x1C2B3C0: missileBot_fire (the egg missileBot_fire_bot when the cast's 5 % roll hit, MissileBotLevel) at muzzle + dir, LookRotation(dir); Mole_missile turns 0.3 rad toward the target's bounds centre every 0.2 s at 8 m/s (Mole_missile::Update@0x1CA0660; checks/fx_mole_research/verify_tp/missile_sim2.py on the standard target body (Bat decision 4: radius 0.3, y 0.1-1.1, ClosestPointOnBounds clamped into x +-0.3, y 0.1..1.1, z 9.7..10.3; TTO missileBot_fire trigger 0.2 x 0.2 x 0.5 centred 0.25 ahead): hits 2.55-3.57 s); RPC_missile_hit@0x1C35100: missileBot_hit at the hit point (ClosestPointOnBounds: the top of the target), the hero's rotation; Mole::WarheadHit@0x1C3FFE0: a pair's second hit within 0.5 s -> TwinImpact -> RPC_twinImpact@0x1C39D90: twinImpact there, LookRotation(flat dir), 4 pairs, egg or not (FireMissile sets twin = hasSkill(453) for the egg prefab too, Mole.c:34141-34143, and OnTriggerEnter calls MissileBotScatter and then WarheadHit, :44470-44537); an egg's hit also splits (Mole::MissileBotScatter@0x1C2E1E0, part P9); SinkIn(0.45) at 1.30 (0x1C78ED1): the pad sinks over 0.55 s and is destroyed at 2.30 (MoleLaunchPad::Update@0x1C82450). LinkedSalvo (Auto Gyro Guns within 20 m) has nothing to fire here",
    "cues": [
    [0, "voice", "missile1|missile2"],
    [0, "fx", "tto/missilePad", {"d": -1.35, "sink": 1.75, "kill": 2.3, "kicks": [0.95, 1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3]}],
    [0, "fx", "assemble_dust", -1.35],
    [0, "sound", "missile_base"],
    [0.3, "fx", "tto/missile_lock", {"y": 0.6, "d": 10}],
    [0.3, "sound", "beep", {"vol": 0.6}],
    [0.45, "sound", "megaPunch_hit", {"vol": 0.6}],
    [0.45, "fx", "chopper_forwardDust", -1.35],
    [0.6, "sound", "nAttack_hit", {"vol": 0.425}],
    [0.72, "sound", "nAttack_hit", {"vol": 0.46}],
    [0.95, "sound", "missile_fire"],
    [0.95, "fx", "tto/missileBot_fire", {"x": -0.13, "y": 1.59, "d": -1.17, "rot": [-72.2, 0, 0], "to": [0, 0.6, 10], "kill": 1.6, "p": 0.05, "roll": "!egg"}],
    [0.95, "fx", "tto/missilePad_launch", {"x": -0.128, "y": 0.64, "d": -1.478, "rot": [-72.2, 0, 0]}],
    [0.95, "fx", "tto/missileBot_fire_bot", {"x": -0.13, "y": 1.59, "d": -1.17, "rot": [-72.2, 0, 0], "to": [0, 0.6, 10], "kill": 1.6, "p": 0.05, "roll": "egg"}],
    [1.0, "fx", "tto/missileBot_fire", {"x": -0.34, "y": 1.59, "d": -1.01, "rot": [-72.2, -45, 0], "to": [0, 0.6, 10], "kill": 1.683, "p": 0.05, "roll": "!egg"}],
    [1.0, "fx", "tto/missilePad_launch", {"x": -0.128, "y": 0.64, "d": -1.223, "rot": [-72.2, -45, 0]}],
    [1.0, "fx", "tto/missileBot_fire_bot", {"x": -0.34, "y": 1.59, "d": -1.01, "rot": [-72.2, -45, 0], "to": [0, 0.6, 10], "kill": 1.683, "p": 0.05, "roll": "egg"}],
    [1.05, "fx", "tto/missileBot_fire", {"x": -0.18, "y": 1.59, "d": -1.48, "rot": [-72.2, -90, 0], "to": [0, 0.6, 10], "kill": 1.975, "p": 0.05, "roll": "!egg"}],
    [1.05, "fx", "tto/missilePad_launch", {"x": 0.128, "y": 0.64, "d": -1.478, "rot": [-72.2, -90, 0]}],
    [1.05, "fx", "tto/missileBot_fire_bot", {"x": -0.18, "y": 1.59, "d": -1.48, "rot": [-72.2, -90, 0], "to": [0, 0.6, 10], "kill": 1.975, "p": 0.05, "roll": "egg"}],
    [1.1, "fx", "tto/missileBot_fire", {"x": -0.09, "y": 1.59, "d": -1.44, "rot": [-72.2, -135, 0], "to": [0, 0.6, 10], "kill": 2.275, "p": 0.05, "roll": "!egg"}],
    [1.1, "fx", "tto/missilePad_launch", {"x": 0.128, "y": 0.64, "d": -1.223, "rot": [-72.2, -135, 0]}],
    [1.1, "fx", "tto/missileBot_fire_bot", {"x": -0.09, "y": 1.59, "d": -1.44, "rot": [-72.2, -135, 0], "to": [0, 0.6, 10], "kill": 2.275, "p": 0.05, "roll": "egg"}],
    [1.15, "fx", "tto/missileBot_fire", {"x": -0.13, "y": 1.59, "d": -1.78, "rot": [-72.2, -180, 0], "to": [0, 0.6, 10], "kill": 2.417, "p": 0.05, "roll": "!egg"}],
    [1.15, "fx", "tto/missilePad_launch", {"x": -0.128, "y": 0.64, "d": -1.478, "rot": [-72.2, -180, 0]}],
    [1.15, "fx", "tto/missileBot_fire_bot", {"x": -0.13, "y": 1.59, "d": -1.78, "rot": [-72.2, -180, 0], "to": [0, 0.6, 10], "kill": 2.417, "p": 0.05, "roll": "egg"}],
    [1.2, "fx", "tto/missileBot_fire", {"x": 0.09, "y": 1.59, "d": -1.44, "rot": [-72.2, -225, 0], "to": [0, 0.6, 10], "kill": 2.275, "p": 0.05, "roll": "!egg"}],
    [1.2, "fx", "tto/missilePad_launch", {"x": -0.128, "y": 0.64, "d": -1.223, "rot": [-72.2, -225, 0]}],
    [1.2, "fx", "tto/missileBot_fire_bot", {"x": 0.09, "y": 1.59, "d": -1.44, "rot": [-72.2, -225, 0], "to": [0, 0.6, 10], "kill": 2.275, "p": 0.05, "roll": "egg"}],
    [1.25, "fx", "tto/missileBot_fire", {"x": 0.43, "y": 1.59, "d": -1.48, "rot": [-72.2, -270, 0], "to": [0, 0.6, 10], "kill": 1.983, "p": 0.05, "roll": "!egg"}],
    [1.25, "fx", "tto/missilePad_launch", {"x": 0.128, "y": 0.64, "d": -1.478, "rot": [-72.2, -270, 0]}],
    [1.25, "fx", "tto/missileBot_fire_bot", {"x": 0.43, "y": 1.59, "d": -1.48, "rot": [-72.2, -270, 0], "to": [0, 0.6, 10], "kill": 1.983, "p": 0.05, "roll": "egg"}],
    [1.3, "fx", "tto/missileBot_fire", {"x": 0.34, "y": 1.59, "d": -1.01, "rot": [-72.2, -315, 0], "to": [0, 0.6, 10], "kill": 1.683, "p": 0.05, "roll": "!egg"}],
    [1.3, "fx", "tto/missilePad_launch", {"x": 0.128, "y": 0.64, "d": -1.223, "rot": [-72.2, -315, 0]}],
    [1.3, "fx", "tto/missileBot_fire_bot", {"x": 0.34, "y": 1.59, "d": -1.01, "rot": [-72.2, -315, 0], "to": [0, 0.6, 10], "kill": 1.683, "p": 0.05, "roll": "egg"}],
    [2.55, "fx", "tto/missileBot_hit", {"x": -0.01, "y": 1.1, "d": 9.7}],
    [2.683, "fx", "tto/missileBot_hit", {"x": -0.17, "y": 1.1, "d": 9.7}],
    [2.683, "fx", "tto/twinImpact", {"x": -0.17, "y": 1.1, "d": 9.7}],
    [2.983, "fx", "tto/missileBot_hit", {"x": 0.17, "y": 1.1, "d": 9.7}],
    [3.025, "fx", "tto/missileBot_hit", {"x": -0.23, "y": 1.1, "d": 9.73}],
    [3.233, "fx", "tto/missileBot_hit", {"x": 0.24, "y": 1.1, "d": 9.73}],
    [3.233, "fx", "tto/twinImpact", {"x": 0.24, "y": 1.1, "d": 9.73}],
    [3.375, "fx", "tto/missileBot_hit", {"x": -0.17, "y": 1.1, "d": 9.87}],
    [3.375, "fx", "tto/twinImpact", {"x": -0.17, "y": 1.1, "d": 9.87}],
    [3.475, "fx", "tto/missileBot_hit", {"x": 0.17, "y": 1.1, "d": 9.87}],
    [3.567, "fx", "tto/missileBot_hit", {"x": 0.0, "y": 1.1, "d": 9.8}],
    [3.567, "fx", "tto/twinImpact", {"x": 0.0, "y": 1.1, "d": 9.8}]
    ]
  }
```

S1 is unchanged for the 10 s ride. Option B's tail: the 4th shot's `barrelRailgun2*^@0.1` made `@1.9`, then
`barrelRailgun3^0.05@0.5 barrelRailgun2*^@1.9` x 3, `barrelRailgun3^0.05@0.5 barrelRailgun2*^@0.5 barrelRailgun4^0.05@0.5`;
the turret's `kill` 27.45, `shots` [8.85, 11.25, 13.65, 16.05, 18.45, 20.85, 23.25, 25.65], `rideEnd` 26.65.
