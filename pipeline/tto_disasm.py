r"""Annotated disassembly of TTO methods (IL2CPP, x64), for reading game rules from a TTO decompile's GameAssembly.dll
(2026-11-18: the pet rules of 1.7.0, plans/wardrobe_pets_tto_rules.md). Capstone over the DLL, as wardrobe_icons.py
reads it; each instruction gets its call target's name (methods.tsv), its metadata usage (TypeInfo / MethodDef /
String literal / FieldInfo / MethodRef, through the decompile's tools/usages.py), and its constant when it loads one
from .rdata (float32 / float64 of the bytes at the rip-relative address, or an immediate that reads as a float).

  uv run --no-project --with pefile --with capstone python -I pipeline/tto_disasm.py [<target> ...]
      [--switch] [--slots <Class>] [--literals <regex>] [--callers <target>]
      [--dec <decompile folder>] [--tools <tools folder>] [--build <build.py>]
  target = an RVA (0x1adac10) or Class::Method as methods.tsv names it (PetControl::Init; every overload)
  --switch = also print the method's chain of string compares: each literal compared (String::Equals /
             op_Equality, then jne / je) -> the first other literal on its "equal" branch, and the calls before it
  --slots = a class's virtual slots: a virtual call reads [vtable + 0x138 + 16 x slot] (checked on 1.7.0:
            CharacterEquipment::EquipAll calls EquipWeapon, slot 5, at +0x188 and EquipPet, slot 17, at +0x248)
  --literals = every string literal of the metadata matching the regex (case-insensitive)
  --callers = every direct call / jmp (E8 / E9 rel32) to the method in the code, with the function holding it
              (virtual calls through the vtable are not found this way)
  A jump table (a C# switch on an int) is printed with its entries as RVAs; a leaf function with no .pdata
  entry is read up to its first ret / jmp.

The pet rules of 1.7.0 were read with (2026-11-18):
  ... tto_disasm.py --switch CharacterEquipment::EquipPet CharacterEquipment::GetPetSize
      CharacterEquipment::IsStaticLargePet PetScales::Multiplier PetScales::Family PetScales::PetScale
      PetScales::HeroScale PetScales::EnsureLoaded PetScales::BuildIndex
      Assets.Scripts.Utility.EquipmentUtility::MapPetCodeName 0x165d8b0 Stringf::getLastDigit
      PetControl::Init PetControl::LateUpdate PetControl::Start PetControl::ResolveClips PetControl::FindClip
      PetControl::SetAnimPrefixes PetControl::PlayIdle PetControl::PlayRun PetControl::.ctor PetData::getData
      SheepEquipment::get_CharacterType CharacterEquipment::EquipAll --slots CharacterEquipment --slots PetControl
  ... tto_disasm.py PetShopData::getUpgradeItem GameItemTable::Request MotherFlowerBugPet::.cctor
      --callers PetControl::SetAnimPrefixes --callers CharacterEquipment::GetPetSize --callers PetControl::PlayIdle
      --literals "rabby|tianlong|violeta|koalia|selene|dragonz|dryad|valkornoct|cute ?cat|piggy|shark"

--dec defaults to the 2026-11-18 decompile on either PC (D:\12tails or C:\Users\Jump\Desktop\12tails). Its build
constants (tools/build.py) are needed to read the metadata; a decompile folder without tools/ (the home PC's 11-18)
gets them from find_constants.py (--tools, default the newest decompile that has one) run on <dec>/client into the
temp folder once (about 10 s), keyed by the DLL's hash; --build names one instead.
"""
import argparse
import hashlib
import os
import re
import struct
import subprocess
import sys
import tempfile
import types

BIBLES = (r"D:\12tails", r"C:\Users\Jump\Desktop\12tails")


def pick_dec():
    for b in BIBLES:
        p = os.path.join(b, "DecompiledSource_TTO_2026-11-18")
        if os.path.isdir(p):
            return p
    sys.exit("no DecompiledSource_TTO_2026-11-18 found; pass --dec")


