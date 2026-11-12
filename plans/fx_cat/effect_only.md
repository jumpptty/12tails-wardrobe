# Cat: the skills with no body animation (effect-only tiles)

Research only (2026-11-13, home PC). Read-only researcher: only this report and `checks/fx_cat_research/effect_only/`
were written. Probes (read only, exit 0): `uv run --no-project --with UnityPy python -I pipeline/wardrobe_fx.py cat --probe
awareness1,awareness2,damageRoulette_ring,damageRoulette,evenOdds_hit,insight,treasureHunt,deadEffect` and `... --probe
lifeGamble_ring,skillGamble_ring,lifeGamble_hit,skillGamble_hit` (outputs and a summariser in
`checks/fx_cat_research/effect_only/`). Sources: `D:\12tails\DecompiledSource\Cat.cs` (cited `:line`), `CharacterControl.cs`,
`TreasureBox.cs`, the TTO pseudo-C `DecompiledSource_TTO_2026-11-02/pseudo/Cat.c`, the BB rip
(`RippedAssets/.../heroes/cat/Cat.prefab`, `effects/*.prefab`, `voices/`, `sounds/`, `Material/*.mat`), the Bible's
`12t_reference/cat-skill-reference.md`, its skill cards and `assets.js`, `plans/fx_inventory.md` (### cat). Templates: the
Penguin's effect_only.md (+ its Verification) and the Bat's decisions.md 18 / 28.

## Result

Four Cat skills play no clip at all, and one more (Nine Lives) plays only base clips that nobody else covers:

| Tile (Bible name) | Bible icon | RPC | Effects | Voices | Buildable |
|---|---|---|---|---|---|
| **Awareness** (active, max 2) | `cat_awareness2` | `RPC_awareness` :8563 (plain method) | `awareness2` at the hero; Insight #421's `insight` mark 1.69 m up for 3 s | awareness1 / awareness2 | yes (all parts built) |
| **Damage Roulette** (active, max 2) | `cat_damageRoulette2` | `RPC_damageRoulette` :9585, coroutine :26940 | `damageRoulette_ring` at the hero; the status's spinning `damageRoulette` 0.89 m up from 0.2 s, cut at 10 s | damageRoulette1 / damageRoulette2 | yes |
| **Treasure Hunt** (passive #123) | `cat_treasureHunt1` | `RPC_treasureHunt` :9078 (plain method, started from `TreasureBox.cs:334`) | `treasureHunt` coin burst at the box (1 m ahead) | none | **needs WorldParticleCollider** (the coins bounce on the ground; shared with Lucky Dice's `luckyDice`) |
| **Even Odds** (passive #422) | `cat_evenOdds1` (= `cat_evenOdds5`, same bytes) | `RPC_evenOdds` :9335 (plain method, started inside Life / Skill Gamble) | `evenOdds_hit` at the hero, 0.4 s into the gamble clip | the host skill's (lifeGamble1/2 or skillGamble1/2) | yes |
| **Nine Lives** (passive #263/#264) | `cat_nineLives2` | `RPC_nineLives` :9634, coroutine :27238 (started from `Update` :346) | `deadEffect` at 0 | ninelife1 / ninelife2 at 3 s (TTO's fix, see Q5) | yes; body clips `ko` then `getUp` (base clips: a sequence, not root) |

**No effect uses followState** except the gamble rings that Even Odds' tile reuses (`lifeGamble_ring`, `skillGamble_ring`:
followState true, cut at 0.7 s). Every voice and every effect sound named exists in the rip. Lengths: awareness1 0.64 s,
awareness2 0.71, damageRoulette1 0.92, damageRoulette2 1.21, ninelife1 1.01, ninelife2 0.88, lifeGamble1 1.17,
lifeGamble2 0.76, skillGamble1 1.15, skillGamble2 0.99 (inSight1 0.58, inSight2 0.66: Q1); the effects' own sounds
awareness 1.08, damageRoulette 0.93, evenOdds 0.93, gamble_ring 0.51.

Insight (#421, `cat_insight5`) has no RPC: it only adds the `insight` status to every Awareness cast, so it is folded into
the Awareness tile (passives on, as the Penguin's Penguin Of Arc into Mana Arc and the Sheep's KO Heal into Quick Heal).

## Accounting: every RPC_* in Cat.cs (84 definitions)

`grep -E "^\s(public|private|internal|protected) [^(]*\bRPC_\w+\(" Cat.cs` = 84; the groups below add up to 31 + 24 + 17 + 7 +
5 = 84.

**Clips other researchers cover (31):** RPC_nAttack1-4 :8225-8246, RPC_cAttack1 :8549 (cAttack1 / cAttack2), RPC_luckyCard
:9121 and RPC_luckyDice :9382 (throw1), RPC_fateDraw :9135 and RPC_doubleDown :9436 (instantCast), RPC_powerShuffle :9142,
RPC_lifeGamble :9149, RPC_skillGamble :9242 (gamble), RPC_twoPair :9457 and RPC_copycat :9521 (pointTarget),
RPC_grandCasinoArcade :9641, RPC_flyingDagger :9818, RPC_disarm :10212 and RPC_bleed :10262 (throw2), RPC_forwardLunge
:9868, RPC_reverseThrust :9918, RPC_backflip :9968, RPC_heartRipper1 :9975, RPC_heartRipper2 :9982, RPC_moonBlade :10312,
RPC_moonStorm :10319, RPC_deltaStrike :10326, RPC_finishingBlow1 :10383, RPC_finishingBlow2 :10390, RPC_swiftPace :10397,
RPC_pillagePlunge :10490 (pillage), RPC_supportFire :10540 (supportFire1 / 2). (`node pipeline/clip_calls.js
D:/12tails/DecompiledSource wardrobe/data cat` lists exactly these 31 as the RPCs that play a skill clip.)

**Phases of those skills (24):** RPC_nAttack_hit :8253, RPC_cAttack0 :8556 (Charge Attack's release, PlayAnimation(root)
:20348), RPC_luckyCard_hit :9128, RPC_lifeGamble_heal :9156 / _hit :9199, RPC_skillGamble_heal :9249 / _hit :9292,
RPC_luckyDice_hit :9389, RPC_doubleDown_hit :9450, RPC_twoPair_hit :9464, RPC_copycat_hit :9528,
RPC_grandCasinoArcade_hit :9648, RPC_flyingDagger_hit :9825, RPC_forwardLunge_hit :9875, RPC_reverseThrust_hit :9925,
RPC_disarm_hit :10219, RPC_bleed_hit :10269, RPC_deltaStrike_hit :10333, RPC_pillagePlunge_hit :10497, RPC_supportFire0
:10547 (its cancel, from :41269), RPC_supportFire_fire :10636, RPC_supportFire_hit :10776, and two passives' procs that
live inside clip skills: **RPC_hiddenBlade_hit :10059** (Hidden Blade #331-334 / Jagged Knife #433's replacement hit inside
nAttack1-4, :16638-19074: hiddenBlade_hit at the target's hit point + voice hiddenBlade1 / 2 :10146-10177) and
**RPC_backStab_hit :10340** (Backstab #413 inside Forward Lunge :30409 / :30656 and Reverse Thrust :31491 / :31728:
backStab_hit at the hit point). Both draw only at the target and both are those clips' researchers' (Q8).

**Shared by every class (17):** the 12 supplement skills (SkillData `getSupportSkill`, the Bible reference's "Support-skill
exclusion"): RPC_obsidianFang :10926 (+ _hit :10933), RPC_stunningGround :10976, RPC_psalmOfEnergy :11216, RPC_seaAegis
:11386, RPC_assassinate :11573 (its assets live in the Cat's folder, `assassinate_hit` / assassinate1-2, but Penguin.cs
:40299 and Wolf.cs :38328 load the same Cat files: it is a shared skill, not the Cat's), RPC_zephyrLore :11580,
RPC_mineWalker :11674, RPC_replenishment :11681, RPC_elementalBound :11810, RPC_divineChannel :11956, RPC_astralShift
:11963, RPC_bloodCarnage :12154; items / mount / coin / pet: RPC_useItem :12945, RPC_useMount :13002, RPC_useCoin :13055,
RPC_petEffect :15246. (The private `onSupport` :10886, voice `support`, is the shared team-support line, not an RPC.)

**Emotes, KO, mission (7, the attacks_emotes researcher's):** RPC_emotion :12501, RPC_emotion0 :12508 (cancel to standby),
RPC_activateIcon1 :15284 (battle looped + activate1), RPC_activateIcon2 :15291 (cancel), RPC_ko :15389, RPC_dead :15396,
RPC_revive :15403.

**Mine (5):** RPC_awareness :8563, RPC_damageRoulette :9585, RPC_treasureHunt :9078, RPC_evenOdds :9335 (effect-only),
RPC_nineLives :9634 (base clips only).

**TTO:** the TTO client's Cat RPCs not in BB are RPC_anchorYank, RPC_crescentEclipse, RPC_dropAnchor, RPC_eclipseRupture
(Crescent Eclipse's phase) and RPC_royalFlush (`pseudo/Cat.c` "// ==== Cat::RPC_*"), all clip skills of the tto
researcher. None of the five above is TTO-only, so the released-list rule does not touch them.

## How each reads (junk predicates evaluated by hand)

### Awareness (cat_awareness2, sLv 2)
- Dispatcher: `cat_awareness2` :5912, `num2++` :5918 (sLv 2) → `this.RPC_awareness(...)` :7846 (a plain call), ActionEvent
  :7855. No PlayAnimation anywhere between the press and the end of the method (none in the dispatcher :5800-8550).
- All at 0, no wait: actionTime; addTimeOut("awareness", 1) :8574 (bare 1 s); sLv 2 → `Effects/awareness2` :8630,
  `Instantiate(..., hero position, Quaternion.identity)` :8642 (sLv 1 would be awareness1 :8591 / :8603).
- The local player's `AddScreenWarp(0.1, "barrierMask", 1.5, ...)` :8668: left out (as the Penguin's Dispell).
- Voice, when `z0XRgIOuIl < Time.time` (:8706; +3 s :8712): Random.Range(0, 2) :8717 → awareness1 (:8729, PlayOneShot :8741)
  or awareness2 (:8760, :8772).
- `awareness` Lv 2, 1 s, on every unit within 12 x sLv = 24 m (:8674, FindAreaTarget :8797, RPC_AddStatus :8837): its
  apply only strips blend / invisible (CharacterControl.cs:36204-36227): nothing drawn.
- Insight #421 (passives on): `hasSkill(421)` :8848 → `insight` Lv 1 for chaAdjust(3) :8854. The status apply
  (CharacterControl.cs:36402-36431): `Effects/insight` Instantiated at `mChar.bounds.center + 0.5 x mChar.height x up`,
  identity, named insightFx, parented; removed with the status (:16256-16269). mChar is the CharacterController: the Cat's
  is m_Center y 0.89, m_Height 1.6, m_Radius 0.2 (`heroes/cat/Cat.prefab:835-841`), so the root sits at 0.89 + 0.8 = 1.69 m
  and its one particle (node y 0.5) at 2.19 m. chaAdjust(3) = 3 s at CHA 1 (CharacterControl.cs:20593: (int)(3 x 1.015)).
- Treasure Hunt #123's part of Awareness (`hasSkill(123)` :8896 → displayTreasure :8916, the minimap for chaAdjust(5)) and
  the reveal of boxes / hidden items within 24 m (:8922-9041, TreasureFound :8945) draw nothing on the Cat.
- Probe: awareness1/2 EffectControl life 1, afterLife 1, followPosition false, followState false; one RingEmitter (windRay),
  radius 0 → 5 m (awareness1) / 0 → 8 m (awareness2), life 0.5; AudioSource `awareness`. insight: no EffectControl, one
  one-shot EllipsoidParticleEmitter (energy 12, size 0.3, local space) + ParticleAnimator + ParticleRenderer (material
  `insight`, built-in shader 203 = alpha). All parts built.

### Damage Roulette (cat_damageRoulette2, sLv 2)
- Dispatcher: `cat_damageRoulette2` :6165, `num2++` :6171 → `StartCoroutine(RPC_damageRoulette(...))` :7582, ActionEvent
  :7595. No PlayAnimation.
- At 0 (the default case): addTimeOut agiAdjust(60) :27071; `Effects/damageRoulette_ring` :27080, `createEffect(..., hero
  position, Quaternion.identity)` :27092; voice Random.Range(0, 2) :27135 → damageRoulette1 (:27145, PlayOneShot :27207) or
  damageRoulette2 (:27176, :27201); no voice timer.
- Yield 0.2 :27209 → case 2: `RPC_AddStatus("damageRoulette", sLv, chaAdjust(12), ...)` on herself :27052.
- The status apply (CharacterControl.cs:36254-36273): `Instantiate(Effects/damageRoulette, zero, identity)`, size
  `Clamp(2 x mChar.radius + 0.4, 1, 1.5)` = Clamp(0.8) = 1, named damageRouletteFx, moved to `collider.bounds.center` (y
  0.89), parented, localScale 1. Destroyed when the status ends (:16223-16236). chaAdjust(12) ≥ 12 s → cut at 10 s.
- While it holds, the Cat's hits go to a random unit within 24 m (CharacterControl.cs:4832-4890): no effect.
- Probe: damageRoulette_ring EffectControl life 1, followPosition true; ImageEmitter (Ring2) and LineEmitter (Ray4) 1 m up;
  AudioSource `damageRoulette`. damageRoulette: no EffectControl; an Animation (`root`, 1 s, wrap 2 = loop: a full turn a
  second about the local z axis) on a StaticMesh cross of four panels (`damageroulette`, shader 202 = addsoft). Parts built.
- Identity rotation in world: as the Penguin's identity Instantiates (ManaVortex, Frost Spike), no `rot`.

### Treasure Hunt (passive #123)
- Not a key press. `TreasureBox.cs` OnGUI (:183-400): once a box has been found (`i3mcJ7xDCyp`, set by TreasureFound
  :402-465, which Awareness sends within 24 m), and the local player stands within 2 m ((int)Clamp(sqrMagnitude) ≤ 3,
  :239-242), the box shows a button; clicking it as a Cat (:267-273; "Only for cat!" otherwise :369) takes the box level
  (wood 1 ... diamond 4, :286-322) and calls `cat.RPC_treasureHunt(box position, box forward, 0, level)` :334 (ActionEvent
  :343); the box plays `open` :349 and is destroyed 3 s later (:355). Any Cat can do it: #123 is not checked here.
- RPC_treasureHunt (:9078-9116): `Effects/treasureHunt` :9091, `Instantiate(..., firePos, Quaternion.identity)` :9101; the
  level is unused; no voice.
- Probe: EffectControl life 1, afterLife 0, no follow; one-shot EllipsoidParticleEmitter (12-36 coins, `Gil` 2 x 2 sheet,
  size 0.1, energy 1-1.5, world space, localVelocity y 3, rndVelocity (4, 2, 4)); ParticleAnimator force (0, -9, 0),
  autodestruct; a RingEmitter 0.2 → 0.8 m. The rip prefab also has a **WorldParticleCollider** (`effects/treasureHunt.prefab
  :176-187`: bounceFactor 0.5, collisionEnergyLoss 0, collidesWith layer bit 0 = Default, minKillVelocity 0), which
  `wardrobe_fx.py` does not export (it only reads MonoBehaviours, renderers, meshes, legacy emitters and AudioSources): the
  coins would fall through the floor. Lucky Dice's `luckyDice` carries the same collider with the same values
  (`luckyDice.prefab:246-252`), so the part is needed for the Cat in any case.

### Even Odds (passive #422)
- Its only callers are the lose branches of Life Gamble (:22801-22826) and Skill Gamble (:23328-23353): `hasSkill(422)` and
  `isTimeOut("evenOdds") == 0` → `RPC_evenOdds(hero position, forward, 0)` and the loss is skipped (the life branch jumps
  past RPC_AddDamage / lifeGamble_hit :22834-22839 to the 0.3 s wait; the skill branch past the MP / SP halving and
  skillGamble_hit :23361-23371).
- RPC_evenOdds (:9335-9378): addTimeOut evenOdds agiAdjust(90) :9342; `Effects/evenOdds_hit` :9351, `createEffect(...,
  hero position, hero rotation)` :9361. No voice.
- The host timeline, both skills alike: at 0 PlayAnimation(gamble, 0) (life :22949, skill :23481), the ring at the hero
  with her rotation (life :22967-22979, skill :23499-23511), voice Random.Range(0, 2) (life :23022 → lifeGamble1 :23032 /
  lifeGamble2 :23063, PlayOneShot :23102 / :23097; skill :23554 → :23564 / :23595, :23646 / :23649; no voice timer); Yield
  0.4 (life :23111, skill :23630) → the roll (life `lckAdjust(50) > Random.Range(0, 100)` :22768, skill
  `Random.Range(0, 100) < lckAdjust(50)` :23290) → Even Odds on a loss; Yield 0.3 (:23100, :23636) → standby at 0.7 s
  (:22879, :23411).
- Probe: evenOdds_hit EffectControl life 2, followPosition; a one-shot sprite 2 m up, two RingEmitters (0.8 m, 1.5 m up);
  AudioSource `evenOdds`. lifeGamble_ring / skillGamble_ring: life 1, followPosition, **followState true** (cut at 0.7 s);
  ImageEmitter Ring_Gambler, LineEmitter, RingEmitter (emission 4 vs 6: otherwise the same); AudioSource `gamble_ring`.
- It fires only inside the gamble clip, so its tile is the gamble clip, not root: a sequence of its own ("Even Odds:
  gamble") whose `@EvenOdds:gamble` entry is a two-member pool, each member that host skill's own opening plus the burst
  (the "@<sequence>:<clip>" pools stay random and keep each member's ring and voice together, as the Sheep's seals).

### Nine Lives (passive #263 / #264, max rank 2)
- Trigger: `Update` (:101 on) when her HP is gone: autoLife (:245-272) and the Small Anubi pet (:291-303) first, then
  `Random.Range(0, 100) < lckAdjust(nineLivesLv x 6)` :334 (getNineLivesLv :9591-9630: 2 = 12 %) and no `death` status
  (:340) → `StartCoroutine(RPC_nineLives(...))` :346 (ActionEvent :359) **in place of** RPC_dead (:367).
- Coroutine (:27238-27660), at 0 (default case): hp 0, actionState dead (:27581-27584), back at her spot and facing,
  `animation.Rewind(); animation.Play("ko")` (a cut, :27608), `Instantiate(deadEffect, position, rotation)` :27614 (the Cat
  prefab's field, `effects/deadEffect`: EffectControl life 3). No voice at 0 (RPC_ko's ko1 / 2 and RPC_dead's dead1 / 2
  are not played). Yield 3 :27638.
- Case 2 (3.0 s), still dead: hp 99, ko refilled, actionState attack, addTimeOut agiAdjust(60) :27390 (never read: the
  Bible's note), `noDamage` 3 s :27395 (draws nothing: its apply only releases targets, CharacterControl.cs:32931-32935),
  `animation.Play("getUp")` (a cut, :27400), voice Random.Range(0, 2) :27441 → `Voices/nineLives1` :27453 /
  `nineLives2` :27485. **BB has no such files** (the rip has `ninelife1.wav` / `ninelife2.wav`): BB logs "Cannot find
  nineLives1 voice" and stays silent. **TTO fixed the names**: `pseudo/Cat.c:20332-20344` loads
  `.../voices/ninelife1` / `ninelife2`. Yield 1 :27632 → case 3: standby at 4.0 s (:27529).
- Clips: `ko` (0.83 s, base) held to 3 s (the page clamps a once clip on its last frame, index.html startStep), then
  `getUp` (0.9 s, base): 3.9 s, the game's standby 0.1 s later.

## Choices made here (rule by rule)
- **Max rank / passives on:** Awareness 2 (awareness2) with Insight's mark; Damage Roulette 2; Nine Lives 2 (only the
  proc chance changes).
- **Procs every play:** Treasure Hunt, Even Odds and Nine Lives are passives whose tile is the proc itself (the Penguin's
  Frost Spike): no `p`. Even Odds ignores its 90 s cooldown.
- **Voices every play:** Awareness' 3 s voice timer only thins out spamming (Penguin choice).
- **Long buffs cut at 10 s:** the roulette (chaAdjust(12)) `kill 10`; the Insight mark keeps its 3 s.
- **Step lengths:** the longest effect or voice. The Cat's idle `root` is 0.8 s and a once step is clamped on its last
  frame (index.html startStep: `clampWhenFinished = !loop`), so steps longer than the idle are written `root*@t` (held =
  looped idle for t s; the parser and `wardrobe_fx_check.py`'s seqs() take it). Awareness `root*@3` (insight 3 s;
  awareness2 1 + 1), Damage Roulette `root*@10.2` (the roulette from 0.2 to 10.2 s: a shorter step would stack a second
  roulette on each loop round), Treasure Hunt `root*@1` (life 1; `*` harmless). (The Penguin's / Bat's `root@2` tiles
  freeze on the idle's last frame for the rest of the step too: a note for the editor, not this job.)
- **First steps keep the page's 0.2 s fade** although the game cuts (gamble PlayAnimation(.., 0), ko by animation.Play):
  the Bat's decision 28 / the Sheep's and the Penguin's.
- **Left out:** Awareness' camera screen warp (barrierMask); the box for Treasure Hunt (a world object); every status that
  only changes numbers.

## PASTE-READY

### 1. `wardrobe/index.html` SEQ: append to the cat line (after the last current entry, before `],`)

```js
    // Awareness and Damage Roulette play no animation (the dispatcher calls RPC_awareness straight, Cat.cs:7846, and
    // starts RPC_damageRoulette, :7582; neither calls PlayAnimation, :8563-9075, :26940-27237); Treasure Hunt is the coin
    // burst of a found box a Cat opens (TreasureBox.cs:334, RPC_treasureHunt :9078): their effects on the idle stance,
    // held (*) as long as the longest effect, the roulette status cut at 10 s; Even Odds (passive #422) fires 0.4 s into
    // Life / Skill Gamble's gamble clip in place of a lost roll (:22813, :23340): its own tile on that clip; Nine Lives
    // (passive #263-264) replaces the death: ko held 3 s, then getUp (RPC_nineLives :27608, :27638, :27400)
    // (2026-11-13, plans/fx_cat/effect_only.md)
    "Awareness: root*@3", "Damage Roulette: root*@10.2", "Treasure Hunt: root*@1", "Even Odds: gamble", "Nine Lives: ko@3 getUp"],
```
(the comment holds no `"`, so `wardrobe_fx_check.py`'s seqs() parses the line the same way; the entry before it needs a
trailing comma)

### 2. `wardrobe/index.html` SEQ_SKILL: add a cat entry (e.g. before `penguin:`)

```js
const SEQ_SKILL = { cat: { "@Awareness": "awareness", "@DamageRoulette": "damageRoulette", "@TreasureHunt": "treasureHunt",
    "@EvenOdds": "evenOdds", "@NineLives": "nineLives" },
  penguin: { ...
```
(the ids are `"@" + name without spaces`, as chains() makes them; the values are the Bible's skill keys as
`data/icons/hd/index.json` will hold them)

### 3. `wardrobe/fx_cues/cat.json`: six entries (the file is `{}` today; merge with the other researchers' entries)

```json
  "@Awareness:root": {
    "why": "Cat.cs RPC_awareness (:8563-9075, a plain method: no clip, no wait; cat_awareness2 :5912-5918 gives sLv 2, the dispatcher calls it straight :7846, ActionEvent :7855; the tile plays it on the idle stance), all at 0: addTimeOut 1 s (:8574); sLv 2: Effects/awareness2 at the hero's position, Quaternion.identity (Instantiate :8630-8642; sLv 1 would be awareness1 :8591-8603; EffectControl life 1 + afterLife 1, no followPosition, no followState; its ring 0 -> 8 m; plays its own Sounds/awareness); the local player's camera screen warp barrierMask (AddScreenWarp :8668) left out (the page has no camera effects); voice awareness1 / awareness2 (Random.Range(0, 2) :8717, :8729-8772; the game skips it within 3 s of the last, :8706-8712); the awareness status (Lv 2, 1 s) on every unit within 12 x sLv = 24 m (FindAreaTarget :8797, RPC_AddStatus :8837) only strips blend / invisible and draws nothing (CharacterControl.cs:36204-36227); Insight #421 on (passives on, hasSkill(421) :8848): insight Lv 1 for chaAdjust(3) = 3 s (:8854), whose apply puts Effects/insight at the CharacterController's bounds centre + 0.5 x height up = 0.89 + 0.8 = 1.69 m (Cat.prefab m_Center y 0.89, m_Height 1.6), identity, parented (CharacterControl.cs:36402-36431), destroyed with the status (:16256-16269; no EffectControl: kill 3); Treasure Hunt #123's minimap list (displayTreasure :8916) and the boxes and hidden items it reveals (:8922-9041) draw nothing on the Cat",
    "cues": [
    [0, "fx", "awareness2"],
    [0, "voice", "awareness1|awareness2"],
    [0, "fx", "insight", {"y": 1.69, "kill": 3}]
    ]
  },
  "@DamageRoulette:root": {
    "why": "Cat.cs RPC_damageRoulette (:9585, coroutine :26940-27237) at max rank (sLv 2, cat_damageRoulette2 :6165-6171; the dispatcher starts it with no clip, :7582-7595; the tile plays it on the idle stance): at 0 addTimeOut agiAdjust(60) (:27071), Effects/damageRoulette_ring at the hero's position, Quaternion.identity (createEffect :27080-27092; EffectControl life 1, followPosition; plays its own Sounds/damageRoulette), voice damageRoulette1 / damageRoulette2 (Random.Range(0, 2) :27135, :27145-27207; no voice timer); Yield 0.2 (:27209): the damageRoulette status Lv 2 for chaAdjust(12) s on herself (:27052), whose apply Instantiates Effects/damageRoulette (the roulette: a looped 1 s Animation turning a StaticMesh) at her collider's bounds centre (Cat.prefab CharacterController m_Center y 0.89), identity, parented, scale Clamp(2 x radius 0.2 + 0.4, 1, 1.5) = 1 (CharacterControl.cs:36254-36273), destroyed with the status (:16223-16236; no EffectControl): cut at 10 s (kill 10, the 10 s rule); the hits it turns onto a random unit within 24 m (CharacterControl.cs:4832-4890) draw nothing",
    "cues": [
    [0, "fx", "damageRoulette_ring"],
    [0, "voice", "damageRoulette1|damageRoulette2"],
    [0.2, "fx", "damageRoulette", {"y": 0.89, "kill": 10}]
    ]
  },
  "@TreasureHunt:root": {
    "why": "Cat.cs RPC_treasureHunt (:9078-9116, a plain method, no clip; the tile plays it on the idle stance, every play): TreasureBox.cs OnGUI: a box Awareness has found (TreasureFound :402-465, sent within 24 m, Cat.cs:8927-8945) shows a button while the player stands within 2 m ((int)sqrMagnitude <= 3, :239-242); a Cat clicking it (:267-273, else 'Only for cat!' :369; Treasure Hunt #123 is not checked) calls cat.RPC_treasureHunt(the box's position, its forward, 0, box level) (:286-334, ActionEvent :343), the box plays open (:349) and goes 3 s later (:355); RPC_treasureHunt Instantiates Effects/treasureHunt there, Quaternion.identity (:9091-9101; the level unused; EffectControl life 1: 12-36 coins thrown up 3 m/s +- (4, 2, 4), gravity -9, bouncing 0.5 on the ground: WorldParticleCollider, treasureHunt.prefab:176-187; no voice, no sound); the box itself (a world object) is not drawn: the burst 1 m ahead (any spot within 2 m)",
    "cues": [
    [0, "fx", "treasureHunt", 1]
    ]
  },
  "@EvenOdds:gamble": {
    "why": "Even Odds #422 (passive, CD agiAdjust(90), Cat.cs:9342) has no press of its own: a Life Gamble or Skill Gamble roll lost with #422 learned and evenOdds off cooldown calls RPC_evenOdds in place of the loss (Cat.cs:22801-22826, :23328-23353), 0.4 s into the gamble clip; its own tile on that clip, the host skill picked at random each play (the members below keep each skill's ring and voice together), the proc every play",
    "skills": {
      "lifeGamble": {
        "why": "Cat.cs RPC_lifeGamble (coroutine :22625-23125): at 0 addTimeOut agiAdjust(30) (:22940), clip gamble cut (:22949), Effects/lifeGamble_ring at the hero's position and rotation (createEffect :22967-22979; EffectControl life 1, followPosition, followState: cut at standby 0.7 s; plays its own Sounds/gamble_ring), voice lifeGamble1 / lifeGamble2 (Random.Range(0, 2) :23022, :23032-23102; no voice timer); Yield 0.4 (:23111): the roll lckAdjust(50) > Random.Range(0, 100) (:22768) lost (a win heals, :22774-22779), Even Odds #422 on and off cooldown (hasSkill(422) :22801, isTimeOut :22807): RPC_evenOdds (:22813) in place of the 50 % HP loss and lifeGamble_hit (:22834-22839): Effects/evenOdds_hit at the hero's position and rotation (createEffect :9351-9361; EffectControl life 2, followPosition; plays its own Sounds/evenOdds); Yield 0.3 (:23100): standby at 0.7 s (:22879)",
        "cues": [
        [0, "fx", "lifeGamble_ring", {"cut": 0.7}],
        [0, "voice", "lifeGamble1|lifeGamble2"],
        [0.4, "fx", "evenOdds_hit"]
        ]
      },
      "skillGamble": {
        "why": "Cat.cs RPC_skillGamble (coroutine :23147-23655): at 0 addTimeOut agiAdjust(30) (:23472), clip gamble cut (:23481), Effects/skillGamble_ring at the hero's position and rotation (createEffect :23499-23511; EffectControl life 1, followPosition, followState: cut at standby 0.7 s; plays its own Sounds/gamble_ring), voice skillGamble1 / skillGamble2 (Random.Range(0, 2) :23554, :23564-23649; no voice timer); Yield 0.4 (:23630): the roll Random.Range(0, 100) < lckAdjust(50) (:23290) lost (a win multiplies MP / SP by 1.5, RPC_skillGamble_heal :23306), Even Odds #422 on and off cooldown (hasSkill(422) :23328, isTimeOut :23334): RPC_evenOdds (:23340) in place of halving MP / SP and skillGamble_hit (:23361-23371): Effects/evenOdds_hit at the hero's position and rotation (createEffect :9351-9361; EffectControl life 2, followPosition; plays its own Sounds/evenOdds); Yield 0.3 (:23636): standby at 0.7 s (:23411)",
        "cues": [
        [0, "fx", "skillGamble_ring", {"cut": 0.7}],
        [0, "voice", "skillGamble1|skillGamble2"],
        [0.4, "fx", "evenOdds_hit"]
        ]
      }
    }
  },
  "@NineLives:ko": {
    "why": "Cat.cs RPC_nineLives (:9634, coroutine :27238-27660), Nine Lives #264's proc (max rank: getNineLivesLv 2, :9591-9630; the tile plays the proc every play): when her HP is gone (Update, after autoLife :245-272 and the Small Anubi pet :291-303), Random.Range(0, 100) < lckAdjust(2 x 6) (:334) with no death status (:340) starts it (:346, ActionEvent :359) in place of RPC_dead (:367); at 0: hp 0, actionState dead (:27581-27584), Rewind + animation.Play(ko) (a cut, :27608), deadEffect (the Cat prefab's field, Effects/deadEffect) at her position and rotation (Instantiate :27614; EffectControl life 3); no voice (RPC_ko's ko1 / ko2 and RPC_dead's dead1 / dead2 are not played); Yield 3 (:27638): getUp",
    "cues": [
    [0, "fx", "deadEffect"]
    ]
  },
  "@NineLives:getUp": {
    "why": "Cat.cs RPC_nineLives case 2, 3 s after the ko: hp 99, ko refilled, actionState attack (:27365-27375), addTimeOut agiAdjust(60) (:27390, never read), noDamage 3 s (:27395; draws nothing, CharacterControl.cs:32931-32935), animation.Play(getUp) (a cut, :27400), voice Random.Range(0, 2) (:27441): BB asks for Voices/nineLives1 / nineLives2 (:27453, :27485), which BB's data lacks (the rip has ninelife1 / ninelife2: silent in BB); TTO's fix loads voices/ninelife1 / ninelife2 (pseudo/Cat.c:20332-20344; taken as the Bat's decision 18); Yield 1 (:27632): standby (:27529)",
    "cues": [
    [0, "voice", "ninelife1|ninelife2"]
    ]
  },
```
(the comma after the last `}` only if another entry follows; check with
`py -3 -c "import json; json.load(open('wardrobe/fx_cues/cat.json', encoding='utf-8'))"`)

Without the WorldParticleCollider part the Treasure Hunt cue still plays, but the coins fall through the floor; the part
must be built first (missing parts are always built), and Lucky Dice needs it anyway.

### 4. `pipeline/wardrobe_skill_icons.py`

```python
EFFECT_ONLY = {"sheep": ["quickHeal"], "penguin": ["manaArc", "dispell", "doubleCast", "tripleCast", "frostSpike"],
               "bat": ["massCast", "shadowGaze", "switch", "shadowSacrifice"],
               "cat": ["awareness", "damageRoulette", "treasureHunt"]}
OWN_TILE = {"sheep": {"sealOfAttack": ["cast3"], "sealOfDefense": ["cast3"], "edenSanctuary": ["cast3"]},
            "bat": {"nightmare": ["cast3", "channel"], "mindControl": ["cast3", "channel"]},
            "cat": {"evenOdds": ["gamble"], "nineLives": ["ko", "getUp"]}}
```
`best` finds `cat_awareness2`, `cat_damageRoulette2`, `cat_treasureHunt1`, `cat_evenOdds5` (the same bytes as the card's
`cat_evenOdds1`) and `cat_nineLives2`. Then `py -3 pipeline\wardrobe_skill_icons.py`. (`ko` / `getUp` are base clips:
moveSkillIcons runs only for skill moves, so the KO tiles keep their own icons.)

### 5. The part: WorldParticleCollider (for the parts stage)
- `pipeline/wardrobe_fx.py`: a branch for the built-in `WorldParticleCollider` (read_typetree: m_BounceFactor,
  m_CollisionEnergyLoss, m_CollidesWith.m_Bits, m_MinKillVelocity, m_SendCollisionMessage) into the node's comps, like the
  EllipsoidParticleEmitter branch; then add it to `wardrobe_fx_inventory.py`'s BUILT.
- The page's legacy particle system (the node with the EllipsoidParticleEmitter + ParticleAnimator): each frame, a live
  particle whose world y goes below the floor (y 0, the only Default-layer surface the page has) while moving down is put
  back on it with `v.y = -v.y x bounceFactor` (Unity's legacy collider also scales the speed along the surface by the
  bounce; take 1 there unless a closer reading of Unity 3.5 says otherwise), energy minus collisionEnergyLoss, killed below
  minKillVelocity. Both Cat users have bounce 0.5, loss 0, minKill 0, layer bit 0.

### 6. Build, then check

```
uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py cat --fx awareness2,insight,damageRoulette_ring,damageRoulette,treasureHunt,evenOdds_hit,lifeGamble_ring,skillGamble_ring,deadEffect --voices awareness1,awareness2,damageRoulette1,damageRoulette2,lifeGamble1,lifeGamble2,skillGamble1,skillGamble2,ninelife1,ninelife2
py -3 pipeline\wardrobe_skill_icons.py
uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py D:/12tails-wardrobe checks/fx_cat dark --cls cat
```
`damageRoulette` and `insight` are loaded from CharacterControl.cs (not Cat.cs), so the inventory does not list them; the
probe builds them from the Cat's effects folder and every part they use is built. The effects' own sounds come with them
(awareness, damageRoulette, evenOdds, gamble_ring).

## Coordination with the other Cat researchers
- **The gamble clip must be a pool** (`"gamble": {"skills": {"powerShuffle", "lifeGamble", "skillGamble"}}`, one tile each:
  the standing rule). If it stayed a plain clip, "Even Odds: gamble" would take it out of the skill tab: renderMovesUI drops
  every clip a sequence uses (`used`, index.html). `@EvenOdds:gamble` is never a pool host (it is an own key).
- **Life / Skill Gamble's lose branch:** with "passives on", a literal reading would turn every lost gamble into Even Odds.
  Recommended: the gamble tiles keep their own win / lose (Even Odds has a 90 s cooldown, so most losses are plain) and Even
  Odds shows on its own tile (Q4).
- The KO researcher's `ko` entry (deadEffect, voices) is not reached by the Nine Lives tile: `@NineLives:ko` is looked up
  first (fxStart), and `@NineLives:getUp` keeps a `getUp` / `revive` entry out of it.

## Open questions (each with my recommended answer)
1. **Awareness' voice with Insight learned:** BB plays awareness1 / awareness2 whatever is learned (:8717-8772); TTO plays
   inSight1 / inSight2 when #421 is learned (`pseudo/Cat.c` RPC_awareness :33631, hasSkill(0x1a5) ~:33841, loads
   ~:33928 / :33962; the files are in BB's rip, unused). Recommended: BB's awareness1|awareness2 (BB content; TTO changed
   behaviour rather than fixing a bug). Alternative cue: `[0, "voice", "inSight1|inSight2"]` (+ `--voices inSight1,inSight2`).
2. **Heights from the Cat's CharacterController** (height 1.6, centre 0.89: taller than the Penguin's 1 / 0.6): the roulette
   at 0.89 m, the Insight mark's root at 1.69 m (its sprite at 2.19 m). Recommended: the game's numbers; the QA shots judge
   whether the mark floats too high over the page's Cat (then `y` 1.3 or so, said in `why`).
3. **Treasure Hunt's tile:** recommended its own tile, the coin burst 1 m ahead with no box (its RPC carries the skill's
   name; the Frost Spike precedent of a passive's proc on the idle stance), after the WorldParticleCollider part. Alternative:
   no tile (it is a world interaction, open to any Cat, at a box the page does not have).
4. **Even Odds:** recommended its own tile on the gamble clip, the two hosts as a random pool (above). Alternatives: one host
   only (Skill Gamble, its prerequisite: `"@EvenOdds:gamble": {"why": ..., "cues": [...]}` with the skillGamble member's
   cues), or no tile and Even Odds folded into the gamble tiles' lose branch.
5. **Nine Lives' voice:** recommended TTO's fix `ninelife1|ninelife2` (BB asks for names its data lacks; the Bat's decision
   18). Alternative: silent, as BB plays it. And its tile at all: recommended yes (a skill with its own RPC, Bible card and
   icon; only base clips, so `ko@3 getUp` rather than root).
6. **Damage Roulette's step:** recommended `root*@10.2` (the whole cut buff, no stacking when the tile loops). Alternative
   `root*@1.2` (ring and voice; with looping on, the roulettes would stack).
7. **The camera screen warp** (`barrierMask`, Awareness): left out, as the Penguin's Dispell; a screen post effect would be a
   cross-class part (Penguin ringMask, Chameleon zoomMask, Whale ringMask / burstMask, Cat barrierMask).
8. **Hidden Blade / Jagged Knife and Backstab** (passives with RPCs of their own, drawn only at the target): recommended no
   tiles of their own; the nAttack / Forward Lunge / Reverse Thrust researchers decide them as phases. Note for them: at the
   standard target (rot [0, 180, 0], facing the hero) `Quaternion.Angle` between the two facings is 180°, so Hidden Blade's
   `< 45°` (`< 75°` with #433) and Forward Lunge's Backstab `< 45°` never pass, while Reverse Thrust's Backstab `> 135°`
   always does.
9. **The idle freeze in effect-only tiles:** a `root@t` step longer than the idle clip stops on its last frame
   (clampWhenFinished); recommended `root*@t` for the Cat (above) and the same change for the Penguin's / Bat's tiles in a
   later pass.

## Verification

Checker, 2026-11-13 (read only; scripts in `checks/fx_cat_research/verify/`: `keys.py` dumps a Cat.cs range's effect /
voice / yield / clip lines, `blocks.py` parses this report's JSON block and runs it through `wardrobe_fx_check.py`'s
KINDS / OPTS). Every line cited below was re-read in the source.

**RPC_* listing redone.** `grep -E "^\s*(public|private|internal|protected) [^(]*\bRPC_\w+\(" Cat.cs` = 84, the same 84
names and lines as the report; the five groups re-counted (31 + 24 + 17 + 7 + 5). `node pipeline/clip_calls.js
D:/12tails/DecompiledSource wardrobe/data cat` lists exactly the 31 clip RPCs (plus PlayerControl's walk). The only
clip calls inside the five "mine" RPCs are RPC_nineLives' `animation.Play("getUp")` :27400 and `("ko")` :27608 (none in
:8563-9120, :9335-9381, :26940-27237). The TTO comparison holds: `pseudo/Cat.c` "// ==== Cat::RPC_*" minus BB's =
RPC_anchorYank, RPC_crescentEclipse, RPC_dropAnchor, RPC_eclipseRupture, RPC_royalFlush (BB-only: the 12 supplement
skills, items / mount / coin / pet, emotes, activateIcon, ko / dead / revive).

**Confirmed** (times, positions, picks, ranks): Awareness :5912/:5918/:7846/:7855, :8574, :8591-8642 (identity),
:8668, :8674 (12 x sLv), :8706-8772, :8797, :8837, :8848-8854; insight at `mChar.bounds.center + 0.5 x mChar.height x
up`, identity, parented (CharacterControl.cs:36402-36431; mChar is the CharacterController, :29789 / :991; Cat.prefab
:835-841 height 1.6, radius 0.2, centre y 0.89, root scale 1): y 1.69. Damage Roulette :6165/:6171/:7582/:7595,
:27071-27209, status :27052 chaAdjust(12); CharacterControl.cs:36254-36273 (collider.bounds.center, Clamp(0.8, 1, 1.5)
= 1), removal :16223-16236 / insight :16256-16269; awareness status apply strips blend / invisible (:36204-36227);
noDamage draws nothing (:32931). Treasure Hunt: TreasureBox.cs :239-242 (`(int)Clamp(sqrMagnitude) <= 3`), :267-273,
:286-322, :334, :343, :349, :355, :369; Cat.cs :9091-9101 identity; WorldParticleCollider treasureHunt.prefab:176-187
(m_Bits 1 = layer 0, Default; bounce 0.5, loss 0, minKill 0), and the same on luckyDice.prefab:240-252 (the only
other Cat prefab with one; tormentRain_fire, millionaire1 / 2 elsewhere). Even Odds: :22768, :22801-22826, the jump
`goto Block_52` -> IL_1F7 = `Yield(3, 0.3)` (:23112-23113, :23099-23100) past :22834-22839; skill branch :23290,
:23328-23353, :23361-23384; RPC_evenOdds :9342-9361 (hero position and rotation); rings :22967-22979 / :23499-23511
(hero rotation); voices :23022-23102 / :23554-23649; standby :22879 / :23411. Probe: lifeGamble_ring / skillGamble_ring
life 1, followState true, emission 4 / 6; evenOdds_hit life 2, AudioSource evenOdds. Nine Lives: :334, :340, :346,
:359, :367; :27581-27614 (Rewind + Play(ko), wrapMode Once :27611, deadEffect at position + rotation); case 2 guarded by
`actionState == "dead"` (:27355), :27365-27400 (noDamage 3 s :27395), voices nineLives1 / 2 (:27453 / :27485; the rip
has only ninelife1 / ninelife2.wav; TTO pseudo/Cat.c:20332-20344 loads ninelife1 / 2); Yield(2, 3) :27638, Yield(3, 1)
:27632, standby :27529. TTO's Awareness inSight1 / 2 with 0x1a5 = 421 (pseudo/Cat.c:33631, :33841). Icons: assets.js
has cat_awareness2, cat_damageRoulette2, cat_treasureHunt1 (and a rank-less cat_treasureHunt: `best` takes 1),
cat_evenOdds5, cat_nineLives2.

**Page / tool claims confirmed:** the SEQ token regex `^(\w+)(\*)?([~^!])?(?:@([\d.]+))?$` (index.html:1259) takes
`root*@3`; a chain step without `*` is LoopOnce + clampWhenFinished whatever the clip's data loop flag (index.html:1365-1366;
`root` is `loop: true` in clips.json but `play()` sets mode "back" for a skill chain), so the `*` is needed for idle steps
longer than 0.8 s; fxStart looks up `@<id>:<clip>` first (index.html:4607), a pool without `pick` stays random
(:4609-4614), cue times restart per step (`FX.t = 0`, :4604); `cut` acts only on a followState root (:4016), `kill` on
age (:4010); poolChains skips `@` keys (:1279), so `@EvenOdds:gamble`'s members make no extra tiles, and
`wardrobe_skill_icons.py` likewise reads pools only from keys without `@`; `renderMovesUI`'s `used` drops a sequence's
clips only from the skill tab (index.html:3483-3485), so `root` / `ko` / `getUp` keep their base tiles;
`wardrobe_fx_check.py` seqs() strips `//` comments and parses the SEQ line, split_key resolves `@NineLives:ko`,
`@EvenOdds:gamble`; `blocks.py`: the six entries are valid JSON, times in order, every kind and option one the checker
accepts. `wardrobe_fx.py --fx ...` merges into fx.json (pipeline/wardrobe_fx.py:493-496), so the build line is safe.

**Corrections (none changes a cue):**
1. "The private `onSupport` :10886" -> `onSupport` is defined at Cat.cs:10869 (called :11227, :11590).
2. Nothing else: no time, position, pick, rank or buildability claim was wrong. (Q8's side note about Backstab angles
   was not re-derived; it is the other researchers' call.)

The paste-ready blocks 1-6 stand as written.
