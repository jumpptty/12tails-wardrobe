export const meta = {
  name: 'sheep-fx-build',
  description: 'Build the Sheep effects: missing parts in parallel, one editor writes the cues and builds, one QA pass checks Sheep and the Wolf',
  phases: [
    { title: 'Build', detail: '4 builders, one file set each' },
    { title: 'Integrate', detail: 'one editor: sheep.json, data build, checks' },
    { title: 'QA', detail: 'headless checks, screenshots, Wolf regression, fixes' },
  ],
}

const CTX = `Repo C:\\work\\12tails-wardrobe (the OFFICE PC; the Bible is C:\\Users\\Jump\\Desktop\\12tails). We are giving the SHEEP class its
skill effects and sounds in the wardrobe page, the way the Wolf was done. READ FIRST: plans/fx_sheep/decisions.md (the user's 20
decisions, binding; also "every missing part gets built, nothing is left out for a missing part"), plans/fx_sheep/parts.md (each
missing part: BB source file:line, serialized fields, the Sheep's values, exact LAYOUTS lines, the proposed split), and the other
research reports in plans/fx_sheep/ (attacks_emotes, own_skills, cast_a, cast_b, tto; each ends with a "Verification" section whose
corrections win). The plug-in interface for effect parts: the comment above FX_PART_FILES in wardrobe/index.html and
plans/fx_wolf/build_rules.md ("The interfaces"); working examples: ringEmitter / imageEmitter / lineEmitter / legacyParticles in
index.html and wardrobe/fxparts/*.js. Game sources: C:\\Users\\Jump\\Desktop\\12tails\\DecompiledSource\\*.cs (BB, the authority);
TTO pseudo-C DecompiledSource_TTO_2026-11-02\\pseudo\\ (and the newer DecompiledSource_TTO_2026-11-09 if it helps); TTO's decrypted
bundles for this PC: tto_assets\\2026-11-09\\dec + catalog.bin (pipeline/wardrobe_fx_tto.py finds them).
Follow the game: cite file:line for every behaviour in code comments; where you must approximate, say so in a comment and in your
report. Quality bar from the user: "we are top quality".`

const RULES = `RULES: edit ONLY the files you own (listed below). If you need a change in a file you don't own, describe it exactly
(file, anchor, new text) in your report's shared_changes. Never git commit. No browser / Playwright in the Build phase (check JS with
node --check, e.g. node --input-type=module --check < file.js; Python by running it read-only). Never run pipeline/wardrobe_fx.py
without --probe in the Build phase. Probe scripts only under checks/fx_sheep_build/<your name>/.`

