"""Read-only: print each probed effect's EffectControl fields (life, afterLife, follow*) from the researchers' probe dumps."""
import json, sys
def docs(path):
    s = open(path, encoding="utf-8").read(); i = 0; dec = json.JSONDecoder()
    while i < len(s):
        while i < len(s) and s[i].isspace(): i += 1
        if i >= len(s): break
        try: o, i = dec.raw_decode(s, i); yield o
        except json.JSONDecodeError: i = s.find("\n{", i + 1); i = len(s) if i < 0 else i + 1
def walk(o, name=None):
    if isinstance(o, dict):
        if o.get("type") == "EffectControl" or "followState" in o:
            print(name, {k: o.get(k) for k in ("life", "afterLife", "followState", "followPosition", "followRotation") if k in o})
        for k, v in o.items(): walk(v, k if name is None else name)
    elif isinstance(o, list):
        for v in o: walk(v, name)
for p in sys.argv[1:]:
    print("==", p)
    for d in docs(p): walk(d)
