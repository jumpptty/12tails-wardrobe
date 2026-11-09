// wardrobe/fxparts/groundhug.js: TTO's GroundHugEmitter (agent F, 2026-11-09; plans/fx_wolf/build_rules.md, tto.md 3).
// Read from TTO's machine code: Ghidra (the Bible's tools/run_ghidra.bat, read only, over names.tsv) on every method
// below, then capstone where Ghidra dropped an argument (TTO1102 = DecompiledSource_TTO_2026-11-02, client/GameAssembly.dll).
// The CRT helpers were identified by running them under unicorn: FUN_180308640 = cosf, FUN_180308bd0 = sinf,
// FUN_180306720 = ceil (so Mathf.CeilToInt = FUN_1809f9e50), FUN_1803067f0 = floorf, FUN_180306c80 = powf.
//
// Fields (dump.cs TypeDefIndex 410): shape (0 Disc, 1 Band, 2 Strip), Life, Delay, repeatForever, Emission (int),
// EmissionPeriod, start/endRadius, start/endWidth, start/endHeight, startAngle, Rotation, uvTile, uvRotation, Color1..5,
// lift, segments, rings, resample, motes (ParticleSystem), motesPerSecond. Consts GroundMask 1, RayUp 12, RayDown 24, Step .75.
//
// What the game does (all established from the code unless marked APPROX):
// - Awake@0x22612C0: a new dynamic Mesh "GroundHug" on the node's MeshFilter. Start@0x2264610 = Sample().
// - Sample@0x22639F0: sampledAt = transform.position (world); a height grid of the terrain under the shape (rings of
//   radius step 0.75, or for a Strip rows along forward x columns across) from Ground(); Strip: stripDir = forward with
//   y = 0, normalised (Vector3.forward if |xz|^2 <= 1e-4), stripSide = (dir.z, 0, -dir.x); grid columns
//   nA = clamp(CeilToInt(2 x (0.5 x max(startWidth, endWidth) x Scale + (resample > 0 ? 1.5 : 0)) / 0.75) + 1, 3, 17).
// - Ground(p, near)@0x2263100: Physics.RaycastNonAlloc from (p.x, near + 12, p.z) down, 36 m, layer mask 1; the hit
//   whose y is nearest `near`; none -> near. GroundAt(p)@0x2262BD0: bilinear lookup in the grid. The page's floor is flat
//   at y = 0 (the hero's feet), so every grid height is that one value: gy = Ground(sampledAt, sampledAt.y), kept for
//   the emitter's life (the game re-samples only when resample > 0 and the node moved, same value on a flat floor).
// - get_Scale@0x2264A40 = max(|lossyScale.x|, 0.01). get_Centre@0x22649C0 = sampledAt, or the live position when
//   resample > 0 (each Build* reads it the same way).
// - LateUpdate@0x2263360: clock += dt; when clock >= max(0, Emission - 1) x EmissionPeriod + Delay + Life: repeatForever
//   -> clock = Delay (the loop restarts at Delay, not 0), else Mesh.Clear and the script disables itself (the node stays).
//   Then the mesh is rebuilt every frame by shape. Every vertex is made in WORLD space and stored through
//   transform.InverseTransformPoint (Add@0x2261100), so the shapes lie flat on the ground whatever the node's rotation or
//   height (the zone spawns 1.2 m up; its ring still lies on the floor). Colour = Ramp(u)@0x2263760: the 5-key ramp
//   (keys at 0 / .25 / .5 / .75 / 1), the page's ramp(e, u).
// - BuildDisc@0x2261A10 (one disc): from clock >= Delay; u = clamp01((clock - Delay) / max(Life, 1e-4));
//   R = lerp(startRadius, endRadius, u) x Scale, drawn while R > 0.01; n = max(2, rings) rings x (segments + 1) points:
//   ring i radius R x i / n, angle a = 2 pi j / segments, point (c.x + cos a x r, gy + lift, c.z + sin a x r);
//   uv = (cos b x f / 2 + .5, sin b x f / 2 + .5), f = i / n, b = a - (u x Rotation + startAngle) (RADIANS: the turn is
//   the texture's, the mesh does not move; Rune's Rotation 6.283 = one turn a life).
// - BuildBand@0x2261390 (max(1, Emission) bands, band k live while 0 <= age <= Life, age = clock - Delay - k x
//   EmissionPeriod): u = clamp01(age / Life); R = lerp(start/endRadius) x Scale, R2 = R + lerp(start/endWidth) x Scale,
//   H = lerp(start/endHeight) x Scale; segments + 1 pairs at a = 2 pi i / segments (no startAngle / Rotation):
//   bottom (c.x + cos a R, gy + lift, c.z + sin a R) uv (i x uvTile / segments + Time.time x uvRotation x uvTile, 0),
//   top (c.x + cos a R2, gy + lift + H, c.z + sin a R2) uv (same, 1): a RingEmitter-like wall standing on the ground
//   (negative widths lean it inward). Band 0 also feeds EmitMotes(R, c) each frame it is live.
// - BuildStrip@0x2261FB0 (one strip): u as the disc; L = lerp(startHeight, endHeight) x Scale = the LENGTH,
//   hw = lerp(startWidth, endWidth) x Scale / 2 = the half WIDTH, drawn while L > 0.01 and hw > 0.001; rows
//   n = max(2, CeilToInt(2 L)), columns max(2, nA); row i at d = i L / n + startRadius x Scale along stripDir, column k
//   at w = (2 k / (cols - 1) - 1) x hw along stripSide, y = gy + lift; uv = (i / n x uvTile + Time.time x uvRotation x
//   uvTile, k / (cols - 1)). (resample > 0 re-reads forward each frame.) Rake's Claw0..2: 0.5 -> 38 m long, 8 -> 6.4 m wide.
// - EmitMotes(r, o)@0x22627A0: motesDue += dt x motesPerSecond; per whole one: angle Random.Range(0, 2 pi), position
//   (o.x + cos x r, GroundAt + 0.1, o.z + sin x r), velocity Vector3.up x Random.Range(1.5, 3.5),
//   applyShapeToPosition false, ParticleSystem.Emit(params, 1) on `motes` (the domain Wall's Motes system, world space:
//   its moveWithTransform = 1).
//
// On the page: points are made in the mirror group's space (= Unity's world for the effect: the hero's frame, floor y 0)
// and turned into the node's own space with the inverse of fx.uMatrix(node), as the game's InverseTransformPoint.
// Time.time (the band's and strip's UV scroll) = a clock of this emitter's own that starts at the page clock and stops
// with Space (APPROX: the game's global clock; only the scroll's phase differs).
// The motes go to the ParticleSystem part (fxparts/shuriken.js) built on the `motes` node ({node: i} from
// wardrobe_fx_tto.py): its emit(count, { position, velocity, applyShapeToPosition: false, space: "world" }), Unity world
// (mirror-space) vectors; no such emitter -> no motes.
// No stop(): TTO's EffectControl::Update@0x1A233A0 at the after-life reaches only its children's ParticleSystems (Stop),
// ImageEmitters and RingEmitters (GetComponentsInChildren<...>), never a GroundHugEmitter, so a repeatForever band runs
// on until the effect is destroyed at life + afterLife, as in the game.
export default function register(api) {
  const { V, ramp, fxMesh, setMesh } = api;
  // Ground(p, near) on the page's flat floor (y 0): the ray from near + 12 down 36 m meets it when it lies in that span
  const ground = near => (near + 12 >= 0 && near - 24 <= 0 ? 0 : near);

  api.part("GroundHugEmitter", (fx, node, e, mat, nodeDef) => {
    if (!mat || e.enabled === false || nodeDef.active === false) return null;
    const m = fxMesh(node, mat);
    let clock = 0, done = false, sampled = null, gy = 0, dir = null, nA = 2, motesDue = 0, motes = null;
    let now = performance.now() / 1000;
    const L = (a, b, u) => a + (b - a) * u;
    const clamp01 = x => Math.min(1, Math.max(0, x));
    const pose = () => {
      const um = fx.uMatrix(node);
      return { um, inv: um.clone().invert(), pos: V().setFromMatrixPosition(um), scale: Math.max(0.01, Math.abs(V().setFromMatrixScale(um).x)) };
    };
    const forwardFlat = () => {
      const f = V(0, 0, 1).applyQuaternion(fx.uQuat(node));
      if (f.x * f.x + f.z * f.z <= 1e-4) return V(0, 0, 1);
      const d = V(f.x, 0, f.z), l = d.length();
      return l <= 1e-5 ? V() : d.multiplyScalar(1 / l);
    };
    const sample = P => {                    // Sample@0x22639F0 (on a flat floor: the one ground height and the strip axes)
      sampled = P.pos.clone(); gy = ground(sampled.y);
      if (e.shape === 2) {
        dir = forwardFlat();
        const hw = P.scale * 0.5 * Math.max(e.startWidth, e.endWidth) + (e.resample > 0 ? 1.5 : 0);
        nA = Math.min(17, Math.max(3, Math.ceil((hw + hw) / 0.75) + 1));
      }
    };
    // the motes: the ParticleSystem emitter built on the node `motes` names ({node: i} from wardrobe_fx_tto.py)
    const motesTarget = () => {
      const r = e.motes;
      if (!r) return null;
      const i = typeof r === "number" ? r : typeof r === "object" && !Array.isArray(r) ? r.node : null;
      const n = i != null ? fx.nodes[i] : typeof r === "string" ? fx.nodes.find(o => o.name === r) : null;
      return n ? fx.emitters.find(x => x.node === n && typeof x.emit === "function") || null : null;
    };
    const emitMotes = (dt, r, c) => {        // EmitMotes@0x22627A0
      if (!(e.motesPerSecond > 0)) return;
      motes ||= motesTarget();
      if (!motes) return;
      motesDue += dt * e.motesPerSecond;
      while (motesDue >= 1) {
        motesDue -= 1;
        const a = Math.random() * 2 * Math.PI;
        motes.emit(1, { position: V(c.x + Math.cos(a) * r, gy + 0.1, c.z + Math.sin(a) * r), velocity: V(0, 1.5 + Math.random() * 2, 0),
                        applyShapeToPosition: false, space: "world" });
      }
    };
    return { node, update(dt) {
      if (done) return;
      now += dt;
      const P = pose();
      if (!sampled) sample(P);
      clock += dt;                                                         // LateUpdate@0x2263360
      if (clock >= Math.max(0, e.Emission - 1) * e.EmissionPeriod + e.Delay + e.Life) {
        if (!e.repeatForever) { done = true; setMesh(m, [], [], [], []); return; }
        clock = e.Delay;
      }
      const live = e.resample > 0;                                         // get_Centre: live position when resample > 0
      const c = live ? P.pos : sampled, s = P.scale, y0 = gy + e.lift;
      const pos = [], col = [], uv = [], idx = [];
      const add = (x, y, z, u, v, k) => { const p = V(x, y, z).applyMatrix4(P.inv); pos.push(p.x, p.y, p.z); uv.push(u, v); col.push(...k); };
      if (e.shape === 0) {                                                 // BuildDisc@0x2261A10
        if (clock >= e.Delay) {
          const u = clamp01((clock - e.Delay) / Math.max(e.Life, 1e-4)), R = L(e.startRadius, e.endRadius, u) * s;
          if (R > 0.01) {
            const k = ramp(e, u), turn = u * e.Rotation + e.startAngle, n = Math.max(2, e.rings), S = e.segments, W = S + 1;
            for (let i = 0; i <= n; i++) {
              const f = i / n, r = f * R;
              for (let j = 0; j <= S; j++) {
                const a = j * 2 * Math.PI / S, b = a - turn;
                add(c.x + Math.cos(a) * r, y0, c.z + Math.sin(a) * r, Math.cos(b) * f * 0.5 + 0.5, Math.sin(b) * f * 0.5 + 0.5, k);
              }
            }
            for (let i = 0; i < n; i++) for (let j = 0; j < S; j++) {
              const q = i * W + j;
              idx.push(q, q + W, q + 1, q + 1, q + W, q + W + 1);
            }
          }
        }
      } else if (e.shape === 1) {                                          // BuildBand@0x2261390
        const S = e.segments, scroll = now * e.uvRotation * e.uvTile;
        for (let b = 0; b < Math.max(1, e.Emission); b++) {
          const age = clock - e.Delay - b * e.EmissionPeriod;
          if (!(age >= 0 && age <= e.Life)) continue;
          const u = clamp01(age / Math.max(e.Life, 1e-4)), R = L(e.startRadius, e.endRadius, u) * s;
          const R2 = R + L(e.startWidth, e.endWidth, u) * s, H = L(e.startHeight, e.endHeight, u) * s, k = ramp(e, u), base = pos.length / 3;
          for (let i = 0; i <= S; i++) {
            const a = i * 2 * Math.PI / S, ca = Math.cos(a), sa = Math.sin(a), uu = i * e.uvTile / S + scroll;
            add(c.x + ca * R, y0, c.z + sa * R, uu, 0, k);
            add(c.x + ca * R2, y0 + H, c.z + sa * R2, uu, 1, k);
          }
          for (let i = 0; i < S; i++) { const q = base + 2 * i; idx.push(q, q + 1, q + 2, q + 2, q + 1, q + 3); }
          if (b === 0) emitMotes(dt, R, c);
        }
      } else if (clock >= e.Delay) {                                       // BuildStrip@0x2261FB0
        const u = clamp01((clock - e.Delay) / Math.max(e.Life, 1e-4));
        const len = L(e.startHeight, e.endHeight, u) * s, hw = L(e.startWidth, e.endWidth, u) * s * 0.5;
        if (len > 0.01 && hw > 0.001) {
          const k = ramp(e, u), d = live ? forwardFlat() : dir, sx = d.z, sz = -d.x;
          const n = Math.max(2, Math.ceil(len + len)), cols = Math.max(2, nA), scroll = now * e.uvRotation * e.uvTile;
          for (let i = 0; i <= n; i++) {
            const dd = i * len / n + e.startRadius * s, uu = i / n * e.uvTile + scroll;
            for (let j = 0; j < cols; j++) {
              const t = j / (cols - 1), w = (t + t - 1) * hw;
              add(c.x + sx * w + d.x * dd, y0, c.z + sz * w + d.z * dd, uu, t, k);
            }
          }
          for (let i = 0; i < n; i++) for (let j = 0; j < cols - 1; j++) {
            const q = i * cols + j;
            idx.push(q, q + 1, q + cols, q + cols, q + 1, q + cols + 1);
          }
        }
      }
      setMesh(m, pos, col, uv, idx);
    } };
  });
}
