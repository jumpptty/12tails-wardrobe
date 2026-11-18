r"""Mocks for the user's pick of the pet camera and the pet block's place (user 2026-11-18, the pets plan's Task 6).

  uv run --no-project --with UnityPy --with pillow --with numpy --with playwright python -I pipeline/wardrobe_pet_mocks.py
        [--reextract] [--only smallAnubi,kiteChula] [--no-shots]

Writes checks/pet_mocks/ (git-ignored): index.html (the page to open), the shots, pets/ (the extracted meshes and textures).
Nothing of wardrobe/index.html is changed: the REAL page is opened in headless Playwright, a pet's mesh is put into its
scene by page.evaluate (wardrobe.debug() gives THREE, scene, camera, controls, C), and the camera is fitted the way
heroFitPose() fits the hero, only to the union of the hero's box and the pet's box and in another direction.

Pets (the plan's provisional sizes; static: the prefab's pose, no idle clip):
  smallAnubi (0, 0, -1.0) x1.8 | miniMokBug (0, 0, -2.0) x1.8 | kiteChula (0, 0.8, 0) x1.0 (ParentPosition, the Sheep's
  offset_sheep y) | momBalloon (0, 0, -1.0) + offset_sheep x1.0 (its PetControl's offset_sheep is 0, 0, 0).
Meshes: TTO 2026-11-04's bundles (12tails-video/tto_assets/2026-11-04/dec, read only), the prefab's renderers; a skinned
mesh is skinned by its own bones' prefab pose (wardrobe_tot.py's prop_nodes), then x -> -x and the winding follows the
normals (wardrobe_data.py's prop_mesh). The Sheep in its standard outfit (the page's first-visit look) is the hero.
"""
import asyncio, functools, http.server, json, os, sys, threading
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "checks" / "pet_mocks"
PETS_DIR = OUT / "pets"
ASSETS = ROOT.parent / "12tails-video" / "tto_assets" / "2026-11-04"
if not ASSETS.is_dir():
    ASSETS = Path(r"D:\12tails-video\tto_assets\2026-11-04")
argv = sys.argv[1:]
ONLY = set(argv[argv.index("--only") + 1].split(",")) if "--only" in argv else None

# prefab -> catalog container key, where it stands in the hero's space (three.js, the hero faces +z), scale
PETS = {
    "smallAnubi": dict(key="7cf64f17054b2be4d8e7f51aab455b0b", name="Small Anubi", code="sab", at=[0, 0, -1.0], scale=1.8,
                       spot="หลังตัวละคร 1.0 ม. · ขนาด Lv 9 (×1.8)"),
    "miniMokBug": dict(key="3b808c6ec8af0714eb40c26cd2068c56", name="Mini Mok Bug", code=None, at=[0, 0, -2.0], scale=1.8,
                       spot="หลังตัวละคร 2.0 ม. · ขนาด Lv 9 (×1.8)"),
    "kiteChula": dict(key="ce46c1fa535c68642b7152e6a96537b5", name="Kite Chula", code=None, at=[0, 0.8, 0], scale=1.0,
                      spot="ติดตัวละคร สูงขึ้น 0.8 ม. (ว่าวลอยเหนือหัว)"),
    "momBalloon": dict(key="d0e31b4f269ce2446b32c1db088ae8d3", name="Mom Balloon", code=None, at=[0, 0, -1.0], scale=1.0,
                       spot="หลังตัวละคร 1.0 ม. (ลอยตามหลัง)"),
}


