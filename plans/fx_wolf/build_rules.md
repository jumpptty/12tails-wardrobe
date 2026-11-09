# Building the Wolf's missing effect parts: shared rules (2026-11-09)

The user: "make the effects we can't draw work including TTO skills effects" ... "I meant every missing effect from Wolf
hero along". Seven agents build in parallel, each in files it alone owns; then one editor adds the newly drawable effects
to `wardrobe/fx_cues/wolf.json`. Read `plans/fx_wolf/parts.md` (what each BB part does, file:line, the Wolf's values)
and `plans/fx_wolf/tto.md` (TTO's three skills) first.

## Who owns what (never edit anything else)

| Agent | Files it owns |
|---|---|
| A vortex + emblem | `wardrobe/fxparts/vortex.js`, `wardrobe/fxparts/emblem.js` |
| B trails | `wardrobe/fxparts/trail.js` (TrailEmitter + Unity's TrailRenderer) |
| C meshes | `pipeline/wardrobe_fx_mesh.py`, `wardrobe/fxparts/mesh.js` (StaticMesh, Animation, SkinnedMeshRenderer, ShatterMesh) |
| D control | `wardrobe/fxparts/control.js` (EmitterControl, EffectControl below the root) |
| E TTO reader | `pipeline/wardrobe_fx_tto.py` (new) |
| F TTO emitters | `wardrobe/fxparts/groundhug.js`, `arcribbon.js`, `groundfollower.js` |
| G Shuriken | `wardrobe/fxparts/shuriken.js` (Unity's ParticleSystem + ParticleSystemRenderer) |

Shared files (`wardrobe/index.html`, `pipeline/wardrobe_fx.py`, `wardrobe_fx_check.py`, `wardrobe/fx_cues/*`, NOTES,
HANDOFF, the reports) are the lead's: if your part needs a change there, describe it exactly in your report instead.

## The interfaces (already in place, commit after 9b87ddf)

- **Page parts:** the comment above `FX_PART_FILES` in `wardrobe/index.html`. A module default-exports
  `register(api)` and calls `api.part(type, build)`; `build(fx, node, comp, mat, nodeDef, data)` returns
  `{ node, update(dt, cam), stop?() }` (see `ringEmitter` / `imageEmitter` / `lineEmitter` / `legacyParticles` in
  index.html for working examples: Unity-space numbers inside the mirror group, `fxMesh` + `setMesh` for geometry,
  `fxMaterial` for the game's particle shaders, `ramp(e, u)` for the 5-colour ramps). `api` has THREE, V, vA, nz, rnd,
  clamp01, ramp, fxMesh, setMesh, fxMaterial, hermite, texLoader, camera, renderer, scene, Sound, FX, DATA, hero().
  `cam` in update = the camera's right / up / fwd in Unity space. Pure ES module, no imports (THREE comes from api).
- **BB extraction:** `pipeline/wardrobe_fx.py` decodes VortexEmitter, EmblemEmitter (+ `imageTex`: its picture,
  exported to data/fx/tex), TrailEmitter, EmitterControl, ShatterMesh (LAYOUTS, field names as in parts.md); dumps
  TrailRenderer and Light typetrees (+ `mats`); hands MeshFilter / SkinnedMeshRenderer / Animation to
  `pipeline/wardrobe_fx_mesh.py`'s `component()` (agent C). See what a prefab gives with the read-only probe:
  `uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py wolf --probe name1,name2`
- **TTO effects:** named `tto/<prefab>` in cues and in `data/wolf/fx.json` (the BB build skips them); materials and
  textures prefixed `tto_` to never collide with BB's. Agent E writes them in the same JSON shape as wardrobe_fx.py
  (effects {nodes: [{name, parent, pos, rot, scale, comps, mats}]}, materials {name: {blend, tex, scale, offset, tint,
  color}}, Unity space, left-handed, the page mirrors), MonoBehaviour fields under their serialized names, Unity
  components (ParticleSystem, ParticleSystemRenderer, ...) as UnityPy `read_typetree()` gives them (JSON-safe), the
  default (not Ronin) style.
- **Cue options** (if your part needs placement): `{d, x, y, rot, vol, cut, p, roll, scale, kill}`, see the comment above
  `cueOf` in index.html.

## Rules

- No Playwright or browser tests (the user tests by hand). Check JS syntax with `node --check <file>` (rename to .mjs
  or use `node --input-type=module --check < file`), Python by running it on the Wolf's real data.
- Never run `pipeline/wardrobe_fx.py wolf` without `--probe` (the lead rebuilds the data once at the end); agent E may
  run its own script, writing only `tto/` entries and `tto_` textures.
- Follow the game: cite file:line (BB `D:\12tails\DecompiledSource\*.cs`, TTO `D:\12tails\DecompiledSource_TTO_2026-11-02\`)
  for every behaviour; where you must approximate, say so in a code comment and in your report.
- Report back: what you built, how faithful (per behaviour), the Wolf effects it unlocks, any change needed in a shared
  file (exact), and what the user should look for when testing.
