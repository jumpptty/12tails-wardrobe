"""Penguin parts numbers (read only). py -3 -I checks/fx_penguin_research/parts/calc.py
Unity 3.5 PhysX: 50 FixedUpdates/s; linear drag as v *= (1 - drag*dt) each step (assumed; the exp form gives the same to 4 %).
"""
import math
DT, DRAG = 0.02, 2.0
# tornado: Init v = 5 x owner.forward (Penguin_tornado.cs:98), drag 2 (:103), no input -> no force
v, x = 5.0, 0.0
for k in range(int(3 / DT)):
    v *= 1 - DRAG * DT; x += v * DT
    if k in (19, 49, 99, 149): print(f"tornado t={(k+1)*DT:.2f}s x={x:.3f} m v={v:.3f}")
print(f"tornado limit {5 * (1 - DRAG*DT) / DRAG:.3f} m")
# typhoon: start 4 m ahead (Penguin.cs:33353, sLv 3), v0 = rotateH(5 fwd, (tID-1)*120) (Penguin_typhoon.cs:848),
# drag 2 (:853), AddForce((11 - mLv) * flat dir to target) every step, mass 1 (:372), target 10 m ahead
for th in (0, 120, 240):
    a = math.radians(th)
    px, pz = 0.0, 4.0
    vx, vz = -5 * math.sin(a), 5 * math.cos(a)          # Math.rotateH: x' = x cos - z sin, z' = z cos + x sin (Math.cs:840-841)
    first = None; mind = 99
    for k in range(int(6 / DT)):
        dx, dz = 0 - px, 10 - pz; d = math.hypot(dx, dz)
        if d > 1e-6: vx += 8 * dx / d * DT; vz += 8 * dz / d * DT
        vx *= 1 - DRAG * DT; vz *= 1 - DRAG * DT
        px += vx * DT; pz += vz * DT
        d = math.hypot(px, pz - 10); mind = min(mind, d)
        if first is None and d <= 3: first = (k + 1) * DT
    print(f"typhoon theta {th}: within 3 m of the target at {first:.2f} s, at 6 s ({px:.2f}, {pz:.2f}), closest {mind:.2f} m")
print("terminal speed", round(8 * DT * (1 - DRAG*DT) / (DRAG*DT), 3), "m/s")
# chaAdjust(6) at CHA 1, LCK 1 (CharacterControl.cs:20593-): num = clamp(1 + Range(0, ceil(0.2)) , 1, 512) = 1
print("chaAdjust(6) =", math.ceil(int(6 * (1 + 0.015 * 1))), "-> iceBlock life", math.ceil(int(6 * 1.015)) + 6, "s, typhoon life", math.ceil(int(6 * 1.015)), "s")
print("arcticEmperor phases", 0, 0 + 0.3, 0.3 + 7.7, 0.3 + 7.7 + 1.0)
print("nAttack ball: 14 m/s x 1.4 s =", 14 * 1.4, "m; manaMissile 12 m/s x 3 s =", 36, "m")
