# Effect parts each class needs

Written by `pipeline/wardrobe_fx_inventory.py` (do not edit by hand; run it again). Effects = the prefabs in a
class's own Effects folder (`heroes/<cls>/effects`) that its `<Class>.cs` loads: skills, hits, buffs, projectiles,
not only skills. Physics parts (colliders, Rigidbody) are left out: they draw nothing.
Ready = every part is one the page builds today (Animation, AudioSource, EffectControl, EffectControl(child), EllipsoidParticleEmitter, EmblemEmitter, EmitterControl, ImageEmitter, LineEmitter, ParticleAnimator, ParticleRenderer, RingEmitter, ShatterMesh, SkinnedMeshRenderer, StaticMesh, TrailEmitter, TrailRenderer, VortexEmitter) and `wardrobe_fx.py`
extracts it (checked in memory). Each class's code also loads its pet's and other classes' effects (shown on it,
like a Sheep's heal): counted apart, never this class's skills.

## Per class

| class | own effects | ready | not ready | parts missing (own effects needing it) | others' loaded |
|---|---|---|---|---|---|
| bat | 26 | 18 | 8 | AlphaTimer 2, BoltEmitter 2, ProjectileControl 1, Bat_echoes 1, Bat_guardianOfTheNight 1, Light 1, Bat_mirageOrb 1, AudioControl 1 | 29 |
| bison | 46 | 35 | 11 | AlphaTimer 9, UVScroll 2, Bison_earthRupture 1, ProjectileControl 1, ParticleSystemRenderer 1, ParticleSystem 1 | 28 |
| cat | 67 | 58 | 9 | AlphaTimer 3, WorldParticleCollider 2, StatusControl 1, UVScroll 1, Cat_grandCasinoArcade 1, Cat_supportFire 1, ParticleSystemRenderer 1, ParticleSystem 1 | 28 |
| chameleon | 57 | 46 | 11 | BoltEmitter 6, Chameleon_nAttack 2, ProjectileControl 2, ParticleSystemRenderer 2, ParticleSystem 2, WorldParticleCollider 1 | 28 |
| mole | 78 | 56 | 22 | ProjectileControl 6, Mole_mine 4, ParticleSystemRenderer 3, ParticleSystem 3, AlphaTimer 2, Mole_stunMine 2, Mole_timeNuke 2, Mole_bazooka 1, Mole_cartBomb 1, Mole_flameCarnival 1, rotationControl 1, AudioControl 1, Mole_grenadeCluster 1, Mole_mortarShot 1, Mole_napalm 1, Mole_stunGrenade 1, Mole_warCapital 1, CharacterControl 1, Mole_warMissile 1 | 28 |
| monkey | 51 | 36 | 15 | AlphaTimer 6, ProjectileControl 5, Monkey_fireBall 4, Monkey_earthPulse 1, rotationControl 1, Monkey_lavu 1, Monkey_runicFlame 1, Monkey_runicSand 1, ParticleSystemRenderer 1, ParticleSystem 1, AudioControl 1 | 28 |
| panda | 71 | 58 | 13 | AlphaTimer 12, BoltEmitter 2, AudioControl 1, ParticleSystemRenderer 1, ParticleSystem 1 | 28 |
| penguin | 48 | 36 | 12 | Penguin_tornado 3, Penguin_typhoon 3, AlphaTimer 2, Penguin_arcticEmperor 1, Penguin_cosmicFriday 1, Penguin_iceBlock 1, ProjectileControl 1, Penguin_nAttack 1 | 28 |
| rabbit | 84 | 61 | 23 | Rabbit_potion 13, AlphaTimer 3, WorldParticleCollider 2, Rabbit_acidicField 1, ParticleSystemRenderer 1, ParticleSystem 1, Rabbit_healingField 1, Rabbit_sniperCamera 1, Rabbit_stickyGum 1 | 24 |
| sheep | 51 | 38 | 13 | AlphaTimer 6, Sheep_seal 4, ProjectileControl 3, Sheep_cAttack 1, Sheep_edenSanctuary 1, Sheep_homingLight 1, Sheep_nAttack 1 | 27 |
| whale | 51 | 43 | 8 | whale_kingdomKnight 2, UVScroll 1, AlphaTimer 1, AudioControl 1, Whale_flyingShield 1, ParticleSystemRenderer 1, ParticleSystem 1, Whale_homingShield 1, ProjectileControl 1, Whale_javelin 1, BoltEmitter 1 | 28 |
| wolf | 69 | 67 | 2 | Light 2 | 28 |

## Per missing part

Own effects that need the part (all classes), and how many of those it alone blocks
(every other part of theirs is built).

| part | effects | blocks alone | classes |
|---|---|---|---|
| AlphaTimer | 46 | 39 | bat, bison, cat, mole, monkey, panda, penguin, rabbit, sheep, whale |
| Rabbit_potion | 13 | 13 | rabbit |
| BoltEmitter | 11 | 9 | bat, chameleon, panda, whale |
| WorldParticleCollider | 5 | 5 | cat, chameleon, rabbit |
| Sheep_seal | 4 | 4 | sheep |
| Mole_mine | 4 | 4 | mole |
| Penguin_typhoon | 3 | 3 | penguin |
| Penguin_tornado | 3 | 3 | penguin |
| Light | 3 | 2 | bat, wolf |
| whale_kingdomKnight | 2 | 2 | whale |
| Mole_timeNuke | 2 | 2 | mole |
| Mole_stunMine | 2 | 2 | mole |
| AudioControl | 5 | 1 | bat, mole, monkey, panda, whale |
| Whale_homingShield | 1 | 1 | whale |
| Whale_flyingShield | 1 | 1 | whale |
| StatusControl | 1 | 1 | cat |
| Rabbit_stickyGum | 1 | 1 | rabbit |
| Rabbit_sniperCamera | 1 | 1 | rabbit |
| Rabbit_healingField | 1 | 1 | rabbit |
| Rabbit_acidicField | 1 | 1 | rabbit |
| Penguin_iceBlock | 1 | 1 | penguin |
| Penguin_cosmicFriday | 1 | 1 | penguin |
| Penguin_arcticEmperor | 1 | 1 | penguin |
| Monkey_runicSand | 1 | 1 | monkey |
| Monkey_runicFlame | 1 | 1 | monkey |
| Mole_flameCarnival | 1 | 1 | mole |
| Mole_cartBomb | 1 | 1 | mole |
| Cat_supportFire | 1 | 1 | cat |
| Cat_grandCasinoArcade | 1 | 1 | cat |
| Bat_mirageOrb | 1 | 1 | bat |
| Bat_guardianOfTheNight | 1 | 1 | bat |
| ProjectileControl | 20 | 0 | bat, bison, chameleon, mole, monkey, penguin, sheep, whale |
| ParticleSystemRenderer | 11 | 0 | bison, cat, chameleon, mole, monkey, panda, rabbit, whale |
| ParticleSystem | 11 | 0 | bison, cat, chameleon, mole, monkey, panda, rabbit, whale |
| UVScroll | 4 | 0 | bison, cat, whale |
| Monkey_fireBall | 4 | 0 | monkey |
| rotationControl | 2 | 0 | mole, monkey |
| Chameleon_nAttack | 2 | 0 | chameleon |
| Whale_javelin | 1 | 0 | whale |
| Sheep_nAttack | 1 | 0 | sheep |
| Sheep_homingLight | 1 | 0 | sheep |
| Sheep_edenSanctuary | 1 | 0 | sheep |
| Sheep_cAttack | 1 | 0 | sheep |
| Penguin_nAttack | 1 | 0 | penguin |
| Monkey_lavu | 1 | 0 | monkey |
| Monkey_earthPulse | 1 | 0 | monkey |
| Mole_warMissile | 1 | 0 | mole |
| Mole_warCapital | 1 | 0 | mole |
| Mole_stunGrenade | 1 | 0 | mole |
| Mole_napalm | 1 | 0 | mole |
| Mole_mortarShot | 1 | 0 | mole |
| Mole_grenadeCluster | 1 | 0 | mole |
| Mole_bazooka | 1 | 0 | mole |
| CharacterControl | 1 | 0 | mole |
| Bison_earthRupture | 1 | 0 | bison |
| Bat_echoes | 1 | 0 | bat |

