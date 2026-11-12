# Bison effects + sounds research: skills_a (nine skill clips)

Researcher `skills_a`, 2026-11-13 (home PC). Scope: the clips calamityHammer, cleave, earthRupture, earthSmasher,
enrage, farStun, instantRush, knockDown, magmaClutter and every skill that plays them. Research only (recipe steps 1-3).
Line numbers are `D:\12tails\DecompiledSource\Bison.cs` unless another file is named. Times are seconds from the start
of the clip the cue is keyed by. Distance 0 = at the hero; x = metres to the hero's right (Unity +x, as the Penguin's
Ice Block cues).

Read-only probes, in `checks\fx_bison_research\skills_a\` (nothing there writes outside that folder):
- `cond.py <file> <from> <to>`: a line range with every opaque predicate `if (a - b op c)` worked out (TRUE / FALSE);
  `f.sh` drops the junk lines. Its outputs: `enrage.txt`, `knockDown.txt`, `farStun.txt`, `instantRush.txt`,
  `powerCleave.txt`, `earthRupture.txt`, `earthSmasher.txt`, `magmaClutter.txt`, `calamityHammer.txt`,
  `calamity_fire.txt` (OnCalamityHammer + RPC_calamityHammer_fire).
- `probe\probe.json` / `probe_all.json`: `wardrobe_fx.py bison --probe` of the 25 effects these skills load;
  `probe\summ.py` -> `probe\summary.txt` (per node: EffectControl, AudioSource, emitter Life / Delay, unknown parts).
- `probe_tto\probe.json`: `wardrobe_fx_tto.py bison --probe magmaClutter_ring2,earthRupture` (TTO's copies).
- `entries.py` -> `entries.json`: the cue entries below, JSON-checked.

Max rank and passives on: Enrage 4 + Rage Control #402, Knock Down 4 + Aftershock #422, Far Stun 2 + Mass Stun #442,
Instant Rush 1, Power Cleave 2 + Power Reel #403 + Power Hammer 2 (#304; counts only with a hammer worn), Earth Rupture 2,
Earth Smasher 2, Magma Clutter 5, Calamity Hammer 5 (`12t_reference/bison-skill-reference.md`).

---

## Read this first

1. **No pools.** Each of the nine clips has exactly one `PlayAnimation` call in BB (`:21064, :23278, :23947, :24367,
   :26252, :28739, :29390, :31724, :32273`; `checks\fx_bison_research\skills_b\clip_calls.txt` agrees), each from its
   own skill's coroutine. In TTO (`pseudo/Bison.c`) the clip names appear only in the same nine coroutines; the
   `'calamityHammer'` string in `RPC_magmaQuake` (TTO Magma Quake) is the axe version's **voice** name
   (`pseudo/Bison.c:7695-7700`; the clip is `magmaQuakeAxe` for both weapons), not a clip call. So every entry is a plain
   `{why, cues}` keyed by its clip; no SEQ line and no SEQ_SKILL entry is needed (each plays as a single-clip tile).
   `cleave` is Power Cleave; Power Hammer (#302 / #304) is a passive that changes it (no tile of its own).
2. **Missing part P1: `Bison_earthRupture`** (inventory: "earthRupture needs Bison_earthRupture"). The wave prefab's
   root has ProjectileControl (velocity (0, 0, 12), life 0 in the prefab) + Bison_earthRupture and **no
   EffectControl** (probe). `Bison_earthRupture.FixedUpdate` (Bison_earthRupture.cs:96-127): clock += dt; Destroy at
   `ProjectileControl.life`, which the hero's code sets to **2** (`RPC_earthRupture_fire2` :8892); else
   `rigidbody.velocity = TransformDirection(ProjectileControl.velocity)` every step (12 m/s along its own forward,
   constant). `OnCollisionEnter` (:131-190) only calls `hit()` on Player / Enemy tags after `IgnoreCollision`: the wave
   passes through everything, the 10 m target too, and the floor never stops it (sphere collider radius 1 centred 1 m
   up on a root 0.2 m up). The part is `fxparts/sheep.js`'s mover with `LIFE = 2`, no own velocity, no floor stop:
   a `fxparts/bison.js` registering `Bison_earthRupture`. The Destroy takes the legacy particles with it (no
   after-life). Until it exists the waves stand at the spawn point.
3. **Missing part P2: magmaClutter_ring2's Shuriken.** Its `TrailEmitter` node also carries a ParticleSystem (class 198)
   + ParticleSystemRenderer (199) + MeshFilter / MeshRenderer (the rip's prefab, lines 175-1270); `wardrobe_fx.py`
   doesn't decode BB's Shuriken and drops them silently (the probe shows only the TrailEmitter). TTO's client copy
   reads whole (`probe_tto`: EffectControl life 1 + afterLife 0.5, followPosition, followState, AudioSource
   magmaClutter2, the ParticleSystem with material `tto_Bomb2` and the TrailEmitter), so the cue names
   **`tto/magmaClutter_ring2`**, built by `wardrobe_fx_tto.py bison` (it builds every `tto/<prefab>` fx cue), as the
   weapons' 15 Shuriken effects were (NOTES.md 2026-11-12, `wardrobe_weapon_fx.py`). Open question 5.
4. **Missing part P3: a `worn` cue option.** Power Cleave plays the axe set (powerCleave1|2 voice, the `powerCleave`
   arc) or, with a hammer in the main hand, the hammer set (powerHammer1|2, `powerHammer`) (`:26318-26450`,
   `:26116-26204`; `getPowerHammerLv` :8192-8236). The page's `notWorn` takes one item and there is no positive
   `worn` (`index.html` fxStart: `C?.state?.[c.notWorn[0]] === c.notWorn[1]`). Needed: `notWorn: [slot, item | [items]]`
   and `worn: [slot, item | [items]]` (the cue plays only while one of the items is worn there). Without it both sets
   play together. The hammers: BB's `isHammer` (:8284-8468) has **22 codes** (w_bsn5, 15, 19, 22, 24, 25, 32, 34, 35,
   40, 41, 42, 45, 46, 49, 50, 51, 52, 59, 60, 61, 62), in the wardrobe's names (`wardrobe/data/item_map.json`):
   stoneClub, toyHammer, bdWeapon, defenderHammer, defenderHammerR, barbell, warlordHammer, warlordHammerR, hallowLance,
   havocHammer, havocHammerR, havocHammerV, superStarBass, mummyMace, goldenHammer, royalHammer (50 and 51),
   royalHammerR, specialHammer, legendHammer (60 and 61), legendHammerR (not a wardrobe prop today; harmless); plus
   **timeHammer** (w_bsn69), which only TTO counts (open question 2). The main hand is slot `"R"` (the Bison is not in
   `SWAP_HANDS`).
5. **Missing part P4: Enrage's look.** The `enrage` status (from 0.5 s) makes the Bison bigger and redder:
   `transform.localScale += sLv x 0.05` and `mColor = (0.8 + 0.05 sLv, 0.8 - 0.05 sLv, 0.8 - 0.05 sLv)` through
   `setColor` = every child Renderer's `material.color` (`_Color`) (CharacterControl.cs:34713-34729, :21702-21800); its
   end puts the scale back and the colour to the usual 0.86 grey (:15412-15425; the default `mColor` 0.86, :139). At
   Enrage 4 + Rage Control sLv = 5: **scale x 1.25, colour (1.05, 0.55, 0.55)**, i.e. x (1.221, 0.640, 0.640) of the
   normal look. A new `HERO_SKINS["enrage"]` look (index.html): each mesh's material colour times that ratio (the
   texture kept, lit as before) and the hero's root scaled 1.25 for the cue's `kill` (10 s, the standing cut; the game's
   chaAdjust(24) s); a `HeroSkin` today has no scale and always draws a shell (FX/CosmicRift), so the look needs those two
   hooks. Until built, the `skin` cue counts as missing (`FX.missing["skin:enrage"]`, the fx check fails): leave it out
   of the first cue pass. Open question 1.
6. **Missing part P5: the cleave tile's icon.** `wardrobe/data/icons/hd/index.json` has no skill for `cleave` (the clip
   isn't named like its skill): `pipeline/wardrobe_skill_icons.py` needs `CLIP_SKILLS["bison"] = {"cleave":
   ["powerCleave"]}` (the Bible has `bison_powerCleave2`). Then run it.
7. **BB file bugs** (Debug.LogError at run time): `Voices/magmaClutter1` / `magmaClutter2` (:31777, :31808) are not in
   BB's files (the rip's `bison/voices` has none; the two names exist only under `bison/sounds`, the rings' own
   sounds); TTO loads `sounds/magmaClutter1` / `magmaClutter2` in their place (pseudo/Bison.c:7480-7550): cued as a
   `sound` (the Sheep's decision 10, TTO's fix). `Effects/magmaClutter_hit` (:9203) isn't in BB's files either
   (probe: KeyError); it would only show on a hit target, so nothing is lost.
8. **Effects on targets left out (out of reach of the 10 m target point, as the Penguin's Mana Arc):** knockDown_hit
   (box 2 m ahead, radius 4), powerCleave_hit / powerHammer_hit (1 m behind to 4 m ahead), earthSmasher's nAttack_hit
   (radius 7), magmaClutter_hit (2 m ahead). The ones that do reach it are in: Mass Stun (target-mode, no range check)
   and Calamity Hammer's strikes (target-mode). Earth Rupture's waves cross the 10 m point but their hit draws nothing.
9. **The hero doesn't travel** (the Wolf's Feral Assault / Penguin's Blink convention): Knock Down steps 1.2 m before the
   slam (moveSpeed 1 x 0.4 s + 4 x 0.2 s), Earth Smasher leaps 1.2 m (2 x 0.6 s), Magma Clutter dashes 1.5 + 1 m, Instant
   Rush 12 m. Every effect is placed relative to the standing hero (afterShock 2 m ahead, not 3.2 m). The effects spawned
   at the start of a moving skill all have followPosition, so this matches the game's look relative to the Bison.
10. **Screen-only effects left out:** `CameraEffect.AddMotionBlur` (Enrage, Mass Stun, Instant Rush, Earth Smasher,
    Calamity Hammer), `AddCamereShake`, `AutoZoom` (Knock Down, Earth Smasher): the player's own camera.

Every other effect is **ready** (inventory + probe): enrage_ring, knockDown_ring, afterShock, farStun_ring, massStun
(its Animation rocks), instantRush_ring (Animation + SkinnedMeshRenderer + AlphaTimer), instantRush_dust, powerCleave,
powerCleave_ring, powerReel_ring, powerHammer (TrailRenderer), earthRupture_ring, earthSmasher, earthSmasher_ring,
magmaClutter_ring1, calamityHammer_ring, calamityHammer_fire. Every voice is in BB's rip (`bison/voices`: enrage1-2,
knockDown1-2, farStun1-2, instantRush1-2, powerCleave1-2, powerHammer1-2, earthRupture1-2, earthSmasher1-2,
calamityHammer) and every effect sound in `bison/sounds`.

---

## Enrage (clip `enrage`, 1.0 s)

`RPC_enrage` (:20759-21215; dispatch :3711-3765), `enrage.txt`.

| t | what | source |
|---|---|---|
| 0 | clip cut in (`PlayAnimation("enrage", 0)`), wrap Once; voice enrage1 / enrage2 (`Random.Range(0, 2)`) | :21064, :21105-21164 |
| 0.2 | `enrage_ring` Instantiated at the hero, hero rotation (EC life 1 + afterLife 1, no followPosition / followState; AudioSource `enrage`) | Yield 0.2 :21207; :20911-20923 |
| 0.5 | status `enrage` Lv sLv + RageControl = 5, `chaAdjust(12 + 12)` = 24 s: scale x 1.25, tint (1.05, 0.55, 0.55) (Read this first 5) | Yield 0.3 :21211; :20968-20973 |
| 0.8 | `actionState = "standby"` | Yield 0.3 :21213; :20994 |

The voice plays for the player's own hero (and team-mates in team games, :21082-21098). Motion blur (:21179-21182)
left out. Rank changes only the status level (tint / scale); no rank picks an effect. Titan Form blocks Enrage (not on).

## Knock Down (clip `knockDown`, 1.3 s)

`RPC_knockDown` (:22761-23470; dispatch :3855-3909), `knockDown.txt`.

| t | what | source |
|---|---|---|
| 0 | clip cut in, wrap Once; voice knockDown1 / knockDown2 (Random.Range(0, 2)); `knockDown_ring` createEffect at the hero, hero rotation (EC life 1 + afterLife 2, followPosition, followState; its LineEmitter waits 0.2 s; AudioSource `knockDown_ring`) | :23278, :23319-23378, :23387-23405 |
| 0.3 | moveSpeed 1 | Yield 0.3 :23460; :22908 |
| 0.7 | moveSpeed 4 | Yield 0.4 :23458; :22935 |
| 0.9 | Aftershock #422 on: `afterShock` Instantiated at hero + 2 x forward, hero rotation (EC life 1; AudioSource `afterShock`); without it `knockDown` the same way | Yield 0.2 :23453; :22967-23039 |
| 0.9 | hit: FindAreaTarget(pos + 2 fwd, 4 x rangeMod, 2) -> `RPC_knockDown_hit` at each damaged target + 1.5 m up (out of reach) | :23064, :23126-23142 |
| 1.1 | standby (the ring's cut) | Yield 0.2 :23467; :23208 |

Rank: the KO only. Aftershock also adds the `afterShock` status on targets (no prefab).

## Far Stun (clip `farStun`, 1.2 s)

`RPC_farStun` (:23532-24091; dispatch :3945-3963), `farStun.txt`; `RPC_massStun_fire` :9082-9170, `RPC_farStun_fire`
:7632-7725.

| t | what | source |
|---|---|---|
| 0 | clip cut in; voice farStun1 / farStun2 | :23947, :23988-24070 |
| 0.4 | `farStun_ring` Instantiated at hero + TransformDirection(0.5, 0, 0.15), hero rotation (EC life 2, no followState; ImageEmitter / RingEmitter wait 0.3 s; AudioSource `farStun_ring`) | Yield 0.4 :24068; :23689-23707 |
| 0.7 | Mass Stun #442 on: `RPC_massStun_fire(target.position, hero forward)`: `massStun` Instantiated at the target's position, LookRotation(hero forward) (EC life 2, no AudioSource; rock Animation): **the 10 m target point, no rot** | Yield 0.3 :24066; :23797-23820, :9096-9108 |
| 1.0 | standby | Yield 0.3 :24074; :23877 |

Without Mass Stun: `farStun` (EC life 3, AudioSource `farStun_hit`) the same way (:7646-7658). The Bison's self-hit
(:7717, :9167) draws nothing on the page.

## Instant Rush (clip `instantRush`, 1.0 s)

`RPC_instantRush` (:24136-24578; dispatch :3981, cast check > 12 m :5752-5799), `instantRush.txt`.

| t | what | source |
|---|---|---|
| 0 | clip cut in; voice instantRush1 / instantRush2; `instantRush_ring` (EC life 1; AudioSource `instantRush`) and `instantRush_dust` (EC life 1, followPosition) createEffect at the cast position, LookRotation(tDir) (= the facing the hero was just given, :24364) | :24367, :24408-24467, :24476-24526 |
| 0.1 | moveSpeed 24 (12 m in 0.5 s) | Yield 0.1 :24572; :24271 |
| 0.6 | standby | Yield 0.5 :24570; :24297 |

The game refuses a target nearer than 12 m ("Target too close"); nothing is drawn at the target, so the 10 m point
doesn't matter.

## Power Cleave (clip `cleave`, 1.333 s)

`RPC_powerCleave` (:25688-26641; dispatch :4107-4125), `powerCleave.txt`.

| t | what | source |
|---|---|---|
| 0 | clip cut in; voice powerCleave1 / powerCleave2 (axe) or powerHammer1 / powerHammer2 (`mPowerHammerLv > 0`: a hammer worn) | :26252, :26272-26283, :26318-26450 |
| 0 | `powerCleave_ring` createEffect at the hero, hero rotation (EC life 1 + afterLife 1, followPosition, followState; AudioSource `powerCleave`) | :26459-26477 |
| 0 | Power Reel on (owner): `powerReel_ring` the same way (EC life 1 + afterLife 1, followPosition, followState; no sound); pull pass 1 (FindAreaTarget 8 m, force 2 toward the Bison) | :26499-26525, :26554-26593 |
| 0.2, 0.4 | pull passes 2 and 3 | Yield(2, 0.2) :26628, i++ :25835 |
| 0.6 | i >= 3 (:26545), or without the reel Yield(3, 0.6) (:26619): `powerCleave` (axe) or `powerHammer` (hammer) createEffect at the hero, hero rotation, localScale = the hero's (EC life 0.3, followPosition, followState; an Animation swinging a TrailEmitter / TrailRenderer) | :26116-26204 |
| 0.7 | the hit (FindRecTarget from 1 m behind, 4 m wide, 5 m long): `RPC_powerCleave_hit` / `RPC_powerHammer_hit` at each target (out of reach) | Yield 0.1 :26617; :25893-26010 |
| 1.0 | moveSpeed 0 | Yield 0.3 :26608; :26043 |
| 1.2 | standby (the cut of both rings and the arc) | Yield 0.2 :26615; :26064 |

**New timing (for the Bible):** with Power Reel the three passes take exactly the no-reel wait, so the arc is at 0.6 s,
the hit at 0.7 s and standby at 1.2 s either way (case 3's `break` lands on IL_1B5B, the arc, right after the switch,
:26114-26116). The reference left the Power Reel cast length unstated.

## Earth Rupture (clip `earthRupture`, 1.7 s)

`RPC_earthRupture` (:28466-28903; dispatch :4251-4269), `earthRupture.txt`; `RPC_earthRupture_fire1` :8762-8818,
`RPC_earthRupture_fire2` :8829-8929.

| t | what | source |
|---|---|---|
| 0 | clip cut in; voice earthRupture1 / earthRupture2; `earthRupture_ring` createEffect at the hero, hero rotation (EC life 2 + afterLife 2, followPosition, followState; emitters wait 0.2 / 0.8 s; AudioSource `earthRupture`) | :28739, :28780-28839, :28848-28864 |
| 0.8 | sLv 2: `RPC_earthRupture_fire2(hero + TransformDirection(0, 0.2, 0.4), forward)`: three `earthRupture` waves, LookRotation(forward) x Euler(0, 25 i, 0), i = -1, 0, 1, life 2, 12 m/s (Read this first 2) | Yield 0.8 :28899; :28620-28634, :8853-8907 |
| 1.5 | standby (the ring's cut) | Yield 0.7 :28891; :28669 |

Rank 1 (`fire1`): one wave. Each wave: 3 Animation + SkinnedMeshRenderer rock strips (clip `root` 1.2 s, wrap 2 =
loop) and two legacy emitters (Dust3, Smoke1); TTO's copy swaps the emitters for Shuriken (BB's are built).

## Earth Smasher (clip `earthSmasher`, 3.5 s)

`RPC_earthSmasher` (:28935-29585; dispatch :4287-4305), `earthSmasher.txt`.

| t | what | source |
|---|---|---|
| 0 | clip with a 0.2 s fade (`PlayAnimation("earthSmasher", 0.2f)`); voice earthSmasher1 / earthSmasher2; `earthSmasher_ring` createEffect at the hero, hero rotation (EC life 1 + afterLife 3, followPosition, followState; AudioSource `earthSmasher`) | :29390, :29431-29490, :29499-29517 |
| 0.8 | moveSpeed 2 (the leap) | Yield 0.8 :29577; :29082 |
| 1.4 | moveSpeed 0; `earthSmasher` Instantiated at the hero, hero rotation (EC life 2; rocks Animation 1 m ahead, emitters 1-1.5 m ahead); hit radius 7 -> `RPC_nAttack_hit` at each target (out of reach) | Yield 0.6 :29583; :29109-29245 |
| 2.6 | camera zoom back | Yield 1.2 :29572; :29299 |
| 3.2 | standby (the ring's cut) | Yield 0.6 :29579; :29320 |

Rank: damage and KO only.

## Magma Clutter (clip `magmaClutter`, 1.8 s)

`RPC_magmaClutter` (:31242-31903; dispatch :4467), `magmaClutter.txt`.

| t | what | source |
|---|---|---|
| 0 | clip cut in; moveSpeed 5; (BB) voice Voices/magmaClutter1 / 2, missing -> (TTO) sound magmaClutter1 / magmaClutter2 (Read this first 7); `magmaClutter_ring1` createEffect at the hero, hero rotation (EC life 1 + afterLife 1, followPosition, followState; emitters 1.5 m ahead wait 0.3 s; AudioSource `magmaClutter1`) | :31724-31733, :31765-31824, :31833-31849 |
| 0.3 | moveSpeed 0, the lift (FindAreaTarget 1 m ahead, radius 2; no effect) | Yield 0.3 :31896; :31378-31457 |
| 0.8 | moveSpeed 5; `magmaClutter_ring2` createEffect at the hero, hero rotation (root scale 0.7; EC life 1 + afterLife 0.5, followPosition, followState; AudioSource `magmaClutter2`; Animation `cleave` swinging the TrailEmitter + Shuriken node) | Yield 0.5 :31882; :31495-31518 |
| 1.0 | moveSpeed 0, the gore (FindRecTarget to 2 m ahead) -> magmaClutter_hit at targets (out of reach; missing in BB) | Yield 0.2 :31880; :31555-31627 |
| 1.3 | standby (both rings' cut) | Yield 0.3 :31884; :31654 |

## Calamity Hammer (clip `calamityHammer`, 2.5 s)

`RPC_calamityHammer` (:31959-32397; dispatch :4503), `OnCalamityHammer` (:32444-32639), `RPC_calamityHammer_fire`
(:32671-32897); `calamityHammer.txt`, `calamity_fire.txt`.

| t | what | source |
|---|---|---|
| 0 | clip cut in; voice calamityHammer (one file, no pick); `calamityHammer_ring` createEffect at the hero, hero rotation (EC life 3 + afterLife 1, followPosition, followState; slam emitters at (0, 0.05 / 0.2, 3.5) wait 2.1 s, a LineEmitter 0.3 s, rings 0 / 0.3 s; AudioSource `calamityHammer_ring`) | :32273, :32314-32332, :32343-32360 |
| 2.1 | the slam's hit (FindAreaTarget 3.5 m ahead, radius 3; drawn by the ring's delayed emitters); `OnCalamityHammer(tID)` starts | Yield 2.1 :32387; :32117-32156 |
| 2.1 + 1.5 k (k = 0..9) | pass k: while hp > 0 and the target exists, `RPC_calamityHammer_fire(target.position)` | :32564-32606, Yield(2, 1.5) :32635 |
| 2.4 + 1.5 k | after Yield 0.3: `calamityHammer_fire` Instantiated at that position, `Quaternion.identity` (EC life 1 + afterLife 1; AudioSource `calamityHammer_fire`); hit radius 1 | :32895, :32779-32797 |
| 2.3 | standby (the ring's cut) | Yield 0.2 :32394; :32203 |

So the strikes land at 2.4, 3.9, 5.4, 6.9, 8.4, 9.9, 11.4, 12.9, 14.4, 15.9 s on the 10 m target point; cued up to
10 s (six; open question 3). `Quaternion.identity` = world axes: the effect is round (rings, image emitters, particles
around one point), so no rot.

---

## Cue entries (paste-ready for `wardrobe/fx_cues/bison.json`)

`checks\fx_bison_research\skills_a\entries.json` (valid JSON). Order of building: the six entries needing no new part
(knockDown, farStun, instantRush, earthSmasher, calamityHammer, and magmaClutter once `wardrobe_fx_tto.py bison` has
built `tto/magmaClutter_ring2`) can go in at once; `earthRupture` with P1, `cleave` with P3, `enrage`'s skin cue with P4
(its first two cues can go in before).

```json
{
 "enrage": {
  "why": "Bison.cs RPC_enrage (:20759-21215) at max rank (sLv 4) with Rage Control #402 on (passives on: status Lv 4 + 1 = 5, chaAdjust(12 + 12) s, :20968-20973): clip (PlayAnimation(\"enrage\", 0) :21064) and voice enrage1 / enrage2 (Random.Range(0, 2) :21105-21164) at 0; Yield 0.2 (:21207): enrage_ring Instantiated at the hero, hero rotation (:20911-20923; EffectControl life 1 + afterLife 1, no followState; plays its own Sounds/enrage); Yield 0.3 (:21211): at 0.5 s the status (RPC_AddStatus :20973): the body + 0.05 x 5 = 1.25 x and every renderer's _Color (1.05, 0.55, 0.55) for the usual 0.86 grey (CharacterControl.cs:34713-34729, setColor :21702-21800; undone at its end, :15412-15425): the skin cue enrage (index.html HERO_SKINS, a part to build), cut at 10 s (the standing rule; 24 s in the game); Yield 0.3 (:21213): standby at 0.8 s (:20994); the camera's motion blur (:21179-21182) is the player's screen only",
  "cues": [
   [
    0,
    "voice",
    "enrage1|enrage2"
   ],
   [
    0.2,
    "fx",
    "enrage_ring"
   ],
   [
    0.5,
    "skin",
    "enrage",
    {
     "kill": 10
    }
   ]
  ]
 },
 "knockDown": {
  "why": "Bison.cs RPC_knockDown (:22761-23470) at max rank (sLv 4) with Aftershock #422 on (passives on, hasSkill(422) :22967): clip (PlayAnimation(\"knockDown\", 0) :23278), voice knockDown1 / knockDown2 (Random.Range(0, 2) :23319-23378) and knockDown_ring created at the hero, hero rotation (createEffect :23393-23405; EffectControl life 1 + afterLife 2, followPosition, followState; plays its own Sounds/knockDown_ring) at 0; Yield 0.3 (:23460) moveSpeed 1 (:22908), Yield 0.4 (:23458) moveSpeed 4 (:22935): the game steps the Bison 1.2 m on, the wardrobe hero doesn't travel; Yield 0.2 (:23453): at 0.9 s afterShock, in place of knockDown (:22972-23039), Instantiated 2 m ahead, hero rotation (:22996; life 1; plays its own Sounds/afterShock); the hit (FindAreaTarget 2 m ahead, radius 4, :23064) can't reach the 10 m target, so no knockDown_hit (:23132, :7498-7521); Yield 0.2 (:23467): standby at 1.1 s (:23208), the ring's cut; the camera zooms (:23425-23431, :23054) are the player's screen only",
  "cues": [
   [
    0,
    "voice",
    "knockDown1|knockDown2"
   ],
   [
    0,
    "fx",
    "knockDown_ring",
    0,
    1.1
   ],
   [
    0.9,
    "fx",
    "afterShock",
    2
   ]
  ]
 },
 "farStun": {
  "why": "Bison.cs RPC_farStun (:23532-24091) at max rank (sLv 2) with Mass Stun #442 on (passives on, hasSkill(442) :23797): clip (PlayAnimation(\"farStun\", 0) :23947) and voice farStun1 / farStun2 (Random.Range(0, 2) :23988-24070) at 0; Yield 0.4 (:24068): farStun_ring Instantiated at the hero + TransformDirection(0.5, 0, 0.15) (0.5 m right, 0.15 m ahead), hero rotation (:23695-23707; EffectControl life 2, no followState; plays its own Sounds/farStun_ring); Yield 0.3 (:24066): at 0.7 s RPC_massStun_fire at the target's position (tPos :23763, :23820): massStun Instantiated there, LookRotation(the hero's forward) (:9096-9108; life 2, no AudioSource) at the 10 m target point; farStun (RPC_farStun_fire :7646-7658, life 3, Sounds/farStun_hit) is the version without the passive; the Bison's hit on itself (:9167) draws nothing; Yield 0.3 (:24074): standby at 1.0 s (:23877); the blur and the target's camera shake (:23814, :23783) are screen only",
  "cues": [
   [
    0,
    "voice",
    "farStun1|farStun2"
   ],
   [
    0.4,
    "fx",
    "farStun_ring",
    {
     "x": 0.5,
     "d": 0.15
    }
   ],
   [
    0.7,
    "fx",
    "massStun",
    10
   ]
  ]
 },
 "instantRush": {
  "why": "Bison.cs RPC_instantRush (:24136-24578), one rank: clip (PlayAnimation(\"instantRush\", 0) :24367), voice instantRush1 / instantRush2 (Random.Range(0, 2) :24408-24467), instantRush_ring (EffectControl life 1; plays its own Sounds/instantRush) and instantRush_dust (life 1, followPosition) created at the cast position, LookRotation(tDir) = the hero's facing (createEffect :24476-24526) at 0; Yield 0.1 (:24572): the 12 m rush (moveSpeed 24 for 0.5 s, :24271; the wardrobe hero doesn't travel; the game wants the target over 12 m away, :5752-5799); Yield 0.5 (:24570): standby at 0.6 s (:24297); no hit and no effect at the target; the motion blur (:24546-24549) is the player's screen only",
  "cues": [
   [
    0,
    "voice",
    "instantRush1|instantRush2"
   ],
   [
    0,
    "fx",
    "instantRush_ring"
   ],
   [
    0,
    "fx",
    "instantRush_dust"
   ]
  ]
 },
 "cleave": {
  "why": "Bison.cs RPC_powerCleave (:25688-26641), the only clip call of cleave (:26252), at max rank (sLv 2) with Power Reel #403 and Power Hammer #304 on (passives on); Power Hammer counts only with a hammer in the main hand (getPowerHammerLv :8192-8236; isHammer :8284-8468, BB's 22 codes in the wardrobe's names, wardrobe/data/item_map.json, plus timeHammer w_bsn69, TTO's fix TTO1102:Bison::isHammer@0x1B4EF30): clip cut in (PlayAnimation(\"cleave\", 0)) at 0 with voice powerCleave1 / powerCleave2, or powerHammer1 / powerHammer2 with a hammer (Random.Range(0, 2) :26318-26450); powerCleave_ring created at the hero, hero rotation (createEffect :26459-26477; EffectControl life 1 + afterLife 1, followPosition, followState; plays its own Sounds/powerCleave) and, Power Reel on, powerReel_ring the same way (:26499-26525; no sound) at 0; the reel's three pull passes at 0, 0.2, 0.4 s (FindAreaTarget 8 m :26554, Yield(2, 0.2) :26628, i++ :25835, i >= 3 :26545) end at 0.6 s, the no-reel wait's time too (Yield(3, 0.6) :26619): at 0.6 s powerCleave (axe) or powerHammer (hammer) created at the hero, scaled as the hero (:26116-26204; life 0.3, followPosition, followState); Yield 0.1 (:26617): the hit at 0.7 s (FindRecTarget 1 m behind to 4 m ahead, :25893) can't reach the 10 m target, so no powerCleave_hit / powerHammer_hit (:25928, :25990); Yield 0.3 (:26608) and 0.2 (:26615): standby at 1.2 s (:26064), the cut of all three",
  "cues": [
   [
    0,
    "voice",
    "powerCleave1|powerCleave2",
    {
     "notWorn": [
      "R",
      [
       "stoneClub",
       "toyHammer",
       "bdWeapon",
       "defenderHammer",
       "defenderHammerR",
       "barbell",
       "warlordHammer",
       "warlordHammerR",
       "hallowLance",
       "havocHammer",
       "havocHammerR",
       "havocHammerV",
       "superStarBass",
       "mummyMace",
       "goldenHammer",
       "royalHammer",
       "royalHammerR",
       "specialHammer",
       "legendHammer",
       "legendHammerR",
       "timeHammer"
      ]
     ]
    }
   ],
   [
    0,
    "voice",
    "powerHammer1|powerHammer2",
    {
     "worn": [
      "R",
      [
       "stoneClub",
       "toyHammer",
       "bdWeapon",
       "defenderHammer",
       "defenderHammerR",
       "barbell",
       "warlordHammer",
       "warlordHammerR",
       "hallowLance",
       "havocHammer",
       "havocHammerR",
       "havocHammerV",
       "superStarBass",
       "mummyMace",
       "goldenHammer",
       "royalHammer",
       "royalHammerR",
       "specialHammer",
       "legendHammer",
       "legendHammerR",
       "timeHammer"
      ]
     ]
    }
   ],
   [
    0,
    "fx",
    "powerCleave_ring",
    0,
    1.2
   ],
   [
    0,
    "fx",
    "powerReel_ring",
    0,
    1.2
   ],
   [
    0.6,
    "fx",
    "powerCleave",
    {
     "notWorn": [
      "R",
      [
       "stoneClub",
       "toyHammer",
       "bdWeapon",
       "defenderHammer",
       "defenderHammerR",
       "barbell",
       "warlordHammer",
       "warlordHammerR",
       "hallowLance",
       "havocHammer",
       "havocHammerR",
       "havocHammerV",
       "superStarBass",
       "mummyMace",
       "goldenHammer",
       "royalHammer",
       "royalHammerR",
       "specialHammer",
       "legendHammer",
       "legendHammerR",
       "timeHammer"
      ]
     ],
     "cut": 1.2
    }
   ],
   [
    0.6,
    "fx",
    "powerHammer",
    {
     "worn": [
      "R",
      [
       "stoneClub",
       "toyHammer",
       "bdWeapon",
       "defenderHammer",
       "defenderHammerR",
       "barbell",
       "warlordHammer",
       "warlordHammerR",
       "hallowLance",
       "havocHammer",
       "havocHammerR",
       "havocHammerV",
       "superStarBass",
       "mummyMace",
       "goldenHammer",
       "royalHammer",
       "royalHammerR",
       "specialHammer",
       "legendHammer",
       "legendHammerR",
       "timeHammer"
      ]
     ],
     "cut": 1.2
    }
   ]
  ]
 },
 "earthRupture": {
  "why": "Bison.cs RPC_earthRupture (:28466-28903) at max rank (sLv 2): clip (PlayAnimation(\"earthRupture\", 0) :28739), voice earthRupture1 / earthRupture2 (Random.Range(0, 2) :28780-28839) and earthRupture_ring created at the hero, hero rotation (createEffect :28848-28864; EffectControl life 2 + afterLife 2, followPosition, followState; its emitters wait 0.2 / 0.8 s; plays its own Sounds/earthRupture) at 0; Yield 0.8 (:28899): RPC_earthRupture_fire2 (sLv != 1, :28620-28634) from the hero + TransformDirection(0, 0.2, 0.4): three waves Instantiated at LookRotation(forward) x Euler(0, 25 i, 0), i = -1, 0, 1 (:8853-8877), ProjectileControl.life 2 (:8892), each moved by Bison_earthRupture at its ProjectileControl.velocity (0, 0, 12) along its own forward, set again every FixedUpdate, and Destroyed at 2 s (Bison_earthRupture.cs:96-127): 24 m, through every target (OnCollisionEnter only hits, :131-190), the 10 m target included; Yield 0.7 (:28891): standby at 1.5 s (:28669), the ring's cut",
  "cues": [
   [
    0,
    "voice",
    "earthRupture1|earthRupture2"
   ],
   [
    0,
    "fx",
    "earthRupture_ring",
    0,
    1.5
   ],
   [
    0.8,
    "fx",
    "earthRupture",
    {
     "y": 0.2,
     "d": 0.4,
     "rot": [
      0,
      -25,
      0
     ]
    }
   ],
   [
    0.8,
    "fx",
    "earthRupture",
    {
     "y": 0.2,
     "d": 0.4
    }
   ],
   [
    0.8,
    "fx",
    "earthRupture",
    {
     "y": 0.2,
     "d": 0.4,
     "rot": [
      0,
      25,
      0
     ]
    }
   ]
  ]
 },
 "earthSmasher": {
  "why": "Bison.cs RPC_earthSmasher (:28935-29585) at max rank (sLv 2): clip with the game's 0.2 s fade (PlayAnimation(\"earthSmasher\", 0.2f) :29390), voice earthSmasher1 / earthSmasher2 (Random.Range(0, 2) :29431-29490) and earthSmasher_ring created at the hero, hero rotation (createEffect :29499-29517; EffectControl life 1 + afterLife 3, followPosition, followState; plays its own Sounds/earthSmasher) at 0; Yield 0.8 (:29577): moveSpeed 2 for the leap (:29082; 1.2 m in the game, the wardrobe hero doesn't travel); Yield 0.6 (:29583): at 1.4 s earthSmasher Instantiated at the hero, hero rotation (:29126-29144; life 2; its rocks 1 m ahead in the prefab); the 7 m hit (:29193) can't reach the 10 m target, so no nAttack_hit (:29222); Yield 1.2 (:29572) and 0.6 (:29579): standby at 3.2 s (:29320), the ring's cut; the shake, blur and zooms (:29120, :29174, :29549, :29299) are the player's screen only",
  "cues": [
   [
    0,
    "voice",
    "earthSmasher1|earthSmasher2"
   ],
   [
    0,
    "fx",
    "earthSmasher_ring",
    0,
    3.2
   ],
   [
    1.4,
    "fx",
    "earthSmasher"
   ]
  ]
 },
 "magmaClutter": {
  "why": "Bison.cs RPC_magmaClutter (:31242-31903), one rank: clip (PlayAnimation(\"magmaClutter\", 0) :31724) and magmaClutter_ring1 created at the hero, hero rotation (createEffect :31833-31849; EffectControl life 1 + afterLife 1, followPosition, followState; its emitters 1.5 m ahead wait 0.3 s; plays its own Sounds/magmaClutter1) at 0; BB's voice Voices/magmaClutter1 / magmaClutter2 (Random.Range(0, 2) :31765-31824) is in none of BB's files (Cannot find magmaClutter1 voice): TTO plays Sounds/magmaClutter1 / magmaClutter2 there (TTO1102 Bison.<RPC_magmaClutter>d__179::MoveNext@0x1B68900, pseudo/Bison.c:7480-7550), taken as TTO's fix (plans/fx_sheep/decisions.md 10); moveSpeed 5 (:31733), the lift at 0.3 s (Yield 0.3 :31896; FindAreaTarget 1 m ahead, radius 2, :31413); Yield 0.5 (:31882): at 0.8 s the dash (moveSpeed 5 :31495; the wardrobe hero doesn't travel) and magmaClutter_ring2 created at the hero, hero rotation (:31500-31518; life 1 + afterLife 0.5, followPosition, followState; plays its own Sounds/magmaClutter2; its Shuriken burst read from TTO's copy, as the weapons' Shuriken, NOTES.md 2026-11-12); Yield 0.2 (:31880): the gore at 1.0 s (FindRecTarget to 2 m ahead, :31568) can't reach the 10 m target (and BB has no magmaClutter_hit, :9203); Yield 0.3 (:31884): standby at 1.3 s (:31654), both rings' cut; the shake (:31389) is screen only",
  "cues": [
   [
    0,
    "sound",
    "magmaClutter1|magmaClutter2"
   ],
   [
    0,
    "fx",
    "magmaClutter_ring1",
    0,
    1.3
   ],
   [
    0.8,
    "fx",
    "tto/magmaClutter_ring2",
    0,
    1.3
   ]
  ]
 },
 "calamityHammer": {
  "why": "Bison.cs RPC_calamityHammer (:31959-32397), one rank, a target skill: clip (PlayAnimation(\"calamityHammer\", 0) :32273), voice calamityHammer (one file, :32314-32332) and calamityHammer_ring created at the hero, hero rotation (createEffect :32343-32360; EffectControl life 3 + afterLife 1, followPosition, followState; its slam emitters 3.5 m ahead wait 2.1 s; plays its own Sounds/calamityHammer_ring) at 0; Yield 2.1 (:32387): the slam's hit 3.5 m ahead (radius 3, :32117; drawn by the ring's delayed emitters) and OnCalamityHammer (:32156): ten passes 1.5 s apart (i < 10 :32564, Yield(2, 1.5) :32635) while the hero lives and the target exists (:32574, :32593), each RPC_calamityHammer_fire at the target's position of that moment (:32601): Yield 0.3 (:32895), then calamityHammer_fire Instantiated there, Quaternion.identity (:32779-32797; EffectControl life 1 + afterLife 1; plays its own Sounds/calamityHammer_fire), so at 2.4, 3.9 ... 15.9 s on the 10 m target point, cut at 10 s (the standing rule: the six up to 9.9 s); Yield 0.2 (:32394): standby at 2.3 s (:32203), the ring's cut; the blur and the shakes (:32182, :32820) are screen only",
  "cues": [
   [
    0,
    "voice",
    "calamityHammer"
   ],
   [
    0,
    "fx",
    "calamityHammer_ring",
    0,
    2.3
   ],
   [
    2.4,
    "fx",
    "calamityHammer_fire",
    10
   ],
   [
    3.9,
    "fx",
    "calamityHammer_fire",
    10
   ],
   [
    5.4,
    "fx",
    "calamityHammer_fire",
    10
   ],
   [
    6.9,
    "fx",
    "calamityHammer_fire",
    10
   ],
   [
    8.4,
    "fx",
    "calamityHammer_fire",
    10
   ],
   [
    9.9,
    "fx",
    "calamityHammer_fire",
    10
   ]
  ]
 }
}
```

Build lines (recipe 4): `wardrobe_fx.py bison` (every BB effect, voice and the `sound` cues these name), then
`wardrobe_fx_tto.py bison` (the `tto/magmaClutter_ring2` cue), then the fx check.

---

## For the Bible (to offer the user; never written there from here)

1. **Power Hammer's hammers in BB:** `isHammer` (Bison.cs:8284-8468) accepts **22** codes (w_bsn5, 15, 19, 22, 24, 25,
   32, 34, 35, 40, 41, 42, 45, 46, 49, 50, 51, 52, 59, 60, 61, 62), every opaque predicate in the chain false
   (`cond.py` 8284-8520). The reference says 6 (TTO sweep, "Power Hammer works with 24 hammers") and 10 (Magma Quake
   "BB's list has 10"): TTO adds only w_bsn68 and w_bsn69 (the Time Hammer, the wardrobe's `timeHammer`), so the
   "[แอบ Buff]" is two weapons, not 18.
2. **Power Cleave with Power Reel:** the arc at 0.6 s, the hit at 0.7 s, standby at 1.2 s, the same as without the reel
   (the three 0.2 s passes replace the 0.6 s wait; case 3 falls through to IL_1B5B, :26114-26116). The reference:
   "the cast length with Power Reel is deliberately not stated".
3. **Magma Clutter's voices:** BB asks for `Voices/magmaClutter1` / `2`, which BB doesn't have (only the rings' sounds of
   those names); TTO plays `Sounds/magmaClutter1` / `2` instead. BB also lacks `Effects/magmaClutter_hit`.
4. **Enrage's look:** the body grows 5 % per status level and turns red, `_Color` (0.8 + 0.05 Lv, 0.8 - 0.05 Lv,
   0.8 - 0.05 Lv) over the normal 0.86 (CharacterControl.cs:34717-34729); at Lv 5 (Enrage 4 + Rage Control) x 1.25,
   (1.05, 0.55, 0.55). The reference names the scale, not the tint.
5. **Calamity Hammer's strikes:** each lands 0.3 s after its pass (RPC_calamityHammer_fire's Yield 0.3), so at 2.4 +
   1.5 k s of the cast (the reference gives the passes at 0, 1.5 ... 13.5 s after the windup and the 0.3 s wait; this is
   the sum).

---

## Open questions (each with the recommended answer)

1. **Enrage's look (P4): build the red tint and the 1.25 x size as a `skin` cue for 10 s?** Recommended: **yes**. It is
   what Enrage shows for its whole time (the ring lasts 1 s); the Penguin's decision 10 left out a passive's side tint
   (Double Spell's), not a skill's own look; the user's rule is to build every missing part. Alternative: leave the look
   out and keep the ring and voice only.
2. **Power Cleave's hammer set (P3): play it by the worn weapon, with which list?** Recommended: **yes, by the worn
   weapon, BB's 22 codes plus `timeHammer`** (TTO counts w_bsn69, the Time Hammer, as a hammer, and TTO's 1.5.9.1 patch
   line "ค้อนไทม์ไบสัน" reads as that fix: the Sheep's decision 10, TTO's fixes for BB bugs). The default weapon (an
   axe) plays the axe set. Alternative: BB's 22 only (drop `timeHammer` from both lists).
3. **Calamity Hammer's ten strikes: all of them (to 15.9 s), or cut at 10 s?** Recommended: **cut at 10 s, six
   strikes** (the standing rule for long fields; the Penguin's Ice Shield / Mana Vortex). Alternative: all ten (the
   tile then lasts about 18 s); add `[11.4 ... 15.9, "fx", "calamityHammer_fire", 10]`.
4. **Magma Clutter's start sound:** BB's voice is missing; TTO plays one of the two ring sounds there, which doubles
   ring1's own `magmaClutter1` half the time. Recommended: **follow TTO** (`[0, "sound", "magmaClutter1|magmaClutter2"]`,
   decision 10). Alternative: no start voice (BB's silence).
5. **magmaClutter_ring2 (P2): TTO's copy (`tto/magmaClutter_ring2`) or teach `wardrobe_fx.py` BB's Shuriken?**
   Recommended: **TTO's copy**, as the weapons' Shuriken (NOTES.md 2026-11-12): TTO's copy is the same prefab (same
   EffectControl, AudioSource, Animation, TrailEmitter) with the ParticleSystem in a readable form. Online (the skill
   effects are published since 2026-11-09, `wardrobe_publish.py publish_fx`) it goes out scrambled like every `tto/`
   effect (its `tto_Bomb2` texture, and the Bison's fx.json once it holds a `tto/` key), as the weapons' TTO copies did;
   it is BB content (BB's prefab), so the content rule holds, but `publish_fx`'s docstring ("TTO's effects are only cued
   for released TTO skills") no longer says it all: worth a line there. Alternative: a BB Shuriken reader in
   `wardrobe_fx.py` (no scrambling, more work).
6. **Effects of moving skills: relative to the standing hero?** Recommended: **yes** (Knock Down's afterShock 2 m, not
   3.2 m; Earth Smasher's blast at the hero), the convention of the Wolf's Feral Assault and the Penguin's Blink.
7. **Mass Stun on the 10 m point even though Far Stun's ring is at the hero?** Recommended: **yes** (the standing rule;
   the skill has no range check, :5733-5752 per the reference). Its blast has no sound (massStun has no AudioSource;
   Far Stun's own `farStun` had `farStun_hit`): kept as the game's.
8. **The cleave tile's icon (P5):** Recommended: **Power Cleave's** (`CLIP_SKILLS["bison"]["cleave"] = ["powerCleave"]`);
   Power Hammer is a passive and gets no icon on it.

## Verification (read-only checker, 2026-11-13)

Checked against `Bison.cs`, `Bison_earthRupture.cs`, `CharacterControl.cs`, the probes in `checks\fx_bison_research\skills_a\`
and TTO's `pseudo/Bison.c`, every opaque predicate resolved (`cond.py`) and every coroutine traced with `pipeline/clip_flow.js`;
my probe `checks\fx_bison_research\verify_a\blocks.py` (the block parses, cue times in order; it writes the block below).

**Times, names, positions, picks and ranks: all confirmed.** Re-derived:

- **Clips:** one `PlayAnimation` each (:21064, :23278, :23947, :24367, :26252, :28739, :29390, :31724, :32273). In TTO each
  name string is used only by its own coroutine; `magmaClutter` / `calamityHammer` also appear in `Bison::Start`
  (pseudo/Bison.c:18767-18831), which only sets their cooldowns, and `calamityHammer` in Magma Quake as the axe's voice.
- **Enrage:** entry 0 -> `Yield(2, 0.2)` enrage_ring (:20923) -> `Yield(3, 0.3)` status at 0.5 (:20968-20973,
  `chaAdjust(12 + 12 x 1)`, Lv sLv + 1) -> `Yield(4, 0.3)` standby 0.8. Look: CharacterControl.cs:34717-34729, undone :15416-15428.
- **Knock Down:** 0 ring + voice; 0.3 moveSpeed 1; 0.7 moveSpeed 4; 0.9 afterShock at `position + 2 x forward` (:22996),
  hit; 1.1 standby (:23208).
- **Far Stun:** 0.4 farStun_ring at `TransformDirection(0.5, 0, 0.15)` (:23707); 0.7 tPos = the target (:23763),
  `hasSkill(442)` -> RPC_massStun_fire -> `Instantiate(massStun, tPos, LookRotation(tDir))` with tDir = the hero's
  forward (:23820, :9108): the hero's facing, no `[0, 180, 0]`; 1.0 standby.
- **Instant Rush:** both effects `createEffect(..., mPos, LookRotation(tDir))` at 0 (:24494, :24526); 0.1 moveSpeed 24; 0.6 standby.
- **Power Cleave:** with the reel, entry -> IL_14F0 pass at 0 -> `Yield(2, 0.2)` -> case 2 `i++` -> ... `i >= 3` ->
  `goto IL_1B5B` = the arc (:26545-26549) at 0.6 -> IL_8F5 `Yield(4, 0.1)` (:26617) -> hit 0.7 -> `Yield(5, 0.3)` ->
  `Yield(6, 0.2)` -> standby 1.2. Without it: `goto IL_949` `Yield(3, 0.6)` (:26499-26501, :26619), case 3 `break`
  falls onto IL_1B5B: the same times. The new-timing claim holds.
- **Hammers:** `isHammer` resolved (:8284-8468): exactly the 22 codes listed; TTO's `Bison__isHammer` (pseudo/Bison.c:26239)
  has 24 = those + w_bsn68 + w_bsn69. The wardrobe names match `item_map.json`; no listed name is also a non-hammer
  code's; `legendHammerR` is not a prop; w_bsn68 has no wardrobe name.
- **Earth Rupture:** 0.8 fire2 (`sLv == 1` -> fire1, :28620-28634) at `TransformDirection(0, 0.2, 0.4)`; three waves
  `LookRotation(fireDir) x Euler(0, 25 i, 0)`, life 2 (:8853-8892); Bison_earthRupture.cs:96-127 (velocity every
  FixedUpdate, Destroy at life), :131-190 (hit only); 1.5 standby.
- **Earth Smasher:** 0.2 fade (:29390); 0.8 moveSpeed 2; 1.4 earthSmasher at the hero (:29144); 2.6; 3.2 standby.
- **Magma Clutter:** 0.3 lift; 0.8 ring2 (:31518); 1.0 gore; 1.3 standby. BB's `Voices/magmaClutter1/2` (:31777, :31808)
  are not in the rip's `voices/` (rip_list.txt); TTO loads `sounds/magmaClutter1/2`.
- **Calamity Hammer:** `Yield(2, 2.1)` -> slam + OnCalamityHammer (:32156) -> `Yield(3, 0.2)` standby 2.3. OnCalamityHammer:
  case 0 -> IL_17F (owner) `i = 0` -> IL_24B fires at once (:32601), then `Yield(2, 1.5)` (:32635), `i < 10` (:32564);
  RPC_calamityHammer_fire `Yield(2, 0.3)` then `Instantiate(..., hitPos, Quaternion.identity)` (:32797): strikes at
  2.4 + 1.5 k. The slam (radius 3 at 3.5 m, :32117) and the strikes spawn nothing at the hit targets.
- **Probe claims** (summary.txt): every EffectControl life / afterLife / followPosition / followState quoted matches;
  each cut sits on a followState effect (the ones on effects already past their life, the knockDown / earthSmasher /
  powerCleave rings and the 0.3 s arcs, are harmless).
- **Formats:** cues fit `cueOf` (index.html:4333-4344); `worn` and a list in `notWorn` need P3 as said (`worn()`, :4462,
  takes one item); a `skin` cue with no `HERO_SKINS` entry fails the fx check (:4513-4515), as said.

**Corrections:**
1. **Block format** (Cue entries): the block is `json.dumps(indent=1)`, one array element per line, wrapped in an outer `{}`.
   The cue file's format (recipe step 3, the other classes' files) is one entry per key at 2 spaces, `why` / `cues` at 4,
   one cue per line, to paste inside `bison.json`'s braces. Same content; the corrected block is below.
2. **TTO lines** (Read this first 7, the magmaClutter `why`, For the Bible 3): TTO's magmaClutter start sound is
   `Random.Range(0, 2)` at pseudo/Bison.c:7483, the loads at :7494 (`sounds/magmaClutter1`) and :7529 (`magmaClutter2`),
   PlayOneShot at :7554: **:7483-7554**, not 7480-7550 (the `why` changed in the block below). Read this first 1: Magma
   Quake's voice choice (calamityHammer for the axe, earthSmasher1 / 2 with a hammer, `Row6Voice`) is **:7696-7702**.
3. **Wording** (Read this first 8): Knock Down's hit is a **circle** (`FindAreaTarget`, :23064) centred 2 m ahead with radius
   4 (2 + 2 with Aftershock), not a box. Its reach (6 m) still misses the 10 m point: no cue change.

Corrected block set (paste inside the braces of `wardrobe/fx_cues/bison.json`; as the report says, `enrage`'s skin cue
waits for P4, `cleave` for P3, `earthRupture` for P1, and `tto/magmaClutter_ring2` for the `wardrobe_fx_tto.py bison` build):

```json
  "enrage": {
    "why": "Bison.cs RPC_enrage (:20759-21215) at max rank (sLv 4) with Rage Control #402 on (passives on: status Lv 4 + 1 = 5, chaAdjust(12 + 12) s, :20968-20973): clip (PlayAnimation(\"enrage\", 0) :21064) and voice enrage1 / enrage2 (Random.Range(0, 2) :21105-21164) at 0; Yield 0.2 (:21207): enrage_ring Instantiated at the hero, hero rotation (:20911-20923; EffectControl life 1 + afterLife 1, no followState; plays its own Sounds/enrage); Yield 0.3 (:21211): at 0.5 s the status (RPC_AddStatus :20973): the body + 0.05 x 5 = 1.25 x and every renderer's _Color (1.05, 0.55, 0.55) for the usual 0.86 grey (CharacterControl.cs:34713-34729, setColor :21702-21800; undone at its end, :15412-15425): the skin cue enrage (index.html HERO_SKINS, a part to build), cut at 10 s (the standing rule; 24 s in the game); Yield 0.3 (:21213): standby at 0.8 s (:20994); the camera's motion blur (:21179-21182) is the player's screen only",
    "cues": [
    [0, "voice", "enrage1|enrage2"],
    [0.2, "fx", "enrage_ring"],
    [0.5, "skin", "enrage", {"kill": 10}]
    ]
  },
  "knockDown": {
    "why": "Bison.cs RPC_knockDown (:22761-23470) at max rank (sLv 4) with Aftershock #422 on (passives on, hasSkill(422) :22967): clip (PlayAnimation(\"knockDown\", 0) :23278), voice knockDown1 / knockDown2 (Random.Range(0, 2) :23319-23378) and knockDown_ring created at the hero, hero rotation (createEffect :23393-23405; EffectControl life 1 + afterLife 2, followPosition, followState; plays its own Sounds/knockDown_ring) at 0; Yield 0.3 (:23460) moveSpeed 1 (:22908), Yield 0.4 (:23458) moveSpeed 4 (:22935): the game steps the Bison 1.2 m on, the wardrobe hero doesn't travel; Yield 0.2 (:23453): at 0.9 s afterShock, in place of knockDown (:22972-23039), Instantiated 2 m ahead, hero rotation (:22996; life 1; plays its own Sounds/afterShock); the hit (FindAreaTarget 2 m ahead, radius 4, :23064) can't reach the 10 m target, so no knockDown_hit (:23132, :7498-7521); Yield 0.2 (:23467): standby at 1.1 s (:23208), the ring's cut; the camera zooms (:23425-23431, :23054) are the player's screen only",
    "cues": [
    [0, "voice", "knockDown1|knockDown2"],
    [0, "fx", "knockDown_ring", 0, 1.1],
    [0.9, "fx", "afterShock", 2]
    ]
  },
  "farStun": {
    "why": "Bison.cs RPC_farStun (:23532-24091) at max rank (sLv 2) with Mass Stun #442 on (passives on, hasSkill(442) :23797): clip (PlayAnimation(\"farStun\", 0) :23947) and voice farStun1 / farStun2 (Random.Range(0, 2) :23988-24070) at 0; Yield 0.4 (:24068): farStun_ring Instantiated at the hero + TransformDirection(0.5, 0, 0.15) (0.5 m right, 0.15 m ahead), hero rotation (:23695-23707; EffectControl life 2, no followState; plays its own Sounds/farStun_ring); Yield 0.3 (:24066): at 0.7 s RPC_massStun_fire at the target's position (tPos :23763, :23820): massStun Instantiated there, LookRotation(the hero's forward) (:9096-9108; life 2, no AudioSource) at the 10 m target point; farStun (RPC_farStun_fire :7646-7658, life 3, Sounds/farStun_hit) is the version without the passive; the Bison's hit on itself (:9167) draws nothing; Yield 0.3 (:24074): standby at 1.0 s (:23877); the blur and the target's camera shake (:23814, :23783) are screen only",
    "cues": [
    [0, "voice", "farStun1|farStun2"],
    [0.4, "fx", "farStun_ring", {"x": 0.5, "d": 0.15}],
    [0.7, "fx", "massStun", 10]
    ]
  },
  "instantRush": {
    "why": "Bison.cs RPC_instantRush (:24136-24578), one rank: clip (PlayAnimation(\"instantRush\", 0) :24367), voice instantRush1 / instantRush2 (Random.Range(0, 2) :24408-24467), instantRush_ring (EffectControl life 1; plays its own Sounds/instantRush) and instantRush_dust (life 1, followPosition) created at the cast position, LookRotation(tDir) = the hero's facing (createEffect :24476-24526) at 0; Yield 0.1 (:24572): the 12 m rush (moveSpeed 24 for 0.5 s, :24271; the wardrobe hero doesn't travel; the game wants the target over 12 m away, :5752-5799); Yield 0.5 (:24570): standby at 0.6 s (:24297); no hit and no effect at the target; the motion blur (:24546-24549) is the player's screen only",
    "cues": [
    [0, "voice", "instantRush1|instantRush2"],
    [0, "fx", "instantRush_ring"],
    [0, "fx", "instantRush_dust"]
    ]
  },
  "cleave": {
    "why": "Bison.cs RPC_powerCleave (:25688-26641), the only clip call of cleave (:26252), at max rank (sLv 2) with Power Reel #403 and Power Hammer #304 on (passives on); Power Hammer counts only with a hammer in the main hand (getPowerHammerLv :8192-8236; isHammer :8284-8468, BB's 22 codes in the wardrobe's names, wardrobe/data/item_map.json, plus timeHammer w_bsn69, TTO's fix TTO1102:Bison::isHammer@0x1B4EF30): clip cut in (PlayAnimation(\"cleave\", 0)) at 0 with voice powerCleave1 / powerCleave2, or powerHammer1 / powerHammer2 with a hammer (Random.Range(0, 2) :26318-26450); powerCleave_ring created at the hero, hero rotation (createEffect :26459-26477; EffectControl life 1 + afterLife 1, followPosition, followState; plays its own Sounds/powerCleave) and, Power Reel on, powerReel_ring the same way (:26499-26525; no sound) at 0; the reel's three pull passes at 0, 0.2, 0.4 s (FindAreaTarget 8 m :26554, Yield(2, 0.2) :26628, i++ :25835, i >= 3 :26545) end at 0.6 s, the no-reel wait's time too (Yield(3, 0.6) :26619): at 0.6 s powerCleave (axe) or powerHammer (hammer) created at the hero, scaled as the hero (:26116-26204; life 0.3, followPosition, followState); Yield 0.1 (:26617): the hit at 0.7 s (FindRecTarget 1 m behind to 4 m ahead, :25893) can't reach the 10 m target, so no powerCleave_hit / powerHammer_hit (:25928, :25990); Yield 0.3 (:26608) and 0.2 (:26615): standby at 1.2 s (:26064), the cut of all three",
    "cues": [
    [0, "voice", "powerCleave1|powerCleave2", {"notWorn": ["R", ["stoneClub", "toyHammer", "bdWeapon", "defenderHammer", "defenderHammerR", "barbell", "warlordHammer", "warlordHammerR", "hallowLance", "havocHammer", "havocHammerR", "havocHammerV", "superStarBass", "mummyMace", "goldenHammer", "royalHammer", "royalHammerR", "specialHammer", "legendHammer", "legendHammerR", "timeHammer"]]}],
    [0, "voice", "powerHammer1|powerHammer2", {"worn": ["R", ["stoneClub", "toyHammer", "bdWeapon", "defenderHammer", "defenderHammerR", "barbell", "warlordHammer", "warlordHammerR", "hallowLance", "havocHammer", "havocHammerR", "havocHammerV", "superStarBass", "mummyMace", "goldenHammer", "royalHammer", "royalHammerR", "specialHammer", "legendHammer", "legendHammerR", "timeHammer"]]}],
    [0, "fx", "powerCleave_ring", 0, 1.2],
    [0, "fx", "powerReel_ring", 0, 1.2],
    [0.6, "fx", "powerCleave", {"notWorn": ["R", ["stoneClub", "toyHammer", "bdWeapon", "defenderHammer", "defenderHammerR", "barbell", "warlordHammer", "warlordHammerR", "hallowLance", "havocHammer", "havocHammerR", "havocHammerV", "superStarBass", "mummyMace", "goldenHammer", "royalHammer", "royalHammerR", "specialHammer", "legendHammer", "legendHammerR", "timeHammer"]], "cut": 1.2}],
    [0.6, "fx", "powerHammer", {"worn": ["R", ["stoneClub", "toyHammer", "bdWeapon", "defenderHammer", "defenderHammerR", "barbell", "warlordHammer", "warlordHammerR", "hallowLance", "havocHammer", "havocHammerR", "havocHammerV", "superStarBass", "mummyMace", "goldenHammer", "royalHammer", "royalHammerR", "specialHammer", "legendHammer", "legendHammerR", "timeHammer"]], "cut": 1.2}]
    ]
  },
  "earthRupture": {
    "why": "Bison.cs RPC_earthRupture (:28466-28903) at max rank (sLv 2): clip (PlayAnimation(\"earthRupture\", 0) :28739), voice earthRupture1 / earthRupture2 (Random.Range(0, 2) :28780-28839) and earthRupture_ring created at the hero, hero rotation (createEffect :28848-28864; EffectControl life 2 + afterLife 2, followPosition, followState; its emitters wait 0.2 / 0.8 s; plays its own Sounds/earthRupture) at 0; Yield 0.8 (:28899): RPC_earthRupture_fire2 (sLv != 1, :28620-28634) from the hero + TransformDirection(0, 0.2, 0.4): three waves Instantiated at LookRotation(forward) x Euler(0, 25 i, 0), i = -1, 0, 1 (:8853-8877), ProjectileControl.life 2 (:8892), each moved by Bison_earthRupture at its ProjectileControl.velocity (0, 0, 12) along its own forward, set again every FixedUpdate, and Destroyed at 2 s (Bison_earthRupture.cs:96-127): 24 m, through every target (OnCollisionEnter only hits, :131-190), the 10 m target included; Yield 0.7 (:28891): standby at 1.5 s (:28669), the ring's cut",
    "cues": [
    [0, "voice", "earthRupture1|earthRupture2"],
    [0, "fx", "earthRupture_ring", 0, 1.5],
    [0.8, "fx", "earthRupture", {"y": 0.2, "d": 0.4, "rot": [0, -25, 0]}],
    [0.8, "fx", "earthRupture", {"y": 0.2, "d": 0.4}],
    [0.8, "fx", "earthRupture", {"y": 0.2, "d": 0.4, "rot": [0, 25, 0]}]
    ]
  },
  "earthSmasher": {
    "why": "Bison.cs RPC_earthSmasher (:28935-29585) at max rank (sLv 2): clip with the game's 0.2 s fade (PlayAnimation(\"earthSmasher\", 0.2f) :29390), voice earthSmasher1 / earthSmasher2 (Random.Range(0, 2) :29431-29490) and earthSmasher_ring created at the hero, hero rotation (createEffect :29499-29517; EffectControl life 1 + afterLife 3, followPosition, followState; plays its own Sounds/earthSmasher) at 0; Yield 0.8 (:29577): moveSpeed 2 for the leap (:29082; 1.2 m in the game, the wardrobe hero doesn't travel); Yield 0.6 (:29583): at 1.4 s earthSmasher Instantiated at the hero, hero rotation (:29126-29144; life 2; its rocks 1 m ahead in the prefab); the 7 m hit (:29193) can't reach the 10 m target, so no nAttack_hit (:29222); Yield 1.2 (:29572) and 0.6 (:29579): standby at 3.2 s (:29320), the ring's cut; the shake, blur and zooms (:29120, :29174, :29549, :29299) are the player's screen only",
    "cues": [
    [0, "voice", "earthSmasher1|earthSmasher2"],
    [0, "fx", "earthSmasher_ring", 0, 3.2],
    [1.4, "fx", "earthSmasher"]
    ]
  },
  "magmaClutter": {
    "why": "Bison.cs RPC_magmaClutter (:31242-31903), one rank: clip (PlayAnimation(\"magmaClutter\", 0) :31724) and magmaClutter_ring1 created at the hero, hero rotation (createEffect :31833-31849; EffectControl life 1 + afterLife 1, followPosition, followState; its emitters 1.5 m ahead wait 0.3 s; plays its own Sounds/magmaClutter1) at 0; BB's voice Voices/magmaClutter1 / magmaClutter2 (Random.Range(0, 2) :31765-31824) is in none of BB's files (Cannot find magmaClutter1 voice): TTO plays Sounds/magmaClutter1 / magmaClutter2 there (TTO1102 Bison.<RPC_magmaClutter>d__179::MoveNext@0x1B68900, pseudo/Bison.c:7483-7554), taken as TTO's fix (plans/fx_sheep/decisions.md 10); moveSpeed 5 (:31733), the lift at 0.3 s (Yield 0.3 :31896; FindAreaTarget 1 m ahead, radius 2, :31413); Yield 0.5 (:31882): at 0.8 s the dash (moveSpeed 5 :31495; the wardrobe hero doesn't travel) and magmaClutter_ring2 created at the hero, hero rotation (:31500-31518; life 1 + afterLife 0.5, followPosition, followState; plays its own Sounds/magmaClutter2; its Shuriken burst read from TTO's copy, as the weapons' Shuriken, NOTES.md 2026-11-12); Yield 0.2 (:31880): the gore at 1.0 s (FindRecTarget to 2 m ahead, :31568) can't reach the 10 m target (and BB has no magmaClutter_hit, :9203); Yield 0.3 (:31884): standby at 1.3 s (:31654), both rings' cut; the shake (:31389) is screen only",
    "cues": [
    [0, "sound", "magmaClutter1|magmaClutter2"],
    [0, "fx", "magmaClutter_ring1", 0, 1.3],
    [0.8, "fx", "tto/magmaClutter_ring2", 0, 1.3]
    ]
  },
  "calamityHammer": {
    "why": "Bison.cs RPC_calamityHammer (:31959-32397), one rank, a target skill: clip (PlayAnimation(\"calamityHammer\", 0) :32273), voice calamityHammer (one file, :32314-32332) and calamityHammer_ring created at the hero, hero rotation (createEffect :32343-32360; EffectControl life 3 + afterLife 1, followPosition, followState; its slam emitters 3.5 m ahead wait 2.1 s; plays its own Sounds/calamityHammer_ring) at 0; Yield 2.1 (:32387): the slam's hit 3.5 m ahead (radius 3, :32117; drawn by the ring's delayed emitters) and OnCalamityHammer (:32156): ten passes 1.5 s apart (i < 10 :32564, Yield(2, 1.5) :32635) while the hero lives and the target exists (:32574, :32593), each RPC_calamityHammer_fire at the target's position of that moment (:32601): Yield 0.3 (:32895), then calamityHammer_fire Instantiated there, Quaternion.identity (:32779-32797; EffectControl life 1 + afterLife 1; plays its own Sounds/calamityHammer_fire), so at 2.4, 3.9 ... 15.9 s on the 10 m target point, cut at 10 s (the standing rule: the six up to 9.9 s); Yield 0.2 (:32394): standby at 2.3 s (:32203), the ring's cut; the blur and the shakes (:32182, :32820) are screen only",
    "cues": [
    [0, "voice", "calamityHammer"],
    [0, "fx", "calamityHammer_ring", 0, 2.3],
    [2.4, "fx", "calamityHammer_fire", 10],
    [3.9, "fx", "calamityHammer_fire", 10],
    [5.4, "fx", "calamityHammer_fire", 10],
    [6.9, "fx", "calamityHammer_fire", 10],
    [8.4, "fx", "calamityHammer_fire", 10],
    [9.9, "fx", "calamityHammer_fire", 10]
    ]
  }
```
