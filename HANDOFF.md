# Handoff between the two PCs

Steps one PC left for the other. A session reads this at the start, does what is listed for its PC (where the user's
go-ahead is needed, says so), and deletes each item once it is done. Empty = nothing pending.

## Home PC

- Publishing from the office still drops 4 Monkey back items (its rip is damaged, NOTES.md 2026-11-09 "office
  publishing"): publish from home.
- FYI: the Bible commit `0704e0f6` (reference notes on skill animations and weapon codes) was made at the office and
  not pushed; pull it there before editing those four reference files at home.

## Office PC

- **Pick up the home PC's work of 2026-11-09 (night)** (the user: "make sure I can pull from work PC and continue working
  on the wardrobe"). Code: `cd C:\work\12tails-wardrobe ; git pull` (everything is pushed). Data: the home PC wrote a
  fresh transfer (`C:\Users\Jump\Desktop\12tails-wardrobe-transfer`: `wardrobe_data.tar` 362 MB, 8,107 files, plus
  `README.txt`); the user uploads that folder to Google Drive and downloads it at the office. Then, in PowerShell:
  `Move-Item C:\work\12tails-wardrobe\wardrobe\data C:\work\12tails-wardrobe\wardrobe_data_old` (git ignores it there),
  then `tar.exe -xf <download folder>\wardrobe_data.tar -C C:\work\12tails-wardrobe`. It carries what git can't: the
  Wolf's effects and sounds (`data\wolf\fx.json`, `data\wolf\sfx\`, `data\fx\tex\`, TTO's included), the Bible's skill
  icons (`data\icons\hd\`), the rebuilt item map. Check: run `wardrobe.cmd`, pick the Wolf, play Cross Break with
  เสียงท่าทาง on. Delete `wardrobe_data_old` once happy. (No adopt step: the office did it on 2026-11-09.)
- The TTO effects (`pipeline\wardrobe_fx_tto.py`) build at home only (it reads the video folder's
  `tto_assets\2026-11-04`); the BB effects (`pipeline\wardrobe_fx.py <cls>`) and the skill icons
  (`pipeline\wardrobe_skill_icons.py`) build on either PC.
- The online copy was deployed from home on 2026-11-09 (effects on, version 00f769bf); publishing from the office still
  drops 4 Monkey back items (its damaged rip), so publish from home (Home PC section).

## Video repo (either PC)

- The rebuilt `wardrobe_dist` (2026-11-09, the piece menu) breaks the trailer script: `trailer_features.py` clicks
  `#vmode` ("inspect", "download") and a tile's `.sk[data-sk="up"]`, both gone. Their replacements: a click on the
  piece (or a right-click on the tile) opens `#pmenu`; its items are `.pm-item[data-a="view" | "up" | "png" | "glb"]`.
  Fix it in a video session (that repo's rules).

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
