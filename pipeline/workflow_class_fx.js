export const meta = {
  name: 'class-fx',
  description: "One 12 Tails class's skill effects + sounds: research (6 readers + 3 checkers) or build (planner, builders, editor, QA)",
  phases: [
    { title: 'Research', detail: 'six read-only researchers, one report each in plans/fx_<cls>/' },
    { title: 'Verify', detail: 'three checkers append ## Verification' },
    { title: 'Plan', detail: 'decisions.md + the builders split' },
    { title: 'Build', detail: 'builders on disjoint files' },
    { title: 'Edit', detail: 'one editor: cues, tiles, icons, data, the gate' },
    { title: 'QA', detail: 'wardrobe_fx_shots.py on dark and white, fixes, gates' },
  ],
}

const A = args
const cls = A.cls, Cls = A.Cls
const REPO = 'C:/work/12tails-wardrobe'
const ENV = `Environment (office PC): this repo is ${REPO}. The Bible repo (read only) is C:/Users/Jump/Desktop/12tails: DecompiledSource/ (BB's decompiled C#), DecompiledSource_TTO_2026-11-02 (cited "TTO1102:"; also _2026-11-06, _2026-11-09), 12t_reference/${cls}-skill-reference.md, 12t_projects/bible/index.html (skill cards), 12TailsOnline_Data (the BB rip wardrobe_fx.py reads). Reports written at the home PC cite D:/12tails/... : the same files are at C:/Users/Jump/Desktop/12tails/... here. The video repo (read only, never write or commit there) is C:/work/12tails-video. TTO bundles: wardrobe_fx_tto.py finds this repo's git-ignored tto_assets/2026-11-09 by itself. Git-ignored scratch under checks/ from the home PC's runs (checks/fx_<cls>_research/...) is NOT on this PC: re-probe what you need. Python: \`uv run --no-project --with <pkgs> python -I ...\` or \`py -3\`, never a global pip install. Never commit, never push, never deploy (the lead does). Never touch plans/reskins/. The Edit tool can rewrite wardrobe/index.html with CRLF: after any edit of it, \`grep -c $'\\r$' wardrobe/index.html\` must print 0 (convert back to LF if not).`
const RULES = `Standing rules (the user's): the top rank's effects where the code picks by rank, passives on; random picks as the game makes them; effects on an enemy go to the target point 10 m ahead (homing aims 0.6 m up); long buffs / fields / summons cut at 10 s; one tile per skill with its Bible icon (pool members one tile each); skills with no body clip get effect-only tiles on the idle stance; every missing page part is BUILT, never left out; TTO skills included but cued only if in wardrobe/tto_released.json (for ${cls}: ${A.released.join(', ') || 'none'}); game behaviour from the Bible first, the decompiled code for the rest. The user is not available: decide by these rules and by the earlier classes' decisions (plans/fx_<cls>/decisions.md of wolf, sheep, penguin, bat, bison, cat, chameleon, mole) by analogy, and write each call down.`
const MODELS = `Models for format and depth: plans/fx_recipe.md; NOTES.md from "## 2026-11-13 (overnight, home), every class's skill effects: the run" to the end (the Chameleon's section is the last full class); plans/fx_chameleon/ and plans/fx_mole/ (the same report names).`

function researcher(role, scope) {
  return `You are the \`${role}\` researcher for the ${Cls}'s skill effects + sounds in the 12 Tails Wardrobe.
${ENV}
READ ONLY: the only repo file you write is plans/fx_${cls}/${role}.md (create the folder if missing); probe scripts and their outputs go under checks/fx_${cls}_research/${role}/ (git-ignored). Never run pipeline/wardrobe_fx.py or wardrobe_fx_tto.py without --probe, never edit any other repo file, no browser.
${MODELS} Your model reports are plans/fx_mole/${role}.md and plans/fx_chameleon/${role}.md: match their structure (a short summary, "Read this first", per item with file:line citations for every time, name and position, paste-ready cue entries for wardrobe/fx_cues/${cls}.json in the page's CURRENT cue format: read the cue-format comment in wardrobe/index.html and the existing wardrobe/fx_cues/*.json, parts needed, left out (with reasons), open questions each with your recommended answer, offers for the Bible (never written there)).
${RULES}
Your scope: ${scope}
Use the tools the earlier researchers used (pipeline/clip_flow.js, pipeline/clip_calls.js, wardrobe_fx.py ${cls} --probe <effects>, wardrobe_fx_tto.py ${cls} --probe, plans/fx_inventory.md "Per effect"). The decompiled code has opaque predicates (if (a - b == c) junk): evaluate them, as the earlier reports did.
Return a 3-line summary: what you covered, how many cue entries, the biggest open point.`
}

