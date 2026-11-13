# Effect parts each class needs

Written by `pipeline/wardrobe_fx_inventory.py` (do not edit by hand; run it again). Effects = the prefabs in a
class's own Effects folder (`heroes/<cls>/effects`) that its `<Class>.cs` loads: skills, hits, buffs, projectiles,
not only skills. Physics parts (colliders, Rigidbody) are left out: they draw nothing.
Ready = every part is one the page builds today (AlphaTimer, Animation, AudioControl, AudioSource, AutoGyroGun, BarrelBot, BarrelBotAI, BatSwarmFlap, Bat_echoes, Bat_guardianOfTheNight, Bat_illusion, Bat_illusionFire, Bat_mirageOrb, Bat_nAttack, Bison_c6Arc, Bison_earthRupture, Bison_overLord, Bison_row6Fx, BoltEmitter, Buiten, Cat_grandCasinoArcade, Cat_supportFire, Chameleon_campFire, Chameleon_nAttack, Chameleon_needlePrison, CharacterControl, EffectControl, EffectControl(child), EllipsoidParticleEmitter, EmblemEmitter, EmitterControl, Gadina, Gadina_AI, Gaos, Gaos_AI, GroundConformParticles, ImageEmitter, Ja, Ja_AI, KingKaiser, KingKaiserAI, Light, LineEmitter, ManaVortex, Mole_bazooka, Mole_cartBomb, Mole_flameCarnival, Mole_grenadeCluster, Mole_mine, Mole_missile, Mole_mortarShot, Mole_nAttack, Mole_napalm, Mole_stunGrenade, Mole_stunMine, Mole_timeNuke, Mole_warCapital, Mole_warMissile, Monkey_earthPulse, Monkey_fireBall, Monkey_lavu, Monkey_runicFlame, Monkey_runicSand, ParticleAnimator, ParticleRenderer, Penguin_arcticEmperor, Penguin_cosmicFriday, Penguin_iceBlock, Penguin_manaMissile, Penguin_nAttack, Penguin_snowMan, Penguin_tornado, Penguin_typhoon, Phoenix, Phoenix_AI, Phoenix_fireBall, Phoenix_skyCrimson_fire, ProjectileControl, RingEmitter, Rotate, ShatterMesh, Sheep_cAttack, Sheep_edenSanctuary, Sheep_homingLight, Sheep_nAttack, Sheep_seal, SkinnedMeshRenderer, StaticMesh, StatusControl, TrailEmitter, TrailRenderer, UVScroll, VortexEmitter, WorldParticleCollider, rotationControl) and `wardrobe_fx.py`
extracts it (checked in memory). Each class's code also loads its pet's and other classes' effects (shown on it,
like a Sheep's heal): counted apart, never this class's skills.

## Per class

| class | own effects | ready | not ready | parts missing (own effects needing it) | others' loaded |
|---|---|---|---|---|---|
| bat | 26 | 26 | 0 |  | 29 |
| bison | 46 | 45 | 1 | ParticleSystemRenderer 1, ParticleSystem 1 | 28 |
| cat | 67 | 66 | 1 | ParticleSystemRenderer 1, ParticleSystem 1 | 28 |
| chameleon | 57 | 55 | 2 | ParticleSystemRenderer 2, ParticleSystem 2 | 28 |
| mole | 78 | 75 | 3 | ParticleSystemRenderer 3, ParticleSystem 3 | 28 |
| monkey | 51 | 50 | 1 | ParticleSystemRenderer 1, ParticleSystem 1 | 28 |
| panda | 71 | 70 | 1 | ParticleSystemRenderer 1, ParticleSystem 1 | 28 |
| penguin | 48 | 48 | 0 |  | 28 |
| rabbit | 84 | 66 | 18 | Rabbit_potion 13, Rabbit_acidicField 1, ParticleSystemRenderer 1, ParticleSystem 1, Rabbit_healingField 1, Rabbit_sniperCamera 1, Rabbit_stickyGum 1 | 24 |
| sheep | 51 | 51 | 0 |  | 27 |
| whale | 51 | 45 | 6 | whale_kingdomKnight 2, Whale_flyingShield 1, ParticleSystemRenderer 1, ParticleSystem 1, Whale_homingShield 1, Whale_javelin 1 | 28 |
| wolf | 69 | 69 | 0 |  | 28 |

## Per missing part

Own effects that need the part (all classes), and how many of those it alone blocks
(every other part of theirs is built).

| part | effects | blocks alone | classes |
|---|---|---|---|
| Rabbit_potion | 13 | 13 | rabbit |
| whale_kingdomKnight | 2 | 2 | whale |
| Whale_javelin | 1 | 1 | whale |
| Whale_homingShield | 1 | 1 | whale |
| Whale_flyingShield | 1 | 1 | whale |
| Rabbit_stickyGum | 1 | 1 | rabbit |
| Rabbit_sniperCamera | 1 | 1 | rabbit |
| Rabbit_healingField | 1 | 1 | rabbit |
| Rabbit_acidicField | 1 | 1 | rabbit |
| ParticleSystemRenderer | 11 | 0 | bison, cat, chameleon, mole, monkey, panda, rabbit, whale |
| ParticleSystem | 11 | 0 | bison, cat, chameleon, mole, monkey, panda, rabbit, whale |

## Build order (greedy)

Each step: the part that makes the most own effects ready, given the ones above it
(when none alone does, the part most not-ready effects need). Ready after = all classes.

| step | part | newly ready | ready after |
|---|---|---|---|
| 0 | (built today) | 666 | 666 / 699 |
| 1 | Rabbit_potion | 13 | 679 / 699 |
| 2 | whale_kingdomKnight | 2 | 681 / 699 |
| 3 | Whale_javelin | 1 | 682 / 699 |
| 4 | Whale_homingShield | 1 | 683 / 699 |
| 5 | Whale_flyingShield | 1 | 684 / 699 |
| 6 | Rabbit_stickyGum | 1 | 685 / 699 |
| 7 | Rabbit_sniperCamera | 1 | 686 / 699 |
| 8 | Rabbit_healingField | 1 | 687 / 699 |
| 9 | Rabbit_acidicField | 1 | 688 / 699 |
| 10 | ParticleSystemRenderer | 0 | 688 / 699 |
| 11 | ParticleSystem | 11 | 699 / 699 |

## Per effect

### bat

