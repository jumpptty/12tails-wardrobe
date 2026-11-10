# Penguin effects + sounds research: the three TTO Lv 100 skills (Constellation, Frost Field, Emperors March)

Scope: the TTO clips `constellation` (1.0 s), `frostFieldLeap` (1.1 s), `emperorPenguin` (1.6 s), all `tto: true` in
`wardrobe/data/penguin/clips.json`. No BB code plays them. Research only: this file is the only file written, plus the probe
scripts in `checks/fx_penguin_research/tto/`. Sources:
- TTO's pseudo-C `C:\Users\Jump\Desktop\12tails\DecompiledSource_TTO_2026-11-02\pseudo\Penguin.c` and `CharacterControl.c`,
  cited as `TTO1102:Method@RVA` plus `Penguin.c:<line>`;
- capstone over `client\GameAssembly.dll` for the floats Ghidra drops (`dis.py`, `consts.py`);
- the call-site finder `callers.py` / `jumps.py`;
- the Bible's `12t_reference\penguin-skill-reference.md` "TTO Lv 100 skills" (lines 764-822);
- TTO's 2026-11-09 bundles on this PC (`tto_assets\2026-11-09`), read with `wardrobe_fx_tto.py penguin --probe`.
  Its output is `checks/fx_penguin_research/tto/probe.json`; `compact.txt` and `summary.txt` summarise it.

Times are seconds from the start of the clip the cue is keyed by. Every wait is `Penguin::Until(start + t)`
(`TTO1102:Penguin::Until@0x1DB15A0`, `Penguin.c:41709`). Its MoveNext is `Penguin.<Until>d__386::MoveNext@0x1B257C0`, the
same machine code as the Sheep's (`comiss [this+0x20], Time.time`, yield while t > now). So a wait is an **absolute time
from the coroutine start**, not a step to add. All three skills have one rank, so max rank changes nothing.

**Re-checked 2026-11-10 (the resumed `tto` agent, office PC).** The first draft (commit 38b1c19) stopped unverified at the
98 % limit; it was complete (sections 1-8). This pass re-traced every wait and spawn in `Penguin.c` (RPC_constellation
:6849-7022, StarLines :22538-22981, RPC_frostFieldLeap :11395-11534, FrostFieldLoop :1324-1432, RPC_emperorPenguin
:8645-9077, EmperorShot :292-852, AddFrostMarks :38229-38311, BurstFx :38592-38640), re-ran `calc.py` (same numbers),
checked every sound against the rip's folders and the clip lengths in `clips.json` (1.0 / 1.1 / 1.6). All held. Two
changes, both from the decisions, not new findings:
- **Frost Burst is now cued, at the target** (it was left out under question 6). The task's rule puts effects on the
  target at the target point, like Divinity Sword's strike (Sheep decision 2); `BurstFx@0x1DA3310` (`Penguin.c:38592-38640`)
  spawns `frostField_burst` at the foe's transform (its feet), identity, plus `Row6Sound("frozenBlast")` (`sounds/`).
  Emperors March: at 1.173 s, 10 m (section 2.3). Frost Field: at 4.8 s, 1.5 m (section 2.2). Question 6 is gone.
- **The status looks stay out by Sheep decision 4** ("its buff look does not float over the empty spot"): `frostMarkFx`,
  `frostBiteFx`, `manaFractureFx` ride the foe's body (`AddPenguinRow6Fx@0x24ADC20`), and `hit()` itself spawns no prefab
  (`CharacterControl::hit@0x24D57E0`, `CharacterControl.c:6555`: no effect string), so the hits draw nothing to leave out.

## Read this first

1. **This PC reads every Penguin TTO prefab.** There are 28 TTO-only prefabs; all of them are probed and listed in
   section 5. There is no arcana style: the catalog has no `heroes/penguin/arcana/`.
2. **TTO1102's code is TTO1109's.** The bundles are 1109 and the decompile is 1102. `cmp1109.py` compares 16 methods
   between the two GameAssembly.dll files: the three coroutines, StarLines, FrostFieldLoop, FlockRise, EmperorShot,
   FlockSpot, Row6Beak, Row6Foot, GoalFx, Scatter, StarImpact, Row6Begin, FieldLanding and DoRow6Skill.
   - Each has the same size and the same float constants in the same order.
   - The named call targets match too. `RPC_emperorPenguin` has one more unnamed call after `Row6End` (`calls1109.py`);
     it does not change what the method does.
3. **No voices, no Multi Cast.** None of the three coroutines plays a voice or rolls a proc.
   - Every sound goes through `Penguin::Row6Sound@0x1DB04B0` (`Penguin.c:41262`). It plays
     `GameAssets/characters/heroes/penguin/sounds/<name>` with `PlayOneShot` on the hero, volume 1 for the owner
     (0.75 for others). So every sound cue is kind **`"sound"`** (the `sounds/` folder).
   - Every Row6Sound name is in the rip's `sounds/` and none in `voices/` (checked 2026-11-10, file by file), except
     the two TTO-only ones (item 4).
   - The only `voices/` and `multiCast` loads in Penguin.c belong to BB skills (Arctic Wind, Blink, Falling Comets ...).
     So no 24 % roll applies here, by analogy with Sheep decision 6 (Grand Codex).
4. **Two TTO-only sounds.** `emperorPenguin_whistle` (0.620 s) and `emperorPenguin_flock` (1.052 s) are in TTO's catalog
   (`penguin/sounds/`, 44 names) but not in BB's rip (42 names). `wardrobe_fx.py` builds `"sound"` cues from BB's rip only
   (`rip_wav`, `cue_names`), so these two need TTO's own clip (part P8).
   - The other 13 sounds are BB's recordings, the same length to the millisecond (`sounds.py`).
5. **Name collisions:**
   - `emperorPenguin_whistle` is both an effect (`tto/emperorPenguin_whistle`) and a sound (`sounds/emperorPenguin_whistle`);
     both are used at 0 s. The cue kind keeps them apart.
   - These sounds share a name with a BB Penguin effect: `blink`, `iceBlock`, `blizzard`, `castEffect`, `fallingComet`,
     `manaArc`, `absoluteZero`, `fallingStar_ring`, `frozenBlast` (the Frost Burst's sound, now cued; BB also has a
     `frozenBlast` effect prefab, never spawned here). Every Row6 sound is a `sounds/` clip, never an effect.
   - `iceBlock` plays **twice** at 0.3 s: `Row6Sound("iceBlock")` and `emperorPenguin_crack`'s own AudioSource
     (`sounds/iceBlock`, vol 0.8). The game does this; keep both.
   - BB's `voices/` has `marchofthePenguin1/2` and `frostBite1/2`, but no TTO code plays them.
   - "Launch" means two things. The Bible's "launch at 0.85" (`penguin-skill-reference.md:807`) is the start of
     EmperorShot. The **effect** `emperorPenguin_launch` is spawned at **0.8**, with the kick.
   - The constellation prefab `constellation_impact` is also used by Emperors March, but only with +3 penguins (question 3).
