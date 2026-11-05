r"""In-game item icons for the wardrobe (user 2026-11-04: "the wardrobe is really hard to use without the in-game icons").

  uv run --no-project --with pefile --with capstone --with UnityPy --with pillow python wardrobe_icons.py
  -> wardrobe/data/item_map.json  (per class: item code -> model, for weapon / armor / accessory / trinket)
     wardrobe/data/icons/<folder>/<name>.webp  (gamegui/icons/items/<folder>/<name>, every item icon)
     wardrobe/data/icons.json      (per class: outfit / prop name -> icon path, and every code of it)

Icons are named by item code (gamegui/icons/items/armor/shp24 = a_shp24), models by name, and TTO keeps no item table
in its bundles: the code -> model link is compiled into each <Class>Equipment's static string switches
(WeaponAsset / BowAsset / ArrowAsset / LanceAsset / ShieldAsset, ArmorMeshAsset, AccessoryAsset, TrinketAsset;
TTO1102 dump.cs, SheepEquipment RVAs 0x1a9f040 ...). Read with capstone from the TTO decompile's GameAssembly.dll: the
C# string switch compiles to a hash tree, so codes and names are not adjacent; each code compare (op_Equality, test al,
jne / je) is followed to its "equal" branch and the first name literal on it is the model. Checked against BB's code
(SheepEquipment.cs: w_shp1 -> noviceBook, a_all1 -> Sheep_scout). The DLL is TTO1102's; items added by a later patch
need the decompile redone (its BUILD.md). Several codes can share a model (Sheep a_shp24 and a_shp37 = Sheep_halloween).
"""
import json
import os
import re
import subprocess
import sys

DEC = r"D:\12tails\DecompiledSource_TTO_2026-11-02"
sys.path.insert(0, os.path.join(DEC, "tools"))
from binary import Binary          # noqa: E402  (the TTO decompile's tools)
from usages import Usages          # noqa: E402
import capstone                    # noqa: E402
from capstone import x86_const as X  # noqa: E402
import UnityPy                     # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "tto_assets", "2026-11-04")
OUT = os.path.join(ROOT, "wardrobe", "data")
CLASSES = ["bat", "bison", "cat", "chameleon", "mole", "monkey", "panda", "penguin", "rabbit", "sheep", "whale", "wolf"]
CODE = re.compile(r"^[a-z]{1,2}_[a-z]+\d+[a-z0-9]*$")

cwd = os.getcwd()
os.chdir(DEC)
b = Binary("client/GameAssembly.dll")
u = Usages(b, "global-metadata.decrypted.dat")
dump = open("dump.cs", encoding="utf-8").read()
os.chdir(cwd)
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True


def mapping(rva):
    s, e = b.func_range(b.IB + rva)
    if s < b.IB:
        s, e = s + b.IB, e + b.IB
    ins = list(md.disasm(b.B[b.off(s): b.off(s) + (e - s)], s))
    at = {x.address: j for j, x in enumerate(ins)}
    lit = {}
    for j, x in enumerate(ins):
        for op in x.operands:
            if op.type == X.X86_OP_MEM and op.mem.base == X.X86_REG_RIP:
                tgt = x.address + x.size + op.mem.disp
                r = u.resolve(tgt)
                if r and r[0] == 5:
                    lit[j] = u.literal((b.q(tgt) & 0x1FFFFFFF) >> 1)

    def first_name(j, limit=60):
        for _ in range(limit):
            if j >= len(ins):
                return None
            if j in lit and not CODE.match(lit[j]):
                return lit[j]
            x = ins[j]
            if x.mnemonic == "ret":
                return None
            if x.mnemonic == "jmp" and x.operands and x.operands[0].type == X.X86_OP_IMM:
                j = at.get(x.operands[0].imm, len(ins))
                continue
            j += 1
        return None
    out = {}
    for j, l in lit.items():
        if not CODE.match(l):
            continue
        for k in range(j + 1, min(j + 12, len(ins))):
            if ins[k].mnemonic in ("jne", "je"):
                op = ins[k].operands[0]
                eq = (at.get(op.imm) if op.type == X.X86_OP_IMM else None) if ins[k].mnemonic == "jne" else k + 1
                if eq is not None and (n := first_name(eq)):
                    out[l] = n
                break
    return out


