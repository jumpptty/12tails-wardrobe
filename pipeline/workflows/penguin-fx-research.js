export const meta = {
  name: 'penguin-fx-research',
  description: 'Research the Penguin class effects + sounds (6 read-only researchers, 3 checkers re-trace the claims)',
  phases: [
    { title: 'Research', detail: '6 researchers, one report each in plans/fx_penguin/' },
    { title: 'Verify', detail: 'each checker re-traces two reports against Penguin.cs and fixes them' },
  ],
}

const COMMON = `You are researching the 12 Tails Wardrobe's PENGUIN class effects and sounds (repo C:\\work\\12tails-wardrobe, the OFFICE PC;
the Bible is C:\\Users\\Jump\\Desktop\\12tails). The Wolf and the Sheep are finished; the Penguin is next, built the same way.

READ FIRST: plans/fx_recipe.md (the method), plans/fx_sheep/decisions.md and plans/fx_wolf/decisions.md (the user's decisions:
APPLY THEM TO THE PENGUIN BY ANALOGY without asking again: ally skills as self-casts on the hero, effects on an enemy / a target
at the target point 10 m ahead, projectiles end where they meet the ground at that point, skill-altering passives ON at max
rank, random picks kept as "a|b" or rolls (Free Cast / Return Cast-like flashes rolled at 24 %), TTO's voice fixes where BB asks
for files that don't exist, every missing effect part gets BUILT later so write cues for those effects too (mark the part they
need), a skill played with a cast bar becomes a sequence with it, a shared clip's skills become a "skills" pool; raise a
question ONLY for something those decisions don't answer). The Sheep's research is the model for format and depth:
plans/fx_sheep/*.md (e.g. cast_a.md, parts.md, tto.md), and the finished wardrobe/fx_cues/sheep.json shows the cue options in use
(d, x, y, rot, vol, cut, p, roll "!name", scale, kill, to, bone; the per-sequence keys "@<Sequence id>:<clip>"; the comment above
cueOf in wardrobe/index.html). The Sheep section of plans/fx_inventory.md shows the format; the Penguin section says which Penguin
effects need a part the page lacks (Penguin_tornado, Penguin_typhoon, Penguin_arcticEmperor, Penguin_cosmicFriday,
Penguin_iceBlock, Penguin_nAttack). The page's Penguin sequences: SEQ in wardrobe/index.html (the "penguin:" line). Cues are keyed
by the clip they start with.

SOURCES: C:\\Users\\Jump\\Desktop\\12tails\\DecompiledSource\\Penguin.cs (BB, the authority), CharacterControl.cs, PenguinSkill.cs,
the Bible's 12t_reference\\penguin-skill-reference.md and its skill cards in 12t_projects\\bible\\index.html; TTO:
DecompiledSource_TTO_2026-11-02\\pseudo\\Penguin.c (cite TTO1102:Method@RVA). This PC has TTO's decrypted bundles
(tto_assets\\2026-11-09, read by pipeline/wardrobe_fx_tto.py --probe). Tools:
  node pipeline/clip_flow.js C:/Users/Jump/Desktop/12tails/DecompiledSource/Penguin.cs RPC_<name> "Effects/|Voices/|Sounds/|createEffect|Instantiate|PlayOneShot|PlayAnimation|WaitForSeconds|actionState"
  node pipeline/clip_calls.js C:/Users/Jump/Desktop/12tails/DecompiledSource wardrobe/data penguin
  uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py penguin --probe name1,name2   (READ ONLY)
  uv run --no-project --with UnityPy --with pillow --with imageio-ffmpeg python -I pipeline/wardrobe_fx_tto.py penguin --probe tto/name1,tto/name2   (READ ONLY)
  the QA tools pipeline/wardrobe_fx_probe.py / wardrobe_fx_trace.py exist if you need to see an effect (one headless browser at a time; prefer reading).
The rip's Penguin voices / sounds / effects: C:\\Users\\Jump\\Desktop\\12tails\\RippedAssets\\ExportedProject\\Assets\\Resources\\gameassets\\characters\\heroes\\penguin\\{voices,sounds,effects}.
Say which folder each cue's file is in (kind "voice" = voices/, "sound" = sounds/; names can collide with different recordings).

RULES: research only. Write ONLY your report file; probe scripts only under checks/fx_penguin_research/<your name>/. Never edit any
other file, never run wardrobe_fx.py / wardrobe_fx_tto.py without --probe. Cite file:line for every time, name and distance.
Times are seconds from the start of the clip the cue is keyed by; follow the flattened state machine (Yield(n, WaitForSeconds(t)))
from the clip's PlayAnimation, add the waits, double-check each sum. Report per clip: the skill(s), coroutine + line range, the
timeline, a ready-to-paste cue entry (exact JSON as in sheep.json, with a "why" citing lines), what is left out and why (only
"on an enemy with no target-point analogue" or "needs an attacker" are acceptable reasons; a missing part is NOT a reason: cue it
and name the part), and only genuinely new questions. Start the report with "Read this first": blockers, name collisions, game
bugs, SEQ step-time errors, surprises.`

