# Panda effects + sounds research: the TTO-only clips (Nine Dragons, Tempest Dance, Yin Yang Fist)

Scope: the four TTO skill clips of `wardrobe/data/panda/clips.json` (`tto: true`, group `skill`): `nineDragons` (3.9 s),
`tempestDance` (2.4 s, loop), `tempestDanceEnd` (1.3 s), `yinYangFist` (2.3 s). No BB code plays them. Research only
(office PC, 13/11/2026): this file is the only repo file written; probes and outputs are in
`checks/fx_panda_research/tto/` (git-ignored). Sources:
- TTO's pseudo-C `C:\Users\Jump\Desktop\12tails\DecompiledSource_TTO_2026-11-02\pseudo\Panda.c` (cited `Panda.c:<line>`,
  methods as `TTO1102:Method@RVA`); `fn.py` (a noise-dropping printer) -> `nine_movenext.txt`, `nine_dragon.txt`,
  `nine_king.txt`, `nine_fns.txt`, `tempest_movenext.txt`, `tempest_end_movenext.txt`, `tempest_fns.txt`,
  `tempest_glide.txt`, `yinyang_movenext.txt`, `yinyang_seal.txt`, `yinyang_fns.txt`, `dorow6.txt`, `shadowfist.txt`,
  `cc_panda_row6.txt` (TTO `CharacterControl.c`);
- capstone over `client\GameAssembly.dll` for the floats Ghidra drops (`dis.py`): `nine_movenext.asm` (the King's
  `Until(start + 1.6)`), `king_movenext.asm` (the weave's `sin(2 pi u)` / `sin(pi u)`, the slam's `rise + 1.05 + 0.3`),
  `seal_movenext.asm` (the Yang `Until(sealStart + 1.2)`, the shakes 0.55 / 0.25), `vanish.asm` (`SetActive(false)`);
- the Bible's `12t_reference\panda-skill-reference.md` "TTO Lv 100 skills" (lines 1120-1180: Nine Dragons :1126,
  Tempest Dance :1147, Yin Yang Fist :1162) and the cards `panda_nineDragons` / `panda_tempestDance` /
  `panda_yinYangFist` (icons `panda_nineDragons5` / `panda_tempestDance5` / `panda_yinYangFist5`, `bible/index.html:19322-19323`);
