"""Read-only probe (fx_penguin_research/parts): the names of Unity's built-in shaders by path ID. BB's data folder has no
"unity default resources" (Unity 3.5 keeps it in the player), so this reads Reborn's "unity default resources" and
"unity_builtin_extra" (a later Unity): materials refer to built-in shaders by file ID, which Unity keeps stable, so the
IDs BB's materials use (7, 30, 34, 200-207) can be named, not guessed.
  uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I checks/fx_penguin_research/parts/probe7.py
"""
import os
import UnityPy

R = next(os.path.join(p, "12TailsReborn_Data", "Resources") for p in (r"D:\12tails", r"C:\Users\Jump\Desktop\12tails")
         if os.path.isdir(os.path.join(p, "12TailsReborn_Data", "Resources")))
for fn in ("unity default resources", "unity_builtin_extra"):
    env = UnityPy.load(os.path.join(R, fn))
    for f in env.files.values():
        for pid, o in sorted(f.objects.items()):
            if o.type.name != "Shader" or pid > 300:
                continue
            try:
                t = o.read_typetree()
                name = t.get("m_ParsedForm", {}).get("m_Name") or t.get("m_Name") or "?"
                if name == "?" and t.get("m_Script"):
                    name = t["m_Script"].split('"')[1]
            except Exception as e:      # noqa: BLE001
                try:
                    name = o.read().m_Name
                except Exception:      # noqa: BLE001
                    name = f"(unreadable: {e})"
            print(fn, pid, name)