## Build order (greedy)

Each step: the part that makes the most own effects ready, given the ones above it
(when none alone does, the part most not-ready effects need). Ready after = all classes.

| step | part | newly ready | ready after |
|---|---|---|---|
| 0 | (built today) | 552 | 552 / 699 |
| 1 | AlphaTimer | 39 | 591 / 699 |
| 2 | Rabbit_potion | 13 | 604 / 699 |
| 3 | BoltEmitter | 9 | 613 / 699 |
| 4 | WorldParticleCollider | 5 | 618 / 699 |
| 5 | Sheep_seal | 4 | 622 / 699 |
| 6 | Mole_mine | 4 | 626 / 699 |
| 7 | UVScroll | 3 | 629 / 699 |
| 8 | AudioControl | 3 | 632 / 699 |
| 9 | Penguin_typhoon | 3 | 635 / 699 |
| 10 | Penguin_tornado | 3 | 638 / 699 |
| 11 | Light | 3 | 641 / 699 |
| 12 | whale_kingdomKnight | 2 | 643 / 699 |
| 13 | Mole_timeNuke | 2 | 645 / 699 |
| 14 | Mole_stunMine | 2 | 647 / 699 |
| 15 | rotationControl | 1 | 648 / 699 |
| 16 | Whale_homingShield | 1 | 649 / 699 |
| 17 | Whale_flyingShield | 1 | 650 / 699 |
| 18 | StatusControl | 1 | 651 / 699 |
| 19 | Sheep_edenSanctuary | 1 | 652 / 699 |
| 20 | Rabbit_stickyGum | 1 | 653 / 699 |
| 21 | Rabbit_sniperCamera | 1 | 654 / 699 |
| 22 | Rabbit_healingField | 1 | 655 / 699 |
| 23 | Rabbit_acidicField | 1 | 656 / 699 |
| 24 | Penguin_iceBlock | 1 | 657 / 699 |
| 25 | Penguin_cosmicFriday | 1 | 658 / 699 |
| 26 | Penguin_arcticEmperor | 1 | 659 / 699 |
| 27 | Monkey_runicSand | 1 | 660 / 699 |
| 28 | Monkey_runicFlame | 1 | 661 / 699 |
| 29 | Monkey_lavu | 1 | 662 / 699 |
| 30 | Mole_flameCarnival | 1 | 663 / 699 |
| 31 | Mole_cartBomb | 1 | 664 / 699 |
| 32 | Cat_supportFire | 1 | 665 / 699 |
| 33 | Cat_grandCasinoArcade | 1 | 666 / 699 |
| 34 | Bat_mirageOrb | 1 | 667 / 699 |
| 35 | Bat_guardianOfTheNight | 1 | 668 / 699 |
| 36 | ProjectileControl | 0 | 668 / 699 |
| 37 | Monkey_fireBall | 4 | 672 / 699 |
| 38 | Chameleon_nAttack | 2 | 674 / 699 |
| 39 | Whale_javelin | 1 | 675 / 699 |
| 40 | Sheep_nAttack | 1 | 676 / 699 |
| 41 | Sheep_homingLight | 1 | 677 / 699 |
| 42 | Sheep_cAttack | 1 | 678 / 699 |
| 43 | Penguin_nAttack | 1 | 679 / 699 |
| 44 | Monkey_earthPulse | 1 | 680 / 699 |
| 45 | Mole_warMissile | 1 | 681 / 699 |
| 46 | Mole_stunGrenade | 1 | 682 / 699 |
| 47 | Mole_napalm | 1 | 683 / 699 |
| 48 | Mole_mortarShot | 1 | 684 / 699 |
| 49 | Mole_grenadeCluster | 1 | 685 / 699 |
| 50 | Mole_bazooka | 1 | 686 / 699 |
| 51 | Bison_earthRupture | 1 | 687 / 699 |
| 52 | Bat_echoes | 1 | 688 / 699 |
| 53 | ParticleSystemRenderer | 0 | 688 / 699 |
| 54 | ParticleSystem | 10 | 698 / 699 |
| 55 | Mole_warCapital | 0 | 698 / 699 |
| 56 | CharacterControl | 1 | 699 / 699 |

## Per effect

### bat

- `bigcast_ring` (Bat.cs:30026): ready
- `blackservant_ring` (Bat.cs:44917): ready
- `bloodcarnage_ring` (Bat.cs:16065): ready
- `charm_hit` (Bat.cs:13666): ready
- `deadeffect` (Bat.cs:53740): ready
- `demongaze_hit` (Bat.cs:11542): ready
- `dreamburst_hit` (Bat.cs:13989): needs AlphaTimer
- `dreamdazzle_hit` (Bat.cs:35102): ready
- `echoes` (Bat.cs:11825): needs Bat_echoes, ProjectileControl
- `echoes_hit` (Bat.cs:11928): ready
- `echoes_ring` (Bat.cs:27967): ready
- `guardian` (Bat.cs:30549): needs Bat_guardianOfTheNight
- `masscast` (Bat.cs:11140): ready
- `mindcontrol_ring` (Bat.cs:13738): needs BoltEmitter, Light
- `mirageorb` (Bat.cs:12669): needs Bat_mirageOrb
- `nefariouswhip_hit` (Bat.cs:44025): needs AudioControl
- `nightmare_ring` (Bat.cs:11996): needs BoltEmitter
- `paranoia_hit` (Bat.cs:14599): ready
- `phantasmblast_hit` (Bat.cs:36059): ready
- `shadowgaze_hit` (Bat.cs:11582): ready
- `shadowsacrifice_ring` (Bat.cs:14301): ready
- `shatteringdream_hit` (Bat.cs:42548): needs AlphaTimer
- `souleater_hit` (Bat.cs:14413): ready
- `souleater_ring` (Bat.cs:40715): ready
- `swap_hit` (Bat.cs:13562): ready
- `switch_hit` (Bat.cs:13368): ready

### bison

