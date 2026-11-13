// wardrobe/fxparts/shuriken.js: Unity's ParticleSystem ("Shuriken") and its ParticleSystemRenderer, for TTO's effects
// (plans/fx_wolf/tto.md section 3: zone Glints, shatter / shards Glass + Sparks, rake and burst rays, the waves' Sparks,
// the domain's Motes, the pulse's Sparkles). The component is UnityPy's read_typetree() of the ParticleSystem (field
// names as Unity serializes them: lengthInSec, looping, moveWithTransform, InitialModule, ShapeModule, EmissionModule,
// ...), the renderer the same node's "ParticleSystemRenderer" (nodeDef.comps), its material the node's mats[0].
// Shuriken is Unity's native engine code (no game source): the behaviour follows Unity's documented semantics (Manual,
// "Particle System modules"; ScriptReference ParticleSystem.*), field by field as serialized. TTO's own calls into it:
//   - EffectControl's after-life stops every system under the effect without clearing it: TTO1102:EffectControl::Update
//     @0x1A233A0, GetComponentsInChildren<ParticleSystem>(true) then ParticleSystem.Stop(false, StopEmitting) at
//     0x1A23661 -> stop() below (emission ends, the living particles run out).
//   - GroundHugEmitter feeds the domain's Motes (rate 0) with Emit(EmitParams { position, applyShapeToPosition, velocity },
//     n): TTO1102:GroundHugEmitter::EmitMotes@0x22627A0 (set_position 0x22629D6, Emit 0x2262ACC) -> emit() below.
// Everything is simulated in Unity's space and drawn in the Unity world of the effect (the mirror group's space): the
// quads are built there and the mesh, a child of the node so it goes when the node is destroyed, undoes the node's
// matrix. Approximations are marked APPROX.
// 2026-11-10 (the Sheep's TTO effects, plans/fx_sheep/tto.md "Probed 2026-11-10"): the simulation space read the right
// way round (moveWithTransform 1 = World: Unity's ParticleSystemSimulationSpace Local 0 / World 1 / Custom 2; it was read
// as 0 = world, so every TTO system simulated in the wrong space, the Wolf's too), World collision on the page's floor
// (the Sparks of gleamingBreath_exhale, grandCodex_cast, lucentBarrier_reflect), mesh particles (m_RenderMode 4: the
// shards and prism shells, the renderer's "mesh" from wardrobe_fx_tto.py). The curve readers are shared on
// api.curves (tto_sheep.js's Line / Trail renderers use them).
// 2026-11-10 (the Penguin's TTO effects, plans/fx_penguin/tto.md section 6 parts P2 and P6): the TrailModule (particle
// ribbons: the meteors of constellation_star's Meteor1, constellation_giant's Giant1 / Escort1 and
// constellation_giantImpact's Five), drawn with the renderer's second material (Unity's trailMaterial, m_Materials[1]);
// Unity's built-in Quad as a mesh particle's mesh (emperorPenguin_launch's Ring1-3, emperorPenguin_goal's Net / Net2:
// the renderer's m_Mesh is a reference into "unity default resources", path id 10210, which no bundle holds;
// wardrobe_fx_tto.py BUILTIN_MESH writes it inline, and QUAD below stands in for data built before that). No Wolf or
// Sheep system enables a TrailModule or names a built-in mesh (their fx.json, checked 2026-11-10), so what they draw
// is unchanged.
// 2026-11-13 (the Monkey's TTO effects, plans/fx_monkey/parts.md T3, decision 62): SubModule (sub-emitters), NoiseModule
// (APPROX) and LightsModule (APPROX, api.pointLight), compile() below. A system that enables none of them runs exactly as
// before (every new path is gated on P.subs / P.noise / P.lights; emitRange's carry moved into `main`, the same number).
export default function register(api) {
  const { THREE } = api;
  const V = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);
  const DEG = Math.PI / 180, G = -9.81;                       // Physics.gravity (Unity's default; TTO never sets it here)
  const num = (x, d = 0) => (typeof x === "number" ? x : typeof x === "boolean" ? +x : d);
  const on = x => x === true || x === 1;
  const clamp01 = x => (x < 0 ? 0 : x > 1 ? 1 : x);
  const lerp = (a, b, k) => a + (b - a) * k;
  const frac = x => x - Math.floor(x);
  const vec = (o, d = [0, 0, 0]) => (!o ? d : Array.isArray(o) ? [num(o[0], d[0]), num(o[1], d[1]), num(o[2], d[2])]
    : [num(o.x, d[0]), num(o.y, d[1]), num(o.z, d[2])]);
  const rgba = o => {
    if (!o) return [1, 1, 1, 1];
    if (Array.isArray(o)) return [num(o[0], 1), num(o[1], 1), num(o[2], 1), num(o[3], 1)];
    if (!("r" in o) && "rgba" in o) { const v = o.rgba >>> 0; return [(v & 255) / 255, ((v >>> 8) & 255) / 255, ((v >>> 16) & 255) / 255, (v >>> 24) / 255]; }
    return [num(o.r, 1), num(o.g, 1), num(o.b, 1), num(o.a, 1)];
  };
  // the game's colours are gamma values; the page's vertex colours are linear (as index.html's ramp / linRGBA)
  const toLin = c => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
  const lin = c => [toLin(c[0]), toLin(c[1]), toLin(c[2]), c[3]];
  const randUnit = () => { const z = 2 * Math.random() - 1, a = 2 * Math.PI * Math.random(), r = Math.sqrt(1 - z * z); return V(r * Math.cos(a), r * Math.sin(a), z); };
  const finite = x => typeof x === "number" && Number.isFinite(x) && Math.abs(x) < 1e30;
  // smooth 3D value noise in [-1, 1] (the NoiseModule's APPROX, compile() below): hashed lattice values, smoothstep-blended
  const hash3 = (x, y, z) => { const s = Math.sin(x * 127.1 + y * 311.7 + z * 74.7) * 43758.5453; return s - Math.floor(s); };
  const vnoise = (x, y, z) => {
    const ix = Math.floor(x), iy = Math.floor(y), iz = Math.floor(z), sm = t => t * t * (3 - 2 * t);
    const fx = sm(x - ix), fy = sm(y - iy), fz = sm(z - iz);
    const e = (a, b, c) => hash3(ix + a, iy + b, iz + c);
    const l = (a, b, k) => a + (b - a) * k;
    return 2 * l(l(l(e(0, 0, 0), e(1, 0, 0), fx), l(e(0, 1, 0), e(1, 1, 0), fx), fy),
                 l(l(e(0, 0, 1), e(1, 0, 1), fx), l(e(0, 1, 1), e(1, 1, 1), fx), fy), fz) - 1;
  };
  // Unity's built-in Quad ("unity default resources" path id 10210; wardrobe_fx_tto.py BUILTIN_MESH, the same numbers):
  // 1 x 1 in the XY plane about its centre, normal -z, triangles 0 3 1 / 3 0 2
  const QUAD = { name: "Quad", verts: 4, pos: [-0.5, -0.5, 0, 0.5, -0.5, 0, -0.5, 0.5, 0, 0.5, 0.5, 0],
    nrm: [0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1], uv: [0, 0, 1, 0, 0, 1, 1, 1], col: null, idx: [0, 3, 1, 3, 0, 2], sub: [[0, 6]] };
  const builtinMesh = r => (r && typeof r === "object" && (r.builtin === 10210 || r.pathID === 10210) ? QUAD : null);

  // ---- AnimationCurve: Unity's Hermite between keys; an infinite tangent = stepped (holds the left key); weighted
  // tangents (weightedMode 1 in / 2 out / 3 both) = Unity's cubic Bezier with the key weights; clamped outside the keys
  // (APPROX: m_PreInfinity / m_PostInfinity loop and ping-pong are not used by particle curves, which run 0..1)
  function curveFn(cv) {
    const ks = (Array.isArray(cv) ? cv : cv?.m_Curve) || [];
    const K = ks.map(k => ({ t: num(k.time), v: num(k.value), i: k.inSlope, o: k.outSlope, w: num(k.weightedMode),
                             wi: num(k.inWeight, 1 / 3), wo: num(k.outWeight, 1 / 3) }));
    if (!K.length) return () => 0;
    if (K.length === 1) return () => K[0].v;
    const last = K[K.length - 1];
    return t => {
      if (t <= K[0].t) return K[0].v;
      if (t >= last.t) return last.v;
      let lo = 0, hi = K.length - 1;
      while (hi - lo > 1) { const m = (lo + hi) >> 1; if (K[m].t <= t) lo = m; else hi = m; }
      const a = K[lo], b = K[hi], dx = b.t - a.t;
      if (!(dx > 0) || !finite(a.o) || !finite(b.i)) return a.v;
      const s = (t - a.t) / dx, m0 = a.o * dx, m1 = b.i * dx;
      if ((a.w & 2) || (b.w & 1)) {                         // weighted: Bezier, x(u) solved by bisection
        const w0 = a.w & 2 ? a.wo : 1 / 3, w1 = b.w & 1 ? b.wi : 1 / 3;
        const bz = (p0, p1, p2, p3, u) => { const n = 1 - u; return n * n * n * p0 + 3 * n * n * u * p1 + 3 * n * u * u * p2 + u * u * u * p3; };
        let l = 0, h = 1, u = s;
        for (let it = 0; it < 24; it++) { u = (l + h) / 2; if (bz(0, w0, 1 - w1, 1, u) < s) l = u; else h = u; }
        return bz(a.v, a.v + w0 * m0, b.v - w1 * m1, b.v, u);
      }
      const s2 = s * s, s3 = s2 * s;
      return (2 * s3 - 3 * s2 + 1) * a.v + (s3 - 2 * s2 + s) * m0 + (-2 * s3 + 3 * s2) * b.v + (s3 - s2) * m1;
    };
  }
  // ---- MinMaxCurve: minMaxState 0 constant (scalar), 1 curve (scalar x maxCurve), 2 random between two curves (both
  // x scalar), 3 random between two constants (minScalar..scalar); r = the particle's own random for that property.
  // Returns f(t, r) with f.k = true when it is a constant (f.c)
  function mmCurve(c, def = 0) {
    let f;
    if (c == null) f = () => def, f.k = true, f.c = def;
    else if (typeof c === "number") f = () => c, f.k = true, f.c = c;
    else {
      const st = num(c.minMaxState), S = num(c.scalar, def), m = num(c.minScalar, 0);
      if (st === 0) f = () => S, f.k = true, f.c = S;
      else if (st === 3) f = (t, r) => m + (S - m) * r;
      else {
        const mx = curveFn(c.maxCurve);
        if (st === 1) f = t => S * mx(t);
        else { const mn = curveFn(c.minCurve); f = (t, r) => { const a = mn(t); return S * (a + (mx(t) - a) * r); }; }
      }
    }
    return f;
  }
  // ---- Gradient: up to 8 colour keys (key<i>.rgb at ctime<i> / 65535) and 8 alpha keys (key<i>.a at atime<i>), each
  // interpolated on its own; m_Mode 0 blend, 1 fixed (the first key at or after t), 2 perceptual (APPROX: blended
  // linearly). Evaluated on the stored (gamma) values, then made linear: returns f(t) -> [r, g, b, a] linear
  function gradFn(g) {
    if (!g || !("key0" in g)) { const c = lin(rgba(g)); return () => c; }
    const nc = Math.max(1, Math.min(8, num(g.m_NumColorKeys, 2))), na = Math.max(1, Math.min(8, num(g.m_NumAlphaKeys, 2)));
    const ck = [], ak = [];
    for (let i = 0; i < nc; i++) { const k = rgba(g["key" + i]); ck.push([num(g["ctime" + i]) / 65535, k[0], k[1], k[2]]); }
    for (let i = 0; i < na; i++) ak.push([num(g["atime" + i]) / 65535, rgba(g["key" + i])[3]]);
    ck.sort((a, b) => a[0] - b[0]); ak.sort((a, b) => a[0] - b[0]);
    const fixed = num(g.m_Mode) === 1;
    const ev = (K, t, j) => {
      if (t <= K[0][0]) return K[0][j];
      const L = K[K.length - 1];
      if (t >= L[0]) return L[j];
      let i = 1; while (K[i][0] < t) i++;
      if (fixed) return K[i][j];
      const a = K[i - 1], b = K[i], d = b[0] - a[0];
      return d > 0 ? lerp(a[j], b[j], (t - a[0]) / d) : b[j];
    };
    return t => [toLin(ev(ck, t, 1)), toLin(ev(ck, t, 2)), toLin(ev(ck, t, 3)), ev(ak, t, 1)];
  }
  // ---- MinMaxGradient: 0 colour (maxColor), 1 gradient, 2 random between two colours, 3 between two gradients,
  // 4 random colour (a random point of maxGradient). Returns f(t, r) -> linear rgba, f.k when constant
  function mmGrad(c) {
    let f;
    if (!c) { const w = [1, 1, 1, 1]; f = () => w; f.k = true; return f; }
    if (!("minMaxState" in c)) { const g = gradFn(c); f = t => g(t); return f; }
    const st = num(c.minMaxState);
    if (st === 0) { const k = lin(rgba(c.maxColor)); f = () => k; f.k = true; }
    else if (st === 1) { const g = gradFn(c.maxGradient); f = t => g(t); }
    else if (st === 2) { const a = lin(rgba(c.minColor)), b = lin(rgba(c.maxColor)); f = (t, r) => a.map((x, j) => lerp(x, b[j], r)); }
    else if (st === 3) { const ga = gradFn(c.minGradient), gb = gradFn(c.maxGradient); f = (t, r) => { const a = ga(t), b = gb(t); return a.map((x, j) => lerp(x, b[j], r)); }; }
    else { const g = gradFn(c.maxGradient); f = (t, r) => g(r); }
    return f;
  }
  // MultiModeParameter (the shape's radius / arc): {value, mode 0 random / 1 loop / 2 ping-pong / 3 burst spread,
  // spread, speed (a MinMaxCurve)}; older files hold a plain number
  const mmp = (p, d) => (typeof p === "number" || p == null ? { value: num(p, d), mode: 0, spread: 0, speed: () => 0 }
    : { value: num(p.value, d), mode: num(p.mode), spread: num(p.spread), speed: mmCurve(p.speed, 1) });
  // a position along a MultiModeParameter, 0..1 (Unity's arc / edge modes); ctx = { t (system time), nt, i, n (burst) }
  const mmpPick = (p, ctx) => {
    let u;
    if (p.mode === 1) u = frac(ctx.t * p.speed(ctx.nt, 0));
    else if (p.mode === 2) { const x = frac(ctx.t * p.speed(ctx.nt, 0) / 2) * 2; u = x > 1 ? 2 - x : x; }
    else if (p.mode === 3 && ctx.n > 0) u = ctx.i / ctx.n;
    else u = Math.random();
    if (p.spread > 0) u = Math.floor(u / p.spread) * p.spread;
    return u;
  };

  // ---- ShapeModule: where a particle starts and which way it goes (shape space: then m_Position / m_Rotation /
  // m_Scale). Types as serialized: 0 sphere, 1 sphere shell, 2 hemisphere (+z half), 3 its shell, 4 cone (base),
  // 7 cone shell, 8 cone volume, 9 its shell, 5 box (volume, along +z), 15 box shell, 16 box edge, 10 circle (the XY
  // plane, outward), 11 circle edge, 12 single-sided edge (along x, emits +y), 17 donut, 18 rectangle (+z). radiusThickness
  // 1 = the whole volume, 0 = the surface. The module off: the centre, along +z. APPROX: mesh / sprite shapes (6, 13,
  // 14, 19, 20) emit from the centre; the direction turns with m_Rotation only (not m_Scale); alignToDirection ignored
  function shapeFn(sh) {
    if (!sh || !on(sh.enabled)) return null;
    const type = num(sh.type), R = mmp(sh.radius, 1), arc = mmp(sh.arc, 360), th = clamp01(num(sh.radiusThickness, 1));
    const ang = Math.min(90, Math.max(0, num(sh.angle, 25))) * DEG, len = num(sh.length, 5), dR = num(sh.donutRadius, 0.2);
    const pos = V(...vec(sh.m_Position)), scl = V(...vec(sh.m_Scale, [1, 1, 1]));
    const rot = new THREE.Quaternion().setFromEuler(new THREE.Euler(...vec(sh.m_Rotation).map(x => x * DEG), "YXZ"));   // Unity's Euler: z, x, y
    const rDir = num(sh.randomDirectionAmount), sDir = num(sh.sphericalDirectionAmount), rPos = num(sh.randomPositionAmount);
    const vol = (t, pw) => Math.pow(lerp(Math.pow(1 - t, pw), 1, Math.random()), 1 / pw);   // radius fraction, uniform in area / volume
    return ctx => {
      let p, d;
      const r0 = R.value, theta = () => mmpPick(arc, ctx) * arc.value * DEG;
      switch (type) {
        case 0: case 1: case 2: case 3: {
          d = randUnit(); if (type >= 2) d.z = Math.abs(d.z);
          p = d.clone().multiplyScalar(r0 * (type === 1 || type === 3 ? 1 : vol(th, 3))); break;
        }
        case 4: case 7: case 8: case 9: {
          const a = theta(), f = type === 7 || type === 9 ? 1 : vol(th, 2), c = Math.cos(a), s = Math.sin(a);
          p = V(c * f * r0, s * f * r0, 0);
          const k = (r0 > 0 ? f : Math.sqrt(Math.random())) * Math.tan(ang);   // aims at the matching point of the top circle
          d = V(c * k, s * k, 1).normalize();
          if (type >= 8) p.addScaledVector(d, Math.random() * len / d.z);
          break;
        }
        case 5: case 15: case 16: {
          p = V(Math.random() - .5, Math.random() - .5, Math.random() - .5);
          if (type === 15) { const k = Math.floor(Math.random() * 3); p.setComponent(k, Math.random() < .5 ? -.5 : .5); }
          if (type === 16) { const k = Math.floor(Math.random() * 3); for (let j = 0; j < 3; j++) if (j !== k) p.setComponent(j, Math.random() < .5 ? -.5 : .5); }
          d = V(0, 0, 1); break;
        }
        case 10: case 11: {
          const a = theta(), f = type === 11 ? 1 : vol(th, 2);
          d = V(Math.cos(a), Math.sin(a), 0); p = d.clone().multiplyScalar(f * r0); break;
        }
        case 12: p = V(r0 * (2 * mmpPick(R, ctx) - 1), 0, 0); d = V(0, 1, 0); break;
        case 17: {
          const a = theta(), c = V(Math.cos(a) * r0, Math.sin(a) * r0, 0), b = Math.random() * 2 * Math.PI, rr = dR * vol(th, 2);
          d = V(Math.cos(a) * Math.cos(b), Math.sin(a) * Math.cos(b), Math.sin(b)); p = c.addScaledVector(d, rr); break;
        }
        case 18: p = V(Math.random() - .5, Math.random() - .5, 0); d = V(0, 0, 1); break;
        default: p = V(); d = V(0, 0, 1);
      }
      p.multiply(scl).applyQuaternion(rot).add(pos);
      d.applyQuaternion(rot);
      if (sDir > 0) { const o = p.clone().sub(pos); if (o.lengthSq() > 1e-12) d.lerp(o.normalize(), sDir); }
      if (rDir > 0) d.lerp(randUnit(), rDir);
      if (d.lengthSq() > 1e-12) d.normalize(); else d.set(0, 0, 1);
      if (rPos > 0) p.addScaledVector(randUnit(), Math.random() * rPos);
      return { p, d };
    };
  }

  // ---- the whole system's settings, compiled once per component (the data is shared by every spawn: never mutated)
  const CACHE = new WeakMap();
  function compile(ps) {
    if (CACHE.has(ps)) return CACHE.get(ps);
    const I = ps.InitialModule || {}, E = ps.EmissionModule || {}, mod = n => (on(ps[n]?.enabled) ? ps[n] : null);
    const P = {
      dur: Math.max(0.05, num(ps.lengthInSec, 5)), loop: on(ps.looping), prewarm: on(ps.prewarm),
      playOnAwake: ps.playOnAwake == null ? true : on(ps.playOnAwake), delay: mmCurve(ps.startDelay, 0),
      // moveWithTransform is the serialized simulation space (ParticleSystemSimulationSpace): 0 local, 1 world, 2 custom
      // (APPROX: custom = local). The Sheep's prefabs agree: the wisp's Orbit (0) rides with it, its Sparkle (1) stays
      // behind; the book's Astrolabe (0) hangs under it, its Glyphs (1) rise from where it was
      world: num(ps.moveWithTransform, 0) === 1, scaling: num(ps.scalingMode, 1), simSpeed: num(ps.simulationSpeed, 1),
      stopAction: num(ps.stopAction), max: Math.max(0, num(I.maxNumParticles, 1000)),
      life: mmCurve(I.startLifetime, 5), speed: mmCurve(I.startSpeed, 5), color: mmGrad(I.startColor),
      size: mmCurve(I.startSize, 1), sizeY: mmCurve(I.startSizeY, 1), sizeZ: mmCurve(I.startSizeZ, 1), size3D: on(I.size3D),
      rotX: mmCurve(I.startRotationX, 0), rotY: mmCurve(I.startRotationY, 0), rot: mmCurve(I.startRotation, 0), rot3D: on(I.rotation3D),
      flipRot: num(I.randomizeRotationDirection), grav: mmCurve(I.gravityModifier ?? ps.gravityModifier, 0),
      shape: shapeFn(ps.ShapeModule),
    };
    if (on(E.enabled)) {
      P.rate = mmCurve(E.rateOverTime ?? E.rate, 0); P.rateD = mmCurve(E.rateOverDistance, 0);
      const bs = E.m_Bursts || [];
      P.bursts = bs.slice(0, E.m_BurstCount ?? bs.length).map(b => ({
        time: num(b.time), cycles: num(b.cycleCount, 1), interval: Math.max(1e-4, num(b.repeatInterval, 0.01)),
        prob: num(b.probability, 1),
        count: b.countCurve != null ? mmCurve(b.countCurve, 30) : ((t, r) => lerp(num(b.minCount), num(b.maxCount), r)) }));
    } else P.bursts = [];
    let m;
    if ((m = mod("VelocityModule"))) P.vel = { x: mmCurve(m.x), y: mmCurve(m.y), z: mmCurve(m.z), world: on(m.inWorldSpace),
      orb: [mmCurve(m.orbitalX), mmCurve(m.orbitalY), mmCurve(m.orbitalZ)], off: [mmCurve(m.orbitalOffsetX), mmCurve(m.orbitalOffsetY), mmCurve(m.orbitalOffsetZ)],
      radial: mmCurve(m.radial), speedMod: mmCurve(m.speedModifier, 1) };
    if ((m = mod("InheritVelocityModule"))) P.inherit = { mode: num(m.m_Mode), k: mmCurve(m.m_Curve, 0) };
    if ((m = mod("ForceModule"))) P.force = { x: mmCurve(m.x), y: mmCurve(m.y), z: mmCurve(m.z), world: on(m.inWorldSpace), perFrame: on(m.randomizePerFrame) };
    if ((m = mod("ClampVelocityModule"))) P.limit = { sep: on(m.separateAxis), x: mmCurve(m.x, 1), y: mmCurve(m.y, 1), z: mmCurve(m.z, 1),
      mag: mmCurve(m.magnitude, 1), world: on(m.inWorldSpace), dampen: num(m.dampen, 1), drag: mmCurve(m.drag, 0),
      dragSize: on(m.multiplyDragByParticleSize), dragVel: on(m.multiplyDragByParticleVelocity) };
    if ((m = mod("LifetimeByEmitterSpeedModule"))) P.lifeBySpeed = { k: mmCurve(m.m_Curve, 1), range: vec(m.m_Range, [0, 1]) };
    if ((m = mod("SizeModule"))) P.sizeOL = { sep: on(m.separateAxes), x: mmCurve(m.curve, 1), y: mmCurve(m.y, 1), z: mmCurve(m.z, 1) };
    if ((m = mod("SizeBySpeedModule"))) P.sizeBS = { sep: on(m.separateAxes), x: mmCurve(m.curve, 1), y: mmCurve(m.y, 1), range: vec(m.range, [0, 1]) };
    if ((m = mod("RotationModule"))) P.rotOL = { sep: on(m.separateAxes), x: mmCurve(m.x), y: mmCurve(m.y), z: mmCurve(m.curve) };
    if ((m = mod("RotationBySpeedModule"))) P.rotBS = { sep: on(m.separateAxes), x: mmCurve(m.x), y: mmCurve(m.y), z: mmCurve(m.curve), range: vec(m.range, [0, 1]) };
    if ((m = mod("ColorModule"))) P.colOL = mmGrad(m.gradient);
    if ((m = mod("ColorBySpeedModule"))) P.colBS = { g: mmGrad(m.gradient), range: vec(m.range, [0, 1]) };
    if ((m = mod("UVModule")) && num(m.mode) === 0) P.uv = { tx: Math.max(1, num(m.tilesX, 1)), ty: Math.max(1, num(m.tilesY, 1)),
      time: num(m.timeMode), fps: num(m.fps, 30), frame: mmCurve(m.frameOverTime, 0), start: mmCurve(m.startFrame, 0),
      speedRange: vec(m.speedRange, [0, 1]), row: num(m.animationType) === 1, rowMode: num(m.rowMode, 1), rowIndex: num(m.rowIndex),
      cycles: num(m.cycles, 1), flipU: num(m.flipU), flipV: num(m.flipV) };
    // CollisionModule type 1 (World) against the page's floor, the only collider it has (y 0 of the effect's Unity world
    // = the hero's feet). Unity's world collision also meets the heroes' colliders and the map: APPROX, the floor only.
    // m_Dampen: the share of the speed along the floor lost, m_Bounce: the share of the speed into the floor sent back,
    // m_EnergyLossOnCollision: the share of the lifetime lost, min/maxKillSpeed: killed after a hit outside that speed,
    // radiusScale x half the particle's size = its radius (APPROX: its start size, not the size over its life)
    if ((m = mod("CollisionModule")) && num(m.type) === 1) P.coll = { dampen: mmCurve(m.m_Dampen, 0), bounce: mmCurve(m.m_Bounce, 1),
      loss: mmCurve(m.m_EnergyLossOnCollision, 0), minKill: num(m.minKillSpeed), maxKill: num(m.maxKillSpeed, 1e4), radius: num(m.radiusScale, 1) };
    // TrailModule (Unity's Manual "Trails module"; fields as serialized): mode 0 Particles = each particle leaves a
    // trail (a share `ratio` of them, picked at birth), 1 Ribbon = a strip through the living particles by age
    // (ribbonCount strips); lifetime = how long each trail point lives, a multiplier of its particle's lifetime
    // (sizeAffectsLifetime: x its size too); a point is added once the particle has moved minVertexDistance from the
    // last; worldSpace: the points stay where they were made even in a Local system (a World system's are world anyway);
    // dieWithParticles: the trail goes with its particle, else it stays and its points run out; widthOverTrail and
    // colorOverTrail along the trail (0 = the particle's end, 1 = the oldest point), colorOverLifetime over the
    // particle's life, inheritParticleColor (x the particle's colour), sizeAffectsWidth (x its size); textureMode 0
    // Stretch (u 0..1 along the trail), 1 Tile (u = metres x textureScale.x), 2 DistributePerSegment, 3 RepeatPerSegment.
    // Drawn facing the camera (Unity's trail alignment View), with the renderer's trail material (m_Materials[1]).
    // APPROX: the curves along the trail run by its share of the length (as tto_sheep.js's LineRenderer); lifetime is
    // read at the particle's birth; a Ribbon's width and colour keys are its particles' (nearest); generateLightingData,
    // shadowBias, splitSubEmitterRibbons and attachRibbonsToTransform are not read (no lights or sub-emitters here)
    if ((m = mod("TrailModule"))) P.trail = { mode: num(m.mode), ratio: num(m.ratio, 1), life: mmCurve(m.lifetime, 1),
      minD: Math.max(0, num(m.minVertexDistance, 0.2)), world: on(m.worldSpace), die: on(m.dieWithParticles),
      sizeW: on(m.sizeAffectsWidth), sizeL: on(m.sizeAffectsLifetime), inherit: m.inheritParticleColor == null ? true : on(m.inheritParticleColor),
      colLife: mmGrad(m.colorOverLifetime), width: mmCurve(m.widthOverTrail, 1), colTrail: mmGrad(m.colorOverTrail),
      ribbons: Math.max(1, num(m.ribbonCount, 1)), tex: num(m.textureMode), texScale: vec(m.textureScale, [1, 1, 1]) };
    // 2026-11-13, the Monkey (plans/fx_monkey/parts.md T3, Interfaces 6, decision 62; tto_monkey builder):
    // SubModule (Unity's Manual "Sub Emitters module"): subEmitters[] = { emitter: {node: i} (a system of the same
    // effect), type 0 Birth / 1 Collision / 2 Death, properties (bit mask: 1 colour, 2 size, 4 rotation, 8 lifetime, 16
    // duration; only 2, InheritSize, is read: the child's start size x the parent particle's size), emitProbability }.
    // The child is built idle (it never plays by itself, as Unity's sub-emitter systems) and runs one emission instance
    // per trigger: Birth = from the parent particle's birth, following it, while it lives (looping as the child's own
    // duration loops); Collision / Death = one pass of the child's duration at the hit / death point. An instance runs the
    // child's own rate over time and bursts (runeGolem_quake's crystals: a burst of 1 every 0.04 s, 10 cycles, so each
    // flying carrier leaves a short trail). Every Monkey sub-emitter is Birth with InheritSize (buitenBastion_rise,
    // runeGolem_rise / _quake / _pound / _crumble).
    // NoiseModule: APPROX, a cheap smooth value noise in place of Unity's curl noise: per axis a velocity offset in
    // [-1, 1] x strength (x positionAmount; damping: / frequency), sampled at the particle's position x frequency + the
    // scroll (scrollSpeed x time), not kept in the velocity (as Unity's); octaves, quality, remap, rotation and size
    // amounts are not read (jaAscension_pillar's / runeGolem_rise's Sparks Confetti Noise: strength 0.2, 1 octave).
    // LightsModule: APPROX, through api.pointLight (the scene's two pooled point lights, index.html): at most two lights
    // per system (min(maxLights, 2)), on its brightest particles among the share `ratio` picked at birth; the template is
    // the module's `light` (a Light component of the effect, usually disabled itself): colour x the particle's colour
    // (`color`), range m_Range x rangeCurve (x the particle's size: `range`), intensity m_Intensity x intensityCurve (x
    // its alpha: `intensity`), x 2 pi as fxparts/light.js scales a light. Released when the system has no particles, its
    // node leaves the stage or the effect goes.
    // CustomDataModule: nothing to draw (no page shader reads custom data).
    if ((m = mod("SubModule"))) P.subs = (m.subEmitters || []).filter(s => typeof s?.emitter?.node === "number")
      .map(s => ({ node: s.emitter.node, type: num(s.type), size: (num(s.properties) & 2) !== 0, p: num(s.emitProbability, 1) }));
    if ((m = mod("NoiseModule"))) P.noise = { sep: on(m.separateAxes), x: mmCurve(m.strength, 1), y: mmCurve(m.strengthY, 1),
      z: mmCurve(m.strengthZ, 1), freq: Math.max(1e-4, num(m.frequency, 0.5)), damp: on(m.damping), scroll: mmCurve(m.scrollSpeed, 0),
      amount: mmCurve(m.positionAmount, 1) };
    if ((m = mod("LightsModule"))) P.lights = { ref: m.light, ratio: num(m.ratio, 0), max: Math.min(2, num(m.maxLights, 20)),
      col: on(m.color), sizeRange: on(m.range), alphaI: on(m.intensity), range: mmCurve(m.rangeCurve, 1), inten: mmCurve(m.intensityCurve, 1) };
    // not drawn (no prefab of the classes built so far enables them): ExternalForces, Collision with planes (type 0),
    // Trigger; the UV module's sprite mode
    P.skipped = ["ExternalForcesModule", "CollisionModule", "TriggerModule", "TrailModule"]
      .filter(n => mod(n) && !(n === "CollisionModule" && P.coll) && !(n === "TrailModule" && P.trail));
    if (P.skipped.length) console.warn("Shuriken: not drawn", P.skipped.join(", "));
    CACHE.set(ps, P);
    return P;
  }
  const speedT = (s, r) => (r[1] > r[0] ? clamp01((s - r[0]) / (r[1] - r[0])) : 0);

  function build(fx, node, ps, mat, nodeDef, data) {
    const P = compile(ps);
    const rd = nodeDef.comps.find(c => c.type === "ParticleSystemRenderer") || {};
    if (!mat) {                                                // the renderer's own material list, if the reader put it there
      const nm = (rd.mats || rd.materials || []).find(x => typeof x === "string");
      if (nm && data.materials?.[nm]) mat = api.fxMaterial(fx.cls, nm, data.materials[nm]);
    }
    const RM = num(rd.m_RenderMode), drawn = mat && RM !== 5 && rd.m_Enabled !== 0 && rd.m_Enabled !== false;
    // mesh particles: the renderer's m_Mesh (wardrobe_fx_tto.py), or Unity's built-in Quad it names
    const pMesh = RM === 4 ? (rd.mesh?.verts ? rd.mesh : builtinMesh(rd.m_Mesh)) : null;
    const mesh = drawn ? api.fxMesh(node, mat) : null;
    if (mesh) { mesh.matrixAutoUpdate = false; mesh.renderOrder = num(rd.m_SortingOrder); }
    // the trails' own mesh: the renderer's trail material (drawn with render mode None too: trails only)
    let tmesh = null;
    if (P.trail && rd.m_Enabled !== 0 && rd.m_Enabled !== false) {
      const tn = (rd.m_Materials || [])[1], td = typeof tn === "string" ? data.materials?.[tn] : null;
      if (td) { tmesh = api.fxMesh(node, api.fxMaterial(fx.cls, tn, td)); tmesh.matrixAutoUpdate = false; tmesh.renderOrder = num(rd.m_SortingOrder); }
      else console.warn("Shuriken: a TrailModule with no trail material (m_Materials[1])", fx.name, node.name);
    }
    const lenScale = num(rd.m_LengthScale, 2), velScale = num(rd.m_VelocityScale), align = num(rd.m_RenderAlignment);
    const sortMode = num(rd.m_SortMode), minSize = num(rd.m_MinParticleSize), maxSize = num(rd.m_MaxParticleSize, 0.5);
    const pivot = vec(rd.m_Pivot);

    // a sub-emitter's child (SubModule, compile() above) is built idle: its parent, an earlier node of the same effect,
    // listed it in fx.shurikenSubs at its own build (asSub() below covers any other order)
    if (P.subs) { fx.shurikenSubs ||= new Set(); for (const s of P.subs) fx.shurikenSubs.add(s.node); }
    let isSub = !!fx.shurikenSubs?.has(fx.nodes?.indexOf(node));
    const parts = [];
    let ghosts = [];                         // the trails of dead particles (dieWithParticles off): { pts, life, k, w }
    let time = 0, delay = -1, emitting = P.playOnAwake && !isSub, played = P.playOnAwake && !isSub, ended = false, ready = false;
    const main = { acc: 0 };                 // the rate's carry (a sub-emitter instance keeps its own)
    let accD = 0, noiseT = 0;
    const inst = [];                         // this child's sub-emitter instances: { t, acc, o, loop, done }
    const pending = [];
    // this frame's emitter: Unity-world position T, rotation Rq (Ri inverse), Sm = the scale the simulation sees
    // (scalingMode 0 hierarchy: the lossy scale, 1 local: the node's own, 2 shape: none, the shape alone is scaled by
    // the lossy scale, Ssh); sizeK = the particles' size factor; gSim = gravity in simulation space
    const T = V(), Rq = new THREE.Quaternion(), Ri = new THREE.Quaternion(), lossy = V(1, 1, 1), Sm = V(1, 1, 1), Ssh = V(1, 1, 1);
    const lastT = V(), eVel = V(), gSim = V(), camPos = V(), M = new THREE.Matrix4(), Minv = new THREE.Matrix4();
    let sizeK = 1, haveLast = false, tanHalf = 0;
    const safe = v => V(Math.abs(v.x) < 1e-6 ? 1e-6 : v.x, Math.abs(v.y) < 1e-6 ? 1e-6 : v.y, Math.abs(v.z) < 1e-6 ? 1e-6 : v.z);
    const frame = dt => {
      M.copy(fx.uMatrix(node));
      M.decompose(T, Rq, lossy); Ri.copy(Rq).invert();
      Sm.copy(P.scaling === 0 ? lossy : P.scaling === 1 ? node.scale : V(1, 1, 1));
      Ssh.copy(P.scaling === 2 ? lossy : V(1, 1, 1));
      sizeK = (Math.abs(Sm.x) + Math.abs(Sm.y) + Math.abs(Sm.z)) / 3;
      if (haveLast && dt > 0) eVel.copy(T).sub(lastT).divideScalar(dt); else eVel.set(0, 0, 0);
      lastT.copy(T); haveLast = true;
      gSim.copy(worldToSimDir(V(0, G, 0)));
      api.camera.getWorldPosition(camPos).applyMatrix4(fx.mirrorInv);
      tanHalf = api.camera.isPerspectiveCamera ? Math.tan(api.camera.fov * DEG / 2) : 0;
    };
    // simulation space <-> the effect's Unity world (local: T + R (Sm x p); world: as is)
    const toWorld = p => (P.world ? p.clone() : p.clone().multiply(Sm).applyQuaternion(Rq).add(T));
    const toWorldDir = v => (P.world ? v.clone() : v.clone().multiply(Sm).applyQuaternion(Rq));
    const worldToSimDir = w => (P.world ? w.clone() : w.clone().applyQuaternion(Ri).divide(safe(Sm)));
    const localToSimDir = v => (P.world ? v.clone().multiply(Sm).applyQuaternion(Rq) : v.clone());

    // one particle. bi / bn: its place in a burst (the shape's burst-spread mode); o: Emit()'s EmitParams
    function emitOne(tau, preAge, bi = 0, bn = 0, o = null) {
      if (parts.length >= P.max) return;
      const nt = clamp01(tau / P.dur);                          // start values run over the system's duration
      let life = P.life(nt, Math.random());
      if (o?.startLifetime != null) life = o.startLifetime;
      if (P.lifeBySpeed) life *= P.lifeBySpeed.k(speedT(eVel.length(), P.lifeBySpeed.range), Math.random());
      if (!(life > 0)) return;
      const sh = P.shape ? P.shape({ t: tau, nt, i: bi, n: bn }) : { p: V(), d: V(0, 0, 1) };
      let p = sh.p.multiply(Ssh), v = sh.d.multiplyScalar(P.speed(nt, Math.random()));
      if (o?.position) { const q = V(...vec(o.position)); p = o.applyShapeToPosition ? q.add(p) : q; }
      if (o?.velocity) v = V(...vec(o.velocity));
      const given = o?.space === "world";                       // emit() positions / velocities already in Unity world
      if (P.world) {
        if (!(o?.position && given)) p = p.multiply(Sm).applyQuaternion(Rq).add(T);
        if (!(o?.velocity && given)) v = v.multiply(Sm).applyQuaternion(Rq);
        // InheritVelocity acts on world-space systems only; mode 0 initial: the emitter's velocity x the curve at birth
        if (P.inherit && P.inherit.mode === 0) v.addScaledVector(eVel, P.inherit.k(0, Math.random()));
      } else {
        if (o?.position && given) p = p.sub(T).applyQuaternion(Ri).divide(safe(Sm));
        if (o?.velocity && given) v = worldToSimDir(v);
      }
      const s = P.size(nt, Math.random());
      const size = o?.startSize != null ? V(o.startSize, o.startSize, o.startSize)
        : P.size3D ? V(s, P.sizeY(nt, Math.random()), P.sizeZ(nt, Math.random())) : V(s, s, s);
      if (o?.sizeMul != null) size.multiplyScalar(o.sizeMul);   // a sub-emitter's InheritSize (SubModule)
      const flip = Math.random() < P.flipRot ? -1 : 1;
      const rot = o?.rotation != null ? V(0, 0, o.rotation * DEG)
        : V(P.rot3D ? P.rotX(nt, Math.random()) : 0, P.rot3D ? P.rotY(nt, Math.random()) : 0, P.rot(nt, Math.random())).multiplyScalar(flip);
      const c0 = o?.startColor ? lin(rgba(o.startColor)) : P.color(nt, Math.random());
      const R = Array.from({ length: 16 }, Math.random);       // the particle's own randoms, one per curve
      const q = { p, v, vt: v.clone(), age: 0, life, size, rot, flip, c0, R, sf: P.uv ? P.uv.start(nt, R[10]) : 0,
                  row: P.uv ? Math.floor(R[12] * P.uv.ty) : 0 };
      if (P.trail && P.trail.mode === 0 && Math.random() < P.trail.ratio) {   // its trail starts where it is born
        q.tr = [{ p: trailPt(p), a: preAge, fresh: true }];
        q.trLife = P.trail.life(nt, Math.random()) * life * (P.trail.sizeL ? size.x : 1);
      }
      if (P.lights) q.lit = Math.random() < P.lights.ratio;    // the LightsModule's share, picked at birth
      if (preAge > 0 && !step(q, preAge)) return;              // emitted inside the frame: run the rest of it
      parts.push(q);
      if (P.subs) subBirth(q);
    }
    // one particle forward by dt; false = it died
    const tmp = V();
    function step(q, dt) {
      q.age += dt;
      if (q.age >= q.life) return false;
      const u = q.age / q.life, R = q.R;
      const g = P.grav(u, R[13]);                              // APPROX: a gravity curve runs over the particle's life
      if (g) q.v.addScaledVector(gSim, g * dt);
      if (P.force) {
        const f = P.force, rr = f.perFrame ? [Math.random(), Math.random(), Math.random()] : [R[3], R[4], R[5]];
        tmp.set(f.x(u, rr[0]), f.y(u, rr[1]), f.z(u, rr[2]));
        q.v.addScaledVector(f.world ? worldToSimDir(tmp) : localToSimDir(tmp), dt);
      }
      if (P.limit) {                                           // Limit Velocity: dampen = the share of the excess removed
        const L = P.limit, k = 1 - Math.pow(1 - clamp01(L.dampen), dt * 30);   // APPROX: Unity's per-frame dampen at 30 fps
        const vv = L.world ? toWorldDir(q.v) : q.v.clone();
        if (L.sep) {
          const lim = [L.x(u, R[6]), L.y(u, R[6]), L.z(u, R[6])];
          for (let j = 0; j < 3; j++) { const c = vv.getComponent(j), a = Math.abs(lim[j]); if (Math.abs(c) > a) vv.setComponent(j, lerp(c, Math.sign(c) * a, k)); }
        } else { const sp = vv.length(), a = Math.abs(L.mag(u, R[6])); if (sp > a && sp > 0) vv.multiplyScalar(lerp(1, a / sp, k)); }
        let drag = L.drag(u, R[14]);
        if (drag) {
          if (L.dragSize) drag *= q.size.x * q.size.x;
          if (L.dragVel) drag *= vv.lengthSq();
          vv.multiplyScalar(Math.max(0, 1 - drag * dt));
        }
        q.v.copy(L.world ? worldToSimDir(vv) : vv);
      }
      q.vt.copy(q.v);
      let sm = 1;
      if (P.vel) {                                             // Velocity over Lifetime: added to the motion, not kept
        const m = P.vel;
        tmp.set(m.x(u, R[0]), m.y(u, R[1]), m.z(u, R[2]));
        if (tmp.lengthSq()) q.vt.add(m.world ? worldToSimDir(tmp) : localToSimDir(tmp));
        const rad = m.radial(u, R[15]);
        if (rad) {
          const c = P.world ? T : V();
          const d = q.p.clone().sub(c); if (d.lengthSq() > 1e-12) q.vt.addScaledVector(d.normalize(), rad);
        }
        const w = V(m.orb[0](u, R[0]), m.orb[1](u, R[1]), m.orb[2](u, R[2]));
        if (w.lengthSq()) {                                    // orbital: turns the position about the centre + offset
          const c = V(m.off[0](u, 0), m.off[1](u, 0), m.off[2](u, 0));
          if (P.world) c.applyQuaternion(Rq).add(T);
          const a = w.length(), wq = new THREE.Quaternion().setFromAxisAngle(localToSimDir(w).normalize(), a * dt);
          q.p.sub(c).applyQuaternion(wq).add(c);
        }
        sm = m.speedMod(u, R[15]);
      }
      if (P.inherit && P.inherit.mode === 1 && P.world) q.vt.addScaledVector(eVel, P.inherit.k(u, R[13]));   // mode 1: current
      if (P.noise) {                                           // NoiseModule (APPROX, compile() above)
        const N = P.noise, f = N.freq, k = N.amount(u, R[6]) / (N.damp ? f : 1);
        const sx = N.x(u, R[3]), sy = N.sep ? N.y(u, R[4]) : sx, sz = N.sep ? N.z(u, R[5]) : sx;
        const X = q.p.x * f + noiseT, Y = q.p.y * f, Z = q.p.z * f;
        q.vt.x += vnoise(X, Y, Z) * sx * k; q.vt.y += vnoise(X + 31.7, Y + 11.3, Z) * sy * k; q.vt.z += vnoise(X, Y + 57.1, Z + 23.9) * sz * k;
      }
      q.p.addScaledVector(q.vt, sm * dt);
      if (P.coll && !collide(q, u)) return false;
      if (P.rotOL || P.rotBS) {                                // angular velocity (radians a second, as serialized)
        const sp = q.vt.length();
        for (const [m, t] of [[P.rotOL, u], [P.rotBS, P.rotBS ? speedT(sp, P.rotBS.range) : 0]]) {
          if (!m) continue;
          q.rot.z += m.z(t, R[8]) * dt * q.flip;
          if (m.sep) { q.rot.x += m.x(t, R[8]) * dt * q.flip; q.rot.y += m.y(t, R[8]) * dt * q.flip; }
        }
      }
      return true;
    }
    // the system's clock: start delay, then rate and bursts over [a, b) of the duration (looping wraps)
    // (o, st: a sub-emitter instance's EmitParams and its own carry; its spot is its parent particle's, so no rate over
    // distance)
    function emitRange(a, b, extra, o = null, st = main) {
      const dur = P.dur, nt = a / dur;
      const rate = P.rate ? P.rate(nt, Math.random()) : 0;
      if (rate > 0) {
        const before = st.acc; st.acc += rate * (b - a);
        const n = Math.floor(st.acc);
        for (let k = 1; k <= n; k++) { const tau = a + (k - before) / rate; emitOne(tau, b - tau + extra, 0, 0, o); }
        st.acc -= n;
      }
      const rd2 = !o && P.rateD ? P.rateD(nt, Math.random()) : 0;
      if (rd2 > 0) {                                           // rate over distance: the emitter's own travel
        const before = accD; accD += rd2 * eVel.length() * (b - a);
        const n = Math.floor(accD);
        for (let k = 1; k <= n; k++) { const tau = a + (b - a) * (k - before) / Math.max(1e-9, accD - before); emitOne(tau, b - tau + extra); }
        accD -= n;
      }
      for (const B of P.bursts) {
        const cc = B.cycles <= 0 ? Infinity : B.cycles;
        for (let j = Math.max(0, Math.ceil((a - B.time) / B.interval - 1e-6)); j < cc && j < 1e5; j++) {
          const tau = B.time + j * B.interval;
          if (tau >= b) break;
          if (tau < a || Math.random() >= B.prob) continue;
          const n = Math.max(0, Math.round(B.count(tau / dur, Math.random())));
          for (let i = 0; i < n; i++) emitOne(tau, b - tau + extra, i, n, o);
        }
      }
    }
    function advance(dt) {
      let left = dt;
      if (delay > 0) { const k = Math.min(delay, left); delay -= k; left -= k; if (delay > 0) return; }
      while (left > 1e-9 && emitting) {
        const st = Math.min(left, P.dur - time);
        emitRange(time, time + st, left - st);
        time += st; left -= st;
        if (time >= P.dur - 1e-9) { if (P.loop) time = 0; else emitting = false; }
      }
    }
    // World collision with the floor (P.coll above): false = the hit killed it
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
      if (P.subs) subTrigger(q, 1);                            // a Collision sub-emitter, at the hit point
      const sp = v.length();
      return q.age < q.life && sp >= C.minKill && sp <= C.maxKill;
    }
    function stepAll(dt) {                                     // dead ones swap-removed, as Unity's particle buffer
      for (let i = parts.length - 1; i >= 0; i--) if (!step(parts[i], dt)) {
        const q = parts[i];                                    // its trail stays (dieWithParticles off) and runs out
        if (q.tr?.length && !P.trail.die) ghosts.push({ pts: q.tr, life: q.trLife, k: q.tk || [1, 1, 1, 1], w: q.tw ?? 1 });
        if (P.subs) subEnd(q);
        parts[i] = parts[parts.length - 1]; parts.pop();
      }
      if (P.subs) for (const q of parts) subFollow(q);
    }
    // ---- SubModule (compile() above): the children looked up when due (later nodes of the effect: the Bat's gotcha), each
    // trigger an instance of the child's emission at the particle's Unity-world spot (EmitParams, applyShapeToPosition)
    const pSizeOf = q => q.size.x * (P.sizeOL ? P.sizeOL.x(clamp01(q.age / q.life), q.R[7]) : 1);   // its size now (InheritSize)
    const subPS = s => { const c = fx.nodes?.[s.node]?.userData.particleSystem || null; if (c && !c.isSub) c.asSub(); return c; };
    const subOpts = (q, s) => ({ position: toWorld(q.p), space: "world", applyShapeToPosition: true, sizeMul: s.size ? pSizeOf(q) : null });
    function subBirth(q) {
      for (const s of P.subs) if (s.type === 0 && Math.random() < s.p) {
        const c = subPS(s);
        if (c) (q.subI ||= []).push([c.subStart(subOpts(q, s), true), s]);
      }
    }
    function subFollow(q) {
      if (!q.subI) return;
      for (const [I, s] of q.subI) { I.o.position.copy(toWorld(q.p)); if (s.size) I.o.sizeMul = pSizeOf(q); }
    }
    function subTrigger(q, type) { for (const s of P.subs) if (s.type === type && Math.random() < s.p) subPS(s)?.subStart(subOpts(q, s), false); }
    function subEnd(q) { if (q.subI) for (const [I] of q.subI) I.done = true; subTrigger(q, 2); }
    // one instance's step: the child's own rate and bursts over its duration (a Birth one loops while its particle lives)
    function runInst(s, dt) {
      let left = dt;
      while (left > 1e-9 && !s.done) {
        const st = Math.min(left, P.dur - s.t);
        emitRange(s.t, s.t + st, left - st, s.o, s);
        s.t += st; left -= st;
        if (s.t >= P.dur - 1e-9) { if (s.loop && P.loop) s.t = 0; else s.done = true; }
      }
    }
    // ---- LightsModule (compile() above): the pooled lights this system holds, given back when it has nothing to light
    const lit = [], LC = V(), LP = V();
    let lightTpl = null;
    const lightsOff = () => { for (const l of lit.splice(0)) api.releaseLight?.(l); };
    if (P.lights) for (let o = node; o && o !== fx.mirror; o = o.parent) o.addEventListener("removed", lightsOff);
    function lightsFrame() {
      const L = P.lights;
      if (!lightTpl) {
        const r = L.ref, nd = typeof r?.node === "number" ? data.effects?.[fx.name]?.nodes?.[r.node] : null;
        lightTpl = nd?.comps?.find(c => c.type === "Light") || {};
        const c = lightTpl.m_Color || { r: 1, g: 1, b: 1 };
        LC.set(toLin(num(c.r, 1)), toLin(num(c.g, 1)), toLin(num(c.b, 1)));
      }
      let shown = !!api.pointLight;
      for (let o = node; o && shown; o = o.parent) shown = o.visible;
      const best = [];
      if (shown) for (const q of parts) {
        if (!q.lit) continue;
        const u = q.age / q.life, c = pColour(q, u, q.vt.length());
        best.push({ q, u, c, I: num(lightTpl.m_Intensity, 1) * L.inten(u, q.R[1]) * (L.alphaI ? c[3] : 1) });
      }
      best.sort((a, b) => b.I - a.I).length = Math.min(best.length, L.max);
      while (lit.length > best.length) api.releaseLight(lit.pop());
      while (lit.length < best.length) { const l = api.pointLight(); if (!l) break; lit.push(l); }
      fx.mirror.updateWorldMatrix(true, false);
      lit.forEach((l, i) => {
        const { q, u, c, I } = best[i];
        LP.copy(toWorld(q.p)).applyMatrix4(fx.mirror.matrixWorld);
        if (l.parent && l.parent !== api.scene) l.parent.worldToLocal(LP);
        l.position.copy(LP);
        l.color.setRGB(LC.x * (L.col ? c[0] : 1), LC.y * (L.col ? c[1] : 1), LC.z * (L.col ? c[2] : 1));
        l.distance = num(lightTpl.m_Range, 10) * L.range(u, q.R[2]) * (L.sizeRange ? pSize(q, u, q.vt.length()) : 1);
        l.intensity = 2 * Math.PI * Math.max(0, I);
      });
    }
    // ---- trail points: in the effect's Unity world (worldSpace, or a World system), else in the system's space (they
    // move with it); each ages by the frame, goes at its lifetime, and a new one is added at the particle once it is
    // minVertexDistance from the newest
    const trailFixed = () => P.world || P.trail.world;
    function trailPt(p) { return trailFixed() ? toWorld(p) : p.clone(); }
    const trailW = k => (trailFixed() ? k.p : toWorld(k.p));
    function trailStep(dt) {
      const md2 = P.trail.minD * P.trail.minD;
      const age = (pts, life) => {
        for (const k of pts) { if (k.fresh) k.fresh = false; else k.a += dt; }
        while (pts.length && pts[0].a >= life) pts.shift();
      };
      for (const q of parts) {
        if (!q.tr) continue;
        age(q.tr, q.trLife);
        const h = trailPt(q.p), last = q.tr[q.tr.length - 1];
        if (!last || last.p.distanceToSquared(h) >= md2) q.tr.push({ p: h, a: 0 });
      }
      for (const g of ghosts) age(g.pts, g.life);
      ghosts = ghosts.filter(g => g.pts.length > 1);
    }

    const ps0 = {
      node, comp: ps,
      // Unity's ParticleSystem.Emit(EmitParams, count) (GroundHugEmitter.EmitMotes@0x22627A0): o.position / o.velocity
      // are in the system's simulation space as Unity reads EmitParams (space "world" = already in the effect's Unity
      // world), o.applyShapeToPosition adds the shape's point; also o.startSize, o.startLifetime, o.startColor
      // ([r, g, b, a] gamma), o.rotation (degrees). Works stopped or not playing, as Unity's
      emit(count = 1, o = {}) { played = true; if (!ready) { pending.push([count, o]); return; } for (let i = 0; i < count; i++) emitOne(time, 0, i, count, o); },
      play() { played = true; emitting = true; ended = false; if (P.loop || time >= P.dur) time = 0; },
      // ParticleSystem.Stop(StopEmitting): EffectControl's after-life (TTO1102:EffectControl::Update@0x1A233A0, 0x1A23661)
      stop() { emitting = false; },
      // the GroundHugEmitter's `motes` reference -> this system: wardrobe_fx_tto.py's {node: i, type: "ParticleSystem"}
      // (the effect's node i), or [fileID, pathID] / an id
      matches(ref) {
        if (ref && typeof ref === "object" && !Array.isArray(ref) && "node" in ref) return fx.nodes?.[ref.node] === node;
        const ids = [ps.pathID, ps.path_id, ps.m_PathID, ps.fileID, ps.id, ps._id, ps.ref].filter(x => x != null).map(String);
        const want = String(Array.isArray(ref) ? ref[ref.length - 1] : ref);   // [fileID, pathID]: the pathID names it
        return ids.includes(want);
      },
      get count() { return parts.length; },
      // a sub-emitter's child (SubModule): idle, and one emission instance per trigger (o: EmitParams as emit()'s, plus
      // sizeMul; loop: a Birth instance, run until its parent particle marks it done)
      get isSub() { return isSub; },
      asSub() { isSub = true; emitting = false; played = false; parts.length = 0; },
      subStart(o, loop) { const s = { t: 0, acc: 0, o, loop, done: false }; inst.push(s); played = true; return s; },
      dispose: lightsOff,
      update(dt, cam) {
        dt *= P.simSpeed;
        frame(dt);
        if (!ready) {
          ready = true;
          if (delay < 0) delay = Math.max(0, P.delay(0, Math.random()));
          if (P.prewarm && P.loop && emitting) {               // prewarm: one whole loop already run (and no start delay)
            delay = 0;
            for (let t = 0; t < P.dur; t += 1 / 30) { stepAll(1 / 30); advance(1 / 30); }
          }
          for (const [n, o] of pending.splice(0)) this.emit(n, o);
        }
        if (P.noise) noiseT += dt * P.noise.scroll(time / P.dur, 0);
        stepAll(dt);
        if (emitting) advance(dt);
        if (inst.length) {                                     // sub-emitter instances (SubModule)
          for (const s of inst) runInst(s, dt);
          for (let i = inst.length - 1; i >= 0; i--) if (inst[i].done) inst.splice(i, 1);
        }
        if (P.trail) trailStep(dt);
        // the system has stopped (no emission and no particles): its stopAction (1 disable, 2 destroy, 3 callback); a
        // sub-emitter's child never stops on its own (its parent triggers it again)
        if (!ended && !isSub && played && !emitting && !parts.length && delay <= 0) {
          ended = true;
          if (P.stopAction === 2) return "destroy";
          if (P.stopAction === 1) node.visible = false;
        }
        if (mesh) (pMesh ? renderMesh : render)(cam);
        if (tmesh) renderTrails(cam);
        if (P.lights) lightsFrame();
      },
    };
    node.userData.particleSystem = ps0;
    (fx.particleSystems ||= []).push(ps0);

    // ---- ParticleSystemRenderer: m_RenderMode 0 billboard (m_RenderAlignment 0 view, 1 world, 2 local, 3 facing the
    // camera's position; 4 velocity = APPROX view), 1 stretched (head at the particle, length = size x m_LengthScale +
    // speed x m_VelocityScale, back along the motion; negative = forward, as the game's legacy particles), 2 horizontal
    // (flat on the ground), 3 vertical (upright, facing the camera), 4 mesh (APPROX: drawn as a billboard), 5 none.
    // m_MaxParticleSize / m_MinParticleSize clamp a billboard's size to that share of the view's height. m_SortMode 0 the
    // buffer's order, 1 by distance (far first), 2 oldest in front, 3 youngest in front. Billboard rotation turns
    // clockwise as seen (Unity's). APPROX: m_Flip, the camera-velocity stretch, freeform stretching and m_SortingFudge
    // are ignored; a stretched quad runs u from head to tail (as index.html's legacy particles)
    function render(cam) {
      const det = M.determinant();
      if (!Number.isFinite(det) || Math.abs(det) < 1e-12) { mesh.visible = false; return; }
      mesh.visible = node.visible !== false;
      Minv.copy(M).invert(); mesh.matrix.copy(Minv); mesh.matrixWorldNeedsUpdate = true;   // the quads are in the effect's Unity world
      let order = parts;
      if (sortMode === 1) order = parts.map(q => [q, toWorld(q.p).distanceToSquared(camPos)]).sort((a, b) => b[1] - a[1]).map(x => x[0]);
      else if (sortMode === 2) order = parts.slice().sort((a, b) => a.age - b.age);
      else if (sortMode === 3) order = parts.slice().sort((a, b) => b.age - a.age);
      const pos = [], col = [], uvs = [], idx = [];
      const wUp = V(0, 1, 0), tm = P.uv;
      for (const q of order) {
        const u = q.age / q.life, R = q.R, W = toWorld(q.p), Vw = toWorldDir(q.vt), sp = q.vt.length();
        // size
        let sx = q.size.x, sy = P.size3D ? q.size.y : q.size.x;
        if (P.sizeOL) { const m = P.sizeOL; const a = m.x(u, R[7]); sx *= a; sy *= m.sep ? m.y(u, R[7]) : a; }
        if (P.sizeBS) { const m = P.sizeBS, t = speedT(sp, m.range), a = m.x(t, R[7]); sx *= a; sy *= m.sep ? m.y(t, R[7]) : a; }
        sx *= sizeK; sy *= sizeK;
        if (tanHalf && RM !== 4) {
          const dist = Math.max(0, W.clone().sub(camPos).dot(cam.fwd)), vh = 2 * dist * tanHalf;
          const hi = maxSize * vh, lo = minSize * vh;
          const cl = x => (x > hi ? hi : x < lo ? lo : x);
          if (vh > 0) { sx = cl(sx); sy = cl(sy); }
        }
        if (!(sx > 0 || sy > 0)) continue;
        // colour
        let c = q.c0;
        if (P.colOL) { const k = P.colOL(u, R[9]); c = [c[0] * k[0], c[1] * k[1], c[2] * k[2], c[3] * k[3]]; }
        if (P.colBS) { const k = P.colBS.g(speedT(sp, P.colBS.range), R[9]); c = [c[0] * k[0], c[1] * k[1], c[2] * k[2], c[3] * k[3]]; }
        // the texture sheet's tile (Grid mode; frameOverTime / startFrame are shares of the whole sheet or row)
        let u0 = 0, v0 = 0, u1 = 1, v1 = 1;
        if (tm) {
          const N = tm.row ? tm.tx : tm.tx * tm.ty;
          let fi;
          if (tm.time === 2) fi = Math.floor(q.sf * N + q.age * tm.fps);
          else { const x = tm.time === 1 ? speedT(sp, tm.speedRange) : u; fi = Math.floor(frac(q.sf + tm.frame(x, R[11]) * tm.cycles) * N); }
          fi = ((fi % N) + N) % N;
          const row = tm.row ? (tm.rowMode === 0 ? tm.rowIndex : tm.rowMode === 1 ? q.row : 0) : 0;
          const k = tm.row ? row * tm.tx + fi : fi, cx = k % tm.tx, cy = Math.floor(k / tm.tx) % tm.ty;
          u0 = cx / tm.tx; u1 = (cx + 1) / tm.tx; v1 = 1 - cy / tm.ty; v0 = 1 - (cy + 1) / tm.ty;   // tiles left to right, top row first
          if (tm.flipU > 0 && R[12] < tm.flipU) [u0, u1] = [u1, u0];
          if (tm.flipV > 0 && R[14] < tm.flipV) [v0, v1] = [v1, v0];
        }
        let corners;
        if (RM === 1) {                                        // stretched along the motion
          const vl = Vw.length();
          if (vl < 1e-6) continue;
          const D = Vw.clone().divideScalar(vl), L = sx * lenScale + vl * velScale;
          let side = V().crossVectors(D, cam.fwd);
          if (side.lengthSq() < 1e-10) side = cam.right.clone();
          side.normalize().multiplyScalar(sx / 2);
          const tail = W.clone().addScaledVector(D, -L);
          corners = [W.clone().sub(side), W.clone().add(side), tail.clone().sub(side), tail.add(side)];
          uvs.push(u0, v0, u0, v1, u1, v0, u1, v1);
        } else {
          let ax, ay;
          if (RM === 2) { ax = V(1, 0, 0); ay = V(0, 0, 1); }
          else if (RM === 3) { ax = V(cam.right.x, 0, cam.right.z); if (ax.lengthSq() < 1e-10) ax = V(1, 0, 0); ax.normalize(); ay = wUp.clone(); }
          else if (align === 1) { ax = V(1, 0, 0); ay = V(0, 1, 0); }
          else if (align === 2) { ax = V(1, 0, 0).applyQuaternion(Rq); ay = V(0, 1, 0).applyQuaternion(Rq); }
          else if (align === 3) {                              // facing: the plane square to the line to the camera
            const f = camPos.clone().sub(W); if (f.lengthSq() < 1e-10) f.copy(cam.fwd).negate(); f.normalize();
            ax = cam.right.clone().addScaledVector(f, -cam.right.dot(f)).normalize();
            ay = cam.up.clone().addScaledVector(f, -cam.up.dot(f)).addScaledVector(ax, -cam.up.dot(ax)).normalize();
          } else { ax = cam.right.clone(); ay = cam.up.clone(); }
          const a = q.rot.z, cs = Math.cos(a), sn = Math.sin(a);
          const X = ax.clone().multiplyScalar(cs).addScaledVector(ay, -sn).multiplyScalar(sx / 2);
          const Y = ay.clone().multiplyScalar(cs).addScaledVector(ax, sn).multiplyScalar(sy / 2);
          const C = W.clone().addScaledVector(X, -2 * pivot[0]).addScaledVector(Y, -2 * pivot[1]);
          corners = [[-1, -1], [1, -1], [-1, 1], [1, 1]].map(([i, j]) => C.clone().addScaledVector(X, i).addScaledVector(Y, j));
          uvs.push(u0, v0, u1, v0, u0, v1, u1, v1);
        }
        const b = pos.length / 3;
        for (const v of corners) pos.push(v.x, v.y, v.z);
        col.push(...c, ...c, ...c, ...c);
        idx.push(b, b + 1, b + 2, b + 2, b + 1, b + 3);
      }
      api.setMesh(mesh, pos, col, uvs, idx);
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
      // (in the effect's Unity space right x up = fwd, numerically: a proper rotation)
      else if (align !== 4) Qa.setFromRotationMatrix(Mb.makeBasis(cam.right, cam.up, cam.fwd));
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
      api.setMesh(mesh, pos, col, uvs, idx, nrm);                 // (normals in the same kept buffers, 2026-11-10)
    }

    // ---- the TrailModule's strips (P.trail above): a particle's runs from where it is now through its points, newest
    // to oldest; a ribbon through the living particles, youngest to oldest. Each point's side = the trail's direction x
    // the line to the camera (Unity's View alignment), width and colour by its share s of the strip's length
    const pColour = (q, u, sp) => {                            // the particle's colour now (as render() draws it)
      let c = q.c0;
      if (P.colOL) { const k = P.colOL(u, q.R[9]); c = [c[0] * k[0], c[1] * k[1], c[2] * k[2], c[3] * k[3]]; }
      if (P.colBS) { const k = P.colBS.g(speedT(sp, P.colBS.range), q.R[9]); c = [c[0] * k[0], c[1] * k[1], c[2] * k[2], c[3] * k[3]]; }
      return c;
    };
    const pSize = (q, u, sp) => {                              // its x size now, in metres
      let sx = q.size.x;
      if (P.sizeOL) sx *= P.sizeOL.x(u, q.R[7]);
      if (P.sizeBS) sx *= P.sizeBS.x(speedT(sp, P.sizeBS.range), q.R[7]);
      return sx * sizeK;
    };
    const mul4 = (a, b) => [a[0] * b[0], a[1] * b[1], a[2] * b[2], a[3] * b[3]];
    function renderTrails(cam) {
      const det = M.determinant();
      if (!Number.isFinite(det) || Math.abs(det) < 1e-12) { tmesh.visible = false; return; }
      tmesh.visible = node.visible !== false;
      Minv.copy(M).invert(); tmesh.matrix.copy(Minv); tmesh.matrixWorldNeedsUpdate = true;   // the strips are in the effect's Unity world
      const T0 = P.trail, pos = [], col = [], uvs = [], idx = [];
      const strip = (L, wAt, cAt) => {                         // L: points in the effect's Unity world, head first
        const n = L.length;
        if (n < 2) return;
        const acc = [0];
        for (let i = 1; i < n; i++) acc.push(acc[i - 1] + L[i].distanceTo(L[i - 1]));
        const len = acc[n - 1];
        if (!(len > 1e-6)) return;
        let side = cam.right.clone();
        const b0 = pos.length / 3;
        for (let i = 0; i < n; i++) {
          const s = acc[i] / len, tan = L[Math.min(n - 1, i + 1)].clone().sub(L[Math.max(0, i - 1)]);
          const sd = V().crossVectors(tan, camPos.clone().sub(L[i]));
          if (sd.lengthSq() > 1e-12) side = sd.normalize();    // seen end-on: keep the last good side
          const w = wAt(s) / 2, k = cAt(s);
          const u = T0.tex === 1 ? acc[i] * T0.texScale[0] : T0.tex === 2 ? i / (n - 1) : T0.tex === 3 ? i * T0.texScale[0] : s;
          const a = L[i].clone().addScaledVector(side, -w), b = L[i].clone().addScaledVector(side, w);
          pos.push(a.x, a.y, a.z, b.x, b.y, b.z); col.push(...k, ...k); uvs.push(u, 0, u, 1);
          if (i) { const q = b0 + 2 * i - 2; idx.push(q, q + 1, q + 2, q + 2, q + 1, q + 3); }
        }
      };
      if (T0.mode === 1) {                                     // Ribbon: the living particles, youngest first
        const order = parts.slice().sort((a, b) => a.age - b.age);
        for (let r = 0; r < T0.ribbons; r++) {
          const ks = order.filter((_, i) => i % T0.ribbons === r).map(q => {
            const u = q.age / q.life, sp = q.vt.length();
            return { W: toWorld(q.p), k: mul4(T0.inherit ? pColour(q, u, sp) : [1, 1, 1, 1], T0.colLife(u, q.R[3])), w: T0.sizeW ? pSize(q, u, sp) : 1 };
          });
          if (ks.length < 2) continue;
          const at = s => ks[Math.min(ks.length - 1, Math.round(s * (ks.length - 1)))];
          strip(ks.map(x => x.W), s => T0.width(s, 0.5) * at(s).w, s => mul4(T0.colTrail(s, 0.5), at(s).k));
        }
      } else {
        for (const q of parts) {
          if (!q.tr) continue;
          const u = q.age / q.life, sp = q.vt.length();
          q.tk = mul4(T0.inherit ? pColour(q, u, sp) : [1, 1, 1, 1], T0.colLife(u, q.R[3]));
          q.tw = T0.sizeW ? pSize(q, u, sp) : 1;
          const L = [toWorld(q.p)];
          for (let i = q.tr.length - 1; i >= 0; i--) { const w = trailW(q.tr[i]); if (w.distanceToSquared(L[L.length - 1]) > 1e-12) L.push(w); }
          strip(L, s => T0.width(s, q.R[2]) * q.tw, s => mul4(T0.colTrail(s, q.R[4]), q.tk));
        }
        for (const g of ghosts) {                              // a dead particle's trail: from its newest point
          const L = [];
          for (let i = g.pts.length - 1; i >= 0; i--) { const w = trailW(g.pts[i]); if (!L.length || w.distanceToSquared(L[L.length - 1]) > 1e-12) L.push(w); }
          strip(L, s => T0.width(s, 0.5) * g.w, s => mul4(T0.colTrail(s, 0.5), g.k));
        }
      }
      api.setMesh(tmesh, pos, col, uvs, idx);
    }
    return ps0;
  }

  api.curves = { curveFn, gradFn };                              // for tto_sheep.js (read when an effect is built)
  api.part("ParticleSystem", build);
  api.part("ParticleSystemRenderer", () => null);              // read by its ParticleSystem from the same node's comps
}
