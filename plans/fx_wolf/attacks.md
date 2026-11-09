# Wolf effects + sounds research: Normal Attack, Charge Attack, Blade Fang, Blade Song

Scope: nAttack1-4, cAttack1-3, bladeFang1-3, bladeSong3-4 (researcher "attacks", 2026-11-09). Research only; nothing
in the repo was changed. Source = `D:\12tails\DecompiledSource\Wolf.cs` (`:line`); behaviour cross-checked with
`12t_reference\wolf-skill-reference.md`. Temporary read-only probes: `checks\fx_wolf_research\attacks\` (`probe.py`
= parts / EffectControl / AudioSource of every effect named here; `probe_dust2.py` = the hero prefab's `dust_forward`
field; `cond.sh` = a condensed view of a line range).

## Read this first: two blockers for the editor

1. **Voice / sound name collisions (the build picks the wrong file).** These clips play sounds from the class's
   `Sounds/` folder straight from the hero's code (`audio.PlayOneShot`, not an effect's AudioSource), and several share
   a name with a `Voices/` file: `nAttack1`, `nAttack2`, `nAttack3`, `cAttack1`, `cAttack2`, `bladeFang1`, `bladeFang2`
   exist in both `characters/heroes/wolf/sounds/` and `.../voices/`. `wardrobe_fx.py` `rip_wav()` looks in `sounds/`
   first and writes one `sfx/<name>.mp3`, and the page loads `sfx/<name>.mp3` by name. So today a cue
   `[0, "voice", "nAttack1"]` would play the **sword swing**, not the voice, and the two can never both exist.
   Below, a plain name = the `Voices/` file (as in the pilot's cues) and `"Sounds/<name>"` = the hero-played sound
   file. That spelling needs a build + page change (look the folder up from the prefix, keep the folder in the sfx
   file name, and look in `voices/` first for a plain name) before these cues can go in. The editor may pick another
   spelling; the point is that the folder has to be carried. Later: `bladeFang_underSlash` / `upperSlash` (and the
   bloodFang ones) carry an AudioSource with `Sounds/bladeFang2`, which will collide with the voice `bladeFang2`
   once those effects are built.
   - Volumes the cue format can't carry: the Normal Attack swings are `PlayOneShot(clip, 0.5f)` (half volume); the
     Charge Attack sounds and every voice are full volume (the voice is 0.75 only for other players).
2. **Three page timings disagree with the code** (`SEQ` in `index.html`; not a cue-file change, so for the user / main
   session). Cues below are written to the game's timing; where the page cuts a clip before a cue's time that cue
   never fires.
   - **Blade Fang `bladeFang1@0.2` should be `@0.7`** (about 90% sure). After the clip, the voice and
     `bladeFang_ring`, the start code `break`s out of the loop (`:26613`) into `Yield(2, 0.5)` (`:26652`): a 0.5 s
     wind-up before the dash and the first slash (case 2, `:25636`), first hit at 0.7 (case 3), then `bladeFang2`.
     `bladeFang1` is 0.7 s long, which fits a cut at 0.7. The Bible (`wolf-skill-reference.md:303`, "clips change at
     0 / 0.2 / 0.5 / 0.8 s, hits 0.2 / 0.4 / 0.7 / 1.0") and NOTES "Max rank everywhere" count from the dash, not from
     the press, so they leave out that 0.5 s: from the press it is 0 / 0.7 / 1.0 / 1.3, hits 0.7 / 0.9 / 1.2 / 1.5,
     standby 1.7. The later steps (`bladeFang2@0.3 bladeFang3@0.3 bladeFang2`) are right.
   - **Blade Song `bladeSong3@3.1` should be `@2.9`** (about 85% sure). The slash loop runs case 4 (a slash) and then
     goes straight to the check `i < 5 + 2 * sLv` (`:30273`) with no wait in between. Slashes come at 0.9, 1.1 ... 2.9
     (11 at rank 3), and `bladeSong4` crossfades in right after the 11th, at 2.9 s (`:30289`). The wait is before
     each slash (`Yield(4, 0.2)` `:30514`), not after the last one. NOTES' 0.9 + 0.2 × 11 = 3.1 counts one wait too
     many.
   - **Charge Attack: `cAttack1` should be `@0.8`, and `cAttack2*~@4.8` would need about `@5.1`** for the third
     charge ring to show (about 80% sure). The game cuts to `cAttack2` 0.8 s after the press (`Yield(2, 0.8)` `:19220`).
     The page plays all of `cAttack1` (1.0 s) and then 4.8 s of `cAttack2`: 5.8 s held in total, as NOTES planned.
     But the charge ticks run once a second from `cAttack2`'s start, and the tick that spawns `cAttack1_ring3` (the
     rank-3 "full" ring) comes 5.0 s into `cAttack2`, after the page's step has ended. Also, the third wave needs
     `ceil(held − 0.8) ≥ 6`, so held **more than** 5.8 s (Bible `:823`); exactly 5.8 gives `cTime` 5, two waves. With
     `cAttack1@0.8 cAttack2*~@5.1`, the hold is 5.9 s (three waves) and every tick fires.
   - Not affecting cues, the same kind of error: **Normal Attack `nAttack2^@0.96` should be `@0.64`.** Stages 2-4 wait
     from stage 1's `actionTime` (`:16267` +0.8, `:16959` +1.44, `:18024` +1.97). The Bible's combo table
     (`wolf-skill-reference.md:877-884`) has stage 3 at 1.44, and nAttack2's own state ends at 0.64 (`:16188`). The
     page starts stage 3 at 0.8 + 0.96 = 1.76. `nAttack3` (0.53 s) and `nAttack4` run their full clips, which is fine.

The Blade Fang wind-up and the Blade Song 2.9 s are game-timing findings the Bible's reference lacks (or states from
the dash). Offer them to the user for the Bible (its own repo and rules).

## Rules applied

- Max rank: Combo rank 3 (all 4 stages), Charge Attack rank 3 (`getChargeAttackLv()` = 3; with Sky Slasher #411 it
  would be 4, which only changes ticks from 12 s on, so the page's hold is the same either way), Blade Fang rank 3
  (`sLv` 3 = four slashes), Blade Song rank 3 (11 slashes) with Last Blade (#354, since the page plays `bladeSong4`).
- Game mode taken as mission / arena (`Game.mGameType > 4`): the charge ticks, their sounds and the release only exist
  there (`:18646`, `:18872`; Bible `:821`).
- "Sounds/" PlayOneShots are gated on `gameObject == Game.mPlayer` (only you hear your own swings). The wardrobe hero is
  the player, so they are kept.
- Left out by rule: everything at a target (hit sparks `nAttack_hit` / `bladeFang_hit`, `RPC_*_hit` sounds), camera
  effects (motion blur), damage, SP.
- No effect here has `followState` (checked in memory, `probe.py`), so no cue needs a 5th value.
- Random picks are 50/50 `Random.Range(0, 2) == 0` choices, written `a|b`.

## nAttack1 (Normal Attack, stage 1): `$RPC_nAttack1$29242`, `Wolf.cs:14852-15550`

Flow: start: clip `PlayAnimation("nAttack1", 0.2f)` (`:15444`), voice `Voices/nAttack1` (`:15491`, played `:15536`),
`Yield(2, 0.15)` (`:15547`). Case 2 (0.15): `moveSpeed 6`, `dust_forward` at the hero (`Instantiate(dust_forward,
position, rotation)`, `:14985`), `Yield(3, 0.2)` (`:15529`). Case 3 (0.35): `Sounds/nAttack1` at 0.5 volume
(`:15018`, `:15030`), `Yield(4, 0.3)` (`:15543`). Case 4 (0.65): the hit, plus `darkEdge1` if Dark Edge is on (below),
`Yield(5, 0.15)` (`:15525`). Case 5 (0.8): standby (`:15372`).

```json
  "nAttack1": {
    "why": "Wolf.cs RPC_nAttack1: clip and voice nAttack1 at 0 (:15444, :15491-15536); 0.15 s, the lunge's dust_forward at the hero (:14985, the Wolf prefab's dust_forward field); 0.2 s, the swing Sounds/nAttack1 (:15018-15030, volume 0.5); hit at 0.65 (left out: nAttack_hit at the target :8194; darkEdge1 :15103 only while the Dark Edge buff is on); standby 0.8 (:15372)",
    "cues": [
    [0, "voice", "nAttack1"],
    [0.15, "fx", "dust_forward"],
    [0.35, "voice", "Sounds/nAttack1"]
    ]
  },
