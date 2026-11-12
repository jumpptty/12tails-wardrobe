# Chameleon effects + sounds research: the cast channel and its pool, the slayer and stride skills (skills_a)

Researcher `skills_a`, 2026-11-13 (home PC). Scope: the clips `allSlain`, `allSlayer1-3`, `backStep`, `cast1-4`,
`focusFire1-2`, `leftStride`, `massShot`, `needlePrison`, and every skill that plays them. Research only (recipe steps 1-3).
Line numbers are `D:\12tails\DecompiledSource\Chameleon.cs` unless another file is named. Times are seconds from the start
of the clip the cue is keyed by. Distance 0 = at the hero. Max rank and passives on everywhere.

Read-only probes, in `checks\fx_chameleon_research\skills_a\` (git-ignored):
- `clip_calls.txt`: `clip_calls.js` output for the class. `coroutines.txt`: every `$RPC_*` coroutine's first line.
- `clean.py <file> <from> <to>`: a line range with the opaque predicates worked out (a false test drops its block).
  `clean_<RPC>.txt` holds one per coroutine in scope; `mn.sh <RPC>` prints its MoveNext without the iterator boilerplate.
- `cond.py`: the same range with the predicates just dropped.
- `probe.json` / `probe_summary.txt` (`summ.py`): `wardrobe_fx.py chameleon --probe` of 46 effects (`probe_list.txt`).
- `probe2.py` / `probe2.json`: `needlePrison`, `campFire1`, `campFire2` in memory, with the two layouts read from the
  decompile (below). Nothing is written.
- `probe_fields.py` / `probe_fields.txt`: the Chameleon MonoBehaviour's fields. Field 4 `nAttack_bowFx1` = `bow_fire1`.
  `probe_ref.py`: needlePrison's `mPrisonArrow` = `needlePrison_arrow`.
- `stride_sim.py` / `stride_sim.txt`: Left Stride's Double Strider clone path, its arrows' aims, flights and hit points.
- `entries.py` -> `cues.json`, and `pretty.py` -> `cues_pretty.json`: the paste-ready entries at the end, checked as JSON.

---

## Read this first

1. **14 skills, 17 cue keys.** Every skill gets its own tile:
   - The **Cast** pool `cast3` has 5 members: True Invisibility, Mass Invisibility, Final Entrapment, Camp Fire, Mark of
     Slayer.
   - **Tent** goes through the same channel, then plays the `sleep` clip. It needs its own sequence:
     `@Tent:cast3` and `@Tent:sleep`.
   - **Immunity, Venom Shock, Blood Burn, Rusty Decay** play `cast3` straight from the key press, with no channel (the
     dispatcher `:8288`, `:8020`, `:7620`, `:6986`). Each needs its own one-step sequence, as the Sheep's Seal and Eden
     Sanctuary: `@Immunity:cast3`, `@VenomShock:cast3`, `@BloodBurn:cast3`, `@RustyDecay:cast3`.
   - **All Slayer** is four skills on one coroutine (sLv 1-4 = All Bug / Tail / Elemental / Machine Slayer). They differ
     on `allSlayer2` (the race's eye) and on `allSlayer3` (the race's voice, fire and hit). So both clips are pools with the
     same four member names. poolChains makes the four tiles from the first one. `fxStart` keeps `FX.pick` across steps
     (`index.html:4604-4612`), so each tile plays its own race on both clips.
   - The plain entries: Perfect Blend (`backStep`), Fatal Strike (`cast4`), Needle Prison, Mass Shot, Left Stride,
     All Slain.
   - `cast2` gets no entry: only the channel and the mission's `RPC_activateIcon1` play it (no tile, as the Penguin's
     decision 19).
   - Focus Fire gets no entry: no code plays it (item 9).
2. **Page changes needed** (`wardrobe/index.html`). SEQ `chameleon`:
   - Add `"Immunity: cast3"`, `"Venom Shock: cast3"`, `"Blood Burn: cast3"`, `"Rusty Decay: cast3"`.
   - Add `"Tent: cast1 cast2*@0 cast3~@0.4 sleep*~@0.7"`. sleep cuts in at 0.4 s with a 0.5 s crossfade in the game
     (`:36063`); the page's nearest fade is `~` = 0.2. The heal comes at 0.9 s and standby at 1.1 s.
   - Change All Slayer to `"All Slayer: allSlayer1 allSlayer2*@0.1 allSlayer3"`. This is the bar's floor, 0.1 s
     (`CharacterControl.cs:20584-20588`), as the Bat's Guardian decision. The eyes come on allSlayer2's first frame.
   - SEQ_SKILL `chameleon`: `{"@Immunity": "immunity", "@VenomShock": "venomShock", "@BloodBurn": "bloodBurn",
     "@RustyDecay": "rustyDecay", "@Tent": "tent"}`.
   - `pipeline/wardrobe_skill_icons.py` CLIP_SKILLS `chameleon`: `backStep: ["perfectBlend"]`, `cast4: ["fatalStrike"]`.
     The Bible's icon keys match every member name: `chameleon_allBugSlayer1`, `allTailSlayer2`, `allElementalSlayer3`,
     `allMachineSlayer4`, `trueInvisibility2`, `massInvisibility2`, `finalEntrapment2`, `campFire2`, `markOfSlayer5`,
     `tent5`, `immunity3`, `venomShock2`, `bloodBurn2`, `rustyDecay5`.
3. **Three voice bugs in BB; TTO fixes two of them.** These are cued by the Sheep's decision 10.
   - **All Slayer:** BB loads `Voices/allBugSlayer1 / 2` (and Tail, Elemental, Machine), `:33598-33876`. The rip has only
     `allBugSlayer.wav` etc., one each, so BB plays nothing. TTO1102 loads `Voices/allBugSlayer` ... with no number. Cued as
     `allBugSlayer`, `allTailSlayer`, `allElementalSlayer`, `allMachineSlayer`.
   - **True Invisibility:** BB asks `trueInvisibility1 / 2` (`:21286`, `:21317`), but the files are `invisible1 / 2`.
     TTO loads `invisible1 / 2` (pseudo `Chameleon.c:21367-21370`). Cued that way.
   - **Immunity:** it asks `immunity1 / 2` (`:19071`, `:19102`). Neither BB's data nor TTO has them, and TTO asks the
     same. **No voice cue.**
4. **Parts to build** (details under "Parts"):
   - `HERO_SKINS["FX/Invisible"]` (True / Mass Invisibility).
   - `HERO_SKINS["FX/Blend"]` (Perfect Blend; already attacks_emotes' P3).
   - `Chameleon_needlePrison` (16 arrows round the target).
   - `Chameleon_campFire` (a layout and a no-op).
   - The Double Strider clone's mover (shared with skills_b's Right Stride).
   - A `life` cue option (Final Entrapment's cage, 7 s).
   - `hideProp` (attacks_emotes' P2) and `Chameleon_nAttack` (attacks_emotes' P1) are used here too.
5. **The arrow in hand: `hideProp` slot L, not R.** On the page `R` = อาวุธหลัก (the first piece, the bow = mWep1 on
   mount_Hand_L) and `L` = อาวุธที่ 2 (the second piece, the arrow = mWep2 on mount_Hand_R):
   - `ChameleonEquipment.cs:1660-1715`.
   - `index.html:1036-1044`: "The Chameleon's bow (first piece) does belong on the left".

   attacks_emotes uses `L` (right). **skills_b's cues use `"R"`: that would hide the bow** (open question 9).
6. **After a cast-bar skill the arrow stays hidden.** RPC_cast1 switches mWep2's renderers off (`:18498-18517`). None of
   the six `_cast` coroutines switches them back on (no `enabled = true` in any of them). Only the next attack, or
   `invisible`'s end (`CharacterControl.cs:16458-16500`), shows it again. Cued as `hideProp L` until the next pick. This is
   a possible Bible finding.
7. **The blend look is FX/Blend, not FX/Invisible.**
   - `blend` (Perfect Blend; also Charge Attack and Silent Walk) on the hero's own team: FX/Blend
     (`CharacterControl.cs:36835-36929`).
   - `invisible` (True / Mass Invisibility): FX/Invisible, 0.2 s after the status (`:36942-36958` -> Block_989 Yield 0.2
     -> case 2 `:32493-32684`).
   - skills_b's `silentWalk` entry cues FX/Invisible for the blend, citing the invisible lines. It should be FX/Blend (open
     question 13).
8. **Not in the inventory, all probed:** `immunity`, `invisible`, `needlePrison` (+ `needlePrison_arrow`), `fatalStrike`,
   `venomShock`, `rustyDecay`, `campFire1 / 2`. They are loaded by CharacterControl's status code or by a string concat.
   Every one is ready except `needlePrison` (no layout for Chameleon_needlePrison) and `campFire1 / 2` (no layout for
   Chameleon_campFire).
9. **Focus Fire is not a skill.** `focusFire1 / 2` are in BB's rip (`heroes/chameleon/animations`, clips.json `tto: false`),
   but nothing plays them:
   - No BB file names them (`grep -r focusFire DecompiledSource` = 0).
   - TTO's pseudo names nothing, and its locale has no such skill.
   - The Bible has no card.

   NOTES.md:98 lists "Focus Fire" among the "TTO-only sequences": that is wrong (it is BB data no code plays). No cues
   (open question 14).

---

## cast1: RPC_cast1, the cast channel (plain entry)

`$RPC_cast1$22545` (`:17732-18689`). The dispatcher starts it for six skills: `:7032` (tent, sLv 5), `:7069`
(markOfSlayer, sLv 5), `:7722` (campFire), `:7969` (finalEntrapment), `:7990` (massInvisibility), `:8154`
(trueInvisibility). TTO1102's `<RPC_cast1>d__150` has the same six.

| t | what | source |
|---|---|---|
| 0 | cast time per skill: campFire / trueInvisibility 3 + sLv, massInvisibility 4 + 2 sLv, finalEntrapment / tent 6, markOfSlayer 7; magAdjust (the page: 0) | :18257-18368 |
| 0 | actionState attack, myCommand cast, cooldown | :18371-18380 |
| 0 | `PlayAnimation("cast1", 0.2f)`, Once | :18389 |
| 0 | voice cast1 / cast2, `Random.Range(0, 2)` | :18430-18489 |
| 0 | mWep2 (the arrow) hidden, never shown again here | :18498-18517 |
| 0 | castRing at the hero's position, `Quaternion.Euler(270, 90, 0)` world-absolute (createEffect) | :18534-18544 |
| 0.4 | `PlayAnimation("cast2", 0)` looped (cast1 is 0.4 s long) | Yield 0.4 :18585; :17901-17906 |
| 0.5 | the ring's `root` clip looped; the cast bar starts | Yield 0.1 :18592; :17933-17961 |
| bar end | the skill's `RPC_<skill>_cast` starts and sets myCommand: castRing's followState ends | :18075-18246 |

castRing (probe): Animation create 0.47 s / root 2 s / destroy; EffectControl life 60, afterLife 0.5, followPosition,
followState; its own looping Sounds/cast_ring.

At high INT the bar is its 0.1 s floor, so the release comes at about 0.6 s. The SEQ `cast2*@0` drops the game's 0.1 s
wait plus the 0.1 s bar (open question 2). The ring's cut is 0.35: the page restarts FX.t at the 0.4 s step edge (the Bat's
and the Penguin's 0.65 before 0.7). Its `root` clip at 0.5 s is never reached on the page.

## cast3: the Cast pool (`skills`): 5 members

Each starts with `PlayAnimation("cast3", 0.2f)` (the SEQ's `cast3~`). Standby is at 0.7 s.

| member | t | what | source |
|---|---|---|---|
| trueInvisibility (rank 2 + Erase Senses #412) | 0 | voice invisible1 / invisible2 (TTO's fix, Read this first 3) | :21276-21335 |
| | 0.4 | `invisible` on the target ally, here self (Sheep decision 1): chaAdjust(4 + 8 + 4) = 16 s, cut at 10 s; Effects/invisible at the hero (life 2, followPosition, own Sounds/invisible) | :21155; CharacterControl.cs:36942-36958 |
| | 0.6 | the FX/Invisible skin, kill 10 (part) | CharacterControl.cs:32493-32684 |
| massInvisibility (rank 2) | 0 | voice massInvisibility1 / 2 | :24703-24757 |
| | 0.4 | `invisible` on every Player in the team container, the caster too: chaAdjust(12) = 12 s, cut at 10 s; invisible at the hero; the skin at 0.6 | :24522-24575 |
| finalEntrapment (rank 2) | 0 | voice finalEntrapment1 / 2 | :25138-25197 |
| | 0.4 | Effects/finalEntrapment at the target's position, identity, `EffectControl.life = FloorToInt(chaAdjust(7))` = 7; the prefab says 6 (option `life`, part) | :24999-25004; :9116-9175 |
| campFire (rank 2) | 0 | voice campFire1 / 2 | :29530-29589 |
| | 0.4 | Effects/campFire2 on the ground 2 m ahead (getSpawnPos), `Euler(270, 90, 0)` world-absolute, Chameleon_campFire timer chaAdjust(30) = 30 s, cut at 10 s | :29355-29365; :9417-9458 |
| markOfSlayer (sLv 5) | 0 | no voice; markOfSlayer_ring at the hero (followState: cut at the 0.7 s standby) | :36884-36900 |
| | 0.4 | markOfSlayer_hit by the target at its bounds centre (10 m, 0.6 up) with the **hero's** rotation (no rot); slayerMark draws nothing | :36752-36792 |

The camera's motion blur (`:36694-36705`) is left out.

## Tent (`@Tent:cast3`, `@Tent:sleep`)

`RPC_tent_cast` (`:35950-36564`), started by the channel. `actionTime` is set at cast3's start.

| t (skill) | clip t | what | source |
|---|---|---|---|
| 0 | cast3 0 | cast3 (0.2 fade), voice tent1 / tent2; the m_fab14 item spent | :36368-36489 |
| 0.4 | sleep 0 | `PlayAnimation("sleep", 0.5f)` looped. tent_ring at the hero: the tent model `tent_tri`, stars, smoke, life 99, followState, own Sounds/tent | Yield 0.4 :36535; :36063-36096 |
| 0.9 | sleep 0.5 | castTime = magAdjust(12) with a cast bar (the bar rule: 0.1). The tent status (zzz emote, left out). The end test `actionTime + castTime + 0.5` has passed, so: tent_heal at the hero, full heal, cooldowns reset | Yield 0.5 :36526; :36128-36337 |
| 1.1 | sleep 0.7 | standby: tent_ring cut | Yield 0.2 :36533; :36228 |

`tent_destroy` (`:36181`) comes only when the channel is broken.

## Immunity, Venom Shock, Blood Burn, Rusty Decay: cast3 with no channel (`@<Skill>:cast3`)

Each starts with `PlayAnimation("cast3", 0.2f)`. Standby is at 0.5 s. The arrow (slot L) is hidden from 0 to 0.5.

- **Immunity** (rank 2 + Skin Shift #421, status level 5). `:18689-19240`.
  - Voice: none (Read this first 3).
  - At 0.2: immunity_ring at the hero (life 1, followPosition, own Sounds/immune_ring).
  - At 0.2: the immunity status, chaAdjust(12) = 12 s, cut at 10 s.
  - Its look (`CharacterControl.cs:36591-36613`): Effects/immunity at `collider.bounds.center + 0.1 × height` up. The
    Chameleon's CharacterController (center y 0.98, height 1.8, radius 0.3, Chameleon.prefab:898-910) puts it at
    **y 1.16**. Parented to the hero, scale `Clamp(0.3 + 0.4, 0.5, 1.5)` = **0.7**, no EffectControl, own looping
    Sounds/immune.
- **Venom Shock** (rank 2, enemy target). `:23758-24389`.
  - At 0: voice venomShock1 / 2 (venomShock3 is never played) and venomShock_ring at the hero.
  - At 0.2: the venomShock status on the target. Its apply (`CharacterControl.cs:36972-37030`) detonates the target's
    poison: Effects/venomShock at its bounds centre, identity, when the poison has more than 1 s left. Drawn at 10 m,
    0.6 up (open question 5).
  - The camera's venomRamp is left out.
- **Blood Burn** (rank 2). `:29654-30217`.
  - At 0: voice bloodBurn1 / 2.
  - At 0.2: bloodBurn at the hero (life 1, followPosition, own Sounds/cAttack_ring). The self-damage and the MP / SP
    heal draw nothing.
- **Rusty Decay** (one rank, status level 2). `:35336-35950`.
  - At 0: voice rustyDecay1 / 2 and rustyDecay_ring.
  - At 0.2: the rustyDecay status. Its apply (`CharacterControl.cs:37142-37200`) detonates rust: Effects/rustyDecay at the
    target's bounds centre, identity, when the rust has more than 1 s left. Drawn at 10 m, 0.6 up (open question 5).
  - The camera's rustyRamp is left out.

## backStep: Perfect Blend (plain entry)

`RPC_perfectBlend` (`:20438-20960`), rank 2 + Erase Senses #412.

| t | what | source |
|---|---|---|
| 0 | `PlayAnimation("backStep", 0)`, voice perfectBlend1 / 2 | :20789-20886 |
| 0.1 | moveSpeed -8 (the hop back: 1.6 m by 0.3 s, no mover on the page); perfectBlend_ring at the hero (life 1) | Yield 0.1 :20907; :20584-20607 |
| 0.3 | moveSpeed 0; blend at the hero + 1.2 up (own Sounds/blend); the blend status, chaAdjust(2 × 2 + 4) = 8 s: the FX/Blend skin, kill 8 | Yield 0.2 :20911; :20644-20693; CharacterControl.cs:36665-36929 |
| 0.5 | standby | Yield 0.2 :20918 |

## needlePrison: Needle Prison (plain entry)

`RPC_needlePrison` (`:21406-22195`), rank 2 + Mass House Lock #422. It needs a target: the 10 m point.

| t | what | source |
|---|---|---|
| 0 | `PlayAnimation("needlePrison", 0)`, voice needlePrison1 / 2 (needlePrison3 is never played) | :21915-22015 |
| 0 | #422: massLock_ring at the hero (life 1, followPosition; its rays delayed 0.8 s) | :22024-22061 |
| 0.3 | Sounds/cAttack_bow | Yield 0.3 :22103; :21564-21582 |
| 0.8 | Sounds/bow_fire1 (the field nAttack_bowFx1); arrow hidden to 1.0 | Yield 0.5 :22094; :21619-21658 |
| 0.8 | needlePrison status on the target (#422: every enemy within 6 m of it): getDebuff(3) + 2 = 5 s at equal CHA (Damage.cs:317-319), so kill 5 | :21684-21750 |
| 1.0 | standby | Yield 0.2 :22101 |

The status look (`CharacterControl.cs:36622-36656`):
- Effects/needlePrison at the target's feet, identity, parented to the target. It plays its own Sounds/needlePrison.
- Chameleon_needlePrison.Init(`Clamp(2 × radius, 0.5, 2)`) = **0.6** for a 0.3 m target. It spawns **16 needlePrison_arrow**
  one every 0.05 s at `pos + rotateH(0.6 × forward, i × 67.5°)`, `LookRotation(up)`, parented (`Chameleon_needlePrison.cs:144-213`).
- needlePrison_arrow: a skinned arrow with Animation root 0.5 s, a Light, an ImageEmitter.

## massShot: Mass Shot (plain entry)

`RPC_massShot` (`:22195-23037`), rank 2 + Mass House Lock #422.

| t | what | source |
|---|---|---|
| 0 | `PlayAnimation("massShot", 0)`, voice massShot1 / 2; the camera's AutoZoom left out | :22771-22907 |
| 0.2 | moveSpeed -2 (hop back); #422: massHouseShot at the hero (else massShot; life 1; its arrow rain delayed 0.4-0.6 s; own Sounds/massHouseShot) | Yield 0.2 :22927; :22342-22420 |
| 0.8 | arrow hidden to 1.4; hits on enemies in FindAreaTarget(hero, 9) | Yield 0.6 :22933; :22446-22591 |
| 1.2 / 1.4 | moveSpeed 0 / standby | :22629, :22701 |

FindAreaTarget measures to the target's edge (`Damage.cs:963-1120`). The 10 m point is out of the 9 m reach, so no
`nAttack_hit` is cued (the Penguin's Mana Arc, the Cat's and Bison's convention).

## cast4: Fatal Strike (plain entry)

`RPC_fatalStrike` (`:26159-26607`), rank 4 + Extra Arrows #403 (level 5, 10 arrows).

| t | what | source |
|---|---|---|
| 0 | Rewind + `PlayAnimation("cast4", 0)`, voice fatalStrike1 / 2, fatalStrike_ring at the hero (life 1, own Sounds/aura1) | :26409-26546 |
| 0.3 | the fatalStrike status, chaAdjust(12) = 12 s. Its look (`CharacterControl.cs:37038-37131`): Effects/fatalStrike (blood particles, no EffectControl) Instantiated at mount_Hand_L and at mount_Hand_R and parented to each. Cued with `bone`, kill 10 | Yield 0.3 :26569; :26313 |
| 0.5 | standby | Yield 0.2 :26567 |

## leftStride: Left Stride (plain entry)

`RPC_leftStride` (`:26607-27821`), rank 2 (5 arrows) + Double Strider #423 + Bow Mastery (40 m/s,
`Chameleon_nAttack.cs:94-100`) + Critical Plus 4.

| t | what | source |
|---|---|---|
| 0 | `PlayAnimation("leftStride", 0.2f)` | :27106 |
| 0 | the hero runs left at runSpeed + 1, facing the target; no mover on the page | :27112-27130; strideLeft :27546-27605 |
| 0 | #423: the old clone destroyed. doubleStrider_left at the hero: a skinned Chameleon with its own 2.7 s root clip, EffectControl life 3, followState | :27137-27207 |
| 0 | doubleStrideLeft moves the clone: every FixedUpdate, `LookAt(flat target)`, then `Translate((runSpeed + 1) × right × dt)` | :27725-27795 |
| 0 | voice leftStride1 / 2; strideShot_dust at the hero (life 2, followState, own looping Sounds/rightStride_footStep) | :27214-27337 |
| 0.366, 0.799, 1.232, 1.665, 2.098 | each shot: Sounds/bow_fire1 | Yield 0.366 :27371, 0.433 :27369; :26931-26937 |
| (each shot) | `RPC_nAttack_fire` from hero + TD(-0.38, 1.2, 1) at the target's centre | :26949-26971 |
| (each shot) | #423: a second arrow from the clone + its TD(0.4, 1.2, 1) | :27004-27032 |
| 0.366 → 2.298 | the arrow in hand (slot L) hidden | :26765-26792; :26823-26851 |
| shot + 0.22 | each arrow meets the target's 0.3 m radius: nAttack_hit with the hero's rotation; criticalPlus_hit at 20 %, its own draw per arrow (effect_only.md) | Chameleon_nAttack.cs:406-436, :620-669 |
| 2.298 | standby: the clone's and the dust's followState cut (cued 2.3) | Yield 0.2 :27365; :26862-26889 |

- runSpeed = `0.01 × (400 + 2 × AGI − 4 × weight)` (CharacterDataClass.cs:979, loaded into CharacterControl.cs:1458). At
  the page's stats (stat 1, weight 0) that is 4.02, so the clone moves at **5.02 m/s**.
- The clone's spots (`stride_sim.py`): x 2.10 / 3.89 / 5.58 / 7.01 / 8.06, d 1.23 / 1.85 / 2.89 / 4.27 / 5.85. It curves
  towards the target as it turns to face it. Its arrows' yaw is −13.5 / −25.5 / −38.2 / −50.8 / −62.8°.
- The hero's arrows: rot [3.81, 2.42, 0], all five the same (she stays).
- The clone's arrows go through `RPC_nAttack_fire` too, so they are real Combo arrows (Bible :327, :440, :446).

## allSlayer1 / allSlayer2 / allSlayer3: All Slayer (plain, pool, pool)

`RPC_allSlayer` (`:32144-32805`) and `RPC_allSlayer_fire` (`:32805-34044`). sLv 1-4 = All Bug / Tail / Elemental /
Machine Slayer, each with its own cooldown key; Improved Slayer 4.

| t (skill) | clip, t | what | source |
|---|---|---|---|
| 0 | allSlayer1, 0 | `PlayAnimation("allSlayer1", 0)`; no voice | :32440 |
| 0.5 | allSlayer1, 0.5 | allSlayer_ring at the hero (life 60, afterLife 0.2, followState): cut 0.65 on the page; the game cuts it at 0.8 | Yield 0.5 :32734; :32291-32309 |
| 0.7 | allSlayer2, 0 | `PlayAnimation("allSlayer2", 0)` looped; the bar magAdjust(4 + 4) (the rule: 0.1) | Yield 0.2 :32739; :32346-32390 |
| 0.7 | allSlayer2, 0 | first frame: the marking pass (FindAreaTarget 40 m; the race, or slayerMark; up to 8): the race's eye by the target at its bounds centre (life 1 + 0.5, own Sounds/slayerCharge). One pass: the next would be 2 s later | :32461-32673; RPC_allSlayer_mark :9568-9760 |
| 0.8 | allSlayer3, 0 | `PlayAnimation("allSlayer3", 0)`; the race's voice (TTO's fix); the camera's motion blur left out | :33531-33895 |
| 1.0 | allSlayer3, 0.2 | the arrow hidden (to 0.95); the race's `all<Race>Slayer_fire` at the hero (life 1, own Sounds/slayerFire) | Yield 0.2 :33944; :32952-33157 |
| 1.1 | allSlayer3, 0.3 | hits: RPC_allSlayer_hit Instantiates `all<Race>Slayer_hit` at the target's feet, identity (a bolt from 12 m; own Sounds/allSlayer_hit) | Yield 0.1 :33928; :33191-33347; :9766-9930 |
| 1.6 / 1.75 | allSlayer3, 0.8 / 0.95 | standby / the arrow back | :33439, :33479-33507 |

- `allBugSlayer_fire` is spelled `allBugSLayer_fire` in the rip. Resources.Load and `wardrobe_fx.effect()` both find it
  in any case (probe OK).
- The page's target stands for one of the skill's race (open question 5).

## allSlain: All Slain (plain entry)

`RPC_allSlain` (`:34044-34709`), rank 2.

| t | what | source |
|---|---|---|
| 0 | `PlayAnimation("allSlain", 0)`, voice allSlain1 / 2 (allSlain3 is never played) | :34489-34589 |
| 0 | allSlain_ring at the hero (life 2, afterLife 0.2, own Sounds/allSlain_ring) | :34598-34614 |
| 0.7 | allSlain_hit at every target in the All Slain list (feet, identity; a bolt from 12 m; own Sounds/allSlain_hit): drawn at the 10 m point (open question 5); the camera's motion blur left out | Yield 0.7 :34655; :34191-34243; :9940-9975 |
| 0.8 | the camera shake, left out | Yield 0.1 :34659; :34310 |
| 1.0 / 1.5 | damage / standby | :34377, :34419 |

## focusFire1 / focusFire2: no entry

Read this first 9. The SEQ `"Focus Fire: focusFire1 focusFire2"` stays a plain move: no skill, no effects, no sounds.

---

## Effects in this scope (probe)

| effect | ready? | notes |
|---|---|---|
| castRing | ready | Animation create / root / destroy, life 60, followState |
| invisible | ready | VortexEmitter + RingEmitter, life 2 |
| finalEntrapment | ready | SkinnedMesh cage, Animation root 0.9 s, life 6 (code 7) |
| campFire1 / campFire2 | **needs the Chameleon_campFire layout + a no-op part** | StaticMesh fire + legacy particles; no EffectControl |
| markOfSlayer_ring, markOfSlayer_hit | ready | |
| tent_ring, tent_heal, tent_destroy | ready | the tent StaticMesh `tent_tri` |
| immunity_ring, immunity | ready | immunity: RingEmitters, no EffectControl |
| venomShock_ring, venomShock, rustyDecay_ring, rustyDecay, bloodBurn | ready | |
| perfectBlend_ring, blend | ready | |
| massLock_ring, massHouseShot (massShot) | ready | |
| needlePrison | **needs the Chameleon_needlePrison layout + part** | the root: the script and an AudioSource only |
| needlePrison_arrow | ready | SkinnedMesh arrow, Light, ImageEmitter |
| fatalStrike_ring, fatalStrike | ready | |
| strideShot_dust | ready | |
| doubleStrider_left | ready to draw; **its motion is a part** | SkinnedMesh clone, Animation root 2.7 s, life 3 |
| nAttack | **needs Chameleon_nAttack** (attacks_emotes P1) | ProjectileControl velocity z 30 (40 with Bow Mastery) |
| nAttack_hit, criticalPlus_hit | ready | |
| allSlayer_ring, the four `*Slayer_eye`, `all*Slayer_fire`, `all*Slayer_hit`, allSlain_ring, allSlain_hit | ready | the hits: BoltEmitter + EffectControl velocity |

Sounds: every voice cued is in `voices/`. The `sound` cues cAttack_bow and bow_fire1 are in `sounds/`. Every effect's own
sound resolves: aura1 is in `Resources/sound/fx`, through rip_wav's fallback.

## Parts (for the parts stage)

1. **`HERO_SKINS["FX/Invisible"]`** (True / Mass Invisibility). On the hero's own team, every Diffuse renderer's material
   becomes `new Material(FX/Invisible)` with its mainTexture, and every other renderer is switched off
   (`CharacterControl.cs:32626-32684`). It comes 0.2 s after the status. The game's shader text is in
   `checks/fx_chameleon_research/parts/shaders.txt:254`:
   - pass 1: the texture at alpha 0.35;
   - pass 2: `Cull Front`, `Blend SrcAlpha SrcColor`, a pushed-out shell.

   The rip's `Invisible.shader` is an AssetRipper dummy.
2. **`HERO_SKINS["FX/Blend"]`** (Perfect Blend). The same switch (`:36835-36929`). This is attacks_emotes' P3 (Charge
   Attack): one part for both.
3. **`Chameleon_needlePrison`**:
   - `wardrobe_fx.py` LAYOUTS `[("mPrisonArrow", "r")]` (Chameleon_needlePrison.cs:47, 8 bytes, proved by probe2.py).
   - A page part that, from the spawn, places 16 copies of the referenced `needlePrison_arrow` (the entry's
     `builds`). One every 0.05 s, at `rotateH(r × forward, i × 67.5°)`, `LookRotation(up)`, parented to the prison.
     `r` = the cue's `radius`, 0.6.
   - Destroyed with the prison (kill 5).
4. **`Chameleon_campFire`**: LAYOUTS `[("mLv", "i")]` (Chameleon_campFire.cs:219, 4 bytes). A no-op part: its Update only
   heals sitting allies and ends the fire at its timer (Chameleon_campFire.cs:52-183). The cue's kill does that.
5. **The Double Strider clone's mover** (doubleStrider_left here, doubleStrider_right in skills_b). Every 0.02 s, until
   the cut:
   - turn the clone to face the cue's `to` on the flat;
   - move it along its own right by `strafe × dt` m.

   Here `strafe` is +5.02. skills_b's Right Stride has `strafe` −6; one runSpeed for both (open question 8).
6. **`life` cue option**: sets the spawned root's `EffectControl.life` (`RPC_finalEntrapment_hit :9172`), so the cage
   lasts 7 s, not the prefab's 6.
7. Used from attacks_emotes:
   - `hideProp` (P2): slot L.
   - `Chameleon_nAttack` (P1): Left Stride's 10 arrows. They are the Normal Attack's arrow: a copy of the worn arrow
     piece, 40 m/s, `to` = the target 0.6 m up.

   Left Stride's `nAttack_hit` / `criticalPlus_hit` are explicit cues at the arrival times, as the Penguin's Mana Missile.
   If P1 ends up spawning its own hit, drop them.

## Passives, ranks, random picks

- **Ranks:** Immunity 2, Perfect Blend 2, True / Mass Invisibility 2, Needle Prison 2, Mass Shot 2, Venom Shock 2,
  Final Entrapment 2, Fatal Strike 4, Left Stride 2, Camp Fire 2, Blood Burn 2, All Slain 2. Each All Slayer has one
  rank. Tent and Mark of Slayer are sLv 5 (the dispatcher). Rusty Decay is level 2.
- **Passives on:**
  - Skin Shift #421: Immunity level 5, no change to the look.
  - Erase Senses #412: Perfect Blend 8 s, True Invisibility 16 s.
  - Mass House Lock #422: massLock_ring, massHouseShot, Needle Prison +2 s.
  - Extra Arrows #403: Fatal Strike level 5.
  - Double Strider #423: the clone.
  - Bow Mastery: 40 m/s.
  - Far Reach 4: the arrow's life 0.8 s.
  - Improved Slayer 4: All Slayer's bar and its cap of 8.
  - Critical Plus 4: 20 % crits.
- **Random picks:** every `voice1|voice2` is `Random.Range(0, 2) == 0` (the lines above). The Cast pool and the All
  Slayer pools are even picks per play. Critical Plus is an independent `p 0.2` per arrow.
- **Durations at the page's CHA 1:** chaAdjust(n) = int(n × 1.015) (CharacterControl.cs:20593-20619): 8, 12, 16, 30,
  and 7 for the cage. Cut at 10 s: invisible, immunity, fatalStrike, campFire.

## TTO

- TTO1102 has every coroutine here (`pseudo/Chameleon.c`) with the same effect names.
- The only string changes are the two voice fixes (Read this first 3). Its annotated waits match where they show:
  - leftStride 0.366 / 0.433 / 0.2;
  - tent 0.4 / 0.5 / 0.1 / 0.2;
  - fatalStrike 0.3 / 0.2;
  - immunity 0.2 / 0.3.
- None of these skills is a TTO-only skill. The released TTO list (apexHunt, chainLightning, venomPhantom1-3) is
  outside this scope.

## Possible Bible findings (to offer the user; not written there)

1. **All Slayer is silent in BB.** Its numbered voices (allBugSlayer1 / 2 ...) don't exist; the files are unnumbered.
   TTO loads the unnumbered ones. All Bug Slayer's branch also writes Blood Burn's voice cache field. This is harmless:
   the load returns null, so Blood Burn reloads its own voice later.
2. **True Invisibility is silent in BB.** It asks trueInvisibility1 / 2; the files are invisible1 / 2. TTO fixed it.
3. **Immunity has no voice in BB or TTO.** It asks immunity1 / 2, which neither has.
4. **After any cast-bar skill the arrow in hand stays hidden** until the next attack, or until `invisible` ends.
5. **Left Stride's Double Strider clone runs the other way.** It moves at runSpeed + 1 and turns to the target every
   physics step. The two split apart at 2 × (runSpeed + 1).
6. **focusFire1 / 2 are unused animations** in BB's data, played by no client.
7. **Unused voice files:** needlePrison3, venomShock3, allSlain3.

## Open questions (each with my recommended answer)

1. **All Slayer's held step:** `allSlayer2*@0.1` (the bar's floor) instead of `@0`? **Yes**: the eyes spawn on its
   first frame, as the Bat's Guardian `bigCast2*@0.1`.
2. **The Cast tile's `cast2*@0`:** the game shows cast2 for 0.1 s plus the 0.1 s floor bar. **Keep `@0`**: every class's
   Cast tile has it, and the ring is cut at the cast1 edge anyway.
3. **The five new sequences and SEQ_SKILL entries** (Read this first 2). **Yes**: one tile per skill. Tent's sleep and
   the four channel-less skills can't share the Cast host.
4. **Tent's channel by the cast-bar rule.** At high INT the sleep lasts 0.7 s and the tent stands 0.7 s; at the page's
   stats it would be magAdjust(12) = 12 s. **Follow the rule (0.7 s)**: it is the user's "assume high INT, no cast bar",
   applied as to Slayer and All Slayer. If the tent looks too brief, `sleep*~@3` with tent_heal at 3 + 0.1 is the
   alternative for the user.
5. **Effects that need a state on the enemy:**
   - Venom Shock needs poison, Rusty Decay needs rust.
   - All Slain needs a listed target.
   - All Slayer needs the race.

   **Draw them at the 10 m target** (the rule: effects on an enemy go to the target point). The page's target stands for
   a fitting enemy; without it these tiles would show nothing at the target.
6. **Mass Shot's hits:** none. The 9 m reach misses the 10 m point. **Leave them out**, as Mana Arc.
7. **Perfect Blend's 1.6 m hop:** ring and blend both at the hero (no mover). **Yes**, as Feral Strike and Frost Field.
   The alternative is the ring 1.6 m ahead, where she stood.
8. **The clone's speed:** 5.02 (runSpeed at the page's stats, CharacterDataClass.cs:979) here, 6 in skills_b (the field's
   initial 5, CharacterControl.cs:88). **Use one value for both strides; I recommend 5.02**, because loadCharacterData
   replaces the 5 (CharacterControl.cs:1458). The clone's spots and aims here are worked out for 5.02.
9. **hideProp slot:** **L** (the arrow, the second piece). skills_b's `"R"` cues should become `"L"`.
10. **The voice fixes:** True Invisibility `invisible1|invisible2` and All Slayer's unnumbered voices (TTO's fixes),
    and no Immunity voice. **As cued** (Sheep decision 10).
11. **Final Entrapment's 7 s:** **build the `life` option.** It is tiny. Without it the cage ends at 6 s, harmless.
12. **Camera effects** (motion blur, AutoZoom, colour ramps, shake) and **Tent's zzz emote:** left out, as every class
    so far.
13. **Hero skins:** build FX/Invisible and FX/Blend. skills_b's silentWalk skin should be FX/Blend (Read this first 7).
14. **Focus Fire:** no cues. **Keep the tile as a plain move** (it is the Chameleon's own animation, not a copied one).
    Removing it like the Wolf's Cast tile is the user's call. Correct NOTES.md:98 ("TTO-only").
15. **castRing's root clip at 0.5 s:** not reached (cut at 0.35). **No action.**

---

## Paste-ready entries for `wardrobe/fx_cues/chameleon.json`

Generated by `checks/fx_chameleon_research/skills_a/entries.py` and checked as JSON (`cues_pretty.json`). The keys go at
the top level of the cue file. Build names besides the cues: `builds` needlePrison_arrow (in its entry).

```json
{
  "cast1": {
    "why": "Chameleon.cs RPC_cast1 ($RPC_cast1$22545, :17732-18689), the cast channel for True Invisibility, Mass Invisibility, Camp Fire, Final Entrapment, Tent and Mark of Slayer (the dispatcher :7032-8154, its skill switch :18083-18246): at 0 (IL_454): cast time and cooldown per skill (:18257-18380), actionState attack, myCommand cast, clip cast1 (0.2 fade, :18389), voice cast1 / cast2 (Random.Range(0, 2) :18430, Voices/cast1 :18442, Voices/cast2 :18473; PlayOneShot volume 1 for the local player), the arrow in hand (mWep2, the page's slot L) hidden (:18498-18517) and never shown again by the channel or the release (no enabled = true in RPC_cast1 or any of the six _cast coroutines; the next attack or invisible's end shows it): hideProp L until the next pick (plans/fx_chameleon/attacks_emotes.md part P2), castRing at the hero's position with Quaternion.Euler(270, 90, 0), world-absolute (createEffect :18544; Resources chameleon/effects/castRing :18534; EffectControl life 60, afterLife 0.5, followPosition, followState; Animation create / root / destroy; plays its own looping Sounds/cast_ring); Yield 0.4 (:18585): cast2 cut in and looped at 0.4 s (:17901-17906; the cast1 clip is 0.4 s); Yield 0.1 (:18592): the ring's root clip looped and the cast bar magAdjust (:17933-17961; the page: none, its floor 0.1 s, CharacterControl.cs:20584-20588), then each frame until it ends (YieldDefault(4) :18607) the skill's RPC_<skill>_cast starts (:18088-18246) and sets myCommand to the skill: the ring's followState cut there (about 0.6 s); on the page the cast1 step ends at 0.4 s and FX.t restarts, so the cut is cued 0.35 (the Bat's and the Penguin's 0.65 before their 0.7 s edge)",
    "cues": [
    [0, "voice", "cast1|cast2"],
    [0, "fx", "castRing", {"rot": [270, 90, 0], "cut": 0.35}],
    [0, "hideProp", "L"]
    ]
  },
  "cast3": {
    "why": "Chameleon.cs: the cast3 clip after the RPC_cast1 channel (the bar 0 s, then RPC_cast1 starts the skill's coroutine, :18083-18246): 5 Chameleon skills, one per play, even chance, picked anew on every play (each with its own tile, poolChains): True Invisibility (:21241), Mass Invisibility (:24668), Final Entrapment (:25103), Camp Fire (:29464), Mark of Slayer (:36878), all PlayAnimation(cast3, 0.2f), the SEQ's cast3~. Tent (:36368) also goes through the channel but plays sleep after cast3: its own sequence (@Tent:cast3, @Tent:sleep). Immunity, Venom Shock, Blood Burn and Rusty Decay play cast3 straight from the key press, with no channel (the dispatcher :8288, :8020, :7620, :6986): their own sequences (@Immunity:cast3 ...), as the Sheep's Seal and Eden Sanctuary",
    "skills": {
      "trueInvisibility": {"why": "Chameleon.cs RPC_trueInvisibility_cast (:20960-21406), max rank 2 + Erase Senses #412 (passives on): at 0: clip cast3 (0.2 fade, :21241), voice: the code asks Voices/trueInvisibility1 / trueInvisibility2 (Random.Range(0, 2) :21276, :21286, :21317), which BB's data does not have (voices/ holds invisible1 / invisible2); TTO1102 loads Voices/invisible1 / invisible2 (TTO pseudo Chameleon.c:21367-21370): TTO's fix, as plans/fx_sheep/decisions.md 10; Yield 0.4 (:21368): the target ally (or self: ally-targeted skills show as self-casts, plans/fx_sheep/decisions.md 1) gets 'invisible' sLv 2 for chaAdjust(4 + 4 x 2 + 4) = 16 s (:21155; chaAdjust(16) at the page's CHA 1 = 16, CharacterControl.cs:20593-20619), cut at 10 s (the long-buff rule) (CharacterControl.cs status add 'invisible' :36942-36958: Effects/invisible at the holder's position, identity, InitEffectControl(holder): EffectControl life 2, followPosition, plays its own Sounds/invisible; then Yield 0.2 (Block_989 :42212-42213) and case 2 (:32493-32684): for the holder's own team every Diffuse renderer's material becomes new Material(FX/Invisible) with its mainTexture and every other renderer is switched off: the hero-skin cue FX/Invisible, a part to build); Yield 0.3 (:21364): standby at 0.7 s (:21182)",
        "cues": [
        [0, "voice", "invisible1|invisible2"],
        [0.4, "fx", "invisible"],
        [0.6, "skin", "FX/Invisible", {"kill": 10}]
        ]},
      "massInvisibility": {"why": "Chameleon.cs RPC_massInvisibility_cast (:24389-24837), max rank 2: at 0: clip cast3 (0.2 fade, :24668), voice massInvisibility1 / massInvisibility2 (Random.Range(0, 2) :24703, :24713, :24744); Yield 0.4 (:24776): every Player in the caster's team container, the caster too, gets 'invisible' sLv 2 for chaAdjust(4 x 2 + 4) = 12 s (:24522-24575), cut at 10 s (CharacterControl.cs status add 'invisible' :36942-36958: Effects/invisible at the holder's position, identity, InitEffectControl(holder): EffectControl life 2, followPosition, plays its own Sounds/invisible; then Yield 0.2 (Block_989 :42212-42213) and case 2 (:32493-32684): for the holder's own team every Diffuse renderer's material becomes new Material(FX/Invisible) with its mainTexture and every other renderer is switched off: the hero-skin cue FX/Invisible, a part to build); Yield 0.3 (:24785): standby at 0.7 s (:24609)",
        "cues": [
        [0, "voice", "massInvisibility1|massInvisibility2"],
        [0.4, "fx", "invisible"],
        [0.6, "skin", "FX/Invisible", {"kill": 10}]
        ]},
      "finalEntrapment": {"why": "Chameleon.cs RPC_finalEntrapment_cast (:24837-25269), max rank 2, enemy target: the 10 m target point: at 0: clip cast3 (0.2 fade, :25103), voice finalEntrapment1 / finalEntrapment2 (Random.Range(0, 2) :25138, :25148, :25179); Yield 0.4 (:25220): mDuration = FloorToInt(chaAdjust(2 x 2 + 3)) = 7 (:24999) and RPC_finalEntrapment_hit at the target's position (:25004; :9116-9175): the old cage destroyed, Effects/finalEntrapment Instantiated there with Quaternion.identity, its EffectControl.life set to 7 (:9172; the prefab says 6: the cue's life, a page option to build; plays its own Sounds/finalEntrapment_hit and the looping finalEntrapment); Yield 0.3 (:25214): standby at 0.7 s (:25044)",
        "cues": [
        [0, "voice", "finalEntrapment1|finalEntrapment2"],
        [0.4, "fx", "finalEntrapment", {"d": 10, "life": 7}]
        ]},
      "campFire": {"why": "Chameleon.cs RPC_campFire_cast (:29212-29654), max rank 2: at 0: clip cast3 (0.2 fade, :29464), voice campFire1 / campFire2 (Random.Range(0, 2) :29530, :29540, :29571); Yield 0.4 (:29608): RPC_campFire_create at getSpawnPos(position + 2 x forward) (the ground 2 m ahead, :29355-29365; :9417-9458): Effects/campFire + sLv = campFire2, Instantiated with Quaternion.Euler(270, 90, 0), world-absolute (:9440), Chameleon_campFire.Init(owner, chaAdjust(30) = 30 s) (:29360, :9452): its Update only heals sitting allies every 4 s and destroys the fire when the 30 s end (Chameleon_campFire.cs:52-183; it draws nothing: a no-op part, its one field mLv i, Chameleon_campFire.cs:219), cut at 10 s (kill 10; plays its own looping Sounds/campFire); Yield 0.3 (:29603): standby at 0.7 s (:29405)",
        "cues": [
        [0, "voice", "campFire1|campFire2"],
        [0.4, "fx", "campFire2", {"d": 2, "rot": [270, 90, 0], "kill": 10}]
        ]},
      "markOfSlayer": {"why": "Chameleon.cs RPC_markOfSlayer_cast (:36564-36976), max rank (sLv 5, the dispatcher :7069), enemy target: the 10 m target point: no voice; at 0: clip cast3 (0.2 fade, :36878) and markOfSlayer_ring at the hero's position and rotation (createEffect :36900; EffectControl life 1, afterLife 1, followPosition, followState: cut at the standby, 0.7 s); the camera's motion blur for the local player (:36694-36705) left out; Yield 0.4 (:36927): markOfSlayer_hit created by the target at its collider.bounds.center with the HERO's rotation (:36770: no rot; the target 0.6 m up, plans/fx_penguin/decisions.md 3; plays its own Sounds/markOfSlayer_hit) and the slayerMark status (:36792: draws nothing); Yield 0.3 (:36936): standby at 0.7 s (:36819)",
        "cues": [
        [0, "fx", "markOfSlayer_ring", {"cut": 0.7}],
        [0.4, "fx", "markOfSlayer_hit", {"d": 10, "y": 0.6}]
        ]}
    }
  },
  "@Tent:cast3": {
    "why": "Chameleon.cs RPC_tent_cast (:35950-36564; RPC_cast1 starts it when the bar ends, :18192-18216), the one rank (sLv 5, :7032): at 0 (IL_885): clip cast3 (0.2 fade, :36368), voice tent1 / tent2 (Random.Range(0, 2) :36409, :36421, :36452); the m_fab14 item spent (:36489); Yield 0.4 (:36535): the sleep clip, its entry (@Tent:sleep) has the rest",
    "cues": [
    [0, "voice", "tent1|tent2"]
    ]
  },
  "@Tent:sleep": {
    "why": "Chameleon.cs RPC_tent_cast case 2 at 0.4 s (:36063-36096): PlayAnimation(sleep, 0.5f) looped (the SEQ's sleep*~: the page's nearest fade is 0.2) and tent_ring at the hero's position and rotation (createEffect :36091; the tent model tent_tri, stars, smoke; EffectControl life 99, followPosition, followState; plays its own Sounds/tent); Yield 0.5 (:36526): case 3 at 0.9 s: the channel castTime = magAdjust(12) with a cast bar (:36128-36151; the cast-bar rule, high INT: its floor 0.1 s) and the tent status (:36139: moveSpeed 0, a zzz emote every 3 s, CharacterControl.cs:9274-9289, left out); the channel's end test actionTime + castTime + 0.5 (:36280, actionTime from cast3's start) has passed, so at 0.9 s (sleep 0.5 s): tent_heal at the hero (:36306; plays its own Sounds/tent_heal), the full heal and the cooldown reset (:36326-36337, nothing drawn); Yield 0.2 (:36533): standby at 1.1 s (sleep 0.7 s, :36228): tent_ring's followState cut there. tent_destroy (:36181) comes only when the channel is broken: not cued",
    "cues": [
    [0, "fx", "tent_ring", {"cut": 0.7}],
    [0.5, "fx", "tent_heal"]
    ]
  },
  "@Immunity:cast3": {
    "why": "Chameleon.cs RPC_immunity (:18689-19240), started straight from the key press (the dispatcher :8288, no channel), max rank 2 + Skin Shift #421 (status level 2 x 2 + 1 = 5): at 0: clip cast3 (0.2 fade, :19018); voice: the code asks Voices/immunity1 / immunity2 (Random.Range(0, 2) :19059, :19071, :19102), which BB's data does not have, and TTO1102 asks the same (TTO pseudo Chameleon.c RPC_immunity d__152): no voice cue; the arrow in hand (slot L) hidden (:19127-19146) until 0.5 s (:18885-18920): hideProp L; Yield 0.2 (:19174): immunity_ring at the hero's position and rotation (createEffect :18854; EffectControl life 1, followPosition; plays its own Sounds/immune_ring) and the immunity status for chaAdjust(12) = 12 s (:18876), whose look (CharacterControl.cs status add :36591-36613) is Effects/immunity at collider.bounds.center + 0.1 x height up (CharacterController center y 0.98, height 1.8, radius 0.3, Chameleon.prefab: y 1.16), the hero's rotation, parented to the hero, scaled Clamp(0.3 + 0.4, 0.5, 1.5) = 0.7 (no EffectControl: it goes with the status; plays its own looping Sounds/immune), cut at 10 s (kill 10); Yield 0.3 (:19172): standby at 0.5 s (:18948)",
    "cues": [
    [0, "hideProp", "L", {"kill": 0.5}],
    [0.2, "fx", "immunity_ring"],
    [0.2, "fx", "immunity", {"y": 1.16, "scale": 0.7, "kill": 10}]
    ]
  },
  "@VenomShock:cast3": {
    "why": "Chameleon.cs RPC_venomShock (:23758-24389), started straight from the key press (the dispatcher :8020, no channel), max rank 2, enemy target: the 10 m target point: at 0: clip cast3 (0.2 fade, :24098), voice venomShock1 / venomShock2 (Random.Range(0, 2) :24139, :24151, :24182; venomShock3 is never played) and venomShock_ring at the hero's position and rotation (createEffect :24225; plays its own Sounds/venomShock_ring); the arrow in hand (slot L) hidden (:24239-24258) until 0.5 s (:23965-24000): hideProp L; the camera's venomRamp (:24281) left out; Yield 0.2 (:24314): the venomShock status on the target (:23956), whose apply (CharacterControl.cs:36972-37030) detonates the target's poison: Effects/venomShock created by the target at its collider.bounds.center, identity (:37002; the target 0.6 m up; plays its own Sounds/venomShock), when it has poison with more than 1 s left: drawn (the skill's point; the page's target stands for a poisoned one, open question 5); Yield 0.3 (:24308): standby at 0.5 s (:24028)",
    "cues": [
    [0, "voice", "venomShock1|venomShock2"],
    [0, "fx", "venomShock_ring"],
    [0, "hideProp", "L", {"kill": 0.5}],
    [0.2, "fx", "venomShock", {"d": 10, "y": 0.6}]
    ]
  },
  "@BloodBurn:cast3": {
    "why": "Chameleon.cs RPC_bloodBurn (:29654-30217), started straight from the key press (the dispatcher :7620, no channel), max rank 2: at 0: clip cast3 (0.2 fade, :29994), voice bloodBurn1 / bloodBurn2 (Random.Range(0, 2) :30035, :30047, :30078); the arrow in hand (slot L) hidden (:30103-30122) until 0.5 s (:29855-29883): hideProp L; Yield 0.2 (:30152): bloodBurn at the hero's position and rotation (createEffect :29819; EffectControl life 1, followPosition; plays its own Sounds/cAttack_ring), the self-damage 30 and the MP / SP heal (:29841-29846, nothing drawn); Yield 0.3 (:30156): standby at 0.5 s (:29911)",
    "cues": [
    [0, "voice", "bloodBurn1|bloodBurn2"],
    [0, "hideProp", "L", {"kill": 0.5}],
    [0.2, "fx", "bloodBurn"]
    ]
  },
  "@RustyDecay:cast3": {
    "why": "Chameleon.cs RPC_rustyDecay (:35336-35950), started straight from the key press (the dispatcher :6986, no channel), its one rank (status level 2), enemy target: the 10 m target point: at 0: clip cast3 (0.2 fade, :35665), voice rustyDecay1 / rustyDecay2 (Random.Range(0, 2) :35706, :35718, :35749) and rustyDecay_ring at the hero's position and rotation (createEffect :35792; plays its own Sounds/venomShock_ring); the arrow in hand (slot L) hidden (:35806-35825) until 0.5 s (:35532-35567): hideProp L; the camera's rustyRamp (:35848) left out; Yield 0.2 (:35873): the rustyDecay status on the target (:35523), whose apply (CharacterControl.cs:37142-37200) detonates the target's rust: Effects/rustyDecay created by the target at its collider.bounds.center, identity (:37172; the target 0.6 m up; plays its own Sounds/venomShock), when it has rust with more than 1 s left: drawn (open question 5); Yield 0.3 (:35880): standby at 0.5 s (:35595)",
    "cues": [
    [0, "voice", "rustyDecay1|rustyDecay2"],
    [0, "fx", "rustyDecay_ring"],
    [0, "hideProp", "L", {"kill": 0.5}],
    [0.2, "fx", "rustyDecay", {"d": 10, "y": 0.6}]
    ]
  },
  "backStep": {
    "why": "Chameleon.cs RPC_perfectBlend (:20438-20960), the only code that plays backStep, max rank 2 + Erase Senses #412 (passives on): at 0: clip backStep cut (PlayAnimation(backStep, 0) :20789), voice perfectBlend1 / perfectBlend2 (Random.Range(0, 2) :20830, :20840, :20871); Yield 0.1 (:20907): moveSpeed -8 (the hop back, 1.6 m by 0.3 s: no hero mover on the page, plans/fx_penguin/decisions.md 8, so both effects at the hero) and perfectBlend_ring at the hero's position and rotation (createEffect :20607; EffectControl life 1); Yield 0.2 (:20911): moveSpeed 0, blend at the hero + 1.2 m up with its rotation (createEffect :20667; plays its own Sounds/blend) and the blend status sLv 2 for chaAdjust(2 x 2 + 4) = 8 s (:20687), whose look for the hero's own team (CharacterControl.cs:36665-36929): every Diffuse renderer's material becomes new Material(FX/Blend) with its mainTexture, every other renderer off: the hero-skin cue FX/Blend (a part to build), 8 s; Yield 0.2 (:20918): standby at 0.5 s (:20719)",
    "cues": [
    [0, "voice", "perfectBlend1|perfectBlend2"],
    [0.1, "fx", "perfectBlend_ring"],
    [0.3, "fx", "blend", {"y": 1.2}],
    [0.3, "skin", "FX/Blend", {"kill": 8}]
    ]
  },
  "needlePrison": {
    "why": "Chameleon.cs RPC_needlePrison (:21406-22195), max rank 2 + Mass House Lock #422 (passives on), enemy target: the 10 m target point: at 0: clip needlePrison cut (PlayAnimation(needlePrison, 0) :21915), voice needlePrison1 / needlePrison2 (Random.Range(0, 2) :21956, :21968, :21999; needlePrison3 is never played), #422: massLock_ring at the hero's position and rotation (createEffect :22061; EffectControl life 1, followPosition; its rays have a 0.8 s delay); Yield 0.3 (:22103): Sounds/cAttack_bow (:21570-21582); Yield 0.5 (:22094): at 0.8 s the prefab field nAttack_bowFx1 = Sounds/bow_fire1 (:21619-21625; the Chameleon MonoBehaviour's 4th field, checks/fx_chameleon_research/skills_a/probe_fields.txt), the arrow in hand (slot L) hidden (:21631-21658) until 1.0 s (:21764-21799): hideProp L, and the needlePrison status on the target (with #422 every enemy within 6 m of it) for getDebuff(1 + 2) + 2 = 5 s at equal CHA (:21694-21750; Damage.cs:317-319), whose look (CharacterControl.cs:36622-36656): Effects/needlePrison at the target's position, identity, parented to it (plays its own Sounds/needlePrison), Chameleon_needlePrison.Init(Clamp(2 x radius, 0.5, 2)) = 0.6 for a 0.3 m target: 16 needlePrison_arrow (its field mPrisonArrow) one every 0.05 s at position + rotateH(0.6 x forward, i x 67.5 deg), LookRotation(up), parented (Chameleon_needlePrison.cs:144-213): a part to build (its layout mPrisonArrow r); the prison goes with the status: kill 5; Yield 0.2 (:22101): standby at 1.0 s (:21827)",
    "builds": ["needlePrison_arrow"],
    "cues": [
    [0, "voice", "needlePrison1|needlePrison2"],
    [0, "fx", "massLock_ring"],
    [0.3, "sound", "cAttack_bow"],
    [0.8, "sound", "bow_fire1"],
    [0.8, "hideProp", "L", {"kill": 0.2}],
    [0.8, "fx", "needlePrison", {"d": 10, "radius": 0.6, "kill": 5}]
    ]
  },
  "massShot": {
    "why": "Chameleon.cs RPC_massShot (:22195-23037), max rank 2 + Mass House Lock #422 (passives on): at 0: clip massShot cut (PlayAnimation(massShot, 0) :22771), voice massShot1 / massShot2 (Random.Range(0, 2) :22812, :22824, :22855); the camera's AutoZoom (:22907) left out; Yield 0.2 (:22927): moveSpeed -2 (the hop back; no hero mover on the page) and, #422 on, massHouseShot at the hero's position and rotation (createEffect :22371; else massShot :22408; EffectControl life 1; its arrow rain has a 0.4-0.6 s delay; plays its own Sounds/massHouseShot); Yield 0.6 (:22933): at 0.8 s the arrow in hand (slot L) hidden (:22446-22473) until 1.4 s (:22638-22673): hideProp L, and the hits on every enemy in FindAreaTarget(hero, 6 + 3 = 9 m) (:22508; Damage.cs:963-1120 measures to the target's edge): the 10 m target point is out of reach, so no nAttack_hit (as the Penguin's Mana Arc); Yield 0.4 (:22929): moveSpeed 0 at 1.2 s; Yield 0.2 (:22937): standby at 1.4 s (:22701)",
    "cues": [
    [0, "voice", "massShot1|massShot2"],
    [0.2, "fx", "massHouseShot"],
    [0.8, "hideProp", "L", {"kill": 0.6}]
    ]
  },
  "cast4": {
    "why": "Chameleon.cs RPC_fatalStrike (:26159-26607), the only code that plays cast4, max rank 4 + Extra Arrows #403 (status level 5, 10 arrows): at 0: clip cast4 cut (Rewind + PlayAnimation(cast4, 0) :26409-26412), voice fatalStrike1 / fatalStrike2 (Random.Range(0, 2) :26453, :26465, :26496) and fatalStrike_ring at the hero's position and rotation (createEffect :26537; EffectControl life 1, followPosition; plays its own Sounds/aura1); Yield 0.3 (:26569): the fatalStrike status for chaAdjust(12) = 12 s (:26313), whose look for the hero's own team (CharacterControl.cs:37038-37131): Effects/fatalStrike Instantiated at mount_Hand_L and at mount_Hand_R and parented to each (no EffectControl: they go with the status, or when its 10 arrows are spent, :8494-8530), cut at 10 s; Yield 0.2 (:26567): standby at 0.5 s (:26339)",
    "cues": [
    [0, "voice", "fatalStrike1|fatalStrike2"],
    [0, "fx", "fatalStrike_ring"],
    [0.3, "fx", "fatalStrike", {"bone": "mount_Hand_L", "kill": 10}],
    [0.3, "fx", "fatalStrike", {"bone": "mount_Hand_R", "kill": 10}]
    ]
  },
  "leftStride": {
    "why": "Chameleon.cs RPC_leftStride (:26607-27821), max rank 2 (2 x 2 + 1 = 5 arrows, :27058) + Double Strider #423 + Bow Mastery (40 m/s arrows, Chameleon_nAttack.cs:94-100; passives on), enemy target: the 10 m target point: at 0 (IL_89C): clip leftStride (0.2 fade, :27106), the hero runs left at runSpeed + 1 facing the target (strideLeft :27546-27605; no hero mover on the page); #423: the old clone destroyed and doubleStrider_left (the clone: a skinned Chameleon with its own 2.7 s root clip; EffectControl life 3, followState) at the hero's position and rotation (createEffect :27173), which doubleStrideLeft moves the other way: every FixedUpdate LookAt(flat target) and Translate((runSpeed + 1) x right x dt, World) while myCommand is leftStride (:27725-27795; runSpeed 4.02 at the page's stats, CharacterDataClass.cs:979: 5.02 m/s, a part to build, shared with Right Stride's doubleStrider_right: to = the target, strafe = + m/s to its right); voice leftStride1 / leftStride2 (Random.Range(0, 2) :27243, :27255, :27286); strideShot_dust at the hero (createEffect :27329; EffectControl life 2, followState; plays its own looping Sounds/rightStride_footStep); Yield 0.366 (:27371), then 0.433 between arrows (:27369): at 0.366, 0.799, 1.232, 1.665, 2.098 s: the arrow in hand (slot L) hidden at the first (:26765-26792) until 2.298 s (:26823-26851): hideProp L, the prefab field nAttack_bowFx1 = Sounds/bow_fire1 (:26931-26937), RPC_nAttack_fire from hero + TransformDirection(-0.38, 1.2, 1) at the target's collider centre (:26949-26971; the target 0.6 m up, plans/fx_penguin/decisions.md 3) and, #423, a second one from the clone + its TransformDirection(0.4, 1.2, 1) (:27004-27032; the clone's spots from checks/fx_chameleon_research/skills_a/stride_sim.py): the nAttack arrow (ProjectileControl, Chameleon_nAttack: the Normal Attack's arrow part, :8447-8545), each meeting the target's 0.3 m radius about 0.22 s later: nAttack_hit there with the hero's rotation (Chameleon_nAttack.cs:436, RPC_nAttack_hit :8565-8597; plays its own Sounds/bow_hit1; Critical Plus 4's crit on each landed arrow, its own draw: lckAdjust(4 x 4 + 4) = 20 % (Chameleon_nAttack.cs:620-643), criticalPlus_hit at the same spot and frame with the hero's rotation (:669; Chameleon.cs:9325-9364; plays its own Sounds/bow_hit3; plans/fx_chameleon/effect_only.md 'Critical Plus'); the Poison Arrow roll's poison draws nothing (CharacterControl.cs:36965-36969)); after the 5th, Yield 0.2 (:27365): the arrow back and standby at 2.298 s (:26862-26889): the clone's and the dust's followState cut (cued 2.3)",
    "cues": [
    [0, "voice", "leftStride1|leftStride2"],
    [0, "fx", "strideShot_dust", {"cut": 2.3}],
    [0, "fx", "doubleStrider_left", {"to": [0, 0, 10], "strafe": 5.02, "cut": 2.3}],
    [0.366, "sound", "bow_fire1"],
    [0.366, "fx", "nAttack", {"x": -0.38, "y": 1.2, "d": 1, "rot": [3.81, 2.42, 0], "to": [0, 0.6, 10]}],
    [0.366, "fx", "nAttack", {"x": 2.1, "y": 1.2, "d": 1.23, "rot": [3.81, -13.47, 0], "to": [0, 0.6, 10]}],
    [0.366, "hideProp", "L", {"kill": 1.932}],
    [0.586, "fx", "nAttack_hit", {"x": -0.01, "y": 0.62, "d": 9.7}],
    [0.586, "fx", "nAttack_hit", {"x": 0.07, "y": 0.62, "d": 9.71}],
    [0.586, "fx", "criticalPlus_hit", {"x": -0.01, "y": 0.62, "d": 9.7, "p": 0.2}],
    [0.586, "fx", "criticalPlus_hit", {"x": 0.07, "y": 0.62, "d": 9.71, "p": 0.2}],
    [0.799, "sound", "bow_fire1"],
    [0.799, "fx", "nAttack", {"x": -0.38, "y": 1.2, "d": 1, "rot": [3.81, 2.42, 0], "to": [0, 0.6, 10]}],
    [0.799, "fx", "nAttack", {"x": 3.89, "y": 1.2, "d": 1.85, "rot": [3.8, -25.53, 0], "to": [0, 0.6, 10]}],
    [1.019, "fx", "nAttack_hit", {"x": -0.01, "y": 0.62, "d": 9.7}],
    [1.019, "fx", "nAttack_hit", {"x": 0.13, "y": 0.62, "d": 9.73}],
    [1.019, "fx", "criticalPlus_hit", {"x": -0.01, "y": 0.62, "d": 9.7, "p": 0.2}],
    [1.019, "fx", "criticalPlus_hit", {"x": 0.13, "y": 0.62, "d": 9.73, "p": 0.2}],
    [1.232, "sound", "bow_fire1"],
    [1.232, "fx", "nAttack", {"x": -0.38, "y": 1.2, "d": 1, "rot": [3.81, 2.42, 0], "to": [0, 0.6, 10]}],
    [1.232, "fx", "nAttack", {"x": 5.58, "y": 1.2, "d": 2.89, "rot": [3.8, -38.15, 0], "to": [0, 0.6, 10]}],
    [1.452, "fx", "nAttack_hit", {"x": -0.01, "y": 0.62, "d": 9.7}],
    [1.452, "fx", "nAttack_hit", {"x": 0.18, "y": 0.62, "d": 9.76}],
    [1.452, "fx", "criticalPlus_hit", {"x": -0.01, "y": 0.62, "d": 9.7, "p": 0.2}],
    [1.452, "fx", "criticalPlus_hit", {"x": 0.18, "y": 0.62, "d": 9.76, "p": 0.2}],
    [1.665, "sound", "bow_fire1"],
    [1.665, "fx", "nAttack", {"x": -0.38, "y": 1.2, "d": 1, "rot": [3.81, 2.42, 0], "to": [0, 0.6, 10]}],
    [1.665, "fx", "nAttack", {"x": 7.01, "y": 1.2, "d": 4.27, "rot": [3.79, -50.75, 0], "to": [0, 0.6, 10]}],
    [1.885, "fx", "nAttack_hit", {"x": -0.01, "y": 0.62, "d": 9.7}],
    [1.885, "fx", "nAttack_hit", {"x": 0.23, "y": 0.62, "d": 9.81}],
    [1.885, "fx", "criticalPlus_hit", {"x": -0.01, "y": 0.62, "d": 9.7, "p": 0.2}],
    [1.885, "fx", "criticalPlus_hit", {"x": 0.23, "y": 0.62, "d": 9.81, "p": 0.2}],
    [2.098, "sound", "bow_fire1"],
    [2.098, "fx", "nAttack", {"x": -0.38, "y": 1.2, "d": 1, "rot": [3.81, 2.42, 0], "to": [0, 0.6, 10]}],
    [2.098, "fx", "nAttack", {"x": 8.06, "y": 1.2, "d": 5.85, "rot": [3.79, -62.77, 0], "to": [0, 0.6, 10]}],
    [2.318, "fx", "nAttack_hit", {"x": -0.01, "y": 0.62, "d": 9.7}],
    [2.318, "fx", "nAttack_hit", {"x": 0.27, "y": 0.62, "d": 9.86}],
    [2.318, "fx", "criticalPlus_hit", {"x": -0.01, "y": 0.62, "d": 9.7, "p": 0.2}],
    [2.318, "fx", "criticalPlus_hit", {"x": 0.27, "y": 0.62, "d": 9.86, "p": 0.2}]
    ]
  },
  "allSlayer1": {
    "why": "Chameleon.cs RPC_allSlayer (:32144-32805), the four All Slayer skills' shared opening (sLv 1-4 = All Bug / Tail / Elemental / Machine Slayer, the dispatcher :7522): no voice; at 0: clip allSlayer1 cut (PlayAnimation(allSlayer1, 0) :32440); Yield 0.5 (:32734): allSlayer_ring at the hero's position and rotation (createEffect :32309; EffectControl life 60, afterLife 0.2, followPosition, followState); Yield 0.2 (:32739): allSlayer2 cut in and looped at 0.7 s (:32346-32351, its entry), then the bar magAdjust(4 + Improved Slayer 4) (:32381-32390; the cast-bar rule: its floor 0.1 s) and RPC_allSlayer_fire when it ends (:32474, :32700) sets myCommand allSlayer2: the ring's followState cut at 0.8 s; the page restarts FX.t at the 0.7 s step edge, so it is cued 0.65 (as castRing's)",
    "cues": [
    [0.5, "fx", "allSlayer_ring", {"cut": 0.65}]
    ]
  },
  "allSlayer2": {
    "why": "Chameleon.cs RPC_allSlayer case 3 / 4 (:32327-32673): allSlayer2 looped from 0.7 s, and on its first frame (the eye timer starts at 0, :32371, :32491-32507) the marking pass: every enemy in FindAreaTarget(hero, 40, 10) (:32512) of the skill's race (sLv 1 Bugs / Plants, 2 Tails, 3 Elementals, 4 Robots, or with slayerMark) that is on screen, up to 4 + Improved Slayer 4 = 8 (:32550-32630), gets RPC_allSlayer_mark (:32645; :9568-9760): its race's eye created by the target at its collider.bounds.center, identity (the target 0.6 m up; EffectControl life 1, afterLife 0.5, followPosition; plays its own Sounds/slayerCharge); the next pass would come 2 s later, after the 0.1 s bar: one eye per play; one member per skill (its own tile, poolChains), the same member's allSlayer3 entry next",
    "skills": {
      "allBugSlayer": {"why": "allBugSlayer (sLv 1, Bugs / Plants): RPC_allSlayer_mark sLv 1 loads Effects/bugSlayer_eye (Chameleon.cs:9615) at the 10 m target 0.6 m up",
        "cues": [
        [0, "fx", "bugSlayer_eye", {"d": 10, "y": 0.6}]
        ]},
      "allTailSlayer": {"why": "allTailSlayer (sLv 2, Tails): RPC_allSlayer_mark sLv 2 loads Effects/tailSlayer_eye (Chameleon.cs:9652) at the 10 m target 0.6 m up",
        "cues": [
        [0, "fx", "tailSlayer_eye", {"d": 10, "y": 0.6}]
        ]},
      "allElementalSlayer": {"why": "allElementalSlayer (sLv 3, Elementals): RPC_allSlayer_mark sLv 3 loads Effects/elementalSlayer_eye (Chameleon.cs:9689) at the 10 m target 0.6 m up",
        "cues": [
        [0, "fx", "elementalSlayer_eye", {"d": 10, "y": 0.6}]
        ]},
      "allMachineSlayer": {"why": "allMachineSlayer (sLv 4, Robots): RPC_allSlayer_mark sLv 4 loads Effects/machineSlayer_eye (Chameleon.cs:9730) at the 10 m target 0.6 m up",
        "cues": [
        [0, "fx", "machineSlayer_eye", {"d": 10, "y": 0.6}]
        ]}
    }
  },
  "allSlayer3": {
    "why": "Chameleon.cs RPC_allSlayer_fire (:32805-34044), started when the bar ends (0.8 s), myCommand allSlayer2: at 0: clip allSlayer3 cut (PlayAnimation(allSlayer3, 0) :33546) and the race's voice: BB asks Voices/allBugSlayer1 / 2, allTailSlayer1 / 2, allElementalSlayer1 / 2, allMachineSlayer1 / 2 (Random.Range(0, 2) :33598-33876), which BB's data does not have (voices/ holds allBugSlayer, allTailSlayer, allElementalSlayer, allMachineSlayer, one each; All Bug Slayer's first branch also loads into Blood Burn's field and plays a never-set one, :33604-33622), and TTO1102 loads Voices/allBugSlayer ... allMachineSlayer with no number (TTO pseudo Chameleon.c RPC_allSlayer_fire d__188): TTO's fix (plans/fx_sheep/decisions.md 10); the camera's motion blur (:33892-33895) left out; Yield 0.2 (:33944): the arrow in hand (slot L) hidden (:32952-32979) until 0.95 s (:33479-33507): hideProp L, and the race's all<Race>Slayer_fire at the hero's position and rotation (:32989-33157; EffectControl life 1, followPosition; plays its own Sounds/slayerFire); Yield 0.1 (:33928): at 0.3 s the hits on the marked targets (FindAreaTarget(hero, 40, 10) :33216, the same race / slayerMark test, up to 8): RPC_allSlayer_hit Instantiates the race's all<Race>Slayer_hit at the target's position (its feet), identity (:33320; :9766-9930; a bolt from 12 m up; plays its own Sounds/allSlayer_hit): the 10 m target point; Yield 0.5 (:33942): standby at 0.8 s (:33439); Yield 0.15 (:33936): the arrow back at 0.95 s",
    "skills": {
      "allBugSlayer": {"why": "sLv 1: voice allBugSlayer (TTO's fix), allBugSlayer_fire (Chameleon.cs:33006, created :33018), allBugSlayer_hit (Chameleon.cs:9785)",
        "cues": [
        [0, "voice", "allBugSlayer"],
        [0.2, "fx", "allBugSlayer_fire"],
        [0.2, "hideProp", "L", {"kill": 0.75}],
        [0.3, "fx", "allBugSlayer_hit", {"d": 10}]
        ]},
      "allTailSlayer": {"why": "sLv 2: voice allTailSlayer (TTO's fix), allTailSlayer_fire (Chameleon.cs:33047, created :33059), allTailSlayer_hit (Chameleon.cs:9822)",
        "cues": [
        [0, "voice", "allTailSlayer"],
        [0.2, "fx", "allTailSlayer_fire"],
        [0.2, "hideProp", "L", {"kill": 0.75}],
        [0.3, "fx", "allTailSlayer_hit", {"d": 10}]
        ]},
      "allElementalSlayer": {"why": "sLv 3: voice allElementalSlayer (TTO's fix), allElementalSlayer_fire (Chameleon.cs:33088, created :33100), allElementalSlayer_hit (Chameleon.cs:9859)",
        "cues": [
        [0, "voice", "allElementalSlayer"],
        [0.2, "fx", "allElementalSlayer_fire"],
        [0.2, "hideProp", "L", {"kill": 0.75}],
        [0.3, "fx", "allElementalSlayer_hit", {"d": 10}]
        ]},
      "allMachineSlayer": {"why": "sLv 4: voice allMachineSlayer (TTO's fix), allMachineSlayer_fire (Chameleon.cs:33133, created :33145), allMachineSlayer_hit (Chameleon.cs:9900)",
        "cues": [
        [0, "voice", "allMachineSlayer"],
        [0.2, "fx", "allMachineSlayer_fire"],
        [0.2, "hideProp", "L", {"kill": 0.75}],
        [0.3, "fx", "allMachineSlayer_hit", {"d": 10}]
        ]}
    }
  },
  "allSlain": {
    "why": "Chameleon.cs RPC_allSlain (:34044-34709), max rank 2: at 0: clip allSlain cut (PlayAnimation(allSlain, 0) :34489), voice allSlain1 / allSlain2 (Random.Range(0, 2) :34530, :34542, :34573; allSlain3 is never played) and allSlain_ring at the hero's position and rotation (createEffect :34614; EffectControl life 2, afterLife 0.2, followPosition; plays its own Sounds/allSlain_ring); Yield 0.7 (:34655): at 0.7 s RPC_allSlain_hit for every target in the All Slain list (the targets the Chameleon's attacks hit since the last cast, addAllSlainList :9983-10060; Bible chameleon-skill-reference.md:483): allSlain_hit Instantiated at the target's position (its feet), identity (:34227; :9940-9975; a bolt from 12 m up; plays its own Sounds/allSlain_hit): the 10 m target point (the page's target stands for a listed one, open question 5); the camera's motion blur (:34270-34275) and, Yield 0.1 (:34659), shake at 0.8 s (:34310) left out; Yield 0.2 (:34644): the damage at 1.0 s (:34377, nothing drawn); Yield 0.5 (:34651): standby at 1.5 s (:34419)",
    "cues": [
    [0, "voice", "allSlain1|allSlain2"],
    [0, "fx", "allSlain_ring"],
    [0.7, "fx", "allSlain_hit", {"d": 10}]
    ]
  }
}
```

## Verification

Checker `verify_a`, 2026-11-13 (home PC), read only. Each coroutine in scope re-read with the opaque predicates worked
out (`checks\fx_chameleon_research\verify_a\flow.sh <from> <to>`): RPC_cast1, the five `_cast` members, RPC_tent_cast,
RPC_immunity, RPC_venomShock, RPC_bloodBurn, RPC_rustyDecay, RPC_perfectBlend, RPC_needlePrison, RPC_massShot,
RPC_fatalStrike, RPC_leftStride (+ strideLeft / doubleStrideLeft), RPC_allSlayer, RPC_allSlayer_fire, RPC_allSlain, and the
status looks (CharacterControl.cs:36591-37200, :32493-32684, Block_989 :42213). The clip callers listed again
(`verify_a\playcalls.txt`): cast3 has exactly the 10 callers named here (5 pool members, Tent, the 4 channel-less skills),
cast4 / backStep / needlePrison / massShot / leftStride / allSlain / allSlayer1-3 one caller each, cast2 only RPC_cast1 and
RPC_activateIcon1, focusFire1 / 2 none. BB vs TTO1102 strings per coroutine (`verify_a\tto_strings.py`): the only
differences in scope are the two voice fixes (True Invisibility, All Slayer), as Read this first 3 says. The paste block
parses (17 keys).

Checked and right: every time, voice pair, rank, duration and spot in the tables and the paste block except the items
below; in particular castRing at 0 with Euler(270, 90, 0) and its 0.35 cut; the invisible look 0.2 s after the status
(Block_989); chaAdjust at CHA 1 (8, 12, 16, 30, 7); Immunity at y 1.16, scale 0.7 (CharacterController centre 0.98,
height 1.8, radius 0.3, Chameleon.prefab:903-910; `mChar` in the status coroutine is the CharacterController,
CharacterControl.cs:29789); needlePrison's 16 arrows (Chameleon_needlePrison.cs:172-197) and its 5 s (Damage.cs:317-319,
getDebuff(3) + 2); the cage's life 7 (:9172); Mass Shot's 9 m edge test (Damage.cs:1094-1124); Fatal Strike's two hand
copies (CharacterControl.cs:37088-37113: spawned with world identity, then parented, which the `bone` option's local
identity does not copy, but the prefab is a 0.1 m sphere emitter with no velocity or force, probe.json, so it looks the
same); All Slayer's single marking pass on allSlayer2's first frame (eye timer 0, :32371, :32491-32507) and the fire 0.1 s
later (:32474); `EffectControl.followState` ends on an actionState or myCommand change (EffectControl.cs:226-232), so
the ring cuts are right; the clone moves +right at runSpeed + 1 after its LookAt (:27769-27775), the hero -right
(:27589); the pool / poolChains wiring (index.html:1329-1350: both All Slayer pools share the four tiles, FX.pick kept,
:4799); the icon names resolve through the page's UI.skills fallback (the HD index has none of them).

Corrections:

1. **Tent's sleep fade: the page has `~0.5`** (skills_a.md:44-45, :504). The SEQ token takes a fade length after `~`
   (index.html:1278, SEQ_ALT :1285, :1290: "~0.3" = a 0.3 s crossfade), so the game's `PlayAnimation("sleep", 0.5f)`
   (:36063) can be written exactly: **`"Tent: cast1 cast2*@0 cast3~@0.4 sleep*~0.5@0.7"`**. The `@Tent:sleep` cues stand
   (FX.t counts from the step start either way).
2. **Left Stride's hits come about 0.045 s earlier, at the arrow's trigger-box contact** (skills_a.md:258, :261-266, :365,
   :583, :592-623; `stride_sim.py` takes the arrow's origin reaching a 0.3 m sphere). The game hits in
   `Chameleon_nAttack.OnTriggerEnter` when the arrow's BoxCollider (0.3 x 0.3 x 1.5 centred 1 m ahead: front 1.75 m ahead of
   the origin, nAttack.prefab:34-44) touches the target's CharacterController; it destroys the arrow there (:379-397) and
   puts the hit at `target.ClosestPointOnBounds(arrow box centre)` (:406). On the standard target body (capsule centred
   0.6 m up, radius 0.3, height 1: Bat decision 4, "contact tests and ClosestPointOnBounds") `verify_a\box_hit2.py` gives:
   - the hero's arrows: hit **shot + 0.174 s** (0.54, 0.973, 1.406, 1.839, 2.272) at **x -0.04, y 0.67, d 9.7**;
   - the clone's: **0.541, 0.974, 1.407, 1.84, 2.274**, at **x 0.24, y 0.67, d 9.7** (the first) and **x 0.3, y 0.67, d 9.7**
     (the other four: the side shots land on the bounds' corner).

   (An AABB contact test, `verify_a\box_hit.py`, gives the same within 3 ms.) The `nAttack` cues (spots, rot, to) stand.
   For P1 (attacks_emotes part P1) this means: an arrow cued with `to` ends when its box front (1.75 m ahead of its
   origin) reaches the target body, about 2 m before the origin would; the `nAttack_hit` / `criticalPlus_hit` cues come at
   that same moment.

Additions (no cue change):
- Part 1 (FX/Invisible, skills_a.md:334-341), the numbers from `checks\fx_chameleon_research\parts\shaders.txt:282-298`:
  pass 2 pushes the vertex `xy += (n.x P[0][0], n.y P[1][1]) x clip z x 0.003` and writes colour **(0.3, 0.6, 1, 0.75)**
  (a blue rim; FX/Blend's is 0.002 and (0.8, 0.8, 0.3, 0.5)); pass 1 is FX/Blend's (the texture at alpha 0.35).
- Focus Fire (Read this first 9, finding 6): BB's rip also has its skill icons, `gamegui/icons/skills/chameleon/
  focusFire0-4.png` (the page's `data/icons/skills/chameleon/focusfire0-4.webp`), still with no code, locale or Bible card:
  a cut skill, animations and icons left in the data. The recommendation (no cues, plain move) stands.
- Unused voice files (finding 7): also `allSlayer.wav` (no BB or TTO code loads `Voices/allSlayer`; RPC_allSlayer loads
  only allSlayer_ring).

Corrected paste-ready blocks (only these changed; every other entry above stands as written).

SEQ `chameleon` (index.html), the Tent line in place of Read this first 2's:

```
"Tent: cast1 cast2*@0 cast3~@0.4 sleep*~0.5@0.7"
```

```json
  "@Tent:sleep": {
    "why": "Chameleon.cs RPC_tent_cast case 2 at 0.4 s (:36063-36096): PlayAnimation(sleep, 0.5f) looped (the SEQ's sleep*~0.5) and tent_ring at the hero's position and rotation (createEffect :36091; the tent model tent_tri, stars, smoke; EffectControl life 99, followPosition, followState; plays its own Sounds/tent); Yield 0.5 (:36526): case 3 at 0.9 s: the channel castTime = magAdjust(12) with a cast bar (:36128-36151; the cast-bar rule, high INT: its floor 0.1 s) and the tent status (:36139: moveSpeed 0, a zzz emote every 3 s, CharacterControl.cs:9274-9289, left out); the channel's end test actionTime + castTime + 0.5 (:36280, actionTime from cast3's start) has passed, so at 0.9 s (sleep 0.5 s): tent_heal at the hero (:36306; plays its own Sounds/tent_heal), the full heal and the cooldown reset (:36326-36337, nothing drawn); Yield 0.2 (:36533): standby at 1.1 s (sleep 0.7 s, :36228): tent_ring's followState cut there. tent_destroy (:36181) comes only when the channel is broken: not cued",
    "cues": [
    [0, "fx", "tent_ring", {"cut": 0.7}],
    [0.5, "fx", "tent_heal"]
    ]
  },
  "leftStride": {
    "why": "Chameleon.cs RPC_leftStride (:26607-27821), max rank 2 (2 x 2 + 1 = 5 arrows, :27058) + Double Strider #423 + Bow Mastery (40 m/s arrows, Chameleon_nAttack.cs:94-100; passives on), enemy target: the 10 m target point: at 0 (IL_89C): clip leftStride (0.2 fade, :27106), the hero runs left at runSpeed + 1 facing the target (strideLeft :27546-27605, vMovement -right :27589; no hero mover on the page); #423: the old clone destroyed and doubleStrider_left (the clone: a skinned Chameleon with its own 2.7 s root clip; EffectControl life 3, followState) at the hero's position and rotation (createEffect :27173), which doubleStrideLeft moves the other way: every FixedUpdate LookAt(flat target) and Translate((runSpeed + 1) x right x dt, World) while myCommand is leftStride (:27725-27795; runSpeed 4.02 at the page's stats, CharacterDataClass.cs:979: 5.02 m/s, a part to build, shared with Right Stride's doubleStrider_right: to = the target, strafe = + m/s to its right); voice leftStride1 / leftStride2 (Random.Range(0, 2) :27243, :27255, :27286); strideShot_dust at the hero (createEffect :27329; EffectControl life 2, followState; plays its own looping Sounds/rightStride_footStep); Yield 0.366 (:27371), then 0.433 between arrows (:27369): at 0.366, 0.799, 1.232, 1.665, 2.098 s: the arrow in hand (slot L) hidden at the first (:26765-26792) until 2.298 s (:26823-26851): hideProp L, the prefab field nAttack_bowFx1 = Sounds/bow_fire1 (:26931-26937), RPC_nAttack_fire from hero + TransformDirection(-0.38, 1.2, 1) at the target's collider centre (:26949-26971; the target 0.6 m up, plans/fx_penguin/decisions.md 3) and, #423, a second one from the clone + its TransformDirection(0.4, 1.2, 1) (:27004-27032; the clone's spots from checks/fx_chameleon_research/skills_a/stride_sim.py): the nAttack arrow (ProjectileControl, Chameleon_nAttack: the Normal Attack's arrow part, :8447-8545); each arrow hits when its trigger box (0.3 x 0.3 x 1.5 centred 1 m ahead, nAttack.prefab:34-44) touches the target body (capsule radius 0.3 centred 0.6 m up, plans/fx_bat/decisions.md 4) and is destroyed there (Chameleon_nAttack.cs:379-397): the hero's 0.174 s after the shot, the clone's 0.175-0.176 s (checks/fx_chameleon_research/verify_a/box_hit2.py); nAttack_hit at target.ClosestPointOnBounds(the box centre) (Chameleon_nAttack.cs:406, :436; RPC_nAttack_hit :8565-8597) with the hero's rotation (plays its own Sounds/bow_hit1); Critical Plus 4's crit on each landed arrow, its own draw: lckAdjust(4 x 4 + 4) = 20 % (Chameleon_nAttack.cs:620-643), criticalPlus_hit at the same spot and frame with the hero's rotation (:669; Chameleon.cs:9325-9364; plays its own Sounds/bow_hit3; plans/fx_chameleon/effect_only.md 'Critical Plus'); the Poison Arrow roll's poison draws nothing (CharacterControl.cs:36965-36969); after the 5th, Yield 0.2 (:27365): the arrow back and standby at 2.298 s (:26862-26889): the clone's and the dust's followState cut (cued 2.3)",
    "cues": [
    [0, "voice", "leftStride1|leftStride2"],
    [0, "fx", "strideShot_dust", {"cut": 2.3}],
    [0, "fx", "doubleStrider_left", {"to": [0, 0, 10], "strafe": 5.02, "cut": 2.3}],
    [0.366, "sound", "bow_fire1"],
    [0.366, "fx", "nAttack", {"x": -0.38, "y": 1.2, "d": 1, "rot": [3.81, 2.42, 0], "to": [0, 0.6, 10]}],
    [0.366, "fx", "nAttack", {"x": 2.1, "y": 1.2, "d": 1.23, "rot": [3.81, -13.47, 0], "to": [0, 0.6, 10]}],
    [0.366, "hideProp", "L", {"kill": 1.932}],
    [0.54, "fx", "nAttack_hit", {"x": -0.04, "y": 0.67, "d": 9.7}],
    [0.54, "fx", "criticalPlus_hit", {"x": -0.04, "y": 0.67, "d": 9.7, "p": 0.2}],
    [0.541, "fx", "nAttack_hit", {"x": 0.24, "y": 0.67, "d": 9.7}],
    [0.541, "fx", "criticalPlus_hit", {"x": 0.24, "y": 0.67, "d": 9.7, "p": 0.2}],
    [0.799, "sound", "bow_fire1"],
    [0.799, "fx", "nAttack", {"x": -0.38, "y": 1.2, "d": 1, "rot": [3.81, 2.42, 0], "to": [0, 0.6, 10]}],
    [0.799, "fx", "nAttack", {"x": 3.89, "y": 1.2, "d": 1.85, "rot": [3.8, -25.53, 0], "to": [0, 0.6, 10]}],
    [0.973, "fx", "nAttack_hit", {"x": -0.04, "y": 0.67, "d": 9.7}],
    [0.973, "fx", "criticalPlus_hit", {"x": -0.04, "y": 0.67, "d": 9.7, "p": 0.2}],
    [0.974, "fx", "nAttack_hit", {"x": 0.3, "y": 0.67, "d": 9.7}],
    [0.974, "fx", "criticalPlus_hit", {"x": 0.3, "y": 0.67, "d": 9.7, "p": 0.2}],
    [1.232, "sound", "bow_fire1"],
    [1.232, "fx", "nAttack", {"x": -0.38, "y": 1.2, "d": 1, "rot": [3.81, 2.42, 0], "to": [0, 0.6, 10]}],
    [1.232, "fx", "nAttack", {"x": 5.58, "y": 1.2, "d": 2.89, "rot": [3.8, -38.15, 0], "to": [0, 0.6, 10]}],
    [1.406, "fx", "nAttack_hit", {"x": -0.04, "y": 0.67, "d": 9.7}],
    [1.406, "fx", "criticalPlus_hit", {"x": -0.04, "y": 0.67, "d": 9.7, "p": 0.2}],
    [1.407, "fx", "nAttack_hit", {"x": 0.3, "y": 0.67, "d": 9.7}],
    [1.407, "fx", "criticalPlus_hit", {"x": 0.3, "y": 0.67, "d": 9.7, "p": 0.2}],
    [1.665, "sound", "bow_fire1"],
    [1.665, "fx", "nAttack", {"x": -0.38, "y": 1.2, "d": 1, "rot": [3.81, 2.42, 0], "to": [0, 0.6, 10]}],
    [1.665, "fx", "nAttack", {"x": 7.01, "y": 1.2, "d": 4.27, "rot": [3.79, -50.75, 0], "to": [0, 0.6, 10]}],
    [1.839, "fx", "nAttack_hit", {"x": -0.04, "y": 0.67, "d": 9.7}],
    [1.839, "fx", "criticalPlus_hit", {"x": -0.04, "y": 0.67, "d": 9.7, "p": 0.2}],
    [1.84, "fx", "nAttack_hit", {"x": 0.3, "y": 0.67, "d": 9.7}],
    [1.84, "fx", "criticalPlus_hit", {"x": 0.3, "y": 0.67, "d": 9.7, "p": 0.2}],
    [2.098, "sound", "bow_fire1"],
    [2.098, "fx", "nAttack", {"x": -0.38, "y": 1.2, "d": 1, "rot": [3.81, 2.42, 0], "to": [0, 0.6, 10]}],
    [2.098, "fx", "nAttack", {"x": 8.06, "y": 1.2, "d": 5.85, "rot": [3.79, -62.77, 0], "to": [0, 0.6, 10]}],
    [2.272, "fx", "nAttack_hit", {"x": -0.04, "y": 0.67, "d": 9.7}],
    [2.272, "fx", "criticalPlus_hit", {"x": -0.04, "y": 0.67, "d": 9.7, "p": 0.2}],
    [2.274, "fx", "nAttack_hit", {"x": 0.3, "y": 0.67, "d": 9.7}],
    [2.274, "fx", "criticalPlus_hit", {"x": 0.3, "y": 0.67, "d": 9.7, "p": 0.2}]
    ]
  },
```
