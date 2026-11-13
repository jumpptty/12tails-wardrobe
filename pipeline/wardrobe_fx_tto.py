r"""TTO's skill effects for the wardrobe (2026-11-09; plans/fx_wolf/tto.md, build_rules.md agent E): the prefabs a class's
TTO-only skills spawn, read from TTO's decrypted client bundles (the video folder's tto_assets/<date>/dec + catalog.bin,
read only) with UnityPy, in the same JSON shape as pipeline/wardrobe_fx.py's BB effects. Why the bundles and not the rip
(tto.md 4.1): the catalog address is exactly what the game loads (gameassets/characters/heroes/<cls>/effects/<name>,
BaseHero::ArcanaLoad, TTO1102:Wolf::Row6Spawn@0x1F0F050), so the default style never gets mixed up with the Ronin arcana
copy (.../arcana/ronin/effects/<name>, which AssetRipper flattened into X / X_0 at random); and every object reads with a
full type tree (no byte layouts). The office PC decrypts its own TTO install into <repo>/tto_assets/<date> (ASSETS below),
so both PCs build.

  uv run --no-project --with UnityPy --with pillow --with imageio-ffmpeg python -I pipeline/wardrobe_fx_tto.py wolf
builds the class's TTO effects: SKILL_FX[cls] (every prefab its TTO skills spawn) plus every "tto/<prefab>" fx cue in
wardrobe/fx_cues/<cls>.json; --fx a,b builds those instead; --probe [a,b] prints the effects' JSON and writes nothing.
-> wardrobe/data/<cls>/fx.json: effects "tto/<prefab>" and materials "tto_<material>" merged in (every other entry kept),
   wardrobe/data/fx/tex/tto_<texture>.webp, wardrobe/data/<cls>/sfx/<clip>.mp3 (the AudioSources' clips: TTO's default
   clips are BB's own recordings, tto.md 4.3, so they come from BB's rip WAVs through wardrobe_fx.rip_wav)

Output, per node (as wardrobe_fx.effect): {name, parent, pos, rot (x, y, z, w), scale, comps, mats?, active?}, Unity's own
left-handed space (the page mirrors, tto.md 4.4). Components:
- the game's old emitters (EffectControl, ImageEmitter, RingEmitter, LineEmitter): exactly BB's fields and value shapes
  (wardrobe_fx.LAYOUTS: colours / vectors as lists, bools as booleans, a reference as [fileID, pathID]); checked field
  for field against LAYOUTS (TTO has BB's fields in BB's order, tto.md 3)
- TTO's own scripts (GroundHugEmitter, ArcRibbonEmitter, GroundFollower, ...): {"type": <script>, <serialized name>: value}
  with Color -> [r, g, b, a], Vector2/3/4 / Quaternion -> lists, bool fields (by the type tree) -> booleans, references
  resolved (see ref() below; GroundHugEmitter.motes -> {"node": i, "type": "ParticleSystem"})
- Unity components (ParticleSystem, ParticleSystemRenderer, MeshFilter, MeshRenderer, AudioSource, anything else): their
  read_typetree() dict minus m_GameObject, plus "type"; floats rounded to 6 places, +-inf -> +-1e30; references resolved
  (ref()); a ParticleSystem's disabled modules shrink to {"enabled": false}; AudioSource also carries BB's keys clip /
  volume / playOnAwake / loop (what the page plays); a renderer's first materials also go to the node's "mats" (the page
  hands mats[0] to the part)
- meshes (2026-11-10, the Sheep's Codex book and its shards / prism shells): a MeshFilter with a mesh also gets a
  {"type": "StaticMesh", <mesh>} after it (wardrobe/fxparts/mesh.js draws it with the node's MeshRenderer materials); a
  ParticleSystemRenderer's m_Mesh (mesh render mode) carries its geometry inline as "mesh": <mesh>; <mesh> = the BB
  build's shape (pipeline/wardrobe_fx_mesh.py mesh_dict: name, verts, pos, nrm, uv, col, idx, sub). A Mesh reference
  anywhere else is written {"mesh": name}
- Unity 5.5+'s TrailRenderer (its LineParameters: widthCurve, colorGradient, ...) is written as type
  "TrailRendererModern", so wardrobe/fxparts/trail.js (Unity 3.5's layout, BB's) never misreads it; tto_sheep.js draws it
  and LineRenderer. Both lose the shadow / light-probe / ray-tracing plumbing, as MeshRenderer does
- a material whose shader is not one of Unity's legacy particle shaders also carries "props": its floats and colours by
  name (TTO's own TTO/Sheep/* shaders, Standard, Particles/Standard Unlit: tto_sheep.js reads them)
- CODE_MOVERS: a prefab the game's code moves every frame gets that code as a component of its own at the head of the
  root's comps ({"type": "Sheep.BreathFly"}: the coroutine, not a script in the prefab; tto_sheep.js runs it)
- sounds: BB's rip WAV of the clip's name, else TTO's own AudioClip from the bundle (FMOD through UnityPy)
- (2026-11-10, the Penguin: plans/fx_penguin/tto.md section 6) a SkinnedMeshRenderer in the BB build's shape
  (wardrobe_fx_mesh.py: mesh + w / j / bind, bones = node indices, root, mats; mesh.js skins it); Unity's built-in Quad
  (BUILTIN_MESH) inline as a mesh particle's "mesh" where the renderer names it in "unity default resources"; the hero's
  own sounds/ clips the skills play that BB's rip lacks (SKILL_SOUNDS, plus any such "sound" cue) from TTO's bundle ->
  wardrobe/data/<cls>/sfx/<name>.mp3
"""
import argparse
import glob
import importlib.util
import json
import math
import os
import subprocess
import sys

import UnityPy

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "wardrobe", "data")
VIDEO = os.path.join(os.path.dirname(ROOT), "12tails-video")          # extracted inputs, read only (CLAUDE.md)
# the video folder's bundles (home), else this repo's own decrypted copy, the newest date (office 2026-11-10: the TTO
# install's 538 bundles through the Bible's tools/bundle_decrypt.js into <repo>/tto_assets/<date>/dec + catalog.bin,
# git-ignored; after a TTO patch decrypt again into a new date)
ASSETS = next((p for p in [os.path.join(VIDEO, "tto_assets", "2026-11-04")]
               + sorted(glob.glob(os.path.join(ROOT, "tto_assets", "*", "catalog.bin")), reverse=True)
               if os.path.exists(p)), os.path.join(VIDEO, "tto_assets", "2026-11-04"))
ASSETS = os.path.dirname(ASSETS) if ASSETS.endswith("catalog.bin") else ASSETS
BIBLE = next((p for p in (r"D:\12tails", r"C:\Users\Jump\Desktop\12tails") if os.path.isdir(p)), r"D:\12tails")
AA_CATALOG = os.path.join(BIBLE, "DecompiledSource_TTO_2026-11-02", "tools", "aa_catalog.py")

