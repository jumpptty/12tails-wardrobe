# Cat effects: decisions (2026-11-13), decided overnight, for the user's review

The user was asleep, so the planner decided every open question in the six reports in this folder (attacks_emotes,
skills_a, skills_b, effect_only, parts, tto), each read with its "## Verification" (the verification wins where the two
differ). Rules used, in this order: the standing rules (top rank, passives on; random picks as the game makes them;
enemy effects at the 10 m target point; homing aims 0.6 m up; target-rotation effects rot [0, 180, 0]; long buffs /
fields cut at 10 s; a tile per skill, effect-only tiles on the idle stance; missing parts always built; TTO cues only
for the released `anchorYank`, `crescentEclipse1`, `crescentEclipse2`, `dropAnchor`, `royalFlush1`), the page's own SEQ
rule (index.html above SEQ, the user 2026-11-09: "a charge = full charge, a channel = its duration, or three hits (at
least 3 s) when it runs until the player moves"), then the Wolf's, Sheep's, Penguin's, Bat's and Bison's decisions by
analogy, then the reports' own recommendations. Every item is **decided overnight, for the user's review**: any of them
can be turned round in the morning.

Already in the tree from the Bat's and the Bison's builds (checked 2026-11-13; nothing to rebuild for the Cat): UVScroll
(`fxparts/uvscroll.js` + its LAYOUTS line), AlphaTimer driving Opaque1 / Opaque2 (`alphatimer.js` OPACITY), the
Shuriken graft (`SHURIKEN_FROM_TTO`, one table entry to add), `particles.js`' multiply / AdditiveOffset / AlphaOffset,
`api.spawn` with the entry's `"builds"`, `worn` / `notWorn`, `everyCycle`, the `"sound"` cue's rip-wide fallback.

## Tiles and sequences
1. Normal Attack SEQ to the code's fixed starts: `"Normal Attack: nAttack1@0.6 nAttack2^@0.6 nAttack3@0.5 nAttack4"`
   (stages at 0.6 / 1.2 / 1.7 s). Reason: the dispatcher's waits (attacks_emotes item 1, verified); Sheep decision 12.
2. The first step keeps the page's 0.2 s fade (nAttack1, cAttack1, the gamble clip and ko are cuts in the game).
   Reason: Bat decision 28, Bison decision 4 (attacks_emotes Q4, effect_only).
3. Charge Attack at full charge with Double Focus #411 on: `"Charge Attack: cAttack1@0.5 cAttack2*@2.6"` (three ticks,
   6 / 6 stacks). Reason: passives on; the SEQ rule "a charge = full charge" (attacks_emotes Q1).
4. Grand Casino Arcade: `"grandCasinoArcade1 grandCasinoArcade2*@13.2 grandCasinoArcade3"`, all five spins (15.9 s), not cut
   at 10 s. Reason: top rank (sLv 2 = 5 spins); a channel of fixed length is "its duration" in the SEQ rule, and the 10 s
   cut is for long buffs / fields (skills_a item 2, parts Q2).
5. Heart Ripper `"heartRipper1@0.4 heartRipper2"`, Finishing Blow `"finishingBlow1@0.4 finishingBlow2"`. Reason: the
   coroutines' waits (skills_a item 2, Q6, verified).
