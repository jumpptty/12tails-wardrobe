# Probes behind the Sheep reports and build

The research and build agents' scripts and their smaller outputs, copied from the git-ignored
`checks/fx_sheep_research/` and `checks/fx_sheep_build/` (2026-11-10, so the other PC has them): a report citing
`checks/fx_sheep_research/<x>` means `research/<x>` here, `checks/fx_sheep_build/<x>` means `build/<x>`. The builders'
self-checks run with node: `build/alphatimer/check.mjs`, `build/sheep_parts/check_sheep.mjs`. Outputs over 400 KB were
left out (e.g. `build/tto/probe.json`): rerun the read-only probe (`pipeline/wardrobe_fx.py sheep --probe ...`,
`pipeline/wardrobe_fx_tto.py sheep --probe ...`). Scripts carry the office's paths (`C:\work\...`, the Bible at
`C:\Users\Jump\Desktop\12tails`); at home use `D:\`.
