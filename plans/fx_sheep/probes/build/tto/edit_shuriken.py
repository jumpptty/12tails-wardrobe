"""One-off: apply the 2026-11-10 Sheep edits to wardrobe/fxparts/shuriken.js (each anchor must match exactly once)."""
p = "wardrobe/fxparts/shuriken.js"
s = open(p, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:70], s.count(a))
    s = s.replace(a, b)


rep('''// matrix. Approximations are marked APPROX.
export default function register(api) {''', '''// matrix. Approximations are marked APPROX.
// 2026-11-10 (the Sheep's TTO effects, plans/fx_sheep/tto.md "Probed 2026-11-10"): the simulation space read the right
// way round (moveWithTransform 1 = World: Unity's ParticleSystemSimulationSpace Local 0 / World 1 / Custom 2; it was read
// as 0 = world, so every TTO system simulated in the wrong space, the Wolf's too), World collision on the page's floor
// (the Sparks of gleamingBreath_exhale, grandCodex_cast, lucentBarrier_reflect), mesh particles (m_RenderMode 4: the
// shards and prism shells, the renderer's "mesh" from wardrobe_fx_tto.py). The curve readers are shared on
// api.curves (tto_sheep.js's Line / Trail renderers use them).
export default function register(api) {''')

rep('''      // moveWithTransform is the serialized simulation space: 0 world, 1 local, 2 custom (APPROX: custom = local)
      world: num(ps.moveWithTransform, 1) === 0,''', '''      // moveWithTransform is the serialized simulation space (ParticleSystemSimulationSpace): 0 local, 1 world, 2 custom
      // (APPROX: custom = local). The Sheep's prefabs agree: the wisp's Orbit (0) rides with it, its Sparkle (1) stays
      // behind; the book's Astrolabe (0) hangs under it, its Glyphs (1) rise from where it was
      world: num(ps.moveWithTransform, 0) === 1,''')

rep('''    // not drawn (no Wolf prefab enables them): NoiseModule, ExternalForces, Collision, Trigger, SubModule (sub-emitters),
    // Lights, TrailModule (ribbons), CustomData; the UV module's sprite mode
    P.skipped = ["NoiseModule", "ExternalForcesModule", "CollisionModule", "TriggerModule", "SubModule", "LightsModule", "TrailModule"].filter(n => mod(n));''',
    '''    // CollisionModule type 1 (World) against the page's floor, the only collider it has (y 0 of the effect's Unity world
    // = the hero's feet). Unity's world collision also meets the heroes' colliders and the map: APPROX, the floor only.
    // m_Dampen: the share of the speed along the floor lost, m_Bounce: the share of the speed into the floor sent back,
    // m_EnergyLossOnCollision: the share of the lifetime lost, min/maxKillSpeed: killed after a hit outside that speed,
    // radiusScale x half the particle's size = its radius (APPROX: its start size, not the size over its life)
    if ((m = mod("CollisionModule")) && num(m.type) === 1) P.coll = { dampen: mmCurve(m.m_Dampen, 0), bounce: mmCurve(m.m_Bounce, 1),
      loss: mmCurve(m.m_EnergyLossOnCollision, 0), minKill: num(m.minKillSpeed), maxKill: num(m.maxKillSpeed, 1e4), radius: num(m.radiusScale, 1) };
    // not drawn (no Wolf or Sheep prefab enables them): NoiseModule, ExternalForces, Collision with planes (type 0),
    // Trigger, SubModule (sub-emitters), Lights, TrailModule (ribbons), CustomData; the UV module's sprite mode
    P.skipped = ["NoiseModule", "ExternalForcesModule", "CollisionModule", "TriggerModule", "SubModule", "LightsModule", "TrailModule"]
      .filter(n => mod(n) && !(n === "CollisionModule" && P.coll));''')

rep('''      q.p.addScaledVector(q.vt, sm * dt);''', '''      q.p.addScaledVector(q.vt, sm * dt);
      if (P.coll && !collide(q, u)) return false;''')

rep('''    function stepAll(dt) {''', '''    // World collision with the floor (P.coll above): false = the hit killed it
    function collide(q, u) {
      const C = P.coll, W = toWorld(q.p), r = C.radius * q.size.x * sizeK / 2;
      if (W.y >= r) return true;
      const v = toWorldDir(q.v);
      if (v.y >= 0) return true;                               // already leaving the floor
      const k = q.R[5];
      v.x *= 1 - C.dampen(u, k); v.z *= 1 - C.dampen(u, k); v.y = -v.y * C.bounce(u, k);
      W.y = r;
      q.p.copy(P.world ? W : W.sub(T).applyQuaternion(Ri).divide(safe(Sm)));
      q.v.copy(worldToSimDir(v));
      q.age += C.loss(u, k) * q.life;
      const sp = v.length();
      return q.age < q.life && sp >= C.minKill && sp <= C.maxKill;
    }
    function stepAll(dt) {''')

rep('''    const RM = num(rd.m_RenderMode), drawn = mat && RM !== 5 && rd.m_Enabled !== 0 && rd.m_Enabled !== false;''',
    '''    const RM = num(rd.m_RenderMode), drawn = mat && RM !== 5 && rd.m_Enabled !== 0 && rd.m_Enabled !== false;
    const pMesh = RM === 4 && rd.mesh?.verts ? rd.mesh : null;   // mesh particles: the renderer's m_Mesh (wardrobe_fx_tto.py)''')

