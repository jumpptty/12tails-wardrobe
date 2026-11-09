# Wolf effects research: the shared clips cast1, cast2, cast3, instantCast

Researcher's report for the Wolf cue file (`wardrobe/fx_cues/wolf.json`). Read-only; sources: `D:\12tails\DecompiledSource\Wolf.cs`
(BB), `CharacterControl.cs`, the TTO pseudo-C (`DecompiledSource_TTO_2026-11-02/pseudo/Wolf.c`), the rip's prefabs, and
a read-only probe of BB's own effect data (`checks/fx_wolf_research/cast/probe.py`, which imports `wardrobe_fx.effect()`
and prints EffectControl settings without writing anything). Max rank everywhere.

## 1. Which skills play the shared clips

### cast1 / cast2 / cast3 (the wardrobe's "Cast" tile): no Wolf skill plays them

- `clip_calls.js ... wolf` ends with `(no call found: bladeSurge cast1 cast2 cast3 resonanceClaw windBoundDomain)`.
- In `Wolf.cs` the three names appear only in `PlayAnimation`'s loader (`:1255-1290`, it loads the clip assets).
  There is no `RPC_cast1` / `RPC_cast` in `Wolf.cs` (the classes that have one: Bat, Chameleon, Penguin, Rabbit, Sheep,
  Whale and their Shadow AIs), no `PlayAnimation` with a non-literal name (the only hit, `:1007`, is the method itself),
  and no other file plays the Wolf's cast clips (the `"cast1"` hits in `M100_GameTutorial1.cs`, `M502...`, `Walrus.cs`
  are the Walrus NPC).
- TTO's client is the same: the only cast-family string in `pseudo/Wolf.c` is `'instantCast'` (four uses, below).
- Things in the Wolf's folders that look related but aren't: `Voices/cast` is the mount summon's voice
  (`RPC_useMount`, `Wolf.cs:43695`; that coroutine plays the `battle` loop for its 6 s cast, `:43648`, not cast1-3);
  `Effects/castFX` and `Effects/cast_ring` are loaded by no Wolf code (no `Resources.Load` of either in `Wolf.cs` or
  `CharacterControl.cs`).
- So the Wolf's "Cast: cast1 cast2*@0 cast3" in `SEQ` (`wardrobe/index.html:984`) is the page's analogy with the
  casters (its comment says SEQ = sequences "the BB code plays"); BB never plays it for the Wolf. **No cues for
  cast1 / cast2 / cast3**: there is no skill to pick at random for this tile. Whether to keep the tile at all is a page
  question for the user (open question 1).

### instantCast: four skills, all at max rank in one build

| Skill | Coroutine | Clip call | Skill data |
|---|---|---|---|
| Brave Spirit 4 (+ Glorious Spirit #402) | `$RPC_braveSpirit$29356`, `Wolf.cs:20200-20890` | `PlayAnimation("instantCast", 0.2f)` `:20597` | Paladin r1, Lv 21; instant, self + allies in 15 m |
| Second Wind | `$RPC_secondWind$29420`, `Wolf.cs:23080-23580` | `:23381` | Paladin r6c4, Lv 32 |
| Lunar Eclipse 2 | `$RPC_lunarEclipse$29600`, `Wolf.cs:31084-31550` | `:31341` | Blade Master r8, Lv 40 |
| Holy Sword | `$RPC_holySword$29639`, `Wolf.cs:32775-33285` | `:33083` | Class C r4, Lv 75 |

Each is one clip (wrapMode Once, 0.2 s crossfade, the hero stopped, `moveSpeed = 0`); no second RPC. Holy Armor, the
Holy Sword's twin, plays `darkEdge` (`:33598`), not instantCast. TTO uses the same assets and waits (its four
coroutines `Wolf.<RPC_braveSpirit>d__194`, `<RPC_secondWind>d__201`, `<RPC_lunarEclipse>d__224`,
`<RPC_holySword>d__230` load the same Effects / Voices / Sounds paths and carry the same 0.5 / 0.2 / 0.6 / 0.7 constants).

## 2. Per skill: timeline, proposed cues

