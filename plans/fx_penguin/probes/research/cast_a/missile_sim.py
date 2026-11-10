"""Read only: Mana Missile's 7 homing missiles (rank 4 + #402) flown to the 10 m ground point, as Penguin_manaMissile does
(12 m/s, Penguin_manaMissile.cs ctor w17fC8Ic9V = (0, 0, 12); every 0.1 s RotateTowards(forward, to - pos, 0.15 rad);
FixedUpdate 0.02 s), fired from 1 m up, 1 m ahead (Penguin.cs:21169), rotation LookRotation(fireDir) x
Euler(-0.2|a|, a, 0) (:10220), a = -72 + 24 i (:10199-10215). The sphere (radius 0.3, the prefab) meets the floor at
y = 0.3. Prints each missile's ground time (from the fire), its landing point and its distance to the aim point.
  py -3 checks/fx_penguin_research/cast_a/missile_sim.py [aim distance, 10] [aim height, 0]"""
import math
import sys

D = float(sys.argv[1]) if len(sys.argv) > 1 else 10.0
H = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0


def qmul(a, b):
    w1, x1, y1, z1 = a; w2, x2, y2, z2 = b
    return (w1*w2 - x1*x2 - y1*y2 - z1*z2, w1*x2 + x1*w2 + y1*z2 - z1*y2, w1*y2 - x1*z2 + y1*w2 + z1*x2, w1*z2 + x1*y2 - y1*x2 + z1*w2)


def axis(ax, deg):
    h = math.radians(deg) / 2
    s = math.sin(h)
    return (math.cos(h), s if ax == 0 else 0, s if ax == 1 else 0, s if ax == 2 else 0)


def euler(x, y, z):            # Unity: Z, then X, then Y (q = qy * qx * qz)
    return qmul(qmul(axis(1, y), axis(0, x)), axis(2, z))


def rot(q, v):
    p = (0,) + tuple(v)
    w, x, y, z = q
    r = qmul(qmul(q, p), (w, -x, -y, -z))
    return r[1:]


def look(d):                   # LookRotation(d), up = Y
    yaw = math.degrees(math.atan2(d[0], d[2]))
    pitch = -math.degrees(math.atan2(d[1], math.hypot(d[0], d[2])))
    return euler(pitch, yaw, 0)


def towards(cur, tgt, maxrad):
    n = lambda v: tuple(c / math.sqrt(sum(k * k for k in v)) for c in v)
    a, b = n(cur), n(tgt)
    ang = math.acos(max(-1, min(1, sum(i * j for i, j in zip(a, b)))))
    if ang <= maxrad:
        return b
    t = maxrad / ang                          # slerp a -> b by maxrad
    s = math.sin(ang)
    return tuple((math.sin((1 - t) * ang) * i + math.sin(t * ang) * j) / s for i, j in zip(a, b))


fire = (0.0, 1.0, 1.0)
aim = (0.0, H, D)
fdir = tuple(a - f for a, f in zip(aim, fire))
base = look(fdir)
for i in range(7):
    a = -72 + 24 * i
    q = qmul(base, euler(-0.2 * abs(a), a, 0))
    fwd = rot(q, (0, 0, 1))
    p, t, nxt, dt = list(fire), 0.0, 0.0, 0.02
    while t < 3.0:
        t += dt
        if nxt < t:
            nxt = t + 0.1
            fwd = towards(fwd, tuple(a_ - p_ for a_, p_ in zip(aim, p)), 0.15)
        p = [pc + 12 * fc * dt for pc, fc in zip(p, fwd)]
        if p[1] <= 0.3:
            break
    print(f"missile yaw {a:+4d}: ground at {t:.2f} s after the fire, at x {p[0]:+.2f} z {p[2]:.2f} "
          f"({math.hypot(p[0], p[2] - D):.2f} m from the aim)" if p[1] <= 0.3 else f"missile yaw {a:+4d}: no ground in 3 s, at {p}")


def to_euler(q):               # Unity's eulerAngles (Z, X, Y order): q = qy * qx * qz
    w, x, y, z = q
    sx = 2 * (w * x - y * z)
    ex = math.degrees(math.asin(max(-1, min(1, sx))))
    ey = math.degrees(math.atan2(2 * (w * y + x * z), 1 - 2 * (x * x + y * y)))
    ez = math.degrees(math.atan2(2 * (w * z + x * y), 1 - 2 * (x * x + z * z)))
    return round(ex, 2), round(ey, 2), round(ez, 2)


print("spawn rotation of each missile, as a cue rot (Unity Euler after the hero's facing):")
for i in range(7):
    a = -72 + 24 * i
    q = qmul(base, euler(-0.2 * abs(a), a, 0))
    e = to_euler(q)
    assert all(abs(u - v) < 1e-3 for u, v in zip(rot(euler(*e), (0, 0, 1)), rot(q, (0, 0, 1))))   # round trip
    print(f"  yaw {a:+4d}: rot {list(e)}")
