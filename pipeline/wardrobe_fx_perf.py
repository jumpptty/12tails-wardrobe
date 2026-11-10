"""Effect cost meter (2026-11-10, user: "please fix TTO skills lag ... something might be unoptimized?"). Plays tiles on a
virtual clock (fixed 1/30 s steps, as wardrobe_fx_shots.py) and measures each frame: the time in the page's frame callback
(requestAnimationFrame), the part of it inside renderer.render (draw submission; the rest is the effects' simulation and
the page's JS), WebGL buffers created / deleted, bytes uploaded (bufferData / bufferSubData), the GPU geometries three
keeps (renderer.info.memory) and the JS heap. A frame's numbers are the frame callback's; swiftshader's own drawing runs
elsewhere and is not in them, so the CPU side is what this compares (before / after a change, same tiles, same machine).
  uv run --no-project --with playwright python -I pipeline/wardrobe_fx_perf.py <repo> <cls> <tile>[,<tile>...] [seconds=4] [--profile] [--real] [--gpu] [--baseline]
Prints one line per tile; exits 1 on a page error."""
import asyncio, functools, http.server, json, sys, threading
from pathlib import Path

ROOT, CLS, TILES = Path(sys.argv[1]), sys.argv[2], sys.argv[3].split(",")
SECS = float(sys.argv[4]) if len(sys.argv) > 4 else 4.0
PROFILE = "--profile" in sys.argv               # also Chrome's CPU profile of the measured play: the hottest functions
REAL = "--real" in sys.argv                     # real time instead of the virtual clock: frames a second and the worst gap,
                                                # the first play of each tile included (shader compiles happen there)
GPU = "--gpu" in sys.argv                       # the PC's own GPU (ANGLE on D3D11) instead of swiftshader
BASELINE = "--baseline" in sys.argv             # serve the page with the old setMesh (for a before / after comparison)
OLD_SETMESH = """function setMesh(m, pos, col, uv, idx) {
  const g = m.geometry;
  g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute("color", new THREE.Float32BufferAttribute(col, 4));
  g.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2));
  g.setIndex(idx);
}
"""


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


http.server.ThreadingHTTPServer.request_queue_size = 128
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/wardrobe/index.html?fxbg=dark"

# before the page's scripts: count the GL buffer calls and time every frame callback
INIT = """(() => {
  const S = window.__perf = { on: false, frames: 0, frameMs: [], create: 0, del: 0, bytes: 0, renderMs: 0 };
  for (const C of [window.WebGL2RenderingContext, window.WebGLRenderingContext].filter(Boolean)) {
    const P = C.prototype, cb = P.createBuffer, db = P.deleteBuffer, bd = P.bufferData, bs = P.bufferSubData;
    P.createBuffer = function () { if (S.on) S.create++; return cb.apply(this, arguments); };
    P.deleteBuffer = function () { if (S.on) S.del++; return db.apply(this, arguments); };
    P.bufferData = function (t, d) { if (S.on && d && d.byteLength) S.bytes += d.byteLength; return bd.apply(this, arguments); };
    P.bufferSubData = function (t, o, d, so, len) { if (S.on && d) S.bytes += len ? len * (d.BYTES_PER_ELEMENT || 1) : d.byteLength; return bs.apply(this, arguments); };
  }
  const raf = window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame = f => raf(t => { const a = performance.now(); try { f(t); } finally {
    if (S.on) { S.frames++; S.frameMs.push(performance.now() - a); } } });
})();"""
CLOCK = """() => { const { THREE, renderer } = wardrobe.debug(), P = THREE.Clock.prototype, S = window.__perf;
  if (P.__virtual) return; P.__virtual = true; const real = P.getDelta;
  window.__v = { t: 0, target: 0, step: 1 / 30 };
  P.getDelta = function () { real.call(this); const v = window.__v;
    if (v.t + 1e-9 < v.target) { const s = Math.min(v.step, v.target - v.t); v.t += s; return s; } return 0; };
  const r = renderer.render.bind(renderer);
  renderer.render = (a, b) => { const t = performance.now(); r(a, b); if (S.on) S.renderMs += performance.now() - t; }; }"""