```

- `dust_forward`: **ready** (EffectControl life 0.5 + 2 LineEmitters; extracts in memory). It is not in
  `fx_inventory.md` because the code never `Resources.Load`s it. It is the hero prefab's inspector field `dust_forward`
  (`Wolf.cs:14247`), and `probe_dust2.py` found the Wolf MonoBehaviour (resources.assets path 79653) pointing at
  `heroes/wolf/effects/dust_forward` (its first field). `wardrobe_fx.py wolf` finds it by name like any other effect.
- Left out: `nAttack_hit` (ready, but spawned at the target's hit point, `RPC_nAttack_hit` `:8194`) and its
  `Sounds/nAttack_hit` (`:8213`, played only when something is hit).
- Left out, **Dark Edge only**: `darkEdge1` (ready) at 0.65 s, `position + TransformDirection(0, 1, 1)` = 1 m ahead
  and 1 m up (`:15091-15103`), only when `getStatusLv("darkEdge") > 0`. That is another skill's buff, not a rank of
  this one. If the user wants Normal Attack shown "under Dark Edge": `[0.65, "fx", "darkEdge1", 1]` (the cue can't
  carry the 1 m height).

## nAttack2: `$RPC_nAttack2$29260`, `Wolf.cs:15611-16275`

The clip starts at case 2, after `Yield(2, actionTime − now + 0.8)` (`:16267`) = 0.8 s after stage 1 started. From the
clip: voice `Voices/nAttack2` (`:15802`, `:16256`), `Yield(3, 0.16)` (`:16261`). Case 3 (0.16): `moveSpeed 4`,
`Sounds/nAttack2` (`:15857`, `:15869`, 0.5), `Yield(4, 0.32)` (`:16265`). Case 4 (0.48): the hit (plus `darkEdge1`
`:15942` under Dark Edge), `Yield(5, 0.16)` (`:16272`). Case 5 (0.64): standby (`:16188`).

```json
  "nAttack2": {
    "why": "Wolf.cs RPC_nAttack2 (from its clip, :15740): voice nAttack2 at 0 (:15802, :16256); 0.16 s, the swing Sounds/nAttack2 (:15857-15869, volume 0.5); hit at 0.48 (left out: nAttack_hit at the target; darkEdge1 :15942 only under Dark Edge); standby 0.64 (:16188)",
    "cues": [
    [0, "voice", "nAttack2"],
    [0.16, "voice", "Sounds/nAttack2"]
    ]
  },
