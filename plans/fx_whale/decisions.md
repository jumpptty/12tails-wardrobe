# Whale effects: decisions (2026-11-13), decided overnight, for the user's review

The user asked for the build ("build the Whale") and was then not available, so the planner decided every open question
in the six reports in this folder (attacks_emotes, skills_a, skills_b, effect_only, parts, tto), each read with its
"## Verification" (the verification wins where the two differ). Rules used, in this order: the standing rules (top rank,
passives on; random picks as the game makes them; enemy effects at the 10 m target point, homing aims 0.6 m up; long
buffs / fields / summons cut at 10 s; a tile per skill with its Bible icon, pool members one each, effect-only tiles on
the idle stance; missing parts always built; TTO cues only for the released `clap`, `leviathanCall`, `wai`: all three are
in `wardrobe/tto_released.json`), the page's SEQ rule (a charge = full charge, a channel = its duration, at least 3 s for
a hold until the player acts; high INT: every cast bar at magAdjust's 0.1 s floor), then the Wolf's, Sheep's, Penguin's,
Bat's, Bison's, Cat's, Chameleon's, Mole's, Monkey's, Panda's and Rabbit's decisions by analogy, then the reports' own
recommendations. Every item is **decided overnight, for the user's review**: any of them can be turned round later.

Already in the tree (checked 2026-11-13 at home; nothing to rebuild for the Whale): the `hideProp` kind (slots `R` / `L`
/ `hero`), the `"sound"` kind, `p` / `roll` / `!roll`, `everyCycle`, `vol`, a followState `cut` written on a later step's
clock or at its step's end (it comes at the step change), `kill`, `replace` (the Rabbit's: every living copy disposed at
the spawn), `atBone` (the Panda's: the effect put once at a hero bone's position, not parented), x / y / d as `[lo, hi]`,
`api.spawn` + an entry's `"builds"`, `api.propModel` + `PROP_STARTER`, `api.boneMatrix`, `fx.cutNow()`, mesh.js's
`fxAnim.play(name, fade, wrap)` / `rewind()`, bat.js's `fx:castRing`, the Shuriken graft matched by material (the
Chameleon's route, no SHURIKEN_MAT), cat.js's `trajectoryVector` / `lookEuler` exports, the Fx floor clip (the Panda's
`floor`), groundhug.js / shuriken.js / uvscroll.js / tto_sheep.js's TrailRendererModern / mesh.js's skinned meshes, the
OPTS words `slot`, `end`, `standing`, `release`, `to`, one-step SEQ lines and entries with no cues. Probed here before
deciding: TTO's five Leviathan Breach prefabs export from the home bundles (`tto_assets/2026-11-04`, no warning, the node
numbers of parts.md / tto.md), and BB's `javelin`, `flyingShield`, `homingShield`, `grandTide`, `castRing` export too.

## Tiles and sequences
1. Normal Attack: `"Normal Attack: nAttack1@0.8 nAttack2@1.0 nAttack3"` (2.7 s); stages 2-3 cut in, the first step keeps
   the page's 0.2 s fade. Reason: only stage 1 writes actionTime, so the clips start at 0.8 / 1.8 s (attacks_emotes Read
   this first 1, verified; Bat decision 28).
