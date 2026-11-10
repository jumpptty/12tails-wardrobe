export const meta = {
  name: 'sheep-fx-research',
  description: 'Research the Sheep class effects + sounds (6 read-only researchers, 3 checkers re-trace the claims)',
  phases: [
    { title: 'Research', detail: '6 researchers, one report each in plans/fx_sheep/' },
    { title: 'Verify', detail: 'each checker re-traces two reports against Sheep.cs and fixes them' },
  ],
}

const COMMON = `You are researching the 12 Tails Wardrobe's SHEEP class effects and sounds (repo C:\\work\\12tails-wardrobe, the OFFICE PC;
the Bible is C:\\Users\\Jump\\Desktop\\12tails). The Wolf is finished; Sheep is next, built the same way.

READ FIRST: plans/fx_recipe.md (the method: find what the game does, cue format, max rank, target-hit rule, followState),
plans/fx_wolf/decisions.md (the user's Wolf decisions: apply them to the Sheep by analogy, e.g. skill-altering passives ON at
max rank, enemy hits left out, a target point 10 m ahead, random picks kept as "a|b" or rolls), the comment above cueOf in
wardrobe/index.html (cue options d, x, y, rot, vol, cut, p, roll, scale, kill) and how wardrobe/fx_cues/wolf.json is written
(plain entries, and the shared-clip "skills" pool, e.g. its darkEdge entry). Format model for your report:
plans/fx_wolf/counters.md. The Sheep section of plans/fx_inventory.md says which Sheep effects the page draws today
("ready") and which need a missing part (write those as "left out: <name> needs <part>" so they are added later).
The page's Sheep sequences (SEQ in wardrobe/index.html): "Normal Attack: nAttack1@0.8 nAttack2^ nAttack3",
"Charge Attack: cAttack1@0.8 cAttack0*~@4 cAttack2", "Cast: cast1 cast2*@0 cast3~",
"Holy Light: holyLight1@0.6 holyLight2*@0 holyLight3@0.4 holyLight4*@3", "Lullaby: holyLight1@0.6 holyLight2*@0 lullaby*@3".
Cues are keyed by the clip they start with.

SOURCES: C:\\Users\\Jump\\Desktop\\12tails\\DecompiledSource\\Sheep.cs (BB, the authority), CharacterControl.cs, SheepSkill.cs,
the Bible's 12t_reference\\sheep-skill-reference.md and its skill cards in 12t_projects\\bible\\index.html; TTO:
DecompiledSource_TTO_2026-11-02\\pseudo\\Sheep.c (cite TTO as TTO1102:Method@RVA, never by line). Tools:
  node pipeline/clip_flow.js C:/Users/Jump/Desktop/12tails/DecompiledSource/Sheep.cs RPC_<name> "Effects/|Voices/|Sounds/|createEffect|Instantiate|PlayOneShot|PlayAnimation|WaitForSeconds|actionState"
  node pipeline/clip_calls.js C:/Users/Jump/Desktop/12tails/DecompiledSource wardrobe/data sheep
  uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py sheep --probe name1,name2   (READ ONLY; never run wardrobe_fx.py without --probe)
The rip's Sheep voices / sounds: C:\\Users\\Jump\\Desktop\\12tails\\RippedAssets\\ExportedProject\\Assets\\Resources\\gameassets\\characters\\heroes\\sheep\\{voices,sounds,effects}.
Voices and sounds can share a name with different recordings: say which folder each cue's file is in (cue kind "voice" =
voices/, "sound" = sounds/).

RULES: research only. Write ONLY your report file (path below); any probe scripts only under checks/fx_sheep_research/<your name>/.
Never edit any other file, never run a browser or Playwright. Cite file:line for every time, name and distance. Times are
seconds from the start of the clip the cue is keyed by; follow the flattened state machine (Yield(n, WaitForSeconds(t)) =
wait t then case n) from the clip's PlayAnimation, add the waits, and double-check each sum. Report per clip: the skill(s),
coroutine + line range, the timeline, a ready-to-paste cue entry (exact JSON as in wolf.json, with a "why" citing lines),
what is left out and why, and open questions for the user (only real decisions, e.g. which passive, which rank-gated
variant). Finish with a short "Read this first" section at the top: blockers, name collisions, surprises.`

