export const meta = {
  name: 'penguin-fx-build',
  description: 'Build the Penguin effects: missing parts in parallel, one editor writes the cues and builds, one QA pass checks Penguin, Sheep and Wolf',
  phases: [
    { title: 'Build', detail: '4 builders, one file set each' },
    { title: 'Integrate', detail: 'one editor: penguin.json, data build, checks' },
    { title: 'QA', detail: 'headless checks, screenshots, Sheep + Wolf regression, fixes' },
  ],
}

// Home PC paths (D:\12tails-wardrobe, the Bible at D:\12tails). At the office: C:\work\12tails-wardrobe and
// C:\Users\Jump\Desktop\12tails, TTO bundles in this repo's tto_assets\2026-11-09 (CLAUDE.md "Two PCs").
const REPO = 'D:/12tails-wardrobe'

const CTX = `Repo D:\\12tails-wardrobe (the HOME PC; the Bible is D:\\12tails). We are giving the PENGUIN class its skill effects
and sounds in the wardrobe page, the way the Wolf and the Sheep were done. READ FIRST: plans/fx_penguin/decisions.md (the user's 20
decisions, binding; the Sheep's plans/fx_sheep/decisions.md and the Wolf's plans/fx_wolf/decisions.md hold by analogy where they don't
speak; and "every missing part gets built, nothing is left out for a missing part": plans/fx_recipe.md), plans/fx_penguin/parts.md (each
missing BB part: source file:line, serialized fields, the LAYOUTS block, "Interfaces (fixed up front)", "Who builds what"),
plans/fx_penguin/tto.md (the TTO skills; section 6 = the TTO parts P1-P8, P7 not wanted: decision 8), and the other reports in
plans/fx_penguin/ (attacks_emotes, own_skills, cast_a, cast_b; each ends with a "Verification" section whose corrections win). How the
Sheep was built: NOTES.md 2026-11-10 "the Sheep's effects: built and cued" and "QA pass"; pipeline/workflows/sheep-fx-build.js. The
plug-in interface for effect parts: the comment above FX_PART_FILES in wardrobe/index.html and plans/fx_wolf/build_rules.md ("The
interfaces"); working examples: wardrobe/fxparts/*.js (sheep.js, tto_sheep.js, alphatimer.js are the newest). Game sources:
D:\\12tails\\DecompiledSource\\*.cs (BB, the authority); TTO pseudo-C D:\\12tails\\DecompiledSource_TTO_2026-11-02\\pseudo\\ (Penguin.c);
TTO's decrypted bundles on this PC: D:\\12tails-video\\tto_assets\\2026-11-04 (read only; pipeline/wardrobe_fx_tto.py finds them).
Follow the game: cite file:line for every behaviour in code comments; where you must approximate, say so in a comment and in your
report. Quality bar from the user: "we are top quality".`

const RULES = `RULES: edit ONLY the files you own (listed below). If you need a change in a file you don't own, describe it exactly
(file, anchor, new text) in your report's shared_changes. Never git commit. Never write in D:\\12tails-video or D:\\12tails. No browser /
Playwright in the Build phase (check JS with node --check, e.g. node --input-type=module --check < file.js; Python by running it
read-only). Never run pipeline/wardrobe_fx.py without --probe in the Build phase. Probe scripts only under
checks/fx_penguin_build/<your name>/.`

