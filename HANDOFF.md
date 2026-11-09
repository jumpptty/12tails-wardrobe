# Handoff between the two PCs

Steps one PC left for the other. A session reads this at the start, does what is listed for its PC (where the user's
go-ahead is needed, says so), and deletes each item once it is done. Empty = nothing pending.

## Home PC

- **Rebuild the item map once** (left by the office, 2026-11-09): `py -3 -I pipeline\bb_item_codes.py`. The parser fix
  (commit 7d255b3) changed 14 codes in `wardrobe\data\item_map.json` / `icons.json`, which are not in git. Do it before
  any `transfer_to_drive.ps1`, or the office gets the old map back. Check: `wardrobe_sets_check.py` exits 0 (the
  Chameleon legend set wears legendBow).
- **Publish the online copy** (user's go-ahead to deploy): `py -3 pipeline\wardrobe_publish.py --out wardrobe_dist`
  after the rebuild above; it carries 2026-11-09's changes (max-rank moves, R / V tiles in ชุด, the item-map fix). The
  user deploys (NOTES.md "Online copy").
- FYI: the Bible commit `0704e0f6` (reference notes on skill animations and weapon codes) was made at the office and
  not pushed; pull it there before editing those four reference files at home.