const RESEARCH = [
  { key: 'attacks_emotes', file: 'plans/fx_sheep/attacks_emotes.md', scope: `Normal Attack nAttack1-3 and Charge Attack cAttack0 / cAttack1 / cAttack2 (RPC_nAttack1-3, RPC_cAttack1, RPC_cAttack2; their projectiles and hits: a projectile flying to the target is a left-out target effect unless the game spawns something at the hero), the dispatcher's stage windows that set the SEQ step times (check @0.8 and the charge times against the code and say if SEQ is wrong). ALSO the emotes and basic moves, exactly as was done for the Wolf (see the wave / bow / laugh / sleep / cheer / beg / cry / talk / battle / ko entries at the end of wardrobe/fx_cues/wolf.json and NOTES.md 2026-11-10 "emote and basic-move voices"): Sheep's RPC_emotion (emo_<name> -> Voices/<name>, emo_chat -> chat1-5?), which emote plays which clip, which voice files exist in the rip, RPC_ko / RPC_dead voices; propose those entries too.` },
  { key: 'own_skills', file: 'plans/fx_sheep/own_skills.md', scope: `The Sheep skills with their own clips: Holy Light (RPC_holyLight: holyLight1 > holyLight2 loop > holyLight3 > holyLight4 loop, the SEQ "Holy Light" steps), Lullaby (RPC_lullaby: holyLight2 loop > lullaby loop > holyLight1, SEQ "Lullaby"), Purifying Tear (RPC_purifyingTear), Soul of Arms (RPC_soulOfArms_cast), Book Bash (RPC_bookBash: bookBash1 / 2 / 3; the page shows them as three separate tiles, a random pick in the game: say how the game picks). Check the SEQ step times for Holy Light and Lullaby against the code and say if they are wrong.` },
  { key: 'cast_a', file: 'plans/fx_sheep/cast_a.md', scope: `The Cast tile (cast1, cast2, cast3): RPC_cast1 (plays cast2 looping, then cast1: the casting channel every cast-time skill goes through; what effects / voices it has, and how it hands over to the skill's own *_cast RPC), and the FIRST HALF of the 23 skills whose *_cast RPC plays cast3: heal, bless, allHeal, pacify, sleep, clear, cleanse, allCleanse, overHeal, revive, revert (RPC_<skill>_cast). cast3 is shared, so its cue entry is a "skills" pool (like darkEdge in wolf.json): write one pool member per skill ({cues, why}); another researcher (cast_b) writes the other 12 members, the editor merges. Note which of these skills target an ally / an enemy / an area and where their effects appear (on the hero = kept; on the target = left out unless the target is the Sheep itself, e.g. a self heal: say what the wardrobe should do, following the decisions file).` },
  { key: 'cast_b', file: 'plans/fx_sheep/cast_b.md', scope: `The SECOND HALF of the 23 skills whose *_cast RPC plays cast3: lightBind, illuminate, feather, allFeather, divinitySword, divinitySpear, seal (RPC_seal), repel, reverse, divinityAxe, edenSanctuary (RPC_edenSanctuary), worldEncarta (RPC_<skill>_cast). cast3 is shared, so its cue entry is a "skills" pool (like darkEdge in wolf.json): write one pool member per skill ({cues, why}); another researcher (cast_a) writes the other 11 plus RPC_cast1, the editor merges. Note which of these skills target an ally / an enemy / an area and where their effects appear (on the hero = kept; on the target = left out, a target point 10 m ahead per the decisions file). Several of these effects need missing parts (AlphaTimer, Sheep_seal, Sheep_edenSanctuary): list them as left out with the part.` },
  { key: 'tto', file: 'plans/fx_sheep/tto.md', scope: `The Sheep's three TTO Lv 100 skills: gleamingBreath, grandCodex, lucentBarrier (no BB code plays them; TTO's pseudo-C DecompiledSource_TTO_2026-11-02\\pseudo\\Sheep.c and SheepSkill.c, the Bible's sheep-skill-reference.md "TTO Lv 100 skills", the TTO rip RippedAssets_TTO_2026-11-04). Model: plans/fx_wolf/tto.md (how the Wolf's three TTO skills were researched: coroutine timings from the pseudo-C, Ghidra-dropped floats, prefab names as tto/<prefab>, which TTO emitter scripts / Unity ParticleSystem parts they need, sounds). Note: TTO effects are BUILT only on the home PC (pipeline/wardrobe_fx_tto.py reads the video folder's tto_assets, which this PC lacks), so write the cues so the home PC can build them, and say which parts the page already has for TTO (wardrobe/fxparts/groundhug.js, arcribbon.js, groundfollower.js, shuriken.js) and which would be new. Sounds / voices the TTO skills play: where they are in the rip.` },
  { key: 'parts', file: 'plans/fx_sheep/parts.md', scope: `The effect parts the Sheep's effects need that the page cannot draw yet (plans/fx_inventory.md: AlphaTimer 6, Sheep_seal 4, ProjectileControl 3, Sheep_cAttack 1, Sheep_edenSanctuary 1, Sheep_homingLight 1, Sheep_nAttack 1). Model: plans/fx_wolf/parts.md. For each script: what it does in BB (C:\\Users\\Jump\\Desktop\\12tails\\DecompiledSource\\<Script>.cs, file:line), its serialized fields and the Sheep prefabs' values (probe with wardrobe_fx.py sheep --probe), whether it draws anything or only moves / fades / times other parts (ProjectileControl flying to a target may be a left-out target effect: say so), how it would plug into the page (the comment above FX_PART_FILES in wardrobe/index.html: a wardrobe/fxparts/<file>.js module's api.part(type, build); and what pipeline/wardrobe_fx.py LAYOUTS would need to decode its fields), which Sheep effects each unblocks, and for AlphaTimer also how many OTHER classes' effects it unblocks (plans/fx_inventory.md "Per missing part"). Rank the parts by value (effects unblocked / effort) and propose which agent should build which, with file ownership that never overlaps (as plans/fx_wolf/build_rules.md did).` },
]

