# Goal: every class's skill SFX + VFX, committed, pushed and deployed

(The user, 2026-11-13, before an unattended overnight run: "finish all classes skill sfx and vfx all skills, commit
push and deploy"; usage guard at 70 % for this run.)

Run unattended until done or until the usage guard says stop. Don't ask the user questions: decide by the standing
rules below, and write every judgement call into NOTES.md.

Read first: CLAUDE.md, NOTES.md (its skill-effects sections), HANDOFF.md ("Next up" and the Penguin items),
plans/fx_recipe.md, plans/fx_wolf/decisions.md, plans/fx_sheep/decisions.md, plans/fx_penguin/*.md (the last class
done this way, as the template).

State at the start: Wolf and Sheep are done and online. The Penguin is built and cued, but still needs its effect-only
tiles (Mana Arc, Dispell, Frost Spike, Double / Triple Cast) and its QA. Not started: Bat, Bison, Cat, Chameleon, Mole,
Monkey, Panda, Rabbit, Whale. Weapons' own effects are separate and done (weapon_fx.json, 2026-11-13).

Order: Penguin first, then Bat, Bison, Cat, Chameleon, Mole, Monkey, Panda, Rabbit, Whale.

Per class, the established way (HANDOFF "Next up"):
1. Research workflow: read-only researchers, one report each in plans/fx_<cls>/, plus checkers. Researchers never run
   wardrobe_fx.py and never edit repo files.
2. Build workflow: one builder per missing page part (each in its own wardrobe/fxparts/ file; missing parts are always
   built), then ONE editor writes wardrobe/fx_cues/<cls>.json and builds with wardrobe_fx.py / wardrobe_fx_tto.py,
   then a QA pass.
3. Every skill gets its own tile with its Bible icon. Skills with no body clip get effect-only tiles on the idle stance.
4. Standing rules: the top rank's effects where the code picks by rank; random picks as the game does them; effects
   on an enemy go to the target point 10 m ahead; TTO skills included, but cued only if the skill is in
   wardrobe/tto_released.json (the publish rule); game behaviour from the Bible first, the decompiled code for the rest.
5. Gate (the user is asleep, so this replaces their hand checks for this run):
   `uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py D:/12tails-wardrobe checks/fx_<cls> dark --cls <cls>`
   must pass with every cued effect spawned and no page or console errors. Also re-run the weapon check
   (`pipeline/wardrobe_weapon_fx_check.py`) and the unit tests from CLAUDE.md. Fix failures before moving on. If a
   skill still can't be made right, leave it out of the cues and list it in NOTES.md and HANDOFF.md for the user.
6. After each class passes: append to NOTES.md (what was built, any judgement calls, anything uncertain), commit and
   push, then publish and deploy (NOTES.md "Online copy"):
   `py -3 pipeline/wardrobe_publish.py --out wardrobe_dist` (read the report and count changes; nothing non-BB or
   unreleased TTO, and its check must say "no problems"), then, from an EMPTY folder:
   `npx wrangler deploy D:/12tails-wardrobe/pipeline/site_worker.mjs --assets D:/12tails-wardrobe/wardrobe_dist --name 12tails-wardrobe --compatibility-date 2026-11-07`
   Then curl https://12tails-wardrobe.jumpthai.workers.dev to confirm a 200 and the new data folder.

Usage guard, at 70 % for this run (CLAUDE.md says 98 %; for this run it is 70): before the first workflow, start
`py -3 -I pipeline/usage_watch.py 70 300` in the background and keep it running. When it prints REACHED (the account's
weekly usage at 70 %): stop the running workflow and start no new agent or class, then commit and push everything
(finished and partial reports, code, data). Say in NOTES.md which agents finished and which files are partial, and add
a HANDOFF.md item to resume from there on either PC. Deploy only classes that already passed step 5. A BLIND line
means 30 minutes without a usage reading: note it and carry on.

Keep the workflows within the usual size (under 10 agents each). Don't touch the Bat skin work in plans/reskins/.
Never write in the video or Bible repos. When everything is done: one summary in NOTES.md, HANDOFF.md updated (the
Penguin items and "Next up" closed or narrowed), this file deleted (its work done), a final commit, push and deploy,
and a closing message listing each class's skills, what's left out, and the live URL.
