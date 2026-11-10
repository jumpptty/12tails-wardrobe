"""Compare the float constants (rip-relative loads, in order) and call counts of Penguin methods between TTO 1102 and 1109.
uv run --no-project --with capstone python -I cmp1109.py <TTO root folder 1102> <TTO root folder 1109>"""
import re, struct, sys, bisect, capstone
want = ['<RPC_constellation>d__340\tMoveNext', '<StarLines>d__341\tMoveNext', '<RPC_frostFieldLeap>d__349\tMoveNext',
        '<FrostFieldLoop>d__350\tMoveNext', '<RPC_emperorPenguin>d__356\tMoveNext', '<EmperorShot>d__358\tMoveNext',
        '<FlockRise>d__357\tMoveNext', 'Penguin\tFlockSpot', 'Penguin\tRow6Beak', 'Penguin\tRow6Foot', 'Penguin\tGoalFx',
        'Penguin\tScatter', 'Penguin\tStarImpact', 'Penguin\tRow6Begin', 'Penguin\tFieldLanding', 'Penguin\tDoRow6Skill']
def load(root):
    B = open(root + '/client/GameAssembly.dll', 'rb').read()
    pe = struct.unpack_from('<I', B, 0x3c)[0]; n = struct.unpack_from('<H', B, pe + 6)[0]; o = struct.unpack_from('<H', B, pe + 20)[0]
    secs = [struct.unpack_from('<8sIIII', B, pe + 24 + o + 40 * i) for i in range(n)]
    rows = []
    for l in open(root + '/methods.tsv', encoding='utf-8', errors='replace'):
        p = l.rstrip('\n').split('\t')
        if p[0].startswith('0x'): rows.append((int(p[0], 16), '\t'.join(p[1:3])))
    starts = sorted({r[0] for r in rows})
    return B, secs, rows, starts
def rd(B, secs, rva, k=4):
    for nm, vs, va, rs, raw in secs:
        if va <= rva < va + max(vs, rs): return B[raw + rva - va: raw + rva - va + k]
def sig(root):
    B, secs, rows, starts = load(root); md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64); out = {}
    for w in want:
        rva = next(r[0] for r in rows if r[1].endswith(w) or r[1] == w)
        end = starts[bisect.bisect_right(starts, rva)]
        code = rd(B, secs, rva, end - rva); fl = []; calls = 0
        for ins in md.disasm(code, rva):
            if ins.mnemonic == 'call': calls += 1
            m = re.search(r'\[rip ([+-]) (0x[0-9a-f]+)\]', ins.op_str)
            if m and ('ss' in ins.mnemonic or 'xmm' in ins.op_str):
                t = ins.address + ins.size + int(m.group(2), 16) * (1 if m.group(1) == '+' else -1)
                b = rd(B, secs, t)
                if b: fl.append(round(struct.unpack('<f', b)[0], 6))
        out[w] = (end - rva, calls, fl)
    return out
a, b = sig(sys.argv[1]), sig(sys.argv[2])
for w in want:
    same = a[w][2] == b[w][2] and a[w][1] == b[w][1]
    print(w.replace('\t', '::'), 'size', a[w][0], b[w][0], 'calls', a[w][1], b[w][1], 'SAME floats+calls' if same else 'DIFF')
    if not same: print('   1102', a[w][2]); print('   1109', b[w][2])