```

- Dark Edge only (left out): `[0.48, "fx", "darkEdge1", 1]`.

## nAttack3: `$RPC_nAttack3$29276`, `Wolf.cs:16333-16972`

Clip at case 2 (stage 1 + 1.44 s, `:16959`). From the clip: `moveSpeed 4`, voice `Voices/nAttack3` (`:16522`,
`:16534`) and `Sounds/nAttack2` (`:16560`, `:16572`, 0.5) together, `Yield(3, 0.33)` (`:16957`). Case 3 (0.33): the
hit (`darkEdge1` `:16645` under Dark Edge), `Yield(4, 0.2)` (`:16965`). Case 4 (0.53): standby (`:16891`).

```json
  "nAttack3": {
    "why": "Wolf.cs RPC_nAttack3 (from its clip, :16462): voice nAttack3 and the swing Sounds/nAttack2 (volume 0.5) at 0 (:16522-16572); hit at 0.33 (left out: nAttack_hit at the target; darkEdge1 :16645 only under Dark Edge); standby 0.53 (:16891)",
    "cues": [
    [0, "voice", "nAttack3"],
    [0, "voice", "Sounds/nAttack2"]
    ]
  },
```

- Dark Edge only (left out): `[0.33, "fx", "darkEdge1", 1]`.

## nAttack4: `$RPC_nAttack4$29292`, `Wolf.cs:17030-18027`

Clip at case 2 (stage 1 + 1.97 s, `:18024`). From the clip: voice `Voices/nAttack4` (`:17221`, `:18010`),
`Yield(3, 0.16)` (`:18022`). Case 3 (0.16): `moveSpeed 4`, `Sounds/nAttack1` (`:17276`, `:17288`, 0.5),
`Yield(4, 0.14)` (`:18008`). Case 4 (0.30): hit 1 (`darkEdge1` `:17356` under Dark Edge), `Yield(5, 0.3)` (`:18006`).
Case 5 (0.60): `Sounds/nAttack3` (`:17624`, `:17636`, 0.5), `Yield(6, 0.2)` (`:18002`). Case 6 (0.80): `moveSpeed 0`,
hit 2 (`darkEdge2` `:17694` under Dark Edge), `Yield(7, 0.5)` (`:17992`). Case 7 (1.30): standby (`:17925`). This
matches the Bible's 2.27 / 2.77 hits from stage 1 (`wolf-skill-reference.md:884`).

```json
  "nAttack4": {
    "why": "Wolf.cs RPC_nAttack4 (from its clip, :17159): voice nAttack4 at 0 (:17221, :18010); 0.16 s, the swing Sounds/nAttack1 (:17276-17288, volume 0.5); hit 1 at 0.3; 0.3 s, the second swing Sounds/nAttack3 at 0.6 (:17624-17636, volume 0.5); hit 2 at 0.8 (left out: nAttack_hit at the target; darkEdge1 :17356 / darkEdge2 :17694 only under Dark Edge); standby 1.3 (:17925)",
    "cues": [
    [0, "voice", "nAttack4"],
    [0.16, "voice", "Sounds/nAttack1"],
    [0.6, "voice", "Sounds/nAttack3"]
    ]
  },
