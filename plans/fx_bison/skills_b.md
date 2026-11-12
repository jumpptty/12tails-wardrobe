# Bison effects + sounds research: overPower, overSwing, prideCrusher, slam, trample, volcanicRam, warcry (skills_b)

Researcher `skills_b`, 2026-11-13 (home PC). Scope: the clips `overPower`, `overSwing`, `prideCrusher`, `slam`,
`trample1`, `trample2`, `volcanicRam`, `warcry` and every skill that plays them. Research only (recipe steps 1-3).
Line numbers are `D:\12tails\DecompiledSource\Bison.cs` unless another file is named. Times are seconds from the start
of the clip the entry is keyed by. Distance 0 = at the hero. Max rank, passives on (the Wolf's / Sheep's / Penguin's
decisions): Slam 2, Trample 2, Over Power 2, Warcry 2, Titan Form 2; Aspect of the Horde #412, Steel Skin #433,
Mythril Skin #443, Over Swing #273, Raw Strength #431 (damage only). Page stats: `chaAdjust(n)` = n.

Read-only probes and scripts, in `checks\fx_bison_research\skills_b\`:
- `clean.py` / `dump.py` (copied from the Bat's: a coroutine with its opaque `if (a - b == c)` predicates worked out)
  and `clean_RPC_<name>.txt` for the ten coroutines; I re-checked the branch points by hand in the raw file (slam
  :21470-21520, trample :22120-22200, overSwing :25258-25446).
- `clip_calls.txt` (`clip_calls.js` for the Bison), `tto_strings.txt` (every string literal of TTO's ten coroutines).
- `cc_addStatus_bison.txt` / `cc_removeStatus_bison.txt` (CharacterControl's status visuals for overPower, ironShield,
  diamondShield, titanForm, fear).
- `probe.json` / `probe_summary.txt` (`wardrobe_fx.py bison --probe` on 24 effects), `probe2.py` / `probe2.json`
  (aspect_slam and aspect_trample with UVScroll's layout patched in for that run only).
- `voice_container.py` / `voice_container.txt` (BB's Resources container: which pride / onslaught voices exist).
- `cues.py` -> `cues.json` (the entries below, checked: valid JSON, times in order, known kinds and options).

## Read this first

1. **Two pools.**
   - `overPower` is played by Over Power (:24855) and Titan Form (:29891). Two pool members, `overPower.skills`
     `overPower` / `titanForm`.
   - `warcry` is played by Warcry (:27096), Iron Shield (:27799), Diamond Shield (:28389) and Onslaught (:30615).
     Four pool members, `warcry.skills` `warcry` / `ironShield` / `diamondShield` / `onslaught`.
   - No SEQ holds either clip, so poolChains gives each member a tile of the clip alone and hides the plain clip
     (`C.poolClips`). Tiles: Over Power, Titan Form, Warcry, Iron Shield, Diamond Shield, Onslaught. No SEQ_SKILL
     entry is needed.
   - Icons: `data/icons/hd/index.json` has overPower and warcry but not titanForm, ironShield, diamondShield or
     onslaught. `wardrobe_skill_icons.py` adds pool members' Bible icons once the cue file names them (NOTES
     2026-11-10).
2. **Trample's SEQ step is wrong: `trample2*@2.6` should be `trample2*@2.4`.**
   - Phase 1: passes at 0.3, 0.5 and 0.7 s (the first pass runs straight from case 2, `goto IL_12D6` :22133).
   - At i = 3 (0.9 s) trample2 starts (:22511-22518), so `trample1@0.9` is right.
   - Phase 2: 2 + 5 x 2 = 12 passes 0.2 s apart (:22197, :22686), standby at 0.9 + 2.4 = 3.3 s (:22215-22220).
3. **FX.t restarts at every step** (`fxStart`, index.html:4441), and a cue's `cut` is read against it (:3954).
   - Effects/trample2 is cued on trample1 at 0.3 s but ends when the hero stands at 3.3 s. Its cut is therefore
     **2.4**: trample2's own time, where the cut is reached.
   - aspect_trample (cued on trample2 at 0) has the same cut, 2.4.
4. **The parts the page still needs:**
   - **UVScroll** (aspect_slam, aspect_trample; the inventory's "needs UVScroll").
     - Layout `"UVScroll": [("scroll_x", "f"), ("scroll_y", "f")]`: 8 bytes, UVScroll.cs:67-70. With it patched
       in, `probe2.py` decodes both effects clean, and nothing else is missing.
     - Update: `renderer.material` _MainTex offset = (Repeat(Time.time x scroll_x, 100), Repeat(Time.time x
       scroll_y, 100)) (UVScroll.cs:44-45). This is the global clock, not the effect's age.
     - Both effects have scroll (0.2, -0.2). aspect_slam's node has StaticMesh + UVScroll + AlphaTimer.
       aspect_trample has two skinned ghost Bisons 2.5 m left and right (Animation + SkinnedMeshRenderer +
       AlphaTimer + UVScroll).
   - **A cue's `bone` with a `rot`.** overPower_horn2 is parented to the Head bone with localRotation
     Euler(-90, 0, 0) (CharacterControl.cs:35016-35025). Today a cue's bone forces localRotation identity: the bone
     branch in `Fx.update` (index.html:3985-3990) overwrites the root's quaternion, so the cue's `rot` is lost. The
     part: in the bone branch, multiply the rot in as localRotation.
     - The Head bone exists in `data/bison/rig.json`, and every scale on its chain is 1, so localScale 1 = world
       scale 1.
   - **Titan Form's look: a `skin` cue `titanForm`** (HERO_SKINS has only FX/CosmicRift). The status does two things:
     - Hero scale: localScale += 0.3 x sLv + 0.2 = +0.8, to x 1.8 (CharacterControl.cs:35219).
     - Tint: every renderer's `_Color` rgb set to (0.6, 0.7, 1), alpha kept (setColor :21702-21790, called
       :35222-35225). The default is (0.86, 0.86, 0.86): removeStatus puts that back (:15679-15691). So relative to
       the normal look the tint is about x (0.70, 0.81, 1.16).
     - Both last kill seconds (10).
     - skills_a's Enrage status needs the same two things: `localScale += 0.05 x sLv`, colour (0.8 + 0.05 sLv,
       0.8 - 0.05 sLv, 0.8 - 0.05 sLv) (CharacterControl.cs:34717-34729). One part should serve both.
   - Everything else is built: Ring / Line / Emblem emitters, legacy particles, StaticMesh, Animation,
     SkinnedMeshRenderer, AlphaTimer, TrailEmitter, AudioSource (a loop too), EffectControl.
5. **The status visuals come from CharacterControl, so the inventory doesn't list them.** CharacterControl's
   `addStatus` (CharacterControl.cs:32343; visuals at :35003-35267) draws them, not Bison.cs. They are
   overPower_horn2, overPower_ring, ironShield, diamondShield and titanForm.
   - All five probe clean with built parts.
   - None has an EffectControl: each lives until removeStatus destroys it (:15519-15709). Each gets `kill` = the
     status time: overPower 9 s, ironShield / diamondShield 8 s, titanForm 60 s cut to 10.
   - Each is drawn at once on RPC_AddStatus. The addStatus coroutine's only wait is its last YieldDefault (:32750).
6. **A game bug in BB and TTO: Pride Crusher and Onslaught are silent** (offer it for the Bible).
   - BB loads `Voices/prideCrusher1` / `prideCrusher2` (:31073-31132) and `Voices/onslaught1` / `onslaught2`
     (:30251-30310).
   - No such clips exist. BB's Resources container has only `voices/overpride1` / `overpride2` (Over Pride, :8673)
     under those words (`voice_container.txt`). The BB rip's voices folder and TTO's rip have none either.
   - TTO asks for the same paths (`tto_strings.txt`), so it has no fix.
   - So these two skills play no voice cue; their effects still play their own Sounds/prideCrusher and Sounds/warcry.
7. **volcanicRam is an animation that no code plays.**
   - It sits in BB's rip (`heroes/bison/animations/volcanicRam.prefab`, `AnimationClip/volcanicRam.anim`).
   - No `.cs` in the Bible repo names it (BB, both Reborn decompiles), and no TTO string does
     (`names.tsv`, `pseudo/Bison.c`).
   - So it has no cues. Whether its tile stays is question 1.
8. **TTO plays these clips through the same ten coroutines, with the same literals.** RPC_slam, RPC_trample,
   RPC_overPower, RPC_overSwing (from doBeginCharge), RPC_warcry, RPC_ironShield, RPC_diamondShield, RPC_titanForm,
   RPC_onslaught and RPC_prideCrusher are at `pseudo/Bison.c` :2537 / :5644 / :12142 / :12717 / :13173 / :14804 /
   :15340 / :16401 / :16838 / :17945 / :22223. None of TTO's released skills (magmaQuakeAxe, titanDrop,
   unchainedFury) plays a clip in this scope (they have their own clips).
9. **Nothing in scope lands on the 10 m target.**
   - Over Swing's circles (6 / 8 m), Pride Crusher's 8 m box and Slam's 3 m box don't reach it. Trample's boxes
     don't either with the hero in place.
   - Warcry's fear (30 m) and Onslaught's damage (30 m) reach it, but draw nothing: fear only changes ATK / TAL
     (CharacterControl.cs:35312-35322), and RPC_AddDamage spawns no effect for these codes.
   - So no `nAttack_hit` sparks are cued.
10. **Left out, with no page part to draw them:**
    - The camera motion blur: Over Power :25020, Over Swing :25235, Warcry :26915, the shields :27656 / :28243,
      Onslaught :30384.
    - The camera shakes: Pride Crusher :30862, Onslaught :30357.
    - The precedent is the Penguin's Dispell screen warp (NOTES 2026-11-13).

## Over Power (`overPower` pool member `overPower`)

- RPC: `RPC_overPower` :24610-25082 (MoveNext :24724). Key press :6681, remote :4053 / :4071.
- Timeline:
  - 0: clip cut in, `PlayAnimation(overPower, 0)`, WrapMode.Once (:24855-24858), moveSpeed 0.
    - Voice overPower1 / overPower2, `Random.Range(0, 2)` (:24896-24955).
    - Effects/overPower via createEffect at the hero's position and rotation (:24979-24997). EffectControl life 1 +
      afterLife 2, no followState, followPosition; two RingEmitters with Delay 0.3; it plays its own
      Sounds/overPower.
    - The motion blur (:25017-25020) is left out.
  - `Yield(2, 0.5)` (:25043). At 0.5: `RPC_AddStatus(overPower, sLv 2, chaAdjust(9), ...)` (:24764). The status
    visuals (CharacterControl.cs:35003-35040), both removed at the status end (:15526-15553):
    - `overPower_horn` + sLv = **overPower_horn2**: Instantiate, parent `findChildObject(Head)`, localPosition 0,
      localRotation Euler(-90, 0, 0), localScale 1. A StaticMesh, no EffectControl.
    - **overPower_ring**: at the hero, world identity, parented, localScale 1. A RingEmitter with repeatForever, no
      EffectControl.
  - `Yield(3, 0.3)` (:25041). At 0.8: standby (:24785).
- Max rank: horn2 (horn1 at rank 1). The status value is the only other rank change.
- Random: the voice. Rolls: none.
- Buildable: overPower ready (inventory). horn2 / ring probe clean; the horn needs the bone + rot part.
- Cue: `cues.json` `overPower.skills.overPower` (below).

## Titan Form (`overPower` pool member `titanForm`)

- RPC: `RPC_titanForm` :29638-30085 (MoveNext :29752). Key press :6505, remote :4359 / :4377.
- Timeline:
  - 0: `animation.Rewind()` + `PlayAnimation(overPower, 0)`, Once (:29888-29894), moveSpeed 0.
    - Voice titanForm1 / titanForm2, `Random.Range(0, 2)` (:29932-29991).
    - **titanForm_ring** via createEffect at the hero, hero rotation (:30000-30016). Life 1 + 2, no followState; its
      own Sounds/titanForm.
  - `Yield(2, 0.3)` (:30049). At 0.3: `RPC_AddStatus(titanForm, sLv 2, chaAdjust(60), 0, ...)` and `RPC_AddHeal`
    (:29792-29797). RPC_AddHeal spawns nothing (CharacterControl.cs:7130-7530). The status
    (CharacterControl.cs:35209-35298):
    - Removes enrage / enlarge.
    - Scale +0.8 (:35219) and tint (0.6, 0.7, 1) (:35222-35225).
    - Stats and rangeMod.
    - **titanForm** (Resources) Instantiated at the hero, identity, then parented with localScale one (:35243-35267).
      It was made after the growth, so it is drawn at the hero's 1.8: cue `scale 1.8`. A RingEmitter with
      repeatForever, no EffectControl.
    - Removed at the status end (:15675-15709).
  - `Yield(3, 0.5)` (:30047). At 0.8: standby (:29818).
- Max rank: scale +0.8 (rank 1: +0.5). The status lasts 60 s, cut at 10 (the long-buff rule).
- Buildable: titanForm_ring ready. titanForm probes clean. The growth and tint need the `skin` titanForm part.
- Cue: `overPower.skills.titanForm`.

## Over Swing (`overSwing`)

- RPC: `RPC_overSwing` :25083-25687 (MoveNext :25186).
  - Started from `doBeginCharge` when the Charge Attack press comes with the overPower status on, Over Swing #273
    and no overSwing timeout (:5169-5280, start :5259). Bible bsn_overSwing1.
  - Remote: `RPC_overSwing1` (:5272, :4089).
- Timeline:
  - 0: `PlayAnimation(overSwing, 0.2)`, WrapMode.Loop (:25464-25467), moveSpeed 0.
    - Voice overSwing1 / overSwing2, `Random.Range(0, 2)` (:25505-25564).
    - **overSwing_ring** via createEffect at the hero, hero rotation (:25573-25589). Life 1 + 2, no followState; a
      LineEmitter at 1.5 m and a RingEmitter (Delay 0.5); its own Sounds/overSwing.
  - `Yield(2, 0.5)` (:25623). At 0.5: moveSpeed 3 (:25219). The motion blur (:25230-25235) is left out. Brute
    Strength and the Over Power level are read (damage only).
  - `if (i < 2) Yield(3, 0.2)` (:25431, :25629). At 0.7: a circle of 6 m (:25293). At 0.9 (i = 1): a circle of 8 m.
    - Each hit spawns `RPC_nAttack_hit` at the target + 1.5 m up (:25332; Bison.cs:7084-7097 instantiates
      nAttack_hit).
    - The 10 m target is 8.8 m away at 0.9 s, even with the game's 1.2 m of travel, and FindAreaTarget subtracts only
      its 0.3 m radius (Damage.cs:1074-1124). So: no hit.
  - At i = 2: moveSpeed 0 and `Yield(4, 0.1)` (:25439, :25625). At 1.0: standby (:25379).
- The tile: LOOPS has overSwing, so it holds `max(1, round(1.5 / 1.2))` x 1.2 = 1.2 s; the game's 1.0 is close
  enough (question 4).
- The Over Power status it needs is on throughout, so the tile carries the horn and ring for its 1.2 s (question 3).
- Max rank: single rank. Raw Strength's roll is damage only.
- Buildable: overSwing_ring ready. The horn needs the bone + rot part.
- Cue: `overSwing`.

## Pride Crusher (`prideCrusher`)

- RPC: `RPC_prideCrusher` :30710-31241 (MoveNext :30813). Key press :6048, remote :4449.
- Timeline:
  - 0: `PlayAnimation(prideCrusher, 0)`, Once (:31032-31035), moveSpeed 1 (:31041).
    - The voice load (:31073-31132) finds nothing (item 6).
    - **prideCrusher_ring** via createEffect at the hero, hero rotation (:31141-31157). Life 2 + 1, **followState**;
      Line / Ring emitters, the crack ones with Delay 0.6, legacy particles 4 m ahead; its own Sounds/prideCrusher.
  - `Yield(2, 0.6)` (:31184). At 0.6: moveSpeed 0, the camera shake (:30862, left out), and the box 1 / 1 wide by
    8 m ahead (:30881), which misses the 10 m target. `hit()` spawns no effect.
  - `Yield(3, 0.2)` (:31189). At 0.8: standby (:30962). This cuts the ring: the cue's 5th value is 0.8.
- Max rank: single rank (Bible: Class C).
- Buildable: ready.
- Cue: `prideCrusher`.

## Slam (`slam`)

- RPC: `RPC_slam` :21253-21887 (MoveNext :21367). Key press :6873, remote :3783 / :3801.
- Timeline:
  - 0: `PlayAnimation(slam, 0)`, Once (:21676-21679), moveSpeed 0, removeLockStatus (:21688).
    - Voice slam1 / slam2, `Random.Range(0, 2)` (:21720-21779).
    - **slam_ring** via createEffect at the hero, hero rotation (:21788-21804). Life 1, no followState.
  - `Yield(2, 0.2)` (:21835). At 0.2:
    - moveSpeed 7 (:21400).
    - **slam_dust** via Instantiate at the hero, hero rotation (:21405-21423). Life 1, followPosition false; the
      trample_dust mesh; its own Sounds/slam.
    - With Aspect of the Horde: **aspect_slam** via createEffect at the hero (:21437-21461). Life 1,
      **followState**; needs UVScroll.
    - i = 0, then the first hit round straight away (:21516, :21600).
  - Then `Yield(3, 0.1)` (:21839), with i++ in case 3. Hit rounds at 0.2, 0.3, 0.4 and 0.5 s: a 3 m box (4 m wide
    with Aspect), which misses the target.
  - At i = 4 (0.6): moveSpeed 0, standby (:21516-21549). This cuts aspect_slam: 5th value 0.6.
- Max rank: 4 hit rounds instead of 3. No effect changes.
- Buildable: slam_ring and slam_dust ready. aspect_slam needs UVScroll.
- Cue: `slam`.

## Trample (`trample1` + `trample2`, the "Trample" SEQ)

- RPC: `RPC_trample` :21888-22760 (MoveNext :22002). Key press :6821, remote :3819 / :3837.
- trample1 timeline:
  - 0: `PlayAnimation(trample1, 0)`, Once (:22386-22391), moveSpeed -2 (:22401), removeLockStatus (:22406).
    - Voice trample1 / trample2, `Random.Range(0, 2)` (:22442-22502; PlayOneShot :22679 / :22700).
  - `Yield(2, 0.3)` (:22696). At 0.3:
    - moveSpeed 7 (:22035).
    - The sLv switch gives **Effects/trample2** at rank 2 (trample1 at rank 1) via createEffect at the hero, hero
      rotation (:22040-22116). Life 4 + 1, **followState**, followPosition; ghost-Bison mesh + line / ring emitters;
      its own Sounds/trample2.
    - i = 0, `goto IL_12D6` (:22133): phase 1, i < 3. A box from 1 m behind (:22586), and **trample_dust** via
      Instantiate at the hero, hero rotation (:22642-22658).
  - `Yield(3, 0.2)` (:22703), with i++ in case 3 (:22155). Dust at 0.3, 0.5 and 0.7.
- trample2 timeline (times from its start, 0.9 s after trample1's):
  - At i = 3 (0.9): `PlayAnimation(trample2, 0)`, Loop (:22511-22518), moveSpeed 9 (:22521).
    - **aspect_trample** via createEffect at the hero (:22524-22548). Life 3, **followState**; needs UVScroll.
    - i = 0, IL_471: phase 2. **trample_dust** (:22268-22274) and a 3 m box (:22293).
  - `Yield(4, 0.2)` (:22686), with i++ in case 4 (:22182). Dust at 0, 0.2, ..., 2.2 (12).
  - At i = 12 (2.4): moveSpeed 0, standby (:22197-22220). This cuts aspect_trample and Effects/trample2: cut 2.4 in
    trample2's time (item 3).
- The hero stays in place (the Wolf's Feral Strike / Penguin decision 8 convention), so every dust is at the hero and
  the 10 m target is never trampled. In the game the run covers 4.2 + 21.6 m and would hit it at about 1.3 and 1.5 s.
- Max rank: Effects/trample2, and 12 phase-2 passes instead of 7.
- Buildable: trample2 and trample_dust ready. aspect_trample needs UVScroll.
- Cues: `trample1` and `trample2`. SEQ fix: `"Trample: trample1@0.9 trample2*@2.4"`.

## Warcry (`warcry` pool member `warcry`)

- RPC: `RPC_warcry` :26715-27286 (MoveNext :26829). Key press :6598, remote :4179 / :4197.
- Timeline:
  - 0: `PlayAnimation(warcry, 0)`, Once (:27096-27099). Voice warcry1 / warcry2, `Random.Range(0, 2)`
    (:27137-27233).
  - `Yield(2, 0.3)` (:27221). At 0.3: **warcry_ring** via createEffect at the hero, `Quaternion.identity`
    (:26862-26880). Life 2, no followState; Emblem / Ring / Line emitters; its own Sounds/warcry. The motion blur
    (:26910-26915) is left out.
  - `Yield(3, 0.3)` (:27218). At 0.6: hate + fear on enemies within 30 m (:26955-26999). Nothing drawn (item 9).
  - `Yield(4, 0.2)` (:27223). At 0.8: standby (:27026).
- Identity rotation: no `rot`, as the Sheep's sealOfAttack and the Wolf's valor_emblem (the page's hero stands at
  identity; the ring is round anyway).
- Max rank: radius 30 m only.
- Buildable: ready.
- Cue: `warcry.skills.warcry`.

## Iron Shield (`warcry` pool member `ironShield`)

- RPC: `RPC_ironShield` :27287-27873 (MoveNext :27401). Key press :5921, remote :4215.
- Timeline:
  - 0: `PlayAnimation(warcry, 0)` (:27799).
  - `Yield(2, 0.3)` (:27826). At 0.3:
    - Voice ironShield1 / ironShield2 (:27535-27594). It would be perfectShield1 / 2 if diamondShield were already
      on (:27462-27527), never on this tile.
    - **ironShield_ring** via createEffect at the hero, hero rotation (:27603-27621). Life 1 + 1, **followState**;
      its own Sounds/shield_create.
    - The motion blur is left out.
  - `Yield(3, 0.3)` (:27834). At 0.6: status ironShield for chaAdjust(6) + 2 with Steel Skin #433 = 8 s
    (:27691-27708). The status draws **ironShield** at the hero, identity, parented (CharacterControl.cs:35054-35076):
    orbiting shield mesh, trail, a looping Sounds/shield. Removed at the status end (:15587-15603).
  - `Yield(4, 0.2)` (:27832). At 0.8: standby (:27729). This cuts the ring: 0.8.
- Not drawn: perfectShield / perfectArmor (both shields at once, CharacterControl.cs:11973-12033). Question 5.
- Buildable: all ready.
- Cue: `warcry.skills.ironShield`.

## Diamond Shield (`warcry` pool member `diamondShield`)

- RPC: `RPC_diamondShield` :27874-28465 (MoveNext :27988). Key press :5947, remote :4233.
- The same shape as Iron Shield:
  - 0: Rewind + `PlayAnimation(warcry, 0)` (:28386-28389).
  - At 0.3: voice diamondShield1 / diamondShield2 (:28122-28181; perfectShield1 / 2 only with ironShield on), and
    **diamondShield_ring** via createEffect (:28190-28208; followState).
  - At 0.6: status diamondShield for 6 + 2 = 8 s with Mythril Skin #443 (:28278-28295). It draws **diamondShield**
    (CharacterControl.cs:35085-35107), removed at :15609-15625.
  - At 0.8: standby (:28316). Cut 0.8.
- Buildable: all ready.
- Cue: `warcry.skills.diamondShield`.

## Onslaught (`warcry` pool member `onslaught`)

- RPC: `RPC_onslaught` :30086-30709 (MoveNext :30189). Key press :5994, remote :4431.
- Timeline:
  - 0: `PlayAnimation(warcry, 0)` (:30615).
  - `Yield(2, 0.3)` (:30652). At 0.3:
    - The voice load (:30251-30310) finds nothing (item 6).
    - **onslaught_ring** via createEffect at the hero, identity (:30319-30337). Life 2, no followState; its own
      Sounds/warcry.
    - The shake (:30357) and motion blur (:30379-30384) are left out.
  - `Yield(3, 0.3)` (:30647). At 0.6: damage from the hate list within 30 m (:30419-30518). Nothing drawn.
  - `Yield(4, 0.2)` (:30640). At 0.8: standby (:30545).
- Buildable: ready.
- Cue: `warcry.skills.onslaught`.

## Paste-ready entries for `wardrobe/fx_cues/bison.json`

Also in `checks/fx_bison_research/skills_b/cues.json` (made and checked by `cues.py`). The two pools use the Wolf's
instantCast / the Penguin's cast3 shape (`{why, skills: {member: {why, cues}}}`). Trample is keyed by its two clips,
as the Sheep's holyLight1 / holyLight3 / holyLight4. A cue's 5th value is the followState cut.

```json
 "overPower": {
  "why": "The overPower clip is played by two skills: Over Power (RPC_overPower, Bison.cs:24855) and Titan Form (RPC_titanForm, :29891); one tile each (poolChains); the two never meet in the game (each refuses while the other is on, :6473-6485, :6666-6678)",
  "skills": {
   "overPower": {
    "why": "Bison.cs RPC_overPower (:24610-25082), max rank sLv 2 (dispatch :6681): clip cut in (PlayAnimation(overPower, 0) :24855), voice overPower1 / overPower2 (Random.Range(0, 2), :24896-24955) and Effects/overPower at the hero, hero rotation (createEffect :24985-24997; no followState; plays its own Sounds/overPower) at 0; the camera's motion blur (:25017-25020) left out; Yield 0.5 (:25043): the overPower status, sLv 2, chaAdjust(9) = 9 s (:24764): CharacterControl's addStatus Instantiates overPower_horn2 (overPower_horn + sLv) on the Head bone, localPosition 0, localRotation Euler(-90, 0, 0), localScale 1, and overPower_ring at the hero, world identity, parented (CharacterControl.cs:35003-35040), both destroyed when the status ends (:15519-15553): kill 9; Yield 0.3 (:25041): standby 0.8 s (:24785)",
    "cues": [
     [0, "voice", "overPower1|overPower2"],
     [0, "fx", "overPower"],
     [0.5, "fx", "overPower_horn2", {"bone": "Head", "rot": [-90, 0, 0], "kill": 9}],
     [0.5, "fx", "overPower_ring", {"kill": 9}]
    ]
   },
   "titanForm": {
    "why": "Bison.cs RPC_titanForm (:29638-30085), max rank sLv 2 (dispatch :6505): clip overPower cut in (Rewind, PlayAnimation(overPower, 0) :29888-29891), voice titanForm1 / titanForm2 (Random.Range(0, 2), :29932-29991) and Effects/titanForm_ring at the hero, hero rotation (createEffect :30000-30016; no followState; plays its own Sounds/titanForm) at 0; Yield 0.3 (:30049): the titanForm status, sLv 2, chaAdjust(60) (:29792; cut at 10 s, the long-buff rule) and RPC_AddHeal (:29797, draws nothing): addStatus grows the hero by 0.3 x 2 + 0.2 = 0.8 (localScale 1.8, CharacterControl.cs:35219), tints every renderer's _Color (0.6, 0.7, 1) where the default is (0.86, 0.86, 0.86) (setColor :35222-35225, :21702-21790; back at removal :15679-15691) and Instantiates Effects/titanForm at the hero, world identity, parented with localScale 1 after the growth, so drawn 1.8 x (:35243-35267; destroyed at removal :15709): kill 10, scale 1.8; the growth and tint are the skin cue titanForm (a page part to build); Yield 0.5 (:30047): standby 0.8 s (:29818)",
    "cues": [
     [0, "voice", "titanForm1|titanForm2"],
     [0, "fx", "titanForm_ring"],
     [0.3, "skin", "titanForm", {"kill": 10}],
     [0.3, "fx", "titanForm", {"scale": 1.8, "kill": 10}]
    ]
   }
  }
 },
 "overSwing": {
  "why": "Bison.cs RPC_overSwing (:25083-25687), started by the Charge Attack press while the overPower status is on, with Over Swing #273 (doBeginCharge :5169-5280, :5259): clip (PlayAnimation(overSwing, 0.2) looped, :25464-25467), voice overSwing1 / overSwing2 (Random.Range(0, 2), :25505-25564) and Effects/overSwing_ring at the hero, hero rotation (createEffect :25573-25589; no followState; plays its own Sounds/overSwing) at 0; Yield 0.5 (:25623): moveSpeed 3 (:25219; the page's hero stays in place), the camera's motion blur (:25230-25235) left out; Yield 0.2 (:25629): circles of 6 and 8 m at 0.7 and 0.9 s (:25293), each hit an nAttack_hit at the target + 1.5 m up (:25332): the 10 m target is out of reach (8.8 m away at 0.9 s even in the game, radius 0.3; FindAreaTarget Damage.cs:1074-1124): none; moveSpeed 0 and Yield 0.1 (:25439, :25625): standby 1.0 s (:25379). The Over Power status it needs is always on: overPower_horn2 on the Head bone and overPower_ring (CharacterControl.cs:35003-35040) shown for the tile's 1.2 s (kill 1.2)",
  "cues": [
   [0, "voice", "overSwing1|overSwing2"],
   [0, "fx", "overSwing_ring"],
   [0, "fx", "overPower_horn2", {"bone": "Head", "rot": [-90, 0, 0], "kill": 1.2}],
   [0, "fx", "overPower_ring", {"kill": 1.2}]
  ]
 },
 "prideCrusher": {
  "why": "Bison.cs RPC_prideCrusher (:30710-31241), single rank (dispatch :6048): clip cut in (PlayAnimation(prideCrusher, 0) :31032), moveSpeed 1 (:31041; the hero stays in place), Effects/prideCrusher_ring at the hero, hero rotation (createEffect :31141-31157; plays its own Sounds/prideCrusher) at 0; no voice: Voices/prideCrusher1 / prideCrusher2 (:31073-31132) are in neither BB's resources (mainData's container has only voices/overpride1 / 2, checks/fx_bison_research/skills_b/voice_container.txt) nor TTO's rip, so the game logs 'Cannot find prideCrusher1 voice' and plays none; Yield 0.6 (:31184): the camera shake (:30862) left out, the 8 m box ahead (:30881) misses the 10 m target; Yield 0.2 (:31189): standby 0.8 s (:30962), which cuts prideCrusher_ring (EffectControl followState, life 2 + 1)",
  "cues": [
   [0, "fx", "prideCrusher_ring", 0, 0.8]
  ]
 },
 "slam": {
  "why": "Bison.cs RPC_slam (:21253-21887), max rank sLv 2 (dispatch :6873), Aspect of the Horde #412 on (passives on; getAspectOfTheHordeLv = hasSkill(412) ? 1 : 0): clip cut in (PlayAnimation(slam, 0) :21676), voice slam1 / slam2 (Random.Range(0, 2), :21720-21779) and Effects/slam_ring at the hero, hero rotation (createEffect :21788-21804) at 0; Yield 0.2 (:21835): moveSpeed 7 (:21400; the page's hero stays in place), slam_dust Instantiated at the hero, hero rotation (:21405-21423; plays its own Sounds/slam), aspect_slam at the hero (createEffect :21437-21461; followState, needs the UVScroll part); hit rounds of a 3 m box ahead at 0.2, 0.3, 0.4, 0.5 s (:21600, Yield 0.1 :21839; the 10 m target out of reach); i >= 2 + sLv: standby 0.6 s (:21516-21549), which cuts aspect_slam",
  "cues": [
   [0, "voice", "slam1|slam2"],
   [0, "fx", "slam_ring"],
   [0.2, "fx", "slam_dust"],
   [0.2, "fx", "aspect_slam", 0, 0.6]
  ]
 },
 "trample1": {
  "why": "Bison.cs RPC_trample (:21888-22760), max rank sLv 2 (dispatch :6821), Aspect of the Horde #412 on; the Trample sequence's first step (SEQ trample1@0.9): clip cut in (PlayAnimation(trample1, 0) :22386), moveSpeed -2 (:22401; the hero stays in place), voice trample1 / trample2 (Random.Range(0, 2) :22442-22502, played :22679 / :22700) at 0; Yield 0.3 (:22696): moveSpeed 7 (:22035), Effects/trample2 (the sLv 2 one; sLv 1 = trample1, :22040-22116) at the hero, hero rotation (createEffect :22108; followState, life 4 + 1; plays its own Sounds/trample2), cut when the hero stands at 3.3 s = 2.4 s into trample2 (the page's FX.t restarts at every step, fxStart index.html:4441, so the cut is in trample2's time); phase-1 passes at 0.3, 0.5, 0.7 s (goto IL_12D6 :22133, Yield 0.2 :22703, i++ :22155), each a trample_dust Instantiated at the hero, hero rotation (:22642-22658) and a box behind-to-ahead (:22586; the 10 m target out of reach in place); at i = 3 (0.9 s) the clip changes: trample2's own entry",
  "cues": [
   [0, "voice", "trample1|trample2"],
   [0.3, "fx", "trample2", 0, 2.4],
   [0.3, "fx", "trample_dust"],
   [0.5, "fx", "trample_dust"],
   [0.7, "fx", "trample_dust"]
  ]
 },
 "trample2": {
  "why": "Bison.cs RPC_trample, phase 2 from 0.9 s (times from this clip's start): i >= 3 (:22511): PlayAnimation(trample2, 0) looped (:22515-22518), moveSpeed 9 (:22521), aspect_trample at the hero, hero rotation (Aspect of the Horde #412 on, createEffect :22524-22548; followState, life 3, needs the UVScroll part); 2 + 5 x sLv = 12 passes 0.2 s apart (IL_471 :22197, Yield 0.2 :22686, i++ :22182), each a trample_dust Instantiated at the hero, hero rotation (:22268-22274) and a 3 m box ahead (:22293; the hero stays in place, so the 10 m target is never met: no nAttack_hit); i = 12 at 2.4 s: moveSpeed 0, standby (:22197-22220), which cuts aspect_trample (and trample1's trample2 effect); the SEQ step should be trample2*@2.4 (now @2.6)",
  "cues": [
   [0, "fx", "aspect_trample", 0, 2.4],
   [0, "fx", "trample_dust"], [0.2, "fx", "trample_dust"], [0.4, "fx", "trample_dust"], [0.6, "fx", "trample_dust"],
   [0.8, "fx", "trample_dust"], [1.0, "fx", "trample_dust"], [1.2, "fx", "trample_dust"], [1.4, "fx", "trample_dust"],
   [1.6, "fx", "trample_dust"], [1.8, "fx", "trample_dust"], [2.0, "fx", "trample_dust"], [2.2, "fx", "trample_dust"]
  ]
 },
 "warcry": {
  "why": "The warcry clip is played by four skills: Warcry (RPC_warcry, Bison.cs:27096), Iron Shield (RPC_ironShield, :27799), Diamond Shield (RPC_diamondShield, :28389) and Onslaught (RPC_onslaught, :30615); one tile each (poolChains); the shield tiles show one shield alone (no perfectShield / perfectArmor: those need the other shield already on, CharacterControl.cs:11973-12033)",
  "skills": {
   "warcry": {
    "why": "Bison.cs RPC_warcry (:26715-27286), max rank sLv 2 (dispatch :6598): clip cut in (PlayAnimation(warcry, 0) :27096), voice warcry1 / warcry2 (Random.Range(0, 2), :27137-27233) at 0; Yield 0.3 (:27221): Effects/warcry_ring at the hero, world identity (createEffect :26862-26880; plays its own Sounds/warcry), the camera's motion blur (:26910-26915) left out; Yield 0.3 (:27218): hate and fear on every enemy within 18 + 6 x 2 = 30 m (:26955-26999), the 10 m target included, but fear draws nothing (CharacterControl.cs:35312-35322: ATK / TAL only) and RPC_AddDamage(1, 0 ...) draws nothing; Yield 0.2 (:27223): standby 0.8 s (:27026)",
    "cues": [
     [0, "voice", "warcry1|warcry2"],
     [0.3, "fx", "warcry_ring"]
    ]
   },
   "ironShield": {
    "why": "Bison.cs RPC_ironShield (:27287-27873), single rank (dispatch :5921), Steel Skin #433 on: clip warcry cut in (PlayAnimation(warcry, 0) :27799); Yield 0.3 (:27826): voice ironShield1 / ironShield2 (Random.Range(0, 2) :27535-27594; perfectShield1 / 2 only while diamondShield is on, :27462-27527, never on this tile), Effects/ironShield_ring at the hero, hero rotation (createEffect :27603-27621; followState, life 1 + 1; plays its own Sounds/shield_create), the camera's motion blur (:27651-27656) left out; Yield 0.3 (:27834): the ironShield status, chaAdjust(6) + 2 = 8 s with Steel Skin (:27691-27708): addStatus Instantiates Effects/ironShield at the hero, world identity, parented (CharacterControl.cs:35054-35076; its own looping Sounds/shield), destroyed at removal (:15587-15603): kill 8; Yield 0.2 (:27832): standby 0.8 s (:27729), which cuts ironShield_ring",
    "cues": [
     [0.3, "voice", "ironShield1|ironShield2"],
     [0.3, "fx", "ironShield_ring", 0, 0.8],
     [0.6, "fx", "ironShield", {"kill": 8}]
    ]
   },
   "diamondShield": {
    "why": "Bison.cs RPC_diamondShield (:27874-28465), single rank (dispatch :5947), Mythril Skin #443 on: clip warcry cut in (Rewind, PlayAnimation(warcry, 0) :28386-28389); Yield 0.3 (:28421): voice diamondShield1 / diamondShield2 (Random.Range(0, 2) :28122-28181; perfectShield1 / 2 only while ironShield is on, :28049-28114, never on this tile), Effects/diamondShield_ring at the hero, hero rotation (createEffect :28190-28208; followState, life 1 + 1; plays its own Sounds/shield_create), the camera's motion blur (:28238-28243) left out; Yield 0.3 (:28417): the diamondShield status, chaAdjust(6) + 2 = 8 s with Mythril Skin (:28278-28295): addStatus Instantiates Effects/diamondShield at the hero, world identity, parented (CharacterControl.cs:35085-35107; its own looping Sounds/shield), destroyed at removal (:15609-15625): kill 8; Yield 0.2 (:28425): standby 0.8 s (:28316), which cuts diamondShield_ring",
    "cues": [
     [0.3, "voice", "diamondShield1|diamondShield2"],
     [0.3, "fx", "diamondShield_ring", 0, 0.8],
     [0.6, "fx", "diamondShield", {"kill": 8}]
    ]
   },
   "onslaught": {
    "why": "Bison.cs RPC_onslaught (:30086-30709), single rank (dispatch :5994): clip warcry cut in (PlayAnimation(warcry, 0) :30615); Yield 0.3 (:30652): Effects/onslaught_ring at the hero, world identity (createEffect :30319-30337; plays its own Sounds/warcry), the camera shake (:30357) and motion blur (:30379-30384) left out; no voice: Voices/onslaught1 / onslaught2 (:30251-30310) are in neither BB's resources (checks/fx_bison_research/skills_b/voice_container.txt) nor TTO's rip, so the game plays none; Yield 0.3 (:30647): damage from the hate list on every enemy within 30 m (:30419-30518), RPC_AddDamage(413 ...) draws nothing; Yield 0.2 (:30640): standby 0.8 s (:30545)",
    "cues": [
     [0.3, "fx", "onslaught_ring"]
    ]
   }
  }
 }