- `aftershock` (Bison.cs:22984): ready
- `aspect_slam` (Bison.cs:21449): needs AlphaTimer, UVScroll
- `aspect_trample` (Bison.cs:22536): needs AlphaTimer, UVScroll
- `calamityhammer_fire` (Bison.cs:32785): ready
- `calamityhammer_ring` (Bison.cs:32350): ready
- `cattack1_dust` (Bison.cs:19320): ready
- `cattack2_dust` (Bison.cs:20379): ready
- `deadeffect` (Bison.cs:41201): ready
- `diamondshield_ring` (Bison.cs:28196): ready
- `earthrupture` (Bison.cs:8775): needs Bison_earthRupture, ProjectileControl
- `earthrupture_ring` (Bison.cs:28854): ready
- `earthsmasher` (Bison.cs:29132): needs AlphaTimer
- `earthsmasher_ring` (Bison.cs:29505): ready
- `enrage_ring` (Bison.cs:20911): ready
- `farstun` (Bison.cs:7646): ready
- `farstun_ring` (Bison.cs:23695): ready
- `holdcharge_fire` (Bison.cs:20280): ready
- `instantrush_dust` (Bison.cs:24514): ready
- `instantrush_ring` (Bison.cs:24482): needs AlphaTimer
- `ironshield_ring` (Bison.cs:27609): ready
- `knockdown` (Bison.cs:23019): ready
- `knockdown_hit` (Bison.cs:7511): ready
- `knockdown_ring` (Bison.cs:23393): ready
- `magmaclutter_ring1` (Bison.cs:31839): ready
- `magmaclutter_ring2` (Bison.cs:31506): needs ParticleSystem, ParticleSystemRenderer
- `massstun` (Bison.cs:9096): needs AlphaTimer
- `onslaught_ring` (Bison.cs:30325): ready
- `overpower` (Bison.cs:24985): ready
- `overswing_ring` (Bison.cs:25579): ready
- `powercleave` (Bison.cs:26129): ready
- `powercleave_hit` (Bison.cs:8162): ready
- `powercleave_ring` (Bison.cs:26465): ready
- `powerhammer` (Bison.cs:26179): ready
- `powerhammer_hit` (Bison.cs:8254): ready
- `powerreel_ring` (Bison.cs:26513): ready
- `pridecrusher_ring` (Bison.cs:31147): ready
- `slam_dust` (Bison.cs:21411): needs AlphaTimer
- `slam_ring` (Bison.cs:21794): ready
- `solidcharge_ring` (Bison.cs:19358): ready
- `spinhack_ring` (Bison.cs:20417): ready
- `stunningground_ring` (Bison.cs:9378): ready
- `titanform_ring` (Bison.cs:30006): ready
- `trample1` (Bison.cs:22057): needs AlphaTimer
- `trample2` (Bison.cs:22096): needs AlphaTimer
- `trample_dust` (Bison.cs:22648): needs AlphaTimer
- `warcry_ring` (Bison.cs:26868): ready

### cat

- `assassinate_hit` (Cat.cs:41949): ready
- `awareness1` (Cat.cs:8591): ready
- `awareness2` (Cat.cs:8630): ready
- `backstab_hit` (Cat.cs:10353): ready
- `bleed_fire` (Cat.cs:34887): ready
- `bleed_hit` (Cat.cs:10282): ready
- `bleed_ring` (Cat.cs:35207): ready
- `copycat_hit` (Cat.cs:9541): ready
- `copycat_ring` (Cat.cs:26750): ready
- `damageplus` (Cat.cs:19749): needs StatusControl
- `damageplus_ring` (Cat.cs:19987): ready
- `damageroulette_ring` (Cat.cs:27080): ready
- `deltastrike` (Cat.cs:37470): needs AlphaTimer, UVScroll
- `deltastrike_cat` (Cat.cs:37305): needs AlphaTimer
- `deltastrike_ring` (Cat.cs:37105): ready
- `disarm` (Cat.cs:34055): ready
- `disarm_hit` (Cat.cs:10232): ready
- `disarm_ring` (Cat.cs:34375): ready
- `doubledown1_hit` (Cat.cs:25441): ready
- `doubledown2_hit` (Cat.cs:25405): ready
- `doubledown_ring` (Cat.cs:24711): ready
- `evenodds_hit` (Cat.cs:9351): ready
- `fatedraw_ring` (Cat.cs:21714): ready
- `finishingblow_hit` (Cat.cs:38739): ready
- `finishingblow_ring1` (Cat.cs:38445): ready
- `finishingblow_ring2` (Cat.cs:39223): ready
- `flyingdagger_fire` (Cat.cs:29156): ready
- `flyingdagger_hit` (Cat.cs:9838): ready
- `forwardlunge_hit` (Cat.cs:9888): ready
- `grandcasinoarcade` (Cat.cs:27826): needs Cat_grandCasinoArcade
- `grandcasinoarcade_hit1` (Cat.cs:9669): ready
- `grandcasinoarcade_hit2` (Cat.cs:9706): ready
- `grandcasinoarcade_hit3` (Cat.cs:9743): ready
- `grandcasinoarcade_hit7` (Cat.cs:9784): ready
- `grandcasinoarcade_ring1` (Cat.cs:28645): ready
- `grandcasinoarcade_ring2` (Cat.cs:28406): ready
- `hiddenblade_hit` (Cat.cs:10072): ready
- `ladyluck_ring` (Cat.cs:21585): ready
- `lifegamble_heal` (Cat.cs:9169): ready
- `lifegamble_hit` (Cat.cs:9212): ready
- `lifegamble_ring` (Cat.cs:22967): ready
- `luckycard_fire` (Cat.cs:20626): ready
- `luckydice` (Cat.cs:23872): needs WorldParticleCollider
- `moonblade` (Cat.cs:35984): ready
- `moonstorm` (Cat.cs:36726): ready
- `nattack_dust` (Cat.cs:16320): ready
- `nattack_hit` (Cat.cs:8266): ready
- `pillageplunge_hit` (Cat.cs:10510): ready
- `pillageplunge_ring1` (Cat.cs:40471): ready
- `pillageplunge_ring2` (Cat.cs:40110): ready
- `pillageplunge_ring3` (Cat.cs:40289): ready
- `powershuffle_ring` (Cat.cs:22424): ready
- `reversethrust` (Cat.cs:31169): ready
- `reversethrust_hit` (Cat.cs:9938): ready
- `skillgamble_heal` (Cat.cs:9262): ready
- `skillgamble_hit` (Cat.cs:9305): ready
- `skillgamble_ring` (Cat.cs:23499): ready
- `supportfire_cannon` (Cat.cs:41072): needs AlphaTimer
- `supportfire_fire` (Cat.cs:10731): needs Cat_supportFire
- `supportfire_hit` (Cat.cs:10790): needs ParticleSystem, ParticleSystemRenderer
- `supportfire_ring` (Cat.cs:40920): ready
- `supportfire_smoke` (Cat.cs:10699): ready
- `swiftpace_ring1` (Cat.cs:39733): ready
- `swiftpace_ring2` (Cat.cs:39608): ready
- `treasurehunt` (Cat.cs:9091): needs WorldParticleCollider
- `twopair_hit` (Cat.cs:9477): ready
- `twopair_ring` (Cat.cs:26195): ready

### chameleon

