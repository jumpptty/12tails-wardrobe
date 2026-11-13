Summary: 8 clips, 18 coroutines (17 on the Monkey, plus the Phoenix's and Gadina's moves they start), 14 tiles, 10 cue keys (17 entries with the pool members, 50 cues).
- **Pools:**
  - `runicCast`: Runic Flame, Runic Sand.
  - `summonAttack`: Summon Attack, Sky Crimson, Planet Breaker, Instant Blaze, Earth Guard.
  - `summonRelease`: Unsummon, Summon Release, Summon Soul.
- **Sequences:**
  - New: Earth Form Attack (three stages on `summonAttack`) and Upheaval.
  - Fixed: Sentinel Guard's step times.
- **Summons:** every command tile needs a summon on stage, so the tile shows one standing 2 m ahead (Phoenix 4 or Gadina 4). Its commanded move is the skill's whole look, so it is cued: Sky Crimson, Instant Blaze, Planet Breaker, Earth Guard.
- **Parts:** Rotate (the runic rings), Monkey_lavu's upheaval circle, the Gadina Armor's clip timeline, and the summon part. The summon part needs new options: `hide`, `moves`, `turn`, `ring`.
- **One page change:** a per-step cue key. The Earth Form's three stages all play `summonAttack`.
- **BB bug with a TTO fix:** Runic Sand's voice. BB asks for `Voices/runicSand`, a file it doesn't have; TTO plays `Sounds/runicSand`.

---

# Monkey effects + sounds research: skill clips, second half (skills_b)

Researcher `skills_b`, 2026-11-13 (office PC). Research only (recipe steps 1-3); nothing built, no browser.

**Scope.** The clips runicCast, sentinalGuard0, sentinalGuard1, sentinalGuard2, summonAttack, summonDefense, summonRelease and upheaval. Also every coroutine that plays them (`pipeline/clip_calls.js`, `checks\fx_monkey_research\skills_b\clip_calls.txt`).

