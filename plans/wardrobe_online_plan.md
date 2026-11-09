> **Moved here from the Bible repo** (`d:\12tails\docs\superpowers\plans\2026-11-07-wardrobe-online.md`, 2026-11-09): the wardrobe lives in this repo. The text is unchanged: `D:\12tails-video\comic-skit` is this root since the 2026-11-08 move, and its decision log is `.superpowers\sdd\2026-11-07-wardrobe-online\progress.md` here (untracked; the hub mirror art and its `art\HOW.md` stay in the Bible).

# Wardrobe Online Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Put the existing local 12 Tails Wardrobe (`D:\12tails-video\comic-skit\wardrobe\`) online on its own free host and open it from a new Bible menu tool.

**Architecture:** A publish script builds a clean copy of the wardrobe (page + data in a content-hashed folder, comic-skit-only parts removed, cache headers) into `wardrobe_dist\`, checks it against Cloudflare Pages' limits and against case-sensitive paths, and the user deploys it with `wrangler pages deploy`. The Bible gets one new TOOLS entry whose launcher links open that URL in a new tab; no wardrobe code or data enters `index.html` or `assets.js`.

**Tech Stack:** Python 3 (publish script, `py -3`), the wardrobe's existing three.js r160 page (jsDelivr importmap, unchanged), Cloudflare Pages direct upload (`npx wrangler`), the Bible's scratch-script patching + `node scripts/validate_skills.js`.

**Spec:** none. The user skipped the questions ("plan go", 2026-11-07); the findings this plan argues from are in the chat of that day: Bible download = `assets.js` 31 MB (20 MB gzip) + `index.html` 7.4 MB (1.9 MB gzip); GitHub Pages = 1 GB site, 100 GB/month soft bandwidth; wardrobe data = 277 MiB in 6,465 files (JSON 129.5 MB / 80 files, WebP 114.2 MB / 6,127, mesh `.bin` 33.3 MB / 257; largest file `all/props_trinkets.json` 8.8 MB); one class's JSON = 25 MB raw / 4.9 MB gzip; meshes gzip to 0.36. The calls below are Claude's, not the user's, until the user confirms them.

**Two repos:** Tasks 1-3 change `D:\12tails-video\comic-skit` (its own private git repo, `jumpptty/12tails-comic-skit`; read its `NOTES.md` "Wardrobe app" first). Task 4 changes the Bible repo `d:\12tails`.

## The user's content rule (2026-11-07)

**"BB 3D models only; the only thing you may bring from TTO are face paints, 50% of their own face paints."** So the public copy holds:
- every outfit, colour / edition, weapon, headpiece, back trinket, emote and move **only where its files come from BB's client** (`D:\12tails\RippedAssets\`), never from TTO (`tto_assets\`, `D:\12tails\RippedAssets_TTO_2026-11-04\`, TTO bundles);
- item icons, class portraits, emote and skill icons **re-taken from BB's rip** (TTO's copies of BB icons are pixel-identical, but the published file must come from BB); a picture with no BB source is dropped;
- BB's own faces, plus **half of TTO's own faces per class: the first 50% by TTO face number, rounded down** (Claude's call on which half; the user may name others).
How the data marks TTO (the page's pink dot, TTO-tagged emotes, face numbering) is read from `pipeline/wardrobe_data.py`, `wardrobe_icons.py`, `wardrobe_ui_assets.py` and `wardrobe_editions.py`; anything whose source cannot be shown to be BB is left out, not guessed.

## Decisions taken without the user

1. **Which half of TTO's faces** (above): the first 50% by number.
2. **Host = a separate Cloudflare Pages project `12tails-wardrobe`** (URL `https://12tails-wardrobe.pages.dev/`), direct upload, not R2 and not the Bible's GitHub Pages: no CORS work, no 280 MB in the Bible repo, no share of GitHub's 100 GB/month. The first deploy needs the user's Cloudflare login (like the ☕ Worker).
3. **Link out, not embed:** the Bible tool opens the wardrobe in a new tab. The Bible's double-click rule stays intact; the tile simply needs internet.
4. **The public page drops "คัดลอกให้ Claude"** (a skit-pipeline tool) and keeps everything else, including "บันทึกภาพ" and the per-class loadout in `localStorage`.
5. **GoatCounter on the wardrobe page** (same account as the Bible, path `/wardrobe/`) so bandwidth can be judged from visits.

## Global Constraints

