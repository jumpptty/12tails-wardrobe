# Monkey effects: the parts the page cannot draw yet (or draws wrongly)

Research 13/11/2026, office PC (one of the Monkey fx researchers; scope: every part the Monkey's effects need: the
inventory's 51, the 14 Monkey prefabs it does not list, the components `wardrobe_fx.effect()` drops, the shaders, the hero
code acting on its effects, the summons the Monkey's skills make (five elementals, the Lavu serpent, the two armours), and
the released TTO skills' prefabs: Buiten Bastion, Ja Ascension, Rune Golem (`golemCall`), Solar Call (`sunAvatar`)).
Models: `plans/fx_mole/parts.md`, `plans/fx_chameleon/parts.md`. Read only: nothing in `wardrobe/data` was written;
`wardrobe_fx.py` / `wardrobe_fx_tto.py` ran with `--probe` only (or were imported read only); no browser. BB lines are
`C:\Users\Jump\Desktop\12tails\DecompiledSource\<file>` (= the home PC's `D:\12tails\...`), read through `annotate.py`
(every opaque `if (a - b ==/!= c)` evaluated to TRUE / FALSE, line numbers kept); TTO is `TTO1102:` =
`DecompiledSource_TTO_2026-11-02` (`dump.cs`, `pseudo/Monkey.c`, `pseudo/CharacterControl.c`). `Rotate.cs` is not in BB's
decompile (an `Assembly-UnityScript-firstpass` script, not decompiled): its source is Reborn's,
`DecompiledSource_Reborn/Assembly-UnityScript-firstpass/Rotate.cs:7-31`, its 16 bytes confirm the fields.

The Mole build is running beside this research: its LAYOUTS (with `rotationControl`), the `"s"` string type, `FIELD_PREFABS`,
`SOUND_REFS`, the robots' `EXTRA_FOLDERS` and `clip_dict` are already in the working tree's `pipeline/wardrobe_fx.py`
(uncommitted); `fxparts/mole.js`, `rotationcontrol.js`, `robots.js`, `tto_mole.js` are not written yet. This report leans on
those as they are described in `plans/fx_mole/decisions.md` 32-34, 53-54.

Probes (read only, outputs beside them) in `checks/fx_monkey_research/parts/` (git-ignored; re-run on either PC):
- `probe.py monkey` -> `probe_monkey.txt`, `probe_monkey.json`: all **65** prefabs in `heroes/monkey/effects` through
  `wardrobe_fx.effect()` (unknown scripts' bytes captured instead of raising; the Mole's `rotationControl` layout in memory),
  every component type per node (what `effect()` drops), every material's blend. Last lines: dropped `BoxCollider 7,
  Rigidbody 7, ParticleSystem 3, ParticleSystemRenderer 3`; `UNKNOWN scripts: Monkey_earthPulse [0], Monkey_fireBall [4 x4],
  Monkey_lavu [0], Monkey_runicFlame [24], Rotate [16 x2], Monkey_runicSand [24]`. `show.py`, `clips.py`: node trees,
  every Animation's clips. `loaded.txt` + `diff.py`: the prefabs Monkey.cs loads by path vs the folder.
- `summons.py` -> `summons.txt`; `summons2.py` -> `summons2.txt` (Gaos, the elemental Lavu); `refs.py` -> `refs.txt` (the
  summons' script fields decoded with the layouts below, each reference resolved); `dupes.py` (container keys that repeat).
- `physics.py` -> `physics.txt` (Rigidbody / BoxCollider of the projectiles); `psmats.py` -> `psmats.txt` (volcanicEruption's
  Shuriken materials, hpTransfer's bolt target).
- `catalog_keys.py` -> `catalog_keys.txt` (TTO's 649 Monkey addresses); `tto_probe.json` / `.err` (`wardrobe_fx_tto.py monkey
  --probe` of the 25 TTO prefabs) + `tto_sum.py` -> `tto_summary.txt`, `tto_detail.py` (the Shuriken modules the page skips);
  `golem.py` -> `golem.txt`, `golem.json` (TTO's Rune Golem folder, the address base swapped); `shader_state.py` ->
  `shader_state.txt` (TTO's `Eric/URP Particles/*` pass state); `tto_clips.py` -> `tto_clips.txt` (TTO's AnimationClips).
- `src/*.txt`: `annotate.py` of Monkey.cs, Monkey_*.cs, the summons' scripts, CharacterControl.cs, Math.cs, rotationControl.cs.

## Read this first

1. **Six Monkey scripts and one Unity 3.5 component block or spoil 14 BB effects; one shader is new (a one-line alias).**
   | effect | what blocks it | today |
   |---|---|---|
   | `fireBall1`-`4` (Fireball, by rank: top = `fireBall4`) | `Monkey_fireBall` (4 bytes `mLv`, no layout): the 30 m/s shot, its hit | **not buildable** (raises) |
   | `earthPulse` | `Monkey_earthPulse` (0 bytes): the 15 m/s shot, its hit | builds, **hangs** at the muzzle |
   | `lavu` (Lavu, the serpent) | `Monkey_lavu` (0 bytes): the summon / standby / upheaval / unsummon flight, the body chain; `rotationControl` on 5 segments; `FX/Lavu` on every mesh | builds, **stands still** (and its material falls back) |
   | `runicFlame`, `runicSand` (one trap segment each) | `Monkey_runicFlame` / `_runicSand` (24 bytes, no layout): data only | **not buildable** |
   | `runicFlame_ring`, `runicSand_ring` (status looks on the Monkey) | `Rotate` (16 bytes, no layout): the rune disc's spin | **not buildable** |
   | `volcanicEruption` | Unity 3.5's ParticleSystem (3 systems), dropped | builds without its smoke / fire bursts |
   | `mikeBlink` | the hero's code reparents the worn weapon (`mWep1`, slot R) onto its animated `mount_Summon` node | builds, an animated **empty** node |
   | `phoenixArmor`, `gadinaArmor` (Fire Avatar / Earth Form) | the hero's code plays their clips (`summon`, then `root`, the attacks' `nAttack*` / `cAttack*` / `blazingForm*`) | play their default `root` only |
   Shader: `FX/Lavu` (`Lavu.mat`, the serpent) is `FX/Phoenix`'s pass without the Transparent queue tags (rip
   `Resources/gameassets/shader/Lavu.shader:1-21` vs `Phoenix.shader:1-23`): mesh.js's `phoenix(d)` draws it (part 7). Every
   other BB blend is built (`probe_monkey.txt`: addsoft 121, add 12, alpha 7, opaque 7, FX/Phoenix 2, AlphaOffset 1, premul 1,
   multiply 1, multiply2 1).
2. **The Monkey is a summoner: five elemental characters and a serpent.** Summon Phoenix / Ja / Gadina / Buiten Hou Hou /
   Gaos instantiate whole characters from `Resources/GameAssets/Characters/Elementals/` (`Monkey.cs:11430-11547`,
   `:11932-12049`, `:12653-12770`, `:13210-13327`, `:14432`), each with CharacterControl + its own script + an AI and legacy
   clips (`summon` / `create`, `root`, `run`, attacks); the top ranks are Phoenix4, Ja4, Gadina4, Buiten4, Gaos. Lavu is not
   an elemental here: Monkey.cs spawns `Effects/lavu` (`Monkey_lavu`, `:13889-13915`); the elemental `Lavu/Lavu` prefab
   (CharacterControl + `Lavu` + `LavuPart`) is used only by `Game.cs`. By the Penguin's Mana Vortex and the Mole's robots
   (Mole decisions 32-34): the summons are built and shown, playing their summon clip then `root`, cut at 10 s (part 9).
3. **Two extractor gaps the summons hit.**
   - `Game.container` (`wardrobe_fx.py:327`, `{k: v for k, v in m_Container}`) keeps the **last** entry of a repeated key:
     `gameassets/characters/elementals/gaos/gaos` and `.../lavu/lavu` are listed twice (GameObject, then the MonoScript of the
     same name: `dupes.py`), so the Gaos summon (and `gaos/effects/gaosfire`) resolve to a MonoScript and do not build. 40
     effect keys repeat across the game (bugs, robots, tails); none of the Monkey's own effects. Fix: prefer the GameObject.
   - The summons' own effects are mostly **script fields with no Resources path** (`refs.txt`: Phoenix's `summon_ring`,
     `fireBall`, `fireBall_hit`, `instantBlaze_ring`, `skyCrimson_*`; Ja's `summon_ring`, `suicideBomb`; Gadina's
     `summonEffect`, `Gadina_sword1-4`, `Gadina_shield1-4`, `nAttack_hit1-4`, `earthGuard_ring`, `planetBreaker1-2`; Buiten's
     `summonEffect`; their AudioClips); only the Gaos' are in Resources. The Mole build's `FIELD_PREFABS` / `SOUND_REFS` carry
     them; their names repeat (three `summon_ring`, two `summonEffect`, Phoenix's `fireBall_hit` vs the Monkey's own), so they
     get prefixed effect names (LAYOUTS section).
4. **The inventory misses 14 Monkey prefabs; none of them blocks beyond the table above.** From `diff.py` and the greps:
   - status looks `CharacterControl.cs` loads: `buitenSoul`, `gadinaSoul`, `gaosSoul`, `jaSoul`, `phoenixSoul`
     (`:38149-38299`, on the soul's holder, `mChar.bounds.center + 0.5 height up`, identity), `fireKeep` (`:38118-38139`),
     `ignite` (`:37899-37906`, on the target's collider centre), `groundLock` (`:17134`, the target), `runicFlame_ring`,
     `runicSand_ring` (`:37854`, `:38066`: parented to the Monkey, identity, named `runicFlameFx` / `runicSandFx`, removed by name);
   - hero prefab fields: `castRing` (`Monkey.cs:19306`, Instantiate `:24882`), `castEffect_fire` (`:19309`, `:26461` ...:
     hero + `TransformDirection(0, 1, 1)`, hero rotation), `hpTransfer` (`Monkey_hpTransfer`, `:19276`, `:21027`);
   - `elementalBound` (the Bat's `RPC_elementalBound` loads it, `Bat.cs:15705`: another class's).
   All use built parts. `castRing` here has no Animation (`probe_monkey.txt`: EffectControl life 999, followState): bat.js's
   `fx:castRing` hook is not needed (its `cls` check leaves the Monkey out, correctly). `hpTransfer`'s BoltEmitter has no
   TargetNode (`psmats.txt`: -1): the page's "no TargetNode aims at the cue's `to`" (index.html:3904) covers it; the hero's
   code sets `TargetPosition = target collider centre - forward x 2 x extents.x` every frame (`Monkey.cs:21179-21181`, `:20996`).
   Tool gap (as before): `wardrobe_fx_inventory.py` sees neither status looks, hero prefab fields, summons, nor the hero's
   code acting on an effect (mikeBlink, the armours).
5. **The TTO released skills bring four TTO scripts, a summon, two shaders and four Shuriken modules the page skips**
   (`tto_summary.txt`, `tto_detail.py`, `golem.txt`, `shader_state.txt`):
   - scripts `BastionWardFx` (bastionWard), `MonkeyBuitenOffering` (buitenBastion_offering), `SunCrownFx` (solarCrown),
     `SunburnFx` (sunburn), `MonkeyRow6Rise` (the Rune Golem's quake spikes), and the summon `RuneGolem`
     (`GameAssets/characters/elementals/runeGolem/RuneGolem`, `TTO1102:pseudo/Monkey.c` `RPC_runeGolem_create` RVA 0x1ccf990;
     `dump.cs:113918`), with its own 13 effects under `elementals/runegolem/effects/`;
   - shaders `Eric/URP Particles/Additive` (35 materials: Blend One [_Blend2] = One One, Cull [_CullMode] = Off, ZWrite Off,
     ColorMask RGB) and `Eric/URP Particles/Alpha Blended` (1: SrcAlpha OneMinusSrcAlpha);
   - Shuriken `SubModule` (buitenBastion_rise, runeGolem_crumble / _quake / _rise: the crystal burst's children are
     sub-emitters), `NoiseModule` (jaAscension_pillar), `LightsModule` (the burst Lights), `CustomDataModule` (read by no
     page shader: nothing to draw), all in shuriken.js's "not drawn" list (`shuriken.js:287-291`);
   - an `Animator` with the Mecanim controller `FX_Magic_Circle` on the three Sigils (buitenBastion_offering,
     jaAscension_callFx, runeGolem_circle), and every TTO `Animation`'s clips "written by name only, not exported"
     (`tto_probe.err`: solarCrown's / sunAvatar_comet's Ja, the offering's Buiten idol, the Rune Golem). The legacy clips are
     plain curves (`tto_clips.txt`: `m_Legacy` true, not compressed, rotation / position / scale curves only), so BB's clip
     reader shape reads them (part T1).
6. **Game quirks (offer to the user for the Bible; none changes a cue).**
   - Summon Gaos with Fire Soul #422 looks for `Effects/volcanicSoul_ring`, which BB does not hold: "Cannot find
     volcanicSoul_ring Effect" on every such summon (`Monkey.cs:14376-14407`); the Phoenix's is `fireSoul_ring` (`:11360-11372`).
   - Runic Flame / Runic Sand pass their life through the RPC's `tID` argument: `Init(owner, char, tID)` sets `mLife =
     Time.time + nLife` (`Monkey.cs:12509`, `:13775`; `Monkey_runicFlame.cs:20-27`).
   - The Mike Blink strike carries the worn weapon itself off the hand (`Monkey.cs:35920-35933`: `mWep1.transform.parent =
     mikeBlink/mount_Summon`), and `resetMikeBlink` puts it back on the hero's `mount_Summon` (`:14015-14029`): a weapon whose
     prefab sits off its mount's origin snaps to local zero / identity / scale 1 after each blink.
   - Gadina's sword and shield are chosen by Titan Sword / Aegis of Earth rank at the summon, not by the Gadina's rank
     (`Gadina.cs:544-622`, `:715-793`: rank 0-3 -> `Gadina_sword1-4` on `mount_Hand_R`, `Gadina_shield1-4` on `mount_Hand_L`,
     ATK +0 / 20 / 35 / 50).
   - The Fire Avatar / Earth Form armours are destroyed in the Monkey's Update as soon as her action is not "attack" and
     neither the status nor the command is held (`Monkey.cs:460-530`): standing in the form keeps them, the code crossfades
     them to `root` / `run` by her moveSpeed (< 2: `root`) with a 0.2 s fade.

## The Monkey's blocked set

"Where" is where BB spawns it; the times and the tiles are the skills researchers' (`attacks_emotes.md`, `skills_*.md`,
`effect_only.md`, `tto.md`), so the cue shapes here are the parts' contract.

| effect | skill (spawn) | missing part(s) | where |
|---|---|---|---|
| `fireBall4` (+ `fireBall_hit`) | Fireball `RPC_fireBall_fire` (`Monkey.cs:11092-11278`): `LookRotation(fireDir)` (`:11099`), life `2 x rangeMod` (`:11278`) | LAYOUT + `Monkey_fireBall` mover | firePos (the cast's), aimed at the target |
| `earthPulse` (+ `earthPulse_hit`) | Earth Pulse `RPC_earthPulse_fire` (`:13104`, life 3 `:13113`); hit `RPC_earthPulse_hit` coroutine | `Monkey_earthPulse` mover | firePos, `LookRotation(fireDir)` |
| `lavu` (+ `lavu_ring`) | Lavu `$RPC_lavu_cast` (`:34445-34870`): `RPC_lavu_summon` (`:13876-13930`) | `Monkey_lavu`; `rotationControl` (Mole build); FX/Lavu alias | hero + `TransformDirection(0, -2, 3)`, `LookRotation(forward) x Euler(-90, 0, 0)` (pointing up) |
| `runicFlame`, `runicSand` | Runic Flame / Sand (`:12491-12509`, `:13757-13775`) | LAYOUTS (data only) | tPos, `LookRotation(tDir)` |
| `runicFlame_ring`, `runicSand_ring` | the `runicFlame` / `runicSand` statuses (`CharacterControl.cs:37854`, `:38066`) | LAYOUT + `Rotate` part | parented to the Monkey, identity |
| `volcanicEruption` | Volcanic Eruption (`Monkey.cs:43326-43861`) | Shuriken graft (one table line) | the cast point (Bible 2.6) |
| `mikeBlink` | Mike Blink `$RPC_mikeBlink1` (`:35713-36270`, Instantiate `:35895-35933`) | `fx:mikeBlink` (the worn R piece on its `mount_Summon`) | `mPos + tDir`, `LookRotation(vFlat(tDir)) x Euler(270, 90, 0)` |
| `mikeCircle` | HP Transfer with Mike Circle #411 (`:21055-21067`) | none (built) | target collider centre - 0.15 up, hero rotation x `Euler(270, 90, 0)`; life 99: the cue's `kill` |
| `phoenixArmor` (+ `_create`, `_destroy`) | Fire Avatar (`:38380-38450`: Instantiate at the hero, parented, local 0, `Play("summon")`) | clip timeline (part 8) | the hero (`followNode`), local 0 |
| `gadinaArmor` (+ `_create`, `_destroy`) | Earth Form (`:40732-40747`, `Play("summon")`) | clip timeline (part 8) | the hero, local 0 |
| Phoenix4 / Ja4 / Gadina4 (+ sword4, shield4) / Buiten4 / Gaos | Summon Phoenix / Ja / Gadina / Buiten / Gaos (`:11380-11740`, `:12207`, `:12957`, `:13460`, `:14595`) | EXTRA_FOLDERS, layouts / NOT_DRAWN, FIELD_PREFABS, container fix, summon part (part 9) | `mPos`, `LookRotation(tDir)` |
| TTO: bastionWard (+ chip / break / hit) | Buiten Bastion | `BastionWardFx` | the holder (`CharacterControl.c:17302-17309` Bind) |
| TTO: buitenBastion_offering (+ awaken / burst / lock / rise / slam) | Buiten Bastion | `MonkeyBuitenOffering`; Animator `FX_Magic_Circle`; TTO clips; Shuriken Sub / Lights | tto.md's |
| TTO: jaAscension_* | Ja Ascension (`pseudo/Monkey.c:10252` `<RPC_jaAscension_cast>d__315`) | Animator; Shuriken Noise | tto.md's |
| TTO: runeGolem_circle / _stomp, the RuneGolem summon + its 13 effects | Rune Golem (`golemCall`, `:16230` `<RPC_runeGolem_cast>d__320`, `RPC_runeGolem_create`) | TTO summon extraction (3 gaps), `RuneGolem`, `MonkeyRow6Rise`, TTO clips, Shuriken Sub / Lights | tto.md's |
| TTO: solarCrown, sunburn, sunAvatar_* | Solar Call (`RPC_sunAvatar_cast`, `RPC_solarEcho`, `RPC_solarCollapse`) | `SunCrownFx`, `SunburnFx`; TTO clips (solarCrown / comet's Ja model) | tto.md's |
| TTO: every `Eric/URP Particles/*` material | all four skills | the two shaders (api.shader) | - |

## LAYOUTS (paste into `pipeline/wardrobe_fx.py`, after the Mole's blocks)

```python
# the Monkey's parts (plans/fx_monkey/parts.md, 2026-11-13; checks/fx_monkey_research/parts/probe_monkey.txt, refs.txt: each
# instance's bytes are the listed fields exactly); Monkey_earthPulse / Monkey_lavu keep every field private (0 bytes)
LAYOUTS.update({
    "Monkey_fireBall": [("mLv", "i")],                # Monkey_fireBall.cs:327 (4 bytes: fireBall1-4 = 1-4; its damage only, :200)
    # Monkey_runicFlame.cs:239-248 / Monkey_runicSand.cs:261-270 (24 bytes, all zero in the prefab; Init sets them, data only)
    "Monkey_runicFlame": [("mLife", "f"), ("mOwner", "r"), ("mOwnerChar", "r"), ("isInit", "b")],
    "Monkey_runicSand": [("mLife", "f"), ("mOwner", "r"), ("mOwnerChar", "r"), ("isInit", "b")],
    # Rotate (Assembly-UnityScript-firstpass; BB's not decompiled, Reborn's DecompiledSource_Reborn/
    # Assembly-UnityScript-firstpass/Rotate.cs:7-9, ctor default (10, 15, 19)): 16 bytes; runicFlame_ring/magicRune
    # (0, 0, 180) false, runicSand_ring/magicRune (0, 0, 120) false (fxparts/rotationcontrol.js)
    "Rotate": [("speed", "v3"), ("useWorldSpace", "b")],
    "Monkey_earthPulse": [], "Monkey_lavu": [],
})
# the Monkey's summons (Resources characters/elementals/<x>/<x><rank>, EXTRA_FOLDERS; plans/fx_monkey/parts.md part 9):
# data only (fxparts/elementals.js plays their clips); every public field in declaration order (refs.txt decodes the top
# ranks with them, byte for byte); the AIs' 8 bytes are the Mole's "s" string ("none")
R = lambda *ns: [(n, "r") for n in ns]
LAYOUTS.update({
    # Buiten.cs:522-552 (52 bytes)
    "Buiten": [("BuitenType", "i")] + R("mSummoner") + [("isSummon", "b"), ("followDistance", "f")]
              + R("mSummonerChar", "summonEffect", "buiten_summonFX", "buiten_unsummonFX"),
    # Gadina.cs:2344-2422 (180 bytes)
    "Gadina": [("GadinaType", "i"), ("mSwordLv", "i"), ("mShieldLv", "i")]
              + R(*[f"Gadina_sword{i}" for i in range(1, 5)], *[f"Gadina_shield{i}" for i in range(1, 5)],
                  *[f"nAttack_hit{i}" for i in range(1, 5)], "nAttack_hitFX", "earthGuard_ring", "planetBreaker1",
                  "planetBreaker2", "gadina_cry", "mSummoner")
              + [("isSummon", "b"), ("followDistance", "f")] + R("mSummonerChar", "summonEffect"),
    # Ja.cs:1319-1349 (56 bytes)
    "Ja": [("JaType", "i")] + R("mChar", "suicideBomb_hit", "mSummoner") + [("isSummon", "b"), ("followDistance", "f")]
          + R("mSummonerChar") + [("mSummonLv", "i")] + R("summon_ring"),
    # Phoenix.cs:2103-2154 (124 bytes)
    "Phoenix": [("PhoenixType", "i")] + R("mChar", "pheonix_cry", "fireBall", "fireBall_hit", "instantBlaze_ring",
                                           "skyCrimson_dust", "pheonix_skyCrimsonFX", "skyCrimson_fire", "skyCrimson_hit",
                                           "mSummoner")
               + [("isSummon", "b"), ("followDistance", "f")] + R("mSummonerChar")
               + [("mRapidFireLv", "i"), ("mIntenseFireLv", "i")] + R("summon_ring", "pheonix_unsummon"),
    # Gaos.cs:2098-2164 (144 bytes; all its effects are also in Resources, gaos/effects/)
    "Gaos": R("gaos_cry", "footStep_left", "footStep_right", "nAttack1_ring", "nAttack2_ring", "nAttack_hit",
              "nAttack_hitFX", "tailSpin_ring", "tailSpin_hit", "tailSpin_hitFX", "gaosFire_ring", "gaosFire",
              "gaosFire_hit", "rampage_ring1", "rampage_ring2", "summon_ring", "unsummon_ring", "dead_ring"),
    "Gadina_AI": [("AI_state", "s")], "Ja_AI": [("AI_state", "s")], "Phoenix_AI": [("AI_state", "s")],
    "Gaos_AI": [("AI_state", "s")],                    # *_AI.cs (8 bytes: "none"; Gaos_AI.cs:1626)
})
```

Extractor lines (lead, `wardrobe_fx.py`):
- `SHURIKEN_FROM_TTO["monkey"] = ["volcanicEruption"]`, **no** `SHURIKEN_MAT` entry: the Chameleon's by-material route.
  BB's three `Particle System` nodes (one name, three times) carry `Bomb2` (multiply2) at (0, 3, 0), `ExplosionRay` (addsoft)
  at 0, `Bomb4` (multiply2) at (0, 3.6, 0) (`psmats.txt`); TTO's copy has `tto_Bomb2`, `tto_ExplosionRay`, `tto_Bomb4` at the
  same places (`tto_summary.txt`), one each: a unique match.
- `EXTRA_FOLDERS["monkey"] = ["gameassets/characters/elementals/phoenix", "gameassets/characters/elementals/ja",
  "gameassets/characters/elementals/gadina", "gameassets/characters/elementals/buiten", "gameassets/characters/elementals/gaos",
  "gameassets/characters/elementals/gaos/effects"]` (the cue names Phoenix4, Ja4, Gadina4, Buiten4, Gaos, and Gaos'
  `summon_ring` etc. by the aliases below).
- `Game.__init__`: keep the GameObject when a container key repeats (`for k, v in rm["m_Container"]: if k not in self.container
  or <v is a GameObject>: self.container[k] = v`), else Gaos and `gaosFire` resolve to their MonoScripts (Read this first 3).
- `FIELD_PREFABS["monkey"]` (the Mole build's mechanism; names prefixed, the field names repeat across summons):
  `phoenix_summon_ring` (phoenix/phoenix4, Phoenix, summon_ring), `ja_summon_ring` (ja/ja4, Ja, summon_ring),
  `buiten_summonEffect` (buiten/buiten4, Buiten, summonEffect), `gadina_summonEffect` (gadina/gadina4, Gadina, summonEffect),
  `gadina_sword4` (gadina/gadina4, Gadina, Gadina_sword4), `gadina_shield4` (gadina/gadina4, Gadina, Gadina_shield4); the
  rest (`phoenix_fireBall`, `phoenix_fireBall_hit`, `phoenix_instantBlaze_ring`, `phoenix_skyCrimson_*`, `ja_suicideBomb`,
  `gadina_nAttack_hit4`, `gadina_earthGuard_ring`, `gadina_planetBreaker1/2`) only if a tile cues the summons' moves.
  `ALIASES["monkey"]`: `gaos_summon_ring` -> `gameassets/characters/elementals/gaos/effects/summon_ring` (and the other Gaos
  effects a tile names). `SOUND_REFS |= {"Buiten", "Gadina", "Phoenix", "Gaos"}` (their summon / cry clips) if the part
  plays them; `SOUND_ALIASES["monkey"]["lavu_summon"] = "characters/elementals/lavu/sounds/lavu_summon"` (Lavu's cast sound,
  `Monkey.cs:34644-34656`, a Sounds clip outside the hero's folder).
- `NOT_DRAWN` keeps `CharacterControl`.

## Each part

Page parts plug in as the comment above `FX_PART_FILES` says (`wardrobe/index.html:3869-3938`, read 13/11/2026):
`wardrobe/fxparts/<file>.js` default-exports `register(api)`, `api.part(type, build)`; `build(fx, node, comp, mat, nodeDef,
data)` returns `{ node, update(dt, cam) ("destroy"), stop?(), dispose?() }` or null; `"fx:<effect>"` = the hero's code
acting on that effect; `api.spawn(name, at, opts)` (+ the entry's `"builds"`), `opts.followNode` / `opts.local`;
`api.propModel(slot, fallback)`; `node.userData.fxAnim.play(name, fade, wrap)` (mesh.js:270-341). Space: Unity's, inside the
effect's mirror group, the hero's feet at the origin, +z her facing. The target body (Bat decision 4): centre (0, 0.6, 10),
h 1, r 0.3 (box x +-0.3, y 0.1..1.1, z 9.7..10.3).

### 1. Monkey_fireBall, Monkey_earthPulse: the two straight shots (`fxparts/monkey.js`, new)

**What they do in BB.** One pattern (the Mole's shells without gravity):
- ctor: a private local velocity, `Monkey_fireBall.cs:26` **(0, 0, 30)**, `Monkey_earthPulse.cs:26` **(0, 0, 15)**.
- Awake (`Monkey_fireBall.cs:38-51`, `Monkey_earthPulse.cs:38-51`): layer 1, `rigidbody.velocity =
  TransformDirection(v)` once. Rigidbody **gravity off**, rotation frozen (112), drag 0; trigger box 0.25 x 0.25 x 0.5
  centred on the root (`physics.txt`).
- FixedUpdate (`:63-79`): clock; at `ProjectileControl.life` Destroy: fireBall `2 x rangeMod` (`Monkey.cs:11278`),
  earthPulse 3 (`:13113`). No LookAt (no gravity: the heading never changes).
- OnTriggerEnter (`Monkey_fireBall.cs:91-264`, `Monkey_earthPulse.cs:91-194`): any collider not on the owner's layer, 1 or
  2 -> Destroy (`:158`), `isDestroyed`, then on the owner's client `vector = mCollider.ClosestPointOnBounds(collider.bounds.
  center)` (`:170`), `RPC_fireBall_hit(vector, forward, 0)` (`:185`) / `StartCoroutine(RPC_earthPulse_hit(vector, forward, 0))`
  (`Monkey_earthPulse.cs:185`). The hits: `fireBall_hit` at hitPos with **the hero's** rotation (`Monkey.cs:11318`);
  `earthPulse_hit` from the coroutine (its own timeline: the skills researcher's).
- The trail: fireBall's root carries its own EllipsoidParticleEmitter (world space, Smoke3) and the skinned `FireBall` head
  (`root` clip 0.4 s, loop) scaled 1 / 1.2 / 1.6 / 2 by rank (`probe_monkey.txt` node 1); earthPulse two particle children.

**The page part (monkey.js, about 40 lines; reuse the Mole's shell mover if `mole.js` exports it, Interfaces 1).** A table
`SHOT = { Monkey_fireBall: { v: 30, life: 2, half: [0.125, 0.125, 0.25], hit: "fireBall_hit", rot: "hero" },
Monkey_earthPulse: { v: 15, life: 3, half: [0.125, 0.125, 0.25], hit: "earthPulse_hit", rot: "fwd" } }`; build: `vel =
(0, 0, v) x fx.uQuat(node)`; each 0.02 s step `p += vel x 0.02`, life -> `"destroy"`; contact: the target body (box centre
within `0.3 + 0.25` of the axis and y in the body's range, then `ClosestPointOnBounds` = p clamped into the body box), else
the floor (lowest box corner <= 0, hit `(p.x, 0, p.z)`); on contact `api.spawn(hit, { x, y, d: z, rot })` (`[0, 0, 0]` for
"hero" = the page's facing; `lookEuler(vel)` for "fwd", the earthPulse_hit coroutine's own rotation the skills researcher
reads) and `"destroy"`. `"builds": ["fireBall_hit"]` / `["earthPulse_hit"]`. APPROX: floor and body are the only colliders.

### 2. Monkey_lavu: the serpent (`fxparts/monkey.js`)

**What it does (`Monkey_lavu.cs`, all private).** Nodes (`show.py lavu`): root (the head end) at 0; `body1`-`body5`, `tail`
children at local z -3, -6, -9, -12, -15, -18, each with a `model` child (a Lavu mesh, FX/Lavu; models 2-5 and the tail's spin
by `rotationControl` x +-90 deg/s, self space: part 3); `head` at 0; `particle` (Acid3) at z -0.29.
- `summon(summoner)` (`:333-466`): owner, state summon, `t0 = now`; `parts[0..5] = Find("body1".."body5", "tail")`
  (`:353-383`); the trail `h[8]`: `h[0] = root`, `h[i + 1] = parts[i].position`, `h[7] = tail` (`:388-420`); next sample at
  `now + 0.25` (`:425`); then each FixedUpdate `Translate(10 x forward x dt)` (`:457`: **10 m/s along its own forward**)
  until `now >= t0 + 2` (`:436`) -> standby.
- Update (`:23-140`), once started: owner gone -> Destroy (`:140`); in **standby** (`:42-58`): `forward = RotateTowards(
  forward, summoner + 4 up - position, dt, 1)` (`:48`: turns at most **1 rad/s**), `Translate(8 x forward x dt)` (`:53`:
  **8 m/s**), `rotation = LookRotation(forward)`; in every state: when `now > next` (`:64`), `next = now + 0.25`, shift
  `h[i] = h[i - 1]` for i = 7..1, `h[0] = position` (`:75-97`); then for j = 0..5 (`:103-125`): `parts[j].position =
  Lerp(h[j], h[j + 1], 4 (next - now))`, `parts[j].rotation = LookRotation(Slerp(h[j] - h[j + 1], h[j + 1] - h[j + 2],
  4 (next - now)))` (world). So each segment slides from one sample to the next over 0.25 s: a chain 2.5 m apart at 10 m/s,
  2 m at 8 m/s.
- `upheaval()` (`:600-686`, the Upheaval command while summoned): `t0 = now`; while the summoner's `actionState == "attack"`
  and `myCommand == "upheaval"`: `target = summoner + rotateH(6 forward, Repeat(120 (now - t0), 360)) + up x sin(4 now)`
  (`:632`; rotateH `Math.cs:840-841`: x = -r sin a, z = r cos a); for the first 3 s `position = Slerp(position, target,
  0.33 (now - t0))`, `rotation = LookRotation(target - position)` (`:637-648`), then `position = target`, `rotation =
  Euler(-30 cos(4 now), -Repeat(90 + 120 (now - t0), 360), 0)` (`:657-662`); then standby again (`:672`).
- `unsummon()` (`:886-930`): state unsummon, `t0 = now`; the `particle` emitter's emit off (`:892-912`); each frame
  `Translate(8 forward dt)` (`:839`) and every renderer's `_Color = (0.86, 0.86, 0.86, Lerp(0.86, 0, now - t0))` (`:867`);
  Destroy at `t0 + 1` (`:819-825`).
- Spawn (`Monkey.cs:13899`): hero + `TransformDirection(0, -2, 3)` (`:34550`: under the floor, 3 m ahead), rotation
  `LookRotation(forward) x Euler(-90, 0, 0)`: its forward points **up**, so it bursts out of the ground and climbs 20 m in 2 s
  (to y 18), then turns over towards the Monkey's head + 4 m and circles there (8 m/s at 1 rad/s: a loop of radius 8 m).

**The page part `Monkey_lavu` (monkey.js, about 60 lines).** State from the cue: `fx.at.lavu` = `"summon"` (default) or
`"upheaval"` (Upheaval's tile: start already summoned, circling), `fx.at.unsummon` (age, optional). The summoner = the hero's
feet (0, 0, 0) of the effect's space (the cue sits at the hero; `d` / `y` only offset the spawn). Each frame: the state's
move (above, page dt; summon on a 0.02 s step as FixedUpdate), the 0.25 s trail sampling, and the six segments written in
the effect's space (they are children of the root in the prefab: write their local transform = root^-1 x world, or detach
them under the effect group at build). Unsummon: the materials' opacity x `Lerp(0.86, 0, t) / 0.86`, the particle node's
legacy emitter `stop()`, `"destroy"` at 1 s. The cue's `kill` (10 s rule: the status is `chaAdjust(60)`, `Monkey.cs:34561-
34590`) ends it otherwise. APPROX: `transform.Find` children only; the summoner standing still (the hero is in place).

### 3. rotationControl and Rotate (`fxparts/rotationcontrol.js`; the Mole's file, one more part)

- `rotationControl` (the Mole's part 5, built by the Mole build): `lavu`'s nodes 4, 6, 8, 10, 14: (90, 0, 0) / (-90, 0, 0)
  alternating, `useWorldRotation` false (`probe_monkey.txt`): each segment rolls a quarter turn a second about its own x.
- `Rotate` (new, about 8 lines): `Update`: `useWorldSpace` ? `transform.Rotate(speed x dt, Space.World)` :
  `transform.Rotate(speed x dt, Space.Self)` (Reborn `Rotate.cs:19-29`). Self: `node.quaternion.multiply(q(Euler(dt x
  speed, "YXZ", radians)))` (as rotationControl's false branch); World: `node.quaternion.premultiply(...)` of the same
  rotation expressed in the parent's frame (inside the mirror group Unity's numbers hold). The two rune discs: (0, 0, 180)
  and (0, 0, 120) deg/s about the disc's local z (the disc node is turned `(0.5, -0.5, -0.5, -0.5)`, so local z is the
  world's up: the rune spins flat on the ground). Add `"Rotate"` to `BUILT`.

### 4. Monkey_runicFlame, Monkey_runicSand: data only (layouts, no page code)

`Init(owner, ownerChar, nLife)` (`Monkey_runicFlame.cs:20-48`): `mLife = now + nLife`, owner, started; Update: owner gone /
dead or the life over -> Destroy (`:69-123`); OnTriggerEnter (box 0.3 x 1 x 1.2 at (0, 0.5, -0.8), `physics.txt`): a foe ->
`hit(1, talAdjust(24))` / Runic Sand `groundLock` Lv 1 for `getDebuff(2)` s (`Monkey_runicSand.cs:207-225`). They draw only
their child emitters (Flame2 / Dust3, built). The page: no part; the cue's `kill` is their life. Add `"Monkey_runicFlame",
"Monkey_runicSand"` to `BUILT` ("data only: the trap's segments; the cue's kill").

### 5. Volcanic Eruption's Shuriken (`wardrobe_fx.py` graft, lead; shuriken.js unchanged)

The table line above. Modules (TTO's copies, `tto_summary.txt`): Initial, Shape, Emission, Size, Color, Force, Rotation: all
read by shuriken.js. The prefab: EffectControl 12 s + 3 after (`probe_monkey.txt`), AudioControl (0.5 in, 11, 0.5 out),
Animation `root` 12 s (the volcano mesh rising and sinking): the 10 s rule cuts it (`kill` 10).

### 6. fx:mikeBlink: the worn weapon on the blink (`fxparts/monkey.js`)

**What BB does (`$RPC_mikeBlink1`, `Monkey.cs:35760-36270`).** Case 2: the voice (`:31`), `mikeBlink` at `mPos + tDir`,
`LookRotation(vFlat(tDir).normalized) x Euler(270, 90, 0)` (`:35895-35920`), `mWep1.transform.parent = mikeBlink/
mount_Summon` (`:35920-35933`, localPosition kept as the world pose: Unity's reparent); the prefab's Animation `root` (1.1 s,
Once) moves `mount_Summon` from (3.77, 0.57, 0.95) (`show.py mikeblink`); the strike box at the end; case 3/4
`resetMikeBlink()` (`:14015-14029`): back on the hero's `mount_Summon`, local zero / identity / scale 1, the effect destroyed.
`mWep1` is the Monkey's first piece (MonkeyEquipment.cs:932-957, on `mount_Summon`): the page's slot **R** (placements.json
`weapons.monkey.fallback.bone` = `mount_Summon`).

**The page part (about 15 lines).** `api.part("fx:mikeBlink", fx => ...)`: at build, `const m = api.propModel("R", true)`
(`PROP_STARTER.monkey = { R: "noviceMike" }`, item_map w_mnk1, Interfaces 2), added under the node named `mount_Summon` at
local 0 / identity (APPROX: Unity keeps the world pose at the reparent; the hand's mount and the node's start differ by the
prefab's offset, and the next frame's clip pose moves it anyway); freed with the effect. The hand's own piece is hidden for the
blink by the cue `[t, "hideProp", "R", {"kill": d}]` (built kind). `"builds"`: none.

### 7. FX/Lavu (`fxparts/mesh.js`, one line)

`mesh.js:187` `else if (d.blend === "shader:FX/Phoenix") m = phoenix(d);` -> `|| d.blend === "shader:FX/Lavu"`. The two
shaders are the same pass (fixed-function lit, `combine texture * primary double, texture alpha * primary alpha`, Blend
SrcAlpha OneMinusSrcAlpha, AlphaTest Greater 0, ColorMask RGB); FX/Lavu has no `QUEUE=Transparent` tag (Geometry queue) and
`Fallback "Diffuse"`. `Lavu.mat`: `_Color` (0.777, 0.777, 0.777, 0.792), `_Emission` (0.059, 0.059, 0.059, 0)
(`probe_monkey.txt`, rip `Material/Lavu.mat`): the serpent draws 79 % opaque, lit x 1.55 plus a faint self glow. APPROX:
queue order (the page sorts it with the transparent pass). Lavu's unsummon fade writes `_Color.a` (part 2): opacity.

### 8. The armours' clip timeline (`fxparts/elementals.js`, shared with part 9)

`phoenixArmor` / `gadinaArmor` (no EffectControl, no AudioSource): parented to the Monkey at local 0 / identity
(`Monkey.cs:38395-38438`, `:40732-40747`), `Play("summon")` (1.0 s / 0.8 s, Once), then the Update's `CrossFade("root", 0.2)`
while she stands (`:509`, `:573`; `run` when moving), wrapMode Loop (`:523`, `:587`); the form's attacks play `nAttack` /
`blazingForm1` / `blazingForm2` (`:39224`, `:40001`, `:39595`) on the Phoenix one and `nAttack1-3`, `cAttack0-2` on the Gadina
one (`:41444`, `:41836`, `:42370`, `:43279`, `:42918`, `:42786`), the Phoenix's back to `root` with 0.5 s (`:40360`).
**The page:** `api.part("fx:phoenixArmor" | "fx:gadinaArmor", fx => ...)`: a timeline from the cue option `clips` =
`[[age, clip, fade?, wrap?], ...]` (default `[[0, "summon"], [len(summon), "root", 0.2, 2]]`), each item at its age calling
the root node's `fxAnim.play(clip, fade, wrap)`. The cue rides the hero: `{"bone": null, "kill": K}` with followPosition
(the effect sits at the hero; the hero is in place). Clip lengths (`clips.py`): phoenixArmor root 1.3 Loop, run 1.0, nAttack
1.0, blazingForm1 0.8, blazingForm2 0.7 Loop, summon 1.0; gadinaArmor root 1.0 Loop, run 0.8, summon 0.8, nAttack1 1.2,
nAttack2 1.0, nAttack3 1.0, cAttack0 0.5, cAttack1 0.5, cAttack2 2.0 Loop.

### 9. The summons: Phoenix, Ja, Gadina, Buiten Hou Hou, Gaos (`fxparts/elementals.js`, new)

| summon (top rank) | prefab | scripts (bytes) | clips (`summons.txt`) | summon coroutine |
|---|---|---|---|---|
| Phoenix4 | `elementals/phoenix/phoenix4` | CharacterControl 684, Phoenix 124, Phoenix_AI 8 | root, run, ko, summon, nAttack, skyCrimson1/2, instantBlaze (play, Once) | `Phoenix.cs:4297-4313`: `Play("summon")`, `summon_ring` at its position, identity; `Yield 1` (`:4510`) |
| Ja4 | `elementals/ja/ja4` | CharacterControl 672, Ja 56, Ja_AI 8 | root, run, ko, summon, unsummon, suicideRun | `Ja.cs:1997-2013`: `Play("summon")`, `summon_ring`; `Yield 1` (`:2047`) |
| Gadina4 | `elementals/gadina/gadina4` | CharacterControl 676, Gadina 180, Gadina_AI 8 | root (Loop), run, die, summon, unSummon, nAttack4, planetBreak, guard | `Gadina.cs:6134-6139` the ranks; the sword / shield on `mount_Hand_R` / `_L` (`:544-622`, `:715-793`) |
| Buiten4 | `elementals/buiten/buiten4` | CharacterControl 684, Buiten 52 | root, create, destroy, unSummon | `Buiten.cs:761-812`: `Play("create")`, `summonEffect` at its pose; `Yield 1` |
| Gaos | `elementals/gaos/gaos` (container fix) | CharacterControl 668, Gaos 144, Gaos_AI 8 | root, run, ko, nAttack1/2, tailSpin, gaosFire, rampage1/2, summon, unsummon | `Gaos.cs:4873-4925`: `Play("summon")`, `createEffect(summon_ring, its pose)`; waits 0.7 / 0.8 / 1.2 |
The spawn (each `RPC_<x>_create`): Instantiate at `mPos`, `LookRotation(tDir)` (`Monkey.cs:11380-11420` Phoenix; the others
the same shape), layer = the Monkey's, CharacterControl owner fields, then `StartCoroutine(<x>.summon(...))` (`:11740`,
`:12207`, `:12957`, `:13460`, `:14595`); with Fire Soul #422 the Phoenix summon also spawns `fireSoul_ring` at the hero
(`:11360-11372`). `mPos` is the cast's (the skills researchers').

**The page part (elementals.js, about 50 lines).** Registered for the scripts `Phoenix`, `Ja`, `Gadina`, `Buiten`, `Gaos` (the
summon's root node): the clip timeline of part 8 (default `[[0, "summon"], [len, "root", 0.2, 2]]`; Buiten's first clip
`create`), the summon's ring spawned at build (`api.spawn("phoenix_summon_ring" | "ja_summon_ring" | "gaos_summon_ring" |
"buiten_summonEffect" | "gadina_summonEffect", { x, y, d, rot })` at the root's spawn pose, the entry's `"builds"`), and for
Gadina the cue option `attach` = `[["gadina_sword4", "mount_Hand_R"], ["gadina_shield4", "mount_Hand_L"]]` spawned with
`followNode` = the named bone node of this Fx, `local` zero / identity. No AI (no `run`, no attacks): the moves the summon
commands play (Summon Attack's) are left to a later job (question 6). Cut at 10 s. CharacterControl and the summons' scripts
draw nothing themselves (layouts above, or `NOT_DRAWN`). The summons' legacy clips extract through BB's clip reader
(Animation on the root; the Mole build's `clip_dict` reads events too).

## TTO parts (the released skills: Buiten Bastion, Ja Ascension, Rune Golem, Solar Call)

All page code in `fxparts/tto_monkey.js` (new) and `fxparts/shuriken.js`; the extractor in `wardrobe_fx_tto.py`. Field values
are the prefabs' (`tto_probe.json`, `golem.json`); the methods' bodies are not in `pseudo/` (only their callers): the builder
disassembles them at the RVAs `dump.cs` gives (the Chameleon's `disasm.py` route: capstone over the client's
`GameAssembly.dll`, calls named from `methods.tsv`). The timelines are `tto.md`'s.

### T1. Extractor (`wardrobe_fx_tto.py`, lead)

- **Legacy AnimationClips**: today every TTO `Animation`'s clips are "written by name only, not exported" (`tto_probe.err`).
  TTO's clips are legacy with plain rotation / position / scale curves (`tto_clips.txt`: `m_Legacy` true, not compressed, no
  float curves), so the BB reader's shape (`wardrobe_fx_mesh` clip_dict: `{len, wrap, tracks: {node: {path, q, p, s}}}`,
  paths resolved against the prefab's nodes) reads them. Needed by solarCrown / sunAvatar_comet (a Ja model: root, run, ko,
  summon, unsummon, suicideRun), buitenBastion_offering's Buiten idol (root, create, destroy, unSummon), the Rune Golem,
  volcanicEruption's TTO copy (not used: BB's is built).
- **Addresses outside `heroes/<cls>/`**: `Tto(cls, names)` builds `gameassets/characters/heroes/<cls>/<folder>/<name>`
  (`wardrobe_fx_tto.py:308`); the Rune Golem lives at `gameassets/characters/elementals/runegolem/runegolem` and its
  effects under `.../runegolem/effects/` (`golem.txt`). An `EXTRA_FOLDERS`-like list per class (`"monkey":
  ["gameassets/characters/elementals/runegolem", "gameassets/characters/elementals/runegolem/effects"]`), tried after the
  class's own folder (`golem.py` swaps the base and builds all 13 effects).
- **The root GameObject**: `runegolem` raises `KeyError: 'm_Component'` (`golem.txt`): its bundle container maps the id to
  more than one asset and the last one is not the GameObject; take the GameObject (as BB's container fix).
- `SKILL_FX["monkey"]` = `tto.md`'s list (the 25 prefabs probed here + the golem's).

### T2. `Eric/URP Particles/Additive` and `Alpha Blended` (`tto_monkey.js`, api.shader)

Pass state (`shader_state.txt`, raw): Additive `Blend One [_Blend2]` (every material saves `_Blend2` 1: One One), `Cull
[_CullMode]` (0: Off), ZWrite Off, ZTest LEqual, ColorMask RGB; Alpha Blended `SrcAlpha OneMinusSrcAlpha`, Cull Off, ZWrite
Off. Properties: `_MainTex`, `_Noise`, `_Flow`, `_Mask`, `_SpeedMainTexUVNoiseZW`, `_DistortionSpeedXYPowerZ`, `_Emission`,
`_Color`, `_Usecenterglow`, `_Usedepth`, `_Usecustomrandom`, `_Depthpower`, `_CullMode`, `_Blend2` (+ `_Opacity` for Alpha
Blended): Hovl Studio's particle shaders (`Blend_TwoSides` / `Add_CenterGlow` family). Every Monkey material has `_Noise`,
`_Flow`, `_Mask` unset and the speeds 0, `_Usecenterglow` / `_Usedepth` 0 (`tto_probe.json` props). So the fragment reduces
to `col = tex x _Color x vertexColor x _Emission`, Additive `rgb x alpha` added (One One), Alpha Blended `alpha = tex.a x
_Color.a x vcol.a x _Opacity`. The compiled programs are not in the parsed form (`m_SubPrograms` empty: the blob is
compressed); APPROX until the builder decompresses one (medium sure: the property set and Hovl's published shaders agree).
Note `tto_flare_h47s10`'s `_Color` 5.28 (HDR): no clamp before the blend.

### T3. Shuriken: SubModule, NoiseModule, LightsModule (`fxparts/shuriken.js`)

- **SubModule** (buitenBastion_rise node 1, runeGolem_crumble / _quake / _rise / _pound: `"subEmitters": [{"emitter": {"node":
  2}, "type": 0 (Birth), "properties": 2, "emitProbability": 1}]`): the child system is not played on its own; each particle
  born in the parent starts one emission of the child at that particle's position (Birth; type 1 Collision, 2 Death),
  `properties` 2 = InheritColor? (Unity's SubEmitterProperties bit mask: 1 InheritColor, 2 InheritSize, 4 InheritRotation,
  8 InheritLifetime, 16 InheritDuration): 2 = the size. The parent here is a carrier with no renderer material (`mats [None]`).
- **NoiseModule** (jaAscension_pillar "Sparks Confetti Noise": strength 0.2): Unity's curl noise; APPROX acceptable (a
  value-noise offset per particle), or leave the sparks un-noised (question 9).
- **LightsModule** (the bursts' "Light" nodes, with a `Light` component the module copies per particle: ratio 1, range 2,
  intensity 1): one api.pointLight per system at the particles' centre, or skip (question 9). `CustomDataModule`: nothing to
  draw (no page shader reads custom data).

### T4. The Animator `FX_Magic_Circle` (`tto_monkey.js` + extractor)

The three Sigils (offering node 12, jaAscension_callFx node 1, runeGolem_circle node 1) carry an `Animator` whose Mecanim
controller is written by name only. A Mecanim (non-legacy) clip needs the muscle-clip reader (streamed / dense / constant
curves + the binding constant) in `wardrobe_fx_tto.py`; a smaller route: probe the controller's single clip at build time
and, if it only scales / spins the Sigil node, write it as a legacy-shaped clip (`fxAnim`). Question 8.

### T5. The TTO scripts (`tto_monkey.js`)

| script | prefab | fields (dump.cs) | values (prefab) | methods (RVA) |
|---|---|---|---|---|
| `BastionWardFx` | bastionWard (28 nodes: 6 plates of `Stone` + `Rune`, Runes GroundHug, Glyphs) | `:110111` ring, plates[], chip, spin; mHolder, mFull, mShown, mRest[] | ring node 1, plates 2/6/10/14/18/22, chip `bastionWard_chip` | Bind 0x1ce3c20 (`CharacterControl.c:17309`), Awake 0x1ce3a90, LateUpdate 0x1ce3d40, FirstShown 0x1ce3c60 |
| `MonkeyBuitenOffering` | buitenBastion_offering | `:112263` idol, circle, plate, awaken, burst, lockOn; consts LiftEnd 0.9, BurstAt 1.25, FlyTime 0.7, FlyStagger 0.05, OrbitTime 0.45, LockAt 2.65, Plates 6, LiftHeight 1.7, LiftSwell 1.25, ArcHeight 4.5, ChestHeight 1, IdolChest 2.2 | idol node 1, circle 11, plate 26, awaken / burst / lockOn the three prefabs | Init 0x1d15fb0 (`pseudo/Monkey.c:900`), HideBody 0x1d15ef0, Run 0x1d16350, Slot 0x1d16500, Bezier 0x1cc2d50, Spawn 0x1d165a0, Shake 0x1d163c0 |
| `SunCrownFx` | solarCrown (halo, orbit with a Ja model) | `:114096` halo, ring, orbit, orbitRadius, orbitSpeed, ringSpeed | halo 1, ring null, orbit 6, 0.75, 140, 40 | On 0x1d6e380, SunAt 0x1d6e5a0 (`Monkey.c:17847`, `:44649`), Bind 0x1d6de50, LateUpdate 0x1d6ded0, Relight 0x1d6e460 |
| `SunburnFx` | sunburn | `:114078` ring, marks[], spin | ring 1, marks 2/5/8/11/14, spin 120 | Bind 0x1d6e830, LateUpdate 0x1d6e860 |
| `MonkeyRow6Rise` | runeGolem_quake Spike0-5 | `:112319` delay, depth, riseTime, hold, sinkTime, overshoot, tilt | delay 0.03-0.05, depth 1.13-1.66, riseTime 0.13, hold 0.7, sinkTime 0.5, overshoot 0.15, tilt 25.6-32.3 | Awake 0x1d16800, Update 0x1d16c70, Place 0x1d16880 |
| `RuneGolem` (summon) | elementals/runegolem/runegolem | `:113918` consts: RiseTime 0.7, RoarAt 2.05, SummonLength 2.9, AuraRadius 8, AuraGap 1.5, FistCooldown 1.6, PoundCooldown 7, QuakeGap 12, CrumbleTime 2.4, FxPath `GameAssets/characters/elementals/runeGolem/effects/` ... | - | Init, Rise, Fist, Quake, Crumble, Loop, Once (`dump.cs:113988-114046`) |
Pages: each a `api.part(<script>, ...)` reading its fields from the comp (node references are `{node: i}`); the holder of a
Bind is the hero (the page's only character: the effect's root at her). The Rune Golem: as part 9's summons (Rise 0.7 s, the
roar at 2.05, `root` from 2.9 s, cut 10), its effects spawned by name from its own folder (`runeGolem_rise`, `_riseBurst`,
`_roar`; T1's addressing).

### T6. Already built for these prefabs

GroundHugEmitter (22 nodes), ImageEmitter / LineEmitter / RingEmitter / EffectControl in TTO's BB shape, StaticMesh,
SkinnedMeshRenderer, Light, AudioControl, `Particles/Standard Unlit` (11, tto_sheep.js), `FlexibleCelShader/Cel No Outline`
(tto_BuitenHouHou, tto_ja: tto_penguin.js), add / addsoft / alpha / premul / multiply / multiply2; Shuriken Initial, Shape,
Emission, Size, Color, Rotation, Force, Velocity, ClampVelocity, InheritVelocity, UV, SizeBySpeed, Collision (world, the
floor). `Legacy Shaders/Transparent/Diffuse` is only on TTO's volcanicEruption copy (not drawn: BB's is).

## Interfaces (fixed up front, so the builders run in parallel)

1. **Shot mover** (monkey.js, part 1): if the Mole build's `fxparts/mole.js` exports its shell stepper (`shellStep` / the
   body + floor contact), import it (`import { ... } from "./mole.js"`); else monkey.js keeps its own ~40 lines with the same
   body box (Bat decision 4). `cat.js`'s `lookEuler` is exported (`cat.js:44`).
2. **`PROP_STARTER.monkey = { R: "noviceMike" }`** (lead, index.html:5007): mikeBlink's fallback when nothing is worn.
3. **The clip timeline** (elementals.js): cue option `clips: [[age, clip, fade, wrap], ...]` read by the summons' and the
   armours' parts; option `attach: [[effect, bone], ...]` (spawned with `followNode` = this Fx's node of that name).
4. **Data names** (lead's extractor, used by elementals.js and the cues): `Phoenix4`, `Ja4`, `Gadina4`, `Buiten4`, `Gaos`
   (EXTRA_FOLDERS), `phoenix_summon_ring`, `ja_summon_ring`, `gaos_summon_ring`, `buiten_summonEffect`,
   `gadina_summonEffect`, `gadina_sword4`, `gadina_shield4` (FIELD_PREFABS / ALIASES); TTO `tto/<prefab>` as before, the
   golem's `tto/runeGolem` and `tto/runeGolem_<x>`.
5. **TTO clips in the data** (T1): an Animation component of a TTO effect carries `clips` in BB's shape, so mesh.js's
   Animation part plays them unchanged.
6. **Shuriken** (T3): `SubModule` reads `subEmitters[].emitter.node` (an index into the same effect's nodes); the child's
   system is built idle (no own play) and exposes `emitAt(position, n)` for the parent.
7. **Unchanged, used:** `api.spawn` + `followNode` / `local`, the entry's `builds`, `api.propModel`, the `hideProp` kind,
   `fxAnim.play(name, fade, wrap)`, the cue's `kill`, `rot`, `d`, `y`, `to`.

## Rank by value (effects made right / effort)

| rank | part | Monkey effects | other classes | work |
|---|---|---|---|---|
| 1 | LAYOUTS (Monkey + summons) | fireBall1-4, runicFlame / Sand (+ rings) extract | - | 1 block |
| 2 | shot movers (part 1) | Fireball, Earth Pulse + hits | (Mole's mover shared) | ~40 lines |
| 3 | Monkey_lavu + FX/Lavu | Lavu, Upheaval with Lavu | - | ~60 + 1 lines |
| 4 | summons + armours (parts 8-9) + container fix / FIELD_PREFABS / EXTRA_FOLDERS | five summon skills, Fire Avatar, Earth Form | Penguin / Mole style | ~60 lines + extractor |
| 5 | Shuriken graft line | volcanicEruption | - | 1 line |
| 6 | Rotate | the two runic rings | any `Rotate` user | ~8 lines |
| 7 | fx:mikeBlink | Mike Blink | - | ~15 lines |
| 8 | TTO legacy clips + addressing + root fix (T1) | solarCrown, sunAvatar_comet, the offering's idol, the Rune Golem | every TTO Animation | ~40 lines (pipeline) |
| 9 | Eric/URP Particles shaders (T2) | 36 TTO materials (all four skills) | any TTO Hovl effect | ~30 lines |
| 10 | TTO scripts (T5) | Buiten Bastion, Solar Call, the golem's quake | - | ~150 lines |
| 11 | Shuriken Sub / Noise / Lights (T3) | buitenBastion_rise, the golem's bursts, the pillar | all classes' TTO | ~50 lines |
| 12 | Animator FX_Magic_Circle (T4) | three Sigils | - | probe first |

After all, `BUILT` in `pipeline/wardrobe_fx_inventory.py` += `Monkey_fireBall`, `Monkey_earthPulse`, `Monkey_lavu`,
`Monkey_runicFlame`, `Monkey_runicSand` (data only), `Rotate`; NOTES for volcanicEruption's grafted systems; run it again.

## Who builds what (never two owners for one file; as `plans/fx_wolf/build_rules.md`)

| agent | owns | builds |
|---|---|---|
| A: monkey | `wardrobe/fxparts/monkey.js` (new), `wardrobe/fxparts/rotationcontrol.js` (the Mole's, + `Rotate`), `wardrobe/fxparts/mesh.js` (one line) | parts 1, 2, 3 (Rotate), 6, 7 |
| B: elementals | `wardrobe/fxparts/elementals.js` (new) | parts 8, 9 (and the Rune Golem's summon clips by the same timeline, T5's last row) |
| C: tto_monkey | `wardrobe/fxparts/tto_monkey.js` (new), `wardrobe/fxparts/shuriken.js` | T2, T3, T4 (page side), T5 |
| D: page_pipeline | `wardrobe/index.html`, `pipeline/wardrobe_fx.py`, `pipeline/wardrobe_fx_tto.py`, `pipeline/wardrobe_fx_inventory.py` | LAYOUTS, the container fix, EXTRA_FOLDERS / FIELD_PREFABS / ALIASES / SOUND_REFS / SOUND_ALIASES, `SHURIKEN_FROM_TTO.monkey`; T1 (clips, addressing, root, `SKILL_FX.monkey`); `PROP_STARTER.monkey`; `FX_PART_FILES += "monkey", "elementals", "tto_monkey"`; `BUILT`; the rebuild and the cues (the editor's) |

Rules as before: `node --check`, no browser for the builders, never `wardrobe_fx.py monkey` / `wardrobe_fx_tto.py monkey`
without `--probe` (D rebuilds once). The Mole build must be finished first (it owns `rotationcontrol.js`, `wardrobe_fx.py`,
`index.html` now); A edits `rotationcontrol.js` only after it exists. After editing `wardrobe/index.html`, `grep -c $'\r$'
wardrobe/index.html` must print 0.

## Paste-ready cue fragments (the parts' shapes; the clip researchers' entries win where they differ)

Keys as the earlier cue files (`"<clip>" | "@Skill:clip": {"why", "cues"[, "builds"]}`); valid JSON. The Lavu timeline is
read from `clip_flow.js Monkey.cs RPC_lavu_cast` (case 0: clip `cast3` (`:34785`), voice `lavu` (`:34815`, `:34864`),
`Yield(2, 0.3)` (`:34862`); case 2 at 0.3: `castEffect_fire` at hero + `TransformDirection(0, 1, 1)`, hero rotation
(`:34510`), an old summon unsummoned (`:34523`); `Yield(3, 0.1)` (`:34858`); case 3 at 0.4: `RPC_lavu_summon` at hero +
`TransformDirection(0, -2, 3)` (`:34550-34561`), the `lavu` status `chaAdjust(60)` (`:34590`), `lavu_ring` at hero + 3
forward, identity (`:34612-34624`), the sound `lavu_summon` (`:34644-34656`); `Yield(4, 0.2)` (`:34848`); case 4 at 0.6:
standby (`:34715`)); its key (the Lavu tile; `cast3` is a pool clip) is the skills researcher's.

```json
  "@Lavu:cast3": {
    "why": "Monkey.cs $RPC_lavu_cast (:34445-34870): cast3 and voice lavu at 0 (:34785, :34815 / :34864); 0.3 castEffect_fire at hero + TransformDirection(0, 1, 1), hero rotation (:34510); 0.4 RPC_lavu_summon (:34550-34561 -> :13876-13915): the lavu serpent at hero + (0, -2, 3), LookRotation(forward) x Euler(-90, 0, 0) (:13899), Monkey_lavu.summon: 10 m/s up for 2 s, then standby round the Monkey's head + 4 m (Monkey_lavu.cs:333-466, :42-58; parts.md part 2); the lavu status chaAdjust(60) s (:34590), cut at 10; lavu_ring at hero + 3 forward, identity (:34612-34624); the sound lavu_summon (Elementals/Lavu/Sounds, :34644-34656)",
    "cues": [
    [0, "voice", "lavu"],
    [0.3, "fx", "castEffect_fire", {"y": 1, "d": 1}],
    [0.4, "fx", "lavu", {"y": -2, "d": 3, "rot": [-90, 0, 0], "kill": 9.6}],
    [0.4, "fx", "lavu_ring", {"d": 3}],
    [0.4, "sound", "lavu_summon"]
    ]
  },
  "@SummonPhoenix:cast3": {
    "why": "shape only (the times and the spawn point are the skills researcher's): RPC_phoenix_create (Monkey.cs:11340-11740): with Fire Soul #422 fireSoul_ring at the hero (:11360-11372); Phoenix4 (max rank) at mPos, LookRotation(tDir) (:11380-11420); Phoenix.summon (Phoenix.cs:4297-4313): its summon clip and its summon_ring at its position, identity, then root (parts.md part 9); cut at 10",
    "builds": ["phoenix_summon_ring"],
    "cues": [
    [0.4, "fx", "fireSoul_ring"],
    [0.4, "fx", "Phoenix4", {"d": 3, "kill": 9.6, "clips": [[0, "summon"], [1, "root", 0.2, 2]]}]
    ]
  }
```

(`lavu`'s `kill` 9.6 = 10 - 0.4: the 10 s rule from the tile's start; the `d` 3 of `Phoenix4` is a placeholder for `mPos`.)
The other part-carrying cues, shapes only:
- Fireball: `[t, "fx", "fireBall4", {"y": Y, "d": D, "rot": [pitch, yaw, 0]}]`, `"builds": ["fireBall_hit"]`; Earth Pulse the
  same with `earthPulse`, `"builds": ["earthPulse_hit"]` (aimed at the 10 m point: Bat decision 1).
- Runic Flame / Sand: `[t, "fx", "runicFlame_ring", {"kill": K}]` (on the Monkey), and each segment `[t, "fx", "runicFlame",
  {"d": D, "kill": K}]`.
- Mike Blink: `[t, "fx", "mikeBlink", {"d": 10, "rot": [270, 90, 0]}]` + `[t, "hideProp", "R", {"kill": 1.1}]`.
- HP Transfer with Mike Circle: `[t, "fx", "hpTransfer", {"y": 0.82, "d": 0.88, "to": [0, 0.6, 9.4], "kill": K}]`,
  `[t, "fx", "mikeCircle", {"y": 0.45, "d": 10, "rot": [270, 90, 0], "kill": K}]` (`Monkey.cs:21027`, `:21067`, `:21179-21181`).
- Fire Avatar: `[t, "fx", "phoenixArmor_create"]`, `[t, "fx", "phoenixArmor", {"clips": [[0, "summon"], [1, "root", 0.2,
  2]], "kill": K}]`; Earth Form the same with `gadinaArmor` (`summon` 0.8).
- Gadina: `[t, "fx", "Gadina4", {"d": D, "kill": K, "attach": [["gadina_sword4", "mount_Hand_R"], ["gadina_shield4",
  "mount_Hand_L"]]}]`, `"builds": ["gadina_summonEffect", "gadina_sword4", "gadina_shield4"]`.
- Volcanic Eruption: `[t, "fx", "volcanicEruption", {"d": D, "kill": 10}]`.

## How sure I am

| item | sure | why |
|---|---|---|
| The Monkey layouts (4 / 24 / 24 / 16 bytes) | high | public fields in order, byte sums exact, values decoded (mLv 1-4; Rotate (0, 0, 180) / (0, 0, 120)) |
| The summons' layouts | high | `refs.txt`: all five decode exactly with these, references resolve to the named objects |
| Rotate's semantics | medium-high | Reborn's source of the same firstpass script; BB's not decompiled |
| The shots (30 / 15 m/s, no gravity, lives 2 / 3) | high | literals and the Rigidbody flags |
| Monkey_lavu's flight | high | the coroutines and Update read whole; the spawn line plain |
| Lavu cast timing (0 / 0.3 / 0.4 / 0.6) | medium | clip_flow order of the flattened cases; the skills researcher confirms |
| FX/Lavu = FX/Phoenix | high | the two shader files side by side |
| The graft's match | high | BB and TTO materials one to one |
| The summon clip defaults | medium | each summon coroutine's Play line; the waits per summon are the skills researchers' |
| TTO URP shader math | medium | pass state read; the fragment from the property set (programs not decompressed) |
| TTO scripts' behaviour | low | fields and RVAs only; bodies to disassemble |
| TTO clips readable as BB's | high | `tto_clips.txt` (legacy, plain curves) |

## Open questions (each with my recommended answer)

1. **The summons: show them?** Recommended: **yes**, standing models with their summon clip then `root`, cut at 10 s, no AI
   (Mole decision 32, the Penguin's Mana Vortex); Gadina with sword4 / shield4 (passives on: Titan Sword 3, Aegis 3).
2. **Lavu after the summon flight**: standby loops round her head at 8 m/s, well above the default camera. Recommended: keep
   the game's flight (the camera fit is the editor's), cut at 10 s.
3. **Upheaval with Lavu**: the tile needs Lavu present. Recommended: the Upheaval tile spawns `lavu` with `"lavu":
   "upheaval"` (already circling at r 6, the slerp-in first 3 s as the code), the effect-only precondition shown, as the
   Mole's Detonate needs a nuke.
4. **Mike Blink's distance**: the game blinks only past 12 m (Bible 4.12). Recommended: the standard 10 m target (the
   standing rule), noted in the why.
5. **HP Transfer's target is an ally** (or her summon), not an enemy. Recommended: the same 10 m point (one target on the
   page), the bolt to its chest less `2 x extents.x` = 0.6 m.
6. **The summons' commanded moves** (Phoenix's fireballs, Gadina's attacks, Gaos' rampage, Summon Attack / Defense /
   Release). Recommended: the summon tiles show the summon only; Summon Attack etc. as effect-only tiles on the idle stance
   with the summon standing (no AI), offered to the user as a separate job for the moves (the Mole's Barrel Bot AI call).
7. **The Rune Golem** (released TTO `golemCall`): build it. Recommended: **yes** (missing parts are always built, the skill
   is released): T1's three extractor fixes, then part 9's timeline with RuneGolem's Rise (0.7 s) / roar (2.05 s) / root
   (2.9 s), cut 10.
8. **`FX_Magic_Circle`** (Mecanim). Recommended: probe its clip first; if it only spins / scales the Sigil, export it as a
   legacy-shaped clip (small); else build the muscle-clip reader in `wardrobe_fx_tto.py` (the rule says build).
9. **Shuriken Noise / Lights**. Recommended: Sub **yes** (whole bursts depend on it); Noise as a cheap value-noise drift
   (APPROX); Lights through api.pointLight (two pooled: the brightest system only, APPROX).
10. **The armours' attack clips** (Fire Avatar / Earth Form attacks play `nAttack*` / `cAttack*` / `blazingForm*` on them).
    Recommended: the attack tiles in the form cue the armour with its `clips` timeline matching the hero's clip (the skills
    researchers' times).

## Offers for the Bible (never written there)

Read this first 6 (volcanicSoul_ring missing; Runic life through tID; Mike Blink moves the worn weapon; Gadina's sword /
shield by the passives' ranks; the armours live only in the form). Also: the Monkey's Lavu skill uses an effect prefab
(`Effects/lavu`, `Monkey_lavu`), not the elemental `Lavu` character, whose own script and attacks (`Lavu.cs:805`, `:869`)
the Bible cites for Lavu's damage: worth a check of which object deals Lavu's hits.

## Per-effect status (`plans/fx_inventory.md` "### monkey", unchanged by this research)

42 of 51 ready; not ready: `earthPulse` (Monkey_earthPulse), `fireBall1`-`4` (Monkey_fireBall), `lavu` (Monkey_lavu,
rotationControl), `runicFlame` (Monkey_runicFlame), `runicSand` (Monkey_runicSand), `volcanicEruption` (ParticleSystem,
ParticleSystemRenderer). Not listed there (this report): the 14 of Read this first 4 (`runicFlame_ring` / `runicSand_ring`
need `Rotate`), `mikeBlink` / the armours (ready by the inventory, but the hero's code acts on them: parts 6, 8), the five
summons, every TTO prefab.

## Verification (2026-11-13, checker)

Read-only re-derivation on the office PC (BB `DecompiledSource/*.cs`, BB's rip `RippedAssets/.../Resources/gameassets`,
TTO1102 `pseudo/Monkey.c`, TTO's 2026-11-09 bundles through `wardrobe_fx_tto.effect()`, the working tree's page and
parts). Probes in `checks/fx_monkey_research/verify/` (git-ignored; tto.md's Verification lists them: `probe_v.json`,
`catalog.txt`, `clips_v.py`, `golem_audio.py`, `mats_v.py`, `mats_v2.txt`, `shader_v.py`). This section wins over the body.

**Confirmed** (no change): 65 prefabs in BB's `heroes/monkey/effects` (the rip folder); the shots' local velocities
(0, 0, 30) / (0, 0, 15) (Monkey_fireBall.cs:26, Monkey_earthPulse.cs:26) and lives `2 x rangeMod` / 3 (Monkey.cs:11278,
:13113); the Lavu cast's timeline (Monkey.cs $RPC_lavu_cast: `PlayAnimation("cast3", 0.2f)` and the `lavu` voice at 0,
`Yield(2, 0.3)`, castEffect_fire at hero + TransformDirection(0, 1, 1), `Yield(3, 0.1)`, the summon at hero +
TransformDirection(0, -2, 3), the `lavu` status `chaAdjust(60)`, `lavu_ring` at hero + 3 forward, identity, the sound
`Elementals/Lavu/Sounds/lavu_summon` (in the rip: `characters/elementals/lavu/sounds/lavu_summon.wav`), `Yield(4, 0.2)`:
0 / 0.3 / 0.4 / 0.6, so "medium" -> high); `fireSoul_ring` is loaded from `Heroes/Monkey/Effects` (Monkey.cs:11360-11372,
in the rip); slot R's bone is `mount_Summon` (`wardrobe/data/placements.json` weapons.monkey.fallback.bone); item_map's
`w_mnk1` is `noviceMike`; the TTO pass state of T2 (`shader_v.py`: Additive src One, dst `[_Blend2]`, ZWrite Off, Cull
`[_CullMode]`, ColorMask RGB; Alpha Blended SrcAlpha OneMinusSrcAlpha, ZWrite Off; tto.md P2's `_SrcBlend` reading is
the wrong one, tto.md Verification 4); `MonkeyRow6Rise` x 6 on `runeGolem_quake` (`probe_v.json`); the paste fragment is
valid JSON (2 keys, 7 cues). Not re-probed: the LAYOUTS' bytes (`refs.txt`), the container dupes (`dupes.py`), the
Shuriken modules of T3, the physics boxes.

1. **T1's legacy-clip item is already built.** What is wrong: "today every TTO Animation's clips are written by name
   only". The working tree's exporter writes them (`animation()`, pipeline/wardrobe_fx_tto.py:707-753, the Mole build,
   Mole decision 56): `clips_v.py` gives the comet's / crown's `Ja` root 1.2 (Loop), run 1.0, ko 1.2, summon 1.2, unsummon
   1.2, suicideRun 1.0, and RuneGolem's root 5.3, run 1.2, attack1 1.0, attack2 1.0, attack3 1.3333, summon 2.9, quake 1.6,
   collapse 2.0, no lost paths. Rank 8 shrinks to the addressing and SKILL_FX (item 3).
2. **T1's root `KeyError: 'm_Component'` does not reproduce** on the 2026-11-09 bundles: the AssetBundle container maps
   `runegolem` to its GameObject only, and `effect()` exports it (24 nodes: Animation, CharacterController,
   CharacterControl, AudioSource with no clip, RuneGolem, SkinnedMeshRenderer; `probe_v.json`, `golem_audio.py`). The
   "take the GameObject" guard costs one line and may stay; it is not a blocker.
3. **T1's addressing misses two folders.** The boosted summons' auras live in `gameassets/characters/elementals/ja/effects`
   (`jaascension_aura`) and `.../buiten/effects` (`buitenbastion_aura`) (`catalog.txt`), so the per-class list is
   `"monkey": [".../elementals/ja/effects", ".../elementals/buiten/effects", ".../elementals/runegolem",
   ".../elementals/runegolem/effects"]` (tto.md P1). The golem folder holds 13 effects = tto.md's 12 + `runeFracture`
   (the quake's status look on the foe: built in SKILL_FX, never cued, Cat decision 44, Chameleon 53, Mole 52).
4. **Parts missing from this report (tto.md's), and their owners.** P5 `Monkey.SunComet` and P7 `Monkey.SolarCollapse`
   (code movers on `sunAvatar_comet` / `sunAvatar_dive`: CODE_MOVERS in wardrobe_fx_tto.py, the movers in tto_monkey.js);
   P8 the boosted summons (cue options `boost` 2: the Ja at level 6 with `tto/jaAscension_aura` parented at its root, the
   Buiten x 1.2 with `tto/buitenBastion_aura` parented unscaled; `standing`: spawned already summoned in `root`, no ring;
   tto.md 2.1, 2.3, section 6); P10 TTO's own hero voice `voices/buiten` (BB's rip has `buiten.wav.meta` only; TTO's
   catalog has `heroes/monkey/voices/buiten`; `tto_clips` reads `sounds/` only, wardrobe_fx_tto.py:395-421). Ownership
   (adds to "Who builds what"): C tto_monkey.js P5, P7 (beside P6 = T5's SunCrownFx); B elementals.js P8 (it owns the Ja4 /
   Buiten4 part); D CODE_MOVERS, P10 in wardrobe_fx_tto.py.
5. **The Rune Golem runs its AI (T5's last row and B's "the Rune Golem's summon clips" overruled).** What is wrong: T5 and
   the ownership table give the golem part 9's summon-only timeline ("Rise 0.7 s, the roar at 2.05, root from 2.9 s, cut
   10"). Decided as tto.md Q7: the AI as the code on the 10 m target (walk, fist, quake, pound; the aura pulse every 1.5 s
   from 0.7 with `tto/stoneAegis` on the hero; the glow; `MonkeyRow6Rise` in the quake), its end the game's CrumbleAway at
   10 s (`end`). Reason: Bat decision 24 (the guardian's AI as the code), Mole decision 32 (the Auto Gyro Gun's AI fires at
   the 10 m target); the skill is released and its whole look is the golem's moves. Owner: C (tto_monkey.js, tto.md's
   "P2-P7, P9"), not B. Its spawns are the entry's `builds` (tto.md's block).
6. **The summons end with the game's unsummon at 10 s after the spawn, not a `kill`.** What is wrong: part 9's "cut at 10 s"
   and the fragments' `"kill": 9.6` (= 10 - 0.4, counted from the tile's start). Decided as Bat decision 25 (the
   guardian's own unsummon 10 s after the summon) and tto.md's `"end": 10` for the same Ja4 / Buiten4 parts: option `end`
   (seconds after the spawn) plays each summon's unsummon coroutine: Phoenix `ko`, Destroy 1 s later (Phoenix.cs:5264,
   :5306); Ja `ko`, 1 s (Ja.cs:2219, $unsummon$18387); Gadina `unSummon` + `summonEffect` at its position, identity, then
   its waits (Gadina.cs:6717-6804: the builder reads the order); Buiten `unSummon` + `summonEffect`, Destroy 1 s
   (Buiten.cs:974-1016); Gaos `unsummon` + `unsummon_ring`, Destroy 1.5 s (Gaos.cs:5106-5164). Lavu: its own `unsummon`
   option (part 2: the 1 s fade, Monkey_lavu.cs:819-867) at 10, `kill` 11. Builds gain the unsummon looks
   (`gadina_summonEffect`, `buiten_summonEffect`, `gaos_unsummon_ring` as ALIASES). (The Mole's robots, cut by `kill`,
   have no unsummon of their own to show.)
7. **Interfaces 3's new `clips` option duplicates two the page has.** The Cat's `anims` (`[[seconds after the spawn,
   clip], ...]`, index.html:4717-4718, cat.js:114-135) is the hero's code playing clips on an effect's Animation, and the
   Mole's `clip` (the summon plays that clip once, then root, index.html:4755-4756) is the robots' one-off. Decided:
   reuse. The summons' parts carry their own default timeline in the robots.js shape (one `api.part` per summon script,
   `run(node, [[t, fn], ...])`, robots.js:48-52: summon / create, then root with the coroutine's wait, the ring spawned
   at 0); the armours (part 8) take `anims` with an optional third and fourth item (fade, wrap), defaults 0.2 / Loop for
   `root` and 0 / Once otherwise. No `clips` option.
8. **Interfaces 4: `tto/RuneGolem`**, not `tto/runeGolem` (tto.md's cue, the game's prefab name in
   `RPC_runeGolem_create`'s 'GameAssets/characters/elementals/runeGolem/RuneGolem'; matches Ja4 / Buiten4's casing).
9. **Interfaces 1:** `fxparts/mole.js` now exists and exports only `mortarVector` (mole.js:40), a gravity arc, no straight
   stepper: monkey.js keeps its own ~40 lines (the report's fallback). **Interfaces 2:** `PROP_STARTER` is at
   index.html:5165 (`{ chameleon: { R: "noviceBow", L: "noviceArrow" } }`); add `monkey: { R: "noviceMike" }` there.
10. **T2's numbers.** 39 Additive + 2 Alpha Blended materials over the 28 TTO prefabs in scope (`probe_v.json`, unique per
    folder), not 35 / 1; and the speeds are not 0 everywhere: `tto_Trail_01_1_h7s10` / `_h11s10` scroll V at -0.8 /s
    (`_SpeedMainTexUVNoiseZW` (0, -0.8, 0, 0), `mats_v2.txt`): the shader part reads that vector (uv += speed.xy x t).
    `_Emission` varies 1-3 (Additive) and 4 (Alpha Blended); `_Blend2` 1 on every Additive material. The `_SrcBlend` /
    `_DstBlend` / `_ZWrite` some materials save are stale (the shader declares none of them): ignore them.
11. **T4 / question 8 decided: build the Sigil scroll.** tto.md section 5 already read FX_Magic_Circle's one clip
    (`animator.py`): a 2 s loop animating the Sigil's ParticleSystemRenderer material `_MainTex_ST` with x, y, z constant
    (1, 1, 0) and w (the V offset) 0 -> -1. The exporter writes that curve on the Animator comp (`{"type": "Animator",
    "uv": {"len": 2, "w": [[0, 0], [2, -1]]}}`, read from the controller's clip; the streamed-curve reader is only needed
    for this one binding), and tto_monkey.js scrolls the Sigil's own material copy's map offset y (uvscroll.js's
    `ownMats` pattern; Unity's and three's offsets share the sense, uvscroll.js:13-15). Three Sigils:
    jaAscension_callFx, runeGolem_circle, jaAscension_aura (and the unreleased buitenBastion_offering).
12. **The paste fragment's keys are dead without SEQ lines.** `@Lavu:cast3` / `@SummonPhoenix:cast3` are tried only when
    a sequence named "Lavu" / "Summon Phoenix" plays cast3 (index.html:4700-4703, `own` in poolChains :1423); index.html's
    Monkey SEQ has neither (:1296-1297). As cast3 pool members on the Cast host instead, each tile would end with cast3
    (1.0 s) and a loop would restart the summon every round. Decided as tto.md's S1 (a root hold through the summon's
    end): two SEQ lines and SEQ_SKILL entries (their own icon, as the Bat's Nightmare), and the skills researcher's cast3
    pool must not list `lavu` / `phoenix` as members too. Corrected fragment below (spawn time 0.4 and `d` 3 of the
    Phoenix still the skills researcher's placeholders).

Corrected fragment (replaces the body's; keys as the earlier cue files):

```json
  "@Lavu:cast3": {
    "why": "Monkey.cs $RPC_lavu_cast (:34445-34870): cast3 with a 0.2 s fade and voice lavu at 0 (:34785, :34815 / :34864); 0.3 castEffect_fire at hero + TransformDirection(0, 1, 1), hero rotation (:34510); 0.4 RPC_lavu_summon (:34550-34561 -> :13876-13915): the lavu serpent at hero + (0, -2, 3), LookRotation(forward) x Euler(-90, 0, 0) (:13899), Monkey_lavu.summon: 10 m/s up for 2 s, then standby round the Monkey's head + 4 m (Monkey_lavu.cs:333-466, :42-58; parts.md part 2); the lavu status chaAdjust(60) s (:34590) cut at 10 s after the summon by its own unsummon (Monkey_lavu.cs:886-930: the 1 s fade, Destroy at 1 s; Bat decision 25; parts.md Verification 6); lavu_ring at hero + 3 forward, identity (:34612-34624); the sound lavu_summon (Elementals/Lavu/Sounds, :34644-34656)",
    "cues": [
    [0, "voice", "lavu"],
    [0.3, "fx", "castEffect_fire", {"y": 1, "d": 1}],
    [0.4, "fx", "lavu", {"y": -2, "d": 3, "rot": [-90, 0, 0], "unsummon": 10, "kill": 11}],
    [0.4, "fx", "lavu_ring", {"d": 3}],
    [0.4, "sound", "lavu_summon"]
    ]
  },
  "@SummonPhoenix:cast3": {
    "why": "shape only (the times and the spawn point are the skills researcher's): RPC_phoenix_create (Monkey.cs:11340-11740): with Fire Soul #422 fireSoul_ring at the hero (:11360-11372); Phoenix4 (max rank) at mPos, LookRotation(tDir) (:11380-11420); Phoenix.summon (Phoenix.cs:4297-4313): its summon clip and its summon_ring at its position, identity, then root after 1 s (the part's own timeline, parts.md Verification 7); its unsummon 10 s after the spawn (end: ko, gone 1 s later, Phoenix.cs:5264-5306; Bat decision 25)",
    "builds": ["phoenix_summon_ring"],
    "cues": [
    [0.4, "fx", "fireSoul_ring"],
    [0.4, "fx", "Phoenix4", {"d": 3, "end": 10}]
    ]
  }
```

SEQ lines (index.html SEQ monkey; cast3 1.0 s, so the root hold = 0.4 + 10 + 1 - 1.0 = 10.4) and SEQ_SKILL:

```
"Lavu: cast1 cast2*~@0 cast3~ root*~@10.4", "Summon Phoenix: cast1 cast2*~@0 cast3~ root*~@10.4"
monkey: { "@Lavu": "lavu", "@SummonPhoenix": "phoenix" }
```

(The bar `@0` follows the page's Monkey Cast line; the skills researcher's 0.1 s floor, tto.md Q5 / Mole decision 6,
moves all of them together.) The other part-carrying cue shapes stand, with `end` in place of `kill` on every summon
(Gadina4 `{"d": D, "end": 10, "attach": [...]}`) and the armours' `clips` written `anims`
(`{"anims": [[0, "summon"], [1, "root", 0.2, 2]], "kill": K}`).