# every prefab the class's TTO skills spawn, default style (tto.md section 0 and 2; the two the page cannot cue because
# they land on a hit enemy, resonanceClaw_burst and windBound, are built too)
SKILL_FX = {
    "wolf": [
        # Blade Surge: TTO1102:Wolf.<RPC_bladeSurge>d__317::MoveNext@0x1F1F640
        "bladeSurge_aura", "bladeSurge_zone", "bladeSurge_cut", "bladeSurge_flicker", "bladeSurge_sheathe",
        "bladeSurge_shatter", "bladeSurge_shards",
        # Resonance Claw: <RPC_resonanceClaw>d__329::MoveNext@0x1F3C1E0 (+ RPC_resonanceBurst@0x1F0DB20 on hit targets)
        "resonanceClaw_charge", "resonanceClaw_rake", "resonanceClaw_wave_twin", "resonanceClaw_wave_light",
        "resonanceClaw_wave_dark", "resonanceClaw_burst",
        # Wind Bound Domain: <RPC_windBoundDomain>d__313::MoveNext@0x1F51890 (+ CharacterControl::AddWindBoundFx@0x24AF350)
        "windBoundDomain_cast", "windBoundDomain_plant", "windBoundDomain_domain", "windBoundDomain_pulse", "windBound",
    ],
    # plans/fx_sheep/tto.md section 3: all 24 Sheep TTO-only prefabs (no arcana style); the ones the page cannot cue (on
    # an enemy, an attacker's reflected hit, the revived ally's status look) are built too
    "sheep": [
        # Gleaming Breath: TTO1102:Sheep.<RPC_gleamingBreath>d__260::MoveNext@0x1E892F0, <BreathFly>d__261@0x1E72EA0,
        # CharacterControl::AddSheepRow6Fx@0x24AE620 (the status look)
        "gleamingBreath_cast", "gleamingBreath_exhale", "gleamingBreath_wisp", "gleamingBreath_land", "gleamingBreath",
        # Lucent Barrier: <RPC_lucentBarrier>d__262::MoveNext@0x1E919A0, Sheep::Row6Beam@0x1E5D640, AddSheepRow6Fx;
        # CharacterControl::LucentReflectFx@0x24B5840 (a reflected hit)
        "lucentBarrier_cast", "lucentBarrier_beam", "lucentBarrier_land", "lucentBarrier",
        "lucentBarrier_reflect", "lucentBarrier_reflectBeam", "lucentBarrier_panel",
        # Grand Codex: <RPC_grandCodex>d__263@0x1E89740, <CodexOpen>d__265@0x1E73940, Sheep::CodexRead@0x1E55B60,
        # <VerdictFall>d__269@0x1E9ECD0, AddSheepRow6Fx (scriptureBind on slowed enemies)
        "grandCodex_cast", "grandCodex_field", "grandCodex_book", "grandCodex_close",
        "grandCodex_page_psalm", "grandCodex_page_seal", "grandCodex_page_verdict",
        "grandCodex_psalm", "grandCodex_seal", "grandCodex_verdict", "grandCodex_spear", "scriptureBind",
    ],
    # plans/fx_penguin/tto.md section 5: all 28 Penguin TTO-only prefabs (no arcana style: the catalog has no
    # heroes/penguin/arcana/); the three status looks on foes (frostMarkFx, frostBiteFx, manaFractureFx) are built too
    "penguin": [
        # Constellation: TTO1102:Penguin.<RPC_constellation>d__340::MoveNext@0x1DE7560 (Penguin.c:6783-7032),
        # <StarLines>d__341::MoveNext@0x1E2C220 (:22423-23060), Penguin::StarImpact@0x1DB1000 (:37493)
        "constellation_cast", "constellation_mark", "constellation_line", "constellation_star", "constellation_impact",
        "constellation_lineFire", "constellation_ignite", "constellation_giant", "constellation_giantImpact",
        # Frost Field: <RPC_frostFieldLeap>d__349::MoveNext@0x1DEF770 (:11314-11556), <FrostFieldLoop>d__350@0x1DC38F0
        # (:1268-1450), Penguin::BurstFx@0x1DA3310 (:38592-38640)
        "frostField_leap", "frostField_trail", "frostField_land", "frostField_field", "frostField_burst",
        # Emperor's March: <RPC_emperorPenguin>d__356::MoveNext@0x1DEA490 (:8457-9102), <FlockRise>d__357@0x1DC31F0
        # (:986-1167), <EmperorShot>d__358@0x1DC1520 (:103-969), GoalFx@0x1DA74E0, Scatter@0x1DB09F0
        "emperorPenguin_whistle", "emperorPenguin_summon", "emperorPenguin_crack", "emperorPenguin_emerge",
        "emperorPenguin_penguin", "emperorPenguin_ball", "emperorPenguin_kick", "emperorPenguin_launch",
        "emperorPenguin_frost", "emperorPenguin_goal", "emperorPenguin_poof",
        # the status looks on foes: CharacterControl::AddPenguinRow6Fx@0x24ADC20 (CharacterControl.c:25195)
        "frostMarkFx", "frostBiteFx", "manaFractureFx",
    ],
    # plans/fx_bat/tto.md sections 2, 5, 6 P3 (2026-11-13): Nightfall Swarm, the released one: TTO1102:Bat.
    # <RPC_nightfallSwarm>d__336::MoveNext (pseudo/Bat.c:18584-19497): the wrap at the cast (Row6Spawn :18863), the burst at
    # her chest at 0.4 s (:18882-18895), the 28 bats (:19013), the hits on the foes passed (:19082-19214), the reform at the
    # landing (:19433)
    "bat": ["nightfallSwarm_wrap", "nightfallSwarm_burst", "nightfallSwarm_bat", "nightfallSwarm_hit", "nightfallSwarm_reform"],
    # plans/fx_bison/parts.md part 10 as its Verification corrects it (2026-11-13, decisions.md 42): the three released
    # skills' 17 prefabs and the status look unchained (TTO1102: addresses; titanDrop_slam is "titanDrop_slam" + (i + 1))
    "bison": [
        # Magma Quake: TTO1102:Bison.<RPC_magmaQuake>d__234::MoveNext@0x1B69E50, <MagmaQuakeTicks>d__239@0x1B5C3A0,
        # Bison::MagmaQuakeImpact@0x1B41710
        "magmaQuake_magmaField", "magmaQuake_quakeField", "magmaQuake_magmaTick", "magmaQuake_quakeTick",
        "magmaQuake_magmaSlam", "magmaQuake_quakeSlam",
        # Titan Drop: <RPC_titanDrop>d__281::MoveNext@0x1B78BD0, Bison::TitanDropCharge@0x1B46C50, <TitanDropRings>d__289@0x1BA91D0
        "titanDrop_takeoff", "titanDrop_mark", "titanDrop_charge", "titanDrop_dive",
        "titanDrop_slam1", "titanDrop_slam2", "titanDrop_slam3",
        # Unchained Fury: <RPC_unchainedFury>d__278::MoveNext@0x1B7BFC0 (+ CharacterControl::AddUnchainedFx@0x24AEB60, the status look)
        "unchainedFury_chains", "unchainedFury_break", "unchainedFury_roar", "unchainedFury_plant", "unchained",
    ],
    # plans/fx_cat/tto.md sections 2 and 5, parts.md "TTO" (2026-11-13, decisions.md 57): the 26 prefabs the released skills
    # spawn (checks/fx_cat_research/parts/catalog_keys.txt, tto_released.json; 24 cued, the two left out below them) and
    # the two status looks unchained (no arcana style: the catalog has no heroes/cat/arcana/)
    "cat": [
        # Royal Flush: TTO1102:Cat.<RPC_royalFlush>d__306::MoveNext@0x1BC7700 (pseudo/Cat.c), Cat::DealHand@0x1B805E0,
        # <RoyalFlushBursts>d__307::MoveNext@0x1BF3F60, <RoyalSwordFall>d__308::MoveNext@0x1BF4840
        "royalFlush_shuffle", "royalFlush_table", "royalFlush_card", "royalFlush_bang", "royalFlush_hand",
        "royalFlush_burst", "royalFlush_burstBig", "royalFlush_sword", "royalFlush_swordHit",
        # Crescent Eclipse: <RPC_crescentEclipse>d__345::MoveNext@0x1BA3320 (Cat.c:3404-4266); the death rupture
        # (left out, decisions.md 44): Cat::RPC_eclipseRupture@0x1B87160 (:42051-42080), only when an eclipsed foe dies
        "crescentEclipse_takeoff", "crescentEclipse_trail", "crescentEclipse_moon", "crescentEclipse_blade",
        "crescentEclipse_ring", "crescentEclipse_dive", "crescentEclipse_land", "crescentEclipse_click",
        "crescentEclipse_burst", "crescentEclipse_rupture",
        # Drop Anchor: <RPC_dropAnchor>d__388::MoveNext@0x1BAA670 (:7137-7303), <DropAnchorFlightAndLand>d__389
        # ::MoveNext@0x1B9D6C0 (:138-384), <AnchorHold>d__391::MoveNext@0x1B9D460; the yank: <RPC_anchorYank>d__394
        # ::MoveNext@0x1B9E500 (:660-856); the anchored foe's chain (left out): Cat_anchorChain.Bind from
        # CharacterControl.<addStatus>d__481::MoveNext (0x24FD823)
        "dropAnchor_anchor", "dropAnchor_slam", "dropAnchor_heave", "dropAnchor_smash", "dropAnchor_shrapnel",
        "dropAnchor_sink", "dropAnchor_chain",
        # the status looks (left out, decisions.md 44): CharacterControl::AddCatRow6Fx@0x24ABBB0 (CharacterControl.c:5791,
        # Cat_row6StatusFx.Init: eclipsed, Crescent Eclipse's burst), CharacterControl::AddCatRow6Status@0x24ABF90
        # (dealersMark: none of the released skills applies it)
        "eclipsed", "dealersMark",
    ],
    # plans/fx_chameleon/tto.md section 5 and Verification 1 (decisions.md 61): all 31 Chameleon TTO-only prefabs (no
    # arcana style); the ghost's own venomPhantom_ghostFire / _ghostShatter (ChameleonAfterimage fireFx / shatterFx, named
    # only by the part: an entry's "builds" never builds a tto/ name, so they must be here), the foe status looks, the kill
    # reward and the storm arrows (not cued) are built too
    "chameleon": [
        # Venom Phantom: TTO1102:Chameleon.<RPC_venomPhantom>d__294::MoveNext@0x1C581A0, <PhantomShot>b__1@0x1BF5870,
        # <RPC_phantomRequiem>d__301::MoveNext@0x1C1B140, EchoFx@0x1BCFE00; AddChameleonRow6Fx (phantomVenom)
        "venomPhantom_coil", "venomPhantom_shot", "venomPhantom_hit", "venomPhantom_ghost", "venomPhantom_ghostFire",
        "venomPhantom_ghostShatter", "venomPhantom_requiem", "venomPhantom_beam", "venomPhantom_rupture",
        "venomPhantom_echo", "phantomVenomFx",
        # Apex Hunt: <RPC_apexHunt>d__304::MoveNext@0x1BF8FB0, ApexVolley@0x1BCE570, <ApexArrow>d__312@0x1BEC9D0,
        # ImpactFx@0x1BD05B0, TrophyFx@0x1BD9270, CharacterControl::AddApexLockFx@0x24AB5A0 (preyFx)
        "apexHunt_crouch", "apexHunt_takeoff", "apexHunt_hang", "apexHunt_loose", "apexHunt_arrow", "apexHunt_impact",
        "apexHunt_land", "apexHunt_trophy", "preyFx",
        # Chain Lightning: <RPC_chainLightning>d__317::MoveNext@0x1BFF820, OverloadFx@0x1BD18B0,
        # <StormDragonForm>d__328@0x1C5B820, StormArrow@0x1BD8290, StormArrowHit@0x1BD8120, HopFx@0x1BD0370;
        # AddChameleonRow6Fx (stormCharge, staticDrain)
        "chainLightning_draw", "chainLightning_overload", "chainLightning_zapHot", "chainLightning_stormDragon",
        "chainLightning_muzzle", "stormChargeFx", "staticDrainFx", "chainLightning_arrow", "chainLightning_zap",
        "chainLightning_bolt", "chainLightning_boltHot",
    ],
    # plans/fx_mole/tto.md section 5 and Verification 4 (decisions.md 56): the 24 prefabs of the released Barrel Railgun,
    # Missile with Twin Warhead and Kaiser Arsenal (the never-spawned gun barrelRailgun left out); the ones the parts spawn
    # (arcs, shocks, warheads, muzzle flashes, hits: no cue names them) must be here, an entry's "builds" never builds a
    # tto/ name
    "mole": [
        # Barrel Railgun: TTO1102:Mole.<RPC_barrelRailgun>d__418::MoveNext@0x1C606D0, <RPC_barrelRailgun_fire>d__424@0x1C62250,
        # <RailRip>d__428@0x1C93700, <RailTrenchSparks>d__427@0x1C93C70, <RPC_barrelRailgun_overload>d__429@0x1C62C00
        "barrelRailgun_turret", "barrelRailgun_line", "barrelRailgun_beam", "barrelRailgun_muzzle", "barrelRailgun_recoil",
        "barrelRailgun_blast", "barrelRailgun_trench", "barrelRailgun_rip", "barrelRailgun_arc", "barrelRailgun_hit",
        "barrelRailgun_overload", "barrelRailgun_shock", "barrelRailgun_lock",
        # Missile with Twin Warhead: <RPC_missile>d__344::MoveNext@0x1C78270, Mole::SpawnMissilePad@0x1C3D4D0,
        # RPC_missile_lock@0x1C352E0, FireMissile@0x1C2B3C0, MissileBotScatter@0x1C2E1E0, RPC_twinImpact@0x1C39D90
        "missilePad", "missilePad_launch", "missileBot_fire", "missileBot_fire_bot", "missileBot_hit", "missile_lock",
        "twinImpact",
        # Kaiser Arsenal: TTO1102:KingKaiser.<RPC_kaiserArsenal>d__72::MoveNext@0x1CB7460, SpawnPods@0x1CB19A0,
        # ArsenalShot@0x1CAF000, RPC_kaiserArsenal_hit@0x1CB0CA0
        "kaiserArsenalPod", "kaiserArsenal_muzzle", "kaiserWarhead", "kaiserArsenal_hit",
    ],
}
# the hero's own sounds/ clips the TTO skills play that BB's rip lacks (Penguin::Row6Sound@0x1DB04B0, Penguin.c:41262:
# GameAssets/characters/heroes/<cls>/sounds/<name>, PlayOneShot on the hero): TTO's own recordings, read from its bundle
# (plans/fx_penguin/tto.md "Read this first" 4, part P8) -> wardrobe/data/<cls>/sfx/<name>.mp3, the "sound" cue's file.
# Every other "sound" cue of fx_cues/<cls>.json that the rip lacks is looked up in TTO's catalog too
SKILL_SOUNDS = {
    # RPC_emperorPenguin: Row6Sound("emperorPenguin_whistle") (:8695), Row6Sound("emperorPenguin_flock") (:9063)
    "penguin": ["emperorPenguin_whistle", "emperorPenguin_flock"],
    # RPC_nightfallSwarm: Row6Sound("nightfallSwarm_screech"), Row6Sound("nightfallSwarm_flap") at 0.4 s (Bat.c:18896-18897;
    # Row6Sound@0x1AD00B0 loads sounds/ only, :45157-45190); "nightfallSwarm" is the clip and command, not a sound
    # (plans/fx_bat/parts.md Verification 2)
    "bat": ["nightfallSwarm_screech", "nightfallSwarm_flap"],
}
# Unity's built-in legacy particle shaders by name, to wardrobe_fx.BUILTIN_BLEND's words (the page's fxMaterial knows
# these); any other shader -> "shader:<name>"
# (2026-11-13, plans/fx_cat/tto.md P8, decisions.md 56, 57: the three names TTO's re-serialised copies give BB's built-ins
# 205 / 206 / 207, wardrobe_fx.BUILTIN_BLEND: the Cat's dropAnchor_smash / royalFlush_swordHit tto_Bomb2 = Multiply
# (Double), dropAnchor_shrapnel tto_Default-Particle = Alpha Blended Premultiply; before, they came out "shader:<name>"
# and fell to the page's alpha-blend default)
SHADER_BLEND = {"Legacy Shaders/Particles/Additive": "add", "Legacy Shaders/Particles/Additive (Soft)": "addsoft",
                "Legacy Shaders/Particles/Alpha Blended": "alpha", "Legacy Shaders/Diffuse": "opaque",
                "Legacy Shaders/Particles/Multiply": "multiply", "Legacy Shaders/Particles/Multiply (Double)": "multiply2",
                "Legacy Shaders/Particles/Alpha Blended Premultiply": "premul"}