- Cloudflare Pages free plan: at most **20,000 files** per deploy and **25 MiB per file**.
- Never put wardrobe data or three.js code into `12t_projects/bible/index.html` or `assets.js`.
- Bible text in Thai; two fonts only (Prompt, JetBrains Mono + Prompt); hover = small lift / brightness, no soft gold glow.
- `index.html` is CRLF and is patched only by scratch Node scripts that back it up first (12t_projects/bible/CLAUDE.md §1); run `node scripts/validate_skills.js` before the commit and prepend a `CHANGELOG_DATA` entry with the exact commit subject.
- Scratch scripts live in the session scratchpad, never in either repo's `scripts/` folder; the publish script itself is permanent and lives in `comic-skit\pipeline\`.
- `wardrobe_dist\` is build output: kept out of git (the comic-skit `.gitignore` is a whitelist, so confirm it is not listed).
- Commit or push only when the user asks.

## Review Focus

1. **Case mismatch:** a file referenced as `Wolf_blade1R.webp` but stored as `wolf_blade1r.webp` loads on the Windows test server and 404s on Cloudflare. `--check` compares every referenced path case-sensitively (Task 1, `test_case_mismatch_is_reported`).
2. **Rebuild leaves the old data folder:** publishing twice must leave exactly one `data-*` folder, or the file count doubles toward 20,000 (Task 1, `test_republish_keeps_one_data_folder`).
3. **Removed TTO items leave dangling references:** icons, item map, sets, placements, outfit lists or emote lists that still name a removed TTO item would show broken tiles or a crash on pick (Task 1, `test_bb_only_leaves_no_references`).
4. **Stale cache after an update:** the data folder name must change whenever any data file changes, and the page must stop using `cache: "no-cache"` (Task 1, `test_hash_changes_with_content`, `test_page_rewritten`).
5. **Offline Bible:** with no internet the new tile must still render and simply fail to open, never break the menu (Task 4 validator check: the entry has no mount function and links with `target="_blank"`).

---

### Task 1: Publish script with checks

**Files:**
- Create: `D:\12tails-video\comic-skit\pipeline\wardrobe_publish.py`
- Create: `D:\12tails-video\comic-skit\pipeline\test_wardrobe_publish.py`

**Interfaces:**
- Consumes: the wardrobe folder layout (`wardrobe/index.html`, `wardrobe/data/**`, `const DATA = "data/";` at `wardrobe/index.html:135`, `fetch(p, { cache: "no-cache" })`, the "คัดลอกให้ Claude" button at `:120` and its handler). How the data marks a TTO item: read `pipeline/wardrobe_data.py` / `wardrobe_icons.py` (the page shows a pink dot for TTO).
- Produces: `publish(src: Path, out: Path, bb_rip: Path) -> dict` (returns `{"files": int, "bytes": int, "data_dir": str, "dropped": {kind: [names]}, "tto_faces": {cls: [numbers]}}`), always applying the content rule above; `check(out: Path) -> list[str]` (problems, empty = fine); CLI `py -3 pipeline/wardrobe_publish.py [--out wardrobe_dist] [--bb-rip D:\12tails\RippedAssets\ExportedProject\Assets\Resources]` (publish, write `wardrobe_dist_report.json` beside the output with every dropped item and kept TTO face, then check, exit 1 on problems) and `--check <dir>`.

- [ ] **Step 1: Write the failing tests** (`test_wardrobe_publish.py`, plain `unittest`, each builds a tiny fake wardrobe in a temp dir: an `index.html` containing the three strings above, `data/meta.json`, `data/cat/outfits.json` naming `tex/a1.webp`, `o_a.bin`, one TTO-flagged outfit, one TTO-tagged emote, four TTO-own faces and two BB faces, plus a fake BB rip holding the BB icons):
  - `test_page_rewritten`: output `index.html` has `const DATA = "data-<10 hex>/";`, no `no-cache`, no `คัดลอกให้ Claude`, one GoatCounter script with `data-goatcounter-settings` path `/wardrobe/`, and a link to `https://jumpptty.github.io/12tails/12t_projects/bible/`.
  - `test_hash_changes_with_content`: changing one byte of one data file changes `data_dir`.
  - `test_republish_keeps_one_data_folder`: two `publish()` calls into the same `out` leave exactly one `data-*` folder.
  - `test_headers_file`: `_headers` gives `/data-*/*` `Cache-Control: public, max-age=31536000, immutable` and `/` `Cache-Control: no-cache`.
  - `test_case_mismatch_is_reported`: a reference `tex/A1.webp` to a stored `tex/a1.webp` makes `check()` return a problem naming both.
  - `test_limits_reported`: a 26 MiB file, and 20,001 files (sparse empty files are fine), each produce a problem.
  - `test_bb_only_leaves_no_references`: the TTO outfit and the TTO emote are gone (files and every JSON mention), the report lists them under `dropped`.
  - `test_tto_faces_first_half`: of four TTO-own faces numbered 30-33 the output keeps 30 and 31, both BB faces stay, `tto_faces` = `{"cat": [30, 31]}`; with three TTO faces only the first is kept.
  - `test_icons_from_bb_rip`: a published icon's bytes equal the fake BB rip's file, and an icon with no BB source is dropped (and its tile reference removed).

- [ ] **Step 2: Run them, expect failures**
  Run: `cd /d D:\12tails-video\comic-skit && py -3 -m unittest pipeline.test_wardrobe_publish -v`
  Expected: FAIL / ERROR (module not found).

- [ ] **Step 3: Implement `publish` and `check` in `pipeline/wardrobe_publish.py`**
  Hash = first 10 hex of SHA-256 over the sorted relative paths and bytes of `data/**` (after the `--no-tto` filter); copy with `shutil.copy2`; delete any previous `data-*` before copying; rewrite the page by exact string replacement and fail loudly if any of the three anchors is missing (the page may have changed). `check` walks the referenced paths the page builds (`<cls>/tex/<name><color><edition>.webp`, `<cls>/faces/<n>.webp`, `<cls>/o_<name>.bin`, icon paths in `icons.json` / `ui.json`) from the JSON, compared case-sensitively with `os.listdir` names.

- [ ] **Step 4: Run the tests, expect PASS**
  Run: `py -3 -m unittest pipeline.test_wardrobe_publish -v`

- [ ] **Step 5: Publish the real wardrobe and read the report**
  Run: `py -3 pipeline/wardrobe_publish.py --out wardrobe_dist`
  Expected: exit 0, about 6,4xx files, about 280 MB, no problems. Any case-mismatch problem is fixed in the data builder (`wardrobe_data.py`), not by renaming in `wardrobe_dist`.

- [ ] **Step 6: Commit (comic-skit repo, when the user asks)**
  `git add pipeline/wardrobe_publish.py pipeline/test_wardrobe_publish.py` then commit `wardrobe: publish script for the online copy (hashed data folder, Cloudflare limits, case check)`.

### Task 2: Check the built copy in a browser

**Files:** none changed (fixes go back to Task 1).

**Interfaces:**
- Consumes: `wardrobe_dist\` from Task 1.

- [ ] **Step 1: Serve it the way Cloudflare will (case-sensitive is not reproducible on Windows; Task 1's check covers it)**
  Run: `py -3 -m http.server 8772 --bind 127.0.0.1 --directory wardrobe_dist` (background).
- [ ] **Step 2: Load it in Playwright** (an isolated context; screenshots under `d:\12tails\.playwright-mcp\`, deleted afterwards): open `http://127.0.0.1:8772/`, pick two classes, change outfit, colour, face and a weapon.
  Expected: no console errors, no 404 in the network log, every data request under `/data-<hash>/`, the Bible link present, no "คัดลอกให้ Claude", no pink TTO dot on any tile, the TTO emotes absent, the face picker showing BB faces plus only the kept TTO faces.
- [ ] **Step 3: Stop the server** (TaskStop on its task id).

### Task 3: First deploy to Cloudflare Pages (the user runs the login step)

**Files:**
- Modify: `D:\12tails-video\comic-skit\NOTES.md` (new subsection under "Wardrobe app": "Online copy" with the URL, the publish and deploy commands, the TTO decision)

**Interfaces:**
- Consumes: `wardrobe_dist\`; the user's Cloudflare login (never taken by Claude).
- Produces: the live URL `https://12tails-wardrobe.pages.dev/` for Task 4.

- [ ] **Step 1: Show the user `wardrobe_dist_report.json`** (what was dropped, which TTO faces were kept) and get their go for the upload.
- [ ] **Step 2: The user creates the project and deploys**
  `cd /d D:\12tails-video\comic-skit && npx wrangler pages project create 12tails-wardrobe --production-branch main` then `npx wrangler pages deploy wardrobe_dist --project-name 12tails-wardrobe --branch main --commit-dirty=true` (`--branch main` is required: without it wrangler takes the branch of the current folder's git repo and a non-`main` checkout makes a silent preview deploy).
- [ ] **Step 3: Verify the live copy**
  Run: `curl -sI https://12tails-wardrobe.pages.dev/` (200, `cache-control: no-cache`) and `curl -sI -H "Accept-Encoding: br, gzip" https://12tails-wardrobe.pages.dev/data-<hash>/cat/clips.json` (200, `cache-control: public, max-age=31536000, immutable`, a `content-encoding`). Then the Task 2 Playwright pass against the live URL, once at desktop size and once at 390 x 844 (phone: does the picker leave the 3D view visible, do the Thai button labels fit, does opening a picker pop the on-screen keyboard), and a GoatCounter check that `/wardrobe/` counted the visit.
- [ ] **Step 4: Write the NOTES.md subsection** (URL, `wardrobe_publish.py` + `wrangler pages deploy` commands, redeploy after every `wardrobe_data.py` run, the user's content rule word for word).

### Task 4: Bible menu tool that opens the wardrobe

**Files:**
- Modify: `d:\12tails\12t_projects\bible\index.html` (the `TOOLS` array at `const TOOLS = [` ~line 31612; `mountLauncher`'s stage CTA, filmstrip thumb, phone grid tile and art link; `route()`), via one scratch Node patch script
- Modify: `d:\12tails\scripts\validate_skills.js` (new check `[LAUNCH LINK ERROR]`)
- Modify: `d:\12tails\.claude\skills\bible-hub-tools\SKILL.md` (a short "Wardrobe (external tool)" section)

**Interfaces:**
- Consumes: the live URL from Task 3.
- Produces: TOOLS entry `{ id: "wardrobe", title: "ตู้เสื้อผ้า", shortTitle: "ตู้เสื้อผ้า", category: "", href: "https://12tails-wardrobe.pages.dev/", art: <an existing TOOL_ART portrait key> }`; a launcher rule "a tool with `href` links there with `target="_blank" rel="noopener"` everywhere the launcher builds `#<id>` links, and `route()` never mounts it".

- [ ] **Step 1: Write the failing validator check `[LAUNCH LINK ERROR]`** in `scripts/validate_skills.js`, next to the other launcher checks: every TOOLS entry with `href` has an `https://` URL, no mount function, and the launcher markup built for it (stage, thumb, grid tile, art link) uses that URL with `target="_blank"` and `rel="noopener"`, never `#wardrobe`; and the TOOLS list contains the `wardrobe` entry.
- [ ] **Step 2: Run it, expect `[LAUNCH LINK ERROR]`**
  Run: `node scripts/validate_skills.js`
- [ ] **Step 3: Patch `index.html`** (one scratch script, backup first, CRLF anchors, dry run then write): add the entry after the existing tools (not one of the two main tools, so no wax seal), and teach the launcher's link builders the `href` rule. Art: reuse a `TOOL_ART` portrait (placeholder until the user picks art, as Special Pet Info did).
- [ ] **Step 4: Run the validator, expect SUCCESS**
  Run: `node scripts/validate_skills.js`
- [ ] **Step 5: Update the skill doc** (`bible-hub-tools`): the entry, the `href` rule, where the wardrobe lives and how it is published (pointer to comic-skit `NOTES.md` "Online copy").
- [ ] **Step 6: Changelog + commit (when the user asks)**
  Prepend `CHANGELOG_DATA` entry and commit `feat(bible): ตู้เสื้อผ้า menu tool opens the online 12 Tails Wardrobe` with `index.html`, `scripts/validate_skills.js`, the skill doc.

### Task 5: Emotes loop endlessly (user 2026-11-07, runs before Task 3)

User: "Please make all emotes loop endlessly too."

**Files:**
- Modify: `D:\12tails-video\comic-skit-wardrobe-online\wardrobe\index.html` (`play()`, the `const loop = ...` line, ~514)
- Create (not tracked): the junction `D:\12tails-video\comic-skit-wardrobe-online\wardrobe\data` → `D:\12tails-video\comic-skit\wardrobe\data`, so the worktree's `wardrobe\` is a complete publish source

**Interfaces:**
- Consumes: Task 1's CLI (`--src`, `--out`) and its three page anchors (unchanged by this edit).
- Produces: every clip whose `group` is `"emote"` plays with `THREE.LoopRepeat` until another move is picked (no return to idle); `"base"` and `"skill"` clips keep their current rule (`loop` flag or `root`).

- [ ] **Step 1: Confirm the junction target is git-ignored in the worktree** (`git check-ignore -v wardrobe/data/meta.json` prints a rule), then create it (`cmd //c mklink /J wardrobe\data D:\12tails-video\comic-skit\wardrobe\data` from the worktree).
- [ ] **Step 2: Edit `play()`** so `loop` is also true when `C.clipsData[name].group === "emote"`.
- [ ] **Step 3: Republish from the worktree**: `py -3 pipeline/wardrobe_publish.py --src D:/12tails-video/comic-skit-wardrobe-online/wardrobe --out D:/12tails-video/comic-skit/wardrobe_dist`; expected exit 0, check clean, the same data folder name as before (data unchanged), and the output page contains the new condition. `py -3 -m unittest pipeline.test_wardrobe_publish -v` still passes.
- [ ] **Step 4: Verify in a browser** (Playwright, isolated context, the Task 2 serving recipe): play the emote `wave` (and one more emote) and, after more than twice its clip duration, `window.wardrobe.debug()` still reports it as the current move and its action is running; a base move still returns to idle.
- [ ] **Step 5: Commit** in the worktree: `wardrobe: emotes loop until another move is picked`.

### Tasks 7-9 (user 2026-11-07, after the first deploy): "Do all your suggested fix", "Restyle the palette of the App to match 12TailsBible premium Brand", mirrored / off-centre face icons

All three change `wardrobe/index.html` in the comic-skit worktree (branch `wardrobe-online`, which `main` now fast-forwards to), so they run one after another. Local preview without a junction: `py -3 <scratchpad>/devserve.py D:/12tails-video/comic-skit D:/12tails-video/comic-skit-wardrobe-online 8773` serves the main checkout but takes every `wardrobe/` file except `wardrobe/data/` from the worktree; open `http://127.0.0.1:8773/wardrobe/` (full local data, TTO items included). Visual checks with Playwright are expected for these tasks (comic-skit project, not the Bible).

**Task 7: phone layout** (live check findings, 390 x 844). At widths up to 760 px: the picker opens as a bottom sheet (about half the screen) and the 3D model stays fully visible above it while the sheet is open, picking keeps it open, its ✕ is always on screen (also after scrolling); on touch devices (`(hover: none), (pointer: coarse)`) no picker focuses its search input on open; the top-bar labels fit on one line at 360 px and up (shorter labels or icons with the full name as `title` / `aria-label`); the ของประดับหลัง tile's label and ring stay inside the tile; at 390 x 844 and 360 x 740 the page does not scroll (document height <= viewport height). Desktop (1366 x 768 and up) looks and behaves as before. Verify with Playwright metrics (scrollHeight vs innerHeight, label element heights, `document.activeElement` after opening each picker with touch emulation, the picker's rect against the visible canvas area) plus screenshots at 390 x 844, 360 x 740 and 1366 x 768.

**Task 8: Bible brand palette.** Restyle the page with the Bible's dark "Ledger" tokens (from `12t_projects/bible/index.html`, `:root[data-theme="dark"]`): ink `#150f0c`, panel `#1f1712`, panel-2 `#271c15`, line `#4a3a26`, text `#ece4d6`, muted `#b0a189`, gold `#c9a227`, gold-soft `rgba(201,162,39,.14)`, seal (oxblood) `#c2503c`, shadow `0 1px 2px rgba(0,0,0,.5), 0 20px 44px -22px rgba(0,0,0,.75)`; brand basics in `12t_projects/bible/CLAUDE.md` §2 ("Ledger" design system, hover = a small lift or brightness and never a gold glow, two fonts only: Prompt, and `'JetBrains Mono','Prompt',monospace` for numbers). Colours become CSS custom properties on `:root`; selected states, rings and focus use gold; the TTO pink dot stays pink (it marks TTO content). Text contrast at least 4.5:1 on its background. Verify with screenshots at 1366 x 768 and 390 x 844 for the user.

**Task 9: face icons. CANCELLED by the user (2026-11-07: "actually, let's skip the face job"); nothing was changed.** Some classes (the user named Mole and Penguin) draw the face mirrored on the 3D model, so their face tiles look the other way round; other icons (Wolf) are off centre in the ring. Find, per class, whether the in-game face is mirrored relative to the overlay image (from the outfit mesh's face UVs, confirmed by comparing a 3D close-up with the tile), and recompute each class's face crop so the face features sit centred in the circular icon. The pipeline stays the source of truth: `pipeline/wardrobe_ui_assets.py` writes the result into `data/ui.json` (`faceBox` per class plus a new per-class mirror flag, e.g. `faceMirror: ["mole", "penguin", ...]`), back up `D:/12tails-video/comic-skit/wardrobe/data/ui.json` before regenerating it, and the page mirrors the tile image (`transform: scaleX(-1)` or equivalent) for those classes. The publish script must carry the new field into the public copy (test). Verify every class with a side-by-side screenshot of the face tiles and the 3D face.

**Task 10: download a piece's texture, try your own skin** (user 2026-11-07: "allow user to download the texture of the gear pieces, and upload their own texture to for trying out skins (most user just use GPT generated image to reskin the original)"). For every worn piece (outfit, main and second weapon, headpiece, back trinket): a download button saves that piece's texture as shown (outfit: the current colour / edition) as a lossless PNG in its original UV layout, named `<class>_<piece>_<colour>.png`; an upload button takes an image file (PNG / JPEG / WebP, any size), scales it to the original texture's size (a short Thai notice when the aspect ratio differs), and applies it to that piece only; on an outfit the face is still composed on top with the page's face-block rule; a reset button returns the piece to its own texture. A piece with several textures offers each one. Custom skins are kept per piece for the visit (switching away and back keeps them; reload clears them) and never leave the visitor's browser (no network request carries them). Buttons sit in the picker header of the piece's topic, with Thai labels ดาวน์โหลดลาย / อัปโหลดลาย / คืนลายเดิม and the same Ledger styling; they fit the Task 7 phone layout. Verify with Playwright: a downloaded PNG's size equals the texture's; a test image uploaded to the outfit and to a weapon shows on the model (screenshot), the face still drawn on the outfit; reset restores; no request is sent when uploading (network log); headed-Chrome sizes as in Task 8.

**Task 11: left-panel layout** (user 2026-11-07, runs after Task 9 and before Task 10): "1 = Class, Color, Face; 2 = Gear Set (use entire row) and stylize it to hint that it is special; 3 = หมวก + ชุด; 4 = อาวุธ 1 + 2; 5 = ประดับ + ท่าทาง". Row 1 holds three tiles: อาชีพ, a new สี topic (the character colour: its ring shows the current colour, its picker shows what each colour and, where the outfit has them, each R / V edition looks like; the colour bar moves out of the set picker so colour has one home), หน้า. Row 2 is the ชุดเซ็ต tile across the full width, styled as special with the Bible's gilded frame (double gold line with L corners; Bible `--cg-gild`, `border-image`) and the current set's piece icons in a row, no glow. Rows 3-5 as the user listed. The phone layout keeps the same row order with compact tiles and still fits 390x700 and 360x620 without scrolling; desktop fits 1366x607 and 1920x919 without scrolling. Undo / redo, sets and colours behave as before (colour changes stay undoable).

**Task 12: WASD camera** (user 2026-11-07: "add a simple aswd control to, the way I love for the reach preview in the skill-details tool"; runs after Task 10). Copy the reach preview's feel (Bible `12t_projects/bible/index.html` ~12139-12170, `.claude/skills/bible-skill-page-ui/SKILL.md` "keyboard (user 2026-10-13)"): W / S move the look-at point forward / back along the view direction on the ground plane, A / D strafe; the camera moves with it (orbit distance and angles unchanged); speed 0.3 view-widths per second scaled by the current zoom distance; eased (target lerp 0.12 per frame) with a requestAnimationFrame loop that stops when settled; keys read by `e.code` so a Thai layout works; ignored with Ctrl / Meta / Alt held and while focus is in a text field (the picker search box); held keys cleared on window blur; the mouse still orbits and zooms; มุมกล้องเริ่มต้น (and double-click on the stage, if it resets today) also resets the pan. A small "WASD" hint over the stage on devices with a keyboard and mouse (hidden on touch), readable on the white stage. Verify with Playwright: holding W for 1 s moves the camera target forward by about the expected distance and the view settles after release; typing w in the search box moves nothing; reset returns the target; headed-Chrome sizes.

After Task 12: republish (`--src D:/12tails-video/comic-skit-wardrobe-online/wardrobe --data D:/12tails-video/comic-skit/wardrobe/data --out D:/12tails-video/comic-skit/wardrobe_dist`), local check of the dist, the user reviews and deploys.

## Not in this plan (separate work)

- **Split `assets.js` per container** so a small icon change stops re-sending 20 MB: its own plan.
- **Deep links** from class guide sets / item tooltips into the wardrobe (`#<class>/<outfit>`): after the online copy has run for a while.
- **Shrinking the data** (binary clips instead of 8 MB JSON per class): only if visits show bandwidth matters; Cloudflare already serves the JSON compressed.