```

- Dark Edge only (left out): `[0.3, "fx", "darkEdge1", 1]`, `[0.8, "fx", "darkEdge2", 1]` (`darkEdge2` ready,
  EffectControl life 1.0).

## cAttack1 (Charge Attack, the press): `$RPC_cAttack1$29320`, `Wolf.cs:18501-19226`

Start: clip `PlayAnimation("cAttack1", 0.2f)` (`:18742`), voice `charge1` or `charge2` (`Random.Range(0, 2) == 0`,
`:18783`, loads `:18795` / `:18827`, plays `:19209` / `:19196`), `Yield(2, 0.8)` (`:19220`). Then case 2 starts
`cAttack2`, so everything after it belongs to that clip.

```json
  "cAttack1": {
    "why": "Wolf.cs RPC_cAttack1: clip and voice charge1 / charge2 (Random.Range(0, 2), :18742-18827, :19196-19209) at 0; at 0.8 s it cuts to cAttack2 (:19220), whose cues hold the charge",
    "cues": [
    [0, "voice", "charge1|charge2"]
    ]
  },
```

## cAttack2 (the held charge): the same coroutine, case 2 and the 1 s tick (`IL_586`, `:18851-19201`)

Case 2 (the clip's 0): `PlayAnimation("cAttack2", 0.2f)`, looped (`:18636-18641`), `Sounds/cAttack1` (`:18658`,
`:18670`, full volume, needs `mGameType > 4` `:18646`), `count = 0`, `chargeLv = getChargeAttackLv()` = 3, then straight
into the tick. **Each tick** (`:18851`), while still charging: `count++` (`:18867`). If `count < 2`, `Sounds/cAttack2`
(`:18892`, `:18904`). Otherwise `Sounds/cAttack3` (`:18942`, `:18954`), skipped only at `count ≥ 12` with charge rank 4.
Then **`cAttack1_ring` at the hero every tick** (`:18976`, `:18988`, `Quaternion.identity`), and one tier ring
0.15 m up: `count ≥ 12` and rank ≥ 4 `skySlasher_ring` (`:19020-19032`), else `count ≥ 6` and rank ≥ 3
`cAttack1_ring3` (`:19068-19080`), else `count ≥ 4` and rank ≥ 2 `cAttack1_ring2` (`:19116-19128`), else `count ≥ 2`
`cAttack1_ring1` (`:19160-19172`). Then `Yield(3, 1)` (`:19201`). So tick k comes (k − 1) s into `cAttack2`.

| cAttack2 time | count | sound | rings |
|---|---|---|---|
| 0 | 1 | Sounds/cAttack1 + Sounds/cAttack2 | cAttack1_ring |
| 1, 2 | 2, 3 | Sounds/cAttack3 | cAttack1_ring + cAttack1_ring1 |
| 3, 4 | 4, 5 | Sounds/cAttack3 | cAttack1_ring + cAttack1_ring2 |
| 5 (6, 7 ...) | 6+ | Sounds/cAttack3 | cAttack1_ring + cAttack1_ring3 |

```json
  "cAttack2": {
    "why": "Wolf.cs RPC_cAttack1 case 2 (cut to cAttack2, looped, :18636): Sounds/cAttack1 (:18658-18670); the charge tick every 1 s from here (:18851, :19201): tick 1 Sounds/cAttack2 (:18892-18904), later ticks Sounds/cAttack3 (:18942-18954); cAttack1_ring at the hero every tick (:18988); the rank ring 0.15 m up: ticks 2-3 cAttack1_ring1 (:19172), 4-5 cAttack1_ring2 (:19128), 6+ cAttack1_ring3 (rank 3, :19080); mission / arena only (mGameType > 4, :18646, :18872)",
    "cues": [
    [0, "voice", "Sounds/cAttack1"],
    [0, "voice", "Sounds/cAttack2"],
    [0, "fx", "cAttack1_ring"],
    [1, "voice", "Sounds/cAttack3"],
    [1, "fx", "cAttack1_ring"],
    [1, "fx", "cAttack1_ring1"],
    [2, "voice", "Sounds/cAttack3"],
    [2, "fx", "cAttack1_ring"],
    [2, "fx", "cAttack1_ring1"],
    [3, "voice", "Sounds/cAttack3"],
    [3, "fx", "cAttack1_ring"],
    [3, "fx", "cAttack1_ring2"],
    [4, "voice", "Sounds/cAttack3"],
    [4, "fx", "cAttack1_ring"],
    [4, "fx", "cAttack1_ring2"],
    [5, "voice", "Sounds/cAttack3"],
    [5, "fx", "cAttack1_ring"],
    [5, "fx", "cAttack1_ring3"]
    ]
  },
