r"""Which effect parts each class's skills need (2026-11-09, prep for every class's effects; HANDOFF "Next up"). For every
class: every effect prefab its own code loads (the Resources paths in DecompiledSource\<Class>.cs that end in a
GameObject under an Effects folder), what each is made of (Unity component types; the game's scripts by name; a mesh
drawn by no emitter = "StaticMesh"; an EffectControl below the root = "EffectControl(child)", which the page ignores),
and whether the page builds all of it today (BUILT). Writes plans\fx_inventory.md (the tables) and
plans\fx_inventory.json (per class: effect -> parts, the source line that loads it).

  uv run --no-project --with UnityPy python -I pipeline/wardrobe_fx_inventory.py
"""
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wardrobe_fx import BIBLE, Game, effect  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BIBLE, "DecompiledSource")
CLASSES = ["bat", "bison", "cat", "chameleon", "mole", "monkey", "panda", "penguin", "rabbit", "sheep", "whale", "wolf"]
# what the page's Fx builds (wardrobe/index.html "skill effects and sounds"); MeshFilter / Transform are carried by these
BUILT = {"EffectControl", "RingEmitter", "ImageEmitter", "LineEmitter", "EllipsoidParticleEmitter", "ParticleAnimator",
         "ParticleRenderer", "AudioSource",
         # 2026-11-09, wardrobe/fxparts (plans/fx_wolf/build_rules.md): vortex, emblem, trail, control, mesh
         "VortexEmitter", "EmblemEmitter", "TrailEmitter", "TrailRenderer", "EmitterControl", "EffectControl(child)",
         "StaticMesh", "Animation", "SkinnedMeshRenderer", "ShatterMesh",
         # 2026-11-10, the Sheep (plans/fx_sheep/parts.md): fxparts/alphatimer.js; fxparts/sheep.js (the three movers read
         # ProjectileControl's velocity, Eden Sanctuary's clip switch and end); Sheep_seal draws nothing (data only)
         "AlphaTimer", "ProjectileControl", "Sheep_seal", "Sheep_nAttack", "Sheep_homingLight", "Sheep_cAttack",
         "Sheep_edenSanctuary",
         # 2026-11-10, the Penguin (plans/fx_penguin/parts.md "Who builds what"): fxparts/penguin.js (its eight scripts;
         # Penguin_snowMan hides the hero, decisions.md 17), mesh.js's AdditiveSaturate / Opaque1 / Opaque2 / DiffuseAmbient
         # materials (shaders, not parts: this table doesn't see them); index.html's BoltEmitter and the ManaVortex
         # summon's script (cast_a.md "Read this first" 2; the summon is not under an Effects folder, so it isn't listed)
         "Penguin_tornado", "Penguin_typhoon", "Penguin_arcticEmperor", "Penguin_cosmicFriday", "Penguin_iceBlock",
         "Penguin_nAttack", "Penguin_manaMissile", "Penguin_snowMan", "BoltEmitter", "ManaVortex",
         # 2026-11-13, the Bat (plans/fx_bat/parts.md "Who builds what"): fxparts/bat.js (Echoes' orbs, the bolts, Mirage
         # Orb, Guardian of the Night; Bat_illusion's clones are the page's "clone" cue, index.html HeroClone),
         # fxparts/audiocontrol.js, fxparts/light.js (Unity's Light, the page's pooled point lights), fxparts/tto_bat.js
         # (TTO's BatSwarmFlap); fxparts/particles.js's MultiplyOffset / AlphaOffset / AdditiveOffset / 205 shaders and
         # mesh.js's Opaque1 with both passes are shaders, not parts (this table doesn't see them)
         "Bat_echoes", "Bat_guardianOfTheNight", "Bat_illusion", "Bat_illusionFire", "Bat_mirageOrb", "Bat_nAttack",
         "AudioControl", "Light", "BatSwarmFlap",
         # 2026-11-13, the Bison (plans/fx_bison/parts.md "Who builds what", decisions.md 36-46): fxparts/uvscroll.js,
         # fxparts/bison.js (Bison_earthRupture's mover); Bison_overLord draws nothing (an aura trigger, never cued);
         # fxparts/tto_bison.js (TTO's Bison_c6Arc, Bison_row6Fx, GroundConformParticles: a no-op on the flat floor;
         # its EnergyArc / MoltenCrust are shaders). magmaClutter_ring2's ParticleSystem is not decoded from BB: wardrobe_fx.py
         # grafts it from TTO's copy (SHURIKEN_FROM_TTO), so the effect still lists ParticleSystem below (NOTES); perfectArmor's
         # Velvet is not built: no code adds its status (unreachable, decision 45)
         "UVScroll", "Bison_earthRupture", "Bison_overLord", "Bison_c6Arc", "Bison_row6Fx", "GroundConformParticles",
         # 2026-11-13, the Cat (plans/fx_cat/parts.md "Who builds what", decisions.md 46-53, 59): StatusControl draws
         # nothing (data only: the cue's kill is damagePlus' life); fxparts/cat.js (Cat_grandCasinoArcade's sign flicker
         # and the machine's clips, Cat_supportFire's cannonball); fxparts/worldcollider.js (Unity 3.5's
         # WorldParticleCollider: luckyDice's / treasureHunt's dice and coins bounce on the floor); fxparts/additivealpha.js
         # (Transparent/AdditiveAlpha, a shader: this table doesn't see it). supportFire_hit's ParticleSystem is grafted
         # from TTO's copy as magmaClutter_ring2's (NOTES below)
         "StatusControl", "Cat_grandCasinoArcade", "Cat_supportFire", "WorldParticleCollider",
         # 2026-11-13, the Chameleon (plans/fx_chameleon/parts.md "Rank by value", decisions.md 55-61): fxparts/chameleon.js
         # (Chameleon_nAttack: the arrow, a copy of the worn arrow, index.html api.propModel; Chameleon_needlePrison's 16
         # needles); Chameleon_campFire draws nothing (data only: its heal; the cue's kill is its life); mesh.js's FX/Invisible
         # and Self-Illumin/DoubleTexture, index.html's FX/Blend / FX/Invisible hero looks are shaders (this table doesn't see
         # them). thunderDragon_ring2's and zeroShot_ring's ParticleSystems are grafted from TTO's copies (NOTES below)
         "Chameleon_nAttack", "Chameleon_needlePrison", "Chameleon_campFire"}
