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

- **Done for the Wolf and the Sheep (2026-11-10, NOTES.md "one tile per skill"); the Penguin's pools split by the same
  page code already; left for the Penguin: its effect-only tiles (Mana Arc, Dispell, Frost Spike, Double / Triple Cast:
  read each RPC, add SEQ "<Name>: root@<t>" + SEQ_SKILL + cue key "@<Name>:root", build with `wardrobe_fx.py penguin
  --fx ... --voices ...`), then its QA.** The original item:
- **Every skill gets a tile, Wolf and Sheep first, then the Penguin** (user 2026-11-10: "Yes to both, but redo Wolf and
  Sheep first"; NOTES.md "skills without an animation, and the pooled tiles"): (1) one tile per skill instead of the
  pools (the Cast tile's random pick among the skills sharing cast3, cast4, blink): each tile plays the shared clip with
  that skill's cues, its own Bible icon; (2) the skills the game plays with no body animation (Penguin: Mana Arc,
  Dispell, Frost Spike; the Wolf's and Sheep's to be found: their RPCs that call no clip) get effect-only tiles on the
  idle stance, researched and cued like the rest. Then the Penguin's unfinished QA (its workflow stopped in QA).
- **The Penguin's effects: QA, the user's hand checks, then deploy** (built and cued at home 2026-11-10, NOTES.md "the
  Penguin's effects: built and cued"; the workflow's QA step over Penguin, Sheep and Wolf was cut off). The built data
  (`wardrobe/data/penguin/fx.json`, `sfx/`, `data/fx/tex/tto_*`) travels in git with the commit. Optional: rebuild the
  Wolf and Sheep data with `wardrobe_fx.py` so their KO deadEffect gets the new premul blend (207); until then it stays
  additive (look at it on the white stage). Deploy only when the user asks.

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
