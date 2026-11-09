# The Wolf's effect parts as built (2026-11-09, commit 2c3408b): notes for the cue editor

Summarised by the lead from the seven builders' reports (agents A-G, `build_rules.md`). Inventory now: 67 of the Wolf's
69 own effects ready (`plans/fx_inventory.md`); the two left (`crusader_hit`, `lawbringer_hit`, a Light) land on the
target and stay out anyway.

## BB parts (fxparts/vortex, emblem, trail, control, mesh)

- **VortexEmitter** (vortex.js): `darkEdge_ring` (6-arm spiral at the feet, rises, gone ~0.63 s), `dualBrand_slash3`.
  BB targets 80 fps; `?vortexfps=60` compares.
- **EmblemEmitter** (emblem.js): `holyArmor_ring` (Delay 0.2), `holySword_ring` (0.4), `resurrection_ring` (0.9),
  `valor_emblem` (Delay 0): a flat picture ~2.5 m above the hero, drawn over everything, fixed screen size (shrinks past
  5 m, gone at 40 m). `resurrection_hit` is on the target: out.
- **TrailEmitter / TrailRenderer** (trail.js): `dualBrand_slash1/2/4` (wide ribbons), `crusader` / `lawBringer` slashes
  (thin camera-facing streaks; TrailRenderer approximated, no source). Possible colour swap between Crusader (white to
  blue as read) and Law Bringer (white to gold): flag it for the user.
- **EmitterControl / child EffectControl** (control.js): `artBreaker_ring` (dust ~2 m ahead at 1.0 s, gone 2.0 s),
  `cAttack2` and `skySlasher` (their foot dust is destroyed on frame 2, as in the game: correct to see nothing),
  `dualBrand_slash3` (its vortex shoots FORWARD at 12 m/s, not up: corrects parts.md).
- **Meshes** (mesh.js, wardrobe_fx_mesh.py): `bladeFang_underSlash` / `bladeFang_upperSlash` and `bloodFang_underSlash` /
  `bloodFang_upperSlash` (skinned blades; spawned at the hero's rotation x Euler(270, 90, 0): cue option
  `{"rot": [270, 90, 0]}`), `mirrorBlade_mirror` (StaticMesh + ShatterMesh: a pane 1.25 m ahead from 0, shatters at
  1.2 s, gone 1.8 s; the game's DistortGlass is approximated as a multiply), the Animation half of `crusader`,
  `lawBringer`, `dualBrand_slash1/2/4`.
- Blood Fang is on (decisions.md): Blade Fang's slashes are the `bloodFang_*` ones, at the times and rotations the
  research reports give (attacks.md, counters.md "future lines").

## TTO parts (fxparts/groundhug, arcribbon, groundfollower, shuriken; pipeline/wardrobe_fx_tto.py)

- Built TTO effects (in `data/wolf/fx.json`, cue them by these names): Blade Surge `tto/bladeSurge_aura`, `_zone`,
  `_cut`, `_flicker`, `_sheathe`, `_shatter`, `_shards`; Resonance Claw `tto/resonanceClaw_charge`, `_rake`,
  `_wave_twin`, `_wave_light`, `_wave_dark` (`_burst` is on a hit target: out); Wind Bound Domain
  `tto/windBoundDomain_cast`, `_plant`, `_domain`, `_pulse` (`tto/windBound` is an enemy status: out).
- Timelines, positions, rolls / yaws: `tto.md` section 4 (and 5: the options Blade Surge needs: y, rot, scale, kill
  are now in the cue format; random line scatter is not: approximate with a few fixed placements or leave out, note it).
- TTO's effects carry their own AudioSources (the page plays them), so the sound-only stand-in cues added earlier for
  the TTO skills must be dropped where the effect now plays that sound (else it plays twice). `iceBreak` and
  `shatteringDream_hit` are now in data/wolf/sfx.
- Rebuild the TTO effects after editing their cues: `uv run --no-project --with UnityPy --with pillow --with
  imageio-ffmpeg python -I pipeline/wardrobe_fx_tto.py wolf` (home PC only: it reads the video folder's tto_assets).
