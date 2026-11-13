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
    # the Cat's pillagePlunge clip is Pillage Plunge, card pillage (2026-11-13, plans/fx_cat/decisions.md 15, skills_b.md
    # item 3, Q10: the tile had no icon)
    "cat": {"pillage": ["pillagePlunge"]},
    # the Chameleon's backStep is Perfect Blend, cast4 Fatal Strike, rainOfArrow Torment Rain (2026-11-13,
    # plans/fx_chameleon/decisions.md 14, skills_a.md item 2, skills_b.md "Page changes")
    "chameleon": {"backStep": ["perfectBlend"], "cast4": ["fatalStrike"], "rainOfArrow": ["tormentRain"]},
    # the Mole's grenade clip is Stun Grenade, hammer Mega Hammer, Assemble's clips Auto Gyro Gun and Barrel Bot, dig1 King
    # Kaiser; the TTO missilePad is Missile with Twin Warhead (2026-11-13, plans/fx_mole/decisions.md 14, skills_b.md
    # Verification 3; missilePad the editor's: the Bible has no icon of its own)
    "mole": {"grenade": ["stunGrenade"], "hammer": ["megaHammer"], "assemble1": ["autoGyroGun", "barrelBot"],
             "assemble2": ["autoGyroGun", "barrelBot"], "dig1": ["kingKaiser"], "missilePad": ["missile", "twinWarhead"]},
    # the Monkey's earthPulse clip is Titanic Earth Pulse; the TTO tiles: the boosted Ja / Buiten with their passive, Ja
    # Ascension's solarCall, golemCall Rune Golem, sanctumRaise (not released) Buiten Bastion (2026-11-13,
    # plans/fx_monkey/decisions.md 18, tto.md S2)
    "monkey": {"earthPulse": ["titanicEarthPulse"], "jaAscension": ["ja", "jaAscension"], "buitenBastion": ["buiten", "buitenBastion"],
               "solarCall": ["jaAscension"], "golemCall": ["runeGolem"], "sanctumRaise": ["buitenBastion"]},
    # the Panda's fujinKen1-3 are Fuujin Ken (the Bible's key spells it with two u's: panda_fuujinKen1 / 5; 2026-11-13,
    # plans/fx_panda/decisions.md 60, skills_a.md Read this first 7)
    "panda": {"fujinKen1": ["fuujinKen"], "fujinKen2": ["fuujinKen"], "fujinKen3": ["fuujinKen"]},
    # the Rabbit's maim clip is Maim Shot (2026-11-13, plans/fx_rabbit/decisions.md 13, skills_a.md Verification 4; the
    # pools gilShot / mix3 / mix4 / medicalShot give their members their icons through the cue file)
    "rabbit": {"maim": ["maimShot"]},
    # the Whale's divingWave clip is Whale Wave and divingStorm Mal Storm (Diving Press #443 on, Whale.cs:32111-32125,
    # :32775-32789), gobble Gobble Up, the TTO leviathanCall Leviathan Breach (2026-11-13, plans/fx_whale/decisions.md 12,
    # 17, skills_a.md "Page lines, as corrected", tto.md S3; the pools cast3 / flyingShield give their members their icons
    # through the cue file)
    "whale": {"divingWave": ["whaleWave"], "divingStorm": ["malStorm"], "gobble": ["gobbleUp"], "leviathanCall": ["leviathanBreach"]},
}
# pool members that are one skill's ranks, each a cast of its own (the Mole's TNT 1-4, decisions.md 12): the Bible key of
# their own rank's icon
# (the Rabbit's: the Bible card's own icon where its picture differs from the highest-numbered key's, 2026-11-13,
# plans/fx_rabbit/decisions.md 13, skills_a.md Read this first 8, skills_b.md Verification 5; cAttack and customizedShotgun
# the editor's, compared the same way: cards rabbit_cAttack3 / rabbit_customizedShotgun2 against the 4 keys)
RANK_ICONS = {"mole": {f"tnt{n}": f"mole_tnt{n}" for n in range(1, 5)},
              "rabbit": {"backpack": "rabbit_backpack2", "circleShot": "rabbit_circleShot2", "fourShot": "rabbit_fourShot2",
                         "gorgonShot": "rabbit_gorgonShot2", "mall": "rabbit_mall2", "shake": "rabbit_shake3",
                         "miracleBlend": "rabbit_miracleBlend1", "stickyGum": "rabbit_stickyGum2",
                         "acidicField": "rabbit_acidicField2", "rapidTrance": "rabbit_rapidTrance1",
                         "statScan": "rabbit_statScan1", "shootingArray": "rabbit_shootingArray2",
                         "millionaire": "rabbit_millionaire2", "truceTrading": "rabbit_truceTrading2",
                         "cAttack": "rabbit_cAttack3", "customizedShotgun": "rabbit_customizedShotgun2"},
              # the Whale's 12th Kingdom Knight: its Bible key starts with a digit, which the icon pattern below cannot read
              # (2026-11-13, plans/fx_whale/decisions.md 17, parts.md Verification 1: the top rank's)
              "whale": {"12thKingdomKnight": "whale_12thKingdomKnight2"}}


