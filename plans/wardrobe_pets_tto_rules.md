# TTO's pet rules, read from 1.7.0 (2026-11-18)

Task 1 of `plans/wardrobe_pets_plan.md`; serves `plans/wardrobe_pets_design.md` ("Goals" placement / size, "Data").
Every TTO citation is `TTO1118:` (the 2026-11-18 client, patch 1.7.0, `D:\12tails\DecompiledSource_TTO_2026-11-18`),
an RVA in `GameAssembly.dll`. Positions are in Unity space (the wardrobe converts: x -> -x).

**In one line: TTO = BB for the spawn point, the rotation, the rest point of every follow type and the level scale of
every BB pet; TTO adds a per-pet / per-class multiplier (only TTO pets are in it), two size exceptions (the Cute Cats
p_all31-35 at a flat 4x, S.ValkorNoct p_svk at 0.1 + 0.01 x level), and picks the idle clip by
`PetControl.idlePrefix`, which changes what plays at rest for three pets only (BlueShark, PinkShark: `root_Cute`;
koalia: `battle`); no BB pet changes.**

## How it was read

- `pipeline/tto_disasm.py` (capstone over the DLL, as `wardrobe_icons.py`; names from `methods.tsv`, metadata usages
  through the decompile's `tools/usages.py`). The home PC's 11-18 folder has no `tools/`, so the script takes the 11-14
  folder's tools and derives 1.7.0's build constants with its `find_constants.py` into the temp folder (they match
  BUILD.md: `TABLE_VA 0x1835CA550`, header 0x45C, order (2, 1, 0)). Command lines in its docstring.
- `pipeline/tto_pet_probe.py`: every pet prefab's PetControl fields and Animation clips from decrypted bundles. Run on
  `12tails-video\tto_assets\2026-11-04` (all clips readable) and on today's pet prefab bundle alone
  (`a4c2b80dbbffe327c3ae16b606b93a2d`, decrypted into a scratch folder): all 101 prefabs have the same followType,
  followDistance, idlePrefix, runPrefix, attackClip, emotes and m_PlayAutomatically in both; today's clip names are
  partly unreadable without the dependency bundles (`?`), the readable ones match 11-04.
- `Config/PetScale`: the TextAsset in today's `resources.assets` (UnityPy; listed below in full).
- BB: `D:\12tails\DecompiledSource` (`PetControl.cs`, `SheepEquipment.cs:4140-5060`, `PetShopData.cs`, `PetData.cs`),
  the Bible's `12Tails-Mechanics-Reference.md` §4.9.

## 1. Spawn point and rotation: same as BB

`TTO1118:CharacterEquipment::EquipPet@0x1adac10` is one method for all twelve classes (no `<Class>Equipment` overrides
it; `EquipAll@0x1ada440` calls it through vtable +0x248, slot 17). After the pick of the prefab (section 5):
- gate `Game.mGameType >= 2` (static +0x60, `0x1adb539`), as BB's `if (Game.mGameType < 2) break`;
- `Instantiate(prefab, transform.position - transform.forward, transform.rotation)` (`0x1adcc1c-0x1adcce5`) = BB
  `SheepEquipment.cs:5010`;
- `petObject.transform.localScale = GetPetSize(nPet, lv)` (`0x1adcd3b`, `0x1adcd65`; section 2);
- `PetControl.Init(this.gameObject, lv)` through vtable +0x178 (slot 4, `0x1adcdcf`) = BB `:5026-5038`;
- `characterControl.mPet` (+0x158) = the pet, `characterControl.pet` (+0xe8) = the code; then
  `EquipmentVisibility::Apply` (tail call `0x1adceaf`: shows / hides the pet and trinket by two PlayerPrefs settings
  and some statuses; nothing for a still hero in the wardrobe).

`TTO1118:PetControl::Init@0x1a928a0`: `transform_0 = owner.transform`, `cc = GetComponent<CharacterControl>()`,
`int_0 = nLv`, then `ResolveClips()` (new, section 4), then a jump table on followType (table 0x1a930c0):
- 0 FloatBehind (`0x1a92a43`): offset = `offset_<cc.Type>` (cc.Type = CharacterControl +0x38: "Wolf" ->
  offset_wolf +0x5c, Bison +0x68, Panda +0x74, Whale +0x80, Cat +0x8c, Chameleon +0x98, Mole +0xa4, Rabbit +0xb0,
  Monkey +0xbc, Penguin +0xc8, Sheep +0xd4, Bat +0xe0; any other: LogError, offset 0), then as 1-3;
- 1 / 2 / 3 (`0x1a92c9b-0x1a92db5`): `position = owner.position - followDistance x owner.forward`, the 5-point trail
  filled with it;
- 4 / 5 (`0x1a92de5`): the offset only (same per-class table); the position is left at the spawn point;
- then `bool_0` (initialised) = true (`0x1a92dcf`).
This is BB's `Init` (`PetControl.cs:42-514`) except BB's `animation["run"] != null` test, which TTO moved into
`ResolveClips`.

`TTO1118:PetControl::LateUpdate@0x1a930e0` (jump table 0x1a94064), with the hero standing still:
- 0 FloatBehind (`0x1a931ba`): `Slerp(pos, owner.pos - fd x owner.forward + offset, 2 dt)`, rotation `Lerp` to the
  owner's: rests at **owner - fd x forward + offset** (the offset in world axes, not turned by the hero; the wardrobe's
  hero faces +z at the origin, so world = hero space), facing the hero's way. No clip call.
