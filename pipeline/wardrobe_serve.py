"""wardrobe.cmd's server: serves this folder on http://127.0.0.1:8771 like `py -3 -m http.server`, and quits once no
wardrobe page is open (user 2026-11-10: "closing the Wardrobe viewport browser closes the server instance together with
it"). Each open page (wardrobe/index.html, tto_picker.html, only on this port) holds /__alive, an event stream; GRACE
seconds after the last one closes (a reload reconnects well within it) the server exits, and its minimised window with
it. Until the first page connects it waits.
  py -3 pipeline/wardrobe_serve.py [port]"""
import functools, http.server, os, sys, threading, time

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8771
GRACE = 10
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lock = threading.Lock()
pages, last_close = 0, None


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global pages, last_close
        if self.path != "/__alive":
            return super().do_GET()
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        with lock:
            pages += 1
        try:
            while True:                  # a comment every 2 s: a closed tab shows up as a failed write
                self.wfile.write(b": alive\n\n")
                self.wfile.flush()
                time.sleep(2)
        except OSError:
            pass
        finally:
            with lock:
                pages -= 1
                last_close = time.monotonic()


def watch():
    while True:
        time.sleep(1)
        with lock:
            if pages == 0 and last_close is not None and time.monotonic() - last_close > GRACE:
                print("no wardrobe page open: server closed", flush=True)
                os._exit(0)


class Server(http.server.ThreadingHTTPServer):
    request_queue_size = 128             # the page loads dozens of files at once (NOTES.md: the 5-deep stdlib queue refused some)


if __name__ == "__main__":
    threading.Thread(target=watch, daemon=True).start()
    with Server(("127.0.0.1", PORT), functools.partial(Handler, directory=ROOT)) as srv:
        print(f"wardrobe server: http://127.0.0.1:{PORT}/wardrobe/ (closes {GRACE} s after the last page)", flush=True)
        srv.serve_forever()
