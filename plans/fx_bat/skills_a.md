# Bat effects + sounds research: the cast channel (cast1, cast2) and the bigCast skills (bigCast1-3)

Researcher `skills_a`, 2026-11-13 (home PC). Scope: the clips `cast1`, `cast2`, `bigCast1`, `bigCast2`, `bigCast3` and
every skill that plays them: the shared cast channel `RPC_cast1` (21 BB skills; their cast3 releases are not in this
scope), and the three bigCast skills Guardian of the Night, Nefarious Whip, Black Servant (bigCast3 is their pool).
Research only (recipe steps 1-3). Line numbers are `D:\12tails\DecompiledSource\Bat.cs` unless another file is named.
Times are seconds from the start of the clip the cue is keyed by. Distance 0 = at the hero.

Read-only probes, in `checks\fx_bat_research\skills_a\` (git-ignored):
- `clip_calls.txt`, `flow_*.txt`: `clip_calls.js` / `clip_flow.js` output.
- `cond.py <file> <from> <to>`: a line range with the opaque predicates and lone braces dropped.
- `probe.json` (+ `summ.py` to read it): `wardrobe_fx.py bat --probe castRing,castEffect,bigCast_ring,guardian,guardian_ring,nefariousWhip_hit,blackServant_ring,blackServant,massCast`.
- `probe2.py` / `probe2.json`: `wardrobe_fx.effect()` in memory for `guardian` and `nefariousWhip_hit`, with the two
  layouts read from the decompile (below); nothing written.
- `probe_mats.py` / `probe_mats.txt`: each effect's materials and own sounds. `probe_shader_ids.py` / `.txt`: each
  material's built-in shader id.
- `probe_fields.py`: the Bat hero prefab's `Bat` MonoBehaviour fields: field 8 `castEffect` =
  `heroes/bat/effects/castEffect`, field 9 `castRing` = `heroes/bat/effects/castRing`.
- `cues.json`: the paste-ready entries below, checked as valid JSON.

---

## Read this first

1. **The Bat's shadow materials are built-in shader 205 (Particles/Multiply), which the page draws as additive.**
   `probe_shader_ids.txt`: ShadowRay, ShadowLine1, ShadowLine3, ShadowRing3 and Smoke4_multiply are all id 205 in
   "unity default resources". `wardrobe_fx.py` BUILTIN_BLEND has no 205 ("left out until a cued effect uses it"), so they
   come out `"add"`: a dark shadow drawn as a bright glow. They are in bigCast_ring, guardian, guardian_ring,
   nefariousWhip_hit, blackServant_ring and blackServant, so six of the nine effects here, and very likely most of the
   Bat's other shadow effects. **Part needed: the Particles/Multiply blend** (Blend Zero SrcColor; colour =
   lerp(white, texture x vertex colour, alpha); ZWrite Off, Cull Off, no _TintColor; medium sure on the id, as 206 / 207
   were), drawn like the existing `multiply2` (index.html:3781-3797), including its empty-canvas alpha trick. It must
   be built before the Bat's effects look right; it is a cross-class part (the parts researcher should own it).
2. **bigCast1 is the same channel in all three bigCast skills; bigCast3 is their pool.** The three channel coroutines
   (RPC_guardianOfTheNight, RPC_nefariousWhip, RPC_blackServant) differ only in myCommand, the cooldown and the bar
   length. So `bigCast1` and `bigCast2` are plain entries and `bigCast3` holds `skills: {guardianOfTheNight,
   nefariousWhip, blackServant}`. poolChains (index.html:1238-1257) then gives each its own tile with the steps of the
   "Guardian of the Night" sequence (the host, then hidden). The member ids come out `@GuardianOfTheNight`,
   `@NefariousWhip`, `@BlackServant` (the host's own id is `@GuardianoftheNight`, so no clash).
3. **bigCast_ring needs a cast bar that lasts at least a frame or two.** It is spawned when bigCast2 starts and has
   followState, so the game ends it when the release starts. magAdjust never goes below 0.1 s
   (CharacterControl.cs:20584-20588), so at top INT the game shows it for 0.1 s and then its 1 s after-life. With the
   page's `bigCast2*@0` it would be cut in its first frame. Recommended SEQ change (index.html:1152):
   `"Guardian of the Night: bigCast1@1 bigCast2*@0.1 bigCast3~"`. The `@1` is there because bigCast2 cuts in at 1.0 s
   (:30000) while the bigCast1 clip is 1.033 s long. With that change the cues below work as written. Open question 1.
4. **Three parts are missing, besides 1:**
   - `Bat_guardianOfTheNight`, the summon's script (the inventory lists it).
   - `AudioControl`, which shapes nefariousWhip_hit's looping sound (the inventory lists it).
   - (small, optional) castRing's `root` clip, which the coroutine starts 0.5 s after spawning the ring.

   Specs are under "Parts". The two layouts `wardrobe_fx.py` needs are proven by `probe2.py`, which uses up exactly the
   field bytes:
   - `Bat_guardianOfTheNight` (16 bytes): `guardianBlade` r, `castEffect` r (Bat_guardianOfTheNight.cs:169-175).
   - `AudioControl` (24 bytes): `minVolume` f, `maxVolume` f, `delay` f, `fadein` f, `middle` f, `fadeout` f
     (AudioControl.cs:233-248).
5. **Four effects are not in `fx_inventory.md`, but they are ready:**
   - `castRing` and `castEffect` are hero prefab fields (probe_fields.py).
   - `guardian_ring` and `blackServant` are loaded by CharacterControl.cs (:40545, :41379), as the status looks.
6. **Auto Mass (#431) rolls in RPC_cast1, but its cue belongs on cast3.** When the bar ends, with #431 learned and no
   massCast status up, `Random.Range(0, 100) < lckAdjust(12)` (about 12 %) draws `massCast` at the hero, with hero
   position and rotation (:23354), and gives massCast Lv 1 for 3 s (:23360).
   - It covers only 11 skills (:23270-23332): phantomBane, dissolute, corruption, curse, doom, blind, confusion,
     dreamDazzle, phantasmBlast, charm, shame.
   - It runs the same frame the `_cast` coroutine starts, so it lands at cast3 time 0.
   - For the cast3 researcher / editor, the cue in each of those 11 members:
     `[0, "fx", "massCast", {"p": 0.12, "roll": "autoMass"}]`.
   - Two catches (open questions 5 and 6):
     - The effect field is loaded only by RPC_massCast (:11134-11140). So BB draws the flash only once the Bat has cast
       Mass Cast in that session (like the Penguin's multiCast).
     - The status's purple tint (CharacterControl.cs:40037-40044) works like the Penguin's multiCast tint.
7. **A voice file's case.** The code loads `Voices/guardianOfTheNight1|2`, but the rip's files are
   `voices/guardianOftheNight1.wav` / `2.wav`. Resources.Load and Windows `os.path.exists` both ignore case, so
   `rip_wav` finds them. The built files take the cue's spelling (`v_guardianOfTheNight1.mp3`), and the page asks for
   that name, so online (case-sensitive) still matches. No change is needed; this is a note for whoever checks it.

---

## cast1: RPC_cast1, the cast channel (plain entry)

- **Coroutine:** `$RPC_cast1$19912`, `:22843-25026`.
  - The dispatcher starts it with the skill's name. It serves 21 BB skills (`:23369-24363`): Phantom Bane, Dissolute,
    Corruption, Curse, Nightmare, Doom, Mirage Orb, Shadow Illusion, Blind, Confusion, Hate Transfer, Swap, Dream
    Dazzle, Phantasm Blast, Charm, Mind Control, Mimic, Shame, Dark Stalker, Paranoia, Shattering Dream.
  - Nothing in the channel differs by skill except the cast time (`:24451-24800`; e.g. Shattering Dream 5 s, Mimic
    4 + 2 x sLv) and the cooldown.
  - It also serves the page's "Cast" tile (whose cast3 pool is hidden behind its members) and the "Nightmare" tile.
- **Timeline** (state machine; `case 0` goes to `IL_3785`):
  - **0:** `actionState = "attack"`, `myCommand = "cast"` (`:24803-24809`). `PlayAnimation("cast1", 0.2f)`, played once
    (`:24821`; the clip is 0.7 s, data/bat/clips.json). Voice `Random.Range(0, 2) == 0` ? `Voices/cast1` :
    `Voices/cast2` (`:24862-24917`; volume 1 for the local player, 0.75 for others). Then `Yield(2, 0.2)` (`:25021`).
  - **0.2 (case 2):** an older ring is destroyed (`:23016-23022`). `castRing` is instantiated at the hero position with
    `Quaternion.Euler(270, 90, 0)`, world-absolute (`:23028`), and `InitEffectControl(hero)` runs (`:23033-23038`).
    Then `Yield(3, 0.3)` (`:25019`).
  - **0.5 (case 3):** `moveSpeed = 0` (`:23065`). Then `Yield(4, 0.2)` (`:25023`).
  - **0.7 (case 4):** `PlayAnimation("cast2", 0)`, looped (`:23092-23097`). The ring's `root` clip is looped
    (`:23102-23107`). Then the cast bar: `castTime = now + magAdjust(...)` (`:23112`, `DisplayCastBar` `:23129`).
  - **Every frame** (`YieldDefault(5)`, `:25013`) it faces the target (`:23207-23224`). When `Time.time >= castTime`
    (`:23239`), the Auto Mass roll runs (Read this first, item 6), then `RPC_<skill>_cast` starts. Each sets
    `myCommand = "<skill>"` and plays cast3 with a 0.2 s fade (e.g. RPC_phantomBane_cast `:25607-25610`,
    RPC_nightmare_cast `:28736-28741`).
  - With no target, it calls `RPC_cast0` instead.
- **The cut:** castRing has followState (it records actionState / myCommand at init and goes to its after-life when
  either changes, EffectControl.cs:194-247), so it ends at cast3's start. Its afterLife is 0, so it is destroyed the
  next frame (EffectControl.cs:179-183); the `destroy` clip is never seen. On the page this is `cut: 0.65` on cast1's
  clock (the step edge 0.7, less 0.05, as the Penguin's 0.65 / the Sheep's 0.55).
- **Effects:**
  - `castRing`, **ready** (Animation create 0.47 s / root 2 s / destroy 0.5 s, StaticMesh with Ring_Shadow (202
    addsoft), EffectControl life 60, afterLife 0, followPosition, followState; AudioSource `cast_ring`, playOnAwake,
    loop).
  - The `root` clip starts after the cut, so its gap doesn't matter here.
  - `rot [270, 90, 0]`: the same reading as the Sheep's castRing. It is world-absolute in the game, a flat ring, so only
    the turn of its pattern differs.
- **Left out:** the Shadow Illusion clones start their own `RPC_cast1` / `RPC_cast2` (`:24936-24983`, `:24391-24436`).
  There are no clones on the page.
- **TTO1102:** `Bat.<RPC_cast1>d__154::MoveNext@0x1af42d0` has the same 21-skill list and the same voices
  (`String:'.../voices/cast1'`, `cast2`). Its waits were not re-traced.

```json
  "cast1": {
    "why": "Bat.cs RPC_cast1 ($RPC_cast1$19912, :22843-25026), the cast channel the dispatcher starts for every cast-time skill (21 BB skills: Phantom Bane, Dissolute, Corruption, Curse, Nightmare, Doom, Mirage Orb, Shadow Illusion, Blind, Confusion, Hate Transfer, Swap, Dream Dazzle, Phantasm Blast, Charm, Mind Control, Mimic, Shame, Dark Stalker, Paranoia, Shattering Dream, :23369-24363; the Cast tile and the Nightmare tile): at 0 (IL_3785): cast time and cooldown per skill (:24451-24800), actionState attack and myCommand cast (:24803-24809), clip cast1 (0.2 fade, :24821) and voice cast1 / cast2 (Random.Range(0, 2) :24862, Voices/cast1 :24874-24886, Voices/cast2 :24905-24917; PlayOneShot volume 1 for the local player); Yield 0.2 (:25021): castRing at the hero position, Quaternion.Euler(270, 90, 0), world-absolute (:23028; the hero prefab's castRing field = Resources bat/effects/castRing, checks/fx_bat_research/skills_a/probe_fields.py), InitEffectControl(hero) (:23033-23038; EffectControl life 60, afterLife 0, followPosition, followState; plays its own looping Sounds/cast_ring); Yield 0.3 (:25019): moveSpeed 0 at 0.5 s (:23065); Yield 0.2 (:25023): cast2 cut in and looped and the ring's root clip looped at 0.7 s (:23092-23107), the cast bar magAdjust (:23112-23129; the page: none), then each frame until it ends (YieldDefault(5) :25013, :23239) the skill's RPC_<skill>_cast starts (:23369-24363) and sets myCommand to the skill (e.g. RPC_phantomBane_cast :25607): the ring's followState cut at the step edge 0.7 s (EffectControl.cs:194-247; afterLife 0: destroyed at once, :179-183), cued 0.65 because the page restarts FX.t at each step (as the Penguin's); Auto Mass #431's roll at the bar's end (:23247-23363) is cued on the 11 cast3 skills it covers; the Shadow Illusion clones' own RPC_cast1 (:24936-24983) left out (no clones on the page)",
    "cues": [
    [0, "voice", "cast1|cast2"],
    [0.2, "fx", "castRing", {"rot": [270, 90, 0], "cut": 0.65}]
    ]
  }
