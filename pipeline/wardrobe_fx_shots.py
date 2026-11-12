"""Effect QA shots on a virtual clock (2026-11-10, the Penguin's QA pass): like wardrobe_fx_probe.py (camera views, a pool
forced to one skill, props worn, each live effect's world box in the hero's frame), but the page's one THREE.Clock is
replaced by a fixed step (1/30 s a frame, 0 once the asked time is reached), so every shot and box is taken at exactly the
clip time asked, however slowly swiftshader draws (the probe's real-time samples could land 10 s late on a heavy effect).
The tile is played once first at a coarse step so its files and textures are loaded, then again for the shots. Each
sample also prints how many hero meshes are drawn / hidden (heroHide, a skin's copies) and the live effects' opacity.
  uv run --no-project --with playwright python -I pipeline/wardrobe_fx_shots.py <repo> <out dir> <cls> <tile>
      <t1,t2,...> [side|front|back|far|top|near|book|spot|bookside|bookback|behind, several joined by ,] [<cue key>=<skill> | <cue key>!<roll> | <cue key>%<effect>, several joined by +] [<props JSON>]
(<cue key>!<roll>: that roll always comes up, e.g. ko!dead for the KO tile's deadEffect; cast3=iceBlock+cast3!doubleSpell.)
(<cue key>%<effect>: that effect's chance cues (a "p" with no roll) always fire, e.g. anchorYank%tto/dropAnchor_shrapnel; 2026-11-13, the Cat's QA.)
Shots: <out>/<cls>_<tile>_<view>_<t>[_skill][_white][_prop...].png (dark backdrop; the environment variable BG=white keeps the page's white
stage). One browser.
  ... wardrobe_fx_shots.py <repo> <out dir> <cls> --jobs <jobs.json>   (2026-11-13, the Penguin's QA pass): several tiles in
      one browser, a fresh context and page for each; jobs.json = [[tile, "t1,t2", view, force, {props}], ...] (the last three
      optional, as the arguments above); the console errors are printed per job.
SEED=<n> (environment) seeds Math.random (repeatable only as far as the page's own call order is: the loads are async);
PARTS=1 also lists each drawn part of the live effects (node, material, vertices, box, indices behind the camera / off
screen / NaN); HIDE=<regex>
hides the parts whose "<effect>/<node>#<n>/<material>" matches (n: the part's number in the listing) before each shot (to find which part draws what)."""
import asyncio, functools, http.server, json, os, sys, threading
from pathlib import Path

ROOT, OUT, CLS = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
if sys.argv[4] == "--jobs":
    JOBS = json.loads(Path(sys.argv[5]).read_text(encoding="utf-8"))
else:
    JOBS = [sys.argv[4:9]]
JOBS = [(j[0], [float(x) for x in str(j[1]).split(",")], j[2] if len(j) > 2 and j[2] else "side", j[3] if len(j) > 3 else "",
         (json.loads(j[4]) if isinstance(j[4], str) else j[4]) if len(j) > 4 else {}) for j in JOBS]
OUT.mkdir(parents=True, exist_ok=True)


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


http.server.ThreadingHTTPServer.request_queue_size = 128
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/wardrobe/index.html" + ("" if os.environ.get("BG") == "white" else "?fxbg=dark")   # BG=white: the page's white stage
CAMS = {"side": ([20, 6, 5], [0, 1, 0]), "front": ([0, 3, 18], [0, 1, 0]), "back": ([0, 4, -10], [0, 1, 0]), "far": ([-8, 4, 20], [0, 1, 0]),
        "book": ([3, 3.5, 15.5], [0, 1, 0]), "bookside": ([8, 3.5, 11], [0, 1, 0]), "bookback": ([-2, 4, 5], [0, 1, 0]),
        "spot": ([5, 3, 17], [0, 1, 0]), "top": ([0.01, 22, 5], [0, 0, 5]), "near": ([4, 2, 4], [0, 1, 0]),
        "behind": ([0, 11, -10], [0, 0, 9])}   # behind and above: the 10 m target area and +-10 m around it
