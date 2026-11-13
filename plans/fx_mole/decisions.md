# Mole effects: decisions (2026-11-13), decided overnight, for the user's review

The user was asleep, so the planner decided every open question in the six reports in this folder (attacks_emotes,
skills_a, skills_b, effect_only, parts, tto), each read with its "## Verification" (the verification wins where the two
differ). Rules used, in this order: the standing rules (top rank, passives on; random picks as the game makes them;
enemy effects at the 10 m target point; homing aims 0.6 m up; target-rotation effects rot [0, 180, 0]; long buffs /
fields cut at 10 s; a tile per skill, pool members one each, effect-only tiles on the idle stance; missing parts always
built; TTO cues only for the released `barrelRailgun1`-`4`, `kaiserArsenal`, `missilePad`: all six Mole TTO clips are in
it), the page's SEQ rule (a charge = full charge, a channel = its duration, at least 3 s for a hold that runs until the
player lets go; high INT, the cast bar at magAdjust's 0.1 s floor), then the Wolf's, Sheep's, Penguin's, Bat's, Bison's,
Cat's and Chameleon's decisions by analogy, then the reports' own recommendations. Every item is **decided overnight,
for the user's review**: any of them can be turned round in the morning.

Already in the tree (nothing to rebuild for the Mole): the `hideProp` kind with slot `"hero"` (the whole hero, her props
and their weapon_fx particles; Chameleon decision 49), so **no `hideHero` cue kind** (attacks_emotes verification 1, parts
verification 1, skills_a verification 2); SEQ steps that repeat a clip (Venom Phantom); `worn` / `notWorn`; the `"sound"`
kind; `api.spawn` + the entry's `"builds"`; cat.js's `trajectoryVector` / `lookEuler` exports and `STEP = 0.02`; the
Chameleon's no-SHURIKEN_MAT graft route (BB's own PSR materials matched by node name and material); `additivealpha.js`,
`particles.js`, `alphatimer.js`, `shuriken.js`, `groundhug.js`, `tto_sheep.js`'s LineRenderer, `tto_penguin.js`'s cel shader.

## Tiles and sequences
1. Normal Attack: `"Normal Attack: nAttack1@0.7 nAttack2@0.5 nAttack2@0.5 nAttack2@0.5 nAttack2"` (five shells, Combo 4);
   stages 2-5 cut in (no fade mark), the first step keeps the page's 0.2 s fade. Reason: one coroutine, clips at 0.7 /
   1.2 / 1.7 / 2.2 s (attacks_emotes Read this first 1, verified; a SEQ may repeat a clip, verification 3).
2. Charge Attack: `"Charge Attack: superDig@0.7 dig2*@2.3 root~@0.2"` (released at 3.0 s, the plain surfacing, key
   `@ChargeAttack:root`). Reason: the SEQ rule's "at least 3 s" for a hold; Super Dig on (attacks_emotes Q3).
