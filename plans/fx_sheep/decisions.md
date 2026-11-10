# Sheep effects: the user's decisions (2026-11-10)

From the chat, after the six research reports in this folder (attacks_emotes, own_skills, cast_a, cast_b, tto, parts)
and their verification sections. The user: "yeah let's go with your recc" (all 20 below), and earlier: "when you need
parts the page don't have yet, you have to make it work, we are top quality!" (every missing part gets built; nothing
is left out for a missing part). The Wolf's decisions (plans/fx_wolf/decisions.md) still hold where these don't speak.

## Who the effects land on
1. Ally-targeted skills show as self-casts on the Sheep (the game lets her target herself, GameGui.cs:37904-37921):
   Heal, Bless, Pacify, Clear, Cleanse, Revert, Illuminate, Feather, Repel, Reverse, World Encarta,
   Lucent Barrier. (Soul of Arms was listed here by mistake: its arms hit the target, Sheep.cs:34100-34118, so they go
   to the 10 m target point by decision 2; QA 2026-11-10.) Revive (a knocked-out ally) and effects on enemies follow the target-point rule below.
2. Divinity Sword / Spear / Axe (summoned at the enemy) show at the target point 10 m ahead, strikes and Spear's ring
   included.
3. The normal-attack ball (homingLight) and the charge ball end where they meet the ground at the 10 m target point
   (about 0.8 s), not their full 1.7 s / 5 s flight.
4. Gleaming Breath: a revived ally 10 m ahead (gleamingBreath_land at 1.22 s); its 15 s buff look does not float over
   the empty spot.
5. Grand Codex: its field 10 m ahead.

## Passives and ranks (passives on, max rank)
6. Return Cast's flash (returnCast) rolled at 24 % on every cast skill, Holy Light, Lullaby, Purifying Tear and the TTO
   skills (Gleaming Breath, Lucent Barrier), like the Wolf's Double Art; not on Grand Codex (TTO1102 never rolls it).
7. Homing Light #401: the normal attack shoots homingLight.
8. The charge ball at BB's max (Charge Attack 4, full charge: +1.6 m on the glow, Sheep_cAttack.Init).
9. Lucent Barrier lasts its tooltip's 3 s.

## Game bugs: TTO's fixes
10. Use TTO's fixed voices where BB asks for files that don't exist: All Cleanse = allClear1|allClear2, Seal of Defense
    = sealofDefend1|sealofDefend2, the charge release = cAttack1|cAttack2. (Offer each BB bug to the user for the Bible.)
11. The KO tile shows deadEffect at the hero on half the plays (RPC_dead spawns it, RPC_ko doesn't; both play the ko
    clip), for the Wolf too.

## Page and tiles
12. Normal Attack SEQ to the code's times: stage 2 at 0.7 s, stage 3 at 1.5 s ("nAttack1@0.7 nAttack2^@0.8 nAttack3").
13. A sequence can carry its own cues for a clip it shares (Holy Light and Lullaby both start with holyLight1).
14. Fix the Cast tile's pool: a new pick on every play of the tile, not only on the first.
15. Book Bash keeps its three tiles, each with its own cues.
16. Soul of Arms, Gleaming Breath and Lucent Barrier become sequences with the cast bar first (cast1 > cast2 held >
    the skill's clip), as the game plays them.
17. Seal and Eden Sanctuary get their own tiles without the cast bar (cast3 alone; Seal cuts in with no fade).
18. Seal of Attack and Seal of Defense are two separate skills.
19. Seal fields end at 10 s (cue kill; 60 s+ in the game); Eden Sanctuary keeps its 13 s.
20. Eden Sanctuary's field 1 m ahead, where the seal goes.
