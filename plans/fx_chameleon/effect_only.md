# Chameleon: the skills with no body animation (effect-only tiles)

Research only (2026-11-13, home PC). I worked read-only: I wrote this report and files under
`checks/fx_chameleon_research/effect_only/` (git-ignored) and nothing else.

**What was run:**
- The probe, with `--probe` only: `uv run --no-project --with UnityPy python -I pipeline/wardrobe_fx.py chameleon --probe
  criticalPlus_hit,clearArrow,nAttack_hit,zephyrLore_ring` (exit 0). Its output is `probe1.json`: four JSON objects, one
  after another.
- A list of every `Resources.Load(".../Chameleon/Effects|Voices|Sounds/...")` in Chameleon.cs, with the method that
  holds it: `loads.txt`.
- A JSON parse check of the fragments below: `fragments.json`.

**Sources:**
- `D:\12tails\DecompiledSource\Chameleon.cs` (cited as `:line`), `Chameleon_nAttack.cs` and `CharacterControl.cs`.
- The TTO pseudo-C `DecompiledSource_TTO_2026-11-02\pseudo\Chameleon.c`.
- The Bible's `12t_reference/chameleon-skill-reference.md`, and the skill cards and `assets.js` in `12t_projects/bible/`.
- `node pipeline/clip_calls.js D:/12tails/DecompiledSource wardrobe/data chameleon`.
- `plans/fx_inventory.md` ("### chameleon").

The templates were the Sheep's Quick Heal and the Penguin's and Bat's effect_only.md.

## Read this first

1. **The Chameleon has no effect-only skill.** Every active the key dispatcher can start reaches a coroutine that plays
   a body clip:
   - Skin Shift → `skinShift`; Perfect Blend → `backStep`; Fatal Strike → `cast4`; Torment Rain → `rainOfArrow`.
   - Immunity, Venom Shock, Blood Burn and Rusty Decay → `cast3`.
   - The cast-bar skills (True / Mass Invisibility, Final Entrapment, Camp Fire, Tent, Mark of Slayer) → `cast1` /
     `cast2`, then `cast3`.
   - The rest have their own clips.

   The dispatcher's 51 `chm_*` cTypes (`:6387-7148`) all reach one of these. `clip_calls.js` finds a skill clip for
   every one of those RPCs. So no `"<Name>: root@t"` SEQ line, no SEQ_SKILL entry, no `"@<Name>:root"` cue and no
   EFFECT_ONLY entry is needed.
2. **The TTO Lv 100 skills all have bodies too.** Venom Phantom, Apex Hunt and Chain Lightning play their clips through
   `Row6Clip` / `Row6Begin`. TTO's extra `RPC_phantomRequiem` is Venom Phantom's finale (Bible,
   `TTO1102:Chameleon.<RPC_phantomRequiem>d__301`), a phase. Those researchers cover them.
