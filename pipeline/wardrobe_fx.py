r"""Skill effects (VFX) and skill sounds for the wardrobe, read from BB's own data (2026-11-09 pilot; user: "let's try
wolf cross break, armor break, and grand cross"). Why not the rip: AssetRipper kept every effect's hierarchy, materials
and Unity's legacy particles, but the game's own emitter scripts (RingEmitter, ImageEmitter, LineEmitter, EffectControl)
come out as a bare m_Script: their settings are only in 12TailsOnline_Data/resources.assets, as raw bytes in the fields'
declaration order (the file's type tree stops at MonoBehaviour's header). So: mainData's ResourceManager maps the
Resources path to the prefab in resources.assets; GameObject / Transform / renderers / legacy particles / AudioSource /
Material read through the type tree; MonoBehaviour fields decoded with LAYOUTS, and every decode must use up exactly
the object's bytes (the self-check); the script's name from its MonoScript in sharedassets0.assets.

Kept in Unity's space (left-handed): the page builds each effect inside a group scaled (-1, 1, 1), the same mirror as
wardrobe_data.py's x -> -x, so positions, rotations and emitter vectors need no conversion here.

  uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py wolf
builds every effect and voice the class's cue file names (wardrobe/fx_cues/<cls>.json, the page's cues: "fx" and
"voice" cues, "a|b" = both; and an entry's "builds", the effects and sounds a page part spawns that no cue names,
2026-11-13); --fx a,b [--voices c,d] builds those instead (probing a skill before its cues are written).
-> wardrobe/data/<cls>/fx.json (effects, materials, which sound each plays), wardrobe/data/fx/tex/<texture>.webp,
   wardrobe/data/<cls>/sfx/<sound>.mp3 (64 kbps mono: plays in every browser)
"""
import argparse
import io
import json
import os
import struct
import subprocess

import UnityPy

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "wardrobe", "data")
BIBLE = next((p for p in (r"D:\12tails", r"C:\Users\Jump\Desktop\12tails") if os.path.isdir(p + r"\12TailsOnline_Data")), r"D:\12tails")
GAME = os.path.join(BIBLE, "12TailsOnline_Data")
RIP = os.path.join(BIBLE, r"RippedAssets\ExportedProject\Assets\Resources\gameassets")
# Unity 3.5's built-in shaders by their id in "unity default resources": the Particle shader files in alphabetical order
# from 200 (Add, AddMultiply, AddSmooth, Alpha Blend ...), which the materials bear out (2026-11-09, 1,200 of them):
# every 200 material saves a _TintColor (Additive has one), 202's mostly don't (Additive (Soft) has none) and its
# textures are 75% alpha-less on black, 203's carry alpha 97% of the time (Alpha Blended); 7 = Diffuse. The same rule one
# step on (plans/fx_penguin/parts.md "Read this first" 4, 2026-11-10; medium sure, the ids are not in the game files):
# 205 = Particles/Multiply (its 24 materials in the rip are BlackTrail, ShadowLine1-4, Smoke4_multiply ...: dark on white),
# so 206 = Particles/Multiply (Double) (15 materials: the Penguin's fallingComet1 and giantComet comet bodies) and 207 =
# Particles/Alpha Blended Premultiply (13: every class's <cls>_dead, netherBane, fireWall). The page draws them in
# fxMaterial (wardrobe/index.html: "multiply2", "premul"). 205 = "multiply" since 2026-11-13 (the Bat's shadow effects:
# ShadowRay, ShadowLine1 / 3, Smoke4_multiply, nightmare_bolt, darkStalker ...; plans/fx_bat/decisions.md 40, parts.md
# part 9: drawn by wardrobe/fxparts/particles.js through api.shader; before, they fell back to "add" and glowed where the
# game darkens). An unknown id still falls back to "add". 205 / 206 / 207 are CERTAIN since 2026-11-13 (plans/fx_cat/
# parts.md "Read this first" 4, decisions.md 56): TTO re-serialised BB's prefabs with Unity's own shader names
# (checks/fx_cat_research/parts/tto_bbcopies.json, tto_probe.json): ShadowLine2 (205) = Legacy Shaders/Particles/Multiply,
# Bomb2 (206; rip Material/Bomb2_0.mat m_Shader fileID 206) = Legacy Shaders/Particles/Multiply (Double), cat_dead (207) =
# Legacy Shaders/Particles/Alpha Blended Premultiply
BUILTIN_BLEND = {200: "add", 202: "addsoft", 203: "alpha", 7: "opaque", 205: "multiply", 206: "multiply2", 207: "premul"}

