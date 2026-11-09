# Handoff between the two PCs

Steps one PC left for the other. A session reads this at the start, does what is listed for its PC (where the user's
go-ahead is needed, says so), and deletes each item once it is done. Empty = nothing pending.

## Home PC

- **Rebuild the item map once** (left by the office, 2026-11-09): `py -3 -I pipeline\bb_item_codes.py`. The parser fix
  (commit 7d255b3) changed 14 codes in `wardrobe\data\item_map.json` / `icons.json`, which are not in git. Do it before
  any `transfer_to_drive.ps1`, or the office gets the old map back. Check: `wardrobe_sets_check.py` exits 0 (the
  Chameleon legend set wears legendBow).
- **Publish the online copy** (user's go-ahead to deploy): `py -3 pipeline\wardrobe_publish.py --out wardrobe_dist`
  after the rebuild above; it carries 2026-11-09's changes (max-rank moves, R / V tiles in ชุด, the item-map fix). The
  user deploys (NOTES.md "Online copy").
- **Build the effects pilot's data** (left by the office, 2026-11-09; the data isn't in git):
  `uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py wolf --fx armorBreak_ring,armorBreak2,crossBreak_ring,crossBreak,grandCross_ring,grandCross,feralStrike_ring,feralStrike --voices armorBreak1,armorBreak2,crossBreak1,crossBreak2,grandCross1,grandCross2,feralStrike1,feralStrike2`
  (reads `12TailsOnline_Data` in the Bible folder). Check: `wardrobe_fx_check.py` exits 0.
- **Office publishing** (2026-11-09): the office can build the public copy now (pilot switched off in it), but its rip
  is damaged (177 zero-filled Monkey files): textures come from `bb_rip_fix.py`, back items from the Reborn rip, and 4
  Monkey back items (legendTrinket, legendTrinketR, partyWhistle, poseidonTrinket) are still dropped there (Reborn's
  meshes are skinned / multi-stream, which `read_mesh_shape` refuses). So publish from home tonight, or teach the
  reader multi-stream meshes first.
- FYI: the Bible commit `0704e0f6` (reference notes on skill animations and weapon codes) was made at the office and
  not pushed; pull it there before editing those four reference files at home.

## Next up (either PC; agreed at the office 2026-11-09)

- **Effects + sounds for every class**, the plan the user and Claude settled on (NOTES.md "skill effects" entries):
  1. Prep, one session: move `FX_CUES` out of `index.html` into one tracked cue file per class (so parallel agents
     never edit the same lines), write the per-skill recipe from the pilot (trace the coroutine with `clip_flow.js`,
     probe the prefabs, `wardrobe_fx.py`, cue lines, `wardrobe_fx_check.py`), and list which effect parts each class
     needs (built: EffectControl, Ring / Image / Line emitters, legacy particles; not yet: Vortex / Bolt / Emblem /
     Trail emitters, Animation and skinned-mesh effects, the 46 Shuriken systems).
  2. One agent does the Wolf's remaining skills from the recipe alone, to prove it.
  3. Fan out: one agent per missing effect part, then one per class (the session limit is under 10 agents per
     workflow unless the user raises it; the user starts it with "use a workflow"). Headless browser checks one at a
     time (three at below-normal priority if the user asks for speed): the PC rule.
  Measured: Feral Strike took 4 min 7 s end to end; about 16-20 agent-hours in all, about 4-6 h wall clock in parallel.
- **The user's open decisions** (ask before building on them): the backdrop (`?fxbg=dark` / `spot` / `white`); a game
  clip of Cross Break to check its stretched slashes (they come out huge); whether to add the four skills' effect and
  sound timings to the Bible's Wolf reference.