3. **One passive draws an effect from its own RPC with no clip: Critical Plus (#311-314, the Bible card "Critical Plus",
   icon `chameleon_criticalPlus4`).** It is a roll on the hits of the `Chameleon_nAttack` arrows (Normal Attack, Clear
   Arrow, Left Stride and the Double Strider clone's arrows). It is not a key press. By the Penguin's Spread Shot
   precedent (a passive on the attack's own arrows, cued as a `p` roll inside `nAttack1-3`, no tile of its own), it
   belongs **inside the `nAttack1` entry (and `leftStride`)** as a `p 0.2` roll. That owner gets the fragment below.
   Open question 1 gives the own-tile option.
4. **Clear Arrow (#263)** is the Normal Attack arrow swapped for `clearArrow` while the Chameleon is `invisible`. It is a
   phase of `nAttack1`, not effect-only (open question 2).
5. `wardrobe/fx_cues/chameleon.json` is still `{}`, so nothing here collides with an existing key.

## Accounting: every RPC_* in Chameleon.cs (67 definitions)

I listed them with `grep -oE '(void|IEnumerator) RPC_\w+' Chameleon.cs`, which gives 67. The groups below add up to
43 + 13 + 7 + 4 = 67.

**Their clip is in the excluded list (other researchers), with their phases: 43**
- `nAttack1` (`RPC_nAttack1` :8440, clip :16009 `animation.Play("nAttack1")`, a hard cut). Its phases:
  - `RPC_nAttack_fire` :8447: the `nAttack` arrow (:8460).
  - `RPC_nAttack_hit` :8565: `nAttack_hit` at hitPos with the hero's rotation.
  - `RPC_clearArrow_fire` :8983: Clear Arrow's arrow, chosen at :15586-15643 when `getClearArrow()`.
  - `RPC_criticalPlus_hit` :9325: Critical Plus' crit flash. It is called only from `Chameleon_nAttack.cs:669` / :680,
    so it also rides on Left Stride's arrows.
- Charge Attack:
  - `RPC_cAttack1` :8652 plays cAttack1, cAttack2 and silentWalk.
  - `RPC_cAttack2` :8659 is the release (cAttack3 / cAttack4, :17218, :17376). It is started from the dispatcher's
    receive switch (:3649-3793) and the charge release.
  - `RPC_cAttack0` :8666 is the cancel.
- The cast channel: `RPC_cast1` :8673 (cast1 / cast2, `castRing` :18534) and `RPC_cast0` :8680 (the cancel: standby,
  no effect).
- cast3: `RPC_immunity` :8709, `RPC_trueInvisibility_cast` :8783, `RPC_venomShock` :8924, `RPC_massInvisibility_cast`
  :8931, `RPC_bloodBurn` :9480, `RPC_rustyDecay` :10080, `RPC_tent_cast` :10087 and `RPC_markOfSlayer_cast` :10094.
  Two more come with phases:
  - `RPC_finalEntrapment_cast` :9109, with `RPC_finalEntrapment_hit` :9116 (the cage at the target, `finalEntrapment`
    :9142).
  - `RPC_campFire_cast` :9410, with `RPC_campFire_create` :9417 (the fire).
- Own clips:
  - `RPC_quickFire` :8769, `RPC_perfectBlend` :8776 (backStep), `RPC_needlePrison` :8790, `RPC_massShot` :8797 and
    `RPC_poisonVolley` :8917.
  - `RPC_tormentRain` :9251 (rainOfArrow), with `RPC_tormentRain_fire` :9258 (the rain, 0.8 s later).
  - `RPC_fatalStrike` :9265 (cast4), `RPC_leftStride` :9368 and `RPC_rightStride` :9389.
  - `RPC_slayer` :9487 (slayer1 / slayer2) and `RPC_slayer_fire` :9494 (slayer3).
  - `RPC_allSlayer` :9554 (allSlayer1 / allSlayer2), `RPC_allSlayer_fire` :9561 (allSlayer3), and the target-side
    phases `RPC_allSlayer_mark` :9568 (the `*Slayer_eye` marks :9615-9730, started from the cast at :32645) and
    `RPC_allSlayer_hit` :9766.
  - `RPC_allSlain` :9933 (allSlain), with `RPC_allSlain_hit` :9940 (at each listed target, :34227).
  - `RPC_skinShift` :10073, `RPC_zeroShot` :10101 and `RPC_thunderDragon` :10108 (thunderDragon1 / thunderDragon2).
    Thunder Dragon's reflect (CharacterControl.cs:4603-4627) is damage only, with no effect.

**The supplement skills (`sup_*`), in all 12 hero files: 13**
- `RPC_obsidianFang` :10172 / `_hit` :10179, `RPC_stunningGround` :10222, `RPC_psalmOfEnergy` :10465 and `RPC_seaAegis`
  :10635.
- `RPC_assassinate` :10822 and `RPC_zephyrLore` :10829. `zephyrLore_ring` (:10848) is a Chameleon/Effects prefab, but Bat
  (:15494), Bison (:9984) and Cat (:11599) load the same file. The probe shows life 12, followPosition, and its own
  sounds zephyrLore and zephyrLore_ring.
- `RPC_mineWalker` :10923, `RPC_replenishment` :10930, `RPC_elementalBound` :11059, `RPC_divineChannel` :11202,
  `RPC_astralShift` :11209 and `RPC_bloodCarnage` :11400.
- The voice they share, `onSupport()` (:10115-10170, `Voices/support`), is not in the rip's chameleon/voices folder.

These are not Chameleon skills. As the Penguin's report says, they would be a cross-class job if ever wanted.

**Emotes, KO, mission: 7.** All of these have clips, so none is effect-only. Whoever does the emotes covers them (the
Penguin's attacks_emotes / Sheep decision 11 convention).
- `RPC_emotion` :11747 (the emote clips; voice `Voices/chat`, :40466) and `RPC_emotion0` :11754 (its cancel).
- `RPC_ko` :14637 (ko; ko1 / ko2 :46409-46440), `RPC_dead` :14644 (dead1 / dead2 :46770-46801, `deadEffect` :46832) and
  `RPC_revive` :14651 (getUp; voice revive :47136).
- `RPC_activateIcon1` :14530 (the mission's cast2 loop, voice activate1 :45983). No tile, by the Penguin's decision 19.
- `RPC_activateIcon2` :14537 (its end: standby, the camera's ActivateIcon, voice activate2 :14603; no effect, the
  mission only).

**Items, mount, coin, pet: 4.** `RPC_useItem` :12194, `RPC_useMount` :12251 (voices mount1 / mount2 :44383-44414),
`RPC_useCoin` :12304 and `RPC_petEffect` :14492.

**Effect-only: 0.**

`loads.txt` cross-checks this. Every literal Chameleon Effects / Voices / Sounds load in Chameleon.cs sits inside one
of the RPCs above. The one exception is the shared `onSupport`. No effect is drawn from Update or the dispatcher.

**Outside Chameleon.cs:** CharacterControl.cs loads six Chameleon status effects:
- `Immunity` :36595, `needlePrison` :36629, `invisible` :36949, `venomShock` :36991, `fatalStrike` :37077 and
  `rustyDecay` :37161.
- `Chameleon_nAttack.cs:205` also loads `fatalStrike`.

All of them belong to statuses that clip skills give: Immunity, Needle Prison, True / Mass Invisibility, Venom Shock,
Fatal Strike and Rusty Decay. Those skills' researchers cover them.

**TTO** (`pseudo/Chameleon.c` methods) keeps every BB RPC. It adds `RPC_venomPhantom`, `RPC_phantomRequiem`,
`RPC_apexHunt` and `RPC_chainLightning` (all three skills are in the excluded list), and the weapon hooks
`OnWeaponEffect15` / `OnWeaponEffect39` (weapon_fx's domain). It adds no skill without a body.

## Critical Plus: the one clip-less effect (a roll, not a tile)

### Trigger
`Chameleon_nAttack.OnTriggerEnter` (`Chameleon_nAttack.cs:336`) runs on the owner, on a hit:
- `vector = mCollider.ClosestPointOnBounds(arrow collider centre)` (:406): the point on the target's bounds nearest
  the arrow.
- `RPC_nAttack_hit(vector, ...)` is always called (:436).
- `num2` is the crit chance:
  - It starts at 0, plus the set pieces' bonuses (weapon w_chm43 / 44 / 48, armour a_chm43 / 48, accessory
    c_chm43 / 48: +2 to +5, :517-617, :806-820).
  - Plus `getCriticalPlusLv() * 4 + 4` = **20 at rank 4** (:620-631).
- `Random.Range(0, 100) < lckAdjust(num2)` (:643). lckAdjust(20) = 20 at LCK 1 (CharacterControl.cs:20658: floor(100 ×
  20.2 / 100.2)). So it is **20 %** in plain gear.
- Then the damage × (1.8 + 0.15 × CriticalPlusLv) with Bull's Eye #413 (:649-655, 2.4 at rank 4), or × 1.8 without it.
- Then `chameleon.RPC_criticalPlus_hit(vector, forward, 0)` (:669, ActionEvent :680).

The junk predicates on this path were worked out by hand. :621 `271376 - 435422 = -164046`, so `!=` is false and the
code goes on. :625, :641, :643 and :669 each lead to the next statement.

### Spawn
`RPC_criticalPlus_hit` (:9325-9364) is a plain method with no wait.
- It loads `Effects/criticalPlus_hit` (:9338) and calls `Instantiate(..., hitPos, this.transform.rotation)` (:9348): at
  the hit point, with **the Chameleon's** rotation. That is not the target's, so the `rot [0,180,0]` rule does not apply.
- It is the same spot, frame and rotation as `nAttack_hit` (`RPC_nAttack_hit` :8565, `Instantiate(..., hitPos,
  this.transform.rotation)`, :8578-8588).

### Max rank and timing
Critical Plus 4 (#314, top rank; the Bible card's rank 5 is Bull's Eye #413, which only changes the damage). Both
effects appear on the crit together: nAttack_hit (bow_hit1) and criticalPlus_hit (bow_hit3).

### The effect (probe)
- EffectControl: life 1, afterLife 0, followPosition false, **followState false** (so no cut time).
- One ImageEmitter: 2 images over 0.1 s, life 0.2, 1 → 2 m, rndScale 0.4, rndRotation 3.14, material
  `vitalityStrike_hit`.
- Its own AudioSource `bow_hit3` (playOnAwake). The file is in the rip:
  `RippedAssets/.../heroes/chameleon/sounds/bow_hit3.wav`.
- The inventory says **ready** (fx_inventory.md "criticalPlus_hit (Chameleon.cs:9338): ready"). No voice.

### Paste-ready fragment for the nAttack1 entry (and leftStride's arrows)
This goes in the `nAttack1` cue entry, beside its `nAttack_hit` cue. It uses the **same time, `d` and `y` as that
`nAttack_hit` cue**, and the owner of nAttack1 computes those. My estimate is about 0.43 s / d 9.6 / y 1.2:
- The arrow leaves at 0.2 s from hero + 1.5 m up + 1 m forward (:15586-15592).
- Bow Mastery #401 (passives on) makes it 40 m/s (Chameleon_nAttack.cs:100).
- It meets the front of the 10 m target's bounds.

```json
    [0.43, "fx", "criticalPlus_hit", {"d": 9.6, "y": 1.2, "p": 0.2}]
```

Add this to the entry's `why`: "Critical Plus 4's crit (passives on): `lckAdjust(4 × 4 + 4)` = 20 % per landed arrow
(Chameleon_nAttack.cs:620-643), `RPC_criticalPlus_hit` at the hit point with the hero's rotation, the same spot and
frame as nAttack_hit (:669; Chameleon.cs:9338-9348; EffectControl life 1, its own Sounds/bow_hit3)."

No `roll` name is needed: it is an independent draw per arrow. Left Stride fires `2 × 2 + 1 = 5` arrows plus the Double
Strider clone's 5 (`:27058`, `:26998-27043`), and each one rolls on its own. So the leftStride owner adds the same cue
(`p 0.2`) beside each arrow's `nAttack_hit`.

The build needs `--fx criticalPlus_hit` in that class build line (its texture `vitalityStrike_hit` and the sound
bow_hit3 come with it).

## Paste-ready (effect-only tiles)

None. Each block stays as it is:
- `wardrobe/index.html` SEQ `chameleon:`: no `root@` line.
- SEQ_SKILL: no `chameleon:` entry.
- `wardrobe/fx_cues/chameleon.json`: no `@<Name>:root` key.
- `pipeline/wardrobe_skill_icons.py` EFFECT_ONLY: no `"chameleon"` key.

The only paste-ready item is the Critical Plus fragment above, for the nAttack1 / leftStride owners.

**If the user wants Critical Plus as a tile of its own** (open question 1, not recommended), it is a skill on another
skill's clip, as the Penguin's MP Transfer on nAttack1 is:
- SEQ chameleon gets `"Critical Plus: nAttack1!"` (`!` because the game hard-cuts nAttack1, :16009).
- SEQ_SKILL gets `chameleon: { "@CriticalPlus": "criticalPlus" }`.
- The cue key is `"@CriticalPlus:nAttack1"`: the nAttack1 entry's cues copied, with the crit at every play
  (`[<nAttack_hit t>, "fx", "criticalPlus_hit", {"d": <same>, "y": <same>}]`, no `p`).
- wardrobe_skill_icons.py gets `OWN_TILE["chameleon"] = {"criticalPlus": ["nAttack1"]}`, not EFFECT_ONLY, because it
  has a clip. The Bible has `chameleon_criticalPlus4`, so `best` finds it.

## Open questions (each with my recommendation)

1. **Critical Plus: a roll on the arrows, or a tile of its own?** I recommend the roll (`p 0.2`) inside nAttack1 and
   leftStride, like the Penguin's Spread Shot (#401). Frost Spike got a tile because it is started by being hit, with
   no clip of its own, and Critical Plus is not like that. The own-tile shape is given above if the user wants "every
   passive a tile".
2. **Clear Arrow (#263): the nAttack1 tile's arrow, or a tile of its own?** I recommend the plain `nAttack` arrow on the
   nAttack1 tile: Clear Arrow needs the Chameleon to be `invisible`, and no Normal Attack press gives that. Clear Arrow
   could be offered as `"Clear Arrow: nAttack1!"` (SEQ_SKILL `@ClearArrow` → `clearArrow`, OWN_TILE `{"clearArrow":
   ["nAttack1"]}`, Bible icon `chameleon_clearArrow1`), playing `clearArrow` in place of `nAttack`. Both need the
   `Chameleon_nAttack` part that the inventory lists for `nAttack` / `clearArrow`. That is the nAttack1 owner's call.
3. **The supplement skills (`sup_*`, here with Chameleon's own `zephyrLore_ring`)**: I recommend leaving them out, as
   the Penguin's report did. If they are ever wanted, it is one cross-class job (the same 13 RPCs in all 12 hero files).
4. **The emote, KO, dead and revive RPCs** have clips and are not effect-only. They need whoever covers the Chameleon's
   emotes. If no researcher in this run has them, they should be listed for the attacks / emotes job (the voices and
   `deadEffect` are cited above).

## Verification

Checker, 2026-11-13 (home PC), read-only against `D:\12tails\DecompiledSource` and the TTO pseudo-C. Probe output:
`checks/fx_chameleon_research/verify_b_eo/probe_crit.json` (`wardrobe_fx.py chameleon --probe criticalPlus_hit`, exit 0).

**Redone RPC_* listing.** `grep -nE '(void|IEnumerator) RPC_\w+' Chameleon.cs` gives 67 definitions; every line number in
the accounting matches (8440 ... 14651), and the groups are 43 + 13 + 7 + 4 = 67 as stated. `clip_calls.js` finds a skill
clip for every RPC the report says has one (Chameleon.cs:16009 nAttack1 ... :38240 thunderDragon1, :45928 the mission's
cast2). The dispatcher's `"chm_*"` literals: 51, all in :6387-7148, each one a skill whose RPC plays a clip. Every literal
`Heroes/Chameleon/(Effects|Voices|Sounds)` load in Chameleon.cs sits inside an RPC (or its `$RPC_*$` coroutine class) or
`onSupport` (:10142, `Voices/support`, absent from the rip's `chameleon/voices`). Outside Chameleon.cs only
CharacterControl.cs (the six status loads, :36595-37161) and Chameleon_nAttack.cs:205 (`fatalStrike`) load Chameleon
effects. **Conclusion confirmed: no effect-only tile; the four "none" blocks stand.**

Confirmed as written: RPC_criticalPlus_hit (:9325-9364, junk predicates worked out: it loads at :9338 and Instantiates
at :9348 with `this.transform.rotation`, the Chameleon's); its only callers Chameleon_nAttack.cs:669 / :680 (and the
ActionEvent receiver Chameleon.cs:2714 / :4837); the chance `getCriticalPlusLv() * 4 + 4` (:620-631) with
getCriticalPlusLv = 4 at #314 (Chameleon.cs:9272-9320); `Random.Range(0, 100) < lckAdjust(20)` (:643; strict `<`, so 20 %,
not the Penguin's `<=` 21 %), lckAdjust at CharacterControl.cs:20658 = floor(2020 / 100.2) = 20; the probe (life 1,
afterLife 0, followPosition / followState false, one ImageEmitter 2 images / 0.1 s / life 0.2 / 1 -> 2 m / rndScale 0.4 /
rndRotation 3.14, material vitalityStrike_hit, AudioSource bow_hit3 playOnAwake; `bow_hit3.wav` is in the rip);
fx_inventory.md:288 "ready"; Left Stride's `sLv * 2 + 1` arrows (:27058) plus the clone's (:26998-27043, RPC_nAttack_fire
:26971 / :27032); zephyrLore_ring loads (Bat.cs:15494, Bison.cs:9984, Cat.cs:11599, Chameleon.cs:10848); the emote / KO /
dead / revive / mission / mount voice lines (:14603, :40466, :44383, :44414, :45983, :46409, :46440, :46770, :46801,
:46832, :47136).

**Corrections**

1. **The Critical Plus fragment's place is wrong** (report "Paste-ready fragment", `0.43 / d 9.6 / y 1.2`). The report says
   it must share the nAttack1 owner's `nAttack_hit` time and place; that owner's cue is `[0.4281, "fx", "nAttack_hit",
   {"d": 10}]` (plans/fx_chameleon/attacks_emotes.md:165: the arrow from 1 m ahead / 1.5 m up aimed at the 10 m ground
   point, 0.2 + 9.1241 m / 40 m/s). On that path the arrow is 1.5 x (10 - 9.6) / 9 = 0.07 m up at d 9.6, so `y 1.2` is a
   point the arrow never reaches. The standing rule (effects on an enemy go to the 10 m target point) gives the same spot:
   d 10, ground, t 0.4281.
2. **The crit only rolls on a real enemy hit**, not on the ground landing the nAttack_hit cue shows: after
   RPC_nAttack_hit (:436) the code needs `tag == "Player"` or `"Enemy"`, a CharacterControl with hp > 0 (:451-482), and only
   then reaches the crit sum (:516-643). The report's Trigger section reads as if every landed arrow rolls ("20 % per landed
   arrow" in the `why`). It is 20 % per arrow that hits a foe; in the wardrobe that foe is the 10 m target point, so the
   cue stays a `p 0.2` roll there, but the `why` should say so. Note too that attacks_emotes.md:151-154 left the crit out
   ("every hit-side proc ... no target-point analogue"): the two reports disagree, a decision for the user (the
   precedents: the Penguin's Spread Shot and the Bat's Auto Mass stayed rolls in the owner's entry; the Bison's Berserker
   Rush / Fury Trance and the Penguin's Frost Spike, procs with no clip, got tiles; Critical Plus rides on a clip, so the
   roll or the MP-Transfer-style own tile both fit; the standing rule "every skill gets its own tile" leans to the own tile).
3. **TTO (Read this first 2, and the TTO paragraph)**: besides `RPC_phantomRequiem`, TTO's `Chameleon::Row6ActionCode`
   (pseudo/Chameleon.c:35125-35143) names six more action strings: `RPC_apexLock`, `RPC_apexImpact`, `RPC_apexTrophy`
   (Apex Hunt), `RPC_chainHop` (Chain Lightning), `RPC_phantomShot`, `RPC_phantomEcho` (Venom Phantom). They are phases of
   the three released skills, sent as action codes, not methods of their own (methods.tsv has no `Chameleon RPC_apexImpact`
   etc.), and tto.md covers them (tto.md:60, :131, :210). The conclusion (no TTO skill without a body) stands.
4. Not effect-only but worth a line: the page's SEQ `"Focus Fire: focusFire1 focusFire2"` (wardrobe/index.html:1208) has
   no caller in BB (`clip_calls.js`: "no call found: ... focusFire1 focusFire2") nor TTO (`pseudo_all.raw.c`: 0 hits for
   focusFire), and no Bible card. It is skills_a's clip; it gets no cues and no effect-only tile.

**Corrected paste-ready fragment** (for the nAttack1 entry, beside its nAttack_hit cue; JSON checked):

```json
    [0.4281, "fx", "criticalPlus_hit", {"d": 10, "p": 0.2}]
```

`why` addition: "Critical Plus 4's crit (passives on): on an arrow that hits a foe (tag Player / Enemy, hp > 0,
Chameleon_nAttack.cs:451-482), `Random.Range(0, 100) < lckAdjust(4 x 4 + 4)` = 20 % (:620-643), RPC_criticalPlus_hit at the
hit point with the hero's rotation (:669; Chameleon.cs:9338-9348; EffectControl life 1, its own Sounds/bow_hit3): here at
the 10 m target point, the same spot and time as nAttack_hit."

For leftStride, the same cue (`p 0.2`, no `roll`: each arrow draws on its own) goes beside each of that entry's arrow
hits, with that hit's own time and `d` / `x` / `y` from skills_a's `stride_sim.txt`, not the nAttack1 numbers. The
own-tile option, if chosen: `"@CriticalPlus:nAttack1"` = the nAttack1 cues plus `[0.4281, "fx", "criticalPlus_hit",
{"d": 10}]` (no `p`); SEQ `"Critical Plus: nAttack1!"`; SEQ_SKILL `chameleon: { "@CriticalPlus": "criticalPlus" }`;
`OWN_TILE["chameleon"] = {"criticalPlus": ["nAttack1"]}` (icons criticalplus0-4.webp exist in
wardrobe/data/icons/skills/chameleon/).
