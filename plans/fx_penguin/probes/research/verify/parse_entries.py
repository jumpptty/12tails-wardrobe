"""Read-only: parse every ```json block of the two Penguin reports as one object, check cue times are in order and
every cued name is a file in the rip's voices/ or effects/ (novaFlare: elementals/manavortex/effects)."""
import json, os, re, sys
RIP = r"C:\Users\Jump\Desktop\12tails\RippedAssets\ExportedProject\Assets\Resources\gameassets\characters"
have = {"voice": {f[:-4] for f in os.listdir(os.path.join(RIP, r"heroes\penguin\voices")) if f.endswith(".wav")},
        "fx": {f[:-7] for f in os.listdir(os.path.join(RIP, r"heroes\penguin\effects")) if f.endswith(".prefab")} | {"novaFlare"}}
for rep in sys.argv[1:]:
    txt = open(rep, encoding="utf-8").read()
    for blk in re.findall(r"```json\n(.*?)```", txt, re.S):
        d = json.loads("{" + blk.strip().rstrip(",") + "}")
        for key, e in d.items():
            groups = e["skills"].items() if "skills" in e else [(key, e)]
            for sk, g in groups:
                ts = [c[0] for c in g["cues"]]
                assert ts == sorted(ts), (key, sk)
                for c in g["cues"]:
                    for n in c[2].split("|"):
                        assert n in have[c[1]], (key, sk, c)
                print(os.path.basename(rep), key, sk, len(g["cues"]), "ok")