6. **No prefab has `followState`**, so no `cut`s are needed. The code destroys these early (the cues' `kill`):
   - the marks (at their star's impact);
   - the lines (`ClearStarFx`);
   - the ball and the flock (at the Goal).

   `frostField_field`'s own life, 8 + 0.6 s, ends before the code's `Destroy(field, 9)`, so it needs no kill.
7. **Missing parts** (section 6): P1-P8.
   - Code movers for the constellation lines, the ball and the flock.
   - Shuriken's TrailModule (the meteor streaks).
   - A TTO SkinnedMeshRenderer export and the `FlexibleCelShader/Cel No Outline` shader (the penguins).
   - Unity's built-in Quad as a particle mesh.
   - A vector `scale` cue option.
   - The two TTO sounds.

   Per the rule, every effect below is cued anyway, with the part it needs named.
8. **Cue options the parts need.** `scale` as `[x, y, z]` is **not safe to paste yet**: `index.html:3149` does
   `multiplyScalar(at.scale || 1)`, and an array there gives NaN.
   - Only the variant B lineFire cues use it. Paste them after P5.
   - `i` (the penguin's index) and `ignite` (the lines' widening time) are new keys. Today's `cueOf` (`index.html:3467`)
     simply drops them, so they are harmless.
9. **Emperors March runs past its clip.** The Goal and the flock's poofs land at **1.636 s**, after the clip's 1.6 s.
   - The page keeps later cues in the idle tail, as for Grand Codex.
   - With the วนซ้ำ (loop) toggle on, the clip restarts at 1.6 s, so the Goal never shows.
10. **Frost trail: 13 frosts, not 14.** `frostAt` is a float32 that starts at 1.2 and adds 1.6 each step
    (`EmperorShot`, `Penguin.c:428`, `:552`).
    - After 13 frosts it is 22.0000019, which is more than the 22 m reach.
    - So the last frost is at 0.45 + 20.8 = 20.85 m. In real numbers it would be 14 (`calc.py`).
    - This is a new finding for the Bible: offer it to the user.
11. **SEQ:** nothing to fix in my scope.
    - The three skills have no cast bar (Bible :771; they never call `RPC_cast1`), so they stay single tiles.
    - Each clip's length equals its `Row6End` time: 1.0 = `Until(start + 1)`, `Penguin.c:7011`; 1.1 = `:11534`;
      1.6 = `:9077`.
12. **Game quirk (harmless here).** `RPC_constellation` state 1 calls `Row6End` only on the path where the star list is
    non-empty (`Penguin.c:6886-7016`). With no stars at 0.4 s, the Penguin stays in `attack`.
    - The caster's own client always has at least the target (`PickStars@0x1DA8960` adds it first, `Penguin.c:37227`).
    - Offer it for the Bible only if the user wants such corner cases.
13. **Surprises the page will show (APPROXIMATED, no part fixes them):**
    - Constellation's marks, stars, impacts and Giant Star spawn with **world identity**; the page turns every cue by the
      hero's facing (`cueOf` comment, `index.html:3446-3466`). The meteors (`Meteor1` at local (−3, 12, 2.5), `Giant1` at
      (−6, 22, 5): `summary.txt`) so come from a hero-relative side, not the map's fixed one. The Penguin faces the
      target, so it looks right.
    - Two of the five poofs at the Goal are at or below the ground (i 3: y −0.29): the flock's ring centre is ballAt's
      0.2 m + 0.15 m, with a 0.65 m radius (`Penguin.c:612-626`). The game does the same.
    - `frostField_trail` (2 TrailRendererModern, followPosition) rides a hero that doesn't travel on the page, so its
      ribbons stay short (only the clip's own airborne Root motion, 0.2-0.73 s, moves it).
14. **Focus Intellect turns Emperors March red.** `EmperorSpawn(..., red)@0x1DA44B0` (`Penguin.c:39744`) and `GoalFx`
    call `FocusRedden@0x1DA5630`, which swaps the materials for red copies.
    - `red` is set when the cast took Focus (`RPC_emperorPenguin` `<red> = coded.y > 0.5`, `Penguin.c:8594`; DoRow6Skill
      puts y = 1 when `TakeFocus() >= 1`).
    - The Bible doesn't mention it. Question 4.

---

## 1. Shared machinery (`TTO1102:Penguin`)

- **`Row6Begin(command, mPos, dir)@0x1DAF8B0`** (`Penguin.c:41406`):
  - sets actionState `attack` and puts the hero at mPos;
  - `LookAt(mPos + vFlat(dir))` when |vFlat(dir)|² > 0.0001;
  - `PlayAnimation(command, 0.1)`, wrapMode Once, moveSpeed 0.
- **`Row6End(command)@0x1DAFF70`** (`:41510`): sets `standby`, but only while the action is still this command.
- **`Row6Spawn(name, pos, rot, owned)@0x1DB06F0`** (`:39637`):
  - loads `GameAssets/characters/heroes/penguin/effects/<name>` and logs `Cannot find <name> effect`;
  - owned → `CharacterControl.createEffect`; otherwise a bare `Object.Instantiate`.
  - Owned prefabs: only `constellation_cast` and `frostField_trail`.
- **`EmperorSpawn(name, pos, rot, red)@0x1DA44B0`** (`:39744`) = `Row6Spawn(..., owned false)`, plus `FocusRedden` when
  `red`. Every Emperors March effect goes through it, except `constellation_impact`.
- **`Row6Beak()@0x1DAF620`** (`:41729`) = the `Head` bone + 0.16 × forward − 0.03 × up (with no Head bone: hero + 0.67 up).
  - On the page, Head at emperorPenguin 0.017 s is (0.011 fwd, 0.039 right, 0.673 up), from `bones.py`: rig x forward,
    −y right, z up. The sign was checked: `Foot2_R` / `mount_Hand_R` are −y; the result is about ±5 cm.
  - So the beak is **0.17 m ahead, 0.04 m right, 0.64 m up**.
- **`Row6Foot()@0x1DB0160`** (`:41814`) = the `Foot2_R` bone (with none: hero + 0.3 forward).
  - At emperorPenguin 0.8 s: (0.103, 0.189 right, 0.170 up), so **0.10 m ahead, 0.19 m right, 0.17 m up**.
- **Status looks: `CharacterControl::AddPenguinRow6Fx(status, lv)@0x24ADC20`** (`CharacterControl.c:25195`) loads
  `penguin/effects/<status>Fx`.
  - Its two call sites in `<addStatus>d__481::MoveNext` are 0x24FD582 and 0x24FD5A2 (`callers.py`).
  - The dispatch at 0x24EE951-0x24EE996 (`jumps.py`; string literals resolved from the rip-relative loads) reaches them
    only for **frostMark** and **frostBite** (the generic case) and **manaFracture** (its own case).
  - `frostField` and `frozenGround` have no look. So the Penguin's own `frostField` buff (Frost Field) draws nothing.
  - All three looks sit on foes.

## 2. Per skill

### 2.1 Constellation (`constellation`, 1.0 s; cell 452)

The cast is `DoRow6Skill@0x1DA35F0` (`Penguin.c:36576`):
- it needs a living foe within 16 m flat;
- `TakeFocus`, then `mStarFlockUntil = now + 8` (the Emperors March window, `:36656-36660`);
- `PickStars(target)@0x1DA8960` adds the target first, then up to 4 more foes from `FoesAround(target, 10)` sorted by flat
  distance (`:37227-37400`). Each star spot is `StarGround(foe position)`: a raycast down from 3 m above, 8 m long
  (`:38096`), which is the ground under the foe.

Coroutine `TTO1102:Penguin.<RPC_constellation>d__340::MoveNext@0x1DE7560` (`Penguin.c:6783-7032`):
- **0.00**:
  - `Row6Begin("constellation")`, facing the target (`:6849`);
  - `ClearStarFx`;
  - `Row6Sound("fallingStar_ring")` (`:6856`);
  - `constellation_cast` **owned** at the hero, hero rotation (`:6871`);
  - `Until(start + 0.4)` (`:6876`).
- **0.40** (state 1, still the current cast):
  - the stars are put in sky order (`InSkyOrder@0x1DA7F90`, `:6893`): ascending `atan2(dx, dz)` about the stars' mean
    (the comparison `<InSkyOrder>b__0@0x1DCE5F0`, `Penguin.c:48-100`);
  - per star: `constellation_mark`, world, at `StarAt(star) + up` (**1 m over the ground spot**), identity rotation
    (`:6902-6924`);
  - `Row6Sound("castEffect")` (`:6943`);
  - `StarLineCount(n)` (`:37411`): n ≥ 3 gives n lines (a closed ring), n = 2 gives 1, n = 1 gives 0. Per line:
    `constellation_line`, world, at `StarAt(star i)`, identity (`:6948-6995`). Its LineRenderers start disabled (probe:
    `m_Enabled` false);
  - `StarLines(step, stars, marks, lines, start)` starts (`:7004`);
  - `Until(start + 1.0)` (`:7011`).
- **1.00**: `Row6End` (`:7022`). The clip is 1.0 s ✓.

`StarLines` (`TTO1102:Penguin.<StarLines>d__341::MoveNext@0x1E2C220`, `Penguin.c:22423-23060`) runs every frame from 0.4:
- **Marks follow their foes** until each star falls (`:22580-22621`): position = `StarAt + up`.
- **Lines:**
  - line i runs from mark i to mark (i + 1) % n, both 1 m up;
  - its end point grows `f = clamp01((now − (start + 0.4 + 0.12 i)) / 0.12)` (`:22659`; 0.12 at `DAT_1830046e4`);
  - `SetPosition(0, from)`, `SetPosition(1, lerp(from, to, f))`, and `set_enabled(f > 0)` (`:22689-22703`; capstone
    0x1E2CA35 `comiss xmm6, xmm7; seta dl`).
- **Star i falls** at `start + 1.1 + 0.3 i` (`:22715`):
  - `constellation_star`, world, at the ground spot, identity (`:22736`);
  - **0.6 s later** the mark is destroyed and `StarImpact(spot)` runs (`:22759-22770`);
  - `StarImpact@0x1DB1000` (`:37493`) spawns `constellation_impact`, world, at the spot, identity; the prefab plays its
    own `fallingStar_hit`. Then come the hits.
- **lastImpact** = start + 1.1 + 0.6 + 0.3 (n − 1) (`:22537`).
- **Ignite**, at lastImpact + 0.05 (`:22790`):
  - middle = `StarGround(mean of the spots)` (`:22809`);
  - every LineRenderer's `widthMultiplier ×= 2.2` (`:22833-22834`; capstone 0x1E2CE9A `mulss xmm0, xmm12`, with
    xmm12 = 2.2 loaded at 0x1E2CE08);
  - per segment, `constellation_lineFire`, world, at the segment's midpoint (1 m up), `LookRotation(b − a)`, localScale
    (1, 1, |b − a|) (`:22884-22904`);
  - if there are lines: `constellation_ignite` at the middle, identity, then `Row6Sound("manaArc")` (`:22921-22923`).
- **No Giant Star (n < 3):** `Until(now + 0.6)` (`:22936`; the 0.6 from capstone 0x1E2D59A), then `ClearStarFx`
  (`:22556`), which destroys the marks and lines (`mStarFx`).
- **Giant Star (n ≥ 3):**
  - at the ignite: `constellation_giant` at the middle, identity, and `Row6Sound("fallingComet")` (`:22953-22954`);
  - at lastImpact + 0.05 + 0.6: `ClearStarFx`, then `constellation_giantImpact` at the middle and
    `Row6Sound("novarFlare")` (`:22966-22981`). Then come the hits.
- Sums checked against the Bible (:782): one star impacts at 1.1 + 0.6 = 1.7. With five, the impacts are at 1.7, 2.0,
  2.3, 2.6, 2.9, and the Giant at 2.9 + 0.05 + 0.6 = 3.55 ✓ (Bible: 3.55 for 5 stars).

**Variant A, one star (the lone target 10 m ahead, by the decisions).** The star is the skill's own summon at the foe,
like Divinity Sword (Sheep decision 2).
- With n = 1 there are 0 lines and no Giant Star. Ignite at 1.75 spawns nothing; ClearStarFx at 2.35 finds nothing left.
- The cue file gets the cast, the mark, the star and the impact.

```json
  "constellation": {
    "why": "TTO1102:Penguin.<RPC_constellation>d__340::MoveNext@0x1DE7560 (Penguin.c:6783-7032; plans/fx_penguin/tto.md 2.1, variant A: the lone target 10 m ahead, plans/fx_wolf/decisions.md): 0: Row6Begin facing it (:6849), Row6Sound fallingStar_ring (Penguin::Row6Sound@0x1DB04B0 = sounds/, vol 1, :6856), constellation_cast owned at the hero (:6871; EffectControl 1 + 0.5, followPosition); Until 0.4 (:6876): constellation_mark at StarAt + up = 1 m over the star's ground spot (StarGround@0x1DB0E70), identity (:6902-6924), Row6Sound castEffect (:6943); StarLineCount(1) = 0 lines (:37411); Until 1 (:7011): Row6End; StarLines@0x1E2C220 (:22423-23060): the star falls at start + 1.1 + 0.3 x 0 (:22715) = constellation_star at the spot (:22736), 0.6 s later the mark is destroyed (kill 1.3) and StarImpact@0x1DB1000 spawns constellation_impact at the spot (:22759-22770, :37493; its own sounds/fallingStar_hit 0.8); with one star no lineFire / ignite / Giant Star (n < 3); no voice, no Multi Cast roll; left out: the hits and the manaFracture look on the hit foe (CharacterControl::AddPenguinRow6Fx@0x24ADC20: on an enemy)",
    "cues": [
    [0, "sound", "fallingStar_ring"],
    [0, "fx", "tto/constellation_cast"],
    [0.4, "fx", "tto/constellation_mark", {"d": 10, "y": 1, "kill": 1.3}],
    [0.4, "sound", "castEffect"],
    [1.1, "fx", "tto/constellation_star", {"d": 10}],
    [1.7, "fx", "tto/constellation_impact", {"d": 10}]
    ]
  },
```

**Variant B, five stars: the target 10 m ahead and the 4 foes PickStars would add (question 1, my recommended default).**
- The layout is a regular pentagon: circumradius 3 m about a centre 13 m ahead, with the target vertex nearest the hero
  (10 m). The other four are within 10 m of the target, as `FoesAround(target, 10)` asks.
- Sky order, with the hero facing +z: the compass angles about the middle are −108, −36, 36, 108 and 180, so the target
  is star 4 at +180. (`atan2(+0, −3)` = +π; in the game the order depends on the map's north.)
- All numbers come from `calc.py`.

| star | x, d | falls | impact | mark kill |
|---|---|---|---|---|
| 0 | −2.853, 12.073 | 1.1 | 1.7 | 1.3 |
| 1 | −1.763, 15.427 | 1.4 | 2.0 | 1.6 |
| 2 | 1.763, 15.427 | 1.7 | 2.3 | 1.9 |
| 3 | 2.853, 12.073 | 2.0 | 2.6 | 2.2 |
| 4 (target) | 0, 10 | 2.3 | 2.9 | 2.5 |

- Lines: line i is cued at its draw start, 0.4 + 0.12 i. The game spawns all five at 0.4, hidden until f > 0, so the look
  is the same, and the part needs no delay. Each line is killed at the Giant impact, 3.55.
- lineFire: each segment is 3.527 m long, with yaw 18, 90, 162, −126, −54.
- The middle is 13 m ahead.

```json
  "constellation": {
    "why": "TTO1102:Penguin.<RPC_constellation>d__340::MoveNext@0x1DE7560 (Penguin.c:6783-7032) + <StarLines>d__341::MoveNext@0x1E2C220 (:22423-23060) (plans/fx_penguin/tto.md 2.1, variant B: the target 10 m ahead and 4 foes, a pentagon R 3 m about 13 m ahead, checks/fx_penguin_research/tto/calc.py): 0: Row6Begin, Row6Sound fallingStar_ring (:6856), constellation_cast owned (:6871); Until 0.4: a constellation_mark 1 m over each star spot (StarAt + up, :6902-6924; it follows its foe until the fall, :22580-22621), Row6Sound castEffect (:6943), 5 lines (StarLineCount@0x1DB1320: n >= 3 = a closed ring), line i from mark i to mark i+1 drawn over 0.12 s from 0.4 + 0.12 i (:22659-22703; cued at its draw start, the game's are hidden until then), widthMultiplier x 2.2 at the ignite (:22833-22834, capstone 0x1E2CE9A); Until 1: Row6End (:7022); star i (sky order, InSkyOrder@0x1DA7F90: ascending atan2(dx, dz), target last) falls at 1.1 + 0.3 i (:22715-22736) and lands 0.6 s later: its mark destroyed, constellation_impact at the spot (StarImpact@0x1DB1000, :22759-22770); ignite at lastImpact + 0.05 = 1.1 + 0.6 + 0.3 x 4 + 0.05 = 2.95 (:22537, :22790): constellation_lineFire at each segment's midpoint, LookRotation(segment), localScale (1, 1, 3.527) (:22884-22904), constellation_ignite at the middle (StarGround of the spots' mean, :22809) + Row6Sound manaArc (:22921-22923), constellation_giant at the middle + Row6Sound fallingComet (:22953-22954); 2.95 + 0.6 = 3.55: ClearStarFx (the lines go: kill), constellation_giantImpact at the middle + Row6Sound novarFlare (:22966-22981); left out: the hits and the manaFracture look on hit foes (AddPenguinRow6Fx@0x24ADC20: on an enemy)",
    "cues": [
    [0, "sound", "fallingStar_ring"],
    [0, "fx", "tto/constellation_cast"],
    [0.4, "fx", "tto/constellation_mark", {"x": -2.853, "y": 1, "d": 12.073, "kill": 1.3}],
    [0.4, "fx", "tto/constellation_mark", {"x": -1.763, "y": 1, "d": 15.427, "kill": 1.6}],
    [0.4, "fx", "tto/constellation_mark", {"x": 1.763, "y": 1, "d": 15.427, "kill": 1.9}],
    [0.4, "fx", "tto/constellation_mark", {"x": 2.853, "y": 1, "d": 12.073, "kill": 2.2}],
    [0.4, "fx", "tto/constellation_mark", {"y": 1, "d": 10, "kill": 2.5}],
    [0.4, "sound", "castEffect"],
    [0.4, "fx", "tto/constellation_line", {"x": -2.853, "y": 1, "d": 12.073, "to": [-1.763, 1, 15.427], "ignite": 2.55, "kill": 3.15}],
    [0.52, "fx", "tto/constellation_line", {"x": -1.763, "y": 1, "d": 15.427, "to": [1.763, 1, 15.427], "ignite": 2.43, "kill": 3.03}],
    [0.64, "fx", "tto/constellation_line", {"x": 1.763, "y": 1, "d": 15.427, "to": [2.853, 1, 12.073], "ignite": 2.31, "kill": 2.91}],
    [0.76, "fx", "tto/constellation_line", {"x": 2.853, "y": 1, "d": 12.073, "to": [0, 1, 10], "ignite": 2.19, "kill": 2.79}],
    [0.88, "fx", "tto/constellation_line", {"y": 1, "d": 10, "to": [-2.853, 1, 12.073], "ignite": 2.07, "kill": 2.67}],
    [1.1, "fx", "tto/constellation_star", {"x": -2.853, "d": 12.073}],
    [1.4, "fx", "tto/constellation_star", {"x": -1.763, "d": 15.427}],
    [1.7, "fx", "tto/constellation_impact", {"x": -2.853, "d": 12.073}],
    [1.7, "fx", "tto/constellation_star", {"x": 1.763, "d": 15.427}],
    [2.0, "fx", "tto/constellation_impact", {"x": -1.763, "d": 15.427}],
    [2.0, "fx", "tto/constellation_star", {"x": 2.853, "d": 12.073}],
    [2.3, "fx", "tto/constellation_impact", {"x": 1.763, "d": 15.427}],
    [2.3, "fx", "tto/constellation_star", {"d": 10}],
    [2.6, "fx", "tto/constellation_impact", {"x": 2.853, "d": 12.073}],
    [2.9, "fx", "tto/constellation_impact", {"d": 10}],
    [2.95, "fx", "tto/constellation_lineFire", {"x": -2.308, "y": 1, "d": 13.75, "rot": [0, 18, 0], "scale": [1, 1, 3.527]}],
    [2.95, "fx", "tto/constellation_lineFire", {"y": 1, "d": 15.427, "rot": [0, 90, 0], "scale": [1, 1, 3.527]}],
    [2.95, "fx", "tto/constellation_lineFire", {"x": 2.308, "y": 1, "d": 13.75, "rot": [0, 162, 0], "scale": [1, 1, 3.527]}],
    [2.95, "fx", "tto/constellation_lineFire", {"x": 1.427, "y": 1, "d": 11.036, "rot": [0, -126, 0], "scale": [1, 1, 3.527]}],
    [2.95, "fx", "tto/constellation_lineFire", {"x": -1.427, "y": 1, "d": 11.036, "rot": [0, -54, 0], "scale": [1, 1, 3.527]}],
    [2.95, "fx", "tto/constellation_ignite", {"d": 13}],
    [2.95, "sound", "manaArc"],
    [2.95, "fx", "tto/constellation_giant", {"d": 13}],
    [2.95, "sound", "fallingComet"],
    [3.55, "fx", "tto/constellation_giantImpact", {"d": 13}],
    [3.55, "sound", "novarFlare"]
    ]
  },
```

- `ignite` (new key) = seconds after the line's spawn when its width doubles ×2.2, i.e. 2.95 − spawn.
- `to` is the existing option: the line's end, the next mark.

### 2.2 Frost Field (`frostFieldLeap`, 1.1 s; cell 453)

The cast is `DoRow6Skill` (`Penguin.c:36950-37000`):
- `addTimeOut(agiAdjust(75))`;
- `FieldLanding(body, facing)@0x1DA4590` (`:38641`): the target's flat distance, capped at 14, minus 1.5 m. With no
  target it aims 9.5 m ahead (`DAT_1830057b4`), so 8 m. Then a wall check and the ground. **With the target 10 m ahead
  the landing is 8.5 m ahead;**
- `TakeFocus`.

Coroutine `TTO1102:Penguin.<RPC_frostFieldLeap>d__349::MoveNext@0x1DEF770` (`Penguin.c:11314-11556`):
- **0.00**:
  - `Row6Begin("frostFieldLeap", mPos, offset)` (`:11384`); land = mPos + offset;
  - `Row6Sound("blink")` (`:11395`);
  - `Until(start + 0.2)` (`:11400`).
- **0.20**:
  - `frostField_leap`, world, at mPos (the takeoff spot), hero rotation (`:11423`);
  - `frostField_trail` **owned** at the hero, hero rotation (`:11438`; EffectControl followPosition, so it rides the
    hero);
  - flight t0 = now, 0.6 s (`0x3F19999A`, `:11441`). Every frame the hero is at
    `lerp(mPos, land, u) + up × 10 u (1 − u)` (`:11478-11485`), which peaks at 2.5 m at u = 0.5.
- **0.80** (flight over):
  - the hero is at `land` (`:11500`);
  - `frostField_land`, world, at land, hero rotation (`:11523`);
  - `Row6Sound("iceBreak")` (`:11525`);
  - `FrostFieldLoop(land)` (`:11528`): `TTO1102:Penguin.<FrostFieldLoop>d__350::MoveNext@0x1DC38F0` (`Penguin.c:1268-1450`)
    spawns `frostField_field`, world, at the centre, identity (`:1324`), `Destroy(field, 9)` (`:1335`), and
    `Row6Sound("blizzard")` (`:1337`). Then 8 s of ticks: 1 s apart from the landing (`:1345`), `frostField` on the
    Penguin, `frozenGround` and a mark on each foe within 9 m;
  - `Until(start + 1.1)` (`:11534`).
- **1.10**: `Row6End` (`:11545`). The clip is 1.1 s ✓; the clip's own pose is airborne 0.2-0.73 s (its Root track).
- Sum: 0.2 + 0.6 = 0.8 ✓ (Bible :793: takeoff 0.2, landing and field 0.8, free at 1.1).

The wardrobe hero doesn't travel. By the Feral Strike convention (`plans/fx_wolf/misc.md` item 4: effects after a dash
go at 0, where the page's hero stands), the takeoff, the land and the field are all at the hero. Question 5 asks
whether the page should move the hero instead.

```json
  "frostFieldLeap": {
    "why": "TTO1102:Penguin.<RPC_frostFieldLeap>d__349::MoveNext@0x1DEF770 (Penguin.c:11314-11556; plans/fx_penguin/tto.md 2.2): 0: Row6Begin (:11384), Row6Sound blink (sounds/, :11395); Until 0.2: frostField_leap at the takeoff spot, hero rotation (:11423), frostField_trail owned at the hero (:11438; EffectControl 0.75 + 0.6, followPosition), the 0.6 s leap (:11441-11485: lerp to the landing + up x 10u(1-u), 2.5 m peak; FieldLanding@0x1DA4590: 1.5 m short of the target, 8.5 m for the target 10 m ahead) - the page's hero doesn't travel, so the landing is at 0 (Feral Strike's convention, plans/fx_wolf/misc.md item 4); 0.8: frostField_land at the landing, hero rotation (:11523), Row6Sound iceBreak (:11525), FrostFieldLoop@0x1DC38F0 (:1268-1450): frostField_field at the centre, identity (:1324; EffectControl 8 + 0.6 ends it before the code's Destroy 9, :1335), Row6Sound blizzard (:1337); ticks 1 s apart from the landing (:1345-1393), one Frost Mark each on the target 1.5 m past the landing (within 9 m, :1376; AddFrostMarks@0x1DA2E60 :1432): the 5th, at 0.8 + 4 = 4.8 s, sets off FrostBurst (:38311) = BurstFx@0x1DA3310 (:38592-38640): frostField_burst at the foe's feet, identity, + Row6Sound frozenBlast (sounds/), cued at the target 1.5 m ahead (the target point, moved with the landing to the hero); Until 1.1: Row6End (:11545); the cues after 1.1 s run on in the idle tail; no voice, no Multi Cast roll; left out: the frostMarkFx / frostBiteFx / frozenGround / 20 % freeze looks on the foe (status looks on its body, Sheep decision 4); the Penguin's own frostField buff has no look (AddPenguinRow6Fx@0x24ADC20 serves frostMark, frostBite, manaFracture only)",
    "cues": [
    [0, "sound", "blink"],
    [0.2, "fx", "tto/frostField_leap"],
    [0.2, "fx", "tto/frostField_trail"],
    [0.8, "fx", "tto/frostField_land"],
    [0.8, "sound", "iceBreak"],
    [0.8, "fx", "tto/frostField_field"],
    [0.8, "sound", "blizzard"],
    [4.8, "fx", "tto/frostField_burst", {"d": 1.5}],
    [4.8, "sound", "frozenBlast"]
    ]
  },
```

- The burst: the target stands 10 m from the cast point and the landing is 8.5 m (FieldLanding, 1.5 m short), so it is
  1.5 m past the field's centre, inside the 9 m ring. Marks at 0.8, 1.8, 2.8, 3.8 s (looks only), the burst at the 5th,
  **4.8 s** (Bible `penguin-skill-reference.md:795`: "burst at 4.8 s"). Its later marks (5.8 / 6.8 / 7.8 s) give Frost Bite, a look on the body only.
- `mBurstDone` is cleared when a field starts (Bible `penguin-skill-reference.md:795`; the only clear is FrostFieldLoop's `HashSet.Clear` on `mBurstDone` at its start, `Penguin.c:1343`), so every play of the tile bursts: no roll.

Variant "the hero leaps", if question 5 says so: leap and trail at 0 as above, then `frostField_land` and
`frostField_field` at `{"d": 8.5}`. The hero would need a page-side mover for 0.2-0.8 s (not an effect part).

### 2.3 Emperors March (`emperorPenguin`, 1.6 s; cell 454)

The cast is `DoRow6Skill` (`Penguin.c:36700-36790`):
- dir = the facing, or the flat direction to a foe within 22 m;
- `extra` = 3 if Constellation was cast in the last 8 s, else 0 (then the window is cleared);
- `addTimeOut(agiAdjust(120))`;
- `TakeFocus`.

It passes `coded = dir × (extra + 1)`, with y = 1 when Focus was taken.

Coroutine `TTO1102:Penguin.<RPC_emperorPenguin>d__356::MoveNext@0x1DEA490` (`Penguin.c:8457-9102`):
- **0.00** (state 0):
  - extra = round(|coded|) − 1, clamped 0..6 (`:8593`), so **5 penguins** by default;
  - red = coded.y > 0.5 (`:8594`);
  - `Row6Begin("emperorPenguin", mPos, dir)` (`:8628`);
  - `Until(start + 0)` (`:8645`; capstone 0x1DEA8F4 `xorps xmm1, xmm1; addss xmm6, xmm1`), which is one frame.
- **0.00** (state 1, about one frame):
  - `emperorPenguin_whistle` at `Row6Beak()`, hero rotation (`:8656-8668`);
  - `emperorPenguin_summon` at the hero, `LookRotation(dir)` (`:8693`);
  - `Row6Sound("emperorPenguin_whistle")` (`:8695`);
  - `Until(start + 0.3)` (`:8700`).
- **0.30** (state 2, still the current cast):
  - `emperorPenguin_crack` at hero + 1.75 × dir, `LookRotation(dir)` (`:8720-8743`; its own `sounds/iceBlock` 0.8);
  - `Row6Sound("iceBlock")` (`:8744`);
  - the flock tilt q = `LookRotation(dir) × Euler(0x3F490FDB = 45°, 0, 0)` (`:8766`; the product order is look × euler,
    read from the quaternion terms); axis = q × up = (0, 0.707 up, 0.707 forward);
  - for i < 5 + extra:
    - spot = `FlockSpot(dir, i, n)@0x1DA4BF0` (`:39146`). The angle comes from capstone 0x1DA4D4F-0x1DA4DDD:
      u = i / (n − 1) (0.5 if n ≤ 1), a = (150 u − 75)°, r = 1.25 for i < 5, else 1.9;
      spot = hero + (right sin a + dir cos a) r, on the ground (a 4 m raycast from 2 m up);
    - `emperorPenguin_emerge` at the spot, `LookRotation(dir)` (`:8821`);
    - `emperorPenguin_penguin` at spot − 0.7 × axis, rotation q (`:8829`);
  - with extra > 0 (+3): `constellation_impact` at hero + 1.2 × dir, identity (`:8846-8862`);
  - `FlockRise(penguins, axis)` (`:8867`);
  - `Until(start + 0.55)` (`:8874`).
- **FlockRise** (`TTO1102:Penguin.<FlockRise>d__357::MoveNext@0x1DC31F0`, `Penguin.c:986-1167`), for 0.25 s:
  - s = 4 (t − 0.3);
  - h = (1 − (1 − s)²) 0.7 + 0.15 sin(sπ);
  - position = start + axis × h, then exactly start + 0.7 axis (the spot) from 0.55.
- **0.55** (state 3):
  - ballAt = hero + 0.45 dir + 0.2 up (`:8892`);
  - `emperorPenguin_ball` at ballAt + 0.8 up, identity (`:8929`);
  - every frame until 0.8: ball = ballAt + up × (1 − u²) 0.8, with u = 4 (t − 0.55) (`:9021-9055`): from 1.0 m down to
    0.2 m.
- **0.80**:
  - `emperorPenguin_kick` at `Row6Foot()`, `LookRotation(dir)` (`:8963-8984`);
  - `emperorPenguin_launch` at ballAt, `LookRotation(dir)` (`:9006`);
  - `Row6Sound("cAttack")` (`:9008`);
  - `Until(start + 0.85)` (`:9013`).
- **0.85** (state 5):
  - `Row6Sound("emperorPenguin_flock")` (`:9063`);
  - `EmperorShot(ball, penguins, ballAt, dir, extra, focus, red)` (`:9068`);
  - `Until(start + 1.6)` (`:9077`).
- **1.60**: `Row6End` (`:9090`). The clip is 1.6 s ✓.

**EmperorShot** (`TTO1102:Penguin.<EmperorShot>d__358::MoveNext@0x1DC1520`, `Penguin.c:103-969`):
- reach = 22 m (`0x41B00000`, `:284`), or 0.3 m short of a wall (`:309`; no walls on the page);
- every frame, d = min(28 e, reach), with e = time since 0.85 (`:441-444`). The ball is at from + dir d, at ground + 0.45
  (`:479`), spinning about the side axis at 900°/s (`:578`);
- the frost trail: `frostAt` from 1.2 (`:428`) while ≤ d. `emperorPenguin_frost` at from + dir × frostAt, on the ground
  (from 2.2 up, `:525`), `LookRotation(dir)` (`:551`); then frostAt += 1.6 (`:552`);
- the flock, penguin i:
  - delay = 0.06 + 0.035 i (`:588`); s = clamp01((e − delay) / 0.18) (`:589`);
  - target = from + dir × max(0, d − 28 delay) + (side cos θ + up sin θ) 0.65 + 0.15 up (`:612-620`);
  - θ = 2π i / n + 540° × e (capstone 0x1DC2287-0x1DC22B3);
  - position = lerp(start, target, s);
  - rotation = slerp(startRot, `LookRotation(motion) × Euler(0x3FB2B8C2 = 80°, 0, 0)`, s) (`:682`): the flock whirls
    around the lane, belly-down;
- hits along the lane (`:729`): each foe once, `AddFrostMarks(foe, n)`. A foe of weight ≥ 60, or a structure, stops the
  ball;
- at d ≥ reach (`:817`), or a stop:
  - `GoalFx(ballPos, dir, red)@0x1DA74E0` (`:852`, `Penguin.c:38964`): `emperorPenguin_goal` at the ball,
    `LookRotation(flat dir)`, and `Row6Sound("absoluteZero")`;
  - the Goal hits;
  - `Destroy(ball)` (`:842`);
  - `Scatter@0x1DB09F0` (`:844`, `:39047`): `emperorPenguin_poof` at each penguin's position, identity, then
    `Destroy(penguin)`;
- the owner's client does this. Other clients get the Goal through `RPC_emperorGoal`.

Full reach (question 2's default) puts the Goal at 0.85 + 22 / 28 = **1.636 s** (the first frame with d ≥ 22), at
0.45 + 22 = **22.45 m ahead, 0.45 m up** ✓ (Bible :809: 1.64 s, 22.45 m). Numbers from `calc.py`:
- Flock spots (x, d): (−1.207, 0.324), (−0.761, 0.992), (0, 1.25), (0.761, 0.992), (1.207, 0.324). Each penguin starts
  0.495 m lower and 0.495 m behind its spot.
- Frosts (t, d): (0.893, 1.65), (0.95, 3.25), (1.007, 4.85), (1.064, 6.45), (1.121, 8.05), (1.179, 9.65), (1.236, 11.25),
  (1.293, 12.85), (1.35, 14.45), (1.407, 16.05), (1.464, 17.65), (1.521, 19.25), (1.579, 20.85).
- Poofs at the Goal (x, y, d), with every s = 1:
  - i 0: (0.282, 0.936, 20.77);
  - i 1: (−0.47, 0.799, 19.79);
  - i 2: (−0.572, 0.042, 18.81);
  - i 3: (0.116, −0.29, 17.83);
  - i 4: (0.644, 0.263, 16.85).
- Kills:
  - the ball: spawned 0.55, destroyed 1.636, so 1.086 (its own life is 4 + 0.2);
  - the penguins: 0.3 → 1.636, so 1.336 (own life 6 + 0.2).

```json
  "emperorPenguin": {
    "why": "TTO1102:Penguin.<RPC_emperorPenguin>d__356::MoveNext@0x1DEA490 (Penguin.c:8457-9102; plans/fx_penguin/tto.md 2.3; 5 penguins, no Focus, the ball's full 22 m: checks/fx_penguin_research/tto/calc.py): 0: Row6Begin (:8628), Until(start + 0) (:8645), then emperorPenguin_whistle at Row6Beak@0x1DAF620 = Head + 0.16 fwd - 0.03 up (0.17 ahead, 0.04 right, 0.64 up on the page's rig) with the hero's rotation, emperorPenguin_summon at the hero, Row6Sound emperorPenguin_whistle (TTO's own sounds/ clip, :8656-8695); Until 0.3: emperorPenguin_crack 1.75 m ahead (:8720-8743; its own sounds/iceBlock 0.8) + Row6Sound iceBlock (:8744), per penguin i of 5 emperorPenguin_emerge at FlockSpot@0x1DA4BF0 (angle (150 i/4 - 75) deg, r 1.25, capstone 0x1DA4D4F-0x1DA4DDD) and emperorPenguin_penguin 0.7 m down the 45 deg tilt axis from it, turned LookRotation(dir) x Euler(45, 0, 0) (:8766-8829), rising along it for 0.25 s (FlockRise@0x1DC31F0, :986-1167); Until 0.55: emperorPenguin_ball 0.45 ahead, 1.0 up, dropped to 0.2 m by 0.8 (:8892-9055); 0.8: emperorPenguin_kick at Row6Foot@0x1DB0160 = Foot2_R (0.10 ahead, 0.19 right, 0.17 up), emperorPenguin_launch at the ball (0.45 ahead, 0.2 up), Row6Sound cAttack (:8963-9008); Until 0.85: Row6Sound emperorPenguin_flock (TTO's own), EmperorShot@0x1DC1520 (:103-969): the ball rolls 28 m/s to 22 m at ground + 0.45, spinning 900 deg/s, an emperorPenguin_frost on the ground every 1.6 m from 1.2 m (float32: 13, the last 20.85 m ahead, :428-552), the flock whirls round the lane (0.65 m, 540 deg/s, 0.06 + 0.035 i behind, :588-682); Until 1.6: Row6End (:9090); 0.85 + 22/28 = 1.636: GoalFx@0x1DA74E0 emperorPenguin_goal at the ball 22.45 m ahead, 0.45 up + Row6Sound absoluteZero (:852), Destroy(ball) (kill 1.086), Scatter@0x1DB09F0 emperorPenguin_poof at each penguin, then Destroy (kill 1.336) (:842-844); no voice, no Multi Cast roll; the ball passes the 10 m target at 0.85 + (10 - 0.95)/28 = 1.173 s (lane test :790-791): AddFrostMarks(foe, 5) (:811) = an instant Frost Burst (:38311), BurstFx@0x1DA3310 (:38592-38640): frostField_burst at the foe's feet, identity, + Row6Sound frozenBlast (sounds/), at the target point 10 m ahead; the cues after 1.6 s run on in the idle tail; left out: the frostMarkFx / frostBiteFx looks on the foe (status looks on its body, Sheep decision 4; the hits draw nothing); constellation_impact 1.2 m ahead only with Constellation's +3 penguins (:8846-8862)",
    "cues": [
    [0, "fx", "tto/emperorPenguin_whistle", {"d": 0.17, "x": 0.04, "y": 0.64}],
    [0, "fx", "tto/emperorPenguin_summon"],
    [0, "sound", "emperorPenguin_whistle"],
    [0.3, "fx", "tto/emperorPenguin_crack", {"d": 1.75}],
    [0.3, "sound", "iceBlock"],
    [0.3, "fx", "tto/emperorPenguin_emerge", {"x": -1.207, "d": 0.324}],
    [0.3, "fx", "tto/emperorPenguin_emerge", {"x": -0.761, "d": 0.992}],
    [0.3, "fx", "tto/emperorPenguin_emerge", {"d": 1.25}],
    [0.3, "fx", "tto/emperorPenguin_emerge", {"x": 0.761, "d": 0.992}],
    [0.3, "fx", "tto/emperorPenguin_emerge", {"x": 1.207, "d": 0.324}],
    [0.3, "fx", "tto/emperorPenguin_penguin", {"x": -1.207, "y": -0.495, "d": -0.171, "rot": [45, 0, 0], "i": 0, "to": [0, 0.45, 22.45], "kill": 1.336}],
    [0.3, "fx", "tto/emperorPenguin_penguin", {"x": -0.761, "y": -0.495, "d": 0.497, "rot": [45, 0, 0], "i": 1, "to": [0, 0.45, 22.45], "kill": 1.336}],
    [0.3, "fx", "tto/emperorPenguin_penguin", {"y": -0.495, "d": 0.755, "rot": [45, 0, 0], "i": 2, "to": [0, 0.45, 22.45], "kill": 1.336}],
    [0.3, "fx", "tto/emperorPenguin_penguin", {"x": 0.761, "y": -0.495, "d": 0.497, "rot": [45, 0, 0], "i": 3, "to": [0, 0.45, 22.45], "kill": 1.336}],
    [0.3, "fx", "tto/emperorPenguin_penguin", {"x": 1.207, "y": -0.495, "d": -0.171, "rot": [45, 0, 0], "i": 4, "to": [0, 0.45, 22.45], "kill": 1.336}],
    [0.55, "fx", "tto/emperorPenguin_ball", {"d": 0.45, "y": 1.0, "to": [0, 0.45, 22.45], "kill": 1.086}],
    [0.8, "fx", "tto/emperorPenguin_kick", {"d": 0.1, "x": 0.19, "y": 0.17}],
    [0.8, "fx", "tto/emperorPenguin_launch", {"d": 0.45, "y": 0.2}],
    [0.8, "sound", "cAttack"],
    [0.85, "sound", "emperorPenguin_flock"],
    [0.893, "fx", "tto/emperorPenguin_frost", {"d": 1.65}],
    [0.95, "fx", "tto/emperorPenguin_frost", {"d": 3.25}],
    [1.007, "fx", "tto/emperorPenguin_frost", {"d": 4.85}],
    [1.064, "fx", "tto/emperorPenguin_frost", {"d": 6.45}],
    [1.121, "fx", "tto/emperorPenguin_frost", {"d": 8.05}],
    [1.173, "fx", "tto/frostField_burst", {"d": 10}],
    [1.173, "sound", "frozenBlast"],
    [1.179, "fx", "tto/emperorPenguin_frost", {"d": 9.65}],
    [1.236, "fx", "tto/emperorPenguin_frost", {"d": 11.25}],
    [1.293, "fx", "tto/emperorPenguin_frost", {"d": 12.85}],
    [1.35, "fx", "tto/emperorPenguin_frost", {"d": 14.45}],
    [1.407, "fx", "tto/emperorPenguin_frost", {"d": 16.05}],
    [1.464, "fx", "tto/emperorPenguin_frost", {"d": 17.65}],
    [1.521, "fx", "tto/emperorPenguin_frost", {"d": 19.25}],
    [1.579, "fx", "tto/emperorPenguin_frost", {"d": 20.85}],
    [1.636, "fx", "tto/emperorPenguin_goal", {"d": 22.45, "y": 0.45}],
    [1.636, "sound", "absoluteZero"],
    [1.636, "fx", "tto/emperorPenguin_poof", {"x": 0.282, "y": 0.936, "d": 20.77}],
    [1.636, "fx", "tto/emperorPenguin_poof", {"x": -0.47, "y": 0.799, "d": 19.79}],
    [1.636, "fx", "tto/emperorPenguin_poof", {"x": -0.572, "y": 0.042, "d": 18.81}],
    [1.636, "fx", "tto/emperorPenguin_poof", {"x": 0.116, "y": -0.29, "d": 17.83}],
    [1.636, "fx", "tto/emperorPenguin_poof", {"x": 0.644, "y": 0.263, "d": 16.85}]
    ]
  }
```

- `to` on the ball and the flock = where the ball stops (the Goal). `i` (new) = the penguin's index, which fixes its delay
  and ring angle. The flock size (5) is the mover's default, or a second key once +3 is wanted.
- Each frost spawns on the first frame with d ≥ frostAt, which is at most one frame after its time.
- **The Frost Burst on the 10 m target** (added 2026-11-10): the ball's lane test takes a foe once its centre is within
  0.5 m ahead of the ball (`Penguin.c:790-791`), the ball starting 0.45 m ahead at 28 m/s, so the 10 m target is hit at
  0.85 + (10 − 0.45 − 0.5) / 28 = 0.85 + 9.05 / 28 = 0.85 + 0.323 = **1.173 s** (Bible `penguin-skill-reference.md:808`:
  `0.85 + max(0, d − 0.95) / 28`). `AddFrostMarks(foe, 5)` (`:811`) gives 5 marks at once (Bible `:810`), so the 5th is
  this hit: `FrostBurst` → `BurstFx` (`:38311`, `:38592-38640`) = `frostField_burst` at the foe's feet, identity, and
  `Row6Sound("frozenBlast")`. Its `mBurstDone` is cleared only by a Frost Field (Bible `:810`): in the game a foe bursts
  once per map without one; the tile shows the first play's look every time (one play = one fresh foe).
- Variant "+3 penguins" (question 3), n = 8:
  - extra spots at i 5-7, r 1.9;
  - u = i / 7 for every penguin, so all 8 spots move;
  - `constellation_impact` at `{"d": 1.2}` at 0.3 s;
  - 8 poofs.

  `calc.py` gives the numbers with `flock = 8`.

## 3. What is left out, all three (only "on an enemy" / "needs an attacker")

- The statuses' looks on the foe's body (on an enemy with no target-point analogue: Sheep decision 4, a status look
  does not float over the empty spot):
  - `manaFracture` → `manaFractureFx`;
  - `frostMark` → `frostMarkFx`;
  - `frostBite` → `frostBiteFx` (AddPenguinRow6Fx@0x24ADC20, section 1);
  - the 20 % `frost` freeze (`Penguin.<Freeze>d__352::MoveNext@0x1DC3720`, `Penguin.c:1186`; BB's frost look).
- The hits themselves draw nothing (`CharacterControl::hit@0x24D57E0`, `CharacterControl.c:6555`: no effect load).
- **Cued now, not left out:** the Frost Burst on the target (`BurstFx@0x1DA3310`, `Penguin.c:38592-38640`:
  `frostField_burst` at the foe's feet + `Row6Sound("frozenBlast")`), at the target point: Emperors March 1.173 s at
  10 m, Frost Field 4.8 s at 1.5 m (sections 2.2, 2.3). The Frost Burst's splash on other foes within 3 m has no
  look of its own.
- Nothing is left out for a missing part: every effect is cued, and the parts are listed in section 6.

## 4. Sounds and voices

- All `"sound"` (the `sounds/` folder). In BB's rip they are
  `C:\Users\Jump\Desktop\12tails\RippedAssets\ExportedProject\Assets\Resources\gameassets\characters\heroes\penguin\sounds\<name>.wav`.
  Lengths, TTO = BB: fallingStar_ring 1.448, castEffect 0.960, manaArc 0.928, fallingComet 2.497, novarFlare 1.998,
  blink 0.884, iceBreak 0.419, blizzard 2.874, iceBlock 0.862, cAttack 1.040, absoluteZero 2.268.
- TTO-only (in TTO's bundle at `gameassets/characters/heroes/penguin/sounds/`): emperorPenguin_whistle 0.620,
  emperorPenguin_flock 1.052.
- The prefabs' own AudioSources (play on awake, built with the effect), from BB's `sounds/`:
  - `fallingStar_hit` 1.952: `constellation_impact` vol 0.8, `constellation_giantImpact` vol 1.0;
  - `iceBlock`: `emperorPenguin_crack` vol 0.8.
- No voices (`voices/`) in any of the three.

## 5. Probed 2026-11-10 (office PC, TTO's 2026-11-09 bundles)

`uv run --no-project --with UnityPy --with pillow --with imageio-ffmpeg python -I pipeline/wardrobe_fx_tto.py penguin --probe <28 names>`
→ `checks/fx_penguin_research/tto/probe.json`. The summary is `compact.txt`, from `compact.py`.

The catalog has 91 Penguin effects; these 28 are TTO-only. The rest are BB's names.

| Prefab | EffectControl (life + after) | Parts (node: type) | AudioSource |
|---|---|---|---|
| constellation_cast | 1.0 + 0.5, followPosition | GroundHug (Rune), 4 ImageEmitters, PS Stars | - |
| constellation_mark | 5.0 + 0.3 | 5 ImageEmitters, GroundHug (Floor), PS Dust (loop) | - |
| constellation_line | 6.0 + 0.2 | **2 LineRenderers** (Glow, Core; world space, disabled, 2 points) | - |
| constellation_star | 1.4 + 0.4 | 4 PS (Meteor1 with **TrailModule**), GroundHug (Warn) | - |
| constellation_impact | 1.0 + 0.4 | 2 GroundHugs, 3 ImageEmitters, PS Sparks, PS Dust | fallingStar_hit 0.8 |
| constellation_lineFire | 1.0 + 0.4 | PS Sparks, PS Motes (Box shape, stretched by the root's z scale) | - |
| constellation_ignite | 0.9 + 0.4 | 2 ImageEmitters, PS Motes | - |
| constellation_giant | 1.4 + 0.4 | 8 PS (Giant1, Escort1 with **TrailModule**), 2 GroundHugs | - |
| constellation_giantImpact | 1.8 + 0.6 | 4 GroundHugs, 4 ImageEmitters, 3 PS (Five with **TrailModule**) | fallingStar_hit 1.0 |
| frostField_leap | 0.9 + 0.3 | 3 GroundHugs, ImageEmitter, PS Snow / Glints, PS Chunks (mesh `penguinRow6_spike`) | - |
| frostField_trail | 0.75 + 0.6, followPosition | ImageEmitter, 2 TrailRendererModern, 3 PS (loop) | - |
| frostField_land | 1.8 + 0.4 | 5 GroundHugs, 4 ImageEmitters, 10 mesh PS (spike), PS Shards (stretched), PS Snow | - |
| frostField_field | **8.0 + 0.6** | 7 GroundHugs, 8 mesh PS (spike), 4 PS (6.5-7 s), PS Crystals (mesh) | - |
| frostField_burst | 1.4 + 0.5 | 8 mesh PS (spike), 3 GroundHugs, 5 ImageEmitters, PS Shards, PS Snow | - |
| emperorPenguin_whistle | 0.7 + 0.3 | 6 ImageEmitters, PS Notes, PS Gust | - |
| emperorPenguin_summon | 1.1 + 0.4 | 3 GroundHugs, PS Swirl, PS Glints | - |
| emperorPenguin_crack | 1.6 + 0.5 | 2 GroundHugs, PS Chunks (mesh), PS Snow | iceBlock 0.8 |
| emperorPenguin_emerge | 1.2 + 0.4 | 3 ImageEmitters, 3 mesh PS, 2 GroundHugs, PS Plume / Glints | - |
| emperorPenguin_penguin | 6.0 + 0.2 | **SkinnedMeshRenderer** `SmallIcePenguin_tri` (7 bones, no Animation: bind pose; Body scale 1.4; the staff bone scale 0), material `tto_SmallIcePenguin` = **FlexibleCelShader/Cel No Outline**; ImageEmitter Aura, 2 TrailRendererModern, 2 PS (loop) | - |
| emperorPenguin_ball | 4.0 + 0.2 | StaticMesh `SoccerBall_tri` (168 v, blend opaque, tex SoccerBall), 4 ImageEmitters, 2 TrailRendererModern, 5 PS (IceBits mesh) | - |
| emperorPenguin_kick | 0.5 + 0.3 | 4 ImageEmitters, 2 PS | - |
| emperorPenguin_launch | 0.9 + 0.3 | 3 PS Rings (mesh = **Unity built-in Quad**), PS Streaks, PS Gust, GroundHug, 2 ImageEmitters | - |
| emperorPenguin_frost | 1.6 + 0.4 | 2 GroundHugs, 2 mesh PS (spike), PS Snow | - |
| emperorPenguin_goal | 2.2 + 0.5 | 5 GroundHugs, 6 ImageEmitters, 7 mesh PS (spike), PS Net / Net2 (**built-in Quad**), 3 PS (Shards, Stars, Afterfall) | - |
| emperorPenguin_poof | 0.8 + 0.3 | 3 ImageEmitters, 2 PS | - |
| frostMarkFx / frostBiteFx / manaFractureFx | **none** (status looks on foes) | 3 PS each | - |

- **The mesh particles.** `penguinRow6_spike` (378 vertices) comes inline in the renderer's `mesh`, which shuriken.js
  draws.
  - The built-in-Quad renderers keep an unresolved `m_Mesh` `{"file": 3, "pathID": 10210}`. That is Unity's
    `unity default resources` Quad, which is not in any bundle.
- **Shuriken modules used:** Color, Velocity, Size, Rotation and **Trail** (4 systems).
  - Shapes: sphere 0, hemisphere 2, cone 4, box 5, circle 10. All of them are in shuriken.js.
  - Trail is in shuriken.js's skip list (`P.skipped`, shuriken.js:258).
- **Textures** (14): tto_IcePenguin1, tto_Line_DoubleEdge1, tto_Line_SimpleBall, tto_Line_vertMultilines4,
  tto_SoccerBall, tto_frost, and tto_penguinRow6_{crack, fang, fracture, frostFacets, iceDisc, rune, snowflake, star}.
- **Blends:** addsoft 9, add 3, opaque 1, `shader:FlexibleCelShader/Cel No Outline` 1.
  - The cel shader's props: `_RampLevels` 2, `_HighIntensity` 1.5, `_LowIntensity` 1, `_HighColor` / `_LowColor`
    white, `_OutlineSize` 0, no rim and no fresnel.
- **No followState anywhere. No GroundFollower, ArcRibbon or HelixRibbon / Bolt / GroundConform.**

## 6. Parts the page lacks (effect: part)

| # | Part | Effects | What it does (source) |
|---|---|---|---|
| P1 | `Penguin.StarLines` code mover (CODE_MOVERS) on the line | constellation_line | Both LineRenderers run from the cue's spot to `to`. The end point grows over 0.12 s from spawn. Enabled once f > 0. `widthMultiplier × 2.2` at `ignite` s (StarLines@0x1E2C220, `Penguin.c:22659-22703`, `:22833`). |
| P2 | Shuriken **TrailModule** (particle ribbons) in shuriken.js | constellation_star, constellation_giant, constellation_giantImpact | The meteors' streaks (Meteor1, Giant1, Escort1, Five). |
| P3 | **TTO SkinnedMeshRenderer export** in wardrobe_fx_tto.py (vertices, weights, bind poses in mesh.js's shape; today `{"mesh": name}` only) + the **`FlexibleCelShader/Cel No Outline`** shader (a 2-level ramp cel shader) | emperorPenguin_penguin | The flock's ice-penguin bodies. |
| P4 | `Penguin.EmperorShot` / `Penguin.FlockRise` code movers on the ball and the flock | emperorPenguin_ball, emperorPenguin_penguin | Ball: drop 0.55-0.8, roll at 28 m/s to `to` at ground + 0.45, spin 900°/s about the side axis. Penguin: rise 0.3-0.55, then whirl after the ball (index `i`, delay 0.06 + 0.035 i, ring 0.65 m at 540°/s, slerp to LookRotation(motion) × Euler(80, 0, 0) over 0.18 s). (Penguin.c:986-1167, :103-969) |
| P5 | Cue option `scale` as `[x, y, z]` (index.html:3149) | constellation_lineFire | localScale (1, 1, segment length) (`Penguin.c:22904`). |
| P6 | Unity's built-in **Quad** as a particle mesh (pathID 10210) | emperorPenguin_launch (Ring1-3), emperorPenguin_goal (Net, Net2) | A 1 × 1 quad in the XY plane. Either wardrobe_fx_tto.py writes it, or shuriken.js falls back to it. |
| P7 | (page, optional, question 5) a hero mover | frostFieldLeap | The 0.6 s leap of the Penguin itself (`Penguin.c:11441-11485`). |
| P8 | `"sound"` cues from TTO's bundle | emperorPenguin (sounds emperorPenguin_whistle, emperorPenguin_flock) | `wardrobe_fx.py` reads only BB's rip. wardrobe_fx_tto.py already decodes TTO's own clips (FMOD) for AudioSources; it needs `gameassets/characters/heroes/penguin/sounds/<name>` too. |

Parts that already exist and are used here: EffectControl, ImageEmitter, GroundHug (`groundhug.js`), Shuriken (mesh mode,
stretched, World / Local), LineRenderer and TrailRendererModern (`tto_sheep.js`), StaticMesh (`mesh.js`), AudioSource.
None uses `arcribbon.js` or `groundfollower.js`.

Build notes for the parts stage (home or office: this PC has the bundles):
- add `SKILL_FX["penguin"]` (these 28 names, so the left-out ones are built too);
- add CODE_MOVERS for `constellation_line`, `emperorPenguin_ball` and `emperorPenguin_penguin`;
- then run `wardrobe_fx_tto.py penguin` and `wardrobe_fx.py penguin` (the BB `sounds/`).

## 7. New questions (only what the Sheep / Wolf decisions don't answer)

1. **Constellation: how many stars?** The decisions put "the target" 10 m ahead but don't say whether other foes stand
   near it. Constellation's look (lines, ignition, Giant Star: 5 of its 9 prefabs) needs 3 or more.
   - Default: **B, five stars**: the target and 4 foes in a 3 m pentagon about 13 m ahead.
   - A is one star: cast, mark, star, impact.
2. **Emperors March: does the 10 m target stop the ball?** Only a foe of weight ≥ 60, or a structure, does.
   - Default: **no**: the full 22 m run and the Goal at 22.45 m, 1.636 s.
   - Otherwise the Goal comes at the target, 1.173 s: the ball stops "right after hitting" it (Bible
     `penguin-skill-reference.md:809`), so the Goal, the burst and the poofs all at 1.173 s near 10 m, the frosts up
     to 8.05 m (the 9.65 m one comes at 1.179, after the stop), the ball's and the flock's kills shortened to 0.623 /
     0.873.
   - Sheep decision 3 (the ball ends at the target point) was a homing ball that the game always ends on a hit; this
     ball passes a light foe, so the decision doesn't settle it.
3. **+3 penguins** (Constellation cast within the last 8 s): default **5** (the tile played alone).
4. **Focus Intellect's red Emperors March** (FocusRedden): default **off**. Focus is a separate active skill, not a
   passive.
5. **Frost Field's leap**: default **in place** (Feral Strike's convention: the land and the field at the hero). The
   alternative is a page hero mover (P7), with the land and the field 8.5 m ahead.
(The first draft's question 6, the Frost Burst on the target, is answered by the decisions: effects on the target go
to the target point; cued, sections 2.2 / 2.3.)

## 8. For the Bible (offer to the user; that repo's own rules)

- Emperors March:
  - the frost trail is 13 prints, one every 1.6 m from 1.65 m, the last at 20.85 m; float32 drops the 14th;
  - the flock whirls round the lane at 540°/s, 0.65 m out;
  - `iceBlock` plays twice at 0.3 s;
  - Focus turns every effect red (`FocusRedden`);
  - the `emperorPenguin_launch` effect comes at 0.8 s, not 0.85.
- Constellation:
  - the lines widen ×2.2 at ignition;
  - with 2 stars the line vanishes 0.6 s after ignition;
  - with no stars the Penguin never leaves `attack` (`RPC_constellation` state 1).
- Frost Field: the Penguin's `frostField` buff has no look.

## Verification (2026-11-10)

A skeptical re-trace by a checker agent (office PC). Probes in `checks/fx_penguin_research/verify/`:
`tto_calc.py` (float32 frost count, flock spots, Goal and burst times) and `tto_probe4.json` (a fresh
`wardrobe_fx_tto.py penguin --probe constellation_line,frostField_field,frostField_trail,constellation_cast`).

**What I checked, against `DecompiledSource_TTO_2026-11-02\pseudo\Penguin.c` (function cites are the `// ====` header
lines, 2 above the bodies; that is fine):**
- RPC_constellation: Row6Begin :6849, ClearStarFx :6855, fallingStar_ring :6856, constellation_cast owned (flag 1)
  :6871, Until 0.4 :6876, marks :6924, castEffect :6943, StarLineCount :6948, lines :6973, StarLines :7004, Until 1
  :7011, Row6End :7022. All held.
- StarLines: lastImpact = start + 1.1 + 0.6 + 0.3 (n − 1) (:22538-22539); draw f with 0.12 (:22658-22659); the star at
  start + 1.1 + 0.3 i (:22715), the mark destroyed and StarImpact 0.6 s later (:22744-22770); ignite at lastImpact +
  0.05 (:22778); lineFire at the midpoint of the two marks (fixedAt + up), LookRotation, localScale (1, 1, length)
  (:22884-22904); ignite + manaArc, giant + fallingComet, ClearStarFx + giantImpact + novarFlare at + 0.6
  (:22921-22981). Every string literal resolved (manaArc, fallingComet, novarFlare, constellation_star / lineFire /
  ignite / giant / giantImpact). The variant B numbers re-derived by hand: pentagon vertices, the 5 midpoints, length
  3.527, yaws 18 / 90 / 162 / −126 / −54, each line's `ignite` + spawn = 2.95 and `kill` + spawn = 3.55, mark kills.
- RPC_frostFieldLeap: blink :11395, Until 0.2 :11400, leap :11423 (not owned), trail :11438 (owned), flight 0x3F19999A
  :11441, arc ×10 :11478, land :11523 (not owned), iceBreak :11525, FrostFieldLoop :11528, Until 1.1 :11534, Row6End
  :11545. FrostFieldLoop: field :1324, Destroy 9 :1335, blizzard :1337, mBurstDone cleared :1343, end = now + 8 :1345,
  first tick = now (:1347), +1 s each (:1393), 9 m (81) :1376, AddFrostMarks(foe, 1, fromField) :1432. AddFrostMarks:
  marks forgotten after 3 s, burst on the 5th (`< 5` test), FrostBurst :38311; BurstFx (:38590) spawns
  frostField_burst and plays frozenBlast. FieldLanding: min(dist, 14) − 1.5, 9.5 m with no target, so 8.5 m for a
  10 m target, the target 1.5 m past the centre: the 4.8 s / 1.5 m burst cue holds.
- RPC_emperorPenguin: Until(start + 0.0) :8645, whistle / summon / whistle sound :8668-8695, Until 0.3 :8700, crack
  1.75 :8720-8743, iceBlock :8744, emerge :8821, penguin :8829, constellation_impact 1.2 :8846-8862, FlockRise :8867,
  Until 0.55 :8874, ballAt 0.45 dir + 0.2 up :8892-8908, ball + 0.8 up :8929, kick (Row6Foot) / launch (ballAt) /
  cAttack :8963-9008, Until 0.85 :9013, flock :9063, EmperorShot :9068, Until 1.6 :9077, Row6End :9090. All strings
  resolved. EmperorShot: reach 0x41B00000 = 22, 28 m/s, frostAt 0x3F99999A = 1.2 step 1.6, 900, 0.65, 0.15, 0.06,
  0.035, 0.18 all present; the lane test (:790-791) is `proj(foe − from) ≤ d + 0.5`, so a foe 10 m from the hero
  (9.55 m from `from`) is hit at d = 9.05: 0.85 + 9.05 / 28 = 1.1732 s; AddFrostMarks(foe, flock) right after the hit
  (:811). Float32: 13 frosts (frostAt after 13 steps = 22.000002 > 22), Goal at 0.85 + 22 / 28 = 1.6357 s. Flock spots
  (−1.207, 0.324) ... (1.207, 0.324) and the poofs' y (from.y 0.2 + 0.15 + 0.65 sin θ) re-derived.
- Row6Beak (Head, 0.16, 0.03, fallback 0.67), Row6Foot (Foot2_R, fallback 0.3), Row6Sound (`sounds/` path, volume 1
  owner / 0.75 others, PlayOneShot) held. `CharacterControl::hit` (TTO CharacterControl.c:6555-7090) loads no effect
  (its only effect-like string is `BarrierFX`, a lookup on the hit one); AddPenguinRow6Fx's literals are frostBite,
  frostMark, manaFracture (+ `Fx`).
- Targets: Constellation and Emperors March hit foes only; Frost Field's only self status is `frostField` (0x3F7 on
  the caster), which has no look. No ally effect is cued.
- Sounds: all 13 BB names are in the rip's `penguin/sounds/` and none in `voices/` (42 files in `sounds/`); the two
  TTO-only ones are in neither. Clip lengths 1.0 / 1.1 / 1.6 in `wardrobe/data/penguin/clips.json`.
- Prefabs: `compact.txt` matches the table row by row (node counts recounted); `probe.json` has 28 effects and no
  `followState: true`; my fresh probe gives the same EffectControl values (line 6 + 0.2, field 8 + 0.6, trail
  0.75 + 0.6 followPosition, cast 1 + 0.5 followPosition) and both LineRenderers `m_Enabled` false.
- Bible lines (`penguin-skill-reference.md`): 764, 782, 793, 795, 807, 808 (the `0.85 + max(0, d − 0.95) / 28` formula),
  809, 810 held; two were off (below). Page: `index.html:3149` (scale × number), `:3467` cueOf (drops unknown keys,
  passes `scale` through) held.

**Corrections made in this file:**
1. "no cast bar (Bible :770" -> ":771". Proof: `penguin-skill-reference.md:771` is "**Cast:** no cast bar (they never go
   through `RPC_cast1` ..."; :770 is the skill-data line.
2. "(Bible :808: 1.64 s, 22.45 m)" -> ":809". Proof: :809 "Stop and Goal ... (at full range 1.64 s, 22.45 m ahead)".
3. "`mBurstDone` is cleared when a field starts (... AddFrostMarks :38268-38306)" -> FrostFieldLoop `Penguin.c:1343`.
   Proof: :1343 `HashSet<T>::Clear(*(lVar1 + 0x6f8))`, and 0x6f8 is `mBurstDone` (AddFrostMarks :38270-38272 reads it,
   :38306 only adds to it); `HashSet<int>::Clear` is used nowhere else in the file.
4. Section 5, `emperorPenguin_goal`: "4 PS" -> "3 PS (Shards, Stars, Afterfall)". Proof: `compact.txt` line 24; the
   other PS are the 7 mesh ones and Net / Net2.

**Unresolved (not disproved, not re-run):** the 1102 = 1109 identity (`cmp1109.py`, capstone over both DLLs) and the
AddPenguinRow6Fx dispatch addresses (`callers.py`, `jumps.py`) were not re-run; the rig-derived beak / foot offsets
(`bones.py`) and the sign of `side` in the poofs' x were not re-derived; the 0.6 of the no-Giant `Until()` (capstone
0x1E2D59A) was not re-read (it only matters for n = 1 / 2).

## Built 2026-11-10 (home PC, the `tto` builder of the Penguin build)

The parts of section 6 (P1-P6, P8; not P7, decision 8) are built and the Penguin's TTO effects are in
`wardrobe/data/penguin/fx.json` (`uv run --no-project --with UnityPy --with pillow --with imageio-ffmpeg python -I
pipeline/wardrobe_fx_tto.py penguin`: "28 TTO effects, 14 materials, 14 textures, 4 sounds (2 TTO's own:
emperorPenguin_flock, emperorPenguin_whistle)"; 12 new `wardrobe/data/fx/tex/tto_*.webp`, the shared `tto_Line_*` ones
rewritten byte for byte the same). Decisions applied: 6 (five stars), 7 (the full 22 m run, the Goal at 22.45 m,
1.636 s), 8 (Frost Field in place: no hero mover), 14 (5 penguins), 15 (no FocusRedden). Probes in
`checks/fx_penguin_build/tto/` (git-ignored): `probe.json` / `probe3.json` (the 28 prefabs, before / after the exporter
changes), `cel_dxbc.py` -> `dxbc_cel.txt` + `cel_parsed.json` (the cel shader), `cel_mat.py`, `trail.py`, `cues.py` ->
`cues.json` (the block below, parsed and checked against fx.json), `parts_check.mjs` -> `parts_check.txt` (a node run
of the parts on the built data, three 0.160.0 as the page: 52 checks pass).

### What was built, by part

| # | Part | Where | Notes |
|---|---|---|---|
| P1 | `Penguin.StarLines` | `wardrobe/fxparts/tto_penguin.js` (new), on `constellation_line` (CODE_MOVERS) | Draws the line's two LineRenderers itself: tto_sheep.js's LineRenderer part leaves disabled ones (`m_Enabled` false, as these are) unbuilt. From the cue's spot to `to`, f = clamp01(age / 0.12), shown once f > 0, x 2.2 wide at `ignite` (else kill - 0.6). |
| P2 | Shuriken TrailModule | `wardrobe/fxparts/shuriken.js` | Particle trails (mode 0) and ribbons (mode 1), the renderer's `m_Materials[1]` (Unity's trailMaterial). |
| P3 | SkinnedMeshRenderer export + `FlexibleCelShader/Cel No Outline` | `pipeline/wardrobe_fx_tto.py`; the shader in `tto_penguin.js` (api.shader) | The BB build's shape (mesh + `w` / `j` / `bind`, `bones` node indices, `root`, `mats`), so mesh.js skins it unchanged. SmallIcePenguin_tri: 1145 vertices, 900 triangles, 7 bones (staff, Root, Spine, Head, Tail, Leg_R, Leg_L). |
| P4 | `Penguin.EmperorShot`, `Penguin.FlockRise` | `tto_penguin.js`, on `emperorPenguin_ball` / `emperorPenguin_penguin` (CODE_MOVERS) | The ball's drop, roll, spin and Destroy at the Goal; the penguins' rise, whirl after the ball and Destroy at the Goal (Scatter). |
| P5 | cue `scale` `[x, y, z]` | index.html (not mine) | Still needed by the five lineFire cues (shared change). |
| P6 | Unity's built-in Quad | `wardrobe_fx_tto.py` BUILTIN_MESH (inline `mesh`, `m_Mesh` = `{"mesh": "Quad", "builtin": 10210}`); `shuriken.js` QUAD as a fallback | The external file of the reference is `Library/unity default resources` (checked by the exporter), path id 10210. |
| P8 | TTO's own sounds | `wardrobe_fx_tto.py` SKILL_SOUNDS + `tto_clips()` | `gameassets/characters/heroes/penguin/sounds/emperorPenguin_whistle` / `_flock` through the catalog -> `wardrobe/data/penguin/sfx/<name>.mp3` (0.65 s / 1.05 s as mp3). Also any `"sound"` cue the rip's `sounds/` lacks. |

`groundhug.js`, `arcribbon.js`, `groundfollower.js`: no change needed. The Penguin's 44 GroundHugEmitters are shapes 0
(Disc) and 1 (Band), none with motes; one (`constellation_mark`'s Floor) has `resample` 0.12, which groundhug.js already
reads (the live centre; the page's foe stands still). No ArcRibbon or GroundFollower in any Penguin prefab.

### Probed on this PC (TTO's 2026-11-04 bundles, `D:\12tails-video\tto_assets\2026-11-04`)
- All 28 prefabs are there, with the same nodes, components and EffectControl values as section 5 (office, 2026-11-09
  bundles): e.g. constellation_line 6 + 0.2, frostField_field 8 + 0.6, frostField_trail 0.75 + 0.6 followPosition. No
  followState anywhere.
- **TrailModule** (4 systems, all `mode` 0, `ratio` 1, `minVertexDistance` 0.2, `worldSpace` false in World systems,
  `inheritParticleColor` true, trail material `tto_Line_DoubleEdge1` (addsoft)):
  - constellation_star Meteor1 (local (-3, 12, 2.5)): one particle, life 0.6 s, 21.03 m/s, no shape (along the node's
    +z); trail life 0.35 x 0.6 = 0.21 s (about 4.4 m), width 0.5 x (1 -> 0), colour white -> (1, 0.85, 0.45) at 0.3 ->
    (0.72, 0.45, 1), alpha 1 -> 0.6 -> 0; `dieWithParticles` false (the streak runs out after the meteor lands).
  - constellation_giant Giant1 ((-6, 22, 5); 38.91 m/s, size 3.2, width 1.6 x (1 -> 0)) and Escort1 ((-4, 20, 7);
    34.78 m/s, life 0.62, width 0.4 x (1 -> 0), colour white -> (0.93, 0.85, 1) -> (0.72, 0.45, 1)).
  - constellation_giantImpact Five: 5 particles in a circle (r 0.1, turned 90 deg about x), 9 m/s, life 0.6, trail
    life 0.25 x 0.6 = 0.15 s, width 0.5 x the particle's size (`sizeAffectsWidth`), `dieWithParticles` true.
  - stopAction 0 on all four.
- **Mesh particles on the Quad**: emperorPenguin_launch Ring1-3 and emperorPenguin_goal Net / Net2, `m_RenderMode` 4,
  `m_RenderAlignment` 2 (local), rotation3D, no texture sheet; material `tto_penguinRow6_rune`.
- **The cel material** `tto_SmallIcePenguin`: `_MainTex` IcePenguin1, no `_NormalTex` and no `_EmmisTex` (their
  defaults `bump` and `black`, from the shader's property info), `_RampLevels` 2, `_LightScalar` 1, `_HighIntensity`
  1.5, `_LowIntensity` 1, white `_Color` / `_HighColor` / `_LowColor`, `_FresnelBrightness` 0, `_RimAlpha` 0,
  `_SceneLighting` 1, no shader keywords.
- **The cel shader** (`FlexibleCelShader/Cel No Outline`, 88 programs; Queue Geometry, Opaque; passes FORWARD Blend One
  Zero, FORWARD_DELTA One One, a shadow caster). Its FORWARD fragment program (DIRECTIONAL LIGHTPROBE_SH,
  `dxbc_cel.txt` program 33), with the $Globals layout from the parsed form: band = round(sat(N.L x _LightScalar) x
  levels) / levels, levels = max(round(_RampLevels) - 1, 1); scene = 1 + _SceneLighting (1 - _TTOCelSceneLightCut)
  (min((_LightColor0 band + SH) / (0.65 band + 0.42), 1.8) - 1) per channel (**TTO's own light normalisation**: the
  0.65 / 0.42 / 1.8 constants and `_TTOCelSceneLightCut` are not in the asset store shader); colour = _MainTex x _Color
  x lerp(_LowColor x _LowIntensity, _HighColor x _HighIntensity, band) x 0.5 x scene, + fresnel and rim terms (0 here),
  then blended to _EmmisTex by its brightest channel (black here). So the penguins are the texture x 0.75 lit, x 0.5
  unlit, opaque.

### Corrections and new facts (code cites are `pseudo/Penguin.c`)
1. **`side` in EmperorShot is the hero's right.** `side = normalize(Cross(up, dir))` (`:417-426`), so the flock's
   ring offset is (up sin th + right cos th) x 0.65; the poofs' x signs in 2.3 hold (the Verification's unresolved
   "sign of side"). The node run lands penguin 0 at (0.295, 0.929, 20.70) and penguin 3 at (0.102, -0.292, 17.76) on
   the Goal frame at 120 fps (2.3: (0.282, 0.936, 20.77), (0.116, -0.29, 17.83): the last frame before d >= 22).
2. **The ball's spin** is `Transform.Rotate(side, deltaTime x 900)` in Space.Self (`:563-578`); the ball is spawned
   with identity (`EmperorSpawn` with `Quaternion.identity`, `:8923-8929`), so its own side axis stays the world's.
3. **The ball's height while rolling** is the ground under it + 0.45: a 5 m ray down from ballPos + 2 up (`:466-479`),
   so it jumps from ballAt's 0.2 m to 0.45 m on the shot's first frame (0.85 s). `to`'s y is not read.
4. **The ball between 0.8 and 0.85 s**: state 4's drop loop runs only while now < start + 0.8 (`:9013-9055`), so the
   game holds the last drop frame (less than one frame above ballAt); the page holds it at ballAt (APPROX).
5. **FlockRise** (`:1076-1100`): s = 4 (now - t0) while now < t0 + 0.25, h = (1 - (1 - s)^2) x 0.7 + 0.15 sin(s pi)
   (0.7 = DAT_182f3ff88, 0.15 = DAT_183004e94); after it, from + 0.7 axis exactly (`:1129-1160`). The flock turns only
   on frames it moves (`|step|^2 > DAT_182f3ff60`, `:664`; the epsilon's value not read: 1e-8 on the page).
6. **StarLines draws each line's LineRenderers through `lines[i]`, every LineRenderer under the line** (`:22622-22703`),
   and x 2.2 is applied to each of them at the ignite (`:22812-22834`). The line's start point is `fixedAt[i] + up`,
   refreshed each frame until the star falls (`:22580-22621`).
7. **cueOf drops `ignite`, `i` and `n`** (index.html `cueOf`): the parts work without them (`ignite` = kill - 0.6:
   ClearStarFx always comes 0.6 s after the ignite, `:22936`, `:22966`; `i` from the spot's angle a = atan2(x, d) of
   the FlockSpot, i = round((a + 75) / 150 x (n - 1)); `n` = 5); passing them through is a shared change (below), so a
   +3 flock (n = 8) can be cued later.
8. **The lines are cued at their draw start** (0.4 + 0.12 i, as 2.1 variant B): the part draws them out over 0.12 s
   from the cue. The game spawns all five at 0.4 hidden, so the look is the same.
9. **The gamma convention**: the cel shader's arithmetic is taken on gamma values (as every TTO shader here,
   tto_sheep.js): the colour factor is made linear before it multiplies the texture. If TTO renders in linear space
   the penguins would be brighter (x 0.75 linear instead of x 0.52); to check by eye.

### The cue entries (ready to paste into `wardrobe/fx_cues/penguin.json`)
Sections 2.1 (variant B), 2.2 and 2.3 as written, parsed and checked by `cues.py` (every `tto/` effect is in fx.json;
the two TTO sounds are in sfx/); only the `why`s gain their parts. The five lineFire cues' `scale` `[1, 1, 3.527]`
need P5 (index.html now multiplies the root's scale by an array). The `kind "sound"`
cues `emperorPenguin_whistle` / `emperorPenguin_flock` play TTO's own clips (written by this build); `wardrobe_fx.py
penguin` will report them as missing from the rip (harmless: it never deletes sfx files).

```json
{
  "constellation": {
    "why": "TTO1102:Penguin.<RPC_constellation>d__340::MoveNext@0x1DE7560 (Penguin.c:6783-7032) + <StarLines>d__341::MoveNext@0x1E2C220 (:22423-23060) (plans/fx_penguin/tto.md 2.1, variant B: the target 10 m ahead and 4 foes, a pentagon R 3 m about 13 m ahead, checks/fx_penguin_research/tto/calc.py): 0: Row6Begin, Row6Sound fallingStar_ring (:6856), constellation_cast owned (:6871); Until 0.4: a constellation_mark 1 m over each star spot (StarAt + up, :6902-6924; it follows its foe until the fall, :22580-22621), Row6Sound castEffect (:6943), 5 lines (StarLineCount@0x1DB1320: n >= 3 = a closed ring), line i from mark i to mark i+1 drawn over 0.12 s from 0.4 + 0.12 i (:22659-22703; cued at its draw start, the game's are hidden until then), widthMultiplier x 2.2 at the ignite (:22833-22834, capstone 0x1E2CE9A); Until 1: Row6End (:7022); star i (sky order, InSkyOrder@0x1DA7F90: ascending atan2(dx, dz), target last) falls at 1.1 + 0.3 i (:22715-22736) and lands 0.6 s later: its mark destroyed, constellation_impact at the spot (StarImpact@0x1DB1000, :22759-22770); ignite at lastImpact + 0.05 = 1.1 + 0.6 + 0.3 x 4 + 0.05 = 2.95 (:22537, :22790): constellation_lineFire at each segment's midpoint, LookRotation(segment), localScale (1, 1, 3.527) (:22884-22904), constellation_ignite at the middle (StarGround of the spots' mean, :22809) + Row6Sound manaArc (:22921-22923), constellation_giant at the middle + Row6Sound fallingComet (:22953-22954); 2.95 + 0.6 = 3.55: ClearStarFx (the lines go: kill), constellation_giantImpact at the middle + Row6Sound novarFlare (:22966-22981); left out: the hits and the manaFracture look on hit foes (AddPenguinRow6Fx@0x24ADC20: on an enemy) Parts (2026-11-10): the lines' StarLines mover (wardrobe/fxparts/tto_penguin.js Penguin.StarLines: `to` = the next mark, `ignite` = the widening, else kill - 0.6), the meteors' TrailModule (shuriken.js), lineFire's `scale` [1, 1, length] (index.html, P5).",
    "cues": [
    [0, "sound", "fallingStar_ring"],
    [0, "fx", "tto/constellation_cast"],
    [0.4, "fx", "tto/constellation_mark", {"x": -2.853, "y": 1, "d": 12.073, "kill": 1.3}],
    [0.4, "fx", "tto/constellation_mark", {"x": -1.763, "y": 1, "d": 15.427, "kill": 1.6}],
    [0.4, "fx", "tto/constellation_mark", {"x": 1.763, "y": 1, "d": 15.427, "kill": 1.9}],
    [0.4, "fx", "tto/constellation_mark", {"x": 2.853, "y": 1, "d": 12.073, "kill": 2.2}],
    [0.4, "fx", "tto/constellation_mark", {"y": 1, "d": 10, "kill": 2.5}],
    [0.4, "sound", "castEffect"],
    [0.4, "fx", "tto/constellation_line", {"x": -2.853, "y": 1, "d": 12.073, "to": [-1.763, 1, 15.427], "ignite": 2.55, "kill": 3.15}],
    [0.52, "fx", "tto/constellation_line", {"x": -1.763, "y": 1, "d": 15.427, "to": [1.763, 1, 15.427], "ignite": 2.43, "kill": 3.03}],
    [0.64, "fx", "tto/constellation_line", {"x": 1.763, "y": 1, "d": 15.427, "to": [2.853, 1, 12.073], "ignite": 2.31, "kill": 2.91}],
    [0.76, "fx", "tto/constellation_line", {"x": 2.853, "y": 1, "d": 12.073, "to": [0, 1, 10], "ignite": 2.19, "kill": 2.79}],
    [0.88, "fx", "tto/constellation_line", {"y": 1, "d": 10, "to": [-2.853, 1, 12.073], "ignite": 2.07, "kill": 2.67}],
    [1.1, "fx", "tto/constellation_star", {"x": -2.853, "d": 12.073}],
    [1.4, "fx", "tto/constellation_star", {"x": -1.763, "d": 15.427}],
    [1.7, "fx", "tto/constellation_impact", {"x": -2.853, "d": 12.073}],
    [1.7, "fx", "tto/constellation_star", {"x": 1.763, "d": 15.427}],
    [2.0, "fx", "tto/constellation_impact", {"x": -1.763, "d": 15.427}],
    [2.0, "fx", "tto/constellation_star", {"x": 2.853, "d": 12.073}],
    [2.3, "fx", "tto/constellation_impact", {"x": 1.763, "d": 15.427}],
    [2.3, "fx", "tto/constellation_star", {"d": 10}],
    [2.6, "fx", "tto/constellation_impact", {"x": 2.853, "d": 12.073}],
    [2.9, "fx", "tto/constellation_impact", {"d": 10}],
    [2.95, "fx", "tto/constellation_lineFire", {"x": -2.308, "y": 1, "d": 13.75, "rot": [0, 18, 0], "scale": [1, 1, 3.527]}],
    [2.95, "fx", "tto/constellation_lineFire", {"y": 1, "d": 15.427, "rot": [0, 90, 0], "scale": [1, 1, 3.527]}],
    [2.95, "fx", "tto/constellation_lineFire", {"x": 2.308, "y": 1, "d": 13.75, "rot": [0, 162, 0], "scale": [1, 1, 3.527]}],
    [2.95, "fx", "tto/constellation_lineFire", {"x": 1.427, "y": 1, "d": 11.036, "rot": [0, -126, 0], "scale": [1, 1, 3.527]}],
    [2.95, "fx", "tto/constellation_lineFire", {"x": -1.427, "y": 1, "d": 11.036, "rot": [0, -54, 0], "scale": [1, 1, 3.527]}],
    [2.95, "fx", "tto/constellation_ignite", {"d": 13}],
    [2.95, "sound", "manaArc"],
    [2.95, "fx", "tto/constellation_giant", {"d": 13}],
    [2.95, "sound", "fallingComet"],
    [3.55, "fx", "tto/constellation_giantImpact", {"d": 13}],
    [3.55, "sound", "novarFlare"]
    ]
  },
  "frostFieldLeap": {
    "why": "TTO1102:Penguin.<RPC_frostFieldLeap>d__349::MoveNext@0x1DEF770 (Penguin.c:11314-11556; plans/fx_penguin/tto.md 2.2): 0: Row6Begin (:11384), Row6Sound blink (sounds/, :11395); Until 0.2: frostField_leap at the takeoff spot, hero rotation (:11423), frostField_trail owned at the hero (:11438; EffectControl 0.75 + 0.6, followPosition), the 0.6 s leap (:11441-11485: lerp to the landing + up x 10u(1-u), 2.5 m peak; FieldLanding@0x1DA4590: 1.5 m short of the target, 8.5 m for the target 10 m ahead) - the page's hero doesn't travel, so the landing is at 0 (Feral Strike's convention, plans/fx_wolf/misc.md item 4); 0.8: frostField_land at the landing, hero rotation (:11523), Row6Sound iceBreak (:11525), FrostFieldLoop@0x1DC38F0 (:1268-1450): frostField_field at the centre, identity (:1324; EffectControl 8 + 0.6 ends it before the code's Destroy 9, :1335), Row6Sound blizzard (:1337); ticks 1 s apart from the landing (:1345-1393), one Frost Mark each on the target 1.5 m past the landing (within 9 m, :1376; AddFrostMarks@0x1DA2E60 :1432): the 5th, at 0.8 + 4 = 4.8 s, sets off FrostBurst (:38311) = BurstFx@0x1DA3310 (:38592-38640): frostField_burst at the foe's feet, identity, + Row6Sound frozenBlast (sounds/), cued at the target 1.5 m ahead (the target point, moved with the landing to the hero); Until 1.1: Row6End (:11545); the cues after 1.1 s run on in the idle tail; no voice, no Multi Cast roll; left out: the frostMarkFx / frostBiteFx / frozenGround / 20 % freeze looks on the foe (status looks on its body, Sheep decision 4); the Penguin's own frostField buff has no look (AddPenguinRow6Fx@0x24ADC20 serves frostMark, frostBite, manaFracture only) Parts: none new (decision 8: in place).",
    "cues": [
    [0, "sound", "blink"],
    [0.2, "fx", "tto/frostField_leap"],
    [0.2, "fx", "tto/frostField_trail"],
    [0.8, "fx", "tto/frostField_land"],
    [0.8, "sound", "iceBreak"],
    [0.8, "fx", "tto/frostField_field"],
    [0.8, "sound", "blizzard"],
    [4.8, "fx", "tto/frostField_burst", {"d": 1.5}],
    [4.8, "sound", "frozenBlast"]
    ]
  },
  "emperorPenguin": {
    "why": "TTO1102:Penguin.<RPC_emperorPenguin>d__356::MoveNext@0x1DEA490 (Penguin.c:8457-9102; plans/fx_penguin/tto.md 2.3; 5 penguins, no Focus, the ball's full 22 m: checks/fx_penguin_research/tto/calc.py): 0: Row6Begin (:8628), Until(start + 0) (:8645), then emperorPenguin_whistle at Row6Beak@0x1DAF620 = Head + 0.16 fwd - 0.03 up (0.17 ahead, 0.04 right, 0.64 up on the page's rig) with the hero's rotation, emperorPenguin_summon at the hero, Row6Sound emperorPenguin_whistle (TTO's own sounds/ clip, :8656-8695); Until 0.3: emperorPenguin_crack 1.75 m ahead (:8720-8743; its own sounds/iceBlock 0.8) + Row6Sound iceBlock (:8744), per penguin i of 5 emperorPenguin_emerge at FlockSpot@0x1DA4BF0 (angle (150 i/4 - 75) deg, r 1.25, capstone 0x1DA4D4F-0x1DA4DDD) and emperorPenguin_penguin 0.7 m down the 45 deg tilt axis from it, turned LookRotation(dir) x Euler(45, 0, 0) (:8766-8829), rising along it for 0.25 s (FlockRise@0x1DC31F0, :986-1167); Until 0.55: emperorPenguin_ball 0.45 ahead, 1.0 up, dropped to 0.2 m by 0.8 (:8892-9055); 0.8: emperorPenguin_kick at Row6Foot@0x1DB0160 = Foot2_R (0.10 ahead, 0.19 right, 0.17 up), emperorPenguin_launch at the ball (0.45 ahead, 0.2 up), Row6Sound cAttack (:8963-9008); Until 0.85: Row6Sound emperorPenguin_flock (TTO's own), EmperorShot@0x1DC1520 (:103-969): the ball rolls 28 m/s to 22 m at ground + 0.45, spinning 900 deg/s, an emperorPenguin_frost on the ground every 1.6 m from 1.2 m (float32: 13, the last 20.85 m ahead, :428-552), the flock whirls round the lane (0.65 m, 540 deg/s, 0.06 + 0.035 i behind, :588-682); Until 1.6: Row6End (:9090); 0.85 + 22/28 = 1.636: GoalFx@0x1DA74E0 emperorPenguin_goal at the ball 22.45 m ahead, 0.45 up + Row6Sound absoluteZero (:852), Destroy(ball) (kill 1.086), Scatter@0x1DB09F0 emperorPenguin_poof at each penguin, then Destroy (kill 1.336) (:842-844); no voice, no Multi Cast roll; the ball passes the 10 m target at 0.85 + (10 - 0.95)/28 = 1.173 s (lane test :790-791): AddFrostMarks(foe, 5) (:811) = an instant Frost Burst (:38311), BurstFx@0x1DA3310 (:38592-38640): frostField_burst at the foe's feet, identity, + Row6Sound frozenBlast (sounds/), at the target point 10 m ahead; the cues after 1.6 s run on in the idle tail; left out: the frostMarkFx / frostBiteFx looks on the foe (status looks on its body, Sheep decision 4; the hits draw nothing); constellation_impact 1.2 m ahead only with Constellation's +3 penguins (:8846-8862) Parts (2026-11-10): Penguin.EmperorShot (the ball's drop and roll, `to` = the Goal) and Penguin.FlockRise (the rise and whirl; `i` the index, else read from the spot; `n` 5) in wardrobe/fxparts/tto_penguin.js, the flock's skinned SmallIcePenguin_tri (mesh.js) with FlexibleCelShader/Cel No Outline (tto_penguin.js), the launch / goal rings on Unity's built-in Quad (shuriken.js), TTO's own sounds emperorPenguin_whistle / emperorPenguin_flock (sfx/, wardrobe_fx_tto.py SKILL_SOUNDS).",
    "cues": [
    [0, "fx", "tto/emperorPenguin_whistle", {"d": 0.17, "x": 0.04, "y": 0.64}],
    [0, "fx", "tto/emperorPenguin_summon"],
    [0, "sound", "emperorPenguin_whistle"],
    [0.3, "fx", "tto/emperorPenguin_crack", {"d": 1.75}],
    [0.3, "sound", "iceBlock"],
    [0.3, "fx", "tto/emperorPenguin_emerge", {"x": -1.207, "d": 0.324}],
    [0.3, "fx", "tto/emperorPenguin_emerge", {"x": -0.761, "d": 0.992}],
    [0.3, "fx", "tto/emperorPenguin_emerge", {"d": 1.25}],
    [0.3, "fx", "tto/emperorPenguin_emerge", {"x": 0.761, "d": 0.992}],
    [0.3, "fx", "tto/emperorPenguin_emerge", {"x": 1.207, "d": 0.324}],
    [0.3, "fx", "tto/emperorPenguin_penguin", {"x": -1.207, "y": -0.495, "d": -0.171, "rot": [45, 0, 0], "i": 0, "to": [0, 0.45, 22.45], "kill": 1.336}],
    [0.3, "fx", "tto/emperorPenguin_penguin", {"x": -0.761, "y": -0.495, "d": 0.497, "rot": [45, 0, 0], "i": 1, "to": [0, 0.45, 22.45], "kill": 1.336}],
    [0.3, "fx", "tto/emperorPenguin_penguin", {"y": -0.495, "d": 0.755, "rot": [45, 0, 0], "i": 2, "to": [0, 0.45, 22.45], "kill": 1.336}],
    [0.3, "fx", "tto/emperorPenguin_penguin", {"x": 0.761, "y": -0.495, "d": 0.497, "rot": [45, 0, 0], "i": 3, "to": [0, 0.45, 22.45], "kill": 1.336}],
    [0.3, "fx", "tto/emperorPenguin_penguin", {"x": 1.207, "y": -0.495, "d": -0.171, "rot": [45, 0, 0], "i": 4, "to": [0, 0.45, 22.45], "kill": 1.336}],
    [0.55, "fx", "tto/emperorPenguin_ball", {"d": 0.45, "y": 1.0, "to": [0, 0.45, 22.45], "kill": 1.086}],
    [0.8, "fx", "tto/emperorPenguin_kick", {"d": 0.1, "x": 0.19, "y": 0.17}],
    [0.8, "fx", "tto/emperorPenguin_launch", {"d": 0.45, "y": 0.2}],
    [0.8, "sound", "cAttack"],
    [0.85, "sound", "emperorPenguin_flock"],
    [0.893, "fx", "tto/emperorPenguin_frost", {"d": 1.65}],
    [0.95, "fx", "tto/emperorPenguin_frost", {"d": 3.25}],
    [1.007, "fx", "tto/emperorPenguin_frost", {"d": 4.85}],
    [1.064, "fx", "tto/emperorPenguin_frost", {"d": 6.45}],
    [1.121, "fx", "tto/emperorPenguin_frost", {"d": 8.05}],
    [1.173, "fx", "tto/frostField_burst", {"d": 10}],
    [1.173, "sound", "frozenBlast"],
    [1.179, "fx", "tto/emperorPenguin_frost", {"d": 9.65}],
    [1.236, "fx", "tto/emperorPenguin_frost", {"d": 11.25}],
    [1.293, "fx", "tto/emperorPenguin_frost", {"d": 12.85}],
    [1.35, "fx", "tto/emperorPenguin_frost", {"d": 14.45}],
    [1.407, "fx", "tto/emperorPenguin_frost", {"d": 16.05}],
    [1.464, "fx", "tto/emperorPenguin_frost", {"d": 17.65}],
    [1.521, "fx", "tto/emperorPenguin_frost", {"d": 19.25}],
    [1.579, "fx", "tto/emperorPenguin_frost", {"d": 20.85}],
    [1.636, "fx", "tto/emperorPenguin_goal", {"d": 22.45, "y": 0.45}],
    [1.636, "sound", "absoluteZero"],
    [1.636, "fx", "tto/emperorPenguin_poof", {"x": 0.282, "y": 0.936, "d": 20.77}],
    [1.636, "fx", "tto/emperorPenguin_poof", {"x": -0.47, "y": 0.799, "d": 19.79}],
    [1.636, "fx", "tto/emperorPenguin_poof", {"x": -0.572, "y": 0.042, "d": 18.81}],
    [1.636, "fx", "tto/emperorPenguin_poof", {"x": 0.116, "y": -0.29, "d": 17.83}],
    [1.636, "fx", "tto/emperorPenguin_poof", {"x": 0.644, "y": 0.263, "d": 16.85}]
    ]
  }
}
```

### Shared changes asked (files I do not own; all three already in index.html when this was written: FX_PART_FILES
has "tto_penguin", cueOf keeps every option (`...o`), the root's `scale` takes an array)
- `wardrobe/index.html` `FX_PART_FILES`: add `"tto_penguin"` after `"tto_sheep"` (it reads `api.curves`, which
  shuriken.js sets).
- `wardrobe/index.html` `cueOf`: pass `ignite: o.ignite, i: o.i, n: o.n` through (optional, see 7).
- `wardrobe/index.html` (P5): `scale` as `[x, y, z]` at the root (`o.scale.fromArray(n.scale || [1, 1, 1])` then
  multiply by the vector, or by the number as now).

### Left for a browser check (QA)
- The cel penguins' look (the light band at N.L 0.5 under the page's sun; brightness: item 9), their facing as they
  whirl (belly-down, LookRotation(motion) x Euler(80, 0, 0)), the staff collapsed (its bone scale 0).
- The meteor streaks' width and colour; the launch rings and the goal nets (mesh particles on the Quad, local
  alignment).
- Emperor's March runs past its clip (the Goal at 1.636 s, the clip 1.6 s): with the loop toggle on the Goal never
  shows (2.3 "Read this first" 9).
