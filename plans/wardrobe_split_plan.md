# Wardrobe Split Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the 12 Tails Wardrobe out of `jumpptty/12tails-video` into its own repo `jumpptty/12tails-wardrobe`
(`D:\12tails-wardrobe`), so wardrobe and video sessions never share commits, notes or uncommitted files.

**Architecture:** A history-preserving copy of the wardrobe's paths (`git filter-repo` on a fresh clone) becomes the
new repo; its scripts find the video folder as their sibling and only read from it; the page's prop textures move
into its own data. The untracked data moves by one tested PowerShell script. The video repo then drops the moved
files and reads the wardrobe as its sibling.

**Tech Stack:** git 2.42 + `uvx git-filter-repo`, Python 3 (`py -3`, unittest), PowerShell 5.1, Playwright
(`uv run --no-project --with playwright`), background Blender for one skitlib check.

**Spec:** `plans/wardrobe_split_design.md` (approved 2026-11-09). Read it first; this plan argues from it.

## Global Constraints

- New repo `https://github.com/jumpptty/12tails-wardrobe.git` (exists, empty, private); folder `D:\12tails-wardrobe`
  (office `C:\work\12tails-wardrobe`); branch `main`.
- The wardrobe finds the video folder as `<wardrobe root>\..\12tails-video` and the video finds the wardrobe as
  `<video root>\..\12tails-wardrobe`; the Bible stays as each script already finds it.
