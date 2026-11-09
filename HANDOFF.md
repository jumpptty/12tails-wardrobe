# Handoff between the two PCs

Steps one PC left for the other. A session reads this at the start, does what is listed for its PC (where the user's
go-ahead is needed, says so), and deletes each item once it is done. Empty = nothing pending.

## Home PC

- **Deploy the built online copy** (the USER, 2026-11-09): `wardrobe_dist` was rebuilt at home with the item-map fix
  (6,899 files, data folder `data-7e0350ddb2`, check: no problems, pilot off). Deploy it from an empty folder with the
  wrangler line in NOTES.md "Online copy". Delete this item once deployed. (Publishing from the office still drops 4
  Monkey back items: its rip is damaged, see NOTES.md 2026-11-09 "office publishing"; publish from home.)
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