const BUILD = [
  { key: 'alphatimer', owns: 'wardrobe/fxparts/alphatimer.js (new), wardrobe/fxparts/mesh.js',
    task: `Build AlphaTimer (parts.md "AlphaTimer"): it fades its own node's renderer material over time (AlphaTimer.cs:378-402),
draws nothing itself; find the mesh child lazily on the first update, clone the material per spawn (copy onBeforeCompile), the
blend rules in parts.md (add / alpha: opacity = min(1, 2a); Phoenix: opacity = a; addsoft / opaque: no-op). In mesh.js: a proper
material for the game's lit shader "FX/Phoenix" (parts.md "Read this first" 1: Lambert + emission from _Emission; today mesh.js:55
falls back to a particle material with a warning), and an animation API for Eden Sanctuary: the Animation emitter exposes
play(clipName) (crossfade or cut as Unity's Animation.Play) and stores itself as node.userData.fxAnim, so another part can call
node.userData.fxAnim?.play("destroy"). The material() side of _Emission in pipeline/wardrobe_fx.py belongs to agent page_pipeline:
tell it the exact field you read (e.g. mat.emission as [r,g,b,a]). Make sure the Wolf's effects that use mesh.js still look the same.` },
  { key: 'sheep_parts', owns: 'wardrobe/fxparts/sheep.js (new)',
    task: `Build the Sheep's own scripts (parts.md "ProjectileControl + Sheep_nAttack / Sheep_homingLight / Sheep_cAttack" and
"Sheep_edenSanctuary"): ProjectileControl data + the three movers (constant velocity TransformDirection (0,0,12) / (0,0,8), the
code's life 1.7 / 1.7 / 5 s; decision 3: they end where they meet the ground at the 10 m target point, about 0.8 s: take the cue's
placement / pitch from parts.md, end the ball with its impact as the game's collision would); homing only with a target (none here).
Sheep_cAttack.Init's glow growth (decision 8: BB max, +1.6 m) needs a per-spawn addSize hook in index.html's legacyParticles: agent
page_pipeline adds it; agree the name: the hook is fx.addSize (metres) read by legacyParticles when building; your part sets it in
build before the particles' first emission, or say exactly what you need. Sheep_edenSanctuary (0 serialized bytes): plays its create
clip, switches to the destroy clip at 12 s, destroys the effect at 13 s (Sheep_edenSanctuary.cs:73, :129-135, :409, :423): call
node.userData.fxAnim?.play(name) (agent alphatimer adds that API to mesh.js's Animation emitter). Sheep_seal needs no page code
(parts.md): nothing to do for it.` },
  { key: 'page_pipeline', owns: 'wardrobe/index.html, pipeline/wardrobe_fx.py, pipeline/wardrobe_fx_check.py, pipeline/wardrobe_fx_inventory.py, plans/fx_inventory.md, plans/fx_inventory.json',
    task: `(1) pipeline/wardrobe_fx.py: the LAYOUTS lines parts.md gives for AlphaTimer, ProjectileControl, Sheep_seal and the 0-byte
movers / Sheep_edenSanctuary, and material() keeping _Emission for FX/Phoenix (agree the JSON field with agent alphatimer: name it
"emission", [r, g, b, a]); also make --probe / the build accept the effect names' real case (tto.md notes "--probe returncast" finds
nothing while the inventory lists lower case). Prove each layout by probing the Sheep prefabs read-only (--probe).
(2) wardrobe/index.html: FX_PART_FILES += "alphatimer", "sheep"; a per-spawn addSize (metres) that legacyParticles adds to the
particle size when set on the Fx (for Sheep_cAttack; agent sheep_parts sets fx.addSize in its build; make the order work: the part
runs before the particles' first emission, or read it lazily); an effect's looping AudioSource (loop true) plays looped until the
effect ends instead of once (lullaby_ring, divinityAxe, edenSanctuary, cAttack_charge; Sound in index.html: return a stop handle);
decisions 12 (Normal Attack SEQ "nAttack1@0.7 nAttack2^@0.8 nAttack3": check the SEQ notation in its comment), 13 (a sequence can
carry its own cues for a clip it shares: fxStart tries the key "@<Sequence name>:<clip>" before "<clip>", e.g. "@Lullaby:holyLight1";
document it in the comment above cueOf), 14 (the cast pool re-picks on every play of the tile, not only step 0 of the first play: see
cast_b.md "Read this first" 1 and fxStart's FX.pick), 16 (new SEQ sequences for the Sheep: "Soul of Arms: cast1 cast2*@0 soulOfArms~"
style, and the same for Gleaming Breath and Lucent Barrier with their TTO clips gleamingBreath / lucentBarrier; follow how the existing
Sheep "Cast" entry is written and what the reports say about the cast bar), 17 (tiles "Seal" and "Eden Sanctuary" = cast3 alone, no
cast bar; Seal cuts in with no fade; they need their own cue keys via decision 13). Keep the Wolf and every other class working; the
existing SEQ entries' meaning must not change except decision 12.
(3) pipeline/wardrobe_fx_check.py: handle "@<Sequence>:<clip>" cue keys (play that sequence's tile) and the new tiles.
(4) pipeline/wardrobe_fx_inventory.py: add the parts built today to BUILT (AlphaTimer, ProjectileControl, Sheep_seal, Sheep_nAttack,
Sheep_homingLight, Sheep_cAttack, Sheep_edenSanctuary, and the TTO ones agent tto reports, if you get them: else leave a TODO line
in your report) and regenerate plans/fx_inventory.md/.json by running it.
Run the repo's unit tests afterwards: py -3 -m unittest pipeline.test_wardrobe_publish pipeline.test_wardrobe_props_tex pipeline.test_repo_rules.` },
  { key: 'tto', owns: 'pipeline/wardrobe_fx_tto.py, wardrobe/fxparts/tto_sheep.js (new), wardrobe/fxparts/shuriken.js, wardrobe/fxparts/groundhug.js, wardrobe/fxparts/arcribbon.js, wardrobe/fxparts/groundfollower.js, plans/fx_sheep/tto.md',
    task: `The Sheep's three TTO skills (plans/fx_sheep/tto.md). The researcher could not read the Sheep's TTO prefabs; this PC now
has them (tto_assets\\2026-11-09). (1) Add the Sheep to wardrobe_fx_tto.py (SKILL_FX["sheep"]: every prefab its TTO skills spawn,
tto.md's table) and --probe every one: their parts, EffectControl life / followState, AudioSources, meshes; write the facts into
tto.md (a new section "Probed 2026-11-10"), correcting the report where the prefabs disagree with it. (2) Build every part they need
that the page lacks, so nothing is left out for a missing part (decisions: the user's rule): at least the lucentBarrier_beam's
RabbitTracer (a TTO script, Set(from, to) draws the line: read its code from TTO's GameAssembly via the Bible's tools, as the Wolf's
TTO parts were: plans/fx_wolf/tto.md and wardrobe/fxparts/groundhug.js show how), and gleamingBreath_wisp's flight (BreathFly@0x1E72EA0:
mouth -> the revived ally's chest 10 m ahead, up-arc u x 0.9 x (1 - u), clamp(d/16, 0.15, 0.6) s, destroyed 0.3 s after landing):
as a part in tto_sheep.js driven by cue placement, or the smallest cue-option design you can justify; plus any ParticleSystem feature
the prefabs use that shuriken.js does not draw yet. (3) Run uv run --no-project --with UnityPy --with pillow --with imageio-ffmpeg
python -I pipeline/wardrobe_fx_tto.py sheep to write the tto/ effects into wardrobe/data/sheep/fx.json (it only touches tto/ entries
and tto_ textures; nobody else builds the Sheep's data before you finish). Report the new part file names (for FX_PART_FILES) and
any cue changes tto.md's entries need.` },
]