const REPORT = {
  type: 'object',
  properties: {
    report: { type: 'string' },
    clips: { type: 'array', items: { type: 'string' } },
    cue_entries: { type: 'integer', description: 'cue entries or pool members proposed' },
    left_out_needing_parts: { type: 'array', items: { type: 'string' }, description: 'effect: part' },
    questions: { type: 'array', items: { type: 'string' }, description: 'decisions for the user' },
    summary: { type: 'string' },
  },
  required: ['report', 'clips', 'cue_entries', 'left_out_needing_parts', 'questions', 'summary'],
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
    `You are a skeptical checker for the 12 Tails Wardrobe's Sheep effects research (repo C:\\work\\12tails-wardrobe, office PC; Bible C:\\Users\\Jump\\Desktop\\12tails).
Two researchers wrote these reports: ${pair.map(r => r.file).join(' and ')}. Researchers' summaries: ${JSON.stringify((found || []).filter(Boolean).map(f => ({ report: f.report, summary: f.summary })))}.
On the Wolf, such reports had wrong step times and line numbers that had to be fixed by hand, so assume errors exist.
Independently RE-TRACE every claim a cue depends on: each cue's time (re-add the waits along the flattened state machine from the clip's PlayAnimation, with node pipeline/clip_flow.js C:/Users/Jump/Desktop/12tails/DecompiledSource/Sheep.cs RPC_<name> "<pattern>"), each effect / voice / sound name and which rip folder holds it (voices vs sounds, C:\\Users\\Jump\\Desktop\\12tails\\RippedAssets\\ExportedProject\\Assets\\Resources\\gameassets\\characters\\heroes\\sheep), each distance, each max-rank choice, each "left out" reason, each SEQ step-time claim; for a parts report, each file:line and serialized-field claim; for TTO, check against DecompiledSource_TTO_2026-11-02\\pseudo\\Sheep.c. The method is plans/fx_recipe.md; the user's rules are plans/fx_wolf/decisions.md.
Fix every error you confirm DIRECTLY in the report (edit only these two report files; probe scripts only under checks/fx_sheep_research/verify/), and append to each report a section "## Verification (2026-11-10)" listing what you checked and each correction (old -> new, with the line that proves it). Do not "fix" a claim you could not disprove: list it under unresolved instead. No browser, no Playwright, never run wardrobe_fx.py without --probe.`,
    { label: `verify:${pair.map(r => r.key).join('+')}`, phase: 'Verify', schema: VERDICT }),
)

return PAIRS.map((pair, i) => ({ pair: pair.map(r => r.key), verify: results[i] }))
