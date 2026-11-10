"""The Penguin TTO cue numbers (plans/fx_penguin/tto.md): Emperors March's flock spots, frost trail, ball, goal and the
flock's positions at the goal; Constellation variant B (5 stars). Space: x right, y up, d ahead of the hero (hero faces
+z = d). float32 where the game accumulates. uv run --no-project --with numpy python -I calc.py"""
import math, json
import numpy as np
f32 = np.float32
r3 = lambda v: round(float(v), 3)
# ---- Emperors March (TTO1102:Penguin.<RPC_emperorPenguin>d__356 / FlockSpot@0x1DA4BF0 / FlockRise d__357 / EmperorShot d__358)
flock = 5
print("== flock spots (FlockSpot: u = i/(flock-1), a = 150u - 75 deg, r 1.25 for i<5 else 1.9; right*sin + fwd*cos)")
axis = (0.0, math.cos(math.radians(45)), math.sin(math.radians(45)))   # LookRotation(dir) x Euler(45,0,0) applied to up
spots = []
for i in range(flock):
    u = 0.5 if flock <= 1 else min(1, max(0, i / (flock - 1)))
    a = math.radians(u * 150 - 75); r = 1.25 if i < 5 else 1.9
    x, d = r * math.sin(a), r * math.cos(a); spots.append((x, d))
    print(i, "emerge", {"x": r3(x), "d": r3(d)}, "penguin start", {"x": r3(x), "y": r3(-0.7 * axis[1]), "d": r3(d - 0.7 * axis[2])})
print("== frost trail (frostAt float32 from 1.2, += 1.6 while <= d; d = min(28 e, reach 22); at 0.45 + f ahead, ground)")
reach = f32(22); fa = f32(1.2); out = []
while fa <= reach:
    t = 0.85 + float(fa) / 28; out.append((r3(t), r3(0.45 + float(fa)))); fa = f32(fa + f32(1.6))
print(len(out), out, "next frostAt", float(fa))
e_goal = 22 / 28; tg = 0.85 + e_goal
print("== goal at", r3(tg), "ball at d", 0.45 + 22, "y 0.45 (ground + 0.45)")
print("== flock at the goal (lag = d - 28 (0.06 + 0.035 i), ring 0.65 around the lane at 2 pi i / n + 540 deg x e, + 0.15 up; centre = from (0.45 ahead, 0.2 up) + lag)")
for i in range(flock):
    delay = 0.06 + 0.035 * i; s = min(1, max(0, (e_goal - delay) / 0.18)); lag = max(0, 22 - delay * 28)
    th = 2 * math.pi * i / flock + math.radians(540) * e_goal
    x = 0.65 * math.cos(th); y = 0.2 + 0.15 + 0.65 * math.sin(th); d = 0.45 + lag
    print(i, "s", round(s, 3), "poof", {"x": r3(x), "y": r3(y), "d": r3(d)})
print("== ball drop 0.55-0.8: ballAt (0.45 ahead, 0.2 up) + up (1 - u^2) 0.8, u = 4 (t - 0.55)")
for t in (0.55, 0.6, 0.7, 0.8): u = min(1, 4 * (t - 0.55)); print(t, "y", r3(0.2 + (1 - u * u) * 0.8))
print("== flock rise 0.3-0.55: h = (1 - (1 - s)^2) 0.7 + 0.15 sin(s pi), s = 4 (t - 0.3), along axis (0, .707, .707)")
for t in (0.3, 0.4, 0.425, 0.5, 0.55): s = min(1, 4 * (t - 0.3)); print(t, r3((1 - (1 - s) ** 2) * 0.7 + 0.15 * math.sin(s * math.pi)))
# ---- Constellation variant B: target 10 m ahead, 4 foes, a regular pentagon R 3 m about (0, 13)
print("== Constellation B (pentagon R 3 about d 13; InSkyOrder = ascending atan2(dx, dz) about the stars' mean; target last at +180)")
R, c = 3.0, 13.0
phis = [-108, -36, 36, 108, 180]        # ascending order
st = [(R * math.sin(math.radians(p)), c + R * math.cos(math.radians(p))) for p in phis]
st[-1] = (0.0, 10.0)
for i, (x, d) in enumerate(st):
    print(i, "star", {"x": r3(x), "d": r3(d)}, "falls", round(1.1 + 0.3 * i, 2), "impact", round(1.7 + 0.3 * i, 2), "mark kill", round(1.3 + 0.3 * i, 2))
n = len(st)
for i in range(n):
    a, b = st[i], st[(i + 1) % n]; dx, dd = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dd)
    yaw = math.degrees(math.atan2(dx, dd)); t0 = 0.4 + 0.12 * i
    print(i, "line spawn", round(t0, 2), {"x": r3(a[0]), "y": 1, "d": r3(a[1]), "to": [r3(b[0]), 1, r3(b[1])], "kill": round(3.55 - t0, 2)},
          "lineFire", {"x": r3((a[0] + b[0]) / 2), "y": 1, "d": r3((a[1] + b[1]) / 2), "rot": [0, r3(yaw), 0], "len": r3(L)})
mx = sum(p[0] for p in st) / n; md = sum(p[1] for p in st) / n
print("middle (ignite / giant / giantImpact)", {"x": r3(mx), "d": r3(md)}, "lastImpact", round(1.7 + 0.3 * (n - 1), 2), "ignite", round(1.75 + 0.3 * (n - 1), 2), "giantImpact", round(2.35 + 0.3 * (n - 1), 2))