const BUILT = {
  type: 'object',
  properties: {
    built: { type: 'array', items: { type: 'string' } },
    files_changed: { type: 'array', items: { type: 'string' } },
    api_notes: { type: 'string', description: 'what the editor must know: part file names, hooks, cue options, data fields' },
    shared_changes: { type: 'array', items: { type: 'string' }, description: 'exact changes needed in files you do not own' },
    faithfulness: { type: 'string' },
    unlocks: { type: 'array', items: { type: 'string' } },
    problems: { type: 'array', items: { type: 'string' } },
  },
  required: ['built', 'files_changed', 'api_notes', 'shared_changes', 'faithfulness', 'unlocks', 'problems'],
}
const RESULT = {
  type: 'object',
  properties: {
    done: { type: 'array', items: { type: 'string' } },
    checks: { type: 'array', items: { type: 'string' }, description: 'each check run and its exact outcome' },
    problems_left: { type: 'array', items: { type: 'string' } },
    for_the_user: { type: 'array', items: { type: 'string' }, description: 'what to look at when testing; Bible findings to offer' },
  },
  required: ['done', 'checks', 'problems_left', 'for_the_user'],
}

phase('Build')
const builds = await parallel(BUILD.map(b => () => agent(
  `${CTX}\n\n${RULES}\n\nYOUR NAME: ${b.key}. FILES YOU OWN: ${b.owns}.\nYOUR TASK: ${b.task}`,
  { label: `build:${b.key}`, phase: 'Build', schema: BUILT })))
const buildNotes = BUILD.map((b, i) => ({ agent: b.key, report: builds[i] || 'FAILED: no report' }))
log(`build reports: ${buildNotes.filter(n => typeof n.report === 'object').length}/4`)