| clip | played by | length |
|---|---|---|
| runicCast | RPC_runicFlame, RPC_runicSand | 0.8 s |
| summonAttack | RPC_summonAttack, RPC_skyCrimson, RPC_planetBreaker, RPC_instantBlaze, RPC_earthGuard, RPC_gadinaArmor_nAttack1 / 2 / 3 | 0.8 s |
| summonDefense | RPC_summonDefense | 0.8 s |
| summonRelease | RPC_unsummon, RPC_summonRelease, RPC_summonSoul | 0.8 s |
| sentinalGuard1, sentinalGuard2, sentinalGuard0 | RPC_gadinaArmor_sentinalGuard, RPC_gadinaArmor_sentinalGuard0 | 0.5 / 2.0 (loop) / 0.5 s |
| upheaval | RPC_upheaval (+ RPC_upheaval0's root) | 0.8 s, played with Loop |

**Conventions.**
- Line numbers are `C:\Users\Jump\Desktop\12tails\DecompiledSource\Monkey.cs` unless another file is named. The home PC has the same files under `D:\12tails\`.
- "TTO1102:" means `DecompiledSource_TTO_2026-11-02\pseudo\Monkey.c`.
- Times are seconds from the start of the clip the entry is keyed by. Distance 0 = at the hero; d = metres ahead, x = right, y = up.
- Max rank, passives on: Phoenix 4, Gadina 4 (Titan Sword 3 and Aegis of Earth 3 give sword4 / shield4), Revised Skill #404, Revised Magic #414, Stone Sentinel #443, Lavu 2. Every command skill here has a single rank.
- The target is the standing 10 m target point: bounds centre 0.6 m up, radius 0.3 (Penguin decision 3, Bat decision 4).

**Read-only probes and scripts**, all in `C:\work\12tails-wardrobe\checks\fx_monkey_research\skills_b\` (git-ignored):
- `rd.py FILE FROM TO` prints a .cs range with the opaque predicates worked out. `if (F) { continue; }` pairs are dropped; true ones show as `if (T)` / `ALWAYS continue`.
  - Outputs: `summonAttack.txt`, `summonDefense.txt`, `unsummon.txt`, `summonRelease.txt`, `summonSoul.txt`, `runicSand.txt`, `upheaval.txt`, `upheaval0.txt`, `skyCrimson.txt`, `planetBreaker.txt`, `instantBlaze.txt`, `earthGuard.txt`, `ga1-3.txt` (the Earth Form attacks), `sentinalGuard.txt`, `sentinalGuard0.txt`, `ph_skyCrimson.txt`, `ph_instantBlaze.txt`, `ga_planetBreaker.txt`, `ga_earthGuard.txt`.
  - `RPC_*.flow.txt` is clip_flow.js output.
- `probe.json` + `probe_sum.txt` (`psum.py`): `wardrobe_fx.py monkey --probe` on 19 effects. probe.err is empty.
- `probe2.py` -> `probe2.json`: `effect()` with layouts added in memory only. Rotate (16 bytes) and Monkey_runicFlame / Monkey_runicSand (24 bytes) each decode exactly, and effect()'s self-check passes.
- `probe3.py` -> `probe3.json`: Phoenix4's `Phoenix` script (124 bytes) and Gadina4's `Gadina` script (180 bytes) decode exactly with their public fields in order (Phoenix.cs:2103-2154, Gadina.cs:2344-2422). Every field prefab is then walked through an in-memory FIELD_PREFABS.
- `probe4.py` -> `probe4.txt`: the summons' scripts and Animation clip names.
- `calc.py` -> `calc.txt`: Sky Crimson's ball, the Phoenix's fireball, Instant Blaze's run, the soul's height, Lavu's circle.
- `pool.json`. `pool.py` checks it: valid JSON, cue times in order, kinds, and option names against `wardrobe_fx_check.py` OPTS plus the new names. `fmt.py` turns it into `pool_block.json`, the block below (re-parsed: equal).

## Read this first

1. **Pools and tiles (14).**
   - `runicCast`: Runic Flame, Runic Sand.
   - `summonAttack`: Summon Attack #121, Sky Crimson #224, Planet Breaker #324, Instant Blaze #412, Earth Guard #413.
   - `summonRelease`: Unsummon #123, Summon Release #124, Summon Soul.
   - Single: Summon Defense #122.
   - Sequences:
     - **Earth Form Attack** (new): `summonAttack@0.9 summonAttack~@0.8 summonAttack~`.
     - **Upheaval** (new): `upheaval*@3.1 root~0.35@0.35`.
     - **Sentinel Guard** (times fixed): `sentinalGuard1@0.5 sentinalGuard2*@6.1 sentinalGuard0`.
   - Every pool member's key is its Bible skill id, so poolChains names the tile and finds its icon (`monkey_skyCrimson1` ... in the Bible's assets.js).
2. **Every command needs a summon.** The dispatcher refuses each command without one: Summon Attack :7550, Defense :7589, Unsummon :7621, Release :7653, Sky Crimson :7790, Planet Breaker :8120, Instant Blaze :8388, Earth Guard :8439, Summon Soul :8504.
   - So each tile shows the summon already standing, as Mole decision 37's Kaiser.
   - Where it stands: on the floor 2 m ahead, facing forward (getSpawnPos(hero + 2 forward) in phoenix_cast / gadina_cast; skills_a uses d 2 too).
   - The named commands play their summon's move: Phoenix 4 for Sky Crimson / Instant Blaze, Gadina 4 for Planet Breaker / Earth Guard.
   - The generic commands (Attack / Defense / Unsummon / Release / Soul) use **Phoenix 4** (question 1).
   - The cues use parts.md's interfaces: `clips` [[age, clip, fade, wrap]] (parts.md "Interfaces" 3), `attach` for Gadina's sword4 / shield4, and the `phoenix_*` / `gadina_*` FIELD_PREFABS names. New options for the summon part: `hide`, `moves`, `turn`, `ring` (false: no summon ring, it is already out).
3. **The summons' commanded moves are the skills' looks, so they are cued.** This differs from parts.md Q6, which recommends standing only. The two calls:
   - **The named skills are cued.** Without their moves, Sky Crimson, Planet Breaker, Instant Blaze and Earth Guard show nothing but a 0.8 s hand wave. The rule is "every missing part is built", so the four coroutines are cued from the game's code (times below).
   - **AI follow-ups are left out** (Mole decision 32's Barrel Bot call):
     - Summon Attack keeps only the Phoenix's first shot. The command puts the AI straight into its attack window (AI_setTimer(3)), so that shot is the command's own result. Later shots are left out.
     - Summon Defense keeps the turn and the cry; the walk back is left out.
     - Summon Release's later attack on the Monkey is left out (question 2).
4. **Runic Flame / Runic Sand draw no trail on the page.**
   - The segments drop only once the Monkey is 1.58 m from the last one (`sqrMagnitude >= 2.5`, :12413, :13679). The hero does not travel (Bison decision 17), so no segment drops.
   - Each tile shows the status ring on the Monkey at 0.3 s, cut at 10 s. The status lasts FloorToInt(0.2 SP) s: 20 s at SP 100.
   - **The rings need the `Rotate` part.** `runicFlame_ring/magicRune` has "no layout for Rotate (16 field bytes)".
   - Rotate's layout is `[("speed", "v3"), ("useWorldSpace", "b")]`, from Reborn's `Assembly-UnityScript-firstpass/Rotate.cs`; BB's firstpass is not decompiled. probe2 proved it byte-exact:
     - runicFlame_ring: (0, 0, 180) deg/s, self space;
     - runicSand_ring: (0, 0, 120) deg/s, self space.
   - parts.md part 3 has the same layout and part.
5. **Runic Sand's voice is a BB bug with a TTO fix.**
   - BB loads `Voices/runicSand` (:34307). The rip's monkey/voices has no such file, so BB logs "Cannot find runicSand voice" (:34322) and plays nothing.
   - TTO1102 `Monkey.<RPC_runicSand>d__219` loads `sounds/runicSand` in its place (pseudo/Monkey.c:16770-16830).
   - The cue is `[0, "sound", "runicSand"]` (Sheep decision 10). Runic Flame's voice exists in both games.
6. **Upheaval is Lavu's command while the attack button is held** (:10358-10406).
   - The Monkey loops the `upheaval` clip. Lavu circles him on a 6 m ring (Monkey_lavu.cs:580-686).
   - An `upheaval` wave spawns at the Monkey every 0.5 s from 2.0 s (:35147-35176, :35421).
   - It ends on the button's release, or at SP <= 1: then RPC_upheaval0 plays root with a 0.35 s fade (:35674).
   - Held for three waves (2.0 / 2.5 / 3.0 s), released at 3.1 s (question 3).
   - The tile needs Lavu present: `lavu` with parts.md's `"lavu": "upheaval"` and the release age.
7. **Earth Form's tiles need the Gadina Armor already worn.** Both Earth Form Attack and Sentinel Guard happen only in Earth Form.
   - The game parents `gadinaArmor` (a skinned shell with its own Animation) to the Monkey at the form's cast (:40719-40747).
   - Each move plays the armour's own clip: nAttack1-3, cAttack1 / cAttack2 / cAttack0.
   - Each tile spawns the armour at 0 with its `clips` timeline (parts.md part 8), cut at 10 s.
   - attacks_emotes.md item 11 hands both moves to this report.
8. **Earth Form Attack needs a per-step cue key** (the page change, question 5).
   - All three stages play `summonAttack`, each with its own voice, sound and ring.
   - fxStart looks a sequence's cues up by clip (`tab[ch.id + ":" + clip] ?? tab["@" + ch.name + ":" + clip] ?? tab[clip]`, index.html fxStart), so every stage would get stage 1's cues.
   - Proposed: try `"@<seq>:<clip>#<step>"` first (step = the step index from 0). The block uses `@EarthFormAttack:summonAttack#0`, `#1` and `#2`.
9. **The code's own voice picks** (not bugs; offered for the Bible):
   - Sentinel Guard and Earth Guard say summonDefense (:42959, :38104);
   - Summon Release says unsummon (:23871);
   - Instant Blaze has no voice.
   - TTO does the same: TTO1102 `<RPC_gadinaArmor_sentinalGuard>d__243`, `<RPC_earthGuard>d__232`, `<RPC_summonRelease>d__175`.
10. **TTO.**
    - The released TTO clips (buitenBastion, golemCall, jaAscension, solarCall, clap, wai) are not in this scope, and none of them plays these clips.
    - Rune Golem's cast reuses the *voice* `upheaval`, not the clip (TTO1102 `<RPC_runeGolem_cast>d__320` Row6Voice). That belongs to the TTO report.
    - Every BB coroutine here has a TTO twin with the same strings and waits:

      | coroutine | pseudo/Monkey.c line |
      |---|---|
      | runicFlame / runicSand | :16425 / :16770 |
      | summonAttack / summonDefense | :18705 / :19028 |
      | unsummon / summonRelease / summonSoul | :20866 / :19574 / :19829 |
      | skyCrimson / planetBreaker | :17115 / :15908 |
      | instantBlaze / earthGuard | :10047 / :3884 |
      | upheaval / upheaval0 | :21250 / :21122 |
      | gadinaArmor_nAttack1-3 | :6718 / :7348 / :7883 |
      | gadinaArmor_sentinalGuard / sentinalGuard0 | :8589 / :8417 |

    - BB is the authority for the cues. The one TTO fix used is Runic Sand's voice.

## Per clip

Format: the RPC (file:line), then the timeline. The `why` of each entry in the JSON carries every citation.

### runicCast (pool: Runic Flame, Runic Sand; clip 0.8 s)

| | 0 s | 0.3 s | standby |
|---|---|---|---|
| runicFlame (RPC_runicFlame :29301-29670) | runicCast, 0.1 s fade (:29583); voice runicFlame (:29619, :29664) | status runicFlame FloorToInt(0.2 SP) s (:29442) -> `runicFlame_ring` at the Monkey, identity, parented (CharacterControl.cs:37854-37879) | 0.6 (:29510) |
| runicSand (RPC_runicSand :33989-34360) | runicCast, 0.1 s fade (:34271); sound runicSand (TTO's fix, Read this first 5) | status runicSand -> `runicSand_ring` (CharacterControl.cs:38066-38091) | 0.6 (:34198) |

- Each status removes the other (:37851, :38063).
- The rings have no EffectControl. Each is destroyed with its status (CharacterControl.cs:17101-17115, :17184-17198): `kill: 10`.
- Each ring loops its own Sounds/runicFlame / runicSand and plays runicCast once (probe2).
- Left out: the camera's motion blur (:29489, :34177) and the trail (Read this first 4).
- Buildable: once Rotate is built (parts.md part 3).

### upheaval (Lavu's Upheaval; looped clip)

- At 0:
  - voice upheaval (:35358, :35370);
  - `upheaval_ring` at the Monkey, identity (:35389-35401). It has EffectControl 3 + 1 s and followState, so it is cut when his command changes at the release: `cut: 3.1`. Its own sound is lavu_flyby.
  - Lavu gets SendMessage("upheaval") (:35430).
- Lavu (Monkey_lavu.upheaval, Monkey_lavu.cs:600-686):
  - it Slerps over 3 s onto `summoner + rotateH(6 forward, 120 deg/s x t) + up sin(4t)` (:632-648);
  - then it rides the circle, one lap per 3 s, with Euler(-30 cos 4t, -(90 + 120 t), 0) (:657-662);
  - at the release it goes back to standby (:672): 8 m/s at 1 rad/s toward 4 m above the Monkey (:42-58).
- The waves: the first 2 s in (:35421), then every 0.5 s (:35147-35153). Each is `upheaval` Instantiated at the Monkey, identity (:35164-35176), with EffectControl 2 s and its own sound lavu_upheaval.
  - It costs 1 SP with Revised Skill (:35196).
  - RPC_AddDamage hits every enemy within 12 m (:35201-35240): the 10 m target takes it, with nothing drawn.
  - The camera shake (:35258) is left out.
  - Damage Cast's 2 m hits every 0.4 s (:35056-35133) miss the target.
- The release at 3.1 s: RPC_upheaval0, root with a 0.35 s fade (:35674), standby 0.35 s later (:35634).
- Buildable:
  - upheaval_ring and upheaval are ready (inventory).
  - lavu needs Monkey_lavu (parts.md part 2) with rotationControl (the Mole's).
  - lavu_flyby and lavu_upheaval live in the rip's `elementals/lavu/sounds/`, not monkey/sounds. rip_wav searches anywhere in the rip, so it finds them.

### summonAttack (pool: 5 members; clip 0.8 s)

Every member: the voice at 0, the order at 0.3 s (Yield 0.3), standby 0.6 s (Yield 0.3). The summon stands 2 m ahead with `ring: false`, `single: true`, `kill: 10`. The summon's times below are tile times (its routine starts at 0.3).

- **summonAttack** (RPC_summonAttack :21893-22432):
  - Voice summonAttack (:22366, :22415).
  - Phoenix.RPC_summonAttack (Phoenix.cs:1890-1926) sets 1200 hate and AI_setTimer(3), so its next frame is RPC_nAttack:
    - nAttack with a 0.3 s CrossFade and pheonix_cry at 0.3 (:2594, :2612);
    - the shot 0.5 s in, at 0.8 (:2354), from Phoenix + (0, 2.4, 1) (:2425) toward the target's centre (:2461): `{"d": 3, "y": 2.4, "rot": [14.42, 0, 0], "to": [0, 0.6, 10]}`;
    - Phoenix_fireBall flies at 30 m/s and meets the body at (0, 0.675, 9.709) at 1.03 s, where its part spawns `phoenix_fireBall_hit`;
    - root at 1.1.
- **skyCrimson** (RPC_skyCrimson :27138-27527; Phoenix.RPC_skyCrimson Phoenix.cs:3360-3994):
  - 0: voice skyCrimson.
  - 0.3: skyCrimson1 (0.2 fade), the cry, `phoenix_skyCrimson_dust` at the Phoenix.
  - 2.3: every renderer of the Phoenix off (:3507-3529), so `hide` [2.3, 5.3]. The colour ramp (:3572) is left out.
  - 3.3: one ball per enemy within 24 m (:3622), with the sound phoenix_skyCrimson (:3696).
    - fireDir = (target centre - Phoenix - 20 up).normalized; firePos = centre - 12 dir (:3645-3655).
    - So the ball starts at (0, 11.694, 5.425) with rot [67.59, 0, 0] and flies at 16 m/s.
    - It bursts only on layer 0, the floor (Phoenix_skyCrimson_fire.cs:143-179), so it passes through the target.
    - It lands at (0, 0, 10.247) at 4.09 s as `phoenix_skyCrimson_hit`, identity (Phoenix.cs:1856).
  - 5.3: skyCrimson2, the Phoenix shown again.
  - 5.8: dust again, and a 300 HP heal.
  - 6.3: root.
- **planetBreaker** (RPC_planetBreaker :31599-32020; Gadina.RPC_planetBreaker Gadina.cs:5403-5884):
  - 0: voice planetBreaker; `planetBreaker_ring` at the Monkey, identity (:31967-31977).
  - 0.3: planetBreak (CrossFade, 0.3 s), `gadina_planetBreaker1` at the Gadina, gadina_cry.
  - 1.1: `gadina_planetBreaker2` (AlphaTimer; its own sound gadina_planetBreaker).
  - Pulses at 1.4 / 1.7 / 2.0. The target 8 m from the Gadina sits in the 5-12 m ring, which takes a flat hit with no effect (:5675-5698); the inner ring's `nAttack_hit` (:5659) needs a target within 5 m.
  - 2.6: root.
- **instantBlaze** (RPC_instantBlaze :37266-37651; Phoenix.RPC_instantBlaze Phoenix.cs:2685-3288):
  - No voice.
  - 0.3: instantBlaze (0.2 fade), the cry.
  - 0.8: the dash at 12 m/s (:2826). `phoenix_instantBlaze_ring` rides the Phoenix (followPosition; spawned by the part).
  - Hit boxes at 1.0 / 1.2 / 1.4 / 1.6. They apply burn, with nothing drawn.
  - 1.6: 6 m/s.
  - 1.8: stop.
  - 1.9: root, 12.8 m ahead, through the target (calc.txt; `moves` [[0.8, 12], [1.6, 6], [1.8, 0]]).
  - The summon moves; the hero does not (Chameleon decision 30).
- **earthGuard** (RPC_earthGuard :37696-38160; Gadina.RPC_earthGuard Gadina.cs:5028-5370):
  - 0: voice summonDefense.
  - +1000 hate on the target (:37958).
  - 0.3: guard (CrossFade, 0.3 s), `gadina_earthGuard_ring` (EffectControl life 10, followState), gadina_cry.
  - Six heals 2 s apart from 0.8 s, with nothing drawn.
  - The Gadina stands by at 13.3, so it is cut at 10 s. The ring ends at 10.3 by its own life.

### Earth Form Attack (sequence on summonAttack: 0 / 0.9 / 1.7 s)

| stage | RPC | at its 0 | then | standby |
|---|---|---|---|---|
| 1 | RPC_gadinaArmor_nAttack1 :40994-41546 | summonAttack (0.2 fade :41360); voice summonAttack (:41408); sound nAttack1 (:41506); armour nAttack1 (:41444); `gAttack1_ring` (:41461-41473) | punches at 0.3 / 0.6 within 2 m (:41145, :41222) | 1.0 (:41304) |
| 2 | RPC_gadinaArmor_nAttack2 :41597-42089, waits to actionTime + 0.9 (:42088) | voice sAttack1 (:41739); sound nAttack2 (:41785); armour nAttack2 (:41836); `gAttack2_ring` (:41853-41865) | hits at 0.4 / 0.6 within 4 m (:41924) | 0.8 (:42012) |
| 3 | RPC_gadinaArmor_nAttack3 :42131-42596, waits to actionTime + 1.7 (:42595) | voice sAttack2 (:42273); sound nAttack2 (:42319); armour nAttack3 (:42370); `gAttack3_ring` (:42387-42399) | hit 3 m ahead, 3 m wide, at 0.4 (:42453); camera shake (left out) | 0.8 (:42535) |

- Each later stage is started inside the window before it (:9774-9796 at 0.3-0.8 s, :9817-9849). actionTime stays stage 1's: no stage sets it before its own standby (:42017, :42540).
- No hit reaches the 10 m target, so `gadinaArmor_hit` (:41184) is not cued (Bison decision 16).
- The armour: spawned at 0 with `clips` [[0, nAttack1], [0.9, nAttack2], [1.7, nAttack3], [2.5, root 0.2 Loop]]. The root comes from Update's CrossFade("root", 0.2) once he stands by (:567-587).
- Buildable: the gAttack rings and the armour are ready by the inventory. The armour's timeline is parts.md part 8.

### summonDefense (Summon Defense; clip 0.8 s)

- 0: voice summonDefense (:22883, :22936).
- 0.3: the order to Phoenix / Gadina / Ja (:22641-22736). The Phoenix, standing or running, LookAts the Monkey on the flat (Phoenix.cs:2000), so it turns 180 deg: `turn: 0.3`. It cries (:2009) and its AI goes to defense (:1993).
- Standby 0.6 (:22794).

### summonRelease (pool: Unsummon, Summon Release, Summon Soul; clip 0.8 s)

- **unsummon** (RPC_unsummon :22983-23545):
  - 0: voice unsummon.
  - 0.3: MP back (Phoenix4 35, :23202) and SendMessage("unsummon") (:23367).
  - Phoenix.unsummon (Phoenix.cs:5127-5308): ko (:5264), pheonix_unsummon (:5276), destroyed 1 s later (:5306): `end: 0.3`, the Bat guardian's option.
- **summonRelease** (RPC_summonRelease :23579-23920):
  - 0: voice unsummon (:23871).
  - 0.3: SendMessage("summonRelease") (:23735). Phoenix.summonRelease (Phoenix.cs:2028-2057) adds 1200 hate on the Monkey and sets layer 15; nothing changes on screen.
- **summonSoul** (RPC_summonSoul :23949-24632):
  - The target is a player (:8522): the Monkey himself (Sheep decision 1).
  - 0: voice summonSoul.
  - 0.4 (Yield 0.4 :24630):
    - `summonSoul_ring` at the Monkey, his rotation (:24150-24162);
    - phoenixSoul 4 for 240 s (:24234), which spawns `phoenixSoul` at mChar.bounds.center + 0.5 height up, identity (CharacterControl.cs:38149-38179). With the Monkey's controller (centre 0.7, height 1.3; rip Monkey.prefab:949-955) that is `y: 1.35`; its own sound is fireSoul.
  - Standby 0.6 (:24436).
  - The other souls are jaSoul / gadinaSoul / buitenSoul / gaosSoul (:24247-24407). All are ready by the probe; question 1 decides which one shows.

### Sentinel Guard (sequence: sentinalGuard1 0.5 s > sentinalGuard2 held > sentinalGuard0)

- Stone Sentinel's Earth Form charge needs >= 10 MP / SP (:10282-10340).
- **sentinalGuard1**, RPC_gadinaArmor_sentinalGuard (:42635-43069), at 0:
  - the clip with a 0.1 s fade (:42892);
  - the armour's cAttack1 (:42918);
  - voice summonDefense (:42959, :43054).
- **sentinalGuard2**, case 2 at 0.5 (:42751-42829):
  - the clip cut in, Loop (:42770);
  - the armour's cAttack2, Loop (:42786);
  - `sentinalGuard_ring` at the Monkey, his rotation (:42797-42815; life 99, followState, its own looping sound).
  - Then every 3 s: MP -8 with Revised Magic (:43012) and a 0.2 MHP heal (:43017; nothing drawn) at 0.5, 3.5 and 6.5 s.
- **The release** at 6.6 s: RPC_gadinaArmor_sentinalGuard0 (:43099-43299):
  - sentinalGuard0 cut in (:43270);
  - the armour's cAttack0 (:43279);
  - standby 0.3 s later (:43217).
- The ring's cut is 6.1, written in sentinalGuard2's own clock: the step's end (Chameleon decision 62).
- The armour's timeline sits on sentinalGuard1's cue: [[0, cAttack1], [0.5, cAttack2 Loop], [6.6, cAttack0], [6.9, root 0.2 Loop]].
- Buildable: sentinalGuard_ring is ready. The armour needs parts.md part 8.

## Effects at a glance

- **Ready (inventory / probe):**
  - on the Monkey: upheaval_ring, upheaval, planetBreaker_ring, summonSoul_ring, phoenixSoul, sentinalGuard_ring, gAttack1_ring, gAttack2_ring, gAttack3_ring;
  - the summons' field prefabs (probe3): phoenix_skyCrimson_dust, phoenix_skyCrimson_hit, phoenix_instantBlaze_ring, phoenix_fireBall_hit, gadina_earthGuard_ring, gadina_planetBreaker1, gadina_planetBreaker2 (AlphaTimer is built);
  - the other souls: jaSoul, gadinaSoul, buitenSoul, gaosSoul.
- **Need a part:**

  | effect | part |
  |---|---|
  | runicFlame_ring, runicSand_ring | Rotate (layout proved) |
  | lavu | Monkey_lavu's upheaval state (parts.md part 2) |
  | gadinaArmor | the clip timeline (parts.md part 8) |
  | Phoenix4, Gadina4 | the summon part (parts.md part 9), plus this report's `hide`, `moves`, `turn`, `ring` |
  | phoenix_fireBall | `Phoenix_fireBall` layout `[("mLv", "i")]` (Phoenix_fireBall.cs:382; 4 field bytes) and a 30 m/s mover that stops on `to` and spawns phoenix_fireBall_hit (parts.md part 1's shot mover) |
  | phoenix_skyCrimson_fire | ProjectileControl (life 2) + Phoenix_skyCrimson_fire (no fields) and a 16 m/s mover that bursts on the floor only, spawning phoenix_skyCrimson_hit at the contact, identity |

- **Not cued:**
  - runicFlame / runicSand segments: the hero stands (Read this first 4).
  - gadinaArmor_hit, the Planet Breaker inner ring's nAttack_hit, the Earth Form punches and Damage Cast's hits: out of reach.
  - Instant Blaze's burns, Earth Guard's / Sentinel Guard's / Sky Crimson's heals, the hate and MP returns: no effect.
  - The summons' later AI moves: question 2.
  - The camera's motion blur, colour ramp and shakes.

## Paste-ready cue entries for wardrobe/fx_cues/monkey.json

This is the block from `checks\fx_monkey_research\skills_b\pool_block.json`, checked by `pool.py`.

Option names beyond today's OPTS (`pipeline/wardrobe_fx_check.py:171-174`):
- from parts.md: `clips`, `attach`, `lavu`;
- from this report: `hide`, `moves`, `turn`, `ring`.

The `@EarthFormAttack:summonAttack#n` keys need the per-step lookup (Read this first 8); the check must also map them to the Earth Form Attack tile.

```json
{
"runicCast": {
  "why": "The runicCast clip: Runic Flame (RPC_runicFlame, PlayAnimation(\"runicCast\", 0.1) Monkey.cs:29583; dispatcher mnk_runicFlame1 :7986-8005) and Runic Sand (RPC_runicSand :34271; mnk_runicSand1 :8329-8348), one per play, even chance, picked anew on every play (one tile each, poolChains); each puts its status ring on the Monkey at 0.3 s and stands by at 0.6 s; the trail segments (runicFlame / runicSand) drop only while he moves (RunicFlame / RunicSand every 0.2 s, a segment once he is 1.58 m from the last, sqrMagnitude >= 2.5, :12384-12441, :13668-13707): the hero does not travel (plans/fx_bison/decisions.md 17), so none; the camera's motion blur (:29489, :34177) is left out",
  "skills": {
    "runicFlame": {
      "why": "Monkey.cs RPC_runicFlame (:29301-29670), rank 1: clip runicCast, 0.1 s fade (:29583), voice runicFlame (load :29619, PlayOneShot :29664) at 0; Yield 0.3 (:29658): RPC_AddStatus(\"runicFlame\", 1, FloorToInt(0.2 sp)) (:29442; SP then 0, :29463) -> CharacterControl's addStatus removes runicSand (:37851) and creates runicFlame_ring at the Monkey, Quaternion.identity, parented to him (:37854-37879); no EffectControl: it lives while the status does (destroyed at its end, CharacterControl.cs:17101-17115): FloorToInt(0.2 SP) s, 20 s at SP 100: cut at 10 s (kill 10, the 10 s rule); its magicRune spins by Rotate (0, 0, 180) deg/s, it loops its own Sounds/runicFlame and plays runicCast once (checks/fx_monkey_research/skills_b/probe2.json); Yield 0.3 (:29656): standby 0.6 s (:29510)",
      "cues": [
        [0, "voice", "runicFlame"],
        [0.3, "fx", "runicFlame_ring", {"kill": 10}]
      ]
    },
    "runicSand": {
      "why": "Monkey.cs RPC_runicSand (:33989-34360), rank 1: clip runicCast, 0.1 s fade (:34271); its voice: BB loads Voices/runicSand (:34307), which BB does not have (none in the rip's monkey/voices; Debug.LogError \"Cannot find runicSand voice\" :34322): silent in BB; TTO plays Sounds/runicSand in its place (TTO1102 Monkey.<RPC_runicSand>d__219, pseudo/Monkey.c:16770-16830): TTO's fix (plans/fx_sheep/decisions.md 10), a \"sound\" cue at 0 (PlayOneShot :34345); Yield 0.3 (:34352): RPC_AddStatus(\"runicSand\", 1, FloorToInt(0.2 sp)) (:34130; SP then 0 :34151) -> addStatus removes runicFlame (CharacterControl.cs:38063) and creates runicSand_ring at the Monkey, identity, parented to him (:38066-38091), destroyed with the status (:17184-17198): cut at 10 s (kill 10); magicRune spins by Rotate (0, 0, 120) deg/s, its own looping Sounds/runicSand and a one-shot runicCast (probe2.json); Yield 0.3 (:34350): standby 0.6 s (:34198)",
      "cues": [
        [0, "sound", "runicSand"],
        [0.3, "fx", "runicSand_ring", {"kill": 10}]
      ]
    }
  }
},
"upheaval": {
  "why": "Monkey.cs RPC_upheaval (:34904-35455), Lavu's Upheaval: the attack button held with Lavu summoned (dispatcher :10358-10406; released -> RPC_upheaval0 :10681-10698); clip upheaval, 0.2 s fade, wrapMode Loop (:35322-35325), voice upheaval (load :35358, PlayOneShot :35370) and upheaval_ring createEffect at the Monkey, identity (:35389-35401; EffectControl 3 + 1 s, followPosition + followState: cut when his command changes at the release; its own Sounds/lavu_flyby) at 0; Lavu SendMessage(\"upheaval\") (:35430): Monkey_lavu.upheaval (Monkey_lavu.cs:580-686) Slerps the snake over 3 s onto a 6 m circle round the Monkey, one lap per 3 s, bobbing Sin(4t) m (:632-662), back to standby (4 m above him, :48-58) when his command changes (:672); every FixedUpdate (Yield WaitForFixedUpdate :35452): the first wave 2 s in (mUpheavalTimer = now + 2 :35421), then every 0.5 s (:35147-35153): upheaval Instantiated at the Monkey, identity (:35164-35176; EffectControl 2 s, its own Sounds/lavu_upheaval), 1 SP each with Revised Skill #404 (passives on, :35196), RPC_AddDamage on every enemy within 12 m (:35201-35240: the 10 m target, no effect drawn), camera shake (:35258, left out); Damage Cast's 2 m hits every 0.4 s (:35056-35133) miss the 10 m target; it runs until the button is released (or SP <= 1, :35265-35286): three waves, 2.0 / 2.5 / 3.0 s, then the release at 3.1 s (the channel-until-release rule, SEQ comment: three hits), RPC_upheaval0: PlayAnimation(\"root\", 0.35) (:35674), standby 0.35 s later (:35634, Yield :35685); Lavu: the summon shown already in the air at its standby height (y 4), cut at 10 s (the summon rule, plans/fx_mole/decisions.md 32, 37)",
  "cues": [
    [0, "voice", "upheaval"],
    [0, "fx", "upheaval_ring", {"cut": 3.1}],
    [0, "fx", "lavu", {"y": 4, "kill": 10, "single": true, "lavu": "upheaval", "release": 3.1}],
    [2.0, "fx", "upheaval"],
    [2.5, "fx", "upheaval"],
    [3.0, "fx", "upheaval"]
  ]
},
"summonAttack": {
  "why": "The summonAttack clip: Summon Attack (RPC_summonAttack, PlayAnimation(\"summonAttack\", 0.2) Monkey.cs:22330), Sky Crimson (RPC_skyCrimson :27439), Planet Breaker (RPC_planetBreaker :31900), Instant Blaze (RPC_instantBlaze :37613), Earth Guard (RPC_earthGuard :38068) (pipeline/clip_calls.js), one per play, even chance, picked anew on every play (one tile each, poolChains); each command needs its summon (dispatcher :7546-7575, :7778-7796, :8108-8126, :8376-8421, :8427-8470): the summon stands already summoned on the floor 2 m ahead, facing forward (getSpawnPos(hero + 2 forward), phoenix_cast / gadina_cast), Phoenix 4 or Gadina 4 (max rank), cut at 10 s (plans/fx_mole/decisions.md 32, 37); every one: voice (or none) at 0, the order to the summon at 0.3 s (Yield 0.3), standby 0.6 s (Yield 0.3); the Earth Form's three normal attacks play this clip too: their own sequence, Earth Form Attack (\"@EarthFormAttack:summonAttack#<step>\")",
  "skills": {
    "summonAttack": {
      "why": "Monkey.cs RPC_summonAttack (:21893-22432), Summon Attack (#121): target locked (:7556; the 10 m target), clip, 0.2 s fade (:22330), voice summonAttack (load :22366, PlayOneShot :22415) at 0; Yield 0.3 (:22417): Phoenix.RPC_summonAttack (:22087): hate list cleared, 1200 hate on the target, AI_setTimer(3) (Phoenix.cs:1890-1926): straight into the attack window, no select or idle (12t_reference/monkey-skill-reference.md 4.5): RPC_nAttack at once: CrossFade(\"nAttack\") (:2594) and pheonix_cry (:2612), the fireball 0.5 s in (actionTime + 0.5 :2354) from the Phoenix + (0, 2.4, 1) (Phoenix4 :2425) toward the target's bounds centre (:2461; 10 m ahead 0.6 m up: rot [14.42, 0, 0], calc.txt), RPC_fireball_fire (:2475), standby 0.3 s later (:2634): the shot at 0.8 s; Phoenix_fireBall 30 m/s (Phoenix_fireBall.cs:26) meets the target's body at (0, 0.675, 9.709) 0.231 s later as fireBall_hit (calc.txt; the part spawns it: builds); the Phoenix's later AI shots are left out (plans/fx_mole/decisions.md 32's AI rule: the command's own shot only, question 2); Yield 0.3 (:22426): standby 0.6 s (:22247)",
      "builds": ["phoenix_fireBall_hit"],
      "cues": [
        [0, "voice", "summonAttack"],
        [0, "fx", "Phoenix4", {"d": 2, "single": true, "kill": 10, "ring": false, "clips": [[0, "root", 0, 2], [0.3, "nAttack", 0.3, 1], [1.1, "root", 0.2, 2]]}],
        [0.8, "fx", "phoenix_fireBall", {"d": 3, "y": 2.4, "rot": [14.42, 0, 0], "to": [0, 0.6, 10]}]
      ]
    },
    "skyCrimson": {
      "why": "Monkey.cs RPC_skyCrimson (:27138-27527), Sky Crimson (#224): needs Phoenix4 (:7790, :27294); clip, 0.2 s fade (:27439), voice skyCrimson (load :27475, PlayOneShot :27523) at 0; Yield 0.3 (:27517): Phoenix.RPC_skyCrimson (:27342; Phoenix.cs:3360-3994), times from its start (+0.3): CrossFade(\"skyCrimson1\", 0.2) (:3908), pheonix_cry (:3932), skyCrimson_dust at the Phoenix, its rotation (:3942) at 0.3; Yield 2 (:3971): every renderer off (:3507-3529; the colour ramp :3572 left out) at 2.3; Yield 1 (:3992): at 3.3 one skyCrimson_fire per enemy within 24 m (:3622): fireDir = (target centre - Phoenix - 20 up).normalized, firePos = target centre - 12 fireDir (:3645-3655) = (0, 11.694, 5.425), rot [67.59, 0, 0] (calc.txt), and its sound phoenix_skyCrimson (:3696); ProjectileControl life 2 (:1813-1822), Phoenix_skyCrimson_fire 16 m/s (Phoenix_skyCrimson_fire.cs:28, :53) bursting only on layer 0, the floor (:143-179: it passes the target): skyCrimson_hit, identity (Phoenix.cs:1856) at (0, 0, 10.247) 0.791 s later, 4.09 s (calc.txt; builds); Yield 2 (:3979): skyCrimson2 and the renderers back (:3723-3751) at 5.3; Yield 0.5 (:3977): skyCrimson_dust again (:3795) and a 300 HP heal at 5.8; Yield 0.5 (:3983): standby 6.3 (:3838); the Monkey: Yield 0.3 (:27521), standby 0.6 s (:27383)",
      "builds": ["phoenix_skyCrimson_hit"],
      "cues": [
        [0, "voice", "skyCrimson"],
        [0, "fx", "Phoenix4", {"d": 2, "single": true, "kill": 10, "hide": [2.3, 5.3], "ring": false, "clips": [[0, "root", 0, 2], [0.3, "skyCrimson1", 0.2, 1], [5.3, "skyCrimson2", 0, 1], [6.3, "root", 0.2, 2]]}],
        [0.3, "fx", "phoenix_skyCrimson_dust", {"d": 2}],
        [3.3, "fx", "phoenix_skyCrimson_fire", {"d": 5.425, "y": 11.694, "rot": [67.59, 0, 0]}],
        [5.8, "fx", "phoenix_skyCrimson_dust", {"d": 2}]
      ]
    },
    "planetBreaker": {
      "why": "Monkey.cs RPC_planetBreaker (:31599-32020), Planet Breaker (#324): needs Gadina4 (:8120, :31755); clip, 0.2 s fade (:31900), voice planetBreaker (load :31936) and planetBreaker_ring createEffect at the Monkey, identity (:31967-31977) at 0; Yield 0.3 (:32005): Gadina.RPC_planetBreaker (:31803; Gadina.cs:5403-5884), times from its start (+0.3): CrossFade(\"planetBreak\") (:5817), planetBreaker1 at the Gadina, its rotation (:5843; followPosition), gadina_cry (:5857) at 0.3; Yield 0.8 (:5883): planetBreaker2 (:5545; AlphaTimer, its own Sounds/gadina_planetBreaker) at 1.1; three pulses 0.3 s apart (i < 3 :5864, Yield :5875) at 1.4 / 1.7 / 2.0: inside 5 m nAttack_hit on a hit (:5589-5664), 5-12 m a flat hit with no effect (:5675-5698): the target 8 m from the Gadina is in the outer ring: nothing drawn; Yield 0.6 (:5870): standby 2.6 (:5735); the Monkey: Yield 0.3 (:32014), standby 0.6 s (:31844)",
      "builds": ["gadina_sword4", "gadina_shield4"],
      "cues": [
        [0, "voice", "planetBreaker"],
        [0, "fx", "planetBreaker_ring"],
        [0, "fx", "Gadina4", {"d": 2, "single": true, "kill": 10, "ring": false, "attach": [["gadina_sword4", "mount_Hand_R"], ["gadina_shield4", "mount_Hand_L"]], "clips": [[0, "root", 0, 2], [0.3, "planetBreak", 0.3, 1], [2.6, "root", 0.2, 2]]}],
        [0.3, "fx", "gadina_planetBreaker1", {"d": 2}],
        [1.1, "fx", "gadina_planetBreaker2", {"d": 2}]
      ]
    },
    "instantBlaze": {
      "why": "Monkey.cs RPC_instantBlaze (:37266-37651), Instant Blaze (#412): needs Phoenix4 (:8388, :37433); no voice (none loaded); clip, 0.2 s fade (:37613); Yield 0.3 (:37646): the Phoenix aimed flat at the target (:37481-37509: straight ahead), Phoenix.RPC_instantBlaze (:37516; Phoenix.cs:2685-3288), times from its start (+0.3): CrossFade(\"instantBlaze\", 0.2) (:3240), pheonix_cry (:3258) at 0.3; Yield 0.5 (:3275): the dash at moveSpeed 12 (:2826) and instantBlaze_ring at the Phoenix, its rotation, riding it (:2837; followPosition; its own Sounds/instantBlaze; the part spawns it: builds) at 0.8; four hit boxes 0.2 s apart (i < 4 :3148, Yield :3281) at 1.0 / 1.2 / 1.4 / 1.6 (burn on a hit, no effect drawn :2942-2987; the reference's 0.7-1.3 s from the Phoenix's start); moveSpeed 6 (:3156) and a 200 HP heal (:3167) at 1.6; stop (:3075) at 1.8, standby (:3096) 1.9: 9.6 + 1.2 = 10.8 m, so it ends 12.8 m ahead, through the target (collisions ignored meanwhile, :3203, :3038; calc.txt); the summon moves, the hero does not (plans/fx_chameleon/decisions.md 30); the Monkey: Yield 0.3 (:37641), standby 0.6 s (:37557)",
      "builds": ["phoenix_instantBlaze_ring"],
      "cues": [
        [0, "fx", "Phoenix4", {"d": 2, "single": true, "kill": 10, "moves": [[0.8, 12], [1.6, 6], [1.8, 0]], "ring": false, "clips": [[0, "root", 0, 2], [0.3, "instantBlaze", 0.2, 1], [1.9, "root", 0.2, 2]]}]
      ]
    },
    "earthGuard": {
      "why": "Monkey.cs RPC_earthGuard (:37696-38160), Earth Guard (#413): needs Gadina4 (:8439, :37877); clip, 0.2 s fade (:38068), voice summonDefense (the code's own pick: load :38104) at 0; Yield 0.3 (:38159): +1000 hate on the target, no damage (:37958), Gadina.RPC_earthGuard (:37971; Gadina.cs:5028-5370), times from its start (+0.3): CrossFade(\"guard\") (:5313), earthGuard_ring at the Gadina, its rotation (:5331; EffectControl life 10, followPosition + followState), gadina_cry (:5343) at 0.3; Yield 0.5 (:5360), then six heals 2 s apart (i >= 6 :5261, Yield 2 :5362) at 0.8 ... 10.8 (no effect drawn), Yield 0.5 (:5367): standby 13.3 (:5209): the Gadina cut at 10 s; the ring ends by its own life at 10.3; the Monkey: Yield 0.3 (:38152), standby 0.6 s (:38012)",
      "builds": ["gadina_sword4", "gadina_shield4"],
      "cues": [
        [0, "voice", "summonDefense"],
        [0, "fx", "Gadina4", {"d": 2, "single": true, "kill": 10, "ring": false, "attach": [["gadina_sword4", "mount_Hand_R"], ["gadina_shield4", "mount_Hand_L"]], "clips": [[0, "root", 0, 2], [0.3, "guard", 0.3, 1]]}],
        [0.3, "fx", "gadina_earthGuard_ring", {"d": 2}]
      ]
    }
  }
},
"@EarthFormAttack:summonAttack#0": {
  "why": "Earth Form Attack, stage 1: Monkey.cs RPC_gadinaArmor_nAttack1 (:40994-41546), the normal attack in Earth Form (dispatcher :9749-9876): clip summonAttack, 0.2 s fade (:41360), voice summonAttack (load :41396, PlayOneShot :41408), Sounds/nAttack1 (:41496-41506), the worn Gadina Armor (gadinaArmor, parented to the Monkey at the Earth Form cast, :40719-40747) plays its nAttack1 (:41444-41449) and gAttack1_ring createEffect at the Monkey, his rotation (:41461-41473) at 0; Yield 0.3 (:41534): the right punch at 0.3 (FindAreaTarget(TransformDirection(0.5, 0, 1.5)), 2 m, :41145), Yield 0.3 (:41538): the left at 0.6 (:41222): gadinaArmor_hit only on a hit (:41184, :41261): the 10 m target is out of reach (plans/fx_bison/decisions.md 16); Yield 0.4 (:41544): standby 1.0 s (:41304); the armour is shown already worn (the Earth Form status chaAdjust(120) :40671: cut at 10 s; plans/fx_mole/decisions.md 37's form-already-on rule), its clips the hero's code plays: nAttack1 at 0, nAttack2 at 0.9, nAttack3 at 1.7 (the later stages' own cues), back to root when the Monkey stands by (CrossFade(\"root\", 0.2) Monkey.cs:567-587) at 2.5",
  "cues": [
    [0, "voice", "summonAttack"],
    [0, "sound", "nAttack1"],
    [0, "fx", "gadinaArmor", {"single": true, "kill": 10, "clips": [[0, "nAttack1", 0, 1], [0.9, "nAttack2", 0, 1], [1.7, "nAttack3", 0, 1], [2.5, "root", 0.2, 2]]}],
    [0, "fx", "gAttack1_ring"]
  ]
},
"@EarthFormAttack:summonAttack#1": {
  "why": "Earth Form Attack, stage 2: Monkey.cs RPC_gadinaArmor_nAttack2 (:41597-42089), started inside stage 1's 0.3-0.8 s window (:9774-9796) and waiting to actionTime + 0.9 (Yield :42088; actionTime is stage 1's: no stage sets it before its standby, :42017): voice sAttack1 (load :41727, PlayOneShot :41739), Sounds/nAttack2 (:41773-41785), clip summonAttack, 0.2 s fade (:41805), the armour's nAttack2 (:41836) and gAttack2_ring at the Monkey (:41853-41865) at 0 (0.9 s after stage 1); Yield 0.2 (:42075): two hits 0.2 s apart within 4 m (i < 2 :42059, Yield :42077, :41924) at 0.4 / 0.6: out of reach; Yield 0.2 (:42071): standby 0.8 s (:42012)",
  "cues": [
    [0, "voice", "sAttack1"],
    [0, "sound", "nAttack2"],
    [0, "fx", "gAttack2_ring"]
  ]
},
"@EarthFormAttack:summonAttack#2": {
  "why": "Earth Form Attack, stage 3: Monkey.cs RPC_gadinaArmor_nAttack3 (:42131-42596), started in stage 2's window (:9817-9849), waiting to actionTime + 1.7 (Yield :42595): voice sAttack2 (load :42261, PlayOneShot :42273), Sounds/nAttack2 (:42307-42319), clip summonAttack, 0.2 s fade (:42339), the armour's nAttack3 (:42370) and gAttack3_ring at the Monkey (:42387-42399) at 0 (1.7 s after stage 1); Yield 0.4 (:42584): camera shake (:42434, left out) and one hit 3 m ahead, 3 m wide (:42453): out of reach; Yield 0.4 (:42582): standby 0.8 s (:42535)",
  "cues": [
    [0, "voice", "sAttack2"],
    [0, "sound", "nAttack2"],
    [0, "fx", "gAttack3_ring"]
  ]
},
"summonDefense": {
  "why": "Monkey.cs RPC_summonDefense (:22485-22940), Summon Defense (#122), the only skill on this clip: needs a summon (:7589); clip, 0.2 s fade (:22847), voice summonDefense (load :22883, PlayOneShot :22936) at 0; Yield 0.3 (:22923): the order to Phoenix / Gadina / Ja (:22641-22736): the summon (Phoenix 4, standing 2 m ahead, question 1) if standing or running turns to face the Monkey (LookAt his flat position :2000: yaw 180) and cries (pheonix_cry :2009), its hate cleared and its AI set to defense (Phoenix.cs:1941-1998; the walk back by its AI is left out, question 2); Yield 0.3 (:22934): standby 0.6 s (:22794)",
  "cues": [
    [0, "voice", "summonDefense"],
    [0, "fx", "Phoenix4", {"d": 2, "single": true, "kill": 10, "turn": 0.3, "ring": false, "clips": [[0, "root", 0, 2]]}]
  ]
},
"summonRelease": {
  "why": "The summonRelease clip: Unsummon (RPC_unsummon, PlayAnimation(\"summonRelease\", 0.2) Monkey.cs:23458), Summon Release (RPC_summonRelease :23835), Summon Soul (RPC_summonSoul :24519) (pipeline/clip_calls.js), one per play, even chance, picked anew on every play (one tile each, poolChains); each needs a summon (dispatcher :7617-7672, :8504): Phoenix 4 standing 2 m ahead (question 1), cut at 10 s",
  "skills": {
    "unsummon": {
      "why": "Monkey.cs RPC_unsummon (:22983-23545), Unsummon (#123): clip summonRelease, 0.2 s fade (:23458), voice unsummon (load :23494, PlayOneShot :23532) at 0; Yield 0.3 (:23541): half the summon's MP back (Phoenix4 35, :23202), SendMessage(\"unsummon\") (:23367): Phoenix.unsummon (Phoenix.cs:5127-5308): actionState dead, ko clip (:5264), pheonix_unsummon (:5276), destroyed 1 s later (Yield 1 :5306, Destroy :5222): end 0.3 (the Bat guardian's end option: the unsummon, gone 1 s later); Yield 0.3 (:23537): standby 0.6 s (:23405)",
      "cues": [
        [0, "voice", "unsummon"],
        [0, "fx", "Phoenix4", {"d": 2, "single": true, "end": 0.3, "ring": false, "clips": [[0, "root", 0, 2]]}]
      ]
    },
    "summonRelease": {
      "why": "Monkey.cs RPC_summonRelease (:23579-23920), Summon Release (#124): clip summonRelease, 0.2 s fade (:23835), voice unsummon (the code's own pick: load :23871, PlayOneShot :23916) at 0; Yield 0.3 (:23907): Phoenix / Gadina / Ja / Gaos get SendMessage(\"summonRelease\") (:23735; Buiten and Lavu are unsummoned, :23743): Phoenix.summonRelease (Phoenix.cs:2028-2057): 1200 hate on the Monkey, isSummon off, layer 15 (a neutral enemy): nothing changes on screen; its AI then turns on the Monkey (left out, question 2); Yield 0.3 (:23911): standby 0.6 s (:23782)",
      "cues": [
        [0, "voice", "unsummon"],
        [0, "fx", "Phoenix4", {"d": 2, "single": true, "kill": 10, "ring": false, "clips": [[0, "root", 0, 2]]}]
      ]
    },
    "summonSoul": {
      "why": "Monkey.cs RPC_summonSoul (:23949-24632), Summon Soul (C skill): a player target (dispatcher :8490-8555): the Monkey himself (plans/fx_sheep/decisions.md 1: ally skills as self-casts); clip summonRelease, 0.2 s fade (:24519), voice summonSoul (load :24555, PlayOneShot :24600) at 0; Yield 0.4 (:24630): once per summon (isTimeOut summonSoul :24124, addTimeOut 999 :24139), summonSoul_ring createEffect at the Monkey, his rotation (:24150-24162; EffectControl 1 + 1 s, followPosition), and the summon's soul status on the target, Phoenix4: phoenixSoul 4 for 240 s (:24234) -> CharacterControl addStatus: deltaAtk(10 sLv) and phoenixSoul createEffect at mChar.bounds.center + 0.5 mChar.height up, identity (CharacterControl.cs:38149-38179): the Monkey's CharacterController centre 0.7, height 1.3 (rip Monkey.prefab:949-955) -> 1.35 m up (calc.txt; EffectControl 1 + 1 s, followPosition, its own Sounds/fireSoul); Yield 0.2 (:24608): standby 0.6 s (:24436)",
      "cues": [
        [0, "voice", "summonSoul"],
        [0, "fx", "Phoenix4", {"d": 2, "single": true, "kill": 10, "ring": false, "clips": [[0, "root", 0, 2]]}],
        [0.4, "fx", "summonSoul_ring"],
        [0.4, "fx", "phoenixSoul", {"y": 1.35}]
      ]
    }
  }
},
"sentinalGuard1": {
  "why": "Sentinel Guard (Stone Sentinel #443's Earth Form charge: the attack button held in Earth Form with >= 10 MP / SP, Monkey.cs:10282-10340), RPC_gadinaArmor_sentinalGuard (:42635-43069): clip sentinalGuard1, 0.1 s fade (:42892), the armour's cAttack1 (:42918-42923), voice summonDefense (the code's own pick: load :42959, PlayOneShot :43054; TTO the same, TTO1102 Monkey.<RPC_gadinaArmor_sentinalGuard>d__243) at 0; Yield 0.5 (:43066): sentinalGuard2 (the next step); the armour shown already worn (Earth Form, cut at 10 s; as Earth Form Attack), its clips: cAttack1 at 0, cAttack2 looped at 0.5 (:42786-42791), cAttack0 at the release 6.6 (RPC_gadinaArmor_sentinalGuard0 :43279-43282), root when the Monkey stands by 0.3 s later (:567-587)",
  "cues": [
    [0, "voice", "summonDefense"],
    [0, "fx", "gadinaArmor", {"single": true, "kill": 10, "clips": [[0, "cAttack1", 0, 1], [0.5, "cAttack2", 0, 2], [6.6, "cAttack0", 0, 1], [6.9, "root", 0.2, 2]]}]
  ]
},
"sentinalGuard2": {
  "why": "RPC_gadinaArmor_sentinalGuard case 2 (Monkey.cs:42751-42829), 0.5 s after the press: PlayAnimation(\"sentinalGuard2\", 0), wrapMode Loop (:42770-42775), sentinalGuard_ring createEffect at the Monkey, his rotation (:42797-42815; EffectControl life 99, followPosition + followState: cut when his command becomes sentinalGuard0 at the release; its own looping Sounds/sentinalGuard_ring) at 0; while held, every 3 s (Yield 3 :43062) MP -8 with Revised Magic #414 (:43012) and a heal of 0.2 MHP (:43017; no effect drawn) at 0, 3, 6 s of this step; held until the button is released (or MP < 10, :43006-43039): the third heal, then the release at 6.1 s into this step (the channel-until-release rule: three ticks)",
  "cues": [
    [0, "fx", "sentinalGuard_ring", {"cut": 6.1}]
  ]
}
}
```

## Page changes (for the page_pipeline builder; index.html is edited elsewhere, so anchor by text)

- **SEQ.monkey** (index.html, the `monkey:` line of SEQ):
  - replace `"Sentinel Guard: sentinalGuard1 sentinalGuard2* sentinalGuard0"` with `"Sentinel Guard: sentinalGuard1@0.5 sentinalGuard2*@6.1 sentinalGuard0"`;
  - add `"Upheaval: upheaval*@3.1 root~0.35@0.35"`;
  - add `"Earth Form Attack: summonAttack@0.9 summonAttack~@0.8 summonAttack~"`.
  - Comment for the block: "the Monkey (plans/fx_monkey/skills_b.md): Sentinel Guard's sentinalGuard2 at 0.5 s (Yield 0.5 Monkey.cs:43066), held for three heals 3 s apart, released at 6.6 s (:43062; the channel-until-release rule), sentinalGuard0 cut in (:43270); Upheaval's waves at 2.0 / 2.5 / 3.0 s (:35421, :35153), released at 3.1 s, root with RPC_upheaval0's 0.35 s fade (:35674), standby 0.35 s later (:35685); Earth Form Attack's stages at actionTime + 0.9 / + 1.7 (:42088, :42595), each PlayAnimation(summonAttack, 0.2) (:41805, :42339)".
  - LOOPS.monkey `upheaval` can stay: the sequence now owns the clip.
- **SEQ_SKILL.monkey** (merge with skills_a's): `"@EarthFormAttack": "earthForm", "@SentinelGuard": "stoneSentinel", "@Upheaval": "lavu"` (Bible icons monkey_earthForm5, monkey_stoneSentinel5, monkey_lavu2).
- **The per-step cue key** in fxStart: try `"@<seq>:<clip>#<step>"` before the existing lookups. The `ch.id` / `"@" + ch.name` forms take `+ "#" + step`, and `step` is the step index fxStart already receives.
  - This fixes any sequence that plays one clip at several steps. Only the Earth Form Attack needs it today.
  - `pipeline/wardrobe_fx_check.py` must strip the `#<n>` when it maps a key to its tile.
- **wardrobe_fx_check.py OPTS** += `"clips", "attach", "lavu"` (parts.md) and `"hide", "moves", "turn", "ring"` (this report).
- **Extractor (lead, wardrobe_fx.py)**, on top of parts.md's EXTRA_FOLDERS / FIELD_PREFABS / SOUND_REFS:
  - FIELD_PREFABS["monkey"] for the summons' move prefabs this block cues:
    - from (`gameassets/characters/elementals/phoenix/phoenix4`, `Phoenix`, field): `phoenix_fireBall` (fireBall), `phoenix_fireBall_hit` (fireBall_hit), `phoenix_instantBlaze_ring`, `phoenix_skyCrimson_dust`, `phoenix_skyCrimson_fire`, `phoenix_skyCrimson_hit`;
    - from (`.../gadina/gadina4`, `Gadina`, field): `gadina_earthGuard_ring`, `gadina_planetBreaker1`, `gadina_planetBreaker2`.
    - probe3 walks every one.
  - LAYOUTS `Phoenix_fireBall`: `[("mLv", "i")]`.
  - SOUND_REFS |= `{"Phoenix", "Gadina"}` so the summon part can play:
    - Phoenix: `Phoenix_pheonix_cry`, `Phoenix_phoenix_skyCrimson`, `Phoenix_pheonix_unsummon`;
    - Gadina: `Gadina_gadina_cry`.
- **Icons:** no CLIP_SKILLS line is needed. The pool members' keys are Bible ids, and `summonAttack`, `summonDefense` and `summonRelease` already have their own icon entries (`wardrobe/data/icons/hd/index.json`).

## Parts needed (what this scope asks of parts.md's builders)

1. **Rotate** (parts.md part 3): as written.
2. **Monkey_lavu's upheaval state** (parts.md part 2): `"lavu": "upheaval"`, plus `release` (this report).
   - The cue spawns it at y 4 (its standby height). It Slerps onto the circle over the first 3 s (Monkey_lavu.cs:637-648).
   - At `release` age it returns to standby: RotateTowards the Monkey + 4 up at 1 rad/s, 8 m/s.
3. **The armour's clip timeline** (parts.md part 8): `clips` [[age, clip, fade, wrap]].
   - Earth Form Attack: nAttack1-3 at 0 / 0.9 / 1.7, root at 2.5.
   - Sentinel Guard: cAttack1, cAttack2 Loop, cAttack0, root.
   - skills_a's Earth Form block writes `anims` for the same thing. One name is needed, and parts.md's `clips` is the interface.
4. **The summon part** (parts.md part 9) plus four options:
   - **`ring: false`**: no summon clip and no summon ring at the spawn (it stands already summoned); `clips` starts at root.
   - **`hide: [from, to]`**: every renderer off between those ages (Sky Crimson, Phoenix.cs:3507-3529, :3743-3751).
   - **`moves: [[age, m/s], ...]`**: walks the summon along its own forward at that speed from that age (Instant Blaze, :2826, :3156, :3075). The part also spawns `phoenix_instantBlaze_ring` riding it at the first move (:2837): `api.spawn` with followNode, in the entry's builds.
   - **`turn: age`**: the summon turns to face the hero on the flat (yaw +180) and cries (Summon Defense, :2000-2009).
   - **`end`**: for Phoenix, the ko clip, `Phoenix_pheonix_unsummon`, and gone 1 s later (Phoenix.cs:5264-5306).
   - **The cries:** the part plays `Phoenix_pheonix_cry` / `Gadina_gadina_cry` with the clips the code pairs them with: nAttack, skyCrimson1, instantBlaze, planetBreak, guard (:2612, :3932, :3258, Gadina.cs:5857, :5343), and with `turn`. It plays `Phoenix_phoenix_skyCrimson` at the ball (Sky Crimson age 3.3, :3696). One way: a fifth `clips` element, the sound, e.g. `[0.3, "nAttack", 0.3, 1, "Phoenix_pheonix_cry"]`; the builder picks. The block leaves the sounds to the part.
5. **Two summon projectiles** (monkey.js, with parts.md part 1's shot mover):
   - `phoenix_fireBall`: 30 m/s, stops on `to` (the body), spawns `phoenix_fireBall_hit`.
   - `phoenix_skyCrimson_fire`: 16 m/s along its forward, no gravity. It bursts only on the floor (y 0), spawning `phoenix_skyCrimson_hit` identity at the contact; ProjectileControl life 2 caps it.

## Left out (with reasons)

- Runic Flame / Sand's segments: the hero stands (Bison decision 17).
- The camera's motion blur (:29489, :34177), colour ramp (Phoenix.cs:3572) and shakes (:35258, :42434): camera effects, as in every class.
- The summons' AI after the command: Summon Attack's later shots, Summon Defense's walk back, a released summon attacking the Monkey (Mole decision 32; question 2).
- Hits on the 10 m target that draw nothing (Upheaval's 12 m RPC_AddDamage, Planet Breaker's outer ring, Instant Blaze's burns), and hits that cannot reach it: the Earth Form punches, Damage Cast's 2 m, Planet Breaker's 5 m inner ring.
- Heals, hate, MP returns and SP costs: numbers only.
- Lavu's own `RPC_nAttack` attacks (Lavu.cs): this scope's Upheaval does not call them.

## Open questions (each with my recommendation)

1. **Which summon stands in the generic command tiles?** (Summon Attack / Defense / Unsummon / Release / Soul)
   - Recommended: **Phoenix 4**. Every command reaches it, and its reactions are all in Phoenix.cs. Summon Soul then shows phoenixSoul.
   - Alternative: a random summon per play (Phoenix 4 / Ja 4 / Gadina 4 / Gaos) with the matching soul. That needs one roll shared by two cues (the summon and its soul), which the page has only for `p` chances. It also needs every summon's command reactions built.
2. **The summons' follow-ups.**
   - Recommended: cue only what the command itself makes happen: Summon Attack's first shot, Defense's turn and cry, Unsummon's ko.
   - The AI's later behaviour is a separate job, offered to the user (Mole decision 32's Barrel Bot).
3. **How long the hold-to-channel skills are held.**
   - Recommended: three ticks, by the SEQ comment's "three hits when it runs until the player releases":
     - Upheaval: three waves, released at 3.1 s;
     - Sentinel Guard: three heals, released at 6.6 s.
   - Alternative: 10 s (both are SP / MP-limited channels: Upheaval costs 1 SP a wave, about 50 s at SP 100). That shows Lavu's full circling: at 3.1 s it has only just reached the ring.
4. **Runic trail.** Recommended: none (the game drops no segment for a Monkey standing still). Alternative: a demo trail of segments 1.58 m apart behind him, which the game never shows standing.
5. **The per-step cue key.**
   - Recommended: the small fxStart addition (Page changes).
   - Fallback with no page change: one entry `@EarthFormAttack:summonAttack`. All three stages would then say summonAttack and show gAttack1_ring, which is wrong for stages 2 and 3.
6. **Lavu between rounds.** With the loop toggle on, `single: true` keeps one Lavu, but it will not start a new circle each round. Recommended: accept it; the tile plays once by default.
   - The same holds for the armour's `clips` and the summons' `clips` under `single`.
   - A part could restart its timeline when a `single` cue comes again; offered to the parts builder.
7. **Earth Form tiles show the armour without its cast.** Recommended: yes, as Mole decision 37's Kaiser. Earth Form's own cast tile (skills_a) shows the summon clip.
8. **Earth Guard's 13 s guard.** Recommended: cut at 10 s, the summon rule. The ring ends at 10.3 s by its own life.

## Offers for the Bible (never written there)

1. **Runic Sand is silent in BB.** It loads `Voices/runicSand` (Monkey.cs:34307), which the game files don't have ("Cannot find runicSand voice" :34322). TTO plays `Sounds/runicSand` instead (TTO1102 `Monkey.<RPC_runicSand>d__219`).
2. **Shared voices:** Sentinel Guard and Earth Guard say the Summon Defense line (:42959, :38104); Summon Release says the Unsummon line (:23871); Instant Blaze has no voice. Same in TTO.
3. **Upheaval timing:**
   - the first wave comes 2 s after the hold starts, then every 0.5 s (:35421, :35153);
   - 1 SP per wave with Revised Skill, 2 without (:35196);
   - it ends when SP drops to 1 or the button is released (:35265, :10681);
   - Lavu circles the Monkey 6 m out, one lap every 3 s, after a 3 s glide in (Monkey_lavu.cs:632-662).
4. **Sky Crimson timing:**
   - the Phoenix vanishes 2 s after the order and returns at 5 s (Phoenix.cs:3507-3529, :3743-3751);
   - the balls fall at 3 s from 20 m above the Phoenix, toward every enemy within 24 m, at 16 m/s;
   - they burst only on the ground (Phoenix_skyCrimson_fire.cs:143), so a flying or jumping target is hit by the 5 m burst below it, not by the ball;
   - the Phoenix heals 300 HP at 5.5 s (:3817).
5. **Planet Breaker's pulses** come 1.1 / 1.4 / 1.7 s after the order (Gadina.cs:5864-5883; the reference gives the count only).
6. **Earth Guard's ring** lasts 10 s (its EffectControl), while the six heals run to 10.5 s and the guard to 13 s (Gadina.cs:5261-5367).
7. **Summon Soul works once per summon** (`addTimeOut("summonSoul", 999)` on the summon, Monkey.cs:24124-24139: "SummonSoul has already been used"). Worth a line on the card if it is not there.

## Verification (2026-11-13)

A read-only re-trace by the checker on the office PC. My scripts and outputs are in `checks\fx_monkey_research\verify\`. They are the same tools as skills_a's Verification:
- `clean.py`: prints a .cs range with the opaque predicates worked out.
- `blocks.py`: parses this block. It has 10 keys and 50 cues, is valid JSON, and every time list is in order.
- `cont.txt`: BB's container.
- `ripgap.txt`: the voices / sounds the rip lacks.
- `probe.txt`: `wardrobe_fx.py monkey --probe`.
- `fix.py` -> `b_fixed.json`: the whole block corrected, re-parsed. `b_changed.txt` holds the changed keys, pasted under item 4.

The Verification wins over the report body.

**Checked and confirmed** (clip_flow.js, the waits added up):
- **Earth Form Attack.**
  - Stage 1 sets actionTime and command gAttack1 at its start (:41339-41345). Its standby at 1.0 checks `myCommand == "gAttack1"` (:41280-41304).
  - Stage 2 (Yield(2, actionTime - now + 0.9), :42088) and stage 3 (+ 1.7, :42595) set attack and their own command when they start, inside the previous stage's window (:42047-42052, :42570-42573). So the earlier stages never reach standby, and actionTime stays stage 1's. The stages come at 0.9 / 1.7, and the last standby at 2.5.
  - The voices: summonAttack / sAttack1 / sAttack2. The sounds: Sounds/nAttack1 / nAttack2 / nAttack2. The rings: gAttack1-3_ring.
- **Sentinel Guard:**
  - Yield 0.5, then case 2: sentinalGuard2 cut in, Loop (:42770-42775), the armour's cAttack2 Loop, sentinalGuard_ring (:42815).
  - Heals at 0.5 / 3.5 / 6.5 (Yield 3, :43062; MP - 8 with #414, :43012).
  - The release: sentinalGuard0 cut in (:43270), cAttack0 (:43279), standby 0.3 later (:43297).
- **Upheaval:**
  - At 0: the clip with a 0.2 fade and Loop, the voice, upheaval_ring, `mUpheavalTimer = now + 2` (:35421), Lavu SendMessage (:35430).
  - Waves every 0.5 s after that (:35147-35153), so 2.0 / 2.5 / 3.0.
  - RPC_upheaval0: root with a 0.35 fade (:35674), standby 0.35 later (:35685).
- **The Phoenix's moves** (times from the Phoenix's own start; on the tile, + 0.3):
  - Sky Crimson: 0 / 2 (renderers off, :3529) / 3 (the ball and phoenix_skyCrimson, :3696) / 5 (skyCrimson2, renderers on) / 5.5 (dust) / 6 (standby).
  - Instant Blaze: 0 (CrossFade 0.2, the cry) / 0.5 (moveSpeed 12, the ring, :2826-2837) / hits every 0.2 s / moveSpeed 6 (:3156) / stop at 1.5 (:3075) / standby at 1.6. That is 9.6 + 1.2 = 10.8 m.
  - nAttack: the shot at actionTime + 0.5 (:2354), standby 0.3 later (:2634).
  - Summon Attack's `AI_setTimer(3)` sets T0 = now - 3 (Phoenix_AI.cs:507-511): straight into the attack window, as the Bible says (monkey-skill-reference.md, the Phoenix AI cycle).
- **The Gadina's moves:**
  - Planet Breaker: 0 (planetBreak, planetBreaker1, the cry) / 0.8 (planetBreaker2) / pulses at 1.1 / 1.4 / 1.7 / standby at 2.3.
  - Earth Guard: 0 / 0.5, then 2 s ticks.
- **Geometry** (all match):
  - The Summon Attack shot: (0, 2.4, 3) to (0, 0.6, 10). The pitch is atan(1.8 / 7) = 14.42 deg. It meets the body front after 6.918 m = 0.231 s, at y 0.677.
  - The Sky Crimson ball: fireDir (0, -19.4, 8) / 20.985. firePos (0, 11.694, 5.425), rot 67.59. It lands at z 10.247 after 12.649 m = 0.791 s, at 4.09 s.
- **Sounds and voices.**
  - Every voice the block names is in the rip's `monkey/voices` (planetBreaker, runicFlame, sAttack1, sAttack2, skyCrimson, summonAttack, summonDefense, summonSoul, unsummon, upheaval).
  - The sound cues `nAttack1`, `nAttack2` and `runicSand` are in `monkey/sounds`.
  - BB's container has no `voices/runicsand` (`cont.txt`), so BB's load fails. TTO loads `GameAssets/characters/heroes/monkey/sounds/runicSand` (TTO1102 pseudo/Monkey.c:16809).
  - lavu_flyby / lavu_upheaval are the effects' own AudioSources (probe: upheaval_ring, upheaval). rip_wav finds them anywhere (wardrobe_fx.py:772-779).
- **The probe** (`probe.txt`): upheaval_ring 3 + 1 followState (no drawn component), upheaval 2 s, planetBreaker_ring 1 s, summonSoul_ring and phoenixSoul 1 + 1 followPosition, sentinalGuard_ring 99 followState (looping sound), gAttack1-3_ring. runicFlame_ring / runicSand_ring fail on "no layout for Rotate (16 field bytes)", as the report says.
- **Pools, icons and TTO:**
  - Every pool member key is a Bible id with an icon (assets.js `monkey_runicFlame1` ... `monkey_summonSoul5`).
  - The SEQ tokens parse (index.html SEQ_ALT :1376). A later step with no fade marker is a cut (startStep, :1539).
  - No TTO clip or cue is in scope, and the TTO released rule holds.

**Findings:**

1. **The per-step key would hide the Earth Form Attack tile and give its three stages to every summonAttack pool member.**
   - **Why it breaks:** poolChains looks for a sequence's own key with `tab[ch.id + ":" + clip] || tab["@" + ch.name + ":" + clip]` (index.html:1423). With only `#0` / `#1` / `#2` keys, `"@EarthFormAttack:summonAttack"` is not found. So Earth Form Attack becomes the `summonAttack` pool's host (`hosts[0]`, :1427-1428) and is set `hidden` (:1438). Summon Attack, Sky Crimson, Planet Breaker, Instant Blaze and Earth Guard then each play its three steps (0.9 / 0.8 / 0.8 s), and the Earth Form Attack tile disappears (:3653).
   - **Correction:**
     - Stage 1 keeps the plain sequence key `"@EarthFormAttack:summonAttack"`. Stages 2 and 3 are `"@EarthFormAttack:summonAttack#1"` / `"#2"`.
     - fxStart tries the step's key first:

       ```js
       tab[ch.id + ":" + clip + "#" + step] ?? tab["@" + ch.name + ":" + clip + "#" + step] ?? tab[ch.id + ":" + clip] ?? tab["@" + ch.name + ":" + clip]
       ```

       This sits before `tab[clip]` (index.html:5319). With that, poolChains needs no change.
     - `wardrobe_fx_check.py`'s `split_key` strips `#<n>` (and checks that step n of the sequence plays the clip). Its `entry_for` also needs the step, or it tallies stage 1's cues for all three stages.
     - Read this first 8, question 5 and "Page changes" read so from here.
2. **The summons' sounds: wrong names, and not built.**
   - **Wrong names:** SOUND_REFS names a summon's clip `<script, first letter lower case>_<AudioClip name>` (wardrobe_fx.py:237-244; the Mole's `sound:autoGyroGun_create`, `sound:kingKaiser_kaiser_create`). So the four sounds are `phoenix_pheonix_cry`, `phoenix_phoenix_skyCrimson`, `phoenix_pheonix_unsummon` and `gadina_gadina_cry`, not `Phoenix_...` / `Gadina_...`. The AudioClips are `Assets/AudioClip/pheonix_cry.wav`, `phoenix_skyCrimson.wav`, `pheonix_unsummon.wav` and `gadina_cry.wav`.
   - **Not built:** "the block leaves the sounds to the part", but the extractor exports only what cues and `builds` name (cue_names :834-849). As the Mole's entries do, each entry lists its part's sounds in `builds`:

     | entry | builds added |
     |---|---|
     | summonAttack / instantBlaze / summonDefense | `sound:phoenix_pheonix_cry` |
     | skyCrimson | `sound:phoenix_pheonix_cry`, `sound:phoenix_phoenix_skyCrimson` |
     | unsummon | `sound:phoenix_pheonix_unsummon` |
     | planetBreaker / earthGuard | `sound:gadina_gadina_cry` |

   - Corrected in item 4.
3. **Sentinel Guard's icon.** Each earlier SEQ_SKILL tile got an `OWN_TILE` line in `pipeline/wardrobe_skill_icons.py` so its HD Bible icon is written (sheep, bat, cat, chameleon; :67-73). Without one, the tile falls back to `icons/skills/monkey/stonesentinel5.webp`.
   - Add `OWN_TILE["monkey"]["stoneSentinel"] = ["sentinalGuard1", "sentinalGuard2", "sentinalGuard0"]`.
   - Earth Form Attack (`earthForm`) and Upheaval (`lavu`) get theirs through skills_a's cast3 pool / OWN_TILE.
   - "Icons: no CLIP_SKILLS line is needed" stays true.
4. **Corrected paste-ready entries.** These replace the same keys of the block: the `#0` key becomes `@EarthFormAttack:summonAttack`, and every other key stands as written. The whole corrected block is in `checks\fx_monkey_research\verify\b_fixed.json`.

```json
{
  "summonAttack": {
    "why": "The summonAttack clip: Summon Attack (RPC_summonAttack, PlayAnimation(\"summonAttack\", 0.2) Monkey.cs:22330), Sky Crimson (RPC_skyCrimson :27439), Planet Breaker (RPC_planetBreaker :31900), Instant Blaze (RPC_instantBlaze :37613), Earth Guard (RPC_earthGuard :38068) (pipeline/clip_calls.js), one per play, even chance, picked anew on every play (one tile each, poolChains); each command needs its summon (dispatcher :7546-7575, :7778-7796, :8108-8126, :8376-8421, :8427-8470): the summon stands already summoned on the floor 2 m ahead, facing forward (getSpawnPos(hero + 2 forward), phoenix_cast / gadina_cast), Phoenix 4 or Gadina 4 (max rank), cut at 10 s (plans/fx_mole/decisions.md 32, 37); every one: voice (or none) at 0, the order to the summon at 0.3 s (Yield 0.3), standby 0.6 s (Yield 0.3); the Earth Form's three normal attacks play this clip too: their own sequence, Earth Form Attack (\"@EarthFormAttack:summonAttack#<step>\")",
    "skills": {
      "summonAttack": {
        "why": "Monkey.cs RPC_summonAttack (:21893-22432), Summon Attack (#121): target locked (:7556; the 10 m target), clip, 0.2 s fade (:22330), voice summonAttack (load :22366, PlayOneShot :22415) at 0; Yield 0.3 (:22417): Phoenix.RPC_summonAttack (:22087): hate list cleared, 1200 hate on the target, AI_setTimer(3) (Phoenix.cs:1890-1926): straight into the attack window, no select or idle (12t_reference/monkey-skill-reference.md 4.5): RPC_nAttack at once: CrossFade(\"nAttack\") (:2594) and pheonix_cry (:2612), the fireball 0.5 s in (actionTime + 0.5 :2354) from the Phoenix + (0, 2.4, 1) (Phoenix4 :2425) toward the target's bounds centre (:2461; 10 m ahead 0.6 m up: rot [14.42, 0, 0], calc.txt), RPC_fireball_fire (:2475), standby 0.3 s later (:2634): the shot at 0.8 s; Phoenix_fireBall 30 m/s (Phoenix_fireBall.cs:26) meets the target's body at (0, 0.675, 9.709) 0.231 s later as fireBall_hit (calc.txt; the part spawns it: builds); the Phoenix's later AI shots are left out (plans/fx_mole/decisions.md 32's AI rule: the command's own shot only, question 2); Yield 0.3 (:22426): standby 0.6 s (:22247); verification 2: the summon part's cries / move sounds (SOUND_REFS, named <script lower-first>_<AudioClip name>, wardrobe_fx.py:237-244): builds",
        "builds": ["phoenix_fireBall_hit", "sound:phoenix_pheonix_cry"],
        "cues": [
          [0, "voice", "summonAttack"],
          [0, "fx", "Phoenix4", {"d": 2, "single": true, "kill": 10, "ring": false, "clips": [ [ 0, "root", 0, 2 ], [ 0.3, "nAttack", 0.3, 1 ], [ 1.1, "root", 0.2, 2 ] ]}],
          [0.8, "fx", "phoenix_fireBall", {"d": 3, "y": 2.4, "rot": [ 14.42, 0, 0 ], "to": [ 0, 0.6, 10 ]}]
        ]
      },
      "skyCrimson": {
        "why": "Monkey.cs RPC_skyCrimson (:27138-27527), Sky Crimson (#224): needs Phoenix4 (:7790, :27294); clip, 0.2 s fade (:27439), voice skyCrimson (load :27475, PlayOneShot :27523) at 0; Yield 0.3 (:27517): Phoenix.RPC_skyCrimson (:27342; Phoenix.cs:3360-3994), times from its start (+0.3): CrossFade(\"skyCrimson1\", 0.2) (:3908), pheonix_cry (:3932), skyCrimson_dust at the Phoenix, its rotation (:3942) at 0.3; Yield 2 (:3971): every renderer off (:3507-3529; the colour ramp :3572 left out) at 2.3; Yield 1 (:3992): at 3.3 one skyCrimson_fire per enemy within 24 m (:3622): fireDir = (target centre - Phoenix - 20 up).normalized, firePos = target centre - 12 fireDir (:3645-3655) = (0, 11.694, 5.425), rot [67.59, 0, 0] (calc.txt), and its sound phoenix_skyCrimson (:3696); ProjectileControl life 2 (:1813-1822), Phoenix_skyCrimson_fire 16 m/s (Phoenix_skyCrimson_fire.cs:28, :53) bursting only on layer 0, the floor (:143-179: it passes the target): skyCrimson_hit, identity (Phoenix.cs:1856) at (0, 0, 10.247) 0.791 s later, 4.09 s (calc.txt; builds); Yield 2 (:3979): skyCrimson2 and the renderers back (:3723-3751) at 5.3; Yield 0.5 (:3977): skyCrimson_dust again (:3795) and a 300 HP heal at 5.8; Yield 0.5 (:3983): standby 6.3 (:3838); the Monkey: Yield 0.3 (:27521), standby 0.6 s (:27383); verification 2: the summon part's cries / move sounds (SOUND_REFS, named <script lower-first>_<AudioClip name>, wardrobe_fx.py:237-244): builds",
        "builds": ["phoenix_skyCrimson_hit", "sound:phoenix_pheonix_cry", "sound:phoenix_phoenix_skyCrimson"],
        "cues": [
          [0, "voice", "skyCrimson"],
          [0, "fx", "Phoenix4", {"d": 2, "single": true, "kill": 10, "hide": [ 2.3, 5.3 ], "ring": false, "clips": [ [ 0, "root", 0, 2 ], [ 0.3, "skyCrimson1", 0.2, 1 ], [ 5.3, "skyCrimson2", 0, 1 ], [ 6.3, "root", 0.2, 2 ] ]}],
          [0.3, "fx", "phoenix_skyCrimson_dust", {"d": 2}],
          [3.3, "fx", "phoenix_skyCrimson_fire", {"d": 5.425, "y": 11.694, "rot": [ 67.59, 0, 0 ]}],
          [5.8, "fx", "phoenix_skyCrimson_dust", {"d": 2}]
        ]
      },
      "planetBreaker": {
        "why": "Monkey.cs RPC_planetBreaker (:31599-32020), Planet Breaker (#324): needs Gadina4 (:8120, :31755); clip, 0.2 s fade (:31900), voice planetBreaker (load :31936) and planetBreaker_ring createEffect at the Monkey, identity (:31967-31977) at 0; Yield 0.3 (:32005): Gadina.RPC_planetBreaker (:31803; Gadina.cs:5403-5884), times from its start (+0.3): CrossFade(\"planetBreak\") (:5817), planetBreaker1 at the Gadina, its rotation (:5843; followPosition), gadina_cry (:5857) at 0.3; Yield 0.8 (:5883): planetBreaker2 (:5545; AlphaTimer, its own Sounds/gadina_planetBreaker) at 1.1; three pulses 0.3 s apart (i < 3 :5864, Yield :5875) at 1.4 / 1.7 / 2.0: inside 5 m nAttack_hit on a hit (:5589-5664), 5-12 m a flat hit with no effect (:5675-5698): the target 8 m from the Gadina is in the outer ring: nothing drawn; Yield 0.6 (:5870): standby 2.6 (:5735); the Monkey: Yield 0.3 (:32014), standby 0.6 s (:31844); verification 2: the summon part's cries / move sounds (SOUND_REFS, named <script lower-first>_<AudioClip name>, wardrobe_fx.py:237-244): builds",
        "builds": ["gadina_sword4", "gadina_shield4", "sound:gadina_gadina_cry"],
        "cues": [
          [0, "voice", "planetBreaker"],
          [0, "fx", "planetBreaker_ring"],
          [0, "fx", "Gadina4", {"d": 2, "single": true, "kill": 10, "ring": false, "attach": [ [ "gadina_sword4", "mount_Hand_R" ], [ "gadina_shield4", "mount_Hand_L" ] ], "clips": [ [ 0, "root", 0, 2 ], [ 0.3, "planetBreak", 0.3, 1 ], [ 2.6, "root", 0.2, 2 ] ]}],
          [0.3, "fx", "gadina_planetBreaker1", {"d": 2}],
          [1.1, "fx", "gadina_planetBreaker2", {"d": 2}]
        ]
      },
      "instantBlaze": {
        "why": "Monkey.cs RPC_instantBlaze (:37266-37651), Instant Blaze (#412): needs Phoenix4 (:8388, :37433); no voice (none loaded); clip, 0.2 s fade (:37613); Yield 0.3 (:37646): the Phoenix aimed flat at the target (:37481-37509: straight ahead), Phoenix.RPC_instantBlaze (:37516; Phoenix.cs:2685-3288), times from its start (+0.3): CrossFade(\"instantBlaze\", 0.2) (:3240), pheonix_cry (:3258) at 0.3; Yield 0.5 (:3275): the dash at moveSpeed 12 (:2826) and instantBlaze_ring at the Phoenix, its rotation, riding it (:2837; followPosition; its own Sounds/instantBlaze; the part spawns it: builds) at 0.8; four hit boxes 0.2 s apart (i < 4 :3148, Yield :3281) at 1.0 / 1.2 / 1.4 / 1.6 (burn on a hit, no effect drawn :2942-2987; the reference's 0.7-1.3 s from the Phoenix's start); moveSpeed 6 (:3156) and a 200 HP heal (:3167) at 1.6; stop (:3075) at 1.8, standby (:3096) 1.9: 9.6 + 1.2 = 10.8 m, so it ends 12.8 m ahead, through the target (collisions ignored meanwhile, :3203, :3038; calc.txt); the summon moves, the hero does not (plans/fx_chameleon/decisions.md 30); the Monkey: Yield 0.3 (:37641), standby 0.6 s (:37557); verification 2: the summon part's cries / move sounds (SOUND_REFS, named <script lower-first>_<AudioClip name>, wardrobe_fx.py:237-244): builds",
        "builds": ["phoenix_instantBlaze_ring", "sound:phoenix_pheonix_cry"],
        "cues": [
          [0, "fx", "Phoenix4", {"d": 2, "single": true, "kill": 10, "moves": [ [ 0.8, 12 ], [ 1.6, 6 ], [ 1.8, 0 ] ], "ring": false, "clips": [ [ 0, "root", 0, 2 ], [ 0.3, "instantBlaze", 0.2, 1 ], [ 1.9, "root", 0.2, 2 ] ]}]
        ]
      },
      "earthGuard": {
        "why": "Monkey.cs RPC_earthGuard (:37696-38160), Earth Guard (#413): needs Gadina4 (:8439, :37877); clip, 0.2 s fade (:38068), voice summonDefense (the code's own pick: load :38104) at 0; Yield 0.3 (:38159): +1000 hate on the target, no damage (:37958), Gadina.RPC_earthGuard (:37971; Gadina.cs:5028-5370), times from its start (+0.3): CrossFade(\"guard\") (:5313), earthGuard_ring at the Gadina, its rotation (:5331; EffectControl life 10, followPosition + followState), gadina_cry (:5343) at 0.3; Yield 0.5 (:5360), then six heals 2 s apart (i >= 6 :5261, Yield 2 :5362) at 0.8 ... 10.8 (no effect drawn), Yield 0.5 (:5367): standby 13.3 (:5209): the Gadina cut at 10 s; the ring ends by its own life at 10.3; the Monkey: Yield 0.3 (:38152), standby 0.6 s (:38012); verification 2: the summon part's cries / move sounds (SOUND_REFS, named <script lower-first>_<AudioClip name>, wardrobe_fx.py:237-244): builds",
        "builds": ["gadina_sword4", "gadina_shield4", "sound:gadina_gadina_cry"],
        "cues": [
          [0, "voice", "summonDefense"],
          [0, "fx", "Gadina4", {"d": 2, "single": true, "kill": 10, "ring": false, "attach": [ [ "gadina_sword4", "mount_Hand_R" ], [ "gadina_shield4", "mount_Hand_L" ] ], "clips": [ [ 0, "root", 0, 2 ], [ 0.3, "guard", 0.3, 1 ] ]}],
          [0.3, "fx", "gadina_earthGuard_ring", {"d": 2}]
        ]
      }
    }
  },
  "@EarthFormAttack:summonAttack": {
    "why": "Earth Form Attack, stage 1: Monkey.cs RPC_gadinaArmor_nAttack1 (:40994-41546), the normal attack in Earth Form (dispatcher :9749-9876): clip summonAttack, 0.2 s fade (:41360), voice summonAttack (load :41396, PlayOneShot :41408), Sounds/nAttack1 (:41496-41506), the worn Gadina Armor (gadinaArmor, parented to the Monkey at the Earth Form cast, :40719-40747) plays its nAttack1 (:41444-41449) and gAttack1_ring createEffect at the Monkey, his rotation (:41461-41473) at 0; Yield 0.3 (:41534): the right punch at 0.3 (FindAreaTarget(TransformDirection(0.5, 0, 1.5)), 2 m, :41145), Yield 0.3 (:41538): the left at 0.6 (:41222): gadinaArmor_hit only on a hit (:41184, :41261): the 10 m target is out of reach (plans/fx_bison/decisions.md 16); Yield 0.4 (:41544): standby 1.0 s (:41304); the armour is shown already worn (the Earth Form status chaAdjust(120) :40671: cut at 10 s; plans/fx_mole/decisions.md 37's form-already-on rule), its clips the hero's code plays: nAttack1 at 0, nAttack2 at 0.9, nAttack3 at 1.7 (the later stages' own cues), back to root when the Monkey stands by (CrossFade(\"root\", 0.2) Monkey.cs:567-587) at 2.5; verification 1: stage 1 keeps the plain sequence key (poolChains' own() sees it, so Earth Form Attack is not taken as the summonAttack pool's host); stages 2 / 3 are #1 / #2",
    "cues": [
      [0, "voice", "summonAttack"],
      [0, "sound", "nAttack1"],
      [0, "fx", "gadinaArmor", {"single": true, "kill": 10, "clips": [ [ 0, "nAttack1", 0, 1 ], [ 0.9, "nAttack2", 0, 1 ], [ 1.7, "nAttack3", 0, 1 ], [ 2.5, "root", 0.2, 2 ] ]}],
      [0, "fx", "gAttack1_ring"]
    ]
  },
  "@EarthFormAttack:summonAttack#1": {
    "why": "Earth Form Attack, stage 2: Monkey.cs RPC_gadinaArmor_nAttack2 (:41597-42089), started inside stage 1's 0.3-0.8 s window (:9774-9796) and waiting to actionTime + 0.9 (Yield :42088; actionTime is stage 1's: no stage sets it before its standby, :42017): voice sAttack1 (load :41727, PlayOneShot :41739), Sounds/nAttack2 (:41773-41785), clip summonAttack, 0.2 s fade (:41805), the armour's nAttack2 (:41836) and gAttack2_ring at the Monkey (:41853-41865) at 0 (0.9 s after stage 1); Yield 0.2 (:42075): two hits 0.2 s apart within 4 m (i < 2 :42059, Yield :42077, :41924) at 0.4 / 0.6: out of reach; Yield 0.2 (:42071): standby 0.8 s (:42012)",
    "cues": [[0, "voice", "sAttack1"], [0, "sound", "nAttack2"], [0, "fx", "gAttack2_ring"]]
  },
  "@EarthFormAttack:summonAttack#2": {
    "why": "Earth Form Attack, stage 3: Monkey.cs RPC_gadinaArmor_nAttack3 (:42131-42596), started in stage 2's window (:9817-9849), waiting to actionTime + 1.7 (Yield :42595): voice sAttack2 (load :42261, PlayOneShot :42273), Sounds/nAttack2 (:42307-42319), clip summonAttack, 0.2 s fade (:42339), the armour's nAttack3 (:42370) and gAttack3_ring at the Monkey (:42387-42399) at 0 (1.7 s after stage 1); Yield 0.4 (:42584): camera shake (:42434, left out) and one hit 3 m ahead, 3 m wide (:42453): out of reach; Yield 0.4 (:42582): standby 0.8 s (:42535)",
    "cues": [[0, "voice", "sAttack2"], [0, "sound", "nAttack2"], [0, "fx", "gAttack3_ring"]]
  },
  "summonDefense": {
    "why": "Monkey.cs RPC_summonDefense (:22485-22940), Summon Defense (#122), the only skill on this clip: needs a summon (:7589); clip, 0.2 s fade (:22847), voice summonDefense (load :22883, PlayOneShot :22936) at 0; Yield 0.3 (:22923): the order to Phoenix / Gadina / Ja (:22641-22736): the summon (Phoenix 4, standing 2 m ahead, question 1) if standing or running turns to face the Monkey (LookAt his flat position :2000: yaw 180) and cries (pheonix_cry :2009), its hate cleared and its AI set to defense (Phoenix.cs:1941-1998; the walk back by its AI is left out, question 2); Yield 0.3 (:22934): standby 0.6 s (:22794); verification 2: the cry at the turn (Phoenix.cs:2009) is the part's: a build",
    "cues": [
      [0, "voice", "summonDefense"],
      [0, "fx", "Phoenix4", {"d": 2, "single": true, "kill": 10, "turn": 0.3, "ring": false, "clips": [ [ 0, "root", 0, 2 ] ]}]
    ],
    "builds": ["sound:phoenix_pheonix_cry"]
  },
  "summonRelease": {
    "why": "The summonRelease clip: Unsummon (RPC_unsummon, PlayAnimation(\"summonRelease\", 0.2) Monkey.cs:23458), Summon Release (RPC_summonRelease :23835), Summon Soul (RPC_summonSoul :24519) (pipeline/clip_calls.js), one per play, even chance, picked anew on every play (one tile each, poolChains); each needs a summon (dispatcher :7617-7672, :8504): Phoenix 4 standing 2 m ahead (question 1), cut at 10 s",
    "skills": {
      "unsummon": {
        "why": "Monkey.cs RPC_unsummon (:22983-23545), Unsummon (#123): clip summonRelease, 0.2 s fade (:23458), voice unsummon (load :23494, PlayOneShot :23532) at 0; Yield 0.3 (:23541): half the summon's MP back (Phoenix4 35, :23202), SendMessage(\"unsummon\") (:23367): Phoenix.unsummon (Phoenix.cs:5127-5308): actionState dead, ko clip (:5264), pheonix_unsummon (:5276), destroyed 1 s later (Yield 1 :5306, Destroy :5222): end 0.3 (the Bat guardian's end option: the unsummon, gone 1 s later); Yield 0.3 (:23537): standby 0.6 s (:23405); verification 2: pheonix_unsummon (Phoenix.cs:5276) is the part's: a build",
        "cues": [
          [0, "voice", "unsummon"],
          [0, "fx", "Phoenix4", {"d": 2, "single": true, "end": 0.3, "ring": false, "clips": [ [ 0, "root", 0, 2 ] ]}]
        ],
        "builds": ["sound:phoenix_pheonix_unsummon"]
      },
      "summonRelease": {
        "why": "Monkey.cs RPC_summonRelease (:23579-23920), Summon Release (#124): clip summonRelease, 0.2 s fade (:23835), voice unsummon (the code's own pick: load :23871, PlayOneShot :23916) at 0; Yield 0.3 (:23907): Phoenix / Gadina / Ja / Gaos get SendMessage(\"summonRelease\") (:23735; Buiten and Lavu are unsummoned, :23743): Phoenix.summonRelease (Phoenix.cs:2028-2057): 1200 hate on the Monkey, isSummon off, layer 15 (a neutral enemy): nothing changes on screen; its AI then turns on the Monkey (left out, question 2); Yield 0.3 (:23911): standby 0.6 s (:23782)",
        "cues": [
          [0, "voice", "unsummon"],
          [0, "fx", "Phoenix4", {"d": 2, "single": true, "kill": 10, "ring": false, "clips": [ [ 0, "root", 0, 2 ] ]}]
        ]
      },
      "summonSoul": {
        "why": "Monkey.cs RPC_summonSoul (:23949-24632), Summon Soul (C skill): a player target (dispatcher :8490-8555): the Monkey himself (plans/fx_sheep/decisions.md 1: ally skills as self-casts); clip summonRelease, 0.2 s fade (:24519), voice summonSoul (load :24555, PlayOneShot :24600) at 0; Yield 0.4 (:24630): once per summon (isTimeOut summonSoul :24124, addTimeOut 999 :24139), summonSoul_ring createEffect at the Monkey, his rotation (:24150-24162; EffectControl 1 + 1 s, followPosition), and the summon's soul status on the target, Phoenix4: phoenixSoul 4 for 240 s (:24234) -> CharacterControl addStatus: deltaAtk(10 sLv) and phoenixSoul createEffect at mChar.bounds.center + 0.5 mChar.height up, identity (CharacterControl.cs:38149-38179): the Monkey's CharacterController centre 0.7, height 1.3 (rip Monkey.prefab:949-955) -> 1.35 m up (calc.txt; EffectControl 1 + 1 s, followPosition, its own Sounds/fireSoul); Yield 0.2 (:24608): standby 0.6 s (:24436)",
        "cues": [
          [0, "voice", "summonSoul"],
          [0, "fx", "Phoenix4", {"d": 2, "single": true, "kill": 10, "ring": false, "clips": [ [ 0, "root", 0, 2 ] ]}],
          [0.4, "fx", "summonSoul_ring"],
          [0.4, "fx", "phoenixSoul", {"y": 1.35}]
        ]
      }
    }
  }
}
```

5. **Missed: the summons' own moves.** Six Bible cards (Phoenix - Fireball, Gadina - Normal Attack, Ja - Detonate, Gaos - Fire / Rampage / Tail Spin) have no tile in any report. This report's Summon Attack shot is the Phoenix - Fireball tile's base. The decision and the follow-up research job are in skills_a's Verification item 9.
6. **Minor.**
   - **`release`:** the cue option `release` (Lavu's) is already an OPTS name, used by the Chameleon's TTO parts (Apex Hunt's prey reticle). The parts read their own fx.at, so the two do not clash. Add only the new names: `hide`, `moves`, `turn`, `ring` (from this report) and `clips`, `attach`, `lavu` (parts.md).
   - **Sentinel Guard's ring:** the ring's `cut` 6.1 equals its 6.1 s step, so fxStart cuts it at the step change (index.html:5311-5315). That is as meant.
   - **The Planet Breaker ring:** planetBreaker_ring is EC life 1, followPosition (probe), as written.

**Not re-checked here:** probe2 / probe3 / probe4 (the Rotate / Monkey_runic* / Phoenix / Gadina layouts proved in memory on the home PC: they need LAYOUTS and FIELD_PREFABS that are not in `wardrobe_fx.py` yet), the TTO twin table (Read this first 10), and calc.txt's Lavu circle.
