<!-- Saved by the lead from the researcher's returned text (2026-11-13): its Write was refused. -->

Summary: 11 clips, 20 coroutines, 23 tiles.
- **Pools:**
  - `mine`: Landmine, Stun Mine, Time Nuke, Flame Carnival.
  - `mortarShot`: Mortar Shot, Napalm.
  - `punch`: Mega Punch, Mega Drill.
  - `tnt`: TNT 1-4.
  - `warFactory`: one skill whose five weapons come in a fixed order, not at random. I propose `"order": "cycle"`.
- **Parts to build:** ballistic shells (Mole_mortarShot, Mole_napalm, Mole_stunGrenade, Mole_grenadeCluster), Mole_missile (homing), Mole_bazooka, Mole_cartBomb, and Mole_timeNuke's countdown label.
- **Data-only scripts:** Mole_mine, Mole_stunMine, Mole_flameCarnival.
- **New LAYOUTS:** proved byte-exact by an in-memory probe.
- **Shuriken grafts from TTO:** napalm_ring and bazooka_ring.
- **Missing sound:** megaDrill_ring's `gallonDrill` exists only as an .ogg outside Resources.
- **Possible Bible findings:** Mortar Shot fires every 0.2 s, not 0.1 s; Grenade Cluster has no voice and no ring in BB, and no ring in TTO; Stun Grenade's blast is `nAttack_hit`.

---

# Mole effects + sounds research: skill clips, second half (skills_b)

Scope: the clips grenade, grenadeCluster, hammer, mine, missile, mortarShot, punch, skyDrill, superDig, tnt and warFactory, and every skill that plays them (`pipeline/clip_calls.js`): 20 coroutines, 23 tiles. Research only (recipe steps 1-3).

- Line numbers are `D:\12tails\DecompiledSource\Mole.cs` unless another file is named.
- Times are seconds from the start of the clip the entry is keyed by. Distance 0 = at the hero.
- Max rank, passives on: Landmine 4, Stun Mine 2, Time Nuke 2, Mortar Shot 2, TNT 1-4, Stun Grenade 2, Mega Punch 2, Mega Hammer 2, Missile 4, Sky Drill 2 with Sky Shaker #413, Speed Drill 2, Charge Attack 3, Super Dig #411, Super TNT #422, Mega Drill #433, Grenade Cluster #432, Mine Lover #402.

