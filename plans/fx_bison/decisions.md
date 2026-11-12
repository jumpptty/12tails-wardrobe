# Bison effects: decisions (2026-11-13), decided overnight, for the user's review

The user was asleep, so the planner decided every open question in the six reports in this folder (attacks_emotes,
skills_a, skills_b, effect_only, parts, tto), each read with its "## Verification" (the verification wins where the two
differ). Rules used, in this order: the standing rules (top rank, passives on; random picks as the game makes them;
enemy effects at the 10 m target point; homing aims 0.6 m up; target-rotation effects rot [0, 180, 0]; long buffs /
fields cut at 10 s; a tile per skill, effect-only tiles on the idle stance; missing parts always built; TTO cues only
for the released `magmaQuakeAxe`, `titanDrop`, `unchainedFury`), then the Wolf's, Sheep's, Penguin's and Bat's decisions
by analogy, then the reports' own recommendations. Every item is **decided overnight, for the user's review**: any of
them can be turned round in the morning.

What the Bat's build already gave the page (checked in the tree, 2026-11-13; nothing to rebuild for the Bison): the
`"sound"` cue's fallback to the rip's `Resources/sound/fx` (`hero_sound_wav`, wardrobe_fx.py), `"everyCycle"` entries,
`worn` with one item, `particles.js`' AdditiveOffset / MultiplyOffset, `audiocontrol.js` with the delay rule (a delayed
source starts only inside its fade-in), `mesh.js`' Opaque1 drawn with both passes, `api.spawn`, the light pool.

## Tiles and sequences
1. Normal Attack plays the game's roll for the third stage: `"Normal Attack: nAttack1@0.7 nAttack2@0.7
   nAttack4@1.3%56|nAttack3@0.8 nAttack5~0.3"` (56 % the spin, else stage 3, drawn when the sequence starts; Added Swing
   at 2.7 s after the spin or 2.2 s after stage 3, its 0.3 s crossfade). Reason: random picks as the game makes them
   (attacks_emotes Q2), not both clips one after the other as today.
2. The page builds the two SEQ forms that line needs: a step with alternatives `a|b`, each with its own fade and `@t`,
   `%p` = the first one's chance in percent (else even), drawn at step 0 and kept for the play; and a crossfade of any
   length `~0.3` (`~` alone stays 0.2). Reason: missing page parts are always built (attacks_emotes P1, P2).
3. Charge Attack with Hold Charge on: `"Charge Attack: cAttack1@0.8 cAttack2*~@7.2 root~@0.2 cAttack6*@1.816"`, the
   release's cues under `"@ChargeAttack:root"` (the stored charge's ring and glow), the stored spin with
   `holdCharge_fire`, and the voices `holdCharge1|holdCharge2`. Reason: passives on (attacks_emotes Q1 option A).
4. The first step keeps the page's 0.2 s fade (cAttack1 is a cut in the game). Reason: as the Sheep, Penguin and Bat
   (attacks_emotes Q6).
5. Trample's step is `trample2*@2.4`, not 2.6 (skills_b item 2, confirmed by its verification and effect_only's
   correction 1); the cut of trample2 / aspect_trample is 2.4 against trample2's own clock.
6. Berserker Rush and Fury Trance get effect-only tiles on the idle stance, `"Berserker Rush: root@6"`, `"Fury Trance:
   root@10"`, cue keys `@BerserkerRush:root` / `@FuryTrance:root`, SEQ_SKILL `bison: { "@BerserkerRush":
   "berserkerRush", "@FuryTrance": "furyTrance" }`, `EFFECT_ONLY["bison"] = ["berserkerRush", "furyTrance"]`. The proc
   plays on every play (no 16 % roll). Reason: one tile per skill, the Penguin's Frost Spike (effect_only Q1).
7. Fury Trance shows `furyTrance3` only (max rank; effect_only Q2); Berserker Rush lasts 6 s (Rage Control on;
   effect_only Q3); Fury Trance's 12 s is cut at 10 s.