CLOCK = """() => { const { THREE } = wardrobe.debug(), P = THREE.Clock.prototype;
  if (P.__virtual) return; P.__virtual = true; const real = P.getDelta;
  window.__v = { t: 0, target: 0, step: 1 / 30 };
  P.getDelta = function () { real.call(this); const v = window.__v;
    if (v.t + 1e-9 < v.target) { const s = Math.min(v.step, v.target - v.t); v.t += s; return s; } return 0; }; }"""
CAM = """([p, t]) => { const { camera, controls, C, THREE } = wardrobe.debug();
  const hq = new THREE.Quaternion(); C.root.getWorldQuaternion(hq); const hp = new THREE.Vector3(); C.root.getWorldPosition(hp);
  controls.maxDistance = 200; controls.minDistance = 0.1; controls.enableDamping = false;
  camera.position.copy(new THREE.Vector3(...p).applyQuaternion(hq).add(hp));
  controls.target.copy(new THREE.Vector3(...t).applyQuaternion(hq).add(hp)); controls.update(); }"""
STATE = """() => { const { FX, THREE, C } = wardrobe.debug(); const hp = new THREE.Vector3(); C.root.getWorldPosition(hp);
  const hq = new THREE.Quaternion(); C.root.getWorldQuaternion(hq); const inv = hq.clone().invert();
  let drawn = 0, hidden = 0, copies = 0;
  C.root.traverse(o => { if (!o.isMesh) return; if (o.userData.lookCopy) { if (o.layers.mask) copies++; return; }
    if (o.userData.hoverOverlay) return; if (o.layers.mask & 1) drawn++; else hidden++; });
  const fx = FX.live.map(f => { const b = new THREE.Box3(), ops = new Set(); f.group.updateMatrixWorld(true);
    f.group.traverse(o => { if ((o.isMesh || o.isLine || o.isPoints) && o.geometry?.attributes.position?.count && o.visible) {
      o.geometry.computeBoundingBox(); const bb = o.geometry.boundingBox.clone();
      if (!bb.isEmpty()) b.union(bb.applyMatrix4(o.matrixWorld));
      for (const m of [].concat(o.material || [])) ops.add(m.opacity.toFixed(2)); } });
    const age = f.age != null ? ` age ${f.age.toFixed(2)}` : '';
    if (b.isEmpty()) return f.name + age + ': (nothing drawn)';
    const lo = b.min.clone().sub(hp).applyQuaternion(inv), hi = b.max.clone().sub(hp).applyQuaternion(inv);
    const mn = lo.clone().min(hi), mx = lo.clone().max(hi), r = v => v.toArray().map(x => x.toFixed(2)).join(',');
    return `${f.name}${age}: min(${r(mn)}) max(${r(mx)}) op ${[...ops].slice(0, 6).join('/')}`; });
  return { t: window.__v.t, FXt: FX.t, hero: `hero meshes drawn ${drawn}, hidden ${hidden}, skin copies drawn ${copies}`, fx }; }"""

# the drawn parts of the live effects, in the hero's frame (PARTS=1), and hiding some of them (HIDE=<regex>)
PART_WALK = """const { FX, THREE, C } = wardrobe.debug(); const hp = new THREE.Vector3(); C.root.getWorldPosition(hp);
  const inv = C.root.getWorldQuaternion(new THREE.Quaternion()).invert(), out = [];
  for (const f of FX.live) { f.group.updateMatrixWorld(true); f.group.traverse(o => {
    if (!(o.isMesh || o.isLine || o.isPoints) || !o.visible || !o.geometry?.attributes.position?.count) return;
    const mat = [].concat(o.material || [])[0], node = o.name || o.parent?.name || '?', id = `${f.name}/${node}#${out.length}/${mat?.name || mat?.type || '-'}`;
    out.push([o, id]); }); }"""
