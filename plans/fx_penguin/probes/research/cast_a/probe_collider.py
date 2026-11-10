"""Read only: the Penguin and Sheep hero prefabs' CharacterController (centre, radius, height): Ice Shield's look sits at
collider.bounds.center, scaled Clamp(radius + 0.4, 0.5, 2) (CharacterControl.cs:38619-38627).
  uv run --no-project --with UnityPy python -I checks/fx_penguin_research/cast_a/probe_collider.py"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "pipeline"))
import wardrobe_fx as W  # noqa: E402

g = W.Game()
md = g.files["mainData"]
rm = next(o for o in md.objects.values() if o.type.name == "ResourceManager").read_typetree()
for cls in ("penguin", "sheep"):
    for k, v in rm["m_Container"]:
        o = g.obj(v, md)
        if k != f"gameassets/characters/heroes/{cls}/{cls}" or o is None or o.type.name != "GameObject":
            continue
        for comp in o.read_typetree()["m_Component"]:
            c = g.obj(comp[1] if isinstance(comp, (list, tuple)) else comp.get("second", comp.get("component")), o.assets_file)
            if c is not None and c.type.name in ("CharacterController", "CapsuleCollider", "Transform"):
                t = c.read_typetree()
                print(cls, c.type.name, {kk: t[kk] for kk in t if kk in ("m_Radius", "m_Height", "m_Center", "m_LocalScale")})
