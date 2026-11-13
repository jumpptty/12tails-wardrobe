"""Headless check of the skill effects and sounds (2026-11-09 pilot: Wolf Armor Break, Cross Break, Grand Cross, Feral
Strike). For every class with cues (wardrobe/fx_cues/<cls>.json, or --cls a,b): first the files, every effect a cue
names in data/<cls>/fx.json and every voice in data/<cls>/sfx; then the page, each cued clip's tile played (the
sequence tile when the clip is one of its steps), which effects are alive (and their emitters' vertex counts) sampled
over time, a screenshot shortly after each effect first appears and one at the busiest frame (peak), once per backdrop
(?fxbg=dark = the page's dark background, white = its default, side by side in <out>/compare.html). Fails on a missing file, a cued effect that never
spawns, a page error, a console error or a failed request.
  uv run --no-project --with playwright python -I pipeline/wardrobe_fx_check.py D:/12tails-wardrobe checks/<dir> [dark,spot,white] [--cls wolf]
--files-only: only the file checks (no browser; 2026-11-09, the user tests the page by hand): every effect, voice
(v_<name>.mp3) and sound (<name>.mp3) the cues name, every cue's shape, and that each cue key is a clip of the class.
A key "@<sequence>:<clip>" (2026-11-10, the Sheep: index.html cueOf) is that clip's cues when the sequence plays it: the
sequence must be one of the class's in index.html's SEQ and play the clip, and its tile is played. A "skin" cue (2026-11-10,
the Penguin's Cosmic Rift / Cosmic Friday: the hero's own look, index.html HERO_SKINS) names one of the page's skins; in
the page it must take hold (FX.spawned "skin:<name>") like an effect. 2026-11-13, the Bat: a "clone" cue (a copy of the
dressed hero, index.html HeroClone) names a clip of the class and must appear (FX.spawned "clone:<clip>"); an entry's
"builds" (what a page part spawns, api.spawn, or plays: "sound:<name>" / "voice:<name>") must be in the data too, and
its effects must spawn (the page counts them in FX.spawned); "everyCycle": true is a flag (the run's wing flap).
2026-11-13, the Bison (plans/fx_bison/decisions.md 1, 2, 22): a SEQ step may hold alternatives "a|b" (each with its own
fade / @t / %p, index.html seqStep): every alternative's clip belongs to the sequence, and a sequence tile with
alternatives is played once per alternative (the page's test hook window.__seqAlt forces the pick), so each one's cues
are checked; a "lift" cue (the hero raised along a curve, index.html LIFTS / HeroLift) names one of the page's LIFTS and
must take hold (FX.spawned "lift:<name>"). 2026-11-13, the Cat (plans/fx_cat/decisions.md 47, 58): a "hideProp" cue
names a prop slot (R, L, Head, Back) and carries a kill; it is not expected in the tally (it takes hold only while a prop
is worn there: FX.spawned "hideProp:<slot>"); since the Chameleon (2026-11-13, plans/fx_chameleon/decisions.md 13, 48, 49)
it may name "hero" (the whole hero hidden) and may leave out its kill (hidden until the next pick); SEQ tokens such as root*~@5.65, dropAnchor! and crescentEclipse2^ give their
clip names (seqs). 2026-11-13, the Whale (plans/fx_whale/decisions.md 31, 32, 66): a cue's rot is checked (rot_ok: three
angles, each a number, "random" or a [lo, hi] pair of whole numbers; or the words "random" / "randomYaw"), around is
[lo, hi] whole metres, withRot is true and only beside atBone."""
import argparse, asyncio, functools, http.server, json, re, sys, threading
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("root", type=Path)
ap.add_argument("out", type=Path)
ap.add_argument("variants", nargs="?", default="dark,white")
ap.add_argument("--cls", default="", help="classes to check (default: every class whose cue file has cues)")
ap.add_argument("--files-only", action="store_true", help="the file checks alone, no browser")
A = ap.parse_args()
ROOT, OUT, VARIANTS = A.root, A.out, A.variants.split(",")
OUT.mkdir(parents=True, exist_ok=True)
CUE_DIR, DATA = ROOT / "wardrobe" / "fx_cues", ROOT / "wardrobe" / "data"
CUES = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(CUE_DIR.glob("*.json"))}
CLASSES = A.cls.split(",") if A.cls else [c for c, t in CUES.items() if t]