DROP = {"m_GameObject"}                          # dropped from every Unity component's dict
MESH_RENDERER_KEEP = {"type", "m_Enabled", "m_Materials", "m_SortingLayerID", "m_SortingLayer", "m_SortingOrder",
                      "m_RendererPriority"}
# the shadow / lightmap / probe / ray-tracing plumbing of a Line- or TrailRenderer (unlit lines never read it)
RENDERER_PLUMBING = ("m_CastShadows", "m_ReceiveShadows", "m_DynamicOccludee", "m_StaticShadowCaster", "m_MotionVectors",
                     "m_LightProbe", "m_ReflectionProbe", "m_RayTrac", "m_SmallMeshCulling", "m_ForceMeshLod",
                     "m_MeshLodSelectionBias", "m_RenderingLayerMask", "m_Lightmap", "m_StaticBatch", "m_ProbeAnchor")
# prefabs the game's code moves every frame (not a script in the prefab): the code becomes the root's first component,
# so the page runs it before the prefab's own parts each frame (wardrobe/fxparts/tto_sheep.js)
CODE_MOVERS = {
    # TTO1102:Sheep.<BreathFly>d__261::MoveNext@0x1E72EA0: mouth -> the revived ally's chest on an up-arc, then Destroy 0.3
    "gleamingBreath_wisp": "Sheep.BreathFly",
    # TTO1102:Sheep.<CodexOpen>d__265::MoveNext@0x1E73940: the book's drop and bob (CodexBob@0x1E55980), its FlipPivot
    # page turns (CodexFlipAngle@0x1E55A00) before each of the ten reads, Destroy(book, 0.1) after the last
    "grandCodex_book": "Sheep.CodexOpen",
    # TTO1102:Penguin.<StarLines>d__341::MoveNext@0x1E2C220 (Penguin.c:22423-23060): each line's two LineRenderers run
    # from its star's mark to the next one's, drawn out over 0.12 s (:22659-22703), widthMultiplier x 2.2 at the ignite
    # (:22833-22834); ClearStarFx destroys it (wardrobe/fxparts/tto_penguin.js)
    "constellation_line": "Penguin.StarLines",
    # <RPC_emperorPenguin>d__356 state 3-4 (Penguin.c:8892-9055: the ball dropped onto ballAt) + <EmperorShot>d__358
    # ::MoveNext@0x1DC1520 (:103-969: rolled 28 m/s to the reach at ground + 0.45, spun 900 deg/s, Destroy at the Goal)
    "emperorPenguin_ball": "Penguin.EmperorShot",
    # <FlockRise>d__357::MoveNext@0x1DC31F0 (:986-1167: up the tilt axis over 0.25 s) + EmperorShot's flock (:588-700:
    # whirled after the ball round the lane, Scatter's Destroy at the Goal)
    "emperorPenguin_penguin": "Penguin.FlockRise",
    # <RPC_nightfallSwarm>d__336 state 2 (Bat.c:19036-19337: each bat along the road with its lag, lane and bob, the hero
    # hidden from HideBody at 0.4 s to ShowBody at 0.9 s) + <Regather>d__337::MoveNext@0x1B25130 (:25281-25507: back to her
    # chest, Row6Chest, shrinking, Destroy after 0.25 s) (plans/fx_bat/tto.md 6 P1; wardrobe/fxparts/tto_bat.js)
    "nightfallSwarm_bat": "Bat.NightfallSwarm",
    # TTO1102:Cat.<RoyalSwordFall>d__308::MoveNext@0x1BF4840 (Cat.c:26104-26412; plans/fx_cat/tto.md 2.1, P3): spun in and
    # grown over 0.35 s, risen 1.2 m, fallen to its `to` - 1.1 up by 0.8 s, held 0.6, sunk and shrunk 0.5, Destroy
    # (wardrobe/fxparts/tto_cat.js)
    "royalFlush_sword": "Cat.RoyalSwordFall",
    # TTO1102:Cat.<DropAnchorFlightAndLand>d__389::MoveNext@0x1B9D6C0 (Cat.c:138-384; tto.md 2.3, P5 and Verification 3):
    # 0.35 s to its `to` on a 12u(1 - u) (3 m) arc with one 360 deg flip about its right axis, then upright there, the
    # inactive Leash node's Edge / Pull RingEmitters held back until that landing (wardrobe/fxparts/tto_cat.js)
    "dropAnchor_anchor": "Cat.DropAnchorFlight",
    # TTO1102:Chameleon.<ApexArrow>d__312@0x1BEC9D0 (Chameleon.c:565-591; plans/fx_chameleon/tto.md 6 P5, parts.md
    # Verification 7): from the spawn to its `to` (hero-relative at the spawn, so it works under Apex Hunt's lift) in
    # 0.12 s, a straight lerp, turned along it; Destroy(arrow, 0.3) after the arrival (wardrobe/fxparts/tto_chameleon.js)
    "apexHunt_arrow": "Chameleon.ApexArrow",
}
# Unity's built-in meshes, which no bundle holds: a PPtr into "Library/unity default resources" by its path id (the
# mesh-particle renderers of emperorPenguin_launch's Ring1-3 and emperorPenguin_goal's Net / Net2 use the Quad,
# plans/fx_penguin/tto.md part P6), in the BB build's mesh shape (wardrobe_fx_mesh.mesh_dict). The Quad (path id 10210):
# 1 x 1 in the XY plane about its centre, facing -z (its normal), uv (0, 0) at (-0.5, -0.5), triangles 0 3 1 / 3 0 2
# (clockwise seen from -z: Unity's front face)
BUILTIN_MESH = {
    10210: {"name": "Quad", "verts": 4, "pos": [-0.5, -0.5, 0, 0.5, -0.5, 0, -0.5, 0.5, 0, 0.5, 0.5, 0],
            "nrm": [0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1], "uv": [0, 0, 1, 0, 0, 1, 1, 1], "col": None,
            "idx": [0, 3, 1, 3, 0, 2], "sub": [[0, 6]]},
}
MB_HEADER = {"m_GameObject", "m_Enabled", "m_Script", "m_Name", "m_EditorHideFlags", "m_EditorClassIdentifier"}


