# Handoff between the two PCs

Steps one PC left for the other. A session reads this at the start, does what is listed for its PC (where the user's
go-ahead is needed, says so), and deletes each item once it is done. Empty = nothing pending.

## Either PC: community skins, the user's setup (once), then a deploy

Built and tested 2026-11-11 (NOTES.md "community skins"); not deployed yet. The user's steps, in order (Claude never
sees the secrets):
1. **Discord:** a private channel for submissions. Channel settings → Integrations → Webhooks → New webhook → copy its URL.
2. **Discord bot** (for the import): discord.com/developers → New Application → Bot: turn on **Message Content Intent**,
   copy the token; OAuth2 → URL Generator: scope `bot`, permissions View Channels + Read Message History → open the URL,
   add it to the server, and allow it in the private channel. Copy the channel's id (Developer Mode → right-click → Copy
   Channel ID). On each PC write `%APPDATA%\12tails-wardrobe\discord.json` = `{"token": "<bot token>", "channel": "<id>"}`.
3. **Turnstile:** Cloudflare dashboard → Turnstile → Add widget, hostname `12tails-wardrobe.jumpthai.workers.dev`, mode
   Managed. Put the **site key** in `wardrobe/community_config.json` ("turnstile_site_key"; public, it goes in git).
4. **Secrets** (from any folder, logged in to wrangler): `npx wrangler secret put DISCORD_WEBHOOK --name 12tails-wardrobe`
   (paste the webhook URL), `npx wrangler secret put TURNSTILE_SECRET --name 12tails-wardrobe` (paste the secret key).
5. Then Claude: publish, deploy with the Worker script (NOTES.md "Online copy"), send one test skin, approve it, run
   `py -3 -I pipeline/wardrobe_community.py`, publish, deploy, and check it in the menu. Delete this item.

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
