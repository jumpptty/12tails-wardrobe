# Cat effects + sounds research: the TTO-only clips (Royal Flush, Crescent Eclipse, Drop Anchor, shikifujin)

Scope: the six TTO clips of `wardrobe/data/cat/clips.json` (`tto: true`, group `skill`): `royalFlush1` (1.0 s),
`crescentEclipse1` (1.0 s), `crescentEclipse2` (1.3 s), `dropAnchor` (1.1 s), `anchorYank` (1.0 s), `shikifujin` (4.8 s).
No BB code plays them. Research only: this file is the only file written in the repo, plus the probe scripts and outputs
in `checks/fx_cat_research/tto/` (git-ignored). Sources:
- TTO's pseudo-C `D:\12tails\DecompiledSource_TTO_2026-11-02\pseudo\Cat.c` (and `CharacterControl.c`), cited as
  `TTO1102:Method@RVA` plus `Cat.c:<line>`;
- capstone over `client\GameAssembly.dll` for the floats Ghidra drops (`dis.py`; the disassemblies `royalFlush_movenext.asm`,
  `royalFlushBursts.asm`, `royalSwordFall.asm`, `eclipse_movenext.asm`), the call-site finder `callers.py`, the function
  printer `fn.py` (pseudo-C minus noise lines);
- the Bible's `12t_reference\cat-skill-reference.md` "TTO Lv 100 skills" (lines 1005-1090; Royal Flush :1009-1041,
  Crescent Eclipse :1043-1069, Drop Anchor :1071-1088);