def load_path(name, path):
    """A module by its path (python -I leaves the script's folder off sys.path)."""
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


_bb = None
_mesh = None


def mesh():
    """pipeline/wardrobe_fx_mesh.py (mesh_dict: the BB build's mesh shape)."""
    global _mesh
    if _mesh is None:
        _mesh = load_path("wardrobe_fx_mesh", os.path.join(HERE, "wardrobe_fx_mesh.py"))
    return _mesh


def bb():
    """pipeline/wardrobe_fx.py (LAYOUTS, rip_wav, cue_lists); imported lazily: it needs nothing loaded at import time."""
    global _bb
    if _bb is None:
        _bb = load_path("wardrobe_fx", os.path.join(HERE, "wardrobe_fx.py"))
    return _bb


def num(x):
    """A JSON-safe float: 6 places, +-inf -> +-1e30 (wardrobe_data.py's convention), NaN -> None."""
    if math.isnan(x):
        return None
    if math.isinf(x):
        return 1e30 if x > 0 else -1e30
    return round(x, 6)


class Tto:
    """TTO's bundles for a set of effect addresses: the catalog resolves address -> internal id -> bundles (bundle names
    change every TTO build, so never by file name); each bundle's own AssetBundle m_Container is keyed by the internal id
    (env.container is empty for these, tto.md 4.1)."""

    def __init__(self, cls, names, assets=ASSETS, style="", folder=None):
        self.cls = cls
        cat = load_path("aa_catalog", AA_CATALOG).Catalog(os.path.join(assets, "catalog.bin"))
        # folder: another folder of the class's (pipeline/wardrobe_weapon_fx.py: "weapons", BB's weapons in TTO's client)
        base = f"gameassets/characters/heroes/{cls}/{folder or style + 'effects'}/"
        want = {base + n.lower(): n for n in names}
        self.iid, deps = {}, set()                  # internal id -> prefab name
        for addr, loc in cat.entries():
            if addr in want:
                self.iid[loc["id"]] = want[addr]
                deps.update(loc["bundles"])
        missing = sorted(set(want.values()) - set(self.iid.values()))
        if missing:
            raise SystemExit(f"not in TTO's catalog under {base}: {missing}")
        self.env = UnityPy.load(*[os.path.join(assets, "dec", b) for b in sorted(deps)])
        self.sf = {}                                # serialized file name (lower case) -> file, to follow externals
        for f in self.env.files.values():
            self._collect(f, None)
        self.roots = {}                             # prefab name -> its root GameObject
        for o in self.env.objects:
            if o.type.name == "AssetBundle":
                for k, v in o.read_typetree()["m_Container"]:
                    if k in self.iid:
                        self.roots[self.iid[k]] = o.assets_file.objects[v["asset"]["m_PathID"]]
        self.scripts = {}

    def _collect(self, f, key):
        if type(f).__name__ == "BundleFile":
            for k, sub in f.files.items():
                self._collect(sub, k)
        elif hasattr(f, "objects") and hasattr(f, "externals") and isinstance(key, str):
            self.sf[os.path.basename(key).lower()] = f

    def deref(self, af, p):
        """The object a PPtr names, read against the file that holds the reference; None for a null one or a file not
        loaded (Unity's built-in resources)."""
        if not p or not p.get("m_PathID"):
            return None
        if p["m_FileID"] == 0:
            return af.objects.get(p["m_PathID"])
        f = self.sf.get(os.path.basename(af.externals[p["m_FileID"] - 1].path).lower())
        return f.objects.get(p["m_PathID"]) if f is not None else None

    def builtin_mesh(self, af, p):
        """Unity's own mesh a PPtr names in its built-in resources (BUILTIN_MESH), else None."""
        if not p or not p.get("m_FileID") or p.get("m_PathID") not in BUILTIN_MESH:
            return None
        ext = af.externals[p["m_FileID"] - 1].path.replace("\\", "/").lower()
        return BUILTIN_MESH[p["m_PathID"]] if ext.endswith("unity default resources") else None

    def prefab_of(self, o):
        """The name of the loaded prefab whose hierarchy holds o (a GameObject or a component), else None."""
        go = o if o.type.name == "GameObject" else self.deref(o.assets_file, o.read_typetree().get("m_GameObject"))
        while go is not None:
            tr = next((c for c in (self.deref(go.assets_file, x["component"]) for x in go.read_typetree()["m_Component"])
                       if c is not None and c.type.name == "Transform"), None)
            father = tr.read_typetree()["m_Father"] if tr is not None else None
            if not father or not father.get("m_PathID"):
                break
            ft = self.deref(tr.assets_file, father)
            go = self.deref(ft.assets_file, ft.read_typetree()["m_GameObject"]) if ft is not None else None
        if go is None:
            return None
        return next((n for n, r in self.roots.items() if r.assets_file is go.assets_file and r.path_id == go.path_id), None)

    def script(self, o, t):
        key = (o.assets_file.name, t["m_Script"]["m_FileID"], t["m_Script"]["m_PathID"])
        if key not in self.scripts:
            so = self.deref(o.assets_file, t["m_Script"])
            self.scripts[key] = so.read_typetree()["m_ClassName"] if so is not None else "?"
        return self.scripts[key]


