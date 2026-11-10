"""Export the three TTO/Sheep shaders with UnityPy's ShaderConverter (read only) into this folder."""
import os, sys, importlib.util
H = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("t", os.path.join(H, "..", "..", "..", "pipeline", "wardrobe_fx_tto.py"))
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
tto = t.Tto("sheep", ["gleamingBreath_cast", "lucentBarrier", "gleamingBreath_land"])
for o in tto.env.objects:
    if o.type.name == "Shader":
        tt = o.read_typetree()
        n = tt["m_ParsedForm"]["m_Name"]
        if n.startswith("TTO/"):
            try:
                txt = o.read().export()
            except Exception as e:
                txt = f"export failed: {e!r}"
            open(os.path.join(H, "export_" + n.replace("/", "_").replace(" ", "_") + ".shader"), "w", encoding="utf-8").write(txt)
            print(n, len(txt))
