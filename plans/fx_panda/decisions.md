# Panda effects: decisions (2026-11-13), decided overnight, for the user's review

The user was away, so the planner decided every open question in the six reports in this folder (attacks_emotes,
skills_a, skills_b, effect_only, parts, tto), each read with its "## Verification" (the verification wins where the two
differ). Rules used, in this order: the standing rules (top rank, passives on; random picks as the game makes them;
enemy effects at the 10 m target point; homing aims 0.6 m up; long buffs / fields / summons cut at 10 s; a tile per
skill with its Bible icon, pool members one each, effect-only tiles on the idle stance; missing parts always built; TTO
cues only for the released `nineDragons`, `tempestDance`, `tempestDanceEnd`, `yinYangFist`, `clap`, `wai`: all four
skill clips are released, `clap` / `wai` have no effects and stay silent), the page's SEQ rule (a charge = full charge,
a channel = its duration, at least 3 s for a hold that runs until the player lets go), then the Wolf's, Sheep's,
Penguin's, Bat's, Bison's, Cat's, Chameleon's and Mole's decisions by analogy, then the reports' own recommendations.
Every item is **decided overnight, for the user's review**: any of them can be turned round in the morning.

Already in the tree (nothing to rebuild for the Panda): the Shuriken `NoiseModule` and `LightsModule` (the Monkey's
build, `shuriken.js:310-327`; parts.md T5 and question 4 answered by it); `hideProp` slot `"hero"`; `single`; `vol` on
sounds; the 4th cue element as a bare number = `d`; `api.spawn`; `api.shader`; `api.pointLight`; tto_sheep.js's
`TrailRendererModern`, `LineRenderer` and lit `Standard`; tto_chameleon.js's `ChameleonLightning` (autoBolt); groundhug.js;
the HERO_SKINS body look (`{ grow, tint }`, the Bison's).

## Tiles and sequences
1. Normal Attack: `"Normal Attack: nAttack1@0.6 nAttack2@0.9 nAttack3@0.9 nAttack4@0.6 nAttack5"` (3.8 s). Reason:
   the stage anchors 0.6 / 1.5 / 2.4 / 3.0 s after stage 1 (attacks_emotes Read this first 1, Verification 1).
2. Charge Attack: `"Charge Attack: cAttack1@0.7 cAttack2*@3 root~@0.2"`, cues keyed `@ChargeAttack:cAttack1|2`. Reason:
   the game's 0.7 s, the SEQ rule's 3 s hold, RPC_cAttack0's CrossFade(root, 0.2) (attacks_emotes Q3, Q4, Verification 5).
3. Raijin Ken: `"Raijin Ken: cAttack1@0.7 cAttack2*@4.3 raijinKen1@1.7 raijinKen2"` (7.5 s), cues keyed
   `@RaijinKen:cAttack1|2`. skills_b's `!` marks are dropped: the first step keeps the page's fade where the game cuts
   in, and a later unmarked step is a cut already. Reason: the 5 s hold (:41896, TTO the same; skills_b Q1); Mole
   decision 1, Cat decision 2 (skills_b Verification 5's reading of the grammar).
4. Ashura: `"Ashura: ashura@1.2 ashuraFist"` (the fist cuts in). Reason: Ashura Fist is Ashura's own sub-state with no
   icon, it exists only under the red form (skills_a Q1; the Chameleon's Tent).
5. Tiger Toss / Climbing Cliff / Crumbling Mountain: `"Tiger Toss: grab@0.2 tigerToss"`, `"Climbing Cliff: grab@0.2
   climbingCliff"`, `"Crumbling Mountain: grab@0.2 crumblingMountain"`; the toss and the climbs assume the grab held.
   Reason: skills_a's form (skills_a / skills_b Verification: it plays the same as `grab^@0.2 tigerToss!`); one tile per
   skill, Climbing Cliff kept although Crumbling Mountain takes over at SP >= 40 (skills_a Q6, Q7); Mole decision 27.
6. Qi Strike: `"Qi Strike: qiStrike1@4 root*~@3 qiStrike2~"`, key `@QiStrike:root`. Reason: with passives on, Delay Qi
   always diverts the charge's end (:23036); the hold 3 s (the SEQ rule; the tooltip's "max 3 sec") (skills_a Q2,
   effect_only Verification 1).
7. Delay Qi gets its own tile with the same steps, `"Delay Qi: qiStrike1@4 root*~@3 qiStrike2~"`; its only own key is
   `@DelayQi:root` (the same three cues as `@QiStrike:root`); its qiStrike1 / qiStrike2 steps fall back to the plain keys.
   Reason: one tile per skill with its Bible icon `panda_delayQi1` (skills_a Verification 1, effect_only Verification 1;
   Chameleon decision 12, Mole decision 3).
8. Fuujin Ken stands as `"Fuujin Ken: fujinKen1 fujinKen2*@8 fujinKen3"`. Reason: the code's 1.0 / 9.0 / 9.7 s (skills_a).
9. Roll Around: `"Roll Around: rollAround*@6"` (each round recasts voice and ring). Reason: the 6 s mRollTimer
   (skills_b Q5; `^` on a first step is not read, Verification 5).
10. Tempest Dance: `"Tempest Dance: tempestDance*@5 tempestDanceEnd^"` (the end's 0.1 s fade). Reason: Row6Begin's
    PlayAnimation(clip, 0.1) (tto Read this first 1, P7, Q5).
11. Effect-only tiles on the idle stance: `"Mystic Sage: root*@1"`, `"Safe Guard: root*@1"` (keys `@MysticSage:root`,
    `@SafeGuard:root`), each the proc alone with no attacker. Reason: procs with no clip, held for the effect's 1 s life
    (effect_only Q4; the Penguin's Frost Spike, the Bison's Berserker Rush).
12. Sacred Sage Technique: `"Sacred Sage Technique: cAttack1@0.7 cAttack2*@3 root~@0.2"`, keys
    `@SacredSageTechnique:cAttack1|2`, voice only (its ring is missing from both games' data). Reason: a passive with its
    own RPC riding the charge's clips (Chameleon decision 12; effect_only Q2, Verification 2).
13. Sacred Sage is not in the plain Charge Attack tile. Reason: it needs SP > 100 and HP below max (effect_only Q3).
14. The `stasisBlow` pool: Stasis Blow and Death Blow, one tile each, even chance on the pool; no CLIP_SKILLS line.
    Reason: one tile per member; the icon script's pool loop gives Death Blow its icon (skills_b Verification 4).
15. Wind & Cloud and Rain & Storm get single-clip tiles (no SEQ line: the clips, 3.6 s and 3.0 s, outlast their 3.3 /
    2.8 s standbys). Their clips are missing from the data because of the `[a-z0-9_]+` filter: fixed now in code,
    rebuilt at home, cued then (decision 52). Reason: BB skills with Bible cards; missing parts are built, never left out
    (effect_only Verification 3, skills_b Verification 1).
16. SEQ_SKILL `panda: { "@QiStrike": "qiStrike", "@RaijinKen": "raijinKen", "@TigerToss": "tigerToss", "@MysticSage":
    "mysticSage", "@SafeGuard": "safeGuard", "@SacredSageTechnique": "sacredSageTechnique", "@DelayQi": "delayQi" }`.
    Reason: the merged entry of skills_a / skills_b / effect_only Verifications (keeps Delay Qi's and Sacred Sage's icons
    off the Qi Strike, Charge Attack and root tiles, moveSkillIcons).
17. Emotes as attacks_emotes' block: wave takes emo_hi's `hi` every play, bow `ty|bow`, talk chat1-5, battle the emote's
    voice; sit, beg, dance, every pose and the TTO emote clips (clap, wai, ...) silent. Reason: the code's voice table and
    the rip's files (attacks_emotes Q7, Verification 2; Bat decision 36).
18. KO: `deadEffect` and dead1|2 on half the plays (`roll dead`), ko1|2 on the other half; getUp silent; the run's
    step_light1 / step_light3 at 0.1 / 0.4 s every cycle. Reason: RPC_dead / RPC_ko; BB's RPC_revive loads no voice
    (attacks_emotes Q6; Sheep decision 11, Mole decision 16).
19. activateIcon1 and the event mode's `f_wtb1`: no tile. Reason: Penguin decision 19.

## Where things land
20. The hero does not travel: the combo's runs, every dash, lunge, step back, roll, steer, Wind Walker's warp. Reason:
    Penguin decision 8, Bison decision 17, Mole decision 28 (attacks_emotes Q2, skills_b Q4).
21. No hit is drawn where the reach misses the 10 m target (the Combo's boxes, Three Steps, Rushing Falcon, Tower Rush,
    Rising Vortex / Dragons, Water Monkey / Crane, Pummel, Qi Strike, Drunken Fist, Ashura Fist, Fuujin Ken within 2 m,
    Wind & Cloud 4 m, Rain & Storm 6 m, Tempest Dance 4.5 / 5.5 m, Yin Yang Fist 7 / 7.5 m); Stasis / Death Blow have no
    hit look at all. Reason: Bison decision 16, Mole decision 29 (tto Q6: as the game does with a foe at 10 m).
22. Raijin Ken's strike at the target's front (0, 0.6, 9.7), facing the hero `rot [0, 180, 0]`. Reason: bounds.center -
    extents.x x dir (:41753-41763), LookRotation(-hitDir) (skills_b Read this first 5).
23. Lotus Palm's flash at (0, 1, 9.7), drawn even on a dodge. Reason: ClosestPointOnBounds(mPos + up) on the standard body
    (skills_a).
24. Heaven Palm's four blasts at the target's feet, d 10, scale 1.5, at **1.2 / 1.8 / 2.2 / 2.6 s** (the nominal times,
    not skills_a's 1/60-late 1.22 ...). Reason: Mole decision 45, one frame model per class, and the Panda's other
    frame-loop test (Lotus Palm's 1.4) is already nominal (skills_a Q8 overruled).
25. Crumbling Mountain's three Crushing Monolith doubles at the 10 m target (d 9.6 / x +-0.4 d 10, facing it); Tiger
    Pounce's splash at d 10 too (skills_b Q2 overruled). Reason: the enemy-at-target rule, and one grabbed target needs
    one spot (skills_a Q4, skills_b Verification 3).
26. Climbing Cliff's and Crumbling Mountain's hit flashes at the hero's `Root` bone + 0.3 m forward at the spawn moment,
    left there: the new cue option `atBone` (decision 41). Reason: the game Instantiates them unparented at Root.position
    (skills_a Q3; riding `bone: "Root"` only as the fallback).
27. Sp Transfer's ally at the 10 m point: the bolt from `{y 0.4, d 0.5}` to `[0, 0.6, 10]`, `kill 0.3`. Reason: the skill
    refuses the Panda herself (Sheep decisions 1, 4's exception; skills_b Q7).
28. Nine Dragons: the eight dragons from the cued hand spots (tto.md's fk table, +-3 cm), each flying the code's Bezier to
    the target + 0.6 up (`to: [0, 0.6, 10]`) in 0.7 s; the bites at the target's feet (0, 0, 10) at 1.10 + 0.11 k with
    punch1 / punch2 at 0.9; the King from (0, 0.7, 0.4) to `to: [0, 0, 10]` + 0.8 up in 0.4 s; kingRise at 2.0, eight
    `risingDragon_hit` at (0, 1, 10) from 2.0 every 0.15 s, the fall at 3.35, all on the ground point. Reason: tto
    Verification 1-2 (getSpawnPos is the ground; the Sheep / Cat movers' cued spawn + `to`); tto Q1, Q2, Q3.
29. Bites, strikes, kingRise and fall are cues, not the movers' spawns. Reason: one owner per spawn, the times fixed by the
    fixed target (parts Q3, tto Q2; the Chameleon's arrow hits).
30. Tempest Dance and Yin Yang Fist: every effect on the Panda or the ground under her; the yinYangFist seal at her feet.
    Reason: no target taken; nothing reaches 10 m (tto Read this first 4).
31. The Panda's own status looks: `drunken` at y 0.89 (`kill 10`, `single`), `delayQi` at her feet (`kill 3`, the release
    at the end of the 3 s hold), the Ashura line emitter on her `Root` bone (`kill 10`, `single`). Reason: the status
    applies (CharacterControl.cs:35342 / :35396 / :35500) with the controller's bounds (parts part 4, skills_a).

## Summons and special
32. No summons (the ogres and dragons are effects). Reason: parts Read this first 5.
33. Ashura's red Panda: the HERO_SKINS body look `"ashura": () => ({ tint: [1 / 0.86, 0, 0] })`, cue `[0.8, "skin",
    "ashura", {"kill": 10}]`. Reason: setColor(1, 0, 0) on every renderer (CharacterControl.cs:35484-35496); the Bison's
    Enrage (Bison decision 31; parts Q2, skills_a P1); 24 s cut at 10.
34. Raijin Ken hides the Panda 1 s at 5.5 s: `[0.5, "hideProp", "hero", {"kill": 1}]` on `raijinKen1`. Reason: the hide
    status disables every renderer (skills_b Verification 2; Chameleon decision 49).
35. Three Steps' blade trails switched on and off by the cue's new `enable` list (fxNode1 0.1-0.5 s, fxNode2 0.4-0.8 s,
    fxNode3 from 1.2 s). Reason: the hero's code switches them (:20873-:21277); without it the skill draws nothing
    (parts Q1, skills_b Q6).
36. Tempest Dance's limb trails hang on the hero's Hand_R / Hand_L / Foot_R / Foot_L and stop emitting 0.75 s into the
    end: `[0, "fx", "tto/tempestDance_trails", {"off": 5.75, "kill": 6.18}]` on the `tempestDance` key (the effect outlives
    its 5 s step). Reason: TempestTrails (tto Verification 1, parts Verification 7); not tto.md's `childBones` / `stop`.
37. `tempestDance_counter` (needs an attacker's evaded hit) and `yinYang` (the Yin status on a foe, and none in 7 m):
    built (SKILL_FX), not cued. Reason: Mole decision 50, Cat decision 44 (tto Q6, parts Verification 4).
38. `drunk` and `paralysis` on the target: not cued (their BB parts exist). Reason: a status look on a foe, Cat decision
    44 (parts Verification 5).

## Passives, ranks, rolls, voices, sounds
39. Passives on, max rank: Combo 4 (#101-104), Aura Blast #401, Charge Attack 3, Aura Field #411, Sacred Sage 2 (+ Heaven
    Breath #443), Qi Strike 3 (+ Delay Qi #214, Qi Burst #412), Pummel 2 (+ Ogre Impact #422), Tower Rush 2 (+ #422), Three
    Steps 2 (+ Nine Steps #402), Drunken Fist 2 (+ Drunken Plus 2, Drunken Spin #403), Ashura 2, Lotus Palm 2, Heaven Palm 2,
    Water Monkey 2 / Water Crane 2 (+ Time and Tide #413), Stasis / Death Blow 2 (+ Wind Walker #423), Tiger Toss (+ Tiger
    Pounce #232, Climbing Cliff, Crumbling Mountain, Crushing Monolith #432), Rising Vortex 2, Rising Dragons 2, Roll 2, Roll
    Around #421, Sp Transfer 2, Raijin Ken #444, Fuujin Ken, Combo Link, Mystic Sage 2, Safe Guard, Wind & Cloud 2, Rain &
    Storm 2, Spirit Fist #433; the TTO three have one rank. Reason: the standing rule; their looks replace the base ones
    (Nine Steps' voices, Time and Tide's clones, the ogres, drunkenSpin, crushingMonolith).
40. Every look the game gates on a mission / arena (the punches and their sounds, the wheel, Aura Blast's voice and burst,
    the charge's rings) is shown. Reason: the Sheep / Penguin / Mole precedent (attacks_emotes Q5).
41. Pummel's ogre arms at offsets drawn per spawn, `x / y / d` as `[lo, hi]` floats (Random.Range's float form). Reason:
    random picks as the game makes them; whole-metre `spread` cannot draw 0.2-0.6 m (skills_a Q5, P3).
42. Every voice pick is the game's even `a|b`; Raijin Ken's `raijinKen1|2` and Fuujin Ken's `fuujinKen1|2` keep BB's
    spelling (the rip's lower-case files are found case-free on Windows). Reason: skills_b Read this first 8, Verification.
43. Combo Link and the palms assume their condition (a team combo; a target). Reason: Mole decision 27 (skills_a Q9).
44. The status looks are cut at 10 s with `single` (a refreshed status applies once). Reason: the 10 s rule, Cat decision
    37 (skills_a Q10).
45. Sounds: only BB's own rip (every TTO voice / sound is a BB file, tto Read this first 3); no lookup widening needed.
    Reason: tto Verification "Confirmed".

## Left out
46. Camera effects (motion blurs, shakes, whiteRamp, deltaRamp, Raijin Ken's effectCamera cut, Row6Shake), toasts and
    on-screen texts ("ClimbingCliff!", "Nine Dragons!", "Eye of the Storm"). Reason: Bison decision 35, Cat 43, Mole 51.
47. Heals, SP ticks, damage numbers, Resistance's popup, Combo Plus / Shadow Fist stacks, noForce, atkUp, lock. Reason:
    no look (Sheep decision 4, Cat 44; effect_only "Left out").
48. The missing `sacredSage_ring` / `heavenBreath_ring`: no stand-in. Reason: absent from both games; Mole decision 33.
49. The three dead prefabs (`drunkenFist_hit`, `qiStrike_emblem`, `windcloud_hit`): no cue. Reason: no code loads them.
50. TempestSteer / TempestGlide (the player's steering, the remote catch-up). Reason: the owner's unsteered view (parts Q8).

## Parts and data (every missing part is built)
51. Page (index.html): HERO_SKINS `ashura`; cue option `atBone` (spawn at a bone's world position + x / y / d along the
    hero's facing, her facing + rot, not parented); range-valued `x` / `y` / `d` in cueOf; `api.boneMatrix(name, fx)`;
    `FX_PART_FILES += "tto_panda"`; the SEQ / SEQ_SKILL lines above; the cue-format comment learns `enable`, `k`, `off`,
    `atBone` and the ranges. Reason: skills_a P1-P3, parts Interfaces 1, 6, 8 (Verification 3, 8).
52. `pipeline/wardrobe_data.py`: `animations/[a-z0-9_]+` -> `animations/[a-z0-9_&]+` at both places (:49, :210) now; the
    Panda's data rebuild (it reads D:\ rips and TTO's bundles) and the two cue entries (`wind&cloud`, `rain&storm`,
    effect_only Verification 5's block) at the **home PC**: the lead rewrites the existing HANDOFF item to say so, with
    the build line (`wardrobe_fx.py panda --fx windCloud,rainStorm --voices windCloud1,windCloud2,rainStorm1,rainStorm2
    --sounds windCloud,punch1`) and a browser look at the two tiles and their `&` icon URLs. Reason: effect_only
    Verification 3; the office cannot build the data (CLAUDE.md "Two PCs"); the cue check would reject keys that are not
    clips yet.
53. `fxparts/trail.js`: a disabled TrailRenderer is built hidden, and the cue's `enable` shows / hides it by node name.
    Reason: parts part 1.
54. `fxparts/tto_panda.js` (new): HelixRibbonEmitter (T1, from parts.md's read of the five methods), the code movers
    `Panda.NineDragon` / `Panda.NineKing` (T2 with tto Verification 2's contract: options `k`, `to`, `kill`; no
    `fromBone`, `c1`, `c2`, `flight`, `aim`), the hook `fx:tto/tempestDance_trails` (T3, `off`), the shaders
    `ERB/Particles/Add_CenterGlow`, `ERB/Particles/Blend_CenterGlow`, `Particles/Standard Surface` (T4; the bamboo's
    `_BumpMap` left out, APPROX, parts Q6). `fxparts/tto_sheep.js` gets TrailRendererModern's `emitOff()` (not `stop`).
    Reason: parts T1-T4, Interfaces 5; tto Q8.
55. Extractors: `wardrobe_fx.py` `SHURIKEN_FROM_TTO["panda"] = ["raijinKen_hit"]` (no SHURIKEN_MAT, the Chameleon's
    route); `wardrobe_fx_tto.py` `SKILL_FX["panda"]` = the 15 prefabs and the two `CODE_MOVERS` (parts.md's snippet), and
    `material()` saves `_Noise` as `noiseTex` / `noiseScale` / `noiseOffset`. Reason: parts "LAYOUTS" (verified), parts Q5.
56. No `LAYOUTS`, no new BB script, no shuriken.js change (Noise / Lights are the Monkey's; the Panda's values sit inside
    that model). Reason: parts Read this first 2, T5.
57. TTO1102's code with this PC's 2026-11-09 bundles. Reason: Bat decision 44, Chameleon decision 44; HANDOFF's
    "identical" check.
58. Inventory (`wardrobe_fx_inventory.py`, the editor's): the status looks `ashura`, `drunken`, `drunk`, `delayQi`,
    `paralysis` as ready (CharacterControl-loaded); `threeStep` (the disabled trails) and `raijinKen_hit` (the graft) noted
    as drawn; the three dead prefabs noted; rerun it. Reason: parts Read this first 3, skills_a item 6 (the Mole's item 3).
59. Check (`wardrobe_fx_check.py`, the editor's): OPTS += `enable`, `k`, `off`, `atBone`; `x` / `y` / `d` may be a
    two-number list wherever the check reads them as numbers. Reason: parts / tto Verification 3, skills_a P2-P3.
60. Icons (`wardrobe_skill_icons.py`, the editor's): `CLIP_SKILLS["panda"] = {"fujinKen1": ["fuujinKen"], "fujinKen2":
    ["fuujinKen"], "fujinKen3": ["fuujinKen"]}`; `EFFECT_ONLY["panda"] = ["mysticSage", "safeGuard"]`;
    `OWN_TILE["panda"] = {"sacredSageTechnique": ["cAttack1", "cAttack2"], "delayQi": ["qiStrike1", "root", "qiStrike2"]}`;
    the Bible-key pattern `([A-Za-z]+?)` -> `([A-Za-z&]+?)` (harmless until the home rebuild). Reason: skills_a item 7,
    effect_only Verification 5.
61. The paste-ready blocks the editor uses: attacks_emotes' as written (17 keys); skills_a's (14 keys) with Heaven Palm's
    times per decision 24, plus `@DelayQi:root` (decision 7); skills_b's with `tigerToss` and `raijinKen1` from its
    Verification 2-3 (the two `&` entries held back, decision 52); effect_only Verification 5's first five; tto's
    Verification block (54 cues). parts.md's fragments are superseded by those (parts Verification 1, 6). The empty
    `@RaijinKen:cAttack2` / `raijinKen2` entries stay as records unless the check refuses an empty cue list.
62. Build order (the editor's): `wardrobe_fx_tto.py panda`, then `wardrobe_fx.py panda`, then `wardrobe_skill_icons.py`,
    then `wardrobe_fx_check.py ... --cls panda`. Reason: the Mole's order (its decision 60's note).

## Offered to the user for the Bible (not written there)
The Combo's press windows in effect (stage 2 closes at 0.6 s, stage 4 at 2.4, stage 5 at 3.1) and its look by stage
(punches at 0.1 / 0.3 and 0.2 / 0.4 s, the wheel at 0.1, Aura Blast at 0.3), Aura Blast's voice only in missions; the
charge's rings at 0.7 s and its one plain release; chat1-5, the emote voices the data lacks, BB's silent revive (TTO's
plays Voices/revive); the run's step sounds for every player; Ashura's status 0.8 s after the cast; the climbs' flashes at
Root + 0.3 m (others see + 1 m) and their range-free hits; Pummel with Ogre Impact silent; Heaven Palm 2's 1.5x blast and
its first-frame-after pulses; Lotus Palm's flash before the hit roll; Combo Link voiceless; Crushing Monolith's doubles;
Raijin Ken's real 7.5 s timeline (cAttack2 held to 5 s, raijinKen1 at 5.0, the hit at 5.5, the hide 1 s, standby 7.5);
Water Monkey's / Water Crane's hits 0.2 s apart; Stasis / Death Blow with no hit look; Nine Steps' voices, Time and Tide's
clones; Death Blow on the stasisBlow clip; Wind & Cloud's / Rain & Storm's hit times one wait later than the reference's
table; Three Steps' trail switching; the three dead prefabs; sacredSage_ring / heavenBreath_ring missing from both games;
Safe Guard reaching the owner only through the ActionEvent; Mystic Sage's double at the hero, not the hit point; Delay
Qi's standby after 0.2 s with the glow on, `delayQi_fire` at the release; Nine Dragons' hand order, Bezier, 0.7 s cap,
bites at the foe's feet, the King's weave and 0.5 s vanish, the strikes 1 m up (others 1.5 m); Tempest Dance's gust every
other tick and its trails stopping 0.75 s into the end; Yin Yang Fist's seal under the Panda, the burst at 1.75 s, the
Yin mark under a foe; TTO's HelixRibbonEmitter.
