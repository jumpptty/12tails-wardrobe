# Chameleon effects: decisions (2026-11-13), decided overnight, for the user's review

The user was asleep, so the planner decided every open question in the six reports in this folder (attacks_emotes,
skills_a, skills_b, effect_only, parts, tto), each read with its "## Verification" (the verification wins where the two
differ). Rules used, in this order: the standing rules (top rank, passives on; random picks as the game makes them;
enemy effects at the 10 m target point; homing aims 0.6 m up; target-rotation effects rot [0, 180, 0]; long buffs /
fields cut at 10 s; a tile per skill, pool members one each, effect-only tiles on the idle stance; missing parts always
built; TTO cues only for the released `apexHunt`, `chainLightning`, `venomPhantom1`, `venomPhantom2`, `venomPhantom3`),
the page's SEQ rule (index.html above SEQ: "a charge = full charge, a channel = its duration, or three hits (at least
3 s) when it runs until the player moves"; the user's "assume high INT, no cast bar"), then the Wolf's, Sheep's,
Penguin's, Bat's, Bison's and Cat's decisions by analogy, then the reports' own recommendations. Every item is
**decided overnight, for the user's review**: any of them can be turned round in the morning.

Already in the tree from the Cat's / Bison's / Bat's builds (checked 2026-11-13; nothing to rebuild for the Chameleon):
the `hideProp` cue kind for a prop slot (HeroPropHide; no `kill` = until the next pick), WorldParticleCollider
(`fxparts/worldcollider.js` + the `collide` hook; generic, bounce 0 needs nothing new), Transparent/AdditiveAlpha
(`fxparts/additivealpha.js` through api.shader, which mesh.js's SkinnedMeshRenderer reaches too) and its extractor `cut`,
the `"lift"` kind (LIFTS / HeroLift), the `"skin"` / `"clone"` kinds, `worn` / `notWorn`, `everyCycle`, `single`, the
entry's `"builds"`, `api.spawn` with `followNode` / `local`, the Shuriken graft (by node path, one material per class),
tto_sheep.js's LineRenderer (`driven`), the `"sound"` cue's rip-wide fallback.

## Tiles and sequences
1. Charge Attack: `"Charge Attack: cAttack1 cAttack2*@9 cAttack3*@3.4 cAttack4"` (cAttack4 at the 18th swing, 3.4 s, not
   3.6). Reason: the code's clip change at swing 2n - 1 (attacks_emotes item 1, verified); full charge by the SEQ rule.
2. The first step keeps the page's 0.2 s fade (nAttack1, cAttack1 are cuts in the game). Reason: Bat decision 28, Cat
   decision 2.
3. The Normal Attack tile stays one shot (the วนซ้ำ toggle repeats it), voice `nAttack1` on every play. Reason: each
   tile play is a fresh shot from idle, as the Penguin's MP Transfer (attacks_emotes Q2, Q3).
4. Quick Fire `"quickFire1@0.6 quickFire2*@1.7 quickFire3"`; Slayer `"slayer1@1 slayer2*~@0.1 slayer3~"`; All Slayer
   `"allSlayer1 allSlayer2*@0.1 allSlayer3"`; Thunder Dragon unchanged. Reason: the coroutines' fixed starts and the cast
   bar's 0.1 s floor, as the Bat's Guardian (skills_b item 1, skills_a Q1, verified).
5. Tent gets its own sequence `"Tent: cast1 cast2*@0 cast3~@0.4 sleep*~0.5@0.7"` (keys `@Tent:cast3`, `@Tent:sleep`).
   Reason: one tile per skill; `~0.5` is the game's own 0.5 s crossfade (skills_a verification 1); high INT, so the
   0.7 s sleep (skills_a Q4).
6. Immunity, Venom Shock, Blood Burn, Rusty Decay get one-step tiles `"<Name>: cast3"` (keys `@<Name>:cast3`). Reason:
   they play cast3 with no channel, as the Sheep's Seal / Eden Sanctuary (Sheep decision 17; skills_a Q3).
7. The Cast tile keeps `cast2*@0`; its pool `cast3` has five members (True Invisibility, Mass Invisibility, Final
   Entrapment, Camp Fire, Mark of Slayer), one tile each. Reason: every class's Cast tile (skills_a Q2); one tile per
   member.
8. Slayer (`slayer1-3`) and All Slayer (`allSlayer2`, `allSlayer3`) are pools of four members each (Bug / Tail /
   Elemental / Machine), one tile per member through poolChains, the pick kept across the steps. Reason: one tile per
   skill (skills_a item 1, skills_b item 2).
9. Torment Rain gets the new tile `"Torment Rain: rainOfArrow@2.7"`. Reason: the rain lands 2.0-2.6 s into a 2.0 s clip;
   a cue at the clip's end would be lost to the restart (skills_b Q1).
10. Venom Phantom: `"Venom Phantom: venomPhantom1@0.3 venomPhantom2^@0.22 venomPhantom2^@0.22 venomPhantom2^@0.22
    venomPhantom2^@0.22 venomPhantom2^@0.22 venomPhantom3^"`, the game's 0.05 s shot crossfade written as `^` (0.1 s),
    no new token. Reason: the coroutine's five shots at 0.3 + 0.22 i (tto item 1, verified); tto Q1.
11. Apex Hunt and Chain Lightning stay single clips (no SEQ, no cast bar); Chain Lightning's cues run on past the 0.9 s
    clip in the idle tail (they show in the default play-once mode; the loop toggle cuts them, a page-wide limit). Reason:
    Bison decision 15, Cat decision 22's note.
12. **Critical Plus** gets its own tile `"Critical Plus: nAttack1"` (key `@CriticalPlus:nAttack1`: the nAttack1 cues with
    `criticalPlus_hit` at the hit on every play), **and** rolls `p 0.2` beside every arrow hit in nAttack1, Left Stride
    and Clear Arrow. Reason: the standing "every skill gets its own tile" with the Cat's Even Odds shape (Cat decision 11:
    own tile plus the roll in the hosts); effect_only Q1 and its verification 2.