PARTS = "() => { " + PART_WALK + """
  return out.map(([o, id]) => { o.geometry.computeBoundingBox(); const b = o.geometry.boundingBox.clone().applyMatrix4(o.matrixWorld);
    const lo = b.min.clone().sub(hp).applyQuaternion(inv), hi = b.max.clone().sub(hp).applyQuaternion(inv), r = v => v.toArray().map(x => x.toFixed(2)).join(',');
    const { camera } = wardrobe.debug(), P = o.geometry.attributes.position, I = o.geometry.index, v = new THREE.Vector4(); let behind = 0, far = 0, nan = 0;
    camera.updateMatrixWorld(); const M = camera.projectionMatrix.clone().multiply(camera.matrixWorldInverse).multiply(o.matrixWorld);
    const n = I ? I.count : P.count;
    for (let k = 0; k < n; k++) { const j = I ? I.getX(k) : k; v.set(P.getX(j), P.getY(j), P.getZ(j), 1).applyMatrix4(M);
      if (!Number.isFinite(v.x + v.y + v.z + v.w)) nan++; else if (v.w < camera.near) behind++; else if (Math.abs(v.x / v.w) > 4 || Math.abs(v.y / v.w) > 4) far++; }
    return `${id} v ${P.count} i ${I ? I.count : '-'} min(${r(lo.clone().min(hi))}) max(${r(lo.clone().max(hi))}) indices behind the camera ${behind}, off-screen x4 ${far}, NaN ${nan}`; }); }"""
HIDE = "re => { " + PART_WALK + " for (const [o, id] of out) if (new RegExp(re).test(id)) o.visible = false; }"