const RESEARCH = [
  { key: 'attacks_emotes', file: 'plans/fx_penguin/attacks_emotes.md', scope: `Normal Attack nAttack1-3 (RPC_nAttack1-3; the projectile spreadShot_fire needs Penguin_nAttack), Charge Attack cAttack1 / cAttack2 (RPC_cAttack1), MP Transfer (RPC_mpTransfer plays nAttack1: a shared clip, propose how the Normal Attack tile and MP Transfer coexist), RPC_activateIcon1 (plays cAttack2: what it is), the dispatcher's stage windows vs the SEQ step times. ALSO the emotes, basic moves and KO exactly as for the Wolf and the Sheep (wolf.json / sheep.json's wave / bow / laugh / sleep / cheer / beg / cry / talk / battle / ko entries; RPC_emotion, RPC_ko, RPC_dead: which voice files exist in the Penguin's rip, deadEffect on half the KO plays).` },
  { key: 'own_skills', file: 'plans/fx_penguin/own_skills.md', scope: `The Penguin skills with their own clips: Falling Stars (RPC_fallingStars, cast4) and Nova Flare (RPC_novaFlare, cast4): a shared clip, a pool or sequences; Blink (RPC_blink) and Parallel Shift (RPC_parallelShift), both playing blink; Arctic Emperor (RPC_arcticEmperor; the arcticEmperor effect needs Penguin_arcticEmperor); Focus Intellect (RPC_focusIntellect). Check the SEQ entries for these against the code.` },
  { key: 'cast_a', file: 'plans/fx_penguin/cast_a.md', scope: `The Cast tile (cast1, cast2, cast3): RPC_cast1 (cast2 loop, then cast1: the casting channel and its effects / voices, how it hands over to each skill's *_cast RPC) and the FIRST HALF of the skills whose *_cast RPC plays cast3: manaMissile, manaBurn, fallingComets, manaVortex, meteora, frozenBlast, arcticWind, iceShield. cast3 is shared, so a "skills" pool (as sheep.json's cast3): one member per skill; cast_b writes the rest; the editor merges.` },
  { key: 'cast_b', file: 'plans/fx_penguin/cast_b.md', scope: `The SECOND HALF of the cast3 skills: iceBlock (needs Penguin_iceBlock), snowMan, tornado (tornado1-3 need Penguin_tornado), typhoon (typhoon1-3 need Penguin_typhoon), absoluteZero (FX/Phoenix: the page now draws it), blizzard, snowBall, cosmicRift, and Cosmic Friday (RPC_cosmicFriday_cast: its own cosmicFriday clip looping, then cast3; the cosmicFriday effect needs Penguin_cosmicFriday): a "skills" pool member per cast3 skill, and Cosmic Friday's own entry / sequence. Rank-gated variants (tornado1-3, typhoon1-3): max rank.` },
  { key: 'tto', file: 'plans/fx_penguin/tto.md', scope: `The Penguin's three TTO Lv 100 skills: constellation, emperorPenguin, frostFieldLeap (TTO pseudo-C pseudo\\Penguin.c / PenguinSkill.c, the Bible's "TTO Lv 100 skills", the model plans/fx_sheep/tto.md and its "Probed 2026-11-10" section). This PC CAN read their prefabs: list them from TTO's catalog (pipeline/wardrobe_fx_tto.py's catalog code, the Bible's tools/aa_catalog.py) and --probe each (parts, EffectControl life / followState, AudioSources, meshes, code movers like the Sheep's BreathFly / CodexOpen). Name every TTO script / Unity component they use that the page lacks (wardrobe/fxparts/tto_sheep.js, shuriken.js, groundhug.js, arcribbon.js, groundfollower.js are what exists).` },
  { key: 'parts', file: 'plans/fx_penguin/parts.md', scope: `Every part the Penguin's effects need that the page lacks: Penguin_tornado (3 effects), Penguin_typhoon (3), Penguin_arcticEmperor, Penguin_cosmicFriday, Penguin_iceBlock, Penguin_nAttack, plus anything the Penguin's prefabs use that the page draws wrongly (shaders like Transparent/Opaque1 or built-ins the Sheep QA flagged, unusual emitter settings): BB source file:line, serialized fields and the Penguin's values (probe), what each draws or moves, the exact LAYOUTS lines wardrobe_fx.py needs, how it plugs in (FX_PART_FILES comment in index.html; model wardrobe/fxparts/sheep.js), which effects it unblocks, and a split into builders with non-overlapping file ownership (model plans/fx_sheep/parts.md "Who builds what").` },
]