# serialized fields of the game's scripts, in declaration order: (name, type); f float, i int, b bool (1 byte, then
# aligned to 4), v2 / v3 / c (Color) / q, r (a reference: fileID + pathID, 8 bytes in Unity 3.5)
LAYOUTS = {
    "RingEmitter": [("Life", "f"), ("Delay", "f"), ("Emission", "f"), ("EmissionPeriod", "f"), ("startRadius", "f"),
                    ("endRadius", "f"), ("rndRadius", "f"), ("startHeight", "f"), ("endHeight", "f"), ("rndHeight", "f"),
                    ("startWidth", "f"), ("endWidth", "f"), ("rndWidth", "f"), ("localVelocity", "v3"), ("rndVelocity", "v3"),
                    ("Color1", "c"), ("Color2", "c"), ("Color3", "c"), ("Color4", "c"), ("Color5", "c"),
                    ("localRotation", "v3"), ("uvRotation", "f"), ("ringTri", "i"), ("uvTile", "f"),
                    ("repeatForever", "b"), ("qualitySetting", "i")],
    # EffectControl.cs:549-564 (32 bytes: each bool in its own 4 bytes; effectRotationMode 0 normal, 1 followObject,
    # 2 faceCamera, 3 faceUp, 4 freeze)
    "EffectControl": [("life", "f"), ("afterLife", "f"), ("followPosition", "b"), ("followState", "b"),
                      ("effectRotationMode", "i"), ("velocity", "v3")],
    # ImageEmitter.cs:1275-1366 (188 bytes; ImageEmitterMode 0 FaceCamera, 1 Horizontal, 2 Vertical, 3 LocalRotation)
    "ImageEmitter": [("Emission", "i"), ("EmissionTime", "f"), ("Life", "f"), ("Delay", "f"), ("startHeight", "f"),
                     ("endHeight", "f"), ("startWidth", "f"), ("endWidth", "f"), ("rndScale", "f"), ("rndLife", "f"),
                     ("startPosition", "v3"), ("localVelocity", "f"), ("rndVelocity", "f"), ("worldVelocity", "v3"),
                     ("ImageEmitterMode", "i"), ("useWorldSpace", "b"), ("Color1", "c"), ("Color2", "c"), ("Color3", "c"),
                     ("Color4", "c"), ("Color5", "c"), ("Rotation", "f"), ("rndRotation", "f"), ("startAngle", "f"),
                     ("spreadAngle", "f"), ("repeatForever", "b"), ("mMeshFilter", "r")],
    # LineEmitter.cs:1433-1502 (180 bytes; lineEmitterMode 0 directional, 1 alwaysUp, 2 alwaysHorizontal, 3 faceCamera,
    # 4 localUp; symetry is never read)
    "LineEmitter": [("Life", "f"), ("Delay", "f"), ("Emission", "f"), ("EmissionTime", "f"), ("startRadius", "f"),
                    ("endRadius", "f"), ("rndRadius", "f"), ("startHeight", "f"), ("endHeight", "f"), ("rndHeight", "f"),
                    ("startWidth", "f"), ("endWidth", "f"), ("rndWidth", "f"), ("localVelocity", "v3"), ("rndVelocity", "v3"),
                    ("Color1", "c"), ("Color2", "c"), ("Color3", "c"), ("Color4", "c"), ("Color5", "c"),
                    ("lineEmitterMode", "i"), ("symetry", "b"), ("localRotation", "v3"), ("repeatForever", "b")],
}
# the Wolf's other effect parts (plans/fx_wolf/parts.md, 2026-11-09): every instance in the 12 classes decodes and uses up
# exactly its bytes (VortexEmitter 164 / 31, EmblemEmitter 68 / 24, TrailEmitter 124 / 22, EmitterControl 12 / 32,
# ShatterMesh 56 / 5)
LAYOUTS.update({
    "EmitterControl": [("Delay", "f"), ("Life", "f"), ("AfterLife", "f")],          # EmitterControl.cs:175-181
    "VortexEmitter": [("Life", "f"), ("Delay", "f"), ("startRadius", "f"), ("endRadius", "f"), ("rndRadius", "f"),
                      ("startWidth", "f"), ("endWidth", "f"), ("length", "i"), ("alwaysUp", "b"), ("localVelocity", "v3"),
                      ("Color1", "c"), ("Color2", "c"), ("Color3", "c"), ("Color4", "c"), ("Color5", "c"),
                      ("Rotation", "f"), ("vortexCount", "i"), ("vortexRadian", "f"), ("Spin", "v3"),
                      ("VortexEmitterMode", "i"), ("UVTile", "f"), ("repeatForever", "b")],
    "EmblemEmitter": [("Life", "f"), ("Delay", "f"), ("image", "r"), ("startHeight", "f"), ("endHeight", "f"),
                      ("startWidth", "f"), ("endWidth", "f"), ("rndScale", "f"), ("velocity", "v3"), ("alpha1", "f"),
                      ("alpha2", "f"), ("alpha3", "f"), ("alpha4", "f"), ("alpha5", "f")],
    "TrailEmitter": [("startWidth", "f"), ("endWidth", "f"), ("life", "f"), ("alwaysUp", "b"), ("minDistance", "f"),
                     ("Color1", "c"), ("Color2", "c"), ("Color3", "c"), ("Color4", "c"), ("TrailEmitterMode", "i"),
                     ("uvHeight", "f"), ("localVelocity", "f"), ("worldVelocity", "f"), ("isTimer", "b"), ("delay", "f"),
                     ("easeIn", "f"), ("easeMiddle", "f"), ("easeOut", "f"), ("minQuality", "i")],
    "ShatterMesh": [("Life", "f"), ("Delay", "f"), ("worldVelocity", "v3"), ("localVelocity", "v3"),
                    ("rndVelocity", "v3"), ("rndRotation", "v3")],
})
# the Sheep's parts (plans/fx_sheep/parts.md, 2026-11-10): every AlphaTimer (56) and ProjectileControl (20) in the 12
# classes and the Sheep's 4 Sheep_seal decode and use up exactly their bytes; the Sheep's movers and Eden Sanctuary keep
# every field private (0 field bytes: the empty layout makes the self-check say so)
LAYOUTS.update({
    # AlphaTimer.cs:378-402 (36 bytes): fades its own renderer's _Color, else _TintColor (wardrobe/fxparts/alphatimer.js)
    "AlphaTimer": [("MinAlpha", "f"), ("MaxAlpha", "f"), ("FadeDelay", "f"), ("FadeEaseIn", "f"), ("FadeMiddle", "f"),
                   ("FadeEaseOut", "f"), ("eraseShadow", "b"), ("repeat", "b"), ("endDestroy", "b")],
    # ProjectileControl.cs:72-87 (32 bytes): data only; life is the hero code's (Sheep.cs:9343, :11472, :9838), not this
    "ProjectileControl": [("life", "f"), ("dmg", "f"), ("velocity", "v3"), ("OwnerID", "i"), ("isInitialized", "b"),
                          ("isDestroyed", "b")],
    "Sheep_seal": [("mSealType", "i")],             # Sheep_seal.cs:348 (0 attack, 1 defense, 2 earth, 3 heaven)
    "Sheep_nAttack": [], "Sheep_homingLight": [], "Sheep_cAttack": [], "Sheep_edenSanctuary": [],
})
# the Penguin's parts (plans/fx_penguin/parts.md, 2026-11-10; proved by --probe on this PC's BB data, read only,
# checks/fx_penguin_build/page_pipeline/layouts.txt): every Penguin_tornado / _typhoon (3 each), the arcticEmperor and the
# iceBlock decode and use up exactly their bytes; the other Penguin scripts keep every field private (0 field bytes)
LAYOUTS.update({
    # Penguin_tornado.cs:605, :635, :638 / Penguin_typhoon.cs:515, :557, :560 (28 bytes): mLv = the hit radius (m) and
    # the steering force 11 - mLv; nPosition / nVelocity = the owner's network copy (0 in the prefab)
    "Penguin_tornado": [("mLv", "i"), ("nPosition", "v3"), ("nVelocity", "v3")],
    "Penguin_typhoon": [("mLv", "i"), ("nPosition", "v3"), ("nVelocity", "v3")],
    # Penguin_arcticEmperor.cs:225-246 (32 bytes): AlphaTimer's fade on _TintColor.a plus a second one on _Emission.a
    "Penguin_arcticEmperor": [("MinAlpha", "f"), ("MaxAlpha", "f"), ("MinEmission", "f"), ("MaxEmission", "f"),
                              ("FadeDelay", "f"), ("FadeEaseIn", "f"), ("FadeMiddle", "f"), ("FadeEaseOut", "f")],
    "Penguin_iceBlock": [("mLife", "i"), ("mLv", "i")],     # Penguin_iceBlock.cs:264, :267 (8 bytes); Init overwrites both
    "Penguin_cosmicFriday": [], "Penguin_nAttack": [], "Penguin_manaMissile": [], "Penguin_snowMan": [],
})
# the Mana Vortex summon (Resources characters/elementals/manavortex/ManaVortex, Penguin.cs:10421; plans/fx_penguin/cast_a.md
# "Read this first" 2; checks/fx_penguin_build/page_pipeline/vortex.txt): its BoltEmitter (BoltEmitter.cs:499-553, 152
# bytes: the lightning from the node to TargetObject, drawn by the page's boltEmitter) and ManaVortex (ManaVortex.cs:540-549,
# 28 bytes: data only; the page's ManaVortex part plays its create / root clips)
LAYOUTS.update({
    "BoltEmitter": [("TargetPosition", "v3"), ("TargetObject", "r"), ("TargetCollider", "r"), ("Height", "f"),
                    ("StartWidth", "f"), ("EndWidth", "f"), ("Width1", "f"), ("Width2", "f"), ("Width3", "f"),
                    ("Width4", "f"), ("Width5", "f"), ("rndWidth", "f"), ("rndZigg", "f"), ("Color1", "c"), ("Color2", "c"),
                    ("Color3", "c"), ("Color4", "c"), ("Color5", "c"), ("BoltCount", "i")],
    "ManaVortex": [("novaFlare", "r"), ("mCreator", "r"), ("mCreatorChar", "r"), ("isSummon", "b")],
})
# the Bat's parts (plans/fx_bat/parts.md, 2026-11-13; checks/fx_bat_research/parts/probe.txt: each instance's bytes are
# the listed fields exactly; Bat_nAttack / Bat_illusionFire keep every field private)
LAYOUTS.update({
    "Bat_echoes": [("mTarget", "r"), ("mEchoesLv", "i")],                       # Bat_echoes.cs:577, :580 (12 bytes)
    "Bat_mirageOrb": [("isVisible", "b")],                                       # Bat_mirageOrb.cs:408 (4; Init sets it)
    "Bat_guardianOfTheNight": [("guardianBlade", "r"), ("castEffect", "r")],     # Bat_guardianOfTheNight.cs:169, :175 (16)
    # Bat_illusion.cs:2894-2945 (80 bytes): references only (the clone copies the hero, part 6)
    "Bat_illusion": [("mChar", "r"), ("Weapon", "r"), ("nAttack_fire", "r"), ("nAttack_hit", "r"), ("Bat_drainLife", "r"),
                     ("Bat_drainLife_charge", "r"), ("cAttack_hit", "r"), ("castEffect_illusion", "r"),
                     ("castRing_illusion", "r"), ("illusion_dust", "r")],
    "Bat_nAttack": [], "Bat_illusionFire": [],
    # AudioControl.cs:233-248 (24 bytes; Bat nefariousWhip_hit, and one effect each of Mole, Monkey, Panda, Whale)
    "AudioControl": [("minVolume", "f"), ("maxVolume", "f"), ("delay", "f"), ("fadein", "f"), ("middle", "f"),
                     ("fadeout", "f")],
})
# the Bison's parts (plans/fx_bison/parts.md, 2026-11-13, decisions.md 36, 39; checks/fx_bison_research/parts/probe.txt:
# UVScroll's three instances are its two floats exactly, (0.2, -0.2); Bison_earthRupture / Bison_overLord keep every
# field private)
LAYOUTS.update({
    "UVScroll": [("scroll_x", "f"), ("scroll_y", "f")],   # UVScroll.cs:67, :70 (8 bytes; Bison 2, Cat 1, Whale 1)
    "Bison_earthRupture": [],                             # Bison_earthRupture.cs:218-228: all private (the mover, fxparts/bison.js)
    "Bison_overLord": [],                                 # Bison_overLord.cs:206-215: all private (an aura trigger: draws nothing)
})
# the Cat's parts (plans/fx_cat/parts.md, 2026-11-13, decisions.md 49, 50; checks/fx_cat_research/parts/probe.txt: each
# instance's bytes are the listed fields exactly; UVScroll is the Bison's line above, deltaStrike_tri's (1, 1); StatusControl
# keeps every field private, 0 bytes, so it needs no entry)
LAYOUTS.update({
    "Cat_grandCasinoArcade": [("mRenderer", "r")],        # Cat_grandCasinoArcade.cs:144 (8 bytes: its own SMR; fxparts/cat.js)
    "Cat_supportFire": [("mVelocity", "v3")],             # Cat_supportFire.cs:240 (12 bytes; (0, 0, 30): fxparts/cat.js)
})
# the Chameleon's parts (plans/fx_chameleon/parts.md "LAYOUTS", 2026-11-13; checks/fx_chameleon_research/parts/probe.txt:
# each instance's bytes are the listed fields exactly; Chameleon_nAttack keeps every field private, 0 bytes)
LAYOUTS.update({
    "Chameleon_campFire": [("mLv", "i")],              # Chameleon_campFire.cs:219 (4 bytes: campFire1 1, campFire2 2; draws nothing)
    "Chameleon_needlePrison": [("mPrisonArrow", "r")], # Chameleon_needlePrison.cs:47 (8 bytes: -> needlePrison_arrow; fxparts/chameleon.js)
    "Chameleon_nAttack": [],                           # Chameleon_nAttack.cs: all private (the arrow mover, fxparts/chameleon.js)
})
# BB effects whose Unity 3.5 Shuriken (ParticleSystem + ParticleSystemRenderer) this file does not decode, grafted from
# TTO's client copy of the same prefab (2026-11-13, plans/fx_bison/decisions.md 40, parts.md part 5): magmaClutter_ring2's
# TrailEmitter node carries the swing's puffs; TTO's copy has them decoded but loses the node's Animation `cleave` (the
# swing), so BB's effect stays (its TrailEmitter keeps ["ExplosionRay"] and the swing) and TTO's two components go on a new
# child of that node at local identity. Their material: SHURIKEN_MAT, BB's own of the same shader (TTO's tto_Bomb2 is
# Legacy Shaders/Particles/Multiply (Double); BB's Bomb2 is built-in 206 = multiply2, read from the BB effect named
# beside it), so no TTO texture ships and fxparts/shuriken.js reads it as any node's mats[0]
# The Cat's supportFire_hit (2026-11-13, plans/fx_cat/decisions.md 54, parts.md part 6): its node "ParticleSystem" is a
# Unity 3.5 Shuriken only (12 puffs at 0 in a 25 deg cone); TTO's re-serialised copy matches BB's values field for field
# (checks/fx_cat_research/parts/tto_probe.json, ps_sum.txt), so it is grafted the same way, its material BB's Bomb2 (206,
# multiply2) read from supportFire_hit's own Shuriken renderer (bb_material: effect() skips a ParticleSystemRenderer)
# The Chameleon's thunderDragon_ring2 (2 systems) and zeroShot_ring (3) (2026-11-13, plans/fx_chameleon/parts.md part 7
# and its Verification 4, decisions.md 58): four BB materials (spark3, thunderDragon_particle, zeroShot1 / 2 multiply2,
# zeroShot3), repeated node names (two "ParticleSystem", three "Particle System", two at one spot) and TTO's node order
# not BB's, so a class with no SHURIKEN_MAT entry is grafted otherwise: effect()'s walk keeps each BB
# ParticleSystemRenderer's own materials (node["mats"], node["ps"] = True; only for these listed effects, so every other
# effect's data stays as it was), and graft_shuriken matches each such BB node to the TTO node of the same name whose
# renderer's first material is "tto_" + BB's mats[0] (the next unused one in TTO's order on a tie), its ParticleSystem and
# ParticleSystemRenderer dicts going on the BB node itself with BB's materials (no TTO texture ships). The Bison's and the
# Cat's grafts (SHURIKEN_MAT) are made as before, by node path, onto a "_shuriken" child
# the Mole's parts (plans/fx_mole/parts.md, 2026-11-13; checks/fx_mole_research/parts/probe.txt: each instance's bytes are
# the listed fields exactly; TTO's re-serialised copies name the same fields, checks/fx_mole_research/parts/tto_sum.txt);
# the other Mole scripts keep every field private (0 field bytes)
LAYOUTS.update({
    "Mole_mine": [("mLv", "i")],                     # Mole_mine.cs:239 (4 bytes; mine1-4 = 1-4: the damage rank only)
    "Mole_stunMine": [("mLv", "i")],                 # Mole_stunMine.cs:239 (4; stunMine1-2 = 1-2)
    "Mole_stunGrenade": [("mLv", "i")],              # Mole_stunGrenade.cs:355 (4; 1; RPC_stunGrenade_fire sets it, Mole.cs:11319)
    # Mole_timeNuke.cs:341, :344, :350 (16 bytes: 1 / 2, true, the timeNuke_explosion prefab [24, 386])
    "Mole_timeNuke": [("mLv", "i"), ("isVisible", "b"), ("timeNuke_explosion", "r")],
    "Mole_missile": [("mTarget", "r")],              # Mole_missile.cs:433 (8; [0, 0]: the hero's code sets it, Mole.cs:13189)
    "Mole_warMissile": [("mTarget", "r")],           # Mole_warMissile.cs:345 (8; [0, 0]; Mole.cs:14563)
    # rotationControl.cs:75-84 (16 bytes; flameCarnival_fire/fire_ctrl (0, 180, 0), false; also the Monkey's lavu)
    "rotationControl": [("mRotation_x", "f"), ("mRotation_y", "f"), ("mRotation_z", "f"), ("useWorldRotation", "b")],
    "Mole_bazooka": [], "Mole_cartBomb": [], "Mole_flameCarnival": [], "Mole_grenadeCluster": [], "Mole_mortarShot": [],
    "Mole_napalm": [], "Mole_nAttack": [], "Mole_warCapital": [],
})
# the Mole's summons (Resources characters/robots/<robot>/<prefab>, EXTRA_FOLDERS; plans/fx_mole/decisions.md 32, 34, 53,
# parts.md part 11): data only (fxparts/robots.js plays their clips); every public field in declaration order, all
# references but the ints, BarrelBot's bool and the AIs' string ("s": an int length, the bytes, aligned to 4)
LAYOUTS.update({
    # AutoGyroGun.cs:1056-1089 (36 bytes)
    "AutoGyroGun": [("mChar", "r"), ("mLv", "i"), ("autoGyroGun_fire", "r"), ("nAttack_fx", "r"), ("create_fx", "r")],
    # BarrelBot.cs:1958-2045 (208 bytes)
    "BarrelBot": [("mChar", "r")] + [(n, "i") for n in ("BarrelBotLv", "PunchLv", "HammerLv", "ChopperLv", "MissileLv",
                                                        "CannonLv", "DrillLv")]
                 + [(n, "r") for n in ("nAttack_fx", "nAttack_hit", "punch", "punch_hit", "hammer", "hammer_hit", "chopper",
                                       "chopper_startDust", "chopper_forwardDust", "chopper_hit", "missile_fire",
                                       "missile_hit", "drill_ring", "drill_hit", "cannon", "cannon_fire", "cannon_hit",
                                       "cannonForm_ring")]
                 + [("isCreate", "b"), ("mCreator", "r"), ("mCreatorChar", "r"), ("create_fx", "r")],
    "BarrelBotAI": [("AI_state", "s")],              # BarrelBotAI.cs:1690
    # KingKaiser.cs:1430-1466 (100 bytes)
    "KingKaiser": [("mChar", "r"), ("mLv", "i")] + [(n, "r") for n in (
        "footStep_left", "footStep_right", "nAttack_hit", "kaiserMissile", "kaiserMissile_hit", "kaiserBeam_charge",
        "kaiser_openFx", "kaiserBeam", "kaiser_createFx", "kaiser_box", "kaiser_cryFx")],
    "KingKaiserAI": [("AI_state", "s")],             # KingKaiserAI.cs:1314
    # the hero prefab's own script (heroes/mole/mole, Mole.cs:19403-20084: its 15 public fields, all references, 120
    # bytes), read only for FIELD_PREFABS (the prefabs it holds that no Resources path names)
    "Mole": [(n, "r") for n in ("mChar", "nAttack_fireFx", "nAttack_fire", "nAttack_hit", "skyDrill_hit", "Mole_chopper",
                                "chopper_startDust", "chopper_forwardDust", "chopper_hit", "missileBase", "missile_fire",
                                "missile_hit", "kaiser_dust", "kaiser_box", "deadEffect")],
})
# the scripts whose AudioClip references are written as the clip's name (and the clip exported to sfx/ as any effect's
# sound, wardrobe/data/<cls>/sfx/<name>.mp3): the summons' own sounds their parts play (2026-11-13, plans/fx_mole/
# decisions.md 54: AutoGyroGun's nAttack_fx / create_fx, BarrelBot's, KingKaiser's kaiser_createFx ...; fxparts/robots.js)
# The clip's own bytes, not a rip WAV by name: these clips live outside Resources, and the rip's Assets/AudioClip holds
# several recordings under one name (create, create_0, create_1; nAttack, nAttack_0 ... _14), so a name says nothing. The
# sound is named "<script, first letter lower case>_<clip>" (autoGyroGun_create, barrelBot_nAttack,
# kingKaiser_kaiser_create: two robots' "create" may differ), which the field then holds
SOUND_REFS = {"AutoGyroGun", "BarrelBot", "KingKaiser"}
FIELD_SOUNDS = {}                 # that name -> its AudioClip object (main() writes its samples)
# prefabs a script holds only in a field (no Resources path of their own), built under the field's name: effect name ->
# (the holder prefab's Resources container path, its script, the field) (2026-11-13, plans/fx_mole/decisions.md 54,
# skills_a.md "Read this first" 4: King Kaiser's kaiser_dust / kaiser_box are the Mole prefab's, sharedassets8 path ids 387
# / 379; the Auto Gyro Gun's shot autoGyroGun_fire is AutoGyroGun4's)
FIELD_PREFABS = {"mole": {
    "kaiser_dust": ("gameassets/characters/heroes/mole/mole", "Mole", "kaiser_dust"),
    "kaiser_box": ("gameassets/characters/heroes/mole/mole", "Mole", "kaiser_box"),
    "autoGyroGun_fire": ("gameassets/characters/robots/autogyrogun/autogyrogun4", "AutoGyroGun", "autoGyroGun_fire"),
}}
# the bitmap fonts a script draws with (OnGUI's GUIStyle font), exported when a built effect carries the script:
# script -> (name, its Resources path) (2026-11-13, plans/fx_mole/decisions.md 55, parts.md part 6 and Interfaces 3: the Time
# Nuke's countdown, Mole_timeNuke.cs:65 GameGui/Fonts/GMO24) -> fx.json "fonts": {name: {tex, ascent, line, chars: {char:
# {uv: [x, y, w, h], vert: [x, y, w, h], width}}}}, Unity's numbers as stored: uv in the texture's 0-1 space with its
# origin at the bottom left (the webp's rows are top first, so a pixel row = (1 - uv.y - uv.h) x height), vert the glyph's
# box in pixels from the pen (x right, y up: y -10 and height -9 = the box from 10 px below the line's top, 9 px tall),
# width the pen's advance; the texture data/fx/tex/<name>.webp (Alpha8: the glyphs in its alpha, white rgb)
FONTS = {"Mole_timeNuke": ("GMO24", "gamegui/fonts/gmo24")}
FONTS_USED = set()                # the FONTS entries the run's effects need (effect() adds, main() exports)
# a hero clip another rig plays, added to the effect's root Animation under its name (add_hero_clips): Kaiser Arsenal is
# the King Kaiser's move, TTO's mole/animations/kaiserArsenal crossfaded on the Kaiser's own Animation
# (TTO1102:KingKaiser.<RPC_kaiserArsenal>d__72, KingKaiser.c:308-329; 2026-11-13, plans/fx_mole/decisions.md 37, 56): its 22
# tracks are the Kaiser's bones (Root, Body, Lid ... footTarget_R), which wardrobe_data.py keeps in clips.json from TTO's
# bundle; effect name prefix -> clips
HERO_CLIPS = {"mole": {"KingKaiser_": ["kaiserArsenal"]}}
SHURIKEN_FROM_TTO = {"bison": ["magmaClutter_ring2"], "cat": ["supportFire_hit"],
                     "chameleon": ["thunderDragon_ring2", "zeroShot_ring"],
                     # the Mole's (2026-11-13, plans/fx_mole/parts.md part 8, decisions.md 53): BB Cloud1 / Bomb1_a / Smoke1
                     # -> TTO tto_Cloud1 / tto_Bomb1_a / tto_Smoke1, one system each, by the Chameleon's route
                     "mole": ["bazooka_ring", "napalm_ring", "warCapital"]}
