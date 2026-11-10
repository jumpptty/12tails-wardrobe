# Penguin effects: the user's decisions (2026-11-10)

From the chat (home PC), after the six research reports in this folder (attacks_emotes, own_skills, cast_a, cast_b,
tto, parts) and their verification sections. The user: "go with your recc" (all 20 below). The Sheep's and the Wolf's
decisions (plans/fx_sheep/decisions.md, plans/fx_wolf/decisions.md) still hold by analogy where these don't speak, and
every missing part gets built (plans/fx_recipe.md).

## Where things land
1. Normal Attack: the ball ends on the ground at the 10 m target point (attacks_emotes' cues: pitched 4.514 deg, ends
   at 0.6807 s), as the Sheep's decision 3; not the game's no-target 5.57 m / 0.363 s landing.
2. The same holds for the Sheep (its Normal Attack stays as built).
3. Homing missiles (Mana Missile and any other projectile the game aims at `collider.bounds.center`) aim at the target
   0.6 m up (the CharacterController centre), so they reach the 10 m target, not the floor point (cast_a "Unresolved").
   Rule for every class from now on.
4. Effects the game draws with the target's rotation (snowMan_ring, snowBall_cast, snowMan, Mana Burn's manaSurge):
   the target faces the hero, `rot [0, 180, 0]` (cast_b's convention; cast_a's manaSurge changes to it). Rule for every
   class from now on.
5. Nova Flare: the blast at the Mana Vortex's spot 5 m ahead (Penguin.cs:27133); no vortex model.
6. Constellation: five stars, the target and 4 foes in a 3 m pentagon about 13 m ahead (tto.md option B).
7. Emperor's March: the 10 m target does not stop the ball: the full 22 m run, the Goal at 22.45 m, 1.636 s.
8. Frost Field's leap in place: the landing and the field at the hero (the Wolf's Feral Strike convention); no hero
   mover.

## Passives, rolls, statuses
9. Double Spell (12 %): the rerun's effects and voice play on the same roll, once (as TTO); the clip does not restart.
10. Double Spell's purple tint (multiCast, CharacterControl.cs:38470-38477) is left out.
11. Tornado and Typhoon are two members of the cast pool (as the Sheep's Seal of Attack / Defense).
12. Typhoon's first swerve: 0, 120 or 240 degrees at random on each play.
13. Ice Shield (30 s) and Mana Vortex (60 s) are cut at 10 s (cue `kill: 10`), as the Sheep's seal fields.
14. Emperor's March plays with 5 penguins (the tile alone, no Constellation within 8 s).
15. Focus Intellect's red Emperor's March (FocusRedden) is off.

## Hero looks
16. Cosmic Rift and Cosmic Friday get the hero-skin look: a `"skin"` cue kind and the FX/CosmicRift material part
    (cast_b "Hero-skin cues"). Only these two; the multiCast tint stays out (10).
17. Snow Man hides the hero for the snowman's time; she shows again at its end, or on the next pick (`dispose`).

## Weapons and tiles
18. The Staff of Time (`w_pgn59`, the wardrobe's `specialScepter`): when worn, the Normal Attack and Spread Shot balls
    move at 0.01 m/s and last 12 s, as the game (parts.md question 1; attacks_emotes question 3's "no" is overruled).
19. activateIcon1 (the mission "activate" clip on cAttack2): no tile.
20. Ice Shield, Mana Vortex and the rest keep the cue entries the reports give, corrected by their verification
    sections and by the rules above.