13. **Clear Arrow** gets its own tile `"Clear Arrow: nAttack1"` (key `@ClearArrow:nAttack1`): the nAttack1 cues with
    `clearArrow` in place of `nAttack`, the hero in the `FX/Invisible` skin (no kill: until the next pick, the state the
    skill needs), the hand arrow hidden with no kill (the game shows it again only when she is not invisible). Reason:
    one tile per skill; the precondition shown, as Torment Rain's cage (decision 26) and the Snow Ball precedent
    (effect_only Q2).
14. SEQ_SKILL `chameleon: { "@Immunity": "immunity", "@VenomShock": "venomShock", "@BloodBurn": "bloodBurn",
    "@RustyDecay": "rustyDecay", "@Tent": "tent", "@CriticalPlus": "criticalPlus", "@ClearArrow": "clearArrow" }`;
    `wardrobe_skill_icons.py` `CLIP_SKILLS["chameleon"] = {"backStep": ["perfectBlend"], "cast4": ["fatalStrike"],
    "rainOfArrow": ["tormentRain"]}` and `OWN_TILE["chameleon"] = {"immunity": ["cast3"], "venomShock": ["cast3"],
    "bloodBurn": ["cast3"], "rustyDecay": ["cast3"], "tent": ["cast3", "sleep"], "criticalPlus": ["nAttack1"],
    "clearArrow": ["nAttack1"]}`; no EFFECT_ONLY entry. Reason: the Sheep's seal and the Cat's Even Odds / Nine Lives
    shapes; every icon is in the Bible (skills_a item 2, skills_b item 3, effect_only).
15. No effect-only (`root@t`) tile: every Chameleon skill has a body clip (effect_only item 1, verified).
16. Focus Fire (`focusFire1` / `focusFire2`, played by no BB or TTO code, no card) is hidden: its SEQ line goes and
    `NEVER_PLAYED.chameleon = ["focusFire1", "focusFire2"]`. Reason: the Wolf's cast1-3 ("Remove the tile"), Bison
    decision 9, Cat decision 14 (overrules skills_a Q14's "keep a plain move"); mentioned to the user in case he wants it.
    NOTES.md:98 calls it "TTO-only": the editor corrects that line.
17. Silent Walk keeps its looped tile with the charge's look: `FX/Blend` skin `kill 1.6` (the page's hold, whole 0.8 s
    cycles) and `cAttack_ring1` at 0 and 1 s. Reason: the game plays the clip only under the charge's blend (attacks_emotes
    Q5 and its verification 1; skills_b verification 2: FX/Blend, not FX/Invisible).