# skills the game plays with no body animation, shown as idle-stance tiles (index.html SEQ "<Name>: root@<t>", 2026-11-10;
# found by listing each class's RPC_* that calls no clip, NOTES.md that day; the Bat's 2026-11-13, plans/fx_bat/effect_only.md)
# (the Bison's Berserker Rush and Fury Trance, passives' procs: plans/fx_bison/effect_only.md, decisions.md 6)
EFFECT_ONLY = {"bison": ["berserkerRush", "furyTrance"], "sheep": ["quickHeal"], "penguin": ["manaArc", "dispell", "doubleCast", "tripleCast", "frostSpike"],
               "bat": ["massCast", "shadowGaze", "switch", "shadowSacrifice"],
               # the Cat's Awareness, Damage Roulette and Treasure Hunt (2026-11-13, plans/fx_cat/effect_only.md block 4,
               # decisions.md 8, 10)
               "cat": ["awareness", "damageRoulette", "treasureHunt"],
               # the Mole's Reload, Fire Barrage, Bombardment and Synchro Mole (2026-11-13, plans/fx_mole/effect_only.md)
               "mole": ["reload", "fireBarrage", "bombardment", "synchroMole"],
               # the Monkey's Instant Cast, Fire Rune, Earth Rune and Blazing Fire (2026-11-13, plans/fx_monkey/decisions.md 18,
               # effect_only.md Verification 3: Fire Avatar - Fireball takes the Fireball's icon through SEQ_SKILL)
               "monkey": ["instantCast", "fireRune", "earthRune", "blazingFire"],
               # the Panda's Mystic Sage and Safe Guard (2026-11-13, plans/fx_panda/decisions.md 11, 60, effect_only.md)
               "panda": ["mysticSage", "safeGuard"],
               # the Whale's Auto Shield (2026-11-13, plans/fx_whale/effect_only.md block 4, decisions.md 7)
               "whale": ["autoShield"]}
