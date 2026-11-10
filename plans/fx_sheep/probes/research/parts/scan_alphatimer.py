"""Read-only: every AlphaTimer / ProjectileControl instance in all 12 classes' own effects (plans/fx_inventory.json):
does the candidate layout use up exactly its bytes, the values, and what renderer + material shader the AlphaTimer's
node has (AlphaTimer fades only its own node's renderer.material: _Color if the shader has it, else _TintColor, else it
disables itself). Writes nothing but stdout.
  uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I checks/fx_sheep_research/parts/scan_alphatimer.py
"""
import collections, importlib.util, json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..", "..", "..")
spec = importlib.util.spec_from_file_location("wfx", os.path.join(ROOT, "pipeline", "wardrobe_fx.py"))
wfx = importlib.util.module_from_spec(spec); spec.loader.exec_module(wfx)
LAY = {"AlphaTimer": [("MinAlpha", "f"), ("MaxAlpha", "f"), ("FadeDelay", "f"), ("FadeEaseIn", "f"), ("FadeMiddle", "f"),
                      ("FadeEaseOut", "f"), ("eraseShadow", "b"), ("repeat", "b"), ("endDestroy", "b")],
       "ProjectileControl": [("life", "f"), ("dmg", "f"), ("velocity", "v3"), ("OwnerID", "i"), ("isInitialized", "b"), ("isDestroyed", "b")]}
inv = json.load(open(os.path.join(ROOT, "plans", "fx_inventory.json"), encoding="utf-8"))
game = wfx.Game(); md = game.files["mainData"]
stats = collections.Counter(); rows = []
def shader_of(m, base):
    mo = game.obj(m, base)
    if mo is None: return None
    t = mo.read_typetree(); sh = t["m_Shader"]; own = mo.assets_file
    if sh["m_FileID"] and "default resources" in own.externals[sh["m_FileID"] - 1].path:
        s = wfx.BUILTIN_BLEND.get(sh["m_PathID"], f"builtin{sh['m_PathID']}")
    else:
        so = game.obj(sh, own); src = so.read_typetree().get("m_Script", "") if so else ""
        s = "shader:" + (src.split('"')[1] if src.count('"') >= 2 else "?")
    return t["m_Name"], s
for cls, e in inv.items():
    for name, v in e["own"].items():
        if not ({"AlphaTimer", "ProjectileControl"} & set(v["parts"])): continue
        key = f"gameassets/characters/heroes/{cls}/effects/{name}"
        def walk(go_obj, path):
            go = go_obj.read_typetree(); kids = []; here = []; rend = []
            for comp in go["m_Component"]:
                c = game.obj(comp[1] if isinstance(comp, (list, tuple)) else comp.get("second"), go_obj.assets_file)
                if c is None: continue
                ty = c.type.name
                if ty == "Transform": kids = c.read_typetree()["m_Children"]
                elif ty == "MonoBehaviour":
                    raw = c.get_raw_data(); sn = game.script_name(raw, c.assets_file)
                    here.append(sn)
                    if sn in LAY:
                        try: d = wfx.decode(raw, LAY[sn], wfx.header_len(raw)); stats[sn + " ok"] += 1
                        except Exception as ex: d = f"FAIL {ex}"; stats[sn + " FAIL"] += 1
                        rows.append((cls, name, path + "/" + go["m_Name"], sn, d))
                elif ty.endswith("Renderer"):
                    t = c.read_typetree(); rend.append((ty, [shader_of(m, c.assets_file) for m in t.get("m_Materials", [])]))
                else:
                    if ty not in ("MeshFilter",): here.append(ty)
            if "AlphaTimer" in here:
                rows.append((cls, name, path + "/" + go["m_Name"], "  renderer", rend, "others on node:", [h for h in here if h != "AlphaTimer"]))
            for ch in kids:
                tro = game.obj(ch, go_obj.assets_file)
                if tro is not None: walk(game.obj(tro.read_typetree()["m_GameObject"], tro.assets_file), path + "/" + go["m_Name"])
        walk(game.obj(game.container[key], md), "")
for r in rows: print(*r)
print(dict(stats))
