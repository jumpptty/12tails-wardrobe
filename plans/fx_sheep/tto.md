# Sheep effects + sounds research: the three TTO Lv 100 skills (Gleaming Breath, Lucent Barrier, Grand Codex)

Scope: the TTO clips `gleamingBreath` (1.7 s), `lucentBarrier` (1.4 s), `grandCodex` (1.4 s), all `tto: true` in
`wardrobe/data/sheep/clips.json`. No BB code plays them. Research only: this file is the only file written, plus the probe
scripts in `checks/fx_sheep_research/tto/`. Sources: TTO's pseudo-C
`C:\Users\Jump\Desktop\12tails\DecompiledSource_TTO_2026-11-02\pseudo\Sheep.c` and `CharacterControl.c`, cited as
`TTO1102:Method@RVA`. Where the pseudo-C is unclear I used capstone over `client\GameAssembly.dll` (the `il2cpp` section)
and the call-site finder `checks/fx_sheep_research/tto/callers.py`. Other sources: the Bible's `sheep-skill-reference.md`
"TTO Lv 100 skills", the TTO Addressables catalog (`client\aa\catalog.bin` through `tools\aa_catalog.py`), BB's rip for
voices and sounds, and BB's `CharacterControl.cs` for the Reverse status look.

Times are seconds from the start of the clip the cue is keyed by. The TTO coroutines wait with `Sheep::Until(start + t)`.
The machine code at `TTO1102:Sheep.<Until>d__284::MoveNext@0x1B257C0` is `comiss [this+0x20], Time.time` and yields while
`t > now`. So every wait is an **absolute time from the coroutine start**, not a step to add up. I checked each sum below
against that. All three skills have one rank, so max rank changes nothing for them. The two passives ride on Revive 2 /
Reverse 2 (max rank).

## Read this first

1. **This PC cannot read any Sheep TTO prefab.**
   - `RippedAssets_TTO_2026-11-04\ExportedProject\Assets` holds a single font (`GMO38.ttf`), on both `C:\Users\Jump\Desktop\12tails` and `D:\12tails`.
   - The video folder has no `tto_assets`.
   - The TTO clients here (`DecompiledSource_TTO_2026-11-0{2,6,9}\client\aa_dec`) hold 1-3 bundles each. None is the effects bundle: `325c14de928ce90f8296b1adce8a7656.bundle` in the 1102 catalog, `c61d6fd6...` in 1109.

   So everything below comes from the **code**: times, positions, rotations, owned or world, voices.

   What each prefab *contains* is not known yet: EffectControl life and followState, which emitter scripts and Unity
   parts, and its own AudioSource clips. The home PC has to read that with the probe in section 5 before the cues are
   final. Wherever a cue depends on it, I say so (`cut` only if followState; a `kill` that may be redundant).
2. **Gleaming Breath and Lucent Barrier have voices; Grand Codex has none.** `TTO1102:Sheep::Row6Voice@0x1E5EBD0` plays
   `GameAssets/characters/heroes/sheep/voices/<a or b>`: a `Random.Range(0, 2)` pick, `PlayOneShot` on the hero's `_audio`,
   volume 1 for the owner (0.75 for others).
   - Its only two callers (callers.py) are the Gleaming Breath and Lucent Barrier coroutines. They use revive1 / revive2 and reverse1 / reverse2.
   - None of the three coroutines calls `PlayOneShot` on a *sound*, and none has camera effects (no `AddCamereShake`; grepped in every Row6 coroutine).
   - So the only sounds besides the voices come from the effects' own AudioSources. What those are is unknown on this PC (item 1).
3. **No arcana style for the Sheep.** The catalog has no `heroes/sheep/arcana/` at all (the Wolf had Ronin copies). There
   is only one prefab per name, so there is no default-or-style question.
4. **Name collisions:**
   - `gleamingBreath` and `lucentBarrier` are each three things: the clip (cue key), the status, and a TTO prefab (the status's look, `effects/gleamingBreath`, `effects/lucentBarrier`). In cues, the prefab is always `tto/<name>`.
   - `grandCodex_verdict` is spawned at two places: at the codex spot on every verdict page (`CodexRead`), and at each speared enemy's chest (`VerdictFall`).
   - The TTO bundle also carries its own copies of BB's `revive` and `reverse` prefabs. Cues without `tto/` build BB's.
   - BB's `voices/` has `reverse1`, `reverse2`, `revive1`, `revive2`, `repel1`, `repel2`; `sounds/` has `repel` (the clip BB's `reverse` status effect plays on awake) but no `revive` or `reverse` sound. So the voice cues below are all `"voice"` (`voices/`).
   - `wardrobe_fx.py` needs the effect name `returnCast` in camelCase: `--probe returncast` finds nothing, while the inventory lists it in lower case.
5. **Target choices are real decisions** (section 4).
   - Gleaming Breath's target is a *dead ally*, so it can never be the Sheep herself.
   - Lucent Barrier's target can be herself: `Row6Begin` gets the target's direction only when `body != this.gameObject`, in `<RPC_lucentBarrier>d__262` state 0.
   - Grand Codex needs a ground spot. The Wolf decision gives 10 m ahead.

   My defaults: Gleaming Breath to an ally 10 m ahead, Lucent Barrier on herself, Grand Codex 10 m ahead.
6. **Grand Codex runs 20.7 s past its 1.4 s clip.** The page already keeps a skill's later cues in the idle tail
   (`index.html` comment above `isSkillMove`; `fxTick` runs on `FX.t`), so all ten pages and the close can be cued. With
   the วนซ้ำ toggle on, each loop restarts the cues, so they never get past 1.4 s.
7. **Free Cast / Return Cast** rolls at the start of the two passives' coroutines (`getFreeCast`, owner only). With Return
   Cast (431) learned (passives on) the proc is BB's `returnCast` effect at the hero, which the probe says is ready.
   Grand Codex never rolls in TTO1102, but does in TTO1109 (Return Cast only). See the questions.

---

## 1. Shared machinery (`TTO1102:Sheep`)

- `Row6Begin(command, mPos, tDir)@0x1E5D850`:
  - sets actionState `attack`;
  - puts the hero at mPos and `LookAt(mPos + vFlat(tDir))` when `|vFlat(tDir)|² > 0.0001`;
  - calls `BaseHero.PlayAnimation(command, 0.1)` with wrapMode Once and `moveSpeed 0`.

  The clip has the skill's name. `Row6End(command)@0x1E5DD70` sets `standby`, but only if the action is still this skill. That moment is the `cut` for a followState effect.
- `Row6Spawn(name, pos, rot, owned)@0x1E5E900` loads `GameAssets/characters/heroes/sheep/effects/<name>`
  (`Row6Prefab@0x1E5E730`, `Debug.LogError("Cannot find <name> effect")`).
  - `owned` true → `CharacterControl.createEffect` (EffectControl gets the hero, so followPosition / followState work).
  - false → a bare `Object.Instantiate`.

  Only the three `_cast` effects are owned.
