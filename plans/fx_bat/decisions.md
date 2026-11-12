# Bat effects: decisions (2026-11-13), decided overnight, for the user's review

The user was asleep, so the planner decided every open question in the six reports in this folder (attacks_emotes,
skills_a, skills_b, effect_only, parts, tto), each report read with its "## Verification" (the verification wins where
the two differ). Rules used: the standing rules (top rank, passives on; random picks as the game makes them; enemy
effects at the 10 m target point; homing aims 0.6 m up; target-rotation effects rot [0, 180, 0]; long buffs / fields
cut at 10 s; a tile per skill; missing parts always built; TTO cues only for the released `nightfallSwarm`), then the
Wolf's, Sheep's and Penguin's decisions by analogy, then the reports' own recommendations. Every item is **decided
overnight, for the user's review**: any of them can be turned round in the morning.

## Where things land
1. Normal Attack bolts end on the ground at the 10 m target point (centre 0.6062 s, side bolts 0.6276 s at x +-3.44):
   Penguin decision 1 / Sheep decision 3, and here it is also the game's own untargeted shot (attacks_emotes Q1).
2. Drain Life's tick flash `drainLife_hit` at the target point 0.6 m up, not at the Bat's feet: the network copy and the
   clones draw it there, the own-client spot is a BB / TTO bug (attacks_emotes Q2; offered for the Bible).
3. Black Servant's servant ring on the standard target body: y 1.1, scale 0.7 (skills_a verification correction 2:
   Penguin decision 3's 0.6 m centre, height 1, radius 0.3 is every class's target body).
4. The target body for contact tests and ClosestPointOnBounds is that same body (centre 0.6 m up, height 1, radius 0.3):
   Echoes' hits at d 9.7 (parts verification correction 1), the guardian's two hits at (0, 1, 10.3) / (0, 1, 9.7)
   (parts Q4): one body for every Bat cue.
5. Mirage Orb with Distant Orb at the target's feet (d 10, no rot), ending with its 11th tick at 5.0 s; without a target
   the part's `kill` 10 covers it (skills_b Q1, parts part 3: passives on).
6. Shadow Gaze's `demonGaze_hit` at the target's centre, `{"d": 10, "y": 0.6}` (effect_only Q4: collider.bounds.center =
   0.6 m up).
7. Dark Stalker's mesh approximated on the Penguin-sized body: d 10, y 0.35, rot [0, 180, 0], kill 10 (skills_b Q3's
   recommendation; the exact Hip_L bind pose would need a target model the page has not).
8. Switch in the hero-stays frame: one `switch_hit` at the hero and one at each clone's summon spot (x -+1.5, d 2.6), no
   roll, no clone bodies (effect_only verification correction 5: as Blink and Swap, each effect with its owner).
9. Shadow Sacrifice: the ring at the hero and the two clones' `illusion_dust` at their summon spots, no clone bodies
   (effect_only Q1: a clone that pops in only to vanish reads worse than the dust).
