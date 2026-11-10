"""Disassemble the TTO/Sheep shaders' D3D11 programs (read only): the Shader's compressedBlob (LZ4) holds serialized
sub-programs, each carrying a DXBC container; D3DDisassemble (Windows' d3dcompiler_47.dll) prints them."""
import ctypes, os, sys, importlib.util
import lz4.block
H = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("t", os.path.join(H, "..", "..", "..", "pipeline", "wardrobe_fx_tto.py"))
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
tto = t.Tto("sheep", ["gleamingBreath_cast", "lucentBarrier", "gleamingBreath_land"])
d3d = ctypes.WinDLL("d3dcompiler_47.dll")
class Blob(ctypes.Structure): pass
def dis(b):
    out = ctypes.c_void_p()
    hr = d3d.D3DDisassemble(ctypes.c_char_p(b), ctypes.c_size_t(len(b)), 0, None, ctypes.byref(out))
    if hr != 0: return f"D3DDisassemble failed {hr:#x}"
    vt = ctypes.cast(ctypes.cast(out, ctypes.POINTER(ctypes.c_void_p))[0], ctypes.POINTER(ctypes.c_void_p))
    getptr = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)(vt[3]); getsize = ctypes.WINFUNCTYPE(ctypes.c_size_t, ctypes.c_void_p)(vt[4])
    return ctypes.string_at(getptr(out), getsize(out)).decode("latin1")
for o in tto.env.objects:
    if o.type.name != "Shader": continue
    tt = o.read_typetree(); n = tt["m_ParsedForm"]["m_Name"]
    if not n.startswith("TTO/Sheep/") or "Goddess" in n: continue
    blob = bytes(tt["compressedBlob"])
    off, cl, dl = tt["offsets"], tt["compressedLengths"], tt["decompressedLengths"]
    # one platform; per-platform lists may be nested (one segment each)
    off, cl, dl = [x[0] if isinstance(x, list) else x for x in (off[0], cl[0], dl[0])] if isinstance(off[0], list) else (off[0], cl[0], dl[0])
    raw = lz4.block.decompress(blob[off:off + cl], uncompressed_size=dl)
    lines = [f"// {n}"]
    k = raw.find(b"DXBC")
    while k >= 0:
        size = int.from_bytes(raw[k + 24:k + 28], "little")
        lines.append(f"// ===== DXBC at {k}"); lines.append(dis(raw[k:k + size]))
        k = raw.find(b"DXBC", k + size)
    open(os.path.join(H, "dxbc_" + n.split("/")[-1].replace(" ", "_") + ".txt"), "w").write("\n".join(lines))
    print(n)
