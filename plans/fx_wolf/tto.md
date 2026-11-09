# Wolf effects research: the three TTO Lv 100 skills (Blade Surge, Resonance Claw, Wind Bound Domain)

Researcher's report for the Wolf cue file (`wardrobe/fx_cues/wolf.json`) and for the lead (code). Read-only. Sources:
TTO's pseudo-C `D:\12tails\DecompiledSource_TTO_2026-11-02\pseudo\Wolf.c` and `CharacterControl.c` (cited Bible-style as
`TTO1102:Method@RVA`, never by line), the instructions where Ghidra dropped a float (capstone over `client\GameAssembly.dll`,
`checks\fx_wolf_research\tto\dis.py`), the Bible (`12t_reference\wolf-skill-reference.md`, "TTO Lv 100 skills"), the TTO rip
(`D:\12tails\RippedAssets_TTO_2026-11-04\ExportedProject\Assets\`), and TTO's decrypted bundles that the video repo already
holds (`D:\12tails-video\tto_assets\2026-11-04\dec` + `catalog.bin`, read with UnityPy). Every probe script is in
`D:\12tails-wardrobe\checks\fx_wolf_research\tto\` (scan.py, fields.py, ps.py, mats.py, where.py, ogg_len.py, dis.py,
ub_probe2.py, ub_colors.py, ub_audio.py; outputs scan_main.txt, scan_0.txt, fields_default.txt, rc_movenext.asm,
guids.json). Nothing else was written. All three skills have one rank, so "max rank" changes nothing.

## 0. Two findings to read first

1. **Every prefab exists twice in TTO: the default and the Ronin arcana style.** The game loads
   `GameAssets/characters/heroes/wolf/effects/<name>` through `BaseHero::ArcanaLoad` (`TTO1102:Wolf::Row6Spawn@0x1F0F050`,
   `Wolf::Row6Prefab@0x1F0EEA0`), and the catalog has a second copy of each under
   `.../wolf/arcana/ronin/effects/<name>` (and `arcana/ronin/sounds/`), used while the Wolf wears the Ronin arcana armour
   (`ArcanaRegistry::Resolve` / `StyleOf(armorCode)`). AssetRipper flattened both into the rip's Assets root as `X.prefab`
   and `X_0.prefab`, and which one got `_0` is arbitrary. Settled from the bundles (`ub_colors.py`: the catalog's internal
   id -> the bundle's own `m_Container` -> the prefab): **default = blue / white (Blade Surge), violet / gold / white
   (Resonance Claw), mint green (Wind Bound Domain); Ronin = crimson in every prefab.** Default files in the rip:

   | Effect | Default (use this) | Ronin |
   |---|---|---|
   | bladeSurge_aura | `bladeSurge_aura.prefab` | `_0` |
   | bladeSurge_zone | `bladeSurge_zone_0.prefab` | plain |
   | bladeSurge_cut | `bladeSurge_cut.prefab` | `_0` |
   | bladeSurge_flicker | `bladeSurge_flicker.prefab` | `_0` |
   | bladeSurge_sheathe | `bladeSurge_sheathe_0.prefab` | plain |
   | bladeSurge_shatter | `bladeSurge_shatter_0.prefab` | plain |
   | bladeSurge_shards | `bladeSurge_shards.prefab` | `_0` |
   | resonanceClaw_charge | `resonanceClaw_charge.prefab` | `_0` |
   | resonanceClaw_rake | `resonanceClaw_rake_0.prefab` | plain |
   | resonanceClaw_wave_twin | `resonanceClaw_wave_twin_0.prefab` | plain |
   | resonanceClaw_wave_light | `resonanceClaw_wave_light.prefab` | `_0` |
   | resonanceClaw_wave_dark | `resonanceClaw_wave_dark_0.prefab` | plain |
   | resonanceClaw_burst (on a target, not cued) | `resonanceClaw_burst_0.prefab` | plain |
   | windBoundDomain_cast | `windBoundDomain_cast.prefab` | `_0` |
   | windBoundDomain_plant | `windBoundDomain_plant_0.prefab` | plain |
   | windBoundDomain_domain | `windBoundDomain_domain_0.prefab` | plain |
   | windBoundDomain_pulse | `windBoundDomain_pulse.prefab` (no Ronin copy) | - |
   | windBound (enemy status, not cued) | `windBound_0.prefab` | plain |

   The default prefabs also all reference the un-suffixed materials (`wolfRow6_cutline.mat`, `Line_vertMultilines2.mat`,
   ...), the Ronin ones the `_<hash>` copies; the Ronin wave prefabs are also built differently (3 ribbons, crescent at
   y 2.36) from the default ones (6 ribbons incl. a Foot set, crescent at y 3.47).
2. **TTO's rip keeps every setting, and TTO's bundles read with full type trees**, unlike BB. But most of these effects are
   drawn by three scripts TTO added (`GroundHugEmitter`, `ArcRibbonEmitter`, `GroundFollower`) and by Unity's Shuriken
   `ParticleSystem`, none of which the page draws today, and none of whose code is decompiled yet (section 4).

## 1. Shared machinery (all three skills)

- Entry: `TTO1102:Wolf::DoRow6Skill@0x1F09850` -> the coroutine. `Wolf::Row6Begin@0x1F0E8D0` (command, mPos, tDir, clip,
  wrap) sets actionState `attack`, puts the hero at mPos facing flat tDir (`LookAt`), `PlayAnimation(clip, 0.1)` with
  WrapMode 1 (Once). The clip has the skill's own name: `bladeSurge` (2.6 s), `resonanceClaw` (1.6 s), `windBoundDomain`
  (1.7 s), already in `wardrobe/data/wolf/clips.json` (`tto: true`). `Wolf::Row6End@0x1F0ECF0` -> `standby` (this is the
  "action changes" moment for a followState effect).
- `Wolf::Row6Spawn(name, pos, rot, owned)@0x1F0F050`: `owned` true -> `CharacterControl::createEffect@0x24CFBC0`
  (Instantiate + hands the hero to the prefab's EffectControl, so followPosition / followState work); false -> a bare
  `Object.Instantiate` (world-placed; EffectControl gets no owner). Noted per effect below.
- No voice: none of the three coroutines (nor DoRow6Skill, nor `Wolf::OnRow6ActionEvent@0x1F0A430`, the other clients'
  replay) plays a voice. The sounds are the prefabs' own AudioSources (play on awake) plus Blade Surge's per-cut
  `PlayOneShot` (`Wolf::Row6Clip@0x1F0EAA0`, on the hero's `_audio`).
- Camera-only extras (owner only; the page has no camera effects, listed so the lead can decide): `AddCamereShake`
  0.35 / 0.6 (Blade Surge 1.2 / 2.1 s), 0.5 (Resonance Claw 0.62 s), 0.4 (Wind Bound Domain 0.8 s); `whiteRamp` flash and
  `speedMask` motion blur at Blade Surge 2.1 s and Resonance Claw 0.62 s; Blade Surge's `lunarRamp` colour grade from 0.3 s
  to 2.1 s, fading out over 0.3 s (`Wolf::BladeSurgeGrade@0x1F085A0`).

## 2. Per skill: timeline and proposed cues

Times are seconds after the clip starts (= the coroutine start). Unity space, hero frame (+z forward, +y up). "World" =
plain Instantiate at that spot. The cue format today is `[t, "fx"|"voice", "name or a|b", distance?, actionChangeTime?]`;
what it cannot say (height, roll, yaw, scale, a kill time, a random scatter) is marked **needs** and gathered in 2.4.

### 2.1 Blade Surge (`bladeSurge`, 2.6 s)

Coroutine `TTO1102:Wolf.<RPC_bladeSurge>d__317::MoveNext@0x1F1F640` (Bible timeline: 0 / 0.30-1.05 cuts / 1.20 slam /
2.10 strike / 2.60 end; each wait is the time left to its mark).

- **0.00** `bladeSurge_aura`, owned, at the hero, hero rotation. EffectControl life 11, afterLife 0.2,
  followPosition 1, **followState 1** -> ends at Row6End (2.6). Sound `bladeSong_ring` (vol 1). 3 GroundHug bands.
- **0.30** `bladeSurge_zone`, world, at `hero + 1.2 up` (`Wolf::BladeSurgeZone@0x1F097A0`), hero rotation. Life 13, but
  destroyed outright at 2.10 by `Wolf::BladeSurgeClearFx@0x1F07620` (no after-life). Shade (alpha fill) + Dome (14.7 m
  camera-facing ImageEmitters, repeatForever), a 7 m GroundHug ring, Shuriken "Glints" (40/s).
- **Cuts k = 0..5 at 0.30 + 0.15 k** (0.30, 0.45, 0.60, 0.75, 0.90, 1.05) and **the slam (k = 6) at 1.20**, each
  `Wolf::BladeSurgeCut(k, slam)@0x1F07840`:
  - `bladeSurge_flicker`, world, at `hero + 1.0 up + 0.6 forward`, rotation `heroRot * AngleAxis(roll, forward)`,
    roll = `Wolf.BladeSurgeFlickerRoll[k % 4]` = `[0, -70, 180, 90]` (`Wolf::.cctor@0x1F0F9B0`): rolls 0, -70, 180, 90,
    0, -70, slam 180. The slam's flicker is scaled 2.2. Life 0.15.
  - Sound `GameAssets/characters/heroes/wolf/sounds/bladeFang{k % 3 + 1}`, PlayOneShot vol 1: bladeFang1, 2, 3, 1, 2, 3,
    slam 1. (Default clips are BB's own: 0.484 s each, `ub_audio.py`.)
  - Six `bladeSurge_cut` "lines" (`Wolf::BladeSurgeLine@0x1F08A60`, called 6 times), world, **random**: v = insideUnitSphere,
    v.y x 0.45; if |v.xz| < 0.25 push v.xz out by 0.3 along itself (forward if ~0); pos = `hero + 1.2 up + v x 6.3`
    (6.3 = 7 x rangeMod x 0.9, rangeMod 1), y clamped to >= hero + 0.3; rotation `AngleAxis(Random 0..360, up) *
    FromToRotation(up, normalize(onUnitSphere with y x 0.6))`; uniform scale Random 0.6..1.4. They stay (life 14) until
    ClearFx at 2.10. 6 x 7 = 42 lines.
  - Slam only: two more `bladeSurge_cut` at `hero + 1.3 up + 3 forward`, rotation `heroRot * AngleAxis(+45 / -45,
    forward)`, scale 1.6 (also kept until 2.10): 44 lines in all (the cap of 90 is never reached).
  - The hits, `RPC_bladeSong_hit` and the paralysis are on targets: left out.
- **2.10** (`Wolf::BladeSurgeShatter@0x1F09240`, then ClearFx):
  - `bladeSurge_sheathe`, owned, at the hero (followPosition 1, life 0.5). Sound `artCancel2` (BB's, 0.226 s).
  - `bladeSurge_shatter`, world, at `hero + 1.2 up`, hero rotation. Sound `shatteringDream_hit` (BB has it under
    `bat/sounds/`). 18 m dome flash, 9.8 m ground ring, Shuriken glass (160) + sparks (90).
  - `bladeSurge_shards` once per **world** quadrant (signs of line.x - centre.x and line.z - centre.z) that holds more than
    3 lines, at the mean position of that quadrant's lines, hero rotation. With 44 lines a quadrant has <= 3 only 0.2% of
    the time, so effectively always 4 shards; Monte Carlo of the code's distribution: means at about
    **(+-2.47, 1.39, +-2.47)** m from the hero (each jitters by about a metre). Sound `iceBreak` vol 0.8 each (BB has it
    under `penguin/sounds/`), so 4 overlapping.
  - Then every line and the zone are destroyed. The judgment strike and `RPC_bladeSurgeJudge` (which spawns
    `bladeSurge_shards` / `bladeSurge_cut` at far targets) are on targets: left out.
- **2.60** Row6End -> the aura's after-life.

Proposed cues (strict format first; the needs list says what is lost):

```json
"bladeSurge": {
  "why": "TTO1102:Wolf.<RPC_bladeSurge>d__317::MoveNext@0x1F1F640 (default style, not arcana/ronin): aura owned at 0 (followState, Row6End 2.6); zone 1.2 m up at 0.3 (BladeSurgeZone@0x1F097A0), destroyed 2.1 (BladeSurgeClearFx@0x1F07620); cuts 0.30+0.15k and slam 1.20 (BladeSurgeCut@0x1F07840): flicker 1 m up 0.6 m ahead rolled BladeSurgeFlickerRoll[k%4] = 0/-70/180/90 (Wolf::.cctor@0x1F0F9B0, slam x2.2), bladeFang(k%3+1), 6 random bladeSurge_cut lines each (BladeSurgeLine@0x1F08A60), slam + 2 cuts 1.3 m up 3 m ahead rolled +-45 x1.6; 2.1 sheathe owned, shatter 1.2 m up, 4 shards at the line quadrants' means (BladeSurgeShatter@0x1F09240)",
  "cues": [
  [0, "fx", "bladeSurge_aura", 0, 2.6],
  [0.3, "fx", "bladeSurge_zone"],
  [0.3, "fx", "bladeSurge_flicker", 0.6],  [0.3, "voice", "bladeFang1"],
  [0.45, "fx", "bladeSurge_flicker", 0.6], [0.45, "voice", "bladeFang2"],
  [0.6, "fx", "bladeSurge_flicker", 0.6],  [0.6, "voice", "bladeFang3"],
  [0.75, "fx", "bladeSurge_flicker", 0.6], [0.75, "voice", "bladeFang1"],
  [0.9, "fx", "bladeSurge_flicker", 0.6],  [0.9, "voice", "bladeFang2"],
  [1.05, "fx", "bladeSurge_flicker", 0.6], [1.05, "voice", "bladeFang3"],
  [1.2, "fx", "bladeSurge_flicker", 0.6],  [1.2, "voice", "bladeFang1"],
  [1.2, "fx", "bladeSurge_cut", 3], [1.2, "fx", "bladeSurge_cut", 3],
  [2.1, "fx", "bladeSurge_sheathe"],
  [2.1, "fx", "bladeSurge_shatter"],
  [2.1, "fx", "bladeSurge_shards"], [2.1, "fx", "bladeSurge_shards"], [2.1, "fx", "bladeSurge_shards"], [2.1, "fx", "bladeSurge_shards"]
  ]
}
```

Needs (Blade Surge loses the most without them): zone / shatter at y 1.2 and killed at 2.1; flicker at y 1.0 with its roll
(0, -70, 180, 90, 0, -70, 180) and slam scale 2.2; the two slam cuts at y 1.3, roll +45 / -45, scale 1.6, killed at 2.1;
the 42 random lines (the skill's main look: a cage of glowing blade strokes that builds up and shatters), killed at 2.1;
the 4 shards at (+-2.47, 1.39, +-2.47). In the strict format the zone and the two cuts would stand for their full life
(13.3 s / 14 s), so they should not go in until the page has a kill time.

### 2.2 Resonance Claw (`resonanceClaw`, 1.6 s)

Coroutine `TTO1102:Wolf.<RPC_resonanceClaw>d__329::MoveNext@0x1F3C1E0` (waits read from the instructions: 0.62 at
0x1F3CBE3, 0.05 at 0x1F3CA7D, 0.93 at 0x1F3C689; yaws at 0x1F3C39C and 0x1F3C529, each matched to its spawn's string).

- **0.00** `resonanceClaw_charge`, owned, at the hero (followPosition 1, life 1.8, afterLife 0.6). Sound
  `twinResonance_ring` (BB's, 2.997 s). Two GroundHug bands.
- **0.62** origin and facing fixed. `resonanceClaw_rake`, world, at the hero, hero rotation (life 1, afterLife 0.2):
  three sweeping slash ribbons at 1.35 m (ArcRibbon "Comet"), a ground ring and rune 1.2 m ahead, a ray burst
  (Shuriken + ImageEmitter `grandCross_mark`) 1.2 m ahead, and three ground claw strips at yaw -45 / 0 / +45 that grow to
  38 m long, 8 -> 6.4 m wide, over 1.35 s (the three damage lanes). Sound `skySlasher` (BB's, 1.198 s).
- **0.62** `resonanceClaw_wave_twin`, world, at the hero, hero rotation: EffectControl velocity (0, 0, 36) (36 m/s
  forward, life 1 + 0.12, so it runs out to 36 m as the lane does), GroundFollower, 6 crescent ribbons, Shuriken sparks.
  Sound `cAttack4` vol 0.9 (BB's, 1.062 s).
- **0.67** `resonanceClaw_wave_light`, world, rotation `AngleAxis(-45, up) * heroRot` (Unity: toward the hero's left), and
  `resonanceClaw_wave_dark`, world, `AngleAxis(+45, up) * heroRot` (right). Same build as the twin, no sound.
- **1.60** Row6End. The waves run on by themselves.
- Left out: `ResonanceClawRun` (`<ResonanceClawRun>d__330::MoveNext@0x1F52000`) only hits; the burst ~2.02 s
  (`Wolf::RPC_resonanceBurst@0x1F0DB20`: `resonanceClaw_burst` at each hit target, scale 0.75 + 0.25 n, plus
  `twinResonance_hit` on the hero's AudioSource at most every 0.2 s) needs a target that was hit: on an enemy, so not cued.

```json
"resonanceClaw": {
  "why": "TTO1102:Wolf.<RPC_resonanceClaw>d__329::MoveNext@0x1F3C1E0 (default style): charge owned at 0; Waits 0.62 (0x1F3CBE3): rake and wave_twin (velocity 36 m/s forward) at the hero; Waits 0.05 (0x1F3CA7D): wave_light at AngleAxis(-45, up) (0x1F3C39C) and wave_dark at +45 (0x1F3C529); Waits 0.93 -> Row6End 1.6. The burst (RPC_resonanceBurst@0x1F0DB20) is on hit targets: left out",
  "cues": [
  [0, "fx", "resonanceClaw_charge"],
  [0.62, "fx", "resonanceClaw_rake"],
  [0.62, "fx", "resonanceClaw_wave_twin"],
  [0.67, "fx", "resonanceClaw_wave_light"],
  [0.67, "fx", "resonanceClaw_wave_dark"]
  ]
}
```

Needs: yaw -45 / +45 on the two side waves (without it all three waves overlap straight ahead). Nothing else; the hero
does not move during the clip, so world vs owned makes no difference on the page.

### 2.3 Wind Bound Domain (`windBoundDomain`, 1.7 s)

Coroutine `TTO1102:Wolf.<RPC_windBoundDomain>d__313::MoveNext@0x1F51890` (0.8 at 0x1F51F7C, 0.9 at 0x1F51D31) and
`<WindBoundHeals>d__315::MoveNext@0x1F52EC0` (2 at 0x1F52F84).

- **0.00** `windBoundDomain_cast`, owned, at `hero + 0.2 forward`, hero rotation (followPosition 1, life 1.2). Sound
  `secondWind` (BB's, 1.419 s). A GroundHug sigil disc, a band, a LineEmitter (12 streaks, 1.2 m up).
- **0.80** (only if the action was not cut short) `windBoundDomain_plant`, world, at `hero + 0.7 forward`, hero rotation
  (life 1.4; a 14.6 m shock ring). Sound `grandCross` (BB's, 1.337 s).
- **0.80** `windBoundDomain_domain`, world, at the hero, **identity rotation** (life 6, afterLife 0.5): a 15 m sigil disc,
  a 14.65 m wall band that emits Shuriken motes at 45/s, an inner wall, gusts sweeping inward every 0.7 s.
- **0.80** `windBoundDomain_pulse`, world, at the hero, identity rotation (life 1.1): a ring out to 14.4 m, a 15 m glow,
  60 sparkles.
- **2.80, 4.80, 6.80** `windBoundDomain_pulse` again (`WindBoundHeals`: Waits 2, then while now <= 0.8 + 6.05, on every
  client, before the owner's 3% heal). These are after the clip ends (1.7 s).
- **1.70** Row6End. Left out: the `windBound` status effect (`CharacterControl::AddWindBoundFx@0x24AF350`, prefab
  `windBound`) on enemies; the heals spawn nothing (`RPC_AddHeal` has no effect).

```json
"windBoundDomain": {
  "why": "TTO1102:Wolf.<RPC_windBoundDomain>d__313::MoveNext@0x1F51890 (default style): cast owned 0.2 m ahead at 0; Waits 0.8 (0x1F51F7C): plant 0.7 m ahead, domain and pulse at the hero (identity rotation); Waits 0.9 -> Row6End 1.7; WindBoundHeals@0x1F52EC0: Waits 2 (0x1F52F84) then a pulse every 2 s while t <= 6.85 (2.8, 4.8, 6.8)",
  "cues": [
  [0, "fx", "windBoundDomain_cast", 0.2],
  [0.8, "fx", "windBoundDomain_plant", 0.7],
  [0.8, "fx", "windBoundDomain_domain"],
  [0.8, "fx", "windBoundDomain_pulse"],
  [2.8, "fx", "windBoundDomain_pulse"],
  [4.8, "fx", "windBoundDomain_pulse"],
  [6.8, "fx", "windBoundDomain_pulse"]
  ]
}
```

Needs: cues after the clip ends (2.8-6.8 s; the domain itself lasts to 7.3 s); identity rotation for domain / pulse only
turns the sigil textures, so it can be ignored.

### 2.4 What the cue format would need (for the lead)

An optional 6th element, e.g. `{"at": [x, y, z], "roll": deg, "yaw": deg, "scale": s, "until": t}` (hero frame, Unity
metres and degrees; `at` replaces distance; `roll` about the hero's forward, `yaw` about up; `until` = destroy at clip
time t with no after-life), and a scatter cue for Blade Surge's lines
(`{"scatter": "bladeSurge_cut", "n": 6, "r": 6.3, "yk": 0.45, "minY": 0.3, "y": 1.2, "push": [0.25, 0.3], "tiltY": 0.6,
"scale": [0.6, 1.4], "until": 2.1}` per cut), or a small per-skill script hook in the page instead. Without at least
`at`/`roll`/`yaw`/`until`, Resonance Claw and Wind Bound Domain still work (minus the side-wave yaw); Blade Surge does not.

## 3. Does TTO's rip keep the settings? Component inventory

**Yes.** In every prefab YAML every MonoBehaviour has its fields serialized by name after `m_EditorClassIdentifier:`
(BB's rip had only `m_Script`); the scripts themselves (`Assets\Scripts\TTO.Game\*.cs`) are AssetRipper dummy classes,
but their `.cs.meta` GUIDs name the script (GroundHugEmitter `a85a61e01977fe60e9b5d03e9860e598`, ImageEmitter
`eb6194ecc51f008fa4e7eadc4897adb8`, EffectControl `a316d4e8a3d12ee256913ebc3f25e6d0`, ...). TTO's old-style emitters have
exactly BB's fields in BB's order (EffectControl `life, afterLife, followPosition, followState, effectRotationMode,
velocity`; ImageEmitter / RingEmitter / LineEmitter match `LAYOUTS` field for field). **Shuriken is used** (fully
serialized: `InitialModule`, `ShapeModule`, `EmissionModule` with `m_Bursts`, `ColorModule`, ...), next to the old
emitters, but no Unity legacy particles appear. All MeshFilters have `m_Mesh: {fileID: 0}` (meshes built at runtime).

Default variants (counts; "page" = drawn by `wardrobe/index.html` today):

| Prefab | EffectControl | ImageEmitter | RingEmitter | LineEmitter | AudioSource | GroundHugEmitter | ArcRibbonEmitter | GroundFollower | Shuriken PS |
|---|---|---|---|---|---|---|---|---|---|
| bladeSurge_aura | 1 | | | | 1 | 3 band | | | |
| bladeSurge_zone | 1 | 2 | | | | 1 band | | | 1 |
| bladeSurge_cut | 1 | 6 | | | | | | | |
| bladeSurge_flicker | 1 | 3 | | | | | | | |
| bladeSurge_sheathe | 1 | 1 | | | 1 | 1 band | | | |
| bladeSurge_shatter | 1 | 2 | | | 1 | 1 band | | | 2 |
| bladeSurge_shards | 1 | 2 | | | 1 | 1 band | | | 2 |
| resonanceClaw_charge | 1 | | | | 1 | 2 band | | | |
| resonanceClaw_rake | 1 | 1 | | | 1 | 1 band, 1 disc, 3 strip | 9 (Comet) | | 1 |
| resonanceClaw_wave_twin | 1 (velocity 36) | | | | 1 | | 6 (Crescent) | 1 | 1 |
| resonanceClaw_wave_light / _dark | 1 (velocity 36) | | | | | | 6 (Crescent) | 1 | 1 |
| resonanceClaw_burst (not cued) | 1 | 2 | 1 | | | | | | 1 |
| windBoundDomain_cast | 1 | | | 1 | 1 | 1 disc, 1 band | | | |
| windBoundDomain_plant | 1 | | | | 1 | 1 disc, 2 band | | | |
| windBoundDomain_domain | 1 | | | | | 1 disc, 3 band (Wall emits the motes PS) | | | 1 |
| windBoundDomain_pulse | 1 | | | | | 1 disc, 1 band | | | 1 |
| windBound (not cued) | | | | | | 1 disc, 2 band | | | |
| **page draws it** | yes | yes | yes | yes | yes (playOnAwake) | **no** | **no** | **no** | **no** (only legacy) |

So with today's page: Resonance Claw would show almost nothing but sounds (its look is ArcRibbon + GroundHug), Wind Bound
Domain only the cast's LineEmitter streaks, Blade Surge its ImageEmitter flashes, cut lines, domes and glints-less zone.
GroundHugEmitter is in 12 of the 18 default prefabs (in 11 of the 16 that are cued): it is the first thing to build.

Shuriken systems used (`ps.py`; `minScalar..scalar`, state 3 = random between two constants, state 0 = constant `scalar`):
zone Glints (looping, 40/s, life 0.4-0.9, sphere); shatter Glass (burst 160 at 0, life 0.9-1.7, speed 2.5-8, size
0.25-0.75, Rotation + Color modules) and Sparks (burst 90, speed 8-18, stretched render, lengthScale 3, velScale 0.04);
shards the same with bursts 71 / 40; rake Rays (burst 1, cone, Velocity + InheritVelocity, stretched, scalingMode Shape);
waves Sparks (looping 260/s, box shape); domain Motes (rate 0, fed by the Wall's `motes` / `motesPerSecond` 45); pulse
Sparkles (burst 60 at 0.05, circle shape).

The new scripts' fields (from `dump.cs` and the YAML):
- `GroundHugEmitter` (`dump.cs` TypeDefIndex 410): `shape` (0 Disc, 1 Band, 2 Strip), `Life, Delay, repeatForever,
  Emission, EmissionPeriod, startRadius, endRadius, startWidth, endWidth, startHeight, endHeight, startAngle, Rotation,
  uvTile, uvRotation, Color1..5, lift, segments, rings, resample, motes (ParticleSystem ref), motesPerSecond`; consts
  `GroundMask 1, RayUp 12, RayDown 24, Step 0.75`; methods Awake 0x22612C0, Start 0x2264610, LateUpdate 0x2263360,
  Sample 0x22639F0, Grid 0x2262B60, Ground 0x2263100, GroundAt 0x2262BD0, Ramp 0x2263760, get_Scale 0x2264A40,
  get_Centre 0x22649C0, StripTurned 0x2264620, Add(Vector3 **world**, uv, colour) 0x2261100, BuildDisc 0x2261A10,
  BuildBand 0x2261390, BuildStrip 0x2261FB0, EmitMotes 0x22627A0. It raycasts the ground and builds its mesh in world
  space, hugging the terrain by `lift`; on the page's flat floor that is y = the hero's feet + lift. For a Strip,
  startHeight/endHeight look like the length (rake claws 0.5 -> 38 m = the 36.6 m lanes) and width the lane width (8).
- `ArcRibbonEmitter` (TypeDefIndex 402): `Life, Delay, flat, profile (0 Crescent, 1 Comet), taper, centre (v3),
  startRadius, endRadius, startHead, endHead, startTail, endTail (degrees), easeHead, easeTail, startHeight, endHeight,
  lean, uvTile, uvScroll, Color1..5, segments, trail, trailStep, trailFade`; methods Awake 0x225D2A0, LateUpdate
  0x225DD80, PoseAt 0x225E3D0, Ramp 0x225E660, Ease 0x225DD40, Build 0x225D370, Add 0x225D080.
- `GroundFollower`: `smoothing` (12); private clearance, ready; Start 0x2261030, LateUpdate 0x2260ED0.
None of these methods is in `pseudo/`; they need a Ghidra run (BUILD.md: a targets file + `tools\run_ghidra.bat`, then
`annotate.py`) before the page can draw them faithfully. That is a decompile job in the Bible's tree, not something this
research did.

## 4. A TTO reader for `pipeline/wardrobe_fx.py`

### 4.1 Recommended source: TTO's decrypted bundles (not the YAML)

`wardrobe_data.py` already reads `D:\12tails-video\tto_assets\2026-11-04\dec\*.bundle` with UnityPy via
`D:\12tails\DecompiledSource_TTO_2026-11-02\tools\aa_catalog.py <tto_assets>\catalog.bin --grep ...` (columns: address,
type, internal id, bundles). For these effects that works too, and it is better than the rip:
- the address is exactly what the game loads (`gameassets/characters/heroes/wolf/effects/<name lower>` vs
  `.../arcana/ronin/effects/...`), so no default / Ronin guessing;
- every MonoBehaviour, ParticleSystem and AudioSource reads with `read_typetree()` (fields by name; no `LAYOUTS`, no byte
  self-check); the MonoScript (`m_Script` PPtr into an external file) gives `m_ClassName`;
- AudioClip and Texture2D come straight from the bundle.
Gotchas seen: `env.container` is empty for these; the bundle's own AssetBundle object's `m_Container` is keyed by the
catalog's **internal id** (e.g. default bladesurge_zone = `a4fc213a3471ece40b304a604ccfdc17`), value `{asset: PPtr}`. All
35 Wolf Lv 100 effects (both styles) sit in `2de56e912320270dc0a0c2d02d114205.bundle` of this catalog, with their
dependencies in the 28 bundles the catalog lists (all present in `dec`). Bundle names change every TTO build, so resolve
through the catalog, never by file name. The bundles are the video repo's extracted files (read-only for this repo, as
CLAUDE.md allows); the office PC has no TTO bundles (same limit as `wardrobe_data.py`).

### 4.2 If it has to be the YAML (the rip)

- Folders: prefabs, `.ogg` sounds and the skill clips (`bladeSurge.anim`, ...) flat in `Assets\`; materials in
  `Assets\Material\` and `Assets\Art\Material\`; textures (already PNG) in `Assets\Texture2D\` (wolfRow6_*,
  grandCross_mark) and `Assets\Art\Texture2D\` (Line_*, Ray1); scripts' GUIDs in `Assets\Scripts\TTO.Game\*.cs.meta`.
  GUIDs are AssetRipper's own (they do not match the catalog), so build a guid -> path index from the `.meta` files
  (a full walk of the 40,727-entry Assets root took about 2.5 min; cache it, or index only the folders above).
- Pick files with the table in section 0 (default = the listed file, not "the one without `_0`").
- Parse: split on `^--- !u!<classID> &<fileID>` (1 GameObject, 4 Transform, 114 MonoBehaviour, 23 MeshRenderer,
  33 MeshFilter, 82 AudioSource, 198 ParticleSystem, 199 ParticleSystemRenderer); no `stripped` documents in these
  prefabs. Unity's YAML is not plain YAML (tags, anchors); a regex split per document then a YAML load of each body works.
- GameObject: `m_Name`, `m_IsActive`, `m_Component: [- component: {fileID: N}]`.
- Transform: `m_LocalPosition {x,y,z}`, `m_LocalRotation {x,y,z,w}`, `m_LocalScale`, `m_Children [{fileID}]`,
  `m_Father` -> the same `pos` / `rot` (x, y, z, w) / `scale` / parent index as `effect()`.
- MonoBehaviour: `m_Script: {fileID: 11500000, guid: G, type: 3}` -> script name; fields after `m_EditorClassIdentifier`.
  Convert to `effect()`'s shapes: Color `{r,g,b,a}` -> `[r,g,b,a]` (the page's `ramp()` indexes `a[j]`), Vector3
  `{x,y,z}` -> `[x,y,z]`, 0/1 bools -> booleans, refs `{fileID: N}` (ImageEmitter `mMeshFilter`, GroundHugEmitter
  `motes` -> the ParticleSystem document id) -> `[0, N]` like the `"r"` type.
- MeshRenderer: `m_Materials: [{fileID: 2100000, guid: G, type: 2}]` -> `mats`.
- Material: `m_Shader: {fileID: 200 | 202 | 203, guid: 0000000000000000f000000000000000, type: 0}` (Unity's built-in
  extra resources, same ids as `BUILTIN_BLEND`: 200 add, 202 addsoft, 203 alpha; test the guid instead of BB's
  "default resources" external path); `m_SavedProperties.m_TexEnvs` is a **mapping** `_MainTex: {m_Texture: {fileID:
  2800000, guid: G, type: 3}, m_Scale: {x,y}, m_Offset: {x,y}}`, `m_Colors` a mapping `_TintColor: {r,g,b,a}` /
  `_Color` (some have both; e.g. `wolfRow6_dome`, `wolfRow6_shards` have neither -> null). Output the same
  `{blend, tex, scale, offset, tint, color}`.
- AudioSource (Unity 6): the clip is in **`m_Resource: {fileID: 8300000, guid: G, type: 3}`**; `m_audioClip` is
  `{fileID: 0}`. Also `m_Volume`, `m_PlayOnAwake`, `Loop`. The guid points at e.g. `artCancel2_0.ogg`: AssetRipper's
  collision suffix, the clip's real name is `artCancel2`. Name sounds by the clip name, not the file.
- ParticleSystem: emit a new comp (e.g. `{"type": "ParticleSystem", ...the modules...}`) with the renderer's
  `m_RenderMode`, `m_LengthScale`, `m_VelocityScale`, `m_Materials`.

### 4.3 Textures and sounds

- Textures: `wolfRow6_burst, _cutline, _dome, _fill, _getsuga_band, _getsuga_edge, _getsuga_haze, _shards, _sigil` and
  `grandCross_mark` are TTO's; `Line_vertMultilines2 / 4 / 7`, `Line_SimpleBall`, `Line_Multilines2`, `Ray1` are the same
  art as BB's (pixel difference <= 14/255, compression only), so they can share `wardrobe/data/fx/tex/<name>.webp` with
  BB's. Strip AssetRipper's `_<hash>` suffix (`grandCross_mark_ee386f0a.png`) or the default/Ronin copies will collide.
- Sounds: every default clip these skills play is BB's own sound (lengths equal to BB's WAVs to the millisecond,
  `ub_audio.py` / `ogg_len.py`): bladeSong_ring 0.757, artCancel2 0.226, bladeFang1-3 0.484, twinResonance_ring 2.997,
  skySlasher 1.198, cAttack4 1.062, secondWind 1.419, grandCross 1.337 (all in BB's `wolf/sounds/`), shatteringDream_hit
  1.691 (`bat/sounds/`), iceBreak 0.419 (`penguin/sounds/`). `rip_wav()` already finds all of them (its whole-rip walk
  covers the Bat / Penguin ones), so the TTO reader need not decode audio. The Ronin sounds differ (`arcana/ronin/sounds/`).

### 4.4 Coordinates

Same as BB: the YAML and the bundles are Unity's own left-handed space, quaternions `{x, y, z, w}`, so no conversion; the
page's `(-1, 1, 1)` mirror group covers it, as for BB. Keep the Unity yaw signs in cues (wave_light -45, wave_dark +45).
Two runtime differences to keep in mind: GroundHugEmitter builds its mesh in world space from raycast ground heights
(the page must use the floor, not the node's height: the zone spawns 1.2 m up but its ring lies on the ground), and
EffectControl `velocity` (0, 0, 36) on the waves is the whole 36 m run in 1 s, which the page already applies in the
spawn frame.

### 4.5 Content rule

These are TTO-only skills and the wolfRow6_* textures are TTO's; the sounds are BB's. The fx pilot is local only
(`FX_ON` off in the published copy), so nothing changes online today; when effects go online, the TTO release list and
the BB-content rule (`wardrobe_publish.py`) would have to decide about these.

## 5. Open questions, and how sure I am

1. **Default vs Ronin** (section 0): sure. Read from the bundles' own container via the catalog addresses, and the colours
   agree with the rip files listed.
2. **Timeline and positions** (section 2): sure for the times (Bible plus the instructions for every Ghidra-dropped float),
   positions, owned / world, the flicker roll table, the cut sounds, the ±45° slam blades, the side-wave yaws (matched to
   each spawn's string in the machine code). Fairly sure for the line scatter (read from pseudo-C; the clamp/push order is
   as Ghidra shows it). The shard positions are a Monte Carlo of that distribution, so they are a mean, not exact.
3. **Pulses at 2.8 / 4.8 / 6.8 s**: sure from the code; whether the page should play cues after its 1.7 s clip ends is the
   lead's call.
4. **How GroundHugEmitter / ArcRibbonEmitter / GroundFollower draw**: not known. Only fields and method names are read.
   They need decompiling first (section 3). My reading of Strip's height as length is a guess from the numbers.
5. **TTO's ImageEmitter / RingEmitter / LineEmitter / EffectControl behaving as BB's**: likely (same fields, same order)
   but not checked in TTO's code.
6. **Should the page show the Ronin style** when the Wolf wears the Ronin arcana outfit (`ArcanaRegistry.StyleOf`)? The
   wardrobe has no arcana notion today. User's call.
7. **Camera effects** (shake, white flash, motion blur, the lunarRamp grade during Blade Surge): the page has none. User or
   lead's call.
8. **Cue-format extension** (section 2.4): needed for Blade Surge to look right at all. Lead's call on the shape.
