// wardrobe/fxparts/trail.js: the game's TrailEmitter (TrailEmitter.cs) and Unity 3.5's built-in TrailRenderer
// (plans/fx_wolf/parts.md "TrailEmitter", "TrailRenderer"; the loader comment above FX_PART_FILES in index.html).
// Wolf: dualbrand_slash1 / 2 / 4 (TrailEmitter on SlashN and its child), crusader / lawbringer (TrailRenderer on
// crusader_upperSlash / crusader_sideSlash). The nodes are swung by the effect's Animation (agent C's part), so every
// update reads the node's pose afresh.
//
// Space: both trails keep their points in Unity's world, which on the page is the effect's mirror group (fx.mirror,
// scaled (-1, 1, 1), placed at the hero): a node's pose there is fx.uMatrix(node) = mirrorInv x matrixWorld, its
// rotation fx.uQuat(node), Vector3.up is (0, 1, 0). The mesh hangs under the node and its vertices are moved into the
// node's space with the inverse of that matrix, as the game does (worldToLocalMatrix.MultiplyPoint, TrailEmitter.cs:388,
// :488): drawn through the node's own matrix they land back on the Unity-world points, so the ribbon stays where the
// node has been while the node moves on, the mirror applies once, and the trail goes when its node is destroyed.

const QUALITY = 5;   // QualitySettings.GetQualityLevel(): the page draws as the game's top level (Unity 3.5's Fantastic)