rep('''        if (mesh) render(cam);''', '''        if (mesh) (pMesh ? renderMesh : render)(cam);''')

rep('''  api.part("ParticleSystem", build);''', '''  api.curves = { curveFn, gradFn };                              // for tto_sheep.js (read when an effect is built)
  api.part("ParticleSystem", build);''')

# the mesh renderer, after render()
rep('''      api.setMesh(mesh, pos, col, uvs, idx);
    }
    return ps0;''', '''      api.setMesh(mesh, pos, col, uvs, idx);
    }

    // ---- m_RenderMode 4, mesh particles: the renderer's mesh drawn at every particle, scaled by its size (x, y, z
    // with size3D or a separate-axes size module, else uniform) and turned by its rotation (rotation3D: Unity's Euler
    // z, x, y, the page's "YXZ", in radians as serialized; else about z), inside the renderer's alignment:
    // m_RenderAlignment 1 world, 2 local (the system's rotation), 0 view / 3 facing (the camera's axes), 4 velocity (z
    // along the motion). Vertex colour = the particle's x the mesh's own (white without); the mesh's uv0; normals turned
    // with the particle (TTO/Sheep/Prism Veil reads them). APPROX: the texture sheet, m_Flip, pivot and the mesh
    // distribution (m_Mesh1..3) are not applied: every Sheep mesh renderer has one mesh and no sheet
    const Q = new THREE.Quaternion(), Qa = new THREE.Quaternion(), E = new THREE.Euler(), Mb = new THREE.Matrix4();
    function renderMesh(cam) {
      const det = M.determinant();
      if (!Number.isFinite(det) || Math.abs(det) < 1e-12) { mesh.visible = false; return; }
      mesh.visible = node.visible !== false;
      Minv.copy(M).invert(); mesh.matrix.copy(Minv); mesh.matrixWorldNeedsUpdate = true;
      const g = pMesh, nv = g.verts, mp = g.pos, mn = g.nrm, mu = g.uv, mc = g.col, mi = g.idx;
      let order = parts;
      if (sortMode === 1) order = parts.map(q => [q, toWorld(q.p).distanceToSquared(camPos)]).sort((a, b) => b[1] - a[1]).map(x => x[0]);
      else if (sortMode === 2) order = parts.slice().sort((a, b) => a.age - b.age);
      else if (sortMode === 3) order = parts.slice().sort((a, b) => b.age - a.age);
      if (align === 1) Qa.identity();
      else if (align === 2) Qa.copy(Rq);
      else if (align !== 4) Qa.setFromRotationMatrix(Mb.makeBasis(cam.right, cam.up, cam.fwd.clone().negate()));
      const pos = [], col = [], uvs = [], nrm = [], idx = [], v = V(), n = V();
      for (const q of order) {
        const u = q.age / q.life, R = q.R, W = toWorld(q.p);
        let sx = q.size.x, sy = P.size3D ? q.size.y : sx, sz = P.size3D ? q.size.z : sx;
        if (P.sizeOL) { const m = P.sizeOL, a = m.x(u, R[7]); sx *= a; sy *= m.sep ? m.y(u, R[7]) : a; sz *= m.sep ? m.z(u, R[7]) : a; }
        sx *= sizeK; sy *= sizeK; sz *= sizeK;
        if (!(Math.abs(sx) + Math.abs(sy) + Math.abs(sz) > 0)) continue;
        let c = q.c0;
        if (P.colOL) { const k = P.colOL(u, R[9]); c = [c[0] * k[0], c[1] * k[1], c[2] * k[2], c[3] * k[3]]; }
        if (align === 4) {                                     // velocity: the mesh's z along the motion
          const d = toWorldDir(q.vt); if (d.lengthSq() < 1e-12) d.set(0, 0, 1); d.normalize();
          Qa.setFromUnitVectors(V(0, 0, 1), d);
        }
        Q.setFromEuler(P.rot3D ? E.set(q.rot.x, q.rot.y, q.rot.z, "YXZ") : E.set(0, 0, q.rot.z, "YXZ")).premultiply(Qa);
        const b = pos.length / 3;
        for (let i = 0; i < nv; i++) {
          v.set(mp[3 * i] * sx, mp[3 * i + 1] * sy, mp[3 * i + 2] * sz).applyQuaternion(Q).add(W);
          pos.push(v.x, v.y, v.z);
          if (mn) { n.set(mn[3 * i], mn[3 * i + 1], mn[3 * i + 2]).applyQuaternion(Q); nrm.push(n.x, n.y, n.z); } else nrm.push(0, 0, 1);
          uvs.push(mu ? mu[2 * i] : 0, mu ? mu[2 * i + 1] : 0);
          if (mc) col.push(c[0] * mc[4 * i], c[1] * mc[4 * i + 1], c[2] * mc[4 * i + 2], c[3] * mc[4 * i + 3]);
          else col.push(c[0], c[1], c[2], c[3]);
        }
        for (const k of mi) idx.push(b + k);
      }
      api.setMesh(mesh, pos, col, uvs, idx);
      mesh.geometry.setAttribute("normal", new THREE.Float32BufferAttribute(nrm, 3));
    }
    return ps0;''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