- `bigCast_ring` (Bat.cs:30026): ready
- `blackServant_ring` (Bat.cs:44917): ready
- `bloodCarnage_ring` (Bat.cs:16065): ready
- `charm_hit` (Bat.cs:13666): ready
- `deadEffect` (Bat.cs:53740): ready
- `demonGaze_hit` (Bat.cs:11542): ready
- `dreamBurst_hit` (Bat.cs:13989): ready
- `dreamDazzle_hit` (Bat.cs:35102): ready
- `echoes` (Bat.cs:11825): ready
- `echoes_hit` (Bat.cs:11928): ready
- `echoes_ring` (Bat.cs:27967): ready
- `guardian` (Bat.cs:30549): ready
- `massCast` (Bat.cs:11140): ready
- `mindControl_ring` (Bat.cs:13738): ready
- `mirageOrb` (Bat.cs:12669): ready
- `nefariousWhip_hit` (Bat.cs:44025): ready
- `nightmare_ring` (Bat.cs:11996): ready
- `paranoia_hit` (Bat.cs:14599): ready
- `phantasmBlast_hit` (Bat.cs:36059): ready
- `shadowGaze_hit` (Bat.cs:11582): ready
- `shadowSacrifice_ring` (Bat.cs:14301): ready
- `shatteringDream_hit` (Bat.cs:42548): ready
- `soulEater_hit` (Bat.cs:14413): ready
- `soulEater_ring` (Bat.cs:40715): ready
- `swap_hit` (Bat.cs:13562): ready
- `switch_hit` (Bat.cs:13368): ready

### bison

Status looks `CharacterControl.cs` loads for the Bison (not in `Bison.cs`, so not scanned above; every one ready): holdCharge_ring + holdCharge (:34670, :34673), berserkerRush_ring + berserkerRush (:34876, :34888), furyTrance1-3 (:34963), overPower_horn1-2 (:35010, on Head with localRotation Euler(-90, 0, 0): the cue's bone + rot) + overPower_ring (:35028), ironShield (:35064), diamondShield (:35095), perfectShield (:35129), perfectArmor (:35164; its Velvet shader not built: unreachable, no BB or TTO code adds the perfectShield / perfectArmor status), titanForm (:35243); the hero prefab's nAttack_hit / cAttack_hit and overLord (plans/fx_bison/parts.md "Read this first" 2).

- `afterShock` (Bison.cs:22984): ready
- `aspect_slam` (Bison.cs:21449): ready
- `aspect_trample` (Bison.cs:22536): ready
- `calamityHammer_fire` (Bison.cs:32785): ready
- `calamityHammer_ring` (Bison.cs:32350): ready
- `cAttack1_dust` (Bison.cs:19320): ready
- `cAttack2_dust` (Bison.cs:20379): ready
- `deadEffect` (Bison.cs:41201): ready
- `diamondShield_ring` (Bison.cs:28196): ready
- `earthRupture` (Bison.cs:8775): ready
- `earthRupture_ring` (Bison.cs:28854): ready
- `earthSmasher` (Bison.cs:29132): ready
- `earthSmasher_ring` (Bison.cs:29505): ready
- `enrage_ring` (Bison.cs:20911): ready
- `farStun` (Bison.cs:7646): ready
- `farStun_ring` (Bison.cs:23695): ready
- `holdCharge_fire` (Bison.cs:20280): ready
- `instantRush_dust` (Bison.cs:24514): ready
- `instantRush_ring` (Bison.cs:24482): ready
- `ironShield_ring` (Bison.cs:27609): ready
- `knockDown` (Bison.cs:23019): ready
- `knockDown_hit` (Bison.cs:7511): ready
- `knockDown_ring` (Bison.cs:23393): ready
- `magmaClutter_ring1` (Bison.cs:31839): ready
- `magmaClutter_ring2` (Bison.cs:31506): needs ParticleSystem, ParticleSystemRenderer (its ParticleSystem / ParticleSystemRenderer (Unity 3.5 Shuriken, not decoded from BB) are grafted from TTO's copy by `wardrobe_fx.py` (SHURIKEN_FROM_TTO, BB's Bomb2 material): drawn)
- `massStun` (Bison.cs:9096): ready
- `onslaught_ring` (Bison.cs:30325): ready
- `overPower` (Bison.cs:24985): ready
- `overSwing_ring` (Bison.cs:25579): ready
- `powerCleave` (Bison.cs:26129): ready
- `powerCleave_hit` (Bison.cs:8162): ready
- `powerCleave_ring` (Bison.cs:26465): ready
- `powerHammer` (Bison.cs:26179): ready
- `powerHammer_hit` (Bison.cs:8254): ready
- `powerReel_ring` (Bison.cs:26513): ready
- `prideCrusher_ring` (Bison.cs:31147): ready
- `slam_dust` (Bison.cs:21411): ready
- `slam_ring` (Bison.cs:21794): ready
- `solidCharge_ring` (Bison.cs:19358): ready
- `spinHack_ring` (Bison.cs:20417): ready
- `stunningGround_ring` (Bison.cs:9378): ready
- `titanForm_ring` (Bison.cs:30006): ready
- `trample1` (Bison.cs:22057): ready
- `trample2` (Bison.cs:22096): ready
- `trample_dust` (Bison.cs:22648): ready
- `warcry_ring` (Bison.cs:26868): ready

### cat

- `assassinate_hit` (Cat.cs:41949): ready
- `awareness1` (Cat.cs:8591): ready
- `awareness2` (Cat.cs:8630): ready
- `backStab_hit` (Cat.cs:10353): ready
- `bleed_fire` (Cat.cs:34887): ready
- `bleed_hit` (Cat.cs:10282): ready
- `bleed_ring` (Cat.cs:35207): ready
- `copycat_hit` (Cat.cs:9541): ready
- `copycat_ring` (Cat.cs:26750): ready
- `damagePlus` (Cat.cs:19749): ready
- `damagePlus_ring` (Cat.cs:19987): ready
- `damageRoulette_ring` (Cat.cs:27080): ready
- `deltaStrike` (Cat.cs:37470): ready
- `deltaStrike_cat` (Cat.cs:37305): ready
- `deltaStrike_ring` (Cat.cs:37105): ready
- `disarm` (Cat.cs:34055): ready
- `disarm_hit` (Cat.cs:10232): ready
- `disarm_ring` (Cat.cs:34375): ready
- `doubleDown1_hit` (Cat.cs:25441): ready
- `doubleDown2_hit` (Cat.cs:25405): ready
- `doubleDown_ring` (Cat.cs:24711): ready
- `evenOdds_hit` (Cat.cs:9351): ready
- `fateDraw_ring` (Cat.cs:21714): ready
- `finishingBlow_hit` (Cat.cs:38739): ready
- `finishingBlow_ring1` (Cat.cs:38445): ready
- `finishingBlow_ring2` (Cat.cs:39223): ready
- `flyingDagger_fire` (Cat.cs:29156): ready
- `flyingDagger_hit` (Cat.cs:9838): ready
- `forwardLunge_hit` (Cat.cs:9888): ready
- `grandCasinoArcade` (Cat.cs:27826): ready
- `grandCasinoArcade_hit1` (Cat.cs:9669): ready
- `grandCasinoArcade_hit2` (Cat.cs:9706): ready
- `grandCasinoArcade_hit3` (Cat.cs:9743): ready
- `grandCasinoArcade_hit7` (Cat.cs:9784): ready
- `grandCasinoArcade_ring1` (Cat.cs:28645): ready
- `grandCasinoArcade_ring2` (Cat.cs:28406): ready
- `hiddenBlade_hit` (Cat.cs:10072): ready
- `ladyLuck_ring` (Cat.cs:21585): ready
- `lifeGamble_heal` (Cat.cs:9169): ready
- `lifeGamble_hit` (Cat.cs:9212): ready
- `lifeGamble_ring` (Cat.cs:22967): ready
- `luckyCard_fire` (Cat.cs:20626): ready
- `luckyDice` (Cat.cs:23872): ready
- `moonBlade` (Cat.cs:35984): ready
- `moonStorm` (Cat.cs:36726): ready
- `nAttack_dust` (Cat.cs:16320): ready
- `nAttack_hit` (Cat.cs:8266): ready
- `pillagePlunge_hit` (Cat.cs:10510): ready
- `pillagePlunge_ring1` (Cat.cs:40471): ready
- `pillagePlunge_ring2` (Cat.cs:40110): ready
- `pillagePlunge_ring3` (Cat.cs:40289): ready
- `powerShuffle_ring` (Cat.cs:22424): ready
- `reverseThrust` (Cat.cs:31169): ready
- `reverseThrust_hit` (Cat.cs:9938): ready
- `skillGamble_heal` (Cat.cs:9262): ready
- `skillGamble_hit` (Cat.cs:9305): ready
- `skillGamble_ring` (Cat.cs:23499): ready
- `supportFire_cannon` (Cat.cs:41072): ready
- `supportFire_fire` (Cat.cs:10731): ready
- `supportFire_hit` (Cat.cs:10790): needs ParticleSystem, ParticleSystemRenderer (its ParticleSystem / ParticleSystemRenderer (Unity 3.5 Shuriken, not decoded from BB) are grafted from TTO's copy by `wardrobe_fx.py` (SHURIKEN_FROM_TTO, BB's Bomb2 material): drawn)
- `supportFire_ring` (Cat.cs:40920): ready
- `supportFire_smoke` (Cat.cs:10699): ready
- `swiftPace_ring1` (Cat.cs:39733): ready
- `swiftPace_ring2` (Cat.cs:39608): ready
- `treasureHunt` (Cat.cs:9091): ready
- `twoPair_hit` (Cat.cs:9477): ready
- `twoPair_ring` (Cat.cs:26195): ready