function checker(roles) {
  return `You are a checker for the ${Cls}'s skill effects research in the 12 Tails Wardrobe.
${ENV}
Check these reports: ${roles.map(r => `plans/fx_${cls}/${r}.md`).join(' and ')}. For each one, re-derive its claims from the sources: the clip names and timings (the coroutine's waits added up), every effect / voice / sound name exists (wardrobe_fx.py ${cls} --probe, the rip), positions and distances, rank picks, the TTO released rule, that the paste-ready cue entries are valid JSON in the page's current cue format (wardrobe/index.html's cue-format comment, existing wardrobe/fx_cues/*.json) and their keys are real clips of the class (wardrobe/data/${cls}/clips.json) or the page's SEQ "@Skill:clip" keys. Also look for anything missed (a skill, a voice, an effect, a needed part).
Append a "## Verification (<date>)" section at the end of EACH report: numbered findings, each with what is wrong, the evidence (file:line) and the corrected value or block (corrected paste-ready blocks in full where a block changes). The Verification wins over the report body. Touch nothing else in the repo (probes under checks/fx_${cls}_research/verify/). Never run wardrobe_fx.py without --probe. No browser.
${RULES}
Return a 2-line summary: how many findings, the most important.`
}

if (A.mode === 'research') {
  const own = A.skillClips.filter(c => !/^(nAttack|cAttack)/.test(c))
  const half = Math.ceil(own.length / 2)
  const sa = own.slice(0, half), sb = own.slice(half)
  const emoteClips = A.ttoEmotes || []
  const ROLES = [
    ['attacks_emotes', `the Normal Attack (clips ${A.skillClips.filter(c => /^nAttack/.test(c)).join(', ')}) with its combo / passives, the Charge Attack (clips ${A.skillClips.filter(c => /^cAttack/.test(c)).join(', ') || '(none: find what the charge plays)'}) and its releases, every emote and basic move (the class's emote / basic-move clips in wardrobe/data/${cls}/clips.json, TTO-only emote clips ${emoteClips.join(', ')}: silent unless code plays a voice), RPC_emotion / RPC_ko / RPC_dead (KO, deadEffect), run footsteps.`],
    ['skills_a', `the skill clips ${sa.join(', ')} and every skill that plays them (pools: one tile per member).`],
    ['skills_b', `the skill clips ${sb.join(', ')} and every skill that plays them (pools: one tile per member).`],
    ['tto', `the TTO skill clips ${A.ttoClips.join(', ')} (wardrobe/data/${cls}/clips.json tto: true; released: ${A.released.join(', ')}): TTO's code (pseudo-C and dump in the TTO decompiles), their prefabs in TTO's bundles (wardrobe_fx_tto.py ${cls} --probe), the cue entries for the released ones, the parts they need.`],
    ['effect_only', `every skill of the ${Cls} that plays NO body clip (its dispatcher plays no PlayAnimation): account for every RPC_* in DecompiledSource/${Cls}.cs (a table: RPC, skill, clip or none, covered by which report), check each passive, and write the effect-only tiles on the idle stance ("<Skill Name>: root*@<t>" SEQ lines, keys "@Skill:root") with their cues.`],
    ['parts', `every page part the ${Cls}'s effects need: run wardrobe_fx.py ${cls} --probe over all its effect prefabs (heroes/${cls}/effects) and the TTO released skills' prefabs; list the scripts with field bytes and no layout (paste-ready LAYOUTS for pipeline/wardrobe_fx.py), the components effect() drops, shaders the page lacks (wardrobe/fxparts/ has what is built), the hero code acting on its effects, summons; plans/fx_inventory.md's per-effect status for the class. End with "## Who builds what": up to four builders on disjoint files (each new part in its own wardrobe/fxparts/<name>.js; one page_pipeline builder owning wardrobe/index.html + pipeline/wardrobe_fx.py + wardrobe_fx_tto.py when those change), and "## Interfaces" fixed up front so the builders run in parallel.`],
  ]
  phase('Research')
  const reports = await parallel(ROLES.map(([role, scope]) => () =>
    agent(researcher(role, scope), { label: `research:${cls}:${role}`, phase: 'Research' })))
  log(`${Cls} research: ${reports.filter(Boolean).length}/6 reports`)
  phase('Verify')
  const PAIRS = [['attacks_emotes', 'effect_only'], ['skills_a', 'skills_b'], ['tto', 'parts']]
  const checks = await parallel(PAIRS.map(p => () =>
    agent(checker(p), { label: `verify:${cls}:${p.join('+')}`, phase: 'Verify' })))
  return { cls, mode: 'research', reports, checks }
}