Read-only probes, in `checks\fx_mole_research\skills_b\`:
- `flow.js` prints a coroutine's lines with the junk predicates and lone braces dropped. Its outputs are `RPC_<name>.txt`, `.r.txt` (gotos kept) and `.short.txt`.
- `probe.json` / `probe_compact.txt`: `wardrobe_fx.py mole --probe` on 44 effects.
- `probe2.py` -> `probe2.json`: the six prefabs whose scripts have no layout (mine4, stunMine2, timeNuke2, missile_fire, stunGrenade, flameCarnival_fire). They go through `wardrobe_fx.effect()` with the layouts added in memory only. Every one decodes exactly: effect()'s self-check passes.
- `probe_fields.py` -> `probe_fields.txt`: the hero prefab's Mole fields in order. They are missileBase, missile_fire, missile_hit, nAttack_fireFx (= the AudioClip nAttack_fire) and skyDrill_hit (= the prefab chopper_hit).
- `tto_probe.json`: `wardrobe_fx_tto.py mole --probe napalm_ring,bazooka_ring`. TTO's copies decode their Shuriken.
- `calc.py` -> `calc.txt`: launch rotations and flights (getMortarVector, getTrajectoryVector, rotateH, the missiles' homing), with Physics.gravity -9.8 at 50 Hz.
- `pool.py` -> `pool.json` / `pool_pretty.txt`: the entries below. It checks valid JSON, cue times in order, and kinds fx / voice / sound only.

## Read this first

1. **Pools.**
   - Four of the eleven clips are shared:
     - `mine`: Landmine, Stun Mine, Time Nuke, Flame Carnival.
     - `mortarShot`: Mortar Shot, Napalm.
     - `punch`: Mega Punch, Mega Drill.
     - `warFactory`: one skill, five weapons in turn.
   - `tnt` is played by four casts, TNT 1-4 (#221-224). Each has its own key and cooldown (:26180, doSkill :4312-4366).
   - The other six clips have one skill each:
     - grenade = Stun Grenade;
     - grenadeCluster = Grenade Cluster;
     - hammer = Mega Hammer;
     - missile = Missile;
     - skyDrill = Sky Drill (the charge's release);
     - superDig = the Charge Attack's dive with Super Dig on.

2. **War Factory steps, it does not roll.**
   - doSkill's counter goes 1 -> 5 and wraps (:7417-7421): Saw Machine, Bazooka, Tesla Coil, Roller Machine, Cart Bomb.
   - The entry is a pool with `"order": "cycle"`: one tile, the next weapon on each play. The page needs a small addition for that (question 2).
   - Without that addition the pool falls back to five tiles.

3. **Parts to build** (none of the Mole's are built yet):
   - **Ballistic shells:** Mole_mortarShot and Mole_napalm (20 m/s), Mole_stunGrenade (15 m/s), Mole_grenadeCluster (6 m/s, with a random tilt).
     - Each uses gravity, turns along its velocity, and bursts on the floor into its hit: mortarShot_hit / napalm_hit / nAttack_hit / grenadeCluster_hit.
     - Model: the Cat's `trajectoryVector` and its gravity stepping (`fxparts/cat.js`). getMortarVector (Math.cs:1011-1060) is new.
   - **Mole_missile:** 8 m/s; turns toward its target by up to 0.3 rad every 0.2 s.
   - **Mole_bazooka:** 24 m/s straight; stops on the target's body.
   - **Mole_cartBomb:** the hero's code drives it at 6 m/s; it blows up 3 s after its Init.
   - **Mole_timeNuke:** the OnGUI countdown 60, 59 ... in the GMO24 font, colour (0.8, 0.3, 0.3), 1.0 m above the nuke.
   - **Data-only:** Mole_mine, Mole_stunMine, Mole_flameCarnival. They run gameplay and draw nothing for the owner.
   - **LAYOUTS in wardrobe_fx.py**, proved by probe2:
     - Mole_mine / Mole_stunMine / Mole_stunGrenade: `[("mLv", "i")]`.
     - Mole_timeNuke: `[("mLv", "i"), ("isVisible", "b"), ("timeNuke_explosion", "r")]`.
     - Mole_missile: `[("mTarget", "r")]`.
     - rotationControl, if ever needed: `[("mRotation_x", "f"), ("mRotation_y", "f"), ("mRotation_z", "f"), ("useWorldRotation", "b")]`.
   - **SHURIKEN_FROM_TTO** for `napalm_ring` and `bazooka_ring`.
     - BB's ParticleSystem nodes have no readable fields; TTO's copies decode them.
     - The materials are tto_Bomb1_a for napalm_ring and tto_Cloud1 for bazooka_ring.
     - SHURIKEN_MAT holds one material per class today, so it needs a per-effect form here.
     - The node order differs: bazooka_ring's ParticleSystem is node 7 in BB and node 1 in TTO.
   - **One sound:** megaDrill_ring's AudioSource clip `gallonDrill` exists only as `Assets/AudioClip/gallonDrill.ogg`. That is outside Resources and not a WAV, so `rip_wav` will report it missing (question 8).

4. **Fire point.**
   - Mortar Shot, Napalm and Stun Grenade fire from the worn weapon's `firePoint` child when it has one (:24696-24712, :37106-37122, :27343-27365).
   - Otherwise they fire from TransformDirection(0.2, 1, 0.6).
   - TTO always uses the fixed point (the Bible: TTO1102 `<RPC_mortarShot>d__216`, `<RPC_napalm>d__273`).
   - The cues use the fixed point (question 3).

5. **Where things land** (decisions applied by analogy):
   - The shells burst on the floor at the 10 m target point (Sheep decision 3): Mortar Shot 4.08 s after each shot, Stun Grenade 0.64 s.
   - Napalm's five shells land at the target and at the target + world (±5, 0, ±5).
   - Missiles and Bazooka shells stop on the target's body, aimed 0.6 m up (Penguin decision 3).
   - The Cart Bomb is stopped by the target at 9.2 m (question 6).
   - The mines, the nuke and Flame Carnival never trigger: their 4 m spheres sit 9 m from the 10 m target point. They are cut at 10 s.
   - TNT n blows up 8 n m ahead, not on the target.
   - The melee weapons reach only 2-5 m, so they draw no hits: punch, hammer, drill, saw, tesla coil, roller.

6. **Grenade Cluster's voice and ring.**
   - The voice:
     - BB asks for `Voices/grenadeCluster1|2`, but the rip only has `granadeCluster1|2.wav`, so BB is silent ("Cannot find" :38201 / :38232).
     - TTO asks for grenadeCluster1|2 and its catalog has them.
     - The cue plays the rip's recordings (Sheep decision 10).
   - The ring:
     - BB loads `granadeCluster_ring`; TTO loads `grenadeCluster_ring`.
     - Neither game has either file, so neither game shows a ring.

7. **Stun Grenade's burst is the normal attack's hit.**
   - Mole_stunGrenade calls `RPC_nAttack_hit` (Mole_stunGrenade.cs:193).
   - It never calls RPC_stunGrenade_hit, whose `stunGrenade_hit` prefab exists in neither game.
   - So the entry builds `nAttack_hit`.

8. **Possible Bible findings** (offer them to the user; none changes a cue):
   - Mortar Shot's shells are 0.2 s apart (Yield(3, 0.2) :25033), not 0.1 s. The first shell comes at 0.3 s (Yield(2, 0.1) :25040 + 0.2). The reference's "0.1 s apart" (mol_mortarShot1-2) is the first wait only.
   - Grenade Cluster has no voice and no ring in BB: both are missing file names. TTO has no ring either.
   - Stun Grenade's blast effect is nAttack_hit.
   - Mega Drill has no voice.
   - Time Nuke's renderers and countdown are hidden from other teams (Mole_timeNuke.cs:74-100), as the mines' are (Mole_mine.cs:80-97).
   - The Cart Bomb has no contact fuse. It blows up only 3 s after its Init, or when the Mole's action changes (Mole_cartBomb.cs:83-130).

9. **TTO.**
   - No skill in the released list (barrelRailgun1-4, kaiserArsenal, missilePad) plays these clips; each has a clip of its own.
   - TTO's Missile runs BB's coroutine (`Mole::OldMissile`) unless the Missile Bot passive is learned; then it plays `missilePad` (TTO1102 `Mole.<RPC_missile>d__344::MoveNext`, pseudo/Mole.c:16064-16120). That belongs to the TTO report.
   - Every BB coroutine here has a TTO twin playing the same clip (pseudo/Mole.c):

     | skill(s) | line(s) |
     |---|---|
     | stunGrenade | :21221 |
     | grenadeCluster | :12260 |
     | megaHammer | :14526 |
     | mine / stunMine / timeNuke / flameCarnival | :15555 / :21615 / :22751 / :10716 |
     | mortarShot / napalm | :16638 / :18404 |
     | megaPunch / megaDrill | :15162 / :14070 |
     | skyDrill | :20512 |
     | tnt | :23151 |
     | the five War Factory weapons | :19802 / :4582 / :22246 / :19379 / :7949 |

   - BB is the authority for the cues.

## Per clip

Format: the RPC (file:line), then the timeline.
- **fx** = an effect (where / rotation);
- **voice** = a Voices/ clip;
- **sound** = a Sounds/ clip the hero's code plays.

Then: where it ends (standby), followState cuts, random picks, passives, buildability. The "why" of each entry in the JSON carries every citation.

### mine (pool: 4 members; clip 1.0 s)

| member | RPC | 0 s | 0.3 s | standby |
|---|---|---|---|---|
| mine (Landmine 4) | RPC_mine :23601-24076 | voice mine1\|mine2 (:23958) | sound mine (:23794); fx mine4 0.5 m ahead, Euler(270, 90, 0) (:24398) | 0.8 (:23830) |
| stunMine (Stun Mine 2) | RPC_stunMine :26463-26862 | voice stunMine1\|stunMine2 (:26747) | sound mine (:26583); fx stunMine2 0.5 m ahead, Euler(270, 90, 0) (:27106) | 0.8 (:26619) |
| timeNuke (Time Nuke 2) | RPC_timeNuke :30574-30954 | voice timeNuke1\|timeNuke2 (:30836) | sound mine (:30689); fx timeNuke2 1 m ahead, identity (:11687) | 0.8 (:30725) |
| flameCarnival | RPC_flameCarnival :38399-38831 | voice activate2\|mine2 (:38712) | sound mine (:38486); fx flameCarnival 1 m ahead, identity (:38518) | 0.8 (:38601) |

- **Max rank picks the prefab:** mine<sLv> (switch :24254-24398), stunMine<sLv> (:27043-27106), timeNuke<sLv> (:11624-11687).
- **Lifetimes, all cut at 10 s (`kill: 10`):**
  - mine: 60 s (chaAdjust, Mole_mine.cs:60);
  - stunMine: 60 s (talAdjust, Mole_stunMine.cs:60);
  - timeNuke: 60 s fuse (Mole_timeNuke.cs:241). Time Nuke's blast `timeNuke_explosion` (:796) therefore never comes.
  - flameCarnival: 90 s (Mole_flameCarnival.cs:53).
- **Buildable:**
  - mine4, stunMine2 and timeNuke2 are a StaticMesh plus an ImageEmitter glow (probe2).
  - flameCarnival is two StaticMeshes plus its Animation 'close' and its own Sounds/flameCarnival.
  - Parts: Mole_mine, Mole_stunMine and Mole_flameCarnival are data-only; Mole_timeNuke draws the countdown.

### mortarShot (pool: 2 members; clip 1.5 s)

- **mortarShot** (RPC_mortarShot :24470-25095):
  - 0: voice mortarShot1|mortarShot2 (:24858).
  - Five shells at 0.3 / 0.5 / 0.7 / 0.9 / 1.1 (Yield 0.1 :25040, then Yield 0.2 :25033 per shell; `a <= 2 sLv` :24927). Each shell:
    - sound nAttack_fire (:24684);
    - fx mortarShot_fire from (0.2, 1, 0.6), rot [-83.34, -1.22, 0] (LookRotation(getMortarVector(.., 20)) :10768-10771);
    - it lands at (0, 10.06) 4.08 s later as mortarShot_hit, identity (:10804-10830), so at 4.38 ... 5.18 s.
  - Standby 1.1 (:24983).
- **napalm** (RPC_napalm :37008-37504):
  - 0: voice mortarShot2, no random pick (:37419, :37456).
  - 0.3: fx napalm_ring at (0.2, 1, 0.6), hero rotation (:37146).
  - 0.3: five fx napalm, rot from calc.txt (aims :37185-37232; LookRotation(getMortarVector) :13737).
  - They land 4.04-4.10 s later as napalm_hit, rotated to the shell's flat heading (:37769).
  - Standby 0.6 (:37319).
- **Buildable:**
  - mortarShot_hit and napalm_hit are ready.
  - mortarShot_fire and napalm each need their part; the shell model and its legacy particle trail are ready.
  - napalm_ring needs the Shuriken graft.

### punch (pool: 2 members; clip 0.8 s)

- **megaPunch** (RPC_megaPunch :32324-32811):
  - 0: voice megaPunch1|megaPunch2 (:32712).
  - 0.2: fx megaPunch at the hero (:32421; followState, cut 0.6).
  - 0.3: the punch, within 3 m (:32513).
  - Standby 0.6 (:32601).
  - moveSpeed -5 at 0.2 (:32398) is a 0.5 m step back; the page leaves it out.
- **megaDrill** (RPC_megaDrill :39390-39788):
  - No voice.
  - 0.2: fx megaDrill_ring at the hero (:39483; followState, life 0.8 + 0.2, cut 1.0).
  - Four drill hits at 0.4-0.7, within 3 m (:39561-39782).
  - Standby 1.0 (:39657).
  - Its own sound is gallonDrill (see Read this first 3).
- **Buildable:** both are ready.

### tnt (pool: TNT 1-4; clip 0.8 s)

- RPC_tnt :25639-26383, with sLv = n:
  - 0: voice tnt1|tnt2 (:26230).
  - 0.2: fx tnt at the hero (:25804; followState, cut 0.8).
  - 0.5: fx superTNT_hit, identity, 8 n m ahead on the floor (getSpawnPos :25846-25893). Super TNT #422 is on (passives on); without it the hit is tnt_hit (:25910-25928).
  - 0.5: sound tnt (:25970).
  - Standby 0.8 (:26119).
- **Buildable:** both effects are ready.
- TNT 4 lands 32 m out, far beyond the 10 m point (question 1).

### grenade (Stun Grenade 2; clip 1.0 s)

- RPC_stunGrenade :27258-27660:
  - 0: voice stunGrenade1|stunGrenade2 (:27566).
  - 0.6: fx stunGrenade from (0.2, 1, 0.6), rot [-6.75, -1.22, 0] (getTrajectoryVector at speed 15, :11295-11298; Mole_stunGrenade).
  - It bursts on the floor at (0, 10.13) 0.64 s later (1.24 s) as nAttack_hit, identity (Mole_stunGrenade.cs:193, :10103-10105).
  - Standby 0.8 (:27414).
- **Buildable:** stunGrenade needs Mole_stunGrenade; nAttack_hit is ready.

### grenadeCluster (Grenade Cluster; clip 1.0 s)

- RPC_grenadeCluster :37919-38294:
  - 0: voice granadeCluster1|granadeCluster2 (TTO's fix, Read this first 6). No ring.
  - 0.5: eight fx grenadeCluster_fire from (0, 1, 0.5) + 0.5 dir (:38002-38014, :13810).
    - Each has yaw -45 i and a tilt drawn per grenade from Random.Range(3, 10).
    - They fly at 6 m/s and burst on the floor 4.8-5.6 m out, 0.66-1.04 s later, as grenadeCluster_hit, identity (:13865).
  - Standby 0.7 (:38062).
- The cue carries `"tilt": [3, 9]` for the part (fx.at). The part sets:
  - dir = normalize((0, 0.1 k, 1) turned by the yaw);
  - the root moved by 0.5 dir;
  - rotation LookRotation(dir).
- **Buildable:** grenadeCluster_fire needs Mole_grenadeCluster; grenadeCluster_hit is ready.

### hammer (Mega Hammer 2; clip 1.0 s)

- RPC_megaHammer :32938-33396:
  - 0: voice megaHammer1|megaHammer2 (:33278); fx megaHammer at the hero (:33362; followState, cut 0.7).
  - 0.4: fx assemble_dust 1.4 m ahead, hero rotation (:33042). The camera shake is left out.
  - Standby 0.7 (:33167).
- **Buildable:** all ready.

### missile (Missile 4; clip 1.0 s)

- RPC_missile :34309-34921:
  - 0: voice missile1|missile2 (:34827).
  - 0.1: sound missile_base (:34411); four fx missileBase at the hero, rot [270, 45 / 135 / 225 / 315, 0] (:34522; followState, cut 0.8).
  - 0.6: sound missile_fire (:34577); four fx missile_fire at the hero + dir, rot [-16.7, 45 / -45 / -135 / 135, 0] (:34668, :13140).
  - The missiles home on the target 0.6 m up. The front two hit at 1.78 s, the back two at 3.48 s, as missile_hit with the hero's rotation (:13208).
  - Standby 0.8 (:34716).
- **Buildable:** missileBase and missile_hit are ready; missile_fire needs Mole_missile.

### skyDrill (Sky Drill 2 + Sky Shaker; clip 1.3 s)

- RPC_skyDrill :31569-32185:
  - 0: voice skyDrill1|skyDrill2 (:31874).
  - 0: fx skyDrill at the hero, rot [270, 90, 0] (:31960; followState, life 0.55).
  - 0: fx skyShaker_ring at the hero (:31998), in place of skyDrill_ring.
  - The two ring hits (0.1, 0.2 s) and Sky Shaker's blow reach 5 m at most. The motion blur and shake are left out.
  - Standby 1.0 (:31743).
- **Buildable:** all ready.

### superDig (Charge Attack with Super Dig; clip 1.033 s)

- RPC_cAttack1 :21477-22504:
  - 0: voice superDig (:22383); fx dig_hole at the hero + 0.05 m up (:22446; it loops its own Sounds/dig).
  - fx superDig_dust at 0.1 / 0.3 / 0.5 (:21645-21676).
  - At 0.6 the hero's renderers go off: he is underground (:21609, :22031-22061).
  - Underground, dig_dirt comes every 0.2 s until the release. The release is Sky Drill after more than 3 s.
- **Buildable:** all ready.
- The tile keeps the clip whole and leaves the underground phase to the Charge Attack (question 5).

### warFactory (War Factory, 5 steps in turn; clip 5.0 s)

Every step opens with its voice and fx warFactory_ring at the hero (followState, life 1). The machine comes at 0.3 s.

| step | RPC | 0.3 s | later | standby |
|---|---|---|---|---|
| sawMachine | :40443-40964 | sawMachine_ring (:40531; followState) | cuts at 0.4-1.0 within 4 m | 1.3 (:40619) |
| bazooka | :41081-41536 | bazooka_ring (:41168; followState, life 2) | bazooka_fire at 0.9 / 1.2 / 1.5 from (-0.25, 1, 1), 24 m/s; bazooka_hit on the target at 9.7 m, 1 m up, 0.35 s later | 2.2 (:41256) |
| teslaCoil | :41647-42149 | teslaCoil_ring (:41735; 2.7 s) | shocks at 1.0-2.2 within 5 m | 3.0 (:41833) |
| rollerMachine | :42264-42838 | rollerMachine_ring (:42352; followState, 3.2 s) | crushes at 0.6 and 1.0-2.8 within 2 m; moveSpeed 1 (no travel) | 3.5 (:42545) |
| cartBomb | :42964-43546 | cartBomb_ring (:43051); cartBomb_fire on the floor 0.5 m ahead (:43106) | driven at 6 m/s from 0.5 s, stopped by the target at 9.2 m; cartBomb_hit at 3.3 s | about 3.5 (:43196) |

- **Buildable:**
  - Ready: warFactory_ring, sawMachine_ring, teslaCoil_ring, rollerMachine_ring, cartBomb_ring, bazooka_hit (AlphaTimer), cartBomb_hit.
  - bazooka_ring needs the Shuriken graft.
  - bazooka_fire needs Mole_bazooka.
  - cartBomb_fire needs Mole_cartBomb.

## Effects at a glance

- **Ready:** mortarShot_hit, napalm_hit, tnt, tnt_hit, superTNT_hit, nAttack_hit, grenadeCluster_hit, megaPunch, megaDrill_ring, megaHammer, assemble_dust, missileBase, missile_hit, skyDrill, skyShaker_ring, superDig_dust, dig_hole, warFactory_ring, sawMachine_ring, teslaCoil_ring, rollerMachine_ring, cartBomb_ring, cartBomb_hit, bazooka_hit.
- **Need a part:**

  | effect | part |
  |---|---|
  | mine4 | Mole_mine (data-only) |
  | stunMine2 | Mole_stunMine (data-only) |
  | flameCarnival | Mole_flameCarnival (data-only) |
  | timeNuke2 | Mole_timeNuke (the countdown) |
  | mortarShot_fire | Mole_mortarShot |
  | napalm | Mole_napalm |
  | stunGrenade | Mole_stunGrenade |
  | grenadeCluster_fire | Mole_grenadeCluster |
  | missile_fire | Mole_missile (the inventory misses it: it is a prefab field, not a Resources.Load) |
  | bazooka_fire | Mole_bazooka |
  | cartBomb_fire | Mole_cartBomb |
  | napalm_ring, bazooka_ring | the Shuriken graft from TTO |

- **Not cued:**
  - Hits that only land on a target: mine_hit, stunMine_hit, megaPunch_hit, megaDrill_hit, skyDrill_hit (= chopper_hit), sawMachine_hit, rollerMachine_hit.
  - flameCarnival_fire (rotationControl): never triggered.
  - timeNuke_explosion: comes after the 10 s cut.
  - skyDrill_ring (Sky Shaker replaces it) and tnt_hit (Super TNT replaces it).
  - granadeCluster_ring and stunGrenade_hit: in neither game.
- **Sounds:**
  - "sound" cues: mine, nAttack_fire, tnt, missile_base, missile_fire. All are in the rip's mole/sounds.
  - The effects' own AudioSources are all found by rip_wav, except gallonDrill.
  - missile_hit plays the Penguin's Sounds/manaMissile_hit; rip_wav finds it through its search anywhere in the rip.

## Paste-ready cue entries for wardrobe/fx_cues/mole.json

These are 11 keys, from `checks\fx_mole_research\skills_b\pool_pretty.txt`, checked by `pool.py`.

Cue options used beyond the page's documented ones:
- `"tilt"` on grenadeCluster_fire, for Mole_grenadeCluster;
- `"to"` on bazooka_fire and cartBomb_fire, the target body for those parts;
- `"order": "cycle"` on the warFactory pool, the page addition (question 2).

The pool members' keys become the tile names poolChains makes ("Stun Mine", "Mega Drill" ...). TNT's `tnt1` ... `tnt4` and War Factory's members have no icon or name of their own (questions 1 and 2).

```json
{
"mine": {
  "why": "The mine clip: four Mole skills, one per play, even chance, picked anew on every play (plans/fx_sheep/decisions.md 14; one tile each, poolChains): Landmine (RPC_mine, PlayAnimation(\"mine\", 0.2) Mole.cs:23917), Stun Mine (RPC_stunMine :26706), Time Nuke (RPC_timeNuke :30795), Flame Carnival (RPC_flameCarnival :38671) (pipeline/clip_calls.js); each lays its device at 0.3 s and stands by at 0.8 s; every device's trigger (4 m sphere, rip prefabs) is 9 m short of the 10 m target point: no blast",
  "skills": {
    "mine": {
      "why": "Mole.cs RPC_mine (:23601-24076), Landmine 4 (max rank; Mine Lover #402 changes only the cooldown :23891-23905): clip mine, 0.2 s fade (:23917), voice mine1 / mine2 (Random.Range(0, 2) :23958, loads :23968 / :23999, PlayOneShot :24039 / :24042) at 0; Yield 0.3 (:24045): RPC_mine_create(mPos + 0.5 tDir) (:23758) Instantiates mine<sLv> = mine4 (switch :24254-24398) with Quaternion.Euler(270, 90, 0), a world rotation (the page's hero faces +z: the same) (:24398), Init 0.3 s later (:24233); Mole_mine draws nothing of its own (it hides the renderers from other teams only, Mole_mine.cs:80-97; a data-only part) and lives chaAdjust(60) s (:60, :146): cut at 10 s (kill 10, the Sheep's seal fields); Sounds/mine (load :23782, PlayOneShot :23794); Yield 0.5 (:24037): standby 0.8 s (:23830)",
      "cues": [
        [0, "voice", "mine1|mine2"],
        [0.3, "sound", "mine"],
        [0.3, "fx", "mine4", {"d": 0.5, "rot": [270, 90, 0], "kill": 10}]
      ]
    },
    "stunMine": {
      "why": "Mole.cs RPC_stunMine (:26463-26862), Stun Mine 2: clip mine, 0.2 s fade (:26706), voice stunMine1 / stunMine2 (Random.Range(0, 2) :26747, loads :26757 / :26788, PlayOneShot :26834 / :26830) at 0; Yield 0.3 (:26832): RPC_stunMine_create(mPos + 0.5 tDir) (:26547) Instantiates stunMine2 (sLv 2, :27082-27106) with Quaternion.Euler(270, 90, 0) (:27106), Init 0.3 s later (:27019); Mole_stunMine draws nothing (hides from other teams, Mole_stunMine.cs:80-97; data-only) and lives talAdjust(60) s (:60, the Bible's BB bug): cut at 10 s; Sounds/mine (:26571, :26583); Yield 0.5 (:26823): standby 0.8 s (:26619)",
      "cues": [
        [0, "voice", "stunMine1|stunMine2"],
        [0.3, "sound", "mine"],
        [0.3, "fx", "stunMine2", {"d": 0.5, "rot": [270, 90, 0], "kill": 10}]
      ]
    },
    "timeNuke": {
      "why": "Mole.cs RPC_timeNuke (:30574-30954), Time Nuke 2: clip mine, 0.2 s fade (:30795), voice timeNuke1 / timeNuke2 (Random.Range(0, 2) :30836, loads :30846 / :30877, PlayOneShot :30922 / :30925) at 0; Yield 0.3 (:30914): RPC_timeNuke_create(mPos + tDir) (:30653): timeNuke2 (sLv 2, :11663-11687) 1 m ahead, Quaternion.identity (:11687), Init(hero) (:11711); Mole_timeNuke draws the fuse's countdown over it: OnGUI label FloorToInt(start + 60 - now) (60, 59 ...) in GameGui/Fonts/GMO24, colour (0.8, 0.3, 0.3), centred in 30 x 30 px at the nuke + (0.2 mLv + 0.6) = 1.0 m up (mLv 2 in the prefab, checks/fx_mole_research/skills_b/probe2.json) (Mole_timeNuke.cs:62-68, :142-175; the part to build); the fuse is 60 s (:241, :276): cut at 10 s, so its blast timeNuke_explosion (:796) never comes; Sounds/mine (:30677, :30689); Yield 0.5 (:30920): standby 0.8 s (:30725)",
      "cues": [
        [0, "voice", "timeNuke1|timeNuke2"],
        [0.3, "sound", "mine"],
        [0.3, "fx", "timeNuke2", {"d": 1, "kill": 10}]
      ]
    },
    "flameCarnival": {
      "why": "Mole.cs RPC_flameCarnival (:38399-38831): clip mine, 0.2 s fade (:38671), voice activate2 / mine2 (Random.Range(0, 2) :38712, loads :38722 / :38753, PlayOneShot :38804 / :38787) at 0; Yield 0.3 (:38794): Sounds/mine (:38474-38486) and flameCarnival Instantiated 1 m ahead (mPos + tDir), Quaternion.identity (:38518), InitFlameCarnival (:38559); its Animation plays 'close' on awake and its AudioSource Sounds/flameCarnival (probe); Mole_flameCarnival lives chaAdjust(90) s (Mole_flameCarnival.cs:53), hides from other teams (:80-93) and fires flameCarnival_fire only when an enemy walks into its 4 m trigger (OnTriggerEnter :198-280; the 10 m target is 9 m away: never): data-only, cut at 10 s; Yield 0.5 (:38807): standby 0.8 s (:38601)",
      "cues": [
        [0, "voice", "activate2|mine2"],
        [0.3, "sound", "mine"],
        [0.3, "fx", "flameCarnival", {"d": 1, "kill": 10}]
      ]
    }
  }
},
"mortarShot": {
  "why": "The mortarShot clip: Mortar Shot (RPC_mortarShot, PlayAnimation(\"mortarShot\", 0.2) Mole.cs:24807) and Napalm (RPC_napalm :37401), one per play, even chance, picked anew on every play (one tile each, poolChains); both fire from the fixed point TransformDirection(0.2, 1, 0.6) (the weapon's firePoint is BB's first choice, :24696-24712, :37106-37122; TTO always uses the fixed point: question 3)",
  "skills": {
    "mortarShot": {
      "why": "Mole.cs RPC_mortarShot (:24470-25095), Mortar Shot 2: aimed at the target's position (:24761-24772: the 10 m target point); clip, 0.2 s fade (:24807), voice mortarShot1 / mortarShot2 (Random.Range(0, 2) :24858, loads :24870 / :24902, PlayOneShot :25035 / :25042) at 0; Yield 0.1 (:25040), then 2 sLv + 1 = 5 shells (a <= 2 sLv :24927), each after Yield 0.2 (:25033): 0.3, 0.5, 0.7, 0.9, 1.1 s (the Bible's '0.1 s apart' is the first wait only: question 7); each shell: the weapon's 'fire' clip (:24666-24671, not on the page), Sounds/nAttack_fire (the hero prefab's field nAttack_fireFx, :24684; probe_fields.txt), RPC_mortarShot_fire (:24728): mortarShot_fire with LookRotation(getMortarVector(firePos, target, 20)) (:10768-10771; Math.cs:1011-1060: 83.34 deg up, calc.txt), life 5 x rangeMod (:10780); Mole_mortarShot: 20 m/s (Mole_mortarShot.cs:26, :51), Rigidbody gravity on, drag 0 (rip prefab; Physics.gravity -9.8), LookAt(position + velocity) every FixedUpdate (:86), bursts on the first collider not its own layer / 1 / 2 (OnTriggerEnter :98-171): RPC_mortarShot_hit = mortarShot_hit at the contact, identity (:10804-10830; its own Sounds/nAttack_hit): on the floor at the 10 m point (0, 10.06 m) 4.08 s after each shot (plans/fx_sheep/decisions.md 3; the part spawns it: builds); standby at 1.1 s (:24983)",
      "builds": ["mortarShot_hit"],
      "cues": [
        [0, "voice", "mortarShot1|mortarShot2"],
        [0.3, "sound", "nAttack_fire"],
        [0.3, "fx", "mortarShot_fire", {"x": 0.2, "y": 1, "d": 0.6, "rot": [-83.34, -1.22, 0]}],
        [0.5, "sound", "nAttack_fire"],
        [0.5, "fx", "mortarShot_fire", {"x": 0.2, "y": 1, "d": 0.6, "rot": [-83.34, -1.22, 0]}],
        [0.7, "sound", "nAttack_fire"],
        [0.7, "fx", "mortarShot_fire", {"x": 0.2, "y": 1, "d": 0.6, "rot": [-83.34, -1.22, 0]}],
        [0.9, "sound", "nAttack_fire"],
        [0.9, "fx", "mortarShot_fire", {"x": 0.2, "y": 1, "d": 0.6, "rot": [-83.34, -1.22, 0]}],
        [1.1, "sound", "nAttack_fire"],
        [1.1, "fx", "mortarShot_fire", {"x": 0.2, "y": 1, "d": 0.6, "rot": [-83.34, -1.22, 0]}]
      ]
    },
    "napalm": {
      "why": "Mole.cs RPC_napalm (:37008-37504): aimed at the target (:37371-37380: the 10 m target point); clip mortarShot, 0.2 s fade (:37401), voice mortarShot2 always (load :37419, PlayOneShot :37456: no pick, no voice-setting check) at 0; Yield 0.3 (:37454): the weapon's 'fire' clip (:37094-37099), napalm_ring createEffect at the fire point, hero rotation (:37128-37146; plays its own Sounds/napalm_ring; its Shuriken from TTO's copy, SHURIKEN_FROM_TTO), and 5 shells at once (i < 5 :37173) aimed at the target and the target + world (-5, 0, -5), (-5, 0, 5), (5, 0, -5), (5, 0, 5) (:37185-37232): RPC_napalm_fire (:37238): napalm with LookRotation(getMortarVector(firePos, aim, 20)) (:13737-13740), life 5 x rangeMod (:13749); Mole_napalm: 20 m/s (Mole_napalm.cs:26, :51), gravity, bursts on contact (OnTriggerEnter :98-179): RPC_napalm_hit = napalm_hit at the contact, LookRotation(the shell's flat forward) (:37757-37769; EffectControl 3 + 3 s, its own Sounds/napalm_hit): on the floor 4.04-4.10 s after, at (0, 10.06), (-5.04, 5.04), (-5.04, 15.12), (5.04, 5.03), (5.04, 15.12) m (calc.txt; builds); Yield 0.3 (:37459): standby 0.6 s (:37319)",
      "builds": ["napalm_hit"],
      "cues": [
        [0, "voice", "mortarShot2"],
        [0.3, "fx", "napalm_ring", {"x": 0.2, "y": 1, "d": 0.6}],
        [0.3, "fx", "napalm", {"x": 0.2, "y": 1, "d": 0.6, "rot": [-83.34, -1.22, 0]}],
        [0.3, "fx", "napalm", {"x": 0.2, "y": 1, "d": 0.6, "rot": [-85.2, -49.76, 0]}],
        [0.3, "fx", "napalm", {"x": 0.2, "y": 1, "d": 0.6, "rot": [-78.98, -19.86, 0]}],
        [0.3, "fx", "napalm", {"x": 0.2, "y": 1, "d": 0.6, "rot": [-85.41, 47.49, 0]}],
        [0.3, "fx", "napalm", {"x": 0.2, "y": 1, "d": 0.6, "rot": [-79.08, 18.43, 0]}]
      ]
    }
  }
},
"punch": {
  "why": "The punch clip: Mega Punch (RPC_megaPunch, PlayAnimation(\"punch\", 0.2) Mole.cs:32671) and Mega Drill (RPC_megaDrill :39739), one per play, even chance, picked anew on every play (one tile each, poolChains); both punch within 3 m (FindRecTarget :32513, :39563): no hit at the 10 m target point (the Bison's decision 16)",
  "skills": {
    "megaPunch": {
      "why": "Mole.cs RPC_megaPunch (:32324-32811), Mega Punch 2 (Mega Drill #433's passive part only raises damage and KO, :32488-32499): clip, 0.2 s fade (:32671), voice megaPunch1 / megaPunch2 (Random.Range(0, 2) :32712, loads :32722 / :32753, PlayOneShot :32792 / :32795) at 0; Yield 0.2 (:32798): moveSpeed -5 (:32398: a 0.5 m step back over 0.1 s; the page's hero doesn't travel, the Bison's decision 17) and megaPunch createEffect at the hero, hero rotation (:32403-32421; followPosition + followState; plays its own Sounds/megaPunch); Yield 0.1 (:32810): the punch, megaPunch_hit only on a target hit within 3 m (:32513-32552, :13062-13085); Yield 0.3 (:32788): standby 0.6 s (:32601): megaPunch's cut",
      "cues": [
        [0, "voice", "megaPunch1|megaPunch2"],
        [0.2, "fx", "megaPunch", {"cut": 0.6}]
      ]
    },
    "megaDrill": {
      "why": "Mole.cs RPC_megaDrill (:39390-39788), no voice (none loaded): clip punch, 0.2 s fade (:39739); Yield 0.2 (:39776): moveSpeed -5 (:39460; no travel) and megaDrill_ring createEffect at the hero, hero rotation (:39465-39483; followPosition + followState, EffectControl 0.8 + 0.2 s; its AudioSource's clip gallonDrill is only in the rip's Assets/AudioClip/gallonDrill.ogg: question 8); Yield 0.1 (:39774): moveSpeed 0, four drill hits 0.1 s apart from 0.4 s (i < 4 :39761, Yield 0.1 :39782) within 3 m (:39563), megaDrill_hit only on a target (:39592-39602, :13906-13929); Yield 0.3 (:39778): standby 1.0 s (:39657)",
      "cues": [
        [0.2, "fx", "megaDrill_ring", {"cut": 1.0}]
      ]
    }
  }
},
"tnt": {
  "why": "The tnt clip: TNT 1-4 (#221-224) are four casts the Mole has together at max rank, each with its own key and cooldown (Mole.cs:26180, doSkill :4312-4366; Bible mole-skill-reference 'TNT is four separate casts'): one tile each (question 1), each throwing 8 x n m ahead (:25846)",
  "skills": {
    "tnt1": {
      "why": "Mole.cs RPC_tnt (:25639-26383) with sLv 1: TNT 1 (#221), its own key and cooldown \"tnt1\" (:26180; doSkill :4312): clip tnt, 0.2 s fade (:26189), voice tnt1 / tnt2 (Random.Range(0, 2) :26230, loads :26240 / :26271, PlayOneShot :26305 / :26320) at 0; Yield 0.2 (:26311): tnt createEffect at the hero, hero rotation (:25786-25804; the bundle in hand, followPosition + followState: cut at the standby); Yield 0.3 (:26314): at 0.5 s the blast at getSpawnPos(mPos + 8 sLv forward) = 8 m ahead on the ground (:25846-25857; Math.cs getSpawnPos: the floor below), Super TNT #422 on (passives on, :25841): superTNT_hit, Quaternion.identity (:25869-25893; without it tnt_hit, :25910-25928), playing its own Sounds/superTNT_hit; Sounds/tnt, the owner's (:25944-25970); Yield 0.3 (:26326): standby 0.8 s (:26119)",
      "cues": [
        [0, "voice", "tnt1|tnt2"],
        [0.2, "fx", "tnt", {"cut": 0.8}],
        [0.5, "fx", "superTNT_hit", {"d": 8}],
        [0.5, "sound", "tnt"]
      ]
    },
    "tnt2": {
      "why": "Mole.cs RPC_tnt (:25639-26383) with sLv 2: TNT 2 (#222), its own key and cooldown \"tnt2\" (:26180; doSkill :4330): clip tnt, 0.2 s fade (:26189), voice tnt1 / tnt2 (Random.Range(0, 2) :26230, loads :26240 / :26271, PlayOneShot :26305 / :26320) at 0; Yield 0.2 (:26311): tnt createEffect at the hero, hero rotation (:25786-25804; the bundle in hand, followPosition + followState: cut at the standby); Yield 0.3 (:26314): at 0.5 s the blast at getSpawnPos(mPos + 8 sLv forward) = 16 m ahead on the ground (:25846-25857; Math.cs getSpawnPos: the floor below), Super TNT #422 on (passives on, :25841): superTNT_hit, Quaternion.identity (:25869-25893; without it tnt_hit, :25910-25928), playing its own Sounds/superTNT_hit; Sounds/tnt, the owner's (:25944-25970); Yield 0.3 (:26326): standby 0.8 s (:26119)",
      "cues": [
        [0, "voice", "tnt1|tnt2"],
        [0.2, "fx", "tnt", {"cut": 0.8}],
        [0.5, "fx", "superTNT_hit", {"d": 16}],
        [0.5, "sound", "tnt"]
      ]
    },
    "tnt3": {
      "why": "Mole.cs RPC_tnt (:25639-26383) with sLv 3: TNT 3 (#223), its own key and cooldown \"tnt3\" (:26180; doSkill :4348): clip tnt, 0.2 s fade (:26189), voice tnt1 / tnt2 (Random.Range(0, 2) :26230, loads :26240 / :26271, PlayOneShot :26305 / :26320) at 0; Yield 0.2 (:26311): tnt createEffect at the hero, hero rotation (:25786-25804; the bundle in hand, followPosition + followState: cut at the standby); Yield 0.3 (:26314): at 0.5 s the blast at getSpawnPos(mPos + 8 sLv forward) = 24 m ahead on the ground (:25846-25857; Math.cs getSpawnPos: the floor below), Super TNT #422 on (passives on, :25841): superTNT_hit, Quaternion.identity (:25869-25893; without it tnt_hit, :25910-25928), playing its own Sounds/superTNT_hit; Sounds/tnt, the owner's (:25944-25970); Yield 0.3 (:26326): standby 0.8 s (:26119)",
      "cues": [
        [0, "voice", "tnt1|tnt2"],
        [0.2, "fx", "tnt", {"cut": 0.8}],
        [0.5, "fx", "superTNT_hit", {"d": 24}],
        [0.5, "sound", "tnt"]
      ]
    },
    "tnt4": {
      "why": "Mole.cs RPC_tnt (:25639-26383) with sLv 4: TNT 4 (#224), its own key and cooldown \"tnt4\" (:26180; doSkill :4366): clip tnt, 0.2 s fade (:26189), voice tnt1 / tnt2 (Random.Range(0, 2) :26230, loads :26240 / :26271, PlayOneShot :26305 / :26320) at 0; Yield 0.2 (:26311): tnt createEffect at the hero, hero rotation (:25786-25804; the bundle in hand, followPosition + followState: cut at the standby); Yield 0.3 (:26314): at 0.5 s the blast at getSpawnPos(mPos + 8 sLv forward) = 32 m ahead on the ground (:25846-25857; Math.cs getSpawnPos: the floor below), Super TNT #422 on (passives on, :25841): superTNT_hit, Quaternion.identity (:25869-25893; without it tnt_hit, :25910-25928), playing its own Sounds/superTNT_hit; Sounds/tnt, the owner's (:25944-25970); Yield 0.3 (:26326): standby 0.8 s (:26119)",
      "cues": [
        [0, "voice", "tnt1|tnt2"],
        [0.2, "fx", "tnt", {"cut": 0.8}],
        [0.5, "fx", "superTNT_hit", {"d": 32}],
        [0.5, "sound", "tnt"]
      ]
    }
  }
},
"grenade": {
  "why": "Mole.cs RPC_stunGrenade (:27258-27660), Stun Grenade 2, the only skill on the grenade clip: aimed at the target's position, else 12 m ahead (:27466-27501: the 10 m target point); clip, 0.2 s fade (:27525), voice stunGrenade1 / stunGrenade2 (Random.Range(0, 2) :27566, loads :27576 / :27607, PlayOneShot :27653 / :27656) at 0; Yield 0.6 (:27647): from the fixed fire point (:27343-27365; question 3) toward the target's feet (:27370), RPC_stunGrenade_fire (:27375): stunGrenade with LookRotation(getTrajectoryVector(firePos, target, 15)) (:11295-11298; 6.75 deg up, calc.txt), life 3 x rangeMod (:11307), mLv = sLv + Grenade Cluster #432 (:11319, gameplay only); Mole_stunGrenade: 15 m/s (Mole_stunGrenade.cs:28, :57), gravity, LookAt(velocity) (:92), bursts on contact (OnTriggerEnter :104-193) with RPC_nAttack_hit (:193; not RPC_stunGrenade_hit, whose stunGrenade_hit is in neither game's files): nAttack_hit at the contact, identity (Mole.cs:10103-10105; its own Sounds/nAttack_hit), on the floor at the 10 m point (0, 10.13 m) 0.64 s after the throw (plans/fx_sheep/decisions.md 3; builds); Yield 0.2 (:27651): standby 0.8 s (:27414)",
  "builds": ["nAttack_hit"],
  "cues": [
    [0, "voice", "stunGrenade1|stunGrenade2"],
    [0.6, "fx", "stunGrenade", {"x": 0.2, "y": 1, "d": 0.6, "rot": [-6.75, -1.22, 0]}]
  ]
},
"grenadeCluster": {
  "why": "Mole.cs RPC_grenadeCluster (:37919-38294), Grenade Cluster (one rank), the only skill on its clip: clip, 0.2 s fade (:38132); the voice: BB asks for Voices/grenadeCluster1 / grenadeCluster2 (Random.Range(0, 2) :38173, loads :38185 / :38216), which BB doesn't have ('Cannot find' :38201 / :38232; the rip has granadeCluster1 / 2.wav); TTO plays grenadeCluster1 / 2, in its catalog (TTO1102:Mole.<RPC_grenadeCluster>d__276::MoveNext, pseudo/Mole.c:12058-12066): TTO's fix, BB's recordings (plans/fx_sheep/decisions.md 10; question 4); its ring Effects/granadeCluster_ring (:38241-38257) is in neither game's files (BB 'Cannot find' :38266, TTO's grenadeCluster_ring not in its catalog): none; Yield 0.5 (:38287): 8 grenades (i < 8 :38002) from position + TransformDirection(0, 1, 0.5) (:38004), each dir = rotateH(forward + 0.1 Random.Range(3, 10) up, 45 i).normalized (:38009; rotateH turns +z toward -x, Math.cs:838-843, so Unity yaw -45 i; the int 3 ... 9 drawn per grenade: 16.7 ... 42.0 deg up, the part's tilt), RPC_grenadeCluster_fire (:38014): grenadeCluster_fire at firePos + 0.5 dir, LookRotation(dir) (:13810), life 5 x rangeMod (:13819); Mole_grenadeCluster: 6 m/s (Mole_grenadeCluster.cs:28, :53), gravity, LookAt(velocity) (:88), bursts on contact (OnTriggerEnter :100-184): grenadeCluster_hit at the contact, LookRotation(zero) = identity (:13865; its own Sounds/grenade_hit), on the floor 4.8 ... 5.6 m out 0.66 ... 1.04 s after the throw (calc.txt; builds); Yield 0.2 (:38291): standby 0.7 s (:38062)",
  "builds": ["grenadeCluster_hit"],
  "cues": [
    [0, "voice", "granadeCluster1|granadeCluster2"],
    [0.5, "fx", "grenadeCluster_fire", {"y": 1, "d": 0.5, "rot": [0, 0, 0], "tilt": [3, 9]}],
    [0.5, "fx", "grenadeCluster_fire", {"y": 1, "d": 0.5, "rot": [0, 315, 0], "tilt": [3, 9]}],
    [0.5, "fx", "grenadeCluster_fire", {"y": 1, "d": 0.5, "rot": [0, 270, 0], "tilt": [3, 9]}],
    [0.5, "fx", "grenadeCluster_fire", {"y": 1, "d": 0.5, "rot": [0, 225, 0], "tilt": [3, 9]}],
    [0.5, "fx", "grenadeCluster_fire", {"y": 1, "d": 0.5, "rot": [0, 180, 0], "tilt": [3, 9]}],
    [0.5, "fx", "grenadeCluster_fire", {"y": 1, "d": 0.5, "rot": [0, 135, 0], "tilt": [3, 9]}],
    [0.5, "fx", "grenadeCluster_fire", {"y": 1, "d": 0.5, "rot": [0, 90, 0], "tilt": [3, 9]}],
    [0.5, "fx", "grenadeCluster_fire", {"y": 1, "d": 0.5, "rot": [0, 45, 0], "tilt": [3, 9]}]
  ]
},
"hammer": {
  "why": "Mole.cs RPC_megaHammer (:32938-33396), Mega Hammer 2, the only skill on the hammer clip (Mega Drill #433 raises only damage and KO, :33081-33092): clip, 0.2 s fade (:33237), voice megaHammer1 / megaHammer2 (Random.Range(0, 2) :33278, loads :33290 / :33321, PlayOneShot :33302 / :33333) and megaHammer createEffect at the hero, hero rotation (:33346-33362; followPosition + followState; plays its own Sounds/megaHammer) at 0; Yield 0.4 (:33395): the camera shake (:33018, left out: the Bison's decision 35), assemble_dust Instantiated 1.4 m ahead, hero rotation (:33024-33042), the blow within 3 m (FindRecTarget :33106: nothing at 10 m); Yield 0.3 (:33390): standby 0.7 s (:33167): megaHammer's cut",
  "cues": [
    [0, "voice", "megaHammer1|megaHammer2"],
    [0, "fx", "megaHammer", {"cut": 0.7}],
    [0.4, "fx", "assemble_dust", {"d": 1.4}]
  ]
},
"missile": {
  "why": "Mole.cs RPC_missile (:34309-34921), Missile 4, the only BB skill on the missile clip (TTO's OldMissile is the same, TTO1102:Mole::RPC_missile without the Missile Bot passive, pseudo/Mole.c:16064-16076): clip cut (:34786), voice missile1 / missile2 (Random.Range(0, 2) :34827, loads :34837 / :34868, PlayOneShot :34918 / :34905) at 0; Yield 0.1 (:34920): Sounds/missile_base (:34399, :34411) and sLv = 4 launchers (start -45, step 90 at rank 4, :34481-34492): missileBase createEffect at the hero, rotation x Euler(270, 90 - 45 + 90 b, 0) (:34515-34522; the hero prefab's field missileBase, probe_fields.txt; followPosition + followState, life 0.8: cut at the standby); Yield 0.5 (:34912): Sounds/missile_fire (:34565, :34577), 4 missiles (i < sLv :34614), each locked on a random enemy within 32 m (:34604-34656: the one target), dir = rotateH(forward + 0.3 up, -45 + 90 i).normalized (:34668: Unity yaw 45, -45, -135, 135, 16.7 deg up), RPC_missile_fire (:34673): the field missile_fire at the hero + dir, LookRotation(dir) (:13140), life 5 x rangeMod (:13149), mTarget (:13189); Mole_missile: ProjectileControl.velocity (0, 0, 8) (probe2.json), no gravity (rip prefab), RotateTowards(forward, the target's bounds centre - position, 0.3 rad) every 0.2 s (Mole_missile.cs:157-162; aimed 0.6 m up, plans/fx_penguin/decisions.md 3), missile_hit with the hero's rotation where it touches anything not on its layer / 1 / 2 (OnTriggerEnter :188-290, Mole.cs:13206-13208) or where its life runs out (Update :46-118); its sound is the Penguin's Sounds/manaMissile_hit (the rip); the two front ones reach the target 1.18 s after the launch, the two back ones 2.88 s (calc.txt); Yield 0.2 (:34903): standby 0.8 s (:34716)",
  "builds": ["missile_hit"],
  "cues": [
    [0, "voice", "missile1|missile2"],
    [0.1, "sound", "missile_base"],
    [0.1, "fx", "missileBase", {"rot": [270, 45, 0], "cut": 0.8}],
    [0.1, "fx", "missileBase", {"rot": [270, 135, 0], "cut": 0.8}],
    [0.1, "fx", "missileBase", {"rot": [270, 225, 0], "cut": 0.8}],
    [0.1, "fx", "missileBase", {"rot": [270, 315, 0], "cut": 0.8}],
    [0.6, "sound", "missile_fire"],
    [0.6, "fx", "missile_fire", {"x": 0.6773, "y": 0.2873, "d": 0.6773, "rot": [-16.7, 45, 0], "to": [0, 0.6, 10]}],
    [0.6, "fx", "missile_fire", {"x": -0.6773, "y": 0.2873, "d": 0.6773, "rot": [-16.7, -45, 0], "to": [0, 0.6, 10]}],
    [0.6, "fx", "missile_fire", {"x": -0.6773, "y": 0.2873, "d": -0.6773, "rot": [-16.7, -135, 0], "to": [0, 0.6, 10]}],
    [0.6, "fx", "missile_fire", {"x": 0.6773, "y": 0.2873, "d": -0.6773, "rot": [-16.7, 135, 0], "to": [0, 0.6, 10]}]
  ]
},
"skyDrill": {
  "why": "Mole.cs RPC_skyDrill (:31569-32185), Sky Drill 2, the charge's release after more than 3 s underground with Sky Drill learned (doReleaseCharge :9972-10018, sLv = getSkyDrillLv() :12258), the only skill on its clip: clip cut (:31825), voice skyDrill1 / skyDrill2 (Random.Range(0, 2) :31874, loads :31886 / :31917, PlayOneShot :31898 / :31929), skyDrill createEffect at the hero, rotation x Euler(270, 90, 0) (:31942-31960; followPosition + followState, life 0.55) and, Sky Shaker #413 on (passives on), skyShaker_ring Instantiated at the hero, hero rotation (:31974-31998; skyDrill_ring only without it, :32015-32033), playing its own Sounds/skyDrill, all at 0; the camera's motion blur (:32054-32059) and shake (:32153) left out (the Bison's decision 35); Sky Shaker's 5 m blow (:32085-32120) and the two rings at 0.1 / 0.2 s (radius 1 + i, :31649; Yield 0.1 :32184) hit only targets within 5 m (skyDrill_hit = the prefab field skyDrill_hit, the chopper_hit prefab, :12274, probe_fields.txt); Yield 0.8 (:32180): standby 1.0 s (:31743)",
  "cues": [
    [0, "voice", "skyDrill1|skyDrill2"],
    [0, "fx", "skyDrill", {"rot": [270, 90, 0], "cut": 1.0}],
    [0, "fx", "skyShaker_ring"]
  ]
},
"superDig": {
  "why": "Mole.cs RPC_cAttack1 (:21477-22504), the Charge Attack with Super Dig #411 on (passives on): the superDig clip cut, in place of dig1 (:22290-22304), the only player of this clip: voice superDig in place of cAttack (:22359-22383; at most once per 2 s, :22348-22354), dig_hole Instantiated at the hero + 0.05 m up, hero rotation (:22428-22446; its node 1 loops Sounds/dig for its 2 s), at 0; superDig_dust at the hero, hero rotation, every 0.2 s from 0.1 s (dustTimer = now + 0.1 :22466, + 0.2 :21653, Instantiate :21658-21676; mission / arena only, mGameType > 4 :21637, kept as the Sheep's precedent) until actionTime + 1 - 0.2 x Speed Drill 2 = 0.6 s (:21609, getSpeedDrillLv :22463): 0.1, 0.3, 0.5; at 0.6 s the hero goes under: every renderer off (:22031-22061) until the release, dig_dirt every 0.2 s from 0.9 s at the moving hero, random yaw (:21758-21792), for up to 4 x Charge Attack 3 = 12 s (:21553); that phase belongs to the Charge Attack's tile (question 5)",
  "cues": [
    [0, "voice", "superDig"],
    [0, "fx", "dig_hole", {"y": 0.05}],
    [0.1, "fx", "superDig_dust"],
    [0.3, "fx", "superDig_dust"],
    [0.5, "fx", "superDig_dust"]
  ]
},
"warFactory": {
  "order": "cycle",
  "why": "The warFactory clip: War Factory (#434, one skill) plays it five ways in turn, Saw Machine, Bazooka, Tesla Coil, Roller Machine, Cart Bomb (Mole.cs doSkill (:7376-7460): War Factory's counter steps 1 -> 5 and wraps (:7417-7421); RPC_sawMachine :40826, RPC_bazooka :41400, RPC_teslaCoil :41920, RPC_rollerMachine :42699, RPC_cartBomb :43406, each animation.Rewind() + PlayAnimation(\"warFactory\", 0.2)); every one opens with its voice and warFactory_ring created at the hero, hero rotation (followPosition + followState, its own Sounds/warFactory) at 0 and its machine at 0.3 s; each weapon's own hits reach 2-5 m (FindRecTarget / FindAreaTarget): nothing at 10 m except the Bazooka's shells; one tile, the five in the game's order, one per play (question 2)",
  "skills": {
    "sawMachine": {
      "why": "Mole.cs RPC_sawMachine (:40443-40964): clip (:40826), voice sawMachine (load :40873, PlayOneShot :40885), warFactory_ring (:40897-40913) at 0; Yield 0.3 (:40963): sawMachine_ring createEffect at the hero, hero rotation (:40513-40531; followPosition + followState, its own Sounds/sawMachine); Yield 0.1 (:40951): four cuts 0.2 s apart from 0.4 s (i 1-4 :40568, :40594, :40671; Yield 0.2 :40959) within 4 m (:40704-40746; sawMachine_hit only on a target, and not in the rip); Yield 0.1 (:40957): standby 1.3 s (:40619): both rings' cut",
      "cues": [
        [0, "voice", "sawMachine"],
        [0, "fx", "warFactory_ring", {"cut": 1.3}],
        [0.3, "fx", "sawMachine_ring", {"cut": 1.3}]
      ]
    },
    "bazooka": {
      "why": "Mole.cs RPC_bazooka (:41081-41536): clip (:41400), voice bazooka (load :41447, PlayOneShot :41459), warFactory_ring (:41471-41487) at 0; Yield 0.3 (:41515): bazooka_ring createEffect at the hero, hero rotation (:41150-41168; followPosition + followState, life 2; its Shuriken from TTO's copy, SHURIKEN_FROM_TTO); Yield 0.6 (:41530): three shells 0.3 s apart (i < 3 :41308, Yield 0.3 :41520): 0.9, 1.2, 1.5 s, each bazooka_fire at the hero + TransformDirection(-0.25, 1, 1), LookRotation(forward) (:41318-41346), life 2 x rangeMod (:41361), playing its own Sounds/bazooka_fire; Mole_bazooka: 24 m/s straight (Mole_bazooka.cs:28, :53; no gravity, rip prefab), bursts on the first collider not its layer / 1 / 2 (OnTriggerEnter :93-182): RPC_bazooka_hit = bazooka_hit at the contact, LookRotation(its flat forward) (:182, Mole.cs:14013-14036): on the 10 m target's body front, 9.7 m ahead and 1 m up, 0.35 s after each shot (builds); Yield 0.4 (:41522): standby 2.2 s (:41256): both rings' cut",
      "builds": ["bazooka_hit"],
      "cues": [
        [0, "voice", "bazooka"],
        [0, "fx", "warFactory_ring", {"cut": 2.2}],
        [0.3, "fx", "bazooka_ring", {"cut": 2.2}],
        [0.9, "fx", "bazooka_fire", {"x": -0.25, "y": 1, "d": 1, "to": [0, 0.6, 10]}],
        [1.2, "fx", "bazooka_fire", {"x": -0.25, "y": 1, "d": 1, "to": [0, 0.6, 10]}],
        [1.5, "fx", "bazooka_fire", {"x": -0.25, "y": 1, "d": 1, "to": [0, 0.6, 10]}]
      ]
    },
    "teslaCoil": {
      "why": "Mole.cs RPC_teslaCoil (:41647-42149): clip (:41920), voice teslaCoil (load :41975, PlayOneShot :41987), warFactory_ring (:41999-42017) at 0; Yield 0.3 (:42127): teslaCoil_ring createEffect at the hero, hero rotation (:41717-41735; EffectControl 2.7 s, no followState; its own Sounds/teslaCoil); Yield 0.7 (:42149): seven shocks 0.2 s apart, 1.0 ... 2.2 s (i < 7 :42034, Yield 0.2 :42147), within 5 m (:42046), paralysis on the hit (:42109; drawn on the target only); Yield 0.6 (:42135): standby 3.0 s (:41833)",
      "cues": [
        [0, "voice", "teslaCoil"],
        [0, "fx", "warFactory_ring", {"cut": 3.0}],
        [0.3, "fx", "teslaCoil_ring"]
      ]
    },
    "rollerMachine": {
      "why": "Mole.cs RPC_rollerMachine (:42264-42838): clip (:42699), voice rollerMachine (load :42746, PlayOneShot :42758), warFactory_ring (:42770-42786) at 0; Yield 0.3 (:42822): rollerMachine_ring createEffect at the hero, hero rotation (:42334-42352; followPosition + followState, life 3.2, its own Sounds/rollerMachine); Yield 0.3 (:42826): the first crush at 0.6 s within 2 m (:42394) and a camera shake (:42462, left out); Yield 0.4 (:42832): moveSpeed 1 from 1.0 s (:42489; the hero doesn't travel), ten crushes 0.2 s apart, 1.0 ... 2.8 s (i < 10 :42597, Yield 0.2 :42816; rollerMachine_hit only on a target, :14070-14093); moveSpeed 0 at 3.0 (:42603), Yield 0.5 (:42828): standby 3.5 s (:42545): the ring's cut",
      "cues": [
        [0, "voice", "rollerMachine"],
        [0, "fx", "warFactory_ring", {"cut": 3.5}],
        [0.3, "fx", "rollerMachine_ring", {"cut": 3.5}]
      ]
    },
    "cartBomb": {
      "why": "Mole.cs RPC_cartBomb (:42964-43546), the fifth step, which arms the 180 s cooldown (:43394): clip (:43406), voice cartBomb (load :43453, PlayOneShot :43465), warFactory_ring (:43477-43493) at 0; Yield 0.3 (:43540): cartBomb_ring createEffect at the hero, hero rotation (:43033-43051) and cartBomb_fire at getSpawnPos(hero + 0.5 forward) = on the floor 0.5 m ahead, hero rotation (:43070-43106), Mole_cartBomb.Init (:43132); Yield 0.2 (:43544): from 0.5 s, every FixedUpdate (Yield WaitForFixedUpdate :43538), the hero's code drives it at 6 m/s along the hero's forward (the arrow keys steer it, :43262-43296); Mole_cartBomb (Update, Mole_cartBomb.cs:52-130) blows up 3 s after its Init (:83-88) or when the hero's action changes: RPC_cartBomb_hit = cartBomb_hit at the cart, LookRotation(its forward) (:127, Mole.cs:14128-14154; its own Sounds/cartBomb_hit), 3.3 s; the cart is solid (CapsuleCollider radius 0.5, no trigger, rip prefab) and every layer collides (mainData PhysicsManager m_LayerCollisionMatrix all set, checks/fx_cat_research/parts/probe_ps.txt), so the 10 m target stops it at 9.2 m from 1.95 s and it blows up there at 3.3 s (question 6; builds); the cart's own AudioSource loops Sounds/cartBomb; the cart gone, Yield 0.2 (:43520): standby about 3.5 s (:43196)",
      "builds": ["cartBomb_hit"],
      "cues": [
        [0, "voice", "cartBomb"],
        [0, "fx", "warFactory_ring", {"cut": 3.5}],
        [0.3, "fx", "cartBomb_ring"],
        [0.3, "fx", "cartBomb_fire", {"d": 0.5, "to": [0, 0.6, 10]}]
      ]
    }
  }
}
}
```

## Open questions (each with my recommendation)

1. **TNT 1-4: four tiles or one?**
   - What the game does: each TNT is a cast of its own, with its own key "tnt" + n and its own 90 s cooldown (doSkill :4312-4366). A max-rank Mole has all four, landing at 8 / 16 / 24 / 32 m.
   - Recommended: four tiles, as the pool is written. The page must name the tiles "TNT 1" ... "TNT 4" and give each the rank icon `icons/skills/mole/tnt<n>.webp`; moveSkillIcons finds no icon for `tnt1`.
   - Alternative: one tile at top rank (TNT 4, 32 m, probably off camera).

2. **War Factory: one tile cycling, or five tiles?**
   - What the game does: it is one skill (#434, one icon `warfactory5`) that steps through its weapons in a fixed order (:7417-7421). It is not random, and not five skills.
   - Recommended: one tile, the next weapon on each play in the game's order. With `"order": "cycle"` the page steps FX.pick through `skills` in key order instead of drawing at random.
   - Each play's step should end at that weapon's standby (1.3 / 2.2 / 3.0 / 3.5 / 3.5 s), then fade to idle over 0.2 s. The rest of the 5 s clip is never seen in the game.
   - Fallback with no page change: five tiles (poolChains), each given the War Factory icon by alias.

3. **Fire point for Mortar Shot, Napalm and Stun Grenade.**
   - Recommended: the fixed TransformDirection(0.2, 1, 0.6), as TTO does.
   - Alternative: the page looks up the `firePoint` node under the worn R-hand weapon at play time when it exists (BB's first choice).

4. **Grenade Cluster's voice.**
   - BB asks for a file it doesn't have, so it is silent; TTO plays it.
   - Recommended: play the rip's granadeCluster1|2 (Sheep decision 10), and offer the BB bug to the Bible.

5. **Super Dig tile and the Charge Attack.**
   - Recommended: the superDig tile plays the dive only (voice, dig_hole, three dust puffs) and keeps the hero visible. Hiding him at 0.6 s would blank the last 0.43 s of a 1.03 s clip.
   - Note for whoever writes the Charge Attack (the attacks report): with passives on, the game's Charge Attack always opens with superDig, never dig1 (:22290-22304). That sequence should start with superDig and own the underground phase: the hidden hero, dig_dirt every 0.2 s from 0.9 s, and Speed Drill 2's 0.6 s dive.

6. **Cart Bomb and the target.**
   - Recommended: the cart is stopped by the 10 m target at 9.2 m (at 1.95 s) and blows up there at 3.3 s. The cart is a solid capsule, and mainData's collision matrix lets every layer touch.
   - Alternative: the full 17.3 m run. That matches the page's other projectiles that pass through the target (Penguin decision 7, Bison decision 21), but those also pass through it in the game.

7. **Mortar Shot's interval.**
   - The cues follow the code: 0.2 s apart, the first at 0.3 s.
   - Recommended: offer the Bible a correction of its "0.1 s apart".

8. **gallonDrill (megaDrill_ring's own sound).**
   - Recommended: let `rip_wav` (or SOUND_ALIASES) read `Assets/AudioClip/<name>.ogg` when no WAV exists, so the build has it.
   - Otherwise the drill plays silent and the build lists the sound as missing.

9. **Time Nuke's countdown.**
   - Recommended: build it in Mole_timeNuke as the game draws it:
     - the digits FloorToInt(60 - age) from the GMO24 bitmap font (`Resources/gamegui/fonts/GMO24.asset` and its texture), colour (0.8, 0.3, 0.3);
     - a 30 x 30 px box centred on the screen point 1.0 m above the nuke;
     - drawn only while the camera is less than 30 m away.
   - With the 10 s cut it shows 60 ... 51. Numbers stay digits.

10. **Devices kept past their clip.**
    - Recommended: the mines, the nuke and Flame Carnival stay 10 s (`kill: 10`, like the Sheep's seal fields). Each play lays a new one and they stack, as in the game.
    - Alternative: remove them on the next pick only.

11. **No travel.** Mega Punch's and Mega Drill's step back (moveSpeed -5 for 0.1 s) and the Roller Machine's 1 m/s roll are left out (Bison decision 17).

## Verification

Read-only check, 2026-11-13 (home PC), against `D:\12tails\DecompiledSource\Mole.cs`, `Math.cs`, `Mole_stunGrenade.cs`,
`Mole_cartBomb.cs`, the TTO pseudo-C, the Bible's cards / `mole-skill-reference.md`, the BB rip and BB's own Resources
container (`12TailsOnline_Data` mainData + resources.assets, ResourceManager read with UnityPy, read-only). Helpers
(git-ignored): `checks/fx_mole_research/verify_eo_b/` (`pred.py` evaluates every junk predicate in a line range,
`clip_calls.txt`, `container.py`).

**Verdict: every cue time, position, rotation, rank, random pick and buildability claim I checked holds; the JSON block
parses and equals `checks/.../skills_b/pool.json`. The corrections are citations and the check / icon side, not cue values.**

Checked and confirmed:
- **Clips and members:** clip_calls.js gives exactly these 11 clips' players (mine x4, mortarShot x2, punch x2, tnt, grenade,
  grenadeCluster, hammer, missile, skyDrill, superDig in cAttack1, warFactory x5). Every key is a clip in
  `wardrobe/data/mole/clips.json` (mine 1.0, mortarShot 1.5, punch 0.8, tnt 0.8, grenade 1.0, grenadeCluster 1.0, hammer
  1.0, missile 1.0, skyDrill 1.3, superDig 1.0333, warFactory 5.0 s). Max ranks match the Bible cards (Landmine 4, Mortar
  Shot 2, TNT 4, Stun Mine 2, Stun Grenade 2, Time Nuke 2, Speed Drill 2, Sky Drill 2, Mega Punch 2, Mega Hammer 2,
  Missile 4, Charge Attack 3; Napalm, Grenade Cluster, Flame Carnival, Mega Drill, War Factory 1).
- **Timelines (state machines walked with pred.py):** mine / stunMine / timeNuke / flameCarnival: voice 0, Yield 0.3 lay +
  Sounds/mine, Yield 0.5, standby 0.8. mortarShot: voice, Yield 0.1, then one shell per Yield 0.2 = 0.3 ... 1.1, standby at
  the last. napalm 0.3 / 0.6. megaPunch 0.2 fx, 0.3 punch, 0.6 standby. megaDrill 0.2 ring, hits 0.4-0.7, standby 1.0.
  tnt 0.2 / 0.5 / 0.8 (TNT n = sLv n: mol_tnt4 num 1 +1 +1 +1, :6573-6610, :8841-8851). stunGrenade 0.6 / 0.8.
  grenadeCluster 0.5 / 0.7. megaHammer 0 / 0.4 / 0.7. missile 0.1 / 0.6 / 0.8. skyDrill rings 0.1 / 0.2, standby 1.0.
  superDig dust 0.1 / 0.3 / 0.5 (dustTimer +0.1 then +0.2, until actionTime + 1 - 0.2 x 2 = 0.6, :21609; the
  mGameType > 4 gate :21637, as stated). War Factory's counter 1 -> 5 wrap; saw cuts 0.4-1.0, standby 1.3; bazooka shells
  0.9 / 1.2 / 1.5, standby 2.2.
- **Geometry recomputed:** getMortarVector (Math.cs:1009-1075, predicates evaluated): fire point (0.2, 1, 0.6) -> (0, 0, 10)
  = rot [-83.34, -1.22, 0]. Napalm aims are the target + world (-5,0,-5), (-5,0,5), (5,0,-5), (5,0,5) (:37185-37232;
  getMortarVector(firePos, firePos + fireDir) :13737) = [-85.2, -49.76], [-78.98, -19.86], [-85.41, 47.49], [-79.08, 18.43]:
  all five as in the block. getTrajectoryVector worked by hand for Stun Grenade (v 15, y -1, d 9.40): 6.75 deg up,
  yaw -1.22. Missile: missileBase Euler(270, 90 - 45 + 90 b) = 45 / 135 / 225 / 315 (:34478-34522); rotateH(+a) turns
  left (Math.cs:838-843), so fireDir -45 + 90 i = Unity yaw 45, -45, -135, 135, 16.7 deg up, spawned at hero + dir
  (:13140): the +-0.6773 / 0.2873 offsets are right. Grenade Cluster yaws 0, 315 ... 45 and tilt 0.1 x Random.Range(3, 10)
  (:38009) are right. TNT lands 8 n m along transform.forward (:25846). Bazooka fire point TransformDirection(-0.25, 1, 1),
  LookRotation(forward) (:41318-41346).
- **Files:** every voice and sound named exists in the rip (granadeCluster1 / 2 included). BB's Resources container has
  `mole/voices/granadecluster1|2` and no grenadecluster voice, no grenadecluster_ring / granadecluster_ring, no
  stungrenade_hit and no gallondrill (that sound is only `Assets/AudioClip/gallonDrill.ogg`). So the silent-voice, no-ring
  and gallonDrill claims hold. missile_fire, missileBase, missile_hit, mine4, stunMine2 and timeNuke2 are in the container
  too. Stun Grenade's burst is `RPC_nAttack_hit` (Mole_stunGrenade.cs:193), and Mole.nAttack_hit is the hero prefab's
  nAttack_hit field (probe_fields).
- **Cuts:** every `cut` sits on a followState effect (probe: tnt, megaPunch, megaDrill_ring, megaHammer, missileBase,
  skyDrill, warFactory_ring, sawMachine_ring, bazooka_ring, rollerMachine_ring) and is compared with the clip time
  (index.html Fx cutAt, :4188). megaDrill_ring 1.0, skyDrill 1.0, and warFactory_ring / rollerMachine_ring 3.5 fall at or
  after their own life, so they do nothing and do no harm.
- **TTO:** the cited twins at pseudo/Mole.c:21221 / 12260 / 14526 / 15555 / 21615 / 22751 / 10716 / 16638 / 18404 /
  15162 / 14070 / 20512 / 23151 / 19802 / 4582 / 22246 / 19379 / 7949 are PlayAnimation calls; OldMissile is at :16064.

Corrections:
1. **The TNT citations ":4312-4366" are not doSkill.** Mole.cs:4312 / 4330 / 4348 / 4366 are in `onActionEvent`
   (Mole.cs:3380), the peers' replay of RPC_tnt1-4. The owner's cast is doSkill `mol_tnt1-4` (:6573-6610, num through
   IL_2401 / IL_224C :8841-8851) and `StartCoroutine(RPC_tnt(..., num))` :8815. "Read this first" 1 and question 1 also
   say "doSkill :4312-4366". The cue values are right. Exact replacements in the paste block (the tnt entry):
   - pool why: `(Mole.cs:26180, doSkill :4312-4366;` -> `(Mole.cs:26180; doSkill mol_tnt1-4 :6573-6610 -> num 1-4 via :8841-8851, RPC_tnt :8815; the peers replay RPC_tnt1-4 in onActionEvent :4312-4366;`
   - tnt1: `(:26180; doSkill :4312)` -> `(:26180; doSkill mol_tnt1 :6602, RPC_tnt :8815; onActionEvent :4312 for the peers)`
   - tnt2: `(:26180; doSkill :4330)` -> `(:26180; doSkill mol_tnt2 :6594, RPC_tnt :8815; onActionEvent :4330 for the peers)`
   - tnt3: `(:26180; doSkill :4348)` -> `(:26180; doSkill mol_tnt3 :6586, RPC_tnt :8815; onActionEvent :4348 for the peers)`
   - tnt4: `(:26180; doSkill :4366)` -> `(:26180; doSkill mol_tnt4 :6573, RPC_tnt :8815; onActionEvent :4366 for the peers)`
2. **The check rejects two new keys until they are added** (the report doesn't say so): `pipeline/wardrobe_fx_check.py`
   ENTRY_KEYS (:182) has no `"order"`, so the warFactory entry fails with "unknown entry keys". OPTS (:171-174) has no
   `"tilt"`, so every grenadeCluster_fire cue fails the cue-shape test (:213). Paste:
   ```python
   ENTRY_KEYS, SKILL_KEYS = {"why", "cues", "skills", "builds", "everyCycle", "order"}, {"why", "cues", "builds", "everyCycle"}
   # OPTS gains "tilt" (Mole_grenadeCluster's per-grenade Random.Range(3, 10) tilt, plans/fx_mole/skills_b.md)
   ```
   On the page, `tilt` already reaches the part through cueOf's `{ ...o }` spread (index.html cueOf, from :4629 at this check). `order`
   needs the pick in fxStart (around index.html:5092, `FX.pick = names[random]` today; index.html is being edited, so
   anchor by text) to step through `Object.keys(e.skills)`.
3. **Two single-skill clips have no icon (a missing part the report leaves out):** `wardrobe/data/icons/hd/index.json` has
   no mole entry for `grenade` or `hammer`: their base names match no Bible icon (`punch` is covered by its pool). Paste
   into `pipeline/wardrobe_skill_icons.py` CLIP_SKILLS:
   ```python
       # the Mole's grenade clip is Stun Grenade, hammer is Mega Hammer (2026-11-13, plans/fx_mole/skills_b.md Verification 3)
       "mole": {"grenade": ["stunGrenade"], "hammer": ["megaHammer"]},
   ```
4. **Tile names:** poolChains names a member from its key (index.html:1379), so `mine` shows "Mine", not the Bible's
   "Landmine" (and `tnt1` shows "Tnt1", as question 1 says). Renaming the key would lose its icon (`best` keys on the
   Bible's `mole_mine4`), so the tile needs a display alias or stays "Mine". This belongs in question 1 too.
5. **Counts:** "23 tiles" holds only with War Factory as five tiles. With the recommended `"order": "cycle"` it is 19.
6. War Factory's counter is at :7416-7427 (not :7417-7421).

Corrected paste-ready blocks: the cue block stands except for the five `why` replacements in correction 1. Add the
check lines (correction 2) and the CLIP_SKILLS line (correction 3).
