# Rabbit effects + sounds research: the three TTO Lv 100 skills (Bounty Hunt, Coin Ricochet, Medic Turret)

Scope: the TTO-only skill clips `bountyHunt` (1.8 s), `coinRicochet` (1.9 s) and `medicTurret` (1.3 s), all `tto: true`,
group `skill` in `wardrobe/data/rabbit/clips.json`. No BB code plays them. **All three are in the released list**
(`wardrobe/tto_released.json:271-274`, rabbit clips: bountyHunt, clap, coinRicochet, medicTurret, wai), so all three get
cues. (clap / wai are emotes: the attacks_emotes report's.) Research only: this file is the only file written in the
repo, plus the probes in `checks/fx_rabbit_research/tto/` (git-ignored). Office PC, 13/11/2026.

Sources:
- TTO's pseudo-C `C:\Users\Jump\Desktop\12tails\DecompiledSource_TTO_2026-11-02\pseudo\Rabbit.c` (`:<line>` alone = this
  file) and `pseudo_c6_extra\rabbit\RabbitMedicTurret.c` (cited `RMT.c:<line>`), cited as `TTO1102:Method@RVA`; `dump.cs`
  for fields and constants (Rabbit `:119989`, RabbitMedicTurret `:120550`, RabbitSpin `:120616`, RabbitTracer `:120630`).
  Unlike BB's C#, these functions have no opaque `if (a - b == c)` predicates; the BB status code read for the capsule's
  statuses (`DecompiledSource/CharacterControl.cs:37491-37520`, `:16819-16850`) has them, all evaluated true
  (`171261 - 170975 == 286`, `4094 - 186379 == -182285`, `111808 - 200236 == -88428`).