2. Entended Wave (#401) gets no tile: `extendedWave1-3` ride the three stages at their 0. Reason: always on with no roll,
   as the Mole's Super Dig (Mole decision 2; attacks_emotes verification 8).
3. Charge Attack: `"Charge Attack: cAttack1 cAttack2*@2.29 root~@0.2"` (released at 2.99 s, the plain lowering; no cue on
   `cAttack2` or `root`). Reason: the test is `actionTime + 3 <= Time.time`, so 3.0 s is already Shield Bash: the Mole's
   decisions 2-3 mirrored (attacks_emotes Q1).
4. Shield Bash (#114) gets its own tile `"Shield Bash: cAttack1 cAttack2*@2.3 shieldBash~"` (released at 3.0 s); there is
   no single `shieldBash` tile, its cues stay on the plain `shieldBash` key. Reason: one tile per skill, the passive that
   replaces the release shown with its hold (Mole decision 3; attacks_emotes verification 7 overrules skills_b Q7).
5. Knight of the Deep (#273) gets its own tile `"Knight of the Deep: cAttack1 cAttack2*@2.3 shieldBash~"` (keys
   `@KnightoftheDeep:cAttack1` / `:cAttack2`) with the six knights already standing and guarding (decision 40). Reason: a
   passive with a precondition gets a tile with the precondition's look (Chameleon decision 13; attacks_emotes Q2).
6. Shield Reflect (#411) gets its own tile `"Shield Reflect: cAttack1 cAttack2*@2.29 root~@0.2"` (key
   `@ShieldReflect:cAttack2`): `shieldReflect` at the cAttack2 step's 0, on every play. Reason: a passive started by a hit
   gets a tile that procs every play (the Penguin's Frost Spike, Bison decision 6; attacks_emotes verification 4).
7. Auto Shield (#261-263) gets the effect-only tile `"Auto Shield: root*@1"` (key `@AutoShield:root`), `shield` on every
   play, no `p`. Reason: no clip and no tile where the Whale is hit (effect_only Q1; Frost Spike, Cat decision 35).
8. Wall Puncture (#251-254) gets its own tile `"Wall Puncture: peninsulaImpale"` (key `@WallPuncture:peninsulaImpale`:
   every stab's hit is the proc), and Peninsula Impale becomes the one-step `"Peninsula Impale: peninsulaImpale"` (its
   cues on the plain `peninsulaImpale` key, with the 40 % rolls). Reason: Peninsula Impale's 12 m box is the only host
   whose hits reach the 10 m target; the Chameleon's Critical Plus shape (Chameleon decision 12; attacks_emotes
   verification 5, effect_only verification 2). A clip a SEQ plays leaves the single-clip list, so the host needs its line.
9. Cast: `"Cast: cast1 cast2*@0 cast3~"` stays; `cast3` is a pool of eight (Bubble Shield, Heavy Weight, Hydro Blast,
   Rejuvenate, Call To Arm, Salvation, Megalodon, Revitalize), one tile per member. Reason: every class's Cast tile
   (Chameleon decision 7); the bar is 0.1 s with Reduced Cast and high MAG (skills_a, verified).
10. Honor, 12th Kingdom Knight and Bubble Burst get one-step tiles `"Honor: cast3"`, `"12th Kingdom Knight: cast3"`,
    `"Bubble Burst: cast3"` (keys `@Honor:cast3`, `@12thKingdomKnight:cast3`, `@BubbleBurst:cast3`). Reason: they play cast3
    from the key press with no channel (Sheep decision 17, Chameleon decision 6; parts verification 1).
11. The `flyingShield` clip is a pool of two (Flying Shield, Homing Shield), one tile each. Reason: the standing rule.
12. Whale Wave is the `divingWave` tile and Mal Storm the `divingStorm` tile; `LOWER_RANK.whale = ["malStorm"]`, no
    `malStorm` entry; Diving Press (#443) gets no tile. Reason: with the passive on, the malStorm clip is never played
    (Monkey decision 6; skills_a Q2, skills_b Q1).
13. `"Bowling Whale: bowlingWhale1@1 bowlingWhale2*@6"` and `"Grand Tide: grandTide1 grandTide2*@3 grandTide0"` stay as
    they are; no cue key for `bowlingWhale2`, `grandTide2`, `grandTide0` or the plain `cast2` (skills_b's empty
    `grandTide2` entry is dropped: nothing depends on it). Reason: the code matches the lines, and those steps load
    nothing (skills_a Q13, skills_b verification 4, Q11).
14. Leviathan Breach (TTO, released): `"Leviathan Breach: cast1@0.1 cast2*^@0 leviathanCall^"`, keys
    `@LeviathanBreach:cast1`, an empty `@LeviathanBreach:cast2`, the plain `leviathanCall`; the 2.4 s clip plays whole
    (the game frees her at 0.75 s). Reason: tto Read this first 1-2, verification 6; Chameleon decision 11.
15. Cues past a clip's end run in the idle tail, as the game does them after the standby: Megalodon's shark at 4.0 s,
    the Rejuvenate / Revitalize ticks, the bubble, the knights, the Homing Shield, the stuck javelin, Leviathan Breach to
    4.15 s (its effects to 9.95 s). The วนซ้ำ toggle cuts the cued ones (not the part-made). Reason: the page-wide limit
    of Chameleon decision 11 and Mole decision 21; holding the clip's last pose instead would be wrong for a free hero.
16. Passives with no tile of their own, because they ride a skill's cues: Tide Cutter (Sweep), Spiral Blast (Hydro
    Blast), Peninsula Asunder (both Peninsulas), Diving Press, Over Weight, Honor Stand, Wonder Belly, Reduced Cast;
    because they draw and say nothing: Last Hope (its two voices exist in neither game), Harden Skin, Over Presence, the
    stat and size passives. Reason: the Mole's passives table (effect_only, verified; Q2).
17. Page lines. `SEQ.whale` = `["Normal Attack: nAttack1@0.8 nAttack2@1.0 nAttack3", "Charge Attack: cAttack1
    cAttack2*@2.29 root~@0.2", "Shield Bash: cAttack1 cAttack2*@2.3 shieldBash~", "Knight of the Deep: cAttack1
    cAttack2*@2.3 shieldBash~", "Shield Reflect: cAttack1 cAttack2*@2.29 root~@0.2", "Cast: cast1 cast2*@0 cast3~",
    "Honor: cast3", "12th Kingdom Knight: cast3", "Bubble Burst: cast3", "Bowling Whale: bowlingWhale1@1
    bowlingWhale2*@6", "Grand Tide: grandTide1 grandTide2*@3 grandTide0", "Peninsula Impale: peninsulaImpale", "Wall
    Puncture: peninsulaImpale", "Leviathan Breach: cast1@0.1 cast2*^@0 leviathanCall^", "Auto Shield: root*@1"]`.
    `SEQ_SKILL.whale = { "@ShieldBash": "shieldBash", "@KnightoftheDeep": "knightOfTheDeep", "@ShieldReflect":
    "shieldReflect", "@WallPuncture": "wallPuncture", "@AutoShield": "autoShield", "@Honor": "honor",
    "@12thKingdomKnight": "12thKingdomKnight", "@BubbleBurst": "bubbleBurst", "@LeviathanBreach": "leviathanBreach" }`.
    `wardrobe_skill_icons.py`: `CLIP_SKILLS["whale"] = {"divingWave": ["whaleWave"], "divingStorm": ["malStorm"],
    "gobble": ["gobbleUp"], "leviathanCall": ["leviathanBreach"]}`; `OWN_TILE["whale"] = {"honor": ["cast3"],
    "12thKingdomKnight": ["cast3"], "bubbleBurst": ["cast3"], "knightOfTheDeep": ["cAttack1", "cAttack2", "shieldBash"],
    "shieldReflect": ["cAttack1", "cAttack2", "root"], "wallPuncture": ["peninsulaImpale"]}`; `EFFECT_ONLY["whale"] =
    ["autoShield"]`; `RANK_ICONS["whale"] = {"12thKingdomKnight": "whale_12thKingdomKnight2"}` (the key starts with a
    digit, which the icon regex cannot read). Reason: the four reports' page lines merged (attacks_emotes verification 3
    and 6, skills_a verification 1, tto verification 7, effect_only block 4).
18. KO: `ko1|ko2`, or on half the plays `dead1|dead2` with `deadEffect` (roll `dead` / `!dead`); getUp: `revive` on half
    the plays. Reason: Sheep decision 11, the Wolf's and the Cat's shapes (attacks_emotes, verified).
19. Emotes as attacks_emotes' block: wave `hi|wave`, bow `ty|bow`, talk takes the chat's `chat1-5`, sleep, cheer, beg,
    cry, battle; laugh, sit, dance, every pose and the TTO-only emote clips (`clap` and `wai` too, though released) are
    silent. Reason: the code and the data (no such voice in BB or TTO); Bat decision 36.
20. The run's footsteps: `step_heavy1` at 0.1 and 0.6 s of every cycle (`"sound"`, `"everyCycle": true`). Reason: the
    clip's AnimationEvents, as the Bat's wing flap and the Chameleon's steps.
21. No tile and no cue: activateIcon1 (the mission channel), RPC_cAttack0 (a release under 1 s), the SP-0 auto release,
    game code 967's item attack. Reason: Penguin decision 19, Cat decision 35.

## Where things land
22. No hit is drawn where the reach misses the 10 m target: the Normal Attack's 7 m box, Shield Bash's 3 m, Round Table's
    4 m pulse, Sweep's 6 / 5 m, Shield Rush's 2 m box, Peninsula Round's 4 m, Grand Tide's 3 m, Bowling Whale's 3 m,
    Whale Wave's 9 m, Call To Arm's and Bubble Burst's blasts (hits only). Reason: Bison decision 16, Mole decision 29.
23. Peninsula Impale's ten hits land at d 10, y 1 (1.0 + 0.3 k s), each with one roll: `wallPuncture_hit` + its sound at
    p 0.4, else `nAttack_hit` + its sound (rolls `impaleWp1-10` / `!impaleWp1-10`); the ten `asunderImpale` at the hero at
    0.8 + 0.3 k. Reason: the 12 m Asunder box; lckAdjust(40) at LCK 1 (skills_b, verified; Cat decisions 40 / 41).
24. Javelin: thrown from (x 1.2, y 2.2, d 1) at `rot [2.878, -7.595, 0]` (getTrajectoryVector at the body's centre, 24
    m/s), `slot: "R"` kept on the cue; it passes through the target with no hit drawn, sticks in the floor about 11.9 m
    ahead at 0.46 s and stands to its 3 s life. Reason: the code; `javelin_hit` is never spawned and BB has no such
    prefab (skills_b item 3, verification 3; parts part 1).
25. Flying Shield draws no hit: its 1 m trigger passes 1.64 m from the target body, and the part still tests the contact;
    the cue takes no `to`. Reason: as the game at this target, the Mole's untriggered Flame Carnival (parts Q1; skills_a
    verification 2).
26. Homing Shield homes on the body's centre (0, 0.6, 10), the part's default, and spawns `flyingShield_hit` on every
    pass through the body until its 3 s life; the cue is `{"y": 1, "d": 1}` with no `to` and no `kill`. Reason: Penguin
    decision 3; the game's repeat hits (skills_a Q9, verification 2).
27. Enemy-target casts at the 10 m point: Heavy Weight's `heavy` (`d: 10`, the enemy case), Hydro Blast's `spiralBlast`
    (`d: 10`, scale 1.3), Megalodon's `megalodon_ring` at 0 and `megalodon` at 4.0 s (`d: 10`, scale 1.5). Reason: the
    effects-on-enemy rule (skills_a Q1).
28. Ally-target casts are shown as self-casts: Bubble Shield (`bubbleShield_cast` and `bubbleShield` at y 1.3, scale 1.2,
    `kill: 10`, `replace: true`: one bubble, the status is one), Rejuvenate, Revitalize (herself included). Salvation
    shows only its ring (the code leaves the caster out). Reason: Penguin decision 1; the Mole's Barrel Cannon for a look
    with nobody to receive it (skills_a Q4; parts verification 6 for the 1.2 and the 1.3).
29. Call To Arm assumes an ally at the 10 m point: `callToArm_ring` 8 m behind her (`d: -8`, where she left) and at her
    (where she lands), both at 0.5 s. Reason: each effect with its owner in the hero-stays frame (Bat decision 8;
    skills_a Q3).
30. Preconditions assumed, where the skill cannot be cast without them: Bubble Burst pops her own Bubble Shield
    (`bubbleBurst` at y 1.3; no bubble is shown first, it goes in the same frame), Gobble Up spits a swallowed target
    (`gobbleUp_hit` at d 1, APPROXIMATED), Swallow has Gobble Up learned and catches the pulled target at d 1, y 0.6
    (APPROXIMATED: the pulls bring a 10 m target into the 2 m grab box). Reason: Mole decision 27, Chameleon decision 26
    (skills_a Q5, Q6; skills_b Q2, Q3, verification 6).
31. Mal Storm's 24 bolts use the new cue option `around: [lo, hi]`: a whole-metre radius and a whole-degree angle drawn
    per cue when the clip starts (`[3, 5]`, and `[5, 8]` for Diving Press's second bolt), `y: 12`, identity. Reason: random
    picks as the game makes them; `spread` draws a square (skills_a P4, verification 3). The bolts draw 12-22 m up, as
    the game puts them.
32. Peninsula Round's 28 `asunderRound` rings are left where the lance hand was: the existing `atBone: "mount_Hand_R"`
    with the new flag `withRot: true` (the bone's rotation too, the cue's `rot` after it) and `rot [0, 0, [-30, 29]]` (a
    rot element `[lo, hi]` = a whole number drawn per cue). Reason: `Instantiate(prefab, hand.position, hand.rotation x
    Euler(0, 0, Random.Range(-30, 30)))`, not parented (skills_b Q8, verification 2). The reports' word `boneAt` is not
    added: the page already has `atBone` for the same one-time spawn, and two look-alike words would be a trap.
33. The hero does not travel: the swings' steps, Sweep's and Shield Rush's dashes, the Peninsulas' advance, Bowling
    Whale's roll, Grand Tide's ride and its closing slide, Call To Arm's teleport. Reason: Penguin decision 8.
34. Fixed spots: Auto Shield's `shield` at d 1, y 1; Shield Reflect's `shieldReflect` at d 0.7, y 1; `shieldRush_ring` at
    y 1.3 (her body's centre); `honor_cast` at y 2 with `kill: 1` (the game never destroys it); the rejuvenate ticks and
    `bubbleBurst` at y 1.3. Reason: the code's numbers (effect_only, attacks_emotes verification 4, skills_b Q6, skills_a
    Q11).
35. Leviathan Breach at the 10 m target: 3 hops; the warning circle at d 10 (`kill: 4.25`); the slam 0.75 m left and
    0.9 m ahead at 0.6 s; three dolphins from d 1.5 (x 0 / -1.43 / 1.43) to d 9 (x 0 / -2.2 / 2.2) at 0.55 / 0.65 /
    0.75 s; the Leviathan at d 10 at 1.95 s, its crash at 4.15 s. Reason: the game's own count and lanes at this target
    (tto Read this first 3, verification 5, 6).
36. The body stays the size the page draws (Whale_tri scale 1; y 1.3 is its centre), not the 1.05 of Super Size 4 + Mega
    Size. Reason: a body-size change is outside the effects work; told to the user (effect_only Q5).

## Summons and special
37. **The six knights are built and shown** (12th Kingdom Knight 2: six `kingdomKnight2`): each rises from 1 m under the
    floor to its slot with its `kingdomKnight_ring2` (part-spawned), stands on its `root` loop, and at `end: 10` plays
    `unsummon` and goes 1 s later. The rise is y = -e^(-4 t) (the code's `Lerp(.., 4 dt)` without a frame rate). Reason:
    missing parts are always built; the summons rule (Monkey decision 30; parts Q2, skills_a Q7; Mole decision 45).
38. A recast replaces the knights: `"replace": true` on the slot-0 knight cue (the first of the six), so the older six go
    as the new six arrive; their 1 s unsummon on a recast is not shown. Reason: RPC_kingdomKnight unsummons the old
    knights (Whale.cs:28799); without it the วนซ้ำ toggle would stack six more every 1.2 s (the Rabbit's `replace`).
39. No knight volley is cued (every 3 s, only while she is not attacking, on the nearest enemy within 8 m: the target is
    10 m away); the part's `attack` option is built and unused. Reason: parts Q2, skills_a verification 7; Mole
    decision 26.
40. Knight of the Deep's tile shows the six knights standing from 0 (`standing`, no rise, no ring) and guarding: `guard:
    [0, T]` with T = 3.0 / 3.1 / 3.2 / 3.3 / 3.4 / 3.0 for slots 0-5 (a first wait of 0.1 x slot, then every 0.5 s a
    random flat facing and its `cAttack` clip, back to `root` at T), `kill: 3.8` (the tile's end); `roundTable1` and the
    voice `roundTable` at 0, `roundTable_ring` at the cAttack2 step's 0 with `cut: 2.3`. Reason: attacks_emotes
    verification 2; the precondition shown (Monkey decision 34).
41. Grand Tide's wave: `[1, "fx", "grandTide", {"release": 4}]`: `fx:grandTide` plays `root` looped at age 1.0 and calls
    `fx.cutNow()` at age 4 (the `destroy` clip and the 1 s after-life over grandTide0); its two Unity 3.5 ParticleSystems
    are grafted from TTO's copy. Reason: a cue's `cut` cannot cross two step edges; parts' interface (skills_b
    verification 1, parts Q4; `anims` / `end` are not used).
42. Bowling Whale's ball: `bowlingWhale` at 0.5 s with `cut: 5.95` on bowlingWhale2's clock; the hero is not hidden.
    Reason: fxStart keeps a later step's cut, and the coroutine has no Renderer line (skills_a, verified).
43. The cast ring: BB's channel cues `castRing` at 0.1 s with `rot [270, 90, 0]`, `cut: 0.55` (the hook's 0.5 s restart
    never comes); Leviathan Breach's is BB's `castRing` too, `cut: 0.1`, with the new `animLoop: "root"` (its `root` clip
    looped from the spawn). Reason: Sheep's shape (skills_a verification 4); TTO's copy draws as BB's (tto verification
    1, 4).
44. **The Leviathan and the dolphins are built** (TTO's `WhaleLeviathan`, `WhaleDolphin`): the keyed rise, breach and
    dive with tail flex and fade, the geyser / trail / crash / pool children switched on at their times with fresh
    clocks; each dolphin's hops along its lane, a fresh splash at each landing. Reason: missing parts are always built;
    `leviathanCall` is released (tto P1, P2; every constant is in the instructions, tto verification).
45. What is under the floor is hidden, as the game's ground hides it: the rising knights, the stuck javelin's buried
    tip, the dolphins' and the Leviathan's bodies (from 1.4 m and 9 m under it). The page exposes its floor clip to the
    parts (`fx.clipFloor(node)`); the parts clip only those bodies, never the ground discs. Reason: the Panda's `floor`
    (Panda's QA); the page's floor hides nothing by itself.

## Passives, ranks, rolls, voices, sounds
46. Passives on, max rank: Combo (#101, #102) + Entended Wave #401, Charge Attack 3 + Shield Bash #114 + Shield Reflect
    #411, Auto Shield 3, Wall Puncture 4, Sweep 2 + Tide Cutter #402, Javelin 2, Shield Rush 2, Flying Shield 2, Homing
    Shield #422, Swallow 2 + Gobble Up #233 + Wonder Belly #432, Peninsula Impale 2 and Peninsula Round 2 + Peninsula
    Asunder #442, 12th Kingdom Knight 2 + Knight of the Deep #273, Honor 4 + Honor Stand #412, Bubble Shield 4 + Bubble
    Burst #403, Heavy Weight 2 + Over Weight #413, Hydro Blast 4 + Spiral Blast #423, Rejuvenate 4 + Revitalize #433,
    Call To Arm, Salvation 2, Megalodon 2, Whale Wave 2 and Mal Storm 2 + Diving Press #443, Bowling Whale #434, Grand
    Tide, Reduced Cast #373. Reason: the standing rule.
47. Every look the game gates on `mGameType > 4` (extendedWave1-3, Shield Bash, the voices' mission gates) is shown.
    Reason: the Sheep / Penguin / Cat / Mole precedent (attacks_emotes Q4).
48. Rolls as the game makes them: one Wall Puncture roll per Impale stab (p 0.4); every two-voice skill picks one of its
    two; the chat picks chat1-5; KO / dead and getUp / revive at even chance. Auto Shield, Shield Reflect and the Wall
    Puncture tile proc on every play (their tiles are the proc). Reason: random picks as the game; decisions 6-8.
49. Round Table's own voice: TTO's fix, `[0, "sound", "roundTable1|roundTable2"]` at the cAttack2 step's 0 (BB asks
    for Voices/ files it lacks; both are BB's own sounds/). Reason: Sheep decision 10, Mole decision 47 (attacks_emotes
    verification 1 reverses its Q3).
50. Rejuvenate's heal tick (`rejuvenate_hit`, once every 4 s on the status clock at a phase the cast does not set) is
    cued at the mean: 2 s after the status, then 4 s on (2.3 / 6.3 s; Revitalize 2.5 / 6.5 s). Reason: Bat decision 16
    (skills_a Q10).
51. Hero-played sounds are `"sound"` cues: `nAttack1-3`, `roundTable1`, `cast2`, `honor` (`vol: 2`), `sweep`, `swallow`,
    `nAttack_hit`, `wallPuncture_hit`, `step_heavy1`, and Leviathan Breach's `grandTide_ring`, `shieldBash_hit`,
    `whaleWave`, `grandTide`, `bowlingWhale` (all BB's rip). The effects' own AudioSources come with them (`heavy`'s
    `reduce` is found in the Rabbit's sounds by the rip walk). Reason: the code's PlayOneShot (reports, verified).
52. Durations at CHA 1, cut by the 10 s rule: Bubble Shield 12 -> 10, the rejuvenate status 18 -> the ticks inside 10,
    the knights 60 -> `end: 10`; Homing Shield and noShield 3 s; Megalodon ends at 7 s, the Leviathan at 9.95 s (whole).
    Reason: the 10 s rule is per buff / summon.
53. The javelin and the Homing Shield fly on the 0.02 s step, not on frame time. Reason: the same flight on a long
    first frame (the Mole editor's fix for its missiles; parts Q6, skills_b Q10).
54. The thrown lance and both flying shields are fresh copies of the worn piece (slot R the lance, slot L the shield;
    the starter `noviceLance` / `noviceShield` with nothing worn: `PROP_STARTER.whale`), their weapon_fx particles
    along; the worn piece is hidden meanwhile: `hideProp R` 0.5 s (Javelin), `hideProp L` 1 s (Flying Shield) and 3 s
    (Homing Shield), meshes only (no `all`). Reason: the game copies mWep2 / mWep1 and switches off the MeshRenderers
    (parts Read this first 4, Q5; Chameleon decision 50).
55. TTO1102's code with the 2026-11-04 bundles at home; Leviathan Breach has no voice, and the cast's BB voice `cast` is
    kept off its tile by the `@LeviathanBreach:cast1` key. Reason: Bat decision 44, Mole decision 57; the three TTO
    builds have the same method sizes (tto verification).

## Left out
56. Camera effects: the screen warps (Bubble Shield, Honor, Bubble Burst, Bowling Whale), the motion blurs (Megalodon,
    Wall Puncture, Peninsula Round), every shake, Leviathan Breach's `iceRamp` tint and Row6Shakes, the cast bars.
    Reason: Bison decision 35, Cat decision 43.
57. Looks that need a foe or an attacker beyond the tiles above: every hit effect out of reach (decision 22), the plain
    `shield` block look while charging without the reflect, the swallowed target's body, `wet` and the whirlpool's pull,
    the salvation bubble on allies, Honor's emblem on other allies, the `overPresence` slow. Reason: Sheep decision 4,
    Cat decision 44.
58. Not in either game's play or not released: the TTO passives' looks (Sovereign Impaler, Oceans Resilience: not in the
    released list), the Bible's eight Reborn-only Whale skills, the 13 supplement skills (`sup_*`), the `divingStorm`
    effect prefab and the orphan voices no code loads, `javelin_hit` / `bowlingWhale_hit` (no prefab in BB). Reason: the
    released-list rule (Mole decision 15); effect_only verification 4; Chameleon decision 54.

## Parts and data (every missing part is built)
59. `pipeline/wardrobe_fx.py`: parts.md's LAYOUTS block (`whale_kingdomKnight: [("kingdomKnight_ring2", "r")]`, the four
    empty ones) and `SHURIKEN_FROM_TTO["whale"] = ["grandTide"]` with no SHURIKEN_MAT entry (BB Water2 / Splash3 matched
    to TTO's by material). Reason: parts, verified; the Bison's, Cat's, Chameleon's and Mole's grafts must build as before.
60. `wardrobe/fxparts/whale.js` (new): `Whale_javelin` (the lance copy, 24 m/s under gravity, the stick, 3 s),
    `Whale_flyingShield` (the shield copy on the clip-driven node, the 1 m contact test), `Whale_homingShield` (the copy
    at Euler(0, 0, 90) spinning 1200 deg/s, 12 m/s, 4 rad/s, y x 0.2, a hit per pass, 3 s), `whale_kingdomKnight`
    (options `slot`, `end`, `standing`, `guard`, `attack`), `fx:grandTide` (`release`). One target body for all of
    them: the Bat's capsule (axis (0, 0.4-0.8, 10), radius 0.3). Reason: parts parts 1-4, 6 and verification 8.
61. `wardrobe/fxparts/bat.js`, `fx:castRing` only: `"whale"` let through the class gate, and a cue's `animLoop` played
    looped at the first update with the 0.5 s restart skipped. Reason: parts part 7, tto verification 4.
62. `wardrobe/fxparts/tto_whale.js` (new): `WhaleDolphin` (the cue's spot = the lane's start, `to`, `hops`) and
    `WhaleLeviathan`, from tto.md's P1 / P2 numbers. A dolphin's splash is a fresh effect per landing with its own
    clock (made inside the part: the same prefab spawned in a splash-only mode, or a sub-effect handed to `api.spawn` as
    `opts.data`), so the extractor needs no sub-prefab export. Reason: tto P1, P2 and its note on fresh clocks.
63. `wardrobe/index.html`: decision 17's lines; `PROP_STARTER.whale`; `FX_PART_FILES += "whale", "tto_whale"`; cueOf's
    `around`; rotOf's `[lo, hi]` element; `withRot` beside `atBone`; `fx.clipFloor(node)` for the parts; the cue-format
    comment's dated Whale lines. Reason: one owner for the page.
64. `pipeline/wardrobe_fx_tto.py`: `SKILL_FX["whale"]` = the five TTO prefabs (`leviathanBreach_warn`,
    `leviathanCall_raise`, `leviathanCall_slam`, `leviathanBreach_dolphin`, `leviathanBreach`); no TTO castRing, no TTO
    sound. Reason: parts verification 5, tto P4.
65. Inventory (`wardrobe_fx_inventory.py`, the editor's): BUILT += `Whale_flyingShield`, `Whale_homingShield`,
    `Whale_javelin`, `whale_kingdomKnight`, `Whale_overPresence` (data only: an aura's trigger); NOTES += grandTide's
    graft; the ten prefabs it misses (`bubbleShield`, `salvation`, `heavy`, `honor_cast`, `shield`, `shieldReflect`,
    `rejuvenate_hit`, `kingdomKnight_ring2`, `overPresence`, `divingStorm`) noted; rerun it. Reason: the recipe's rule.
66. The check (`wardrobe_fx_check.py`, the editor's): OPTS += `guard`, `attack`, `around`, `withRot`, `animLoop`, `hops`;
    a rot list may hold a `[lo, hi]` pair. Reason: Cat decision 58.
67. The paste-ready blocks to use are the corrected ones: attacks_emotes' block with its verification's
    `@KnightoftheDeep:cAttack1` / `:cAttack2`, `@ShieldReflect:cAttack2` and `@WallPuncture:peninsulaImpale`; skills_a's
    block with its verification's `@12thKingdomKnight:cast3` (+ `replace` on slot 0, decision 38) and `flyingShield`,
    `bubbleShield` with `replace` (decision 28); skills_b's block with its verification's `grandTide1`, `peninsulaRound`
    with every `"boneAt": "mount_Hand_R"` written `"atBone": "mount_Hand_R", "withRot": true` (decision 32), no
    `grandTide2`; effect_only's `@AutoShield:root`; tto's section 7 as written. Where two reports hold one key
    (`shieldBash`, `javelin`, `flyingShield`, `grandTide1`, `@12thKingdomKnight:cast3`): the cues are the same, either
    why. The editor pastes them after the builders.

## Offered to the user for the Bible (not written there)
The combo's clip starts (0.8 / 1.8 s; the reference's "stage 3 at 2.4" line is a slip), its voices at 0.2 / 0.2 / 0 s and
swing sounds, stage 3's press window, Entended Wave's bursts 4 m ahead on the hit times; the Charge Attack's under-1 s
release lowering the shield, the 1 s wait before a new charge, cAttack2 from 0.7 s; Shield Bash's timeline; Round Table's
ring and sound from the charge's 0.7 s, its missing BB voices (TTO plays them from sounds/), the knights' guard (a 0.1 s
x slot wait, a random facing every 0.5 s) and their volley only while she is not attacking, on a foe within 8 m; the
knights' slots and their rise from under the ground, rank 1 = four of the kingdomKnight1 look; Auto Shield's spot (1 m
toward the attacker, 1 m up) and its +2 SP per rank; Shield Reflect's spot; Last Hope silent in both games; Over
Presence's aura drawing nothing; Flying Shield's 1 s loop out to 11.98 m and back, 3.5 m to each side, missing a target
inside the loop; Homing Shield flying on after a hit and hitting again each pass; the javelin as a copy of the worn lance
that sticks in the ground and draws no hit (`javelin_hit` missing, as `bowlingWhale_hit`); Mal Storm's 12 strikes (24
bolts with Diving Press) and its four hits; Whale Wave at 0.7 s; Peninsula Impale's stabs 0.3 s apart (not 0.2: +0.6 m
each); Peninsula Round's hand rings; Grand Tide's wave timeline; Shield Rush's ring on the body's centre; Swallow's
standby at 2.9 s; Rejuvenate's 4 s tick clock; the unused `divingStorm` prefab and the orphan voices (honorStand1-2,
peninsulaAsunder1-2, penninsulaImpale1-2, giganticStrike, finalMove, transform, voices/shield); the footsteps
(`step_heavy1` at 0.1 / 0.6 s) and the emote voices the Whale has and lacks, pose15's 0.5 s fade; Leviathan Breach's look
and sound timeline (the warning circle 8 m in radius, the slam, the dolphins' 2.5 m hops, the Leviathan's keyed breach,
the cast ring's `cast1` sound), its 0.1 s bar with Reduced Cast.
