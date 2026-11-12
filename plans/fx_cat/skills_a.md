# Cat effects + sounds research: instantCast, gamble, Grand Casino Arcade, Forward Lunge, Backflip, Heart Ripper, Delta Strike, Finishing Blow

Researcher `skills_a`, 2026-11-13 (home PC). Scope: the clips `backflip`, `deltaStrike`, `finishingBlow1`,
`finishingBlow2`, `forwardLunge`, `gamble`, `grandCasinoArcade1-3`, `heartRipper1-2`, `instantCast` and every skill that
plays them. Research only (recipe steps 1-3). Line numbers are `D:\12tails\DecompiledSource\Cat.cs` unless another file
is named. Times are seconds from the start of the clip the cue is keyed by. Distance 0 = at the hero.

Read-only probes, in `checks\fx_cat_research\skills_a\` (git-ignored):
- `simplify.py <file> <coroutine> [out]`: one coroutine with the opaque predicates (`if (a - b != c)`) worked out and
  their dead branches dropped; `RPC_*.txt`, `doubleDown_fire.txt` are its output for every coroutine here.
- `probe_a.json`, `probe_b.json`, `probe_c.json`, `probe_bat_doom.json`: `wardrobe_fx.py cat --probe ...` (and `bat
  --probe doom`); `summ.py <json>` prints each effect's EffectControl, AudioSource, scripts and Animation clips.
- `probe_gca.py` / `probe_uv.py` (+ `probe_gca.json`, `probe_ds.json`): `wardrobe_fx.effect()` in memory for
  `grandCasinoArcade` and `deltaStrike`, with the two missing layouts (below); nothing written.
- `probe_mats.py` / `probe_mats.txt`: the materials and own sounds of the key effects.
- `keys.py` / `keys.txt`: BB's Resources container keys for the names here (the Finishing Blow voice check).
- `make_cues.py` -> `cues.json`: the paste-ready entries at the end, checked as valid JSON.

---

## Read this first

1. **Two pools.** `instantCast` = Fate Draw (:21563) and Double Down (:24693); `gamble` = Power Shuffle (:22403), Life
   Gamble (:22949) and Skill Gamble (:23481). No other BB coroutine plays them (every `PlayAnimation` in Cat.cs listed),
   and TTO's client names `instantCast` / `gamble` only in the same five coroutines (pseudo/Cat.c:6582, :7370, :13548,
   :21531, :23544). No SEQ holds these clips, so poolChains gives each member a tile of its own on the clip alone (Fate
   Draw, Double Down, Power Shuffle, Life Gamble, Skill Gamble) and hides the clip tiles (C.poolClips).
2. **Three SEQ timings in index.html are off** (the cues below assume the fixed ones):
   - Grand Casino Arcade: grandCasinoArcade2 is held **13.2 s**, not 13.5: grandCasinoArcade3 starts at 14.9 s
     (0.4 + 1.3 set-up, five spins of 2.0 + 0.7, the last 2.0 + 0.4: :28782, :28784, :28780, :28809, :28513); 15.2 s is
     ring2, 15.9 s standby. -> `"Grand Casino Arcade: grandCasinoArcade1 grandCasinoArcade2*@13.2 grandCasinoArcade3"`.
   - Heart Ripper: heartRipper2 starts at **0.4 s** (Yield 0.2 + 0.2, :33126, :33124, RPC_heartRipper2 :32891); the
     heartRipper1 clip is 0.5 s. -> `"Heart Ripper: heartRipper1@0.4 heartRipper2"`.
   - Finishing Blow: the same, finishingBlow2 at **0.4 s** (:38494, :38485, :38323; clip 0.5 s). -> `"Finishing Blow:
     finishingBlow1@0.4 finishingBlow2"`.
   Every switch is a cut in the game (`PlayAnimation(x, 0)`), which the page's plain step already is.
