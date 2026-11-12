# Chameleon effects + sounds research: Combo (nAttack1), Charge Attack (cAttack1-4), emotes, basic moves, KO

Scope: the clips nAttack1 (RPC_nAttack1 and its dispatcher `doNormalAttack`), cAttack1, cAttack2 (RPC_cAttack1,
`doBeginCharge`), cAttack3, cAttack4 (the release RPC_cAttack2, `doReleaseCharge`; the early release RPC_cAttack0), any
MP / SP transfer style skill that plays an attack clip (there is none, below), the emotes (RPC_emotion), the basic moves
(run, falling, getUp, root, battle) and KO (RPC_ko, RPC_dead), plus silentWalk (the Charge Attack's walk, Silent Walk
#411). Research only (recipe steps 1-3). Line numbers are `D:\12tails\DecompiledSource\Chameleon.cs` unless another file
is named. Times are seconds from the start of the clip the cue is keyed by. Distance 0 = at the hero. Every opaque
predicate on the paths below was evaluated by `checks\fx_chameleon_research\attacks_emotes\preds.py` (it tags each
`if (a - b ==/!= c)` line T / F); each one goes the normal way.

Probes (read-only, nothing written outside `checks\`), all in `checks\fx_chameleon_research\attacks_emotes\`:
- `probe.txt` / `probe_summary.txt`: `wardrobe_fx.py chameleon --probe nAttack,nAttack_hit,clearArrow,cAttack_fire,cAttack_ring1,cAttack_ring2,blend,deadEffect,invisible`;
- `probe_fields.py` / `probe_fields.txt`: the Chameleon MonoBehaviour's PPtrs on the hero prefab (the AudioClip fields);
- `probe_events.py` / `probe_events.txt`: AnimationEvents on the Chameleon's clips;
- `shader_probe.py` / `shader_probe.txt`: the game's FX/Blend and FX/Camaflage shader text (resources.assets);
- `geom.py` / `geom.txt`: the arrow's aim, flight and ground contact;
- `clip_calls.txt` (`node pipeline/clip_calls.js D:/12tails/DecompiledSource wardrobe/data chameleon`) and the
  `clip_flow.js` dumps `nAttack1.txt`, `RPC_cAttack1.txt`, `RPC_cAttack2.txt`, `RPC_emotion.txt`, `RPC_ko.txt`,
  `RPC_dead.txt`, `RPC_revive.txt`, `RPC_activateIcon1.txt`.

TTO: `DecompiledSource_TTO_2026-11-02\pseudo\Chameleon.c` (TTO1102) has the same coroutines with the same literals and
waits (below); nothing in this scope is TTO-only, so the released-list rule does not come in.

---

## Read this first

1. **One SEQ step-time error** (index.html work, not a cue job). Today: `"Charge Attack: cAttack1 cAttack2*@9 cAttack3*@3.6 cAttack4"`.
   - cAttack1 -> cAttack2 at **0.8 s** (Yield 0.2 :16791 + Yield 0.6 :16782, then `PlayAnimation("cAttack2", 0)` :16370):
     the clip's own 0.8 s, a cut. Right as written.
   - `cAttack2*@9`: the release at 0.8 + 9 = 9.8 s gives `n = FloorToInt(Clamp(9.8 - 0.8, 0, 3 x 3)) = 9` (:6228,
     Charge Attack 3 = #113, getChargeAttackLv :8608), the full volley. Right.
   - **cAttack3 lasts 3.4 s, not 3.6.** The volley's 2n = 18 swings fire at 0.2 i (i = 0 ... 17), and the clip changes to
     cAttack4 **at the last swing**, i == 2n - 1 = 17, so at 17 x 0.2 = **3.4 s** (`PlayAnimation("cAttack4", 0)` :17212-17218,
     before that swing's cAttack_fire :17265). The 3.6 counted the 18th hit (0.2 s after the 18th swing), not the clip change.
     Standby comes 0.3 s after the 18th hit: 3.6 + 0.3 = **3.9 s** (:17440, :17147), 0.5 s into cAttack4 (0.6 s clip).
   - **Proposed: `"Charge Attack: cAttack1 cAttack2*@9 cAttack3*@3.4 cAttack4"`.** The cues below are placed for it (the
     18th cAttack_fire is cAttack4's own cue at 0). Every step cuts in in the game (`PlayAnimation(x, 0)` :16688, :16370,
     :17376, :17218); the first step keeps the page's 0.2 s fade (Bat decision 28, as the Sheep and the Penguin).
2. **The arrow you see in flight is the worn arrow.** The `nAttack` prefab has no renderer of its own (ProjectileControl +
   Chameleon_nAttack only, probe). `Chameleon_nAttack.Init` instantiates a copy of `mChar.mWep2` (the arrow piece, the
   page's slot **L**; `mWep2` = the mount_Hand_R piece, ChameleonEquipment.cs:1660-1715) as the projectile's child at
   localPosition 0, localRotation `Euler(0, 270, 270)`, every Renderer switched on (Chameleon_nAttack.cs:110-188). With
   `w_chm25` (Snooker) it copies **mWep1** instead (:114-120), the page's slot **R** (`snookerBall`). Copying the whole
   piece copies its own particles too: the arrows with weapon effects (weapon_fx.json: bdArrow, championArrow, flamingArrow,
   frozenArrow, heartArrow, paperArrow, poseidonArrow, royalArrow, royalArrowR, salamanderArrow, specialArrow) fly with them.
   This is the inventory's "needs Chameleon_nAttack" (part P1).
3. **The arrow in the hand is hidden while it is "shot"** (part P2, the Cat's proposed `hideProp` cue kind,
   plans/fx_cat/skills_b.md:61, item 7). Every `Renderer` under `mWep2` (mesh and particle renderers both) is switched off:
   - Combo: at 0.2 s (:15516-15548), back on at 1.8 s if she is idle and not invisible (case 4 :15761-15813);
   - the volley: at the release (:17385-17407), back on at the 3.9 s standby if not invisible (:17084-17125).
4. **Charge Attack blends the hero** (part P3). At 0.8 s (cAttack2's start) RPC_cAttack1 creates `blend` 0.6 m up and puts
   the `blend` status on her (`chaAdjust(3 x 3 + 3)` = 12 s, :16302-16364; mission / arena only, `mGameType > 4`, kept as the
   Sheep's precedent). The status's look (CharacterControl.cs:36665-36934): **for her own team** every Diffuse material
   becomes `new Material(Shader.Find("FX/Blend"))` with its own texture and every other renderer is switched off
   (:36835-36926); for other teams `FX/Camaflage` (a screen refraction), or every renderer off with Erase Senses #412
   (:36681-36825). The release ends it: `Chameleon.Update` removes `blend` once she is neither standby nor run and the
   command is not perfectBlend / cAttack1 (:166-201), so at RPC_cAttack2's `myCommand = "cAttack2"` (:17293). The cues use the
   own-team look, a `"skin"` cue (the Penguin's decision 16 kind) with a new `HERO_SKINS["FX/Blend"]` (question 4).
5. **Hero-played sounds (`"sound"` cues).** The hero's code plays these itself (`audio.PlayOneShot`), no effect carries them:
   - Combo, 0.2 s: `nAttack_bowFx1` = **`sounds/bow_fire1`** (the prefab field, probe_fields.txt: Chameleon MonoBehaviour
     offset 48), or **`sounds/plunger`** with `w_chm15` (Plunger Bow) worn (:15645-15695); the page's `w_chm15` is R `plungerBow`
     (data/item_map.json), so the two cues take `worn` / `notWorn ["R", "plungerBow"]` (Bat decision 15's options);
   - Charge, 0.2 s: **`sounds/cAttack_bow`** (:16253-16265);
   - run: AnimationEvents `playLeftFootEvent` at 0.1 s and `playRightFootEvent` at 0.4 s on `run` (probe_events.txt; the only
     events on any Chameleon clip), which play `footStep_left` = **`step_light2`** and `footStep_right` = **`step_light3`**
     (:101-155; probe_fields.txt offsets 32 / 40), own hero or anyone in a mission; both wavs are in
     `Resources/sound/fx/`, which `hero_sound_wav`'s fallback already searches (wardrobe_fx.py:391-406, built for the Bat's
     step_fly1), and the entry takes the Bat's `"everyCycle": true`.
   The effects that bring their own sound: `nAttack_hit` (bow_hit1), `cAttack_fire` (cAttack_fire), `blend` (blend).
6. **No KO voices in BB.** RPC_ko loads `Voices/ko1|ko2`, RPC_dead `Voices/dead1|dead2`, RPC_revive `Voices/revive`; none
   is in the rip's `heroes/chameleon/voices/` (the game logs "Cannot find ..." and stays silent). So the KO entry is the
   Sheep's (deadEffect on half the plays, no voice; Sheep decision 11).
7. **Emote voices**: the rip has hi, wave, ty, bow, cheer, cry, sleep and chat1-7 (RPC_emotion draws chat1-5 only). There is
   no laugh, beg, battle, sit, talk, pose or dance voice: those tiles stay silent.
8. **No MP / SP transfer style skill plays an attack clip.** `clip_calls.txt`: nAttack1 is played only by RPC_nAttack1
   (:16009), cAttack1-4 only by RPC_cAttack1 / RPC_cAttack2 (:16370-16688, :17218, :17376). (The Chameleon has no such
   skill; RPC_activateIcon1, the mission's "activate" channel, plays cast2 with a 0.5 s fade :45928 and loads a missing
   `Voices/activate1` :45983: no tile, Penguin decision 19.)
9. **The Bible's Charge Attack timing is off.** `chameleon-skill-reference.md:253` says the `blend` status comes "0.2 s later";
   the code adds both waits first: 0.2 (:16791) + 0.6 (:16782) = **0.8 s** (case 3 :16283-16364). Offer below.
10. **The full-charge ring comes 1 s before the full charge.** Ring k (k = 1, 2, ...) comes when `chargeTimer < held - 0.8`
    first holds with chargeTimer = k - 1 (:16422-16428), i.e. at held = 0.8 + (k - 1); ring k < 9 is `cAttack_ring1`, k == 9
    is `cAttack_ring2` (:16445-16508), so at **8.8 s** (8.0 s into cAttack2). At that moment the release would give
    `n = floor(8.8 - 0.8)` = 8; n = 9 needs 9.8 s (:6228). The tile's `@9` hold (release at 9.8) shows both. Offer below.
11. **Name collisions** (the cue kind picks the folder; voices are saved as `v_<name>`):
    - `nAttack1`, `cAttack1`, `cAttack2`, `bow` are clip names and `voices/` files; `nAttack2` is a voice only (no clip);
    - `blend`, `cAttack_fire` are effects and `sounds/` files (each effect plays its own);
    - `nAttack` is an effect only (the arrow; no `sounds/nAttack`);
    - `bow_fire1`, `cAttack_bow`, `plunger` are `sounds/` only; `step_light2` / `step_light3` live in `Resources/sound/fx/`.

---

## The dispatchers

- **`doNormalAttack`** (:5943-6060): own hero, from standby or run (:5996-6004), the `nAttack` timeout free (:6011). The aim
  `tDir = a - position` (:5984), where GameGui passes `a` = the enemy's `collider.bounds.center` (GameGui.cs:1626) or, with no
  target, `position + 10 forward` (GameGui.cs:1659); only a targeted other within 3 m changes it to `3 flat(dir) + up`
  (:6017-6040). No Penguin-style 0.25 m drop: the no-target shot aims at the 10 m ground point exactly (as the Bat's).
  (Game code 967 swaps the attack for `useItem("f_wtb1")`, :5957-5973: an event mode, out of scope.)
- **One clip, no stages.** The Chameleon's Combo (#101-104) is a rate of fire, not a chain: every shot is a fresh
  RPC_nAttack1 with `Rewind` + `animation.Play("nAttack1")` (:16006-16009). Combo 4 sets the `nAttack` timeout to 0.3 s
  (:15944-15950) and standby comes at 0.3 s (:15705-15731), so a held button fires every 0.3 s (+ frames; Bible :241). The
  page's single `nAttack1` tile is one shot (question 3).
- **`doBeginCharge`** (:6074-6156): from standby or run, the `cAttack` timeout free (:6123), Charge Attack #111 learned
  (:6129), not within 0.1 s of the last action (:6138) -> RPC_cAttack1 (:6144).
- **`doReleaseCharge`** (:6173-6266): while `attack` / `cAttack1` (:6204-6212). After 1.8 s and in a mission / arena
  (:6216-6222): `n = FloorToInt(Clamp(held - 0.8, 0, 3 x getChargeAttackLv()))` (:6228) -> RPC_cAttack2(n) (:6233; the
  network name `RPC_cAttack_fire<n>`, :6246, maps back to it, :1922-2018). Earlier: RPC_cAttack0 (:6254), no attack.
- **RPC_cAttack0** (`$RPC_cAttack0$22540` :17527, MoveNext :17619-17706): `myCommand "cAttack0"` (:17681), `CrossFade("root",
  0.2)` (:17690), standby 0.2 s later (`Yield(2, 0.2)` :17704 -> :17645). No voice, no effect: no tile, no cue.

---

## nAttack1 (the Combo shot)

Coroutine `RPC_nAttack1` (`$RPC_nAttack1$22484` :15380, MoveNext :15483-16051).

| t (s) | what | source |
|---|---|---|
| 0 | voice (below); `actionState "attack"`, `actionTime`, `myCommand "nAttack1"`, timeout 0.3 (Combo 4); Rewind, `animation.Play("nAttack1")` (a cut), Once; wait 0.2 | :15834-15933, :15935-16012, `Yield(2, 0.2)` :16036 |
| 0.2 | still `attack` / `nAttack1` (:15498-15513): **mWep2's renderers off** (:15516-15548); own hero (or anyone in a mission): **`sounds/plunger`** if `weapon == "w_chm15"`, else the field `nAttack_bowFx1` = **`bow_fire1`** (:15645-15695); own hero in a mission / arena (:15570-15580): `firePos = mPos + (0, 1.5, 0) + forward` (:15586), `fireDir = tDir - (0, 1.5, 0) - forward` (:15591), **RPC_clearArrow_fire** if `getClearArrow()` (Clear Arrow #263 and the `invisible` status, :15596-15602), else **RPC_nAttack_fire** (:15624); wait 0.1 | `Yield(3, 0.1)` :16038 |
| 0.3 | standby (if still `attack` / `nAttack1`); wait 1.5 | :15705-15731, `Yield(4, 1.5)` :16040 |
| 1.8 | if she is not attacking, the command is not nAttack1 and she is not `invisible`: mWep2's renderers on | :15761-15813 |

- **The voice** (:15834-15933): the voice option on, own hero or a mission teammate (:15840-15862). If more than 0.5 s has
  passed since the last action (`Time.time > actionTime + 0.5` :15863): `Voices/nAttack1` (load :15875, PlayOneShot :15887).
  Otherwise (a held button: each new shot starts right at the last one's standby, which set actionTime :15726)
  `Random.Range(0, 2) == 0` (:15898): `Voices/nAttack2` (:15910, :15922), else silent. A tile play starts from idle, so
  the cue is `nAttack1` (question 2; the Penguin kept MP Transfer's fresh-cast voice the same way).
- **RPC_nAttack_fire** (:8447-8545): `Effects/nAttack` (:8460) Instantiated at firePos, `LookRotation(fireDir)` (:8473);
  ProjectileControl life `(0.4 + 0.1 x getFarReachLv()) x rangeMod` (:8482) = **0.8 s** at Far Reach 4 (:8716-8768, passives
  on); `Chameleon_nAttack.Init(owner, fatalStrike status lv, 0)` (:8497).
- **Chameleon_nAttack** (`Chameleon_nAttack.cs`): Awake: layer 1, velocity `TransformDirection(0, 0, 30)` (:28-34); Init:
  **40 m/s** with Bow Mastery #401 (:94-100; passives on); the worn arrow's copy as its child (:110-188, Read this first 2);
  FixedUpdate: `age += dt`, Destroy at `life` (:53-62); OnTriggerEnter: on any collider not on the owner's layer and not
  layer 1 / 2 it destroys itself (:379-397) and, before any Player / Enemy test, calls the owner's `RPC_nAttack_hit` at
  `mCollider.ClosestPointOnBounds(collider.bounds.center)` (:406-436, the test :451-461): the ground counts.
- **RPC_nAttack_hit** (:8565-8600): `Effects/nAttack_hit` (:8578) Instantiated at the contact point with **the hero's
  rotation** (:8588). It plays its own `sounds/bow_hit1` (probe).
- **Geometry** (`geom.txt`; the 10 m ground point, the Bat's decision 1 and here the game's own no-target shot, centre path):
  - fire point 1 m ahead, 1.5 m up; aim (0, -1.5, 9): pitch **9.4623 deg** down; path 9.1241 m;
  - at 40 m/s: 0.2281 s, so the arrow meets the floor at the 10 m point **0.4281 s** into nAttack1 (the clip is 0.5333 s);
  - the game-true contact on flat ground (nAttack.prefab's trigger box 0.3 x 0.3 x 1.5 centred 1 m along the arrow, no
    gravity): the box's lower front corner touches down after 6.47 m, **0.362 s**, the hit about **8.37 m** ahead (question 1);
  - for comparison, aimed at a 0.6 m body centre at 10 m: pitch 5.71 deg, 0.4261 s.
- **TTO1102** `<RPC_nAttack1>d__143::MoveNext@0x1c06230` (pseudo/Chameleon.c:10796-11382): the same strings (:10845-10851,
  plunger / w_chm15 / RPC_clearArrow_fire / nAttack1 / nAttack2), `Random.Range(0, 2)` (:11068), the cut `Animation.Play`
  (:11165), waits 0.2 (:11183), 0.1 (:11374), 1.5 (:10883).
- Left out: Clear Arrow's own arrow (`clearArrow`, nClearLv 1: needs the `invisible` status, which the tile does not have);
  Fatal Strike's `fatalStrike` child on the arrow (Chameleon_nAttack.cs:197-250: only under the Fatal Strike buff, its own
  tile's business); every hit-side proc (damage, crit, Poison Arrow, Double Effect's `onNormalAttackHit` bow procs, Chain
  Lightning's fork / chain): they act on an enemy actually hit (Chameleon_nAttack.cs:451-799), with no target-point analogue.

```json
  "nAttack1": {
    "why": "Chameleon.cs RPC_nAttack1 (:15380-16051): at 0 the voice, own hero (:15840-15862): nAttack1 when more than 0.5 s since the last action (:15863, load :15875, PlayOneShot :15887; a held button gives nAttack2 or nothing, Random.Range(0, 2) :15898-15922: the tile starts from idle), clip cut (Rewind + animation.Play :16006-16009); 0.2 s (Yield(2, 0.2) :16036): mWep2's renderers off (:15516-15548; the page's L, the arrow and its own particles) until 1.8 s (Yield(3, 0.1) :16038, standby :15721, Yield(4, 1.5) :16040, back on :15761-15813: hideProp kill 1.6), the hero's PlayOneShot of the field nAttack_bowFx1 = sounds/bow_fire1 (checks/fx_chameleon_research/attacks_emotes/probe_fields.txt), or sounds/plunger with w_chm15 = R plungerBow (:15645-15695, data/item_map.json); RPC_nAttack_fire (:15624, :8447-8545): Effects/nAttack at mPos + (0, 1.5, 0) + forward (:15586), LookRotation(tDir - (0, 1.5, 0) - forward) (:15591, :8473), the no-target aim position + 10 forward (GameGui.cs:1659, doNormalAttack :5984) = the 10 m ground point (Bat decision 1): pitch atan(1.5 / 9) = 9.4623 deg; Chameleon_nAttack flies it 40 m/s with Bow Mastery #401 (Chameleon_nAttack.cs:100; passives on), life (0.4 + 0.1 x 4) = 0.8 s (:8482), carrying a copy of the worn arrow (mWep2; w_chm25 mWep1) at Euler(0, 270, 270) (:110-188), and ends on the floor (:379-397); at 0.2 + 9.1241 m / 40 m/s = 0.4281 s RPC_nAttack_hit at the contact point (:406-436, before any Player / Enemy test), nAttack_hit there with the hero's rotation (:8588; plays its own Sounds/bow_hit1); the arrow's trigger box is not counted (geom.txt: the game-true touch 8.37 m / 0.362 s)",
    "cues": [
    [0, "voice", "nAttack1"],
    [0.2, "hideProp", "L", {"kill": 1.6}],
    [0.2, "sound", "bow_fire1", {"notWorn": ["R", "plungerBow"]}],
    [0.2, "sound", "plunger", {"worn": ["R", "plungerBow"]}],
    [0.2, "fx", "nAttack", {"d": 1, "y": 1.5, "rot": [9.4623, 0, 0]}],
    [0.4281, "fx", "nAttack_hit", {"d": 10}]
    ]
  },
```

Sure: high on the trace and the times. The landing assumes the 10 m ground point (question 1).

---

## cAttack1 (Charge Attack: the draw)

Coroutine `RPC_cAttack1` (`$RPC_cAttack1$22502` :16112, MoveNext :16215-16797).

| t (s) | what | source |
|---|---|---|
| 0 | `actionState "attack"`, `actionTime`, `myCommand "cAttack1"`, timeout `cAttack` 1 s, LookAt, **`PlayAnimation("cAttack1", 0)`** (cut), Once; voice `Voices/cAttack1` (the option on; own hero or a mission teammate; no time gate, no random); wait 0.2 | :16657-16706, voice :16708-16778, `Yield(2, 0.2)` :16791 |
| 0.2 | still `attack` / `cAttack1` (:16229-16243): **`sounds/cAttack_bow`** (load :16253, PlayOneShot :16265); wait 0.6 | `Yield(3, 0.6)` :16782 |
| 0.8 | case 3 (:16283-16394): the change to cAttack2 (next section) | |

- TTO1102 `<RPC_cAttack1>d__147::MoveNext@0x1bfade0` (pseudo/Chameleon.c:4318-5059): the same strings (blend, cAttack_bow,
  cAttack_ring1 / 2, silentWalk, voices/cAttack1), waits 0.2 (:4668) and 0.6 (:4444), Silent Walk `hasSkill(0x19b)` (:4848).

```json
  "cAttack1": {
    "why": "Chameleon.cs RPC_cAttack1 (:16112-16797): at 0 the clip cut (PlayAnimation(cAttack1, 0) :16688) and voice cAttack1 (own hero or a mission teammate, no gate: :16708-16745, PlayOneShot :16778); 0.2 s (Yield(2, 0.2) :16791): the hero's PlayOneShot of Sounds/cAttack_bow (:16253-16265); at 0.8 s (Yield(3, 0.6) :16782) the change to the looped cAttack2, whose entry holds the blend and the rings",
    "cues": [
    [0, "voice", "cAttack1"],
    [0.2, "sound", "cAttack_bow"]
    ]
  },
```

## cAttack2 (Charge Attack: the held charge)

Same coroutine, case 3 at 0.8 s, then the per-FixedUpdate loop. Times below from cAttack2's own start (= 0.8 s).

- **0** (case 3 :16283-16394), still `attack` / `cAttack1`; in a mission / arena (`mGameType > 4` :16302):
  - not already blended (`!isBlend` :16313): **`Effects/blend`** created at `position + 0.6 up`, the hero's rotation
    (:16325-16337); it plays its own `sounds/blend` (probe: EffectControl life 1, a LineEmitter, AudioSource blend);
  - own hero: `RPC_AddStatus("blend", 4, chaAdjust(3 x 3 + 3))` (:16358): the FX/Blend look (Read this first 4) until the
    release, 9 s in the tile (12 s status);
  - `PlayAnimation("cAttack2", 0)` looped (:16370-16375); `mChargeTimer = 0` (:16388).
- **The loop** (`Yield(4, WaitForFixedUpdate)` :16776; it ends when she leaves `attack` / `cAttack1`, :16404-16418):
  - `if (chargeTimer < held - 0.8)`: chargeTimer++ (:16422-16428), and for her own layer (:16433-16439): while
    chargeTimer < 3 x 3 = 9 **`cAttack_ring1`**, at 9 **`cAttack_ring2`**, at the hero's position and rotation
    (:16445-16508). The first comes in case 3's own frame (held just past 0.8): rings at **0, 1, ..., 7** (ring1) and **8**
    (ring2), then nothing.
  - `cAttack_ring1` (probe): EffectControl life 1, followPosition, followState; a legacy Ellipsoid smoke burst (one-shot) and a
    RingEmitter. Ready. Each ends on its life before the next.
  - `cAttack_ring2`: life 1, followState (no followPosition); the same smoke and ring, plus a `star8` sparkle 0.7 m up, 1.1 m
    ahead after 0.5 s. Ready. Its life would run to 9.0 + a frame: the followState cut at the release (RPC_cAttack2's
    `myCommand "cAttack2"`), **8.95** in the page (the Penguin's 2.95 under a 3 s step).
  - Silent Walk #411 (passives on, :16526-16653): moving, she walks at speed 2 with `silentWalk` (0.2 fade :16584 / :16634);
    standing, `PlayAnimation("cAttack2", 0.2)` each frame (:16604 / :16648), a no-op on the playing clip. The tile stands.

```json
  "cAttack2": {
    "why": "Chameleon.cs RPC_cAttack1 case 3 (0.8 s in: Yield(2, 0.2) :16791 + Yield(3, 0.6) :16782; times from this clip), mission / arena (mGameType > 4 :16302): Effects/blend at the hero + 0.6 up, her rotation (:16325-16337; plays its own Sounds/blend), the blend status on her (RPC_AddStatus(blend, 4, chaAdjust(12)) :16358) whose look for her own team is FX/Blend on every Diffuse material, every other renderer off (CharacterControl.cs:36835-36926; the skin cue, index.html HERO_SKINS) until the release (Chameleon.cs Update :166-201 removes it at RPC_cAttack2's myCommand cAttack2 :17293): kill 9, the tile's hold; PlayAnimation(cAttack2, 0) looped (:16370-16375); each FixedUpdate (:16776) chargeTimer++ when chargeTimer < held - 0.8 (:16422-16428), for her own layer (:16433-16439) cAttack_ring1 while chargeTimer < 3 x Charge Attack 3 (:16445-16469), cAttack_ring2 at 9 (:16484-16508), at her position and rotation: rings at 0 ... 7 s, the full-charge ring at 8 s (8.8 s from the press; n = 9 needs the 9.8 s release, :6228); cAttack_ring2's followState cut at the release, 8.95 (EffectControl, as the Penguin's 2.95); ring1s end on their 1 s life",
    "cues": [
    [0, "fx", "blend", {"y": 0.6}],
    [0, "skin", "FX/Blend", {"kill": 9}],
    [0, "fx", "cAttack_ring1"],
    [1, "fx", "cAttack_ring1"],
    [2, "fx", "cAttack_ring1"],
    [3, "fx", "cAttack_ring1"],
    [4, "fx", "cAttack_ring1"],
    [5, "fx", "cAttack_ring1"],
    [6, "fx", "cAttack_ring1"],
    [7, "fx", "cAttack_ring1"],
    [8, "fx", "cAttack_ring2", {"cut": 8.95}]
    ]
  },
```

Sure: high. The rings' frame offsets (one FixedUpdate, 0.02 s) are not counted.

## cAttack3 (Charge Attack: the volley)

Coroutine `RPC_cAttack2` (`$RPC_cAttack2$22514` :16841, MoveNext :16955-17445), started by `doReleaseCharge` with n = 9.

| t (s) | what | source |
|---|---|---|
| 0 | `actionState "attack"`, `actionTime`, `myCommand "cAttack2"` (this ends the blend), LookAt, `myForce -= 0.5 forward`; voice **`Voices/cAttack2`** (own hero or a mission teammate); n != 1: **`PlayAnimation("cAttack3", 0)`** looped; **mWep2's renderers off**; i = 0 | :17283-17309, voice :17311-17358, :17370-17382, :17385-17407, :17412 |
| 0.2 i (i = 0 ... 17) | swing i: at i == 17 first `PlayAnimation("cAttack4", 0)`, Once (:17212-17223); still `attack` / `cAttack2`: **`Effects/cAttack_fire`** created at the hero's position and rotation (:17253-17265); wait 0.2 | IL_A65 :17201, `Yield(2, 0.2)` :17434 |
| 0.2 (i + 1) | own hero: `FindRecTarget(pos, forward, 1, 8, 12, 4)` and the hits (:16970-17050); i++ (:17059) | case 2 |
| 3.6 | i = 18 = 2n: wait 0.3 | `Yield(3, 0.3)` :17440 |
| 3.9 | still `attack` / `cAttack2`: not invisible -> mWep2's renderers on (:17084-17125); standby (:17130-17157) | case 3 |

- `cAttack_fire` (probe): EffectControl life 1; two ImageEmitters and two LineEmitters 0.65 m up, 1.5 m ahead (the bow's
  flash and the `massShot` streaks), two dust LineEmitters at the feet; it plays its own `sounds/cAttack_fire`. Ready.
- 18 swings: 0, 0.2, ..., 3.2 in cAttack3 (17 cues), the 18th at 3.4 = cAttack4's 0 (next section).
- Left out: the hits (damage on enemies in the box, no effect drawn by this code, the Poison / Rust words TTO adds);
  `myForce -0.5 forward` (a small push back at the release: the wardrobe has no hero mover, the Wolf's Feral Strike /
  Penguin decision 8 convention; question 7).
- TTO1102 `<RPC_cAttack2>d__148::MoveNext@0x1bfc3f0` (pseudo/Chameleon.c:5076-5748): the same strings (cAttack3, cAttack4,
  effects/cAttack_fire, voices/cAttack2) and the Renderer switch (Type:UnityEngine.Renderer :5140); TTO adds Poison / Rust
  to the hits (:5147, `Random.Range(0, 100)` on the target), nothing drawn by the hero.

```json
  "cAttack3": {
    "why": "Chameleon.cs RPC_cAttack2 (:16841-17445; doReleaseCharge at 9.8 s: n = FloorToInt(Clamp(9.8 - 0.8, 0, 3 x 3)) = 9, :6228-6233): at 0 myCommand cAttack2 (:17293; the blend ends, Update :166-201), voice cAttack2 (own hero or a mission teammate, :17311-17358), PlayAnimation(cAttack3, 0) looped (:17376-17382), mWep2's renderers off (:17385-17407; the page's L) until the 3.9 s standby (case 3 :17084-17157: hideProp kill 3.9); 2n = 18 swings 0.2 s apart (IL_A65 :17201-17277, Yield(2, 0.2) :17434, i++ :17059), each Effects/cAttack_fire at the hero's position and rotation (:17253-17265; plays its own Sounds/cAttack_fire): 17 here at 0 ... 3.2 s, the 18th with cAttack4 at 3.4 s (i == 2n - 1, :17212-17218); the hits (:16970-17050) draw nothing; myForce -0.5 forward (:17308) left out (no hero mover)",
    "cues": [
    [0, "voice", "cAttack2"],
    [0, "hideProp", "L", {"kill": 3.9}],
    [0, "fx", "cAttack_fire"],
    [0.2, "fx", "cAttack_fire"],
    [0.4, "fx", "cAttack_fire"],
    [0.6, "fx", "cAttack_fire"],
    [0.8, "fx", "cAttack_fire"],
    [1.0, "fx", "cAttack_fire"],
    [1.2, "fx", "cAttack_fire"],
    [1.4, "fx", "cAttack_fire"],
    [1.6, "fx", "cAttack_fire"],
    [1.8, "fx", "cAttack_fire"],
    [2.0, "fx", "cAttack_fire"],
    [2.2, "fx", "cAttack_fire"],
    [2.4, "fx", "cAttack_fire"],
    [2.6, "fx", "cAttack_fire"],
    [2.8, "fx", "cAttack_fire"],
    [3.0, "fx", "cAttack_fire"],
    [3.2, "fx", "cAttack_fire"]
    ]
  },
```

## cAttack4 (Charge Attack: the last swing)

```json
  "cAttack4": {
    "why": "Chameleon.cs RPC_cAttack2 IL_A65 at i == 2n - 1 = 17 (3.4 s after the release, the proposed cAttack3*@3.4): PlayAnimation(cAttack4, 0), Once (:17212-17223), then the 18th Effects/cAttack_fire at the hero's position and rotation (:17253-17265; its own Sounds/cAttack_fire); its hit at 0.2 s, standby at 0.5 s (Yield(3, 0.3) :17440, :17147; the arrow back on, :17084-17125, cAttack3's hideProp ends there)",
    "cues": [
    [0, "fx", "cAttack_fire"]
    ]
  },
```

Sure: high. With today's `cAttack3*@3.6` the 18th fire would come 0.2 s late (question: none, Read this first 1).

## silentWalk (the Charge Attack's walk, Silent Walk #411): optional, recommended yes

The clip is played only inside RPC_cAttack1's loop, while she moves (:16526-16594, :16611-16644), so it always comes after
cAttack2's start: the blend look is on and the rings keep coming each second, following her (`cAttack_ring1`'s
followPosition). The page plays it as a `LOOPS` move for `HOLD_SECS` (1.5 s, index.html:1245, :1339-1342). No
AnimationEvent on it (probe_events.txt). Question 5.

```json
  "silentWalk": {
    "why": "Chameleon.cs RPC_cAttack1's loop with Silent Walk #411 (passives on, :16526-16653): moving while charging, PlayAnimation(silentWalk, 0.2) (:16584, :16634), always after cAttack2's start (case 3 :16302-16388), so under the blend status (its own-team look FX/Blend, CharacterControl.cs:36835-36926: the skin cue, kill 1.5 = the page's HOLD_SECS) with cAttack_ring1 each second at her (:16422-16469; followPosition, life 1), the phase picked at 0 s",
    "cues": [
    [0, "skin", "FX/Blend", {"kill": 1.5}],
    [0, "fx", "cAttack_ring1"],
    [1, "fx", "cAttack_ring1"]
    ]
  },
```

---

## Emotes and basic moves

`RPC_emotion` (`$RPC_emotion$23182` :40223, MoveNext :40340-41046), as the other classes':

- The voice at 0, **before** the clip (:40408-40486). Gates: the voice option (:40408); more than 2 s since the last action
  (`Time.time > actionTime + 2` :40414); own hero, game code 31, or a mission teammate (:40420-40442).
- `emo_chat` -> `Voices/chat` + `Random.Range(1, 6)` = chat1-5 (:40466; chat6 / chat7 are in the rip, never drawn); every
  other `emo_<name>` -> `Voices/<name>` (`Substring(4)` :40474), `PlayOneShot` (:40486, volume 1) only if it loads.
- Then `actionState "emotion"` (:40505) and the clip with a 0.2 s fade. No effect and no `Sounds/` anywhere in RPC_emotion.

| emote | clip | voice (voices/) | source |
|---|---|---|---|
| emo_hi, emo_wave | wave | hi / wave | :40540, :40547 -> :40981 |
| emo_ty, emo_bow | bow | ty / bow | :40556, :40563 -> :40974 |
| emo_laugh | laugh | none (no file) | :40570-40576 |
| emo_sit | sit | none | :40590-40596 |
| emo_sleep | sleep | sleep | :40602-40608 |
| emo_cheer | cheer | cheer | :40614-40620 |
| emo_beg | beg | none (no file) | :40626-40632 |
| emo_cry | cry | cry | :40638-40644 |
| emo_talk, emo_chat | talk | talk: none; chat: chat1-5 | :40652, :40659 -> :40952 |
| emo_pose | pose5 / 15 / 25 / 35 / 45 / 58 / 65 / 46 / 66 by the worn set (w_chm56 + c_all56: `animation.Stop()`), else pose | none | :40666-40912 |
| emo_battle | battle | none (no file) | :40922-40928 |
| emo_dance | dance | none | :40937-40945 |

- TTO-only emote clips (clap, cooking, fishingChameleon, mining, planting, pose37, wai) stay silent (Bat decision 36).
- **KO** (no voices, Read this first 6):
  - `RPC_ko` (`$RPC_ko$23351` :46150): `actionState "ko"` (:46349), `PlayAnimation("ko", 0)` (:46364); `Random.Range(0, 2)`
    (:46399) ko1 / ko2 (:46409, :46440: not in the rip); getUp after 3 s (`Yield(2, 3)` :46482 -> :46266), standby 1 s later
    (`Yield(3, 1)` :46479 -> :46290). No effect.
  - `RPC_dead` (`$RPC_dead$23358` :46526): Rewind + `PlayAnimation("ko", 0)` (:46720-46723); dead1 / dead2 (:46758-46813: not
    in the rip); then **always** `Instantiate(deadEffect, hero position, hero rotation)` (IL_76D :46825-46842; the voice gates
    jump there, :46743, :46751; its predicate `65344 - 113841 != -48496` holds).
  - `deadEffect` (probe): EffectControl life 3, no follow; the `chameleon_dead` ImageEmitter 0.8 m up (Life 1.2) and two dust
    LineEmitters, all after Delay 0.5. Ready.
  - Sheep decision 11: one of the two at random, even chance.
- **getUp**: RPC_ko's (no voice) or RPC_revive's (`animation.Play("getUp")` :47163, `Voices/revive` :47136: not in the rip):
  nothing. **falling, root, battle**: nothing (the battle clip's other callers, RPC_useMount :44493 and RPC_useCoin :44816, add
  no sound). **run**: the footsteps (Read this first 5).

```json
  "wave": {
    "why": "Chameleon.cs RPC_emotion (:40223): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:40474, PlayOneShot :40486; the rip has hi, wave, ty, bow, cheer, cry, sleep, chat1-7); no effect, no sound; emo_hi (:40540) and emo_wave (:40547) both play the wave clip (:40981): voice hi or wave",
    "cues": [
    [0, "voice", "hi|wave"]
    ]
  },
  "bow": {
    "why": "Chameleon.cs RPC_emotion (:40223): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:40474, PlayOneShot :40486; the rip has hi, wave, ty, bow, cheer, cry, sleep, chat1-7); no effect, no sound; emo_ty (:40556) and emo_bow (:40563) both play the bow clip (:40974): voice ty or bow",
    "cues": [
    [0, "voice", "ty|bow"]
    ]
  },
  "sleep": {
    "why": "Chameleon.cs RPC_emotion (:40223): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:40474, PlayOneShot :40486; the rip has hi, wave, ty, bow, cheer, cry, sleep, chat1-7); no effect, no sound; emo_sleep (:40602-40608): voices/sleep",
    "cues": [
    [0, "voice", "sleep"]
    ]
  },
  "cheer": {
    "why": "Chameleon.cs RPC_emotion (:40223): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:40474, PlayOneShot :40486; the rip has hi, wave, ty, bow, cheer, cry, sleep, chat1-7); no effect, no sound; emo_cheer (:40614-40620)",
    "cues": [
    [0, "voice", "cheer"]
    ]
  },
  "cry": {
    "why": "Chameleon.cs RPC_emotion (:40223): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:40474, PlayOneShot :40486; the rip has hi, wave, ty, bow, cheer, cry, sleep, chat1-7); no effect, no sound; emo_cry (:40638-40644)",
    "cues": [
    [0, "voice", "cry"]
    ]
  },
  "talk": {
    "why": "Chameleon.cs RPC_emotion (:40223): every emote's voice at 0, before its clip, emo_<name> = Voices/<name> (:40474, PlayOneShot :40486); no effect, no sound; emo_chat (:40659) plays the talk clip (:40952) with chat1-5 at random (Random.Range(1, 6), :40466; chat6 / chat7 in the rip are never drawn); emo_talk (:40652) plays it silent (no Voices/talk): the tile takes the chat's voice",
    "cues": [
    [0, "voice", "chat1|chat2|chat3|chat4|chat5"]
    ]
  },
  "run": {
    "why": "the run clip's AnimationEvents playLeftFootEvent at 0.1 s and playRightFootEvent at 0.4 s (checks/fx_chameleon_research/attacks_emotes/probe_events.txt) -> Chameleon.cs :101-155: the hero's audio.PlayOneShot(footStep_left) = step_light2 / (footStep_right) = step_light3 (the fields :14841-14844, probe_fields.txt; Resources/sound/fx/), own hero or anyone in a mission (mGameType > 4, :108-117, :137-146); every cycle of the run (the events fire each loop: everyCycle, as the Bat's wing flap)",
    "everyCycle": true,
    "cues": [
    [0.1, "sound", "step_light2"],
    [0.4, "sound", "step_light3"]
    ]
  },
  "ko": {
    "why": "Chameleon.cs RPC_ko (:46150) and RPC_dead (:46526) both play the ko clip (:46364, :46723); their voices ko1 / ko2 / dead1 / dead2 (:46409, :46440, :46770, :46801) are not in BB's data (the rip's heroes/chameleon/voices/ has none: silent in the game); RPC_dead always puts deadEffect at the hero's position and rotation (:46825-46842; EffectControl life 3), RPC_ko nothing (getUp after 3 s, :46482): one of the two at random, even chance (Sheep decision 11)",
    "cues": [
    [0, "fx", "deadEffect", {"p": 0.5, "roll": "dead"}]
    ]
  }
```

---

## Parts needed (build stage)

1. **P1 `Chameleon_nAttack`** (`nAttack`; `clearArrow` uses the same script, not cued here).
   - Motion: velocity `TransformDirection(0, 0, 30)` at Awake (Chameleon_nAttack.cs:34), **40** when the owner has #401 (Init
     :94-100; passives on: 40); a straight line, no gravity (`m_UseGravity: 0`); life = ProjectileControl.life, 0.8 s
     (Chameleon.cs:8482; FixedUpdate `age += dt`, Destroy at life, :53-62).
   - End: when its origin meets the floor (y 0) going down, as the Penguin's / Sheep's / Bat's parts (the trigger box not
     counted: question 1).
   - The look: a fresh copy of the worn piece in its BB prefab frame (root at identity, its own nodes and its weapon_fx
     particles, renderers on), the projectile's child at localPosition 0, localRotation `Euler(0, 270, 270)` (:120-188):
     slot **L** (mWep2), or slot **R** with `w_chm25` worn (:114-120; the page's R `snookerBall`, data/item_map.json). No piece
     worn there: nothing visible (`if (!gameObject) break` :193-195). A page hook is needed for the copy (for example
     `api.propCopy(slot)`: `buildProp(p)` + `finishProp` + `weaponFx` on a new root, disposed with the effect), since the
     worn model sits under its TTO placement on a hand bone.
   - Not built: Fatal Strike's child (:197-250, only under its buff); Clear Arrow's `nClearLv` branch (:272-321).
2. **P2 `hideProp`** cue kind (shared with the Cat's P6, plans/fx_cat/skills_b.md:61): `[t, "hideProp", slot, {"kill": s}]`
   takes that slot's model **and its weapon particles** off the camera (the game switches off every `Renderer` under mWep2,
   particle renderers included: :15516-15548, :17385-17407), held per cue (a key per cue, as `heroHide`: a held button's
   later shots keep it hidden), back at `kill` or on a new pick. The flying copy (P1) is built with its renderers on
   (Chameleon_nAttack.cs:175-186), so it shows while the hand's arrow is hidden.
3. **P3 `HERO_SKINS["FX/Blend"]`** (index.html, beside FX/CosmicRift; the game's shader text in `shader_probe.txt`,
   resources.assets path id 971):
   - pass 1: `SetTexture [_MainTex] { ConstantColor (1,1,1,0.35) combine texture, constant alpha }`, `Blend SrcAlpha
     OneMinusSrcAlpha`, `ColorMask RGB`, default cull (back) and ZWrite: the texture unlit at 35 %;
   - pass 2: `Cull Front`, `Blend SrcAlpha SrcColor`, `ColorMask RGB`, the vertex pushed out along its view-space normal,
     `xy += (n.x x P[0][0], n.y x P[1][1]) x clip z x 0.002` (CosmicRift's 0.008), colour **(0.8, 0.8, 0.3, 0.5)**: a thin
     yellow rim behind the body (src x 0.5 + dst x src colour);
   - the order is ghost first, then the shell (CosmicRift's is shell first); every other renderer switched off (the page's
     approximation: every hero mesh taken as Diffuse, as CosmicRift's note says); Queue Transparent.
4. Already built, used here: the `"sound"` fallback to `Resources/sound/fx/` (wardrobe_fx.py `hero_sound_wav`), `everyCycle`
   (index.html fxTick), `worn` / `notWorn` (fxStart), the `"skin"` kind, legacy particles (fxparts/particles.js, for the rings'
   smoke). Everything else cued is ready by the probe and the inventory: nAttack_hit, cAttack_fire, cAttack_ring1,
   cAttack_ring2, blend, deadEffect.

Inventory note: `plans/fx_inventory.md` "### chameleon" has `nAttack` "needs Chameleon_nAttack" (right) and every other
effect here ready (right); it cannot see the three AudioClip fields (bow_fire1, step_light2, step_light3), which are
hero-played sounds, not effects.

## Left out

- Every hit-side effect and proc on the enemy (damage, crits, Poison Arrow / Rusty Decay words, Double Effect's bow procs,
  Chain Lightning's fork and chain, Venom Phantom's brand): no target-point analogue (they need an enemy actually hit).
- Clear Arrow's arrow and Fatal Strike's arrow child: they need a status the tile does not have.
- The release push `myForce -0.5 forward` (:17308): no hero mover (question 7).
- RPC_cAttack0 (the early release): nothing drawn, no tile.
- The blend look as other teams see it (FX/Camaflage, or hidden with Erase Senses): question 4.
- Game code 967's `useItem("f_wtb1")` normal attack (:5957-5973): an event mode.

## Open questions (each with the recommended answer)

1. **The Combo arrow's landing.** The cues end it on the floor at the 10 m point after 0.4281 s (centre path; Bat decision 1,
   and here also the game's own no-target shot). The game-true touch of its 0.3 x 0.3 x 1.5 trigger box on flat ground is
   8.37 m after 0.362 s; a targeted enemy is aimed at its 0.6 m body centre (pitch 5.71 deg, 0.4261 s to the centre).
   **Recommended: keep the 10 m ground picture** (the cues above).
2. **The Combo voice.** The game says `nAttack1` only after a 0.5 s pause; a held button's shots say `nAttack2` half the time,
   nothing the other half. **Recommended: `nAttack1` on every play** (each tile play is a fresh shot from idle, as the
   Penguin's MP Transfer kept its fresh-cast voice); the `nAttack1|nAttack2` held-fire pick would need a "repeat" cue option
   the page does not have.
3. **The Combo tile.** One shot today (`nAttack1`, 0.5333 s). The game's Combo 4 is a shot every 0.3 s while held; a
   `"Normal Attack: nAttack1@0.3 nAttack1@0.3 nAttack1"` sequence would show three, but every step would replay the same
   `nAttack1` cues (voice included). **Recommended: keep the single shot** (the วนซ้ำ toggle already repeats it).
4. **The blend look.** **Recommended: the own-team FX/Blend skin** (the wardrobe's hero is the player's own; CharacterControl.cs
   :36835-36926), not the enemy's FX/Camaflage refraction or the Erase Senses hide. Perfect Blend (another report) gives the
   same status, so P3 serves both.
5. **The silentWalk tile.** **Recommended: yes**, the entry above (the blend skin for its 1.5 s and a ring each second), since
   the game plays the clip only under the charge's blend; the alternative is a silent, plain walk.
6. **Weapon variants.** **Recommended: yes**, as the Penguin's Staff of Time (decision 18) and the Bat's Homing Wand (decision
   15): the Plunger Bow's `plunger` sound (`worn` / `notWorn ["R", "plungerBow"]`) and the Snooker set's flying ball (P1 copies
   slot R with `w_chm25`, `snookerBall` worn in R). The game keys both on the weapon code (`w_chm15`, `w_chm25`); the page keys
   them on the worn piece.
7. **The release push** (`myForce -0.5 forward`, :17308). **Recommended: left out** (no hero mover; the Wolf's Feral Strike /
   Penguin decision 8 convention).
8. **TTO-only emote clips** silent; `talk` keeps BB's chat1-5 (chat6 / chat7 never drawn). **Recommended: as Bat decision 36.**
9. **activateIcon1** (cast2, silent: `Voices/activate1` missing). **Recommended: no tile** (Penguin decision 19).

## Offer for the Bible

New for `chameleon-skill-reference.md` (its Combo :238-248 and Charge Attack :250-258 sections), offered, not written:
- Charge Attack: the `blend` status and its puff come **0.8 s** after the press (Yield 0.2 + 0.6, :16791, :16782), not 0.2 s
  (:253); cAttack2 loops from 0.8 s.
- The charge rings: one each second from 0.8 s for her own team, `cAttack_ring2` (the "full" ring) at 8.8 s at rank 3
  (chargeTimer == 3 x rank), one second before the release reaches the full n = 9 at 9.8 s (`floor(held - 0.8)`).
- The volley's look: cAttack3 looped at the release, a `cAttack_fire` per swing every 0.2 s, cAttack4 with the last swing at
  0.2 x (2n - 1) s, standby at 0.4 n + 0.3 s; the voice `cAttack2`; a 0.5 push back.
- The Combo voice: `nAttack1` after a 0.5 s pause, else `nAttack2` half the time; the bow sound `bow_fire1` (`plunger` with
  the Plunger Bow); the arrow in flight is a copy of the worn arrow (the Snooker ball with w_chm25), and the hand's arrow is
  hidden from 0.2 s to 1.8 s after the last shot.
- BB has no Chameleon ko / dead / revive / activate voices (silent).

## Verification

Checker `verify_a`, 2026-11-13 (home PC), read only. Every coroutine in scope re-read from `D:\12tails\DecompiledSource\Chameleon.cs`
with the opaque predicates worked out (`checks\fx_chameleon_research\verify_a\flow.sh`, `c_nAttack1.txt`, `c_cAttack1.txt`,
`c_cAttack2.txt`), the clip callers listed again (`verify_a\playcalls.txt`: every `PlayAnimation` / `animation.Play` /
`CrossFade` literal mapped to its coroutine), BB vs TTO1102 asset strings per coroutine diffed (`verify_a\tto_strings.py`),
the paste blocks parsed as JSON (`verify_a\parse_blocks.py`: all 13 entries parse; kinds fx / hideProp / skin / sound /
voice). Checked and right: every time in the nAttack1, cAttack1-4, emote and KO tables; the Combo voice gate and pick
(:15863, :15898); the 10 m ground aim (GameGui.cs:1659), pitch 9.4623, 40 m/s (Chameleon_nAttack.cs:100), hit 0.4281 s; the
Charge's 0.8 s blend (the Bible's "0.2 s" at chameleon-skill-reference.md:253 is wrong, as item 9 says); rings 0 ... 7 + the
full ring at 8 (chargeTimer counted after the increment, :16422-16508); the volley's cAttack4 at 3.4 and standby at 3.9
(:17202-17218, :17440), so **`cAttack3*@3.4` is right**; the hand's arrow switches (:15516-15548 / :15761-15813,
:17385-17407 / :17084-17125); the fields footStep_left / footStep_right / nAttack_bowFx1 in declaration order
(:14841-14847 = probe offsets 32 / 40 / 48); `step_light2` / `step_light3` in `Resources/sound/fx/`; slot L = mWep2 =
getWeapon(code, 2) on mount_Hand_R (ChameleonEquipment.cs:1643-1715), `w_chm15` = R plungerBow, `w_chm25` = R snookerBall
(item_map.json); the FX/Blend shader numbers (push 0.002, colour c[0].yyzw = (0.8, 0.8, 0.3, 0.5), shader_probe.txt:29-44);
`EffectControl.followState` ends on an actionState **or** myCommand change (EffectControl.cs:226-232), which is what the
8.95 ring cut needs; TTO1102 has the same strings in every coroutine here (no TTO-only cue).

Corrections:

1. **silentWalk's hold is 1.6 s, not 1.5** (attacks_emotes.md:307, :312, :314). A held LOOPS move plays whole cycles:
   `Math.max(1, Math.round(HOLD_SECS / clip.duration)) * clip.duration` (index.html:1431; HOLD_SECS 1.5 at :1274, the hold
   set at :1407) = round(1.5 / 0.8) x 0.8 = **1.6 s** for the 0.8 s silentWalk. The skin's kill becomes 1.6. The line
   references `index.html:1245, :1339-1342` are stale: now :1274, :1407, :1431.
2. Wording only (attacks_emotes.md:354): RPC_dead loads `Resources.Load(".../Effects/deadEffect")` (:46832) and Instantiates
   it at the hero's position and rotation (:46842); it is not a prefab field. The cue is unchanged.

Notes (no change to the cues):
- The Combo's arrow in the game ends where its trigger box (front 1.75 m ahead of the origin) first touches something
  (nAttack.prefab:34-44, Destroy on contact Chameleon_nAttack.cs:379-397); question 1's centre-path picture is the Bat's
  decision 1 and stands. For a **targeted** arrow (Left Stride's, skills_a) the same box decides the hit time: see
  skills_a.md "## Verification" 2, which P1 needs (an end at the target body, not only on the floor).
- skills_b's silentWalk entry (FX/Invisible) and this one (FX/Blend) both exist; this one is right (CharacterControl.cs:
  36835-36926 is the blend branch, the invisible look is :32626-32684).

Corrected paste-ready block (only this entry changed; every other block above stands as written):

```json
  "silentWalk": {
    "why": "Chameleon.cs RPC_cAttack1's loop with Silent Walk #411 (passives on, :16526-16653): moving while charging, PlayAnimation(silentWalk, 0.2) (:16584, :16634), always after cAttack2's start (case 3 :16302-16388), so under the blend status (its own-team look FX/Blend, CharacterControl.cs:36835-36926: the skin cue, kill 1.6 = the page's hold, HOLD_SECS 1.5 rounded to whole 0.8 s cycles, index.html:1274, :1431) with cAttack_ring1 each second at her (:16422-16469; followPosition, life 1), the phase picked at 0 s",
    "cues": [
    [0, "skin", "FX/Blend", {"kill": 1.6}],
    [0, "fx", "cAttack_ring1"],
    [1, "fx", "cAttack_ring1"]
    ]
  },
```
