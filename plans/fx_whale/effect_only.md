# Whale: the skills with no body animation (effect-only tiles)

Research only (2026-11-13, office PC). I worked read-only: I wrote this report and files under
`checks/fx_whale_research/effect_only/` (git-ignored) and nothing else.

**What was run:**
- The probe, with `--probe` only: `uv run --no-project --with UnityPy python -I pipeline/wardrobe_fx.py whale --probe
  shield,overPresence,shieldReflect` (exit 0). Output: `probe.json` (three JSON objects, one after another).
- `node pipeline/clip_calls.js C:/Users/Jump/Desktop/12tails/DecompiledSource wardrobe/data whale` -> `clip_calls.txt`.
- The RPC listing `grep -nE "^\s*(public|private|protected|internal)[^(]*\bRPC_\w+\(" Whale.cs` -> `bb_rpc.txt` (76);
  `groups.txt` puts each one in one group, diffed against the listing (the same 76, none twice).
- `loads.py` -> `loads.txt`: every literal `Effects/` / `Voices/` / `Sounds/` load in Whale.cs (211) with the method or
  coroutine class that holds it.
- `pred.py <file> <from> <to>`: every junk predicate in a line range, evaluated T / F (`pred_autoshield.txt`,
  `pred_lasthope.txt`).
- `voice_check.py` (BB's Resources container and the rip for `lastHope1` / `lastHope2`), `shield_clip.py` (which
  AudioClip the `shield` prefab's AudioSource points at), `tto_cat.py` (TTO's catalog addresses, `tto_assets/2026-11-09`).
- `cues.json`: the one cue entry below, checked with `json.load`.

**Sources:**
- `C:\Users\Jump\Desktop\12tails\DecompiledSource\Whale.cs` (cited as `:line`), `CharacterControl.cs` (cited `CC:line`),
  `Game.cs`, `Whale_overPresence.cs`, `whale_kingdomKnight.cs`.
- TTO: `DecompiledSource_TTO_2026-11-02/methods.tsv`, `pseudo/Whale.c`, and the TTO catalog.
- The Bible's `12t_reference/whale-skill-reference.md` (cited "ref §") and its skill cards (`12t_projects/bible/index.html`,
  `assets.js`).
- `plans/fx_inventory.md` ("### whale").

The templates were the Mole's and the Chameleon's `effect_only.md`, and the Penguin's Frost Spike (a passive started by
being hit).

## Read this first

1. **No Whale active plays without a body clip.** Every key-dispatcher path reaches a coroutine that plays a clip:
   - `doSkill` (:6003-8016) itself calls no PlayAnimation / CrossFade / animation.Play.
   - `clip_calls.js` finds a clip for each of its 31 skill RPCs (the table below).
   - The eight cast-bar skills (Bubble Shield, Heavy Weight, Hydro Blast, Rejuvenate, Call To Arm, Salvation,
     Megalodon, Revitalize) go through `RPC_cast1` (cast1 / cast2) and then play `cast3` in their own `_cast`
     coroutine.
   - Honor, 12th Kingdom Knight and Bubble Burst play `cast3`. Homing Shield plays `flyingShield`.
   - Whale Wave / Mal Storm play `divingWave` / `divingStorm` with Diving Press, else `malStorm`.

   So no active needs a `root@` line.
2. **One passive draws an effect with no clip: Auto Shield (#261-263, Bible card `whale_autoShield`, icon
   `whale_autoShield3`).**
   - It is a roll on the receiving side of a direct hit (`RPC_AddDamage`, CC:4406-4595), not a key press.
   - On success it draws `Effects/shield` between the Whale and the attacker.
   - By the Penguin's Frost Spike precedent (a passive started by being hit, with no clip, gets a tile and procs on
     every play; Bison decision 6, Cat decisions 10 and 35), it gets **one effect-only tile, `"Auto Shield: root*@1"`**.
     Its cues are below.
3. **Every other passive was checked, and none draws anything on the Whale without a clip:**
   - Last Hope's only look is a voice that exists in neither BB's data nor TTO's (open question 2).
   - Harden Skin and Over Presence draw nothing.
   - The rest ride on a skill with a clip (the passives table).