// ---- build ----
const DOCS = `Read first: plans/fx_${cls}/decisions.md (decided overnight; it wins over the reports), the six reports plans/fx_${cls}/{attacks_emotes,skills_a,skills_b,tto,effect_only,parts}.md, each with its "## Verification" (which wins over the report body), plans/fx_recipe.md, and NOTES.md's skill-effects sections (from "## 2026-11-13 (overnight, home), every class's skill effects: the run" to the end: how the Bat, Bison, Cat and Chameleon were built, the gotchas, the page's current parts).`

let groups = A.groups
if (!groups) {
  phase('Plan')
  const plan = await agent(`You are the build planner for the ${Cls}'s skill effects + sounds in the 12 Tails Wardrobe.
${ENV}
Read the six reports plans/fx_${cls}/{attacks_emotes,skills_a,skills_b,tto,effect_only,parts}.md with their "## Verification" sections (they win), and as models plans/fx_mole/decisions.md and plans/fx_chameleon/decisions.md.
${RULES}
Write plans/fx_${cls}/decisions.md: titled "# ${Cls} effects: decisions (<date>), decided overnight, for the user's review", numbered decisions grouped as the Mole's (Tiles and sequences, Where things land, summons / special, Passives ranks rolls voices sounds, Left out, Parts and data, Offered to the user for the Bible), each with a one-line reason; decide every open question of the reports. Write no other repo file.
Then split the build into at most four builders on DISJOINT files (parts.md "Who builds what" is the starting point): each new page part in its own wardrobe/fxparts/<name>.js; ONE builder named page_pipeline owns wardrobe/index.html + pipeline/wardrobe_fx.py + pipeline/wardrobe_fx_tto.py if any of them changes. The editor (after the builders) owns wardrobe/fx_cues/${cls}.json, pipeline/wardrobe_skill_icons.py, pipeline/wardrobe_fx_check.py, pipeline/wardrobe_fx_inventory.py and the data build; do not give those to builders. Each builder's task names the decisions and report sections it implements and the interfaces it codes against.`,
    { label: `plan:${cls}`, phase: 'Plan', schema: {
      type: 'object', required: ['groups'], properties: { groups: { type: 'array', items: {
        type: 'object', required: ['name', 'owns', 'task'],
        properties: { name: { type: 'string' }, owns: { type: 'array', items: { type: 'string' } }, task: { type: 'string' } } } } } } })
  groups = (plan && plan.groups || []).slice(0, 4)
  log(`${Cls} plan: ${groups.map(g => g.name).join(', ')}`)
}

const others = g => groups.filter(x => x !== g).map(x => `${x.name}: ${x.owns.join(', ')}`).join('; ')
phase('Build')
const built = await parallel(groups.map(g => () => agent(`You are the \`${g.name}\` builder for the ${Cls}'s skill effects in the 12 Tails Wardrobe (three.js page wardrobe/index.html, effect parts in wardrobe/fxparts/, data built by pipeline/wardrobe_fx.py / wardrobe_fx_tto.py).
${ENV}
${DOCS}
You own ONLY: ${g.owns.join(', ')}. Other builders run at the same time and own: ${others(g) || 'nobody else'}. The editor after you owns wardrobe/fx_cues/${cls}.json, pipeline/wardrobe_skill_icons.py, pipeline/wardrobe_fx_check.py, pipeline/wardrobe_fx_inventory.py and the data rebuild. Never edit a file you don't own; anything you need there goes in your return as "for the editor" / "for <builder>" with the exact change. Code against parts.md's "## Interfaces" and the existing part API (read wardrobe/index.html's Fx code and two existing parts, e.g. wardrobe/fxparts/cat.js and chameleon.js, for how a part registers and what api it gets).
Your task: ${g.task}
${RULES}
Rules for builders: \`node --check\` every JS file you write; no browser; never run wardrobe_fx.py ${cls} or wardrobe_fx_tto.py ${cls} without --probe (the editor rebuilds once; --probe is fine to test your extraction code paths); keep the other classes working (the page code is shared). A part that needs another node of its effect must look it up when it is due, not when the part is built (the Bat's gotcha).
Return: what you built (file, function, which decision / report item), the interfaces you expose, anything left for the editor (exact), and anything you could not finish.`,
  { label: `build:${cls}:${g.name}`, phase: 'Build' })))