### chameleon

- `allBugSlayer_fire` (Chameleon.cs:33006): ready
- `allBugSlayer_hit` (Chameleon.cs:9785): ready
- `allElementalSlayer_fire` (Chameleon.cs:33088): ready
- `allElementalSlayer_hit` (Chameleon.cs:9859): ready
- `allMachineSlayer_fire` (Chameleon.cs:33133): ready
- `allMachineSlayer_hit` (Chameleon.cs:9900): ready
- `allSlain_hit` (Chameleon.cs:9953): ready
- `allSlain_ring` (Chameleon.cs:34604): ready
- `allSlayer_ring` (Chameleon.cs:32297): ready
- `allTailSlayer_fire` (Chameleon.cs:33047): ready
- `allTailSlayer_hit` (Chameleon.cs:9822): ready
- `blend` (Chameleon.cs:16325): ready
- `bloodBurn` (Chameleon.cs:29807): ready
- `bugSlayer_eye` (Chameleon.cs:9615): ready
- `bugSlayer_fire` (Chameleon.cs:31797): ready
- `castRing` (Chameleon.cs:18534): ready
- `cAttack_fire` (Chameleon.cs:17253): ready
- `cAttack_ring1` (Chameleon.cs:16457): ready
- `cAttack_ring2` (Chameleon.cs:16496): ready
- `clearArrow` (Chameleon.cs:8996): ready
- `criticalPlus_hit` (Chameleon.cs:9338): ready
- `deadEffect` (Chameleon.cs:46832): ready
- `doubleStrider_left` (Chameleon.cs:27161): ready
- `doubleStrider_right` (Chameleon.cs:28535): ready
- `elementalSlayer_eye` (Chameleon.cs:9689): ready
- `elementalSlayer_fire` (Chameleon.cs:31875): ready
- `fatalStrike_ring` (Chameleon.cs:26527): ready
- `finalEntrapment` (Chameleon.cs:9142): ready
- `immunity_ring` (Chameleon.cs:18842): ready
- `machineSlayer_eye` (Chameleon.cs:9730): ready
- `machineSlayer_fire` (Chameleon.cs:31914): ready
- `markOfSlayer_hit` (Chameleon.cs:36758): ready
- `markOfSlayer_ring` (Chameleon.cs:36890): ready
- `massHouseShot` (Chameleon.cs:22359): ready
- `massLock_ring` (Chameleon.cs:22051): ready
- `massShot` (Chameleon.cs:22396): ready
- `nAttack` (Chameleon.cs:8460): ready
- `nAttack_hit` (Chameleon.cs:8578): ready
- `perfectBlend_ring` (Chameleon.cs:20595): ready
- `poisonVolley` (Chameleon.cs:23618): ready
- `quickFire_fire` (Chameleon.cs:19478): ready
- `rightStride_fire` (Chameleon.cs:28247): ready
- `rustyDecay_ring` (Chameleon.cs:35780): ready
- `skinShift_ring` (Chameleon.cs:35102): ready
- `strideShot_dust` (Chameleon.cs:27317): ready
- `tailSlayer_eye` (Chameleon.cs:9652): ready
- `tailSlayer_fire` (Chameleon.cs:31836): ready
- `tent_destroy` (Chameleon.cs:36181): ready
- `tent_heal` (Chameleon.cs:36294): ready
- `tent_ring` (Chameleon.cs:36079): ready
- `thunderDragon_ring1` (Chameleon.cs:38276): ready
- `thunderDragon_ring2` (Chameleon.cs:37992): needs ParticleSystem, ParticleSystemRenderer (its ParticleSystems / ParticleSystemRenderers (Unity 3.5 Shuriken, not decoded from BB) are grafted from TTO's copy by `wardrobe_fx.py` (SHURIKEN_FROM_TTO, matched by node name and material, BB's own materials): drawn)
- `tormentRain_fire` (Chameleon.cs:25996): ready
- `tormentRain_ring` (Chameleon.cs:25411): ready
- `venomShock_ring` (Chameleon.cs:24213): ready
- `zephyrLore_ring` (Chameleon.cs:10848): ready
- `zeroShot_ring` (Chameleon.cs:37637): needs ParticleSystem, ParticleSystemRenderer (its ParticleSystems / ParticleSystemRenderers (Unity 3.5 Shuriken, not decoded from BB) are grafted from TTO's copy by `wardrobe_fx.py` (SHURIKEN_FROM_TTO, matched by node name and material, BB's own materials): drawn)

### mole