Times are seconds after instantCast starts (the coroutine's `PlayAnimation`). The clip is 1.5 s long
(`data/wolf/clips.json`); each skill hands back to standby before it ends (1.1-1.3 s).

### Brave Spirit (rank 4, with Glorious Spirit learned: see the rule in section 3)

Flow: clip, voice, sound at 0 (`:20597-20795`); wait 0.5 (`:20833`) -> case 2: the effect 0.2 m ahead
(`createEffect(..., position + 0.2f * forward, rotation)`, `:20369` / `:20406`); wait 0.2 (`:20831`) -> case 3 (0.7 s):
`valor` on every ally in the cylinder, the Wolf included (`:20456-20489`); wait 0.6 (`:20824`) -> standby at 1.3 s
(`:20515`).
- `hasSkill(402)` (Glorious Spirit) swaps the voice pair (`:20638`: gloriousSpirit1 / 2, else braveSpirit1 / 2, each
  `Random.Range(0, 2)`) and the effect (`:20345`: braveSpirit, else gloriousSpirit, `:20357` / `:20394`).
- `Sounds/braveSpirit` (`:20779-20795`) is a second PlayOneShot from the coroutine itself, always played (outside the
  pvoice check); not an effect's AudioSource, so it needs its own cue (as a "voice" cue: `wardrobe_fx.rip_wav` looks
  in `sounds/` first, so the name `braveSpirit` resolves to `sounds/braveSpirit.wav`).
- The effects have no followState (probe: braveSpirit / gloriousSpirit `life 1, afterLife 1, followPosition true,
  followState false`), so no 5th value.
- Left out: `valor_emblem`, the buff's mark, which `valor`'s apply instantiates over each receiver at
  `position + 2 * up` (`CharacterControl.cs:33969-33975`) at 0.7 s: it is an EmblemEmitter (probe: "no layout for
  EmblemEmitter (68 field bytes)") and the cue format has no upward offset. Not in `fx_inventory.md` (it lists only
  what `Wolf.cs` loads).

```json
[0, "voice", "gloriousSpirit1|gloriousSpirit2"],
[0, "voice", "braveSpirit"],
[0.5, "fx", "gloriousSpirit", 0.2]
```
Without Glorious Spirit: `[0, "voice", "braveSpirit1|braveSpirit2"], [0, "voice", "braveSpirit"], [0.5, "fx", "braveSpirit", 0.2]`.

why: `RPC_braveSpirit: clip (:20597); voice gloriousSpirit1 / 2 by Glorious Spirit #402 (:20638-20699) and the braveSpirit sound (:20779-20795) at 0; gloriousSpirit 0.2 m ahead at 0.5 s (:20833, :20394-20406); valor at 0.7 s (:20489), its valor_emblem 2 m above the hero left out: needs EmblemEmitter (CharacterControl.cs:33969); standby 1.3 s (:20824, :20515)`

### Second Wind

Flow: clip, voice secondWind1 / 2 (`Random.Range(0, 2)`, `:23422-23477`) and `Sounds/secondWind` (`:23490-23506`) at 0;
wait 0.6 (`:23548`) -> case 2: `secondWind` 0.2 m ahead (`:23221-23233`); wait 0.2 (`:23550`) -> 0.8 s: the heal
(`RPC_AddHeal`, `:23278`); wait 0.5 (`:23552`) -> standby at 1.3 s (`:23299`). Probe: `secondWind` life 1.5, afterLife 0,
followPosition true, followState false.

```json
[0, "voice", "secondWind1|secondWind2"],
[0, "voice", "secondWind"],
[0.6, "fx", "secondWind", 0.2]
```
why: `RPC_secondWind: clip (:23381); voice secondWind1 / 2 (:23422-23477) and the secondWind sound (:23490-23506) at 0; secondWind 0.2 m ahead at 0.6 s (:23548, :23221-23233); the heal at 0.8 s (:23278); standby 1.3 s (:23552, :23299)`

### Lunar Eclipse (rank 2)

Flow: clip, voice lunarEclipse1 / 2 (`:31382-31437`) and `Sounds/braveSpirit` (the same sound as Brave Spirit,
`:31450-31468`) at 0; on the player's own camera a colour ramp `AddColorRamp("lunarRamp", "centerMask", 10, ...)`
(`:31488-31491`); wait 0.7 (`:31517`) -> case 2: `RPC_AddStatus("lunarEclipse", ...)` (`:31238`); wait 0.6 (`:31510`)
-> standby at 1.3 s (`:31259`). No effect prefab at all. The status's look: `setColor(Color.black)` on the hero for its
duration (`CharacterControl.cs:34241-34248`; removal `:15143`). Rank changes only the numbers.