3. Sky Drill gets its own tile `"Sky Drill: superDig@0.7 dig2*@2.31 skyDrill"` (released at 3.01 s, the `> 3` test true).
   Reason: one tile per skill (Sky Drill #313-314 is a passive with its own clip); attacks_emotes Q3.
4. `dig2` is the hidden underground step of both (its `dig_dirt` entry stays), and `NEVER_PLAYED.mole = ["dig2"]` is
   written too, as the record that no BB or TTO code plays it; mentioned to the user. Reason: attacks_emotes verification
   4, skills_a verification 4 (harmless with the SEQs; skills_a Q7).
5. The superDig entry is attacks_emotes' corrected one (`[0.6, "hideProp", "hero", {"kill": 2.4}]`); skills_b's
   "keep the hero visible" tile does not arise (a clip a SEQ plays is hidden). Reason: attacks_emotes verification 1, 4;
   skills_b Q5.
6. Assemble pool (Auto Gyro Gun, Barrel Bot): `"Assemble: assemble1 assemble2*@0.1"` (magAdjust's 0.1 s floor), one tile
   per member. Reason: high INT / the Bat's bigCast2 precedent (skills_a, verified).
7. War Capital gets its own tile `"War Capital: assemble1 assemble2*@8"` (keys `@WarCapital:assemble1/2`), the 8 s floor
   of its 24 s bar. Reason: one tile per skill; magAdjust cannot go below 8 s, not a long buff (skills_a Q2).
8. Bunker `"Bunker: bunker@3"`; Flame Turret `"Flame Turret: flameTurret1 flameTurret2*@4.5"` (chaAdjust(5) = 5 at CHA 1);
   the page's first-step fade stays where the game cuts in. Reason: skills_a Q8, Q9; Cat decision 2.
9. King Kaiser: `"King Kaiser: dig1@4.9 root*@10"` (key `@KingKaiser:root`). Reason: skills_a's timeline, the 240 s
   form cut at 10 s.
10. Barrel Railgun (TTO, released): tto.md's S1 line `"Barrel Railgun: assemble1@0.6 assemble2*@5.4
    barrelRailgun1>0.55^@0.65 barrelRailgun2*^@2.2 barrelRailgun3^0.05@0.5 barrelRailgun2*^@1.9 ... barrelRailgun4^0.05@0.5"`
    (17.15 s), the ride cut at 10 s (4 shots), the new token `>t` = start the step's clip at t s. Reason: the code plays
    Assemble's clips through the fixed 6 s bar (tto Read this first 1, verified); the 10 s rule (tto Q1); skills_a Q12.
11. Effect-only tiles on the idle stance: `"Reload: root*@1.1"`, `"Fire Barrage: root*@5.3"`, `"Bombardment: root*@8.2"`,
    `"Synchro Mole: root*@10"` (keys `@Reload:root` ...). Reason: the dispatcher plays no clip for them (effect_only,
    verified; the Sheep's Quick Heal shape).
12. Pools, one tile per member: `mine` (Landmine, Stun Mine, Time Nuke, Flame Carnival), `mortarShot` (Mortar Shot,
    Napalm), `punch` (Mega Punch, Mega Drill), `tnt` (**TNT 1-4, four tiles**, each its own cast landing 8 n m ahead, with
    its rank icon `tnt<n>` and its Bible name, not "Tnt1"). Reason: the standing rule (skills_b Q1 and verification 4).
13. War Factory: **one tile**, a pool with `"order": "cycle"`: each play takes the next weapon in the game's order (Saw
    Machine, Bazooka, Tesla Coil, Roller Machine, Cart Bomb) and ends at that weapon's standby (1.3 / 2.2 / 3.0 / 3.5 /
    3.5 s, a member key `"standby"`), then the 0.2 s fade to idle; poolChains makes no per-member tiles for a cycle entry.
    Reason: one skill (#434, one icon) whose counter steps 1 -> 5 and wraps (skills_b Q2); the members are not skills.
14. SEQ_SKILL `mole: { "@ChargeAttack": <the page's existing Charge Attack id>, "@SkyDrill": "skyDrill", "@WarCapital":
    "warCapital", "@KingKaiser": "kingKaiser", "@Reload": "reload", "@FireBarrage": "fireBarrage", "@Bombardment":
    "bombardment", "@SynchroMole": "synchroMole", "@BarrelRailgun": "barrelRailgun" }`; `wardrobe_skill_icons.py`
    `CLIP_SKILLS["mole"] = {"grenade": ["stunGrenade"], "hammer": ["megaHammer"], "assemble1": ["autoGyroGun",
    "barrelBot"], "assemble2": ["autoGyroGun", "barrelBot"], "dig1": ["kingKaiser"]}` (+ the tnt1-4 rank icons and War
    Factory's `warfactory5`), `OWN_TILE["mole"] = {"warCapital": ["assemble1", "assemble2"]}`, `EFFECT_ONLY["mole"] =
    ["reload", "fireBarrage", "bombardment", "synchroMole"]`. Reason: skills_a "Page lines", skills_b verification 3,
    effect_only block 4.
15. activateIcon1 (the mission channel), RPC_cAttack0's early release, barrelCannon's TTO War Area (not released): no
    tile, no cue. Reason: Penguin decision 19; the released-list rule.
16. KO: `deadEffect` on half the plays (RPC_dead), no voice; getUp silent (no Voices/revive in the rip). Reason: Sheep
    decision 11, the Wolf's shape (attacks_emotes item 9).
17. Emotes as attacks_emotes' block: the bow tile takes emo_ty's `ty`, talk takes chat's voice, chat picks chat1-3
    only (Random.Range(1, 4)), `pose` on every pose clip BB plays; pose37 and TTO-only emote clips silent. Reason: the
    code (attacks_emotes item 8, verified); Cat decision 16.

## Where things land
18. Every shell aims at the **10 m ground point** (`to: [0, 0, 10]`), the Normal Attack's lob rising 6.75 deg and landing
    9.83 m ahead after 0.62 s; the hits are **part-spawned** on contact with the floor or the standard target body (the
    entries' `"builds"`). Reason: Penguin decision 1, Sheep decision 3 (attacks_emotes Q1); parts Q1, as the Cat's Support
    Fire.
19. The worn cannon's `firePoint` node is the muzzle when it has one (28 of 44 BB cannons), re-aimed from there at `to`:
    options `firePoint: "R"` and `to` on the Normal Attack, **Mortar Shot, Napalm and Stun Grenade** (each with its own
    vector: getTrajectoryVector 15 for the Normal Attack and Stun Grenade, getMortarVector 20 for Mortar Shot / Napalm);
    the cue's x / y / d / rot stay the fallback. Reason: BB's code reads it first (attacks_emotes Q2; skills_b Q3 is
    overruled: BB, not TTO, is the content, skills_b Read this first 9).
20. Double Cannon (`specialCannon`, no firePoint) fires its two shells ∓0.3 m and ±9 deg (`worn` / `notWorn`). Reason:
    the code (attacks_emotes item 4).
21. Mortar Shot and Napalm keep the game's 83-degree lob and its ~4 s fall (landing 4.4-5.2 s into the tile, in the
    idle tail; the loop toggle cuts nothing part-made). Reason: getMortarVector at the 10 m point (parts Q2).
22. Missiles (BB `missile_fire`, TTO `missileBot_fire`) home on the target body's centre 0.6 m up and **spawn their own
    hits** on contact (BB `missile_hit` with the hero's rotation; TTO `tto/missileBot_hit`, and `tto/twinImpact` on a
    pair's second hit within 0.5 s, the cue's `pair`); the TTO missilePad entry drops its cued hits and blasts and the
    missiles' `kill`. Reason: parts Q1's rule for every projectile; BB's and TTO's Mole_missile are one script (one part,
    one owner); the egg's 64 split missiles need the same contact logic anyway (tto Q5's alternative, made the rule;
    tto verification 1-3: the standard body, the egg keeps the gold blasts, splits carry the last pair's id, their
    direction from the hero's forward + 0.3 up).
23. Bazooka's shells (24 m/s, no gravity) and the Cart Bomb stop on the target body: the cart's centre at 9.2 m, its
    boom at 3 s after its spawn (driving from 0.2 s after the spawn, 6 m/s). Reason: the solid capsule and the game's
    collision matrix (skills_b Q6, parts Q5, parts verification 5).
24. Grenade Cluster's eight grenades: yaw -45 i, a tilt drawn per grenade from Random.Range(3, 10) (`tilt: [3, 9]`),
    6 m/s, bursting on the floor. Reason: random picks as the game does them (skills_b).
25. Fire Barrage and Bombardment aim **9 m** ahead (1 m in front of the 10 m target), Fire Barrage's side aircraft at the
    game's own spots (x ±1.098, d 13.098, yaw ∓30), all of Bombardment's 35 cues. Reason: the code's aim (effect_only Q1,
    Q3, Q4).
26. Mines, Stun Mines, Time Nuke and Flame Carnival lie where the game lays them (0.5 / 1 m ahead), never triggered (the
    10 m target is outside their 4 m spheres), `kill: 10`, stacking play after play. Reason: the 10 s rule (skills_b Q10,
    parts Q3); Flame Carnival's `fx:flameCarnival` is still built with an unused `trigger` option (missing parts always
    built).
27. Detonate assumes Time Nuke 2's nuke 1 m ahead (the skill refuses to start without one): `[0, "fx", "timeNuke2",
    {"d": 1, "kill": 3}]`, `detonate` at it at 0.6 s; the nuke's own part explodes it 0.5 s later (`timeNuke_explosion`
    at 1.1 s, its meshes off, gone at 1.5 s), so the entry builds `timeNuke_explosion` and drops skills_a's cued
    explosion. Reason: the precondition shown (Chameleon decision 13 / 26); one source for the blast (parts part 6).
28. The hero does not travel: the Chopper's flight, Flame Turret's turns, Mega Punch / Mega Drill's step back, the Roller
    Machine's roll, the burrow's movement. Barrel Railgun's hop onto the seat is the one exception (decision 40). Reason:
    Penguin decision 8, Bison decision 17 (skills_a item 9, skills_b Q11).
29. No hit is drawn where the reach misses the 10 m target: the Chopper's hits (skills_a Q10), the melee weapons' 2-5 m
    (punch, hammer, drill, saw, tesla coil, roller), Sky Drill's and Sky Shaker's 1-5 m rings. TNT's blasts are not hits:
    they are drawn where the game puts them, 8 n m ahead (TNT 4 at 32 m). Reason: Bison decision 16, the Penguin's Mana
    Arc (skills_b Read this first 5).
30. Unowned followState roots (TTO `barrelRailgun_blast`, `barrelRailgun_rip`) carry `"cut"` = their spawn time. Reason:
    the game's no-owner after-life (tto Q6); no page change.
31. The turret's 13 locks and the pad's 3 locks stay cued (fixed times, steps.txt); the pods' locks are their part's (they
    ride the Kaiser's arms). Reason: tto Q7.

## Summons and the King Kaiser
32. The summons are built and shown, each cut at 10 s: Auto Gyro Gun 4 (create, then root from 0.8 s; **its AI fires at
    the 10 m target**: the first shot 2 s after Awake, then every 2 s: the gun turns, `fire`, `nAttack_fx`,
    `autoGyroGun_fire` at the turret, root 0.7 s later), Barrel Bot 4 (getUp, standby 0.8 s later, root; standing, no
    AI), War Capital (open, root from 1 s; no volleys: its first scan is 12 s after the create). Reason: the Penguin's
    Mana Vortex rule, the Bat's Guardian (skills_a Q1, Q3; parts Q6 and verification 4); Barrel Bot's six-weapon AI is
    gameplay, offered to the user as a separate job.
33. Barrel Cannon without a bot: clip + voice only (the game's own no-bot look); the missing `barrelCannon_ring` and
    `advanceRepair_ring` get no stand-in. Reason: skills_a Q4, Q11 (Bible offers).
34. **The King Kaiser is built** (parts verification 4 overrules parts Q6 / Q8's "its own job"): the clip reader learns
    Unity 3.5's compressed / float curves, the robots load from `Characters/Robots/`, and the Kaiser plays create
    (kaiser_createFx), root from 3 s. Reason: missing parts are always built; kaiserArsenal is released.
35. The Kaiser's colour follows the outfit colour through the new cue option `"pick": "color"` on
    `KingKaiser_r|KingKaiser_g|KingKaiser_b|KingKaiser_k|KingKaiser_w`; an outfit with no colour number (steamSuit) gets
    the first (`_r`), as Fire Barrage's planes. Reason: Skin / 100 (skills_a verification 1, effect_only P1; BB has no
    `KingKaiser_p`, so the game's else would show nothing).
36. The Mole is hidden while the Kaiser stands with the page's `[0, "hideProp", "hero", {"kill": 9.95}]`, not a
    KingKaiser `hideHero` option. Reason: skills_a verification 2 (the hide status turns off every renderer).
37. **Kaiser Arsenal plays on the King Kaiser**: the tile shows the Kaiser already standing at the hero's spot (colour
    pick, option `"clip": "kaiserArsenal"`: that clip once from 0, then root), the Mole hidden for 4.4 s, the pods on the
    Kaiser's own Arm_R / Arm_L (cue option `"host": "KingKaiser"`, the hero's bone as the fallback), wearing its colour,
    the 16 warheads from the pods homing on the target (KaiserWarhead, 12 m/s, 0.4 rad every 0.15 s, hits part-made).
    Reason: the clip is the Kaiser's rig and the move is the Kaiser's (tto Read this first 6, Q4); the precondition shown.

## Passives, ranks, rolls, voices, sounds
38. Passives on, max rank: Combo 4, Charge Attack 3, Speed Drill 2, Super Dig #411, Sky Drill 2 + Sky Shaker #413,
    Landmine 4, Stun Mine 2, Time Nuke 2, Mortar Shot 2, TNT 1-4, Super TNT #422, Stun Grenade 2, Mega Punch 2, Mega Hammer
    2, Mega Drill #433, Grenade Cluster #432, Missile 4 (+ Twin Warhead #453 on the TTO tile), Mine Lover #402, Auto Gyro
    Gun 4 (+ Hidden Turret #403), Barrel Bot 4 (+ Double Bot #423), Bunker 2, Flame Turret 3, Chopper 3 (+ Barrel Cannon
    #443), Reload 2, Fire Barrage 2, Bombardment 2, Synchro Mole 2, King Kaiser (+ #372, #373). Reason: the standing rule.
39. Every look the game gates on `mGameType > 4` (the shells, the cannon sound, superDig_dust, Sky Drill) is shown.
    Reason: the Sheep / Penguin / Cat precedent (attacks_emotes Q6).
40. Barrel Railgun's hop: a **3-axis lift** (`LIFTS.barrelRailgun`: onto the seat 0.63 m up, 0.55 m ahead by 6.55 s,
    seated to 16.65 s, off to 0.8 m left / 0.97 m ahead by 17.07 s), cue `[0, "lift", "barrelRailgun"]` on
    `@BarrelRailgun:assemble1`. Reason: without it the Mole stands inside the turret for 10 s (tto Q2; Apex Hunt's lift,
    Chameleon decision 34).
41. Missile with Twin Warhead's 5 % egg rolled per play as the game does (`p 0.05`, `roll egg` / `!egg` on the launches),
    the egg's eight-way splits made by the missile part. Reason: random picks as the game does them (tto Q3).
42. The Trumpet (`trumpet`, w_mol25) plays the 26-note tune one note per shot through the new option `tune` (a per-class
    counter kept across plays and tiles, reset on a class change, starting on the 2nd note); stage 1 drops the cannon
    sound with it, stages 2-5 keep it (BB's quirk, kept). Reason: attacks_emotes Q5.
43. The worn cannon's own recoil: a new cue kind `propAnim` `[t, "propAnim", "R", {"clip": "fire"}]` at every Normal
    Attack shot (the prop's clip once if it has one, then back to its own loop; `root` at the standby only if the prop has
    a root clip). Reason: missing parts are always built (attacks_emotes Q4 overrules parts Q7's "out"); if the props'
    data lack the clips, the extraction is the video repo's: say so.
44. `dig_dirt` turns to a random yaw drawn per spawn: `rot: "randomYaw"` beside the page's `"random"`. Reason: the code
    (attacks_emotes part 4).
45. The frame-loop timers use the code's nominal intervals for the whole class (superDig_dust 0.1 / 0.3 / 0.5, dig_dirt
    every 0.2 s, King Kaiser's dig_dust every 0.1 s from 0.1 to 1.8 s), not a 60 fps model. Reason: one model per class
    (attacks_emotes verification note); the page has no fixed frame rate.
46. The Chopper's engine: the generic cue option **`playAudio`** (seconds after the spawn when the root's
    playOnAwake-off AudioSource starts, stopped when the effect ends), `[0.3, "fx", "chopper", {"bone": "mount_Cannon",
    "cut": 5.15, "playAudio": 0.4}]`; no `fx:chopper` part. Reason: one generic option beats a class hook (skills_a P3 over
    parts part 9); the 5.15 cut stays inside the 5.2 s clip so the loop toggle cannot carry it into the next round
    (skills_a verification note).
47. Voices with the rip's / TTO's fixes where BB's load fails: Grenade Cluster plays the rip's `granadeCluster1|2`;
    Napalm `mortarShot2` (one file); Barrel Cannon `barrelBot2`; Mega Drill, Detonate's nuke and the TTO Barrel Railgun /
    Kaiser Arsenal silent where the code plays no voice. Reason: Sheep decision 10 (skills_b Q4).
48. Sounds outside the class's `sounds/` are found: the lookup widens to `.ogg` and to `Assets/AudioClip/`
    (`gallonDrill.ogg` for megaDrill_ring, `beep.ogg` for the missile lock, `kaiser_open.wav`, `kaiser_box.wav`). Reason:
    skills_b Q8, tto P15, skills_a P2.
49. Synchro Mole's ring at the hero, `kill: 10`; the summons' green tint and head look are left out. Reason: the 10 s rule,
    no summon in that tile (effect_only Q6).
50. Smart Shell, the mines' hits, `flameCarnival_fire` (never triggered), `timeNuke_explosion` in the mine pool (after
    the 10 s cut), War Capital's volleys (after 12 s): no cue. Reason: they need a foe or come after the cut (effect_only
    Q7, skills_b, skills_a).

## Left out
51. Camera effects (motion blurs, shakes, King Kaiser's zoom and colour ramp, MissilePadLock's shake), the owner's cast
    bars, the on-screen "WarCapital is now operational." message. Reason: Bison decision 35, Cat decision 43.
52. Status looks on a foe (Barrel Railgun's paralysis, King Kaiser's noForce), Advance Repair's heal numbers, Barrel
    Bot's cannon form on the Barrel Cannon tile. Reason: Sheep decision 4, Cat decision 44.

## Parts and data (every missing part is built)
53. `wardrobe_fx.py` LAYOUTS as parts.md's block (verified byte for byte) + the robots' (AutoGyroGun 36, BarrelBot 208,
    BarrelBotAI 8 with a new string type, KingKaiser / KingKaiserAI); `SHURIKEN_FROM_TTO["mole"] = ["bazooka_ring",
    "napalm_ring", "warCapital"]` with no SHURIKEN_MAT entry; `NOT_DRAWN` keeps CharacterControl; `EXTRA_FOLDERS["mole"]`
    the three robot folders. Reason: parts, verified.
54. Prefabs held only in script fields (no Resources path) are exported under the field's name: the Mole prefab's
    `kaiser_dust`, `kaiser_box` (sharedassets8 path ids 387 / 379); the robots' `autoGyroGun_fire`, `nAttack_fx`,
    `create_fx`, `kaiser_createFx`. The other hero-prefab fields (`nAttack_fire`, `nAttack_hit`, `deadEffect`, `chopper*`,
    `missile*`, `synchroMole*`, `timeNuke_explosion`) are in the Resources container and build by name; only the inventory
    misses them. Reason: skills_a P2, parts Read this first 5, attacks_emotes field_keys.
55. The Time Nuke's countdown is drawn as the game does: the GMO24 bitmap font exported to `fx.json` `"fonts"`, the digits
    of floor(60 - age) in (0.8, 0.3, 0.3) in a 30 x 30 px box 1.0 m above the nuke, only within 30 m, centred by the
    measured ink, gone at 59 s or on detonate (60 ... 51 inside the 10 s cut). Reason: parts Q4, skills_b Q9 (skills_a P4's
    "left out" overruled: missing parts are built).
56. The TTO side: `SKILL_FX["mole"]` = tto verification 4's 24 prefabs; the `arcPrefab` references resolved to
    `tto/barrelRailgun_arc`; `barrelRailgun_rip`'s own `root` clip exported; the kaiserArsenal clip added to the King
    Kaiser effect's Animation. Reason: tto P4, P7, P16, decision 37.
57. TTO1102's code with the 2026-11-04 bundles. Reason: Bat decision 44, Chameleon decision 44.
58. Inventory (`wardrobe_fx_inventory.py`, the editor's): BUILT += Mole_nAttack, Mole_mortarShot, Mole_stunGrenade,
    Mole_grenadeCluster, Mole_napalm, Mole_bazooka, Mole_missile, Mole_warMissile, Mole_cartBomb, Mole_mine, Mole_stunMine,
    Mole_flameCarnival, Mole_timeNuke, Mole_warCapital, rotationControl, AutoGyroGun, BarrelBot, BarrelBotAI, KingKaiser,
    KingKaiserAI; the 13 field prefabs and the three grafted systems' NOTES; rerun it. Reason: the recipe's rule.
59. The check (`wardrobe_fx_check.py`, the editor's): KINDS += `propAnim`; OPTS += `tune`, `firePoint`, `tilt`, `pick`,
    `playAudio`, `clip`, `host`, `pair`, `trigger`, `finish`, `ride`, `shots`, `rideEnd`, `tier`, `sink`, `kicks`, `fold`;
    ENTRY_KEYS += `order`, SKILL_KEYS += `standby`; the cue-format comment in index.html learns them. Reason: Cat decision
    58, Chameleon decision 62.
60. The paste-ready blocks to use are the corrected ones: attacks_emotes' (superDig from its verification), skills_a's
    (`@KingKaiser:root` from its verification, with decisions 35-36; the chopper per 46; detonate per 27; dig1's dust per
    45), skills_b's (the five tnt `why` fixes), effect_only's as written, parts' LAYOUTS (the chopper entry is skills_a's),
    tto's section 7 with its verification's missilePad changed by decision 22 (no cued hits, `pair` on each launch) and the
    kaiserArsenal entry by decision 37. The editor pastes them after the builders, merged where two reports touch one key
    (`skyDrill`: either; `superDig`: attacks_emotes').

## Offered to the user for the Bible (not written there)
The Combo's press windows (stage 1 + 0.5 / 0.8 / 1.1 / 1.4 s) and clip starts (0.7 / 1.2 / 1.7 / 2.2 s); the shell's lob
(15 m/s, ~6.75 deg, ~9.8 m in 0.62 s); the Trumpet's Mary Had a Little Lamb from the 2nd note, and stage 1 dropping the
cannon sound while 2-5 keep it; the burrow hiding the hero from 0.6 s, the 12 s auto-surfacing never Sky Drill, Sky
Drill's rings at 0.1 / 0.2 s, the reference's swapped dig-in citations; chat picking only chat1-3, emo_bow / emo_beg /
revive naming voices the data lacks; dig2 never played; advanceRepair_ring and barrelCannon_ring missing from both games;
War Capital's first salvo 12 s after it is built and its 8 s minimum assemble; Advance Repair's first tick at 1 s; the
Chopper's 0.4 s ticks from 1.3 s; Mortar Shot's shells 0.2 s apart (not 0.1); Grenade Cluster silent and ringless in BB
(ringless in TTO); Stun Grenade's blast being nAttack_hit; Mega Drill voiceless; the Cart Bomb's 3 s fuse with no contact
fuse; mines / nukes / Flame Carnival hidden only from enemies, Flame Carnival's trigger lighting the Mole's renderers;
KingKaiser_p missing in BB; warCapital_dead missing; missile_hit drawn with the hero's rotation; Fire Barrage / Bombardment
planes coloured by the hero's colour and their spots; Barrel Railgun's assembly steps, hop, seat and shrink; the TTO
missiles' 8 m/s and 72-degree climb (hits 2.55-3.57 s), the egg keeping the gold blasts and the splits making them too;
Kaiser Arsenal's 12 m/s warheads and pod timings.
