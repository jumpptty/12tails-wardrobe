# The wardrobe gets its own repo (design, 2026-11-09)

## Why

On 2026-11-09 one session committing a wardrobe change had to stop and coordinate with another session that was
committing fight-recreation shots and leaving trailer work behind, all in the one repo `jumpptty/12tails-video` and
the one `NOTES.md`. The user: "make a separate repo for the wardrobe, independent of the video works, so there's a
clear line between them". Success means a wardrobe session and a video session can run at the same time and never
have to look at each other's commits, notes or uncommitted files.

## Goals

- A private repo `jumpptty/12tails-wardrobe` holds everything that is only the wardrobe: the page, its build /
  publish / check scripts and tests, its plans and decision log, its own `CLAUDE.md` and `NOTES.md`.
- Folder `D:\12tails-wardrobe` on the home PC, `C:\work\12tails-wardrobe` on the office PC: a sibling of the Bible
  repo and the video repo (`D:\12tails`, `D:\12tails-video`; office `C:\Users\Jump\Desktop\12tails`,
  `C:\work\12tails-video`).
- The wardrobe never writes into the video folder and never commits there.
- The video repo no longer contains wardrobe files; it reads the wardrobe from outside, as it reads the Bible.
- The office PC ends up with the same layout through one short list of steps the user runs there.

## Non-goals

- No change to the public site (https://12tails-wardrobe.jumpthai.workers.dev): no redeploy is needed, its name and
  URL stay. The rebuilt `wardrobe_dist` should be byte-identical to the current one; if it isn't, the difference is
  reported to the user, not deployed.
- The extraction scripts (`extract*.py`, `extract_tto_*.py`, `props.py`, `skins.py`, ...) and their outputs stay in
  the video repo; the wardrobe reads their outputs.
- No change to the trailer's footage or edit; only where it finds the wardrobe.
- No change to the Bible beyond the one pointer in its hub skill.

## Anti-goals (a failure even if everything "works")

- Losing or corrupting the untracked wardrobe data (`wardrobe\data`, 300 MB). The office PC has no game rips to
  rebuild it.
- Sweeping another session's uncommitted work into a commit (the video repo has a live peer session,
  `12tails-video-18`).