item_map = {}
for cls in CLASSES:
    m = re.search(rf"public class {cls.capitalize()}Equipment : CharacterEquipment.*?\n}}", dump, re.S)
    funcs = re.findall(r"// RVA: (0x[0-9a-f]+)[^\n]*\n\s*private static string (\w+Asset)\(", m.group(0))
    kinds = {}
    for rva, fn in funcs:
        if fn == "ArmorMaterialAsset":
            continue
        kind = {"ArmorMeshAsset": "armor", "AccessoryAsset": "accessory", "TrinketAsset": "trinket"}.get(fn, "weapon")
        for code, model in mapping(int(rva, 16)).items():       # one code can give two pieces: bow + arrow, lance + shield
            names = kinds.setdefault(kind, {}).setdefault(code, [])
            if model not in names:
                names.append(model)
    item_map[cls] = kinds
    print(cls, {k: len(v) for k, v in kinds.items()}, flush=True)   # item_map.json: code -> [model, ...]
# shared items (fashion wings, Halloween headbands, seals, auras: heroes/all/...): CharacterEquipment's loaders return
# the asset path ("gameassets/characters/heroes/all/azure_wing"); the model name is its last part, kept lower case
ce = re.search(r"public abstract class CharacterEquipment : MonoBehaviour.*?\n}", dump, re.S).group(0)
shared = {}
for rva, fn in re.findall(r"// RVA: (0x[0-9a-f]+)[^\n]*\n\s*protected static GameObject (LoadSharedTrinket|LoadSharedAccessory|LoadSeal|LoadAura)\(", ce):
    kind = "accessory" if fn == "LoadSharedAccessory" else "trinket"
    for code, path in mapping(int(rva, 16)).items():
        names = shared.setdefault(kind, {}).setdefault(code, [])
        if path.rsplit("/", 1)[-1].lower() not in names:
            names.append(path.rsplit("/", 1)[-1].lower())
item_map["all"] = shared
print("all (shared)", {k: len(v) for k, v in shared.items()}, flush=True)
os.makedirs(OUT, exist_ok=True)
json.dump(item_map, open(os.path.join(OUT, "item_map.json"), "w"), indent=1)

# ---- icons ----
cat = subprocess.run([sys.executable, "-P", os.path.join(DEC, "tools", "aa_catalog.py"), os.path.join(ASSETS, "catalog.bin"),
                      "--grep", r"^gamegui/icons/items/(weapon|armor|accessory|acessory|trinket)/"],
                     capture_output=True, text=True, encoding="utf-8", check=True).stdout
icons, bundles = {}, set()
for line in cat.splitlines():
    p = line.split("\t")
    if len(p) >= 4 and p[1].endswith("Texture2D"):
        folder, name = p[0].split("/")[-2:]
        icons[(folder, name)] = p[2]
        bundles.add(p[3].split()[0])
env = UnityPy.load(*[os.path.join(ASSETS, "dec", x) for x in sorted(bundles)])
cont = dict(env.container.items())
written = set()
for (folder, name), iid in sorted(icons.items()):
    if iid in cont:
        d = os.path.join(OUT, "icons", folder)
        os.makedirs(d, exist_ok=True)
        cont[iid].read().image.save(os.path.join(d, f"{name}.webp"), "WEBP", lossless=True)
        written.add((folder, name))
print("icons written", len(written), "of", len(icons), flush=True)

FOLDERS = {"weapon": ["weapon"], "armor": ["armor"], "accessory": ["accessory", "acessory"], "trinket": ["trinket"]}
index = {}
for cls, kinds in item_map.items():
    entry = {"outfits": {}, "weapons": {}, "accessories": {}, "trinkets": {}}
    for kind, codes in kinds.items():
        slot = {"armor": "outfits", "weapon": "weapons", "accessory": "accessories", "trinket": "trinkets"}[kind]
        for code, models in sorted(codes.items(), key=lambda kv: (len(kv[0]), kv[0])):
            for model in models:
                name = model.split("_", 1)[1] if kind == "armor" and model.lower().startswith(cls + "_") else model
                if cls == "all":
                    name = name.lower()                 # the page looks shared items up by lower-case name
                e = entry[slot].setdefault(name, {"icon": None, "codes": []})
                e["codes"].append(code)
                short = code.split("_", 1)[1]
                for f in FOLDERS[kind]:
                    if not e["icon"] and (f, short) in written:
                        e["icon"] = f"icons/{f}/{short}.webp"
    index[cls] = entry
json.dump(index, open(os.path.join(OUT, "icons.json"), "w"), separators=(",", ":"))
for cls, e in index.items():
    print(cls, {k: f"{sum(1 for x in v.values() if x['icon'])}/{len(v)}" for k, v in e.items()})
