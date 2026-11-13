# Rabbit: the skills with no body animation (effect-only tiles)

Research only (2026-11-13, office PC). Read-only researcher: nothing in the repo was changed but this report and files
under `checks/fx_rabbit_research/effect_only/` (git-ignored). The probes ran with `--probe` only:
- `uv run --no-project --with UnityPy python -I pipeline/wardrobe_fx.py rabbit --probe
  nAttack_fire,nAttack_hit,fromTheAbove_ring,kneeShot_hit,maimShot_hit,herbFinder,snipeShot_hit,bounce1,bounce2` (exit 0;
  `probe.json`, summary `probe_summary.txt`).
- The same with `circleShot_hit,contract_ring,fourShot_hit,mall,tenShot_hit,allHpDrug1` (`probe2.json`, a cross-check
  for the other owners).
- `wardrobe_fx_tto.py rabbit --probe kneeShot_hit,herbFinder,snipeShot_hit` (exit 1: "not in TTO's catalog under
  gameassets/characters/heroes/rabbit/effects/: ['herbFinder', 'kneeShot_hit', 'snipeShot_hit']", `tto_probe.err`).

Sources (this PC's paths; the home PC has them under `D:\12tails\...`):
- `C:\Users\Jump\Desktop\12tails\DecompiledSource\Rabbit.cs` (cited `:line`), `CharacterControl.cs`, `Herb.cs`.
- The TTO method table and pseudo-C (`DecompiledSource_TTO_2026-11-02/methods.tsv`, `pseudo/Rabbit.c`, cited TTO1102).
- The Bible's `12t_reference/rabbit-skill-reference.md`, skill cards (`12t_projects/bible/index.html`), `assets.js`.
- `node pipeline/clip_calls.js .../DecompiledSource wardrobe/data rabbit` (`clip_calls.txt`), `pipeline/clip_flow.js`
  per RPC (`flow_RPC_*.txt`), `plans/fx_inventory.md` "### rabbit", `wardrobe/data/rabbit/clips.json`, the BB rip's wavs.

Helpers in `checks/fx_rabbit_research/effect_only/`:
- `tools/loads.py` → `loads.txt`: all 193 literal `Heroes/*/Effects|Voices|Sounds` loads in Rabbit.cs, with the method
  holding each.
- `tools/pred.py`, `tools/clean.py`: every junk predicate (`a - b ==/!= c`) in a line range evaluated T/F. `clean.py`
  prints the code with them replaced by `[T]` / `[F]`.
- `cues.json`: the paste-ready cue entries, checked with `json.load`.

Templates followed: `plans/fx_mole/effect_only.md` and `plans/fx_chameleon/effect_only.md`, and the earlier classes'
`decisions.md`.

## Result

**No Rabbit active is effect-only.** The key dispatcher `doSkill` (:6391-8807; its `rab_*` literals :6586-7596) starts
an RPC for every BB active, and each one plays a body clip (`clip_calls.js`: 32 RPCs with skill clips). The three TTO
actives (Bounty Hunt, Coin Ricochet, Medic Turret) start their clip through `Row6Begin` → `BaseHero::PlayAnimation(cmd,
0.1)`:
- `TTO1102:Rabbit.<RPC_bountyHunt>d__352` (pseudo/Rabbit.c:3321), `<RPC_coinRicochet>d__343` (:6371) and
  `<RPC_medicTurret>d__334` (:13131).
- `Rabbit::Row6Begin` is at :38983, and its PlayAnimation call 48 lines further down.

**Four passives have an RPC of their own that plays no clip.** Each is checked below:

| Passive (Bible card, icon) | RPC (no clip) | Started from | Draws | Tile |
|---|---|---|---|---|
| **From the Above** #421 (`rabbit_fromTheAbove5`) | `RPC_fromTheAbove` :9605 (coroutine :21964-22275) | `doNormalAttack` (:8944-8997) while Bounce is airborne | `nAttack_fire` 12 m above the hero, aimed down at the target; `nAttack_hit` at the hit | **its own tile on Bounce's clips** (block 1-4), the hero hidden |
| **Knee Shot** #402 (`rabbit_kneeShot5`) | `RPC_kneeShot_hit` :9669 | Maim Shot's hit, a 20 % roll (:23256-23294) | `kneeShot_hit`: **not in BB's Resources nor TTO's catalog**, so nothing is drawn | no tile; in Maim Shot `maimShot_hit` becomes `p 0.8` (block 5) |
| **Snipe Mastery** #431 (`rabbit_snipeMastery5`) | `RPC_snipeShot_hit` :11435 | every Normal Attack hit, in place of `nAttack_hit` (:17594-17631, :18265-18302) | `snipeShot_hit`: **missing in BB and TTO**, so nothing is drawn | no tile; the Normal Attack owner's call (Open question 1) |
| **Herb Finder** 1-2 #321/#323 (`rabbit_herbFinder*`) | `RPC_herbFinder` :10532 | `Herb.cs` OnGUI: a Rabbit clicking a field herb within ~1.7 m (:140-222) | `herbFinder`: **missing in BB and TTO**, so nothing is drawn | no tile (Open question 3) |

So **one effect-only tile** gets cues: **From the Above** (`"From the Above: bounce1@9.5 bounce2@1.4"`, 17 cues, built only
from parts the page already has). The other three draw nothing in either game. The game logs "Cannot find
kneeShot_hit / snipeShot_hit / herbFinder Effect" (:9701, :11467, :10564; the same strings in TTO1102 pseudo/Rabbit.c),
and the wardrobe follows the game.

`wardrobe/fx_cues/rabbit.json` is `{}` today, so nothing here collides.

## Read this first

1. **From the Above is not a body-less skill in the dispatcher's sense.** It rides on Bounce's airborne state:
   - The Normal Attack key, while `myCommand == "bounce"`, starts `RPC_fromTheAbove` in place of `RPC_nAttack`.
   - RPC_fromTheAbove plays no clip. The hero is hidden in the sky (the `hide` status turns all her Renderers off,
     CharacterControl.cs:32818-32848).

   By the Chameleon's Critical Plus / Clear Arrow precedent (decisions.md 12, 13: a skill on another skill's clip gets
   its own tile, `OWN_TILE`, not `EFFECT_ONLY`), its tile is **Bounce's clips with the air shots added**. Its keys are
   `@FromtheAbove:bounce1` / `@FromtheAbove:bounce2`.
2. **The Bounce tile's own timeline is the Bounce owner's.** My tile copies it from the code (cited below), because the
   air shots fall inside it. Bounce's tile, passives on, already shows From the Above's landing ring (`fromTheAbove_ring`
   **in place of** the `bounce2` effect, :21820-21875), and that ring is in my tile too.

   A cross-check for that owner: by the same code the page's `"Bounce: bounce1 bounce2"` has no air time. The game holds
   the hero hidden for 8.6 s at rank 2. Bounce's own tile would be `"Bounce: bounce1@9.5 bounce2@1.4"` with the same
   cues as mine minus the shots.
3. **Three of the Rabbit's own effect prefabs do not exist.** BB's `resources.assets` container (the probe's KeyError)
   and TTO's catalog both lack `kneeShot_hit`, `snipeShot_hit` and `herbFinder`.
   - The game draws nothing there, so a Knee Shot proc shows Maim Shot's hit without its `maimShot_hit` puff.
   - With Snipe Mastery (passives on), **every Normal Attack hit shows no hit effect**: its `RPC_nAttack_hit` is skipped
     for the missing `snipeShot_hit`.

   This changes the Normal Attack owner's entry (Open question 1). The same check found five more missing prefabs in
   other owners' skills (`probe2.json`): `circleShot_hit`, `fourShot_hit`, `tenShot_hit`, `contract_ring`, `mall`.
   None of these is in `plans/fx_inventory.md` (it lists only prefabs that exist, so it says nothing of these).
4. **The rip folder is not the authority.** `RippedAssets/.../rabbit/effects/` names some prefabs differently
   (`allHpDrug.prefab` for the container's `allHpDrug1`, which the probe reads). The container is the authority, and the
   probe reads it.

## Accounting: every RPC_* in Rabbit.cs (88 definitions)

`grep -nE "^\s*(public|private|protected|internal)[^(]*\bRPC_\w+\(" Rabbit.cs` gives 88 definitions. The groups below add
up to 32 + 28 + 4 + 13 + 11 = 88. "Clip" is what `clip_calls.js` / `clip_flow.js` find. "Owner" is the report that covers
the skill: skills = skills_a / skills_b, attacks = attacks_emotes.

**Skill RPCs that play a body clip (32):**

| RPC (:line) | Skill | Clip | Owner |
|---|---|---|---|
| nAttack :9105 | Normal Attack (+ Bouncing Bullet #401, Snipe Mastery #431, Hyper Shot) | nAttack (:17854) | attacks |
| cAttack1 :9357 / cAttack2 :9364 | Charge Attack (+ Dead Shot #411) | cAttack1, cAttack2 loop (:18921, :18636) / cAttack3 (:19318) | attacks |
| cast1 :9487 | the mix channel (Mix, Shake, Miracle Blend, Sticky Gum, Acidic Field, Healing Field) | mix1, mix2 loop (:20455, :20259) | skills |
| bounce :9591 / bounce0 :9598 | Bounce (+ From the Above's landing ring) | bounce1 (:21238) / bounce2 (:21571) | skills |
| statScan :9612 | Stat Scan | statScan (:22755) | skills |
| maimShot :9619 | Maim Shot (+ Knee Shot #402) | maim (:23486) | skills |
| mix_cast :9712, shake_cast :9726, miracleBlend_cast :9740 | Mix, Shake, Miracle Blend (+ Extra Potion #412, Miracle Drop #422) | mix3 (:24141, :25018, :25932) | skills |
| stickyGum_cast :10025, acidicField_cast :10099, healingField_cast :11275 | Sticky Gum, Acidic Field, Healing Field | mix4 (:26841, :27343, :37941) | skills |
| medicalShot :10202 | Immune / Boost / Heat / Life Shot | medicalShot (:28612; gilShot :28552) | skills |
| rapidTrance :10425 | Rapid Trance | rapidTrance (:29199) | skills |
| gorgonShot :10432 | Gorgon Shot | gorgonShot (:29859) | skills |
| gilShot :10482 | Gil Shot | gilShot (:30539) | skills |
| backpack :10687 | Backpack (+ Big Bag #423's `bigbag_ring`, :31024-31041) | backpack (:31428) | skills |
| fourShot :10737, circleShot :10787 | Four Shot, Circle Shot (+ Ten Shot #433's +10 dmg) | fourShot (:32022), circleShot (:32945) | skills |
| mall :10837, mall_setup :10844, mall_open :10869 | Mall | mall1 loop (:33439, :10854), mall2 loop (:33860) | skills |
| truceTrading1 :10930 | Truce Trading & Co. | truceTrading loop (:34233) | skills |
| shootingArray :10944 | Shooting Array | shootingArray (:35775) | skills |
| shotgun :11037 | Customized Shotgun (worn shotgun only, `isShotgun()` :11098) | nAttack (:36492) | attacks |
| millionaire :11261 | Millionaire | millionaire (:36834) | skills |
| diamondShot :11385 | Diamond Shot | gilShot (:38454) | skills |
| tenShot :11478 | Ten Shot | tenShot (:39086) | skills |
| extravagance :11528 | Extravagance | extravagance (:40003) | skills |
| contract :11535 | Contract | truceTrading loop (:40631) | skills |

The table has 32 RPCs in 23 rows.

**Phases of those skills, with no clip of their own (28):**

| Skill | Phase RPCs |
|---|---|
| Normal Attack | nAttack_hit :9112 |
| Charge Attack | cAttack0 :9371 (the cancel: `CrossFade("root", 0.2)` :20022, no effect), cAttack_hit :9378 |
| Maim Shot | maimShot_hit :9626 |
| Mix, Shake, Miracle Blend | mix_create :9719, shake_create :9733, miracleBlend_create :9747, potion_hit :9754 (a picked potion's burst) |
| Sticky Gum, Acidic Field | stickyGum_create :10032, acidicField_create :10106 |
| Medical Shots | immuneShot_hit :10209, boostShot_hit :10252, heatShot_hit :10295, lifeShot_hit :10338 |
| Gorgon Shot, Gil Shot | gorgonShot_hit :10439, gilShot_hit :10489 |
| Backpack, Four Shot, Circle Shot | backpack_hit :10694, fourShot_hit :10744, circleShot_hit :10794 |
| Mall | mall_close :10876 (plain method, no load) |
| Truce Trading | truceTrading2 :10937. It plays the emote clips `cheer` / `cry` (:34739, :34843), with truceTrading_success / _fail and the voices tradeSuccess / tradeFail. `clip_calls.js` misses these because they are emote clips. |
| Shooting Array | shootingArray_hit :10951, shootingArray_finalhit :10994 |
| Customized Shotgun | shotgun_hit :11044 |
| Healing Field | healingField_create :11282 |
| Diamond Shot, Ten Shot | diamondShot_hit :11392, tenShot_hit :11485 |
| Contract | contract_create :11542 (the mercenary) |

**The passives' own RPCs, with no clip (this report, 4):** fromTheAbove :9605, kneeShot_hit :9669, herbFinder :10532,
snipeShot_hit :11435.

**The supplement skills (`sup_*`), in all 12 hero files (13):** obsidianFang :12039 / _hit :12046, stunningGround :12089,
psalmOfEnergy :12329, seaAegis :12499, assassinate :12686, zephyrLore :12693, mineWalker :12787, replenishment :12794,
elementalBound :12923, divineChannel :13069, astralShift :13076, bloodCarnage :13267. They are not Rabbit skills (the
Bible's judgment call, rabbit-skill-reference.md:42-51; the Penguin / Mole precedent). The voice they share, `onSupport`,
is not in this rip either.

**Shared by every class (11):** emotion :13614 / emotion0 :13621, useItem :14058, useMount :14115, useCoin :14168,
petEffect :16365, activateIcon1 :16403 / activateIcon2 :16410 (the mission; no tile, Penguin decision 19), ko :16450,
dead :16457, revive :16464. The attacks / emotes owner covers them.

**Effect-only actives: 0.** Every literal Rabbit load in `loads.txt` sits in one of the RPCs above. The exceptions are
`$millionaire_createPeppon` and `$onNormalAttackHit`, which belong to Millionaire and to the weapon procs, and the shared
`onSupport`.

**Outside the RPCs:**
- **Rabbit.Update** (:240-440) draws one thing: `RPC_createEffect("autoLife")` (:300), with RPC_AddHeal, when the Rabbit
  dies while holding Life Shot's `autoLife` status. That is Life Shot's target-side effect, the Life Shot owner's (a
  status look on whoever was shot).
- **The Herb** (`Herb.cs`): Herb Finder, below.

**TTO** (methods.tsv, Rabbit) keeps every BB RPC above and adds `RPC_bountyHunt`, `RPC_coinRicochet`, `RPC_medicTurret`
and `RPC_medicTurret_create`. Its action strings add `RPC_bountyClaim`, `RPC_coinRicochet_pay` and
`RPC_truceTrading_fire*`, the phases of those skills and of Truce Trading, and `RPC_Fishing` / `RPC_Fishing0`, a shared
activity. All three TTO skills play their clip through Row6Begin, as above. TTO adds no skill without a body. TTO's
`RPC_fromTheAbove` (`<RPC_fromTheAbove>d__180`, pseudo/Rabbit.c:9238) keeps BB's strings: nAttack, nAttack_fire,
RPC_nAttack_hit, bounce, HyperShot. I did not re-trace its numbers, and BB's code is the content.

## The passives, each one checked

| Passive (Bible) | Where it runs | Draws a look of its own? | Tile? |
|---|---|---|---|
| Combo (nAttack 1-4), Charge Attack ranks, Hyper Shot 1-4 (#131-134) | ranges and damage (getNormalAttackLv :9494, getHypershotLv; the "HyperShot" screen message) | no | no |
| Stat Plus, Super Stat Plus, Revised Skill / Magic / Art (#404 / #414 in returnMPSP :8808) | stats, refunds | no | no |
| Medical Enhancement 1-3, Alchemist Lab 1-4, Med Research #432 | durations, levels, the town lab | no | no |
| Bunny Bargain 1-4, Skill Bargain #413, Special Deal 1-4, New Order #444, Diamond Shot's +20 (#403 in gilShot) | money, shops, the mercenary | no | no |
| Dead Shot #411 | Charge Attack's head-shot damage through the sniper camera (:19445-19468) | no (damage only) | no |
| Bouncing Bullet #401 | inside RPC_nAttack (:17459-17527, the ricochet path :18097-18302, game type > 4, shown: Chameleon decision 42): `bouncingBullet`, `bouncingBullet_hit`, voice `bouncingBullet`, sound `nAttack` | yes, on every Normal Attack | no: the Normal Attack tile shows it (passives on), the Bison's Power Hammer precedent (Bison decision 10) |
| Extra Potion #412, Miracle Drop #422 | Mix's bottles 3 → 5 (mix_cast :23891), Miracle Blend's extra kinds (:25603) | inside those skills, on every play | no (their tiles, passives on) |
| Big Bag #423 | Backpack's `bigbag_ring` (:31024-31041); Herb Finder always succeeds (:10624) | inside Backpack, on every play | no (Backpack's tile) |
| Customized Shotgun 1-2 (#353/354) | the Normal Attack becomes RPC_shotgun with a worn shotgun (:9042-9076, `isShotgun()` :11098) | yes, a worn-item variant | no (the attacks owner's `worn` case) |
| **From the Above #421** | the air shot RPC_fromTheAbove (:8944-8997), the landing ring and stomp in RPC_bounce0 (:21608-21652, :21820-21840) | yes; the Bounce tile shows the ring, and nothing shows the air shots | **its own tile** |
| **Knee Shot #402** | Maim Shot's 20 % roll (:23256-23273) → RPC_kneeShot_hit **in place of** RPC_maimShot_hit (:23288-23325) | no: kneeShot_hit is missing in both games | no; Maim Shot carries the roll (block 5) |
| **Snipe Mastery #431** | the Normal Attack's hits: RPC_snipeShot_hit **in place of** RPC_nAttack_hit (:17594-17631, :18265-18302; the shotgun :36313) | no: snipeShot_hit is missing in both games | no (Open question 1) |
| **Herb Finder 1-2** | Herb.cs OnGUI → RPC_herbFinder | no: herbFinder is missing in both games | no (Open question 3) |

## How each reads (junk predicates worked by hand: `pred.py` / `clean.py`)

### From the Above (#421, passive; the air shot and the landing)

**The press** (`doNormalAttack` :8876-9101; `pred.py` 8878-9010):
- `vector = a - mTransform.position` (:8917), where a = `targetArray[0]`, the target point. The guards :8915 and :8918
  are true.
- The actionState is not `standby` (:8929) and not `run` (:8935). Then, all needed (:8944-8976):
  - `hasSkill(421)`;
  - `actionState == "attack"`;
  - `myCommand == "bounce"`;
  - `Time.time > actionTime + 1`;
  - `isTimeOut("nAttack") == 0`.

  The junk predicates between them are all false (8948 / 8956 / 8964 / 8972 / 8980: F).
- Then `StartCoroutine(RPC_fromTheAbove(position, vector, 0))` (:8984), and `ActionEvent` (:8997).
- Without #421 the press does nothing while she is in the air (`break` :8946).

**RPC_fromTheAbove** (`$RPC_fromTheAbove$26940`, MoveNext :22067-22275; `pred.py` 22076-22272):
- **case 0** (the press): `addTimeOut("nAttack", 1.5)` (:22247), then `addTimeOut("bounce", agiAdjust(36))` (:22250; :22248
  T). Then:
  - `firePos = mPos + 12 up` (:22253; :22251 T);
  - `fireDir = tDir - 12 up` (:22256; :22254 T);
  - `fireRot = LookRotation(fireDir)` (:22259; :22257 T).

  :22260 is T, so the next stop is `Yield(2, 0.1 s)` (:22272).
- **case 2** (+0.1 s):
  - It loads `Effects/nAttack_fire` (:22087) and Instantiates it at firePos, fireRot (:22099). Every guard in case 2 is F.
  - For the owner it raycasts from firePos along fireDir, range `16 + 5 × getNormalAttackLv()` (:22129, :22134).
  - On a hit: `RPC_nAttack_hit(hit.point, forward)` (:22140). This is the plain hit, not snipeShot_hit: Snipe Mastery is
    not read here (Bible rabbit-skill-reference.md:565).
  - Then the damage (:22202) and `YieldDefault(1)` (:22234) → Block_10 → the end.
- **RPC_nAttack_hit** (:9112-9150): `nAttack_hit` at the hit point with **the hero's rotation** (:9135).

**Geometry** (the 10 m ground target point; the hero stands on the ground while hidden):
1. tDir = (0, 0, 10), so fireDir = (0, -12, 10) from (0, 12, 0).
2. Pitch = atan2(12, 10) = **50.19 deg down**: Unity Euler x +50.19, after the hero's facing.
3. The ray is sqrt(12² + 10²) = 15.62 m long, within the range (16 at Combo 0, 36 at Combo 4). It meets the ground at
   **d 10**: `nAttack_hit` at d 10, the same frame (a raycast).

**When the shots come** (Bounce at rank 2, the Bible's max; :21219-21379):
- The bounce starts at 0. `actionTime = Time.time` (:21223), so the first press passes `> actionTime + 1` at **1.0 s**.
- Each shot arms a 1.5 s `nAttack` timeout (:22247), so a held attack presses at **1.0, 2.5, 4.0, 5.5, 7.0, 8.5 s**. The
  shots fire 0.1 s later: **1.1, 2.6, 4.1, 5.6, 7.1, 8.6 s**.
- The landing starts at 8.9 s and sets `myCommand = "bounce0"` (:21746), which ends the presses. So there are 6 shots
  (Open question 2).

**Bounce's timeline, which the tile sits on** (the Bounce owner's; traced here because the shots fall inside it):
- **0.** IL_160 (:21219-21248):
  - attack / bounce, `addTimeOut("bounce", agiAdjust(30))`;
  - `PlayAnimation("bounce1", 0)` (:21238), a cut;
  - the voice: for the owner, `Random.Range(0, 2) == 0` (:21279) gives bounce1 (:21289 → Block_82 PlayOneShot :21383),
    else bounce2 (:21320 → Block_27 PlayOneShot :21363).

  Then `Yield(2, 0.5)` (:21357).
- **0.5.** `bounce1` at the hero's position and rotation (:21019-21031; EffectControl life 0.5, its AudioSource `bounce1`).
  Then `Yield(3, 0.4)` (:21375).
- **0.9.** `addStatus("hide", 1, 4 × 2 + 1)` (:21068) and `mBounceTimer = Time.time + 8` (:21073).
  - `hide`: layer 2, and every Renderer under the hero off, the pet told OnParentHide (CharacterControl.cs:32818-32867).
  - Then a FixedUpdate loop (:21379) moves her by the keys (:21134-21190) until `Time.time > mBounceTimer` (:21108).
- **8.9.** `RPC_bounce0` (:21114). In RPC_bounce0 (:21430-21925):
  - at its start (:21740-21808): `bounce0`, voice `bounce0` (:21796, PlayOneShot :21808);
  - with #421: **`fromTheAbove_ring`** at the hero's position and rotation (:21820-21840, :21822 / :21838 T), **in place
    of** the `bounce2` effect (the else :21857-21875);
  - then `Yield(2, 0.6)` (:21908).
- **9.5.** `removeStatus("hide")` (:21566), and `PlayAnimation("bounce2", 0)` (:21571), a cut.
  - **9.9:** the stomp: `FindAreaTarget(3 × rangeMod)` and `hit(421, ..., atk, KO 20)` (:21608-21652). No effect.
  - **10.3:** standby (:21688).

**The prefabs** (probe; all "ready" in fx_inventory.md:579, :605):

| Prefab | What it is |
|---|---|
| `nAttack_fire` | EffectControl life 1, no follow. A LineEmitter tracer (life 0.1, local velocity +z 10) and a one-shot smoke puff (`Rabbit_nAttack_smoke`). Its own AudioSource `nAttack` (0.996 s) on awake. |
| `nAttack_hit` | EffectControl life 1. A one-shot particle puff and a 24-line LineEmitter burst. |
| `fromTheAbove_ring` | EffectControl life 2. Two LineEmitter and two RingEmitter dust bursts, all with **Delay 1.0**, so they show at 9.9 s, the stomp. Its AudioSource `fromTheAbove` (1.79 s) on awake. |
| `bounce1` | life 0.5. A dust burst and the FireRing ring. Its AudioSource `bounce1` (0.394 s). |

**Voices** (BB rip): bounce1 0.536 s, bounce2 1.176 s, bounce0 0.987 s.

**Step lengths:**
- bounce1 is a 0.9 s once clip, held on its last frame (the Cat's decision 9: a once step clamps) under the hide, to 9.5 s.
- bounce2 (1.1 s) is held to 1.4 s, so the ring's life (8.9 + 2 = 10.9 = 9.5 + 1.4) and its sound (to 10.69) are not
  cut by the restart. This is the Chameleon's Torment Rain (decision 9).
- The 8.6 s hide is under the 10 s rule.

### Knee Shot (#402, passive in Maim Shot)

RPC_maimShot (`$RPC_maimShot$26971`, :22949-23660; `clean.py` 23083-23630):
- **0:** `PlayAnimation("maim", 0.2)` (:23486), the voice maimShot1 / maimShot2 (:23527-23625), `Yield(2, 0.5)`
  (:23610).
- **0.5:** `maimShot_fire` from hero + 1 up (:23111-23156), then Block_88 → `Yield(3, 0.1)` (:23608).
- **0.6:** for the owner, the raycast (:23216). Then:
  - `RPC_nAttack_hit` at the hit, on every hit (:23224);
  - with #402, `Random.Range(0, 100) < lckAdjust(20)` (:23262; strict `<`, so 20 % at LCK 1) sets KO 40 and isKneeShot
    (:23268-23273);
  - after `hit() != 0` (:23280, a real foe), **either** `RPC_kneeShot_hit` (:23294) **or** `RPC_maimShot_hit` (:23314).
- RPC_kneeShot_hit (:9669-9708) loads `Effects/kneeShot_hit` (:9682) and Instantiates it at the hit with
  `LookRotation(forward)` (:9692; :9690 / :9693 T).
- **The prefab is missing** in BB's container and TTO's catalog, so the game draws nothing on a Knee Shot.

**Effect on the page:** Maim Shot's `maimShot_hit` cue rolls `p 0.8`, and nothing is drawn in its place.
- The 20 % are drawn as BB's own `<` (lckAdjust(20) = floor(100 × 20.2 / 100.2) = 20, CharacterControl.cs:20658, as the
  Chameleon's crit).
- `nAttack_hit` stays on every play.

### Snipe Mastery (#431, passive in the Normal Attack)

- RPC_nAttack's plain path: on a hit, `hasSkill(431)` (:17594) → `RPC_snipeShot_hit` (:17600), **else**
  `RPC_nAttack_hit` (:17620).
- The ricochet path with Bouncing Bullet: the same split for every listed hit (:18265-18302).
- The shotgun: :36313.
- RPC_snipeShot_hit (:11435-11475) loads `Effects/snipeShot_hit` (:11448) and Instantiates it at the hit with the hero's
  rotation (:11458).
- **The prefab is missing in both games.** With passives on, the Normal Attack's own hits draw no hit effect.
  `bouncingBullet_hit` at the ricochet points (:18135-18147) is a separate load and still draws.
- This is the attacks owner's entry (Open question 1).

### Herb Finder (1-2; #321 / #323)

**Trigger** (Herb.cs OnGUI :94-280): a field herb, kept on a 50 % roll at Start (:27-31), shows a button while the
player stands within `(int)sqrMagnitude <= 3` (:140-146, about 1.7 m). A Rabbit with `getHerbFinderLv() > 0` (:184)
clicking it gets:
- the herb marked taken and destroyed 1 s later (:188-191, Update :76-82);
- the success roll `getHerbFinder()` (Rabbit.cs:10617-10682): Big Bag #423 always succeeds (:10624), else the roll fails
  on `Random.Range(0, 100) > lckAdjust(20 × lv)` (:10666), so ≤ passes, 41 % at rank 2;
- then `RPC_herbFinder(herb position, forward, 0, 1 green / 2 blue)` (:213) and the ActionEvent (:222).

**RPC_herbFinder** (:10532-10570) loads `Effects/herbFinder` (:10545) and Instantiates it at the herb, identity
(:10555). The rank is not used.

**The prefab is missing in both games.** There is no Rabbit clip (Herb.cs plays none) and no look. The herb item that
enters her bag is inventory, not a look.

## Choices made here (rule by rule)

**Max rank.**
- Bounce 2: 8 s in the air.
- From the Above is one rank.
- Combo 4: range 36. It does not matter here: the 15.62 m ray reaches at any Combo.

**Passives on.** From the Above's air shots and ring, and Knee Shot's roll, are on. Snipe Mastery's missing hit is the
attacks owner's (Open question 1).

**The 10 m target point.** The air shot aims at the ground point 10 m ahead from 12 m up, `nAttack_hit` at d 10. Its spawn
is the raycast hit, so there is no 0.6 m homing offset: the rule's homing case is a projectile that seeks.

**Rotations.**
- The air shot's `rot [50.19, 0, 0]`: LookRotation of (0, -12, 10), the pitch after the hero's facing.
- `nAttack_hit`, `bounce1` and `fromTheAbove_ring` take the hero's rotation, so no `rot`.

**Random picks.**
- Bounce's voice is `bounce1|bounce2` (Random.Range(0, 2), :21279).
- Knee Shot is `p 0.8` on `maimShot_hit`. It is one roll, and its only other outcome draws nothing, so no `roll` name is
  needed.

**The hero hidden** from 0.9 to 9.5 s: `[0.9, "hideProp", "hero", {"kill": 8.6}]`. This hides the whole hero, her props
and their weapon_fx, the Chameleon / Mole shape (Chameleon decision 49, Mole decision 5). The game turns off every
Renderer under her (CharacterControl.cs:32834-32848).

**Fades.** bounce1 keeps the page's first-step 0.2 s fade, though the game cuts (Chameleon decision 2). bounce2 is a cut,
as the game's `PlayAnimation("bounce2", 0)`.

**One tile, its Bible icon.** `rabbit_fromTheAbove5` (assets.js; `wardrobe/data/icons/skills/rabbit/fromtheabove5.webp`)
through `OWN_TILE`, as the Chameleon's Critical Plus. Knee Shot, Snipe Mastery and Herb Finder get no tile: they have no
look in the game (Open questions 1, 3, 4).

## Parts needed

**None.** Every cue uses kinds and options the page has:
- `fx` with d / y / rot;
- `voice`;
- `hideProp` "hero" with kill.

Every prefab is built from parts the page already builds (EffectControl, LineEmitter, RingEmitter, ImageEmitter, the
Ellipsoid emitter with ParticleAnimator and ParticleRenderer, AudioSource; fx_inventory "ready").

## PASTE-READY

### 1. `wardrobe/index.html` SEQ: the rabbit line (index.html:1329-1330 at this reading; anchor on the text)

```js
  rabbit: ["Charge Attack: cAttack1 cAttack2* cAttack3", "Mix: mix1 mix2*@0 mix3~", "Sticky Gum: mix1 mix2*@0 mix4~", "Bounce: bounce1 bounce2",
    "Mall: mall1* mall2*",
    // From the Above (#421, passive) plays no clip: the Normal Attack key while Bounce is airborne starts RPC_fromTheAbove
    // (Rabbit.cs:8944-8997), the shot from 12 m above the hidden hero; its tile is Bounce's clips with the shots, bounce1
    // held under the hide to the landing's bounce2 at 9.5 s (Bounce 2: hide at 0.9 :21068, landing at 0.9 + 8 :21073,
    // bounce2 0.6 s later :21566-21571), bounce2 held to 1.4 s for the landing ring's life (2026-11-13,
    // plans/fx_rabbit/effect_only.md)
    "From the Above: bounce1@9.5 bounce2@1.4"],
```
If another researcher has changed the first lines, keep theirs and append the comment and the tile.

### 2. `wardrobe/index.html` SEQ_SKILL: add a rabbit entry (merge with any other rabbit ids)

```js
  // the Rabbit (2026-11-13, plans/fx_rabbit/effect_only.md): From the Above on Bounce's clips (a skill with a tile of its
  // own shows on that tile only: the Bounce tile keeps its own icon, moveSkillIcons)
  rabbit: { "@FromtheAbove": "fromTheAbove" },
```

### 3. `wardrobe/fx_cues/rabbit.json`: two entries

The file is `{}` today. The same cues are in `checks/fx_rabbit_research/effect_only/cues.json`, checked with
`json.load`.

```json
  "@FromtheAbove:bounce1": {
    "why": "Rabbit.cs From the Above (#421, passive), on Bounce at max rank (Bounce 2) with its air shots; no clip of its own. Bounce (RPC_bounce :9591 -> $RPC_bounce$26916 :20867-21400): at 0 PlayAnimation(bounce1, 0) (:21238), actionTime = now (:21223), voice bounce1 / bounce2 (Random.Range(0, 2) :21279; :21289 -> PlayOneShot :21383, :21320 -> :21363); Yield 0.5 (:21357): Effects/bounce1 at the hero, its rotation (:21019-21031; life 0.5, its AudioSource bounce1); Yield 0.4 (:21375): at 0.9 addStatus(hide, 1, 4 x 2 + 1) (:21068: layer 2 and every Renderer under the hero off, CharacterControl.cs:32818-32848) and the landing timer 0.9 + 8 (:21073); the FixedUpdate loop (:21379) starts RPC_bounce0 at 8.9 (:21108-21114). The air shot: doNormalAttack (:8876-9101) with hasSkill(421), actionState attack, myCommand bounce, Time > actionTime + 1 and the nAttack timeout clear (:8944-8976, the junk predicates between them false) starts RPC_fromTheAbove(position, target - position) (:8984; $RPC_fromTheAbove$26940 :21964-22275): at the press addTimeOut(nAttack, 1.5) (:22247), firePos = hero + 12 up, fireDir = tDir - 12 up, fireRot = LookRotation(fireDir) (:22253-22259), Yield 0.1 (:22272); then Effects/nAttack_fire at firePos, fireRot (:22087-22099; life 1, its AudioSource nAttack) and the owner's raycast (range 16 + 5 x Combo, :22129-22134) -> RPC_nAttack_hit at the hit (:22140; nAttack_hit with the hero's rotation, :9135; Snipe Mastery is not read here). Held attack: presses at 1.0, 2.5, 4.0, 5.5, 7.0, 8.5 (1.5 s apart), shots 0.1 s later; to the 10 m ground point from 12 m up: pitch atan2(12, 10) = 50.19 deg, the hit at d 10. The landing (RPC_bounce0 :9598 -> $RPC_bounce0$26929 :21430-21925) at 8.9: voice bounce0 (:21796, PlayOneShot :21808) and, with #421, Effects/fromTheAbove_ring at the hero, its rotation (:21820-21840; in place of the bounce2 effect, the else :21857-21875; life 2, its dust bursts delayed 1 s to the stomp, its AudioSource fromTheAbove); Yield 0.6 (:21908): the hide removed and bounce2 at 9.5 (:21566-21571, the next step)",
    "cues": [
    [0, "voice", "bounce1|bounce2"],
    [0.5, "fx", "bounce1"],
    [0.9, "hideProp", "hero", {"kill": 8.6}],
    [1.1, "fx", "nAttack_fire", {"y": 12, "rot": [50.19, 0, 0]}],
    [1.1, "fx", "nAttack_hit", {"d": 10}],
    [2.6, "fx", "nAttack_fire", {"y": 12, "rot": [50.19, 0, 0]}],
    [2.6, "fx", "nAttack_hit", {"d": 10}],
    [4.1, "fx", "nAttack_fire", {"y": 12, "rot": [50.19, 0, 0]}],
    [4.1, "fx", "nAttack_hit", {"d": 10}],
    [5.6, "fx", "nAttack_fire", {"y": 12, "rot": [50.19, 0, 0]}],
    [5.6, "fx", "nAttack_hit", {"d": 10}],
    [7.1, "fx", "nAttack_fire", {"y": 12, "rot": [50.19, 0, 0]}],
    [7.1, "fx", "nAttack_hit", {"d": 10}],
    [8.6, "fx", "nAttack_fire", {"y": 12, "rot": [50.19, 0, 0]}],
    [8.6, "fx", "nAttack_hit", {"d": 10}],
    [8.9, "voice", "bounce0"],
    [8.9, "fx", "fromTheAbove_ring"]
    ]
  },
  "@FromtheAbove:bounce2": {
    "why": "Rabbit.cs RPC_bounce0 after its 0.6 s wait (:21547-21581): the hide removed (:21566) and PlayAnimation(bounce2, 0) (:21571); 0.4 s later the stomp, FindAreaTarget(3 x rangeMod) and hit(421, ..., ATK, KO 20) (:21608-21652, no effect), 0.4 s later standby (:21688). Nothing is drawn in this step: the voice bounce0 and fromTheAbove_ring came at the landing's start, 0.6 s before it, in the bounce1 step. This entry stays empty on purpose, so that a plain bounce2 entry of the Bounce tile does not play its landing cues a second time.",
    "cues": []
  }
```
(Add the comma after the last `}` only if another entry follows.)

Check: `py -3 -c "import json; json.load(open('wardrobe/fx_cues/rabbit.json', encoding='utf-8'))"`.

If the Bounce owner writes no plain `bounce2` entry, the empty `@FromtheAbove:bounce2` entry is harmless.

### 4. `pipeline/wardrobe_skill_icons.py` OWN_TILE: add the rabbit entry

```python
            # the Rabbit's From the Above on Bounce's clips (2026-11-13, plans/fx_rabbit/effect_only.md)
            "rabbit": {"fromTheAbove": ["bounce1", "bounce2"]},
```
No EFFECT_ONLY entry is needed. The Bible has `rabbit_fromTheAbove5`, so `best` finds it.

Then `py -3 pipeline\wardrobe_skill_icons.py` adds it to `data/icons/hd/index.json` and writes
`icons/hd/rabbit/fromTheAbove.webp`.

### 5. A fragment for the Maim Shot owner (Knee Shot #402, passives on)

In the `maim` entry, the hit puff at the owner's time and spot (0.6 s by the coroutine above; d / y are that owner's):

```json
    [0.6, "fx", "maimShot_hit", {"d": 10, "y": <the owner's>, "p": 0.8}]
```

Add this to that entry's `why`: "Knee Shot #402 (passives on): on a hit on a foe, `Random.Range(0, 100) < lckAdjust(20)` =
20 % (:23256-23273) sends RPC_kneeShot_hit in place of RPC_maimShot_hit (:23288-23325); its prefab kneeShot_hit is in
neither BB's Resources nor TTO's catalog, so the game draws nothing then: maimShot_hit on 80 % of the plays (nAttack_hit,
:23224, on every play)."

### 6. Build and check

```
uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py rabbit --fx nAttack_fire,nAttack_hit,bounce1,fromTheAbove_ring --voices bounce0,bounce1,bounce2
py -3 pipeline\wardrobe_skill_icons.py
uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py <this folder> checks/fx_rabbit dark --cls rabbit
```
A plain `wardrobe_fx.py rabbit` picks them up from the cue file once every Rabbit cue is in.

## Left out (with reasons)

- **Knee Shot's, Snipe Mastery's and Herb Finder's own effects:** the prefabs do not exist in either game, so the game
  draws nothing (Read this first 3). No look is invented. This follows the earlier missing-asset calls: the Chameleon's
  and Mole's missing KO voices stay silent (Chameleon decision 19), and the Mole's missing `Effects/bombardment` is
  harmless.
- **The stomp's damage** at 9.9 s (no effect), and the movement while hidden (the player's keys).
- **Bounce's cooldown re-arm** to agiAdjust(36) (:22250): not a look.
- **The herb object, the Mall and the mercenary:** other owners' or world objects.
- **The supplement skills and `onSupport`:** a cross-class job (the Penguin / Mole precedent).

## Open questions (each with my recommended answer)

1. **Snipe Mastery hides the Normal Attack's hit effect.** With #431 the game sends RPC_snipeShot_hit in place of
   RPC_nAttack_hit, and `snipeShot_hit` exists in neither BB nor TTO. A passives-on Normal Attack therefore shows no hit
   puff on its own hits (the ricochet's `bouncingBullet_hit` still shows).
   - *Recommend following the game:* no `nAttack_hit` cue on the Normal Attack's own hits. Write it down in that entry's
     `why`, and flag it to the user, since it reads as "missing" on the page.
   - Alternative: show `nAttack_hit` as if Snipe Mastery were off (a passive switched off for looks, against the rule).
   - That owner decides. No own tile for Snipe Mastery either way: there is no look to show.
2. **From the Above's shot count.** *Recommend 6 shots* (a held attack at the game's 1.5 s cadence through the 8 s air
   time, from 1.0 s): the skill's whole look, as the Mole's Bombardment kept all its bombs (Mole Q4).
   - Alternative: one shot at 1.0 s, as the Normal Attack tile's one shot (Chameleon decision 3).
   - Either way the tile runs 9.5 + 1.4 s.
3. **Herb Finder: no tile.** Its RPC's prefab is missing, so a tile would play nothing on the idle stance. The Cat's
   Treasure Hunt got a tile because its coin burst exists.
   - *Recommend no tile and no EFFECT_ONLY entry.*
   - If the user wants every card on the page anyway, `"Herb Finder: root*@1"` with no cues and EFFECT_ONLY `"rabbit":
     ["herbFinder"]` is the shape (icon `rabbit_herbFinder2`). It would be an empty tile.
4. **Knee Shot: no own tile.** The proc's only visible change is the missing `maimShot_hit`.
   - *Recommend no tile*, and the `p 0.8` in Maim Shot (block 5).
   - The Chameleon's Critical Plus got an own tile because its crit draws something; Knee Shot's draws nothing.
   - If wanted anyway: `"Knee Shot: maim"`, key `@KneeShot:maim` = Maim Shot's cues without `maimShot_hit`, `OWN_TILE`
     `{"kneeShot": ["maim"]}`, SEQ_SKILL `"@KneeShot": "kneeShot"` (icon `rabbit_kneeShot5`).
5. **Bounce's own tile has no air time** in the page's SEQ today (`"Bounce: bounce1 bounce2"`).
   - *Recommend the Bounce owner use `"Bounce: bounce1@9.5 bounce2@1.4"`* with this tile's cues minus the six shots: the
     hide `[0.9, "hideProp", "hero", {"kill": 8.6}]`, `bounce1` at 0.5, the voices, and `fromTheAbove_ring` (passives
     on) with `bounce0` at 8.9.
   - The two tiles then differ only by the shots.
6. **The air shot's target is the ground point.** The ray from 12 m up meets the ground 10 m ahead. With a real foe at
   10 m it would meet the foe's collider a little before and above that point.
   - *Recommend d 10, ground* (the standing target-point rule, as the Chameleon verification 1 fixed nAttack_hit at d 10).

## Offers for the Bible (not written there)

- **From the Above's air shot timing:**
  - the first press works only after `actionTime + 1` = 1.0 s into Bounce (:8968);
  - one shot per 1.5 s (the `nAttack` timeout, :22247), so at most 6 at Bounce 2;
  - each fires 0.1 s after the press (:22272) from 12 m above the hero, at the target (:22253-22259).
- **With From the Above, the landing draws `fromTheAbove_ring` in place of the `bounce2` effect** (:21820-21875). Its
  dust is delayed 1 s, to the stomp. The hide lasts from 0.9 s to landing + 0.6 s (:21068, :21566); the status's own
  4 × sLv + 1 is never reached.
- **Missing prefabs** (in neither BB's Resources nor TTO's catalog, so the game logs "Cannot find ... Effect" and draws
  nothing): `kneeShot_hit` (Knee Shot), `snipeShot_hit` (Snipe Mastery), `herbFinder` (Herb Finder). For the other
  cards' owners: `circleShot_hit`, `fourShot_hit`, `tenShot_hit`, `contract_ring`, `mall`.
  - Consequence: with Snipe Mastery, a Normal Attack hit has no hit effect.
  - Consequence: a Knee Shot proc has no maim hit puff.
- **Herb Finder's success roll** fails on `> lckAdjust(20 × lv)` (:10666), so it passes on `<=`. The Bible's line 349
  already says so.


---
## Verification (13/11/2026)

Checker, office PC. I re-derived the claims from `C:\Users\Jump\Desktop\12tails\DecompiledSource\Rabbit.cs` and from the
rip. I also ran three probes:
- `wardrobe_fx.py rabbit --probe` on 23 names, which include all of this report's (`checks/fx_rabbit_research/verify/probe.json`);
- `wardrobe_fx_tto.py rabbit --probe snipeShot_hit,kneeShot_hit,herbFinder` (`tto_probe.err`);
- `checks/fx_rabbit_research/verify/verify.py`, output in `verify.txt`.

**This section wins over the report body.**

**Confirmed as written** (no change):
- **The RPCs.** Rabbit.cs has 88 RPC definitions. The four passives' RPCs are at :9605, :9669, :10532 and :11435.
- **Missing prefabs.**
  - kneeShot_hit, snipeShot_hit and herbFinder are KeyErrors in BB and are not in TTO's catalog. catalog.bin holds only
    the icon keys herbfinder0-4, kneeshot5 and snipemastery5.
  - circleShot_hit, fourShot_hit, tenShot_hit, contract_ring and mall are KeyErrors in BB too (probe.json).
- **No Rabbit active is effect-only.** bountyHunt, coinRicochet and medicTurret are clips in data/rabbit/clips.json.
- **Bounce's clock.**
  - bounce1 is cut in at 0 (:21238), with actionTime set at :21223.
  - Then come Yield 0.5 (:21357), Yield 0.4 (:21375), the hide at 0.9 s (:21068) and the timer at 0.9 + 8 (:21073).
  - At the landing: the voice bounce0 (:21796), fromTheAbove_ring (:21830), and bounce2's effect only in the else
    (:21865).
  - Then Yield 0.6 (:21908), removeStatus (:21566) and bounce2 (:21571).
  - The landing's strict `Time.time > mBounceTimer` on the fixed step puts it between 8.9 and 8.92 s. It is kept at 8.9:
    within one fixed step, and Mole decision 45 uses the nominal times.
- **The air shot.**
  - The gate is at :8944-8976.
  - The nAttack timeout of 1.5 s is at :22247, firePos and fireDir at :22253-22259, and the 0.1 s wait at :22272.
  - nAttack_fire spawns at :22087-22099. The ray is at :22119-22140, with no Snipe Mastery branch.
  - No Hyper Shot or voice: the flat distance of about 9.7 m is under 16 (:22168-22214).
  - So 6 shots, at 1.1, 2.6, 4.1, 5.6, 7.1 and 8.6 s.
- **The files.** The voices bounce0, bounce1 and bounce2 are 0.987, 0.536 and 1.176 s long. The sounds bounce1 and
  fromTheAbove are 0.394 and 1.79 s. The lives: bounce1 0.5 s, fromTheAbove_ring 2 s (probe).
- The JSON block parses. Both keys are steps of the proposed tile, and every option is in OPTS.
- Herb Finder's 41 % at rank 2 checks out: lckAdjust(40) = 40, and the roll passes on `<=`, so 41 of 100.

**Findings**

1. **The From the Above entry: the pitch, and the hit goes on the target body.** This is the one entry for both reports
   (attacks_emotes.md's block is dropped, its Verification 4).
   - **rot 50.19 → 50.194.** That is atan2(12, 10) = 50.194°, the value attacks_emotes uses. The class's pitches carry 3
     decimals (5.711).
   - **The hit moves from d 10 on the ground to `{"y": 0.36, "d": 9.7}`.** Open question 6 is reversed.
     - The ray's mask, ~(own + layers 1, 2) (:22119), takes the foe's layer.
     - From (0, 12, 0) toward the 10 m ground point, the ray meets the standard target body's lower cap at
       **(0, 0.356, 9.703)**, 15.16 m out (verify.txt). The body is the CharacterController capsule: centre 0.6 m up,
       height 1, radius 0.3.
     - Every cue in the class uses that one body (Bat decision 4). attacks_emotes' nAttack counts its hit for the voice,
       and skills_a puts every Rabbit ray hit on it (skills_a.md:344, :357, :393).
     - Chameleon decision 22's d 10 was an arrow at its ground arrival time. It is not this class's rule.

   The corrected block is below.
2. **The SEQ block is out of date: merge it with attacks_emotes.md.**
   - The SEQ block still has `"Charge Attack: cAttack1 cAttack2* cAttack3"` and `"Bounce: bounce1 bounce2"`.
   - The rabbit line after both reports (lines 1351-1352 at this reading; anchor on the text):
     - Normal Attack, Customized Shotgun and Charge Attack come from attacks_emotes.
     - From the Above comes from here.
     - Mix, Sticky Gum, Bounce and Mall are as their owners set them. Bounce is skills_a.md:108's.
     - The TTO tiles are tto.md's, and they get added to this line.

   ```js
     // the Rabbit (2026-11-13, plans/fx_rabbit/attacks_emotes.md, effect_only.md and their Verifications): the Normal
     // Attack one shot (Bouncing Bullet's ricochet with the passives on), Customized Shotgun its own tile on the same clip
     // (the shotgun shot); the Charge Attack's scope 1.0 s after the press (Rabbit.cs:19032), held 4 s to Dead Shot's x3
     // (:19486); From the Above (#421, passive, no clip of its own: the Normal Attack key while Bounce is airborne,
     // :8944-8997) on Bounce's clips, bounce1 held under the hide to the landing's bounce2 at 9.5 s (:21068, :21073,
     // :21566-21571), its bounce2 step as the Bounce tile's
     rabbit: ["Normal Attack: nAttack", "Customized Shotgun: nAttack", "Charge Attack: cAttack1@1 cAttack2*@4 cAttack3",
       "Mix: mix1 mix2*@0 mix3~", "Sticky Gum: mix1 mix2*@0 mix4~", "Bounce: bounce1@9.5 bounce2!",
       "Mall: mall1* mall2*", "From the Above: bounce1@9.5 bounce2!"],
   ```

   **`bounce2@1.4` is dropped. Its reason does not hold.**
   - The page never cuts an effect when a round starts again or on the way back to idle. fxClear runs only on a new pick
     (index.html:1543, `if (!tail) fxClear()`), and fxStart's step change only cuts followState effects with a cut
     (:5376-5380).
   - So the landing ring (8.9-10.9 s) and its sound (to 10.69 s) play out in full either way.
   - The hold would only freeze bounce2's last frame for 0.3 s.
   - The From the Above tile takes the Bounce tile's bounce2 step, so the two tiles differ only by the shots (this
     report's own aim, Q5). If skills_a's verification changes the Bounce line, change this one to match.
3. **SEQ_SKILL: one rabbit entry for both reports.**

   ```js
     // the Rabbit (2026-11-13, plans/fx_rabbit/attacks_emotes.md, effect_only.md): Customized Shotgun on the Normal
     // Attack's clip, From the Above on Bounce's clips (a skill with a tile of its own shows on that tile only)
     rabbit: { "@CustomizedShotgun": "customizedShotgun", "@FromtheAbove": "fromTheAbove" },
   ```
4. **OWN_TILE (block 4): merge it with Customized Shotgun.** attacks_emotes left that one out (its Verification 3).

   ```python
               # the Rabbit's Customized Shotgun on the Normal Attack's clip, From the Above on Bounce's clips (2026-11-13,
               # plans/fx_rabbit/attacks_emotes.md, effect_only.md)
               "rabbit": {"customizedShotgun": ["nAttack"], "fromTheAbove": ["bounce1", "bounce2"]},
   ```
5. **Block 5 (the Knee Shot fragment) is dropped.**
   - It is not valid JSON as written: `"y": <the owner's>`.
   - Its d 10 is the ground.
   - skills_a's maim entry already carries the roll on the body: `[0.6, "fx", "maimShot_hit", {"d": 9.7, "y": 0.61,
     "p": 0.8, "kill": 1}]` (skills_a.md:345), with nAttack_hit on every play (:344).
6. **Snipe Mastery's "the shotgun: :36313" is wrong** (the table rows and the Snipe Mastery section).
   - :36313-36325 is Snipe Mastery's x1.5 on the shotgun's Hyper Shot term.
   - RPC_shotgun always draws shotgun_hit (:36354) and never calls RPC_snipeShot_hit.
   - This changes the text only.
7. **Bouncing Bullet's row says "voice `bouncingBullet` ... on every Normal Attack". That is wrong.**
   - The voice needs a hit with bounceCount > 1 (:18331, :17937).
   - In the tile's geometry the hit is in segment 1 (bounceCount 1), so the voice is nAttack2 (attacks_emotes item 2).
   - This changes the text only.
8. **Open question 5 is settled already.** skills_a gives Bounce the same 9.5 s tile and cues (skills_a.md:108,
   :329-335).
   - Its key is the plain `bounce1`, so `@FromtheAbove:bounce1` is tried first on this tile and nothing plays twice.
   - skills_a writes no bounce2 entry (skills_a.md:222). So the empty `@FromtheAbove:bounce2` does nothing, and it can
     stay as a guard.

**Calls made (the user was not available):**
- The hit goes on the body (Bat decision 4: one body for every cue in the class).
- 6 shots (Mole Q4: the whole look, every press at the earliest moment).
- No tile for Knee Shot, Snipe Mastery or Herb Finder. Their prefabs exist in neither game, and a passive with no look
  gets no tile, as Stat Plus gets none.
- From the Above's bounce2 step follows the Bounce tile's.

**Corrected block 3** (`wardrobe/fx_cues/rabbit.json`, both entries). verify.py checked it: 2 entries, 17 cues, ok.

```json
  "@FromtheAbove:bounce1": {
    "why": "Rabbit.cs From the Above (#421, passive), on Bounce at max rank (Bounce 2) with its air shots; no clip of its own. Bounce (RPC_bounce :9591 -> $RPC_bounce$26916 :20867-21400): at 0 PlayAnimation(bounce1, 0) (:21238), actionTime = now (:21223), voice bounce1 / bounce2 (Random.Range(0, 2) :21279; :21289 -> PlayOneShot :21383, :21320 -> :21363); Yield 0.5 (:21357): Effects/bounce1 at the hero, its rotation (:21019-21031; life 0.5, its AudioSource bounce1); Yield 0.4 (:21375): at 0.9 addStatus(hide, 1, 4 x 2 + 1) (:21068: layer 2 and every Renderer under the hero off, CharacterControl.cs:32818-32848) and the landing timer 0.9 + 8 (:21073); the FixedUpdate loop (:21379) starts RPC_bounce0 at 8.9 (:21108-21114). The air shot: doNormalAttack (:8876-9101) with hasSkill(421), actionState attack, myCommand bounce, Time > actionTime + 1 and the nAttack timeout clear (:8944-8976, the junk predicates between them false) starts RPC_fromTheAbove(position, target - position) (:8984; $RPC_fromTheAbove$26940 :21964-22275): at the press addTimeOut(nAttack, 1.5) (:22247), firePos = hero + 12 up, fireDir = tDir - 12 up, fireRot = LookRotation(fireDir) (:22253-22259), Yield 0.1 (:22272); then Effects/nAttack_fire at firePos, fireRot (:22087-22099; life 1, its AudioSource nAttack) and the owner's raycast (range 16 + 5 x Combo, :22129-22134) -> RPC_nAttack_hit at the hit (:22140; nAttack_hit with the hero's rotation, :9135; Snipe Mastery is not read here). Held attack: presses at 1.0, 2.5, 4.0, 5.5, 7.0, 8.5 (1.5 s apart), shots 0.1 s later; to the 10 m ground point from 12 m up: pitch atan2(12, 10) = 50.194 deg; the ray (mask ~(own + layers 1, 2) :22119, so the foe's layer counts) meets the standard target body (Bat decision 4, the CharacterController capsule centred 0.6 m up, height 1, radius 0.3; the class's other ray hits, skills_a.md) on its lower cap at (0, 0.356, 9.703), 15.16 m out (checks/fx_rabbit_research/verify/verify.txt), within the 36 m range; flat distance 9.7 < 16: no Hyper Shot, no voice (:22168-22214). The landing (RPC_bounce0 :9598 -> $RPC_bounce0$26929 :21430-21925) at 8.9: voice bounce0 (:21796, PlayOneShot :21808) and, with #421, Effects/fromTheAbove_ring at the hero, its rotation (:21820-21840; in place of the bounce2 effect, the else :21857-21875; life 2, its dust bursts delayed 1 s to the stomp, its AudioSource fromTheAbove); Yield 0.6 (:21908): the hide removed and bounce2 at 9.5 (:21566-21571, the next step)",
    "cues": [
      [0, "voice", "bounce1|bounce2"],
      [0.5, "fx", "bounce1"],
      [0.9, "hideProp", "hero", {"kill": 8.6}],
      [1.1, "fx", "nAttack_fire", {"y": 12, "rot": [50.194, 0, 0]}],
      [1.1, "fx", "nAttack_hit", {"y": 0.36, "d": 9.7}],
      [2.6, "fx", "nAttack_fire", {"y": 12, "rot": [50.194, 0, 0]}],
      [2.6, "fx", "nAttack_hit", {"y": 0.36, "d": 9.7}],
      [4.1, "fx", "nAttack_fire", {"y": 12, "rot": [50.194, 0, 0]}],
      [4.1, "fx", "nAttack_hit", {"y": 0.36, "d": 9.7}],
      [5.6, "fx", "nAttack_fire", {"y": 12, "rot": [50.194, 0, 0]}],
      [5.6, "fx", "nAttack_hit", {"y": 0.36, "d": 9.7}],
      [7.1, "fx", "nAttack_fire", {"y": 12, "rot": [50.194, 0, 0]}],
      [7.1, "fx", "nAttack_hit", {"y": 0.36, "d": 9.7}],
      [8.6, "fx", "nAttack_fire", {"y": 12, "rot": [50.194, 0, 0]}],
      [8.6, "fx", "nAttack_hit", {"y": 0.36, "d": 9.7}],
      [8.9, "voice", "bounce0"],
      [8.9, "fx", "fromTheAbove_ring"]
    ]
  },
  "@FromtheAbove:bounce2": {
    "why": "Rabbit.cs RPC_bounce0 after its 0.6 s wait (:21547-21581): the hide removed (:21566) and PlayAnimation(bounce2, 0) (:21571); 0.4 s later the stomp, FindAreaTarget(3 x rangeMod) and hit(421, ..., ATK, KO 20) (:21608-21652, no effect), 0.4 s later standby (:21688). Nothing is drawn in this step: the voice bounce0 and fromTheAbove_ring came at the landing's start, 0.6 s before it, in the bounce1 step. This entry stays empty on purpose, so that a plain bounce2 entry of the Bounce tile does not play its landing cues a second time.",
    "cues": []
  }
```
