"""Read float constants from TTO1102's GameAssembly.dll by VA (read only). usage: consts.py 0x182f39b94 ..."""
import struct, sys, pefile
pe = pefile.PE(r"C:\Users\Jump\Desktop\12tails\DecompiledSource_TTO_2026-11-02\client\GameAssembly.dll", fast_load=True)
base = pe.OPTIONAL_HEADER.ImageBase
for a in sys.argv[1:]:
    rva = int(a, 16) - base
    b = pe.get_data(rva, 8)
    print(a, struct.unpack("<f", b[:4])[0], struct.unpack("<d", b)[0])