- `allbugslayer_fire` (Chameleon.cs:33006): ready
- `allbugslayer_hit` (Chameleon.cs:9785): needs BoltEmitter
- `allelementalslayer_fire` (Chameleon.cs:33088): ready
- `allelementalslayer_hit` (Chameleon.cs:9859): needs BoltEmitter
- `allmachineslayer_fire` (Chameleon.cs:33133): ready
- `allmachineslayer_hit` (Chameleon.cs:9900): needs BoltEmitter
- `allslain_hit` (Chameleon.cs:9953): needs BoltEmitter
- `allslain_ring` (Chameleon.cs:34604): ready
- `allslayer_ring` (Chameleon.cs:32297): ready
- `alltailslayer_fire` (Chameleon.cs:33047): ready
- `alltailslayer_hit` (Chameleon.cs:9822): needs BoltEmitter
- `blend` (Chameleon.cs:16325): ready
- `bloodburn` (Chameleon.cs:29807): ready
- `bugslayer_eye` (Chameleon.cs:9615): ready
- `bugslayer_fire` (Chameleon.cs:31797): ready
- `castring` (Chameleon.cs:18534): ready
- `cattack_fire` (Chameleon.cs:17253): ready
- `cattack_ring1` (Chameleon.cs:16457): ready
- `cattack_ring2` (Chameleon.cs:16496): ready
- `cleararrow` (Chameleon.cs:8996): needs Chameleon_nAttack, ProjectileControl
- `criticalplus_hit` (Chameleon.cs:9338): ready
- `deadeffect` (Chameleon.cs:46832): ready
- `doublestrider_left` (Chameleon.cs:27161): ready
- `doublestrider_right` (Chameleon.cs:28535): ready
- `elementalslayer_eye` (Chameleon.cs:9689): ready
- `elementalslayer_fire` (Chameleon.cs:31875): ready
- `fatalstrike_ring` (Chameleon.cs:26527): ready
- `finalentrapment` (Chameleon.cs:9142): ready
- `immunity_ring` (Chameleon.cs:18842): ready
- `machineslayer_eye` (Chameleon.cs:9730): ready
- `machineslayer_fire` (Chameleon.cs:31914): ready
- `markofslayer_hit` (Chameleon.cs:36758): ready
- `markofslayer_ring` (Chameleon.cs:36890): ready
- `masshouseshot` (Chameleon.cs:22359): ready
- `masslock_ring` (Chameleon.cs:22051): ready
- `massshot` (Chameleon.cs:22396): ready
- `nattack` (Chameleon.cs:8460): needs Chameleon_nAttack, ProjectileControl
- `nattack_hit` (Chameleon.cs:8578): ready
- `perfectblend_ring` (Chameleon.cs:20595): ready
- `poisonvolley` (Chameleon.cs:23618): ready
- `quickfire_fire` (Chameleon.cs:19478): ready
- `rightstride_fire` (Chameleon.cs:28247): ready
- `rustydecay_ring` (Chameleon.cs:35780): ready
- `skinshift_ring` (Chameleon.cs:35102): ready
- `strideshot_dust` (Chameleon.cs:27317): ready
- `tailslayer_eye` (Chameleon.cs:9652): ready
- `tailslayer_fire` (Chameleon.cs:31836): ready
- `tent_destroy` (Chameleon.cs:36181): ready
- `tent_heal` (Chameleon.cs:36294): ready
- `tent_ring` (Chameleon.cs:36079): ready
- `thunderdragon_ring1` (Chameleon.cs:38276): needs BoltEmitter
- `thunderdragon_ring2` (Chameleon.cs:37992): needs ParticleSystem, ParticleSystemRenderer
- `tormentrain_fire` (Chameleon.cs:25996): needs WorldParticleCollider
- `tormentrain_ring` (Chameleon.cs:25411): ready
- `venomshock_ring` (Chameleon.cs:24213): ready
- `zephyrlore_ring` (Chameleon.cs:10848): ready
- `zeroshot_ring` (Chameleon.cs:37637): needs ParticleSystem, ParticleSystemRenderer

### mole

- `assemble_box` (Mole.cs:23086): ready
- `assemble_dust` (Mole.cs:11764): ready
- `bazooka_fire` (Mole.cs:41324): needs Mole_bazooka, ProjectileControl
- `bazooka_hit` (Mole.cs:14026): needs AlphaTimer
- `bazooka_ring` (Mole.cs:41156): needs ParticleSystem, ParticleSystemRenderer
- `bombardment_b` (Mole.cs:29996): ready
- `bombardment_fire` (Mole.cs:30418): ready
- `bombardment_g` (Mole.cs:29984): ready
- `bombardment_hit` (Mole.cs:30274): needs AlphaTimer
- `bombardment_k` (Mole.cs:30008): ready
- `bombardment_r` (Mole.cs:29972): ready
- `bombardment_signal` (Mole.cs:29668): ready
- `bombardment_w` (Mole.cs:30020): ready
- `bunker` (Mole.cs:25254): ready
- `bunker_hole` (Mole.cs:25457): ready
- `cartbomb_fire` (Mole.cs:43076): needs Mole_cartBomb
- `cartbomb_hit` (Mole.cs:14142): ready
- `cartbomb_ring` (Mole.cs:43039): ready
- `chopppercannon_ring` (Mole.cs:33707): ready
- `detonate` (Mole.cs:31113): ready
- `detonate_ring` (Mole.cs:31392): ready
- `dig_dirt` (Mole.cs:21780): ready
- `dig_dust` (Mole.cs:22241): ready
- `dig_hole` (Mole.cs:22434): ready
- `firebarrage_b` (Mole.cs:29131): ready
- `firebarrage_g` (Mole.cs:29119): ready
- `firebarrage_hit1` (Mole.cs:29000): ready
- `firebarrage_hit2` (Mole.cs:29035): ready
- `firebarrage_k` (Mole.cs:29143): ready
- `firebarrage_r` (Mole.cs:29107): ready
- `firebarrage_signal` (Mole.cs:28787): ready
- `firebarrage_w` (Mole.cs:29155): ready
- `flamecarnival` (Mole.cs:38506): needs Mole_flameCarnival
- `flamecarnival_fire` (Mole.cs:38968): needs AudioControl, rotationControl
- `flameturret` (Mole.cs:28349): ready
- `flameturret_fire` (Mole.cs:27899): ready
- `grenadecluster_fire` (Mole.cs:13800): needs Mole_grenadeCluster, ProjectileControl
- `grenadecluster_hit` (Mole.cs:13855): ready
- `megadrill_hit` (Mole.cs:13919): ready
- `megadrill_ring` (Mole.cs:39471): ready
- `megahammer` (Mole.cs:33352): ready
- `megapunch` (Mole.cs:32409): ready
- `megapunch_hit` (Mole.cs:13075): ready
- `mine1` (Mole.cs:24269): needs Mole_mine
- `mine2` (Mole.cs:24308): needs Mole_mine
- `mine3` (Mole.cs:24347): needs Mole_mine
- `mine4` (Mole.cs:24386): needs Mole_mine
- `mine_hit` (Mole.cs:10543): ready
- `minewalker_ring` (Mole.cs:45379): ready
- `mortarshot_fire` (Mole.cs:10758): needs Mole_mortarShot, ProjectileControl
- `mortarshot_hit` (Mole.cs:10818): ready
- `napalm` (Mole.cs:13727): needs Mole_napalm, ProjectileControl
- `napalm_hit` (Mole.cs:37757): ready
- `napalm_ring` (Mole.cs:37134): needs ParticleSystem, ParticleSystemRenderer
- `reload` (Mole.cs:10325): ready
- `rollermachine_hit` (Mole.cs:14083): ready
- `rollermachine_ring` (Mole.cs:42340): ready
- `sawmachine_ring` (Mole.cs:40519): ready
- `skydrill` (Mole.cs:31948): ready
- `skydrill_ring` (Mole.cs:32021): ready
- `skyshaker_ring` (Mole.cs:31986): ready
- `smartshell_hit` (Mole.cs:11503): ready
- `stungrenade` (Mole.cs:11285): needs Mole_stunGrenade, ProjectileControl
- `stunmine1` (Mole.cs:27055): needs Mole_stunMine
- `stunmine2` (Mole.cs:27094): needs Mole_stunMine
- `stunmine_hit` (Mole.cs:11040): ready
- `superdig_dust` (Mole.cs:21664): ready
- `supertnt_hit` (Mole.cs:25881): ready
- `teslacoil_ring` (Mole.cs:41723): ready
- `timenuke1` (Mole.cs:11636): needs Mole_timeNuke
- `timenuke2` (Mole.cs:11675): needs Mole_timeNuke
- `tnt` (Mole.cs:25792): ready
- `tnt_hit` (Mole.cs:25916): ready
- `warcapital` (Mole.cs:14267): needs CharacterControl, Mole_warCapital, ParticleSystem, ParticleSystemRenderer
- `warcapital_fire` (Mole.cs:44238): ready
- `warfactory_ring` (Mole.cs:40903): ready
- `warmissile` (Mole.cs:14507): needs Mole_warMissile, ProjectileControl
- `warmissile_hit` (Mole.cs:14603): ready

