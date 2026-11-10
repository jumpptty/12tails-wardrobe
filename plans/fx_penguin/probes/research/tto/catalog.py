"""List TTO's catalog addresses under gameassets/characters/heroes/penguin/ (effects, sounds, voices, arcana), with each
effect's bundle. py -3 -I catalog.py <aa_catalog.py> <tto_assets/<date>/catalog.bin>"""
import importlib.util, sys, collections
spec = importlib.util.spec_from_file_location("aa_catalog", sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
cat = m.Catalog(sys.argv[2]); base = "gameassets/characters/heroes/penguin/"
by = collections.defaultdict(list)
for addr, loc in cat.entries():
    if addr.startswith(base):
        rest = addr[len(base):]; k = rest.rsplit("/", 1)[0] if "/" in rest else "."
        by[k].append((rest.rsplit("/", 1)[-1], loc["bundles"]))
for k in sorted(by):
    names = sorted({n for n, _ in by[k]})
    print(f"{k} ({len(names)}):", ", ".join(names))