def seqs():
    """index.html's SEQ: {cls: {sequence id (its name without spaces): [[each step's alternative clips]]}} (a step "a|b"
    lists both, index.html seqStep: the clip name before *, ~t, ^, !, @t, %p)."""
    html = (ROOT / "wardrobe" / "index.html").read_text(encoding="utf-8")
    block = re.sub(r"//[^\n]*", "", re.search(r"\nconst SEQ = \{(.*?)\n\};", html, re.S).group(1))
    out, cls = {}, None
    for m in re.finditer(r'(\w+): \[|"([^"]+)"', block):
        if m.group(1):
            cls = m.group(1); out[cls] = {}
        else:
            name, body = m.group(2).split(": ", 1)
            out[cls][name.replace(" ", "")] = [[re.match(r"\w+", a).group(0) for a in t.split("|")] for t in body.split()]
            RAW.setdefault(cls, {})[name.replace(" ", "")] = [t.split("|") for t in body.split()]
    return out


RAW = {}            # {cls: {sequence id: [[each step's alternative tokens]]}}: their @t holds (play_time)
SEQS = seqs()


def play_time(cls, sq, force):
    """The seconds a play of sequence sq takes before its last step starts (each earlier step's @t hold of the alternative
    played, else its clip's length): the cap waits that long more (2026-11-13, the Monkey's Summon Gaos: its 8 s bar,
    then the Gaos' unsummon ring 10 s after the release)."""
    clips = json.loads((DATA / cls / "clips.json").read_text(encoding="utf-8"))
    total = 0.0
    for i, alts in enumerate(RAW.get(cls, {}).get(sq, [])[:-1]):
        tok = alts[min((force or {}).get(i, 0), len(alts) - 1)]
        m = re.search(r"@([\d.]+)", tok)
        total += float(m.group(1)) if m else clips.get(re.match(r"\w+", tok).group(0), {}).get("len", 0)
    return total


def seq_clips(cls, sq):
    """Every clip sequence sq of the class may play (each step's alternatives)."""
    return [c for alts in SEQS.get(cls, {}).get(sq, []) for c in alts]


def seq_plays(cls, sq):
    """The plays that show every alternative once: for k = 0 .. the most alternatives a step has - 1, ({step index:
    k for each step with alternatives}, the clip each step then plays); one play ({}, the clips) when none has any."""
    steps = SEQS[cls][sq]
    n = max([len(a) for a in steps] or [1])
    return [({i: min(k, len(a) - 1) for i, a in enumerate(steps) if len(a) > 1}, [a[min(k, len(a) - 1)] for a in steps])
            for k in range(n)]


def hero_skins():
    """index.html's HERO_SKINS: the names a "skin" cue may give."""
    html = (ROOT / "wardrobe" / "index.html").read_text(encoding="utf-8")
    block = re.search(r"\nconst HERO_SKINS = \{(.*?)\n\};", html, re.S)
    return set(re.findall(r'^  "([^"]+)":', block.group(1), re.M)) if block else set()


SKINS = hero_skins()


def lifts():
    """index.html's LIFTS: the names a "lift" cue may give (2026-11-13, the Bison's Titan Drop)."""
    html = (ROOT / "wardrobe" / "index.html").read_text(encoding="utf-8")
    block = re.search(r"\nconst LIFTS = \{(.*?)\n\};", html, re.S)
    return set(re.findall(r'^  "?(\w+)"?:', block.group(1), re.M)) if block else set()


LIFT_NAMES = lifts()


def split_key(key):
    """A cue key's (sequence id or None, clip): "@Eden Sanctuary:cast3" and "@EdenSanctuary:cast3" are one key; a step's
    own key "@<sequence>:<clip>#<step index>" (2026-11-13, the Monkey's Earth Form Attack, index.html fxStart) gives the
    clip without its "#<n>" (key_step: n)."""
    if key.startswith("@") and ":" in key:
        sq, clip = key[1:].split(":", 1)
        return sq.replace(" ", ""), clip.split("#", 1)[0]
    return None, key


def key_step(key):
    """A step's own key's step index ("@EarthFormAttack:summonAttack#2" -> 2), else None."""
    m = re.search(r"#(\d+)$", key) if key.startswith("@") else None
    return int(m.group(1)) if m else None


def entry_for(cls, sq, clip, step=None):
    """The entry the page runs for a clip in a play of sequence sq (None: a single clip), as fxStart looks it up: the
    step's own key first ("@<sequence>:<clip>#<step>"), then the sequence's, then the clip's."""
    for want in ((sq, clip, step), (sq, clip, None)):
        for key, e in CUES[cls].items():
            if sq and (*split_key(key), key_step(key)) == want:
                return e
    return CUES[cls].get(clip, {})


def alt_view(e, alt):
    """The entry as a play with this step's alternative drawn (index.html fxStart's `alt` filter): a cue with an "alt" k
    plays only when the step's alternative is k (2026-11-13, the Monkey's Summon Gaos: the 8 s bar or the instant one)."""
    keep = lambda cues: [c for c in cues if not (len(c) > 3 and isinstance(c[3], dict) and "alt" in c[3] and c[3]["alt"] != alt)]
    out = dict(e, cues=keep(e.get("cues", []))) if "cues" in e else dict(e)
    if "skills" in e:
        out["skills"] = {n: dict(m, cues=keep(m.get("cues", []))) for n, m in e["skills"].items()}
    return out