# a line after an effect in the "Per effect" list, and a class's own notes under its heading (2026-11-13, the Bison:
# decisions.md 40, 45, 46): what this scan cannot see
NOTES = {
    "bison": {
        "magmaClutter_ring2": "its ParticleSystem / ParticleSystemRenderer (Unity 3.5 Shuriken, not decoded from BB) are "
                              "grafted from TTO's copy by `wardrobe_fx.py` (SHURIKEN_FROM_TTO, BB's Bomb2 material): drawn",
        "perfectArmor": "Velvet (its shader) not built: no BB or TTO code adds the perfectArmor status (unreachable)",
        "perfectShield": "no BB or TTO code adds the perfectShield status (unreachable; never cued)",
    },
    "cat": {
        "supportFire_hit": "its ParticleSystem / ParticleSystemRenderer (Unity 3.5 Shuriken, not decoded from BB) are "
                           "grafted from TTO's copy by `wardrobe_fx.py` (SHURIKEN_FROM_TTO, BB's Bomb2 material): drawn",
    },
    "chameleon": {
        n: "its ParticleSystems / ParticleSystemRenderers (Unity 3.5 Shuriken, not decoded from BB) are grafted from TTO's "
           "copy by `wardrobe_fx.py` (SHURIKEN_FROM_TTO, matched by node name and material, BB's own materials): drawn"
        for n in ("thunderDragon_ring2", "zeroShot_ring")
    },
}
CLASS_NOTES = {
    "bison": ["Status looks `CharacterControl.cs` loads for the Bison (not in `Bison.cs`, so not scanned above; every one "
              "ready): holdCharge_ring + holdCharge (:34670, :34673), berserkerRush_ring + berserkerRush (:34876, :34888), "
              "furyTrance1-3 (:34963), overPower_horn1-2 (:35010, on Head with localRotation Euler(-90, 0, 0): the cue's bone "
              "+ rot) + overPower_ring (:35028), ironShield (:35064), diamondShield (:35095), perfectShield (:35129), "
              "perfectArmor (:35164; its Velvet shader not built: unreachable, no BB or TTO code adds the perfectShield / "
              "perfectArmor status), titanForm (:35243); the hero prefab's nAttack_hit / cAttack_hit and overLord "
              "(plans/fx_bison/parts.md \"Read this first\" 2)."],
}
EMITTERS = {"RingEmitter", "ImageEmitter", "LineEmitter", "VortexEmitter", "EmblemEmitter", "BoltEmitter", "TrailEmitter"}
# not parts: MeshRenderer is an emitter's own renderer (else counted as StaticMesh); physics draws nothing (the game uses it
# for hits, which the wardrobe has no targets for)
SKIP = {"Transform", "MeshFilter", "MeshRenderer", "BoxCollider", "SphereCollider", "CapsuleCollider", "MeshCollider",
        "Rigidbody", "CharacterController"}