Effects this scan does not see (2026-11-13, plans/fx_mole/parts.md "Read this first" 5, decisions.md 54): the hero prefab's fields in the Resources container, built by name: chopper, chopper_forwardDust, chopper_hit, chopper_StartDust (`Mole.cs:19763-19781`), missileBase, missile_fire (Mole_missile), missile_hit (`:19784-19802`), nAttack_fire (Mole_nAttack), nAttack_hit (`:19436-19439`), deadEffect (`:20084`), synchroMole, synchroMole_ring, timeNuke_explosion (`Mole_timeNuke.cs:350`); prefabs held only in script fields (no Resources path), exported under the field's name (`wardrobe_fx.py` FIELD_PREFABS): the Mole prefab's kaiser_dust and kaiser_box, AutoGyroGun4's autoGyroGun_fire; the summons Characters/Robots/AutoGyroGun4, BarrelBot4 and KingKaiser_<r g b k w> (EXTRA_FOLDERS), their AudioClip fields exported as sounds (SOUND_REFS). Every one ready.

- `assemble_box` (Mole.cs:23086): ready
- `assemble_dust` (Mole.cs:11764): ready
- `bazooka_fire` (Mole.cs:41324): ready
- `bazooka_hit` (Mole.cs:14026): ready
- `bazooka_ring` (Mole.cs:41156): needs ParticleSystem, ParticleSystemRenderer (its ParticleSystem / ParticleSystemRenderer (Unity 3.5 Shuriken, not decoded from BB) are grafted from TTO's copy by `wardrobe_fx.py` (SHURIKEN_FROM_TTO, matched by node name and material, BB's own materials): drawn)
- `bombardment_b` (Mole.cs:29996): ready
- `bombardment_fire` (Mole.cs:30418): ready
- `bombardment_g` (Mole.cs:29984): ready
- `bombardment_hit` (Mole.cs:30274): ready
- `bombardment_k` (Mole.cs:30008): ready
- `bombardment_r` (Mole.cs:29972): ready
- `bombardment_signal` (Mole.cs:29668): ready
- `bombardment_w` (Mole.cs:30020): ready
- `bunker` (Mole.cs:25254): ready
- `bunker_hole` (Mole.cs:25457): ready
- `cartBomb_fire` (Mole.cs:43076): ready
- `cartBomb_hit` (Mole.cs:14142): ready
- `cartBomb_ring` (Mole.cs:43039): ready
- `choppperCannon_ring` (Mole.cs:33707): ready
- `detonate` (Mole.cs:31113): ready
- `detonate_ring` (Mole.cs:31392): ready
- `dig_dirt` (Mole.cs:21780): ready
- `dig_dust` (Mole.cs:22241): ready
- `dig_hole` (Mole.cs:22434): ready
- `fireBarrage_b` (Mole.cs:29131): ready
- `fireBarrage_g` (Mole.cs:29119): ready
- `fireBarrage_hit1` (Mole.cs:29000): ready
- `fireBarrage_hit2` (Mole.cs:29035): ready
- `fireBarrage_k` (Mole.cs:29143): ready
- `fireBarrage_r` (Mole.cs:29107): ready
- `fireBarrage_signal` (Mole.cs:28787): ready
- `fireBarrage_w` (Mole.cs:29155): ready
- `flameCarnival` (Mole.cs:38506): ready
- `flameCarnival_fire` (Mole.cs:38968): ready
- `flameTurret` (Mole.cs:28349): ready
- `flameTurret_fire` (Mole.cs:27899): ready
- `grenadeCluster_fire` (Mole.cs:13800): ready
- `grenadeCluster_hit` (Mole.cs:13855): ready
- `megaDrill_hit` (Mole.cs:13919): ready
- `megaDrill_ring` (Mole.cs:39471): ready
- `megaHammer` (Mole.cs:33352): ready
- `megaPunch` (Mole.cs:32409): ready
- `megaPunch_hit` (Mole.cs:13075): ready
- `mine1` (Mole.cs:24269): ready
- `mine2` (Mole.cs:24308): ready
- `mine3` (Mole.cs:24347): ready
- `mine4` (Mole.cs:24386): ready
- `mine_hit` (Mole.cs:10543): ready
- `mineWalker_ring` (Mole.cs:45379): ready
- `mortarShot_fire` (Mole.cs:10758): ready
- `mortarShot_hit` (Mole.cs:10818): ready
- `napalm` (Mole.cs:13727): ready
- `napalm_hit` (Mole.cs:37757): ready
- `napalm_ring` (Mole.cs:37134): needs ParticleSystem, ParticleSystemRenderer (its ParticleSystem / ParticleSystemRenderer (Unity 3.5 Shuriken, not decoded from BB) are grafted from TTO's copy by `wardrobe_fx.py` (SHURIKEN_FROM_TTO, matched by node name and material, BB's own materials): drawn)
- `reload` (Mole.cs:10325): ready
- `rollerMachine_hit` (Mole.cs:14083): ready
- `rollerMachine_ring` (Mole.cs:42340): ready
- `sawMachine_ring` (Mole.cs:40519): ready
- `skyDrill` (Mole.cs:31948): ready
- `skyDrill_ring` (Mole.cs:32021): ready
- `skyShaker_ring` (Mole.cs:31986): ready
- `smartShell_hit` (Mole.cs:11503): ready
- `stunGrenade` (Mole.cs:11285): ready
- `stunMine1` (Mole.cs:27055): ready
- `stunMine2` (Mole.cs:27094): ready
- `stunMine_hit` (Mole.cs:11040): ready
- `superDig_dust` (Mole.cs:21664): ready
- `superTNT_hit` (Mole.cs:25881): ready
- `teslaCoil_ring` (Mole.cs:41723): ready
- `timeNuke1` (Mole.cs:11636): ready
- `timeNuke2` (Mole.cs:11675): ready
- `tnt` (Mole.cs:25792): ready
- `tnt_hit` (Mole.cs:25916): ready
- `warCapital` (Mole.cs:14267): needs ParticleSystem, ParticleSystemRenderer (its ParticleSystem / ParticleSystemRenderer (Unity 3.5 Shuriken, not decoded from BB) are grafted from TTO's copy by `wardrobe_fx.py` (SHURIKEN_FROM_TTO, matched by node name and material, BB's own materials): drawn)
- `warCapital_fire` (Mole.cs:44238): ready
- `warFactory_ring` (Mole.cs:40903): ready
- `warMissile` (Mole.cs:14507): ready
- `warMissile_hit` (Mole.cs:14603): ready

### monkey