const BUILD = [
  { key: 'shaders', owns: 'wardrobe/fxparts/mesh.js',
    task: `parts.md "Who builds what" row A and "Interfaces" 1 and 5: in mesh.js's material(): AdditiveSaturate (two passes, so
material() may return a list for one name; withMaterials and ShatterMesh take a list and keep both), Opaque1, Opaque2 (only pass 2
draws: _Color.a below the 0.95 test), DiffuseAmbient (like opaque, colour = 2 x _Color, _Ambient white; APPROXIMATED: the game's
lights); the Animation emitter's play(name, fade = 0, wrap): a third argument overrides the wrap mode as Unity's animation.wrapMode
after Play (the tornado / typhoon clips carry wrap 0 under a Loop component). Every existing caller (the Wolf's and the Sheep's
effects, fxparts/sheep.js's fxAnim.play(name, fade)) must behave exactly as before. Tell agent page_pipeline the exact material JSON
fields you read (it owns pipeline/wardrobe_fx.py's material()).` },
  { key: 'penguin', owns: 'wardrobe/fxparts/penguin.js (new)',
    task: `parts.md row B: Penguin_tornado, Penguin_typhoon, Penguin_arcticEmperor, Penguin_cosmicFriday, Penguin_iceBlock,
Penguin_nAttack, Penguin_manaMissile, Penguin_snowMan, coded against parts.md "Interfaces" (agent shaders adds play(name, fade, wrap)
and the material lists; agent page_pipeline adds Sound.play's setVolume, Fx.dispose calling e.dispose?.(), the 206 / 207 builtins).
Decisions that land in your part: 1 (the Normal Attack ball ends on the ground at the 10 m target point, attacks_emotes' cue numbers);
3 (Mana Missiles aim at the target 0.6 m up: the 10 m point raised 0.6 m; check missile_sim.py's landing times against the code, the
cast_a verification flags a mismatch); 12 (Typhoon's first swerve 0 / 120 / 240 deg at random each play); 17 (Snow Man hides the hero's
meshes, outfit and props, from the spawn, shows them again at the cut and in dispose(): a new pick must never leave her hidden; say
exactly which api you use to reach the hero's meshes, and if the api lacks it, put the hook in shared_changes for index.html); 18 (the
Staff of Time: when the worn main-hand weapon is specialScepter (w_pgn59) the Normal Attack and Spread Shot balls move at 0.01 m/s and
last 12 s: say what api you read the worn weapon from). Look at fxparts/sheep.js for how the Sheep's projectiles end at the ground.` },
  { key: 'page_pipeline', owns: 'wardrobe/index.html, pipeline/wardrobe_fx.py, pipeline/wardrobe_fx_check.py, pipeline/wardrobe_fx_inventory.py, plans/fx_inventory.md, plans/fx_inventory.json',
    task: `(1) pipeline/wardrobe_fx.py: the LAYOUTS block from parts.md (prove each layout by --probe on the Penguin prefabs, read
only); material() keeps the fields agent shaders needs (AdditiveSaturate, Opaque1/2, DiffuseAmbient). (2) wardrobe/index.html, the
lead's items in parts.md "Who builds what": BUILTIN_BLEND 206 (Multiply Double, mesh.js glass's luminance trick, APPROXIMATED) and
207 (premultiplied alpha) and their fxMaterial cases (207 = every class's deadEffect: the Wolf's and Sheep's KO must still look right);
FX_PART_FILES += "penguin" (and "tto_penguin": agent tto makes it); Sound.play's handle setVolume(v) (Interfaces 2); Fx.dispose calls
e.dispose?.() on every emitter (Interfaces 3); the cue option scale as [x, y, z] (tto.md P5); decision 16: a "skin" cue kind and the
FX/CosmicRift hero material for Cosmic Rift / Cosmic Friday (cast_b.md "Hero-skin cues": the hero's outfit material swapped for the
cue's time, restored at its end and on the next pick / class change, never leaving a changed material behind); any hero hook agent
penguin needs for Snow Man (decision 17: hide / show the hero's meshes) and for reading the worn weapon (decision 18); the Penguin's
SEQ / tile changes the reports ask for (grep plans/fx_penguin/*.md for SEQ, tile, sequence; e.g. two cast pool members Tornado /
Typhoon, decision 11; no activateIcon1 tile, decision 19). Keep the Wolf, the Sheep and every other class working; existing SEQ
entries' meaning must not change. (3) pipeline/wardrobe_fx_check.py: whatever the new tiles and cue kinds need. (4)
pipeline/wardrobe_fx_inventory.py: add to BUILT the parts in parts.md's list (Penguin_tornado ... Penguin_snowMan) and the TTO ones
agent tto reports (else a TODO in your report), regenerate plans/fx_inventory.md/.json by running it. Run the unit tests afterwards:
py -3 -m unittest pipeline.test_wardrobe_publish pipeline.test_wardrobe_props_tex pipeline.test_repo_rules.` },
  { key: 'tto', owns: 'pipeline/wardrobe_fx_tto.py, wardrobe/fxparts/tto_penguin.js (new), wardrobe/fxparts/shuriken.js, wardrobe/fxparts/groundhug.js, wardrobe/fxparts/arcribbon.js, wardrobe/fxparts/groundfollower.js, plans/fx_penguin/tto.md',
    task: `The Penguin's TTO skills (plans/fx_penguin/tto.md, section 6's parts P1-P6 and P8; not P7: decision 8). (1)
SKILL_FX["penguin"] in wardrobe_fx_tto.py (tto.md's 28 names, so the left-out ones are built too) and CODE_MOVERS for
constellation_line (P1 StarLines), emperorPenguin_ball and emperorPenguin_penguin (P4 EmperorShot / FlockRise). (2) P2: Shuriken's
TrailModule (particle ribbons) in shuriken.js (today in its skip list). P3: the TTO SkinnedMeshRenderer export (vertices, weights,
bind poses in mesh.js's shape) plus the "FlexibleCelShader/Cel No Outline" shader (2-level ramp; register it the way tto_sheep.js
registers TTO shaders, api.shader / FXSHADERS). P6: Unity's built-in Quad (pathID 10210) as a particle mesh. P8: the TTO sounds
emperorPenguin_whistle / emperorPenguin_flock from TTO's bundle (heroes/penguin/sounds). The P5 cue scale [x, y, z] is page_pipeline's.
(3) Decisions in your skills: 6 (Constellation: five stars, the target and 4 foes in a 3 m pentagon about 13 m ahead), 7 (Emperor's
March: the full 22 m run, the Goal at 22.45 m, 1.636 s), 14 (5 penguins), 15 (FocusRedden off), 8 (Frost Field in place). Write the
probed facts and every correction into tto.md (a new section "Built 2026-11-10") with the cue entries ready to paste. (4) The
Wolf's and the Sheep's TTO effects use shuriken.js: they must look the same (if your Trail module changes what they draw, it is
because they have Trail modules the page skipped: say which). (5) Run uv run --no-project --with UnityPy --with pillow --with
imageio-ffmpeg python -I pipeline/wardrobe_fx_tto.py penguin to write the tto/ effects into wardrobe/data/penguin/fx.json (it only
touches tto/ entries and tto_ textures; nobody else builds the Penguin's data before you finish). Report the new part file names
and any cue changes.` },
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
log(`build reports: ${buildNotes.filter(n => typeof n.report === 'object').length}/${BUILD.length}`)

phase('Integrate')
const editor = await agent(
  `${CTX}\n\nYou are the ONE EDITOR for the Penguin (the Sheep was done the same way: NOTES.md 2026-11-10 "the Sheep's effects:
built and cued"). Four builders just finished; their reports (JSON): ${JSON.stringify(buildNotes)}.
You may now edit any file. Do, in order:
1. Apply every shared_change the builders asked for (check each against the code; FX_PART_FILES must list every new part module).
   Make the parts work together.
2. Write wardrobe/fx_cues/penguin.json (valid JSON, the Sheep file's layout) from the reports' ready-to-paste entries, corrected by
   their Verification sections and by plans/fx_penguin/decisions.md (all 20 apply: the 10 m ground point for the Normal Attack,
   missiles at the target 0.6 m up, target-rotation effects at rot [0, 180, 0] (cast_a's manaSurge changes to it), Nova Flare 5 m
   ahead, five Constellation stars, Emperor's March's full run with 5 penguins, Frost Field in place, Double Spell's rerun cues on the
   12 % roll (no clip restart), Tornado / Typhoon as two pool members, Ice Shield / Mana Vortex kill 10, the skin cues for Cosmic Rift /
   Friday, Snow Man hiding the hero, the Staff of Time, no activateIcon1 tile; plus the Sheep / Wolf rules by analogy: self-casts,
   rolls, KO deadEffect on half the plays, emote and KO voices). Every effect the builders made drawable goes in: nothing stays "left
   out" for a missing part. Effects only on enemies stay out (decisions). Each entry's "why" cites file:line.
3. Build the Penguin: uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py penguin,
   then uv run --no-project --with UnityPy --with pillow --with imageio-ffmpeg python -I pipeline/wardrobe_fx_tto.py penguin
   (re-run after the first so the tto/ entries stay); fix every missing effect / sound it reports. Do NOT rebuild the Wolf or the
   Sheep data (git diff wardrobe/data/wolf wardrobe/data/sheep must stay empty).
4. Checks, one at a time (one headless browser at a time):
   uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py ${REPO} checks/fx_penguin --cls penguin --files-only
   uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py ${REPO} checks/fx_penguin dark --cls penguin
   Both must exit 0 with errors []: fix the cause of every failure (page, part, cue or data), re-run until clean.
5. Unit tests: py -3 -m unittest pipeline.test_wardrobe_publish pipeline.test_wardrobe_props_tex pipeline.test_repo_rules.
Never git commit. Report exactly what each check printed at the end.`,
  { label: 'editor:penguin', phase: 'Integrate', schema: RESULT })

phase('QA')
const qa = await agent(
  `${CTX}\n\nYou are the QA pass for the Penguin's effects. The builders and the editor report: ${JSON.stringify({ builds: buildNotes, editor })}.
Assume something is still wrong and find it. One headless browser at a time. Do:
1. Penguin: uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py ${REPO} checks/fx_penguin_qa dark --cls penguin
   then LOOK at the screenshots (open them with the Read tool). The default camera faces the hero, so effects 10 m ahead are behind
   it: use pipeline/wardrobe_fx_probe.py (its "back" view looks ahead from behind the hero; per-effect world boxes; a pool forced to
   one skill; props worn, e.g. specialScepter for the Staff of Time) and pipeline/wardrobe_fx_trace.py (per-frame age / position /
   opacity) where the screenshots can't tell. Does each effect sit where the reports and decisions put it (at the hero, 5 m / 10 m /
   13 m / 22 m ahead, the ball ending at the ground, the missiles at 0.6 m up, the five stars, Snow Man hiding and restoring the hero,
   the Cosmic skin restored), is anything invisible, black, huge, inside-out or flickering? Compare a sample of at least 15 cues
   against the reports' file:line claims and the decisions.
2. No regression in the Wolf and the Sheep (mesh.js, shuriken.js, index.html and the 206 / 207 builtins changed): run
   uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py ${REPO} checks/fx_wolf_qa dark --cls wolf
   uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py ${REPO} checks/fx_sheep_qa dark --cls sheep
   and their --files-only runs; look at their KO deadEffect and TTO effects especially.
3. The rest of the page: pipeline/wardrobe_moves_check.py and pipeline/wardrobe_menu_check.py (read each docstring for the exact
   command line); the unit tests; powershell -ExecutionPolicy Bypass -File pipeline\\test_adopt_from_video.ps1.
4. Fix every real problem you find (any file; never git commit), re-run the affected checks until clean. Thai on-screen text: check
   mark placement where you changed or added any.
Report each check's exact outcome, what you fixed, what is left, and what the user should look at by hand.`,
  { label: 'qa:penguin+sheep+wolf', phase: 'QA', schema: RESULT })

return { builds: buildNotes, editor, qa }