- capstone over `client\GameAssembly.dll` for the floats Ghidra drops: `dis.py` (annotates rip-relative float loads and
  call targets from `methods.tsv`) -> `coin_movenext.asm` (RPC_coinRicochet's three `Until`s: 0.3, CoinShotAt[k], 1.9),
  `ricochets.asm` (CoinRicochets' Row6Sound volume 0.7, reaches 18 / 9, the 0.07 wait), `spin.asm` (RabbitSpin.Update).
  `FUN_180308bd0` is sinf (plans/fx_sheep/tto.md Verification; Penguin.c:1083).
- The Bible: `12t_reference/rabbit-skill-reference.md` "TTO Lv 100 skills" (:1014-1065; Medic Turret :1018-1031, Coin
  Ricochet :1034-1049, Bounty Hunt :1051-1065) and "Server Balance Variations (TTO)" (:824-838: TTO1109's InSight and
  stacking changes, no effect on the looks).
- TTO's bundles (this PC: `tto_assets/2026-11-09`, found by `wardrobe_fx_tto.py` itself): `wardrobe_fx_tto.py rabbit
  --probe <the 25 TTO-only prefabs>` -> `probe.json` (`compact.py` -> `compact.txt`); `catalog.py` -> `catalog.txt` (every
  catalog address under `heroes/rabbit/` against BB's rip); `cc.py` -> `cc.txt` (TTO's Rabbit prefab: CharacterController
  centre 0.7, height 1.2, radius 0.3, the same as BB's `Rabbit.prefab:817-823`); BB's three reused prefabs through
  `wardrobe_fx.py rabbit --probe lifeShot,boostShot,heatShot` -> `probe_bb.json`.
- `bones.py` -> `bones.txt` (a bone's spot in the hero's space on the page from `rig.json` + `clips.json` with the page's
  own hermite, `index.html` hermite / buildClip; cue x = -rig x, d = rig z; sanity: the idle's toes 0.07 ahead, the right
  hand 0.15 right); `cues.py` -> `cues_paste.json` (section 7's cues, every name checked against `probe.json` / BB's rip),
  `block.py` -> `cues_block.txt` (section 7 as pasted, parsed back).

Times are seconds from the start of the clip the cue is keyed by. Every wait in the three coroutines is
`Rabbit::Until(start + t)` (`@0x1E12EA0`, `:41886` area; the absolute-time wait every TTO class uses, start = `Time.time`
at the first state), so a time is from the cast, not a step to add; the shot hops use `Waits.Get(0.07)` and the capsule
`Waits.Get(0.25)`. All three skills have one rank (Bible :1038, :1055, the Medic tooltip): max rank changes nothing.

## Read this first

1. **Three single clips, no sequences, no cast bar.** Each skill is `Row6Begin(command)` = `PlayAnimation(<command>, 0.1)`,
   wrapMode Once (`Rabbit::Row6Begin@0x1E10F50`, `:38981-39056`), then `Row6End` at its clip's length (1.8 / 1.9 / 1.3 s).
   No SEQ line is needed; the cue keys are the plain clip names. (The page fades a single clip in over 0.2 s, the game
   0.1 s: as every TTO tile so far.) Medic Turret's turret outlives its 1.3 s clip by 9 s: its cues run in the idle
   tail (question 4: a hold line for the loop toggle).
2. **Where things go.** The lone target stands 10 m ahead; `Row6Chest` (`@0x1E11140`, `:39226`) = the collider's bounds
   centre = the standard body's **0.6 m up** (Bat decisions 3-4); its feet (0, 0, 10). **The Rabbit's own chest is 0.7 m
   up** (her CharacterController centre, `cc.txt`). The two hands are `mountHand_L` / `mountHand_R` (`Row6Hand(right)
   @0x1E11AB0`, `:39306`: `Row6Hand(false)` = the **left** hand, used for the poster and the coins); the gun's muzzle is
   `Row6Muzzle@0x1E11BF0` (`:39352-39490`): a child named `fire` / `Fire` / `muzzle` under `mountHand_R`, else
   `mountHand_R + 0.35 x forward` (`:39468`). **No Rabbit gun has such a child** (all 45 in `data/rabbit/props_weapons.json`,
   and BB's rip prefabs have only their mesh node), so the muzzle is always the hand + 0.35 ahead; its spot at each shot is
   computed from the clip (`bones.txt`) and written into the cue.
3. **The Medic Turret shoots the Rabbit herself.** `MedicTurretPick@0x1E089A0` takes the ally with the lowest HP share
   within 10 m, the Rabbit included, ties to the nearest; Race 4 (Robots) and 6 (Structure) are skipped (`:40167`), and
   the turret's own CharacterControl is `Race: 4` (`probe.json`), so it never picks itself. With the Rabbit alone (the
   page), every beat's capsule flies back to her (Sheep decision 1: ally skills land on the hero).
4. **Released, all cued: 82 cues in 3 entries** (section 7: Bounty Hunt 18, Coin Ricochet 23, Medic Turret 41).
5. **25 TTO-only prefabs, all probed; no arcana style** (`catalog.txt`: 75 TTO-only addresses under `heroes/rabbit/`, of
   them 25 effects: 7 `bountyHunt_*`, 8 `coinRicochet_*`, 8 `medicTurret*`, and the status looks `bounty`, `gilded`).
   22 are cued; `bounty`, `gilded` (status looks on the foe) and `bountyHunt_claim` (the kill reward) are left out
   (section 3). Three BB prefabs are reused through TTO's catalog copies: `lifeShot`, `boostShot`, `heatShot` (the
   capsule's hit; cued as BB's rip copies, Bison decision 43; inventory: ready). Every sound and voice is a BB recording
   in BB's rip (`catalog.txt`: `sounds/coin`, `truceTrading`, `shotgun`, `deadShot`, `diamondShot`, `backpack_hit`;
   voices `contract1/2`, `lifeShot1/2`); no TTO-only hero sound.
6. **No camera effects, no proc rolls, no passives.** `Row6Shake@0x1E12160` is never called by these skills (its only
   reference is its own definition); the random picks are the voices (`Random.Range(0, 2)`, `Row6Voice@0x1E12B10`) and the
   capsule's kind (`Random.Range(1, 4)`, `RMT.c:471`), both written as `"a|b"` picks.
7. **Missing parts (section 6): P1-P6**, all small: `RabbitSpin` (the coin's spin), three code movers (`Rabbit.CoinRise`,
   `Rabbit.PosterFly`, `Rabbit.TurretCapsule`), the `RabbitMedicTurret` script (grow, head turn, the end's shrink), and the
   two `Eric/URP Particles` shaders (already decided for the Monkey, decision 61) plus Shuriken's NoiseModule (Monkey
   decision 62). `RabbitTracer`, `TrailRendererModern`, `LineRenderer` (tto_sheep.js), `GroundHugEmitter`, Shuriken with
   World collision and the TrailModule, `Particles/Standard Unlit`, `FlexibleCelShader/Cel No Outline` and
   `Particles/AdditiveOffset` are built already.

---

## 1. Shared machinery (`TTO1102:Rabbit`)

- **`Row6Begin(command, mPos, tDir)@0x1E10F50`** (`:38981`): actionState `attack`, actionTime now, myCommand = command;
  the hero at mPos, `LookAt(mPos + vFlat(tDir))`; `PlayAnimation(command, 0.1)`, wrapMode Once, moveSpeed 0.
  **`Row6End(command)@0x1E114C0`** (`:39085`): `standby` while still doing that command.
- **`Row6Spawn(name, pos, rot, owned)@0x1E12360`** (`:38716`): `Row6Prefab` loads
  `GameAssets/characters/heroes/rabbit/effects/<name>` (`:38655`, cached); owned -> `CharacterControl.createEffect`, else
  `Object.Instantiate`. Owned here: `coinRicochet_flick` and `medicTurret_cast` only (neither has followState).
- **`Row6Sound(name, volume)@0x1E12290`** (`:38898`): `sounds/<name>`, PlayOneShot on the hero, volume x 0.7 for other
  players' copies (`:38922`). **`Row6Voice(a, b)@0x1E12B10`** (`:38831`): `voices/a` or `voices/b` (`Random.Range(0, 2)`),
  only with the voice option on, the owner's at 1 (`:38884`).
- **`Row6Tracer(name, a, b)@0x1E12940`** (`:41234`): Instantiate at a, identity, then its `RabbitTracer.Set(a, b)` (the
  page's `RabbitTracer` part reads the cue's spot as a and `to` as b: tto_sheep.js).
- **Statics** (`Rabbit::.cctor@0x1E12F10`, `:41886`): `CoinShotAt` [0.75, 0.95, 1.15, 1.35], `CoinHang` (hero-local,
  x right, z ahead) (-0.9, 1.55, 1.6), (-0.3, 1.85, 1.9), (0.3, 1.75, 1.8), (0.9, 1.5, 1.55), `HiredGunAt` [1.15, 1.35,
  1.55], `HiredGunAngle` [-65, 65, 180]. Constants (`dump.cs` Rabbit): CoinFlickAt 0.3, CoinRiseTime 0.35, CoinLength
  1.9, CoinHopTime 0.07, PosterThrowAt 0.4, PosterFlight 0.25, FlareAt 0.85, HiredGunDistance 14, HiredGunHeight 7,
  BountyLength 1.8, TurretPlantAt 0.55, TurretLength 1.3, TurretAhead 1.8.

## 2. Per skill

### 2.1 Bounty Hunt (`bountyHunt`, 1.8 s; cell 454) - released

Coroutine `TTO1102:Rabbit.<RPC_bountyHunt>d__352::MoveNext@0x1E30840` (`:3251-3674`):
- **0.00** (state 0): `Row6Begin` (`:3321`); cooldown `agiAdjust(120)` (`:3329`); **voice `contract1 | contract2`**
  (`:3331`); body = the marked target; spot = mPos + toMark (its feet). `Until(start + 0.4)` (`:3381`).
- **0.40** (state 1, still doing it): **sound `truceTrading` 0.8** (`:3394`); `PosterFly(step, mountHand_L, body, spot)`
  (`:3403`) = `<PosterFly>d__353::MoveNext@0x1E28850` (`:556-786`):
  - **`bountyHunt_poster`** at the left hand (**0.039 m left, 0.884 up, 0.349 ahead** at 0.4 s, `bones.txt`) with the
    hero's rotation, not owned (`:614`);
  - every frame while `now < t0 + 0.25` (`:628`): position = lerp(from, chest + 0.6 up, clamp01(s)) + up x 0.8 s (1 - s),
    s = 4 (now - t0) (`:654`, `:667-693`): a 0.2 m arc to **(0, 1.2, 10)**; `Rotate(forward, 900 x dt, Self)` (`:715`);
  - the first frame past 0.25: Destroy (`:733`); the target alive: **`bountyHunt_pin`** at its chest, identity (`:764`;
    its own AudioSource truceTrading_fail 0.6), `RPC_AddStatus(bounty = 719, 1, 12 s)` (`:769`) and `BountyWatch`
    (`:772`). So the pin lands at **0.65** (Bible :1058).
  `Until(start + 0.85)` (`:3410`).
- **0.85** (state 2): **`bountyHunt_flare`** at `Row6Muzzle` (**0.205 right, 1.082 up, 0.475 ahead**: mountHand_R at
  0.85 s + 0.35 ahead), identity, not owned (`:3431`; the prefab's Muzzle node is turned -90 degrees about x, so its shot
  and flash go straight up; its Burst / Flash sit 11.5 m up; own sound nAttack 1.0); **sound `shotgun` 0.8** (`:3433`);
  `BountyOrders` (`:3436`: Contract's units, none on the page). Then `Until(start + HiredGunAt[i])` (`:3464`).
- **1.15 / 1.35 / 1.55** (state 3, shot i, only the step checked: the shots come even if the Rabbit is interrupted):
  chest = `Row6Chest(target)` (`:3509`), spot = its feet; dir = vFlat(hero - spot) = (0, 0, -1) (`:3533`); gun = spot +
  AngleAxis(HiredGunAngle[i], up) x dir x 14 + up x 7 (`:3565-3602`):

  | i | angle | gun (x right, y, d) | muzzle rot = LookRotation(chest - gun) | hit rot = LookRotation(gun - chest) |
  |---|---|---|---|---|
  | 0 | -65 | (12.688, 7, 4.083) | [24.567, -65, 0] | [-24.567, 115, 0] |
  | 1 | +65 | (-12.688, 7, 4.083) | [24.567, 65, 0] | [-24.567, -115, 0] |
  | 2 | 180 | (0, 7, 24) | [24.567, 180, 0] | [-24.567, 0, 0] |

  (AngleAxis(θ, up) x (0, 0, -1) = (-sin θ, 0, -cos θ); the pitch atan(6.4 / 14) = 24.567 degrees.)
  **`bountyHunt_muzzle`** at the gun (`:3618`; own nAttack 1.0), **`bountyHunt_tracer`** = Row6Tracer(gun, chest)
  (`:3625`; RabbitTracer life 0.32, travel 0.08, width 0.16), **`bountyHunt_hit`** at the chest (`:3642`), **sound
  `deadShot` 0.8** (`:3643`), `HiredGunHit` (`:3654`: the hit, no raycast, no effect, `:41501-41553`).
- **1.80** (state 4): `Row6End` (`:3665`).
- The kill watch (`<BountyWatch>d__356@0x1E26E80`, `:1-100`): a kill within 12 s -> `BountyClaim@0x1E05700` (`:41580`):
  cooldown -45, SP +20, heals, and `BountyClaimFx@0x1E05380` (`:41710`): `bountyHunt_claim` + sound
  `truceTrading_success` 0.9. Needs a kill: left out.

### 2.2 Coin Ricochet (`coinRicochet`, 1.9 s; cell 453) - released

Coroutine `TTO1102:Rabbit.<RPC_coinRicochet>d__343::MoveNext@0x1E36300` (`:6311-6692`), its waits from the
instructions (`coin_movenext.asm`):
- **0.00** (state 0): `Row6Begin` (`:6371`); cooldown `agiAdjust(60)` (`:6379`); **no voice**; hang[i] =
  `TransformPoint(CoinHang[i])` (`:6469`): the four spots above, fixed at the cast. `Until(start + 0.3)` (0x1E36D77).
- **0.30** (state 1): **sound `coin` 1** (`:6493`); **`coinRicochet_flick`** owned at the left hand (**0.098 left, 1.068
  up, 0.192 ahead**) with the hero's rotation (`:6494-6508`; followPosition, life 0.5 + 0.3); four **`coinRicochet_coin`**
  there, identity, not owned (`:6526`), each `CoinRise(step, coin, hand, hang[i], 0.04 i)` (`:6509`, `:6543`) =
  `<CoinRise>d__346::MoveNext@0x1E27890` (`:440-539`), every frame while the coin lives: u = clamp01((now - t0 -
  delay) / 0.35), e = 1 - (1 - u)^2, position = lerp(hand, hang, e) + up x 0.08 sin(40 delay + 6 Time.time)
  (`:469-524`): an eased 0.35 s rise, coin i leaving 0.04 i s later, then a 0.08 m bob. The coin's `Coin` node spins
  900 deg/s about its y (`RabbitSpin`, `spin.asm`: `Rotate(axis, degreesPerSecond x dt, Self)`), its Trail draws behind.
  `Until(start + CoinShotAt[0])` (0x1E36963).
- **coin k at 0.75 / 0.95 / 1.15 / 1.35** (state 2): the coin's spot (its position, else hang[k]); the coin destroyed
  (`:6628`); **`coinRicochet_shot`** = Row6Tracer(Row6Muzzle, coin) (`:6632-6636`; its Muzzle node plays nAttack 1.0);
  **`coinRicochet_ping`** at the coin, identity (`:6645`; own gilShot 0.75); `CoinChain` -> `<CoinRicochets>d__348
  ::MoveNext@0x1E27210` (`:6648`; `:173-423`) with the selected target:
  - cashOut = k is the last coin (`:235`: k == CoinShotAt.Length - 1);
  - hop 0: `CoinNext(coin, target, 18)` (`:303-311`) = the target; **`coinRicochet_ricochet`** (cash out:
    **`coinRicochet_cashTracer`**) = Row6Tracer(coin, chest) (`:393-404`); `Waits.Get(0.07)` (`:408`);
  - then **`coinRicochet_hit`** (cash out: **`coinRicochet_cashout`**) at the chest, identity (`:269`; own gilShot_hit 1.0),
    and `Row6Sound(gilShot_hit, or diamondShot for the cash out, 0.7)` only when hop > 0 or cash out (`:276`; 0.7 =
    0x182F3FF88, `ricochets.asm` 0x1E27439): so **coins 1-3 have no hero sound on their hit, coin 4 has `diamondShot`
    0.7**; `CoinHit` (the damage and Gilded, no effect, `:41095`);
  - hops 1-2: `CoinNext(last chest, null, 9)` finds no other foe on the page; the chain ends (the 8 m "miss" tracer is hop
    0's only, `:345-357`).
  The coin spots at the shots, with the bob taken at the clip's time (question 3): (-0.9, 1.472, 1.6), (-0.3, 1.918, 1.9),
  (0.3, 1.700, 1.8), (0.9, 1.526, 1.55); the muzzle (mountHand_R + 0.35 ahead): (-0.030, 0.900, 0.454), (0.021, 0.904,
  0.430), (0.056, 0.904, 0.407), (0.089, 0.900, 0.376). Hits at **0.82 / 1.02 / 1.22 / 1.42** (Bible :1048).
- **1.90** (state 3; `Until` 0x1E369CF): `Row6End` (`:6561`).

### 2.3 Medic Turret (`medicTurret`, 1.3 s; cell 452) - released

Coroutine `TTO1102:Rabbit.<RPC_medicTurret>d__334::MoveNext@0x1E420E0` (`:13058-13300`):
- **0.00**: `Row6Begin` (`:13131`); cooldown `agiAdjust(90)` (`:13139`); **voice `lifeShot1 | lifeShot2`** (`:13141`);
  **`medicTurret_cast`** owned at the hero, her rotation (`:13153`; followPosition, life 0.9 + 0.3, own cast1 0.8).
  `Until(start + 0.55)` (`:13158`).
- **0.55**: **sound `backpack_hit` 0.9** (`:13172`); the owner places it: dir = vFlat(aim), a wall raycast 2.3 m from
  0.6 m up (none here), so **1.8 m ahead** (`:13212-13234`), dropped to the ground (`Row6Ground`, `:13254`) ->
  `RPC_medicTurret_create@0x1E0DE50` (`:13268`; `:39868-40089`): an old turret destroyed (`:39916`); **`medicTurret`** at
  the spot, LookRotation(vFlat(dir)) = her facing (`:39948-39959`), on her layer, `isSummon`, its stats from her Lv;
  `RabbitMedicTurret.Init` (`:40056`); **`medicTurret_deploy`** at the spot, identity (`:40085`; own medicalShot_ring 0.9).
- **1.30**: `Row6End` (`:13280-13292`).
- **The turret** (`RabbitMedicTurret`, `RMT.c`; constants `dump.cs:120553-120562`: Beats 10, ShotGap 1.5, ShotReach 10,
  CapsuleFlight 0.25, FieldRadius 6, DeployTime 0.45, FirstBeat 0.75, Life 15, TurnSpeed 540):
  - `Awake@0x1E69A70`: Head, Muzzle, Model found by name; mAimDir = its forward. `Init@0x1E6A350`: Model localScale 0.01,
    mBorn = now, the first beat at **+0.75** (`RMT.c:142-161`).
  - `Update@0x1E6A6C0`: Model localScale = max(0.01, k (1 + 0.18 sin(1.5 pi k)(1 - k))), k = clamp01(age / 0.45)
    (`:225-252`: grows in 0.45 s with a small overshoot); the Head turns toward vFlat(mAimDir) at 540 deg/s (`:314-351`);
    a beat whenever now >= mNextBeat, mNextBeat += 1.5 (`:403`), 10 beats; after the 10th it stays to age 15, then
    `Die(true)` (`:374-401`; a copy that is not the owner's dies at 16.5).
  - `Beat@0x1E69CB0` (`:422-570`): `MedicTurretPulse` (`:461`: `RPC_AddHeal` to allies within 6 m, no look);
    `MedicTurretPick(turret)` (`:469`) = the Rabbit (Read this first 3); kind = `Random.Range(1, 4)` (`:471`), level
    `RollLv` 55 / 30 / 12 / 3 % (`:472`, no look); `Fire(ally, kind, lv)` (`:491`).
  - `<Fire>d__29::MoveNext@0x1E74270` (`RMT.c:1181-1392`): **`medicTurret_beat`** at the turret, identity
    (`BeatFx` `:1251` -> `Rabbit::MedicTurretBeatFx@0x1E08760`, `:40376`; own healingField 0.6; a 6 m GroundHug pulse);
    mAimDir = ally - turret, the Head snapped to LookRotation(vFlat(it)) (`:1321-1327`): it faces her; the muzzle = the
    Muzzle node (`:1351`; Head (0, 0.78, 0) + Muzzle (0, 0.06, 0.3345) turned to her: **0.84 up, 1.466 ahead**);
    `MedicTurretShotFx(muzzle, ally, kind)` (`:1372`; `Rabbit.c:40218-40344`): **`medicTurret_shot`** at the muzzle,
    identity, `RabbitTracer.Set(muzzle, her chest)` (`:40264-40318`; life 0.25, travel 0.05, width 0.1; its Muzzle node
    plays medicalShot_fire 1.0) and `TurretCapsule(muzzle, ally, kind)` = `<TurretCapsule>d__338::MoveNext@0x1E7AA60`
    (`:24911-25135`): **`medicTurret_capsule`** at the muzzle, identity (`:24972`), lerp(muzzle, her chest,
    clamp01(4 age)) (`:24985-25026`), `Rotate(right, 1080 x dt, Self)` (`:25049`), destroyed at 0.25 (`:25067`); then
    **`medicTurret_hit`** at her chest, identity (`:25097`; own medicalShot_hit 0.8) and **`lifeShot` (kind 1) /
    `boostShot` (2) / `heatShot` (3)** at her feet, identity, `Destroy(2)` (`:25119-25130`). `Waits.Get(0.25)`
    (`RMT.c:1379`): `MedicTurretShotHit` (`:1237`: the heal and the autoLife / boost / heat status, which draw nothing in
    `addStatus`: `CharacterControl.cs:37491-37520`, no `createEffect`).
  - `Die` -> `<RPC_dead>d__31::MoveNext@0x1E768C0` (`RMT.c:1393-1537`): **`medicTurret_break`** at the turret (`:1469`;
    `MedicTurretBreakFx@0x1E08880`, `:40593`; own backpack_hit 0.8), the Model shrunk linearly to 0.01 over **0.4 s**
    (`:1501-1526`), Destroy (`:1507`).
- **On the page, cut at 10 s after the spawn** (the standing rule; question 1): beats at spawn + 0.75 ... 9.75 =
  **1.3, 2.8, 4.3, 5.8, 7.3, 8.8, 10.3** (7 of 10), each capsule's hit 0.25 s later; the end at **10.55** (break, shrink,
  gone 10.95). The game: 10 beats to 14.8 + 0.55 = 15.35, the end at 15.55.

## 3. What is left out (only "on an enemy's body" / "needs a kill" / chat)

- Bounty Hunt: the **Bounty look** on the foe (`bounty` = `bountyFx` through `CharacterControl::AddRabbitRow6Fx
  @0x24AE1D0`: a wanted poster and crosshair over it for 12 s; Sheep decision 4, Chameleon decision 53's Prey); the kill
  claim (`bountyHunt_claim` + `truceTrading_success`: needs a kill; Chameleon's apexHunt_trophy); the mercenary orders
  (no Contract units); the push of the hits.
- Coin Ricochet: the **Gilded look** on the foe (`gilded` = `gildedFx`, the same dispatcher; Sheep decision 4); the
  bounce hops 2-3 and their 8 m miss tracer (one target: neither happens); the gold chat line (`CoinSettle@0x1E06F80`).
- Medic Turret: the heals and their numbers (Mole decision 52), the statuses (no looks), the capsule level; beats 8-10
  and the game's 15 s end (the 10 s cut).
Everything else is cued.

## 4. Sounds and voices

| t (s) | kind | name | where | in BB's rip |
|---|---|---|---|---|
| bountyHunt 0 | voice | contract1 \| contract2 | Row6Voice (`:3331`) | voices/ |
| bountyHunt 0.4 | sound | truceTrading 0.8 | `:3394` | sounds/ |
| bountyHunt 0.65 | own | truceTrading_fail 0.6 (bountyHunt_pin) | prefab | sounds/ |
| bountyHunt 0.85 | sound | shotgun 0.8 | `:3433` | sounds/ |
| bountyHunt 0.85, 1.15, 1.35, 1.55 | own | nAttack 1.0 (flare Muzzle, bountyHunt_muzzle Fire) | prefabs | sounds/ |
| bountyHunt 1.15 / 1.35 / 1.55 | sound | deadShot 0.8 | `:3643` | sounds/ |
| coinRicochet 0.3 | sound | coin 1 | `:6493` | sounds/ |
| coinRicochet 0.75 ... 1.35 | own | nAttack 1.0 (coinRicochet_shot Muzzle), gilShot 0.75 (ping) | prefabs | sounds/ |
| coinRicochet 0.82 ... 1.42 | own | gilShot_hit 1.0 (hit / cashout) | prefabs | sounds/ |
| coinRicochet 1.42 | sound | diamondShot 0.7 | `:276` | sounds/ |
| medicTurret 0 | voice | lifeShot1 \| lifeShot2 | Row6Voice (`:13141`) | voices/ |
| medicTurret 0 | own | cast1 0.8 (medicTurret_cast) | prefab | sounds/ |
| medicTurret 0.55 | sound | backpack_hit 0.9 | `:13172` | sounds/ |
| medicTurret 0.55 | own | medicalShot_ring 0.9 (deploy) | prefab | sounds/ |
| each beat | own | healingField 0.6 (beat), medicalShot_fire 1.0 (shot) | prefabs | sounds/ |
| each hit | own | medicalShot_hit 0.8 (medicTurret_hit) + 1.0 (lifeShot / boostShot / heatShot) | prefabs | sounds/ |
| medicTurret 10.55 | own | backpack_hit 0.8 (break) | prefab | sounds/ |

(The turret prefab's own AudioSource, medicalShot_fire with playOnAwake off, is never played by its code.)

## 5. Probed (office PC, TTO's 2026-11-09 bundles; `probe.json`, `compact.txt`)

All 25 export; the one warning is `bountyHunt_claim`'s Animator Avatar (`dollarAvatar`, written by name only: left out
anyway). Materials 60: addsoft 18, add 7, alpha 4, premul 1, `Particles/Standard Unlit` 5, `FlexibleCelShader/Cel No
Outline` 7, `Particles/AdditiveOffset` 1 (built), **`Eric/URP Particles/Additive` 15 + `/Alpha Blended` 1** (P6),
`Legacy Shaders/Specular` 1 (the claim's dollar only: not cued).

| prefab | EffectControl (life + after) | what it holds | own sound | needs |
|---|---|---|---|---|
| bountyHunt_poster | 1.0 + 0 (the code destroys it at 0.25) | Front / Back StaticMesh quads (tto_rabbitRow6_wanted), TrailRendererModern | - | P3 |
| bountyHunt_pin | 0.7 + 0.3 | Shuriken Sparks (World collision), ImageEmitter flash | truceTrading_fail 0.6 | - |
| bountyHunt_flare | 2.6 + 0.4 | Star (Shuriken, TrailModule), Burst / Flash 11.5 m up, Muzzle (up): smoke, Line / Image emitters | nAttack 1.0 | - |
| bountyHunt_muzzle | 0.8 + 0.3 | Fire: smoke, Line / Image emitters; Sparks; Flash | nAttack 1.0 | - |
| bountyHunt_tracer | none (RabbitTracer life 0.32) | LineRenderer + RabbitTracer (0.32 / 0.08 / 0.16, head Spark) | - | built |
| bountyHunt_hit | 0.9 + 0.3 | Hit: Shuriken, Image / Line / 2 Ring emitters; Sparks | - | - |
| coinRicochet_flick | 0.5 + 0.3, followPosition | Glints (Shuriken), Flash | - | - |
| coinRicochet_coin | 3.0 + 0 (the code destroys it at the shot) | Coin StaticMesh + **RabbitSpin** (y, 900), Glint, TrailRendererModern | - | P1, P2 |
| coinRicochet_shot | none (RabbitTracer 0.22) | LineRenderer + RabbitTracer (0.22 / 0.05 / 0.09), Muzzle: smoke, LineEmitter | nAttack 1.0 | built |
| coinRicochet_ping | 0.5 + 0.3 | Sparks, RingEmitter, Flash | gilShot 0.75 | - |
| coinRicochet_ricochet | none (RabbitTracer 0.26) | LineRenderer + RabbitTracer (0.26 / 0.06 / 0.1) | - | built |
| coinRicochet_cashTracer | none (RabbitTracer 0.35) | LineRenderer + RabbitTracer (0.35 / 0.06 / 0.18) | - | built |
| coinRicochet_hit | 0.8 + 0.3 | Hit: Shuriken (tto_Gil), Image / Line emitters; Sparks | gilShot_hit 1.0 | - |
| coinRicochet_cashout | 1.6 + 0.4 | Hit, Burst, **Stars** (URP Additive), Coins, Flash | gilShot_hit 1.0 | P6 |
| medicTurret | none (the code: Life 15, Die, Destroy) | **RabbitMedicTurret**, CharacterControl (Race 4), CharacterController, Animation (no clip); Model: Base / Head StaticMesh (cel), Muzzle, Lamp, Beacon; Serum, Cross / LifeMotes (URP), Halo0/1 RingEmitters, FieldSparkles, Field GroundHug 6 m (repeatForever), Aura | - | P5, P6 |
| medicTurret_cast | 0.9 + 0.3, followPosition | GroundHug ring, LineEmitter, Seal: 11 Shuriken systems (URP Additive / Alpha Blended) | cast1 0.8 | P6 |
| medicTurret_deploy | 1.2 + 0.4 | 2 GroundHug rings (to 6 m), Emblem (AdditiveOffset ImageEmitter), Sparks | medicalShot_ring 0.9 | - |
| medicTurret_beat | 1.0 + 0.3 | GroundHug pulse 0.5 -> 6 m, Flash ring 6 m, Sparks | healingField 0.6 | - |
| medicTurret_shot | none (RabbitTracer 0.25) | LineRenderer + RabbitTracer (0.25 / 0.05 / 0.1), Muzzle LineEmitter | medicalShot_fire 1.0 | built |
| medicTurret_capsule | 1.0 + 0.2 (the code destroys it at 0.25) | Capsule StaticMesh (cel), Glow, TrailRendererModern | - | P4 |
| medicTurret_hit | 1.0 + 0.3 | Hit: Shuriken Glow / Sparks (**NoiseModule**) / Flash | medicalShot_hit 0.8 | P6 (noise) |
| medicTurret_break | 1.4 + 0.4 | Sparks, Serum (World collision), GroundHug ring, Flash | backpack_hit 0.8 | - |
| bountyHunt_claim | 2.2 + 0.5 | dollar (Specular, Animator, PowerUpRotation), runes, coins, ring | coin 0.9 | not cued |
| bounty | none (the status) | Poster, Crosshair (Shuriken) | - | not cued |
| gilded | none (the status) | Glints, Shimmer GroundHug (repeatForever) | - | not cued |

BB's copies (`probe_bb.json`): `lifeShot`, `boostShot`, `heatShot`: EffectControl 1.0 + 1.0, no follow, own
medicalShot_hit 1.0: ready. The prefab root's stored position (the turret's (-0.2, 50, -64.3)) is ignored: the page
places a root at the cue's spot, as Instantiate does (`index.html` Fx, the `n.parent < 0` branch).

## 6. Parts the page lacks (effect: part)

Every part is cued anyway (the rule); the TTO file to hold them: `wardrobe/fxparts/tto_rabbit.js`.

| # | Part | Effects | What it does (source) |
|---|---|---|---|
| P1 | `RabbitSpin` (TTO.Game TypeDefIndex 3913, in the prefab) | coinRicochet_coin (Coin) | `Update@0x1E6EE30`: `transform.Rotate(axis, degreesPerSecond x deltaTime, Space.Self)` (`spin.asm`); the prefab: axis (0, 1, 0), 900. |
| P2 | `Rabbit.CoinRise` (code mover, CODE_MOVERS) | coinRicochet_coin | From the cue's spot (the hand) to `to` (the hang spot): u = clamp01((age - delay) / 0.35), e = 1 - (1 - u)^2, position = lerp(from, to, e) + up x 0.08 sin(40 delay + 6 now), now = the clip time (`fx.at.at` + age; question 3) (`:440-539`). The cue's `kill` ends it at the shot. |
| P3 | `Rabbit.PosterFly` (code mover) | bountyHunt_poster | 0.25 s: s = 4 age, position = lerp(from, `to`, clamp01(s)) + up x 0.8 s (1 - s); `Rotate(forward, 900 dt, Self)` (`:628-715`); gone at 0.25 (the cue's `kill`). |
| P4 | `Rabbit.TurretCapsule` (code mover) | medicTurret_capsule | 0.25 s: position = lerp(from, `to`, clamp01(4 age)); `Rotate(right, 1080 dt, Self)` (`:24985-25049`); gone at 0.25 (`kill`). |
| P5 | `RabbitMedicTurret` (TTO.Game, in the prefab) | medicTurret | Model localScale 0.01 at the spawn, then max(0.01, k (1 + 0.18 sin(1.5 pi k)(1 - k))), k = clamp01(age / 0.45) (`RMT.c:142-161`, `:225-252`); Head: toward vFlat(aimDir) at 540 deg/s, aimDir = its forward until the first of `beats`, then snapped to face `aim` (the cue's point: her feet) (`:314-351`, `:1321-1327`); at `end` (seconds after the spawn; Monkey decision 30's option) the grow stops and the Model shrinks linearly from its scale to 0.01 over 0.4 s (`:1501-1526`; the cue's `kill` = end + 0.4). The beats' looks are cued (beat, shot, capsule, hit). CharacterControl / CharacterController draw nothing; its Animation has no clip. |
| P6 | Shaders `Eric/URP Particles/Additive`, `/Alpha Blended`; Shuriken `NoiseModule` | medicTurret, medicTurret_cast, coinRicochet_cashout; medicTurret_hit | Monkey decisions 61 and 62 (built with the Monkey's parts: one part, every class). |
| P7 | `SKILL_FX["rabbit"]` and `CODE_MOVERS` in `wardrobe_fx_tto.py` | all | SKILL_FX = the 22 cued TTO prefabs + `bounty`, `gilded`, `bountyHunt_claim` (built, not cued: the Cat's and the Wolf's precedent); CODE_MOVERS `coinRicochet_coin: Rabbit.CoinRise`, `bountyHunt_poster: Rabbit.PosterFly`, `medicTurret_capsule: Rabbit.TurretCapsule`. (The 22 come in by `cue_tto` from the cue file anyway.) |

Not needed: `RabbitTracer` (tto_sheep.js, decompiled with the Sheep; the five tracers' fields above), the `to` option
(cueOf passes it), `"a|b"` picks, World collision, the TrailModule, TrailRendererModern.

## 7. The cue entries (ready to paste into `wardrobe/fx_cues/rabbit.json`)

`checks/fx_rabbit_research/tto/cues_block.txt` (built by `cues.py` + `block.py`, parsed back): 3 keys, **82 cues**. The
file is `{}` today, so this block is the whole file until the other reports' entries join it. Options beyond the page's
own: `delay` (P2), `end`, `beats`, `aim` (P5) for the parts (`fx.at`, cueOf passes unknown keys through).

```json
{
  "bountyHunt": {
    "why": "TTO1102:Rabbit.<RPC_bountyHunt>d__352::MoveNext@0x1E30840 (pseudo/Rabbit.c:3251-3674; plans/fx_rabbit/tto.md 2.1): Row6Begin(bountyHunt) = PlayAnimation(clip, 0.1), Once (:3321; Rabbit::Row6Begin@0x1E10F50 :38981); cooldown agiAdjust(120) (:3329); Row6Voice(contract1, contract2) = voices/contract1 or contract2, Random.Range(0, 2), volume 1 for the owner (:3331; Row6Voice@0x1E12B10 :38831-38896); Until(start + 0.4) (:3381): Row6Sound(truceTrading, 0.8) (:3394; sounds/, x 0.7 for others, Row6Sound@0x1E12290 :38898-38930) and PosterFly from Row6Hand(false) = mountHand_L (:3403; Row6Hand@0x1E11AB0 :39306; the clip at 0.4 s: 0.039 m left, 0.884 up, 0.349 ahead, checks/fx_rabbit_research/tto/bones.txt): <PosterFly>d__353::MoveNext@0x1E28850 (:556-786) spawns bountyHunt_poster there with the hero's rotation (:614), flies it 0.25 s (:628) to the target's chest + 0.6 up (:654; Row6Chest@0x1E11140 = the collider's bounds centre, the standard target body 0.6 m up 10 m ahead) along lerp(from, to, clamp01(4t)) + up x 0.8 x 4t (1 - 4t) (:667-693), turning about its own forward 900 deg/s (:715), then Destroy (:733) and bountyHunt_pin at the chest, identity (:764) (its own sound truceTrading_fail 0.6), with the Bounty status (eStatus 719, 12 s, :769) and BountyWatch (:772); Until(start + 0.85) (:3410): bountyHunt_flare at Row6Muzzle, identity (:3431; Row6Muzzle@0x1E11BF0 :39352-39490: a child named fire / Fire / muzzle under mountHand_R, else mountHand_R + 0.35 x forward (:39468); no Rabbit gun has one, data/rabbit/props_weapons.json: 0.205 right, 1.082 up, 0.475 ahead at 0.85 s) and Row6Sound(shotgun, 0.8) (:3433); BountyOrders (:3436) sends Contract's units, none here; the hired guns at Until(start + HiredGunAt[i]) = 1.15 / 1.35 / 1.55 (:3464; Rabbit::.cctor@0x1E12F10 :41886: HiredGunAt [1.15, 1.35, 1.55], HiredGunAngle [-65, 65, 180]): gun = spot + AngleAxis(HiredGunAngle[i], up) x vFlat(hero - spot) x 14 + up x 7 (:3533-3602; spot = the target's feet, dir (0, 0, -1)): (12.688, 7, 4.083), (-12.688, 7, 4.083), (0, 7, 24); bountyHunt_muzzle at the gun, LookRotation(chest - gun) (:3613-3618), bountyHunt_tracer = Row6Tracer(gun, chest) (:3625; Row6Tracer@0x1E12940 :41234: Instantiate at the gun, identity, RabbitTracer.Set(gun, chest)), bountyHunt_hit at the chest, LookRotation(gun - chest) (:3637-3642), Row6Sound(deadShot, 0.8) (:3643), HiredGunHit (:3654, no raycast, no effect); Until(start + 1.8) (:3474): Row6End (:3665), the clip's 1.8 s. Left out: the Bounty look on the foe (bountyFx, CharacterControl::AddRabbitRow6Fx@0x24AE1D0; Sheep decision 4) and the kill claim (BountyClaim@0x1E05700 / BountyClaimFx@0x1E05380: bountyHunt_claim + truceTrading_success; needs a kill)",
    "cues": [
    [0, "voice", "contract1|contract2"],
    [0.4, "sound", "truceTrading", {"vol": 0.8}],
    [0.4, "fx", "tto/bountyHunt_poster", {"x": -0.039, "y": 0.884, "d": 0.349, "to": [0, 1.2, 10], "kill": 0.25}],
    [0.65, "fx", "tto/bountyHunt_pin", {"y": 0.6, "d": 10}],
    [0.85, "fx", "tto/bountyHunt_flare", {"x": 0.205, "y": 1.082, "d": 0.475}],
    [0.85, "sound", "shotgun", {"vol": 0.8}],
    [1.15, "fx", "tto/bountyHunt_muzzle", {"x": 12.688, "y": 7.0, "d": 4.083, "rot": [24.567, -65.0, 0]}],
    [1.15, "fx", "tto/bountyHunt_tracer", {"x": 12.688, "y": 7.0, "d": 4.083, "to": [0, 0.6, 10]}],
    [1.15, "fx", "tto/bountyHunt_hit", {"y": 0.6, "d": 10, "rot": [-24.567, 115.0, 0]}],
    [1.15, "sound", "deadShot", {"vol": 0.8}],
    [1.35, "fx", "tto/bountyHunt_muzzle", {"x": -12.688, "y": 7.0, "d": 4.083, "rot": [24.567, 65.0, 0]}],
    [1.35, "fx", "tto/bountyHunt_tracer", {"x": -12.688, "y": 7.0, "d": 4.083, "to": [0, 0.6, 10]}],
    [1.35, "fx", "tto/bountyHunt_hit", {"y": 0.6, "d": 10, "rot": [-24.567, -115.0, 0]}],
    [1.35, "sound", "deadShot", {"vol": 0.8}],
    [1.55, "fx", "tto/bountyHunt_muzzle", {"x": 0.0, "y": 7.0, "d": 24.0, "rot": [24.567, 180.0, 0]}],
    [1.55, "fx", "tto/bountyHunt_tracer", {"x": 0.0, "y": 7.0, "d": 24.0, "to": [0, 0.6, 10]}],
    [1.55, "fx", "tto/bountyHunt_hit", {"y": 0.6, "d": 10, "rot": [-24.567, 0.0, 0]}],
    [1.55, "sound", "deadShot", {"vol": 0.8}]
    ]
  },
  "coinRicochet": {
    "why": "TTO1102:Rabbit.<RPC_coinRicochet>d__343::MoveNext@0x1E36300 (pseudo/Rabbit.c:6311-6692; plans/fx_rabbit/tto.md 2.2), no voice: Row6Begin(coinRicochet) (:6371); cooldown agiAdjust(60) (:6379); the four hang spots hang[i] = TransformPoint(CoinHang[i]) at the cast (:6469; Rabbit::.cctor@0x1E12F10 :41886: (-0.9, 1.55, 1.6), (-0.3, 1.85, 1.9), (0.3, 1.75, 1.8), (0.9, 1.5, 1.55), x right, z ahead); Until(start + 0.3) (capstone 0x1E36D77, checks/fx_rabbit_research/tto/coin_movenext.asm): Row6Sound(coin, 1) (:6493), coinRicochet_flick owned at Row6Hand(false) = mountHand_L with the hero's rotation (:6494-6508; the clip at 0.3 s: 0.098 m left, 1.068 up, 0.192 ahead, bones.txt), four coinRicochet_coin there, identity (:6526), each CoinRise(coin, hand, hang[i], delay 0.04 i) (:6509, :6543; <CoinRise>d__346::MoveNext@0x1E27890 :440-539: e = 1 - (1 - clamp01((now - t0 - delay) / 0.35))^2, position = lerp(hand, hang, e) + up x 0.08 sin(40 delay + 6 Time.time) :469-524; part P2 on the coin, its Coin node spun 900 deg/s by RabbitSpin, part P1); coin k at Until(start + CoinShotAt[k]) = 0.75 / 0.95 / 1.15 / 1.35 (capstone 0x1E36963; CoinShotAt, the .cctor): the coin destroyed (:6628: kill = CoinShotAt[k] - 0.3), coinRicochet_shot = Row6Tracer(Row6Muzzle, coin) (:6632-6636; Row6Muzzle = mountHand_R + 0.35 forward, no gun has a muzzle child: bones.txt at each shot), coinRicochet_ping at the coin, identity (:6645; its own sound gilShot 0.75), CoinChain -> <CoinRicochets>d__348::MoveNext@0x1E27210 (:6648; :173-423): hop 0 CoinNext(coin, the selected target, 18 m) (:303-311) = the target; coinRicochet_ricochet (coin 4, the cash-out coin k = CoinShotAt.Length - 1 (:235): coinRicochet_cashTracer) = Row6Tracer(coin, Row6Chest) (:393-404; the coin's spot is hang[k] with the bob at the shot's clip time, decision in question 3); Waits.Get(0.07) (:408): coinRicochet_hit (cash out: coinRicochet_cashout) at the chest, identity (:269), Row6Sound(gilShot_hit 0.7, or diamondShot 0.7 for the cash out) only when hop > 0 or cash out (:276; the volume 0.7 from the instructions, capstone 0x1E27439, ricochets.asm); hops 2-3 look for another foe within 9 m (:303): none here, so each coin hits once (no miss tracer: that is hop 0 only, :353-357); Until(start + 1.9) (capstone 0x1E369CF): Row6End (:6561), the clip's 1.9 s. Left out: the Gilded look on the foe (gildedFx, AddRabbitRow6Fx; Sheep decision 4) and the gold chat (CoinSettle@0x1E06F80)",
    "cues": [
    [0.3, "sound", "coin"],
    [0.3, "fx", "tto/coinRicochet_flick", {"x": -0.098, "y": 1.068, "d": 0.192}],
    [0.3, "fx", "tto/coinRicochet_coin", {"x": -0.098, "y": 1.068, "d": 0.192, "to": [-0.9, 1.55, 1.6], "delay": 0.0, "kill": 0.45}],
    [0.3, "fx", "tto/coinRicochet_coin", {"x": -0.098, "y": 1.068, "d": 0.192, "to": [-0.3, 1.85, 1.9], "delay": 0.04, "kill": 0.65}],
    [0.3, "fx", "tto/coinRicochet_coin", {"x": -0.098, "y": 1.068, "d": 0.192, "to": [0.3, 1.75, 1.8], "delay": 0.08, "kill": 0.85}],
    [0.3, "fx", "tto/coinRicochet_coin", {"x": -0.098, "y": 1.068, "d": 0.192, "to": [0.9, 1.5, 1.55], "delay": 0.12, "kill": 1.05}],
    [0.75, "fx", "tto/coinRicochet_shot", {"x": -0.03, "y": 0.9, "d": 0.454, "to": [-0.9, 1.472, 1.6]}],
    [0.75, "fx", "tto/coinRicochet_ping", {"x": -0.9, "y": 1.472, "d": 1.6}],
    [0.75, "fx", "tto/coinRicochet_ricochet", {"x": -0.9, "y": 1.472, "d": 1.6, "to": [0, 0.6, 10]}],
    [0.82, "fx", "tto/coinRicochet_hit", {"y": 0.6, "d": 10}],
    [0.95, "fx", "tto/coinRicochet_shot", {"x": 0.021, "y": 0.904, "d": 0.43, "to": [-0.3, 1.918, 1.9]}],
    [0.95, "fx", "tto/coinRicochet_ping", {"x": -0.3, "y": 1.918, "d": 1.9}],
    [0.95, "fx", "tto/coinRicochet_ricochet", {"x": -0.3, "y": 1.918, "d": 1.9, "to": [0, 0.6, 10]}],
    [1.02, "fx", "tto/coinRicochet_hit", {"y": 0.6, "d": 10}],
    [1.15, "fx", "tto/coinRicochet_shot", {"x": 0.056, "y": 0.904, "d": 0.407, "to": [0.3, 1.7, 1.8]}],
    [1.15, "fx", "tto/coinRicochet_ping", {"x": 0.3, "y": 1.7, "d": 1.8}],
    [1.15, "fx", "tto/coinRicochet_ricochet", {"x": 0.3, "y": 1.7, "d": 1.8, "to": [0, 0.6, 10]}],
    [1.22, "fx", "tto/coinRicochet_hit", {"y": 0.6, "d": 10}],
    [1.35, "fx", "tto/coinRicochet_shot", {"x": 0.089, "y": 0.9, "d": 0.376, "to": [0.9, 1.526, 1.55]}],
    [1.35, "fx", "tto/coinRicochet_ping", {"x": 0.9, "y": 1.526, "d": 1.55}],
    [1.35, "fx", "tto/coinRicochet_cashTracer", {"x": 0.9, "y": 1.526, "d": 1.55, "to": [0, 0.6, 10]}],
    [1.42, "fx", "tto/coinRicochet_cashout", {"y": 0.6, "d": 10}],
    [1.42, "sound", "diamondShot", {"vol": 0.7}]
    ]
  },
  "medicTurret": {
    "why": "TTO1102:Rabbit.<RPC_medicTurret>d__334::MoveNext@0x1E420E0 (pseudo/Rabbit.c:13058-13300; plans/fx_rabbit/tto.md 2.3): Row6Begin(medicTurret) (:13131); cooldown agiAdjust(90) (:13139); Row6Voice(lifeShot1, lifeShot2) (:13141); medicTurret_cast owned at the hero, the hero's rotation (:13153); Until(start + 0.55) (:13158): Row6Sound(backpack_hit, 0.9) (:13172), the spot 1.8 m ahead (no wall within 2.3 m, :13212-13234) on the ground (Row6Ground :13254) -> RPC_medicTurret_create@0x1E0DE50 (:13268; :39868-40089): medicTurret at the spot, LookRotation(flat aim) = the hero's facing (:39948-39959), RabbitMedicTurret.Init (:40056), medicTurret_deploy at the spot, identity (:40085); Until(start + 1.3): Row6End (:13280-13292), the clip's 1.3 s. The turret (TTO1102:RabbitMedicTurret, pseudo_c6_extra/rabbit/RabbitMedicTurret.c; part P5): its Model grows over 0.45 s (:225-252), beats at 0.75 + 1.5 k s after its spawn (:142, :403; Beats 10, Life 15, dump.cs:120553-120560): each beat MedicTurretPulse (heals, no look, :461), MedicTurretPick = the lowest-HP ally within 10 m, the Rabbit included, the turret itself never (Race 4 Robots skipped, Rabbit.c:40167; its CharacterControl Race 4, probe.json) = the Rabbit, the only ally (Sheep decision 1); kind Random.Range(1, 4) (:471): <Fire>d__29::MoveNext@0x1E74270 (:1181-1392): MedicTurretBeatFx = medicTurret_beat at the turret, identity (:1251; Rabbit.c:40376), the head turned to her (:1321-1327), MedicTurretShotFx from the Muzzle (Head 0.78 + Muzzle (0, 0.06, 0.3345) turned to her: 0.84 up, 1.466 ahead) (:1372; Rabbit.c:40218-40344): medicTurret_shot there, identity, RabbitTracer.Set(muzzle, her chest = her CharacterController centre 0.7 m up, checks/fx_rabbit_research/tto/cc.txt) (:40264-40318) and <TurretCapsule>d__338::MoveNext@0x1E7AA60 (Rabbit.c:24911-25135): medicTurret_capsule from the muzzle, lerp to her chest over 0.25 s (:24985-25026), spun about its right 1080 deg/s (:25049), destroyed (:25067), then medicTurret_hit at her chest, identity (:25097) and lifeShot / boostShot / heatShot (kind 1 / 2 / 3, one each third) at her feet, identity, Destroy 2 s (:25119-25130); the statuses autoLife / boost / heat draw nothing (DecompiledSource/CharacterControl.cs:37491-37520). The game's turret lives 15 s (10 beats) and dies by Die -> <RPC_dead>d__31@0x1E768C0: medicTurret_break at it (:1469), the Model shrunk over 0.4 s (:1501-1526), Destroy (:1507): cut at 10 s after the spawn (question 1, the standing rule; Monkey decision 30's `end`): 7 beats, the end at 10.55 s",
    "cues": [
    [0, "voice", "lifeShot1|lifeShot2"],
    [0, "fx", "tto/medicTurret_cast"],
    [0.55, "sound", "backpack_hit", {"vol": 0.9}],
    [0.55, "fx", "tto/medicTurret", {"d": 1.8, "kill": 10.4, "end": 10.0, "beats": [0.75, 2.25, 3.75, 5.25, 6.75, 8.25, 9.75], "aim": [0, 0, 0]}],
    [0.55, "fx", "tto/medicTurret_deploy", 1.8],
    [1.3, "fx", "tto/medicTurret_beat", 1.8],
    [1.3, "fx", "tto/medicTurret_shot", {"y": 0.84, "d": 1.466, "to": [0, 0.7, 0]}],
    [1.3, "fx", "tto/medicTurret_capsule", {"y": 0.84, "d": 1.466, "to": [0, 0.7, 0], "kill": 0.25}],
    [1.55, "fx", "tto/medicTurret_hit", {"y": 0.7}],
    [1.55, "fx", "lifeShot|boostShot|heatShot", {"kill": 2}],
    [2.8, "fx", "tto/medicTurret_beat", 1.8],
    [2.8, "fx", "tto/medicTurret_shot", {"y": 0.84, "d": 1.466, "to": [0, 0.7, 0]}],
    [2.8, "fx", "tto/medicTurret_capsule", {"y": 0.84, "d": 1.466, "to": [0, 0.7, 0], "kill": 0.25}],
    [3.05, "fx", "tto/medicTurret_hit", {"y": 0.7}],
    [3.05, "fx", "lifeShot|boostShot|heatShot", {"kill": 2}],
    [4.3, "fx", "tto/medicTurret_beat", 1.8],
    [4.3, "fx", "tto/medicTurret_shot", {"y": 0.84, "d": 1.466, "to": [0, 0.7, 0]}],
    [4.3, "fx", "tto/medicTurret_capsule", {"y": 0.84, "d": 1.466, "to": [0, 0.7, 0], "kill": 0.25}],
    [4.55, "fx", "tto/medicTurret_hit", {"y": 0.7}],
    [4.55, "fx", "lifeShot|boostShot|heatShot", {"kill": 2}],
    [5.8, "fx", "tto/medicTurret_beat", 1.8],
    [5.8, "fx", "tto/medicTurret_shot", {"y": 0.84, "d": 1.466, "to": [0, 0.7, 0]}],
    [5.8, "fx", "tto/medicTurret_capsule", {"y": 0.84, "d": 1.466, "to": [0, 0.7, 0], "kill": 0.25}],
    [6.05, "fx", "tto/medicTurret_hit", {"y": 0.7}],
    [6.05, "fx", "lifeShot|boostShot|heatShot", {"kill": 2}],
    [7.3, "fx", "tto/medicTurret_beat", 1.8],
    [7.3, "fx", "tto/medicTurret_shot", {"y": 0.84, "d": 1.466, "to": [0, 0.7, 0]}],
    [7.3, "fx", "tto/medicTurret_capsule", {"y": 0.84, "d": 1.466, "to": [0, 0.7, 0], "kill": 0.25}],
    [7.55, "fx", "tto/medicTurret_hit", {"y": 0.7}],
    [7.55, "fx", "lifeShot|boostShot|heatShot", {"kill": 2}],
    [8.8, "fx", "tto/medicTurret_beat", 1.8],
    [8.8, "fx", "tto/medicTurret_shot", {"y": 0.84, "d": 1.466, "to": [0, 0.7, 0]}],
    [8.8, "fx", "tto/medicTurret_capsule", {"y": 0.84, "d": 1.466, "to": [0, 0.7, 0], "kill": 0.25}],
    [9.05, "fx", "tto/medicTurret_hit", {"y": 0.7}],
    [9.05, "fx", "lifeShot|boostShot|heatShot", {"kill": 2}],
    [10.3, "fx", "tto/medicTurret_beat", 1.8],
    [10.3, "fx", "tto/medicTurret_shot", {"y": 0.84, "d": 1.466, "to": [0, 0.7, 0]}],
    [10.3, "fx", "tto/medicTurret_capsule", {"y": 0.84, "d": 1.466, "to": [0, 0.7, 0], "kill": 0.25}],
    [10.55, "fx", "tto/medicTurret_hit", {"y": 0.7}],
    [10.55, "fx", "lifeShot|boostShot|heatShot", {"kill": 2}],
    [10.55, "fx", "tto/medicTurret_break", 1.8]
    ]
  }
}
```

Notes on the block:
- `"lifeShot|boostShot|heatShot"` is the page's per-cue random pick (`pickOf`, made when the clip starts): one pick per
  beat, a third each, as the game's `Random.Range(1, 4)` per beat.
- The poster's and the capsule's `kill` 0.25 is the movers' own Destroy, written on the cue too, so they also end right
  before P3 / P4 exist (otherwise they would sit at the hand / muzzle for their EffectControl life).
- Every muzzle and hand spot is fixed at the cue's time (the game reads the bone then; the effects do not follow it).

## 8. Open questions (each with my recommended answer)

1. **Medic Turret's length: 10 s or the game's 15 s?** Recommend **10 s after the spawn** (7 beats, the end's break and
   shrink at 10.55 s), the standing rule for summons (Monkey decision 30's `end: 10`, Mole decision on Barrel Railgun's
   ride, Bat's Mind Control). B: the full 15 s (10 beats to 15.35, `end` 15, `kill` 15.4, the break at 15.55; three
   more beat groups at 11.8 / 13.3 / 14.8).
2. **The capsule's target: the Rabbit herself?** Recommend **yes**: the game picks her (lowest HP share within 10 m, ties
   to the nearest, the Rabbit included, the Robot-race turret skipped; Read this first 3), and Sheep decision 1 puts ally
   skills on the hero. B: an ally standing at the 10 m point (Monkey decision 20's ally analogue) would need a body
   there and 10 m capsule flights the game would not make (the pick reaches 10 m from the turret, which stands 8.2 m from
   it: in reach, but nearer is the Rabbit at equal HP).
3. **The coins' bob phase.** CoinRise bobs by `sin(40 delay + 6 Time.time)`: absolute time, so any phase is a real game
   moment. Recommend **Time.time = 0 at the cast** (P2 uses the clip's time; the shot tracers' ends and the pings are
   cued at that phase, so they meet the coin exactly). B: P2 with a random phase and the cues at the hang spots (up to
   8 cm off).
4. **The Medic Turret tile under the loop toggle.** With วนซ้ำ on, a single clip restarts at its 1.3 s end and its
   unreached cues are dropped (`seqTick` / `fxStart`; the Mole verification's note on `missilePad`), so the turret would
   vanish after one beat. Recommend **a hold line** in `SEQ.rabbit` (`index.html:1351`): `"Medic Turret: medicTurret@10.95"`
   (the clip, then held to the turret's end, as the Chameleon's `"Torment Rain: rainOfArrow@2.7"`, `index.html:1288`);
   the plain `medicTurret` key still matches (the `@MedicTurret:` key is tried first and falls back). Bounty Hunt and Coin
   Ricochet need none (every cue inside their clips). B: leave it (loop off is the default; the tail plays then).
5. **The status looks on the foe** (Bounty's 12 s wanted poster + crosshair, Gilded's glints). Recommend **left out**
   (Sheep decision 4, Chameleon decision 53's Prey, Cat decision 44), built but not cued (P7). They are the skills' most
   visible marks on the target, so this one is worth a look from the user later.
6. **The hand spots.** Recommend the **fixed spots from the clip** (`bones.txt`), as the Chameleon's (its `bones.py`).
   If the hero is ever scaled or lifted on these tiles, a `bone`-relative spot would be needed (none is: no lift, no
   scale cue).

## 9. For the Bible (offer to the user; that repo's own rules)

- **Bounty Hunt:** the poster leaves the Rabbit's **left** hand, spins 900 deg/s on a 0.2 m arc and lands 0.6 m above the
  target's chest; the flare is fired straight up from her gun (its burst 11.5 m up); the three hired-gun shots come out
  of the air 14 m from the target and 7 m up, at -65 / +65 / 180 degrees from the target-to-Rabbit line (no gunman model),
  each a tracer with a muzzle flash and the deadShot sound; the target shows a wanted poster + crosshair (`bountyFx`) for
  the 12 s; a claimed bounty shows a spinning gold dollar (`bountyHunt_claim`) with truceTrading_success.
- **Coin Ricochet:** the four coins are flicked from the left hand and rise in 0.35 s (0.04 s apart) to fixed spots in
  front of her (0.9 / 0.3 m either side, 1.5-1.85 m up, 1.55-1.9 m ahead), bobbing 0.08 m and spinning 900 deg/s; each is
  shot from her gun 0.2 s apart; only bounces (hops 2-3) and the cash-out coin play a hero sound on their hit
  (gilShot_hit / diamondShot at 0.7); a coin with no target in reach shoots its tracer 8 m forward.
- **Medic Turret:** the turret grows in over 0.45 s, turns its head to the ally it shoots, and shrinks away over 0.4 s at
  its end (medicTurret_break); with no other ally it shoots the Rabbit herself (the turret's own Race is Robots, which
  the pick skips: the Bible's "the turret's Race is not claimed either way", :1031, can now be filled in: Race 4,
  its prefab's CharacterControl); each capsule flies 0.25 s spinning 1080 deg/s and shows Life / Boost / Heat Shot's own
  hit effect on the ally for 2 s.

## Verification (the researcher's own checks)

- Every time: the coroutine's `Until` constants as the annotator labels them (Bounty Hunt 0.4 / 0.85 / HiredGunAt /
  1.8; Medic Turret 0.55 / 1.3; the turret 0.75 / 1.5 / 15 / 16.5 / 0.45 / 0.4; PosterFly 0.25; TurretCapsule 0.25 and
  Waits 0.25; CoinRise 0.35) and the three Ghidra dropped in RPC_coinRicochet read from the instructions
  (`coin_movenext.asm`: 0.3 at 0x1E36D77, CoinShotAt[k] at 0x1E36963, 1.9 at 0x1E369CF); the tables from the .cctor's
  `InitializeArray` labels and its CoinHang stores (0xBF666666 ... decoded: -0.9, 1.55, 1.6 ...). All agree with the
  Bible (:1023-1027, :1041-1042, :1058-1061).
- Row6Hand(false) = mountHand_L: the field index `(right ^ 1)` over mHandR 0x710 / mHandL 0x718 (`:39306-39350`).
- The capsule's kind -> effect: `kind 2 boostShot, kind 3 heatShot, else lifeShot` (`:25098-25102`, the raw lines).
- `cues.py` builds the block from these numbers and checks every `tto/` name in `probe.json`, every BB effect in the
  rip's `heroes/rabbit/effects/`, every sound / voice in its `sounds/` / `voices/`; `block.py` re-parses the pasted text
  (82 cues). The hired-gun rotations re-computed by hand (atan2(6.4, 14) = 24.567; yaw atan2(-12.688, 5.917) = -65).
- Not done: a browser check (read-only researcher); P1-P5 are specified, not built; the bob phase (question 3) is a
  choice, not a game fact.

## Verification (13/11/2026)

Checker, office PC, read only (probes in `checks/fx_rabbit_research/verify/tp/`: `tto_probe.json` = a fresh
`wardrobe_fx_tto.py rabbit --probe` of the 25 prefabs + the three BB copies; `cues_check.py` = every paste-ready block
parsed, each cue shaped as `pipeline/wardrobe_fx_check.py:221-222` checks it, keys against `wardrobe/data/rabbit/clips.json`,
`tto/` names against the probe, BB names / voices / sounds against the rip through `wardrobe_fx.rip_wav` /
`hero_sound_wav`). This section wins over the body above.

1. **Confirmed (no change).** Every `Until` / `Waits` constant re-read in `pseudo/Rabbit.c` (Bounty Hunt 0.4 `:3381`, 0.85
   `:3410`, HiredGunAt `:3464`, 1.8 `:3474`; PosterFly 0.25 `:628`; CoinRise 0.35 / 40 / 6 / 0.08 `:469-519`, its t0 =
   Time.time + delay `:469`; the hop 0.07 `:408`; Medic Turret 0.55 / 1.3 `:13158`, `:13280`; TurretCapsule 0.25 / 1080
   `:24985-25049`) and the Ghidra drops in `coin_movenext.asm` (0.3 `0x1E36D77`, 1.9 `0x1E369CF`) and `ricochets.asm`
   (0.7 `0x1E27439`); the statics' order in `dump.cs:120168-120185` (CoinShotAt `0x0`, CoinHang `0x8`, HiredGunAt
   `0x10`, HiredGunAngle `0x18`: the annotator's "Rabbit.HiredGunAngle" label at `:6659` and in the cash-out test `:235`
   is CoinShotAt's array length at `+0x18`, so the cash-out is coin 4, as the body says). The hired guns re-derived from
   `:3528-3605` (AngleAxis about up applied to (0, 0, -1), x 14, + 7 up): (12.688, 7, 4.083) / (-12.688, 7, 4.083) /
   (0, 7, 24), muzzle rot [24.567, -65 / 65 / 180, 0], hit rot [-24.567, 115 / -115 / 0, 0]. The poster flies to the
   chest **+ 0.6 up** (`:650-654`, Vector3.up at static `+0x18`) and the pin spawns at the chest (`:747-764`): `to`
   [0, 1.2, 10] and the pin at y 0.6 are right. Row6Hand(false) = mountHand_L (`:39337`, index `right ^ 1`); Row6Muzzle's
   fallback = mountHand_R + 0.35 x the hero's forward (`:39461-39473`); no Rabbit weapon has a `fire` / `Fire` / `muzzle`
   node (`data/rabbit/props_weapons.json`: 0 of 45); the hand spots re-run with `bones.py` (0.4 s L: -0.039 / 0.884 /
   0.349; 0.85 s R: 0.205 / 1.082 / 0.125 + 0.35; the four coin shots likewise). The coin bob values (1.472 / 1.918 /
   1.700 / 1.526) recomputed. All 25 TTO prefabs and their EffectControl / own sounds match section 5 (`tto_probe.json`;
   RabbitSpin axis (0, 1, 0) 900; the five RabbitTracer fields). The JSON block parses: 3 keys, all real clips (bountyHunt
   1.8, coinRicochet 1.9, medicTurret 1.3), 82 cues, every name present (voices contract1/2, lifeShot1/2 in `voices/`;
   truceTrading, shotgun, deadShot, coin, diamondShot, backpack_hit in `sounds/`). All three clips are in
   `wardrobe/tto_released.json` rabbit: cued. Icons: `data/icons/hd/index.json` has bountyHunt / coinRicochet /
   medicTurret.

2. **Medic Turret: the turret's beats belong to its part, not to cues (the two reports disagree).** This report cues every
   beat (beat, shot, capsule, hit, drop) and P5 only turns the head; `parts.md` Interfaces 3-4 have the turret part and
   `Rabbit.TurretCapsule` spawn the same effects with `api.spawn`. Built as written, both would draw every beat twice.
   Decision (by the earlier classes): the beats are the summon script's own (`RabbitMedicTurret::Update` `RMT.c:397-404`
   -> `Beat` `:451-492` -> `<Fire>d__29` `:1181-1392`), so the part makes them, as the Mole's Auto Gyro Gun fires from its
   part (Mole decision 32, `fxparts/robots.js:57-68` `api.spawn(autoGyroGun_fire)`); the capsule's hit and drop are the
   mover's (`Rabbit.c:25097`, `:25119-25130`; one owner per hit, Monkey decision 21 / Mole decision 22); and part-made
   beats survive the วนซ้ำ toggle (Mole decision 21: "the loop toggle cuts nothing part-made"), so **question 4's hold
   line is dropped** (no `SEQ.rabbit` line for Medic Turret; a held step would also freeze the 1.3 s clip's last pose for
   9.65 s where the game is back at standby). Corrected entry (replaces section 7's `"medicTurret"` in full):

```json
{
  "medicTurret": {
    "why": "TTO1102:Rabbit.<RPC_medicTurret>d__334::MoveNext@0x1E420E0 (pseudo/Rabbit.c:13058-13300; plans/fx_rabbit/tto.md 2.3 and its Verification 2): Row6Begin(medicTurret) (:13131); cooldown agiAdjust(90) (:13139); Row6Voice(lifeShot1, lifeShot2) (:13141); medicTurret_cast owned at the hero, the hero's rotation (:13153); Until(start + 0.55) (:13158): Row6Sound(backpack_hit, 0.9) (:13172), the spot 1.8 m ahead (no wall within 2.3 m, :13212-13234) on the ground (Row6Ground :13254) -> RPC_medicTurret_create@0x1E0DE50 (:39868-40089): an older turret destroyed (:39906-39916), medicTurret at the spot, LookRotation(flat aim) = the hero's facing (:39948-39959), RabbitMedicTurret.Init (:40056), medicTurret_deploy at the spot, identity (:40085); Until(start + 1.3): Row6End (:13280-13292), the clip's 1.3 s. The turret's life is its part's (RabbitMedicTurret, pseudo_c6_extra/rabbit/RabbitMedicTurret.c; tto.md Verification 2's P5): the Model grows over 0.45 s (:225-252); beats at 0.75 + 1.5 k s after the spawn (:142, :397-404), each Fire (:1181-1392): medicTurret_beat at the turret (BeatFx :1251 -> Rabbit.c:40376), the head snapped to the ally (:1321-1327), medicTurret_shot from the Muzzle node with RabbitTracer.Set(muzzle, the ally's chest) and the capsule (Rabbit.c:40218-40344) flown 0.25 s by Rabbit.TurretCapsule (Rabbit.c:24911-25135), which spawns medicTurret_hit at the chest and lifeShot / boostShot / heatShot (Random.Range(1, 4), RMT.c:471) at the feet for 2 s (:25097-25130); the ally = the Rabbit (MedicTurretPick: the lowest HP share within 10 m, her included, the Race 4 turret skipped, Rabbit.c:40141-40209; ally [0, 0.7, 0] = her collider centre, checks/fx_rabbit_research/tto/cc.txt); the game's 15 s cut at 10 s after the spawn (the 10 s rule, Monkey decision 30's end): end 10 = Die -> RPC_dead (RMT.c:1393-1537): medicTurret_break at it, the Model shrunk over 0.4 s, gone: kill 10.4; 7 beats (1.3 ... 10.3 s from the cast). builds: the capsule's drops (BB's copies, Bison decision 43); the tto/ prefabs come from SKILL_FX",
    "builds": ["lifeShot", "boostShot", "heatShot"],
    "cues": [
    [0, "voice", "lifeShot1|lifeShot2"],
    [0, "fx", "tto/medicTurret_cast"],
    [0.55, "sound", "backpack_hit", {"vol": 0.9}],
    [0.55, "fx", "tto/medicTurret", {"d": 1.8, "end": 10, "kill": 10.4, "ally": [0, 0.7, 0]}],
    [0.55, "fx", "tto/medicTurret_deploy", 1.8]
    ]
  }
}
```

   Section 7's block is then 3 keys, **46 cues** (Bounty Hunt 18, Coin Ricochet 23, Medic Turret 5). Parts P4 / P5 become
   (the contract of `parts.md` Interfaces 3-4, with that report's Verification 3):
   - **P5 `RabbitMedicTurret`** (on `tto/medicTurret`'s root): Model scale 0.01 at the spawn, then max(0.01, k (1 + 0.18
     sin(1.5 pi k)(1 - k))), k = clamp01(age / 0.45); beats at age 0.75 + 1.5 k (k = 0 ... 9, only while age < `end`);
     each beat: `api.spawn("tto/medicTurret_beat")` at the turret, identity; the Head snapped to face the flat direction
     to `ally` (between beats turned toward it at 540 deg/s, `RMT.c:314-351`); the muzzle = the `Muzzle` node's world
     position after the snap (0.84 up, 1.466 ahead here); `api.spawn("tto/medicTurret_shot")` there, identity, `to` =
     `ally`; `api.spawn("tto/medicTurret_capsule")` there, identity, `to` = `ally`, `ally` = [ally x, 0, ally d], `kind` =
     lifeShot / boostShot / heatShot (a third each, drawn per beat). At `end`: the beats stop,
     `api.spawn("tto/medicTurret_break")` at the turret, identity, and the Model shrinks linearly from its scale to 0.01
     over 0.4 s; the cue's `kill` removes it. At its build an earlier live `tto/medicTurret` is removed at once (the old
     turret's Destroy, `Rabbit.c:39906-39916`; with วนซ้ำ on, the recast every 1.3 s replaces it instead of stacking).
   - **P4 `Rabbit.TurretCapsule`**: lerp(spawn, `to`, clamp01(4 age)), Rotate(right, 1080 dt, Self); at age 0.25 it removes
     itself and spawns `tto/medicTurret_hit` at `to` (identity) and `kind` at `ally` (identity, kill 2).
   - P2 / P3 unchanged (PosterFly spawns nothing on arrival: the pin is cued; `parts.md` Verification 2).
   - `pipeline/wardrobe_fx_check.py` OPTS (the lead's) += `delay` (P2) and `ally` (P5); `end` is there already; the body's
     `beats` / `aim` options are gone.

3. **Coin Ricochet charges Gil per hit (not in the body).** Each landed hop first calls `CoinPayHit` on the owner's client
   (`Rabbit.c:384-388`; `CoinPayHit@0x1E06C00` `:38057-38105`: the next hit's price `CoinRicochetCost(hits + 1) - paid`
   from `PlayerData.Gil`; short of Gil: `mCoinBroke`, and that hop's tracer, hit and sound are skipped). The page plays
   the Rabbit with enough Gil (every cue as written); the chat summary (`CoinSettle@0x1E06F80`: "... G total", "out of
   gil, the rest dropped") stays out with the other chat lines. The Bible's Gold bullet has the price already: nothing new
   to offer.

4. **Section 8 questions 1, 2, 3, 5, 6: kept** (10 s cut after the spawn = Monkey decision 30, Mole 32; the capsule on the
   Rabbit = Sheep decision 1; the bob from the clip time: `fx.at.at` is the cue's time, as `fxparts/tto_penguin.js:42`
   reads it; status looks out = Sheep decision 4; fixed hand spots). **Question 4: dropped** (item 2).

5. **Nothing missed.** Every string the three coroutines and their helpers load is accounted for (Bounty Hunt 10, Coin
   Ricochet 6 + CoinRicochets 7, Medic Turret 6 + TurretCapsule 5, RabbitMedicTurret's states `dead` / `none`; no other
   effect, voice or sound). `MedicTurretPulse` (`Rabbit.c:40517-40592`) heals and draws nothing, so there is one
   `medicTurret_beat` per beat (Fire's BeatFx; Beat's own BeatFx call, `RMT.c:486`, is the no-ally branch only).

6. **P6 is built already** (by the Monkey's builders during this check, uncommitted): the two Eric/URP shaders through
   `api.shader` in `fxparts/tto_monkey.js:153-154` and Shuriken's NoiseModule in `fxparts/shuriken.js:310-323`, `:488`.
   Nothing to build for P6; P1-P5 (with item 2's P4 / P5) and P7 remain.
