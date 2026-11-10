"""A Penguin bone in the rig's own space (z up), rest pose and at a clip time (from checks/fx_sheep_research/tto/head.py; linear between keys, about +-5 cm). Row6Beak = Head + 0.16 forward - 0.03 up (TTO1102:Penguin::Row6Beak@0x1DAF620), Row6Foot = Foot2_R (Row6Foot@0x1DB0160).

py -3 -I bones.py <wardrobe/data/penguin> <clip> <t> <bone,bone>"""
import json, sys, os
d, clip, t = sys.argv[1], sys.argv[2], float(sys.argv[3])
rig = json.load(open(os.path.join(d, 'rig.json'), encoding='utf-8'))['bones']
tr = json.load(open(os.path.join(d, 'clips.json'), encoding='utf-8'))[clip]['tracks']
def qmul(a, b):
    ax, ay, az, aw = a; bx, by, bz, bw = b
    return [aw*bx+ax*bw+ay*bz-az*by, aw*by-ax*bz+ay*bw+az*bx, aw*bz+ax*by-ay*bx+az*bw, aw*bw-ax*bx-ay*by-az*bz]
def rot(q, v):
    x, y, z, w = q; p = qmul(qmul(q, [*v, 0]), [-x, -y, -z, w]); return p[:3]
def sample(keys, n):
    if t <= keys[0][0]: return keys[0][1:1+n]
    for a, b in zip(keys, keys[1:]):
        if a[0] <= t <= b[0]:
            u = (t - a[0]) / (b[0] - a[0]) if b[0] > a[0] else 0
            return [a[1+i] + (b[1+i] - a[1+i]) * u for i in range(n)]
    return keys[-1][1:1+n]
def world(name, posed):
    i = next(k for k, b in enumerate(rig) if b['name'] == name); chain = []
    while i >= 0: chain.append(rig[i]); i = rig[i]['parent']
    P, Q = [0, 0, 0], [0, 0, 0, 1]
    for b in reversed(chain):
        p, q = b['p'], b['q']
        if posed and b['name'] in tr:
            if 'p' in tr[b['name']]: p = sample(tr[b['name']]['p'], 3)
            if 'q' in tr[b['name']]: q = sample(tr[b['name']]['q'], 4)
        P = [P[k] + rot(Q, p)[k] for k in range(3)]; Q = qmul(Q, q)
    return [round(x, 3) for x in P]
for n in sys.argv[4].split(','):
    try: print(n, 'rest', world(n, False), f'{clip}@{t}', world(n, True))
    except StopIteration: print(n, 'not in rig')