def tto_clips(cls, names, assets=ASSETS):
    """TTO's own AudioClips at gameassets/characters/heroes/<cls>/sounds/<name> (the address Penguin::Row6Sound@0x1DB04B0
    loads, Penguin.c:41262), found through the catalog as the effects are: {name: AudioClip object}; a name the catalog
    lacks is left out."""
    if not names:
        return {}
    cat = load_path("aa_catalog", AA_CATALOG).Catalog(os.path.join(assets, "catalog.bin"))
    base = f"gameassets/characters/heroes/{cls}/sounds/"
    want = {base + n.lower(): n for n in names}
    iid, deps = {}, set()
    for addr, loc in cat.entries():
        if addr in want:
            iid[loc["id"]] = want[addr]
            deps.update(loc["bundles"])
    if not iid:
        return {}
    env = UnityPy.load(*[os.path.join(assets, "dec", b) for b in sorted(deps)])
    out = {}
    for o in env.objects:
        if o.type.name == "AssetBundle":
            for k, v in o.read_typetree()["m_Container"]:
                if k in iid:
                    c = o.assets_file.objects.get(v["asset"]["m_PathID"])
                    if c is not None and c.type.name == "AudioClip":
                        out[iid[k]] = c
    return out


def cue_sounds(cls):
    """The "sound" cue names of wardrobe/fx_cues/<cls>.json ("a|b" = both)."""
    path = os.path.join(ROOT, "wardrobe", "fx_cues", cls + ".json")
    if not os.path.exists(path):
        return []
    out = []
    for entry in json.load(open(path, encoding="utf-8")).values():
        for cues in bb().cue_lists(entry):
            for cue in cues:
                if cue[1] == "sound":
                    out += [n for n in str(cue[2]).split("|") if n not in out]
    return out