- `Row6Mouth()@0x1E5E4A0` = the `Head` bone + 0.22 × forward − 0.04 × up (hero + 1.25 up when there is no Head bone).
- `Row6Hand(true)@0x1E5E360` = `mount_Hand_R` (else the hero).
- `Row6Chest(cc)@0x1E5DB80` = the collider's bounds centre (else position + up).
- On the page, from the Sheep's own rig and clips (`checks/fx_sheep_research/tto/head.py`, rig space z up, +x forward;
  about ±5 cm, the sign of x read from the hand reaching forward in the beam pose):
  - mouth at gleamingBreath 0.62 s: Head (0.127 fwd, 1.249 up) → **0.35 m ahead, 1.21 m up**;
  - right hand at lucentBarrier 0.58 s: **0.49 m ahead, 1.12 m up**, 0.04 m to the side.
- Chest: BB's `Sheep.prefab` CharacterController has centre y 0.8, height 1.5, radius 0.3 (the TTO prefab is assumed the
  same, not checked). So the chest is **0.8 m up**, the collider top 1.55 m.
- Status looks, `CharacterControl::AddSheepRow6Fx(status)@0x24AE620`, called from `<addStatus>d__481::MoveNext` at
  0x24FD426 / 0x24FD446 / 0x24FD486 (callers.py):
  - It instantiates `sheep/effects/<status>` with identity rotation, parented to the holder and named `<status>Fx`.
  - Scale: clamp(2 × radius, 1, 4) / lossyScale = 1 for the Sheep.
  - `lucentBarrier` sits at the bounds centre; `gleamingBreath` 0.25 m over the collider top (1.8 m); any other status (the third caller, `scriptureBind`) at the feet.
  - `RemoveSheepRow6Fx@0x24C2850` destroys it when the status ends (`removeStatus@0x24E2990`, 0x24E8B45-8D).

## 2. Per skill

### 2.1 Gleaming Breath (`gleamingBreath`, 1.7 s; skill 452, replaces Revive's landing)

The path: after Revive's cast bar, `StartGleamingBreath@0x1E5EEB0` starts `RPC_gleamingBreath(mPos, tDir, tID, sLv)` in
place of `RPC_revive_cast`. The cast bar itself is Revive's and is not part of this clip.

Coroutine `TTO1102:Sheep.<RPC_gleamingBreath>d__260::MoveNext@0x1E892F0`:

- **0.00** (state 0):
  - `Row6Body(tID)`; `Row6Begin("gleamingBreath")`, facing the target when there is one.
  - `start = Time.time`.
  - `Row6Voice("revive1", "revive2")`: a random pick.
  - Owner only: `getFreeCast("revive", sLv)` (`Sheep::getFreeCast@0x1E64E40`). It rolls `Random.Range(0, 100) < lckAdjust(24)` with Free Cast 2 (132), or 12 with Free Cast 1. On a proc with Return Cast (431), `RPC_returnCast@0x1E5B0F0` spawns `effects/returnCast` at the hero; without Return Cast, `RPC_freeCast@0x1E58D30` spawns `effects/freeCast`.
  - `Row6Spawn("gleamingBreath_cast", hero pos, hero rot, owned)`.
  - Then `Until(start + 0.62)`.
- **0.62** (state 1), if this is still the current Gleaming Breath (`step == mGleamStep` at +0x658):
  - `gleamingBreath_exhale`, world, at `Row6Mouth()` with the hero's rotation;
  - `StartCoroutine(BreathFly(mouth, body, sLv))`;
  - then `Until(start + 1.7)`.
- **BreathFly** (`TTO1102:Sheep.<BreathFly>d__261::MoveNext@0x1E72EA0`), first step in the same frame (0.62):
  - `to` = the target's chest. **With no target CharacterControl, `to = mouth + 3 × forward`**: the game's own no-target path.
  - `flight = clamp(|to − mouth| × 0.0625, 0.15, 0.6)`.
  - It spawns `gleamingBreath_wisp`, world, at the mouth, `LookRotation(to − mouth)`.
  - Every frame: `u = (now − t0) / flight`, position = `lerp(mouth, to, clamp01(u)) + up × u × 0.9 × (1 − u)` (a 0.225 m arc), facing its motion. `to` follows the target.
  - When the flight is over: `Destroy(wisp, 0.3)`.

  With no target it stops there. With a target:
  - `gleamingBreath_land`, world, at the target's **transform position** (feet), identity rotation;
  - on the revived player's client, `ReviveEvent(252 + sLv, ceil(0.9 × maxHP))`;
  - if alive, `RPC_AddStatus(gleamingBreath, 1, GleamingSeconds[rank − 1] = 15 s at Revive 2)`. Its look comes from `AddSheepRow6Fx` 0.25 m over the ally's collider, for 15 s.
- **1.70** (state 2): `Row6End("gleamingBreath")` (clip 1.7 s ✓).

