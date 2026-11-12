# Bison: the skills with no body animation (effect-only tiles)

Research only (2026-11-13, home PC). Read-only researcher: nothing else in the repo was changed. One probe ran with
`--probe` only (`uv run --no-project --with UnityPy python -I pipeline/wardrobe_fx.py bison --probe
berserkerRush,berserkerRush_ring,furyTrance1,furyTrance2,furyTrance3,overLord,deadEffect,revert`, exit 0; output in
`checks/fx_bison_research/effect_only/probe.json`; `revert` is the Sheep's prefab, so the Bison folder has no such key).
Sources: `D:\12tails\DecompiledSource\Bison.cs` (cited `:line`), `CharacterControl.cs`, `BisonSkill.cs`, the Bible's
`12t_reference/bison-skill-reference.md` and skill cards (`12t_projects/bible/index.html`, `assets.js`), the TTO method
table and pseudo-C (`DecompiledSource_TTO_2026-11-02/methods.tsv`, `pseudo/Bison.c`), `plans/fx_inventory.md` (bison),
`wardrobe/data/bison/clips.json` / `rig.json`, and the rip's voices (`RippedAssets/.../heroes/bison/voices|sounds|effects`).
I followed the Penguin's report (`plans/fx_penguin/effect_only.md`, Frost Spike: a passive proc with no clip gets its own
idle-stance tile) and the Sheep's Quick Heal. A map of every `Effects/` / `Voices/` / `Sounds/` load to the method that
holds it is in `checks/fx_bison_research/effect_only/loads.txt` (163 loads).

## Result

**Every one of the Bison's 18 actives plays a body clip.** `BisonSkill.cs` gives exactly 18 `cType`s (:431-1968), and
`node pipeline/clip_calls.js` finds a clip in each one's RPC. Iron Shield, Diamond Shield and Onslaught play `warcry`,
and Titan Form plays `overPower`. All of them are in the other researchers' list. The Bison has no clip-less key press
like the Penguin's Mana Arc or the Sheep's Quick Heal.

**Two passives fire on their own, with no clip, and draw something on the Bison.** Both are run every frame from
`Update` (:182, calls :277 and :289, both predicates live) and add a status whose apply hangs effects on the hero's bones
(`CharacterControl.cs`). They are the Bison's Frost Spike: each gets its own idle-stance tile, and the proc plays on
every play.

| Tile (Bible name) | Bible icon | Code | Effects | Voices | Buildable |
|---|---|---|---|---|---|
| **Berserker Rush** | `bison_berserkerRush4` | `getBerserkerRush` :7740-7830 (no RPC) → `berserkerRush` status apply, CharacterControl.cs:34752-34942 | `berserkerRush_ring` at the hero (EffectControl life 1, follows), `berserkerRush` on HandMount_L and HandMount_R (held, 6 s) | none | yes |
| **Fury Trance** | `bison_furyTrance3` | `getFuryTrance` :7920-8124 (no RPC) → `furyTrance` status apply, CharacterControl.cs:34956-34992 | `furyTrance3` on the Neck bone (held, 12 s, cut at 10) | furyTrance1 / furyTrance2 | yes |