# sequences that are one skill on a shared clip (index.html SEQ_SKILL): their skill's icon, with that clip (the Bat's
# Nightmare and Mind Control: cast3 then channel, plans/fx_bat/skills_b.md Verification 3; the Cat's Even Odds on the
# gamble clip and Nine Lives' ko then getUp, plans/fx_cat/effect_only.md block 4, decisions.md 8, 11, 12)
OWN_TILE = {"sheep": {"sealOfAttack": ["cast3"], "sealOfDefense": ["cast3"], "edenSanctuary": ["cast3"]},
            "bat": {"nightmare": ["cast3", "channel"], "mindControl": ["cast3", "channel"]},
            "cat": {"evenOdds": ["gamble"], "nineLives": ["ko", "getUp"]},
            # the Chameleon's cast3 skills with no channel, Tent's channel then sleep, Critical Plus and Clear Arrow on the
            # Normal Attack's clip (2026-11-13, plans/fx_chameleon/decisions.md 5, 6, 12-14)
            "chameleon": {"immunity": ["cast3"], "venomShock": ["cast3"], "bloodBurn": ["cast3"], "rustyDecay": ["cast3"],
                          "tent": ["cast3", "sleep"], "criticalPlus": ["nAttack1"], "clearArrow": ["nAttack1"]},
            # the Mole's War Capital on Assemble's clips; the Charge Attack (the burrow, no cAttack clip: Super Dig's superDig)
            # its own cAttack3 (2026-11-13, plans/fx_mole/decisions.md 7, 14; cAttack the editor's, for the HD icon)
            "mole": {"warCapital": ["assemble1", "assemble2"], "cAttack": ["superDig"]},
            # the Monkey's Mike Blink / Mike Circle on the Normal Attack's / HP Transfer's clips, the cast skills with their
            # own sequences, Sentinel Guard (2026-11-13, plans/fx_monkey/decisions.md 18, attacks_emotes.md Verification 3,
            # skills_a.md Verification 7, skills_b.md Verification 3)
            "monkey": {"mikeBlink": ["nAttack1", "nAttack2"], "mikeCircle": ["cAttack1", "cAttack2"], "lavu": ["cast3"],
                       "volcanicEruption": ["cast3"], "summonGaos": ["damageCast2", "cast3"], "fireKeep": ["damageCast2", "root", "cast3"],
                       "stoneSentinel": ["sentinalGuard1", "sentinalGuard2", "sentinalGuard0"]},
            # the Panda's Sacred Sage Technique on the charge's clips, Delay Qi on Qi Strike's and the idle hold (2026-11-13,
            # plans/fx_panda/decisions.md 7, 12, 60, effect_only.md Verification 5)
            "panda": {"sacredSageTechnique": ["cAttack1", "cAttack2"], "delayQi": ["qiStrike1", "root", "qiStrike2"]},
            # the Rabbit's Customized Shotgun on the Normal Attack's clip, From the Above on Bounce's clips, Contract on Truce
            # Trading's clip and the bow (2026-11-13, plans/fx_rabbit/decisions.md 13, attacks_emotes.md Verification 3,
            # effect_only.md Verification 4, skills_b.md Verification 6)
            "rabbit": {"customizedShotgun": ["nAttack"], "fromTheAbove": ["bounce1", "bounce2"], "contract": ["truceTrading", "bow"]},
            # the Whale's cast3 skills with no channel (Honor, 12th Kingdom Knight, Bubble Burst), Knight of the Deep and
            # Shield Reflect on the Charge Attack's clips, Wall Puncture on Peninsula Impale's (2026-11-13,
            # plans/fx_whale/decisions.md 5, 6, 8, 10, 17, attacks_emotes.md Verification 3-5)
            "whale": {"honor": ["cast3"], "12thKingdomKnight": ["cast3"], "bubbleBurst": ["cast3"],
                      "knightOfTheDeep": ["cAttack1", "cAttack2", "shieldBash"], "shieldReflect": ["cAttack1", "cAttack2", "root"],
                      "wallPuncture": ["peninsulaImpale"]}}


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
            # ("&": the Panda's panda_wind&cloud2 / panda_rain&storm2, plans/fx_panda/decisions.md 60)
            m = re.fullmatch(rf"{cls}_([A-Za-z&]+?)(\d*)", k)
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
                # (a cycle pool, "order": "cycle", is one skill on its clip's own tile: its members get no tile, no icon)
                if not key.startswith("@") and isinstance(e, dict) and e.get("skills") and e.get("order") != "cycle":
                    for m in e["skills"]:
                        pools.setdefault(m, []).append(key)
        best.update({s: (0, k) for s, k in RANK_ICONS.get(cls, {}).items() if k in icons})
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