4. **TTO** adds one active, Leviathan Breach (`RPC_leviathanCast` / `RPC_leviathanBreach`, clip `leviathanCall`,
   released: the tto researcher's). Its two Lv 100 passives draw without a clip:
   - Sovereign Impaler: the `impaler` marker on the Whale, and the `sovereignImpale` spear on the enemy.
   - Oceans Resilience: the `oceanResilience` look on the Whale.

   Neither is in `wardrobe/tto_released.json` (whale: clap, leviathanCall, wai), so by the released-list rule (Mole
   decision 15) they get no tile and no cue.
5. `wardrobe/fx_cues/whale.json` is `{}` today, so nothing here collides with an existing key.

## Accounting: every RPC_* in Whale.cs (76 definitions)

Listed with the grep above (`bb_rpc.txt`). The groups add up to 31 + 21 + 13 + 7 + 4 = **76**. Effect-only RPCs: **0**.

**Skill RPCs with their own clip (31).** For these, the clip column is what `clip_calls.js` reports, with the line of
the call. They are covered by the other researchers (attacks_emotes, skills_a, skills_b; the lead's split).

| RPC (definition) | Skill (Bible) | Clip (call) |
|---|---|---|
| RPC_nAttack1 :8269, _nAttack2 :8276, _nAttack3 :8283 | Normal Attack | nAttack1 :16524, nAttack2 :16808, nAttack3 :18007 |
| RPC_cAttack1 :8647 | Charge Attack | cAttack1 :18988, cAttack2 (loop) :18827 |
| RPC_shieldBash :8668 | Shield Bash (#114, the 3 s release) | shieldBash :20040 |
| RPC_cast1 :8718 | the cast bar (8 cast skills) | cast1 :21270, cast2 (loop) :20458 |
| RPC_sweep :8754 | Sweep | sweep :22287 |
| RPC_javelin :8761 | Javelin | javelin :23200 |
| RPC_honor :8878 | Honor | cast3 :23704 |
| RPC_shieldRush :8885 | Shield Rush | shieldRush :24445 |
| RPC_flyingShield :8935 | Flying Shield | flyingShield :25014 |
| RPC_swallow :8985 | Swallow | swallow :25543 |
| RPC_gobbleUp :9052 | Gobble Up | gobble :26384 |
| RPC_peninsulaImpale :9129 | Peninsula Impale | peninsulaImpale :27274 |
| RPC_peninsulaRound :9136 | Peninsula Round | peninsulaRound :27834 |
| RPC_kingdomKnight :9643 | 12th Kingdom Knight | cast3 :28640 |
| RPC_bubbleShield_cast :9889 | Bubble Shield | cast3 :29835 |
| RPC_heavyWeight_cast :9896 | Heavy Weight | cast3 :30364 |
| RPC_hydroBlast_cast :9967 | Hydro Blast | cast3 :30850 |
| RPC_rejuvenate_cast :10154 | Rejuvenate | cast3 :31469 |
| RPC_whaleWave :10161 | Whale Wave | divingWave :32117 / malStorm :32125 |
| RPC_malStorm :10168 | Mal Storm | divingStorm :32781 / malStorm :32789 |
| RPC_callToArm_cast :10336 | Call To Arm | cast3 :33329 |
| RPC_salvation_cast :10343 | Salvation | cast3 :33883 |
| RPC_megalodon_cast :10350 | Megalodon | cast3 :34317 |
| RPC_homingShield :10364 | Homing Shield (#422) | flyingShield :35302 |
| RPC_bubbleBurst :10478 | Bubble Burst (#403) | cast3 :35653 |
| RPC_revitalize_cast :10485 | Revitalize (#433) | cast3 :36329 |
| RPC_bowlingWhale :10492 | Bowling Whale | bowlingWhale1 :37013, bowlingWhale2 (loop) :36733 |
| RPC_grandTide :10559, RPC_grandTide0 :10566 | Grand Tide (and its end) | grandTide1 :37781, grandTide2 :37488; grandTide0 :38179 |

**Phases of those skills, inside their tiles (21).** They have no clip of their own and belong to the owners of the
skills above. The caller lines are from `grep` (each RPC's ActionEvent receiver is at :4177-5707).
- RPC_nAttack_hit :8290.
- RPC_cAttack2 :8654 is the release: `PlayAnimation("root", 0.2)`, standby. RPC_cAttack0 :8661 is the cancel: root,
  standby. Neither draws anything.
- RPC_shieldBash_hit :8675. RPC_cast0 :8725 is the cast cancel: standby, nothing drawn.
- RPC_javelin_fire :8768 (from the javelin coroutine :22967), RPC_javelin_hit :8835, RPC_shieldRush_hit :8892,
  RPC_flyingShield_hit :8942, RPC_swallow_hit :8992, RPC_gobbleUp_hit :9059.
- **RPC_wallPuncture_hit :9234**: Wall Puncture's proc. It is called from the hits of nAttack1-3 (:16314, :17204, :17568,
  :18380), Sweep (:21839, :22088) and Peninsula Impale (:26919): a roll that rides on those clips. See the passives table.
- RPC_kingdomKnight_attack :9806: the knights' volley, started every 3 s by `KingdomKnight()` (:9771, the owner's
  Update). The knights' own `kingdomKnight_ring2` is drawn by `whale_kingdomKnight.cs:132`. This is the 12th Kingdom
  Knight owner's (a summon, cut at 10 s).
- RPC_roundTable :9820: Knight of the Deep's Round Table, started from the charge coroutine when `hasSkill(273)`
  (:18855). It has `roundTable_ring` and its voices. The Charge Attack owner's.
- RPC_kingdomKnight_unsummon :9827 (:9790, :28799).
- RPC_hydroBlast_fire :9974 (:30751), RPC_megalodon_fire :10357 (:34482).
- RPC_homingShield_fire :10371 (:35194), RPC_homingShield_move :10458, RPC_homingShield_destroy :10468.
- RPC_bowlingWhale_hit :10499.

**The supplement skills (`sup_*`), the same in all 12 hero files: 13.**
- RPC_obsidianFang :10630 / _hit :10637, RPC_stunningGround :10680, RPC_psalmOfEnergy :10923.
- RPC_seaAegis :11093: Whale-themed, with `seaAegis_ring` and voices seaAegis1 / seaAegis2. Bat.cs:15297 loads the same
  files.
- RPC_assassinate :11280, RPC_zephyrLore :11287, RPC_mineWalker :11381, RPC_replenishment :11388, RPC_elementalBound
  :11517, RPC_divineChannel :11663, RPC_astralShift :11670, RPC_bloodCarnage :11861.
- The voice they share is `onSupport()` (`Voices/support` :10600; this one is in the rip).

The Bible leaves all 13 out of the Whale's roster: ref "Notes on judgment calls" 1, including `seaAegis`
(`WhaleSkill.cs` has no `seaAegis`). As the Penguin's and the Chameleon's reports say, they are a cross-class job if
they are ever wanted.

**Emotes, KO, mission: 7.** All of these have clips, so none is effect-only. They belong to the attacks / emotes owner.
- RPC_emotion :12208 (voice `Voices/chat` :40133) and RPC_emotion0 :12215.
- RPC_ko :15096 (ko1 / ko2 :46037 / :46068), RPC_dead :15103 (dead1 / dead2 :46399 / :46430, `deadEffect` :46461) and
  RPC_revive :15110 (voice revive :46775).
- RPC_activateIcon1 :14991 (the mission's channel, voice activate1 :45660). No tile, by Penguin decision 19.
- RPC_activateIcon2 :14998 (its end, voice activate2 :15064).

**Items, mount, coin, pet: 4.** RPC_useItem :12652, RPC_useMount :12709 (voices mount / cast :43989 / :44114),
RPC_useCoin :12762 and RPC_petEffect :14953.

**Other draws outside the RPCs.** `loads.txt` cross-checks this:
- Every literal Whale load in Whale.cs sits in one of the RPCs above, their `$RPC_*$` coroutine classes, `onSupport`,
  `createMalstormBolt` (:10188, Mal Storm's Diving Press bolt, called from its coroutine), or `LastHope()` (:9559 /
  :9590, the two voices, below).
- Update (:230-330) calls `GobbleUp()` :9102, `KingdomKnight()` :9650, `LastHope()` :9371 and `HardenSkin()` :10230.
  Of these, only `LastHope()` loads anything.
- `Start()` (:76-108) creates the Over Presence aura (`createOverPresence` :9905, the prefab field `this.overPresence`)
  when #313 is learned in game types > 4.

**Outside Whale.cs:** CharacterControl.cs loads these Whale effects:
- **`shield`** at CC:4595: Auto Shield, this report.
- `shieldReflect` CC:30920 and `shield` CC:30989: the charge's `shield` status in `AddDamage`. They are on the cAttack1
  clip: the Charge Attack owner's.
- `rejuvenate_hit` CC:8910, `honor_cast` CC:35561, `heavy` CC:35928, `bubbleShield` CC:35973, `salvation` CC:36033,
  `bubbleBurst` CC:44114: the statuses that clip skills give. Their owners cover them.

No other script outside Whale.cs and CharacterControl.cs loads a Whale effect (`grep -rln "Heroes/Whale/"`: the rest
are Game.cs's prefab, WhaleEquipment.cs's weapons, the mounts' nAttack voices and Bat.cs's Sea Aegis copy).

**TTO** (`methods.tsv`, class Whale, 54 RPCs):
- It keeps every BB skill RPC. The shared supplement / emote / item RPCs no longer appear under Whale (24 names, moved
  out of the class).
- It adds only `RPC_leviathanCast` and `RPC_leviathanBreach` (Leviathan Breach; `pseudo/Whale.c:10200-10205` loads
  `leviathanCall`, `leviathanCall_slam`, `leviathanCall_raise`).
- The rest is TTO's Row6 helpers: `WallPunctureStrike`, `AddImpalerStack`, `SovereignLance`, `SovereignImpact`,
  `OceanUpdate`, `OnRow6Took`, `Dolphin*`, `Leviathan*`.

## The passives, each one checked

| Passive (Bible) | Where it runs | Draws on the Whale, with no clip? | Tile? |
|---|---|---|---|
| **Auto Shield** #261-263 | RPC_AddDamage, receiver side (CC:4406-4595) | **yes: `Effects/shield`** | **yes, this report** |
| Last Hope #264 | `LastHope()` from Update (:9371-9625) | no: `lastHope` gives stats only (CC:35898-35911); `RPC_AddHeal` (:9617-9621) draws nothing; the voices lastHope1 / lastHope2 are missing (below) | no (open question 2) |
| Harden Skin #351-354 | `HardenSkin()` from Update (:10230-10266) | no: `RPC_AddStatus("hardenSkin")` (:10266); the apply is `deltaDef` only (CC:35913-35921); no load | no |
| Over Presence #313 / #314 | `Start()` -> `createOverPresence` (:86-92, :9905-9952) | no: the `overPresence` prefab is one node holding only `Whale_overPresence` (probe); `Whale_overPresence.cs` loads and instantiates nothing; the status is `moveMod` only (CC:35951-35955) | no |
| Wall Puncture #251-254 | `getWallPuncture()` (:9196) on the hits of nAttack1-3, Sweep, Peninsula Impale, Javelin | `wallPuncture_hit` at the struck target (:9247), on those clips | no (the hosts' owners, open question 4) |
| Tide Cutter #402 | inside Sweep (`tideCutter_ring` :22309, voices :22374 / :22405) | on the sweep clip | no (sweep owner) |
| Entended Wave #401 | inside the Normal Attack (`extendedWave1-3` :16554, :16850, :18045) | on the nAttack clips | no (attacks owner) |
| Shield Bash #114 | the charge release (`doReleaseCharge` :8486-8560 -> RPC_shieldBash) | its own clip `shieldBash` | no (attacks owner) |
| Knight of the Deep #273 (Round Table) | RPC_roundTable from the charge (:18855) | `roundTable_ring` on the cAttack1 clip | no (charge owner) |
| Shield Reflect #411 | the charge's `shield` status (CC:30920) | `shieldReflect` on the cAttack1 clip | no (charge owner) |
| Spiral Blast #423, Diving Press #443, Peninsula Asunder #442, Over Weight #413, Honor Stand #412, Wonder Belly #432, Bubble Burst's passive part, Reduced Cast #373 | inside skills with clips (`spiralBlast` :9997, `divingWave` / `divingStorm`, `asunderImpale` / `asunderRound` :27157 / :28013; the rest are numbers only) | in those skills' cues | no (others) |
| Culinary Tongue #121 / #122, Gourmet Heart #421 | the food path (GameGui.cs) | no | no |
| Super Size #131-134, Mega Size #431, Stat Plus, Super Stat Plus, Revised Skill / Magic / Art | stats; Super / Mega Size also scale the body (ref §4.12; Game.cs:2795 `Whale_tri` x 0.8 + 0.05 n) | no effect | no (open question 5) |

## Auto Shield: the one clip-less effect

### Trigger (CharacterControl.cs, worked by hand)
`RPC_AddDamage(nActionCode, nDamage, nKo, nHate, nForce, nAttackerID)` (CC:3680) runs when the Whale takes a direct hit.
Effect Damage goes through `RPC_AddEffectDamage` and never gets here.
- `gameObject` is the attacker, from `PhotonClient.ActorNrList[nAttackerID]` (CC:3774-3792).
- The block runs for a Whale (CC:4299). Outside Peninsula Round's `attack` (CC:4305-4315), it goes to `IL_3264`
  (CC:4406). Then:
  - `hasSkill(261)` (CC:4407);
  - not holding the charge, the `shield` status (CC:4415);
  - none of sleep / snowMan / snowBall / petrify / paralysis (CC:4423-4455).
- The level `num8` is 1, 2 at #262 (CC:4468) and **3 at #263** (CC:4480), which is the top rank.
- The roll: `Random.Range(0, 100) >= lckAdjust(num8 * 6 + 6)` skips the block (CC:4492). So it succeeds when the draw
  is under lckAdjust(24).
  - lckAdjust (CC:20658) is `floor(100 n / (n - c + 100))` with `n = c (1 + 0.01 LCK)`.
  - At LCK 1: n = 24.24, so floor(2424 / 100.24) = **24 %**. This is the Wolf's Double Art convention (plain stats).
- On success:
  - `RPC_AddHeal(264, 0, 0, 6, ...)`: **+6 SP** (CC:4500). AddHeal (CC:7130, :7444) loads and instantiates nothing.
  - The charge rank `num9` is 3 with #113 (CC:4510-4545). The hit is cut by `10 + 10 × 3` = 40 (CC:4546).
  - The effect (CC:4563-4595):
    - `position = hero + TransformDirection(0, 1, 1)` and `vector3 = forward`.
    - With an attacker: `vector3 = vFlat(attacker − hero).normalized` and `position = hero + vector3 + up`.
    - `Instantiate(Effects/shield, position, LookRotation(vector3))`.
    - So it is **1 m toward the attacker on the flat, 1 m up, facing the attacker**.
- Every junk predicate on CC:4299-4600 is false (`pred_autoshield.txt`, 48 of them, all F), so the straight-line
  reading above holds. Examples:
  - :4301 `15430 - 252037 = -236607` (the `!=` is false);
  - :4564 `273683 - 330332 = -56649` (`== -56648` is false);
  - :4596 `106021 - 539063 = -433042` (the `!=` is false), so `goto IL_1011`.
- KO is not changed. There is no voice (the block loads none). Nothing else in the code loads `Voices/shield`, which is
  an orphan file in the rip.

### Where it goes in the wardrobe
The attacker stands at the standing 10 m target point straight ahead, so the flat direction is the hero's facing. The
effect goes at **d 1, y 1, with the hero's rotation (no `rot`)**. That is also exactly the game's no-attacker fallback
(CC:4563 / :4568).

### The effect (probe, `probe.json`)
- EffectControl: life 1, afterLife 0, followPosition false, **followState false** (no cut time).
- One RingEmitter (life 0.3, 1 per 0.1 s, radius 0.2 -> 1.6 m, blue to violet, material `Line_DoubleLine1`, ringTri 24).
  It sits at local (0, 0, 1), turned −90° about x, so it is a ring standing up and facing out, 1 m further on.
- Its AudioSource is `shield` (playOnAwake).
  - The clip is pathID 188 in sharedassets4, which is the container's `gameassets/characters/heroes/whale/sounds/shield`
    and not `.../voices/shield` (pathID 217) (`shield_clip.py`).
  - `wardrobe_fx.rip_wav`'s sounds-first order picks that same `sounds/shield.wav` (0.475 s).
- Not in `plans/fx_inventory.md`: the inventory lists Whale.cs loads only, and this one is CharacterControl.cs's. The
  probe shows it is built only from parts the page has (EffectControl, RingEmitter, AudioSource), so it is **ready**.
  The TTO catalog has the same `whale/effects/shield`.

### Step length
The longest part is the effect's life, 1 s (its sound is 0.475 s). The Whale's idle `root` is 1.0 s, looped
(`wardrobe/data/whale/clips.json`). By the Mole's and the Cat's convention (Cat decision 9), the step is written held:
`root*@1`.

## Paste-ready

### 1. `wardrobe/index.html` SEQ: the whale line
The line is at index.html:1369 at this reading. Anchor on its text. If another researcher has changed the first
entries, keep theirs and append this one.

```js
  whale: ["Normal Attack: nAttack1 nAttack2 nAttack3", "Charge Attack: cAttack1 cAttack2*", "Cast: cast1 cast2*@0 cast3~",
    "Bowling Whale: bowlingWhale1@1 bowlingWhale2*@6", "Grand Tide: grandTide1 grandTide2*@3 grandTide0",
    // Auto Shield (passive #261-263) plays no animation: a direct hit on a Whale who is not charging rolls lckAdjust(24)
    // in RPC_AddDamage (CharacterControl.cs:4406-4492) and draws Effects/shield 1 m toward the attacker, 1 m up
    // (:4563-4595): its effect on the idle stance, every play, held 1 s (the shield's life) (2026-11-13,
    // plans/fx_whale/effect_only.md; the Penguin's Frost Spike)
    "Auto Shield: root*@1"],
```

### 2. `wardrobe/index.html` SEQ_SKILL (from index.html:3432): add a whale entry, merged with any other whale ids
```js
  whale: { "@AutoShield": "autoShield" },
```

### 3. `wardrobe/fx_cues/whale.json`: one entry
The file is `{}` today. The same text, checked with `json.load`, is in `checks/fx_whale_research/effect_only/cues.json`.

```json
  "@AutoShield:root": {
    "why": "Auto Shield 3 (#263, passive, top rank; passives on) has no clip: it is a roll inside RPC_AddDamage, the receiver's side of a direct hit (CharacterControl.cs:3680; the attacker from nAttackerID :3774-3792). For a Whale (:4299) not in Peninsula Round's attack (:4305-4315 -> IL_3264 :4406), with #261 (:4407), not holding the charge's shield status (:4415) and not asleep / snowMan / snowBall / petrified / paralysed (:4423-4455): rank 3 (:4468-4490), Random.Range(0, 100) >= lckAdjust(3 x 6 + 6) skips (:4492), so lckAdjust(24) = 24 % at LCK 1 (:20658); on success +6 SP (RPC_AddHeal(264, 0, 0, 6) :4500, nothing drawn), the hit cut by 10 + 10 x Charge Attack rank 3 = 40 (:4510-4546), and Effects/shield Instantiated at the hero + the flat unit direction to the attacker + 1 m up, LookRotation(that direction) (:4563-4595; no attacker: hero + TransformDirection(0, 1, 1), the facing); every junk predicate on the path false (:4299-4600, worked by hand). The attacker is the 10 m target point ahead (the standing rule), so 1 m ahead, 1 m up, the hero's facing. The tile plays the proc on every play (no p: the Penguin's Frost Spike, Bison decision 6). Effects/shield: EffectControl life 1, afterLife 0, no followState; one RingEmitter (0.2 -> 1.6 m, blue, life 0.3) 1 m ahead in its own frame; its AudioSource plays sounds/shield (the clip's pathID 188 = the container's whale/sounds/shield, not voices/shield; 0.475 s). No voice (Auto Shield loads none)",
    "cues": [
    [0, "fx", "shield", {"d": 1, "y": 1}]
    ]
  }
```
Put a comma after the closing `}` only if another entry follows. Every option used (`d`, `y`) is in
`wardrobe_fx_check.py`'s OPTS. Check the file with `py -3 -c "import json; json.load(open('wardrobe/fx_cues/whale.json',
encoding='utf-8'))"`.

### 4. `pipeline/wardrobe_skill_icons.py` EFFECT_ONLY (from :62): add the whale list
```python
               # the Whale's Auto Shield (2026-11-13, plans/fx_whale/effect_only.md)
               "whale": ["autoShield"]}
```
(This goes after the `"monkey": [...]` entry, whose closing `}` becomes `,`.)

The Bible card is `whale_autoShield` with `icon:"whale_autoShield3"` (index.html:19588; assets.js has
`whale_autoShield1-3`), so `best` finds the top rank. `wardrobe/data/icons/skills/whale/autoshield0-4.webp` exist.
`py -3 pipeline\wardrobe_skill_icons.py` then adds it with clips ["root"].

### 5. Build and check
No page part is missing. Once the whale cues are in, a plain `wardrobe_fx.py whale` builds `shield` from the cue file.
Alone, it would be:
```
uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py whale --fx shield
```
The `shield` prefab's own sound comes with it. Then run the class check (`wardrobe_fx_check.py ... --cls whale`).

## Parts needed
None. `shield` is EffectControl + RingEmitter + AudioSource, all of which the page builds.

## Left out (with reasons)
- **Last Hope (#264): no tile.** It draws nothing in the scene:
  - The `lastHope` status is ATK / DEF only (CC:35898-35911).
  - The heal `RPC_AddHeal(264, pool)` (:9617-9621) shows no effect.
  - The voices it loads, `Voices/lastHope1` / `lastHope2` (:9559 / :9590, `Random.Range(0, 2)`), are in neither BB's
    Resources container (only the icons `gamegui/icons/skills/whale/lasthope0-4` match), nor the rip, nor TTO's catalog
    (`voice_check.py`, `tto_cat.py`). So the game itself hits `Debug.LogError("Cannot find lastHope1 voice")` and is
    silent.

  The precedents for a passive that draws nothing: the Mole's passives table (no tile).
- **Harden Skin, Over Presence: no tile.** Nothing is drawn (the table above).
- **The 13 supplement skills: left out** (Penguin / Chameleon effect_only Q3; the Bible's roster).
- **The Auto Shield SP gain and damage cut:** numbers, nothing drawn.
- **The attacker's own hit:** that is the attacker's effect, not the Whale's.
- **TTO's Sovereign Impaler and Oceans Resilience: no tile, no cue.**
  - They are not released (`tto_released.json` whale clips: clap, leviathanCall, wai; Mole decision 15).
  - For the record, their prefabs are in TTO's catalog: `whale/effects/impaler`, `oceanresilience`, `sovereignimpale`,
    `sovereignimpale_rise`.
  - The `impaler` / `oceanResilience` looks come from `CharacterControl::AddWhaleRow6Status` (ref "Sovereign Impaler":
    "impaler is a stack marker only ... the FX"; `pseudo/CharacterControl.c:36580`, :36618). The spear falls on the
    enemy (`Whale::SovereignLance@0x1EC1AC0`).

## Open questions (each with my recommended answer)

1. **Auto Shield: a tile of its own, or a `p 0.24` roll somewhere?** *Recommend the own tile, playing every time*
   (Frost Spike, Berserker Rush / Fury Trance, Treasure Hunt: procs started by something other than a key press, with
   no clip, got own tiles with no `p`).
   - No other tile hosts it: the wardrobe has no tile where the Whale is hit.
   - The spot is the same whichever reading is taken: d 1, y 1 (toward the 10 m target point, or the no-attacker
     fallback).
2. **Last Hope: no tile.** *Recommend no tile.* There is nothing to see or hear; its voices exist nowhere. A tile would
   be the idle stance and the icon only. If the user wants every passive a tile anyway, the shape would be
   `"Last Hope: root*@1"` with an empty cue list, which `wardrobe_fx_check.py` would likely flag as an entry with no
   cue. I don't recommend it.
3. **The Charge Attack's own `shield` / `shieldReflect`** (CC:30920 / :30989, a hit blocked while charging) need a hit
   on the Whale, like Auto Shield, but they ride on the cAttack1 clip. *Recommend that the Charge Attack owner decide.*
   For them: both spawn at `mTransform.position + TransformDirection(0, 1, 0.7)` with the hero's rotation (CC:30920,
   :30989), i.e. d 0.7, y 1, no `rot`, when a hit lands during the charge.
4. **Wall Puncture (#251-254)** is a proc on clip hosts: lckAdjust(40) = 40 % at rank 4 (`getWallPuncture` :9196,
   `lckAdjust(10 × lv) > Random.Range(0, 100)`), and `wallPuncture_hit` at the struck target (:9234-9290). *Recommend
   the Chameleon's Critical Plus shape* (Chameleon decision 12): its own tile on nAttack1, plus a `p 0.4` roll beside the
   hits of nAttack1-3, Sweep and Peninsula Impale (and Javelin). That is for the attacks / skills owners. It is not
   effect-only.
5. **Not an effect, flagged for the lead:** with "passives on", Super Size 4 + Mega Size give the Whale's mesh
   `Whale_tri` the scale `0.8 + 0.05 × 5` = 1.05 (Game.cs:2795, ref §4.12; 0.8 with neither). The page does not touch
   `Whale_tri` (no match in index.html or wardrobe_data.py). *Recommend leaving it to the user* (a body-size change,
   outside the effects work). It is mentioned only because it changes where hand-bound effects sit.

## Offers for the Bible (not written there)
1. Auto Shield's look:
   - `Effects/shield` 1 m toward the attacker on the flat and 1 m up, facing them (no attacker: 1 m ahead, 1 m up)
     (CC:4563-4595), with its own sound `sounds/shield`.
   - The SP is `RPC_AddHeal(264, 0, 0, 2 × lv)` (CC:4500).
   - The card already has the chance and the cut; the spot is new.
2. Last Hope is silent in game: BB loads `Voices/lastHope1` / `lastHope2` (Whale.cs:9559 / :9590), which BB's data does
   not hold and TTO's catalog does not either.
3. Over Presence's aura object draws nothing: the prefab holds only the `Whale_overPresence` script.
4. Orphan Whale voices in BB's data that no BB code loads by a literal path: `voices/shield`, `honorStand1/2`,
   `giganticStrike1/2`, `finalMove1/2`, `transform1/2`, `peninsulaAsunder1/2`, `penninsulaImpale1/2`. I checked this with
   `grep -rl 'Voices/<name>"'` over DecompiledSource: 0 files each, and Whale.cs has no `peninsulaAsunder` /
   `giganticStrike` / `finalMove` at all. The only computed Whale voice loads are the chat (`chat` + 1-5, :40133) and the
   emote's `Voices/` + its name (:40141), and none of these names is an emote. They are likely cut content. This is
   worth a line only if the Bible tracks unused assets.

## Verification (2026-11-13)

Checked on the office PC, read only; probes in `checks/fx_whale_research/verify/` (the `ae_` files: `ae_probe.txt` =
`wardrobe_fx.py whale --probe ...,shield,shieldReflect,overPresence`, exit 0; `ae_audio.txt`; `ae_tto_cat.txt`;
`ae_clip_calls.txt`; `ae_eo_blocks.py`). **The Verification wins over the report body.**

**Confirmed (no change):**
- 76 RPC definitions in Whale.cs (the same grep); clip_calls.js finds a clip for all 31 skill RPCs, as tabled; no active
  plays without a clip.
- Auto Shield, every step re-read (CharacterControl.cs:4299-4596, the predicates worked by hand): the Whale gate :4299,
  IL_3264 :4406, #261 :4407, no `shield` status :4415, the five status skips, rank 3 at #263, `Random.Range(0, 100) >=
  lckAdjust(num8 * 6 + 6)` skips; lckAdjust (:20658-20671) = floor(100 x 24.24 / 100.24) = **24 %** at LCK 1; `RPC_AddHeal
  (264, 0, 0, num8 * 2, ...)` = +6 SP; the cut `nDamage - 10 - 10 x num9` = 40 at #113; the spot `hero + vFlat(attacker -
  hero).normalized + up`, `LookRotation(that)` (no attacker: `TransformDirection(0, 1, 1)`, the facing) -> **d 1, y 1, no
  rot**. The probe: shield = EffectControl life 1, no follow, AudioSource `shield`, one RingEmitter (Line_DoubleLine1)
  at local (0, 0, 1): ready.
- Last Hope's voices lastHope1 / lastHope2 (:9559, :9590) are in neither BB's container, the rip, nor TTO's catalog (the
  same 114 whale voices, `ae_tto_cat.txt`), so Sheep decision 10's TTO fix has nothing to offer: no tile stands.
  Over Presence's prefab is the one node with `Whale_overPresence` (probe), whose script loads and instantiates nothing;
  Harden Skin only adds the `hardenSkin` status (:10266).
- Sovereign Impaler / Oceans Resilience: not in `tto_released.json` (whale clips clap, leviathanCall, wai): no tile, no
  cue (Mole decision 15).
- Block 3 parses; its key `@AutoShield:root` is the SEQ name without spaces; `d`, `y` are in OPTS; `whale_autoShield3` is
  in assets.js and `best` picks it; EFFECT_ONLY's insertion point is as described.

**Findings:**

1. **Shield Reflect (#411) fell between this report (Q3: "the Charge Attack owner decide") and attacks_emotes.md (left
   out as "the receive side").** It is a passive with its own Bible card (`whale_shieldReflect`, icon
   `whale_shieldReflect5`) whose only look, `Effects/shieldReflect` at `TransformDirection(0, 1, 0.7)` with the hero's
   rotation (CharacterControl.cs:30869-30920), comes from a hit on the held charge: the same kind of hit-started passive
   as Auto Shield, so by this report's own rule it gets a tile. Decided in attacks_emotes.md's Verification 4 (tile
   `"Shield Reflect: cAttack1 cAttack2*@2.29 root~@0.2"`, entry `@ShieldReflect:cAttack2`, the full block there): it is
   on the charge's clips, not effect-only. Q3's spot (d 0.7, y 1, no rot) is right.

2. **Q4 (Wall Puncture) cannot go on nAttack1.** The Chameleon's Critical Plus shape needs a host whose hit reaches the
   10 m point; the Normal Attack's box is 4 + 3 = 7 m (Whale.cs:16444, :17334, :18509), Sweep's 6 / 5 m, and Javelin's
   proc draws nothing (skills_b.md). Only Peninsula Impale's 12 m box reaches it. Decided in attacks_emotes.md's
   Verification 5: `"Wall Puncture: peninsulaImpale"` (every stab a proc, entry `@WallPuncture:peninsulaImpale`, the full
   block there) plus `"Peninsula Impale: peninsulaImpale"` so the Peninsula Impale tile stays in the list (a clip a SEQ
   plays leaves the single-clip list, index.html:3700); the `p 0.4` rolls stay in skills_b's hosts.

3. **Block 1 (the SEQ line) and block 2 (SEQ_SKILL) are superseded by the merged lines** in attacks_emotes.md's
   Verification 6 (they hold `"Auto Shield: root*@1"` last and `"@AutoShield": "autoShield"`). Block 4 (EFFECT_ONLY
   `"whale": ["autoShield"]`) stands, and goes in with attacks_emotes.md Verification 3's `OWN_TILE["whale"]`.

4. **Missed in the accounting: the Bible's eight `onlyServer: "reborn"` Whale skills** (Tidal Reach, Abyssal Pierce,
   Bulwark Chorus, Leviathan Tide, Ocean Feast, Last Bulwark, Pod Call, Maelstrom Abyss; 12t_projects/bible/index.html:
   19620-19627). They are the Reborn client's, neither BB nor TTO (no Whale.cs or TTO RPC for them): out of scope, as the
   Mole's effect_only Verification 3 put its five. No tile, no cue.

5. **Line nits:** `createOverPresence` is defined at Whale.cs:9903 (its call at :92); the report's ":9905" is a line
   inside it.
