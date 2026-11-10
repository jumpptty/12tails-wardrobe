"""Read only: the Penguin hero MonoBehaviour's public fields (Penguin.cs:16413-17004: mChar, footsteps, nAttack_fire,
nAttack_hit, castEffect, castRing, manaMissile_fire, manaMissile_Fx, manaMissile_hit, deadEffect) and what each points at.
  uv run --no-project --with UnityPy python -I checks/fx_penguin_research/cast_a/probe_fields.py"""
import os
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "pipeline"))
import wardrobe_fx as W  # noqa: E402

g = W.Game()
md = g.files["mainData"]
by_pid = {}
for k, v in g.container.items():
    o = g.obj(v, md)
    if o is not None:
        by_pid[(o.assets_file.name, o.path_id)] = k
rm = next(o for o in md.objects.values() if o.type.name == "ResourceManager").read_typetree()
root = next(o for k, v in rm["m_Container"] if k == "gameassets/characters/heroes/penguin/penguin"
            for o in [g.obj(v, md)] if o is not None and o.type.name == "GameObject")   # the path is the prefab's and the script's
go = root.read_typetree()
for comp in go["m_Component"]:
    c = g.obj(comp[1] if isinstance(comp, (list, tuple)) else comp.get("second", comp.get("component")), root.assets_file)
    if c is None or c.type.name != "MonoBehaviour":
        continue
    raw = c.get_raw_data()
    name = g.script_name(raw, c.assets_file)
    off = W.header_len(raw)
    print(name, len(raw) - off, "field bytes")
    if name != "Penguin":
        continue
    for i in range(0, len(raw) - off, 8):
        fid, pid = struct.unpack_from("<ii", raw, off + i)
        o = g.obj((fid, pid), c.assets_file)
        nm = (o.read_typetree().get("m_Name") if o is not None and o.type.name in ("GameObject", "AudioClip") else (o.type.name if o else None))
        print(f"  field {i // 8}: ({fid}, {pid}) -> {o.type.name if o else None} {nm}  {by_pid.get((o.assets_file.name, o.path_id)) if o else ''}")
