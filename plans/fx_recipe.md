# Recipe: one skill's effects and sounds

For a session or agent adding a skill's effects and sounds to the wardrobe (the plan: HANDOFF.md "Next up"; the pilot:
NOTES.md 2026-11-09 "skill effects + sounds pilot" and "Feral Strike"). Feral Strike took about 4 minutes this way.
Local only: the public copy has the pilot switched off (`FX_ON`), so nothing here needs a publish.

What each step touches: one class's cue file `wardrobe/fx_cues/<cls>.json` (tracked), and that class's built data
`wardrobe/data/<cls>/fx.json`, `wardrobe/data/<cls>/sfx/`, `wardrobe/data/fx/tex/` (not in git). Never `index.html`:
if a skill needs a part the page doesn't build, that is a separate job (below).

## 1. Find what the game does

1. The skill's clip name(s): the ท่าสกิล list, or `wardrobe/data/<cls>/clips.json` (group `skill`). A skill that plays
   several clips in a row is one sequence tile (`SEQ` in `index.html`); cues still belong to the clip they start with.
2. Behaviour first from the Bible: `D:\12tails\12t_reference\<cls>-skill-reference.md` and the skill card in
   `12t_projects/bible/index.html` (office: `C:\Users\Jump\Desktop\12tails\...`). **Max rank** everywhere (the user's
   rule): where the code picks an effect or a clip by `sLv`, take the top rank's.
3. The coroutine: usually `RPC_<skill>` in `DecompiledSource\<Class>.cs`. Its flow with the effect and sound lines:

   ```
   node pipeline/clip_flow.js D:/12tails/DecompiledSource/Wolf.cs RPC_crossBreak "Effects/|Voices/|Sounds/|createEffect|Instantiate|PlayOneShot"
   ```

   It is a flattened state machine: `return this.Yield(5, new WaitForSeconds(0.4f))` = wait 0.4 s, then go on at
   `case 5:`. Follow the case numbers from the clip's `PlayAnimation` (time 0) and add up the waits to each
   `createEffect` / `Instantiate` (an effect) and `audio.PlayOneShot` (a voice). `Random.Range(0, 2) == 0` choosing
   between two loads = a random pick, written `"a|b"`. A second RPC the coroutine starts (a release, a hit) has its own
   clip and its own cues. `Debug.LogError("Cannot find ... Effect")` lines name the prefab too.
4. Where it spawns: `hero position` (+ `rotation`) = distance 0; `position + 0.6f * transform.forward` = 0.6. An effect
   spawned **at the target** (hits on an enemy, `target.position`) is left out: the wardrobe has no target (the pilot's
   rule; say so in `why`). A buff the skill puts on the hero itself stays (distance 0).
5. When the effect's `EffectControl` has `followState` (shown by `wardrobe_fx.py --fx <name>` in `fx.json`), the game
   ends it when the hero's `actionState` changes: the clip time of that change (the coroutine's `actionState =
   "standby"`) is the cue's 5th value.

Worked example, Cross Break (`Wolf.cs`): `PlayAnimation("crossBreak", 0.2f)` at 0 (:24078); voice crossBreak1 or 2
(:24119-24223) at 0; `crossBreak_ring` created at the hero at 0.1 s (:23748); `crossBreak` instantiated 0.6 m ahead
at 1.2 s (:23896).

## 2. Check every effect is buildable

Look the effect up in `plans/fx_inventory.md` ("Per effect", your class): **ready** = the page builds all its parts and
`wardrobe_fx.py` extracts it. An effect that "needs" a part (AlphaTimer, ProjectileControl, a class script, ...) gets
that part BUILT before the class is done (user 2026-11-10: "when you need parts the page don't have yet, you have to
make it work, we are top quality!"): a parts stage, one agent per part with its own files (`plans/fx_wolf/build_rules.md`),
then the cues. A single-skill job that meets one notes it for that stage instead of building it inline. `pipeline/wardrobe_fx_inventory.py` rewrites the inventory (after a part is built, add
it to its `BUILT` and run it again).

## 3. Write the cues

In `wardrobe/fx_cues/<cls>.json`, one entry per clip, keyed by the clip's name:

```json
  "crossBreak": {
    "why": "RPC_crossBreak: clip, voice crossBreak1 / 2 (:24078-24223); crossBreak_ring at 0.1 s (:23748); the cross 0.6 m ahead at 1.2 s (:23896)",
    "cues": [
    [0, "voice", "crossBreak1|crossBreak2"],
    [0.1, "fx", "crossBreak_ring"],
    [1.2, "fx", "crossBreak", 0.6]
    ]
  }
```

A cue: `[seconds after the clip starts, "fx" | "voice", name ("a|b" = random pick), metres ahead (optional, 0),
the clip time the hero's action changes (optional, for followState effects)]`. `why` cites the source lines (file:line)
for every time and name. Only voices go in as `"voice"`: a sound an effect plays itself (its AudioSource) comes with the
effect. The file must stay valid JSON (`py -3 -c "import json; json.load(open('wardrobe/fx_cues/<cls>.json', encoding='utf-8'))"`).

## 4. Build and check

```
uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I pipeline/wardrobe_fx.py <cls>
uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py D:/12tails-wardrobe checks/fx_<cls> dark --cls <cls>
```

The build takes every effect and voice the cue file names (it reads `12TailsOnline_Data` in the Bible folder; both
PCs have it). The check must exit 0: it fails on a named effect or voice missing from the data, a cued effect that never
spawns (a cue key that isn't a clip of the class shows as "no tile ... in the <group> tab"; emote and basic-move keys
are played from their own tab, 2026-11-10), and any page error. Emotes and basic moves: see NOTES.md 2026-11-10 (the
Wolf's emote voices, from `RPC_emotion`, `RPC_ko`, `RPC_dead`). Then look at
`checks/fx_<cls>/compare.html` (or the `_peak.png` shots): the effect should sit where the game puts it. Headless checks
run one at a time on this PC.

## 5. Record

A line in NOTES.md's session log (the skills done, anything odd, open points). A new game-mechanic finding (a timing
the Bible's reference lacks) is offered to the user for the Bible (its own repo and rules), never written there from
here. The built data isn't in git: the other PC needs it carried (`transfer_to_drive.ps1`) or rebuilt with the build
line above; put that in HANDOFF.md.