def pick_tools(dec):
    if os.path.isdir(os.path.join(dec, "tools")):
        return os.path.join(dec, "tools")
    root = os.path.dirname(dec)
    for name in sorted(os.listdir(root), reverse=True):
        p = os.path.join(root, name, "tools")
        if name.startswith("DecompiledSource_TTO_") and os.path.isfile(os.path.join(p, "usages.py")):
            return p
    sys.exit("no decompile tools/ folder found; pass --tools")


def load_build(dec, tools, build):
    if build is None and os.path.isfile(os.path.join(dec, "tools", "build.py")):
        build = os.path.join(dec, "tools", "build.py")
    if build is None:
        dll = os.path.join(dec, "client", "GameAssembly.dll")
        sha = hashlib.sha256(open(dll, "rb").read()).hexdigest()
        build = os.path.join(tempfile.gettempdir(), f"tto_build_{sha[:16]}", "build.py")
        if not os.path.isfile(build):
            os.makedirs(os.path.dirname(build), exist_ok=True)
            subprocess.run([sys.executable, "-P", os.path.join(tools, "find_constants.py"), dll,
                            os.path.join(dec, "client", "global-metadata.dat"), "--write", build], check=True,
                           stdout=subprocess.DEVNULL)
    c = types.ModuleType("build")
    exec(compile(open(build, encoding="utf-8").read(), build, "exec"), c.__dict__)
    sha = hashlib.sha256(open(os.path.join(dec, "client", "GameAssembly.dll"), "rb").read()).hexdigest()
    if c.GAME_ASSEMBLY_SHA256 != sha:
        sys.exit(f"{build} is for another GameAssembly.dll")
    return c


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="*")
    ap.add_argument("--slots", action="append", help="print a class's virtual slots (full name, e.g. PetControl)")
    ap.add_argument("--literals", action="append", help="print the string literals matching a regex")
    ap.add_argument("--callers", action="append", help="print the direct call / jmp sites of a method (RVA or name)")
    ap.add_argument("--dec")
    ap.add_argument("--tools")
    ap.add_argument("--build")
    ap.add_argument("--switch", action="store_true")
    a = ap.parse_args(argv)
    dec = a.dec or pick_dec()
    tools = a.tools or pick_tools(dec)
    c = load_build(dec, tools, a.build)
    sys.modules["build"] = c
    sys.path.insert(0, tools)
    import capstone
    from capstone import x86_const as X
    from binary import Binary
    from usages import Usages
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    b = Binary(os.path.join(dec, "client", "GameAssembly.dll"))
    u = Usages(b, os.path.join(dec, "global-metadata.decrypted.dat"), c)
    names, by_name = {}, {}
    for line in open(os.path.join(dec, "methods.tsv"), encoding="utf-8").read().splitlines()[1:]:
        p = line.split("\t")
        if len(p) >= 3 and p[0].startswith("0x"):
            rva = int(p[0], 16)
            names.setdefault(rva, []).append(f"{p[1]}::{p[2]}")
            by_name.setdefault(f"{p[1]}::{p[2]}", []).append(rva)
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    FLT = ("ss", "ps")
    DBL = ("sd", "pd")

    def label(rva):
        n = names.get(rva)
        if not n:
            return None
        return n[0] + (f" (+{len(n) - 1} folded)" if len(n) > 1 else "")

    def note(x):
        out = []
        for op in x.operands:
            if op.type == X.X86_OP_MEM and op.mem.base == X.X86_REG_RIP:
                tgt = x.address + x.size + op.mem.disp
                r = u.resolve(tgt)
                if r:
                    out.append(r[1])
                else:
                    try:
                        off = b.off(tgt)
                    except Exception:
                        continue
                    m = x.mnemonic
                    if m.endswith(DBL) or m in ("movsd",):
                        out.append(f"={struct.unpack_from('<d', b.B, off)[0]:g}")
                    elif m.endswith(FLT) or m.startswith(("movss", "cvtss", "comiss", "ucomiss")):
                        v = struct.unpack_from('<4f', b.B, off) if m.endswith("ps") else struct.unpack_from('<f', b.B, off)
                        out.append("=" + ",".join(f"{f:g}" for f in v))
                    else:
                        out.append(f"[{tgt - b.IB:#x}]")
            elif op.type == X.X86_OP_IMM and x.mnemonic in ("call", "jmp") and (n := label(op.imm - b.IB)):
                out.append(n)
            elif op.type == X.X86_OP_IMM and x.mnemonic == "mov" and 0x3c000000 <= op.imm <= 0x47ffffff:
                out.append(f"float {struct.unpack('<f', struct.pack('<I', op.imm))[0]:g}?")
        return "  ; " + " | ".join(out) if out else ""

    if a.callers:   # direct call / jmp rel32 sites in the code sections, named by the function that holds them
        want = {b.IB + (int(t, 16) if t.startswith("0x") else by_name[t][0]): t for t in a.callers}
        for sec in b.pe.sections:
            if not sec.Characteristics & 0x20000000:   # IMAGE_SCN_MEM_EXECUTE
                continue
            data = sec.get_data()
            base = b.IB + sec.VirtualAddress
            for op in (0xE8, 0xE9):
                i = data.find(bytes([op]))
                while i != -1:
                    if i + 5 <= len(data):
                        tgt = base + i + 5 + struct.unpack_from("<i", data, i + 1)[0]
                        if tgt in want:
                            site = base + i
                            try:
                                fs, _ = b.func_range(site)
                                who = label(fs - b.IB) or f"{fs - b.IB:#x}"
                            except AssertionError:
                                who = "?"
                            print(f"  {'call' if op == 0xE8 else 'jmp '} {want[tgt]} from {site - b.IB:#x} in {who}")
                    i = data.find(bytes([op]), i + 1)
    for rx in a.literals or []:   # every string literal of the metadata matching the regex (case-insensitive)
        pat = re.compile(rx, re.I)
        print(f"== string literals matching {rx!r}")
        for i in range(len(u.lit_idx)):
            s = u.literal(i)
            if pat.search(s):
                print(f"  {i:6d}  {s!r}"[:300])
    for cls in a.slots or []:   # a virtual call is call [vtable + 0x138 + 16 x slot] (VirtualInvokeData pairs)
        m = u.m
        for td in range(m.n_td):
            try:
                t = m.typedef(td)
                if m.fullname(td) != cls:
                    continue
            except ValueError:   # a record past the readable ones
                break
            print(f"== slots of {cls} (typedef {td})")
            for i in range(t["methodStart"], t["methodStart"] + t["methodCount"]):
                f = struct.unpack_from("<IHHIIhIHHhH", m.d, m.at("methods", i))
                if f[9] >= 0:
                    print(f"  slot {f[9]:3d}  [vtable + {0x138 + 16 * f[9]:#x}]  {m.s(f[0])}")
            break
    for t in a.targets:
        rvas = [int(t, 16)] if t.startswith("0x") else by_name.get(t, [])
        if not rvas:
            print(f"== {t}: not in methods.tsv")
        for rva in rvas:
            try:
                s, e = b.func_range(b.IB + rva)
                print(f"== {label(rva) or t} @ {rva:#x}  [{s - b.IB:#x}, {e - b.IB:#x})")
                ins = list(md.disasm(bytes(b.B[b.off(s): b.off(s) + (e - s)]), s))
            except AssertionError:   # a leaf function has no .pdata entry: read it up to its first ret / tail jmp
                s = b.IB + rva
                ins = []
                for x in md.disasm(bytes(b.B[b.off(s): b.off(s) + 0x400]), s):
                    ins.append(x)
                    if x.mnemonic in ("ret", "jmp", "int3"):
                        break
                print(f"== {label(rva) or t} @ {rva:#x}  (leaf, no .pdata: read to its first ret / jmp)")
            bound = None
            for x in ins:   # jump / call targets as RVAs, like the listing's addresses
                ops = re.sub(r"0x18[0-9a-f]{7}\b", lambda m: f"{int(m.group(0), 16) - b.IB:#x}", x.op_str)
                extra = ""
                if x.mnemonic == "cmp" and len(x.operands) == 2 and x.operands[1].type == X.X86_OP_IMM:
                    bound = x.operands[1].imm
                # a C# switch's jump table: mov reg, dword [base + idx*4 + table], base = the image base (a lea of
                # rip minus its own address); the entries are RVAs, as many as the cmp before the ja allows
                m = x.operands[1] if x.mnemonic == "mov" and len(x.operands) == 2 else None
                if m is not None and m.type == X.X86_OP_MEM and m.mem.scale == 4 and m.mem.index and bound is not None \
                        and 0x1000 < m.mem.disp < 0x4000000 and 0 <= bound < 64:
                    rvas = struct.unpack_from(f"<{bound + 1}I", b.B, b.off(b.IB + m.mem.disp))
                    extra = "  ; jump table: " + ", ".join(f"{k}->{r:#x}" for k, r in enumerate(rvas))
                print(f"  {x.address - b.IB:#09x}  {x.mnemonic:8s} {ops}{note(x)}{extra}")
            if a.switch:
                for code, subject, path, via in switch(ins, u, b, X, names):
                    print(f"  switch {subject} == {code!r} -> {path!r}" + (f"  (after {', '.join(via)})" if via else ""))