Effects this scan does not see (2026-11-13, plans/fx_monkey/attacks_emotes.md part 2, decisions.md 59, 67): the hero prefab's fields in the Resources container, built by name: hpTransfer (`Monkey_hpTransfer`, `Monkey.cs:21027`: BoltEmitter, Light, AudioSource), castRing (`:24882`), castEffect_fire (`:26461`); prefabs held only in the summons' script fields (no Resources path), exported under the field's name (`wardrobe_fx.py` FIELD_PREFABS): phoenix_summon_ring, phoenix_fireBall (Phoenix_fireBall), phoenix_fireBall_hit, phoenix_instantBlaze_ring, phoenix_skyCrimson_dust, phoenix_skyCrimson_fire (Phoenix_skyCrimson_fire), phoenix_skyCrimson_hit, ja_summon_ring, buiten_summonEffect, gadina_summonEffect, gadina_earthGuard_ring, gadina_planetBreaker1 / 2, gadina_sword4, gadina_shield4, and gaos_summon_ring / gaos_unsummon_ring (ALIASES: elementals/gaos/effects); the summons Characters/Elementals/Phoenix/Phoenix4, Ja4, Gadina4, Buiten4, Gaos (EXTRA_FOLDERS), their AudioClip fields exported as sounds (SOUND_REFS); the Lavu serpent's lavu_summon (SOUND_ALIASES). Every one ready.

- `blazingArrow` (Monkey.cs:27703): ready
- `blazingForm0_ring` (Monkey.cs:40318): ready
- `blazingForm_fire` (Monkey.cs:39493): ready
- `blazingForm_ring` (Monkey.cs:39969): ready
- `deadEffect` (Monkey.cs:52233): ready
- `earthPulse` (Monkey.cs:13094): ready
- `earthPulse_hit` (Monkey.cs:32806): ready
- `earthPulse_ring` (Monkey.cs:32501): ready
- `earthRune_hit` (Monkey.cs:13613): ready
- `earthSoul_ring` (Monkey.cs:12600): ready
- `elementalBound_ring` (Monkey.cs:15530): ready
- `fireBall1` (Monkey.cs:11119): ready
- `fireBall2` (Monkey.cs:11158): ready
- `fireBall3` (Monkey.cs:11197): ready
- `fireBall4` (Monkey.cs:11236): ready
- `fireBall_hit` (Monkey.cs:11308): ready
- `fireRune_hit` (Monkey.cs:12347): ready
- `fireSoul_ring` (Monkey.cs:11377): ready
- `flashFire` (Monkey.cs:28556): ready
- `flashFire_ring` (Monkey.cs:28814): ready
- `gadinaArmor` (Monkey.cs:40695): ready
- `gadinaArmor_create` (Monkey.cs:40758): ready
- `gadinaArmor_destroy` (Monkey.cs:14280): ready
- `gAttack1_ring` (Monkey.cs:41461): ready
- `gAttack2_ring` (Monkey.cs:41853): ready
- `gAttack3_ring` (Monkey.cs:42387): ready
- `gAttack_hit` (Monkey.cs:14211): ready
- `groundLock_hit` (Monkey.cs:31127): ready
- `instantCast` (Monkey.cs:25036): ready
- `instantCast_ring` (Monkey.cs:10966): ready
- `lavu` (Monkey.cs:13889): ready
- `lavu_ring` (Monkey.cs:34612): ready
- `mikeBlink` (Monkey.cs:35895): ready
- `mikeCircle` (Monkey.cs:21055): ready
- `nAttack_hit` (Monkey.cs:10747): ready
- `pAttack_ring` (Monkey.cs:38914): ready
- `phoenixArmor` (Monkey.cs:38383): ready
- `phoenixArmor_create` (Monkey.cs:38449): ready
- `phoenixArmor_destroy` (Monkey.cs:14140): ready
- `planetBreaker_ring` (Monkey.cs:31967): ready
- `runicFlame` (Monkey.cs:12481): ready
- `runicSand` (Monkey.cs:13747): ready
- `secondStone` (Monkey.cs:31034): ready
- `sentinalGuard_ring` (Monkey.cs:42803): ready
- `stoneHammer` (Monkey.cs:33523): ready
- `summonSoul_ring` (Monkey.cs:24150): ready
- `upheaval` (Monkey.cs:35164): ready
- `upheaval_ring` (Monkey.cs:35389): ready
- `volcanicEruption` (Monkey.cs:43494): needs ParticleSystem, ParticleSystemRenderer (its ParticleSystems / ParticleSystemRenderers (Unity 3.5 Shuriken, not decoded from BB) are grafted from TTO's copy by `wardrobe_fx.py` (SHURIKEN_FROM_TTO, matched by material, BB's own materials): drawn)
- `volcanicEruption_ring` (Monkey.cs:43457): ready
- `worldIgnition` (Monkey.cs:30309): ready

### panda

- `ashuraFist` (Panda.cs:29770): ready
- `ashuraRing` (Panda.cs:30498): ready
- `auraBlast` (Panda.cs:18450): ready
- `auraField_ring` (Panda.cs:19072): ready
- `cAttack_ring` (Panda.cs:19034): ready
- `climbingCliff_hit` (Panda.cs:8747): ready
- `climbingCliff_ring` (Panda.cs:27699): ready
- `comboLink_ring` (Panda.cs:40690): ready
- `crushingMonolith` (Panda.cs:28525): ready
- `crushingMonolith_hit` (Panda.cs:9781): ready
- `deadEffect` (Panda.cs:50719): ready
- `deathBlow` (Panda.cs:35027): ready
- `deathBlow_ring` (Panda.cs:35545): ready
- `delayQi_fire` (Panda.cs:23759): ready
- `delayQi_ring` (Panda.cs:24217): ready
- `drunkenFist` (Panda.cs:31668): ready
- `drunkenSpin` (Panda.cs:31633): ready
- `fuujinKen_hit` (Panda.cs:9838): ready
- `fuujinKen_ring1` (Panda.cs:41267): ready
- `fuujinKen_ring2` (Panda.cs:40928): ready
- `fuujinKen_ring3` (Panda.cs:41312): ready
- `heavenPalm` (Panda.cs:9529): ready
- `heavenPalm_ring` (Panda.cs:40294): ready
- `lotusPalm` (Panda.cs:9479): ready
- `lotusPalm_ring` (Panda.cs:39465): ready
- `mysticSage_hit` (Panda.cs:9583): ready
- `nAttack_hit1` (Panda.cs:8007): ready
- `nAttack_hit2` (Panda.cs:8093): ready
- `nAttack_punch` (Panda.cs:15271): ready
- `nAttack_wheel` (Panda.cs:16927): ready
- `psalmOfEnergy_ring` (Panda.cs:10249): ready
- `pummel_dust` (Panda.cs:25033): ready
- `pummel_hit` (Panda.cs:8576): ready
- `pummel_ogre` (Panda.cs:24492): ready
- `pummel_ogreArm1` (Panda.cs:24553): ready
- `pummel_ogreArm2` (Panda.cs:24589): ready
- `qiBurst` (Panda.cs:23798): ready
- `qiStrike` (Panda.cs:23833): ready
- `qiStrike_hit` (Panda.cs:8519): ready
- `qiStrike_ring` (Panda.cs:23247): ready
- `raijinKen_hit` (Panda.cs:42515): needs ParticleSystem, ParticleSystemRenderer
- `raijinKen_ring1` (Panda.cs:42181): ready
- `raijinKen_ring2` (Panda.cs:41928): ready
- `rainStorm` (Panda.cs:38305): ready
- `risingDragon` (Panda.cs:29665): ready
- `risingDragon_hit` (Panda.cs:8932): ready
- `risingDragon_ring` (Panda.cs:29509): ready
- `risingVortex` (Panda.cs:29251): ready
- `risingVortex_hit` (Panda.cs:8882): ready
- `rollAround_ring` (Panda.cs:20624): ready
- `rushingFalcon` (Panda.cs:22711): ready
- `rushingFalcon_hit` (Panda.cs:8462): ready
- `safeGuard_hit` (Panda.cs:9737): ready
- `spTransfer` (Panda.cs:36062): ready
- `stasisBlow` (Panda.cs:34212): ready
- `stasisBlow_endDust` (Panda.cs:34464): ready
- `stasisBlow_ring` (Panda.cs:34727): ready
- `threeStep` (Panda.cs:21716): ready
- `threeStep_hit` (Panda.cs:8412): ready
- `tigerPounce_hit` (Panda.cs:8690): ready
- `tigerToss` (Panda.cs:26621): ready
- `timeAndTideCrane` (Panda.cs:33804): ready
- `timeAndTideMonkey` (Panda.cs:33237): ready
- `towerRush_hit` (Panda.cs:8626): ready
- `towerRush_ogre` (Panda.cs:25383): ready
- `towerRush_ring` (Panda.cs:25756): ready
- `waterCrane` (Panda.cs:33841): ready
- `waterCrane_hit` (Panda.cs:9088): ready
- `waterMonkey` (Panda.cs:33272): ready
- `waterMonkey_hit` (Panda.cs:9038): ready
- `windCloud` (Panda.cs:36687): ready