async def main():
    from playwright.async_api import async_playwright
    errors = []
    async with async_playwright() as p:
        gl = ["--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"] if GPU else ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"]
        b = await p.chromium.launch(args=gl + ["--autoplay-policy=no-user-gesture-required", "--disable-gpu-vsync", "--disable-frame-rate-limit"])
        page = await b.new_page(viewport={"width": 1366, "height": 768})
        page.on("pageerror", lambda e: errors.append(str(e)))
        await page.add_init_script(INIT)
        if BASELINE:                                    # the page as before 2026-11-10's fix: new buffers every frame
            async def old_page(route):
                r = await route.fetch(); s = await r.text()
                a = s.index("function setMesh(m, pos, col, uv, idx, nrm) {"); b = s.index("\n}\n", a) + 3
                s = s[:a] + OLD_SETMESH + s[b:]
                await route.fulfill(response=r, body=s)
            async def old_shuriken(route):
                r = await route.fetch(); s = await r.text()
                s = s.replace("api.setMesh(mesh, pos, col, uvs, idx, nrm);",
                              'api.setMesh(mesh, pos, col, uvs, idx); mesh.geometry.setAttribute("normal", new THREE.Float32BufferAttribute(nrm, 3));')
                await route.fulfill(response=r, body=s)
            await page.route("**/wardrobe/index.html*", old_page)
            await page.route("**/fxparts/shuriken.js*", old_shuriken)
        await page.goto(URL)
        await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
        print("GL:", await page.evaluate("""() => { const g = wardrobe.debug().renderer.getContext(), e = g.getExtension('WEBGL_debug_renderer_info');
          return e ? g.getParameter(e.UNMASKED_RENDERER_WEBGL) : g.getParameter(g.RENDERER); }"""), flush=True)
        await page.evaluate("c => wardrobe.show(c, {})", CLS)
        await page.wait_for_function("c => wardrobe.debug().C?.cls === c && wardrobe.debug().FX.cueTab[c]", arg=CLS, timeout=120000)
        async def click(tile):
            if await page.locator('#picker').is_hidden():
                await page.click('button.topic[data-t="move"]')
            for g in ("skill", "emotion", "base"):
                if await page.locator(f'.pk-tab[data-g="{g}"]').count():
                    await page.click(f'.pk-tab[data-g="{g}"]')
                    if await page.locator(f'#pkBody .pk-item[data-m="{tile}"]').count():
                        break
            await page.click(f'#pkBody .pk-item[data-m="{tile}"]')

        if REAL:
            for tile in TILES:
                for k in ("first", "again"):
                    await page.evaluate("() => Object.assign(window.__perf, { on: true, frames: 0, frameMs: [], ts: [], create: 0, del: 0, bytes: 0, renderMs: 0 })")
                    await page.evaluate("""() => { const S = window.__perf; const tick = t => { if (!S.on) return; S.ts.push(t); requestAnimationFrame(tick); }; requestAnimationFrame(tick); }""")
                    await click(tile)
                    await page.wait_for_timeout(int(SECS * 1000))
                    s = await page.evaluate("""() => { const S = window.__perf; S.on = false; const g = [];
                      for (let i = 1; i < S.ts.length; i++) g.push(S.ts[i] - S.ts[i - 1]);
                      const f = S.frameMs.slice().sort((a, b) => a - b), n = f.length || 1;
                      return { fps: g.length / ((S.ts.at(-1) - S.ts[0]) / 1000 || 1), worst: Math.max(0, ...g), over50: g.filter(x => x > 50).length,
                        js: f.reduce((a, b) => a + b, 0) / n, create: S.create, programs: wardrobe.debug().renderer.info.programs.length }; }""")
                    print(f"{CLS} {tile} ({k} play, real time): {s['fps']:.0f} fps, worst gap {s['worst']:.0f} ms, {s['over50']} gaps over 50 ms, "
                          f"frame JS {s['js']:.1f} ms, GL buffers created {s['create']}, shader programs {s['programs']}", flush=True)
            await b.close()
            if errors:
                print("page errors:", json.dumps(errors[:10], ensure_ascii=False)); sys.exit(1)
            return
        await page.evaluate(CLOCK)

        async def run(secs, step):
            await page.evaluate("([t, s]) => { window.__v.t = 0; window.__v.target = t; window.__v.step = s; }", [secs, step])
            await page.wait_for_function("() => window.__v.t + 1e-9 >= window.__v.target", timeout=600000, polling=50)

        for tile in TILES:
            await click(tile)                       # warm-up: files and textures loaded, shaders compiled
            await run(SECS, 0.1)
            await click(tile)
            await page.evaluate("() => Object.assign(window.__perf, { on: true, frames: 0, frameMs: [], create: 0, del: 0, bytes: 0, renderMs: 0 })")
            if PROFILE:
                cdp = await page.context.new_cdp_session(page)
                await cdp.send("Profiler.enable"); await cdp.send("Profiler.setSamplingInterval", {"interval": 200})
                await cdp.send("Profiler.start")
            await run(SECS, 1 / 30)
            if PROFILE:                                 # self time per function, the top 15
                prof = (await cdp.send("Profiler.stop"))["profile"]
                dt = dict(zip(prof["samples"], prof["timeDeltas"]))
                self_t = {}
                for n in prof["nodes"]:
                    f = n["callFrame"]
                    key = f"{f['functionName'] or '(anon)'} {f['url'].rsplit('/', 1)[-1]}:{f['lineNumber'] + 1}"
                    self_t[key] = self_t.get(key, 0) + n.get("hitCount", 0)
                tot = sum(self_t.values()) or 1
                print("   profile (share of samples, self time):", "; ".join(f"{100 * v / tot:.1f}% {k}" for k, v in
                      sorted(self_t.items(), key=lambda x: -x[1])[:15]), flush=True)
            s = await page.evaluate("""() => { const S = window.__perf; S.on = false; const { renderer } = wardrobe.debug();
              const f = S.frameMs.slice().sort((a, b) => a - b), n = f.length || 1, sum = f.reduce((a, b) => a + b, 0);
              return { frames: S.frames, mean: sum / n, p95: f[Math.floor(0.95 * (n - 1))] || 0, render: S.renderMs / n,
                create: S.create, del: S.del, mb: S.bytes / 1048576, geoms: renderer.info.memory.geometries,
                heap: performance.memory ? performance.memory.usedJSHeapSize / 1048576 : 0 }; }""")
            top = await page.evaluate("""() => { const { FX } = wardrobe.debug(), out = [];
              for (const f of FX.live) f.group.traverse(o => { const n = o.geometry?.attributes?.position?.count;
                if (n) out.push([n, f.name + " / " + (o.parent?.name || "?")]); });
              return out.sort((a, b) => b[0] - a[0]).slice(0, 6); }""")
            print(f"{CLS} {tile}: {s['frames']} frames, frame {s['mean']:.1f} ms (p95 {s['p95']:.1f}), of it render {s['render']:.1f} ms; "
                  f"GL buffers created {s['create']} / deleted {s['del']} ({s['create'] / max(1, s['frames']):.0f} a frame), "
                  f"uploaded {s['mb']:.1f} MB, geometries {s['geoms']}, heap {s['heap']:.0f} MB", flush=True)
            print("   largest meshes at the end (vertices, effect / node):", "; ".join(f"{n} {w}" for n, w in top), flush=True)
        await b.close()
    if errors:
        print("page errors:", json.dumps(errors[:10], ensure_ascii=False))
        sys.exit(1)


asyncio.run(main())