- The wardrobe only READS the video folder (`outfits\`, `tex\`, `props\json\`, `props\tex\`, `tto_assets\`,
  `tot_assets\`); it never writes or commits there.
- No junctions or symlinks; every data move is a same-drive rename; nothing already in a target is overwritten.
- The live peer session `12tails-video-18` works in the video repo: message it before the cutover, stage only this
  work, never `checkout` / `reset` / `stash` / `rebase`.
- No Cloudflare deploy (the user's). The Bible commits are committed, NOT pushed. Pushes go only to
  `12tails-wardrobe` and `12tails-video`.
- The rebuilt `wardrobe_dist` must equal the current one; a difference is reported, not deployed.
- Commit messages end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Review Focus

1. **Adopt re-run or a target that already has data** (the office restores the tar first): the script must never
   overwrite; at home it stops, at the office (`-SetAside`) it renames the video's old copy to `wardrobe_data_old`.
   Test: Task 3 scratch run with a pre-filled target.
2. **`-SetAside` with nothing restored yet** (the office forgot the tar): must stop with a message, not move the
   old office copy in. Test: Task 3.
3. **A prop texture the props JSON names but the video folder lacks:** listed by name and non-zero exit, never a
   silent grey prop. Test: Task 2 `test_missing_texture_reported`.
4. **A folder held by a running server / editor during the move:** each item moves as one rename; the first failure
   stops the script and prints what already moved and what didn't. Test: Task 3 (a file held open in the scratch
   source).
5. **A peer skit build during the cutover window** (skitlib reads `placements.json` every build): the peer is told to
   hold builds before Task 5 and released after. Check: Task 5 message + reply.

---

### Task 1: The new repo with the wardrobe's history

**Files:**
- Create: `D:\12tails-wardrobe\` (clone + filter), `D:\12tails-wardrobe\.gitignore`

**Interfaces:**
- Produces: repo at `D:\12tails-wardrobe` on `main`, remote `origin` = the new GitHub URL, holding exactly the 23
  paths below with their history.

- [ ] **Step 1: Clone and filter**

```bash
git clone --no-local D:/12tails-video D:/12tails-wardrobe
cd D:/12tails-wardrobe && uvx git-filter-repo --force \
  --path wardrobe/ --path wardrobe.cmd --path plans/wardrobe_online_plan.md \
  --path pipeline/wardrobe_data.py --path pipeline/wardrobe_editions.py --path pipeline/wardrobe_icons.py \
  --path pipeline/wardrobe_moves_check.py --path pipeline/wardrobe_placements.py --path pipeline/wardrobe_publish.py \
  --path pipeline/wardrobe_tot.py --path pipeline/wardrobe_ui_assets.py --path pipeline/test_wardrobe_publish.py \
  --path pipeline/bb_item_codes.py --path pipeline/placement_sweep.py --path pipeline/clip_calls.js --path pipeline/clip_flow.js
git remote add origin https://github.com/jumpptty/12tails-wardrobe.git
```

- [ ] **Step 2: Verify the paths and history**

Run: `git ls-files | wc -l` → `23` (8 under `wardrobe/`, `wardrobe.cmd`, the plan, 13 scripts); `git log --oneline -- wardrobe/index.html | wc -l` equals the same count run in
`D:\12tails-video`; `git status` clean.

- [ ] **Step 3: Whitelist `.gitignore`** — `/*`, then `!/.gitignore`, `!/CLAUDE.md`, `!/NOTES.md`, `!/wardrobe.cmd`,
  `!/pipeline/`, `!/plans/`, `!/wardrobe/`, then `/wardrobe/data/` and `__pycache__/`.

- [ ] **Step 4: Copy the design and this plan in** (`plans\wardrobe_split_design.md`, `plans\wardrobe_split_plan.md`
  from the video folder; they were never committed there), commit `wardrobe: own repo (split from 12tails-video with
  its history); whitelist .gitignore; the split's design and plan`. No push yet.

### Task 2: Prop textures inside the wardrobe; the scripts read the video folder as a sibling

**Files:**
- Create: `pipeline/wardrobe_props_tex.py`, `pipeline/test_wardrobe_props_tex.py`
- Modify: `wardrobe/index.html:701`, `pipeline/wardrobe_publish.py:36,115` (+ docstring),
  `pipeline/test_wardrobe_publish.py:52,859,877`, `pipeline/wardrobe_data.py` (ASSETS, outfits, `tex/faces_tto`,
  `props/json`; calls the copy at the end), `pipeline/wardrobe_tot.py:22,43,46`, `pipeline/wardrobe_icons.py:33`,
  `pipeline/wardrobe_ui_assets.py:25`, `pipeline/wardrobe_placements.py:4,27`

**Interfaces:**
- Produces: `copy_prop_textures(data: Path, src: Path) -> tuple[int, list[str]]` (copied count, missing names);
  CLI `py -3 pipeline/wardrobe_props_tex.py [--data wardrobe/data] [--src <video>/props/tex]`, exit 1 when anything
  is missing. Each script gets `VIDEO = os.path.join(os.path.dirname(ROOT), "12tails-video")`.

- [ ] **Step 1: Write the failing tests** in `pipeline/test_wardrobe_props_tex.py` (temp folders):
  - `test_copies_referenced_only`: `data/cat/props_weapons.json` names `a.png` and `b.png` in `nodes[].mats[].tex`,
    `src` holds `a.png`, `b.png`, `c.png` → returns `(2, [])`, `data/props/tex` holds exactly `a.png`, `b.png`.
  - `test_missing_texture_reported`: JSON names `x.png`, `src` lacks it → `(0, ["x.png"])`.
  - `test_existing_copy_kept`: `data/props/tex/a.png` already there (different bytes) → not overwritten, count 0.
- [ ] **Step 2: Run** `py -3 -m unittest pipeline.test_wardrobe_props_tex -v` → FAIL (module missing).
- [ ] **Step 3: Implement** `copy_prop_textures` (walk `data/*/props_*.json`; textures under `data/props/tex/`).
- [ ] **Step 4: Run** the same → 3 PASS.
- [ ] **Step 5: The page and publish:** `index.html:701` → ``texLoader.load(`${DATA}props/tex/${m.tex}`)``; drop
  the "prop textures" rewrite in `wardrobe_publish.py` (and its docstring line); in `test_wardrobe_publish.py` the
  fixture page uses `${DATA}props/tex/`, line 859 stays, line 877's anchor list loses the prop-texture anchor.
- [ ] **Step 6: Sibling reads, own writes:** `wardrobe_data.py`, `wardrobe_icons.py`, `wardrobe_ui_assets.py`,
  `wardrobe_placements.py` (ASSETS), `wardrobe_tot.py` (ASSETS) read through `VIDEO`; `wardrobe_tot.PTEX` =
  `wardrobe/data/props/tex`; `wardrobe_placements.CFG` = `<ROOT>/tto_config`; `wardrobe_data.py` ends by calling
  `copy_prop_textures(OUT, VIDEO/props/tex)` unless `--no-props`. Docstrings say so.
- [ ] **Step 7: Run** `py -3 -m unittest pipeline.test_wardrobe_publish pipeline.test_wardrobe_props_tex` → all PASS;
  `git grep -n "\.\./props\|\.\./fonts"` → only the publish guard's message and the docstrings of old behaviour, none
  in code paths.
- [ ] **Step 8: Commit** `wardrobe: prop textures in its own data (data/props/tex, the published copy's path); the
  scripts read the video folder as their sibling and never write there`.

### Task 3: `adopt_from_video.ps1`

**Files:**
- Create: `pipeline/adopt_from_video.ps1`

**Interfaces:**
- Consumes: `pipeline/wardrobe_props_tex.py` (Task 2).
- Produces: `powershell -ExecutionPolicy Bypass -File pipeline\adopt_from_video.ps1 [-Video <path>] [-SetAside]
  [-DryRun] [-NoShortcut]`. Default `-Video` = sibling `12tails-video`. Moves, in order, each only if the source
  exists and the target does not: `wardrobe\data`, `wardrobe_dist`, `wardrobe_dist_report.json`,
  `wardrobe_dist_report.prev.json`, `.superpowers\sdd\2026-11-07-wardrobe-online`. `-SetAside`: the target
  `wardrobe\data` must already exist (else stop: "restore wardrobe_data.tar first"); the video's `wardrobe\data` is
  renamed to `<video>\wardrobe_data_old`. Then runs the props copy, repoints `Desktop\12 Tails Wardrobe.lnk` to
  `<wardrobe>\wardrobe.cmd` (working folder `<wardrobe>`), and removes `<video>\wardrobe` only if empty. Exit 1 at the
  first failure, printing moved / not moved.

- [ ] **Step 1: Write it**, with `-DryRun` printing each planned move and refusal.
- [ ] **Step 2: Scratch test** under the session scratchpad: fake `video\` and `wardrobe\` trees (small files) →
  (a) a normal run moves all five and leaves `video\wardrobe` with only a tracked-looking `index.html`;
  (b) re-run → every item refused, nothing changed, exit 0 with "already in place";
  (c) `-SetAside` with an empty target → stops with the restore message, nothing moved;
  (d) `-SetAside` with a filled target → old copy renamed to `wardrobe_data_old`;
  (e) a file in the source held open (`[IO.File]::Open(...)` in the same session) → stops, prints moved / not moved.
  Use `-NoShortcut` for all scratch runs.
- [ ] **Step 3: Commit** `wardrobe: adopt_from_video.ps1 moves the untracked data in (home) or sets the old copy aside
  (office), repoints the shortcut`.

### Task 4: The two repos' docs, and the video side's readers (working tree only)

**Files:**
- Create (wardrobe): `CLAUDE.md`, `NOTES.md`
- Modify (video): `pipeline/skins.py:25`, `pipeline/skitlib.py:432,451` (+ a `WARDROBE` constant), 
  `pipeline/extract_tto_props.py:44`, `pipeline/trailer_common.py:15`, `pipeline/transfer_to_drive.ps1` (drop
  `-WardrobeOnly` and the `wardrobe\data` entry), `CLAUDE.md` (the wardrobe paragraph), `NOTES.md` (sections out,
  pointer in); delete the 23 moved tracked files and `plans/wardrobe_split_*.md`

**Interfaces:**
- Produces (video): `skitlib.WARDROBE = os.path.join(os.path.dirname(ROOT), "12tails-wardrobe")`;
  `trailer_common.WARDROBE_DIST = ROOT.parent / "12tails-wardrobe" / "wardrobe_dist"`.

- [ ] **Step 1: Check the peer's state first:** `git -C D:/12tails-video status --short`; any of the files above
  modified by someone else → message `12tails-video-18` and wait, or stage only this task's hunks (the HEAD-based
  staging used for NOTES.md earlier today).
- [ ] **Step 2: Wardrobe `NOTES.md`:** the sections "Wardrobe app", "ToT student outfits in the LOCAL wardrobe",
  "Online copy" and the wardrobe-only session-log entries, text unchanged except commands / paths now under
  `D:\12tails-wardrobe` (the deploy: `--assets D:\12tails-wardrobe\wardrobe_dist`); a top note "split from
  12tails-video on 2026-11-09; older mixed history is in that repo's NOTES.md".
- [ ] **Step 3: Wardrobe `CLAUDE.md`:** per the design's "The wardrobe's CLAUDE.md" bullet.
- [ ] **Step 4: Video side:** the edits listed above; video `CLAUDE.md` paragraph → "the wardrobe has its own repo
  (`D:\12tails-wardrobe`, GitHub `12tails-wardrobe`); never edit it from here; the trailer and the office fallbacks
  only read it"; video `NOTES.md` keeps a two-line pointer where the sections were.
- [ ] **Step 5: Verify (pre-cutover):** `git -C D:/12tails-video grep -n -i "wardrobe[/\\\\]data\|wardrobe_dist"`
  → only the readers above, all through `WARDROBE` / `WARDROBE_DIST` / the sibling path. Nothing committed yet.

### Task 5: Cutover on the home PC, verify, commit, push

- [ ] **Step 1: Hold the peer:** message `12tails-video-18`: no skit builds or trailer runs until released (the data
  moves now); wait for its reply.
- [ ] **Step 2: Adopt for real:** `powershell -ExecutionPolicy Bypass -File D:\12tails-wardrobe\pipeline\adopt_from_video.ps1`
  → five items moved, props copy `missing: 0`, shortcut repointed.
- [ ] **Step 3: Verify the wardrobe:**
  - `py -3 -m unittest pipeline.test_wardrobe_publish pipeline.test_wardrobe_props_tex` → PASS.
  - `uv run --no-project --with playwright python -I pipeline/wardrobe_moves_check.py D:/12tails-wardrobe checks/split`
    → its pass line.
  - A headless load of the local page (served from `D:\12tails-wardrobe` like `wardrobe.cmd`) on a class with props:
    no 404 and no page error.
  - `py -3 pipeline/wardrobe_publish.py --out wardrobe_dist_new` then `diff -r wardrobe_dist wardrobe_dist_new` → no
    differences; delete `wardrobe_dist_new` and its reports.
- [ ] **Step 4: Verify the video side:** the 53 trailer tests (`uv run --no-project --with playwright --with pillow
  --with numpy --with soundfile --with scipy python -m unittest pipeline.test_trailer`) → OK; background Blender
  `import skitlib; print(skitlib.tto_placement("cat", "Head", "default"))` → a placement, not an error;
  `py -3 -c` on `skins.py`'s `WARDROBE_FACES` → an existing folder.
- [ ] **Step 5: Commit and push both:** wardrobe (`wardrobe: CLAUDE.md, NOTES.md (its sections from 12tails-video)`)
  → `git push -u origin main`; video (`wardrobe: moved to its own repo 12tails-wardrobe (D:\12tails-wardrobe); the
  trailer, skitlib, skins and extract_tto_props read it as the sibling folder`) staging only this work → `git push`.
- [ ] **Step 6: Release the peer** with the new paths (`WARDROBE_DIST`, `skitlib.WARDROBE`).

### Task 6: Transfer step, Bible pointer, office steps

**Files:**
- Create (wardrobe): `pipeline/transfer_to_drive.ps1`
- Modify (Bible): `D:\12tails\.claude\skills\bible-hub-tools\SKILL.md:71,75`

**Interfaces:**
- Produces: `powershell -ExecutionPolicy Bypass -File pipeline\transfer_to_drive.ps1 -Drive <letter> [-Dest <folder>]`
  → `<drive>:\12tails-wardrobe-transfer\wardrobe_data.tar` (`wardrobe\data`, prop textures included, under 4 GB),
  `12tails-wardrobe.bundle` (`git bundle --all`), `README.txt` with the office restore steps. `-Dest` for tests.

- [ ] **Step 1: Write it**; test with `-Dest` in the scratchpad: tar lists `wardrobe/data/meta.json` and
  `wardrobe/data/props/tex/`; delete the test output after.
- [ ] **Step 2: Commit + push** `wardrobe: transfer_to_drive.ps1 (data tar + bundle + restore steps)`.
- [ ] **Step 3: Bible:** SKILL.md lines 71 / 75 name `D:\12tails-wardrobe` (office `C:\work\12tails-wardrobe`, GitHub
  `12tails-wardrobe`), commit `docs: the wardrobe has its own repo now (12tails-wardrobe)`. Not pushed.
- [ ] **Step 4: Office steps for LINE** (plain text, no markdown): run the transfer when the drive is plugged in
  (Claude runs it given the letter); office: close everything, check `git status`, `remote set-url` to
  `12tails-video`, `git pull`, `move_project.ps1 -DryRun` then real, `git clone
  https://github.com/jumpptty/12tails-wardrobe.git C:\work\12tails-wardrobe`, `tar -xf <drive>\12tails-wardrobe-transfer\wardrobe_data.tar -C C:\work\12tails-wardrobe`,
  `adopt_from_video.ps1 -SetAside`, open `wardrobe.cmd`.
