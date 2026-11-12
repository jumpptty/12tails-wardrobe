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
its effects must spawn (the page counts them in FX.spawned); "everyCycle": true is a flag (the run's wing flap)."""
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
    """index.html's SEQ: {cls: {sequence id (its name without spaces): [step clips]}}."""
    html = (ROOT / "wardrobe" / "index.html").read_text(encoding="utf-8")
    block = re.sub(r"//[^\n]*", "", re.search(r"\nconst SEQ = \{(.*?)\n\};", html, re.S).group(1))
    out, cls = {}, None
    for m in re.finditer(r'(\w+): \[|"([^"]+)"', block):
        if m.group(1):
            cls = m.group(1); out[cls] = {}
        else:
            name, body = m.group(2).split(": ", 1)
            out[cls][name.replace(" ", "")] = [re.match(r"\w+", t).group(0) for t in body.split()]
    return out


SEQS = seqs()


def hero_skins():
    """index.html's HERO_SKINS: the names a "skin" cue may give."""
    html = (ROOT / "wardrobe" / "index.html").read_text(encoding="utf-8")
    block = re.search(r"\nconst HERO_SKINS = \{(.*?)\n\};", html, re.S)
    return set(re.findall(r'^  "([^"]+)":', block.group(1), re.M)) if block else set()


SKINS = hero_skins()


def split_key(key):
    """A cue key's (sequence id or None, clip): "@Eden Sanctuary:cast3" and "@EdenSanctuary:cast3" are one key."""
    if key.startswith("@") and ":" in key:
        sq, clip = key[1:].split(":", 1)
        return sq.replace(" ", ""), clip
    return None, key


def entry_for(cls, sq, clip):
    """The entry the page runs for a clip in a play of sequence sq (None: a single clip), as fxStart looks it up."""
    for key, e in CUES[cls].items():
        if sq and split_key(key) == (sq, clip):
            return e
    return CUES[cls].get(clip, {})


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
                  | {n for e in CUES[cls].values() for k, n in builds(e) if k == kind})


def expected(entries):
    """The effects every play of these entries must show, as the page tallies them (FX.spawned): fx cues, "skin:<name>",
    "clone:<clip>" (their "a|b" picks and rolled procs vary: not expected; nor a "worn" cue's, which needs an item the
    check's default dress lacks: the Bat's Homing Wand hits), and the effects their "builds" names."""
    out = {("skin:" if cue[1] == "skin" else "clone:" if cue[1] == "clone" else "") + cue[2] for e in entries for cue in e.get("cues", [])
           if cue[1] in ("fx", "skin", "clone") and "|" not in cue[2]
           and not (len(cue) > 3 and isinstance(cue[3], dict) and ("p" in cue[3] or "worn" in cue[3]))}
    return sorted(out | {n for e in entries for k, n in builds({"builds": e.get("builds", [])}) if k == "fx" and "|" not in n})


# index.html cueOf (2026-11-10, the Penguin: spread; i, n and ignite, passed on to the TTO parts, plans/fx_penguin/tto.md;
# hideHero for penguin.js's snowman; notWorn [slot, item], fxStart: the Staff of Time's missing landings; 2026-11-13, the
# Bat: worn [slot, item] (the Homing Wand's hits), end (the guardian's unsummon, fxparts/bat.js); a "clone" cue takes x,
# y, d, kill)
OPTS = {"d", "x", "y", "rot", "vol", "cut", "p", "roll", "scale", "kill", "to", "bone", "spread", "i", "n", "ignite", "hideHero", "notWorn",
        "worn", "end"}
KINDS = ("fx", "voice", "sound", "skin", "clone")
ENTRY_KEYS, SKILL_KEYS = {"why", "cues", "skills", "builds", "everyCycle"}, {"why", "cues", "builds", "everyCycle"}


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
        elif sq and clip not in SEQS.get(cls, {}).get(sq, []):
            errs.append(f"{cls}: cue key {key}: no sequence {sq} in index.html's SEQ that plays {clip}")
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
                if not ok:
                    errs.append(f"{cls}: {key}: bad cue {c}")
                elif c[1] == "skin":
                    errs += [f"{cls}: {key}: skin {n} is not one of index.html's HERO_SKINS {sorted(SKINS)}"
                             for n in c[2].split("|") if n not in SKINS]
                elif c[1] == "clone":                       # a copy of the hero playing one of her clips (HeroClone)
                    errs += [f"{cls}: {key}: clone {n} is not a clip of the class" for n in c[2].split("|") if n not in clips]
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
    const s = ch.find(s => s.steps.some(st => st.clip === c));
    return s ? [s.id, "skill"] : [c, /^walk$/i.test(c) ? "base" : C.clipsData[c]?.group || "skill"]; }); }"""


def safe(n):
    """An effect's name as a file name part ("skin:FX/CosmicRift" -> "skin_FX_CosmicRift")."""
    return re.sub(r"[^\w.-]", "_", n)


async def play_tile(page, var, cls, tile, group, expect, shots, cap=CAP):
    await page.evaluate("() => { const { FX } = wardrobe.debug(); FX.spawned = {}; FX.missing = {}; }")
    if await page.locator('#picker').is_hidden():                      # reopen the move picker
        await page.click('button.topic[data-t="move"]')
    await page.click(f'.pk-tab[data-g="{group}"]')
    if await page.locator(f'#pkBody .pk-item[data-m="{tile}"]').count() == 0:
        return [f"{cls}: no tile {tile} in the {group} tab (cue file key not a clip of this class?)"]
    await page.click(f'#pkBody .pk-item[data-m="{tile}"]')
    await page.click('#pkClose') if await page.locator('#pkClose').count() else None
    t0 = await page.evaluate("() => performance.now()")
    samples, first, shot, peak, key = [], {}, set(), 0, tile.lstrip("@")
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
    print(f"== {var} {cls} {tile}: " + " | ".join(samples[::3]))
    return [f"{cls} {tile}: cued effect {n} " + ("is not in fx.json" if n in tally["m"] else "never spawned")
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
                    "() => wardrobe.debug().chains().filter(c => c.pick).map(c => [c.id, c.pick, c.steps.map(s => s.clip)])")}
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
                    entries = [entry_for(cls, sq, c) for c in SEQS[cls][sq]] if sq else [CUES[cls].get(tile, {})]
                    # (a skin cue's look: "skin:<name>", a clone "clone:<clip>", as the page tallies them; a part's spawns too)
                    expect = expected(entries)
                    # a skill's late cues run on in the idle tail (Grand Codex's last page at 20.7 s): wait for them too
                    cap = CAP + max([c[0] for e in entries for cues in cue_lists(e) for c in cues] or [0])
                    errs = await play_tile(page, var, cls, tile, group, expect, shots, cap)
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