SHURIKEN_MAT = {"bison": ("Bomb2", "magmaClutter_ring1"),   # (BB material, a BB effect of the class that has it)
                "cat": ("Bomb2", "supportFire_hit")}
# a summon's gameplay scripts, kept by name only (no layout: CharacterControl's 684 bytes are the character's stats and
# state, nothing an effect draws)
NOT_DRAWN = {"CharacterControl"}
# effects the hero's code takes from another folder than heroes/<cls>/effects (tried in this order after it): Nova Flare's
# blast is the Mana Vortex's field (ManaVortex.cs:540, Resources characters/elementals/manavortex/effects/novaFlare;
# plans/fx_penguin/own_skills.md "Read this first" 1); the Mana Vortex summon itself (the cue name manaVortex)
# The Mole's summons (2026-11-13, plans/fx_mole/decisions.md 32, 34, 53): AutoGyroGun1-4, BarrelBot1-4, KingKaiser_<colour>
# (Mole.cs:11902-12031, :12472-12601, :35720-35794)
EXTRA_FOLDERS = {"penguin": ["gameassets/characters/elementals/manavortex/effects", "gameassets/characters/elementals/manavortex"],
                 "mole": ["gameassets/characters/robots/autogyrogun", "gameassets/characters/robots/barrelbot",
                          "gameassets/characters/robots/kingkaiser"]}