8. Two pools, one tile per member, from the cue file (poolChains): `overPower` = Over Power, Titan Form; `warcry` =
   Warcry, Iron Shield, Diamond Shield, Onslaught. Their 0.2 s pool fade stays (the game cuts in). Reason: the Penguin's
   Blizzard note, 0.2 s not worth a page change (skills_b Q8).
9. volcanicRam (an animation no code in BB or TTO plays) is hidden: `NEVER_PLAYED.bison = ["volcanicRam"]`. Reason: the
   Wolf's cast1-3 precedent (the user 2026-11-09: "Remove the tile") (skills_b Q1); mentioned to the user in case he
   wants the animation kept as a plain tile.
10. The `cleave` tile is Power Cleave: `CLIP_SKILLS["bison"] = {"cleave": ["powerCleave"]}` in wardrobe_skill_icons.py
    (Power Hammer is a passive and gets no icon) (skills_a Q8, P5).
11. Over Swing keeps its looped 1.2 s tile (no SEQ line; the game stands at 1.0 s) and wears the Over Power horn and ring
    for the tile (kill 1.2): in the game Over Swing is never seen without them (skills_b Q3, Q4).
12. No Perfect Shield / Perfect Armor tile: it is two skills' combination, and no BB or TTO code ever adds the
    `perfectShield` / `perfectArmor` status (parts "Read this first" 2) (skills_b Q5, effect_only Q5).
13. TTO-only emote clips stay silent; chat voices stay BB's; the laugh is silent (the Bison has no laugh voice); no
    activateIcon1 tile (attacks_emotes Q5, Q8; Penguin decision 19, Bat decision 36).
14. The run's footsteps `step_heavy1` at 0.1 s and `step_heavy2` at 0.6 s of every cycle (`"everyCycle": true`, `"sound"`
    cues), as the Bat's wing flap (attacks_emotes Q7; already built).
15. The TTO tiles are single clips (no SEQ, no cast bar) (tto "Read this first" 10).

## Where things land
16. Melee hits draw nothing: no `nAttack_hit`, `axe_hit1` / `hammer_hit1`, Over Pride voice or gear procs, since the
    Bison's 5-8 m reach cannot meet the 10 m target point. Reason: the Wolf's attacks (attacks_emotes Q3, effect_only Q4).
17. The hero does not travel (Knock Down, Earth Smasher, Magma Clutter, Instant Rush, Trample): every effect relative to
    the standing hero (afterShock 2 m ahead), no Trample sparks at 10 m. Reason: the Wolf's Feral Assault, the Penguin's
    decision 8 (skills_a Q6, skills_b Q6).
18. Mass Stun's blast at the 10 m target point, with the hero's facing (no rot [0, 180, 0]: LookRotation(the hero's
    forward), skills_a verification); Far Stun's ring at the hero (skills_a Q7).
19. Calamity Hammer's strikes at the 10 m target point, cut at 10 s: six strikes, 2.4 ... 9.9 s (skills_a Q3; the
    standing 10 s rule, the Penguin's Ice Shield).
20. KO: `deadEffect` 1 m behind the Bison (`d: -1`), as the game's RPC_dead (attacks_emotes Q4).
21. Earth Rupture's three waves fly 12 m/s for 2 s (24 m) through the 10 m target, no floor or target stop (parts part 3).
22. Titan Drop in place with its height (tto Q1 option C): the Bison is lifted along TitanDropPath's height curve from
    0.4 to 1.5 s (3 m at 1.2 s), never moved forward; the takeoff at the hero, the mark and the three slam rings at
    0.26 m right, 3.9 m ahead (the axe head's strike relative to the landed body, as Frost Field's burst), the dive at the
    lifted hero with rot [47.5, -2.4, 0], riding him down. Reason: the leap is the skill's whole look, and decision 8's
    "no travel" keeps the slam where the clip's axe strikes; moving the slam to 10 m (the verification's open point) would
    detach it from the swing 6 m away.
