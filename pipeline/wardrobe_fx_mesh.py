"""Mesh parts of the game's effects, for pipeline/wardrobe_fx.py (2026-11-09; plans/fx_wolf/parts.md steps 5, 7, 9:
StaticMesh = a MeshFilter drawn by a MeshRenderer with no emitter, SkinnedMeshRenderer, Animation, and the data
ShatterMesh needs). Its own file so the mesh work never edits wardrobe_fx.py.

component(game, comp_obj, ty, node, ctx) is called for every MeshFilter, SkinnedMeshRenderer and Animation component of
an effect node; it returns a list of component dicts to append to node["comps"] (JSON-safe), or None. ctx: cls, effect
(the prefab's name), mats / texs / sounds (the run's collections: add to them), material (wardrobe_fx.material: call
ctx["material"](game, pptr, comp_obj.assets_file, ctx["mats"], ctx["texs"]) for a renderer's materials).
"""


def component(game, comp_obj, ty, node, ctx):
    return None                          # not built yet (the mesh agent fills this in)
