# Wolf effects research: powerBreak, provoke, resurrection, thirdRend, twinResonance, feralAssault

Research only (2026-11-09). Source: `D:\12tails\DecompiledSource\Wolf.cs` (BB) unless named. All six clips are **BB's
own**: each is played by an `RPC_<skill>` coroutine in BB's `Wolf.cs`, and `wardrobe/data/wolf/clips.json` has them in
group `skill` with `tto: false`. Clip lengths (clips.json): powerBreak 1.2, provoke 1.1, resurrection 2.0, thirdRend 1.4,
twinResonance 3.0, feralAssault 2.6 s. Every proposed cue time falls inside its clip.

| Clip | Skill (reference) | Coroutine | Ranks |
|---|---|---|---|
| powerBreak | Power Break `wlf_powerBreak1-2` (#221/223) | `RPC_powerBreak` (:8523, body `$RPC_powerBreak$29386` :21744) | 2, max = 2 |
| provoke | Provoke `wlf_provoke1-2` (#321/322) | `RPC_provoke` (:8707, body :26760) | 2 (rank changes only duration / hate) |
| resurrection | Mass Resurrection (`massResurrection`) | `RPC_massResurrection` (:8648, body :24835) | 2 (rank changes only revive chance) |
| thirdRend | Third Rend `wlf_thirdRend5` (#422, Class C) | `RPC_thirdRend` (:9134, body :32087) | 1 |
| feralAssault | Feral Assault `wlf_feralAssault5` (#443, Class C) | `RPC_feralAssault` (:9255, body :35072) | 1 |
| twinResonance | Twin Resonance `wlf_twinResonance5` (#444, Class C) | `RPC_twinResonance` (:9398, body :36967) + `RPC_twinResonance_fire` (:9405, body :37425) | 1 |

Prefab facts below come from a read-only in-memory probe (`checks/fx_wolf_research/misc/probe.py`: imports
`wardrobe_fx.Game` / `effect`, prints the node tree, EffectControl and AudioSource; writes nothing; a dummy 17-float
layout for EmblemEmitter so the probe can read the resurrection prefabs' EffectControl).

---

## powerBreak (Power Break)

Flow (`RPC_powerBreak`): at 0 the clip (`PlayAnimation("powerBreak", 0)` :22114), voice `powerBreak1` or `powerBreak2`
(`Random.Range(0, 2) == 0`, :22155-22210), then the effect **picked by rank** (:22223): `sLv == 1` -> `powerBreak1`
(:22233-22243), else `powerBreak2` (:22268-22278); both `createEffect` at the hero's position + rotation. Max rank 2 ->
`powerBreak2`. Then `Yield(2, 0.5)` (:22317) -> case 2: dash `moveSpeed = 6` (:21891) -> `Yield(3, 0.2)` (:22315) ->
case 3: stop, the hit box (:21918-22008) -> `Yield(4, 0.3)` (:22308) -> case 4: `actionState = "standby"` (:22032) at
**1.0 s**.

`powerBreak2`: EffectControl life 1.0, afterLife 1.0, followPosition, **followState** -> 5th value 1.0 (the standby);
its own sound `powerBreak` (AudioSource). Inventory: **ready**. (`powerBreak1` is ready too, not used: rank 1.)

Left out: the hit sparks `RPC_nAttack_hit` at the target (:21975).

```json
  "powerBreak": {
    "why": "Wolf.cs RPC_powerBreak: clip, voice powerBreak1 / 2 (:22114-22210) and the effect picked by rank at once (sLv 1 = powerBreak1, else powerBreak2: max rank 2 = powerBreak2, at the hero, :22223-22278); 0.5 s, a 0.2 s dash (:21891), the hit (:21936), 0.3 s, standby at 1.0 s (:22032), which ends powerBreak2 (EffectControl followState: the 5th value); left out: the hit sparks at the target (RPC_nAttack_hit :21975)",
    "cues": [
    [0, "voice", "powerBreak1|powerBreak2"],
    [0, "fx", "powerBreak2", 0, 1.0]
    ]
  }
```

Sure: high.

## provoke (Provoke)

Flow (`RPC_provoke`): the game needs a target: `tID == 0` ends the coroutine before anything plays (:26965-26969). At 0
the clip (`PlayAnimation("provoke", 0.2f)` :27033) and voice `provoke1` or `provoke2` (:27082-27137);
`mProvokeTime = Time.time + 0.8f` (:27150); every frame the hero turns to the target (:27221-27227, `YieldDefault(2)`
:27248) until 0.8 s, then `RPC_AddStatus("provoke", ...)` on the target (:27186). **No effect in the coroutine.** The
only effect, `Effects/provoke`, is created by the provoke status handler **on the provoked enemy**
(`CharacterControl.cs:34082-34098`, `self.createEffect(mProvoke, self.mTransform.position, ...)` where self = the
holder). Its parts (EllipsoidParticleEmitter + 2 RingEmitters, sound `provoke`) look buildable, but it is not in
`fx_inventory.md` (the inventory scans `Wolf.cs` only).

Left out: `provoke` (on the enemy, 0.8 s in). It is an on-enemy status mark, not a skill effect that needs a target
point to exist, so the 10 m exception does not apply in my reading. If the user wants it anyway: `[0.8, "fx", "provoke", 10]`.

```json
  "provoke": {
    "why": "RPC_provoke: clip, voice provoke1 / 2 (:27033-27137) at 0; no effect in the coroutine; left out: the provoke effect, made by the provoke status on the provoked enemy 0.8 s in (mProvokeTime :27150, RPC_AddStatus :27186, CharacterControl.cs:34082-34098)",
    "cues": [
    [0, "voice", "provoke1|provoke2"]
    ]
  }
```

Sure: high (voice); medium on reading the 10 m exception as not covering this effect.

## resurrection (Mass Resurrection)

Flow (`RPC_massResurrection`): at 0 the clip (`PlayAnimation("resurrection", 0.2f)` :25275), voice `resurrection1` or
`resurrection2` (:25316-25371), `resurrection_ring` `createEffect` at the hero (:25390-25400). `Yield(2, 0.8)` (:25434)
-> case 2: camera motion blur, own player only (:24990-24995) -> `Yield(3, 0.4)` (:25430) -> case 3: area search r 40
(:25027), `resurrection_hit` on each dead ally revived (:25114-25126), `ReviveEvent` (:25157) -> `Yield(4, 0.6)`
(:25436) -> standby at 1.8 s (:25193). No rank pick of effects.

`resurrection_ring`: **needs EmblemEmitter** (one node `EmblemEmitter` at y 2.6; the other 7 nodes are Image / Line /
Ring emitters). EffectControl life 2, afterLife 1, followPosition, no followState; carries the sound `resurrection`
(2.0 s), which is lost while the ring is left out. `resurrection_hit`: needs EmblemEmitter, and is at the target anyway.

```json
  "resurrection": {
    "why": "RPC_massResurrection: clip resurrection, voice resurrection1 / 2 (:25275-25371) at 0; left out: resurrection_ring (at the hero at 0, :25390-25400) needs EmblemEmitter (its sound resurrection comes with it); resurrection_hit on each revived ally 1.2 s in (:25114-25126, at the target; needs EmblemEmitter); the camera motion blur at 0.8 s (:24990-24995) is not an effect prefab; standby at 1.8 s (:25193)",
    "cues": [
    [0, "voice", "resurrection1|resurrection2"]
    ]
  }
```

When EmblemEmitter is built, add `[0, "fx", "resurrection_ring"]` (no 5th value: no followState). Sure: high.

## thirdRend (Third Rend)

Flow (`RPC_thirdRend`): at 0 the clip (`PlayAnimation("thirdRend", 0.1f)` :32544), voice `thirdRend1` or `thirdRend2`
(:32585-32640), `thirdRend_ring` `createEffect` at the hero (:32659-32669). Then `Yield(2, 0.2)` (:32714) -> step
`moveSpeed 3` (:32223) -> 0.2 (:32716) -> `moveSpeed 2` (:32250) -> 0.1 (:32708) -> `moveSpeed 3` (:32277) -> 0.1
(:32698) -> hit box at 0.6 s (:32317-32382) -> 0.3 (:32712) -> `moveSpeed 1` (:32416) -> 0.1 (:32704) -> stop +
standby at **1.0 s** (:32443-32460).

`thirdRend_ring`: EffectControl life 1, afterLife 1, no followPosition, no followState; its own sound `thirdRend`.
Inventory: **ready**. (Its slash rings sit 1 and 2 m ahead inside the prefab, so distance 0 is right.)

Left out: hit sparks `RPC_nAttack_hit` at the target (:32377).

```json
  "thirdRend": {
    "why": "RPC_thirdRend: clip, voice thirdRend1 / 2 (:32544-32640) and thirdRend_ring at the hero (:32659-32669) at 0; the step-in 0.2-1.0 s (moveSpeed 3 / 2 / 3 / 1, :32223-32416), the hit at 0.6 s (:32317), standby at 1.0 s (:32460; thirdRend_ring has no followState); left out: the hit sparks at the target (RPC_nAttack_hit :32377)",
    "cues": [
    [0, "voice", "thirdRend1|thirdRend2"],
    [0, "fx", "thirdRend_ring"]
    ]
  }
```

Sure: high.

## feralAssault (Feral Assault)

Flow (`RPC_feralAssault`): at 0 the clip (`PlayAnimation("feralAssault", 0)` :35432) and `feralAssault_ring1`
**`Object.Instantiate`** at the hero (:35463-35475). **No voice:** the coroutine loads none and `Wolf.cs` has no
`Voices/feralAssault*` (the three rings carry their own sounds `feralAssualt_ring1-3`, the game's spelling). `Yield(2,
0.9)` (:35702) -> case 2 at 0.9 s: dash `moveSpeed = floor(14 / clamp(moveMod))` (:35208), `feralAssault_ring2`
`createEffect` at the hero (:35219-35231), camera motion blur (:35266-35271), i = 0 -> `IL_C19` (:35498): i < 4 = a hit
box (:35633-35673, `RPC_feralStrike_hit` at each target) then `Yield(3, 0.3)` (:35696), case 3 `i++` (:35306): hits at
0.9 / 1.2 / 1.5 / 1.8 s. At i = 4 (**2.1 s**): stop (:35503), `feralAssault_ring3` `Object.Instantiate` at the hero's
spot (:35515-35527), the r 6 finisher (:35547-35587, `RPC_feralAssault_hit` at targets), white camera flash
(:35592-35603); `Yield(4, 0.3)` (:35698) -> standby at **2.4 s** (:35333).

Effects (all **ready** in the inventory):
- `feralAssault_ring1`: EffectControl life 1, afterLife 1, **followState** (no followPosition). Instantiated, so
  `InitEffectControl` never runs (only `CharacterControl.createEffect`, `CharacterControl.cs:24191-24200`, gives the
  owner). In `EffectControl.Update` a followState effect with no owner jumps straight to its after-life on its first
  frame (`EffectControl.cs:194-200`: `if (!owner) time = life`). So in the game it is cut at once: it is destroyed
  1.0 s after it spawns, not 2.0 s (its LineEmitter1/2, Delay 0.9 + Life 0.4, show only 0.1 s). The 5th value **0**
  does exactly this on the page (`cut: c[4]` is kept as 0, `index.html:3225`; the test is `cutAt != null`, `:2990`).
- `feralAssault_ring2`: createEffect (owner = hero), life 1.2, afterLife 0, followPosition, followState. Spawned at
  0.9, so its life ends at 2.1, before the standby at 2.4. The 5th value 2.4 is faithful but changes nothing.
- `feralAssault_ring3`: life 1, afterLife 1, no follow flags. In the game it spawns where the dash ended (nominally
  16.8 m from the cast point, reference `wlf_feralAssault5`); the wardrobe hero does not travel, so distance 0 puts it
  at the hero, as the Feral Strike pilot did with its dash effect.

Left out: `feralStrike_hit` / `feralAssault_hit` at the targets (:35668, :35582); the camera motion blur and white flash
(not effect prefabs).

```json
  "feralAssault": {
    "why": "RPC_feralAssault: clip (:35432), no voice in BB (the rings carry the sounds); feralAssault_ring1 Instantiated at the hero at 0 (:35463-35475): no EffectControl owner, so its followState cuts it at once (EffectControl.cs:194-200): 5th value 0; 0.9 s standing (:35702), then the dash with feralAssault_ring2 at the hero (createEffect, followState, :35208-35231); four hits 0.3 s apart (:35498-35696); at 2.1 s the stop and feralAssault_ring3 at the hero's spot (Instantiate, :35503-35527; 0 m: the wardrobe hero doesn't travel); standby at 2.4 s (:35333); left out: the hits at the targets (feralStrike_hit :35668, feralAssault_hit :35582), the camera blur and flash (:35266, :35603)",
    "cues": [
    [0, "fx", "feralAssault_ring1", 0, 0],
    [0.9, "fx", "feralAssault_ring2", 0, 2.4],
    [2.1, "fx", "feralAssault_ring3"]
    ]
  }
```

Sure: high on the times and the ownerless cut (read in `EffectControl.cs` and `CharacterControl.createEffect`);
medium-high on distance 0 for ring3 (a wardrobe choice, not the game's spot).

## twinResonance (Twin Resonance)

Flow (`RPC_twinResonance`): at 0 the clip (`PlayAnimation("twinResonance", 0.1f)` :37228), voice `twinResonance1` or
`twinResonance2` (:37269-37324), `twinResonance_ring` `Object.Instantiate` at the hero (:37343-37353). `Yield(2, 2f)`
(:37391) -> case 2 at **2.0 s**: starts `RPC_twinResonance_fire(transform.position, transform.forward)` (:37110; other
clients via `ActionEvent` :37115) and a camera motion blur (:37120-37125) -> `Yield(3, 0.8)` (:37389) -> standby at
2.8 s (:37146).

`RPC_twinResonance_fire` (:37425): at once `twinResonance_fire` `Object.Instantiate` at the hero's position, rotation
`LookRotation(forward)` (:37590-37602), then 40 ticks 0.4 s apart (:37622, :37714), each a 190-degree cone hit of radius
0.8 i + 3 (:37644; `twinResonance_hit` at targets, :37690); destroyed early only if the hero dies or is KO'd
(:37543-37566). BB = 40 x 0.4 s; the Bible's 150 x 0.178 s variant (`index.html:19684`) is a server swap, not BB.

Effects (both **ready**):
- `twinResonance_ring`: life 3, afterLife 1, no follow flags; its sound `twinResonance_ring` (3.0 s).
- `twinResonance_fire`: life 16, afterLife 1, no follow flags; its sound `twinResonance_fire` (1.99 s) is an
  AudioSource with **loop: true** (looped about 17 s in the game).

```json
  "twinResonance": {
    "why": "RPC_twinResonance: clip, voice twinResonance1 / 2 (:37228-37324) and twinResonance_ring Instantiated at the hero (:37343-37353) at 0; 2 s (:37391), then RPC_twinResonance_fire (:37110): twinResonance_fire Instantiated at the hero facing forward (:37590-37602), 40 ticks x 0.4 s (:37622, :37714; its EffectControl life 16); standby at 2.8 s (:37146); no followState on either; left out: twinResonance_hit at the targets (:37690), the camera blur (:37120-37125)",
    "cues": [
    [0, "voice", "twinResonance1|twinResonance2"],
    [0, "fx", "twinResonance_ring"],
    [2.0, "fx", "twinResonance_fire"]
    ]
  }
```

Sure: high on the cues. Two page things for the editor to check (not cue matters): the page's `Sound.play` plays an
AudioSource once and ignores `loop`, so the fire's sound plays 2 s, not the game's 16-17 s (`index.html` Fx constructor,
`c.type === "AudioSource"`). The fire also outlives the 3.0 s clip by about 15 s: check what the page does with a live
effect when the clip ends or the move changes.

---

## Recipe problems hit

1. **Ownerless followState (step 1.5).** The recipe says followState effects end when the hero's action changes, but
   an effect spawned by `Object.Instantiate` (not `createEffect`) has no owner, and `EffectControl.Update` then cuts
   it on its first frame (`EffectControl.cs:194-200`). The cue needs a 5th value of 0 for those (`feralAssault_ring1`
   here). The pilot's note ("Instantiate, so no EffectControl owner") hints at the owner but not at this effect. Add:
   "Instantiate + followState = 5th value 0".
2. **Reading followState without writing data.** Step 1.5 points at `wardrobe_fx.py --fx <name>`, which writes the
   shared `fx.json`; a research agent may not run it. `wardrobe_fx.effect()` also raises on any component without a
   layout (EmblemEmitter), so the EffectControl of an unbuildable prefab can't be read either. A read-only
   `--probe` (print the tree, no writes, unknown scripts skipped) would serve both cases.
3. **The inventory only covers `<Class>.cs`.** Effects a skill's status makes in `CharacterControl.cs` (Provoke's
   `provoke`) aren't listed, so step 2 can't answer for them.
4. **Effects after a dash.** Nothing says whether an effect spawned at the hero after the game moved them (Feral
   Assault's ring3 at about 16.8 m) goes at 0 (where the wardrobe hero stands) or at the game's distance. I used 0,
   as Feral Strike did.
5. **Camera effects** (`CameraEffect.AddMotionBlur` / `AddColorRamp`: Mass Resurrection, Feral Assault, Twin
   Resonance) aren't mentioned; I left them out as not effect prefabs. A line in the recipe would settle it.
6. **Reading the flow.** `clip_flow.js` lists the matching lines in source order, not in run order. The order comes
   from the `goto IL_x` -> `IL_x: return this.Yield(n, ...)` labels at the end of `MoveNext`, which you read by hand.
   The opaque `if (123 - 456 != -333) continue;` guards make that harder. Stripping them (`grep -Ev 'if \([0-9]+ -
   [0-9]+ [!=]= -?[0-9]+\)'` and blank / brace lines) made each coroutine readable in one screen. Worth a tip in step
   1.3, or an option in `clip_flow.js`.
7. **Page gaps the recipe doesn't name:** a looping AudioSource (`loop: true`) plays once, and nothing says how
   effects that outlive the clip (Twin Resonance's 16 s fire) should behave.