```

- The three `5` cues fire only if the page's `cAttack2` step runs past 5.0 s (blocker 2). With today's `@4.8` they
  never fire, and `wardrobe_fx_check.py` would report `cAttack1_ring3` as never spawned. Either change the SEQ
  (`cAttack1@0.8 cAttack2*~@5.1`) or drop the three `5` lines.
- All **ready**: `cAttack1_ring` (EffectControl life 1 + afterLife 1, EllipsoidParticleEmitter + LineEmitter),
  `cAttack1_ring1` / `ring2` / `ring3` (one RingEmitter each, **no EffectControl**: the page drops them when their
  emitter ends, `Fx.update` `index.html:3008`). The game's 0.15 m height for the tier rings can't be written in a cue.
  They go in at distance 0, at the hero's feet.
- `skySlasher_ring` (ready) is never reached here: it needs 12 ticks and Sky Slasher.

## cAttack3 (the release): `$RPC_cAttack2$29329`, `Wolf.cs:19261-19907`

Start: `cTime = clamp(ceil(held − 0.8), 0, 2 × rank)` (`:19731`), clip `PlayAnimation("cAttack3", 0)` (cut, `:19752`),
voice `Voices/cAttack1` or `Voices/cAttack2` (`Random.Range(0, 2) == 0`, `:19793-19848`), a camera motion blur for the
local player (`:19870`), `Yield(2, 0.2)` (`:19904`). Case 2 (0.2): the **`cAttack2` effect** at the hero
(`Instantiate(cAttack2, position, rotation)`, `:19403`, `:19415`), `Yield(3, 0.3)` (`:19895`). Case 3 (0.5): wave 1;
`Yield(4, 0.1)`; case 4 (0.6): wave 2 if `cTime ≥ 4` (`:19517`); `Yield(5, 0.1)`; case 5 (0.7): wave 3 if
`cTime ≥ 6` (`:19592`); `Yield(6, 0.8)` (`:19891`); case 6 (1.5): standby (`:19676`). Each wave's hit calls
`RPC_nAttack_hit` at the target.

```json
  "cAttack3": {
    "why": "Wolf.cs RPC_cAttack2 (the release, clip cut in :19752): voice cAttack1 / cAttack2 (Random.Range(0, 2), :19793-19848) at 0; left out: the cAttack2 effect at the hero at 0.2 s (:19415) needs EffectControl(child); the waves' nAttack_hit at the targets (0.5 / 0.6 / 0.7 s); the camera motion blur (:19870)",
    "cues": [
    [0, "voice", "cAttack1|cAttack2"]
    ]
  },
```

- `cAttack2` effect: **needs EffectControl(child)**. When it is built, add `[0.2, "fx", "cAttack2"]`. Its own
  AudioSource plays `Sounds/cAttack4`.
- The voice names `cAttack1|cAttack2` are the `Voices/` files. They collide with `Sounds/cAttack1` / `Sounds/cAttack2`
  in the cAttack2 cues above (blocker 1).

## bladeFang1 (Blade Fang, the press and slash 1): `$RPC_bladeFang$29468`, `Wolf.cs:25489-26698`

Start: `PlayAnimation("bladeFang1", 0.2f)` (`:26402`). Voice: with Blood Fang (#403) `Voices/bloodFang1` or
`bloodFang2` (`:26451-26512`), else `Voices/bladeFang1` or `bladeFang2` (`Random.Range(0, 2) == 0`, `:26524-26579`).
`bladeFang_ring` at the hero (`createEffect(.., position, rotation)`, `:26598`, `:26610`), then `break` (`:26613`) to
`Yield(2, 0.5)` (`:26652`). Case 2 (0.5): `moveSpeed 12` (the dash), `dust_forward` at the hero (`:25641`),
`bladeFang_underSlash` (or `bloodFang_underSlash`) at the hero, turned `Euler(270, 90, 0)` (`:25658-25707`),
`Yield(3, 0.2)` (`:26686`). Case 3 (0.7): `moveSpeed 6`, hit 1 (`:25766-25789`), `bladeFang_count = 0` (`:25827`), then
`IL_16C1`: `count < sLv`, so the clip cuts to `bladeFang2` (`:26627-26640`).

```json
  "bladeFang1": {
    "why": "Wolf.cs RPC_bladeFang: clip, voice bladeFang1 / bladeFang2 (Random.Range(0, 2), :26402, :26524-26579) and bladeFang_ring at the hero (:26610) at 0; then a 0.5 s wait (:26613 -> :26652); the dash at 0.5 s with dust_forward at the hero (:25641) (left out: bladeFang_underSlash :25670 needs Animation, SkinnedMeshRenderer); hit 1 at 0.7 (bladeFang_hit at the target, left out), then bladeFang2 (:26640)",
    "cues": [
    [0, "voice", "bladeFang1|bladeFang2"],
    [0, "fx", "bladeFang_ring"],
    [0.5, "fx", "dust_forward"]
    ]
  },
