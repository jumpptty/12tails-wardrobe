# Monkey effects: decisions (13/11/2026), decided overnight, for the user's review

The user was away, so the planner decided every open question in the six reports in this folder (attacks_emotes,
skills_a, skills_b, effect_only, parts, tto), each read with its "## Verification" (the verification wins where the two
differ). Rules used, in this order: the standing rules (top rank, passives on; random picks as the game makes them;
enemy effects at the 10 m target point, the target body of Bat decision 4: centre (0, 0.6, 10), r 0.3, h 1; homing
aims 0.6 m up; long buffs / fields / summons cut at 10 s; a tile per skill with its Bible icon, pool members one each,
effect-only tiles on the idle stance; missing parts always built; TTO cues only for the released `buitenBastion`,
`golemCall`, `jaAscension`, `solarCall`, `clap`, `wai`), the page's SEQ rule (a charge = full charge, a channel = its
duration, three ticks / at least 3 s for a hold the player ends; high INT, the cast bar at magAdjust's 0.1 s floor),
then the Wolf's, Sheep's, Penguin's, Bat's, Bison's, Cat's, Chameleon's and Mole's decisions by analogy, then the
reports' own recommendations. Every item is **decided overnight, for the user's review**: any of them can be turned
round.

Already in the tree (reused, not rebuilt): `hideProp` with slot `"hero"` and option `all`; the parts' `end` option
(bat.js: the guardian's unsummon N s after the spawn); `single`; `anims` (cat.js, `[[age, clip]]`: widened here, not
renamed); `api.spawn` + an entry's `"builds"` with `followNode` / `local`; `api.propModel(slot, true)` with
`PROP_STARTER`; `api.pointLight`; `fxAnim.play(name, fade, wrap)`; robots.js's `run(node, [[t, fn]])` clip timeline;
`fxparts/rotationcontrol.js` (rotationControl, the Mole's); `wardrobe_fx.py`'s `FIELD_PREFABS`, `SOUND_REFS` (sound names
`<script, first letter lower>_<AudioClip name>`), the `"s"` string type, `EXTRA_FOLDERS`, `ALIASES`, `SOUND_ALIASES`,
`SHURIKEN_FROM_TTO` by-material grafts, `clip_dict`; `wardrobe_fx_tto.py`'s `animation()` (TTO legacy clips: tto.md
P4 and parts.md T1's clip item are **done**, parts verification 1, tto verification 5); `CODE_MOVERS`; tto_penguin.js's
cel shader, tto_sheep.js's `Particles/Standard Unlit`, light.js, uvscroll.js's own-material pattern, alphatimer.js's
per-renderer material copies; cat.js's `lookEuler`. `fxparts/mole.js` exports only `mortarVector` (a gravity arc): the
Monkey's straight shots get their own mover (parts verification 9).

## Tiles and sequences
1. Normal Attack: `"Normal Attack: nAttack1@0.5 nAttack2~"`. Reason: stage 2's clip comes at stage 1 + 0.5 s with a 0.2 s
   crossfade (attacks_emotes Read this first 1, verified).
2. Mike Blink #401 gets its own tile `"Mike Blink: nAttack1@0.5 nAttack2~"` (keys `@MikeBlink:nAttack1` /
   `@MikeBlink:nAttack2`, attacks_emotes verification 1's corrected blocks: strike 1 cued at stage 2's 0, not at 0.5 of
   a 0.5 s step), at the 10 m target (not past the game's 12 m gate). Reason: one tile per skill (Chameleon decisions
   12-13); a cue at a step's very end never fires (index.html seqTick / fxDue); the standing target (attacks_emotes Q1).
3. With nothing worn in R the blink carries the starter `noviceMike` (`PROP_STARTER.monkey = { R: "noviceMike" }`);
   one `fx:mikeBlink` part, parts.md part 6's. Reason: Chameleon decision 50 (attacks_emotes verification 2).
4. The Charge Attack tile is renamed **"HP Transfer"**: `"HP Transfer: cAttack1 cAttack2*@3.2"` (three 1 s ticks), and
   Mike Circle #411 gets `"Mike Circle: cAttack1 cAttack2*@3.2"` (no own key: the plain `cAttack2` entry). Reason: the
   Bible's name (as the Bat's Drain Life); the SEQ rule's three ticks; one tile per skill (attacks_emotes Q2, Q4, Q5).