SHOT_AFTER = 0.15     # seconds after an effect first appears
SETTLE, CAP = 1.5, 15.0   # stop a tile this long after its last expected effect appeared, or at CAP + its last cue's time


def cue_lists(entry):
    """An entry's cue lists: its cues, or every skill's of a shared clip ({skills: {name: {cues}}})."""
    return [entry.get("cues", [])] + [s.get("cues", []) for s in entry.get("skills", {}).values()]


def all_cues(cls):
    return [c for e in CUES[cls].values() for cues in cue_lists(e) for c in cues]


def builds(e):
    """An entry's "builds" as (kind, name): "sound:<name>" / "voice:<name>" / ["sound", name], else an effect (as
    wardrobe_fx.builds reads them); a pool's skills may carry their own."""
    out = []
    for x in [e] + list(e.get("skills", {}).values()):
        for b in x.get("builds", []) if isinstance(x.get("builds", []), list) else []:
            if isinstance(b, list) and len(b) == 2:
                out.append((b[0], b[1]))
            elif isinstance(b, str) and ":" in b and b.split(":", 1)[0] in ("fx", "sound", "voice"):
                out.append(tuple(b.split(":", 1)))
            else:
                out.append(("fx", str(b)))
    return out


def names(cls, kind):
    return sorted({n for c in all_cues(cls) if c[1] == kind for n in str(c[2]).split("|")}
                  # (a builds name "a|b": a part's random pick, built in full, not expected: the Rabbit's turret drops)
                  | {n for e in CUES[cls].values() for k, b in builds(e) if k == kind for n in b.split("|")})


def expected(entries):
    """The effects every play of these entries must show, as the page tallies them (FX.spawned): fx cues, "skin:<name>",
    "clone:<clip>" (their "a|b" picks and rolled procs vary: not expected; nor a "worn" cue's, which needs an item the
    check's default dress lacks: the Bat's Homing Wand hits), and the effects their "builds" names."""
    out = {("skin:" if cue[1] == "skin" else "clone:" if cue[1] == "clone" else "lift:" if cue[1] == "lift" else "") + cue[2]
           for e in entries for cue in e.get("cues", [])
           if cue[1] in ("fx", "skin", "clone", "lift") and "|" not in cue[2]
           and not (len(cue) > 3 and isinstance(cue[3], dict) and ("p" in cue[3] or "worn" in cue[3]))}
    return sorted(out | {n for e in entries for k, n in builds({"builds": e.get("builds", [])}) if k == "fx" and "|" not in n})


