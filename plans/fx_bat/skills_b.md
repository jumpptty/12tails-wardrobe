# Bat effects + sounds research: cast3, channel, echoes, soulEater (skills_b)

Researcher `skills_b`, 2026-11-13 (home PC). Scope: the clips `cast3`, `channel`, `echoes`, `soulEater` and every skill
that plays them. Research only (recipe steps 1-3). Line numbers are `D:\12tails\DecompiledSource\Bat.cs` unless another
file is named. Times are seconds from the start of the clip the entry is keyed by. Distance 0 = at the hero. Max rank,
passives on (the Wolf's / Sheep's / Penguin's decisions): Auto Mass #431, Demon Bane #402, Distant Orb #403,
Chiroptophobia #423, Shadow Mastery, Shattering Dream #443, #432 (Curse level), #422 (Dissolute level).

The target is the standing 10 m target point, taken as a Penguin-sized body (CharacterController height 1, radius 0.3,
centre 0.6 m up: the 0.6 m aim rule; `bounds.center` = y 0.6, `height` = 1, `radius` = 0.3, feet = y 0).

Read-only probes and scripts, in `checks\fx_bat_research\skills_b\`:
- `clean.py` (a .cs range with the opaque `if (a - b == c)` predicates worked out: false blocks dropped, true ones
  unwrapped), `dump.py` + `clean_<RPC>.txt` (every coroutine in scope, cleaned), `mn.sh` / `key.sh` (their MoveNext).
- `probe.json` + `probe_summary.txt` (`wardrobe_fx.py bat --probe` on 44 effects), `probe2.py` + `probe2.json` (echoes
  and mirageOrb with candidate layouts patched in for that run only), `probe_fields.py` + `probe_fields.txt` (the Bat
  prefab's fields: field 7 castEffect = bat/effects/castEffect, field 9 illusion, field 10 illusion_ring).
- `cc_addStatus_bat.txt`, `cc_ticks.txt` (CharacterControl's status visuals and ticks), `echoes_sim.py` / `.txt`,
  `tto_clip_funcs.txt` (TTO functions that play these clips), `cues.py` -> `cues.json` / `cues_pretty.json` (the
  entries below, checked as JSON).

## Read this first

1. **cast3 is a pool of 19 skills; Nightmare and Mind Control are two sequences of their own.** RPC_cast1 (the shared
   channel, skills_a's) starts 21 coroutines when the bar ends (:23368-24383). 19 of them play only cast3 (0.2 s fade)
   and become `cast3.skills` members, one tile each through poolChains, with the Cast tile as host (hidden). Nightmare
   (:28741, :28640) and Mind Control (:37656, :37309) play cast3, then `channel` 0.5 s later, looped until their status
   ends. They must not be pool members: the Nightmare sequence would otherwise play a random member on its cast3 step.
   They get `@Nightmare:cast3`, `@Nightmare:channel`, `@MindControl:cast3` and `@MindControl:channel` (the Sheep's
   `@SealofAttack:cast3` shape).
2. **Page changes this needs (no cue can do them):**
   - SEQ (index.html:1152, `bat`): add `"Mind Control: cast1 cast2*@0 cast3~@0.5 channel*~@9.9"`. Mind Control has no
     tile today: its channel lasts the status's 12 s from 0.4 s; at the 10 s cut that is 9.9 s of channel.
   - Optional: Nightmare's `channel*~@9` -> `@8.9`. The status is getDebuff(9) = 9 s from 0.4 s, so the channel ends
     8.9 s in (:28600, :28876-28932).
   - SEQ_SKILL (index.html:3202): `bat: { "@Nightmare": "nightmare", "@MindControl": "mindControl" }`. Without it,
     their tiles show every skill icon whose clips include cast1 to cast3.
3. **The parts the page still needs:**
   - **Bat_echoes.** A homing orb: ProjectileControl velocity (0, 0, 4), every 0.1 s RotateTowards the target's
     bounds centre by 0.5 rad (Bat_echoes.cs:147-174), life 5 s. wardrobe_fx.py also needs
     `"Bat_echoes": [("mTarget", "r"), ("mEchoesLv", "i")]` (12 bytes; probe2.py proved it decodes).
   - **Bat_mirageOrb.** The orb's _TintColor starts at (0.5, 0.5, 0.5, 0.5) and its alpha eases to 0.05 at 5 x dt a
     frame (Bat_mirageOrb.cs:26, :222-244). Layout `[("isVisible", "b")]` (4 bytes, proved).
   - **The Shadow Illusion clones, a new cue kind `clone`.** The `illusion` prefab is a stock Bat body. Its mesh,
     material and props are swapped for the owner's at summon (Bat_illusion.cs:60-421), and its script has 80 field
     bytes with no layout. So the clone is the dressed hero copied on the page, tinted (0.3, 0.2, 0.5), in the idle
     stance, for kill seconds. `fxDue` must learn the kind: today any kind that is not fx or skin is played as a sound.
   - **BoltEmitter aimed at the cue's `to`.** nightmare_ring and mindControl_ring get `TargetCollider` = the target at
     runtime (Bat.cs:12015-12033, :13757-13775). BoltEmitter then aims at its bounds centre (BoltEmitter.cs:155-161).
     The data's TargetPosition is the prefab's world (250, 54, 150), more than 50 m off, so today the page draws
     nothing. The part: with no TargetNode and a cue `to`, aim at that hero-relative point. The inventory calls
     nightmare_ring "ready"; it is not.
   - **Light.** mindControl_ring's Point light: cyan (0.085, 0.92, 1), range 2, intensity 1 (the inventory's "needs
     Light").
   - Everything else here is built: Image / Line / Ring / Emblem / Vortex emitters, legacy particles, StaticMesh,
     Animation, AlphaTimer and ShatterMesh (shatteringDream_hit), EffectControl.
4. **Most of the look is drawn by CharacterControl, so the inventory misses it.** CharacterControl draws the status
   visuals on the target when the status is added (`addStatus`, CharacterControl.cs:40052-41320), not Bat.cs:
   phantomBane, corruption, curse, doom, nightmare, blind, confuse, charm, mindControl, shame, darkStalker,
   chiroptophobia, plus the phantomBane_hit tick (:9443-9491). All probe clean with built parts. They are placed at
   the target point by the Penguin's precedent (snowMan, a status visual, at d 10). The status tints and emoticons are
   left out, as the Penguin's multiCast tint (decision 10): charm purple, mindControl / mimic cyan, emo_heart /
   emo_panic / emo_blush.
5. **Status visuals with no EffectControl last as long as the status.** blind, confuse, charm, mindControl,
   nightmare, darkStalker and chiroptophobia are destroyed by removeStatus (CharacterControl.cs:18118-18493). They get
   `kill` = the status time, at most 10 s (decision 13). Those with an EffectControl (life 1-2) end by themselves.
6. **Auto Mass #431 on 11 members.** At the bar's end: 12 %, luck ignored, the switch at :23270-23332, at cast3 time 0.
   The members are Phantom Bane, Dissolute, Corruption, Curse, Doom, Blind, Confusion, Dream Dazzle, Phantasm Blast,
   Charm and Shame. Cue: `[0, "fx", "massCast", {"p": 0.12, "roll": "autoMass"}]`, as skills_a item 6. BB loads the
   effect's field only in RPC_massCast (:11134-11140), so the flash shows only after a Mass Cast in that session. It is
   cued anyway, as the Penguin's multiCast was.
7. **A BB bug, TTO's fix (offer it for the Bible).** RPC_confusion_cast loads `Voices/confusion1` / `confusion2`
   (:33008, :33039). The game has only `voices/confuse1` / `confuse2`, so Confusion is silent in BB. TTO loads
   `Voices/confuse1` / `confuse2` (TTO1102 `Bat.<RPC_confusion_cast>d__188::MoveNext`, pseudo/Bat.c:7358). Cue:
   `confuse1|confuse2` (Sheep decision 10).
8. **Two names to keep exactly.**
   - Shadow Illusion's second voice is `ShadowIllusion2.wav` in the rip. BB asks for `shadowIllusion2`;
     Resources.Load and Windows ignore case. The cue keeps BB's spelling, and the built file `v_shadowIllusion2.mp3`
     matches it (skills_a item 7).
   - Shattering Dream has no voice at all, in BB or TTO.
9. **TTO matches BB in this scope.** Every TTO coroutine here loads the same names and waits the same: 0.4 / 0.3 /
   0.2 / 0.1, `Waits` constants listed per function in `tto_clip_funcs.txt` and checked in this session. Two TTO-only
   skills play cast3 through `Bat::Row6BeginRelease` (pseudo/Bat.c:45398): Crimson Verdict
   (`Bat.<RPC_crimsonVerdict>d__313`, :8380) and Evil Twin (`Bat.<RPC_evilTwin>d__322`, :11929). Neither is in
   `tto_released.json` (only nightfallSwarm), so they are researched but not cued: the tto report has their parts.

## The skills, at a glance

| Skill (clip) | At 0 | At 0.4 (unless noted) | Standby | Needs |
|---|---|---|---|---|
| Phantom Bane (cast3) | voice, castEffect, Auto Mass | Sounds/phantomBane; phantomBane at target centre; phantomBane_hit tick every 2 s (APPROX phase) | 1.1 | - |
| Dissolute | voice, castEffect, Auto Mass | (status draws nothing) | 1.2 | - |
| Corruption | voice, castEffect, Auto Mass | corruption at target centre | 1.2 | - |
| Curse | voice, castEffect, Auto Mass | curse at target centre | 1.2 | - |
| Doom | voice, castEffect, Auto Mass | doom at target centre (doom_hit at 60 s: out) | 1.2 | - |
| Mirage Orb | voice, castEffect, the orb at the target's feet (Distant Orb), scale 3 | - | 0.8 | Bat_mirageOrb |
| Shadow Illusion | voice, castEffect | 2 clones + illusion_ring at (+-1.5, 0, 2.6) | 1.1 | clone kind |
| Blind | voice, castEffect, Auto Mass | blind 1 m up on target; chiroptophobia 2 m up at 0.9 (APPROX) | 1.0 | - |
| Confusion | voice confuse1/2 (TTO's fix), castEffect, Auto Mass | confuse 0.8 m up; chiroptophobia at 0.9 | 1.0 | - |
| Hate Transfer | voice, castEffect | (nothing drawn) | 1.2 | - |
| Swap | voice, castEffect | swap_hit at target and at hero | 1.2 | - |
| Dream Dazzle | voice, castEffect, Auto Mass | dreamDazzle_hit at target feet + sound | 1.2 | - |
| Phantasm Blast | voice, castEffect, Auto Mass | phantasmBlast_hit at target feet + sound | 1.2 | - |
| Charm | voice, castEffect, Auto Mass | charm_hit; charm (50 %) at target centre, scale 0.7 | 1.2 | - |
| Mimic | voice, castEffect | (the transform: left out) | 1.0 | - |
| Shame | voice, castEffect, Auto Mass | shame at target feet | 1.2 | - |
| Dark Stalker | voice, castEffect | darkStalker on the target (APPROX bone) | 1.2 | - |
| Paranoia | voice, castEffect | paranoia_hit at target feet | 1.2 | - |
| Shattering Dream | castEffect (no voice) | shatteringDream_hit + sound | 1.2 | - |
| Nightmare (cast3 > channel) | voice, castEffect | nightmare at target centre, scale 3, 9 s; channel + nightmare_ring at 0.5 | 9.4 | BoltEmitter to |
| Mind Control (cast3 > channel) | voice, castEffect | mindControl at target centre, scale 0.7; channel + mindControl_ring at 0.5 | 12.4 (cut 10.4) | BoltEmitter to, Light, SEQ |
| Echoes (echoes) | voice; echoes_ring at 0.1 | 3 homing orbs at 0.6; hits ~3.0-3.2 | 0.8 | Bat_echoes |
| Soul Eater (soulEater) | voice; soulEater_ring at 0.5 | soulEater_hit at target feet + sound at 0.7 | 1.0 | - |

The castEffect in every cast3 skill: the Bat prefab's `castEffect` field (= Resources bat/effects/castEffect,
probe_fields.txt field 7), at `position + TransformDirection(0, 1.3, 1)` with the hero's rotation: `{"d": 1, "y": 1.3}`.
It has EffectControl life 2, no followState, one ImageEmitter (Delay 0.2), and plays its own Sounds/cast_effect.

## Per clip: the timelines

Every cast3 coroutine has the same frame (worked through the opaque predicates with clean.py):
- `default` (time 0): actionState attack, myCommand = the skill, `PlayAnimation("cast3", 0.2f)` + wrapMode Once, the
  hero turned to the target, moveSpeed -0.5, the voice `Random.Range(0, 2)` (only with the pvoice setting on, and for
  others only in the same team), castEffect, then `Yield(2, 0.4)`.
- `case 2` (0.4 s): the skill's work, then `Yield(3, t)`.
- `case 3`: moveSpeed 0, then `Yield(4, 0.4)`.
- `case 4`: standby.

The per-skill lines are in each entry's `why`.

### Targeted debuffs (Phantom Bane, Dissolute, Corruption, Curse, Doom, Blind, Confusion, Shame)

- **case 2 adds the status** to the target, or with massCast on to `FindAreaTarget(target, 18, 12)`, up to 6. Status
  times use getDebuff(t, CHA, CHA) = t at equal CHA (Damage.cs:317-319). The visual comes from `addStatus`:
  - phantomBane / corruption / curse / doom: at `collider.bounds.center`, identity (:40059-40500).
  - blind: parented at up x height (:40581-40600); confuse: parented at up x (height - 0.2) (:40626-40645).
  - shame: at the feet (:40944-40953).
- **Phantom Bane's tick.** `Math.mod(2 x tickTime, 4) == 1` (CharacterControl.cs:9455) fires once in each 2 s window of
  the game clock (Math.mod floors, Math.cs:39-67; the 0.5 s tick, :8667-8676). The phase relative to the cast is not
  knowable, so the ticks are cued at their mean, 1 s after the status, then every 2 s, up to 9.4 s.
- **Corruption's tick** draws only while the target attacks (:9508-9587): left out.
- **Chiroptophobia #423** is a passive that adds effects. Every 1 s the Bat gives any enemy within 12 m holding blind
  or confuse the chiroptophobia status (Bat.cs:13166-13241). It draws a looping particle cloud at up x (height + 1)
  (:41301-41320), which goes when neither status is left, or past 13 m (:9703-9759). Cued at 0.9, the mean of the
  timer's phase (APPROXIMATED), ending with the blind / confuse (kill 9.5).

### Hits at the target (Dream Dazzle, Phantasm Blast, Shattering Dream, Paranoia, Charm, Soul Eater, Swap)

- **The hit coroutines draw at once at the target's `transform.position`** (the feet):
  - dreamDazzle_hit (:35114), phantasmBlast_hit (:36071) and shatteringDream_hit (:42560) with identity, plus
    `playAudioAtPoint` of their Sounds/... (one "sound" cue each).
  - paranoia_hit (:14611), charm_hit (:13676) and soulEater_hit (:14425) with the hero's rotation. Their own sounds
    come with the effect (paranoia, charm); Soul Eater's is played by the Bat's AudioSource (:14468).
  - The later damage ticks (3 x 0.2 s) draw nothing.
- **Charm then rolls 50 %** (`lckAdjust(20 x 2 + 10)`, :36505). The charm status's visual sits at the bounds centre,
  scale 0.7 (:40668-40677).
- **Swap** moves the Bat to the target and the target to the Bat, with a swap_hit at each (:13553-13572). On the page
  the hero stays put (no hero mover, as Feral Assault and Blink).

### Self / ground (Mirage Orb, Shadow Illusion, Hate Transfer, Mimic, Dark Stalker)

- **Mirage Orb.** Fired at time 0, in the main body, before the first Yield (:31235-31268). Distant Orb #403 (passives
  on) puts it at the locked target's feet (:9284-9301). Scale 1 + 0.5 x 4 = 3 (:12682), life 30 s.
- **Shadow Illusion.** Two clones at 0.4, from case 2 via ActionEvent (:31511-31559), at the ground spots 1.5 m
  left / right and 2.6 m ahead, facing the hero's forward (:12944). Each comes with illusion_ring (:13064) and lasts
  60 s.
- **Hate Transfer.** Ally-targeted, nothing drawn: BB never loads Effects/hateTransfer or hateTransfer_ring.
- **Mimic.** The Bat becomes a cyan-tinted copy of the target and is hidden for 72 s (:38936-39312). Left out (Open
  question 2).
- **Dark Stalker.** A static mesh that clings to a bone of the target's class (:40996-41278), cued at hip height
  (Open question 3).

### Nightmare and Mind Control (cast3 > channel)

- **At 0.4 (case 2):** moveSpeed 0 and the status.
  - nightmare: getDebuff(9), :28600-28613. Its visual is scale clamp(h + 2, 2, 6) = 3 with a looping root clip and
    a looping sound (:40368-40398).
  - mindControl: getDebuff(3 x 2 + 6) = 12, :37054-37261. Its visual is scale 0.7 (:40735-40744).
- **`Yield(3, 0.1)`, then at 0.5 (case 3):** `PlayAnimation("channel", 0.2f)` looped, and the ring at the hero with a
  BoltEmitter to the target (:28640-28654, :37309-37325).
- **Then every fixed step:** the Bat faces the target; the channel ends when the status is gone, too far (40 m) or
  dead (:28876-28932, :37424-37512). RPC_nightmare0 / RPC_mindControl0 set standby (:12060-12109, :13802-13871), and
  the rings' followState ends there.
- **Left out:** the clones' own channel (no clones), and Mind Control's camera lock.

### Echoes (echoes clip, RPC_echoes :27814-28408)

- **0:** `PlayAnimation("echoes", 0)` cut (:28211), voice echoes1|2.
- **0.1:** echoes_ring at the hero (followState).
- **0.6:** three orbs from 2 m up at yaw 0, -120 and +120 (`Math.rotateH(forward, 120 i)`; Math.cs:838-843:
  x = -sin, so i = 1 turns left). Each homes on a random enemy within 20 m: the one target.
- **0.8:** standby (the ring's cut).
- **The hits.** `echoes_sim.py` (50 Hz physics, 60 fps Update, the 0.5 rad turn every 0.1 s, the orb's 0.3 m box
  against the target's capsule) puts them at 3.02 s (middle) and 3.2 s (sides), at d 9.7, y 0.66, x 0 / -+0.05.
  These are APPROXIMATED; the Bat_echoes part's own stepping should replace them, as the Penguin's missiles were.
- **No bounce.** At rank 2 each orb would bounce to the nearest *other* enemy within 30 m (Bat_echoes.cs:369-530):
  there is none.

### Soul Eater (soulEater clip, RPC_soulEater :40562-41216)

- **0:** `PlayAnimation("soulEater", 0)` cut (:41016), voice soulEater1|2.
- **0.5:** soulEater_ring at the hero (followState).
- **0.7:** RPC_soulEater_hit: soulEater_hit at the target's feet with the hero's rotation, and Sounds/soulEater_hit.
  The player's camera colour ramp is left out, as the Wolf's camera effects were.
- **1.0:** standby (the ring's cut).

## Buildability (inventory + probe)

| Effect | Where loaded | Probe | Status |
|---|---|---|---|
| castEffect, massCast, curse, doom, phantomBane, phantomBane_hit, corruption, shame, swap_hit, dreamDazzle_hit, phantasmBlast_hit, charm_hit, paranoia_hit, soulEater_ring, soulEater_hit, echoes_ring, echoes_hit, illusion_ring, blind, confuse, charm, mindControl, nightmare, darkStalker, chiroptophobia | Bat.cs / CharacterControl.cs addStatus | clean (probe_summary.txt) | ready |
| shatteringDream_hit | Bat.cs:42548 | AlphaTimer + ShatterMesh (built) | ready |
| nightmare_ring | Bat.cs:11996 | BoltEmitter, TargetPosition far off | needs BoltEmitter `to` |
| mindControl_ring | Bat.cs:13738 | BoltEmitter + Light | needs BoltEmitter `to` + Light |
| echoes | Bat.cs:11825 | "no layout for Bat_echoes (12 field bytes)" | needs Bat_echoes (+ layout) |
| mirageOrb | Bat.cs:12669 | "no layout for Bat_mirageOrb (4 field bytes)" | needs Bat_mirageOrb (+ layout) |
| illusion (clone) | the Bat prefab's field 9 | "no layout for Bat_illusion (80 field bytes)" | page clone kind |

Sounds the cues name (`--sounds`), all in the rip's bat/sounds: phantomBane, dreamDazzle_hit, phantasmBlast_hit,
shatteringDream_hit, soulEater_hit. Every voice named is in bat/voices (checked).

## Paste-ready cues for wardrobe/fx_cues/bat.json

These merge with skills_a's `cast1` / `cast2` entries. The file is `checks\fx_bat_research\skills_b\cues_pretty.json`
(valid JSON; the same as `cues.json`).

```json
{
  "cast3": {
    "why": "Bat.cs: the cast3 clip after the RPC_cast1 channel (:22843-25102; the bar 0 s, then RPC_cast1 starts the skill's coroutine, :23368-24383): 19 Bat skills, one per play, even chance, picked anew on every play (each with its own tile, poolChains): Phantom Bane (:25610), Dissolute (:26266), Corruption (:26928), Curse (:27590), Doom (:29544), Mirage Orb (:31111), Shadow Illusion (:31672), Blind (:32334), Confusion (:32949), Hate Transfer (:33544), Swap (:34093), Dream Dazzle (:34686), Phantasm Blast (:35647), Charm (:36646), Mimic (:38400), Shame (:39840), Dark Stalker (:40376), Paranoia (:41630), Shattering Dream (:42243); Nightmare (:28741) and Mind Control (:37656) play cast3 then channel, in their own sequences (@Nightmare:cast3, @MindControl:cast3); all at max rank, passives on; every one draws castEffect 1 m ahead 1.3 m up at 0; Auto Mass #431 rolls 12 % on 11 of them (RPC_cast1 :23247-23360)",
    "skills": {
      "phantomBane": {
        "why": "Bat.cs RPC_phantomBane_cast :25103-25826 (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): clip cast3 (0.2 fade, :25610), voice phantomBane1 / phantomBane2 (Random.Range(0, 2) :25657-25716), castEffect (the Bat prefab's castEffect field = Resources bat/effects/castEffect, probe_fields.txt field 7) at TransformDirection(0, 1.3, 1), hero rotation (life 2, plays its own Sounds/cast_effect) (:25725) at 0; Auto Mass #431 (passives on): RPC_cast1 rolls Random.Range(0, 100) < lckAdjust(12) = 12 % when the bar ends, for this skill (the switch :23270-23332; not while massCast is on, :23253), draws massCast at the hero, hero rotation (createEffect :23354; Resources bat/effects/massCast :11140; life 1, followPosition, plays its own Sounds/massCast) and adds massCast Lv 1 for 3 s (:23360; its purple tint, CharacterControl.cs:40037-40047, left out as the Penguin's multiCast tint), which spreads the debuff to FindAreaTarget(target, 18, 12), up to 6 (one target point shown); Yield 0.4 (:25745): Sounds/phantomBane on the caster's own client (gameObject == Game.mPlayer, :25261-25291) and the phantomBane status, rank 4 + Demon Bane #402 (+1 level, getDebuff(12) + getDebuff(6) = 18 s at equal CHA, :25433-25489; Damage.cs:317-319): CharacterControl addStatus draws Effects/phantomBane at the target's bounds centre, identity (CharacterControl.cs:40059-40068; life 1, followPosition), and its 0.5 s status tick draws phantomBane_hit at the bounds centre once in every 2 s (Math.mod(2 x tick time, 4) == 1, CharacterControl.cs:9455-9491; Math.mod floors, Math.cs:39-67; plays its own Sounds/phantomBane_hit): APPROXIMATED to 1 s after the status and every 2 s up to the 10 s cut (the phase is the game clock's); Yield 0.3 (:25743): moveSpeed 0 at 0.7; Yield 0.4 (:25751): standby 1.1 s",
        "cues": [
          [0, "voice", "phantomBane1|phantomBane2"],
          [0, "fx", "castEffect", {"d": 1, "y": 1.3}],
          [0, "fx", "massCast", {"p": 0.12, "roll": "autoMass"}],
          [0.4, "sound", "phantomBane"],
          [0.4, "fx", "phantomBane", {"d": 10, "y": 0.6}],
          [1.4, "fx", "phantomBane_hit", {"d": 10, "y": 0.6}],
          [3.4, "fx", "phantomBane_hit", {"d": 10, "y": 0.6}],
          [5.4, "fx", "phantomBane_hit", {"d": 10, "y": 0.6}],
          [7.4, "fx", "phantomBane_hit", {"d": 10, "y": 0.6}],
          [9.4, "fx", "phantomBane_hit", {"d": 10, "y": 0.6}]
        ]
      },
      "dissolute": {
        "why": "Bat.cs RPC_dissolute_cast :25827-26488 (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): clip cast3 (0.2 fade, :26266), castEffect (the Bat prefab's castEffect field = Resources bat/effects/castEffect, probe_fields.txt field 7) at TransformDirection(0, 1.3, 1), hero rotation (life 2, plays its own Sounds/cast_effect) (:26284), voice dissolute1 / dissolute2 (:26316-26415) at 0; Auto Mass #431 (passives on): RPC_cast1 rolls Random.Range(0, 100) < lckAdjust(12) = 12 % when the bar ends, for this skill (the switch :23270-23332; not while massCast is on, :23253), draws massCast at the hero, hero rotation (createEffect :23354; Resources bat/effects/massCast :11140; life 1, followPosition, plays its own Sounds/massCast) and adds massCast Lv 1 for 3 s (:23360; its purple tint, CharacterControl.cs:40037-40047, left out as the Penguin's multiCast tint), which spreads the debuff to FindAreaTarget(target, 18, 12), up to 6 (one target point shown); Yield 0.4 (:26409): the dissolute status (:26145) removes the target's buffs and draws nothing (CharacterControl.cs:40160-40246); Yield 0.4 (:26398): moveSpeed 0; Yield 0.4 (:26413): standby 1.2 s",
        "cues": [
          [0, "voice", "dissolute1|dissolute2"],
          [0, "fx", "castEffect", {"d": 1, "y": 1.3}],
          [0, "fx", "massCast", {"p": 0.12, "roll": "autoMass"}]
        ]
      },
      "corruption": {
        "why": "Bat.cs RPC_corruption_cast :26489-27150 (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): clip cast3 (0.2 fade, :26928), castEffect (the Bat prefab's castEffect field = Resources bat/effects/castEffect, probe_fields.txt field 7) at TransformDirection(0, 1.3, 1), hero rotation (life 2, plays its own Sounds/cast_effect) (:26946), voice corruption1 / corruption2 (:26978-27065) at 0; Auto Mass #431 (passives on): RPC_cast1 rolls Random.Range(0, 100) < lckAdjust(12) = 12 % when the bar ends, for this skill (the switch :23270-23332; not while massCast is on, :23253), draws massCast at the hero, hero rotation (createEffect :23354; Resources bat/effects/massCast :11140; life 1, followPosition, plays its own Sounds/massCast) and adds massCast Lv 1 for 3 s (:23360; its purple tint, CharacterControl.cs:40037-40047, left out as the Penguin's multiCast tint), which spreads the debuff to FindAreaTarget(target, 18, 12), up to 6 (one target point shown); Yield 0.4 (:27070): the corruption status (15 s, :26778-26807): Effects/corruption at the target's bounds centre, identity (CharacterControl.cs:40113-40122; life 1); Yield 0.4 (:27063), Yield 0.4 (:27077): standby 1.2 s; left out: corruption_hit, drawn only while the target itself attacks (CharacterControl.cs:9508-9587)",
        "cues": [
          [0, "voice", "corruption1|corruption2"],
          [0, "fx", "castEffect", {"d": 1, "y": 1.3}],
          [0, "fx", "massCast", {"p": 0.12, "roll": "autoMass"}],
          [0.4, "fx", "corruption", {"d": 10, "y": 0.6}]
        ]
      },
      "curse": {
        "why": "Bat.cs RPC_curse_cast :27151-27813 (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): clip cast3 (0.2 fade, :27590), castEffect (the Bat prefab's castEffect field = Resources bat/effects/castEffect, probe_fields.txt field 7) at TransformDirection(0, 1.3, 1), hero rotation (life 2, plays its own Sounds/cast_effect) (:27608), voice curse1 / curse2 (:27640-27740) at 0; Auto Mass #431 (passives on): RPC_cast1 rolls Random.Range(0, 100) < lckAdjust(12) = 12 % when the bar ends, for this skill (the switch :23270-23332; not while massCast is on, :23253), draws massCast at the hero, hero rotation (createEffect :23354; Resources bat/effects/massCast :11140; life 1, followPosition, plays its own Sounds/massCast) and adds massCast Lv 1 for 3 s (:23360; its purple tint, CharacterControl.cs:40037-40047, left out as the Penguin's multiCast tint), which spreads the debuff to FindAreaTarget(target, 18, 12), up to 6 (one target point shown); Yield 0.4 (:27732): the curse status (rank 4, +1 with #432, 15 s, :27435-27469): Effects/curse at the target's bounds centre, identity (CharacterControl.cs:40297-40306; life 2, legacy particles, plays its own Sounds/curse); Yield 0.4 (:27734), Yield 0.4 (:27724): standby 1.2 s",
        "cues": [
          [0, "voice", "curse1|curse2"],
          [0, "fx", "castEffect", {"d": 1, "y": 1.3}],
          [0, "fx", "massCast", {"p": 0.12, "roll": "autoMass"}],
          [0.4, "fx", "curse", {"d": 10, "y": 0.6}]
        ]
      },
      "doom": {
        "why": "Bat.cs RPC_doom_cast :29105-29763 (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): clip cast3 (0.2 fade, :29544), voice doom1 / doom2 (:29591-29646), castEffect (the Bat prefab's castEffect field = Resources bat/effects/castEffect, probe_fields.txt field 7) at TransformDirection(0, 1.3, 1), hero rotation (life 2, plays its own Sounds/cast_effect) (:29659) at 0; Auto Mass #431 (passives on): RPC_cast1 rolls Random.Range(0, 100) < lckAdjust(12) = 12 % when the bar ends, for this skill (the switch :23270-23332; not while massCast is on, :23253), draws massCast at the hero, hero rotation (createEffect :23354; Resources bat/effects/massCast :11140; life 1, followPosition, plays its own Sounds/massCast) and adds massCast Lv 1 for 3 s (:23360; its purple tint, CharacterControl.cs:40037-40047, left out as the Penguin's multiCast tint), which spreads the debuff to FindAreaTarget(target, 18, 12), up to 6 (one target point shown); Yield 0.4 (:29684): the doom status (getDebuff(60), :29394-29423): Effects/doom at the target's bounds centre, identity (CharacterControl.cs:40491-40500; life 2, plays its own Sounds/doom_cast); Yield 0.4, Yield 0.4 (:29686, :29691): standby 1.2 s; left out: doom_hit when the status runs out 60 s later (CharacterControl.cs:10364-10404, :44199), past the 10 s cut",
        "cues": [
          [0, "voice", "doom1|doom2"],
          [0, "fx", "castEffect", {"d": 1, "y": 1.3}],
          [0, "fx", "massCast", {"p": 0.12, "roll": "autoMass"}],
          [0.4, "fx", "doom", {"d": 10, "y": 0.6}]
        ]
      },
      "mirageOrb": {
        "why": "Bat.cs RPC_mirageOrb_cast :30879-31356 (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): clip cast3 (0.2 fade, :31111), castEffect (the Bat prefab's castEffect field = Resources bat/effects/castEffect, probe_fields.txt field 7) at TransformDirection(0, 1.3, 1), hero rotation (life 2, plays its own Sounds/cast_effect) (:31129), voice mirageOrb1 / mirageOrb2 (:31161-31216) at 0, and at once RPC_mirageOrb_fire (:31235-31268): Distant Orb #403 on (passives on) puts the orb at the locked target's feet (rtRvLQShcf = the target's transform.position at the key press, :9284-9301; else hero + TransformDirection(0, 1, 1)), Instantiate(mirageOrb, identity), localScale 1 + 0.5 x rank 4 = 3 (:12679-12682), Bat_mirageOrb.Init(rank + 2, life chaAdjust(30) = 30 s, :12799, :31265): the orb's _TintColor starts (0.5, 0.5, 0.5, 0.5) (Bat_mirageOrb.cs:26) and its alpha eases to 0.05 at 5 x dt a frame for the caster's team (:222-244), flashing to 0.4 when an enemy touches it (:319); cut at 10 s (kill); plays its own Sounds/mirageOrb; needs the Bat_mirageOrb part; Yield 0.4 (:31304): moveSpeed 0; Yield 0.4 (:31302): standby 0.8 s",
        "cues": [
          [0, "voice", "mirageOrb1|mirageOrb2"],
          [0, "fx", "castEffect", {"d": 1, "y": 1.3}],
          [0, "fx", "mirageOrb", {"d": 10, "scale": 3, "kill": 10}]
        ]
      },
      "shadowIllusion": {
        "why": "Bat.cs RPC_shadowIllusion_cast :31357-31928 (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): clip cast3 (0.2 fade, :31672), castEffect (the Bat prefab's castEffect field = Resources bat/effects/castEffect, probe_fields.txt field 7) at TransformDirection(0, 1.3, 1), hero rotation (life 2, plays its own Sounds/cast_effect) (:31690), voice shadowIllusion1 / shadowIllusion2 (:31722-31771; the rip's file is ShadowIllusion2.wav, Resources.Load ignores case) at 0; Yield 0.4 (:31882): rank 4 = two clones, RPC_shadowIllusion_create (sent by ActionEvent, :31527, :31559) at getSpawnVector(hero + up, TransformDirection(-1.5, -1, 2.6)) and (1.5, -1, 2.6) (:31511-31546: on the ground 1.5 m left / right, 2.6 m ahead), each Instantiate(illusion, LookRotation(hero forward)) and illusion_ring there, identity (:12944, :13058-13064; plays its own Sounds/illusionSmoke): the clone copies the Bat's mesh, material, weapon, hat and trinket and is tinted (0.3, 0.2, 0.5) for its own team (Bat_illusion.cs:60-421), lives chaAdjust(60) = 60 s (:13115): cut at 10 s; the clone is a new page part, cue kind clone (a copy of the dressed hero as worn, tinted, standing in the idle stance; the illusion prefab's own body is replaced by the owner's at summon, so there is nothing for wardrobe_fx.py to build); Yield 0.3 (:31877): moveSpeed 0; Yield 0.4 (:31871): standby 1.1 s; any earlier clones vanish at 0 (RPC_disappear :31790-31845; none on a fresh play)",
        "cues": [
          [0, "voice", "shadowIllusion1|shadowIllusion2"],
          [0, "fx", "castEffect", {"d": 1, "y": 1.3}],
          [0.4, "fx", "illusion_ring", {"x": -1.5, "d": 2.6}],
          [0.4, "fx", "illusion_ring", {"x": 1.5, "d": 2.6}],
          [0.4, "clone", "illusion", {"x": -1.5, "d": 2.6, "kill": 10, "tint": [0.3, 0.2, 0.5]}],
          [0.4, "clone", "illusion", {"x": 1.5, "d": 2.6, "kill": 10, "tint": [0.3, 0.2, 0.5]}]
        ]
      },
      "blind": {
        "why": "Bat.cs RPC_blind_cast :31929-32543 (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): clip cast3 (0.2 fade, :32334), voice blind1 / blind2 (:32381-32436), castEffect (the Bat prefab's castEffect field = Resources bat/effects/castEffect, probe_fields.txt field 7) at TransformDirection(0, 1.3, 1), hero rotation (life 2, plays its own Sounds/cast_effect) (:32449) at 0; Auto Mass #431 (passives on): RPC_cast1 rolls Random.Range(0, 100) < lckAdjust(12) = 12 % when the bar ends, for this skill (the switch :23270-23332; not while massCast is on, :23253), draws massCast at the hero, hero rotation (createEffect :23354; Resources bat/effects/massCast :11140; life 1, followPosition, plays its own Sounds/massCast) and adds massCast Lv 1 for 3 s (:23360; its purple tint, CharacterControl.cs:40037-40047, left out as the Penguin's multiCast tint), which spreads the debuff to FindAreaTarget(target, 18, 12), up to 6 (one target point shown); Yield 0.4 (:32478): the blind status (rank 2, getDebuff(15), :32208-32213): Effects/blind parented to the target, localPosition up x height (1 m), no EffectControl: it stays until the status ends (CharacterControl.cs:40581-40600, removal :18192-18208; plays its own Sounds/blind): cut at 10 s; Chiroptophobia #423 (passives on): every 1 s the Bat gives each enemy within 12 m holding blind / confuse the chiroptophobia status (Bat.cs:13166-13241), drawn as Effects/chiroptophobia at up x (height + 1) = 2 m, looping (CharacterControl.cs:41301-41320; removed when blind and confuse are gone, :9703-9715; plays its own Sounds/chiroptophobia): APPROXIMATED 0.5 s after the blind (the Bat's 1 s timer's phase), ending with it; Yield 0.2 (:32472): moveSpeed 0; Yield 0.4 (:32467): standby 1.0 s",
        "cues": [
          [0, "voice", "blind1|blind2"],
          [0, "fx", "castEffect", {"d": 1, "y": 1.3}],
          [0, "fx", "massCast", {"p": 0.12, "roll": "autoMass"}],
          [0.4, "fx", "blind", {"d": 10, "y": 1, "kill": 10}],
          [0.9, "fx", "chiroptophobia", {"d": 10, "y": 2, "kill": 9.5}]
        ]
      },
      "confusion": {
        "why": "Bat.cs RPC_confusion_cast :32544-33160 (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): clip cast3 (0.2 fade, :32949), castEffect (the Bat prefab's castEffect field = Resources bat/effects/castEffect, probe_fields.txt field 7) at TransformDirection(0, 1.3, 1), hero rotation (life 2, plays its own Sounds/cast_effect) (:33064) at 0; voice: BB loads Voices/confusion1 / confusion2 (:33008, :33039), which the game has no file for (the rip: voices/confuse1, confuse2), so BB plays nothing; TTO loads Voices/confuse1 / confuse2 (TTO1102 Bat.<RPC_confusion_cast>d__188::MoveNext, pseudo/Bat.c:7358): TTO's fix (Sheep decision 10); Auto Mass #431 (passives on): RPC_cast1 rolls Random.Range(0, 100) < lckAdjust(12) = 12 % when the bar ends, for this skill (the switch :23270-23332; not while massCast is on, :23253), draws massCast at the hero, hero rotation (createEffect :23354; Resources bat/effects/massCast :11140; life 1, followPosition, plays its own Sounds/massCast) and adds massCast Lv 1 for 3 s (:23360; its purple tint, CharacterControl.cs:40037-40047, left out as the Penguin's multiCast tint), which spreads the debuff to FindAreaTarget(target, 18, 12), up to 6 (one target point shown); Yield 0.4 (:33087): the confuse status (rank 2, getDebuff(15), :32823-32828): Effects/confuse parented to the target at up x (height - 0.2) = 0.8 m, no EffectControl: until the status ends (CharacterControl.cs:40626-40645, removal :18214-18230; plays its own Sounds/confusion): cut at 10 s; Chiroptophobia #423 as Blind's (Bat.cs:13166-13241, CharacterControl.cs:41301-41320): APPROXIMATED at 0.9; Yield 0.2 (:33097): moveSpeed 0; Yield 0.4 (:33093): standby 1.0 s",
        "cues": [
          [0, "voice", "confuse1|confuse2"],
          [0, "fx", "castEffect", {"d": 1, "y": 1.3}],
          [0, "fx", "massCast", {"p": 0.12, "roll": "autoMass"}],
          [0.4, "fx", "confuse", {"d": 10, "y": 0.8, "kill": 10}],
          [0.9, "fx", "chiroptophobia", {"d": 10, "y": 2, "kill": 9.5}]
        ]
      },
      "hateTransfer": {
        "why": "Bat.cs RPC_hateTransfer_cast :33161-33756 (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): (an ally target: the Sheep's decision 1, a self-cast) clip cast3 (0.2 fade, :33544), voice hateTransfer1 / hateTransfer2 (:33591-33646), castEffect (the Bat prefab's castEffect field = Resources bat/effects/castEffect, probe_fields.txt field 7) at TransformDirection(0, 1.3, 1), hero rotation (life 2, plays its own Sounds/cast_effect) (:33659) at 0; Yield 0.4 (:33679): the monsters within 40 m of the ally hand the Bat's hate to it (:33338-33420), nothing drawn (BB's code never loads Effects/hateTransfer or hateTransfer_ring); Yield 0.4 (:33687): moveSpeed 0; Yield 0.4 (:33692): standby 1.2 s",
        "cues": [
          [0, "voice", "hateTransfer1|hateTransfer2"],
          [0, "fx", "castEffect", {"d": 1, "y": 1.3}]
        ]
      },
      "swap": {
        "why": "Bat.cs RPC_swap_cast :33757-34279 (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): clip cast3 (0.2 fade, :34093), voice swap1 / swap2 (:34140-34195), castEffect (the Bat prefab's castEffect field = Resources bat/effects/castEffect, probe_fields.txt field 7) at TransformDirection(0, 1.3, 1), hero rotation (life 2, plays its own Sounds/cast_effect) (:34208) at 0; Yield 0.4 (:34238): within 32 m (:33930-33935) RPC_swap_hit twice (:33947-33970): the Bat moved to the target's spot and the target to the Bat's, swap_hit Instantiated at each, hero rotation (:13553-13572; plays its own Sounds/swap at 0.5): at the target point and at the hero, who stays where it is on the page (the Wolf's Feral Assault: no hero mover); Yield 0.4 (:34243): moveSpeed 0; Yield 0.4 (:34236): standby 1.2 s",
        "cues": [
          [0, "voice", "swap1|swap2"],
          [0, "fx", "castEffect", {"d": 1, "y": 1.3}],
          [0.4, "fx", "swap_hit", {"d": 10}],
          [0.4, "fx", "swap_hit"]
        ]
      },
      "dreamDazzle": {
        "why": "Bat.cs RPC_dreamDazzle_cast :34280-34894 (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): clip cast3 (0.2 fade, :34686), voice dreamDazzle1 / dreamDazzle2 (:34733-34788), castEffect (the Bat prefab's castEffect field = Resources bat/effects/castEffect, probe_fields.txt field 7) at TransformDirection(0, 1.3, 1), hero rotation (life 2, plays its own Sounds/cast_effect) (:34801) at 0; Auto Mass #431 (passives on): RPC_cast1 rolls Random.Range(0, 100) < lckAdjust(12) = 12 % when the bar ends, for this skill (the switch :23270-23332; not while massCast is on, :23253), draws massCast at the hero, hero rotation (createEffect :23354; Resources bat/effects/massCast :11140; life 1, followPosition, plays its own Sounds/massCast) and adds massCast Lv 1 for 3 s (:23360; its purple tint, CharacterControl.cs:40037-40047, left out as the Penguin's multiCast tint), which spreads the debuff to FindAreaTarget(target, 18, 12), up to 6 (one target point shown); Yield 0.4 (:34825): RPC_dreamDazzle_hit (:34550): at once dreamDazzle_hit at the target's feet, identity (tChar.createEffect :35102-35114) and Sounds/dreamDazzle_hit at that point (playAudioAtPoint :35139-35157), then 3 hits 0.2 s apart that draw nothing (:35012-35046, :35201); Shattering Dream #443 adds a level only (:35172-35178); Yield 0.4 (:34833): moveSpeed 0; Yield 0.4 (:34831): standby 1.2 s",
        "cues": [
          [0, "voice", "dreamDazzle1|dreamDazzle2"],
          [0, "fx", "castEffect", {"d": 1, "y": 1.3}],
          [0, "fx", "massCast", {"p": 0.12, "roll": "autoMass"}],
          [0.4, "fx", "dreamDazzle_hit", {"d": 10}],
          [0.4, "sound", "dreamDazzle_hit"]
        ]
      },
      "phantasmBlast": {
        "why": "Bat.cs RPC_phantasmBlast_cast :35241-35852 (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): clip cast3 (0.2 fade, :35647), voice phantasmBlast1 / phantasmBlast2 (:35694-35749), castEffect (the Bat prefab's castEffect field = Resources bat/effects/castEffect, probe_fields.txt field 7) at TransformDirection(0, 1.3, 1), hero rotation (life 2, plays its own Sounds/cast_effect) (:35762) at 0; Auto Mass #431 (passives on): RPC_cast1 rolls Random.Range(0, 100) < lckAdjust(12) = 12 % when the bar ends, for this skill (the switch :23270-23332; not while massCast is on, :23253), draws massCast at the hero, hero rotation (createEffect :23354; Resources bat/effects/massCast :11140; life 1, followPosition, plays its own Sounds/massCast) and adds massCast Lv 1 for 3 s (:23360; its purple tint, CharacterControl.cs:40037-40047, left out as the Penguin's multiCast tint), which spreads the debuff to FindAreaTarget(target, 18, 12), up to 6 (one target point shown); Yield 0.4 (:35788): RPC_phantasmBlast_hit (:35511): at once phantasmBlast_hit at the target's feet, identity (:36059-36071) and Sounds/phantasmBlast_hit there (playAudioAtPoint :36096-36114), then 3 hits 0.2 s apart drawing nothing (:35969-36001, :36156); #443 adds a level only (:36129-36135); Yield 0.4 (:35783): moveSpeed 0; Yield 0.4 (:35792): standby 1.2 s",
        "cues": [
          [0, "voice", "phantasmBlast1|phantasmBlast2"],
          [0, "fx", "castEffect", {"d": 1, "y": 1.3}],
          [0, "fx", "massCast", {"p": 0.12, "roll": "autoMass"}],
          [0.4, "fx", "phantasmBlast_hit", {"d": 10}],
          [0.4, "sound", "phantasmBlast_hit"]
        ]
      },
      "charm": {
        "why": "Bat.cs RPC_charm_cast :36197-36854 (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): clip cast3 (0.2 fade, :36646), voice charm1 / charm2 (:36693-36748), castEffect (the Bat prefab's castEffect field = Resources bat/effects/castEffect, probe_fields.txt field 7) at TransformDirection(0, 1.3, 1), hero rotation (life 2, plays its own Sounds/cast_effect) (:36761) at 0; Auto Mass #431 (passives on): RPC_cast1 rolls Random.Range(0, 100) < lckAdjust(12) = 12 % when the bar ends, for this skill (the switch :23270-23332; not while massCast is on, :23253), draws massCast at the hero, hero rotation (createEffect :23354; Resources bat/effects/massCast :11140; life 1, followPosition, plays its own Sounds/massCast) and adds massCast Lv 1 for 3 s (:23360; its purple tint, CharacterControl.cs:40037-40047, left out as the Penguin's multiCast tint), which spreads the debuff to FindAreaTarget(target, 18, 12), up to 6 (one target point shown); Yield 0.4 (:36784): RPC_charm_hit: charm_hit at the target's feet, hero rotation (:13660-13676; plays its own Sounds/charm), then the roll Random.Range(0, 100) < lckAdjust(20 x 2 + 10) = 50 % (:36505; luck ignored): the charm status for getDebuff(12) = 12 s (:36511-36516): Effects/charm at the target's bounds centre, parented, localScale clamp(radius 0.3 + 0.4, 0.5, 2) = 0.7 (CharacterControl.cs:40668-40677; its RingEmitter repeats until the status ends, :18236-18249): cut at 10 s; its purple tint of the target and emo_heart left out; a failed roll shows a text only (RPC_AddDamage(-83) :36524); Yield 0.4 (:36782): moveSpeed 0; Yield 0.4 (:36788): standby 1.2 s",
        "cues": [
          [0, "voice", "charm1|charm2"],
          [0, "fx", "castEffect", {"d": 1, "y": 1.3}],
          [0, "fx", "massCast", {"p": 0.12, "roll": "autoMass"}],
          [0.4, "fx", "charm_hit", {"d": 10}],
          [0.4, "fx", "charm", {"d": 10, "y": 0.6, "scale": 0.7, "kill": 10, "p": 0.5, "roll": "charm"}]
        ]
      },
      "mimic": {
        "why": "Bat.cs RPC_mimic_cast :37867-38695 (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): clip cast3 (0.2 fade, :38400), castEffect (the Bat prefab's castEffect field = Resources bat/effects/castEffect, probe_fields.txt field 7) at TransformDirection(0, 1.3, 1), hero rotation (life 2, plays its own Sounds/cast_effect) (:38605) at 0; voice mimic1 / mimic2 (:38537-38592; allMimic1 / allMimic2 only with #373 and a clone already out, :38447-38521: none on a fresh play); Yield 0.4 (:38648): RPC_mimic_create (by ActionEvent, :38226 / :38266): a copy of the target Instantiated at the Bat's spot and rotation, tinted (0.3, 0.85, 1) by the mimic status, the Bat hidden for chaAdjust(60) + 12 s (Bat.cs:38936-39312, CharacterControl.cs:40851-40858): left out, the wardrobe has no target body to copy (Open questions); Yield 0.2 (:38627): moveSpeed 0; Yield 0.4 (:38642): standby 1.0 s",
        "cues": [
          [0, "voice", "mimic1|mimic2"],
          [0, "fx", "castEffect", {"d": 1, "y": 1.3}]
        ]
      },
      "shame": {
        "why": "Bat.cs RPC_shame_cast :39400-40060 (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): clip cast3 (0.2 fade, :39840), castEffect (the Bat prefab's castEffect field = Resources bat/effects/castEffect, probe_fields.txt field 7) at TransformDirection(0, 1.3, 1), hero rotation (life 2, plays its own Sounds/cast_effect) (:39858), voice shame1 / shame2 (:39890-39980) at 0; Auto Mass #431 (passives on): RPC_cast1 rolls Random.Range(0, 100) < lckAdjust(12) = 12 % when the bar ends, for this skill (the switch :23270-23332; not while massCast is on, :23253), draws massCast at the hero, hero rotation (createEffect :23354; Resources bat/effects/massCast :11140; life 1, followPosition, plays its own Sounds/massCast) and adds massCast Lv 1 for 3 s (:23360; its purple tint, CharacterControl.cs:40037-40047, left out as the Penguin's multiCast tint), which spreads the debuff to FindAreaTarget(target, 18, 12), up to 6 (one target point shown); Yield 0.4 (:39972): the shame status (Lv 5, getDebuff(15), :39685-39719): Effects/shame at the target's feet, identity (CharacterControl.cs:40944-40953; life 1, plays its own Sounds/shame); emo_blush on the target left out (:40941); Yield 0.4 (:39983): moveSpeed 0; Yield 0.4 (:39987): standby 1.2 s",
        "cues": [
          [0, "voice", "shame1|shame2"],
          [0, "fx", "castEffect", {"d": 1, "y": 1.3}],
          [0, "fx", "massCast", {"p": 0.12, "roll": "autoMass"}],
          [0.4, "fx", "shame", {"d": 10}]
        ]
      },
      "darkStalker": {
        "why": "Bat.cs RPC_darkStalker_cast :40061-40561 (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): clip cast3 (0.2 fade, :40376), voice darkStalker1 / darkStalker2 (:40423-40478), castEffect (the Bat prefab's castEffect field = Resources bat/effects/castEffect, probe_fields.txt field 7) at TransformDirection(0, 1.3, 1), hero rotation (life 2, plays its own Sounds/cast_effect) (:40491) at 0; Yield 0.4 (:40508): the darkStalker status, Lv 9 for 999 s (:40263): Effects/darkStalker (one static mesh, no EffectControl) Instantiated with the target's rotation and parented to a bone by the target's class (CharacterControl.cs:40996-41278; a Penguin: Hip_L, local (-0.15, -0.03, -0.07), Euler(-14, 200, 37) :41240-41256): APPROXIMATED at the target point 0.35 m up (the Penguin's hip), the target facing the hero (rot [0, 180, 0]); cut at 10 s; its tick (Effect Damage, CharacterControl.cs:9770-9794) draws nothing; Yield 0.4 (:40514): moveSpeed 0; Yield 0.4 (:40521): standby 1.2 s",
        "cues": [
          [0, "voice", "darkStalker1|darkStalker2"],
          [0, "fx", "castEffect", {"d": 1, "y": 1.3}],
          [0.4, "fx", "darkStalker", {"d": 10, "y": 0.35, "rot": [0, 180, 0], "kill": 10}]
        ]
      },
      "paranoia": {
        "why": "Bat.cs RPC_paranoia_cast :41217-41835 (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): clip cast3 (0.2 fade, :41630), voice paranoia1 / paranoia2 (:41677-41732), castEffect (the Bat prefab's castEffect field = Resources bat/effects/castEffect, probe_fields.txt field 7) at TransformDirection(0, 1.3, 1), hero rotation (life 2, plays its own Sounds/cast_effect) (:41745) at 0 (no Auto Mass roll: not in RPC_cast1's list, :23270-23332); Yield 0.4 (:41771): RPC_paranoia_hit (:41497): paranoia_hit at the target's feet, hero rotation (:14593-14611; plays its own Sounds/paranoia); Yield 0.4 (:41766): moveSpeed 0; Yield 0.4 (:41777): standby 1.2 s",
        "cues": [
          [0, "voice", "paranoia1|paranoia2"],
          [0, "fx", "castEffect", {"d": 1, "y": 1.3}],
          [0.4, "fx", "paranoia_hit", {"d": 10}]
        ]
      },
      "shatteringDream": {
        "why": "Bat.cs RPC_shatteringDream_cast :41836-42347 (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): clip cast3 (0.2 fade, :42243) and castEffect (the Bat prefab's castEffect field = Resources bat/effects/castEffect, probe_fields.txt field 7) at TransformDirection(0, 1.3, 1), hero rotation (life 2, plays its own Sounds/cast_effect) (:42261) at 0; no voice (BB loads none, the rip has none, TTO1102 Bat.<RPC_shatteringDream_cast>d__216 loads none either); no Auto Mass roll (:23270-23332); Yield 0.4 (:42290): RPC_shatteringDream_hit (:42107): at once shatteringDream_hit at the target's feet, identity (:42542-42560; AlphaTimer + ShatterMesh) and Sounds/shatteringDream_hit there (playAudioAtPoint :42585-42603), then 3 hits 0.2 s apart drawing nothing (:42453-42490, :42633); Yield 0.4 (:42288): moveSpeed 0; Yield 0.4 (:42285): standby 1.2 s",
        "cues": [
          [0, "fx", "castEffect", {"d": 1, "y": 1.3}],
          [0.4, "fx", "shatteringDream_hit", {"d": 10}],
          [0.4, "sound", "shatteringDream_hit"]
        ]
      }
    }
  },
  "@Nightmare:cast3": {
    "why": "Bat.cs RPC_nightmare_cast :28409-29104 (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): clip cast3 (0.2 fade, :28741), voice nightmare1 / nightmare2 (:28800-28855), castEffect (the prefab field, Resources bat/effects/castEffect) at TransformDirection(0, 1.3, 1), hero rotation (:28868) at 0 (no Auto Mass roll: not in RPC_cast1's list, :23270-23332); Yield 0.4 (:29046): moveSpeed 0 and the nightmare status for getDebuff(9) = 9 s (:28600-28613): Effects/nightmare at the target's bounds centre, identity, parented, localScale clamp(height 1 + 2, 2, 6) = 3 (CharacterControl.cs:40368-40398; its root clip loops, plays its own looping Sounds/nightMare; no EffectControl: destroyed when the status ends, :18118-18143): kill 9; the target's emo_panic left out (:40414); Yield 0.1 (:29041): the channel step at 0.5 (its entry)",
    "cues": [
      [0, "voice", "nightmare1|nightmare2"],
      [0, "fx", "castEffect", {"d": 1, "y": 1.3}],
      [0.4, "fx", "nightmare", {"d": 10, "y": 0.6, "scale": 3, "kill": 9}]
    ]
  },
  "@Nightmare:channel": {
    "why": "Bat.cs RPC_nightmare_cast case 3 (:28621-28694) (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): at 0.5 after cast3: clip channel (0.2 fade, looped, :28640-28645) and createNightmareRing(hero, target) (:28654): nightmare_ring at the hero, hero rotation (Bat.cs:11965-12036; EffectControl life 60, followPosition, followState, rotation mode followObject; plays its own looping Sounds/drainLife), its BoltEmitter's TargetCollider = the target's collider, so the bolts run to its bounds centre (BoltEmitter.cs:155-161): to [0, 0.6, 10]; every fixed step the Bat faces the target (:28990) and the channel lasts while the target holds nightmare (:28876-28932): the status's 9 s from 0.4 end it at 9.4 s, 8.9 s into channel, RPC_nightmare0 sets standby (:12060-12109): the ring's followState cut at 8.9",
    "cues": [
      [0, "fx", "nightmare_ring", {"to": [0, 0.6, 10], "cut": 8.9}]
    ]
  },
  "@MindControl:cast3": {
    "why": "Bat.cs RPC_mindControl_cast :36855-37866 (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): clip cast3 (0.2 fade, :37656), voice mindControl1 / mindControl2 (:37703-37758), castEffect (the prefab field) at TransformDirection(0, 1.3, 1), hero rotation (:37771) at 0 (no Auto Mass roll); Yield 0.4 (:37805): moveSpeed 0 and, for a hero-class target no higher in level (:37238-37261), the mindControl status for getDebuff(3 x 2 + 6) = 12 s (:37054): Effects/mindControl at the target's bounds centre, identity, parented, localScale clamp(0.3 + 0.4, 0.5, 2) = 0.7 (CharacterControl.cs:40735-40744; two repeating RingEmitters, no EffectControl: destroyed with the status, :18270-18323): cut at 10 s; its cyan tint of the target left out (:40750-40753); Yield 0.1 (:37796): the channel step at 0.5 (its entry)",
    "cues": [
      [0, "voice", "mindControl1|mindControl2"],
      [0, "fx", "castEffect", {"d": 1, "y": 1.3}],
      [0.4, "fx", "mindControl", {"d": 10, "y": 0.6, "scale": 0.7, "kill": 10}]
    ]
  },
  "@MindControl:channel": {
    "why": "Bat.cs RPC_mindControl_cast case 3 (:37290-37404) (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): at 0.5 after cast3: clip channel (0.2 fade, looped, :37309) and createMindControlRing(hero, target) (:37325): mindControl_ring at the hero, hero rotation (Bat.cs:13707-13778; life 60, followPosition, followState, followObject rotation; plays its own looping Sounds/drainLife; its Point light, cyan (0.08, 0.92, 1), range 2, intensity 1), its BoltEmitter's TargetCollider = the target: to [0, 0.6, 10]; the camera locks on the target (left out); the channel lasts while the target holds mindControl (:37424-37512), 12 s from 0.4: cut at 10 s from the status, 9.9 s into channel (RPC_mindControl0 :13802-13871 sets standby)",
    "cues": [
      [0, "fx", "mindControl_ring", {"to": [0, 0.6, 10], "cut": 9.9}]
    ]
  },
  "echoes": {
    "why": "Bat.cs RPC_echoes (:27814-28408; its own key, no cast bar; rank 2): clip echoes cut (PlayAnimation(echoes, 0) :28211) and voice echoes1 / echoes2 (Random.Range(0, 2) :28252-28348) at 0; Yield 0.1 (:28330): echoes_ring at the hero, hero rotation (createEffect :27961-27979; life 1 + afterLife 1, followPosition, followState; plays its own Sounds/echoe_ring); Yield 0.5 (:28336): at 0.6 three RPC_echoes_fire (:28039-28115) from 2 m up, Math.rotateH(forward, 120 i) (Math.cs:838-843: 0, -120, +120 degrees of yaw), each homing on a random enemy within 20 m (:28029-28081): the one target, 10 m ahead (rule: aim 0.6 m up); Instantiate(echoes, LookRotation(dir)), life 5 x rangeMod 1 = 5 s (:11835-11844), velocity (0, 0, 4) (the prefab's ProjectileControl, probe2.json), every 0.1 s RotateTowards the target's bounds centre by 0.5 rad (Bat_echoes.cs:147-174); needs the Bat_echoes part; on the target echoes_hit at ClosestPointOnBounds(the orb's centre), hero rotation (Bat_echoes.cs:303-324, RPC_echoes_hit :11938; plays its own Sounds/echoe_hit): checks/fx_bat_research/skills_b/echoes_sim.py: the middle orb at 3.02 s, the side ones at 3.2 s (APPROXIMATED: the Bat_echoes part's own stepping replaces these); the bounce to the nearest other enemy within 30 m (:369-530) finds none; Yield 0.2 (:28351): standby at 0.8 (:28141): echoes_ring's followState cut",
    "cues": [
      [0, "voice", "echoes1|echoes2"],
      [0.1, "fx", "echoes_ring", {"cut": 0.8}],
      [0.6, "fx", "echoes", {"y": 2, "to": [0, 0.6, 10]}],
      [0.6, "fx", "echoes", {"y": 2, "rot": [0, -120, 0], "to": [0, 0.6, 10]}],
      [0.6, "fx", "echoes", {"y": 2, "rot": [0, 120, 0], "to": [0, 0.6, 10]}],
      [3.02, "fx", "echoes_hit", {"d": 9.7, "y": 0.66}],
      [3.2, "fx", "echoes_hit", {"d": 9.7, "x": -0.05, "y": 0.66}],
      [3.2, "fx", "echoes_hit", {"d": 9.7, "x": 0.05, "y": 0.66}]
    ]
  },
  "soulEater": {
    "why": "Bat.cs RPC_soulEater (:40562-41216; its own key, no cast bar; target: the 10 m target point): clip soulEater cut (PlayAnimation(soulEater, 0) :41016) and voice soulEater1 / soulEater2 (Random.Range(0, 2) :41057-41149) at 0; Yield 0.5 (:41139): soulEater_ring at the hero, hero rotation (createEffect :40709-40727; life 1 + afterLife 1, followPosition, followState; plays its own Sounds/soulEater_ring); Yield 0.2 (:41137): at 0.7 the player's camera colour ramp shadowRamp (:40764-40775, left out: a camera effect) and RPC_soulEater_hit on the target (Auto Mass's area only with #431 and massCast on, :40828-40857): soulEater_hit at its feet, hero rotation (:14407-14425) and Sounds/soulEater_hit on the Bat's own AudioSource (:14439-14468); Yield 0.3 (:41156): standby at 1.0 (:40946): soulEater_ring's followState cut",
    "cues": [
      [0, "voice", "soulEater1|soulEater2"],
      [0.5, "fx", "soulEater_ring", {"cut": 1.0}],
      [0.7, "fx", "soulEater_hit", {"d": 10}],
      [0.7, "sound", "soulEater_hit"]
    ]
  }
}
```

## Open questions (each with my recommended answer)

1. **Mirage Orb with Distant Orb at the target's feet (d 10), or at the hero's 1 m ahead / 1 m up?** Recommend d 10.
   Passives are on and a target point exists, and the passive moves it there (:9284-9301). The orb fades to 0.05
   alpha within about a second (its stealth), so either spot shows mostly the drop and its sound.
2. **Mimic: show the transformation?** The game hides the Bat and puts a cyan copy of the target in its place for
   72 s. There is no target body to copy. Recommend leaving it out (voice + castEffect only). The alternative, hiding
   the hero and showing it tinted cyan for 10 s as if it copied another Bat, would invent a look.
3. **Dark Stalker's placement.** The mesh rides a bone chosen by the target's class (:41020-41278). Recommend the
   Penguin case (the body behind the 0.6 m rule), approximated as d 10, y 0.35, rot [0, 180, 0], kill 10. If the
   parts stage wants it exact, put the Penguin's Hip_L local offset (-0.15, -0.03, -0.07), Euler(-14, 200, 37) on a
   Penguin-sized dummy's bind pose.
4. **Phantom Bane's tick phase.** It runs on the game clock, so it is unknowable. Recommend the mean (1 s after the
   status, then every 2 s), as the Sheep's illuminate_hit. Or drop the ticks if they read as noise.
5. **Shadow Illusion clones: build the clone kind, or leave them out?** Recommend building it ("missing parts are always
   built"): a copy of the current hero (outfit, colour, face, props as worn), tinted (0.3, 0.2, 0.5), in the idle
   stance, for 10 s. The clones copy the Bat's moves in the game too, which the idle stance stands in for.
6. **Nightmare's channel length.** Recommend `@8.9` (the code's 9 s status from 0.4) over today's `@9`. It is a 0.1 s
   difference, so leaving `@9` is harmless; the ring's cue cut stays 8.9 either way.
7. **Mind Control's sequence and its cut.** Recommend adding `Mind Control: cast1 cast2*@0 cast3~@0.5 channel*~@9.9` and
   SEQ_SKILL entries for it and Nightmare. This puts the 12 s status cut at 10 s from where it lands.
8. **Status tints and emoticons** (charm purple, mindControl / mimic cyan, massCast purple; emo_heart / panic / blush).
   Recommend leaving them out, as the Penguin's decision 10.
9. **The Auto Mass flash shows in BB only after a Mass Cast that session** (skills_a's open questions 5 / 6). Recommend
   cueing it at 12 % regardless, as the Penguin's multiCast.
10. **Offer for the Bible.** Confusion is silent in BB (it loads `confusion1/2`; the files are `confuse1/2`), and TTO
    fixed it. Also: the Phantom Bane tick and Chiroptophobia timings above, if the reference lacks them. Recommend
    offering both to the user for `bat-skill-reference.md` (not written here).

## Verification

Read-only check (2026-11-13, home PC). I re-read the claims against `D:\12tails\DecompiledSource\Bat.cs`,
`CharacterControl.cs`, `Math.cs`, `Bat_echoes.cs`, the TTO pseudo-C (`pseudo/Bat.c`), the Bible
(`bat-skill-reference.md`, `assets.js`), the rip's voices / sounds, `wardrobe/data/bat/clips.json`, the page
(`wardrobe/index.html` cueOf / fxStart / fxDue / chains / poolChains / SEQ_SKILL), `pipeline/wardrobe_fx.py`,
`pipeline/wardrobe_fx_check.py` and `pipeline/wardrobe_skill_icons.py`. I worked the opaque predicates by hand where a
claim hung on them. My probes and outputs: `checks/fx_bat_research/verify_b/` (`probe_b.json`, `wardrobe_fx.py bat
--probe` on 27 of the cued effects, exit 0; `mats_b.txt` = every cued effect's materials and blends; `shader_ids_b.txt` =
their built-in shader ids; `summ.py`).

### What holds
- **The pool.** RPC_cast1 starts exactly 21 coroutines (:23386-:24352); clip_calls.js confirms cast3 at the cited lines
  for all 21, and `channel` (0.2, Loop) for Nightmare (:28640) and Mind Control (:37309). The 19 members, their cast3
  lines, castEffect lines and voice loads match. Auto Mass's switch (:23253 hasStatus, :23259 roll, :23270-:23332) holds
  exactly the 11 skills named; the flash :23354 and massCast Lv 1 for 3 s :23360. The pool shape works with the page:
  poolChains takes "Cast" as the host (no "@Cast:cast3"), while "@Nightmare:cast3" / "@MindControl:cast3" make those two
  sequences their own; member tile ids come out as "@PhantomBane" ... "@ShatteringDream"; every member has a Bible icon.
- **Step times** (Yield waits, case by case): 0.4 / 0.3 / 0.4 (Phantom Bane, Shadow Illusion: standby 1.1), 0.4 / 0.2 /
  0.4 (Blind, Confusion, Mimic: 1.0), 0.4 / 0.4 (Mirage Orb: 0.8), 0.4 / 0.4 / 0.4 for the rest (1.2). Nightmare: 0.4
  status getDebuff(9) (:28600, :28613), Yield 0.1 (:29041), channel + ring at 0.5 (:28640, :28654), the loop ends on
  `!hasStatus("nightmare")` (:28876-:28932): 8.9 s of channel. Mind Control: getDebuff(2 x 3 + 6) = 12 at rank 2
  (:37054), channel + ring at 0.5 (:37309, :37325). Echoes: ring at 0.1 (:27979, Yield :28330), three fires at 0.6
  (Yield :28336; the `while (i < 3)` loop, 2 m up, Math.rotateH(forward, 120 i): x = -sin, so i = 1 is yaw -120,
  i = 2 yaw +120, Math.cs:838-843), standby at 0.8 (Yield :28351, :28141). Soul Eater: ring 0.5 (:41139, :40727), hit
  0.7 (:41137, :40897), standby 1.0 (:41156, :40946).
- **Places:** castEffect at TransformDirection(0, 1.3, 1) with the hero's rotation (:25725 and each member's line); the
  status looks in addStatus exactly as cited (phantomBane :40068, corruption :40122, curse :40306, doom :40500 at
  bounds.center; nightmare :40377-:40398 scale clamp(h + 2, 2, 6); blind :40600 up x height; confuse :40645
  up x (height - 0.2); charm :40668-:40677 and mindControl :40735-:40744 scale clamp(r + 0.4, 0.5, 2); shame :40953 at
  the feet; darkStalker :41005-:41256, the Penguin branch Hip_L (-0.15, -0.03, -0.07), Euler(-14, 200, 37);
  chiroptophobia :41320 up x (height + 1)). The hits: dreamDazzle :35114, phantasmBlast :36071, shatteringDream :42560 at
  the feet, identity; paranoia :14611, soulEater :14425, charm :13676 at the feet, hero rotation; swap :13572 at both
  ends (:33947-:33970). Chiroptophobia: `Chiroptophobia()` (:13166-:13241), every 1 s, FindAreaTarget(Bat, 12, 5),
  status 60 s, so the 0.9 s mean phase and the end with blind / confuse hold. Phantom Bane's tick: Math.mod(2 x tick,
  4) == 1 (CharacterControl.cs:9455; Math.mod floors, Math.cs:39-67; the tick :8667), phantomBane_hit at bounds.center
  (:9491): once per 2 s window, the mean phase as cued.
- **Names:** Confusion's BB loads `Voices/confusion1` / `confusion2` (:33008, :33039), the rip has only confuse1 /
  confuse2; TTO loads `Voices/confuse1` / `confuse2` (pseudo/Bat.c:7407, :7413, in `Bat.<RPC_confusion_cast>d__188`
  from :7358). Shattering Dream loads no voice (castEffect only, :42261). Hate Transfer: no code in Bat.cs or
  CharacterControl.cs loads Effects/hateTransfer(_ring), though the rip has both prefabs, and the Bat prefab's fields
  (:19587-:19782) don't hold them. The sounds cued are the only Bat Sounds/ the code plays besides nAttack,
  demonGaze_hit / shadowGaze_hit and dreamBurst_hit. Every voice named is in the rip (ShadowIllusion2.wav as written).
- **Parts:** nightmare_ring / mindControl_ring: EC life 60, followPosition + followState, rotation mode 1, AudioSource
  drainLife (loop), a BoltEmitter (the prefab's TargetPosition / TargetObject only); mindControl_ring's Point light
  (0.0846, 0.921, 1), range 2, intensity 1. echoes and mirageOrb stop the probe with "no layout for Bat_echoes (12 field
  bytes)" / "Bat_mirageOrb (4 field bytes)": the layouts are needed before the cue file names them, or the whole bat
  build stops there (wardrobe_fx.py:294 raises).
- The paste-ready block parses as JSON (7 keys, 19 members); its cue shapes pass wardrobe_fx_check.py's file check
  except the `clone` cues (correction 2).

### Corrections
1. **Ten cued effects are not "ready": two shaders the page does not draw.** The probe passes them, but their materials
   fall back (wardrobe_fx.py:43, :227; plans/fx_bat/parts.md "Read this first" 4 and part 9):
   - the game's `Particles/MultiplyOffset` (drawn as plain alpha today, a dark smudge, not a multiply): **phantomBane**
     (Shadow1), **corruption** (corruption), **blind** (blind), **soulEater_ring** and **soulEater_hit** (corruption);
   - built-in **205** (Particles/Multiply; no entry in BUILTIN_BLEND, so drawn additive: bright where the game darkens):
     **paranoia_hit** (ShadowLine3, ShadowRay), **echoes_ring** (ShadowRay), **echoes_hit** (ShadowRay),
     **darkStalker** (darkStalker), **nightmare_ring** (nightmare_bolt).
   So "Read this first" 3's "Everything else here is built" and 4's "All probe clean with built parts" are wrong, and the
   Buildability table's first row loses these ten (corrected table below). Both shaders are part 9 of parts.md
   (MultiplyOffset, AlphaOffset, 205); no new part, but the five 205 effects here are not in parts.md's list.
2. **The `clone` cue kind needs more than fxDue.** As the page and checks stand: fxStart preloads every cue that is not
   fx / skin as a sound (index.html:4464: it would fetch `illusion.mp3`), fxDue plays it as a sound (:4519), and
   wardrobe_fx_check.py's file check rejects it: `KINDS = ("fx", "voice", "sound", "skin")` (:95) and `tint` is not in
   `OPTS` (:94), so both clone cues come out as "bad cue"; its spawn tally (:225-:226, :237-:238) counts only fx / skin.
   The clone part has to extend all four, as the `skin` kind did (e.g. tally `"clone:illusion"`). wardrobe_fx.py's
   cue_names skips unknown kinds already (:375).
3. **The tile icons for Nightmare and Mind Control need `OWN_TILE`, as the Sheep's seals did.** SEQ_SKILL alone makes
   moveSkillIcons look up `HDI.bat.nightmare` / `.mindControl`, which `wardrobe_skill_icons.py` never writes (no clip is
   named like them, and they are not pool members), so the page falls back to the last of the game's own icons by
   numeric sort (`nightmare4`, `mindcontrol4` in ui.json, not the Bible's top-rank `bat_nightmare2` / `bat_mindControl2`
   upscales). Add `"bat": {"nightmare": ["cast3", "channel"], "mindControl": ["cast3", "channel"]}` to `OWN_TILE`
   (wardrobe_skill_icons.py:41) and rerun it.
4. **SEQ / SEQ_SKILL must be merged with effect_only.md's.** Both reports add to the same `bat:` SEQ line and the same
   `bat:` SEQ_SKILL key; the merged blocks are in effect_only.md's Verification (they include this report's Mind
   Control line, Nightmare `@8.9` and both SEQ_SKILL entries). Line numbers: SEQ is index.html:1151-1152, SEQ_SKILL
   :3208 (not :3202).
5. **Small:** mindControl_ring's light is (0.085, 0.92, 1) as the parts summary says (the `why` of
   "@MindControl:channel" writes 0.08); Mirage Orb's "DistantOrb" banner (:31253, a UI text) is left out like the other
   banners (say so in the why); the Swap entry's frame (one hit at the hero, one at the target point) is the one
   effect_only.md's Switch now follows (its correction 5).

No time, name, random pick, rank or position in the cue lists is wrong; the cues stay as written, apart from the `why`
text below.

### Corrected paste-ready blocks

Buildability (replaces the table's rows 1 and 2; the rest stands):

| Effect | Where loaded | Probe | Status |
|---|---|---|---|
| castEffect, massCast, curse, doom, phantomBane_hit, shame, swap_hit, dreamDazzle_hit, phantasmBlast_hit, charm_hit, illusion_ring, confuse, charm, mindControl, nightmare, chiroptophobia | Bat.cs / CharacterControl.cs addStatus | clean, built shaders | ready |
| shatteringDream_hit | Bat.cs:42548 | AlphaTimer + ShatterMesh (built) | ready |
| phantomBane, corruption, blind, soulEater_ring, soulEater_hit | CharacterControl.cs addStatus / Bat.cs | clean; a `shader:Particles/MultiplyOffset` material | needs the MultiplyOffset shader (parts.md part 9) |
| paranoia_hit, echoes_ring, echoes_hit, darkStalker | Bat.cs / CharacterControl.cs addStatus | clean; built-in 205 materials | needs 205 = multiply (parts.md part 9) |
| nightmare_ring | Bat.cs:11996 | BoltEmitter (prefab target far off); nightmare_bolt is 205 | needs BoltEmitter `to` + 205 |

`pipeline/wardrobe_skill_icons.py` OWN_TILE (line 41):
```python
OWN_TILE = {"sheep": {"sealOfAttack": ["cast3"], "sealOfDefense": ["cast3"], "edenSanctuary": ["cast3"]},
            "bat": {"nightmare": ["cast3", "channel"], "mindControl": ["cast3", "channel"]}}
```
`"@MindControl:channel"`'s `why`, the light's colour (cues unchanged):
```json
  "@MindControl:channel": {
    "why": "Bat.cs RPC_mindControl_cast case 3 (:37290-37404) (target: the 10 m target point, a Penguin-sized body: bounds centre 0.6 m up, CharacterController height 1, radius 0.3): at 0.5 after cast3: clip channel (0.2 fade, looped, :37309) and createMindControlRing(hero, target) (:37325): mindControl_ring at the hero, hero rotation (Bat.cs:13707-13778; life 60, followPosition, followState, followObject rotation; plays its own looping Sounds/drainLife; its Point light, cyan (0.085, 0.92, 1), range 2, intensity 1), its BoltEmitter's TargetCollider = the target: to [0, 0.6, 10]; the camera locks on the target (left out); the channel lasts while the target holds mindControl (:37424-37512), 12 s from 0.4: cut at 10 s from the status, 9.9 s into channel (RPC_mindControl0 :13802-13871 sets standby)",
    "cues": [
      [0, "fx", "mindControl_ring", {"to": [0, 0.6, 10], "cut": 9.9}]
    ]
  },
```
In `"mirageOrb"`'s `why`, after "puts the orb at the locked target's feet (... :9284-9301 ...)", add: "its 'DistantOrb'
banner (:31253) left out".