### monkey

- `blazingarrow` (Monkey.cs:27703): needs AlphaTimer
- `blazingform0_ring` (Monkey.cs:40318): ready
- `blazingform_fire` (Monkey.cs:39493): ready
- `blazingform_ring` (Monkey.cs:39969): ready
- `deadeffect` (Monkey.cs:52233): ready
- `earthpulse` (Monkey.cs:13094): needs Monkey_earthPulse, ProjectileControl
- `earthpulse_hit` (Monkey.cs:32806): needs AlphaTimer
- `earthpulse_ring` (Monkey.cs:32501): ready
- `earthrune_hit` (Monkey.cs:13613): needs AlphaTimer
- `earthsoul_ring` (Monkey.cs:12600): ready
- `elementalbound_ring` (Monkey.cs:15530): ready
- `fireball1` (Monkey.cs:11119): needs Monkey_fireBall, ProjectileControl
- `fireball2` (Monkey.cs:11158): needs Monkey_fireBall, ProjectileControl
- `fireball3` (Monkey.cs:11197): needs Monkey_fireBall, ProjectileControl
- `fireball4` (Monkey.cs:11236): needs Monkey_fireBall, ProjectileControl
- `fireball_hit` (Monkey.cs:11308): ready
- `firerune_hit` (Monkey.cs:12347): needs AlphaTimer
- `firesoul_ring` (Monkey.cs:11377): ready
- `flashfire` (Monkey.cs:28556): ready
- `flashfire_ring` (Monkey.cs:28814): ready
- `gadinaarmor` (Monkey.cs:40695): ready
- `gadinaarmor_create` (Monkey.cs:40758): ready
- `gadinaarmor_destroy` (Monkey.cs:14280): ready
- `gattack1_ring` (Monkey.cs:41461): ready
- `gattack2_ring` (Monkey.cs:41853): ready
- `gattack3_ring` (Monkey.cs:42387): ready
- `gattack_hit` (Monkey.cs:14211): ready
- `groundlock_hit` (Monkey.cs:31127): ready
- `instantcast` (Monkey.cs:25036): ready
- `instantcast_ring` (Monkey.cs:10966): ready
- `lavu` (Monkey.cs:13889): needs Monkey_lavu, rotationControl
- `lavu_ring` (Monkey.cs:34612): ready
- `mikeblink` (Monkey.cs:35895): ready
- `mikecircle` (Monkey.cs:21055): ready
- `nattack_hit` (Monkey.cs:10747): ready
- `pattack_ring` (Monkey.cs:38914): ready
- `phoenixarmor` (Monkey.cs:38383): ready
- `phoenixarmor_create` (Monkey.cs:38449): ready
- `phoenixarmor_destroy` (Monkey.cs:14140): ready
- `planetbreaker_ring` (Monkey.cs:31967): ready
- `runicflame` (Monkey.cs:12481): needs Monkey_runicFlame
- `runicsand` (Monkey.cs:13747): needs Monkey_runicSand
- `secondstone` (Monkey.cs:31034): ready
- `sentinalguard_ring` (Monkey.cs:42803): ready
- `stonehammer` (Monkey.cs:33523): needs AlphaTimer
- `summonsoul_ring` (Monkey.cs:24150): ready
- `upheaval` (Monkey.cs:35164): ready
- `upheaval_ring` (Monkey.cs:35389): ready
- `volcaniceruption` (Monkey.cs:43494): needs AudioControl, ParticleSystem, ParticleSystemRenderer
- `volcaniceruption_ring` (Monkey.cs:43457): ready
- `worldignition` (Monkey.cs:30309): needs AlphaTimer

### panda

- `ashurafist` (Panda.cs:29770): ready
- `ashuraring` (Panda.cs:30498): ready
- `aurablast` (Panda.cs:18450): needs AlphaTimer
- `aurafield_ring` (Panda.cs:19072): ready
- `cattack_ring` (Panda.cs:19034): ready
- `climbingcliff_hit` (Panda.cs:8747): ready
- `climbingcliff_ring` (Panda.cs:27699): needs AlphaTimer
- `combolink_ring` (Panda.cs:40690): ready
- `crushingmonolith` (Panda.cs:28525): needs AlphaTimer
- `crushingmonolith_hit` (Panda.cs:9781): ready
- `deadeffect` (Panda.cs:50719): ready
- `deathblow` (Panda.cs:35027): ready
- `deathblow_ring` (Panda.cs:35545): ready
- `delayqi_fire` (Panda.cs:23759): ready
- `delayqi_ring` (Panda.cs:24217): ready
- `drunkenfist` (Panda.cs:31668): ready
- `drunkenspin` (Panda.cs:31633): ready
- `fuujinken_hit` (Panda.cs:9838): ready
- `fuujinken_ring1` (Panda.cs:41267): ready
- `fuujinken_ring2` (Panda.cs:40928): needs AlphaTimer, AudioControl
- `fuujinken_ring3` (Panda.cs:41312): ready
- `heavenpalm` (Panda.cs:9529): ready
- `heavenpalm_ring` (Panda.cs:40294): ready
- `lotuspalm` (Panda.cs:9479): ready
- `lotuspalm_ring` (Panda.cs:39465): ready
- `mysticsage_hit` (Panda.cs:9583): needs AlphaTimer
- `nattack_hit1` (Panda.cs:8007): ready
- `nattack_hit2` (Panda.cs:8093): ready
- `nattack_punch` (Panda.cs:15271): ready
- `nattack_wheel` (Panda.cs:16927): ready
- `psalmofenergy_ring` (Panda.cs:10249): ready
- `pummel_dust` (Panda.cs:25033): ready
- `pummel_hit` (Panda.cs:8576): ready
- `pummel_ogre` (Panda.cs:24492): needs AlphaTimer
- `pummel_ogrearm1` (Panda.cs:24553): needs AlphaTimer
- `pummel_ogrearm2` (Panda.cs:24589): needs AlphaTimer
- `qiburst` (Panda.cs:23798): needs AlphaTimer
- `qistrike` (Panda.cs:23833): ready
- `qistrike_hit` (Panda.cs:8519): ready
- `qistrike_ring` (Panda.cs:23247): ready
- `raijinken_hit` (Panda.cs:42515): needs AlphaTimer, BoltEmitter, ParticleSystem, ParticleSystemRenderer
- `raijinken_ring1` (Panda.cs:42181): ready
- `raijinken_ring2` (Panda.cs:41928): ready
- `rainstorm` (Panda.cs:38305): ready
- `risingdragon` (Panda.cs:29665): ready
- `risingdragon_hit` (Panda.cs:8932): ready
- `risingdragon_ring` (Panda.cs:29509): ready
- `risingvortex` (Panda.cs:29251): ready
- `risingvortex_hit` (Panda.cs:8882): ready
- `rollaround_ring` (Panda.cs:20624): ready
- `rushingfalcon` (Panda.cs:22711): ready
- `rushingfalcon_hit` (Panda.cs:8462): ready
- `safeguard_hit` (Panda.cs:9737): ready
- `sptransfer` (Panda.cs:36062): needs BoltEmitter
- `stasisblow` (Panda.cs:34212): ready
- `stasisblow_enddust` (Panda.cs:34464): ready
- `stasisblow_ring` (Panda.cs:34727): ready
- `threestep` (Panda.cs:21716): ready
- `threestep_hit` (Panda.cs:8412): ready
- `tigerpounce_hit` (Panda.cs:8690): ready
- `tigertoss` (Panda.cs:26621): ready
- `timeandtidecrane` (Panda.cs:33804): ready
- `timeandtidemonkey` (Panda.cs:33237): needs AlphaTimer
- `towerrush_hit` (Panda.cs:8626): ready
- `towerrush_ogre` (Panda.cs:25383): needs AlphaTimer
- `towerrush_ring` (Panda.cs:25756): ready
- `watercrane` (Panda.cs:33841): ready
- `watercrane_hit` (Panda.cs:9088): ready
- `watermonkey` (Panda.cs:33272): ready
- `watermonkey_hit` (Panda.cs:9038): ready
- `windcloud` (Panda.cs:36687): ready