- 1 FloatFollow (`0x1a933ad`) / 3 RunFollow (`0x1a939b6`): the trail logic of BB (shift when
  `(owner - trail[4]).sqrMagnitude > (fd / 5)^2`; move only when `(trail[0] - pos).sqrMagnitude > 0.2`). Still: the
  first frame puts the owner's point in trail[4], trail[0] stays the rest point, so the pet never moves: rests at
  **owner - fd x forward**, the spawn rotation (the hero's), and calls `PlayIdle` (`0x1a939ac`).
- 2 RunBehind (`0x1a93753`): `Slerp` to owner - fd x forward, rotation `Lerp` to the owner's; `PlayIdle` while
  `sqrMagnitude < 1` (`0x1a9399f`).
- 4 ParentPosition (`0x1a93d61`): `position = owner.pos + transform.TransformDirection(offset)` (offset == 0 by
  Unity's 1e-10 test: `owner.pos`); rotation untouched = the spawn rotation (the hero's). No clip call.
- 5 ParentAll (`0x1a93eb1`): the same and `rotation = owner.rotation`. No clip call.
- Gates as BB: not initialised or hidden (+0x58, set by `OnParentHide@0x1a94140`) -> nothing; owner gone -> Destroy
  (`0x1a94027`).

So `rest_point` = BB's (design "Placement"): **same**. Rotation = the hero's for every type: **same**.

## 2. Size: `GetPetSize`, different for two groups

`TTO1118:CharacterEquipment::GetPetSize@0x1adcff0` returns the localScale (Vector3.one x s):
1. `IsStaticLargePet(nPet)` (`@0x1add410`, inlined here at `0x1add043`; no other caller): length 7, starts with
   `"p_all3"` (Ordinal) and the 7th char is `'1'..'5'`, i.e. **p_all31-35 (the Cute Cats): s = 4.0**
   (`StaticLargePetScale = 4.0`, dump.cs:97364; `0x1add0ee` / `0x1add0ff`). No level, no multiplier.
2. else `nPet.Length >= 5` and `nPet.Substring(0, 5) == "p_svk"` (S.ValkorNoct): **s = lv x 0.01 + 0.1**
   (`0x1add151-0x1add160`; Lv 1 0.11, Lv 9 0.19).
3. else **s = lv x 0.1 + 0.9** (`0x1add16a-0x1add179`) = BB `SheepEquipment.cs:5021`.
4. For 2 and 3: **s x PetScales.Multiplier(get_CharacterType(), nPet)** (`0x1add193` vtable +0x178 = slot 4
   `get_CharacterType`, `0x1add1a2`, product `0x1add1cd`). `get_CharacterType` is the capitalised class name in all 12
   (`BatEquipment@0x1abb610` "Bat" ... `WolfEquipment@0x1b262f0` "Wolf"), the keys of the table below.

`lv` (EquipPet): 1 for the codes matched whole (all `p_all...` codes, section 5; `0x1adb663`); for the six-character
family codes `Stringf.getLastDigit(nPet)` (`@0x166d5e0`: the last character as an int, 0 if it is not a digit), and 1
if negative (`0x1adc773`) = BB `:4986-5002`.

## 3. The multiplier: `PetScales`, TTO only

`TTO1118:PetScales::Multiplier(hero, code)@0x1af5440`, its table from `EnsureLoaded@0x1af5100`
(`Resources.Load<TextAsset>("Config/PetScale")`, `JsonUtility.FromJson<PetScaleData>`; empty table if missing) and
`BuildIndex@0x1af4d80` (byHero[hero] = the hero row, byCode[hero][code] = its entries, byPet[code] = the pets list;
default ordinal, case-sensitive dictionaries):
1. code empty -> 1.
2. byCode[hero] has `code` (or `Family(code)`) -> that value if > 0, else 1; **returned alone** (no pet or hero scale).
   `Family(code)@0x1af52b0` = `code.Substring(0, 5)` when the code has 6 characters and that is not `"p_all"`, else
   null (so `p_lcr9` -> `p_lcr`).
3. else `PetScale(code)` (`@0x1af57e0`, inlined): byPet[code] > 0, else byPet[Family(code)] > 0, else 1;
   times `HeroScale(hero, code)` (`@0x1af5330`, inlined): byHero[hero].scale > 0 **only when the code starts with
   "p_all"**, else 1.

Today's table (`resources.assets`, 2026-11-18 21:23 install): every hero `"scale": 1.0`; entries only Bison p_all85 /
p_all86 1.5 and Whale p_all85 / p_all86 2.0; pets p_all88, p_all87, p_all89, p_all81, p_all76, p_all75 0.5, p_allhlw
1.5. So: no BB code is touched (BB's p_all1-24 get HeroScale 1.0); p_all85 / 86 = 1.5 beside the Bison, 2.0 beside
the Whale, 1 elsewhere. Matches the design.

**`pet_scale(code, level, cls)` for Task 4** (cls capitalised for the table):
`4.0` if code is p_all31-35; else `(level x 0.01 + 0.1 if code[:5] == "p_svk" else level x 0.1 + 0.9) x
Multiplier(cls, code)`, with level = 1 for every `p_all...` code. The plan's expected values hold (`p_lcr` Lv 9 Sheep
1.8, p_all85 Whale 2.0, p_all88 Cat 0.5); add p_all31 -> 4.0 and p_svk Lv 9 -> 0.19.

## 4. The idle clip: different rule, three pets differ

TTO (`TTO1118:PetControl`):
- `.ctor@0x1a95010`: `idlePrefix = "root"`, `runPrefix = "run"`, `followDistance = 1`, `int_0 = 1` (field defaults;
  the prefab's serialized values replace them).
- `ResolveClips@0x1a94d30` (from `Init` and `Start@0x1a94f30`, once): `anim = GetComponent<Animation>()`; if there is
  one: `anim.cullingType = 1`, `idleAnim = FindClip(idlePrefix)`, `runAnim = FindClip(runPrefix)`, `bool_1` ("has
  clips", BB's "has run") = idleAnim != null || runAnim != null.
- `FindClip(prefix)@0x1a92600`: null if the prefix is empty; lower-cases both; over the Animation's states: a state
  named the prefix, or starting with prefix + `"_"`, is returned at once; otherwise the first one starting with the
  prefix; else null.
- `PlayIdle@0x1a94bf0`: unless an emote is acting (`actingClip`, `Acting@0x1a925a0`), if `bool_1` and `idleAnim`:
  `anim.CrossFade(idleAnim, 0.2)`. Called only from LateUpdate's at-rest branch (`0x1a939ac`, types 1 / 2 / 3; its one
  call site). `PlayRun@0x1a94c80` the same with runAnim while moving.
- `SetAnimPrefixes@0x1a94ea0` (sets both prefixes, clears and re-resolves) has no direct caller in the code.

BB (`PetControl.cs:490`, `:655`, `:706`, `:803`): CrossFade `"root"` at rest for types 1 / 2 / 3 only when the
Animation has a `"run"` clip; otherwise nothing is called.

In both, when nothing is called the Animation's default clip (`m_Animation`) plays only if `m_PlayAutomatically`;
types 0 / 4 / 5 never call a clip. **`idle_clip` for Task 4:** followType 1 / 2 / 3 and `FindClip(clips, idlePrefix)`
found -> that clip; else the default clip if `m_PlayAutomatically`, else none (the prefab pose). Inputs per prefab:
the clip names in state order, `m_Animation`, `m_PlayAutomatically`, PetControl's `followType` and `idlePrefix`.
The plan's `idle_clip(clip_names, default)` needs those three added; its expected values still hold with the prefabs'
own prefixes (`["root", "run"]` -> root; all64's prefix is `chibiDog_alert`; no clips -> None), and koalia
(`["run", "battle", "root"]`, prefix `battle`, default root) -> battle is the test that tells the rules apart.

What it gives (probe, all 101 prefabs): every `tto_idle` is an exact name match (state order never matters today).
idlePrefix is `root` on 91 prefabs; `chibiDog_root` (all63 / 65 / 68), `chibiDog_alert` (all64 / 66 / 67),
`halloweenGhost_root`, `root_Cute` (BlueShark, PinkShark), `battle` (koalia). Against BB's rule, what plays at rest
differs only for **BlueShark and PinkShark (`root_Cute`, BB `root`) and koalia (`battle`, BB `root`)**; the chibi dogs,
halloweenGhost and miniSkyBug get by CrossFade the clip BB plays as the default. `m_PlayAutomatically` is false on the
seven Rabbies, smallFlowerDryad and smallSelene, all type 1 / 3 with `root` found, so they still idle on `root`. No
Animation: kiteButterfly, kiteChula, kitePukpao, soccerBall (prefab pose). Emotes (`PlayEmoteOf` from
`BaseHero.<RPC_emotion>`) and `attackClip` (`PlayAttackOf` from `<RPC_petEffect>`) exist only on the six chibi dogs;
out of scope (idle only).

## 5. Code -> prefab (EquipPet) and the pets BB lacks

EquipPet compares `nPet` whole first (`0x1adb656-0x1adb9fd`), then, for a 6-character code, `nPet.Substring(0, 5)`
(`0x1adba0e-0x1adbfd8`). Read with `tto_disasm.py --switch`. Catalog keys are lower case (the code passes mixed case).

Whole codes (level 1):
- BB's ten, as BB: p_all1 bigbugBalloon, p_all2 bluebugBalloon, p_all3 momBalloon, p_all4 dadBalloon, p_all11
  smallSmashBall, p_all12 soccerBall, p_all21 kiteChula, p_all22 kitePukpao, p_all23 kiteButterfly, p_all24 kiteSnake
  (`GameAssets/characters/pet/<name>`).
- TTO's:

| code | address | prefab | size (any class unless noted) |
|---|---|---|---|
| p_all57 / 58 / 59 / 70 | `gameassets/characters/Pets/all57` / `all58` / `all59` / `all70` | all57 ... | 1.0 |
| p_all83 | `gameassets/characters/Pets/moneypiggy` | MoneyPiggy | 1.0 |
| p_all85 | `gameassets/characters/pets/tianlonga` | TianlongA | 1.0; Bison 1.5, Whale 2.0 |
| p_all86 | `gameassets/characters/pets/tianlongb` | tianlongB | 1.0; Bison 1.5, Whale 2.0 |
| p_all87 | `gameassets/characters/pets/violeta` | violeta | 0.5 |
| p_all88 | `gameassets/characters/pets/apo` | apo | 0.5 |
| p_all89 | `gameassets/characters/pets/koalia` | koalia | 0.5 |
| p_all31 / 32 / 33 / 34 / 35 | `gameassets/characters/pets/cutecat/cutecat_w` / `_b` / `_o` / `_v` / `_r` | CuteCat_W ... | 4.0 |
| p_all81 | `gameassets/characters/pets/dino/greenshark` | GreenShark | 0.5 |
| p_all76 | `gameassets/characters/pets/dino/blueshark` | BlueShark | 0.5 |
| p_all75 | `gameassets/characters/pets/dino/pinkshark` | PinkShark | 0.5 |
| p_allhlw | `GameAssets/Characters/Pets/` + map(p_allhlw) = `.../smallSelene/smallSelene` | smallSelene | 1.5 |
| p_all90 | `gameassets/characters/pets/halloweenghost` | halloweenGhost | 1.0 |
| p_all63 ... p_all68 | `gameassets/characters/pets/` + code[2:] = `.../all63` ... `.../all68` | all63 ... all68 | 1.0 |

Family codes (6 characters, level = last digit): BB's 56 as BB (`GameAssets/characters/pet/<name>`; e.g. p_lcr
littleCarron, p_lcp littleCarron_p, p_lcs littleCarron_s ... p_mnb miniNemesisBug, the same pairs as
`SheepEquipment.cs:4309-4980`). Any other family: `"GameAssets/Characters/Pets/" + MapPetCodeName(family)`
(`0x1adbff4`); `EquipmentUtility::MapPetCodeName@0x165d810` looks the code up in a table filled by its `.cctor@0x165d8b0`
(the code itself when absent). TTO's families:

| family | address (`GameAssets/Characters/Pets/...`) | prefab | size |
|---|---|---|---|
| p_mrd / p_mrg / p_mrw | `miniRabby/miniRabbyB` / `G` / `W` | miniRabbyB ... | 0.9 + 0.1 lv |
| p_srb / p_srg / p_srs / p_srw | `smallRabby/smallRabbyB` / `G` / `S` / `W` | smallRabbyB ... | 0.9 + 0.1 lv |
| p_drz | `smallDragonZ/smallDragonZ` | smallDragonZ | 0.9 + 0.1 lv |
| p_sfd | `smallflowerdryad/smallflowerdryad` | smallFlowerDryad | 0.9 + 0.1 lv |
| p_mtf | `MotherFlowerBug/MotherFlowerBug` | MotherFlowerBug | 0.9 + 0.1 lv |
| p_svk | `ValkorNoct_Pet` | ValkorNoct_Pet | 0.1 + 0.01 lv |

(the table also maps p_allhlw -> `smallSelene/smallSelene`, used by the whole-code branch above). Note p_mrd, not
p_mrb, is the blue Mini Rabby: p_mrb stays MiniReefBug.

These 37 prefabs are exactly the 37 `characters/pets/` GameObjects of today's catalog (plus one FBX); the 64 BB ones
are the 64 `characters/pet/` GameObjects (effects aside). **p_lck (littleCarronCake) and p_lpd (littlePepponDisco)**
are in both EquipPets but their prefabs exist nowhere (not in TTO's catalog or built-in Resources, not in BB's rip):
no tile. Icons `gamegui/icons/items/pet/<code>` exist in today's catalog for every TTO code above (all31-35, all57-90,
allhlw, drz, mrd / mrg / mrw, mtf, sfd, srb / srg / srs / srw, svk); none for lck / lpd.

Follow values of the TTO pets (probe): all RunFollow (3), distance 1, except the seven Rabbies and MotherFlowerBug
(distance 1.5), smallFlowerDryad and smallSelene (FloatFollow 1, distance 1), smallDragonZ (ParentPosition 4,
distance 0) and TianlongA / B (ParentPosition 4).

## 6. Game names of the TTO pets: not in the client

`TTO1118:PetData::getData@0x2290100` reads `GameData`'s item table (`GameItemTable::Get@0x228d740` ->
`GameItemDef::ToItemClass`), which the server sends (`GameItemTable::Request@0x228df50` through
`GameConnection::OpCustom`, gzip in memory, no file). TTO's locale (`locale/en.json`, `th.json`) has no pet names
(no `p_` key; `CampPet` is the guild camp's pet), BB's `PetData.cs` names no TTO code, and the string literals hold
only **"S.ValkorNoct"** (the chat line "S.ValkorNoct raises a magic wall (", literal 15133; the Bible's name for
p_svk). The other 36 have no game name in the client: the tile can only use the prefab name (humanize) or a nickname.

## 7. Levels: the pet shop

- BB (`PetShopData.getUpgradeItem`, `PetShopData.cs:123-670`, called with `name.Substring(0, 5)`,
  `PetShopGui.cs:1884-1904`, up to 9): **47 families upgrade to Lv 9**: p_lcr, p_lcp, p_lmp, p_lpp, p_lct, p_lcc,
  p_lpk, p_lml, p_lbd, p_lcs, p_lms, p_lps, p_lmc, p_lmn, p_lmo, p_ldc, p_ldm, p_ldp, p_ldt, p_ldn, p_ldk, p_skr,
  p_skg, p_sky, p_skb, p_skk, p_sfb, p_sim, p_sam, p_sob, p_sgb, p_slb, p_stb, p_spb, p_swb, p_ssq, p_snb, p_sab,
  p_spg, p_spf, p_msb, p_mcb, p_mab, p_mrb, p_mmb, p_mgb, p_mnb. No recipe (Lv 1, shops sell Lv 1 only, the Bible):
  p_srp, p_sss, p_sbb, p_sdm, p_sdv, p_skz, p_skm (and p_lck, p_lpd, which have no prefab). The `p_all...` codes have
  no level.
- TTO: `TTO1118:PetShopData::getUpgradeItem@0x2291060` looks the code up in `_upgradeMat`, which `LoadData@0x2290280`
  fills from the server's Hashtable; not in the client (see section 8).

## 8. Not settled

- **Which levels TTO's own family pets reach** (p_mrd / mrg / mrw, p_srb / srg / srs / srw, p_drz, p_sfd, p_mtf,
  p_svk): the upgrade list is server data. Evidence for 1-9 in code only: `MotherFlowerBugPet.HealPerLevel` has 9
  entries (20, 25, 30, 35, 40, 50, 55, 60, 65; `MotherFlowerBugPet::.cctor@0x1a92500`), and the Bible's S.ValkorNoct
  (`p_svk`, "pet level N 1-9", its tooltip read at Lv 9). Nothing for the Rabbies, DragonZ, FlowerDryad. The size rule
  for any level is above; the level to show is the user's or Task 4's call.
- **TTO pets' game names**: server data (section 6).
- **Today's clip names**: read only where they sit in the prefab bundle; the full list (and the 1.7.0 check of the
  idle table above) needs the dependency bundles (Task 2's decrypt). PetControl's own fields are already the same as
  11-04's for all 101.
- A default clip whose wrap mode does not loop (types 0 / 4 / 5, or nothing found): Unity plays it once; whether any
  pet has one is in the clip data (Task 4 reads `m_WrapMode`), not in this code.