```json
[0, "voice", "lunarEclipse1|lunarEclipse2"],
[0, "voice", "braveSpirit"]
```
why: `RPC_lunarEclipse: clip (:31341); voice lunarEclipse1 / 2 (:31382-31437) and the braveSpirit sound (:31450-31468) at 0; no effect prefab; left out: the screen colour ramp (camera, :31488) and the status's black body tint from 0.7 s (:31517, :31238; CharacterControl.cs:34241), which no cue can express; standby 1.3 s (:31510)`

### Holy Sword

Flow: clip, voice holySword1 / 2 (`:33132-33187`), `holySword_ring` at the hero (`createEffect(..., position,
rotation)`, distance 0, `:33206-33218`) at 0; wait 0.5 (`:33244`) -> case 2: the player's camera motion blur
(`:32916-32921`) and, if the equipped weapon has ATK, `RPC_AddStatus("holySword", 5, chaAdjust(24), ...)` (`:32943-32969`);
wait 0.6 (`:33246`) -> standby at 1.1 s (`:32990`).
- `holySword_ring`: needs EmblemEmitter (`fx_inventory.md`; probe agrees). It carries an AudioSource playing
  `holySword_ring` on awake (rip prefab: `m_PlayOnAwake: 1`, clip = `sounds/holySword_ring.wav`), so leaving the effect
  out also drops that sound.
- The status's look: `holySword` (`Effects/holySword`, legacy particles only: EllipsoidParticleEmitter +
  ParticleAnimator + ParticleRenderer, parts the page builds; the probe extracted it) instantiated twice, parented to
  `mount_Hand_L` and `mount_Hand_R` at local (0, 0, 0.2), rotation Euler(90, 0, 0) (`CharacterControl.cs:34264-34290`),
  kept for the status's `chaAdjust(24)` s and removed with it (`:15166`). Not in `fx_inventory.md` (loaded by
  `CharacterControl.cs`). Left out: the cue format places effects at the hero's root + metres ahead, it can't parent to
  a bone or last past the clip.

```json
[0, "voice", "holySword1|holySword2"]
```
Once EmblemEmitter is built, add `[0, "fx", "holySword_ring"]` (its own sound comes with it). Optional stand-in until
then: `[0, "voice", "holySword_ring"]` (the ring's sound alone; the recipe says only coroutine voices are "voice" cues,
so this is the editor's / user's call).

why: `RPC_holySword: clip (:33083); voice holySword1 / 2 (:33132-33187) at 0; left out: holySword_ring at the hero at 0 needs EmblemEmitter (:33206-33218), the status's holySword glow on both hands from 0.5 s (:32969; CharacterControl.cs:34264) needs a bone-attached cue, the camera blur (:32921); standby 1.1 s (:33246, :32990)`

### Inventory status of every effect named

