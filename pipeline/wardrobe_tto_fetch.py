r"""Fetch and decrypt the TTO client's bundles for given addresses, into a dated folder.

    py -3 pipeline/wardrobe_tto_fetch.py --out tto_assets/2026-11-18 --grep "characters/pets?/" [--grep "<regex>" ...]

Reads the live client's catalog (%LOCALAPPDATA%\TailsTopia\game\TailsTopia\TailsTopiaOnline_Data\StreamingAssets\aa\
catalog.bin, override with --client <the aa folder>), lists the rows whose address matches a regex with the Bible's
aa_catalog.py, and for every bundle on those rows (the first holds the asset, the rest are its dependencies) decrypts it
with the Bible's bundle_decrypt.js into <out>/dec/ unless it is already there. The catalog is copied to <out>/catalog.bin.
Later steps read <out> with UnityPy (UnityPy.load(<out>/dec/<bundle>...)). Read only: the client and the Bible.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

TOOLS = r"D:\12tails\DecompiledSource_TTO_2026-11-14\tools"
CLIENT_AA = os.path.join(os.environ.get("LOCALAPPDATA", ""), "TailsTopia", "game", "TailsTopia",
                         "TailsTopiaOnline_Data", "StreamingAssets", "aa")


def bundles_for(rows, pattern):
    """Every bundle listed on the rows whose address matches the regex (row: address, type, id, bundles)."""
    rx = re.compile(pattern)
    return {b for r in rows if len(r) >= 4 and rx.search(r[0]) for b in r[3].split()}


def require_bundles(rows, pattern):
    """bundles_for, but a pattern that matches nothing stops the run (a typo or a catalog without the addresses)."""
    got = bundles_for(rows, pattern)
    if not got:
        sys.exit(f"no address in the catalog matches --grep {pattern!r}: nothing to fetch for it")
    return got


def catalog_rows(catalog, pattern):
    out = subprocess.run([sys.executable, "-P", os.path.join(TOOLS, "aa_catalog.py"), catalog, "--grep", pattern],
                         capture_output=True, text=True, encoding="utf-8", check=True).stdout
    return [line.split("\t") for line in out.splitlines() if line.count("\t") >= 3]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", required=True, help="output folder (gets catalog.bin and dec/)")
    ap.add_argument("--grep", action="append", required=True, help="address regex; repeat for more")
    ap.add_argument("--client", default=CLIENT_AA, help="the client's StreamingAssets\aa folder")
    a = ap.parse_args()
    dec = os.path.join(a.out, "dec")
    os.makedirs(dec, exist_ok=True)
    catalog = os.path.join(a.out, "catalog.bin")
    shutil.copyfile(os.path.join(a.client, "catalog.bin"), catalog)
    need = set()
    for pat in a.grep:
        rows = catalog_rows(catalog, pat)
        got = require_bundles(rows, pat)
        print(f"{pat}: {len(rows)} addresses, {len(got)} bundles")
        need |= got
    todo = sorted(b for b in need if not os.path.exists(os.path.join(dec, b)))
    print(f"{len(need)} bundles needed, {len(need) - len(todo)} already decrypted, {len(todo)} to do", flush=True)
    src = os.path.join(a.client, "StandaloneWindows64")
    for b in todo:
        if not os.path.exists(os.path.join(src, b)):
            sys.exit(f"missing in the client: {os.path.join(src, b)}")
    for i in range(0, len(todo), 50):
        with tempfile.TemporaryDirectory() as tmp:  # only the needed bundles, never the whole install
            for b in todo[i:i + 50]:
                shutil.copyfile(os.path.join(src, b), os.path.join(tmp, b))
            subprocess.run(["node", os.path.join(TOOLS, "bundle_decrypt.js"), tmp, dec], check=True)
    missing = [b for b in need if not os.path.exists(os.path.join(dec, b))]
    if missing:
        sys.exit(f"not decrypted: {missing[:5]} ...")
    print(f"{len(need)} bundles in {dec}")


if __name__ == "__main__":
    main()
