"""TTO's Penguin sounds/ clips the three Row6 skills play (Penguin::Row6Sound@0x1DB04B0 = penguin/sounds/<name>) and the
two prefab AudioSource clips: TTO's AudioClip length vs BB's rip WAV. Writes nothing.
uv run --no-project --with UnityPy python -I sounds.py <aa_catalog.py> <tto_assets/<date>> <BB rip penguin folder>"""
import importlib.util, os, sys, wave, UnityPy
spec = importlib.util.spec_from_file_location("aa_catalog", sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
assets, rip = sys.argv[2], sys.argv[3]
names = ["fallingStar_ring", "castEffect", "manaArc", "fallingComet", "novarFlare", "blink", "iceBreak", "blizzard",
         "emperorPenguin_whistle", "iceBlock", "cAttack", "emperorPenguin_flock", "absoluteZero", "frozenBlast", "fallingStar_hit"]
cat = m.Catalog(os.path.join(assets, "catalog.bin")); base = "gameassets/characters/heroes/penguin/sounds/"
want = {base + n.lower(): n for n in names}; iid = {}; deps = set()
for addr, loc in cat.entries():
    if addr in want: iid[loc["id"]] = want[addr]; deps.update(loc["bundles"])
env = UnityPy.load(*[os.path.join(assets, "dec", b) for b in sorted(deps)])
tto = {}
for o in env.objects:
    if o.type.name == "AssetBundle":
        for k, v in o.read_typetree()["m_Container"]:
            if k in iid:
                a = o.assets_file.objects[v["asset"]["m_PathID"]].read()
                tto[iid[k]] = round(a.m_Length, 3)
for n in names:
    p = os.path.join(rip, "sounds", n + ".wav"); bb = None
    if os.path.exists(p):
        with wave.open(p) as w: bb = round(w.getnframes() / w.getframerate(), 3)
    print(f"{n:24s} TTO {tto.get(n)}  BB sounds/ {bb}")