class Build:
    """One run's collections: materials and textures (by object, so two different assets with one name never share an
    output name), sounds."""

    def __init__(self, tto):
        self.tto = tto
        self.mats = {}           # output name -> material dict
        self.texs = {}           # output name -> Texture2D object reader
        self.names = {}          # (type, file, pathID) -> output name (materials and textures named apart)
        self.sounds = {}         # clip name -> its AudioClip object (TTO's own, used when BB's rip has no such WAV)

    def out_name(self, o, name):
        key = (o.type.name, o.assets_file.name, o.path_id)
        if key in self.names:
            return self.names[key], False
        used = {v for k, v in self.names.items() if k[0] == key[0]}
        n, i = name, 2
        while n in used:                          # a second asset with the same name: never overwrite the first
            n = f"{name}_{i}"; i += 1
        self.names[key] = n
        return n, True

    def texture(self, o):
        n, new = self.out_name(o, "tto_" + o.read_typetree()["m_Name"])
        if new:
            self.texs[n] = o
        return n

    def material(self, o):
        t = o.read_typetree()
        n, new = self.out_name(o, "tto_" + t["m_Name"])
        if not new:
            return n
        sh = self.tto.deref(o.assets_file, t["m_Shader"])
        shn = sh.read_typetree().get("m_ParsedForm", {}).get("m_Name", "?") if sh is not None else "?"
        props = t["m_SavedProperties"]
        tex, scale, offset, scale_tex = None, [1, 1], [0, 0], None
        for k, v in props["m_TexEnvs"]:
            if k == "_ScaleTex":                   # TTO/ChameleonSpirit's scale pattern (2026-11-13, plans/fx_chameleon/parts.md T2:
                to = self.tto.deref(o.assets_file, v["m_Texture"])   # chmRow6_phantomSpirit / _goldSpirit -> chmRow6_scalesTile)
                if to is not None:
                    scale_tex = self.texture(to)
            if k == "_MainTex":
                to = self.tto.deref(o.assets_file, v["m_Texture"])
                if to is not None:
                    tex = self.texture(to)
                scale = [num(v["m_Scale"]["x"]), num(v["m_Scale"]["y"])]
                offset = [num(v["m_Offset"]["x"]), num(v["m_Offset"]["y"])]
        colors = {k: [num(v[c]) for c in "rgba"] for k, v in props["m_Colors"]}
        self.mats[n] = {"blend": SHADER_BLEND.get(shn, "shader:" + shn), "tex": tex, "scale": scale, "offset": offset,
                        "tint": colors.get("_TintColor"), "color": colors.get("_Color")}
        if scale_tex:                              # exported like _MainTex (data/fx/tex/<name>.webp; fxparts/tto_chameleon.js)
            self.mats[n]["scaleTex"] = scale_tex
        if not shn.startswith("Legacy Shaders/"):  # TTO's own shaders, Standard, Particles/Standard Unlit: every number
            self.mats[n]["props"] = {**{k: num(v) for k, v in props["m_Floats"]}, **colors}
        return n


def bool_fields(o):
    """The names of a MonoBehaviour's top-level bool fields, by its type tree (UnityPy reads them as 0 / 1). TTO's type
    trees write a C# bool as UInt8 (EffectControl's followPosition, m_Enabled); the new scripts' only UInt8 fields are
    bools in TTO's dump.cs (ArcRibbonEmitter.flat :11465, GroundHugEmitter.repeatForever :11671), none is a byte."""
    node = getattr(getattr(o, "serialized_type", None), "node", None)
    return {c.m_Name for c in getattr(node, "m_Children", []) if c.m_Type in ("bool", "UInt8")}


