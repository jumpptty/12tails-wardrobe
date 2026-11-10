"""Read-only check (fx_penguin_research/parts): the tornado's and typhoon's paths on the page's flat ground, as
Penguin_tornado.cs / Penguin_typhoon.cs move them (Unity units, x right, z ahead of the hero). FixedUpdate every 0.02 s
(Unity's default); drag 2 (Penguin_tornado.cs:103, Penguin_typhoon.cs:853) as PhysX's damping v *= 1 - drag dt (the other
common form, v /= 1 + drag dt, is printed too); mass 1 (the prefab's Rigidbody), ForceMode.Force (a = F).
  tornado: v0 = 5 x forward (:98), no input, so no force: x(t) = 2.5 (1 - e^-2t)
  typhoon: v0 = rotateH(5 x forward, (tID - 1) x 120) (:848; Math.cs:838-842), force (11 - mLv) = 8 toward the target,
           flat (:360-372), speed capped at 30 (:405-416; 40 with Ice Twister #443, :385-396)
  py -3 -I checks/fx_penguin_research/parts/sim_typhoon.py
"""
import math

DT = 0.02


def run(v, p, target, force, damp, T):
    out = []
    for k in range(int(round(T / DT))):
        if target is not None and force:
            d = (target[0] - p[0], target[1] - p[1]); n = math.hypot(*d)
            if n > 1e-9:
                v = (v[0] + force * d[0] / n * DT, v[1] + force * d[1] / n * DT)
        s = math.hypot(*v)
        if s > 30:
            v = (30 * v[0] / s, 30 * v[1] / s)
        v = damp(v)
        p = (p[0] + v[0] * DT, p[1] + v[1] * DT)
        out.append(((k + 1) * DT, p, v))
    return out


for name, damp in (("v *= 1 - 2dt", lambda v: (v[0] * (1 - 2 * DT), v[1] * (1 - 2 * DT))),
                   ("v /= 1 + 2dt", lambda v: (v[0] / (1 + 2 * DT), v[1] / (1 + 2 * DT)))):
    tr = run((0, 5), (0, 4), None, 0, damp, 6)
    print(f"tornado ({name}): from 4 m ahead, at 0.5 / 1 / 2 / 6 s:",
          [f"{t:.1f}s z {p[1]:.2f}" for t, p, v in tr if round(t, 2) in (0.5, 1.0, 2.0, 6.0)],
          f"(closed form 2.5 (1 - e^-2t) at 6 s: {4 + 2.5 * (1 - math.exp(-12)):.2f})")
    for ang in (0, 120, 240):
        a = math.radians(ang)
        v0 = (-5 * math.sin(a), 5 * math.cos(a))          # rotateH((0, 0, 5), ang): x = -z sin, z = z cos
        tr = run(v0, (0, 4), (0, 10), 8, damp, 6)
        first = next((t for t, p, v in tr if math.hypot(p[0], p[1] - 10) < 0.5), None)
        last = tr[-1]
        dmax = max(math.hypot(p[0], p[1] - 10) for t, p, v in tr if first and t > first + 1) if first else None
        print(f"  typhoon ({name}) angle {ang:3d}: v0 ({v0[0]:+.2f}, {v0[1]:+.2f}); within 0.5 m of the 10 m point at "
              f"{first if first is None else round(first, 2)} s; at 6 s at ({last[1][0]:+.2f}, {last[1][1]:.2f}); "
              f"wobble after arrival + 1 s: {dmax and round(dmax, 2)} m; terminal speed F / drag = 4 m/s")