```

Sure: high for the times and names.

## cast2: no entry

The cast bar's loop. Nothing is spawned in it: the ring's root clip, the bar and facing the target only. The page holds it
for 0 s (the user's no-cast-bar rule; no cue depends on it).

---

## bigCast1: the shared channel of Guardian of the Night, Nefarious Whip, Black Servant (plain entry)

| | Guardian of the Night | Nefarious Whip | Black Servant |
|---|---|---|---|
| coroutine | `$RPC_guardianOfTheNight$20085` :29768-30311 | `$RPC_nefariousWhip$20427` :42675-43239 | `$RPC_blackServant$20474` :44569-44688 (state 0 at `IL_8D1`) |
| myCommand at 0 | guardianOfTheNight1 :30197 | nefariousWhip1 :43039 | blackServant :44576 |
| cooldown | agiAdjust(600) :30200 | agiAdjust(180) :43044 | agiAdjust(180) :44579 |
| bigCast1 (0.2 fade) | :30209 | :43059 | :44588 |
| voice `Voices/bigCast` | :30256, PlayOneShot :30306 | :43116, :43222 | :44635, :44682 |
| Yield 0.2 / 0.5 / 0.3 | :30298 / :30302 / :30304 | :43230 / :43237 / :43228 | :44669 / :44671 / :44675 |
| castRing (0.2 s) | :29933 | :42829 | :44288 |
| ring root (0.7 s) | :29968-29973 | :42864-42869 | :44323-44328 |
| bigCast2 cut + loop (1.0 s) | :30000-30005 | :42896-42901 | :44355-44360 |
| bigCast_ring (1.0 s) | :30026-30038 | :42922-42934 | :44381-44393 |
| bar | magAdjust(3 x sLv + 7) = 13 s at rank 2, :30052 | magAdjust(7) :42948 | magAdjust(7) :44407 |
| release starts | :30155-30176 | :43187-43208 | :44534-44555 |
| release's myCommand | guardianOfTheNight2 :30697 | nefariousWhip2 :43605 | blackServant2 :45331 |

- **Timeline:**
  - **0:** bigCast1 with a 0.2 s fade, and the voice `bigCast` (one file; the local player always).
  - **0.2:** `castRing` by `mChar.createEffect` (InitEffectControl inside, CharacterControl.cs:24191-24210) at
    `position + TransformDirection(0, 0, -0.1)` (0.1 m behind), `Quaternion.Euler(270, 90, 0)`, world-absolute.
  - **0.7:** the ring's root clip, looped.
  - **1.0:** bigCast2 cut in and looped, the ring's root again, `bigCast_ring` (bigCast2's entry), the bar. Then every
    frame it faces the target, and at the bar's end the release starts.
- **The cut:** the release changes myCommand, so castRing's followState cuts it at the bar's end.
  - On the page that is the step edge bigCast1 -> bigCast2 (1.0 s with the `bigCast1@1` of Read this first, item 3;
    1.033 s without it), so `cut: 0.95` on bigCast1's clock.
  - A cut on bigCast2's clock can't be used: the ring would be cut the moment it spawns, because the page's cut compares
    the current step's clock (index.html:3947).
- **Effects:**
  - `castRing`, **ready** (as in cast1).
  - Its `root` clip runs 0.7-1.0 s here, about 0.25 s the page shows as `create`'s last pose. Optional part (Parts, 3).
- **TTO1102:** `Bat.<RPC_guardianOfTheNight>d__173`, `<RPC_nefariousWhip>d__218` and `<RPC_blackServant>d__221` have the
  same strings and the same 0.2 / 0.3 / 0.5 constants (`.../effects/bigCast_ring`, `.../voices/bigCast`).

```json
  "bigCast1": {
    "why": "The channel of the three bigCast skills, the same in each (Bat.cs RPC_guardianOfTheNight :29768-30311, RPC_nefariousWhip :42675-43239, RPC_blackServant :44569-44688; TTO1102's three load the same names): at 0: actionState attack and myCommand guardianOfTheNight1 / nefariousWhip1 / blackServant (:30191-30197, :43029-43039, :44570-44576), clip bigCast1 (0.2 fade, :30209, :43059, :44588) and voice bigCast (one file; :30256 + :30306, :43116 + :43222, :44635 + :44682); Yield 0.2 (:30298, :43230, :44669): castRing 0.1 m behind the hero, TransformDirection(0, 0, -0.1), Quaternion.Euler(270, 90, 0) world-absolute, by createEffect (InitEffectControl, CharacterControl.cs:24191-24210) (:29933, :42829, :44288); Yield 0.5 (:30302, :43237, :44671): the ring's root clip looped at 0.7 s (:29968-29973, :42864-42869, :44323-44328); Yield 0.3 (:30304, :43228, :44675): bigCast2 cut in and looped at 1.0 s (:30000-30005, :42896-42901, :44355-44360; bigCast2's entry has the rest); the release RPC_<skill>_cast sets myCommand guardianOfTheNight2 / nefariousWhip2 / blackServant2 (:30697, :43605, :45331): the ring's followState cut there (EffectControl.cs:194-247; afterLife 0), cued 0.95 on bigCast1's clock (the step edge 1.0, less the page's 0.05 margin)",
    "cues": [
    [0, "voice", "bigCast"],
    [0.2, "fx", "castRing", {"d": -0.1, "rot": [270, 90, 0], "cut": 0.95}]
    ]
  }
