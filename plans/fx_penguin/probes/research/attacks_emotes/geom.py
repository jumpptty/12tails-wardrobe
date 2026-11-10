"""The Penguin's normal-attack ball geometry, target point 10 m ahead on the ground (decision 3 analogue).
firePos = (0, 0.75, 0.5) local (Penguin.cs:17238), fireDir = tDir - (0, 0.75, 0.5) (:17243), 14 m/s (Penguin_nAttack.cs:103).
Spread Shot: pellet i in -1..1 at firePos + 0.3 i right, rotation lhs * Euler(0, 15 i, 0) (Penguin.cs:11496-11520).
Unity: Euler(x, y, z) = Qy * Qx * Qz; +x pitches the forward axis down."""
import math

def qmul(a, b):
    w1, x1, y1, z1 = a; w2, x2, y2, z2 = b
    return (w1*w2 - x1*x2 - y1*y2 - z1*z2, w1*x2 + x1*w2 + y1*z2 - z1*y2, w1*y2 - x1*z2 + y1*w2 + z1*x2, w1*z2 + x1*y2 - y1*x2 + z1*w2)
def qax(axis, deg):
    h = math.radians(deg) / 2; s = math.sin(h)
    return (math.cos(h), axis[0]*s, axis[1]*s, axis[2]*s)
def rot(q, v):
    w, x, y, z = q; p = (0, *v); qc = (w, -x, -y, -z)
    return qmul(qmul(q, p), qc)[1:]
def unity_euler(q):
    w, x, y, z = q
    sx = 2 * (w*x - y*z)                       # Unity ZXY: x = asin(-m12)
    ex = math.degrees(math.asin(max(-1, min(1, sx))))
    ey = math.degrees(math.atan2(2 * (w*y + x*z), 1 - 2 * (x*x + y*y)))
    ez = math.degrees(math.atan2(2 * (w*z + x*y), 1 - 2 * (x*x + z*z)))
    return ex, ey, ez

H, Z0, SPEED = 0.75, 0.5, 14.0
fire_dir = (0.0, 0.0 - H, 10.0 - Z0)
theta = math.degrees(math.atan2(H, 10.0 - Z0))
print(f"pitch {theta:.4f} deg")
lhs = qax((1, 0, 0), theta)
for i in (-1, 0, 1):
    q = qmul(lhs, qax((0, 1, 0), 15 * i))
    d = rot(q, (0, 0, 1))
    start = (0.3 * i, H, Z0)
    s = H / -d[1]                              # path length to y = 0
    land = tuple(start[k] + s * d[k] for k in range(3))
    print(f"i={i:+d} euler {tuple(round(e, 3) for e in unity_euler(q))} dir {tuple(round(c, 4) for c in d)} path {s:.4f} m, {s / SPEED:.4f} s, lands {tuple(round(c, 3) for c in land)}")
# the game's own no-target click: a = pos + 10 forward (GameGui.cs:1659), vector -= 0.25 up (Penguin.cs:9306)
d2 = (0.0, -0.25 - H, 10.0 - Z0); s2 = H / -d2[1] * math.hypot(d2[1], d2[2])
print(f"no-target click: pitch {math.degrees(math.atan2(-d2[1], d2[2])):.3f} deg, lands z {Z0 + H / -d2[1] * d2[2]:.3f}, {s2:.4f} m, {s2 / SPEED:.4f} s")
for shot, base in (("stage1", 0.3), ("stage2", 0.5 + 0.3), ("stage3", 1.0 + 0.3)):
    print(shot, "shot at", round(base, 4), "s after stage 1; centre lands", round(base + 9.529428 / SPEED, 4), "side", round(base + 9.865761 / SPEED, 4))
