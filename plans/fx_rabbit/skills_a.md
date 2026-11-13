Summary: all 11 clips are traced, with file:line, through the opaque predicates and the timed waits. 10 skills, 11 cue keys,
39 cues. One pool: `gilShot`, played by Gil Shot and Diamond Shot (and by the four medical shots under Rapid Trance's
status, left as a state variant). Bounce is one 9.5 s sequence: the Rabbit is hidden from 0.9 s to 9.5 s, with the From the
Above landing ring at 8.9 s. Mall is one 8 s sequence: the stall is picked by the outfit colour (mall1-5), and the steps are
mall1, mall2, then the emote clip `sit`. Two parts are needed: P1, a one-line Shuriken graft for extravagance_ring, and P2,
a no-op Rabbit_mall part. The icon fixes are page lines. `kneeShot_hit` is missing from both games' data. There are
9 open questions, each with a recommended answer.

# Rabbit effects + sounds research: skills_a (eleven skill clips)

Researcher `skills_a`, 2026-11-13 (office PC).
- **Scope:** the clips backpack, bounce1, bounce2, circleShot, extravagance, fourShot, gilShot, gorgonShot, maim, mall1 and
  mall2, and every skill that plays them.
- **Method:** research only (recipe steps 1-3).
- **Line numbers:** `C:\Users\Jump\Desktop\12tails\DecompiledSource\Rabbit.cs` (the home PC's `D:\12tails\...`) unless
  another file is named. "TTO1102" means `DecompiledSource_TTO_2026-11-02\pseudo\Rabbit.c`.
- **Units:** times are seconds from the start of the clip the cue is keyed by. d = metres ahead, x = metres right, y =
  metres up.

## Read-only probes

Everything is in `C:\work\12tails-wardrobe\checks\fx_rabbit_research\skills_a\` (git-ignored). Nothing there writes
outside that folder.

- **Coroutine reads:**
  - `clean.py <file> <from> <to>` works out the opaque predicates (`if (a - b == c)`): a false test drops its block and
    keeps its else, a true one keeps its block.
  - `mn.sh <RPC>` prints one coroutine's cleaned MoveNext.
  - Outputs: `clean_bounce.txt`, `clean_bounce0.txt`, `clean_maimShot.txt`, `clean_gilShot.txt`, `clean_diamondShot.txt`,
    `clean_medicalShot.txt`, `clean_gorgonShot.txt`, `clean_backpack.txt`, `clean_fourShot.txt`, `clean_circleShot.txt`,
    `clean_mall.txt`, `clean_mall_open.txt`, `clean_extravagance.txt`, `clean_hits.txt` (the `RPC_*_hit` methods and
    `RPC_mall_setup` / `_close`) and `clean_Rabbit_mall.txt`.
  - Also `flow_RPC_*.txt` (clip_flow.js) and `clip_calls.txt` (clip_calls.js).
- **`probe\probe.json`** with `probe\summary.txt` (from `summ.py`): `wardrobe_fx.py rabbit --probe` of 36 names.
  - KeyError for: kneeShot_hit, fourShot_hit, circleShot_hit, mall, mall0, mall6, mall7.
  - Every other name read whole.
- **`probe\probe_tto.json`** (`wardrobe_fx_tto.py rabbit --probe extravagance_ring,mall1`): TTO's extravagance_ring
  has two readable ParticleSystems, with materials tto_Gil and tto_star5. `probe_tto.err`: kneeShot_hit, fourShot_hit
  and circleShot_hit are not in TTO's catalog either.
- **`probe\probe2.py` -> `probe2.txt`:** extravagance_ring with `SHURIKEN_FROM_TTO["rabbit"] = ["extravagance_ring"]` set
  in memory only. Both systems graft by the Chameleon's `graft_by_material` route: node 3 gets material Gil and node 4
  gets star5.
- **`hitpoints.py` -> `hitpoints.txt`:** where the shots meet the standard target body (Bat decision 4: a capsule centred
  0.6 m up, 10 m ahead, height 1, radius 0.3), and the fire effects' pitch.
- **`cues.json`:** the paste-ready block below, checked with json.load. Every time list is in order, and every option is
  in wardrobe_fx_check.py's OPTS.

## Max rank and passives on

- Bounce 2 (8 s airborne) + From the Above #421 (`rab_fromTheAbove5`, RabbitSkill.cs:3182).
- Maim Shot 4 + Knee Shot #402 (:3215).
- Gil Shot 4 + Diamond Shot #403 (damage only).
- Diamond Shot (one rank).
- Gorgon Shot 2.
- Backpack 2 + Big Bag #423 (:3292).
- Four Shot 2 and Circle Shot 2, with Ten Shot #433 (damage only).
- Mall 2. Extravagance (one rank) + Skill Bargain #413 (the fee only).

Only Bounce's rank changes a look: the airborne time is 4 x sLv. The passives pick effects:
- #421: fromTheAbove_ring replaces bounce2's landing effect.
- #402: a 20 % chance that the maim hit is the missing kneeShot_hit.
- #423: bigbag_ring replaces backpack_ring.

---

## Read this first

### 1. Who plays these clips

| clip | BB | TTO1102 |
|---|---|---|
| bounce1 | RPC_bounce :21238 | `<RPC_bounce>d__178` (:2715) |
| bounce2 | RPC_bounce0 :21571 (the landing, started by RPC_bounce :21114) | `<RPC_bounce0>d__179` (:2160) |
| maim | RPC_maimShot :23486 | `<RPC_maimShot>d__182` (:11695) |
| gilShot | RPC_gilShot :30539; RPC_diamondShot :38454; RPC_medicalShot :28552 (**only under Rapid Trance's status**) | the same three (:9678, :7498, :13403) |
| gorgonShot | RPC_gorgonShot :29859 | :10478 |
| backpack | RPC_backpack :31428 | :1311 |
| fourShot | RPC_fourShot :32022 | :8647 |
| circleShot | RPC_circleShot :32945 | :5617 |
| extravagance | RPC_extravagance :40003 | :8226 |
| mall1 | RPC_mall :33439; RPC_mall_setup :10854 (the server's setup reply, MallGui.cs:4929: the same looped clip again) | :12441, :35549 |
| mall2 | RPC_mall_open :33860 (MallGui.cs:4965) | :12934 |

- TTO's copies load the same effect and voice names. The exceptions: the Mall's voices (item 5) and TTO's Mall spot gates
  (lawn, Life Altar), which change no look.
- **No TTO skill plays any of these clips.** The TTO actives Bounty Hunt, Coin Ricochet and Medic Turret have clips of
  their own. So no TTO cue comes from this scope.

### 2. The gilShot pool: Gil Shot and Diamond Shot

- The two members are one tile each. Their timings are the same: ring at 0, fire and hit at 1.0, standby 1.3. Only the
  names differ.
- No sequence plays gilShot, so each member's tile is the clip alone (poolChains).
- The medical shots under Rapid Trance's status play gilShot too:
  - No cooldown and no voice at the cast.
  - medicalShot_ring at 0.3 s, then the fire at 1.0 s instead of 1.4 s (:28548-28555, Yield 0.3 :28735, Yield 0.7
    :28730).
  - They are the same four skills as the medicalShot tiles, in a state a 12 s active buff gives (not a passive). So no
    member: open question 3.

### 3. Bounce: hidden for 8.6 s, From the Above at the landing

- bounce1 plays once. At 0.9 s the hide status switches every Renderer off (CharacterControl.cs:32818-32853), and the
  8 s timer starts (:21068-21073).
- At 8.9 s, RPC_bounce0 plays the voice bounce0 and **fromTheAbove_ring** (#421). With the passive, the bounce2 effect
  is the else branch (:21820-21887), so it never shows.
- At 9.5 s the hero is shown again and bounce2 cuts in. At 9.9 s comes the 3 m stomp (no look). Standby is at 10.3 s.
- Page line: **SEQ "Bounce: bounce1@9.5 bounce2!"** (was "bounce1 bounce2").
- The hide uses the page's whole-hero cue, `[0.9, "hideProp", "hero", {"kill": 8.6}]`: Chameleon decision 49, the Mole's
  King Kaiser. It matches the hide status, which turns off all renderers, the weapon's included.
- The steering and From the Above's air shots need the player's keys, so they are left out (open question 2).

### 4. Mall: the stall by outfit colour, then mall2 and sit

- RPC_mall loads `Effects/mall` + Math.div(Skin, 100) (:33507). That is `mall1`-`mall5` by the outfit's colour number
  (RabbitEquipment.cs:1474-1492). The probe has mall1-5 and no other number.
- The cue is the Mole's `"pick": "color"` list (index.html pickOf). Every wardrobe Rabbit outfit has colours 1-5
  (data/rabbit/outfits.json), so no fallback is needed.
- The stall is a mesh plus the Rabbit_mall script:
  - The script has no serialised fields.
  - Its OnGUI draws the buy button for other players only (Rabbit_mall.cs:163).
  - It destroys the stall once the owner leaves mallSetup / mallOpen (:110-137).
- After the setup window, RPC_mall_open cuts in mall2, looped. 2 s later it plays the emote clip `sit` with a 0.2 s fade,
  looped (:33834-33863).
- Page line: **SEQ "Mall: mall1*@3 mall2*!@2 sit*~@3"** (was "mall1* mall2*").
  - The two holds use the SEQ rule's 3 s for a hold that runs until the player acts: the setup window and the sit until a
    move.
  - The stall's kill is 7.95.
  - `sit` takes the cue key `@Mall:sit`, so the sit emote tile gets no Mall cue (as the Chameleon's `@Tent:sleep`).

### 5. The Mall's voices are TTO's (BB's own recordings, never played by BB)

- BB's rip has `voices/mallOpen.wav` and `mallClose.wav`, but no BB code loads them.
- TTO1102 plays mallOpen in RPC_mall_open (pseudo/Rabbit.c:12915-13000) and mallClose in RPC_mall_close (:35591-35700).
- They are cued on mall2 at 0 and on `@Mall:sit` at 2.95 s (the close at the end of the 3 s hold). Open question 5 says
  to drop the two cues if the BB look is wanted.

### 6. Missing parts

- **P1 extravagance_ring's Shuriken:**
  - BB's two ParticleSystem nodes are dropped by the extractor (inventory: "needs ParticleSystem, ParticleSystemRenderer").
  - TTO's copy reads whole. The fix is `SHURIKEN_FROM_TTO["rabbit"] = ["extravagance_ring"]`, with **no** SHURIKEN_MAT
    entry, so it takes the Chameleon's graft_by_material route.
  - Proved in memory: probe2.txt grafts node 3 from TTO node 1 (Gil) and node 4 from TTO node 4 (star5).
  - The two nodes share the name "ParticleSystem". The SHURIKEN_MAT route's dict by name path would give both the
    second system, so do not add a SHURIKEN_MAT entry.
  - Then add extravagance_ring to the inventory's built list.
- **P2 Rabbit_mall:**
  - The script has zero field bytes. The probe reads mall1-5 with no layout.
  - It needs a no-op part (`fxparts/rabbit.js`: `api.part("Rabbit_mall", () => null)`), as Chameleon_campFire's, so that
    the inventory can list it as built.
  - The stall's life is the cue's kill.
  - The inventory scanner misses mall1-5 entirely, because the name is built by string concatenation (:33507). Add them
    by hand, as the Mole's field effects were added.

### 7. Missing from both games' data (no stand-in)

- **`kneeShot_hit`**:
  - Knee Shot's roll (20 % at LCK 1, :23256-23273) calls RPC_kneeShot_hit (:9669-9704). That loads
    `Effects/kneeShot_hit`, which is in neither BB's Resources nor TTO's catalog.
  - The game logs "Cannot find kneeShot_hit Effect" and draws nothing, and those 20 % of hits lose the maimShot_hit flash
    too.
  - It is cued as maimShot_hit at `p` 0.8. There is no stand-in, as for the Mole's advanceRepair_ring (Mole decision on
    the missing rings).
- `fourShot_hit` and `circleShot_hit` (RPC_fourShot_hit :10744, RPC_circleShot_hit :10794) are never called. Their
  prefabs do not exist, and Four Shot and Circle Shot spawn nAttack_hit instead.
- All three are a Bible finding to offer.

### 8. Icons (page lines)

- `maim` gets no icon today: no skill is named "maim". Diamond Shot needs one too. Add
  `CLIP_SKILLS["rabbit"] = {"maim": ["maimShot"], "gilShot": ["gilShot", "diamondShot"]}`.
- **Five tiles in scope show a rank-IV icon for a rank-2 skill:** Backpack, Circle Shot, Four Shot, Gorgon Shot and Mall.
  - wardrobe_skill_icons.py takes the highest number in assets.js, which also holds rank III/IV images
    (`rabbit_mall3` / `4` ...).
  - The Bible's cards use `rabbit_<skill>2`. `data/icons/hd/rabbit/mall.webp` is byte-equal to `rabbit_mall4` (II / III /
    IV checked by eye, `checks\...\skills_a\mall_icons.png`).
  - Fix: `RANK_ICONS["rabbit"] = {"backpack": "rabbit_backpack2", "circleShot": "rabbit_circleShot2", "fourShot":
    "rabbit_fourShot2", "gorgonShot": "rabbit_gorgonShot2", "mall": "rabbit_mall2"}`. RANK_ICONS already overrides
    `best` for any skill (:126).
  - Out of my scope, the same check gives millionaire, shootingArray, statScan, rapidTrance, truceTrading, cAttack and
    nAttack at their "4" keys. Each needs comparing with its card's top rank.

### 9. Left out: hits out of reach, statuses, camera, travel

- **Hits that never reach the 10 m target:** Backpack's three 3 m pulses (backpack_hit), Circle Shot's three 8 m pulses,
  and Four Shot's back, left and right cones. Bounce's 3 m stomp has no look.
- **Statuses with no look:** maim, petrify (the Gorgon target's stone look is an enemy model the page has not), and
  Extravagance's atkUp (CharacterControl.cs:33176-33180, deltaAtk only).
- **Camera effects:** the motion blurs (Gorgon :30009, Circle :32663, Extravagance :39859) and Circle Shot's AutoZoom.
- **Steps the hero would take:** Maim -1 m/s, Gil -1, Gorgon -3 (the recoil) and Bounce's landing -5. The hero does not
  travel (Mole Read this first 9).
- **Screen text and money:** Extravagance's "+N atk" message, the Gil and Diamond fees, the Mall windows.

### What is ready (inventory + probe)

- **Effects:** bounce1, fromTheAbove_ring, maimShot_fire, maimShot_hit, nAttack_hit, gilShot_ring, gilShot_fire,
  gilShot_hit, diamondShot_ring, diamondShot_fire, diamondShot_hit, gorgonShot_ring, gorgonShot_fire (its AlphaTimer is
  built), gorgonShot_hit, bigbag_ring (TrailEmitter, StaticMesh, Animation), fourShot_fire, circleShot_ring, circleShot.
- **Not ready yet:** extravagance_ring (P1) and mall1-5 (P2).
- **Voices** (all in BB's rip, `voices/`): bounce0-2, maimShot1-2, gilShot1-2, diamondShot1-2, gorgonShot1-2, backpack1-2,
  fourShot1-2, circleShot1-2, mallOpen, mallClose.
- **Effect sounds** (all in BB's rip, `sounds/`): bounce1, fromTheAbove, nAttack, gilShot, gilShot_hit, diamondShot,
  gorgonShot, bigbag_ring, fourShot_fire, circleShot, extravagance_ring.

---

## Bounce (`bounce1` 0.9 s, `bounce2` 1.1 s)

Sources: RPC_bounce :20867-21425; RPC_bounce0 :21430-21959.

| time (tile) | what happens | source |
|---|---|---|
| 0 | bounce1 cut in (Once); voice bounce1 or 2 | :21238, :21279-21338 |
| 0.5 | `bounce1` effect at the hero (life 0.5, own sound) | :21019-21031, Yield 0.5 :21357 |
| 0.9 | hide status (9 s); timer = now + 8 | :21068-21073, Yield 0.4 :21375 |
| 8.9 | Time > timer: RPC_bounce0, voice bounce0, `fromTheAbove_ring` (#421; else bounce2) | :21108-21114, :21796-21887 |
| 9.5 | hide removed; bounce2 cut in | :21566-21571, Yield 0.6 :21908 |
| 9.9 | moveSpeed -5; 3 m stomp (#421), damage only | :21603-21652, Yield 0.4 :21906 |
| 10.3 | standby | :21683-21698, Yield 0.4 :21910 |

- `bounce2` gets no entry: nothing visible starts on its clock.
- Rank 1 would be 4.9 s instead of 8.9 s (open question 1).

## Maim Shot (`maim`, 1.0 s)

Source: RPC_maimShot :22949-23697.

| time | what happens | source |
|---|---|---|
| 0 | clip (0.2 fade); voice maimShot1 or 2 | :23486, :23527-23586 |
| 0.5 | `maimShot_fire` at (0, 1, 0), pitched 2.29° down toward the target's centre | :23106-23156, Yield 0.5 :23610 |
| 0.6 | ray hit at (0, 0.612, 9.7): `nAttack_hit`; then 80 % `maimShot_hit` / 20 % the missing kneeShot_hit | :23211-23325, Yield 0.1 :23608 |
| 0.8 | standby | :23402-23417 |

maimShot_hit has no EffectControl: one ImageEmitter burst of 0.3 + 0.5 s, and the game never destroys it. The page gets
`kill` 1 so that a looping tile does not pile them up.

## The gilShot pool (`gilShot`, 1.7 s): Gil Shot and Diamond Shot

Sources: RPC_gilShot :30125-30835; RPC_diamondShot :38030-38720.

| time | Gil Shot | Diamond Shot | source |
|---|---|---|---|
| 0 | clip (0.2 fade); voice gilShot1 or 2; `gilShot_ring` (followState, life 0.5) | clip; `diamondShot_ring`; voice diamondShot1 or 2 | :30539-30736 / :38454-38658 |
| 1.0 | `gilShot_fire` at (0, 1, 0), pitched 2.29°; `gilShot_hit` at (0, 0.612, 9.7), identity | `diamondShot_fire`; `diamondShot_hit` (identity) | :30282-30388 / :38176-38282 |
| 1.3 | standby | standby | :30455-30470 / :38370-38385 |

The rings' followState never cuts them: their 0.5 s life ends before the 1.3 s standby.

## Gorgon Shot (`gorgonShot`, 2.0 s)

Source: RPC_gorgonShot :29387-30120.

| time | what happens | source |
|---|---|---|
| 0 | clip; voice gorgonShot1 or 2; `gorgonShot_ring` (life 3, no followState) | :29859-29986 |
| 1.3 | firePos = position + (0, 1, 1); fireDir to the target's centre | :29545-29567, Yield 1.3 :30042 |
| 1.4 | `gorgonShot_fire` at (d 1, y 1), pitched 2.29° (beam mesh, AlphaTimer); SphereCastAll r 1, 36 m: `gorgonShot_hit` at the contact (0, 0.692, 9.7) | :29594-29688, Yield 0.1 :30029 |
| 1.8 | standby | :29775-29790 |

## Backpack (`backpack`, 1.2 s)

Source: RPC_backpack :30840-31760.

| time | what happens | source |
|---|---|---|
| 0 | clip cut in (Once); voice backpack1 or 2 | :31428, :31499-31562 |
| 0.2 | the gun's MeshRenderers off (slot R); `bigbag_ring` (Big Bag) with its swung bag mesh | :30987-31053, Yield 0.2 :31695 |
| 0.3 / 0.5 / 0.7 | 3 m pulses, nothing in reach | :31568-31643 |
| 1.0 | standby; the gun on again | :31322-31394 |

## Four Shot (`fourShot`, 1.8 s)

Source: RPC_fourShot :31823-32500.

| time | shot | fire point (x, y, d) | source |
|---|---|---|---|
| 0 | clip; voice fourShot1 or 2 | | :32022, :32093-32156 |
| 0.4 | forward: hits the target, `nAttack_hit` at ClosestPointOnBounds(hero + up) = (0, 1, 9.7) | (0.15, 0.85, 0.85) | :32246, :32380-32390 |
| 0.7 | back | (0.15, 1, -0.85) | :32263 |
| 1.0 | left | (-0.65, 0.65, 0) | :32280 |
| 1.3 | right | (0.85, 0.75, -0.2) | :32297 |
| 1.6 | standby | | :32162-32193 |

Each `fourShot_fire` has identity rotation (:32326). The waits are Yield 0.4 :32442, then 0.3 each (:32436). The Bible's
"0.3-0.4 s between shots" is 0.4 to the first and 0.3 after that.

## Circle Shot (`circleShot`, 1.3 s)

Source: RPC_circleShot :32503-33220.

| time | what happens | source |
|---|---|---|
| 0 | clip; voice circleShot1 or 2; `circleShot_ring` (followState, life 1) | :32945-33084 |
| 0.6 | `circleShot` 1.7 m up | :32903-32921 (Yield 0.4 :33157, 0.2 :33143) |
| 0.733 | `circleShot` 2.2 m up; pulse 1 (8 m) | Yield 0.133 :33141 |
| 0.866 | `circleShot` 1.7 m up; pulse 2 | — |
| 1.0 | pulse 3 | — |
| 1.1 | standby | Yield 0.1 :33154 |

## Extravagance (`extravagance`, 1.2 s)

Source: RPC_extravagance :39711-40115.
- At 0: the clip and `extravagance_ring` (followPosition; Gil coins and star sparks through P1). **No voice**: BB and TTO
  load none.
- At 0.7 s: atkUp, which has no look. Standby at 1.0 s.

## Mall (`mall1` 0.8 s loop, `mall2` 1.2 s loop, then `sit`)

Sources: RPC_mall :33223-33734; RPC_mall_open :33739-33891; RPC_mall_close :10876-10919; Rabbit_mall.cs.

| time (tile) | what happens | source |
|---|---|---|
| 0 | mall1 (0.2 fade, Loop); no voice; stall `mall<colour>` at the hero | :33439-33553 |
| 0-3 | the setup window (hold rule) | :33569-33641 |
| 3 | mall2 cut in (Loop); voice mallOpen (TTO) | :33857-33863; TTO1102 :12915-13000 |
| 5 | sit (0.2 fade, Loop) | :33834-33839, Yield 2 :33871 |
| 7.95 | the close (hold rule): voice mallClose (TTO); standby; the stall destroyed | :10907-10913; Rabbit_mall.cs:110-137; TTO1102 :35591-35700 |

---

## Paste-ready cue entries for wardrobe/fx_cues/rabbit.json

Validated in `C:\work\12tails-wardrobe\checks\fx_rabbit_research\skills_a\cues.json`.

```json
{
  "bounce1": {
    "why": "Rabbit.cs RPC_bounce (:20867-21425), Bounce rank 2 (sLv 2), From the Above #421 on (passives on): bounce1 cut in (PlayAnimation(bounce1, 0), Once, :21238-21241; the page's first-step fade stays, Cat decision 2) and voice bounce1 / bounce2 (Random.Range(0, 2) :21279-21338, PlayOneShot :21383 / :21363) at 0; Yield 0.5 (:21357): Effects/bounce1 Instantiated at the hero, hero rotation (:21019-21031; EffectControl life 0.5, its own Sounds/bounce1); Yield 0.4 (:21375): at 0.9 s (bounce1's last frame) addStatus hide (level 1, 4 x sLv + 1 = 9 s, :21068), every Renderer of the hero off (CharacterControl.cs:32818-32853: the page's whole-hero hideProp), mBounceTimer = now + 4 x sLv = 8 s (:21073); each FixedUpdate until Time > mBounceTimer (:21108; the steering by the arrow keys :21136-21190 and the From the Above air shot on the attack key, :8944 / :22100-22260, left out: the player's input): at 8.9 s RPC_bounce0 (:21114; :21496-21925): voice bounce0 (one file, :21796-21808) and, #421 learned, Effects/fromTheAbove_ring at the hero, hero rotation (:21820-21840; life 2, its own Sounds/fromTheAbove) in place of Effects/bounce2 (the else branch :21859-21875, not drawn with the passive); Yield 0.6 (:21908): at 9.5 s removeStatus hide (:21566, the hero shown again: CharacterControl.cs:14547-14573) and bounce2 cut in (:21571, the SEQ's bounce1@9.5 bounce2!)",
    "cues": [
      [0, "voice", "bounce1|bounce2"],
      [0.5, "fx", "bounce1"],
      [0.9, "hideProp", "hero", {"kill": 8.6}],
      [8.9, "voice", "bounce0"],
      [8.9, "fx", "fromTheAbove_ring"]
    ]
  },
  "maim": {
    "why": "Rabbit.cs RPC_maimShot (:22949-23697), Maim Shot rank 4 + Knee Shot #402 (passives on): maim (0.2 fade, Once, :23486-23489) and voice maimShot1 / maimShot2 (Random.Range(0, 2) :23527-23586, PlayOneShot :23622 / :23625) at 0; Yield 0.5 (:23610): moveSpeed -1 (the step back, left out: the hero does not travel), firePos = position + up, fireDir = the target's collider.bounds.center - position - up (:23111-23127: from (0, 1, 0) to the 10 m target 0.6 m up, pitch atan(0.4 / 10) = 2.29 deg), Effects/maimShot_fire at firePos, FromToRotation(forward, fireDir) (:23133-23156; life 1, its own Sounds/nAttack); Yield 0.1 (:23608): at 0.6 s the Raycast from firePos along fireDir (16 + 5 x Combo m, :23211-23216) meets the standard target body at (0, 0.612, 9.7) (checks/fx_rabbit_research/skills_a/hitpoints.txt): RPC_nAttack_hit there (:23224; Rabbit.cs:9112-9147 Effects/nAttack_hit, hero rotation) and, the hit landing, Knee Shot's roll Random.Range(0, 100) < lckAdjust(20) = 20 at LCK 1 (:23256-23273; CharacterControl.cs:20658: floor(100 x 20.2 / 100.2)): 20 % RPC_kneeShot_hit (:23294; Effects/kneeShot_hit, :9682, is in neither BB's data nor TTO's catalog: nothing drawn), 80 % RPC_maimShot_hit (:23314; Effects/maimShot_hit at the hit, LookRotation(forward) = the hero's, :9639-9649; no EffectControl, one ImageEmitter burst of 0.3 + 0.5 s, so the game never destroys it: kill 1 for the page); the maim status (getDebuff(3), :23337-23348) draws nothing; Yield 0.1 x 2 (:23628, :23620): standby at 0.8 s (:23402-23417)",
    "cues": [
      [0, "voice", "maimShot1|maimShot2"],
      [0.5, "fx", "maimShot_fire", {"y": 1, "rot": [2.29, 0, 0]}],
      [0.6, "fx", "nAttack_hit", {"d": 9.7, "y": 0.61}],
      [0.6, "fx", "maimShot_hit", {"d": 9.7, "y": 0.61, "p": 0.8, "kill": 1}]
    ]
  },
  "gilShot": {
    "why": "The gilShot clip is played by RPC_gilShot (Rabbit.cs:30539) and RPC_diamondShot (:38454), each with a 0.2 s fade, Once, and by RPC_medicalShot only under Rapid Trance's status (:28548-28552: the four medical shots' state variant, no member: their tiles are on medicalShot, open question 3); TTO1102's three coroutines name it the same (pseudo/Rabbit.c:7498, :9678, :13403): one tile each (poolChains), the clip alone",
    "skills": {
      "gilShot": {
        "why": "Rabbit.cs RPC_gilShot (:30125-30835), Gil Shot rank 4 + Diamond Shot #403 (damage only): gilShot (0.2 fade, Once, :30539-30542), voice gilShot1 / gilShot2 (Random.Range(0, 2) :30580-30639) and Effects/gilShot_ring at the hero, hero rotation (createEffect :30720-30736; EffectControl life 0.5 + afterLife 1, followPosition, followState; its own Sounds/gilShot) at 0; Yield 1 (:30769): at 1.0 s moveSpeed -1 (left out), firePos = position + up, fireDir to the target's bounds centre (:30287-30303: pitch 2.29 deg), Effects/gilShot_fire at firePos, FromToRotation(forward, fireDir) (:30309-30332; life 1, its own Sounds/nAttack), the Raycast (16 + 5 x Combo m, :30364-30369) meets the target body at (0, 0.612, 9.7) (hitpoints.txt): RPC_gilShot_hit there (:30377; Effects/gilShot_hit, Quaternion.identity, :10502-10512; life 1, its own Sounds/gilShot_hit); Yield 0.2, 0.1 (:30771, :30775): standby at 1.3 s",
        "cues": [
          [0, "voice", "gilShot1|gilShot2"],
          [0, "fx", "gilShot_ring"],
          [1, "fx", "gilShot_fire", {"y": 1, "rot": [2.29, 0, 0]}],
          [1, "fx", "gilShot_hit", {"d": 9.7, "y": 0.61}]
        ]
      },
      "diamondShot": {
        "why": "Rabbit.cs RPC_diamondShot (:38030-38720), Diamond Shot (one rank): gilShot (0.2 fade, Once, :38454-38457), Effects/diamondShot_ring at the hero, hero rotation (createEffect :38538-38556; life 0.5 + 1, followPosition, followState; its own Sounds/diamondShot) and voice diamondShot1 / diamondShot2 (Random.Range(0, 2) :38599-38658, PlayOneShot :38694 / :38690) at 0; Yield 1 (:38680): at 1.0 s firePos = position + up, fireDir to the target's bounds centre (:38181-38197: pitch 2.29 deg), Effects/diamondShot_fire at firePos, FromToRotation(forward, fireDir) (:38203-38226; life 1, its own Sounds/nAttack), the Raycast (:38258-38263) meets the target body at (0, 0.612, 9.7): RPC_diamondShot_hit there (:38271; Effects/diamondShot_hit, identity, :11405-11415; its own Sounds/gilShot_hit), then RPC_AddEffectDamage 1000 (:38322, the number only); Yield 0.2, 0.1 (:38678, :38684): standby at 1.3 s",
        "cues": [
          [0, "fx", "diamondShot_ring"],
          [0, "voice", "diamondShot1|diamondShot2"],
          [1, "fx", "diamondShot_fire", {"y": 1, "rot": [2.29, 0, 0]}],
          [1, "fx", "diamondShot_hit", {"d": 9.7, "y": 0.61}]
        ]
      }
    }
  },
  "gorgonShot": {
    "why": "Rabbit.cs RPC_gorgonShot (:29387-30120), Gorgon Shot rank 2: gorgonShot (0.2 fade, Once, :29859-29862), voice gorgonShot1 / gorgonShot2 (Random.Range(0, 2) :29900-29959) and Effects/gorgonShot_ring at the hero, hero rotation (createEffect :29968-29986; life 3 + 1, no followState; its own Sounds/gorgonShot) at 0; the local player's motion blur (:30009) left out; Yield 1.3 (:30042): firePos = position + TransformDirection(0, 1, 1), fireDir to the target's bounds centre (:29545-29561: pitch 2.29 deg); Yield 0.1 (:30029): at 1.4 s moveSpeed -3 (the recoil, left out), Effects/gorgonShot_fire at firePos, FromToRotation(forward, fireDir) (:29594-29617; life 1, its beam mesh Rabbit_gorgonShot 1 m ahead with its 0.4 s root clip and AlphaTimer), SphereCastAll radius 1, 36 m (:29644): its contact with the target body at (0, 0.692, 9.7) (hitpoints.txt): RPC_gorgonShot_hit there (:29677; Effects/gorgonShot_hit, LookRotation(forward), :10452-10462; life 1); the petrify status (:29699-29710) draws nothing here; Yield 0.2, 0.2 (:30040, :30033): standby at 1.8 s",
    "cues": [
      [0, "voice", "gorgonShot1|gorgonShot2"],
      [0, "fx", "gorgonShot_ring"],
      [1.4, "fx", "gorgonShot_fire", {"d": 1, "y": 1, "rot": [2.29, 0, 0]}],
      [1.4, "fx", "gorgonShot_hit", {"d": 9.7, "y": 0.69}]
    ]
  },
  "backpack": {
    "why": "Rabbit.cs RPC_backpack (:30840-31760), Backpack rank 2 + Big Bag #423 (passives on): backpack cut in (PlayAnimation(backpack, 0), Once, :31428-31433; the page's first-step fade stays) and voice backpack1 / backpack2 (Random.Range(0, 2) :31499-31562, PlayOneShot :31681 / :31674) at 0; Yield 0.2 (:31695): mWep1's MeshRenderers off (:30987-31014: the gun, the page's slot R; its weapon_fx particles stay) and, #423 learned, Effects/bigbag_ring at the hero, hero rotation (createEffect :31024-31053; EffectControl life 0.8, followPosition, followState; the bag mesh Rabbit_bigbag swung by its 0.83 s root clip, a trail, a ring; its own Sounds/bigbag_ring) in place of backpack_ring (Euler(270, 90, 0), the else branch :31072-31090); Yield 0.1 (:31677): three pulses at 0.3, 0.5, 0.7 s (FindAreaTarget 3 m with Big Bag, :31588; Yield 0.2 :31666), none reaching the 10 m target (backpack_hit only on a hit, :31632); at 0.9 s j = 3, Yield 0.1 (:31685): standby at 1.0 s and the gun shown again (:31366-31394): hideProp R from 0.2 for 0.8 s",
    "cues": [
      [0, "voice", "backpack1|backpack2"],
      [0.2, "hideProp", "R", {"kill": 0.8}],
      [0.2, "fx", "bigbag_ring"]
    ]
  },
  "fourShot": {
    "why": "Rabbit.cs RPC_fourShot (:31823-32500), Four Shot rank 2 + Ten Shot #433 (damage only): fourShot (0.2 fade, Once, :32022-32027) and voice fourShot1 / fourShot2 (Random.Range(0, 2) :32093-32156, PlayOneShot :32432 / :32427) at 0; Yield 0.4 (:32442), then one shot every 0.3 s (Yield 0.3 :32436) at 0.4, 0.7, 1.0, 1.3 s, each Effects/fourShot_fire at position + TransformDirection(...) with Quaternion.identity (:32308-32326; life 1, its own Sounds/fourShot_fire): forward (0.15, 0.85, 0.85) :32246, back (0.15, 1, -0.85) :32263, left (-0.65, 0.65, 0) :32280, right (0.85, 0.75, -0.2) :32297; each a FindAngleTarget cone of 24 m, 70 deg (:32355): only the forward one holds the 10 m target: RPC_nAttack_hit at its collider.ClosestPointOnBounds(position + up) = (0, 1, 9.7) (:32380-32390; nAttack_hit, hero rotation); at 1.6 s i = 4: standby (:32162-32193)",
    "cues": [
      [0, "voice", "fourShot1|fourShot2"],
      [0.4, "fx", "fourShot_fire", {"d": 0.85, "x": 0.15, "y": 0.85}],
      [0.4, "fx", "nAttack_hit", {"d": 9.7, "y": 1}],
      [0.7, "fx", "fourShot_fire", {"d": -0.85, "x": 0.15, "y": 1}],
      [1, "fx", "fourShot_fire", {"x": -0.65, "y": 0.65}],
      [1.3, "fx", "fourShot_fire", {"d": -0.2, "x": 0.85, "y": 0.75}]
    ]
  },
  "circleShot": {
    "why": "Rabbit.cs RPC_circleShot (:32503-33220), Circle Shot rank 2 + Ten Shot #433 (damage only): circleShot (0.2 fade, Once, :32945-32948), voice circleShot1 / circleShot2 (Random.Range(0, 2) :32998-33057) and Effects/circleShot_ring at the hero, hero rotation (createEffect :33066-33084; life 1 + 1, followPosition, followState: the 1.1 s standby comes after its life; its own Sounds/circleShot) at 0; the camera's AutoZoom (:33119, :32894) and motion blur (:32663) left out; Yield 0.4 (:33157), Yield 0.2 (:33143): from 0.6 s three Effects/circleShot at position + (1.7 + 0.5 x (i % 2)) up, hero rotation (:32903-32921): 1.7, 2.2, 1.7 m up at 0.6, 0.733, 0.866 s (Yield 0.133 :33141), each pulse's FindAreaTarget of 8 m (:32727, at 0.733, 0.866, 1.0 s) short of the 10 m target (nAttack_hit only on a hit, :32771); at 1.0 s i = 3, Yield 0.1 (:33154): standby at 1.1 s",
    "cues": [
      [0, "voice", "circleShot1|circleShot2"],
      [0, "fx", "circleShot_ring"],
      [0.6, "fx", "circleShot", {"y": 1.7}],
      [0.733, "fx", "circleShot", {"y": 2.2}],
      [0.866, "fx", "circleShot", {"y": 1.7}]
    ]
  },
  "extravagance": {
    "why": "Rabbit.cs RPC_extravagance (:39711-40115), Extravagance (one rank): extravagance (0.2 fade, Once, :40003-40006) and Effects/extravagance_ring at the hero, hero rotation (createEffect :40015-40033; EffectControl life 1 + 1, followPosition; two ImageEmitters, three RingEmitters and two Shuriken systems, Gil coins and star5 sparks, read from TTO's copy: SHURIKEN_FROM_TTO, the part; its own Sounds/extravagance_ring) at 0; no voice (none loaded, BB or TTO: pseudo/Rabbit.c:8226 names only the effect); the fee (:40056-40074) and the motion blur at 0.5 s (:39859) left out; Yield 0.5, 0.2 (:40100, :40095): at 0.7 s atkUp 5 for chaAdjust(6) (:39902; CharacterControl.cs:33176-33180 deltaAtk only, no look) and the '+N atk' message (:39907) left out; Yield 0.3 (:40107): standby at 1.0 s",
    "cues": [
      [0, "fx", "extravagance_ring"]
    ]
  },
  "mall1": {
    "why": "Rabbit.cs RPC_mall (:33223-33734), Mall rank 2: mall1 (0.2 fade, looped, :33439-33444), no voice, Effects/mall + Math.div(Skin, 100) (:33507: mall1-mall5 by the outfit's colour number, RabbitEquipment.cs:1474-1492 Skin / 100 = 1-5; every wardrobe Rabbit outfit has colours 1-5) at the hero, LookRotation(forward, the ground normal) = the hero's on the flat floor (:33479-33531): the stall mesh Rabbit_mall, its Rabbit_mall script Init (:33542-33553; Rabbit_mall.cs:37-62: no serialised fields; its OnGUI draws the buy button for other players only, :163, and destroys the stall once the owner's actionState leaves attack / mallSetup / mallOpen, :110-137); the MallGui setup window (:33569-33641) held until the player opens the shop: the SEQ rule's 3 s for a hold (mall1*@3); then RPC_mall_open (MallGui.cs:4965) mall2, sit (@Mall:sit); the stall lives to the close: kill 7.95 (the tile's 3 + 2 + 3 s less the page's margin)",
    "cues": [
      [0, "fx", "mall1|mall2|mall3|mall4|mall5", {"pick": "color", "kill": 7.95}]
    ]
  },
  "mall2": {
    "why": "Rabbit.cs RPC_mall_open (:33739-33891), started by MallGui on the server's open reply (MallGui.cs:4957-4977): myCommand mallOpen, mall2 cut in, looped (:33857-33863, the SEQ's mall2*!); TTO1102's copy also plays Voices/mallOpen here (pseudo/Rabbit.c:12915-13000: PlayerPrefs pvoice, the clip loaded from voices/mallOpen; BB's rip has mallOpen.wav, which BB's code never plays: open question 5); Yield 2 (:33871): sit (@Mall:sit)",
    "cues": [
      [0, "voice", "mallOpen"]
    ]
  },
  "@Mall:sit": {
    "why": "Rabbit.cs RPC_mall_open case 2 (:33834-33839): 2 s after mall2, sit with a 0.2 fade, looped (the SEQ's sit*~), held until the player moves away: the SEQ rule's 3 s; then RPC_mall_close (Rabbit.cs:10876-10919: standby; the stall's script destroys it, Rabbit_mall.cs:110-119), which in TTO1102 plays Voices/mallClose (pseudo/Rabbit.c:35591-35700; BB's rip has mallClose.wav, never played by BB: open question 5) at the close, 2.95 s into this step (the step's 3 s less the page's margin)",
    "cues": [
      [2.95, "voice", "mallClose"]
    ]
  }
}
```

## Page lines

- `SEQ.rabbit`:
  - "Bounce: bounce1@9.5 bounce2!" (was "Bounce: bounce1 bounce2").
  - "Mall: mall1*@3 mall2*!@2 sit*~@3" (was "Mall: mall1* mall2*").
  - The other single-clip skills need no SEQ line: Maim Shot, Gil Shot, Diamond Shot (pool tiles), Gorgon Shot, Backpack,
    Four Shot, Circle Shot and Extravagance.
- `wardrobe_skill_icons.py`:
  - `CLIP_SKILLS["rabbit"] = {"maim": ["maimShot"], "gilShot": ["gilShot", "diamondShot"]}`.
  - `RANK_ICONS["rabbit"] = {"backpack": "rabbit_backpack2", "circleShot": "rabbit_circleShot2", "fourShot":
    "rabbit_fourShot2", "gorgonShot": "rabbit_gorgonShot2", "mall": "rabbit_mall2"}` (Read this first 8).
- **Data:** `SHURIKEN_FROM_TTO["rabbit"] = ["extravagance_ring"]` (P1). The `fxparts/rabbit.js` no-op `Rabbit_mall` (P2).
  The inventory additions: mall1-5, and extravagance_ring and Rabbit_mall as built.
- `wardrobe_fx_check.py` needs nothing new: every option used is in OPTS, and `hideProp` "hero" / "R" are in
  HIDE_TARGETS.

## Parts summary

| part | what | for |
|---|---|---|
| P1 extravagance_ring Shuriken | `SHURIKEN_FROM_TTO["rabbit"] = ["extravagance_ring"]`, no SHURIKEN_MAT (graft_by_material; proved in memory, probe2.txt) | Extravagance |
| P2 Rabbit_mall | no layout (zero field bytes); a no-op part in `fxparts/rabbit.js`; inventory: mall1-5 listed, Rabbit_mall built | Mall |

There is no stand-in for the missing kneeShot_hit (item 7).

## Bible findings to offer the user

1. `kneeShot_hit` is loaded by BB's and TTO's Knee Shot (Rabbit.cs:9682) but is in neither game's data. So a knee shot
   (20 % at LCK 1) draws no hit flash at all. `fourShot_hit` and `circleShot_hit` have RPCs (:10744, :10794) but are never
   called and do not exist.
2. **Bounce timeline (rank 2):**
   - The 8 s timer starts 0.9 s after the press (:21073, after Yield 0.5 + 0.4).
   - The landing effect and the bounce0 voice come at 8.9 s.
   - The Rabbit reappears and plays bounce2 at 9.5 s.
   - From the Above's stomp is at 9.9 s, and standby at 10.3 s.
   - Rank 1 is 4.9 / 5.5 / 5.9 / 6.3 s.
   - With From the Above, the landing shows fromTheAbove_ring **instead of** the bounce2 effect (:21820-21887).
3. **Shot times:** Maim Shot fires at 0.5 s and hits at 0.6 s. Gil Shot and Diamond Shot fire and hit at 1.0 s. Gorgon
   Shot fires at 1.4 s. Four Shot's shots come at 0.4 / 0.7 / 1.0 / 1.3 s. Circle Shot's pulses come at 0.733 / 0.866 /
   1.0 s.
4. **Medical shots under Rapid Trance:**
   - They play the gilShot clip and say no voice at the cast.
   - They fire at 1.0 s instead of 1.4 s (:28548-28555, :28730-28735).
   - The reference says only "no cast bar, no cooldown".
5. **Mall:**
   - The stall model follows the armour colour (mall1-5, :33507).
   - BB never plays its recorded mallOpen / mallClose voices; TTO plays both (TTO1102 :12933, :35614).
   - After opening, the Rabbit sits 2 s later (:33871).

## Open questions (recommended answers)

1. **Bounce's 8 s in the air (rank 2):** keep the hero hidden from 0.9 s to 9.5 s on the tile? Recommended: yes. It is the
   top rank's look and under the 10 s cut. Rank 1's 4 s would be "bounce1@5.5" with the hide kill 4.6 and the landing cues
   at 4.9.
2. **From the Above's air shots while airborne:** leave them out? Recommended: yes. They need the attack key, like the
   Chameleon's and the Mole's player-input branches. Only the passive's landing ring and stomp are automatic.
3. **Rapid Trance's medical shots on gilShot:** pool members? Recommended: no.
   - Immune, Boost, Heat and Life Shot already get their tiles on medicalShot (skills_b's).
   - Rapid Trance is a temporary state from a 12 s active, not a passive.
   - One tile per skill is kept. Offer the variant as a later tile if wanted.
4. **Knee Shot:** maimShot_hit at `p` 0.8, with nothing on the other 20 %? Recommended: yes. That is the game's roll at
   LCK 1 (lckAdjust(20) = 20, the Cat's decisions 32 and 40 convention), and kneeShot_hit does not exist. No stand-in.
5. **Mall voices:** cue TTO's mallOpen / mallClose (BB's own recordings, never wired in BB)? Recommended: yes. TTO wires
   BB's files, as the Sheep's decision 10 took TTO's voice fixes.
   - Against: the Bat / Bison "chat voices stay BB's" (there TTO swapped BB's voices for new ones; here BB has none).
   - If the planner prefers BB's silence, drop the `mall2` entry and the `@Mall:sit` entry.
6. **Mall's holds:** 3 s for the setup window and 3 s for the sit? Recommended: yes, the SEQ rule for a hold until the
   player acts. That makes an 8 s tile, with the stall's kill 7.95.
7. **The rank-IV icons:** apply the RANK_ICONS override for Backpack, Circle Shot, Four Shot, Gorgon Shot and Mall?
   Recommended: yes (the Bible cards' own icons). Tell the lead that seven more Rabbit tiles outside this scope show the
   same "4" pick and need a look.
8. **maimShot_hit's `kill` 1:** the game never destroys it (no EffectControl). Recommended: keep the kill. Its burst ends
   at 0.8 s, and without an EffectControl the page has no end for it on a looping tile.
9. **Backpack's gun:** hide only the meshes (`hideProp` R, no `all`)? Recommended: yes. The code switches off mWep1's
   MeshRenderers only (:30987-31014), so a weapon's own particles stay.

## Verification (13/11/2026)

Checker, office PC, research only. Probes in `C:\work\12tails-wardrobe\checks\fx_rabbit_research\verify\` (git-ignored):
`probe_a.json` (`wardrobe_fx.py rabbit --probe` of 30 names: every effect cued here, plus backpack_ring, backpack_hit,
bounce2, kneeShot_hit, mall6, medicalShot_ring), `summ.py`, `graft.py` -> `graft.txt` (P1 in memory), `tto_probe.txt`
(`wardrobe_fx_tto.py rabbit --probe kneeShot_hit,fourShot_hit,circleShot_hit`), `cues_a.json` (the body's block, parsed),
`cues_a_fixed.json` (the corrected block below, checked with json.loads). The Verification wins over the body.

**What holds (re-derived, no change):**
- **Clips and lengths:** bounce1 0.9, bounce2 1.1, maim 1.0, gilShot 1.7, gorgonShot 2.0, backpack 1.2, fourShot 1.8,
  circleShot 1.3, extravagance 1.2, mall1 0.8, mall2 1.2 and sit 0.8 (wardrobe/data/rabbit/clips.json). Every cue key is
  a real clip, or `@Mall:sit` (a valid SEQ key).
- **Timings: every coroutine's waits added up again.**
  - Bounce: 0.5 + 0.4, then FixedUpdate until now > the timer at 8.9 s, then 0.6 / 0.4 / 0.4 (Rabbit.cs:21357, :21375,
    :21379, :21073, :21108, :21906-21910; RPC_bounce0's cases :21543-21688). The stomp is #421 only (:21608).
  - Maim Shot: 0.5 / 0.1 / 0.1 / 0.1 (:23608-23628).
  - Gil Shot: 1 / 0.2 / 0.1 (:30769-30775). Diamond Shot: the same (:38678-38684).
  - Gorgon Shot: 1.3 / 0.1 / 0.2 / 0.2 (:30029-30042).
  - Backpack: 0.2 / 0.1 / 0.2 x 3 / 0.1 (:31666-31695).
  - Four Shot: 0.4, then 0.3 per shot (:32436, :32442). The fire points and directions per shot index are right
    (:32233-32300).
  - Circle Shot: 0.4 / 0.2, then 0.133 per pulse, then 0.1. The effects come at i = 0, 1, 2, at 1.7 + 0.5 x (i % 2) m
    up (:32903-32921, :33141-33157).
  - Extravagance: 0.5 / 0.2 / 0.3 (:40095-40107).
  - Mall: RPC_mall_open's Yield 2 (:33871). In TTO1102, mallOpen plays before mall2 (pseudo/Rabbit.c:12960-13040).
- **Names: every effect, voice and sound named exists.**
  - The probe reads every cued effect, and mall1-5. KeyError for kneeShot_hit and mall6.
  - TTO's catalog lacks kneeShot_hit, fourShot_hit and circleShot_hit.
  - Every voice is in the rip's `voices/`. Every effect's own AudioSource clip is in `sounds/`.
  - EffectControl life / afterLife / followPosition / followState match the body for every effect. followState acts only
    within `life` (EffectControl.cs:194-232), so the rings' cut claim holds.
  - bounce1's effectRotationMode 3 (faceUp) is drawn by fxparts/control.js:88.
- **Positions:**
  - The ray hits on the Bat decision 4 body: maim (0, 0.612, 9.7) and gorgon (0, 0.692, 9.7). The gorgon contact is the
    r 1 sphere from (0, 1, 1) along the (0, 1, 0) -> (0, 0.6, 10) direction (:29545-29561): its centre is 1.3 m short at
    z 8.7, y 0.692.
  - The pitch: atan(0.4 / 10) = 2.29 deg.
  - Four Shot's ClosestPointOnBounds is (0, 1, 9.7).
- **Rank picks and passives:** as the body says (RabbitSkill.cs:1361-1395: Ten Shot #433 is an active skill whose
  learned rank adds +10 to Four Shot and Circle Shot, :32374, :32732). Knee Shot: lckAdjust(20) at LCK 1 =
  floor(100 x 20.2 / 100.2) = 20 (CharacterControl.cs:20658-20668).
- **No TTO skill is in scope.** The page lines are right:
  - SEQ syntax: `seqStep`'s SEQ_ALT regex parses both lines.
  - `"pick": "color"` works for every Rabbit outfit: all 23 outfits have colours 1-5.
  - RANK_ICONS: the current HD icons are byte-equal to rabbit_mall4, backpack4, circleShot4, fourShot4 and gorgonShot4.
    The Bible cards use `<skill>2` (12t_projects/bible/index.html). wardrobe_skill_icons.py:126 applies RANK_ICONS to
    any skill.
  - Diamond Shot's top icon diamondShot5 is byte-equal to the card's diamondShot1.
- **P1 is proved again** (graft.txt): node 3 is grafted from TTO node 1 (Gil), node 4 from TTO node 4 (star5).

**Findings:**

1. **The Mall's voices: drop both cues (reverses open question 5).**
   - BB loads no voice in RPC_mall / RPC_mall_open / RPC_mall_close (no "Voices/mall" string anywhere in BB's
     DecompiledSource). TTO1102 wires BB's own unused mallOpen / mallClose recordings (pseudo/Rabbit.c:12933, :35614).
   - That is the Cat's case: BB's unused rollTheDice / inSight recordings, which TTO plays, were not taken. "TTO's
     voice only where BB's file is missing; TTO's [added voice] is a behaviour change, not a fix" (plans/fx_cat/
     decisions.md 34, line 114). Also Monkey decision 47: BB is the content.
   - **Corrected:** no `mall2` entry and no `@Mall:sit` entry.
     - The sit step then falls back to the plain `sit` key, which has no entry (attacks_emotes.md:343: "No entry for
       sit"), so it stays silent.
     - The SEQ line is unchanged: "Mall: mall1*@3 mall2*!@2 sit*~@3".
     - Counts: 9 cue keys, 37 cues.
     - "What is ready: Voices" loses mallOpen and mallClose.
   - Bible finding 5 stays as written (BB never plays them, TTO plays both).
2. **P2's precedent is the Bison's Bison_overLord, not Chameleon_campFire.**
   - Bison_overLord is a no-op `api.part("Bison_overLord", () => null)` (fxparts/bison.js:42), with
     `"Bison_overLord": []` in LAYOUTS (wardrobe_fx.py:159).
   - Chameleon_campFire has a 4-byte LAYOUT (wardrobe_fx.py:171) and no part (fxparts/chameleon.js:11-12).
   - The no-op `api.part("Rabbit_mall", () => null)` in `fxparts/rabbit.js` stands. No LAYOUTS entry is needed: a script
     with zero field bytes passes (wardrobe_fx.py:618-620), and the probe read mall1-5 without one.
3. **Mall's stall: two facts the body missed** (no cue change, add to Bible finding 5):
   - In BB's data, mall4 and mall5 both use mall3's material `Rabbit_mall3` (probe_a.json: mall1 Rabbit_mall1, mall2
     Rabbit_mall2, mall3-5 Rabbit_mall3). So colours 3, 4 and 5 show the same stall.
   - The stall prefab is loaded once and cached (`if (!this.zXXPFPINyb)`, Rabbit.cs:33500-33507). The session's first
     Mall fixes the stall's colour, even if the armour colour changes later.
   - The page's pick by the current colour is the look of a first Mall, so it stays as written.
   - The stall's root sits at (0, 50, -64) in the prefab. Instantiate (and the page's root placement,
     index.html Fx ctor) overrides that, and its mesh child is at (0, 0.05, 0): a 1.4 m mat on the floor.
4. **`CLIP_SKILLS["rabbit"]` needs only `"maim": ["maimShot"]`.**
   - Once the cue file holds the gilShot pool, wardrobe_skill_icons.py:115-133 gives Gil Shot and Diamond Shot each
     their icon on the gilShot clip anyway.
   - The `"gilShot": [...]` line gives the same index. It is redundant and harmless: drop it for the shorter line.
   - **Corrected:** `CLIP_SKILLS["rabbit"] = {"maim": ["maimShot"]}`.
5. **Cross-report: Bounce's sequence shape.**
   - effect_only.md proposes "bounce1@9.5 bounce2@1.4" for Bounce and for its From the Above tile (:49, :71, :272,
     :379, :498), holding bounce2 0.3 s past its 1.1 s end so that fromTheAbove_ring's 2 s life (8.9 -> 10.9) ends
     inside the tile.
   - **Call: keep this report's "Bounce: bounce1@9.5 bounce2!", and use the same steps for From the Above.**
   - Reason: skill tiles play once by default, and the idle tail shows an effect that outlives its tile; the loop toggle
     cutting it is the page-wide limit (Cat decision 22, Monkey decision 8). In the game, the Rabbit is at standby at
     10.3 s and idles while the ring ends (:21683-21698). A frozen last frame of bounce2 is not that.
   - The attacks_emotes report gives the Bounce owner this sequence's shape (attacks_emotes.md:160, :624). The lead should
     write one shape for both lines.
6. **Missed in this scope: nothing.**
   - Every RPC that plays these 11 clips is covered. effect_only.md's 88-RPC census, rows bounce ... mall, agrees, and
     TTO1102 has the same coroutines.
   - Every passive that changes a look is in: #421, #402, #423. #403, #433 and #413 change no look.
   - `bounce2`, `backpack_ring` and `backpack_hit` are rightly not cued (passive-off look, and hits out of reach).
7. **Outside this report, for the lead: `plans/fx_rabbit/skills_b.md` does not exist.**
   - Its researcher's scratch stops at 10:37 (`checks\fx_rabbit_research\skills_b\`: flows, probes, `pool.json` /
     `pool_pretty.txt`), but no report was written. Nothing was verified for it.
   - Its scope is uncued: effect_only.md:96-121 rows owned by "skills" that are not this report's:
     - the mix channel (mix1 / mix2) and mix3 / mix4: Mix, Shake, Miracle Blend (+ Extra Potion #412, Miracle Drop
       #422), Sticky Gum, Acidic Field, Healing Field;
     - Stat Scan; the four medical shots (Immune, Boost, Heat, Life Shot) on medicalShot; Rapid Trance;
     - Truce Trading & Co. (with its cheer / cry outcomes); Shooting Array; Millionaire; Ten Shot; Contract (on
       truceTrading).
   - Re-run that researcher, then its checker.

**Corrected paste-ready block** (replaces the body's in full; finding 1: `mall2` and `@Mall:sit` removed, the
`mall1` why updated):

```json
{
  "bounce1": {
    "why": "Rabbit.cs RPC_bounce (:20867-21425), Bounce rank 2 (sLv 2), From the Above #421 on (passives on): bounce1 cut in (PlayAnimation(bounce1, 0), Once, :21238-21241; the page's first-step fade stays, Cat decision 2) and voice bounce1 / bounce2 (Random.Range(0, 2) :21279-21338, PlayOneShot :21383 / :21363) at 0; Yield 0.5 (:21357): Effects/bounce1 Instantiated at the hero, hero rotation (:21019-21031; EffectControl life 0.5, its own Sounds/bounce1); Yield 0.4 (:21375): at 0.9 s (bounce1's last frame) addStatus hide (level 1, 4 x sLv + 1 = 9 s, :21068), every Renderer of the hero off (CharacterControl.cs:32818-32853: the page's whole-hero hideProp), mBounceTimer = now + 4 x sLv = 8 s (:21073); each FixedUpdate until Time > mBounceTimer (:21108; the steering by the arrow keys :21136-21190 and the From the Above air shot on the attack key, :8944 / :22100-22260, left out: the player's input): at 8.9 s RPC_bounce0 (:21114; :21496-21925): voice bounce0 (one file, :21796-21808) and, #421 learned, Effects/fromTheAbove_ring at the hero, hero rotation (:21820-21840; life 2, its own Sounds/fromTheAbove) in place of Effects/bounce2 (the else branch :21859-21875, not drawn with the passive); Yield 0.6 (:21908): at 9.5 s removeStatus hide (:21566, the hero shown again: CharacterControl.cs:14547-14573) and bounce2 cut in (:21571, the SEQ's bounce1@9.5 bounce2!)",
    "cues": [
      [0, "voice", "bounce1|bounce2"],
      [0.5, "fx", "bounce1"],
      [0.9, "hideProp", "hero", {"kill": 8.6}],
      [8.9, "voice", "bounce0"],
      [8.9, "fx", "fromTheAbove_ring"]
    ]
  },
  "maim": {
    "why": "Rabbit.cs RPC_maimShot (:22949-23697), Maim Shot rank 4 + Knee Shot #402 (passives on): maim (0.2 fade, Once, :23486-23489) and voice maimShot1 / maimShot2 (Random.Range(0, 2) :23527-23586, PlayOneShot :23622 / :23625) at 0; Yield 0.5 (:23610): moveSpeed -1 (the step back, left out: the hero does not travel), firePos = position + up, fireDir = the target's collider.bounds.center - position - up (:23111-23127: from (0, 1, 0) to the 10 m target 0.6 m up, pitch atan(0.4 / 10) = 2.29 deg), Effects/maimShot_fire at firePos, FromToRotation(forward, fireDir) (:23133-23156; life 1, its own Sounds/nAttack); Yield 0.1 (:23608): at 0.6 s the Raycast from firePos along fireDir (16 + 5 x Combo m, :23211-23216) meets the standard target body at (0, 0.612, 9.7) (checks/fx_rabbit_research/skills_a/hitpoints.txt): RPC_nAttack_hit there (:23224; Rabbit.cs:9112-9147 Effects/nAttack_hit, hero rotation) and, the hit landing, Knee Shot's roll Random.Range(0, 100) < lckAdjust(20) = 20 at LCK 1 (:23256-23273; CharacterControl.cs:20658: floor(100 x 20.2 / 100.2)): 20 % RPC_kneeShot_hit (:23294; Effects/kneeShot_hit, :9682, is in neither BB's data nor TTO's catalog: nothing drawn), 80 % RPC_maimShot_hit (:23314; Effects/maimShot_hit at the hit, LookRotation(forward) = the hero's, :9639-9649; no EffectControl, one ImageEmitter burst of 0.3 + 0.5 s, so the game never destroys it: kill 1 for the page); the maim status (getDebuff(3), :23337-23348) draws nothing; Yield 0.1 x 2 (:23628, :23620): standby at 0.8 s (:23402-23417)",
    "cues": [
      [0, "voice", "maimShot1|maimShot2"],
      [0.5, "fx", "maimShot_fire", {"y": 1, "rot": [2.29, 0, 0]}],
      [0.6, "fx", "nAttack_hit", {"d": 9.7, "y": 0.61}],
      [0.6, "fx", "maimShot_hit", {"d": 9.7, "y": 0.61, "p": 0.8, "kill": 1}]
    ]
  },
  "gilShot": {
    "why": "The gilShot clip is played by RPC_gilShot (Rabbit.cs:30539) and RPC_diamondShot (:38454), each with a 0.2 s fade, Once, and by RPC_medicalShot only under Rapid Trance's status (:28548-28552: the four medical shots' state variant, no member: their tiles are on medicalShot, open question 3); TTO1102's three coroutines name it the same (pseudo/Rabbit.c:7498, :9678, :13403): one tile each (poolChains), the clip alone",
    "skills": {
      "gilShot": {
        "why": "Rabbit.cs RPC_gilShot (:30125-30835), Gil Shot rank 4 + Diamond Shot #403 (damage only): gilShot (0.2 fade, Once, :30539-30542), voice gilShot1 / gilShot2 (Random.Range(0, 2) :30580-30639) and Effects/gilShot_ring at the hero, hero rotation (createEffect :30720-30736; EffectControl life 0.5 + afterLife 1, followPosition, followState; its own Sounds/gilShot) at 0; Yield 1 (:30769): at 1.0 s moveSpeed -1 (left out), firePos = position + up, fireDir to the target's bounds centre (:30287-30303: pitch 2.29 deg), Effects/gilShot_fire at firePos, FromToRotation(forward, fireDir) (:30309-30332; life 1, its own Sounds/nAttack), the Raycast (16 + 5 x Combo m, :30364-30369) meets the target body at (0, 0.612, 9.7) (hitpoints.txt): RPC_gilShot_hit there (:30377; Effects/gilShot_hit, Quaternion.identity, :10502-10512; life 1, its own Sounds/gilShot_hit); Yield 0.2, 0.1 (:30771, :30775): standby at 1.3 s",
        "cues": [
          [0, "voice", "gilShot1|gilShot2"],
          [0, "fx", "gilShot_ring"],
          [1, "fx", "gilShot_fire", {"y": 1, "rot": [2.29, 0, 0]}],
          [1, "fx", "gilShot_hit", {"d": 9.7, "y": 0.61}]
        ]
      },
      "diamondShot": {
        "why": "Rabbit.cs RPC_diamondShot (:38030-38720), Diamond Shot (one rank): gilShot (0.2 fade, Once, :38454-38457), Effects/diamondShot_ring at the hero, hero rotation (createEffect :38538-38556; life 0.5 + 1, followPosition, followState; its own Sounds/diamondShot) and voice diamondShot1 / diamondShot2 (Random.Range(0, 2) :38599-38658, PlayOneShot :38694 / :38690) at 0; Yield 1 (:38680): at 1.0 s firePos = position + up, fireDir to the target's bounds centre (:38181-38197: pitch 2.29 deg), Effects/diamondShot_fire at firePos, FromToRotation(forward, fireDir) (:38203-38226; life 1, its own Sounds/nAttack), the Raycast (:38258-38263) meets the target body at (0, 0.612, 9.7): RPC_diamondShot_hit there (:38271; Effects/diamondShot_hit, identity, :11405-11415; its own Sounds/gilShot_hit), then RPC_AddEffectDamage 1000 (:38322, the number only); Yield 0.2, 0.1 (:38678, :38684): standby at 1.3 s",
        "cues": [
          [0, "fx", "diamondShot_ring"],
          [0, "voice", "diamondShot1|diamondShot2"],
          [1, "fx", "diamondShot_fire", {"y": 1, "rot": [2.29, 0, 0]}],
          [1, "fx", "diamondShot_hit", {"d": 9.7, "y": 0.61}]
        ]
      }
    }
  },
  "gorgonShot": {
    "why": "Rabbit.cs RPC_gorgonShot (:29387-30120), Gorgon Shot rank 2: gorgonShot (0.2 fade, Once, :29859-29862), voice gorgonShot1 / gorgonShot2 (Random.Range(0, 2) :29900-29959) and Effects/gorgonShot_ring at the hero, hero rotation (createEffect :29968-29986; life 3 + 1, no followState; its own Sounds/gorgonShot) at 0; the local player's motion blur (:30009) left out; Yield 1.3 (:30042): firePos = position + TransformDirection(0, 1, 1), fireDir to the target's bounds centre (:29545-29561: pitch 2.29 deg); Yield 0.1 (:30029): at 1.4 s moveSpeed -3 (the recoil, left out), Effects/gorgonShot_fire at firePos, FromToRotation(forward, fireDir) (:29594-29617; life 1, its beam mesh Rabbit_gorgonShot 1 m ahead with its 0.4 s root clip and AlphaTimer), SphereCastAll radius 1, 36 m (:29644): its contact with the target body at (0, 0.692, 9.7) (hitpoints.txt): RPC_gorgonShot_hit there (:29677; Effects/gorgonShot_hit, LookRotation(forward), :10452-10462; life 1); the petrify status (:29699-29710) draws nothing here; Yield 0.2, 0.2 (:30040, :30033): standby at 1.8 s",
    "cues": [
      [0, "voice", "gorgonShot1|gorgonShot2"],
      [0, "fx", "gorgonShot_ring"],
      [1.4, "fx", "gorgonShot_fire", {"d": 1, "y": 1, "rot": [2.29, 0, 0]}],
      [1.4, "fx", "gorgonShot_hit", {"d": 9.7, "y": 0.69}]
    ]
  },
  "backpack": {
    "why": "Rabbit.cs RPC_backpack (:30840-31760), Backpack rank 2 + Big Bag #423 (passives on): backpack cut in (PlayAnimation(backpack, 0), Once, :31428-31433; the page's first-step fade stays) and voice backpack1 / backpack2 (Random.Range(0, 2) :31499-31562, PlayOneShot :31681 / :31674) at 0; Yield 0.2 (:31695): mWep1's MeshRenderers off (:30987-31014: the gun, the page's slot R; its weapon_fx particles stay) and, #423 learned, Effects/bigbag_ring at the hero, hero rotation (createEffect :31024-31053; EffectControl life 0.8, followPosition, followState; the bag mesh Rabbit_bigbag swung by its 0.83 s root clip, a trail, a ring; its own Sounds/bigbag_ring) in place of backpack_ring (Euler(270, 90, 0), the else branch :31072-31090); Yield 0.1 (:31677): three pulses at 0.3, 0.5, 0.7 s (FindAreaTarget 3 m with Big Bag, :31588; Yield 0.2 :31666), none reaching the 10 m target (backpack_hit only on a hit, :31632); at 0.9 s j = 3, Yield 0.1 (:31685): standby at 1.0 s and the gun shown again (:31366-31394): hideProp R from 0.2 for 0.8 s",
    "cues": [
      [0, "voice", "backpack1|backpack2"],
      [0.2, "hideProp", "R", {"kill": 0.8}],
      [0.2, "fx", "bigbag_ring"]
    ]
  },
  "fourShot": {
    "why": "Rabbit.cs RPC_fourShot (:31823-32500), Four Shot rank 2 + Ten Shot #433 (damage only): fourShot (0.2 fade, Once, :32022-32027) and voice fourShot1 / fourShot2 (Random.Range(0, 2) :32093-32156, PlayOneShot :32432 / :32427) at 0; Yield 0.4 (:32442), then one shot every 0.3 s (Yield 0.3 :32436) at 0.4, 0.7, 1.0, 1.3 s, each Effects/fourShot_fire at position + TransformDirection(...) with Quaternion.identity (:32308-32326; life 1, its own Sounds/fourShot_fire): forward (0.15, 0.85, 0.85) :32246, back (0.15, 1, -0.85) :32263, left (-0.65, 0.65, 0) :32280, right (0.85, 0.75, -0.2) :32297; each a FindAngleTarget cone of 24 m, 70 deg (:32355): only the forward one holds the 10 m target: RPC_nAttack_hit at its collider.ClosestPointOnBounds(position + up) = (0, 1, 9.7) (:32380-32390; nAttack_hit, hero rotation); at 1.6 s i = 4: standby (:32162-32193)",
    "cues": [
      [0, "voice", "fourShot1|fourShot2"],
      [0.4, "fx", "fourShot_fire", {"d": 0.85, "x": 0.15, "y": 0.85}],
      [0.4, "fx", "nAttack_hit", {"d": 9.7, "y": 1}],
      [0.7, "fx", "fourShot_fire", {"d": -0.85, "x": 0.15, "y": 1}],
      [1, "fx", "fourShot_fire", {"x": -0.65, "y": 0.65}],
      [1.3, "fx", "fourShot_fire", {"d": -0.2, "x": 0.85, "y": 0.75}]
    ]
  },
  "circleShot": {
    "why": "Rabbit.cs RPC_circleShot (:32503-33220), Circle Shot rank 2 + Ten Shot #433 (damage only): circleShot (0.2 fade, Once, :32945-32948), voice circleShot1 / circleShot2 (Random.Range(0, 2) :32998-33057) and Effects/circleShot_ring at the hero, hero rotation (createEffect :33066-33084; life 1 + 1, followPosition, followState: the 1.1 s standby comes after its life; its own Sounds/circleShot) at 0; the camera's AutoZoom (:33119, :32894) and motion blur (:32663) left out; Yield 0.4 (:33157), Yield 0.2 (:33143): from 0.6 s three Effects/circleShot at position + (1.7 + 0.5 x (i % 2)) up, hero rotation (:32903-32921): 1.7, 2.2, 1.7 m up at 0.6, 0.733, 0.866 s (Yield 0.133 :33141), each pulse's FindAreaTarget of 8 m (:32727, at 0.733, 0.866, 1.0 s) short of the 10 m target (nAttack_hit only on a hit, :32771); at 1.0 s i = 3, Yield 0.1 (:33154): standby at 1.1 s",
    "cues": [
      [0, "voice", "circleShot1|circleShot2"],
      [0, "fx", "circleShot_ring"],
      [0.6, "fx", "circleShot", {"y": 1.7}],
      [0.733, "fx", "circleShot", {"y": 2.2}],
      [0.866, "fx", "circleShot", {"y": 1.7}]
    ]
  },
  "extravagance": {
    "why": "Rabbit.cs RPC_extravagance (:39711-40115), Extravagance (one rank): extravagance (0.2 fade, Once, :40003-40006) and Effects/extravagance_ring at the hero, hero rotation (createEffect :40015-40033; EffectControl life 1 + 1, followPosition; two ImageEmitters, three RingEmitters and two Shuriken systems, Gil coins and star5 sparks, read from TTO's copy: SHURIKEN_FROM_TTO, the part; its own Sounds/extravagance_ring) at 0; no voice (none loaded, BB or TTO: pseudo/Rabbit.c:8226 names only the effect); the fee (:40056-40074) and the motion blur at 0.5 s (:39859) left out; Yield 0.5, 0.2 (:40100, :40095): at 0.7 s atkUp 5 for chaAdjust(6) (:39902; CharacterControl.cs:33176-33180 deltaAtk only, no look) and the '+N atk' message (:39907) left out; Yield 0.3 (:40107): standby at 1.0 s",
    "cues": [
      [0, "fx", "extravagance_ring"]
    ]
  },
  "mall1": {
    "why": "Rabbit.cs RPC_mall (:33223-33734), Mall rank 2: mall1 (0.2 fade, looped, :33439-33444), no voice, Effects/mall + Math.div(Skin, 100) (:33507: mall1-mall5 by the outfit's colour number, RabbitEquipment.cs:1474-1492 Skin / 100 = 1-5; every wardrobe Rabbit outfit has colours 1-5) at the hero, LookRotation(forward, the ground normal) = the hero's on the flat floor (:33479-33531): the stall mesh Rabbit_mall, its Rabbit_mall script Init (:33542-33553; Rabbit_mall.cs:37-62: no serialised fields; its OnGUI draws the buy button for other players only, :163, and destroys the stall once the owner's actionState leaves attack / mallSetup / mallOpen, :110-137); the MallGui setup window (:33569-33641) held until the player opens the shop: the SEQ rule's 3 s for a hold (mall1*@3); then RPC_mall_open (MallGui.cs:4965) mall2 and, 2 s later, sit (no cue entries: BB plays no voice there, the mallOpen / mallClose voices are TTO1102's behaviour change, Cat decision 34; the sit emote has no entry of its own, attacks_emotes.md:343); the stall lives to the close: kill 7.95 (the tile's 3 + 2 + 3 s less the page's margin)",
    "cues": [
      [0, "fx", "mall1|mall2|mall3|mall4|mall5", {"pick": "color", "kill": 7.95}]
    ]
  }
}
```

**Corrected page lines:**
- SEQ unchanged: "Bounce: bounce1@9.5 bounce2!", "Mall: mall1*@3 mall2*!@2 sit*~@3".
- `CLIP_SKILLS["rabbit"] = {"maim": ["maimShot"]}` (finding 4).
- RANK_ICONS and P1 as in the body.
- P2 in `fxparts/rabbit.js`, after the Bison_overLord pattern (finding 2).