- TTO's bundles on this PC (`tto_assets/2026-11-09`, found by `wardrobe_fx_tto.py` itself) through
  `wardrobe_fx_tto.py panda --probe <15 names>` -> `probe.json` (`compact.py` -> `compact.txt`); `catalog.py` ->
  `catalog.txt` (every catalog address under `heroes/panda/`, against BB's rip); BB's `risingDragon_hit` through
  `wardrobe_fx.py panda --probe risingDragon_hit` -> `probe_bb.json`;
- `fk.py` (forward kinematics over `wardrobe/data/panda/rig.json` + `clips.json`) -> `fk_nine.txt` (the hands at the
  eight dragon launches);
- `cues.py` (+ `why.json`) -> `cues_paste.json`: section 7's block, built from the numbers above and parsed.

Times are seconds from the start of the clip (step) the cue is keyed by. The Panda's TTO waits are `Panda::Until(t)`
(absolute, against the coroutine's `start`), `Waits.Get(t)` (Tempest Dance's end) and a per-frame 0.3 s clock (the dance).
None of the three skills has ranks (one rank each, `PandaSkill::getSkill@0x1dbe8b0`, Bible :1124); passives on (Spirit
Fist, Shadow Fist, Combo Plus, Focused Art) change hit numbers only, never a look here (section 3).

**Released list:** all four clips (`nineDragons`, `tempestDance`, `tempestDanceEnd`, `yinYangFist`) are in it
(`wardrobe/tto_released.json:210-214`), so all get cues.

## Read this first

1. **Three skills, four clips, one sequence.** Each starts in `Panda::DoRow6Skill@0x1D520F0` (`Panda.c:40316-40590`,
   no cast bar) and plays its clip through `Panda::Row6Begin@0x1D5B700` = `PlayAnimation(clip, 0.1)` (`:41500-41570`,
   `DAT_1830031e0` = 0.1). Nine Dragons (3.9 s, `Until(start + 3.9)` then Row6End) and Yin Yang Fist (2.3 s) are single
   clips whose release falls on the clip's end: plain keys `nineDragons`, `yinYangFist`, every cue inside the clip.
   Tempest Dance is `tempestDance` looped for a flat 5 s (the page's SEQ has it, `index.html:1302`), then
   `tempestDanceEnd` for 1.3 s (0.75 + 0.55). **One SEQ fix:** `tempestDanceEnd` comes in with Row6Begin's 0.1 s fade
   (`Panda.c:23391`), so the line should read `"Tempest Dance: tempestDance*@5 tempestDanceEnd^"` (today a cut; the first
   step keeps the page's fade, Sheep / Bat decisions). Keys `tempestDance` and `tempestDanceEnd`: no other tile plays them.
2. **15 TTO-only prefabs, all probed, no arcana style** (`catalog.txt`: 94 Panda effects in TTO, 79 in BB's rip):
   6 `nineDragons_*`, 5 `tempestDance_*`, 3 `yinYangFist_*` and `yinYang` (the Yin status look on a foe,
   `CharacterControl::AddYinYangFx@0x24AF630`). 13 are cued; `tempestDance_counter` (needs an attacker) and `yinYang`
   (a status look on a foe) are left out and should still be built (`SKILL_FX`, as the Wolf's left-out ones). One BB
   prefab is reused: `risingDragon_hit` (Nine Dragons' strikes; inventory "ready"), cued as BB's rip copy (Bison decision 43).
3. **Every sound and voice is BB's own.** Voices through `Panda::Row6Voice@0x1D5C940` (`voices/<a>` or `<b>`,
   `Random.Range(0, 2)`, volume 1 for the owner): `risingDragon1|risingDragon2`, `rainStorm1|rainStorm2`,
   `waterCrane1|waterCrane2`, `finalMove` (one name). Hero sounds through `Row6Sound@0x1D5C2C0` (`sounds/<name>`):
   only the dragon bites' `punch1` / `punch2` at 0.9. Prefab AudioSources: qiStrike, risingVortex, risingDragons,
   ashuraFist, rainStorm (looping), fuujinken1, fuujinken2, raijinken_hit, waterCrane, threeSteps_hit, and BB's
   risingDragon_hit's explosion1: all in BB's rip (`probe.json` "sounds", `catalog.txt`). No TTO-only clip, no P15-style
   lookup.
4. **The 10 m target is outside every area of Tempest Dance and Yin Yang Fist** (storm 4.5 m with Spirit Fist, blast
   5.5 m, Yin 7 m, Yang 7.5 m, Bible :1153-1170): nothing lands, so their statuses (Cut, yinYang), Shadow Fist and the
   "Eye of the Storm" text never show, as in the game with a foe 10 m away. Their effects are all on the Panda or the
   ground under her. Nine Dragons does reach it: 8 bites, the King's landing and 8 `risingDragon_hit` strikes on it.
5. **Three code movers and one new emitter script** (section 6): the dragons' Bezier flight (`<NineDragon>d__336`),
   the King's 0.4 s weave (`<NineKing>d__339`), the trails hung on the hero's hands and feet (`TempestTrails`), and
   **`HelixRibbonEmitter`** (TTO.Game.dll, not decompiled: on the aura, pulse, end, charge, seal and yinYang). Plus
   three shaders the page lacks (`Particles/Standard Surface`, `ERB/Particles/Add_CenterGlow`,
   `ERB/Particles/Blend_CenterGlow`, all on `yinYangFist_burst`).
6. **No unowned followState roots** (the Mole's question 6 does not arise): the three owned spawns are the cast
   effects (`nineDragons_cast`, `yinYangFist_charge`: followPosition only) and `tempestDance_aura` (followPosition +
   followState: its command changes at 5.0 s, `cut 5`); every other spawn is a bare Instantiate with no follow flags.
7. **No camera effects cued.** `Row6Shake` (0.3 / 0.5 / 0.6 in Nine Dragons, 0.4 in the dance's end, 0.55 / 0.25 in Yin
   Yang Fist) is the player's screen (`Panda::Row6Shake@0x1D5C190`, `AddCamereShake` to Game.mPlayer only): left out
   (Bison decision 35, Cat 43).

---

## 1. Shared machinery (`TTO1102:Panda`)

- **`Row6Begin(command, mPos, tDir, clip, wrap)@0x1D5B700`** (`Panda.c:41500-41570`): actionState `attack`, the command,
  the hero at mPos turned to `mPos + vFlat(tDir)`, `PlayAnimation(clip, 0.1)`, the wrap mode, moveSpeed 0.
  `Row6Doing(command)@0x1D5BA90`: still attack + this command; `Row6End@0x1D5BB20`: standby.
- **`Row6Prefab(name)@0x1D5BFC0`** (`:41178-41235`): `GameAssets/characters/heroes/panda/effects/<name>` (cached).
  `Row6Spawn(name, pos, rot, owned)@0x1D5C380` (`:41239-41295`): owned -> `createEffect`, else `Instantiate`.
- **`Row6Voice(a, b)@0x1D5C940`** (`:41354-41419`): only when `pvoice` is on and the caster is the owner (or a teammate in
  a mission); `b == null || Random.Range(0, 2) == 0` -> a, else b; `PlayOneShot` at 1 (owner) / 0.75.
  **`Row6Sound(name, volume)@0x1D5C2C0`** (`:41421-41449`): `sounds/<name>`, `PlayOneShot` at the given volume.
- **`Row6Hand(right)@0x1D5BE80`** (`:41785-41829`): `Hand_R` / `Hand_L` (found by name, cached), else the hero.
- **Target.** `Row6Target(target, 10)@0x1D5C4B0` keeps the clicked foe when `reach^2 >= d^2` (`:40707`) and the line
  of sight is clear: the 10 m target stays the mark; `toMark = vFlat(target - hero)` (`:40522-40535`). Tempest Dance and
  Yin Yang Fist take no target (`:40364-40460`).

## 2. Per skill

### 2.1 Nine Dragons (`nineDragons`, 3.9 s; cell 452) - released

Coroutine `TTO1102:Panda.<RPC_nineDragons>d__331::MoveNext@0x1D899A0` (`Panda.c:13461-13690`):
- **0.00** (state 0): `Row6Begin('nineDragons', mPos, toMark, 'nineDragons', Once)` (`:13520`); cooldown `agiAdjust(240)`
  (`:13529-13530`); `addStatus(5 noForce, 1, 3)` on the Panda (`:13533-13536`; no look); **voice
  `risingDragon1|risingDragon2`** (`:13537`); **`nineDragons_cast` owned** at the hero, the hero's rotation (`:13550`;
  EffectControl 2.0 + 0.4, followPosition; its AudioSource qiStrike 0.8); `mark` = the target (`:13551-13576`).
- **0.40 + 0.11 k, k = 0-7** (`Until`, `:13587-13589`; capstone 0x1D8A002: 0.11, 0x1D89FF7: 0.4): while Row6Doing,
  `prey = NinePrey(mark)` once (`NinePrey@0x1D54BF0`: the foes in `FindAreaTarget(Panda, 10, 6)`, the mark first,
  `:13610`), dead ones dropped, dragon k at `prey[k % N]` = the target (`:13630-13636`), from `Row6Hand(~k & 1)`:
  **k even = Hand_R, k odd = Hand_L** (`:13640`), `NineDragon(step, k, hand, prey, NineFan(k))` (`:13645-13651`).
- **1.60** (state 2; `Until(start + 1.6)`, capstone 0x1D8A02F, the float Ghidra drops at `:13595`): `Row6Shake(0.3)`
  (`:13662`; left out), `NineKing(step, mark, spot)` (`:13665-13667`).
- **3.90** (`Until(start + 3.9)`, `:13668`): `Row6End` (`:13680`). The clip is 3.9 s.

**Each dragon: `<NineDragon>d__336::MoveNext@0x1D6F860` (`Panda.c:75-401`):**
- `side` = the hero's right x (k even ? +1 : -1) (`:136-154`: `cross(up, fwd)`); `end = NineAim(prey, fallback)` =
  the prey's position + 0.6 up (`NineAim@0x1D52A30`, `:42124-42200`) = **(0, 0.6, 10)**;
  `flight = clamp(1.6 |from - end| / 22, 0.35, 0.7)` (`:177-189`): from about 9.78 m, **0.7 s** (the clamp's top).
- `c1 = from + 1.4 fwd + side (1.3 + 0.15 (k % 4)) + up (2.2 + 0.2 (k % 3))` (`:190-223`); **`nineDragons_dragon`**
  bare Instantiate at the hand, `LookRotation(c1 - from)` (`:224-242`).
- Every frame while `t < t0 + flight` (`:255-310`): `end` re-aimed (the target is still), `c2 = end + 0.6 side + 2.4 up`
  (`:275-287`), `pos = Bezier(from, c1, c2, end, (t - t0) / flight)` (cubic, `Panda::Bezier@0x1D51F00`,
  `:42205-42236`), `NineFly(d, last, pos)` = `rotation = LookRotation(pos - last)` when it moved, `position = pos`
  (`NineFly@0x1D53F80`, `:42273-42335`).
- On arrival (`:312-381`): `NineFly` to `end`; **`NineVanish(d)`** (`@0x1D55070`, `:42339-42421`): its `Body`,
  `HeadGlow`, `HeadHalo` children `SetActive(false)` (`vanish.asm` 0x1D5520B: `xor edx, edx`), every ParticleSystem
  `Stop(true, StopEmitting)`, `Destroy(d, 0.5)` (the Trail keeps fading); **`nineDragons_bite`** at
  `getSpawnPos(end)` = the target's feet **(0, 0, 10)**, identity (`:316-361`); `Row6Sound(k even ? punch1 : punch2,
  0.9)` for the owner (0.6 others), at most one per 0.06 s (`mBiteSoundAt`, `:362-374`: the bites are 0.11 s apart, all
  play); `NineBite` (the owner's hit, `:376-381`; no effect).
- The hands (`fk.py` on the `nineDragons` clip, Unity space, x right / y up / d ahead; +-3 cm, the 0.1 s fade-in
  ignored):

  | k | launch | hand | from (x, y, d) | c1 | spawn rot | bite (arrival) |
  |---|---|---|---|---|---|---|
  | 0 | 0.40 | R | (0.101, 0.371, 0.225) | (1.401, 2.571, 1.625) | (-49.03, 42.88, 0) | 1.10 |
  | 1 | 0.51 | L | (-0.042, 0.346, 0.215) | (-1.492, 2.746, 1.615) | (-49.98, -46.01, 0) | 1.21 |
  | 2 | 0.62 | R | (0.109, 0.368, 0.209) | (1.709, 2.968, 1.609) | (-50.73, 48.81, 0) | 1.32 |
  | 3 | 0.73 | L | (-0.039, 0.377, 0.212) | (-1.789, 2.577, 1.612) | (-44.47, -51.34, 0) | 1.43 |
  | 4 | 0.84 | R | (0.106, 0.352, 0.222) | (1.406, 2.752, 1.622) | (-51.48, 42.88, 0) | 1.54 |
  | 5 | 0.95 | L | (-0.047, 0.328, 0.207) | (-1.497, 2.928, 1.607) | (-52.22, -46.01, 0) | 1.65 |
  | 6 | 1.06 | R | (0.106, 0.378, 0.216) | (1.706, 2.578, 1.616) | (-45.98, 48.81, 0) | 1.76 |
  | 7 | 1.17 | L | (-0.034, 0.393, 0.216) | (-1.784, 2.793, 1.616) | (-46.96, -51.34, 0) | 1.87 |

  c2 = (+-0.6, 3.0, 10) by k's side. The Bible's "0.75 + 0.11 k for a target within 4.8 m, up to 0.35 s later for far
  ones" (:1132) gives the same: 1.10 + 0.11 k at 10 m.

**The Dragon King: `<NineKing>d__339::MoveNext@0x1D701C0` (`Panda.c:405-765`), from 1.60:**
- `from = hero + 0.4 fwd + 0.7 up` = **(0, 0.7, 0.4)** (`:465-475`); `end = NineMark(mark, spot)` = `getSpawnPos(the
  mark's position)` = **(0, 0, 10)** (`NineMark@0x1D549C0`, `:42816-42846`); `aim = end + 0.8 up` (`:487-495`);
  `dir = normalize(vFlat(aim - from))` = forward, `side = cross(up, dir)` = right (`:497-541`); **`nineDragons_king`**
  bare Instantiate at `from`, `LookRotation(dir)` (`:549-557`; EffectControl 1.2 + 0.5; AudioSource risingDragons 1.0;
  its Body Animation `pandaRow6_dragonSwim` looped, 0.6 s).
- The flight, every frame for 0.4 s (`:625-693`), u = (t - t0) / 0.4: `pos = from + (aim - from) clamp01(u) + side x
  0.9 sin(2 pi u)(1 - u) + up x 0.6 sin(pi u)` (`king_movenext.asm` 0x1D7086D `x 6.28319`, 0x1D7088F `x 3.14159`,
  0x1D708A1 `x 0.9`; the up term `x 0.6` at `:674`), turned along its motion (NineFly).
- **2.00** (arrival, `:697-741`): NineFly to `aim`, NineVanish (Destroy 0.5 later); **`nineDragons_kingRise`** at `end`,
  `LookRotation(dir)` (`:720-727`); `Row6Shake(0.5)` (`:728`; left out); `NineCharge` (the dash hit) and
  `NineKingLock` (the `lock` status, no look) for the owner (`:735-738`); `rise = now`.
- **2.00 + 0.15 k, k = 0-7** (`Until(rise + 0.15 k)`, `:743-750`): `NineKingHit(end)` (`@0x1D54120`, `:614-619`):
  on each struck foe (3 m circle at `end`: the target), `RPC_risingDragon_hit(foe + 1 up, fwd)` locally
  (`:42692-42715`): **`risingDragon_hit`** (`panda/effects/risingDragon_hit`, BB's prefab) at **(0, 1, 10)**, identity
  (`Panda::RPC_risingDragon_hit@0x1D58980`, `:38121-38212`). The RPC sent to others uses +1.5 up (`:42737-42745`): not
  the owner's.
- **3.35** (`Until(rise + 1.05 + 0.3)`, `king_movenext.asm` 0x1D70BF5 / 0x1D70BFD): **`nineDragons_fall`** at `end`,
  `LookRotation(dir)` (`:588-595`); `Row6Shake(0.6)` (`:596`; left out); `NineFall` (the slam hit; "Nine Dragons!" on
  the caster's screen, `:43274`: left out) (`:603`).

**Timeline** (cast-relative):

| s | what |
|---|---|
| 0 | voice risingDragon1 / 2, nineDragons_cast (qiStrike) |
| 0.40 ... 1.17 | 8 dragons from the hands, R / L in turn (risingVortex 0.35 each) |
| 1.10 ... 1.87 | 8 bites at the target's feet, punch1 / punch2 |
| 1.60 | the King leaves (risingDragons) |
| 2.00 | the King lands: kingRise; the strikes start |
| 2.00 ... 3.05 | 8 risingDragon_hit at the target + 1 up (explosion1) |
| 3.35 | nineDragons_fall (ashuraFist) |
| 3.90 | standby |

### 2.2 Tempest Dance (`tempestDance` looped 5 s > `tempestDanceEnd` 1.3 s; cell 453) - released

**The dance: `<RPC_tempestDance>d__346::MoveNext@0x1D9B1B0` (`Panda.c:23122-23315`):**
- **0.00** (state 0): `Row6Begin('tempestDance', ..., 'tempestDance', Loop)` (`:23164`); `addTimeOut(7.3)` (`:23171`);
  **voice `rainStorm1|rainStorm2`** (`:23172`); **`tempestDance_aura` owned** at the hero, the hero's rotation
  (`:23188`; EffectControl 5.3 + 0.4, followPosition, **followState**; AudioSource rainStorm 0.6, **looping**);
  **`TempestTrails(true)`** (`:23189`); the owner: status `tempestDance` (309) 6 s (`:23227-23229`; no look:
  TTO's CharacterControl has a Row6 look only for `yinYang`, `cc_panda_row6.txt`); `next = start + 0.3` (`:23231`).
- **`TempestTrails(on)@0x1D5F010`** (`Panda.c:43469-43705`): off first (each listed TrailRenderer `emitting = false`,
  `Destroy(its GameObject, trail.time + 0.05)`, `:43521-43555`); on: for each child of `tempestDance_trails`, the hero's
  bone of the same name (`findChildObject`), `Instantiate(child, bone)`, localPosition 0, localRotation identity,
  `TrailRenderer.Clear()` (`:43558-43691`). The children: **Hand_R, Hand_L (m_Time 0.3), Foot_R, Foot_L (0.38)**, all
  `tto_Line_DoubleEdge1` (`probe.json`); the four bones are in `data/panda/rig.json`.
- Every frame while Row6Doing (`:23240-23291`): the owner at 5 s calls `TempestFinish` and the coroutine ends
  (`:23253-23256`), else `TempestSteer` (the move keys: none on the page, so the Panda stays put); each 0.3 s tick n
  (`next += 0.3`): **n even spawns `tempestDance_pulse`** at the hero, the hero's rotation, bare Instantiate
  (`:23260-23281`; EffectControl 0.4 + 0.1); `TempestStorm` for the owner (`:23284-23285`; r 4.5 m: misses the target).
  Ticks at 0.3 ... 4.8 (16); pulses at **0.3, 0.9, 1.5, 2.1, 2.7, 3.3, 3.9, 4.5** (8).
- **5.00**: `TempestFinish@0x1D5DBC0` (`Panda.c:44677-44760`): `StandbyEvent`, `landed = min(landed, 30)`,
  `RPC_tempestDanceEnd` started (its first part runs at once). The aura's command changes (tempestDance ->
  tempestDanceEnd): its followState sends it to its 0.4 s after-life (`EffectControl.cs:194-250`): **cut 5**. The trails
  are NOT switched off here (the coroutine returns before its own `TempestTrails(false)` at `:23298`, which runs only
  when interrupted).

**The end: `<RPC_tempestDanceEnd>d__355::MoveNext@0x1D9AD20` (`Panda.c:23333-23486`):**
- **0.00**: `Row6Begin('tempestDanceEnd', ..., 'tempestDanceEnd', Once)` (`:23391`: **fade 0.1**); the owner does not
  glide (`TempestGlide` is the other clients' catch-up when 2 m off, `:23376-23402`); cooldown `agiAdjust(75)`, the
  status removed (`:23406-23413`); **voice `waterCrane1|waterCrane2`** (`:23415`); `Waits.Get(0.75)` (`:23419`).
- **0.75** (state 1): **`TempestTrails(false)`** (`:23442`): the trails stop emitting and go 0.35 / 0.43 s later;
  while Row6Doing: **`tempestDance_end`** at the hero, the hero's rotation, bare Instantiate (`:23468`; EffectControl
  1.0 + 0.4; AudioSource fuujinken2 1.0); `Row6Shake(0.4)` (`:23470`; left out); `TempestEye(landed)` (`:23473`; the
  5.5 m blast misses the target; "Eye of the Storm x N!" needs 20 landed). `Waits.Get(0.55)` (`:23449`).
- **1.30**: `Row6End` (`:23435`). The clip is 1.3 s.

**Timeline** (cast-relative; step 2 from 5.0):

| s | what |
|---|---|
| 0 | voice rainStorm1 / 2, aura (rainStorm loop), trails on hands and feet |
| 0.3, 0.9 ... 4.5 | 8 tempestDance_pulse gusts |
| 5.0 | tempestDanceEnd (fade 0.1), voice waterCrane1 / 2; the aura's after-life |
| 5.75 | tempestDance_end (fuujinken2); the trails stop |
| 6.18 | the last trail gone |
| 6.3 | standby |

### 2.3 Yin Yang Fist (`yinYangFist`, 2.3 s; cell 454) - released

Coroutine `<RPC_yinYangFist>d__357::MoveNext@0x1DCDC50` (`Panda.c:29191-29300`):
- **0.00** (state 0): `Row6Begin('yinYangFist', ..., 'yinYangFist', Once)` (`:29224`); cooldown `agiAdjust(120)`
  (`:29232-29233`); **voice `finalMove`** (`:29234`; one name); **`yinYangFist_charge` owned** at the hero, the hero's
  rotation (`:29248`; EffectControl 0.62 + 0.15, followPosition; AudioSource qiStrike 0.8); `Until(start + 0.55)`.
- **0.55** (state 1, while Row6Doing): `YinYangSeal(gen, hero position)` (`:29279-29286`):
  `<YinYangSeal>d__358::MoveNext@0x1DCE740` (`Panda.c:29553-29682`): `seal = getSpawnPos(at)` (the ground under her;
  `at` if none, `:29583-29600`), **`yinYangFist_seal`** there, identity, bare Instantiate (`:29613`; EffectControl
  1.4 + 0.3; AudioSource fuujinken1 0.9); `Row6Shake(0.55)` (`seal_movenext.asm` 0x1DCE82E; left out); Yin pulses
  `SealYin` at sealStart + 0.4 k, k = 0-2 (`:29619-29650`: 0.55, 0.95, 1.35; the owner's hits, r 7 m: miss).
- **1.75** (`Until(sealStart + 1.2)`, `seal_movenext.asm` 0x1DCEAAF): **`yinYangFist_burst`** at the seal, identity
  (`:29667`; EffectControl 1.6 + 2.8; AudioSource raijinken_hit 1.0); `Row6Shake(0.25)` (0x1DCEA19; left out);
  `SealYang` (r 7.5 m: misses).
- **2.30** (`Until(start + 2.3)`, `:29287`): `Row6End` (`:29264-29265`). The clip is 2.3 s.

## 3. What is left out (only "on an enemy's body" / "needs a foe in reach" / the player's screen)

- Nine Dragons: the `noForce` status on the Panda (no look in BB's or TTO's code), the `lock` status on the target
  (a status on a foe: Sheep decision 4, Cat 44), the "Nine Dragons!" text, the three camera shakes. SP and Combo Plus
  stacks (`ComboPlus`: `comboPlus` status = `deltaAtk` only, BB `CharacterControl.cs:35473`): no look.
- Tempest Dance: `tempestDance_counter` (needs an attacker's hit to evade, `RPC_tempestCounter@0x1D59F30`; built, not
  cued); the storm's `cut` status and Shadow Fist on hit foes (none in 4.5 m); the blast (none in 5.5 m) and its text;
  the shake; the 309 status (no look).
- Yin Yang Fist: the `yinYang` status look on a foe (`AddYinYangFx@0x24AF630`, `tto/yinYang`; built, not cued; none in
  7 m anyway), the two shakes.
- The other clients' paths (`TempestFollow`, `TempestGlide`, the +1.5 up RPC of the strike hit).

Everything else is cued: Nine Dragons' bites and strikes go to the target 10 m ahead (the rule).

## 4. Sounds and voices

| t (s, in the cue's key) | kind | name | where | in BB's rip |
|---|---|---|---|---|
| nineDragons 0 | voice | risingDragon1 \| risingDragon2 | Row6Voice (`:13537`) | voices/ |
| own | AudioSource | qiStrike 0.8 (cast), risingVortex 0.35 (each dragon), risingDragons 1.0 (King), ashuraFist 1.0 (fall), explosion1 0.5 (risingDragon_hit) | prefabs | sounds/ (explosion1: BB's prefab) |
| nineDragons 1.10 ... 1.87 | sound | punch1 / punch2 0.9 | Row6Sound (`:362-374`) | sounds/ |
| tempestDance 0 | voice | rainStorm1 \| rainStorm2 | `:23172` | voices/ |
| own | AudioSource | rainStorm 0.6 **loop** (aura, until it is destroyed: 5.0 + 0.4) | prefab | sounds/ |
| tempestDanceEnd 0 | voice | waterCrane1 \| waterCrane2 | `:23415` | voices/ |
| own | AudioSource | fuujinken2 1.0 (end) | prefab | sounds/ |
| yinYangFist 0 | voice | finalMove | `:29234` | voices/ |
| own | AudioSource | qiStrike 0.8 (charge), fuujinken1 0.9 (seal), raijinken_hit 1.0 (burst) | prefabs | sounds/ |
| (not cued) | AudioSource | waterCrane, threeSteps_hit (counter) | prefab | sounds/ |

## 5. Probed (office PC, TTO's 2026-11-09 bundles; `probe.json`, `compact.txt`)

All 15 export with no warning (`probe.err` empty). Animations export with their clips (the exporter's `animation()`,
Mole decision 56): `pandaRow6_dragonSwim` (0.6 s, loop, 6 tracks) on the dragon's and King's Body, `root` (2.0 s, 7
tracks) on kingRise's `Panda_flyingDragon`, `root` (0.43 s) on the counter's `mysticSage_hit`. Materials (45): add 11,
addsoft 19, alpha 2, multiply 1, `Particles/Standard Unlit` 4 (built: tto_sheep.js), **`Particles/Standard Surface` 4,
`ERB/Particles/Add_CenterGlow` 3, `ERB/Particles/Blend_CenterGlow` 1** (not built: P5). 43 textures.

| prefab | EffectControl (life + after) | parts | own sound | needs |
|---|---|---|---|---|
| nineDragons_cast | 2.0 + 0.4, followPosition | 6 Shuriken (GoldCircle, Rune, flare, star, ring, shock, glow), GroundHug Kick | qiStrike 0.8 | - |
| nineDragons_dragon | 1.2 + 0.3 | Body (Animation dragonSwim, x 2.1) + SkinnedMesh `flyingDragon_tri` (dragonGold, 7 bones), HeadGlow / HeadHalo ImageEmitters, TrailRendererModern (0.3 s), Shuriken Sparks | risingVortex 0.35 | P1 |
| nineDragons_bite | 0.5 + 0.35 | 6 Shuriken (Rays, Hit, Glow, Sparks, Flash, ShockWave), RingEmitter Snap | - | - |
| nineDragons_king | 1.2 + 0.5 | as the dragon at x 6.5 (dragonFire), Trail 0.45 s | risingDragons 1.0 | P2 |
| nineDragons_kingRise | 2.0 + 0.6 | Panda_flyingDragon (Animation root 2.0 s, SkinnedMesh), RingEmitter, 4 GroundHugs, LineEmitter, 5 Shuriken | - | - |
| nineDragons_fall | 1.6 + 0.6 | 4 GroundHugs, LineEmitter, 7 Shuriken | ashuraFist 1.0 | - |
| tempestDance_aura | 5.3 + 0.4, followPosition, **followState** | 2 HelixRibbonEmitters (Inner, Outer), GroundHug Floor (repeatForever), Shuriken Motes | rainStorm 0.6 loop | P3 |
| tempestDance_trails | none (the code destroys the trails) | 4 TrailRendererModern children named after bones | - | P4 |
| tempestDance_pulse | 0.4 + 0.1 | HelixRibbonEmitter Gust | - | P3 |
| tempestDance_counter | 0.7 + 0.3 | ImageEmitters, mysticSage_hit (Animation, StaticMesh, AlphaTimer), LineEmitter | waterCrane 1.0, threeSteps_hit 1.0 | not cued |
| tempestDance_end | 1.0 + 0.4 | 2 HelixRibbonEmitters (Burst, Flung), GroundHug Floor | fuujinken2 1.0 | P3 |
| yinYangFist_charge | 0.62 + 0.15, followPosition | 2 ImageEmitters (Taiji, Enso), HelixRibbonEmitter Qi | qiStrike 0.8 | P3 |
| yinYangFist_seal | 1.4 + 0.3 | 4 GroundHugs (Open, Seal 7 m, Enso, Trigrams), 2 HelixRibbonEmitters (Pull, Closing) | fuujinken1 0.9 | P3 |
| yinYangFist_burst | 1.6 + 2.8 | 63 nodes: YinYang / Bamboo / Expl / GroundWave / DustRing / InkPlume / CreamPlume / Wisps / LeafBurst / LeafFall Shuriken; 5 Strikes (each: Glow / Core / Restrike / 2 Branch LineRenderers + autoBolt ChameleonLightning from 10 m up, delays 0-0.33; Flash + Light (disabled) + Sparks + Dust); GroundHug Shock | raijinken_hit 1.0 | P5 |
| yinYang | none (the status removes it) | GroundHug Symbol (repeatForever), HelixRibbonEmitter Pull | - | not cued (P3) |

BB's copy (`probe_bb.json`): `risingDragon_hit` = a legacy EllipsoidParticleEmitter + ParticleAnimator + AudioSource
explosion1 0.5 (inventory `plans/fx_inventory.md:472`: ready).

## 6. Parts the page lacks (effect: part)

Home `wardrobe/fxparts/tto_panda.js` (new); numbers above. Every part is cued anyway (the rule).

| # | Part | Effects | What it does (source) |
|---|---|---|---|
| P1 | `Panda.NineDragon` (CODE_MOVERS, the coroutine as the root's first component) | nineDragons_dragon | From the spawn spot along `Bezier(from, c1, c2, to, u)`, u = age / `flight`, turned along its motion each frame (NineFly); at u = 1: at `to`, then NineVanish: `Body`, `HeadGlow`, `HeadHalo` off, every Shuriken stops emitting, the Trail keeps fading; the cue's `kill` (flight + 0.5) is the Destroy (`Panda.c:75-401`, `:42273-42421`). Cue options `c1`, `c2`, `to` ([x, y, d], hero-relative), `flight`. |
| P2 | `Panda.NineKing` (CODE_MOVERS) | nineDragons_king | 0.4 s (`flight`) from the spawn to `aim` with the weave `+ right x 0.9 sin(2 pi u)(1 - u) + up x 0.6 sin(pi u)`, turned along its motion; then NineVanish as P1, `kill` 0.9 (`Panda.c:625-702`, `king_movenext.asm`). Cue options `aim`, `flight`. |
| P3 | **`HelixRibbonEmitter`** (TTO.Game.dll TypeDefIndex 411, `dump.cs:11764-11809`; **not decompiled**: Awake 0x2264A90, LateUpdate 0x2264EF0, Ends 0x2264E00, Rebuild 0x2265090, .ctor 0x2265660, `methods.tsv:3306-3311`) | tempestDance_aura, _pulse, _end, yinYangFist_charge, _seal, yinYang | Fields: ribbons, turns, height, radiusBottom / Top, widthBottom / Top, segments, spin (deg/s), scroll, uvTile, wobble, wobbleSpeed, Life, Delay, fadeIn, fadeOut, repeatForever, radiusScaleStart / End, colorBottom / Top, endFade; a rebuilt Mesh on the node's MeshRenderer (verts / uvs / cols) each LateUpdate from `Rebuild(t, alpha)`. The parts stage reads the four methods with capstone (as KaiserArsenalPod's numbers were, Mole P11). |
| P4 | `Panda.TempestTrails`: cue option `childBones` (each child of the root hung under the hero's bone of its own name, localPosition 0, localRotation identity, as a cue's `bone` per child) + **`stop` for TrailRendererModern** (`emitting = false`: no new points, the old ones fade over m_Time) | tempestDance_trails | `Panda.c:43469-43705` (on), `:43521-43555` (off: emitting false, Destroy after m_Time + 0.05). Today `stop` stops Shuriken systems only (`index.html:4297`) and tto_sheep.js's trail has no `stop()`. |
| P5 | Shaders `Particles/Standard Surface` (Unity's, lit particles: bamboo, smokePuff, smokeWisp, bambooLeaf), `ERB/Particles/Add_CenterGlow` (Add_noise, Mask13, Circle42: scrolling main + noise UV, `_Emission`, centre glow), `ERB/Particles/Blend_CenterGlow` (YinYang) | yinYangFist_burst | From their props (`probe.json` materials; the ERB pair's compiled programs in the bundle, as TTO/ChameleonSpirit's were read, Chameleon P3). |
| P6 | `SKILL_FX["panda"]` in `wardrobe_fx_tto.py` (the 15 prefabs: the 13 cued + `tempestDance_counter`, `yinYang`) and CODE_MOVERS `nineDragons_dragon` -> `Panda.NineDragon`, `nineDragons_king` -> `Panda.NineKing` | all | then `wardrobe_fx_tto.py panda` and `wardrobe_fx.py panda` (the BB effects, voices, sounds). |
| P7 | SEQ: `tempestDanceEnd^` | the Tempest Dance tile | `"Tempest Dance: tempestDance*@5 tempestDanceEnd^"` (`index.html:1302`; Row6Begin's 0.1 s fade, `Panda.c:23391`). |

Parts that already exist and are used here: EffectControl, ImageEmitter, RingEmitter, LineEmitter, GroundHugEmitter
(groundhug.js), Shuriken, Animation + SkinnedMeshRenderer + StaticMesh (mesh.js), AlphaTimer, Light (light.js; the
burst's are disabled), LineRenderer + TrailRendererModern (tto_sheep.js), ChameleonLightning with `autoBolt` and `delay`
(tto_chameleon.js, loaded for every class: `FX_PART_FILES`), legacy particles (risingDragon_hit), `Particles/Standard
Unlit` (tto_sheep.js), a followState `cut` at the step change (Chameleon P8).

## 7. The cue entries (ready to paste into `wardrobe/fx_cues/panda.json`)

`checks/fx_panda_research/tto/cues_paste.json` (parsed by `cues.py`): 4 keys, **54 cues** (nineDragons 37, tempestDance
11, tempestDanceEnd 2, yinYangFist 4). The part options (`c1`, `c2`, `flight`, `aim`, `childBones`) are passed through
to the parts (`cueOf`, "every other option is passed on as it is, for the parts"); `to` is the existing cue option;
`stop` exists but needs P4 for the trails. Nothing here needs a roll or a pick beyond the voices'. The file is `{}` today,
so these four keys go in beside the BB researchers' entries.

```json
{
  "nineDragons": {
    "why": "TTO1102:Panda.<RPC_nineDragons>d__331::MoveNext@0x1D899A0 (pseudo/Panda.c:13461-13690; plans/fx_panda/tto.md 2.1), the 10 m target clicked (Panda::Row6Target@0x1D5C4B0 keeps it: reach^2 < d^2 rejects, :40707; DoRow6Skill@0x1D520F0 toMark = vFlat(target - hero), :40522-40535): Row6Begin('nineDragons', clip nineDragons, Once; PlayAnimation fade 0.1, Panda::Row6Begin@0x1D5B700 :41500-41570); cooldown, noForce Lv 1 3 s on the Panda (no look); Row6Voice risingDragon1 / risingDragon2 (Random.Range(0, 2), voices/, Panda::Row6Voice@0x1D5C940); nineDragons_cast owned at the hero, its rotation (:13550; followPosition, its own AudioSource qiStrike 0.8). Dragons k = 0-7 at Until(start + 0.4 + 0.11 k) (:13587-13589), prey[k % N] = the target (:13610-13636), from Row6Hand(k even) = Hand_R, odd Hand_L (:13640; Panda::Row6Hand@0x1D5BE80; the hand spots: checks/fx_panda_research/tto/fk.py on the nineDragons clip, +-3 cm): <NineDragon>d__336@0x1D6F860 (Panda.c:75-401): end = NineAim (the target + 0.6 up, Panda::NineAim@0x1D52A30), flight = clamp(1.6 |from - end| / 22, 0.35, 0.7) = 0.7 (:177-189), c1 = from + 1.4 fwd + side (1.3 + 0.15 (k % 4)) + up (2.2 + 0.2 (k % 3)), side = +-right by k's parity (:140-223), nineDragons_dragon bare Instantiate at the hand, LookRotation(c1 - from) (:224-241); each frame Bezier(from, c1, end + 0.6 side + 2.4 up, end) (:255-310, Panda::Bezier@0x1D51F00) faced along its motion (NineFly@0x1D53F80); on arrival NineVanish@0x1D55070 (Body / HeadGlow / HeadHalo SetActive(false), its ParticleSystems Stop, Destroy 0.5: :42339-42421) and nineDragons_bite at getSpawnPos(end) = the target's feet, identity (:316-361), Row6Sound punch1 (k even) / punch2 at 0.9 (the owner's; 0.6 others; at most one per 0.06 s, :362-374). Until(start + 1.6) (capstone 0x1D8A02F): Row6Shake 0.3 (the player's camera: left out) and <NineKing>d__339@0x1D701C0 (Panda.c:405-765): nineDragons_king at hero + 0.4 fwd + 0.7 up, LookRotation(flat dir) (:465-557), 0.4 s to aim = the target's ground + 0.8 up with a weave side x 0.9 sin(2 pi u)(1 - u) and up x 0.6 sin(pi u) (:625-693; capstone 0x1D7086D, 0x1D7088F), NineVanish; at 2.0 nineDragons_kingRise at the landing point, LookRotation(dir) (:720-727), shake 0.5 (left out), NineCharge + NineKingLock (the lock status: no look); 8 strikes Until(rise + 0.15 k) (:743-750): NineKingHit@0x1D54120 on each struck foe -> RPC_risingDragon_hit(foe + 1 up, fwd)@0x1D58980: risingDragon_hit (BB's prefab, cued as the rip's copy, Bison decision 43) at the foe + 1 up, identity (:42692-42715, :38199-38212); Until(rise + 1.05 + 0.3) (capstone 0x1D70BF5-0x1D70BFD): nineDragons_fall at the landing point, LookRotation(dir) (:588-595), shake 0.6 (left out), NineFall (its 'Nine Dragons!' text is the player's screen: left out); Until(start + 3.9): Row6End (:13668-13680)",
    "cues": [
    [0, "voice", "risingDragon1|risingDragon2"],
    [0, "fx", "tto/nineDragons_cast"],
    [0.4, "fx", "tto/nineDragons_dragon", {"x": 0.101, "y": 0.371, "d": 0.225, "rot": [-49.03, 42.88, 0], "c1": [1.401, 2.571, 1.625], "c2": [0.6, 3.0, 10.0], "to": [0.0, 0.6, 10.0], "flight": 0.7, "kill": 1.2}],
    [0.51, "fx", "tto/nineDragons_dragon", {"x": -0.042, "y": 0.346, "d": 0.215, "rot": [-49.98, -46.01, 0], "c1": [-1.492, 2.746, 1.615], "c2": [-0.6, 3.0, 10.0], "to": [0.0, 0.6, 10.0], "flight": 0.7, "kill": 1.2}],
    [0.62, "fx", "tto/nineDragons_dragon", {"x": 0.109, "y": 0.368, "d": 0.209, "rot": [-50.73, 48.81, 0], "c1": [1.709, 2.968, 1.609], "c2": [0.6, 3.0, 10.0], "to": [0.0, 0.6, 10.0], "flight": 0.7, "kill": 1.2}],
    [0.73, "fx", "tto/nineDragons_dragon", {"x": -0.039, "y": 0.377, "d": 0.212, "rot": [-44.47, -51.34, 0], "c1": [-1.789, 2.577, 1.612], "c2": [-0.6, 3.0, 10.0], "to": [0.0, 0.6, 10.0], "flight": 0.7, "kill": 1.2}],
    [0.84, "fx", "tto/nineDragons_dragon", {"x": 0.106, "y": 0.352, "d": 0.222, "rot": [-51.48, 42.88, 0], "c1": [1.406, 2.752, 1.622], "c2": [0.6, 3.0, 10.0], "to": [0.0, 0.6, 10.0], "flight": 0.7, "kill": 1.2}],
    [0.95, "fx", "tto/nineDragons_dragon", {"x": -0.047, "y": 0.328, "d": 0.207, "rot": [-52.22, -46.01, 0], "c1": [-1.497, 2.928, 1.607], "c2": [-0.6, 3.0, 10.0], "to": [0.0, 0.6, 10.0], "flight": 0.7, "kill": 1.2}],
    [1.06, "fx", "tto/nineDragons_dragon", {"x": 0.106, "y": 0.378, "d": 0.216, "rot": [-45.98, 48.81, 0], "c1": [1.706, 2.578, 1.616], "c2": [0.6, 3.0, 10.0], "to": [0.0, 0.6, 10.0], "flight": 0.7, "kill": 1.2}],
    [1.1, "fx", "tto/nineDragons_bite", 10],
    [1.1, "sound", "punch1", {"vol": 0.9}],
    [1.17, "fx", "tto/nineDragons_dragon", {"x": -0.034, "y": 0.393, "d": 0.216, "rot": [-46.96, -51.34, 0], "c1": [-1.784, 2.793, 1.616], "c2": [-0.6, 3.0, 10.0], "to": [0.0, 0.6, 10.0], "flight": 0.7, "kill": 1.2}],
    [1.21, "fx", "tto/nineDragons_bite", 10],
    [1.21, "sound", "punch2", {"vol": 0.9}],
    [1.32, "fx", "tto/nineDragons_bite", 10],
    [1.32, "sound", "punch1", {"vol": 0.9}],
    [1.43, "fx", "tto/nineDragons_bite", 10],
    [1.43, "sound", "punch2", {"vol": 0.9}],
    [1.54, "fx", "tto/nineDragons_bite", 10],
    [1.54, "sound", "punch1", {"vol": 0.9}],
    [1.6, "fx", "tto/nineDragons_king", {"y": 0.7, "d": 0.4, "aim": [0, 0.8, 10], "flight": 0.4, "kill": 0.9}],
    [1.65, "fx", "tto/nineDragons_bite", 10],
    [1.65, "sound", "punch2", {"vol": 0.9}],
    [1.76, "fx", "tto/nineDragons_bite", 10],
    [1.76, "sound", "punch1", {"vol": 0.9}],
    [1.87, "fx", "tto/nineDragons_bite", 10],
    [1.87, "sound", "punch2", {"vol": 0.9}],
    [2.0, "fx", "tto/nineDragons_kingRise", 10],
    [2.0, "fx", "risingDragon_hit", {"y": 1, "d": 10}],
    [2.15, "fx", "risingDragon_hit", {"y": 1, "d": 10}],
    [2.3, "fx", "risingDragon_hit", {"y": 1, "d": 10}],
    [2.45, "fx", "risingDragon_hit", {"y": 1, "d": 10}],
    [2.6, "fx", "risingDragon_hit", {"y": 1, "d": 10}],
    [2.75, "fx", "risingDragon_hit", {"y": 1, "d": 10}],
    [2.9, "fx", "risingDragon_hit", {"y": 1, "d": 10}],
    [3.05, "fx", "risingDragon_hit", {"y": 1, "d": 10}],
    [3.35, "fx", "tto/nineDragons_fall", 10]
    ]
  },
  "tempestDance": {
    "why": "TTO1102:Panda.<RPC_tempestDance>d__346::MoveNext@0x1D9B1B0 (pseudo/Panda.c:23122-23315; plans/fx_panda/tto.md 2.2): Row6Begin('tempestDance', clip tempestDance, Loop; fade 0.1) (:23164); addTimeOut 7.3 (:23171); Row6Voice rainStorm1 / rainStorm2 (:23172); tempestDance_aura owned at the hero, its rotation (:23188; followPosition + followState: its command changes to tempestDanceEnd at 5.0 s, so cut 5; its own looping AudioSource rainStorm 0.6); TempestTrails(true) (:23189; Panda::TempestTrails@0x1D5F010, Panda.c:43469-43705: each child of tempestDance_trails (Hand_R, Hand_L, Foot_R, Foot_L, TrailRenderers 0.3 / 0.3 / 0.38 / 0.38 s) instantiated under the hero's bone of its name, localPosition 0, localRotation identity, Clear(); off = emitting false, Destroy(trail.time + 0.05)); status tempestDance (309) 6 s on the Panda (no look: CharacterControl has none for it); the 0.3 s clock from start + 0.3 (:23231): each tick (pulse n = 0, 1, ...) with n even spawns tempestDance_pulse at the hero, its rotation, bare Instantiate (:23260-23281): 0.3, 0.9 ... 4.5 (8); TempestStorm (the owner's hits, r (3.5 + 1) m with Spirit Fist: the 10 m target is outside, so no Cut look and no Shadow Fist); at 5.0 s TempestFinish@0x1D5DBC0 (:23254-23256; Panda.c:44677-44760): StandbyEvent and RPC_tempestDanceEnd (the next step). The trails are switched off only by RPC_tempestDanceEnd's TempestTrails(false) 0.75 s into the end (Panda.c:23442): stop 5.75, kill 5.75 + 0.38 + 0.05 = 6.18. Steering (TempestSteer) has no input on the page: the Panda stays put",
    "cues": [
    [0, "voice", "rainStorm1|rainStorm2"],
    [0, "fx", "tto/tempestDance_aura", {"cut": 5}],
    [0, "fx", "tto/tempestDance_trails", {"childBones": true, "stop": 5.75, "kill": 6.18}],
    [0.3, "fx", "tto/tempestDance_pulse"],
    [0.9, "fx", "tto/tempestDance_pulse"],
    [1.5, "fx", "tto/tempestDance_pulse"],
    [2.1, "fx", "tto/tempestDance_pulse"],
    [2.7, "fx", "tto/tempestDance_pulse"],
    [3.3, "fx", "tto/tempestDance_pulse"],
    [3.9, "fx", "tto/tempestDance_pulse"],
    [4.5, "fx", "tto/tempestDance_pulse"]
    ]
  },
  "tempestDanceEnd": {
    "why": "TTO1102:Panda.<RPC_tempestDanceEnd>d__355::MoveNext@0x1D9AD20 (pseudo/Panda.c:23333-23486; plans/fx_panda/tto.md 2.2), started by TempestFinish at 5.0 s: Row6Begin('tempestDanceEnd', clip tempestDanceEnd, Once; fade 0.1) (:23391); cooldown agiAdjust(75), the status removed (:23406-23413); Row6Voice waterCrane1 / waterCrane2 (:23415); Waits.Get(0.75) (:23419): TempestTrails(false) (:23442: the trails' stop, on the tempestDance cue), tempestDance_end at the hero, its rotation, bare Instantiate (:23468; its own AudioSource fuujinken2 1.0), Row6Shake 0.4 (the player's camera: left out), TempestEye (the owner's 5.5 m blast: the 10 m target is outside; its 'Eye of the Storm x N!' text needs 20 hits landed); Waits.Get(0.55) (:23449): Row6End at 1.3 s, the clip's length (:23435). The owner never glides (TempestGlide is the other clients' catch-up, :23376-23402)",
    "cues": [
    [0, "voice", "waterCrane1|waterCrane2"],
    [0.75, "fx", "tto/tempestDance_end"]
    ]
  },
  "yinYangFist": {
    "why": "TTO1102:Panda.<RPC_yinYangFist>d__357::MoveNext@0x1DCDC50 (pseudo/Panda.c:29191-29300; plans/fx_panda/tto.md 2.3): Row6Begin('yinYangFist', clip yinYangFist, Once; fade 0.1) (:29224); cooldown agiAdjust(120) (:29232-29233); Row6Voice finalMove (one name, :29234); yinYangFist_charge owned at the hero, its rotation (:29248; followPosition, its own AudioSource qiStrike 0.8); Until(start + 0.55) (:29249): <YinYangSeal>d__358@0x1DCE740 (Panda.c:29553-29682) at the hero's position: the seal at getSpawnPos (the ground under her), yinYangFist_seal there, identity, bare Instantiate (:29583-29613; its own AudioSource fuujinken1 0.9), Row6Shake 0.55 (capstone 0x1DCE82E; the player's camera: left out); SealYin at sealStart + 0.4 k, k = 0-2 (:29619-29650; r 7 m: the 10 m target is outside, so no yinYang status look on it); Until(sealStart + 1.2) (capstone 0x1DCEAAF): yinYangFist_burst at the seal, identity (:29667; its own AudioSource raijinken_hit 1.0), Row6Shake 0.25 (left out), SealYang (r 7.5 m: outside); Until(start + 2.3): Row6End (:29287, :29264-29265)",
    "cues": [
    [0, "voice", "finalMove"],
    [0, "fx", "tto/yinYangFist_charge"],
    [0.55, "fx", "tto/yinYangFist_seal"],
    [1.75, "fx", "tto/yinYangFist_burst"]
    ]
  }
}
```

The dragon and King cues need P1 / P2 to fly; without them they sit at their spawn spot until `kill` (the bites and
strikes still play on time). The trails cue needs P4 (`childBones`; without it the four trails hang at the hero's feet
and never move, so nothing is drawn).

## 8. Open questions (each with my recommended answer)

1. **The dragons' launch spots: cued numbers or the live bone?** The game reads `Hand_R` / `Hand_L` at each launch.
   Recommend **the cued numbers** from `fk.py` (the Sheep's mouth / hand spots did the same, `plans/fx_sheep/tto.md:77`);
   +-3 cm, and the clip's 0.1 s fade-in from idle is ignored (all launches are 0.4 s or later). Alternative: a cue option
   `fromBone` read at the spawn (exact under any outfit pose change, but no such option exists).
2. **Hits and bites: cued or part-made?** Recommend **cued** at the code's fixed times (section 7; Mole question 5): the
   flight is exactly 0.7 s at 10 m, so P1 only flies and vanishes; the bites, the punch sounds and the strikes stay
   visible in the cue file.
3. **`risingDragon_hit` from BB's rip or TTO's bundle?** TTO loads `panda/effects/risingDragon_hit` from its own
   addressables (`:38145`). Recommend **BB's rip copy** (Bison decision 43; inventory "ready").
4. **The trails: a Panda part or a generic option?** Recommend the **generic cue option `childBones`** (any prefab whose
   children are named after bones; P4) plus `stop()` on TrailRendererModern; a `Panda.TempestTrails` CODE_MOVER is the
   alternative if the parts stage prefers keeping cue options few.
5. **The dance's length:** the code's flat 5 s (not CHA-scaled; the 7.3 s lock is the cooldown's) and the end's 1.3 s, as
   today's SEQ; only the 0.1 s fade into the end is new (P7). Recommend as written.
6. **Nothing lands for Tempest Dance and Yin Yang Fist** (the target is 10 m away, outside 4.5 / 5.5 / 7 / 7.5 m).
   Recommend **as the game does with a foe at 10 m**: no Cut / yinYang looks, no counter. A closer second dummy would
   change every class's rule: not proposed.
7. **`yinYangFist_burst`'s strike flashes**: the five Strikes' bolts wait 0-0.33 s (`delay`), but their Flash / Sparks /
   Dust Shuriken have `startDelay` 0 (`probe.json`): all five flashes fire at once at 1.75 while the bolts fall in
   turn. Recommend **as exported** (it is the prefab), and a look in the browser check.
8. **HelixRibbonEmitter has no decompile.** Recommend the parts stage reads `Rebuild@0x2265090` / `LateUpdate@0x2264EF0` /
   `Ends@0x2264E00` with capstone (the fields are known); six of the 13 cued prefabs depend on it (P3), so build it, never
   leave those out (the user's rule).

## 9. For the Bible (offer to the user; that repo's own rules)

- **Nine Dragons:** the dragons leave the hands in turn (right on even launches, left on odd), each on a Bezier through
  a point 1.4 m ahead and 2.2-2.6 m up on its own side; at 10 m every flight is the 0.7 s cap, so the bites land at
  1.10-1.87 s; the bite effect is at the foe's feet. The King leaves 0.4 m ahead and 0.7 m up and weaves (0.9 m sideways,
  0.6 m up) on its 0.4 s flight; each of the 8 strikes shows `risingDragon_hit` on every foe it hits, 1 m above its
  feet (others see it 1.5 m up). Three camera shakes (0.3 / 0.5 / 0.6).
- **Tempest Dance:** a gust every other storm tick (8 in the 5 s, at 0.3 + 0.6 n); trails on both hands and feet that stop
  only 0.75 s into the end, with the closing burst; the aura ends at 5 s (its wind loop with it).
- **Yin Yang Fist:** the seal sits on the ground under the Panda at 0.55 s with a 0.55 shake, the Yang burst (five
  lightning strikes from 10 m up, bamboo and leaves) at 1.75 s with a 0.25 shake; the Yin status shows a small taiji
  under the foe (`yinYang`).

## Verification (the researcher's own checks)

- Every wait Ghidra dropped was read from the instructions: Nine Dragons' `Until(start + 1.6)` (0x1D8A02F), the slam's
  `rise + 1.05 + 0.3` (0x1D70BF5 / 0x1D70BFD), the Yang's `sealStart + 1.2` (0x1DCEAAF); the weave's `2 pi` / `pi` / 0.9
  (0x1D7086D / 0x1D7088F / 0x1D708A1); NineVanish's `SetActive(false)` (0x1D5520B). The rest are labelled DAT constants
  in the pseudo-C (0.4, 0.11, 3.9, 1.6, 0.35, 0.7, 22, 1.4, 1.3, 0.15, 2.2, 0.2, 0.6, 2.4, 0.9, 0.06, 0.8, 0.7, 0.4,
  0.15 / 0.3, 5, 6.5, 7.3, 0.75, 0.55, 0.55, 0.4, 1.19, 2.3, 120, 240, 75).
- The three Until times agree with the Bible's (Nine Dragons :1132, Yin Yang Fist :1167) and Tempest Dance's 5 / 5.75 /
  6.3 (:1155).
- `cues_paste.json` parses (`cues.py`: the formatted text `json.loads` back to the same object), 54 cues; every `tto/` name
  is in `probe.json`, `risingDragon_hit` in BB's rip (`probe_bb.json`); every voice in BB's `voices/` and both sounds in
  `sounds/` (`catalog.txt` lists the same names in TTO); the bones Hand_R / Hand_L / Foot_R / Foot_L are in
  `data/panda/rig.json`.
- `fk.py`'s idle pose puts the hands 0.26 m up, 0.19 m out and the Head bone 0.51 m up (the chibi rig), a sanity check
  of the tri transform and the mirror; the launch spots are 0.33-0.39 m up, 0.21-0.23 m ahead.
- Not done: a browser check (read-only researcher); HelixRibbonEmitter's and the ERB shaders' code (P3, P5).

## Verification (13/11/2026, checker; wins over the body above)

Re-derived on the office PC from `pseudo/Panda.c` (TTO1102), BB's `Math.cs` / `Panda.cs`, the Bible, the probes and the
page. Probes in `checks/fx_panda_research/verify/` (git-ignored): `tto_probe.json` (`wardrobe_fx_tto.py panda --probe` of
the 15 prefabs, no error), `bb_probe.json` (`wardrobe_fx.py panda --probe risingDragon_hit,...`), `fk_check.py` (the
hands at the launches with the page's own sampling: hermite baked at 30 fps, then slerp, as `buildClip`,
`index.html:1156`), `dis.py` -> `helix_small.asm` / `helix_rebuild.asm` (capstone over `client/GameAssembly.dll`),
`cues_check.py` (the blocks parsed, keys against `clips.json`, options against the check's `OPTS`), `fix_cues.py` ->
`cues_fixed.json` (the corrected block below, parsed back).

**Confirmed as written:** the four clips and lengths (`clips.json`: nineDragons 3.9, tempestDance 2.4 loop,
tempestDanceEnd 1.3, yinYangFist 2.3, all `tto: true`); all four in `wardrobe/tto_released.json:209-214`; every wait
(`Panda.c:13587` 0.4 + 0.11 k, `:13668` 3.9; King `Until(rise + 0.15 k)`, and 1.6 / 3.35 / 1.75 agree with the Bible's
"read from the instructions", `panda-skill-reference.md:1132`, `:1167`); the dance's pulses (`Panda.c` state loop: the
tick counter `pulses` even -> pulse, so 0.3 + 0.6 n, n = 0-7; the 16th tick at 4.8 is odd) and the end's 0.75 / 0.55;
Row6Begin's fade 0.1 (`Panda.c:41548`) and Row6Hand(~k & 1) = Hand_R for even k (`:41819`, offset `0x6b8 + (r ^ 1) x
8`); the dragon's side `cross(up, fwd)`, c1, c2, the clamp (0.7 at 9.78 m) and the spawn turn (all eight `rot`s
recomputed from (side, up, 1.4)); the hand table (`fk_check.py` reproduces all 24 numbers exactly); getSpawnPos =
the ground under the point (BB `Math.cs:1090-1110`: a ray from 2 m up, 4 m down), so the bites, kingRise and fall at
(0, 0, 10); the strikes at the foe + 1 up, identity (`Panda.c:42708-42715`, `RPC_risingDragon_hit` Instantiate with
`Quaternion.identity`); the seal's identity turn (`Panda.c:29609`); EffectControl lives, follow flags and AudioSources
of all 15 (`tto_probe.json`; only the aura has followState); every voice (`voices/risingDragon1|2`, `rainStorm1|2`,
`waterCrane1|2`, `finalMove`) and sound (`sounds/punch1`, `punch2`, the prefabs' clips; explosion1 in
`Assets/Resources/sound/fx`) in BB's rip; the 13 cued names exist; HelixRibbonEmitter's 23 fields (`dump.cs:11767-11789`)
and the probe's field names; the 10 m target outside 4.5 / 5.5 / 7 / 7.5 m (`rangeMod` 1, Mechanics reference :829).
The page carries the tempestDance cues past the 2.4 s clip: a held step starts its cues once and `FX.t` runs to 5 s
(`startStep`, `fxTick`, `index.html:1522-1530`, `:5468`), and the aura's `cut 5` comes at the step change (`fxStart`,
`index.html:5315-5320`: cutAt <= the step's end and age < life 5.3).

1. **The trails cue's `childBones` / `stop` do not work and should not be built that way.** `stop` (`index.html:4297`)
   calls `stop?.()` on every emitter, and so does every EffectControl at its life end (`:4311`); giving
   TrailRendererModern a `stop()` would change every TTO trail already cued. Decision (parts.md Interfaces 4-5, T3,
   which this verification adopts): the hook `fx:tto/tempestDance_trails` hangs each child on the hero's bone of its
   name (no `childBones` option: the hook knows its prefab) and reads the cue's **`off`** (seconds after the spawn) to
   call each trail's new `emitOff()`. Corrected cue: `[0, "fx", "tto/tempestDance_trails", {"off": 5.75, "kill": 6.18}]`
   (5.75 + 0.38 + 0.05). P4 reads accordingly.
2. **The dragons' and the King's options: one contract, the earlier classes' shape.** tto.md (c1, c2, flight, aim) and
   parts.md (k, fromBone, to) disagreed. Decision, by the Sheep / Cat movers (`fx_cues/sheep.json:420`
   gleamingBreath_wisp `{"d", "y", "to"}`, `cat.json:488` royalFlush_sword `{"d", "y", "to"}`): the spawn spot is cued
   (this report's fk numbers and `rot`, the Sheep's cued mouth / hand, `plans/fx_sheep/tto.md:76-79`), the target point is
   the existing `to`, and the mover computes the rest from the code's constants: **dragon `{x, y, d, rot, k, to, kill}`**
   (`k` gives side = +-right and c1's 1.3 + 0.15 (k % 4) / 2.2 + 0.2 (k % 3); c2 = to + 0.6 side + 2.4 up; flight =
   clamp(1.6 |spawn - to| / 22, 0.35, 0.7)); **King `{y, d, to: [0, 0, 10], kill}`** (`to` = the game's `end`, NineMark's
   ground point, as royalFlush_sword's; aim = to + 0.8 up and the 0.4 s flight are the mover's constants). No `c1`,
   `c2`, `flight`, `aim`, `fromBone` words; no `api.boneMatrix` for the dragons (the trails still need it).
3. **New cue words need the check's list and the cue-format comment.** `wardrobe_fx_check.py:176` (`OPTS`, enforced at
   `:222`) rejects unknown options; tto.md's block would have failed it (c1, c2, flight, aim, childBones). With 1-2 the
   Panda's new words are **`k`, `off`** (here) and **`enable`** (Three Steps, parts.md part 1 / skills_b.md): add them
   to `OPTS` and to the cue-format comment (`index.html` "2026-11-13, the <class>" paragraphs, `:4690-4780`).
4. **P6 is incomplete:** `FX_PART_FILES` needs `"tto_panda"` (`index.html:4020`) and the extractor's CODE_MOVERS lines
   are parts.md's (its "LAYOUTS" snippet, unchanged).
5. **Minor:** "Read this first" 1 says "`Panda.c:23391`" for the end's fade: the fade is inside Row6Begin
   (`Panda.c:41548`), `:23391` is only the call. `RPC_risingDragon_hit`'s Instantiate is at `:38213` area (identity),
   not `:38199-38212`. No value changes.

Nothing missed: the four clips are the Panda's only released TTO skill clips (`clap`, `wai`: no effect prefab, silent,
attacks_emotes.md:267); no rank picks (one rank each); every prefab the three coroutines load is in SKILL_FX (the 13 + the
counter + `yinYang`); the CollisionModule on nineDragons_fall's Sparks (type 1, World) is drawn today
(`shuriken.js:262-268`).

Corrected paste-ready block (54 cues; replaces section 7's; `cues_fixed.json`, parsed back to the same object):

```json
{
  "nineDragons": {
    "why": "TTO1102:Panda.<RPC_nineDragons>d__331::MoveNext@0x1D899A0 (pseudo/Panda.c:13461-13690; plans/fx_panda/tto.md 2.1), the 10 m target clicked (Panda::Row6Target@0x1D5C4B0 keeps it: reach^2 < d^2 rejects, :40707; DoRow6Skill@0x1D520F0 toMark = vFlat(target - hero), :40522-40535): Row6Begin('nineDragons', clip nineDragons, Once; PlayAnimation fade 0.1, Panda::Row6Begin@0x1D5B700 :41500-41570); cooldown, noForce Lv 1 3 s on the Panda (no look); Row6Voice risingDragon1 / risingDragon2 (Random.Range(0, 2), voices/, Panda::Row6Voice@0x1D5C940); nineDragons_cast owned at the hero, its rotation (:13550; followPosition, its own AudioSource qiStrike 0.8). Dragons k = 0-7 at Until(start + 0.4 + 0.11 k) (:13587-13589), prey[k % N] = the target (:13610-13636), from Row6Hand(k even) = Hand_R, odd Hand_L (:13640; Panda::Row6Hand@0x1D5BE80; the hand spots: checks/fx_panda_research/tto/fk.py on the nineDragons clip, +-3 cm): <NineDragon>d__336@0x1D6F860 (Panda.c:75-401): end = NineAim (the target + 0.6 up, Panda::NineAim@0x1D52A30), flight = clamp(1.6 |from - end| / 22, 0.35, 0.7) = 0.7 (:177-189), c1 = from + 1.4 fwd + side (1.3 + 0.15 (k % 4)) + up (2.2 + 0.2 (k % 3)), side = +-right by k's parity (:140-223), nineDragons_dragon bare Instantiate at the hand (the cue's k: Panda.NineDragon computes side, c1, c2 and flight from it, its spawn spot and to), LookRotation(c1 - from) (:224-241); each frame Bezier(from, c1, end + 0.6 side + 2.4 up, end) (:255-310, Panda::Bezier@0x1D51F00) faced along its motion (NineFly@0x1D53F80); on arrival NineVanish@0x1D55070 (Body / HeadGlow / HeadHalo SetActive(false), its ParticleSystems Stop, Destroy 0.5: :42339-42421) and nineDragons_bite at getSpawnPos(end) = the target's feet, identity (:316-361), Row6Sound punch1 (k even) / punch2 at 0.9 (the owner's; 0.6 others; at most one per 0.06 s, :362-374). Until(start + 1.6) (capstone 0x1D8A02F): Row6Shake 0.3 (the player's camera: left out) and <NineKing>d__339@0x1D701C0 (Panda.c:405-765): nineDragons_king at hero + 0.4 fwd + 0.7 up, LookRotation(flat dir) (:465-557), 0.4 s to aim = the target's ground + 0.8 up with a weave side x 0.9 sin(2 pi u)(1 - u) and up x 0.6 sin(pi u) (:625-693; capstone 0x1D7086D, 0x1D7088F), NineVanish; at 2.0 nineDragons_kingRise at the landing point, LookRotation(dir) (:720-727), shake 0.5 (left out), NineCharge + NineKingLock (the lock status: no look); 8 strikes Until(rise + 0.15 k) (:743-750): NineKingHit@0x1D54120 on each struck foe -> RPC_risingDragon_hit(foe + 1 up, fwd)@0x1D58980: risingDragon_hit (BB's prefab, cued as the rip's copy, Bison decision 43) at the foe + 1 up, identity (:42692-42715, :38199-38212); Until(rise + 1.05 + 0.3) (capstone 0x1D70BF5-0x1D70BFD): nineDragons_fall at the landing point, LookRotation(dir) (:588-595), shake 0.6 (left out), NineFall (its 'Nine Dragons!' text is the player's screen: left out); Until(start + 3.9): Row6End (:13668-13680)",
    "cues": [
    [0, "voice", "risingDragon1|risingDragon2"],
    [0, "fx", "tto/nineDragons_cast"],
    [0.4, "fx", "tto/nineDragons_dragon", {"x": 0.101, "y": 0.371, "d": 0.225, "rot": [-49.03, 42.88, 0], "k": 0, "to": [0.0, 0.6, 10.0], "kill": 1.2}],
    [0.51, "fx", "tto/nineDragons_dragon", {"x": -0.042, "y": 0.346, "d": 0.215, "rot": [-49.98, -46.01, 0], "k": 1, "to": [0.0, 0.6, 10.0], "kill": 1.2}],
    [0.62, "fx", "tto/nineDragons_dragon", {"x": 0.109, "y": 0.368, "d": 0.209, "rot": [-50.73, 48.81, 0], "k": 2, "to": [0.0, 0.6, 10.0], "kill": 1.2}],
    [0.73, "fx", "tto/nineDragons_dragon", {"x": -0.039, "y": 0.377, "d": 0.212, "rot": [-44.47, -51.34, 0], "k": 3, "to": [0.0, 0.6, 10.0], "kill": 1.2}],
    [0.84, "fx", "tto/nineDragons_dragon", {"x": 0.106, "y": 0.352, "d": 0.222, "rot": [-51.48, 42.88, 0], "k": 4, "to": [0.0, 0.6, 10.0], "kill": 1.2}],
    [0.95, "fx", "tto/nineDragons_dragon", {"x": -0.047, "y": 0.328, "d": 0.207, "rot": [-52.22, -46.01, 0], "k": 5, "to": [0.0, 0.6, 10.0], "kill": 1.2}],
    [1.06, "fx", "tto/nineDragons_dragon", {"x": 0.106, "y": 0.378, "d": 0.216, "rot": [-45.98, 48.81, 0], "k": 6, "to": [0.0, 0.6, 10.0], "kill": 1.2}],
    [1.1, "fx", "tto/nineDragons_bite", 10],
    [1.1, "sound", "punch1", {"vol": 0.9}],
    [1.17, "fx", "tto/nineDragons_dragon", {"x": -0.034, "y": 0.393, "d": 0.216, "rot": [-46.96, -51.34, 0], "k": 7, "to": [0.0, 0.6, 10.0], "kill": 1.2}],
    [1.21, "fx", "tto/nineDragons_bite", 10],
    [1.21, "sound", "punch2", {"vol": 0.9}],
    [1.32, "fx", "tto/nineDragons_bite", 10],
    [1.32, "sound", "punch1", {"vol": 0.9}],
    [1.43, "fx", "tto/nineDragons_bite", 10],
    [1.43, "sound", "punch2", {"vol": 0.9}],
    [1.54, "fx", "tto/nineDragons_bite", 10],
    [1.54, "sound", "punch1", {"vol": 0.9}],
    [1.6, "fx", "tto/nineDragons_king", {"y": 0.7, "d": 0.4, "to": [0, 0, 10], "kill": 0.9}],
    [1.65, "fx", "tto/nineDragons_bite", 10],
    [1.65, "sound", "punch2", {"vol": 0.9}],
    [1.76, "fx", "tto/nineDragons_bite", 10],
    [1.76, "sound", "punch1", {"vol": 0.9}],
    [1.87, "fx", "tto/nineDragons_bite", 10],
    [1.87, "sound", "punch2", {"vol": 0.9}],
    [2.0, "fx", "tto/nineDragons_kingRise", 10],
    [2.0, "fx", "risingDragon_hit", {"y": 1, "d": 10}],
    [2.15, "fx", "risingDragon_hit", {"y": 1, "d": 10}],
    [2.3, "fx", "risingDragon_hit", {"y": 1, "d": 10}],
    [2.45, "fx", "risingDragon_hit", {"y": 1, "d": 10}],
    [2.6, "fx", "risingDragon_hit", {"y": 1, "d": 10}],
    [2.75, "fx", "risingDragon_hit", {"y": 1, "d": 10}],
    [2.9, "fx", "risingDragon_hit", {"y": 1, "d": 10}],
    [3.05, "fx", "risingDragon_hit", {"y": 1, "d": 10}],
    [3.35, "fx", "tto/nineDragons_fall", 10]
    ]
  },
  "tempestDance": {
    "why": "TTO1102:Panda.<RPC_tempestDance>d__346::MoveNext@0x1D9B1B0 (pseudo/Panda.c:23122-23315; plans/fx_panda/tto.md 2.2): Row6Begin('tempestDance', clip tempestDance, Loop; fade 0.1) (:23164); addTimeOut 7.3 (:23171); Row6Voice rainStorm1 / rainStorm2 (:23172); tempestDance_aura owned at the hero, its rotation (:23188; followPosition + followState: its command changes to tempestDanceEnd at 5.0 s, so cut 5; its own looping AudioSource rainStorm 0.6); TempestTrails(true) (:23189; Panda::TempestTrails@0x1D5F010, Panda.c:43469-43705: each child of tempestDance_trails (Hand_R, Hand_L, Foot_R, Foot_L, TrailRenderers 0.3 / 0.3 / 0.38 / 0.38 s) instantiated under the hero's bone of its name, localPosition 0, localRotation identity, Clear(); off = emitting false, Destroy(trail.time + 0.05)); status tempestDance (309) 6 s on the Panda (no look: CharacterControl has none for it); the 0.3 s clock from start + 0.3 (:23231): each tick (pulse n = 0, 1, ...) with n even spawns tempestDance_pulse at the hero, its rotation, bare Instantiate (:23260-23281): 0.3, 0.9 ... 4.5 (8); TempestStorm (the owner's hits, r (3.5 + 1) m with Spirit Fist: the 10 m target is outside, so no Cut look and no Shadow Fist); at 5.0 s TempestFinish@0x1D5DBC0 (:23254-23256; Panda.c:44677-44760): StandbyEvent and RPC_tempestDanceEnd (the next step). The trails are switched off only by RPC_tempestDanceEnd's TempestTrails(false) 0.75 s into the end (Panda.c:23442): off 5.75 (fx:tto/tempestDance_trails, its TrailRendererModern emitOff), kill 5.75 + 0.38 + 0.05 = 6.18. Steering (TempestSteer) has no input on the page: the Panda stays put",
    "cues": [
    [0, "voice", "rainStorm1|rainStorm2"],
    [0, "fx", "tto/tempestDance_aura", {"cut": 5}],
    [0, "fx", "tto/tempestDance_trails", {"off": 5.75, "kill": 6.18}],
    [0.3, "fx", "tto/tempestDance_pulse"],
    [0.9, "fx", "tto/tempestDance_pulse"],
    [1.5, "fx", "tto/tempestDance_pulse"],
    [2.1, "fx", "tto/tempestDance_pulse"],
    [2.7, "fx", "tto/tempestDance_pulse"],
    [3.3, "fx", "tto/tempestDance_pulse"],
    [3.9, "fx", "tto/tempestDance_pulse"],
    [4.5, "fx", "tto/tempestDance_pulse"]
    ]
  },
  "tempestDanceEnd": {
    "why": "TTO1102:Panda.<RPC_tempestDanceEnd>d__355::MoveNext@0x1D9AD20 (pseudo/Panda.c:23333-23486; plans/fx_panda/tto.md 2.2), started by TempestFinish at 5.0 s: Row6Begin('tempestDanceEnd', clip tempestDanceEnd, Once; fade 0.1) (:23391); cooldown agiAdjust(75), the status removed (:23406-23413); Row6Voice waterCrane1 / waterCrane2 (:23415); Waits.Get(0.75) (:23419): TempestTrails(false) (:23442: the trails' stop, on the tempestDance cue), tempestDance_end at the hero, its rotation, bare Instantiate (:23468; its own AudioSource fuujinken2 1.0), Row6Shake 0.4 (the player's camera: left out), TempestEye (the owner's 5.5 m blast: the 10 m target is outside; its 'Eye of the Storm x N!' text needs 20 hits landed); Waits.Get(0.55) (:23449): Row6End at 1.3 s, the clip's length (:23435). The owner never glides (TempestGlide is the other clients' catch-up, :23376-23402)",
    "cues": [
    [0, "voice", "waterCrane1|waterCrane2"],
    [0.75, "fx", "tto/tempestDance_end"]
    ]
  },
  "yinYangFist": {
    "why": "TTO1102:Panda.<RPC_yinYangFist>d__357::MoveNext@0x1DCDC50 (pseudo/Panda.c:29191-29300; plans/fx_panda/tto.md 2.3): Row6Begin('yinYangFist', clip yinYangFist, Once; fade 0.1) (:29224); cooldown agiAdjust(120) (:29232-29233); Row6Voice finalMove (one name, :29234); yinYangFist_charge owned at the hero, its rotation (:29248; followPosition, its own AudioSource qiStrike 0.8); Until(start + 0.55) (:29249): <YinYangSeal>d__358@0x1DCE740 (Panda.c:29553-29682) at the hero's position: the seal at getSpawnPos (the ground under her), yinYangFist_seal there, identity, bare Instantiate (:29583-29613; its own AudioSource fuujinken1 0.9), Row6Shake 0.55 (capstone 0x1DCE82E; the player's camera: left out); SealYin at sealStart + 0.4 k, k = 0-2 (:29619-29650; r 7 m: the 10 m target is outside, so no yinYang status look on it); Until(sealStart + 1.2) (capstone 0x1DCEAAF): yinYangFist_burst at the seal, identity (:29667; its own AudioSource raijinken_hit 1.0), Row6Shake 0.25 (left out), SealYang (r 7.5 m: outside); Until(start + 2.3): Row6End (:29287, :29264-29265)",
    "cues": [
    [0, "voice", "finalMove"],
    [0, "fx", "tto/yinYangFist_charge"],
    [0.55, "fx", "tto/yinYangFist_seal"],
    [1.75, "fx", "tto/yinYangFist_burst"]
    ]
  }
}
```
