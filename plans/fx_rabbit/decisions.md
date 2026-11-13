# Rabbit effects: decisions (13/11/2026), decided overnight, for the user's review

The user was not available, so the planner decided every open question in the six reports in this folder
(attacks_emotes, skills_a, skills_b, effect_only, parts, tto), each read with its "## Verification" (the verification
wins where the two differ). Rules used, in this order: the standing rules (top rank, passives on; random picks as the
game makes them; enemy effects at the 10 m target point, homing aims 0.6 m up; long buffs / fields / summons cut at 10 s;
a tile per skill with its Bible icon, pool members one each, effect-only tiles on the idle stance; missing parts always
built; TTO cues only for the released `bountyHunt`, `coinRicochet`, `medicTurret`, `clap`, `wai`: all five are in
`wardrobe/tto_released.json`), the page's SEQ rule (a charge = full charge, a channel = its duration, at least 3 s for a
hold until the player acts; high INT: every cast bar at magAdjust's 0.1 s floor), then the Wolf's, Sheep's, Penguin's,
Bat's, Bison's, Cat's, Chameleon's, Mole's and Monkey's decisions by analogy, then the reports' own recommendations.
Every item is **decided overnight, for the user's review**: any of them can be turned round in the morning.

Already in the tree (committed, nothing to rebuild for the Rabbit): the `hideProp` kind with slot `"hero"` / `"R"`;
`worn` / `notWorn` + `ITEM_SETS`; `pick: "color"`; `playAudio` (Mole decision 46: the first playOnAwake-off AudioSource,
stopped when the Fx goes); the `"skin"` kind + `HERO_SKINS` tints (Bison's enrage shape); `rot: "randomYaw"`; `p` /
`roll` / `"!roll"`; `scale` [x, y, z]; `bone`; `api.spawn` + the entry's `"builds"`; `CODE_MOVERS` (Chameleon.ApexArrow);
RabbitTracer, LineRenderer (tto_sheep.js); the two Eric/URP Particles shaders (`fxparts/tto_monkey.js:153-154`) and
Shuriken's NoiseModule (`fxparts/shuriken.js`), so tto P6 / parts Q7 are done and **no `urpparticles.js`**; the
Chameleon's no-SHURIKEN_MAT graft route; SEQ_ALT's `a|b` steps (Truce Trading's outcome). A script with no page part is
skipped silently by the Fx constructor, so the 0-byte Rabbit scripts need **no no-op parts**.

## Tiles and sequences
1. Normal Attack `"Normal Attack: nAttack"` (one shot; the first step keeps the page's 0.2 s fade). Reason: one clip, one
   shot (attacks_emotes item 1, verified); a one-step SEQ takes nAttack out of the ท่าสกิล list as every class.
2. Customized Shotgun: the Normal Attack's cues carry `worn` / `notWorn ["R", "rabbitShotgun"]` (new
   `ITEM_SETS.rabbitShotgun`, the 10 props of isShotgun), **and** its own tile `"Customized Shotgun: nAttack"` (key
   `@CustomizedShotgun:nAttack`, always the shotgun shot, no voice). Reason: attacks_emotes Q2; one tile per skill, the
   item precondition shown (Chameleon decision 13's shape).
3. Charge Attack `"Charge Attack: cAttack1@1 cAttack2*@4 cAttack3"` (the scope at 1.0 s, held 4 s to Dead Shot's x3).
   Reason: the SEQ rule's full charge (attacks_emotes Q3, verified).
4. From the Above (#421, no clip) gets its own tile `"From the Above: bounce1@9.5 bounce2!"` (keys `@FromtheAbove:bounce1`
   / `@FromtheAbove:bounce2`, the second empty on purpose), six air shots at 1.1 ... 8.6 s. Reason: the Chameleon's Critical
   Plus shape (a skill on another skill's clips); every press at the earliest, as the Mole's Bombardment (effect_only Q2,
   attacks_emotes Q4; effect_only verification 1-2 for the block and the dropped `bounce2@1.4`).
5. Bounce `"Bounce: bounce1@9.5 bounce2!"`, the hero hidden 0.9-9.5 s, fromTheAbove_ring + bounce0 at 8.9 s. Reason: rank 2's
   8 s in the air, under the 10 s cut (skills_a Q1 and verification 5 over effect_only's `bounce2@1.4`).
6. Mall `"Mall: mall1*@3 mall2*!@2 sit*~@3"` (8 s), the stall `mall1|...|mall5` by `pick: "color"`, `kill 7.95`, **no voice**
   (no `mall2` / `@Mall:sit` entries). Reason: the SEQ rule's 3 s holds (skills_a Q6); BB never plays mallOpen / mallClose,
   TTO's wiring is a behaviour change (skills_a verification 1, Cat decision 34).
7. The channel hosts are renamed `"Cast: mix1@0.6 mix2*@0.1 mix3~"` and `"Field Cast: mix1@0.6 mix2*@0.1 mix4~"` (hidden
   hosts); pools `mix3` (Mix, Shake, Miracle Blend), `mix4` (Sticky Gum, Acidic Field, Healing Field), `medicalShot`
   (Immune, Boost, Heat, Life Shot), `gilShot` (Gil Shot, Diamond Shot): one tile per member. Reason: poolChains' `taken`
   would drop the members `mix` / `stickyGum` under today's host names (skills_b Read this first 2, verified).
8. `"Truce Trading: truceTrading*@0.12 cheer*~@2|cry*~@2"` (keys `@TruceTrading:...`), the outcome an even pick. Reason:
   p = 2 / HP at LCK 1 makes cheer all but impossible; Cat decision 32 shows every outcome (skills_b Q1, verification 9).
9. `"Contract: truceTrading*@0.1 bow~@1.2"` (keys `@Contract:truceTrading`, `@Contract:bow`). Reason: the 0.1 s bar floor,
   then the summon and bow (skills_b Read this first 3, Q11).
10. The three TTO skills stay single clips (`bountyHunt`, `coinRicochet`, `medicTurret`), no SEQ line, **no Medic Turret
    hold line**. Reason: no cast bar (tto Read this first 1); the turret's beats are part-made, so the loop toggle cuts
    nothing of them and a held last pose would be wrong (tto verification 2, dropping tto Q4).
11. No effect-only (`root@t`) tile and no EFFECT_ONLY entry: every active plays a clip; Knee Shot, Snipe Mastery and Herb
    Finder get no tile (their prefabs exist in neither game: nothing to show). Reason: effect_only Result and Q3-Q4, verified;
    a passive with no look gets no tile.
12. Rapid Trance's medical-shot variant on `gilShot` is not a pool member. Reason: a 12 s active's state, not a passive;
    the four shots have their tiles on `medicalShot` (skills_a Q3).
13. SEQ_SKILL `rabbit: { "@CustomizedShotgun": "customizedShotgun", "@FromtheAbove": "fromTheAbove", "@TruceTrading":
    "truceTrading", "@Contract": "contract" }`; `wardrobe_skill_icons.py` `CLIP_SKILLS["rabbit"] = {"maim": ["maimShot"]}`,
    `OWN_TILE["rabbit"] = {"customizedShotgun": ["nAttack"], "fromTheAbove": ["bounce1", "bounce2"], "contract":
    ["truceTrading", "bow"]}`, `RANK_ICONS["rabbit"]` = skills_b verification 5's 14 card icons (backpack2, circleShot2,
    fourShot2, gorgonShot2, mall2, shake3, miracleBlend1, stickyGum2, acidicField2, rapidTrance1, statScan1,
    shootingArray2, millionaire2, truceTrading2), and the editor compares `nAttack` / `cAttack` with their cards the same
    way, adding them only if they differ. Reason: skills_a verification 4, skills_b verification 5-6, effect_only
    verification 3-4, attacks_emotes verification 3.
14. KO: `deadEffect` on half the plays, ko1 / ko2 and dead1 / dead2 voices, getUp silent (RPC_revive loads no voice).
    Emotes: bow takes `ty|bow`, chat picks chat1-3, no footsteps (no AnimationEvents); clap, wai and the other TTO-only
    emote clips silent. Reason: attacks_emotes items 8-10 (verified); Cat decision 16.
15. RPC_cAttack0 (the cancel), RPC_activateIcon1: no tile, no cue. Reason: Chameleon decision 18, Penguin decision 19.

## Where things land
16. Normal Attack aims at the no-target **10 m ground point**: the Bouncing Bullet tracer from (0, 1, 1) meets the floor at
    d 11 (`bouncingBullet_hit`), the second tracer 0.02 s later; the graze of the target body counts as a hit, so voice
    `nAttack2` at 0.34 s. Reason: Penguin decision 1 / Chameleon 22 (attacks_emotes Q1, verification 1's capsule).
17. **Snipe Mastery's hit draws nothing**, as the game (`snipeShot_hit` exists in neither game); flagged to the user, since
    it reads as "missing" on the page. Reason: passives on (parts Q2, effect_only Q1).
18. Every ray hit goes on the standard target body, the CharacterController capsule (centre 0.6 m up, height 1, radius
    0.3): maim / gil / diamond / medical (0, 0.612, 9.7), gorgon (0, 0.692, 9.7), Four Shot / Ten Shot (0, 1, 9.7),
    cAttack_hit (0, 1.05, 9.83), From the Above (0, 0.36, 9.7). Reason: Bat decision 4 (attacks_emotes verification 1,
    effect_only verification 1).
19. The Medical Shots aim at an **ally at the 10 m point** (they refuse the Rabbit herself). Reason: Monkey decision 20
    (skills_b verification 4).
20. Stat Scan is drawn on the target with the new cue option `owner` `[0, 0, 10]`: it faces the camera and, followPosition
    with the target as owner, sits at owner + R x (spawn - owner), so it swings round the target as the view turns.
    Reason: BB's EffectControl faceCamera branch (parts verification 4, skills_b verification 3).
21. bounce1 / bounce2 (faceUp) and statScan (faceCamera) turn by their **root** EffectControl's mode, a new page part.
    Reason: the page applies the mode only to a child (parts Read this first 4, part 5); built for every class.
22. Fields and the gum on the floor 2 m ahead, `kill 10`, `replace` (one of each kind: the game Destroys the old one); the
    potions 1.5 m round the hero, `kill 10`, stacking play after play; Sticky Gum `scale` [2.5, 1, 2.5]. Reason: the 10 s
    rule and the code (skills_b Q5, parts part 1, 3).
23. The potions' and stars' ring turns by one random angle per play: the new option `yaw` (`"cast"`, one
    Random.Range(0, 360) per play per name, reset with `FX.rolls`). Reason: RPC_cast1's one draw (skills_b Q6, P1).
24. Millionaire's 18 coins at hero + vFlat(2 x Random.onUnitSphere): the new option `sphere` (2), rot `[270, "random", 0]`
    (a `"random"` inside a rot list = Random.Range(0, 360) per spawn). Reason: random picks as the game (skills_b P2).
25. Hits out of reach are not drawn: Backpack's 3 m and Circle Shot's 8 m pulses, Four Shot's back / left / right cones,
    Ten Shot's first four volleys, Shooting Array's 6 m pulses, Millionaire's 8 m pulses, Bounce's stomp. Reason: Bison
    decision 16 (skills_a item 9, skills_b Read this first 5).
26. The hero does not travel (recoils, the fields' lunge, the Medical Shot's step, Bounce's steering). Reason: Penguin
    decision 8, Bison decision 17.
27. TTO hand and muzzle spots are fixed from the clip (`bones.txt`): the poster and coins from mountHand_L, the shots from
    mountHand_R + 0.35 forward (no Rabbit gun has a muzzle child). Reason: tto Read this first 2, Q6, verified.
28. Bounty Hunt: the poster flies to the chest **+ 0.6 up** (`to` [0, 1.2, 10], `kill 0.25`) and spawns nothing on arrival;
    the pin is cued at 0.65 s on the chest; the hired guns' muzzles / tracers / hits at the three fixed spots. Reason:
    parts verification 2, tto verification 1.
29. Coin Ricochet: each coin's first hit only (no second foe for hops 2-3); the bob phase from the cast (Time.time = 0 at
    the cast, the cue's clip time `fx.at.at` + age), so the cued tracers meet the coins. Reason: tto Q3, verification 4.

## Summons, the turret, special
30. Contract shows **the Light Golem** (level 3, SP >= 65), on the floor 3 m ahead facing forward, `root` looped from the
    spawn, **its own LightGolem1 material** (no swap: that is layer 9's), `kill 10`, no AI; Panther / Leopard not built.
    Reason: top rank (parts Q3, skills_b Q2); skills_b verification 1; Mole decision 32. Its part lives in
    `fxparts/rabbit.js` (elementals.js is class-guarded to the Monkey; one owner per file, skills_b verification 2).
31. The Medic Turret is a part-driven summon: `[0.55, "fx", "tto/medicTurret", {"d": 1.8, "end": 10, "kill": 10.4,
    "ally": [0, 0.7, 0], "replace": true}]`; its part grows the Model, makes the 7 beats (beat, head snap, shot, capsule),
    the break and the 0.4 s shrink at `end`; the capsule mover spawns the hit and the drop. No beat is cued. Reason: tto
    verification 2, parts verification 3 (one owner per beat, Mole decision 32); the 10 s cut after the spawn (Monkey
    decision 30's `end`).
32. The turret's capsules fly to **the Rabbit herself** (her chest 0.7 m up; the drop at her feet), the kind drawn per beat
    (a third each), BB's lifeShot / boostShot / heatShot as the drops. Reason: MedicTurretPick includes her and skips the
    Robot-race turret (parts Q4, Q5, tto Q2).
33. One turret at a time through the cue's `replace` (the game destroys the older turret at the create), not a turret-side
    lookup. Reason: one generic option (decision 22's) covers it; with วนซ้ำ the recast replaces, never stacks.
34. Ten Shot's second gun: the new cue kind **`propCopy`** `[0.2, "propCopy", "R", {"bone": "mountHand_L", "kill": 2.6}]`
    (a full copy of the worn main weapon with its weapon_fx, hidden with the hero, nothing when no weapon is worn). Reason:
    the code's Instantiate(mWep1) (parts part 6, skills_b P4, Q9).
35. Rapid Trance's purple tint: `HERO_SKINS["rapidTrance"]` = `{ grow: 1, tint: [0.48 / 0.86, 0.43 / 0.86, 0.78 / 0.86] }`,
    cued `[1.1, "skin", "rapidTrance", {"kill": 10}]`. Reason: setColor (skills_b P5, Q8), Bison's enrage shape.

## Passives, ranks, rolls, voices, sounds
36. Passives on, max rank: Combo 4, Hyper Shot 4, Bouncing Bullet #401, Snipe Mastery #431, Dead Shot #411, Customized
    Shotgun 2, From the Above #421, Bounce 2, Maim Shot 4 + Knee Shot #402, Gil Shot 4, Gorgon Shot 2, Backpack 2 + Big Bag
    #423 (bigbag_ring), Four Shot 2, Circle Shot 2, Mix 4 + Extra Potion #412 (5 hpPot4), Shake 3 (3 spPot3), Miracle Blend +
    Miracle Drop #422, Sticky Gum 2, Acidic Field 2, Truce Trading 2, Contract level 3, Shooting Array 2, Millionaire 2,
    Mall 2. Reason: the standing rule.
37. Knee Shot: `maimShot_hit` at `p 0.8` (`kill 1`), nothing on the other 20 %. Reason: lckAdjust(20) at LCK 1 and the
    missing kneeShot_hit (skills_a Q4, Q8).
38. Miracle Blend: each bottle rolls randomPot6 at `p 0.05`, else randomPot1-5 even. Reason: lckAdjust(5) at LCK 1, as the
    game (skills_b).
39. The Charge Attack's deadShot plays **through the scope's own AudioSource**: `[0, "fx", "sniperCamera", {"y": 1.05, "d":
    0.15, "playAudio": 0.1, "kill": 4.2}]` on `cAttack2` (gone 0.2 s after the release, the game's Destroy, which stops
    the sound), not attacks_emotes verification 2's `"sound"` kill / SoundCut. Reason: the built `playAudio` gives the
    same 4.1 s with no new page code (parts part 2); the Rabbit_sniperCamera layout is needed anyway.
40. Every look the game gates on missions / arenas (the Normal Attack shot, the shotgun, the cAttack voice, the release,
    the Medical Shot's voice) is shown. Reason: the Sheep / Penguin / Mole precedent (attacks_emotes Q6, skills_b Q7).
41. Voices as the code loads them: Healing Field `shake2|mix2`, Extravagance and Customized Shotgun silent, Coin Ricochet
    silent, Bounty Hunt `contract1|contract2`, Medic Turret `lifeShot1|lifeShot2`. Reason: the reports' reads, Sheep
    decision 10 (TTO's fix only where BB's file is missing).
42. Hero-played sounds as `"sound"` cues: `nAttack` on the Bouncing Bullet shot (its prefab has no AudioSource); TTO's
    Row6Sound calls with their volumes. Reason: attacks_emotes item 5, tto section 7.
43. Frame-loop timers at the code's nominal intervals (the scope's 0.1 s check, the 0.02 s fixed step). Reason: Mole
    decision 45.

## Left out
44. The scope's first-person camera, FOV 60, scope picture, range readout, Dead Shot picture and bar; motion blurs;
    AutoZoom; the HyperShot / Dead Shot! / "+N atk" messages; Mall's buy button and shop windows; Stat Scan's chat lines;
    Coin Ricochet's gold chat. Reason: Bison decision 35, Cat decision 43, Mole decision 51 (parts Q1).
45. Status looks on others: Bounty's wanted poster and Gilded's glints on the foe, the allies' statuses, the drinker's
    `enlarge` / `reduce` / `miracleDrop` / `autoLife`; Bounty Hunt's kill reward (`bountyHunt_claim`). Built (SKILL_FX /
    the data), not cued. Reason: Sheep decision 4, Cat decision 44, Chameleon decision 53 (tto Q5, parts Q6).
46. Gear procs on a hit, damage numbers, the potions' pickups, Coin Ricochet's Gil per hit (the page plays her with
    enough Gil). Reason: Chameleon decision 53, Monkey 52; tto verification 3.
47. The missing prefabs draw nothing: `snipeShot_hit`, `kneeShot_hit`, `herbFinder`, `contract_ring`, `fourShot_hit`,
    `circleShot_hit`, `tenShot_hit`, `mall` / `mall0` / `mall6`. No stand-in. Reason: Mole's warCapital_dead (parts item 8).
48. The plain rifle path (nAttack_fire + its ray) on the Normal Attack: Bouncing Bullet replaces it with the passives on.
    Reason: attacks_emotes "Left out".

## Parts and data (every missing part is built)
49. `wardrobe_fx.py`: parts.md's LAYOUTS block as written (Rabbit_potion, Rabbit_sniperCamera, the four 0-byte scripts,
    LightGolem, LightGolemAI; 97 built, 0 raise, verified twice), `SHURIKEN_FROM_TTO["rabbit"] = ["extravagance_ring"]`
    with no SHURIKEN_MAT entry, `EXTRA_FOLDERS["rabbit"] = ["gameassets/characters/elementals/lightgolem"]`. Reason: parts
    parts 1-4, 7, verification 1.
50. `wardrobe_fx_tto.py`: `SKILL_FX["rabbit"]` = parts.md's 25 names; `CODE_MOVERS` += `medicTurret_capsule:
    Rabbit.TurretCapsule`, `bountyHunt_poster: Rabbit.PosterFly`, `coinRicochet_coin: Rabbit.CoinRise`. Reason: parts
    "TTO", tto P7, parts verification 7.
51. `fxparts/tto_rabbit.js` (new): RabbitSpin, the three movers (PosterFly with no arrival spawn), RabbitMedicTurret
    (decisions 31-33), and **PowerUpRotation** (`Rotate(0, 0, speed dt)`, three lines, on the uncued claim: a missing part,
    built). Reason: tto P1-P5 with verification 2, parts verification 2-3; the build-every-part rule over parts Q6.
52. `fxparts/rabbit.js` (new): only the `LightGolem` part (decision 30). The four 0-byte scripts and Rabbit_mall get **no
    no-op parts** (the page skips a script with no part; inventory BUILT names them). Reason: skills_b verification 2's
    "optional"; YAGNI.
53. `fxparts/control.js`: `EffectControl(root)` (modes 2 / 3 on the root while `fx.age < life`, with `owner`) for every
    class; `fxparts/sheep.js`: `if (fx.cls !== "sheep") return null;` at the top of `fx:cAttack_charge`. Reason: parts
    parts 5, 8 and verification 4.
54. `wardrobe/index.html`: the SEQ / SEQ_SKILL lines (decisions 1-10, 13), `ITEM_SETS.rabbitShotgun`, the `propCopy` kind,
    the cue options `yaw`, `sphere`, `replace` and `"random"` inside a rot list, `HERO_SKINS.rapidTrance`, the
    `EffectControl(root)` call, `FX_PART_FILES += "rabbit", "tto_rabbit"`, the cue-format comment for each. Reason: the
    parts above; one owner (page_pipeline).
55. `wardrobe/fx_cues/rabbit.json` (the editor's, after the builders) pastes the corrected blocks: attacks_emotes' with its
    verification's nAttack / cAttack3 (its cAttack2 entry replaced by decision 39's sniperCamera cue, its From the Above
    block dropped for effect_only's); skills_a verification's whole block; skills_b's with its verification's statScan,
    `@Contract:bow`, medicalShot (the tenShot from skills_b, not parts'); effect_only verification's two entries; tto's
    section 7 with its verification's medicTurret (`medicTurret_deploy`'s bare `1.8` written `{"d": 1.8}`, `replace` added
    to the turret cue).
56. The check (`wardrobe_fx_check.py`, the editor's): KINDS += `propCopy`; OPTS += `yaw`, `sphere`, `replace`, `owner`,
    `ally`, `delay` (not `kind`: spawn-only); a rot list may hold `"random"`. Reason: parts verification 5, skills_b
    "Page changes" 10.
57. The inventory (`wardrobe_fx_inventory.py`, the editor's): BUILT += `Rabbit_potion`, `Rabbit_sniperCamera`,
    `Rabbit_acidicField`, `Rabbit_healingField`, `Rabbit_stickyGum`, `Rabbit_mall`, `LightGolem`, `LightGolemAI`,
    `RabbitMedicTurret`, `RabbitSpin`, `Rabbit.TurretCapsule`, `Rabbit.PosterFly`, `Rabbit.CoinRise`, `PowerUpRotation`;
    the 12 unlisted prefabs (castStar, castLight, deadEffect, mall1-5, autoLife, enlarge, reduce, miracleDrop) listed by
    hand; extravagance_ring's grafted-systems NOTE; rerun. Reason: the recipe's rule (parts item 7).
58. TTO1102's code with the 2026-11-09 bundles. Reason: Bat decision 44, Chameleon decision 44 (the bundles this PC has).

## Offered to the user for the Bible (not written there)
Snipe Mastery's and Knee Shot's hits are missing prefabs (no hit drawn), with `fourShot_hit`, `circleShot_hit`,
`tenShot_hit`, `herbFinder`, `contract_ring`; Bouncing Bullet: the floor counts as a wall (a no-target shot ricochets 1 m
past the target point), segments a fixed step apart (not 0.3 s), the first-segment bounce exception; the Normal Attack's
shot at 0.3 s and standby 0.83 s, the shotgun voiceless (standby 0.79 s); the scope 1.0 s after the press, only on the
owner's screen and in missions (`mGameType >= 3`), deadShot from 0.1 s on a head to the release; the Normal Attack and the
Charge Attack's voice mission-only; RPC_revive loading no voice; From the Above's air shots (from 1.0 s, every 1.5 s, at most
6) and its ring replacing bounce2's effect; Bounce's timeline (8.9 / 9.5 / 9.9 / 10.3 s); the shot times of Maim, Gil,
Gorgon, Four and Circle Shot; the Medical Shots firing at 1.4 s (1.0 s with the gilShot clip under Rapid Trance) and their
shot voice mission-only; Rapid Trance's tint and its fixed voices; Healing Field borrowing shake2 / mix2; BB never playing
mallOpen / mallClose (TTO does), mall3-5 sharing one stall material, the cached stall colour; Acidic / Healing Field pulsing
7 times, not 6; Rabbit_potion's never-set "taken" flag; one field of each kind; Millionaire's 18 coins and burst times; Ten
Shot's volleys 0.4-0.5 s apart; the golem's second material only on layer 9; the TTO timelines (the poster's left hand, arc
and chest + 0.6 landing, the hired guns' spots, the coins' hang spots and bob, the Medic Turret shooting the Rabbit herself,
its Race 4, grow and shrink).
