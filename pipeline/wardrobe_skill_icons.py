r"""Skill icons from the 12 Tails Bible, for the wardrobe's ท่าสกิล tiles (2026-11-09; user: "for Wolf animations that might
come from various skills, display all their skill icons, i want all skills to use circle frame too like our class guide
format. Resurrection is Mass Ressurection icon, please borrow upscaled skill icon from the bible too").

The Bible keeps 128 px upscales of the game's skill icons in 12t_projects\bible\assets.js (BIBLE_ASSETS.SKILL_ICONS,
"<class>_<skill><rank>": a WebP data URI). This copies, per class, each skill's highest-rank icon to
wardrobe/data/icons/hd/<cls>/<skill>.webp and writes wardrobe/data/icons/hd/index.json:
  {cls: {skill: {"icon": "icons/hd/<cls>/<skill>.webp", "clips": [skill clips it covers]}}}
A clip belongs to the skill named like it (trailing digits and an "End" dropped: bladeFang2 -> bladeFang,
tempestDanceEnd -> tempestDance), unless CLIP_SKILLS says otherwise: clips several skills play list them all (the page
then shows every one of their icons on the tile, in the class guide's ring layout).

  py -3 pipeline\wardrobe_skill_icons.py
"""
import base64
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "wardrobe", "data")
BIBLE = next((p for p in (r"D:\12tails", r"C:\Users\Jump\Desktop\12tails") if os.path.isfile(p + r"\12t_projects\bible\assets.js")), r"D:\12tails")
ASSETS = os.path.join(BIBLE, "12t_projects", "bible", "assets.js")

# clips whose skill is not the one named like the clip, or that several skills play (plans/fx_wolf/cast.md, counters.md)
CLIP_SKILLS = {
    "wolf": {
        "instantCast": ["braveSpirit", "secondWind", "lunarEclipse", "holySword"],   # RPC_braveSpirit / secondWind / lunarEclipse / holySword
        "darkEdge": ["darkEdge", "holyArmor"],                                       # Holy Armor plays darkEdge (Wolf.cs:33598)
        "resurrection": ["massResurrection"],                                        # RPC_massResurrection
        "mirrorCounter1": ["mirrorBlade"], "mirrorCounter2": ["mirrorBlade"],        # Mirror Blade
    },
    # the cleave tile is Power Cleave (2026-11-13, plans/fx_bison/decisions.md 10, skills_a.md Q8: Power Hammer, a passive,
    # gets no icon)
    "bison": {"cleave": ["powerCleave"]},
}


# skills the game plays with no body animation, shown as idle-stance tiles (index.html SEQ "<Name>: root@<t>", 2026-11-10;
# found by listing each class's RPC_* that calls no clip, NOTES.md that day; the Bat's 2026-11-13, plans/fx_bat/effect_only.md)
# (the Bison's Berserker Rush and Fury Trance, passives' procs: plans/fx_bison/effect_only.md, decisions.md 6)
EFFECT_ONLY = {"bison": ["berserkerRush", "furyTrance"], "sheep": ["quickHeal"], "penguin": ["manaArc", "dispell", "doubleCast", "tripleCast", "frostSpike"],
               "bat": ["massCast", "shadowGaze", "switch", "shadowSacrifice"]}
# sequences that are one skill on a shared clip (index.html SEQ_SKILL): their skill's icon, with that clip (the Bat's
# Nightmare and Mind Control: cast3 then channel, plans/fx_bat/skills_b.md Verification 3)
OWN_TILE = {"sheep": {"sealOfAttack": ["cast3"], "sealOfDefense": ["cast3"], "edenSanctuary": ["cast3"]},
            "bat": {"nightmare": ["cast3", "channel"], "mindControl": ["cast3", "channel"]}}


def bible_icons():
    """{key: webp bytes} of BIBLE_ASSETS.SKILL_ICONS."""
    text = open(ASSETS, encoding="utf-8").read()
    start = text.index("BIBLE_ASSETS.SKILL_ICONS = {")
    end = text.index("};", start)
    return {k: base64.b64decode(v) for k, v in re.findall(r'"([^"]+)":\s*"data:image/webp;base64,([^"]+)"', text[start:end])}


def main():
    icons = bible_icons()
    meta = json.load(open(os.path.join(DATA, "meta.json"), encoding="utf-8"))
    index, written = {}, 0
    for c in meta["classes"]:
        cls = c["cls"]
        best = {}                                    # skill -> (rank, key): the highest rank the Bible has
        for k in icons:
            m = re.fullmatch(rf"{cls}_([A-Za-z]+?)(\d*)", k)
            if m:
                r = int(m.group(2) or 0)
                if m.group(1) not in best or r > best[m.group(1)][0]:
                    best[m.group(1)] = (r, k)
        lower = {s.lower(): s for s in best}
        clips = json.load(open(os.path.join(DATA, cls, "clips.json"), encoding="utf-8"))
        out = {}
        for clip, v in clips.items():
            if v.get("group") != "skill":
                continue
            skills = CLIP_SKILLS.get(cls, {}).get(clip)
            if skills is None:
                base = re.sub(r"End$", "", re.sub(r"\d+$", "", clip))
                skills = [lower[base.lower()]] if base.lower() in lower else []
            for s in skills:
                if s not in best:
                    print(f"  {cls}/{clip}: the Bible has no icon for {s}", file=sys.stderr)
                    continue
                out.setdefault(s, {"icon": f"icons/hd/{cls}/{s}.webp", "clips": []})["clips"].append(clip)
        # one tile per skill (2026-11-10): every member of a cue-file pool (a clip several skills play, {skills: {...}}, the
        # page's poolChains) gets its own icon, the pool's clip as its clip; a skill the game plays with no animation
        # (EFFECT_ONLY, an idle-stance tile) the idle clip root
        cues_path = os.path.join(ROOT, "wardrobe", "fx_cues", f"{cls}.json")
        pools = {}
        if os.path.isfile(cues_path):
            for key, e in json.load(open(cues_path, encoding="utf-8")).items():
                if not key.startswith("@") and isinstance(e, dict) and e.get("skills"):
                    for m in e["skills"]:
                        pools.setdefault(m, []).append(key)
        for s, cl in [*pools.items(), *((s, ["root"]) for s in EFFECT_ONLY.get(cls, [])), *OWN_TILE.get(cls, {}).items()]:
            s = lower.get(s.lower(), s)
            if s not in best:
                print(f"  {cls}: the Bible has no icon for {s}", file=sys.stderr)
                continue
            v = out.setdefault(s, {"icon": f"icons/hd/{cls}/{s}.webp", "clips": []})
            v["clips"] += [c for c in cl if c not in v["clips"]]
        os.makedirs(os.path.join(DATA, "icons", "hd", cls), exist_ok=True)
        for s in out:
            open(os.path.join(DATA, "icons", "hd", cls, s + ".webp"), "wb").write(icons[best[s][1]])
            written += 1
        index[cls] = dict(sorted(out.items()))
        print(f"{cls}: {len(out)} skill icons for {sum(len(v['clips']) for v in out.values())} clips")
    json.dump(index, open(os.path.join(DATA, "icons", "hd", "index.json"), "w", encoding="utf-8"), indent=1)
    print(f"{written} icons -> {os.path.join(DATA, 'icons', 'hd')}")


if __name__ == "__main__":
    main()