# ---------------------------------------------------------------------------------------------------- extraction
def extract():
    import numpy as np
    import UnityPy
    from UnityPy.helpers.MeshHelper import MeshHandler

    P = lambda c: c.component if hasattr(c, "component") else c[1]
    dec = ASSETS / "dec"
    env = UnityPy.load(*[str(dec / f) for f in sorted(os.listdir(dec)) if f.endswith(".bundle")])
    container = dict(env.container.items())
    PETS_DIR.mkdir(parents=True, exist_ok=True)

    def comp(go, typ):
        return next((P(c).read() for c in go.m_Component if P(c).type.name == typ), None)

    def mat4(tr):
        p, q, s = tr.m_LocalPosition, tr.m_LocalRotation, tr.m_LocalScale
        x, y, z, w = q.x, q.y, q.z, q.w
        R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                      [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                      [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
        M = np.eye(4)
        M[:3, :3] = R * np.array([s.x, s.y, s.z])
        M[:3, 3] = [p.x, p.y, p.z]
        return M

    def texture(mat_ptr, tag):
        """{tex: png file name or None, color} of a material's _MainTex / _Color."""
        tex, color = None, [1, 1, 1, 1]
        try:
            m = mat_ptr.read()
            for k, v in m.m_SavedProperties.m_TexEnvs:
                if k == "_MainTex" and v.m_Texture.m_PathID:
                    t = v.m_Texture.read()
                    fn = f"{tag}_{t.m_Name}.png"
                    if not (PETS_DIR / fn).exists():
                        t.image.save(PETS_DIR / fn)
                    tex = fn
            for k, v in m.m_SavedProperties.m_Colors:
                if k == "_Color":
                    color = [round(v.r, 3), round(v.g, 3), round(v.b, 3), round(v.a, 3)]
        except Exception as e:
            print(f"    material: {type(e).__name__}: {e}")
        return {"tex": tex, "color": color}

    def mesh_arrays(h, pos, nrm):
        """x mirrored; the winding follows the normals (wardrobe_data.py prop_mesh)."""
        pos = np.array(pos, float) * [-1, 1, 1]
        nrm = None if nrm is None else np.array(nrm, float) * [-1, 1, 1]
        subs = h.get_triangles()
        tris = np.array([t for sub in subs for t in sub], int).reshape(-1, 3)
        flip = True
        if nrm is not None and len(tris):
            cr = np.cross(pos[tris[:, 1]] - pos[tris[:, 0]], pos[tris[:, 2]] - pos[tris[:, 0]])
            flip = ((cr * (nrm[tris[:, 0]] + nrm[tris[:, 1]] + nrm[tris[:, 2]])).sum(1) > 0).sum() < len(tris) / 2
        if flip:
            tris = tris[:, [0, 2, 1]]
        groups, k = [], 0
        for si, sub in enumerate(subs):
            groups.append([k * 3, len(sub) * 3, si])
            k += len(sub)
        return {"pos": [round(float(x), 5) for x in pos.ravel()],
                "nrm": None if nrm is None else [round(float(x), 4) for x in nrm.ravel()],
                "uv": [round(float(x), 5) for v in h.m_UV0 for x in v[:2]] if h.m_UV0 else None,
                "idx": [int(x) for x in tris.ravel()], "groups": groups}

    for pet, spec in PETS.items():
        if ONLY and pet not in ONLY:
            continue
        go = container[spec["key"]].read()
        # the prefab's tree, each node's matrix relative to the prefab root (the root's own TRS is the page's to place)
        T = []

        def walk(tr, parent):
            k = len(T)
            T.append((tr.m_GameObject.read(), tr, parent))
            for ch in tr.m_Children:
                walk(ch.read(), k)
        walk(next(P(c) for c in go.m_Component if P(c).type.name == "Transform").read(), -1)
        world = []
        for g, tr, parent in T:
            world.append(np.eye(4) if parent < 0 else world[parent] @ mat4(tr))
        by_name = {g.m_Name: i for i, (g, _, _) in enumerate(T)}
        meshes = []
        for k, (g, tr, parent) in enumerate(T):
            if not g.m_IsActive:
                continue
            mf, mr, smr = comp(g, "MeshFilter"), comp(g, "MeshRenderer"), comp(g, "SkinnedMeshRenderer")
            if mf and mr and mf.m_Mesh.m_PathID:
                h = MeshHandler(mf.m_Mesh.read())
                h.process()
                V = np.array(h.m_Vertices, float)
                W = (np.c_[V, np.ones(len(V))] @ world[k].T)[:, :3]
                N = None
                if h.m_Normals:
                    N = np.array(h.m_Normals, float) @ np.linalg.inv(world[k][:3, :3])
                    N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-9
                d = mesh_arrays(h, W, N)
                d["mats"] = [texture(m, pet) for m in mr.m_Materials]
                d["node"] = g.m_Name
                meshes.append(d)
            if smr and smr.m_Mesh.m_PathID:
                m = smr.m_Mesh.read()
                h = MeshHandler(m)
                h.process()
                bones = [b.read().m_GameObject.read().m_Name for b in smr.m_Bones]
                V = np.array(h.m_Vertices, float)
                Wt, J = np.array(h.m_BoneWeights, float), np.array(h.m_BoneIndices, int)
                Nn = np.array(h.m_Normals, float) if h.m_Normals else None
                if not bones or not len(Wt):
                    W = (np.c_[V, np.ones(len(V))] @ world[k].T)[:, :3]
                    N = None if Nn is None else Nn @ np.linalg.inv(world[k][:3, :3])
                else:
                    B = [world[by_name[b]] if b in by_name else np.eye(4) for b in bones]
                    bp = [np.array([[getattr(b, f"e{r}{c}") for c in range(4)] for r in range(4)]) for b in m.m_BindPose]
                    W, N = np.zeros_like(V), (np.zeros_like(V) if Nn is not None else None)
                    for i in range(len(bones)):
                        M = B[i] @ bp[i]
                        w = (Wt * (J == i)).sum(1)[:, None]
                        W += w * (np.c_[V, np.ones(len(V))] @ M.T)[:, :3]
                        if N is not None:
                            N += w * (Nn @ np.linalg.inv(M[:3, :3]))
                if N is not None:
                    N = N / (np.linalg.norm(N, axis=1, keepdims=True) + 1e-9)
                d = mesh_arrays(h, W, N)
                d["mats"] = [texture(mm, pet) for mm in smr.m_Materials]
                d["node"] = g.m_Name
                meshes.append(d)
        pc = next((P(c).read_typetree() for c in go.m_Component if P(c).type.name == "MonoBehaviour"), {})
        out = {"pet": pet, "meshes": meshes, "rootMatrix": mat4(T[0][1]).tolist(),
               "petControl": {k: v for k, v in pc.items() if k in ("followType", "followDistance", "offset_sheep")}}
        (PETS_DIR / f"{pet}.json").write_text(json.dumps(out), encoding="utf-8")
        allp = np.array([x for m in meshes for x in m["pos"]]).reshape(-1, 3)
        print(pet, "meshes", [(m["node"], len(m["pos"]) // 3, [t["tex"] for t in m["mats"]]) for m in meshes],
              "bbox", allp.min(0).round(2).tolist(), allp.max(0).round(2).tolist(), "petControl", out["petControl"])




# ---------------------------------------------------------------------------------------------------- the page's side
# window.__pm: loads a pet into the page's scene, fits the camera to the hero + pet like heroFitPose() (index.html ~4001),
# measures the pet's projection. Everything reads the page's own THREE / scene / camera through wardrobe.debug().
PM_JS = r"""
window.__pm = (() => {
  const dbg = () => wardrobe.debug();
  const FIT_DIR = () => { const { THREE } = dbg(); return new THREE.Vector3(.48, .1, 2.55).normalize(); };
  const stage = document.getElementById("stage");
  const isPhone = () => matchMedia("(max-width: 760px)").matches;
  function vbox(root, THREE) {                       // the page's visibleBox(root, false)
    const box = new THREE.Box3(), v = new THREE.Vector3();
    root.updateMatrixWorld(true);
    root.traverseVisible(o => { if (!o.isMesh) return; const n = o.geometry.attributes.position.count;
      for (let i = 0; i < n; i++) box.expandByPoint(o.getVertexPosition(i, v).applyMatrix4(o.matrixWorld)); });
    return box;
  }
  function heroBox() {                               // heroFitPose()'s box: the body and the worn pieces, clamped
    const { C, THREE } = dbg();
    C.mixer.update(0); C.root.updateMatrixWorld(true);
    const body = new THREE.Box3();
    for (const m of C.meshes) body.union(vbox(m, THREE));
    if (body.isEmpty()) body.setFromCenterAndSize(new THREE.Vector3(0, .5, 0), new THREE.Vector3(.5, 1, .5));
    const h0 = Math.max(body.max.y - body.min.y, 0.5), box = body.clone();
    for (const o of Object.values(C.props)) box.union(vbox(o, THREE));
    box.intersect(new THREE.Box3(body.min.clone().add(new THREE.Vector3(-h0 * .4, -h0 * .05, -h0 * .4)), body.max.clone().add(new THREE.Vector3(h0 * .4, h0 * .65, h0 * .4))));
    return { box, h0 };
  }
  function petBox() {
    const { C, THREE } = dbg(), g = C.root.getObjectByName("pet");
    return g ? vbox(g, THREE) : null;
  }
  // heroFitPose() with a direction of its own and an optional second box (the pet's): the same 78 % / 85 % start, then
  // pulled back until every corner of the box (and the contact shadow's near edge) is inside the stage with the
  // toolbar band clear. The width of the start is the box's extent across the view (heroFitPose's is its x extent)
  function fit(dir, withPet) {
    const { C, THREE, camera } = dbg();
    const hb = heroBox(), h0 = hb.h0, box = hb.box.clone();
    if (withPet) { const pb = petBox(); if (pb) box.union(pb); }
    const vw = stage.clientWidth, vh = stage.clientHeight;
    const c = box.getCenter(new THREE.Vector3()), h = Math.max(box.max.y - box.min.y, 0.5), target = new THREE.Vector3(c.x, c.y - h * .01, c.z);
    const t = Math.tan(camera.fov * Math.PI / 360), right = new THREE.Vector3(dir.z, 0, -dir.x).normalize();
    const cs = []; for (const x of [box.min.x, box.max.x]) for (const y of [box.min.y, box.max.y]) for (const z of [box.min.z, box.max.z]) cs.push(new THREE.Vector3(x, y, z));
    const ex = cs.map(p => p.dot(right)), wide = Math.max(...ex) - Math.min(...ex);
    let d = Math.max(h / (2 * t * .78), wide / (2 * t * (vw / vh) * .85));
    const cam = camera.clone(); cam.clearViewOffset(); cam.updateProjectionMatrix();
    const bar = document.querySelector(".bar").getBoundingClientRect().bottom - stage.getBoundingClientRect().top;
    const top = Math.max(64, bar + 8), foot = vh - 12, dy = isPhone() ? 22 : 0, v = new THREE.Vector3();
    const pts = cs.slice(); pts.push(new THREE.Vector3(c.x, 0, c.z + h0 * .26));
    const fits = dd => { cam.position.copy(target).addScaledVector(dir, dd); cam.lookAt(target); cam.updateMatrixWorld();
      return pts.every(p => { v.copy(p).project(cam); const y = (1 - v.y) / 2 * vh + dy, x = (v.x + 1) / 2 * vw; return y >= top && y <= foot && x >= 6 && x <= vw - 6; }); };
    if (!fits(d)) {
      let lo = d, hi = d * 1.25;
      for (let i = 0; i < 12 && !fits(hi); i++) { lo = hi; hi *= 1.25; }
      for (let i = 0; i < 20; i++) { const m = (lo + hi) / 2; if (fits(m)) hi = m; else lo = m; }
      d = hi;
    }
    return { pos: target.clone().addScaledVector(dir, d), target, d, h };
  }
  function dirOf(turnDeg, rise) {                    // yaw from +z towards +x, rise = y over the horizontal length
    const { THREE } = dbg(), a = turnDeg * Math.PI / 180;
    return new THREE.Vector3(Math.sin(a), rise, Math.cos(a)).normalize();
  }
  function aim(dir, withPet) {
    const { camera, controls, renderer, scene } = dbg(), f = fit(dir, withPet);
    controls.enableDamping = false;
    camera.position.copy(f.pos); controls.target.copy(f.target); controls.update(); camera.updateMatrixWorld();
    renderer.render(scene, camera);
    return { pos: f.pos.toArray(), d: f.d };
  }
  async function loadPet(data, spec) {
    const { C, THREE } = dbg();
    C.root.getObjectByName("pet")?.removeFromParent();
    const g = new THREE.Group(); g.name = "pet";
    const tl = new THREE.TextureLoader();
    for (const m of data.meshes) {
      const geo = new THREE.BufferGeometry();
      geo.setAttribute("position", new THREE.Float32BufferAttribute(m.pos, 3));
      if (m.nrm) geo.setAttribute("normal", new THREE.Float32BufferAttribute(m.nrm, 3)); else geo.computeVertexNormals();
      if (m.uv) geo.setAttribute("uv", new THREE.Float32BufferAttribute(m.uv, 2));
      geo.setIndex(m.idx);
      for (const [a, b, mi] of m.groups) geo.addGroup(a, b, mi);
      const mats = [];
      for (const mm of m.mats) {                     // the page's prop material: Lambert, both sides, cut at 0.5
        const mat = new THREE.MeshLambertMaterial({ color: new THREE.Color(mm.color[0], mm.color[1], mm.color[2]), side: THREE.DoubleSide, alphaTest: .5 });
        if (mm.tex) { const t = await tl.loadAsync("/checks/pet_mocks/pets/" + mm.tex); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; mat.map = t; }
        mats.push(mat);
      }
      g.add(new THREE.Mesh(geo, mats.length ? mats : mats[0]));
    }
    g.position.fromArray(spec.at); g.scale.setScalar(spec.scale);
    C.root.add(g); g.updateMatrixWorld(true);
    const b = vbox(g, THREE);
    return { min: b.min.toArray(), max: b.max.toArray() };
  }
  function petShown(on) { const g = dbg().C.root.getObjectByName("pet"); if (g) g.visible = on; dbg().renderer.render(dbg().scene, dbg().camera); }
  function project() {                               // the pet's vertices on the stage, CSS px from the stage's corner
    const { C, THREE, camera } = dbg(), g = C.root.getObjectByName("pet"), vw = stage.clientWidth, vh = stage.clientHeight;
    camera.updateMatrixWorld(); g.updateMatrixWorld(true);
    let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; const v = new THREE.Vector3();
    g.traverse(o => { if (!o.isMesh) return; const n = o.geometry.attributes.position.count;
      for (let i = 0; i < n; i++) { o.getVertexPosition(i, v).applyMatrix4(o.matrixWorld).project(camera);
        const x = (v.x + 1) / 2 * vw, y = (1 - v.y) / 2 * vh; x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); } });
    return { x0, y0, x1, y1, vw, vh };
  }
  function freeze() {
    const { C, controls } = dbg(); C.mixer.timeScale = 0; controls.enableDamping = false;
    return { pos: dbg().camera.position.toArray(), target: controls.target.toArray() };
  }
  return { fit, aim, dirOf, loadPet, petShown, project, freeze, FIT_DIR: () => FIT_DIR().toArray(), heroOnly: () => { const d = FIT_DIR(), f = fit(d, false); return { pos: f.pos.toArray(), target: f.target.toArray() }; } };
})();
"""

TURNS, RISES = (30, 40, 55), (0.10, 0.25)
TODAY_TURN, TODAY_RISE = 10.66, 0.0385            # FIT_DIR (.48, .1, 2.55): atan(.48/2.55) deg, .1 / hypot(.48, 2.55)


def label(turn, rise):
    return f"หมุน {turn}° · เงย {rise:.2f}"


# ---------------------------------------------------------------------------------------------------- panel variants
# the pet block is a clone of the อาวุธ / ประดับ button (same classes), so the page's CSS lays it out
CSS = {
    "today": "",
    # A: right after ประดับ in the same row: three blocks across (4 of the 12 columns each)
    "A": '.topic[data-t="R"], .topic[data-t="Back"], .topic[data-t="pet"] { grid-column: span 4; }',
    # B: beside ท่าทาง: the last row split in two halves, the move's ring back at a half block's size
    "B": '.topic[data-t="move"], .topic[data-t="pet"] { grid-column: span 6; }'
         ' @media (min-width: 761px) { .topic[data-t="move"] .ring { --d: min(100cqw, calc(100cqh - 26px)); } }',
    # C: its own full row at the bottom, the ring sized like ท่าทาง's across a row; one more row in the grid's template
    "C": '.topic[data-t="pet"] { grid-column: 1 / -1; } @media (min-width: 761px) { .topic[data-t="pet"] .ring { --d: min(calc(50cqw - 14px), calc(100cqh - 26px)); } }'
         ' .topics { grid-template-rows: minmax(96px, 1.1fr) minmax(96px, .8fr) repeat(4, minmax(104px, 1fr)); }'
         ' @media (max-height: 1000px) and (min-width: 900px) { .topics { grid-template-rows: minmax(0, 1.1fr) minmax(0, .8fr) repeat(4, minmax(0, 1fr)); } }'
         ' @media (max-width: 760px) { .topics { grid-template-rows: 96px 40px repeat(4, 46px); } }',
}
PANEL_NAMES = {"today": "ตอนนี้ (ยังไม่มีช่องสัตว์เลี้ยง)", "A": "A · ต่อจากประดับ (3 ช่องในแถวเดียวกัน)",
               "B": "B · ข้างท่าทาง (แถวสุดท้ายแบ่งครึ่ง)", "C": "C · แถวของตัวเองข้างล่างสุด"}
ADD_PET = r"""() => {
  const back = document.querySelector('.topic[data-t="Back"]'), b = back.cloneNode(true);
  b.dataset.t = "pet"; b.removeAttribute("aria-expanded"); b.setAttribute("aria-label", "สัตว์เลี้ยง"); b.onclick = null;
  b.querySelector(".tname").textContent = "สัตว์เลี้ยง";
  const ring = b.querySelector(".ring"); ring.className = "ring t-pet"; ring.innerHTML = '<img alt="" src="/checks/pet_mocks/ui/sab.png">';
  back.after(b);
  return new Promise(r => { const im = b.querySelector("img"); im.complete ? r() : (im.onload = im.onerror = () => r()); });
}"""
INK = r"""() => [...document.querySelectorAll('.topic .tname')].map(e => { const r = e.getBoundingClientRect(); return { t: e.closest('.topic').dataset.t, text: e.textContent, x: r.x, y: r.y, w: r.width, h: r.height, cx: r.x + r.width / 2 }; })"""


def ink_offsets(png, items, dsf):
    """Per label: the ink's centre against its block's centre (px, CSS): dx; and the ink's top / bottom inside the label box."""
    from PIL import Image
    im = Image.open(png).convert("L")
    out = []
    for it in items:
        box = (int(it["x"] * dsf), int(it["y"] * dsf), int((it["x"] + it["w"]) * dsf), int((it["y"] + it["h"]) * dsf))
        crop = im.crop(box)
        px = crop.load()
        xs, ys = [], []
        for yy in range(crop.height):
            for xx in range(crop.width):
                if px[xx, yy] > 150:                    # the label's pale ink on the dark panel block
                    xs.append(xx); ys.append(yy)
        if not xs:
            continue
        inkc = (min(xs) + max(xs)) / 2 / dsf
        out.append({"t": it["t"], "text": it["text"], "dx": round(inkc - it["w"] / 2, 2), "inkTop": round(min(ys) / dsf, 1),
                    "inkBottom": round(max(ys) / dsf, 1), "boxH": round(it["h"], 1)})
    return out


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    http.server.ThreadingHTTPServer.request_queue_size = 128
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}/wardrobe/index.html"


def shoot():
    from PIL import Image, ImageChops
    from playwright.sync_api import sync_playwright
    srv, URL = serve()
    (OUT / "shots").mkdir(parents=True, exist_ok=True)
    (OUT / "panels").mkdir(parents=True, exist_ok=True)
    (OUT / "ui").mkdir(parents=True, exist_ok=True)
    icon = Path(r"D:\12tails\RippedAssets\ExportedProject\Assets\Resources\gamegui\icons\items\pet\sab.png")
    if not icon.exists():
        icon = Path(r"C:\Users\Jump\Desktop\12tails\RippedAssets\ExportedProject\Assets\Resources\gamegui\icons\items\pet\sab.png")
    Image.open(icon).convert("RGBA").resize((128, 128), Image.LANCZOS).save(OUT / "ui" / "sab.png")
    errors, report = [], {"shots": [], "panels": [], "ink": {}, "selfcheck": None, "pets": {}}

    def hook(pg, tag):
        pg.on("pageerror", lambda e: errors.append(f"{tag} pageerror: {e}"))
        pg.on("console", lambda m: errors.append(f"{tag} console.{m.type}: {m.text}") if m.type == "error" else None)

    def ready(pg):
        pg.goto(URL)
        pg.wait_for_function("() => window.wardrobe && wardrobe.debug().C && wardrobe.debug().C.meshes.length > 0", timeout=90000)
        pg.wait_for_timeout(2500)

    with sync_playwright() as pw:
        args = ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"]
        try:
            browser = pw.chromium.launch(args=args)
        except Exception:                           # the pip playwright wants a build this PC lacks: use the newest one installed
            shells = sorted((Path.home() / "AppData/Local/ms-playwright").glob("chromium_headless_shell-*/*/chrome-headless-shell.exe"))
            browser = pw.chromium.launch(args=args, executable_path=str(shells[-1]))
        # ---------------- the camera shots: desktop 1600 x 1000, picker closed
        ctx = browser.new_context(viewport={"width": 1600, "height": 1000}, device_scale_factor=1)
        pg = ctx.new_page()
        hook(pg, "stage")
        ready(pg)
        pg.evaluate(PM_JS)
        pg.evaluate("wardrobe.show('sheep')")
        pg.evaluate("__pm.freeze()")
        # self-check: the page's own fit (the reset button) against this script's hero-only fit in FIT_DIR
        pg.click("#resetCam")
        pg.wait_for_timeout(900)
        page_pose = pg.evaluate("(() => { const d = wardrobe.debug(); return { pos: d.camera.position.toArray(), target: d.controls.target.toArray() }; })()")
        mine = pg.evaluate("__pm.heroOnly()")
        dp = max(abs(a - b) for a, b in zip(page_pose["pos"] + page_pose["target"], mine["pos"] + mine["target"]))
        report["selfcheck"] = {"page": page_pose, "script": mine, "max_abs_diff": round(dp, 5)}
        print("self-check: the page's heroFitPose vs this script's hero-only fit, max |diff|", round(dp, 5))
        stage = pg.locator("#stage")
        for pet, spec in PETS.items():
            if ONLY and pet not in ONLY:
                continue
            data = json.loads((PETS_DIR / f"{pet}.json").read_text(encoding="utf-8"))
            box = pg.evaluate("([d, s]) => __pm.loadPet(d, s)", [data, spec])
            report["pets"][pet] = box
            cols = [("today", TODAY_TURN, TODAY_RISE)] + [(f"t{t}_r{int(r * 100):02d}", t, r) for r in RISES for t in TURNS]
            for tag, turn, rise in cols:
                pg.evaluate("([t, r]) => __pm.aim(__pm.dirOf(t, r), true)", [turn, rise])
                pg.wait_for_timeout(120)
                fn = f"shots/{pet}_{tag}.png"
                with_pet = stage.screenshot(path=str(OUT / fn))
                proj = pg.evaluate("__pm.project()")
                pg.evaluate("__pm.petShown(false)")
                no_pet = stage.screenshot()
                pg.evaluate("__pm.petShown(true)")
                from io import BytesIO
                diff = ImageChops.difference(Image.open(BytesIO(with_pet)).convert("RGB"), Image.open(BytesIO(no_pet)).convert("RGB")).convert("L")
                px = sum(diff.point(lambda v: 255 if v > 12 else 0).histogram()[255:])
                bbox = {k: round(proj[k]) for k in ("x0", "y0", "x1", "y1")}
                inside = proj["x0"] >= 0 and proj["y0"] >= 0 and proj["x1"] <= proj["vw"] and proj["y1"] <= proj["vh"]
                report["shots"].append({"pet": pet, "tag": tag, "turn": turn, "rise": rise, "file": fn, "bbox": bbox,
                                        "pet_pixels": px, "inside": inside, "stage": [proj["vw"], proj["vh"]]})
                print(f"  {pet:11s} {tag:10s} bbox {bbox} pet pixels {px} inside-stage {inside}")
        ctx.close()
        # ---------------- the panel
        for kind, vp, dsf, mobile in (("desktop", {"width": 1600, "height": 1000}, 1, False), ("phone", {"width": 390, "height": 700}, 2, True)):
            for var in ("today", "A", "B", "C"):
                ctx = browser.new_context(viewport=vp, device_scale_factor=dsf, is_mobile=mobile, has_touch=mobile)
                pg = ctx.new_page()
                hook(pg, f"{kind}-{var}")
                ready(pg)
                if var != "today":
                    pg.evaluate(ADD_PET)
                    pg.add_style_tag(content=CSS[var])
                    pg.wait_for_timeout(600)
                pg.evaluate("wardrobe.debug().C.mixer.timeScale = 0")
                pg.wait_for_timeout(300)
                aside = f"panels/{kind}_{var}_panel.png"
                full = f"panels/{kind}_{var}_page.png"
                pg.locator("aside").screenshot(path=str(OUT / aside))
                pg.screenshot(path=str(OUT / full))
                items = pg.evaluate(INK)
                ar = pg.evaluate("(() => { const r = document.querySelector('aside').getBoundingClientRect(); return [r.x, r.y]; })()")
                for it in items:                            # aside-relative, for the panel shot
                    it["x"] -= ar[0]; it["y"] -= ar[1]
                if var != "today":
                    report["ink"][f"{kind}_{var}"] = ink_offsets(OUT / aside, items, dsf)
                    # is the stacked tone mark of สัตว์เลี้ยง (ี + ้) cut by the label's own overflow: hidden? ink count with and without
                    pet = next(i for i in items if i["t"] == "pet")
                    big = dict(pet, y=pet["y"] - 6, h=pet["h"] + 12)
                    def ink_n(path):
                        im = Image.open(path).convert("L")
                        c = im.crop((int(big["x"] * dsf), int(big["y"] * dsf), int((big["x"] + big["w"]) * dsf), int((big["y"] + big["h"]) * dsf)))
                        return sum(c.point(lambda v: 255 if v > 150 else 0).histogram()[255:])
                    n0 = ink_n(OUT / aside)
                    pg.add_style_tag(content='.topic[data-t="pet"] .tname { overflow: visible !important; }')
                    pg.wait_for_timeout(200)
                    pg.locator("aside").screenshot(path=str(OUT / "panels" / "_clip_test.png"))
                    n1 = ink_n(OUT / "panels" / "_clip_test.png")
                    report.setdefault("clip", {})[f"{kind}_{var}"] = {"ink_hidden": n0, "ink_visible": n1, "cut_px": n1 - n0}
                report["panels"].append({"kind": kind, "var": var, "panel": aside, "page": full})
                print("  panel", kind, var)
                ctx.close()
        browser.close()
    report["errors"] = errors
    (OUT / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    srv.shutdown()
    return report


# ---------------------------------------------------------------------------------------------------- the page
def build_index(rep):
    from html import escape
    shots = {(s["pet"], s["tag"]): s for s in rep["shots"]}
    pan = {(p["kind"], p["var"]): p for p in rep["panels"]}
    rows = []
    for pet, spec in PETS.items():
        if (pet, "today") not in shots:
            continue
        def cell(tag, turn, rise, cls=""):
            s = shots[(pet, tag)]
            lab = (f"ตอนนี้ · หมุน {turn:.1f}° · เงย {rise:.2f}" if tag == "today" else label(turn, rise))
            return (f'<figure class="{cls}"><a href="{s["file"]}" target="_blank"><img src="{s["file"]}" loading="lazy" alt="{escape(lab)}"></a>'
                    f'<figcaption>{escape(lab)}</figcaption></figure>')
        grid = cell("today", TODAY_TURN, TODAY_RISE, "today")
        for r in RISES:
            for t in TURNS:
                grid += cell(f"t{t}_r{int(r * 100):02d}", t, r)
        rows.append(f'<section class="pet"><h3>{escape(spec["name"])} <span>{escape(spec["spot"])}</span></h3><div class="mx">{grid}</div></section>')
    cams = "\n".join(rows)
    panels = []
    for var in ("today", "A", "B", "C"):
        d, p = pan[("desktop", var)], pan[("phone", var)]
        panels.append(
            f'<section class="var"><h3>{escape(PANEL_NAMES[var])}</h3><div class="pp">'
            f'<figure><a href="{d["page"]}" target="_blank"><img class="dp" src="{d["panel"]}" alt="เดสก์ท็อป {var}"></a><figcaption>คอมพิวเตอร์ 1600 × 1000 · กดดูทั้งหน้า</figcaption></figure>'
            f'<figure><a href="{p["page"]}" target="_blank"><img class="ph" src="{p["panel"]}" alt="มือถือ {var}"></a><figcaption>มือถือ 390 × 700 · กดดูทั้งหน้า</figcaption></figure>'
            f'</div></section>')
    notes = ""
    ink = rep.get("ink", {})
    if ink:
        mine = [abs(x["dx"]) for v in ink.values() for x in v if x["t"] == "pet"]
        rest = [abs(x["dx"]) for v in ink.values() for x in v if x["t"] != "pet"]
        notes = (f"<p class=\"fine\">ตรวจกึ่งกลางตัวอักษรตามหมึกจริงจากภาพ (ซ้าย - ขวา): ป้าย \"สัตว์เลี้ยง\" เยื้องจากกึ่งกลางช่องไม่เกิน {max(mine):.1f} px "
                 f"ป้ายช่องอื่นไม่เกิน {max(rest):.1f} px ทั้งคอมพิวเตอร์และมือถือ ทุกตัวอย่าง</p>")
    clip = rep.get("clip", {})
    cut = [k for k, v in clip.items() if v["cut_px"] > 0 and k.startswith("phone")]
    if cut:
        notes += ("<p class=\"fine\">ข้อสังเกต: บนมือถือ ไม้โท + สระอี ของคำว่า \"สัตว์เลี้ยง\" ถูกตัดที่ขอบบนของป้ายชื่อ "
                  "(ป้ายชื่อในมือถือตั้ง overflow: hidden และ line-height 1.3) ต้องเผื่อที่ด้านบนอีกเล็กน้อยตอนทำจริง · บนคอมพิวเตอร์ไม่ถูกตัด</p>")
    html = f"""<!doctype html>
<html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>ตัวอย่างมุมกล้องและช่องสัตว์เลี้ยง</title>
<style>
:root {{ --bg:#faf7f0; --ink:#2b2520; --muted:#7a6e60; --line:#d9cfbd; --gold:#a77c1c; --card:#fff; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#1b1815; --ink:#efe6d6; --muted:#a89c8a; --line:#3a332b; --gold:#d4af37; --card:#26221d; }} }}
* {{ box-sizing: border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink); font:16px/1.5 "Noto Sans Thai","Sarabun","Leelawadee UI",system-ui,sans-serif; }}
main {{ max-width:1900px; margin:0 auto; padding:24px 16px 64px; }}
h1 {{ font-size:26px; margin:0 0 6px; }} h2 {{ font-size:21px; margin:40px 0 4px; padding-top:20px; border-top:2px solid var(--gold); }}
h3 {{ font-size:17px; margin:22px 0 8px; }} h3 span {{ color:var(--muted); font-weight:400; font-size:14px; margin-left:8px; }}
.note {{ background:var(--card); border:1px solid var(--line); border-left:4px solid var(--gold); padding:10px 14px; border-radius:6px; margin:10px 0 0; }}
.fine {{ color:var(--muted); font-size:13px; margin:6px 0 0; }}
.mx {{ display:grid; grid-template-columns: 1.15fr repeat(3, 1fr); gap:10px; }}
.mx .today {{ grid-row: span 2; border-color:var(--gold); }}
figure {{ margin:0; background:var(--card); border:1px solid var(--line); border-radius:8px; padding:6px; }}
figure img {{ width:100%; height:auto; display:block; border-radius:4px; }}
figcaption {{ text-align:center; font-size:14px; padding:6px 2px 2px; font-weight:600; }}
.today figcaption {{ color:var(--gold); }}
.vars {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(700px, 1fr)); gap:24px; }}
.var {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:4px 14px 14px; }}
.pp {{ display:flex; gap:16px; align-items:flex-start; }}
.pp figure {{ border:0; padding:0; background:none; }} .pp .dp {{ width:340px; max-width:100%; }} .pp .ph {{ width:300px; max-width:100%; }}
.pp figure:first-child {{ flex:0 1 340px; }} .pp figure:last-child {{ flex:0 1 300px; }}
@media (max-width:700px) {{ .mx {{ grid-template-columns:1fr 1fr; }} .mx .today {{ grid-column:1 / -1; grid-row:auto; }} .vars {{ grid-template-columns:1fr; }} .pp {{ flex-wrap:wrap; }} }}
</style></head><body><main>
<h1>ตัวอย่างมุมกล้องและช่องสัตว์เลี้ยง</h1>
<p class="note">ขนาดของสัตว์เลี้ยงเป็นค่าชั่วคราว และโมเดลในภาพนี้ยืนนิ่ง (ยังไม่มีท่าทาง) · กดที่ภาพเพื่อดูภาพเต็ม</p>

<h2>มุมกล้องตอนมีสัตว์เลี้ยง</h2>
<p class="fine">ซ้าย = มุมปัจจุบันของหน้า · แถวบน = เงย 0.10 · แถวล่าง = เงย 0.25 · คอลัมน์ = หมุน 30° / 40° / 55° จากด้านหน้าตัวละคร (ด้านเดียวกับตอนนี้) · กล้องกรอบทั้งตัวละครและสัตว์เลี้ยง</p>
{cams}

<h2>ตำแหน่งช่องสัตว์เลี้ยงในแผง</h2>
<p class="fine">ช่อง "สัตว์เลี้ยง" ใช้ไอคอน Small Anubi ในวงกลม ทำสำเนาจากปุ่มประดับ (คลาสเดียวกัน) · ตัวอย่าง C ต้องเพิ่มหนึ่งแถวในตารางของแผง</p>
{notes}
<div class="vars">
{chr(10).join(panels)}
</div>
</main></body></html>
"""
    (OUT / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    if "--reextract" in argv or not all((PETS_DIR / f"{p}.json").exists() for p in PETS if not ONLY or p in ONLY):
        extract()
    if "--no-shots" not in argv:
        rep = shoot()
        build_index(rep)
        print("errors:", rep["errors"] or "none")
        print("index:", OUT / "index.html")
