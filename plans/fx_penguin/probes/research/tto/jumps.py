"""Find jumps/branches (jcc/jmp rel32 or rel8) to given RVAs inside a function range of TTO's GameAssembly.dll.
uv run --no-project --with capstone python -I jumps.py <dll> <from> <to> <target> [target...]"""
import struct, sys, capstone
dll, a, b, *ts = sys.argv[1:]
a, b = int(a, 16), int(b, 16); ts = {int(t, 16) for t in ts}
B = open(dll, 'rb').read()
pe = struct.unpack_from('<I', B, 0x3c)[0]; n = struct.unpack_from('<H', B, pe + 6)[0]; o = struct.unpack_from('<H', B, pe + 20)[0]
for i in range(n):
    name, vs, va, rs, raw = struct.unpack_from('<8sIIII', B, pe + 24 + o + 40 * i)
    if va <= a < va + vs: break
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
for ins in md.disasm(B[raw + a - va: raw + b - va], a):
    if ins.mnemonic.startswith('j') and ins.op_str.startswith('0x') and int(ins.op_str, 16) in ts:
        print(hex(ins.address), ins.mnemonic, ins.op_str)