3. **Parts missing** (specs under "Parts"):
   - `Cat_grandCasinoArcade` (the machine's script: its blinking lights) plus the coroutine's `fire` / `destroy`
     animation calls on the machine; the inventory lists the script.
   - `UVScroll` (Delta Strike's triangle; the inventory lists it).
   - The Bat's `doom` effect for the Cat (Casino Doom): a cross-folder lookup in `wardrobe_fx.py`, no page part.
   The two layouts `wardrobe_fx.py` needs are proven (they use up exactly the field bytes, `probe_uv.py`):
   - `Cat_grandCasinoArcade` (8 bytes): `mRenderer` r (Cat_grandCasinoArcade.cs:144).
   - `UVScroll` (8 bytes): `scroll_x` f, `scroll_y` f (UVScroll.cs:67-70); the triangle's are 1, 1.
4. **Effects not in `fx_inventory.md` but ready:** `fortune` (the fortune status's emblem, CharacterControl.cs:36239),
   `forwardLunge_dust` (a hero-prefab field, Cat.cs:15857: `checks/fx_cat_research/attacks_emotes/probe_fields.txt`
   field 2 = GameObject forwardLunge_dust, the same name in Resources cat/effects), `doom` (Bat folder,
   CharacterControl.cs:40491).
5. **Passives on, max rank:** Lady Luck #412 turns Fate Draw's ring and voices into ladyLuck_ring + ladyLuck1|2; Roll the
   Dice #432 makes Double Down's strike doubleDown2_hit; Even Odds #422 takes Life / Skill Gamble's loss (evenOdds_hit in
   place of the loss effect). Ranks: Fate Draw 4, Power Shuffle 2, Double Down 2, Grand Casino Arcade 2, Forward Lunge 2,
   Backflip 2, Heart Ripper 2, Delta Strike 2 (each only changes numbers here, except GCA's spin count and Delta
   Strike's 1.5 scale and cat positions).
6. **Where the "target" effects go.** Heart Ripper and Finishing Blow put the Cat **at** the target (:32868-32891,
   :38300-38323): the wardrobe hero stays put, so the target comes to her. Finishing Blow's three `finishingBlow_hit`
   spawn at the Cat herself (:38751, :38851, :38958) whatever they hit: at the hero. Heart Ripper's two stabs draw
   `nAttack_hit` at ClosestPointOnBounds(Cat + 1 up) of a target she stands inside, which is her own point 1 m up (the
   target body of plans/fx_bat/decisions.md 4: radius 0.3). Forward Lunge's hits are melee (3 / 4 m boxes) and never
   reach the 10 m target: left out, as the Wolf's, Bison's and the Cat's combo. Double Down's strikes are on random
   characters **the Cat included** (below): the 10 m target or the Cat, even chance. Delta Strike does **not** teleport
   (mPos = her own position, :7078) and draws nothing on its targets. Open question 1.
7. **Double Down can strike the Cat.** doubleDown_fire picks among on-screen characters from `FindAreaTarget(hero, 24, 10,
   130816)` (:25047-25106); FindAreaTarget scans every Enemy- and Player-tagged object of the mask (Damage.cs:963-1120),
   the caster too (the Bible's Damage Roulette note relies on the same, `gameObject3 == this.gameObject`). With one
   target that is a coin flip per strike. Open question 2.
8. **BB's Finishing Blow is silent.** It loads `Voices/finishingBlow1 / 2` (:39288, :39319); BB's data has only
   `voices/finisingblow1 / 2` (keys.txt), so the loads fail. TTO loads `finisingBlow1 / 2` (pseudo/Cat.c:8376-8388).
   Cued with TTO's names, as the Sheep's decision 10.
9. **Grand Casino Arcade's outcomes depend on LCK** (`Random.Range(0, clamp(LCK, 0, 255))` :27993): at LCK 1 every spin
   is Casino Doom (no number at all). Cued at the 255 cap (Doom 5, 111 45, 222 40, 333 30, 777 135 of 255). Open
   question 3.

---

## instantCast: the pool (`skills`): Fate Draw, Double Down

Clip 1.0 s. Both coroutines cut the clip in (`PlayAnimation("instantCast", 0)`, wrapMode Once).

### Fate Draw (`$RPC_fateDraw$21755`, :21254-21917; rank 4 with Lady Luck #412)

| t | what | lines |
|---|---|---|
| 0 | actionState attack, cooldown, `PlayAnimation("instantCast", 0)` | :21545-21566 |
| 0 | `hasSkill(412)`: ladyLuck_ring `createEffect(hero position, hero rotation)` (else fateDraw_ring :21714-21726) | :21575-21597 |
| 0 | voice ladyLuck1 / ladyLuck2 (`Random.Range(0, 2)`; else fateDraw1 / fateDraw2 :21769-21863); wait 0.4 | :21640-21681, :21853, :21856, `Yield(2, 0.4)` :21865 |
| 0.4 | owner only: everyone of the Cat's layer within 15 m (the Cat too) gets fortune, level sLv + 1, chaAdjust(30) | :21414, :21447-21453 |
| 0.4 | the fortune status: `Instantiate(fortune, position + 2 up, identity)` on each receiver | CharacterControl.cs:36235-36247 |
| 0.7 | standby (wait 0.3) | `Yield(3, 0.3)` :21849, :21493 |

- ladyLuck_ring: EffectControl life 1 + afterLife 1, followPosition, no followState; plays its own `Sounds/fateDraw`;
  an EmitterControl'd legacy emitter (Delay 0.3). Ready.
- fortune: one EmblemEmitter (Life 0.5, Delay 0.1, its texture `fortune`), no EffectControl: the Wolf's valor_emblem
  case, `{"y": 2}`. Ready (not in the inventory: CharacterControl.cs loads it).
- No roll, no random pick but the voice.

### Double Down (`$RPC_doubleDown$21824`, :24447-24886; rank 2 with Roll the Dice #432)

| t | what | lines |
|---|---|---|
| 0 | clip (cut), doubleDown_ring `createEffect(hero, hero rotation)` | :24693, :24711-24723 |
| 0 | voice doubleDown1 / doubleDown2 (`Random.Range(0, 2)`); wait 0.3 | :24766-24852, `Yield(2, 0.3)` :24846 |
| 0.3 | owner: `StartCoroutine(doubleDown_fire(sLv))`; wait 0.1 | :24599, `Yield(3, 0.1)` :24843 |
| 0.4 | standby | :24623 |
| 0.3 + 0.4 k, k = 0..7 | doubleDown_fire (:24887-25205): `sLv x 3 + 2` = 8 strikes (:25027), each `FindAreaTarget(hero, sLv x 6 + 12 = 24, 10, 130816)` (:25047), on-screen only (:25075), one at random (:25106), `RPC_doubleDown_hit(its position)` (:25124); wait 0.4 (:25155) | |
| same | RPC_doubleDown_hit (:25206-25517): mRange 2 with #432 (:25389-25396), `Instantiate(doubleDown2_hit, hitPos, identity)` (:25405-25415; else doubleDown1_hit :25441-25451); the damage 0.4 s later (:25358, `Yield(2, 0.4)` :25470) | |

- Strikes at 0.3, 0.7, 1.1, 1.5, 1.9, 2.3, 2.7, 3.1 s, each on the 10 m target or the Cat (Read this first 7): one roll
  per strike (`dd1` .. `dd8`), the target's at `d 10`, the Cat's at 0. Identity rotation: drawn in the hero's facing
  (APPROXIMATED, as the Penguin's identity spawns).
- doubleDown2_hit: life 2 + 1, Animation (`Base Stack`, 1 s) + SkinnedMeshRenderer (the cactus, opaque), Ring /
  Image emitters, an EmitterControl'd legacy emitter (Delay 0.4); plays its own `Sounds/doubleDown2`. Ready.
- doubleDown_ring: life 1, no sound. Ready.
- The strikes go on after standby (the coroutine checks only the Cat's death, :24994-25002): the tile's tail keeps them.

### The pool entry

See `instantCast` in the paste-ready block.

---

## gamble: the pool (`skills`): Power Shuffle, Life Gamble, Skill Gamble

Clip 1.0 s, cut in. All three: the ring and the voice at 0, the outcome at 0.4 s (`Yield(2, 0.4)`), standby at 0.7 s
(`Yield(3, 0.3)`).

### Power Shuffle (`$RPC_powerShuffle$21769`, :21918-22624; rank 2)

| t | what | lines |
|---|---|---|
| 0 | clip (cut) :22403; `removePowerStatus` :22415; powerShuffle_ring `createEffect(hero, hero rotation)` :22424-22436 | |
| 0 | voice powerShuffle1 / powerShuffle2 (`Random.Range(0, 2)`) | :22479-22520, `Yield(2, 0.4)` :22564 |
| 0.4 | owner: one stat up, another down (`Random.Range(1, 9)`, `(plus + Random.Range(0, 7)) % 8 + 1` :22072-22077; Even Odds sLv + 1 :22087-22093); the xUp / xDown statuses draw nothing (CharacterControl.cs:33176-33296: deltaAtk ... only) | :22099-22306 |
| 0.7 | standby | `Yield(3, 0.3)` :22576, :22333 |

powerShuffle_ring: life 1, no followState, plays `Sounds/powerShuffle`. Ready.

### Life Gamble (`$RPC_lifeGamble$21783`, :22625-23146; Even Odds #422 on)

| t | what | lines |
|---|---|---|
| 0 | clip (cut) :22949; lifeGamble_ring `createEffect(hero, hero rotation)` :22967-22979 | |
| 0 | voice lifeGamble1 / lifeGamble2 | :23022-23063, `Yield(2, 0.4)` :23111 |
| 0.4 | owner: `lckAdjust(50) > Random.Range(0, 100)` (:22768): won: heal 50 % (:22774), `RPC_lifeGamble_heal` (:22779) = lifeGamble_heal at the hero (:9156-9180) | |
| 0.4 | lost: `hasSkill(422)` (:22801) and Even Odds' timer free (`isTimeOut("evenOdds") == 0` :22807): `RPC_evenOdds` (:22813) = evenOdds_hit at the hero, Even Odds' 90 s timer (:9335-9360, :9342); the loss is skipped (:22829 -> :23100). Without it: 50 % HP lost (:22834) and `RPC_lifeGamble_hit` (:22839) = lifeGamble_hit at the hero (:9199-9225) | |
| 0.7 | standby | `Yield(3, 0.3)` :23100, :22879 |

- lifeGamble_ring has **followState** (life 1): cut at standby, 0.7 s. Plays `Sounds/gamble_ring`.
- lifeGamble_heal (life 2, `Sounds/gamble_heal`), evenOdds_hit (life 2, `Sounds/evenOdds`), lifeGamble_hit (life 2,
  `Sounds/gamble_hit`): ready.
- The roll: lckAdjust(50) = 50 at LCK 1 (the Wolf's / Sheep's lowest-LCK convention; 78 % at LCK 255). Even Odds catches
  every loss in the wardrobe (no timers kept). Open questions 4, 5.

### Skill Gamble (`$RPC_skillGamble$21790`, :23147-23681; Even Odds #422 on)

The same shape: clip :23481, skillGamble_ring :23499-23511 (followState, life 1, `Sounds/gamble_ring`), voice
skillGamble1 / skillGamble2 :23554-23595, `Yield(2, 0.4)` :23630; at 0.4 `Random.Range(0, 100) < lckAdjust(50)` (:23290):
won: MP / SP x 1.5 and `RPC_skillGamble_heal` (:23306) = skillGamble_heal at the hero (:9249-9275, `Sounds/gamble_success`);
lost: Even Odds (:23328-23340) = evenOdds_hit; without it MP / SP halved and skillGamble_hit (:23361-23371, :9292-9318,
`Sounds/gamble_fail`); standby 0.7 s (`Yield(3, 0.3)` :23636, :23411).

### The pool entry

See `gamble` in the paste-ready block. The two gambles share the roll name `gamble` (one skill per play, so no clash).

---

## grandCasinoArcade1-3: Grand Casino Arcade (`$RPC_grandCasinoArcade$21905`, :27674-28900; rank 2)

One coroutine, three clips; the SEQ `grandCasinoArcade1 grandCasinoArcade2*@13.2 grandCasinoArcade3` (Read this first 2).
Times below are from the skill's start, then per clip.

| t (skill) | what | lines |
|---|---|---|
| 0 | actionState attack, cooldown 600 s; **the Cat turns to face the camera** (`LookAt(mPos - vFlat(Camera.main.forward))`); `PlayAnimation("grandCasinoArcade1", 0)` | :28603-28624 |
| 0 | noDamage / noForce, `sLv x 5 + 7` = 17 s (draw nothing: CharacterControl.cs:32931-32940 releaseTarget only) | :28633-28636 |
| 0 | grandCasinoArcade_ring1 `Instantiate(hero, hero rotation)` | :28645-28657 |
| 0 | voice grandCasinoArcade1 / grandCasinoArcade2 (`Random.Range(0, 2)`); wait 0.4 | :28700-28777, `Yield(2, 0.4)` :28796 |
| 0.4 | the machine: grandCasinoArcade `createEffect(hero, hero rotation)`; its child `grandCasinoArcade` found (`transform.Find`); camera zoom / shake / blur (player only); wait 1.3 | :27826-27919, `Yield(3, 1.3)` :28782 |
| 1.7 | `PlayAnimation("grandCasinoArcade2", 0)`, wrapMode Loop; i = 0 | :27946-27956 |
| 1.7 + 2.7 i, i = 0..4 | (IL_9BB, i < sLv x 2 + 1 = 5 :28507) the machine's `animation.Play("fire")` :28554; `Sounds/grandCasino2` `PlayOneShot(clip, 2)` :28566-28578; wait 2 | `Yield(4, 2)` :28784 |
| 3.7 + 2.7 i | owner: `mCasinoResult = Random.Range(0, clamp(LCK, 0, 255))` :27993: < 5 Casino Doom (doom on the Cat's layer within 24 m, the Cat too, level + 1, 60 s, :27998-28048; `RPC_grandCasinoArcade_hit(0)` :28059 draws nothing), < 50 hit 1, < 90 hit 2, < 120 hit 3, else hit 7 (:28077-28203; `RPC_grandCasinoArcade_hit(n)`); the damage (:28209-28265); camera blur; then wait 0.7 (0.4 after the fifth) | `Yield(5, 0.7)` :28780, `Yield(6, 0.4)` :28809, i++ :28596 |
| 14.9 | (i = 5) `PlayAnimation("grandCasinoArcade3", 0)`, the machine's `animation.Play("destroy")`; wait 0.3 | :28513-28531, `Yield(7, 0.3)` :28786 |
| 15.2 | camera shake, zoom back; grandCasinoArcade_ring2 `Instantiate(hero, hero rotation)` (its error text says ring1); wait 0.7 | :28369-28418, `Yield(8, 0.7)` :28793 |
| 15.9 | standby | :28454 |

`RPC_grandCasinoArcade_hit(hitLv)` (:9648-9800): hitLv 1 / 2 / 3 / 7 = `Instantiate(grandCasinoArcade_hit<n>, hero
position + 4.5 up, hero rotation)` (:9669-9679, :9706-9716, :9743-9753, :9784-9794); any other level breaks out, so
Casino Doom draws no number (the data's `grandcasinoarcade_hit0` effect and `sounds/grandCasino_hit0` are never used).
The Doom status's look: `createEffect(Bat/Effects/doom, collider.bounds.center, identity)` (CharacterControl.cs:40487-40504)
on every receiver; here the Cat's, about 0.6 m up (the CharacterController centre of the standing rules).

Per clip (the cue keys):
- **grandCasinoArcade1** (0-1.7): ring1 and the voice at 0, the machine at 0.4 (`anims` below).
- **grandCasinoArcade2** (held 13.2 s): sounds at 0, 2.7, 5.4, 8.1, 10.8; results at 2.0, 4.7, 7.4, 10.1, 12.8.
- **grandCasinoArcade3** (from 14.9): ring2 at 0.3; standby at 1.0.

Effects:
- grandCasinoArcade (the machine): EffectControl life 16 + afterLife 1, **followState**; node 1 `grandCasinoArcade`
  holds an Animation (clips `create` 1.467 s, played on spawn; `fire` 2.5 s; `destroy` 1.0 s, which sinks the root to -5),
  the SkinnedMeshRenderer (materials GrandCasinoArcade1 FX/Phoenix, GrandCasinoArcade2 / 3 additive) and
  `Cat_grandCasinoArcade`; a one-shot legacy smoke. **Needs the part** (below). No cut: the hero's action changes at
  15.9 s, inside grandCasinoArcade3's step, and the page compares `cut` with the current step's clock (FX.t restarts
  each step), so a cut of 15.5 would never fire and one of 1.0 would fire in the first step; destroy has sunk the
  machine by 15.9 anyway, and its life ends at 16.4 + 1 (the game's: 15.9 + 1).
- grandCasinoArcade_ring1 / _ring2: life 3, own `Sounds/grandCasino1`. Ready.
- grandCasinoArcade_hit1 / 2 / 3 / 7: life 2, an EmblemEmitter (the 111 / 222 / 333 / 777 picture) + rings + a legacy
  burst; own `grandCasino_hit1` (1, 2, 3) / `grandCasino_hit7`. Ready.
- doom (Bat): life 2, three ImageEmitters, own `Sounds/doom_cast` (bat/sounds, found by the rip-wide search). Ready,
  once `wardrobe_fx.py` can find it for the Cat (Parts 3).

Random picks: per spin one draw over 255 (the cap): a roll `casino<i>` with p 5/255 = 0.0196 for doom, and on the rest
one name from 50 = 9 x hit1, 8 x hit2, 6 x hit3, 27 x hit7 (45 : 40 : 30 : 135). Open question 3.

Left out: the camera's AutoZoom, AddCamereShake, AddMotionBlur (player's camera only); the damage; the turn to the
camera (the wardrobe hero keeps her facing; open question 7).

---

## forwardLunge: Forward Lunge (`$RPC_forwardLunge$21957`, :29924-31010; rank 2)

| t | what | lines |
|---|---|---|
| 0 | clip (cut) :30796; voice forwardLunge1 / forwardLunge2 (`Random.Range(0, 2)`); wait 0.3 | :30837-30924, `Yield(2, 0.3)` :30941 |
| 0.3 | moveSpeed 9, i = 0 | :30071, :30106 |
| 0.3 + 0.1 i, i = 0..3 | hits in `FindRecTarget(hero, fwd, 1, 1, 3, 2)` (:30518-30704, melee); `Instantiate(forwardLunge_dust, hero, hero rotation)` :30721 (the prefab field); nAttack_dust at hero + TransformDirection(+0.2, 0, 0) when i is odd, (-0.2, 0, 0) when even, hero rotation (:30744-30759); wait 0.1, i++ | `Yield(3, 0.1)` :30930, :30132 |
| 0.7 | i = 4: moveSpeed 12 :30260; the last hit `FindRecTarget(..., 4, 2)` :30271-30457; nAttack_dust at the hero :30480-30492; wait 0.1 | `Yield(4, 0.1)` :30915 |
| 0.8 | moveSpeed 6; wait 0.2 | :30158, `Yield(5, 0.2)` :30935 |
| 1.0 | standby | :30184 |

- The Cat dashes 3.6 + 1.2 + 1.2 = 6 m; the wardrobe hero stays (Feral Assault / Blink / the Bison's convention), so all
  the dust is placed at the standing hero (each dust spawns at the hero's position of its moment in the game).
- forwardLunge_dust: life 0.5, two LineEmitters. nAttack_dust: life 1, one ImageEmitter. Ready.
- Left out: forwardLunge_hit / backStab_hit (Backstab #413 behind the target, :30304-30373) at a target the 3 / 4 m
  boxes never reach from the standing hero.

## backflip: Backflip (`$RPC_backflip$21996`, :32024-32651; rank 2)

| t | what | lines |
|---|---|---|
| 0 | the Cat turns her back to the target (`LookAt(mPos - vFlat(tDir))`), clip (cut), `removeLockStatus(5)` | :32402-32432 |
| 0 | owner only: `Sounds/backflip` `PlayOneShot` (the rip's `sounds/backFlip.wav`) | :32435-32459 |
| 0 | voice backflip1 / backflip2 (`Random.Range(0, 2)`; the rip's `backFlip1 / 2`); wait 0.15 | :32503-32592, `Yield(2, 0.15)` :32582 |
| 0.15 | moveSpeed 4; wait 0.25 | :32171, `Yield(3, 0.25)` :32597 |
| 0.4 | moveSpeed 6 + 4 x 2 = 14, collisions off in a 4 m strip; wait 0.4 | :32198-32243, `Yield(4, 0.4)` :32600 |
| 0.8 | collisions back, stop; wait 0.1 | :32269-32329, `Yield(5, 0.1)` :32586 |
| 0.9 | standby | :32350 |

No effect prefab. `"sound"` + `"voice"` only (the same name `backflip` is a clip and a sound; voices are saved as
`v_<name>`).

---

## heartRipper1, heartRipper2: Heart Ripper (rank 2; on a knocked-out target, :7340-7373)

### heartRipper1 (`$RPC_heartRipper1$22011`, :32652-33168)

| t | what | lines |
|---|---|---|
| 0 | clip (cut) :32995; voice heartRipper1 / heartRipper2 (`Random.Range(0, 2)`); wait 0.2 | :33036-33128, `Yield(2, 0.2)` :33126 |
| 0.2 | moveSpeed 5; wait 0.2 | :32809, `Yield(3, 0.2)` :33124 |
| 0.4 | stop; mPos = target - forward x target.collider.bounds.extents.x (getSpawnPos); `StartCoroutine(RPC_heartRipper2(mPos, ...))` | :32836-32891 |
| 0.9 | (its standby check fails: myCommand is heartRipper2 by then) | :32913-32935 |

### heartRipper2 (`$RPC_heartRipper2$22023`, :33169-33799), from 0.4 s

| t | what | lines |
|---|---|---|
| 0 | the Cat at mPos (the target's near face), clip (cut), moveSpeed 2, collision with the target off; wait 0.2 | :33660-33711, `Yield(2, 0.2)` :33733 |
| 0.2 | stop; owner: `FindAreaTarget(Cat, 1, 5)`, each hit: `RPC_nAttack_hit(ClosestPointOnBounds(Cat + up))`; wait 0.4 | :33327-33432, `Yield(3, 0.4)` :33737 |
| 0.6 | moveSpeed -8; the second stab the same way; wait 0.2 | :33454-33544, `Yield(4, 0.2)` :33739 |
| 0.8 | stop, collision back; wait 0.2 | :33566-33592, `Yield(5, 0.2)` :33731 |
| 1.0 | standby | :33608 |

- Where the stab lands: she starts 0.3 m short of the target's centre and moves 2 x 0.2 = 0.4 m, so at both stabs she is
  0.1 m past it, inside its bounds (radius 0.3, height 1 at centre 0.6: plans/fx_bat/decisions.md 4); ClosestPointOnBounds
  of a point inside is the point: her own position, 1 m up. `RPC_nAttack_hit` (:8253-8325): `Instantiate(nAttack_hit,
  hitPos, transform.rotation)` and `Sounds/nAttack_hit` (throttled to one per 0.1 s, :8292-8312; no owner gate).
- nAttack_hit: life 1, two ImageEmitters. Ready.
- Open question 1 (at the hero vs at the 10 m point).

---

## deltaStrike: Delta Strike (`$RPC_deltaStrike$22138`, :36952-38094; rank 2)

mPos is the Cat's own position (`RPC_deltaStrike(this.KOIRnET4pM.position, vector2, 0, num2)` :7078; `position = mPos`
:37720): no teleport.

| t | what | lines |
|---|---|---|
| 0 | clip (cut) :37730; noForce 3 s :37750; camera colour ramp (player) :37766; voice deltaStrike1 / deltaStrike2 (`Random.Range(0, 2)`); wait 0.3 | :37803-37996, `Yield(2, 0.3)` :37963 |
| 0.3 | deltaStrike_ring `createEffect(hero, hero rotation)`; lock (3 s) on the enemies in `FindRecTarget(hero, fwd, 1, 3 sLv + 3, 2 sLv + 4, 6)`; wait 0.5 | :37105-37186, `Yield(3, 0.5)` :37969 |
| 0.8 | lock again; wait 0.5 | :37220-37265, `Yield(4, 0.5)` :37954 |
| 1.3 | deltaStrike_cat twice: cPos = mPos + TransformDirection(+-(1.5 sLv + 1.5), 0, 2 sLv + 4) = (+-4.5, 0, 8), dropped to the ground (raycast, layer 1), rotation LookRotation(cPos - (mPos + 4.5 forward)) = yaw +-atan2(4.5, 3.5) = +-52.1 deg; lock again; wait 0.2 | :37305-37430, `Yield(5, 0.2)` :37986 |
| 1.5 | deltaStrike `Instantiate(hero + 0.5 forward, hero rotation)`, localScale 1.5 at sLv 2; wait 0.6 | :37470-37500, `Yield(6, 0.6)` :37980 |
| 2.1-2.6 | six ticks 0.1 s apart (damage only) | :37532-37541, :37872-37941, `Yield(7, 0.1)` :37967 |
| 2.9 | the finisher (damage only), camera blur | `Yield(8, 0.2)` :37988, :37574-37630 |
| 3.0 | standby | `Yield(9, 0.1)` :37992, :37648 |

- deltaStrike_ring: life 3 + afterLife 2, followPosition, **followState**: cut at standby, 3.0 s (inside the 4.0 s clip);
  three EmblemEmitters (the delta pictures at 0 / 0.3 / 0.6 s), lines, rings; own `Sounds/deltaStrike`. Ready.
- deltaStrike_cat: life 2, StaticMesh + AlphaTimer (MaxAlpha 0.5) + a ShadowRay ring (shader 205, the multiply the Bat's
  parts added). Ready.
- deltaStrike: life 2; node 1 Animation `root` (2 s); `deltaStrike_tri` SkinnedMeshRenderer (material `deltastrike`,
  alpha blended) with **UVScroll** (1, 1); three TrailEmitters (Ray4), a ShatterMesh pane with AlphaTimer, a ShadowLine2
  ring (205). **Needs UVScroll** (below); everything else is built.
- Left out: the lock status (draws nothing), the camera colour ramp and blurs.

---

## finishingBlow1, finishingBlow2: Finishing Blow (#423, Class C; on a knocked-out target, :6448-6495)

### finishingBlow1 (`$RPC_finishingBlow1$22168`, :38095-38530)

| t | what | lines |
|---|---|---|
| 0 | clip (cut) :38427; finishingBlow_ring1 `Instantiate(hero, hero rotation)`; wait 0.2 | :38439-38467, `Yield(2, 0.2)` :38494 |
| 0.2 | moveSpeed 5; wait 0.2 | :38241, `Yield(3, 0.2)` :38485 |
| 0.4 | stop; mPos at the target (:38300-38305); `StartCoroutine(RPC_finishingBlow2(mPos, ...))` | :38268-38341 |

No voice in finishingBlow1. finishingBlow_ring1: life 1, own `aura1` (Resources sound/fx). Ready.

### finishingBlow2 (`$RPC_finishingBlow2$22178`, :38531-39461), from 0.4 s

| t | what | lines |
|---|---|---|
| 0 | the Cat at mPos, clip (cut), collision off; finishingBlow_ring2 `createEffect(hero, hero rotation)` | :39162-39243 |
| 0 | voice `finishingBlow1 / finishingBlow2` (`Random.Range(0, 2)`): missing in BB's data (Read this first 8); TTO's `finisingBlow1 / 2`; wait 0.3 | :39278-39394, `Yield(2, 0.3)` :39388 |
| 0.3 | hit 799 (owner) and `Instantiate(finishingBlow_hit, the Cat's position, identity)` (always) ; wait 0.3 | :38678-38765, `Yield(3, 0.3)` :39381 |
| 0.6 | the same; wait 0.5 | :38788-38865, `Yield(4, 0.5)` :39354 |
| 1.1 | the same (+ OpenWound); wait 0.3 | :38888-38972, `Yield(5, 0.3)` :39373 |
| 1.4 | moveSpeed -8, hit 199 (no effect); wait 0.2 | :38995-39044, `Yield(6, 0.2)` :39379 |
| 1.6 | stop, collision back; wait 0.2 | :39068-39094, `Yield(7, 0.2)` :39361 |
| 1.8 | standby | :39110 |

- finishingBlow_ring2: life 3 + 1, own `Sounds/finishingBlow`. finishingBlow_hit: life 1 + 1, own
  `Sounds/finishingBlow_hit`. Identity rotation: drawn in the hero's facing (APPROXIMATED). Ready.

---

## Effects in this scope

| effect | where it is loaded | parts | ready? |
|---|---|---|---|
| ladyLuck_ring | :21585 | EffectControl, AudioSource, Image / Ring emitters, legacy + EmitterControl | ready |
| fortune | CharacterControl.cs:36239 (not in the inventory) | EmblemEmitter | ready |
| doubleDown_ring | :24711 | Image / Ring emitters | ready |
| doubleDown2_hit | :25405 | Animation, SkinnedMeshRenderer, emitters, legacy + EmitterControl | ready |
| powerShuffle_ring | :22424 | Image / Line emitters | ready |
| lifeGamble_ring, skillGamble_ring | :22967, :23499 | Image / Line / Ring emitters (followState) | ready |
| lifeGamble_heal, skillGamble_heal, evenOdds_hit | :9169, :9262, :9351 | emitters, legacy | ready |
| grandCasinoArcade_ring1 / _ring2 | :28645, :28406 | Ring emitters, legacy | ready |
| grandCasinoArcade | :27826 | Animation, SkinnedMeshRenderer, **Cat_grandCasinoArcade**, legacy | **needs the part** (+ layout) |
| grandCasinoArcade_hit1 / 2 / 3 / 7 | :9669-9784 | EmblemEmitter, rings, legacy | ready |
| doom (Bat) | CharacterControl.cs:40491 | Image emitters | ready; **needs the cross-folder lookup** |
| forwardLunge_dust | prefab field :15857 (not in the inventory) | Line emitters | ready |
| nAttack_dust | :30480, :30732 | ImageEmitter | ready |
| nAttack_hit | :8266 | ImageEmitters | ready |
| deltaStrike_ring | :37105 | Emblem / Line / Ring emitters (followState) | ready |
| deltaStrike_cat | :37305 | StaticMesh, AlphaTimer, RingEmitter (205) | ready |
| deltaStrike | :37470 | Animation, SkinnedMeshRenderer, **UVScroll**, TrailEmitter, StaticMesh, ShatterMesh, AlphaTimer, RingEmitter (205) | **needs UVScroll** (+ layout) |
| finishingBlow_ring1 / _ring2 / _hit | :38445, :39223, :38739 | Image / Line / Ring emitters | ready |

Not cued (the passives / Even Odds pick the others): fateDraw_ring, doubleDown1_hit, lifeGamble_hit, skillGamble_hit,
all ready. Never spawned by the code: grandCasinoArcade_hit0. Forward Lunge's forwardLunge_hit / backStab_hit (out of
reach).

Voices (all in BB's rip, `cat/voices`): ladyLuck1-2, doubleDown1-2, powerShuffle1-2, lifeGamble1-2, skillGamble1-2,
grandCasinoArcade1-2, forwardLunge1-2, backflip1-2 (`backFlip1-2.wav`), heartRipper1-2, deltaStrike1-2,
finisingBlow1-2. Sounds the code plays (`"sound"`): grandCasino2, backflip (`backFlip.wav`), nAttack_hit. Every other
sound comes with its effect (AudioSource): fateDraw, doubleDown2, powerShuffle, gamble_ring / _heal / _success, evenOdds,
grandCasino1, grandCasino_hit1 / _hit7, doom_cast (bat), deltaStrike, aura1, finishingBlow, finishingBlow_hit.
Name collisions: `doubleDown1 / 2` are voices and sounds (the cue kind picks the folder; voices saved as `v_`);
`deltaStrike`, `backflip`, `forwardLunge` are clips and sounds / effects.

---

## Parts (for the parts stage)

1. **Cat_grandCasinoArcade** (wardrobe/fxparts/cat.js; on node 1 `grandCasinoArcade`, after its Animation and
   SkinnedMeshRenderer). `wardrobe_fx.py` LAYOUTS: `"Cat_grandCasinoArcade": [("mRenderer", "r")]` (8 bytes, proven).
   - The script (Cat_grandCasinoArcade.cs): Awake takes `mRenderer.materials[1]` (GrandCasinoArcade2) and `[2]`
     (GrandCasinoArcade3) (:38, :50); Update sets `_TintColor` = (0.5, 0.5, 0.5, a) with a = 0.15 sin(4 Time.time) on
     the first and (0.5, 0.5, 0.5, 0.15 - a) on the second (:94-115): the lights blink against each other at 4 rad/s
     (the first's alpha is negative half the time: drawn as 0). Time.time is the game clock (the page clock will do).
     Both materials are additive (`probe_mats.txt`); set the tint the way fxMaterial maps `_TintColor`. One machine at
     a time, so a shared material is fine; a clone per spawn is safer (bat.js does that for the guardian).
   - The coroutine's animation calls, from the cue option `anims` (fx.at.anims: `[[seconds after the spawn, clip]]`):
     at each time, `node.userData.fxAnim.play(clip)` (mesh.js Animation's play; the clip's own wrap, Once). The values
     (`[1.3, "fire"] ... [12.1, "fire"], [14.5, "destroy"]`) are the coroutine's 1.7 / 4.4 / 7.1 / 9.8 / 12.5 and 14.9 s
     less the 0.4 s spawn (:28554, :28531). (An alternative is a cue kind that plays a clip on a live effect from the
     grandCasinoArcade2 / 3 steps; the part keeps it in one file.)
2. **UVScroll** (fxparts/cat.js or a shared file: Delta Strike's triangle; other classes may carry it). LAYOUTS:
   `"UVScroll": [("scroll_x", "f"), ("scroll_y", "f")]` (8 bytes, proven). Each frame: the node's renderer's first
   material `_MainTex` offset = (Repeat(t x scroll_x, 100), Repeat(t x scroll_y, 100)) with t the game clock (UVScroll.cs:44-45);
   the texture needs RepeatWrapping (mesh.js's texture() sets it). The deltaStrike_tri's values are (1, 1). The clock is
   global, so all instances scroll alike (a shared material is the game's look too).
3. **doom for the Cat** (`wardrobe_fx.py` only): `EXTRA_FOLDERS["cat"] = ["gameassets/characters/heroes/bat/effects"]`
   or `ALIASES["cat"] = {"doom": "gameassets/characters/heroes/bat/effects/doom"}` (`cat --probe doom` is a KeyError
   today; `bat --probe doom` reads). Its sound doom_cast is found by rip_wav's rip-wide search.
4. **SEQ** (index.html, the editor's): Read this first 2.

---

## Passives, ranks, random picks

- Lady Luck #412 (Fate Draw: ring + voices), Roll the Dice #432 (Double Down: doubleDown2_hit, 2 m), Even Odds #422
  (Life / Skill Gamble: evenOdds_hit, the loss skipped; Power Shuffle sLv + 1: numbers), Backstab #413 (Forward Lunge:
  backStab_hit, out of reach), Finishing Blow #423 (Backflip's lock level: numbers). Open Wound, Power numbers: numbers.
- Random: every voice pair `a|b` (`Random.Range(0, 2) == 0`); Double Down's 8 target picks (rolls `dd1-8`, 50 %); the
  gambles' roll `gamble` (50 %, LCK 1); GCA's five results (rolls `casino1-5` + the 50-name pick, LCK 255).
- No rank picks an effect here except GCA (spins = 2 sLv + 1) and Delta Strike (scale 1.5 and the cat spots at sLv 2).

## TTO and others

The TTO client (TTO1102 pseudo/Cat.c) loads the same effects, voices and sounds in these fifteen coroutines (strings per
function: RPC_fateDraw :7324-7891 ... RPC_finishingBlow2 :8333-9218), the only change being Finishing Blow's voice
(`finisingBlow1 / 2`, :8376-8388). No TTO-only skill plays these clips (its five released moves have clips of their own),
so nothing here is TTO's.

## Possible Bible findings (to offer the user; not written there)

1. **Delta Strike does not teleport.** The reference says "The Cat teleports to a pre-computed landing position near the
   target (`KOIRnET4pM.position = mPos`, Cat.cs:37720)"; the owner calls `RPC_deltaStrike(this.KOIRnET4pM.position,
   vector2, 0, num2)` (:7078), so mPos is her own position: the triangle is cut from where she stands.
2. **Double Down can strike the Cat herself.** Its targets are on-screen characters from `FindAreaTarget(hero, 24, 10,
   130816)` (:25047-25106), which includes the caster (Damage.cs:963-1120); the reference says "enemies and allies".
   Whether the strike then hurts her (`hit()` on herself) is not traced.
3. **Finishing Blow's voice never plays on BB**: it loads `Voices/finishingBlow1 / 2` (:39288, :39319), the data has
   `finisingBlow1 / 2`; TTO loads the right names (pseudo/Cat.c:8376-8388).
4. **Lady Luck also changes Fate Draw's voices** (ladyLuck1 / ladyLuck2, :21640-21681), not only the ring.
5. **Casino Doom shows no number**: `RPC_grandCasinoArcade_hit(0)` draws nothing (:9648-9800); the data's
   `grandcasinoarcade_hit0` effect and `grandCasino_hit0` sound are unused.

## Open questions (each with my recommended answer)

1. **Heart Ripper's stabs: at the hero or at the 10 m point?** The game puts the Cat at the knocked-out target, so the
   spark is on her own spot 1 m up. Recommended: at the hero (`{"y": 1}`), as written: the target comes to the standing
   hero (as Finishing Blow's hits, which the game spawns at the Cat). Alternative: `{"d": 10.1, "y": 1}` (the target
   rule), the spark 10 m from the stabbing Cat.
2. **Double Down: half the strikes on the Cat?** Recommended: yes, as the game does with one target (rolls `dd1-8`).
   Alternative: all eight at the 10 m target (drop the `!dd` cues and the p / roll of the others).
3. **Grand Casino Arcade's luck.** Recommended: the 255 cap (777 on 53 % of spins, Doom 2 %), the only setting where every
   outcome shows; written that way. Alternatives: even odds over 111 / 222 / 333 / 777 (no Doom); LCK 1 (every spin
   Doom: the Bat's doom on the Cat and no number, five times).
4. **Life / Skill Gamble's loss with Even Odds.** Recommended: Even Odds catches every loss (the wardrobe keeps no 90 s
   timer; passives on), as written. Alternative: alternate per play, or 1 in 3 losses shows lifeGamble_hit /
   skillGamble_hit.
5. **The gambles' 50 %** (lckAdjust(50) at LCK 1, the Wolf's Double Art convention) while GCA uses LCK 255: recommended
   keep both (the proc rule for the gambles; GCA's LCK 1 shows nothing). For one LCK everywhere, the gambles at 255 are
   78 % (`p: 0.78`).
6. **The three SEQ fixes** (Read this first 2). Recommended: yes.
7. **Grand Casino Arcade turns the Cat to the camera, Backflip turns her away from the target.** Recommended: no turn in
   the wardrobe (the clips play in her own facing, as every in-place skill).
8. **Finishing Blow's voice**: recommended TTO's `finisingBlow1|finisingBlow2` (Sheep decision 10), as written; BB
   itself is silent.
9. **Forward Lunge's dust** all at the standing hero (the game drops one per 0.1 s along a 6 m dash). Recommended: as
   written (no hero mover). Alternative: spread them behind her by the distance still to run (0.3 s: -2.4 m, 0.4 s: -1.5,
   0.5 s: -0.6, 0.6 s: +0.3 ...), which only looks right if the clip itself carries her forward.

## Paste-ready cues (wardrobe/fx_cues/cat.json)

Twelve entries: the two pools (`instantCast`: fateDraw, doubleDown; `gamble`: powerShuffle, lifeGamble, skillGamble)
and ten plain clip entries. They assume the SEQ fixes of Read this first 2 and the parts above (`anims` is read by
Cat_grandCasinoArcade). Checked as valid JSON (`cues.json`).

```json
{
  "instantCast": {
    "why": "instantCast is played by two Cat skills, Fate Draw (Cat.cs:21563) and Double Down (:24693), both instant and both in one build: each play shows one, even chance (the pool rule); no other BB or TTO coroutine plays it (TTO pseudo/Cat.c: only RPC_fateDraw and RPC_doubleDown name it)",
    "skills": {
      "fateDraw": {
        "why": "Cat.cs RPC_fateDraw (:21254-21917; rank 4, Lady Luck #412 on: the passives rule): at 0 clip (cut, :21563); hasSkill(412) (:21575) picks ladyLuck_ring at the hero, hero rotation (createEffect :21585-21597; EffectControl life 1 + 1, followPosition, plays its own Sounds/fateDraw) and voice ladyLuck1 / ladyLuck2 (Random.Range(0, 2) :21640-21681, PlayOneShot :21853 / :21856) in place of fateDraw_ring + fateDraw1 / fateDraw2 (:21706-21863); Yield 0.4 (:21865): fortune on everyone of the Cat's layer within 15 m, the Cat included (FindAreaTarget :21414; fortune sLv + 1, chaAdjust(30) :21447-21453): the status puts the fortune emblem 2 m above each (Instantiate(fortune, position + 2 x up, identity), CharacterControl.cs:36235-36247; an EmblemEmitter alone, as the Wolf's valor_emblem): the hero's own; Yield 0.3 (:21849): standby 0.7 s (:21493)",
        "cues": [
          [0, "fx", "ladyLuck_ring"],
          [0, "voice", "ladyLuck1|ladyLuck2"],
          [0.4, "fx", "fortune", {"y": 2}]
        ]
      },
      "doubleDown": {
        "why": "Cat.cs RPC_doubleDown (:24447-24886; rank 2, Roll the Dice #432 on): at 0 clip (cut, :24693), doubleDown_ring at the hero (createEffect :24711-24723) and voice doubleDown1 / doubleDown2 (Random.Range(0, 2) :24766-24852); Yield 0.3 (:24846): doubleDown_fire (:24599); standby 0.4 s (Yield 0.1 :24843, :24623). doubleDown_fire (:24887-25205): sLv x 3 + 2 = 8 strikes (:25027), one every 0.4 s from 0.3 s (Yield :25155), each on a random on-screen character within 24 m in layer mask 130816 (FindAreaTarget :25047, isOnScreen :25075, Random.Range :25106), which scans the Enemy and Player tags (Damage.cs:963-1120): the Cat is a candidate too, so with one target each strike falls on the target (10 m) or on the Cat, even chance; RPC_doubleDown_hit at that one's feet (:25124): doubleDown2_hit (hasSkill(432) :25392-25415; else doubleDown1_hit :25441-25451), Instantiate(hitPos, identity: drawn in the hero's facing, APPROXIMATED; plays its own Sounds/doubleDown2); the damage 0.4 s later (:25358)",
        "cues": [
          [0, "fx", "doubleDown_ring"],
          [0, "voice", "doubleDown1|doubleDown2"],
          [0.3, "fx", "doubleDown2_hit", {"d": 10, "p": 0.5, "roll": "dd1"}],
          [0.3, "fx", "doubleDown2_hit", {"p": 0.5, "roll": "!dd1"}],
          [0.7, "fx", "doubleDown2_hit", {"d": 10, "p": 0.5, "roll": "dd2"}],
          [0.7, "fx", "doubleDown2_hit", {"p": 0.5, "roll": "!dd2"}],
          [1.1, "fx", "doubleDown2_hit", {"d": 10, "p": 0.5, "roll": "dd3"}],
          [1.1, "fx", "doubleDown2_hit", {"p": 0.5, "roll": "!dd3"}],
          [1.5, "fx", "doubleDown2_hit", {"d": 10, "p": 0.5, "roll": "dd4"}],
          [1.5, "fx", "doubleDown2_hit", {"p": 0.5, "roll": "!dd4"}],
          [1.9, "fx", "doubleDown2_hit", {"d": 10, "p": 0.5, "roll": "dd5"}],
          [1.9, "fx", "doubleDown2_hit", {"p": 0.5, "roll": "!dd5"}],
          [2.3, "fx", "doubleDown2_hit", {"d": 10, "p": 0.5, "roll": "dd6"}],
          [2.3, "fx", "doubleDown2_hit", {"p": 0.5, "roll": "!dd6"}],
          [2.7, "fx", "doubleDown2_hit", {"d": 10, "p": 0.5, "roll": "dd7"}],
          [2.7, "fx", "doubleDown2_hit", {"p": 0.5, "roll": "!dd7"}],
          [3.1, "fx", "doubleDown2_hit", {"d": 10, "p": 0.5, "roll": "dd8"}],
          [3.1, "fx", "doubleDown2_hit", {"p": 0.5, "roll": "!dd8"}]
        ]
      }
    }
  },
  "gamble": {
    "why": "gamble is played by three Cat skills, Power Shuffle (Cat.cs:22403), Life Gamble (:22949) and Skill Gamble (:23481), all instant: each play shows one, even chance (the pool rule); no other BB or TTO coroutine plays it",
    "skills": {
      "powerShuffle": {
        "why": "Cat.cs RPC_powerShuffle (:21918-22624; rank 2; Even Odds #422's sLv + 1 :22087-22093 changes numbers only): at 0 clip (cut, :22403), removePowerStatus (:22415), powerShuffle_ring at the hero (createEffect :22424-22436; life 1, plays its own Sounds/powerShuffle) and voice powerShuffle1 / powerShuffle2 (Random.Range(0, 2) :22479-22520); Yield 0.4 (:22564): one stat up, another down (:22072-22306; the xUp / xDown statuses draw nothing, CharacterControl.cs:33176-33296); Yield 0.3 (:22576): standby 0.7 s (:22333)",
        "cues": [
          [0, "fx", "powerShuffle_ring"],
          [0, "voice", "powerShuffle1|powerShuffle2"]
        ]
      },
      "lifeGamble": {
        "why": "Cat.cs RPC_lifeGamble (:22625-23146; Even Odds #422 on): at 0 clip (cut, :22949), lifeGamble_ring at the hero (createEffect :22967-22979; followState: cut at standby 0.7 s; plays its own Sounds/gamble_ring) and voice lifeGamble1 / lifeGamble2 (Random.Range(0, 2) :23022-23063); Yield 0.4 (:23111): the roll lckAdjust(50) > Random.Range(0, 100) (:22768; 50 % at LCK 1, as the Wolf's Double Art 24 %): won: RPC_lifeGamble_heal (:22779) = lifeGamble_heal at the hero (:9156-9180; plays Sounds/gamble_heal); lost: Even Odds takes the loss (hasSkill(422) :22801 with its 90 s timer free :22807; the wardrobe keeps no timers): RPC_evenOdds (:22813) = evenOdds_hit at the hero (:9335-9360; plays Sounds/evenOdds), no lifeGamble_hit (:22834-22839 skipped, :22829); Yield 0.3 (:23100): standby 0.7 s (:22879)",
        "cues": [
          [0, "fx", "lifeGamble_ring", {"cut": 0.7}],
          [0, "voice", "lifeGamble1|lifeGamble2"],
          [0.4, "fx", "lifeGamble_heal", {"p": 0.5, "roll": "gamble"}],
          [0.4, "fx", "evenOdds_hit", {"p": 0.5, "roll": "!gamble"}]
        ]
      },
      "skillGamble": {
        "why": "Cat.cs RPC_skillGamble (:23147-23681; Even Odds #422 on): at 0 clip (cut, :23481), skillGamble_ring at the hero (createEffect :23499-23511; followState: cut at standby 0.7 s; plays its own Sounds/gamble_ring) and voice skillGamble1 / skillGamble2 (Random.Range(0, 2) :23554-23595); Yield 0.4 (:23630): the roll Random.Range(0, 100) < lckAdjust(50) (:23290; 50 % at LCK 1): won: RPC_skillGamble_heal (:23306) = skillGamble_heal at the hero (:9249-9275; plays Sounds/gamble_success); lost: Even Odds (:23328-23340) = evenOdds_hit at the hero (RPC_evenOdds :9335-9360), no skillGamble_hit (:23361-23371 skipped); Yield 0.3 (:23636): standby 0.7 s (:23411)",
        "cues": [
          [0, "fx", "skillGamble_ring", {"cut": 0.7}],
          [0, "voice", "skillGamble1|skillGamble2"],
          [0.4, "fx", "skillGamble_heal", {"p": 0.5, "roll": "gamble"}],
          [0.4, "fx", "evenOdds_hit", {"p": 0.5, "roll": "!gamble"}]
        ]
      }
    }
  },
  "grandCasinoArcade1": {
    "why": "Cat.cs RPC_grandCasinoArcade (:27674-28900; rank 2): at 0 the Cat turns to face the camera (LookAt(mPos - flat(camera forward)) :28618), clip (cut, :28621), noDamage / noForce 17 s (:28633-28636, draw nothing), grandCasinoArcade_ring1 at the hero, hero rotation (Instantiate :28645-28657; life 3, plays its own Sounds/grandCasino1) and voice grandCasinoArcade1 / grandCasinoArcade2 (Random.Range(0, 2) :28700-28777); Yield 0.4 (:28796): the machine grandCasinoArcade at the hero (createEffect :27826-27838; life 16 + 1, followState; its Animation plays create, Cat_grandCasinoArcade blinks its lights); its child grandCasinoArcade (Find :27858) plays fire at each spin, 1.7 / 4.4 / 7.1 / 9.8 / 12.5 s (:28554), and destroy at 14.9 s (:28531): anims = those times after the spawn (part Cat_grandCasinoArcade); no cut: standby is at 15.9 s, in grandCasinoArcade3's step, and destroy has sunk the machine by then (its root to -5); left out: the camera zoom, shake and blur (:27887-27919)",
    "cues": [
      [0, "fx", "grandCasinoArcade_ring1"],
      [0, "voice", "grandCasinoArcade1|grandCasinoArcade2"],
      [0.4, "fx", "grandCasinoArcade", {"anims": [[1.3, "fire"], [4.0, "fire"], [6.7, "fire"], [9.4, "fire"], [12.1, "fire"], [14.5, "destroy"]]}]
    ]
  },
  "grandCasinoArcade2": {
    "why": "Cat.cs RPC_grandCasinoArcade from 1.7 s (Yield 1.3 :28782; clip looped :27946-27951; times from this step's start, the sequence's grandCasinoArcade2*@13.2): sLv x 2 + 1 = 5 spins (:28507), each Sounds/grandCasino2 at volume 2 (PlayOneShot(clip, 2) :28566-28578), Yield 2 (:28784) to its result, then 0.7 s (:28780; 0.4 after the last, :28809): spins at 0 / 2.7 / 5.4 / 8.1 / 10.8, results at 2.0 / 4.7 / 7.4 / 10.1 / 12.8. A result: Random.Range(0, clamp(LCK, 0, 255)) (:27993), at the 255 cap: < 5 Casino Doom (5 / 255: doom on the Cat's layer within 24 m, the Cat included, :27998-28048; the doom status draws the Bat's doom at the collider centre, about 0.6 m up, identity, CharacterControl.cs:40487-40504; RPC_grandCasinoArcade_hit(0) draws nothing, :9648-9800), < 50 hit1 (45), < 90 hit2 (40), < 120 hit3 (30), else hit7 (135): grandCasinoArcade_hit<n> at the hero + 4.5 m up, hero rotation (:9669-9794; each plays its own grandCasino_hit1 / _hit7); the 50 names = 9 : 8 : 6 : 27; left out: the damage and the camera blur (:28283-28295)",
    "cues": [
      [0.0, "sound", "grandCasino2", {"vol": 2}],
      [2.0, "fx", "doom", {"y": 0.6, "p": 0.0196, "roll": "casino1"}],
      [2.0, "fx", "grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7", {"y": 4.5, "p": 0.0196, "roll": "!casino1"}],
      [2.7, "sound", "grandCasino2", {"vol": 2}],
      [4.7, "fx", "doom", {"y": 0.6, "p": 0.0196, "roll": "casino2"}],
      [4.7, "fx", "grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7", {"y": 4.5, "p": 0.0196, "roll": "!casino2"}],
      [5.4, "sound", "grandCasino2", {"vol": 2}],
      [7.4, "fx", "doom", {"y": 0.6, "p": 0.0196, "roll": "casino3"}],
      [7.4, "fx", "grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7", {"y": 4.5, "p": 0.0196, "roll": "!casino3"}],
      [8.1, "sound", "grandCasino2", {"vol": 2}],
      [10.1, "fx", "doom", {"y": 0.6, "p": 0.0196, "roll": "casino4"}],
      [10.1, "fx", "grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7", {"y": 4.5, "p": 0.0196, "roll": "!casino4"}],
      [10.8, "sound", "grandCasino2", {"vol": 2}],
      [12.8, "fx", "doom", {"y": 0.6, "p": 0.0196, "roll": "casino5"}],
      [12.8, "fx", "grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit1|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit2|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit3|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7|grandCasinoArcade_hit7", {"y": 4.5, "p": 0.0196, "roll": "!casino5"}]
    ]
  },
  "grandCasinoArcade3": {
    "why": "Cat.cs RPC_grandCasinoArcade from 14.9 s (the sixth IL_9BB, i = 5 :28507): clip grandCasinoArcade3 (cut, :28513), the machine's destroy (:28531; its anims); Yield 0.3 (:28786): grandCasinoArcade_ring2 at the hero, hero rotation (Instantiate :28406-28418; life 3, plays its own Sounds/grandCasino1); Yield 0.7 (:28793): standby at 1.0 s (:28454); left out: the camera shake and zoom back (:28369-28392)",
    "cues": [
      [0.3, "fx", "grandCasinoArcade_ring2"]
    ]
  },
  "forwardLunge": {
    "why": "Cat.cs RPC_forwardLunge (:29924-31010; rank 2): at 0 clip (cut, :30796) and voice forwardLunge1 / forwardLunge2 (Random.Range(0, 2) :30837-30924); Yield 0.3 (:30941): the dash (moveSpeed 9 :30071), i = 0 to 3 every 0.1 s (Yield :30930, i++ :30132): forwardLunge_dust at the hero (the prefab field forwardLunge_dust, Cat.cs:15857 = Resources cat/effects/forwardLunge_dust; Instantiate :30721) and nAttack_dust 0.2 m left (i even) or right (i odd) (isOdd :30744, TransformDirection(+-0.2, 0, 0) :30750 / :30759); i = 4 at 0.7 s: moveSpeed 12 (:30260), nAttack_dust at the hero (:30480-30492); Yield 0.1 (:30915): moveSpeed 6 (:30158); Yield 0.2 (:30935): standby 1.0 s (:30184). The hero stays in place (the Feral Assault / Blink convention). Left out: the hits (FindRecTarget 3 / 4 m ahead :30518, :30271: the 10 m target is out of reach) and forwardLunge_hit / backStab_hit at it",
    "cues": [
      [0, "voice", "forwardLunge1|forwardLunge2"],
      [0.3, "fx", "forwardLunge_dust"],
      [0.3, "fx", "nAttack_dust", {"x": -0.2}],
      [0.4, "fx", "forwardLunge_dust"],
      [0.4, "fx", "nAttack_dust", {"x": 0.2}],
      [0.5, "fx", "forwardLunge_dust"],
      [0.5, "fx", "nAttack_dust", {"x": -0.2}],
      [0.6, "fx", "forwardLunge_dust"],
      [0.6, "fx", "nAttack_dust", {"x": 0.2}],
      [0.7, "fx", "nAttack_dust"]
    ]
  },
  "backflip": {
    "why": "Cat.cs RPC_backflip (:32024-32651; rank 2): at 0 the Cat turns her back to the target (LookAt(mPos - flat(tDir)) :32417), clip (cut, :32420), Sounds/backflip (owner only, :32435-32459; the rip's sounds/backFlip.wav) and voice backflip1 / backflip2 (Random.Range(0, 2) :32503-32592; the rip's backFlip1 / 2); moveSpeed 4 at 0.15 s, 6 + 4 x 2 = 14 at 0.4 s, 0 at 0.8 s (:32171, :32198, :32329; the hero stays in place), standby 0.9 s (:32350). No effect prefab",
    "cues": [
      [0, "sound", "backflip"],
      [0, "voice", "backflip1|backflip2"]
    ]
  },
  "heartRipper1": {
    "why": "Cat.cs RPC_heartRipper1 (:32652-33168; rank 2, on a knocked-out target :7359): at 0 clip (cut, :32995) and voice heartRipper1 / heartRipper2 (Random.Range(0, 2) :33036-33128); Yield 0.2 (:33126): moveSpeed 5 (:32809); Yield 0.2 (:33124): at 0.4 s the Cat is put at the target (target - forward x its extents.x, :32868-32873) and RPC_heartRipper2 starts (:32891): the sequence's heartRipper2 at 0.4 s (heartRipper1@0.4). No effect prefab",
    "cues": [
      [0, "voice", "heartRipper1|heartRipper2"]
    ]
  },
  "heartRipper2": {
    "why": "Cat.cs RPC_heartRipper2 (:33169-33799), the Cat at the target (the wardrobe hero stays put: the target comes to her): at 0 clip (cut, :33675), moveSpeed 2 (:33684); Yield 0.2 (:33733): stop (:33327) and the stab: enemies within 1 m (FindAreaTarget :33355), RPC_nAttack_hit at ClosestPointOnBounds(Cat + 1 up) (:33384-33394); she is 0.1 m past the target's centre, inside its 0.3 m box, so the point is her own, 1 m up: nAttack_hit there, hero rotation (:8253-8280) and Sounds/nAttack_hit (:8307); Yield 0.4 (:33737): at 0.6 s the second stab (:33467-33506) as she springs back (moveSpeed -8 :33454); Yield 0.2 (:33739): stop (:33566); Yield 0.2 (:33731): standby 1.0 s (:33608)",
    "cues": [
      [0.2, "fx", "nAttack_hit", {"y": 1}],
      [0.2, "sound", "nAttack_hit"],
      [0.6, "fx", "nAttack_hit", {"y": 1}],
      [0.6, "sound", "nAttack_hit"]
    ]
  },
  "deltaStrike": {
    "why": "Cat.cs RPC_deltaStrike (:36952-38094; rank 2): the Cat stays where she is (mPos = her own position, the dispatcher :7078; :37720): at 0 clip (cut, :37730), noForce 3 s (:37750) and voice deltaStrike1 / deltaStrike2 (Random.Range(0, 2) :37803-37996); Yield 0.3 (:37963): deltaStrike_ring at the hero (createEffect :37105-37117; life 3 + 2, followState: cut at standby 3.0 s; plays its own Sounds/deltaStrike); Yield 0.5 + 0.5 (:37969, :37954): at 1.3 s deltaStrike_cat twice at (+-4.5, 0, 8) on the ground, each facing away from (0, 0, 4.5): yaw +-52.1 (cPos = mPos + TransformDirection(+-(1.5 sLv + 1.5), 0, 2 sLv + 4), raycast down :37322-37371); Yield 0.2 (:37986): at 1.5 s deltaStrike 0.5 m ahead, hero rotation, scale 1.5 at rank 2 (:37470-37495; needs UVScroll); then six ticks 0.1 s apart from 2.1 s and the finisher at 2.9 s (:37872-37927, :37574-37603: damage only); standby 3.0 s (Yield 0.1 :37992, :37648); left out: the lock status (draws nothing), the camera colour ramp and blur (:37766, :37627)",
    "cues": [
      [0, "voice", "deltaStrike1|deltaStrike2"],
      [0.3, "fx", "deltaStrike_ring", {"cut": 3.0}],
      [1.3, "fx", "deltaStrike_cat", {"x": 4.5, "d": 8, "rot": [0, 52.1, 0]}],
      [1.3, "fx", "deltaStrike_cat", {"x": -4.5, "d": 8, "rot": [0, -52.1, 0]}],
      [1.5, "fx", "deltaStrike", {"d": 0.5, "scale": 1.5}]
    ]
  },
  "finishingBlow1": {
    "why": "Cat.cs RPC_finishingBlow1 (:38095-38530; Finishing Blow #423, on a knocked-out target :6448-6495): at 0 clip (cut, :38427) and finishingBlow_ring1 at the hero, hero rotation (Instantiate :38445-38455; life 1, plays its own aura1); Yield 0.2 (:38494): moveSpeed 5 (:38241); Yield 0.2 (:38485): at 0.4 s the Cat is put at the target (:38300-38305) and RPC_finishingBlow2 starts (:38323): the sequence's finishingBlow2 at 0.4 s (finishingBlow1@0.4). No voice here",
    "cues": [
      [0, "fx", "finishingBlow_ring1"]
    ]
  },
  "finishingBlow2": {
    "why": "Cat.cs RPC_finishingBlow2 (:38531-39461): at 0 clip (cut, :39177), finishingBlow_ring2 at the hero (createEffect :39223-39235; life 3 + 1, plays its own Sounds/finishingBlow) and the voice: BB loads Voices/finishingBlow1 / finishingBlow2 (:39278-39319), which BB's data lacks (it has voices/finisingBlow1 / 2), so BB is silent; TTO's fix (TTO1102 pseudo/Cat.c:8376-8388 loads finisingBlow1 / 2) is taken, as the Sheep's decision 10; Yield 0.3 (:39388): the first blow, finishingBlow_hit at the Cat herself, identity (drawn in the hero's facing, APPROXIMATED; Instantiate(position, identity) :38739-38751, hit or not; plays its own Sounds/finishingBlow_hit), again at 0.6 s (Yield 0.3 :39381, :38851) and 1.1 s (Yield 0.5 :39354, :38958); Yield 0.3 (:39373): at 1.4 s the spring back (moveSpeed -8 :38995; the last hit, 199, draws nothing); stop 1.6 s (:39068), standby 1.8 s (:39110)",
    "cues": [
      [0, "fx", "finishingBlow_ring2"],
      [0, "voice", "finisingBlow1|finisingBlow2"],
      [0.3, "fx", "finishingBlow_hit"],
      [0.6, "fx", "finishingBlow_hit"],
      [1.1, "fx", "finishingBlow_hit"]
    ]
  }
}
```

## Verification

Checker `verify_a`, 2026-11-13 (home PC), read only. Re-traced with `clip_flow.js` every coroutine here (RPC_fateDraw,
RPC_doubleDown, doubleDown_fire, RPC_doubleDown_hit, RPC_powerShuffle, RPC_lifeGamble, RPC_skillGamble,
RPC_grandCasinoArcade, RPC_forwardLunge, RPC_backflip, RPC_heartRipper1 / 2, RPC_deltaStrike, RPC_finishingBlow1 / 2) and
the helpers they call (RPC_nAttack_hit :8253-8325, RPC_lifeGamble_heal / RPC_skillGamble_heal / RPC_evenOdds :9160-9362,
RPC_grandCasinoArcade_hit :9648-9800, Delta Strike's caller :7078, Damage.FindAreaTarget, CharacterControl's fortune
:36235-36247 and doom :40487-40504 looks, lckAdjust :20658-20670), the opaque predicates on the spawn / voice / wait paths
worked by hand, and a fresh read-only probe of every effect (`checks/fx_cat_research/verify_a/probe.json`; the machine and
the triangle still fail on their missing layouts, as reported). Checked: every time, wait, position, offset, rotation,
random pick, roll, rank, passive and buildability claim, the clip lengths (`data/cat/clips.json`: grandCasinoArcade1 1.7 s
= its switch time, heartRipper1 / finishingBlow1 0.5 s, the looped grandCasinoArcade2 2.7 s = one spin), the
rip's files (`finisingBlow1 / 2`, `backFlip*`, `grandCasino_hit1` / `_hit7` only), the TTO lines (pseudo/Cat.c:6582, :7370,
:13548, :21531, :23544, :8376-8388) and the paste-ready block (valid JSON; the GCA pick is exactly 9 : 8 : 6 : 27 names).
All of it holds: no time, name, position, pick, rank or buildability claim is wrong.

Confirmed in particular: GCA's spins at 1.7 + 2.7 i, results 2.0 s later, `i >= sLv x 2` choosing the 0.4 s last wait
(:28303, :28780, :28809), `i++` (:28596), grandCasinoArcade3 at i = 5 (:28507-28531), ring2 at 15.2, standby 15.9; the
result bands < 5 / 50 / 90 / 120 of `Random.Range(0, clamp(LCK, 0, 255))` (:27993-28181) and the hit numbers at hero + 4.5
up, hero rotation, level 0 drawing nothing; Double Down's eight strikes at 0.3 + 0.4 k (`i >= sLv x 3 + 2` :25027, wait
:25155), mask 130816 over the Enemy and Player tags with no caster exclusion (Damage.cs:963-1120); lckAdjust(50) = 50 at LCK
1 (78 at 255); Even Odds skipping the loss (:22801-22839); the fortune emblem at + 2 up, identity (predicates 69098 - 438866
= -369768, 297678 - 269719 = 27959); Forward Lunge's dust sides (i even -0.2, odd +0.2, :30744-30759) and the i = 4 finisher
dust at the hero (:30480-30492); Heart Ripper's 0.3 m start short of the centre (:32868) and 0.4 m move (moveSpeed 2 x 0.2,
:33684), the spark at ClosestPointOnBounds(Cat + up) (:33384); Delta Strike's cats at (+-4.5, 0, 8), yaw +-atan2(4.5, 3.5)
= +-52.1 (:37322-37371), the triangle at + 0.5 forward with scale 1.5 only at sLv 2 (:37482-37495), no teleport (the
caller passes her own position, :7078); finishingBlow_hit outside the owner's hit block, so always (:38688-38751).

Corrections (no paste-ready block changes):

1. **Double Down's later strikes need the play-once tail** (Double Down, "The strikes go on after standby"). The tile's
   clip is 1.0 s; by default a skill plays once and its later cues run on in the idle stance (index.html:1339-1357), so all
   eight strikes show. With the skill tab's วนซ้ำ toggle on, the clip restarts at 1.0 s: the step's end fires only the cues
   before it (`fxDue(S.dur, false)` index.html:1384) and the restart's `fxStart` replaces `FX.cues` (:1374, :4630), so only
   the 0.3 and 0.7 s strikes ever show. A page-wide limit (any effect outliving its clip, as Wind Bound Domain's pulses), not
   a cue fault; noted for the editor, no change here.
2. **Casino Doom's look at y 0.6** is the standing target body's centre (Penguin decision 3), not a measured Cat
   CharacterController centre; it stands as an approximation (the doom effect is drawn at `collider.bounds.center`,
   CharacterController in the Cat prefab not probed).

Not changed (judgement calls already flagged as questions, both consistent with the precedents): Heart Ripper's stab spark
at the hero + 1 up (question 1; the Penguin's Blink / Parallel Shift put an effect "where she lands" at 0 m, the hero not
travelling), Double Down's coin flip between the target and the Cat (question 2), GCA at the LCK 255 cap (question 3).