# index.html cueOf (2026-11-10, the Penguin: spread; i, n and ignite, passed on to the TTO parts, plans/fx_penguin/tto.md;
# hideHero for penguin.js's snowman; notWorn [slot, item], fxStart: the Staff of Time's missing landings; 2026-11-13, the
# Bat: worn [slot, item] (the Homing Wand's hits), end (the guardian's unsummon, fxparts/bat.js); a "clone" cue takes x,
# y, d, kill)
# 2026-11-13, the Cat (plans/fx_cat/decisions.md 37, 50, 58): single (no second copy while one lives: its kill renewed,
# index.html fxDue), anims (fx:grandCasinoArcade's clip schedule, fxparts/cat.js); the TTO parts' (fxparts/tto_cat.js,
# plans/fx_cat/tto.md 2.1-2.3): flip, pulse, gather, gatherTo, hand (Royal Flush's cards and banner), eclipse, recall,
# home (Crescent Eclipse's moon and blades)
# 2026-11-13, the Chameleon (plans/fx_chameleon/decisions.md 30, 32, 48, 55, 56, 59, 60, 62): strafe (the Double Strider
# clone's m/s along its right), speed (the arrow's m/s, fxparts/chameleon.js), fatal (Fatal Strike's blood on the arrow),
# slot (the prop the arrow copies), r (Needle Prison's ring), life (the root EffectControl's life, index.html Fx), stop
# (seconds after the spawn: every Shuriken system stops emitting), all (a hideProp's weapon_fx particles hidden too); the TTO
# parts' (fxparts/tto_chameleon.js, plans/fx_chameleon/tto.md 7): bow, face, slide, slots (the ghosts), ghost, shatterGhosts
# (a beam's and the rupture's), lockOnly, release, tint (the prey reticle: its race colour), from (a lightning bolt's
# start); radius (Needle Prison's ring, as r: skills_a.md's block)
# 2026-11-13, the Mole (plans/fx_mole/decisions.md 19, 22, 24, 26, 35, 37, 42, 46, 59): tune (the Trumpet's notes in turn),
# firePoint (the worn cannon's muzzle), tilt (Grenade Cluster's per-grenade pitch), pick ("color": the outfit colour's
# name), playAudio (the root AudioSource started), clip (the King Kaiser's), host (a living effect's bone), pair (a TTO
# missile's twin pair), trigger (Flame Carnival's, never cued); the TTO parts' (fxparts/tto_mole.js): finish, ride, shots,
# rideEnd, tier (the rail turret and its beam), sink, kicks, launch, egg (the missile pad), fold (the arsenal pods)
# 2026-11-13, the Monkey (plans/fx_monkey/decisions.md 9, 24, 31, 37-39, 66): alt (the step's drawn alternative, index.html
# fxStart); the summons' and armours' (fxparts/elementals.js): alpha, standing, hide, moves, turn, attach, boost; Lavu's
# (fxparts/monkey.js): lavu, unsummon (release is already the Chameleon's); the TTO parts' (fxparts/tto_monkey.js): rise,
# head, top, dive
# 2026-11-13, the Panda (plans/fx_panda/decisions.md 26, 35, 36, 41, 59): enable (Three Steps' trails switched on / off by
# node name, fxparts/trail.js), atBone (spawned at a hero bone's world position, index.html Fx), k and off (the TTO parts',
# fxparts/tto_panda.js: a Nine Dragons dragon's index, the limb trails' emitOff time); x / y / d may be [lo, hi] (a float
# drawn per play, index.html cueOf: Pummel's ogre arms)
OPTS = {"d", "x", "y", "rot", "vol", "cut", "p", "roll", "scale", "kill", "to", "bone", "spread", "i", "n", "ignite", "hideHero", "notWorn",
        "worn", "end", "single", "anims", "flip", "pulse", "gather", "gatherTo", "hand", "eclipse", "recall", "home",
        "strafe", "speed", "fatal", "slot", "r", "life", "stop", "all", "bow", "face", "slide", "slots", "ghost", "shatterGhosts",
        "lockOnly", "release", "from", "tint", "radius",
        "tune", "firePoint", "tilt", "pick", "playAudio", "clip", "host", "pair", "trigger", "finish", "ride", "shots",
        "rideEnd", "tier", "sink", "kicks", "fold", "launch", "egg",
        "alpha", "standing", "hide", "moves", "turn", "attach", "lavu", "unsummon", "boost", "rise", "head", "top", "dive", "alt",
        "enable", "atBone", "k", "off", "floor",   # floor: the Panda's QA (index.html Fx, clipped at the ground; a node name or a list of them: the Whale's QA)
        # 2026-11-13, the Rabbit (plans/fx_rabbit/decisions.md 20, 22-24, 29, 31, 56): yaw (one random angle per play per name,
        # index.html cueOf), sphere (a random flat offset within r), replace (an older live copy disposed at the spawn), owner
        # (the root EffectControl's followPosition owner, fxparts/control.js), ally / delay (fxparts/tto_rabbit.js's turret and
        # coins); a rot list may hold "random" (Random.Range(0, 360) per spawn); kind rides api.spawn only, never a cue
        "yaw", "sphere", "replace", "owner", "ally", "delay",
        # 2026-11-13, the Whale (plans/fx_whale/decisions.md 31, 32, 40, 43, 66): around ([lo, hi] whole metres at a random
        # whole angle about the cue's spot, index.html cueOf: Mal Storm's bolts), withRot (with atBone: the bone's rotation
        # too, index.html Fx: Peninsula Round's rings); the knights' guard ([from, to] ages) and attack ([ages], built, not
        # cued) (fxparts/whale.js); animLoop (fx:castRing's clip looped from the spawn, fxparts/bat.js); hops (a Leviathan
        # Breach dolphin's, fxparts/tto_whale.js); a rot list may hold a [lo, hi] pair of whole numbers (rot_ok)
        "guard", "attack", "around", "withRot", "animLoop", "hops"}