```

## bigCast2: the bar (plain entry)

- `bigCast_ring` at the hero, with hero position and rotation, at bigCast2's start (rows above). It is **ready**:
  - EffectControl life 99, afterLife 1, followPosition, followState.
  - Parts: VortexEmitter (ShadowRay, life 1, three vortices, repeatForever), LineEmitter `RayEmitter` (ShadowRay,
    24 / s), RingEmitter (ShadowLine1, 4 per 0.2 s).
  - AudioSource `bigCast_ring`, playOnAwake, loop.
  - Its materials are all built-in 205 (Read this first, item 1).
- **The cut:** the bar's end, the same followState change as castRing's. With `bigCast2*@0.1` the cue is `cut: 0.05` on
  bigCast2's clock. If a frame misses the window, it falls at 0.05 into bigCast3, still before the clip's visible start.
  In the after-life its emitters stop, and the page's RingEmitters run on for the 1 s (as the game, index.html:3951).
- Without the SEQ change (bar `@0`), the same cue still plays, but the ring is cut in its first frame: only its first
  particles fade over the 1 s after-life.

```json
  "bigCast2": {
    "why": "The cast bar of the three bigCast skills (Bat.cs :30000-30069, :42896-42965, :44355-44424): at its start bigCast_ring at the hero, hero position and rotation, by createEffect (Resources bat/effects/bigCast_ring :30026-30038, :42922-42934, :44381-44393; EffectControl life 99, afterLife 1, followPosition, followState; plays its own looping Sounds/bigCast_ring); the bar magAdjust(3 x 2 + 7) / magAdjust(7) / magAdjust(7) (:30052, :42948, :44407), at least 0.1 s (magAdjust's floor, CharacterControl.cs:20584-20588: the SEQ's bigCast2*@0.1); the release sets myCommand at the bar's end (:30697, :43605, :45331): the ring's followState cut, cued 0.05 (the step edge 0.1 less the page's margin)",
    "cues": [
    [0, "fx", "bigCast_ring", {"cut": 0.05}]
    ]
  }