# an effect the page names otherwise than its prefab, because the class's own folder has a prefab of that name too: the
# name -> its Resources container path, tried before the class's folder (2026-11-13, plans/fx_bat/parts.md Interfaces 6:
# Guardian of the Night's hits are Shade4's Effects/nAttack_hit, Bat.cs:12606-12619, not the Bat's own nAttack_hit)
# (2026-11-13, plans/fx_cat/decisions.md 55, skills_a.md part 3: Casino Doom's doom is the Bat's effect, the status look
# CharacterControl.cs:40491 loads from heroes/bat/effects whoever holds it; one effect, not the whole Bat folder)
ALIASES = {"bat": {"guardian_hit": "gameassets/characters/elementals/shade4/effects/nattack_hit"},
           "cat": {"doom": "gameassets/characters/heroes/bat/effects/doom"}}
# the same for a sound (rip_wav): the name -> its WAV under the rip's gameassets, without ".wav" (the guardian's swing is
# Shade4's Sounds/nAttack, Bat_guardianOfTheNight.cs:1047; the Bat's own sounds/nAttack.wav would win by name)
SOUND_ALIASES = {"bat": {"guardian_nAttack": "characters/elementals/shade4/sounds/nAttack"}}
SIZES = {"f": 4, "i": 4, "v2": 8, "v3": 12, "c": 16, "q": 16, "r": 8}


def decode(raw, layout, off):
    """The fields after the MonoBehaviour header; raises when the layout doesn't use up exactly the object's bytes."""
    out = {}
    for name, ty in layout:
        if ty == "b":
            out[name] = bool(raw[off]); off = (off + 4) & ~3
        elif ty == "i":
            out[name] = struct.unpack_from("<i", raw, off)[0]; off += 4
        elif ty == "r":
            out[name] = list(struct.unpack_from("<ii", raw, off)); off += 8
        elif ty == "s":                  # a string: its byte length, the UTF-8 bytes, aligned to 4
            n = struct.unpack_from("<i", raw, off)[0]
            out[name] = raw[off + 4:off + 4 + n].decode("utf-8"); off = (off + 4 + n + 3) & ~3
        else:
            n = SIZES[ty] // 4
            v = struct.unpack_from(f"<{n}f", raw, off); off += 4 * n
            out[name] = v[0] if n == 1 else [round(x, 5) for x in v]
    if off != len(raw):
        raise ValueError(f"layout used {off} of {len(raw)} bytes")
    return {k: round(v, 5) if isinstance(v, float) else v for k, v in out.items()}


def header_len(raw):
    """m_GameObject (8) + m_Enabled (4) + m_Script (8) + m_Name (int length + bytes, aligned to 4)."""
    n = struct.unpack_from("<i", raw, 20)[0]
    return 24 + ((n + 3) & ~3)


class Game:
    def __init__(self):
        self.env = UnityPy.load(*(os.path.join(GAME, f) for f in ("mainData", "resources.assets", "sharedassets0.assets")))
        self.files = {os.path.basename(k): f for k, f in self.env.files.items()}
        self.ra = self.files["resources.assets"]
        md = self.files["mainData"]
        rm = next(o for o in md.objects.values() if o.type.name == "ResourceManager").read_typetree()
        self.container = {k: v for k, v in rm["m_Container"]}
        self.scripts = {}

    def obj(self, pptr, base=None):
        """The object a PPtr names, read against the file that holds the reference (fileID 0 = that file; each file
        numbers its externals its own way); a sharedassets file is loaded the first time it is named. None when the
        file isn't in the game folder (Unity's built-in resources)."""
        base = base or self.ra
        fid, pid = (pptr["m_FileID"], pptr["m_PathID"]) if isinstance(pptr, dict) else pptr
        if fid == 0:
            return base.objects.get(pid)
        name = os.path.basename(base.externals[fid - 1].path)
        if name not in self.files and os.path.exists(os.path.join(GAME, name)):
            env = UnityPy.load(os.path.join(GAME, name))
            self.files.update({os.path.basename(k): f for k, f in env.files.items()})
        f = self.files.get(name)
        return f.objects.get(pid) if f else None

    def script_name(self, raw, base=None):
        """The MonoBehaviour's script, its PPtr read against the file holding the component (base; resources.assets by
        default; Mole megapunch_hit's are in another file, 2026-11-09)."""
        base = base or self.ra
        fid, pid = struct.unpack_from("<ii", raw, 12)
        key = (base.name, fid, pid)
        if key not in self.scripts:
            o = self.obj((fid, pid), base)
            self.scripts[key] = o.read_typetree()["m_ClassName"] if o is not None and o.type.name == "MonoScript" else f"?{fid}:{pid}"
        return self.scripts[key]


