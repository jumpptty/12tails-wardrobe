# Rabbit effects + sounds research: Normal Attack (nAttack, Combo and its passives), Charge Attack (cAttack1-3), emotes, basic moves, KO

Short summary: The Rabbit's Normal Attack is one clip, `nAttack`, and one shot at 0.3 s. With the passives on it is the
**Bouncing Bullet** shot. Aimed at the no-target 10 m ground point, the tracer meets the floor 11 m ahead, sparks there
(`bouncingBullet_hit`) and bounces up as a second tracer 0.02 s later. The hit on a target at the target point plays the
Hyper Shot voice `nAttack2`. Snipe Mastery's own hit effect draws nothing: its prefab is in neither BB's data nor TTO's.
With a shotgun worn, Customized Shotgun replaces the shot with a voiceless blast (`shotgun_fire` + `shotgun_hit`). That
needs a `worn` / `notWorn` set (one new `ITEM_SETS` line) and gets a tile of its own.

The Charge Attack is the sniper shot: cAttack1 for 1.0 s (the `cAttack_charge` glow and voice), then cAttack2 looped
with the scope. The scope's own AudioSource plays `deadShot` when the crosshair settles on a head. The release goes
into cAttack3 with `cAttack_fire`, `cAttack_hit` on the target's head and the voice `headShot`. Proposed sequence:
`"Charge Attack: cAttack1@1 cAttack2*@4 cAttack3"`.

From the Above (a passive) fires the normal attack from 12 m up during Bounce's air phase. It plays no clip of its own,
so it gets its own tile on the Bounce sequence; the Bounce report sets that sequence's shape. The emotes are the usual
`RPC_emotion` voices; the Rabbit has `bow` and `beg` voices. KO is the Wolf's entry. There are no footsteps or other
AnimationEvents. 25 + 1 entries, 50 cues. The page needs one `ITEM_SETS` line and its SEQ / SEQ_SKILL lines; every cued
effect and sound is ready.

=====================================================================

