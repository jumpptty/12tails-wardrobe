<!-- Saved by the lead from the researcher's returned text: its Write was refused. -->

Summary: all 10 clips are traced, with file:line, through the opaque predicates and the timed waits.
- **Pools:** two.
  - cast3: the eight cast-bar skills after the shared RPC_cast1 channel. Three more skills play cast3 straight from the key press, each on its own tile: Honor, 12th Kingdom Knight and Bubble Burst.
  - flyingShield: Flying Shield and Homing Shield.
- **Diving Press #443 (passives on):** Whale Wave and Mal Storm play divingWave / divingStorm, so the malStorm clip only plays at a lower rank.
- **grandTide0:** no effect or voice of its own.
- **Cues:** 10 keys, 91 cues.
- **Missing parts (P1-P4):** whale_kingdomKnight (a layout and the knights' rise), Whale_flyingShield, Whale_homingShield, and a cue option for Mal Storm's random bolt ring.
- **Open questions:** 14, each with a recommended answer.

# Whale effects + sounds research: skills_a (ten skill clips)

Researcher `skills_a`, 2026-11-13 (office PC).
- **Scope:** the clips bowlingWhale1, bowlingWhale2, cast1, cast2, cast3, divingStorm, divingWave, flyingShield, gobble and grandTide0, and every skill that plays them.
- **Method:** research only (recipe steps 1-3).
- **Line numbers:** `C:\Users\Jump\Desktop\12tails\DecompiledSource\Whale.cs` (the home PC's `D:\12tails\...`) unless another file is named. "TTO" means `DecompiledSource_TTO_2026-11-02\pseudo\Whale.c`.
- **Units:** times are seconds from the start of the clip the cue is keyed by. d = metres ahead, x = metres right, y = metres up.

## Read-only probes

Everything is in `C:\work\12tails-wardrobe\checks\fx_whale_research\skills_a\` (git-ignored). Nothing there writes outside that folder.

- **Coroutine reads:**
  - `cond.py <file> <from> <to>` works out the opaque predicates (`if (a - b == c)` becomes TRUE / FALSE).
  - `f.sh <from> <to>` does the same with the junk lines dropped (`F=<file>` for another .cs).
  - `g.sh` keeps only the flow lines: cases, gotos, waits, loads, effects, statuses.
  - Flow dumps:
    - `flow_RPC_cast1.txt` (clip_flow.js), `cast1_a.txt`, `cast1_b.txt`.
    - `*.flow`: bubbleBurst, callToArm, flyingShield, gobble, heavyWeight, homingShield, hydroBlast, kingdomKnight, megalodon, rejuvenate, revitalize, salvation.
    - `honor.txt`, `bubbleShield.txt`, `whaleWave.txt`, `malStorm.txt`, `bowling.txt`, `grandTide.txt`.
    - `knight.txt` (whale_kingdomKnight.cs).
    - `clip_calls.txt` (clip_calls.js).
  - `skillnums.txt`: WhaleSkill.cs's number to name map. 373 reducedCast1, 403 bubbleBurst5, 412 honorStand5, 413 overWeight5, 422 homingShield5, 423 spiralBlast5, 433 revitalize5, 434 bowlingWhale5, 443 divingPress5.
- **`probe.json` -> `summary.txt`, `summ2.py`:** `wardrobe_fx.py whale --probe` of the 35 named effects; castRing is in `probe_castRing.json`. Every one reads except kingdomKnight1 / kingdomKnight2: "no layout for whale_kingdomKnight (8 field bytes)".
- **`probe2.py` -> `probe2.json`:** kingdomKnight2 with a stand-in layout patched in memory, `whale_kingdomKnight: [("kingdomKnight_ring2", "r")]`. It reads whole:
  - 10 nodes.
  - Animation clips root (1 s, loop), nAttack, cAttack and unsummon.
  - The Shrimp_tri skinned mesh and a TrailRenderer on the lance.
  - The ring2 reference resolved.
- **`entries.py` -> `entries.json`, `block.json`:** the cue entries, JSON-checked. Times are in order, every kind is known, and the one new option is listed.

## Max rank and passives on

- **Cast-bar skills:**
  - Bubble Shield 4 (+ Bubble Burst #403), Heavy Weight 2 (+ Over Weight #413).
  - Hydro Blast 4 (+ Spiral Blast #423), Rejuvenate 4 (+ Revitalize #433).
  - Salvation 2, Megalodon 2.
  - Call To Arm and Revitalize: one rank each.
- **Reduced Cast #373:** halves the base cast time before magAdjust (:21237-21243). The bar is 0.1 s at the highest MAG either way.
- **Key-press cast3 skills:** Honor 4 (+ Honor Stand #412), 12th Kingdom Knight 2, Bubble Burst (one rank).
- **Others:** Whale Wave 2 and Mal Storm 2 with Diving Press #443; Flying Shield 2; Homing Shield #422; Gobble Up; Bowling Whale #434; Grand Tide.

Where the rank or a passive picks the look:
- **#423 Spiral Blast:** Hydro Blast draws spiralBlast instead of hydroBlast, and the voice is spiralBlast1 / 2 (:9985, :30859).
- **#443 Diving Press:**
  - The divingWave / divingStorm clips replace malStorm (:32111, :32775).
  - The divingWave effect replaces whaleWave (:31853).
  - Mal Storm gets a second bolt per strike (:10206).
- **12th Kingdom Knight 2:** six kingdomKnight2 knights. Rank 1 has four kingdomKnight1 (:28414-28480).
- **Megalodon 2:** the shark at scale 1.5 (:34807).
- **Hydro Blast 4:** spiralBlast at scale 0.9 + 0.1 x 4 = 1.3 (:10014).

---

## Read this first

### 1. Who plays these clips

| clip | BB | TTO |
|---|---|---|
| cast1 / cast2 | RPC_cast1 :21270 / :20458 (the channel for 8 cast-bar skills) | same (TTO:4016); **TTO's Leviathan Call** also plays them (item 1b) |
| cast3 | the 8 `_cast` coroutines after the channel; RPC_honor :23704, RPC_kingdomKnight :28640, RPC_bubbleBurst :35653 from the key press | same (TTO:2289-17835) |
| divingWave | RPC_whaleWave :32117 (with #443) | same (TTO:21413) |
| divingStorm | RPC_malStorm :32781 (with #443) | same (TTO:10842) |
| flyingShield | RPC_flyingShield :25014; RPC_homingShield :35302 | same (TTO:5105, :7481) |
| gobble | RPC_gobbleUp :26384 | same (TTO:5607) |
| bowlingWhale1 / 2 | RPC_bowlingWhale :37013 / :36733 | same (TTO:1071) |
| grandTide0 | RPC_grandTide0 :38179, started when Grand Tide's ride ends (:37674) | same (TTO:6157) |

- TTO's copies load the same effect, voice and sound names as BB's. I checked the string list of each coroutine one by one (TTO:1071-21413). No look changes.
- **1b. TTO's Leviathan Call:** RPC_leviathanCast (TTO:10488) plays cast1 and cast2. Its strings: castTime 1.5, magAdjusted, castRing, grandTide_ring, then RPC_leviathanBreach. That sequence is the tto report's. The cast1 cues below can be reused there as `@LeviathanCall:cast1` if its timing matches.
- **The malStorm clip** is played only without Diving Press (Whale Wave :32125, Mal Storm :32789). With the passives on it is never played: `LOWER_RANK.whale = ["malStorm"]` (open question 2).
- **Unused by both BB and TTO:** the rip has honorStand1 / honorStand2 voices and a divingStorm effect prefab, but no code loads them. Mal Storm creates `malStorm` with or without #443 (:32480).

### 2. The cast3 pool and the three own tiles

- `RPC_cast1` (:20229-21440) is the channel for the eight skills whose mode is cast (sType :21098-21231).
- At its end, the dispatcher (:20567-21085) starts the skill's `RPC_<skill>_cast`, which plays cast3 with a 0.2 s fade. This is the page's "Cast: cast1 cast2*@0 cast3~", which stays as it is.
- Honor, 12th Kingdom Knight and Bubble Burst start from the key press and play cast3 with a 0.2 s fade, with no channel.
  - Each gets its own tile, as the Sheep's Eden Sanctuary and the Chameleon's Immunity did.
  - Their keys: `@Honor:cast3`, `@12thKingdomKnight:cast3`, `@BubbleBurst:cast3`.
- All eleven reach standby at 1.0 s. The clip is 1.2 s.

### 3. Missing part P1: whale_kingdomKnight

- **Extractor:** `LAYOUTS["whale_kingdomKnight"] = [("kingdomKnight_ring2", "r")]`. It is the script's only serialized field (whale_kingdomKnight.cs:312, 8 bytes), proved by probe2.py.
- **Page part** (whale_kingdomKnight.cs:23-245):
  - Init places the knight at owner + TransformDirection(slot) - up, that is 1 m below the ground, with the owner's rotation.
  - Update eases it to owner + TransformDirection(slot) with Lerp(pos, goal, 4 dt) (:229-234). In the wardrobe that is a rise from y -1 to 0: y = -e^(-4t).
  - The knight's own Animation plays root, looped (the prefab's default).
  - Left out: knightAttack (nAttack, then a hit) and knightGuard (cAttack, with Knight of the Deep during her Charge Attack). Both need an enemy within 8 m while she charges (Whale.cs:9650-9781), and there is none here.
- **Cues:** each knight gets its slot (x, d) with y -1, so the part only adds the rise.
- The six kingdomKnight_ring2 are cued directly at the slots (Init's Instantiate at the knight + up, :126-132), so the part spawns nothing.

### 4. Missing part P2: Whale_flyingShield

- Whale_flyingShield has no serialized fields; it reads already.
- **Page part** (Whale_flyingShield.cs:37-213):
  - **The shield copy:** Init puts a copy of her worn shield under the effect's `flyingShield` node, at local position 0 and identity rotation. mWep1 is the shield on mount_Hand_L (WhaleEquipment.cs:1640-1707), which is the page's L slot.
  - **The flight** comes from the effect's own Animation:
    - The root is placed at hero rotation x Euler(270, 90, 0), which maps a local (x, y, z) to (-y, z, -x) in her frame.
    - At 0.27 s the node is out on her left (x -3.5).
    - At 0.53 s it reaches 11.85 m ahead, 1.36 m up.
    - At 1.0 s it is back at her, coming in on her right (probe.json).
  - **Hits:** each time its 1 m trigger sphere enters an enemy, flyingShield_hit appears at the node with LookRotation(the node's forward) (:126-210, Whale.cs:8942-8965).
    - The part tests the sphere against the standard target body at the cue's `to` (the Bat's body: centre 0.6 m up, height 1, radius 0.3).
    - On the way out the path passes about 0.7 m left of the 10 m line, so I expect a hit near 0.45 s.
    - On the way back it passes about 1.7 m right, so probably no second hit. The part decides from the real curve.
- **Her own shield** is hidden from 0.5 to 1.5 s: `hideProp L` (:24857-24923).

### 5. Missing part P3: Whale_homingShield

- Whale_homingShield has no serialized fields.
- **Page part** (Whale_homingShield.cs:20-469):
  - **The shield copy:** Init puts a copy of her shield at local Euler(0, 0, 90), spun 1200 deg/s about its local x (:122-135, :324).
  - **Steering, each frame** (:278-284):
    - forward = RotateTowards(forward, target centre - pos, 4 dt rad, 1).
    - The rotation is LookRotation(Scale(forward, (1, 0.2, 1))).
    - It then moves 12 m/s forward.
    - The target centre is the cue's `to` (0.6 m up at 10 m).
  - **Hits:** flyingShield_hit at the shield, LookRotation(forward), each time its 0.5 m trigger sphere enters the target body (:340-418).
  - **Repeat hits:** at 12 m/s with a 4 rad/s turn (a 3 m turning radius), it passes through, circles and comes back, so it can hit more than once in its 3 s.
  - **End:** destroyed at Init + 3 s (:225-249).
- **Her own shield:** noShield for chaAdjust(3) = 3 s hides it (CharacterControl.cs:36060-36070; back at :16155). On the page: `hideProp L` with kill 3.

### 6. Missing part P4: the cue option `around`

- createMalstormBolt (:10175-10218) places each bolt at the hero + Random.Range(lo, hi + 1) m along forward turned Random.Range(0, 360) degrees, 12 m up, with identity rotation.
- The page's `spread` draws x and d separately, which gives a square, not a ring.
- **New option `around: [lo, hi]`** (whole metres):
  - When the clip starts, draw r = randInt(lo, hi) and a = randInt(0, 359).
  - Then x += r sin(a) and d += r cos(a). The direction does not matter, because the angle is uniform.
  - The rotation stays as the cue gives it (identity here). Unlike `spread`, it does not turn the effect.
- **Where it goes:** in cueOf beside `spread` (index.html:4858), and in wardrobe_fx_check.py's OPTS.

### 7. Assumed set-ups (the skill cannot be cast without them)

- **Call To Arm:** an ally at the 10 m target point. RPC_cast1 cancels the skill without a teammate (:20946).
  - She lands 2 m short of the ally, so 8 m ahead.
  - In the hero-stays frame, the departure ring is 8 m behind her (d -8) and the arrival ring is at her.
- **Gobble Up:** a swallowed target (doSkill :6284).
  - The target is held at her position (CharacterControl.cs:9040) and spat out at 0.5 s with a push of 10 x forward.
  - The hit 0.1 s later is cued 1 m ahead (APPROXIMATED).
- **Bubble Burst:** her own Bubble Shield on her. It pops only shields she cast (:35863), so the burst is at her centre.
- **Salvation:** castable alone, but it gives its bubble only to teammates other than herself (:33754). So only its ring shows (the Mole's Barrel Cannon precedent).

### 8. Left out: hits, statuses and camera effects

- **Hits only (nothing drawn):** the area hits of Whale Wave, Mal Storm, Call To Arm and Bubble Burst; Megalodon's pulls and bites; Bowling Whale's rolling hits; Gobble Up's 3 m hit; Honor's hate; Hydro Blast's wash.
- **Camera effects:** the screen warps (Bubble Shield, Honor, Bubble Burst, Bowling Whale), Megalodon's motion blur, and the camera shakes (Whale Wave, Mal Storm, Megalodon).
- **Effects on allies:** the salvation bubble (the wardrobe has no ally) and Honor's honor_cast on other allies.
- **Travel:** the hero does not travel. In the game, Bowling Whale rolls at 7 m/s for 6 s (:36706-36921), Grand Tide rides, and grandTide0 slides at 2 m/s (:38188). In the wardrobe every effect stays at the standing hero.

### What is ready

- **Effects (by the probe):** castRing, bubbleShield_cast, bubbleShield, heavy, spiralBlast, rejuvenate, rejuvenate_hit, callToArm_ring, salvation_ring, megalodon_ring, megalodon, revitalize_ring, honor_cast (an EmblemEmitter), kingdomKnight_ring1, kingdomKnight_ring2, bubbleBurst_ring, bubbleBurst, divingWave, malStorm, malStorm_bolt (a BoltEmitter; the rip's file is malstorm_bolt), gobbleUp_ring, gobbleUp_hit, bowlingWhale_ring, bowlingWhale (AlphaTimer, UVScroll, AudioControl), flyingShield_hit.
  - Every component is in wardrobe_fx_inventory.py's BUILT.
- **Effects that need a part:** kingdomKnight2 (P1), flyingShield (P2), homingShield (P3).
- **Missing from plans/fx_inventory.md "### whale":** honor_cast, heavy, bubbleShield, salvation and rejuvenate_hit, which CharacterControl's status code loads by their Resources paths, and kingdomKnight_ring2, the knight's field. They belong in the inventory's CLASS_NOTES.
- **Voices** (all in BB's rip, voices/): cast, bubbleShield1-2, heavyWeight1-2, spiralBlast1-2, rejuvenate1-2, callToArm1-2, salvation1-2, megalodon1-2, revitalize1-2, honor1-2, kingdomKnight1-2, bubbleBurst1-2, whaleWave1-2, malStorm1-2, flyingShield1-2, homingShield1-2, gobbleUp, bowlingWhale1-2.
- **Sounds the code plays** (sounds/): cast2 and honor.
- **Sounds the effects play:** cast1, bubbleShield, hydroBlast, rejuvenate, rejuvenate_hit, callToArm, salvation, megalodon, revitalize_ring, KingdomKnight_ring, bubbleBurst, whaleWave, malStorm, javelin, shieldBash_hit, gobble, bowlingWhale, bowlingWhale_ring.
  - Exception: heavy's AudioSource clip `reduce` is not in whale/sounds. The build should say where it finds it (a shared Sounds clip?).

---

## Cast channel (`cast1` 0.6 s, `cast2` 0.6 s loop)

Source: RPC_cast1 :20229-21440.

| time | what happens | source |
|---|---|---|
| 0 | cast1 (0.2 s fade, Once); voice cast (one file) | :21270, :21311-21376 |
| 0.1 | castRing at the hero, Euler(270, 90, 0) (absolute; EC 60, followPosition, followState, create clip, its looping cast1 sound) | :20403-20421, Yield :21357 |
| 0.6 | cast2 cut in, looped; the ring's root clip | :20458-20479, Yield :21381 |
| 0.6 + bar | the bar magAdjust(castTime), halved first by #373: 0.1 s at the highest MAG; then the skill's `_cast` (myCommand changes, so the ring ends) | :21237-21249, :20559-21085 |

- **castTime at max rank:** Bubble Shield 4.5, Heavy Weight 4, Hydro Blast 4.5, Rejuvenate 5.5, Call To Arm 5, Salvation 5, Megalodon 8, Revitalize 6 (:21107-21226).
  - Each is halved by #373 and floored, then reduced by MAG/32 (CharacterControl.cs:20584-20588), so all are 0.1 s at the highest MAG.
- **The ring's cut** is 0.55: the step edge at 0.6, less the page's margin.
  - Its root clip (from 0.6) therefore never shows, so no castRing hook is needed. The Bat's fx:castRing hook is for the Bat only.
- cast2 has no cues.

## cast3 pool (eight members, after the channel)

All eight start with cast3 at a 0.2 s fade and reach standby at 1.0 s. Ally targets are shown as self-casts (Penguin decision 1). Enemy targets are at the 10 m point.

| member | 0 | later | sources |
|---|---|---|---|
| Bubble Shield | voice, sound cast2 | 0.3: bubbleShield_cast, and the bubble (y 1.3, scale 1.2, kill 10) | :29835-29971, :29682-29722; CharacterControl.cs:35969-36019 |
| Heavy Weight | voice, cast2 | 0.3: heavy at the target (d 10) | :30364-30500, :30228-30250; CharacterControl.cs:35924-35934 |
| Hydro Blast (#423) | voice spiralBlast1 / 2, cast2 | 0.6: spiralBlast at the target, scale 1.3 | :30850-31076, :9974-10014 |
| Rejuvenate (#433) | cast2, voice | 0.3: rejuvenate; rejuvenate_hit ticks at 2.3 and 6.3 | :31469-31638, :31310-31356; CharacterControl.cs:8874-8925 |
| Call To Arm | voice, cast2 | 0.5: two callToArm_rings (d -8 and 0) | :33329-33456, :33141-33171 |
| Salvation | voice, cast2 | 0.5: salvation_ring | :33883-34019, :33689-33788 |
| Megalodon | voice; megalodon_ring at the target | 4.0: megalodon at the target, scale 1.5 | :34317-34482, :34738-34813 |
| Revitalize | voice; revitalize_ring | rejuvenate_hit ticks at 2.5 and 6.5 | :36329-36465, :36236 |

- **The bubbles:** the Whale's CharacterController has centre y 1.3 and radius 0.8 (Whale.prefab:649-655).
  - So bounds.center is 1.3 m up.
  - The bubble scale is Clamp(0.8 + 0.4, 0.5, 1.5) = 1.2.
- **The rejuvenate tick** runs on the game's own 0.5 s status clock: once every 4 s (mod(2t, 8) == 1), at a phase the cast does not set.
  - It is cued at the mean: 2 s after the status, then every 4 s, inside 10 s (the Bat's Phantom Bane precedent).
- **Megalodon** starts its fire coroutine at cast3's 0 s: four pulls 1 s apart, the shark at 4 s, and the second bite at 5.5 s (:34684-34973).

## Honor (`@Honor:cast3`)

Source: RPC_honor :23422-24000.

| time | what happens | source |
|---|---|---|
| 0 | cast3 (0.2 s fade); voice honor1 or 2; the honor status on her (her own layer, 15 m), so honor_cast appears 2 m over her, identity | :23704-23868; CharacterControl.cs:35554-35564 |
| 0.3 | Sounds/honor at volume 2 | :23569-23587, Yield :23947 |
| 0.5 | moveSpeed 0 | Yield :23955 |
| 1.0 | standby | Yield :23961, :23651 |

- honor_cast is an EmblemEmitter (delay 0.4, life 0.5) with no EffectControl. The game never destroys it, so it is cued with kill 1.
- Page line: "Honor: cast3".
- `SEQ_SKILL.whale["@Honor"] = "honor"`.

## 12th Kingdom Knight (`@12thKingdomKnight:cast3`)

Source: RPC_kingdomKnight :28262-28866; whale_kingdomKnight.cs.

| time | what happens | source |
|---|---|---|
| 0 | cast3 (0.2 s fade); voice kingdomKnight1 or 2; kingdomKnight_ring1 at the hero | :28640-28767 |
| 0.5 | six kingdomKnight2 at the slots, 1 m down, rising (P1); a kingdomKnight_ring2 at each slot; the status for 60 s | :28414-28552; whale_kingdomKnight.cs:23-147 |
| 1.0 | standby | :28820, :28570 |

- **Slots** in her frame (x right, d ahead): (1.6, 1.6), (-1.6, 1.6), (1.6, -1.6), (-1.6, -1.6), (2.2, 0), (-2.2, 0).
- **The knights** are cut at 10 s (kill 10, the summons rule).
- **Page line:** "12th Kingdom Knight: cast3".
- **`SEQ_SKILL.whale["@12thKingdomKnight"] = "12thKingdomKnight"`**, matching the Bible's key whale_12thKingdomKnight2.

## Bubble Burst (`@BubbleBurst:cast3`)

Source: RPC_bubbleBurst :35464-36064.

| time | what happens | source |
|---|---|---|
| 0 | cast3 (0.2 s fade); voice bubbleBurst1 or 2; bubbleBurst_ring at the hero | :35653-35780 |
| 0 | each of her own Bubble Shields within 200 m is removed, with Effects/bubbleBurst at its owner's collider centre | :35811-35961 |
| 1.0 | standby | Yield :35998 |

- The tile assumes her own shield (item 7), so bubbleBurst is at y 1.3.
- **Page line:** "Bubble Burst: cast3".
- **`SEQ_SKILL.whale["@BubbleBurst"] = "bubbleBurst"`.**

## Whale Wave (`divingWave`, 1.2 s)

Source: RPC_whaleWave :31694-32315.

| time | what happens | source |
|---|---|---|
| 0 | divingWave (0.2 s fade, Once); voice whaleWave1 or 2 | :32117, :32169-32252 |
| 0.7 | camera shake (left out); divingWave at the hero (EC 1 + 1, its whaleWave sound); the 9 m hit | :31847-31877, :31940, Yield :32245 |
| 1.0 | standby | Yield :32255, :32038 |

## Mal Storm (`divingStorm`, 3.2 s)

Source: RPC_malStorm :32315-32999; createMalstormBolt :10175-10218.

| time | what happens | source |
|---|---|---|
| 0 | divingStorm (0.2 s fade, Once); voice malStorm1 or 2 | :32781, :32833-32922 |
| 0.7 | camera shake (left out); malStorm at the hero (EC 3, its sound); hit 1 of 4 | :32468-32492, :32663-32749, Yield :32912 |
| 0.8 to 1.9, every 0.1 | createMalstormBolt: one bolt 3-5 m out at a random angle, 12 m up; with #443 a second one 5-8 m out | cases 3-5 :32513-32597; :10200-10215 |
| 1.0, 1.3, 1.6 | hits 2-4 | :32663 |
| 2.0 | standby | Yield :32944, :32611 |

- That gives 24 bolt cues, using the new `around` option (P4).

## Flying Shield and Homing Shield (`flyingShield`, 1.9 s): a pool

| | Flying Shield (:24642-25220) | Homing Shield (:35040-35464) |
|---|---|---|
| 0 | clip (0.2 s fade); voice flyingShield1 / 2 | clip (0.2 s fade); voice homingShield1 / 2 |
| 0.5 | flyingShield at the hero x Euler(270, 90, 0) (EC 1, its javelin sound; P2); her shield hidden | homingShield 1 m up and 1 m ahead, LookRotation(forward), life 3 (P3); noShield hides her shield for 3 s |
| hits | flyingShield_hit where the shield meets the target (the part) | flyingShield_hit on each entry (the part) |
| later | 1.5 s: her shield back | 3.5 s: her shield back |
| standby | 1.7 s (:24944) | 1.2 s (:35232) |

- `wardrobe_skill_icons.py` needs nothing for this pool. The cue file's skills make the two tiles, and the Bible has whale_flyingShield2 and whale_homingShield5.

## Gobble Up (`gobble`, 1.0 s)

Source: RPC_gobbleUp :26006-26575.

| time | what happens | source |
|---|---|---|
| 0 | gobble (0.2 s fade, Once); voice gobbleUp (one file); gobbleUp_ring at the hero (EC 2, followPosition, its gobble sound) | :26384-26471 |
| 0.5 | the swallowed target is shown again and pushed 10 x forward | :26142-26233, Yield :26510 |
| 0.6 | the 3 m hit; gobbleUp_hit at the target, LookRotation(forward) | :26258-26306, :9059-9082, Yield :26498 |
| 0.9 | standby | Yield :26502, :26331 |

- The swallowed target's body is not drawn (the wardrobe has none). Only its hit is.

## Bowling Whale (`bowlingWhale1` 1.0 s, `bowlingWhale2` 0.67 s loop)

Source: RPC_bowlingWhale :36538-37250.

| time | what happens | source |
|---|---|---|
| 0 | bowlingWhale1 (0.2 s fade, Once); voice bowlingWhale1 or 2; bowlingWhale_ring at the hero; screen warp (left out) | :37013-37163 |
| 0.5 | bowlingWhale at the hero (EC 7 + 1, followPosition, followState, its looping sound with AudioControl); moveSpeed 7 | :36674-36706, Yield :37189 |
| 1.0 | bowlingWhale2 cut in, looped, for 6 s; hits every 0.25 s within 3 m (left out) | :36733-36852, Yield :37187 |
| 7.0 | standby: the ball ends (followState) | :36867, :36967 |

- The page's "Bowling Whale: bowlingWhale1@1 bowlingWhale2*@6" is right.
- The ball's cut (5.95) is written on bowlingWhale2's clock, as the Mole's Flame Turret's was (index.html fxStart keeps a cut written on a later step's clock).
- bowlingWhale2 has no cues.

## grandTide0 (1.0 s)

Source: RPC_grandTide0 :38002-38230, started at the end of the ride (:37674).

- PlayAnimation(grandTide0, 0) is a cut, as the page's step already is. Then moveSpeed 2, and standby at 0.8 s (Yield :38204).
- There is no effect, voice or sound, so it gets **no cue key**.
- **For skills_b**, who has Grand Tide's grandTide1 / 2:
  - At the same moment, RPC_grandTide plays its `grandTide` effect's `destroy` clip (:37700-37711).
  - That effect is followState with afterLife 1 (probe: EC 99 + 1; clips create 1 s, root 2.03 s, destroy 1 s), so the destroy shows during grandTide0.
  - On the page that would be: spawned at 1.0 s (:37436), `anims [[1, "root"], [4, "destroy"]]` (create plays on awake), and cut 2.95 on grandTide2's clock.
  - This is skills_b's entry: I offer it here and did not write it.

---

## Paste-ready cue entries for wardrobe/fx_cues/whale.json

Validated in `C:\work\12tails-wardrobe\checks\fx_whale_research\skills_a\entries.json`:
- entries.py counts 10 keys and 91 cues: 64 fx, 18 voice, 7 sound, 2 hideProp.
- The one option the check does not know yet is `around` (P4).

```json
{
 "cast1": {
  "why": "Whale.cs RPC_cast1 (:20229-21440), the cast channel the dispatcher starts for the eight cast-time skills (sType :21098-21231: bubbleShield, heavyWeight, hydroBlast, rejuvenate, callToArm, salvation, megalodon, revitalize): at 0: clip cast1 (0.2 fade, Once, :21270-21273) and voice cast (Voices/cast, one file, :21311-21376); Yield 0.1 (:21357): castRing at the hero's position, Quaternion.Euler(270, 90, 0) (createEffect :20403-20421; EffectControl life 60, followPosition, followState; Animation create; plays its own looping Sounds/cast1); Yield 0.5 (:21381): at 0.6 s cast2 cut in and looped and the ring's root clip (:20458-20479), the cast bar magAdjust(castTime) (Reduced Cast #373 halves it first, :21237-21249; 0.1 s at the highest MAG, the page's cast2*@0), then the skill's RPC_<skill>_cast, which sets myCommand: the ring's followState cut at the step edge 0.6 s, cued 0.55 (the page restarts FX.t at each step, as the Sheep's)",
  "cues": [
   [0, "voice", "cast"],
   [0.1, "fx", "castRing", { "rot": [ 270, 90, 0 ], "cut": 0.55 }]
  ]
 },
 "cast3": {
  "why": "The cast3 clip after the RPC_cast1 channel: 8 Whale skills, one per play, even chance, picked anew on every play: Bubble Shield (:29835), Heavy Weight (:30364), Hydro Blast (:30850; Spiral Blast #423 on), Rejuvenate (:31469; Revitalize #433 on), Call To Arm (:33329), Salvation (:33883), Megalodon (:34317), Revitalize (:36329), started from RPC_cast1's dispatch (:20572-21085); Honor (:23704), 12th Kingdom Knight (:28640) and Bubble Burst (:35653) play cast3 from the key press with no channel: their own tiles (@Honor, @12thKingdomKnight, @BubbleBurst)",
  "skills": {
   "bubbleShield": {
    "why": "Whale.cs RPC_bubbleShield_cast (:29518-30055), rank 4, Bubble Burst #403 on (status Lv + 1, more burst damage: no look change), ally target shown as a self-cast (Penguin decision 1): at 0: clip cast3 (0.2 fade, :29835-29838), voice bubbleShield1 / bubbleShield2 (Random.Range(0, 2) :29870-29929), Sounds/cast2 (PlayOneShot :29955-29971; the screen warp :29949 left out); Yield 0.3 (:29997): bubbleShield_cast at the target's collider centre, identity (tChar.createEffect :29682-29700; the Whale's CharacterController centre y 1.3, Whale.prefab:655; life 1 + 1, followPosition; plays its own Sounds/bubbleShield) and the bubbleShield status for chaAdjust(12) = 12 s (:29722), whose apply puts Effects/bubbleShield at the collider centre, parented, scale Clamp(radius 0.8 + 0.4, 0.5, 1.5) = 1.2 (CharacterControl.cs:35969-36019; m_Radius 0.8, Whale.prefab:650; no EffectControl: removed with the status, CharacterControl.cs:16085-16098): cut at 10 s (kill 10); Yield 0.2 (:29999): moveSpeed 0; Yield 0.5 (:30011): standby at 1.0 s",
    "cues": [
     [0, "voice", "bubbleShield1|bubbleShield2"],
     [0, "sound", "cast2"],
     [0.3, "fx", "bubbleShield_cast", { "y": 1.3 }],
     [0.3, "fx", "bubbleShield", { "y": 1.3, "scale": 1.2, "kill": 10 }]
    ]
   },
   "heavyWeight": {
    "why": "Whale.cs RPC_heavyWeight_cast (:30055-30581), rank 2, Over Weight #413 on (status Lv + 1: weight only); target mode 'all' (WhaleSkill.cs:1741-1766), taken as an enemy at the 10 m target point (the enemy branch :30237-30250, getDebuff 15 s): at 0: clip cast3 (0.2 fade, :30364-30367), voice heavyWeight1 / heavyWeight2 (Random.Range(0, 2) :30416-30475), Sounds/cast2 (:30483-30500); Yield 0.3 (:30536): the heavy status on the target (:30228 / :30250), whose apply Instantiates Effects/heavy at the target's position, identity, and InitEffectControl(target) (CharacterControl.cs:35924-35934; EffectControl life 1, followPosition; plays its own Sounds/reduce); Yield 0.2 (:30526), Yield 0.5 (:30534): standby at 1.0 s (:30305)",
    "cues": [
     [0, "voice", "heavyWeight1|heavyWeight2"],
     [0, "sound", "cast2"],
     [0.3, "fx", "heavy", { "d": 10 }]
    ]
   },
   "hydroBlast": {
    "why": "Whale.cs RPC_hydroBlast_cast (:30581-31145), rank 4, Spiral Blast #423 on (passives on), enemy target: the 10 m target point: at 0: clip cast3 (0.2 fade, :30850-30853), with #423 the voice spiralBlast1 / spiralBlast2 (hasSkill(423) :30859, Random.Range(0, 2) :30894-30953; hydroBlast1 / 2 only without it, :30963-31051), Sounds/cast2 (:31059-31076); Yield 0.6 (:31105): RPC_hydroBlast_fire at the target's position (:30751; :9974-10142): with #423 Effects/spiralBlast Instantiated there, identity, scale 0.9 + 0.1 x 4 = 1.3 (:9985-10014; EffectControl life 2; plays its own Sounds/hydroBlast); Yield 0.4 (:31109): standby at 1.0 s (:30791)",
    "cues": [
     [0, "voice", "spiralBlast1|spiralBlast2"],
     [0, "sound", "cast2"],
     [0.6, "fx", "spiralBlast", { "d": 10, "scale": 1.3 }]
    ]
   },
   "rejuvenate": {
    "why": "Whale.cs RPC_rejuvenate_cast (:31145-31694), rank 4, Revitalize #433 on (status Lv 4 + 1 = 5, :31336-31342: the heal only), ally target shown as a self-cast: at 0: clip cast3 (0.2 fade, :31469-31472), Sounds/cast2 (:31498-31510), voice rejuvenate1 / rejuvenate2 (Random.Range(0, 2) :31553-31638); Yield 0.3 (:31644): Effects/rejuvenate at the target's position, identity (tChar.createEffect :31310-31322; life 2, followPosition; plays its own Sounds/rejuvenate) and the rejuvenate status for chaAdjust(18) = 18 s (:31356); its tick (CharacterControl.cs:8874-8925) heals and draws Effects/rejuvenate_hit at the collider centre (y 1.3), identity, when Math.mod(2 x tickTime, 8) == 1 on the game's 0.5 s status clock (:8667-8676): once every 4 s at a phase the cast does not set, cued at the mean, 2 s after the status, then every 4 s within the 10 s (as the Bat's Phantom Bane, plans/fx_bat/skills_b.md); Yield 0.2 (:31653), Yield 0.5 (:31632): standby at 1.0 s (:31410)",
    "cues": [
     [0, "sound", "cast2"],
     [0, "voice", "rejuvenate1|rejuvenate2"],
     [0.3, "fx", "rejuvenate"],
     [2.3, "fx", "rejuvenate_hit", { "y": 1.3 }],
     [6.3, "fx", "rejuvenate_hit", { "y": 1.3 }]
    ]
   },
   "callToArm": {
    "why": "Whale.cs RPC_callToArm_cast (:32999-33553), one rank; RPC_cast1 sends it only with a teammate (the lowest-HP Player-tagged member other than herself, :20792-20889) to getSpawnPos(ally - 2 x unit direction) (:20901-20924), else 'Cannot find target possible position' and cast0 (:20946-20951): the tile assumes an ally at the 10 m target point, so she lands 8 m ahead: at 0: clip cast3 (0.2 fade, :33329-33332), voice callToArm1 / callToArm2 (Random.Range(0, 2) :33370-33429), Sounds/cast2 (:33437-33456); Yield 0.5 (:33499): callToArm_ring Instantiated where she stands, her rotation (:33141), the teleport to the landing spot (:33155), callToArm_ring again there (:33171; EffectControl life 1; each plays its own Sounds/callToArm), the 12 m hit (:33193-33221: hit effects on enemies only); in the hero-stays frame (the Bat's Switch, decision 8: each effect with its owner) the first ring is 8 m behind her, the second at her; Yield 0.5 (:33504): standby at 1.0 s (:33258)",
    "cues": [
     [0, "voice", "callToArm1|callToArm2"],
     [0, "sound", "cast2"],
     [0.5, "fx", "callToArm_ring", { "d": -8 }],
     [0.5, "fx", "callToArm_ring"]
    ]
   },
   "salvation": {
    "why": "Whale.cs RPC_salvation_cast (:33553-34096), rank 2: at 0: clip cast3 (0.2 fade, :33883-33886), voice salvation1 / salvation2 (Random.Range(0, 2) :33935-33990), Sounds/cast2 (:34002-34019); Yield 0.5 (:34052): salvation_ring at the hero, hero rotation (createEffect :33689-33701; life 1, followPosition; plays its own Sounds/salvation), and the salvation status (chaAdjust(2 x 2 + 2) = 6 s) on every living Player-tagged teammate except herself (:33754 gameObject != self, :33788; Bible whale-skill-reference.md:245): the bubble (CharacterControl.cs:36029-36048) is on allies only, none in the wardrobe (the Mole's Barrel Cannon precedent: the game's own look with nobody to receive it); Yield 0.5 (:34045): standby at 1.0 s (:33824)",
    "cues": [
     [0, "voice", "salvation1|salvation2"],
     [0, "sound", "cast2"],
     [0.5, "fx", "salvation_ring"]
    ]
   },
   "megalodon": {
    "why": "Whale.cs RPC_megalodon_cast (:34096-34567), rank 2, enemy target: the 10 m target point (its ground, Physics.Raycast down :34464-34476): at 0: clip cast3 (0.2 fade, :34317-34320), voice megalodon1 / megalodon2 (Random.Range(0, 2) :34352-34407; no cast2 sound, BB and TTO alike), the motion blur (:34431) left out, and RPC_megalodon_fire started (:34482; :34567-35040): megalodon_ring Instantiated at the target, identity, at once (:34738-34756; EffectControl life 4 + 3; plays its own Sounds/megalodon), four pulls 1 s apart (i < 4, Yield(2, 1) :34973, :34684-34685, the pull only), at 4 s Effects/megalodon at the target, identity, scale 1.5 at sLv 2 (:34784-34813; life 3; Animation root), the camera shake (:34834) left out, the bite, Yield 1.5 (:34971) and the second bite at 5.5 s (hits only); the cast's own standby: Yield 0.5 (moveSpeed 0, :34231), Yield 0.5: 1.0 s (:34258)",
    "cues": [
     [0, "voice", "megalodon1|megalodon2"],
     [0, "fx", "megalodon_ring", { "d": 10 }],
     [4, "fx", "megalodon", { "d": 10, "scale": 1.5 }]
    ]
   },
   "revitalize": {
    "why": "Whale.cs RPC_revitalize_cast (:36064-36538), one rank: at 0: clip cast3 (0.2 fade, :36329-36332), voice revitalize1 / revitalize2 (Random.Range(0, 2) :36381-36436), revitalize_ring at the hero, hero rotation (createEffect :36448-36465; life 1 + 1, followPosition; plays its own Sounds/revitalize_ring); Yield 0.5 (:36492): rejuvenate Lv 3 for chaAdjust(18) on every Player-tagged teammate, herself included (no self check, :36214-36236): its tick's rejuvenate_hit at her collider centre once every 4 s on the status clock (CharacterControl.cs:8874-8925), cued at the mean, 2 s after the status, then 4 s on; Yield 0.5 (:36496): standby at 1.0 s (:36270)",
    "cues": [
     [0, "voice", "revitalize1|revitalize2"],
     [0, "fx", "revitalize_ring"],
     [2.5, "fx", "rejuvenate_hit", { "y": 1.3 }],
     [6.5, "fx", "rejuvenate_hit", { "y": 1.3 }]
    ]
   }
  }
 },
 "@Honor:cast3": {
  "why": "Whale.cs RPC_honor (:23422-24000), rank 4 (Honor Stand #412: KO and hate only), from the key press with no channel: at 0: clip cast3 (0.2 fade, :23704-23707), voice honor1 / honor2 (Random.Range(0, 2) :23745-23804; honorStand1 / 2 in the rip are played by no BB or TTO code), the screen warp (:23824) left out, the honor status on every teammate within 15 m, herself included (own layer, :23836-23868), whose apply Instantiates Effects/honor_cast 2 m over the receiver, identity (CharacterControl.cs:35554-35564; an EmblemEmitter, delay 0.4 + life 0.5, no EffectControl: never destroyed, kill 1 once drawn); Yield 0.3 (:23947): Sounds/honor at volume 2 (PlayOneShot :23569-23587); Yield 0.2 (:23955): moveSpeed 0; Yield 0.5 (:23961): standby at 1.0 s (:23651)",
  "cues": [
   [0, "voice", "honor1|honor2"],
   [0, "fx", "honor_cast", { "y": 2, "kill": 1 }],
   [0.3, "sound", "honor", { "vol": 2 }]
  ]
 },
 "@12thKingdomKnight:cast3": {
  "why": "Whale.cs RPC_kingdomKnight (:28262-28866), rank 2, from the key press: at 0: clip cast3 (0.2 fade, :28640-28643), voice kingdomKnight1 / kingdomKnight2 (Random.Range(0, 2) :28681-28736), kingdomKnight_ring1 at the hero, hero rotation (createEffect :28748-28767; life 1 + 1, followPosition; plays its own Sounds/KingdomKnight_ring), earlier knights unsummoned (:28799); Yield 0.5 (:28816): 2 + 2 x 2 = 6 knights, Effects/kingdomKnight2 at sLv 2 (:28414-28480), whale_kingdomKnight.Init(owner, 2, slot) (:28501-28506; whale_kingdomKnight.cs:23-147): slot 0-5 = (1.6, 0, 1.6), (-1.6, 0, 1.6), (1.6, 0, -1.6), (-1.6, 0, -1.6), (2.2, 0, 0), (-2.2, 0, 0) in her frame, placed 1 m below the ground, her rotation, each with its kingdomKnight_ring2 (the prefab's field, = Resources whale/effects/kingdomKnight_ring2) at the knight + up = the slot on the ground (:126-132); Update eases each to its slot, Lerp 4 x dt (:229-234): the rise (the part); their attacks need an enemy within 8 m during her Charge Attack (Whale.cs:9650-9781; whale_kingdomKnight.cs:163-239): none here; the kingdomKnight status chaAdjust(60) (:28527-28538): the knights cut at 10 s (kill 10); Yield 0.5 (:28820): standby at 1.0 s (:28570)",
  "cues": [
   [0, "voice", "kingdomKnight1|kingdomKnight2"],
   [0, "fx", "kingdomKnight_ring1"],
   [0.5, "fx", "kingdomKnight2", { "x": 1.6, "d": 1.6, "y": -1, "kill": 10 }],
   [0.5, "fx", "kingdomKnight_ring2", { "x": 1.6, "d": 1.6 }],
   [0.5, "fx", "kingdomKnight2", { "x": -1.6, "d": 1.6, "y": -1, "kill": 10 }],
   [0.5, "fx", "kingdomKnight_ring2", { "x": -1.6, "d": 1.6 }],
   [0.5, "fx", "kingdomKnight2", { "x": 1.6, "d": -1.6, "y": -1, "kill": 10 }],
   [0.5, "fx", "kingdomKnight_ring2", { "x": 1.6, "d": -1.6 }],
   [0.5, "fx", "kingdomKnight2", { "x": -1.6, "d": -1.6, "y": -1, "kill": 10 }],
   [0.5, "fx", "kingdomKnight_ring2", { "x": -1.6, "d": -1.6 }],
   [0.5, "fx", "kingdomKnight2", { "x": 2.2, "y": -1, "kill": 10 }],
   [0.5, "fx", "kingdomKnight_ring2", { "x": 2.2 }],
   [0.5, "fx", "kingdomKnight2", { "x": -2.2, "y": -1, "kill": 10 }],
   [0.5, "fx", "kingdomKnight_ring2", { "x": -2.2 }]
  ]
 },
 "@BubbleBurst:cast3": {
  "why": "Whale.cs RPC_bubbleBurst (:35464-36064), one rank, from the key press: at 0: clip cast3 (0.2 fade, :35653-35656), voice bubbleBurst1 / bubbleBurst2 (Random.Range(0, 2) :35694-35749), bubbleBurst_ring at the hero, hero rotation (createEffect :35761-35780; life 1; plays its own Sounds/cast2), the screen warp (:35805) left out; at once every teammate within 200 m holding a bubbleShield she cast (sID == her ActorNr, :35811-35863) has it removed (:35932; the bubble goes, CharacterControl.cs:16085-16098), the 12 m blast (hits only) and Effects/bubbleBurst at its collider centre, identity (:35937-35961; life 1, followPosition; plays its own Sounds/bubbleBurst): the tile assumes her own Bubble Shield on her (the Detonate precedent: the skill is the shields' pop), so the burst at her centre, y 1.3; Yield 1 (:35998): standby at 1.0 s (:35600)",
  "cues": [
   [0, "voice", "bubbleBurst1|bubbleBurst2"],
   [0, "fx", "bubbleBurst_ring"],
   [0, "fx", "bubbleBurst", { "y": 1.3 }]
  ]
 },
 "divingWave": {
  "why": "divingWave is Whale Wave's clip with Diving Press #443 (passives on; without it the malStorm clip, :32111-32125): Whale.cs RPC_whaleWave (:31694-32315), rank 2: at 0: clip divingWave (0.2 fade, Once, :32117), voice whaleWave1 / whaleWave2 (Random.Range(0, 2) :32169-32252); Yield 0.7 (:32245): the camera shake (:31847) left out, with #443 Effects/divingWave at the hero, hero rotation (createEffect :31853-31877; whaleWave without it, :31900; EffectControl life 1 + 1; plays its own Sounds/whaleWave), the 9 m area hit (:31940-32011, hits only); Yield 0.3 (:32255): standby at 1.0 s (:32038)",
  "cues": [
   [0, "voice", "whaleWave1|whaleWave2"],
   [0.7, "fx", "divingWave"]
  ]
 },
 "divingStorm": {
  "why": "divingStorm is Mal Storm's clip with Diving Press #443 (:32775-32789): Whale.cs RPC_malStorm (:32315-32999), rank 2: at 0: clip divingStorm (0.2 fade, Once, :32781), voice malStorm1 / malStorm2 (Random.Range(0, 2) :32833-32922); Yield 0.7 (:32912): the camera shake (:32468) left out, Effects/malStorm at the hero, hero rotation (createEffect :32474-32492; the rip's divingStorm prefab is loaded by no BB or TTO code; EffectControl life 3; plays its own Sounds/malStorm), the first of four 12 m area hits (i < 4, :32663-32749: 0.7, 1.0, 1.3, 1.6 s, hits only); then createMalstormBolt every 0.1 s (cases 3-5, Yields :32916, :32942, :32938, twelve times, 0.8 ... 1.9 s; :10175-10218): Effects/malStorm_bolt (the rip's malstorm_bolt) at the hero + Random.Range(3, 6) m (int: 3-5) along forward turned Random.Range(0, 360) deg, 12 m up, identity, and with #443 a second at Random.Range(5, 9) (5-8) m (BoltEmitter; EffectControl life 0.5); Yield 0.1 (:32944): standby at 2.0 s (:32611)",
  "cues": [
   [0, "voice", "malStorm1|malStorm2"],
   [0.7, "fx", "malStorm"],
   [0.8, "fx", "malStorm_bolt", { "around": [ 3, 5 ], "y": 12 }],
   [0.8, "fx", "malStorm_bolt", { "around": [ 5, 8 ], "y": 12 }],
   [0.9, "fx", "malStorm_bolt", { "around": [ 3, 5 ], "y": 12 }],
   [0.9, "fx", "malStorm_bolt", { "around": [ 5, 8 ], "y": 12 }],
   [1.0, "fx", "malStorm_bolt", { "around": [ 3, 5 ], "y": 12 }],
   [1.0, "fx", "malStorm_bolt", { "around": [ 5, 8 ], "y": 12 }],
   [1.1, "fx", "malStorm_bolt", { "around": [ 3, 5 ], "y": 12 }],
   [1.1, "fx", "malStorm_bolt", { "around": [ 5, 8 ], "y": 12 }],
   [1.2, "fx", "malStorm_bolt", { "around": [ 3, 5 ], "y": 12 }],
   [1.2, "fx", "malStorm_bolt", { "around": [ 5, 8 ], "y": 12 }],
   [1.3, "fx", "malStorm_bolt", { "around": [ 3, 5 ], "y": 12 }],
   [1.3, "fx", "malStorm_bolt", { "around": [ 5, 8 ], "y": 12 }],
   [1.4, "fx", "malStorm_bolt", { "around": [ 3, 5 ], "y": 12 }],
   [1.4, "fx", "malStorm_bolt", { "around": [ 5, 8 ], "y": 12 }],
   [1.5, "fx", "malStorm_bolt", { "around": [ 3, 5 ], "y": 12 }],
   [1.5, "fx", "malStorm_bolt", { "around": [ 5, 8 ], "y": 12 }],
   [1.6, "fx", "malStorm_bolt", { "around": [ 3, 5 ], "y": 12 }],
   [1.6, "fx", "malStorm_bolt", { "around": [ 5, 8 ], "y": 12 }],
   [1.7, "fx", "malStorm_bolt", { "around": [ 3, 5 ], "y": 12 }],
   [1.7, "fx", "malStorm_bolt", { "around": [ 5, 8 ], "y": 12 }],
   [1.8, "fx", "malStorm_bolt", { "around": [ 3, 5 ], "y": 12 }],
   [1.8, "fx", "malStorm_bolt", { "around": [ 5, 8 ], "y": 12 }],
   [1.9, "fx", "malStorm_bolt", { "around": [ 3, 5 ], "y": 12 }],
   [1.9, "fx", "malStorm_bolt", { "around": [ 5, 8 ], "y": 12 }]
  ]
 },
 "flyingShield": {
  "why": "The flyingShield clip: Flying Shield (RPC_flyingShield :25014) and Homing Shield (RPC_homingShield :35302), one tile each (poolChains)",
  "skills": {
   "flyingShield": {
    "why": "Whale.cs RPC_flyingShield (:24642-25220), rank 2: at 0: clip flyingShield (0.2 fade, Once, :25014-25017), voice flyingShield1 / flyingShield2 (Random.Range(0, 2) :25055-25138); Yield 0.5 (:25143): Effects/flyingShield at the hero, hero rotation x Euler(270, 90, 0) (createEffect :24789-24807; EffectControl life 1; plays its own Sounds/javelin; its Animation flyingShield (1 s) carries the child node out on the left to 11.85 m ahead at 1.36 m up and back on the right, checks/fx_whale_research/skills_a/probe.json), Whale_flyingShield.Init (:24818-24840; Whale_flyingShield.cs:37-108: a copy of her worn shield mWep1 under the node), her shield's MeshRenderers off (:24857-24879; mWep1 = the shield on mount_Hand_L, WhaleEquipment.cs:1640-1707: the page's L); on each enemy it enters (its 1 m trigger sphere, Whale_flyingShield.cs:126-210) RPC_flyingShield_hit: flyingShield_hit at the shield, LookRotation(its forward) (Whale.cs:8942-8965; the part, at the 10 m target body); Yield 1 (:25145): at 1.5 s the renderers back on (:24897-24923); Yield 0.2 (:25131): standby at 1.7 s (:24944)",
    "builds": ["flyingShield_hit"],
    "cues": [
     [0, "voice", "flyingShield1|flyingShield2"],
     [0.5, "fx", "flyingShield", { "rot": [ 270, 90, 0 ], "to": [ 0, 0.6, 10 ] }],
     [0.5, "hideProp", "L", { "kill": 1 }]
    ]
   },
   "homingShield": {
    "why": "Whale.cs RPC_homingShield (:35040-35464), one rank (Homing Shield #422), enemy target: the 10 m target point: at 0: clip flyingShield (0.2 fade, Once, :35302-35305), voice homingShield1 / homingShield2 (Random.Range(0, 2) :35343-35425); Yield 0.5 (:35428): RPC_homingShield_fire at the hero + TransformDirection(0, 1, 1) (1 m up, 1 m ahead), LookRotation(forward) (:35194; :10371-10431): Effects/homingShield, Whale_homingShield.Init(chaAdjust(3) = 3 s, her, the target) (Whale_homingShield.cs:20-146: a copy of her shield at Euler(0, 0, 90), spun 1200 deg/s about its x, :324); each frame it turns towards the target's collider centre at 4 rad/s, its heading flattened (y x 0.2), and flies 12 m/s (:257-284), hitting on each entry of its 0.5 m trigger sphere (:340-418: flyingShield_hit at it, LookRotation(forward), RPC_flyingShield_hit), destroyed at 3 s (:225-249; plays its own Sounds/javelin); the noShield status for chaAdjust(3) = 3 s (:35211) turns her shield's MeshRenderers off (CharacterControl.cs:36060-36070, back at its end :16155): hideProp L 3 s; Yield 0.7 (:35430): standby at 1.2 s (:35232)",
    "builds": ["flyingShield_hit"],
    "cues": [
     [0, "voice", "homingShield1|homingShield2"],
     [0.5, "fx", "homingShield", { "y": 1, "d": 1, "to": [ 0, 0.6, 10 ], "kill": 3 }],
     [0.5, "hideProp", "L", { "kill": 3 }]
    ]
   }
  }
 },
 "gobble": {
  "why": "gobble is Gobble Up's clip (RPC_gobbleUp :26384): Whale.cs RPC_gobbleUp (:26006-26575), one rank; doSkill casts it only with a swallowed target (mSwallowObject, :6284: 'mouth is empty!'): the tile assumes Swallow's target held in her (the Detonate precedent): at 0: clip gobble (0.2 fade, Once, :26384-26387), voice gobbleUp (one file; the error names gobbleUp1, :26431-26447), gobbleUp_ring at the hero, hero rotation (createEffect :26454-26471; EffectControl life 2, followPosition; plays its own Sounds/gobble); Yield 0.5 (:26510): the target's renderers back on, gobble / swallow removed, pushed with 10 x forward (:26142-26233; the swallowed target stands at her, CharacterControl.cs:9040, after Swallow's pulls to 1 m ahead); Yield 0.1 (:26498): the 3 m hit round it (:26258-26286) and RPC_gobbleUp_hit at its position, LookRotation(her forward) (:26301; :9059-9082: gobbleUp_hit, life 1): 1 m ahead (APPROXIMATED: 0.1 s into its knockback); Yield 0.3 (:26502): standby at 0.9 s (:26331)",
  "cues": [
   [0, "voice", "gobbleUp"],
   [0, "fx", "gobbleUp_ring"],
   [0.6, "fx", "gobbleUp_hit", { "d": 1 }]
  ]
 },
 "bowlingWhale1": {
  "why": "Whale.cs RPC_bowlingWhale (:36538-37250), Bowling Whale #434 (one rank): at 0: clip bowlingWhale1 (0.2 fade, Once, :37013-37016), voice bowlingWhale1 / bowlingWhale2 (Random.Range(0, 2) :37054-37109), bowlingWhale_ring at the hero, hero rotation (createEffect :37121-37140; life 1 + 1, followPosition; plays its own Sounds/bowlingWhale_ring), the screen warp (:37163) left out; Yield 0.5 (:37189): Effects/bowlingWhale at the hero, hero rotation (createEffect :36674-36692; EffectControl life 7 + 1, followPosition, followState; Animation root; its looping Sounds/bowlingWhale with AudioControl's fades), moveSpeed 7 (:36706); Yield 0.5 (:37187): at 1.0 s bowlingWhale2 cut in, looped, for 6 s (:36733-36743; the SEQ's bowlingWhale2*@6), the roll steered by the arrow keys and the 3 m hits every 0.25 s (:36779-36852; the hero does not travel: hits left out, the Chopper's rule); at 7.0 s standby (:36867, :36967): the effect's followState cut on bowlingWhale2's clock, 5.95 (the step's 6 s less the page's margin; a later step's cut, as the Mole's Flame Turret)",
  "cues": [
   [0, "voice", "bowlingWhale1|bowlingWhale2"],
   [0, "fx", "bowlingWhale_ring"],
   [0.5, "fx", "bowlingWhale", { "cut": 5.95 }]
  ]
 }
}
```

## Page lines (for the editor)

- **`SEQ.whale`:** add "Honor: cast3", "12th Kingdom Knight: cast3" and "Bubble Burst: cast3".
  - Each first step fades 0.2 s, as in the game. Without an @t the step runs the clip's 1.2 s; the game's standby is at 1.0 s.
  - The rest stays: Cast, Bowling Whale and Grand Tide are right as they are.
- **`SEQ_SKILL.whale`:** `{ "@Honor": "honor", "@12thKingdomKnight": "12thKingdomKnight", "@BubbleBurst": "bubbleBurst" }`.
- **`LOWER_RANK.whale`:** `["malStorm"]` (open question 2).
- **`wardrobe_skill_icons.py`:**
  - `CLIP_SKILLS["whale"] = {"divingWave": ["whaleWave"], "divingStorm": ["malStorm"], "gobble": ["gobbleUp"]}`.
  - `OWN_TILE["whale"] = {"honor": ["cast3"], "12thKingdomKnight": ["cast3"], "bubbleBurst": ["cast3"]}`.
  - The cast3 and flyingShield pools come from the cue file. bowlingWhale1/2 and grandTide0 get their icons by name.
  - The Bible has every icon key used: whale_bubbleShield4, heavyWeight2, hydroBlast4, rejuvenate4, callToArm1, salvation2, megalodon2, revitalize5, honor4, 12thKingdomKnight2, bubbleBurst5, whaleWave2, malStorm2, flyingShield2, homingShield5, gobbleUp1, bowlingWhale5, grandTide5.
- **cueOf:** the option `around` (P4); wardrobe_fx_check.py OPTS += "around".
- **New part file:** `fxparts/whale.js` (P1-P3), added to FX_PART_FILES.
- **`wardrobe_fx.py`:** `LAYOUTS["whale_kingdomKnight"]`.
- **Inventory:** add whale_kingdomKnight, Whale_flyingShield and Whale_homingShield to BUILT once built, and add the status-loaded effects to CLASS_NOTES.

## Parts summary

| part | what | for |
|---|---|---|
| P1 whale_kingdomKnight | Extractor: the layout `[("kingdomKnight_ring2", "r")]`. Page: the rise from y -1 to the slot (y = -e^(-4t)), the root loop; the attacks are left out | 12th Kingdom Knight |
| P2 Whale_flyingShield | A copy of the worn L prop under the animated `flyingShield` node; contact with the target body at `to` (1 m sphere) spawns flyingShield_hit, LookRotation(node forward), once per entry | Flying Shield |
| P3 Whale_homingShield | A copy of the worn L prop at Euler(0, 0, 90), spun 1200 deg/s about its x; steering at 12 m/s with RotateTowards 4 rad/s toward `to` (heading y x 0.2); a 0.5 m sphere, flyingShield_hit per entry; ends at 3 s | Homing Shield |
| P4 `around` | Cue option: r = randInt(lo, hi), a = randInt(0, 359) when the clip starts; x += r sin a, d += r cos a; no turning (index.html cueOf + OPTS) | Mal Storm |

## Bible findings to offer the user (check against the reference first; never written there)

1. **Unused assets:** the divingStorm effect prefab and the honorStand1 / honorStand2 voices are in the game data, but neither BB nor TTO loads them. Mal Storm creates `malStorm` with or without Diving Press (Whale.cs:32480).
2. **Mal Storm's bolts:** 12 strikes 0.1 s apart, from 0.8 s to 1.9 s.
   - Each strike puts a bolt 3-5 m out (whole metres) at a random angle, 12 m up.
   - With Diving Press there is a second bolt 5-8 m out (Whale.cs:10200-10215, :32513-32597).
   - The four area hits land at 0.7, 1.0, 1.3 and 1.6 s; standby at 2.0 s.
3. **Whale Wave:** its wave and hit come at 0.7 s, and standby at 1.0 s.
4. **12th Kingdom Knight's knights:**
   - They stand at fixed slots: (+-1.6, +-1.6) and (+-2.2, 0) m in her frame.
   - They rise from 1 m below the ground.
   - They act only while she uses her Charge Attack with an enemy within 8 m (Whale.cs:9695-9771; I did not re-derive the exact gate).
5. **Homing Shield:** flies 12 m/s and turns 4 rad/s toward the target. It can hit again each time it re-enters the target in its 3 s (Whale_homingShield.cs:257-418).
6. **Flying Shield:** the shield goes out on her left to about 11.9 m and comes back on her right in 1 s (the flyingShield Animation).
7. **Rejuvenate's heal tick** runs on the global 0.5 s status clock, once every 4 s, with the rejuvenate_hit effect each time (CharacterControl.cs:8874-8925).

## Open questions (recommended answers)

1. **Heavy Weight's target** (mode "all"): on the enemy at 10 m, or on herself (the weight combo with Whale Wave)? Recommended: the enemy, by the effects-on-enemy rule; the reference calls the enemy case the practical one.
2. **The malStorm clip:** hide it with `LOWER_RANK.whale = ["malStorm"]`? Recommended: yes, since Diving Press is on. The clip is skills_b's; if skills_b cued it, that key just goes unused.
3. **Call To Arm's two rings:** departure 8 m behind and arrival at her (written), or both at her (the Penguin's Blink precedent)? Recommended: as written, each ring at its owner's spot (the Bat's Switch).
4. **Salvation:** only the ring, or the bubble on her as a stand-in ally? Recommended: ring only. The code excludes the caster (:33754), and Barrel Cannon is the precedent for a look with nobody to receive the effect.
5. **Bubble Burst:** assume her own shield, so the burst shows at her centre? Recommended: yes (the Detonate precedent).
6. **Gobble Up:** assume a swallowed target, with the hit 1 m ahead? Recommended: yes. The knockback distance is APPROXIMATED.
7. **12th Kingdom Knight:** build the six knights with their rise, and cut them at 10 s? Recommended: yes (P1). Their attacks are left out, since there is no enemy within 8 m and no charge.
8. **Flying Shield's hit:** found by the part's contact with the target, or a fixed cue near 0.45 s? Recommended: the part (the code's trigger).
9. **Homing Shield's hits:** one or several? Recommended: whatever the part's contact test gives, as in the game (repeat entries hit again).
10. **The rejuvenate / revitalize ticks:** at the mean phase (2 s after the status, then every 4 s)? Recommended: yes (the Bat's Phantom Bane precedent).
11. **honor_cast:** kill 1? Recommended: yes. The game never destroys it, but its emitter is done by 0.9 s.
12. **castRing's absolute Euler(270, 90, 0):** written relative to the hero; this is the same at the page's facing and the ring is round. Recommended: keep it.
13. **grandTide0:** no key of its own, with the grandTide effect's destroy left to skills_b's grandTide1 entry? Recommended: yes; the data is given in the grandTide0 section.
14. **TTO's Leviathan Call opens with cast1 / cast2** (RPC_leviathanCast, TTO:10488). Recommended: the tto report owns the sequence; reuse this report's castRing cue as `@LeviathanCall:cast1` if its timing matches.

## Not done

- No "## Verification" section: that is the checker's job.
- No browser, no build, no repo edit apart from this report, which was returned as text.

## Verification (13/11/2026)

A read-only re-check by the checker (office PC). It covers BB `DecompiledSource/Whale.cs`, `CharacterControl.cs`, `Math.cs` and `BoltEmitter.cs`, BB's rip, `wardrobe/index.html`, `pipeline/wardrobe_fx_check.py`, `pipeline/wardrobe_skill_icons.py`, `data/whale/clips.json`, the Bible's `assets.js` / `index.html` and the sibling reports' Verification sections. This section wins over the report body. Probes are in `checks/fx_whale_research/verify_a/`:
- `RPC_<name>.txt`: `pipeline/clip_flow.js` dumps of all 20 coroutines in scope, with the Effects / Voices / Sounds / moveSpeed lines kept.
- `malStorm_cases.txt`: Mal Storm's cases with the opaque predicates evaluated.
- `probe.json` + `summary.txt`: `wardrobe_fx.py whale --probe` of the 27 cued effects, run here; `probe.err` is empty.
- `fs_check.py`: the Flying Shield node's path, worked out again from this probe's clip.
- `check_block.py`: each json block of a report checked against `wardrobe_fx_check.py`'s KINDS / OPTS / entry keys and clips.json.

**Checked and confirmed (no change).**
- **Waits, case by case** (each Yield's state number followed to its case; the predicates evaluated). All eleven cast3 users reach standby at 1.0 s:
  - Bubble Shield, Heavy Weight, Rejuvenate and Honor: 0.3 + 0.2 + 0.5.
  - Hydro Blast: 0.6 + 0.4.
  - Call To Arm, Salvation, Megalodon, Revitalize and 12th Kingdom Knight: 0.5 + 0.5.
  - Bubble Burst: 1.
  - Their effects and statuses land in case 2 at the times in the tables.
- **Cast channel:** voice `cast` before Yield(2, 0.1) (Block_154 -> IL_524, :21376 / :21357), castRing at 0.1, cast2 and the ring's root at 0.6 (:21381).
  - Cast times as listed (:21107-21226).
  - #373 is `FloorToInt(0.5 x castTime)` before magAdjust (:21243-21249).
  - The cast-bar skills, Revitalize included, are dispatched by RPC_cast1 (:20584-21010 and the 20530 block's :534). Honor, 12th Kingdom Knight and Bubble Burst start directly (:4231-4285, :4591-4609).
- **Mal Storm, traced through its gotos:**
  - case 2 at 0.7: the effect and i = 0, then the hit loop (:32663, `i >= 4` -> IL_E96).
  - Then IL_444 Yield(3, 0.1), case 3 a bolt -> IL_E1E Yield(4), case 4 a bolt -> IL_C9B Yield(5), case 5 a bolt and i++.
  - So the hits come at 0.7 / 1.0 / 1.3 / 1.6, there are 12 bolt strikes from 0.8 to 1.9, and standby is at 2.0.
  - createMalstormBolt (:10200-10215): int `Range(3, 6)` / `Range(5, 9)` m, `Range(0, 360)` deg, + 12 up, identity; the second bolt only with #443.
- **Whale Wave:** voice at 0, Yield 0.7, then the effect (divingWave with #443, :31853), the 9 m hit and Yield 0.3. Wrap Once is set after the if / else (:32131), so it applies to both clips.
- **Rejuvenate's tick:** `Math.mod` floors its arguments (Math.cs:46-49). So `mod(2 x clock, 8) == 1` (CharacterControl.cs:8886), on a clock reset every >= 0.5 s (:8667-8676), fires once every 4 s at a free phase, and the mean-phase cue is right (Bat decision 16).
  - Revitalize gives `rejuvenate` Lv 3 to every Player child of her team parent, herself included (the :36210 loop; predicates evaluated).
  - The status apply only adds the status (IL_D5A, :32702-32729), so there is no extra look.
- **Positions and scales:**
  - spiralBlast 0.9 + 0.1 x 4 = 1.3 (:10014).
  - megalodon 1.5 only at `sLv == 2` (:34807-34813), after four pulls (`i >= 4` :34778, Yield(2, 1) :34973).
  - honor_cast at position + 2 up, identity (CharacterControl.cs:35564).
  - heavy at the holder, InitEffectControl (:35928-35934).
  - bubble scale Clamp(0.8 + 0.4) = 1.2 at bounds.center (:35999-36019).
  - Salvation skips herself (`!= self` :33754).
  - Gobble Up's push (:26223) and its hit at the target, LookRotation(her forward), no sound (:9059-9082).
  - Bowling Whale's 6 s roll timer (:36743).
- **Names:**
  - All 27 effects read in this probe. EffectControl lives, follow flags and AudioSources are as the report states. The rip's file is `malstorm_bolt` (Resources.Load ignores case; the probe reads it as `malStorm_bolt`).
  - All 39 cued / named voices are in `whale/voices/`, and `cast2` and `honor` are in `whale/sounds/`.
  - Neither Whale.cs nor TTO's pseudo/Whale.c loads `Effects/divingStorm` or `honorStand1/2`. TTO's one `divingStorm` string (:10883) is the clip.
- **Components:** BoltEmitter, UVScroll, AudioControl, EmblemEmitter, VortexEmitter, AlphaTimer and EmitterControl are all in the inventory's BUILT.
- **TTO:** the Whale's released TTO clip is `leviathanCall` alone (`tto_released.json`), and this report adds no TTO key. I did not re-derive TTO's copies of these coroutines (no TTO look is used here).
- **The block:** it parses, with 10 keys and 91 cues (64 fx, 18 voice, 7 sound, 2 hideProp).
  - Every key is a clip of the class, or an `@` key of a SEQ line the report adds.
  - Times are in order, and the entry keys are valid.
  - The only unknown option is `around`, on the 24 bolt cues.
- **Bowling Whale's ball** `cut 5.95` stands, rather than parts.md table 9's "`kill` across the step edge":
  - fxStart leaves a cut written in a later step's clock (index.html:5374-5379).
  - Fx then cuts it at FX.t 5.95 of bowlingWhale2, at age 6.45 < life 7 (:4341).
  - That plays the followState end and its 1 s after-life, as the game does.
- **Icons:** the regex picks `whale_bubbleBurst5`, `homingShield5`, `revitalize5`, `bowlingWhale5` and `grandTide5` over their `1` keys. Each pair is byte-identical (md5 checked), so this needs no change.

**Findings.**

1. **The 12th Kingdom Knight entry: parts.md Verification 1 replaces this report's.**
   - What is wrong: the cues place each knight with `x`, `d`, `y -1` and `kill 10`, and cue the six `kingdomKnight_ring2` themselves. That is not the fixed interface (parts.md Interfaces 1 and 3):
     - The part reads `slot` (required) and puts the knight at `(ox, -1, oz)` itself. The cue's own x / d would be added on top: the slot twice.
     - The part spawns ring2 itself (`"builds": ["kingdomKnight_ring2"]`), so the six cued rings would be doubled.
     - The cut is `end` (the `unsummon` clip, then gone 1 s later), not `kill`.
   - The page lines also miss the icon fix. `whale_12thKingdomKnight2` starts with a digit, so the icon regex `{cls}_([A-Za-z]+?)(\d*)` (wardrobe_skill_icons.py:109) never reads it. Add `RANK_ICONS["whale"] = {"12thKingdomKnight": "whale_12thKingdomKnight2"}` (the top rank; the `1` and `2` icons differ), and keep this report's three-skill `OWN_TILE["whale"]`.
   - The corrected entry is parts.md Verification 1's, repeated below.

2. **Flying Shield never hits the 10 m target.**
   - What is wrong (item 4, the `flyingShield` why, open question 8): "the path passes about 0.7 m left of the 10 m line, so I expect a hit near 0.45 s", and "at 0.53 s it reaches 11.85 m ahead".
   - The node's path, worked out again from this probe's clip with the root at hero x Euler(270, 90, 0) (`fs_check.py`):
     - It crosses d 10 at about x -2.3 (0.37 s).
     - It is farthest ahead at 0.50 s: d 11.98, x 0.20.
     - Its closest pass to the Bat-decision-4 capsule is **1.64 m at 0.44 s**, outside the 1 m trigger.
     - parts.md's `fs_path.txt` agrees (1.48 m against its box; parts.md Verification 8 measures against the capsule).
   - So no `flyingShield_hit` is drawn. The part keeps the contact test, which finds none (question 8 stands: the part decides).
   - `"to"` on the flyingShield cue is read by no part (Interfaces 1: "javelin / flyingShield take none"; the body is whale.js's constant), so it is dropped.
   - Homing Shield's cue takes parts.md's shape, `{"y": 1, "d": 1}`. Its `to` is the part's default (0, 0.6, 10), and its `kill 3` repeats the part's own 3 s end. `builds` stays on homingShield only.
   - The corrected `flyingShield` entry is below.

3. **P4 `around` is in no builder's list.**
   - parts.md's page_pipeline row (:336) never names it. Every missing part is built (the rule), so it goes to page_pipeline, as skills_b's `boneAt` did (skills_b.md Verification 2). Three changes:
     - **`wardrobe/index.html` cueOf**, after the `spread` block (:4858-4861), one line:
       `if (Array.isArray(o.around)) { const r = randInt(o.around[0], o.around[1]), a = randInt(0, 359) * Math.PI / 180; q.x += r * Math.sin(a); q.d += r * Math.cos(a); }`
       - `randInt` includes `hi`, so `[3, 5]` = Unity's int `Range(3, 6)`.
       - It leaves `q.rot` alone: the bolt is identity.
     - **The cue-format comment** gets a dated line for it.
     - **`pipeline/wardrobe_fx_check.py:215`:** `OPTS += "around"`. Without it the check reports all 24 bolt cues as "bad cue" (`check_block.py`).
   - Until P4 is built, the divingStorm entry stays out of whale.json.
   - For the editor's browser check: the bolt prefab's BoltEmitter is at local y 10 with its BoltTarget at the root (probe). At the game's +12 m the bolts draw 12-22 m up, above the storm. This is faithful (Whale.cs:10203), but it may sit above the frame.

4. **castRing needs the hook word after all (parts.md part 7). No cue change.**
   - What is wrong: "no castRing hook is needed. The Bat's fx:castRing hook is for the Bat only."
   - parts.md part 7 lets `"whale"` through bat.js's gate, for TTO's Leviathan Breach ring, which loops from its spawn (tto.md Verification 4).
   - For BB's channel the hook does nothing. The cut at 0.55 comes at age 0.45, before the hook's 0.5 s (bat.js `t < 0.5`), the same as the Sheep's `[0.1, castRing, {rot, cut 0.55}]` (sheep.json:58).

5. **TTO's sequence is Leviathan Breach, keyed `@LeviathanBreach:cast1`.**
   - What is wrong (item 1b, open question 14): `@LeviathanCall:cast1`. The SEQ line is "Leviathan Breach: cast1@0.1 cast2*^@0 leviathanCall^", with keys `@LeviathanBreach:cast1` / `:cast2` (tto.md :35, :43, :242-250).
   - Its entry carries its own castRing (cut at 0.1) and no voice, so nothing from this report's cast1 entry is reused there. Question 14 is closed.

6. **grandTide0: the offered destroy data is superseded.**
   - The wave's end is skills_b's / parts.md's `[1, "fx", "grandTide", {"release": 4}]`: fx.cutNow() at age 4 (skills_b.md Verification 1, parts.md section 6).
   - This report's `anims [[1, "root"], [4, "destroy"]]` and `cut 2.95` are not used.
   - "No key for grandTide0" (question 13) stands, as skills_b.md Verification 4 also says.

7. **The knights' attack gate is the other way round.**
   - What is wrong (item 3 "Left out", Bible finding 4): "Both need an enemy within 8 m while she charges".
   - KingdomKnight() (Whale.cs:9680-9781, predicates evaluated) returns while the status lives when `actionState == "attack"` (:9695-9697) or `myCommand == "cAttack1"` (:9703-9705).
   - Otherwise, every 3 s (:9711-9719), it sends the knights at the closest enemy within 8 m (:9729-9776).
   - So the knights attack while she is **not** attacking. During her charge, with Round Table, they guard (whale_kingdomKnight.cs knightGuard, parts.md section 4). When the status ends, they are unsummoned (:9784-9796).
   - No cue change: the 10 m target is outside 8 m. Bible finding 4 should read this way.

8. **heavy's `reduce` sound is found, so this report's exception closes.**
   - The only `reduce` WAV in the rip is `characters/heroes/rabbit/sounds/reduce.wav`.
   - rip_wav's walk under gameassets finds it (wardrobe_fx.py:870-876), so no SOUND_ALIASES line is needed.

**Corrected paste-ready entries.** Only `@12thKingdomKnight:cast3` and `flyingShield` change. Every other entry in the block above stands as written. `divingStorm` goes in once P4 is built (finding 3).

```json
  "@12thKingdomKnight:cast3": {
    "why": "Whale.cs $RPC_kingdomKnight$28772 (:28262-28850), max rank sLv 2 (12thKingdomKnight1 / 2, whale-skill-reference.md:22), started by the dispatcher with no cast bar (:7482; Heavy Weight / Bubble Shield go through RPC_cast1, :7415, :7447): at 0 the clip cast3 (0.2 fade, :28640), voice kingdomKnight1 | kingdomKnight2 (Random.Range(0, 2) :28681; :28693 / :28724; PlayOneShot :28705 / :28736), kingdomKnight_ring1 by createEffect at the hero, hero rotation (:28755-28767), the old knights unsummoned (:28799); Yield(2, 0.5) (:28816): at 0.5 2 + 2 sLv = 6 knights (:28414), kingdomKnight2 for sLv 2 (:28468-28480), Init(owner, sLv, slot i) (:28506): each at hero + TransformDirection(slot) - up, slot 0-5 = (1.6, 0, 1.6), (-1.6, 0, 1.6), (1.6, 0, -1.6), (-1.6, 0, -1.6), (2.2, 0, 0), (-2.2, 0, 0) (whale_kingdomKnight.cs:54-120), kingdomKnight_ring2 at its slot on the floor (:126-132), rising to the slot (Lerp 4 / s, :229); the kingdomKnight status chaAdjust(60) (:28527-28538), cut at 10 s after the summon (Bat decision 25): end 10 = unsummon(), its clip unsummon then Destroy 1 s later (whale_kingdomKnight.cs:867-913, Whale.cs:9827-9868); Yield(3, 0.5) (:28820): 1.0 standby (:28570). No volley: KingdomKnight() sends them every 3 s, only while she is not attacking, at FindClosestTarget(the Whale, 8) (Whale.cs:9695-9729; the volley RPC :29062), and the target is 10 m away",
    "builds": ["kingdomKnight_ring2"],
    "cues": [
      [0, "voice", "kingdomKnight1|kingdomKnight2"],
      [0, "fx", "kingdomKnight_ring1"],
      [0.5, "fx", "kingdomKnight2", {"slot": 0, "end": 10}],
      [0.5, "fx", "kingdomKnight2", {"slot": 1, "end": 10}],
      [0.5, "fx", "kingdomKnight2", {"slot": 2, "end": 10}],
      [0.5, "fx", "kingdomKnight2", {"slot": 3, "end": 10}],
      [0.5, "fx", "kingdomKnight2", {"slot": 4, "end": 10}],
      [0.5, "fx", "kingdomKnight2", {"slot": 5, "end": 10}]
    ]
  },
  "flyingShield": {
    "why": "The flyingShield clip: Flying Shield (RPC_flyingShield :25014) and Homing Shield (RPC_homingShield :35302), one tile each (poolChains)",
    "skills": {
      "flyingShield": {
        "why": "Whale.cs RPC_flyingShield (:24642-25220), rank 2: at 0: clip flyingShield (0.2 fade, Once, :25014-25017), voice flyingShield1 / flyingShield2 (Random.Range(0, 2) :25055-25138); Yield 0.5 (:25143): Effects/flyingShield at the hero, hero rotation x Euler(270, 90, 0) (createEffect :24789-24807; EffectControl life 1; plays its own Sounds/javelin; its Animation flyingShield (1 s) carries the child node out on the left (x -3.5 at 0.25 s), to 11.98 m ahead at 0.50 s, 1.36 m up, and back on the right), Whale_flyingShield.Init (:24818-24840; Whale_flyingShield.cs:37-108: a copy of her worn shield mWep1 under the node: the part), her shield's MeshRenderers off (:24857-24879; mWep1 = the shield on mount_Hand_L, WhaleEquipment.cs:1640-1707: the page's L); on each enemy its 1 m trigger sphere enters (Whale_flyingShield.cs:126-210) RPC_flyingShield_hit: flyingShield_hit at the shield, LookRotation(its forward) (Whale.cs:8942-8965): at the standard 10 m body the path's closest pass is 1.64 m at 0.44 s (checks/fx_whale_research/verify_a/fs_check.py; parts' fs_path.txt), so no hit, as in the game (the part tests contact); Yield 1 (:25145): at 1.5 s the renderers back on (:24897-24923); Yield 0.2 (:25131): standby at 1.7 s (:24944)",
        "cues": [
          [0, "voice", "flyingShield1|flyingShield2"],
          [0.5, "fx", "flyingShield", {"rot": [270, 90, 0]}],
          [0.5, "hideProp", "L", {"kill": 1}]
        ]
      },
      "homingShield": {
        "why": "Whale.cs RPC_homingShield (:35040-35464), one rank (Homing Shield #422), enemy target: the 10 m target point: at 0: clip flyingShield (0.2 fade, Once, :35302-35305), voice homingShield1 / homingShield2 (Random.Range(0, 2) :35343-35425); Yield 0.5 (:35428): RPC_homingShield_fire at the hero + TransformDirection(0, 1, 1) (1 m up, 1 m ahead), LookRotation(forward) (:35194; :10371-10431): Effects/homingShield, Whale_homingShield.Init(chaAdjust(3) = 3 s, her, the target) (Whale_homingShield.cs:20-146: a copy of her shield at Euler(0, 0, 90), spun 1200 deg/s about its x, :324); each frame it turns towards the target's collider centre (the part's default, the body's (0, 0.6, 10)) at 4 rad/s, its heading flattened (y x 0.2), and flies 12 m/s (:257-284), hitting on each entry of its 0.5 m trigger sphere (:340-418: flyingShield_hit at it, LookRotation(forward), RPC_flyingShield_hit), destroyed at 3 s by the part (:225-249; plays its own Sounds/javelin); the noShield status for chaAdjust(3) = 3 s (:35211) turns her shield's MeshRenderers off (CharacterControl.cs:36060-36070, back at its end :16155): hideProp L 3 s; Yield 0.7 (:35430): standby at 1.2 s (:35232)",
        "builds": ["flyingShield_hit"],
        "cues": [
          [0, "voice", "homingShield1|homingShield2"],
          [0.5, "fx", "homingShield", {"y": 1, "d": 1}],
          [0.5, "hideProp", "L", {"kill": 3}]
        ]
      }
    }
  },
```

**Page lines, as corrected:**
- `SEQ.whale += "Honor: cast3", "12th Kingdom Knight: cast3", "Bubble Burst: cast3"`.
- `SEQ_SKILL.whale = {"@Honor": "honor", "@12thKingdomKnight": "12thKingdomKnight", "@BubbleBurst": "bubbleBurst"}`, merged with tto.md's `"@LeviathanBreach": "leviathanBreach"`.
- `LOWER_RANK.whale = ["malStorm"]` (skills_b.md Verification agrees).
- `CLIP_SKILLS["whale"]` as this report gives it.
- `OWN_TILE["whale"] = {"honor": ["cast3"], "12thKingdomKnight": ["cast3"], "bubbleBurst": ["cast3"]}`.
- `RANK_ICONS["whale"] = {"12thKingdomKnight": "whale_12thKingdomKnight2"}` (finding 1).
- P4 `around` and `OPTS += "around"` go to page_pipeline (finding 3).

**For the Bible (still only offered):**
- Finding 7's gate replaces finding 4.
- Finding 6 is refined by finding 2: the shield goes out to 11.98 m ahead at 0.50 s, swinging 3.5 m to each side.
- Findings 1-3, 5 and 7 of that list are confirmed.
