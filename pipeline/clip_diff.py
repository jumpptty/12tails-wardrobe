r"""Where a wardrobe clip differs from BB's (2026-11-09; user: "can you prove that TTO edited Whale talk animation?"). The
publish only says "keys differ from BB's <clip>.anim"; this lists every bone and channel (q rotation, p position, s
scale) whose keys differ: key counts, key times, and the largest value difference, in the same rows the publish compares
(wardrobe_publish.hero_rows: BB's keys turned into the wardrobe's mirrored space).
  py -3 pipeline\clip_diff.py whale talk
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wardrobe_publish as wp  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def main(cls, name):
    sys.stdout.reconfigure(encoding="utf-8")
    mine = json.loads((ROOT / "wardrobe" / "data" / cls / "clips.json").read_text(encoding="utf-8"))[name]["tracks"]
    bb_rip = wp.BBRip(wp.BB_RIP)
    paths = bb_rip.class_clips(cls).get(name, [])
    if not paths:
        print(f"BB has no {cls} clip named {name}")
        return 1
    for path in paths:
        bb = {}
        for field, curve_path, keys in wp.read_clip(path)[1]:
            if keys:
                slot = wp.CURVE_SLOTS[field][0]
                bb.setdefault(curve_path.rsplit("/", 1)[-1], {})[slot] = wp.hero_rows(keys, slot)
        print(f"== {cls} {name} against BB's {path.name}")
        same, diffs = 0, []
        for bone in sorted(set(bb) | set(mine)):
            for slot in sorted(set(bb.get(bone, {})) | set(mine.get(bone, {}))):
                a, b = bb.get(bone, {}).get(slot), mine.get(bone, {}).get(slot)
                if a == b:
                    same += 1
                    continue
                if a is None or b is None:
                    diffs.append(f"{bone}.{slot}: only in {'the wardrobe' if a is None else 'BB'} ({len(a or b)} keys)")
                    continue
                ta, tb = [r[0] for r in a], [r[0] for r in b]
                if len(a) != len(b) or ta != tb:
                    diffs.append(f"{bone}.{slot}: BB {len(a)} keys at {fmt(ta)}, the wardrobe {len(b)} at {fmt(tb)}")
                    diffs[-1] += "\n      played back (Unity's Hermite curves, 600 samples): " + motion_gap(a, b, slot)
                    continue
                d = max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb) if abs(x) < 1e29 and abs(y) < 1e29)
                k = max(range(len(a)), key=lambda i: max((abs(x - y) for x, y in zip(a[i], b[i]) if abs(x) < 1e29 and abs(y) < 1e29), default=0))
                diffs.append(f"{bone}.{slot}: same {len(a)} key times, values differ by up to {d:.4g} (key {k} at t={ta[k]:g}: "
                             f"BB {fmt(a[k][1:5])}, the wardrobe {fmt(b[k][1:5])})")
        print(f"{same} channels identical, {len(diffs)} differ")
        for line in diffs:
            print("  " + line)
    return 0


def sample(rows, t):
    """A channel's value at time t: Unity's Hermite curve between keys (an infinite slope = a step), held past the ends."""
    n = (len(rows[0]) - 1) // 3
    if t <= rows[0][0]:
        return rows[0][1:1 + n]
    for r0, r1 in zip(rows, rows[1:]):
        if t <= r1[0]:
            dt = r1[0] - r0[0]
            if dt <= 0:
                return r1[1:1 + n]
            s = (t - r0[0]) / dt
            h00, h10, h01, h11 = 2 * s ** 3 - 3 * s ** 2 + 1, s ** 3 - 2 * s ** 2 + s, -2 * s ** 3 + 3 * s ** 2, s ** 3 - s ** 2
            out = []
            for c in range(n):
                p0, p1, m0, m1 = r0[1 + c], r1[1 + c], r0[1 + 2 * n + c], r1[1 + n + c]
                if abs(m0) > 1e29 or abs(m1) > 1e29:
                    out.append(p0)
                else:
                    out.append(h00 * p0 + h10 * dt * m0 + h01 * p1 + h11 * dt * m1)
            return out
    return rows[-1][1:1 + n]


def motion_gap(a, b, slot):
    """How far apart the two channels play: the largest gap over the clip (degrees for a rotation) and when."""
    import math
    end = max(a[-1][0], b[-1][0])
    worst, at = 0.0, 0.0
    for i in range(601):
        t = end * i / 600
        x, y = sample(a, t), sample(b, t)
        if slot == "q":
            nx, ny = math.sqrt(sum(v * v for v in x)) or 1, math.sqrt(sum(v * v for v in y)) or 1
            dot = min(1.0, abs(sum(u * v for u, v in zip(x, y))) / (nx * ny))
            gap = math.degrees(2 * math.acos(dot))
        else:
            gap = max(abs(u - v) for u, v in zip(x, y))
        if gap > worst:
            worst, at = gap, t
    return f"largest gap {worst:.3g}{' deg' if slot == 'q' else ''} at t={at:.3f} s of {end:.3f} s"


def fmt(xs):
    xs = list(xs)
    return "[" + ", ".join(f"{x:.4g}" for x in xs[:8]) + (", ..." if len(xs) > 8 else "") + "]"


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