```

## bigCast3: the pool (`skills`): Guardian of the Night, Nefarious Whip, Black Servant

Every release has the same frame. In state 0 (the coroutine's default block) it checks that myCommand is still the
channel's. Then:
- `myCommand = "<skill>2"`, `PlayAnimation("bigCast3", 0.2f)` once (the 2.0 s clip), and the skill's voice.
- `Yield(2, 0.5)`: `castEffect` (the hero prefab field, `heroes/bat/effects/castEffect`) at
  `position + TransformDirection(0, 1.8, 1)` (1.8 m up, 1 m ahead), with hero rotation, and the skill's own work.
- The waits that follow, then standby.

castEffect is **ready**: EffectControl life 2 (no follow), one ImageEmitter (castEffect, 202 addsoft, LocalRotation
mode, delay 0.2, life 0.5), AudioSource `cast_effect` once.

### Guardian of the Night (#271 / #272, rank 2)

- **Coroutine:** `$RPC_guardianOfTheNight_cast$20100` `:30362-30841`.
- **0:** myCommand guardianOfTheNight2 (`:30697`), bigCast3 (`:30700`). Voice `Random.Range(0, 2)`:
  `guardianOfTheNight1` / `guardianOfTheNight2` (`:30741-30800`, PlayOneShot `:30825-30828`). Then `Yield(2, 0.5)`
  (`:30837`).
- **0.5:** castEffect (`:30504`). Then `Yield(3, 0.5)` (`:30821`).
- **1.0:**
  - An older guardian is destroyed (`:30531-30537`).
  - `Effects/guardian` is instantiated at `position - 4 * transform.forward` (4 m behind the hero; `spL2mZrk3v` is
    `this.transform`, `:57`) with hero rotation (`:30549-30561`).
  - `Bat_guardianOfTheNight.Init(hero, sLv)` starts (`:30586`).
  - Status `guardianOfTheNight` for `chaAdjust(30 x 2)` (60 s or more, `:30592-30603`, local player).
  - The AI timer: first scan 4 s later (`:30614`).
  - Then `Yield(4, 1)` (`:30816`).
- **2.0:** standby (`:30641`).
- **The status look** (CharacterControl.cs:40541-40564): `Effects/guardian_ring` by `createEffect` at the hero,
  `Quaternion.identity`, parented to the hero, named `guardianOfTheNightFx`.
  - It is **ready**: no EffectControl, one RingEmitter (ShadowLine1, 205).
  - It lasts the status: kill 10 (the standing rule).
- **The summon `guardian`** (`probe2.json`): Animation (root 1.6 s loop / run / walk 2.0 s loop / nAttack 1.8 / cast 1.7
  / ko 2.0), the `Bat_guardianOfTheNight` script, AudioSource `guardian_ring` (playOnAwake, loop). Two RingEmitters
  (ShadowLine1 / ShadowRay, 205) at z -0.2. `Shade4_tri` SkinnedMeshRenderer (2,349 vertices, two submeshes,
  materials `guardian1` FX/Phoenix + `guardian2` Transparent/Opaque1, both built in mesh.js; scale 1.2). A legacy
  ParticleEmitter on Spine1 (ShadowRay). No EffectControl: it stays until unsummoned. **Needs Bat_guardianOfTheNight**
  (Parts, 1); everything else is built.
- **Its life in the game:**
  - Init (Bat_guardianOfTheNight.cs:283-470): walk looped (`:436-439`). Over 1 s it glides from 4 to 2 m behind the
    owner, `Lerp(owner - 4 fwd, owner - 2 fwd, t)` (`:338`). Material 0's alpha goes 0 -> 0.8 and material 1's 0 -> 1
    (`:351-406`).
  - Then standby (`:306`). In Update (`:32-98`), within 3 m of the owner it does `CrossFade("root", 0.2)`, looped.
    Farther away it would walk after him (never here: the hero stands still).
  - The status's end (Bat.cs:12436-12442) calls `unsummon` (Bat_guardianOfTheNight.cs:1998-2121): `ko` played once,
    alpha back to 0.8 / 1, destroyed 2 s later.
- **Its AI** (Bat.cs:12275-12445): from 4 s after the summon, every 2.5 s, a random living enemy within
  `FindAreaTarget(32, 12)`.
  - Under 16 m it attacks (`attack`, Bat_guardianOfTheNight.cs:622-1450): it fades out, reappears 6 m before the
    target, plays `nAttack` with `Shade4/Sounds/nAttack` and a `guardianBlade` on its `sword` bone, hits 4 m around,
    puts `Shade4/Effects/nAttack_hit` on the hit (Bat.cs:12606-12629), and fades back.
  - Otherwise, 50 % of the time, `castSpell` (`:1646-1868`: `cast` clip, its castEffect at (0, 2.75, 1.2), curse or
    nightmare on the target).
  - Left out (open question 2): the skill has no target, and these are the summon's own choices, not the skill's
    timeline.
- **Rank:** rank 2 is the top. sLv only sets the guardian's damage and the 30 x sLv duration; nothing drawn differs by
  rank.

```json
      "guardianOfTheNight": {
        "why": "Bat.cs RPC_guardianOfTheNight_cast (:30362-30841; started when the bar ends, :30155-30176), no target: at 0: myCommand guardianOfTheNight2 (:30697), clip bigCast3 (0.2 fade, :30700), voice guardianOfTheNight1 / guardianOfTheNight2 (Random.Range(0, 2) :30741, :30751, :30782, PlayOneShot :30825-30828; the rip's files are voices/guardianOftheNight1 / 2.wav: Resources.Load and Windows paths are case-blind); Yield 0.5 (:30837): castEffect 1.8 m up 1 m ahead, TransformDirection(0, 1.8, 1), hero rotation (:30504; the hero prefab's castEffect field = bat/effects/castEffect; plays its own Sounds/cast_effect); Yield 0.5 (:30821): at 1.0 s the guardian, Resources bat/effects/guardian, 4 m behind the hero (position - 4 x transform.forward, hero rotation, :30549-30561), Bat_guardianOfTheNight.Init(hero, sLv 2) (:30586; walk looped, glides from 4 to 2 m behind in 1 s while its two materials fade in, alpha 0 to 0.8 / 0 to 1, then standby and root, Bat_guardianOfTheNight.cs:283-470, :32-98; plays its own looping Sounds/guardian_ring), and the guardianOfTheNight status for chaAdjust(30 x 2), 60 s or more (:30592-30603), whose apply puts Effects/guardian_ring at the hero, identity, parented (CharacterControl.cs:40541-40564); both last until the status ends (the summon's ko clip then gone 2 s later, Bat.cs:12436-12442, Bat_guardianOfTheNight.cs:1998-2121): cut at 10 s (unsummon 10, kill 12; guardian_ring kill 10); its AI (first scan 4 s after the summon, then every 2.5 s, Bat.cs:12275-12445, :30614) finds no enemy here: no attacks; Yield 1 (:30816): standby at 2.0 s (:30641)",
        "cues": [
        [0, "voice", "guardianOfTheNight1|guardianOfTheNight2"],
        [0.5, "fx", "castEffect", {"d": 1, "y": 1.8}],
        [1.0, "fx", "guardian", {"d": -4, "unsummon": 10, "kill": 12}],
        [1.0, "fx", "guardian_ring", {"kill": 10}]
        ]
      }
