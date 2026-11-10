# Handoff between the two PCs

Steps one PC left for the other. A session reads this at the start, does what is listed for its PC (where the user's
go-ahead is needed, says so), and deletes each item once it is done. Empty = nothing pending.

## Home PC

- **The Sheep's effects data was built at the office** (NOTES.md 2026-11-10 "the Sheep's effects: built and cued"):
  `wardrobe\data\sheep\fx.json`, `wardrobe\data\sheep\sfx\`, the new `wardrobe\data\fx\tex\` textures (tto_*,
  sheep's) and `wardrobe\data\wolf\fx.json` + `fx\tex\wolf_dead.webp` (the Wolf's deadEffect). `wardrobe\data` is
  tracked in git since 2026-11-10 (NOTES.md "`wardrobe\data` in git"), so they come with the commit: `git add` the
  untracked data files with it, then a plain pull at home brings them (check: `wardrobe_fx_check.py ... --cls sheep
  --files-only`). Only if they were left out of the commit: rebuild at home, `uv run --no-project --with UnityPy --with
  imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py sheep`, then the same with `pipeline/wardrobe_fx_tto.py
  sheep`, and `pipeline/wardrobe_fx.py wolf --fx deadEffect` (not a full Wolf rebuild: NOTES.md 2026-11-10).

- The usage guard came from the office (CLAUDE.md "Usage guard", `pipeline\usage_watch.py`): nothing to install. Its
  first run at home may be blocked by the safety check (it reads the saved Claude login); the user allowed it on
  2026-11-10, so ask them once and run it. Check: `py -3 -I pipeline/usage_watch.py --once` prints the weekly %.

- FYI: the Bible commit `0704e0f6` (reference notes on skill animations and weapon codes) was made at the office and
  not pushed; pull it there before editing those four reference files at home.

## Office PC

- Every effect builds on either PC now: TTO's (`pipeline\wardrobe_fx_tto.py`) reads the video folder's
  `tto_assets\2026-11-04` at home and, at the office, this repo's own git-ignored `tto_assets\2026-11-09` (the TTO
  install decrypted 2026-11-10; the 18 Wolf TTO effects come out identical). After a TTO patch: decrypt again into a
  new date (NOTES.md 2026-11-10 "TTO bundles at the office").

## Either PC

- **Continue the Penguin's effects research** (stopped at 98 % of the weekly limit, 2026-11-10; NOTES.md "the
  Penguin's research stopped"). Done: `plans/fx_penguin/own_skills.md`. Possibly incomplete: `plans/fx_penguin/tto.md`
  (its agent never returned: read its end; re-run its part if it stops short). Still to write: `attacks_emotes.md`
  (Normal / Charge Attack, MP Transfer on nAttack1, activateIcon1 on cAttack2, emotes, KO), `cast_a.md` (the Cast
  channel + cast3 skills manaMissile, manaBurn, fallingComets, manaVortex, meteora, frozenBlast, arcticWind,
  iceShield), `cast_b.md` (iceBlock, snowMan, tornado, typhoon, absoluteZero, blizzard, snowBall, cosmicRift, Cosmic
  Friday), `parts.md` (Penguin_tornado, _typhoon, _arcticEmperor, _cosmicFriday, _iceBlock, _nAttack + anything drawn
  wrongly). Then three checkers (attacks_emotes + own_skills, cast_a + cast_b, tto + parts) re-trace and fix in place.
  Same method as the Sheep's (`plans/fx_sheep/*.md` and its decisions apply by analogy; ask the user only new
  questions); then the build workflow as the Sheep's (NOTES.md "the Sheep's effects: built and cued"). Start the usage
  guard first. The workflow scripts to copy are in `pipeline\workflows\` (its README: what to keep, the home paths).

## Video repo (either PC)

- **Retire the wardrobe trailer** (user 2026-11-10: "the trailer video is already published, you may delete everything
  related to it to save space"), in a video session (that repo's rules): its frames `renders\wardrobe_trailer\` (home
  PC only, the space; not on the office PC), `pipeline\trailer_*.py` + `test_trailer.py`, `plans\trailer_*.json`,
  `plans\wardrobe_trailer_*.md`, `captions\wardrobe_trailer\`, `renders\yt_shorts\wardrobe_trailer\`; check `music_*.py`
  and anything else only the trailer uses. The wardrobe no longer keeps `window.wardrobe` working for it.

## Next up (either PC)

- **Effects + sounds for every class, one class at a time with two workflows** (user 2026-11-10: "use workflows to do
  the next class"): research (six read-only researchers + three checkers, reports in `plans/fx_<cls>/`), then build
  (one builder per missing part with its own files, one editor writes `wardrobe/fx_cues/<cls>.json` and builds, one QA
  pass), then the user's checks list and a deploy. Done: Wolf, Sheep. In progress: Penguin (2026-11-10). Left: Bat,
  Bison, Cat, Chameleon, Mole, Monkey, Panda, Rabbit, Whale. The user's standing decisions: `plans/fx_wolf/decisions.md`
  and `plans/fx_sheep/decisions.md` apply to every class by analogy; missing parts are always built (memory
  "feedback-build-missing-fx-parts", `plans/fx_recipe.md`).
- Settled since 2026-11-09 (no longer open): the backdrop is a manual toggle, white by default (the พื้นหลัง button);
  effects on an enemy go to the target point 10 m ahead; the user declined the Sheep's Bible findings (2026-11-10: "no need to
  offer"; they stay in NOTES.md and the reports). Still open: a game clip of Cross Break to check its stretched
  slashes.