### penguin

- `absoluteZero` (Penguin.cs:33844): ready
- `arcticEmperor` (Penguin.cs:35042): ready
- `arcticWind` (Penguin.cs:30766): ready
- `astralShift_ring` (Penguin.cs:12805): ready
- `blink` (Penguin.cs:22817): ready
- `blink_ring` (Penguin.cs:23034): ready
- `blizzard` (Penguin.cs:34430): ready
- `cAttack_ring` (Penguin.cs:18593): ready
- `cosmicFriday` (Penguin.cs:39256): ready
- `cosmicFriday_ring` (Penguin.cs:39219): ready
- `cosmicRift_ring` (Penguin.cs:38736): ready
- `deadlyFrost` (Penguin.cs:30739): ready
- `dispell` (Penguin.cs:22289): ready
- `fallingComet` (Penguin.cs:26881): ready
- `fallingStar` (Penguin.cs:25871): ready
- `fallingStar_ring` (Penguin.cs:25563): ready
- `focusIntellect_ring` (Penguin.cs:35969): ready
- `frostSpike_ring` (Penguin.cs:37883): ready
- `frozenBlast` (Penguin.cs:29677): ready
- `frozenBreak` (Penguin.cs:29631): ready
- `giantComet` (Penguin.cs:37615): ready
- `giantStar` (Penguin.cs:37328): ready
- `iceBlock` (Penguin.cs:10716): ready
- `manaArc` (Penguin.cs:21821): ready
- `manaBurn` (Penguin.cs:24795): ready
- `manaField_ring` (Penguin.cs:18558): ready
- `manaPool_hit` (Penguin.cs:10562): ready
- `manaSurge` (Penguin.cs:24758): ready
- `meteora` (Penguin.cs:28348): ready
- `meteora_hit` (Penguin.cs:28412): ready
- `meteora_ring` (Penguin.cs:28521): ready
- `mpTransfer` (Penguin.cs:23488): ready
- `mpTransfer_ring` (Penguin.cs:23651): ready
- `multiCast` (Penguin.cs:9838): ready
- `parallelShift` (Penguin.cs:36642): ready
- `parallelShift_ring` (Penguin.cs:36854): ready
- `penguinOfArc` (Penguin.cs:21786): ready
- `snowBall_cast` (Penguin.cs:38253): ready
- `snowMan_ring` (Penguin.cs:32319): ready
- `spreadShot_fire` (Penguin.cs:11486): ready
- `tornado1` (Penguin.cs:10897): ready
- `tornado2` (Penguin.cs:10936): ready
- `tornado3` (Penguin.cs:10975): ready
- `tornado_hit` (Penguin.cs:10802): ready
- `tornado_ring` (Penguin.cs:10857): ready
- `typhoon1` (Penguin.cs:11170): ready
- `typhoon2` (Penguin.cs:11209): ready
- `typhoon3` (Penguin.cs:11248): ready

### rabbit

