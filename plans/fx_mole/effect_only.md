# Mole: the skills with no body animation (effect-only tiles)

Research only (2026-11-13, home PC). Read-only researcher: nothing in the repo was changed but this report and files
under `checks/fx_mole_research/effect_only/`. One probe ran, `--probe` only (`uv run --no-project --with UnityPy python
-I pipeline/wardrobe_fx.py mole --probe reload,fireBarrage_signal,fireBarrage_r,...,synchroMole,bombardment`, exit 0;
output `probe.json`, summary `probe_summary.txt`; `bombardment` alone is not a prefab, see Fire Barrage / Bombardment).
Sources: `D:\12tails\DecompiledSource\Mole.cs` (cited `:line`), `CharacterControl.cs`, `Math.cs`, `MoleEquipment.cs`,
the Bible's `12t_reference/mole-skill-reference.md` and skill cards (`12t_projects/bible/index.html`, `assets.js`), the
TTO method table and pseudo-C (`DecompiledSource_TTO_2026-11-02/methods.tsv`, `pseudo/Mole.c`, `pseudo/MoleSkill.c`),
`plans/fx_inventory.md` (mole), `wardrobe/data/mole/clips.json`, and the rip's voices / sounds
(`RippedAssets/.../heroes/mole/voices|sounds`). Templates followed: the Bison's, Cat's and Penguin's `effect_only.md`
(the Sheep's Quick Heal shape). Helpers in `checks/fx_mole_research/effect_only/`: `loads.txt` (all 183 `Heroes/Mole/`
Effects / Voices / Sounds loads in Mole.cs with the method holding each), `clip_calls.txt`, `flow_RPC_*.txt`,
`bb_rpc.txt` / `tto_rpc.txt` / `groups.txt` (the RPC accounting, checked to cover the 102 exactly once), `cues.json`
(the four cue entries, checked with `json.load`).

## Result

**Four Mole actives play no body clip**: the dispatcher (`doSkill`, Mole.cs:6338-8972, which calls no PlayAnimation /
animation.Play / CrossFade at all) calls or starts their RPC straight, and none of those RPCs (nor what they start) plays
a clip. The Mole goes on with whatever she was doing (the cast only needs standby / run / emotion, :6444-6458). Each gets
an idle-stance tile, as the Sheep's Quick Heal / the Penguin's Mana Arc:

| Tile (Bible name) | Bible icon | Code | Effects (max rank) | Voices | Buildable |
|---|---|---|---|---|---|
| **Reload** | `mole_reload2` | `RPC_reload` :10168 (plain method, called :8942) | `reload` at the hero | reload1 / reload2 | yes (ready) |
| **Fire Barrage** | `mole_fireBarrage2` | `RPC_fireBarrage` :11403 (coroutine :28462, started :8636) + `RPC_fireBarrage_fire` :11410 (:28859) | `fireBarrage_signal`; 3 aircraft `fireBarrage_<colour>`; `fireBarrage_hit2` | fireBarrage1 / fireBarrage2 | yes (ready), **plus the colour pick (P1)** |
| **Bombardment** | `mole_bombardment2` | `RPC_bombardment` :11417 (:29343, started :8420) + `_fire` :11424 (:29738) + `_hit` :11431 (:30119) | `bombardment_signal`; 3 bombers `bombardment_<colour>`; 15 `bombardment_fire`; 15 `bombardment_hit` | bombardment1 / bombardment2 | yes (ready, AlphaTimer built), **plus P1** |
| **Synchro Mole** | `mole_synchroMole2` | `RPC_synchroMole` :13220 (plain method, called :7920) -> status apply CharacterControl.cs:37714-37748 | `synchroMole_ring` at the hero (held, 30 s, cut at 10) | synchroMole1 / synchroMole2 | yes (only built parts) |

All four voices pairs are in the rip (reload1 0.758 s / reload2 1.087, fireBarrage1 0.781 / 2 1.242, bombardment1 1.314
/ 2 1.535, synchroMole1 1.106 / 2 1.359). The effects' own sounds come with their AudioSources (signal 2.306 s, plane
0.891 s looped, fireBarrage 1.306, bombardment 1.999, synchroMole 1.4). Every prefab is built only from parts the page
already has (probe): EffectControl, RingEmitter, LineEmitter, ImageEmitter, Ellipsoid emitter + ParticleAnimator +
ParticleRenderer, StaticMesh, SkinnedMeshRenderer with Animation, AudioSource, AlphaTimer (`bombardHit_tri`; built for the
Bison). None has `followState`. `synchroMole_ring` and `synchroMole` are not in `plans/fx_inventory.md` (loaded from
CharacterControl.cs, not Mole.cs); the probe shows them buildable.

**One page part is missing (P1, below):** Fire Barrage's aircraft and Bombardment's bombers are picked by the hero's
colour (`Math.div(mChar.Skin, 100)`: 1 `_r`, 2 `_g`, 3 `_b`, 4 `_k`, 5 `_w`, anything else `_r`; Mole.cs:29096-29163,
:29961-30028). The page has no cue that follows the hero's colour. The cues below use a new option `"pick": "color"`.

