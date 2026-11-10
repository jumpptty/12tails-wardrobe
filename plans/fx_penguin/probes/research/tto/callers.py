"""Find direct E8 call sites to given RVAs in TTO's GameAssembly.dll, and name the function each lies in (methods.tsv).
py -3 -I callers.py <GameAssembly.dll> <methods.tsv> 0x24ae620 [0x...]"""
import bisect, struct, sys
dll, tsv, *targets = sys.argv[1:]
B = open(dll, 'rb').read()
pe = struct.unpack_from('<I', B, 0x3c)[0]
nsec = struct.unpack_from('<H', B, pe + 6)[0]; opt = struct.unpack_from('<H', B, pe + 20)[0]
secs = [struct.unpack_from('<8sIIII', B, pe + 24 + opt + 40 * i) for i in range(nsec)]
text = next(s for s in secs if s[0].rstrip(b'\0') == b'il2cpp')
_, vsize, va, rsize, raw = text
rows = []
for line in open(tsv, encoding='utf-8', errors='replace'):
    p = line.rstrip('\n').split('\t')
    for x in p:
        if x.startswith('0x'):
            try: rows.append((int(x, 16), '\t'.join(p))); break
            except ValueError: pass
rows.sort(); keys = [r[0] for r in rows]
for t in targets:
    t = int(t, 16); hits = []
    i = B.find(b'\xe8', raw)
    end = raw + rsize
    while 0 <= i < end - 5:
        rva = va + (i - raw)
        if rva + 5 + struct.unpack_from('<i', B, i + 1)[0] == t:
            k = bisect.bisect_right(keys, rva) - 1
            hits.append((hex(rva), rows[k][1][:160] if k >= 0 else '?'))
        i = B.find(b'\xe8', i + 1)
    print(hex(t), len(hits)); [print('  ', h) for h in hits]
