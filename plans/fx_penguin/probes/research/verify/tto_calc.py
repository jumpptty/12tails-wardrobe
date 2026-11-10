# re-check of tto.md numbers (verification 2026-11-10)
import numpy as np, math
f=np.float32(1.2); n=0
while f <= np.float32(22.0):
    n+=1; f=np.float32(f+np.float32(1.6))
print("frosts", n, repr(f))
for i in range(5):
    a=math.radians(150*i/4-75); print("spot",i, round(1.25*math.sin(a),3), round(1.25*math.cos(a),3))
e=np.float32(22)/np.float32(28); print("goal t", 0.85+float(e))
print("burst t", 0.85+(10-0.45-0.5)/28)
