# Sheep effects + sounds research: the Cast tile (cast1, cast2, cast3), first 11 cast3 skills

Researcher `cast_a`, 2026-11-10 (office PC). Scope: `RPC_cast1` (the cast channel) and the cast3 pool members for Heal,
Bless, All Heal, Pacify, Sleep, Clear, Cleanse, All Cleanse, Over Heal, Revive, Revert. `cast_b` writes the other 12
members of the cast3 pool. Research only (recipe steps 1-3). Line numbers are
`C:\Users\Jump\Desktop\12tails\DecompiledSource\Sheep.cs` unless another file is named. Times are seconds from the start
of the clip the cue is keyed by. Distance 0 = at the hero.

Read-only probes, in `checks\fx_sheep_research\cast_a\`:
- `probe_fields.py` reads the Sheep hero MonoBehaviour's serialized fields.
- `probe.py` lists each effect's parts, EffectControl, AudioSource and Animation clips, through `wardrobe_fx.effect()` in
  memory. Nothing is written.
- `cond.sh` gives a condensed view of a line range, with the opaque predicates removed.

The TTO client (TTO1102) matches BB for everything here except All Cleanse's voice (below):
- `TTO1102:Sheep.<RPC_cast1>d__159::MoveNext@0x1e7fd20` has the same skill list and the same cast1 / cast2 / root names.
- `TTO1102:Sheep.<RPC_heal_cast>d__165::MoveNext@0x1e89ab0` loads the same heal / radiantHeal / heal1 / heal2.

---

## Read this first

1. **Three effects are not in `fx_inventory.md` but are ready.** `castRing`, `castEffect1` and `bless` are not in the
   inventory because `Sheep.cs` never `Resources.Load`s them:
   - `castRing` and `castEffect1` are inspector fields of the hero prefab (`public GameObject castRing / castEffect1 /
     castEffect2`, `:16721-16727`). `probe_fields.py` found that the Sheep MonoBehaviour's fields 1-3 point at
     `heroes/sheep/effects/castRing`, `castEffect1` and `castEffect2`. So `wardrobe_fx.py sheep` finds them by name.
   - `bless` is loaded by `CharacterControl.cs:39189` (the status's look).
   - Each one's parts are all parts the page builds, and each extracts in memory. Their parts are in the table at the end.
2. **The castRing's cut and the page's clock.** `fxStart` sets `FX.t = 0` at every sequence step (`index.html:3417`), and
   `seqTick` runs before `fxTick` in the same frame (`:3478-3479`).
   - The ring's real cut is at the step edge: 0.6 s, when cast3 starts. A `cut` of exactly 0.6 on cast1's clock is
     missed on the first round, so the ring would be cut 0.6 s into cast3 (about 1.2 s overall).
   - I propose `cut: 0.55`: it fires on cast1's clock at any frame rate of 20 fps or more, about 0.05 s early.
   - The clean fix is a page job, not a cue job: carry a cue's cut across sequence steps, or cut a followState effect
     when its clip's step ends.
3. **The castRing's after-life clip is not drawn.** The game plays three clips on the ring: `create` at spawn, then
   `root` looped at 0.6 s (`:19869-19874`), then `destroy` when its life ends (`EffectControl.cs:252-291`). The page plays
   only the default clip `create` (`fxparts/mesh.js:115-129`). So in its 1 s after-life the ring holds its last pose,
   then vanishes, where the game shrinks it with the 0.53 s `destroy` clip. `root` barely matters: the page has no cast
   bar, so the ring is cut the moment `root` would start. Not blocking, but it is a gap in the Animation part: playing
   `destroy` in the after-life.
4. **Name collision.** `voices/sleep.wav` and `sounds/sleep.wav` are different recordings.
   - The `sleep` effect's AudioSource clip is named `sleep`. `rip_wav` takes `sounds/` first, which is right for an
     effect's own sound.
   - The Sleep voice cue is `sleep1|sleep2` (voices/ only), so there is no clash in the cues.
   - The `sleep` effect is left out anyway: it plays on the enemy.
   - No other name in this scope is in both folders. Every voice cue below is `"voice"` = `voices/`. No cue here is
     `"sound"`: none of these coroutines plays a `Sounds/` clip itself. Each effect's own sound comes with the effect.
5. **Surprise: All Cleanse is silent in BB.** `RPC_allCleanse_cast` loads `Voices/allCleanse1` and `allCleanse2`
   (`:25676`, `:25707`).
   - Neither file exists: the game data has no `voices/allcleanse1` or `allcleanse2`. The rip's files are
     `voices/allClear1.wav` and `allClear2.wav`, and the game data has `voices/allclear1` / `allclear2`.
   - So BB logs "Cannot find allCleanse1 voice" and says nothing.
   - TTO fixed the path: `TTO1102:Sheep.<RPC_allCleanse_cast>d__173::MoveNext@0x1e75050` loads `Voices/allClear1` /
     `allClear2`.
   - This is a Bible finding too. Offer it to the user for `sheep-skill-reference.md` (that repo's rules).
6. **Free Cast is the Sheep's Double Art.** All 11 skills call `getFreeCast` at time 0. At max rank (Free Cast 2,
   #132) it rolls `Random.Range(0, 100) < lckAdjust(24)`, about 24 % (`:10061-10070`).
   - With Return Cast (#431) learned, the effect is `returnCast` (`:10085-10092`, `:11651-11661`), not `freeCast`
     (`:10116`, `:10157-10167`).
   - "Passives on at max rank", like Sublime Art's ring: `returnCast`, p 0.24. Open question 2.
7. **Cast2 and the cast bar.** In the game the channel always loops cast2 for at least 0.1 s:
   `magAdjust` clamps the cast time to at least 0.1 s (`CharacterControl.cs:20584-20588`). The page's `cast2*@0` is the
   user's "no cast bar" rule, so I changed nothing. None of the cues below depend on it.
8. **For cast_b and the editor: the pool and its cast channel.**
   - `RPC_seal` (`:32731`) and `RPC_edenSanctuary` (`:36960`) play cast3 without going through `RPC_cast1`. In the
     game their cast3 has no cast1 channel before it.
   - `RPC_soulOfArms_cast` is started by `RPC_cast1` but plays its own clip, `soulOfArms` (`:33886`), not cast3.

---

## cast1: RPC_cast1, the cast channel (plain entry)

- **Coroutine:** `$RPC_cast1$27747`, `:19654-21836`. It is the cast channel of all 22 dispatched skills, the 11 here
  among them. It is started by the input dispatch with the skill's name (`sType`), for example `RPC_cast1("heal", ...)`
  at `:4282`.
- **Timeline** (state machine from `PlayAnimation("cast1")`):
  - At 0 (case 0 → `IL_3CFF`):
    - The cast time and cooldown are set per skill (`:21208-21588`) and the cast time is shortened by `magAdjust`
      (`:21588`). `actionState = "attack"` and `myCommand = "cast"` (`:21591-21597`).
    - `PlayAnimation("cast1", 0.2f)`, played once (`:21618`). The clip is 0.6 s long (`data/sheep/clips.json`).
    - The voice is `Random.Range(0, 2) == 0` ? `Voices/cast1` : `Voices/cast2` (`:21659-21758`; PlayOneShot volume 1 for
      the local player).
    - Then `Yield(2, 0.1)` (`:21755`).
  - At 0.1 (case 2): `castRing` is instantiated at the hero, rotation `Quaternion.Euler(270, 90, 0)` (`:19822`), and
    `InitEffectControl(hero)` runs. It is world-absolute, not turned by the hero's facing. It is a flat ring, so only the
    turn of its pattern differs on the page. Then `Yield(3, 0.5)` (`:21751`).
  - At 0.6 (0.1 + 0.5) (case 3):
    - `PlayAnimation("cast2", 0)`, looped (`:19859`). The ring's `root` clip is looped (`:19869-19874`).
    - The cast bar is set: `castTime = Time.time + mCastTime` (`:19879`, `DisplayCastBar` `:19890`).
    - Then every frame (`YieldDefault(4)`, `:21762`) it faces the target (`:19970-19984`), and when `Time.time >= castTime`
      it starts `RPC_<skill>_cast` (`:20003-21127`; heal `:20020`, allHeal `:20069`, bless `:20101`, pacify `:20156`,
      sleep `:20211`, clear `:20266`, cleanse `:20321`, allCleanse `:20370`, overHeal `:20402`, revive `:20457`, revert
      `:20512`). If the target is missing, it calls `RPC_cast0` (standby) instead.
  - **The handover:** the `_cast` coroutine runs at once. It sets `myCommand = "<skill>"` and plays cast3. Because
    `castRing` has followState, it records `actionState` / `myCommand` at init (`EffectControl.cs:122-140`) and goes to
    its after-life when either one changes (`:194-247`). So the ring is cut at cast3's start (0.6 s on the page) and is
    gone 1 s later.
- **Effects:**
  - `castRing`: **ready**.
    - EffectControl: life 60, afterLife 1, followPosition, **followState**.
    - Its parts: Animation (create 0.47 s / root 2 s / destroy 0.53 s), StaticMesh (the ring, child scale 0.1),
      VortexEmitter (Life 0.7, radius 0.2 → 0.6), AudioSource.
    - The AudioSource plays its own `Sounds/cast` (1.87 s), playOnAwake and loop. The page plays it once; the game cuts
      it at about 1.6 s, when the ring is destroyed.
    - The prefab's own root rotation is (0.5, -0.5, -0.5, -0.5), the same as Euler(270, 90, 0) (my own calculation). The
      cue gives `rot`, because the page's root rotation without one is the hero's facing (`index.html:3123`).
  - Left out: `overHeal_ring`. For Over Heal only, it is created on the enemy target once a second while casting
    (`:21137-21184`: `createEffect(overHeal_ring, tObject.position, ...)` on a 1 s timer). The target is an enemy.

```json
  "cast1": {
    "why": "Sheep.cs RPC_cast1 (:19654-21836), the cast channel the dispatcher starts for every cast-time skill (:20003-21127): clip cast1 (0.2 fade, :21618) and voice cast1 / cast2 (Random.Range(0, 2), :21659-21758) at 0; Yield 0.1 (:21755): castRing at the hero, Quaternion.Euler(270, 90, 0) (:19822; the hero prefab's castRing field = Resources sheep/effects/castRing; EffectControl life 60 + afterLife 1, followState; plays its own Sounds/cast, looped); Yield 0.5 (:21751): cast2 looped and the ring's root clip at 0.6 s (:19859-19874), then the cast bar (:19879; the page: none) and the skill's RPC_<skill>_cast, which sets myCommand: the ring's cut at the step edge 0.6 s (EffectControl.cs:122-247), cued 0.55 because the page restarts FX.t at each step (index.html:3417); left out: Over Heal's overHeal_ring on the enemy target every 1 s while casting (:21137-21184)",
    "cues": [
    [0, "voice", "cast1|cast2"],
    [0.1, "fx", "castRing", {"rot": [270, 90, 0], "cut": 0.55}]
    ]
  }