**No Mole passive fires on its own with a look on the Mole** (unlike the Bison's Berserker Rush / Fury Trance): Mole.Update
(:133-465) calls only the shared gear updates (WeaponUpdate :168, TrinketUpdate :180, BootUpdate :192, PetUpdate :204),
PlayerControl (:232) and the KO / death checks (:361, :425); CharacterControl.cs loads one Mole effect pair only,
synchroMole_ring / synchroMole (:37724, :37782). The passives table below checks each one.

**TTO:** every TTO-only Mole skill plays a clip (Barrel Railgun, War Area on `barrelCannon`, Twin Warhead on Missile's
`missilePad`, King Kaiser's `kaiserArsenal`), so nothing here is TTO. TTO keeps the four skills above with small changes
(below); BB's code is the content.

## Accounting: every RPC_* in Mole.cs (102 definitions)

`grep -nE "^\s*(public|private|protected|internal)[^(]*\bRPC_\w+\(" Mole.cs` gives 102, all `public virtual`
(`checks/.../bb_rpc.txt`; `groups.txt` puts each in one group, diffed against the list: the same 102).

**Skills whose clip is in the other researchers' list (30 RPCs; `clip_calls.js`):** RPC_nAttack1 :10056 / nAttack2
:10063 (`nAttack1/2`), RPC_cAttack1 :10154 (`superDig`, `dig1`), RPC_assemble1 :10470 (`assemble2`, `assemble1`: Auto Gyro
Gun, Barrel Bot and War Capital, :4960-5184, :6013, :7579), RPC_mine :10515, RPC_mortarShot :10738, RPC_bunker :10947,
RPC_tnt :11005, RPC_stunMine :11012 (`mine`), RPC_stunGrenade :11265 (`grenade`), RPC_flameTurret :11389 (`flameTurret2`,
`flameTurret1`), RPC_timeNuke :11605 (`mine`), RPC_detonate :11744, RPC_skyDrill :12265, RPC_megaPunch :13055 (`punch`),
RPC_megaHammer :13105 (`hammer`), RPC_chopper :13112, RPC_missile :13126, RPC_kingKaiser :13593 (`dig1`), RPC_advanceRepair
:13658, RPC_napalm :13707 (`mortarShot`), RPC_grenadeCluster :13780, RPC_flameCarnival :13885 (`mine`), RPC_megaDrill
:13899 (`punch`), RPC_barrelCannon :13949, RPC_sawMachine :13956, RPC_bazooka :14006, RPC_teslaCoil :14056,
RPC_rollerMachine :14063, RPC_cartBomb :14113 (the five War Factory units, `warFactory`).

**Effect-only skills (this report, 4):** RPC_reload :10168, RPC_fireBarrage :11403, RPC_bombardment :11417,
RPC_synchroMole :13220.

**Their own phases (4):** RPC_fireBarrage_fire :11410, RPC_bombardment_fire :11424, RPC_bombardment_hit :11431 (all in the
cues below), RPC_synchroMole0 :13514 (the end: strips the status from the summons, draws nothing).

**Phases of the other researchers' skills (40):** nAttack_fire :10070, nAttack_hit :10103, cAttack0 :10161 (Charge
Attack's surfacing, dig_dust), assemble0 :10477 (assemble's cancel), mine_create :10522, mine_hit :10529,
mortarShot_fire :10745, mortarShot_hit :10804, bunker0 :10954, stunMine_create :11019, stunMine_hit :11026,
stunGrenade_fire :11272, stunGrenade_hit :11346, flameTurret_rotate :11396, smartShell_hit :11489 (Smart Shell #264,
called from the mines' triggers, Mole_mine.cs:402 / Mole_stunMine.cs:402, at the mine an enemy steps on), timeNuke_create
:11612, autoGyroGun_create :11751, skyDrill_hit :12272, barrelBot_create :12279, megaPunch_hit :13062, chopper_hit
:13119, missile_fire :13133, missile_hit :13206, kingKaiser_create :13600, advanceRepair0 :13665, napalm_fire :13714,
napalm_hit :13773, grenadeCluster_fire :13787, grenadeCluster_hit :13842, flameCarnival_fire :13892, megaDrill_hit :13906,
sawMachine_hit :13963, bazooka_hit :14013, rollerMachine_hit :14070, cartBomb_update :14120, cartBomb_hit :14128, and War
Capital's four: warCapital_create :14239 (the base, its `warCapital` effect and the laugh voice, from RPC_assemble1),
warCapital_fire :14487 (started every 24 s by the base's OnWarCapital, :43892), warMissile_fire :14494, warMissile_hit
:14589 (Open question 5).

**Shared by every class (24):** the 13 supplement skills (obsidianFang :14739 / _hit :14746, stunningGround :14789,
psalmOfEnergy :15029, seaAegis :15199, assassinate :15386, zephyrLore :15393, mineWalker :15487, replenishment :15494,
elementalBound :15623, divineChannel :15769, astralShift :15776, bloodCarnage :15967; the Bible leaves them out of the
Mole's roster, "Notes on judgment calls", as the Bison's report did); emotion :16314 / emotion0 :16321; useItem :16761,
useMount :16818 (voices mount1 / mount2 / cast), useCoin :16871, petEffect :19065; activateIcon1 :19103 / activateIcon2
:19110 (the mission: no tile, Penguin decision 19); ko :19208, dead :19215, revive :19222 (the basic moves' KO tile).

Totals: 30 + 4 + 4 + 40 + 24 = **102**. Every Mole active is in one of the first two groups (the Bible's 28 BB actives:
the 24 with clips above, incl. Auto Gyro Gun / Barrel Bot / War Capital through assemble, King Kaiser through dig1, the
War Factory steps; and the four here).

## The passives, each one checked

| Passive (Bible) | Where it runs | Draws on the Mole? | Tile? |
|---|---|---|---|
| Gadgeteer, Genius Invention | the Workshop / item cooldowns (Bible) | no | no |
| Stat Plus, Super Stat Plus, Revised Skill / Magic / Art | stats / cooldowns | no | no |
| Extra Powder, Cannon Expert, Mine Lover, Super TNT, Heavy Built, Double Bot, Speed Drill, Super Dig, Sky Drill, Sky Shaker | inside skills with clips (radii, damage, superTNT_hit in TNT, dig dust in Charge Attack, Sky Drill on its release) | in those skills' cues | no (others) |
| Smart Shell #264 | RPC_smartShell_hit from a mine's trigger (Mole_mine.cs:402) | `smartShell_hit` at the mine, i.e. at an enemy | no (the mine researcher; it needs an enemy on the mine) |
| Hidden Turret #403 | the Auto Gyro Gun's own RPC_hide (AutoGyroGun.cs) | the turret's look, not the Mole's | no (assemble) |
| Kaiser Cannon #372, Kaiser Beam #373 | the King Kaiser robot's own attacks (KingKaiser.cs) | the robot | no (King Kaiser) |

Mole.Update has no per-frame proc like the Bison's (above), and the weapon procs (WeaponUpdate, onNormalAttackHit) are the
attacks / weapon-effects researchers'.

## How each reads (junk predicates worked by hand)

### Reload (max rank 2)
- **Dispatch.** `mol_reload2` gives num 2 (:6472-6484); the dispatcher calls `RPC_reload(position, forward, 0, num)`
  directly (:8942) and sends `RPC_reload` + num (:8951). No clip, no actionState change.
- **Body** (:10168-10465, a plain method in a `for (;;)` with junk `continue`s, every one false):
  - removeTimeOut on 13 cooldowns (:10175-10211), at rank 2 nine more (flameTurret ... kingKaiser, :10220-10260), with
    Advance Repair #431 eight more (:10266-10307); `sp + ceil(0.5 x sLv x msp)` (:10313); `addTimeOut("reload",
    agiAdjust(240))` (:10316; `291853 - 336698 != -44844` true).
  - `Effects/reload` (:10325; `258696 - 95337 != 163359` false) and `createEffect(reload, transform.position,
    transform.rotation)` (:10337; `227180 - 413773 != -186593` false).
  - Voice (pvoice on, the owner): `Random.Range(0, 2) == 0` (:10380): reload1 (:10390); `87880 - 259435 != -171554` true
    -> break -> PlayOneShot (:10460). Else reload2 (:10421); `93588 - 168665 != -75076` true -> Block_63 PlayOneShot
    (:10465). Both play, volume 1 for the owner.
- **Prefab `reload`** (probe): EffectControl life 1, afterLife 0, followPosition, no followState; a RingEmitter (1.2 ->
  0.2 m, blue, 3 per 0.1 s, life 0.25) and a LineEmitter burst of 24 (life 0.3) 0.55 m up. A blue ring closing on the
  Mole.
- **TTO** (pseudo/Mole.c:29592-29954): the same list, effect and voices.

### Fire Barrage (max rank 2)
- **Aim** (doSkill): with a target, `mPos = getSpawnPos(target - vector2)` (:8539), vector2 = the unit flat direction from
  the Mole to the target (:6399-6402): **1 m in front of the target, on the Mole's side**. With the standing 10 m target
  point: **9 m ahead**, `tDir` = the hero's facing. (No target: the cursor's ground point, :8571, or 12 m ahead, :8596;
  the Bible's "Where it lands", mole-skill-reference.md.) The coroutine starts at :8636.
- **RPC_fireBarrage** (:28462-28855):
  - case 0 at the press: `Time.time > ww8gUcG76C + 3` (:28644; ww8 is 0 after the last cast, so true) -> voice: pvoice,
    the owner, `Random.Range(0, 2) == 0` (:28679) -> fireBarrage1 (:28691, PlayOneShot :28703; the guards in between all
    false), else fireBarrage2 (:28722, PlayOneShot :28734).
  - `addTimeOut("fireBarrage", 0.5)` (:28748), `ww8 = mTimer = Time.time + 2` (:28751-28754; `185645 - 216516 !=
    -30870`, `165394 - 160246 != 5149`, `39683 - 424713 != -385029` all true). If the local player is on the Mole's
    layer (:28757-28763; the wardrobe's Mole is): destroy an old signal, load `fireBarrage_signal` (:28787) and, inside
    `22501 - 162204 == -139703` (true), Instantiate it at mPos with **the hero's rotation** (:28797). Then Yield 2 s
    (:28819).
  - case 2 at 2.0 s: for the owner, if no re-press moved the timer (`ww8 == mTimer`): `addTimeOut(agiAdjust(120))`
    (:28602), ww8 = 0, StartCoroutine `RPC_fireBarrage_fire(mPos, tDir, 0, sLv)` (:28612), ActionEvent (:28623); then
    the coroutine ends (Block_44 -> return false).
- **RPC_fireBarrage_fire** (:28859-29290), started at 2.0 s:
  - case 0: the aircraft prefab (cached in E4CgCI52Rb the first time): `Math.div(Skin, 100)` (:29096) 1 `_r` (:29107),
    2 `_g` (:29119), 3 `_b` (:29131), 4 `_k` (:29143), 5 `_w` (:29155), else `_r` (:29163). Instantiate at mPos,
    `LookRotation(tDir)` (:29176). `sLv <= 1` -> break; at rank 2 (`249128 - 463222 != -214094` false): `tDir1 =
    rotateH(tDir, 30)`, `tDir2 = rotateH(tDir, -30)` and two more at `mPos - rotateNormal((-3, 0, -3), tDir1)`,
    `LookRotation(tDir1)` (:29199) and `mPos - rotateNormal((3, 0, -3), tDir2)`, `LookRotation(tDir2)` (:29204); then
    `279606 - 242744 != 36863` true -> break -> Yield 1.3 s (:29280).
  - The geometry (Math.cs:838-880): `rotateH(v, a)` turns v by a degrees towards -x (left) seen from above; `rotateNormal(v,
    n)` = v turned from the hero's frame (x right, z forward) into n's frame (= `LookRotation(n) * v`). tDir1 points 30 deg
    left (Unity yaw -30): its plane spawns at mPos + (1.098 right, 4.098 forward) = **x 1.098, d 13.098, rot [0, -30, 0]**;
    tDir2's at **x -1.098, d 13.098, rot [0, 30, 0]**. (BB subtracts here where Bombardment adds: the two side planes
    start beyond the target and cross over it; kept as the game.)
  - case 2 at 3.3 s: `sLv == 1` -> fireBarrage_hit1 (:29000-29012), else **fireBarrage_hit2** (:29035-29047), at mPos with
    the hero's rotation. Then, for the owner, the four damage waves 0.1 s apart (:29227-29285; FindAreaTarget + hit, no
    effect).
- **Prefabs** (probe): `fireBarrage_signal` EffectControl life 3 (gone at 3.0 s), a StaticMesh marker, a 2-image
  ImageEmitter and an ellipsoid puff, AudioSource `signal` (2.3 s) on awake. `fireBarrage_r/g/b/k/w` EffectControl life
  3: `Mole_fireBarrage` with a 3 s Animation flying the `plane` SkinnedMesh in over the spot, its looped
  `plane` sound, four LineEmitter muzzle bursts at 1.1 s and two smoke trails; the five differ only in the plane's
  texture. `fireBarrage_hit2` EffectControl life 1 + afterLife 1, two ImageEmitters of 48 (hit1: 32), AudioSource
  `fireBarrage`. All ready in the inventory.
- **Times:** voice 0, signal 0, aircraft 2.0, impact 3.3; the last thing ends at 3.3 + 2 = 5.3 s.
- **TTO** (unreleased; pseudo/Mole.c:9651-10373): the same timeline; the aircraft gain a 1.4 x change when
  `BarrageLv3` (rank 2 and TTO skill #452, `hasSkill(0x1c4)`) holds. No cue.

### Bombardment (max rank 2)
- **Aim:** the same three branches (:8373 with a target, :8450 / :8480 without): **9 m ahead**, `tDir` = facing. Started
  :8420.
- **RPC_bombardment** (:29343-29733): voice bombardment1 / bombardment2 (`Random.Range(0, 2)` :29560; :29572 ->
  PlayOneShot :29584, :29603 -> :29615; the guards false); `addTimeOut(0.5)` (:29629), timer = Time.time + 4 (:29632);
  own team only (:29638-29644): `bombardment_signal` (:29668) at mPos, **Quaternion.identity** (:29678, inside
  `239229 - 883 == 238346`, true); Yield **4 s** (:29700). case 2: `addTimeOut(agiAdjust(180))` (:29483), StartCoroutine
  `RPC_bombardment_fire` (:29493).
- **RPC_bombardment_fire** (:29738-30078), from 4.0 s: the bomber prefab (cached in asJgP4DOCn; it first tries an
  untyped `Effects/bombardment` (:29956), which is no prefab (the probe's KeyError), then the colour switch overwrites it,
  :29961-30028, the same mapping as Fire Barrage). Instantiate at mPos, `LookRotation(tDir)` (:30039); at rank 2
  (`76851 - 363085 != -286233` true) two more at `mPos + rotateNormal((-3, 0, -3), tDir)` = **x -3, d 6** (:30048) and
  `(3, 0, -3)` = **x 3, d 6** (:30051), both `LookRotation(tDir)`. Yield 1.2 s (:30071). case 2 at 5.2 s (the owner):
  i = 0..4, each `hitPos = getSpawnPos(mPos + tDir x (3i - 6))` (:29912) = **d 3, 6, 9, 12, 15**, StartCoroutine
  `RPC_bombardment_hit(hitPos, tDir, 0, sLv)` (:29929), ActionEvent, Yield 0.1 s (:30073): strikes at **5.2, 5.3, 5.4,
  5.5, 5.6 s**.
- **RPC_bombardment_hit** (:30119-30451), per strike from its start:
  - +0: `bombardment_fire` (:30418) at hitPos, `LookRotation(tDir)` (:30428, inside `91142 - 314282 == -223140` true);
    `238547 - 426283 != -187735` true -> Yield 0.2 (:30447).
  - +0.2: rank 2 (`sLv <= 1` goes straight to the 0.4 wait): `bombardment_fire` at `hitPos + rotateNormal((-3, 0, -3))`
    and `((3, 0, -3))` (:30256, :30261), i.e. 3 m left / right, 3 m nearer; Yield 0.4 (:30449).
  - +0.6: `bombardment_hit` at hitPos (:30286) and at rank 2 the two sides (:30297, :30302), all `LookRotation(tDir)`;
    then the damage (:30317-30394).
- **Prefabs** (probe): `bombardment_signal` EffectControl life 5 (the same marker, `signal` sound). `bombardment_r/g/b/k/w`
  EffectControl life 3: `Mole_bombardment`, a 3 s Animation of the bomber flying over, looped `plane` sound (`_b`'s
  AudioSource has loop off: a data quirk, kept). `bombardment_fire` EffectControl life 2: `Mole_bomb`, a 0.6 s Animation
  dropping the bomb from (7, 0, 14) local onto the spot, AudioSource `bombardment` (2.0 s). `bombardment_hit`
  EffectControl life 1 + afterLife 1: `bombardHit_tri` (a StaticMesh growing x8 in 0.5 s, AlphaTimer), two image bursts,
  a scorch ImageEmitter (life 2) and a RingEmitter.
- **Times:** voice / signal 0, bombers 4.0, bombs 5.2-5.8, blasts 5.8-6.2 (the Bible's 5.8 / 5.9 / 6.0 / 6.1 / 6.2 s),
  the last blast's afterLife ends at 8.2 s. 3 bombers, 15 bombs, 15 blasts.
- **TTO** (unreleased; pseudo/Mole.c:4844-5853): the same flow, the strikes through a `BombardmentFx` helper and
  `BarrageLv` (#452). No cue.

### Synchro Mole (max rank 2)
- **Dispatch:** `mol_synchroMole2` num 2 (:6982-6994); called directly (:7920), ActionEvent (:7933). No clip.
- **Body** (:13220-13510): `addTimeOut(agiAdjust(300))` (:13228); for the owner `RPC_AddStatus("synchroMole", 2,
  chaAdjust(30), tal)` on the Mole (:13237-13242) and `num + 1` s on every own Auto Gyro Gun 1-5 / Barrel Bot 1-5 found by
  tag (:13247-13370); voice: `Random.Range(0, 2)` (:13437) synchroMole1 (:13447; `239432 - 538524 != -299091` true ->
  Block_47 PlayOneShot :13506) or synchroMole2 (:13478; `19958 - 558214 == -538256` true -> IL_549 PlayOneShot :13509).
- **The status on the Mole** (CharacterControl.cs:37714-37748, `Type == "Mole"`; `44612 - 166665 == -122053` true, the
  other guards false): `synchroMole_ring` Instantiated at `mTransform.position`, `Quaternion.identity`, **parented to the
  hero** and named synchroMoleRingFx. The summons' branch (else, :37760-37806: the green `setColor(0.4, 0.9, 0.4)`,
  deltaAtk / deltaDef, and `synchroMole` over the head at `bounds.center + 0.5 x height`) is not the Mole's.
- **Removal** (CharacterControl.cs:16978-17028): destroys synchroMoleRingFx (:16989-16998) and calls RPC_synchroMole0
  (:17016). So the ring lasts the status: 30 s, **cut at 10 s** (the long-buff rule).
- **Prefab `synchroMole_ring`** (probe): no EffectControl; AudioSource `synchroMole` (1.4 s) on awake; two LineEmitters
  and two RingEmitters (one-shot) and an ImageEmitter repeating (life 1.2) on the ground: a green ground glow under the
  Mole while the buff lasts. The page has no follow for a no-EffectControl effect; the tile's hero stands, so `d 0` with
  `kill 10` reads the same.
- **TTO** (pseudo/Mole.c:34310-34530): the same.

## Choices made here (rule by rule)
- **Max rank:** Reload 2, Fire Barrage 2 (three aircraft, hit2), Bombardment 2 (three bombers, side bombs), Synchro Mole 2.
- **The 10 m target point:** Fire Barrage and Bombardment aim 1 m in front of their target (:8539, :8373), so 9 m. (Open
  question 1.)
- **Rotations:** `LookRotation(tDir)` and the hero's rotation = no `rot`. `Quaternion.identity` (Bombardment's signal,
  Synchro Mole's ring) = no `rot`, as the Bison's identity looks: a flat ground marker / a ground glow. The two side
  aircraft keep their yaw (`rot [0, -30, 0]` / `[0, 30, 0]`). Nothing here is drawn with the target's rotation.
- **The colour pick:** the game's own choice by the hero's colour, not random (`"pick": "color"`, P1).
- **Long buff cut at 10 s:** Synchro Mole's ring `kill: 10`.
- **Step lengths:** the longest effect or voice: Reload 1.1 s (reload2 1.087 s; the effect's life 1), Fire Barrage 5.3 s,
  Bombardment 8.2 s, Synchro Mole 10 s. The Mole's idle `root` is 5.0 s (clips.json), and a once step clamps on its last
  frame (the Cat's decision 9), so all four are written held, `root*@t` (harmless on Reload's 1.1 s, as the Cat's
  Treasure Hunt).

## Missing page part

### P1. A cue that follows the hero's colour (`"pick": "color"`)
- **Why:** Fire Barrage's aircraft and Bombardment's bombers (and, for the King Kaiser researcher, `KingKaiser_r/g/b/k/w`,
  Mole.cs:35709-35776) are chosen by `Math.div(mChar.Skin, 100)`. `Skin` is the hero's skin number 100-599
  (MoleEquipment.cs:282-294), whose hundreds pick the outfit texture `Mole_<outfit><n>` (MoleEquipment.cs getArmorMaterial
  :1486, `Math.div(nSkin, 100)` :1504): the same 1-5 the page keeps as `C.state.color` (index.html:808-860).
- **Interface:** a cue's name list `a|b|c|d|e` with the option `"pick": "color"` takes the `C.state.color`-th name (1 =
  first), the first one when the colour is outside the list (the game's `else` = `_r`). Without `pick` the list stays a
  random pick.
- **Where:** `wardrobe/index.html` cueOf (:4553-4562): `name: o.pick === "color" ? (ns[(C?.state?.color ?? 1) - 1] ??
  ns[0]) : ns[Math.floor(Math.random() * ns.length)]`; `pipeline/wardrobe_fx_check.py` OPTS (:163-164) gains `"pick"`.
  The build already builds every name of a `|` list (wardrobe_fx.py cue_names :570), and the check's spawn test already
  skips `|` names (wardrobe_fx_check.py:150); its data test (:140) still sees all five.
- **Game detail kept out:** BB caches the first prefab it loads (E4CgCI52Rb, asJgP4DOCn), so in the game a colour change
  mid-session keeps the old plane until a relog; the page follows the current colour (Open question 2).

## PASTE-READY

### 1. `wardrobe/index.html` SEQ: the mole line (index.html:1232-1233) gains a comment and four tiles (if another
researcher has changed the first lines, keep theirs and append these)

```js
  mole: ["Normal Attack: nAttack1 nAttack2", "Assemble: assemble1 assemble2*@0", "Flame Turret: flameTurret1 flameTurret2*@3",
    "Barrel Railgun: barrelRailgun1 barrelRailgun2*@6 barrelRailgun3@0.65 barrelRailgun4",
    // Reload, Fire Barrage, Bombardment and Synchro Mole play no animation: the dispatcher calls RPC_reload (Mole.cs:8942)
    // and RPC_synchroMole (:7920) straight and starts RPC_fireBarrage (:8636) and RPC_bombardment (:8420), none of which
    // plays a clip (doSkill :6338-8972): their effects on the idle stance, held (the 5 s idle loops) as long as the last
    // effect or voice: Reload 1.1 s (reload2), Fire Barrage 5.3 s (the impact at 3.3 + 2), Bombardment 8.2 s (the last
    // blast at 6.2 + 2), Synchro Mole 10 s (its 30 s ring cut at 10) (2026-11-13, plans/fx_mole/effect_only.md)
    "Reload: root*@1.1", "Fire Barrage: root*@5.3", "Bombardment: root*@8.2", "Synchro Mole: root*@10"],
```

### 2. `wardrobe/index.html` SEQ_SKILL (index.html:3319-3325): add a mole entry (merge with any other mole ids)

```js
  mole: { "@Reload": "reload", "@FireBarrage": "fireBarrage", "@Bombardment": "bombardment", "@SynchroMole": "synchroMole" },
```
(e.g. after the `cat: {...},` line; the chain ids are the names without spaces, as `@BerserkerRush`.)

### 3. `wardrobe/fx_cues/mole.json`: four entries (the file is `{}` today; the same text, checked with json.load, is
`checks/fx_mole_research/effect_only/cues.json`)

```json
  "@Reload:root": {
    "why": "Mole.cs RPC_reload (:10168-10465), a plain method doSkill calls straight (mol_reload1 / 2 :6472-6484, call :8942, ActionEvent :8951; doSkill :6338-8972 calls no PlayAnimation / animation.Play / CrossFade), so the Mole goes on with what she was doing; the tile plays it on the idle stance. At max rank (Reload 2) it clears the listed cooldowns (:10170-10307: 13 at rank 1, 9 more at rank 2, 8 more with Advance Repair #431), adds ceil(0.5 x 2 x msp) SP (:10313) and arms agiAdjust(240) (:10316); Effects/reload (:10325) createEffect at the hero's position and rotation (:10337; EffectControl life 1, followPosition, no followState), voice reload1 / reload2 (Random.Range(0, 2) :10380; reload1 :10390 -> break -> PlayOneShot :10460, reload2 :10421 -> Block_63 PlayOneShot :10465; both predicates worked by hand, plans/fx_mole/effect_only.md)",
    "cues": [
    [0, "fx", "reload"],
    [0, "voice", "reload1|reload2"]
    ]
  },
  "@FireBarrage:root": {
    "why": "Mole.cs RPC_fireBarrage (:11403 -> $RPC_fireBarrage$23666 :28462-28855), started straight from doSkill (:8636, ActionEvent :8649; no clip anywhere on the way) at max rank (mol_fireBarrage2 num++ :6683); the aim mPos = getSpawnPos(target - the unit Mole->target direction vector2) (:8539; vector2 :6399-6402), so 1 m in front of the 10 m target point = 9 m ahead (no target: the cursor's ground point :8571, or 12 m ahead :8596), tDir = vector2 = the hero's facing. At 0: voice fireBarrage1 / fireBarrage2 (Random.Range(0, 2) :28679; :28691 / :28722, PlayOneShot :28703 / :28734; the 3 s voice timer is clear on a first press, :28644), fireBarrage_signal at mPos with the hero's rotation (:28787-28797; shown to the caster's own team, :28757-28763; EffectControl life 3, its AudioSource signal). Yield 2 s (:28819), then RPC_fireBarrage_fire (:28612 -> $RPC_fireBarrage_fire$23676 :28859-29290): at 2.0 the aircraft fireBarrage_<colour> picked by the hero's colour Skin / 100 (1 r, 2 g, 3 b, 4 k, 5 w, else r: :29096-29163; the outfit colour C.state.color) at mPos, LookRotation(tDir) (:29176), and at rank 2 two more (:29181-29204): tDir1 = rotateH(tDir, 30) (30 deg left, Unity yaw -30) at mPos - rotateNormal((-3, 0, -3), tDir1) = 1.098 m right, 13.098 m ahead, and tDir2 = rotateH(tDir, -30) (yaw +30) at 1.098 m left, 13.098 m ahead (Math.cs:838-880 worked through); EffectControl life 3, each with its looped plane sound. Yield 1.3 s (:29280): at 3.3 fireBarrage_hit2 (sLv 2; hit1 is rank 1's, :29000-29047) at mPos with the hero's rotation (EffectControl life 1 + afterLife 1, its AudioSource fireBarrage); the four 0.1 s damage waves after it draw nothing (:29227-29285)",
    "cues": [
    [0, "voice", "fireBarrage1|fireBarrage2"],
    [0, "fx", "fireBarrage_signal", 9],
    [2, "fx", "fireBarrage_r|fireBarrage_g|fireBarrage_b|fireBarrage_k|fireBarrage_w", {"d": 9, "pick": "color"}],
    [2, "fx", "fireBarrage_r|fireBarrage_g|fireBarrage_b|fireBarrage_k|fireBarrage_w", {"d": 13.098, "x": 1.098, "rot": [0, -30, 0], "pick": "color"}],
    [2, "fx", "fireBarrage_r|fireBarrage_g|fireBarrage_b|fireBarrage_k|fireBarrage_w", {"d": 13.098, "x": -1.098, "rot": [0, 30, 0], "pick": "color"}],
    [3.3, "fx", "fireBarrage_hit2", 9]
    ]
  },
  "@Bombardment:root": {
    "why": "Mole.cs RPC_bombardment (:11417 -> $RPC_bombardment$23693 :29343-29733), started straight from doSkill (:8420, ActionEvent :8433; no clip) at max rank (mol_bombardment2 num++ :6704); the aim mPos = 1 m in front of the 10 m target point = 9 m ahead (:8373; no target :8450 / :8480, as Fire Barrage), tDir = the hero's facing. At 0: voice bombardment1 / bombardment2 (Random.Range(0, 2) :29560; :29572 / :29603, PlayOneShot :29584 / :29615), bombardment_signal at mPos, Quaternion.identity (:29668-29678; own team only, :29638-29644; EffectControl life 5, its AudioSource signal). Yield 4 s (:29700), then RPC_bombardment_fire (:29493 -> :29738-30078): at 4.0 the bomber bombardment_<colour> by Skin / 100 (1 r, 2 g, 3 b, 4 k, 5 w, else r: :29961-30028) at mPos, LookRotation(tDir) (:30039), and at rank 2 two more at mPos + rotateNormal((-3, 0, -3)) / ((3, 0, -3), tDir) = 3 m left / right, 3 m nearer (:30048, :30051); EffectControl life 3. Yield 1.2 s (:30071): five strikes 0.1 s apart (Yield 0.1 :30073), strike k (0-4) at 5.2 + 0.1 k s at getSpawnPos(mPos + tDir x (3 k - 6)) = 3, 6, 9, 12, 15 m ahead (:29912, RPC_bombardment_hit :29929 -> :30119-30451); each: bombardment_fire (the falling bomb, EffectControl life 2, sound bombardment) at the strike, LookRotation(tDir) (:30418-30428), Yield 0.2 (:30447), at rank 2 two more 3 m left / right, 3 m nearer (:30256, :30261), Yield 0.4 (:30449), then bombardment_hit at the strike and at rank 2 at the two sides (:30286, :30297, :30302; EffectControl life 1 + afterLife 1) and the damage (:30317-30394): 3 bombers, 15 bombs, 15 blasts, the last at 6.2 s",
    "cues": [
    [0, "voice", "bombardment1|bombardment2"],
    [0, "fx", "bombardment_signal", 9],
    [4, "fx", "bombardment_r|bombardment_g|bombardment_b|bombardment_k|bombardment_w", {"d": 9, "pick": "color"}],
    [4, "fx", "bombardment_r|bombardment_g|bombardment_b|bombardment_k|bombardment_w", {"d": 6, "x": -3, "pick": "color"}],
    [4, "fx", "bombardment_r|bombardment_g|bombardment_b|bombardment_k|bombardment_w", {"d": 6, "x": 3, "pick": "color"}],
    [5.2, "fx", "bombardment_fire", 3],
    [5.3, "fx", "bombardment_fire", 6],
    [5.4, "fx", "bombardment_fire", {"d": 0, "x": -3}],
    [5.4, "fx", "bombardment_fire", {"d": 0, "x": 3}],
    [5.4, "fx", "bombardment_fire", 9],
    [5.5, "fx", "bombardment_fire", {"d": 3, "x": -3}],
    [5.5, "fx", "bombardment_fire", {"d": 3, "x": 3}],
    [5.5, "fx", "bombardment_fire", 12],
    [5.6, "fx", "bombardment_fire", {"d": 6, "x": -3}],
    [5.6, "fx", "bombardment_fire", {"d": 6, "x": 3}],
    [5.6, "fx", "bombardment_fire", 15],
    [5.7, "fx", "bombardment_fire", {"d": 9, "x": -3}],
    [5.7, "fx", "bombardment_fire", {"d": 9, "x": 3}],
    [5.8, "fx", "bombardment_hit", 3],
    [5.8, "fx", "bombardment_hit", {"d": 0, "x": -3}],
    [5.8, "fx", "bombardment_hit", {"d": 0, "x": 3}],
    [5.8, "fx", "bombardment_fire", {"d": 12, "x": -3}],
    [5.8, "fx", "bombardment_fire", {"d": 12, "x": 3}],
    [5.9, "fx", "bombardment_hit", 6],
    [5.9, "fx", "bombardment_hit", {"d": 3, "x": -3}],
    [5.9, "fx", "bombardment_hit", {"d": 3, "x": 3}],
    [6.0, "fx", "bombardment_hit", 9],
    [6.0, "fx", "bombardment_hit", {"d": 6, "x": -3}],
    [6.0, "fx", "bombardment_hit", {"d": 6, "x": 3}],
    [6.1, "fx", "bombardment_hit", 12],
    [6.1, "fx", "bombardment_hit", {"d": 9, "x": -3}],
    [6.1, "fx", "bombardment_hit", {"d": 9, "x": 3}],
    [6.2, "fx", "bombardment_hit", 15],
    [6.2, "fx", "bombardment_hit", {"d": 12, "x": -3}],
    [6.2, "fx", "bombardment_hit", {"d": 12, "x": 3}]
    ]
  },
  "@SynchroMole:root": {
    "why": "Mole.cs RPC_synchroMole (:13220-13510), a plain method doSkill calls straight (mol_synchroMole1 / 2 :6982-6994, call :7920, ActionEvent :7933; no clip) at max rank: agiAdjust(300) (:13228), the synchroMole status Lv 2 on the Mole for chaAdjust(30) = 30 s (:13237-13242; cut at 10 s, the long-buff rule) and for 31 s on each own Auto Gyro Gun / Barrel Bot present (:13247-13370; none in this tile), voice synchroMole1 / synchroMole2 (Random.Range(0, 2) :13437; :13447 -> Block_47 PlayOneShot :13506, :13478 -> IL_549 PlayOneShot :13509). The status's apply on a Mole (CharacterControl.cs:37714-37748, Type == \"Mole\"): Effects/synchroMole_ring Instantiated at the hero's position, Quaternion.identity, parented to the hero (synchroMoleRingFx; no EffectControl: its ImageEmitter repeats until the status's removal destroys it, CharacterControl.cs:16989-16998: kill 10; its AudioSource synchroMole plays on awake); the green tint and the synchroMole look over the head are the summons' (the else branch :37760-37806), not the Mole's; RPC_synchroMole0 (:13514) at the end only strips the summons' status",
    "cues": [
    [0, "fx", "synchroMole_ring", {"kill": 10}],
    [0, "voice", "synchroMole1|synchroMole2"]
    ]
  }
```
(The comma after the last `}` only if another entry follows. `pick` is not in `wardrobe_fx_check.py`'s OPTS yet: the
check fails on these two entries until P1 is built; `d`, `x`, `rot`, `kill` are there.) Check with
`py -3 -c "import json; json.load(open('wardrobe/fx_cues/mole.json', encoding='utf-8'))"`.

### 4. `pipeline/wardrobe_skill_icons.py` EFFECT_ONLY (:46-50): add the mole list

```python
               "cat": ["awareness", "damageRoulette", "treasureHunt"],
               # the Mole's Reload, Fire Barrage, Bombardment and Synchro Mole (2026-11-13, plans/fx_mole/effect_only.md)
               "mole": ["reload", "fireBarrage", "bombardment", "synchroMole"]}
```
The Bible has `mole_reload2`, `mole_fireBarrage2`, `mole_bombardment2`, `mole_synchroMole2` (assets.js; the cards'
`icon`, index.html:17769, :17817, :17818, :17848), so `best` finds the top ranks. Then `py -3 pipeline\wardrobe_skill_icons.py`
adds them to `data/icons/hd/index.json` with clips ["root"] and writes `icons/hd/mole/<skill>.webp`.

### 5. P1 (the page part), then build and check

```js
// wardrobe/index.html cueOf (:4555): a name list picked by the hero's colour (2026-11-13, plans/fx_mole/effect_only.md
// P1: the Mole's Fire Barrage / Bombardment planes, Math.div(mChar.Skin, 100) = C.state.color: 1 _r, 2 _g, 3 _b, 4 _k,
// 5 _w, else the first, Mole.cs:29096-29163, :29961-30028)
  const q = { ...o, at: c[0], kind: c[1], name: o.pick === "color" ? (ns[(C?.state?.color ?? 1) - 1] ?? ns[0]) : ns[Math.floor(Math.random() * ns.length)], ...
```
```python
# pipeline/wardrobe_fx_check.py OPTS (:163): add "pick"
```
```
uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py mole --fx reload,fireBarrage_signal,fireBarrage_r,fireBarrage_g,fireBarrage_b,fireBarrage_k,fireBarrage_w,fireBarrage_hit2,bombardment_signal,bombardment_r,bombardment_g,bombardment_b,bombardment_k,bombardment_w,bombardment_fire,bombardment_hit,synchroMole_ring --voices reload1,reload2,fireBarrage1,fireBarrage2,bombardment1,bombardment2,synchroMole1,synchroMole2
py -3 pipeline\wardrobe_skill_icons.py
uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py D:/12tails-wardrobe checks/fx_mole dark --cls mole
```
A plain `wardrobe_fx.py mole` picks them up from the cue file once every Mole cue is in.

## Open questions (each with my recommended answer)
1. **Where Fire Barrage and Bombardment land.** The game aims 1 m in front of the target (:8539, :8373). *Recommend
   d 9* (the target at the 10 m point, the aim 1 m nearer). Alternatives: d 10 (the rule read loosely), or 12 m (the
   game's no-target, low-cursor branch :8596 / :8480).
2. **The colour pick.** *Recommend building P1* (`"pick": "color"`, the page's current outfit colour), so the planes
   match the hero as in the game. Not a random pick: the game never picks at random. The game's cache (the first colour
   sticks until a relog) is left out. Fallback if P1 is refused: `_r` only.
3. **Fire Barrage's side aircraft** start beyond the target (BB subtracts the offset, :29199 / :29204, where Bombardment
   adds it, :30048). *Recommend keeping the game's spots* (x +-1.098, d 13.098, yaw -+30); a "fix" to mirror
   Bombardment would be our invention. Worth a look in the QA shots: their animation may carry them well off the
   camera.
4. **Bombardment's size:** 35 cues, 3 bombers, 15 bombs, 15 blasts reaching 15 m ahead. *Recommend all of them* (max
   rank, the skill's whole look), cost flagged for QA as the Bison's Magma Quake.
5. **War Capital's periodic fire** (RPC_warCapital_fire / warMissile_fire / warMissile_hit, started by the base every 24
   s, :43892) has no Mole clip but belongs to War Capital, whose cast is the assemble clip. *Recommend the assemble
   researcher decide it* (likely the base's first volley inside the Assemble / War Capital tile); not a tile here.
6. **Synchro Mole on summons:** the green tint and the `synchroMole` look over the head go on the Mole's turrets and bots
   only. *Recommend leaving them out* (no summons in this tile), unless the assemble tiles spawn the summons: then the
   look could ride them.
7. **Smart Shell** (#264) draws `smartShell_hit` only when an enemy sets off a mine. *Recommend no tile and no cue* (no
   enemy, and it belongs to the mines' tiles if anywhere).
8. **Bible offers (not written there):** Fire Barrage's three aircraft / Bombardment's three bombers at rank 2 and their
   spots; the planes coloured by the hero's colour (Skin / 100); Bombardment's 15 bombs and 15 blasts (5 strikes x 3 at
   rank 2, the side ones 0.2 s later); Fire Barrage's one impact effect at 3.3 s for the four damage waves; Synchro Mole's
   ring on the Mole vs. the summons' green tint and head look; BB's missing `Effects/bombardment` load (:29956,
   harmless); `fireBarrage_signal` / `bombardment_signal` shown only to the caster's own team.

## Verification

Read-only check, 2026-11-13 (home PC), against `D:\12tails\DecompiledSource\Mole.cs`, `CharacterControl.cs`, `Math.cs`,
`MoleEquipment.cs`, `Mole_mine.cs` / `Mole_stunMine.cs`, the TTO `methods.tsv` / `pseudo/Mole.c`, the Bible's cards and
`mole-skill-reference.md`, the BB rip's wav files and this report's `probe_summary.txt`. Helpers (git-ignored):
`checks/fx_mole_research/verify_eo_b/` (`rpc.txt` the RPC listing redone, `tto_rpc.txt`, `clip_calls.txt`, `pred.py`: every
junk predicate in a line range evaluated T/F).

**Verdict: the four tiles, every time, position, rank, random pick and the paste-ready blocks 1-5 are right; no cue changes.**

Checked and confirmed:
- **RPC listing redone:** `grep -nE "^\s*(public|private|protected|internal)[^(]*\bRPC_\w+\(" Mole.cs` = 102, every line
  number in the Accounting as cited; groups 30 + 4 + 4 + 40 + 24 recounted by name = 102. `clip_calls.js` (run as
  `node pipeline/clip_calls.js D:/12tails/DecompiledSource wardrobe/data mole`) lists exactly the 30 clip RPCs; none of
  RPC_reload / fireBarrage(_fire) / bombardment(_fire, _hit) / synchroMole plays a clip; doSkill (:6338-8972) holds 0
  PlayAnimation / CrossFade / .Play calls. TTO: 88 Mole RPCs; TTO-only = barrelRailgun (+_fire, _overload, _end),
  flameTurret_end, missileBot_fire, missile_lock, twinImpact, warArea, warArea_strike (War Area starts through
  WarAreaBegin(command, tDir, clip, 0.2 fade), pseudo/Mole.c:2840 / :41176): nothing TTO-only is effect-only, as stated.
- **Calls:** :8942 / :8951 (reload), :8636 / :8649 (fireBarrage), :8420 / :8433 (bombardment), :7920 / :7933 (synchroMole),
  aim :8539 / :8373 `getSpawnPos(target - vector2)`, vector2 = flat normalized (:6399-6402), no-target :8571 / :8596,
  :8450 / :8480 (12 m): all as cited.
- **Reload:** loads :10325 / createEffect :10337 (predicates false as worked), voices :10380 / :10390 / :10421, PlayOneShot
  :10460 / :10465; cooldown lists recounted 13 / 9 (sLv > 1) / 8 (hasSkill(431)).
- **Fire Barrage:** every predicate on the path evaluated (pred.py 28585-28830, 28859-29290): voice 0, signal at mPos with
  transform.rotation (:28797, inside the true `22501 - 162204 == -139703`), Yield 2 (:28819), case 2 starts _fire (:28612);
  colour switch :29096-29163; centre plane LookRotation(tDir) :29176; rank 2 side planes :29199 / :29204 (`249128 - 463222
  != -214094` false, so no skip); Yield 1.3 (:29280); hit2 at mPos, hero rotation (:29035-29047). Geometry redone from
  Math.cs:838-880 (rotateNormal = rotateH(v, atan2(n.z, n.x) - 90) = LookRotation(n) * v; rotateH(+a) turns left):
  tDir1 = (-0.5, 0.866), mPos - rotateNormal((-3,0,-3), tDir1) = mPos + (1.098, 4.098); tDir2 mirrored: **x +-1.098,
  d 13.098, rot [0, -30, 0] / [0, 30, 0]** are right. The page's `x` is Unity's +x = the hero's right (index.html fx
  placement `V(-(at.x), at.y, at.d)` after the Unity->three mirror, about :4955), so the signs hold.
- **Bombardment:** voice :29560-29615, signal identity :29678 (inside the true `239229 - 883 == 238346`), Yield 4
  (:29700); _fire: untyped `Effects/bombardment` :29956 then the colour switch :29961-30028, bombers :30039 / :30048 /
  :30051 (x -+3, d 6), Yield 1.2 (:30071), loop `i >= 5` exit, `getSpawnPos(mPos + tDir x (3i - 6))` (:29912), 0.1 s
  (:30073); _hit: centre bomb :30428 (Yield 0.2 :30447), side bombs :30256 / :30261 (predicates :30250 `117441 - 498586
  != -381145` and the next `== -97259` both false), then Block_8 -> Yield 0.4 (:30449), hits :30286 / :30297 / :30302.
  All 35 cue times / spots re-derived: identical to block 3.
- **Synchro Mole:** :13228, AddStatus :13242 (with ActorNr), voices :13437 / :13447 / :13478, PlayOneShot :13506 /
  :13509 (owner: isMine passes the game-type / team gates :13412-13430); CharacterControl.cs:37714-37748 Type "Mole" ->
  ring at mTransform.position, identity, parented, named synchroMoleRingFx; removal :16978-17028. CharacterControl.cs
  loads only these two Mole effects (:37724, :37782).
- **Durations** (BB rip wavs measured): voices reload1 0.758 / reload2 1.087, fireBarrage1 0.781 / 2 1.242,
  bombardment1 1.314 / 2 1.535, synchroMole1 1.106 / 2 1.359; sounds signal 2.306, plane 0.891, fireBarrage 1.306,
  bombardment 1.999, synchroMole 1.4: all as stated. Step lengths 1.1 / 5.3 / 8.2 / 10 follow from the prefab lives.
- **Colour (P1):** Skin 100-599 (MoleEquipment.cs:282-294), getArmorMaterial `nSkin % 100` overlay / `Math.div(nSkin,
  100)` colour (:1486-1504); every Mole outfit in `wardrobe/data/mole/outfits.json` has colors [1..5] except steamSuit
  ([]), which the fallback `ns[0]` (= `_r`, the game's else) covers. The P1 expression is correct; `pick` does not collide
  with the pool pick (`FX.pick` / `chain.pick` are other objects).
- **Formats:** the block-3 JSON parses and equals `checks/.../effect_only/cues.json`; keys `@Reload:root` etc. match the
  SEQ names through split_key (spaces dropped, wardrobe_fx_check.py:96-101); SEQ tokens `root*@t` as the Cat's; Bible icons
  `mole_reload2` / `mole_fireBarrage2` / `mole_bombardment2` / `mole_synchroMole2` exist (assets.js; cards index.html:17769,
  :17817, :17818, :17848).

Corrections (none changes a cue):
1. **Line numbers in the wardrobe files have moved** (index.html is being edited by other sessions): the mole SEQ line is
   now index.html:1249-1250 (not :1232-1233), SEQ_SKILL from :3337 (not :3319-3325), cueOf from :4629 at this check, its `name:` expression two lines
   down (not :4553-4562 / :4555; it keeps moving), the colour state setOutfit / setColorOrFace :805-850; fx_check OPTS
   :171-174 (not :163-164), expected()'s `|` skip :151 (not :150), wardrobe_fx.py cue_names :622 (not :570);
   wardrobe_skill_icons.py EFFECT_ONLY :49-53 (not :46-50). Anchor the pastes by their text, not the numbers.
2. **Accounting wording:** RPC_barrelCannon (:13949) plays its own `barrelCannon` clip (Mole.cs:40208; Bible card "Barrel
   Bot - Barrel Cannon"); it is not one of "the five War Factory units", which are sawMachine, bazooka, teslaCoil,
   rollerMachine, cartBomb (`warFactory`, :40826-43406). The count 30 is unchanged.
3. **"The Bible's 28 BB actives"** holds once the two mount items are left out: the Bible also has active cards Mole's Tank
   and Giga Cannon (`mount: true`, index.html:17853-17856; they go through useMount) and Mount - Attack / Dash; and the
   five `ver: "reborn"` actives (Air Strike, ICBM, Giga Drill, Iron Overdrive, Total War) are the Reborn client's, neither
   BB nor TTO (no Mole.cs / TTO RPC): out of scope, worth one line in the report.
4. Fire Barrage / Bombardment voices: the gate is "owner, or (game type > 4 and same team)" (:28650-28676,
   :29531-29557), not only "the owner"; for the wardrobe's own hero the voice plays, as written.

Corrected paste-ready blocks: **none needed**; blocks 1-5 stand as written (only the cited insertion line numbers move,
correction 1).