**Scope.**
- The clip `nAttack`: the dispatcher `doNormalAttack`, `RPC_nAttack` (Combo #101-104, Hyper Shot #131-134, Bouncing
  Bullet #401, Snipe Mastery #431), `RPC_shotgun` (Customized Shotgun #353 / #354) and `RPC_fromTheAbove` (From the
  Above #421, the normal attack during Bounce).
- `cAttack1`, `cAttack2`, `cAttack3`: `doBeginCharge`, `RPC_cAttack1`, `doReleaseCharge`, `RPC_cAttack2` (Dead Shot #411)
  and `RPC_cAttack0` (the cancel).
- MP / SP transfer style skills on an attack clip: the Rabbit has none.
- `RPC_emotion`, the basic moves, `RPC_activateIcon1`, `RPC_ko`, `RPC_dead`, `RPC_revive` and the run's footsteps.

**Method.**
- Research only (recipe steps 1-3), office PC, 2026-11-13.
- Line numbers are `C:\Users\Jump\Desktop\12tails\DecompiledSource\Rabbit.cs` (the home PC's `D:\12tails\...`) unless
  another file is named.
- Times are seconds from the start of the clip that keys the cue. Distance 0 means at the hero.
- Every opaque predicate on these paths was evaluated by script: `pred.py` tags each `if (a - b op c)` T / F, and
  `flat.py` drops the false branches. I also read them by hand, including the compound ones at :18840 / :18845. Each
  one goes the normal way.
- The fixed step is 0.02 s and the frame-loop timers use their nominal intervals (Mole decision 45).

**Files** (all in `checks\fx_rabbit_research\attacks_emotes\`, git-ignored):
- `RPC_*.txt`: the `clip_flow.js` dumps. `*_flat.txt`: the coroutines with the predicates evaluated (nAttack, shotgun,
  cAttack1, cAttack2, emotion). `pred.py` and `flat.py` are the predicate tools.
- `clip_calls.txt`: `node pipeline/clip_calls.js <DecompiledSource> wardrobe/data rabbit`.
- `probe.txt` / `probe_summary.txt` (`summ.py`): `wardrobe_fx.py rabbit --probe nAttack_fire,nAttack_hit,snipeShot_hit,`
  `bouncingBullet,bouncingBullet_hit,shotgun_fire,shotgun_hit,cAttack_charge,cAttack_fire,cAttack_hit,sniperCamera,deadEffect`
  (read only).
  - snipeShot_hit: `KeyError`, not in the container.
  - sniperCamera: no layout for Rabbit_sniperCamera.
- `probe_tto.txt` / `probe_tto_err.txt`: `wardrobe_fx_tto.py rabbit --probe snipeShot_hit,...`, which gives "not in
  TTO's catalog ... ['snipeShot_hit']".
- `container.py` / `container.txt`: BB's Resources keys under heroes/rabbit (effects, voices, sounds) and the rip's
  Rabbit voices (170 files) and sounds (82 files).
- `probe_events.py` / `probe_events.txt`: all 52 BB Rabbit clips read, **0 AnimationEvents**.
- `probe_snipercam.py` / `probe_snipercam.txt`: the sniperCamera prefab has a Transform, Rabbit_sniperCamera and an
  AudioSource (`deadShot`, playOnAwake off, loop off). It has **no renderer**.
- `geom.py` / `geom.txt`: the shot geometry.
- `cues.json` (the 25 entries below) and `cues_fromTheAbove.json` (the From the Above block).
- `parse_blocks.py`: both blocks parse against wardrobe_fx_check.py's KINDS / OPTS and the Rabbit's clips, with every
  time list in order, 0 problems.

**TTO.** `DecompiledSource_TTO_2026-11-02\pseudo\Rabbit.c` (TTO1102) has the same coroutines with the same strings:
- `<RPC_nAttack>d__168` :17334 (nAttack1 / nAttack2 / bouncingBullet voices, sounds/nAttack, nAttack_fire, bouncingBullet,
  bouncingBullet_hit, RPC_snipeShot_hit, w_rab59);
- `<RPC_shotgun>d__229` :20992-21569 (shotgun_fire, RPC_shotgun_hit, no voice);
- `<RPC_cAttack1>d__170` :3851 (cAttack_charge, sniperCamera, voices/cAttack);
- `<RPC_cAttack2>d__171` :4360 (cAttack_fire, headShot / hyperShot, Dead Shot!);
- `<RPC_cAttack0>d__172` :3691;
- `<RPC_fromTheAbove>d__180` :9238.

`Rabbit::isShotgun` (:36197) has BB's 12 codes. Its waits are opaque, so the BB times stand. Emotes and KO moved to
BaseHero (BaseHero.c :1937-1976 names the TTO emotes). None of the TTO skills (bountyHunt, coinRicochet, medicTurret)
touches these clips. clap and wai are released, but TTO-only emote clips stay silent (Cat decision 16).

---
## Read this first

**1. The Normal Attack is one clip and one shot.** The passives make that shot the Bouncing Bullet ricochet.
- `doNormalAttack` starts `RPC_nAttack` (:9078), or `RPC_shotgun` with Customized Shotgun and a shotgun (item 3). Combo
  ranks only lengthen the ray (16 / 20 + 5 × Combo); there are no stages.
- At 0: `Rewind` + `animation.Play("nAttack")` (a cut, :17849-17854) and the voice nAttack1.
- At 0.3 s, only in a mission / arena (`mGameType <= 4` skips the whole shot, :17451): with Bouncing Bullet #401 the
  code plays `Sounds/nAttack` itself (:17471-17483) and runs the ricochet loop IL_F77 (:18075-18378), not the plain
  `nAttack_fire` + raycast.
- Each segment is a `bouncingBullet` tracer (:18097-18109) plus a `Physics.Raycast` on **layer 1 = Default** (:17497,
  :18123). The ground is on Default: Math.cs's ground finder casts down with `layerMask = 1` (:1102-1105).
- The aim is the no-target 10 m ground point (GameGui.cs:1659; Penguin decision 1, Bat 1, Chameleon 22, Mole Q1). The
  ray starts at hero + up + forward (:17389) and points along tDir - up (:17394). It therefore meets the floor at
  **(0, 0, 11)**, 1 m past the target point (geom.txt).
- There: `bouncingBullet_hit` (:18135-18147). The reflection, one fixed step later (0.32 s), is a second tracer from
  (0, 0, 11) pitched 5.711° up (:18365-18375). Nothing above it to hit, so the loop ends (bounceCount = 9, :18179).
- Proposed: `"Normal Attack: nAttack"` as a one-step SEQ. A clip a visible sequence plays leaves the ท่าสกิล list
  (Chameleon decision, NOTES 2026-11-13), and Customized Shotgun's tile plays nAttack too. The cue key stays the plain
  `nAttack`. The first step keeps the page's fade (Bat decision 28).

**2. Snipe Mastery's hit effect does not exist, and the Hyper Shot voice needs a hit.**
- Each segment's `RaycastAll` over the hero layers (:18197) hits every target on it. With Snipe Mastery the hit effect
  is `RPC_snipeShot_hit` (:18265-18271, :11435-11467), which loads `Effects/snipeShot_hit`.
- That prefab is in neither BB's container (container.txt) nor TTO's catalog (probe_tto_err.txt): "Cannot find
  snipeShot_hit Effect", and nothing is drawn. So with the passives on, a Normal Attack hit draws no hit spark in either
  game.
- What a hit on the target at the target point does show: segment 1 crosses the standard body (Bat decision 4) at
  (0, 0.13, 9.7), 8.74 m out (inside bounceMagnitude 10).
  - That hit's Hyper Shot (4 × the raw 9.7 m with Snipe Mastery, :18230-18253) sets isHyperShot (:18319-18325).
  - bounceCount is 1 there, so it is not a "bounce" (:18331).
  - After the loop (0.34 s) comes the voice **nAttack2** (:18006-18061, :18395), the Chameleon 22 precedent of an enemy
    hit at the target point (Question 1).

**3. Customized Shotgun swaps the shot when a shotgun is worn (a set and a tile).**
- `getCustomizedShotgunLv()` is above 0 only with `isShotgun()` (:11098). isShotgun is a fixed list: w_rab22, 24, 32, 34,
  39, 47, 48, 50, 51, 52, 55, 69 (:11136-11256; TTO the same, Rabbit.c:36197).
- Through data/item_map.json these are traderGun, traderGunR, merchantGun, merchantGunR, flowerGun, antShotgun,
  antShotgunR, royalGun (w_rab50 and w_rab51), royalGunR and timeShotgun. w_rab55 has no item.
- Not shotguns, whatever their names: mummyShotgun (w_rab46), championGun (w_rab58), pvpBow (w_rab43 / 44) and specialGun
  (w_rab59).
- RPC_shotgun (:36172-36527) has **no voice at all**. Its look: `shotgun_fire` at (0, 1, 1), and `shotgun_hit` at each
  target's position + up = (0, 1, 10).
- The cues use `worn` / `notWorn ["R", "rabbitShotgun"]`, a new ITEM_SETS entry (the Bison's bisonHammer precedent,
  decision 25). Rabbit weapons mount on mount_Hand_R, which is slot R.
- Customized Shotgun gets its own tile, `"Customized Shotgun: nAttack"` (key `@CustomizedShotgun:nAttack`), with the
  shotgun shot whatever is worn (Question 2).

**4. The Charge Attack's sequence times.** Today the page has `"Charge Attack: cAttack1 cAttack2* cAttack3"`.
- cAttack1 → cAttack2 at **1.0 s**: Yield(2, 1) :19032, then `PlayAnimation("cAttack2", 0)` :18636, a cut. The 1.6 s clip
  is cut there.
- cAttack2 is the scope (looped, :18641), held until the player lets go. Full charge is Dead Shot's ×3 at 4 s on a head
  (`1 + 0.5 × clamp(t, 0, 4)`, :19486; the scope's bar fills over 4 s, Rabbit_sniperCamera.cs:500). The timer starts with
  the scope at 1.0 s, so the hold is **4 s** and the release comes at 5.0 s.
- cAttack3 cuts in (`PlayAnimation("cAttack3", 0)` :19318), with standby at 0.7 s.
- Proposed: **`"Charge Attack: cAttack1@1 cAttack2*@4 cAttack3"`** (Question 3).
- A release before 1.0 s, or outside a mission / arena, is the cancel RPC_cAttack0 (no sniperCamera yet, :9297-9303):
  CrossFade to root and nothing drawn, so no tile (Chameleon decision 18).

**5. Sounds the hero's code plays (`"sound"` cues).** No effect carries these:
- `Sounds/nAttack` on the Bouncing Bullet shot (:17471-17483). The bouncingBullet prefab has no AudioSource, while the
  plain path's nAttack_fire carries its own.
- `sounds/deadShot` (Question 7). It is the sniperCamera's AudioSource (`audio.Play()`, Rabbit_sniperCamera.cs:375-393).
  It plays once, the first time the scope's 0.1 s check (:308-314) finds the crosshair on a head zone more than 0.1 s
  and less than 1 s after the Dead Shot timer started (:357-393). That is 0.1 s into cAttack2.

Effects that bring their own sound (probe_summary.txt): cAttack_charge (cAttack1), cAttack_fire (nAttack), shotgun_fire
(shotgun), nAttack_fire (nAttack). Both rip WAVs are in `heroes/rabbit/sounds/`.

**6. The sniperCamera draws nothing in the world.**
- The prefab has no renderer (probe_snipercam.txt). Its script draws the crosshair, the distance label, the Dead Shot
  picture and its bar in OnGUI (Rabbit_sniperCamera.cs:246-510): screen UI, own player only.
- The rest is camera work: specialTarget, FOV 60 and mouse aiming (Rabbit.cs:18698-18816), left out as camera effects
  (Cat decision 43, Chameleon 52).
- So the inventory's "needs Rabbit_sniperCamera" needs no part. Its one world output, the deadShot sound, is a sound cue
  (Question 7).

**7. From the Above is a normal attack from the sky during Bounce. It plays no clip, so its tile rides the Bounce sequence.**
- `doNormalAttack` lets the attack key fire while attack / bounce, more than 1 s after Bounce started, with the nAttack
  timeout free (:8944-8997).
- RPC_fromTheAbove (:22067-22274) plays no clip, voice or sound of its own. After 0.1 s it fires `nAttack_fire` from
  12 m above the hero toward the target (pitch 50.194°). Its ray (36 m) puts `nAttack_hit` at the target point.
- The 1.5 s nAttack timeout allows a shot at 1.1, 2.6, 4.1, 5.6, 7.1 and 8.6 s before the landing at 8.9 s (Bounce 2:
  `4 × sLv` = 8 s from 0.9, :21068-21073).
- The Bounce tile belongs to the skills report. Proposed: a tile `"From the Above: <the Bounce report's steps>"` (key
  `@FromtheAbove:bounce1`, its cues the Bounce entry's plus the block below). The landing stomp with #421
  (fromTheAbove_ring, RPC_bounce0) is Bounce's (Question 4).

**8. Emote voices** (container.txt, rip_audio in container.txt).
- The Rabbit has hi, wave, ty, **bow**, laugh, sleep, cheer, **beg**, cry, battle, pose and chat1-3.
- It has no sit, talk or dance voice.
- emo_chat picks chat1-3 (`Random.Range(1, 4)`, :42683).
- The bow tile takes `ty|bow`, as wave takes `hi|wave`.

**9. KO is the Wolf's entry.**
- ko1 / ko2 for RPC_ko; dead1 / dead2 and deadEffect for RPC_dead, with deadEffect spawned before the voice gate
  (:48806-48818).
- RPC_revive plays getUp and loads **no** voice (:48973-49223), although the rip has voices/revive. getUp is silent.

**10. No footsteps or other basic-move sounds.**
- No AnimationEvent on any of the 52 BB Rabbit clips (probe_events.txt).
- No footstep or other event handler in Rabbit.cs (no `footStep` / `play*Event`).
- So run, root, falling, getUp and battle (the basic move) get no cues; battle has its emote voice (item 8).

**11. No MP / SP transfer style skill plays an attack clip.** clip_calls.txt: nAttack is played only by RPC_nAttack
(:17854) and RPC_shotgun (:36492). cAttack1-3 are played only by RPC_cAttack1 / RPC_cAttack2 (:18921, :18636, :19318).

**12. Mission-only gates are kept**, following the Sheep / Penguin / Mole precedent.
- Gated: the whole Normal Attack shot (:17451), Customized Shotgun (:9051), the cAttack voice (for the own hero too,
  :18939) and the sniper release (:9297).
- Not gated: cAttack_charge, the emotes, KO.

---
## The dispatcher: doNormalAttack (:8876-9100)

- Aim: `vector = targetArray[0] - position` (:8917). GameGui passes the target's `collider.bounds.center`, or with no
  target `position + 10 forward` (GameGui.cs:1626, :1659).
- A target object within 2 m flat (`sqrMagnitude < 4`) gets `3 flat(dir) + up` instead (:9023-9034). It does not matter
  at 10 m.
- From standby or run, with the `nAttack` timeout free (:8929-9005):
  - `getCustomizedShotgunLv() > 0` and a mission / arena (:9042-9057) → RPC_shotgun;
  - else RPC_nAttack (:9078).
- In attack / bounce with #421, more than 1 s after the Bounce, timeout free: RPC_fromTheAbove (:8944-8997).

## nAttack (RPC_nAttack, $RPC_nAttack$26825, :17359-18403), passives on

| t (s) | what happens | lines |
|---|---|---|
| 0 | attack, actionTime, myCommand nAttack, timeout 1.5 (1.0 with w_rab59 specialGun), LookAt, moveSpeed 0 | :17794-17844, :17809-17823 |
| 0 | Rewind, animation.Play(nAttack), Once (a cut) | :17849-17859 |
| 0 | voice nAttack1 (pvoice; own hero, else a mission teammate) | :17864-17901, :18399 |
| 0.3 | still attacking (:17374): moveSpeed -3 (the recoil step) | :17384 |
| 0.3 | firePos (0, 1, 1), fireDir (0, -1, 10) | :17389-17399 |
| 0.3 | town: skip the shot entirely | :17451 |
| 0.3 | #401: Sounds/nAttack; bounceRange 20 + 5 × 4 = 40 | :17459-17527 |
| 0.3 | segment 1: bouncingBullet at (0, 1, 1) rot [5.711, 0, 0]; floor at (0, 0, 11); bouncingBullet_hit there (hero rotation); bounceMagnitude 10, range 30 | :18091-18171 |
| 0.3 | RaycastAll 10 m: the target body at (0, 0.13, 9.7); snipeShot_hit (missing prefab); Hyper Shot set | :18185-18345 |
| 0.32 | segment 2 (range 30 > 12): bouncingBullet at (0, 0, 11) rot [-5.711, 0, 0]; no wall: bounceCount 9 | :18076-18179, :18393 |
| 0.34 | loop done (bounceCount ≥ 3, :18378): HyperShot message, voice nAttack2 | :17924-18061, :18395 |
| 0.49 | moveSpeed 0 | Yield(4, 0.15) :18389, :17722 |
| 0.83 | standby | Yield(5, 0.34) :18391, :17729-17752 |

Without #401 (not shown, passives on): `nAttack_fire` at firePos with LookRotation(fireDir) (:17531-17549), then the own
client's ray of 16 + 5 × 4 = 36 m on every layer but its own and 1 / 2 (:17571-17586). That ray puts nAttack_hit, or
with #431 the missing snipeShot_hit, at the hit point (:17594-17631).

**Hits on an enemy.** `onNormalAttackHit` (:49223-) rolls the weapon's gear procs: happy, charm, clear, heal1, ... by
LCK. They are left out (Chameleon decision 53, Monkey 52).

## Customized Shotgun (RPC_shotgun, $RPC_shotgun$27317, :36172-36527)

| t (s) | what happens | lines |
|---|---|---|
| 0 | attack, myCommand nAttack, timeout 1.5, LookAt; animation.Play(nAttack), Once (no Rewind); **no voice** | :36474-36504 |
| 0.3 | moveSpeed -3 | :36200 |
| 0.3 | shotgun_fire at position + TD(0, 1, 1), hero rotation (own sound "shotgun") | :36205-36223 |
| 0.3 | FindRecTarget from position + forward, 12 m long, half-width 1.5 → 4 m, 4 m high (sLv 2) | :36270 |
| 0.3 | per target: RPC_shotgun_hit at the target's position + up, hero rotation, even when the hit fails | :36354; :11044-11067 |
| 0.45 | moveSpeed 0 | :36518, :36403 |
| 0.79 | standby | :36520, :36409-36432 |

## Charge Attack: cAttack1, cAttack2 (the scope), cAttack3 (the release)

**doBeginCharge** (:9155-9250): from standby / run, #111 learned, 0.1 s after the last action, no scope yet → RPC_cAttack1
(:9225).

**RPC_cAttack1** ($RPC_cAttack1$26855, :18604-19034):

| t (s) | what happens | lines |
|---|---|---|
| 0 | attack, actionTime, myCommand cAttack1, LookAt, PlayAnimation(cAttack1, 0), Once, moveSpeed 0 | IL_B64 :18905-18930 |
| 0 | voice cAttack (pvoice, mission / arena for everyone, same team) | :18933-18969 |
| 0 | cAttack_charge at the hero (life 2, followPosition / followState, own sound cAttack1, a star after 0.7 s) | :18982-18998 |
| 1.0 | still attack / cAttack1: PlayAnimation(cAttack2, 0), Loop | Yield(2, 1) :19032; :18617-18641 |
| 1.0 | own player: sniperCamera at hero + TD(0, 1.05, 0.15), camera specialTarget, FOV 60 | :18646-18725 |
| 1.0- | each frame: the scope turned by the mouse (±30° / ±60°) | case 3, :18741-18863, YieldDefault(3) :19028 |
| 1.1 | the scope's OnGUI: head zone on the 0.1 s check after the timer started → deadShot plays once | Rabbit_sniperCamera.cs:308-393 |

**doReleaseCharge** (:9254-9353), while attack / cAttack1:
- in a mission / arena with the scope alive → RPC_cAttack2 along the scope's flat forward (:9297-9309);
- else RPC_cAttack0 (:9330).

**RPC_cAttack2** ($RPC_cAttack2$26869, :19187-19785), the release at 5.0 s (the cAttack3 step):

| t (s) | what happens | lines |
|---|---|---|
| 0 | attack, myCommand cAttack2, actionTime, LookAt, PlayAnimation(cAttack3, 0), Once, moveSpeed -2 | :19300-19327 |
| 0 | cAttack_fire at position + up, LookRotation(the scope's forward) = the hero's (own sound "nAttack") | :19330-19366 |
| 0 | own client: ray from the scope along its forward, 20 + 5 × 4 = 40 m; RPC_cAttack_hit at the hit point, LookRotation(hero forward) | :19380-19398; :9378-9401 |
| 0 | head zone (:19434); Dead Shot ×3 (:19445-19486); "Dead Shot!" (GUI); voice headShot | :19529-19587 |
| 0.2 | moveSpeed 0; the scope destroyed | Yield(2, 0.2) :19781; :19200-19254 |
| 0.7 | standby | Yield(3, 0.5) :19779; :19257-19275 |

The ray is level at y 1.05 (no mouse), so it meets the target body (cylinder r 0.3, y 0.1-1.1) at (0, 1.05, 9.7), in
the head zone (1.05 - 0.6 = 0.45 > 0.5 × 0.5). That is the head shot whose voice is cued (geom.txt). Hyper Shot's
`hyperShot` voice needs a hit beyond 16 m and is not reached (:19498-19513, :19671).

**RPC_cAttack0** ($RPC_cAttack0$26891, :19951-20062): attack / cAttack0, CrossFade(root, 0.2), the scope destroyed,
standby 0.2 s later. Nothing drawn.

**Prefabs** (probe_summary.txt), all ready by the inventory:
- cAttack_charge: EffectControl life 2 + followPosition + followState, AudioSource cAttack1, cAttack_star (ImageEmitter,
  delay 0.7) at (0.1, 1, 0.6), a LineEmitter 0.7 m up.
- cAttack_fire: life 1, AudioSource nAttack, LineEmitter and ParticleEmitter 2 m ahead.
- cAttack_hit: life 1, ImageEmitter, ParticleEmitter, LineEmitter.

## From the Above (RPC_fromTheAbove, $RPC_fromTheAbove$26940, :22067-22274)

- **At the press:** timeouts nAttack 1.5 and bounce agiAdjust(36) (:22247-22250); firePos = mPos + 12 up, fireDir =
  tDir - 12 up (:22253-22259).
- **At 0.1 s** (Yield(2, 0.1) :22272):
  - nAttack_fire at firePos, LookRotation(fireDir) = [50.194, 0, 0] (:22081-22099; life 1, own sound nAttack, probe);
  - own client: ray 16 + 5 × 4 = 36 m on every layer but its own and 1 / 2 (:22119-22134);
  - RPC_nAttack_hit at the hit point with the hero's rotation (:22140), always nAttack_hit (no Snipe Mastery branch). With
    no target that point is the ground at the target point; with a target, the body's front at the target point;
  - Hyper Shot only beyond 16 m (:22183-22214), so no voice.

---
## Emotes and basic moves

**RPC_emotion** ($RPC_emotion$27480, :42560-43265):
- The voice plays at 0, before the clip (:42625-42703). It is gated by pvoice, by `Time.time > actionTime + 2`, and by
  the player being the own hero, game code 31 or a mission teammate.
- emo_chat loads chat + Random.Range(1, 4). Every other emo_<name> loads Voices/<name> and plays only if the file loads.
- Then the clip with a 0.2 s fade (looped for the talk / pose / battle / dance group, :43173-43174). No effects and no
  Sounds/ loads.

| emote | clip | voice | lines |
|---|---|---|---|
| hi, wave | wave | hi / wave | :42757, :42763 → :43198 |
| ty, bow | bow | ty / bow | :42772, :42778 → :43190 |
| laugh | laugh | laugh | :42785-42791 |
| sit | sit | (none) | :42805-42811 |
| sleep | sleep | sleep | :42817-42823 |
| cheer | cheer | cheer | :42829-42835 |
| beg | beg | beg | :42841-42847 |
| cry | cry | cry | :42853-42859 |
| talk, chat | talk | (none) / chat1-3 | :42867, :42873 → :43167 |
| pose | by worn set | pose | :42880-43126 |
| battle | battle | battle | :43136-43142 |
| dance | dance | (none) | :43151-43159 |

The pose clip by worn set:
- pose5: w_rab5 + a_rab5 + c_rab5.
- pose15: a_rab15 + c_rab15, with no weapon test.
- pose25 / 35 / 45 / 65: weapon, armor and hat of that number.
- pose58: w_rab58 + a_all58 + c_all58.
- pose46: w_rab46 + c_all46.
- w_rab56 + c_all56: a frozen pose (animation.Stop, :43086-43103), no clip.
- pose66: w_rab66 + c_all66.
- Anything else: pose.

**Basic moves:** nothing. No AnimationEvents (probe_events.txt) and no footstep code, so run, root, falling and getUp are
silent.

**RPC_activateIcon1** (:47908-48188): loops battle with a 0.2 s fade (:48104-48122), no voice. No tile (Penguin decision 19).

**KO**
- RPC_ko ($RPC_ko$27649, :48227-48570): actionState ko, the ko clip (:48426-48444); ko1 or ko2 at 0 (Random.Range(0, 2)
  :48476, :48486 / :48517, :48560 / :48563); getUp after 3 s (:48568, :48343); standby 1 s later (:48556).
- RPC_dead ($RPC_dead$27656, :48603-48940): Rewind + ko (:48797-48800); deadEffect at the hero (:48806-48812), before the
  pvoice gate (:48818), so on every path; dead1 or dead2 (:48847-48932).
- deadEffect: life 3, an ImageEmitter 0.8 m up (delay 0.3) and two LineEmitters. Ready (also Effects/deadEffect in the
  container).

**RPC_revive** ($RPC_revive$27663, :48973-49223): getUp, no voice load. Silent.

No entry for sit, dance, getUp, root, run, falling, pose37 or the TTO emote clips (clap, cooking, fishingRabbit, mining,
planting, wai).

---
## Paste-ready cue entries for wardrobe/fx_cues/rabbit.json (identical to checks\fx_rabbit_research\attacks_emotes\cues.json)

```json
  "nAttack": {
    "why": "Rabbit.cs doNormalAttack (:8876-9100): Customized Shotgun 2 (#354, passives on) with a shotgun worn (getCustomizedShotgunLv :11087-11131, isShotgun :11136-11256: w_rab22 / 24 / 32 / 34 / 39 / 47 / 48 / 50 / 51 / 52 / 55 / 69, the set rabbitShotgun) in a mission / arena (mGameType > 4 :9051) starts RPC_shotgun (:9057), else RPC_nAttack (:9078). RPC_nAttack ($RPC_nAttack$26825, :17359-18403): at 0 attack, actionTime, myCommand nAttack, timeout 1.5 (1 with w_rab59 :17809-17823), LookAt the aim, Rewind + animation.Play(nAttack), Once (a cut, :17849-17859), voice nAttack1 (pvoice; own hero, else a mission teammate :17864-17888; load :17901, PlayOneShot :18399), Yield(2, 0.3) (:18385). 0.3 s, still attacking (:17374): moveSpeed -3 (the recoil step back, :17384; in place here, Penguin decision 8), firePos = mPos + up + forward (:17389), fireDir = tDir - up (:17394), the aim the no-target 10 m ground point (GameGui.cs:1659; Penguin decision 1); mission / arena only (mGameType <= 4 skips the whole shot :17451, kept as the Sheep / Penguin precedent); Bouncing Bullet #401 on (:17459): Sounds/nAttack PlayOneShot (:17471-17483; the bouncingBullet prefab has no AudioSource, probe_summary.txt), bounceRange 20 + 5 x Combo 4 = 40 (:17512), the loop IL_F77 (:18075-18378): segment 1 bouncingBullet at firePos, LookRotation(fireDir) (:18097-18109) = [5.711, 0, 0] from (0, 1, 1); Physics.Raycast on layer 1 (Default, :17497, :18123), which the ground is on (Math.cs:1102-1105), meets the floor at (0, 0, 11) (geom.txt): bouncingBullet_hit there with the hero's rotation (LookRotation(forward) :18135-18147), bounceMagnitude int 10.05 = 10, bounceRange 30 (:18161-18171); RaycastAll over the hero layers (130816 - own, :18197) along those 10 m meets the target body (Bat decision 4) at (0, 0.13, 9.7): RPC_snipeShot_hit with Snipe Mastery #431 (:18265-18271), whose prefab Effects/snipeShot_hit is in neither BB's container nor TTO's catalog (container.txt; probe_tto_err.txt): Cannot find snipeShot_hit Effect (:11435-11467), nothing drawn; the hit with Hyper Shot 4 and Snipe Mastery's raw distance (9.7 x 4 > 0, :18230-18253, :18319-18325) sets isHyperShot; bounceCount 1 at the hit, not a bounce (:18331); the floor's reflection (Vector3.Reflect :18365-18370), WaitForFixedUpdate (:18393, 0.02 s nominal): segment 2 bouncingBullet at (0, 0, 11) rot [-5.711, 0, 0] at 0.32 s (range 30 > 12 :18082), no wall above (bounceCount = 9 :18179); the next fixed step (0.34 s) leaves the loop (:18076, :18378) for IL_14D7 (:17924): HyperShot message (GUI), the voice nAttack2 (not isBouncingBullet :17937, isHyperShot :18006; load :18051, PlayOneShot :18395); Yield(4, 0.15) (:18389) moveSpeed 0 at 0.49 s, Yield(5, 0.34) (:18391) standby at 0.83 s (:17729-17752). RPC_shotgun ($RPC_shotgun$27317, :36172-36527): at 0 attack, timeout 1.5, LookAt, animation.Play(nAttack) with no Rewind, Once (:36474-36495), no voice anywhere in it (TTO1102 Rabbit.<RPC_shotgun>d__229 :20992-21569 the same); Yield(2, 0.3) (:36525); 0.3 s moveSpeed -3 (:36200), shotgun_fire at position + TransformDirection(0, 1, 1) with the hero's rotation (:36205-36223; its AudioSource plays shotgun), Damage.FindRecTarget's box from position + forward, 12 m long, half-width 1.5 -> 4 m (sLv 2, :36270) holds the target at 10 m: RPC_shotgun_hit at the target's transform.position + up = (0, 1, 10) with the hero's rotation (:36354; :11044-11067); standby at 0.79 s (Yield 0.15 :36518, 0.34 :36520, :36409-36432). Both take worn / notWorn rabbitShotgun on R (Rabbit weapons mount on mount_Hand_R, data/rabbit/props_weapons.json)",
    "cues": [
      [0, "voice", "nAttack1", {"notWorn": ["R", "rabbitShotgun"]}],
      [0.3, "sound", "nAttack", {"notWorn": ["R", "rabbitShotgun"]}],
      [0.3, "fx", "bouncingBullet", {"y": 1, "d": 1, "rot": [5.711, 0, 0], "notWorn": ["R", "rabbitShotgun"]}],
      [0.3, "fx", "bouncingBullet_hit", {"d": 11, "notWorn": ["R", "rabbitShotgun"]}],
      [0.3, "fx", "shotgun_fire", {"y": 1, "d": 1, "worn": ["R", "rabbitShotgun"]}],
      [0.3, "fx", "shotgun_hit", {"y": 1, "d": 10, "worn": ["R", "rabbitShotgun"]}],
      [0.32, "fx", "bouncingBullet", {"d": 11, "rot": [-5.711, 0, 0], "notWorn": ["R", "rabbitShotgun"]}],
      [0.34, "voice", "nAttack2", {"notWorn": ["R", "rabbitShotgun"]}]
    ]
  },
  "@CustomizedShotgun:nAttack": {
    "why": "Customized Shotgun 2 (#353 / #354, its own tile: one tile per skill, Clear Arrow's shape, Chameleon decision 13): the shotgun shot whatever is worn (the game needs isShotgun, Rabbit.cs:11098; the tile shows the skill): RPC_shotgun ($RPC_shotgun$27317, :36172-36527): at 0 animation.Play(nAttack), Once (:36492-36495), no voice; 0.3 s (Yield(2, 0.3) :36525): shotgun_fire at position + TransformDirection(0, 1, 1), hero rotation (:36205-36223; its own AudioSource shotgun), RPC_shotgun_hit at the 10 m target's position + up (:36354, :11044-11067; the box FindRecTarget 12 m x 1.5-4 m, sLv 2, :36270, mission / arena only :9051); standby at 0.79 s (:36518, :36520, :36422)",
    "cues": [
      [0.3, "fx", "shotgun_fire", {"y": 1, "d": 1}],
      [0.3, "fx", "shotgun_hit", {"y": 1, "d": 10}]
    ]
  },
  "cAttack1": {
    "why": "Rabbit.cs doBeginCharge (:9155-9250, #111, from standby / run, 0.1 s after the last action) -> RPC_cAttack1 ($RPC_cAttack1$26855, :18604-19034), Charge Attack 3 (#113): at 0 (IL_B64 :18905-18930) attack, actionTime, myCommand cAttack1, LookAt, PlayAnimation(cAttack1, 0) (a cut, :18921), Once, moveSpeed 0; the voice cAttack (pvoice, mission / arena for every client, the own hero too :18939, a teammate :18945; load :18957, PlayOneShot :18969; kept as the Sheep / Penguin precedent); cAttack_charge created at the hero's position and rotation (:18982-18998; EffectControl life 2, followPosition, followState, its AudioSource plays cAttack1, its cAttack_star 1 m up 0.6 ahead after a 0.7 s delay, probe_summary.txt; the action stays attack until the release, so it lives its 2 s); Yield(2, 1) (:19032) to the cAttack2 step at 1.0 s",
    "cues": [
      [0, "voice", "cAttack"],
      [0, "fx", "cAttack_charge"]
    ]
  },
  "cAttack2": {
    "why": "Rabbit.cs RPC_cAttack1 case 2 (:18617-18731) at 1.0 s, still attack / cAttack1: PlayAnimation(cAttack2, 0) cut in, Loop (:18636-18641); the own player only (:18646) gets the sniperCamera at position + TransformDirection(0, 1.05, 0.15) (:18654-18684; Transform, the Rabbit_sniperCamera script and an AudioSource deadShot, playOnAwake off, no renderer: probe_snipercam.txt) and the camera's specialTarget / FOV 60 (:18698-18715, left out as the camera effects, Cat decision 43); its OnGUI (Rabbit_sniperCamera.cs:246-468) checks every 0.1 s (:308-314) a ray along its forward, the hero's with no mouse (Rabbit.cs:18762-18816): at y 1.05 it meets the target body's head zone (1.05 - 0.6 > 0.5 x 0.5, Rabbit_sniperCamera.cs:357; geom.txt), Dead Shot #411 on (hasDeadShot :266, :335): mDeadShotTimer = now at the first check (:363-369), and at the next check, more than 0.1 s and under 1 s later (:381-387), audio.Play() = sounds/deadShot (:375-393) once (Loop off): 0.1 s, the nominal interval (Mole decision 45); the crosshair GUI and the Dead Shot bar (:246-305, :479-510) are screen UI, left out; held 4 s (the SEQ's full charge: Dead Shot's x3 at clamp(t, 0, 4) = 4, Rabbit.cs:19486, Rabbit_sniperCamera.cs:500), released at 5.0 s",
    "cues": [
      [0.1, "sound", "deadShot"]
    ]
  },
  "cAttack3": {
    "why": "Rabbit.cs doReleaseCharge (:9254-9353): attack / cAttack1, a mission / arena and the sniperCamera alive (:9297-9303) -> RPC_cAttack2 along the camera's flat forward (:9309; else RPC_cAttack0's cancel :9330, a CrossFade to root, no effect :19960-20060). RPC_cAttack2 ($RPC_cAttack2$26869, :19187-19785): at 0 attack, myCommand cAttack2, LookAt, PlayAnimation(cAttack3, 0) cut in, Once (:19300-19321), moveSpeed -2 (:19327; in place here), cAttack_fire at position + up with LookRotation(the camera's forward = the hero's) (:19330-19366; its own AudioSource plays nAttack, LineEmitter 2 m ahead); the own client's ray from the camera (hero + (0, 1.05, 0.15)) along its forward, 20 + 5 x Combo 4 = 40 m (:19380-19392), meets the target body at (0, 1.05, 9.7) (Bat decision 4's body, cylinder radius 0.3, as its guardian hits at y 1 d 9.7): RPC_cAttack_hit there with LookRotation(hero forward) (:19398; :9378-9401); the head zone (:19434) and Dead Shot 3 x (:19445-19486, the timer set at 1.0 s, 4 s on the head) give Dead Shot! (GUI, :19529-19535) and the voice headShot (pvoice, own or a mission teammate :19540-19562; load :19575, PlayOneShot :19587); Yield(2, 0.2) (:19781): moveSpeed 0, the camera destroyed (:19217-19254); Yield(3, 0.5) (:19779): standby at 0.7 s (:19257-19275)",
    "cues": [
      [0, "fx", "cAttack_fire", {"y": 1}],
      [0, "fx", "cAttack_hit", {"y": 1.05, "d": 9.7}],
      [0, "voice", "headShot"]
    ]
  },
  "wave": {
    "why": "Rabbit.cs RPC_emotion ($RPC_emotion$27480, :42560-43265): every emote's voice at 0, before its clip: pvoice, Time.time > actionTime + 2, own hero / game code 31 / a mission teammate (:42625-42659); emo_chat loads chat + Random.Range(1, 4) (:42677-42683), every other emo_<name> Voices/<name> (Substring(4) :42691), played only if it loads (:42697-42703); the clip with a 0.2 s fade, no effect, no Sounds/ load; the rip's Rabbit voices have hi, wave, ty, bow, laugh, sleep, cheer, beg, cry, battle, pose, chat1-3 and no sit, talk or dance (container.txt); emo_hi (:42757) and emo_wave (:42763) both play wave (:43198): voice hi or wave",
    "cues": [
      [0, "voice", "hi|wave"]
    ]
  },
  "bow": {
    "why": "Rabbit.cs RPC_emotion (:42560): emo_ty (:42772) and emo_bow (:42778) both play bow (:43190); both voices are in the Rabbit's rip (container.txt): voice ty or bow (as wave takes hi or wave)",
    "cues": [
      [0, "voice", "ty|bow"]
    ]
  },
  "laugh": {
    "why": "Rabbit.cs RPC_emotion (:42560): voice at 0, Voices/<name> (:42691, PlayOneShot :42703); emo_laugh (:42785-42791)",
    "cues": [
      [0, "voice", "laugh"]
    ]
  },
  "sleep": {
    "why": "Rabbit.cs RPC_emotion (:42560): voice at 0, Voices/<name> (:42691, PlayOneShot :42703); emo_sleep (:42817-42823)",
    "cues": [
      [0, "voice", "sleep"]
    ]
  },
  "cheer": {
    "why": "Rabbit.cs RPC_emotion (:42560): voice at 0, Voices/<name> (:42691, PlayOneShot :42703); emo_cheer (:42829-42835)",
    "cues": [
      [0, "voice", "cheer"]
    ]
  },
  "beg": {
    "why": "Rabbit.cs RPC_emotion (:42560): voice at 0, Voices/<name> (:42691, PlayOneShot :42703; the Rabbit's rip has beg, container.txt); emo_beg (:42841-42847)",
    "cues": [
      [0, "voice", "beg"]
    ]
  },
  "cry": {
    "why": "Rabbit.cs RPC_emotion (:42560): voice at 0, Voices/<name> (:42691, PlayOneShot :42703); emo_cry (:42853-42859)",
    "cues": [
      [0, "voice", "cry"]
    ]
  },
  "talk": {
    "why": "Rabbit.cs RPC_emotion (:42560): emo_chat (:42873) plays talk (:43167) with Voices/chat + Random.Range(1, 4) = chat1-3 (:42677-42683; the rip has chat1-3); emo_talk (:42867) plays it silent (no Voices/talk): the tile takes the chat's voice",
    "cues": [
      [0, "voice", "chat1|chat2|chat3"]
    ]
  },
  "battle": {
    "why": "Rabbit.cs RPC_emotion (:42560): emo_battle (:43136-43142): voice battle (:42691, PlayOneShot :42703); RPC_activateIcon1 loops the clip without it (:48104-48122, no tile, Penguin decision 19)",
    "cues": [
      [0, "voice", "battle"]
    ]
  },
  "pose": {
    "why": "Rabbit.cs RPC_emotion (:42560): emo_pose's voice Voices/pose (:42691, PlayOneShot :42703; in the rip) at 0, before the clip is chosen by the worn set (:42880-43126): pose with no full set (:43126)",
    "cues": [
      [0, "voice", "pose"]
    ]
  },
  "pose5": {
    "why": "Rabbit.cs RPC_emotion (:42560): emo_pose's voice pose at 0 (:42691, :42703), then pose5 with w_rab5 + a_rab5 + c_rab5 (:42884-42902)",
    "cues": [
      [0, "voice", "pose"]
    ]
  },
  "pose15": {
    "why": "Rabbit.cs RPC_emotion (:42560): emo_pose's voice pose at 0 (:42691, :42703), then pose15 with a_rab15 + c_rab15 (no weapon test, :42911-42923)",
    "cues": [
      [0, "voice", "pose"]
    ]
  },
  "pose25": {
    "why": "Rabbit.cs RPC_emotion (:42560): emo_pose's voice pose at 0 (:42691, :42703), then pose25 with w_rab25 + a_rab25 + c_rab25 (:42931-42949)",
    "cues": [
      [0, "voice", "pose"]
    ]
  },
  "pose35": {
    "why": "Rabbit.cs RPC_emotion (:42560): emo_pose's voice pose at 0 (:42691, :42703), then pose35 with w_rab35 + a_rab35 + c_rab35 (:42958-42976)",
    "cues": [
      [0, "voice", "pose"]
    ]
  },
  "pose45": {
    "why": "Rabbit.cs RPC_emotion (:42560): emo_pose's voice pose at 0 (:42691, :42703), then pose45 with w_rab45 + a_rab45 + c_rab45 (:42985-43003)",
    "cues": [
      [0, "voice", "pose"]
    ]
  },
  "pose46": {
    "why": "Rabbit.cs RPC_emotion (:42560): emo_pose's voice pose at 0 (:42691, :42703), then pose46 with w_rab46 + c_all46 (:43066-43078)",
    "cues": [
      [0, "voice", "pose"]
    ]
  },
  "pose58": {
    "why": "Rabbit.cs RPC_emotion (:42560): emo_pose's voice pose at 0 (:42691, :42703), then pose58 with w_rab58 + a_all58 + c_all58 (:43012-43030)",
    "cues": [
      [0, "voice", "pose"]
    ]
  },
  "pose65": {
    "why": "Rabbit.cs RPC_emotion (:42560): emo_pose's voice pose at 0 (:42691, :42703), then pose65 with w_rab65 + a_rab65 + c_rab65 (:43039-43057)",
    "cues": [
      [0, "voice", "pose"]
    ]
  },
  "pose66": {
    "why": "Rabbit.cs RPC_emotion (:42560): emo_pose's voice pose at 0 (:42691, :42703), then pose66 with w_rab66 + c_all66 (:43106-43118)",
    "cues": [
      [0, "voice", "pose"]
    ]
  },
  "ko": {
    "why": "Rabbit.cs RPC_ko ($RPC_ko$27649, :48227-48570): ko clip (animation.Play :48441) and voice ko1 or ko2 at 0 (own hero, else a mission teammate :48453-48459; Random.Range(0, 2) :48476, loads :48486 / :48517, PlayOneShot :48560 / :48563), getUp after 3 s (Yield(2, 3) :48568, :48343), standby 1 s later (:48556, :48367), no effect; RPC_dead ($RPC_dead$27656, :48603-48940) plays the same clip (Rewind + Play :48797-48800) and puts deadEffect at the hero's position and rotation first, on every path (:48806-48812, before the pvoice gate :48818; the prefab field, also Effects/deadEffect in the container; EffectControl life 3, an ImageEmitter 0.8 m up after 0.3 s and two LineEmitters, probe_summary.txt), then dead1 or dead2 (Random.Range(0, 2) :48847, :48857 / :48888, PlayOneShot :48929 / :48932): one of the two at random, even chance (the Sheep's decision 11, as wolf.json / mole.json: roll dead, its voices with it; '!dead' = RPC_ko's)",
    "cues": [
      [0, "voice", "ko1|ko2", {"p": 0.5, "roll": "!dead"}],
      [0, "voice", "dead1|dead2", {"p": 0.5, "roll": "dead"}],
      [0, "fx", "deadEffect", {"p": 0.5, "roll": "dead"}]
    ]
  }
```

**From the Above block** (`cues_fromTheAbove.json`). Its key and times assume the Bounce report's tile holds bounce1
from 0 through the air phase. The editor re-keys or shifts the times to the step that tile uses for the air phase, and
puts the Bounce entry's own bounce1 cues in with these. A `@` key replaces the plain entry.

```json
  "@FromtheAbove:bounce1": {
    "why": "From the Above #421 (passive; its own tile on the Bounce's air phase, times from RPC_bounce's start, actionTime :21223): doNormalAttack lets the attack key fire while attack / bounce and Time.time > actionTime + 1 with the nAttack timeout free (Rabbit.cs:8944-8997) -> RPC_fromTheAbove ($RPC_fromTheAbove$26940, :22067-22274), which plays no clip and no voice: timeout nAttack 1.5 and bounce agiAdjust(36) (:22247-22250), firePos = mPos + 12 up, fireDir = tDir - 12 up (:22253-22259); Yield(2, 0.1) (:22272): nAttack_fire at firePos, LookRotation(fireDir) = [50.194, 0, 0] (:22081-22099; its own AudioSource plays nAttack), the own client's ray 16 + 5 x 4 = 36 m (:22119-22134) to the target point 15.6 m away (geom.txt): RPC_nAttack_hit there with the hero's rotation (:22140; :9112-9135; never snipeShot_hit); presses at the earliest, 1.0 s and then each 1.5 s timeout: shots at 1.1, 2.6, 4.1, 5.6, 7.1, 8.6 s, before the landing at 0.9 + 4 x 2 = 8.9 s (RPC_bounce case 3 :21068-21073, RPC_bounce0 :21108-21114); the Bounce's own bounce1 cues (its report) go in this entry too",
    "cues": [
      [1.1, "fx", "nAttack_fire", {"y": 12, "rot": [50.194, 0, 0]}],
      [1.1, "fx", "nAttack_hit", {"d": 10}],
      [2.6, "fx", "nAttack_fire", {"y": 12, "rot": [50.194, 0, 0]}],
      [2.6, "fx", "nAttack_hit", {"d": 10}],
      [4.1, "fx", "nAttack_fire", {"y": 12, "rot": [50.194, 0, 0]}],
      [4.1, "fx", "nAttack_hit", {"d": 10}],
      [5.6, "fx", "nAttack_fire", {"y": 12, "rot": [50.194, 0, 0]}],
      [5.6, "fx", "nAttack_hit", {"d": 10}],
      [7.1, "fx", "nAttack_fire", {"y": 12, "rot": [50.194, 0, 0]}],
      [7.1, "fx", "nAttack_hit", {"d": 10}],
      [8.6, "fx", "nAttack_fire", {"y": 12, "rot": [50.194, 0, 0]}],
      [8.6, "fx", "nAttack_hit", {"d": 10}]
    ]
  }
```

Counts: 25 + 1 entries, 50 cues (23 fx, 2 sound, 25 voice).

---
## Parts needed (build stage)

**1. `ITEM_SETS.rabbitShotgun`** (index.html, one line beside bisonHammer). It holds the props of BB's isShotgun
(Rabbit.cs:11136-11256; TTO1102 Rabbit::isShotgun the same, Rabbit.c:36197) through data/item_map.json's rabbit.weapon:

```js
rabbitShotgun: ["traderGun", "traderGunR", "merchantGun", "merchantGunR", "flowerGun", "antShotgun", "antShotgunR",
  "royalGun", "royalGunR", "timeShotgun"]
```

w_rab50 and w_rab51 are both royalGun, and w_rab55 has no item. wardrobe_fx_check.py does not check `worn` items, and
no OPTS change is needed: every option used is already in OPTS (parse_blocks.py).

**2. SEQ / SEQ_SKILL (index.html).**
- `SEQ.rabbit`: add `"Normal Attack: nAttack"` and `"Customized Shotgun: nAttack"`.
- Replace `"Charge Attack: cAttack1 cAttack2* cAttack3"` with `"Charge Attack: cAttack1@1 cAttack2*@4 cAttack3"`.
- Add `"From the Above: <the Bounce tile's steps>"`, after the Bounce report.
- `SEQ_SKILL.rabbit`: `"@CustomizedShotgun": "customizedShotgun"`, `"@FromtheAbove": "fromTheAbove"` (Bible ids
  rabbit_customizedShotgun, rabbit_fromTheAbove).
- The Normal Attack and Charge Attack tiles keep the Combo / Charge Attack icons (rabbit_nAttack, rabbit_cAttack): the
  editor's wardrobe_skill_icons.py run.

**3. Inventory (pipeline/wardrobe_fx_inventory.py, "### rabbit").**
- `deadEffect`: a hero-prefab field, also at Effects/deadEffect. Ready (probed).
- `snipeShot_hit`: named by the code (:11448), in neither game's data. Nothing to build or cue.
- `sniperCamera`: its "needs Rabbit_sniperCamera" becomes "not drawn". No renderer; its OnGUI is screen UI and its
  AudioSource's deadShot is a sound cue (Read this first 6).

**4. Nothing else.**
- Every cued effect is ready by the inventory: bouncingBullet, bouncingBullet_hit, shotgun_fire, shotgun_hit,
  cAttack_charge, cAttack_fire, cAttack_hit, nAttack_fire, nAttack_hit and deadEffect.
- Both sounds (nAttack, deadShot) are in the rip's heroes/rabbit/sounds/, which hero_sound_wav reads first.
- Every voice is in heroes/rabbit/voices/.
- No new cue kind or option.

## Left out

- **The recoil steps.** moveSpeed -3 on the shot (:17384, :36200) and -2 on the release (:19327). The hero stays in place
  (Penguin decision 8).
- **Screen and camera.**
  - The sniper scope: crosshair, distance label, Dead Shot picture and bar (Rabbit_sniperCamera.cs:246-510).
  - The camera's specialTarget, FOV 60 and mouse aiming (Rabbit.cs:18698-18816).
  - The HyperShot / Head Shot! / Dead Shot! messages.
  - Reason: Cat decision 43, Chameleon 52.
- **Gear procs on a hit** (onNormalAttackHit, :49223-): random LCK statuses on the target or the hero, and heal1. Reason:
  Chameleon decision 53, Monkey 52.
- **The plain rifle path** (nAttack_fire + its ray + nAttack_hit / snipeShot_hit, :17531-17631). Under the passives-on
  rule Bouncing Bullet replaces it. nAttack_fire / nAttack_hit still show in From the Above.
- **snipeShot_hit**: no prefab in either game.
- **RPC_cAttack0** (the cancel), **RPC_activateIcon1** (battle looped): no tiles (Chameleon 18, Penguin 19).
- **The 2 s voice gates and the timeouts** (Cat decision 35).
- **Damage and statuses**: Hyper Shot / Dead Shot numbers, SP +1.
- **Silent clips**: the TTO-only emote clips (clap, cooking, fishingRabbit, mining, planting, pose37, wai; Cat decision 16),
  and sit, dance, run, root, falling, getUp.
- **The w_rab56 + c_all56 frozen pose** (animation.Stop, no clip).

## Open questions (each with my recommended answer)

1. **The Normal Attack's target.**
   - **Recommendation: aim at the no-target ground point** (Penguin decision 1, Bat 1, Chameleon 22, Mole Q1). The shot
     then ricochets off the floor 11 m ahead as the game draws it. A target body at the target point counts as hit, as
     Chameleon decision 22's criticalPlus_hit at d 10 does, which gives the Hyper Shot voice nAttack2 at 0.34 s.
   - Alternative A: no target, no nAttack2. Everything drawn stays the same, since Snipe Mastery's hit draws nothing.
   - Alternative B: aim at the body centre (0, 0.6, 10), the game's targeted aim (GameGui.cs:1626).
     - Segment 1 then runs (0, 1, 1) → floor at (0, 0, 26), 25.02 m (bounceMagnitude 25, range 15).
     - Its bouncingBullet_hit and the second tracer are out of the default view.
     - The tracer's length is the prefab's own (its LineEmitter's endRadius 10 / localVelocity (0, 0, 10)), not the
       segment's.
2. **Customized Shotgun.**
   - **Recommendation: `worn` / `notWorn` with `ITEM_SETS.rabbitShotgun` in the Normal Attack tile**, so a worn shotgun
     shows the game's shot.
   - **Plus its own tile `"Customized Shotgun: nAttack"` that always shows the shotgun shot** (one tile per skill; the
     precondition is an item the tile cannot put on).
   - Alternative: the tile follows the worn weapon too (identical to Normal Attack when no shotgun is worn).
3. **The Charge Attack's hold.**
   - **Recommendation: `cAttack2*@4`** (Dead Shot's ×3, the SEQ rule's full charge).
   - Any release after 1.0 s draws the same cues; only the GUI multiplier differs, so `@1.5` would look the same with a
     shorter tile.
4. **From the Above.**
   - **Recommendation: its own tile on the Bounce sequence, with six shots** (each press at the earliest, every 1.5 s, as
     the Combo stages are pressed at the earliest).
   - Alternative: one shot at 1.1 s.
   - Either way the Bounce report owns the sequence's shape and the landing stomp. If it already cues From the Above,
     keep one entry.
5. **Tiles for the other shooting passives** (Bouncing Bullet, Snipe Mastery, Hyper Shot, Dead Shot, Combo).
   - **Recommendation: none of their own.** They change the Normal Attack's / Charge Attack's look with no roll. Passives
     on already shows them there, as the Chameleon's Bow Mastery / Far Reach and the Mole's Speed Drill / Super Dig
     (decisions 38).
   - Alternative: a Bouncing Bullet tile identical to Normal Attack, for its icon.
6. **Show the mission-only shot?** In town the game fires nothing (:17451), the release always cancels (:9297), and the
   cAttack voice is silent (:18939).
   - **Recommendation: show them**, following the precedent.
7. **The sniperCamera.**
   - **Recommendation: no fx cue and no part**, since it has no renderer. Its deadShot as a `"sound"` cue at 0.1 s into
     cAttack2.
   - The alternative, building a Rabbit_sniperCamera layout so an fx cue with `playAudio` starts it, gives the same sound
     for more work.

## Offer for the Bible (rabbit-skill-reference.md; the user decides)

- **Snipe Mastery removes the Normal Attack's hit spark.**
  - RPC_snipeShot_hit loads Effects/snipeShot_hit (:11448), which is in neither BB's data nor TTO's catalog ("Cannot find
    snipeShot_hit Effect").
  - With Snipe Mastery a rifle hit shows no hit effect in either game. The plain-path ray and the Bouncing Bullet both
    take this path (:17594, :18265).
- **Bouncing Bullet.**
  - The floor counts as a wall: it is on layer Default, the bounce ray's mask (:17497, :18123; Math.cs:1102). A no-target
    shot therefore ricochets off the floor 1 m past the target point (11 m ahead).
  - The segments are one fixed step apart (WaitForFixedUpdate :18393), not 0.3 s. :18385 is the 0.3 s wait before the
    shot.
  - "Only after a real ricochet" has one exception. When the first segment hits no wall, bounceCount is set to 9 before
    its RaycastAll (:18179), so its hits already count as a bounce: the Bouncing Bullet message and voice.
- **Timings.**
  - Normal Attack: the shot at 0.3 s, the Hyper Shot / Bouncing Bullet voice after the loop (about 0.34 s), standby at
    0.83 s.
  - Customized Shotgun: no voice at all, standby at 0.79 s.
  - Charge Attack: the scope comes 1.0 s after the press (Yield 1 :19032). A release before that, or outside a mission /
    arena, is the cancel (:9297-9330). The release's standby comes at 0.7 s.
  - The scope plays sounds/deadShot once, about 0.1 s after the crosshair first rests on a head (Rabbit_sniperCamera.cs:357-393).
- **Town.** The Normal Attack fires nothing outside a mission / arena (:17451), and the Charge Attack's voice is
  mission-only for the own hero too (:18939).
- **Voices.** RPC_revive never loads the rip's voices/revive. The Rabbit's emo_chat uses chat1-3.


---
## Verification (13/11/2026)

Checker, office PC. I re-derived the claims from `C:\Users\Jump\Desktop\12tails\DecompiledSource\Rabbit.cs` and
`Rabbit_sniperCamera.cs`, and from the rip (`RippedAssets/.../heroes/rabbit/`: voices, sounds,
`effects/sniperCamera.prefab`). I also ran three probes:
- `wardrobe_fx.py rabbit --probe` on 23 names (`checks/fx_rabbit_research/verify/probe.json`);
- `wardrobe_fx_tto.py rabbit --probe snipeShot_hit,kneeShot_hit,herbFinder` (`tto_probe.err`);
- `checks/fx_rabbit_research/verify/verify.py`, output in `verify.txt`. It parses every block, checks kinds and options
  against wardrobe_fx_check.py, checks keys against data/rabbit/clips.json and the proposed SEQ ids, checks that times are
  in order, and works out the shot geometry.

**This section wins over the report body.**

**Confirmed as written** (no change):
- **nAttack's clock.**
  - The shot comes at 0.3 s (Yield(2, 0.3) :18385).
  - Segment 2 comes one fixed step later: IL_F66 is a WaitForFixedUpdate (:18393), and case 3 goes back into IL_F77
    (:17720-17721).
  - The loop is left at 0.34 s, moveSpeed is 0 at 0.49 s (:18389) and standby comes at 0.83 s (:18391).
  - The Bible's "0.3 s wait between segments" is wrong, so the offer stands.
- **The voice choice at IL_14D7** (:17924-18061).
  - bouncingBullet plays only with isBouncingBullet, which needs bounceCount > 1 at a hit (:18331). Otherwise nAttack2
    plays, with isHyperShot.
  - Snipe Mastery keeps the raw flat distance: without it, `!hasSkill(431)` makes it clamp(d - 16) (:18230-18253).
- **Customized Shotgun.**
  - RPC_shotgun has no voice anywhere.
  - shotgun_fire spawns at position + TD(0, 1, 1) with the hero's rotation (:36205-36223). shotgun_hit spawns at each
    target's position + up (:36354).
  - isShotgun's 12 codes (:11085-11260) map through data/item_map.json to the 10 props listed. w_rab50 and w_rab51 are
    both royalGun, and w_rab55 has no item. All 10 mount on mount_Hand_R (data/rabbit/props_weapons.json), so the
    `ITEM_SETS.rabbitShotgun` line is right.
- **Charge Attack.**
  - cAttack2 starts at 1.0 s (:19032, :18636, Loop :18641).
  - The scope sits at hero + TD(0, 1.05, 0.15) (:18684).
  - The release destroys the scope 0.2 s in, and standby comes at 0.7 s (:19217-19254, :19779-19781).
  - The head zone and Dead Shot are at :19434-19486, and headShot plays on a head (:19529-19587).
  - `"Charge Attack: cAttack1@1 cAttack2*@4 cAttack3"` stands. A charge is shown at full charge (index.html:1202), and
    Dead Shot reaches x3 at 4 s from the timer set at the scope's first check.
- **deadShot.**
  - sniperCamera.prefab:49-53: the `m_audioClip` guid 9970778a... is `sounds/deadShot.wav.meta`, with playOnAwake 0 and
    Loop 0.
  - The 0.1 s check and the window of more than 0.1 s and less than 1 s are as described (Rabbit_sniperCamera.cs:308-393).
- **Voices and sounds.** Every voice is in the rip: nAttack1, nAttack2, cAttack, headShot, hi, wave, ty, bow, laugh,
  sleep, cheer, beg, cry, chat1-3, battle, pose, ko1, ko2, dead1 and dead2. So are both sounds, nAttack and deadShot.
  There is no sit, talk, dance, chat4, clap or wai voice.
- **Effects.**
  - Every cued effect probes.
  - snipeShot_hit is a KeyError in BB and is not in TTO's catalog. catalog.bin has only the icon keys herbfinder0-4,
    kneeshot5, snipemastery5 and snipercamera.
- **RPC_revive** loads no Voices/revive anywhere in Rabbit.cs. Cat.cs:49817 does, which is why the Cat's getUp has a voice
  and the Rabbit's does not.
- The emote branches and pose sets are as listed (:42677-43151).
- **JSON.**
  - Both blocks parse: 25 + 1 entries and 50 cues (23 fx, 2 sound, 25 voice).
  - Every key is a Rabbit clip or a proposed SEQ step, and every option is in OPTS.
- **TTO.** No TTO clip is cued. clap and wai are released but stay silent (Cat decision 16).

**Findings**

1. **The target body is a capsule, not a cylinder, so two hit points move.**
   - The standard body is the CharacterController (Penguin decision 3, plans/fx_penguin/cast_a.md:89; Bat decision 4):
     centre 0.6 m up, height 1, radius 0.3. Its two end caps are centred at y 0.4 and y 0.8. skills_a.md:43 uses the
     capsule too.
   - The report's "cylinder r 0.3, y 0.1-1.1" (:269) is wrong wherever a ray meets the body above y 0.8 or below y 0.4
     (verify.txt).
   - **cAttack3's `cAttack_hit`.** The level scope ray at y 1.05 meets the upper cap at **(0, 1.05, 9.834)**, not at
     d 9.7. This is still the head zone (0.45 > 0.25). The cue becomes `{"y": 1.05, "d": 9.83}`.
   - **nAttack's segment 1** meets the lower cap at **(0, 0.106, 9.941), 8.985 m out**.
     - It is a graze, 1.5 mm inside the radius, but still a hit inside the 10 m RaycastAll. So isHyperShot and the voice
       nAttack2 at 0.34 s stand.
     - No cue changes, because the snipeShot_hit there draws nothing. Only the why's point changes.
     - "Read this first" 2's "(0, 0.13, 9.7), 8.74 m" and the table row at 0.3 s change too: read (0, 0.106, 9.94),
       8.99 m.

   Corrected entries are below (for nAttack, only the why changes).
2. **deadShot must stop when the scope is destroyed. That needs a page part.**
   - The clip is 4.919 s long (sounds/deadShot.wav), and it is the scope's own AudioSource. Destroy(scope) 0.2 s after the
     release (:19254, after Yield(2, 0.2) :19781) stops it.
   - So it plays from 1.1 s to 5.2 s of the tile: **4.1 s**.
   - The page's "sound" cue plays its file to the end and keeps no handle (index.html:5517), so on the page it would run
     0.82 s past the game.
   - Rule: a missing part is built.
   - Cue: `[0.1, "sound", "deadShot", {"kill": 4.1}]`. kill is already in wardrobe_fx_check.py's OPTS.
   - "Parts needed" 4 says "No new cue kind or option". It now reads: one option gains a meaning for sounds.

   The part goes in index.html, beside HeroPropHide, plus one line in fxDue. The cue-format comment gets the sentence from
   the class comment.

   ```js
   // a "sound" / "voice" cue's kill (2026-11-13, the Rabbit's deadShot, plans/fx_rabbit/attacks_emotes.md Verification 2:
   // the sniperCamera's own AudioSource stops when RPC_cAttack2 destroys the scope, Rabbit.cs:19254): the sound stopped
   // kill seconds after its cue, or with a new pick (FX.live; Fx's shape for the checks: name, emitters, attached, group, loops)
   class SoundCut {
     constructor(name, h, kill) { this.name = "sound:" + name; this.alive = true; this.age = 0; this.emitters = []; this.loops = []; this.group = new THREE.Group(); this.h = h; this.killAt = kill; }
     attached() { return false; }
     update(dt) { this.age += dt; if (this.age >= this.killAt) this.dispose(); }
     dispose() { if (this.alive) { this.alive = false; this.h.stop(); } }
   }
   ```

   In fxDue, it replaces `else if (c.kind !== "fx") Sound.play(cls, sfxFile(c), c.vol);`:

   ```js
       else if (c.kind !== "fx") { const h = Sound.play(cls, sfxFile(c), c.vol); if (c.kill != null) FX.live.push(new SoundCut(c.name, h, c.kill)); }
   ```

   - Sound.play's handle already has stop() (index.html:3953-3955).
   - FX.live's update, its filter and fxClear handle it the same way they handle HeroPropHide (:5551-5552, :5434).
   - Its check: a fx_check run on the Charge Attack tile sees `sound:deadShot` leave FX.live at 5.2 s.
3. **Customized Shotgun's tile has no route to its icon.**
   - A SEQ_SKILL tile gets its HD icon only through OWN_TILE in wardrobe_skill_icons.py (:67-76). The Chameleon's
     criticalPlus and clearArrow on nAttack1 (:73) work this way.
   - "Parts needed" 2 names only the icon run.
   - Add this line, merged with effect_only.md block 4:

   ```python
               # the Rabbit's Customized Shotgun on the Normal Attack's clip, From the Above on Bounce's clips (2026-11-13,
               # plans/fx_rabbit/attacks_emotes.md, effect_only.md)
               "rabbit": {"customizedShotgun": ["nAttack"], "fromTheAbove": ["bounce1", "bounce2"]},
   ```
4. **The From the Above block is replaced. Paste only effect_only.md's entry** (its Verification 1).
   - That entry has Bounce's own bounce1 cues and the shots in one `@FromtheAbove:bounce1` key. This block leaves that
     merge to the editor.
   - It changes two things from this block.
     - The hits go on the target body at (0, 0.356, 9.703), `{"y": 0.36, "d": 9.7}`, not on the ground at d 10. The ray's
       mask is ~(own + layers 1, 2) (:22119), so it can hit the foe. Every cue uses the one body (Bat decision 4), as
       this report's own nAttack and skills_a's ray hits do.
     - The pitch stays 50.194.
   - The counts here become 25 entries and 38 cues.
5. **The SEQ and SEQ_SKILL lines** ("Parts needed" 2) are right. effect_only.md's Verification 2 and 3 merge them with
   that report's lines.

**Calls made (the user was not available):**
- The capsule, not the cylinder: the CharacterController is the body (Bat decision 4, Penguin decision 3).
- The graze counts as a hit, because the geometry says so. Q1's recommendation stands.
- deadShot is cut with kill, as the game's Destroy cuts it. It is built as a part, not left running (the standing rule).

**Corrected entries.** Replace these three in the block above; every other entry stays the same. verify.py checked them
(`checks/fx_rabbit_research/verify/verify.py`): 3 entries, 12 cues, ok.

```json
  "nAttack": {
    "why": "Rabbit.cs doNormalAttack (:8876-9100): Customized Shotgun 2 (#354, passives on) with a shotgun worn (getCustomizedShotgunLv :11087-11131, isShotgun :11136-11256: w_rab22 / 24 / 32 / 34 / 39 / 47 / 48 / 50 / 51 / 52 / 55 / 69, the set rabbitShotgun) in a mission / arena (mGameType > 4 :9051) starts RPC_shotgun (:9057), else RPC_nAttack (:9078). RPC_nAttack ($RPC_nAttack$26825, :17359-18403): at 0 attack, actionTime, myCommand nAttack, timeout 1.5 (1 with w_rab59 :17809-17823), LookAt the aim, Rewind + animation.Play(nAttack), Once (a cut, :17849-17859), voice nAttack1 (pvoice; own hero, else a mission teammate :17864-17888; load :17901, PlayOneShot :18399), Yield(2, 0.3) (:18385). 0.3 s, still attacking (:17374): moveSpeed -3 (the recoil step back, :17384; in place here, Penguin decision 8), firePos = mPos + up + forward (:17389), fireDir = tDir - up (:17394), the aim the no-target 10 m ground point (GameGui.cs:1659; Penguin decision 1); mission / arena only (mGameType <= 4 skips the whole shot :17451, kept as the Sheep / Penguin precedent); Bouncing Bullet #401 on (:17459): Sounds/nAttack PlayOneShot (:17471-17483; the bouncingBullet prefab has no AudioSource, probe_summary.txt), bounceRange 20 + 5 x Combo 4 = 40 (:17512), the loop IL_F77 (:18075-18378): segment 1 bouncingBullet at firePos, LookRotation(fireDir) (:18097-18109) = [5.711, 0, 0] from (0, 1, 1); Physics.Raycast on layer 1 (Default, :17497, :18123), which the ground is on (Math.cs:1102-1105), meets the floor at (0, 0, 11) (geom.txt): bouncingBullet_hit there with the hero's rotation (LookRotation(forward) :18135-18147), bounceMagnitude int 10.05 = 10, bounceRange 30 (:18161-18171); RaycastAll over the hero layers (130816 - own, :18197) along those 10 m meets the standard target body (Bat decision 4: the CharacterController capsule, centre 0.6 m up, height 1, radius 0.3) on its lower cap at (0, 0.106, 9.941), 8.985 m out, a graze 1.5 mm inside the radius (checks/fx_rabbit_research/verify/verify.txt): RPC_snipeShot_hit with Snipe Mastery #431 (:18265-18271), whose prefab Effects/snipeShot_hit is in neither BB's container nor TTO's catalog (container.txt; probe_tto_err.txt): Cannot find snipeShot_hit Effect (:11435-11467), nothing drawn; the hit with Hyper Shot 4 and Snipe Mastery's raw distance (the flat 9.94 m x 4 = 39 > 0, :18230-18253, :18319-18325) sets isHyperShot; bounceCount 1 at the hit, not a bounce (:18331); the floor's reflection (Vector3.Reflect :18365-18370), WaitForFixedUpdate (:18393, 0.02 s nominal): segment 2 bouncingBullet at (0, 0, 11) rot [-5.711, 0, 0] at 0.32 s (range 30 > 12 :18082), no wall above (bounceCount = 9 :18179); the next fixed step (0.34 s) leaves the loop (:18076, :18378) for IL_14D7 (:17924): HyperShot message (GUI), the voice nAttack2 (not isBouncingBullet :17937, isHyperShot :18006; load :18051, PlayOneShot :18395); Yield(4, 0.15) (:18389) moveSpeed 0 at 0.49 s, Yield(5, 0.34) (:18391) standby at 0.83 s (:17729-17752). RPC_shotgun ($RPC_shotgun$27317, :36172-36527): at 0 attack, timeout 1.5, LookAt, animation.Play(nAttack) with no Rewind, Once (:36474-36495), no voice anywhere in it (TTO1102 Rabbit.<RPC_shotgun>d__229 :20992-21569 the same); Yield(2, 0.3) (:36525); 0.3 s moveSpeed -3 (:36200), shotgun_fire at position + TransformDirection(0, 1, 1) with the hero's rotation (:36205-36223; its AudioSource plays shotgun), Damage.FindRecTarget's box from position + forward, 12 m long, half-width 1.5 -> 4 m (sLv 2, :36270) holds the target at 10 m: RPC_shotgun_hit at the target's transform.position + up = (0, 1, 10) with the hero's rotation (:36354; :11044-11067); standby at 0.79 s (Yield 0.15 :36518, 0.34 :36520, :36409-36432). Both take worn / notWorn rabbitShotgun on R (Rabbit weapons mount on mount_Hand_R, data/rabbit/props_weapons.json)",
    "cues": [
      [0, "voice", "nAttack1", {"notWorn": ["R", "rabbitShotgun"]}],
      [0.3, "sound", "nAttack", {"notWorn": ["R", "rabbitShotgun"]}],
      [0.3, "fx", "bouncingBullet", {"y": 1, "d": 1, "rot": [5.711, 0, 0], "notWorn": ["R", "rabbitShotgun"]}],
      [0.3, "fx", "bouncingBullet_hit", {"d": 11, "notWorn": ["R", "rabbitShotgun"]}],
      [0.3, "fx", "shotgun_fire", {"y": 1, "d": 1, "worn": ["R", "rabbitShotgun"]}],
      [0.3, "fx", "shotgun_hit", {"y": 1, "d": 10, "worn": ["R", "rabbitShotgun"]}],
      [0.32, "fx", "bouncingBullet", {"d": 11, "rot": [-5.711, 0, 0], "notWorn": ["R", "rabbitShotgun"]}],
      [0.34, "voice", "nAttack2", {"notWorn": ["R", "rabbitShotgun"]}]
    ]
  },
  "cAttack2": {
    "why": "Rabbit.cs RPC_cAttack1 case 2 (:18617-18731) at 1.0 s, still attack / cAttack1: PlayAnimation(cAttack2, 0) cut in, Loop (:18636-18641); the own player only (:18646) gets the sniperCamera at position + TransformDirection(0, 1.05, 0.15) (:18654-18684; Transform, the Rabbit_sniperCamera script and an AudioSource deadShot, playOnAwake off, no renderer: probe_snipercam.txt) and the camera's specialTarget / FOV 60 (:18698-18715, left out as the camera effects, Cat decision 43); its OnGUI (Rabbit_sniperCamera.cs:246-468) checks every 0.1 s (:308-314) a ray along its forward, the hero's with no mouse (Rabbit.cs:18762-18816): at y 1.05 it meets the target body's head zone (1.05 - 0.6 > 0.5 x 0.5, Rabbit_sniperCamera.cs:357; geom.txt), Dead Shot #411 on (hasDeadShot :266, :335): mDeadShotTimer = now at the first check (:363-369), and at the next check, more than 0.1 s and under 1 s later (:381-387), audio.Play() = sounds/deadShot (:375-393) once (Loop off): 0.1 s, the nominal interval (Mole decision 45); the crosshair GUI and the Dead Shot bar (:246-305, :479-510) are screen UI, left out; held 4 s (the SEQ's full charge: Dead Shot's x3 at clamp(t, 0, 4) = 4, Rabbit.cs:19486, Rabbit_sniperCamera.cs:500), released at 5.0 s; the sound is the scope's own AudioSource (sounds/deadShot.wav, 4.919 s, Loop off), so it stops when RPC_cAttack2 destroys the scope 0.2 s after the release (Destroy(ltvEXdf3pV) :19254, Yield(2, 0.2) :19781): 5.2 - 1.1 = 4.1 s after it starts, kill 4.1 (the sound cue's kill, a page part)",
    "cues": [
      [0.1, "sound", "deadShot", {"kill": 4.1}]
    ]
  },
  "cAttack3": {
    "why": "Rabbit.cs doReleaseCharge (:9254-9353): attack / cAttack1, a mission / arena and the sniperCamera alive (:9297-9303) -> RPC_cAttack2 along the camera's flat forward (:9309; else RPC_cAttack0's cancel :9330, a CrossFade to root, no effect :19960-20060). RPC_cAttack2 ($RPC_cAttack2$26869, :19187-19785): at 0 attack, myCommand cAttack2, LookAt, PlayAnimation(cAttack3, 0) cut in, Once (:19300-19321), moveSpeed -2 (:19327; in place here), cAttack_fire at position + up with LookRotation(the camera's forward = the hero's) (:19330-19366; its own AudioSource plays nAttack, LineEmitter 2 m ahead); the own client's ray from the camera (hero + (0, 1.05, 0.15)) along its forward, 20 + 5 x Combo 4 = 40 m (:19380-19392), meets the standard target body (Bat decision 4: the CharacterController capsule, centre 0.6 m up, height 1, radius 0.3) on its upper cap at (0, 1.05, 9.834) (checks/fx_rabbit_research/verify/verify.txt; still the head zone, 1.05 - 0.6 = 0.45 > 0.5 x 0.5, :19434): RPC_cAttack_hit there with LookRotation(hero forward) (:19398; :9378-9401); the head zone (:19434) and Dead Shot 3 x (:19445-19486, the timer set at 1.0 s, 4 s on the head) give Dead Shot! (GUI, :19529-19535) and the voice headShot (pvoice, own or a mission teammate :19540-19562; load :19575, PlayOneShot :19587); Yield(2, 0.2) (:19781): moveSpeed 0, the camera destroyed (:19217-19254); Yield(3, 0.5) (:19779): standby at 0.7 s (:19257-19275)",
    "cues": [
      [0, "fx", "cAttack_fire", {"y": 1}],
      [0, "fx", "cAttack_hit", {"y": 1.05, "d": 9.83}],
      [0, "voice", "headShot"]
    ]
  }
```