def effect(tto, b, name):
    root = tto.roots[name]
    af = root.assets_file
    # pass 1: every GameObject in the walk's order (depth first, children in order), so a reference to a component or
    # GameObject inside the prefab can name its node before that node is built
    order, where = [], {}                    # where: pathID of a GameObject or component -> (node index, type)
    stack = [(root, -1)]
    while stack:
        go, parent = stack.pop()
        idx = len(order); order.append((go, parent))
        t = go.read_typetree()
        where[go.path_id] = (idx, "GameObject")
        kids = []
        for c in t["m_Component"]:
            co = tto.deref(af, c["component"])
            if co is None:
                continue
            where[co.path_id] = (idx, co.type.name)
            if co.type.name == "Transform":
                kids = [tto.deref(af, tto.deref(af, ch).read_typetree()["m_GameObject"]) for ch in co.read_typetree()["m_Children"]]
        stack.extend((k, idx) for k in reversed(kids))

    def ref(holder, p):
        """A reference: null -> None; inside the prefab -> {"node": i, "type": component type} ({"node": i} for a
        GameObject); Material -> its "tto_" name (exported); Texture2D / Sprite -> its "tto_" texture name (exported);
        AudioClip -> its name (exported to sfx); anything else -> {"asset": type, "name": m_Name}."""
        if not p.get("m_PathID"):
            return None
        if p["m_FileID"] == 0 and p["m_PathID"] in where and holder.assets_file is af:
            i, ty = where[p["m_PathID"]]
            return {"node": i} if ty == "GameObject" else {"node": i, "type": ty}
        o = tto.deref(holder.assets_file, p)
        if o is None:
            return {"asset": "?", "file": p["m_FileID"], "pathID": p["m_PathID"]}
        ty = o.type.name
        if ty == "Material":
            return b.material(o)
        if ty == "Texture2D":
            return b.texture(o)
        if ty == "Sprite":
            to = tto.deref(o.assets_file, o.read_typetree()["m_RD"]["texture"])
            return b.texture(to) if to is not None else None
        if ty == "AudioClip":
            n = o.read_typetree()["m_Name"]
            b.sounds.setdefault(n, o)
            return n
        if ty == "Mesh":                       # geometry is exported where it is drawn (MeshFilter, mesh particles)
            return {"mesh": o.read_typetree().get("m_Name")}
        if ty in ("GameObject", "MonoBehaviour", "Transform"):
            # another prefab of this run (or a component on one): its page name, "tto/<prefab>" (2026-11-13,
            # plans/fx_mole/decisions.md 56, tto.md P4: the rail prefabs' arcPrefab = barrelRailgun_arc's MoleRailArc,
            # which a part spawns by that name, api.spawn)
            pf = tto.prefab_of(o)
            if pf:
                return "tto/" + pf
        # not exported; say so, so the next class's run shows what needs writing
        n = o.read_typetree().get("m_Name")
        print(f"warning: {name}: a {ty} reference ({n}) is written by name only, not exported", file=sys.stderr)
        return {"asset": ty, "name": n}

    def safe(holder, v):
        """A Unity component's type-tree value, JSON-safe, references resolved."""
        if isinstance(v, dict):
            if set(v) == {"m_FileID", "m_PathID"}:
                return ref(holder, v)
            return {k: safe(holder, x) for k, x in v.items()}
        if isinstance(v, (list, tuple)):
            return [safe(holder, x) for x in v]
        if isinstance(v, float):
            return num(v)
        if isinstance(v, bytes):
            return v.hex()
        return v

    def field(holder, v, is_bool):
        """A script field, in wardrobe_fx's shapes: Color -> [r, g, b, a], vectors -> lists, bools -> booleans."""
        if is_bool:
            return bool(v)
        if isinstance(v, dict):
            ks = set(v)
            if ks == {"r", "g", "b", "a"}:
                return [num(v[c]) for c in "rgba"]
            for shape in ("xy", "xyz", "xyzw"):
                if ks == set(shape):
                    return [num(v[c]) for c in shape]
        return safe(holder, v)

    layouts = bb().LAYOUTS
    nodes, anims = [], []
    for idx, (go_obj, parent) in enumerate(order):
        go = go_obj.read_typetree()
        node = {"name": go["m_Name"], "parent": parent, "comps": []}
        if not go.get("m_IsActive", 1):
            node["active"] = False                 # an inactive GameObject: not drawn by the game (the page ignores it)
        nodes.append(node)
        for c in go["m_Component"]:
            co = tto.deref(af, c["component"])
            if co is None:
                continue
            ty = co.type.name
            t = co.read_typetree()
            if ty == "Transform":
                p, r, s = t["m_LocalPosition"], t["m_LocalRotation"], t["m_LocalScale"]
                node["pos"] = [round(p[k], 5) for k in "xyz"]
                node["rot"] = [round(r[k], 6) for k in "xyzw"]
                node["scale"] = [round(s[k], 5) for k in "xyz"]
                continue
            if ty == "MonoBehaviour":
                sname = tto.script(co, t)
                entry = {"type": sname}
                fields = {k: v for k, v in t.items() if k not in MB_HEADER}
                lay = layouts.get(sname)
                if lay is not None and sname in ("EffectControl", "ImageEmitter", "RingEmitter", "LineEmitter"):
                    # the old emitters: BB's shapes exactly (the page draws these already); TTO kept BB's fields
                    if list(fields) != [n for n, _ in lay]:
                        raise ValueError(f"{name}/{node['name']}: TTO's {sname} fields {list(fields)} differ from "
                                         f"wardrobe_fx.LAYOUTS {[n for n, _ in lay]}")
                    for n, kind in lay:
                        v = fields[n]
                        if kind == "b":
                            entry[n] = bool(v)
                        elif kind == "r":
                            entry[n] = [v["m_FileID"], v["m_PathID"]]
                        elif kind in ("f",):
                            entry[n] = round(v, 5)
                        elif kind == "i":
                            entry[n] = v
                        else:
                            entry[n] = [round(v[k], 5) for k in ("rgba" if kind == "c" else "xyzw"[:len(v)])]
                else:
                    bools = bool_fields(co)
                    for n, v in fields.items():
                        entry[n] = field(co, v, n in bools)
                if not t.get("m_Enabled", 1):
                    entry["enabled"] = False
                node["comps"].append(entry)
                continue
            if ty == "Animation":                  # its clips need every node: filled in after the walk (below)
                anims.append((idx, len(node["comps"]), co, t))
                node["comps"].append(None)
                continue
            if ty == "SkinnedMeshRenderer":
                # (2026-11-10, part P3: emperorPenguin_penguin's SmallIcePenguin_tri) the BB build's shape
                # (wardrobe_fx_mesh.py: mesh + w / j / bind, bones = node indices, root, mats), which
                # wardrobe/fxparts/mesh.js skins to the effect's own nodes; m_Enabled kept
                mo = tto.deref(co.assets_file, t["m_Mesh"]) if (t.get("m_Mesh") or {}).get("m_PathID") else None
                if mo is None:
                    print(f"warning: {name}/{node['name']}: a SkinnedMeshRenderer with no mesh", file=sys.stderr)
                    continue
                md = mesh().mesh_dict(mo.read(), skinned=True)
                bones = []
                for bp in t["m_Bones"]:
                    r = ref(co, bp)
                    bones.append(r["node"] if isinstance(r, dict) and "node" in r else None)
                rb = ref(co, t["m_RootBone"]) if t.get("m_RootBone") else None
                mats = [ref(co, m) for m in t["m_Materials"]]
                if len(md["bind"]) != 16 * len(bones) or len(md["w"]) != 4 * md["verts"] or len(md["j"]) != 4 * md["verts"]:
                    raise ValueError(f"{name}/{node['name']}: skin of {md['verts']} vertices, {len(bones)} bones, "
                                     f"{len(md['bind']) // 16} bind poses, {len(md['w'])} weights")
                node["comps"].append({"type": ty, **md, "bones": bones,
                                      "root": rb["node"] if isinstance(rb, dict) and "node" in rb else None, "mats": mats,
                                      "m_Enabled": bool(t.get("m_Enabled", 1))})
                if mats and "mats" not in node:
                    node["mats"] = list(mats)
                continue
            entry = {"type": ty, **{k: safe(co, v) for k, v in t.items() if k not in DROP}}
            if ty in ("MeshFilter", "ParticleSystemRenderer"):
                mo = tto.deref(co.assets_file, t["m_Mesh"]) if (t.get("m_Mesh") or {}).get("m_PathID") else None
                md = mesh().mesh_dict(mo.read()) if mo is not None else None
                if mo is None and (t.get("m_Mesh") or {}).get("m_PathID"):
                    md = tto.builtin_mesh(co.assets_file, t["m_Mesh"])    # Unity's own (the Quad, BUILTIN_MESH)
                    if md is not None:
                        entry["m_Mesh"] = {"mesh": md["name"], "builtin": t["m_Mesh"]["m_PathID"]}
                if md and md["verts"]:
                    if ty == "ParticleSystemRenderer":
                        entry["mesh"] = md
                    else:
                        node["comps"] += [entry, {"type": "StaticMesh", **md}]
                        continue
            if ty in ("LineRenderer", "TrailRenderer"):
                entry = {k: v for k, v in entry.items() if not k.startswith(RENDERER_PLUMBING)}
                if ty == "TrailRenderer" and "m_Parameters" in t:
                    entry["type"] = "TrailRendererModern"
            if ty == "ParticleSystem":             # a disabled module's settings are never read by Unity: kept out
                for k, v in list(entry.items()):
                    if isinstance(v, dict) and v.get("enabled") in (False, 0) and k.endswith("Module"):
                        entry[k] = {"enabled": False}
            elif ty == "MeshRenderer":             # only what drawing reads: the rest (1 KB each, 76 in the Wolf's) is
                # shadow / light-probe / lightmap / ray-tracing plumbing, which the unlit particle shaders never read
                entry = {k: v for k, v in entry.items() if k in MESH_RENDERER_KEEP}
            elif ty == "AudioSource":              # + what the page plays (wardrobe_fx's AudioSource shape)
                clip = entry.get("m_Resource") or entry.get("m_audioClip")
                entry.update({"clip": clip, "volume": num(t.get("m_Volume", 1)),
                              "playOnAwake": bool(t.get("m_PlayOnAwake", 1)), "loop": bool(t.get("Loop", 0))})
            if "m_Materials" in entry and ty.endswith("Renderer") and "mats" not in node:
                node["mats"] = list(entry["m_Materials"])
            node["comps"].append(entry)
    for idx, k, co, t in anims:
        nodes[idx]["comps"][k] = animation(tto, name, nodes, idx, co, t)
    if name in CODE_MOVERS:
        nodes[0]["comps"].insert(0, {"type": CODE_MOVERS[name]})
    return {"nodes": nodes}