```

- `bladeFang_ring`: **ready** (EffectControl life 0.5, followPosition, RingEmitter; its AudioSource plays `aura1`,
  found outside the wolf folders by `rip_wav`'s walk). `dust_forward`: ready (see nAttack1).
- `bladeFang_underSlash`: **needs Animation, SkinnedMeshRenderer**. When built: `[0.5, "fx", "bladeFang_underSlash"]`,
  but the game turns it by `Euler(270, 90, 0)` from the hero's rotation, which the cue format can't express. That is
  a separate job (a rotation field or a page rule).
- The `0.5` cue fires only once the SEQ has `bladeFang1@0.7` (blocker 2). With today's `@0.2` the clip is gone
  before 0.5.
- **Blood Fang (#403, Lv 55 Class C passive on Blade Fang 3):** "max rank" alone doesn't say whether it is learned.
  If it is: the voice becomes `bloodFang1|bloodFang2` and the slashes `bloodFang_underSlash` / `upperSlash` (also
  needing Animation + SkinnedMeshRenderer). Today only the voice would differ. **Ask the user** (Quick Fire's Added
  Fire was included on the user's word, NOTES "Max rank everywhere"). The default above is without it.

## bladeFang2 (slashes 2 and 4): the same coroutine, cases 4-6 / 9-10

From the cut (`:26640`): `Yield(4, 0.1)` (`:26694`). Case 4 (0.1): `dust_forward` (`:25854`), `bladeFang_upperSlash`
(or blood) `Euler(270, 90, 0)` (`:25871-25918`), `bladeFang_count++` (`:25933`), `Yield(5, 0.1)` (`:26664`). Case 5
(0.2): hit (`:25973`), `Yield(6, 0.1)` (`:26684`). Case 6 (0.3): after slash 2 (`count` 1 < 3) it cuts to `bladeFang3`
(`:26055-26063`). After slash 4 (`count` 3 ≥ 3): `moveSpeed 0` (`:26631`), `Yield(10, 0.1)` (`:26660`), standby at 0.4
(`:26308`). The page's two `bladeFang2` steps get the same cues, and the game does the same thing in both up to 0.3.

```json
  "bladeFang2": {
    "why": "Wolf.cs RPC_bladeFang cases 4-6 (from the cut to bladeFang2, :26640): 0.1 s, dust_forward at the hero (:25854) (left out: bladeFang_upperSlash :25883 needs Animation, SkinnedMeshRenderer); hit at 0.2 (bladeFang_hit at the target, left out); 0.3 s cut to bladeFang3 (:26063), or after the 4th slash standby at 0.4 (:26308)",
    "cues": [
    [0.1, "fx", "dust_forward"]
    ]
  },
```

- Left out: `bladeFang_upperSlash` at 0.1 (**needs Animation, SkinnedMeshRenderer**; same `Euler(270, 90, 0)` turn).

## bladeFang3 (slash 3): cases 6-9

At the cut (`:26063`): `dust_forward` at once (`:26073`), `Yield(7, 0.1)` (`:26654`). Case 7 (0.1):
`bladeFang_underSlash` (or blood) `Euler(270, 90, 0)` (`:26100-26159`), `count++` (`:26174`), `Yield(8, 0.1)`
(`:26677`). Case 8 (0.2): hit (`:26214`), `Yield(9, 0.1)` (`:26670`). Case 9 (0.3): back to `IL_16C1`, so it cuts to
`bladeFang2` (`:26286-26288`, `:26640`).

```json
  "bladeFang3": {
    "why": "Wolf.cs RPC_bladeFang cases 6-9 (clip cut in :26063): dust_forward at the hero at 0 (:26073) (left out: bladeFang_underSlash at 0.1 s :26124 needs Animation, SkinnedMeshRenderer); hit at 0.2 (bladeFang_hit at the target, left out); 0.3 s cut to bladeFang2 (:26640)",
    "cues": [
    [0, "fx", "dust_forward"]
    ]
  },