# lift: 2026-11-13, the Bison's Titan Drop (index.html LIFTS); hideProp: 2026-11-13, the Cat's throws hiding the worn weapon
# ([t, "hideProp", slot, {"kill": s}], index.html HeroPropHide; plans/fx_cat/decisions.md 47); 2026-11-13, the Chameleon
# (plans/fx_chameleon/decisions.md 13, 48, 49): "hero" (the whole hero, her props and their weapon_fx particles: Thunder
# Dragon), and no kill = hidden until the next pick (after a cast-bar skill, Clear Arrow's hand arrow)
# propCopy: 2026-11-13, the Rabbit's Ten Shot ([t, "propCopy", slot, {"bone", "kill"}]: a copy of the worn prop on a hero
# bone, index.html HeroPropCopy; plans/fx_rabbit/decisions.md 34): FX.spawned "propCopy:<slot>" only when a prop is worn there
KINDS = ("fx", "voice", "sound", "skin", "clone", "lift", "hideProp", "propAnim", "propCopy")   # propAnim: the worn prop's own clip (the Mole, decision 43)
PROP_SLOTS = ("R", "L", "Head", "Back")                          # index.html C.props' keys
HIDE_TARGETS = PROP_SLOTS + ("hero",)                            # index.html fxDue's hideProp (HeroPropHide, heroHide)
# order ("cycle": a pool whose plays take its members in turn), a member's standby (its step's end) and name (its tile's):
# 2026-11-13, the Mole's War Factory and TNT 1-4 (plans/fx_mole/decisions.md 12, 13)
ENTRY_KEYS, SKILL_KEYS = {"why", "cues", "skills", "builds", "everyCycle", "order"}, {"why", "cues", "builds", "everyCycle", "standby", "name"}


def rot_ok(r):
    """A cue's rot as index.html rotOf reads it: "random" / "randomYaw", or three angles, each a number, "random" (a whole
    angle 0 ... 359 per cue, the Rabbit's coins) or a [lo, hi] pair of whole numbers (a whole angle lo ... hi per cue:
    2026-11-13, the Whale's Peninsula Round rings [0, 0, [-30, 29]])."""
    num = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
    whole = lambda v: isinstance(v, int) and not isinstance(v, bool)
    return r in ("random", "randomYaw") or (isinstance(r, list) and len(r) == 3 and all(
        num(v) or v == "random" or (isinstance(v, list) and len(v) == 2 and all(map(whole, v)) and v[0] <= v[1]) for v in r))


