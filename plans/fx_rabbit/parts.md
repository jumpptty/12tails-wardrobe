# Rabbit effects: the parts the page cannot draw yet (or draws wrongly)

Research 13/11/2026, office PC (one of the Rabbit fx researchers; scope: every part the Rabbit's effects need: the
inventory's 84, the 12 Rabbit prefabs it does not list, the components `wardrobe_fx.effect()` drops, the shaders, the hero
code acting on its effects, the summons the Rabbit's skills make, and the released TTO skills' prefabs). Models:
`plans/fx_mole/parts.md`, `plans/fx_chameleon/parts.md`. Read only: nothing in `wardrobe/data` was written;
`wardrobe_fx.py` / `wardrobe_fx_tto.py` ran with `--probe` only (or were imported read only, every table change made in
memory); no browser. `Rabbit.cs`, `Rabbit_<x>.cs`, `CharacterControl.cs`, `EffectControl.cs`, `LightGolem.cs`, `Math.cs`,
`Damage.cs` lines are `C:\Users\Jump\Desktop\12tails\DecompiledSource\<file>` (= the home PC's `D:\12tails\...`; opaque
predicates worked by `annotate.py`, every one evaluated, then read by hand); TTO is `TTO1102:` =
`DecompiledSource_TTO_2026-11-02` (`dump.cs`, `methods.tsv`, `pseudo/Rabbit.c`, `pseudo_c6_extra/rabbit/RabbitMedicTurret.c`,
the client's `GameAssembly.dll` disassembled at the RVAs `dump.cs` gives).

Probes (read only, outputs beside them) in `checks/fx_rabbit_research/parts/` (git-ignored, office PC):
- `probe.py` -> `probe.txt`: all 96 prefabs in `heroes/rabbit/effects` walked node by node (transforms, every component,
  an unknown script's field bytes as ints and floats, every material's blend through `wardrobe_fx.material`, colliders and
  Rigidbodies, Animation clips) and then `wardrobe_fx.effect()` on each. Last lines: `UNKNOWN scripts: Rabbit_acidicField
  [0], Rabbit_healingField [0], Rabbit_potion [4 x13], Rabbit_mall [0 x5], Rabbit_sniperCamera [24], Rabbit_stickyGum [0]`;
  `DROPPED comps: ParticleSystem / ParticleSystemRenderer (extravagance_ring), BoxCollider (the 13 potions),
  SphereCollider (stickyGum)`. **14 effects raise today**: hpPot1-4, spPot1-3, randomPot1-6, sniperCamera.
- `layouts_try.py` -> `layouts_try.txt`: the LAYOUTS block below + `EXTRA_FOLDERS["rabbit"]` set in memory, `effect()` on
  all 96 prefabs and the Light Golem: **97 built, 0 raise** (every decode uses up exactly its bytes).
- `graft_try.py` -> console; `ps_cmp.py` / `ps_cmp2.py` -> `ps_cmp.txt` / `ps_cmp2.txt`: extravagance_ring's two Unity 3.5
  ParticleSystems grafted from TTO's copy in memory (`SHURIKEN_FROM_TTO["rabbit"]`), BB's full type trees beside TTO's.
- `hero_fields.py` -> `hero_fields.txt`: the Rabbit hero prefab's own script (`castStar1`, `castLight`, `deadEffect`);
  `cc_probe.py` -> `cc_probe.txt`: her CharacterController (centre 0.7 m up, height 1.2, radius 0.3).
- `summons.py` -> `summons.txt`: Contract's mercenaries LightPanther / LightLeopard / LightGolem (scripts, bytes, clips).
- `uses.py` -> `uses.txt`: every `Instantiate` in `Rabbit.cs` and each later use of the object in its coroutine.
- `catalog_keys.py` -> `catalog_keys.txt`; `tto_released.json` (+ `tto_released.err`) and `tto_sum.py` -> `tto_sum.txt`:
  `wardrobe_fx_tto.py rabbit --probe` of the 23 prefabs the released TTO skills spawn and the two status looks.
- `disasm.py` -> `disasm_spin.txt`: TTO's `PowerUpRotation.Update` @0x33ad20 and `RabbitSpin.Update` @0x1e6ee30.
- `src/*.txt`: `annotate.py` (each `if (a - b ==/!= c)` replaced by TRUE / FALSE, line numbers kept) of `Rabbit.cs`, the six
  `Rabbit_<x>.cs`, `CharacterControl.cs`, `EffectControl.cs`.

## Read this first

1. **Six Rabbit scripts; two need a layout, four keep every field private and draw nothing of their own.** No Rabbit
   script moves, fades or spawns anything on the page: they are damage / heal / status ticks, a pickup trigger, a shop
   button and the scope's GUI. So the BB side needs LAYOUTS lines and no Rabbit script part.

   | effect(s) | script (field bytes) | what it does in BB | today | the page |
   |---|---|---|---|---|
   | `hpPot1-4`, `spPot1-3`, `randomPot1-6` (Mix / Shake / Miracle Blend potions) | `Rabbit_potion` (4: `potionType`) | a pickup: an ally on the owner's layer walks into its trigger box -> heal / status, `RPC_potion_hit` (`Rabbit_potion.cs:141-486`) | **not buildable** | data only (part 1) |
   | `sniperCamera` (Charge Attack) | `Rabbit_sniperCamera` (24: two Textures, a bool, a float) | the owner's first-person scope: camera, scope picture, range readout, Dead Shot bar and sound (`Rabbit_sniperCamera.cs:41-526`) | **not buildable** | layout; the sound by `playAudio`; the camera and GUI left out (part 2) |
   | `acidicField`, `healingField` | `Rabbit_acidicField` / `Rabbit_healingField` (0) | a 12 m tick every 2 s for `nLife` s (`Rabbit_acidicField.cs:83-221`) | builds (particles, looping sound) | data only; the cue's `kill` (part 3) |
   | `stickyGum` | `Rabbit_stickyGum` (0) | the sticky status every 0.5 s in `sLv + 0.5` m and on trigger (`Rabbit_stickyGum.cs:83-310`) | builds | data only; the hero's code scales it (part 3) |
   | `mall1-5` | `Rabbit_mall` (0) | the buyers' shop button (OnGUI, `Rabbit_mall.cs:74-345`); destroyed when the owner leaves mallSetup / mallOpen | builds (the carpet) | data only; the button left out (part 3) |
2. **One Unity 3.5 ParticleSystem: `extravagance_ring` (2 systems), and TTO's copy matches it field for field.**
   `SHURIKEN_FROM_TTO["rabbit"] = ["extravagance_ring"]` with **no** `SHURIKEN_MAT` entry (the Chameleon's
   graft_by_material route) grafts both onto BB's own nodes with BB's materials (`Gil` alpha, `star5` addsoft), run in
   memory: "TTO node 1 (material Gil)", "TTO node 4 (material star5)" (part 4).
3. **Shaders: nothing to build.** The Rabbit's materials (`probe.txt`): addsoft 35, `Particles/AdditiveOffset` 9
   (particles.js), `Transparent/Opaque2` 8 (the potions' bottles: mesh.js, the Penguin's), add 7, opaque 5, alpha 3,
   `Particles/AlphaOffset` 2 (truceTrading success / failed: particles.js), `Self-Illumin/DoubleTexture` 1
   (`rabbit_stickygum`: doubletexture.js, whose header already names it), premul 1 (`rabbit_dead`).
4. **Two page parts are missing for every class, found here.**
   - **The root EffectControl's rotation modes.** `statScan` (faceCamera, 2), `bounce1` / `bounce2` (faceUp, 3) carry
     them on their **root**; the page applies `effectRotationMode` only to a child EffectControl (`fxparts/control.js:78-95`):
     class Fx keeps the root's (`index.html:4258`) and never reads the mode. In BB the root turns every frame of its live
     phase (`EffectControl.cs:368-407`: `LookAt(Camera.main)` / `FromToRotation(forward, vFlat(camera forward))`), with or
     without an owner. Part 5.
   - **Sheep's `fx:cAttack_charge` hook runs on the Rabbit's `cAttack_charge`** (`FXPARTS["fx:" + name]` is keyed by
     the effect's name only, `index.html:4251`): it finds no legacy emitter on the Rabbit's root and logs
     "effect part fx:cAttack_charge: the ball's particle emitter has no setSize" on every Charge Attack
     (`fxparts/sheep.js:107-110`). Harmless to the look; a one-line class guard (part 8).
5. **The hero's code acts on six effects; four are built, two are new.**
   - built: Sticky Gum's `localScale = (sLv + 0.5, 1, sLv + 0.5)` (`Rabbit.cs:10072`; the cue's per-axis `scale`
     [2.5, 1, 2.5]); Truce Trading's and Contract's flags and Rapid Trance's potion on `mountHand_L` (`:34307-34322`,
     `:40708-40723`, `:28999-29019`; the cue's `bone`); Backpack switches the weapon's MeshRenderers off and on
     (`:31009`, `:31227`, `:31293`, `:31389`; the `hideProp` kind); Mall's prefab by the outfit colour (`"mall" +
     Math.div(Skin, 100)`, `:33507`; the cue's `pick: "color"`); the scope's sound (`audio.Play()` in its own OnGUI; the
     cue's `playAudio`).
   - **new: Ten Shot's second gun**: `Instantiate(mChar.mWep1)` parented to `mountHand_L`, local zero / identity, from
     clip 0.2 s to the standby at 2.8 s (`Rabbit.cs:38896-38922`, `:38960-38981`). No effect prefab holds it: a new cue
     kind `propCopy` (part 6).
   - **new: Contract's mercenary**, a whole character from `Resources/GameAssets/Characters/Elementals/` (part 7).
6. **One summon: Contract** (`RPC_contract_create`, `Rabbit.cs:11542-11760`): sLv 1 two LightPanther, 2 two LightLeopard,
   3 one **LightGolem** (`:11566-11611`), the rank by the SP left after the cost (`:7607` `sp >= 35`, `:7619` `sp >= 65`).
   Its scripts: `LightGolem` (40 bytes), `LightGolemAI` (8: the string "none"), CharacterControl (684, NOT_DRAWN). Its
   clips are plain (no compression, no float curves, `summons.txt`). Part 7.
7. **The inventory misses 12 Rabbit prefabs**: `castStar`, `castLight`, `deadEffect` (the hero prefab's fields
   `castStar1`, `castLight`, `deadEffect`, `Rabbit.cs:16711-17245`, which are the Resources prefabs of those names:
   sharedassets7 path ids 279 / 278 / 277, `hero_fields.txt`, so they build by name), `mall1-5` (the concatenated
   `"mall" + n`, `:33507`), `autoLife` (Life Shot's status look, `CharacterControl.cs:44166`), `enlarge`, `reduce`,
   `miracleDrop` (the random potions' status looks on the drinker, `CharacterControl.cs:37222`, `:37302`, `:37683`). All
   use built parts.
8. **Seven loads name prefabs BB does not hold** ("Cannot find ... Effect" in the game; TTO's catalog lacks them too,
   `catalog_keys.txt`): `snipeShot_hit` (`Rabbit.cs:11448`: **every rifle Combo hit with Snipe Mastery #431**,
   `:17594-17611`, `:18271`), `kneeShot_hit` (`:9682`: Maim Shot's Knee Shot proc, `:23288-23305`), `fourShot_hit`
   (`:10757`), `circleShot_hit` (`:10807`), `tenShot_hit` (`:11498`, `RPC_tenShot_hit`; Ten Shot itself hits with
   `RPC_nAttack_hit`), `herbFinder` (`:10545`), `contract_ring` (`:40661`). Nothing to build; the cues show nothing there
   (Mole's `warCapital_dead`). Offered to the Bible.
9. **TTO (Bounty Hunt, Coin Ricochet, Medic Turret; clap / wai have no effects): 23 prefabs + 2 status looks.** New:
   `RabbitMedicTurret` (the turret's script, with the hero's `MedicTurretPulse` / `ShotFx` / `TurretCapsule`), three code
   movers (`Rabbit.TurretCapsule`, `Rabbit.PosterFly`, `Rabbit.CoinRise`), `RabbitSpin`. Shared with the Monkey's
   research (built by whichever class builds first): `Eric/URP Particles/Additive` (19 materials) and `Alpha Blended` (1),
   Shuriken `NoiseModule` (1 system). Built already: RabbitTracer (5 prefabs), GroundHugEmitter (9), LineRenderer,
   TrailRendererModern, Shuriken Trail / Collision, `Particles/Standard Unlit`, `FlexibleCelShader/Cel No Outline`.
   Section "TTO".
10. **Game quirks (offer to the user for the Bible; none needs a part).**
    - With Snipe Mastery (#431, a passive: on here) the rifle Combo's hit effect is `snipeShot_hit`, which BB lacks: **no
      hit is drawn on any Combo shot** (item 8). The Knee Shot proc (#402) likewise draws no hit.
    - Acidic Field and Healing Field pulse **7 times**, not 6, at base CHA: the life end is noticed only on a tick frame,
      and that branch Destroys the field and then jumps back into the tick (`Rabbit_acidicField.cs:212-216` `goto IL_15E`;
      `Rabbit_healingField.cs:203-207` `goto IL_EE`): ticks at 0, 2, ... 10 and one more at about 12 s.
    - `Rabbit_potion`'s "taken" flag (`fRiN0Squkp`, `Rabbit_potion.cs:525`) is never set anywhere: its Update and
      OnTriggerEnter guards on it (`:121`, `:150`) never fire; the potion goes only by `RPC_potion_hit`'s Destroy
      (`Rabbit.cs:9946`) or its life.
    - The scope is made only on the owner's screen (`gameObject == Game.mPlayer`, `Rabbit.cs:18646`) and its script runs
      only in `mGameType >= 3` (`Rabbit_sniperCamera.cs:57`, else `enabled = false` `:185`); its range readout ends in
      " tm" (`:330`).
    - Contract's Light Golem swaps to its second material only on layer 9 (`LightGolem.cs:83-109`); a player's golem keeps
      its own.

## The Rabbit's blocked set

"Where" is where BB spawns it. The clip times and which tile plays them are the skills researchers'
(`skills_a.md`, `skills_b.md`, `attacks_emotes.md`, `effect_only.md`, `tto.md`), so treat the cue shapes here as the parts'
contract.

| effect | skill (spawn) | missing part(s) | where |
|---|---|---|---|
| `hpPot1-4` | Mix (`RPC_mix_create`, `Rabbit.cs:24354-24535`) | Rabbit_potion layout (data) | hero + rotateH(1.5 tDir, i x 120) (`:23925`; 72 deg with Med Research #412, `:23891-23902`), identity, Init life chaAdjust(60) (`:24535`) |
| `spPot1-3`, `randomPot1-6` | Shake (`:25225-25362`), Miracle Blend (`:26152-26350`) | the same | the same pattern |
| `sniperCamera` | Charge Attack (`RPC_cAttack1` case 2, `:18646-18725`) | Rabbit_sniperCamera layout; the sound (`playAudio`) | hero + TransformDirection(0, 1.05, 0.15), the owner's screen only |
| `extravagance_ring` | Extravagance (`RPC_extravagance`, `:40021-40033`) | Shuriken graft (2 systems) | hero, hero rotation (createEffect) |
| `statScan` | Stat Scan (`:22512-22524`) | root faceCamera (part 5) | the target's ClosestPointOnBounds(hero + 1.5 up), identity, owner = the target |
| `bounce1`, `bounce2` | Bounce (`:21019-21031`), its landing (`:21840-21875`) | root faceUp (part 5) | hero, hero rotation (Instantiate: no owner) |
| (the second gun) | Ten Shot (`RPC_tenShot`, `:38896-38981`) | the `propCopy` cue kind (part 6) | `mountHand_L`, local zero / identity |
| `LightGolem` | Contract (`RPC_contract_create`, `:11611`; spot `:40464`) | EXTRA_FOLDERS, layouts, the loop part (part 7) | getSpawnVector(hero + up, TransformDirection(0, -1, 3)), LookRotation(hero forward) |
| `cAttack_charge` | Charge Attack (`:18988-18998`) | the Sheep hook's class guard (part 8) | hero, hero rotation |

## LAYOUTS (paste into `pipeline/wardrobe_fx.py`, after the Mole's summons block, the one ending with the "Mole" entry)

```python
# the Rabbit's parts (plans/fx_rabbit/parts.md, 2026-11-13; checks/fx_rabbit_research/parts/probe.txt, layouts_try.txt: each
# instance's bytes are the listed fields exactly, all 96 Rabbit prefabs and the Light Golem build); the other Rabbit scripts
# keep every field private (0 field bytes); every Rabbit script is data only on the page (nothing to draw of its own)
LAYOUTS.update({
    # Rabbit_potion.cs:528 (4 bytes: eRabbitPotionType, hpPot1-4 = 0-3, spPot1-3 = 4-6, randomPot1-6 = rdPot1-6 = 7-12)
    "Rabbit_potion": [("potionType", "i")],
    # Rabbit_sniperCamera.cs:553, :556, :589, :592 (24 bytes: the scope and Dead Shot pictures [9, 67] / [9, 54], false, 0)
    "Rabbit_sniperCamera": [("mSniperCamera", "r"), ("mDeadShotCamera", "r"), ("hasDeadShot", "b"), ("mDeadShotTimer", "f")],
    "Rabbit_acidicField": [], "Rabbit_healingField": [], "Rabbit_mall": [], "Rabbit_stickyGum": [],
})
# Contract's mercenary (Resources characters/elementals/lightgolem/LightGolem, Rabbit.cs:11596-11611; parts.md part 7): data
# only (fxparts/rabbit.js loops its root clip); its CharacterControl stays NOT_DRAWN
LAYOUTS.update({
    # LightGolem.cs:1144-1159 (40 bytes; the private float at :1147 is not serialized)
    "LightGolem": [(n, "r") for n in ("mChar", "LightGolem2", "LightGolemIcon2", "nAttack_hit", "nAttack_hitFx")],
    "LightGolemAI": [("AI_state", "s")],             # LightGolemAI.cs:1462 (8 bytes: "none")
})
```

Two more extractor lines (page_pipeline, `wardrobe_fx.py`):
- `SHURIKEN_FROM_TTO["rabbit"] = ["extravagance_ring"]` (beside the Mole's line) and **no** `SHURIKEN_MAT` entry (part 4).
- `EXTRA_FOLDERS["rabbit"] = ["gameassets/characters/elementals/lightgolem"]` (the effect name `LightGolem`, part 7).

`pipeline/wardrobe_fx_tto.py` (page_pipeline):
- `SKILL_FX["rabbit"] = ["bountyHunt_poster", "bountyHunt_pin", "bountyHunt_flare", "bountyHunt_muzzle",
  "bountyHunt_tracer", "bountyHunt_hit", "bountyHunt_claim", "bounty", "coinRicochet_flick", "coinRicochet_coin",
  "coinRicochet_shot", "coinRicochet_ping", "coinRicochet_ricochet", "coinRicochet_hit", "coinRicochet_cashTracer",
  "coinRicochet_cashout", "gilded", "medicTurret_cast", "medicTurret_deploy", "medicTurret", "medicTurret_beat",
  "medicTurret_shot", "medicTurret_capsule", "medicTurret_hit", "medicTurret_break"]` (every prefab the three
  coroutines name, `pseudo/Rabbit.c` strings; `bounty` / `gilded` / `bountyHunt_claim` built but not cued, as the
  Chameleon's kill reward).
- `CODE_MOVERS` += `"medicTurret_capsule": "Rabbit.TurretCapsule"`, `"bountyHunt_poster": "Rabbit.PosterFly"`,
  `"coinRicochet_coin": "Rabbit.CoinRise"`, each with its comment (TTO section T2-T4).

## Each part

Page parts plug in as the comment above `FX_PART_FILES` says (`wardrobe/index.html:3947-4028`): `wardrobe/fxparts/<file>.js`
default-exports `register(api)` and calls `api.part(type, build)`; `build(fx, node, comp, mat, nodeDef, data)` returns
`{ node, update(dt, cam) ("destroy" removes the node), stop?(), dispose?() }` or null; `api.spawn(name, at, opts)` makes an
effect a script instantiates (the entry's `"builds"` puts it in `fx.json`). Space: every root hangs in the effect's mirror
group (Unity's world, the hero's feet at the origin, +z her facing, y 0 the floor). The target body (Bat decision 4, every
class): a cylinder at (0, 0.6, 10), height 1, radius 0.3. The Rabbit's own body: her CharacterController, centre (0, 0.7, 0),
height 1.2, radius 0.3 (`cc_probe.txt`; TTO's `Row6Chest` = a collider's bounds centre, `pseudo/Rabbit.c:39226-39305`).

### 1. Rabbit_potion: the 13 potions (layout only, no page code)

**What it does.** Field `potionType` (`Rabbit_potion.cs:528`); the prefab's 4 bytes are 0-12 in the order hpPot1-4,
spPot1-3, randomPot1-6 (`layouts_try.txt`). `Init(nLife, nID, owner)` (`:45-84`): the life (`chaAdjust(60)` from the hero,
`Rabbit.cs:24535`), the owner and its layer. Update (`:88-137`): Destroy when the owner is gone or the life ends.
OnTriggerEnter (`:141-486`; trigger box 0.6 x 1 x 0.6 at y 0.5, 0.5 x 1 x 0.5 for the random potions, `probe.txt`): on the
owner's client, an ally on the owner's layer heals / gets the status by `potionType` (`:288-443`), then
`rabbit.RPC_potion_hit` (`:455`), which spawns `hpPot_hit` / `spPot_hit` / `mpPot_hit` at the potion and Destroys it
(`Rabbit.cs:9754-9990`; no `destroy` clip is played, though hpPot / spPot carry one).

**The page.** The potions lie 1.5 m from the hero (`Rabbit.cs:23925`), out of her 0.3 m body: nothing walks into them, so
they stand with their `root` drop clip until the cue's `kill` (the 10 s rule; life 60 s). No part: add `"Rabbit_potion"` to
`BUILT` ("data only: a pickup; nothing walks on it"). Their `Transparent/Opaque2` bottles are mesh.js's.

### 2. Rabbit_sniperCamera: `sniperCamera` (layout; the sound by the built `playAudio`)

**What it does in BB.**
- The hero's code (`RPC_cAttack1` case 2, clip 1.0 s after `Yield(2, 1)` `Rabbit.cs:19032`, still in `attack` /
  `cAttack1`): `cAttack2` looped (`:18636-18641`); **only on the owner's own screen** (`:18646`) the prefab at hero +
  TransformDirection(0, 1.05, 0.15) (`:18684`), the camera's `specialTarget` = it (`:18709`, first person) and FOV 60
  (`:18715`); each frame the mouse turns it, pitch +-30, yaw +-60 (`:18762-18844`); at the release / cancel the target is
  cleared and it is destroyed (`:18867-18891`).
- Its script: Awake (`Rabbit_sniperCamera.cs:41-192`): enabled only with `mGameType >= 3` (`:57`, else `enabled = false`
  `:185`); the readout font `Berlin18` in (0.8, 0.2, 0.1, 0.8) (`:73-78`); range 20 + 5 per Combo rank, 40 at Combo 4
  (`:25`, `:121-163`); `hasDeadShot` with skill 411 (`:169-177`). LateUpdate (`:196-240`): it rides the hero's head
  (`:209`), and goes when the camera's target is no longer it (`:228-234`). OnGUI (`:246-526`): the scope picture
  420 x 488 px centred (`:523`; the Dead Shot one after 0.1 s on a head, `:258-290`), every 0.1 s a raycast along its
  forward (`:308-330`) with the distance "N tm" beside the centre (`:302`, `:330`); on a hit above the collider's centre by
  more than half its half-height (`:357`, the head zone) the Dead Shot clock starts (`:363-369`) and, 0.1-1 s into it, its
  AudioSource plays once (`:375-393`; `deadShot.wav` is 4.92 s, it runs to its end or until the aim leaves the head:
  `audio.Stop()` `:409-463`); the bar `castBarBG` / `castBar` (fill over 4 s) / `castBarTop` under the centre (`:495-510`).
- The prefab: no renderer; an AudioSource `deadShot`, playOnAwake off (`probe.txt:441`).

**On the page.** With Dead Shot on (passives on) the scope's horizontal ray from 1.05 m meets the target body at 1.05 m,
above its centre 0.6 by 0.45 > 0.25 (half of the half-height 0.5): the head zone, so **the sound plays about 0.1 s after the
scope appears and runs until the release**. That is the built cue option `playAudio` (Mole decision 46; `index.html:4347-4352`
starts the first playOnAwake-off AudioSource that many seconds after the spawn, Fx.dispose stops it): `[t, "fx",
"sniperCamera", {"y": 1.05, "d": 0.15, "playAudio": 0.1, "kill": <the hold>}]`. The first-person camera, FOV, scope
picture, range readout and Dead Shot bar are the camera's and the GUI's: **left out** (Bison decision 35, Cat 43, Mole 51:
camera effects and the owner's cast bars; question 1). Add `"Rabbit_sniperCamera"` to `BUILT`.

### 3. Rabbit_acidicField, Rabbit_healingField, Rabbit_stickyGum, Rabbit_mall: data only (no page code)

- `Rabbit_acidicField` / `Rabbit_healingField`: Init (`Rabbit_acidicField.cs:40-79`, `Rabbit_healingField.cs:40-77`) the
  life `nLife` (chaAdjust(12) from the hero, the Bible's section 10 / 11), then every 2 s an area tick of 12 m / 3 m
  (`Rabbit_acidicField.cs:131-198`, `Rabbit_healingField.cs:127-189`). Their particles and looping sounds (`acid2`,
  `healingField`) are the prefab's: built. The cue's `kill` 10 (the 10 s rule).
- `Rabbit_stickyGum`: the sticky status every 0.5 s within `sLv + 0.5` m and on its 1 m trigger (`Rabbit_stickyGum.cs:83-310`);
  the hero's code scales the gum `(sLv + 0.5, 1, sLv + 0.5)` (`Rabbit.cs:10072`; max rank 2 -> the cue's `"scale": [2.5, 1,
  2.5]`, the Penguin's per-axis scale) and spawns it with `FromToRotation(up, tDir)` (`:10069`). Its gum mesh is
  doubletexture.js's.
- `Rabbit_mall`: the buyers' "targetMall" button within 2 m (`Rabbit_mall.cs:184-320`; a GUI, left out with the other
  on-screen UI, Mole decision 51) and its end when the owner leaves `attack` with `mallSetup` / `mallOpen` (`:110-137`: the
  cue's `cut` at that clip time). The carpet (`Rabbit_mall1/2/3` add, on its child) is built; `mall4` / `mall5` reuse
  `Rabbit_mall3` (`probe.txt:298-304`).

Add `"Rabbit_acidicField", "Rabbit_healingField", "Rabbit_stickyGum", "Rabbit_mall"` to `BUILT`.

### 4. Unity 3.5's ParticleSystem: `extravagance_ring` (`wardrobe_fx.py` graft, page_pipeline; `fxparts/shuriken.js` unchanged)

| system (BB node, transform) | what it is (BB's full type tree, `ps_cmp2.txt`; TTO's copy the same) | BB material |
|---|---|---|
| `ParticleSystem` (3) at (0, 1.5, 0.3), -90 deg about x | one shot 1 s, hemisphere (type 2) radius 1 angle 25, life 0.5-1, speed 2-4, size 0.1-0.2 (Unity 3.5's scalar x two-constant curve = TTO's min / max), **one burst of 16 at 0.7 s**, Force on: the gold coins | `Gil` alpha |
| `ParticleSystem` (4) at (0, 1, 0) | one shot 0.3 s after a 0.1 s delay, sphere shell radius 1.2 (BB type 1 SphereShell = TTO type 0 with radiusThickness 0), **rate 45**, speed -2 to -3 (BB 3 x curve -1 / -0.667 = TTO -3 / -2: inward), life 0.3-0.5, size 0.1-0.2, ColorModule: the stars drawn in | `star5` addsoft |

Run in memory (`graft_try.py`): both match by name and material, one to one; the graft puts TTO's two components on BB's
own nodes with BB's materials, so BB's transforms hold. After it: the inventory's NOTES gain the line the Mole / Chameleon
have ("grafted from TTO's copy ... drawn").

### 5. The root EffectControl's rotation modes: `statScan`, `bounce1`, `bounce2` (`fxparts/control.js` + one call in `index.html`)

**What BB does** (`EffectControl.cs:303-416`, the live phase only, `age < life`; the same code for a root and a child, with
or without an owner):
- faceCamera (2): `transform.LookAt(Camera.main.transform.position)` (`:372`); with followPosition it then reads the owner
  (`:375-381`: statScan's owner is the scanned target, still, so its spot stays).
- faceUp (3): `rotation = FromToRotation(Vector3.forward, Math.vFlat(Camera.main.transform.forward))` (`:398`): the effect
  yawed to the camera's flat forward (bounce1 / bounce2: their dust lines and rings, life 0.5 / 2).
- followObject (1) and freeze (4): with a still owner they keep the spawn rotation (no-op on the page).

**The page today.** `fxparts/control.js:78-95` already does modes 2 and 3 for a **child** EffectControl; the root's is kept
by class Fx (`index.html:4258`) whose update reads life, afterLife, followState, velocity, never the mode. Every built class
has no root with mode 2 or 3 (Bat's two and the Mole's two roots are mode 1), so nothing shows it yet.

**The part (about 15 lines in control.js + 3 in index.html).** control.js moves its mode-2 / mode-3 code into one local
function and also registers `api.part("EffectControl(root)", (fx, node, c) => ...)`: an emitter whose update applies that
function to the root while `fx.age < c.life` (after it the rotation is left as it was, as the game's after-life branch).
index.html, in the Fx constructor after the components: `if (this.ec && (this.ec.effectRotationMode === 2 ||
this.ec.effectRotationMode === 3) && FXPARTS["EffectControl(root)"]) { const em = FXPARTS["EffectControl(root)"](this,
this.root, this.ec, null, def.nodes[0], d); if (em) this.emitters.push(em); }`. Interfaces 1.

### 6. Ten Shot's second gun: the `propCopy` cue kind (`wardrobe/index.html`, page_pipeline)

**What the hero's code does** (`RPC_tenShot`, `Rabbit.cs:38760-39640`): clip `tenShot` (0.2 fade, Once, `:39086-39091`),
`Yield(2, 0.2)` (`:39609`); case 2 (0.2 s): when `mChar.mWep1` (the worn main weapon, `RabbitEquipment.cs:929-954`:
`mountHand_R`, local zero / identity) exists, `Instantiate(mWep1)` (`:38907`) parented to `mountHand_L`, localPosition 0,
localRotation identity (`:38912-38922`): a full copy of the gun, its particles too; 24 steps of 0.1 s (`:39629`), the
shots at steps 6, 11, 15, 19, 23 (`:39265-39419`); then `Yield(4, 0.2)` (`:39607`) and case 4 (2.8 s): the copy destroyed
(`:38975-38981`) and standby (`:39004`). Interrupted earlier: destroyed at once (`:38960-38968`).

**The page part (about 30 lines, beside HeroPropHide).** `[t, "propCopy", slot, {"bone": name, "kill": s}]`: at t, a copy
of the prop worn in `slot` ("R" = mWep1) built as setProp builds a worn one (buildProp + finishProp + skinProp, its
weapon_fx particles with it: `api.propModel`'s path, `index.html:5180-5200`), hung on the hero's bone `name` at
localPosition 0 / localRotation identity (the same frame the worn piece has on its own bone, RabbitEquipment.cs:934-939),
gone at `kill`, a new pick or a class change; hidden with the hero by heroHide; nothing when no prop is worn there.
`wardrobe_fx_check.py` KINDS += `propCopy`; the cue-format comment learns it. Ten Shot: `[0.2, "propCopy", "R",
{"bone": "mountHand_L", "kill": 2.6}]`. Interfaces 2.

### 7. Contract's Light Golem (`fxparts/rabbit.js`, new; extractor lines above)

**What BB does.** `RPC_contract_create` (`Rabbit.cs:11542-11760`): sLv 3 loads `Characters/Elementals/LightGolem/LightGolem`
(`:11596`), instantiates it at `mPos`, `LookRotation(tDir)` (`:11611`) on the Rabbit's layer (`:11721`), with
`contract_create` there (`:11707`). The spot: `getExpandPos(getSpawnVector(hero + up, TransformDirection(0, -1, 3)), 1, 0.5)`
(`:40464`, `:40475`): on the ground about 3 m ahead; tDir = the hero's forward. Its own script: a 300 s life
(`LightGolem.cs:44`), the AI's `root` CrossFade, wrapMode Loop when idle (`:635-640`, `:763-768`, `:847-866`); with no foe in
its reach it stands looping `root`.

**The page part `LightGolem` (rabbit.js, about 10 lines).** At build `node.userData.fxAnim.play("root", 0, 2)` (Loop; its
data wrap is 0, `layouts_try.txt`), no AI (Mole decision 32: the summons' AI left out). The cue's `kill` 10 (the 10 s
rule). `NOT_DRAWN` keeps CharacterControl (`wardrobe_fx.py:279`); `BUILT += "LightGolem", "LightGolemAI"`. Its body is
`LightGolem1` opaque (Diffuse) on a SkinnedMeshRenderer: mesh.js. The golem's SP pick and the two lower ranks: question 3.

### 8. Sheep's `fx:cAttack_charge` on the Rabbit's `cAttack_charge` (`fxparts/sheep.js`, one line)

`fxparts/sheep.js:107`: first line of the hook `if (fx.cls !== "sheep") return null;` (the Sheep's charge ball,
Sheep.cs's code; the Rabbit's `cAttack_charge` is a star and a line burst nobody resizes, `Rabbit.cs:18988-18998`). The
Bat's `fx:castRing` serves the Chameleon and Whale on purpose (Chameleon parts.md part 8): left as it is.

### 9. Shaders and the rest: nothing to build

Read this first 3. Also checked (`probe.txt`): every Animation plays by itself (no `play` off); `millionaire1/2`'s
WorldParticleCollider (the Cat's worldcollider.js); `castStar`'s SkinnedMeshRenderer flight (`root` clip; the hero's
Instantiate at `LookRotation(tDir) x Euler(0, i x 120 / 72 / 90, 0)`, `Rabbit.cs:23920`, `:24797`, `:25621`, `:25705`);
the potions' and the gum's trigger colliders draw nothing; `backpack_ring`'s root Animation wrap 1.

## TTO: the released skills' parts (for the TTO researcher's `tto.md`; listed here so nothing is missed)

Bounty Hunt, Coin Ricochet, Medic Turret (`wardrobe/tto_released.json` rabbit clips: bountyHunt, coinRicochet, medicTurret,
clap, wai; the two emotes play no effect, Cat decision 16). Their prefabs (`tto_sum.txt`): 23 + the status looks `bounty`
and `gilded` (on the foe: left out, Sheep decision 4 / Cat 44; built). Blends: addsoft 69, `Particles/Standard Unlit` 23,
`Eric/URP Particles/Additive` 19, `FlexibleCelShader/Cel No Outline` 12, alpha 10, add 8, `Legacy Shaders/Specular` 1,
premul 1, `Eric/URP Particles/Alpha Blended` 1, `Particles/AdditiveOffset` 1.

| part | prefab(s) | what it is (`dump.cs` line, fields; RVAs; pseudo-C lines) | build home |
|---|---|---|---|
| T1 `RabbitMedicTurret` | medicTurret (root; + its CharacterControl data, a CharacterController, an Animation with no clips) | `dump.cs:120550`: Beats 10, ShotGap 1.5, ShotReach 10, CapsuleFlight 0.25, FieldRadius 6, DeployTime 0.45, FirstBeat 0.75, Life 15, TurnSpeed 540; mHead / mMuzzle / mModel = its `Head` / `Muzzle` / `Model` nodes (Awake@0x1e69a70, `RabbitMedicTurret.c:1-57`). Init@0x1e6a350 (`:58-176`): Model scale 0.01, first beat at 0.75. Update@0x1e6a6c0 (`:177-421`): Model scale `u (1 + 0.18 sin(1.5 pi u)(1 - u))`, u = age / 0.45 clamped, at least 0.01; Head turned to the flat aim at 540 deg/s (Slerp by `540 dt / angle`); a beat every 1.5 s, 10; Die at 15 s. Beat@0x1e69cb0 (`:422-570`): the hero's `MedicTurretPulse` (`Rabbit.c:40517`: the heal and `medicTurret_beat` at the turret, `:40376`), the ally `MedicTurretPick` (lowest HP %, within 10 m, the Rabbit included: on the page **the Rabbit**), kind `Random.Range(1, 4)`, the aim at the ally, `Fire` (`<Fire>d__29`@0x1e74270, `:1181-1392`: `MedicTurretShotFx` from get_Muzzle (`:629-686`: the Muzzle node, else 0.85 up) to the ally). `ShotFx`@0x1e08f90 (`Rabbit.c:40218-40375`): `medicTurret_shot` at the muzzle, RabbitTracer.Set(muzzle, ally chest), and the `TurretCapsule` coroutine (T2). Die / RPC_dead (`:714-831`, `:1393-1537`): `medicTurret_break` (`Rabbit.c:40593`), shrink over 0.4 s, Destroy | `fxparts/tto_rabbit.js` |
| T2 `Rabbit.TurretCapsule` (code mover) | medicTurret_capsule | `<TurretCapsule>d__338`@0x1e7aa60 (`Rabbit.c:24911-25140`): spawned at the muzzle, for 0.25 s (u = 4 t) moved from it to the ally's chest, turned 1080 deg/s; then Destroyed, `medicTurret_hit` at the chest (identity), and by kind 1 / 2 / 3 `lifeShot` / `boostShot` / `heatShot` at the ally's feet (identity), Destroy after 2 s | `tto_rabbit.js` + CODE_MOVERS |
| T3 `Rabbit.PosterFly` (code mover) | bountyHunt_poster (+ bountyHunt_pin) | `<PosterFly>d__353`@0x1e28850 (`Rabbit.c:556-786`): from the hand to the target's chest in 0.25 s (u = 4 t) on an arc `0.8 u (1 - u)`, turned 900 deg/s; then Destroyed and `bountyHunt_pin` at the chest | `tto_rabbit.js` + CODE_MOVERS |
| T4 `Rabbit.CoinRise` (code mover) | coinRicochet_coin (x4) | `<CoinRise>d__346`@0x1e27890 (`Rabbit.c:440-539`): `pos = from + (to - from)(1 - (1 - u)^2) + up 0.08 sin(40 delay + 6 time)`, u = age / 0.35 clamped; it bobs until the coin is shot | `tto_rabbit.js` + CODE_MOVERS |
| T5 `RabbitSpin` | coinRicochet_coin/Coin (axis (0, 1, 0), 900 deg/s) | `dump.cs:120616`; Update@0x1e6ee30 (`disasm_spin.txt`): `transform.Rotate(axis, degreesPerSecond x dt, Space.Self)` | `tto_rabbit.js` |
| RabbitTracer | bountyHunt_tracer, coinRicochet_shot / _ricochet / _cashTracer, medicTurret_shot | built (`fxparts/tto_sheep.js:245-290`): from the spawn to the cue's `to` | - |
| Shuriken NoiseModule | medicTurret_hit/Sparks | skipped today (`shuriken.js:287-290`); the Monkey's T3 / Panda's T5 add it | `shuriken.js` (whoever builds first) |
| `Eric/URP Particles/Additive` (19), `Alpha Blended` (1) | coinRicochet_cashout's stars, medicTurret's crosses / glows, medicTurret_cast's seal | not registered (`api.shader`): the Monkey's T2 spec (`plans/fx_monkey/parts.md:398`, Blend One One / SrcAlpha OneMinusSrcAlpha, Cull Off, ZWrite Off) | Monkey's file, else `fxparts/urpparticles.js` |
| `PowerUpRotation`, `Legacy Shaders/Specular`, the Animator (no controller) | bountyHunt_claim only (the kill reward, `BountyClaimFx`, `Rabbit.c:41710`) | `dump.cs:416004`, Update@0x33ad20: `Rotate(0, 0, rotationSpeed x dt)` (`reverse` never read) | left out with the claim (question 6) |
| GroundHugEmitter (9), LineRenderer, TrailRendererModern (3), Shuriken Trail / Collision / UV / ClampVelocity / Rotation / InheritVelocity, `Particles/Standard Unlit`, `FlexibleCelShader/Cel No Outline` (the turret, the capsule), premul, AdditiveOffset | all three skills | built (`groundhug.js`, `tto_sheep.js`, `shuriken.js`, `tto_penguin.js`, `particles.js`) | - |

Also: bountyHunt_flare / _muzzle carry 12 nodes with a MeshRenderer and no MeshFilter or emitter (TTO's copies of BB's
nAttack_fire nodes, emptied): they draw nothing in TTO either. Coin Ricochet's bounces (targets 2-3 within 9 m of the last
target, never the same one, `CoinNext`, `Rabbit.c:40856`) find no second foe on the page: only each coin's first hit.

## Interfaces (fixed up front, so the builders run in parallel)

1. **`"EffectControl(root)"`** (part 5): control.js registers it; `build(fx, fx.root, ec, null, def.nodes[0], data)`;
   index.html calls it once per Fx whose root EffectControl has mode 2 or 3 and pushes the emitter it returns. It turns
   the root while `fx.age < ec.life`, in Unity space as control.js's child code does.
2. **`propCopy`** (part 6): `[t, "propCopy", slot ("R", "L", "Head", "Back"), {"bone": <hero bone>, "kill": s}]`.
3. **CODE_MOVERS names** (T2-T4): the root's first comp `{"type": "Rabbit.TurretCapsule" | "Rabbit.PosterFly" |
   "Rabbit.CoinRise"}`. Their options, read as `fx.at`: `to` ([x, y, d] metres right / up / ahead of the hero: the end
   point), TurretCapsule's `kind` (the effect to drop at the ally: "lifeShot" | "boostShot" | "heatShot") and `ally`
   ([x, y, d], the ally's feet), CoinRise's `delay` (the bob's phase). On arrival they spawn with `api.spawn`:
   "tto/medicTurret_hit" at `to` and `kind` at `ally` with kill 2; "tto/bountyHunt_pin" at `to`.
4. **RabbitMedicTurret** (T1): on tto/medicTurret's root comp; options `ally` ([x, y, d] the ally's chest, default
   [0, 0.7, 0] = the Rabbit, her collider centre) and the cue's `kill` (10); it spawns "tto/medicTurret_beat" at the turret
   each beat, "tto/medicTurret_shot" at the muzzle with `to` = ally, "tto/medicTurret_capsule" at the muzzle with `to`,
   `ally` = [ally x, 0, ally d], `kind` drawn per beat (`Random.Range(1, 4)`: a third each). The entry's `"builds"`:
   ["lifeShot", "boostShot", "heatShot"] (BB's, question 5).
5. **Data names**: `LightGolem` (EXTRA_FOLDERS), BB's `extravagance_ring` with its grafted systems, the TTO prefabs as
   `tto/<prefab>`.
6. **Shared, used if present, built if absent** (whoever builds first owns it, nobody else touches it): the two Eric/URP
   shaders through `api.shader("shader:Eric/URP Particles/Additive" | "...Alpha Blended")`; NoiseModule in `shuriken.js`.
7. **Existing, used as they are:** `playAudio`, `pick: "color"`, `scale` [x, y, z], `bone`, `hideProp`, `kill`, `cut`, `to`,
   RabbitTracer, `api.spawn` + `builds`, `fxAnim.play(name, fade, wrap)`, `api.propPoint` (a TTO gun muzzle: `Row6Muzzle`
   looks for a `fire` / `muzzle` / `Fire` node under the weapon, `pseudo/Rabbit.c:39352-39420`).

## Rank by value (effects made right / effort)

| rank | part | Rabbit effects it makes right | other classes | work |
|---|---|---|---|---|
| 1 | LAYOUTS (Rabbit + golem) | 13 potions, sniperCamera extract; the golem | - | 1 block |
| 2 | root EffectControl modes (part 5) | statScan faces the camera, bounce1 / bounce2 face up | any root with mode 2 / 3 | ~18 lines |
| 3 | Shuriken graft line (part 4) | extravagance_ring's coins and stars | - | 1 line |
| 4 | propCopy (part 6) | Ten Shot's second gun | any skill that copies a worn piece | ~30 lines |
| 5 | LightGolem (part 7) | Contract's mercenary | - | ~10 lines + 2 extractor lines |
| 6 | sheep.js guard (part 8) | a warning gone on every Charge Attack | the Sheep keeps its hook | 1 line |
| 7 | TTO T1-T5 | Medic Turret, Bounty Hunt's poster, Coin Ricochet's coins | - | ~150 lines |
| 8 | shared Eric/URP shaders, NoiseModule | 20 TTO materials, 1 system | Monkey, Panda | ~30 + ~25 lines (if absent) |

After all: `BUILT` in `pipeline/wardrobe_fx_inventory.py` += `Rabbit_potion`, `Rabbit_sniperCamera`, `Rabbit_acidicField`,
`Rabbit_healingField`, `Rabbit_stickyGum`, `Rabbit_mall`, `LightGolem`, `LightGolemAI`; NOTES for extravagance_ring's
grafted systems and the 12 unlisted prefabs; run it again (the recipe's rule).

## Who builds what (never two owners for one file; as `plans/fx_wolf/build_rules.md`)

| agent | owns | builds |
|---|---|---|
| A: rabbit | `wardrobe/fxparts/rabbit.js` (new), `wardrobe/fxparts/tto_rabbit.js` (new) | part 7 (LightGolem); T1 RabbitMedicTurret, T2 Rabbit.TurretCapsule, T3 Rabbit.PosterFly, T4 Rabbit.CoinRise, T5 RabbitSpin |
| B: generic | `wardrobe/fxparts/control.js`, `wardrobe/fxparts/sheep.js`; and only if absent when it starts (`grep -l "Eric/URP" wardrobe/fxparts/*.js`; `grep -n NoiseModule wardrobe/fxparts/shuriken.js` still in `P.skipped`): `wardrobe/fxparts/urpparticles.js` (new), `wardrobe/fxparts/shuriken.js` | part 5's `EffectControl(root)`; part 8's guard; the two Eric/URP shaders (the Monkey's T2 spec); NoiseModule (the Panda's T5 / Monkey's T3 spec) |
| C: page_pipeline | `wardrobe/index.html`, `pipeline/wardrobe_fx.py`, `pipeline/wardrobe_fx_tto.py` | the LAYOUTS block; `SHURIKEN_FROM_TTO["rabbit"]`; `EXTRA_FOLDERS["rabbit"]`; `SKILL_FX["rabbit"]` + the three CODE_MOVERS; the `propCopy` kind and its comment; the `EffectControl(root)` call; `FX_PART_FILES += "rabbit", "tto_rabbit"` (+ `"urpparticles"` if B makes it) |
| lead | `pipeline/wardrobe_fx_check.py`, `pipeline/wardrobe_fx_inventory.py`, `wardrobe/fx_cues/rabbit.json` | KINDS += `propCopy`, OPTS += `ally`, `kind`, `delay`; `BUILT` / NOTES; the rebuild and the cues |

A, B and C code against Interfaces 1-6 and run in parallel. Rules as before: `node --check` on every part file, no browser
for the builders, never `wardrobe_fx.py rabbit` / `wardrobe_fx_tto.py rabbit` without `--probe` (the lead rebuilds once);
after an edit of `wardrobe/index.html`, `grep -c $'\r$' wardrobe/index.html` prints 0.

## PASTE-READY (the parts' contract; the skills researchers' entries win where they differ)

Two clips whose whole timeline this research walked. For `wardrobe/fx_cues/rabbit.json` (today `{}`), checked JSON:

```json
  "tenShot": {
    "why": "Rabbit.cs RPC_tenShot (:38760-39640), single rank: at 0 the clip (PlayAnimation(tenShot, 0.2), Once, :39086-39091), Effects/tenShot_ring at the hero, hero rotation (createEffect :39112-39124; EffectControl life 3 followPosition followState: cut at the standby) and voice tenShot1 / tenShot2 (Random.Range(0, 2) :39169-39213, PlayOneShot :39615 / :39620); Yield(2, 0.2) (:39609); 0.2 a copy of mChar.mWep1 (the worn main weapon, RabbitEquipment.cs:929-954) on mountHand_L, local zero / identity (:38907-38922): propCopy; then 24 steps 0.1 s apart (Yield(3, 0.1) :39629), step i at 0.2 + 0.1 i: two Effects/tenShot_fire at steps 6, 11, 15, 19, 23 = 0.8, 1.3, 1.7, 2.1, 2.5 s (:39265-39454), at TransformDirection(-0.6, 0.5, 0.75) / (0.6, 0.5, 0.75) looking rotateH(forward, 45) / (-45) (Math.cs rotateH: +a turns left, so yaw -45 / 45), (-0.4, 0.6, -0.5) / (0.5, 0.6, -0.5) rotateH(-135) / (135) (yaw 135 / -135), (-1.2, 0.75, 0.1) / (1, 0.75, 0.1) rotateH(90) / (-90) (yaw -90 / 90), (-0.3, 0.9, -0.7) / (0.2, 0.8, -0.7) rotateH(-180) / (180) (yaw 180), (-0.3, 0.9, 1) / (0.1, 0.85, 1) forward; each pair's hits FindAngleTarget(hero, dir, 24, 70, 3) (:39477-39480; Damage.cs:1214-1313: half-angle 35 deg), so only the last pair (forward) reaches the 10 m target: two RPC_nAttack_hit at ClosestPointOnBounds(hero + up) = the body's front (0, 1, 9.7) (:39505-39515, :39558-39568), hero rotation (:9135); after the 24th step Yield(4, 0.2) (:39607): 2.8 the copy destroyed (:38975-38981) and standby (:39004): tenShot_ring's followState cut",
    "cues": [
    [0, "voice", "tenShot1|tenShot2"],
    [0, "fx", "tenShot_ring", {"cut": 2.8}],
    [0.2, "propCopy", "R", {"bone": "mountHand_L", "kill": 2.6}],
    [0.8, "fx", "tenShot_fire", {"x": -0.6, "y": 0.5, "d": 0.75, "rot": [0, -45, 0]}],
    [0.8, "fx", "tenShot_fire", {"x": 0.6, "y": 0.5, "d": 0.75, "rot": [0, 45, 0]}],
    [1.3, "fx", "tenShot_fire", {"x": -0.4, "y": 0.6, "d": -0.5, "rot": [0, 135, 0]}],
    [1.3, "fx", "tenShot_fire", {"x": 0.5, "y": 0.6, "d": -0.5, "rot": [0, -135, 0]}],
    [1.7, "fx", "tenShot_fire", {"x": -1.2, "y": 0.75, "d": 0.1, "rot": [0, -90, 0]}],
    [1.7, "fx", "tenShot_fire", {"x": 1, "y": 0.75, "d": 0.1, "rot": [0, 90, 0]}],
    [2.1, "fx", "tenShot_fire", {"x": -0.3, "y": 0.9, "d": -0.7, "rot": [0, 180, 0]}],
    [2.1, "fx", "tenShot_fire", {"x": 0.2, "y": 0.8, "d": -0.7, "rot": [0, 180, 0]}],
    [2.5, "fx", "tenShot_fire", {"x": -0.3, "y": 0.9, "d": 1}],
    [2.5, "fx", "tenShot_fire", {"x": 0.1, "y": 0.85, "d": 1}],
    [2.5, "fx", "nAttack_hit", {"y": 1, "d": 9.7}],
    [2.5, "fx", "nAttack_hit", {"y": 1, "d": 9.7}]
    ]
  },
  "extravagance": {
    "why": "Rabbit.cs RPC_extravagance (:39823-40110), single rank: at 0 the clip (PlayAnimation(extravagance, 0.2), Once, :40003-40006) and Effects/extravagance_ring at the hero, hero rotation (createEffect :40021-40033; EffectControl life 1 + afterLife 1, followPosition; its two Unity 3.5 ParticleSystems grafted from TTO's copy: the 16 coins at 0.7 s, the stars drawn in from 0.1 s; plans/fx_rabbit/parts.md part 4); no voice (none loaded); Yield 0.5 (:40100), Yield 0.2 (:40095): 0.7 atkUp on the hero for chaAdjust(6) (:39902; CharacterControl.cs:33176 loads no look); Yield 0.3 (:40107): 1.0 standby (:39933)",
    "cues": [
    [0, "fx", "extravagance_ring"]
    ]
  }
```

Cue fragments for the other part-bearing skills (their times and keys are the skills researchers'):
- Charge Attack's scope, at the start of the aim loop (`cAttack2`, clip 1.0 of `cAttack1`, `Rabbit.cs:18636-18715`):
  `[0, "fx", "sniperCamera", {"y": 1.05, "d": 0.15, "playAudio": 0.1, "kill": <hold>}]`.
- Sticky Gum: `[t, "fx", "stickyGum", {"d": <spot>, "scale": [2.5, 1, 2.5], "kill": 10}]`.
- Mix / Shake / Miracle Blend potions: `[t, "fx", "hpPot4", {"x": <1.5 sin a>, "d": <1.5 cos a>, "kill": 10}]` per potion
  (a = -i x 120 or 72 deg: rotateH turns left), with `castStar` at the hero turned to each, `castLight` at each spot.
- Acidic / Healing Field: `[t, "fx", "acidicField", {"d": <spot>, "kill": 10}]`.
- Mall: `[t, "fx", "mall1|mall2|mall3|mall4|mall5", {"pick": "color", "cut": <leaves mallSetup / mallOpen>}]`.
- Contract: `[t, "fx", "LightGolem", {"d": 3, "kill": 10}]` and `[t, "fx", "contract_create", {"d": 3}]`;
  `[t0, "fx", "contract_flag", {"bone": "mountHand_L", "kill": ...}]`.
- Stat Scan: `[t, "fx", "statScan", {"y": <1.1>, "d": 9.7}]` (ClosestPointOnBounds(hero + 1.5 up) on the body = (0, 1.1, 9.7);
  identity; it turns to the camera by part 5).
- TTO Medic Turret: `[0.55, "fx", "tto/medicTurret", {"d": 1.8, "kill": 10}]`, the entry's `"builds": ["lifeShot",
  "boostShot", "heatShot"]`; Bounty Hunt's poster `[0.4, "fx", "tto/bountyHunt_poster", {<the hand>, "to": [0, 0.6, 10]}]`;
  Coin Ricochet's coins `[0.3, "fx", "tto/coinRicochet_coin", {<the hand>, "to": [<spot>], "delay": <k>}]` x4 and their shots
  as RabbitTracer cues with `to` (tto.md's times: the Bible's 0.3 / 0.75-1.35 / 0.4-1.55 s).

## plans/fx_inventory.md's per-effect status (the Rabbit)

`### rabbit`: 84 listed, 66 ready, 18 needing a part: `acidicField`, `healingField`, `stickyGum` (their 0-byte scripts: data
only, part 3), `hpPot1-4`, `spPot1-3`, `randomPot1-6` (Rabbit_potion: layout, part 1), `sniperCamera` (layout, part 2),
`extravagance_ring` (ParticleSystem: graft, part 4). The scan does not see: the 12 unlisted prefabs (Read this first 7;
`mall1-5` would read "needs Rabbit_mall"), the root rotation modes (statScan, bounce1, bounce2: listed ready, drawn wrongly
until part 5), the hero code's second gun and summon (parts 6-7), the missing prefabs (item 8). After the build all 96 +
the golem are ready.

## Left out (with reasons)

- The scope's first-person camera, FOV 60, scope picture, range readout, Dead Shot picture and bar (camera effects and
  the owner's GUI: Bison decision 35, Cat 43, Mole 51). Its sound stays.
- Mall's buyers' button and the shop window (on-screen UI, Mole 51).
- The potions' pickups and the drinker's looks `enlarge` / `reduce` / `miracleDrop` / `autoLife` (nothing walks onto a
  potion; Life Shot's look is on an ally): built, not cued (Sheep decision 4 for looks on others).
- Bounty Hunt's kill reward (`bountyHunt_claim`, needs a kill: Chameleon decision 53) with its `PowerUpRotation`,
  `Legacy Shaders/Specular` and controller-less Animator; the `bounty` / `gilded` looks on the foe (Cat decision 44); Coin
  Ricochet's bounces (no second foe); Contract's Panther / Leopard ranks (question 3).
- The seven missing prefabs (item 8): the game draws nothing there.

## How sure I am

| item | sure | why |
|---|---|---|
| The LAYOUTS block | high | public fields in declaration order (`Rabbit_potion.cs:528`, `Rabbit_sniperCamera.cs:553-592`, `LightGolem.cs:1144-1159`, `LightGolemAI.cs:1462`); 4 / 24 / 40 / 8 bytes; 97 prefabs build in memory |
| The four 0-byte scripts draw nothing | high | read whole: ticks, statuses, a GUI button, Destroy |
| extravagance_ring = TTO's copy | high | life, speed, size, shape, burst / rate, delay compared (`ps_cmp2.txt`); the graft run in memory |
| Root modes 2 / 3 missing on the page | high | `index.html:4258` keeps the root's ec, its update (`:4334-4372`) never reads the mode; `control.js:78-95` is the child's |
| The scope's sound at ~0.1 s, to the release | medium-high | the head-zone test with the page's body (1.05 vs 0.85); the OnGUI 0.1 s throttle; 4.92 s clip |
| Ten Shot's times and the two hits | high | case numbers and Yields read in order; FindAngleTarget's half-angle (`Damage.cs:1232`) |
| The golem's spot and loop | medium-high | `:40464` / `:11611`; the AI's idle CrossFade root Loop; getExpandPos's free-spot shift not modelled |
| TTO T1-T5 | medium-high | pseudo-C read for the flow; the floats at their addresses as Ghidra shows them; the turret's ally = the Rabbit (the page's only ally) |

## Open questions (each with my recommended answer)

1. **The scope.** Draw the first-person scope picture over the page (an emblem-style screen overlay, the Wolf's
   emblem.js) or leave the camera's view out? Recommended: **left out** (Bison 35 / Cat 43 / Mole 51: camera effects and
   the owner's GUI), the Dead Shot sound kept with `playAudio` 0.1.
2. **The Combo with Snipe Mastery shows no hit** (`snipeShot_hit` is missing, passives on). Recommended: **as the game**
   (no Combo hit drawn), the attacks researcher's call; offered to the Bible.
3. **Contract's mercenary.** The top rank (the golem, SP >= 65 after the cost, `Rabbit.cs:7619`) only? Recommended: **yes,
   the Light Golem** (the top-rank rule); Panther / Leopard not built (YAGNI: no tile shows them).
4. **The Medic Turret's capsules fly back to the Rabbit** (she is the only ally, `MedicTurretPick` includes her; it fires
   at full HP too). Recommended: **yes** (as the game would with her alone), the head turning to her at 540 deg/s.
5. **The capsule's drop (`lifeShot` / `boostShot` / `heatShot`): BB's prefabs or TTO's copies?** Recommended: **BB's**
   (built for Medical Shot already; TTO's are BB's re-serialised, as every copy compared so far: Mole, Chameleon).
6. **Bounty Hunt's kill reward** (claim, PowerUpRotation, Specular). Recommended: **not built** (no kill on the page,
   Chameleon decision 53); PowerUpRotation is `Rotate(0, 0, speed dt)` should a kill option come.
7. **The Eric/URP shaders and NoiseModule** if the Rabbit builds before the Monkey / Panda. Recommended: **builder B
   builds them generic** (`urpparticles.js`, `shuriken.js`) and the Monkey / Panda builders use them.

## Offers for the Bible (never written there)

- Snipe Mastery's Combo hit and Knee Shot's hit are missing prefabs: no hit effect is drawn (`Rabbit.cs:11435-11460`,
  `:17594-17611`, `:18271`, `:9669-9692`, `:23288-23305`); also `fourShot_hit`, `circleShot_hit`, `tenShot_hit`,
  `herbFinder`, `contract_ring` ("Cannot find").
- Acidic Field / Healing Field pulse 7 times at base CHA, not 6 (the expiry frame's Destroy falls into one more tick,
  `Rabbit_acidicField.cs:212-216`, `Rabbit_healingField.cs:203-207`): the card's pulse count `floor(chaAdjust(12) / 2)` is
  one short (to verify with a game test: medium-high sure).
- `Rabbit_potion`'s "taken" flag is never set (`Rabbit_potion.cs:121`, `:150`, `:525`).
- The scope only on the owner's screen and only in `mGameType >= 3`; Dead Shot's sound runs from 0.1 s on a head to the
  release or the aim leaving the head (`Rabbit_sniperCamera.cs:57`, `:375-463`).
- Contract's golem's second material is for layer 9 only (`LightGolem.cs:83-109`).

## Verification (13/11/2026)

Checker, office PC, read only (probes in `checks/fx_rabbit_research/verify/tp/`: `layouts_try.py` = this report's
LAYOUTS + EXTRA_FOLDERS run again in memory -> `layouts_try.txt`; `bb_probe.json` = `wardrobe_fx.py rabbit --probe` of
seven effects with today's tables; `tto_probe.json`; `cues_check.py` = the paste-ready block parsed and every cue checked
as `pipeline/wardrobe_fx_check.py:221-222` does, keys against `wardrobe/data/rabbit/clips.json`, names against the rip).
This section wins over the body above.

1. **Confirmed (no change).** LAYOUTS: **97 built, 0 raise** again (`layouts_try.txt`: hpPot1-4 / spPot1-3 / randomPot1-6
   potionType 0-12, sniperCamera [9, 67] / [9, 54] / false / 0, LightGolem's five refs, LightGolemAI "none"; refs are 8
   bytes in this Unity, so 8 + 8 + 4 + 4 = 24); today hpPot1, randomPot6, sniperCamera raise "no layout"
   (`bb_probe.json`) and extravagance_ring builds without its two ParticleSystems. Ten Shot (`Rabbit.cs:38873-39010`,
   `:39236-39640`): the counter starts at 0 at 0.2 s (`:38928`), +1 per `Yield(3, 0.1)` (`:38952`), shots at i = 6 / 11 /
   15 / 19 / 23 = 0.8 / 1.3 / 1.7 / 2.1 / 2.5 s, i = 24 -> `Yield(4, 0.2)` -> 2.8 s the copy destroyed and standby
   (`:38974-39004`): kill 2.6 from 0.2 is right; the positions and `Math.rotateH` signs (`Math.cs:838-843`: +a turns the
   forward to -x, the left) give the block's yaws; the last pair's dirs are `forward` (`:39414-39419`); FindAngleTarget
   halves its 70 (`Damage.cs:1232`), so only that pair hits; `RPC_nAttack_hit` draws `nAttack_hit` at the hit point with
   the hero's rotation (`:9112-9150`), at ClosestPointOnBounds(hero + up) = (0, 1, 9.7); voices tenShot1 / tenShot2 at 0
   (`:39181-39229`, PlayOneShot `:39615` / `:39620`). tenShot_ring: life 3, followState (`bb_probe.json`): cut
   2.8. Extravagance: only `extravagance_ring` (`:40003-40033`; no voice or sound load). Contract: 1 + (sp >= 35) +
   (sp >= 65) (`Rabbit.cs:7596-7622`), sLv 3 = LightGolem (`:11590-11597`). Snipe Mastery: `hasSkill(431)` ->
   `RPC_snipeShot_hit` (`:17594-17611`), whose prefab is missing (`:11448`, `:11467`). The Rabbit's `cAttack_charge` has
   only an ImageEmitter and a LineEmitter (`parts/probe.txt:100-103`): the Sheep hook only warns, nothing is resized.
   Acidic Field's expiry falls into one more tick (`Rabbit_acidicField.cs:216`: `136361 - 412693 == -276332` is true ->
   `goto IL_15E`). The block parses: 2 keys, real clips (tenShot 3.0 s, extravagance 1.2 s), 16 cues, every name in the
   rip; it needs the `propCopy` kind (not in `wardrobe_fx_check.py:186` KINDS or the page yet: part 6). Icons:
   `data/icons/hd/index.json` has tenShot / extravagance.

2. **`Rabbit.PosterFly` (Interfaces 3, T3, the fragment at "TTO Medic Turret ... Bounty Hunt's poster"): wrong end point and
   a second pin.** The poster flies to the target's chest **+ 0.6 up** (`pseudo/Rabbit.c:650-654`: Row6Chest, then
   `+ Vector3.up x 0.6`), so `to` = **[0, 1.2, 10]**, not [0, 0.6, 10]; and the pin spawns at the chest (`:747-764`),
   which `tto.md` already cues at 0.65 s (y 0.6, d 10). Corrected: **PosterFly spawns nothing on arrival** (only moves and
   spins, 0.25 s; the cue's `kill` 0.25 ends it), as the Chameleon's `Chameleon.ApexArrow` code mover whose impact is a
   cue (Chameleon decision 59, `wardrobe/fx_cues/chameleon.json:647`). T3's "from the hand to the target's chest" reads
   "to the chest + 0.6 up". The fragment: `[0.4, "fx", "tto/bountyHunt_poster", {"x": -0.039, "y": 0.884, "d": 0.349,
   "to": [0, 1.2, 10], "kill": 0.25}]` (`tto.md` section 7, as written there).

3. **`RabbitMedicTurret` (Interfaces 4, T1): adopted as the owner of the beats, with three fixes** (`tto.md` Verification
   2 drops its cued beats for this contract: one owner per beat, Mole decision 32 / `fxparts/robots.js:57-68`).
   - **The end is missing.** At `end` (seconds after the spawn; the cue's 10, Monkey decision 30) the game's Die ->
     `<RPC_dead>d__31` (`RMT.c:1393-1537`) spawns `tto/medicTurret_break` at the turret and shrinks the Model linearly to
     0.01 over 0.4 s; the beats stop. The cue's `kill` is end + 0.4 = **10.4**, not 10.
   - **Beats:** the first at age 0.75 (`RMT.c:142`), then every 1.5 s (`:403`), at most 10, only while age < `end`
     (7 here). Each: `tto/medicTurret_beat` at the turret, identity; the Head snapped to the flat direction to `ally`
     (`:1321-1327`; turned toward it at 540 deg/s between beats, `:314-351`); the muzzle = the `Muzzle` node's world
     position after the snap (`:1351`); then shot and capsule as written. `medicTurret_beat` comes from Fire's
     `BeatFx` (`RMT.c:1251` -> `Rabbit::MedicTurretBeatFx` `Rabbit.c:40376`), **not** from `MedicTurretPulse`
     (`Rabbit.c:40517-40592` only heals): T1's "the heal and medicTurret_beat" is one effect too many.
   - **One turret at a time:** at its build an earlier live `tto/medicTurret` is removed at once
     (`RPC_medicTurret_create`, `Rabbit.c:39906-39916`: the old `mTurret` destroyed; matters with วนซ้ำ on, which recasts
     every 1.3 s).
   The Medic Turret fragment reads `[0.55, "fx", "tto/medicTurret", {"d": 1.8, "end": 10, "kill": 10.4, "ally": [0, 0.7,
   0]}]` with the entry's `"builds": ["lifeShot", "boostShot", "heatShot"]` (`tto.md` Verification 2 has the whole
   entry). Interfaces 3's TurretCapsule (spawns `tto/medicTurret_hit` at `to` and `kind` at `ally`, kill 2, on arrival at
   0.25) stands.

4. **Part 5: statScan does not keep its spot.** With an owner and followPosition, BB's faceCamera branch moves the root
   every live frame after the turn: `position = owner.position + transform.TransformDirection(offset)`
   (`EffectControl.cs:372-381`; the opaque predicates `79799 - 144601 == -64802`, `144276 - 591515 == -447239`,
   `200154 - 143541 != 56614` all true), with `offset = spawn - owner.position` taken in world space at Init (`:96-104`,
   `88945 - 567211 == -478266` true). statScan is `createEffect`d on the scanned target (`Rabbit.cs:22512-22524`, owner =
   the target, whose transform is at its feet), and its EffectControl has followPosition true (`parts/probe.txt:467`), so
   the world offset (0, 1.1, -0.3) is turned by the camera-facing rotation each frame: with the camera behind the hero the
   scan sits about **0.3 m behind the target's centre line** (yaw 180: (0, 1.1, 10.3)) and swings round the target as the
   view turns, not at (0, 1.1, 9.7). Corrected part: `EffectControl(root)` also takes the cue option `owner` ([x, y, d],
   the owner's transform position); with modes 2 / 3, followPosition and an `owner`, after the turn it sets the root's
   position to owner + R x (spawn - owner) (R = the new rotation; Unity space, as control.js); without `owner` it only
   turns (bounce1 / bounce2: Instantiated, no owner). Stat Scan's fragment: `[t, "fx", "statScan", {"y": 1.1, "d": 9.7,
   "owner": [0, 0, 10]}]`. A game quirk worth offering to the Bible (the scan's mark drifts behind the target).

5. **The lead's checker lines (section "Who builds what", "lead"):** KINDS += `propCopy`; OPTS += **`delay`, `ally`,
   `owner`** (not `kind`: it rides `api.spawn`'s options from the turret part and never stands in a cue file; `end`
   exists already).

6. **Small corrections.** The FXPARTS hook lookup is at `index.html:4289` today (the body's `:4251`; `:4258` for the root
   EffectControl is still right); the TTO materials are 63 distinct, of them `Eric/URP Particles/Additive` **15** and
   `Alpha Blended` 1 (`tto_probe.json` "materials"; the body's 19 counts uses, as its addsoft 69 does). **Both shared
   parts exist now** (built by the Monkey's builders during this check, uncommitted): `api.shader("shader:Eric/URP
   Particles/Additive" | "... Alpha Blended")` in `fxparts/tto_monkey.js:153-154` (in `FX_PART_FILES`,
   `index.html:4088`) and NoiseModule in `fxparts/shuriken.js:310-323`, `:488`; so builder B builds neither (its own
   `grep` condition), no `urpparticles.js`, and tto.md's P6 is done. Part 7: the Monkey's (uncommitted)
   `fxparts/elementals.js` has a `standing` summon mode (root looped from 0, no ring, `elementals.js:146`, options
   comment) that would cover the golem with one SUMMONS entry; it is the Monkey builder's file, so the golem stays in
   `rabbit.js` as written (one owner per file).

7. **Nothing missed** in the parts scope: the TTO table's prefabs equal `SKILL_FX["rabbit"]`'s 25 and the probe's
   (`tto_probe.json`), the three CODE_MOVERS are the three code-moved prefabs, and the BB side's blocked set matches the
   raises and the hero-code reads above.
