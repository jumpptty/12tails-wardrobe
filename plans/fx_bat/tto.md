# Bat effects + sounds research: the TTO Lv 100 skill (Nightfall Swarm)

Scope: the TTO-only clip `nightfallSwarm` (1.4 s, `tto: true`, group `skill` in `wardrobe/data/bat/clips.json`). No BB
code plays it. **It is in the released list** (`wardrobe/tto_released.json`, bat clips: clap, nightfallSwarm, wai), so it
gets cues. Research only: this file is the only file written in `plans/`, plus the probes in
`checks/fx_bat_research/tto/` (git-ignored). Home PC, 2026-11-13.

Sources:
- TTO's pseudo-C `D:\12tails\DecompiledSource_TTO_2026-11-02\pseudo\Bat.c` (and `CharacterControl.c`), cited as
  `TTO1102:Method@RVA` plus `Bat.c:<line>`. (BUILD.md says line numbers change when the export is redone; the RVA is
  the stable cite, the line is for finding it today.)
- capstone over `client\GameAssembly.dll` for the floats Ghidra drops: `checks/fx_bat_research/tto/dis.py` (the Wolf's)
  -> `movenext.asm` (the coroutine), `flap.asm` (BatSwarmFlap).
- The Bible: `12t_reference/bat-skill-reference.md` "TTO Lv 100 skills" (:669-727; Nightfall Swarm :706-718) and the
  card `bat_nightfallSwarm` in `12t_projects/bible/index.html` (:17526).
- TTO's bundles of 2026-11-04 (`D:\12tails-video\tto_assets\2026-11-04`, the home PC's `wardrobe_fx_tto.py` ASSETS):
  `wardrobe_fx_tto.py bat --probe nightfallSwarm_wrap,nightfallSwarm_burst,nightfallSwarm_bat,nightfallSwarm_hit,nightfallSwarm_reform`
  -> `probe.json`, summarised by `compact.py` -> `compact.txt`. `sounds.py` -> `sounds.txt` (the sounds in BB's rip and
  TTO's catalog), `cc.py` -> `cc.txt` (the Bat's CharacterController), `calc.py` -> `calc.txt` (the numbers below),
  `cues.py` -> `cues.json` / `cues_block.txt` (section 7, parsed and checked).

Times are seconds from the start of the clip. Every wait is `Bat::Until(start + t)` (`TTO1102:Bat::Until@0x1AD3590`,
`Bat.c:45752`), the absolute-time wait every TTO class uses (the Penguin's `Until` has the same shape: wait while
`Time.time < t`), so each wait is a time from the coroutine's start, not a step to add. One rank (`bat_nightfallSwarm5`,
maxRank 1 on the card): max rank changes nothing.

## Read this first