def file_errors(cls):
    fx = DATA / cls / "fx.json"
    effects = json.loads(fx.read_text(encoding="utf-8"))["effects"] if fx.exists() else {}
    errs = [f"{cls}: effect {n} is not in {fx.relative_to(ROOT)} (run wardrobe_fx.py {cls})" for n in names(cls, "fx") if n not in effects]
    errs += [f"{cls}: voice v_{n}.mp3 is missing from data/{cls}/sfx (run wardrobe_fx.py {cls})" for n in names(cls, "voice")
             if not (DATA / cls / "sfx" / f"v_{n}.mp3").exists()]
    errs += [f"{cls}: sound {n}.mp3 is missing from data/{cls}/sfx (run wardrobe_fx.py {cls})" for n in names(cls, "sound")
             if not (DATA / cls / "sfx" / f"{n}.mp3").exists()]
    clips = json.loads((DATA / cls / "clips.json").read_text(encoding="utf-8"))
    for key, e in CUES[cls].items():
        sq, clip = split_key(key)
        if clip not in clips:
            errs.append(f"{cls}: cue key {key} is not a clip of the class")
        elif sq and clip not in seq_clips(cls, sq):
            errs.append(f"{cls}: cue key {key}: no sequence {sq} in index.html's SEQ that plays {clip}")
        elif key_step(key) is not None and clip not in (SEQS[cls][sq][key_step(key)] if key_step(key) < len(SEQS[cls][sq]) else []):
            errs.append(f"{cls}: cue key {key}: step {key_step(key)} of {sq} does not play {clip}")
        if not isinstance(e.get("why"), str) or ("cues" in e) == ("skills" in e):
            errs.append(f"{cls}: {key}: an entry needs a why and either cues or skills")
        for x, keys, at in [(e, ENTRY_KEYS, key)] + [(s, SKILL_KEYS, f"{key} {n}") for n, s in e.get("skills", {}).items()]:
            if set(x) - keys:
                errs.append(f"{cls}: {at}: unknown entry keys {sorted(set(x) - keys)}")
            if "builds" in x and not (isinstance(x["builds"], list) and all(isinstance(b, str) or (isinstance(b, list) and len(b) == 2
                                                                                                  and b[0] in ("fx", "sound", "voice")) for b in x["builds"])):
                errs.append(f"{cls}: {at}: builds must be a list of names (\"sound:<name>\" / \"voice:<name>\" for a sound)")
            if "everyCycle" in x and not isinstance(x["everyCycle"], bool):
                errs.append(f"{cls}: {at}: everyCycle must be true or false")
        for cues in cue_lists(e):
            for c in cues:
                ok = (isinstance(c, list) and 3 <= len(c) <= 5 and isinstance(c[0], (int, float)) and c[1] in KINDS
                      and isinstance(c[2], str) and (len(c) < 4 or isinstance(c[3], (int, float)) or (isinstance(c[3], dict) and set(c[3]) <= OPTS)))
                if ok and len(c) > 3 and isinstance(c[3], dict):     # x / y / d: a number or [lo, hi] (the Panda's, cueOf)
                    num = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
                    ok = all(num(v) or (isinstance(v, list) and len(v) == 2 and all(map(num, v)) and v[0] <= v[1])
                             for o, v in c[3].items() if o in ("x", "y", "d"))
                    # rot (rot_ok); around: [lo, hi] whole metres; withRot: true, only beside atBone (the Whale's)
                    whole = lambda v: isinstance(v, int) and not isinstance(v, bool)
                    ok = (ok and ("rot" not in c[3] or rot_ok(c[3]["rot"]))
                          and ("around" not in c[3] or (isinstance(c[3]["around"], list) and len(c[3]["around"]) == 2
                                                        and all(map(whole, c[3]["around"])) and c[3]["around"][0] <= c[3]["around"][1]))
                          and ("withRot" not in c[3] or (c[3]["withRot"] is True and isinstance(c[3].get("atBone"), str))))
                if not ok:
                    errs.append(f"{cls}: {key}: bad cue {c}")
                elif c[1] == "fx" and len(c) > 3 and isinstance(c[3], dict) and c[3].get("floor") not in (None, True, False):
                    # floor: true, or the names of the effect's nodes to clip at the ground (2026-11-14, the Whale's QA; index.html Fx)
                    want = c[3]["floor"] if isinstance(c[3]["floor"], list) else [c[3]["floor"]]
                    for n in c[2].split("|"):
                        have = {x.get("name") for x in effects.get(n, {}).get("nodes", [])}
                        errs += [f"{cls}: {key}: floor node {w!r} is not a node of {n}" for w in want if n in effects and w not in have]
                elif c[1] == "skin":
                    errs += [f"{cls}: {key}: skin {n} is not one of index.html's HERO_SKINS {sorted(SKINS)}"
                             for n in c[2].split("|") if n not in SKINS]
                elif c[1] == "clone":                       # a copy of the hero playing one of her clips (HeroClone)
                    errs += [f"{cls}: {key}: clone {n} is not a clip of the class" for n in c[2].split("|") if n not in clips]
                elif c[1] == "lift":                        # the hero raised along a curve (index.html LIFTS, HeroLift)
                    errs += [f"{cls}: {key}: lift {n} is not one of index.html's LIFTS {sorted(LIFT_NAMES)}"
                             for n in c[2].split("|") if LIFT_NAMES and n not in LIFT_NAMES]
                elif c[1] == "propAnim":                    # the worn prop's own clip once (index.html propAnimPlay)
                    errs += [f"{cls}: {key}: propAnim {n} is not a prop slot (R, L, Head, Back)" for n in c[2].split("|") if n not in PROP_SLOTS]
                elif c[1] == "propCopy":                    # a copy of the worn prop on a bone (index.html HeroPropCopy)
                    o = c[3] if len(c) > 3 and isinstance(c[3], dict) else {}
                    if c[2] not in PROP_SLOTS:
                        errs.append(f"{cls}: {key}: propCopy {c[2]} is not a prop slot (R, L, Head, Back)")
                    if not isinstance(o.get("bone"), str):
                        errs.append(f"{cls}: {key}: propCopy {c[2]}: bone must name the hero bone it goes on")
                elif c[1] == "hideProp":                    # the worn prop's meshes hidden (index.html HeroPropHide)
                    errs += [f"{cls}: {key}: hideProp {n} is not a prop slot (R, L, Head, Back) or hero" for n in c[2].split("|")
                             if n not in HIDE_TARGETS]
                    o = c[3] if len(c) > 3 and isinstance(c[3], dict) else {}
                    if "kill" in o and not isinstance(o["kill"], (int, float)):
                        errs.append(f"{cls}: {key}: hideProp {c[2]}: kill must be the seconds it stays hidden (none: until the next pick)")
                    if "all" in o and not isinstance(o["all"], bool):
                        errs.append(f"{cls}: {key}: hideProp {c[2]}: all must be true or false")
    return errs


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


# the stdlib server queues 5 connections; the page loads dozens of icons at once and the rest were refused
# (ERR_CONNECTION_REFUSED, 2026-11-09: data/icons/skills/emotion/beg.webp)
http.server.ThreadingHTTPServer.request_queue_size = 128
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/wardrobe/index.html"
LIVE = """() => { const { FX } = wardrobe.debug();
  return FX.live.map(f => f.name + ':' + f.emitters.reduce((s, e) => s + (f.attached(e.node) ?
    (e.node.children.find(c => c.isMesh)?.geometry.attributes.position?.count || 0) : 0), 0) + 'v'); }"""
