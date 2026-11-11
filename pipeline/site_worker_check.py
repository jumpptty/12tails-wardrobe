"""The site's Worker (pipeline/site_worker.mjs) run in Cloudflare's own local runtime (wrangler dev), end to end: a
stand-in Discord webhook here receives what the Worker posts; Turnstile is Cloudflare's always-pass test secret (the
real siteverify is called, so this needs the internet). Checks a good submission (the message: payload_json with no
mentions, the PNG, meta.json), a refusal (no consent), another origin, a file path that is not the route.
  py -3 -I pipeline/site_worker_check.py
Exit 1 on any failure. Runs wrangler from an empty scratch folder with an empty assets folder (nothing is deployed)."""
import email.parser, email.policy, http.server, json, os, socket, struct, subprocess, sys, tempfile, threading, time, urllib.request, zlib
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
WORKER = Path(__file__).resolve().parent / "site_worker.mjs"
TEST_SECRET, TEST_TOKEN = "1x0000000000000000000000000000000AA", "XXXX.DUMMY.TOKEN.XXXX"
GOT = []


def free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p


class Hook(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_POST(self):
        raw = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        msg = email.parser.BytesParser(policy=email.policy.HTTP).parsebytes(b"Content-Type: " + self.headers["Content-Type"].encode() + b"\r\n\r\n" + raw)
        parts = {p.get_param("name", header="content-disposition"): p.get_payload(decode=True) for p in msg.iter_parts()}
        GOT.append({"path": self.path, "parts": parts})
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(b"{}")


def png(w, h):
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    return (bytes.fromhex("89504e470d0a1a0a") + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress((b"\0" + b"\xff\0\0\xff" * w) * h)) + chunk(b"IEND", b""))


def multipart(fields, files):
    b = "----wardrobecheck"
    out = b""
    for k, v in fields.items():
        out += f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    for k, (name, data) in files.items():
        out += f'--{b}\r\nContent-Disposition: form-data; name="{k}"; filename="{name}"\r\nContent-Type: image/png\r\n\r\n'.encode() + data + b"\r\n"
    return out + f"--{b}--\r\n".encode(), f"multipart/form-data; boundary={b}"


def post(url, fields, files, origin):
    body, ctype = multipart(fields, files)
    req = urllib.request.Request(url, data=body, method="POST", headers={"Content-Type": ctype, "Origin": origin})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


def main():
    fails = []
    check = lambda ok, what: (print(("ok   " if ok else "FAIL ") + what), ok or fails.append(what))
    hp = free_port()
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", hp), Hook)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    wp = free_port()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:    # workerd may still hold its cache file
        (Path(tmp) / "assets").mkdir()
        (Path(tmp) / "assets" / "index.html").write_text("<!doctype html><title>t</title>", encoding="utf-8")
        cmd = ["npx", "wrangler", "dev", str(WORKER), "--assets", str(Path(tmp) / "assets"), "--name", "wardrobe-check",
               "--compatibility-date", "2026-11-07", "--port", str(wp), "--ip", "127.0.0.1", "--local",
               "--var", f"DISCORD_WEBHOOK:http://127.0.0.1:{hp}/api/webhooks/1/test", "--var", f"TURNSTILE_SECRET:{TEST_SECRET}"]
        proc = subprocess.Popen(cmd, cwd=tmp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                                errors="replace", shell=os.name == "nt", env=dict(os.environ, WRANGLER_SEND_METRICS="false", CI="1"))
        base, origin = f"http://127.0.0.1:{wp}", f"http://127.0.0.1:{wp}"
        try:
            for _ in range(120):
                try:
                    urllib.request.urlopen(base + "/", timeout=2).read(); break
                except Exception:
                    if proc.poll() is not None:
                        print(proc.stdout.read()); sys.exit("wrangler dev stopped")
                    time.sleep(1)
            good = {"token": TEST_TOKEN, "cls": "sheep", "kind": "weapons", "item": "halloweenLantern", "name": "ผู้ทดสอบ",
                    "link": "https://example.com/me", "consent": "1", "tex0": "Sheep_halloweenWeapon.png"}
            st, body = post(base + "/api/submit", good, {"skin0": ("skin0.png", png(8, 8))}, origin)
            check(st == 200 and body == {"ok": True}, f"good submission: {st} {body}")
            g = GOT[-1] if GOT else {"path": "", "parts": {}}
            payload = json.loads(g["parts"].get("payload_json") or b"{}")
            meta = json.loads(g["parts"].get("files[1]") or b"{}")
            check(g["path"].endswith("?wait=true") and payload.get("allowed_mentions") == {"parse": []}, f"Discord got the message: {g['path']}")
            check(meta.get("name") == "ผู้ทดสอบ" and meta.get("textures", [{}])[0].get("w") == 8, f"meta.json: {meta}")
            check((g["parts"].get("files[0]") or b"")[:8] == bytes.fromhex("89504e470d0a1a0a"), "the PNG arrived as sent")
            st, body = post(base + "/api/submit", dict(good, consent="0"), {"skin0": ("skin0.png", png(8, 8))}, origin)
            check((st, body.get("error")) == (400, "consent"), f"no consent refused: {st} {body}")
            st, body = post(base + "/api/submit", good, {"skin0": ("skin0.png", png(8, 8))}, "https://evil.example")
            check((st, body.get("error")) == (403, "origin"), f"another origin refused: {st} {body}")
            try:
                r = urllib.request.urlopen(base + "/nothing-here", timeout=10); code = r.status
            except urllib.error.HTTPError as e:
                code = e.code
            check(code == 404, f"no file, not the route: {code}")
            check(len(GOT) == 1, f"only the good one reached Discord: {len(GOT)}")
        finally:
            if os.name == "nt":
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
                time.sleep(1)
            else:
                proc.terminate()
    print("FAILED: " + "; ".join(fails) if fails else "all ok")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
