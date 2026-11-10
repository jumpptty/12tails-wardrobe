import os, importlib.util, json
H = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("t", os.path.join(H, "..", "..", "..", "pipeline", "wardrobe_fx_tto.py"))
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
tto = t.Tto("sheep", ["gleamingBreath_cast"])
for o in tto.env.objects:
    if o.type.name != "Shader": continue
    tt = o.read_typetree(); n = tt["m_ParsedForm"]["m_Name"]
    if n != "TTO/Sheep/Celestial Ring": continue
    print({k: (v if not isinstance(v, (bytes, list)) or len(v) < 40 else f"<{len(v)}>") for k, v in tt.items() if k != "m_ParsedForm"})
    p = tt["m_ParsedForm"]["m_SubShaders"][0]["m_Passes"][0]
    for k in ("progVertex", "progFragment"):
        print(k, p[k]["m_PlayerSubPrograms"], p[k]["m_ParameterBlobIndices"])