# the tile that plays a cue key and its picker tab: "@<sequence>:<clip>" that sequence's; a clip the sequence holding it
# (ท่าสกิล lists those instead of their clips), else the clip in its own group's tab (อีโมต / ท่าพื้นฐาน cues since
# 2026-11-10: the Wolf's emote voices)
TILES = """clips => { const { chains, C } = wardrobe.debug(), ch = chains();
  return clips.map(c => { const k = c.match(/^@([^:]+):(.+)$/);
    if (k) { const s = ch.find(s => s.id === "@" + k[1].replace(/\\s+/g, "")); return s ? [s.id, "skill"] : [c, "skill"]; }
    const s = ch.find(s => s.steps.some(st => (st.alts || [st]).some(a => a.clip === c)));
    return s ? [s.id, "skill"] : [c, /^walk$/i.test(c) ? "base" : C.clipsData[c]?.group || "skill"]; }); }"""


def safe(n):
    """An effect's name as a file name part ("skin:FX/CosmicRift" -> "skin_FX_CosmicRift")."""
    return re.sub(r"[^\w.-]", "_", n)


async def play_tile(page, var, cls, tile, group, expect, shots, cap=CAP, force=None):
    """force: {step index: alternative index} for a sequence with alternatives (index.html's window.__seqAlt test hook),
    kept while the tile plays; the shots' names then carry "~<alternative>"."""
    await page.evaluate("() => { const { FX } = wardrobe.debug(); FX.spawned = {}; FX.missing = {}; }")
    await page.evaluate("f => { window.__seqAlt = f; }", {str(k): v for k, v in force.items()} if force else None)
    if await page.locator('#picker').is_hidden():                      # reopen the move picker
        await page.click('button.topic[data-t="move"]')
    await page.click(f'.pk-tab[data-g="{group}"]')
    if await page.locator(f'#pkBody .pk-item[data-m="{tile}"]').count() == 0:
        return [f"{cls}: no tile {tile} in the {group} tab (cue file key not a clip of this class?)"]
    await page.click(f'#pkBody .pk-item[data-m="{tile}"]')
    await page.click('#pkClose') if await page.locator('#pkClose').count() else None
    t0 = await page.evaluate("() => performance.now()")
    samples, first, shot, peak, key = [], {}, set(), 0, tile.lstrip("@") + (f"~{max(force.values())}" if force else "")
    while True:
        now = (await page.evaluate("() => performance.now()") - t0) / 1000
        live = await page.evaluate(LIVE)
        samples.append(f"{now:.2f}s " + ",".join(live))
        for n in {x.rsplit(":", 1)[0] for x in live}:
            first.setdefault(n, now)
        for n, at in first.items():
            if n not in shot and now >= at + SHOT_AFTER:
                shot.add(n); p = f"{var}_{cls}_{key}_{safe(n)}.png"; shots.setdefault((cls, key), []).append(n)
                await page.screenshot(path=str(OUT / p))
        total = sum(int(x.rsplit(":", 1)[1][:-1]) for x in live if ":" in x)
        if total > peak:                                               # the frame with the most effect geometry
            peak = total; await page.screenshot(path=str(OUT / f"{var}_{cls}_{key}_peak.png"))
        tally = await page.evaluate("() => { const { FX } = wardrobe.debug(); return { s: FX.spawned, m: FX.missing }; }")
        done = all(n in tally["s"] or n in tally["m"] for n in expect)
        last = max([first.get(n, 0) for n in expect] or [0])
        if (done and now > last + SETTLE) or now > cap:
            break
        await page.wait_for_timeout(30)
    await page.evaluate("() => { window.__seqAlt = null; }")
    print(f"== {var} {cls} {tile}" + (f" (alternatives {force})" if force else "") + ": " + " | ".join(samples[::3]))
    return [f"{cls} {tile}" + (f" (alternatives {force})" if force else "") + f": cued effect {n} " + ("is not in fx.json" if n in tally["m"] else "never spawned")
            for n in expect if n not in tally["s"]]


