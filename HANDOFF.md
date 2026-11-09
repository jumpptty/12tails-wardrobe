# Handoff between the two PCs

Steps one PC left for the other. A session reads this at the start, does what is listed for its PC (where the user's
go-ahead is needed, says so), and deletes each item once it is done. Empty = nothing pending.

## Home PC

- **Deploy the built online copy** (the USER, 2026-11-09): `wardrobe_dist` was rebuilt at home with the item-map fix
  (6,899 files, data folder `data-7e0350ddb2`, check: no problems, pilot off). Deploy it from an empty folder with the
  wrangler line in NOTES.md "Online copy". Delete this item once deployed. (Publishing from the office still drops 4
  Monkey back items: its rip is damaged, see NOTES.md 2026-11-09 "office publishing"; publish from home.)
  **It predates the piece menu** (NOTES.md 2026-11-09 "the piece menu"): to put the menu online, rebuild first
  (`py -3 pipeline\wardrobe_publish.py --out wardrobe_dist`, about 6.5 min) once the user is happy with it locally. That
  rebuild breaks the video repo's trailer script (`trailer_features.py` clicks `#vmode` and the tiles' upload button):
  tell the user, and fix it in a video session.
- FYI: the Bible commit `0704e0f6` (reference notes on skill animations and weapon codes) was made at the office and
  not pushed; pull it there before editing those four reference files at home.

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