1. **One clip, one tile, no cast bar.** `DoRow6Skill` starts the coroutine at the press (Bible :708: "no cast bar, no
   target needed"). The tile is the clip `nightfallSwarm` alone. Its 1.4 s length equals the coroutine's `Row6End` at
   `Until(start + 1.4)` (capstone 0x1B1069D: `addss xmm6, [0x3004950] = 1.4`). Cue key: `"nightfallSwarm"`. No SEQ.
2. **Five prefabs, all on this PC, no arcana style.** `nightfallSwarm_wrap`, `_burst`, `_bat` (x 28), `_hit`, `_reform`
   are at `gameassets/characters/heroes/bat/effects/<name>`. The catalog has no `heroes/bat/arcana/` address
   (`sounds.txt`).
3. **Four sounds, no voices.** Each one is `Row6Sound` = `PlayOneShot` of `GameAssets/characters/heroes/bat/sounds/<name>`,
   volume 1 for the owner (`TTO1102:Bat::Row6Sound@0x1AD00B0`, `Bat.c:45157`). So every cue is kind **`"sound"`**.
   - `bloodCarnage_ring` (1.158 s) and `drainLife` (2.017 s) are BB's own `bat/sounds/` recordings, the same length
     in TTO.
   - `nightfallSwarm_screech` (0.563 s) and `nightfallSwarm_flap` (0.714 s) are TTO-only (`sounds.txt`).
     `wardrobe_fx_tto.py` already fetches any `"sound"` cue that BB's rip lacks from TTO's catalog (part P8, built
     for the Penguin), so the build needs no new code for these two.
   - `Row6Voice` (`@0x1AD02B0`, which would pick from `voices/`) is never called. `bloodCarnage_ring` is also the name
     of a BB Bat effect, which is not spawned here: the cue kind keeps them apart.
4. **No roll, no passive.** The coroutine has no Random roll on a proc and checks no Mass Cast. `DoRow6Skill`'s Nightfall
   branch (`Bat.c:40711-40871`) only aims, sets the cooldown and starts the coroutine.
5. **Where it goes (the standing 10 m target).** With a foe selected within 18 m flat, the swarm flies toward it with
   length `clamp(distance + 2.5, 4, 18)` (`DoRow6Skill`, `Bat.c:40724-40762`: 18, 324 = 18², 2.5, 4). For the 10 m
   target that is **12.5 m**. Without a target it is 18 m forward.
6. **The Bat itself travels 12.5 m.** It is hidden while it does: `HideBody` at 0.4 s, `ShowBody` at 0.9 s, at the end
   of the road. The clip has no root motion: the root track's x and z hold still over the 1.4 s, and only y bobs. So
   the clip is made to play in place. This report cues it **in place** (the Penguin's decision 8, the Wolf's Feral Strike
   convention). The alternative, a hero mover, is open question 1.
7. **The 28 bats are moved by code, not by their prefab.** The coroutine flies them along the road with a per-bat lag,
   lane and wobble. `Regather` then pulls them into the Bat's chest. Their wings flap through a TTO script in the prefab
   (`BatSwarmFlap`). Parts P1 and P2 (section 6) are both missing from the page.
8. **One followState effect.** The wrap has `followPosition` and `followState` and is owned (`createEffect`). The
   hero's action changes at `Row6End`, 1.4 s, which gives the cue `cut: 1.4`. That cut is moot: the wrap's own life
   (0.5 + 0.3) ends at 0.8 s.
9. **The other two Bat TTO skills are not in scope and not released.** Crimson Verdict and Evil Twin go through
   `RPC_row6Cast@0x1B1F5F0`: cast1 and cast2, then a release clip `crimsonVerdict` / `evilTwin` (plus `massCast` with
   Mass Cast). Neither release clip is in `clips.json`, and neither skill is in `tto_released.json`, so they get no cues.

---

## 1. Shared machinery (`TTO1102:Bat`)

- **`Row6Begin(command, mPos, dir)@0x1ACEB30`** (`Bat.c:45321`): sets actionState `attack`, puts the Bat at mPos,
  `LookAt(mPos + vFlat(dir))` when |vFlat(dir)|² > 0.0001, `PlayAnimation(command, 0.1)` with wrapMode Once, and
  moveSpeed 0. So the game's `dir` is the hero's forward, as on the page.
- **`Row6End(command)@0x1ACF1F0`** (`:45553`): sets `standby`, but only while the action is still this command.
- **`Row6Spawn(name, pos, rot, owned)@0x1AD0180`** (`:45099`) loads the prefab through `Row6Prefab@0x1ACF570`
  (`GameAssets/characters/heroes/bat/effects/<name>`, `:45056`).
  - Owned: `CharacterControl.createEffect`. Otherwise a bare `Object.Instantiate`.
  - Only the wrap is owned.
- **`Row6Chest(cc)@0x1ACEE60`** (`:45694`) = `GetComponent<Collider>().bounds.center`, or position + up with no
  collider.
  - The Bat's own chest is **0.9 m up**: its CharacterController `m_Center` (0, 0.9, 0), height 1.7, radius 0.3. That
    is the same in TTO's `heroes/bat/bat` bundle (`cc.txt`) and BB's `Bat.prefab:905-911`.
  - A foe's chest is 0.6 m up, by the standing rule (Penguin decision 3: the CharacterController centre).
- **`HideBody()@0x1AC44A0`** (`:44595`) switches off every enabled Renderer under the Bat and keeps a list of them
  (`mSwarmHidden`). It skips:
  - ParticleSystemRenderer, TrailRenderer and LineRenderer;
  - anything under an `EffectControl` (`GetComponentInParent<EffectControl>`).

  **`ShowBody()@0x1AD0500`** (`:44673`) turns that list back on. The Bat can still be hit while hidden (Bible :710).

## 2. Nightfall Swarm (`nightfallSwarm`, 1.4 s; cell 454)

The press: `TTO1102:Bat::DoRow6Skill@0x1AC2660` (`Bat.c:40656`), branch `bat_nightfallSwarm5` (`:40711-40871`).
- `dir` = the Bat's forward, or toward a foe that is selected (`IsFoe`) and within 18 m flat. With the foe, `go =
  clamp(|flat d| + 2.5, 4, 18)`; otherwise `go` = 18.
- Cooldown `agiAdjust(120)` (`addTimeOut`).
- `SwarmLanding(dir, go)@0x1AD2500` moves the Bat's controller to find the landing; walls stop it.
- `StartCoroutine(RPC_nightfallSwarm(heroPos, offset = landing − heroPos))`, and the same RPC goes to the others.

The coroutine: `TTO1102:Bat.<RPC_nightfallSwarm>d__336::MoveNext@0x1B0EFC0` (`Bat.c:18584-19497`). Its strings
(`:18699-18708`): drainLife, nightfallSwarm_reform, nightfallSwarm_screech, nightfallSwarm_hit, nightfallSwarm,
nightfallSwarm_flap, bloodCarnage_ring, nightfallSwarm_bat, nightfallSwarm_wrap, nightfallSwarm_burst.

### 2.1 Timeline

**0.00, state 0** (`:18712-18874`):
- `dir` = vFlat(offset) normalised, or the forward when it is about zero.
- `Row6Begin("nightfallSwarm", mPos, dir)` (`:18769`). The step counter `mRow6Step` (+0x628) goes up; a later Row6 skill
  ends this one.
- `end = mPos + offset` (`:18772-18776`).
- `road = SwarmPath(mPos, dir, |offset| + 0.01)` (`:18792`; `@0x1AD2D30`):
  - a ground point every 0.5 m (raycast down 6 m, `:44325`, `:44380`);
  - it ends early at a wall (a 1.2 m head-height linecast), at a step up of more than 1.2 m, or at a drop of more
    than 6 m (8.2 m ray).

  Then `end` is added as the road's last point when it is more than 0.5 m flat from it; otherwise it replaces the last
  point (`:18802-18842`). `roadLen = RoadLengths(road)` (`:18849`). `RoadAt(road, len, f)` = the point at fraction f
  of the road's arc length (`@0x1ACE080`).
- **`nightfallSwarm_wrap`, owned**, at the hero's position with its rotation (`:18853-18863`).
- **`Row6Sound("bloodCarnage_ring")`** (`:18864`).
- `Until(start + 0.4)` (`:18865`).

**0.40, state 1, still the current step** (`:18877-19033`):
- **`nightfallSwarm_burst`, not owned**, at `Row6Chest(Bat)` (0.9 m up) with the hero's rotation (`:18882-18895`).
- **`Row6Sound("nightfallSwarm_screech")`** and **`Row6Sound("nightfallSwarm_flap")`** (`:18896-18897`).
- **`HideBody()`** (`:18898`).
- `side` = Cross(up, dir) normalised = the hero's **right** (`:18914-18936`).
- **28 bats** (the loop `< 0x1c`, `:18943-19013`). For each bat i:
  - `lane[i] = side × Random.Range(−1.1, 1.1) + up × Random.Range(0.3, 2.1) + dir × Random.Range(−0.6, 0.6)`
    (capstone 0x1B0F52B-0x1B0F607: the pairs −1.1 / 1.1, 0.3 / 2.1, −0.6 / 0.6);
  - `phase[i] = Random.Range(0, 6.28)` (0x1B0F672);
  - **`nightfallSwarm_bat`, not owned**, at `Row6Chest(Bat) + insideUnitSphere × 0.3`, `LookRotation(dir)`
    (`:18978-19001`), kept in `bats`.
- `hitIds` and `fed` = 0. `dmgBase = max(1, talAdjust(200))`, on the caster's client only (`:19014-19029`).
- `t0 = now`, **`flight = 0x3effffff` = 0.49999997 s** (`:19030-19032`). The code then falls straight into the per-frame
  block in the same frame.

**0.40-0.90, state 2 every frame** (`:19036-19337`):
- `p = clamp01((now − t0) / flight)`, `S = (3 − 2p) p²` (smoothstep, `:19040-19057`).
- The Bat's transform moves to `RoadAt(S)` (`:19067-19075`). It is hidden, but owned effects with followPosition follow
  it.
- **Each bat i** (`:19237-19333`):
  - `u = clamp01(S − ((i % 7) × 0.12 / 7) × (1 − p))` (`:19249-19256`). Bats with i % 7 = 6 trail by up to 0.103 of
    the road at the start, none at the end.
  - Position = `RoadAt(u) + up × 0.9 + sin(π p) × (lane[i] + side × 0.3 cos(7 T + phase[i]) + up × 0.35 sin(9 T +
    phase[i]))`, with T = `Time.time` (`:19246`, `:19273-19328`; 0.35 `:19287`, 0.3 the reused `DAT_1830043a4`,
    0.9 `:19313`, 7 `DAT_183004750`, 9 `DAT_182f39ba4`).
  - The sine and cosine: `FUN_180308bd0` is sinf. Its small-argument path returns x − x³ / 6 (0x3088D0-0x3088E8,
    constant 0x3FC5555555555555). `FUN_180308640` is cosf. The envelope sin(π p) is 0 at both ends, so every bat
    starts on the road 0.9 m up and lands there.
  - Facing: `LookRotation(newPos − oldPos, up)` when the step² is more than 1e-6 (`:19340-19377`; capstone 0x1B0FD67).
  - Height in mid-flight: 0.85 to 3.35 m.
- **The hits** (`:19082-19221`), on the caster's client:
  - every foe in `FoesAround(RoadAt(S), 3.25)` not yet in `hitIds`;
  - `a = dot(vFlat(foe − mPos), dir)`, which must satisfy `−0.5 ≤ a ≤ dot(vFlat(RoadAt(S) − mPos), dir) + 0.8`;
  - and `|dot(…, side)| − 0.5 × collider extent.x ≤ 1.25` (`:19151`).
  - Then: `hit(454, foe, max(1, (int)(dmgBase × (1 + min(0.05 n, 0.5)))), KO 15, magic)` (`:19188`), and
    **`nightfallSwarm_hit`, not owned**, at `Row6Chest(foe)` with `LookRotation(dir)` (`:19192-19214`). If the foe
    lives, `Afflict(foe)` (`:19217`); `fed++`.
  - **For the 10 m target** (`calc.txt`): `12.5 S + 0.8 ≥ 10` gives S ≥ 0.736, p = 0.66312, **t = 0.7316 s**. The
    first 30 or 60 fps frame is 0.733. The swarm point is then 9.2 m ahead, within the 3.25 m radius. Cue: 0.732,
    10 m ahead, 0.6 m up, no extra rotation (dir is the hero's facing, not the target's rotation).
- While p < 1: `yield null` (`:19226-19232`).

**0.90, the frame p reaches 1** (`:19400-19466`). That frame first puts every bat at `end + 0.9 up`, since u = 1 and
sin π ≈ 0, and runs the hits once more. Then:
- the Bat is set to `end` (also its sync fields, `:19405-19416`);
- **`StartCoroutine(Regather(bats))`** (`:19418`);
- **`ShowBody()`** (`:19420`);
- **`nightfallSwarm_reform`, not owned**, at `end` with the Bat's rotation (`:19421-19433`);
- **`Row6Sound("drainLife")`** (`:19434`);
- the heal when `fed > 0`: `RPC_AddHeal(4541, max(1, FloorToInt(min(fed, 5) × 0.03 × mhp)))` (`:19435-19458`).
  `CharacterControl::RPC_AddHeal@0x24BD3D0` loads no prefab (no string literal in its body, `CharacterControl.c:10743`),
  so the heal has no look on the page;
- `Until(start + 1.4)` (`:19460`; 1.4 from capstone 0x1B1069D).

**`Regather`** (`TTO1102:Bat.<Regather>d__337::MoveNext@0x1B25130`, `Bat.c:25281-25507`):
- `from[i]` = each bat's position at the landing.
- Every frame, `k = (now − t0) × 4`:
  - position = `lerp(from[i], Row6Chest(Bat), clamp01(k²))`, the chest read **every frame** (`:25421`);
  - the bat root's localScale = `one × (1 − 0.8 × clamp01(k))` (`:25484-25496`).
- At `t0 + 0.25` (`:25391`) every bat is destroyed (`:25406`): at **1.15 s, 0.75 s after its spawn**.

**1.40, state 3:** `Row6End("nightfallSwarm")` (`:19490`) puts the action at standby. That ends the wrap's
followState, which is already over by then.

**Abort** (the step changed in states 1-2, a newer Row6 skill): every bat destroyed and `ShowBody` (`:19467-19484`). It
does not happen on the page.

### 2.2 The statuses and the passives
- `Afflict@0x1AC1E20` / `AfflictOne@0x1AC1D40` (`:43916-43994`): two different statuses out of six (statuses 0x4b2,
  0x4b4, 0x4b5, 0x4b7, 0x4ba, 0x4bb) through `RPC_AddStatus` on the foe. No prefab, no sound.
- Their looks are the BB status looks on the foe's body: left out, by Sheep decision 4 (a look on a foe's body does not
  float over the empty target point).
- `Chiroptophobia@0x1AC21B0` is not called from this coroutine. Nothing rolls.

## 3. What is left out, and why

- The six statuses' looks on the foe (2.2; Sheep decision 4).
- The heal's number (no prefab).
- The game's hit test against other foes: the page has one target (the 10 m point).
- In place (question 1):
  - the Bat does not travel;
  - the wrap's followPosition does not carry it along the road. In the game it rides the hidden Bat out to about
    11.2 m by its end at 0.8 s;
  - the reform and drainLife are at the hero, not 12.5 m ahead.

## 4. Sounds and voices

| t | Sound | Folder | Source | In BB's rip |
|---|---|---|---|---|
| 0 | bloodCarnage_ring | sounds/ | Row6Sound `:18864` | yes (1.158 s) |
| 0.4 | nightfallSwarm_screech | sounds/ | Row6Sound `:18896` | no: TTO's own (0.563 s, 22050 Hz mono) |
| 0.4 | nightfallSwarm_flap | sounds/ | Row6Sound `:18897` | no: TTO's own (0.714 s) |
| 0.9 | drainLife | sounds/ | Row6Sound `:19434` | yes (2.017 s) |

None of the five prefabs has an AudioSource (`compact.txt`). There are no voices.

TTO's `bat/sounds/` holds 41 names, BB's rip 72. The TTO-only ones are crimsonVerdict_blast, evilTwin_pull,
evilTwin_return, nightfallSwarm_flap and nightfallSwarm_screech (`sounds.txt`).

## 5. Probed 2026-11-13 (home PC, TTO's 2026-11-04 bundles)

| Prefab | EffectControl (life + after) | Nodes / parts | Spawned |
|---|---|---|---|
| nightfallSwarm_wrap | 0.5 + 0.3, **followPosition, followState** | Mist (PS sphere r 0.8, 40/s for 0.35 s, 1.0 m up; Velocity), Eyes (PS burst 10, 1.2 m up) | 0, owned, at the hero |
| nightfallSwarm_burst | 1.2 + 0.4 | Smoke (PS burst 12), Bats (PS burst 22, `tto_batRow6_batSil` silhouettes, 6 m/s), Flash + Ring (ImageEmitter, mode 0) | 0.4 at the chest |
| nightfallSwarm_bat | 3.0 + 0.1 (code destroys at 0.75) | root **BatSwarmFlap** (wingL = node 4 "WingR", wingR = node 3 "WingL", 9 beats/s, amplitude 55, lift 10); Model (rot −90° about x, scale 2.2) > Body (238 v) / WingL / WingR (72 v each, **no UVs**) as **StaticMesh** with `tto_batRow6_batSolid` = **FlexibleCelShader/Cel No Outline**; Trail (**TrailRendererModern**, time 0.09, width 0.035 → 0.01, red → purple, min vertex 0.04) | 0.4, x 28 |
| nightfallSwarm_hit | 0.7 + 0.3 | Bite (ImageEmitter, rot 35), Flash (ImageEmitter), Bats (PS burst 6), Blood (PS burst 12, gravity 1.2) | at the foe's chest |
| nightfallSwarm_reform | 1.0 + 0.4 | Mist (PS burst 16, 1.0 up), Ring (**GroundHugEmitter** shape 0 Disc, r 2.2 → 0.4, 0.5 s, no motes), Flash (ImageEmitter, delay 0.25, 1.0 up), Eyes (PS burst 12, 1.1 up) | 0.9 at the end |

- **Shuriken:** shapes all 0 (sphere); modules Initial, Shape, Emission, Size, Color, Velocity; render mode 0
  (billboard); no Trail, Noise, Sub or Collision module (none of shuriken.js's skipped ones).
- **Materials (7):**
  - `tto_batRow6_wisp` (alpha);
  - `tto_Line_SimpleBall` (addsoft);
  - `tto_batRow6_batSil` (alpha, texture tto_batRow6_bat);
  - `tto_batRow6_ring` (addsoft);
  - `tto_batRow6_batSolid` (the cel shader): `_Color` (0.19, 0.075, 0.17), `_RampLevels` 3, `_HighIntensity` 2.4,
    `_LowIntensity` 1.55, `_LightScalar` 1, `_SceneLighting` 1, `_FresnelBrightness` 0, `_RimAlpha` 0, texture
    `tto_row6_brushwork`. `_EmissionColor` is a leftover Standard prop that is not in the cel shader's `$Globals`
    (tto_penguin.js's list);
  - `tto_Line_DoubleEdge1` (addsoft);
  - `tto_batRow6_slash` (add).
- **Textures (7):** tto_Line_DoubleEdge1 and tto_Line_SimpleBall (shared with the Sheep and the Penguin),
  tto_batRow6_bat, tto_batRow6_ring, tto_batRow6_slash, tto_batRow6_wisp, tto_row6_brushwork.
- **BatSwarmFlap** (`TTO1102:BatSwarmFlap`, dump.cs:98919; not in pseudo/, read with capstone, `flap.asm`):
  - **Awake@0x1B1AEB0**: `restL` / `restR` = the wings' localRotation; `phase = Random.Range(0, 6.28319)`;
    `beatsPerSecond ×= Random.Range(0.85, 1.15)`.
  - **Update@0x1B1AFC0**: `a = sin(Time.time × beatsPerSecond × 2π + phase) × amplitude + lift`;
    `wingL.localRotation = restL × AngleAxis(a, Vector3.up)`; `wingR.localRotation = restR × AngleAxis(−a, up)`.
    The product order is rest × q: the computed x is `qx rw + qw rx + qz ry − qy rz`.
- **Code vs bundles:** the code is 1102 and the bundles are 1104; every prefab name the code loads is in the catalog.
  The installed client is newer (GameAssembly.dll of 2026-11-07, 63,790,592 bytes), but there is no 1107 `methods.tsv`
  at home, so the Penguin's `cmp1109.py` check (same float constants and calls) was not run (question 5).

## 6. Parts the page lacks (effect: part)

| # | Part | Effect | What it does (source) |
|---|---|---|---|
| P1 | `Bat.NightfallSwarm` code mover (CODE_MOVERS) | nightfallSwarm_bat | Section 2.1 state 2 + Regather. (a) Hold `api.heroHide(key, true)` from the spawn until the landing (HideBody → ShowBody); VFX off ignores it. (b) Fly the road from the hero's feet to `to` ([0, 0, 12.5], flat) over `flight` = 0.49999997 s, as in 2.1, with the lag (i % 7) from the cue's `i`, the random lane and phase drawn at spawn, and the facing along the motion. (c) From the landing, `Regather`: lerp to the hero's chest, read live (`Row6Chest`: the hero's position + 0.9 up), by clamp01((4τ)²), root scale 1 − 0.8·clamp01(4τ); "destroy" at τ ≥ 0.25 (the cue's `kill` 0.75 says the same). Space: the effect's Unity world, the hero's feet at the origin facing +z (as `tto_penguin.js`'s movers); the page's clock stands in for `Time.time`. (`Bat.c:19036-19337`, `:25281-25507`) |
| P2 | `BatSwarmFlap` script part | nightfallSwarm_bat (root comp) | Awake / Update as in section 5. The wing nodes are referenced `{"node": 4/3, "type": "Transform"}`. The local rotation is applied to each wing node's rest quaternion in Unity's numbers (the mirror group handles handedness). |
| P3 | Build registrations in `pipeline/wardrobe_fx_tto.py` | all five | `SKILL_FX["bat"]` = the five prefabs; `CODE_MOVERS["nightfallSwarm_bat"] = "Bat.NightfallSwarm"`; optionally `SKILL_SOUNDS["bat"] = ["nightfallSwarm_screech", "nightfallSwarm_flap"]` (the cue file alone already makes the build fetch them). |

Parts that already exist and are used here:
- EffectControl;
- Shuriken (`shuriken.js`: sphere shape, Size / Color / Velocity);
- ImageEmitter;
- GroundHugEmitter (`groundhug.js`, Disc);
- StaticMesh (`mesh.js`);
- the cel shader (`tto_penguin.js`, registered page-wide through `api.shader`; `mesh.js`'s `material()` hands it out
  through fxMaterial). Its formula handles `_RampLevels` 3: levels = 2, so three bands at 0, 0.5 and 1;
- TrailRendererModern (`tto_sheep.js`);
- hero hiding (`api.heroHide`, index.html `lookSync`);
- TTO-only hero sounds (`wardrobe_fx_tto.py` `tto_clips`, P8).

The wing meshes have no UVs: `mesh.js` fills zeros, so the texture is sampled at (0, 0). Unity does the same with no UV
channel.

Build notes for the parts stage (home, or the office with its own bundles):
1. Add P3.
2. Write P1 and P2 (a new `wardrobe/fxparts/tto_bat.js`, added to `FX_PART_FILES`; that is a shared `index.html` edit).
3. Paste section 7.
4. Run `wardrobe_fx_tto.py bat` (the five prefabs, 7 materials, 7 textures, the 2 TTO sounds) and `wardrobe_fx.py bat`
   (the BB `sounds/` bloodCarnage_ring and drainLife).

## 7. The cue entry (paste-ready for `wardrobe/fx_cues/bat.json`; variant A, in place)

Checked: `cues_block.txt` parses inside `{ }` (`cues.py`). `bat.json` is `{}` today. 28 bat cues (i 0-27); `to` is the
road's end; the hit is at the 10 m target point.

```json
  "nightfallSwarm": {
    "why": "TTO1102:Bat.<RPC_nightfallSwarm>d__336::MoveNext@0x1B0EFC0 (pseudo/Bat.c:18584-19497; plans/fx_bat/tto.md 2; the 10 m target: length clamp(10 + 2.5, 4, 18) = 12.5 m, Bat::DoRow6Skill@0x1AC2660 :40724-40807; in place, no hero mover, Penguin decision 8): 0: Row6Begin (:18769), nightfallSwarm_wrap owned at the hero (:18863; followPosition + followState: cut at Row6End 1.4), Row6Sound bloodCarnage_ring (sounds/, :18864), Until(start + 0.4) (:18865); 0.4: nightfallSwarm_burst at Row6Chest@0x1ACEE60 = the collider centre, 0.9 m up (Bat CharacterController m_Center y 0.9, TTO's bundle and BB's Bat.prefab:911), the hero's rotation (:18882-18895), Row6Sound nightfallSwarm_screech + nightfallSwarm_flap (TTO's own sounds/ clips, :18896-18897), HideBody@0x1AC44A0 (:18898), 28 x nightfallSwarm_bat (:18940-19013, 0x1c) flown by the coroutine: the road from the hero to the landing in 0x3effffff = 0.5 s smoothstep (:19032-19067), bat i (i % 7) x 0.12 / 7 x (1 - p) behind, 0.9 m up + sin(pi p) x (its lane: right U(-1.1, 1.1) + up U(0.3, 2.1) + fwd U(-0.6, 0.6), capstone 0x1B0F52B-0x1B0F607; + right 0.3 cos(7 T + phase) + up 0.35 sin(9 T + phase), phase U(0, 6.28) 0x1B0F672; :19240-19330), facing its motion (:19375), its wings flapped by its own BatSwarmFlap (Awake@0x1B1AEB0 / Update@0x1B1AFC0); the 10 m target is passed when 12.5 S(p) + 0.8 >= 10 (the lane test :19085-19151): 0.732 s, nightfallSwarm_hit at its chest (0.6 m up, the target rule), LookRotation(dir) = the hero's facing (:19192-19214); 0.9 (p = 1): ShowBody (:19420), Regather@0x1B25130 (:19418; every bat to the Bat's chest, read live, lerp clamp01((4 t)^2), root scale 1 - 0.8 clamp01(4 t), Destroy at 0.25 s: kill 0.75, Bat.c:25391-25496), nightfallSwarm_reform at the Bat with its rotation (:19433), Row6Sound drainLife (sounds/, :19434), the heal (RPC_AddHeal 4541, no look :19451); Until(start + 1.4) (capstone 0x1B1069D), Row6End (:19490); no voice, no roll, one rank; left out: the six statuses' looks on the foe (Afflict@0x1AC1E20, Sheep decision 4)",
    "cues": [
    [0, "fx", "tto/nightfallSwarm_wrap", {"cut": 1.4}],
    [0, "sound", "bloodCarnage_ring"],
    [0.4, "fx", "tto/nightfallSwarm_burst", {"y": 0.9}],
    [0.4, "sound", "nightfallSwarm_screech"],
    [0.4, "sound", "nightfallSwarm_flap"],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 0, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 1, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 2, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 3, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 4, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 5, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 6, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 7, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 8, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 9, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 10, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 11, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 12, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 13, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 14, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 15, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 16, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 17, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 18, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 19, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 20, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 21, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 22, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 23, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 24, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 25, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 26, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.4, "fx", "tto/nightfallSwarm_bat", {"y": 0.9, "i": 27, "to": [0, 0, 12.5], "kill": 0.75}],
    [0.732, "fx", "tto/nightfallSwarm_hit", {"d": 10, "y": 0.6}],
    [0.9, "fx", "tto/nightfallSwarm_reform"],
    [0.9, "sound", "drainLife"]
    ]
  }
