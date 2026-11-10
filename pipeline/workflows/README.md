# Workflow scripts (Claude Code's Workflow tool)

The scripts of the multi-agent workflows that built the class effects (user 2026-11-10: "use workflows to complete
Sheep class next!", "use workflows to do the next class, Penguin"). They are kept here because a workflow's own copy
lives only in the session that ran it, and a stopped run can be resumed (`resumeFromRunId`) only in that session: on
another PC or in a new session, run the script again (pass it to the Workflow tool as `scriptPath`), or edit a copy.

| Script | What it does | Agents |
|---|---|---|
| `sheep-fx-research.js` | six read-only researchers write `plans/fx_sheep/*.md`, three checkers re-trace and fix them | 9 |
| `sheep-fx-build.js` | four part builders (own files each), one editor (`fx_cues/sheep.json`, data build, checks), one QA pass | 6 |
| `penguin-fx-build.js` | the Sheep's build for the Penguin (home PC paths): four builders (mesh.js shaders, penguin.js, page + pipeline, TTO), one editor, one QA pass that also re-checks the Sheep and the Wolf | 6 |
| `penguin-fx-research.js` | the Sheep's research for the Penguin, the Sheep / Wolf decisions applied by analogy; stopped at 98 % of the weekly limit after `own_skills` (HANDOFF.md "Continue the Penguin's effects research") | 9 |

To continue the Penguin from a new session: copy `penguin-fx-research.js`, keep only the RESEARCH entries still to
write (and tto if `plans/fx_penguin/tto.md` stops short), keep the checker pairs, run it. For the build, copy
`sheep-fx-build.js` and swap the Sheep for the Penguin (its parts from `plans/fx_penguin/parts.md`, its decisions
file). The paths inside are the office PC's (`C:\work\...`, the Bible at `C:\Users\Jump\Desktop\12tails`): at home use
`D:\12tails-wardrobe` and `D:\12tails` (CLAUDE.md "Two PCs"). Start the usage guard first (CLAUDE.md).
