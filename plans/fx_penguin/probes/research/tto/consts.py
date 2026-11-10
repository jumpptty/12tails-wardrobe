"""Annotate a capstone listing with the float32 at each rip-relative operand. py -3 -I consts.py <GameAssembly.dll> <listing>"""
import re, struct, sys
dll, lst = sys.argv[1:]
B = open(dll, 'rb').read()
pe = struct.unpack_from('<I', B, 0x3c)[0]; n = struct.unpack_from('<H', B, pe + 6)[0]; o = struct.unpack_from('<H', B, pe + 20)[0]
secs = [struct.unpack_from('<8sIIII', B, pe + 24 + o + 40 * i) for i in range(n)]
def rd(rva):
    for nm, vs, va, rs, raw in secs:
        if va <= rva < va + max(vs, rs): return B[raw + rva - va: raw + rva - va + 4]
lines = open(lst).read().splitlines()
for k, l in enumerate(lines):
    m = re.search(r'\[rip ([+-]) (0x[0-9a-f]+)\]', l)
    if m:
        nxt = int(lines[k + 1].split()[0], 16) if k + 1 < len(lines) else None
        if nxt:
            t = nxt + (int(m.group(2), 16) * (1 if m.group(1) == '+' else -1)); b = rd(t)
            if b: l += f'   ; [{hex(t)}] f32={struct.unpack("<f", b)[0]:.7g} i32={struct.unpack("<i", b)[0]}'
    print(l)