_mesh = None


def mesh_module():
    """pipeline/wardrobe_fx_mesh.py, loaded by its path (python -I leaves the script's folder off sys.path)."""
    global _mesh
    if _mesh is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location("wardrobe_fx_mesh", os.path.join(HERE, "wardrobe_fx_mesh.py"))
        _mesh = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_mesh)
        _mesh.clip_dict = clip_dict                    # its Animation reader takes this file's clip reader (below)
    return _mesh


def clip_dict(game, clip_obj, anim_tr):
    """wardrobe_fx_mesh.clip_dict, which every Animation of an effect goes through, plus a clip's AnimationEvents
    (2026-11-13, plans/fx_mole/decisions.md 34, parts.md part 11: the King Kaiser's clips did not extract, "compressed /
    float curves / events are not read yet"; probed on this PC: none of KingKaiser_<colour>'s clips is compressed or has
    float curves, its run carries two events, the footsteps, KingKaiser.cs footStep_left / _right): the events as
    "events": [[time, functionName, stringParameter], ...] (data: nothing on the page fires them), the rest as that
    reader's. A compressed clip or float curves still raise (none in any effect or summon the cue files name)."""
    tt = clip_obj.read_typetree()
    if tt.get("m_Compressed") or tt.get("m_CompressedRotationCurves") or tt.get("m_FloatCurves"):
        raise ValueError(f"clip {tt['m_Name']}: compressed / float curves are not read yet")
    M = mesh_module()
    tracks, length, lost = {}, 0.0, []
    for field, slot, comps in (("m_RotationCurves", "q", "xyzw"), ("m_PositionCurves", "p", "xyz"),
                               ("m_ScaleCurves", "s", "xyz")):
        for cv in tt.get(field) or []:
            ks = cv["curve"]["m_Curve"]
            if not ks:
                continue
            t = M._find(game, anim_tr, cv["path"])
            if t is None:
                lost.append(cv["path"]); continue
            tr = tracks.setdefault(str(M._node_of(game, t)), {"path": cv["path"]})
            tr[slot] = M._keys(ks, comps)
            length = max(length, float(ks[-1]["time"]))
    out = {"len": round(length, 4), "wrap": int(tt["m_WrapMode"]), "tracks": tracks}
    if lost:
        out["lost"] = lost
    if tt.get("m_Events"):
        out["events"] = [[round(float(e["time"]), 5), e["functionName"], e.get("data", "")] for e in tt["m_Events"]]
    return tt["m_Name"], out


def material(game, pptr, base, mats, texs):
    o = game.obj(pptr, base)
    if o is None:
        return None
    t = o.read_typetree()
    name = t["m_Name"]
    if name in mats:
        return name
    sh, own = t["m_Shader"], o.assets_file
    if sh["m_FileID"] and "default resources" in own.externals[sh["m_FileID"] - 1].path:
        blend = BUILTIN_BLEND.get(sh["m_PathID"], "add")
    else:                                             # the game's own shader: named in its source's first line
        so = game.obj(sh, own)
        src = so.read_typetree().get("m_Script", "") if so else ""
        blend = "shader:" + (src.split('"')[1] if src.count('"') >= 2 else "?")
    props = t["m_SavedProperties"]
    tex = None; scale = [1, 1]; offset = [0, 0]
    key = lambda k: k["name"] if isinstance(k, dict) else k     # Unity 3.5: FastPropertyName {name}
    for k, v in props["m_TexEnvs"]:
        if key(k) == "_MainTex":
            to = game.obj(v["m_Texture"], own)
            if to is not None:
                tex = to.read().m_Name
                if tex not in texs:
                    texs[tex] = to
            scale = [v["m_Scale"]["x"], v["m_Scale"]["y"]]; offset = [v["m_Offset"]["x"], v["m_Offset"]["y"]]
    colors = {key(k): [v["r"], v["g"], v["b"], v["a"]] for k, v in props["m_Colors"]}
    mats[name] = {"blend": blend, "tex": tex, "scale": scale, "offset": offset,
                  "tint": colors.get("_TintColor"), "color": colors.get("_Color"),
                  # FX/Phoenix's Emission [_Emission] (rip Assets/Resources/gameassets/shader/Phoenix.shader; fxparts/mesh.js),
                  # Transparent/AdditiveSaturate's pass-2 glow too (AdditiveSaturate.shader:27-43)
                  "emission": colors.get("_Emission")}
    # DiffuseAmbient's Ambient [_Ambient] (rip shader/diffuseambient.shader:1-19; the Penguin's snowMan), only when saved
    # (no other material has it: the other materials' data stays as it was)
    if colors.get("_Ambient") is not None:
        mats[name]["ambient"] = colors["_Ambient"]
    # Transparent/AdditiveAlpha's _AdditiveRange (2026-11-13, plans/fx_cat/parts.md part 3, decisions.md 52; rip
    # shader/AdditiveAlpha.shader:1-34: pass 1 lit with alpha test >= it, pass 2 additive with <= it; default 0.9) as
    # "cut", as wardrobe_data.py:281-297 does for the props (the Cat's supportFire_fire ball, PirateCannon_Fire 0.9; the
    # Mole's napalm / nAttack later; wardrobe/fxparts/additivealpha.js)
    if blend == "shader:Transparent/AdditiveAlpha":
        floats = {key(k): v for k, v in props.get("m_Floats", [])}
        mats[name]["cut"] = round(float(floats.get("_AdditiveRange", 0.9)), 4)
    return name


def field_prefab(game, holder, script, field):
    """The root GameObject of the prefab the holder prefab's `script` keeps in `field` (FIELD_PREFABS): the script's bytes
    decoded with its LAYOUTS entry, the reference read against the component's own file."""
    go_obj = game.obj(game.container[holder], game.files["mainData"])
    for comp in go_obj.read_typetree()["m_Component"]:
        c = game.obj(comp[1] if isinstance(comp, (list, tuple)) else comp.get("second", comp.get("component")), go_obj.assets_file)
        if c is None or c.type.name != "MonoBehaviour":
            continue
        raw = c.get_raw_data()
        if game.script_name(raw, c.assets_file) == script:
            o = game.obj(decode(raw, LAYOUTS[script], header_len(raw))[field], c.assets_file)
            if o is None or o.type.name != "GameObject":
                raise ValueError(f"{holder} {script}.{field}: no prefab")
            return o
    raise ValueError(f"{holder}: no {script} script")