- `acidicField` (Rabbit.cs:10119): needs Rabbit_acidicField
- `acidicField_fire` (Rabbit.cs:10172): ready
- `allHpDrug1` (Rabbit.cs:45475): ready
- `allKoDrug1` (Rabbit.cs:45581): ready
- `allMpDrug1` (Rabbit.cs:45509): ready
- `allSpDrug1` (Rabbit.cs:45543): ready
- `backpack_hit` (Rabbit.cs:10707): ready
- `backpack_ring` (Rabbit.cs:31078): ready
- `bigbag_ring` (Rabbit.cs:31041): ready
- `boostShot` (Rabbit.cs:10265): ready
- `bounce1` (Rabbit.cs:21019): ready
- `bounce2` (Rabbit.cs:21865): ready
- `bouncingBullet` (Rabbit.cs:18097): ready
- `bouncingBullet_hit` (Rabbit.cs:18135): ready
- `cast_ring` (Rabbit.cs:23855): ready
- `cAttack_charge` (Rabbit.cs:18988): ready
- `cAttack_fire` (Rabbit.cs:19354): ready
- `cAttack_hit` (Rabbit.cs:9391): ready
- `circleShot` (Rabbit.cs:32909): ready
- `circleShot_ring` (Rabbit.cs:33072): ready
- `contract_create` (Rabbit.cs:11695): ready
- `contract_flag` (Rabbit.cs:40696): ready
- `diamondShot_fire` (Rabbit.cs:38214): ready
- `diamondShot_hit` (Rabbit.cs:11405): ready
- `diamondShot_ring` (Rabbit.cs:38544): ready
- `extravagance_ring` (Rabbit.cs:40021): needs ParticleSystem, ParticleSystemRenderer
- `fourShot_fire` (Rabbit.cs:32314): ready
- `fromTheAbove_ring` (Rabbit.cs:21830): ready
- `gilShot_fire` (Rabbit.cs:30320): ready
- `gilShot_hit` (Rabbit.cs:10502): ready
- `gilShot_ring` (Rabbit.cs:30726): ready
- `gorgonShot_fire` (Rabbit.cs:29605): ready
- `gorgonShot_hit` (Rabbit.cs:10452): ready
- `gorgonShot_ring` (Rabbit.cs:29974): ready
- `healingField` (Rabbit.cs:11295): needs Rabbit_healingField
- `healingField_fire` (Rabbit.cs:11355): ready
- `heatShot` (Rabbit.cs:10308): ready
- `hpPot1` (Rabbit.cs:24375): needs Rabbit_potion
- `hpPot2` (Rabbit.cs:24414): needs Rabbit_potion
- `hpPot3` (Rabbit.cs:24453): needs Rabbit_potion
- `hpPot4` (Rabbit.cs:24492): needs Rabbit_potion
- `hpPot_hit` (Rabbit.cs:9964): ready
- `immuneShot` (Rabbit.cs:10222): ready
- `lifeShot` (Rabbit.cs:10351): ready
- `maimShot_fire` (Rabbit.cs:23144): ready
- `maimShot_hit` (Rabbit.cs:9639): ready
- `medicalShot_fire` (Rabbit.cs:27821): ready
- `medicalShot_ring` (Rabbit.cs:27591): ready
- `millionaire1` (Rabbit.cs:37116): ready
- `millionaire2` (Rabbit.cs:37153): ready
- `millionaire_peppon` (Rabbit.cs:37473): ready
- `millionaire_ring` (Rabbit.cs:36909): ready
- `mpPot_hit` (Rabbit.cs:9880): ready
- `nAttack_fire` (Rabbit.cs:17537): ready
- `nAttack_hit` (Rabbit.cs:9125): ready
- `randomPot1` (Rabbit.cs:26173): needs Rabbit_potion
- `randomPot2` (Rabbit.cs:26204): needs Rabbit_potion
- `randomPot3` (Rabbit.cs:26235): needs Rabbit_potion
- `randomPot4` (Rabbit.cs:26266): needs Rabbit_potion
- `randomPot5` (Rabbit.cs:26297): needs Rabbit_potion
- `randomPot6` (Rabbit.cs:26328): needs Rabbit_potion
- `rapidTrance_potion` (Rabbit.cs:28987): ready
- `rapidTrance_ring` (Rabbit.cs:29062): ready
- `replenishment_ring` (Rabbit.cs:12843): ready
- `shootingArray_finalhit` (Rabbit.cs:11007): ready
- `shootingArray_fire` (Rabbit.cs:35184): ready
- `shootingArray_hit` (Rabbit.cs:10964): ready
- `shootingArray_ring` (Rabbit.cs:35793): ready
- `shotgun_fire` (Rabbit.cs:36211): ready
- `shotgun_hit` (Rabbit.cs:11057): ready
- `sniperCamera` (Rabbit.cs:18660): needs Rabbit_sniperCamera
- `spPot1` (Rabbit.cs:25246): needs Rabbit_potion
- `spPot2` (Rabbit.cs:25285): needs Rabbit_potion
- `spPot3` (Rabbit.cs:25324): needs Rabbit_potion
- `spPot_hit` (Rabbit.cs:9918): ready
- `statScan` (Rabbit.cs:22512): ready
- `statScan_dust` (Rabbit.cs:22545): ready
- `stickyGum` (Rabbit.cs:10045): needs Rabbit_stickyGum
- `tenShot_fire` (Rabbit.cs:39437): ready
- `tenShot_ring` (Rabbit.cs:39112): ready
- `truceTrading_fail` (Rabbit.cs:34859): ready
- `truceTrading_flag` (Rabbit.cs:34295): ready
- `truceTrading_ring` (Rabbit.cs:34263): ready
- `truceTrading_success` (Rabbit.cs:34755): ready

### sheep

- `blueSeal` (Sheep.cs:32226): ready
- `bookBash_hit` (Sheep.cs:11814): ready
- `bookBash_ring1` (Sheep.cs:37543): ready
- `bookBash_ring2` (Sheep.cs:37658): ready
- `bookBash_ring3` (Sheep.cs:37769): ready
- `cAttack` (Sheep.cs:9819): ready
- `cAttack_charge` (Sheep.cs:18698): ready
- `cAttack_hit` (Sheep.cs:9915): ready
- `cAttack_ring` (Sheep.cs:18730): ready
- `cleanse` (Sheep.cs:25343): ready
- `clear` (Sheep.cs:24849): ready
- `deadEffect` (Sheep.cs:46903): ready
- `divineChannel_ring` (Sheep.cs:40167): ready
- `divinityAxe` (Sheep.cs:36690): ready
- `divinityAxe_hit` (Sheep.cs:11757): ready
- `divinitySpear` (Sheep.cs:10752): ready
- `divinitySpear_ring` (Sheep.cs:31886): ready
- `divinitySword` (Sheep.cs:31107): ready
- `edenSanctuary` (Sheep.cs:37123): ready
- `edenSanctuary_ring` (Sheep.cs:37087): ready
- `freeCast` (Sheep.cs:10157): ready
- `heal` (Sheep.cs:22248): ready
- `holylight` (Sheep.cs:27863): ready
- `holylight_ring` (Sheep.cs:28100): ready
- `homingLight` (Sheep.cs:11445): ready
- `illuminate` (Sheep.cs:29372): ready
- `koHeal` (Sheep.cs:10334): ready
- `lullaby_ring` (Sheep.cs:35696): ready
- `nAttack` (Sheep.cs:9316): ready
- `nAttack_hit` (Sheep.cs:9409): ready
- `overHeal` (Sheep.cs:26293): ready
- `overHeal_ring` (Sheep.cs:21172): ready
- `pacify` (Sheep.cs:23760): ready
- `purifyingTear_ring` (Sheep.cs:34841): ready
- `quickHeal` (Sheep.cs:10369): ready
- `radiantHeal` (Sheep.cs:22213): ready
- `redSeal` (Sheep.cs:32191): ready
- `returnCast` (Sheep.cs:11651): ready
- `revert` (Sheep.cs:27339): ready
- `revive` (Sheep.cs:26829): ready
- `sealOfAttack` (Sheep.cs:10822): ready
- `sealOfDefense` (Sheep.cs:10958): ready
- `sealOfEarth` (Sheep.cs:11100): ready
- `sealOfHeaven` (Sheep.cs:11243): ready
- `sleep` (Sheep.cs:24347): ready
- `soulOfArms` (Sheep.cs:34106): ready
- `soulOfArms_ring` (Sheep.cs:33999): ready
- `soulOfArms_trail` (Sheep.cs:34031): ready
- `whiteBurst_hit` (Sheep.cs:11577): ready
- `worldEncarta_hit` (Sheep.cs:11871): ready
- `worldEncarta_ring` (Sheep.cs:38322): ready

### whale