const REPORT = {
  type: 'object',
  properties: {
    report: { type: 'string' },
    clips: { type: 'array', items: { type: 'string' } },
    cue_entries: { type: 'integer' },
    parts_needed: { type: 'array', items: { type: 'string' }, description: 'effect: part' },
    new_questions: { type: 'array', items: { type: 'string' }, description: 'only what the Sheep / Wolf decisions do not answer, each with a recommended default' },
    summary: { type: 'string' },
  },
  required: ['report', 'clips', 'cue_entries', 'parts_needed', 'new_questions', 'summary'],
}
const VERDICT = {
  type: 'object',
  properties: {
    reports: { type: 'array', items: { type: 'string' } },
    claims_checked: { type: 'integer' },
    corrections: { type: 'array', items: { type: 'object', properties: { report: { type: 'string' }, claim: { type: 'string' }, fix: { type: 'string' } }, required: ['report', 'claim', 'fix'] } },
    unresolved: { type: 'array', items: { type: 'string' } },
  },
  required: ['reports', 'claims_checked', 'corrections', 'unresolved'],
}

const PAIRS = [[RESEARCH[0], RESEARCH[1]], [RESEARCH[2], RESEARCH[3]], [RESEARCH[4], RESEARCH[5]]]

const results = await pipeline(
  PAIRS,
  pair => parallel(pair.map(r => () => agent(
    `${COMMON}\n\nYOUR NAME: ${r.key}. YOUR REPORT FILE (the only file you write): ${r.file}\nYOUR SCOPE: ${r.scope}`,
    { label: `research:${r.key}`, phase: 'Research', schema: REPORT }))),
  (found, pair) => agent(
    `You are a skeptical checker for the 12 Tails Wardrobe's Penguin effects research (repo C:\\work\\12tails-wardrobe, office PC; Bible C:\\Users\\Jump\\Desktop\\12tails).
Two researchers wrote: ${pair.map(r => r.file).join(' and ')}. Their summaries: ${JSON.stringify((found || []).filter(Boolean).map(f => ({ report: f.report, summary: f.summary })))}.
On the Wolf and the Sheep, such reports had wrong step times, line numbers and folder claims (15 corrections on the Sheep), so assume errors exist.
Independently RE-TRACE every claim a cue depends on: each time (re-add the waits along the flattened state machine from the clip's PlayAnimation, node pipeline/clip_flow.js C:/Users/Jump/Desktop/12tails/DecompiledSource/Penguin.cs RPC_<name> "<pattern>"), each effect / voice / sound name and its rip folder (C:\\Users\\Jump\\Desktop\\12tails\\RippedAssets\\ExportedProject\\Assets\\Resources\\gameassets\\characters\\heroes\\penguin), each distance and placement, each max-rank and passive choice, each "left out" reason (a missing part is not a valid one), each SEQ claim, each target (enemy vs ally vs self: the Sheep's Soul of Arms was wrongly called an ally buff; check every skill's hit / heal call), each parts claim (file:line, serialized fields), each TTO claim (pseudo\\Penguin.c, and the prefabs via pipeline/wardrobe_fx_tto.py penguin --probe). Method: plans/fx_recipe.md; rules: plans/fx_sheep/decisions.md.
Fix every confirmed error DIRECTLY in the report (edit only these two files; probe scripts under checks/fx_penguin_research/verify/), append "## Verification (2026-11-10)" to each listing what you checked and each correction (old -> new, with the proving line). A claim you could not disprove goes under unresolved, not "fixed". No browser, never run the builders without --probe.`,
    { label: `verify:${pair.map(r => r.key).join('+')}`, phase: 'Verify', schema: VERDICT }),
)

return PAIRS.map((pair, i) => ({ pair: pair.map(r => r.key), research: [], verify: results[i] }))