```

Sure: high for the times and names. The 0.55 is a page workaround (Read this first, item 2).

## cast2: no entry

The loop of the cast bar. The page holds it for 0 s. Nothing is spawned in it: `castTime`, the cast bar and facing the
target only.

## cast3: the shared pool (`skills`), the 11 members here

Every member has the same skeleton, all at time 0 of cast3. There is no wait before the coroutine's only
`Yield(2, 0.5)`. Then case 2 sets standby at 0.5 s. The 1.0 s clip runs on.

- `PlayAnimation("cast3", 0.2f)`, played once. The page's `cast3~` = the 0.2 s crossfade.
- `castEffect1` at the hero, with rotation = hero rotation x `Quaternion.Euler(270, 90, 0)`. This is exactly the cue's
  `rot` meaning (after the hero's facing).
  - It is ready: EffectControl life 0.4, afterLife 1, followPosition, no followState.
  - Parts: Animation `root` 0.8 s and legacy particles. No sound.
- The Free Cast roll, `getFreeCast(<skill>, sLv)`, local player only. With Return Cast on: `returnCast` at the hero
  (hero position + rotation, `:11661`). It is ready: EffectControl life 1, followPosition; ImageEmitter + LineEmitter +
  RingEmitter; no sound.
- The voice `<skill>1|<skill>2` (`Random.Range(0, 2)`, voices/, volume 1).
- The skill's own effect on its target(s). On the hero = kept. On an enemy or a dead ally = left out.
- **Ally-targeted skills (Heal, Bless, Pacify, Clear, Cleanse, Revert).** The target check accepts any character on the
  Sheep's own layer (`GameGui.cs:37904-37921`), and that includes the Sheep herself.
  - I propose the self-cast: the effect at the hero, distance 0. That is the only ally the wardrobe has. Open question 1.
  - In the game these effects spawn at the target's feet with `Quaternion.identity`, so the page's hero-facing yaw turns
    them. They are rings and particles, so the difference is cosmetic.

The entry (the editor merges cast_b's 12 members into `skills`):

```json
  "cast3": {
    "why": "The cast3 clip is played by 23 Sheep skills, 21 of them after the RPC_cast1 channel (Sheep.cs :22032 ... :38159; Seal :32731 and Eden Sanctuary :36960 play it without the channel): each play shows one, picked at random",
    "skills": {
      "heal": {
        "why": "Sheep.cs RPC_heal_cast (:21837-22435): clip cast3 (0.2 fade, :22032), all at 0: Free Cast roll (getFreeCast :22044; rank 2 #132: lckAdjust(24) = 24 %, :10061-10070; Return Cast #431 on: returnCast at the hero, :10085-10092, :11651-11661), castEffect1 at the hero x Euler(270, 90, 0) (:22056; the hero prefab's castEffect1 field), voice heal1 / heal2 (:22091-22146), the heal on the target ally at its feet: Radiant Heal #402 on: radiantHeal (:22201-22225; else heal :22248-22260; plays its own Sounds/heal); shown as a self heal (the ally check takes the Sheep herself, GameGui.cs:37904-37921); Yield 0.5 (:22369): standby 0.5 s (:21973); Radiant Heal's 40 % splash on allies within 8 m draws nothing (:22299-22337)",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "fx", "castEffect1", {"rot": [270, 90, 0]}],
        [0, "voice", "heal1|heal2"],
        [0, "fx", "radiantHeal"]
        ]
      },
      "bless": {
        "why": "Sheep.cs RPC_bless_cast (:22436-22888): clip cast3 (0.2 fade, :22658), all at 0: voice bless1 / bless2 (:22693-22748), castEffect1 at the hero x Euler(270, 90, 0) (:22767), Free Cast roll (getFreeCast :22779, 24 %; Return Cast on: returnCast, :10085-10092), the bless status on the target ally (:22824; Gospel #412 only +1 level and the 30 s cooldown), whose apply draws Effects/bless at the receiver's feet (CharacterControl.cs:39189-39198, no wait; plays its own Sounds/bless); shown as a self bless; Yield 0.5 (:22844): standby 0.5 s (:22593)",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "fx", "castEffect1", {"rot": [270, 90, 0]}],
        [0, "voice", "bless1|bless2"],
        [0, "fx", "bless"]
        ]
      },
      "allHeal": {
        "why": "Sheep.cs RPC_allHeal_cast (:22889-23361): clip cast3 (0.2 fade, :23073), all at 0: Free Cast roll (getFreeCast :23085, 24 %; Return Cast on: returnCast, :10085-10092), castEffect1 at the hero x Euler(270, 90, 0) (:23097), voice allHeal1 / allHeal2 (:23132-23187), heal at every player of the Sheep's team container, the Sheep included (transform.parent, tag Player, :23200-23259; plays its own Sounds/heal); KO Heal #422 changes only the amount (:23289); Yield 0.5 (:23315): standby 0.5 s (:23014)",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "fx", "castEffect1", {"rot": [270, 90, 0]}],
        [0, "voice", "allHeal1|allHeal2"],
        [0, "fx", "heal"]
        ]
      },
      "pacify": {
        "why": "Sheep.cs RPC_pacify_cast (:23362-23949): clip cast3 (0.2 fade, :23585), all at 0: voice pacify1 / pacify2 (:23620-23675), Free Cast roll (getFreeCast :23694, 24 %; Return Cast on: returnCast, :10085-10092), castEffect1 at the hero x Euler(270, 90, 0) (:23706), pacify at the target ally's feet (:23760-23772; no sound of its own); shown as a self pacify; the hate cut on enemies within 40 m draws nothing (:23786-23842); Yield 0.5 (:23882): standby 0.5 s (:23520)",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "fx", "castEffect1", {"rot": [270, 90, 0]}],
        [0, "voice", "pacify1|pacify2"],
        [0, "fx", "pacify"]
        ]
      },
      "sleep": {
        "why": "Sheep.cs RPC_sleep_cast (:23950-24451): clip cast3 (0.2 fade, :24172), all at 0: voice sleep1 / sleep2 (:24207-24262; voices/: voices/sleep.wav and sounds/sleep.wav are other recordings), Free Cast roll (getFreeCast :24281, 24 %; Return Cast on: returnCast, :10085-10092), castEffect1 at the hero x Euler(270, 90, 0) (:24293); Yield 0.5 (:24405): standby 0.5 s (:24107); left out: sleep at the enemy target's collider centre (:24347-24359) and its sleep status (:24382), at the target",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "fx", "castEffect1", {"rot": [270, 90, 0]}],
        [0, "voice", "sleep1|sleep2"]
        ]
      },
      "clear": {
        "why": "Sheep.cs RPC_clear_cast (:24452-24945): clip cast3 (0.2 fade, :24674), all at 0: voice clear1 / clear2 (:24709-24764), Free Cast roll (getFreeCast :24783, 24 %; Return Cast on: returnCast, :10085-10092), castEffect1 at the hero x Euler(270, 90, 0) (:24795), clear at the target ally's feet (:24849-24861; plays its own Sounds/cleanse); shown as a self clear; Purify #442 changes only the status level and time (:24881); Yield 0.5 (:24903): standby 0.5 s (:24609)",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "fx", "castEffect1", {"rot": [270, 90, 0]}],
        [0, "voice", "clear1|clear2"],
        [0, "fx", "clear"]
        ]
      },
      "cleanse": {
        "why": "Sheep.cs RPC_cleanse_cast (:24946-25444): clip cast3 (0.2 fade, :25168), all at 0: voice cleanse1 / cleanse2 (:25203-25258), Free Cast roll (getFreeCast :25277, 24 %; Return Cast on: returnCast, :10085-10092), castEffect1 at the hero x Euler(270, 90, 0) (:25289), cleanse at the target ally's feet (:25343-25355; plays its own Sounds/cleanse); shown as a self cleanse; Purify #442 changes only the status level and time (:25375); Yield 0.5 (:25398): standby 0.5 s (:25103)",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "fx", "castEffect1", {"rot": [270, 90, 0]}],
        [0, "voice", "cleanse1|cleanse2"],
        [0, "fx", "cleanse"]
        ]
      },
      "allCleanse": {
        "why": "Sheep.cs RPC_allCleanse_cast (:25445-25901): clip cast3 (0.2 fade, :25629), all at 0: Free Cast roll (getFreeCast :25738, 24 %; Return Cast on: returnCast, :10085-10092), castEffect1 at the hero x Euler(270, 90, 0) (:25750), cleanse at every player of the Sheep's team container, the Sheep included (:25756-25815; plays its own Sounds/cleanse); Yield 0.5 (:25861): standby 0.5 s (:25570); no voice: BB loads Voices/allCleanse1 / allCleanse2 (:25664-25719), which the game doesn't have (its files are allClear1 / allClear2), so it says nothing (TTO1102:Sheep.<RPC_allCleanse_cast>d__173::MoveNext@0x1e75050 loads allClear1 / allClear2)",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "fx", "castEffect1", {"rot": [270, 90, 0]}],
        [0, "fx", "cleanse"]
        ]
      },
      "overHeal": {
        "why": "Sheep.cs RPC_overHeal_cast (:25902-26431): clip cast3 (0.2 fade, :26124), all at 0: voice overHeal1 / overHeal2 (:26159-26214), Free Cast roll (getFreeCast :26233, 24 %; Return Cast on: returnCast, :10085-10092), castEffect1 at the hero x Euler(270, 90, 0) (:26245); Yield 0.5 (:26382): standby 0.5 s (:26059); left out: overHeal at the enemy target, its position and rotation (:26293-26305), and the strike (:26337-26357), at the target",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "fx", "castEffect1", {"rot": [270, 90, 0]}],
        [0, "voice", "overHeal1|overHeal2"]
        ]
      },
      "revive": {
        "why": "Sheep.cs RPC_revive_cast (:26432-26941): clip cast3 (0.2 fade, :26654), all at 0: voice revive1 / revive2 (:26689-26744), Free Cast roll (getFreeCast :26763, 24 %; Return Cast on: returnCast, :10085-10092), castEffect1 at the hero x Euler(270, 90, 0) (:26775); Yield 0.5 (:26892): standby 0.5 s (:26589); left out: revive at the knocked-out ally's feet (:26829-26841, ReviveEvent :26867), never the Sheep herself",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "fx", "castEffect1", {"rot": [270, 90, 0]}],
        [0, "voice", "revive1|revive2"]
        ]
      },
      "revert": {
        "why": "Sheep.cs RPC_revert_cast (:26942-27436): clip cast3 (0.2 fade, :27164), all at 0: voice revert1 / revert2 (:27199-27254), Free Cast roll (getFreeCast :27273, 24 %; Return Cast on: returnCast, :10085-10092), castEffect1 at the hero x Euler(270, 90, 0) (:27285), revert at the target ally's feet (:27339-27351; plays its own Sounds/revert); shown as a self revert; Yield 0.5 (:27394): standby 0.5 s (:27099)",
        "cues": [
        [0, "fx", "returnCast", {"p": 0.24}],
        [0, "fx", "castEffect1", {"rot": [270, 90, 0]}],
        [0, "voice", "revert1|revert2"],
        [0, "fx", "revert"]
        ]
      }
    }
  }