These prefabs are **not in `plans/fx_inventory.md`**. The inventory lists only the loads in `Bison.cs`, and these are
loaded from `CharacterControl.cs`. The probe shows that each one is built only from parts the page already has (the
inventory's BUILT list): EffectControl, ImageEmitter, RingEmitter, EllipsoidParticleEmitter + ParticleAnimator +
ParticleRenderer. The materials are `Splash1` and `Blood1`. None has an AudioSource or a followState. The two held
looks (`berserkerRush`, `furyTrance1-3`) have **no EffectControl**: the game destroys them when the status is removed,
so their cues need `kill` and `bone`, as the Sheep's Soul of Arms trail and the Penguin's Ice Shield / Focus Intellect
do. Every bone is in `data/bison/rig.json`: HandMount_L, HandMount_R and Neck, each with scale 1. Both voices are in the
rip: furyTrance1 is 0.82 s and furyTrance2 is 0.94 s.

TTO's client has the same `getBerserkerRush` / `getFuryTrance` and no clip-less Bison skill of its own. Its methods
are listed in `methods.tsv`. Its Lv 100 skills `magmaQuake` / `titanDrop` / `unchainedFury` all have clips. The other
researchers cover them.

## Accounting: every RPC_* in Bison.cs (63 definitions)

`grep -nE "^\s*(public|private|protected)[^(]*\bRPC_\w+\(" Bison.cs` gives 63 definitions. They are all `public
virtual`.

**Skills whose clip is in the other researchers' list (26 RPCs; they play 31 clips between them):**
- RPC_nAttack1-5 :7049-7077 (`nAttack1-5`)
- RPC_cAttack1 :7152 (`cAttack1`, `cAttack2`), RPC_cAttack2 :7159 (`cAttack3-6`)
- RPC_enrage :7470, RPC_slam :7477, RPC_trample :7484 (`trample1/2`), RPC_knockDown :7491, RPC_farStun :7625,
  RPC_instantRush :7733
- RPC_overPower :8128, RPC_overSwing :8135, RPC_powerCleave :8142 (`cleave`), RPC_warcry :8473
- RPC_ironShield :8741, RPC_diamondShield :8748, RPC_onslaught :9068 (all three play `warcry`, :27799 / :28389 /
  :30615)
- RPC_earthRupture :8755, RPC_earthSmasher :8940, RPC_titanForm :9033 (`overPower`, :29891), RPC_prideCrusher :9075,
  RPC_magmaClutter :9183, RPC_calamityHammer :9233

**Phases of those skills (12):** RPC_nAttack_hit :7084, RPC_cAttack0 :7166 (Charge Attack's short release / Hold
Charge store), RPC_cAttack_hit :7173, RPC_knockDown_hit :7498, RPC_farStun_fire :7632, RPC_powerCleave_hit :8149,
RPC_powerHammer_hit :8241 (Power Hammer's hit, in Power Cleave), RPC_earthRupture_fire1 :8762, RPC_earthRupture_fire2
:8829, RPC_massStun_fire :9082 (Mass Stun #442's replacement fire, :23797), RPC_magmaClutter_hit :9190,
RPC_calamityHammer_fire :9247.

**Shared by every class (17):**
- The supplement skills: RPC_obsidianFang :9311 / _hit :9318, RPC_stunningGround :9361, RPC_psalmOfEnergy :9601,
  RPC_seaAegis :9771, RPC_assassinate :9958, RPC_zephyrLore :9965, RPC_mineWalker :10059, RPC_replenishment :10066,
  RPC_elementalBound :10195, RPC_divineChannel :10338, RPC_astralShift :10345, RPC_bloodCarnage :10536. Their voice
  `support` is `onSupport` :9254. The Bible excludes them from the Bison's roster (bison-skill-reference.md "Notes on
  judgment calls"), and the Penguin's report left them out as a cross-class job.
- Items / mount / coin / pet: RPC_useItem :11330, RPC_useMount :11387, RPC_useCoin :11440, RPC_petEffect :13637.

**Basic moves, emotes and the mission (7; the ones with clips are not effect-only, the cancels draw nothing):**
- RPC_emotion :10883 plays the emote clips with the chat voice (:34797). RPC_emotion0 :10890 is the cancel.
- RPC_activateIcon1 :13675 plays `battle` (:40354) with voice activate1 (:40401); it gets no tile (Penguin decision 19).
- RPC_activateIcon2 :13682 is a cancel: standby (:13689) and voice activate2 (:13748), no clip, no effect. It is not a
  skill, so it gets no tile.
- RPC_ko :13780 plays `ko` (:40733) with ko1 / ko2 (:40778, :40809).
- RPC_dead :13787 plays `ko` (:41092) with dead1 / dead2 (:41127-41182). `deadEffect` is Instantiated at
  **position − forward, the hero's rotation** (:41201-41213), i.e. 1 m behind. Resting Glory runs here (below). The
  Sheep's decision 11 (the KO tile) covers both.
- RPC_revive :13794 plays `getUp` (`animation.Play` :41507) with voice revive (:41548).

**Left over, and not a tile: RPC_restingGlory :7841** (Resting Glory #261, passive). It runs only from the death
coroutine: `RPC_dead`, owner only, `hasSkill(261)` :41233, calls :41239 / :41248 (the remote copy is :2477 / :4035). It
heals every other `Player` under the team's parent by 35 % of the Bison's max HP (:7841-7900). It loads no effect and
no voice, and `RPC_AddHeal` draws nothing either (CharacterControl.cs:7130-7393 has no load or Instantiate). It has no
teammate to show on, and it already sits inside the KO tile's `ko` clip, so it adds nothing to that tile's cues.

The full list in file order, every one of the 63 with its group:

| # | RPC (Bison.cs line) | Group |
|---|---|---|
| 1-5 | nAttack1 7049, nAttack2 7056, nAttack3 7063, nAttack4 7070, nAttack5 7077 | clip (others) |
| 6 | nAttack_hit 7084 | phase |
| 7-8 | cAttack1 7152, cAttack2 7159 | clip (others) |
| 9-10 | cAttack0 7166, cAttack_hit 7173 | phase |
| 11-14 | enrage 7470, slam 7477, trample 7484, knockDown 7491 | clip (others) |
| 15 | knockDown_hit 7498 | phase |
| 16 | farStun 7625 | clip (others) |
| 17 | farStun_fire 7632 | phase |
| 18 | instantRush 7733 | clip (others) |
| 19 | restingGlory 7841 | passive in RPC_dead, draws nothing: no tile |
| 20-22 | overPower 8128, overSwing 8135, powerCleave 8142 | clip (others) |
| 23-24 | powerCleave_hit 8149, powerHammer_hit 8241 | phase |
| 25-28 | warcry 8473, ironShield 8741, diamondShield 8748, earthRupture 8755 | clip (others) |
| 29-30 | earthRupture_fire1 8762, earthRupture_fire2 8829 | phase |
| 31-34 | earthSmasher 8940, titanForm 9033, onslaught 9068, prideCrusher 9075 | clip (others) |
| 35 | massStun_fire 9082 | phase |
| 36 | magmaClutter 9183 | clip (others) |
| 37 | magmaClutter_hit 9190 | phase |
| 38 | calamityHammer 9233 | clip (others) |
| 39 | calamityHammer_fire 9247 | phase |
| 40-52 | obsidianFang 9311, obsidianFang_hit 9318, stunningGround 9361, psalmOfEnergy 9601, seaAegis 9771, assassinate 9958, zephyrLore 9965, mineWalker 10059, replenishment 10066, elementalBound 10195, divineChannel 10338, astralShift 10345, bloodCarnage 10536 | shared supplement |
| 53-54 | emotion 10883, emotion0 10890 | emote / cancel |
| 55-57 | useItem 11330, useMount 11387, useCoin 11440 | shared item / mount / coin |
| 58 | petEffect 13637 | shared pet |
| 59-60 | activateIcon1 13675, activateIcon2 13682 | mission (no tile) |
| 61-63 | ko 13780, dead 13787, revive 13794 | basic moves (KO tile) |

Totals: 26 skill RPCs with a listed clip + 12 phases + 17 shared (13 supplement + 3 item + pet) + 2 emote + 2 mission +
3 basic + 1 restingGlory = **63**. Not one is a clip-less skill press. The two effect-only tiles come from the passives
below, which have no RPC.

## The passives and procs with no clip, each one checked

I listed every passive in `bison-skill-reference.md` and the skill cards, then looked at what each one draws:

| Passive | Where it runs | Draws / voices | Tile? |
|---|---|---|---|
| **Berserker Rush** #251-254 | getBerserkerRush :7740 (Update) | berserkerRush_ring + 2 x berserkerRush (status look) | **yes** |
| **Fury Trance** #262-264 | getFuryTrance :7920 (Update) | furyTrance1-3 (status look) + furyTrance1/2 voice | **yes** |
| Resting Glory #261 | RPC_restingGlory, from RPC_dead | nothing (heals teammates) | no |
| Over Pride #321-324 | onOverPride :8615, inside every Combo stage after a landed hit (:14907, :15730, :16541, :17339, :17629, :18436, :18726) | voice overPride1 / overPride2 (:8673, :8704; 1 s voice timer), a message | no: a roll on the nAttack clips (below) |
| Overlord #313-314 | createOverLord :8480 (Start :96) | `overLord` = a Bison_overLord trigger volume, no renderer (probe); the ally status `overLord` only does deltaDef (CharacterControl.cs:35327-35331) | no |
| Blood Rage #121-122 / Blood Bath #421 | getBloodRage :7180 (Update :265) | nothing (SP only, no message) | no |
| Raw Strength #431 | getBruteStrengthLv :7361-7393 | the message "Raw Strength!" only (:7382) | no |
| Colossal Armor #363-364, Iron / Diamond Skin, Steel / Mythril Skin | CharacterControl.cs:4011-4298 | nothing (that block has no load or Instantiate) | no |
| Hold Charge, Solid Hold, Spin Hack, Controlled / Improved Swing, Brute Strength, Added Swing, Colossal Weapon, Aspect of the Horde, Aftershock, Mass Stun, Power Hammer, Power Reel, Rage Control | inside skills that have clips | (in those skills' cues: holdCharge_ring / holdCharge, solidCharge_ring, spinHack_ring, aspect_*, afterShock, massStun, powerHammer_hit, powerReel_ring ...) | no (others) |
| perfectShield / perfectArmor (both shields at once) | the shields' status, CharacterControl.cs:35116-35164 | the perfectShield / perfectArmor looks | no (the shields' researcher; Open question 5) |

The weapon procs in `onNormalAttackHit` (:41619-42100) belong to Combo's hits: w_bsn19's `heal1` on the Bison 3 %, and
w_bsn69's Sheep `revert` at the Bison 1 % with a full heal. The others are statuses on the enemy. They are a matter for
the attacks / weapon-effects researchers, not tiles.

## How each reads (junk predicates evaluated by hand)

### Berserker Rush (max rank 4, Rage Control #402 on)
- **Trigger.** `Update` runs it for the owner (:277; the predicate `275832 - 86663 != 189169` is false, so the call
  runs). `while (isMine)` (:7745), and `myDamage != -1` → break (:7749). It goes on only on the frame after a hit took
  HP (the Blood Rage rule, Bible).
- **Rank.** `hasSkill(251)` … `(254)` (:7758-7794); every `continue` guard is false, so num = 4. The roll is
  `Random.Range(0, 100) >= lckAdjust(4 x 4)` → break (:7812), so it procs at 16 %. There is no cooldown.
- **On a proc.** It shows `newGameMessage "BerserkerRush!"` (:7818). Then `sTime = chaAdjust(3 + 3 x 1)` = 6 s (:7821)
  and `RPC_AddStatus("berserkerRush", 4 + 1, 6 s)` (:7824). It loads **no voice**: the 163-load map has none in
  getBerserkerRush, and the rip has no berserkerRush voice. TTO is the same (pseudo/Bison.c:25587-25640).
- **The apply** (CharacterControl.cs:34752, `$$switch == "berserkerRush"`, entry predicate `214485 - 118176 == 96309`
  true):
  - It first removes heavy, groundLock, needlePrison, sticky, ice, snowMan, frost, lightBind, sleep and maim when they
    are ≤ the level (:34752-34875). These draw nothing.
  - `Instantiate(berserkerRush_ring, mTransform.position, Quaternion.identity)` (:34876), then GetComponent EffectControl
    and `InitEffectControl(the hero)` (:34882). The predicates `258428 - 261535 != -3106` and `134685 - 361225 !=
    -226539` are true.
  - `moveMod += 0.1` (:34885).
  - It loads `berserkerRush` (:34888; `182055 - 274984 == -92929` and `196108 - 544535 == -348427` are true). It
    Instantiates it at Vector3.zero, identity (:34897), names it berserkerRush1Fx (:34902), parents it to HandMount_L
    (:34907), and sets localPosition 0 (:34912) and localScale 1 (:34917). It does the same again for berserkerRush2Fx
    on HandMount_R (:34922-34942). Every `continue` guard in between is false (checked one by one).
- **The removal** (CharacterControl.cs:15477-15508): moveMod − 0.1 and Destroy of berserkerRush1Fx and berserkerRush2Fx.
  So the hand looks last exactly as long as the status: 6 s.
- **The prefabs** (probe):
  - `berserkerRush_ring`: EffectControl life 1, afterLife 0, followPosition true, followState false. It has a
    RingEmitter (0.5 → 1.2 m, rising 0 → 1 m, life 0.35, 3 per 0.1 s, Blood1) and a one-shot world-space burst of 24-36
    red sparks.
  - `berserkerRush` (no EffectControl): a camera-facing ImageEmitter (red Splash1, 1 → 2 m, life 0.3,
    repeatForever) and a local-space ellipsoid of 3 Blood1 particles a second. A red pulse sits on each fist.
- **Rotation.** On `transform.parent = bone`, Unity keeps the world rotation (identity), and the code then sets only the
  position and scale. The page's `bone` option sets localRotation identity instead. Both looks are camera-facing quads
  and round, near-still particles, so they read the same either way, and no page part is needed.

### Fury Trance (max rank 3)
- **Trigger.** `Update` runs it for the owner (:289; `283478 - 162589 == 120890` is false, so it runs). If hp ≤ 0 →
  break (:7928). If not mine → break (:7937). The check `UuiqIBSEVe >= Time.time` → break (:7943) is the 3 s lockout.
- **Rank.** `for i = 3 → 1` with `hasSkill(261 + i)` (:7954), and the HP test `hp/mhp < 1 − (0.2 i + 0.2)` (:7960): rank
  3 needs HP under 20 %, rank 2 under 40 %, rank 1 under 60 %. If `getStatusLv("furyTrance") >= i` it returns (:7966).
  Max rank, HP under 20 %: it gives level 3.
- **On a proc.** It shows `newGameMessage "FuryTrance Lv.3"` (:7974). Then `RPC_AddStatus("furyTrance", 3,
  chaAdjust(12) = 12 s)` (:7979) and the lockout `Time.time + 3` (:7984).
- **The voice.** `pvoice` on (:7989). For the owner, `Random.Range(0, 2) == 0` (:8020) loads furyTrance1 (:8032);
  `94537 - 550479 != -455942` is false, so it goes to IL_AD = PlayOneShot (:8118). Otherwise it loads furyTrance2
  (:8064); `33362 - 386633 != -353270` is true, so it goes to Block_42 = PlayOneShot (:8123). Both play at volume 1 for
  the owner. There is no voice timer beyond the 3 s lockout.
- **The apply** (CharacterControl.cs:34956; `45707 - 118371 != -72663` is true):
  - `deltaAtk(3 x 20)` (:34960).
  - It loads `"furyTrance" + sLv` = **furyTrance3** (:34963), Instantiates it at zero, identity (:34972), and names it
    furyTranceFx (:34977).
  - It parents it to **Neck** (:34982) with localPosition 0 (:34987) and localScale 1 (:34992). All the guards in
    between are false.
- **The removal** (CharacterControl.cs:15451-15467): deltaAtk back, and Destroy furyTranceFx.
- **The prefabs** (probe): `furyTrance1/2/3` have no EffectControl. Each has a camera-facing red Splash1 ImageEmitter
  (1 → 2 m, life 0.3, repeatForever) and a world-space ellipsoid of Blood1 wisps rising with worldVelocity y. The rank
  makes them grow: rank 1 is 3 a second at 0.6 m/s, rank 2 is 3-12 at 0.8 m/s, rank 3 is 3-18 at 1.2 m/s and 0.6-1.5 m
  wide. A red aura rises from the neck.
- **A Bible finding (offer to the user).** After the `i` loop the code does `if getStatusLv("furyTrance") <= 0 break;
  RPC_RemoveStatus("furyTrance")` (:8098-8104; `251147 - 352428 == -101281` and `296243 - 197550 == 98693` are true).
  The loop only falls through when no learned rank's HP test passes, so **Fury Trance is removed as soon as HP climbs
  back to 60 % or more** (rank 1's threshold, with all three ranks learned). This happens on the first frame outside the
  3 s lockout. The status level never drops while HP stays low (at 30 % a level 3 stays 3). Also, the 3 s is a lockout
  after each add, not a fixed 3 s tick: otherwise the check runs every frame, so an expired status comes back on the next
  frame while HP is still low. `bison-skill-reference.md:80` says "a check every 3 seconds" and "Removed when the status
  level reaches 0 (:8098-8104)". The card's "ทุก **3 วินาที**" shares that reading.

### Over Pride (why it is not a tile, and a note for the attacks researcher)
- `onOverPride` (:8615) is called in every Combo stage only when that stage's best hit did damage. It sits after
  `if (mMaxDamage <= 0) goto` (nAttack1 :14895-14907), so it is inside the hit-landed branch, after `sp + 1`.
- It plays voice overPride1 / overPride2 (Random.Range(0, 2), :8673 / :8704, with a 1 s voice timer) and shows the
  message "OverPride". There is no effect.
- It is a roll on the `nAttack1-5` clips: Over Pride 4, `lckAdjust(20) + 1` % ≈ 21 % (:8532-8611). It is not a clip-less
  skill. With the 10 m target point, no Combo hit lands (the stages reach about 5-8 m), so by the rules the voice does
  not come. Open question 4.

## Choices made here (rule by rule)
- **Max rank / passives on.** Berserker Rush 4 + Rage Control gives level 5 for 6 s. Fury Trance 3 gives `furyTrance3`.
- **The proc every play** (Frost Spike's rule). The tile is the proc itself, so there is no `p` and no 16 % roll. The
  game's needs (a hit that took HP; HP under 20 %) are what make it happen.
- **Long buffs cut at 10 s.** Fury Trance's 12 s is `kill: 10`. Berserker Rush's 6 s stays 6.
- **Step lengths** (`root@t`): the held look's time, so the next round's look starts as the last one goes and no copies
  pile up. Berserker Rush 6 s (the status; the ring's life is 1). Fury Trance 10 s (the cut; the voice is ≤ 0.94 s).
- **No `rot`.** Both are identity at the hero or on a bone (see Rotation above).

## PASTE-READY

### 1. `wardrobe/index.html` SEQ: the bison line becomes (index.html:1153-1154; if another researcher has changed the
first two lines, keep theirs and append the comment and the two tiles)

```js
  bison: ["Normal Attack: nAttack1@0.7 nAttack2@0.7 nAttack3@0.8 nAttack4@0.8 nAttack5", "Charge Attack: cAttack1 cAttack2*~@7 cAttack6*@1.6",
    "Trample: trample1@0.9 trample2*@2.6",
    // Berserker Rush and Fury Trance (passives) play no animation: Update runs their procs (Bison.cs:277, :289), which only
    // add a status (:7824, :7979) whose look hangs on the hero's bones (CharacterControl.cs:34876-34942 HandMount_L / _R,
    // :34963-34992 Neck): their effects on the idle stance, each step the status's time (Berserker Rush 6 s with Rage
    // Control, Fury Trance cut at 10 s) (2026-11-13, plans/fx_bison/effect_only.md; the user 2026-11-10: effect-only tiles)
    "Berserker Rush: root@6", "Fury Trance: root@10"],
```

### 2. `wardrobe/index.html` SEQ_SKILL (index.html:3208-3210): add a bison entry in front of penguin

```js
const SEQ_SKILL = { bison: { "@BerserkerRush": "berserkerRush", "@FuryTrance": "furyTrance" },
  penguin: { "@MPTransfer": "mpTransfer", "@CosmicFriday": "cosmicFriday", "@ManaArc": "manaArc", "@Dispell": "dispell",
    "@DoubleCast": "doubleCast", "@TripleCast": "tripleCast", "@FrostSpike": "frostSpike" },
  sheep: { "@QuickHeal": "quickHeal", "@SealofAttack": "sealOfAttack", "@SealofDefense": "sealOfDefense", "@EdenSanctuary": "edenSanctuary" } };
```
(if another researcher adds bison ids here too, merge them into the one `bison: {...}`)

### 3. `wardrobe/fx_cues/bison.json`: two entries (the file is `{}` today; checked with json.load in
`checks/fx_bison_research/effect_only/cues.json`)

```json
  "@BerserkerRush:root": {
    "why": "Bison.cs getBerserkerRush (:7740-7830, run every frame from Update :277 for the owner; no clip: the Bison goes on with what she was doing; the tile plays the proc on the idle stance, every play) at max rank: on the frame after a hit took HP (myDamage == -1, :7749) it counts Berserker Rush 1-4 (#251-254, :7758-7794: 4) and rolls Random.Range(0, 100) < lckAdjust(4 x 4) = 16 % (:7812); a proc shows BerserkerRush! (:7818) and adds berserkerRush Lv 4 + Rage Control #402 (passives on) = 5 for chaAdjust(3 + 3) = 6 s (:7821-7824); the status's apply (CharacterControl.cs:34752-34942): berserkerRush_ring at the hero's position, identity, InitEffectControl(the hero) (:34876-34882; EffectControl life 1, followPosition), moveMod + 0.1 (:34885), and two Effects/berserkerRush parented to HandMount_L and HandMount_R, localPosition 0, localScale 1 (:34888-34942; no EffectControl: held until the status goes, whose removal destroys both, :15477-15508: kill 6); the game keeps their world rotation at the reparent where the bone option sets localRotation identity: camera-facing quads and round particles, the same look; no voice or sound (the method loads none, the prefabs have no AudioSource); the 10 control statuses it clears (:34752-34875) draw nothing",
    "cues": [
    [0, "fx", "berserkerRush_ring"],
    [0, "fx", "berserkerRush", {"bone": "HandMount_L", "kill": 6}],
    [0, "fx", "berserkerRush", {"bone": "HandMount_R", "kill": 6}]
    ]
  },
  "@FuryTrance:root": {
    "why": "Bison.cs getFuryTrance (:7920-8124, run every frame from Update :289 for the owner; no clip; the tile plays the proc on the idle stance, every play) at max rank (Fury Trance 3 #264: hasSkill(261 + i) for i = 3, :7954; HP under 1 - (0.2 x 3 + 0.2) = 20 %, :7960; a lower rank's look would be furyTrance1 / furyTrance2): FuryTrance Lv.3 message (:7974), the furyTrance status Lv 3 for chaAdjust(12) = 12 s (:7979; cut at 10 s, the long-buff rule), a 3 s lockout (:7984), voice furyTrance1 / furyTrance2 (Random.Range(0, 2) :8020; :8032 / :8064, PlayOneShot :8118 / :8123); the status's apply (CharacterControl.cs:34956-34992): ATK + 60 (:34960) and Effects/furyTrance + sLv = furyTrance3 (:34963) parented to the Neck bone, localPosition 0, localScale 1 (:34972-34992; no EffectControl: held until the status goes, whose removal destroys it, :15451-15467: kill 10)",
    "cues": [
    [0, "fx", "furyTrance3", {"bone": "Neck", "kill": 10}],
    [0, "voice", "furyTrance1|furyTrance2"]
    ]
  }
```
(The comma after the last `}` goes only if another entry follows. Check with
`py -3 -c "import json; json.load(open('wardrobe/fx_cues/bison.json', encoding='utf-8'))"`.) `bone` and `kill` are in
`wardrobe_fx_check.py`'s OPTS (:94). The page finds the bone by name in `C.byName` (index.html:3985-3990).

### 4. `pipeline/wardrobe_skill_icons.py` EFFECT_ONLY (:39)

```python
EFFECT_ONLY = {"bison": ["berserkerRush", "furyTrance"], "sheep": ["quickHeal"], "penguin": ["manaArc", "dispell", "doubleCast", "tripleCast", "frostSpike"]}
```
The Bible has `bison_berserkerRush4` and `bison_furyTrance3` (assets.js), so `best` finds both. Then run
`py -3 pipeline\wardrobe_skill_icons.py`, which adds `berserkerRush` / `furyTrance` to `data/icons/hd/index.json` with
clips ["root"] and writes `icons/hd/bison/berserkerRush.webp`, `furyTrance.webp`.

### 5. Build (merges into `wardrobe/data/bison/fx.json` and `sfx/`), then check

```
uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py bison --fx berserkerRush_ring,berserkerRush,furyTrance3 --voices furyTrance1,furyTrance2
py -3 pipeline\wardrobe_skill_icons.py
uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py D:/12tails-wardrobe checks/fx_bison dark --cls bison
```
A plain `wardrobe_fx.py bison` (once every Bison cue is in) picks these up from the cue file too. Commit
`wardrobe/data/bison/fx.json`, `sfx/v_furyTrance1.mp3`, `sfx/v_furyTrance2.mp3`, any new `data/fx/tex/*.webp`
(Splash1 / Blood1's textures, if not there yet) and `data/icons/hd/` (bison/berserkerRush.webp, bison/furyTrance.webp,
index.json).

## Open questions (each with my recommended answer)
1. **Should Berserker Rush and Fury Trance get tiles?** They are passive procs with no RPC of their own, unlike the
   Penguin's Frost Spike, which has `RPC_frostSpike_fire`. *Recommend yes:* they are skills, they fire with no clip, and
   they put visible looks on the Bison. This is the user's "one tile per skill" and effect-only rule.
2. **Fury Trance's rank.** *Recommend furyTrance3 only* (the max-rank rule). Ranks 1 and 2 are the same aura, thinner
   and slower. A pool `"furyTrance1|furyTrance2|furyTrance3"` would show HP-dependent levels at random, which the game
   does not do at random.
3. **Berserker Rush's length.** *Recommend 6 s* (Rage Control on, passives on). Without Rage Control it is 3 s: then use
   `root@3` and `kill: 3`.
4. **Over Pride's voice on the Combo tiles** (for whoever writes `nAttack1-5`). *Recommend leaving it out.* It plays
   only after a stage's hit did damage, and at the 10 m target no Combo hit lands. If the user wants it anyway, it is
   `[t_hit, "voice", "overPride1|overPride2", {"p": 0.21}]` at each stage's hit time.
5. **Perfect Shield / Perfect Armor** (both shields at once: CharacterControl.cs:35116-35164, voices perfectShield1/2
   in the rip). This is a state of two clip skills (`warcry` clip), not effect-only. *Recommend* the shields'
   researcher decide it. It is not a separate tile here.
6. **The Fury Trance Bible finding** (above: removed when HP climbs back over 60 %, and a 3 s lockout rather than a 3 s
   tick). *Recommend offering it to the user for bison-skill-reference.md:80 and the card.* Do not write it there from
   here.

## Verification

Checker, 2026-11-13 (home PC), read only. The RPC_* listing redone with the same regex (and a second pass for
`internal` / `static` / `[RPC]` declarations: none), `clip_calls.js` for the Bison, the 18 `cType`s in BisonSkill.cs,
`getBerserkerRush` (:7740-7830) and `getFuryTrance` (:7920-8124) raw with every opaque predicate worked out by hand,
Update's calls (:271-293), the status apply / removal in CharacterControl (:34752-34992, :15451-15508), every
`Heroes/Bison/` load in CharacterControl (12: berserkerRush, berserkerRush_ring, furyTrance, overPower_horn / _ring,
iron / diamond / perfectShield / perfectArmor, titanForm, holdCharge / holdCharge_ring: none missed), the TTO method
table, my own `--probe` on berserkerRush_ring / berserkerRush / furyTrance3, `rig.json`, the icon keys in the Bible's
assets.js, and `wardrobe_skill_icons.py` / `wardrobe_fx.py`'s CLI. Outputs in `checks/fx_bison_research/verify_b/`.

**Confirmed** (no change):
- **63 RPC_* definitions**, every line number and group as listed. Not one is a clip-less skill press; the 18 actives
  (BisonSkill.cs :431-1968) all play a clip (`clip_calls.js`: the 26 skill RPCs; no call found only for magmaQuakeAxe,
  titanDrop, unchainedFury, volcanicRam).
- Berserker Rush: Update's call runs (`275832 - 86663 != 189169` false, :273-277), num = 4 (each `continue` guard
  false), the 16 % roll (`>= lckAdjust(16)` breaks, :7812), 6 s at level 5 with Rage Control #402 (:9047-9049,
  :7821-7824), the ring at the hero / identity / InitEffectControl (EffectControl life 1, afterLife 0, followState
  false), the two held hand looks (no EffectControl) on HandMount_L / _R destroyed at removal (:15484-15508), no voice.
- Fury Trance: the call runs (:289), rank 3 under 20 % HP, 12 s, the 3 s lockout (:7984), the voice pair
  (`94537 - 550479 != -455942` false -> IL_AD :8118; `33362 - 386633 != -353270` true -> Block_42 :8123),
  furyTrance + sLv = furyTrance3 on Neck (no EffectControl), removal :15451-15467.
- The Bible finding is right: after the rank loop `251147 - 352428 == -101281` and `296243 - 197550 == 98693` are true,
  so the status is removed on the first unlocked frame where no learned rank's HP test holds (60 % or more), and a held
  level never drops while HP stays low (:7966 returns).
- Rotation: furyTrance3's ellipsoid is a 0.2 m sphere simulated in world space with worldVelocity (0, 1.2, 0);
  berserkerRush's is a 0.2 m local sphere with a symmetric 0.1 rndVelocity. The page's bone option (localRotation
  identity instead of the game's world identity) changes neither look, as the report says.
- Bones HandMount_L, HandMount_R, Neck in `data/bison/rig.json`; icons `bison_berserkerRush4` / `bison_furyTrance3` in
  assets.js; `--fx` / `--voices` exist and the build merges into fx.json (wardrobe_fx.py :387-390, :430-433);
  EFFECT_ONLY gives the clip `root` (wardrobe_skill_icons.py :90). index.html lines 1153-1154 (SEQ bison) and
  3208-3210 (SEQ_SKILL) are right. Both cue entries: valid JSON, times in order, options in OPTS.
- Resting Glory, Over Pride (21 %: `Random.Range(0, 100) > lckAdjust(20)` fails, :8597), Overlord, the basic-move and
  mission lines (:40354, :40401, :13689, :13748, :40733-41548) all as stated.

**Corrections:**
1. **The SEQ block (paste-ready 1) keeps `"Trample: trample1@0.9 trample2*@2.6"`.** skills_b (checked above, its
   Verification) shows trample2 stands at 2.4 s (Bison.cs:22197-22220: i reaches 2 + 5 x 2 = 12 after 12 passes 0.2 s
   apart from 0.9 s): the merged line must read `trample2*@2.4`. Corrected block below.
2. The Bible line for Fury Trance is **bison-skill-reference.md:292** ("a check every **3 seconds** (`:7984`) ...
   Removed when the status level reaches 0 (`:8098-8104`)"), not :80 (:80 is about Enrage's duration). The card's
   "ทุก **3 วินาที**" is `bison_furyTrance` at 12t_projects/bible/index.html:17575. (Result, Fury Trance section and
   open question 6.)
3. Load count: Bison.cs has **164** `Resources.Load` of Effects / Voices / Sounds, not 163: `loads.txt` misses :34805
   (RPC_emotion's `Voices/` + the emote name). It adds no effect-only skill.
4. Wording: the 26 skill RPCs make 31 `PlayAnimation` calls but play **27 distinct clips** (warcry three more times,
   overPower once more). The "31" is the class's skill-clip count in clips.json, 4 of them never called.

Corrected paste-ready 1 (`wardrobe/index.html` SEQ, the bison line; the rest of the report's blocks 2-5 stand as
written):

```js
  bison: ["Normal Attack: nAttack1@0.7 nAttack2@0.7 nAttack3@0.8 nAttack4@0.8 nAttack5", "Charge Attack: cAttack1 cAttack2*~@7 cAttack6*@1.6",
    "Trample: trample1@0.9 trample2*@2.4",
    // Berserker Rush and Fury Trance (passives) play no animation: Update runs their procs (Bison.cs:277, :289), which only
    // add a status (:7824, :7979) whose look hangs on the hero's bones (CharacterControl.cs:34876-34942 HandMount_L / _R,
    // :34963-34992 Neck): their effects on the idle stance, each step the status's time (Berserker Rush 6 s with Rage
    // Control, Fury Trance cut at 10 s) (2026-11-13, plans/fx_bison/effect_only.md; the user 2026-11-10: effect-only tiles)
    "Berserker Rush: root@6", "Fury Trance: root@10"],
```
