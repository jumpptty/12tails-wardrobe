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

- **Effects + sounds: continue with the Mole, then Monkey, Panda, Rabbit, Whale** (stopped by the user 2026-11-13 07:05,
  "stop here for now, push and deploy all progress"; the run is `plans/goal_fx_all_classes.md`, NOTES.md "every class's
  skill effects: the run"). Done, committed and live: Wolf, Sheep, Penguin, Bat, Bison, Cat, Chameleon. The Mole: its
  research is done and verified (`plans/fx_mole/*.md`), and its build's planner wrote `plans/fx_mole/decisions.md`
  (63 decisions, decided overnight); the builders, editor and QA had not started, so nothing of the Mole is in the page or
  the data yet. Next: the Mole's build (planner output can be reused: give the builders its groups again, or re-plan),
  then for each of Monkey, Panda, Rabbit, Whale the research and the build, each class committed + published + deployed
  when its gate passes. The workflow is `class-fx` as NOTES.md describes it (re-create it in a new session). For the
  user's review: every class's `plans/fx_<cls>/decisions.md` (decided overnight) and the QA contact sheets
  `checks/fx_<cls>_qa/sheets_dark|white/index.html` (git-ignored, home PC).
- Settled since 2026-11-09 (no longer open): the backdrop is a manual toggle, white by default (the พื้นหลัง button);
  effects on an enemy go to the target point 10 m ahead; the user declined the Sheep's Bible findings (2026-11-10: "no need to
  offer"; they stay in NOTES.md and the reports). Still open: a game clip of Cross Break to check its stretched
  slashes.
