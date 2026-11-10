"""Dump the Sheep TTO materials' full property lists and their shaders' parsed forms (read only)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "pipeline"))
import importlib.util
spec = importlib.util.spec_from_file_location("t", os.path.join(os.path.dirname(__file__), "..", "..", "..", "pipeline", "wardrobe_fx_tto.py"))
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
tto = t.Tto("sheep", t.SKILL_FX["sheep"])
seen = set()
for o in tto.env.objects:
    if o.type.name != "Material":
        continue
    m = o.read_typetree()
    if not m["m_Name"].startswith(("sheepRow6", "Point")):
        continue
    sh = tto.deref(o.assets_file, m["m_Shader"])
    shn = sh.read_typetree()["m_ParsedForm"]["m_Name"] if sh else "?"
    p = m["m_SavedProperties"]
    print("MAT", m["m_Name"], "|", shn, "| kw", m.get("m_ValidKeywords") or m.get("m_ShaderKeywords"), "| queue", m.get("m_CustomRenderQueue"))
    print("   floats", {k: round(v, 4) for k, v in p["m_Floats"]})
    print("   colors", {k: [round(v[c], 4) for c in "rgba"] for k, v in p["m_Colors"]})
    print("   texs", {k: (tto.deref(o.assets_file, v["m_Texture"]).read_typetree()["m_Name"] if tto.deref(o.assets_file, v["m_Texture"]) else None, v["m_Scale"], v["m_Offset"]) for k, v in p["m_TexEnvs"]})
    if sh is not None and shn not in seen:
        seen.add(shn)
        pf = sh.read_typetree()["m_ParsedForm"]
        json.dump(pf, open(os.path.join(os.path.dirname(__file__), "shader_" + shn.replace("/", "_").replace(" ", "_") + ".json"), "w"), indent=1, default=str)
        print("   SHADER props", [(x["m_Name"], x["m_Description"], x["m_Type"], x.get("m_DefValue[0]")) for x in pf["m_PropInfo"]["m_Props"]])
        for ss in pf["m_SubShaders"]:
            for ps in ss["m_Passes"]:
                st = ps["m_State"]
                rt = st["rtBlend0"]
                print("   PASS", ps.get("m_Name"), "tags", ps.get("m_Tags"), "blend src", rt["srcBlend"]["val"], "dst", rt["destBlend"]["val"], "op", rt["blendOp"]["val"],
                      "zwrite", st["zWrite"]["val"], "cull", st["culling"]["val"], "ztest", st["zTest"]["val"])
        print("   platforms", sh.read_typetree().get("platforms"))