For the target 10 m ahead (my default): mouth (0.35, 1.21) to chest (10, 0.8) is √(9.65² + 0.41²) = 9.66 m. Then
9.66 × 0.0625 = 0.604, clamped to 0.6 s. The land comes at 0.62 + 0.6 = **1.22 s** (the Bible's range 0.77-1.22 s ✓), and
the wisp is gone at 1.22 + 0.3 = 1.52 s.

```json
  "gleamingBreath": {
    "why": "TTO1102:Sheep.<RPC_gleamingBreath>d__260::MoveNext@0x1E892F0 (plans/fx_sheep/tto.md 2.1; the Sheep has no arcana style): 0: Row6Begin (Sheep::Row6Begin@0x1E5D850), voice revive1 / revive2 (Sheep::Row6Voice@0x1E5EBD0: Random.Range(0, 2), Voices/, vol 1 for the owner); the owner's Free Cast roll getFreeCast(\"revive\") (Sheep::getFreeCast@0x1E64E40: Random.Range(0, 100) < lckAdjust(24) with Free Cast 2; with Return Cast 431, passives on, RPC_returnCast@0x1E5B0F0: returnCast at the hero); gleamingBreath_cast owned at the hero (Row6Spawn@0x1E5E900 -> createEffect); Until 0.62: gleamingBreath_exhale at the mouth (Row6Mouth@0x1E5E4A0: Head + 0.22 forward - 0.04 up = 0.35 m ahead, 1.21 m up at 0.62 s from the Sheep's rig), BreathFly@0x1E72EA0 starts; the revived ally 10 m ahead (plans/fx_wolf/decisions.md: a target point 10 m ahead): flight clamp(9.66 m x 0.0625, 0.15, 0.6) = 0.6 s, gleamingBreath_land at its feet, identity rotation, at 1.22 s; Until 1.7: Row6End; left out: gleamingBreath_wisp (moved every frame mouth -> the ally's chest with an up-arc u x 0.9 x (1 - u), Destroy 0.3 s after landing) needs a scripted mover; the gleamingBreath status look over the ally (CharacterControl::AddSheepRow6Fx@0x24AE620, 0.25 m over its collider, 15 s at Revive 2) has no ally to sit on; the revive itself (ReviveEvent) draws nothing",
    "cues": [
    [0, "voice", "revive1|revive2"],
    [0, "fx", "returnCast", {"p": 0.24}],
    [0, "fx", "tto/gleamingBreath_cast"],
    [0.62, "fx", "tto/gleamingBreath_exhale", {"d": 0.35, "y": 1.21}],
    [1.22, "fx", "tto/gleamingBreath_land", {"d": 10}]
    ]
  },
```

Variant A, the game's own no-target path (BreathFly with no CharacterControl): drop the land cue. The wisp would then
fly 3 m ahead in 0.1875 s and be gone at 0.62 + 0.1875 + 0.3 = 1.11 s, but it is left out either way. That leaves the
cast, the exhale and the voice. If the wisp ever gets a mover, its cue is `[0.62, "fx", "tto/gleamingBreath_wisp", {"d": 0.35, "y": 1.21, "kill": 0.9}]`
(0.6 s flight + 0.3 s; `kill` 0.49 in variant A).

Possible `cut`: if the home PC's probe shows `gleamingBreath_cast` has EffectControl `followState`, add `{"cut": 1.65}`.
That is Row6End at 1.7 minus 0.05, the Wolf's convention (`bladeSurge_aura` cut 2.55 for 2.6) so that it also fires
when วนซ้ำ restarts the clip at 1.7.

### 2.2 Lucent Barrier (`lucentBarrier`, 1.4 s; skill 453, replaces Reverse's landing)

The path: after Reverse's cast bar, `StartLucentBarrier@0x1E5F100` starts `RPC_lucentBarrier` in place of
`RPC_reverse_cast`.

Coroutine `TTO1102:Sheep.<RPC_lucentBarrier>d__262::MoveNext@0x1E919A0`:

- **0.00** (state 0):
  - `Row6Body(tID)`. `Row6Begin("lucentBarrier")` faces the target **only when body exists and `body != this.gameObject`**; on herself it keeps tDir.
  - `start = Time.time`.
  - `Row6Voice("reverse1", "reverse2")`.
  - Owner: `getFreeCast("reverse", sLv)`, the same roll as 2.1.
  - `Row6Spawn("lucentBarrier_cast", hero pos, hero rot, owned)`.
  - `Until(start + 0.58)`.
- **0.58** (state 1), if still current (+0x65C) and the target's CharacterControl has hp ≥ 1:
  - `Row6Beam("lucentBarrier_beam", right hand, Row6Chest(target))` (`Sheep::Row6Beam@0x1E5D640`): world, at the hand, `LookRotation(chest − hand)`, then **`GetComponent<RabbitTracer>().Set(hand, chest)`** if the prefab has one.
  - `lucentBarrier_land`, world, at the target's chest, identity rotation.
  - On the Sheep's client: `t = chaAdjust(3)`. Then `RPC_AddStatus(target, 1114 reverse, sLv, t)` and `RPC_AddStatus(target, 1120 lucentBarrier, sLv, t, LucentReflectPct[sLv − 1] = 20)`.
  - Their looks:
    - `lucentBarrier` through AddSheepRow6Fx, at the chest, scale 1, for t;
    - `reverse` like BB's: `Effects/reverse` at `collider.bounds.center`, parented, scale `clamp(height + 0.2, 1, 3)` = 1.7, until removeStatus (BB `CharacterControl.cs:39770-39778`).

    TTO's addStatus case for reverse is not in the pseudo-C. The catalog has `sheep/effects/reverse`, so it is assumed the same. BB's `reverse` probes fine with `wardrobe_fx.py --probe reverse`: an Animation plus 3 StaticMesh rings, and a play-on-awake AudioSource with `sounds/repel`. It has **no EffectControl, so it needs a `kill`**.
  - Then `Until(start + 1.4)`.
- **1.40** (state 2): `Row6End` (clip 1.4 s ✓).
- `t = chaAdjust(3)`: 3 / 7 / 12 / 16 / 26 s at CHA 1 / 100 / 200 / 300 / 512 (Bible). My default is the tooltip's 3 s.
- Left out in every variant: `lucentBarrier_reflect`, `lucentBarrier_reflectBeam`, `lucentBarrier_panel`. They come from `CharacterControl::LucentReflectFx@0x24B5840`, whose only caller is `LucentReflect@0x24B5FD0` at 0x24B6177. That runs only when an attacker's hit is reflected, so it needs an attacker.

Default: **on herself** (a real game path). The land and both status looks sit on the hero, at 0.8 m.

```json
  "lucentBarrier": {
    "why": "TTO1102:Sheep.<RPC_lucentBarrier>d__262::MoveNext@0x1E919A0 (plans/fx_sheep/tto.md 2.2), cast on herself (Row6Begin turns to the target only when body != the Sheep): 0: Row6Begin, voice reverse1 / reverse2 (Sheep::Row6Voice@0x1E5EBD0), the owner's Free Cast roll getFreeCast(\"reverse\") (Sheep::getFreeCast@0x1E64E40, 24 % with Free Cast 2; Return Cast 431 -> returnCast at the hero, RPC_returnCast@0x1E5B0F0), lucentBarrier_cast owned at the hero; Until 0.58: lucentBarrier_land at her chest (Row6Chest@0x1E5DB80: collider centre, 0.8 m), identity rotation; chaAdjust(3) s (3 s at CHA 1, the tooltip's) of reverse and lucentBarrier on her: their looks, BB's Effects/reverse at the collider centre, scale clamp(1.5 + 0.2, 1, 3) = 1.7 (CharacterControl.cs:39770-39778, no EffectControl: killed with the status) and tto/lucentBarrier at the collider centre, scale 1 (CharacterControl::AddSheepRow6Fx@0x24AE620, destroyed by removeStatus@0x24E2990); Until 1.4: Row6End; left out: lucentBarrier_beam (right hand -> her chest, Row6Beam@0x1E5D640) needs RabbitTracer (TTO script, its Set(from, to) draws the line; not decompiled); lucentBarrier_reflect / _reflectBeam / _panel (CharacterControl::LucentReflectFx@0x24B5840) need an attacker's reflected hit",
    "cues": [
    [0, "voice", "reverse1|reverse2"],
    [0, "fx", "returnCast", {"p": 0.24}],
    [0, "fx", "tto/lucentBarrier_cast"],
    [0.58, "fx", "tto/lucentBarrier_land", {"y": 0.8}],
    [0.58, "fx", "reverse", {"y": 0.8, "scale": 1.7, "kill": 3}],
    [0.58, "fx", "tto/lucentBarrier", {"y": 0.8, "kill": 3}]
    ]
  },
```

- The beam, once RabbitTracer exists, on herself: from the hand (0.49 ahead, 1.12 up) to her chest (0, 0.8). That is
  (−0.49, −0.32), yaw 180, pitch atan(0.32 / 0.49) = 33° down: `[0.58, "fx", "tto/lucentBarrier_beam", {"d": 0.49, "y": 1.12, "rot": [33, 180, 0]}]`.
- Variant "ally 10 m ahead": the beam would be `{"d": 0.49, "y": 1.12, "rot": [1.9, 0, 0]}`, since (9.51, −0.32) gives
  atan(0.32 / 9.51) = 1.9° down. The land would be `{"d": 10, "y": 0.8}`, and the two status looks would sit at `{"d": 10, "y": 0.8}`
  over an empty spot (or be left out).
- Possible `cut`: if `lucentBarrier_cast` has followState, add `{"cut": 1.35}`.

### 2.3 Grand Codex (`grandCodex`, 1.4 s; skill 454, the only branch of `Sheep::DoRow6Skill@0x1E56590`)

The spot: `DoRow6Skill` takes the target or the aimed point. The flat offset is cut to 16 m (|v|² > 256); under 0.1 m
(|v|² < 0.01) it becomes 3 × forward. Then an 8 m raycast down from 3 m above puts it on the ground. The wardrobe uses
the Wolf decision, 10 m ahead (inside the 16 m cap), on the page's floor (y 0).

Coroutine `TTO1102:Sheep.<RPC_grandCodex>d__263::MoveNext@0x1E89740`:

- **0.00**:
  - `Row6Begin("grandCodex", mPos, toSpot)`, facing the spot.
  - `addTimeOut("grandCodex", agiAdjust(120))`.
  - `Row6Spawn("grandCodex_cast", hero, hero rot, owned)`.
  - **No voice** (Row6Voice has only the two callers above) and **no Free Cast** in TTO1102 (no `getFreeCast` call here).
  - `Until(start + 0.7)`.
- **0.70**: if still current (+0x660), `StartCoroutine(CodexOpen(mCodexGen, mPos + toSpot, vFlat(toSpot)))`. Then `Until(start + 1.4)`.
- **1.40**: `Row6End` (clip 1.4 s ✓).

`CodexOpen` (`TTO1102:Sheep.<CodexOpen>d__265::MoveNext@0x1E73940`) runs its first step in the 0.70 frame:

- `rot = CodexRotation(facing)` = `LookRotation(facing) × Euler(−35°, 0, 0)` (`Sheep::CodexRotation@0x1E563A0`).
  - The literal is 0xBF1C61AA = −0.6108652 rad = −35.0°.
  - The product order was read from the quaternion code: look × euler. So it is the hero's facing pitched up 35°: in Unity a negative x turns forward upward.
- `grandCodex_field`, world, at the spot, `LookRotation(facing)` = the hero's facing.
- `hover = spot + 2.6 up`. `grandCodex_book` is spawned world at `hover + 3 up` (5.6 m) with `rot`. `FlipPivot = book.Find("FlipPivot")`, and `t0 = Time.time` (0.70).
- **Every frame**:
  - The book's position = `hover + up × CodexBob(now − t0)`. The argument is from capstone: `subss xmm6, xmm7` at 0x1E74079, with xmm7 = `[this+0x78]` = t0.
  - `CodexBob(τ) = 0.12 sin(2.2 τ) + 3 (1 − clamp01(τ / 0.6))²` (`Sheep::CodexBob@0x1E55980`): it falls from 5.6 m to 2.6 m over 0.6 s, then bobs ±0.12 m.
  - FlipPivot's local rotation = `CodexFlipAngle(readAt − now)` (`@0x1E55A00`). With s = 1 − clamp01(left / 0.45), that is Euler(0, 0, −180° × (3s² − 2s³)): a page turns over the last 0.45 s before each read, then snaps back to identity at the read.
- **Page k = 0..9 at `t0 + 2(k + 1)`**, i.e. clip time 0.7 + 2(k + 1) = 2.7, 4.7 … 20.7. The kind is `CodexPageNames[k % 3]` = psalm (heal), seal (slow), verdict (spears), from `Sheep::.cctor@0x1E5F5A0` and the order in the Bible.

  `Sheep::CodexRead(k % 3, spot, bookAt)@0x1E55B60` spawns two effects:
  - `grandCodex_page_<kind>`, world, at the book's current position, identity;
  - `grandCodex_<kind>`, world, at the spot, identity.

  Then:
  - psalm: the heals (no effect).
  - seal: `scriptureBind` on enemies. Its look comes from AddSheepRow6Fx at the enemy's feet: left out.
  - verdict: `VerdictFall` for the 3 nearest enemies (`<VerdictFall>d__269::MoveNext@0x1E9ECD0`). After `Waits.Get(0.08 i)` it spawns `grandCodex_spear` at the book, flies it 0.3 s to the enemy's chest, then `Destroy(spear, 0.1)`, a `hit()`, and `grandCodex_verdict` at the enemy's chest. These are on enemies: left out.

  The book's height at each read is 2.6 + 0.12 sin(2.2 × 2(k + 1)): 2.486, 2.670, 2.671, 2.486, 2.599, 2.715, 2.531, 2.528, 2.714, 2.602.
- **20.70**, after page 9 in the same frame (k reaches 10, the loop ends): `grandCodex_close`, world, at the book's position with `rot`, then `Destroy(book, 0.1)`. The book is gone at 20.8, which is 20.1 s after it was spawned.

  Only a change of `mCodexGen` stops it earlier (+0x664, bumped in `Sheep::OnDisable@0x1E56E70`). Destroying the book there is the only kill; the field's end is its own EffectControl life (unknown here).
- Sums checked: 0.7 + 2 = 2.7, 0.7 + 20 = 20.7, and 20.7 + 0.1 − 0.7 = 20.1. The spears (left out) would be 6.7 + 0.3 = 7.0, 13.0, 19.0 s plus 0.08 / 0.16, which matches the Bible's hits.

```json
  "grandCodex": {
    "why": "TTO1102:Sheep.<RPC_grandCodex>d__263::MoveNext@0x1E89740 (plans/fx_sheep/tto.md 2.3), the codex spot 10 m ahead on the ground (plans/fx_wolf/decisions.md; DoRow6Skill@0x1E56590 caps it at 16 m): 0: Row6Begin facing the spot, grandCodex_cast owned at the hero, no voice and no Free Cast roll; Until 0.7: CodexOpen@0x1E73940 (t0 = 0.7): grandCodex_field at the spot in the hero's facing, grandCodex_book at the spot + 2.6 up rotated CodexRotation@0x1E563A0 = facing x Euler(-35, 0, 0) (the game drops it from 5.6 m over 0.6 s, then bobs 0.12 sin(2.2 t), CodexBob@0x1E55980, and turns its FlipPivot page -180 deg over the 0.45 s before each read, CodexFlipAngle@0x1E55A00: here it hangs still at 2.6 m), destroyed 0.1 s after the close (kill 20.1); Until 1.4: Row6End; page k = 0..9 at 0.7 + 2(k + 1) s, kind psalm / seal / verdict by k % 3 (Sheep::.cctor@0x1E5F5A0), each spawning grandCodex_page_<kind> at the book (its height at that time) and grandCodex_<kind> at the spot, identity rotation (Sheep::CodexRead@0x1E55B60); 20.7: grandCodex_close at the book, then Destroy(book, 0.1); left out: grandCodex_spear (book -> each of the 3 nearest enemies, 0.3 s, VerdictFall@0x1E9ECD0) and grandCodex_verdict at each speared enemy's chest, the scriptureBind look on slowed enemies (CharacterControl::AddSheepRow6Fx@0x24AE620): all on enemies; the heals draw nothing",
    "cues": [
    [0, "fx", "tto/grandCodex_cast"],
    [0.7, "fx", "tto/grandCodex_field", {"d": 10}],
    [0.7, "fx", "tto/grandCodex_book", {"d": 10, "y": 2.6, "rot": [-35, 0, 0], "kill": 20.1}],
    [2.7, "fx", "tto/grandCodex_page_psalm", {"d": 10, "y": 2.486}],
    [2.7, "fx", "tto/grandCodex_psalm", {"d": 10}],
    [4.7, "fx", "tto/grandCodex_page_seal", {"d": 10, "y": 2.67}],
    [4.7, "fx", "tto/grandCodex_seal", {"d": 10}],
    [6.7, "fx", "tto/grandCodex_page_verdict", {"d": 10, "y": 2.671}],
    [6.7, "fx", "tto/grandCodex_verdict", {"d": 10}],
    [8.7, "fx", "tto/grandCodex_page_psalm", {"d": 10, "y": 2.486}],
    [8.7, "fx", "tto/grandCodex_psalm", {"d": 10}],
    [10.7, "fx", "tto/grandCodex_page_seal", {"d": 10, "y": 2.599}],
    [10.7, "fx", "tto/grandCodex_seal", {"d": 10}],
    [12.7, "fx", "tto/grandCodex_page_verdict", {"d": 10, "y": 2.715}],
    [12.7, "fx", "tto/grandCodex_verdict", {"d": 10}],
    [14.7, "fx", "tto/grandCodex_page_psalm", {"d": 10, "y": 2.531}],
    [14.7, "fx", "tto/grandCodex_psalm", {"d": 10}],
    [16.7, "fx", "tto/grandCodex_page_seal", {"d": 10, "y": 2.528}],
    [16.7, "fx", "tto/grandCodex_seal", {"d": 10}],
    [18.7, "fx", "tto/grandCodex_page_verdict", {"d": 10, "y": 2.714}],
    [18.7, "fx", "tto/grandCodex_verdict", {"d": 10}],
    [20.7, "fx", "tto/grandCodex_page_psalm", {"d": 10, "y": 2.602}],
    [20.7, "fx", "tto/grandCodex_psalm", {"d": 10}],
    [20.7, "fx", "tto/grandCodex_close", {"d": 10, "y": 2.602, "rot": [-35, 0, 0]}]
    ]
  }
```

Notes:

- The game's identity rotations on the page effects and spot effects are world-fixed. The page draws them in the hero's
  facing, the same approximation as the Wolf's Wind Bound Domain: it only turns their textures.
- A `cut` of 1.35 on `grandCodex_cast` is needed only if the probe shows followState.
- If the field's own EffectControl life turns out shorter or longer than the book's 20.1 s, leave it: the game never
  destroys the field by code.

## 3. Effect list (all 24 Sheep TTO prefabs in the catalog, `gameassets/characters/heroes/sheep/effects/`)

| Prefab | Spawned by | Cued |
|---|---|---|
| gleamingBreath_cast | RPC_gleamingBreath 0, owned | yes |
| gleamingBreath_exhale | RPC_gleamingBreath 0.62, mouth | yes |
| gleamingBreath_wisp | BreathFly, moved by code | left out: needs a mover |
| gleamingBreath_land | BreathFly, at the revived ally | yes (10 m variant) |
| gleamingBreath (status look) | AddSheepRow6Fx on the revived ally | left out (no ally) - question |
| lucentBarrier_cast | RPC_lucentBarrier 0, owned | yes |
| lucentBarrier_beam | Row6Beam 0.58 | left out: needs RabbitTracer |
| lucentBarrier_land | RPC_lucentBarrier 0.58, target chest | yes (on herself) |
| lucentBarrier (status look) | AddSheepRow6Fx | yes (on herself) |
| lucentBarrier_reflect / _reflectBeam / _panel | LucentReflectFx (a reflected hit) | left out: needs an attacker |
| grandCodex_cast | RPC_grandCodex 0, owned | yes |
| grandCodex_field, grandCodex_book, grandCodex_close | CodexOpen | yes (book static) |
| grandCodex_page_psalm / _seal / _verdict | CodexRead, at the book | yes |
| grandCodex_psalm / _seal / _verdict | CodexRead, at the spot (verdict also VerdictFall at each hit) | yes (spot only) |
| grandCodex_spear | VerdictFall, flies to enemies | left out: on enemies |
| scriptureBind (status look) | AddSheepRow6Fx on slowed enemies | left out: on enemies |

BB effects the TTO cues use (built by `wardrobe_fx.py` on either PC):

- `returnCast`: EffectControl life 1, followPosition, ImageEmitter + LineEmitter + RingEmitter. Ready; the inventory lists it as `returncast`, Sheep.cs:11651.
- `reverse`: Animation + 3 StaticMesh + AudioSource `repel`. Built by the probe; it is not in `fx_inventory.md` because CharacterControl spawns it.

**Parts:**

- Unknown for all 24 TTO prefabs: they are not on this PC.
- The page already has these parts that TTO effects use: the old emitters (EffectControl, ImageEmitter, RingEmitter, LineEmitter), `fxparts/groundhug.js`, `arcribbon.js`, `groundfollower.js`, `shuriken.js`, `mesh.js` (Animation / StaticMesh), `trail.js`, `vortex.js`, `emblem.js` and `control.js`.
- New, known from the code:
  - **RabbitTracer** (TTO.Game TypeDefIndex 3914: `life, travel, width, head`, a `LineRenderer`; `Set@0x1E6F280`, `Update@0x1E6F420`, `Apply@0x1E6EF20`, none in `pseudo/`), for the beam. It is a Ghidra job first, like GroundHug was.
  - **A codex mover** for the book's drop, bob and FlipPivot page turn (code in CodexOpen, not in the prefab).
  - **A path mover** for the wisp (BreathFly).

  A cue option such as "move from A to B over t with an up-arc" would cover the wisp and, later, the spear.
- Possibly new, depending on the probe: any TTO script the page lacks (`HelixRibbonEmitter`, `BoltEmitter`,
  `GroundConformParticles` exist in TTO.Game), a real Mesh on the book (the TTO build prints "a Mesh reference ... not
  exported" for it, `wardrobe_fx_tto.py`), and LineRenderer.

## 4. Sounds and voices

- Voices (cue kind `"voice"` = `voices/`): `revive1` 0.500 s, `revive2` 1.088 s, `reverse1` 0.585 s, `reverse2` 1.198 s.
  - In the TTO catalog they are `gameassets/characters/heroes/sheep/voices/revive1` etc., in the same bundle as the effects.
  - In BB's rip they are `C:\Users\Jump\Desktop\12tails\RippedAssets\ExportedProject\Assets\Resources\gameassets\characters\heroes\sheep\voices\revive1.wav` etc. The lengths above are BB's WAVs.
  - Whether TTO's are the same recordings is **not checked** (no bundle here). The Wolf's TTO clips all matched BB's to the millisecond. The home PC can compare lengths.
- No new Sheep sounds in TTO: the catalog's `sheep/sounds/` are BB's 36 names. The TTO effects' own AudioSource clips are
  unknown here. `wardrobe_fx_tto.py` copies them from BB's rip by name (`rip_wav`) and prints "missing sounds" for any
  TTO-only clip.
- The `reverse` status look plays `sounds/repel` (2.048 s) on awake.

## 5. For the home PC (build)

- First read the prefabs (writes nothing):

  ```
  uv run --no-project --with UnityPy --with pillow --with imageio-ffmpeg python -I pipeline/wardrobe_fx_tto.py sheep --probe gleamingBreath_cast,gleamingBreath_exhale,gleamingBreath_wisp,gleamingBreath_land,gleamingBreath,lucentBarrier_cast,lucentBarrier_beam,lucentBarrier_land,lucentBarrier,grandCodex_cast,grandCodex_field,grandCodex_book,grandCodex_close,grandCodex_page_psalm,grandCodex_page_seal,grandCodex_page_verdict,grandCodex_psalm,grandCodex_seal,grandCodex_verdict
  ```

  Check, for each prefab:
  - the comp types against the parts above;
  - EffectControl `followState` (then add the `cut`s in section 2);
  - the book's and the field's life;
  - any "Mesh reference" warning;
  - the AudioSource clips.
- Then, once the cues are in `wardrobe/fx_cues/sheep.json`: `wardrobe_fx_tto.py sheep` builds every `tto/` name in them
  (its `cue_tto`), so `SKILL_FX["sheep"]` is optional. Add it only to pre-build the left-out ones: the wisp, the beam,
  the spear, scriptureBind, and the three reflect prefabs.
- `wardrobe_fx.py sheep` (either PC) builds `returnCast`, `reverse` and the four voices.

## 6. Open questions for the user

1. **Gleaming Breath's target:**
   - (B, my default) a revived ally 10 m ahead: the land at 1.22 s;
   - (A) the game's own no-target path: no land.

   Also: show the 15 s `gleamingBreath` buff look over the empty spot 10 m ahead? My default is no.
2. **Lucent Barrier's target:**
   - herself (my default: the land, the barrier and the Reverse look on the hero);
   - an ally 10 m ahead (the effects 10 m away, the beam pointing there).
3. **Lucent Barrier's time** is `chaAdjust(3)`: 3 s (the tooltip's, my default), or a CHA you pick (7 s at CHA 100, 12 at 200).
4. **Free Cast / Return Cast:**
   - Roll `returnCast` at 24 % on Gleaming Breath and Lucent Barrier (Return Cast on, as passives are on)? My default is yes. It should match whatever the BB Sheep reports pick for Revive / Reverse.
   - Grand Codex rolls too in TTO's 09/11 client (`FreeCastNeedsReturnCast` includes grandCodex, Bible), but never in TTO1102. Add it?
5. **Should the two passive tiles become sequences** with Revive's / Reverse's cast bar (`cast1 > cast2` held, then
   `gleamingBreath` / `lucentBarrier` in place of the cast's release), as the game plays them? That is a `SEQ` change in
   `index.html`, not a cue change.
6. **Grand Codex spot:** 10 m ahead (the Wolf rule) puts a 12 m circle and a book 2.6 m up 10 m away. Does it fit the
   page's camera? 3 m ahead (the game's fallback when you aim at your own feet) is the other option.

## Verification (2026-11-10)

An independent re-trace of every cue's time, name, place and every "left out" reason. Sources:
- `DecompiledSource_TTO_2026-11-02\pseudo\Sheep.c` and `CharacterControl.c`;
- the TTO1102 catalog (`tools\aa_catalog.py` over `client\aa\catalog.bin`);
- BB's rip (voices, sounds, `Sheep.prefab`) and BB `CharacterControl.cs`;
- `head.py`, re-run on `wardrobe/data/sheep`.

The numbers are re-derived by `checks/fx_sheep_research/verify/tto_parts_numbers.py`, which exits OK.

**Corrections: none needed in the text.** Every claim below was checked against the line that proves it.

**Gleaming Breath (`<RPC_gleamingBreath>d__260::MoveNext`, Sheep.c:9979-10136):**
- State 0:
  - `Row6Begin` faces `body.position - mPos` when the body exists, else `tDir`.
  - `start = Time.time`, then `Row6Voice(revive1, revive2)`.
  - `getFreeCast("revive")` only when `mChar+0x182` (isMine) is set.
  - `Row6Spawn(gleamingBreath_cast, ..., owned 1)`, then `Until(start + 0.62)`.
- State 1, if `step == +0x658`: the exhale is spawned world at `Row6Mouth` with the hero's rotation, `BreathFly` starts,
  then `Until(start + 1.7)`.
- State 2: `Row6End`.
- `Until(start + t)` takes an absolute time, as the report says.
- BreathFly (Sheep.c:1-374):
  - With no CharacterControl, `to = from + 3 x forward`.
  - `flight = clamp(|to - from| x 0.0625, 0.15, 0.6)`.
  - The arc is `u x 0.9 x (1 - u)`; then `Destroy(wisp, 0.3)`.
  - With no target it returns. Else it spawns the land at `tc.transform.position` with identity rotation.
  - Then, on the target's own client, `ReviveEvent(sLv + 0xFC)` and, if HP >= 1 and not `dead`,
    `RPC_AddStatus(0x45F = 1119, 1, GleamingSeconds[clamp(sLv, 1, 2) - 1])`.
- `Sheep::.cctor`: `GleamingSeconds = {10, 15}`, `LucentReflectPct = {10, 20}`, `CodexPageNames = {psalm, seal, verdict}`.
- `Row6Mouth` = Head + 0.22 forward - 0.04 up (else hero + 1.25 up).
- `head.py` at gleamingBreath 0.62 s gives Head (0.127, 1.249), so the mouth is (0.347, 1.209).
- The flight is 9.66 x 0.0625 = 0.604, clamped to 0.6, so the land comes at 1.22 s. The Bible's 0.77-1.22 s
  (0.62 + 0.15 to 0.62 + 0.6) matches.

**Lucent Barrier (`<RPC_lucentBarrier>d__262::MoveNext`, Sheep.c:12564-12802):**
- State 0:
  - `Row6Begin` turns to the body only when `body != this.gameObject` (`op_Inequality`).
  - `Row6Voice(reverse1, reverse2)`; `getFreeCast("reverse")` (isMine).
  - `Row6Spawn(lucentBarrier_cast, owned 1)`; `Until(start + 0.58)`.
- State 1, if `step == +0x65C` and target HP >= 1:
  - `Row6Beam(lucentBarrier_beam, Row6Hand(1) = mHandR, Row6Chest)`. `Row6Beam` calls `GetComponent<RabbitTracer>().Set`.
  - `lucentBarrier_land` at `Row6Chest` with identity rotation.
  - Owner only: `chaAdjust(3)`, then `RPC_AddStatus(0x45A = 1114)` and
    `RPC_AddStatus(0x460 = 1120, ..., LucentReflectPct[sLv - 1])`.
  - Then `Until(start + 1.4)`.
- `1114` = reverse is confirmed by the Bible (`sheep-skill-reference.md:760`: a repel apply calls `removeStatus(1114)`).
- `AddSheepRow6Fx` (CharacterControl.c:29204):
  - `lucentBarrier` at `bounds.center`;
  - `gleamingBreath` at `center.y + extents.y + 0.25` = 0.8 + 0.75 + 0.25 = 1.8;
  - others at the position;
  - scale `clamp(2 x radius x lossy, 1, 4) / lossy` = 1.
- BB `CharacterControl.cs:39770` creates the reverse look at `collider.bounds.center`. `:39778` sets the scale to
  `clamp(height + 0.2, 1, 3)`.
- BB `Sheep.prefab` CharacterController: height 1.5, radius 0.3, centre y 0.8 (prefab lines 783-789).
- `head.py` at lucentBarrier 0.58 s: mount_Hand_R (0.486, -0.042, 1.115). The beam pitch atan(0.315 / 0.486) = 33°; the
  ally variant atan(0.32 / 9.51) = 1.9°.
- The page reads `rot` as Unity's YXZ Euler (`index.html:3122-3123`), so `[33, 180, 0]` points back and down.

**Grand Codex (`<RPC_grandCodex>d__263` Sheep.c:10153-10274, `<CodexOpen>d__265` :392-716):**
- The coroutine:
  - `Row6Begin(mPos, toSpot)`, `addTimeOut(agiAdjust(120))`, `Row6Spawn(grandCodex_cast, owned 1)`, `Until(start + 0.7)`.
  - No `Row6Voice` and no `getFreeCast`. `Row6Voice` has exactly two call sites in Sheep.c (:10053, :12765).
- 0.7 s: `CodexOpen(mCodexGen, mPos + toSpot, vFlat(toSpot))`, then `Until(1.4)`, then `Row6End`.
- CodexOpen:
  - The field is spawned world at the spot with `LookRotation(facing)`; hover = spot + 2.6 up.
  - The book is spawned at hover + 3 up with `CodexRotation`; `t0 = Time.time`.
  - `readAt = t0 + 2(k + 1)` for k < 10.
  - Each frame: book = hover + up x `CodexBob`, and FlipPivot = `CodexFlipAngle(readAt - now)`.
  - At each read: FlipPivot back to identity, then `CodexRead(k % 3, spot, book position)`.
  - After k = 10: `grandCodex_close` at the book with `rot`, then `Destroy(book, 0.1)`.
- `CodexRotation` is `LookRotation(facing) x FromEulerRad(0xBF1C61AA = -35°, 0, 0)`. The product's x term is
  `l.w*e.x + l.x*e.w + l.y*e.z - l.z*e.y`, which is look x euler.
- `CodexBob` = `0.12 x FUN_180308bd0(2.2 t) + 3(1 - clamp01(t / 0.6))^2`. `FUN_180308bd0` is sin: TTO's Penguin hop uses
  it as `0.15 x f(u x pi)` for u in 0..1 (Penguin.c:1083).
- The heights 2.486 ... 2.602 re-compute exactly.
- `CodexRead` (Sheep.c:32812) spawns `grandCodex_page_<kind>` at `bookAt` and `grandCodex_<kind>` at the spot, both world
  with identity rotation.

**Names and folders:**
- BB `voices/` has `revive1` (0.500 s), `revive2` (1.088), `reverse1` (0.585) and `reverse2` (1.198); there is no
  `revive` or `reverse` sound.
- `sounds/` has 36 names, `repel` among them (2.048 s).
- The TTO catalog:
  - 87 Sheep effects: 24 TTO-only, exactly the report's list, and the rest BB's (`revive`, `reverse`, `returncast`,
    `freecast` included).
  - No `heroes/sheep/arcana/`; 36 sounds.
  - `voices/revive1` sits in the same bundle `325c14de...` as the effects.
- `returnCast`: TTO's `RPC_returnCast@0x1E5B0F0` loads `effects/returnCast` at the hero (Sheep.c:31168). BB
  `Sheep.cs:11651` loads it, and `fx_inventory.md:752` lists it as `returncast` (ready).
- `getFreeCast` (Sheep.c:28602) checks 0x84 (Free Cast 2) for `lckAdjust(24)`, else 0x83 for 12, and 0x1AF (Return Cast)
  to choose between `RPC_returnCast` and `RPC_freeCast`.
- The Bible's line 656 confirms that TTO1109 rolls Grand Codex too (Return Cast only).

**Notes (not errors in the report):**
- The researcher's relayed summary says "3 are left out for missing parts". The report's table has 2:
  `gleamingBreath_wisp` and `lucentBarrier_beam`. The count is 16 cued + 2 parts + 5 enemy / attacker + 1 question = 24.
  The report body is right.
- TTO spawns `returnCast` with a bare `Object.Instantiate` (Sheep.c:31168 + 70), not `createEffect`, so its
  EffectControl's followPosition has no owner in the game. The hero stands still for the whole skill, so the cue is
  unaffected.
- The book's height at a read is the previous frame's bob (positions are written before the read check). The difference
  is under a frame and does not matter.

**Unresolved (not disproved, cannot be checked on this PC):**
- Every prefab's contents: EffectControl life and followState (so the possible `cut`s), parts, AudioSources, and the
  book's Mesh. There is no TTO effects bundle here, as the report says (section 5's probe on the home PC).
