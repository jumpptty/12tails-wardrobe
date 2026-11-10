"""Each Sheep TTO effect sound: BB's rip WAV the build used vs TTO's own AudioClip length (read only)."""
import os, importlib.util, wave
H = os.path.dirname(os.path.abspath(__file__))
def load(n, p):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
t = load("t", os.path.join(H, "..", "..", "..", "pipeline", "wardrobe_fx_tto.py"))
tto = t.Tto("sheep", t.SKILL_FX["sheep"]); b = t.Build(tto)
for n in t.SKILL_FX["sheep"]:
    t.effect(tto, b, n)
for n, o in sorted(b.sounds.items()):
    src = t.bb().rip_wav("sheep", n)
    w = wave.open(src); bl = w.getnframes() / w.getframerate()
    print(f"{n:22} TTO {o.read_typetree().get('m_Length', 0):.3f} s  BB {bl:.3f} s  {os.path.relpath(src, t.bb().RIP)}")
