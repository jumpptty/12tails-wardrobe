# Handoff between the two PCs

Steps one PC left for the other. A session reads this at the start, does what is listed for its PC (where the user's
go-ahead is needed, says so), and deletes each item once it is done. Empty = nothing pending.

## Either PC: community skins, the deploy

Built and tested 2026-11-11 (NOTES.md "community skins"). The one-time setup was done 2026-11-12 at the office (NOTES.md
"community skins: setup done"): channel `#wardrobe-submissions` (id 1570242267397230764, the user's "Jump" server), its
webhook, the bot app "12 Tails Skins" (in the server, allowed in the channel, Message Content Intent on), the Turnstile
widget (site key in `wardrobe/community_config.json`), and both Worker secrets. Deployed 2026-11-12 (d1380e15) and a
test skin sent from the live site ("ทดสอบระบบ", the Sheep's mothLatern), approved, imported, published and deployed
(a37d6a66): the lantern's menu shows ลายจากผู้เล่น 1 and it wears with the credit. Since 2026-11-12 the site reads the
approvals live (NOTES.md "community skins live from Discord"; both bot secrets set, the live page loads the list and
the picture from /api/community). Left: when the user takes the test skin's ✅ away it leaves the site within a minute;
then run the PC import once (so the data's fallback community.json drops it too), publish, deploy, commit. Delete this
item.

## Either PC: a live test of a whole look

Deployed 2026-11-12 (065f1bf4). Send one 2-piece look from the live site (ส่งลุคนี้), approve it in Discord, check it in
the ลายผู้เล่น card; if Discord refuses a big look ("upstream"), lower LIMITS.setBytes in site_worker.mjs.
## Home PC: the bot's token file (once, the user)

The import (`pipeline/wardrobe_community.py`) needs `%APPDATA%\12tails-wardrobe\discord.json` on this PC too; the office
has it. The token never goes in git: carry the file from the office PC (USB / a private message to yourself), or reset
the token on discord.com/developers → 12 Tails Skins → Bot (then the office's copy needs the new one too). Content:
`{"token": "<bot token>", "channel": "1570242267397230764"}`. Delete this item when done.

## Either PC: the Bat skin after the helmeted enemy, to polish with the user (2026-11-13)

NOTES.md "two Bat skins after two in-game enemies" and the bullets after it; the rules are the `reskin-from-image` skill
(`/reskin-from-image`, .claude/skills/). State: outfit royal + head butterflyHood + face 11; the user called it good
("Lady Noir looks good now") up to the chest, neckline (a U), midriff and front piece; the coat's belt (island 33,
the zigzag round the back) picked 2026-11-14 at home: `BELT = "contour"` (NOTES.md "the helmeted Bat skin: finding
the coat's band"); the same day: the helmet band painted round the fringe, the coat's back = her own back panel
copied whole (`COAT_BACK = "panel"`, the pale drop gone), cloth shading on sleeves and stockings, and a 2048 px upscale
(look/royal_2x.png). The user's hair picture was tried on the hair and taken off ("for now": `HAIR_TEX = 0.0`).
Still open:
- The user's word on the passes after it (NOTES.md, the bullets up to "512 px for upload": sharp patterns, lashes).
  The file to upload is the 512 px one (user: "skin reduce to 512x512 please, that's the max game can render"):
  look/royal_512.png; look/royal_2x.png stays for the wardrobe's own preview.
- The weapon is not skinned.
- The 512 px skin is on the home Desktop (`wardrobe_reupload\lady_noir_face11\12tails_ค้างคาว_Royal.png`), not on the
  office's yet (see the names below).
- With `HAIR_TEX` > 0 the painter needs plans/reskins/bat/hair_ref.png (the user's picture, not in git; on the home
  PC). The upscale (`py -3.10 pipeline/wardrobe_skin_upscale.py`) runs on the home PC only (torch + CUDA).
- The sharp patterns need plans/reskins/bat/ref/LadyNoir_x4.png (her sheet upscaled twice, home PC only:
  `py -3.10 pipeline/wardrobe_skin_upscale.py plans/reskins/bat/ref/LadyNoir.png .../LadyNoir_x2.png --bits 8`, then
  x2 -> x4 the same way). Without it the painter runs on the small sheet (blurry patterns): don't rebuild
  look/royal.png at the office.
- To run (once per PC): the references are not in git (game files). Rebuild them once:
  `uv run --no-project --with UnityPy --with pillow --with playwright python -I pipeline/wardrobe_enemy_ref.py plans/reskins/bat/ref LadyNoir+NoirWand:NoirWand BatCult@x-90`
  then `uv run --no-project --with pillow --with numpy --with scipy --with playwright python -I pipeline/wardrobe_bat_enemies.py eyes`
  (the first run rasterises the maps into plans/reskins/bat/eyes/_cache, a few minutes). Live view:
  `py -3 pipeline\wardrobe_serve.py 8771`, then
  http://127.0.0.1:8771/pipeline/wardrobe_skin_live.html?cls=bat&outfit=royal&face=11&head=butterflyHood&skin=/plans/reskins/bat/eyes/look/royal.png&extra=bat%7Caccessories%7CbutterflyHood%7CBat_butterflyHood.png@/plans/reskins/bat/eyes/look/Bat_butterflyHood.png
- The user uploads skins themselves. The office Desktop has them ready (`wardrobe_reupload\`); at home copy from git
  under the names the page's drop reads: plans/reskins/bat/eyes/look/royal_512.png -> `12tails_ค้างคาว_Royal.png`,
  Bat_butterflyHood.png -> `12tails_ค้างคาว_Butterfly_Hood.png` (face 11); plans/reskins/bat/rose/look/summer.png ->
  `12tails_ค้างคาว_summer.png` (face 21, no head piece); plans/reskins/cat/knight/champion.png -> `12tails_แมว_champion.png`,
  Cat_default.png -> `12tails_แมว_default.png` (face 23).
- No deploy from this work. A deploy from either PC: from the main folder at current main (NOTES.md "The opaque-outfit
  deploy d4adea35 had two side effects").

## Home PC

- FYI: the Bible commit `0704e0f6` (reference notes on skill animations and weapon codes) was made at the office and
  not pushed; pull it there before editing those four reference files at home.

## Office PC

- Every effect builds on either PC now: TTO's (`pipeline\wardrobe_fx_tto.py`) reads the video folder's
  `tto_assets\2026-11-04` at home and, at the office, this repo's own git-ignored `tto_assets\2026-11-09` (the TTO
  install decrypted 2026-11-10; the 18 Wolf TTO effects come out identical). After a TTO patch: decrypt again into a
  new date (NOTES.md 2026-11-10 "TTO bundles at the office").

## Either PC

- **The Penguin, for the user's eye** (done overnight 2026-11-13: its effect-only tiles and QA, NOTES.md "the Penguin's
  effect-only tiles"): contact sheets `checks/fx_penguin_qa/sheets_dark|white|behind/index.html` (git-ignored, home PC);
  the open calls in `plans/fx_penguin/effect_only.md` (Mana Arc's random cage, the multiCast tint on Double / Triple
  Cast, Frost Spike with or without the Ice Shield, Dispell's screen warp left out) and decision 17 (the game hides the
  snowmanned target, never the caster: penguin.js HIDE_ONLY_ON_HERO). Optional: rebuild the Wolf and Sheep data with
  `wardrobe_fx.py` so their KO deadEffect gets the premul blend (207).

## Video repo (either PC)

- **Retire the wardrobe trailer** (user 2026-11-10: "the trailer video is already published, you may delete everything
  related to it to save space"), in a video session (that repo's rules): its frames `renders\wardrobe_trailer\` (home
  PC only, the space; not on the office PC), `pipeline\trailer_*.py` + `test_trailer.py`, `plans\trailer_*.json`,
  `plans\wardrobe_trailer_*.md`, `captions\wardrobe_trailer\`, `renders\yt_shorts\wardrobe_trailer\`; check `music_*.py`
  and anything else only the trailer uses. The wardrobe no longer keeps `window.wardrobe` working for it.

## Next up (either PC)

- **Effects + sounds: the run is complete (2026-11-14)**: all twelve classes are built, committed and live (Wolf,
  Sheep, Penguin, Bat, Bison, Cat, Chameleon, Mole, Monkey, Panda, Rabbit, and the Whale, built at home; NOTES.md "the
  Whale's effects: built and cued"). Nothing to rebuild on either PC: pull. For the user's review: every class's
  `plans/fx_<cls>/decisions.md` (decided overnight / unattended) and the QA contact sheets
  `checks/fx_<cls>_qa/sheets_dark|white/index.html` (git-ignored: Mole to Rabbit's are on the office PC, the Whale's
  on the home PC, with `sheets_ground` before and `sheets_fix` after its floor clip). The Whale, for the user's eye:
  the texture fix that came with it (the Sheep's cast ring is pink again, the Bat's Phantom Bane ray is the zigzag);
  the knights' lance trails zigzag while guarding; Honor's emblem sits over her face; Peninsula Round's rings pass
  under the floor unclipped; megalodon_ring is faint on the white stage. A Monkey TTO rebuild belongs to the office
  (the home PC's 2026-11-04 bundles lack three of its textures; `wardrobe_fx_tto.py` stops on a clash unless
  `--retex`). For the user's ear: the Monkey's sounds come from BB's resources container (every WAV in the rip's
  monkey/sounds is zero-filled). The workflow for another class or a rebuild is `pipeline/workflow_class_fx.js`
  (Workflow tool, scriptPath; args `pc: "home"` for D:/ paths, office by default).
- Settled since 2026-11-09 (no longer open): the backdrop is a manual toggle, white by default (the พื้นหลัง button);
  effects on an enemy go to the target point 10 m ahead; the user declined the Sheep's Bible findings (2026-11-10: "no need to
  offer"; they stay in NOTES.md and the reports). Still open: a game clip of Cross Break to check its stretched
  slashes.