- That TTO's `addStatus` case for `reverse` matches BB's look (position, scale 1.7). That case is not in the pseudo-C.
- That TTO's `Sheep.prefab` CharacterController matches BB's (centre 0.8, height 1.5).
- That TTO's four voices are the same recordings as BB's.
- The mouth and hand positions carry head.py's stated ±5 cm (the rig's +x is taken as forward).

## Probed 2026-11-10 (office PC, TTO's 2026-11-09 bundles; agent "tto", Build phase)

Read from `tto_assets\2026-11-09` (the office's own decrypted TTO install) with
`uv run --no-project --with UnityPy --with pillow --with imageio-ffmpeg python -I pipeline/wardrobe_fx_tto.py sheep --probe`
(all 24 prefabs, now `SKILL_FX["sheep"]`). Probe outputs and helper scripts are in `checks/fx_sheep_build/tto/`
(`summary.txt` lists every node and part). Built into `wardrobe/data/sheep/fx.json`: 24 `tto/` effects, 26 `tto_`
materials, 15 textures, 14 sounds.

### Per prefab (EffectControl life + afterLife and follow flags; what draws; sounds)

| Prefab | EffectControl | Parts | AudioSource (play on awake) |
|---|---|---|---|
| gleamingBreath_cast | 1.7 + 0.5, followPosition, **followState** | GroundHug (Consecration), 3 ImageEmitters (Prayer, Hand, Halo), 2 ParticleSystems (Gather, Motes) | castEffect 0.7 |
| gleamingBreath_exhale | 0.9 + 0.4 | 2 ImageEmitters, PS Mist (stretched), PS Sparks (**Collision**, Force) | holyLight_start 0.6 |
| gleamingBreath_wisp | 1.4 + 0.5 | 3 ImageEmitters, 2 **TrailRenderers** (Trail 0.4 s, TrailCore 0.28 s), 3 PS (Orbit local, Sparkle world, Feathers) | none |
| gleamingBreath_land | 2.8 + 0.6 | 3 GroundHugs (seal, echo, ring), 19 ImageEmitters (pillar, crown, two 6-feather seraph wings), PS Feathers | heal 0.9, holyArmor_ring 0.6 |
| gleamingBreath (status look) | **none** (removeStatus destroys it) | 4 PS (Halo flat, Glow, Motes, Feathers; 2 loop) | none |
| lucentBarrier_cast | 1.4 + 0.4, followPosition, **followState** | ImageEmitter + LineEmitter (Cast), PS Shards (**mesh** sheepRow6_shard), PS Motes, 3 ImageEmitters (hex sigil, prism, push) | castEffect 1.0 (on Cast), revert 0.6 |
| lucentBarrier_beam | **none** (RabbitTracer's Destroy(life + 0.05)) | **LineRenderer** + **RabbitTracer** (life 0.4, travel 0.08, width 0.34, head = Head), Head/Glint ImageEmitter | none |
| lucentBarrier_land | 1.4 + 0.4 | PS Inrush (mesh shard), PS Shell (mesh **sheepRow6_prismShell**, Prism Veil), 3 ImageEmitters, PS PrismDust | iceShield 0.7 |
| lucentBarrier (status look) | **none** | 4 PS: Shell, Shimmer (loop 2.8 s; both prism-shell meshes), Orbit (shard meshes), Seal (flat) | none |
| lucentBarrier_reflect | 0.7 + 0.3 | ImageEmitter, PS Shards (mesh), PS Sparks (Collision) | shieldReflect 0.55 |
| lucentBarrier_reflectBeam | **none** | LineRenderer + RabbitTracer (life 0.3, travel 0.05, width 0.18, no head) | none |
| lucentBarrier_panel | 0.6 + 0.2 | 4 ImageEmitters | none |
| grandCodex_cast | 1.4 + 0.5, followPosition, **followState** | 2 GroundHugs, PS Glyphs (UV sheet), 3 ImageEmitters, PS Sparks (Collision) | worldEncarta 0.7 |
| grandCodex_field | **20.6 + 0.6** | 6 GroundHugs (Circle, Boundary, InnerSanctum, CounterScript, Glow, Open), PS Motes (20 s) | edenSanctuary_ring 0.7 |
| grandCodex_book | **none** (CodexOpen's Destroy(book, 0.1)) | **Mesh "Codex"** (13,046 vertices, 7 submeshes, 7 Standard materials), child **FlipPivot** (its own mesh, 754 vertices, manuscript material), Glow / OrbitA / OrbitB / Cone ImageEmitters, PS Astrolabe (flat, local), PS Glyphs (world) | none |
| grandCodex_close | 1.4 + 0.4 | 2 ImageEmitters, PS Glyphs, PS Dust | bookBash_hit 0.8 |
| grandCodex_page_psalm / _seal / _verdict | 1.2 + 0.4 each | 3 ImageEmitters, PS Glyphs (the same build in each) | none |
| grandCodex_psalm | 1.8 + 0.5 | 3 GroundHugs, PS Rise | heal 0.8 |
| grandCodex_seal | 1.6 + 0.5 | 3 GroundHugs, PS Chains | seal 0.8, lightBind 0.5 |
| grandCodex_verdict | 1.1 + 0.3 | 3 ImageEmitters, PS VerdictSplinters (mesh shard) | divinitySpear_ring 0.8 |
| grandCodex_spear | 1.0 + 0.3 | 3 ImageEmitters (shaft, cross shaft, tip), TrailRenderer | divinitySpear 0.6 |
| scriptureBind (status look) | **none** | PS Ring (flat), PS Glyphs (loop) | none |

- **Sounds.** All 14 are BB's recordings. Each is the same length as the rip's WAV to the millisecond (`sounds.py`).
  - 11 come from the Sheep's own `sounds/`.
  - `holyArmor_ring` comes from the Wolf's, `iceShield` from the Penguin's, `shieldReflect` from the Whale's. `rip_wav`'s
    search finds them in BB's rip.
  - None is TTO-only. The build can now also export a TTO-only clip from the bundle (FMOD through UnityPy), should a
    later class need one.
- **Materials and shaders.**
  - Three are TTO's own procedural shaders, disassembled from their D3D11 bytecode (`dxbc_*.txt`):
    - `TTO/Sheep/Celestial Ring` (`sheepRow6_celestial`, no texture): a star-chart disc drawn from the uv, orbiting at
      `_Speed` 0.12;
    - `TTO/Sheep/Celestial Ray` (`sheepRow6_ray`, no texture): a soft beam along u;
    - `TTO/Sheep/Prism Veil` (`sheepRow6_veil`): a fresnel shell over the prism lattice, with a band scrolling up.
  - The book uses Unity's `Standard` (metallic, smoothness, emission).
  - The Sparks use `Particles/Standard Unlit` (`tto_Point`: Fade, HDR `_Color` 6.35).
  - Everything else is Unity's legacy Additive / Additive (Soft) / Alpha Blended.
- **Unity parts the page lacked:**
  - LineRenderer;
  - Unity 5.5+'s TrailRenderer;
  - mesh particles (shuriken m_RenderMode 4): `sheepRow6_shard` (30 vertices) and `sheepRow6_prismShell` (240 vertices,
    with normals);
  - a real MeshFilter mesh (the book);
  - ParticleSystem World collision (3 Sparks systems).

  No Sheep prefab has HelixRibbonEmitter, BoltEmitter or GroundConformParticles, and none has ArcRibbon or GroundFollower.
  The rest is what the page already drew (GroundHug, Image / Line emitters, shuriken).

### Corrections to the report above

- `gleamingBreath_cast`, `lucentBarrier_cast` and `grandCodex_cast` all have **followState**. So the possible cuts in
  2.1, 2.2 and 2.3 are real: `cut` 1.65, 1.35 and 1.35 (Row6End at 1.7 / 1.4 / 1.4, minus the Wolf's 0.05).
- The `gleamingBreath`, `lucentBarrier` and `scriptureBind` status looks and the book have **no EffectControl**. They
  live until the code destroys them.
  - `lucentBarrier`'s cue `kill 3` is needed, as written.
  - The book's `kill 20.1` is now also done by its part (Sheep.CodexOpen, below). The cue's kill is harmless but no
    longer needed.
- `grandCodex_field`'s own life is 20.6 + 0.6 s. Spawned at 0.7, it starts its after-life at 21.3 and is gone at 21.9,
  which is 0.6 s after the close at 20.7. No change to 2.3's note: the game never destroys it.
- `lucentBarrier_beam` and `gleamingBreath_wisp` are no longer "left out". RabbitTracer and the wisp's flight
  (Sheep.BreathFly) are built (below).
- RabbitTracer, decompiled (TTO1102, `RabbitTracer.c`): Set@0x1E6F280, Update@0x1E6F420, Apply@0x1E6EF20, .ctor@0x1E6F4A0.
  Its constants were read at their addresses (`consts.py`).
  - h = clamp01(t / travel); f = clamp01((t - travel) / max(0.01, life - travel)).
  - The line runs from lerp(from, to, clamp01(0.85 f²)) to lerp(from, to, h).
  - Widths: 0.5 w at the start and w at the end, with w = (1 - 0.7 f) x width. Both colours' alpha x (1 - f).
  - The head node sits at the line's head. The object is destroyed life + 0.05 s after Set.

  So the beam shoots from the hand to the chest in 0.08 s. Then its tail catches up while it thins and fades. It is
  gone at 0.45 s.

### Cue changes the tto/ entries need (for the cue file's owner)

A new cue option, `to`, drives the two code-driven parts. It is [x, y, d]: metres right, up and ahead of the hero, the
point the game aims at. index.html must pass it through (see the shared changes).

```json
[0.62, "fx", "tto/gleamingBreath_wisp", {"d": 0.35, "y": 1.21, "to": [0, 0.8, 10]}]
[0.58, "fx", "tto/lucentBarrier_beam", {"d": 0.49, "y": 1.12, "rot": [33, 180, 0], "to": [0, 0.8, 0]}]
```

- The wisp needs no `kill`. Its part destroys it 0.3 s after the 0.6 s flight: 0.9 s after spawning, 1.52 s clip time.
  Without `to` it takes the game's no-target path (3 m ahead, 0.1875 s).
- The beam goes on herself (decision 1). Its root needs no `kill`: RabbitTracer destroys it at 0.45 s. Without `to` it is
  not drawn.
- `cut`s: `tto/gleamingBreath_cast` `{"cut": 1.65}`, `tto/lucentBarrier_cast` `{"cut": 1.35}`, `tto/grandCodex_cast`
  `{"cut": 1.35}`. All three have followState.
- `tto/grandCodex_book`: keep `{"d": 10, "y": 2.6, "rot": [-35, 0, 0]}`; `kill 20.1` is optional. Here y is the hover
  height. The part adds the drop from 3 m higher and the bob, and turns the page before each read.
