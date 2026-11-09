# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

The **12 Tails Wardrobe (ห้องแต่งตัว)**: a three.js page where players dress any 12 Tails hero in every outfit, colour,
face, prop and move, with a public copy at https://12tails-wardrobe.jumpthai.workers.dev that the 12 Tails Bible's hub
opens from its ห้องแต่งตัว tile. It split from `jumpptty/12tails-video` (the skits and dance videos) on 2026-11-09 so
wardrobe and video sessions never share commits, notes or uncommitted files (user: "a clear line between them").

**Read `NOTES.md` first** and append to it during the session, not at the end. **Then `HANDOFF.md`:** do what it lists
for this PC and delete each done item. A step the other PC must take (a rebuild after pulling, a publish, a file to
carry) goes there and gets pushed with the commit; never leave it only in a message to the user (user 2026-11-09). Every script lives in `pipeline/`,
never only in a session scratch dir.

## Two PCs

| | Home PC | Office PC |
|---|---|---|
| This folder | `D:\12tails-wardrobe` | `C:\work\12tails-wardrobe` |
| Video repo (read only) | `D:\12tails-video` | `C:\work\12tails-video` |
| Bible repo (game rips, decompiles) | `D:\12tails` | `C:\Users\Jump\Desktop\12tails` |

Code moves by git (`origin` = private GitHub `jumpptty/12tails-wardrobe`); `wardrobe\data` moves as one tar through
Google Drive (user 2026-11-09: "No flashdrive, google drive only"): `pipeline\transfer_to_drive.ps1 -Dest <folder>`
writes it (the Desktop, say), the user uploads it and downloads it on the other PC. The data build needs the game rips, which only the home PC has: build at home,
carry the data to the office. Scripts find the video folder as their sibling (`<this folder>\..\12tails-video`) and
the Bible under either PC's path.

## The line between this repo and the video repo

- Read the video folder's extracted files (`outfits\`, `tex\faces_tto\`, `props\json\`, `props\tex\`, `tto_assets\`,
  `tot_assets\`) and the Bible's rips; never write or commit in either. If a wardrobe change needs a fresh extraction
  (a new prop, a new outfit), say so: the extraction scripts belong to the video repo.
- The video repo reads this one as its sibling: its trailer films `wardrobe_dist`, its skits read `wardrobe\data`
  (`placements.json`, `icons.json`, the office's prop and face fallbacks), its `extract_tto_props.py` reads
  `item_map.json`. Renaming or moving those breaks it: note any such change in NOTES.md and tell the user.
- A session for video work runs in the video folder, one for wardrobe work here.

## Running things

- The page: `wardrobe.cmd` serves this folder on http://127.0.0.1:8771 and opens `wardrobe/`.
- Data: `pipeline\wardrobe_data.py` and its siblings (`wardrobe_icons.py`, `wardrobe_placements.py`, `wardrobe_tot.py`,
  `wardrobe_ui_assets.py`, `wardrobe_editions.py`, `bb_item_codes.py`); each docstring has its exact command line.
  Plain Python runs as `uv run --no-project --with <pkgs> python ...` or `py -3`, never a global `pip install`.
- Tests: `py -3 -m unittest pipeline.test_wardrobe_publish pipeline.test_wardrobe_props_tex pipeline.test_repo_rules`;
  `powershell -ExecutionPolicy Bypass -File pipeline\test_adopt_from_video.ps1`.
- Browser checks are the norm (unlike the Bible's rule): `pipeline\wardrobe_moves_check.py`, `wardrobe_menu_check.py`
  (the piece menu), `wardrobe_sets_check.py`, `wardrobe_fx_check.py` (headless Playwright), and an isolated Playwright context for anything else so the user's own browser window is left alone.
- The public copy: `py -3 pipeline\wardrobe_publish.py --out wardrobe_dist`, then deploy (NOTES.md "Online copy"):
  Claude may deploy when the user asks for it (user 2026-11-09: "please change that Claude.md setting then deploy"),
  always from an empty folder, never from the video folder. Online it carries BB content plus the TTO items in `wardrobe\tto_released.json` (the
  user's content rule, enforced by the publish; TTO is preview only online: no downloads or uploads). ToT never goes online.

## How the user works

- The audience is Thai: every on-screen word is Thai, numbers stay digits; check Thai mark placement wherever text is
  rendered.
- When a look is being picked, mock several variants side by side so the user picks visually.
- Game behaviour (skill clips, their order and timing): read the Bible first, `12t_reference/<class>-skill-reference.md`
  and the skill cards in `12t_projects/bible/index.html`; the decompiled code only for what they don't cover
  (`pipeline\clip_calls.js`, `clip_flow.js`). A new game-mechanic finding belongs in the Bible's reference too: tell the
  user and offer to add it there (that repo has its own rules, its `AGENTS.md` §4).
- The Bible's hub links here; its `bible-hub-tools` skill describes the tile. A change to the site's URL is one line
  there (the user's to publish).
