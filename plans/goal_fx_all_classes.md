# Goal: every class's skill SFX + VFX, committed, pushed and deployed

(The user, 2026-11-13: "finish all classes skill sfx and vfx all skills, commit push and deploy"; the overnight run
stopped at 07:05 after five classes; resumed 2026-11-13 at the office: "goal prompt to finish what we started".)

Run unattended until done. Don't ask the user questions: decide by the standing
rules below, and write every judgement call into NOTES.md as you go.

Read first: CLAUDE.md, NOTES.md (its skill-effects sections, especially "every class's skill effects: the run" and the
Chameleon, the last class built), HANDOFF.md ("Next up"), plans/fx_recipe.md, plans/fx_chameleon/*.md (the template).

State at the start: Wolf, Sheep, Penguin, Bat, Bison, Cat, Chameleon are done and online (last 49b0bc5). The Mole's
research is done and verified (plans/fx_mole/*.md) and its planner wrote plans/fx_mole/decisions.md: reuse it (give the
builders its parts split again; re-plan only what it leaves unclear). Nothing of the Mole is in the page or data yet.
Not started: Monkey, Panda, Rabbit, Whale.

Order: Mole (build only), then Monkey, Panda, Rabbit, Whale (research, then build). The research of one class may
overlap the build of the one before; builds never overlap (they share wardrobe/index.html).

Workflow: `class-fx`, re-created from NOTES.md's description (args `{mode: "research"|"build", cls, Cls, skills, tto,
released}`). Per class:
1. Research: six read-only researchers, one report each in plans/fx_<cls>/ {attacks_emotes, skills_a, skills_b, tto,
   effect_only, parts}.md, plus three checkers appending "## Verification" (it wins). Researchers never run
   wardrobe_fx.py and never edit repo files.
2. Build: planner -> plans/fx_<cls>/decisions.md ("decided overnight, for the user's review"); up to four builders on
   disjoint files (each missing page part in its own wardrobe/fxparts/ file; missing parts are always built); ONE editor
   writes wardrobe/fx_cues/<cls>.json, tiles, icons (wardrobe_skill_icons.py), data (wardrobe_fx.py / wardrobe_fx_tto.py);
   then one QA with wardrobe_fx_shots.py.
3. Every skill gets its own tile with its Bible icon; skills with no body clip get effect-only tiles on the idle stance.
4. Standing rules: the top rank's effects where the code picks by rank; random picks as the game does them; effects on
   an enemy go to the target point 10 m ahead; TTO skills included, cued only if in wardrobe/tto_released.json; game
   behaviour from the Bible first, the decompiled code for the rest.
5. Gate, from the repo root (works on either PC):
   `uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py . checks/fx_<cls> dark --cls <cls>`
   must pass with every cued effect spawned and no page or console errors; also `pipeline/wardrobe_weapon_fx_check.py`
   and the unit tests from CLAUDE.md. index.html must stay LF (`grep -c $'\r$' wardrobe/index.html` = 0). Fix failures
   before moving on; a skill that still can't be made right is left out of the cues and listed in NOTES.md + HANDOFF.md.
6. After each class passes: NOTES.md (built, judgement calls, uncertain points), commit and push (stage paths by name:
   never commit plans/reskins/, the user's own work), then publish and deploy (NOTES.md "Online copy"):
   `py -3 pipeline/wardrobe_publish.py --out wardrobe_dist` (read the report; nothing non-BB or unreleased TTO; its check
   must say "no problems"), then from an EMPTY folder outside the repo:
   `npx wrangler deploy <repo>/pipeline/site_worker.mjs --assets <repo>/wardrobe_dist --name 12tails-wardrobe --compatibility-date 2026-11-07`
   (`<repo>` = this folder's absolute path on the PC you are on). Then curl https://12tails-wardrobe.jumpthai.workers.dev
   for a 200 and the new data folder.

No usage guard (lifted for good, user 2026-11-13; CLAUDE.md). Deploy only classes that passed step 5.

Keep workflows under 10 agents each. Never write in the video or Bible repos. When everything is done: one summary in
NOTES.md, HANDOFF.md's "Next up" closed or narrowed, this file deleted, a final commit, push and deploy, and a closing
message listing each class's skills, what's left out, and the live URL.
