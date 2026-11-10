"""Read-only: where the Penguin's normal-attack ball's trigger (SphereCollider m_Radius 0.35, nAttack_fire.prefab /
spreadShot_fire.prefab line 82; no gravity, m_UseGravity 0 :94) first touches flat ground at y = 0, i.e. when its centre
is 0.35 m up, for the report's aim (the ground 10 m ahead) and the game's no-target aim (0.25 m lower)."""
import math
R, H, Z0, V = 0.35, 0.75, 0.5, 14.0
for name, ty in (("aim at the 10 m ground point", 0.0), ("no-target click (-0.25)", -0.25)):
    d = (0.0, ty - H, 10.0 - Z0); n = math.hypot(*d); dy = d[1] / n
    s = (H - R) / -dy
    print(f"{name}: centre-to-ground {H / -dy:.4f} m / {H / -dy / V:.4f} s;"
          f" trigger at {s:.4f} m / {s / V:.4f} s, z {Z0 + s * d[2] / n:.3f}")
# side pellets: direction from geom.txt, dir (+-0.2588, -0.076, 0.9629)
dx, dy, dz = 0.2588, -0.0760, 0.9629; n = math.sqrt(dx*dx + dy*dy + dz*dz); dx, dy, dz = dx/n, dy/n, dz/n
s = (H - R) / -dy
print(f"side pellet: trigger at {s:.4f} m / {s / V:.4f} s, x {0.3 + s * dx:.3f}, z {Z0 + s * dz:.3f}")