phase('Integrate')
const editor = await agent(
  `${CTX}\n\nYou are the ONE EDITOR for the Sheep (the Wolf was done the same way: plans/fx_wolf/parts_built.md, NOTES.md 2026-11-09
"every drawable Wolf effect, built and cued"). Four builders just finished; their reports (JSON): ${JSON.stringify(buildNotes)}.
You may now edit any file. Do, in order:
1. Apply every shared_change the builders asked for (check each against the code; FX_PART_FILES must list every new part module,
   e.g. tto_sheep). Make the parts work together (alphatimer / mesh.js Animation API / sheep.js / addSize / looping audio).
2. Write wardrobe/fx_cues/sheep.json (valid JSON, the Wolf file's layout) from the reports' ready-to-paste entries, corrected by
   their Verification sections and by plans/fx_sheep/decisions.md (all 20 apply: self-casts, 10 m target point, ground-ending balls,
   Return Cast 24 % rolls with one roll name per play, Homing Light, BB-max charge glow, TTO's voice fixes, KO deadEffect on half the
   plays, the per-sequence cue keys "@<Sequence>:<clip>", the cast3 pool for the Cast tile, Seal / Eden tiles, two seal skills, seal
   kill 10 s, Eden 1 m ahead, the TTO skills, the emotes and KO voices). Every effect that the builders made drawable goes in: nothing
   stays "left out" for a missing part. Effects only on enemies stay out (decisions). Each entry's "why" cites file:line.
3. The Wolf's KO: add deadEffect on half the plays to wardrobe/fx_cues/wolf.json's ko entry (decision 11) and build it with
   uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py wolf --fx deadEffect
   (only that effect: a full Wolf rebuild on this PC changes four mMeshFilter ids, NOTES.md 2026-11-10; check git diff of
   wardrobe/data/wolf/fx.json shows only deadEffect added).
4. Build the Sheep: uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py sheep,
   then uv run --no-project --with UnityPy --with pillow --with imageio-ffmpeg python -I pipeline/wardrobe_fx_tto.py sheep
   (re-run after the first so the tto/ entries stay), fix every missing effect / sound it reports.
5. Checks, one at a time (this PC's rule: one headless browser at a time):
   uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py C:/work/12tails-wardrobe checks/fx_sheep --cls sheep --files-only
   uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py C:/work/12tails-wardrobe checks/fx_sheep dark --cls sheep
   Both must exit 0 with errors []: fix the cause of every failure (page, part, cue or data), re-run until clean.
6. Unit tests: py -3 -m unittest pipeline.test_wardrobe_publish pipeline.test_wardrobe_props_tex pipeline.test_repo_rules.
Never git commit. Report exactly what each check printed at the end.`,
  { label: 'editor:sheep', phase: 'Integrate', schema: RESULT })

phase('QA')
const qa = await agent(
  `${CTX}\n\nYou are the QA pass for the Sheep's effects. The builders and the editor report: ${JSON.stringify({ builds: buildNotes, editor })}.
Assume something is still wrong and find it. One headless browser at a time on this PC. Do:
1. Sheep: uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py C:/work/12tails-wardrobe checks/fx_sheep_qa dark --cls sheep
   then LOOK at the screenshots (checks/fx_sheep_qa/*_peak.png and the per-effect shots; open them with the Read tool): does each effect
   sit where the reports and decisions put it (at the hero, 1 m / 10 m ahead, the balls ending at the ground, the divinity weapons 10 m
   ahead, the seals and Eden, the self-cast marks on the Sheep), is anything invisible, black, huge, inside-out or flickering? Compare a
   sample of at least 15 cues against the reports' file:line claims and the decisions.
2. The Wolf must not have regressed (mesh.js, index.html and shared parts changed): run
   uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py C:/work/12tails-wardrobe checks/fx_wolf_qa dark --cls wolf
   and compare its peak shots with the Wolf's earlier look where you can (checks/fx_wolf_emotes from this morning).
3. The rest of the page: uv run --no-project --with playwright python -I pipeline/wardrobe_moves_check.py (read its docstring for the
   exact command line) and pipeline/wardrobe_menu_check.py if present; the unit tests.
4. Fix every real problem you find (any file; never git commit), re-run the affected checks until clean. Thai on-screen text: check
   mark placement where you changed or added any.
Report each check's exact outcome, what you fixed, what is left, and what the user should look at by hand.`,
  { label: 'qa:sheep+wolf', phase: 'QA', schema: RESULT })

return { builds: buildNotes, editor, qa }