| Effect | Skill | Status |
|---|---|---|
| `braveSpirit` | Brave Spirit (no #402) | ready (`fx_inventory.md` wolf; Wolf.cs:20357) |
| `gloriousSpirit` | Brave Spirit with #402 | ready (Wolf.cs:20394) |
| `secondWind` | Second Wind | ready (Wolf.cs:23221) |
| `holySword_ring` | Holy Sword | needs EmblemEmitter (Wolf.cs:33206) |
| `holySword` (status, on both hands) | Holy Sword | parts built, not listed (CharacterControl.cs); needs bone attachment + status-length life in the cue format |
| `valor_emblem` (status, 2 m up) | Brave Spirit | not listed (CharacterControl.cs:33969); needs EmblemEmitter + an upward offset |
| (none) | Lunar Eclipse | black tint (setColor) and camera ramp: no prefab |

Sounds to build (all exist in the rip): voices `gloriousSpirit1/2`, `braveSpirit1/2` (if plain Brave Spirit is kept),
`secondWind1/2`, `lunarEclipse1/2`, `holySword1/2`; sounds `braveSpirit`, `secondWind`.

## 3. Game rules that limit the choice

- **All four fit one max build, so none excludes another.** BB's Basic + Class A + Class B pool is 49 points from Lv 50
  (`clamp(lv - 1, 0, 49)`, Mechanics Reference §3.6), rows are learned left to right. Brave Spirit 4 + Weapon Plus 4
  (Holy Sword's prerequisite) + No Ko 1-3 + Second Wind need 22 Paladin skills; Lunar Eclipse 2 (rBn 25) needs 26 Blade
  Master skills: 48 of 49 (`checks/fx_wolf_research/cast/build_check.py`, smallest feasible prefixes per row). Class C:
  Glorious Spirit (0), Revised Skill (0), Revised Magic (1), Revised Art (3), then Holy Sword (rBn 4) = 5 of the 10 C
  points at Lv 100. Tight, but legal: a player can own all of them at once.
- **Glorious Spirit (#402, Lv 55 passive) replaces Brave Spirit's voice pair and effect** (`:20638`, `:20345`). It is a
  learned skill, not a random pick, so not "a|b". The max-rank rule and the Added Fire precedent (NOTES "Max rank
  everywhere": the Lv 55 passive the user wanted) point to the Glorious Spirit version; plain Brave Spirit is the other
  build. Open question 2.
- **Second Wind only below 25 % HP** (`Wolf.cs:5630-5650`, MP / SP refunded otherwise). A condition, not an exclusion:
  a player can cast it.
- **Holy Sword needs an equipped weapon with ATK > 0** for its status (and so the hand glow), `:32943-32963`; the clip,
  voice and ring play regardless. With Holy Armor already on, the status becomes `holyWolf` instead
  (`CharacterControl.cs:11925-11971`: different look, `holyWolfSword1Fx` / `2Fx`, armour, aura); while `holyWolf` is on,
  Lunar Eclipse's status is refused (`:11010-11022`), but its clip, voice and sound still play (the coroutine doesn't
  check). Neither matters for a cast from a clean state, which is what the wardrobe shows.
- **Lunar Eclipse rank and Brave Spirit rank change only numbers** (duration, valor level); no visual pick by `sLv`.
- **Cooldowns** (`agiAdjust`): Brave Spirit 30 s, Holy Sword 240 s, Lunar Eclipse 300 s, Second Wind 300 s. In a real
  fight Brave Spirit is cast about 8-10 times as often as each of the others (weights 1/30 : 1/240 : 1/300 : 1/300 =
  10 : 1.25 : 1 : 1). For showing the skills, an even pick is more useful; a weight field is offered below if the user
  wants "as often as a player casts them".

## 4. Proposed format: one skill's cue set picked at random per play

Keep one entry per clip, keyed by the clip's name; a clip several skills share holds a `skills` map instead of `cues`:

```json
  "instantCast": {
    "why": "instantCast is played by four skills (Brave Spirit :20597, Second Wind :23381, Lunar Eclipse :31341, Holy Sword :33083), all learnable in one Lv 100 build; each play shows one, picked at random",
    "skills": {
      "braveSpirit": {
        "why": "RPC_braveSpirit: ... (section 2)",
        "cues": [
        [0, "voice", "gloriousSpirit1|gloriousSpirit2"],
        [0, "voice", "braveSpirit"],
        [0.5, "fx", "gloriousSpirit", 0.2]
        ]
      },
      "secondWind": {
        "why": "RPC_secondWind: ...",
        "cues": [
        [0, "voice", "secondWind1|secondWind2"],
        [0, "voice", "secondWind"],
        [0.6, "fx", "secondWind", 0.2]
        ]
      },
      "lunarEclipse": {
        "why": "RPC_lunarEclipse: ...",
        "cues": [
        [0, "voice", "lunarEclipse1|lunarEclipse2"],
        [0, "voice", "braveSpirit"]
        ]
      },
      "holySword": {
        "why": "RPC_holySword: ...",
        "cues": [
        [0, "voice", "holySword1|holySword2"]
        ]
      }
    }
  }
```

Rules for the page (later work, not done here):
- The skill is picked once per play of the tile (uniformly, or by an optional `"weight"` per skill, e.g. 1 / cooldown),
  each time the move starts again, and held for all of that play's steps. For a sequence tile every step looks up the
  same skill key in its own clip's `skills` (a step without that key has no cues), so cast1 > cast2 > cast3 would never
  mix two skills' cues. (Not needed for the Wolf, whose Cast tile has no skills, but the Bat / Sheep / Whale researchers
  may have several cast-bar skills on cast1-3.) Entries with plain `cues` keep working as now.
- Optionally show the picked skill's Thai name (the skill icon / name the page already has) so the viewer knows which
  skill they are seeing.
- `wardrobe_fx.py`'s `cue_names` must also walk `skills.*.cues`; `wardrobe_fx_check.py` must play every skill of a
  shared clip (e.g. a query parameter forcing the pick) so each cue set is checked, not one at random.
- The page splits "a|b" only for voices (`fxTick`, `index.html:3243`); an "fx" cue with "a|b" would be treated as one
  missing name. None is needed here.

## 5. Open questions

1. The Wolf's "Cast" tile (cast1 > cast2 > cast3) is played by no Wolf skill in BB or TTO. Keep it as a bare animation
   (no cues), or drop it from `SEQ` (a page change, the user's call)? The clips stay available either way.
2. Brave Spirit: the Glorious Spirit version (max build, as proposed), the plain one, or both as two pool entries?
3. Even pick, or weighted by how often a player can cast each (Brave Spirit far more often)?
4. Holy Sword shows only its voice until EmblemEmitter exists. Add the ring's own sound as a stand-in "voice" cue?
5. Status looks (Holy Sword's glowing hands, Lunar Eclipse's black body, Brave Spirit's emblem) are the most visible part
   of these buffs. They need cue features the format lacks: parent to a bone (`mount_Hand_L` / `_R`), an upward offset,
   a body tint, and a life past the clip (the status lasts 15-24+ s). Worth a page job?
6. A cue file entry for cast1-3 with only a `why` (empty `cues`) would document the finding; whether
   `wardrobe_fx_check.py` accepts an entry with no cues is untested.

## Recipe problems

- **Clips no skill plays:** the recipe assumes each ท่าสกิล clip / SEQ tile has a skill. `clip_calls.js` already prints
  "no call found: cast1 cast2 cast3" for the Wolf, but the page's SEQ has a Wolf "Cast" tile anyway; the recipe has no
  step for "verify the tile is the game's" or for what to do when it isn't.
- **One clip, several skills:** cues are keyed by clip, one cue list per clip; instantCast is shared by four skills and
  the format can hold only one. Section 4's `skills` map is the proposed fix (also affects `cue_names` and the check).
- **Coroutine sounds:** "Only voices go in as voice" reads as `Voices/` only; Brave Spirit, Second Wind and Lunar Eclipse
  also `PlayOneShot` a `Sounds/` clip from the coroutine itself (not an effect's AudioSource). They must be "voice" cues
  (it works: `rip_wav` looks in `sounds/` first), and the recipe should say so. A sound and a voice with the same
  name in both folders would collide (none here).
- **Status looks live outside the coroutine:** a buff's visual is spawned by `CharacterControl.cs`'s status apply
  (`valor_emblem`, `holySword` on the hands, Lunar Eclipse's tint), which `clip_flow.js` on the coroutine never shows
  and `fx_inventory.md` (only what `<Class>.cs` loads) never lists. The recipe's "a buff the skill puts on the hero
  stays (distance 0)" can't be followed for these: they need bone parenting, height offsets, tints, long lives.
- **No read-only probe:** step 1.5 says followState shows in `fx.json` after `wardrobe_fx.py --fx <name>`, but that run
  writes the shared data. Research agents need a dry-run flag (I imported `wardrobe_fx.effect()` in a scratch script,
  `checks/fx_wolf_research/cast/probe.py`, to read followState without writing). The same probe also shows a prefab's
  missing layouts (EmblemEmitter) directly.
- **Effect "a|b":** the recipe's cue description says name "a|b" = random pick for any cue, but the page only splits
  voices.
- **clip_flow.js output** lists the matched lines but not the `IL_xxx` -> `Yield` chain clearly; following
  `goto Block_n` -> `IL_n` -> `Yield(...)` still needs reading the raw source with the junk predicates filtered
  (`grep -v 'if (N - M != K)'`). A filter mode in the tool would save time.