async def main():
    errors = [e for c in CLASSES for e in file_errors(c)]
    if A.files_only:
        print("\n".join(errors) or f"files: no problems ({', '.join(CLASSES)})")
        raise SystemExit(1 if errors else 0)
    from playwright.async_api import async_playwright
    shots = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--autoplay-policy=no-user-gesture-required"])
        page = await b.new_page(viewport={"width": 1366, "height": 768})
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: m.type == "error" and errors.append(m.text + " " + (m.location or {}).get("url", "")))
        page.on("requestfailed", lambda r: errors.append("request failed " + r.url))
        page.on("response", lambda r: r.status >= 400 and errors.append(f"{r.status} {r.url}"))
        for var in VARIANTS:
            await page.goto(URL + "?fxbg=" + var)
            await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
            for cls in CLASSES:
                await page.evaluate("c => wardrobe.show(c)", cls)
                await page.wait_for_function("c => wardrobe.debug().C?.cls === c && wardrobe.debug().FX.cueTab[c]", arg=cls, timeout=120000)
                await page.click('button.topic[data-t="move"]')
                clips = list(CUES[cls])
                tile_of = dict(zip(clips, await page.evaluate(TILES, clips)))
                # one tile per pool member (index.html poolChains, 2026-11-10): a pool's clip is played through each
                # member's own tile, which expects that member's cues; its host tile (the Cast sequence) is not listed
                pools = {p[0]: p for p in await page.evaluate(
                    "() => wardrobe.debug().chains().filter(c => c.pick).map(c => [c.id, c.pick, c.steps.flatMap(s => (s.alts || [s]).map(a => a.clip))])")}
                pooled = {clip for _, pick, steps in pools.values() for clip in steps if CUES[cls].get(clip, {}).get("skills", {}).get(pick)}
                hidden = set(await page.evaluate("() => wardrobe.debug().chains().filter(c => c.hidden).map(c => c.id)"))
                order = [t for c in clips if tile_of[c][0] not in hidden or c in pooled for t in ([tuple(tile_of[c])] if c not in pooled else
                         [(pid, "skill") for pid, pick, steps in pools.values() if c in steps and CUES[cls][c].get("skills", {}).get(pick)])]
                for tile, group in dict.fromkeys(order):   # in cue order, one play per tile
                    if tile in pools:                      # a pool member's tile: its steps, the pool's clip as that member
                        _, pick, steps = pools[tile]
                        entries = [(CUES[cls][c]["skills"][pick] if CUES[cls].get(c, {}).get("skills", {}).get(pick) else entry_for(cls, None, c)) for c in steps]
                        expect = expected(entries)
                        cap = CAP + max([c[0] for e in entries for c in e.get("cues", [])] or [0])
                        errs = await play_tile(page, var, cls, tile, group, expect, shots, cap)
                        errors += [e for e in errs if e not in errors]
                        continue
                    # effects every play must show: a plain entry's (its "a|b" picks and rolled procs vary: not expected);
                    # a shared clip's skills are picked at random, so none of theirs is expected either
                    # a sequence's: each step's entry as the page picks it ("@<sequence>:<clip>" first)
                    sq = tile[1:] if tile.startswith("@") and tile[1:] in SEQS.get(cls, {}) else None
                    # a sequence with alternatives (the Bison's Normal Attack, nAttack4 | nAttack3): once per alternative
                    # a cycle pool's own tile (2026-11-13, the Mole's War Factory, index.html fxStart "order": "cycle"): one
                    # play per member, each expecting that member's cues (the page takes them in the file's order; no other
                    # tile plays the clip, and the class's load starts the turn again)
                    cyc = CUES[cls].get(tile, {}) if not sq and CUES[cls].get(tile, {}).get("order") == "cycle" else {}
                    plays = ([({}, None, m) for m in cyc["skills"].values()] if cyc else
                             [(f, sc, None) for f, sc in (seq_plays(cls, sq) if sq else [({}, None)])])
                    for force, step_clips, member in plays:
                        entries = ([member] if member else [alt_view(entry_for(cls, sq, c, i), force.get(i, 0)) for i, c in enumerate(step_clips)]
                                   if sq else [CUES[cls].get(tile, {})])
                        # (a skin cue's look: "skin:<name>", a clone "clone:<clip>", a lift "lift:<name>", as the page
                        # tallies them; a part's spawns too)
                        expect = expected(entries)
                        # a skill's late cues run on in the idle tail (Grand Codex's last page at 20.7 s): wait for them too
                        cap = CAP + max([c[0] for e in entries for cues in cue_lists(e) for c in cues] or [0]) + (play_time(cls, sq, force) if sq else 0)
                        errs = await play_tile(page, var, cls, tile, group, expect, shots, cap, force)
                        errors += [e for e in errs if e not in errors]
        snd = await page.evaluate("() => { const { Sound } = wardrobe.debug(); return { ctx: Sound.ctx?.state, loaded: Object.keys(Sound.bufs).length }; }")
        print("sound:", snd)
        await b.close()
    rows = "".join(f"<tr><th>{cls} {key} {n}</th>" + "".join(f'<td><img src="{v}_{cls}_{key}_{safe(n)}.png"></td>' for v in VARIANTS) + "</tr>"
                   for (cls, key), ns in shots.items() for n in [*dict.fromkeys(ns), "peak"])
    (OUT / "compare.html").write_text("<!doctype html><meta charset=utf-8><title>Effect backdrops</title><style>body{font:14px sans-serif;"
                                      "margin:16px}img{width:100%}td{vertical-align:top}</style><table><tr><th></th>"
                                      + "".join(f"<th>{v}</th>" for v in VARIANTS) + f"</tr>{rows}</table>", encoding="utf-8")
    print("errors:", errors)
    raise SystemExit(1 if errors else 0)


asyncio.run(main())
