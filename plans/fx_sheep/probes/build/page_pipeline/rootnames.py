"""Read only: does every hero effect prefab's root GameObject carry its Resources name (case aside)?"""
import importlib.util, os, sys
spec = importlib.util.spec_from_file_location("wfx", sys.argv[1]); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
g = w.Game(); md = g.files["mainData"]; same = diff = case = 0
for k, p in g.container.items():
    if "/heroes/" not in k or "/effects/" not in k: continue
    o = g.obj(p, md)
    if o is None or o.type.name != "GameObject": continue
    n = o.read_typetree()["m_Name"]; base = k.rsplit("/", 1)[1]
    if n.lower() != base: diff += 1; print("differs:", k, n)
    elif n != base: case += 1
    else: same += 1
print({"same": same, "case only": case, "differs": diff})
