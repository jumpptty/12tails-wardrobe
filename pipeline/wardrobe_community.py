r"""Community skins: the approved submissions in the private Discord channel -> wardrobe/data (2026-11-11, NOTES.md
"community skins"). The page's send dialog posts a visitor's skin through the site's Worker (pipeline/site_worker.mjs)
to the channel's webhook: one message per set (a whole look: its pieces' PNGs, a preview picture, a meta.json). The user approves a message by reacting ✅;
this script reads the channel with a bot, checks every approved skin against the data (never a TTO piece: user 2026-11-11, "TTO upload should work only on private
version"; the pop-up's picture is the 2D texture) and writes:
  wardrobe/data/community/<cls>/<message id>_<n>.webp   (WebP q92, alpha kept; cls = "all" for a shared piece)
  wardrobe/data/community.json                          {"skins": [{id, cls, kind, item, name, link, at, tex: {tex: file}}]}
The channel is the truth: a message whose ✅ is taken away (or that is deleted) leaves the data at the next run.

  uv run --no-project --with pillow python -I pipeline/wardrobe_community.py [--dry-run]
(plain py -3 works only where Pillow is installed: the office's is not, 2026-11-12)

The bot's token and the channel id: %APPDATA%\12tails-wardrobe\discord.json {"token": "...", "channel": "..."} on each PC
(never in the repo), or the environment's DISCORD_BOT_TOKEN / DISCORD_CHANNEL. The bot needs View Channel and Read
Message History on that channel, and the Message Content intent (the Developer Portal's Bot page): without it Discord
hands a bot every message with its attachments empty. Then publish and deploy as usual (NOTES.md "Online copy").
"""
import io
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "wardrobe" / "data"
API = "https://discord.com/api/v10"
APPROVE = "✅"
KINDS = ("outfits", "weapons", "accessories", "trinkets")
UA = "DiscordBot (https://discord.com, 1)"


class Refused(Exception):
    """A submission that can't go in (the message says why)."""


# ---------- the data side: is the piece there, which textures does it have, how large is each ----------
def piece(data, cls, kind, item):
    """(cls the skin belongs to, its texture names, {tex: (w, h)}); cls is "all" for a shared piece. Raises Refused."""
    if kind not in KINDS:
        raise Refused(f"no such slot {kind!r}")
    if kind == "outfits":
        if cls == "all":
            raise Refused("an outfit belongs to one class")
        o = next((x for x in load(data / cls / "outfits.json", []) if x.get("name") == item), None)
        if not o or not o.get("colors"):
            raise Refused(f"{cls} has no outfit {item!r} with a texture")
        if o.get("tto"):
            raise Refused(f"{item!r} is TTO's: no community skins for TTO pieces (its texture would be the picture)")
        return cls, [""], {"": image_size(data / cls / "tex" / f"{item}{o['colors'][0]}.webp")}
    for owner in ([cls] if cls == "all" else [cls, "all"]):
        p = next((x for x in load(data / owner / f"props_{kind}.json", []) if x.get("name") == item), None)
        if p:
            if p.get("tto"):
                raise Refused(f"{item!r} is TTO's: no community skins for TTO pieces (its texture would be the picture)")
            mats = [m for n in p.get("nodes", []) for m in n.get("mats") or []] + (p.get("mats") or [] if p.get("heroSkin") else [])
            texs = list(dict.fromkeys(m["tex"] for m in mats if m.get("tex")))
            if not texs:
                raise Refused(f"{item!r} has no texture")
            return owner, texs, {t: image_size(data / "props" / "tex" / t) for t in texs}
    raise Refused(f"{cls} has no {kind} piece {item!r}")


