"""Read only: the Sheep's 13 effects through wardrobe_fx.effect() with today's LAYOUTS; each node's decoded parts and
each material's blend / tint / color / emission. Writes nothing."""
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("wfx", sys.argv[1]); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
g = w.Game()
NAMES = ("homingLight,nAttack,cAttack,lullaby_ring,soulOfArms,edenSanctuary,sealOfAttack,sealOfDefense,sealOfEarth,"
         "sealOfHeaven,divinitySpear,divinitySword,divinityAxe,returncast").split(",")
for n in NAMES:
    mats, texs, snd = {}, {}, set()
    try:
        e = w.effect(g, "sheep", n, mats, texs, snd)
    except Exception as ex:
        print(n, "FAILS", type(ex).__name__, ex); continue
    print(f"== {n} (root {e['nodes'][0]['name']}); sounds {sorted(snd)}")
    for nd in e["nodes"]:
        for c in nd["comps"]:
            if c["type"] in ("AlphaTimer", "ProjectileControl", "Sheep_seal", "Sheep_nAttack", "Sheep_homingLight", "Sheep_cAttack", "Sheep_edenSanctuary", "AudioSource"):
                print("  ", nd["name"], json.dumps(c))
    for k, m in mats.items():
        if m["emission"] or m["blend"].startswith("shader:"):
            print("   mat", k, m["blend"], "tint", m["tint"], "color", m["color"], "emission", m["emission"])