18. cast2 alone, activateIcon1 (the mission channel) and RPC_cAttack0 (the early release): no tile, no cue. Reason: Penguin
    decision 19 (attacks_emotes item 8, Q9).
19. KO: `deadEffect` on half the plays, no voice (BB's ko / dead / revive voices are missing and TTO has no fix); getUp
    silent. Reason: Sheep decision 11; Cat decision 17 needs a revive voice the Chameleon lacks (attacks_emotes item 6).
20. Emotes: BB's hi, wave, ty, bow, cheer, cry, sleep and chat1-5; TTO-only emote clips and the voiceless emotes stay
    silent. Reason: Bat decision 36 (attacks_emotes items 7, Q8).
21. The run's footsteps `step_light2` at 0.1 s and `step_light3` at 0.4 s of every cycle (`"sound"`, `"everyCycle": true`).
    Reason: the clip's AnimationEvents, as the Bat's wing flap (attacks_emotes item 5).

## Where things land
22. Normal Attack: the arrow from hero + (0, 1.5, 0) + forward aimed at the 10 m ground point (pitch 9.4623), 40 m/s,
    `nAttack_hit` at 0.4281 s at d 10 (and Critical Plus' roll there, `[0.4281, "fx", "criticalPlus_hit", {"d": 10, "p":
    0.2}]`). Reason: Bat decision 1, Penguin decision 1 (attacks_emotes Q1; parts verification 1; effect_only
    verification 1).
23. Arrows cued with `to` (Left Stride, Right Stride's clone shots, Quick Fire is a ray) end when their trigger box front
    (1.75 m ahead of the origin) meets the standard target body, the hits at the box contact: Left Stride's hero arrows
    shot + 0.174 s at (x -0.04, y 0.67, d 9.7), the clone's at x 0.24 / 0.3. Reason: the game's OnTriggerEnter (skills_a
    verification 2, the block to paste); Bat decision 4's body.
24. Quick Fire's 18 hit flashes at the ray's contact `{"d": 9.7, "y": 0.63}`. Reason: the enemy-at-target rule (skills_b
    Q7).
25. Needle Prison at the target's feet 10 m ahead, 16 needles on its 0.6 m ring, `kill 5` (getDebuff(3) + 2 with Mass
    House Lock). Reason: the skill's own look at the target point (parts verification 2).
26. Torment Rain shows the Final Entrapment cage it needs at the target from 0 (`{"d": 10, "kill": 2.7}`), the rain into
    it at 2.0 s. Reason: the precondition shown, the Snow Ball / seal-field precedent (skills_b Q1).
27. Venom Shock's and Rusty Decay's detonations, All Slain's bolts, All Slayer's / Slayer's eyes and hits, Mark of
    Slayer's hit: at the 10 m target (0.6 m up where the game uses the bounds centre), the hero's rotation where the game
    gives it. Reason: the target stands for a fitting foe (skills_a Q5).
28. Mass Shot draws no hits (its 9 m edge reach misses the 10 m target); Zero Shot's and Thunder Dragon's 3-6 m boxes
    likewise. Reason: the Penguin's Mana Arc, Bison decision 16 (skills_a Q6, skills_b item 7).
29. The hero does not travel: Perfect Blend's hop, Skin Shift's hop, Zero Shot's hop and the volley's push, Left / Right
    Stride's run: every effect at the standing hero. Reason: Penguin decision 8, Cat decision 20 (skills_a Q7, skills_b
    Q5, attacks_emotes Q7).
30. The Double Strider clone does move: `doubleStrider_left` / `doubleStrider_right` turn to face `to` [0, 0, 10] on the
    flat and strafe along their own right at **5.02 m/s** (+ left, - right), their shots cued from the clone's worked-out
    spots (skills_a's table for Left Stride, skills_b verification 4's table for Right Stride). Reason: the game's code
    moves the effect itself (skills_b Q2); runSpeed 4.02 at the page's stats + 1 (CharacterDataClass.cs:979; skills_a
    Q8, skills_b verification 4, overruling skills_b Q9's 5 + 1).
31. Camp Fire 2 at the ground 2 m ahead, `Euler(270, 90, 0)`, `kill 10` (30 s cut). Reason: getSpawnPos and the 10 s rule
    (skills_a "cast3", parts part 9).
32. Final Entrapment's cage at the 10 m target with `life 7` (the code's chaAdjust(7), the prefab's 6). Reason: build the
    tiny cue option (skills_a Q11, parts Interfaces 4).
33. Immunity's look at the hero y 1.16, scale 0.7, `kill 10`; Fatal Strike's two hand looks on `mount_Hand_L` /
    `mount_Hand_R`, `kill 10`, their world-identity turn APPROXIMATED by the bone's local identity (a 0.1 m sphere of
    blood with no velocity: the same look). Reason: the code's numbers (skills_a verification), the 10 s rule.
34. Apex Hunt **lifts the hero** along the game's 4.5 m jump (LIFTS `apexHunt` from 0.22 s, tto verification 2's curve),
    the cues relative to the lifted hero (the lock y -3.9, the arrow's `to` [0, -3.933, 10], the impact y -4.48, loose /
    arrow `rot [27.81, 1.42, 0]`). Reason: Bison decision 22 (Titan Drop lifted in place "because the leap is the skill's
    whole look"), the closer precedent than tto Q3's in-place answer (tto verification 2).
35. Apex Hunt's lock reticle `preyFx` at the target body (lockOnly, released 1.8 s after its 0.55 s spawn, gone 0.25 s
    later), gold. Reason: the skill's own lock marker, not a status (tto Q4; parts verification 6).
36. Venom Phantom with the lone target: five ghosts at the GhostSlots, a beam from each, the rupture at the target
    shattering every ghost. Reason: the standing lone target (tto Q2).
37. Chain Lightning's tail kept whole to 12.05 s (stormCharge 8 s, then staticDrain 4 s, each under 10 s). Reason: the
    10 s cut is per buff, and the slow's look ends the skill (tto Q6; Cat decision 4's reading of the rule).

## Passives, ranks, rolls, voices
38. Passives on, max rank: Bow Mastery #401 (arrows 40 m/s), Far Reach 4 (0.8 s life), Critical Plus 4 (20 %), Erase
    Senses #412 (Perfect Blend 8 s, True Invisibility 16 s), Mass House Lock #422 (massLock_ring, massHouseShot, Needle
    Prison + 2 s), Extra Arrows #403, Double Strider #423, Improved Slayer 4 (All Slayer bar, the slayer fire scale 1.4),
    Skin Shift #421, Silent Walk #411, Charge Attack 3 (n = 9), the ranks of skills_a "Passives". Reason: the standing rule.
39. Voices with TTO's fixes where BB's file is missing: True Invisibility `invisible1|invisible2`, All Slayer
    `allBugSlayer` / `allTailSlayer` / `allElementalSlayer` / `allMachineSlayer` (unnumbered), Torment Rain
    `tormenrRain1|tormenrRain2`; Immunity and Thunder Dragon stay silent (no file in either game). Reason: Sheep decision
    10 (skills_a item 3, skills_b items 4-5).
40. Hero-played sounds as `"sound"` cues: `bow_fire1` on every shot (`plunger` with the Plunger Bow: `worn` / `notWorn
    ["R", "plungerBow"]`), `cAttack_bow`, `quickFire`, `rightStride_fire1|2`. Reason: Bat decision 15's weapon options
    (attacks_emotes Q6).
41. Durations at CHA 1 (chaAdjust): True Invisibility 16 -> 10, Mass Invisibility 12 -> 10, Immunity 12 -> 10, Fatal
    Strike 12 -> 10, Camp Fire 30 -> 10, Perfect Blend 8, Needle Prison 5, the cage 7. Reason: the 10 s rule.
42. Every effect and look the game gates on `mGameType > 4` (the blend puff and status of the charge, the rings) is shown.
    Reason: the Sheep / Penguin / Cat precedent (Cat decision 38).
43. Fatal Strike's blood trail on the arrows: not on the Combo tile (the status is not held there); the arrow part still
    builds the `fatal` option. Reason: parts Q5; every missing part built.
44. TTO1102's code with the 2026-11-04 bundles (no TTO1109 timings). Reason: Bat decision 44, Cat decision 42.

## Hero looks
45. The invisibility and blend looks are the own-team view (the player's own Chameleon): `HERO_SKINS["FX/Blend"]` (the
    texture at 35 % + a (0.8, 0.8, 0.3, 0.5) shell pushed by 0.002) and `HERO_SKINS["FX/Invisible"]` (35 % + a (0.3, 0.6,
    1, 0.75) shell pushed by 0.003), the ghost drawn before the shell, Cull Back; every page mesh taken as Diffuse
    (APPROXIMATED as CosmicRift's). The enemy view (FX/Camaflage, or hidden with Erase Senses) is not drawn. Reason: parts
    Q4, attacks_emotes Q4; Penguin decision 16's hero-skin kind.
46. The FX/Invisible look comes 0.2 s after the `invisible` status, with the `invisible` puff at the status time; the blend
    look at once. Reason: CharacterControl's Block_989 Yield 0.2 (parts part 10, skills_a verification).
47. Chain Lightning darkens the hero: `HERO_SKINS["Chameleon.StormDarken"]` (every hero renderer, props too, to (0.07,
    0.07, 0.09) by clamp01(4 t), held, back over 0.6 s ending at `kill`). Reason: the skill's main look, Penguin decision
    16 (tto Q8).
48. The arrow in hand: `hideProp "L"` (the second piece, the arrow, mWep2) in every shot coroutine, never `"R"`, with the
    new option `"all": true` that hides the piece's weapon_fx particles too (the Chameleon's code switches off every
    Renderer under mWep2, unlike the Cat's MeshRenderers). After a cast-bar skill (cast1) it stays hidden until the next
    pick (no `kill`). Reason: ChameleonEquipment.cs:1646-1715 (skills_b verification 1, skills_a item 5-6, parts Q8;
    attacks_emotes P2).
49. Thunder Dragon hides the whole hero 0.6-3.8 s, her props and their particles too: `[0.6, "hideProp", "hero", {"kill":
    3.2}]`, wired to the page's heroHide. Reason: she becomes the dragon skeleton (skills_b Q3, verification 3).
50. The flying arrow is a fresh copy of the worn second piece (slot L; slot R `snookerBall` with the Snooker set), its own
    weapon_fx particles included; nothing worn: the starter `noviceArrow` (w_chm1) for the projectile only (the hand stays
    empty). Reason: the game copies the whole piece and always holds one (parts Q1, attacks_emotes P1 / Q6, Penguin
    decision 18's worn-weapon variants).
51. Clear Arrow's arrow: the worn arrow's root mesh in the FX/Invisible effect material (35 % white + blue rim), the own-team
    view. Reason: parts Q7.

## Left out
52. Camera effects (motion blurs, AutoZoom, colour ramps venomRamp / rustyRamp, every shake, Row6Shake). Reason: Bison
    decision 35, Cat decision 43.
53. Status looks on a foe (poison, phantomVenom, the 12 s Prey status, stormCharge's fork / chain arrows on other tiles)
    and Tent's zzz emote; Apex Hunt's kill reward (`apexHunt_trophy` + `allSlain_ring`, needs a kill). They are still
    built (SKILL_FX). Reason: Sheep decision 4, Cat decision 44 (tto Q5, Q7, skills_a Q12).
54. Dead prefabs no code loads (`cAttack`, `cAttack_effect`, `quickFire_hit`, `poisonArrow`, `poisonArrow_ring`), the
    supplement skills (`sup_*`). Reason: parts item 2, effect_only Q3.

## Parts and data (every missing part is built)
55. `Chameleon_nAttack` (`nAttack`, `clearArrow`): 40 m/s along the spawn rotation (`fx.at.speed` overrides), 0.8 s life,
    the end on the floor (root y 0) or, with `to`, at the trigger box's contact with the target body; the arrow copy by
    `api.propModel` at local Euler(0, 270, 270); Fatal Strike's child with `local.rot` = the inverse of the arrow's spawn
    turn and `pos` scaled by the copy's scale. Reason: parts part 1 with its verification 1 and 3.
56. `Chameleon_needlePrison` (16 needles, 0.05 s apart, 67.5 degrees each, r 0.6 = `fx.at.r`), `Chameleon_campFire`
    (layout only, draws nothing), `"builds": ["needlePrison_arrow"]`. Reason: parts parts 2 and 9.
57. Self-Illumin/DoubleTexture (texture squared, opaque) and FX/Invisible on an effect mesh, as api.shader materials in
    new part files (mesh.js keeps its owner and is not edited: its `shader:` fallback reaches api.shaders). Reason: parts
    parts 3 and 5; one owner per file.
58. The Shuriken graft for `thunderDragon_ring2` and `zeroShot_ring` matches BB and TTO nodes by (node name, the PSR's
    first material without `tto_`), the next unused on a tie, and keeps BB's own PSR materials per node (no
    `SHURIKEN_MAT["chameleon"]`); the Bison's and Cat's grafts must build byte for byte as before. Reason: parts part 7 and
    its verification 4 (repeated node names, four materials).
59. TTO's parts: ChameleonLightning, ChameleonAfterimage + `TTO/ChameleonSpirit` (a faithful port: wisps, rim, triplanar
    scales, the depth prepass; `scaleTex` from the extractor), ChameleonPreyReticle (with `release`, feet = root y - 0.6),
    the `Chameleon.ApexArrow` code mover (spawn to `to` in 0.12 s, `to` hero-relative at the spawn so it works under the
    lift). The ghost reads tto.md section 7's options (`bow`, `face`, `slide`, `slots`; `ghost: k` on a beam;
    `shatterGhosts` on the rupture), not parts T2's per-ghost lists. Reason: parts T1-T3 and verification 5-7, tto Q10.
60. Page options: the cue `life` (root EffectControl life), `stop` (seconds after the spawn: every Shuriken system stops
    emitting), a followState `cut` at or after its step's end applied at the step change (venomPhantom_coil), the
    `fx:castRing` hook for the Chameleon (bat.js, one line). Reason: tto P7 / P8, parts part 8 and Interfaces 4.
61. `SKILL_FX["chameleon"]` in wardrobe_fx_tto.py is the 31 names of tto verification 1 (required: `"builds"` does not
    build `tto/` names); the inventory's `BUILT` += `Chameleon_nAttack`, `Chameleon_needlePrison`, `Chameleon_campFire`;
    rerun it. Reason: tto verification 1, the recipe's rule.
62. The new cue kind / options (`hideProp` `"hero"` and `all`, `strafe`, `speed`, `fatal`, `life`, `stop`, `r`, `bow`,
    `face`, `slide`, `slots`, `ghost`, `shatterGhosts`, `lockOnly`, `release`) go into `wardrobe_fx_check.py`'s OPTS and
    the cue-format comment in index.html. Reason: Cat decision 58.
63. The paste-ready blocks to use are the corrected ones (verification sections win): attacks_emotes' (silentWalk from
    its verification), skills_a's (Tent's `@Tent:sleep` and leftStride from its verification), skills_b's with every
    `"R"` -> `"L"` (+ `"all": true`), silentWalk dropped in favour of attacks_emotes', Right Stride's clone at 5.02,
    effect_only's corrected crit fragment, parts' corrected nAttack1 / needlePrison (merged into attacks_emotes' and
    skills_a's entries), tto's section 7 with the apexHunt lift block. The editor pastes them after the builders, merged
    where two reports touch one key.

## Offered to the user for the Bible (not written there)
Charge Attack's blend at 0.8 s (not 0.2 s), its rings each second and the full ring at 8.8 s, the volley's swing times and
the cAttack4 change at 0.2 x (2n - 1); the Combo voice rule, the flying arrow being a copy of the worn arrow (the Snooker
ball), the hand arrow hidden 0.2-1.8 s and after any cast-bar skill until the next attack; BB's silent All Slayer, True
Invisibility and Torment Rain (TTO fixed the names), Immunity and Thunder Dragon with no voice in either game, BB's
missing ko / dead / revive voices; Quick Fire's quickFire2 at 0.6 s and quickFire3 at 2.3 s; Slayer's slayer2 at a fixed
1.0 s; Thunder Dragon hiding the hero 0.6-3.8 s; the Double Strider clone circling the other way at runSpeed + 1; Camp
Fire's cached prefab (campFire1 keeps spawning after rank 2 until a relog); Clear Arrow never carrying Fatal Strike's
trail; Needle Prison's 67.5-degree needle order; TTO dropping Torment Rain's ground stick; focusFire1 / 2 and their icons
unused; unused voices (needlePrison3, venomShock3, allSlain3, allSlayer); the TTO skills' timelines (the GhostSlots, the
hang aura's 0.9 s respawn, the storm's near-black darkening).