def load(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default


def image_size(path):
    from PIL import Image
    with Image.open(path) as im:
        return im.size


SLOT_KIND = {"outfit": "outfits", "R": "weapons", "L": "weapons", "Head": "accessories", "Back": "trinkets"}
DEFAULT_SLOT = {"outfits": "outfit", "weapons": "R", "accessories": "Head", "trinkets": "Back"}


def check(data, meta, files):
    """meta.json + {file name: bytes} -> (cls, name, link, face, pieces, preview bytes or None). Raises Refused.
    A submission is a set (meta v2: `pieces`); the first format's one piece (kind, item, textures) reads as a set of one.
    A piece that can't go in (not in the data, TTO's) is left out; a set with none left is refused."""
    from PIL import Image
    cls = str(meta.get("cls", ""))
    name = " ".join(str(meta.get("name", "")).split())[:40]
    link = str(meta.get("link") or "").strip()[:200]
    if not name:
        raise Refused("no name to credit")
    if link and not (link.startswith("https://") and urllib.parse.urlparse(link).netloc):
        raise Refused(f"the link {link!r} is not https")
    face = meta.get("face")
    face = face if isinstance(face, int) and not isinstance(face, bool) and 0 <= face < 200 else None
    defs = meta["pieces"] if isinstance(meta.get("pieces"), list) else [{"kind": meta.get("kind"), "item": meta.get("item"), "textures": meta.get("textures")}]
    if not defs or len(defs) > 6:
        raise Refused("a set has 1 to 6 pieces")
    pieces, why = [], []
    for d in defs:
        try:
            kind, item = str(d.get("kind", "")), str(d.get("item", ""))
            owner, texs, sizes = piece(data, cls, kind, item)
            out = {}
            for t in d.get("textures") or []:
                tex, f = str(t.get("tex", "")), str(t.get("file", ""))
                if tex not in texs:
                    raise Refused(f"{item!r} has no texture {tex!r}")
                if f not in files:
                    raise Refused(f"the message lacks {f}")
                try:
                    with Image.open(io.BytesIO(files[f])) as im:
                        if im.format != "PNG":
                            raise Refused(f"{f} is not a PNG")
                        # the original's size, or exactly 2x / 4x / 8x of it up to 4096 (the page's skinDims: a high-res
                        # skin keeps its detail; user 2026-11-12: "ignore game logic and apply high-res texture")
                        w, h = sizes[tex]
                        if not any(im.size == (w * k, h * k) for k in (1, 2, 4, 8)) or max(im.size) > 4096:
                            raise Refused(f"{f} is {im.size[0]}x{im.size[1]}, the original {w}x{h} (or 2x / 4x / 8x of it)")
                        im.load()
                except Refused:
                    raise
                except Exception as e:
                    raise Refused(f"{f} can't be read ({type(e).__name__})")
                out[tex] = files[f]
            if not out:
                raise Refused(f"no texture for {item!r}")
            slot = d.get("slot") if SLOT_KIND.get(d.get("slot")) == kind else DEFAULT_SLOT[kind]
            pieces.append({"slot": slot, "kind": kind, "item": item, "owner": owner, "tex": out})
        except Refused as e:
            why.append(str(e))
    if not pieces:
        raise Refused(why[0] if why else "no piece in the message")
    preview = None
    for f in ("preview.jpg", "preview.png"):
        if f in files:
            try:
                with Image.open(io.BytesIO(files[f])) as im:
                    im.load()
                preview = files[f]
            except Exception:
                preview = None                   # an unreadable picture only costs the set its thumbnail
            break
    return cls, name, link, face, pieces, preview


def webp(png, quality=92, max_side=None):
    from PIL import Image
    with Image.open(io.BytesIO(png)) as im:
        im = im.convert("RGBA")
        if max_side:
            im.thumbnail((max_side, max_side))
        b = io.BytesIO()
        im.save(b, "WEBP", quality=quality, alpha_quality=100, method=6)
        return b.getvalue()


def old_ids(data):
    j = load(Path(data) / "community.json", {})
    return {s["id"] for s in j.get("sets") or j.get("skins") or []}


def apply(data, approved, dry=False):
    """approved: [(message id, meta, {file: bytes}, timestamp)] -> community.json (sets) + the pictures, mirrored exactly
    (a set no longer approved goes). Returns (added ids, removed ids, [(id, reason)] refused)."""
    data = Path(data)
    old = old_ids(data)
    sets, refused, writes = [], [], {}
    for mid, meta, files, at in approved:
        try:
            cls, name, link, face, pieces, preview = check(data, meta, files)
        except Refused as e:
            refused.append((mid, str(e)))
            continue
        n, out = 0, []
        for p in pieces:
            tex = {}
            for t, png in p["tex"].items():
                rel = f"community/{cls}/{mid}_{n}.webp"
                n += 1
                tex[t] = rel
                writes[rel] = lambda png=png: webp(png)
            out.append({"slot": p["slot"], "kind": p["kind"], "item": p["item"], "owner": p["owner"], "tex": tex})
        thumb = None
        if preview:
            thumb = f"community/{cls}/{mid}_p.webp"
            writes[thumb] = lambda pv=preview: webp(pv, 85, 640)
        title = " ".join(str(meta.get("title") or "").split())[:60]          # ชื่อผลงาน (2026-11-13), optional
        sets.append({"id": mid, "cls": cls, "name": name, **({"title": title} if title else {}), "link": link, "at": at,
                     "face": face, "thumb": thumb, "pieces": out})
    sets.sort(key=lambda s: (s["at"], s["id"]))
    keep = {f for s in sets for p in s["pieces"] for f in p["tex"].values()} | {s["thumb"] for s in sets if s["thumb"]}
    added = [s["id"] for s in sets if s["id"] not in old]
    removed = [i for i in old if i not in {s["id"] for s in sets}]
    if not dry:
        for rel, make in writes.items():
            p = data / rel
            if not p.exists():
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(make())
        for p in (data / "community").rglob("*.webp") if (data / "community").exists() else []:
            if p.relative_to(data).as_posix() not in keep:
                p.unlink()
        (data / "community.json").write_text(json.dumps({"sets": sets}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return added, removed, refused

# ---------- the Discord side ----------
def credentials():
    tok, ch = os.environ.get("DISCORD_BOT_TOKEN"), os.environ.get("DISCORD_CHANNEL")
    cfg = Path(os.environ.get("APPDATA", Path.home())) / "12tails-wardrobe" / "discord.json"
    if (not tok or not ch) and cfg.exists():
        c = json.loads(cfg.read_text(encoding="utf-8"))
        tok, ch = tok or c.get("token"), ch or c.get("channel")
    if not tok or not ch:
        sys.exit(f"no bot token / channel: write {cfg} as {{\"token\": \"...\", \"channel\": \"...\"}} (HANDOFF.md)")
    return tok, str(ch)


def http(url, token=None):
    for _ in range(5):
        req = urllib.request.Request(url, headers={"User-Agent": UA, **({"Authorization": f"Bot {token}"} if token else {})})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(float(json.loads(e.read() or b"{}").get("retry_after", 1)) + 0.2)
                continue
            raise SystemExit(f"Discord answered {e.code} for {url.split('?')[0]}: {e.read()[:200]!r}")
    raise SystemExit("Discord kept rate-limiting; try again later")


def files_of(m):
    """A message's files {name: url}: its attachments plus the embed's picture, which Discord takes out of the
    attachments (the Worker shows skin0.png as the embed image; first live send, 2026-11-12)."""
    att = {a["filename"]: a["url"] for a in m.get("attachments") or []}
    for e in m.get("embeds") or []:
        u = (e.get("image") or {}).get("url") or ""
        if u.startswith("https://"):
            att.setdefault(urllib.parse.urlsplit(u).path.rsplit("/", 1)[-1], u)
    return att


def approved_messages(token, channel):
    """Every webhook message in the channel that a person (not a bot) reacted ✅ to."""
    out, before = [], None
    while True:
        q = "?limit=100" + (f"&before={before}" if before else "")
        page = json.loads(http(f"{API}/channels/{channel}/messages{q}", token))
        if not page:
            break
        before = page[-1]["id"]
        for m in page:
            if not m.get("webhook_id") or not any(r.get("emoji", {}).get("name") == APPROVE for r in m.get("reactions") or []):
                continue
            users = json.loads(http(f"{API}/channels/{channel}/messages/{m['id']}/reactions/{urllib.parse.quote(APPROVE)}?limit=100", token))
            if not any(not u.get("bot") for u in users):
                continue
            att = files_of(m)
            if "meta.json" not in att:
                print(f"  {m['id']}: no meta.json (is the bot's Message Content intent on?)")
                continue
            meta = json.loads(http(att["meta.json"]))
            names = [t.get("file") for d in (meta.get("pieces") or [meta]) for t in d.get("textures") or []] + [n for n in ("preview.jpg", "preview.png") if n in att]
            files = {n: http(att[n]) for n in names if n in att}
            out.append((m["id"], meta, files, meta.get("at") or m.get("timestamp", "")))
    return out


def main():
    dry = "--dry-run" in sys.argv
    token, channel = credentials()
    approved = approved_messages(token, channel)
    added, removed, refused = apply(DATA, approved, dry)
    print(f"{len(approved)} approved in the channel; added {len(added)}, removed {len(removed)}, refused {len(refused)}"
          + (" (dry run: nothing written)" if dry else ""))
    for i in added:
        print("  + " + i)
    for i in removed:
        print("  - " + i)
    for i, why in refused:
        print(f"  ! {i}: {why}")


if __name__ == "__main__":
    main()