```

## bladeSong3 (Blade Song, rank 3): `$RPC_bladeSong$29571`, `Wolf.cs:29704-30517`

Start (`IL_A1F`): `switch (sLv)` and `PlayAnimation("bladeSong3", 0)` (`:30332`, `:30365`), voice `Voices/bladeSong1`
or `bladeSong2` (`Random.Range(0, 2) == 0`, `:30403-30506`), `Yield(2, 0.3)` (`:30500`). Case 2 (0.3):
`bladeSong_ring` at the hero (`createEffect`, `:29857`, `:29869`), `Yield(3, 0.4)` (`:30502`). Case 3 (0.7): the
backstep `moveSpeed −2` (`:29906`), `i = 0` (`:29926`), then the check `i < 5 + 2 × sLv` (`:30273`) and
`Yield(4, 0.2)` (`:30514`). Case 4 (0.9, 1.1, ... 2.9): `moveSpeed 0`, the `bladeSong` slash effect at the hero
(`createEffect`, `:29963`, `:29975`), its hit (`:30018`), `i++` (`:30046`), then straight back to the check. After the
11th slash (2.9 s), with Last Blade (`hasSkill(354)` `:30281`): `PlayAnimation("bladeSong4", 0.2f)` (`:30289`).

```json
  "bladeSong3": {
    "why": "Wolf.cs RPC_bladeSong (rank 3, clip :30365): voice bladeSong1 / bladeSong2 (Random.Range(0, 2), :30403-30506) at 0; 0.3 s, bladeSong_ring at the hero (:29869); 0.4 s, the backstep (:29906); then 5 + 2 x 3 = 11 slashes, each 0.2 s after the last, the bladeSong effect at the hero each time (:29975, loop :30273, wait :30514): 0.9 ... 2.9 s (hits at the targets left out); bladeSong4 right after the 11th (:30289)",
    "cues": [
    [0, "voice", "bladeSong1|bladeSong2"],
    [0.3, "fx", "bladeSong_ring"],
    [0.9, "fx", "bladeSong"],
    [1.1, "fx", "bladeSong"],
    [1.3, "fx", "bladeSong"],
    [1.5, "fx", "bladeSong"],
    [1.7, "fx", "bladeSong"],
    [1.9, "fx", "bladeSong"],
    [2.1, "fx", "bladeSong"],
    [2.3, "fx", "bladeSong"],
    [2.5, "fx", "bladeSong"],
    [2.7, "fx", "bladeSong"],
    [2.9, "fx", "bladeSong"]
    ]
  },
```

- `bladeSong_ring`: **ready** (EffectControl life 1, followPosition, RingEmitter, AudioSource `bladeSong_ring`).
  `bladeSong`: **ready** (EffectControl life 1, LineEmitters, AudioSource `bladeSong`, so each slash sounds by
  itself).
- With the page's `@3.1` all eleven still fire (2.9 < 3.1). Only `bladeSong4` comes 0.2 s late.
- Left out: the slashes' hits (`RPC_bladeSong_hit` at the targets).

## bladeSong4 (Last Blade): the same coroutine, cases 5-7

From the crossfade (`:30289`): `Yield(5, 0.3)` (`:30481`). Case 5 (0.3): a camera motion blur for the local player
(`:30083`), **`bladeSong_finalBlade` at the hero** (`createEffect`, `:30095`, `:30107`), the finisher's hit
(`:30129`), `Yield(6, 0.2)` (`:30489`). Case 6 (0.5): `Yield(7, 0.2)` (`:30498`). Case 7 (0.7): standby (`:30219`).

```json
  "bladeSong4": {
    "why": "Wolf.cs RPC_bladeSong after the last slash (Last Blade, bladeSong4 crossfaded in :30289): 0.3 s, bladeSong_finalBlade at the hero (:30107) (left out: the camera motion blur :30083, the hits at the targets :30129); standby at 0.7 (:30219)",
    "cues": [
    [0.3, "fx", "bladeSong_finalBlade"]
    ]
  }
