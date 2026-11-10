"""Read only: the Mana Vortex summon prefab (Resources GameAssets/Characters/Elementals/ManaVortex/ManaVortex, Penguin.cs:10407):
its nodes, component types, MonoBehaviour script names, Animation clips and AudioSources.
  uv run --no-project --with UnityPy python -I checks/fx_penguin_research/cast_a/probe_vortex.py"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "pipeline"))
import wardrobe_fx as W  # noqa: E402

g = W.Game()
md = g.files["mainData"]
print([k for k in g.container if "elementals/manavortex" in k])
root = g.obj(g.container["gameassets/characters/elementals/manavortex/manavortex"], md)


def walk(o, depth):
    go = o.read_typetree()
    out = []
    kids = []
    for comp in go["m_Component"]:
        c = g.obj(comp[1] if isinstance(comp, (list, tuple)) else comp.get("second", comp.get("component")), o.assets_file)
        if c is None:
            continue
        t = c.type.name
        if t == "MonoBehaviour":
            out.append("Mono " + g.script_name(c.get_raw_data(), c.assets_file))
        elif t == "Animation":
            a = c.read_typetree()
            names = []
            for cl in a.get("m_Animations", []):
                x = g.obj(cl, c.assets_file)
                names.append(x.read_typetree()["m_Name"] if x else "?")
            out.append(f"Animation {names}")
        elif t == "AudioSource":
            a = c.read_typetree()
            x = g.obj(a["m_audioClip"], c.assets_file)
            out.append(f"AudioSource {x.read_typetree()['m_Name'] if x else None} loop {a.get('Loop')} awake {a.get('m_PlayOnAwake')}")
        elif t == "Transform":
            tr = c.read_typetree()
            kids = tr["m_Children"]
            out.append(f"T pos {tr['m_LocalPosition']} scale {tr['m_LocalScale']['x']}")
        else:
            out.append(t)
    print("  " * depth + go["m_Name"], out)
    for k in kids:
        tr = g.obj(k, o.assets_file)
        walk(g.obj(tr.read_typetree()["m_GameObject"], tr.assets_file), depth + 1)


walk(root, 0)