- `asunderImpale` (Whale.cs:27157): ready
- `asunderRound` (Whale.cs:28013): ready
- `bowlingWhale` (Whale.cs:36680): ready
- `bowlingWhale_ring` (Whale.cs:37128): ready
- `bubbleBurst` (Whale.cs:35943): ready
- `bubbleBurst_ring` (Whale.cs:35768): ready
- `bubbleShield_cast` (Whale.cs:29688): ready
- `callToArm_ring` (Whale.cs:33314): ready
- `castRing` (Whale.cs:20409): ready
- `deadEffect` (Whale.cs:46461): ready
- `divingWave` (Whale.cs:31865): ready
- `extendedWave1` (Whale.cs:16554): ready
- `extendedWave2` (Whale.cs:16850): ready
- `extendedWave3` (Whale.cs:18045): ready
- `flyingShield` (Whale.cs:24795): needs Whale_flyingShield
- `flyingShield_hit` (Whale.cs:8955): ready
- `gobbleUp_hit` (Whale.cs:9072): ready
- `gobbleUp_ring` (Whale.cs:26461): ready
- `grandTide` (Whale.cs:37424): needs ParticleSystem, ParticleSystemRenderer
- `grandTide_ring` (Whale.cs:37896): ready
- `homingShield` (Whale.cs:10401): needs Whale_homingShield
- `hydroBlast` (Whale.cs:10037): ready
- `javelin` (Whale.cs:8781): needs Whale_javelin
- `kingdomKnight1` (Whale.cs:28433): needs whale_kingdomKnight
- `kingdomKnight2` (Whale.cs:28468): needs whale_kingdomKnight
- `kingdomKnight_ring1` (Whale.cs:28755): ready
- `malStorm` (Whale.cs:32480): ready
- `malStorm_bolt` (Whale.cs:10188): ready
- `megalodon` (Whale.cs:34790): ready
- `megalodon_ring` (Whale.cs:34744): ready
- `nAttack_hit` (Whale.cs:8303): ready
- `peninsulaImpale` (Whale.cs:27219): ready
- `peninsulaImpale_ring` (Whale.cs:27389): ready
- `peninsulaRound` (Whale.cs:28048): ready
- `peninsulaRound_ring` (Whale.cs:27957): ready
- `rejuvenate` (Whale.cs:31310): ready
- `revitalize_ring` (Whale.cs:36455): ready
- `roundTable_ring` (Whale.cs:29251): ready
- `salvation_ring` (Whale.cs:33689): ready
- `seaAegis_ring` (Whale.cs:11109): ready
- `shieldBash_hit` (Whale.cs:8688): ready
- `shieldBash_ring` (Whale.cs:19811): ready
- `shieldRush_hit` (Whale.cs:8905): ready
- `shieldRush_ring` (Whale.cs:24190): ready
- `spiralBlast` (Whale.cs:9997): ready
- `swallow_hit` (Whale.cs:9020): ready
- `swallow_ring` (Whale.cs:25666): ready
- `sweep_ring` (Whale.cs:22438): ready
- `tideCutter_ring` (Whale.cs:22309): ready
- `wallPuncture_hit` (Whale.cs:9247): ready
- `whaleWave` (Whale.cs:31900): ready

### wolf

- `armorBreak1` (Wolf.cs:22598): ready
- `armorBreak2` (Wolf.cs:22633): ready
- `armorBreak_ring` (Wolf.cs:22966): ready
- `artBreaker_hit` (Wolf.cs:9175): ready
- `artBreaker_ring` (Wolf.cs:34291): ready
- `artCancel_ring` (Wolf.cs:27791): ready
- `artCancel_slide` (Wolf.cs:27759): ready
- `bladeFang_ring` (Wolf.cs:26598): ready
- `bladeFang_underSlash` (Wolf.cs:25658): ready
- `bladeFang_upperSlash` (Wolf.cs:25871): ready
- `bladeSong` (Wolf.cs:29963): ready
- `bladeSong_finalBlade` (Wolf.cs:30095): ready
- `bladeSong_ring` (Wolf.cs:29857): ready
- `bloodFang_underSlash` (Wolf.cs:25695): ready
- `bloodFang_upperSlash` (Wolf.cs:25906): ready
- `braveSpirit` (Wolf.cs:20357): ready
- `cAttack1_ring` (Wolf.cs:18976): ready
- `cAttack1_ring1` (Wolf.cs:19160): ready
- `cAttack1_ring2` (Wolf.cs:19116): ready
- `cAttack1_ring3` (Wolf.cs:19068): ready
- `cAttack2` (Wolf.cs:19403): ready
- `crossBreak` (Wolf.cs:23884): ready
- `crossBreak_ring` (Wolf.cs:23736): ready
- `crusader` (Wolf.cs:21085): ready
- `crusader_hit` (Wolf.cs:8492): ready
- `crusader_ring` (Wolf.cs:21516): ready
- `darkEdge1` (Wolf.cs:15091): ready
- `darkEdge2` (Wolf.cs:17682): ready
- `darkEdge_ring` (Wolf.cs:30731): ready
- `deadEffect` (Wolf.cs:46037): ready
- `doubleArt` (Wolf.cs:18411): ready
- `dualBrand_hit` (Wolf.cs:9325): ready
- `dualBrand_ring` (Wolf.cs:36807): ready
- `dualBrand_slash1` (Wolf.cs:35947): ready
- `dualBrand_slash2` (Wolf.cs:36107): ready
- `dualBrand_slash3` (Wolf.cs:36262): ready
- `dualBrand_slash4` (Wolf.cs:36412): ready
- `feralAssault_hit` (Wolf.cs:9275): ready
- `feralAssault_ring1` (Wolf.cs:35463): ready
- `feralAssault_ring2` (Wolf.cs:35219): ready
- `feralAssault_ring3` (Wolf.cs:35515): ready
- `feralStrike` (Wolf.cs:29106): ready
- `feralStrike_hit` (Wolf.cs:8873): ready
- `feralStrike_ring` (Wolf.cs:29585): ready
- `gloriousSpirit` (Wolf.cs:20394): ready
- `grandCross` (Wolf.cs:24439): ready
- `grandCross_mark` (Wolf.cs:8615): ready
- `grandCross_ring` (Wolf.cs:24743): ready
- `holyArmor_ring` (Wolf.cs:33721): ready
- `holySword_ring` (Wolf.cs:33206): ready
- `lawBringer` (Wolf.cs:21048): ready
- `lawBringer_hit` (Wolf.cs:8457): ready
- `lawBringer_ring` (Wolf.cs:21387): ready
- `mirrorBlade_hit` (Wolf.cs:9225): ready
- `mirrorBlade_mirror` (Wolf.cs:34562): ready
- `mirrorBlade_ring` (Wolf.cs:34962): ready
- `obsidianFang_hit` (Wolf.cs:9575): ready
- `powerBreak1` (Wolf.cs:22233): ready
- `powerBreak2` (Wolf.cs:22268): ready
- `resurrection_hit` (Wolf.cs:25114): ready
- `resurrection_ring` (Wolf.cs:25390): ready
- `secondWind` (Wolf.cs:23221): ready
- `skySlasher` (Wolf.cs:31697): ready
- `skySlasher_ring` (Wolf.cs:19020): ready
- `sublimeArt_ring` (Wolf.cs:18449): ready
- `thirdRend_ring` (Wolf.cs:32659): ready
- `twinResonance_fire` (Wolf.cs:37590): ready
- `twinResonance_hit` (Wolf.cs:9425): ready
- `twinResonance_ring` (Wolf.cs:37343): ready

