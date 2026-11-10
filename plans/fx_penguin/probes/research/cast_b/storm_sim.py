"""Read only: where the Penguin's storms go on the page's flat ground with no steering (tornado3) or a still target 10 m
ahead (typhoon3, tID 1 so rotateH(.., 0)). Unity rigidbody, mass 1, drag 2 (v *= 1 - drag*dt after the force),
fixed step 0.02 s; friction ignored. Penguin_tornado.cs:98-103; Penguin_typhoon.cs:848-853, :372 (force 11 - mLv toward
the target), ticks every 0.35 s from Init (:110-118), hit when |flat distance - target radius| < mLv (Damage.cs FindAreaTarget).
  py -3 -I checks/fx_penguin_research/cast_b/storm_sim.py"""
DT, DRAG, LV = 0.02, 2.0, 3
def run(seek, r=0.5, life=6.0):
    z, v, t, nxt, hits = 4.0, 5.0, 0.0, 0.0, []
    while t < life - 1e-9:
        if t >= nxt - 1e-9:
            nxt += 0.35
            if seek and abs(abs(10 - z) - r) < LV: hits.append(round(t, 2))
        if seek: v += (11 - LV) * (1 if 10 > z else -1) * DT
        v *= 1 - DRAG * DT
        z += v * DT; t += DT
        if not seek and t in (1.0,): pass
    return round(z, 2), hits
print("tornado3 rest (m ahead):", run(False)[0])
for r in (0.3, 0.5, 1.0):
    print("typhoon3 target radius", r, "hits (s after Init):", run(True, r)[1])
