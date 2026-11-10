"""Read only: an independent re-sim of Mana Missile's 7 missiles (Penguin_manaMissile.cs FixedUpdate: 12 m/s, every 0.1 s
RotateTowards(forward, aim - pos, 0.15 rad), the first turn on the first step) to the floor (sphere r 0.3 -> y 0.3).
  py -3 -I checks/fx_penguin_research/verify/missile_hits.py"""
import math, sys
aim = (0.0, float(sys.argv[1]) if len(sys.argv) > 1 else 0.0, 10.0)   # x, y, z
def rot_towards(f, t, ang):
    tn = math.sqrt(sum(c * c for c in t)); t = [c / tn for c in t]
    d = max(-1, min(1, sum(a * b for a, b in zip(f, t)))); th = math.acos(d)
    if th <= ang: return t
    # slerp f -> t by ang
    s = math.sin(th); a = math.sin(th - ang) / s; b = math.sin(ang) / s
    return [a * x + b * y for x, y in zip(f, t)]
def dir_of(yaw):
    pitch = math.atan2(1, 9)                     # down
    f = [0, -math.sin(pitch), math.cos(pitch)]   # Unity forward after LookRotation
    x = math.radians(-0.2 * abs(yaw)); y = math.radians(yaw)
    # local Euler(x, y, 0) applied in the look frame: Ry(y) then Rx(x) on (0,0,1)
    v = [math.sin(y) * math.cos(x), -math.sin(x), math.cos(y) * math.cos(x)]
    # look frame: rotate v by pitch about x
    c, s = math.cos(pitch), math.sin(pitch)
    return [v[0], c * v[1] + s * v[2], -s * v[1] + c * v[2]]
for yaw in (0, 24, 48, 72):
    p = [0.0, 1.0, 1.0]; f = dir_of(yaw); t = 0.0; nxt = 0.0
    while p[1] > 0.3 and t < 3:
        if nxt < t + 1e-9:
            nxt = t + 0.1; f = rot_towards(f, [a - b for a, b in zip((aim[0], aim[1], aim[2]), p)], 0.15)
        p = [a + 12 * 0.02 * b for a, b in zip(p, f)]; t += 0.02
    print(yaw, round(t, 2), [round(c, 2) for c in p])