```

`unsummon` is a new cue option, read by the part (the cue's other options reach the parts as `fx.at`, index.html:4307).
If the part doesn't take it, use `{"d": -4, "kill": 10}` (open question 3).

### Nefarious Whip (#434)

- **Coroutine:** `$RPC_nefariousWhip_cast$20440` `:43287-43745`.
- **0:** myCommand nefariousWhip2 (`:43605`), bigCast3 (`:43608`). Voice `Random.Range(0, 2)`: `nefariousWhip1` /
  `nefariousWhip2` (`:43649-43708`, PlayOneShot `:43726`, `:43742`). Then `Yield(2, 0.5)` (`:43734`).
- **0.5:** castEffect (`:43429`). If the target lives (`:43434-43476`), `RPC_nefariousWhip_hit` (`:43482`; the method
  is at `:14740`). Then `Yield(3, 0.4)` (`:43729`).
- **0.9:** moveSpeed 0 (`:43522`). Then `Yield(4, 0.4)` (`:43738`).
- **1.3:** standby (`:43549`). The 2.0 s clip runs on.
- **RPC_nefariousWhip_hit** (`$...$20451`, `:43783-44077`):
  - At once, `tChar.createEffect(nefariousWhip_hit, target.position, Bat's rotation)` (`:44019-44037`): at the target's
    feet, so the 10 m target point, `d: 10`, no rot (the Bat's rotation is the hero's).
  - Then, on the caster's client, 8 ticks 0.5 s apart (`:44060-44075`): every enemy in `FindAreaTarget(target, 4, 6)`
    takes Effect Damage 434 (`:43918-43957`). Nothing is drawn.
- **nefariousWhip_hit** (`probe2.json`):
  - EffectControl life 5, afterLife 5, followPosition.
  - Six ImageEmitters (nefariousWhip1-3 203 alpha; nefariousWhip4 `Particles/AlphaOffset`; `LineEmitter`
    nefariousWhip5 202): delays 0.5-0.9 s, emitting for 3.5-3.8 s.
  - Two RingEmitters: Smoke4_multiply (205), ShadowRay (205).
  - AudioSource `nefariousWhip` (playOnAwake, **loop**) and **AudioControl** {min 0, max 1, delay 0.5, fadein 0.5,
    middle 4, fadeout 0.2}.
  - **Needs AudioControl** (Parts, 2) and the 205 blend (Read this first, item 1).
  - `Particles/AlphaOffset` needs nothing. It goes the page's plain alpha path (index.html:3829-3838), as the Sheep's
    returnCast already does. The game's second combine (`previous * previous alpha`) darkens its colour by alpha once
    more (rip `gameassets/shader/AlphaOffset.shader`): close enough.

```json
      "nefariousWhip": {
        "why": "Bat.cs RPC_nefariousWhip_cast (:43287-43745; started when the bar ends, :43187-43208; enemy target: the 10 m target point): at 0: myCommand nefariousWhip2 (:43605), clip bigCast3 (0.2 fade, :43608), voice nefariousWhip1 / nefariousWhip2 (Random.Range(0, 2) :43649, :43659, :43690, PlayOneShot :43726, :43742); Yield 0.5 (:43734): castEffect TransformDirection(0, 1.8, 1), hero rotation (:43429), and RPC_nefariousWhip_hit on the target while it lives (:43482), which at once puts nefariousWhip_hit at the target's position with the Bat's rotation (:44025-44037; EffectControl life 5 + afterLife 5; its own looping Sounds/nefariousWhip under an AudioControl: 0.5 s delay, 0.5 s fade-in, 4 s, 0.2 s fade-out, then silent), then 8 damage ticks 0.5 s apart within 4 m of it (:43918-43957, :44060-44075; nothing drawn); Yield 0.4 (:43729): moveSpeed 0 (:43522); Yield 0.4 (:43738): standby at 1.3 s (:43549)",
        "cues": [
        [0, "voice", "nefariousWhip1|nefariousWhip2"],
        [0.5, "fx", "castEffect", {"d": 1, "y": 1.8}],
        [0.5, "fx", "nefariousWhip_hit", {"d": 10}]
        ]
      }
```

### Black Servant (#444)

- **Coroutine:** `$RPC_blackServant_cast$20479` `:44732-45441`. The target must be a dead hero-type player
  (`:8468-8511`), so it is the 10 m target point.
- **0:** myCommand blackServant2 (`:45331`), bigCast3 (`:45334`). Voice `blackServant`, one file (`:45381`, PlayOneShot
  `:45433`; the rip's `blackServant1` / `2.wav` are never loaded by BB). Then `Yield(2, 0.5)` (`:45429`).
- **0.5:**
  - castEffect (`:44878`).
  - `hitChar.createEffect(blackServant_ring, target.position, target.rotation)` (`:44911-44929`): the 10 m point. The
    target faces the hero, so `rot [0, 180, 0]` (Penguin decision 4).
  - `Shadow<Class>_AI` is added (`:44943-45169`).
  - Status `blackServant` Lv 5 for `getDebuff(90)` on the target (`:45206`).
  - Then `Yield(3, 0.4)` (`:45414`).
- **0.9:** moveSpeed 0 (`:45243`). Then `Yield(4, 0.4)` (`:45438`).
- **1.3:** standby (`:45275`).
- **The status apply** (CharacterControl.cs:41338-41413):
  - The dead player is raised: hp and ko set to half, standby, grey `setColor(0.35)`, on the Bat's layer. Nothing of
    that is drawn: there is no body on the page.
  - `Effects/blackServant` is instantiated at `collider.bounds.center + up * extents.y` (the collider's top),
    `Quaternion.identity`, parented, scale `Clamp(radius + 0.4, 0.5, 2)`.
  - With a Bat-sized body (Bat.prefab CharacterController centre y 0.9, height 1.7, radius 0.3) that gives y 1.75 and
    scale 0.7 (open question 4).
  - It has no EffectControl, so it lasts the status: kill 10.
- **blackServant_ring**, **ready**: EffectControl life 1, afterLife 1. ImageEmitter (ShadowRing3, horizontal, 4 in
  0.6 s), RingEmitter (ShadowLine3, rising to 6 m), VortexEmitter (ShadowRay), all 205.
- **blackServant**, **ready**: one RingEmitter (ShadowRay 205, purple, radius 1, life 2), a ring over the head.

```json
      "blackServant": {
        "why": "Bat.cs RPC_blackServant_cast (:44732-45441; started when the bar ends, :44534-44555; target: a dead enemy player, Bat.cs:8468-8511: the 10 m target point): at 0: myCommand blackServant2 (:45331), clip bigCast3 (0.2 fade, :45334), voice blackServant (one file, :45381, PlayOneShot :45433; voices/blackServant1 / 2.wav are never loaded); Yield 0.5 (:45429): castEffect TransformDirection(0, 1.8, 1), hero rotation (:44878), blackServant_ring at the target's position with the target's rotation (:44911-44929; the target faces the hero: rot [0, 180, 0], plans/fx_penguin/decisions.md 4), the Shadow<Class>_AI (:44943-45169) and the blackServant status for getDebuff(90) (:45206), whose apply raises the body (hp and ko to half, standby, grey tint 0.35: no body on the page) and puts Effects/blackServant on top of its collider, collider.bounds.center + up x extents.y, identity, parented, scale Clamp(radius + 0.4, 0.5, 2) (CharacterControl.cs:41338-41413): a Bat-sized body (Bat.prefab CharacterController centre y 0.9, height 1.7, radius 0.3: y 1.75, scale 0.7; the own-class body as plans/fx_penguin/decisions.md 3), no EffectControl: it lasts the status, cut at 10 s (kill 10); Yield 0.4 (:45414): moveSpeed 0 (:45243); Yield 0.4 (:45438): standby at 1.3 s (:45275)",
        "cues": [
        [0, "voice", "blackServant"],
        [0.5, "fx", "castEffect", {"d": 1, "y": 1.8}],
        [0.5, "fx", "blackServant_ring", {"d": 10, "rot": [0, 180, 0]}],
        [0.5, "fx", "blackServant", {"d": 10, "y": 1.75, "scale": 0.7, "kill": 10}]
        ]
      }
```

### The pool entry (the three members above go in `skills`)

```json
  "bigCast3": {
    "why": "The bigCast3 clip is the release of three Bat skills after the bigCast1 / bigCast2 channel (Bat.cs RPC_guardianOfTheNight_cast :30700, RPC_nefariousWhip_cast :43608, RPC_blackServant_cast :45334, each PlayAnimation(bigCast3, 0.2)): one tile each (poolChains, with the Guardian of the Night sequence's steps)",
    "skills": { "guardianOfTheNight": {...}, "nefariousWhip": {...}, "blackServant": {...} }
  }
```

The whole set, valid JSON: `checks\fx_bat_research\skills_a\cues.json`.

TTO1102 for the releases: `<RPC_guardianOfTheNight_cast>d__174` loads the same names and constants (1.8, 4, 0.5, 1),
with the voice path spelled `voices/guardianOftheNight1`. `<RPC_nefariousWhip_cast>d__219`, `<RPC_nefariousWhip_hit>d__220`
and `<RPC_blackServant_cast>d__222` match too; TTO adds an `AddAISummoner` call in the last. No look changes.

---

## Effects in this scope

| effect | loaded at | parts | state |
|---|---|---|---|
| castRing | hero field 9 (RPC_cast1 :23028; bigCast :29933, :42829, :44288) | Animation, StaticMesh, EffectControl, AudioSource | ready (root clip: optional part 3) |
| castEffect | hero field 8 (:30504, :43429, :44878) | ImageEmitter, EffectControl, AudioSource | ready |
| bigCast_ring | :30026, :42922, :44381 | VortexEmitter, LineEmitter, RingEmitter, EffectControl, AudioSource | ready; materials 205 |
| guardian | :30549 | Bat_guardianOfTheNight, Animation, SkinnedMeshRenderer (FX/Phoenix, Opaque1), legacy particles, RingEmitter, AudioSource | needs part 1; materials 205 |
| guardian_ring | CharacterControl.cs:40545 | RingEmitter | ready; material 205 |
| nefariousWhip_hit | :44025 | AudioControl, ImageEmitter, RingEmitter, EffectControl, AudioSource | needs part 2; Smoke4_multiply / ShadowRay 205 |
| blackServant_ring | :44917 | ImageEmitter, RingEmitter, VortexEmitter, EffectControl | ready; materials 205 |
| blackServant | CharacterControl.cs:41379 | RingEmitter | ready; material 205 |
| massCast (Auto Mass, cast3 cue) | :11140 | RingEmitter, LineEmitter, EffectControl, AudioSource | ready (202) |

Voices (`voices/`): cast1, cast2, bigCast, guardianOfTheNight1, guardianOfTheNight2 (files `guardianOftheNight*.wav`),
nefariousWhip1, nefariousWhip2, blackServant. Effects' own sounds (`sounds/`): cast_ring, cast_effect, bigCast_ring,
guardian_ring, nefariousWhip, massCast. No name is in both folders, and no coroutine here plays a `Sounds/` clip
itself.

## Parts (for the parts stage)

1. **Bat_guardianOfTheNight** (a script on the summon's root; `fxparts/bat.js`):
   - Over 1 s from spawn: root position Lerp(spawn, spawn + 2 m along its own forward), clamped. With the cue's d -4
     and hero rotation, that is 4 m to 2 m behind the hero.
   - `walk` looped while it moves. Material 0 (`guardian1`, FX/Phoenix) alpha 0 -> 0.8 and material 1 (`guardian2`,
     Opaque1) alpha 0 -> 1, linear.
   - Then `CrossFade("root", 0.2)`, looped.
   - The saved materials have alpha 0. Without the fade the summon stays invisible (Opaque1's AlphaTest GEqual 0.95).
   - With `fx.at.unsummon` = t: at age t, `ko` once and alpha back to 0.8 / 1; the cue's kill removes it 2 s later.
   - The AI's attack and castSpell are not built (open question 2). Its legacy particle system on Spine1 must follow
     the skinned bone (Spine1).
2. **AudioControl** (any effect's AudioSource; nefariousWhip_hit is the only cued user here):
   - The AudioSource starts `delay` s late (playOnAwake off, AudioControl.cs:55-66, `Play()` at the delay, :149-157).
   - Volume: min until the delay, Lerp(min, max) over `fadein`, max for `middle`, Lerp(max, min) over `fadeout`, then
     min (AudioControl.cs:112-208).
   - It works through the loop handle's `setVolume` (index.html:3694-3700).
   - Here: silent 0.5 s, up to 1 by 1.0 s, held to 5.0 s, down to 0 by 5.2 s, then looping silently until the effect
     ends at 10 s.
3. (optional) **castRing's root clip**: the channel coroutines play the ring's `root` clip, looped, 0.5 s after spawning
   it (:23102 / :29968 / :42864 / :44323; for cast1 the cut comes first). It could be a hook `fx:castRing` (as the
   Sheep's Holy Light ring) that plays `root` looped at age 0.5. Seen only in the bigCast tiles, about 0.25 s.
4. **Particles/Multiply (205)**, Read this first, item 1 (cross-class; the parts researcher's).

## Passives, ranks, random picks

- Random picks: voice cast1|cast2 (:24862), guardianOfTheNight1|2 (:30741), nefariousWhip1|2 (:43649). The other
  voices are single files.
- Auto Mass (#431, 12 %), from RPC_cast1 at the bar's end, on 11 cast3 skills (Read this first, item 6).
- Shadow Mastery (getShadowMasteryLv :24457) changes only the cooldowns.
- Ranks:
  - Guardian of the Night 2 is the top. Its rank changes the bar, the duration and the guardian's damage, and nothing
    drawn.
  - Nefarious Whip and Black Servant are one rank.
  - No effect is picked by sLv in this scope.
- Clones (Shadow Illusion) rerun the channel (:24936-24983) and cast3 (:24391-24436). They are left out (no clones on
  the page).

## TTO and others

- **Crimson Verdict and Evil Twin (TTO, not released: no cues)** play cast1 -> cast2 through
  `TTO1102:Bat.<RPC_row6Cast>d__320::MoveNext@0x1b1f5f0` (pseudo/Bat.c:22069-22418):
  - cast1 with a 0.2 s fade and `Row6Voice("cast1", "cast2")` (:22170-22184).
  - At 0.2 s (`DAT_1830043a0 = 0.2`, :22116, the `ringUp` check :22222-22226) the same castRing, at the hero with
    Euler(4.712, 1.571, 0) rad = (270, 90, 0) (:22242-22272).
  - moveSpeed 0 at 0.5 s (:22276-22281). cast2 looped and the ring's root at 0.7 s (:22282-22298).
  - The bar magAdjust(1.2) / magAdjust(3), then Row6Release.
  - If they are released later, this `cast1` entry fits them as is (their tiles would be "cast1 cast2*@0 <their clip>").
- **Nightfall Swarm** (the released TTO skill) has no cast bar (DoRow6Skill -> SwarmLanding), so nothing here.
- Reborn's Eternal Night (bigCast2) and ToT's Dark Impulse (bigCast3, the Bible's ToT notes) are neither BB nor TTO:
  out of scope.

## Possible Bible findings (to offer the user; not written there)

- The Guardian of the Night summon's first AI scan comes 4 s after the summon (`Qypvswnda4 = Time.time + 4`, :30614).
  The reference has the 2.5 s scan interval but not the first delay.
- BB's Auto Mass flash (`massCast`) draws only after the Bat has cast Mass Cast once in the session: the field is
  loaded only in RPC_massCast (:11134-11140), and RPC_cast1 checks it (:23348). The status itself always applies.
- The Guardian of the Night summon walks in from 4 m to 2 m behind the Bat over its first second, fading in
  (Bat_guardianOfTheNight.cs:338-406).

---

## Open questions (each with my recommended answer)

1. **The bigCast bar on the page.**
   - Recommended: change the Guardian of the Night sequence to `bigCast1@1 bigCast2*@0.1 bigCast3~`. 0.1 s is the
     game's own floor at top INT (magAdjust clamps there), so "no cast bar" holds.
   - That gives bigCast_ring the 0.1 s it shows in the game, and bigCast2 starts at 1.0 s as in the code, not after the
     1.033 s clip.
   - The cues above assume it. Without it, keep the cues: the ring then shows only as its after-life.
2. **The guardian's AI attacks.**
   - Recommended: leave them out. The guardian stands 2 m behind the Bat for the 10 s.
   - Its attacks are the summon's own choices (a random enemy within 32 m, from 4 s after the summon, every 2.5 s), not
     part of the skill's timeline, and the skill has no target.
   - If the user wants them, a part can play one attack on the 10 m point at 4 s after the summon (5.0 s into bigCast3)
     and every 2.5 s. Each attack: a fade-out, a reappearance 6 m before the target, nAttack + Shade4 nAttack sound +
     guardianBlade, Shade4 nAttack_hit at the target, and a fade-back. The spec is in the Guardian section.
3. **The guardian's end at the 10 s cut.**
   - Recommended: the game's own unsummon at 10 s (ko once, gone at 12 s): `{"d": -4, "unsummon": 10, "kill": 12}`.
   - The alternative is a plain `kill: 10`, where it vanishes mid-pose.
   - guardian_ring goes at 10 s either way (the status's end).
4. **Black Servant's body.**
   - Recommended: a Bat-sized body, so the servant ring sits at y 1.75 with scale 0.7 (the own-class body, as the
     Penguin's decision 3).
   - The alternative is the floor (y 0), which matches no class.
5. **Auto Mass's flash.**
   - Recommended: on, at 12 %, on the 11 cast3 skills (passives on), even though BB draws it only once Mass Cast has
     been cast in the session. This is the same call the Penguin's multiCast got (its decision 9).
6. **Auto Mass's purple hero tint** (massCast status, 3 s, CharacterControl.cs:40037-40044).
   - Recommended: leave it out, as the Penguin's multiCast tint (its decision 10).
7. **castRing's root clip** (optional part 3).
   - Recommended: build it. It is cheap and shows in the three bigCast tiles for about 0.25 s.
8. **The 205 blend** (Read this first, item 1).
   - Recommended: build it before any Bat cue is checked. Without it every Bat shadow effect glows white-pink instead
     of darkening, and the QA would judge the wrong look.

## Verification

Checker, 2026-11-13 (home PC), read only against `D:\12tails\DecompiledSource` (Bat.cs, Bat_guardianOfTheNight.cs,
AudioControl.cs, CharacterControl.cs), the TTO pseudo-C, the rip, the probes in `checks/fx_bat_research/skills_a/`,
`wardrobe/data/bat/clips.json`, `wardrobe/index.html` and `pipeline/wardrobe_fx.py`. Every state machine below was
re-traced case by case (which label each case jumps to, which `Yield` that label returns).

**Confirmed as written:** RPC_cast1 0 / 0.2 / 0.5 / 0.7 (start -> IL_3941 `Yield(2, 0.2)` :25021; case 2 -> Block_296
`Yield(3, 0.3)` :25019; case 3 -> IL_3990 `Yield(4, 0.2)` :25023), cast1 with a 0.2 fade (:24821), the voice pick
(:24862), castRing at the hero, `Euler(270, 90, 0)` (:23028), cast2 cut + looped and the ring's root at 0.7 (:23092-23107);
castRing EffectControl life 60 / afterLife 0 / followState, AudioSource cast_ring (probe.json); the Auto Mass roll
(:23247-23360: #431, no massCast status, `Random.Range(0, 100) < lckAdjust(12)` = 12 % at LCK 1 by
CharacterControl.cs:20658-20670, the 11 skills, the flash only if the field was loaded). The three bigCast channels:
0 / 0.2 / 0.7 / 1.0 in each (Guardian: start -> Block_61 -> IL_296 `Yield(2, 0.2)`, case 2 -> IL_586 `Yield(3, 0.5)`,
case 3 -> IL_696 `Yield(4, 0.3)`; Nefarious Whip and Black Servant the same constants, :43228-43237, :44669-44675),
castRing 0.1 m behind by createEffect (:29933, :42829, :44288), bigCast_ring at bigCast2's start (:30038, :42934,
:44393), the bars (:30052, :42948, :44407) and magAdjust's 0.1 s floor (CharacterControl.cs:20584-20588); bigCast2 changes
neither actionState nor myCommand, so both rings end at the release. The releases: Guardian 0 / 0.5 / 1.0 / 2.0 (start ->
IL_86D `Yield(2, 0.5)`, case 2 -> Block_26 `Yield(3, 0.5)`, case 3 -> IL_241 `Yield(4, 1)`), castEffect at
TransformDirection(0, 1.8, 1) (:30504), the guardian at `position - 4 x transform.forward` with the hero's rotation
(:30561), its Init glide `Lerp(owner - 4 fwd, owner - 2 fwd, t)` and the 0 -> 0.8 / 0 -> 1 fades
(Bat_guardianOfTheNight.cs:283-470), unsummon = `ko` then Destroy 2 s later (:1998-2121), guardian_ring by the status at
the hero, identity, parented (CharacterControl.cs:40541-40564), the 4 s first AI scan (:30614); Nefarious Whip 0 / 0.5 /
0.9 / 1.3 with nefariousWhip_hit at the target's feet at once (:44025-44037, before the first `Yield(2, 0.5)` of
RPC_nefariousWhip_hit) and AudioControl {0, 1, 0.5, 0.5, 4, 0.2} (probe2.json; AudioControl.cs: with delay > 0 it turns
playOnAwake off and Stops, then Plays in the fade-in); Black Servant 0 / 0.5 / 0.9 / 1.3, blackServant_ring at the
target's position and rotation (:44929), the status (:45206), the servant ring at `bounds.center + up x extents.y`,
scale `Clamp(radius + 0.4, 0.5, 2)` (CharacterControl.cs:41379-41395). Voices: one random pick each where claimed
(:30741, :43649), blackServant a single file (:45381; TTO the same, pseudo/Bat.c:1065). The two script layouts
(Bat_guardianOfTheNight.cs:169-175; AudioControl.cs:233-248) and the 205 ids (probe_shader_ids.txt). poolChains
(index.html:1238-1262) makes `@GuardianOfTheNight`, `@NefariousWhip`, `@BlackServant` and hides the host
`@GuardianoftheNight`; no clash. cues.json parses.

**Corrections**

1. `plans/fx_bat/skills_a.md:162-166, :175, :178` (bigCast1's castRing, `cut: 0.95`): the game ends the ring at the
   release, which comes at the **bar's end**, not at bigCast2's start (myCommand changes only in RPC_<skill>_cast, :30697,
   :43605, :45331; bigCast2's case 4 sets neither actionState nor myCommand, :29981-30123). With the proposed
   `bigCast1@1 bigCast2*@0.1` that is 1.1 s, so `cut: 0.95` ends it 0.15 s early. castRing has afterLife 0 (probe.json),
   so the game's followState end is a Destroy the next frame (EffectControl.cs:179-183), and a `kill` (counted from the
   spawn, not the step clock, index.html Fx.update) crosses the step edge a cut cannot: **`kill: 0.9`** (1.1 - 0.2). (Without
   the SEQ change: release at 1.033, `kill: 0.833`.) cast1's `cut: 0.65` is only 0.05 s early (cast3 at 0.7 with a 0 bar)
   and can stay, as the Sheep's and the Penguin's.
2. `plans/fx_bat/skills_a.md:336-337, :345, :350, :473-476` (Black Servant's ring at y 1.75): decisions.md 3 of the
   Penguin is not an "own-class body" rule; it fixes the target's centre at 0.6 m up **for every class** (the Penguin's
   CharacterController: centre 0.6, height 1, radius 0.3, Penguin.prefab:683-689). Every other target cue in the Bat's
   reports already uses that body (the drain bolt's `to [0, 0.6, 10]`, drainLife_hit and dreamBurst_hit 0.6 up). A
   Bat-sized corpse (centre 0.9, height 1.7, Bat.prefab:905-911) would be the only target of that size. The same body
   gives the collider's top at 0.6 + 0.5 = **y 1.1**, scale Clamp(0.3 + 0.4, 0.5, 2) = 0.7 (unchanged). (If the user wants
   a Bat-sized corpse, 1.75 stands, but then the 0.6 m aims would need 0.9 too.)
3. `plans/fx_bat/skills_a.md:266, :386-389` (the guardian's own sound): the guardian's AudioSource clip `guardian_ring` is
   not in the Bat's `sounds/`: the rip has it only as `gameassets/characters/elementals/shade4/sounds/guardian_ring.wav`
   (the summon is the Shade4 model). It still builds: an effect's own sound falls back to a search of the whole rip
   (wardrobe_fx.py:353-358). Only the text changes ("Effects' own sounds (`sounds/`): ... guardian_ring" is wrong).
4. `plans/fx_bat/skills_a.md:357-362`: the bigCast3 pool block holds `{...}` placeholders, so it is not paste-ready by
   itself; the whole entry is below (and in checks/fx_bat_research/skills_a/cues.json, which predates corrections 1-3).

**Corrected paste-ready blocks** (replace `bigCast1` and `bigCast3`; `cast1` and `bigCast2` stand as written; parsed as
JSON):

```json
  "bigCast1": {
    "why": "The channel of the three bigCast skills, the same in each (Bat.cs RPC_guardianOfTheNight :29768-30311, RPC_nefariousWhip :42675-43239, RPC_blackServant :44569-44688; TTO1102's three load the same names): at 0: actionState attack and myCommand guardianOfTheNight1 / nefariousWhip1 / blackServant (:30191-30197, :43029-43039, :44570-44576), clip bigCast1 (0.2 fade, :30209, :43059, :44588) and voice bigCast (one file; :30256 + :30306, :43116 + :43222, :44635 + :44682); Yield 0.2 (:30298, :43230, :44669): castRing 0.1 m behind the hero, TransformDirection(0, 0, -0.1), Quaternion.Euler(270, 90, 0) world-absolute, by createEffect (InitEffectControl, CharacterControl.cs:24191-24210) (:29933, :42829, :44288); Yield 0.5 (:30302, :43237, :44671): the ring's root clip looped at 0.7 s (:29968-29973, :42864-42869, :44323-44328); Yield 0.3 (:30304, :43228, :44675): bigCast2 cut in and looped at 1.0 s (:30000-30005, :42896-42901, :44355-44360; bigCast2's entry has the rest); the release RPC_<skill>_cast sets myCommand guardianOfTheNight2 / nefariousWhip2 / blackServant2 (:30697, :43605, :45331): the ring's followState cut there, at the bar's end, not at bigCast2's start (EffectControl.cs:194-247; afterLife 0: destroyed at once, :179-183): with the SEQ's bigCast1@1 bigCast2*@0.1 that is 1.1 s, 0.9 s after the spawn: kill 0.9 (a kill counts from the spawn, so it crosses the step edge a cut cannot; afterLife 0 makes it the game's end exactly)",
    "cues": [
    [0, "voice", "bigCast"],
    [0.2, "fx", "castRing", {"d": -0.1, "rot": [270, 90, 0], "kill": 0.9}]
    ]
  },
  "bigCast3": {
    "why": "The bigCast3 clip is the release of three Bat skills after the bigCast1 / bigCast2 channel (Bat.cs RPC_guardianOfTheNight_cast :30700, RPC_nefariousWhip_cast :43608, RPC_blackServant_cast :45334, each PlayAnimation(bigCast3, 0.2)): one tile each (poolChains, with the Guardian of the Night sequence's steps)",
    "skills": {
      "guardianOfTheNight": {
        "why": "Bat.cs RPC_guardianOfTheNight_cast (:30362-30841; started when the bar ends, :30155-30176), no target: at 0: myCommand guardianOfTheNight2 (:30697), clip bigCast3 (0.2 fade, :30700), voice guardianOfTheNight1 / guardianOfTheNight2 (Random.Range(0, 2) :30741, :30751, :30782, PlayOneShot :30825-30828; the rip's files are voices/guardianOftheNight1 / 2.wav: Resources.Load and Windows paths are case-blind); Yield 0.5 (:30837): castEffect 1.8 m up 1 m ahead, TransformDirection(0, 1.8, 1), hero rotation (:30504; the hero prefab's castEffect field = bat/effects/castEffect; plays its own Sounds/cast_effect); Yield 0.5 (:30821): at 1.0 s the guardian, Resources bat/effects/guardian, 4 m behind the hero (position - 4 x transform.forward, hero rotation, :30549-30561), Bat_guardianOfTheNight.Init(hero, sLv 2) (:30586; walk looped, glides from 4 to 2 m behind in 1 s while its two materials fade in, alpha 0 to 0.8 / 0 to 1, then standby and root, Bat_guardianOfTheNight.cs:283-470, :32-98; plays its own looping guardian_ring, a Shade4 clip: Resources gameassets/characters/elementals/shade4/sounds/guardian_ring.wav), and the guardianOfTheNight status for chaAdjust(30 x 2), 60 s or more (:30592-30603), whose apply puts Effects/guardian_ring at the hero, identity, parented (CharacterControl.cs:40541-40564); both last until the status ends (the summon's ko clip then gone 2 s later, Bat.cs:12436-12442, Bat_guardianOfTheNight.cs:1998-2121): cut at 10 s (unsummon 10, kill 12; guardian_ring kill 10); its AI (first scan 4 s after the summon, then every 2.5 s, Bat.cs:12275-12445, :30614) finds no enemy here: no attacks; Yield 1 (:30816): standby at 2.0 s (:30641)",
        "cues": [
        [0, "voice", "guardianOfTheNight1|guardianOfTheNight2"],
        [0.5, "fx", "castEffect", {"d": 1, "y": 1.8}],
        [1.0, "fx", "guardian", {"d": -4, "unsummon": 10, "kill": 12}],
        [1.0, "fx", "guardian_ring", {"kill": 10}]
        ]
      },
      "nefariousWhip": {
        "why": "Bat.cs RPC_nefariousWhip_cast (:43287-43745; started when the bar ends, :43187-43208; enemy target: the 10 m target point): at 0: myCommand nefariousWhip2 (:43605), clip bigCast3 (0.2 fade, :43608), voice nefariousWhip1 / nefariousWhip2 (Random.Range(0, 2) :43649, :43659, :43690, PlayOneShot :43726, :43742); Yield 0.5 (:43734): castEffect TransformDirection(0, 1.8, 1), hero rotation (:43429), and RPC_nefariousWhip_hit on the target while it lives (:43482), which at once puts nefariousWhip_hit at the target's position with the Bat's rotation (:44025-44037; EffectControl life 5 + afterLife 5; its own looping Sounds/nefariousWhip under an AudioControl: 0.5 s delay, 0.5 s fade-in, 4 s, 0.2 s fade-out, then silent), then 8 damage ticks 0.5 s apart within 4 m of it (:43918-43957, :44060-44075; nothing drawn); Yield 0.4 (:43729): moveSpeed 0 (:43522); Yield 0.4 (:43738): standby at 1.3 s (:43549)",
        "cues": [
        [0, "voice", "nefariousWhip1|nefariousWhip2"],
        [0.5, "fx", "castEffect", {"d": 1, "y": 1.8}],
        [0.5, "fx", "nefariousWhip_hit", {"d": 10}]
        ]
      },
      "blackServant": {
        "why": "Bat.cs RPC_blackServant_cast (:44732-45441; started when the bar ends, :44534-44555; target: a dead enemy player, Bat.cs:8468-8511: the 10 m target point): at 0: myCommand blackServant2 (:45331), clip bigCast3 (0.2 fade, :45334), voice blackServant (one file, :45381, PlayOneShot :45433; voices/blackServant1 / 2.wav are never loaded); Yield 0.5 (:45429): castEffect TransformDirection(0, 1.8, 1), hero rotation (:44878), blackServant_ring at the target's position with the target's rotation (:44911-44929; the target faces the hero: rot [0, 180, 0], plans/fx_penguin/decisions.md 4), the Shadow<Class>_AI (:44943-45169) and the blackServant status for getDebuff(90) (:45206), whose apply raises the body (hp and ko to half, standby, grey tint 0.35: no body on the page) and puts Effects/blackServant on top of its collider, collider.bounds.center + up x extents.y, identity, parented, scale Clamp(radius + 0.4, 0.5, 2) (CharacterControl.cs:41338-41413): the standing target body of every target-point cue (plans/fx_penguin/decisions.md 3: the CharacterController centre 0.6 m up, the Penguin's, Penguin.prefab:683-689: height 1, radius 0.3): top at 0.6 + 0.5 = 1.1 m, scale Clamp(0.3 + 0.4, 0.5, 2) = 0.7, no EffectControl: it lasts the status, cut at 10 s (kill 10); Yield 0.4 (:45414): moveSpeed 0 (:45243); Yield 0.4 (:45438): standby at 1.3 s (:45275)",
        "cues": [
        [0, "voice", "blackServant"],
        [0.5, "fx", "castEffect", {"d": 1, "y": 1.8}],
        [0.5, "fx", "blackServant_ring", {"d": 10, "rot": [0, 180, 0]}],
        [0.5, "fx", "blackServant", {"d": 10, "y": 1.1, "scale": 0.7, "kill": 10}]
        ]
      }
    }
  }
```