```

Notes on the entry:
- The cue options `i` and `to` are passed on to the parts by `cueOf` (index.html:4313: "every other option is passed on
  as it is, for the parts"). `i` is a new key for this mover, as it was for the Penguin's.
- The bats' `y` 0.9 is the spawn spot (the chest). The mover places them on the road 0.9 m up in the same frame, so the
  ±0.3 m sphere jitter of the spawn never draws.
- The 28 bats are the same prefab, one cue each, with the index in `i` (the Penguin's flock shape). They cannot be a
  single cue: each bat is its own prefab instance with its own lane, phase and flap.
- Before P1 and P2 are built, the entry already plays its sounds and the wrap, burst, hit and reform. The bats then
  stand frozen at the chest until their kill.

**Variant B (hero mover, question 1):** the same cues with the reform at `{"d": 12.5}`, plus a page hero mover that
translates the hero to `RoadAt(S(p))` from 0.4 to 0.9 s (hidden), leaves it at 12.5 m until 1.4 s, and puts it back
at the play's end. The bats' Regather then needs no change (it reads the chest live), and the wrap's followPosition
would follow the moved hero.

## 8. For the Bible (offer to the user; that repo's own rules)

These are new against `bat-skill-reference.md:706-718`, which already has 0.4 / 0.5 s smoothstep / 0.9 / 1.4:
- The flight is `0x3effffff` = 0.49999997 s, not exactly 0.5.
- The swarm is 28 bats. Each has:
  - a random lane: right ±1.1, up 0.3-2.1, along ±0.6, times sin(π p);
  - a wobble: right 0.3 cos 7T, up 0.35 sin 9T;
  - a lag of (i % 7) × 0.12 / 7 of the road, fading out by the landing;
  - a flight 0.9 m over the ground path.

  They converge into the Bat over 0.25 s, shrinking to 0.2 (`Regather`). Their wings beat at 9 ± 15 % per second,
  ±55° around 10° (`BatSwarmFlap`).
- When a foe at flat distance D is hit: when `L × S(p) + 0.8 ≥ D`, so at 0.4 + 0.5 × S⁻¹((D − 0.8) / L) s. Against the
  selected target, L = D + 2.5, so a target 10 m away is hit at 0.73 s.
- HideBody leaves the Bat's particle, trail and line renderers and its effects visible. So a weapon's own TTO particle
  effects keep drawing while the Bat is a swarm.
- The sounds: bloodCarnage_ring at 0, nightfallSwarm_screech + nightfallSwarm_flap (TTO-only) at 0.4, drainLife at
  0.9. The heal has no effect prefab.

## Open questions (each with my recommended answer)

1. **In place or a hero mover?** The game moves the hidden Bat 12.5 m. It reappears at the end, where the bats
   converge and the reform plays.
   - **Recommended: A, in place** (section 7). This keeps the convention of Penguin decision 8 and the Wolf's Feral
     Strike, and the clip has no root motion. The bats still fly the 12.5 m road through the 10 m target. At 0.9 s the
     Bat shows again where it stood, with the reform, and `Regather` pulls the bats back into its chest over 0.25 s.
     That is exactly the game's code run with the hero standing still: Regather reads `Row6Chest(mChar)` every frame.
   - B is the faithful one: a page hero mover (a teleport while hidden, so no fake motion is needed), the reform
     12.5 m ahead, the bats converging there. It costs the camera framing: the Bat would stand 12.5 m off for 0.5 s,
     then jump back when the play ends or loops.
2. **The swarm's length: 12.5 m (the target rule) or 18 m (no target)?** **Recommended: 12.5 m.** The standing rule
   puts a target 10 m ahead, and `DoRow6Skill` then aims at it with distance + 2.5. With 18 m the hit would come at
   0.4 + 0.5 × S⁻¹(9.2 / 18) = 0.656 s and `to` would be [0, 0, 18].
3. **Who owns the hero hide?** **Recommended: the bats' mover (P1).** Each bat holds a heroHide key from its spawn
   until the landing; the hide's times are the coroutine's own (HideBody at 0.4 with the bats, ShowBody at the
   landing). The alternative is a mover on `nightfallSwarm_burst` holding it for 0.5 s.
4. **A worn weapon's own effects while the Bat is hidden?** HideBody keeps ParticleSystemRenderers and Trail / Line
   renderers on, so in TTO a weapon's particle effects keep drawing at the hidden hand. **Recommended: leave the
   page's weapon effects (WFX) as they are.** They are not under the hero's meshes that heroHide hides, which is the
   game's own rule.
5. **The installed TTO client (2026-11-07) is newer than the decompile (1102).** **Recommended: accept 1102 for now.**
   The 1104 bundles have every prefab the code names, and the Penguin's 1102-vs-1109 check found its row-6 code
   unchanged. If wanted, the office (with a 1109 `methods.tsv`) can run `plans/fx_penguin/probes/research/tto/cmp1109.py`
   with the Bat's names: `<RPC_nightfallSwarm>d__336`, `<Regather>d__337`, `BatSwarmFlap::Awake/Update`,
   `Bat::DoRow6Skill`, `Bat::Row6Chest`.
6. **The six statuses' looks on the foe** (Afflict: two of Phantom Bane, Corruption, Curse, Amplify Damage, Blind,
   Confuse). **Recommended: left out** (Sheep decision 4: a status look on a foe's body does not float over the empty
   target point), as for the Penguin's frost marks.

## Verification

Checker, 2026-11-13 (home PC), read only, against `D:\12tails\DecompiledSource_TTO_2026-11-02\pseudo\Bat.c`, the
capstone listings this report made (`checks/fx_bat_research/tto/movenext.asm`, `flap.asm`), `dump.cs`, its probes
(`probe.json`, `cc.txt`, `sounds.txt`, `calc.txt`), BB's `Bat.prefab`, the Bible's reference / card, and the page
(`wardrobe/index.html`, `pipeline/wardrobe_fx_tto.py`). Re-read for every claim below; no probe re-run was needed.

**Confirmed (no change):**
- The timeline: wrap (owned, `Row6Spawn(..., 1)` `Bat.c:18863`), `Row6Sound bloodCarnage_ring` (:18864),
  `Until(start + 0.4)` (:18865); at 0.4 burst at `Row6Chest(Bat)` with the hero's rotation (:18882-18895), screech + flap
  (:18896-18897), `HideBody` (:18898), 28 bats (`< 0x1c`, :19013); at 0.9 `Regather` (:19418), `ShowBody` (:19420),
  reform at `end` with the Bat's rotation (:19433), `Row6Sound drainLife` (:19434), heal 0x11bd = 4541 with
  `min(fed, 5) x 0.03 x mhp` (:19440-19451); `Until(start + 1.4)` (capstone 0x1B1069D `addss xmm6, [0x3004950] = 1.4`);
  `Row6End` (:19490).
- `side` = Cross(up, dir) = the hero's right (:18914-18936, Vector3 statics +0x18 = up); the lane's three ranges and
  their order: side U(-1.1, 1.1), up U(0.3, 2.1), dir U(-0.6, 0.6), phase U(0, 6.28) (movenext.asm 0x1B0F52B-0x1B0F672).
- Per frame: smoothstep on `(now - t0) / 0x3effffff` (:19047-19057); the lag `(i % 7) x 0.12 / 7 x (1 - p)` (:19249-19256,
  the divisor is the reused 7); position `RoadAt(u) + 0.9 up + sin(pi p) x (lane + side x 0.3 cos(7 T + phase) + up x 0.35
  sin(9 T + phase))` (:19246-19313); the hit test `FoesAround(RoadAt(S), 3.25)`, `-0.5 <= a <= along(RoadAt(S)) + 0.8`,
  `|side dot| - 0.5 x bounds.extents.x <= 1.25` (bounds +0xc = extents), hit id 0x1c6 = 454, KO 0xf = 15,
  `nightfallSwarm_hit` at `Row6Chest(foe)` with `LookRotation(dir)` (:19082-19214); all on the caster's client (+0x182).
- The landing runs in the same frame as the last flight frame (the `1 <= p` test after the hits, `goto LAB_181b104b7`).
- `Regather`: `k = (now - t0) x 4`, position `lerp(from, Row6Chest(Bat), clamp01(k^2))` with the chest read each frame,
  localScale `1 - 0.8 clamp01(k)`, Destroy at `t0 + 0.25 <= now` (`Bat.c:25391-25496`): kill 0.75 after the 0.4 spawn.
- `DoRow6Skill`: 18 m, 324, 2.5, clamp to [4, 18], also `> 0.01` (a foe on top of the Bat is ignored), cooldown
  `agiAdjust(120)` (`Bat.c:40711-40807`). `Row6Sound` = `GameAssets/characters/heroes/bat/sounds/<name>`, volume 1 for
  the owner, 0.75 for the others (:45157-45190). `Row6Chest` = collider bounds centre (:45694-45750). `HideBody` skips
  ParticleSystemRenderer / TrailRenderer / LineRenderer and anything under an EffectControl (:44595-44672).
- The Bat's CharacterController centre 0.9 (TTO `Bat` in `cc.txt`; BB `Bat.prefab:911`), height 1.7, radius 0.3, scale 1.
- BatSwarmFlap: fields `dump.cs:98919-98936`; Awake U(0, 6.28319) and x U(0.85, 1.15); Update `sin(T x bps x 6.28319 +
  phase) x amplitude + lift` (flap.asm 0x1B1B000-0x1B1B04C: xmm9 = lift +0x38, xmm8 = amplitude +0x34), `rest x
  AngleAxis(a, up)` for wingL and `-a` for wingR (0x1B1B265 `xorps` sign flip), the product order rest x q as written.
  Probe: wingL -> node 4 "WingR", wingR -> node 3 "WingL", 9 / 55 / 10.
- The numbers in `calc.txt`: S = 0.736 -> p = 0.66312 -> t = 0.7316; the 60 fps frame before (0.7167) gives 9.49 m < 10,
  0.7333 gives 10.06 m; 1.15 / 1.4; lag 0.1029.
- Sounds: `bloodCarnage_ring` 1.158 s and `drainLife` 2.017 s in BB's `heroes/bat/sounds/`; `nightfallSwarm_screech`,
  `nightfallSwarm_flap` TTO-only; `wardrobe_fx_tto.py:600-606` fetches every `"sound"` cue the rip lacks (`cue_sounds`),
  so P3's `SKILL_SOUNDS` line is indeed optional. 5 prefabs, 7 materials, 7 textures as listed (`probe.json`).
- Released: `wardrobe/tto_released.json` bat clips = clap, nightfallSwarm, wai; `clips.json` nightfallSwarm 1.4 s.
- The cue block parses (36 cues, 28 bats with i 0-27); its formats match the page's (`cueOf`, `to` = [right, up, ahead],
  kind `"sound"`, `tto/` prefix) and the Penguin's flock entries.

**Corrections (wording and cites; nothing changes in the cue block):**
1. `index.html:4313` (Notes on the entry): the "every other option is passed on as it is, for the parts" line is
   `wardrobe/index.html:4321` today (the file moved; cite `cueOf`'s comment).
2. Read this first 6 ("the root track's x and z hold still, and only y bobs"): in `clips.json` the root's `p` keys are
   [t, x, y, z] in the rig's z-up frame: x holds at -0.04146, **z** is the height that bobs (0.749-1.029 m) and y drifts
   0.0035-0.0706 m (7 cm). The conclusion holds: no root motion, the clip plays in place.
3. 2.1 state 1 (a detail for P1, not a cue change): the bats are spawned at the chest plus the 0.3 m jitter and moved
   to `RoadAt(u) + 0.9 up` in the same frame, and that first move's step (jitter -> road) is what the facing test sees
   (`:19340-19377`), so for one frame each bat faces a random way; from the second frame it faces its motion. The page,
   spawning at the exact chest with no jitter, keeps `LookRotation(dir)` for that frame: invisible at 30-60 fps, left
   as is.
4. 2.2 / Read this first 4 "no roll": true for a proc chance; `AfflictOne` does draw the two statuses at random
   (`Random.Range(0, 6)` then `Random.Range(1, 6)`, `Bat.c:43916-43994`). Their looks are left out anyway (question 6).

Corrected paste-ready block: none needed; section 7's entry stands exactly as written.