23. Magma Quake's tick looks at the game's own spots for a Bison at the origin (seed 0: 144 axe / 120 hammer, fixed), all
    of them kept, the 91 % beyond 10 m included (tto Q3, Q4: the skill's reach; its cost flagged for QA).

## Passives, ranks, weapons
24. Enrage 4 + Rage Control #402 on (sLv 5), Berserker Rush 4 + Rage Control (level 5, 6 s), Iron / Diamond Shield with
    Steel / Mythril Skin (8 s), Titan Form 2, Over Power 2, Knock Down with Aftershock, Far Stun with Mass Stun, Power
    Cleave with Power Reel, Slam / Trample with Aspect of the Horde (parts Q2; skills_b verification: 8 s, not parts'
    6 s).
25. One weapon set `bisonHammer` for both weapon-picked skills (Power Cleave's hammer set, Magma Quake's hammer branch):
    BB's 22 `isHammer` codes plus TTO's `timeHammer` (w_bsn69), i.e. the 20 props stoneClub, toyHammer, bdWeapon,
    defenderHammer, defenderHammerR, barbell, warlordHammer, warlordHammerR, hallowLance, havocHammer, havocHammerR,
    havocHammerV, superStarBass, mummyMace, goldenHammer, royalHammer, royalHammerR, specialHammer, legendHammer,
    timeHammer, plus legendHammerR (w_bsn62; no prop today, harmless). Reason: TTO's fix taken (Sheep decision 10,
    skills_a Q2), and TTO's own 24-code list for its Magma Quake (tto Q2) is the same set.