- Publishing anything (Cloudflare deploys are the user's; GitHub pushes only to the user's own repos).
- Leaving the office PC half moved.
- Junctions or symlinks between the folders (NOTES.md: `git worktree remove` / `git clean` empties a junction's target).

## Decided by the user

- A separate repo, so wardrobe and video sessions never collide (this conversation, 2026-11-09).
- The wardrobe may READ files the video folder already extracted (props, outfits, textures, `tto_assets`,
  `tot_assets`); it never writes there.
- The video side keeps reading the wardrobe from outside: the trailer films the wardrobe's published copy; skits on
  the office PC fall back to the wardrobe's data.
- The office PC has not yet run the steps sent earlier (pull + `move_project.ps1`): the split happens first, then new
  office steps cover the video move and the wardrobe setup in one go.
- **The office gets the home PC's current wardrobe data** ("the latest one"): the office's own copy is older (no ToT
  student outfits, 649 of 660 edition textures, no `tot_*` prop textures). It travels as one tar on the flash drive;
  the office's old copy is renamed out of the way (`<video>\wardrobe_data_old`), not deleted, for the user to delete
  later.
- **The Bible commits are committed, not pushed** (the user: "Commit"): its branch is the one GitHub Pages serves.
- The user creates the GitHub repo `jumpptty/12tails-wardrobe`.

## Claude's calls (the user can overrule any)

- **Name and place:** `jumpptty/12tails-wardrobe` (the Cloudflare site's own name), folders as above. The video
  side finds it as the sibling folder `<video root>\..\12tails-wardrobe`; the wardrobe finds the video folder as
  `<wardrobe root>\..\12tails-video` (both work on both PCs, since the office mirrors `D:\` under `C:\work`).
- **History comes along:** the new repo is made with `git filter-repo` from a fresh clone of the video repo, keeping
  only the paths that move, so `git log` / blame of the wardrobe files survive. The video repo's history is not
  rewritten.
- **Same layout inside:** `wardrobe\` (page, icons, `ui\`, untracked `data\`), `pipeline\` (scripts), `plans\`,
  `wardrobe.cmd`, `CLAUDE.md`, `NOTES.md`, a whitelist `.gitignore` like the video repo's. Commands in docstrings keep
  their shape (`py -3 pipeline/wardrobe_publish.py ...`).
- **Prop textures inside the wardrobe:** the page loads prop textures from `../props/tex/` (the video folder) today,
  which a separate folder can't reach. They move to `wardrobe\data\props\tex\`: the page uses `${DATA}props/tex/`, the
  same path the published copy already uses, so `wardrobe_publish.py`'s "prop textures" rewrite goes away.
  `wardrobe_data.py` copies the textures its props JSON references from the video folder's `props\tex\`;
  `wardrobe_tot.py` writes its `tot_*.png` there instead of into the video folder.
- **No other writes into the video folder:** `wardrobe_placements.py` also copies TTO's `*Placement.json` into the
  video's `tto_assets\2026-11-04\config\` (nothing reads those copies); they go to an untracked `tto_config\` in the
  wardrobe folder instead.
- **Scripts that move** (all tracked): `wardrobe\index.html`, `wardrobe\wardrobe.ico`, `wardrobe\wardrobe_icon.svg`,
  `wardrobe\ui\recolor1-5.webp`, `wardrobe.cmd`; `pipeline\`: `wardrobe_data.py`, `wardrobe_editions.py`,
  `wardrobe_icons.py`, `wardrobe_moves_check.py`, `wardrobe_placements.py`, `wardrobe_publish.py`, `wardrobe_tot.py`,
  `wardrobe_ui_assets.py`, `test_wardrobe_publish.py`, `bb_item_codes.py`, `placement_sweep.py`, `clip_calls.js`,
  `clip_flow.js` (the BB-code tracers that built the page's move-sequence table); `plans\wardrobe_online_plan.md`;
  this design. Untracked, moved as folders: `wardrobe\data\`, `wardrobe_dist\`, `wardrobe_dist_report.json` (+
  `.prev.json`), `.superpowers\sdd\2026-11-07-wardrobe-online\`.
- **Stays in the video repo:** everything else, including the trailer (`trailer_*.py`, `music_*.py`,
  `plans\wardrobe_trailer_*.md`, `captions\wardrobe_trailer\`), `wrangler.jsonc` (it publishes `review\`, not the
  wardrobe) and `move_project.ps1` (history).
- **Video-side readers repointed** to the sibling wardrobe folder: `skins.py` (faces fallback), `skitlib.py`
  (`tto_placement`, which reads the wardrobe's `placements.json` for every skit build, and `_wardrobe_prop`), `extract_tto_props.py` (`item_map.json`), `trailer_common.py`
  (`WARDROBE_DIST`) and whatever else in the trailer reads the wardrobe through it. One commit removes the moved files
  from the video repo.
- **Notes:** the `NOTES.md` sections "Wardrobe app", "ToT student outfits in the LOCAL wardrobe" and "Online copy" move
  to the wardrobe's `NOTES.md`, as do session-log entries that are only about the wardrobe (text unchanged); mixed
  entries and the extraction sections (TTO faces / outfits / animations / props) stay, and the video NOTES keeps a
  two-line pointer. Commands inside the moved sections get the new paths (e.g. the deploy's `--assets
  D:\12tails-wardrobe\wardrobe_dist`); session-log text stays as written. The video `CLAUDE.md`'s wardrobe paragraph (added earlier today) becomes: the wardrobe has its own
  repo, never edit it from here, the trailer and the office fallbacks only read it.
- **The wardrobe's `CLAUDE.md`:** what it is, the two PCs, the line (read the video and Bible folders, never write or
  commit there), how scripts run, browser checks as the norm, the BB-only content rule and the user-only deploy, Thai
  on-screen text, "read the Bible first" for mechanics, "read NOTES.md first".
- **Moving the data:** a script in the new repo, `pipeline\adopt_from_video.ps1`, used first on the home PC (so the
  office runs a tested script): moves `<video>\wardrobe\data`, `wardrobe_dist` and its reports into the wardrobe folder
  (same drive, so each move is a rename), copies the referenced prop textures in, repoints the Desktop shortcut
  "12 Tails Wardrobe" to the new `wardrobe.cmd`, and removes `<video>\wardrobe` once it is empty. It refuses to
  overwrite anything already in the target and stops at the first problem. On the home PC it runs before the
  video-side commit, so the tracked page files are still in `<video>\wardrobe` then: the script leaves them, and the
  folder goes with that commit. On the office PC the wardrobe folder already holds the home data (restored from the
  tar first), so the script renames the office's old `<video>\wardrobe\data` to `<video>\wardrobe_data_old` instead of
  moving it, and still repoints the shortcut.
- **Moving data between PCs:** the video `transfer_to_drive.ps1` drops its `-WardrobeOnly` pack and its
  `wardrobe\data` entry; the wardrobe repo gets its own small transfer step (one tar of `wardrobe\data`, prop
  textures included, + restore steps), since its code now travels by its own GitHub repo. It is used right away: the
  office gets its data this way.
- **Bible pointer:** a new commit on top of the unpushed `9a6a25c` points the `bible-hub-tools` skill at
  `D:\12tails-wardrobe`. Committed only: the Bible's branch `skill-cooldown-lookup` is the one GitHub Pages serves, so
  a push publishes; it waits for the user's yes.
- **Coordination:** message the peer session before the data move (its skit builds read `wardrobe\data` through
  `skitlib.tto_placement`, so a build mid-move would break) and again before the video-side commit; stage only this
  work (the peer's uncommitted files stay out, as done earlier today).
- **Claude memory:** the new project starts with no memories; its rules live in its `CLAUDE.md`.

## Order of work

1. The user creates the empty private repo `jumpptty/12tails-wardrobe` on github.com (no README, licence or
   .gitignore). Claude can't create it.
2. Build the new repo (filter-repo), add `CLAUDE.md`, `NOTES.md`, `.gitignore`, the path changes and the prop-texture
   move; move the untracked data in with `adopt_from_video.ps1`.
3. Verify the wardrobe (below), commit, push.
4. The video-side commit (removals, readers repointed, CLAUDE.md, NOTES.md), coordinated with the peer; verify; push.
5. The Bible pointer commit (not pushed).
6. The wardrobe data tar written to the flash drive when the user plugs it in, and the office steps as a plain-text
   message the user can send through LINE: video pull + `move_project.ps1`, clone the wardrobe repo, restore the tar,
   `adopt_from_video.ps1`.

## How it is checked

- New repo: `py -3 -m unittest pipeline.test_wardrobe_publish` passes; `wardrobe_moves_check.py` passes headless;
  the local page (served like `wardrobe.cmd` does) dresses every class with its props textured and no 404s;
  `wardrobe_publish.py` rebuilds `wardrobe_dist` with `--check` clean and the output identical to the current copy;
  `git log -- wardrobe/index.html` shows its history.
- Video repo: the 53 trailer tests pass against the moved `wardrobe_dist`; the skins / skitlib fallbacks resolve to
  the new folder; `git grep -i wardrobe` there lists only readers and history.
- Nothing is left in `<video>\wardrobe` and nothing the wardrobe uses points into the video folder except the
  read-only inputs named above.

## Left to the builder

The exact filter-repo invocation, how the props textures are copied (only the referenced ones), the wording of the
two `CLAUDE.md`s and the NOTES pointer, the transfer step's details, the shortcut code, commit wording.