def switch(ins, u, b, X, names):
    """A chain of string compares, read off the machine code (TTO1118's EquipPet is an if / else chain, not a hash
    switch): each literal loaded into rdx right before a call to System.String::Equals / op_Equality, then test al /
    jne (or je) -> the first literal loaded on its "equal" branch (jumps followed, stops at ret), and the calls met
    before it (Substring, MapPetCodeName ...: then the path is built, not that literal). subject = the register
    compared (rcx's source)."""
    at = {x.address: j for j, x in enumerate(ins)}
    lit = {}
    for j, x in enumerate(ins):
        for op in x.operands:
            if op.type == X.X86_OP_MEM and op.mem.base == X.X86_REG_RIP:
                tgt = x.address + x.size + op.mem.disp
                r = u.resolve(tgt)
                if r and r[0] == 5:
                    lit[j] = u.literal((b.q(tgt) & 0x1FFFFFFF) >> 1)

    def callee(x):
        if x.mnemonic == "call" and x.operands and x.operands[0].type == X.X86_OP_IMM:
            n = names.get(x.operands[0].imm - b.IB)
            return n[0] if n else None
        return None

    cmp = []   # (literal, index of its jne / je, subject register)
    for j, l in lit.items():
        if not ins[j].op_str.startswith("rdx,"):
            continue
        subject = None
        for k in range(j + 1, min(j + 6, len(ins))):
            if ins[k].mnemonic == "mov" and ins[k].op_str.startswith("rcx,"):
                subject = ins[k].op_str.split(",", 1)[1].strip()
            c = callee(ins[k])
            if c in ("System.String::Equals", "System.String::op_Equality"):
                if k + 2 < len(ins) and ins[k + 1].mnemonic == "test" and ins[k + 2].mnemonic in ("jne", "je"):
                    cmp.append((l, k + 2, subject))
                break
            if c:
                break
    codes = {l for l, _, _ in cmp}

    def follow(j, limit=200):
        via = []
        for _ in range(limit):
            if j is None or j >= len(ins):
                return None, via
            if j in lit and lit[j] not in codes:
                return lit[j], via
            x = ins[j]
            if (c := callee(x)) and not c.startswith("UnityEngine.Object::op_"):
                via.append(c.split("::")[-1])
            if x.mnemonic == "ret":
                return None, via
            if x.mnemonic == "jmp" and x.operands and x.operands[0].type == X.X86_OP_IMM:
                j = at.get(x.operands[0].imm)
                continue
            j += 1
        return None, via

    out = []
    for l, k, subject in cmp:
        op = ins[k].operands[0]
        eq = (at.get(op.imm) if op.type == X.X86_OP_IMM else None) if ins[k].mnemonic == "jne" else k + 1
        path, via = follow(eq)
        out.append((l, subject, path, via))
    return out


if __name__ == "__main__":
    main(sys.argv[1:])