async def shoot(page, errors, TILE, TIMES, VIEW, FORCE, SLOTS):
    errors.clear()
    if os.environ.get("SEED"):                    # SEED=<n>: Math.random seeded (mulberry32), the same rolls on every run
        await page.add_init_script("""(() => { let a = %d >>> 0; Math.random = () => { a = (a + 0x6D2B79F5) >>> 0; let t = a;
          t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; })()""" % int(os.environ["SEED"]))
    await page.goto(URL)
    await page.wait_for_function("window.wardrobe && wardrobe.debug().C", timeout=120000)
    await page.evaluate("([c, s]) => wardrobe.show(c, s)", [CLS, SLOTS])
    await page.wait_for_function("c => wardrobe.debug().C?.cls === c && wardrobe.debug().FX.cueTab[c]", arg=CLS, timeout=120000)
    for force in filter(None, FORCE.split("+")):    # several joined by "+": "cast3=iceBlock+cast3!doubleSpell"
        if "=" in force:
            await page.evaluate("""([c, k, s]) => { const e = wardrobe.debug().FX.cueTab[c][k]; e.skills = { [s]: e.skills[s] }; }""", [CLS, *force.split("=")])
        elif "%" in force:                            # "<cue key>%<effect>": that effect's chance cues (p, no roll) always fire
            await page.evaluate("""([c, k, n]) => { const e = wardrobe.debug().FX.cueTab[c][k];
              for (const x of [e, ...Object.values(e.skills || {})]) if (x.cues) x.cues = x.cues
                .map(q => String(q[2]).split("|").includes(n) && q[3]?.p != null ? [q[0], q[1], q[2], { ...q[3], p: undefined }] : q); }""", [CLS, *force.split("%")])
        elif "!" in force:                            # "<cue key>!<roll>": that roll always comes up (its "!roll" cues left out)
            await page.evaluate("""([c, k, r]) => { const e = wardrobe.debug().FX.cueTab[c][k];
              for (const x of [e, ...Object.values(e.skills || {})]) if (x.cues) x.cues = x.cues.filter(q => q[3]?.roll !== "!" + r)
                .map(q => q[3]?.roll === r ? [q[0], q[1], q[2], { ...q[3], p: undefined, roll: undefined }] : q); }""", [CLS, *force.split("!")])
    await page.evaluate(CLOCK)

    async def click():
        if await page.locator('#picker').is_hidden():
            await page.click('button.topic[data-t="move"]')
        for g in ("skill", "emote", "base"):
            if await page.locator(f'.pk-tab[data-g="{g}"]').count():
                await page.click(f'.pk-tab[data-g="{g}"]')
                if await page.locator(f'#pkBody .pk-item[data-m="{TILE}"]').count():
                    break
        await page.click(f'#pkBody .pk-item[data-m="{TILE}"]')
        if await page.locator('#pkClose').count():
            await page.click('#pkClose')

    async def run_to(t, step):
        await page.evaluate("([t, s]) => { window.__v.target = t; window.__v.step = s; }", [t, step])
        try:
            await page.wait_for_function("() => window.__v.t + 1e-9 >= window.__v.target", timeout=120000, polling=50)
        except Exception:                         # the page's render loop died (an exception in a frame stops it)
            print("STALLED at", await page.evaluate("() => window.__v.t"), "errors:", json.dumps(errors[:10], ensure_ascii=False))
            raise

    # warm-up: the files and textures every cue needs, at a coarse step
    await page.evaluate("() => { window.__v.t = 0; window.__v.target = 0; }")
    await click()
    await run_to(max(TIMES) + 1, 0.1)
    # the play the shots are of
    await page.evaluate("() => { window.__v.t = 0; window.__v.target = 0; }")
    await click()
    views = VIEW.split(",")                      # several views ("back,side"): each sample shot from each, one play
    await page.evaluate(CAM, CAMS[views[0]])
    for t in TIMES:
        await run_to(t, 1 / 30)
        await page.evaluate(CAM, CAMS[views[0]])
        await page.wait_for_timeout(120)            # a frame drawn at dt 0 with the camera placed
        if os.environ.get("HIDE"):
            await page.evaluate(HIDE, os.environ["HIDE"])
            await page.wait_for_timeout(120)
        s = await page.evaluate(STATE)
        print(f"-- {TILE} t {s['t']:.3f} (FX.t {s['FXt']:.3f})  {s['hero']}")
        for x in s["fx"]:
            print("   ", x)
        if os.environ.get("PARTS"):
            for x in await page.evaluate(PARTS):
                print("      part", x)
        sk = "".join("_" + f.replace("=", "!").replace("%", "!").split("!")[-1].split("/")[-1] for f in FORCE.split("+") if f)
        bg = ("_white" if os.environ.get("BG") == "white" else "") + "".join("_" + str(v) for v in SLOTS.values())
        for i, view in enumerate(views):
            if i:
                await page.evaluate(CAM, CAMS[view])
                await page.wait_for_timeout(120)
            await page.screenshot(path=str(OUT / f"{CLS}_{TILE.lstrip('@')}_{view}_{t:05.2f}{sk}{bg}.png"))
    print("console:", json.dumps(errors[:40], ensure_ascii=False, indent=0))


async def main():
    from playwright.async_api import async_playwright
    errors = []
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--autoplay-policy=no-user-gesture-required"])
        for job in JOBS:
            print("== job", json.dumps(job, ensure_ascii=False), flush=True)
            ctx = await b.new_context(viewport={"width": 1366, "height": 768})   # a fresh context each job: the page keeps
            page = await ctx.new_page()                                          # the worn look in localStorage
            page.on("pageerror", lambda e: errors.append(str(e) + " @ " + " | ".join((getattr(e, "stack", "") or "").splitlines()[1:4])))
            page.on("console", lambda m: m.type in ("error", "warning") and "GL Driver" not in m.text and errors.append(m.type + ": " + m.text))
            try:
                await shoot(page, errors, *job)
            except Exception as e:                  # a stalled or failed job: report it, go on with the next
                print("JOB FAILED", job[0], repr(e)[:300], "errors:", json.dumps(errors[:10], ensure_ascii=False))
            await ctx.close()
            sys.stdout.flush()
        await b.close()


asyncio.run(main())
