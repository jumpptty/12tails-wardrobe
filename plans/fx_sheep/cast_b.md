# Sheep effects + sounds research: cast3, second half (cast_b)

Scope: the 12 skills whose coroutine plays `cast3` from Light Bind on: lightBind, illuminate, feather, allFeather,
divinitySword, divinitySpear, seal (`RPC_seal`), repel, reverse, divinityAxe, edenSanctuary (`RPC_edenSanctuary`),
worldEncarta. Research only (recipe steps 1-3). Line numbers are `C:\Users\Jump\Desktop\12tails\DecompiledSource\Sheep.cs`
unless another file is named. Times are seconds from the start of `cast3`. Distance 0 = at the hero. Max rank, and the
skill-altering passives on (decisions.md): Free Cast 2 (#132) + Return Cast (#431), Floating Wing (#423), Intense Bind
(#403), Blinding Light (#413).

Read-only probes, in `checks\fx_sheep_research\cast_b\`: `probe.json` (`wardrobe_fx.py sheep --probe` on every effect
named here, summarised with own_skills' `summarize.py`), `containers.py` (the Resources names under `sheep/`),
`tto_strings.py` (string literals per TTO coroutine), `pool.json` (the pool below, checked as valid JSON). I also ran
cast_a's `probe_fields.py` (read only) for the hero prefab's fields.

## Read this first

1. **The Cast tile can lock onto one skill (page bug, not a cue job).** `fxStart` (`wardrobe/index.html:3416-3428`)
   picks a pool member only `if (step === 0 || !e.skills[FX.pick])`, and only when the clip's own entry has `skills`.
   In "Cast: cast1 cast2*@0 cast3~", `cast3` is step 2. Unless `cast1` is itself a pool with the same skill keys, the
   first play picks at random and every later play of the tile keeps the same `FX.pick`, because the name is still in
   `cast3`'s pool. Fix it one of two ways: make `cast1` (cast_a's `RPC_cast1`) a pool with the same 23 keys, or have
   `fxStart` clear `FX.pick` on step 0. The first way also carries one skill across all three steps.
2. **Seal and Eden Sanctuary never play cast1 / cast2 in the game.** Both start straight from the key press, with no
   cast bar. Seal: `StartCoroutine(RPC_seal(..))` at `:8189`, refused within 12 m of another seal (`sqrMagnitude < 144`,
   `:8170`). Eden: the `shp_edenSanctuary5` branch at `:7539`, refused with "Need a seal in place" when no field exists
   (`:7545-7551`), else `StartCoroutine(RPC_edenSanctuary(..))` at `:7565`. On the page, cast3 always
   comes after cast1 / cast2, so a pick of these two still shows cast1's cues first. Seal also cuts into cast3
   (`PlayAnimation("cast3", 0)`, `:32731`), where every other skill fades in over 0.2 s. A shared step can't do both.
   This is a page question, not a cue question.
3. **Every one of the 12 rolls Free Cast (24 %).** With Return Cast on, a proc draws `returnCast` at the hero, not
   `freeCast`. The hook is `getFreeCast` (`:10054-10125`): `freeCastLv` 2 (`:10049`),
   `Random.Range(0, 100) >= lckAdjust(12 x 2)` fails the roll (`:10070`), `hasSkill(431)` leads to `RPC_returnCast`
   (`:10085-10101`), and the effect is `Instantiate(returnCast, position, rotation)` (`:11651-11661`). Each skill's call
   is at time 0 (lines in the table). Divinity Axe rolls only because Return Cast is on (`:36362-36368`). Eden and World
   Encarta roll even without it (`:37075`, `:38354`). Cue: `[0, "fx", "returnCast", {"p": 0.24}]`. Luck is ignored,
   the same as the Wolf's Double Art. cast_a's 11 skills should carry the same cue.
4. **The cast flash is the hero prefab's `castEffect2` field, not a `Resources.Load`, so the inventory doesn't list it.**
   The Sheep MonoBehaviour's fields (read with cast_a's `probe_fields.py`) are: field 1 = castRing, field 2 =
   castEffect1, field 3 = castEffect2. They are Resources `sheep/effects/castring`, `casteffect1` and `casteffect2`
   (`Sheep.cs:16721-16727`: castRing `:16721`, castEffect1 `:16724`, castEffect2 `:16727`). `castEffect2` is **ready**: EffectControl life 1, no followState, an ImageEmitter and a
   LineEmitter (Delay 0.2), and it plays `sounds/castEffect.wav` itself. Ten of the 12 spawn it at
   `position + TransformDirection(0, 1, 0.7)`, i.e. `{"d": 0.7, "y": 1}`; the ten lines are listed below. World
   Encarta uses `castEffect1` instead, which is **ready** (Animation 0.8 s plus legacy particles, both built), turned
   `Euler(270, 90, 0)`. Eden uses its own `edenSanctuary_ring`, which is **ready** and carries the same 0.7 m / 1 m
   flash inside it.
5. **Most of these skills target someone else, so most of their look is left out.** Nine target an ally (Illuminate,
   Feather, Repel, Reverse, World Encarta) or an enemy (Light Bind and the Divinity trio). Their status marks and
   impacts sit on the target. The hero keeps the voice, the cast flash and the Free Cast roll. Two kept effects sit
   on the ground at or near the hero: All Feather's own wings (the area includes her) and the Seal placed 1 m ahead.
   The Divinity Sword / Spear / Axe strikes are "a target point = 10 m ahead" under the decisions, but all three need
   AlphaTimer, so they are future cues.
6. **Voice and sound names don't collide in this scope.** Every voice here is `<skill>1` / `<skill>2` in `voices/`.
   The `sounds/` files are effect AudioSources (`castEffect`, `edenSanctuary_ring`, `repel` ...). No cue here uses the
   `"sound"` kind.
7. **A BB bug, outside the cue (offer it for the Bible).** `RPC_seal_create` asks for `Voices/sealOfDefense1` /
   `sealOfDefense2` (`:11025`, `:11056`). The rip and the game's Resources container have only `voices/sealofdefend1` /
   `sealofdefend2` (`containers.py`). Unity's `Resources.Load` ignores case but not spelling, so the Seal of Defense
   field is very likely silent in BB. `sealOfAttack1` (`:10889`), `sealOfEarth1` (`:11167`) and `sealOfHeaven1`
   (`:11310`) match their files apart from case. This needs a check in the game. It is a game finding, so offer it to
   the user for the Bible's reference.
8. **TTO matches BB.** Each TTO coroutine loads the same effect and voice names, with the same `RPC_*_fire` / `_hit`
   names: `TTO1102:Sheep.<RPC_lightBind_cast>d__180::MoveNext@0x1e90f30`, `<RPC_illuminate_cast>d__181@0x1e90310`,
   `<RPC_feather_cast>d__182@0x1e88860`, `<RPC_allFeather_cast>d__183@0x1e75e00`,
   `<RPC_divinitySword_cast>d__184@0x1e86c20`, `<RPC_divinitySword_fire>d__185@0x1e877c0`,
   `<RPC_divinitySpear_cast>d__186@0x1e86290`, `<divinitySpear_fire>d__187@0x1e9f3e0`, `<RPC_seal>d__189@0x1e9a880`,
   `<RPC_repel_cast>d__191@0x1e97ac0`, `<RPC_reverse_cast>d__192@0x1e98470`, `<RPC_divinityAxe_cast>d__200@0x1e84ff0`,
   `<RPC_divinityAxe_fire>d__201@0x1e85b80`, `<RPC_edenSanctuary>d__203@0x1e87cf0`,
   `<RPC_worldEncarta_cast>d__206@0x1e9df50`. The TTO waits match BB too (verifier, 2026-11-10: the pseudo-C labels
   most float constants inline, `Waits__Get(DAT_.../*=0.5*/)`): cast3 0.2 s fade everywhere but Seal (0), one 0.5 s wait
   in the single-step casts, 0.3 s after the fire in the Divinity casts, 0.8 s in `RPC_divinitySword_fire`, 1 s in
   `divinitySpear_fire`, 1 s then 0.4 s in `RPC_divinityAxe_fire`. One difference, outside the cues: TTO's
   `RPC_seal_create` loads `Voices/sealofDefend1` / `sealofDefend2` (`pseudo/Sheep.c:30124`, `:30139`), the names
   the files really have, so TTO fixed point 7's BB name. BB is the authority.

## Who is targeted, and where each effect appears

| Skill | Target | On the hero (kept) | On the target / elsewhere (left out) |
|---|---|---|---|
| Light Bind | enemy | castEffect2, returnCast roll | `lightBind` status mark on the enemy (needs AlphaTimer) |
| Illuminate | ally | castEffect2, returnCast roll | `illuminate` at the ally's body centre (ready); `illuminate_hit` heal ticks |
| Feather | ally | castEffect2, returnCast roll | `wing` on the ally's back (ready) |
| All Feather | area: allies within 12 m, herself included | castEffect2, returnCast roll, **`wing` on her back** | wings on the other allies |
| Divinity Sword | enemy | castEffect2, returnCast roll | `divinitySword` at the target's spot (10 m; needs AlphaTimer) |
| Divinity Spear | enemy | castEffect2, returnCast roll | `divinitySpear_ring` on the enemy (ready); 3 `divinitySpear` strikes (10 m; needs AlphaTimer) |
| Seal | ground 1 m ahead | castEffect2, returnCast roll, **`redSeal` / `blueSeal` 1 m ahead** | the seal field (needs Sheep_seal and 3 seals) |
| Repel | ally | castEffect2, returnCast roll | `repel` on the ally (ready) |
| Reverse | ally | castEffect2, returnCast roll | `reverse` on the ally (ready) |
| Divinity Axe | enemy | castEffect2, returnCast roll | `divinityAxe` at the target's spot (10 m; needs AlphaTimer); `divinityAxe_hit` on each enemy |
| Eden Sanctuary | the seal field | edenSanctuary_ring, returnCast roll | `edenSanctuary` at the field (needs AlphaTimer, Sheep_edenSanctuary) |
| World Encarta | ally | castEffect1, returnCast roll | `worldEncarta_ring` (ready) and the `worldEncarta` status (ready) on the ally; `worldEncarta_hit` on enemies |

Targets come from the Bible's reference (`12t_reference/sheep-skill-reference.md`): Light Bind enemy (:494); Illuminate,
Feather ally (:391, :399); Divinity Sword, Spear, Axe enemy (:428, :433, :438); Repel, Reverse ally (:461); World Encarta
ally (:476).

## Per skill: the timeline

Every coroutine starts at case 0 with `actionState = "attack"`, then `PlayAnimation("cast3", ..)`, then the voice.
Everything listed at 0 runs in that same case, before the first `Yield`. In the voice pick, `Random.Range(0, 2) == 0`
plays `<skill>1`, otherwise `<skill>2`. Each voice is in `voices/`.

### lightBind (Light Bind): `$RPC_lightBind_cast$27944`, `:28501-28974`
| t | what | source |
|---|---|---|
| 0 | cast3 (0.2 s fade), voice lightBind1 / 2, getFreeCast, castEffect2 0.7 m ahead 1 m up, `lightBind` status on the enemy (Intense Bind: +1 level, +1 s) | `:28723`, `:28758-28813`, `:28832`, `:28844`, `:28898-28902` |
| 0.5 | standby (Yield 0.5 then case 2) | `:28922`, `:28658` |

Left out: `Effects/lightBind`, made by the status on the enemy (`CharacterControl.cs:39611`, parented to it). It needs
AlphaTimer and it is on an enemy anyway.

### illuminate (Illuminate): `$RPC_illuminate_cast$27959`, `:28975-29478`
| t | what | source |
|---|---|---|
| 0 | cast3, voice illuminate1 / 2, getFreeCast, castEffect2, `illuminate` at the ally's `collider.bounds.center`, status `illuminate` (+2 levels with Blinding Light) | `:29197`, `:29232-29287`, `:29306`, `:29318`, `:29372-29384`, `:29411` |
| 0.5 | standby | `:29433`, `:29132` |

Left out: `illuminate` is on the ally. It is ready (EffectControl life 1, its own `sounds/illuminate`). Also left out:
the status's `illuminate_hit` heal every 3 s on the ally (`CharacterControl.cs:9378-9414`).

### feather (Feather): `$RPC_feather_cast$27972`, `:29479-29957`
| t | what | source |
|---|---|---|
| 0 | cast3, voice feather1 / 2, getFreeCast, castEffect2, status `wing` (Floating Wing #423, else `feather`), chaAdjust(15) | `:29701`, `:29736-29791`, `:29810`, `:29822`, `:29876-29889` |
| 0.5 | standby | `:29910`, `:29636` |

Left out: the `wing` on the ally (see All Feather for where it sits).

### allFeather (All Feather): `$RPC_allFeather_cast$27985`, `:29958-30428`
| t | what | source |
|---|---|---|
| 0 | cast3, voice allFeather1 / 2, getFreeCast, castEffect2; `FindAreaTarget(her position, 12 x rangeMod, 3 x rangeMod, 1 << her layer)`; status `wing` on each, herself included | `:30170`, `:30205-30260`, `:30279`, `:30291`, `:30303-30306`, `:30335-30349` |
| 0.5 | standby | `:30380`, `:30105` |

- The area includes the Sheep. The layer mask is her own layer, and `Damage.FindAreaTarget` (`Damage.cs:963`) scans
  every "Enemy" / "Player" tagged object with no self-exclusion. The reference agrees: every ally in
  `FindAreaTarget(self, ..)`, `:400`. So her own `wing` is "a buff the skill puts on the hero", and it stays.
- Where the status puts it (`CharacterControl.cs:39840-39864`): `Instantiate(wing, zero, her rotation)`, parented to
  her, at `localPosition = (0, 0.85 x mChar.height, -mChar.radius)`. `mChar` is her CharacterController (`CharacterControl.cs:29789`).
  Sheep.prefab's CharacterController is `m_Height 1.5`, `m_Radius 0.3` (`:783-784`). Step by step: y = 0.85 x 1.5 =
  **1.275**, d = -0.3 (behind her).
- It is removed when the status ends (`CharacterControl.cs:18004-18017`, `Destroy(Find("wingFx"))`). The prefab's own
  EffectControl life is 300 s (probe), so the cue needs `kill`. The game's length is chaAdjust(15); 15 s is the base
  before CHA.
- The probe shows `wing` is **ready**: EffectControl plus two ImageEmitters (Wing_L / Wing_R, repeatForever, Delay 1).
  `feather` has the same structure.

### divinitySword (Divinity Sword): `$RPC_divinitySword_cast$27999`, `:30429-30903`; fire `$RPC_divinitySword_fire$28011`, `:30904-31185`
| t | what | source |
|---|---|---|
| 0 | cast3, voice divinitySword1 / 2, getFreeCast, castEffect2; Yield 0.2 | `:30718`, `:30753-30808`, `:30827`, `:30839`, `:30860` |
| 0.2 | case 2: `RPC_divinitySword_fire(target position, hero forward)` (owner, ActionEvent to the others); fire case 0: `divinitySword` at that spot, `LookRotation(hero forward)`; Yield 0.3 | `:30613`, `:31107-31117`, `:30863` |
| 0.5 | standby | `:30653` |
| 1.0 | the hit, 0.2 + 0.8 (fire Yield 0.8, case 2) | `:31137`, `:31044-31072` |

Left out: `divinitySword` needs AlphaTimer (probe: `Sheep_divinitySword: no layout for AlphaTimer`). Future cue (a
target point, 10 m ahead, facing the hero's way): `[0.2, "fx", "divinitySword", {"d": 10}]`.

### divinitySpear (Divinity Spear): `$RPC_divinitySpear_cast$28025`, `:31186-31618`; `$divinitySpear_fire$28036`, `:31619-31984`
| t | what | source |
|---|---|---|
| 0 | cast3, voice divinitySpear1 / 2, getFreeCast, castEffect2; Yield 0.2 | `:31435`, `:31470-31525`, `:31544`, `:31556`, `:31580` |
| 0.2 | `divinitySpear_fire` starts (every client); its case 0: `divinitySpear_ring` on the enemy (`tChar.createEffect(.., its position)`), i = 0, Yield 1; the cast: Yield 0.3 | `:31343`, `:31886-31898`, `:31913`, `:31924`, `:31575` |
| 0.5 | standby | `:31370` |
| 1.2, 2.2, 3.2 | strike i = 0, 1, 2: re-read the target's position, `RPC_divinitySpear_fire` (`divinitySpear` at it, `LookRotation(flat hero-to-target)`), hit; i++, `i < 3` then Yield 1 | `:31749-31809`, `:10739-10770`, `:31826`, `:31840`, `:31924` |

Sums: 0.2 + 1 = 1.2; 1.2 + 1 = 2.2; 2.2 + 1 = 3.2. After the third strike i = 3, so it ends.

Left out:
- `divinitySpear_ring` is on the enemy. It is ready (EffectControl life 4, followPosition, its own
  `sounds/divinitySpear_ring`).
- `divinitySpear` needs AlphaTimer. Future cues: `[1.2, "fx", "divinitySpear", {"d": 10}]`, and the same at 2.2 and 3.2.

### seal (Seal of Attack / Seal of Defense): `$RPC_seal$28053`, `:31985-32839`
| t | what | source |
|---|---|---|
| 0 | `addTimeOut("seal", agiAdjust(12))`, cast3 **cut** (fade 0), getFreeCast, castEffect2; no voice; Yield 0.2 | `:32722`, `:32731`, `:32749`, `:32761`, `:32783` |
| 0.2 | case 2: `nPos = mPos + forward` (1 m ahead), a 4 m raycast down from 2 m up to the ground, `nDir` = the ground normal; sLv 1 = `redSeal`, else `blueSeal`, `FromToRotation(up, nDir)`; `EffectControl.life = chaAdjust(60)`; the last 3 seals kept (the 4th destroys the oldest); a 3rd seal makes a field (`RPC_seal_create`); Yield 0.3 | `:32147-32162`, `:32179-32238`, `:32284`, `:32290-32330`, `:32402-32656`, `:32781` |
| 0.5 | standby | `:32678` |

- `redSeal` / `blueSeal` are **ready**: EffectControl life 60, one ground ImageEmitter (repeatForever). On flat ground
  the rotation is identity.
- Seal of Attack (sLv 1, red) and Seal of Defense (sLv 2, blue) are two castable cards on one coroutine (the reference
  `:449`). The pool below writes them as one member with `"redSeal|blueSeal"` (open question 2).
- Left out: the fields (`sealOfAttack` / `sealOfDefense` / `sealOfEarth` / `sealOfHeaven`, `:10822-11255`). They need
  Sheep_seal and three placed seals. Their voices are `RPC_seal_create`'s, see point 7.
- The page keeps the seal until the next pick (60 s life). With the วนซ้ำ loop on, each round adds another, and
  nothing removes the 4th. A `"kill"` could limit it; I left it out because the game keeps it for 60 s.

### repel (Repel): `$RPC_repel_cast$28070`, `:32840-33266`
| t | what | source |
|---|---|---|
| 0 | cast3, voice repel1 / 2, getFreeCast, castEffect2, status `repel` on the ally, chaAdjust(6) | `:33034`, `:33069-33124`, `:33143`, `:33155`, `:33209` |
| 0.5 | standby | `:33226`, `:32975` |

Left out: `Effects/repel` on the ally's body centre, parented, removed with the status (`CharacterControl.cs:39743-39746`,
`:17953-17957`). Probe: ready (Animation 2 s, 3 StaticMesh rings, sound `repel`, no EffectControl).

### reverse (Reverse): `$RPC_reverse_cast$28079`, `:33267-33695`
| t | what | source |
|---|---|---|
| 0 | cast3, voice reverse1 / 2, getFreeCast, castEffect2, status `reverse` on the ally, chaAdjust(3) | `:33461`, `:33496-33551`, `:33570`, `:33582`, `:33636` |
| 0.5 | standby | `:33659`, `:33402` |

Left out: `Effects/reverse` on the ally (`CharacterControl.cs:39770-39773`, removed `:17975-17979`). It is ready, and
its AudioSource is also the `repel` sound.

### divinityAxe (Divinity Axe): `$RPC_divinityAxe_cast$28134`, `:35975-36446`; fire `$RPC_divinityAxe_fire$28144`, `:36447-36771`
| t | what | source |
|---|---|---|
| 0 | cast3, voice divinityAxe1 / 2, getFreeCast only with Return Cast, castEffect2; Yield 0.2 | `:36253`, `:36288-36343`, `:36362-36368`, `:36381`, `:36409` |
| 0.2 | case 2 (owner): `RPC_divinityAxe_fire(target position, ..)`, ActionEvent to the others; fire case 0: `divinityAxe` at that spot, `Quaternion.identity`, Yield 1; the cast: Yield 0.3 | `:36148-36161`, `:36690-36700`, `:36717`, `:36403` |
| 0.5 | standby | `:36188` |
| 1.2, 1.6, 2.0, 2.4, 2.8 | strikes i = 0-4 (r 3 circle), `divinityAxe_hit` on each struck enemy; Yield 0.4 (case 3, i++) | `:36564-36662`, `:36719`, `:11744-11757` |

Sums: 0.2 + 1.0 = 1.2, then +0.4 each: 1.6, 2.0, 2.4, 2.8. At 3.2, i = 5 and it ends.

Left out:
- `divinityAxe` needs AlphaTimer. Future cue: `[0.2, "fx", "divinityAxe", {"d": 10}]`. Its rotation is world
  identity, and the page's `rot` is after the hero's facing. That is the same thing only if the wardrobe hero faces
  +Z. The axe probably doesn't care.
- `divinityAxe_hit` is on the enemies.

### edenSanctuary (Eden Sanctuary): `$RPC_edenSanctuary$28158`, `:36772-37219`
| t | what | source |
|---|---|---|
| 0 | `addTimeOut(agiAdjust(240))`, cast3, voice edenSanctuary1 / 2, getFreeCast (no gate), `edenSanctuary_ring` at the hero (position, rotation), `edenSanctuary` at the field `jl98IkUjQ5`, `SendMessage("InitEdenSanctuary")` | `:36951`, `:36960`, `:37001-37056`, `:37075`, `:37087-37099`, `:37123-37142` |
| 0.5 | standby | `:37186`, `:36907` |

- `edenSanctuary_ring` is **ready**: EffectControl life 1 + afterLife 1, followPosition, no followState. It holds the
  flash at (0, 1, 0.7), the same as castEffect2, plus a ground RingEmitter, and plays `sounds/edenSanctuary_ring`.
  Eden has no castEffect2 line.
- Left out: `edenSanctuary`. It needs AlphaTimer (probe) and Sheep_edenSanctuary (the inventory), and the field it
  stands on: the current seal field, set by `RPC_seal_create` (`:10834`, `:10970`, `:11112`, `:11255`). A future cue
  needs a spot for it (open question 4).

### worldEncarta (World Encarta): `$RPC_worldEncarta_cast$28180`, `:37948-38425`
| t | what | source |
|---|---|---|
| 0 | cast3, voice worldEncarta1 / 2, `castEffect1` at the hero, rotation x `Euler(270, 90, 0)`; `worldEncarta_ring` at the ally's position; getFreeCast (no gate); status `worldEncarta` (5, chaAdjust(9), ATK); `OnWorldEncarta` | `:38159`, `:38194-38249`, `:38262-38268`, `:38322-38334`, `:38354`, `:38357`, `:38360` |
| 0.5 | standby | `:38386`, `:38094` |

- `castEffect1` is **ready**: Animation `root` 0.8 s, EffectControl life 0.4 + afterLife 1, followPosition, and one
  legacy-particle node at local (0, 0.427, 1.041). Rotated by Euler(270, 90, 0) (Unity applies X then Y):
  - X by 270°: (0, 0.427, 1.041) becomes (0, 1.041, -0.427).
  - Then Y by 90°: (x, z) becomes (z, -x) = (-0.427, 0).
  - So the sparks start at (-0.427, 1.041, 0): about 1 m up, 0.43 m to her left.
- Left out:
  - `worldEncarta_ring` on the ally (ready).
  - The status's `Effects/worldEncarta` on the ally's body centre (`CharacterControl.cs:39886-39911`; Animation 2.03 s
    plus a **looping** AudioSource).
  - `OnWorldEncarta`'s `worldEncarta_hit` on the enemies next to the ally (`:11858-11912`).

## The cue entry (the shared `cast3` pool, my 12 members)

`cast3` is shared by 23 skills. These members go in the `skills` map next to cast_a's 11; the editor writes the outer
`why`. Checked as valid JSON (`checks\fx_sheep_research\cast_b\pool.json`). There is no `cut`: no effect here has
followState (probe). Kept effects that play their own sound: castEffect2 (`castEffect`), edenSanctuary_ring, returnCast
(none), wing (none), redSeal / blueSeal (none). The `"voice"` cues are the `voices/` files.

```json
{
  "cast3": {
    "why": "(the editor's merge line: cast_a's 11 skills + these 12, one per play at even chance)",
    "skills": {
      "lightBind": {
        "why": "Sheep.cs RPC_lightBind_cast (:28501-28974, enemy target): Free Cast roll at the start (getFreeCast :28832; Free Cast 2 + Return Cast #431 on: 24 %, Random.Range(0, 100) < lckAdjust(12 x 2) :10070, returnCast at the hero :10085-10101, Instantiate :11651-11661); clip cast3 (0.2 s fade, :28723) and voice lightBind1 / lightBind2 (Random.Range(0, 2), :28758-28813) at 0; castEffect2 (the Sheep prefab's castEffect2 field = Resources sheep/effects/castEffect2) at the hero 0.7 m ahead 1 m up (TransformDirection(0, 1, 0.7), :28844; plays its own Sounds/castEffect); Yield 0.5 (:28922): standby 0.5 s (:28658); left out: the lightBind status's Effects/lightBind on the enemy (RPC_AddStatus :28899-28902, CharacterControl.cs:39611; at the target, needs AlphaTimer); Intense Bind #403 changes only the status level and duration",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "voice", "lightBind1|lightBind2"],
        [0, "fx", "castEffect2", {"d": 0.7, "y": 1}]
        ]
      },
      "illuminate": {
        "why": "Sheep.cs RPC_illuminate_cast (:28975-29478, ally target): Free Cast roll (getFreeCast :29306; 24 %, returnCast, :10070-10101); clip cast3 (:29197) and voice illuminate1 / illuminate2 (:29232-29287) at 0; castEffect2 0.7 m ahead 1 m up (:29318; plays Sounds/castEffect); standby 0.5 s (Yield :29433, :29132); left out: Effects/illuminate at the ally's body centre (createEffect(.., collider.bounds.center), :29372-29384, at the target; ready) and the illuminate status's 3 s heal tick illuminate_hit on the ally (RPC_AddStatus :29411, CharacterControl.cs:9378-9414); Blinding Light #413 changes only the status level",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "voice", "illuminate1|illuminate2"],
        [0, "fx", "castEffect2", {"d": 0.7, "y": 1}]
        ]
      },
      "feather": {
        "why": "Sheep.cs RPC_feather_cast (:29479-29957, ally target): Free Cast roll (getFreeCast :29810; 24 %, returnCast, :10070-10101); clip cast3 (:29701) and voice feather1 / feather2 (:29736-29791) at 0; castEffect2 0.7 m ahead 1 m up (:29822; plays Sounds/castEffect); standby 0.5 s (Yield :29910, :29636); left out: the wing status (Floating Wing #423 on: wing, not feather, :29876-29889) puts Effects/wing on the ally's back for chaAdjust(15) (CharacterControl.cs:39840-39864; at the target)",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "voice", "feather1|feather2"],
        [0, "fx", "castEffect2", {"d": 0.7, "y": 1}]
        ]
      },
      "allFeather": {
        "why": "Sheep.cs RPC_allFeather_cast (:29958-30428, every ally within 12 m of the Sheep, herself included: FindAreaTarget(her position, 12, 3, her own layer) :30303-30306): Free Cast roll (getFreeCast :30279; 24 %, returnCast, :10070-10101); clip cast3 (:30170) and voice allFeather1 / allFeather2 (:30205-30260) at 0; castEffect2 0.7 m ahead 1 m up (:30291; plays Sounds/castEffect); the wing status on her at 0 (Floating Wing #423 on: wing, :30335-30349, chaAdjust(15)): Effects/wing parented to her at (0, 0.85 x height, -radius) = 1.275 m up, 0.3 m behind (CharacterController height 1.5, radius 0.3, Sheep.prefab:783-784; CharacterControl.cs:39840-39864), destroyed when the status ends (:18004-18017; EffectControl life 300, so kill 15 = the 15 s before CHA); standby 0.5 s (Yield :30380, :30105); left out: the wings on the other allies (at the targets)",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "voice", "allFeather1|allFeather2"],
        [0, "fx", "castEffect2", {"d": 0.7, "y": 1}],
        [0, "fx", "wing", {"d": -0.3, "y": 1.275, "kill": 15}]
        ]
      },
      "divinitySword": {
        "why": "Sheep.cs RPC_divinitySword_cast (:30429-30903, enemy target): Free Cast roll (getFreeCast :30827; 24 %, returnCast, :10070-10101); clip cast3 (:30718) and voice divinitySword1 / divinitySword2 (:30753-30808) at 0; castEffect2 0.7 m ahead 1 m up (:30839; plays Sounds/castEffect); Yield 0.2 (:30860): RPC_divinitySword_fire at the target's spot (:30613); Yield 0.3 (:30863): standby 0.5 s (:30653); left out: Effects/divinitySword at that spot at 0.2 s, turned the hero's way (Instantiate(.., LookRotation(hero forward)), :31107-31117; a target point = 10 m ahead) needs AlphaTimer; its hit 0.8 s later, at 1.0 s (:31137, :31044-31072)",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "voice", "divinitySword1|divinitySword2"],
        [0, "fx", "castEffect2", {"d": 0.7, "y": 1}]
        ]
      },
      "divinitySpear": {
        "why": "Sheep.cs RPC_divinitySpear_cast (:31186-31618, enemy target): Free Cast roll (getFreeCast :31544; 24 %, returnCast, :10070-10101); clip cast3 (:31435) and voice divinitySpear1 / divinitySpear2 (:31470-31525) at 0; castEffect2 0.7 m ahead 1 m up (:31556; plays Sounds/castEffect); Yield 0.2 (:31580): divinitySpear_fire starts (:31343); Yield 0.3 (:31575): standby 0.5 s (:31370); left out: divinitySpear_ring on the enemy at 0.2 s (tChar.createEffect at its position, :31886-31898; on the target; ready) and the three strikes 1 s apart at 1.2 / 2.2 / 3.2 s (Yield 1 :31924, i < 3 :31840), each Effects/divinitySpear at the target's spot (RPC_divinitySpear_fire :10739-10770; a target point = 10 m ahead) needs AlphaTimer",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "voice", "divinitySpear1|divinitySpear2"],
        [0, "fx", "castEffect2", {"d": 0.7, "y": 1}]
        ]
      },
      "seal": {
        "why": "Sheep.cs RPC_seal (:31985-32839; Seal of Attack sLv 1 / Seal of Defense sLv 2, instant: no cast bar, started straight from the press :8189): no voice; Free Cast roll (getFreeCast :32749; 24 %, returnCast, :10070-10101); clip cast3 as a cut (PlayAnimation(cast3, 0), :32731) and castEffect2 0.7 m ahead 1 m up (:32761; plays Sounds/castEffect) at 0; Yield 0.2 (:32783): the seal on the ground 1 m ahead (mPos + forward, raycast down to the ground :32147-32162): redSeal for Seal of Attack, blueSeal for Seal of Defense (:32179-32238), lasting chaAdjust(60) (:32284; EffectControl life 60); Yield 0.3 (:32781): standby 0.5 s (:32678); left out: the seal field a 3rd seal makes (RPC_seal_create :32402-32656, :10789-11255: sealOfAttack / Defense / Earth / Heaven need Sheep_seal and three placed seals) and its voices",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "fx", "castEffect2", {"d": 0.7, "y": 1}],
        [0.2, "fx", "redSeal|blueSeal", {"d": 1}]
        ]
      },
      "repel": {
        "why": "Sheep.cs RPC_repel_cast (:32840-33266, ally target): Free Cast roll (getFreeCast :33143; 24 %, returnCast, :10070-10101); clip cast3 (:33034) and voice repel1 / repel2 (:33069-33124) at 0; castEffect2 0.7 m ahead 1 m up (:33155; plays Sounds/castEffect); standby 0.5 s (Yield :33226, :32975); left out: the repel status's Effects/repel on the ally's body centre for chaAdjust(6) (RPC_AddStatus :33209, CharacterControl.cs:39743-39746, removed :17953-17957; at the target; ready)",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "voice", "repel1|repel2"],
        [0, "fx", "castEffect2", {"d": 0.7, "y": 1}]
        ]
      },
      "reverse": {
        "why": "Sheep.cs RPC_reverse_cast (:33267-33695, ally target): Free Cast roll (getFreeCast :33570; 24 %, returnCast, :10070-10101); clip cast3 (:33461) and voice reverse1 / reverse2 (:33496-33551) at 0; castEffect2 0.7 m ahead 1 m up (:33582; plays Sounds/castEffect); standby 0.5 s (Yield :33659, :33402); left out: the reverse status's Effects/reverse on the ally's body centre for chaAdjust(3) (RPC_AddStatus :33636, CharacterControl.cs:39770-39773, removed :17975-17979; at the target; ready)",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "voice", "reverse1|reverse2"],
        [0, "fx", "castEffect2", {"d": 0.7, "y": 1}]
        ]
      },
      "divinityAxe": {
        "why": "Sheep.cs RPC_divinityAxe_cast (:35975-36446, enemy target): Free Cast roll, only with Return Cast #431 (on: :36362-36368; 24 %, returnCast, :10070-10101); clip cast3 (:36253) and voice divinityAxe1 / divinityAxe2 (:36288-36343) at 0; castEffect2 0.7 m ahead 1 m up (:36381; plays Sounds/castEffect); Yield 0.2 (:36409): RPC_divinityAxe_fire at the target's spot (:36148-36161); Yield 0.3 (:36403): standby 0.5 s (:36188); left out: Effects/divinityAxe at that spot at 0.2 s (Instantiate(.., Quaternion.identity), :36690-36700; a target point = 10 m ahead) needs AlphaTimer; its 5 strikes at 1.2 / 1.6 / 2.0 / 2.4 / 2.8 s (Yield 1 :36717, Yield 0.4 :36719) and divinityAxe_hit on each struck enemy (:36651, :11744-11757; at the target)",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "voice", "divinityAxe1|divinityAxe2"],
        [0, "fx", "castEffect2", {"d": 0.7, "y": 1}]
        ]
      },
      "edenSanctuary": {
        "why": "Sheep.cs RPC_edenSanctuary (:36772-37219; instant, started straight from the press :7539-7565, needs a seal field in place): Free Cast roll with no Return Cast gate (getFreeCast(.., 5) :37075; 24 %, returnCast, :10070-10101); clip cast3 (:36960) and voice edenSanctuary1 / edenSanctuary2 (:37001-37056) at 0; edenSanctuary_ring at the hero (createEffect(.., position, rotation), :37087-37099; its own flash 0.7 m ahead 1 m up and a ground ring; plays its own Sounds/edenSanctuary_ring); no castEffect2; standby 0.5 s (Yield :37186, :36907); left out: Effects/edenSanctuary at the current seal field (jl98IkUjQ5, :37123-37142; the field from RPC_seal_create :10834-11255) needs AlphaTimer, Sheep_edenSanctuary and a placed field",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "voice", "edenSanctuary1|edenSanctuary2"],
        [0, "fx", "edenSanctuary_ring"]
        ]
      },
      "worldEncarta": {
        "why": "Sheep.cs RPC_worldEncarta_cast (:37948-38425, ally target): clip cast3 (:38159) and voice worldEncarta1 / worldEncarta2 (:38194-38249) at 0; castEffect1 (the prefab's castEffect1 field = Resources sheep/effects/castEffect1) at the hero turned hero rotation x Euler(270, 90, 0) (:38262-38268; no castEffect2); Free Cast roll with no Return Cast gate (getFreeCast(.., 5) :38354; 24 %, returnCast, :10070-10101); standby 0.5 s (Yield :38386, :38094); left out: worldEncarta_ring at the ally's feet (tChar.createEffect, :38322-38334; at the target; ready), the worldEncarta status's Effects/worldEncarta on the ally for chaAdjust(9) (:38357, CharacterControl.cs:39886-39911, a looping sound), and OnWorldEncarta's hits on enemies next to the ally every 0.5 s (:38360, worldEncarta_hit :11858-11912)",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "voice", "worldEncarta1|worldEncarta2"],
        [0, "fx", "castEffect1", {"rot": [270, 90, 0]}]
        ]
      }
    }
  }
}
```

How sure: high on every time and name (each wait traced case by case and added up above). The wing's height assumes a
hero scale of 1. I did not read the CharacterController scale.

## Left out, by missing part (for the inventory)

- `lightBind` (Light Bind's mark on the enemy): needs AlphaTimer. It is also on the target, so it stays out.
- `divinitySword`: needs AlphaTimer. Future cue at 10 m ahead, 0.2 s.
- `divinitySpear`: needs AlphaTimer. Future cues at 10 m ahead, 1.2 / 2.2 / 3.2 s.
- `divinityAxe`: needs AlphaTimer. Future cue at 10 m ahead, 0.2 s.
- `edenSanctuary`: needs AlphaTimer, Sheep_edenSanctuary (and a seal field).
- `sealOfAttack` / `sealOfDefense` / `sealOfEarth` / `sealOfHeaven` (the seal fields): need Sheep_seal and three
  placed seals.
- On the target, though ready: `illuminate`, `illuminate_hit`, `wing` (Feather, and other allies), `divinitySpear_ring`,
  `divinityAxe_hit`, `repel`, `reverse`, `worldEncarta_ring`, `worldEncarta`, `worldEncarta_hit`.

## Open questions for the user

1. **Show an ally buff on the Sheep herself, as if she cast it on herself?** In the game she can be her own target for
   Illuminate, Feather, Repel, Reverse and World Encarta. Today only their flash and voice show. If yes, add these
   cues. All are ready, and the times come from the tables above. The 0.8 is her collider centre: CharacterController
   center y 0.8, `Sheep.prefab:789`.
   - Illuminate: `[0, "fx", "illuminate", {"y": 0.8}]`
   - Feather: `[0, "fx", "wing", {"d": -0.3, "y": 1.275, "kill": 15}]`
   - Repel: `[0, "fx", "repel", {"y": 0.8, "kill": 6}]`
   - Reverse: `[0, "fx", "reverse", {"y": 0.8, "kill": 3}]`
   - World Encarta: `[0, "fx", "worldEncarta_ring"]` and `[0, "fx", "worldEncarta", {"y": 0.8, "kill": 9}]`. Its sound
     loops; check that the page stops it on `kill`.

   I left them out to match the Wolf (Mass Resurrection's ally mark was left out).
2. **Seal: one pool member with a random red / blue, or two members (Seal of Attack, Seal of Defense)?** Two members
   give the seals twice the share of plays among the 23 skills.
3. **Divinity Spear's ring on the enemy:** it is ready, and it is the only part of the spear the page can draw today.
   Should it come in as a target mark 10 m ahead (`[0.2, "fx", "divinitySpear_ring", {"d": 10}]`)? My reading of the
   decisions says no: it is attached to the enemy.
4. **Eden Sanctuary's field, once built:** where should it stand? 1 m ahead (where one seal goes) or 10 m ahead (the
   target-point rule)? The game puts it at the centre of three seals, each placed 12 m or more from the others.
5. **The Cast tile for Seal and Eden** (Read this first, point 2): accept cast1 > cast2 before them, or give them their
   own one-clip tile?

## Verification (2026-11-10)

A skeptical re-trace by a checker (office PC). Nothing was built or published, and no browser was used. Read-only
probes: `wardrobe_fx.py sheep --probe` on all 31 cast effects, in `checks/fx_sheep_research/verify/cast_probe.json`,
summarised in `cast_probe_summary.txt`. I also re-ran `cast_a/probe_fields.py`.

**What I checked, and found right:**
- **The seven single-step casts** (lightBind, illuminate, feather, allFeather, repel, reverse, worldEncarta), with
  `clip_flow.js` on each: one `Yield(2, 0.5)` and nothing before it. Every cited line for the clip, voice,
  `getFreeCast`, castEffect2 / castEffect1, the target effect and the status is right.
- **castEffect2:** exactly ten spawns, all `position + TransformDirection(0, 1, 0.7f), rotation`: `:28844`, `:29318`,
  `:29822`, `:30291`, `:30839`, `:31556`, `:32761`, `:33155`, `:33582`, `:36381`.
- **Divinity Sword:**
  - case 0 ends with `Yield(2, 0.2)` `:30860`.
  - case 2 starts the fire `:30613`, then `Block_6` -> `IL_6C5`, which is `Yield(3, 0.3)` `:30863`.
  - case 3 sets standby at 0.2 + 0.3 = 0.5 s `:30653`.
  - The fire's case 0 makes the sword `:31117`, then `Yield 0.8` `:31137`. The hit lands at 0.2 + 0.8 = 1.0 s
    (`:31044-31072`).
- **Divinity Spear:**
  - The cast waits `Yield 0.2` `:31580`, then `0.3` `:31575`.
  - `divinitySpear_fire` makes the ring and sets i = 0 at 0.2 s (`:31898`, `:31913`), then `Yield 1` `:31924`.
  - Strikes come at 1.2, 2.2 and 3.2 s, each with i++ `:31826` and the check `i < 3` `:31840`.
- **Divinity Axe:**
  - The cast waits `Yield 0.2` `:36409`, then `0.3` `:36403`.
  - The fire makes the axe at 0.2 s `:36700` and waits `Yield 1` `:36717`. case 2 sets i = 0 at 1.2 s. case 3
    (i++) runs after each `Yield 0.4` `:36719`.
  - The strikes are at 1.2, 1.6, 2.0, 2.4 and 2.8 s. It ends at i >= 5, at 3.2 s.
- **Seal:**
  - Clip cut `PlayAnimation("cast3", 0)` `:32731`, then castEffect2 `:32764` -> `Yield(2, 0.2)` `:32783`.
  - case 2 places the seal: `forward` 1 m ahead `:32147`, sLv 1 = redSeal `:32179`. Then `Yield(3, 0.3)` `:32781`
    and standby at 0.5 s `:32678`.
  - No voice is loaded.
- **Eden:** one `Yield(2, 0.5)` `:37186`. The getFreeCast at `:37075` has no Return Cast gate, and Divinity Axe's at
  `:36362-36368` has one.
- **Free Cast:** the lines check out (`:10049`, `:10070`, `:10085-10101`, `:11651-11661`).
- **All Feather's wing:**
  - The area check is `hitLayer = 1 << her layer` (`:30303`), and `Damage.cs:963-1080` scans every Player / Enemy
    with no self-exclusion.
  - The wing's placement is `localPosition = (0, 0.85 x height, -radius)` (`CharacterControl.cs:39864`). `mChar` is
    the CharacterController (`:29789`).
  - Sheep.prefab: `m_Height 1.5`, `m_Radius 0.3`, `m_Center y 0.8` (`:783`, `:784`, `:789`). That gives 1.275 m up
    and 0.3 m behind.
- **The effect parts**, re-probed: castEffect2, castEffect1, edenSanctuary_ring, wing / feather, redSeal / blueSeal,
  divinitySpear_ring, illuminate, repel, reverse, worldEncarta_ring and worldEncarta are as stated. divinitySword,
  divinitySpear, divinityAxe, lightBind and edenSanctuary all fail on AlphaTimer.
  - castEffect1's spark node is at (0, 0.42668, 1.0414). Rotated by Euler(270, 90, 0), it comes out at
    (-0.427, 1.041, 0).
- **Voices:** every cue's voice is in the rip's `voices/`. There are no `sealOfDefense*` files, only
  `sealofDefend1/2.wav`.
- **The FX.pick page bug** is confirmed. `index.html:3422` is the only place that sets `FX.pick`, and in
  "Cast: cast1 cast2*@0 cast3~" cast3 is step 2.
- **TTO:** all 15 coroutine names and RVAs match `pseudo/Sheep.c`.
- **The Bible:** the target lines `:391`, `:399`, `:400`, `:428`, `:433`, `:438`, `:449`, `:461`, `:476` and `:494`
  say what is cited.

**Corrections (made above):**
- Read this first, point 4: (`Sheep.cs:16724-16727`) -> (`Sheep.cs:16721-16727`: castRing `:16721`, castEffect1
  `:16724`, castEffect2 `:16727`). The `public GameObject castRing;` declaration is at `:16721`.
- Read this first, point 2, and edenSanctuary's `why`: Eden `:7540-7551` -> `:7539-7565`.
  - `:7539` is `else if (a2 == "shp_edenSanctuary5")`.
  - `:7545-7551` is the "Need a seal in place" refusal.
  - The start is `this.StartCoroutine_Auto(this.RPC_edenSanctuary(..))` at `:7565`.
- Read this first, point 5: "Seven target an ally (...) or an enemy (...)" -> "Nine". The lists name 5 allies + 4
  enemies = 9.
- Read this first, point 8: "I did not re-read the waits in TTO: its float constants are data refs, not inline" ->
  the waits were re-read, and they match.
  - The pseudo labels them inline, for example `Waits__Get(DAT_18300469c/*=0.8*/,0)` in
    `<RPC_divinitySword_fire>d__185`, and `/*=0.4*/` and `/*=1*/` in `<RPC_divinityAxe_fire>d__201`.
  - Also added: TTO's `RPC_seal_create` loads `Voices/sealofDefend1` / `2` (`pseudo/Sheep.c:30124`, `:30139`). TTO
    renamed the path to the real files, which backs point 7's BB bug.

**For the editor (not errors in this report):**
- cast_a puts the ally skills' effects on the hero (its open question 1), and this report leaves them out (open
  question 1 here). The 23-member pool needs one rule, and the user picks it.
- The edenSanctuary_ring flash node carries a 90-degree X turn (`rot (0.7071, 0, 0, 0.7071)`) where castEffect2's
  has none. Same position, a different facing.
