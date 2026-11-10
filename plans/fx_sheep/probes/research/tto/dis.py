"""Disassemble TTO's GameAssembly.dll from RVA a to RVA b (capstone).
uv run --no-project --with capstone python -I dis.py <GameAssembly.dll> 0x1e74080 0x1e740c0"""
import struct, sys, capstone
dll, a, b = sys.argv[1], int(sys.argv[2], 16), int(sys.argv[3], 16)
B = open(dll, 'rb').read()
pe = struct.unpack_from('<I', B, 0x3c)[0]; n = struct.unpack_from('<H', B, pe + 6)[0]; o = struct.unpack_from('<H', B, pe + 20)[0]
for i in range(n):
    name, vs, va, rs, raw = struct.unpack_from('<8sIIII', B, pe + 24 + o + 40 * i)
    if va <= a < va + vs: break
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
for ins in md.disasm(B[raw + a - va: raw + b - va], a):
    print(hex(ins.address), ins.mnemonic, ins.op_str)