def animation(tto, name, nodes, idx, co, t):
    """A legacy Animation in the BB build's shape (wardrobe_fx_mesh.py: {type, clip, play, wrap, clips {name: {len, wrap,
    tracks {node index: {path, q / p / s: keys}}}}}, which wardrobe/fxparts/mesh.js plays), each curve's path found from
    the Animation's node as Unity's Transform.Find does (the first child of that name at each step; this walk's node order
    keeps the children's order); a path that names no node is listed in "lost". A clip with compressed, Euler, float or
    PPtr curves is left out with a warning (2026-11-13, plans/fx_mole/decisions.md 56, tto.md P7: barrelRailgun_rip's drill
    clip root, 3 bones; before, an Animation was written as its raw dict, its clips by name only)."""
    kids = {}
    for i, n in enumerate(nodes):
        kids.setdefault(n["parent"], []).append(i)

    def find(path):
        cur = idx
        for step in [s for s in path.split("/") if s]:
            cur = next((j for j in kids.get(cur, []) if nodes[j]["name"] == step), None)
            if cur is None:
                return None
        return cur

    clips = {}
    for p in t["m_Animations"]:
        cl = tto.deref(co.assets_file, p)
        if cl is None:
            continue
        tt = cl.read_typetree()
        if tt.get("m_Compressed") or any(tt.get(k) for k in ("m_CompressedRotationCurves", "m_EulerCurves", "m_FloatCurves", "m_PPtrCurves")):
            print(f"warning: {name}: clip {tt['m_Name']} has curves the page cannot play (compressed / Euler / float / "
                  "PPtr): left out", file=sys.stderr)
            continue
        tracks, length, lost = {}, 0.0, []
        for field, slot, comps in (("m_RotationCurves", "q", "xyzw"), ("m_PositionCurves", "p", "xyz"),
                                   ("m_ScaleCurves", "s", "xyz")):
            for cv in tt.get(field) or []:
                ks = cv["curve"]["m_Curve"]
                if not ks:
                    continue
                j = find(cv["path"])
                if j is None:
                    lost.append(cv["path"]); continue
                tracks.setdefault(str(j), {"path": cv["path"]})[slot] = mesh()._keys(ks, comps)
                length = max(length, float(ks[-1]["time"]))
        clips[tt["m_Name"]] = {"len": round(length, 4), "wrap": int(tt["m_WrapMode"]), "tracks": tracks,
                               **({"lost": lost} if lost else {})}
    do = tto.deref(co.assets_file, t.get("m_Animation"))
    return {"type": "Animation", "clip": do.read_typetree()["m_Name"] if do is not None else None,
            "play": bool(t.get("m_PlayAutomatically", True)), "wrap": int(t.get("m_WrapMode", 0)), "clips": clips,
            **({} if t.get("m_Enabled", 1) else {"enabled": False})}


def cue_tto(cls):
    """The "tto/<prefab>" names the class's fx cues use ("a|b" = both), without the prefix."""
    path = os.path.join(ROOT, "wardrobe", "fx_cues", cls + ".json")
    if not os.path.exists(path):
        return []
    out = []
    for entry in json.load(open(path, encoding="utf-8")).values():
        for cues in bb().cue_lists(entry):
            for cue in cues:
                if cue[1] == "fx":
                    for n in str(cue[2]).split("|"):
                        if n.startswith("tto/") and n[4:] not in out:
                            out.append(n[4:])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cls")
    ap.add_argument("--fx", default="", help="prefabs to build instead of SKILL_FX[cls] + the cue file's tto/ names")
    ap.add_argument("--probe", nargs="?", const="*", default="", help="print the effects (all, or these) as JSON; writes nothing")
    ap.add_argument("--assets", default=ASSETS, help="TTO's tto_assets/<date> folder (dec/ + catalog.bin)")
    a = ap.parse_args()
    if a.fx:
        names = [n.removeprefix("tto/") for n in a.fx.split(",") if n]
    elif a.probe and a.probe != "*":
        names = [n.removeprefix("tto/") for n in a.probe.split(",") if n]
    else:
        names = list(dict.fromkeys(SKILL_FX.get(a.cls, []) + cue_tto(a.cls)))
    if not names:
        ap.error(f"no TTO effects for {a.cls}: add SKILL_FX['{a.cls}'], tto/ cues, or pass --fx")
    tto = Tto(a.cls, names, a.assets)
    b = Build(tto)
    effects = {"tto/" + n: effect(tto, b, n) for n in names}
    # the hero's own TTO-only sounds (SKILL_SOUNDS, and any "sound" cue BB's rip lacks): TTO's clips, as an effect's
    # own TTO clip below (part P8)
    # (a "sound" cue BB's rip keeps outside the class's sounds/, wardrobe_fx.hero_sound_wav: the Bat's run step_fly1 in
    # Resources/sound/fx, 2026-11-13, is BB's: wardrobe_fx.py builds it)
    hero = [n for n in dict.fromkeys(SKILL_SOUNDS.get(a.cls, []) + cue_sounds(a.cls)) if not bb().hero_sound_wav(a.cls, n)]
    found = tto_clips(a.cls, hero, a.assets)
    for n, o in found.items():
        b.sounds.setdefault(n, o)
    lost = [n for n in hero if n not in found]
    if lost:
        print(f"warning: sounds in neither BB's rip nor TTO's {a.cls}/sounds/: {lost}", file=sys.stderr)
    if a.probe:
        print(json.dumps({"effects": effects, "materials": b.mats, "textures": sorted(b.texs), "sounds": sorted(b.sounds),
                          "hero_sounds": {n: o.read().m_Name for n, o in found.items()}}, indent=1))
        return
    tdir = os.path.join(DATA, "fx", "tex"); os.makedirs(tdir, exist_ok=True)
    for n, o in b.texs.items():
        o.read().image.save(os.path.join(tdir, n + ".webp"), "WEBP", quality=90, method=6)
    # sounds: BB's rip WAV of the same name (TTO's default clips are BB's recordings to the millisecond, tto.md 4.3),
    # 64 kbps mono mp3 as wardrobe_fx.py writes them
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    sdir = os.path.join(DATA, a.cls, "sfx"); os.makedirs(sdir, exist_ok=True)
    missing, own = [], []
    for n in sorted(b.sounds):
        # a hero sound (found above) only from the rip's sounds/ (a voice may share its name); an effect's own anywhere
        src = bb().rip_wav(a.cls, n, "sounds") if n in found else bb().rip_wav(a.cls, n)
        if not src:                            # a TTO-only clip: its own samples (UnityPy decodes them with FMOD)
            try:
                wav = next(iter(b.sounds[n].read().samples.values()))
            except Exception as e:
                print(f"warning: sound {n}: {e!r}", file=sys.stderr)
                missing.append(n); continue
            src = os.path.join(sdir, f"_{n}.wav")
            open(src, "wb").write(wav)
            own.append(n)
        subprocess.run([ff, "-y", "-loglevel", "error", "-i", src, "-ac", "1", "-b:a", "64k", os.path.join(sdir, n + ".mp3")], check=True)
        if n in own:
            os.remove(src)
    out = os.path.join(DATA, a.cls, "fx.json")
    old = json.load(open(out, encoding="utf-8")) if os.path.exists(out) else {}
    merged = {**old, "effects": {**old.get("effects", {}), **effects}, "materials": {**old.get("materials", {}), **b.mats}}
    json.dump(merged, open(out, "w", encoding="utf-8"), separators=(",", ":"), allow_nan=False)   # compact, as wardrobe_fx.py writes it (no NaN: the page refuses one)
    print(f"{a.cls}: {len(effects)} TTO effects, {len(b.mats)} materials, {len(b.texs)} textures, "
          f"{len(b.sounds) - len(missing)} sounds" + (f" ({len(own)} TTO's own: {own})" if own else "")
          + (f", missing sounds: {missing}" if missing else ""))


if __name__ == "__main__":
    main()
