"""Re-derives the numbers in plans/fx_sheep/tto.md and parts.md (verification 2026-11-10). Reads nothing but the
repo's plans/fx_inventory.json and pipeline/wardrobe_fx_inventory.py; asserts every value the reports print.
py -3 -I checks/fx_sheep_research/verify/tto_parts_numbers.py   (run from the repo root)"""
import ast, collections, json, math, re

r = lambda x, n=3: round(x, n)
# tto.md 2.1: mouth (0.347 fwd, 1.209 up) from Head (0.127, 1.249) + 0.22 fwd - 0.04 up; ally chest 10 m ahead, 0.8 up
mouth = (0.127 + 0.22, 1.249 - 0.04)
d = math.hypot(10 - mouth[0], 0.8 - mouth[1])
flight = min(0.6, max(0.15, d * 0.0625))           # BreathFly: clamp(d x 0.0625, 0.15, 0.6)
assert r(d, 2) == 9.66 and flight == 0.6 and r(0.62 + flight, 2) == 1.22
assert 3 * 0.0625 == 0.1875 and r(0.62 + 0.1875 + 0.3, 2) == 1.11 and r(0.1875 + 0.3, 2) == 0.49
assert r(0.25 * 0.9, 3) == 0.225                    # the wisp's arc u x 0.9 x (1 - u) at u = 0.5
# tto.md 2.2: beam hand (0.486 fwd, 1.115 up) -> her chest (0, 0.8); ally variant -> (10, 0.8)
assert r(math.degrees(math.atan2(1.115 - 0.8, 0.486)), 0) == 33
assert r(math.degrees(math.atan2(0.32, 9.51)), 1) == 1.9
assert min(3, max(1, 1.5 + 0.2)) == 1.7             # BB reverse scale clamp(height + 0.2, 1, 3)
# tto.md 2.3: book heights at the reads (CodexBob: 0.12 sin(2.2 tau), the drop term 0 after 0.6 s)
h = [r(2.6 + 0.12 * math.sin(2.2 * 2 * (k + 1))) for k in range(10)]
assert h == [2.486, 2.67, 2.671, 2.486, 2.599, 2.715, 2.531, 2.528, 2.714, 2.602], h
assert [r(0.7 + 2 * (k + 1), 1) for k in (0, 9)] == [2.7, 20.7] and r(20.7 + 0.1 - 0.7, 1) == 20.1
assert r(math.degrees(-0.6108652), 1) == -35.0      # the Euler literal 0xBF1C61AA
# parts.md: the normal-attack ball, firePos (0.3 fwd, 1 up) -> ground 10 m ahead, 12 m/s; sphere radius 0.3
assert r(math.degrees(math.atan(1 / 9.7)), 2) == 5.89
L = math.hypot(9.7, 1); assert r(L, 2) == 9.75 and r(L / 12, 2) == 0.81 and r(0.7 * L / 12, 2) == 0.57
assert r(1.7 * 12, 1) == 20.4 and 5 * 8 == 40 and r(0.05 * 12, 1) == 0.6
# parts.md: charge ball, held 4.8 s (SEQ "cAttack1@0.8 cAttack0*~@4"), RPC_cAttack 0.5 s after the release:
# n = floor(Time - actionTime - 1.3) (Sheep.cs:9807) = floor(5.3 - 1.3) = 4; cap 100 x 4 = 400; size + 0.004 x 400
assert math.floor(4.8 + 0.5 - 1.3) == 4 and min(2.5, 0.004 * 400) == 1.6
# parts.md: AlphaTimer phase sums
for parts, total in (((0, 1, 99, 0), 100), ((0, .5, 9.2, .3), 10), ((0, 1, 11, 1), 13), ((0, .2, 2, .2), 2.4),
                     ((0, 0, .5, .2), .7), ((.3, .4, .6, .2), 1.5)):
    assert r(sum(parts), 3) == total
# parts.md: AlphaTimer-blocked effects in the other classes, from the inventory and its BUILT set
src = open("pipeline/wardrobe_fx_inventory.py", encoding="utf-8").read()
BUILT = ast.literal_eval(re.search(r"BUILT = (\{.*?\})\n", src, re.S).group(1))
inv = json.load(open("plans/fx_inventory.json", encoding="utf-8"))
alone, need = collections.Counter(), collections.Counter()
for cls, v in inv.items():
    for e in v["own"].values():
        miss = set(e["parts"]) - BUILT
        if "AlphaTimer" in miss and cls != "sheep":
            need[cls] += 1; alone[cls] += miss == {"AlphaTimer"}
assert sum(alone.values()) == 34 and sum(need.values()) == 40, (alone, need)
own = inv["sheep"]["own"]
assert (sum(not set(e["parts"]) - BUILT for e in own.values()), len(own)) == (38, 51)
print("all numbers in tto.md and parts.md re-derived OK")