```

- `bladeSong_finalBlade`: **ready** (EffectControl life 1, LineEmitters + RingEmitter, AudioSource `finalBlade`).

## Effects named, with status

| effect | where | status |
|---|---|---|
| dust_forward | nAttack1, bladeFang1/2/3 | ready (not in fx_inventory.md: a prefab field, not a Resources.Load; verified in memory) |
| cAttack1_ring, cAttack1_ring1/2/3 | cAttack2 | ready (ring1-3 have no EffectControl) |
| bladeFang_ring | bladeFang1 | ready |
| bladeSong_ring, bladeSong, bladeSong_finalBlade | bladeSong3/4 | ready |
| darkEdge1, darkEdge2 | nAttack1-4 under Dark Edge only | ready, left out (another skill's buff) |
| cAttack2 | cAttack3 at 0.2 s | needs EffectControl(child) |
| bladeFang_underSlash / upperSlash | bladeFang1/2/3 | needs Animation, SkinnedMeshRenderer (+ a rotation the cue can't carry) |
| bloodFang_underSlash / upperSlash | Blade Fang with Blood Fang | needs Animation, SkinnedMeshRenderer |
| skySlasher_ring | cAttack2 at 12 s with Sky Slasher | ready, not reached |
| nAttack_hit, bladeFang_hit, bloodFang_hit | at the targets | left out (rule) |

Voices / sounds named: `nAttack1`-`nAttack4`, `charge1|charge2`, `cAttack1|cAttack2`, `bladeFang1|bladeFang2`
(or `bloodFang1|bloodFang2`), `bladeSong1|bladeSong2` from `Voices/`; `Sounds/nAttack1`, `Sounds/nAttack2`,
`Sounds/nAttack3`, `Sounds/cAttack1`, `Sounds/cAttack2`, `Sounds/cAttack3` from `Sounds/`. All exist in the rip
(`RippedAssets\...\heroes\wolf\sounds|voices`).

## How sure

- Normal Attack timings and sounds: high (the waits add up to the Bible's combo table).
- Charge Attack tick contents: high (the label `IL_C76` sits after the `count < 2` if/else, so `cAttack1_ring`
  comes on every tick, tick 1 included). That the tier ring repeats every tick (not just once at 2 / 4 / 6): high, the
  conditions are `>=` and run each second.
- Blade Fang 0.5 s wind-up: about 90% (control flow through a `break` out of the flattened loop; the 0.7 s clip length
  agrees).
- Blade Song 2.9 s: about 85%.
- `dust_forward` being the prefab field's effect: confirmed by the PPtr scan.

## Recipe problems hit

1. **The recipe says "Only voices go in as voice"**, but here the hero's own code plays `Sounds/` files
   (`audio.PlayOneShot`, no effect involved). The recipe doesn't say what to do with them. They aren't an effect's
   AudioSource, so they need cues, and the cue/build format has no way to say which folder a name comes from
   (blocker 1). The recipe should say: hero-played `Sounds/` = a sound cue, with the folder carried.
2. **`rip_wav` prefers `sounds/`, and one sfx file per name**, so a voice whose name matches a sound file silently
   plays the wrong file. The recipe's step 4 check would pass (a file loads), so nothing catches it.
3. **No volume in a cue** (the swings are 0.5).
4. **No height or rotation offset in a cue.** `darkEdge1/2` are 1 m up; the charge tier rings are 0.15 m up; the Blade
   Fang slashes are turned `Euler(270, 90, 0)`.
5. **Effects set in the hero prefab's inspector** (`dust_forward`, a public `GameObject` field, `Instantiate(this.x,
   ...)`) are missing from `fx_inventory.md`, which only scans `Resources.Load` paths. Step 2's "look it up in the
   inventory" finds nothing for them. The recipe could say: check such a field with `wardrobe_fx.py --fx <name>` (or
   the in-memory probe) when its name matches a prefab in the class's effects folder.
6. **Cues past the page's step end never fire** (`fxStart` replaces `FX.cues` at each step). The recipe doesn't say to
   compare the cue times with the SEQ step lengths. Here that showed the SEQ timing errors (blocker 2), which the
   recipe forbids fixing in a skill job (no `index.html`), so they need a decision first.
7. **"Max rank" vs Class C passives** that change a skill's effects or voices (Blood Fang on Blade Fang, Sky Slasher on
   Charge Attack, Last Blade on Blade Song) and **another skill's buff** (Dark Edge on Normal Attack): the recipe and
   the user's rule don't say whether they count. Here: Last Blade yes (the page already plays `bladeSong4`), Sky
   Slasher irrelevant, Blood Fang asked, Dark Edge left out.
8. A cue on a clip the page plays twice in one sequence (`bladeFang2`) fires both times. That is right here, but the
   recipe could mention it.