### penguin

- `absolutezero` (Penguin.cs:33844): needs AlphaTimer
- `arcticemperor` (Penguin.cs:35042): needs Penguin_arcticEmperor
- `arcticwind` (Penguin.cs:30766): ready
- `astralshift_ring` (Penguin.cs:12805): ready
- `blink` (Penguin.cs:22817): ready
- `blink_ring` (Penguin.cs:23034): ready
- `blizzard` (Penguin.cs:34430): ready
- `cattack_ring` (Penguin.cs:18593): ready
- `cosmicfriday` (Penguin.cs:39256): needs Penguin_cosmicFriday
- `cosmicfriday_ring` (Penguin.cs:39219): ready
- `cosmicrift_ring` (Penguin.cs:38736): ready
- `deadlyfrost` (Penguin.cs:30739): ready
- `dispell` (Penguin.cs:22289): ready
- `fallingcomet` (Penguin.cs:26881): ready
- `fallingstar` (Penguin.cs:25871): ready
- `fallingstar_ring` (Penguin.cs:25563): ready
- `focusintellect_ring` (Penguin.cs:35969): ready
- `frostspike_ring` (Penguin.cs:37883): needs AlphaTimer
- `frozenblast` (Penguin.cs:29677): ready
- `frozenbreak` (Penguin.cs:29631): ready
- `giantcomet` (Penguin.cs:37615): ready
- `giantstar` (Penguin.cs:37328): ready
- `iceblock` (Penguin.cs:10716): needs Penguin_iceBlock
- `manaarc` (Penguin.cs:21821): ready
- `manaburn` (Penguin.cs:24795): ready
- `manafield_ring` (Penguin.cs:18558): ready
- `manapool_hit` (Penguin.cs:10562): ready
- `manasurge` (Penguin.cs:24758): ready
- `meteora` (Penguin.cs:28348): ready
- `meteora_hit` (Penguin.cs:28412): ready
- `meteora_ring` (Penguin.cs:28521): ready
- `mptransfer` (Penguin.cs:23488): ready
- `mptransfer_ring` (Penguin.cs:23651): ready
- `multicast` (Penguin.cs:9838): ready
- `parallelshift` (Penguin.cs:36642): ready
- `parallelshift_ring` (Penguin.cs:36854): ready
- `penguinofarc` (Penguin.cs:21786): ready
- `snowball_cast` (Penguin.cs:38253): ready
- `snowman_ring` (Penguin.cs:32319): ready
- `spreadshot_fire` (Penguin.cs:11486): needs Penguin_nAttack, ProjectileControl
- `tornado1` (Penguin.cs:10897): needs Penguin_tornado
- `tornado2` (Penguin.cs:10936): needs Penguin_tornado
- `tornado3` (Penguin.cs:10975): needs Penguin_tornado
- `tornado_hit` (Penguin.cs:10802): ready
- `tornado_ring` (Penguin.cs:10857): ready
- `typhoon1` (Penguin.cs:11170): needs Penguin_typhoon
- `typhoon2` (Penguin.cs:11209): needs Penguin_typhoon
- `typhoon3` (Penguin.cs:11248): needs Penguin_typhoon

### rabbit

