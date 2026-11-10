"""Read-only probe (fx_penguin_research/parts): every Material in the game's resources.assets on a Unity built-in shader
("unity default resources" / "unity_builtin_extra"), grouped by the shader's path ID: how many, which saved colour
properties, a few names, and for each sampled texture its mean RGB / alpha and the share of pixels with alpha < 0.5 and
with RGB near white / grey / black (which blend the texture is drawn for). Answers what built-ins 204-208 are.
  uv run --no-project --with UnityPy --with imageio-ffmpeg --with pillow python -I checks/fx_penguin_research/parts/probe4.py
"""
import collections, importlib.util, os
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("wfx", os.path.join(HERE, "..", "..", "..", "pipeline", "wardrobe_fx.py"))
wfx = importlib.util.module_from_spec(spec); spec.loader.exec_module(wfx)
spec2 = importlib.util.spec_from_file_location("lay", os.path.join(HERE, "layouts.py"))
lay = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(lay); wfx.LAYOUTS.update(lay.PENGUIN)
game = wfx.Game()
# every hero class's effects first, so the files their materials live in are loaded (game.obj loads a file when named)
for k in list(game.container):
    if "/heroes/" in k and "/effects/" in k:
        o = game.obj(game.container[k], game.files["mainData"])
        if o is not None and o.type.name == "GameObject":
            try:
                wfx.effect(game, k.split("/")[2], k.rsplit("/", 1)[1], {}, {}, set())
            except Exception:      # noqa: BLE001 (a script with no layout: its materials may be missed)
                pass
groups = collections.defaultdict(list)
for f in list(game.files.values()):
    if not hasattr(f, "objects"): continue
    for o in f.objects.values():
        if o.type.name != "Material":
            continue
        t = o.read_typetree(); sh = t["m_Shader"]
        if not sh["m_FileID"]:
            continue
        ext = f.externals[sh["m_FileID"] - 1].path
        if "default resources" not in ext and "builtin" not in ext:
            continue
        key = lambda k: k["name"] if isinstance(k, dict) else k
        props = sorted(key(k) for k, v in t["m_SavedProperties"]["m_Colors"])
        tex = None
        for k, v in t["m_SavedProperties"]["m_TexEnvs"]:
            if key(k) == "_MainTex":
                tex = game.obj(v["m_Texture"], f)
        groups[(os.path.basename(ext), sh["m_PathID"])].append((t["m_Name"], props, tex))
for (ext, pid), ms in sorted(groups.items()):
    pc = collections.Counter(tuple(p) for _, p, _ in ms)
    print(f"== {ext} {pid}: {len(ms)} materials; props {pc.most_common(3)}")
    print("   e.g.", [n for n, _, _ in ms[:12]])
    if pid in (7, 200, 202, 203):
        continue
    for n, _, tex in ms[:8]:
        if tex is None:
            continue
        try:
            im = tex.read().image.convert("RGBA")
        except Exception as e:      # noqa: BLE001
            print("   ", n, "texture unreadable", e); continue
        px = list(im.resize((32, 32)).get_flattened_data()) if hasattr(im, "get_flattened_data") else list(im.resize((32, 32)).getdata())
        N = len(px)
        mean = [round(sum(p[i] for p in px) / N / 255, 2) for i in range(4)]
        lowA = sum(p[3] < 128 for p in px) / N
        white = sum(min(p[:3]) > 220 for p in px) / N
        grey = sum(all(100 < c < 155 for c in p[:3]) for p in px) / N
        black = sum(max(p[:3]) < 30 for p in px) / N
        print(f"    {n}: tex {tex.read().m_Name} mean rgba {mean}, alpha<0.5 {lowA:.0%}, white {white:.0%}, grey {grey:.0%}, black {black:.0%}")
