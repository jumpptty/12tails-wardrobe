r"""Copy the prop textures the wardrobe's props JSON names into its own data (wardrobe/data/props/tex/), from the video
folder's extracted props (12tails-video/props/tex/, read only). The page loads them from `${DATA}props/tex/`, the same
path the published copy uses (split from 12tails-video on 2026-11-09: a separate folder can't reach ../props/tex/).
An existing copy is never overwritten (wardrobe_tot.py writes its own tot_*.png there); a texture the video folder
lacks is listed and the run exits 1, so a prop never shows up grey.

  py -3 pipeline/wardrobe_props_tex.py [--data wardrobe/data] [--src <video>/props/tex]
wardrobe_data.py runs it at the end of a build; adopt_from_video.ps1 runs it after moving the data in.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VIDEO = ROOT.parent / "12tails-video"


def referenced_textures(data: Path) -> set:
    """Every texture name in data/<cls>/props_<kind>.json (nodes[].mats[].tex)."""
    names = set()
    for f in sorted(data.glob("*/props_*.json")):
        for prop in json.loads(f.read_text(encoding="utf-8")):
            for node in prop.get("nodes", []):
                names.update(m["tex"] for m in node.get("mats", []) if m.get("tex"))
    return names


def copy_prop_textures(data: Path, src: Path) -> tuple:
    """Copy each referenced texture missing from data/props/tex/ out of src; returns (copied, missing names)."""
    dst = data / "props" / "tex"
    copied, missing = 0, []
    for name in sorted(referenced_textures(data)):
        if (dst / name).exists():
            continue
        if not (src / name).is_file():
            missing.append(name)
            continue
        dst.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src / name, dst / name)
        copied += 1
    return copied, missing


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--data", type=Path, default=ROOT / "wardrobe" / "data")
    ap.add_argument("--src", type=Path, default=VIDEO / "props" / "tex")
    a = ap.parse_args(argv)
    copied, missing = copy_prop_textures(a.data, a.src)
    print(f"prop textures: {copied} copied into {a.data / 'props' / 'tex'}, missing: {len(missing)}")
    for name in missing:
        print(f"  missing in {a.src}: {name}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