- `acidicfield` (Rabbit.cs:10119): needs Rabbit_acidicField
- `acidicfield_fire` (Rabbit.cs:10172): ready
- `allhpdrug1` (Rabbit.cs:45475): ready
- `allkodrug1` (Rabbit.cs:45581): ready
- `allmpdrug1` (Rabbit.cs:45509): ready
- `allspdrug1` (Rabbit.cs:45543): ready
- `backpack_hit` (Rabbit.cs:10707): ready
- `backpack_ring` (Rabbit.cs:31078): ready
- `bigbag_ring` (Rabbit.cs:31041): ready
- `boostshot` (Rabbit.cs:10265): ready
- `bounce1` (Rabbit.cs:21019): ready
- `bounce2` (Rabbit.cs:21865): ready
- `bouncingbullet` (Rabbit.cs:18097): ready
- `bouncingbullet_hit` (Rabbit.cs:18135): ready
- `cast_ring` (Rabbit.cs:23855): ready
- `cattack_charge` (Rabbit.cs:18988): ready
- `cattack_fire` (Rabbit.cs:19354): ready
- `cattack_hit` (Rabbit.cs:9391): ready
- `circleshot` (Rabbit.cs:32909): ready
- `circleshot_ring` (Rabbit.cs:33072): ready
- `contract_create` (Rabbit.cs:11695): ready
- `contract_flag` (Rabbit.cs:40696): ready
- `diamondshot_fire` (Rabbit.cs:38214): ready
- `diamondshot_hit` (Rabbit.cs:11405): ready
- `diamondshot_ring` (Rabbit.cs:38544): ready
- `extravagance_ring` (Rabbit.cs:40021): needs ParticleSystem, ParticleSystemRenderer
- `fourshot_fire` (Rabbit.cs:32314): ready
- `fromtheabove_ring` (Rabbit.cs:21830): ready
- `gilshot_fire` (Rabbit.cs:30320): ready
- `gilshot_hit` (Rabbit.cs:10502): ready
- `gilshot_ring` (Rabbit.cs:30726): ready
- `gorgonshot_fire` (Rabbit.cs:29605): needs AlphaTimer
- `gorgonshot_hit` (Rabbit.cs:10452): ready
- `gorgonshot_ring` (Rabbit.cs:29974): ready
- `healingfield` (Rabbit.cs:11295): needs Rabbit_healingField
- `healingfield_fire` (Rabbit.cs:11355): ready
- `heatshot` (Rabbit.cs:10308): ready
- `hppot1` (Rabbit.cs:24375): needs Rabbit_potion
- `hppot2` (Rabbit.cs:24414): needs Rabbit_potion
- `hppot3` (Rabbit.cs:24453): needs Rabbit_potion
- `hppot4` (Rabbit.cs:24492): needs Rabbit_potion
- `hppot_hit` (Rabbit.cs:9964): ready
- `immuneshot` (Rabbit.cs:10222): ready
- `lifeshot` (Rabbit.cs:10351): ready
- `maimshot_fire` (Rabbit.cs:23144): ready
- `maimshot_hit` (Rabbit.cs:9639): ready
- `medicalshot_fire` (Rabbit.cs:27821): ready
- `medicalshot_ring` (Rabbit.cs:27591): ready
- `millionaire1` (Rabbit.cs:37116): needs WorldParticleCollider
- `millionaire2` (Rabbit.cs:37153): needs WorldParticleCollider
- `millionaire_peppon` (Rabbit.cs:37473): needs AlphaTimer
- `millionaire_ring` (Rabbit.cs:36909): ready
- `mppot_hit` (Rabbit.cs:9880): ready
- `nattack_fire` (Rabbit.cs:17537): ready
- `nattack_hit` (Rabbit.cs:9125): ready
- `randompot1` (Rabbit.cs:26173): needs Rabbit_potion
- `randompot2` (Rabbit.cs:26204): needs Rabbit_potion
- `randompot3` (Rabbit.cs:26235): needs Rabbit_potion
- `randompot4` (Rabbit.cs:26266): needs Rabbit_potion
- `randompot5` (Rabbit.cs:26297): needs Rabbit_potion
- `randompot6` (Rabbit.cs:26328): needs Rabbit_potion
- `rapidtrance_potion` (Rabbit.cs:28987): ready
- `rapidtrance_ring` (Rabbit.cs:29062): ready
- `replenishment_ring` (Rabbit.cs:12843): ready
- `shootingarray_finalhit` (Rabbit.cs:11007): ready
- `shootingarray_fire` (Rabbit.cs:35184): ready
- `shootingarray_hit` (Rabbit.cs:10964): ready
- `shootingarray_ring` (Rabbit.cs:35793): ready
- `shotgun_fire` (Rabbit.cs:36211): ready
- `shotgun_hit` (Rabbit.cs:11057): ready
- `snipercamera` (Rabbit.cs:18660): needs Rabbit_sniperCamera
- `sppot1` (Rabbit.cs:25246): needs Rabbit_potion
- `sppot2` (Rabbit.cs:25285): needs Rabbit_potion
- `sppot3` (Rabbit.cs:25324): needs Rabbit_potion
- `sppot_hit` (Rabbit.cs:9918): ready
- `statscan` (Rabbit.cs:22512): needs AlphaTimer
- `statscan_dust` (Rabbit.cs:22545): ready
- `stickygum` (Rabbit.cs:10045): needs Rabbit_stickyGum
- `tenshot_fire` (Rabbit.cs:39437): ready
- `tenshot_ring` (Rabbit.cs:39112): ready
- `trucetrading_fail` (Rabbit.cs:34859): ready
- `trucetrading_flag` (Rabbit.cs:34295): ready
- `trucetrading_ring` (Rabbit.cs:34263): ready
- `trucetrading_success` (Rabbit.cs:34755): ready

### sheep

- `blueseal` (Sheep.cs:32226): ready
- `bookbash_hit` (Sheep.cs:11814): ready
- `bookbash_ring1` (Sheep.cs:37543): ready
- `bookbash_ring2` (Sheep.cs:37658): ready
- `bookbash_ring3` (Sheep.cs:37769): ready
- `cattack` (Sheep.cs:9819): needs ProjectileControl, Sheep_cAttack
- `cattack_charge` (Sheep.cs:18698): ready
- `cattack_hit` (Sheep.cs:9915): ready
- `cattack_ring` (Sheep.cs:18730): ready
- `cleanse` (Sheep.cs:25343): ready
- `clear` (Sheep.cs:24849): ready
- `deadeffect` (Sheep.cs:46903): ready
- `divinechannel_ring` (Sheep.cs:40167): ready
- `divinityaxe` (Sheep.cs:36690): needs AlphaTimer
- `divinityaxe_hit` (Sheep.cs:11757): ready
- `divinityspear` (Sheep.cs:10752): needs AlphaTimer
- `divinityspear_ring` (Sheep.cs:31886): ready
- `divinitysword` (Sheep.cs:31107): needs AlphaTimer
- `edensanctuary` (Sheep.cs:37123): needs AlphaTimer, Sheep_edenSanctuary
- `edensanctuary_ring` (Sheep.cs:37087): ready
- `freecast` (Sheep.cs:10157): ready
- `heal` (Sheep.cs:22248): ready
- `holylight` (Sheep.cs:27863): ready
- `holylight_ring` (Sheep.cs:28100): ready
- `hominglight` (Sheep.cs:11445): needs ProjectileControl, Sheep_homingLight
- `illuminate` (Sheep.cs:29372): ready
- `koheal` (Sheep.cs:10334): ready
- `lullaby_ring` (Sheep.cs:35696): needs AlphaTimer
- `nattack` (Sheep.cs:9316): needs ProjectileControl, Sheep_nAttack
- `nattack_hit` (Sheep.cs:9409): ready
- `overheal` (Sheep.cs:26293): ready
- `overheal_ring` (Sheep.cs:21172): ready
- `pacify` (Sheep.cs:23760): ready
- `purifyingtear_ring` (Sheep.cs:34841): ready
- `quickheal` (Sheep.cs:10369): ready
- `radiantheal` (Sheep.cs:22213): ready
- `redseal` (Sheep.cs:32191): ready
- `returncast` (Sheep.cs:11651): ready
- `revert` (Sheep.cs:27339): ready
- `revive` (Sheep.cs:26829): ready
- `sealofattack` (Sheep.cs:10822): needs Sheep_seal
- `sealofdefense` (Sheep.cs:10958): needs Sheep_seal
- `sealofearth` (Sheep.cs:11100): needs Sheep_seal
- `sealofheaven` (Sheep.cs:11243): needs Sheep_seal
- `sleep` (Sheep.cs:24347): ready
- `soulofarms` (Sheep.cs:34106): needs AlphaTimer
- `soulofarms_ring` (Sheep.cs:33999): ready
- `soulofarms_trail` (Sheep.cs:34031): ready
- `whiteburst_hit` (Sheep.cs:11577): ready
- `worldencarta_hit` (Sheep.cs:11871): ready
- `worldencarta_ring` (Sheep.cs:38322): ready

### whale

