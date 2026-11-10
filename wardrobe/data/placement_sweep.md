# Wearable placement sweep (TTO rules, per class)

Rule (TTO1102 code): the class + item-code entry, else the class fallback; weapons' second hand is `<Class>#2`.
Source: `wardrobe/data/placements.json` (TTO's Config/*Placement tables) + `icons.json` (code -> model).

## Summary (items per class: entry / class fallback / inferred)

| class | trinkets | headpieces | weapons |
|---|---|---|---|
| bat | 24 / 16 / 2 | 5 / 57 / 0 | 0 / 49 / 0 |
| bison | 25 / 15 / 2 | 5 / 55 / 0 | 0 / 46 / 0 |
| cat | 26 / 16 / 2 | 5 / 60 / 0 | 2 / 42 / 0 |
| chameleon | 25 / 15 / 2 | 14 / 48 / 0 | 0 / 90 / 0 |
| mole | 25 / 15 / 2 | 5 / 58 / 0 | 0 / 44 / 0 |
| monkey | 27 / 15 / 2 | 5 / 58 / 0 | 0 / 43 / 0 |
| panda | 29 / 16 / 2 | 5 / 56 / 0 | 0 / 85 / 0 |
| penguin | 26 / 15 / 2 | 26 / 37 / 0 | 0 / 45 / 0 |
| rabbit | 26 / 16 / 2 | 5 / 60 / 0 | 0 / 44 / 0 |
| sheep | 26 / 16 / 2 | 5 / 57 / 0 | 3 / 44 / 0 |
| whale | 25 / 16 / 2 | 5 / 55 / 0 | 0 / 86 / 0 |
| wolf | 25 / 16 / 2 | 5 / 57 / 0 | 0 / 46 / 0 |

## Every item

| class | kind | item | codes | placed by | bone | pos | scale |
|---|---|---|---|---|---|---|---|
| bat | trinkets | bell | t_fem2 | entry | Spine1 | -0,0,0 | 1.0 |
| bat | trinkets | bugAntenna | t_all6 | class fallback | Head | -0,0,0 | 1.0 |
| bat | trinkets | championFlag1 | t_all71 | entry | Spine2 | -0,0,0 | 1.0 |
| bat | trinkets | championFlag2 | t_all72 | entry | Spine2 | -0,0,0 | 1.0 |
| bat | trinkets | championFlag3 | t_all73 | entry | Spine2 | -0,0,0 | 1.0 |
| bat | trinkets | championFlag4 | t_all74 | entry | Spine2 | -0,0,0 | 1.0 |
| bat | trinkets | chineseLantern | t_fem37 | entry | Spine1 | -0,0,0 | 1.0 |
| bat | trinkets | chineseTalisman |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| bat | trinkets | chineseTalismanR | t_fem31 | class fallback | Head | -0,0,0 | 1.0 |
| bat | trinkets | deerHorn | t_fem15 | class fallback | Head | -0,0,0 | 1.0 |
| bat | trinkets | doubleHorn | t_all66 | class fallback | Head | -0,0,0 | 1.0 |
| bat | trinkets | frozenMask | t_fem56 | class fallback | Head | -0,0,0 | 1.0 |
| bat | trinkets | glasses | t_all1 | class fallback | Head | -0,0,0 | 1.0 |
| bat | trinkets | groceryBag | t_all46 | entry | Hand_R | -0,0,0 | 1.0 |
| bat | trinkets | lollipop | t_all9 | class fallback | Head | -0,0,0 | 1.0 |
| bat | trinkets | magazine | t_fem11 | entry | mount_Hand_R | -0,0,0 | 1.0 |
| bat | trinkets | maohWings | t_fem46 | entry | Spine1 | -0,0,0 | 1.0 |
| bat | trinkets | nerdGlasses | t_all4 | class fallback | Head | -0,0,0 | 1.0 |
| bat | trinkets | partyWhistle | t_all7 | class fallback | Head | -0,0,0 | 1.0 |
| bat | trinkets | poseidonTrinket | t_fem66 | entry | Spine1 | -0,0,0 | 1.0 |
| bat | trinkets | quotationFlag |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| bat | trinkets | redNose | t_all8 | class fallback | Head | -0,0,0 | 1.0 |
| bat | trinkets | starGlasses | t_all3 | class fallback | Head | -0,0,0 | 1.0 |
| bat | trinkets | sunGlasses | t_all2 | class fallback | Head | -0,0,0 | 1.0 |
| bat | trinkets | AngleWing | t_all110 | entry | Head | 0.254,0.072,0.001 | 0.5 |
| bat | trinkets | AngleWing_Crimson | t_allhlw6 | entry | Head | 0.254,0.072,0.001 | 0.5 |
| bat | trinkets | AngleWing_Ghost | t_allhlw7 | entry | Head | 0.254,0.072,0.001 | 0.5 |
| bat | trinkets | AngleWing_Pumpkin | t_allhlw8 | entry | Head | 0.254,0.072,0.001 | 0.5 |
| bat | trinkets | AngleWing_Spectral | t_allhlw9 | entry | Head | 0.254,0.072,0.001 | 0.5 |
| bat | trinkets | aura_bloodmoon | t_all186 | class fallback | Head | -0,0,0 | 1.0 |
| bat | trinkets | aura_undeadqueen | t_all185 | class fallback | Head | -0,0,0 | 1.0 |
| bat | trinkets | Azure_Wing | t_all101 | entry | Head | 0.25,0.25,0 | 0.5 |
| bat | trinkets | championWing |  | inferred (Shade Wing's entry) | Head | 0.25,0.25,0 | 0.5 |
| bat | trinkets | daynightwing | t_all102 | entry | Head | 0.25,0.25,0 | 1.0 |
| bat | trinkets | devilWing |  | inferred (Shade Wing's entry) | Head | 0.25,0.25,0 | 0.5 |
| bat | trinkets | Ice_Wing | t_all77 | entry | Head | 0.25,0.25,0 | 0.5 |
| bat | trinkets | MoonlightRabbit | t_all142 | entry | Head | 0.2,0.25,0 | 0.5 |
| bat | trinkets | PumpkonHeadband | t_allhlw3 | entry | Spine2 | -0.0429,0.1769,-0.0006 | 0.3799999952316284 |
| bat | trinkets | ReaperTrinket | t_allhlw5 | entry | Spine2 | -0.333678,0.306938,0.148417 | 0.8892660737037659 |
| bat | trinkets | Shade_Wing | t_all78 | entry | Head | 0.25,0.25,0 | 0.5 |
| bat | trinkets | WhiteWing | t_all188 | entry | Head | 0.2527,0.1263,0.0008 | 0.5 |
| bat | trinkets | WitchyWing | t_all147 | entry | Head | 0.15,0.25,0 | 0.5 |
| bat | accessories | afro | c_all11 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | afroC | c_all12 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | artistHat | c_all39 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | butterflyHood | c_bat47 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | butterflyHoodR | c_bat48 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | cakeHat | c_all9 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | candyHat | c_all10 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | championHelmet | c_all58 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | dreamBand | c_bat32 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | dreamBandR | c_bat34 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | dreamBandV | c_bat38 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | earmuff1 | c_all21 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | earmuff2 | c_all22 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | fanKingHat | c_all38 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | fanKingHat_Shine |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| bat | accessories | flowerBand | c_fem11 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | frozenCrown | c_all56 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | hallowCrown | c_bat35,c_bat51 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | halloweenHat | c_bat37 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | halo | c_all18 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | headphone1 | c_all23 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | headphone2 | c_all24 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | headphone3 | c_all25 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | horn | c_all19 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | illusionMask | c_bat22 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | illusionMaskR | c_bat24 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | japanSakura | c_bat65 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | krathongHat1 | c_all27 | entry | Head | -0,0,0 | 1.0 |
| bat | accessories | krathongHat2 | c_all28 | entry | Head | -0,0,0 | 1.0 |
| bat | accessories | legendHelmet | c_bat60,c_bat61 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | lionHead | c_fem37 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | lizaHood | c_bat36 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | mummyHead | c_all46 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | paperHat | c_all3 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | partyHatB | c_all7 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | partyHatR | c_all8 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | pirateBandana | c_all16 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | pirateBandanaR | c_all26 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | poseidonHelmet | c_all66 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | pvpHelmet | c_all43 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | pvpHelmetR | c_all44 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | queenCrown | c_bat40 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | queenCrownR | c_bat41 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | queenCrownV | c_bat42 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | quizHat | c_all37 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | redPandaHat | c_all1 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | royalCirclet | c_bat50 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | royalCircletR | c_bat52 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | santaHat | c_all15 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | shadowHat | c_bat31 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | shadowHatR | c_bat33 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | showerCap | c_bat5 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | snowmanHead | c_all29 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | starGlasses | c_bat45 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | summerHat | c_bat15 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | teacherHat | c_bat25 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | veggieHat | c_bat19 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | warlockHood | c_bat21 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | warlockHoodR | c_bat23 | class fallback | Head | -0,0,0 | 1.0 |
| bat | accessories | CactonHeadband | c_allhlw1 | entry | Head | 0.0414,-0.0585,0.0025 | 0.3621000051498413 |
| bat | accessories | ChopperTrinket | c_allhlw4 | entry | Wing2_R | 0.3465,0.0821,0.0446 | 0.3961000144481659 |
| bat | accessories | CoconHeadband | c_allhlw2 | entry | Head | 0.0661,-0.04,0.0019 | 0.3499999940395355 |
| bat | weapons | bathBrush | w_bat5 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | batWand | w_bat15 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | bdWeapon | w_bat19 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | butterflyWand | w_bat47 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | butterflyWandR | w_bat48 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | championRapier | w_bat58 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | commonWand | w_bat2 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | dreamWand | w_bat32 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | dreamWandR | w_bat34 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | dreamWandV | w_bat38 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | eclipseWand | w_bat79 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | flamingBaton | w_bat82 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | flamingLance | w_bat84 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | flamingRod | w_bat83 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | flamingWand | w_bat81 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | frozenWand | w_bat56 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | goldenWand | w_bat49 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | hallowCandle | w_bat35 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | halloweenWand | w_bat37 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | heartWand | w_bat14 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | illusionWand | w_bat22 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | illusionWandR | w_bat24 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | japanWagasa | w_bat65 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | legendWand | w_bat60 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | lizaWhip | w_bat36 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | mummyWand | w_bat46 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | noviceWand | w_bat1 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | pandaQuill |  | class fallback (no code) | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | paperWand | w_bat3 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | pinkLatern | w_bat39 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | poseidonWand | w_bat10,w_bat66 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | pvpWand | w_bat43 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | pvpWandR | w_bat44 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | queenWand | w_bat40 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | queenWandR | w_bat41 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | queenWandV | w_bat42 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | royalWand | w_bat50 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | royalWandR | w_bat52 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | shadowWand | w_bat31 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | shadowWandR | w_bat33,w_bat61 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | specialWand |  | class fallback (no code) | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | standardWand | w_bat51 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | standardWandR | w_bat11 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | standardWandV | w_bat12 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | starMicrophone | w_bat45 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | teacherStick | w_bat25 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | timeWand | w_bat69 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | warlockWand | w_bat21 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bat | weapons | warlockWandR | w_bat23 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| bison | trinkets | bugAntenna | t_all6 | class fallback | Head | -0,0,0 | 1.0 |
| bison | trinkets | championFlag1 | t_all71 | entry | Spine2 | -0,0,0 | 1.0 |
| bison | trinkets | championFlag2 | t_all72 | entry | Spine2 | -0,0,0 | 1.0 |
| bison | trinkets | championFlag3 | t_all73 | entry | Spine2 | -0,0,0 | 1.0 |
| bison | trinkets | championFlag4 | t_all74 | entry | Spine2 | -0,0,0 | 1.0 |
| bison | trinkets | chineseLantern | t_mal37 | entry | Spine2 | -0,0,0 | 1.0 |
| bison | trinkets | chineseTalisman | t_mal31 | class fallback | Head | -0,0,0 | 1.0 |
| bison | trinkets | chineseTalismanR |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| bison | trinkets | comic | t_mal11 | entry | HandMount_L | -0,0,0 | 1.0 |
| bison | trinkets | curseAnkh | t_mal46 | class fallback | Head | -0,0,0 | 1.0 |
| bison | trinkets | doubleHorn | t_all66 | class fallback | Head | -0,0,0 | 1.0 |
| bison | trinkets | frozenWing | t_mal56 | entry | Spine2 | -0,0,0 | 1.0 |
| bison | trinkets | glasses | t_all1 | class fallback | Head | -0,0,0 | 1.0 |
| bison | trinkets | groceryBag | t_all46 | entry | Hand_L | -0,0,0 | 1.5 |
| bison | trinkets | legendTrinket | t_bsn60 | entry | Spine1 | -0,0,0 | 1.0 |
| bison | trinkets | lollipop | t_all9 | class fallback | Head | -0,0,0 | 1.0 |
| bison | trinkets | nerdGlasses | t_all4 | class fallback | Head | -0,0,0 | 1.0 |
| bison | trinkets | partyWhistle | t_all7 | class fallback | Head | -0,0,0 | 1.0 |
| bison | trinkets | poseidonTrinket | t_mal66 | entry | Spine2 | -0,0,0 | 1.0 |
| bison | trinkets | quotationFlag |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| bison | trinkets | redNose | t_all8 | class fallback | Head | -0,0,0 | 1.0 |
| bison | trinkets | santaBag | t_mal15 | entry | Spine1 | -0,0,0 | 1.0 |
| bison | trinkets | starGlasses | t_all3 | class fallback | Head | -0,0,0 | 1.0 |
| bison | trinkets | sunGlasses | t_all2 | class fallback | Head | -0,0,0 | 1.0 |
| bison | trinkets | AngleWing | t_all110 | entry | Spine1 | 0.728,0.8196,-0.0005 | 1.5 |
| bison | trinkets | AngleWing_Crimson | t_allhlw6 | entry | Spine1 | 0.728,0.8196,-0.0005 | 1.5 |
| bison | trinkets | AngleWing_Ghost | t_allhlw7 | entry | Spine1 | 0.728,0.8196,-0.0005 | 1.5 |
| bison | trinkets | AngleWing_Pumpkin | t_allhlw8 | entry | Spine1 | 0.728,0.8196,-0.0005 | 1.5 |
| bison | trinkets | AngleWing_Spectral | t_allhlw9 | entry | Spine1 | 0.728,0.8196,-0.0005 | 1.5 |
| bison | trinkets | aura_bloodmoon | t_all186 | class fallback | Head | -0,0,0 | 1.0 |
| bison | trinkets | aura_undeadqueen | t_all185 | class fallback | Head | -0,0,0 | 1.0 |
| bison | trinkets | Azure_Wing | t_all101 | entry | Spine1 | 0.5,0.75,0 | 1.5 |
| bison | trinkets | championWing |  | inferred (Shade Wing's entry) | Spine1 | 0.5,0.75,0 | 1.5 |
| bison | trinkets | daynightwing | t_all102 | entry | Spine1 | 0.5,0.75,0 | 1.5 |
| bison | trinkets | devilWing |  | inferred (Shade Wing's entry) | Spine1 | 0.5,0.75,0 | 1.5 |
| bison | trinkets | Ice_Wing | t_all77 | entry | Spine1 | 0.5,0.75,0 | 1.5 |
| bison | trinkets | MoonlightRabbit | t_all142 | entry | Spine1 | 0.5,0.75,0 | 1.5 |
| bison | trinkets | PumpkonHeadband | t_allhlw3 | entry | Spine2 | 0.58,0.685796,0.00402923 | 0.7497406601905823 |
| bison | trinkets | ReaperTrinket | t_allhlw5 | entry | Spine2 | 0.0397664,0.636171,0.33871 | 1.2662311792373657 |
| bison | trinkets | Shade_Wing | t_all78 | entry | Spine1 | 0.5,0.75,0 | 1.5 |
| bison | trinkets | WhiteWing | t_all188 | entry | Spine1 | 0.4875,0.9942,-0.0143 | 1.5 |
| bison | trinkets | WitchyWing | t_all147 | entry | Spine1 | 0.5,1,0 | 1.5 |
| bison | accessories | afro | c_all11 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | afroC | c_all12 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | americaHat | c_bsn65 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | artistHat | c_all39 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | beetleHelmet | c_bsn47 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | beetleHelmetR | c_bsn48 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | berserkerHelmet | c_bsn21 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | berserkerHelmetR | c_bsn23 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | cakeHat | c_all9 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | candyHat | c_all10 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | championHelmet | c_all58 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | defenderHelmet | c_bsn22 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | defenderHelmetR | c_bsn24 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | dragonHead | c_mal37 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | earmuff1 | c_all21 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | earmuff2 | c_all22 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | fanKingHat | c_all38 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | fanKingHat_Shine |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| bison | accessories | frozenCrown | c_all56 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | gladiatorHelmet | c_bsn31 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | gladiatorHelmetR | c_bsn33 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | gotanHat | c_bsn36 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | halloweenHat | c_bsn37 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | hallowHelmet | c_bsn35 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | halo | c_all18 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | havocHelmet | c_bsn40 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | havocHelmetR | c_bsn41 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | havocHelmetV | c_bsn42 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | headphone1 | c_all23 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | headphone2 | c_all24 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | headphone3 | c_all25 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | horn | c_all19 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | krathongHat1 | c_all27 | entry | Head | -0,0,0 | 1.0 |
| bison | accessories | krathongHat2 | c_all28 | entry | Head | -0,0,0 | 1.0 |
| bison | accessories | legendHelmet | c_bsn60 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | mummyHead | c_all46 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | paperHat | c_all3 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | partyHatB | c_all7 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | partyHatR | c_all8 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | pirateBandana | c_all16 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | pirateBandanaR | c_all26 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | poseidonHelmet |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| bison | accessories | pvpHelmet | c_all43 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | pvpHelmetR | c_all44 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | quizHat | c_all37 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | redPandaHat | c_all1 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | royalHelmet | c_bsn50 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | royalHelmetR | c_bsn51,c_bsn52 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | santaHat | c_all15 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | skull | c_bsn5 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | snowmanHead | c_all29 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | sportBand | c_bsn25 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | summerHat | c_bsn15 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | superStarWig | c_bsn45 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | veggieHat | c_bsn19 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | warlordHelmet | c_bsn32 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | warlordHelmetR | c_bsn34 | class fallback | Head | -0,0,0 | 1.0 |
| bison | accessories | CactonHeadband | c_allhlw1 | entry | Head | 0.1053,-0.2327,-0.028 | 0.800000011920929 |
| bison | accessories | ChopperTrinket | c_allhlw4 | entry | Head | 0.33,0.03,0.00488263 | 1.498843789100647 |
| bison | accessories | CoconHeadband | c_allhlw2 | entry | Head | 0.0519,-0.167,0.0009 | 0.8899999856948853 |
| bison | weapons | americanAxe | w_bsn61,w_bsn65 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | barbell | w_bsn25 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | bdWeapon | w_bsn19 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | beetleAxe | w_bsn47 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | beetleAxeR | w_bsn48 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | berserkerAxe | w_bsn21 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | berserkerAxeR | w_bsn23 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | blueMoonAxe | w_bsn39 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | championAxe | w_bsn58 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | commonAxe | w_bsn2 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | defenderHammer |  | class fallback (no code) | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | defenderHammerR | w_bsn24 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | eclipseAxe | w_bsn79 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | flamingAxe | w_bsn81 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | flamingLance | w_bsn82 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | flamingScythe | w_bsn83 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | frozenAxe | w_bsn56 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | gladiatorAxe | w_bsn31 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | gladiatorAxeR | w_bsn33 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | goldenHammer | w_bsn49 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | gotanHoe | w_bsn36,w_bsn51 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | halloweenAxe | w_bsn37 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | hallowLance | w_bsn35 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | havocHammer | w_bsn40 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | havocHammerR | w_bsn41 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | havocHammerV | w_bsn42 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | heartAxe | w_bsn14 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | legendHammer | w_bsn60 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | mummyMace | w_bsn46 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | noviceAxe | w_bsn1 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | paperAxe | w_bsn3 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | poseidonAxe | w_bsn66 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | pvpAxe | w_bsn43 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | pvpAxeR | w_bsn44 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | royalHammer | w_bsn50 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | royalHammerR | w_bsn52 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | specialHammer | w_bsn59 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | standardAxe |  | class fallback (no code) | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | standardAxeR | w_bsn11 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | standardAxeV |  | class fallback (no code) | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | stoneClub | w_bsn5 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | superStarBass | w_bsn45 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | timeHammer | w_bsn69 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | toyHammer | w_bsn10,w_bsn15 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | warlordHammer | w_bsn32 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| bison | weapons | warlordHammerR | w_bsn34 | class fallback | HandMount_R | -0,0,0 | 1.0 |
| cat | trinkets | bell | t_fem2 | entry | Spine2 | -0,0,0 | 1.0 |
| cat | trinkets | bugAntenna | t_all6 | class fallback | Head | -0,0,0 | 1.0 |
| cat | trinkets | catBell | t_cat5 | entry | Spine2 | -0,0,0 | 1.0 |
| cat | trinkets | championFlag1 | t_all71 | entry | Spine1 | -0,0,0 | 1.0 |
| cat | trinkets | championFlag2 | t_all72 | entry | Spine1 | -0,0,0 | 1.0 |
| cat | trinkets | championFlag3 | t_all73 | entry | Spine1 | -0,0,0 | 1.0 |
| cat | trinkets | championFlag4 | t_all74 | entry | Spine1 | -0,0,0 | 1.0 |
| cat | trinkets | chineseLantern | t_fem37 | entry | Spine1 | -0,0,0 | 1.0 |
| cat | trinkets | chineseTalisman |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| cat | trinkets | chineseTalismanR | t_fem31 | class fallback | Head | -0,0,0 | 1.0 |
| cat | trinkets | deerHorn | t_fem15 | class fallback | Head | -0,0,0 | 1.0 |
| cat | trinkets | doubleHorn | t_all66 | class fallback | Head | -0,0,0 | 1.0 |
| cat | trinkets | frozenMask | t_fem56 | class fallback | Head | -0,0,0 | 1.0 |
| cat | trinkets | glasses | t_all1 | class fallback | Head | -0,0,0 | 1.0 |
| cat | trinkets | groceryBag | t_all46 | entry | Hand_L | -0,0,0 | 0.800000011920929 |
| cat | trinkets | legendTrinket | t_cat60 | entry | Spine1 | -0,0,0 | 1.0 |
| cat | trinkets | lollipop | t_all9 | class fallback | Head | -0,0,0 | 1.0 |
| cat | trinkets | magazine | t_fem11 | entry | mount_Hand_L | -0,0,0 | 1.0 |
| cat | trinkets | maohWings | t_fem46 | entry | Spine2 | -0,0,0 | 1.0 |
| cat | trinkets | nerdGlasses | t_all4 | class fallback | Head | -0,0,0 | 1.0 |
| cat | trinkets | partyWhistle | t_all7 | class fallback | Head | -0,0,0 | 1.0 |
| cat | trinkets | poseidonTrinket | t_fem66 | entry | Spine2 | -0,0,0 | 1.0 |
| cat | trinkets | quotationFlag |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| cat | trinkets | redNose | t_all8 | class fallback | Head | -0,0,0 | 1.0 |
| cat | trinkets | starGlasses | t_all3 | class fallback | Head | -0,0,0 | 1.0 |
| cat | trinkets | sunGlasses | t_all2 | class fallback | Head | -0,0,0 | 1.0 |
| cat | trinkets | AngleWing | t_all110 | entry | Spine1 | 0.2743,0.1137,-0.001 | 1.0 |
| cat | trinkets | AngleWing_Crimson | t_allhlw6 | entry | Spine1 | 0.2743,0.1137,-0.001 | 1.0 |
| cat | trinkets | AngleWing_Ghost | t_allhlw7 | entry | Spine1 | 0.2743,0.1137,-0.001 | 1.0 |
| cat | trinkets | AngleWing_Pumpkin | t_allhlw8 | entry | Spine1 | 0.2743,0.1137,-0.001 | 1.0 |
| cat | trinkets | AngleWing_Spectral | t_allhlw9 | entry | Spine1 | 0.2743,0.1137,-0.001 | 1.0 |
| cat | trinkets | aura_bloodmoon | t_all186 | class fallback | Head | -0,0,0 | 1.0 |
| cat | trinkets | aura_undeadqueen | t_all185 | class fallback | Head | -0,0,0 | 1.0 |
| cat | trinkets | Azure_Wing | t_all101 | entry | Spine1 | -0,0.25,0 | 1.0 |
| cat | trinkets | championWing |  | inferred (Shade Wing's entry) | Spine1 | -0,0.25,0 | 1.0 |
| cat | trinkets | daynightwing | t_all102 | entry | Spine1 | -0,0.1,0 | 1.0 |
| cat | trinkets | devilWing |  | inferred (Shade Wing's entry) | Spine1 | -0,0.25,0 | 1.0 |
| cat | trinkets | Ice_Wing | t_all77 | entry | Spine1 | -0,0.25,0 | 1.0 |
| cat | trinkets | MoonlightRabbit | t_all142 | entry | Spine1 | 0.2,0.2,0 | 1.0 |
| cat | trinkets | PumpkonHeadband | t_allhlw3 | entry | Spine1 | 0.00900736,0.237102,0.00184857 | 0.362842321395874 |
| cat | trinkets | ReaperTrinket | t_allhlw5 | entry | Spine2 | -0.192713,0.501112,-0.0343585 | 0.7912837266921997 |
| cat | trinkets | Shade_Wing | t_all78 | entry | Spine1 | -0,0.25,0 | 1.0 |
| cat | trinkets | WhiteWing | t_all188 | entry | Spine1 | 0.0059,0.3984,0.0012 | 1.0 |
| cat | trinkets | WitchyWing | t_all147 | entry | Spine1 | -0,0.15,0 | 1.0 |
| cat | accessories | abetteHat | c_cat36 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | adventurerHat | c_cat21 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | adventurerHatR | c_cat23 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | afro | c_all11 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | afroC | c_all12 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | artistHat | c_all39 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | assassinHood | c_cat32 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | assassinHoodR | c_cat34,c_cat61 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | cakeHat | c_all9 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | candyHat | c_all10 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | catHead | c_cat5 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | championHelmet | c_all58 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | chineseHair | c_cat25 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | default |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| cat | accessories | dragonflyHat | c_cat47,c_cat51 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | dragonflyHatR | c_cat48 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | earmuff1 | c_all21 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | earmuff2 | c_all22 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | fanKingHat | c_all38 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | fanKingHat_Shine |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| cat | accessories | flowerBand | c_fem11 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | frozenCrown | c_all56 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | gamblerHat | c_cat31 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | gamblerHatR | c_cat33 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | halloweenHat | c_cat37 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | hallowHat | c_cat35 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | halo | c_all18 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | headphone1 | c_all23 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | headphone2 | c_all24 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | headphone3 | c_all25 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | horn | c_all19 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | krathongHat1 | c_all27 | entry | Head | -0,0,0 | 1.0 |
| cat | accessories | krathongHat2 | c_all28 | entry | Head | -0,0,0 | 1.0 |
| cat | accessories | legendHelmet | c_cat60 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | lionHead | c_fem37 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | moroccoHair | c_cat65 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | mummyHead | c_all46 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | paperHat |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| cat | accessories | partyHatB | c_all7 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | partyHatR | c_all8 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | pirateBandana | c_all16 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | pirateBandanaR | c_all26 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | pirateHat | c_cat40 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | pirateHatR | c_cat41 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | pirateHatV | c_cat42 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | poseidonHelmet | c_all66 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | pvpHelmet | c_all43 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | pvpHelmetR | c_all44 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | quizHat | c_all37 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | redPandaHat | c_all1 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | rogueHat | c_cat22 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | rogueHatR | c_cat24 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | royalHelmet | c_cat50 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | royalHelmetR | c_cat52 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | santaHat | c_all15 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | snowmanHead | c_all29 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | standardHat | c_cat10 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | standardHatR | c_cat11 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | standardHatV | c_cat12 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | summerHair | c_cat15 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | superStarCap | c_cat45 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | veggieHat | c_cat19 | class fallback | Head | -0,0,0 | 1.0 |
| cat | accessories | CactonHeadband | c_allhlw1 | entry | Head | 0.1066,-0.0852,-0.007 | 0.25929999351501465 |
| cat | accessories | ChopperTrinket | c_allhlw4 | entry | Head | 0.230411,0.0220316,0.0246794 | 0.42891496419906616 |
| cat | accessories | CoconHeadband | c_allhlw2 | entry | Head | 0.1241,-0.0825,-0.0028 | 0.25619998574256897 |
| cat | weapons | abetteKnife | w_cat36 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | adventurerKnife | w_cat21 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | adventurerKnifeR | w_cat23 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | assassinDagger | w_cat32 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | assassinDaggerR | w_cat34 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | bdWeapon | w_cat19 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | bugZapper | w_cat15 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | championDagger | w_cat58 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | chineseFan | w_cat25 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | commonKnife | w_cat2 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | dragonflyDagger | w_cat47 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | dragonflyDaggerR | w_cat48 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | eclipseDagger | w_cat79 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | fishBone | w_cat5 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | flamingDagger | w_cat81 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | frozenKnife | w_cat56 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | gamblerKnife | w_cat31 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | gamblerKnifeR | w_cat33 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | goldenKnife | w_cat49 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | hallowClaw | w_cat35 | entry | Hand_R | -0,0,0 | 1.0 |
| cat | weapons | halloweenDagger | w_cat37 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | heartKnife | w_cat14 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | legendDagger | w_cat61 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | luckyStarKnife | w_cat39 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | moroccoLamp | w_cat65 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | mummyKnife | w_cat46 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | noviceKnife | w_cat1 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | paperShuriken | w_cat3 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | pirateKnife | w_cat40 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | pirateKnifeR | w_cat41 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | pirateKnifeV | w_cat42 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | poseidonKnife | w_cat66 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | pvpKnife | w_cat43 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | pvpKnifeR | w_cat44 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | rogueKnife | w_cat22 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | rogueKnifeR | w_cat24 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | royalDagger | w_cat50 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | royalDaggerR | w_cat52 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | specialKnife | w_cat59 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | standardKnife | w_cat10 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | standardKnifeR | w_cat11 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | standardKnifeV | w_cat12 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | starRadio | w_cat45 | class fallback | mount_Hand_R | -0,0,0 | 1.0 |
| cat | weapons | timeClaw | w_cat69 | entry | Arm_R | -0,0,0 | 1.0 |
| chameleon | trinkets | bugAntenna | t_all6 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | trinkets | championFlag1 | t_all71 | entry | Spine1 | -0,0,0 | 1.0 |
| chameleon | trinkets | championFlag2 | t_all72 | entry | Spine1 | -0,0,0 | 1.0 |
| chameleon | trinkets | championFlag3 | t_all73 | entry | Spine1 | -0,0,0 | 1.0 |
| chameleon | trinkets | championFlag4 | t_all74 | entry | Spine1 | -0,0,0 | 1.0 |
| chameleon | trinkets | chineseLantern | t_mal37 | entry | Spine1 | -0,0,0 | 1.0 |
| chameleon | trinkets | chineseTalisman | t_mal31 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | trinkets | chineseTalismanR |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| chameleon | trinkets | comic | t_mal11 | entry | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | trinkets | curseAnkh | t_mal46 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | trinkets | doubleHorn | t_all66 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | trinkets | frozenWing | t_mal56 | entry | Spine1 | -0,0,0 | 1.0 |
| chameleon | trinkets | glasses | t_all1 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | trinkets | groceryBag | t_all46 | entry | Hand_L | -0,0,0 | 1.0 |
| chameleon | trinkets | legendTrinket | t_chm60 | entry | Spine2 | -0,0,0 | 1.0 |
| chameleon | trinkets | lollipop | t_all9 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | trinkets | nerdGlasses | t_all4 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | trinkets | partyWhistle | t_all7 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | trinkets | poseidonTrinket | t_mal66 | entry | Spine1 | -0,0,0 | 1.0 |
| chameleon | trinkets | quotationFlag |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| chameleon | trinkets | redNose | t_all8 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | trinkets | santaBag | t_mal15 | entry | Spine2 | -0,0,0 | 1.0 |
| chameleon | trinkets | starGlasses | t_all3 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | trinkets | sunGlasses | t_all2 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | trinkets | AngleWing | t_all110 | entry | Spine2 | 0.202,0.283,0.0002 | 1.0 |
| chameleon | trinkets | AngleWing_Crimson | t_allhlw6 | entry | Spine2 | 0.202,0.283,0.0002 | 1.0 |
| chameleon | trinkets | AngleWing_Ghost | t_allhlw7 | entry | Spine2 | 0.202,0.283,0.0002 | 1.0 |
| chameleon | trinkets | AngleWing_Pumpkin | t_allhlw8 | entry | Spine2 | 0.202,0.283,0.0002 | 1.0 |
| chameleon | trinkets | AngleWing_Spectral | t_allhlw9 | entry | Spine2 | 0.202,0.283,0.0002 | 1.0 |
| chameleon | trinkets | aura_bloodmoon | t_all186 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | trinkets | aura_undeadqueen | t_all185 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | trinkets | Azure_Wing | t_all101 | entry | Spine2 | 0.2,0.25,0 | 1.0 |
| chameleon | trinkets | championWing |  | inferred (Shade Wing's entry) | Spine2 | 0.2,0.25,0 | 1.0 |
| chameleon | trinkets | daynightwing | t_all102 | entry | Spine2 | 0.2,0.25,0 | 1.0 |
| chameleon | trinkets | devilWing |  | inferred (Shade Wing's entry) | Spine2 | 0.2,0.25,0 | 1.0 |
| chameleon | trinkets | Ice_Wing | t_all77 | entry | Spine2 | 0.2,0.25,0 | 1.0 |
| chameleon | trinkets | MoonlightRabbit | t_all142 | entry | Spine2 | 0.15,0.15,0 | 1.0 |
| chameleon | trinkets | PumpkonHeadband | t_allhlw3 | entry | Spine2 | 0.0196,0.24,0.0054 | 0.4523548483848572 |
| chameleon | trinkets | ReaperTrinket | t_allhlw5 | entry | Spine2 | -0.291042,-0.148645,0.360563 | 0.9961799383163452 |
| chameleon | trinkets | Shade_Wing | t_all78 | entry | Spine2 | 0.2,0.25,0 | 1.0 |
| chameleon | trinkets | WhiteWing | t_all188 | entry | Spine2 | 0.2077,0.3611,0.1859 | 1.0 |
| chameleon | trinkets | WitchyWing | t_all147 | entry | Spine2 | -0,0.15,0 | 1.0 |
| chameleon | accessories | afro | c_all11 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | afroC | c_all12 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | artistHat | c_all39 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | busterGoggle | c_chm22 | entry | Goggle | -0,0,0 | 1.0 |
| chameleon | accessories | busterGoggleR | c_chm24 | entry | Goggle | -0,0,0 | 1.0 |
| chameleon | accessories | cakeHat | c_all9 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | candyHat | c_all10 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | championHelmet | c_all58 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | chinaHelmet | c_chm65 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | commandGoggle | c_chm40 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | commandGoggleR | c_chm41 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | commandGoggleV | c_chm42 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | dragonHead | c_mal37 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | earmuff1 | c_all21 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | earmuff2 | c_all22 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | fanKingHat | c_all38 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | fanKingHat_Shine |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| chameleon | accessories | frozenCrown | c_all56 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | halloweenHat | c_chm37 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | halo | c_all18 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | headphone1 | c_all23 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | headphone2 | c_all24 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | headphone3 | c_all25 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | horn | c_all19 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | krathongHat1 | c_all27 | entry | Head | -0,0,0 | 1.0 |
| chameleon | accessories | krathongHat2 | c_all28 | entry | Head | -0,0,0 | 1.0 |
| chameleon | accessories | legendHelmet | c_chm60 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | mantisMask | c_chm47 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | mantisMaskR | c_chm48 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | mummyHead | c_all46 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | oliveCrown | c_chm5 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | pantherHelmet | c_chm36 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | paperHat | c_all3 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | partyHatB | c_all7 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | partyHatR | c_all8 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | pirateBandana | c_all16 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | pirateBandanaR | c_all26 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | poseidonHelmet | c_all66 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | pvpHelmet | c_all43 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | pvpHelmetR | c_all44 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | quizHat | c_all37 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | redPandaHat | c_all1 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | royalHelmet | c_chm50 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | royalHelmetR | c_chm52 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | santaHat | c_all15 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | slayerMask | c_chm32 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | slayerMaskR | c_chm34 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | snookerHat | c_chm25 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | snowmanHead | c_all29 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | standardGoggle | c_chm10,c_chm61 | entry | Goggle | -0,0,0 | 1.0 |
| chameleon | accessories | standardGoggleR | c_chm11 | entry | Goggle | -0,0,0 | 1.0 |
| chameleon | accessories | standardGoggleV | c_chm12 | entry | Goggle | -0,0,0 | 1.0 |
| chameleon | accessories | summerGoggle | c_chm15 | entry | Goggle | -0,0,0 | 1.0 |
| chameleon | accessories | superStarGoggle | c_chm45 | entry | Goggle | -0,0,0 | 1.0 |
| chameleon | accessories | tacticianGoggle | c_chm21 | entry | Goggle | -0,0,0 | 1.0 |
| chameleon | accessories | tacticianGoggleR | c_chm23 | entry | Goggle | -0,0,0 | 1.0 |
| chameleon | accessories | tricksterGoggle | c_chm31 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | tricksterGoggleR | c_chm33 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | veggieHat | c_chm19 | class fallback | Head | -0,0,0 | 1.0 |
| chameleon | accessories | CactonHeadband | c_allhlw1 | entry | Head | 0.0547,-0.008,-0.0011 | 0.3517000079154968 |
| chameleon | accessories | ChopperTrinket | c_allhlw4 | entry | Head | -0.0606,-0.0206,0.0026 | 0.396490216255188 |
| chameleon | accessories | CoconHeadband | c_allhlw2 | entry | Head | 0.0178,0.028,0.0023 | 0.4255000054836273 |
| chameleon | weapons | bdArrow | w_chm19 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | bdBow | w_chm19 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | busterArrow | w_chm22 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | busterArrowR | w_chm24 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | busterBow | w_chm22 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | busterBowR | w_chm24 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | championArrow | w_chm58 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | championBow | w_chm58 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | chinaArrow | w_chm65 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | chinaBow | w_chm65 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | commandArrow | w_chm40 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | commandArrowR | w_chm41 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | commandArrowV | w_chm42 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | commandBow | w_chm40 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | commandBowR | w_chm41 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | commandBowV | w_chm42 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | commonArrow | w_chm2 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | commonBow | w_chm2 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | cupidArrow | w_chm5 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | cupidBow | w_chm5 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | eclipseArrow | w_chm79 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | eclipseBow | w_chm79 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | flamingArch | w_chm82 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | flamingArrow | w_chm81 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | flamingBow | w_chm81 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | flamingShot | w_chm82 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | frozenArrow | w_chm56 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | frozenBow | w_chm56 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | goldenArrow | w_chm49 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | goldenBow | w_chm49 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | hallowArrow | w_chm35 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | hallowBow | w_chm35 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | halloweenArrow | w_chm37 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | halloweenBow | w_chm37 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | heartArrow | w_chm14 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | heartBow | w_chm10,w_chm14 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | legendArrow | w_chm61 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | legendBow |  | class fallback (no code) | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | mantisArrow | w_chm47 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | mantisArrowR | w_chm48 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | mantisBow | w_chm47 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | mantisBowR | w_chm48 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | mummyArrow | w_chm46 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | mummyBow | w_chm46 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | noviceArrow | w_chm1 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | noviceBow | w_chm1 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | pantherArrow | w_chm36 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | pantherBow | w_chm36 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | paperArrow | w_chm3 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | paperBow | w_chm3 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | plungerArrow | w_chm15 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | plungerBow | w_chm15 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | poseidonArrow | w_chm66 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | poseidonBow | w_chm66 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | pvpArrow | w_chm43 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | pvpArrowR | w_chm44 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | pvpBow | w_chm43 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | pvpBowR | w_chm44 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | royalArrow | w_chm50 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | royalArrowR | w_chm51,w_chm52 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | royalBow | w_chm50 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | royalBowR | w_chm51,w_chm52 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | salamanderArrow | w_chm39 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | salamanderBow | w_chm39 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | slayerArrow | w_chm32 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | slayerArrowR | w_chm34 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | slayerBow | w_chm32 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | slayerBowR | w_chm34 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | snookerBall | w_chm25 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | snookerCue | w_chm25 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | specialArrow | w_chm59 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | specialBow | w_chm59 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | standardArrow | w_chm10 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | standardArrowR | w_chm11 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | standardArrowV | w_chm12 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | standardBow | w_chm61 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | standardBowR | w_chm11 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | standardBowV | w_chm12 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | superStarGuitar | w_chm45 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | superStarPick | w_chm45 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | tacticianArrow | w_chm21 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | tacticianArrowR | w_chm23 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | tacticianBow | w_chm21 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | tacticianBowR | w_chm23 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | timeArrow | w_chm69 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | timeBow | w_chm69 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | tricksterArrow | w_chm31 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | tricksterArrowR | w_chm33 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | tricksterBow | w_chm31 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| chameleon | weapons | tricksterBowR | w_chm33 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| mole | trinkets | bugAntenna | t_all6 | class fallback | Head | -0,0,0 | 1.0 |
| mole | trinkets | championFlag1 | t_all71 | entry | UpperBody1 | -0,0,0 | 1.0 |
| mole | trinkets | championFlag2 | t_all72 | entry | UpperBody1 | -0,0,0 | 1.0 |
| mole | trinkets | championFlag3 | t_all73 | entry | UpperBody1 | -0,0,0 | 1.0 |
| mole | trinkets | championFlag4 | t_all74 | entry | UpperBody1 | -0,0,0 | 1.0 |
| mole | trinkets | chineseLantern | t_mal37 | entry | UpperBody1 | -0,0,0 | 1.0 |
| mole | trinkets | chineseTalisman | t_mal31 | class fallback | Head | -0,0,0 | 1.0 |
| mole | trinkets | chineseTalismanR |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| mole | trinkets | comic | t_mal11 | entry | mount_Hand_R | -0,0,0 | 1.0 |
| mole | trinkets | curseAnkh | t_mal46 | class fallback | Head | -0,0,0 | 1.0 |
| mole | trinkets | doubleHorn | t_all66 | class fallback | Head | -0,0,0 | 1.0 |
| mole | trinkets | frozenWing | t_mal56 | entry | UpperBody1 | -0,0,0 | 1.0 |
| mole | trinkets | glasses | t_all1 | class fallback | Head | -0,0,0 | 1.0 |
| mole | trinkets | groceryBag | t_all46 | entry | Hand_L | -0,0,0 | 0.800000011920929 |
| mole | trinkets | legendTrinket | t_mol60 | entry | ROOT | -0,0,0 | 1.0 |
| mole | trinkets | lollipop | t_all9 | class fallback | Head | -0,0,0 | 1.0 |
| mole | trinkets | nerdGlasses | t_all4 | class fallback | Head | -0,0,0 | 1.0 |
| mole | trinkets | partyWhistle | t_all7 | class fallback | Head | -0,0,0 | 1.0 |
| mole | trinkets | poseidonTrinket | t_mal66 | entry | UpperBody1 | -0,0,0 | 1.0 |
| mole | trinkets | quotationFlag |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| mole | trinkets | redNose | t_all8 | class fallback | Head | -0,0,0 | 1.0 |
| mole | trinkets | santaBag | t_mal15 | entry | UpperBody2 | -0,0,0 | 1.0 |
| mole | trinkets | starGlasses | t_all3 | class fallback | Head | -0,0,0 | 1.0 |
| mole | trinkets | sunGlasses | t_all2 | class fallback | Head | -0,0,0 | 1.0 |
| mole | trinkets | AngleWing | t_all110 | entry | UpperBody1 | 0.1261,0.3558,0 | 0.5799999833106995 |
| mole | trinkets | AngleWing_Crimson | t_allhlw6 | entry | UpperBody1 | 0.1261,0.3558,0 | 0.5799999833106995 |
| mole | trinkets | AngleWing_Ghost | t_allhlw7 | entry | UpperBody1 | 0.1261,0.3558,0 | 0.5799999833106995 |
| mole | trinkets | AngleWing_Pumpkin | t_allhlw8 | entry | UpperBody1 | 0.1261,0.3558,0 | 0.5799999833106995 |
| mole | trinkets | AngleWing_Spectral | t_allhlw9 | entry | UpperBody1 | 0.1261,0.3558,0 | 0.5799999833106995 |
| mole | trinkets | aura_bloodmoon | t_all186 | class fallback | Head | -0,0,0 | 1.0 |
| mole | trinkets | aura_undeadqueen | t_all185 | class fallback | Head | -0,0,0 | 1.0 |
| mole | trinkets | Azure_Wing | t_all101 | entry | UpperBody1 | 0.1,0.3,0 | 1.0 |
| mole | trinkets | championWing |  | inferred (Shade Wing's entry) | UpperBody1 | 0.1,0.3,0 | 1.0 |
| mole | trinkets | daynightwing | t_all102 | entry | UpperBody1 | 0.1,0.3,0 | 1.0 |
| mole | trinkets | devilWing |  | inferred (Shade Wing's entry) | UpperBody1 | 0.1,0.3,0 | 1.0 |
| mole | trinkets | Ice_Wing | t_all77 | entry | UpperBody1 | 0.1,0.3,0 | 1.0 |
| mole | trinkets | MoonlightRabbit | t_all142 | entry | UpperBody1 | 0.2,0.2,0 | 1.0 |
| mole | trinkets | PumpkonHeadband | t_allhlw3 | entry | UpperBody1 | -0.0641,0.1291,0.206 | 0.20759999752044678 |
| mole | trinkets | ReaperTrinket | t_allhlw5 | entry | UpperBody1 | 0.0576659,0.634672,0.11547 | 0.41691333055496216 |
| mole | trinkets | Shade_Wing | t_all78 | entry | UpperBody1 | 0.1,0.3,0 | 1.0 |
| mole | trinkets | WhiteWing | t_all188 | entry | UpperBody1 | 0.1,0.4773,0 | 0.699999988079071 |
| mole | trinkets | WitchyWing | t_all147 | entry | UpperBody1 | -0,0.3,0 | 1.0 |
| mole | accessories | africaHat | c_mol65 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | afro | c_all11 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | afroC | c_all12 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | artistHat | c_all39 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | barrelHelmet | c_mol5 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | beeHat | c_mol47 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | beeHatR | c_mol48,c_mol51 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | bomberHat | c_mol31 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | bomberHatR | c_mol33 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | cakeHat | c_all9 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | candyHat | c_all10 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | capitalHat | c_mol40 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | capitalHatR | c_mol41 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | capitalHatV | c_mol42 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | championHelmet | c_all58 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | dragonHead | c_mal37 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | earmuff1 | c_all21 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | earmuff2 | c_all22 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | fanKingHat | c_all38,c_mol61 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | fanKingHat_Shine |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| mole | accessories | frozenCrown | c_all56 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | halloweenHat | c_mol37 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | hallowWig | c_mol35 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | halo | c_all18 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | headphone1 | c_all23 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | headphone2 | c_all24 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | headphone3 | c_all25 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | horn | c_all19 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | infantryHat | c_mol21 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | infantryHatR | c_mol23 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | krathongHat1 | c_all27 | entry | Head | -0,0,0 | 1.0 |
| mole | accessories | krathongHat2 | c_all28 | entry | Head | -0,0,0 | 1.0 |
| mole | accessories | legendHelmet | c_mol60 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | machinistHelmet | c_mol32 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | machinistHelmetR | c_mol34 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | mummyHead | c_all46 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | paperHat | c_all3 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | partyHatB | c_all7 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | partyHatR | c_all8 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | pirateBandana | c_all16 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | pirateBandanaR | c_all26 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | poseidonHelmet | c_all66 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | pvpHelmet | c_all43 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | pvpHelmetR | c_all44 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | quizHat | c_all37 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | redPandaHat | c_all1 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | royalHelmet | c_mol50 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | royalHelmetR | c_mol52 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | santaHat | c_all15 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | snowmanHead | c_all29 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | standardGoggle | c_mol10 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | standardGoggleR | c_mol11 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | standardGoggleV | c_mol12 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | steamHelmet | c_mol22 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | steamHelmetR | c_mol24 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | summerHat | c_mol15 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | superStarWig | c_mol45 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | trumpeterHat | c_mol25 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | veggieHat | c_mol19 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | zappaHelmet | c_mol36 | class fallback | Head | -0,0,0 | 1.0 |
| mole | accessories | CactonHeadband | c_allhlw1 | entry | Head | 0.0002,0.0174,-0.0006 | 0.435699999332428 |
| mole | accessories | ChopperTrinket | c_allhlw4 | entry | Head | 0.0609,-0.1315,0.0051 | 0.5867729783058167 |
| mole | accessories | CoconHeadband | c_allhlw2 | entry | Head | 0.0311,0.0267,-0.0006 | 0.43059998750686646 |
| mole | weapons | africaCannon | w_mol65 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | barrelCannon | w_mol5 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | bdWeapon | w_mol19 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | beeCannon | w_mol47 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | beeCannonR | w_mol48 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | bomberCannon | w_mol31 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | bomberCannonR | w_mol33 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | capitalCannon | w_mol40 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | capitalCannonR | w_mol41 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | capitalCannonV | w_mol42 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | championCannon | w_mol58 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | commonCannon | w_mol2 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | drumSet | w_mol45 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | eclipseCannon | w_mol79 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | flamingCannon | w_mol81 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | frozenCannon | w_mol56 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | goldenCannon | w_mol49 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | hallowCannon | w_mol35 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | halloweenPot | w_mol37 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | heartCannon | w_mol14 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | infantryCannon | w_mol21 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | infantryCannonR | w_mol23 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | legendCannon | w_mol60 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | machinistCannon | w_mol32 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | machinistCannonR | w_mol34 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | mummyCannon | w_mol46 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | noviceCannon | w_mol1 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | paperCannon | w_mol3 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | poseidonCannon | w_mol66 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | pumpkinCannon | w_mol39 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | pvpCannon | w_mol43 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | pvpCannonR | w_mol44 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | royalCannon | w_mol50 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | royalCannonR | w_mol52 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | schoolCannon | w_mol15 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | specialCannon | w_mol59 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | standardCannon | w_mol10 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | standardCannonR |  | class fallback (no code) | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | standardCannonV | w_mol12 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | steamCannon | w_mol22 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | steamCannonR | w_mol24 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | timeCannon | w_mol69 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | trumpet | w_mol25 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| mole | weapons | zappaCannon | w_mol36 | class fallback | mount_Cannon | -0,0,0 | 1.0 |
| monkey | trinkets | bugAntenna | t_all6 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | trinkets | championFlag1 | t_all71 | entry | Spine2 | -0,0,0 | 1.0 |
| monkey | trinkets | championFlag2 | t_all72 | entry | Spine2 | -0,0,0 | 1.0 |
| monkey | trinkets | championFlag3 | t_all73 | entry | Spine2 | -0,0,0 | 1.0 |
| monkey | trinkets | championFlag4 | t_all74 | entry | Spine2 | -0,0,0 | 1.0 |
| monkey | trinkets | chineseLantern | t_mal37 | entry | Spine2 | -0,0,0 | 1.0 |
| monkey | trinkets | chineseTalisman | t_mal31 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | trinkets | chineseTalismanR |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| monkey | trinkets | comic | t_mal11 | entry | mount_Hand_R | -0,0,0 | 1.0 |
| monkey | trinkets | curseAnkh | t_mal46 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | trinkets | doubleHorn | t_all66 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | trinkets | frozenWing | t_mal56 | entry | Spine2 | -0,0,0 | 1.0 |
| monkey | trinkets | glasses | t_all1 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | trinkets | groceryBag | t_all46 | entry | Hand_R | -0,0,0 | 0.800000011920929 |
| monkey | trinkets | legendTrinket | t_mnk60 | entry | Spine2 | -0,0,0 | 1.0 |
| monkey | trinkets | legendTrinketR | t_mnk61 | entry | Spine2 | -0,0,0 | 1.0 |
| monkey | trinkets | lollipop | t_all9 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | trinkets | nerdGlasses | t_all4 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | trinkets | partyWhistle | t_all7 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | trinkets | poseidonTrinket | t_mal66 | entry | Spine2 | -0,0,0 | 1.0 |
| monkey | trinkets | quotationFlag |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| monkey | trinkets | redNose | t_all8 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | trinkets | santaBag | t_mal15 | entry | Spine2 | -0,0,0 | 1.0 |
| monkey | trinkets | starGlasses | t_all3 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | trinkets | starGuitar | t_mnk45 | entry | Spine1 | -0,0,0 | 1.0 |
| monkey | trinkets | sunGlasses | t_all2 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | trinkets | AngleWing | t_all110 | entry | Spine2 | 0.2567,0.0996,-0.0119 | 0.699999988079071 |
| monkey | trinkets | AngleWing_Crimson | t_allhlw6 | entry | Spine2 | 0.2567,0.0996,-0.0119 | 0.699999988079071 |
| monkey | trinkets | AngleWing_Ghost | t_allhlw7 | entry | Spine2 | 0.2567,0.0996,-0.0119 | 0.699999988079071 |
| monkey | trinkets | AngleWing_Pumpkin | t_allhlw8 | entry | Spine2 | 0.2567,0.0996,-0.0119 | 0.699999988079071 |
| monkey | trinkets | AngleWing_Spectral | t_allhlw9 | entry | Spine2 | 0.2567,0.0996,-0.0119 | 0.699999988079071 |
| monkey | trinkets | aura_bloodmoon | t_all186 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | trinkets | aura_undeadqueen | t_all185 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | trinkets | Azure_Wing | t_all101 | entry | Spine2 | 0.1,0.25,0 | 1.0 |
| monkey | trinkets | championWing |  | inferred (Shade Wing's entry) | Spine2 | 0.1,0.25,0 | 1.0 |
| monkey | trinkets | daynightwing | t_all102 | entry | Spine2 | 0.1,0.25,0 | 1.0 |
| monkey | trinkets | devilWing |  | inferred (Shade Wing's entry) | Spine2 | 0.1,0.25,0 | 1.0 |
| monkey | trinkets | Ice_Wing | t_all77 | entry | Spine2 | 0.1,0.25,0 | 1.0 |
| monkey | trinkets | MoonlightRabbit | t_all142 | entry | Spine2 | 0.15,0.1,0 | 1.0 |
| monkey | trinkets | PumpkonHeadband | t_allhlw3 | entry | Spine2 | 0.0327,0.1004,-0.0144 | 0.28784117102622986 |
| monkey | trinkets | ReaperTrinket | t_allhlw5 | entry | Spine2 | -0.105762,0.270473,0.139707 | 0.6644379496574402 |
| monkey | trinkets | Shade_Wing | t_all78 | entry | Spine2 | 0.1,0.25,0 | 1.0 |
| monkey | trinkets | WhiteWing | t_all188 | entry | Spine2 | 0.0995,0.2402,0.0024 | 1.0 |
| monkey | trinkets | WitchyWing | t_all147 | entry | Spine2 | -0,0.1,0 | 1.0 |
| monkey | accessories | afro | c_all11 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | afroC | c_all12 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | artistHat | c_all39 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | cakeHat | c_all9 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | candyHat | c_all10 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | championHelmet | c_all58 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | dragonHead | c_mal37 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | earmuff1 | c_all21 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | earmuff2 | c_all22 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | earthBandana | c_mnk22 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | earthBandanaR | c_mnk24 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | englishHat | c_mnk65 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | fanKingHat | c_all38 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | fanKingHat_shine |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| monkey | accessories | fireBandana | c_mnk21 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | fireBandanaR | c_mnk23 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | frozenCrown | c_all56 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | geoBandana | c_mnk32 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | geoBandanaR | c_mnk34 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | halloweenHat | c_mnk37 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | hallowHead | c_mnk35 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | halo | c_all18 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | headphone1 | c_all23 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | headphone2 | c_all24 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | headphone3 | c_all25 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | horn | c_all19 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | krathongHat1 | c_all27 | entry | Head | -0,0,0 | 1.0 |
| monkey | accessories | krathongHat2 | c_all28 | entry | Head | -0,0,0 | 1.0 |
| monkey | accessories | legendHelmet | c_mnk60 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | magicianHat | c_mnk25 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | mosolyWig | c_mnk36 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | mummyHead | c_all46 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | paperHat | c_all3 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | partyHatB | c_all7 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | partyHatR | c_all8 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | pirateBandana | c_all16 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | pirateBandanaR | c_all26 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | poseidonHelmet | c_all66 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | pvpHelmet | c_all43 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | pvpHelmetR | c_all44 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | pyroHood | c_mnk31 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | pyroHoodR | c_mnk33 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | quizHat | c_all37 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | redPandaHat | c_all1 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | royalCirclet | c_mnk50 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | royalCircletR | c_mnk52 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | santaHat | c_all15 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | sleepHat | c_mnk5 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | snowmanHead | c_all29 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | spiderBandana | c_mnk47 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | spiderBandanaR | c_mnk48 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | standardBandana | c_mnk51,c_mnk61 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | standardBandanaR | c_mnk11 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | standardBandanaV | c_mnk10 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | starBandana | c_mnk45 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | summerCap | c_mnk15 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | theurgistHat | c_mnk40 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | theurgistHatR | c_mnk41 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | theurgistHatV | c_mnk42 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | veggieHat | c_mnk19 | class fallback | Head | -0,0,0 | 1.0 |
| monkey | accessories | CactonHeadband | c_allhlw1 | entry | Head | 0.1795,-0.0262,0.0063 | 0.24310000240802765 |
| monkey | accessories | ChopperTrinket | c_allhlw4 | entry | Head | 0.2179,0.0222,0.0146 | 0.4273514449596405 |
| monkey | accessories | CoconHeadband | c_allhlw2 | entry | Head | 0.1294,-0.0092,0.0092 | 0.2863999903202057 |
| monkey | weapons | bdWeapon | w_mnk19 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | championMike | w_mnk58 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | commonMike | w_mnk2 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | earthMike | w_mnk22 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | earthMikeR | w_mnk24 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | eclipseMike | w_mnk79 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | englishMike | w_mnk65 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | fireMike | w_mnk21 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | fireMikeR | w_mnk23 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | frozenMike | w_mnk56 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | geoMike |  | class fallback (no code) | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | geoMikeR | w_mnk34 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | goldenMike | w_mnk49,w_mnk51 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | goldMike | w_mnk39 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | halloweenMike | w_mnk37 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | heartMike | w_mnk10,w_mnk14 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | legendMike | w_mnk60 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | magicianMike | w_mnk25 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | monkeyHead | w_mnk35 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | moonMike | w_mnk5 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | mosolyMike | w_mnk36 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | mummyMike | w_mnk46 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | needleMike | w_mnk15 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | noviceMike | w_mnk1,w_mnk61 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | paperMike | w_mnk3 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | poseidonMike | w_mnk66 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | pvpMike | w_mnk43 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | pvpMikeR | w_mnk44 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | pyroMike | w_mnk31 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | pyroMikeR | w_mnk33 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | royalMike | w_mnk50 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | royalMikeR | w_mnk52 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | specialMike | w_mnk59 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | spiderMike | w_mnk47 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | spiderMikeR | w_mnk48 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | standardMike |  | class fallback (no code) | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | standardMikeR | w_mnk11 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | standardMikeV | w_mnk12 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | superStarMike | w_mnk45 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | theurgistMike | w_mnk40 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | theurgistMikeR | w_mnk41 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | theurgistMikeV | w_mnk42 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| monkey | weapons | timeMike | w_mnk69 | class fallback | mount_Summon | -0,0,0 | 1.0 |
| panda | trinkets | bugAntenna | t_all6 | class fallback | Head | -0,0,0 | 1.0 |
| panda | trinkets | championFlag1 | t_all71 | entry | Spine2 | -0,0,0 | 1.0 |
| panda | trinkets | championFlag2 | t_all72 | entry | Spine2 | -0,0,0 | 1.0 |
| panda | trinkets | championFlag3 | t_all73 | entry | Spine2 | -0,0,0 | 1.0 |
| panda | trinkets | championFlag4 | t_all74 | entry | Spine2 | -0,0,0 | 1.0 |
| panda | trinkets | chineseLantern | t_mal37 | entry | Spine2 | -0,0,0 | 1.0 |
| panda | trinkets | chineseTalisman | t_mal31 | class fallback | Head | -0,0,0 | 1.0 |
| panda | trinkets | chineseTalismanR |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| panda | trinkets | comic | t_mal11 | entry | mount_Arm_L | -0,0,0 | 1.0 |
| panda | trinkets | curseAnkh | t_mal46 | class fallback | Head | -0,0,0 | 1.0 |
| panda | trinkets | doubleHorn | t_all66 | class fallback | Head | -0,0,0 | 1.0 |
| panda | trinkets | frozenWing | t_mal56 | entry | Spine2 | -0,0,0 | 1.0 |
| panda | trinkets | glasses | t_all1 | class fallback | Head | -0,0,0 | 1.0 |
| panda | trinkets | gourd | t_pnd5 | entry | Spine1 | -0,0,0 | 1.0 |
| panda | trinkets | groceryBag | t_all46 | entry | Hand_L | -0,0,0 | 0.6000000238418579 |
| panda | trinkets | legendTrinket | t_pnd60 | entry | Spine1 | -0,0,0 | 1.0 |
| panda | trinkets | legendTrinketR |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| panda | trinkets | lollipop | t_all9 | class fallback | Head | -0,0,0 | 1.0 |
| panda | trinkets | nerdGlasses | t_all4 | class fallback | Head | -0,0,0 | 1.0 |
| panda | trinkets | partyWhistle | t_all7 | class fallback | Head | -0,0,0 | 1.0 |
| panda | trinkets | poseidonTrinket | t_mal66 | entry | Spine2 | -0,0,0 | 1.0 |
| panda | trinkets | quotationFlag |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| panda | trinkets | redNose | t_all8 | class fallback | Head | -0,0,0 | 1.0 |
| panda | trinkets | santaBag | t_mal15 | entry | Spine1 | -0,0,0 | 1.0 |
| panda | trinkets | starGlasses | t_all3 | class fallback | Head | -0,0,0 | 1.0 |
| panda | trinkets | starGuitar | t_pnd45 | entry | Spine1 | -0,0,0 | 1.0 |
| panda | trinkets | sunGlasses | t_all2 | class fallback | Head | -0,0,0 | 1.0 |
| panda | trinkets | turtleShell1 | t_pnd26 | entry | Spine1 | -0,0,0 | 1.0 |
| panda | trinkets | turtleShell2 | t_pnd27 | entry | Spine1 | -0,0,0 | 1.0 |
| panda | trinkets | AngleWing | t_all110 | entry | Spine2 | 0.1,0.1111,-0.0016 | 0.5 |
| panda | trinkets | AngleWing_Crimson | t_allhlw6 | entry | Spine2 | 0.1,0.1111,-0.0016 | 0.5 |
| panda | trinkets | AngleWing_Ghost | t_allhlw7 | entry | Spine2 | 0.1,0.1111,-0.0016 | 0.5 |
| panda | trinkets | AngleWing_Pumpkin | t_allhlw8 | entry | Spine2 | 0.1,0.1111,-0.0016 | 0.5 |
| panda | trinkets | AngleWing_Spectral | t_allhlw9 | entry | Spine2 | 0.1,0.1111,-0.0016 | 0.5 |
| panda | trinkets | aura_bloodmoon | t_all186 | class fallback | Head | -0,0,0 | 1.0 |
| panda | trinkets | aura_undeadqueen | t_all185 | class fallback | Head | -0,0,0 | 1.0 |
| panda | trinkets | Azure_Wing | t_all101 | entry | Spine2 | 0.1,0.25,0 | 1.0 |
| panda | trinkets | championWing |  | inferred (Shade Wing's entry) | Spine2 | 0.1,0.25,0 | 1.0 |
| panda | trinkets | daynightwing | t_all102 | entry | Spine2 | 0.1,0.25,0 | 1.0 |
| panda | trinkets | devilWing |  | inferred (Shade Wing's entry) | Spine2 | 0.1,0.25,0 | 1.0 |
| panda | trinkets | Ice_Wing | t_all77 | entry | Spine2 | 0.1,0.25,0 | 1.0 |
| panda | trinkets | MoonlightRabbit | t_all142 | entry | Spine2 | 0.2,0.1,0 | 1.0 |
| panda | trinkets | PumpkonHeadband | t_allhlw3 | entry | Spine2 | 0.0264,0.1779,-0.029 | 0.185968816280365 |
| panda | trinkets | ReaperTrinket | t_allhlw5 | entry | Spine2 | -0.0579,0.191044,0.105613 | 0.4473794400691986 |
| panda | trinkets | Shade_Wing | t_all78 | entry | Spine2 | 0.1,0.25,0 | 1.0 |
| panda | trinkets | WhiteWing | t_all188 | entry | Spine2 | 0.1,0.219,0.0044 | 0.5 |
| panda | trinkets | WitchyWing | t_all147 | entry | Spine2 | -0,0.15,0 | 1.0 |
| panda | accessories | afro | c_all11 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | afroC | c_all12 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | artistHat | c_all39 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | bisonMask | c_pnd4 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | brawlerCollar | c_pnd21,c_pnd61 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | brawlerCollarR | c_pnd23 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | cakeHat | c_all9 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | candyHat | c_all10 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | championHelmet | c_all58 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | dragonHead | c_mal37 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | earmuff1 | c_all21 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | earmuff2 | c_all22 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | fanKingHat | c_all38 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | fanKingHat_Shine |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| panda | accessories | fighterBand | c_pnd25 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | frozenCrown | c_all56 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | germanHat | c_pnd65 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | halloweenHat | c_pnd37 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | hallowHead | c_pnd35 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | halo | c_all18 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | headphone1 | c_all23 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | headphone2 | c_all24 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | headphone3 | c_all25 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | horn | c_all19 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | krathongHat1 | c_all27 | entry | Head | -0,0,0 | 1.0 |
| panda | accessories | krathongHat2 | c_all28 | entry | Head | -0,0,0 | 1.0 |
| panda | accessories | legendHelmet | c_pnd60 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | mohawk | c_pnd36 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | mummyHead | c_all46 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | paperHat | c_all3 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | partyHatB | c_all7 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | partyHatR | c_all8 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | pirateBandana | c_all16 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | pirateBandanaR | c_all26 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | poseidonHelmet | c_all66 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | pvpHelmet | c_all43 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | pvpHelmetR | c_all44 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | quizHat | c_all37 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | redPandaHat | c_all1 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | royalHelmet | c_pnd50 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | royalHelmetR | c_pnd51,c_pnd52 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | sageHat | c_pnd32 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | sageHatR | c_pnd34 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | santaHat | c_all15 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | shinHelmet | c_pnd40 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | shinHelmetR | c_pnd41 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | shinHelmetV | c_pnd42 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | snowmanHead | c_all29 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | strikeHelmet | c_pnd31 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | strikeHelmetR | c_pnd33 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | summerWig | c_pnd15 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | superStarWig | c_pnd45 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | veggieHat | c_pnd19 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | wig | c_pnd5 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | wormHelmet | c_pnd47 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | wormHelmetR | c_pnd48 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | wuxianHat | c_pnd22 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | wuxianHatR | c_pnd24 | class fallback | Head | -0,0,0 | 1.0 |
| panda | accessories | CactonHeadband | c_allhlw1 | entry | Head | 0.0426,-0.0299,0.0035 | 0.37940001487731934 |
| panda | accessories | ChopperTrinket | c_allhlw4 | entry | Head | 0.262628,-0.013762,0.023094 | 0.3533 |
| panda | accessories | CoconHeadband | c_allhlw2 | entry | Head | 0.011,-0.0203,0.0142 | 0.45010000467300415 |
| panda | weapons | bdWeapon_L | w_pnd19 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | bdWeapon_R | w_pnd19 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | boxingGrove_L | w_pnd15 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | boxingGrove_R | w_pnd15 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | brawlerGauntlet_L | w_pnd21 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | brawlerGauntlet_R | w_pnd21 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | brawlerGauntletR_L | w_pnd23 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | brawlerGauntletR_R | w_pnd23 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | championGauntlet_L | w_pnd58 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | championGauntlet_R | w_pnd58 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | commonGauntlet_L | w_pnd2 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | commonGauntlet_R | w_pnd2 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | eclipseGauntlet_l | w_pnd79 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | eclipseGauntlet_r | w_pnd79 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | fighterFist_L | w_pnd25 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | fighterFist_R | w_pnd25 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | frozenGauntlet_L | w_pnd56 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | frozenGauntlet_R | w_pnd56 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | germanGlove_L | w_pnd65 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | germanGlove_R | w_pnd65 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | goldenGauntlet_L | w_pnd49 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | goldenGauntlet_R | w_pnd49 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | halloweenScarecrow_L | w_pnd37 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | halloweenScarecrow_R | w_pnd37 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | hallowTonfa_L | w_pnd35 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | hallowTonfa_R | w_pnd35 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | heartGauntlet_L | w_pnd14 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | heartGauntlet_R | w_pnd14 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | holyThread |  | class fallback (no code) | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | legendGauntlet_L | w_pnd60 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | legendGauntlet_R | w_pnd60 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | metalKnuckle_L | w_pnd39 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | metalKnuckle_R | w_pnd39 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | mummyClaw_L | w_pnd46 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | mummyClaw_R | w_pnd46 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | noviceGauntlet_L | w_pnd1 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | noviceGauntlet_R | w_pnd1 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | paperKnuckle_L | w_pnd3 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | paperKnuckle_R | w_pnd3 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | poseidonKnuckle_L | w_pnd66 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | poseidonKnuckle_R | w_pnd66 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | pvpGauntlet_L | w_pnd43 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | pvpGauntlet_R | w_pnd43 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | pvpGauntletR_L | w_pnd44 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | pvpGauntletR_R | w_pnd44 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | royalGauntlet_L | w_pnd50 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | royalGauntlet_R | w_pnd50 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | royalGauntletR_L | w_pnd52 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | royalGauntletR_R | w_pnd52 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | sageGauntlet_L | w_pnd32 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | sageGauntlet_R | w_pnd32 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | sageGauntletR_L | w_pnd34 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | sageGauntletR_R | w_pnd34 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | shinGauntlet_L | w_pnd40 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | shinGauntlet_R | w_pnd40 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | shinGauntletR_L | w_pnd41 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | shinGauntletR_R | w_pnd41 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | shinGauntletV_L | w_pnd42 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | shinGauntletV_R | w_pnd42 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | specialGauntlet_L | w_pnd59 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | specialGauntlet_R | w_pnd59 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | standardGauntlet_L | w_pnd10 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | standardGauntlet_R | w_pnd10 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | standardGauntletR_L | w_pnd11 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | standardGauntletR_R | w_pnd11 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | standardGauntletV_L | w_pnd12 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | standardGauntletV_R | w_pnd12 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | steinKnuckle_L | w_pnd36 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | steinKnuckle_R | w_pnd36 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | strikeGauntlet_L | w_pnd31 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | strikeGauntlet_R | w_pnd31 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | strikeGauntletR_L | w_pnd33 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | strikeGauntletR_R | w_pnd33 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | superStarKnuckle_L | w_pnd45 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | superStarKnuckle_R | w_pnd45 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | timeGauntlet_L | w_pnd69 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | timeGauntlet_R | w_pnd69 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | wormGauntlet_L | w_pnd47 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | wormGauntlet_R | w_pnd47 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | wormGauntletR_L | w_pnd48 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | wormGauntletR_R | w_pnd48 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | wuxianGauntlet_L | w_pnd22 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | wuxianGauntlet_R | w_pnd22 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | wuxianGauntletR_L | w_pnd24 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| panda | weapons | wuxianGauntletR_R | w_pnd24 | class fallback | mount_Arm_L | -0,0,0 | 1.0 |
| penguin | trinkets | bugAntenna | t_all6 | class fallback | Head | -0,0,0 | 1.0 |
| penguin | trinkets | championFlag1 | t_all71 | entry | Spine2 | -0,0,0 | 1.0 |
| penguin | trinkets | championFlag2 | t_all72 | entry | Spine2 | -0,0,0 | 1.0 |
| penguin | trinkets | championFlag3 | t_all73 | entry | Spine2 | -0,0,0 | 1.0 |
| penguin | trinkets | championFlag4 | t_all74 | entry | Spine2 | -0,0,0 | 1.0 |
| penguin | trinkets | chineseLantern | t_mal37 | entry | Spine2 | -0,0,0 | 1.0 |
| penguin | trinkets | chineseTalisman | t_mal31 | class fallback | Head | -0,0,0 | 1.0 |
| penguin | trinkets | chineseTalismanR |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| penguin | trinkets | comic | t_mal11 | entry | mount_Hand_R | -0,0,0 | 1.0 |
| penguin | trinkets | curseAnkh | t_mal46 | class fallback | Head | -0,0,0 | 1.0 |
| penguin | trinkets | doubleHorn | t_all66 | class fallback | Head | -0,0,0 | 1.0 |
| penguin | trinkets | frozenWing | t_mal56 | entry | Spine2 | -0,0,0 | 1.0 |
| penguin | trinkets | glasses | t_all1 | class fallback | Head | -0,0,0 | 1.0 |
| penguin | trinkets | groceryBag | t_all46 | entry | Hand_L | -0,0,0 | 1.0 |
| penguin | trinkets | legendTrinket | t_pgn60 | entry | Spine2 | -0,0,0 | 1.0 |
| penguin | trinkets | legendTrinketR | t_pgn61 | entry | Spine2 | -0,0,0 | 1.0 |
| penguin | trinkets | lollipop | t_all9 | class fallback | Head | -0,0,0 | 1.0 |
| penguin | trinkets | nerdGlasses | t_all4 | class fallback | Head | -0,0,0 | 1.0 |
| penguin | trinkets | partyWhistle | t_all7 | class fallback | Head | -0,0,0 | 1.0 |
| penguin | trinkets | poseidonTrinket | t_mal66 | entry | Spine2 | -0,0,0 | 1.0 |
| penguin | trinkets | quotationFlag |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| penguin | trinkets | redNose | t_all8 | class fallback | Head | -0,0,0 | 1.0 |
| penguin | trinkets | santaBag | t_mal15 | entry | Spine1 | -0,0,0 | 1.0 |
| penguin | trinkets | starGlasses | t_all3 | class fallback | Head | -0,0,0 | 1.0 |
| penguin | trinkets | sunGlasses | t_all2 | class fallback | Head | -0,0,0 | 1.0 |
| penguin | trinkets | AngleWing | t_all110 | entry | Spine2 | 0.2036,0.2319,-0.0008 | 0.699999988079071 |
| penguin | trinkets | AngleWing_Crimson | t_allhlw6 | entry | Spine2 | 0.2036,0.2319,-0.0008 | 0.699999988079071 |
| penguin | trinkets | AngleWing_Ghost | t_allhlw7 | entry | Spine2 | 0.2036,0.2319,-0.0008 | 0.699999988079071 |
| penguin | trinkets | AngleWing_Pumpkin | t_allhlw8 | entry | Spine2 | 0.2036,0.2319,-0.0008 | 0.699999988079071 |
| penguin | trinkets | AngleWing_Spectral | t_allhlw9 | entry | Spine2 | 0.2036,0.2319,-0.0008 | 0.699999988079071 |
| penguin | trinkets | aura_bloodmoon | t_all186 | class fallback | Head | -0,0,0 | 1.0 |
| penguin | trinkets | aura_undeadqueen | t_all185 | class fallback | Head | -0,0,0 | 1.0 |
| penguin | trinkets | Azure_Wing | t_all101 | entry | Spine2 | 0.1,0.25,0 | 1.0 |
| penguin | trinkets | championWing |  | inferred (Shade Wing's entry) | Spine2 | 0.1,0.25,0 | 1.0 |
| penguin | trinkets | daynightwing | t_all102 | entry | Spine2 | 0.1,0.25,0 | 1.0 |
| penguin | trinkets | devilWing |  | inferred (Shade Wing's entry) | Spine2 | 0.1,0.25,0 | 1.0 |
| penguin | trinkets | Ice_Wing | t_all77 | entry | Spine2 | 0.1,0.25,0 | 1.0 |
| penguin | trinkets | MoonlightRabbit | t_all142 | entry | Spine2 | 0.25,0.15,0 | 1.0 |
| penguin | trinkets | PumpkonHeadband | t_allhlw3 | entry | Spine2 | -0.0316,0.2982,-0.0162 | 0.36482229828834534 |
| penguin | trinkets | ReaperTrinket | t_allhlw5 | entry | Spine2 | -0.175478,0.203116,0.249523 | 0.6546868681907654 |
| penguin | trinkets | Shade_Wing | t_all78 | entry | Spine2 | 0.1,0.25,0 | 1.0 |
| penguin | trinkets | WhiteWing | t_all188 | entry | Spine2 | 0.0882,0.358,0.0377 | 1.0 |
| penguin | trinkets | WitchyWing | t_all147 | entry | Spine2 | -0,0.2,0 | 1.0 |
| penguin | accessories | afro | c_all11 | entry | Head | -0,0,0 | 1.0 |
| penguin | accessories | afroC | c_all12 | entry | Head | -0,0,0 | 1.0 |
| penguin | accessories | archMageHat | c_pgn40 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | archMageHatR | c_pgn41 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | archMageHatV | c_pgn42 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | artistHat | c_all39 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | astralHat | c_pgn31 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | astralHatR | c_pgn33 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | beggarHat | c_pgn5 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | cakeHat | c_all9 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | candyHat | c_all10 | entry | Head | -0,0,0 | 1.0 |
| penguin | accessories | championHelmet | c_all58 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | dragonHead | c_mal37 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | earmuff1 | c_all21 | entry | Head | -0,0,0 | 1.0 |
| penguin | accessories | earmuff2 | c_all22 | entry | Head | -0,0,0 | 1.0 |
| penguin | accessories | fanKingHat | c_all38 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | fanKingHat_Shine |  | class fallback (no code) | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | fireFighterHat | c_pgn25 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | franceHat | c_pgn65 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | frostHat | c_pgn32 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | frostHatR | c_pgn34 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | frozenCrown | c_all56 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | garland | c_pgn15 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | hallowBandana | c_pgn35 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | halloweenHat | c_pgn37 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | halo | c_all18 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | headphone1 | c_all23 | entry | Head | -0,0,0 | 1.0 |
| penguin | accessories | headphone2 | c_all24 | entry | Head | -0,0,0 | 1.0 |
| penguin | accessories | headphone3 | c_all25 | entry | Head | -0,0,0 | 1.0 |
| penguin | accessories | horn | c_all19 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | iceHat | c_pgn22 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | iceHatR | c_pgn24 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | krathongHat1 | c_all27 | entry | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | krathongHat2 | c_all28 | entry | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | legendHelmet | c_pgn60,c_pgn61 | entry | Head | -0,0,0 | 1.0 |
| penguin | accessories | mosquitoHat | c_pgn47 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | mosquitoHatR | c_pgn48 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | mummyHead | c_all46 | entry | Head | -0,0,0 | 1.0 |
| penguin | accessories | paperHat | c_all3 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | partyHatB | c_all7 | entry | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | partyHatR | c_all8 | entry | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | pirateBandana | c_all16 | entry | Head | -0,0,0 | 1.0 |
| penguin | accessories | pirateBandanaR | c_all26 | entry | Head | -0,0,0 | 1.0 |
| penguin | accessories | poseidonHelmet | c_all66 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | pvpHelmet | c_all43 | entry | Head | -0,0,0 | 1.0 |
| penguin | accessories | pvpHelmetR | c_all44 | entry | Head | -0,0,0 | 1.0 |
| penguin | accessories | quizHat | c_all37 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | redPandaHat | c_all1 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | regguHat | c_pgn36 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | royalHat | c_pgn50 | entry | Head | -0,0,0 | 1.0 |
| penguin | accessories | royalHatR | c_pgn52 | entry | Head | -0,0,0 | 1.0 |
| penguin | accessories | santaHat | c_all15 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | snowmanHead | c_all29 | entry | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | standardHat | c_pgn10 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | standardHatR | c_pgn11 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | standardHatV | c_pgn12 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | starHat | c_pgn21 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | starHatR | c_pgn23 | class fallback | Hat1 | -0,0,0 | 1.0 |
| penguin | accessories | superStarWig | c_pgn45 | entry | Head | -0,0,0 | 1.0 |
| penguin | accessories | veggieHat | c_pgn19 | entry | Head | -0,0,0 | 1.0 |
| penguin | accessories | CactonHeadband | c_allhlw1 | entry | Head | 0.0878,-0.0556,0.001 | 0.2768999934196472 |
| penguin | accessories | ChopperTrinket | c_allhlw4 | entry | Head | 0.1695,-0.0093,0.011 | 0.49079787731170654 |
| penguin | accessories | CoconHeadband | c_allhlw2 | entry | Head | 0.1024,-0.0443,0.0092 | 0.33239999413490295 |
| penguin | weapons | archScepter | w_pgn40 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | archScepterR |  | class fallback (no code) | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | archScepterV | w_pgn42 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | astralScepter | w_pgn31 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | astralScepterR | w_pgn33 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | bdWeapon | w_pgn19 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | championScepter | w_pgn58 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | commonWand | w_pgn2 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | eclipseScepter | w_pgn79 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | fireExtinguisher | w_pgn25 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | flamingScepter | w_pgn81 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | franceSpyglass | w_pgn65 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | frostStaff | w_pgn32 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | frostStaffR | w_pgn34 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | frozenScepter | w_pgn56 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | goldenScepter | w_pgn49 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | griffinStaff | w_pgn39 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | halloweenStaff | w_pgn37 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | hallowLattern | w_pgn35 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | heartScepter | w_pgn14 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | iceStaff | w_pgn22 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | iceStaffR | w_pgn24 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | legendScepter | w_pgn60 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | lightSceptor |  | class fallback (no code) | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | mosquitoStaff | w_pgn47 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | mosquitoStaffR | w_pgn48 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | mummyStaff | w_pgn46 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | noviceWand | w_pgn1 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | paperCup | w_pgn5 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | paperStaff | w_pgn3 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | poseidonScepter | w_pgn66 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | pvpScepter | w_pgn43 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | pvpScepterR | w_pgn44 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | regguStaff | w_pgn36 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | royalScepter | w_pgn50 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | royalScepterR | w_pgn52 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | shakerWand | w_pgn10,w_pgn15 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | specialScepter | w_pgn59 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | standardWand | w_pgn51,w_pgn61 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | standardWandR | w_pgn11 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | standardWandV | w_pgn12 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | starRecord | w_pgn45 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | starScepter | w_pgn21 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | starScepterR | w_pgn23 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| penguin | weapons | timeScepter | w_pgn69 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| rabbit | trinkets | bell | t_fem2 | entry | Spine1 | -0,0,0 | 1.0 |
| rabbit | trinkets | bugAntenna | t_all6 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | trinkets | championFlag1 | t_all71 | entry | Spine2 | -0,0,0 | 1.0 |
| rabbit | trinkets | championFlag2 | t_all72 | entry | Spine2 | -0,0,0 | 1.0 |
| rabbit | trinkets | championFlag3 | t_all73 | entry | Spine2 | -0,0,0 | 1.0 |
| rabbit | trinkets | championFlag4 | t_all74 | entry | Spine2 | -0,0,0 | 1.0 |
| rabbit | trinkets | chineseLantern | t_fem37 | entry | Spine2 | -0,0,0 | 1.0 |
| rabbit | trinkets | chineseTalisman |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| rabbit | trinkets | chineseTalismanR | t_fem31 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | trinkets | deerHorn | t_fem15 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | trinkets | doubleHorn | t_all66 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | trinkets | frozenMask | t_fem56 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | trinkets | glasses | t_all1 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | trinkets | groceryBag | t_all46 | entry | Hand_L | -0,0,0 | 0.699999988079071 |
| rabbit | trinkets | legendTrinket | t_rab60 | entry | root | -0,0,0 | 1.0 |
| rabbit | trinkets | legendTrinketR | t_rab61 | entry | root | -0,0,0 | 1.0 |
| rabbit | trinkets | lollipop | t_all9 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | trinkets | magazine | t_fem11 | entry | mountHand_L | -0,0,0 | 1.0 |
| rabbit | trinkets | maohWings | t_fem46 | entry | Spine1 | -0,0,0 | 1.0 |
| rabbit | trinkets | nerdGlasses | t_all4 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | trinkets | partyWhistle | t_all7 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | trinkets | poseidonTrinket | t_fem66 | entry | Spine1 | -0,0,0 | 1.0 |
| rabbit | trinkets | quotationFlag |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| rabbit | trinkets | redNose | t_all8 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | trinkets | starGlasses | t_all3 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | trinkets | sunGlasses | t_all2 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | trinkets | AngleWing | t_all110 | entry | Spine1 | 0.0747,-0.0148,-0.1236 | 0.699999988079071 |
| rabbit | trinkets | AngleWing_Crimson | t_allhlw6 | entry | Spine1 | 0.0747,-0.0148,-0.1236 | 0.699999988079071 |
| rabbit | trinkets | AngleWing_Ghost | t_allhlw7 | entry | Spine1 | 0.0747,-0.0148,-0.1236 | 0.699999988079071 |
| rabbit | trinkets | AngleWing_Pumpkin | t_allhlw8 | entry | Spine1 | 0.0747,-0.0148,-0.1236 | 0.699999988079071 |
| rabbit | trinkets | AngleWing_Spectral | t_allhlw9 | entry | Spine1 | 0.0747,-0.0148,-0.1236 | 0.699999988079071 |
| rabbit | trinkets | aura_bloodmoon | t_all186 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | trinkets | aura_undeadqueen | t_all185 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | trinkets | Azure_Wing | t_all101 | entry | Spine1 | -0,0,-0.25 | 1.0 |
| rabbit | trinkets | championWing |  | inferred (Shade Wing's entry) | Spine1 | -0,0,-0.25 | 1.0 |
| rabbit | trinkets | daynightwing | t_all102 | entry | Spine1 | -0,0,-0.25 | 1.0 |
| rabbit | trinkets | devilWing |  | inferred (Shade Wing's entry) | Spine1 | -0,0,-0.25 | 1.0 |
| rabbit | trinkets | Ice_Wing | t_all77 | entry | Spine1 | -0,0,-0.25 | 1.0 |
| rabbit | trinkets | MoonlightRabbit | t_all142 | entry | Spine1 | -0,0,0 | 1.0 |
| rabbit | trinkets | PumpkonHeadband | t_allhlw3 | entry | Spine2 | -0.0021,0.2098,-0.0157 | 0.3031734228134155 |
| rabbit | trinkets | ReaperTrinket | t_allhlw5 | entry | Spine2 | -0.34027,0.205082,0.188334 | 0.8059874176979065 |
| rabbit | trinkets | Shade_Wing | t_all78 | entry | Spine1 | -0,0,-0.25 | 1.0 |
| rabbit | trinkets | WhiteWing | t_all188 | entry | Spine1 | -0.0027,-0.0087,-0.1998 | 1.0 |
| rabbit | trinkets | WitchyWing | t_all147 | entry | Spine1 | -0,0,-0.15 | 1.0 |
| rabbit | accessories | afro | c_all11 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | afroC | c_all12 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | alchemistHat | c_rab31 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | alchemistHatR | c_rab33 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | antHelmet | c_rab47 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | antHelmetR | c_rab48,c_rab61 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | artistHat | c_all39 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | cakeHat | c_all9 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | candyHat | c_all10 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | championHelmet | c_all58 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | earmuff1 | c_all21 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | earmuff2 | c_all22 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | fanKingHat | c_all38 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | fanKingHat_Shine |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| rabbit | accessories | flogBand | c_rab5 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | flowerBand | c_fem11 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | frozenCrown | c_all56 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | halloweenHat | c_rab37 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | hallowHat | c_rab35 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | halo | c_all18 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | headphone1 | c_all23 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | headphone2 | c_all24 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | headphone3 | c_all25 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | horn | c_all19 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | italusHat | c_rab36 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | krathongHat1 | c_all27 | entry | Head | -0,0,0 | 1.0 |
| rabbit | accessories | krathongHat2 | c_all28 | entry | Head | -0,0,0 | 1.0 |
| rabbit | accessories | legendHelmet | c_rab60 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | lionHead | c_fem37 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | magistrateHat | c_rab40 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | magistrateHatR | c_rab41 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | magistrateHatV | c_rab42,c_rab51 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | medicHat | c_rab25 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | merchantHat | c_rab32 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | merchantHatR | c_rab34 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | moonGoddessTiara | c_rab80 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | mummyHead | c_all46 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | nurseCap | c_rab21 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | nurseCapR | c_rab23 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | paperHat | c_all3 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | partyHatB | c_all7 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | partyHatR | c_all8 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | pirateBandana | c_all16 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | pirateBandanaR | c_all26 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | poseidonHelmet | c_all66 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | pvpHelmet | c_all43 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | pvpHelmetR | c_all44 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | quizHat | c_all37 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | redPandaHat | c_all1 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | royalHat | c_rab50 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | royalHatR | c_rab52 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | santaHat | c_all15 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | snowmanHead | c_all29 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | spainHat | c_rab65 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | standardHat | c_rab10 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | standardHatR | c_rab11 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | standardHatV | c_rab12 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | summerHat | c_rab15 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | superStarHood | c_rab45 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | traderHat | c_rab22 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | traderHatR | c_rab24 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | veggieHat | c_rab19 | class fallback | Head | -0,0,0 | 1.0 |
| rabbit | accessories | CactonHeadband | c_allhlw1 | entry | Head | 0.1549,-0.0287,0.0052 | 0.23970000445842743 |
| rabbit | accessories | ChopperTrinket | c_allhlw4 | entry | Head | 0.277914,0.0100188,0.000542012 | 0.42003133893013 |
| rabbit | accessories | CoconHeadband | c_allhlw2 | entry | Head | 0.163,-0.0189,0.0036 | 0.28450000286102295 |
| rabbit | weapons | alchemistGun | w_rab31 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | alchemistGunR | w_rab33 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | antShotgun | w_rab47 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | antShotgunR | w_rab48 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | bdWeapon | w_rab19 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | championGun | w_rab58 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | commonGun | w_rab2 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | dragunovGun |  | class fallback (no code) | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | eclipseRifle | w_rab79 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | flowerGun | w_rab39 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | frozenGun | w_rab56 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | goldenGun | w_rab49 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | halloweenRifle | w_rab37 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | hallowGun | w_rab35 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | heartGun | w_rab14 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | italusRevolver | w_rab36 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | keytar | w_rab45 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | legendGun | w_rab60 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | magistrateGun | w_rab40 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | magistrateGunR | w_rab41 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | magistrateGunV | w_rab42 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | medicGun | w_rab25 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | merchantGun | w_rab32 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | merchantGunR | w_rab34 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | mummyShotgun | w_rab46 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | noviceGun | w_rab1 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | nurseGun | w_rab21 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | nurseGunR | w_rab23 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | paperGun | w_rab3 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | poseidonGun | w_rab66 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | pvpBow | w_rab43 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | pvpBowR | w_rab44 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | royalGun | w_rab50 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | royalGunR | w_rab52 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | spainMusket | w_rab65 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | specialGun | w_rab59 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | standardGun | w_rab61 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | standardGunR | w_rab11 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | standardGunV | w_rab12 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | timeShotgun | w_rab69 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | traderGun | w_rab22 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | traderGunR | w_rab24 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | umbrella | w_rab5 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| rabbit | weapons | waterGun | w_rab10,w_rab15 | class fallback | mountHand_R | -0,0,0 | 1.0 |
| sheep | trinkets | bell | t_fem2 | entry | Spine2 | -0,0,0 | 1.0 |
| sheep | trinkets | bugAntenna | t_all6 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | trinkets | championFlag1 | t_all71 | entry | Spine2 | -0,0,0 | 1.0 |
| sheep | trinkets | championFlag2 | t_all72 | entry | Spine2 | -0,0,0 | 1.0 |
| sheep | trinkets | championFlag3 | t_all73 | entry | Spine2 | -0,0,0 | 1.0 |
| sheep | trinkets | championFlag4 | t_all74 | entry | Spine2 | -0,0,0 | 1.0 |
| sheep | trinkets | chineseLantern | t_fem37 | entry | Spine2 | -0,0,0 | 1.0 |
| sheep | trinkets | chineseTalisman |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| sheep | trinkets | chineseTalismanR | t_fem31 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | trinkets | deerHorn | t_fem15 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | trinkets | doubleHorn | t_all66 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | trinkets | frozenMask | t_fem56 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | trinkets | glasses | t_all1 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | trinkets | groceryBag | t_all46 | entry | Hand_R | -0,0,0 | 0.800000011920929 |
| sheep | trinkets | legendTrinket | t_shp60 | entry | Spine2 | -0,0,0 | 1.0 |
| sheep | trinkets | legendTrinketR | t_shp61 | entry | Spine2 | -0,0,0 | 1.0 |
| sheep | trinkets | lollipop | t_all9 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | trinkets | magazine | t_fem11 | entry | mount_Hand_R | -0,0,0 | 1.0 |
| sheep | trinkets | maohWings | t_fem46 | entry | Spine2 | -0,0,0 | 1.0 |
| sheep | trinkets | nerdGlasses | t_all4 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | trinkets | partyWhistle | t_all7 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | trinkets | poseidonTrinket | t_fem66 | entry | Spine2 | -0,0,0 | 1.0 |
| sheep | trinkets | quotationFlag |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| sheep | trinkets | redNose | t_all8 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | trinkets | starGlasses | t_all3 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | trinkets | sunGlasses | t_all2 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | trinkets | AngleWing | t_all110 | entry | Spine1 | 0.1,0.125,0.0036 | 0.8500000238418579 |
| sheep | trinkets | AngleWing_Crimson | t_allhlw6 | entry | Spine1 | 0.1,0.125,0.0036 | 0.8500000238418579 |
| sheep | trinkets | AngleWing_Ghost | t_allhlw7 | entry | Spine1 | 0.1,0.125,0.0036 | 0.8500000238418579 |
| sheep | trinkets | AngleWing_Pumpkin | t_allhlw8 | entry | Spine1 | 0.1,0.125,0.0036 | 0.8500000238418579 |
| sheep | trinkets | AngleWing_Spectral | t_allhlw9 | entry | Spine1 | 0.1,0.125,0.0036 | 0.8500000238418579 |
| sheep | trinkets | aura_bloodmoon | t_all186 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | trinkets | aura_undeadqueen | t_all185 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | trinkets | Azure_Wing | t_all101 | entry | Spine2 | -0,0.25,0 | 1.0 |
| sheep | trinkets | championWing |  | inferred (Shade Wing's entry) | Spine2 | -0,0.25,0 | 1.0 |
| sheep | trinkets | daynightwing | t_all102 | entry | Spine2 | -0,0.25,0 | 1.0 |
| sheep | trinkets | devilWing |  | inferred (Shade Wing's entry) | Spine2 | -0,0.25,0 | 1.0 |
| sheep | trinkets | Ice_Wing | t_all77 | entry | Spine2 | -0,0.25,0 | 1.0 |
| sheep | trinkets | MoonlightRabbit | t_all142 | entry | Spine2 | 0.15,0.1,0 | 1.0 |
| sheep | trinkets | PumpkonHeadband | t_allhlw3 | entry | Spine2 | 0.00993386,0.209625,-4.65661e-10 | 0.3647150695323944 |
| sheep | trinkets | ReaperTrinket | t_allhlw5 | entry | Spine2 | -0.225731,0.224447,0.236771 | 0.7907245755195618 |
| sheep | trinkets | Shade_Wing | t_all78 | entry | Spine2 | -0,0.25,0 | 1.0 |
| sheep | trinkets | WhiteWing | t_all188 | entry | Spine1 | -0.0018,0.2367,0 | 1.0 |
| sheep | trinkets | WitchyWing | t_all147 | entry | Spine2 | -0,0.15,0 | 1.0 |
| sheep | accessories | afro | c_all11 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | afroC | c_all12 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | artistHat | c_all39 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | cakeHat | c_all9 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | candyHat | c_all10 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | championHelmet | c_all58 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | clericHat | c_shp21 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | clericHatR | c_shp23 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | divineGoddessCrown | c_shp80 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | earmuff1 | c_all21 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | earmuff2 | c_all22 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | enchantBand | c_shp32 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | enchantBandR | c_shp34 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | fanKingHat | c_all38 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | fanKingHat_Shine |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| sheep | accessories | flowerBand | c_fem11 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | frozenCrown | c_all56 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | halloweenHat | c_shp37 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | hallowFlower | c_shp35,c_shp51 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | halo | c_all18 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | headphone1 | c_all23 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | headphone2 | c_all24 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | headphone3 | c_all25 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | hierophantHat | c_shp31 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | hierophantHatR | c_shp33 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | holyHat | c_shp40 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | holyHatR | c_shp41 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | holyHatV | c_shp42 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | horn | c_all19 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | krathongHat1 | c_all27 | entry | Head | -0,0,0 | 1.0 |
| sheep | accessories | krathongHat2 | c_all28 | entry | Head | -0,0,0 | 1.0 |
| sheep | accessories | kuruHat | c_shp36 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | legendHelmet | c_shp60 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | lightBand | c_shp22 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | lightBandR | c_shp24 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | lionHead | c_fem37 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | mothHat | c_shp47 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | mothHatR | c_shp48 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | mummyHead | c_all46 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | paperHat | c_all3 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | partyHatB | c_all7 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | partyHatR | c_all8 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | pirateBandana | c_all16 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | pirateBandanaR | c_all26 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | poseidonHelmet | c_all66 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | pvpHelmet | c_all43 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | pvpHelmetR | c_all44 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | quizHat | c_all37 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | redPandaHat | c_all1 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | royalHat | c_shp50 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | royalHatR | c_shp52 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | russiaHat | c_shp61,c_shp65 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | santaHat | c_all15 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | sheepHat | c_shp5 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | snowmanHead | c_all29 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | summerHat | c_shp15 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | superStarHat | c_shp45 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | veggieHat | c_shp19 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | waitressBand | c_shp25 | class fallback | Head | -0,0,0 | 1.0 |
| sheep | accessories | CactonHeadband | c_allhlw1 | entry | Head | 0.0302353,-0.0104214,0.0041745 | 0.30000001192092896 |
| sheep | accessories | ChopperTrinket | c_allhlw4 | entry | Head | -0.3195,-0.0069,0.0044 | 0.38710564374923706 |
| sheep | accessories | CoconHeadband | c_allhlw2 | entry | Head | 0.1034,-0.0003,0.0042 | 0.2840999960899353 |
| sheep | weapons | bdWeapon | w_shp19 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | championCodex | w_shp58 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | clericBook | w_shp21 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | clericBookR | w_shp23 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | commonBook | w_shp2 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | diary | w_shp15 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | eclipseCodex | w_shp79 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | enchanterScroll | w_shp32 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | enchanterScrollR | w_shp34 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | flamingBook | w_shp82 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | flamingGuard | w_shp84 | entry | Arm_L | -0,0,0 | 1.0 |
| sheep | weapons | flamingScroll | w_shp81 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | flamingShield | w_shp83 | entry | Arm_L | -0,0,0 | 1.0 |
| sheep | weapons | frozenCone | w_shp56 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | goldenCodex | w_shp49 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | hallowBaby | w_shp35 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | halloweenLantern | w_shp37 | entry | mount_Hand_L | 0.1,0,0 | 1.0 |
| sheep | weapons | heartBox | w_shp14 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | hierophantBook | w_shp31 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | hierophantBookR | w_shp33 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | holyCodex | w_shp40 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | holyCodexR | w_shp41 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | holyCodexV | w_shp42 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | kuruScroll | w_shp36 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | legendHarp | w_shp60 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | lightScroll | w_shp22 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | lightScrollR | w_shp24 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | mothLatern | w_shp47 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | mothLaternR | w_shp48 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | mummyBook | w_shp46 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | noviceBook | w_shp1 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | paperBoat | w_shp3 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | poseidonBook | w_shp61,w_shp66 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | pvpBook | w_shp43 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | pvpBookR | w_shp44 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | royalCodex | w_shp50 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | royalCodexR | w_shp52 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | russiaMatryoshka | w_shp65 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | sheepDoll | w_shp5 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | specialOrb | w_shp59 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | standardBook | w_shp10 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | standardBookR | w_shp11 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | standardBookV | w_shp12 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | starMicrophone | w_shp45 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | timeCodex | w_shp69 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | waitressTray | w_shp25 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| sheep | weapons | wolfDoll | w_shp39 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | trinkets | bugAntenna | t_all6 | class fallback | Head | -0,0,0 | 1.0 |
| whale | trinkets | championFlag1 | t_all71 | entry | Spine2 | -0,0,0 | 1.0 |
| whale | trinkets | championFlag2 | t_all72 | entry | Spine2 | -0,0,0 | 1.0 |
| whale | trinkets | championFlag3 | t_all73 | entry | Spine2 | -0,0,0 | 1.0 |
| whale | trinkets | championFlag4 | t_all74 | entry | Spine2 | -0,0,0 | 1.0 |
| whale | trinkets | chineseLantern | t_mal37 | entry | Spine2 | -0,0,0 | 1.0 |
| whale | trinkets | chineseTalisman | t_mal31 | class fallback | Head | -0,0,0 | 1.0 |
| whale | trinkets | chineseTalismanR |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| whale | trinkets | comic | t_mal11 | entry | Hand_R | -0,0,0 | 1.0 |
| whale | trinkets | curseAnkh | t_mal46 | class fallback | Head | -0,0,0 | 1.0 |
| whale | trinkets | doubleHorn | t_all66 | class fallback | Head | -0,0,0 | 1.0 |
| whale | trinkets | frozenWing | t_mal56 | entry | Spine2 | -0,0,0 | 1.0 |
| whale | trinkets | glasses | t_all1 | class fallback | Head | -0,0,0 | 1.0 |
| whale | trinkets | groceryBag | t_all46 | entry | Hand_R | -0,0,0 | 1.2000000476837158 |
| whale | trinkets | legendTrinket | t_whl60 | entry | Spine1 | -0,0,0 | 1.0 |
| whale | trinkets | legendTrinketR |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| whale | trinkets | lollipop | t_all9 | class fallback | Head | -0,0,0 | 1.0 |
| whale | trinkets | nerdGlasses | t_all4 | class fallback | Head | -0,0,0 | 1.0 |
| whale | trinkets | partyWhistle | t_all7 | class fallback | Head | -0,0,0 | 1.0 |
| whale | trinkets | poseidonTrinket | t_mal66 | entry | Spine2 | -0,0,0 | 1.0 |
| whale | trinkets | quotationFlag |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| whale | trinkets | redNose | t_all8 | class fallback | Head | -0,0,0 | 1.0 |
| whale | trinkets | santaBag | t_mal15 | entry | Spine1 | -0,0,0 | 1.0 |
| whale | trinkets | starGlasses | t_all3 | class fallback | Head | -0,0,0 | 1.0 |
| whale | trinkets | sunGlasses | t_all2 | class fallback | Head | -0,0,0 | 1.0 |
| whale | trinkets | AngleWing | t_all110 | entry | Spine1 | 0.494,0.734,0 | 2.0 |
| whale | trinkets | AngleWing_Crimson | t_allhlw6 | entry | Spine1 | 0.494,0.734,0 | 2.0 |
| whale | trinkets | AngleWing_Ghost | t_allhlw7 | entry | Spine1 | 0.494,0.734,0 | 2.0 |
| whale | trinkets | AngleWing_Pumpkin | t_allhlw8 | entry | Spine1 | 0.494,0.734,0 | 2.0 |
| whale | trinkets | AngleWing_Spectral | t_allhlw9 | entry | Spine1 | 0.494,0.734,0 | 2.0 |
| whale | trinkets | aura_bloodmoon | t_all186 | class fallback | Head | -0,0,0 | 1.0 |
| whale | trinkets | aura_undeadqueen | t_all185 | class fallback | Head | -0,0,0 | 1.0 |
| whale | trinkets | Azure_Wing | t_all101 | entry | Spine2 | 0.5,1,0 | 2.0 |
| whale | trinkets | championWing |  | inferred (Shade Wing's entry) | Spine2 | 0.5,1,0 | 2.0 |
| whale | trinkets | daynightwing | t_all102 | entry | Spine2 | 0.2,1,0 | 2.0 |
| whale | trinkets | devilWing |  | inferred (Shade Wing's entry) | Spine2 | 0.5,1,0 | 2.0 |
| whale | trinkets | Ice_Wing | t_all77 | entry | Spine2 | 0.5,1,0 | 2.0 |
| whale | trinkets | MoonlightRabbit | t_all142 | entry | Spine2 | 0.75,0.75,0 | 2.0 |
| whale | trinkets | PumpkonHeadband | t_allhlw3 | entry | Spine2 | 0.1132,0.9958,0 | 0.8835999965667725 |
| whale | trinkets | ReaperTrinket | t_allhlw5 | entry | Spine2 | -0.0962059,0.904866,0.361153 | 1.2593027353286743 |
| whale | trinkets | Shade_Wing | t_all78 | entry | Spine2 | 0.5,1,0 | 2.0 |
| whale | trinkets | WhiteWing | t_all188 | entry | Spine1 | 0.498,0.9269,0 | 2.0 |
| whale | trinkets | WitchyWing | t_all147 | entry | Spine2 | 0.5,1,0 | 2.0 |
| whale | accessories | afro | c_all11 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | afroC | c_all12 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | aquaHelmet | c_whl31 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | aquaHelmetR | c_whl33 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | artistHat | c_all39 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | cakeHat | c_all9 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | candyHat | c_all10 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | championHelmet | c_all58 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | chefHat | c_whl25 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | dragonHead | c_mal37 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | earmuff1 | c_all21 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | earmuff2 | c_all22 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | fanKingHat | c_all38 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | fanKingHat_Shine |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| whale | accessories | frozenCrown | c_all56 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | hallowAnchor | c_whl35 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | halloweenHat | c_whl37 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | halo | c_all18 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | headphone1 | c_all23 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | headphone2 | c_all24 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | headphone3 | c_all25 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | horn | c_all19 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | justiceHelmet | c_whl40 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | justiceHelmetR | c_whl41 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | justiceHelmetV | c_whl42 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | koreaHat | c_whl65 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | krathongHat1 | c_all27 | entry | Head | -0,0,0 | 1.0 |
| whale | accessories | krathongHat2 | c_all28 | entry | Head | -0,0,0 | 1.0 |
| whale | accessories | ladybugHelmet | c_whl47 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | ladybugHelmetR | c_whl48 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | lancerHelmet | c_whl21 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | lancerHelmetR | c_whl23 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | legendHelmet | c_whl60,c_whl61 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | melonStem | c_whl15 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | mummyHead | c_all46 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | paperHat | c_all3 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | partisanHood | c_whl22 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | partisanHoodR | c_whl24 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | partyHatB | c_all7 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | partyHatR | c_all8 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | pirateBandana | c_all16 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | pirateBandanaR | c_all26 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | poseidonHelmet | c_all66 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | pvpHelmet | c_all43 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | pvpHelmetR | c_all44 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | quizHat | c_all37 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | razanBandana | c_whl36 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | redPandaHat | c_all1 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | royalHelmet | c_whl50 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | royalHelmetR | c_whl51,c_whl52 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | santaHat | c_all15 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | snowmanHead | c_all29 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | superStarHat | c_whl45 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | swimGoggle | c_whl5 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | templarHood | c_whl32 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | templarHoodR | c_whl34 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | veggieHat | c_whl19 | class fallback | Head | -0,0,0 | 1.0 |
| whale | accessories | CactonHeadband | c_allhlw1 | entry | Head | -0.3544,-0.1739,0.0158 | 1.721695065498352 |
| whale | accessories | ChopperTrinket | c_allhlw4 | entry | Head | 0.5309,-0.1361,0.0442 | 1.7722543478012085 |
| whale | accessories | CoconHeadband | c_allhlw2 | entry | Head | -0.2439,-0.1763,0.0434 | 1.7015609741210938 |
| whale | weapons | ammoniteLance | w_whl39 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | ammoniteShield | w_whl39 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | aquaLance | w_whl31 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | aquaLanceR | w_whl33 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | aquaShield | w_whl31 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | aquaShieldR | w_whl33 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | bdLance | w_whl19 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | bdShield | w_whl19 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | beachBucket | w_whl5 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | beachShovel | w_whl5 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | championLance | w_whl58 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | championShield | w_whl58 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | chefLance | w_whl25 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | chefShield | w_whl25 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | commonLance |  | class fallback (no code) | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | commonShield |  | class fallback (no code) | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | eclipseLance | w_whl79 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | eclipseShield | w_whl79 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | frozenLance | w_whl56 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | frozenShield | w_whl56 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | goldenLance | w_whl49 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | goldenShield | w_whl49 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | hallowCleaver | w_whl35 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | halloweenShield | w_whl37 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | halloweenSpear | w_whl37 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | hallowShield | w_whl35 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | heartLance | w_whl14 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | heartShield | w_whl14 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | justiceLance | w_whl40 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | justiceLanceR | w_whl41 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | justiceLanceV | w_whl42 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | justiceShield | w_whl40 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | justiceShieldR | w_whl41 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | justiceShieldV | w_whl42 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | koreaLance | w_whl65 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | koreaShield | w_whl65 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | ladybugLance | w_whl47 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | ladybugLanceR | w_whl48,w_whl61 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | ladybugShield | w_whl47 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | ladybugShieldR | w_whl48,w_whl61 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | lancerLance | w_whl21 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | lancerLanceR | w_whl23 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | lancerShield | w_whl21 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | lancerShieldR | w_whl23 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | legendLance | w_whl60 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | legendShield | w_whl60 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | mummyLance | w_whl46 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | mummyShield | w_whl46 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | noviceLance | w_whl1 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | noviceShield | w_whl1 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | paperLance | w_whl3 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | paperShield | w_whl3 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | partisanLance | w_whl22 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | partisanLanceR | w_whl24 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | partisanShield | w_whl22 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | partisanShieldR | w_whl24 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | poseidonShield | w_whl66 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | poseidonSpear | w_whl66 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | pvpLance | w_whl43 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | pvpLanceR | w_whl44 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | pvpShield | w_whl43 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | pvpShieldR | w_whl44 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | razanAnmil | w_whl36 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | razanHammer | w_whl36 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | royalLance | w_whl50 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | royalLanceR | w_whl52 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | royalShield | w_whl50 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | royalShieldR | w_whl52 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | specialLance | w_whl59 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | specialShield | w_whl59 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | standardLance | w_whl51 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | standardLanceR | w_whl11 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | standardLanceV | w_whl12 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | standardShield | w_whl51 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | standardShieldR | w_whl11 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | standardShieldV | w_whl12 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | starDisc | w_whl45 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | starMicrophone | w_whl45 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | templarLance | w_whl32 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | templarLanceR | w_whl34 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | templarShield | w_whl32 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | templarShieldR | w_whl34 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | timeLance | w_whl69 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | timeShield | w_whl69 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | toyLance | w_whl10,w_whl15 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| whale | weapons | toyShield | w_whl10,w_whl15 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | trinkets | bugAntenna | t_all6 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | trinkets | championFlag1 | t_all71 | entry | Spine2 | -0,0,0 | 1.0 |
| wolf | trinkets | championFlag2 | t_all72 | entry | Spine2 | -0,0,0 | 1.0 |
| wolf | trinkets | championFlag3 | t_all73 | entry | Spine2 | -0,0,0 | 1.0 |
| wolf | trinkets | championFlag4 | t_all74 | entry | Spine2 | -0,0,0 | 1.0 |
| wolf | trinkets | chineseLantern | t_mal37 | entry | Spine2 | -0,0,0 | 1.0 |
| wolf | trinkets | chineseTalisman | t_mal31 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | trinkets | chineseTalismanR |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| wolf | trinkets | comic | t_mal11 | entry | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | trinkets | curseAnkh | t_mal46 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | trinkets | doubleHorn | t_all66 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | trinkets | frozenWing | t_mal56 | entry | Spine2 | -0,0,0 | 1.0 |
| wolf | trinkets | glasses | t_all1 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | trinkets | groceryBag | t_all46 | entry | Hand_R | -0,0,0 | 1.0 |
| wolf | trinkets | legendTrinket | t_wlf60 | entry | Spine1 | -0,0,0 | 1.0 |
| wolf | trinkets | legendTrinketR |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| wolf | trinkets | lollipop | t_all9 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | trinkets | nerdGlasses | t_all4 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | trinkets | partyWhistle | t_all7 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | trinkets | poseidonTrinket | t_mal66 | entry | Spine2 | -0,0,0 | 1.0 |
| wolf | trinkets | quotationFlag |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| wolf | trinkets | redNose | t_all8 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | trinkets | santaBag | t_mal15 | entry | Spine1 | -0,0,0 | 1.0 |
| wolf | trinkets | starGlasses | t_all3 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | trinkets | sunGlasses | t_all2 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | trinkets | AngleWing | t_all110 | entry | Spine2 | 0.15,0.247,-0.002 | 1.0 |
| wolf | trinkets | AngleWing_Crimson | t_allhlw6 | entry | Spine2 | 0.15,0.247,-0.002 | 1.0 |
| wolf | trinkets | AngleWing_Ghost | t_allhlw7 | entry | Spine2 | 0.15,0.247,-0.002 | 1.0 |
| wolf | trinkets | AngleWing_Pumpkin | t_allhlw8 | entry | Spine2 | 0.15,0.247,-0.002 | 1.0 |
| wolf | trinkets | AngleWing_Spectral | t_allhlw9 | entry | Spine2 | 0.15,0.247,-0.002 | 1.0 |
| wolf | trinkets | aura_bloodmoon | t_all186 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | trinkets | aura_undeadqueen | t_all185 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | trinkets | Azure_Wing | t_all101 | entry | Spine2 | 0.15,0.25,0 | 1.0 |
| wolf | trinkets | championWing |  | inferred (Shade Wing's entry) | Spine2 | 0.15,0.25,0 | 1.0 |
| wolf | trinkets | daynightwing | t_all102 | entry | Spine2 | 0.15,0.25,0 | 1.0 |
| wolf | trinkets | devilWing |  | inferred (Shade Wing's entry) | Spine2 | 0.15,0.25,0 | 1.0 |
| wolf | trinkets | Ice_Wing | t_all77 | entry | Spine2 | 0.15,0.25,0 | 1.0 |
| wolf | trinkets | MoonlightRabbit | t_all142 | entry | Spine2 | 0.25,0.2,0 | 1.0 |
| wolf | trinkets | PumpkonHeadband | t_allhlw3 | entry | Spine2 | -0.0325111,0.292268,0.165355 | 0.4268050193786621 |
| wolf | trinkets | ReaperTrinket | t_allhlw5 | entry | Spine2 | -0.284174,0.0838864,0.344953 | 0.8993280529975891 |
| wolf | trinkets | Shade_Wing | t_all78 | entry | Spine2 | 0.15,0.25,0 | 1.0 |
| wolf | trinkets | WhiteWing | t_all188 | entry | Spine2 | 0.1323,0.4064,0.0882 | 1.0 |
| wolf | trinkets | WitchyWing | t_all147 | entry | Spine2 | -0,0.25,0 | 1.0 |
| wolf | accessories | afro | c_all11 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | afroC | c_all12 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | artistHat | c_all39 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | bladeBandana | c_wlf32 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | bladeBandanaR | c_wlf34 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | butlerCap | c_wlf25 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | cakeHat | c_all9 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | candyHat | c_all10 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | championHelmet | c_all58 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | dragonHead | c_mal37 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | earmuff1 | c_all21 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | earmuff2 | c_all22 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | fanKingHat | c_all38 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | fanKingHat_Shine |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| wolf | accessories | fcBandana | c_wlf5,c_wlf61 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | frozenCrown | c_all56 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | halloweenHat | c_wlf37 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | hallowMask | c_wlf35 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | halo | c_all18 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | headPhone1 |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| wolf | accessories | headPhone2 |  | class fallback (no code) | Head | -0,0,0 | 1.0 |
| wolf | accessories | headphone3 | c_all25 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | heroHelmet | c_wlf40 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | heroHelmetR | c_wlf41 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | heroHelmetV | c_wlf42 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | horn | c_all19 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | krathongHat1 | c_all27 | entry | Head | -0,0,0 | 1.0 |
| wolf | accessories | krathongHat2 | c_all28 | entry | Head | -0,0,0 | 1.0 |
| wolf | accessories | legendHelmet | c_wlf60 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | ligerMask | c_wlf36 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | mummyHead | c_all46 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | paladinHelmet | c_wlf31 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | paladinHelmetR | c_wlf33 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | paperHat | c_all3 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | partyHatB | c_all7 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | partyHatR | c_all8 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | pirateBandana | c_all16 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | pirateBandanaR | c_all26 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | poseidonHelmet | c_all66,c_wlf51 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | pvpHelmet | c_all43 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | pvpHelmetR | c_all44 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | quizHat | c_all37 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | redPandaHat | c_all1 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | royalHelmet | c_wlf50 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | royalHelmetR | c_wlf52 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | santaHat | c_all15 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | scorpionHelmet | c_wlf47 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | scorpionHelmetR | c_wlf48 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | simpleBandana | c_wlf1 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | simpleBandanaR | c_wlf10,c_wlf11 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | snowmanHead | c_all29 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | soldierHelmet | c_wlf21 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | soldierHelmetR | c_wlf23 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | summerGlasses | c_wlf15 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | superStarHat | c_wlf45 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | thaiHelmet | c_wlf65 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | vagabondBandana | c_wlf22 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | vagabondBandanaR | c_wlf24 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | veggieHat | c_wlf19 | class fallback | Head | -0,0,0 | 1.0 |
| wolf | accessories | CactonHeadband | c_allhlw1 | entry | Head | 0.134,-0.0449,0.0051 | 0.24729999899864197 |
| wolf | accessories | ChopperTrinket | c_allhlw4 | entry | Head | 0.368109,0.0182488,0.0119145 | 0.3938082456588745 |
| wolf | accessories | CoconHeadband | c_allhlw2 | entry | Head | 0.1257,-0.0813,-0.0014 | 0.27459999918937683 |
| wolf | weapons | bdWeapon | w_wlf19 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | boldasSword | w_wlf36 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | butlerDuster | w_wlf25 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | championSword | w_wlf58 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | commonSword | w_wlf2 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | eclipseSword | w_wlf79 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | fan | w_wlf5 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | flamingBrand | w_wlf81 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | frozenSword | w_wlf56 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | goldenSword | w_wlf49 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | halloweenSword | w_wlf37 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | hallowSaw_l |  | class fallback (no code) | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | hallowSaw_r |  | class fallback (no code) | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | heartSword | w_wlf14 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | heroSword | w_wlf40 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | heroSwordR | w_wlf41 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | heroSwordV | w_wlf42 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | knifeSword | w_wlf32 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | knifeSwordR | w_wlf34 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | legendSword | w_wlf60 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | lightStick | w_wlf15 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | mummySword | w_wlf46 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | noviceSword | w_wlf1 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | paladinSword | w_wlf31,w_wlf51 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | paladinSwordR | w_wlf33 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | paperSword | w_wlf3 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | poseidonSword | w_wlf66 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | pvpSword | w_wlf43 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | pvpSwordR | w_wlf44 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | royalSword | w_wlf50 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | royalSwordR | w_wlf52 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | scissorSword | w_wlf39 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | scorpionSword | w_wlf47 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | scorpionSwordR | w_wlf48 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | soldierSword | w_wlf21 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | soldierSwordR | w_wlf23 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | specialSword_l |  | class fallback (no code) | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | specialSword_r |  | class fallback (no code) | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | standardSword | w_wlf10 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | standardSwordR | w_wlf11 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | standardSwordV | w_wlf12 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | starBouquet | w_wlf45 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | thaiSword | w_wlf65 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | timeSword | w_wlf69 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | vagabondSword | w_wlf22 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
| wolf | weapons | vagabondSwordR | w_wlf24 | class fallback | mount_Hand_L | -0,0,0 | 1.0 |