def effect(game, cls, name, mats, texs, sounds):
    key = ALIASES.get(cls, {}).get(name, f"gameassets/characters/heroes/{cls}/effects/{name.lower()}")
    if key not in game.container:                    # another folder the class's code loads it from (EXTRA_FOLDERS)
        key = next((k for k in (f"{f}/{name.lower()}" for f in EXTRA_FOLDERS.get(cls, [])) if k in game.container), key)
    if key not in game.container and name in FIELD_PREFABS.get(cls, {}):
        root = field_prefab(game, *FIELD_PREFABS[cls][name])
    else:
        root = game.obj(game.container[key], game.files["mainData"])
    nodes, at = [], {}                                # at: (file, GameObject pathID) -> node index (a script's GameObject reference)

    def walk(go_obj, parent):
        go = go_obj.read_typetree()
        node = {"name": go["m_Name"], "parent": parent, "comps": []}
        idx = len(nodes); nodes.append(node)
        at[(go_obj.assets_file.name, go_obj.path_id)] = idx
        tr_children = []
        for comp in go["m_Component"]:                 # Unity 3.5: (classID, reference) pairs
            c = game.obj(comp[1] if isinstance(comp, (list, tuple)) else comp.get("second", comp.get("component")), go_obj.assets_file)
            if c is None:
                continue
            ty = c.type.name
            if ty == "Transform":
                t = c.read_typetree()
                p, r, s = t["m_LocalPosition"], t["m_LocalRotation"], t["m_LocalScale"]
                node["pos"] = [round(p["x"], 5), round(p["y"], 5), round(p["z"], 5)]
                node["rot"] = [round(r["x"], 6), round(r["y"], 6), round(r["z"], 6), round(r["w"], 6)]
                node["scale"] = [round(s["x"], 5), round(s["y"], 5), round(s["z"], 5)]
                tr_children = t["m_Children"]
            elif ty == "MonoBehaviour":
                raw = c.get_raw_data()
                sname = game.script_name(raw, c.assets_file)
                lay = LAYOUTS.get(sname)
                entry = {"type": sname}
                if lay is not None:
                    entry.update(decode(raw, lay, header_len(raw)))
                    if sname in SOUND_REFS:            # its AudioClips by name (SOUND_REFS), exported from the game's bytes
                        for fname, fty in lay:
                            o = game.obj(entry[fname], c.assets_file) if fty == "r" and entry[fname][1] else None
                            if o is not None and o.type.name == "AudioClip":
                                entry[fname] = f"{sname[0].lower()}{sname[1:]}_{o.read().m_Name}"
                                FIELD_SOUNDS[entry[fname]] = o
                                sounds.add(entry[fname])
                    if sname == "BoltEmitter":            # its TargetObject: a node of this prefab (BoltTarget), by index
                        ref = game.obj(entry["TargetObject"], c.assets_file) if entry["TargetObject"][1] else None
                        refs.append((entry, ref))
                elif sname in NOT_DRAWN:
                    pass
                elif len(raw) > header_len(raw):
                    raise ValueError(f"{name}/{node['name']}: no layout for {sname} ({len(raw) - header_len(raw)} field bytes)")
                if sname in FONTS:
                    FONTS_USED.add(FONTS[sname])
                if sname == "EmblemEmitter":           # its picture: a Texture2D reference, exported like a material's
                    to = game.obj(entry["image"], c.assets_file)
                    if to is not None:
                        img = to.read()
                        entry["imageTex"] = img.m_Name
                        entry["imageSize"] = [img.m_Width, img.m_Height]   # the emblem's pixel size (fxparts/emblem.js)
                        texs.setdefault(entry["imageTex"], to)
                node["comps"].append(entry)
            elif ty in ("MeshRenderer", "ParticleRenderer"):
                t = c.read_typetree()
                node["mats"] = [material(game, m, c.assets_file, mats, texs) for m in t["m_Materials"]]
                if ty == "ParticleRenderer":
                    node["comps"].append({"type": ty, **{k: v for k, v in t.items() if not k.startswith("m_") or k in ("m_StretchParticles", "m_LengthScale", "m_VelocityScale", "m_MaxParticleSize", "m_CameraVelocityScale", "UV Animation")}})
            elif ty == "ParticleSystemRenderer" and name in SHURIKEN_FROM_TTO.get(cls, []) and cls not in SHURIKEN_MAT:
                # a Unity 3.5 Shuriken's own materials (2026-11-13, the Chameleon's thunderDragon_ring2 / zeroShot_ring:
                # SHURIKEN_FROM_TTO's comment): graft_shuriken matches TTO's node by them and keeps them
                node["mats"] = [material(game, m, c.assets_file, mats, texs) for m in c.read_typetree()["m_Materials"]]
                node["ps"] = True
            # Unity built-ins: their fields as stored (+ a trail's materials); WorldParticleCollider since 2026-11-13
            # (plans/fx_cat/parts.md part 5, decisions.md 53: the Cat's luckyDice / treasureHunt legacy particles bounce on
            # the floor: m_BounceFactor, m_CollisionEnergyLoss, m_CollidesWith {m_Bits}, m_SendCollisionMessage,
            # m_MinKillVelocity; wardrobe/fxparts/worldcollider.js)
            elif ty in ("TrailRenderer", "Light", "WorldParticleCollider"):
                t = c.read_typetree()
                entry = {"type": ty, **{k: v for k, v in t.items() if k not in ("m_GameObject", "m_Materials")}}
                if "m_Materials" in t:
                    entry["mats"] = [material(game, m, c.assets_file, mats, texs) for m in t["m_Materials"]]
                node["comps"].append(json.loads(json.dumps(entry, default=str)))
            elif ty in ("MeshFilter", "SkinnedMeshRenderer", "Animation"):
                # meshes and legacy animations: pipeline/wardrobe_fx_mesh.py (its own file, so the mesh work stays apart)
                got = mesh_module().component(game, c, ty, node, {"cls": cls, "effect": name, "mats": mats, "texs": texs,
                                                                     "sounds": sounds, "material": material})
                if got:
                    node["comps"].extend(got)
            elif ty in ("EllipsoidParticleEmitter", "ParticleAnimator"):
                t = c.read_typetree()
                node["comps"].append({"type": ty, **{k: v for k, v in t.items() if k not in ("m_GameObject", "m_Enabled")}})
            elif ty == "AudioSource":
                t = c.read_typetree()
                clip = game.obj(t["m_audioClip"], c.assets_file)
                if clip is not None:
                    sn = clip.read().m_Name
                    sounds.add(sn)
                    node["comps"].append({"type": "AudioSource", "clip": sn, "volume": t.get("m_Volume", 1),
                                          "playOnAwake": bool(t.get("m_PlayOnAwake", 1)), "loop": bool(t.get("Loop", 0))})
        for ch in tr_children:
            tro = game.obj(ch, go_obj.assets_file)
            if tro is not None:
                walk(game.obj(tro.read_typetree()["m_GameObject"], tro.assets_file), idx)

    refs = []
    walk(root, -1)
    for entry, ref in refs:                           # resolved once every node is known (the target may come later)
        entry["TargetNode"] = at.get((ref.assets_file.name, ref.path_id), -1) if ref is not None else -1
    for prefix, clips in HERO_CLIPS.get(cls, {}).items():
        if name.startswith(prefix):
            add_hero_clips(cls, nodes, clips)
    return {"nodes": nodes}


def font(game, name, path):
    """A FONTS entry: (its fx.json "fonts" dict, the texture as a PIL RGBA image: white, the glyphs in its alpha). The
    Resources container lists the Font and its texture under one path (ResourceManager's m_Container keeps both pairs:
    Game.container keeps only the last), so the pairs are walked for the Font."""
    from PIL import Image
    md = game.files["mainData"]
    rm = next(o for o in md.objects.values() if o.type.name == "ResourceManager").read_typetree()
    fo = next(o for o in (game.obj(v, md) for k, v in rm["m_Container"] if k == path) if o is not None and o.type.name == "Font")
    t = fo.read_typetree()
    img = game.obj(t["m_Texture"], fo.assets_file).read().image.convert("RGBA")
    a = img.getchannel("A")
    img = Image.new("RGBA", img.size, (255, 255, 255, 0)); img.putalpha(a)
    r = lambda d: [round(d[k], 6) for k in ("x", "y", "width", "height")]
    chars = {chr(c["index"]): {"uv": r(c["uv"]), "vert": r(c["vert"]), "width": c["width"]}
             for c in t["m_CharacterRects"] if 32 <= c["index"] < 127}
    return {"tex": name, "ascent": t["m_Ascent"], "line": round(t["m_LineSpacing"], 4), "chars": chars}, img


def add_hero_clips(cls, nodes, clips):
    """HERO_CLIPS: the class's hero clips (wardrobe/data/<cls>/clips.json, wardrobe_data.py's: a track per bone name, x
    mirrored: q (x, -y, -z, w), p (-x, y, z), the slopes too) put back into Unity's space on the effect's root Animation,
    each track on the first node of that name (walk order), its path the names below the root; a bone the effect lacks is
    listed in the clip's "lost"."""
    path = os.path.join(DATA, cls, "clips.json")
    anim = next((c for c in nodes[0]["comps"] if c["type"] == "Animation"), None)
    if anim is None or not os.path.exists(path):
        raise ValueError(f"{nodes[0]['name']}: no root Animation, or no {path}, for the hero clips {clips}")
    data = json.load(open(path, encoding="utf-8"))
    paths = node_paths(nodes)
    first = {}
    for i, n in enumerate(nodes):
        first.setdefault(n["name"], i)
    sign = {"q": (1, -1, -1, 1), "p": (-1, 1, 1), "s": (1, 1, 1)}
    for clip in clips:
        c = data[clip]
        tracks, lost = {}, []
        for bone, tr in c["tracks"].items():
            i = first.get(bone)
            if i is None or i == 0:
                lost.append(bone); continue
            out = tracks.setdefault(str(i), {"path": paths[i]})
            for slot, rows in tr.items():
                s = sign[slot]; n = len(s)
                out[slot] = [[r[0]] + [x * s[k % n] for k, x in enumerate(r[1:])] for r in rows]
        anim["clips"][clip] = {"len": c["len"], "wrap": 2 if c.get("loop") else 0, "tracks": tracks, **({"lost": lost} if lost else {})}


def node_paths(nodes):
    """Each node's name path below the root ("" for the root, "magmaClutter_cleave/TrailEmitter" ...)."""
    out = []
    for n in nodes:
        out.append("" if n["parent"] < 0 else (out[n["parent"]] + "/" if out[n["parent"]] else "") + n["name"])
    return out


