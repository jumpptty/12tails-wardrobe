# Penguin: the skills with no body animation (effect-only tiles)

Research only (2026-11-13, home PC). Read-only researcher: nothing else in the repo was changed; the probe ran with
`--probe` only (`uv run --no-project --with UnityPy python -I pipeline/wardrobe_fx.py penguin --probe
manaArc,penguinOfArc,dispell,frostSpike_ring,manaPool_hit`, exit 0). Sources: `D:\12tails\DecompiledSource\Penguin.cs`
(cited `:line`), `CharacterControl.cs`, the Bible's `12t_reference/penguin-skill-reference.md` and skill cards
(`12t_projects/bible/index.html`), `plans/fx_inventory.md`, `wardrobe/fx_cues/penguin.json`, `wardrobe/data/penguin/fx.json`.
Worked example followed: the Sheep's Quick Heal (SEQ `"Quick Heal: root@1"`, SEQ_SKILL `"@QuickHeal": "quickHeal"`, cue
key `"@QuickHeal:root"`, `wardrobe_skill_icons.py` EFFECT_ONLY).

## Result

Five Penguin skills play no clip. Each one's RPC is called straight from the key dispatcher, with no `PlayAnimation`
before or inside it, so the Penguin carries on with whatever she was doing:

| Tile (Bible name) | Bible icon | RPC | Effects | Voices | Buildable |
|---|---|---|---|---|---|
| **Mana Arc** | `penguin_manaArc4` | `RPC_manaArc` :10291, coroutine `$RPC_manaArc$26093` :21578 | `penguinOfArc` (max rank: Penguin Of Arc #412 on), hero + 0.5 m up, **Random.rotation** | manaArc1 / manaArc2 | yes. The random rotation needs a one-line page option (below); without it there is a fixed fallback |
| **Dispell** | `penguin_dispell2` | `RPC_dispell` :10298, `$RPC_dispell$26104` :22009 | `dispell`, at the hero with her rotation | dispell1 / dispell2 | yes (the screen warp is left out) |
| **Double Cast** | `penguin_doubleCast1` | `RPC_multiCast(sLv 1)` :9819 (a plain method) | `multiCast`, at the hero with her rotation | multiCast1 / multiCast3 | yes (`multiCast` is already built) |
| **Triple Cast** | `penguin_tripleCast2` | `RPC_multiCast(sLv 2)` :9819 | `multiCast`, at the hero with her rotation | multiCast2 / multiCast3 | yes (already built) |
| **Frost Spike** | `penguin_frostSpike5` | `RPC_frostSpike_fire` :11625, `$RPC_frostSpike_fire$26537` :37695 | `frostSpike_ring`, at the hero, Quaternion.identity | frostSpike1 / frostSpike2 | yes |

Every effect is **ready** in `plans/fx_inventory.md` (penguin): `penguinOfArc` :585, `manaArc` :572, `dispell` :561,
`multiCast` :582, `frostSpike_ring` :566. The probe confirms they are built only from parts the page already has:
RingEmitter, VortexEmitter, EllipsoidParticleEmitter + ParticleAnimator + ParticleRenderer, StaticMesh, AlphaTimer,
EffectControl and AudioSource. **No effect uses followState**, so no cue has a cut time. Every voice and every sound an
effect plays exists in the rip (`RippedAssets/.../characters/heroes/penguin/voices|sounds/*.wav`). Voice lengths:
manaArc1 0.84 s, manaArc2 1.05, dispell1 0.83, dispell2 0.82, multiCast1 0.81, multiCast2 0.84, multiCast3 1.45,
frostSpike1 0.56, frostSpike2 0.73. Sounds the effects play themselves: manaArc 0.93 s, dispell 1.49, trippleCast 0.92,
frostSpike 0.50.

**Double Cast / Triple Cast are two actives of their own,** not rolls. They are `pgn_doubleCast1` (#131) and
`pgn_tripleCast2` (#132), both cType-dispatched (:7372 tripleCast2, :7384 doubleCast1). They share one method,
`RPC_multiCast(sLv)`: sLv 1 = Double Cast, 2 = Triple Cast. The remote copies arrive as `RPC_multiCast1` / `RPC_multiCast2`
(:1663, :1675, :4038, :4056). The method gives the `multiCast` status for chaAdjust(12) s. The repeats that status causes
are the `RPC_<skill>_multiCast` phases, already cued as the pool members' Double Spell repeats (roll `doubleSpell`). Double
Spell (#431) is the passive 12 % roll inside `RPC_cast1` (:20100-20144), which is already cued.

**Frost Spike** is a passive (`pgn_frostSpike5` #423, the Bible card `penguin_frostSpike`, `passive:true`). It procs
when a hit lands on an Ice Shield that the hit does not break: `CharacterControl.cs:31236` checks hasSkill(423), then
`Random.Range(0, 100) < lckAdjust(12)` (:31242, 12 %), then calls `RPC_frostSpike_fire(holder position)` (:31259, ActionEvent
:31270). It has its own RPC and coroutine and no clip, so it gets its own tile (HANDOFF lists it). The tile plays the
proc itself, every time, so the cue has no `p`.

## Accounting: every RPC_* in Penguin.cs (92 definitions)

**Cued already** (the key in `wardrobe/fx_cues/penguin.json`):
- RPC_nAttack1 :9644, RPC_nAttack2 :9651, RPC_nAttack3 :9658: `nAttack1-3`
- RPC_cAttack1 :9769: `cAttack1`, `cAttack2`
- RPC_cast1 :9783: `cast1`
- RPC_manaMissile_cast :10011, RPC_manaBurn_cast :10326, RPC_fallingComets_cast :10368, RPC_manaVortex_cast :10389,
  RPC_meteora_cast :10592, RPC_frozenBlast_cast :10606, RPC_arcticWind_cast :10627, RPC_iceShield_cast :10689,
  RPC_iceBlock_cast :10696, RPC_snowMan_cast :10775, RPC_tornado_cast :10782, RPC_typhoon_cast :11130,
  RPC_absoluteZero_cast :11444, RPC_blizzard_cast :11451, RPC_snowBall_cast :11632, RPC_cosmicRift_cast :11639: the
  `cast3` pool's 16 members
- RPC_blink :10305, RPC_parallelShift :11597: the `blink` pool
- RPC_fallingStars :10347, RPC_novaFlare :10542: the `cast4` pool
- RPC_mpTransfer :10319: `@MPTransfer:nAttack1`
- RPC_cosmicFriday_cast :11646: `@CosmicFriday:cast3`, `cosmicFriday`
- RPC_arcticEmperor :11458: `arcticEmperor`
- RPC_focusIntellect :11590: `focusIntellect`
- RPC_emotion :13327: the emote keys
- RPC_ko :16218, RPC_dead :16225: `ko` (one of the two, decision 11)

**Phases of cued skills** (cued inside those skills' entries, or deliberately left out there):
- RPC_nAttack_fire :9665, RPC_nAttack_hit :9709, RPC_spreadShot_fire :11472 (Spread Shot #401's pellets, in nAttack1-3)
- RPC_cAttack0 :9776 (Charge Attack's release: the cAttack2 cut)
- RPC_cast0 :9790, RPC_cosmicFriday_cancel :11653, RPC_emotion0 :13334, RPC_activateIcon2 :16120 (cancels: standby, no
  effect)
- RPC_manaMissile_multiCast :10018, RPC_blink_multiCast :10312, RPC_manaBurn_multiCast :10340,
  RPC_fallingStars_multiCast :10354, RPC_fallingComets_multiCast :10375, RPC_frozenBlast_multiCast :10613,
  RPC_arcticWind_multiCast :10634, RPC_iceBlock_multiCast :10768, RPC_parallelShift_multiCast :11604 (repeats)
- RPC_manaMissile_fire :10025 / _hit :10281, RPC_manaBurn_fire :10333, RPC_fallingStars_fire :10361,
  RPC_fallingComets_fire :10382, RPC_meteora_fire :10599, RPC_frozenBlast_fire :10620, RPC_arcticWind_fire :10641,
  RPC_iceBlock_fire :10703, RPC_tornado_hit / _fire / _move / _destroy :10789-11072, RPC_typhoon_fire / _move /
  _destroy :11137-11360
- RPC_giantStars_fire :11611, RPC_giantComets_fire :11618 (Giant Star #442's swap, called from :25150 / :26323; cued
  with `giantStar` / `giantComet`)
- RPC_manaVortex_create :10396 (Mana Vortex's summon)
- RPC_manaPool_hit :10549 (Nova Flare #254's refund flash. Only ManaVortex.RPC_dead sends it (ManaVortex.cs:1330), and only
  when the vortex holds MP. The Nova Flare cue already explains why it is left out. Not a skill press, so no tile.
  `manaPool_hit` is ready if ever wanted.)
- RPC_activateIcon1 :16113 (no tile, decision 19)
- RPC_revive :16232 (the getUp clip + voice `revive`, the KO tile's continuation; it has a clip, so it is not
  effect-only. Open: `Voices/revive` is not cued on `getUp`; that is outside this task)

**Shared by every class** (the same 12 + 4 RPCs are in all 12 hero files):
- The supplement skills (`sup_*`, SkillData.cs:1526-1750; Penguin dispatcher from :8093): RPC_obsidianFang :11752 / _hit
  :11759, RPC_stunningGround :11802, RPC_psalmOfEnergy :12045, RPC_seaAegis :12215, RPC_assassinate :12402,
  RPC_zephyrLore :12409, RPC_mineWalker :12503, RPC_replenishment :12510, RPC_elementalBound :12639, RPC_divineChannel
  :12782, RPC_astralShift :12789, RPC_bloodCarnage :12980. They are not Penguin skills; a cross-class job if ever.
- Items / mount / coin / pet: RPC_useItem :13771, RPC_useMount :13828, RPC_useCoin :13881, RPC_petEffect :16075

**Effect-only: the five below.** RPC_manaArc :10291, RPC_dispell :10298, RPC_multiCast :9819 (Double Cast + Triple Cast),
RPC_frostSpike_fire :11625. The TTO-only Lv 100 skills (constellation, frostFieldLeap, emperorPenguin) all have clips and
are cued (plans/fx_penguin/tto.md).

## How each reads (junk predicates evaluated)

The obfuscator's `if (a - b ==/!= c)` guards were worked out by hand for every branch quoted here. Every path below is
the live one.

### Mana Arc (max rank 4, Penguin Of Arc #412 on)
- Dispatcher: `pgn_manaArc4` :7430 → `StartCoroutine(RPC_manaArc(...))` :9072, ActionEvent :9085. No PlayAnimation.
- At 0 (case 0, :21753 on): actionTime; addTimeOut("manaArc", 1) :21756 (cooldown 1 s, bare); Focus Intellect read and
  removed (no visual).
  - hasSkill(412) :21774 → `Effects/penguinOfArc` :21786, `createEffect(..., hero + 0.5f * Vector3.up,
    UnityEngine.Random.rotation)` :21798. Without 412: `Effects/manaArc` :21821, created the same way at :21833.
  - Voice, when `Time.time > RFMLZHaMjg` (a 2 s voice timer, set at :21883): Random.Range(0, 2) :21886 → manaArc1 (:21896,
    PlayOneShot :21961) or manaArc2 (:21927, :21958).
- Yield 0.1 s (:21963), then case 2 (:21684): FindAreaTarget(hero, 3, 3) :21696 and hit() :21724. The 10 m target is
  outside 3 m, so nothing is drawn there.
- The effects (probe): EffectControl life 2, afterLife 0, followPosition **false**, followState false. Five RingEmitters
  at fixed tilts under the root (delays 0-0.09 s, lives 0.3-0.5 s, end radii 3.0-3.5 m for penguinOfArc against
  2.2-2.7 m for manaArc), stardust particles, and its own Sounds/manaArc (`sfx/manaArc.mp3` already exists: Constellation's
  Row6Sound). `Random.rotation` turns the whole ring cage at random on every cast, a different gyroscope each time.

### Dispell (max rank 2)
- Dispatcher: `pgn_dispell2` :7468 → `StartCoroutine(RPC_dispell(...))` :9037, ActionEvent :9050. No PlayAnimation.
- At 0 (:22277 on): addTimeOut("dispell", agiAdjust(3 + sLv)) :22280; `Effects/dispell` :22289 created at the hero's
  position and rotation :22301; voice, when `Time.time > yZ9Lw4YB8R` (a 6 s voice timer, :22350): Random.Range(0, 2)
  :22355 → dispell1 (:22367, :22379) or dispell2 (:22398, :22410); the local player's camera gets
  `AddScreenWarp(0.1, "ringMask", 1.5, ...)` :22433.
- Yield 0.1 s (:22443), then case 2 (:22126): orbs named mirageOrb / skyOrb within 6 m are destroyed (:22149); the
  `dispell` status (level 2 x sLv + 1 with #422) goes to every unit in 5 x 3 m, the caster's own team too (:22208,
  :22252). The status draws nothing (CharacterControl.cs:38485-38544 only removes Magical statuses).
- The effect (probe): EffectControl life 1, afterLife 1, followPosition true; a RingEmitter 0.8→2 m, a VortexEmitter
  1→3 m, stardust, and its own Sounds/dispell.
- Left out: the screen warp (a camera post effect for the local player; the page has none; Cat :8668, Chameleon :23234
  and Whale :23824 make the same call, which would be a cross-class part if wanted).

### Double Cast / Triple Cast
- Dispatcher: `pgn_tripleCast2` :7372 / `pgn_doubleCast1` :7384 → `this.RPC_multiCast(pos, dir, tID, sLv)` :9135 (a direct
  call, not a coroutine), ActionEvent `"RPC_multiCast" + sLv` :9144. No PlayAnimation.
- RPC_multiCast :9819-10007, all at 0 with no waits: addTimeOut doubleCast and tripleCast agiAdjust(240) (:9826, :9829, a
  shared cooldown); `Effects/multiCast` :9838 at the hero's position and rotation :9850; the `multiCast` status, level
  sLv, chaAdjust(12) s (:9862). Voice Random.Range(0, 2) :9897: == 0 → sLv 1 multiCast1 (:9911, PlayOneShot :10000),
  sLv 2 multiCast2 (:9942, :10006); else multiCast3 for either rank (:9974, :10003). There is no voice timer.
- The effect (already built in `data/penguin/fx.json`): EffectControl life 1, followPosition true, RingEmitter +
  LineEmitter, its own Sounds/trippleCast (`sfx/trippleCast.mp3` exists).
- Left out by decision 10's analogy: the `multiCast` status's purple tint (CharacterControl.cs:38470-38477). Open
  question for the user: on these two tiles the tint is the buff itself. Decision 10 was about Double Spell's 3 s copy.

### Frost Spike (passive #423, one rank)
- Trigger: CharacterControl.cs:31236-31270 (above). The burst goes at the **holder's** position: the shielded Penguin,
  `mTransform.position`.
- RPC_frostSpike_fire at 0: `Effects/frostSpike_ring` :37883, `Instantiate(..., mPos, Quaternion.identity)` :37895;
  voice, when `Time.time > oTnUqDAQW6` (a 12 s voice timer, :37944): Random.Range(0, 2) :37947 → frostSpike1 (:37957,
  PlayOneShot :38017) or frostSpike2 (:37988, :38020).
- Yield 0.1 s (:38015), then case 2 (:37801): FindAreaTarget(mPos, 5, 3) :37813, `frost` on each foe :37852. The 10 m
  target is outside 5 m, so no status look.
- The effect (probe): EffectControl life 1, followPosition false; `frost` StaticMesh + AlphaTimer (texture frostSpike),
  snowFlake particles, a RingEmitter 1→2 m, its own Sounds/frostSpike.
- Quaternion.identity vs the page's hero facing: the same treatment as ManaVortex's identity Instantiate (no rot), and
  the ring and spikes read the same either way.

## Choices made here (rule by rule)
- **Max rank / passives on** (Quick Heal used KO Heal's koHeal): Mana Arc plays `penguinOfArc`, not `manaArc`.
- **Voices every round:** the game's voice timers (2 / 6 / 12 s) only thin the voice out when the skill is spammed. One
  tile play stands for one press (or one proc), and that voices.
- **Step lengths** (`root@t`): the effect's EffectControl life (+ afterLife), at least the longest voice. Mana Arc 2
  (life 2; also its 2 s voice timer), Dispell 2 (1 + 1), Double / Triple Cast 1.5 (multiCast3 is 1.45 s), Frost Spike 1
  (life 1, voices ≤ 0.73 s). Quick Heal used 1 (life 1 + 1; its 1 s cooldown).
- **No `p` rolls:** each tile is the skill itself. Frost Spike's 12 % is what makes it happen, so it plays every time.

## PASTE-READY

### 1. `wardrobe/index.html` SEQ: the penguin line becomes

```js
  penguin: ["Normal Attack: nAttack1@0.5 nAttack2~@0.5 nAttack3~", "Charge Attack: cAttack1@0.7 cAttack2*~@3", "Cast: cast1 cast2*@0 cast3",
    "Cosmic Friday: cast1@0.7 cast2*@0 cast3@0.4 cosmicFriday*@6", "MP Transfer: nAttack1!",
    // Mana Arc, Dispell, Double Cast / Triple Cast (one RPC_multiCast, sLv 1 / 2) and Frost Spike (Ice Shield's proc,
    // passive #423) play no animation: the dispatcher calls their RPCs straight (Penguin.cs:9037-9144) and none calls
    // PlayAnimation (:9819, :21578, :22009, :37695): their effects on the idle stance, each step one effect's life
    // (2026-11-13, plans/fx_penguin/effect_only.md; the user 2026-11-10: effect-only tiles)
    "Mana Arc: root@2", "Dispell: root@2", "Double Cast: root@1.5", "Triple Cast: root@1.5", "Frost Spike: root@1"],
```

### 2. `wardrobe/index.html` SEQ_SKILL: the penguin entry becomes

```js
const SEQ_SKILL = { penguin: { "@MPTransfer": "mpTransfer", "@CosmicFriday": "cosmicFriday", "@ManaArc": "manaArc", "@Dispell": "dispell",
    "@DoubleCast": "doubleCast", "@TripleCast": "tripleCast", "@FrostSpike": "frostSpike" },
```
(the `sheep:` line after it stays as it is)

### 3. `wardrobe/index.html` cueOf: `"rot": "random"` (Unity's Random.rotation), the one page part Mana Arc needs

Above `const cueOf`:
```js
// Unity's Random.rotation (Mana Arc's ring cage, Penguin.cs:21798): a uniform random rotation (Shoemake), as the Euler
// [x, y, z] degrees the placement takes ("YXZ"); drawn when the clip starts, like a random pick
const randRot = () => {
  const u = Math.random(), a = 2 * Math.PI * Math.random(), b = 2 * Math.PI * Math.random(), s = Math.sqrt(1 - u), t = Math.sqrt(u);
  const e = new THREE.Euler().setFromQuaternion(new THREE.Quaternion(s * Math.sin(a), s * Math.cos(a), t * Math.sin(b), t * Math.cos(b)), "YXZ");
  return [e.x, e.y, e.z].map(r => r * 180 / Math.PI);
};
```
In `cueOf`, `rot: o.rot || null,` becomes `rot: o.rot === "random" ? randRot() : o.rot || null,`. In the options comment
above it, after `rot ([x, y, z] degrees, Unity's Euler, after the hero's facing)`, add `or "random" (Random.rotation)`.
A uniform rotation times the hero's facing is still uniform. `wardrobe_fx_check.py`'s OPTS already allows `rot`, and it
does not type-check the value.

**Without this part** use `{"y": 0.5}` alone: the cage then stands at its prefab tilts every play, one fixed gyroscope.

### 4. `wardrobe/fx_cues/penguin.json`: five entries (insert after `"focusIntellect"` or before `"wave"`)

```json
  "@ManaArc:root": {
    "why": "Penguin.cs RPC_manaArc (:10291, coroutine :21578-21965) at max rank (sLv 4, pgn_manaArc4 :7430; the dispatcher starts it with no clip, :9072-9085; the tile plays it on the idle stance): at 0 addTimeOut 1 s (:21756); Penguin Of Arc #412 on (passives on, hasSkill(412) :21774): Effects/penguinOfArc at the hero + 0.5 m up with Random.rotation (createEffect :21786-21798; else Effects/manaArc the same way, :21821-21833; EffectControl life 2, no followPosition, no followState; plays its own Sounds/manaArc); voice manaArc1 / manaArc2 (Random.Range(0, 2) :21886, :21896-21961; the game skips it within 2 s of the last, :21877-21883); Yield 0.1 (:21963): the hit on foes within 3 m (FindAreaTarget :21696, hit :21724): the 10 m target is out of reach, nothing drawn",
    "cues": [
    [0, "fx", "penguinOfArc", {"y": 0.5, "rot": "random"}],
    [0, "voice", "manaArc1|manaArc2"]
    ]
  },
  "@Dispell:root": {
    "why": "Penguin.cs RPC_dispell (:10298, coroutine :22009-22445) at max rank (sLv 2, pgn_dispell2 :7468; the dispatcher starts it with no clip, :9037-9050; the tile plays it on the idle stance): at 0 addTimeOut agiAdjust(3 + sLv) (:22280), Effects/dispell at the hero's position and rotation (createEffect :22289-22301; EffectControl life 1 + afterLife 1, followPosition; plays its own Sounds/dispell), voice dispell1 / dispell2 (Random.Range(0, 2) :22355, :22367-22410; the game skips it within 6 s of the last, :22344-22350); the local player's camera screen warp ringMask (AddScreenWarp :22433) left out (the page has no camera effects); Yield 0.1 (:22443): orbs within 6 m removed (:22149), the dispell status (2 x sLv, +1 with #422) on every unit within 5 m (:22208, :22252), which draws nothing (CharacterControl.cs:38485-38544)",
    "cues": [
    [0, "fx", "dispell"],
    [0, "voice", "dispell1|dispell2"]
    ]
  },
  "@DoubleCast:root": {
    "why": "Penguin.cs RPC_multiCast (:9819-10007, a plain method: no clip, no wait; pgn_doubleCast1 :7384 calls it with sLv 1, :9135-9144; the tile plays it on the idle stance): all at 0: addTimeOut doubleCast and tripleCast agiAdjust(240) (:9826-9829), Effects/multiCast at the hero's position and rotation (:9838-9850; EffectControl life 1, followPosition; plays its own Sounds/trippleCast), the multiCast status Lv 1 for chaAdjust(12) s (:9862; its purple tint, CharacterControl.cs:38470-38477, left out as decisions.md 10), voice Random.Range(0, 2) (:9897): multiCast1 for sLv 1 (:9911, :10000) or multiCast3 (:9974, :10003)",
    "cues": [
    [0, "fx", "multiCast"],
    [0, "voice", "multiCast1|multiCast3"]
    ]
  },
  "@TripleCast:root": {
    "why": "Penguin.cs RPC_multiCast (:9819-10007, a plain method: no clip, no wait; pgn_tripleCast2 :7372 calls it with sLv 2, :9135-9144; the tile plays it on the idle stance): all at 0: addTimeOut doubleCast and tripleCast agiAdjust(240) (:9826-9829), Effects/multiCast at the hero's position and rotation (:9838-9850; EffectControl life 1, followPosition; plays its own Sounds/trippleCast), the multiCast status Lv 2 for chaAdjust(12) s (:9862; its purple tint, CharacterControl.cs:38470-38477, left out as decisions.md 10), voice Random.Range(0, 2) (:9897): multiCast2 for sLv 2 (:9942, :10006) or multiCast3 (:9974, :10003)",
    "cues": [
    [0, "fx", "multiCast"],
    [0, "voice", "multiCast2|multiCast3"]
    ]
  },
  "@FrostSpike:root": {
    "why": "Penguin.cs RPC_frostSpike_fire (:11625, coroutine :37695-38022), Frost Spike #423's proc (no clip; the tile plays it on the idle stance, the proc every play): a hit absorbed whole by an Ice Shield on a Penguin who learned it rolls lckAdjust(12) = 12 % (CharacterControl.cs:31236-31242) and fires it at her position (:31259-31270); at 0 Effects/frostSpike_ring there, Quaternion.identity (Instantiate :37883-37895; EffectControl life 1; plays its own Sounds/frostSpike), voice frostSpike1 / frostSpike2 (Random.Range(0, 2) :37947, :37957-38020; the game skips it within 12 s of the last, :37938-37944); Yield 0.1 (:38015): frost on foes within 5 m (:37813, :37852): the 10 m target is out of reach, nothing drawn",
    "cues": [
    [0, "fx", "frostSpike_ring"],
    [0, "voice", "frostSpike1|frostSpike2"]
    ]
  },
```
(the comma after the last `}` goes only if another entry follows; check with
`py -3 -c "import json; json.load(open('wardrobe/fx_cues/penguin.json', encoding='utf-8'))"`)

Mana Arc without the page part (3): `[0, "fx", "penguinOfArc", {"y": 0.5}],` and in its why "(Random.rotation not
reproduced: the prefab's tilts)".

**Frost Spike, a variant for the user to look at** (not the default; the game bursts only while the shield is on). It
uses `"Frost Spike: root@2"` and these cues; the shield is Ice Shield's own cue, cut at the step's end:
```json
    [0, "fx", "iceShield", {"y": 0.6, "scale": 0.7, "kill": 2}],
    [0.5, "fx", "frostSpike_ring"],
    [0.5, "voice", "frostSpike1|frostSpike2"]
```
The catch: the shield forms again on every round (with its own Sounds/iceShield). In the game it stays 30 s.

### 5. `pipeline/wardrobe_skill_icons.py` EFFECT_ONLY

```python
EFFECT_ONLY = {"sheep": ["quickHeal"], "penguin": ["manaArc", "dispell", "doubleCast", "tripleCast", "frostSpike"]}
```
The four already listed are in `data/icons/hd/index.json` (clips ["root"]). `frostSpike` is new: the Bible has
`penguin_frostSpike5`, so `best` finds it. Then run `py -3 pipeline\wardrobe_skill_icons.py`.

### 6. Build (merges into `wardrobe/data/penguin/fx.json` and `sfx/`), then check

```
uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py penguin --fx penguinOfArc,dispell,multiCast,frostSpike_ring --voices manaArc1,manaArc2,dispell1,dispell2,multiCast1,multiCast2,multiCast3,frostSpike1,frostSpike2
py -3 pipeline\wardrobe_skill_icons.py
uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py D:/12tails-wardrobe checks/fx_penguin dark --cls penguin
```
`multiCast` is already built; listing it again is harmless (merge) and keeps the line self-contained. Add `manaArc` to
`--fx` only if the user wants the rank-without-412 look. The effects' own sounds come with them: dispell.mp3 and
frostSpike.mp3 are new; manaArc.mp3 and trippleCast.mp3 are already there. The built data is tracked in git: commit
`wardrobe/data/penguin/fx.json`, `sfx/`, any new `data/fx/tex/*.webp` and `data/icons/hd/` (penguin/frostSpike.webp,
index.json).

## Open points for the user
1. Mana Arc's random rotation: build the small `"rot": "random"` option (3), or keep the fixed prefab tilts.
2. Double / Triple Cast: show the `multiCast` purple tint for the buff's time? Decision 10 left out Double Spell's.
3. Frost Spike: the burst alone (default) or with the Ice Shield around her (the variant).
4. Dispell's camera screen warp (and the Cat / Chameleon / Whale ones): left out; a screen post effect would be its
   own cross-class part.

## Verification

Read-only check (2026-11-13, home PC). I re-read every claim against `D:\12tails\DecompiledSource\Penguin.cs`,
`CharacterControl.cs`, `ManaVortex.cs`, `SkillData.cs`, the Bible (`12t_reference/penguin-skill-reference.md`, the
skill cards in `12t_projects/bible/index.html`, `assets.js`), the probe (`wardrobe_fx.py penguin --probe
penguinOfArc,manaArc,dispell,frostSpike_ring,multiCast`, exit 0), `node pipeline/clip_calls.js D:/12tails/DecompiledSource
wardrobe/data penguin`, the rip's WAVs, and the page, cue file and check scripts. I evaluated the junk predicates by hand.

### What holds
- **The list of clip-less skills is complete.** My own listing finds 92 `RPC_*` definitions (`void|IEnumerator RPC_*(`).
  The report's four groups add up to 32 + 39 + 17 + 4 = 92, and nothing is missing or counted twice. clip_calls.js gives
  30 RPCs that play a skill clip, and none of them is manaArc, dispell, multiCast or frostSpike_fire. Of the dispatcher's
  58 `pgn_*` cTypes (Penguin.cs:7372-8067), only these four reach an RPC with no clip. The only CharacterControl branch
  that starts a Penguin RPC is the Frost Spike one (:31259). The other `Type == "Penguin"` checks (:21365, :21401,
  :23063, :23125) test skill ids and spawn nothing. The 16 shared RPCs (12 supplements, obsidianFang_hit, item / mount /
  coin / pet) are in all 12 hero files, including Panda.cs.
- **Ranks (sLv starts at 1, then each `num2++`):**
  - pgn_manaArc4 has 3 increments (:7436, IL_28A5 :9064, IL_4FF :9057), so it reaches IL_2D9B (:9071, call :9072) with
    sLv 4.
  - pgn_dispell2 has 1 increment (:7474) and reaches :9037 with sLv 2.
  - pgn_tripleCast2 has 1 increment (:7378) and pgn_doubleCast1 none, both reaching :9135 with sLv 2 and sLv 1.
- **Mana Arc:**
  - hasSkill(412) is at :21774. penguinOfArc is loaded at :21786 and created at :21798 at hero + 0.5 up with
    `UnityEngine.Random.rotation`. Without #412, manaArc is loaded at :21821 and created at :21833.
  - createEffect is a plain Instantiate plus InitEffectControl (CharacterControl.cs:24191).
  - The voice timer: `<=` skip at :21877, `+2` at :21883. The random pick is at :21886. The voices: manaArc1
    :21896 / :21961 and manaArc2 :21927 / :21958.
  - Yield 0.1 is at :21963. The hit: FindAreaTarget 3 x 3 at :21696, hit at :21724.
- **Dispell:**
  - The cooldown is `agiAdjust(3 + sLv)` (:22280). The effect is loaded at :22289 and created at :22301 with the
    hero's position and rotation.
  - The voice timer is 6 s (:22344-22350). The pick is at :22355 (dispell1 :22367 / :22379, dispell2 :22398 / :22410).
  - The screen warp (:22433) is only for `Game.mPlayer`.
  - Yield 0.1 is at :22443. Orbs are removed within `sqrMagnitude < 36` (:22149-22186). The status mask is 130818
    (every team) at 5 x 3 times rangeMod (:22203-22252).
  - The status draws nothing (CharacterControl.cs:38485-38544).
- **Double Cast / Triple Cast:**
  - RPC_multiCast (:9819-10007) is a plain method with no clip and no wait. It sets both timeouts (:9826, :9829),
    creates the effect (:9838 / :9850) and adds the status (:9862).
  - `Random.Range(0, 2) == 0` (:9897) gives multiCast1 for sLv 1 (:9911, the PlayOneShot reached by the `break` at
    :9921, :10000) or multiCast2 for sLv 2 (:9942, :10006). Otherwise it gives multiCast3 (:9974, :10003). There is no
    voice timer.
  - The remote strings are at :1663 / :1675 / :4038 / :4056.
  - The tint is mColor (0.48, 0.29, 0.78) (CharacterControl.cs:38470-38477).
  - The Bible card's "เข้าสู่ท่าร่ายเวทขั้นสูง" is tooltip wording; the code plays no clip.
- **Frost Spike:**
  - The proc sits in the full-absorb branch of the holder's iceShield status (`sValue > nDamage`). The order is
    isMine, then Type Penguin, then hasSkill(423) (:31236), then `Random.Range(0, 100) < lckAdjust(12)` (:31242), then
    the coroutine at the holder's `mTransform.position` (:31259, ActionEvent :31270). The Bible's #423 section agrees.
  - The effect is a plain `Instantiate(..., mPos, Quaternion.identity)` at :37895 (load :37883).
  - The voice timer is 12 s (:37938-37944). The pick is at :37947, with the voices at :37957 / :38017 and :37988 /
    :38020.
  - Yield 0.1 is at :38015. Frost is applied within 5 x 3 m (:37813, :37852).
- **The probe matches the report:**
  - penguinOfArc / manaArc: life 2, afterLife 0, followPosition false. Five RingEmitters with delays 0-0.09, lives
    0.3-0.5 and end radii 3.0-3.5 against 2.2-2.7.
  - dispell: life 1, afterLife 1, followPosition true. A RingEmitter 0.8 to 2 m and a VortexEmitter 1 to 3 m.
  - frostSpike_ring: life 1, followPosition false. The `frost` StaticMesh with an AlphaTimer, and a RingEmitter 1 to
    2 m.
  - multiCast: life 1, followPosition true, a RingEmitter and a LineEmitter.
  - No effect sets followState.
  - Each effect plays its own sound: manaArc, dispell, frostSpike, trippleCast.
- **The WAV lengths match to the hundredth.** Every named voice and sound is in the rip.
- **Other facts that hold:**
  - The fx_inventory line numbers are right (:561, :566, :572, :582, :585).
  - `multiCast` and `iceShield` are already in `data/penguin/fx.json`.
  - manaArc.mp3 and trippleCast.mp3 are in sfx. dispell.mp3, frostSpike.mp3 and the nine v_ voices are not yet.
  - The Bible has `penguin_frostSpike5`, and `data/icons/hd/index.json` already holds the other four with clips
    ["root"].
  - EFFECT_ONLY already lists the four (wardrobe_skill_icons.py:39).
- **The paste-ready blocks match the formats:**
  - Block 4, put in front of `"wave"`, leaves penguin.json valid JSON (checked with json.loads). Its layout matches
    `"@QuickHeal:root"` (sheep.json:465): 2-space key, 4-space why and cues.
  - With block 1 in place, `wardrobe_fx_check.py`'s `seqs()` parse gives ManaArc / Dispell / DoubleCast / TripleCast /
    FrostSpike = ["root"]. Every token passes chains()'s step regex.
  - `rot` is in the check's OPTS (:94), and its value is not type-checked.
  - The SEQ_SKILL ids match chains()'s `"@" + name without spaces`, and no pool member's id clashes with them.
  - The randRot part is right. cueOf runs per play (index.html:4448). The root spawn turns by `Euler(rot, "YXZ")`
    inside the mirror (:3897). A uniform rotation stays uniform under the hero's facing and the mirror.
- **Random picks are the game's.** The four tiles each use the game's `Random.Range(0, 2)` 50/50 voice pick. No effect
  is a random pick, except Mana Arc's rotation.

### Corrections
1. **effect_only.md:64**: "`ko` (one of the two, decision 11)" points to the wrong file. The Penguin's decisions.md 11 is
   Tornado and Typhoon. The KO rule is the Sheep's: `plans/fx_sheep/decisions.md:31` (11). It should read "(one of the
   two, plans/fx_sheep/decisions.md 11)".
2. **effect_only.md:174-176 (paste-ready block 1, the SEQ comment)** wrongly includes Frost Spike. It says "the
   dispatcher calls their RPCs straight (Penguin.cs:9037-9144)" for all five tiles. Frost Spike is not a key press: its
   RPC is started from Ice Shield's absorb branch (CharacterControl.cs:31259). The tile lines are fine. The corrected
   block is below.
3. **effect_only.md:130-131 (and open point 4, :287)**: "Cat :8668, Chameleon :23234 and Whale :23824 make the same
   call" holds only for the method. The masks differ:
   - Cat uses `barrierMask` (Cat.cs:8668).
   - Chameleon uses `zoomMask` (Chameleon.cs:23234).
   - Whale calls it 9 times: `ringMask` at :23824, :29949, :30381, :31486, :33479, :33900, :36346 and :37163, and
     `burstMask` at :35805.

   So a page screen-warp part would need the three masks.
4. **effect_only.md:78**: Giant Star's swap is started at Penguin.cs:25134 (giantStars_fire) and :26310
   (giantComets_fire). The lines :25150 / :26323 that the report cites are those calls' ActionEvents.

A note, not a correction: block 3 (the page's `"rot": "random"`) has to land before or with block 4's Mana Arc cue. Without
it, `at.rot.map` (index.html:3897) throws on the string. If the page part is not built, use the report's fallback cue
`{"y": 0.5}`.

### Corrected paste-ready block set
Blocks 2-6 and the Frost Spike variant stand as written. Block 1 becomes:

```js
  penguin: ["Normal Attack: nAttack1@0.5 nAttack2~@0.5 nAttack3~", "Charge Attack: cAttack1@0.7 cAttack2*~@3", "Cast: cast1 cast2*@0 cast3",
    "Cosmic Friday: cast1@0.7 cast2*@0 cast3@0.4 cosmicFriday*@6", "MP Transfer: nAttack1!",
    // Mana Arc, Dispell and Double Cast / Triple Cast (one RPC_multiCast, sLv 1 / 2) play no animation: the dispatcher
    // calls their RPCs straight (Penguin.cs:9037-9144); Frost Spike (passive #423) is Ice Shield's proc, started from the
    // shield's absorb (CharacterControl.cs:31259); none calls PlayAnimation (:9819, :21578, :22009, :37695): their
    // effects on the idle stance, each step one effect's life (2026-11-13, plans/fx_penguin/effect_only.md; the user
    // 2026-11-10: effect-only tiles)
    "Mana Arc: root@2", "Dispell: root@2", "Double Cast: root@1.5", "Triple Cast: root@1.5", "Frost Spike: root@1"],
```
(The comment has no `"`, so `wardrobe_fx_check.py`'s `seqs()` still parses the line the same way.)