PATH = re.compile(r'"(GameAssets/[^"]*?/Effects/[^"]+)"', re.I)


def parts(game, root_obj):
    """The set of part names in one prefab's tree."""
    out = set()

    def walk(go_obj, depth):
        go = go_obj.read_typetree()
        here, has_mr, children = set(), False, []
        for comp in go["m_Component"]:
            c = game.obj(comp[1] if isinstance(comp, (list, tuple)) else comp.get("second", comp.get("component")), go_obj.assets_file)
            if c is None:
                continue
            ty = c.type.name
            if ty == "Transform":
                children = c.read_typetree()["m_Children"]
            elif ty == "MonoBehaviour":
                n = game.script_name(c.get_raw_data(), c.assets_file)
                here.add("EffectControl(child)" if n == "EffectControl" and depth else n)
            elif ty == "MeshRenderer":
                has_mr = True
            elif ty not in SKIP:
                here.add(ty)
        if has_mr and not (here & EMITTERS):
            here.add("StaticMesh")
        out.update(here)
        for ch in children:
            tro = game.obj(ch, go_obj.assets_file)
            if tro is not None:
                walk(game.obj(tro.read_typetree()["m_GameObject"], tro.assets_file), depth + 1)

    walk(root_obj, 0)
    return out


def main():
    game = Game()
    md = game.files["mainData"]
    inv, cache = {}, {}
    for cls in CLASSES:
        src = os.path.join(SRC, cls.capitalize() + ".cs")
        loads = {}                                         # Resources path (lower case, as the container) -> (line, the code's spelling)
        for i, line in enumerate(open(src, encoding="utf-8", errors="replace"), 1):
            for p in PATH.findall(line):
                loads.setdefault(p.lower(), (i, p))
        own, others = {}, []
        for key, (line, spelt) in sorted(loads.items()):
            if key not in game.container:
                continue                                   # a folder prefix built at run time, or not a Resources asset
            if key not in cache:
                o = game.obj(game.container[key], md)
                cache[key] = sorted(parts(game, o)) if o is not None and o.type.name == "GameObject" else None
            if cache[key] is None:
                continue
            if f"/heroes/{cls}/effects/" not in key:       # a pet's, or another class's shown on this one (a buff, a potion)
                others.append(key)
                continue
            # named as the code spells it, the name a cue gives (2026-11-10: returnCast, not the container's returncast)
            name = spelt.rsplit("/", 1)[1]
            own[name] = e = {"line": line, "parts": cache[key]}
            # a ready effect must also extract (every script's field bytes decoded); in memory only, nothing written
            if set(cache[key]) <= BUILT:
                try:
                    effect(game, cls, name, {}, {}, set())
                except Exception as ex:                    # noqa: BLE001 (reported, the run goes on)
                    e["extract_error"] = f"{type(ex).__name__}: {ex}"
        inv[cls] = {"own": own, "others": others}
        bad = [k for k, v in own.items() if "extract_error" in v]
        print(f"{cls}: {len(own)} own effects, {len(others)} others' loaded by {cls.capitalize()}.cs"
              + (f"; ready but not extracting: {bad}" if bad else ""))
    json.dump(inv, open(os.path.join(ROOT, "plans", "fx_inventory.json"), "w", encoding="utf-8"), indent=1)
    write_md(inv)