- `asunderimpale` (Whale.cs:27157): ready
- `asunderround` (Whale.cs:28013): ready
- `bowlingwhale` (Whale.cs:36680): needs AlphaTimer, AudioControl, UVScroll
- `bowlingwhale_ring` (Whale.cs:37128): ready
- `bubbleburst` (Whale.cs:35943): ready
- `bubbleburst_ring` (Whale.cs:35768): ready
- `bubbleshield_cast` (Whale.cs:29688): ready
- `calltoarm_ring` (Whale.cs:33314): ready
- `castring` (Whale.cs:20409): ready
- `deadeffect` (Whale.cs:46461): ready
- `divingwave` (Whale.cs:31865): ready
- `extendedwave1` (Whale.cs:16554): ready
- `extendedwave2` (Whale.cs:16850): ready
- `extendedwave3` (Whale.cs:18045): ready
- `flyingshield` (Whale.cs:24795): needs Whale_flyingShield
- `flyingshield_hit` (Whale.cs:8955): ready
- `gobbleup_hit` (Whale.cs:9072): ready
- `gobbleup_ring` (Whale.cs:26461): ready
- `grandtide` (Whale.cs:37424): needs ParticleSystem, ParticleSystemRenderer
- `grandtide_ring` (Whale.cs:37896): ready
- `homingshield` (Whale.cs:10401): needs Whale_homingShield
- `hydroblast` (Whale.cs:10037): ready
- `javelin` (Whale.cs:8781): needs ProjectileControl, Whale_javelin
- `kingdomknight1` (Whale.cs:28433): needs whale_kingdomKnight
- `kingdomknight2` (Whale.cs:28468): needs whale_kingdomKnight
- `kingdomknight_ring1` (Whale.cs:28755): ready
- `malstorm` (Whale.cs:32480): ready
- `malstorm_bolt` (Whale.cs:10188): needs BoltEmitter
- `megalodon` (Whale.cs:34790): ready
- `megalodon_ring` (Whale.cs:34744): ready
- `nattack_hit` (Whale.cs:8303): ready
- `peninsulaimpale` (Whale.cs:27219): ready
- `peninsulaimpale_ring` (Whale.cs:27389): ready
- `peninsularound` (Whale.cs:28048): ready
- `peninsularound_ring` (Whale.cs:27957): ready
- `rejuvenate` (Whale.cs:31310): ready
- `revitalize_ring` (Whale.cs:36455): ready
- `roundtable_ring` (Whale.cs:29251): ready
- `salvation_ring` (Whale.cs:33689): ready
- `seaaegis_ring` (Whale.cs:11109): ready
- `shieldbash_hit` (Whale.cs:8688): ready
- `shieldbash_ring` (Whale.cs:19811): ready
- `shieldrush_hit` (Whale.cs:8905): ready
- `shieldrush_ring` (Whale.cs:24190): ready
- `spiralblast` (Whale.cs:9997): ready
- `swallow_hit` (Whale.cs:9020): ready
- `swallow_ring` (Whale.cs:25666): ready
- `sweep_ring` (Whale.cs:22438): ready
- `tidecutter_ring` (Whale.cs:22309): ready
- `wallpuncture_hit` (Whale.cs:9247): ready
- `whalewave` (Whale.cs:31900): ready

### wolf

- `armorbreak1` (Wolf.cs:22598): ready
- `armorbreak2` (Wolf.cs:22633): ready
- `armorbreak_ring` (Wolf.cs:22966): ready
- `artbreaker_hit` (Wolf.cs:9175): ready
- `artbreaker_ring` (Wolf.cs:34291): ready
- `artcancel_ring` (Wolf.cs:27791): ready
- `artcancel_slide` (Wolf.cs:27759): ready
- `bladefang_ring` (Wolf.cs:26598): ready
- `bladefang_underslash` (Wolf.cs:25658): ready
- `bladefang_upperslash` (Wolf.cs:25871): ready
- `bladesong` (Wolf.cs:29963): ready
- `bladesong_finalblade` (Wolf.cs:30095): ready
- `bladesong_ring` (Wolf.cs:29857): ready
- `bloodfang_underslash` (Wolf.cs:25695): ready
- `bloodfang_upperslash` (Wolf.cs:25906): ready
- `bravespirit` (Wolf.cs:20357): ready
- `cattack1_ring` (Wolf.cs:18976): ready
- `cattack1_ring1` (Wolf.cs:19160): ready
- `cattack1_ring2` (Wolf.cs:19116): ready
- `cattack1_ring3` (Wolf.cs:19068): ready
- `cattack2` (Wolf.cs:19403): ready
- `crossbreak` (Wolf.cs:23884): ready
- `crossbreak_ring` (Wolf.cs:23736): ready
- `crusader` (Wolf.cs:21085): ready
- `crusader_hit` (Wolf.cs:8492): needs Light
- `crusader_ring` (Wolf.cs:21516): ready
- `darkedge1` (Wolf.cs:15091): ready
- `darkedge2` (Wolf.cs:17682): ready
- `darkedge_ring` (Wolf.cs:30731): ready
- `deadeffect` (Wolf.cs:46037): ready
- `doubleart` (Wolf.cs:18411): ready
- `dualbrand_hit` (Wolf.cs:9325): ready
- `dualbrand_ring` (Wolf.cs:36807): ready
- `dualbrand_slash1` (Wolf.cs:35947): ready
- `dualbrand_slash2` (Wolf.cs:36107): ready
- `dualbrand_slash3` (Wolf.cs:36262): ready
- `dualbrand_slash4` (Wolf.cs:36412): ready
- `feralassault_hit` (Wolf.cs:9275): ready
- `feralassault_ring1` (Wolf.cs:35463): ready
- `feralassault_ring2` (Wolf.cs:35219): ready
- `feralassault_ring3` (Wolf.cs:35515): ready
- `feralstrike` (Wolf.cs:29106): ready
- `feralstrike_hit` (Wolf.cs:8873): ready
- `feralstrike_ring` (Wolf.cs:29585): ready
- `gloriousspirit` (Wolf.cs:20394): ready
- `grandcross` (Wolf.cs:24439): ready
- `grandcross_mark` (Wolf.cs:8615): ready
- `grandcross_ring` (Wolf.cs:24743): ready
- `holyarmor_ring` (Wolf.cs:33721): ready
- `holysword_ring` (Wolf.cs:33206): ready
- `lawbringer` (Wolf.cs:21048): ready
- `lawbringer_hit` (Wolf.cs:8457): needs Light
- `lawbringer_ring` (Wolf.cs:21387): ready
- `mirrorblade_hit` (Wolf.cs:9225): ready
- `mirrorblade_mirror` (Wolf.cs:34562): ready
- `mirrorblade_ring` (Wolf.cs:34962): ready
- `obsidianfang_hit` (Wolf.cs:9575): ready
- `powerbreak1` (Wolf.cs:22233): ready
- `powerbreak2` (Wolf.cs:22268): ready
- `resurrection_hit` (Wolf.cs:25114): ready
- `resurrection_ring` (Wolf.cs:25390): ready
- `secondwind` (Wolf.cs:23221): ready
- `skyslasher` (Wolf.cs:31697): ready
- `skyslasher_ring` (Wolf.cs:19020): ready
- `sublimeart_ring` (Wolf.cs:18449): ready
- `thirdrend_ring` (Wolf.cs:32659): ready
- `twinresonance_fire` (Wolf.cs:37590): ready
- `twinresonance_hit` (Wolf.cs:9425): ready
- `twinresonance_ring` (Wolf.cs:37343): ready

