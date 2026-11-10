"""Read only: re-derive Mana Missile's spawn rots (cast_a.md) with Unity's conventions, independent of missile_sim.py.
q = LookRotation(fire point (0,1,1) -> ground point (0,0,10)) * Euler(-0.2|yaw|, yaw, 0) (Penguin.cs:10220)."""
import math

def mat_x(a):
    c, s = math.cos(a), math.sin(a); return [[1, 0, 0], [0, c, -s], [0, s, c]]
def mat_y(a):
    c, s = math.cos(a), math.sin(a); return [[c, 0, s], [0, 1, 0], [-s, 0, c]]
def mat_z(a):
    c, s = math.cos(a), math.sin(a); return [[c, -s, 0], [s, c, 0], [0, 0, 1]]
def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def euler(x, y, z):  # Unity: Ry * Rx * Rz (degrees)
    r = math.radians
    return mul(mul(mat_y(r(y)), mat_x(r(x))), mat_z(r(z)))
def to_euler(m):  # inverse of Ry*Rx*Rz
    x = math.degrees(math.asin(-m[1][2]))
    y = math.degrees(math.atan2(m[0][2], m[2][2]))
    z = math.degrees(math.atan2(m[1][0], m[1][1]))
    return [round(x, 2), round(y, 2), round(z, 2)]

pitch = math.degrees(math.atan2(1, 9))      # down = +x in Unity
look = euler(pitch, 0, 0)
out = []
for i in range(7):
    yaw = -72 + 24 * i
    out.append(to_euler(mul(look, euler(-0.2 * abs(yaw), yaw, 0))))
print(round(pitch, 2), out)
assert out[3] == [6.34, 0.0, 0.0]