export default function register(api) {
  const { V, clamp01, fxMesh, setMesh, fxMaterial, camera } = api;
  // the game's colours are gamma values: the same conversion as the page's linRGBA (index.html, "skill effects")
  const toLin = c => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
  const lin = c => [toLin(c[0]), toLin(c[1]), toLin(c[2]), c[3]];
  const lerpC = (a, b, t) => { t = clamp01(t); return a.map((x, j) => x + (b[j] - x) * t); };   // Color.Lerp clamps t
  const lerp = (a, b, t) => a + (b - a) * t;
  // the node's matrix in Unity's world this frame: refresh it first, since the Animation part may have just posed the
  // node (Fx.update refreshes the group's matrices before the emitters run, not between them)
  const pose = (fx, node) => { node.updateWorldMatrix(true, false); return fx.uMatrix(node); };
  const strip = (idx, n) => { for (let i = 0; i < n - 1; i++) idx.push(2 * i, 2 * i + 1, 2 * i + 2, 2 * i + 2, 2 * i + 1, 2 * i + 3); };

  // ---------- TrailEmitter (TrailEmitter.cs, the game's own; fields :813-867)
  // Sections newest first (Unshift :331, the oldest Pop()ed :200): { point, upDir, uv, time } (WeaponTrailSection.cs)
  api.part("TrailEmitter", (fx, node, e, mat) => {
    // [RequireComponent] MeshFilter + MeshRenderer: without them Awake logs and disables itself (:115-130); the node's
    // first material is its MeshRenderer's
    if (!mat) return null;
    if (QUALITY < e.minQuality) return null;                  // Awake :102, else enabled = false (:146)
    const m = fxMesh(node, mat);
    const secs = [], start = 0;                               // Awake :90-96: the timer's start = Time.time at spawn
    let time = 0, emitting = true, gone = false;              // emitting starts true (ctor :61)
    return { node, renderer: m, update(dt) {
      // Destroy(this) (:248): the component goes, its MeshRenderer keeps drawing the last mesh built
      if (gone) return;
      time += dt;                                             // the trail's own clock (Time.time from spawn), not fx.age,
                                                              // which a followState cut jumps
      // renderer.enabled false: forget every section and leave the mesh as it was (:165-175). On the page that is this
      // mesh's visible flag (no part sets it yet; `renderer` is handed out for one that would)
      if (!m.visible) { secs.length = 0; return; }
      const um = pose(fx, node), position = V().setFromMatrixPosition(um);   // transform.position (:178)
      while (secs.length && time > secs[secs.length - 1].time + e.life) secs.pop();   // pruning (:184-206)
      if (e.isTimer) {                                        // :207-254 (easeIn / Middle / Out only time the window)
        emitting = true;
        if (start + e.delay > time) emitting = false;
        if (start + e.delay + e.easeIn + e.easeMiddle < time) emitting = false;
        // Destroy(this) is deferred to the frame's end: this frame still builds its mesh
        if (start + e.delay + e.easeIn + e.easeMiddle + e.easeOut < time) gone = true;
      }
      // a new section when the node is more than minDistance from the newest (:255-336)
      if (emitting && (!secs.length || secs[0].point.distanceToSquared(position) > e.minDistance * e.minDistance)) {
        // upDir: world up with alwaysUp, else the node's own up now, TransformDirection = rotation only (:286-305)
        const upDir = e.alwaysUp ? V(0, 1, 0) : V(0, 1, 0).applyQuaternion(fx.uQuat(node));
        // uv: the distance along the trail / uvHeight (:306-325)
        const uv = secs.length ? secs[0].uv + secs[0].point.distanceTo(position) / e.uvHeight : 0;
        secs.unshift({ point: position, upDir, uv, time });   // :326-331
      }
      // mesh.Clear() (:343); with fewer than 2 sections nothing is drawn (:346-360: the game's `worldVelocity ==
      // Vector3.zero` compares a float with a vector and never holds, so it builds 0 or 1 sections into a mesh with no
      // triangles, or throws on new int[-6]: empty either way)
      const n = secs.length;
      if (n < 2) { setMesh(m, [], [], [], []); return; }
      const toNode = um.clone().invert();                    // worldToLocalMatrix (:388)
      const pos = [], col = [], uvs = [], idx = [];
      const keys = [e.Color1, e.Color2, e.Color3, e.Color4];
      let u = 0;                                              // :391; the newest section keeps 0 (:456-467)
      secs.forEach((s, i) => {
        const age = time - s.time;
        if (i !== 0) u = clamp01(age / e.life);                                   // :462 / :607
        const a = s.upDir, d = 0.5 * lerp(e.startWidth, e.endWidth, u);          // :468-473 (Mathf.Lerp, u in 0..1)
        const d2 = age * e.localVelocity, d3 = age * e.worldVelocity;            // :478-483
        // point -/+ upDir x d + upDir x d2 + Vector3.up x d3, into the node's space (:488-493 / :633-638)
        const b = s.point.clone().addScaledVector(a, d2); b.y += d3;
        const p0 = b.clone().addScaledVector(a, -d).applyMatrix4(toNode), p1 = b.clone().addScaledVector(a, d).applyMatrix4(toNode);
        pos.push(p0.x, p0.y, p0.z, p1.x, p1.y, p1.z);
        // Stretch (0): u x uvHeight by age (:498-503); Tile (1): the section's distance uv (:643-648); eTrailEmitterMode.cs
        const U = e.TrailEmitterMode === 0 ? u * e.uvHeight : s.uv;
        uvs.push(U, 0, U, 1);
        // four keys at 0 / .33 / .66 / 1, factor 3 (:508-539); Color.Lerp in the game's (gamma) values, then linear
        const c = lin(u < 0.33 ? lerpC(keys[0], keys[1], 3 * u) : u < 0.66 ? lerpC(keys[1], keys[2], 3 * (u - 0.33)) : lerpC(keys[2], keys[3], 3 * (u - 0.66)));
        col.push(...c, ...c);
      });
      strip(idx, n);                                          // :706-749
      setMesh(m, pos, col, uvs, idx);
    } };
  });

  // ---------- TrailRenderer (Unity 3.5's built-in, no source: its 3.5 manual page and the legacy line builder's
  // behaviour as remembered, so this part is an approximation; the fields are its type tree, wardrobe_fx.py)
  // m_Time (each point's life), m_StartWidth at the node / m_EndWidth at the tail, m_Colors (5 packed RGBA keys, head to
  // tail), m_MinVertexDistance, m_Autodestruct (the object is destroyed once it has been idle for m_Time), its own
  // materials in `mats` (the node's `mats` may be a legacy particle renderer's).
  // A TrailRenderer switched off in the prefab (m_Enabled false) is built hidden, and the cue's enable ([[t, nodeName, on],
  // ...], seconds after the spawn) switches it by its node's name: the newest due entry sets it (2026-11-13, the Panda's
  // Three Steps, whose code turns its three blade trails on and off, Panda.cs:20873-21277; plans/fx_panda/parts.md part 1,
  // Interfaces 2). APPROXIMATED: hidden drops its points (Unity's may keep them); none of Three Steps' is switched on twice
  api.part("TrailRenderer", (fx, node, c, _mat, _nodeDef, data) => {
    const name = c.mats?.[0];
    if (!name || !data.materials?.[name]) return null;
    const m = fxMesh(node, fxMaterial(fx.cls, name, data.materials[name]));
    if (c.m_Enabled === false) m.visible = false;
    const en = (fx.at?.enable || []).filter(e => e[1] === node.name).sort((a, b) => a[0] - b[0]);
    // packed colour: r in the low byte, as the legacy particles' colorAnimation keys (index.html legacyParticles)
    const key = x => { const v = (x?.rgba ?? 0xffffffff) >>> 0; return [(v & 255) / 255, ((v >>> 8) & 255) / 255, ((v >>> 16) & 255) / 255, (v >>> 24) / 255]; };
    const keys = [0, 1, 2, 3, 4].map(i => key(c.m_Colors?.[`m_Color[${i}]`]));
    const life = c.m_Time, md2 = c.m_MinVertexDistance * c.m_MinVertexDistance;
    const pts = [];                                           // oldest first: { p (Unity world), time }
    let time = 0, added = false, side0 = V(1, 0, 0);
    return { node, renderer: m, update(dt) {
      time += dt;
      for (const e of en) if (e[0] <= time) m.visible = !!e[2];             // the newest due switch (sorted by time)
      if (!m.visible) { pts.length = 0; return; }
      const um = pose(fx, node), head = V().setFromMatrixPosition(um);
      while (pts.length && time > pts[0].time + life) pts.shift();          // a point lives m_Time
      if (c.m_Autodestruct && added && !pts.length) return "destroy";       // idle for m_Time: Destroy(gameObject)
      if (!pts.length || pts[pts.length - 1].p.distanceToSquared(head) > md2) { pts.push({ p: head.clone(), time }); added = true; }
      // the line: the node's current position first (the trail stays joined to its object between points), then the
      // points newest to oldest
      const L = [];
      if (head.distanceToSquared(pts[pts.length - 1].p) > 1e-12) L.push(head);
      for (let i = pts.length - 1; i >= 0; i--) L.push(pts[i].p);
      const n = L.length;
      if (n < 2) { setMesh(m, [], [], [], []); return; }
      // facing the camera: each point's side = tangent x (camera - point), from the camera's Unity-space position
      const camPos = camera.getWorldPosition(V()).applyMatrix4(fx.mirrorInv);
      const toNode = um.clone().invert();
      const pos = [], col = [], uvs = [], idx = [];
      for (let i = 0; i < n; i++) {
        // width, colour and u spread evenly by point index, head 0 to tail 1 (the legacy builder's "stretch")
        const t = i / (n - 1), w = 0.5 * lerp(c.m_StartWidth, c.m_EndWidth, t);
        const tan = (i === 0 ? L[1].clone().sub(L[0]) : i === n - 1 ? L[n - 1].clone().sub(L[n - 2]) : L[i + 1].clone().sub(L[i - 1]));
        const s = V().crossVectors(tan, camPos.clone().sub(L[i]));
        if (s.lengthSq() > 1e-12) side0 = s.normalize();     // seen end-on: keep the last good side
        const p0 = L[i].clone().addScaledVector(side0, -w).applyMatrix4(toNode), p1 = L[i].clone().addScaledVector(side0, w).applyMatrix4(toNode);
        pos.push(p0.x, p0.y, p0.z, p1.x, p1.y, p1.z);
        uvs.push(t, 0, t, 1);
        const k = Math.min(3, Math.floor(t * 4)), cc = lin(lerpC(keys[k], keys[k + 1], t * 4 - k));
        col.push(...cc, ...cc);
      }
      strip(idx, n);
      setMesh(m, pos, col, uvs, idx);
    } };
  });
}