phase('Edit')
const edited = await agent(`You are the ONE editor for the ${Cls}'s skill effects + sounds in the 12 Tails Wardrobe, after the builders.
${ENV}
${DOCS}
The builders' reports (their "for the editor" items are yours to apply):
${groups.map((g, i) => `--- ${g.name} (owned ${g.owns.join(', ')}):\n${built[i] || '(no report: the builder died; check its files and finish what its task needed)'}`).join('\n')}
Your job, in order:
1. Write wardrobe/fx_cues/${cls}.json from the reports' paste-ready blocks (the corrected ones: Verification and decisions.md win), merged where two reports touch one key; valid JSON; \`why\` cites file:line. Apply decisions.md everywhere it differs from the blocks.
2. The page lines the builders left to you (SEQ / SEQ_SKILL / NEVER_PLAYED / LIFTS / FX_PART_FILES in wardrobe/index.html if not done by page_pipeline), pipeline/wardrobe_skill_icons.py's ${cls} entries (CLIP_SKILLS / OWN_TILE / EFFECT_ONLY as decisions.md says) and run it, pipeline/wardrobe_fx_check.py (new kinds / OPTS / ENTRY_KEYS), pipeline/wardrobe_fx_inventory.py BUILT += the new parts (and run it).
3. Build the data: \`uv run --no-project --with UnityPy --with pillow python -I pipeline/wardrobe_fx_tto.py ${cls}\` (if the class has released TTO cues) then \`uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py ${cls}\` (check each docstring for the exact line and flags). Fix extraction errors at their root.
4. The gate, one headless check at a time: \`uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py ${REPO} checks/fx_${cls} dark --cls ${cls}\` must exit 0 with errors [] and every cued effect spawned; the files-only check must say "no problems". The page / shared parts changed, so also the regression run \`--cls ${A.regress}\` (checks/fx_${cls}_regress): exit 0, errors []. Then the unit tests (\`py -3 -m unittest pipeline.test_wardrobe_publish pipeline.test_wardrobe_props_tex pipeline.test_repo_rules pipeline.test_wardrobe_community\`, \`node --test pipeline/test_site_worker.mjs\`, \`powershell -ExecutionPolicy Bypass -File pipeline\\test_adopt_from_video.ps1\`) and \`uv run --no-project --with playwright python -I pipeline/wardrobe_weapon_fx_check.py\` (see its docstring for args). Fix every failure at its root (in any file; the builders are done). A skill that still can't be made right is left out of the cues and listed for NOTES.md.
5. Append to NOTES.md a section "## <date> (office), the ${Cls}'s effects: built and cued" in the Chameleon section's shape: Parts (new), Cues (counts), Tiles / icons, Data (what was built, file counts), Judgement calls (mine), Gate (exact results), For the QA pass, For the Bible (offer, not written). index.html must stay LF.
Do NOT commit. Return: the gate results (exit codes, tile plays, errors), the counts (cue keys, cues, effects, sounds), what is left out and why, the changed / new files list (paths), and anything for the QA.`,
  { label: `edit:${cls}`, phase: 'Edit' })

phase('QA')
const qa = await agent(`You are the QA pass for the ${Cls}'s skill effects + sounds in the 12 Tails Wardrobe, after the editor.
${ENV}
${DOCS}
The editor's report:
${edited}
Do what the earlier classes' QA passes did (NOTES.md: the Chameleon's "QA pass" bullet is the model): write checks/fx_${cls}_qa/jobs.json covering every ${Cls} tile (worn-weapon variants where cues use worn / notWorn, TTO tiles, KO, emotes, long tiles to their end), shoot them with pipeline/wardrobe_fx_shots.py --jobs (virtual clock; read its docstring) on the dark and the white stage, build the contact sheets with pipeline/wardrobe_fx_sheet.py (checks/fx_${cls}_qa/sheets_dark, sheets_white), and LOOK at the shots (Read the PNGs): each effect where and when the reports and decisions say, nothing hanging in the air, nothing missing, no stalled render loop, no page errors. One headless browser at a time. Fix real bugs at their root (any file), then re-run the gate \`uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py ${REPO} checks/fx_${cls}_qa/gate dark --cls ${cls}\` and, if shared page / part code changed, the regression \`--cls ${A.regress}\`, plus the unit tests and wardrobe_weapon_fx_check.py. index.html must stay LF.
Append a "- **QA pass (<date>, office).**" bullet to the editor's NOTES.md section: what was shot (jobs, shots), what matches, bugs found and fixed (with file), looked into and not bugs, the final gates, and "for the user's eye" items. Do NOT commit.
Return: PASS or FAIL on the final gates (with exit codes and errors), bugs fixed, files changed, items for the user's eye.`,
  { label: `qa:${cls}`, phase: 'QA' })

return { cls, mode: 'build', groups: groups.map(g => g.name), built, edited, qa }
