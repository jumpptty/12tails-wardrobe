"""List the named call targets of one method in TTO 1102 and 1109 and diff them (the extra-call check).
uv run --no-project --with capstone python -I calls1109.py <root1102> <root1109> "<RPC_emperorPenguin>d__356\tMoveNext" """
import struct, sys, bisect, capstone, difflib
def names(root, w):
    B = open(root + '/client/GameAssembly.dll', 'rb').read()
    pe = struct.unpack_from('<I', B, 0x3c)[0]; n = struct.unpack_from('<H', B, pe + 6)[0]; o = struct.unpack_from('<H', B, pe + 20)[0]
    secs = [struct.unpack_from('<8sIIII', B, pe + 24 + o + 40 * i) for i in range(n)]
    rows = {}
    for l in open(root + '/methods.tsv', encoding='utf-8', errors='replace'):
        p = l.rstrip('\n').split('\t')
        if p[0].startswith('0x'): rows.setdefault(int(p[0], 16), p[1] + '::' + p[2])
    st = sorted(rows); rva = next(k for k, v in rows.items() if v.endswith(w.replace('\t', '::')))
    end = st[bisect.bisect_right(st, rva)]
    for nm, vs, va, rs, raw in secs:
        if va <= rva < va + vs: break
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64); out = []
    for ins in md.disasm(B[raw + rva - va: raw + end - va], rva):
        if ins.mnemonic == 'call':
            try: t = int(ins.op_str, 16); out.append(rows.get(t, hex(t)) if t in rows else '?')
            except ValueError: out.append('indirect')
    return out
a, b = names(sys.argv[1], sys.argv[3]), names(sys.argv[2], sys.argv[3])
for l in difflib.unified_diff(a, b, lineterm='', n=2): print(l)
