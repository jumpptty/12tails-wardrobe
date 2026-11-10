"""Read only: the container keys under heroes/penguin that are not in a subfolder."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "pipeline"))
import wardrobe_fx as W
g = W.Game()
md = g.files["mainData"]
for k in g.container:
    if k.startswith("gameassets/characters/heroes/penguin") and k.count("/") <= 4:
        o = g.obj(g.container[k], md); print(k, o.type.name if o else None)
