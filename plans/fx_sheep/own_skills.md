# Sheep effects + sounds research: Holy Light, Lullaby, Purifying Tear, Soul of Arms, Book Bash

Scope: clips holyLight1-4, lullaby, purifyingTear, soulOfArms, bookBash1-3. Research only (recipe steps 1-3). All line
numbers are `C:\Users\Jump\Desktop\12tails\DecompiledSource\Sheep.cs` unless named. Times are seconds from the start of
the clip the cue is keyed by. Distance 0 = at the hero. Prefab facts come from the read-only probe
(`wardrobe_fx.py sheep --probe ...`; output and a summariser in `checks\fx_sheep_research\own_skills\`). The decompile's
`if (a - b != c) continue;` lines are opaque predicates: each one I passed was worked out and goes the normal way.

## Read this first

1. **Blocker: `holyLight1` starts two skills.** Holy Light (`RPC_holyLight`) and Lullaby (`RPC_lullaby`) both open with
   `holyLight1` (0.2 s fade), then `holyLight2`. The page looks cues up by clip alone (`fxStart(st.clip, i)`,
   `index.html:1139`, `:3416-3419`). A `"skills"` pool would pick one skill at random on every play, so the Lullaby tile
   would say Holy Light's line half the time (and the reverse). Only the voice differs: Holy Light says `cast1` /
   `cast2`, Lullaby says `lullaby1` / `lullaby2`. The castRing is the same in both. Fix (a page change, not a cue job):
   let `fxStart` try a key for the sequence first, e.g. `FX.cueTab[cls][chainId + ":" + clip] ?? FX.cueTab[cls][clip]`,
   with the chain id the page already has (`"@Lullaby"`). Both entries are below. Until the page fix lands, put Holy
   Light's in as `holyLight1` and hold Lullaby's back.
2. **The SEQ times for Holy Light and Lullaby are right** (checked below, case by case). The order is holyLight1 >
   holyLight2 > holyLight3 > holyLight4 and holyLight1 > holyLight2 > lullaby. `clip_calls.js` prints the clips in file
   order (holyLight2 first), which is not the order they play.
3. **The two channels have no time limit.** After the cast bar (`magAdjust(6)` for Holy Light, `magAdjust(9)` for
   Lullaby, 0 on the page), the light (or the lullaby) ticks every 1 s until the Sheep moves or her MP / SP runs short.
   The Bible's reference says each one "ends at `actionTime + mCastTime + 0.6`". That is the moment the light *starts*.
   The page's `holyLight4*@3` / `lullaby*@3` (three ticks) is the right stand-in.
4. **Soul of Arms is paced by a timer, not by animation events** (the Bible says events). It hits at 4.6, 5.1, 5.3, 5.5,
   5.7, 6.2 and 9.5 s and goes to standby at 9.8 s. Its main look, the summoned arms (`soulOfArms`), spawns **at the
   target** and needs AlphaTimer. Lullaby's only effect (`lullaby_ring`) also needs AlphaTimer. Both skills will look
   thin until AlphaTimer is built: Lullaby shows only the voice and the cast ring; Soul of Arms shows the voice and the
   rune ring.
5. **`castRing` is an inspector field** (`public GameObject castRing`, `:16721`), not a `Resources.Load`, so the
   inventory doesn't list it. A Resources prefab `sheep/effects/castRing` exists. The probe builds it with no error: its
   parts (Animation, EffectControl, AudioSource, StaticMesh, VortexEmitter) are all on the page, so it is **ready**. I
   couldn't confirm that the field points to this prefab: the rip's `Sheep.prefab` has no decoded script fields. It is
   the same case as the Wolf's `dust_forward`, sure: medium-high. The Cast tile (`RPC_cast1`) probably uses it too:
   keep the two the same.
6. **World-space rotations.** The castRing and `holylight_ring` spawn at `Quaternion.Euler(270, 90, 0)` with no hero
   term (`:28112`, `:28374`, `:35877`). The page's `rot` is applied after the hero's facing, so `rot [270, 90, 0]`
   matches the game when the hero faces world forward. Both prefabs' roots are authored at exactly this rotation
   (quaternion `[0.5, -0.5, -0.5, -0.5]`; Unity's `Euler(270, 90, 0)` works out to the same). Both effects look round
   about the vertical axis, so the yaw part should not show.
7. **Free Cast / Return Cast proc** (the Sheep's Double Art): Holy Light, Lullaby and Purifying Tear call
   `getFreeCast`. Following the Wolf's passives rule (Free Cast 2 #132 and Return Cast #431 learned), a proc is
   `returnCast` at the hero at 24 %. Soul of Arms and Book Bash never roll it. I've put it in the entries below. It is a
   class-wide decision, so check it against the researcher covering the Cast tile.
8. **Name collisions: none in this scope.** The voices (`cast1-2`, `holyLight1-2`, `lullaby1-2`, `purifyingTear1-2`,
   `soulofArms1-2`, `bookBash1-3`) don't share a name with any sound (`cast`, `holyLight`, `holyLight_start`,
   `holyLight_end`, `lullaby`, `purifyingTear`, `soulOfArms`, `bookBash`). The voice `holyLight1` / `holyLight2` has
   the same name as the *clip* `holyLight1` / `holyLight2`. That is harmless (different namespaces) but easy to misread.
   One clash outside my scope: `voices/sleep.wav` and `sounds/sleep.wav` both exist (the `v_` prefix already keeps them
   apart).
9. **Name case.** The code loads `Voices/holylight1`, `Voices/soulOfArms1`, `Sounds/holylight_start`; the rip's files
   are `holyLight1.wav`, `soulofArms1.wav`, `holyLight_start.wav` (`Resources.Load` ignores case). The cues below use
   the rip's spelling, so the built file names match the asset names the effects' own AudioSources use (`holyLight`,
   `cast`).

---

## holyLight1 (Holy Light: the windup)

- Coroutine `RPC_holyLight` (`:27437-28500`, MoveNext `:27551-28434`).

| t (s) | state | what | source |
|---|---|---|---|
| 0 | 0 | `actionState attack`, cooldown; clip `holyLight1` (0.2 s fade); voice `cast1` or `cast2` (`Random.Range(0, 2)`); `castRing` Instantiated at the hero, world `Euler(270, 90, 0)`, `InitEffectControl` (owned); wait 0.6 | `:28247-28265`, `:28306-28361`, `:28374-28380`, `:28429` |
| 0.6 | 2 | clip `holyLight2` (loop, cut); the castRing's `root` animation looped; `mCastTime = magAdjust(6)`, cast bar | `:27584-27620` |
| 0.6 + cast | 2/3 | `IL_C6F`: `Time >= actionTime + mCastTime + 0.6` → holyLight3 (the next clip's entry); until then it polls every frame (`YieldDefault(3)`) | `:28022`, `:28226-28244`, `:28416` |

- Sum: 0 + 0.6 = 0.6 s to holyLight2; with the page's zero cast bar, holyLight3 starts in the same frame, also at 0.6 s.
- Effects:
  - `castRing`: **ready** (see Read this first 5). EffectControl life 60, afterLife 1, followPosition + followState. It
    plays its own `sounds/cast` (looping, 1.87 s). Holy Light **destroys** it when holyLight3 starts
    (`Object.Destroy(mCastRing)`, `:28050-28056`), so it gets `kill 0.6`. `kill` counts the effect's own age, so it
    works across the step change. Its `create` animation (0.47 s) plays on spawn. The switch to `root` at 0.6 s never
    shows, because it is destroyed in that same frame.
  - Small mismatch: the page plays an effect's sound once and doesn't stop it, so `cast.wav` runs its full 1.87 s, while
    the game's ends with the ring at 0.6 s.

```json
  "holyLight1": {
    "why": "Sheep.cs RPC_holyLight (:27437-28500): clip (0.2 s fade, :28265), voice cast1 / cast2 (Random.Range(0, 2), :28306-28361) and the Sheep's castRing field Instantiated at the hero, turned Euler(270, 90, 0) in world space, owned (:28374-28380; built from Resources sheep/effects/castRing, whose root is authored at that rotation; plays its own looping Sounds/cast) at 0; Yield 0.6 (:28429): holyLight2 and the cast bar magAdjust(6) (:27584-27620; 0 on the page), then holyLight3 in the same frame (:28022), which destroys the castRing (:28050-28056: kill 0.6)",
    "cues": [
    [0, "voice", "cast1|cast2"],
    [0, "fx", "castRing", {"rot": [270, 90, 0], "kill": 0.6}]
    ]
  },
```

Sure: high on the trace, medium-high on castRing = the field.

## holyLight2: no entry

The cast bar's loop (`:27584`). Nothing spawns or plays here in either skill. 0 s on the page.

## holyLight3 (Holy Light: the light comes down)

| t (s) | what | source |
|---|---|---|
| 0 | clip `holyLight3` (cut, once) | `:28028-28033` |
| 0 | `getFreeCast("holyLight", sLv)` (owner only): `Random.Range(0, 100) < lckAdjust(12 × 2)` with Free Cast 2; with Return Cast #431, `RPC_returnCast` Instantiates `returnCast` at the hero | `:28038-28044`, `:10054-10120`, `:11638-11660` |
| 0 | castRing destroyed | `:28050-28056` |
| 0 | `Sounds/holylight_start`, `PlayOneShot(clip, 1)`; not voice-gated, so it always plays | `:28062-28080` |
| 0 | `holylight_ring` createEffect at the hero, world `Euler(270, 90, 0)` | `:28094-28112` |
| 0 | voice `holylight1` or `holylight2` (`Random.Range(0, 2)`; pvoice-gated) | `:28126-28224`, played at `:28402` / `:28407` |
| 0 → 0.4 | `Yield(4, WaitForSeconds(0.4))` | `:28400` |
| 0.4 | clip `holyLight4` (loop, cut), `moveSpeed 0` (the next clip's entry) | `:27652-27672` |

- Effects:
  - `holylight_ring`: **ready**. EffectControl life 300, afterLife 0.5, followPosition + **followState**. It plays its
    own `sounds/holyLight` (looping, 2 s; once on the page). Parts: Animation (`create` 0.47 s on spawn), a
    SkinnedMeshRenderer whose bones run out to 12 m along the authored axis (a column of light, after the rotation),
    particles and a repeating RingEmitter.
  - The game ends it when the channel ends (standby, `RPC_holyLight0` `:10609-10640`). On the page that is the end of
    holyLight4's 3 s. The page resets `FX.t` at every step (`fxStart`, `index.html:3417`) and compares `cut` with
    `FX.t` (`:3160`). So a cut of **2.95** never fires during holyLight3 (FX.t only reaches 0.4 there) and fires at
    2.95 s into holyLight4: 0.4 + 2.95 = 3.35 s after the ring spawned. A cut at exactly 3 would be dropped with the
    step end (the same limit as the Wolf's bladeSong3 / bladeSurge cuts). This relies on the step clock resetting, so
    whoever edits the page should know about it.
  - Left out: at holyLight4 + 0.1 s the code restarts the ring's Animation on its `root` clip (2 s,
    `mHolyLightRing.animation.Play("root")`, `:27694-27700`). The page plays only an effect's default clip
    (`fxparts/mesh.js:115-130`). This needs a "play an effect's named Animation clip" cue.
  - `returnCast`: **ready** (EffectControl life 1, no followState, no sound).

```json
  "holyLight3": {
    "why": "Sheep.cs RPC_holyLight at the cast bar's end (actionTime + magAdjust(6) + 0.6, :28022; 0.6 s into holyLight1 on the page): clip (:28028); Free Cast 2 #132 with Return Cast #431 (the passives rule): getFreeCast (:28044) rolls Random.Range(0, 100) < lckAdjust(2 x 12) = 24 % (:10054-10120), a proc Instantiates returnCast at the hero (RPC_returnCast :11638-11660); the castRing destroyed (:28056); Sounds/holyLight_start, full volume (:28062-28080); holylight_ring at the hero turned Euler(270, 90, 0) in world space (createEffect :28100-28112; EffectControl life 300 + afterLife 0.5, followState; plays its own looping Sounds/holyLight); voice holyLight1 / holyLight2 (Random.Range(0, 2), :28157-28224, :28402-28407); Yield 0.4 (:28400): holyLight4. The light lasts until the hero moves or MP runs short (RPC_holyLight0 :10609-10640 sets standby), on the page holyLight4's 3 s: cut 2.95 on the step clock (FX.t restarts with holyLight4; a cut at the step's very end is dropped); left out: the ring's switch to its root animation 0.1 s into holyLight4 (:27700)",
    "cues": [
    [0, "fx", "returnCast", {"p": 0.24}],
    [0, "sound", "holyLight_start"],
    [0, "fx", "holylight_ring", {"rot": [270, 90, 0], "cut": 2.95}],
    [0, "voice", "holyLight1|holyLight2"]
    ]
  },
```

Sure: high on the trace and the times; medium on the ring's look (the column after the rotation hasn't been seen on
the page yet).

## holyLight4 (Holy Light: the channel)

| t (s) | what | source |
|---|---|---|
| 0 | clip `holyLight4` (loop); `Yield(5, 0.1)` | `:27652-27672`, `:28410` |
| 0.1 | ring's `root` animation (left out, above); `mUpdateTime = 0`; the tick loop in the same frame | `:27694-27706`, `:27722` |
| 0.1, 1.1, 2.1 ... | each tick (`mUpdateTime = now + 1`): MP −(4·sLv + 4) (×0.8 with Revised Magic); every enemy within 24 m: `holylight` Instantiated at it (first time) or its life +1 s, and the hit on one that already carries it | `:27796-27958` |
| every frame | ends on movement (`GetAxisRaw`) or `mp < 4·sLv + 4` → `RPC_holyLight0`: standby, `Sounds/holylight_end` | `:27749-27775`, `:10609-10670` |

- Ticks on the page: 0.1 s, then 0.1 + 1 = 1.1 s, then 1.1 + 1 = 2.1 s, so three ticks in the 3 s step. Under the
  page's rule ("three hits, at least 3 s"), `holyLight4*@3` is right.
- Left out: `holylight` (**ready**) at each enemy, which is target-side.
- The end sound: the page's 3 s step stands for "the hero moves", so `holyLight_end` goes at 2.95 s (a cue at the step's
  very end is dropped, as above).

```json
  "holyLight4": {
    "why": "Sheep.cs RPC_holyLight from holyLight4 (:27652; 0.4 s after holyLight3, :28400): ticks every 1 s from 0.1 s (:28410, :27706, :27804; 0.1 / 1.1 / 2.1 s in the page's 3 s): the MP cost and holylight at each enemy within 24 m, the hit on those already carrying it (:27834-27958; at the target, left out); the channel ends when the hero moves or MP < 4 x sLv + 4 (:27749-27775): RPC_holyLight0 sets standby and plays Sounds/holyLight_end (:10609-10670); the page's step ends at 3 s, so 2.95 (a cue at the step's very end is dropped)",
    "cues": [
    [2.95, "sound", "holyLight_end"]
    ]
  },
```

### Holy Light: the SEQ check

`"Holy Light: holyLight1@0.6 holyLight2*@0 holyLight3@0.4 holyLight4*@3"`

| step | page | game | ok |
|---|---|---|---|
| holyLight1 | 0.6 s, 0.2 s fade (a sequence's first step) | `Yield(2, 0.6)` `:28429`; `PlayAnimation("holyLight1", 0.2f)` `:28265` | yes |
| holyLight2 | loop, @0, cut | cast bar `magAdjust(6)` `:27611` (0 under the page's cast-bar rule); `PlayAnimation(.., 0)` `:27584` | yes |
| holyLight3 | 0.4 s, cut | `Yield(4, 0.4)` `:28400`; `PlayAnimation(.., 0)` `:28028`; clip 0.4 s long | yes |
| holyLight4 | loop, @3, cut | no limit, ticks 0.1 / 1.1 / 2.1 s; `PlayAnimation(.., 0)` `:27652` | yes (three ticks) |

Total on the page: 0.6 + 0 + 0.4 + 3 = 4.0 s.

---

## Lullaby's holyLight1 (Lullaby: the windup; needs the page fix)

- Coroutine `RPC_lullaby` (`:35225-35974`, MoveNext to `:35917`).

| t (s) | state | what | source |
|---|---|---|---|
| 0 | 0 | `actionState attack`, cooldown; clip `holyLight1` (0.2 s fade); voice `lullaby1` or `lullaby2` (`Random.Range(0, 2)`, pvoice-gated); `castRing` Instantiated at the hero, world `Euler(270, 90, 0)`, owned; wait 0.6 | `:35750-35771`, `:35809-35864`, `:35877-35883`, `:35901` |
| 0.6 | 2 | clip `holyLight2` (loop, cut); castRing `root` looped; `mCastTime = magAdjust(9)`, cast bar | `:35342-35405` |
| 0.6 + cast | 2/3 | `IL_7BF`: `Time >= actionTime + mCastTime + 0.6` → `lullaby` (next entry); else poll each frame | `:35643`, `:35729-35747`, `:35910` |

- Sum: 0 + 0.6 = 0.6 s; with a zero cast bar, `lullaby` starts at 0.6 s.
- No Free Cast roll here (it is at the lullaby clip).

Proposed key `@Lullaby:holyLight1` (or whatever key the page fix uses):

```json
  "@Lullaby:holyLight1": {
    "why": "Sheep.cs RPC_lullaby (:35225-35974): clip holyLight1 (0.2 s fade, :35768), voice lullaby1 / lullaby2 (Random.Range(0, 2), :35809-35864) and castRing at the hero, turned Euler(270, 90, 0) in world space, owned (:35877-35883) at 0; Yield 0.6 (:35901): holyLight2 and the cast bar magAdjust(9) (:35361-35405; 0 on the page), then lullaby in the same frame (:35643), which destroys the castRing (:35678-35684: kill 0.6)",
    "cues": [
    [0, "voice", "lullaby1|lullaby2"],
    [0, "fx", "castRing", {"rot": [270, 90, 0], "kill": 0.6}]
    ]
  },
```

## lullaby (Lullaby: the channel)

| t (s) | what | source |
|---|---|---|
| 0 | clip `lullaby` (loop, cut) | `:35649-35654` |
| 0 | with Return Cast #431: `getFreeCast("lullaby", 5)`, 24 % → `returnCast` at the hero | `:35659-35671`, `:10054-10120`, `:11638-11660` |
| 0 | castRing destroyed | `:35678-35684` |
| 0 | `lullaby_ring` createEffect at the hero, `Quaternion.identity` | `:35690-35708` |
| 0, 1, 2 ... | `mUpdateTime = 0`, then the tick loop in the same frame; each tick: SP −3 (2), MP −12 (9); `sleep 1` for `getDebuff(6, ...)` on every character within 12 m without `sleep`, the Sheep excepted (allies too) | `:35722-35725`, `:35502-35589` |
| every frame | ends on movement, or `mp < 12` / `sp < 3` → `RPC_lullaby0`: standby, **no sound** | `:35449-35499`, `:11688-11720` |

- Ticks on the page: 0, 1, 2 s, so three in the 3 s step. `lullaby*@3` is right.
- Effects:
  - `lullaby_ring`: **needs AlphaTimer** (the inventory; the probe stops at `lullaby_ring/lullaby_sheep_tri`). It plays
    its own looping `sounds/lullaby` (17.8 s). Left out. Future cue: `[0, "fx", "lullaby_ring", {"cut": 2.95}]` (its
    EffectControl, read past the AlphaTimer: life 99, afterLife 0, followState, followPosition; see Verification).
  - The `sleep` status on targets: target-side.
- With the ring left out, this clip shows only the Return Cast proc. See question 3 for a sound-only stand-in.

```json
  "lullaby": {
    "why": "Sheep.cs RPC_lullaby at the cast bar's end (actionTime + magAdjust(9) + 0.6, :35643; 0.6 s into holyLight1 on the page): clip (:35649); Return Cast #431 learned (the passives rule): getFreeCast(lullaby, 5) (:35665-35671) rolls 24 % (Free Cast 2, :10054-10120), a proc Instantiates returnCast at the hero (:11638-11660); the castRing destroyed (:35684, its holyLight1 cue's kill); the sleep tick at once and every 1 s (:35722-35725, :35502-35589: sleep 1 on every character within 12 m but the Sheep, allies too; at the targets); the channel runs until the hero moves or MP < 12 / SP < 3 (:35449-35499; RPC_lullaby0 :11688-11720, standby, no sound); left out: lullaby_ring at the hero (createEffect, identity, :35690-35708) needs AlphaTimer (it plays its own looping Sounds/lullaby)",
    "cues": [
    [0, "fx", "returnCast", {"p": 0.24}]
    ]
  },
```

### Lullaby: the SEQ check

`"Lullaby: holyLight1@0.6 holyLight2*@0 lullaby*@3"`

| step | page | game | ok |
|---|---|---|---|
| holyLight1 | 0.6 s, 0.2 s fade | `Yield(2, 0.6)` `:35901`; `PlayAnimation("holyLight1", 0.2f)` `:35768` | yes |
| holyLight2 | loop, @0, cut | cast bar `magAdjust(9)` `:35388` (0 on the page); `PlayAnimation(.., 0)` `:35361` | yes |
| lullaby | loop, @3, cut | no limit, ticks 0 / 1 / 2 s; `PlayAnimation(.., 0)` `:35649` | yes (three ticks) |

Total on the page: 0.6 + 0 + 3 = 3.6 s.

---

## purifyingTear (Purifying Tear)

- Coroutine `RPC_purifyingTear` (`:34699-35224`, MoveNext `:34807-35181`). No cast bar: the input starts it directly.

| t (s) | state | what | source |
|---|---|---|---|
| 0 | 0 | `actionState attack`, cooldown `agiAdjust(480)`; with Return Cast #431: `getFreeCast("purifyingTear", 5)`, 24 % → `returnCast`; clip `purifyingTear` (cut, once); voice `purifyingTear1` or `2` (`Random.Range(0, 2)`); wait 0.2 | `:35002-35026`, `:35039`, `:35080-35171`, `:35162` |
| 0.2 | 2 | `purifyingTear_ring` createEffect at the hero, hero rotation; wait 0.2 | `:34835-34853`, `:35167` |
| 0.4 | 3 | every enemy within 40 m drops its hate for the Sheep (no visual); wait 0.2 | `:34890-34934`, `:35157` |
| 0.6 | 4 | standby | `:34967` |

- Sums: 0 + 0.2 = 0.2; 0.2 + 0.2 = 0.4; 0.4 + 0.2 = 0.6 s. The clip is 0.8 s, so the single tile plays it to its end.
- `purifyingTear_ring`: **ready**. EffectControl life 2, afterLife 1, followPosition, no followState. It plays its own
  `sounds/purifyingTear`.

```json
  "purifyingTear": {
    "why": "Sheep.cs RPC_purifyingTear (:34699-35224): Return Cast #431 learned (the passives rule): getFreeCast(purifyingTear, 5) at the press (:35014-35026), 24 % (Free Cast 2, :10054-10120), a proc Instantiates returnCast at the hero (:11638-11660); clip (:35039) and voice purifyingTear1 / purifyingTear2 (Random.Range(0, 2), :35080-35171) at 0; Yield 0.2 (:35162): purifyingTear_ring at the hero (createEffect, hero rotation, :34835-34853; EffectControl life 2 + afterLife 1, no followState; plays its own Sounds/purifyingTear); Yield 0.2 (:35167): enemies within 40 m drop the Sheep's hate at 0.4 s (:34890-34934, no visual); Yield 0.2 (:35157): standby 0.6 s (:34967)",
    "cues": [
    [0, "fx", "returnCast", {"p": 0.24}],
    [0, "voice", "purifyingTear1|purifyingTear2"],
    [0.2, "fx", "purifyingTear_ring"]
    ]
  },
```

Sure: high.

---

## soulOfArms (Soul of Arms)

- Coroutine `RPC_soulOfArms_cast` (`:33696-34698`, MoveNext `:33826-34645`). It runs **after the shared cast**:
  the input starts `RPC_cast1("soulOfArms", ...)` (`:7992`; cast1 > cast2 with the bar `4 + 2·sLv`), whose end starts
  this coroutine (`:20966-20991`). Its first state requires `myCommand == "cast"` (`:33851`).

| t (s) | what | source |
|---|---|---|
| 0 | `myCommand soulOfArms`; clip `soulOfArms` (0.2 s fade, once); voice `soulOfArms1` or `2` (`Random.Range(0, 2)`; files `voices/soulofArms1-2`, 1.5 s / 9.8 s) | `:33861-33891`, `:33925-33980` |
| 0 | `soulOfArms_ring` createEffect at the hero, hero rotation | `:33993-34011` |
| 0 | `soulOfArms_trail` createEffect, then parented to `mount_Hand_R`, local position 0, rotation identity | `:34025-34058` |
| 0 | `soulOfArms` created **on the target** (`tChar.createEffect`) at its collider's bounds centre, `LookRotation(tDir)` | `:34073-34118` |
| 0 | the timer starts (`mSoulOfArmTimer = Time.time`), hit count 0 | `:34134-34139` |
| 4.6 / 5.1 / 5.3 / 5.5 / 5.7 / 6.2 | hits 1-6 on the target, `talAdjust(20·sLv + 10)`, KO 2 | `:34218`/`:34255`, `:34268`/`:34305`, `:34318`/`:34355`, `:34368`/`:34405`, `:34418`/`:34455`, `:34468`/`:34505` |
| 9.5 | hit 7, `talAdjust(50·sLv + 50)` | `:34518`/`:34555` |
| 9.8 | standby | `:34572-34598` |

- Each frame it checks that the target's `soulOfArms` effect still exists. If it's gone (or there was no target), the
  skill goes to standby at once (`:34146-34177`). The arms' effect holds the whole skill up.
- No Free Cast roll (the Bible's `unintended`: it never calls `getFreeCast`).
- Effects:
  - `soulOfArms_ring`: **ready**. EffectControl life 10, afterLife 0.5, followPosition + **followState**, so `cut 9.8`.
    The clip is 10 s long, so the cut fires before the tile ends. No sound of its own. Its ImageEmitters fire at
    0.3 / 1.7 / 3.2 / 5.0 / 6.2 / 8.7 s.
  - `soulOfArms_trail`: **ready** parts (EffectControl life 10, followState, TrailRenderer), but it rides the right-hand
    bone. Left out: needs a bone-attached cue, the same gap as the Wolf's Dark Edge hand aura. Future cue: at 0 on
    `mount_Hand_R`, cut 9.8.
  - `soulOfArms` (the summoned arms): **needs AlphaTimer**, and it sits **at the target**. It plays its own
    `sounds/soulOfArms` (11.5 s, one-shot), so leaving it out also drops the skill's main sound. Left out. See question 3.
    Its EffectControl (read past the AlphaTimer) is life 10 + afterLife 2, no followState: it outlives the 9.8 s, so
    on its own it never ends the skill early.
- The page's tile: `soulOfArms` is a single tile (not in SEQ). The game plays it after the cast: `cast1` (0.2 fade) >
  `cast2` loop (cast bar, 0 on the page) > `soulOfArms` (0.2 fade). See question 5.

```json
  "soulOfArms": {
    "why": "Sheep.cs RPC_soulOfArms_cast (:33696-34698), after the shared cast (RPC_cast1(soulOfArms) :7992, :20966-20991; it needs myCommand cast, :33851): clip (0.2 s fade, :33886), voice soulOfArms1 / soulOfArms2 (Random.Range(0, 2), :33925-33980; the rip's files voices/soulofArms1-2) and soulOfArms_ring at the hero (createEffect, hero rotation, :33993-34011; EffectControl life 10 + afterLife 0.5, followState; no sound) at 0; no Free Cast roll; a timer from 0 (:34134) paces the hits on the target at 4.6, 5.1, 5.3, 5.5, 5.7, 6.2 and the big one at 9.5 s (:34218-34555), standby at 9.8 s (:34572-34598), which ends the ring (followState: cut 9.8); left out: soulOfArms_trail parented to mount_Hand_R (:34025-34058) needs a bone-attached cue; soulOfArms, the summoned arms (plays its own Sounds/soulOfArms), on the target at its collider centre facing the cast direction (tChar.createEffect :34100-34118) needs AlphaTimer and is at the target; with no target, or once that effect is gone, the skill ends at once (:34146-34177)",
    "cues": [
    [0, "voice", "soulofArms1|soulofArms2"],
    [0, "fx", "soulOfArms_ring", {"cut": 9.8}]
    ]
  },
```

Sure: high on the trace (every threshold read from its own case).

---

## bookBash1 / bookBash2 / bookBash3 (Book Bash)

- Coroutine `RPC_bookBash` (`:37224-37900`, MoveNext `:37334-37898`). Each skill press (`shp_bookBash5`, `:7586-7633`)
  runs the coroutine once. There is no rank and no cooldown per cast.
- **How the game picks:** `Random.Range(0, 3)` (`:37523`) gives 0, 1 or 2, even chance. 1 = `bookBash1`
  (`:37526-37639`), 2 = `bookBash2` (`:37641-37754`), anything else (0) = `bookBash3` (`:37756-37865`). So each
  clip is 1/3 of the presses. Each branch plays its own clip, its own ring and its own voice; the rest is shared.

| t (s) | what | source |
|---|---|---|
| 0 | `animation.Rewind()`, the pick; clip `bookBashN` (cut, once); `bookBash_ringN` createEffect at the hero, hero rotation | `:37520-37555` / `:37647-37670` / `:37758-37781` |
| 0 | voice `bookBashN`, **only if** the shared Book Bash voice timer has run out: `Time > eQn8uWoLpl`, then the timer = now + 2 s (1 and 3) or + 1 s (2) | `:37569-37627` / `:37684-37742` / `:37795-37853` |
| 0 → 0.3 | `moveSpeed 0`; `Yield(2, 0.3)` | `:37867-37876`, `:37893` |
| 0.3 | the hit: `FindRecTarget` 2 × 2 × 2 m ahead; on each landed hit `RPC_bookBash_hit` (Instantiates `bookBash_hit` at the struck enemy) and SP +1; `Yield(3, 0.2)` | `:37341-37437`, `:11814-11824`, `:37896` |
| 0.5 | standby | `:37452-37490` |

- Sums: 0 + 0.3 = 0.3; 0.3 + 0.2 = 0.5 s. The clips are 1.0 / 0.7 / 0.7 s long.
- Effects: `bookBash_ring1` / `2` / `3`: **ready**. Each has EffectControl life 0.5, afterLife 1, followPosition, no
  followState; an Animation (0.3 s); a RingEmitter with a 0.2 s delay; a TrailRenderer. Each plays its own
  `sounds/bookBash`. `bookBash_hit` (ready) is at the target, so it is left out.
- The voice gate: a single play on the page always speaks. With the วนซ้ำ loop on, the page would say the line on every
  repeat (bookBash2 every 0.7 s), more often than the game's 1-2 s gate. The cue format has no voice cooldown. Minor.

```json
  "bookBash1": {
    "why": "Sheep.cs RPC_bookBash (:37224-37900): each press plays one of three clips, Random.Range(0, 3): 1 = bookBash1, 2 = bookBash2, 0 = bookBash3, even chance (:37523-37758); clip (no fade, :37532) and bookBash_ring1 at the hero (createEffect, hero rotation, :37537-37555; EffectControl life 0.5 + afterLife 1, no followState; plays its own Sounds/bookBash) at 0; voice bookBash1 only once 2 s have passed since the last Book Bash voice (:37569-37627; a single play always speaks); Yield 0.3 (:37893): the hit, bookBash_hit at each struck enemy (:37360-37437, :11814-11824; at the target, left out); Yield 0.2 (:37896): standby 0.5 s (:37470); no Free Cast roll",
    "cues": [
    [0, "voice", "bookBash1"],
    [0, "fx", "bookBash_ring1"]
    ]
  },
  "bookBash2": {
    "why": "Sheep.cs RPC_bookBash, Random.Range(0, 3) == 2 (:37523, :37641): clip (no fade, :37647) and bookBash_ring2 at the hero (createEffect, hero rotation, :37652-37670; life 0.5 + afterLife 1; plays its own Sounds/bookBash) at 0; voice bookBash2 only once 1 s has passed since the last Book Bash voice (:37684-37742); Yield 0.3 (:37893): the hit (bookBash_hit at the target, left out); Yield 0.2 (:37896): standby 0.5 s (:37470)",
    "cues": [
    [0, "voice", "bookBash2"],
    [0, "fx", "bookBash_ring2"]
    ]
  },
  "bookBash3": {
    "why": "Sheep.cs RPC_bookBash, Random.Range(0, 3) == 0 (:37523, :37756): clip (no fade, :37758) and bookBash_ring3 at the hero (createEffect, hero rotation, :37763-37781; life 0.5 + afterLife 1; plays its own Sounds/bookBash) at 0; voice bookBash3 only once 2 s have passed since the last Book Bash voice (:37795-37853); Yield 0.3 (:37893): the hit (bookBash_hit at the target, left out); Yield 0.2 (:37896): standby 0.5 s (:37470)",
    "cues": [
    [0, "voice", "bookBash3"],
    [0, "fx", "bookBash_ring3"]
    ]
  },
```

Sure: high.

---

## TTO (TTO1102)

The same coroutines, with the same constants where Ghidra shows them:

- `TTO1102:Sheep.<RPC_holyLight>d__178::MoveNext@0x1E8AA90`: waits 0.6, 0.4, 0.1, the 0.2 fade, the 0.8 Revised Magic
  factor.
- `TTO1102:Sheep.<RPC_lullaby>d__198::MoveNext@0x1E92030`: 0.6, 0.2, and Euler 270 / 90 (as radians, 4.712389 /
  1.5707964).
- `TTO1102:Sheep.<RPC_purifyingTear>d__196::MoveNext@0x1E96EC0`: 0.2.
- `TTO1102:Sheep.<RPC_soulOfArms_cast>d__193::MoveNext@0x1E9CCD0`: 4.6, 5.1, 5.3, 5.5, 5.7, 6.2, 9.5, 9.8.
- `TTO1102:Sheep.<RPC_bookBash>d__204::MoveNext@0x1E7CE90`: `Random.Range(0, 3)` with the same 1 / 2 / else branches.
  Its waits come from cached `Waits.Get()`, so their values can't be read there.

No TTO-only effect turned up in these five. TTO's Soul of Arms halves the damage taken (Bible, server balance), which
has no visual. I'd use BB's cues for TTO too.

## Bible findings (to offer the user; not written there)

1. **Holy Light and Lullaby: the cast bar, then an open channel** (`sheep-skill-reference.md` shp_holyLight1-2,
   shp_lullaby5). `actionTime + mCastTime + 0.6` (`:28022`, `:35643`) is when the light / the lullaby *starts*
   (holyLight3 / lullaby). From then on it ticks every 1 s with no time limit, until the Sheep moves or MP (and SP, for
   Lullaby) runs short (`:27722-27973`, `:35420-35596`). Lullaby's first sleep tick is at its start; Holy Light's first
   is 0.5 s after the light (`:28400`, `:28410`). Sure: high.
2. **Soul of Arms: timer-paced, not animation events** (shp_soulOfArms1-2): hits at 4.6, 5.1, 5.3, 5.5, 5.7, 6.2 and
   9.5 s after the soulOfArms clip starts, standby at 9.8 s (`:34134`, `:34218-34598`). It also ends at once if the
   summoned arms' effect on the target is gone (`:34146-34177`). Sure: high.
3. Book Bash's voice has a 2 s (bookBash1 / 3) or 1 s (bookBash2) cooldown (`:37569-37575`). This is a sound detail;
   the Bible probably doesn't need it.

## Open questions for the user

1. **holyLight1 for two skills:** OK to change the page so a sequence can carry its own cues for a shared clip (above,
   Read this first 1)? Otherwise the Lullaby tile says Holy Light's cast line, or each tile says the wrong line half
   the time.
2. **Free Cast / Return Cast:** show the Return Cast flash at 24 % on Holy Light, Lullaby and Purifying Tear, as the
   Wolf's Double Art? (Free Cast 2 and Return Cast learned, by the passives rule. Without Return Cast it would be the
   `freeCast` flash, at 24 % on Holy Light only.)
3. **Soul of Arms' summoned arms and Lullaby's ring both need AlphaTimer.** When AlphaTimer is built, should the arms
   (which spawn on the target) go 10 m ahead, about 1 m up, as the "a cast needs a target point" rule? Without them the
   skill is mostly a 10 s rune ring. Until then, do you want sound-only stand-ins, `[0, "sound", "soulOfArms"]` and
   `[0, "sound", "lullaby"]`? (Each is the effect's own sound: 11.5 s, and 17.8 s looping.)
4. **Book Bash:** keep three tiles, or one "Book Bash" tile that picks bookBash1 / 2 / 3 at random on each play, as the
   game does? The second needs a small page change (a random-pick tile).
5. **Soul of Arms' tile:** make it the game's sequence, `"Soul of Arms: cast1 cast2*@0 soulOfArms~"` (cast1's cues
   come from the Cast tile's research), instead of the bare 10 s clip?

## Verification (2026-11-10)

A second checker re-traced every cue's time, name, folder and placement from the decompile (`clip_flow.js` on each
coroutine, with the opaque predicates on each path worked by hand), the rip, the page and a fresh read-only probe. The
output is in `checks\fx_sheep_research\verify\` (`probe.json`, `probe_summary.txt`). `probe_skipunknown.py` reads an
effect past its AlphaTimer, and its output is `probe_alpha.json`.

**Checked and holding:**
- **Holy Light.**
  - holyLight1 (0.2 fade, :28265), cast1 / cast2 (:28306-28361) and the castRing field (:16721) Instantiated at world `Euler(270, 90, 0)` (:28374).
  - `Yield(2, 0.6)` (:28429). Then holyLight2 with `magAdjust(6)` (:27584, :27611), and holyLight3 at `actionTime + cast + 0.6` (:28022, :28028).
  - In that same frame: getFreeCast (isMine only, :28044), castRing Destroy (:28056), holylight_start at 1.0 (:28080), holylight_ring at world `Euler(270, 90, 0)` (:28112), and holylight1 / 2 (:28169, :28201, :28402 / :28407).
  - `Yield(4, 0.4)` (:28400) leads to holyLight4 (:27652), then `Yield(5, 0.1)` (:28410). After that: root animation (:27700), `mUpdateTime = 0` (:27706), and the tick in the same frame (`121947 − 156875 == −34928`, so no `continue`). Ticks at 0.1 / 1.1 / 2.1.
  - RPC_holyLight0: standby, then holylight_end (:10609-10670).
- **Lullaby.**
  - holyLight1 (:35768), lullaby1 / 2 (:35821, :35852), castRing (:35877), `Yield(2, 0.6)` (:35901).
  - Then holyLight2 with `magAdjust(9)` (:35361, :35388), and lullaby at `+ 0.6` (:35643, :35649).
  - getFreeCast only with #431 and isMine (:35659-35671), Destroy (:35684), lullaby_ring identity (:35708), and the tick at once (:35722-35725, :35502-35589).
  - RPC_lullaby0 sets standby and plays no sound (:11688-11720).
- **Purifying Tear.**
  - #431-gated getFreeCast (:35020-35026), clip (:35039) and voice (:35090, :35121) at 0.
  - `Yield(2, 0.2)` (:35162), then the ring with the hero's rotation (:34853).
  - `Yield(3, 0.2)` (:35167), then the hate drop at 40 m (:34895, :34934).
  - `Yield(4, 0.2)` (:35157), then standby (:34967). So 0 / 0.2 / 0.4 / 0.6.
- **Soul of Arms.**
  - Dispatch is `RPC_cast1("soulOfArms")` (:7992), bar `4 + 2·sLv` (:21540), then RPC_soulOfArms_cast (:20978).
  - It needs myCommand cast (:33851). The clip has a 0.2 fade (:33886), the voices are soulOfArms1 / 2 (:33937, :33968), and the ring is at the hero (:34011).
  - The trail goes on mount_Hand_R (:34048-34058). The arms go on the target (:34118).
  - The timer starts at :34134. The hits come at 4.6 / 5.1 / 5.3 / 5.5 / 5.7 / 6.2 / 9.5 (:34218-34555), standby at 9.8 (:34572-34598), and an early end once the arms are gone (:34146-34177).
- **Book Bash.**
  - `Random.Range(0, 3)` (:37523): 1 gives bookBash1 (:37526), 2 gives bookBash2 (:37641), anything else bookBash3 (:37756).
  - Each branch has its own clip, cut (:37532 / :37647 / :37758), and its own ring with the hero's rotation (:37555 / :37670 / :37781).
  - The voice timer is +2 / +1 / +2 s (:37575, :37690, :37801).
  - `Yield(2, 0.3)` (:37893), then the hit: FindRecTarget, ±1 m wide, 2 m long, 2 m high (:37373; Damage.cs:1416-1450). Then `Yield(3, 0.2)` (:37896) and standby (:37470).
  - No addTimeOut in the coroutine or the press (:7586-7633).
- **Free Cast / Return Cast.**
  - getFreeCast (:10054-10120) needs `shp_<type><sLv>` in SheepSkill. shp_holyLight2, shp_lullaby5 and shp_purifyingTear5 all exist (SheepSkill.cs).
  - getFreeCastLv returns 2 with #132. With #431 it plays RPC_returnCast at the hero (:11638-11660); without it, RPC_freeCast.
  - Lullaby and Purifying Tear call it only with #431, so "freeCast on Holy Light only" without Return Cast is right.
  - Soul of Arms and Book Bash never call it (the list of getFreeCast callers).
- **Rotation.** Unity `Euler(270, 90, 0)` = Ry(90)·Rx(270) = (x, y, z, w) (0.5, −0.5, −0.5, −0.5), the probe's root rotation for both castRing and holylight_ring. The page builds a root's rotation only from the cue's `rot`, in YXZ order (`index.html:3119-3123`).
- **The page.**
  - fxStart looks up by clip (`index.html:1139`, `:3416-3419`). A `skills` entry picks one skill per play (`:3407-3408`, `:3420-3424`).
  - Chain ids are `"@" + name` without spaces (`:1055`). kill counts the effect's age (`:3156`); cut counts the step clock (`:3160`).
  - The Animation part plays only the default clip (`fxparts/mesh.js:115-121`).
- **Prefabs (probe).**
  - castRing: EC life 60 / afterLife 1, followState; looping `cast`; `create` 0.47 s.
  - holylight_ring: life 300 / afterLife 0.5, followState; looping `holyLight`; a bone out to 12.08 m.
  - returnCast: life 1, no followState, no sound.
  - purifyingTear_ring: life 2 / afterLife 1, no followState; plays `purifyingTear`.
  - soulOfArms_ring: life 10 / afterLife 0.5, followState; ImageEmitter delays 0.3 / 1.7 / 3.2 / 5.0 / 6.2 / 8.7.
  - bookBash_ring1-3: life 0.5 / afterLife 1, RingEmitter delay 0.2, a 0.3 s Animation, `bookBash` sound.
  - soulOfArms_trail: life 10 / afterLife 0.5, followState (followPosition false).
- **Rip.**
  - voices/: cast1-2, holyLight1-2, lullaby1-2, purifyingTear1-2, soulofArms1 (1.51 s) and soulofArms2 (9.77 s), bookBash1-3.
  - sounds/: holyLight_start (1.3 s), holyLight_end (0.73 s), cast (1.87 s), holyLight (2.0 s), lullaby (17.82 s), soulOfArms (11.51 s).
- **Clip lengths** (`wardrobe/data/sheep/clips.json`): holyLight1 0.6, holyLight3 0.4, purifyingTear 0.8, soulOfArms 10.0, bookBash1 1.0, bookBash2 0.7, bookBash3 0.7.
- **TTO** (pseudo/Sheep.c):
  - Holy Light `d__178` has 0.6 / 0.4 / 0.1 / 0.2 / 0.8 / 24 / 6.
  - Lullaby `d__198` has 0.6 / 0.2 / 9 / 12, and `local_68 = 4.712389; fStack_64 = 1.5707964` into `Quaternion.Internal_FromEulerRad` (:13187-13192).
  - Purifying Tear `d__196` has 0.2 / 40 / 480.
  - Soul of Arms `d__193` has 4.6 / 5.1 / 5.3 / 5.5 / 5.7 / 6.2 / 9.5 / 9.8.
  - Book Bash `d__204` has `Random.Range(0, 3)` with `== 1` / `== 2` (Sheep.c:3176-3281).

**Corrections:**
- No time, name, folder, distance or line number in the 10 entries was wrong.
- Two "check when built" points are now settled:
  1. lullaby_ring's EffectControl: "owned and probably followState" -> life 99, afterLife 0, followState and followPosition true, AudioSource `lullaby` looped (`probe_alpha.json`). The future cut 2.95 is right.
  2. The summoned arms (`soulOfArms`): EffectControl life 10 + afterLife 2, no followState, `soulOfArms` one-shot (`probe_alpha.json`). They outlive the 9.8 s, so the per-frame check (:34146) doesn't end the skill early.

**A note on 24 %:** `lckAdjust(24)` = `floor(100 n / (n − 24 + 100))` with `n = 24 × (1 + 0.01 × clamp(LCK, 1, 512))` (CharacterControl.cs lckAdjust). That is 24 at LCK 1 and rises with LCK (38 at LCK 100). So 24 % is the lowest-LCK value, the same one the user chose for the Wolf's Double Art (decisions.md). Not changed.
