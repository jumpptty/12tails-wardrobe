"""Read only: per TTO MoveNext (name regex argv[2]) in pseudo/Penguin.c (argv[1]): header RVA, String literals, float-ish
constants. py -3 -I tto_strings.py <Penguin.c> "lightBind_cast|seal>"""
import re, sys
L = open(sys.argv[1], encoding="utf-8", errors="replace").read().split("\n")
pat = re.compile(sys.argv[2])
hdr = re.compile(r"^// ==== ((?:Penguin|Penguin_w+).<(\w+)>d__\d+)::MoveNext .*RVA (0x[0-9a-f]+)")
i = 0
while i < len(L):
    m = hdr.match(L[i])
    if m and pat.search(m.group(2)):
        j = i + 1
        while j < len(L) and not L[j].startswith("// ===="):
            j += 1
        body = L[i:j]
        strs = []
        for s in body:
            for x in re.findall(r"String:'([^']*)'", s):
                if x not in strs: strs.append(x)
        fl = sorted(set(re.findall(r"\b(0x3[ef][0-9a-f]{6})\b", "\n".join(body))))
        print(f"{m.group(1)}::MoveNext@{m.group(3)} lines {i+1}-{j}")
        print("   strings:", strs)
        print("   float bits:", fl)
        i = j
    else:
        i += 1