def bb_material(game, cls, name, want, mats, texs):
    """BB's material `want` from any renderer under the BB effect `name` whose m_Materials lists it, a Unity 3.5
    ParticleSystemRenderer too (effect() skips that component; 2026-11-13, the Cat's supportFire_hit, whose only renderer
    is its Shuriken's, material Bomb2), through material() into mats / texs; nothing when no renderer has it."""
    key = ALIASES.get(cls, {}).get(name, f"gameassets/characters/heroes/{cls}/effects/{name.lower()}")
    todo = [game.obj(game.container[key], game.files["mainData"])]
    while todo:
        go_obj = todo.pop()
        for comp in go_obj.read_typetree()["m_Component"]:
            c = game.obj(comp[1] if isinstance(comp, (list, tuple)) else comp.get("second", comp.get("component")), go_obj.assets_file)
            if c is None:
                continue
            if c.type.name == "Transform":
                for ch in c.read_typetree()["m_Children"]:
                    tro = game.obj(ch, go_obj.assets_file)
                    if tro is not None:
                        todo.append(game.obj(tro.read_typetree()["m_GameObject"], tro.assets_file))
            elif c.type.name.endswith("Renderer"):
                for m in c.read_typetree().get("m_Materials", []):
                    o = game.obj(m, c.assets_file)
                    if o is not None and o.read_typetree()["m_Name"] == want:
                        material(game, m, c.assets_file, mats, texs)
                        return


def graft_shuriken(game, cls, effects, mats, texs):
    """SHURIKEN_FROM_TTO (decisions.md 40): for each listed effect built here, TTO's copy read through
    pipeline/wardrobe_fx_tto.py (Tto / Build / effect, as wardrobe_weapon_fx.tto_weapons does), and under every BB node
    whose name path matches a TTO node carrying a ParticleSystem, a new child node at local identity (pos 0, rot identity,
    scale 1) holding that node's ParticleSystem and ParticleSystemRenderer dicts, its mats (and the renderer's
    m_Materials) = SHURIKEN_MAT's BB material, added to mats. Only where TTO's bundles are (home): elsewhere a warning, and
    BB's effect stays as it is (no puffs). A class with no SHURIKEN_MAT entry (the Chameleon, 2026-11-13): graft_by_material."""
    names = [n for n in SHURIKEN_FROM_TTO.get(cls, []) if n in effects]
    if not names:
        return
    import importlib.util
    import sys
    try:
        spec = importlib.util.spec_from_file_location("wardrobe_fx_tto", os.path.join(HERE, "wardrobe_fx_tto.py"))
        T = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(T)
        if not os.path.exists(os.path.join(T.ASSETS, "catalog.bin")) or not os.path.exists(T.AA_CATALOG):
            raise FileNotFoundError(f"TTO's bundles ({T.ASSETS}) or the catalog reader ({T.AA_CATALOG})")
        tto = T.Tto(cls, names)
        b = T.Build(tto)
        got = {n: T.effect(tto, b, n) for n in names}
    except (Exception, SystemExit) as ex:             # noqa: BLE001 (the office without TTO's bundles: BB's version stays)
        print(f"warning: {cls}: no Shuriken graft for {names} ({type(ex).__name__}: {ex}); BB's version kept", file=sys.stderr)
        return
    if cls not in SHURIKEN_MAT:                       # the Chameleon's: by (name, material), BB's own materials kept
        graft_by_material(cls, names, effects, got)
        return
    mat, src = SHURIKEN_MAT[cls]
    if mat not in mats:                               # BB's material of the same shader, read from a BB effect that has it
        tmp_m, tmp_t = {}, {}
        effect(game, cls, src, tmp_m, tmp_t, set())
        if mat not in tmp_m:                          # only on its Unity 3.5 Shuriken renderer (the Cat's supportFire_hit)
            bb_material(game, cls, src, mat, tmp_m, tmp_t)
        mats[mat] = tmp_m[mat]
        if tmp_m[mat].get("tex") in tmp_t:
            texs.setdefault(tmp_m[mat]["tex"], tmp_t[tmp_m[mat]["tex"]])
    for n in names:
        bb_nodes, tto_nodes = effects[n]["nodes"], got[n]["nodes"]
        tto_at = dict(zip(node_paths(tto_nodes), tto_nodes))
        for i, (path, node) in enumerate(list(zip(node_paths(bb_nodes), bb_nodes))):
            t = tto_at.get(path)
            comps = [c for c in (t or {}).get("comps", []) if c["type"] in ("ParticleSystem", "ParticleSystemRenderer")]
            if not any(c["type"] == "ParticleSystem" for c in comps):
                continue
            comps = json.loads(json.dumps(comps))
            for c in comps:
                if c["type"] == "ParticleSystemRenderer":
                    c["m_Materials"] = [mat]
            bb_nodes.append({"name": node["name"] + "_shuriken", "parent": i, "pos": [0, 0, 0], "rot": [0, 0, 0, 1],
                             "scale": [1, 1, 1], "comps": comps, "mats": [mat]})
            print(f"{cls}: {n}/{path}: TTO's ParticleSystem grafted (node {len(bb_nodes) - 1}, material {mat})", file=sys.stderr)


def graft_by_material(cls, names, effects, got):
    """graft_shuriken for a class with no SHURIKEN_MAT entry (2026-11-13, the Chameleon: SHURIKEN_FROM_TTO's comment,
    plans/fx_chameleon/parts.md part 7, Verification 4): each BB node effect() marked "ps" (a Unity 3.5
    ParticleSystemRenderer, its materials in node["mats"]) takes the TTO node of the same name carrying a ParticleSystem
    whose renderer's first material is "tto_" + mats[0], the next unused one in TTO's order on a tie; that node's
    ParticleSystem and ParticleSystemRenderer dicts go on the BB node itself, the renderer's m_Materials = BB's mats. A BB
    node with no such TTO node: a warning, nothing grafted."""
    import sys

    def first_mat(t):
        r = next((c for c in t["comps"] if c["type"] == "ParticleSystemRenderer"), None)
        m = (r or {}).get("m_Materials") or t.get("mats") or []
        return m[0] if m and isinstance(m[0], str) else None

    for n in names:
        bb_nodes, tto_nodes, used = effects[n]["nodes"], got[n]["nodes"], set()
        for i, node in enumerate(bb_nodes):
            if not node.get("ps") or not node.get("mats"):
                continue
            want = "tto_" + node["mats"][0]
            j = next((k for k, t in enumerate(tto_nodes) if k not in used and t["name"] == node["name"]
                      and any(c["type"] == "ParticleSystem" for c in t["comps"]) and first_mat(t) == want), None)
            if j is None:
                print(f"warning: {cls}: {n}/{node['name']} (node {i}): no TTO node {node['name']!r} with material {want}; "
                      "no Shuriken grafted", file=sys.stderr)
                continue
            used.add(j)
            comps = json.loads(json.dumps([c for c in tto_nodes[j]["comps"]
                                           if c["type"] in ("ParticleSystem", "ParticleSystemRenderer")]))
            for c in comps:
                if c["type"] == "ParticleSystemRenderer":
                    c["m_Materials"] = list(node["mats"])
            node["comps"].extend(comps)
            print(f"{cls}: {n}/{node['name']} (node {i}): TTO's ParticleSystem grafted from TTO node {j} "
                  f"(material {node['mats'][0]})", file=sys.stderr)


def rip_wav(cls, name, folder=None):
    """The rip's WAV: from the class's voices/ or sounds/ when the cue says which (they share names: crusader1, nAttack1
    ... are different recordings in each, 2026-11-09), else sounds/ then voices/ then anywhere (an effect's own sound).
    A name in SOUND_ALIASES[cls] is that file, whatever the folder."""
    alias = SOUND_ALIASES.get(cls, {}).get(name)
    if alias:
        p = os.path.join(RIP, *alias.split("/")) + ".wav"
        return p if os.path.exists(p) else None
    if folder:
        p = os.path.join(RIP, "characters", "heroes", cls, folder, name + ".wav")
        return p if os.path.exists(p) else None
    for sub in (f"characters/heroes/{cls}/sounds", f"characters/heroes/{cls}/voices"):
        p = os.path.join(RIP, *sub.split("/"), name + ".wav")
        if os.path.exists(p):
            return p
    # an effect's sound kept elsewhere: anywhere under gameassets, then anywhere under Resources (Blade Fang's ring plays
    # Resources/sound/fx/aura1.wav, 2026-11-09), a .wav first, then an .ogg; then the rip's Assets/AudioClip (the clips no
    # Resources path names: 2026-11-13, plans/fx_mole/decisions.md 48, megaDrill_ring's gallonDrill.ogg, kaiser_box.wav)
    for top in (RIP, os.path.dirname(RIP)):
        for ext in (".wav", ".ogg"):
            for root, _, fs in os.walk(top):
                if name + ext in fs:
                    return os.path.join(root, name + ext)
    return audioclip_file(name)


def audioclip_file(name):
    """The rip's Assets/AudioClip/<name>.wav or .ogg (AssetRipper's folder for the clips outside Resources; a name it saw
    twice has _0, _1 ... copies beside it, never taken here), else None."""
    for ext in (".wav", ".ogg"):
        p = os.path.join(os.path.dirname(os.path.dirname(RIP)), "AudioClip", name + ext)
        if os.path.exists(p):
            return p
    return None


