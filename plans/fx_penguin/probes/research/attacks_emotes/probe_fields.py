"""Read only: the Penguin hero MonoBehaviour's PPtr fields (Penguin.cs:16413-17004: mChar, footsteps, nAttack_fire,
nAttack_hit, castEffect, castRing, manaMissile_*, deadEffect) and the Resources path each points at. The container has
several entries named heroes/penguin/penguin (prefab and scripts), so all are tried.
  uv run --no-project --with UnityPy python -I checks/fx_penguin_research/attacks_emotes/probe_fields.py"""
import os
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "pipeline"))
import wardrobe_fx as W  # noqa: E402

g = W.Game()
md = g.files["mainData"]
rm = next(o for o in md.objects.values() if o.type.name == "ResourceManager").read_typetree()
by_pid = {}
cands = []
for k, v in rm["m_Container"]:
    o = g.obj(v, md)
    if o is not None:
        by_pid[(o.assets_file.name, o.path_id)] = k
        if k == "gameassets/characters/heroes/penguin/penguin" and o.type.name == "GameObject":
            cands.append(o)
for root in cands:
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
        for i in range(0, len(raw) - off - 7, 8):
            fid, pid = struct.unpack_from("<ii", raw, off + i)
            o = g.obj((fid, pid), c.assets_file)
            nm = o.read_typetree().get("m_Name") if o is not None and o.type.name in ("GameObject", "AudioClip") else (o.type.name if o else None)
            print(f"  field {i // 8}: ({fid}, {pid}) -> {nm}  {by_pid.get((o.assets_file.name, o.path_id)) if o else ''}")
