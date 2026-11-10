# Handoff between the two PCs

Steps one PC left for the other. A session reads this at the start, does what is listed for its PC (where the user's
go-ahead is needed, says so), and deletes each item once it is done. Empty = nothing pending.

## Home PC

- FYI: the Bible commit `0704e0f6` (reference notes on skill animations and weapon codes) was made at the office and
  not pushed; pull it there before editing those four reference files at home.

## Office PC

- Every effect builds on either PC now: TTO's (`pipeline\wardrobe_fx_tto.py`) reads the video folder's
  `tto_assets\2026-11-04` at home and, at the office, this repo's own git-ignored `tto_assets\2026-11-09` (the TTO
  install decrypted 2026-11-10; the 18 Wolf TTO effects come out identical). After a TTO patch: decrypt again into a
  new date (NOTES.md 2026-11-10 "TTO bundles at the office").

## Video repo (either PC)

- **Retire the wardrobe trailer** (user 2026-11-10: "the trailer video is already published, you may delete everything
  related to it to save space"), in a video session (that repo's rules): its frames `renders\wardrobe_trailer\` (home
  PC only, the space; not on the office PC), `pipeline\trailer_*.py` + `test_trailer.py`, `plans\trailer_*.json`,
  `plans\wardrobe_trailer_*.md`, `captions\wardrobe_trailer\`, `renders\yt_shorts\wardrobe_trailer\`; check `music_*.py`
  and anything else only the trailer uses. The wardrobe no longer keeps `window.wardrobe` working for it.

## Next up (either PC; agreed at the office 2026-11-09)

- **Effects + sounds for every class**, the plan the user and Claude settled on (NOTES.md "skill effects" entries):
  1. ~~Prep~~ done at home 2026-11-09 (NOTES.md "step 1 (prep) done"): cues in `wardrobe/fx_cues/<cls>.json`, the
     recipe `plans/fx_recipe.md`, the parts list `plans/fx_inventory.md` (403 of the classes' 699 own effects are
     buildable today; its greedy build order is the order to build the missing parts in).
  2. Next: one agent does the Wolf's remaining skills from `plans/fx_recipe.md` alone, to prove it (48 of the Wolf's
     69 effects are ready).
  3. Fan out: one agent per missing effect part (in the inventory's build order: VortexEmitter, EmblemEmitter,
     EmitterControl, then the mesh parts StaticMesh + Animation + SkinnedMeshRenderer together), then one per class
     (the session limit is under 10 agents per workflow unless the user raises it; the user starts it with "use a
     workflow"). Part agents touch `index.html` and `wardrobe_fx.py` (`LAYOUTS`), so run them one after another or
     in worktrees; class agents touch only their cue file and data. Headless browser checks one at a time (three at
     below-normal priority if the user asks for speed): the PC rule.
  Measured: Feral Strike took 4 min 7 s end to end; about 16-20 agent-hours in all, about 4-6 h wall clock in parallel.
- **The user's open decisions** (ask before building on them): the backdrop (`?fxbg=dark` / `spot` / `white`); a game
  clip of Cross Break to check its stretched slashes (they come out huge); whether to add the four skills' effect and
  sound timings to the Bible's Wolf reference; effects the game spawns at the target (hits on an enemy): the recipe
  leaves them out (no target in the wardrobe), or show them a fixed distance ahead?