5. **The Monkey's cast bar is 0.1 s, not 0**: every channel step is `damageCast2*~@0.1` (Cast, Lavu, Volcanic
   Eruption, Fire Keep and the four TTO tiles); the `castRing` cue's `cut` becomes **0.1** (the step's end: fxStart cuts
   it at the step change, the game's release). Summon Gaos keeps its 8 s bar. Reason: magAdjust's floor, Mole decision 6
   and tto Q5 (overrules skills_a's `@0` / `cut 0.05`, whose own verification 6 already flagged the reasoning).
6. One Cast host `"Cast: damageCast1 damageCast2*~@0.1 cast3~"`; the `"Cast: cast1 ..."` and `"Damage Cast: ..."` lines
   go; `LOWER_RANK.monkey = ["cast1", "cast2"]`, `NEVER_PLAYED.monkey = ["damageCast3"]`. Damage Cast #102/#103 gets no
   tile of its own (its look, the clip swap, is on every cast tile; its hits need a foe within 2 m). Reason: passives on
   (skills_a Q1; the Bison's Power Hammer, decision 10).
7. The **TTO channels are damageCast too**: tto.md's `cast1 cast2*~@0.1` become `damageCast1 damageCast2*~@0.1`, and the
   Sun Avatar key `@JaAscension:cast1` becomes **`@JaAscension:damageCast1`**, carrying the plain `damageCast1` cues (the
   `cast` voice) as well as the standing Ja. Reason: TTO's RPC_cast picks damageCast the same way (skills_a Read this
   first 1); passives on.
8. The cast3 pool `skills` has ten members, one tile each: fireBall, phoenix, ja, worldIgnition, groundLock, gadina,
   stoneHammer, **buitenHouHou** (the card's name and icon), fireAvatar, earthForm (skills_a verification 8's block).
   The summons of phoenix / ja / gadina / buitenHouHou are drawn **in the idle tail** after cast3 (no own sequences:
   parts verification 12's "Summon Phoenix" sequence is overruled). Reason: the Mole's Assemble pool with its summons
   (Mole decisions 6, 21: the loop toggle cuts nothing part-made); the tile plays once by default (skills_b Q6).
9. Own sequences (kept out of `cast3.skills`): `"Lavu: damageCast1 damageCast2*~@0.1 cast3~@2.4"`, `"Volcanic Eruption:
   damageCast1 damageCast2*~@0.1 cast3~@10.3"`, `"Summon Gaos: damageCast1 damageCast2*~@8%88|damageCast2*~@0 cast3~"`
   (Auto Instant's 12 % instant bar as the `|` alternative, cues filtered by the new option `alt`), `"Fire Keep:
   damageCast1 damageCast2*~@0.1 root~@1 cast3"` (the store, key `@FireKeep:root`, then the release). Reason: their
   holds / bars (skills_a Q5, Q6; War Capital's 8 s, Mole decision 7); Fire Keep's whole look is store + release
   (skills_a verification 7, the Cat's Nine Lives).
10. Plain clip tiles: Blazing Arrow (`blazingArrow`), Flash Fire (`flashFire`), Titanic Earth Pulse (`earthPulse`, icon
    through CLIP_SKILLS). Reason: one coroutine each (skills_a).
11. Pools, one tile per member, keys = the Bible ids: `runicCast` (runicFlame, runicSand), `summonAttack` (summonAttack,
    skyCrimson, planetBreaker, instantBlaze, earthGuard), `summonRelease` (unsummon, summonRelease, summonSoul);
    `summonDefense` a single. Reason: the standing rule (skills_b Read this first 1).
12. **Earth Form Attack**: `"Earth Form Attack: summonAttack@0.9 summonAttack~@0.8 summonAttack~"`, stage 1 under the plain
    key `@EarthFormAttack:summonAttack`, stages 2 / 3 under **`@EarthFormAttack:summonAttack#1` / `#2`** (fxStart tries the
    step's `#<step>` key first). Reason: all three stages play one clip with different voices and rings; stage 1 keeps
    the plain key so poolChains does not take the tile as the summonAttack pool's host (skills_b verification 1).
13. `"Sentinel Guard: sentinalGuard1@0.5 sentinalGuard2*@6.1 sentinalGuard0"` (three heals, released at 6.6 s) and
    `"Upheaval: upheaval*@3.1 root~0.35@0.35"` (three waves, released at 3.1 s). Reason: the SEQ rule's three ticks for a
    hold the player ends (skills_b Q3); 10 s would only lengthen nothing-drawn ticks.
14. Effect-only tiles on the idle stance, effect_only verification 4's block: `"Instant Cast: root*@1"`, `"Fire Rune:
    root*@1"`, `"Earth Rune: root*@1"`, `"Fire Avatar - Fireball: root*@1.8"`, `"Blazing Fire: root*@3.5"`. Reason: no
    body clip (Instant Cast; the runes are passive procs; the form's moves play on the armour, the hero hidden).
15. **Phoenix - Fireball** (Bible card `monkey_phoenix_fireBall`) gets an effect-only tile `"Phoenix - Fireball:
    root*@<hold>"`: the Phoenix4 standing 2 m ahead plays `nAttack` (0.3 s fade) with its cry at 0, the shot from
    (0, 2.4, 3) at rot [14.42, 0, 0] to (0, 0.6, 10) at 0.5 s (part-spawned `phoenix_fireBall_hit`), root at 0.8; the
    hold = the hit's end (the editor reads its life from the built data). Reason: one tile per Bible card; the move is
    traced (skills_b's Summon Attack shot, skills_a verification 9).
16. The four TTO tiles (tto verification's corrected S1 with decision 7): `"Ascended Ja: damageCast1 damageCast2*~@0.1
    jaAscension~0.15 root*~@10.4"`, `"Ja Ascension: damageCast1 damageCast2*~@0.1 solarCall~0.15 root*~@12.9"`,
    `"Bastion Buiten: damageCast1 damageCast2*~@0.1 buitenBastion~0.15 root*~@10.3"`, `"Rune Golem: damageCast1
    damageCast2*~@0.1 golemCall~0.15 root*~@11.9"`. `sanctumRaise` (not released): no cue, no sequence, no part.
    Reason: tto Read this first 1, verification 1-2 (the tile name is on screen: the skill's name), Mole decision 15.
17. SEQ_SKILL `monkey: { "@MikeBlink": "mikeBlink", "@MikeCircle": "mikeCircle", "@Lavu": "lavu", "@VolcanicEruption":
    "volcanicEruption", "@SummonGaos": "summonGaos", "@FireKeep": "fireKeep", "@EarthFormAttack": "earthForm",
    "@SentinelGuard": "stoneSentinel", "@Upheaval": "lavu", "@InstantCast": "instantCast", "@FireRune": "fireRune",
    "@EarthRune": "earthRune", "@FireAvatar-Fireball": "fireBall", "@BlazingFire": "blazingFire", "@Phoenix-Fireball":
    "phoenix" }`; **no** `@JaAscension` / `@RuneGolem` entry. Reason: the reports' merged lines (attacks_emotes,
    skills_a, skills_b, effect_only verification 3-4); a SEQ_SKILL value is dropped from every other tile's icons, so
    the TTO tiles take theirs from CLIP_SKILLS (tto verification 3).
18. `wardrobe_skill_icons.py` (the editor's): `CLIP_SKILLS["monkey"] = {"earthPulse": ["titanicEarthPulse"],
    "jaAscension": ["ja", "jaAscension"], "buitenBastion": ["buiten", "buitenBastion"], "solarCall": ["jaAscension"],
    "golemCall": ["runeGolem"], "sanctumRaise": ["buitenBastion"]}`; `OWN_TILE["monkey"] = {"mikeBlink": ["nAttack1",
    "nAttack2"], "mikeCircle": ["cAttack1", "cAttack2"], "lavu": ["cast3"], "volcanicEruption": ["cast3"], "summonGaos":
    ["damageCast2", "cast3"], "fireKeep": ["damageCast2", "root", "cast3"], "stoneSentinel": ["sentinalGuard1",
    "sentinalGuard2", "sentinalGuard0"]}`; `EFFECT_ONLY["monkey"] = ["instantCast", "fireRune", "earthRune",
    "blazingFire"]`; no `ICON_ALIAS` (Fire Avatar - Fireball takes the Fireball's icon through SEQ_SKILL). If the pooled
    filter then drops the Ja / Buiten icon from the two boosted tiles (tto verification 3's risk), they show the TTO
    skill's icon alone: accepted. Reason: attacks_emotes verification 3, skills_a, skills_b verification 3, effect_only
    verification 3, tto S2.
19. KO, emotes, run as attacks_emotes' block: `ko` / `dead` voices with `deadEffect` on half the plays (roll `dead`),
    getUp silent; `wave` takes the `hi` voice (emo_hi / emo_wave), every other emote silent; the run's `step_normal1` on
    both feet every cycle; clap, wai and the other TTO-only emote clips silent. Reason: the code (Sheep decision 11, Bat
    decision 36; attacks_emotes Q9).

## Where things land
20. One target: the 10 m point (feet (0, 0, 10), body as Bat decision 4) for every enemy effect and for the ally skills
    that refuse a self-target: HP Transfer's beam to (0, 0.6, 9.4), Mike Circle at d 10 y 0.45 rot [270, 90, 0], Mike
    Blink's `mikeBlink` at d 10 rot [270, 90, 0], its strikes at d 9.7 / 10.3 y 0.9. Reason: attacks_emotes Q1, Q3 (Sheep
    decision 4's ally analogue); parts Q4, Q5.
21. **Projectile hits are part-spawned on contact** (no hit cue): `fireBall_hit` with the hero's rotation; `earthPulse_hit`
    with the world Euler(270, 90, 0) (not lookEuler(vel)); `phoenix_fireBall_hit`; `phoenix_skyCrimson_hit` (identity,
    floor only: the ball passes the target). The entries list them in `builds`. Reason: one owner per hit (skills_a
    verification 4); Mole decision 18's rule.
22. Fireball (and Fire Keep's release) fires from (0, 1, 1) at rot [2.54, 0, 0] to the body centre (0, 0.6, 10); Titanic
    Earth Pulse from (0, 1, 5) flat to (0, 1, 9.7); Fire Avatar - Fireball from x 0.2 y 1.5 d 1.5 at rot [10.0, -1.35, 0]
    toward the **ground** point (BB aims at the target's position, not its bounds). Reason: the code (skills_a
    verification 8; effect_only Q5).
23. Summons stand where the game puts them, facing forward: Phoenix4 / Ja4 / Gadina4 / Buiten4 2 m ahead, Gaos 9 m,
    Blazing Arrow's Phoenix 2 m **behind** (`d -2`), the Rune Golem 4.5 m; the stand-in summons of the command tiles 2 m
    ahead. Reason: getSpawnPos(hero + n forward) (skills_a verification, skills_b Read this first 2, tto 2.5).
24. Lavu keeps the game's flight: up out of the ground 3 m ahead (y -2, rot [-90, 0, 0]), 10 m/s up for 2 s, then
    circling the Monkey's head + 4 m at 8 m/s; the camera fit is the editor's check. Upheaval's tile spawns Lavu already
    summoned in the upheaval state (`"lavu": "upheaval"`, the 3 s slerp onto the 6 m ring as the code), released at 3.1 s
    (`release`). Reason: parts Q2, Q3 (the precondition shown, Mole decision 27).
25. Instant Blaze's Phoenix dashes through the target to 12.8 m ahead (`moves`); the hero never travels (Blazing Form's
    3 m/s rush shown in place). Reason: Chameleon decision 30, Penguin decision 8 (skills_b; effect_only choice 6).
26. Nothing is drawn where the reach misses the 10 m body: the Combo's 0-7 m / 3.5-7.5 m boxes, the Earth Form punches,
    Damage Cast's 2 m ticks, Planet Breaker's 5 m inner ring. Reason: Bison decision 16 (attacks_emotes, skills_b).
27. Ground Lock's `groundLock_hit` and Second Stone (3.4 s, the idle tail) and Stone Hammer at the target's feet,
    identity. Reason: the code (skills_a).
28. Runic Flame / Sand draw no trail: the game drops a segment only after 1.58 m of travel and the hero stands; each tile
    shows the status ring on the Monkey from 0.3 s, `kill` 10. Reason: Bison decision 17 (skills_b Q4).
29. **Ja Ascension's Solar Collapse falls on the Monkey** (TTO1102: dive 0.3 s, the supernova at the Monkey at root
    10.4, hold 12.9); TTO1106+'s aimed recast onto the 10 m target is offered to the user. Reason: TTO1102's code for
    every class (Bat decision 44, Cat 42, Chameleon 44, Mole 57; tto verification 1).

## Summons, armours and forms
30. **The summons are built and shown**: Phoenix4, Ja4, Gadina4, Buiten4, Gaos (top ranks) play their summon clip
    (Buiten: `create`) with their summon ring / effect at their feet, then `root`; **no AI**; their skill's own summon
    ends with **`end: 10`** (seconds after the spawn) = the game's unsummon coroutine (Phoenix / Ja `ko`, gone 1 s later;
    Gadina `unSummon` + `summonEffect` and its waits; Buiten `unSummon` + `summonEffect`, 1 s; Gaos `unsummon` +
    `unsummon_ring`, 1.5 s), not a `kill`. Reason: Mole decision 32, Penguin's Mana Vortex; Bat decision 25 (parts Q1,
    verification 6; skills_a Q4).
31. One option name per meaning: the armours' and summons' clip timeline is **`anims`** `[[age, clip, fade?, wrap?]]`
    (cat.js's option widened; the reports' `clips` dropped); a summon already out is **`standing: true`** (no summon
    clip, no ring, starts in `root`; skills_b's `ring: false` dropped); plus `hide` [from, to], `moves` [[age, m/s]],
    `turn` (age: face the hero, yaw 180, and cry), `attach` [[effect, bone]], `boost` (TTO), `end`. The editor renames
    `clips` -> `anims` and `"ring": false` -> `"standing": true` in the pasted blocks. Reason: parts verification 7,
    effect_only verification 1 (no second name for the same thing).
32. Gadina4 carries `gadina_sword4` on `mount_Hand_R` and `gadina_shield4` on `mount_Hand_L` (`attach`, in `builds`).
    Reason: Titan Sword 3 / Aegis of Earth 3 at max rank pick them (parts Read this first 6; skills_a verification 2).
33. The command tiles show the summon already standing 2 m ahead (`standing`, `single`, `kill` 10: not their skill's
    summon, so no unsummon look), **Phoenix4** on the generic commands (Summon Attack, Defense, Unsummon, Release, Soul:
    Summon Soul shows `phoenixSoul` at y 1.35), Gadina4 on Planet Breaker / Earth Guard; Unsummon ends its Phoenix with
    `end: 0.3`. Each plays only what the command itself makes happen (Summon Attack's first shot, Sky Crimson, Instant
    Blaze, Planet Breaker, Earth Guard, Defense's turn and cry, Unsummon's ko). Reason: Mole decision 37 (the
    precondition shown), skills_b Q1, Q2.
34. **Titanic Earth Pulse shows its Gadina4** standing 2 m ahead from the tile's start, unsummoned at 0 (`standing`,
    `end: 0`: the code SendMessages "unsummon" to it, Monkey.cs:32489, checked here). Reason: the precondition shown
    (Mole decision 27; overrules skills_a Q7: the unsummon look is the Gadina's own part, already built for decision 30).
35. Blazing Arrow's Phoenix (24 %, roll `blazingPhoenix`, with its Fire Soul ring) at 4.8 s in the idle tail, `end: 10`.
    Reason: random picks as the game makes them (skills_a).
36. Fire Avatar: the whole hero hidden for the 10 s form (`hideProp hero`, kill 10), `phoenixArmor` with the cue's
    `anims` [[0, summon, 0, 1], [0.8, root, 0.2, 2]] (the hero's standby at 1.5 s), `phoenixArmor_create` twice as the
    code. Earth Form: the hero stays visible, `gadinaArmor` [[0, summon, 0, 1], [0.5, root, 0.2, 2]]. Each part's
    default timeline (summon, then root after its length) applies only when a cue gives no `anims`. Reason: skills_a Q8,
    verification 5.
37. The form's own tiles (Fire Avatar - Fireball, Blazing Fire, Earth Form Attack, Sentinel Guard) show the armour already
    worn (`anims` starting at the move's clip, `single`, kill 10) and, for the Fire Avatar ones, the hero hidden with no
    kill (until the next pick). Blazing Fire fades the armour by the new option `alpha` [[age, a]] on its own material
    copies. Reason: Mole decision 37 (the form already on), Chameleon decisions 48-49 (effect_only Q7, verification 2).
38. Lavu: `lavu` at 0.4 with `unsummon: 10` (the 1 s fade) and `kill: 11` (parts verification's corrected `@Lavu:cast3`).
    Reason: the 10 s rule with the game's own end (Bat decision 25).
39. TTO's boosted summons: `boost: 2` = the Ja at level 6 with `tto/jaAscension_aura` parented at its root, the Buiten
    x 1.2 with `tto/buitenBastion_aura` parented unscaled, each with BB's summon ring in `builds` (`ja_summon_ring`,
    `buiten_summonEffect`), `end: 10`; Ja Ascension's Ja standing from the tile's start (`standing`, `boost` 2, kill 0.8:
    hidden and spent at the bar's end). Reason: tto P8, Q2-Q4, verification 8.
40. **The Rune Golem is built with its AI** as the code on the 10 m target: rise (0.7 s), roar (2.05 s), walk 4 m/s with
    footfalls, fist / quake / pound, the aura pulse every 1.5 s from 0.7 with `tto/stoneAegis` on the hero, its glow,
    `MonkeyRow6Rise`'s quake spikes, and at `end: 10` its CrumbleAway (gone 2.4 s later). Reason: tto Q7, Q8, verification
    6; parts verification 5 (Bat decision 24, Mole decision 32's Auto Gyro Gun: a traced AI is built).
41. The BB elementals' own AIs (Phoenix_AI, Ja_AI, Gadina_AI, Gaos_AI) are not run: untraced, and the Phoenix's is the
    only one a report read. Reason: Mole decision 32's Barrel Bot split (skills_a Q4, skills_b Q2); offered (decision 57).

## Passives, ranks, rolls, voices, sounds
42. Passives on, max rank: Combo with #101, Mike Blink #401, Mike Circle #411, HP Transfer at charge level 5, Damage Cast
    #102/#103, Fireball 4, Phoenix 4, Ja 4, World Ignition 2, Ground Lock 4 + Second Stone #403, Gadina 4 (Titan Sword 3,
    Aegis of Earth 3), Stone Hammer 4 + Stone Sentinel #443, Buiten Hou Hou 4, Lavu 2, Flash Fire 4, Fire Soul #422, Earth
    Soul #423, Auto Instant #431, Fire Keep #402 (level 4), Fire Rune 3, Earth Rune 3, Instant Cast 2, Fire Avatar -
    Fireball level 4 (`fireBall4`, voice `sAttack3`), Blazing Fire #442, Revised Skill #404 / Magic #414, Instant Blaze
    #412, Earth Guard #413; TTO Ja Ascension #452, Buiten Bastion #453, Rune Golem #454. Reason: the standing rule.
43. Auto Instant's 12 % `instantCast` (`p` 0.12, lckAdjust(12) at LCK 1) on the plain `damageCast2` entry, so on every
    channel tile; on Summon Gaos it also picks the 0 s bar (`alt`). Reason: random picks as the game makes them (skills_a
    Q3, Q6).
44. Fire Rune: its own tile procs every play; elsewhere 12 % (`p` 0.12) at each roll's game time: Mike Blink's two
    strikes (independent, 1.4 % both: the 1 s lockout not modelled), Fire Avatar - Fireball (0.8 s), the Fireball cast
    (0.8 s of cast3), Fire Keep's release (0.8 s), Fire Avatar's cast (1.5 s), Earth Form's cast (1.2 s), and Earth Form
    Attack's **stage 3 only** (stages 1-2 never reach the standby block that calls it, skills_b verification). A roll at
    or past a non-last step's end moves to the next step's 0; past the last step's end it runs in the idle tail. Reason:
    effect_only Q6 and verification 5; attacks_emotes Q6 and verification 1.
45. Earth Rune: its own tile only (it needs a hit taken). Reason: the Bison's Berserker Rush (effect_only).
46. Every look and voice the game gates on missions / own team (`mGameType > 4`) is shown. Reason: Cat decision 38,
    Chameleon 42, Mole 39 (attacks_emotes Q8).
47. **BB's own voice clips where the rip lacks the file**: `wardrobe_fx.py`'s voice job falls back to the AudioClip in BB's
    Resources container (`gameassets/characters/heroes/<cls>/voices/<name>`): `buiten` and `blazingArrow` are BB's own
    recordings; tto.md's P10 (TTO's `voices/buiten`) is dropped. Runic Sand plays `sounds/runicSand` (BB's file, the load
    TTO's code makes; BB's `Voices/runicSand` does not exist). Reason: BB is the content; Sheep decision 10 only where BB
    has nothing (skills_a verification 1, skills_b Read this first 5).
48. Summon sounds follow SOUND_REFS' naming and are listed in `builds`: `sound:phoenix_pheonix_cry`,
    `sound:phoenix_phoenix_skyCrimson`, `sound:phoenix_pheonix_unsummon`, `sound:gadina_gadina_cry`,
    `sound:buiten_buiten_summon` (the builder confirms the AudioClip's name), and the Gaos' if its summon / unsummon
    plays one; `lavu_summon` through `SOUND_ALIASES`. Reason: skills_b verification 2, skills_a verification 3.
49. Instant Cast's status tint, the FireRune! / EarthRune! texts: left out. Reason: Penguin decision 10, Bat 13, Bison 34,
    Cat 44 (effect_only Q3).

## Left out
50. Camera effects (motion blurs, shakes, the red ramp, Sky Crimson's colour ramp). Reason: Bison decision 35, Cat 43.
51. Statuses on a foe (World Ignition's ignite and its 800-damage explosion, Ground Lock's lock, the burns, Rune
    Fracture: `tto/runeFracture` is built through SKILL_FX, never cued), heal / cost numbers, hate, MP returns. Reason:
    Sheep decision 4, Chameleon 53, Mole 52.
52. onNormalAttackHit's gear procs on Mike Blink's hits; RPC_cAttack0 (draws nothing); activateIcon1; game code 967.
    Reason: Chameleon decision 53, Penguin decision 19 (attacks_emotes).
53. `volcanicSoul_ring` (Summon Gaos with Fire Soul): in neither game's data, no stand-in. Reason: Mole decision 33.
54. Ja Ascension's Solar Echo flares / Sunburn marks / Sunbursts (they need fire-skill hits under the crown): not cued,
    so `SunburnFx` is not built; `MonkeyBuitenOffering`, `BastionWardFx` and their prefabs (sanctumRaise's, unreleased)
    are not built. Reason: no tile spawns them (Mole decision 15); every part a cued effect needs is built.
55. The runic segments' trail, the hero's travel (Blazing Form's rush, the Earth Form punches' steps). Reason: decisions
    25, 28.
56. Titanic Earth Pulse's and Planet Breaker's hits, Upheaval's 12 m damage, Earth Guard's heals: drawn nothing in the
    game either.
57. **A follow-up job, for the lead's HANDOFF.md** (not this build): trace and tile the five untraced summon-move Bible
    cards (Gadina - Normal Attack `monkey_gadina_nAttack`, Ja - Detonate `monkey_ja_detonate`, Gaos - Fire / Rampage /
    Tail Spin) and the BB elementals' AIs (Phoenix_AI's repeat shots, Gadina_AI, Ja_AI, Gaos_AI); their field prefabs are
    already in the LAYOUTS. Reason: no report traced them and cues are never guessed (skills_a verification 9).

## Parts and data (every missing part is built)
58. Four builders on disjoint files (below in the plan): **monkey** (`fxparts/monkey.js` new, `fxparts/rotationcontrol.js`
    + `Rotate`, `fxparts/mesh.js` FX/Lavu line), **elementals** (`fxparts/elementals.js` new: summons + armours),
    **tto_monkey** (`fxparts/tto_monkey.js` new, `fxparts/shuriken.js`), **page_pipeline** (`wardrobe/index.html`,
    `pipeline/wardrobe_fx.py`, `pipeline/wardrobe_fx_tto.py`). The editor after them owns `wardrobe/fx_cues/monkey.json`,
    `pipeline/wardrobe_skill_icons.py`, `pipeline/wardrobe_fx_check.py`, `pipeline/wardrobe_fx_inventory.py` and the data
    build. Reason: parts.md "Who builds what" with its verification 4-5 (the golem to tto_monkey; the inventory to the
    editor, the lead's rule).
59. `wardrobe_fx.py`: parts.md's LAYOUTS block as written (Monkey_fireBall, Monkey_runicFlame / Sand, Rotate,
    Monkey_earthPulse / Monkey_lavu empty, the five summons, the AIs as `"s"`) + `"Phoenix_fireBall": [("mLv", "i")]`,
    `"Phoenix_skyCrimson_fire": []`; `Game.__init__` keeps the GameObject when a container key repeats (Gaos, gaosFire,
    Lavu); `EXTRA_FOLDERS["monkey"]` the five elemental folders + `gaos/effects`; `FIELD_PREFABS["monkey"]`:
    phoenix_summon_ring, ja_summon_ring, buiten_summonEffect, gadina_summonEffect, gadina_sword4, gadina_shield4,
    phoenix_fireBall, phoenix_fireBall_hit, phoenix_instantBlaze_ring, phoenix_skyCrimson_dust, phoenix_skyCrimson_fire,
    phoenix_skyCrimson_hit, gadina_earthGuard_ring, gadina_planetBreaker1, gadina_planetBreaker2; `ALIASES["monkey"]`:
    gaos_summon_ring, gaos_unsummon_ring (`elementals/gaos/effects/...`); `SOUND_REFS |= {"Phoenix", "Gadina", "Buiten",
    "Gaos"}`; `SOUND_ALIASES["monkey"]["lavu_summon"]`; `SHURIKEN_FROM_TTO["monkey"] = ["volcanicEruption"]` (no
    SHURIKEN_MAT: the by-material route, one match each); the voice fallback of decision 47; `NOT_DRAWN` keeps
    CharacterControl. Reason: parts.md, skills_a / skills_b verification.
60. `wardrobe_fx_tto.py`: an extra-folders list per class tried after `heroes/<cls>/effects/` (`"monkey"`: elementals/ja/
    effects, elementals/buiten/effects, elementals/runegolem, elementals/runegolem/effects); `SKILL_FX["monkey"]` = the 12
    heroes/monkey prefabs of tto.md section 5 + jaAscension_aura, buitenBastion_aura, RuneGolem and its 13 effects with
    stoneAegis and runeFracture (every `tto/` name in a `builds` list must be here: `cue_tto` reads cues only);
    `CODE_MOVERS` `Monkey.SunComet` on sunAvatar_comet and `Monkey.SolarCollapse` on sunAvatar_dive; the Animator's
    FX_Magic_Circle clip exported as `{"type": "Animator", "uv": {"len": 2, "w": [[0, 0], [2, -1]]}}` on the Sigil node
    (read from the controller's one streamed curve); the "take the GameObject" root guard (one line). Reason: parts T1
    with verification 1-3, 11; tto P1, P3, P5, P7.
61. The two `Eric/URP Particles` shaders (39 Additive, 2 Alpha Blended): Additive = tex x `_Color` x vertex colour x
    `_Emission`, One One, no depth write, Cull Off, no clamp (HDR `_Color`); Alpha Blended = SrcAlpha OneMinusSrcAlpha,
    alpha x `_Opacity`; `_SpeedMainTexUVNoiseZW.xy` scrolls the UV; the saved `_SrcBlend` / `_DstBlend` / `_ZWrite` are
    stale and ignored. Reason: parts T2 with verification 10, tto verification 4.
62. Shuriken: SubModule **yes** (Birth / Collision / Death sub-emitters; the child built idle with `emitAt`); NoiseModule
    as a cheap per-particle value-noise drift (APPROX); LightsModule through `api.pointLight`, at most two pooled lights
    per system, the brightest (APPROX); CustomData nothing. Reason: parts Q9 (whole bursts depend on Sub).
63. The Sigils' FX_Magic_Circle scroll is built: the Sigil's own material copy's map offset y follows the exported `uv.w`
    curve, looping. Reason: parts Q8 / verification 11.
64. Volcanic Eruption: `kill` 10 on the field (the 12 s Animation and the 22 ticks cut), the ring's `cut` 10.25. Reason:
    the 10 s rule (skills_a).
65. The cue file is pasted by the editor after the builders, from the corrected blocks: attacks_emotes (its blocks with
    verification 1's two Mike Blink entries), skills_a verification 8 (its whole block for the keys it lists, the rest as
    the body), skills_b verification 4, effect_only block 3, parts verification's `@Lavu:cast3`, tto verification's
    block; with these edits: decision 5's `cut` 0.1 on castRing; decision 7's `@JaAscension:damageCast1` (merged with
    damageCast1's cues); decisions 30 / 35's `end: 10` in place of `kill: 10` on every skill's own summon (Phoenix4, Ja4,
    Gadina4, Buiten4, Gaos, Blazing Arrow's Phoenix); decision 31's renames; decision 34's Gadina4 on `earthPulse`;
    decision 15's Phoenix - Fireball entry (`@Phoenix-Fireball:root`); decision 44's Fire Rune rolls; the summons' and
    rings' `builds` (skills_a verification 3, tto verification 8).
66. The check (`wardrobe_fx_check.py`, the editor's): OPTS += `alpha`, `standing`, `hide`, `moves`, `turn`, `attach`,
    `lavu`, `unsummon`, `boost`, `rise`, `head`, `top`, `dive`, `alt`; `split_key` strips `#<n>` (and checks step n of the
    sequence plays that clip), `entry_for` takes the step; `expected()` keeps only the forced alternative's `alt` cues.
    The cue-format comment in index.html learns the new options (page_pipeline). Reason: skills_a verification 10,
    skills_b verification 1, effect_only verification 2.
67. The inventory (the editor's): BUILT += Monkey_fireBall, Monkey_earthPulse, Monkey_lavu, Monkey_runicFlame,
    Monkey_runicSand (data only), Rotate, Phoenix_fireBall, Phoenix_skyCrimson_fire, Phoenix, Ja, Gadina, Buiten, Gaos (+
    their AIs, data only); the hero-prefab fields hpTransfer, castRing, castEffect_fire; NOTES for volcanicEruption's
    grafted systems; rerun it. Reason: the recipe's rule (parts.md, attacks_emotes part 2).
68. TTO1102's code with the 2026-11-09 bundles. Reason: Bat decision 44, Chameleon 44, Mole 57.

## Offered to the user for the Bible (not written there)
The Combo's stage 2 at stage 1 + 0.5 s, its hits at 0.4 / 0.8 s (0-7 m, 3.5-7.5 m), swing sounds at 0.2 / 0.6 s; Mike
Blink's timeline (Mike leaves the hand at 0.3 s, strikes at 0.5 / 0.8 s, back at 1.0 s, or 0.7 s without stage 2; the voice
on strike 1 only; it moves the worn weapon itself, which snaps to its mount's origin after each blink); HP Transfer
(cAttack1 0.7 s, the first heal 1.7 s after the press, the Mikes hitting within 3 m of the ally every 0.5 s); one `ko` and
one `dead` voice, BB's revive silent, `step_normal1` on both feet; `volcanicSoul_ring` missing from both games; every cast
release at 0.3 / 0.4 / 0.8 s (Fire Avatar 0.7 / 1.5, Earth Form 0.7 / 1.2, Lavu standby 2.4, Volcanic Eruption 0.3 /
12.0), the ring only from the bar's start, Summon Gaos's 8 s minimum bar; Blazing Arrow's 24 % Phoenix 2 m behind at 4.8 s
(TTO consumes only a Phoenix4 at the cast); Fire Avatar's create spawned twice; `buiten` and `blazingArrow` present in BB's
data though missing from the rip (the earlier "Blazing Arrow is silent" withdrawn); Runic Sand's missing BB voice (TTO plays
the sound); Runic Flame / Sand's life passed through the RPC's tID; Sentinel Guard / Earth Guard saying the Summon Defense
line, Summon Release the Unsummon line, Instant Blaze silent; Upheaval's first wave 2 s in then every 0.5 s, 1 SP a wave
with Revised Skill, Lavu circling 6 m out once every 3 s; Sky Crimson's timing (the Phoenix gone 2-5 s, the balls from 20 m
up at 16 m/s bursting only on the ground, the heal at 5.5 s); Planet Breaker's pulses at 1.1 / 1.4 / 1.7 s; Earth Guard's
ring 10 s while the guard runs 13 s; Summon Soul once per summon; Gadina's sword / shield chosen by Titan Sword / Aegis of
Earth rank; the armours living only in the form; Fire Avatar hiding every renderer, the form attack's level (and voice) by
idle time, its ball from 0.2 right / 1.5 up / 1.5 ahead at the target's position; Blazing Form's timeline; Instant Cast's
tint; Earth Rune sounding Fire Rune's sound; the Lavu skill using an effect (`Monkey_lavu`), not the elemental `Lavu`
character the Bible cites for its damage; Titanic Earth Pulse unsummoning the Gadina at 0 (its HP kept for the damage);
TTO: the boosted Ja / Buiten (level 6, the aura, the Buiten x 1.2; the TTO Buiten release drops castEffect_fire), Sun
Avatar's comet and crown geometry, the collapse rising 5 m first (TTO1106+ aiming it at a selected foe), the Rune Golem's
rise / roar / walk / quake-before-fist order / 2.4 s crumble, and its Rune Fracture look.