def hero_sound_wav(cls, name):
    """A "sound" cue's WAV (the hero's code plays it): the class's sounds/ (never its voices/, which share names), else
    anywhere in the rip's Resources outside the characters' folders (2026-11-13, plans/fx_bat/attacks_emotes.md "Parts
    needed" 5a: the Bat's wing flap, Bat.cs's field wingFlap = Resources/sound/fx/step_fly1.wav; the other characters'
    clips are their own recordings under the same names, nAttack1 ..., so one of theirs takes a SOUND_ALIASES line)."""
    p = rip_wav(cls, name, "sounds")
    if p or SOUND_ALIASES.get(cls, {}).get(name):
        return p
    chars = os.path.normcase(os.path.join(RIP, "characters"))
    # a .wav, then an .ogg (2026-11-13, plans/fx_mole/decisions.md 48, tto.md P15: the Missile lock's Resources/sound/gui/
    # beep.ogg), then the rip's Assets/AudioClip (kaiser_open.wav: KingKaiser's kaiser_openFx, no Resources path)
    for ext in (".wav", ".ogg"):
        for root, dirs, fs in os.walk(os.path.dirname(RIP)):
            if os.path.normcase(root) == chars:
                dirs[:] = []
            elif name + ext in fs:
                return os.path.join(root, name + ext)
    return audioclip_file(name)


def builds(entry):
    """An entry's "builds" (2026-11-13, plans/fx_bat/parts.md Interfaces 6: what a page part spawns or plays that no cue
    names, api.spawn / Sound.play; the guardian's blade, hits and swing) as (kind, name): "sound:<name>" / "voice:<name>"
    or ["sound", name], else an effect; a pool's skills may carry their own."""
    out = []
    for e in [entry] + list(entry.get("skills", {}).values()):
        for b in e.get("builds", []):
            if isinstance(b, (list, tuple)):
                out.append((b[0], b[1]))
            elif str(b).split(":", 1)[0] in ("sound", "voice", "fx") and ":" in str(b):
                out.append(tuple(str(b).split(":", 1)))
            else:
                out.append(("fx", str(b)))
    return out


def cue_lists(entry):
    """An entry's cue lists: its cues, or every skill's of a shared clip ({skills: {name: {cues}}})."""
    return [entry.get("cues", [])] + [s.get("cues", []) for s in entry.get("skills", {}).values()]


def cue_names(cls):
    """The effects, voices and sounds the class's cue file names, as --fx / --voices / --sounds strings (in cue order, no
    repeats; "a|b" = both)."""
    path = os.path.join(os.path.dirname(DATA), "fx_cues", cls + ".json")
    names = {"fx": [], "voice": [], "sound": []}
    for entry in json.load(open(path, encoding="utf-8")).values():
        for cues in cue_lists(entry) + [[[0, k, n] for k, n in builds(entry)]]:
            for cue in cues:
                if cue[1] not in names:      # a "skin" / "clone" cue (the hero's own look, a copy of her): nothing to build
                    continue
                for n in str(cue[2]).split("|"):
                    if cue[1] == "fx" and n.startswith("tto/"):     # TTO's effects: pipeline/wardrobe_fx_tto.py builds them
                        continue
                    if n not in names[cue[1]]:
                        names[cue[1]].append(n)
    return ",".join(names["fx"]), ",".join(names["voice"]), ",".join(names["sound"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cls")
    ap.add_argument("--fx", default="", help="effects to build instead of the cue file's")
    ap.add_argument("--voices", default="", help="Voices/ clips -> sfx/v_<name>.mp3")
    ap.add_argument("--sounds", default="", help="Sounds/ clips the hero's code plays -> sfx/<name>.mp3")
    ap.add_argument("--probe", default="", help="print these effects' nodes and components as JSON; writes nothing")
    a = ap.parse_args()
    if a.probe:                          # read only (the research agents' ask: --fx writes the shared data)
        game = Game()
        for n in a.probe.split(","):
            try:
                pm = {}
                one = {n: effect(game, a.cls, n, pm, {}, set())}
                graft_shuriken(game, a.cls, one, pm, {})      # (SHURIKEN_FROM_TTO: TTO's Shuriken read too, in memory)
                print(json.dumps(one, indent=1))
            except Exception as e:      # noqa: BLE001 (a script with no layout yet: say so, go on)
                print(json.dumps({n: f"{type(e).__name__}: {e}"}))
        for fname, fpath in sorted(FONTS_USED):      # (FONTS: what fx.json's "fonts" would get; no texture written)
            print(json.dumps({"fonts": {fname: font(game, fname, fpath)[0]}}))
        return
    if not a.fx:
        a.fx, a.voices, a.sounds = cue_names(a.cls)
        if not a.fx and not a.voices and not a.sounds:
            ap.error(f"wardrobe/fx_cues/{a.cls}.json has no cues; write them first, or pass --fx")
    game = Game()
    mats, texs, sounds, effects = {}, {}, set(), {}
    # the page looks an effect up by the cue's name: a --fx name in another case (the inventory's lower-case returncast,
    # plans/fx_sheep/tto.md) is stored under the cue's spelling (the prefab itself is found in any case, effect())
    spell = {n.lower(): n for n in cue_names(a.cls)[0].split(",") if n} if os.path.exists(os.path.join(os.path.dirname(DATA), "fx_cues", a.cls + ".json")) else {}
    for n in [n for n in a.fx.split(",") if n]:
        effects[spell.get(n.lower(), n)] = effect(game, a.cls, n, mats, texs, sounds)
    graft_shuriken(game, a.cls, effects, mats, texs)   # TTO's decoded Shuriken onto BB's effect (decisions.md 40)
    voices =[v for v in a.voices.split(",") if v]
    hero_sounds = [v for v in a.sounds.split(",") if v]
    # textures -> data/fx/tex (shared by every class), sounds -> data/<cls>/sfx
    tdir = os.path.join(DATA, "fx", "tex"); os.makedirs(tdir, exist_ok=True)
    for n, o in texs.items():
        o.read().image.save(os.path.join(tdir, n + ".webp"), "WEBP", quality=90, method=6)
    fonts = {}
    for fname, fpath in sorted(FONTS_USED):          # FONTS: the bitmap fonts the effects' scripts draw with
        fonts[fname], img = font(game, fname, fpath)
        img.save(os.path.join(tdir, fname + ".webp"), "WEBP", lossless=True)
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    sdir = os.path.join(DATA, a.cls, "sfx"); os.makedirs(sdir, exist_ok=True)
    missing, jobs, own = [], [], []
    # a summon's own clip (SOUND_REFS): the game's bytes, written beside the output and removed after the conversion
    for n in sorted(set(sounds) & set(FIELD_SOUNDS)):
        k, v = next(iter(FIELD_SOUNDS[n].read().samples.items()))
        own.append(os.path.join(sdir, "_" + n + os.path.splitext(k)[1]))
        open(own[-1], "wb").write(v)
        jobs.append((n, own[-1], n))
    # an effect's own sound and a Sounds/ cue: <name>.mp3 (from sounds/ first); a voice: v_<name>.mp3 from voices/ only
    jobs += [(n, rip_wav(a.cls, n), n) for n in sorted(set(sounds) - set(FIELD_SOUNDS))]
    jobs += [(n, hero_sound_wav(a.cls, n), n) for n in sorted(set(hero_sounds) - sounds)]
    jobs += [(n, rip_wav(a.cls, n, "voices"), "v_" + n) for n in sorted(set(voices))]
    for n, src, out_name in jobs:
        if not src:
            missing.append(out_name); continue
        subprocess.run([ff, "-y", "-loglevel", "error", "-i", src, "-ac", "1", "-b:a", "64k", os.path.join(sdir, out_name + ".mp3")], check=True)
    for p in own:
        os.remove(p)
    out = os.path.join(DATA, a.cls, "fx.json")
    old = json.load(open(out, encoding="utf-8")) if os.path.exists(out) else {}
    merged = {"effects": {**old.get("effects", {}), **effects}, "materials": {**old.get("materials", {}), **mats}}
    if fonts or old.get("fonts"):
        merged["fonts"] = {**old.get("fonts", {}), **fonts}
    # (allow_nan=False: a NaN would make the page refuse the whole file, 2026-11-13; wardrobe_fx_mesh.r5 writes 0 for one)
    json.dump(merged, open(out, "w", encoding="utf-8"), separators=(",", ":"), allow_nan=False)   # compact: meshes and clips (2026-11-09) doubled it indented
    print(f"{a.cls}: {len(effects)} effects, {len(mats)} materials, {len(texs)} textures, {len(jobs) - len(missing)} sounds"
          + (f", missing sounds: {missing}" if missing else ""))


if __name__ == "__main__":
    main()