```

### Per skill: who it targets, where its effect goes

| Skill (max rank) | Coroutine | Target | Its own effect | Wardrobe |
|---|---|---|---|---|
| Heal 4 + Radiant Heal | `:21837-22435` | ally (or self) | `radiantHeal` at the target's feet (`:22225`) | self: at the hero |
| Bless 4 + Gospel | `:22436-22888` | ally (or self) | `bless` at the receiver (status apply, `CharacterControl.cs:39198`) | self: at the hero |
| All Heal 2 + KO Heal | `:22889-23361` | whole team, the Sheep included | `heal` on each (`:23259`) | at the hero (always) |
| Pacify 2 | `:23362-23949` | ally (or self) | `pacify` at the target's feet (`:23772`) | self: at the hero |
| Sleep 2 | `:23950-24451` | enemy | `sleep` at the target's collider centre (`:24359`) | left out |
| Clear 2 + Purify | `:24452-24945` | ally (or self) | `clear` at the target's feet (`:24861`) | self: at the hero |
| Cleanse 1 + Purify | `:24946-25444` | ally (or self) | `cleanse` at the target's feet (`:25355`) | self: at the hero |
| All Cleanse 1 + Purify | `:25445-25901` | whole team, the Sheep included | `cleanse` on each (`:25815`) | at the hero (always) |
| Over Heal 2 | `:25902-26431` | enemy | `overHeal` at the target (`:26305`); `overHeal_ring` while casting (`:21184`) | left out |
| Revive 2 | `:26432-26941` | knocked-out ally | `revive` at the target's feet (`:26841`) | left out (never herself) |
| Revert 1 | `:26942-27436` | ally (or self) | `revert` at the target's feet (`:27351`) | self: at the hero |

Timing check for every member: everything at 0 (one state, no wait before it). The only wait is `Yield(2, 0.5)`, then
standby: 0 + 0.5 = 0.5 s. That matches the reference: "every heal coroutine finishes with a 0.5 s recovery"
(`sheep-skill-reference.md`, "Shared cast dispatcher").

### Effects used, from the probe

All are ready: every part is built and each extracts in memory.

| Effect | Where it comes from | Parts | EffectControl | Own sound |
|---|---|---|---|---|
| castRing | prefab field, `:16721` | Animation, StaticMesh, VortexEmitter, AudioSource | life 60, afterLife 1, followState | `cast` (loop) |
| castEffect1 | prefab field, `:16724` | Animation, legacy particles | life 0.4, afterLife 1 | none |
| returnCast | `:11651` | ImageEmitter, LineEmitter, RingEmitter | life 1 | none |
| radiantHeal | `:22213` | RingEmitter x3, legacy particles x2 | life 1 | `heal` |
| heal | `:22248`, `:23247` | RingEmitter x2, legacy particles | life 1 | `heal` |
| bless | `CharacterControl.cs:39189` | ImageEmitter, legacy particles | life 1, afterLife 1 | `bless` |
| pacify | `:23760` | RingEmitter x2 | life 1, afterLife 1 | none |
| clear | `:24849` | RingEmitter x2 | life 1, afterLife 1 | `cleanse` |
| cleanse | `:25343` | RingEmitter x2 | life 1, afterLife 1 | `cleanse` |
| revert | `:27339` | ImageEmitter, RingEmitter x3 | life 1, afterLife 1 | `revert` |

Left out, but ready (they are on a target): `sleep`, `overHeal`, `overHeal_ring`, `revive`. Not used: `freeCast` (ready,
replaced by `returnCast` while Return Cast is on) and `castEffect2` (cast_b's skills, `:28844` ...). No effect in this
scope needs a missing part. The one gap is castRing's `destroy` clip in the after-life (Read this first, item 3).

## Open questions for the user

1. **Ally skills on the hero?** Heal, Bless, Pacify, Clear, Cleanse and Revert target an ally or the Sheep herself. I
   propose showing them as a self-cast: their effect at the hero. Or leave them out like an enemy's?
   - Revive stays out either way: its target is a knocked-out ally, never her.
   - Sleep and Over Heal stay out either way: their target is an enemy.
2. **Free Cast's look: `returnCast` or `freeCast`?** Both are rolled 24 % on all 11 skills, like Double Art.
   - "Passives on at max rank" = Return Cast learned, so `returnCast`.
   - Without Return Cast it would be `freeCast`.
3. **All Cleanse's voice: silent (BB) or `allClear1|allClear2` (TTO's fix)?** BB loads a file that doesn't exist. Both
   recordings are in the BB rip, so using them breaks no content rule.

## Verification (2026-11-10)

A skeptical re-trace by a checker (office PC). Nothing was built or published, and no browser was used. Read-only
probes: `checks/fx_sheep_research/cast_a/probe_fields.py` (re-run) and `wardrobe_fx.py sheep --probe` on all 31 cast
effects, in `checks/fx_sheep_research/verify/cast_probe.json`, summarised in `cast_probe_summary.txt`.

**What I checked, and found right:**
- **RPC_cast1 times**, re-added along the state machine (`clip_flow.js ... RPC_cast1`):
  - case 0: `PlayAnimation("cast1", 0.2f)` `:21618`, the voice `cast1` / `cast2` `:21669` / `:21700` (PlayOneShot
    `:21758` / `:21743`), then `Yield(2, 0.1)` `:21755`.
  - case 2: castRing `Instantiate(.., Quaternion.Euler(270, 90, 0))` `:19822`, then `Block_136` = `Yield(3, 0.5)`
    `:21751`.
  - case 3, at 0.1 + 0.5 = 0.6 s: cast2 `:19859`, the ring's `root` `:19869`.
  - The dispatch to the 22 `_cast` coroutines is at `:20020-21092`. cast1 is 0.6 s long and cast3 1.0 s (`data/sheep/clips.json`).
- **All 11 cast3 members** (`clip_flow.js` on each): every effect, voice, `getFreeCast` and `RPC_AddStatus` line in the
  report is right. Each member has exactly one wait, `Yield(2, 0.5)`, and nothing comes before it, so the clip, voice,
  castEffect1, Free Cast roll and the target effect are all at 0, and standby is at 0.5.
  - castEffect1 is `rotation * Euler(270, 90, 0)` (`:22056` and the other ten).
  - Radiant Heal is an if/else: with #402 learned, only radiantHeal is drawn, never heal (`:22201-22268`).
- **Voice files:** every cue's voice exists in the rip's `voices/`. There is no `allCleanse*` file, only
  `allClear1/2.wav`. TTO loads `Voices/allClear1` / `allClear2` (`pseudo/Sheep.c:1145`, `:1147`, in
  `<RPC_allCleanse_cast>d__173` `:1078`), so the All Cleanse finding stands.
- **The sleep clash:** `voices/sleep.wav` (0.917 s) and `sounds/sleep.wav` (1.119 s) have different MD5s.
  `rip_wav` looks in `sounds/` first (`wardrobe_fx.py:280`).
- **Free Cast:** `getFreeCastLv` `:10049`, the roll `:10070` (`lckAdjust(12 x 2)`), Return Cast `:10085-10101`,
  returnCast `:11651-11661`. The Bible's reference ("Free Cast") agrees.
- **The prefab fields:** `probe_fields.py` gives field 1 = castring, 2 = casteffect1, 3 = casteffect2. The
  declarations are at `:16721` / `:16724` / `:16727`.
- **The effect table:** each effect's parts, EffectControl and own sound, re-probed. castRing's Vortex is Life 0.7,
  radius 0.2 to 0.6. `sounds/cast.wav` is 1.872 s.
  - Euler(270, 90, 0) works out to (0.5, -0.5, -0.5, -0.5), step by step:
  - Rx(270) = (x 0.7071, w -0.7071) and Ry(90) = (y 0.7071, w 0.7071).
  - Ry x Rx gives w = -0.5, x = 0.5, y = -0.5, z = -0.5.
- **The 0.55 cut** (`index.html:1123-1153`, `:3416-3417`, `:3160`, `:3478-3479`):
  - **First round:** `play()` starts step 0 outside the render loop, so `FX.t` equals the step clock `S.t`. The last
    cast1 frame has `FX.t < 0.6`, so a cut of exactly 0.6 is missed.
  - **Later rounds:** a step started by `seqTick` resets `FX.t` before that frame's `fxTick` adds dt, so `FX.t` runs one
    frame ahead and a cut of 0.6 would fire. 0.55 works for both, at dt <= 0.05 s. The claim is right.
- The destroy clip is played by `EffectControl.cs:252-288`. `magAdjust` has a 0.1 s floor
  (`CharacterControl.cs:20587`). The ally check is `GameGui.cs:37904-37921`, and bless is at
  `CharacterControl.cs:39189-39198`.
- **TTO:** `<RPC_cast1>d__159@0x1e7fd20` (it uses 4.712389 / 1.5707964 = 270 / 90 degrees) and
  `<RPC_heal_cast>d__165@0x1e89ab0` (heal, radiantHeal, heal1, heal2). Every cast3 member has a 0.2 fade in TTO too,
  and one wait (0.5 where the pseudo labels it).

**Correction:**
- Read-only effect list, "Not used": `castEffect2` (cast_b's skills, `:30833` ...) -> `:28844` ...
  - `:30833` is the `if (!castEffect2)` null check.
  - The first castEffect2 spawn is `Sheep.cs:28844`: `createEffect(castEffect2, position +
    TransformDirection(0, 1, 0.7f), rotation)`.

**For the editor (not errors in this report):**
- cast_b's "Read this first" point 1 applies to this report's plain `cast1` entry. With `cast1` not a pool,
  `fxStart` never re-picks the cast3 member after the first play (`index.html:3422`:
  `if (step === 0 || !e.skills[FX.pick])`). I confirmed it in the page code: `FX.pick` is set nowhere else.
- This report puts the six ally skills' effects on the hero (open question 1). cast_b leaves its five ally buffs out.
  The two halves of the pool need one rule, and the user picks it.