26. `worn` / `notWorn` take `[slot, item]`, `[slot, [items]]` or `[slot, "<set>"]` (a name in the page's `ITEM_SETS`);
    the cues write `["R", "bisonHammer"]` (skills_a's inline lists in `cleave` become the set name). One tile per skill,
    its look following the worn weapon, as the Penguin's Staff of Time (decision 18).
27. Over Pride's voice, Berserker Rush's roll on Unchained Fury's HP payment, and Blood Carnage (the shared support skill:
    a cross-class job, as the Penguin's report) are left out (effect_only Q4; tto Q5; parts Q5).
28. Pride Crusher and Onslaught stay silent: their voice files exist in neither BB nor TTO, so there is no TTO fix to
    take (skills_b Q2; Bat decision 17).
29. Magma Clutter's start sound follows TTO's fix: `[0, "sound", "magmaClutter1|magmaClutter2"]` (BB asks for missing
    voices) (skills_a Q4; Sheep decision 10).
30. Hold Charge: its stored glow `holdCharge` lasts until the spin's press (kill 0.2 in the release step), the ring and
    the fire as attacks_emotes gives them.

## Hero looks
31. Enrage's and Titan Form's body looks are built as `"skin"` cues (the kind the skill reports wrote; the check already
    knows it): HERO_SKINS `enrage` (the hero x 1.25, every hero material's colour x (1.05, 0.55, 0.55) / 0.86 =
    (1.22, 0.64, 0.64)) and `titanForm` (x 1.8, colour x (0.6, 0.7, 1) / 0.86 = (0.70, 0.81, 1.16)), as gamma values like
    the Bat's clone tint, from the status time (Enrage 0.5 s, Titan Form 0.3 s), cut at 10 s or ended by the next pick,
    restored on dispose. Reason: the growth is the skill's whole look (skills_a Q1, skills_b Q7, parts Q1); parts'
    `"look"` kind is the same thing under the existing name. The 1.8x Bison is checked against the camera framing by
    screenshot.
32. Effects the game parents to a grown hero take the growth in that tile only (`titanForm` cue `scale: 1.8`), not a
    general follow-the-hero's-scale rule (parts Q7).
33. Over Power's horn rides the `Head` bone with localRotation Euler(-90, 0, 0): a cue with both `bone` and `rot` keeps
    `rot` as the localRotation under the bone (parts part 6, Interfaces 1).
34. Status tints from passives stay out as before (Penguin decision 10); Enrage / Titan Form are skills' own looks, not
    side tints.
35. The camera's motion blurs, shakes and zooms stay out (skills_b Q9; the Penguin's Dispell).

## Parts and looks
36. UVScroll (aspect_slam, aspect_trample; also Cat / Whale later) is built, scrolled by the page's absolute clock so the
    two Trample hordes move in step, as the game's Time.time (parts Q4, part 1).
37. AlphaTimer drives Transparent/Opaque1 and Opaque2 (alpha = `_Color.a`, both passes), so earthSmasher's and
    massStun's rock fade out as in the game (parts part 2).
38. One per-renderer material copy is shared by the parts on a node (AlphaTimer, UVScroll): the first part clones the
    first material with its other passes and flags it (`mesh.userData.fxOwn`), the next uses it (parts Interfaces 3).
39. `Bison_earthRupture` is a mover in `fxparts/bison.js`; `Bison_overLord` draws nothing and is never cued (made at
    Start): only its empty LAYOUTS entry and a place in BUILT (parts parts 3, 4).
40. magmaClutter_ring2's Shuriken puffs: BB's effect (it keeps the `cleave` swing TTO's copy loses) with TTO's decoded
    ParticleSystem grafted in at build time, as a child node at the TrailEmitter node's own transform with BB's `Bomb2`
    material (the same Multiply (Double) shader, built-in 206, already built for calamityHammer), so no TTO texture and
    no shuriken.js change; the cue names the plain `magmaClutter_ring2`, not `tto/magmaClutter_ring2`. Reason: parts Q3
    and its "Read this first" 5 (TTO's copy has no swing) win over skills_a Q5; the effect stays BB content.
41. TTO's parts are built: Bison_c6Arc (with `repeat` and the ground drape) + the EnergyArc shader, Bison_row6Fx (with
    `bob`), the MoltenCrust shader, GroundConformParticles registered as a no-op on the flat floor (tto B1-B6, parts parts
    8-10 as their verification corrects them: 12 prefabs with arcs, `tto/unchained` included).
42. `SKILL_FX["bison"]` takes the verification's corrected list (with the status look `unchained`).
43. The four BB prefabs TTO's skills reuse (berserkerRush, berserkerRush_ring, calamityHammer_ring, earthSmasher_ring)
    are BB's rip copies (tto Q6).
44. AudioControl needs no change: `audiocontrol.js` already starts a delayed source only inside its fade-in, so
    titanDrop_takeoff's `overSwing` and titanDrop_slam2's `earthSmasher_ring` stay silent, as the game (parts correction
    4, tto correction 1).
45. Velvet (perfectArmor's shader) is not built: no game code ever shows that effect; the inventory says "unreachable"
    (parts Q6).
46. The inventory gains `holdCharge`, `holdCharge_ring` and the other CharacterControl status looks as a note, and BUILT
    += UVScroll, Bison_earthRupture, Bison_overLord, Bison_c6Arc, Bison_row6Fx, GroundConformParticles; magmaClutter_ring2
    noted as grafted (parts "Rank by value").
47. Unchained Fury: `tto/unchained` for its 3 s status, the Berserker Rush look from 0.62 s cut at 10 s (12 s x CHA in the
    game), the plant 2.45 m right, 2.6 m ahead (tto block as written).
48. Every report's corrected paste-ready block is the one to paste (verification sections: skills_a's re-indented block
    and TTO lines, effect_only's corrected SEQ, parts' SKILL_FX), merged where two reports touch the same SEQ / SEQ_SKILL
    line, with decision 26's set name in place of inline item lists.

## Offered to the user for the Bible (not written there)
Combo's fixed clip starts (0.7 / 1.4 s) and Added Swing's 2.2 s after stage 3 but 2.7 s after the spin; the stage voice
and hit times; the charge's timeline and Hold Charge's voice swap, cAttack0 release and holdCharge_fire; deadEffect 1 m
behind; no laugh voice; Power Hammer's 22 BB hammers (+2 in TTO); Power Cleave's timing with Power Reel; Magma Clutter's
missing voices and hit effect (TTO's fix); Enrage's tint; Calamity Hammer's strikes at 2.4 + 1.5 k s; Over Swing's hits at
0.7 / 0.9 s; Slam's sLv + 2 rounds; Trample's phase times; Pride Crusher's and Onslaught's missing voices; Fury Trance's
removal at 60 % HP and its 3 s lockout (bison-skill-reference.md:292); Unchained Fury's `unchained` look and timeline;
Titan Drop's effect times and path; Magma Quake's tick pattern, weapon-butt spot and the axe's impact sound.