```

## Build line for the editor (after the parts)

```
uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py bison
```

It takes every effect and voice the cue file names. For this scope that is:
- Effects: overPower, overPower_horn2, overPower_ring, titanForm_ring, titanForm, overSwing_ring, prideCrusher_ring,
  slam_ring, slam_dust, aspect_slam, trample2, trample_dust, aspect_trample, warcry_ring, ironShield_ring,
  ironShield, diamondShield_ring, diamondShield, onslaught_ring.
- Voices: overPower1/2, titanForm1/2, overSwing1/2, slam1/2, trample1/2, warcry1/2, ironShield1/2, diamondShield1/2.

All of them are in the rip. The voice trample1 / trample2 (`v_trample*.mp3`) and the effect sound trample2
(`trample2.mp3`, sounds/) are different files, as the recipe's crusader1 note. aspect_slam / aspect_trample need the
UVScroll layout in `wardrobe_fx.py` first. Then add UVScroll to `BUILT` in `pipeline/wardrobe_fx_inventory.py`.

## Page changes this scope needs

- SEQ bison: `"Trample: trample1@0.9 trample2*@2.4"` (item 2).
- Optional (question 1): `NEVER_PLAYED.bison = ["volcanicRam"]`.
- Optional (question 4): `"Over Swing: overSwing*@1"`.
- Parts: UVScroll, bone + rot, the `skin` titanForm (scale + tint, shared with Enrage).

## Offers for the Bible (its repo, its rules; not written there)

1. **Over Swing's hits** come at 0.7 and 0.9 s, with standby at 1.0. The bison-skill-reference.md table (:506) says
   0.5 and 0.7. Case 2 only starts the move; the first scan is after `Yield(3, 0.2)` (:25431, :25629).
2. **Slam** makes sLv + 2 hit rounds (4 at Lv 2), at 0.2, 0.3, 0.4 and 0.5 s, with standby at 0.6. The reference
   (:306, :503) says sLv + 1 at 0.3 + 0.1 i: the round at case 2 with i = 0 is missed (:21476 -> :21516).
3. **Trample**: phase 1 at 0.3, 0.5 and 0.7 s, the trample2 switch at 0.9, phase 2 at 0.9 + 0.2 i (12 at Lv 2), and
   standby at 3.3. The reference (:319, :504) says 0.5 / 0.7 / 0.9 and 1.1 + 0.2 i, with the Yield states swapped
   (phase 1 is state 3, :22703; phase 2 is state 4, :22686).
4. **Pride Crusher and Onslaught have no voice in BB or TTO.** The four voice files the code loads don't exist (item 6).

## Open questions (each with my recommendation)

1. **volcanicRam**: an animation no code plays (item 7). Keep the tile with no effects, or hide it with
   NEVER_PLAYED as the Wolf's cast1-3 (the user, 2026-11-09: "Remove the tile")? **Recommend: hide it**, by the
   Wolf's precedent; mention it to the user, since it is a real game animation he may like to keep.
2. **Pride Crusher / Onslaught voices**: none exist in either game. Borrow Over Pride's overPride1 / 2 for Pride
   Crusher (its prerequisite passive), or leave them silent? **Recommend: silent**, as the game (as the Bat's
   Shattering Dream). This is not the Sheep's decision 10 case: TTO has no fix to adopt.
3. **Over Swing's tile wears the Over Power horn and ring** (the status must be on for the skill to happen). Show
   them for the tile (kill 1.2), or leave them to Over Power's own tile? **Recommend: show them** (the cues above):
   in the game Over Swing is never seen without the horns. Drop the two overPower_* cues if not.
4. **Over Swing's length**: the looped tile holds 1.2 s; the game stands at 1.0 s. **Recommend: leave it** (0.2 s of
   swing, no SEQ line). If the user wants the exact time, add `"Over Swing: overSwing*@1"` and make the horn / ring
   kill 1.
5. **Perfect Shield / Perfect Armor** (both shields at once, the Mythril Skin #443 version = perfectArmor): not
   reachable from a single tile. A tile of its own (Iron Shield then Diamond Shield) is possible: perfectShield1 / 2
   voice, perfectArmor at 0.6 s of the second cast, 8 s. **Recommend: no tile.** It is two skills' combination, not a
   skill, and the one-tile-per-skill rule covers skills.
6. **Trample's travel**: the game runs 25.8 m and tramples the 10 m target at about 1.3 and 1.5 s (nAttack_hit at
   the target + 1.5 m). With the hero in place, show those two sparks at 10 m anyway? **Recommend: no**, by the
   in-place convention (Wolf Feral Strike, Penguin decision 8). The sparks would appear with nothing hitting them.
7. **Titan Form's look**: a new `skin` HERO_SKINS entry `titanForm` (hero x 1.8, tint (0.6, 0.7, 1) against the
   default 0.86 grey, 10 s). It needs a page part. **Recommend: build it**, shared with skills_a's Enrage (scale +
   tint, CharacterControl.cs:34717-34729). The growth is the skill's whole look, and the rule is that missing parts
   are built.
8. **The pool tiles' crossfade**: Over Power, Titan Form, Warcry, the shields and Onslaught all cut in
   (`PlayAnimation(..., 0)`), but a pool member with no host SEQ gets a 0.2 s fade (poolChains, index.html:1252).
   **Recommend: leave it**, as the Penguin's Blizzard note (cast_b item 6): 0.2 s of blend, not worth a page change.
9. **Camera motion blur and shakes** (item 10). **Recommend: leave them out** (no page part; the Penguin's Dispell
   precedent). If the user wants them, Over Power / Over Swing / Warcry / the shields / Onslaught (blur) and Pride
   Crusher / Onslaught (shake) would share one camera part.

## Verification

Checker, 2026-11-13 (home PC), read only. Redone from the source: `clip_flow.js` on all ten coroutines, the raw
`MoveNext` of RPC_slam (:21367-21660), RPC_trample (:22002-22704) and RPC_overSwing (:25186-25450) with each opaque
predicate worked out by hand, the yields of the other seven, CharacterControl's status visuals (overPower :35003-35040,
ironShield / diamondShield :35054-35107, titanForm :35205-35267, enrage :34713-34729, removal :15519-15709), my own
`wardrobe_fx.py bison --probe` on the cut effects, the rip's voices / sounds / effects folders, the TTO names /
pseudo-C / metadata strings, and the page (`fxStart` :4440-4441, the followState cut :3954, the bone branch
:3985-3990, `cueOf` :4333-4336, poolChains :1245-1258, LOOPS / HOLD_SECS :1215 / :1222). Outputs in
`checks/fx_bison_research/verify_b/`.

**Confirmed** (no change):
- Every time: Over Power 0 / 0.5 / 0.8; Titan Form 0 / 0.3 / 0.8; Over Swing 0 / 0.5 / circles 0.7 (6 m) and 0.9 (8 m)
  / standby 1.0; Pride Crusher 0 / 0.6 / 0.8; Slam 0 / 0.2 / rounds 0.2-0.5 / standby 0.6 (case 2's `break` at :21482
  falls to :21516 with i = 0, so the round at 0.2 is real: 4 rounds); Trample phase 1 at 0.3 / 0.5 / 0.7 (`goto
  IL_12D6` :22133), trample2 at 0.9 (:22513-22521 predicates true), phase 2 at 0 ... 2.2 (i = 0 dust at the switch via
  `goto IL_471` :22563-22566), standby 2.4 into trample2 (:22197). Warcry / shields / Onslaught 0 / 0.3 / 0.6 / 0.8.
- **The SEQ fix `trample2*@2.4` is right.** On the page the trample2 effect (spawned 0.3 s into trample1, life 4) is
  0.6 + 2.4 = 3.0 s old at the cut, aspect_trample 2.4 (life 3), so both cuts land inside their live phase.
- Rank picks (trample2 at sLv 2, overPower_horn2, 2 + 5 x 2 passes, 2 + sLv rounds), every `Random.Range(0, 2)` voice
  pair, the shields' perfectShield branch (`hasStatus` :27462 / :28049, never on a single tile), Steel / Mythril Skin
  +2 s, every spawn position / rotation (hero position + rotation; warcry_ring and onslaught_ring identity), and the
  hit ranges (Slam 3 m, Pride Crusher 8 m, Trample 3 m / 4 m from 1 m behind, Over Swing 6 / 8 m, Warcry 30 m, Onslaught
  30 m): nothing reaches the 10 m target in place.
- followState: prideCrusher_ring, trample1 / trample2, ironShield_ring, diamondShield_ring true; aspect_slam (life 1) and
  aspect_trample (life 3) true in `probe2.json`; overPower, titanForm_ring, overSwing_ring, slam_ring, warcry_ring,
  onslaught_ring false. Status looks have no EffectControl (diamondShield checked).
- The silent Pride Crusher / Onslaught: no prideCrusher* / onslaught* voice in the BB or Reborn rip (only the effects,
  the sound prideCrusher.wav and the icons). volcanicRam: no `.cs` in the Bible repo names it, and neither TTO's
  names.tsv, pseudo/Bison.c nor its decrypted global-metadata strings (0 hits; `magmaQuakeAxe` has 2).
- The Bible offers (reference :306 / :503 Slam, :319 / :504 Trample, :506 Over Swing) are real differences.
- The page claims (bone branch overwrites the cue's rot; FX.t restarts per step; HERO_SKINS lacks titanForm), all line
  refs spot-checked (key presses, remotes, CharacterControl), and both pools' tile names from poolChains.
- The paste block: valid JSON, times in order, kinds and options all in `wardrobe_fx_check.py`'s KINDS / OPTS (5-value
  cues parse as `{d: c[3], cut: c[4]}` in `cueOf`). The `skin` cue fails the check's HERO_SKINS test until the part is
  built, as the report says.

**Corrections:**
1. Item 8 (TTO): the eleven `pseudo/Bison.c` lines are in file order, not in the order of the names before them. They
   are: diamondShield :2537, ironShield :5644, onslaught :12142, overPower :12717, overSwing :13173, prideCrusher
   :14804, slam :15340, titanForm :16401, trample :16838, warcry :17945, and :22223 = `doBeginCharge`'s overSwing
   literal (function header at pseudo/Bison.c:22190). The claim itself (same coroutines, same literals) stands.
2. Cosmetic: the paste block indents by 1 space; `wardrobe/fx_cues/*.json` uses 2 (keys) / 4 (why, cues). Valid either
   way; re-indent when pasting if the file's look matters.

No time, name, position, random pick, rank, buildability claim or cue changes, so the paste-ready blocks above stand as
written (cue entries, SEQ `"Trample: trample1@0.9 trample2*@2.4"`, the build line).