6. Support Fire keeps `"supportFire1 supportFire2*@3"`; the ring's and the cannons' `cut` is **2.95** (supportFire2's
   clock). Reason: the channel runs until the player moves, so the SEQ rule's "three hits (at least 3 s)" holds (skills_b
   Q6), not parts Q3's 10 s; 2.95 because a cut at exactly a step's end never fires when the tile loops (skills_b
   verification 3; the Penguin's manaField_ring).
7. Five pools, one tile per member, from the cue file (poolChains): `instantCast` = Fate Draw, Double Down; `gamble` =
   Power Shuffle, Life Gamble, Skill Gamble; `pointTarget` = Two Pair, Copycat; `throw1` = Lucky Card, Lucky Dice;
   `throw2` = Flying Dagger, Disarm, Bleed. Reason: one tile per skill (skills_a item 1, skills_b item 1; the gamble
   pool is also what keeps Even Odds' tile from taking the clip out of the skill tab, effect_only "Coordination").
8. The effect-only and passive tiles: `"Awareness: root*@3"`, `"Damage Roulette: root*@10.2"`, `"Treasure Hunt: root*@1"`,
   `"Even Odds: gamble"`, `"Nine Lives: ko@3 getUp"`; SEQ_SKILL `cat: { "@Awareness": "awareness", "@DamageRoulette":
   "damageRoulette", "@TreasureHunt": "treasureHunt", "@EvenOdds": "evenOdds", "@NineLives": "nineLives" }`;
   `wardrobe_skill_icons.py` `EFFECT_ONLY["cat"] = ["awareness", "damageRoulette", "treasureHunt"]`, `OWN_TILE["cat"] =
   {"evenOdds": ["gamble"], "nineLives": ["ko", "getUp"]}`. Reason: one tile per skill; the Penguin's Frost Spike and
   the Sheep's Quick Heal (effect_only block 1-4, verified).
9. Effect-only steps longer than the 0.8 s idle are held (`root*@t`), so the stance loops instead of freezing on its last
   frame. Reason: effect_only Q9, verified (clampWhenFinished). The same fix for the Penguin's / Bat's / Bison's
   `root@t` tiles is offered to the user, not done in this job.
10. Treasure Hunt gets its own tile: the coin burst 1 m ahead, no box. Reason: a passive with its own RPC, card and icon,
    the Frost Spike precedent (effect_only Q3).
11. Even Odds: its own tile on the gamble clip, a random pool of the two hosts (Life / Skill Gamble's cues with the loss
    always caught); and in the Life / Skill Gamble tiles a lost roll (50 %) also shows `evenOdds_hit` in place of the
    loss. Reason: passives on, the page keeps no 90 s cooldown (skills_a Q4); its own tile by one-tile-per-skill
    (effect_only Q4).
12. Nine Lives plays `ninelife1|ninelife2` at 3 s (TTO's fix: BB asks for `nineLives1 / 2`, which its data lacks).
    Reason: Sheep decision 10, Bat decision 18 (effect_only Q5).
13. Drop Anchor is one tile with the automatic yank: `"Drop Anchor: dropAnchor! root*~@5.65 anchorYank"` (7.75 s); Crescent
    Eclipse becomes `"crescentEclipse1! crescentEclipse2^"`; Royal Flush stays a single clip. Reason: the game with no
    second press (tto Q6); the TTO skills cut in (Row6Begin `PlayAnimation(clip, 0)`), so `!` as the Sheep's Seal (Sheep
    decision 17), unlike the combos' first steps (decision 2); Bison decision 15 for the single clip.
14. shikifujin (no TTO or BB code plays it) is hidden: `NEVER_PLAYED.cat = ["shikifujin"]`. Reason: the Wolf's cast1-3
    (the user 2026-11-09: "Remove the tile") and Bison decision 9 (tto Q9); mentioned to the user in case he wants it kept.
15. `pillage` gets its icon: `CLIP_SKILLS["cat"] = {"pillage": ["pillagePlunge"]}`. Reason: the tile has none otherwise
    (skills_b item 3, Q10).
16. activateIcon1 (the mission's battle loop): no tile. TTO-only emote clips stay silent; chat voices are BB's chat1-5.
    Reason: Penguin decision 19, Bat decision 36 (attacks_emotes item 7).
17. getUp gets RPC_revive's voice: `"getUp": [0, "voice", "revive", {"p": 0.5}]` (RPC_ko's getUp is silent, so half the
    plays). Reason: Sheep decision 11's shape for the KO tile (attacks_emotes Q3); the same line for the other classes is
    offered to the user as a cross-class follow-up, not done here. `@NineLives:getUp` keeps it out of Nine Lives.
18. KO: the Wolf / Penguin entry (voices ko1|ko2, dead1|dead2; `deadEffect` on half the plays). Reason: Sheep decision 11
    (attacks_emotes item 9).

## Where things land
19. Melee hits draw nothing: no `nAttack_hit` / `hiddenBlade_hit` on the combo, no Forward Lunge, Moon Blade, Moon Storm,
    Pillage Plunge, Reverse Thrust or Backstab hits (their 2-4 m boxes never reach the 10 m target; Moon Storm's blasts
    that do draw nothing in the game). Reason: the Wolf's and Bison decision 16 (attacks_emotes item 3, skills_b Q1).
20. The hero does not travel: Forward Lunge's dust all at the standing hero, Swift Pace's landing ring at the hero 0.1 m
    up, Pillage Plunge's dash in place, Crescent Eclipse in place (the centre at the hero, its dive from `{"d": -5, "y":
    5.447}` as tto's corrected block). Reason: Penguin decision 8, Bat decisions 8 / 10 (skills_a Q9, skills_b Q2, tto Q4).
21. Heart Ripper's stab sparks at the hero 1 m up; Finishing Blow's hits at the hero. Reason: the game puts the Cat at the
    knocked-out target, so the target comes to the standing hero (skills_a item 6, Q1).
22. Double Down's eight strikes: each a coin flip between the 10 m target and the Cat herself (rolls `dd1-8`), as the
    game's FindAreaTarget with one target. Reason: random picks as the game makes them (skills_a item 7, Q2). Its later
    strikes show in the default play-once mode; the loop toggle cuts them (skills_a verification 1: a page-wide limit,
    noted for the editor).
23. The ray skills' hits (Lucky Card, Flying Dagger, Disarm, Bleed) at the ray's point on the target body's front,
    `{"d": 9.7, "y": 0.62}`, the fire effects pitched `rot [3.43, 0, 0]`; Flying Dagger's side knives hit nothing. Two
    Pair's and Copycat's hits at the target's feet + 0.5 / + 1 m (`d 10`). Reason: Bat decision 4, Penguin decision 3
    (skills_b items 5-6, Q9).
24. Copycat's success shows on every play. Reason: the skill's look; the failure only prints a message (skills_b Q4).
25. Support Fire's shells fly the game's arcs and land 18-26 m ahead (never at the target: the game aims them straight
    ahead). Reason: the barrage is the skill (parts Q1); the camera may pull back if the editor finds the tile empty.
26. Casino Doom's `doom` (the Bat's effect, on the Cat herself) at the Cat's collider centre, **y 0.89** (Cat.prefab's
    CharacterController, effect_only's verification), not skills_a's 0.6 approximation (its verification 2).
27. Awareness' Insight mark and Damage Roulette at the Cat's own heights: the roulette 0.89 m up, the mark's root 1.69 m.
    Reason: the game's numbers (effect_only Q2); if the QA shot shows the mark floating too high, `y` about 1.3 with the
    reason in `why`.
28. Delta Strike: no teleport (its triangle cut from where she stands, + 0.5 forward), scale 1.5 at sLv 2, its two cats at
    (+-4.5, 0, 8). Reason: the caller passes her own position (skills_a item 6, verified).
29. Grand Casino Arcade and Backflip do not turn the Cat (to the camera / away from the target). Reason: every in-place
    skill plays in her own facing (skills_a Q7).
30. Royal Flush: the target 10 m ahead is the centre; the cards' fan, table, banner, bursts and sword there (tto block).

## Passives, ranks, rolls, voices
31. Passives on, max rank: Lady Luck #412 (Fate Draw: ladyLuck_ring + ladyLuck1|ladyLuck2), Roll the Dice #432 (Double
    Down: doubleDown2_hit), Even Odds #422 (decision 11), Double Focus #411 (decision 3), Insight #421 (folded into
    Awareness), Joker #402 (Lucky Card: nothing drawn), Fate Draw 4, Awareness 2, Damage Roulette 2, Nine Lives 2, the rest
    rank 2 (skills_a item 5, effect_only).
32. Grand Casino Arcade's luck at the 255 cap: per spin Doom 5, 111 45, 222 40, 333 30, 777 135 of 255 (rolls
    `casino1-5`). Reason: the only setting where every outcome shows (at LCK 1 every spin is a numberless Doom) (skills_a
    Q3). The gambles keep lckAdjust(50) = 50 % at LCK 1 (the Wolf's Double Art convention) (skills_a Q5).
33. Finishing Blow's voice is TTO's `finisingBlow1|finisingBlow2` (BB loads `finishingBlow1 / 2`, which its data lacks).
    Reason: Sheep decision 10 (skills_a item 8, Q8).
34. Awareness keeps BB's `awareness1|awareness2` (TTO's `inSight1|2` with Insight is a behaviour change, not a fix);
    Lucky Dice keeps BB's `luckyDice1|luckyDice2` (TTO's `rollTheDice1|2` likewise). Reason: Sheep decision 10 takes TTO's
    voice only where BB's file is missing (effect_only Q1, skills_b Q3).
35. Awareness' voice and every proc tile play on every play (no 3 s voice timer, no cooldowns). Reason: the Penguin's
    choice, the Frost Spike precedent (effect_only).
36. Damage Roulette's 12 s status cut at 10 s (`kill` 10 from 0.2 s); the Insight mark keeps its 3 s. Reason: the 10 s
    rule (effect_only Q6).
37. The charge's hand glow `damagePlus` on `mount_Hand_R`, `kill` 10, with the new cue option `"single": true`: while a
    copy from an earlier play lives, no second copy is spawned and **the live copy's kill is renewed** (its killAt = its
    age + the cue's kill). Reason: the 12 s status cut at 10 s (parts Q6); the game's one glow (Cat.cs:20045) kept alive
    by every charge (attacks_emotes verification 2 wins over the plain skip of Q2).
38. `damagePlus_ring` on every tick (also when full) and the rings / glow shown, though the game draws them only in
    missions / arena (`mGameType > 4`). Reason: the Sheep / Penguin / Wolf precedent (attacks_emotes item 4).
39. Royal Flush always deals the Royal Flush hand (hand 9: the sword, all five bursts, cheer + finalMove1|finalMove2), one
    random suit per play for all five cards, ranks 1-5. Reason: the only hand that shows every effect, as decision 32's
    luck cap (tto Q2, Q3); the game's weighted hand odds would need a weighted pool the page has not.
40. Drop Anchor's chain-break shrapnel at `p` 0.25 (lckAdjust(25) at LCK 1). Reason: random picks as the game, at the
    stat-free wardrobe's LCK 1 (tto Q7), as decision 32's gambles.
41. Crescent Eclipse's eight blades are copies of the Cat's worn main-hand weapon at x 1.5 (`HoldWeapon`), the prefab's
    own blade when none is worn. Reason: the game's look (tto Q5); a tile following the worn weapon as Penguin decision 18.
42. TTO1102's code with the 2026-11-04 bundles (clips at speed 1), not TTO1109's 1.6.2.4 timings. Reason: Bat decision 44;
    the code matches these bundles' prefabs; this PC has no 1109 bundles (tto Q1). The 1109 variant is offered.

## Left out
43. Camera effects (Moon Blade / Moon Storm motion blur, Support Fire's shake, Awareness' barrierMask warp, Grand Casino
    Arcade's zoom / blur, TTO's Row6Shake and redRamp). Reason: the Penguin's Dispell, Bison decision 35 (skills_b item 9,
    effect_only Q7, tto Q8).
44. Status looks on a foe (cut, pillage, disarm, bleed, Joker's doom, eclipsed, dropAnchor_chain, paralysis,
    crescentEclipse_rupture) and Open Wound's red ramp; the hero's status tints. Reason: Sheep decision 4, Bat decisions 13
    / 44, Penguin decision 10. They are still built (in SKILL_FX) as the Wolf's left-out ones.
45. Hidden Blade / Jagged Knife and Backstab get no tiles (drawn only at a target the melee boxes never reach); dead code
    `RPC_luckyDice_hit` is not cued; the DamagePlus text, the status icons, Support Fire's SP model. Reason: effect_only
    Q8, skills_b item 10, attacks_emotes "Left out".

## Parts and looks (every missing part is built)
46. StatusControl draws nothing: `BUILT` += `StatusControl` (data only, the cue's `kill` is its life), no page code
    (attacks_emotes part 1, parts part 7).
47. `hideProp`, a new cue kind `[t, "hideProp", "R", {"kill": s}]`: the worn right-hand weapon's meshes hidden from t for s
    seconds (its weapon_fx particles keep drawing, as the game disables only the MeshRenderers); index.html's preload and
    fxDue skip it, `wardrobe_fx_check.py` KINDS gains it. Reason: as the game (skills_b Q7, verification 2).
48. Support Fire's barrage is built the parts researcher's way, all in `fxparts/cat.js` (`fx:supportFire_cannon`: the six
    cannons of one play registered by `api.FX.gen`, the first owns the clock; from age 1.25, every `0.01 x randInt(24,
    35)` s a random living cannon rewinds and plays `fire`, the muzzle spawns `supportFire_smoke` + `supportFire_fire` at
    `getTrajectoryVector`'s pitch for `24 + randInt(0, 23)` m; at the cut every cannon's AlphaTimer `fadeOut(0.5)`), not
    skills_b's `volley` / `fadeOut` / `i` cue options. Reason: one owner file and no new cue options; parts.md's cue
    shapes are the parts' contract. The cues: the ring `{"cut": 2.95}` and six cannons `{"x": X, "d": -2, "cut": 2.95}`,
    X = -7.5 ... 7.5, the entry's `"builds": ["supportFire_fire", "supportFire_smoke", "supportFire_hit"]`.
49. `Cat_supportFire`: 30 m/s along its spawn rotation, gravity -9.8 on the 0.02 s step, turned along its flight, on the
    floor `api.spawn("supportFire_hit")` at the point under it (identity) and destroyed; life 10 (parts part 3).
50. Grand Casino Arcade's machine: `Cat_grandCasinoArcade` blinks materials [1] / [2] (`0.15 sin(4 T)` and its
    counter-phase, the page's absolute clock); `fx:grandCasinoArcade` plays the clips the cue's `anims` option lists
    (`[[1.3, "fire"], [4.0, "fire"], [6.7, "fire"], [9.4, "fire"], [12.1, "fire"], [14.5, "destroy"]]`, skills_a's block)
    on node 1's Animation, and at age 15.5 (the standby) sets `fx.cutAt = -Infinity` so the followState end runs; the
    cue carries no `cut`. Reason: parts verification 1 (a cue's cut is read on the playing step's clock), with the times
    kept in the cue file beside their sources (skills_a) rather than fixed in the part.
51. mesh.js's Animation part is built also when its `play` is off (no pose until a part calls `play()`) and gains
    `rewind()`; alphatimer.js's emitter gains `fadeOut(sec)` (AlphaTimerFadeOut: Max -> Min over sec from now). Reason:
    the cannons are invisible / still without them (parts part 4).
52. `Transparent/AdditiveAlpha` (the shell: lit pass with alpha test >= `_AdditiveRange`, then an additive pass with
    <= it) is a generic page shader (`api.shader`), the extractor saving the material's `cut`; the Mole will reuse it.
    Reason: parts part 3.
53. WorldParticleCollider: the extractor keeps its fields; legacyParticles gains a `collide` hook; the part bounces a
    particle off the floor (y 0) with the **whole velocity x bounceFactor** (0.5), energy minus the loss, killed under
    minKillVelocity, only when the mask holds layer 0. Reason: BB's component's own meaning, the 3.5 manual (parts Q4;
    TTO's normal-only conversion differs only in the skid). luckyDice and treasureHunt; Chameleon / Rabbit reuse it.
54. supportFire_hit's Shuriken burst by the graft: `SHURIKEN_FROM_TTO["cat"] = ["supportFire_hit"]` with BB's `Bomb2`
    material. Reason: the Bison's design, proven field for field here (parts Q5, part 6); a native 3.5 read later if a
    class's BB system has no TTO copy.
55. `doom` for the Cat by an alias: `ALIASES["cat"] = {"doom": "gameassets/characters/heroes/bat/effects/doom"}` (one
    effect, not the whole Bat folder) (skills_a part 3).
56. `BUILTIN_BLEND` 205 / 206 / 207 are now certain (TTO's re-serialised copies name the shaders): a line in its comment
    (parts "Read this first" 4).
57. TTO's parts are built (tto section 6 with its verification): `Cat_royalCard`, `Cat_royalHandBanner`, `Cat_eclipseFx`
    (moon and blade modes), the code movers `Cat.RoyalSwordFall` and `Cat.DropAnchorFlight` (CODE_MOVERS), the latter
    holding the inactive `Leash` node's two RingEmitters back until the landing (verification 3: taken out of
    `fx.emitters` at build, node 2 hidden, put back with a fresh clock at the landing), `Unlit/Color` and `Unlit/Texture`,
    the cel shader's fresnel term (`_FresnelBrightness`, the Penguin's `dxbc_cel.txt` formula: it reaches the other
    classes' cel materials too, NOTES.md says so), and the TTO exporter's blends `Legacy Shaders/Particles/Multiply`,
    `Multiply (Double)`, `Alpha Blended Premultiply` -> multiply / multiply2 / premul. `SKILL_FX["cat"]` = the 26 cued
    prefabs plus the left-out ones (eclipsed, dealersMark, dropAnchor_chain, crescentEclipse_rupture).
58. The new cue options `single`, `anims` (Cat) and `flip`, `pulse`, `gather`, `gatherTo`, `hand`, `eclipse`, `recall`,
    `home` (TTO) go into `wardrobe_fx_check.py`'s OPTS and the cue-format comment in index.html.
59. The inventory's `BUILT` += StatusControl, Cat_grandCasinoArcade, Cat_supportFire, WorldParticleCollider (UVScroll is
    in); ParticleSystem / ParticleSystemRenderer only once every BB system is covered; rerun it (the recipe's rule).
60. Every report's corrected paste-ready block is the one to paste (verification sections: skills_b's supportFire1 with
    decision 48's cue shapes, tto's crescentEclipse2, parts' grandCasinoArcade without `cut`, attacks_emotes' blocks as
    written), merged where two reports touch the same SEQ / SEQ_SKILL line.

## Offered to the user for the Bible (not written there)
The combo's fixed starts (0.6 / 1.2 / 1.7 s), press windows, voice / swing / dust times; the charge's loop at 0.5 s, ticks
at 1 / 2 / 3 s (full on the third with Double Focus), the always-true ring test and the hand glow lasting as the status;
activateIcon1's battle loop; Delta Strike does not teleport; Double Down can strike the Cat herself; BB's Finishing Blow
and Nine Lives are silent (TTO fixed both names); Lady Luck also changes Fate Draw's voices; Casino Doom shows no number;
Grand Casino Arcade's spin / result times and its TTO copy's dead sign light; Moon Storm's two blasts, Moon Blade's circle
times; Pillage Plunge's 4.8 m dash; the five throws hide the weapon; Swift Pace keeps her facing; Support Fire's first shell
at 1.25 s, shells landing 18-26 m ahead whatever the target, the 0.5 s cannon fade; `RPC_luckyDice_hit` dead, BB's unused
rollTheDice / jokerCard / inSight voices (TTO plays them); TTO dropped the coins' bounce; the TTO skills' timelines (Royal
Flush, Crescent Eclipse, Drop Anchor) and shikifujin never played.
