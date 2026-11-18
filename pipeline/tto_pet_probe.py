r"""Each TTO pet prefab's PetControl fields and Animation clips, and the idle clip TTO and BB would play at rest
(2026-11-18, plans/wardrobe_pets_tto_rules.md: TTO1118 picks the idle by PetControl.idlePrefix, BB plays "root" only
when a "run" clip exists). Reads decrypted bundles (the Bible's tools/bundle_decrypt.js output) and the catalog that
lists them; read only.

  uv run --no-project --with UnityPy python -I pipeline/tto_pet_probe.py <dec folder> <catalog.bin> [--json <out>]
  e.g. ... ..\12tails-video\tto_assets\2026-11-04\dec ..\12tails-video\tto_assets\2026-11-04\catalog.bin

Per prefab (catalog addresses under characters/pet/ and characters/pets/, GameObjects, effects left out): followType,
followDistance, idlePrefix, runPrefix, attackClip, the emotes, the Animation's default clip (m_Animation),
m_PlayAutomatically and its clips in m_Animations order, then
  tto_idle = PetControl.FindClip(idlePrefix) (TTO1118 0x1a92600: lower-case; a clip named the prefix, or starting
             with prefix + "_", wins at once in clip order; else the first clip starting with the prefix), played by
             PlayIdle (0x1a94bf0) at rest for followType 1 / 2 / 3; None = nothing called, the default clip plays
             when m_PlayAutomatically (and always for followType 0 / 4 / 5: their LateUpdate never calls PlayIdle)
  bb_idle  = "root" when a "run" clip exists and followType is 1 / 2 / 3 (BB PetControl.cs:490, :655), else None
A PetControl whose type tree lacks idlePrefix / runPrefix gets the C# defaults "root" / "run" (PetControl::.ctor
0x1a95010; printed "(absent: root)"); a present empty string stays empty (FindClip returns null). A clip in a bundle
not given prints as "?" (2026-11-18: today's pet prefab bundle a4c2b80dbbffe327c3ae16b606b93a2d alone gives every
PetControl field, the same as 11-04's for all 101 prefabs, but only some clip names).
"""
import json
import os
import subprocess
import sys

import UnityPy

DEC, CAT = sys.argv[1], sys.argv[2]
OUT = sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv else None
BIBLE = next((p for p in (r"D:\12tails", r"C:\Users\Jump\Desktop\12tails") if os.path.isdir(p)), r"D:\12tails")
TOOL = os.path.join(BIBLE, "DecompiledSource_TTO_2026-11-14", "tools", "aa_catalog.py")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

out = subprocess.run([sys.executable, "-P", TOOL, CAT, "--grep", r"(?i)^gameassets/characters/pets?/"],
                     capture_output=True, text=True, encoding="utf-8", check=True).stdout
rows = {}
for line in out.splitlines():
    p = line.split("\t")
    if len(p) >= 4 and p[1].endswith("GameObject") and "/effects/" not in p[0].lower():
        rows[p[0]] = (p[2], p[3].split())
bundles = sorted({b for _, bs in rows.values() for b in bs if os.path.exists(os.path.join(DEC, b))})
env = UnityPy.load(*[os.path.join(DEC, b) for b in bundles])
container = dict(env.container.items())


def find_clip(names, prefix):
    """TTO1118 PetControl.FindClip over the Animation's states (their order assumed = m_Animations')."""
    if not prefix:
        return None
    p, first = prefix.lower(), None
    for n in names:
        low = n.lower()
        if low == p or low.startswith(p + "_"):
            return n
        if first is None and low.startswith(p):
            first = n
    return first


def comps(go):
    for c in go.m_Components if hasattr(go, "m_Components") else go.m_Component:
        ptr = c.component if hasattr(c, "component") else c if hasattr(c, "read") else c[1]
        try:
            yield ptr.read()
        except Exception:
            continue


def walk(go):
    yield go
    for c in comps(go):
        if c.object_reader.type.name == "Transform":
            for ch in c.m_Children:
                yield from walk(ch.read().m_GameObject.read())
            break


report = []
for addr, (iid, _) in sorted(rows.items()):
    obj = container.get(iid)
    if obj is None:
        report.append({"address": addr, "missing": True})
        continue
    root = obj.read()
    pc, anim = None, None   # the first PetControl and the first Animation in the prefab tree (root first)
    for go in walk(root):
        for c in comps(go):
            t = c.object_reader.type.name
            if t == "MonoBehaviour" and pc is None:
                try:
                    tt = c.object_reader.read_typetree()
                except Exception:
                    continue
                if "followType" in tt and "followDistance" in tt:
                    pc = tt
            elif t == "Animation" and anim is None:
                anim = c
    clips, default, auto = [], None, None
    if anim is not None:
        for p in anim.m_Animations:
            try:
                clips.append(p.read().m_Name)
            except Exception:
                clips.append("?")
        try:
            default = anim.m_Animation.read().m_Name
        except Exception:
            default = None
        auto = bool(anim.object_reader.read_typetree().get("m_PlayAutomatically"))
    row = {"address": addr, "prefab": root.m_Name}
    if pc is None:
        row["petcontrol"] = None
    else:
        ft = pc.get("followType")
        has_idle = "idlePrefix" in pc
        idle_prefix = pc.get("idlePrefix") if has_idle else "root"
        run_prefix = pc.get("runPrefix") if "runPrefix" in pc else "run"
        tto = find_clip(clips, idle_prefix) if ft in (1, 2, 3) else None
        bb = "root" if ft in (1, 2, 3) and "run" in clips else None
        row.update({"followType": ft, "followDistance": pc.get("followDistance"),
                    "idlePrefix": idle_prefix if has_idle else "(absent: root)",
                    "runPrefix": run_prefix if "runPrefix" in pc else "(absent: run)",
                    "attackClip": pc.get("attackClip"), "emotes": [(e.get("emote"), e.get("clip"), e.get("hold"))
                                                                   for e in pc.get("emotes", []) or []],
                    "default": default, "playAutomatically": auto, "clips": clips,
                    "tto_idle": tto, "bb_idle": bb})
    report.append(row)
    flag = "" if pc is None or row["tto_idle"] == row["bb_idle"] else "  <- differs"
    print(json.dumps(row, ensure_ascii=False) + flag)
if OUT:
    json.dump(report, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"{len(report)} prefabs, {sum(1 for r in report if r.get('petcontrol', 1) is None)} without a PetControl, "
      f"{sum(1 for r in report if r.get('missing'))} not in the loaded bundles")