- TTO's 2026-11-04 bundles on this PC (`D:\12tails-video\tto_assets\2026-11-04`), read with
  `uv run --no-project --with UnityPy --with pillow --with imageio-ffmpeg python -I pipeline/wardrobe_fx_tto.py cat --probe <28 names>`
  -> `checks/fx_cat_research/tto/probe.json`; `compact.txt` (`compact.py`), `comptypes.py` (component types, materials),
  `scripts.txt` (`scripts.py`: node trees and the Cat_* script fields), `catalog.txt` (`catalog.py`: every TTO catalog
  address under `heroes/cat/` against BB's rip), `clipevents.py` (the six AnimationClips: no animation events),
  `calc.py` -> `calc.txt` (every position and time below).

Times are seconds from the start of the clip the cue is keyed by. Every wait is `Cat::Until(start + t)`
(`TTO1102:Cat::Until@0x1B8E910`, `Cat.c:38916`: an absolute time from the coroutine's start, as the Penguin's and the
Sheep's) or `Waits.Get(t)` (a cached WaitForSeconds: a step). The skills have one rank, so max rank changes nothing.

**Released list:** `anchorYank`, `crescentEclipse1`, `crescentEclipse2`, `dropAnchor`, `royalFlush1` are all in it and all
get cues. `shikifujin` is not in it, and no TTO code plays it (section 2.4): no cues.

## Read this first

1. **TTO1102's code with the 2026-11-04 bundles, not TTO1109's timings.** The Bible already carries TTO patch 1.6.2.4
   (09/11/2026, `TTO1109:`, office decompile `DecompiledSource_TTO_2026-11-09`, not on this PC): Royal Flush's clip
   plays x 1.35 and every wait shrinks, Crescent Eclipse's clips x 1.18, Drop Anchor has no recast and no pull pose
   (`AnchorYank(pose = false)`: the `anchorYank` clip is never played), and the VFX are rescaled (`Row6Scaled`), the moon
   placed from the camera (`Cat_eclipseFx::MoonSpot`). This PC has only the 2026-11-04 bundles (and the 2026-11-07 TTO
   install, which is not 1109 either), and the page plays clips at speed 1. So this report follows TTO1102, whose code
   matches these bundles' prefabs, by analogy with Bat decision 44 ("TTO 1102's code is accepted"). Question 1.
2. **No `sounds/` kind and no TTO-only sounds.** The Cat's TTO coroutines play voices only, through
   `Cat::Row6Voice(a, b)@0x1B8CB50` (`Cat.c:38622`): `GameAssets/characters/heroes/cat/voices/<a or b>`, a 50 % pick when
   b is given (`Random.Range(0, 2)`, :38662), `PlayOneShot` volume 1 for the owner (0.75 others). Every name is in BB's
   rip `voices/`: jokerCard1/2, cheer, finalMove1/2, battle, follow. Every other sound is a prefab's own AudioSource
   (BB's `sounds/` recordings: the catalog's 48 Cat sounds are BB's 48, `catalog.txt`) or a clip a Cat_* script plays
   (throw1, twoPair, throw_hit, disarm_hit: also BB's). So no `"sound"` cues and no part P8 (the Penguin's TTO sounds).
3. **All 28 TTO-only Cat prefabs are probed** (section 5). The catalog has 104 Cat effects, 28 not in BB's rip:
   10 crescentEclipse_*, 7 dropAnchor_*, 9 royalFlush_*, and two status looks (eclipsed, dealersMark). No arcana style
   (no `heroes/cat/arcana/`). No prefab has `followState`; two have `followPosition` (royalFlush_shuffle,
   crescentEclipse_trail, both spawned owned).
4. **Row6Begin cuts the clip in** (`Cat::Row6Begin@0x1B8B8B0`, `Cat.c:38721`: `PlayAnimation(clip, 0)`, capstone
   0x1B8B9F9 `xorps xmm2, xmm2`, wrapMode Once), unlike the Penguin's 0.1. `Row6PlayClip@0x1B8BD00` (`:38901`) changes
   clip with a 0.08 s fade (Crescent Eclipse's second clip). SEQ lines below say so (`!`, `^`).
5. **Four Cat scripts and two code movers are parts the page lacks** (section 6): `Cat_royalCard`, `Cat_royalHandBanner`,
   `Cat_eclipseFx` (moon and blade modes; the blade carries a copy of the Cat's own worn weapon), `Cat.RoyalSwordFall`,
   `Cat.DropAnchorFlight`, two Unity shaders (`Unlit/Color`, `Unlit/Texture`), the cel shader's fresnel term, an inactive
   node a part switches on, and two legacy blends the TTO exporter does not map. Per the rule every effect is cued anyway,
   with the part it needs named.
6. **Hero stays in place.** Crescent Eclipse leaps 5.5 m up and dives onto the target; the page's hero doesn't travel
   (the clips' Root is in place: `clips.json`), so the whole skill is drawn about the hero (Penguin decision 8, Bat
   decision 10, Feral Strike). The leap variant's numbers are in 2.2. Question 4.
7. **Drop Anchor is one tile with both clips**: the throw, the 6 s wait on the idle stance, the yank (`anchorYank`), as the
   game plays it when the player does not press again (section 2.3). Question 6.
8. **No camera effects.** `Row6Shake` (owner camera shake), `AddCamereShake` and `CameraEffect.AddColorRamp("redRamp")`
   (Royal Flush's sword, Crescent Eclipse's burst) are the player's own screen: left out, as the Wolf's (its tto.md Q7).

---

## 1. Shared machinery (`TTO1102:Cat`)

- **`Row6Begin(command, mPos, tDir, clip)@0x1B8B8B0`** (`Cat.c:38721`): actionState `attack`, the command, the hero put at
  mPos and turned to `mPos + vFlat(tDir)`, `PlayAnimation(clip, 0)` (a cut), wrapMode Once, moveSpeed 0.
- **`Row6End(command)@0x1B8BB10`** (`:38821`): `standby`, only while the action is still this command (`Row6Doing`).
- **`Row6Spawn(name, pos, rot, owned)@0x1B8C020`** (`:38515`): loads `GameAssets/characters/heroes/cat/effects/<name>`
  (`Row6Prefab`, `:38454`, logs `Cannot find <name> effect`); owned -> `CharacterControl.createEffect`, else a bare
  `Object.Instantiate`. Owned here: `royalFlush_shuffle`, `crescentEclipse_trail`.
- **`Row6Voice(a, b)@0x1B8CB50`** (`:38622`): above (Read this first 2).
- **`FlatFace(from, to, fallback)@0x1B84040`** (`:38938`): the flat unit direction from -> to, else the fallback.
- **Targets and spots** (`Cat::DoRow6Skill@0x1B81200`, `Cat.c:37828`): Royal Flush reach 12 (:37871), Crescent Eclipse 14
  (:37922), Drop Anchor 16 (:37925); `Row6Spot@0x1B8C2F0` (:39112) aims at the target when 1 m < flat distance <= reach
  and grounds it. With the target 10 m ahead every spot is the target's feet, 10 m ahead, and `face` = the hero's facing.
- **Status looks** (`CharacterControl::AddCatRow6Fx@0x24ABBB0`, `CharacterControl.c:5791`): `cat/effects/<status>`
  parented to the holder's body, `Cat_row6StatusFx.Init` (eclipsed, dealersMark); `Cat_anchorChain.Bind` from
  `<addStatus>d__481::MoveNext` at 0x24FD823 (`callers.py`) draws the anchored foe's chain (`dropAnchor_chain`). All on
  foes: left out (section 3).

## 2. Per skill

### 2.1 Royal Flush (`royalFlush1`, 1.0 s; cell 452) - released

Coroutine `TTO1102:Cat.<RPC_royalFlush>d__306::MoveNext@0x1BC7700` (`Cat.c:23015-23490`), then
`<RoyalFlushBursts>d__307::MoveNext@0x1BF3F60` (`:25791-26085`) and `<RoyalSwordFall>d__308::MoveNext@0x1BF4840`
(`:26104-26412`). `centre` = mPos + toCentre = the target spot; `face` = FlatFace(mPos, centre, forward).
- **0.00**: `Row6Begin("royalFlush", ..., clip "royalFlush1")` (:23108); `addTimeOut(agiAdjust(120))`; the hand = code /
  1000 (:23117-23127), `DealHand(hand, code % 1000)` (:23137); `Row6Voice("jokerCard1", "jokerCard2")` (:23141);
  `royalFlush_shuffle` **owned** at the hero, hero rotation (:23154; EffectControl 0.6, followPosition, own sound
  powerShuffle); `start` = now; `Until(start + RoyalFlushThrowAt[0])`.
- **Card i at RoyalFlushThrowAt[i] = 0.52, 0.58, 0.64, 0.70, 0.76** (`Cat::.cctor@0x1B8E980`, `Cat.c:43037`; the wait is
  `addss xmm6, [rcx + rax*4 + 0x20]`, capstone 0x1BC7E72): `royalFlush_card`, world, at hero + 0.45 face + 1.3 up
  (:23215-23226, capstone 0x1BC7B50 / 0x1BC7B7D), rotation `LookRotation(FlatFace(mPos, slot, face))` (:23228-23234),
  `SetCard(cards[i])` and `Deal(from, slot, rot, flight 0.35, arc 1.6)` (:23262-23264). The slot is
  `RoyalFlushSlot(centre, face, i)@0x1B8DA00` (:39978) = centre + AngleAxis((i - 2) x 150 x 0.25, up) x face x 3.2,
  grounded: a 150 deg fan of radius 3.2 beyond the target.
- **1.00**: `Until(start + 1)` (capstone 0x1BC7EB2) -> `Row6End` (:23314). The clip is 1.0 s.
- **1.11**: `Until(start + ThrowAt[4] + 0.35)` (capstone 0x1BC7FC9-0x1BC7FD0) -> `royalFlush_table` at the centre,
  `LookRotation(face)` (:23352; EffectControl 3.6, own sound gamble_ring 0.8).
- **Flip i at 1.2 + 0.12 i** (`Until(i x 0.12 + start + 1.2)`, :23371) -> `Cat_royalCard.Flip(0.18)` (:23394).
- **1.95**: `Until(start + 1.95)` (capstone 0x1BC81BF): `royalFlush_bang` at centre + 2.4 up, `LookRotation(face)`
  (:23431; own sound gamble_hit); `royalFlush_hand` at centre + 3.4 up, identity, `Cat_royalHandBanner.Show(hand)`
  (:23450-23466); **hand > 5** (Full House and better) -> `Row6Voice("cheer")` (:23468-23469); the owner's payout; then
  `RoyalFlushBursts` (:23480).
- **RoyalFlushBursts**: bursts = `RoyalFlushBurstCount[hand]` (1, 2, 2, 3, 3, 3, 4, 4, 5, 5); burst k: `royalFlush_burst`
  (the last `royalFlush_burstBig`) at the centre, `LookRotation(face)` (:25896); every card `GlowPulse(1, 0.3)` (the last
  burst 1.6) (:25916); `Row6Shake(0.15 / 0.45)`; the hits; `Waits.Get(0.16)` (capstone 0x1BF446E) (:25935). After the last:
  hand != 9 -> `Fold` = every card `Shatter()` (:25946). **Royal Flush (9):** `Row6Voice("finalMove1", "finalMove2")`
  (:25950); `royalFlush_sword` at centre + 5 up, `LookRotation(face)` (:25981); every card `Gather(centre + 7.5 up, 0.35)`
  (:26004); `RoyalSwordFall` (:26018); `Waits.Get(0.8)` (capstone 0x1BF4794) -> `royalFlush_swordHit` at the centre,
  `LookRotation(face)` (:26044; own sounds grandCasino_hit7 + Boom's supportFire_hit), `Row6Shake(1)`, the redRamp
  colour grade (camera, left out), the sword hit.
- **RoyalSwordFall** (`:26104-26412`): from its spawn point it spins in (`AngleAxis((1 - s) 360, up)`, s = smoothstep(e /
  0.35)), grows 0.15 -> 1, rises 1.2 m (0.35-0.68 s, smoothstep / 0.33), falls to centre - 1.1 up by 0.8 s (f = ((e -
  0.68) / 0.12)^2); held 0.6 s (`Waits.Get(0.6)`); then sinks (centre - up (2.5 k^2 + 1.1), k = 2 (now - s0)) shrinking
  to 0.6 over 0.5 s and is destroyed: 2.75 + 1.9 = **4.65**.
- Sums (calc.txt): bursts 1.95, 2.11, 2.27, 2.43, 2.59; sword 2.75; sword hit **3.55** (Bible :1037: 1.95 + 0.16 k,
  sword 3.55) OK.

**The hand (question 2, recommended: always Royal Flush).** The hand is a weighted roll on the caster's client
(`RoyalFlushOdds` 160 / 260 / 190 / ... / 12 per 1000 plus two `lckAdjust(12)` step-ups, Bible :1019), not a rank. Royal
Flush is the only hand with the sword, the cheer + finalMove voices and all five bursts; at the game's odds it would show
on 1 play in 50-60. Recommended: always hand 9 (the skill's namesake and its whole look, as "top rank"). The cards then
are `DealHand(9, v)` (`Cat::DealHand@0x1B805E0`, `Cat.c:39394`): ranks 1-5 (`<PrivateImplementationDetails>` [1, 2, 3, 4,
5], :39651) of **one suit** drawn by a `System.Random(hand x 7919 + 7919 + v)` (:39444), the five in a shuffled order; a
card = rank + 6 x suit (suit 0 spade, 1 heart, 2 diamond, 3 club: `Cat_royalCard.SuitColors` blue / red / gold / green,
`Cat.c:48035-48057`). Question 3: the suit at random per play (recommended) or fixed spades.

Positions (hero at 0 facing +d, x right; calc.txt):

| card | slot (x, d) | yaw | thrown | lands | flip | first pulse after spawn | gather after spawn |
|---|---|---|---|---|---|---|---|
| 0 | -3.091, 10.828 | -15.932 | 0.52 | 0.87 | 1.20 | 1.43 | 2.23 |
| 1 | -1.948, 12.539 | -8.831 | 0.58 | 0.93 | 1.32 | 1.37 | 2.17 |
| 2 | 0, 13.2 | 0 | 0.64 | 0.99 | 1.44 | 1.31 | 2.11 |
| 3 | 1.948, 12.539 | 8.831 | 0.70 | 1.05 | 1.56 | 1.25 | 2.05 |
| 4 | 3.091, 10.828 | 15.932 | 0.76 | 1.11 | 1.68 | 1.19 | 1.99 |

(flip after spawn = 0.68 + 0.06 i; pulses every 0.16 s from the first, five of them, the last peak 1.6.)

```json
  "royalFlush1": {
    "why": "TTO1102:Cat.<RPC_royalFlush>d__306::MoveNext@0x1BC7700 (Cat.c:23015-23490; plans/fx_cat/tto.md 2.1; hand 9 = Royal Flush, the target 10 m ahead = the centre): 0: Row6Begin(royalFlush, clip royalFlush1) cut in (:23108, Row6Begin@0x1B8B8B0 PlayAnimation(clip, 0)), Row6Voice(jokerCard1, jokerCard2) = a 50 % pick (:23141, Row6Voice@0x1B8CB50 :38662), royalFlush_shuffle owned at the hero (:23154; EffectControl 0.6 followPosition, own powerShuffle); card i at RoyalFlushThrowAt 0.52 + 0.06 i (Cat::.cctor :43037; capstone 0x1BC7E72): royalFlush_card at hero + 0.45 face + 1.3 up (:23215-23226), LookRotation(FlatFace(mPos, slot)) (:23228-23234), SetCard + Deal(slot, 0.35 s, arc 1.6) (:23262-23264) to RoyalFlushSlot@0x1B8DA00 = centre + AngleAxis((i-2) 37.5 deg) face x 3.2 (:39978; calc.txt); Until 1: Row6End (:23314); Until ThrowAt[4] + 0.35 = 1.11: royalFlush_table at the centre, LookRotation(face) (:23352); card i flips at 1.2 + 0.12 i, 0.18 s (:23371-23394); Until 1.95 (capstone 0x1BC81BF): royalFlush_bang at centre + 2.4 up (:23431), royalFlush_hand at centre + 3.4 up, Show(9) (:23450-23466), Row6Voice(cheer) since hand > 5 (:23468-23469); RoyalFlushBursts@0x1BF3F60 (:25791-26085): 5 bursts 0.16 s apart (Waits.Get(0.16), capstone 0x1BF446E), the last royalFlush_burstBig, every card GlowPulse(1, 0.3) (last 1.6) (:25896-25935); then (hand 9) Row6Voice(finalMove1, finalMove2) (:25950), royalFlush_sword at centre + 5 up (:25981), the cards Gather to centre + 7.5 up in 0.35 s (:26004), RoyalSwordFall@0x1BF4840 (:26104-26412: rise 1.2 m, fall to centre - 1.1 up by 0.8 s, hold 0.6, sink 0.5, Destroy); Waits.Get(0.8) (capstone 0x1BF4794): royalFlush_swordHit at the centre (:26044); the cues after 1.0 s run on in the idle tail; left out: the hits, the clubs' paralysis on the foe (a status look on its body, Sheep decision 4), Row6Shake and the redRamp grade (camera only, :25923, :26046-26069)",
    "cues": [
    [0, "voice", "jokerCard1|jokerCard2"],
    [0, "fx", "tto/royalFlush_shuffle"],
    [0.52, "fx", "tto/royalFlush_card", {"d": 0.45, "y": 1.3, "rot": [0, -15.932, 0], "i": 0, "to": [-3.091, 0, 10.828], "flip": 0.68, "pulse": 1.43, "gather": 2.23, "gatherTo": [0, 7.5, 10]}],
    [0.58, "fx", "tto/royalFlush_card", {"d": 0.45, "y": 1.3, "rot": [0, -8.831, 0], "i": 1, "to": [-1.948, 0, 12.539], "flip": 0.74, "pulse": 1.37, "gather": 2.17, "gatherTo": [0, 7.5, 10]}],
    [0.64, "fx", "tto/royalFlush_card", {"d": 0.45, "y": 1.3, "i": 2, "to": [0, 0, 13.2], "flip": 0.8, "pulse": 1.31, "gather": 2.11, "gatherTo": [0, 7.5, 10]}],
    [0.7, "fx", "tto/royalFlush_card", {"d": 0.45, "y": 1.3, "rot": [0, 8.831, 0], "i": 3, "to": [1.948, 0, 12.539], "flip": 0.86, "pulse": 1.25, "gather": 2.05, "gatherTo": [0, 7.5, 10]}],
    [0.76, "fx", "tto/royalFlush_card", {"d": 0.45, "y": 1.3, "rot": [0, 15.932, 0], "i": 4, "to": [3.091, 0, 10.828], "flip": 0.92, "pulse": 1.19, "gather": 1.99, "gatherTo": [0, 7.5, 10]}],
    [1.11, "fx", "tto/royalFlush_table", {"d": 10}],
    [1.95, "fx", "tto/royalFlush_bang", {"d": 10, "y": 2.4}],
    [1.95, "fx", "tto/royalFlush_hand", {"d": 10, "y": 3.4, "hand": 9}],
    [1.95, "voice", "cheer"],
    [1.95, "fx", "tto/royalFlush_burst", {"d": 10}],
    [2.11, "fx", "tto/royalFlush_burst", {"d": 10}],
    [2.27, "fx", "tto/royalFlush_burst", {"d": 10}],
    [2.43, "fx", "tto/royalFlush_burst", {"d": 10}],
    [2.59, "fx", "tto/royalFlush_burstBig", {"d": 10}],
    [2.75, "voice", "finalMove1|finalMove2"],
    [2.75, "fx", "tto/royalFlush_sword", {"d": 10, "y": 5, "to": [0, 0, 10]}],
    [3.55, "fx", "tto/royalFlush_swordHit", {"d": 10}]
    ]
  },
```

- New cue keys for the card part: `i` (slot, already passed through by cueOf's `...o`), `flip`, `pulse`, `gather`
  (seconds after the card's spawn), `gatherTo` ([x, y, d]); the suit is drawn by the part once per play (one random suit
  for all five, ranks 1-5 shuffled), or a `card` key if question 3 says fixed. `hand` (9) for the banner. `to` on the
  sword = the centre it falls to. Without the parts the cards would sit at their spawn for their 9 s life and the sword
  would hang 5 m up for 4 s: P1-P3 are needed for this tile to read.
- SEQ: nothing needed (a single tile; the game's cut vs the page's 0.2 fade: optional `"Royal Flush: royalFlush1!"`).

### 2.2 Crescent Eclipse (`crescentEclipse1` 1.0 s + `crescentEclipse2` 1.3 s; cell 453) - released

Coroutine `TTO1102:Cat.<RPC_crescentEclipse>d__345::MoveNext@0x1BA3320` (`Cat.c:3404-4266`; floats from
`eclipse_movenext.asm`; `xmm14` = 1.0, loaded at 0x1BA34E4). `centre` = ground(mPos + toCentre), `face`, `faceRot` =
LookRotation(face). No voice anywhere (no Row6Voice in the coroutine).
- **0.00** (state 0): `Row6Begin("crescentEclipse", clip "crescentEclipse1")` cut in (:3560); `addTimeOut(agiAdjust(90))`;
  `crescentEclipse_moon` at centre + 3 face + 8.5 up, identity, not owned (:3571-3595; its `Cat_eclipseFx` mode 0);
  `crescentEclipse_ring` at the centre, faceRot (:3610); `Until(start + 0.22)` (:3619).
- **0.22** (state 1): `crescentEclipse_takeoff` at mPos, faceRot (:3639; own sound backFlip); `crescentEclipse_trail`
  **owned** at the hero, faceRot (:3648; EffectControl 1.35, followPosition); apex = mPos + 0.5 flat(toCentre) + 5.5 up.
- **0.22-1.1** (state 2, every frame until start + 1 + 0.1): the hero rises to the apex (u = (t - 0.22) / 0.28, eased
  1 - (1 - u)^2) until 0.5, then hangs (apex + up 0.12 sin(6 (t - 0.5))) (:3701-3755). **Blade k when t >= EclipseThrowAt[k]
  = 0.52 + 0.04 k** (`Cat::.cctor`, `Cat.c:43034`: 0.52 ... 0.80): `crescentEclipse_blade` at hero + 0.3 face + 1 up,
  faceRot, not owned (:3790-3810; capstone 0x1BA3D88 0.3 / 0.3), `HoldWeapon(mChar.mWep1)` (:3827; the worn main-hand
  weapon) and `Fling(from, EclipseSlot(centre, face, k), centre, 0.22)` (:3835). `EclipseSlot@0x1B83AC0` (:40819) = centre
  + AngleAxis(22.5 + 45 k, up) x face x 5, grounded. **t >= 1.0: `Row6PlayClip("crescentEclipse2")`**, a 0.08 s fade
  (:4255-4259; the `clip2` flag).
- **1.10**: the dive: `crescentEclipse_dive` at the hero (the apex), `LookRotation(centre - from)` (:3906-3918; own sound
  moonStorm); 0.2 s to the centre (f = (t / 0.2)^2, :3923-3990).
- **1.30**: the hero at the centre; `crescentEclipse_land` at the centre, faceRot (:3946; own sound finishingBlow_hit);
  `Row6Shake(0.4)`; `Until(start + 1 + 0.75)` (capstone 0x1BA4627-0x1BA462E) (:3958).
- **1.75** (state 4): `crescentEclipse_click` at hero + 0.3 forward + 0.7 up, hero rotation (:4021-4039; own sound
  cAttack_ring); `moon.Eclipse()` (:4048); `Waits.Get(0.1)` (capstone 0x1BA47C4) (:4053).
- **1.85** (state 5-6): home = hero + 1 up; blade k `Recall(home, 0.14)` when 0.04 k has passed (:4081-4162), arrives
  0.14 s later (1.99 ... 2.27).
- **2.27** (all 8 arrived): `crescentEclipse_burst` at the centre, faceRot (:4096; own sound assassinate);
  `Row6Shake(0.7)`, the redRamp grade (camera, left out); `Until(start + 1 + 1.3)` (capstone 0x1BA4C8A-0x1BA4C91) (:4134).
- **2.30**: `Row6End` (:4210). crescentEclipse2 starts at 1.0 and is 1.3 s long: it ends at 2.3 exactly.
- Sums against the Bible (:1052): blades land 0.74-1.02, landing 1.30, click and moon 1.75, returns 1.99-2.27, burst 2.27,
  end 2.30 OK.

**Cat_eclipseFx** (`Cat.c:43483-46081`; probe: moon mode 0, blade mode 1, `moonSize` 7):
- Moon: `Awake` (:44891) starts `Rise` (:44552): from 2.5 m below its spawn up to it over 0.6 s (smoothstep), scale and
  glow up, then a glow pulse until mBorn + 6 and `Set(0.5)` (fade out, Destroy) if never eclipsed; `LateUpdate` (:45035)
  turns it to face the camera every frame (mode 0 only). `Eclipse()` (:45125): `EclipseRun` (:43483): the shadow disc
  slides from local x -1.2 to 0 over 0.18 s, the corona pulses (scale x (1 + sin) and a 32 deg turn) for 0.9 s, then
  `Set(0.7, red)` fades it out and destroys it: gone about 1.75 + 0.18 + 0.9 + 0.7 = 3.53 s.
- Blade: `HoldWeapon(weapon)` (:45235): when the weapon is active, a copy of it (scripts, joints, colliders, rigidbodies,
  audio, animators stripped) is put under `pivot`, its longest bounds axis turned to point down (`FromToRotation(axis,
  down)`), scaled x 1.5 (`HeldScale`), the default `Model` and `glow` switched off and the tip trail moved to its tip
  (:45620-45846). With no weapon the blade keeps its own model (`Model`, Cel-shaded steel + Unlit/Color edge). `Fling`
  (:45847, `FlingRun` :43698): the 0.22 s throw to the slot with a -1080 deg spin (constants 38 / 30 / 14 / -25 / 0.72 /
  0.65 / 0.28 / 0.2), planted, the `bite` particles and `landSound` (disarm_hit) on landing. `Recall` (:45915,
  `RecallRun` :44267): 0.14 s to `home`, the trail detached (autodestruct), Destroy. `Ignite` / `Dismiss` only on an
  interrupted cast (`EclipseAbort@0x1B81F30`, :40926).

Positions in place (centre = the hero; calc.txt). The dive's direction is the game's (apex 5.447 m up and 5 m short of the
centre: 47.45 deg down).

| blade | slot (x, d) | thrown | lands | recalled (after spawn) | home |
|---|---|---|---|---|---|
| 0 | 1.913, 4.619 | 0.52 | 0.74 | 1.85 (1.33) | 1.99 |
| 1 | 4.619, 1.913 | 0.56 | 0.78 | 1.89 (1.33) | 2.03 |
| 2 | 4.619, -1.913 | 0.60 | 0.82 | 1.93 (1.33) | 2.07 |
| 3 | 1.913, -4.619 | 0.64 | 0.86 | 1.97 (1.33) | 2.11 |
| 4 | -1.913, -4.619 | 0.68 | 0.90 | 2.01 (1.33) | 2.15 |
| 5 | -4.619, -1.913 | 0.72 | 0.94 | 2.05 (1.33) | 2.19 |
| 6 | -4.619, 1.913 | 0.76 | 0.98 | 2.09 (1.33) | 2.23 |
| 7 | -1.913, 4.619 | 0.80 | 1.02 | 2.13 (1.33) | 2.27 |

Cue keys: the two clips of the SEQ, each with times from its own start (crescentEclipse2 starts at 1.0); a step's cues
past its length are dropped at the step change (`seqTick` -> `fxDue(S.dur)`), so the dive, landing, click and burst go
under `crescentEclipse2`. The live moon and blades carry on across the step (no `fxClear` between steps).

```json
  "crescentEclipse1": {
    "why": "TTO1102:Cat.<RPC_crescentEclipse>d__345::MoveNext@0x1BA3320 (Cat.c:3404-4266; plans/fx_cat/tto.md 2.2; in place: the centre at the hero, Penguin decision 8 / Bat decision 10): 0: Row6Begin(crescentEclipse, clip crescentEclipse1) cut in (:3560); crescentEclipse_moon at centre + 3 face + 8.5 up, identity (:3571-3595; Cat_eclipseFx mode 0: Rise 0.6 s from 2.5 m below, faces the camera, Eclipse() at 1.75 :4048, then gone); crescentEclipse_ring at the centre, faceRot (:3610); Until 0.22 (:3619): crescentEclipse_takeoff at mPos, faceRot (:3639; own backFlip), crescentEclipse_trail owned at the hero (:3648; EffectControl 1.35 followPosition); blade k at EclipseThrowAt 0.52 + 0.04 k (Cat::.cctor :43034): crescentEclipse_blade at hero + 0.3 face + 1 up, faceRot (:3790-3810), HoldWeapon(the worn main-hand weapon, :3827), Fling to EclipseSlot@0x1B83AC0 = centre + AngleAxis(22.5 + 45 k) face x 5 in 0.22 s (:3835, :40819), recalled 1.85 + 0.04 k = 1.33 s after its spawn to the hero + 1 up in 0.14 s, then destroyed (:4081-4162); crescentEclipse2 at 1.0 (Row6PlayClip, :4259); no voice; the leap (rise to 5.5 m, dive) is the game's transform, not the clip's: left out (hero in place)",
    "cues": [
    [0, "fx", "tto/crescentEclipse_moon", {"d": 3, "y": 8.5, "eclipse": 1.75}],
    [0, "fx", "tto/crescentEclipse_ring"],
    [0.22, "fx", "tto/crescentEclipse_takeoff"],
    [0.22, "fx", "tto/crescentEclipse_trail"],
    [0.52, "fx", "tto/crescentEclipse_blade", {"d": 0.3, "y": 1, "i": 0, "to": [1.913, 0, 4.619], "recall": 1.33, "home": [0, 1, 0]}],
    [0.56, "fx", "tto/crescentEclipse_blade", {"d": 0.3, "y": 1, "i": 1, "to": [4.619, 0, 1.913], "recall": 1.33, "home": [0, 1, 0]}],
    [0.6, "fx", "tto/crescentEclipse_blade", {"d": 0.3, "y": 1, "i": 2, "to": [4.619, 0, -1.913], "recall": 1.33, "home": [0, 1, 0]}],
    [0.64, "fx", "tto/crescentEclipse_blade", {"d": 0.3, "y": 1, "i": 3, "to": [1.913, 0, -4.619], "recall": 1.33, "home": [0, 1, 0]}],
    [0.68, "fx", "tto/crescentEclipse_blade", {"d": 0.3, "y": 1, "i": 4, "to": [-1.913, 0, -4.619], "recall": 1.33, "home": [0, 1, 0]}],
    [0.72, "fx", "tto/crescentEclipse_blade", {"d": 0.3, "y": 1, "i": 5, "to": [-4.619, 0, -1.913], "recall": 1.33, "home": [0, 1, 0]}],
    [0.76, "fx", "tto/crescentEclipse_blade", {"d": 0.3, "y": 1, "i": 6, "to": [-4.619, 0, 1.913], "recall": 1.33, "home": [0, 1, 0]}],
    [0.8, "fx", "tto/crescentEclipse_blade", {"d": 0.3, "y": 1, "i": 7, "to": [-1.913, 0, 4.619], "recall": 1.33, "home": [0, 1, 0]}]
    ]
  },
  "crescentEclipse2": {
    "why": "TTO1102:Cat.<RPC_crescentEclipse>d__345::MoveNext@0x1BA3320 (Cat.c:3404-4266; plans/fx_cat/tto.md 2.2; this clip starts at 1.0 s, Row6PlayClip(crescentEclipse2) 0.08 s fade :4259; times from its start; in place): 1.1 (0.1): the dive, crescentEclipse_dive at the hero, LookRotation(centre - apex) = 47.45 deg down (:3906-3918; own moonStorm); 1.3 (0.3): crescentEclipse_land at the centre, faceRot (:3946; own finishingBlow_hit); Until 1 + 0.75 (capstone 0x1BA4627): crescentEclipse_click at hero + 0.3 forward + 0.7 up (:4021-4039; own cAttack_ring) and moon.Eclipse() (:4048); Waits.Get(0.1); the blades come back 1.85 + 0.04 k (cued on crescentEclipse1); 2.27 (1.27), the 8th home: crescentEclipse_burst at the centre, faceRot (:4096; own assassinate); Until 1 + 1.3 = 2.3: Row6End (:4134, :4210) = this clip's end; left out: the hits, cut / eclipsed on the foes (eclipsed's look on the body, Sheep decision 4), the death rupture (crescentEclipse_rupture, RPC_eclipseRupture@0x1B87160 :42051: only when an eclipsed foe dies), Row6Shake 0.4 / 0.7 and the redRamp grade (camera)",
    "cues": [
    [0.1, "fx", "tto/crescentEclipse_dive", {"rot": [47.45, 0, 0]}],
    [0.3, "fx", "tto/crescentEclipse_land"],
    [0.75, "fx", "tto/crescentEclipse_click", {"d": 0.3, "y": 0.7}],
    [1.27, "fx", "tto/crescentEclipse_burst"]
    ]
  },
```

- New keys: `eclipse` (the moon: seconds after its spawn when `Eclipse()` runs), `recall` and `home` (the blade). `i`
  and `to` are the existing options.
- SEQ (cat): `"Crescent Eclipse: crescentEclipse1! crescentEclipse2^"` in place of today's `"Crescent Eclipse:
  crescentEclipse1 crescentEclipse2"`: the first clip cut in (Row6Begin), the second at the first's end (1.0 s, the
  `fVar22 <= elapsed` test at :4255) with the game's 0.08 s fade (closest: `^` = 0.1). No `@t` needed.

**Leap variant** (question 4: a page hero mover, as the Penguin's declined P7): the target 10 m ahead, the centre there.
The hero rises from 0.22 to (0, 5.5, 5) by 0.5 (eased), hangs (sway 0.12 m), dives 1.1-1.3 to (0, 0, 10) and stays.
Then: moon `{"d": 13, "y": 8.5}`, ring / land / burst `{"d": 10}`, takeoff at 0, blades from (0, 6.5, 5.3) (`{"d": 5.3,
"y": 6.5}`; the sway adds up to +-0.12) to the slots at d + 10 (calc.txt), home `[0, 1, 10]`, dive at `{"d": 5, "y": 5.447}`
with the same rot, click `{"d": 10.3, "y": 0.7}`.

### 2.3 Drop Anchor (`dropAnchor` 1.1 s, then `anchorYank` 1.0 s; cell 454) - both released

The throw: `TTO1102:Cat.<RPC_dropAnchor>d__388::MoveNext@0x1BAA670` (`Cat.c:7137-7303`). `spot` = mPos + toSpot = the
target spot.
- **0.00**: `Row6Begin("dropAnchor", clip "dropAnchor")` cut in (:7212); a raw 7.75 s lock (:7214); `ClearAnchor` (none
  yet) (:7218); `Row6Voice("battle", "follow")` (:7219); `Waits.Get(0.4)` (:7223).
- **0.40** (still the current throw): `dropAnchor_anchor` at hero + 0.4 face + 1.6 up, `LookRotation(face)`, not owned
  (:7246-7273); `DropAnchorFlightAndLand` (:7281); `Waits.Get(0.7)` (:7288).
- **Flight** (`<DropAnchorFlightAndLand>d__389::MoveNext@0x1B9D6C0`, `Cat.c:138-384`): 0.35 s, lerp(from, spot, u) +
  up x 12 u (1 - u) (a 3 m arc, :336-343), turned upright x AngleAxis(360 u, right) (one forward flip, :354-368).
- **0.75**: the anchor at the spot, upright (:236-247); its inactive `Leash` child (Edge + Pull RingEmitters) switched on
  (:251-260); `mAnchorUntil` = now + 6 (:268); `dropAnchor_slam` at the spot, identity (:281; own sound supportFire_hit);
  the owner's camera shake; the slam; `AnchorHold` (:307).
- **1.10**: `Row6End` (:7299). The clip is 1.1 s.
- **AnchorHold** (`<AnchorHold>d__391::MoveNext@0x1B9D460`, `Cat.c:37-121`): `Waits.Get(0.1)` while the anchor is down
  (:75); when `mAnchorUntil` has passed, `AnchorYank(pose)` with pose = the Cat standing (`standby`) or running (:98-109).
  On the tile she stands: **pose, at 6.75 s** (the first 0.1 s poll at or after landing + 6). Pressing the skill again
  (`Cat::TryRecast@0x1B8E820`, free) yanks earlier (question 6).
- **`AnchorYank(pose)@0x1B7FDA0`** (`Cat.c:38101`): one roll `Random.Range(0, 100) < lckAdjust(25)` = the **chain break**
  (25 / 40 / 50 / 57 / 67 % at LCK 1 / 100 / 200 / 300 / 512, calc.txt) packed into flags; then `RPC_anchorYank`.

The yank: `TTO1102:Cat.<RPC_anchorYank>d__394::MoveNext@0x1B9E500` (`Cat.c:660-866`), times from the yank:
- **0.00**: with pose, `Row6Begin("anchorYank", clip "anchorYank")` cut in (:728) and `Row6Voice("battle")` (:729); the
  cooldown `agiAdjust(100)`; `Waits.Get(0.25)` (:734).
- **0.25**: `dropAnchor_heave` at the anchor spot, identity (:846; own sound throw_hit); the haul; `Waits.Get(0.45)` (:856).
- **0.70**: `dropAnchor_smash` at the spot, identity (:761; own sound supportFire_hit); **on a chain break**
  `dropAnchor_shrapnel` at spot + 1 up, identity (:762-782; own sound throw_hit); the owner's camera shake; the smash;
  `ClearAnchor@0x1B80290` (:808, `Cat.c:42525`): `dropAnchor_sink` at the anchor's position, identity (:42586), Destroy(the
  anchor) (:42591), the foes' `anchored` removed; with pose `Waits.Get(0.3)` (:813).
- **1.00**: `Row6End("anchorYank")` (:824). The clip is 1.0 s.
- Sums against the Bible (:1078-1081): landing 0.75, throw free 1.1, the automatic yank at landing + 6, haul + 0.25,
  smash + 0.45 OK.

One tile, the game's own order when the player does not press again: the throw, the idle stance from 1.1 (Row6End's
standby, the page's 0.2 s fade), the yank at 6.75 s. The anchor is spawned at 0.4 and destroyed at 6.75 + 0.7 = 7.45:
`kill` 7.05 after its spawn (below the 10 s cut).

```json
  "dropAnchor": {
    "why": "TTO1102:Cat.<RPC_dropAnchor>d__388::MoveNext@0x1BAA670 (Cat.c:7137-7303; plans/fx_cat/tto.md 2.3; the target spot 10 m ahead): 0: Row6Begin(dropAnchor) cut in (:7212), Row6Voice(battle, follow) = a 50 % pick (:7219, Row6Voice@0x1B8CB50); Waits.Get(0.4) (:7223): dropAnchor_anchor at hero + 0.4 face + 1.6 up, LookRotation(face) (:7246-7273), DropAnchorFlightAndLand@0x1B9D6C0 (:138-384): 0.35 s to the spot on a 3 m arc (12u(1-u), :336-343) with one 360 deg flip about its right axis (:354-368), then upright at the spot, its Leash rings switched on (:251-260); 0.75: dropAnchor_slam at the spot, identity (:281; own supportFire_hit); Waits.Get(0.7): Row6End at 1.1 (:7299); AnchorHold@0x1B9D460 (:37-121) polls every 0.1 s and yanks at landing + 6 = 6.75 with the pull pose (she stands, :101-103): the anchorYank step; the anchor is destroyed by ClearAnchor at the smash, 6.75 + 0.7 = 7.45 (kill 7.05 after its spawn; RPC_anchorYank :808, ClearAnchor@0x1B80290 :42586-42591); left out: the slam's hits, the anchored chain on the foes (dropAnchor_chain, Cat_anchorChain.Bind from <addStatus>d__481 at 0x24FD823: a status look on the foe, Sheep decision 4), the owner's camera shake (:282-299)",
    "cues": [
    [0, "voice", "battle|follow"],
    [0.4, "fx", "tto/dropAnchor_anchor", {"d": 0.4, "y": 1.6, "to": [0, 0, 10], "kill": 7.05}],
    [0.75, "fx", "tto/dropAnchor_slam", {"d": 10}]
    ]
  },
  "anchorYank": {
    "why": "TTO1102:Cat.<RPC_anchorYank>d__394::MoveNext@0x1B9E500 (Cat.c:660-866; plans/fx_cat/tto.md 2.3; the Drop Anchor tile's last step, 6.75 s after the throw: AnchorHold's yank at landing + 6 with the pose; times from this clip's start; the anchor 10 m ahead): 0: Row6Begin(anchorYank) cut in (:728), Row6Voice(battle) (:729); Waits.Get(0.25) (:734): dropAnchor_heave at the anchor, identity (:846; own throw_hit), the haul; Waits.Get(0.45) (:856): dropAnchor_smash at the anchor, identity (:761; own supportFire_hit), on a chain break (AnchorYank@0x1B7FDA0 :38134-38139: Random.Range(0, 100) < lckAdjust(25) = 25 % at LCK 1) dropAnchor_shrapnel at the anchor + 1 up, identity (:762-782; own throw_hit), ClearAnchor@0x1B80290: dropAnchor_sink at the anchor, identity, Destroy(anchor) (:808, :42586-42591); Waits.Get(0.3): Row6End at 1.0 (:813-824); left out: the smash's hits, the bleed on a chain break (a status look on the foe), the owner's camera shake (:784-801)",
    "cues": [
    [0, "voice", "battle"],
    [0.25, "fx", "tto/dropAnchor_heave", {"d": 10}],
    [0.7, "fx", "tto/dropAnchor_smash", {"d": 10}],
    [0.7, "fx", "tto/dropAnchor_shrapnel", {"d": 10, "y": 1, "p": 0.25}],
    [0.7, "fx", "tto/dropAnchor_sink", {"d": 10}]
    ]
  },
```

- SEQ (cat), new: `"Drop Anchor: dropAnchor! root*~@5.65 anchorYank"` = the throw (1.1 s), the idle stance held 5.65 s
  (to 6.75), the yank cut in (a later step with no mark is a cut). Both clips then leave the single tiles (`used`), and
  the tile's icon is the Bible's dropAnchor one (`icons/hd/index.json`: dropAnchor's clips `["dropAnchor"]`; no skill
  lists `root`). The `root` step looks up `@DropAnchor:root` / `root` cues: the Cat's cue file must not get a plain
  `root` key (effect-only tiles use `@<Name>:root`).
- `p` with no `roll` = its own roll each play (index.html `rolled`).
- The `anchor` cue's `to` is the landing spot for its mover (P5).

**TTO1109 variant** (question 1): no recast, `AnchorHold` every frame, `mAnchorUntil` = landing + 5, `AnchorYank(pose =
false)`: no `anchorYank` clip at all; heave 6.0, smash 6.45 (Bible :1073), plus the `Cat_anchorChain`-free countdown
TextMesh over the anchor (`Cat_anchorCountdown`). The SEQ would be `"Drop Anchor: dropAnchor! root*~@5.35"` with the yank's
cues on the root step and the `anchorYank` clip unused.

### 2.4 shikifujin (4.8 s) - not released, no cues

- No TTO code plays it: the string `shikifujin` is in neither TTO1102's `GameAssembly.dll` nor its decrypted
  `global-metadata` (byte search, ASCII and UTF-16), nor the installed 2026-11-07 client's `GameAssembly.dll`, nor any
  `pseudo/`, `pseudo_c6_extra/`, `tooltips/`, `locale/` file; no method or field in `methods.tsv` / `dump.cs`. BB's
  `DecompiledSource/*.cs` has no Cat use either (only the Panda's `fujinKen1-3`, a different name).
- No effect prefab, sound or voice of that name in TTO's catalog (`catalog.txt`), and the AnimationClip has no events
  (`clipevents.py`). NOTES.md already says so ("Cat shikifujin, which TTO never plays", the TTO release list).
- So: nothing to cue. Its tile stays as today's (a local-only TTO motion) unless the user wants it hidden like the Wolf's
  never-played cast clips (`NEVER_PLAYED`). Question 9.

## 3. What is left out (only "on an enemy" / "needs a foe" / camera)

- Status looks on the foe's body (Sheep decision 4; Bat decision 44): `eclipsed` (Crescent Eclipse's burst, 6 s,
  `Cat_row6StatusFx`, faces the camera), `dropAnchor_chain` (the anchored foe's `Cat_anchorChain` LineRenderer to the
  anchor, 10 links of 0.42 m, sag 0.9), BB's `cut` (blades), `bleed` (a chain break), `paralysis` (Royal Flush's clubs).
- `crescentEclipse_rupture` (`RPC_eclipseRupture@0x1B87160`, `Cat.c:42051-42080`): only when an eclipsed foe dies.
- `dealersMark` (a status look, `CharacterControl::AddCatRow6Status@0x24ABF90` with hitMod + 0.08 x lv): none of these six
  skills applies it (no `dealersMark` string in `Cat.c`); no tile.
- The hits themselves draw nothing (`CharacterControl::hit@0x24D57E0`: no effect load, as the Penguin's verification).
- Camera: `Row6Shake@0x1B8BF20`, `AddCamereShake`, `CameraEffect.AddColorRamp("redRamp", 0.6 / 0.8 s)`.
- Nothing is left out for a missing part: every effect is cued, and the parts are listed in section 6.

## 4. Sounds and voices

- Voices (`voice` cues; BB's rip `...\heroes\cat\voices\<name>.wav`, all present): jokerCard1 / jokerCard2, cheer,
  finalMove1 / finalMove2 (Royal Flush); battle / follow (the throw), battle (the yank). Crescent Eclipse has none.
- The prefabs' own AudioSources (play on awake; BB's `sounds/`): powerShuffle (shuffle), gamble_ring 0.8 (table),
  gamble_hit (bang), grandCasino_hit1 (burst), grandCasino_hit7 (burstBig, swordHit), supportFire_hit (swordHit's Boom,
  slam, smash), throw 0.6 (blade), backFlip (takeoff), moonStorm (dive), finishingBlow_hit (land), cAttack_ring (click),
  assassinate (burst), moonBlade 0.7 (moon), throw_hit (heave, shrapnel), bleed_hit (rupture, left out).
- Clips the scripts play (P1, P4): `Cat_royalCard` dealSound throw1 (0.7 at the throw, 1 on landing), flipSound twoPair
  (0.8), shatterSound throw_hit (Shatter, not on hand 9); `Cat_eclipseFx` landSound disarm_hit (blade landing),
  igniteSound none (the moon's Eclipse plays nothing).
- No `sounds/` cue and no TTO-only clip (Read this first 2).

## 5. Probed 2026-11-13 (home PC, TTO's 2026-11-04 bundles)

`uv run --no-project --with UnityPy --with pillow --with imageio-ffmpeg python -I pipeline/wardrobe_fx_tto.py cat --probe
crescentEclipse_blade,...,royalFlush_table` (28 names) -> `checks/fx_cat_research/tto/probe.json` (no errors; summaries
`compact.txt`, `scripts.txt`).

| Prefab | EffectControl (life + after) | Parts | AudioSource |
|---|---|---|---|
| royalFlush_shuffle | 0.6, followPosition | 2 PS (card sprites, glints) | powerShuffle |
| royalFlush_card | 9.0 | **Cat_royalCard**; Pivot > Halo (StaticMesh, add), Card (StaticMesh: Unlit/Texture face atlas 6 x 4, back, Unlit/Color rim), GoldRibbon (TrailRendererModern); Plant, Shards PS | none on awake (the script's) |
| royalFlush_table | 3.6 | 2 GroundHugs (Felt band r 4.4, Inner disc 4.6), RingEmitter | gamble_ring 0.8 |
| royalFlush_bang | 0.8 | 2 ImageEmitters, PS | gamble_hit |
| royalFlush_hand | 1.9 | **Cat_royalHandBanner** (hands = tto_royalFlush_hand0-9, life 1.7, fade 0.45); plate > rays, glow, banner (StaticMesh quads); PS Glints | - |
| royalFlush_burst | 2.0 | 3 PS, 3 RingEmitters, EmblemEmitter | grandCasino_hit1 |
| royalFlush_burstBig | 2.0 | 3 PS, 5 RingEmitters, EmblemEmitter | grandCasino_hit7 |
| royalFlush_sword | 4.0 | Model (StaticMesh: Cel card / gold / chip / grip + Unlit/Color edge), Aura (add), PS Sparkle | - |
| royalFlush_swordHit | 2.2 | 3 PS (one Bomb2 = Multiply (Double)), 3 RingEmitters, GroundHug Crater | grandCasino_hit7 + Boom supportFire_hit |
| crescentEclipse_moon | 7.0 | **Cat_eclipseFx** mode 0; halo, disc, shadow (local x -1.2), corona (StaticMesh quads) | moonBlade 0.7 |
| crescentEclipse_ring | 2.5 | 2 GroundHugs (Sigil r 6.2-6.6, Dark 6.9), 2 RingEmitters | - |
| crescentEclipse_takeoff | 1.0 + 1.0 | 2 ImageEmitters, 2 RingEmitters, PS | backFlip |
| crescentEclipse_trail | 1.35, followPosition | 2 PS | - |
| crescentEclipse_blade | 4.0 | **Cat_eclipseFx** mode 1; pivot > Model (StaticMesh: Cel steel / grip, Unlit/Color edge), glow, BladeTipTrail (TrailRendererModern); PS bite | throw 0.6 |
| crescentEclipse_dive | 0.7 | PS | moonStorm |
| crescentEclipse_land | 2.0 + 1.0 | LineEmitter, 2 RingEmitters, 2 GroundHugs (Cut r 3.4-3.8), PS | finishingBlow_hit |
| crescentEclipse_click | 0.6 | 2 ImageEmitters | cAttack_ring |
| crescentEclipse_burst | 2.2 | 11 PS, LineEmitter, 3 RingEmitters, GroundHug (r 6.4-7.2) | assassinate |
| crescentEclipse_rupture | 1.4 | 2 PS, LineEmitter, RingEmitter, ImageEmitter | bleed_hit (left out) |
| dropAnchor_anchor | 15.0 | Model (StaticMesh, Cel iron), **Leash (inactive)** > Edge, Pull RingEmitters | - |
| dropAnchor_slam | 1.4 | 3 RingEmitters | supportFire_hit |
| dropAnchor_heave | 0.6 | RingEmitter | throw_hit |
| dropAnchor_smash | 2.0 | PS (Bomb2, Multiply (Double)), 2 RingEmitters | supportFire_hit |
| dropAnchor_shrapnel | 1.2 | PS (Default-Particle, Alpha Blended Premultiply) | throw_hit |
| dropAnchor_sink | 0.9 | RingEmitter | - |
| dropAnchor_chain | - | LineRenderer + **Cat_anchorChain** (left out) | - |
| eclipsed, dealersMark | - | **Cat_row6StatusFx** (left out) | - |

- No `followState`; Shuriken modules used: Initial, Emission, Shape (0, 2, 4, 5, 10), Color, Size, Rotation, Velocity,
  Force, InheritVelocity (all in shuriken.js); render modes 0 (billboard) and 1 (stretched). GroundHugs: shapes 0 and 1, no
  motes. 41 textures (tto_*), all exported.
- Shaders: addsoft / add / alpha (legacy), `FlexibleCelShader/Cel No Outline` (8 materials; 5 with `_FresnelBrightness`
  0.1-0.4), `Unlit/Color` (3), `Unlit/Texture` (2), `Legacy Shaders/Particles/Alpha Blended Premultiply` (1),
  `Legacy Shaders/Particles/Multiply (Double)` (1).

## 6. Parts the page lacks (effect: part)

| # | Part | Effects | What it does (source) |
|---|---|---|---|
| P1 | `Cat_royalCard` (class script, in the prefab) | royalFlush_card | `SetCard` (:47512: `_MainTex_ST` = (1/6, 1/4, (card % 6) / 6, (3 - card / 6) x 0.25) on material `faceIndex`); `Deal` (`DealRun` :46565: 0.35 s, lerp with 1 - (1 - u)^1.35, + up x arc 4u(1-u), + planted-right x 0.45 sin(pi u), rotation slerp(planted x Euler(90, 0, 0) x AngleAxis(720 u, fwd) -> lean = planted x Euler(-tiltIn 8, 0, 0)), scale 0.35 + 0.65 sqrt(u); landing: Plant PS, dealSound, GlowPulse(0.6, 0.25), a 0.16 s settle wobble 12 sin(2 pi s)(1 - s) deg); `Flip(0.18)` at `flip` (`FlipRun` :46892: pivot local yaw 0 -> 180 with a 0.12 sin overshoot, lift 0.42 sin(pi s), flipSound 0.8, then GlowPulse(1, 0.4) in the suit colour); `GlowPulse(peak, time)` (`Pulse` :47359, `SetGlow` :47604: glow renderer `_TintColor` = SuitColors x 0.5, alpha k x 0.5, off below 0.01) at `pulse` + 0.16 k (k < 5, last peak 1.6); `Gather(to, 0.35)` at `gather` (`GatherRun` :47135: u^2 lerp with a sideways 1.2 / up 1.5 sin(pi u) arc, AngleAxis(540 u^2, up), scale 1 - 0.8 u^2, glow 1, Destroy); the suit drawn once per play (or `card`). `Shatter` (:47809) only for other hands. |
| P2 | `Cat_royalHandBanner` | royalFlush_hand | `Show(hand)` (:48122): banner `_MainTex` = hands[hand], mScale 0.8 + 0.5 min(hand / 9, 1), mRays 0.25 + 0.75 x; `LateUpdate` (:48349): faces the camera, pop-in (0.12 / 0.24 s, 1.18 overshoot, then + 0.03 / s), alpha in over 0.08 s and out over `fadeTime` 0.45 before `life` 1.7, Destroy; `Apply` (:48299) / `Tint` (:48222): plate scale, banner / glow (x 0.8) / rays (x mRays) `_TintColor` alpha. The exporter must carry `hands` (it does: probe). |
| P3 | `Cat.RoyalSwordFall` (CODE_MOVERS) | royalFlush_sword | Section 2.1 (`Cat.c:26104-26412`): spin-in and grow 0.35 s, rise 1.2 m, fall to `to` - 1.1 up by 0.8 s, hold 0.6, sink and shrink 0.5, Destroy. |
| P4 | `Cat_eclipseFx` (class script; modes Moon / Blade) | crescentEclipse_moon, crescentEclipse_blade | Section 2.2. Moon: Rise, camera-facing LateUpdate, the glow pulse, `Eclipse()` at `eclipse` (EclipseRun shadow slide 0.18 s, corona 0.9 s, Set(0.7) fade + Destroy), else Set(0.5) at 6 s. Blade: `HoldWeapon` = a copy of the hero's worn main-hand weapon (`C.state.R`'s built prop) under `pivot`, longest axis down, x 1.5, Model + glow off, trail to the tip (none worn: its own blade); `Fling` to `to` in 0.22 s with the -1080 deg spin and the landing bite + disarm_hit; `Recall` to `home` at `recall` in 0.14 s, Destroy. |
| P5 | `Cat.DropAnchorFlight` (CODE_MOVERS) | dropAnchor_anchor | 0.35 s to `to` on a 12u(1-u) arc with one 360 deg flip about its right axis, then upright at `to`, and switches the inactive `Leash` node on (its Edge / Pull RingEmitters built then: the page skips `active: false` nodes today, groundhug.js:66 etc.). Destroyed by the cue's `kill`. |
| P6 | Shaders `Unlit/Color`, `Unlit/Texture` (api.shader, e.g. in a new fxparts/tto_cat.js) | royalFlush_card, royalFlush_sword, crescentEclipse_blade | Unity's built-ins: one opaque unlit pass, `_Color` / `_MainTex` x `_MainTex_ST` (no props for Unlit/Texture: the material's scale / offset). Today they fall to the particle material with a warning (mesh.js:195). |
| P7 | The cel shader's fresnel term (tto_penguin.js:111) | royalFlush_card / sword (m_card 0.15, m_gold 0.2, m_chip 0.1), crescentEclipse_blade (m_steel 0.4) | `_FresnelBrightness` > 0 is not drawn today (a console warning); its formula is in the Penguin's `dxbc_cel.txt` (checks/fx_penguin_build/tto/). |
| P8 | `wardrobe_fx_tto.py` SHADER_BLEND: `Legacy Shaders/Particles/Alpha Blended Premultiply` -> `premul`, `Legacy Shaders/Particles/Multiply (Double)` -> `multiply2` | dropAnchor_shrapnel, dropAnchor_smash, royalFlush_swordHit | The page already draws `premul` / `multiply2` (index.html:3847, :3870); the TTO exporter maps only four legacy names (wardrobe_fx_tto.py:141), so these two come out as `shader:...` and fall to the particle default. |

Parts already built and used here: EffectControl, ImageEmitter, RingEmitter, LineEmitter, EmblemEmitter, GroundHug
(groundhug.js), Shuriken (shuriken.js), TrailRendererModern (tto_sheep.js), StaticMesh (mesh.js), the cel shader
(tto_penguin.js), AudioSource.

Build notes for the parts stage (this PC has the bundles):
- add `SKILL_FX["cat"]` (the 26 cued names; eclipsed / dealersMark / dropAnchor_chain / crescentEclipse_rupture too, so
  the left-out ones are built, as the Wolf's) and `CODE_MOVERS` for `royalFlush_sword` and `dropAnchor_anchor`;
- the Cat_* scripts come out as `{"type": "Cat_royalCard", ...}` already (probe: their fields resolved, node refs
  `{"node": i}`, AudioClips by name);
- then `wardrobe_fx_tto.py cat` (after `wardrobe_fx.py cat`, whose voices these cues name).

## 7. Open questions (only what the Wolf / Sheep / Penguin / Bat decisions don't answer)

1. **Which TTO build?** TTO1102 with the 2026-11-04 bundles (recommended: code and prefabs match, clips at speed 1; Bat
   decision 44) or TTO1109's patch 1.6.2.4 (Royal Flush x 1.35 and its shorter waits, Crescent Eclipse x 1.18, Drop
   Anchor's 5 s auto yank with no pull pose, rescaled VFX, the camera-placed moon): needs the office's newer decrypted
   bundles, a page clip-speed option and a re-trace on `DecompiledSource_TTO_2026-11-09`.
2. **Royal Flush's hand**: recommended always Royal Flush (sword, all five bursts, cheer + finalMove; the "top rank" of a
   roll). Alternative: the game's weighted odds (a weighted pool the page doesn't have; the sword 1 play in 50-60).
3. **Royal Flush's suit**: recommended random per play, one suit for all five cards (as `DealHand`'s System.Random), ranks
   1-5 shuffled. Alternative: always spades (suit 0).
4. **Crescent Eclipse's leap**: recommended in place (Penguin decision 8, Bat decision 10). Alternative: a page hero
   mover (rise to 5.5 m, hang, dive onto the 10 m target; 2.2's leap variant), which would serve Frost Field too.
5. **The eclipse blades as the worn weapon**: recommended yes (HoldWeapon, the game's look: eight copies of the Cat's own
   dagger, x 1.5). Alternative: always the prefab's own blade.
6. **Drop Anchor's yank**: recommended the automatic one at 6.75 s (the game with no second press; TTO1109 has no recast
   at all), the tile 7.75 s long. Alternative: a recast right after the throw, `"dropAnchor! anchorYank"` (2.1 s; the
   anchor's kill 1.4).
7. **The chain break's shrapnel**: recommended `p` 0.25 (lckAdjust(25) at LCK 1, the stat-free wardrobe).
   Alternative: 0.40 (LCK 100) or always.
8. **Camera effects** (Row6Shake, redRamp): recommended left out (the page has none; Wolf tto Q7).
9. **shikifujin**: recommended no cues and the tile kept as today (local only, a TTO motion). Alternative: hide it as a
   never-played clip (`NEVER_PLAYED.cat`, as the Wolf's cast clips).

## 8. For the Bible (offer to the user; that repo's own rules)

- Royal Flush (TTO1102): the voice jokerCard1 / 2 at the cast, cheer for Full House and better, finalMove1 / 2 with the
  sword; the cards fly 0.35 s on a 1.6 m arc with a 720 deg spin, land 3.2 m beyond the target on a 150 deg fan, flip
  0.18 s, glow with each blast, then on Royal Flush fly up into the sword (a fold shatters them otherwise); the sword
  rises 1.2 m, drops, stays 0.6 s and sinks; the Royal Flush hand is always ranks 1-5 of one random suit.
- Crescent Eclipse (TTO1102): the second clip starts at 1.0 s; the eight blades are copies of the Cat's own main-hand
  weapon at 1.5 x (`HoldWeapon`); the moon sits 3 m past the target, 8.5 m up, rises 0.6 s and is gone about 1.8 s after
  the eclipse; no voice.
- Drop Anchor (TTO1102): voice battle / follow, battle at the yank; the anchor flips once in flight; a chain break throws
  shrapnel; the pull pose only when the Cat is standing or running at the yank.
- shikifujin: an animation in TTO's bundles that no client code plays (TTO1102, the 2026-11-07 client).

## Verification

Checked 2026-11-13 (home PC, read only) against `D:\12tails\DecompiledSource_TTO_2026-11-02\pseudo\Cat.c`, `dump.cs`,
`methods.tsv`, the capstone dumps in `checks/fx_cat_research/tto/` (`royalFlush_movenext.asm`, `royalSwordFall.asm`),
the probe summary `compact.txt`, BB's rip (`...\heroes\cat\voices\`, `...\sounds\`), the Bible's
`12t_reference/cat-skill-reference.md` 1005-1090 and the page (`wardrobe/index.html`). My own scripts:
`checks/fx_cat_research/verify_tto_parts/` (`blocks.py`: every json block below parses, cue kinds fx / voice only).

Confirmed as written: every string a coroutine spawns or plays (royalFlush / royalFlush1, jokerCard1|2, cheer,
finalMove1|2, the 11 royalFlush_* names; crescentEclipse / crescentEclipse1 / crescentEclipse2 and the 8 effect names;
dropAnchor, anchorYank, battle / follow, Leash, the 7 dropAnchor_* names); every constant (dump.cs 102685-102779:
RoyalFlushThrowAt 0.52 + 0.06 i, flight 0.35, reveal 1.2 + 0.12 i, flip 0.18, bang 1.95, burst gap 0.16, banner 3.4,
sword 5 m and 0.8 s; EclipseTakeoffAt 0.22, ApexAt 0.5, ApexHeight 5.5, EclipseThrowAt 0.52 + 0.04 k, flight 0.22, dive at
1.0 + hang 0.1, dive 0.2, click 0.75, clip 2 1.3, recall step 0.04 / flight 0.14; DropAnchor release 0.4, flight 0.35,
arc 3, life 6, yank pull 0.25, reel 0.45, shatter 25); the waits (`Until` absolute from `start`; capstone 0x1BC7E72,
0x1BC7EB2, 0x1BC7FC9-0x1BC7FD0, 0x1BC8171-0x1BC818E, 0x1BC81BF); `RoyalFlushSlot` (:40013 `(i - 2) x 150 x 0.25`, x 3.2,
grounded) and `EclipseSlot` (:40854 `45 k + 22.5`, x 5, grounded) and every slot / yaw / time in both tables
(calc.txt re-derived: Unity's AngleAxis(+a, up) turns forward to the right, so card 0 at -75 deg is x -3.091); the card
spawn hero + 0.45 face + 1.3 up and its LookRotation(FlatFace(mPos, slot)) (:23190-23236); Gather to the sword's spawn +
2.5 up = centre + 7.5 up (:26001-26004); the hand banner at centre + 3.4 up with identity, cheer only for hand > 5
(:23446-23469); the bursts and sword order in RoyalFlushBursts (:25864-26044); the moon at centre + 3 face + 8.5 up,
identity, not owned (:3571-3595); takeoff at mPos, trail owned at the hero (:3639-3648); the blade at the hero's current
position + 0.3 face + 1 up, HoldWeapon(mChar + 0x128), Fling(.., 0.22) (:3772-3836); clip 2 at t >= 1.0 (:4255-4259, the
`clip2` flag); the dive LookRotation(centre - from) (:3906-3918), land at d0 + 0.2 (:3926-3946), click at hero + 0.3
forward + 0.7 up with the hero's rotation (:4021-4039), home = hero + 1 up (:4069-4074), burst when all eight arrived
(:4087-4098), Row6End (:4210); the anchor at hero + 0.4 face + 1.6 up, LookRotation(face) (:7246-7273), the 12 u (1 - u)
arc and the 360 deg flip about right (DropAnchorFlightAndLand), mAnchorUntil = landing + 6, Leash switched on, slam with
identity; AnchorHold's 0.1 s poll and its pose test (standby -> true, else run); the yank's heave / smash / shrapnel
(spot + 1 up) / ClearAnchor's sink, all identity (:728-856, :42564-42594); `Random.Range(0, 100) < lckAdjust(25)`
(:38134-38136). The SEQ tokens parse with the page's regex (index.html:1259 `^(\w+)(\*)?([~^!])?(?:@([\d.]+))?$`); a
step's cues at or past its length are dropped at the step change (seqTick -> fxDue(S.dur, false), index.html:1384; fxStart
resets FX.cues), the last step's run on in the idle tail (index.html:1382), so the five blocks' keying is right. All seven
voices and every AudioSource / script clip named in section 4 are in BB's rip. The Bible's timeline (1.95 + 0.16 k, sword
3.55; blades 0.74-1.02, landing 1.30; landing 0.75, auto yank at + 6) agrees.

Corrections:
1. **Crescent Eclipse's dive is drawn under the floor** (2.2, crescentEclipse2 cue `[0.1, "fx", "tto/crescentEclipse_dive",
   {"rot": [47.45, 0, 0]}]`). The prefab's only drawing node is `Streak`, 3 m along the root's forward
   (`compact.txt:93`: pos (0, 0, 3), a world-space box burst of 40). Spawned at the hero's feet and pitched 47.45 deg
   down, the streak sits at (0, -2.21, 2.03): 2.2 m below the floor. In the game the root is at the apex, 5.447 m up and
   5 m short of the centre (calc.txt), so the streak lies on the dive path. In place (centre = the hero, as the rest of
   the tile) the apex is `{"d": -5, "y": 5.447}`; with the same rot the streak is at (0, 3.24, -2.97) and the path meets
   the floor exactly at the hero, where `crescentEclipse_land` follows 0.2 s later. Corrected block below.
2. Line references (no change to any cue): Row6Voice's 50 % pick is `Cat.c:38669` (`(param_3 == 0) || Random.Range(0, 2)
   == 0`), not :38662; the cel shader's fresnel / rim warning is `tto_penguin.js:124-125`, not :111 (P7).
3. **P5: the page does not skip the inactive `Leash` today.** Only `Leash` (node 2) carries `active: false`; its children
   `Edge` and `Pull` (nodes 3, 4, the two RingEmitters) carry no flag (`compact.txt:250-258`; `wardrobe_fx_tto.py:473-474`
   flags a node by its own m_IsActive only), and `ringEmitter` (index.html:3965, :4086) never reads `active` (only
   groundhug.js:66, alphatimer.js:44, arcribbon.js, groundfollower.js, tto_sheep.js check a node's own flag). So today the
   leash rings draw from the anchor's spawn at 0.4 s, through the flight. P5 must hold them back: at build take the
   ringEmitters of nodes 3 and 4 out of `fx.emitters` (and hide `fx.nodes[2]`), and at the landing (`to` reached) put
   them back with a fresh clock and show node 2 (Unity: SetActive(true) starts their emitters then). Exporter
   alternative: propagate `active: false` to a disabled node's descendants and let P5 clear it; the part still has to
   start their clocks at the landing.

No other change: royalFlush1, crescentEclipse1, dropAnchor, anchorYank and the SEQ lines stand as written.

### Corrected paste-ready block (crescentEclipse2 only)

```json
  "crescentEclipse2": {
    "why": "TTO1102:Cat.<RPC_crescentEclipse>d__345::MoveNext@0x1BA3320 (Cat.c:3404-4266; plans/fx_cat/tto.md 2.2 and Verification 1; this clip starts at 1.0 s, Row6PlayClip(crescentEclipse2) 0.08 s fade :4259; times from its start; in place, the centre at the hero): 1.1 (0.1): the dive, crescentEclipse_dive at the hero's transform = the apex (5.447 m up: 5.5 + 0.12 sin(6 x 0.6), 5 m short of the centre = d -5 in place), LookRotation(centre - apex) = 47.45 deg down (:3906-3918; own moonStorm; its Streak node 3 m along that, so it lies on the path and the path meets the floor at the hero); 1.3 (0.3): crescentEclipse_land at the centre, faceRot (:3946; own finishingBlow_hit); Until 1 + 0.75 (capstone 0x1BA4627): crescentEclipse_click at hero + 0.3 forward + 0.7 up (:4021-4039; own cAttack_ring) and moon.Eclipse() (:4048); Waits.Get(0.1); the blades come back 1.85 + 0.04 k (cued on crescentEclipse1); 2.27 (1.27), the 8th home: crescentEclipse_burst at the centre, faceRot (:4096; own assassinate); Until 1 + 1.3 = 2.3: Row6End (:4134, :4210) = this clip's end; left out: the hits, cut / eclipsed on the foes (eclipsed's look on the body, Sheep decision 4), the death rupture (crescentEclipse_rupture, RPC_eclipseRupture@0x1B87160 :42051: only when an eclipsed foe dies), Row6Shake 0.4 / 0.7 and the redRamp grade (camera)",
    "cues": [
    [0.1, "fx", "tto/crescentEclipse_dive", {"d": -5, "y": 5.447, "rot": [47.45, 0, 0]}],
    [0.3, "fx", "tto/crescentEclipse_land"],
    [0.75, "fx", "tto/crescentEclipse_click", {"d": 0.3, "y": 0.7}],
    [1.27, "fx", "tto/crescentEclipse_burst"]
    ]
  },
```