10. Nightfall Swarm in place (TTO variant A): the Bat hidden 0.4-0.9 s, the bats fly the 12.5 m road through the 10 m
    target and regather to her chest where she stands (tto Q1; Penguin decision 8, the Wolf's Feral Strike).
11. Nightfall Swarm's road is 12.5 m (`clamp(10 + 2.5, 4, 18)`), not the no-target 18 m (tto Q2: the 10 m target rule).

## Passives, ranks, rolls
12. Auto Mass #431 on, 12 %, on the 11 cast3 members that roll it: `[0, "fx", "massCast", {"p": 0.12, "roll":
    "autoMass"}]`, though BB draws it only after a Mass Cast that session (skills_a Q5, skills_b Q9; Penguin decision 9).
13. Status tints and emoticons stay out: Mass Cast / Auto Mass purple, Charm purple, Mind Control / Mimic cyan,
    emo_heart / panic / blush (skills_a Q6, skills_b Q8, effect_only Q3; Penguin decision 10).
14. Drain Life holds `cAttack2*@6.2`: five ticks and Dream Burst 3's first burst at 6.0 s (attacks_emotes Q3: passives on).
15. The Homing Wand (`specialWand`, w_bat59) homes the Normal Attack bolts when worn, as the game (attacks_emotes Q4,
    parts Q2; Penguin decision 18): a `worn: [slot, item]` cue option, the ground hits marked `notWorn: ["R",
    "specialWand"]`. The bolt part and the hit cues use one contact rule, the 0.4 m sphere touching the 0.3 m body
    (parts calc.txt: 0.54 s after the spawn); the cue editor recomputes the variant's hit times from it
    (attacks_emotes' 0.56 / 0.58 s are centre-pass times).
16. Phantom Bane's damage-tick look (`phantomBane_hit`) at the mean phase: 1 s after the status, then every 2 s (skills_b
    Q4; as the Sheep's illuminate_hit).
17. Shadow Sacrifice's voice as the game: `shadowSacrifice2` at p 0.5, silent otherwise (effect_only Q2: TTO keeps the
    bug, so no TTO fix to take; Sheep decision 10 takes fixes only where TTO made them).
18. Confusion's voice is TTO's fix, `confuse1|confuse2` (BB asks for missing `confusion1/2`; Sheep decision 10).
19. Voice names keep the game's spelling (`guardianOfTheNight1|2`, `shadowIllusion1|shadowIllusion2`): the built file
    takes the cue's spelling, the rip lookup is case-blind (skills_a item 7, skills_b item 8).
20. Shadow Illusion at top rank: two clones.

## Summons and hero looks
21. Shadow Illusion's clones are built: a `"clone"` cue kind that copies the dressed hero (outfit, worn props, a skin
    cue's look), tinted (0.3, 0.2, 0.5), in the idle stance, at (-+1.5, 0, 2.6), `kill` 10, with `illusion_dust` at
    their end (10.4 s) (skills_b Q5, parts part 6: missing parts are always built).
22. Clones appear only in the Shadow Illusion tile; the combo, Drain Life, emotes and KO do not get live clones (parts Q6).
23. Mimic: voice and castEffect only, no transformation (skills_b Q2, parts Q5: there is no target model to copy).
24. Guardian of the Night's AI runs as the code: the first scan **4 s after the summon** (Bat.cs:30614 sets `Qypvswnda4 =
    Time.time + 4`, its predicate true; the planner re-read it: skills_a is right, parts.md's "first scan in the frame
    after the summon" is wrong), then every 2.5 s, each attack the five phases of parts part 4 (fade out, appear behind
    the target, two hits, back, fade in) on the 10 m target (parts Q1: the game's look). The state machine decides
    which scans land; an attack still running at the cut is aborted by the unsummon, as the game.
25. The guardian's end: the game's unsummon at 10 s after the summon (`ko` once, full alpha, gone 2 s later); cue
    `{"d": -4, "end": 10, "to": [0, 0, 10]}` with the entry's `"builds": ["guardian_blade", "guardian_hit"]` and the
    sound `guardian_nAttack`; `guardian_ring` `kill` 10 (skills_a Q3 with parts' option names).
26. The guardian's hits, blade trail and swing sound are spawned by its part (`api.spawn`, `api.Sound`), not cued: their
    times follow its state machine (parts Q3).

## Tiles and sequences
27. Normal Attack SEQ to the code's fixed starts: `nAttack1@0.6 nAttack2@0.6 nAttack3` (attacks_emotes item 1; Sheep
    decision 12's shape).
28. The first step keeps the page's 0.2 s fade (nAttack1, cAttack1 cut in the game) (attacks_emotes Q9; as the Sheep and
    the Penguin).
29. Guardian of the Night SEQ: `bigCast1@1 bigCast2*@0.1 bigCast3~` (skills_a Q1: bigCast2 starts at 1.0 s, 0.1 s is
    magAdjust's floor), with bigCast1's castRing `kill` 0.9 (skills_a verification correction 1).
30. cast3 is a pool of 19 members (one tile each, the Cast tile the hidden host); Nightmare and Mind Control are
    sequences of their own with `@Nightmare:*` / `@MindControl:*` cue keys (skills_b item 1).
31. Nightmare's channel `channel*~@8.9` (the 9 s status from 0.4 s); Mind Control gets its sequence `cast1 cast2*@0
    cast3~@0.5 channel*~@9.9` (12 s status cut at 10 s) (skills_b Q6, Q7).
32. SEQ_SKILL `bat:` holds both reports' keys in one object (Nightmare, Mind Control, Mass Cast, Shadow Gaze, Switch,
    Shadow Sacrifice), and `wardrobe_skill_icons.py` gets `OWN_TILE` bat {nightmare, mindControl} and `EFFECT_ONLY` bat
    {massCast, shadowGaze, switch, shadowSacrifice}, keeping the Penguin's `frostSpike` (skills_b verification 3,
    effect_only verification 1, 2).
33. The four skills with no body clip get effect-only tiles on the idle stance: `Mass Cast: root@1`, `Shadow Gaze:
    root@2`, `Switch: root@1`, `Shadow Sacrifice: root@2` (effect_only verification correction 3: each step = the
    effect's life + afterLife, at least its longest voice; the Penguin's rule).
34. Shadow Gaze's hit sound is a `"sound"` cue (`demonGaze_hit`): the hero's code plays it, the effect has no AudioSource
    (effect_only Q5).
35. The run's wing flap: `step_fly1` at 0.1 s of every run cycle, an `"everyCycle": true` entry flag re-arming the cues
    when the looping action's time wraps, and a build fallback that finds a `"sound"` outside the class's `sounds/`
    (attacks_emotes Q5 as its verification corrects it).
36. TTO-only emote clips (clap, wai, cooking, mining, planting, fishingBat, pose37) stay silent; chat voices stay BB's
    chat1-3 (attacks_emotes Q6; as the Wolf, Sheep, Penguin). A cross-class follow-up with TTO's voices is offered.
37. activateIcon1: no tile (Penguin decision 19).
38. The japanWagasa's open / close on the battle emote: no change in this job (a prop-clip feature, offered separately)
    (attacks_emotes Q8).
39. Nefarious Whip's ground hit at the target point, the hero's rotation (`{"d": 10}`), its sound shaped by AudioControl.

## Parts and looks
40. Built-in 205 is Particles/Multiply (`BUILTIN_BLEND[205] = "multiply"`), built before any Bat cue is checked: without
    it every Bat shadow effect glows instead of darkening (skills_a Q8, effect_only Q7).
41. The game's `Particles/MultiplyOffset`, `AlphaOffset` and `AdditiveOffset` shaders are built now, and their fix
    reaches the already-cued Wolf / Sheep / Penguin effects (Double Art, returnCast banners, bladeFang_hit, the status
    words ...); NOTES.md says their look changes (parts Q7: one builder, one rebuild).
42. Light is built (drainLife pink, mindControl_ring cyan, and the Wolf's crusader_hit / lawbringer_hit), through a pool
    of point lights kept in the scene from the start so nothing recompiles mid-skill (parts Q8; intensity checked by
    eye).
43. castRing's `root` clip plays looped 0.5 s after its spawn (an `fx:castRing` hook) (skills_a Q7: cheap, seen in the
    bigCast tiles).
44. Nightfall Swarm: the bats' mover holds the hero hide (each bat a heroHide key from its spawn to its landing)
    (tto Q3); worn weapon effects keep drawing while she is hidden, as HideBody leaves particles on (tto Q4); TTO 1102's
    code is accepted (tto Q5); the six Afflict statuses' looks on the foe stay out (tto Q6; Sheep decision 4).
45. Every report's corrected paste-ready block is the one to paste (verification sections), merged where two reports
    touch the same SEQ / SEQ_SKILL line.

## Offered to the user for the Bible (not written there)
Combo's fixed clip starts (0.6 / 1.2 s) and shot times; Drain Life's timeline and the own-client hit-flash bug; BB's
chat1-3 only; the run's wing-flap event; Guardian of the Night's first AI scan 4 s after the summon and its walk-in;
Auto Mass's flash only after a Mass Cast that session; Confusion silent in BB (TTO fixed it); Shadow Sacrifice's first
voice never heard (BB and TTO); Shadow Gaze rank 4's remote copy runs as rank 3; Mass Cast's purple tint; Phantom Bane's
tick and Chiroptophobia's timings.