def write_md(inv):
    ready_ = lambda v: set(v["parts"]) <= BUILT and "extract_error" not in v
    effs = [(c, k, set(v["parts"])) for c, e in inv.items() for k, v in e["own"].items()]
    allparts = sorted({p for _, _, x in effs for p in x} - BUILT)
    lines = ["# Effect parts each class needs", "",
             "Written by `pipeline/wardrobe_fx_inventory.py` (do not edit by hand; run it again). Effects = the prefabs in a",
             "class's own Effects folder (`heroes/<cls>/effects`) that its `<Class>.cs` loads: skills, hits, buffs, projectiles,",
             "not only skills. Physics parts (colliders, Rigidbody) are left out: they draw nothing.",
             "Ready = every part is one the page builds today (" + ", ".join(sorted(BUILT)) + ") and `wardrobe_fx.py`",
             "extracts it (checked in memory). Each class's code also loads its pet's and other classes' effects (shown on it,",
             "like a Sheep's heal): counted apart, never this class's skills.", "",
             "## Per class", "", "| class | own effects | ready | not ready | parts missing (own effects needing it) | others' loaded |",
             "|---|---|---|---|---|---|"]
    for cls, e in inv.items():
        own = e["own"]
        need = collections.Counter(p for v in own.values() for p in set(v["parts"]) - BUILT)
        ready = sum(1 for v in own.values() if ready_(v))
        lines.append(f"| {cls} | {len(own)} | {ready} | {len(own) - ready} | "
                     + ", ".join(f"{p} {n}" for p, n in need.most_common()) + f" | {len(e['others'])} |")
    lines += ["", "## Per missing part", "", "Own effects that need the part (all classes), and how many of those it alone blocks",
              "(every other part of theirs is built).", "", "| part | effects | blocks alone | classes |", "|---|---|---|---|"]
    rows = []
    for p in allparts:
        users = [(c, x) for c, _, x in effs if p in x]
        alone = sum(1 for _, x in users if x - BUILT == {p})
        rows.append((alone, len(users), p, sorted({c for c, _ in users})))
    for alone, n, p, cs in sorted(rows, reverse=True):
        lines.append(f"| {p} | {n} | {alone} | {', '.join(cs)} |")
    # greedy build order: each step the part that makes the most effects ready (with what is built by then); when no
    # single part does, the one most effects need (the mesh parts unlock effects only together)
    lines += ["", "## Build order (greedy)", "", "Each step: the part that makes the most own effects ready, given the ones above it",
              "(when none alone does, the part most not-ready effects need). Ready after = all classes.", "",
              "| step | part | newly ready | ready after |", "|---|---|---|---|"]
    sets = [x for _, _, x in effs]
    have, step = set(BUILT), 0
    ready = sum(1 for x in sets if x <= have)
    lines.append(f"| 0 | (built today) | {ready} | {ready} / {len(sets)} |")
    while ready < len(sets):
        cands = {p for x in sets for p in x - have}
        gain = {p: sum(1 for x in sets if not x <= have and x <= have | {p}) for p in cands}
        best = max(cands, key=lambda p: (gain[p], sum(1 for x in sets if p in x and not x <= have), p))
        have.add(best); step += 1
        new_ready = sum(1 for x in sets if x <= have)
        lines.append(f"| {step} | {best} | {new_ready - ready} | {new_ready} / {len(sets)} |")
        ready = new_ready
    lines += ["", "## Per effect", ""]
    for cls, e in inv.items():
        lines += [f"### {cls}", ""] + [x for n in CLASS_NOTES.get(cls, []) for x in (n, "")]
        for k, v in e["own"].items():
            miss = sorted(set(v["parts"]) - BUILT)
            lines.append(f"- `{k}` ({cls.capitalize()}.cs:{v['line']}): " + ("ready" if not miss else "needs " + ", ".join(miss))
                         + (f" **extract fails: {v['extract_error']}**" if "extract_error" in v else "")
                         + (f" ({NOTES[cls][k]})" if k in NOTES.get(cls, {}) else ""))
        lines.append("")
    open(os.path.join(ROOT, "plans", "fx_inventory.md"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
