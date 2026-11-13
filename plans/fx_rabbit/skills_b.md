Summary: 11 clips, 17 coroutines read (plus the create / hit helpers), 17 tiles, 14 cue keys (144 cues).
- **Pools:**
  - `mix3`: Mix, Shake, Miracle Blend (one tile each).
  - `mix4`: Sticky Gum, Acidic Field, Healing Field.
  - `medicalShot`: Immune Shot, Boost Shot, Heat Shot, Life Shot.
  - Truce Trading and Contract (clip `truceTrading`) are two sequences of their own, not a pool.
- **Sequences:**
  - The channel hosts must be renamed `Cast` / `Field Cast`. Today's `Mix` / `Sticky Gum` take the ids of the members `mix` / `stickyGum`, so poolChains would drop those two tiles.
  - New: `Truce Trading` (0.12 s bar, then cheer / cry for 2 s) and `Contract` (0.1 s bar, then bow with the Light Golem).
- **Parts to build:**
  - Cue options: a shared random yaw `yaw` (potions and stars), `sphere` and a per-axis `"random"` rot (Millionaire's coins), `replace` (one field of each kind).
  - The kind `propCopy` (Ten Shot's second gun) and HERO_SKINS `rapidTrance` (the purple tint).
  - `Rabbit_potion`'s layout and four data-only parts.
  - The Light Golem summon (layouts, the LightGolem2 swap, the Monkey's elementals.js).
- **In neither game:** `contract_ring` (BB's Resources and TTO's catalog both lack it), so Contract shows no ring.
- **Possible Bible findings:**
  - Ten Shot's volleys are 0.4-0.5 s apart.
  - The Medical Shots fire at 1.4 s (1.0 s and the gilShot clip under Rapid Trance), and their shot voice only plays in missions / arenas.
  - Rapid Trance tints the Rabbit and fixes the cast voices.
  - Healing Field borrows Shake's / Mix's voice.
  - Millionaire drops 18 coins.

---

# Rabbit effects + sounds research: skill clips, second half (skills_b)

Scope: the clips medicalShot, millionaire, mix1, mix2, mix3, mix4, rapidTrance, shootingArray, statScan, tenShot and truceTrading, and every skill that plays them (`pipeline/clip_calls.js`, `checks/fx_rabbit_research/skills_b/clip_calls.txt`). Research only (recipe steps 1-3).

- Line numbers are `C:\Users\Jump\Desktop\12tails\DecompiledSource\Rabbit.cs` (the home PC's `D:\12tails\...`) unless another file is named. `TTO1102:` = `DecompiledSource_TTO_2026-11-02/pseudo/Rabbit.c`.
- Times are seconds from the start of the clip the entry is keyed by (a SEQ step's own start). Distance 0 = at the hero.
- Max rank, passives on:
  - Mix 4 with Extra Potion #412, Shake 3, Miracle Blend with Miracle Drop #422.
  - Sticky Gum 2, Acidic Field 2 with #442, Healing Field.
  - Immune / Boost / Heat / Life Shot, rank 1 each (Medical Enhancement 3 changes only the allies' statuses).
  - Rapid Trance, Stat Scan, Truce Trading 2, Contract at level 3 (SP >= 65), Shooting Array 2, Millionaire 2, Ten Shot.
  - Where the code picks by rank: hpPot4, spPot3, the Light Golem.
- Stats:
  - High INT: every cast bar at magAdjust's 0.1 s floor (the SEQ rule, plans/fx_mole/decisions.md header).
  - LCK 1 for rolls (the Cat's gamble convention, plans/fx_cat/decisions.md 30).
  - CHA 1 for lifetimes.

Read-only probes, in `C:\work\12tails-wardrobe\checks\fx_rabbit_research\skills_b\` (git-ignored):
- `flow.py` (the Panda researcher's, unchanged): a coroutine with its junk predicates evaluated.
  - It wrote `RPC_<name>.flow.txt` for the 15 coroutines in scope, plus `RPC_mix_create`, `RPC_shake_create`, `RPC_miracleBlend_create`, `RPC_truceTrading2` and `RPC_millionaire_createPeppon`.
  - Where the flattened braces left a branch unclear, I read the raw lines and worked their predicates by hand (quoted below where it matters).
- `probe.json` / `probe_sum.txt` (`psum.py`): `wardrobe_fx.py rabbit --probe` on 44 names.
- `probe2.py` -> `probe2.json`: LAYOUTS `Rabbit` (the hero prefab's script) and `Rabbit_potion` added in memory. Every potion decodes (the self-check passes), and the hero field `castStar1` is the prefab `castStar` (path id 279).
- `probe3.py` -> `probe3.txt`: the Light Golem prefab's nodes, scripts (byte sizes), clips and materials.
- `probe4.py` -> `probe4.txt`: `EXTRA_FOLDERS` rabbit + LAYOUTS `LightGolem` / `LightGolemAI` added in memory. `effect()` builds the Light Golem and its self-check passes. The container lists the key twice (MonoScript, then GameObject), and `Game.container` keeps the GameObject.
- `tto_probe.json` / `.err`: `wardrobe_fx_tto.py rabbit --probe contract_ring,...`. TTO's catalog has no contract_ring.
- `pool.py` -> `pool.json` / `pool_pretty.txt`: the entries below. It checks:
  - valid JSON and cue times in order;
  - the kinds;
  - every key is a Rabbit skill clip or a `@Seq:clip` of a proposed SEQ.

## Read this first

1. **Pools and tiles (17).**

   | clip | played by | tiles |
   |---|---|---|
   | mix1, mix2 | RPC_cast1 (:20091), the channel of all six potion / field skills | none: hidden hosts |
   | mix3 | RPC_mix_cast :24141, RPC_shake_cast :25018, RPC_miracleBlend_cast :25932 | Mix, Shake, Miracle Blend |
   | mix4 | RPC_stickyGum_cast :26841, RPC_acidicField_cast :27343, RPC_healingField_cast :37941 | Sticky Gum, Acidic Field, Healing Field |
   | medicalShot | RPC_medicalShot :28612 with sLv 1-4 | Immune Shot, Boost Shot, Heat Shot, Life Shot |
   | truceTrading | RPC_truceTrading1 :34233, RPC_contract :40631 | Truce Trading, Contract (own SEQs) |
   | rapidTrance, statScan, shootingArray, millionaire, tenShot | one coroutine each | one tile each |

2. **The channel and its two hosts.**
   - RPC_cast1:
     - At 0: `mix1` cut in, voice cast1 / cast2.
     - At 0.6: `mix2` looped (cut in) and the cast bar.
     - The release comes when the bar ends (:20598).
     - The six bars are magAdjust(4 | 4 | 5 | 3 | 3 | 5) = 0.1 s at high INT.
   - Replace the page's `"Mix: mix1 mix2*@0 mix3~"` and `"Sticky Gum: mix1 mix2*@0 mix4~"` with `"Cast: mix1@0.6 mix2*@0.1 mix3~"` and `"Field Cast: mix1@0.6 mix2*@0.1 mix4~"`.
     - Why: poolChains skips a member whose id is already taken (`taken`). The hosts `Mix` / `Sticky Gum` hold `@Mix` / `@StickyGum`, the members' own ids. The hosts are hidden anyway.
     - mix1 keeps the page's first-step fade (every class's convention).
     - mix3 and mix4 have a 0.2 s fade in the game (`~`).

3. **Truce Trading and Contract are sequences, not a pool.**
   - `"Truce Trading: truceTrading*@0.12 cheer*~@2|cry*~@2"`:
     - The 12 s bar is 0.1 s, checked every FixedUpdate, so the roll comes at 0.12 s.
     - Then RPC_truceTrading2 plays the emote `cheer` (the trade made) or `cry` (refused) for 2 s (question 1).
   - `"Contract: truceTrading*@0.1 bow~@1.2"`:
     - The bar magAdjust(3 + 3 level) is 0.1 s, checked every frame.
     - At 0.1 s come the summon, the voice and `bow` (0.2 s fade); the standby follows 1.2 s later.
   - Cue keys: `@TruceTrading:truceTrading / :cheer / :cry` and `@Contract:truceTrading / :bow`. There is no plain `truceTrading` entry, so poolChains makes nothing of the clip.

4. **Parts to build** (paste-ready text in "Page changes"):
   - **P1 `yaw`:** RPC_cast1 draws one Random.Range(0, 360) per cast (:20286) and turns every star and bottle by it. A per-cue `"randomYaw"` would break the ring of bottles.
   - **P2 `sphere` and `"random"` in a rot list:** Millionaire's coins land at hero + vFlat(2 x Random.onUnitSphere), turned Euler(270, Random.Range(0, 360), 0) (:37485).
   - **P3 `replace`:** each RPC_*_create Destroys the hero's previous field of that kind (:10057-10063, :10131-10137, :11307-11313).
   - **P4 kind `propCopy`:** Ten Shot puts a copy of the worn main-hand gun on mountHand_L from 0.2 to 2.8 s (:38901-38922, :38975-38981).
   - **P5 HERO_SKINS `rapidTrance`:** the status sets the hero's colour to (0.48, 0.43, 0.78) (CharacterControl.cs:37520-37523).
   - **P6 potions and fields:**
     - `LAYOUTS["Rabbit_potion"] = [("potionType", "i")]` (Rabbit_potion.cs:528; probe2 proves it).
     - Data-only parts `api.part(type, () => null)` for Rabbit_potion, Rabbit_stickyGum, Rabbit_acidicField and Rabbit_healingField, in a new fxparts/rabbit.js. Their Update only times out and finds targets.
     - Add all four to wardrobe_fx_inventory.py BUILT.
   - **P7 the Light Golem:**
     - `EXTRA_FOLDERS["rabbit"] = ["gameassets/characters/elementals/lightgolem"]`.
     - `LAYOUTS["LightGolem"]` (5 refs, 40 B) and `LAYOUTS["LightGolemAI"] = [("AI_state", "s")]` (probe4 proves them).
     - Export the material `LightGolem2` and swap it onto `CrystalBug_tri`. LightGolem.Start does that for a summon on the owner's layer (LightGolem.cs:58-80).
     - It is played by the Monkey's planned fxparts/elementals.js (plans/fx_monkey/parts.md part 9), registered for `LightGolem`. It has no `summon` clip, so `root` loops from the spawn.
   - **Ready:** everything else.
     - Every other cued effect is `ready` in plans/fx_inventory.md, castStar included (built by its Resources name).
     - Existing options cover the rest: `bone` the flags and the Rapid Trance bottle; `skin` the tint; `p` / `roll` / `"!roll"` the golden bottle; `"randomYaw"` the Shooting Array hits.

5. **Where things land** (standing rules, by analogy):
   - **Fields:** on the floor 2 m ahead; fields and the summon are cut at 10 s.
   - **Medical Shots** aim at an ally at the 10 m point (Sheep decisions 1, 4; the Panda's Sp Transfer).
     - The shot leaves 1 m up, 2.29 deg down.
     - The ray meets the standard body (Bat decisions 3-4: centre 0.6 m up, height 1, radius 0.3) at (0, 0.612, 9.7), where the skill's own effect is drawn.
   - **Stat Scan** sits on the target at ClosestPointOnBounds(hero + 1.5 up) = (0, 1.1, 9.7).
   - **Shooting Array:**
     - Its three hits land at the target's feet (0, 0, 10), each with a random yaw.
     - The finisher lands at the body centre (0, 0.6, 10).
     - The 6 m pulses draw nothing.
   - **Ten Shot:** only the last volley's two 0-deg cones hold the 10 m target, so two nAttack_hit at (0, 1, 9.7) at 2.5 s. The Bible's table agrees (2 hits at 0-10 deg).
   - **Millionaire:** its 8 m pulses miss the target.
   - **No travel** (Bison decision 17): the fields' 5 m/s for 0.1 s and the Medical Shot's -1 m/s are left out.

6. **Rapid Trance's side effects stay off.** With the status on:
   - the cast skills always pick voice 1, and Healing Field always mix2;
   - a Medical Shot plays `gilShot` and fires at 1.0 s (:28548-28552, :27617-27623, :28730).

   A new pick clears the tint, so no status carries into another tile. Every entry is the status-off branch.

7. **TTO.** None of these clips is in tto_released.json (rabbit: bountyHunt, coinRicochet, medicTurret, clap, wai: the TTO report's). Each coroutine has a TTO twin playing the same clip (pseudo/Rabbit.c):

   | coroutine(s) | TTO1102 |
   |---|---|
   | cast1 | :5019 (mix2 :5063, mix1 :5068) |
   | mix_cast / shake_cast / miracleBlend_cast | :16481 (mix3 :16560) / :19071 (:19149) / :15456 (:15537) |
   | stickyGum_cast / acidicField_cast / healingField_cast | :22324 (mix4 :22385) / :803 (:857) / :11192 (:11246) |
   | medicalShot | :13318 (medicalShot :13410, gilShot :13403) |
   | rapidTrance / statScan | :18528 (:18577) / :21586 (:21651) |
   | truceTrading1 / truceTrading2 / contract | :23889 (:23949) / :24488 (cheer :24526, cry :24534) / :6709 (:6764, bow :6759) |
   | shootingArray / millionaire / tenShot | :19866 (:19931) / :14719 (:14787) / :22784 (:22871) |

   TTO also asks for contract_ring (:6755) and logs it missing (:6765). BB is the authority for the cues.

## Per clip

Format: the RPC (file:line), then the timeline.
- **fx** = an effect (where / rotation).
- **voice** = a Voices/ clip.

Effects' own AudioSources play with them, so there are no "sound" cues in scope. The JSON `why`s carry every citation.

### mix1 / mix2 (the channel, RPC_cast1 :20091-20866; mix1 0.633 s, mix2 0.6 s)

| time | what | lines |
|---|---|---|
| 0 | mix1 cut in; voice cast1 \| cast2 | :20455, :20506-20550 |
| 0.6 | mix2 looped, cut in; the bar magAdjust(..) = 0.1 s; the random angle R | Yield 0.6 :20809; :20259-20286, :20420 |
| 0.7 | release (the mix3 / mix4 coroutine) | :20598, :20617-20751 |

- There is no effect.
- The cast times are (:20303-20414):
  - Mix 2 + 0.5 sLv = 4; Shake 2.5 + 0.5 sLv = 4; Miracle Blend 5;
  - Sticky Gum / Acidic Field 1 + sLv = 3; Healing Field 5.
- All are 0.1 s for INT >= 160: `nCastTime - mag / 32`, with a floor of 0.1 (CharacterControl.cs:20584-20589).

### mix3 (pool: Mix, Shake, Miracle Blend; clip 1.0 s)

All three:

| time | what |
|---|---|
| 0 | mix3, 0.2 s fade |
| 0.3 | cast_ring at the hero (identity; followPosition, life 2, Sounds/cast2) |
| 0.3 | n castStar at the hero, LookRotation(tDir) x Euler(0, a i, 0) |
| 0.3 | the voice |
| 0.7 | each bottle's create coroutine (Yield 0.4): castLight and the bottle at hero + rotateH(1.5 tDir, a i), identity |
| 0.8 | standby |

- **The angle:** tDir = rotateH(forward, R) (:20286): option P1 `"yaw": "cast"`.
- **Bottle spots:** rotateH(+a) turns left (Math.cs:838-843), so bottle i sits at x = -1.5 sin(a i), d = 1.5 cos(a i).
- **The voice:** `Random.Range(0, 2) != 0` and no rapidTrance -> voice 2, else voice 1 (:23995-24047). The predicates: 179036 - 486440 = -307404, so `!=` is false and does not skip; 11462 - 286488 = -275026 likewise.
- **The bottles:** Rabbit_potion, Init(chaAdjust(60)), so `kill 10`.
  - They are picked up only by touch: a 0.6 x 1 x 0.6 trigger box (rip hpPot4.prefab), 1.5 m from the hero.
  - They stack across plays, as in the game: the list f0RExLx3gG has no cap (:24525, :9765).

| member | n, a | bottle | voice | coroutine lines |
|---|---|---|---|---|
| mix (Mix 4, #412 on) | 5, 72 deg | hpPot4 (switch sLv :24360-24504) | mix1 \| mix2 | :23702-24225, create :24226-24605 |
| shake (Shake 3) | 3, 120 deg | spPot3 (:25231-25336) | shake1 \| shake2 | :24606-25096, :25097-25434 |
| miracleBlend (#422 on) | 4, 90 deg | randomPot6 at p 0.05 (lckAdjust(5) at LCK 1, :25636-25642), else randomPot1-5 even (:25650) | miracleBlend1 \| miracleBlend2 | :25435-26023, :26024-26421 |

Bottle spots (x, d):
- Mix: (0, 1.5), (-1.4266, 0.4635), (-0.8817, -1.2135), (0.8817, -1.2135), (1.4266, 0.4635).
- Shake: (0, 1.5), (-1.299, -0.75), (1.299, -0.75).
- Miracle Blend: (0, 1.5), (-1.5, 0), (0, -1.5), (1.5, 0).

Each star's rot is [0, a i, 0].

### mix4 (pool: Sticky Gum, Acidic Field, Healing Field; clip 1.2 s)

| member | 0 | 0.4 | 0.5 | 0.8 |
|---|---|---|---|---|
| stickyGum (2) :26422-26933 | mix4, 0.2 fade (:26841) | moveSpeed 5 (left out) | stickyGum 2 m ahead on the floor, scale (2.5, 1, 2.5) (:10069-10072); voice stickyGum1 \| 2 | standby (:26788) |
| acidicField (2) :26934-27427 | mix4 (:27343) | moveSpeed 5 | acidicField (LookRotation(forward)) + acidicField_fire (identity), 2 m ahead (:10143, :10172-10178); voice acidicField1 \| 2 | standby (:27290) |
| healingField :37541-38029 | mix4 (:37941) | moveSpeed 5; voice shake2 \| mix2 (:37712-37764) | healingField + healingField_fire, 2 m ahead (:11282-11365) | standby (:37888) |

- **The waits:** Yield 0.4 / 0.1 / 0.3 (e.g. :26888, :26868, :26878).
- **The fields** have no EffectControl. Their scripts time out after chaAdjust(12) s and draw nothing, so `kill 10`.
- **One at a time:** the next cast of the same field Destroys the old one (P3 `replace`).

### medicalShot (pool: Immune / Boost / Heat / Life Shot; clip 2.1 s)

RPC_medicalShot :27428-28845, sLv 1-4 = the skill:

| time | what | lines |
|---|---|---|
| 0 | medicalShot, 0.2 fade; voice medicalShot1 \| medicalShot2 | :28612, :28644-28685 |
| 0.3 | medicalShot_ring at the hero (followPosition + followState, life 1 + 1) | Yield 0.3 :28735; :27591-27603 |
| 0.3-1.4 | the hero turns to the ally every FixedUpdate | :27728-27756, :28726 |
| 1.4 | medicalShot_fire at hero + 1 up, FromToRotation(forward, ally centre - firePos) = [2.29, 0, 0] | :27734, :27788-27833 |
| 1.4 | voice `<skill>1 \| <skill>2` (missions / arenas only; kept) | :27847-28152 |
| 1.4 | the raycast hits the ally: the skill's own effect (immuneShot / boostShot / heatShot / lifeShot) at (0, 0.612, 9.7), no turn | :28183-28417; :10209-10361 |
| 1.6 | moveSpeed 0 | Yield 0.2 :28733 |
| 1.7 | standby: the ring's cut | Yield 0.1 :28749; :27676 |

- **The 1.4 s branch:** 274159 - 481546 = -207387, so the `== -207386` test is false and no `continue` happens: the code falls through to the fire.
- **The voice gate** is pvoice, then mGameType > 4, then mTeam == layer - 7, with no isMine branch. The predicates (129056 - 176021 = -46965, 166064 - 536590 = -370526, 297876 - 509419 = -211543) skip nothing.

### rapidTrance (Rapid Trance; clip 1.5 s), RPC_rapidTrance :28846-29386

| time | what | lines |
|---|---|---|
| 0 | clip, 0.2 fade; voice rapidTrance1 \| 2 | :29199, :29240-29281 |
| 0.3 | rapidTrance_potion on mountHand_L, local zero (EffectControl life 1: gone at 1.3) | Yield 0.3 :29316; :28987-29019 |
| 0.9 | rapidTrance_ring at the hero, identity (followPosition, life 1 + 1) | Yield 0.6 :29340; :29062-29074 |
| 1.1 | status rapidTrance chaAdjust(12): the purple tint (P5), cut at 10 s | Yield 0.2 :29326; :29119; CharacterControl.cs:37520 |
| 1.3 | standby | Yield 0.2 :29347; :29146 |

### statScan (Stat Scan; clip 1.0 s), RPC_statScan :22333-22948

- 0: the clip cut in (:22755); voice statScan1 | 2 (:22799-22840).
- 0.2 (Yield 0.2 :22883):
  - statScan, made by the target's createEffect, at (0, 1.1, 9.7), identity (faceCamera, life 1 + 0.3) (:22506-22524);
  - statScan_dust at the hero, hero rotation (:22545-22557).
- 0.7: the stats as three chat lines (:22610-22675): text, left out.
- 0.8: standby (:22702).

### truceTrading (Truce Trading and Contract, two sequences; clip 1.0 s, looped)

- **Truce Trading** (RPC_truceTrading1 :33896-34514, then RPC_truceTrading2 :34515-35019):
  - 0: the clip looped; voice truceTrading1 | 2; truceTrading_ring (followState, life 12); truceTrading_flag on mountHand_L.
  - 0.12: the roll, LCK x 2 > Random.Range(0, target.hp) (:34111). It sends RPC_truceTrading_fire with the target, or with 0.
    - The owner's loop waits for the echo (isTrade :34145), so the event reaches the sender too.
    - myCommand changes, which ends the loop and the flag (:34205) and the ring (followState also tests myCommand, EffectControl.cs:226-232).
  - The 2 s outcome step (:34983):
    - `cheer` + truceTrading_success + voice tradeSuccess (:34739-34816);
    - or `cry` + truceTrading_fail + voice tradeFail (:34843-34920).
- **Contract** (RPC_contract :40147-40822):
  - 0: the clip looped; contract_ring asked for but missing; contract_flag on mountHand_L.
  - 0.1: level 3 (:7607-7619):
    - the LightGolem on the floor 3 m ahead, facing forward (:40464, :11596-11611; Math.cs:1210-1224), with contract_create there (:11707);
    - voice contract1 | 2 (:40512-40555);
    - bow, 0.2 fade (:40580).
  - 1.3: the flag Destroyed and standby (:40277-40306, Yield 1.2 :40765).

### shootingArray (Shooting Array 2; clip 2.2 s), RPC_shootingArray :35020-36052; tPos = the target's position (:35754)

| time | what | lines |
|---|---|---|
| 0 | clip, 0.2 fade; shootingArray_ring (followState, life 1 + 1); voice shootingArray1 \| 2 | :35775-35805, :35848-35889 |
| 0.5 / 0.6 / 0.7 | shootingArray_fire at TD(0, 0.8, 1), forward; shootingArray_hit at the target's feet, Euler(0, rand, 0) | :35196 / :35277 / :35374; :35216 / :35291 / :35388; :10974 |
| 0.6, 0.8, 1.0 | damage pulses (6 m around tPos), no look | :35308, :35436, :35504 |
| 1.2 | shootingArray_fire at TD(-0.15, 0.7, 0.25) | :35572 |
| 1.3 | shootingArray_finalhit at the target's centre (0, 0.6, 10) | :35607-35656, :11017 |
| 1.8 | standby: the ring's cut | :35942, :35693 |

### millionaire (Millionaire 2; clip 4.3 s), RPC_millionaire :36589-37342

- 0: the clip; millionaire_ring (followState, life 5 + 1); voice millionaire1 | 2.
- From 0.5 s:
  - **Coins:** 18 millionaire_peppon, one every 0.15 s (0.5 ... 3.05), at hero + vFlat(2 x onUnitSphere), Euler(270, rand, 0) (:37343-37540): P2.
  - **Bursts:** six of them, millionaire1 (i even) / millionaire2 (i odd), at 0.5, 1.0, 1.7, 2.2, 2.9, 3.4.
    - The waits are 0.5 after an even burst (:37275) and 0.7 - 0.1 x div(i, 5) after an odd one (:37266), so the last is 0.6.
    - Each wait ends in an 8 m pulse that misses the target.
- 4.0: standby (:37035, :37058).

### tenShot (Ten Shot; clip 3.0 s), RPC_tenShot :38760-39710

- 0: the clip; tenShot_ring (followState, life 3); voice tenShot1 | 2.
- 0.2: the copy of the worn gun on mountHand_L (P4). A counter i starts at 0 and adds 1 every 0.1 s (:39629, :38952).
- Volleys at i = 6, 11, 15, 19, 23 (0.8, 1.3, 1.7, 2.1, 2.5 s), two tenShot_fire each (:39449 / :39454):

  | time | left (x, y, d; yaw) | right |
  |---|---|---|
  | 0.8 | (-0.6, 0.5, 0.75); -45 | (0.6, 0.5, 0.75); 45 |
  | 1.3 | (-0.4, 0.6, -0.5); 135 | (0.5, 0.6, -0.5); -135 |
  | 1.7 | (-1.2, 0.75, 0.1); -90 | (1, 0.75, 0.1); 90 |
  | 2.1 | (-0.3, 0.9, -0.7); 180 | (0.2, 0.8, -0.7); 180 |
  | 2.5 | (-0.3, 0.9, 1); 0 | (0.1, 0.85, 1); 0 |

- 2.5: two nAttack_hit at (0, 1, 9.7).
- 2.6: i >= 24 (:39238).
- 2.8: the copy Destroyed and standby (:38975-39004).

## Effects at a glance

- **Ready:** cast_ring, castStar, castLight, acidicField_fire, healingField_fire, medicalShot_ring, medicalShot_fire, immuneShot, boostShot, heatShot, lifeShot, rapidTrance_potion, rapidTrance_ring, statScan, statScan_dust, truceTrading_ring, truceTrading_flag, truceTrading_success, truceTrading_fail, contract_flag, contract_create, shootingArray_ring / _fire / _hit / _finalhit, millionaire_ring, millionaire1, millionaire2, millionaire_peppon, tenShot_ring, tenShot_fire, nAttack_hit.
- **Need a part:**

  | effect | part |
  |---|---|
  | hpPot4, spPot3, randomPot1-6 | P6 (layout + data-only part) |
  | stickyGum, acidicField, healingField | P6 (data-only parts) |
  | LightGolem | P7 |

- **Cue options and kinds to build:** P1-P5.
- **Not cued:**
  - contract_ring: in neither game.
  - The allies' statuses, the trade itself, Stat Scan's chat text.
  - The motion blurs (Medical Shot, Millionaire).
  - gilShot: only under Rapid Trance.
- **Sounds:**
  - All 39 voices named are in the rip's rabbit/voices.
  - Every effect sound is in rabbit/sounds: acid1, acid2, cast2, healingField, medicalShot_ring / _fire / _hit, rapidTrance_ring, statScan, stickyGum, truceTrading, truceTrading_success / _fail, shootingArray_ring / _hit, millionaire, tenShot_ring and fourShot_fire.

## Page changes (paste-ready)

1. **SEQ** `rabbit` (Charge Attack / Bounce / Mall are the other reports'):
```js
  rabbit: ["Charge Attack: cAttack1 cAttack2* cAttack3", "Cast: mix1@0.6 mix2*@0.1 mix3~", "Field Cast: mix1@0.6 mix2*@0.1 mix4~",
    "Bounce: bounce1 bounce2", "Mall: mall1* mall2*", "Truce Trading: truceTrading*@0.12 cheer*~@2|cry*~@2",
    "Contract: truceTrading*@0.1 bow~@1.2"],
```
2. **SEQ_SKILL:** `rabbit: { "@TruceTrading": "truceTrading", "@Contract": "contract" }`.
3. **wardrobe_skill_icons.py:**
   - CLIP_SKILLS: `"rabbit": {"mix3": ["mix", "shake", "miracleBlend"], "mix4": ["stickyGum", "acidicField", "healingField"], "medicalShot": ["immuneShot", "boostShot", "heatShot", "lifeShot"]}`.
   - OWN_TILE: `"rabbit": {"contract": ["truceTrading", "bow"]}`.
   - The Bible has every key: rabbit_shake4, miracleBlend4, stickyGum4, acidicField4, healingField5, immuneShot1, boostShot2, heatShot3, lifeShot4, contract5.
4. **P1 `yaw`** (cueOf). `FX.yaws = {}` is reset where `FX.rolls` is (step 0):
```js
  if (o.yaw) {   // RPC_cast1's random angle (Rabbit.cs:20286): one Random.Range(0, 360) per play per name; rotateH turns left
    const deg = (FX.yaws[o.yaw] ??= randInt(0, 359)), R = deg * Math.PI / 180, x = q.x, d = q.d;
    q.x = x * Math.cos(R) - d * Math.sin(R); q.d = d * Math.cos(R) + x * Math.sin(R);
    if (Array.isArray(q.rot)) q.rot = [q.rot[0], q.rot[1] - deg, q.rot[2]];   // LookRotation(rotateH(fwd, R)) = yaw -R
  }
```
5. **P2:**
   - rotOf: `Array.isArray(r) ? r.map(v => v === "random" ? randInt(0, 359) : v) : ...`.
   - cueOf: `if (o.sphere) { const u = 2 * Math.random() - 1, a = 2 * Math.PI * Math.random(), s = Math.sqrt(1 - u * u); q.x += o.sphere * s * Math.cos(a); q.d += o.sphere * s * Math.sin(a); }`. This is the x-z of a uniform point on the sphere: vFlat(r x Random.onUnitSphere).
6. **P3 `replace: true`:** at the spawn, dispose any living Fx of the same name from an earlier play first (Destroy-then-Instantiate).
7. **P4 kind `propCopy`:** `[t, "propCopy", slot, {"bone", "kill"}]`.
   - A copy of `api.propModel(slot)` (its weapon_fx along), parented to that bone, local zero / identity.
   - It is the same size as the worn one: Unity's parent setter keeps the prefab's world scale, as for the original (RabbitEquipment.cs:929).
   - It is removed at kill, on a new pick or on a class change; nothing happens when the slot is empty.
8. **P5:** `"rapidTrance": () => ({ grow: 1, tint: [0.48 / 0.86, 0.43 / 0.86, 0.78 / 0.86] }),` in HERO_SKINS (the Bison's setColor rule).
9. **P6 / P7** (wardrobe_fx.py):
```python
    "Rabbit_potion": [("potionType", "i")],                                    # Rabbit_potion.cs:528 (4 bytes, probe2)
    "LightGolem": [(n, "r") for n in ("mChar", "LightGolem2", "LightGolemIcon2", "nAttack_hit", "nAttack_hitFx")],  # LightGolem.cs:1144-1159
    "LightGolemAI": [("AI_state", "s")],                                       # LightGolemAI.cs:1462
EXTRA_FOLDERS["rabbit"] = ["gameassets/characters/elementals/lightgolem"]      # Contract's summon (Rabbit.cs:11596)
```
   Also:
   - fxparts/rabbit.js: `for (const t of ["Rabbit_potion", "Rabbit_stickyGum", "Rabbit_acidicField", "Rabbit_healingField"]) api.part(t, () => null);`
   - elementals.js registers `LightGolem`, with root looped and the LightGolem2 swap on CrystalBug_tri.
10. **wardrobe_fx_check.py:** OPTS gains `yaw`, `sphere` and `replace`; KINDS gains `propCopy`. Check that its rot test accepts `"random"` inside a list. After any edit of wardrobe/index.html, `grep -c $'\r$'` must print 0.

## Paste-ready cue entries for wardrobe/fx_cues/rabbit.json

These are 14 keys, from `C:\work\12tails-wardrobe\checks\fx_rabbit_research\skills_b\pool_pretty.txt`, checked by pool.py. Put them inside the file's `{}` beside the other reports' keys.

```json
{
"mix1": {
  "why": "Rabbit.cs RPC_cast1 (:20091-20866), the channel every Mix / Shake / Miracle Blend / Sticky Gum / Acidic Field / Healing Field cast opens with (pipeline/clip_calls.js): mix1 cut in (PlayAnimation(\"mix1\", 0) :20455, Once :20460) and voice cast1 / cast2 (Random.Range(0, 2) :20506, loads :20518 / :20550, PlayOneShot :20804 / :20782) at 0; no effect; Yield 0.6 (:20809): mix2 looped, cut in (:20259-20264), the cast bar from 0.6 s (castTime :20269, DisplayCastBar :20280) of magAdjust(2 + 0.5 sLv | 2.5 + 0.5 sLv | 5 | 1 + sLv | 1 + sLv | 5) (:20303-20420) = 0.1 s at high INT (magAdjust's floor, CharacterControl.cs:20584-20589; the SEQ rule, plans/fx_mole/decisions.md header), then the release coroutine (Time.time >= castTime :20598, :20617-20751) with mix3 / mix4: SEQ \"Cast: mix1@0.6 mix2*@0.1 mix3~\" / \"Field Cast: mix1@0.6 mix2*@0.1 mix4~\" (the hidden hosts of the two pools)",
  "cues": [
    [0, "voice", "cast1|cast2"]
  ]
},
"mix3": {
  "why": "The mix3 clip: Mix (RPC_mix_cast, PlayAnimation(\"mix3\", 0.2) Rabbit.cs:24141), Shake (RPC_shake_cast :25018) and Miracle Blend (RPC_miracleBlend_cast :25932), one per play, even chance (one tile each, poolChains; host SEQ \"Cast\"), each released 0.7 s into the channel (mix1 entry); all three: Yield 0.3, cast_ring createEffect at the hero, Quaternion.identity (followPosition, life 2, its own Sounds/cast2), the stars castStar1 (= the prefab castStar, the hero prefab's field, checks/fx_rabbit_research/skills_b/probe2.json) at the hero with LookRotation(tDir) x Euler(0, a i, 0), the bottles 1.5 m out at rotateH(1.5 tDir, a i), tDir = RPC_cast1's random angle rotateH(forward, Random.Range(0, 360)) (:20286): the shared option yaw \"cast\"; each bottle's create coroutine waits 0.4 s, then castLight at the bottle, identity, and the bottle, identity, Rabbit_potion Init chaAdjust(60) (data only; picked up only by touch: its 0.6 m trigger box is 1.5 m from the hero, rip hpPot4.prefab): kill 10; voice at 0.3 (Random.Range(0, 2) != 0 and no rapidTrance status -> voice 2, else voice 1: rapidTrance is off on the page, so an even pick); Yield 0.5: standby 0.8 s",
  "skills": {
    "mix": {
      "why": "Rabbit.cs RPC_mix_cast (:23702-24225), Mix 4 (max rank: hpPot<sLv> = hpPot4, RPC_mix_create switch :24360-24504) with Extra Potion #412 on (hasSkill(412) :23891: 5 bottles 72 deg apart, else 3 at 120, :23881-23902): clip mix3, 0.2 s fade (:24141); Yield 0.3 (:24177): cast_ring (:23855-23867), the loop i < 5 (:23913): castStar1 (:23920), RPC_mix_create(hero + rotateH(1.5 tDir, 72 i)) (:23925-23936); voice mix1 / mix2 (Random.Range(0, 2) != 0 :23995, rapidTrance check :24001, loads :24047 / :24016, PlayOneShot :24179 / :24173); RPC_mix_create (:24226-24605): Yield 0.4 (:24559), castLight (:24354), hpPot4 Instantiated, identity (:24492-24504), Init(chaAdjust(60)) (:24535): at 0.7 s; Yield 0.5 (:24165): standby 0.8 s (:24091)",
      "cues": [
        [0.3, "fx", "cast_ring"],
        [0.3, "fx", "castStar", {"rot": [0, 0, 0], "yaw": "cast"}],
        [0.3, "fx", "castStar", {"rot": [0, 72, 0], "yaw": "cast"}],
        [0.3, "fx", "castStar", {"rot": [0, 144, 0], "yaw": "cast"}],
        [0.3, "fx", "castStar", {"rot": [0, 216, 0], "yaw": "cast"}],
        [0.3, "fx", "castStar", {"rot": [0, 288, 0], "yaw": "cast"}],
        [0.3, "voice", "mix1|mix2"],
        [0.7, "fx", "castLight", {"x": 0.0, "d": 1.5, "yaw": "cast"}],
        [0.7, "fx", "hpPot4", {"x": 0.0, "d": 1.5, "yaw": "cast", "kill": 10}],
        [0.7, "fx", "castLight", {"x": -1.4266, "d": 0.4635, "yaw": "cast"}],
        [0.7, "fx", "hpPot4", {"x": -1.4266, "d": 0.4635, "yaw": "cast", "kill": 10}],
        [0.7, "fx", "castLight", {"x": -0.8817, "d": -1.2135, "yaw": "cast"}],
        [0.7, "fx", "hpPot4", {"x": -0.8817, "d": -1.2135, "yaw": "cast", "kill": 10}],
        [0.7, "fx", "castLight", {"x": 0.8817, "d": -1.2135, "yaw": "cast"}],
        [0.7, "fx", "hpPot4", {"x": 0.8817, "d": -1.2135, "yaw": "cast", "kill": 10}],
        [0.7, "fx", "castLight", {"x": 1.4266, "d": 0.4635, "yaw": "cast"}],
        [0.7, "fx", "hpPot4", {"x": 1.4266, "d": 0.4635, "yaw": "cast", "kill": 10}]
      ]
    },
    "shake": {
      "why": "Rabbit.cs RPC_shake_cast (:24606-25096), Shake 3 (max rank: spPot<sLv> = spPot3, RPC_shake_create :25231-25336): clip mix3, 0.2 s fade (:25018); Yield 0.3 (:25048): cast_ring (:24759-24771), 3 bottles 120 deg apart (i < 3 :24790): castStar1 (:24797), RPC_shake_create(hero + rotateH(1.5 tDir, 120 i)) (:24802-24813); voice shake1 / shake2 (Random.Range(0, 2) != 0 :24872, rapidTrance :24878, loads :24924 / :24893, PlayOneShot :25045 / :25042); RPC_shake_create: Yield 0.4 (:25392), castLight (:25225), spPot3, identity (:25324-25336), Init(chaAdjust(60)) (:25367): at 0.7 s; Yield 0.5 (:25053): standby 0.8 s (:24968)",
      "cues": [
        [0.3, "fx", "cast_ring"],
        [0.3, "fx", "castStar", {"rot": [0, 0, 0], "yaw": "cast"}],
        [0.3, "fx", "castStar", {"rot": [0, 120, 0], "yaw": "cast"}],
        [0.3, "fx", "castStar", {"rot": [0, 240, 0], "yaw": "cast"}],
        [0.3, "voice", "shake1|shake2"],
        [0.7, "fx", "castLight", {"x": 0.0, "d": 1.5, "yaw": "cast"}],
        [0.7, "fx", "spPot3", {"x": 0.0, "d": 1.5, "yaw": "cast", "kill": 10}],
        [0.7, "fx", "castLight", {"x": -1.299, "d": -0.75, "yaw": "cast"}],
        [0.7, "fx", "spPot3", {"x": -1.299, "d": -0.75, "yaw": "cast", "kill": 10}],
        [0.7, "fx", "castLight", {"x": 1.299, "d": -0.75, "yaw": "cast"}],
        [0.7, "fx", "spPot3", {"x": 1.299, "d": -0.75, "yaw": "cast", "kill": 10}]
      ]
    },
    "miracleBlend": {
      "why": "Rabbit.cs RPC_miracleBlend_cast (:25435-26023), Miracle Blend with Miracle Drop #422 on (hasSkill(422) :25603: 4 bottles 90 deg apart, :25614-25683; else 3 of types 1-4, :25693-25747): clip mix3, 0.2 s fade (:25932); Yield 0.3 (:25975): cast_ring (:25577-25589), each bottle: castStar1 (:25621), its spot hero + rotateH(1.5 tDir, 90 m) (:25626), its type 6 when Random.Range(0, 100) < lckAdjust(5) (:25636-25642; 5 at LCK 1, CharacterControl.cs:20667-20668, the gamble convention plans/fx_cat/decisions.md 30: p 0.05, one roll per bottle), else Random.Range(1, 6) = 1-5, even (:25650); RPC_miracleBlend_create (:26024-26421): Yield 0.4 (:26377), castLight (:26152), randomPot<type>, identity (:26173-26340), Init(chaAdjust(60)) (:26353): at 0.7 s; voice miracleBlend1 / miracleBlend2 (Random.Range(0, 2) != 0 :25786, rapidTrance :25792, loads :25838 / :25807); Yield 0.5 (:25958): standby 0.8 s (:25882)",
      "cues": [
        [0.3, "fx", "cast_ring"],
        [0.3, "fx", "castStar", {"rot": [0, 0, 0], "yaw": "cast"}],
        [0.3, "fx", "castStar", {"rot": [0, 90, 0], "yaw": "cast"}],
        [0.3, "fx", "castStar", {"rot": [0, 180, 0], "yaw": "cast"}],
        [0.3, "fx", "castStar", {"rot": [0, 270, 0], "yaw": "cast"}],
        [0.3, "voice", "miracleBlend1|miracleBlend2"],
        [0.7, "fx", "castLight", {"x": 0.0, "d": 1.5, "yaw": "cast"}],
        [0.7, "fx", "randomPot6", {"x": 0.0, "d": 1.5, "yaw": "cast", "kill": 10, "p": 0.05, "roll": "pot1"}],
        [0.7, "fx", "randomPot1|randomPot2|randomPot3|randomPot4|randomPot5", {"x": 0.0, "d": 1.5, "yaw": "cast", "kill": 10, "p": 0.05, "roll": "!pot1"}],
        [0.7, "fx", "castLight", {"x": -1.5, "d": 0.0, "yaw": "cast"}],
        [0.7, "fx", "randomPot6", {"x": -1.5, "d": 0.0, "yaw": "cast", "kill": 10, "p": 0.05, "roll": "pot2"}],
        [0.7, "fx", "randomPot1|randomPot2|randomPot3|randomPot4|randomPot5", {"x": -1.5, "d": 0.0, "yaw": "cast", "kill": 10, "p": 0.05, "roll": "!pot2"}],
        [0.7, "fx", "castLight", {"x": 0.0, "d": -1.5, "yaw": "cast"}],
        [0.7, "fx", "randomPot6", {"x": 0.0, "d": -1.5, "yaw": "cast", "kill": 10, "p": 0.05, "roll": "pot3"}],
        [0.7, "fx", "randomPot1|randomPot2|randomPot3|randomPot4|randomPot5", {"x": 0.0, "d": -1.5, "yaw": "cast", "kill": 10, "p": 0.05, "roll": "!pot3"}],
        [0.7, "fx", "castLight", {"x": 1.5, "d": 0.0, "yaw": "cast"}],
        [0.7, "fx", "randomPot6", {"x": 1.5, "d": 0.0, "yaw": "cast", "kill": 10, "p": 0.05, "roll": "pot4"}],
        [0.7, "fx", "randomPot1|randomPot2|randomPot3|randomPot4|randomPot5", {"x": 1.5, "d": 0.0, "yaw": "cast", "kill": 10, "p": 0.05, "roll": "!pot4"}]
      ]
    }
  }
},
"mix4": {
  "why": "The mix4 clip: Sticky Gum (RPC_stickyGum_cast, PlayAnimation(\"mix4\", 0.2) Rabbit.cs:26841), Acidic Field (RPC_acidicField_cast :27343) and Healing Field (RPC_healingField_cast :37941), one per play, even chance (one tile each, poolChains; host SEQ \"Field Cast\"), released 0.7 s into the channel (mix1 entry); all three: Yield 0.4, moveSpeed 5 for 0.1 s (a 0.5 m lunge, left out: the hero does not travel, plans/fx_bison/decisions.md 17), Yield 0.1: the field on the floor 2 m ahead (a ray down from 2 m up: the page's floor), its script data only (no EffectControl; it destroys itself after chaAdjust(12) s): kill 10 (fields cut at 10 s); the hero keeps one field of each kind, the next cast Destroys the old one first (option replace); Yield 0.3: standby 0.8 s",
  "skills": {
    "stickyGum": {
      "why": "Rabbit.cs RPC_stickyGum_cast (:26422-26933), Sticky Gum 2: clip mix4, 0.2 s fade (:26841); Yield 0.4 (:26888): moveSpeed 5 (:26568, left out); Yield 0.1 (:26868): at 0.5 s RPC_stickyGum_create(mPos + 2 forward on the floor, FromToRotation(up, the floor's normal) = identity, chaAdjust(12)) (:26606-26643; Rabbit.cs:10032-10080): Destroy the old gum (:10057-10063), stickyGum Instantiated with localScale (sLv + 0.5, 1, sLv + 0.5) = (2.5, 1, 2.5) (:10069-10072; its Animation 'root' and its own Sounds/stickyGum), Rabbit_stickyGum.Init (:10075; data only: the slow on enemies inside, Rabbit_stickyGum.cs:83-140); voice stickyGum1 / stickyGum2 (Random.Range(0, 2) != 0 :26692, rapidTrance :26698, loads :26744 / :26713) at 0.5; Yield 0.3 (:26878): standby 0.8 s (:26788)",
      "cues": [
        [0.5, "fx", "stickyGum", {"d": 2, "scale": [2.5, 1, 2.5], "kill": 10, "replace": true}],
        [0.5, "voice", "stickyGum1|stickyGum2"]
      ]
    },
    "acidicField": {
      "why": "Rabbit.cs RPC_acidicField_cast (:26934-27427), Acidic Field 2 (Acid Overflow #442 only raises the level, :10148): clip mix4, 0.2 s fade (:27343); Yield 0.4 (:27379): moveSpeed 5 (:27080, left out); Yield 0.1 (:27377): at 0.5 s RPC_acidicField_create(mPos + 2 forward on the floor, forward, chaAdjust(12)) (:27118-27145; Rabbit.cs:10106-10180): Destroy the old field (:10131-10137), acidicField Instantiated, LookRotation(forward) (:10143; its looping Sounds/acid2), Rabbit_acidicField.Init (:10148; data only: the 2 s acid pulses, Rabbit_acidicField.cs:83-213), and acidicField_fire Instantiated there, identity (:10172-10178; life 2, its own Sounds/acid1); voice acidicField1 / acidicField2 (Random.Range(0, 2) != 0 :27194, rapidTrance :27200, loads :27246 / :27215) at 0.5; Yield 0.3 (:27372): standby 0.8 s (:27290)",
      "cues": [
        [0.5, "fx", "acidicField", {"d": 2, "kill": 10, "replace": true}],
        [0.5, "fx", "acidicField_fire", {"d": 2}],
        [0.5, "voice", "acidicField1|acidicField2"]
      ]
    },
    "healingField": {
      "why": "Rabbit.cs RPC_healingField_cast (:37541-38029), Healing Field: clip mix4, 0.2 s fade (:37941); Yield 0.4 (:37979): moveSpeed 5 (:37676, left out) and the voice shake2 / mix2 (Random.Range(0, 2) != 0 :37712 and no rapidTrance :37718 -> shake2 :37733, else mix2 :37764: Healing Field has no voice of its own) at 0.4; Yield 0.1 (:37982): at 0.5 s RPC_healingField_create(mPos + 2 forward on the floor, forward, chaAdjust(12)) (:37821-37848; Rabbit.cs:11282-11365): Destroy the old field (:11307-11313), healingField Instantiated, LookRotation(forward) (its looping Sounds/healingField), Rabbit_healingField.Init (data only: the 2 s heal pulses, Rabbit_healingField.cs:79-204), healingField_fire there, identity (:11355-11361; life 2, its own Sounds/acid1); Yield 0.3 (:37966): standby 0.8 s (:37888)",
      "cues": [
        [0.4, "voice", "shake2|mix2"],
        [0.5, "fx", "healingField", {"d": 2, "kill": 10, "replace": true}],
        [0.5, "fx", "healingField_fire", {"d": 2}]
      ]
    }
  }
},
"medicalShot": {
  "why": "The medicalShot clip: Immune Shot, Boost Shot, Heat Shot and Life Shot, four skills (immuneShot1, boostShot2, heatShot3, lifeShot4; each rank 1, its own cooldown) that start RPC_medicalShot with sLv 1-4 (Rabbit.cs:28564-28606; Bible rabbit-skill-reference 13-16), one per play, even chance (one tile each, poolChains); all aim at an ally, here at the 10 m point (plans/fx_sheep/decisions.md 1, 4)",
  "skills": {
    "immuneShot": {
      "why": "Rabbit.cs RPC_medicalShot (:27428-28845) with sLv 1 = immuneShot (its own cooldown, :28564-28606): clip medicalShot, 0.2 s fade (:28612; with the rapidTrance status gilShot instead, :28548-28552: off on the page), voice medicalShot1 / medicalShot2 (Random.Range(0, 2) :28644, loads :28654 / :28685) at 0; Yield 0.3 (:28735): medicalShot_ring createEffect at the hero, hero rotation (:27591-27603; followPosition + followState, life 1 + 1, its own Sounds/medicalShot_ring); without rapidTrance (:27617; with it Yield 0.7 :28730 and the shot at 1.0 s) the hero turns to the ally every FixedUpdate (:27751-27756, WaitForFixedUpdate :28726) until actionTime + 1.4 (:27734): at 1.4 s the shot: moveSpeed -1 (:27783, left out: no travel), firePos = hero + 1 up (:27788), fireDir = the ally's collider.bounds.center - firePos (:27804): medicalShot_fire createEffect, FromToRotation(forward, fireDir) (:27810-27833) = 2.2906 deg down to the ally 10 m ahead, 0.6 m up (the target body, plans/fx_bat/decisions.md 3-4; an ally target, plans/fx_sheep/decisions.md 1, 4); the shot's voice immuneShot1 / immuneShot2 (Random.Range(0, 2), loads :27888 / :27919) under PlayerPrefs pvoice, Game.mGameType > 4 and the own team (:27847-27865: missions and arenas only; kept, as the Bison's and Sheep's mGameType > 4 cues); Physics.Raycast 16 + 5 x Combo rank m (:28183-28188) hits the ally's capsule at (0, 0.612, 9.7): RPC_immuneShot_hit (:28240; Rabbit.cs:10209-10232) Instantiates immuneShot at the hit point, LookRotation(the hero's forward) = no turn, life 1 + 1, its own Sounds/medicalShot_hit; the status (remedy + immunity :28282-28287) is the ally's, not drawn; Yield 0.2 (:28733): moveSpeed 0 (:27650); Yield 0.1 (:28749): standby 1.7 s (:27676): the ring's cut",
      "cues": [
        [0, "voice", "medicalShot1|medicalShot2"],
        [0.3, "fx", "medicalShot_ring", {"cut": 1.7}],
        [1.4, "fx", "medicalShot_fire", {"y": 1, "rot": [2.2906, 0, 0]}],
        [1.4, "voice", "immuneShot1|immuneShot2"],
        [1.4, "fx", "immuneShot", {"d": 9.7, "y": 0.612}]
      ]
    },
    "boostShot": {
      "why": "Rabbit.cs RPC_medicalShot (:27428-28845) with sLv 2 = boostShot (its own cooldown, :28564-28606): clip medicalShot, 0.2 s fade (:28612; with the rapidTrance status gilShot instead, :28548-28552: off on the page), voice medicalShot1 / medicalShot2 (Random.Range(0, 2) :28644, loads :28654 / :28685) at 0; Yield 0.3 (:28735): medicalShot_ring createEffect at the hero, hero rotation (:27591-27603; followPosition + followState, life 1 + 1, its own Sounds/medicalShot_ring); without rapidTrance (:27617; with it Yield 0.7 :28730 and the shot at 1.0 s) the hero turns to the ally every FixedUpdate (:27751-27756, WaitForFixedUpdate :28726) until actionTime + 1.4 (:27734): at 1.4 s the shot: moveSpeed -1 (:27783, left out: no travel), firePos = hero + 1 up (:27788), fireDir = the ally's collider.bounds.center - firePos (:27804): medicalShot_fire createEffect, FromToRotation(forward, fireDir) (:27810-27833) = 2.2906 deg down to the ally 10 m ahead, 0.6 m up (the target body, plans/fx_bat/decisions.md 3-4; an ally target, plans/fx_sheep/decisions.md 1, 4); the shot's voice boostShot1 / boostShot2 (Random.Range(0, 2), loads :27961 / :27992) under PlayerPrefs pvoice, Game.mGameType > 4 and the own team (:27847-27865: missions and arenas only; kept, as the Bison's and Sheep's mGameType > 4 cues); Physics.Raycast 16 + 5 x Combo rank m (:28183-28188) hits the ally's capsule at (0, 0.612, 9.7): RPC_boostShot_hit (:28299; Rabbit.cs:10252-10275) Instantiates boostShot at the hit point, LookRotation(the hero's forward) = no turn, life 1 + 1, its own Sounds/medicalShot_hit; the status (boost + 100 HP x level :28341-28346) is the ally's, not drawn; Yield 0.2 (:28733): moveSpeed 0 (:27650); Yield 0.1 (:28749): standby 1.7 s (:27676): the ring's cut",
      "cues": [
        [0, "voice", "medicalShot1|medicalShot2"],
        [0.3, "fx", "medicalShot_ring", {"cut": 1.7}],
        [1.4, "fx", "medicalShot_fire", {"y": 1, "rot": [2.2906, 0, 0]}],
        [1.4, "voice", "boostShot1|boostShot2"],
        [1.4, "fx", "boostShot", {"d": 9.7, "y": 0.612}]
      ]
    },
    "heatShot": {
      "why": "Rabbit.cs RPC_medicalShot (:27428-28845) with sLv 3 = heatShot (its own cooldown, :28564-28606): clip medicalShot, 0.2 s fade (:28612; with the rapidTrance status gilShot instead, :28548-28552: off on the page), voice medicalShot1 / medicalShot2 (Random.Range(0, 2) :28644, loads :28654 / :28685) at 0; Yield 0.3 (:28735): medicalShot_ring createEffect at the hero, hero rotation (:27591-27603; followPosition + followState, life 1 + 1, its own Sounds/medicalShot_ring); without rapidTrance (:27617; with it Yield 0.7 :28730 and the shot at 1.0 s) the hero turns to the ally every FixedUpdate (:27751-27756, WaitForFixedUpdate :28726) until actionTime + 1.4 (:27734): at 1.4 s the shot: moveSpeed -1 (:27783, left out: no travel), firePos = hero + 1 up (:27788), fireDir = the ally's collider.bounds.center - firePos (:27804): medicalShot_fire createEffect, FromToRotation(forward, fireDir) (:27810-27833) = 2.2906 deg down to the ally 10 m ahead, 0.6 m up (the target body, plans/fx_bat/decisions.md 3-4; an ally target, plans/fx_sheep/decisions.md 1, 4); the shot's voice heatShot1 / heatShot2 (Random.Range(0, 2), loads :28034 / :28065) under PlayerPrefs pvoice, Game.mGameType > 4 and the own team (:27847-27865: missions and arenas only; kept, as the Bison's and Sheep's mGameType > 4 cues); Physics.Raycast 16 + 5 x Combo rank m (:28183-28188) hits the ally's capsule at (0, 0.612, 9.7): RPC_heatShot_hit (:28358; Rabbit.cs:10295-10318) Instantiates heatShot at the hit point, LookRotation(the hero's forward) = no turn, life 1 + 1, its own Sounds/medicalShot_hit; the status (heat + 10 SP x level :28400-28405) is the ally's, not drawn; Yield 0.2 (:28733): moveSpeed 0 (:27650); Yield 0.1 (:28749): standby 1.7 s (:27676): the ring's cut",
      "cues": [
        [0, "voice", "medicalShot1|medicalShot2"],
        [0.3, "fx", "medicalShot_ring", {"cut": 1.7}],
        [1.4, "fx", "medicalShot_fire", {"y": 1, "rot": [2.2906, 0, 0]}],
        [1.4, "voice", "heatShot1|heatShot2"],
        [1.4, "fx", "heatShot", {"d": 9.7, "y": 0.612}]
      ]
    },
    "lifeShot": {
      "why": "Rabbit.cs RPC_medicalShot (:27428-28845) with sLv 4 = lifeShot (its own cooldown, :28564-28606): clip medicalShot, 0.2 s fade (:28612; with the rapidTrance status gilShot instead, :28548-28552: off on the page), voice medicalShot1 / medicalShot2 (Random.Range(0, 2) :28644, loads :28654 / :28685) at 0; Yield 0.3 (:28735): medicalShot_ring createEffect at the hero, hero rotation (:27591-27603; followPosition + followState, life 1 + 1, its own Sounds/medicalShot_ring); without rapidTrance (:27617; with it Yield 0.7 :28730 and the shot at 1.0 s) the hero turns to the ally every FixedUpdate (:27751-27756, WaitForFixedUpdate :28726) until actionTime + 1.4 (:27734): at 1.4 s the shot: moveSpeed -1 (:27783, left out: no travel), firePos = hero + 1 up (:27788), fireDir = the ally's collider.bounds.center - firePos (:27804): medicalShot_fire createEffect, FromToRotation(forward, fireDir) (:27810-27833) = 2.2906 deg down to the ally 10 m ahead, 0.6 m up (the target body, plans/fx_bat/decisions.md 3-4; an ally target, plans/fx_sheep/decisions.md 1, 4); the shot's voice lifeShot1 / lifeShot2 (Random.Range(0, 2), loads :28107 / :28138) under PlayerPrefs pvoice, Game.mGameType > 4 and the own team (:27847-27865: missions and arenas only; kept, as the Bison's and Sheep's mGameType > 4 cues); Physics.Raycast 16 + 5 x Combo rank m (:28183-28188) hits the ally's capsule at (0, 0.612, 9.7): RPC_lifeShot_hit (:28417; Rabbit.cs:10338-10361) Instantiates lifeShot at the hit point, LookRotation(the hero's forward) = no turn, life 1 + 1, its own Sounds/medicalShot_hit; the status (autoLife :28459) is the ally's, not drawn; Yield 0.2 (:28733): moveSpeed 0 (:27650); Yield 0.1 (:28749): standby 1.7 s (:27676): the ring's cut",
      "cues": [
        [0, "voice", "medicalShot1|medicalShot2"],
        [0.3, "fx", "medicalShot_ring", {"cut": 1.7}],
        [1.4, "fx", "medicalShot_fire", {"y": 1, "rot": [2.2906, 0, 0]}],
        [1.4, "voice", "lifeShot1|lifeShot2"],
        [1.4, "fx", "lifeShot", {"d": 9.7, "y": 0.612}]
      ]
    }
  }
},
"rapidTrance": {
  "why": "Rabbit.cs RPC_rapidTrance (:28846-29386), Rapid Trance: clip, 0.2 s fade (:29199), voice rapidTrance1 / rapidTrance2 (Random.Range(0, 2) :29240, loads :29250 / :29281) at 0; Yield 0.3 (:29316): rapidTrance_potion Instantiated and parented to mountHand_L, localPosition 0, identity (:28987-29019; option bone; its EffectControl life 1 ends it at 1.3 s, no Destroy in the coroutine); Yield 0.6 (:29340): at 0.9 s rapidTrance_ring createEffect at the hero, identity (:29062-29074; followPosition, life 1 + 1, its own Sounds/rapidTrance_ring); Yield 0.2 (:29326): at 1.1 s the status rapidTrance for chaAdjust(12) s (:29119): CharacterControl.cs:37520-37523 setColor(0.48, 0.43, 0.78) on every renderer (the purple tint, HERO_SKINS rapidTrance: tint = colour / 0.86, the Bison's enrage rule), 13 s at CHA 1: cut at 10 s (kill 10, the Bison's Enrage tint, plans/fx_bison/decisions.md 31); Yield 0.2 (:29347): standby 1.3 s (:29146)",
  "cues": [
    [0, "voice", "rapidTrance1|rapidTrance2"],
    [0.3, "fx", "rapidTrance_potion", {"bone": "mountHand_L"}],
    [0.9, "fx", "rapidTrance_ring"],
    [1.1, "skin", "rapidTrance", {"kill": 10}]
  ]
},
"statScan": {
  "why": "Rabbit.cs RPC_statScan (:22333-22948), Stat Scan: clip cut in (PlayAnimation(\"statScan\", 0) :22755), voice statScan1 / statScan2 (Random.Range(0, 2) :22799, loads :22809 / :22840) at 0; Yield 0.2 (:22883): the target's createEffect(statScan, target.collider.ClosestPointOnBounds(hero + 1.5 up), identity) (:22506-22524) = (0, 1.1, 9.7) on the 10 m target's body (box x / z +-0.3, y 0.1-1.1: plans/fx_bat/decisions.md 4; faceCamera, life 1 + 0.3, its own Sounds/statScan) and statScan_dust Instantiated at the hero, hero rotation (:22545-22557; life 1); Yield 0.5 (:22893): at 0.7 s the three chat lines of the target's stats (:22610-22675, text: left out); Yield 0.1 (:22876): standby 0.8 s (:22702)",
  "cues": [
    [0, "voice", "statScan1|statScan2"],
    [0.2, "fx", "statScan", {"d": 9.7, "y": 1.1}],
    [0.2, "fx", "statScan_dust"]
  ]
},
"@TruceTrading:truceTrading": {
  "why": "Rabbit.cs RPC_truceTrading1 (:33896-34514), Truce Trading 2 (its own tile, SEQ \"Truce Trading: truceTrading*@0.12 cheer*~@2|cry*~@2\"): clip looped, 0.2 s fade (:34233-34236), truceTrading_ring createEffect at the hero, hero rotation (:34263-34275; followPosition + followState, life 12, its looping Sounds/truceTrading), truceTrading_flag Instantiated and parented to mountHand_L, localPosition 0, identity (:34295-34322; no EffectControl: Destroyed when the loop ends, :34199-34205) and voice truceTrading1 / truceTrading2 (Random.Range(0, 2) :34357, loads :34369 / :34400) at 0; the cast bar magAdjust(12) (:34425-34437) = 0.1 s at high INT, checked every FixedUpdate (Time.time - actionTime <= 0.1 :34086, WaitForFixedUpdate :34463): the roll at 0.12 s, LCK x sLv > Random.Range(0, target.hp) on a target not yet traded (:34094-34111) -> RPC_truceTrading_fire<sLv> with the target (:34123), else with 0 (:34139), sent to every client (ActionEvent; the owner's own loop waits on it: isTrade :34145) -> RPC_truceTrading2 (onActionEvent 347 / 348, :3065-3077, :5656-5667): myCommand becomes truceTrading2, which ends the loop (:34051), the flag (kill 0.12) and the ring (followState: myCommand changed, EffectControl.cs:226-232: cut 0.12, the step change)",
  "cues": [
    [0, "voice", "truceTrading1|truceTrading2"],
    [0, "fx", "truceTrading_ring", {"cut": 0.12}],
    [0, "fx", "truceTrading_flag", {"bone": "mountHand_L", "kill": 0.12}]
  ]
},
"@TruceTrading:cheer": {
  "why": "Rabbit.cs RPC_truceTrading2 (:34515-35019), the trade made (tID != 0 :34733; the chance LCK x 2 / the target's HP, an even pick here: question 1): cheer looped, 0.2 s fade (:34739-34744), truceTrading_success createEffect at the hero, hero rotation (:34749-34767; followPosition, life 1 + 1, its own Sounds/truceTrading_success) and voice tradeSuccess (load :34816) at 0; Yield 2 (:34983): standby (:34660), 2.12 s after the cast",
  "cues": [
    [0, "fx", "truceTrading_success"],
    [0, "voice", "tradeSuccess"]
  ]
},
"@TruceTrading:cry": {
  "why": "Rabbit.cs RPC_truceTrading2 (:34515-35019), the trade refused (tID 0 :34733): cry looped, 0.2 s fade (:34843-34848), truceTrading_fail createEffect at the hero, hero rotation (:34853-34871; followPosition, life 1, its own Sounds/truceTrading_fail) and voice tradeFail (load :34920) at 0; Yield 2 (:34983): standby (:34660)",
  "cues": [
    [0, "fx", "truceTrading_fail"],
    [0, "voice", "tradeFail"]
  ]
},
"@Contract:truceTrading": {
  "why": "Rabbit.cs RPC_contract (:40147-40822), Contract (its own tile, SEQ \"Contract: truceTrading*@0.1 bow~@1.2\"): clip truceTrading looped, 0.2 s fade (:40631-40634); contract_ring createEffect at the hero (:40655-40673): neither game has the file (BB's Resources container has no contract_ring, checks/fx_rabbit_research/skills_b/probe.json; TTO's catalog neither, tto_probe.err; the game logs 'Cannot find contract_ring' :40681): no ring; contract_flag Instantiated and parented to mountHand_L, localPosition 0, identity (:40690-40723; no EffectControl, its looping Sounds/truceTrading; Destroyed at the standby :40277-40283: kill 1.3) at 0; the cast bar magAdjust(3 + 3 level) (:40729-40738) = 0.1 s at high INT, checked every frame (actionTime + 0.1 <= Time.time :40359, YieldDefault :40761)",
  "cues": [
    [0, "fx", "contract_flag", {"bone": "mountHand_L", "kill": 1.3}]
  ]
},
"@Contract:bow": {
  "why": "Rabbit.cs RPC_contract (:40147-40822) at 0.1 s, level 3 (the top tier: SP >= 65 after the cost, doSkill :7607-7619; Bible rabbit-skill-reference 'Contract'): RPC_contract_create3 at getExpandPos(getSpawnVector(hero + 1 up, TransformDirection(0, -1, 3))) (:40464-40475) = on the floor 3 m ahead (the ray meets the floor at 3.16 m, under its 4 m reach, Math.cs:1210-1224; no wall, :1242), hero forward, sent to every client (onActionEvent :3401): RPC_contract_create (:11542-11850): LightGolem (Resources Characters/Elementals/LightGolem/LightGolem, :11596) Instantiated there, LookRotation(forward) (:11611), stats x 1.5 (:11798-11837), on the Rabbit's layer, so LightGolem.Start gives its CrystalBug_tri the material LightGolem2 (layer != 9, LightGolem.cs:58-80); it lives 300 s (LightGolem.cs:44): kill 10 (summons cut at 10 s), its AI left out (as plans/fx_monkey/parts.md part 9); contract_create createEffect there, LookRotation(forward) (:11695-11707; followPosition, life 1 + 1, its own Sounds/truceTrading_success); voice contract1 / contract2 (Random.Range(0, 2) :40512, loads :40524 / :40555); bow, 0.2 s fade (:40580-40585); Yield 1.2 (:40765): the flag Destroyed and standby 1.3 s (:40277-40306)",
  "cues": [
    [0, "fx", "LightGolem", {"d": 3, "kill": 10}],
    [0, "fx", "contract_create", {"d": 3}],
    [0, "voice", "contract1|contract2"]
  ]
},
"shootingArray": {
  "why": "Rabbit.cs RPC_shootingArray (:35020-36052), Shooting Array 2 (a target skill: tPos = the target's transform.position = the 10 m point's floor, :35754): clip, 0.2 s fade (:35775), shootingArray_ring createEffect at the hero, hero rotation (:35787-35805; followPosition + followState, life 1 + 1, its own Sounds/shootingArray_ring) and voice shootingArray1 / shootingArray2 (Random.Range(0, 2) :35848, loads :35858 / :35889, PlayOneShot :35973 / :35928) at 0; Yield 0.5 (:35935); three shots at 0.5 / 0.6 / 0.7 s (Yield 0.1 :35962, 0.1 :35926): each shootingArray_fire Instantiated at the hero + TransformDirection(0, 0.8, 1), LookRotation(forward) (:35196, :35277, :35374; life 1) and the owner's RPC_shootingArray_hit(tPos) (:35216, :35291, :35388; Rabbit.cs:10951-10974): shootingArray_hit at the target's feet, Euler(0, Random.Range(0, 360), 0) (rot randomYaw; life 3 + 1, its own Sounds/shootingArray_hit); the damage pulses at 0.6 / 0.8 / 1.0 s (FindAreaTarget(tPos, 6) :35308, :35436, :35504; Yield 0.1 :35965, 0.2 :35971, 0.2 :35940) draw nothing; at 1.2 s a fourth shootingArray_fire at the hero + TransformDirection(-0.15, 0.7, 0.25), LookRotation(forward) (:35572); Yield 0.1 (:35950): at 1.3 s the finisher on every enemy within 6 m (:35607-35630): RPC_shootingArray_finalhit at its collider.bounds.center (:35640; Rabbit.cs:10994-11017) = (0, 0.6, 10), LookRotation(forward) (life 1); Yield 0.5 (:35942): standby 1.8 s (:35693): the ring's cut",
  "cues": [
    [0, "fx", "shootingArray_ring", {"cut": 1.8}],
    [0, "voice", "shootingArray1|shootingArray2"],
    [0.5, "fx", "shootingArray_fire", {"y": 0.8, "d": 1}],
    [0.5, "fx", "shootingArray_hit", {"d": 10, "rot": "randomYaw"}],
    [0.6, "fx", "shootingArray_fire", {"y": 0.8, "d": 1}],
    [0.6, "fx", "shootingArray_hit", {"d": 10, "rot": "randomYaw"}],
    [0.7, "fx", "shootingArray_fire", {"y": 0.8, "d": 1}],
    [0.7, "fx", "shootingArray_hit", {"d": 10, "rot": "randomYaw"}],
    [1.2, "fx", "shootingArray_fire", {"x": -0.15, "y": 0.7, "d": 0.25}],
    [1.3, "fx", "shootingArray_finalhit", {"d": 10, "y": 0.6}]
  ]
},
"millionaire": {
  "why": "Rabbit.cs RPC_millionaire (:36589-37342), Millionaire 2: clip, 0.2 s fade (:36834), the fee (:36874-36897, gameplay), millionaire_ring createEffect at the hero, hero rotation (:36903-36921; followPosition + followState, life 5 + 1, its own Sounds/millionaire) and voice millionaire1 / millionaire2 (Random.Range(0, 2) :36966, loads :36978 / :37010, PlayOneShot :37272 / :37281) at 0; Yield 0.5 (:37270): at 0.5 s the coroutine millionaire_createPeppon (:36736; :37343-37540): 18 millionaire_peppon (i < 18 :37452), one every 0.15 s (Yield 0.15 :37513) from 0.5 to 3.05 s, each Instantiated at the hero + vFlat(2 x Random.onUnitSphere), Euler(270, Random.Range(0, 360), 0) (:37473-37485; the new options sphere and rot [270, \"random\", 0]; life 2 + 0.4, its Animation and AlphaTimer); the camera's motion blur (:36741-36752) left out; six bursts (i < 6 :37035): i even millionaire1 Instantiated at the hero, hero rotation (:37116-37128), i odd millionaire2 createEffect at the hero, hero rotation (:37153-37165) (life 2 each; WorldParticleCollider), at 0.5, 1.0, 1.7, 2.2, 2.9, 3.4 s (waits [0.5, 0.7, 0.5, 0.7, 0.5, 0.6]: 0.5 after an even burst :37275, 0.7 - 0.1 x div(i, 5) after an odd one :37266, Math.cs:23-27); each wait ends in the damage pulse FindAreaTarget(hero, 8) (:37183-37189): the 10 m target is outside it, no nAttack_hit; standby at 4.0 s (i >= 6 :37035, :37058): the ring's cut",
  "cues": [
    [0, "fx", "millionaire_ring", {"cut": 4.0}],
    [0, "voice", "millionaire1|millionaire2"],
    [0.5, "fx", "millionaire1"],
    [0.5, "fx", "millionaire_peppon", {"sphere": 2, "rot": [270, "random", 0]}],
    [0.65, "fx", "millionaire_peppon", {"sphere": 2, "rot": [270, "random", 0]}],
    [0.8, "fx", "millionaire_peppon", {"sphere": 2, "rot": [270, "random", 0]}],
    [0.95, "fx", "millionaire_peppon", {"sphere": 2, "rot": [270, "random", 0]}],
    [1.0, "fx", "millionaire2"],
    [1.1, "fx", "millionaire_peppon", {"sphere": 2, "rot": [270, "random", 0]}],
    [1.25, "fx", "millionaire_peppon", {"sphere": 2, "rot": [270, "random", 0]}],
    [1.4, "fx", "millionaire_peppon", {"sphere": 2, "rot": [270, "random", 0]}],
    [1.55, "fx", "millionaire_peppon", {"sphere": 2, "rot": [270, "random", 0]}],
    [1.7, "fx", "millionaire1"],
    [1.7, "fx", "millionaire_peppon", {"sphere": 2, "rot": [270, "random", 0]}],
    [1.85, "fx", "millionaire_peppon", {"sphere": 2, "rot": [270, "random", 0]}],
    [2.0, "fx", "millionaire_peppon", {"sphere": 2, "rot": [270, "random", 0]}],
    [2.15, "fx", "millionaire_peppon", {"sphere": 2, "rot": [270, "random", 0]}],
    [2.2, "fx", "millionaire2"],
    [2.3, "fx", "millionaire_peppon", {"sphere": 2, "rot": [270, "random", 0]}],
    [2.45, "fx", "millionaire_peppon", {"sphere": 2, "rot": [270, "random", 0]}],
    [2.6, "fx", "millionaire_peppon", {"sphere": 2, "rot": [270, "random", 0]}],
    [2.75, "fx", "millionaire_peppon", {"sphere": 2, "rot": [270, "random", 0]}],
    [2.9, "fx", "millionaire1"],
    [2.9, "fx", "millionaire_peppon", {"sphere": 2, "rot": [270, "random", 0]}],
    [3.05, "fx", "millionaire_peppon", {"sphere": 2, "rot": [270, "random", 0]}],
    [3.4, "fx", "millionaire2"]
  ]
},
"tenShot": {
  "why": "Rabbit.cs RPC_tenShot (:38760-39710), Ten Shot: clip, 0.2 s fade (:39086), tenShot_ring createEffect at the hero, hero rotation (:39106-39124; followPosition + followState, life 3, its own Sounds/tenShot_ring) and voice tenShot1 / tenShot2 (Random.Range(0, 2) :39169, loads :39181 / :39213, PlayOneShot :39615 / :39620) at 0; Yield 0.2 (:39609): at 0.2 s a copy of the worn main-hand weapon (mChar.mWep1, RabbitEquipment.cs:929-954: the mountHand_R piece, the page's slot R) Instantiated and parented to mountHand_L, localPosition 0, identity (:38901-38922; nothing when none is worn): the new kind propCopy, Destroyed at 2.8 s (:38975-38981); a counter i from 0 at 0.2 s, + 1 every 0.1 s (Yield 0.1 :39629, i++ :38952): volleys at i = 6 / 11 / 15 / 19 / 23 = 0.8 / 1.3 / 1.7 / 2.1 / 2.5 s, each two tenShot_fire Instantiated at the hero + TransformDirection(firePos), LookRotation(rotateH(forward, a)) (rotateH(+a) turns left = Unity yaw -a; i 6 :39265-39291, i 11 :39297-39323, i 15 :39329-39355, i 19 :39361-39387, i 23 :39393-39419; Instantiates :39449 / :39454; life 1, its own Sounds/fourShot_fire); each cone FindAngleTarget(hero, dir, 24, 70, 3) (:39477-39480; 35 deg each side, Damage.cs:1232): only the last volley's two forward cones hold the 10 m target, so at 2.5 s two RPC_nAttack_hit at its ClosestPointOnBounds(hero + 1 up) = (0, 1, 9.7) (:39505 / :39558, :39515 / :39568; the Bible's 2 hits at 0-10 deg); i >= 24 at 2.6 s (:39238): Yield 0.2 (:39607): at 2.8 s the copy Destroyed and standby (:39004): the ring's cut",
  "cues": [
    [0, "fx", "tenShot_ring", {"cut": 2.8}],
    [0, "voice", "tenShot1|tenShot2"],
    [0.2, "propCopy", "R", {"bone": "mountHand_L", "kill": 2.6}],
    [0.8, "fx", "tenShot_fire", {"x": -0.6, "y": 0.5, "d": 0.75, "rot": [0, -45, 0]}],
    [0.8, "fx", "tenShot_fire", {"x": 0.6, "y": 0.5, "d": 0.75, "rot": [0, 45, 0]}],
    [1.3, "fx", "tenShot_fire", {"x": -0.4, "y": 0.6, "d": -0.5, "rot": [0, 135, 0]}],
    [1.3, "fx", "tenShot_fire", {"x": 0.5, "y": 0.6, "d": -0.5, "rot": [0, -135, 0]}],
    [1.7, "fx", "tenShot_fire", {"x": -1.2, "y": 0.75, "d": 0.1, "rot": [0, -90, 0]}],
    [1.7, "fx", "tenShot_fire", {"x": 1, "y": 0.75, "d": 0.1, "rot": [0, 90, 0]}],
    [2.1, "fx", "tenShot_fire", {"x": -0.3, "y": 0.9, "d": -0.7, "rot": [0, 180, 0]}],
    [2.1, "fx", "tenShot_fire", {"x": 0.2, "y": 0.8, "d": -0.7, "rot": [0, 180, 0]}],
    [2.5, "fx", "tenShot_fire", {"x": -0.3, "y": 0.9, "d": 1}],
    [2.5, "fx", "tenShot_fire", {"x": 0.1, "y": 0.85, "d": 1}],
    [2.5, "fx", "nAttack_hit", {"d": 9.7, "y": 1}],
    [2.5, "fx", "nAttack_hit", {"d": 9.7, "y": 1}]
  ]
}
}
```

## Open questions (each with my recommendation)

1. **Truce Trading's outcome.**
   - The game's chance is LCK x 2 / the target's HP. At LCK 1 that is almost always `cry`, but the page models no HP.
   - Recommended: an even `cheer|cry`, so both outcomes are shown.
   - Alternative: `cry` alone, the LCK-1 reality.
2. **Contract's tier.** Recommended: level 3, the Light Golem (top tier, full SP). Alternative: level 1's two Light Panthers at (+-1.5, 0, 2.6), the default with low SP.
3. **contract_ring.** Recommended: nothing. Neither game has the file.
4. **The Medical Shots' target.** Recommended: an ally at the 10 m point, the hit effect on its body at (0, 0.612, 9.7). Alternative: the floor point.
5. **Fields across plays.** Recommended: `replace`, one gum / acid / heal field at a time, as the game. The potions stack, as in the game.
6. **The shared yaw.**
   - Recommended: build P1.
   - Fallback: drop the `yaw` options, so R is 0 and the ring always faces the same way.
7. **The Medical Shots' shot voice gate** (mGameType > 4). Recommended: keep the voice, as the Bison's and Sheep's mission cues.
8. **Rapid Trance's tint.** Recommended: `kill 10`, cut at 10 s as Enrage was. The real status lasts 13 s.
9. **Ten Shot with no weapon worn.** Recommended: no copy, as the game (`if (mWep1)`).
10. **Build order.** The Light Golem uses the Monkey's elementals.js. Recommended: build the Monkey first, as planned. Otherwise the Rabbit build needs the minimal root-loop path of that part.
11. **The 0.1 s bars** (Truce Trading 12 s, Contract 12 s at level 3). Recommended: the SEQ rule's high-INT floor, as every class.

## Offers for the Bible (not written there)

1. **Ten Shot's volleys** are at 0.8 / 1.3 / 1.7 / 2.1 / 2.5 s, 0.4-0.5 s apart. The reference's "waiting 0.1-0.2 s between volleys" is the counter's 0.1 s tick.
2. **Medical Shots fire at 1.4 s** (the Rabbit tracks the ally until then). Under Rapid Trance they fire at 1.0 s with the Gil Shot animation. The shot's voice plays only when mGameType > 4 and on the owner's team, with no isMine branch: in the field the owner never hears it.
3. **Rapid Trance tints the Rabbit** (0.48, 0.43, 0.78). While it runs, Mix / Shake / Miracle Blend / Sticky Gum / Acidic Field always say voice 1, and Healing Field always mix2.
4. **Healing Field has no voice of its own:** shake2 / mix2.
5. **Contract asks for contract_ring**, which exists in neither BB nor TTO, so it has no ring.
6. **Truce Trading's outcome:** `cheer` / `cry` for 2 s with tradeSuccess / tradeFail.
7. **Millionaire:** 18 coins every 0.15 s from 0.5 s within 2 m; bursts at 0.5 / 1.0 / 1.7 / 2.2 / 2.9 / 3.4 s; standby at 4.0 s.
8. **One field of each kind:** Sticky Gum / Acidic Field / Healing Field keep one at a time (the previous one is Destroyed).

## Verification

Not yet run (the checker appends it).

## Verification (13/11/2026)

Checker, office PC, read only. Probes in `C:\work\12tails-wardrobe\checks\fx_rabbit_research\verify_b\` (git-ignored):
- `probe.json` / `probe_sum.txt`: `wardrobe_fx.py rabbit --probe` of the 36 built effects the block cues (plus
  gilShot_ring), exit 0, summarised by the researcher's `psum.py`.
- `body_block.json`: the body's paste-ready block, parsed.
- `cues_check.py`: every cue checked as `pipeline/wardrobe_fx_check.py:263-264` does, with KINDS + `propCopy` and OPTS +
  `yaw` / `sphere` / `replace` / `owner`; keys against `wardrobe/data/rabbit/clips.json` and the proposed SEQ ids; times in
  order.
- `fix.py` -> `fixed.json`, `fmt.py` -> `fixed_pretty.txt`: the corrected entries below (checked by `cues_check.py` and
  `json.loads`).

The researcher's flows (`skills_b/*.flow.txt`) were read against the raw `Rabbit.cs` lines, and the predicates that decide
a branch were worked again by hand. This section wins over the body.

**What holds (re-derived, no change):**
- **Clips and keys.** mix1 0.6333, mix2 0.6, mix3 1.0, mix4 1.2, medicalShot 2.1, rapidTrance 1.5, statScan 1.0,
  truceTrading 1.0, shootingArray 2.2, millionaire 4.3, tenShot 3.0 s; cheer 1.2, cry 0.8, bow 1.4 are the class's emote
  clips. Every key is a clip of the class or an `@TruceTrading:` / `@Contract:` step of the proposed SEQ. The block parses:
  14 keys, 144 cues, times in order, every kind and option valid once `propCopy`, `yaw`, `sphere`, `replace` exist.
- **Timings (every wait added again).**
  - RPC_cast1: mix1 cut in at 0 (:20455), Yield 0.6 (:20809), mix2 cut in and the magAdjust bar (:20259, :20420), then a
    per-frame `Time.time < castTime` (:20598): the release at 0.7 s. magAdjust = clamp(t - floor(mag / 32), 0.1, 600)
    (CharacterControl.cs:20584-20589).
  - mix_cast / shake_cast / miracleBlend_cast: Yield 0.3 then 0.5 (:24177 / :24165, :25048 / :25053, :25975 / :25958); the
    create coroutines Yield 0.4 (:24559, :25392, :26377). #412 is Extra Potion (`rab_extraPotion5`, RabbitSkill.cs:3222-3226):
    5 bottles 72 deg apart (:23881-23902). Miracle Drop's predicates (:25605-25660) skip nothing (222938 - 177320 = 45618;
    102528 - 351047 = -248519, not -248518; 268870 - 322571 = -53701). lckAdjust(5) at LCK 1 = floor(505 / 100.05) = 5.
  - The fields: Yield 0.4 / 0.1 / 0.3 (stickyGum :26888, :26868, :26878; acidicField :27379, :27377, :27372; healingField
    :37979, :37982, :37966); each create Destroys the old field first (:10063, :10137, :11313). The spot is 2 m ahead of the
    cast's mPos, not of the lunged hero (:26611, :27123, :37826).
  - medicalShot: Yield 0.3 (:28735), then FixedUpdate (:28726) until actionTime + 1.4 (:27734). 210291 - 379911 = -169620,
    so the first test passes; 274159 - 481546 = -207387, not -207386, so there is no `continue`, and the shot fires. Then
    Yield 0.2 (:28733) and 0.1 (:28749).
  - rapidTrance: Yield 0.3 / 0.6 / 0.2 / 0.2 (:29316, :29340, :29326, :29347). The tint (0.48, 0.43, 0.78) is set by
    setColor (CharacterControl.cs:37520-37529, its predicates true).
  - statScan: Yield 0.2 / 0.5 / 0.1 (:22883, :22893, :22876). ClosestPointOnBounds((0, 1.5, 0)) on the box y 0.1-1.1,
    z 9.7-10.3 = (0, 1.1, 9.7).
  - truceTrading1: `Time.time - actionTime <= magAdjust(12)` per FixedUpdate (:34086, :34463). truceTrading2: cheer / cry
    with a 0.2 fade, Loop, then Yield 2 (:34739, :34843, :34983).
  - contract: a per-frame check (:40359, :40761); the golem by ActionEvent (:40464-40475); bow 0.2 (:40580); Yield 1.2
    (:40765); the flag Destroyed and standby (:40277-40306).
  - shootingArray: 0.5, then 0.1 / 0.1 / 0.1 / 0.2 / 0.2 / 0.1 / 0.5 (:35935, :35962, :35926, :35965, :35971, :35940,
    :35950, :35942). That gives shots at 0.5 / 0.6 / 0.7, pulses at 0.6 / 0.8 / 1.0, the fourth fire at 1.2, the finisher
    at 1.3 and standby at 1.8. shootingArray_hit is Euler(0, Random.Range(0, 360), 0) at tPos (:10974); finalhit is
    LookRotation(forward) at the bounds centre (:11017).
  - millionaire: coins with i < 18, the first at once, then one every 0.15 s (:37452, :37513): 0.5 ... 3.05 s. After an
    even burst, IL_10D3 -> IL_C8A gives Yield 0.5 (:37283, :37275); after an odd one, Yield 0.7 - 0.1 div(i, 5) (:37266;
    Math.div floors, Math.cs:23-27). Bursts come at 0.5, 1.0, 1.7, 2.2, 2.9 and 3.4 s, standby at 4.0. The 8 m pulse misses
    the body (9.7 > 8).
  - tenShot: as parts.md Verification 1 (the same 13 cues).
- **Names.** Every cued effect builds today (`probe_sum.txt`), except hpPot4 / spPot3 / randomPot1-6 (no Rabbit_potion
  layout: P6) and LightGolem (P7).
  - EffectControl life / afterLife / followPosition / followState / mode are as the whys say. statScan has mode 2.
    truceTrading_ring has life 12 and followState. truceTrading_flag and contract_flag have no EffectControl, and
    contract_flag loops Sounds/truceTrading.
  - The cues name 38 distinct voices, all in the rip's `rabbit/voices`. Every AudioSource clip is in `rabbit/sounds`.
  - contract_ring is in neither game (TTO1102 :6755, :6765).
- **Positions.**
  - Bottle spots and star yaws: Math.rotateH (Math.cs:838-843) turns left for +a. Star i's Euler(0, a i, 0) turns right
    while bottle i sits left at a i, but each ring is symmetric, so the set of stars is the same.
  - P1's code is right: tDir = rotateH(forward, R), LookRotation(tDir) = yaw -R, and bottle i sits at
    x = -1.5 sin(R + a i), d = 1.5 cos(R + a i).
  - The Medical Shot ray runs from (0, 1, 0) to (0, 0.6, 10): pitch atan(0.4 / 10) = 2.2906 deg. It meets the body at
    z 9.7, y = 1 - 0.4 x 0.97 = 0.612.
  - The golem lands on the floor 3 m ahead (Math.cs:1210-1236).
- **Rank picks.** Mix 4 (hpPot4, :24480-24504), Shake 3 (spPot3), Miracle Blend with #422, Sticky Gum 2 (scale 2.5),
  Acidic Field 2 (#442 raises only the level, :10148), Contract level 3 (parts.md Verification 1), Truce Trading 2,
  Shooting Array 2, Millionaire 2.
- **TTO.** `wardrobe/tto_released.json` lists the rabbit clips bountyHunt, clap, coinRicochet, medicTurret and wai: none of
  this report's. The twin table's lines are right (TTO1102 :5063 ... :22871 name the same clips).
- **poolChains.**
  - `taken` (index.html:1458, :1471) does skip a member whose id a SEQ already holds, so the hosts must be renamed Cast /
    Field Cast, as written.
  - `hosts.find(name === "Cast")` (:1465) gives mix3 its host; mix4 takes Field Cast.
  - The hidden hosts' clips stay out of the list through the members' own steps (:3699-3700). fx_check's hidden-host path
    covers the plain mix1 key (wardrobe_fx_check.py:377-386, as the Penguin's cast1).

**Findings:**

1. **The Light Golem keeps its own material: P7 and the `@Contract:bow` why have the swap the wrong way round.**
   - `LightGolem.Start` breaks out when `this.gameObject.layer != 9` (LightGolem.cs:77). Only a golem on layer 9 gets its
     CrystalBug_tri material set to LightGolem2 (:109).
   - A player's layer is the team + 7 (Game.cs:4202-4211: team 1 is layer 8, team 2 is layer 9). The page's Rabbit is on
     team 1.
   - So her golem draws the prefab's own `LightGolem1` (`skills_b/probe3.txt:2`, `probe4.txt:6`), as parts.md item 10
     says.
   - **Corrected:** drop P7's "Export the material LightGolem2 and swap it onto CrystalBug_tri": there is nothing to export
     and nothing to swap. The `@Contract:bow` why is corrected in the block below; its cues are unchanged.
2. **P7 belongs in `fxparts/rabbit.js`, not in the Monkey's `elementals.js`** (a sibling conflict).
   - parts.md part 7 builds the `LightGolem` part in rabbit.js (`fxAnim.play("root", 0, 2)`, no AI).
   - parts.md Verification 6 keeps it there although elementals.js has a `standing` mode: one owner per file.
   - So the elementals.js line in "Page changes" 9 gives way to parts.md part 7. Open question 10 (the build order) no
     longer applies: nothing waits on the Monkey's build.
   - P6's no-op lines go into the same rabbit.js, beside skills_a's Rabbit_mall. They are optional, because the page skips
     a script that has no part (index.html:4270). They stay for the record, as in skills_a Verification 2 (the
     Bison_overLord precedent).
3. **Stat Scan's mark does not stay at (0, 1.1, 9.7): it needs the `owner` option** (parts.md Verification 4, checked
   again here).
   - statScan is the target's createEffect (Rabbit.cs:22524), with followPosition and faceCamera (`probe_sum.txt`).
   - After the LookAt, every live frame BB sets position = owner + TransformDirection(offset) (EffectControl.cs:372-381;
     79799 - 144601 == -64802 and 144276 - 591515 == -447239 are true, 200154 - 143541 != 56614 is true). The offset
     = spawn - owner is taken at Init (:96-104).
   - **Corrected cue:** `[0.2, "fx", "statScan", {"d": 9.7, "y": 1.1, "owner": [0, 0, 10]}]`, the owner being the target's
     feet. It needs the `EffectControl(root)` part with `owner` (parts.md part 5).
   - "Page changes" 10 adds `owner` to OPTS, beside `yaw` / `sphere` / `replace`. The full entry is in the block below.
4. **The Medical Shots' ally at 10 m: the right spot, the wrong rule.**
   - Sheep decision 1 is the opposite rule: an ally skill the game lets the hero cast on herself is shown as a self-cast.
   - The Medical Shots refuse the Rabbit herself. doSkill prints "Cannot use immuneShot / boostShot / heatShot / lifeShot
     on yourself" (Rabbit.cs:6848, :6937, :7026, :7115).
   - So they come under Monkey decision 20: ally skills that refuse a self-target go to the 10 m point.
   - The cues stay as they are. Read this first 5, Open question 4 and the five whys should cite Monkey decision 20 and
     those lines; the whys are corrected in the block below.
   - Also in those whys: the ring's cut 1.7 does nothing. The ring lives 1 s from 0.3, so its life ends at 1.3, and
     followState acts only inside the life (EffectControl.cs:194-232, index.html:4341). The cue may stay.
   - shootingArray_ring's cut 1.8 is the same case (life 1 from 0): harmless, left unchanged.
5. **Icons: nine tiles would show a rank-4 picture that is not the skill's card icon, and CLIP_SKILLS is not needed.**
   - wardrobe_skill_icons.py takes each skill's highest-numbered Bible key (:107-113).
     - For shake, miracleBlend, stickyGum, acidicField, rapidTrance, statScan, shootingArray, millionaire and
       truceTrading, that key is `<skill>4`. Its picture differs from the Bible card's icon (the md5s differ).
     - The cards' icons (12t_projects/bible/index.html SKILLS) are shake3, miracleBlend1, stickyGum2, acidicField2,
       rapidTrance1, statScan1, shootingArray2, millionaire2 and truceTrading2.
     - Today's `data/icons/hd/rabbit/` millionaire, rapidTrance, shootingArray, statScan and truceTrading.webp are already
       byte-equal to the `4` keys. These are the "seven more Rabbit tiles outside this scope" of skills_a.md open
       question 7.
     - The others match their cards: mix4; healingField5 = 1; contract5 = 1; tenShot5 = 1; immuneShot1; boostShot2 = 1;
       heatShot3 = 1; lifeShot4 = 1.
   - **Corrected** (merged with skills_a.md's line):
     ```python
     RANK_ICONS = {"mole": {f"tnt{n}": f"mole_tnt{n}" for n in range(1, 5)},
                   "rabbit": {"backpack": "rabbit_backpack2", "circleShot": "rabbit_circleShot2", "fourShot": "rabbit_fourShot2",
                              "gorgonShot": "rabbit_gorgonShot2", "mall": "rabbit_mall2", "shake": "rabbit_shake3",
                              "miracleBlend": "rabbit_miracleBlend1", "stickyGum": "rabbit_stickyGum2",
                              "acidicField": "rabbit_acidicField2", "rapidTrance": "rabbit_rapidTrance1",
                              "statScan": "rabbit_statScan1", "shootingArray": "rabbit_shootingArray2",
                              "millionaire": "rabbit_millionaire2", "truceTrading": "rabbit_truceTrading2"}}
     ```
   - The body's `CLIP_SKILLS["rabbit"]` lines for mix3, mix4 and medicalShot are redundant. Once the cue file holds the
     three pools, :129-147 give every member its icon on the pool's clip (skills_a Verification 4 found the same for
     gilShot).
   - **Corrected:** `CLIP_SKILLS["rabbit"] = {"maim": ["maimShot"]}` (skills_a's line) only. "Page changes" 3's "The
     Bible has every key" list should name the card icons above: rabbit_shake4 and the other `4` keys exist, but they are
     not the cards' icons.
6. **The page lines, merged with the siblings'.** The body's SEQ block still has the old Charge Attack / Bounce / Mall lines
   and lacks Normal Attack, Customized Shotgun and From the Above. Pasting it would undo the Verifications of
   attacks_emotes.md, skills_a.md and effect_only.md.
   ```js
     rabbit: ["Normal Attack: nAttack", "Customized Shotgun: nAttack", "Charge Attack: cAttack1@1 cAttack2*@4 cAttack3",
       "Cast: mix1@0.6 mix2*@0.1 mix3~", "Field Cast: mix1@0.6 mix2*@0.1 mix4~", "Bounce: bounce1@9.5 bounce2!",
       "Mall: mall1*@3 mall2*!@2 sit*~@3", "From the Above: bounce1@9.5 bounce2!",
       "Truce Trading: truceTrading*@0.12 cheer*~@2|cry*~@2", "Contract: truceTrading*@0.1 bow~@1.2"],
   ```
   - SEQ_SKILL: `rabbit: { "@CustomizedShotgun": "customizedShotgun", "@FromtheAbove": "fromTheAbove", "@TruceTrading":
     "truceTrading", "@Contract": "contract" }`.
     - Both of this report's entries are needed. Without them the Truce Trading tile would also show the Contract icon,
       because OWN_TILE gives contract the truceTrading clip (index.html:3463-3468).
   - OWN_TILE: `"rabbit": {"customizedShotgun": ["nAttack"], "fromTheAbove": ["bounce1", "bounce2"], "contract":
     ["truceTrading", "bow"]}`.
   - TTO adds no SEQ line (tto.md Verification 2).
   - SEQ_ALT (index.html:1413) parses every token.
   - attacks_emotes.md's plain emote entries (`bow`, `cheer`, `cry`) do not play in these tiles: the "@" keys come first
     (index.html:5387-5388).
7. **Text corrections (no cue change).**
   - "Every other cued effect is `ready` in plans/fx_inventory.md, castStar included" is wrong. castStar and castLight are
     not in the inventory at all: `### rabbit` lists cast_ring but neither of them. parts.md item 7 explains why: they are
     the hero prefab's fields `castStar1` / `castLight`, built by their Resources names. Both build (`probe_sum.txt`:
     castStar has 3 nodes and life 0.5, castLight life 1).
   - "All 39 voices" should read 38.
   - Read this first 3: the roll compares the raw `lck x sLv` with `Random.Range(0, hp)` (:34111), not lckAdjust. At LCK 1,
     p = 2 / HP.
   - "Standby ... the ring's cut" for Medical Shot and Shooting Array: no cut happens (item 4).
8. **Other sibling conflicts.**
   - parts.md writes "Med Research #412" (Read this first, the hpPot row). #412 is Extra Potion (`rab_extraPotion5`,
     RabbitSkill.cs:3222-3226); Med Research is #432 (:3244-3248). This report has it right.
   - tenShot is also in parts.md's PASTE-READY, with the same cues (only the first two swapped). Paste one copy: this
     report's (parts.md: "the skills researchers' entries win").
   - parts.md's Sticky Gum and field fragments lack `replace`, and its Stat Scan fragment is item 3's. Paste this report's
     entries.
   - LAYOUTS / EXTRA_FOLDERS: the same lines as parts.md. BUILT: parts.md's list is the superset (it also adds
     Rabbit_sniperCamera, Rabbit_mall, LightGolem and LightGolemAI).
9. **The calls hold against the standing rules.**
   - Top rank, passives on: as above.
   - Random picks as the game makes them: the bottles' kinds (a p 0.05 roll per bottle), the voices, the coins' spots and
     yaws, the hit yaws.
     - The one exception is Truce Trading's even cheer | cry (Q1). It follows Cat decision 32: where LCK 1 makes an outcome
       all but impossible, the setting that shows every outcome is taken. Here p = 2 / HP. It stands.
   - Enemy effects at the 10 m point: Stat Scan, Shooting Array, Ten Shot's hits. Millionaire's pulses miss.
   - 10 s cuts: the fields, the bottles (life 60 s), the tint (13 s), the golem (300 s).
   - One tile per skill: 17 tiles (3 + 3 + 4 pool tiles, 2 sequences, 5 single clips).
   - Missing parts built: P1-P7, P7 as corrected by items 1-2. contract_ring is in neither game, so there is nothing to
     build.
   - P3 `replace`, against the Cat's existing `single` (index.html:4768-4771):
     - `single` keeps the old copy and renews its kill.
     - The game Destroys the old field and Instantiates a new one, so its drop clip and its sound start again
       (:10063-10075).
     - So a new option is right.
10. **Nothing missed.**
    - Every RPC that plays these clips is covered (clip_calls.txt). effect_only.md's census rows cast1 ... contract
      agree. truceTrading2 plays the emote clips cheer / cry, which clip_calls misses.
    - Passives that bear on these skills: #412 and #422 are in. #442 changes only the level. New Order #444 changes only
      the golem's stats. Medical Enhancement changes only the statuses. Field Pharmacy and Trading With Wind are
      Reborn-only (their Bible cards say `onlyServer:"reborn"`).
    - The shot ally's status looks draw nothing at the shot. autoLife's look comes only at the holder's death
      (createSpecialEffect case 107, CharacterControl.cs:44160-44178; Rabbit.cs:300).
    - No TTO cue.
    - Bible offers 1-8 stand. The golem's material (item 1) is already parts.md's offer.

**Corrected entries.** These replace the body's `statScan`, `@Contract:bow` and `medicalShot` in full; the other 11 keys
stand as written (14 keys, 144 cues; `verify_b\fixed_pretty.txt`, checked):

```json
{
"statScan": {
  "why": "Rabbit.cs RPC_statScan (:22333-22948), Stat Scan: clip cut in (PlayAnimation(\"statScan\", 0) :22755), voice statScan1 / statScan2 (Random.Range(0, 2) :22799, loads :22809 / :22840) at 0; Yield 0.2 (:22883): the target's createEffect(statScan, target.collider.ClosestPointOnBounds(hero + 1.5 up), identity) (:22506-22524) = (0, 1.1, 9.7) on the 10 m target's body (box x / z +-0.3, y 0.1-1.1: plans/fx_bat/decisions.md 4; faceCamera, life 1 + 0.3, its own Sounds/statScan; followPosition with the scanned target as owner: each live frame after the turn to the camera its spot is owner + rotation x (spawn - owner), EffectControl.cs:96-104, :372-381, so the cue's owner [0, 0, 10], the target's feet: plans/fx_rabbit/parts.md part 5 and its Verification 4) and statScan_dust Instantiated at the hero, hero rotation (:22545-22557; life 1); Yield 0.5 (:22893): at 0.7 s the three chat lines of the target's stats (:22610-22675, text: left out); Yield 0.1 (:22876): standby 0.8 s (:22702)",
  "cues": [
    [0, "voice", "statScan1|statScan2"],
    [0.2, "fx", "statScan", {"d": 9.7, "y": 1.1, "owner": [0, 0, 10]}],
    [0.2, "fx", "statScan_dust"]
  ]
},
"@Contract:bow": {
  "why": "Rabbit.cs RPC_contract (:40147-40822) at 0.1 s, level 3 (the top tier: SP >= 65 after the cost, doSkill :7607-7619; Bible rabbit-skill-reference 'Contract'): RPC_contract_create3 at getExpandPos(getSpawnVector(hero + 1 up, TransformDirection(0, -1, 3))) (:40464-40475) = on the floor 3 m ahead (the ray meets the floor at 3.16 m, under its 4 m reach, Math.cs:1210-1224; no wall, :1242), hero forward, sent to every client (onActionEvent :3401): RPC_contract_create (:11542-11850): LightGolem (Resources Characters/Elementals/LightGolem/LightGolem, :11596) Instantiated there, LookRotation(forward) (:11611), stats x 1.5 (:11798-11837), on the Rabbit's layer (:11721), so LightGolem.Start keeps its prefab material LightGolem1: it swaps CrystalBug_tri to LightGolem2 only on layer 9 (`if (layer != 9) break`, LightGolem.cs:77, the swap :109; layer 9 = team 2, a player's layer is team + 7, Game.cs:4202-4211; the page's Rabbit is team 1); it lives 300 s (LightGolem.cs:44): kill 10 (summons cut at 10 s), its AI left out (Mole decision 32), root looped from the spawn by the LightGolem part in fxparts/rabbit.js (plans/fx_rabbit/parts.md part 7); contract_create createEffect there, LookRotation(forward) (:11695-11707; followPosition, life 1 + 1, its own Sounds/truceTrading_success); voice contract1 / contract2 (Random.Range(0, 2) :40512, loads :40524 / :40555); bow, 0.2 s fade (:40580-40585); Yield 1.2 (:40765): the flag Destroyed and standby 1.3 s (:40277-40306)",
  "cues": [
    [0, "fx", "LightGolem", {"d": 3, "kill": 10}],
    [0, "fx", "contract_create", {"d": 3}],
    [0, "voice", "contract1|contract2"]
  ]
},
"medicalShot": {
  "why": "The medicalShot clip: Immune Shot, Boost Shot, Heat Shot and Life Shot, four skills (immuneShot1, boostShot2, heatShot3, lifeShot4; each rank 1, its own cooldown) that start RPC_medicalShot with sLv 1-4 (Rabbit.cs:28564-28606; Bible rabbit-skill-reference 13-16), one per play, even chance (one tile each, poolChains); all aim at an ally and refuse the Rabbit herself ('Cannot use immuneShot / boostShot / heatShot / lifeShot on yourself', Rabbit.cs:6848, :6937, :7026, :7115), so the ally stands at the 10 m point (plans/fx_monkey/decisions.md 20: ally skills that refuse a self-target; not plans/fx_sheep/decisions.md 1, the self-casts)",
  "skills": {
    "immuneShot": {
      "why": "Rabbit.cs RPC_medicalShot (:27428-28845) with sLv 1 = immuneShot (its own cooldown, :28564-28606): clip medicalShot, 0.2 s fade (:28612; with the rapidTrance status gilShot instead, :28548-28552: off on the page), voice medicalShot1 / medicalShot2 (Random.Range(0, 2) :28644, loads :28654 / :28685) at 0; Yield 0.3 (:28735): medicalShot_ring createEffect at the hero, hero rotation (:27591-27603; followPosition + followState, life 1 + 1, its own Sounds/medicalShot_ring); without rapidTrance (:27617; with it Yield 0.7 :28730 and the shot at 1.0 s) the hero turns to the ally every FixedUpdate (:27751-27756, WaitForFixedUpdate :28726) until actionTime + 1.4 (:27734): at 1.4 s the shot: moveSpeed -1 (:27783, left out: no travel), firePos = hero + 1 up (:27788), fireDir = the ally's collider.bounds.center - firePos (:27804): medicalShot_fire createEffect, FromToRotation(forward, fireDir) (:27810-27833) = 2.2906 deg down to the ally 10 m ahead, 0.6 m up (the target body, plans/fx_bat/decisions.md 3-4; an ally target that is never the Rabbit, Rabbit.cs:6848 / :6937 / :7026 / :7115: plans/fx_monkey/decisions.md 20); the shot's voice immuneShot1 / immuneShot2 (Random.Range(0, 2), loads :27888 / :27919) under PlayerPrefs pvoice, Game.mGameType > 4 and the own team (:27847-27865: missions and arenas only; kept, as the Bison's and Sheep's mGameType > 4 cues); Physics.Raycast 16 + 5 x Combo rank m (:28183-28188) hits the ally's capsule at (0, 0.612, 9.7): RPC_immuneShot_hit (:28240; Rabbit.cs:10209-10232) Instantiates immuneShot at the hit point, LookRotation(the hero's forward) = no turn, life 1 + 1, its own Sounds/medicalShot_hit; the status (remedy + immunity :28282-28287) is the ally's, not drawn; Yield 0.2 (:28733): moveSpeed 0 (:27650); Yield 0.1 (:28749): standby 1.7 s (:27676; the ring's life 1 ended at 1.3 s, so its cut 1.7 changes nothing: followState acts within the life, EffectControl.cs:194-232, index.html:4341)",
      "cues": [
        [0, "voice", "medicalShot1|medicalShot2"],
        [0.3, "fx", "medicalShot_ring", {"cut": 1.7}],
        [1.4, "fx", "medicalShot_fire", {"y": 1, "rot": [2.2906, 0, 0]}],
        [1.4, "voice", "immuneShot1|immuneShot2"],
        [1.4, "fx", "immuneShot", {"d": 9.7, "y": 0.612}]
      ]
    },
    "boostShot": {
      "why": "Rabbit.cs RPC_medicalShot (:27428-28845) with sLv 2 = boostShot (its own cooldown, :28564-28606): clip medicalShot, 0.2 s fade (:28612; with the rapidTrance status gilShot instead, :28548-28552: off on the page), voice medicalShot1 / medicalShot2 (Random.Range(0, 2) :28644, loads :28654 / :28685) at 0; Yield 0.3 (:28735): medicalShot_ring createEffect at the hero, hero rotation (:27591-27603; followPosition + followState, life 1 + 1, its own Sounds/medicalShot_ring); without rapidTrance (:27617; with it Yield 0.7 :28730 and the shot at 1.0 s) the hero turns to the ally every FixedUpdate (:27751-27756, WaitForFixedUpdate :28726) until actionTime + 1.4 (:27734): at 1.4 s the shot: moveSpeed -1 (:27783, left out: no travel), firePos = hero + 1 up (:27788), fireDir = the ally's collider.bounds.center - firePos (:27804): medicalShot_fire createEffect, FromToRotation(forward, fireDir) (:27810-27833) = 2.2906 deg down to the ally 10 m ahead, 0.6 m up (the target body, plans/fx_bat/decisions.md 3-4; an ally target that is never the Rabbit, Rabbit.cs:6848 / :6937 / :7026 / :7115: plans/fx_monkey/decisions.md 20); the shot's voice boostShot1 / boostShot2 (Random.Range(0, 2), loads :27961 / :27992) under PlayerPrefs pvoice, Game.mGameType > 4 and the own team (:27847-27865: missions and arenas only; kept, as the Bison's and Sheep's mGameType > 4 cues); Physics.Raycast 16 + 5 x Combo rank m (:28183-28188) hits the ally's capsule at (0, 0.612, 9.7): RPC_boostShot_hit (:28299; Rabbit.cs:10252-10275) Instantiates boostShot at the hit point, LookRotation(the hero's forward) = no turn, life 1 + 1, its own Sounds/medicalShot_hit; the status (boost + 100 HP x level :28341-28346) is the ally's, not drawn; Yield 0.2 (:28733): moveSpeed 0 (:27650); Yield 0.1 (:28749): standby 1.7 s (:27676; the ring's life 1 ended at 1.3 s, so its cut 1.7 changes nothing: followState acts within the life, EffectControl.cs:194-232, index.html:4341)",
      "cues": [
        [0, "voice", "medicalShot1|medicalShot2"],
        [0.3, "fx", "medicalShot_ring", {"cut": 1.7}],
        [1.4, "fx", "medicalShot_fire", {"y": 1, "rot": [2.2906, 0, 0]}],
        [1.4, "voice", "boostShot1|boostShot2"],
        [1.4, "fx", "boostShot", {"d": 9.7, "y": 0.612}]
      ]
    },
    "heatShot": {
      "why": "Rabbit.cs RPC_medicalShot (:27428-28845) with sLv 3 = heatShot (its own cooldown, :28564-28606): clip medicalShot, 0.2 s fade (:28612; with the rapidTrance status gilShot instead, :28548-28552: off on the page), voice medicalShot1 / medicalShot2 (Random.Range(0, 2) :28644, loads :28654 / :28685) at 0; Yield 0.3 (:28735): medicalShot_ring createEffect at the hero, hero rotation (:27591-27603; followPosition + followState, life 1 + 1, its own Sounds/medicalShot_ring); without rapidTrance (:27617; with it Yield 0.7 :28730 and the shot at 1.0 s) the hero turns to the ally every FixedUpdate (:27751-27756, WaitForFixedUpdate :28726) until actionTime + 1.4 (:27734): at 1.4 s the shot: moveSpeed -1 (:27783, left out: no travel), firePos = hero + 1 up (:27788), fireDir = the ally's collider.bounds.center - firePos (:27804): medicalShot_fire createEffect, FromToRotation(forward, fireDir) (:27810-27833) = 2.2906 deg down to the ally 10 m ahead, 0.6 m up (the target body, plans/fx_bat/decisions.md 3-4; an ally target that is never the Rabbit, Rabbit.cs:6848 / :6937 / :7026 / :7115: plans/fx_monkey/decisions.md 20); the shot's voice heatShot1 / heatShot2 (Random.Range(0, 2), loads :28034 / :28065) under PlayerPrefs pvoice, Game.mGameType > 4 and the own team (:27847-27865: missions and arenas only; kept, as the Bison's and Sheep's mGameType > 4 cues); Physics.Raycast 16 + 5 x Combo rank m (:28183-28188) hits the ally's capsule at (0, 0.612, 9.7): RPC_heatShot_hit (:28358; Rabbit.cs:10295-10318) Instantiates heatShot at the hit point, LookRotation(the hero's forward) = no turn, life 1 + 1, its own Sounds/medicalShot_hit; the status (heat + 10 SP x level :28400-28405) is the ally's, not drawn; Yield 0.2 (:28733): moveSpeed 0 (:27650); Yield 0.1 (:28749): standby 1.7 s (:27676; the ring's life 1 ended at 1.3 s, so its cut 1.7 changes nothing: followState acts within the life, EffectControl.cs:194-232, index.html:4341)",
      "cues": [
        [0, "voice", "medicalShot1|medicalShot2"],
        [0.3, "fx", "medicalShot_ring", {"cut": 1.7}],
        [1.4, "fx", "medicalShot_fire", {"y": 1, "rot": [2.2906, 0, 0]}],
        [1.4, "voice", "heatShot1|heatShot2"],
        [1.4, "fx", "heatShot", {"d": 9.7, "y": 0.612}]
      ]
    },
    "lifeShot": {
      "why": "Rabbit.cs RPC_medicalShot (:27428-28845) with sLv 4 = lifeShot (its own cooldown, :28564-28606): clip medicalShot, 0.2 s fade (:28612; with the rapidTrance status gilShot instead, :28548-28552: off on the page), voice medicalShot1 / medicalShot2 (Random.Range(0, 2) :28644, loads :28654 / :28685) at 0; Yield 0.3 (:28735): medicalShot_ring createEffect at the hero, hero rotation (:27591-27603; followPosition + followState, life 1 + 1, its own Sounds/medicalShot_ring); without rapidTrance (:27617; with it Yield 0.7 :28730 and the shot at 1.0 s) the hero turns to the ally every FixedUpdate (:27751-27756, WaitForFixedUpdate :28726) until actionTime + 1.4 (:27734): at 1.4 s the shot: moveSpeed -1 (:27783, left out: no travel), firePos = hero + 1 up (:27788), fireDir = the ally's collider.bounds.center - firePos (:27804): medicalShot_fire createEffect, FromToRotation(forward, fireDir) (:27810-27833) = 2.2906 deg down to the ally 10 m ahead, 0.6 m up (the target body, plans/fx_bat/decisions.md 3-4; an ally target that is never the Rabbit, Rabbit.cs:6848 / :6937 / :7026 / :7115: plans/fx_monkey/decisions.md 20); the shot's voice lifeShot1 / lifeShot2 (Random.Range(0, 2), loads :28107 / :28138) under PlayerPrefs pvoice, Game.mGameType > 4 and the own team (:27847-27865: missions and arenas only; kept, as the Bison's and Sheep's mGameType > 4 cues); Physics.Raycast 16 + 5 x Combo rank m (:28183-28188) hits the ally's capsule at (0, 0.612, 9.7): RPC_lifeShot_hit (:28417; Rabbit.cs:10338-10361) Instantiates lifeShot at the hit point, LookRotation(the hero's forward) = no turn, life 1 + 1, its own Sounds/medicalShot_hit; the status (autoLife :28459) is the ally's, not drawn; Yield 0.2 (:28733): moveSpeed 0 (:27650); Yield 0.1 (:28749): standby 1.7 s (:27676; the ring's life 1 ended at 1.3 s, so its cut 1.7 changes nothing: followState acts within the life, EffectControl.cs:194-232, index.html:4341)",
      "cues": [
        [0, "voice", "medicalShot1|medicalShot2"],
        [0.3, "fx", "medicalShot_ring", {"cut": 1.7}],
        [1.4, "fx", "medicalShot_fire", {"y": 1, "rot": [2.2906, 0, 0]}],
        [1.4, "voice", "lifeShot1|lifeShot2"],
        [1.4, "fx", "lifeShot", {"d": 9.7, "y": 0.612}]
      ]
    }
  }
}
}
```
