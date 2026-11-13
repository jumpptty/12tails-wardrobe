// wardrobe/fxparts/tto_chameleon.js: what the Chameleon's TTO skills (Venom Phantom, Apex Hunt, Chain Lightning: the
// released three) draw that no other part does (2026-11-13, plans/fx_chameleon/parts.md "TTO parts" T1-T4 with its
// Verification 5-7; plans/fx_chameleon/tto.md sections 6-7 with its Verification 1, 2, 4, 5; decisions.md 34-36, 59).
// TTO1102 = DecompiledSource_TTO_2026-11-02 (client/GameAssembly.dll): methods by RVA (dump.cs:105570-105700), read in
// the disassembly (checks/fx_chameleon_research/parts/disasm_*.txt, tto/cl_*.asm, ai_*.asm) and the pseudo-C
// (pseudo/Chameleon.c, cited by line); the shader from its D3D11 bytecode (parts/dxbc_ChameleonSpirit.txt).
//
//   shader                 TTO/ChameleonSpirit (venomPhantom_ghost's phantomSpirit, apexHunt_arrow's ghost goldSpirit):
//                          api.shader gives a LIST [depth prepass, colour pass] (mesh.js draws a list as passes)
//   ChameleonLightning     TypeDefIndex 3477, on a LineRenderer (tto_sheep.js's part, driven): chainLightning_draw,
//                          _overload (9 auto bolts), _zapHot, stormChargeFx, staticDrainFx (cued); chainLightning_arrow,
//                          _bolt, _boltHot, venomPhantom_echo (built, not cued)
//   ChameleonAfterimage    TypeDefIndex 3476: venomPhantom_ghost, a frozen spirit copy of the hero
//   ChameleonPreyReticle   TypeDefIndex 3478: preyFx (Apex Hunt's lock, lockOnly)
//   Chameleon.ApexArrow    apexHunt_arrow's flight, the coroutine <ApexArrow>d__312 put on its root by wardrobe_fx_tto.py
//                          CODE_MOVERS
//   fx:tto/venomPhantom_coil / _beam / _rupture   the hero's code acting on the ghosts (Chameleon::ClearGhosts, Fire)
//
// Cue options read (fx.at = the cue, index.html's cueOf; [x, y, d] = metres right / up / ahead of the hero, the effect's
// Unity world):
//   bolt (non-auto ChameleonLightning)  from (default: where the cue put the node), to (the target's chest); no `to`:
//                          nothing drawn (as RabbitTracer)
//   venomPhantom_ghost     bow (the hand spot at the shot: Bake's bowPoint), face (the foe point it turns to, default
//                          the 10 m target body (0, 0.6, 10)), slide (SlideTo's time, default GhostSlide 0.18), slots
//                          (default Chameleon's GhostSlots); the slot = the ghosts of this play so far % 5 (the hero's
//                          mGhosts.Count: a per-play registry keyed by api.FX.gen, emptied by ClearGhosts)
//   venomPhantom_beam      ghost: k = ghost k (shot order) Fire()s: its fireFx at its bow point, the flare
//   venomPhantom_rupture   shatterGhosts: true = ClearGhosts(true): every ghost's Shatter()
//   venomPhantom_coil      (no option) ClearGhosts(false) (RPC_venomPhantom :21741 at the skill's start: the last
//                          play's ghosts destroyed at once)
//   preyFx                 lockOnly, release (s after the spawn = Release@0x1C4EA60), tint (a colour field's name:
//                          gold / dim / bug / tail / elem / mach; default gold, the lone dummy's)
//   apexHunt_arrow         to (hero-relative at the spawn: under the "lift" cue the cue gives the lifted numbers); the
//                          cue's kill 0.42 = Destroy(arrow, 0.3) after the 0.12 s flight
// Space: everything in the effect's Unity world (the mirror group's space: the hero's feet at the origin, facing +z, the
// floor at y 0); Unity's local numbers apply inside the mirror as they are, three's "YXZ" Euler = Unity's
// Quaternion.Euler. Clocks: t += dt from the first update (Time.time from the spawn frame).
export default function register(api) {
  const { THREE, V } = api;
  const DEG = Math.PI / 180;
  const clamp01 = x => (x < 0 ? 0 : x > 1 ? 1 : x);
  const num = (x, d = 0) => (x !== null && x !== "" && Number.isFinite(+x) ? +x : d);
  const bool = x => x === true || x === 1 || x === "True" || x === "true";
  const rnd = (a, b) => a + Math.random() * (b - a);                     // Random.Range(float, float)
  const UP = V(0, 1, 0), RIGHT = V(1, 0, 0);
  const vec = a => (Array.isArray(a) && a.length >= 3 ? V(num(a[0]), num(a[1]), num(a[2])) : null);
  const v3 = (o, d = V()) => (Array.isArray(o) ? V(num(o[0]), num(o[1]), num(o[2])) : o && typeof o === "object" ? V(num(o.x), num(o.y), num(o.z)) : d);
  const col4 = (c, d) => (Array.isArray(c) && c.length >= 3 ? [num(c[0]), num(c[1]), num(c[2]), num(c[3], 1)] : d);
  const ref = (fx, r) => (r && typeof r === "object" && typeof r.node === "number" ? fx.nodes[r.node] || null : null);
  // a node's matrix in the effect's Unity world, fresh (fx.uMatrix needs fx.mirrorInv, which Fx.update sets after the
  // parts are built; as tto_sheep.js's uMat)
  const uMat = (fx, o) => { o.updateWorldMatrix(true, false); return fx.mirror.matrixWorld.clone().invert().multiply(o.matrixWorld); };
  const worldPos = (fx, o) => V().setFromMatrixPosition(uMat(fx, o));
  const setWorldPos = (fx, o, w) => {                                   // Transform.set_position
    if (o.parent === fx.mirror) o.position.copy(w);
    else o.position.copy(w.clone().applyMatrix4(uMat(fx, o.parent).invert()));
  };
  const uQuat = (fx, o) => { const q = new THREE.Quaternion(); for (; o && o !== fx.mirror; o = o.parent) q.premultiply(o.quaternion); return q; };
  const setWorldRot = (fx, o, q) => o.quaternion.copy(uQuat(fx, o.parent).invert().multiply(q));   // Transform.set_rotation
  // Quaternion.LookRotation(forward, up) in Unity's numbers (Cross is the same formula in either hand; tto_sheep.js)
  const lookRot = (f, up = UP, q = new THREE.Quaternion()) => {
    if (f.lengthSq() < 1e-12) return q.identity();
    const z = f.clone().normalize(), x = V().crossVectors(up, z);
    if (x.lengthSq() < 1e-12) x.set(1, 0, 0); x.normalize();
    return q.setFromRotationMatrix(new THREE.Matrix4().makeBasis(x, V().crossVectors(z, x), z));
  };
  const camPos = fx => { fx.mirror.updateWorldMatrix(true, false); return api.camera.getWorldPosition(V()).applyMatrix4(fx.mirror.matrixWorld.clone().invert()); };
  const prefixOf = fx => { const i = String(fx.name).lastIndexOf("/"); return i >= 0 ? fx.name.slice(0, i + 1) : ""; };
  // the cue options of an effect a script Instantiates at a pose given as a matrix in fx's Unity world: api.spawn puts
  // its group at the hero root's present pose, so the pose goes through the world into that frame (equal to fx's while
  // the hero stands still)
  const spawnAt = (fx, M) => {
    const H = api.hero?.();
    if (!H?.root) return null;
    fx.mirror.updateWorldMatrix(true, false); H.root.updateWorldMatrix(true, false);
    const p = V(), q = new THREE.Quaternion();
    H.root.getWorldPosition(p); H.root.getWorldQuaternion(q);
    const frame = new THREE.Matrix4().compose(p, q, V(1, 1, 1)).multiply(new THREE.Matrix4().makeScale(-1, 1, 1));
    const L = frame.invert().multiply(fx.mirror.matrixWorld).multiply(M);
    const pos = V(), rq = new THREE.Quaternion(), s = V();
    L.decompose(pos, rq, s);
    const e = new THREE.Euler().setFromQuaternion(rq, "YXZ");
    return { x: pos.x, y: pos.y, d: pos.z, rot: [e.x / DEG, e.y / DEG, e.z / DEG] };
  };

  // ---------------------------------------------------------------- TTO/ChameleonSpirit (parts T2, dxbc_ChameleonSpirit.txt)
  // Queue Transparent+1. Pass 0: ZWrite On, ColorMask 0, ZTest LEqual, Cull Back (a depth prepass: only the front-most
  // surface of the body gets its colour). Pass 1: Blend One OneMinusSrcAlpha (premultiplied), ZWrite Off, ZTest LEqual,
  // Cull Back. vs_4_0: o1 = the world position P, o2 = the world normal N (normal x unity_WorldToObject, normalised).
  // ps_4_0 (cb0[2] _CoreColor, [3] _RimColor, [4] _RimPower / _RimEdge / _InnerGlow, [5] _ScaleColor, [6] _ScaleSize /
  // _ScaleSpeed / _Wisp / _WispScale, [7] _WispSpeed / _MaxGlow / _Fade; cb1[0].y _Time.y, cb1[4] the camera):
  //   q = P _WispScale + (0, -_WispSpeed T, 0); n = 0.65 vn(q) + 0.35 vn(2.3 q + 7.1), vn = a 3D value noise (corners
  //   hashed a = 17 fract(p 0.3183099 + 0.1), fract(a.x a.y a.z (a.x + a.y + a.z)); trilinear with f^2 (3 - 2f));
  //   w = smoothstep(0.25, 0.85, n); wisp = 1 + _Wisp (w - 1);
  //   f = 1 - sat(N.V); pr = f^_RimPower; s = smoothstep(_RimEdge, 1, f);
  //   scales = _ScaleTex.a at (P.x, P.y - _ScaleSpeed T / _ScaleSize) |N.z| + at (P.z, P.y ...) |N.x| + at (P.x, P.z)
  //   |N.y|, all x _ScaleSize (the xz plane not scrolled; the weights not normalised);
  //   A = _Fade sat(0.35 s + _CoreColor.a (0.55 + 0.45 wisp) + 0.25 pr);
  //   rgb = _CoreColor.rgb A + _Fade min(_RimColor.rgb _RimColor.a (pr _InnerGlow wisp + s) + scales _ScaleColor.rgb
  //   _ScaleColor.a (1 - s), _MaxGlow).
  // On the page: the arithmetic on the gamma values (as tto_bison.js's MoltenCrust), the result made linear for
  // linearToOutputTexel; P / N in the page's world (the mirror's x flip and the stage's placement only move the noise
  // field); T = the page clock (APPROX: the wisps' and scales' phase). Canvas alpha: the page renders over a transparent
  // canvas, which takes premultiplied colour, so the alpha written is at least the brightest channel (fxMaterial's
  // "premul" rule; APPROX: where the glow outshines A the colour behind dims by that, not by A). N from the model matrix
  // as a direction (exact for the uniform scales these meshes have). The two passes: one material each, listed depth
  // first (a mesh draws its groups in order; mesh.js's withMaterials gives a list one group per pass), the same vertex
  // program so the depths match. Cull Back = FrontSide: inside the mirror group three keeps Unity's front faces (det < 0),
  // and the afterimage's baked copy keeps the hero's (its triangles turned where its matrix flips them, bake below)
  if (!api.shader) console.warn("tto_chameleon: api.shader missing (index.html), TTO/ChameleonSpirit draws as plain alpha");
  const time = { get value() { return performance.now() / 1000; } };   // Unity's _Time.y (never cloned: a getter)
  const SPIRIT_VERT = `
    varying vec3 vW; varying vec3 vN;
    void main() {
      vec4 w = modelMatrix * vec4(position, 1.0);
      vW = w.xyz;
      vN = (modelMatrix * vec4(normal, 0.0)).xyz;
      gl_Position = projectionMatrix * viewMatrix * w;
    }`;
  const SPIRIT_FRAG = `
    uniform float uTime, uFade, uRimPower, uRimEdge, uInnerGlow, uScaleSize, uScaleSpeed, uWisp, uWispScale, uWispSpeed, uMaxGlow, uHasTex;
    uniform vec4 uCore, uRim, uScale;
    uniform sampler2D uScaleTex;
    varying vec3 vW; varying vec3 vN;
    float hsh(vec3 p) { vec3 a = fract(p * 0.3183099 + 0.1) * 17.0; return fract(a.x * a.y * a.z * (a.x + a.y + a.z)); }
    float vn(vec3 x) {
      vec3 i = floor(x), f = fract(x), u = f * f * (3.0 - 2.0 * f);
      return mix(mix(mix(hsh(i), hsh(i + vec3(1.0, 0.0, 0.0)), u.x), mix(hsh(i + vec3(0.0, 1.0, 0.0)), hsh(i + vec3(1.0, 1.0, 0.0)), u.x), u.y),
                 mix(mix(hsh(i + vec3(0.0, 0.0, 1.0)), hsh(i + vec3(1.0, 0.0, 1.0)), u.x), mix(hsh(i + vec3(0.0, 1.0, 1.0)), hsh(i + vec3(1.0, 1.0, 1.0)), u.x), u.y), u.z);
    }
    vec3 ln(vec3 c) { c = max(c, 0.0); return mix(c / 12.92, pow((c + 0.055) / 1.055, vec3(2.4)), step(0.04045, c)); }
    void main() {
      vec3 q = vW * uWispScale + vec3(0.0, -uWispSpeed * uTime, 0.0);
      float n = 0.65 * vn(q) + 0.35 * vn(q * 2.3 + 7.1);
      float w = clamp((n - 0.25) * 1.666667, 0.0, 1.0);
      w = w * w * (3.0 - 2.0 * w);
      float wisp = 1.0 + uWisp * (w - 1.0);
      vec3 V = normalize(cameraPosition - vW), N = normalize(vN);
      float f = 1.0 - clamp(dot(N, V), 0.0, 1.0);
      float pr = f > 0.0 ? exp2(log2(f) * uRimPower) : 0.0;
      float s = clamp((f - uRimEdge) / (1.0 - uRimEdge), 0.0, 1.0);
      s = s * s * (3.0 - 2.0 * s);
      float scales = 0.0;
      if (uHasTex > 0.5) {
        float st = -uScaleSpeed * uTime;
        vec3 P = vW * uScaleSize;
        scales = texture2D(uScaleTex, vec2(P.x, P.y + st)).a * abs(N.z) + texture2D(uScaleTex, vec2(P.z, P.y + st)).a * abs(N.x)
               + texture2D(uScaleTex, P.xz).a * abs(N.y);
      }
      float A = uFade * clamp(0.35 * s + uCore.a * (0.55 + 0.45 * wisp) + 0.25 * pr, 0.0, 1.0);
      vec3 glow = min(uRim.rgb * uRim.a * (pr * uInnerGlow * wisp + s) + scales * uScale.rgb * uScale.a * (1.0 - s), vec3(uMaxGlow));
      vec3 rgb = uCore.rgb * A + uFade * glow;
      vec4 o = linearToOutputTexel(vec4(ln(rgb), 1.0));
      gl_FragColor = vec4(o.rgb, max(clamp(A, 0.0, 1.0), max(o.r, max(o.g, o.b))));
    }`;
  // phantomSpirit's numbers (tto_probe.json), for a ghost whose data lacks its material
  const PHANTOM = { props: { _Fade: 1, _InnerGlow: 0.35, _MaxGlow: 0.9, _RimEdge: 0.62, _RimPower: 3.4, _ScaleSize: 1.8, _ScaleSpeed: 0.4,
    _Wisp: 0.5, _WispScale: 2.2, _WispSpeed: 0.6, _CoreColor: [0.05, 0.2, 0.05, 0.28], _RimColor: [0.5, 1, 0.3, 0.6], _ScaleColor: [0.35, 0.9, 0.2, 0.06] } };
  const texs = {};
  const scaleTex = d => {
    const n = d?.scaleTex;
    if (!n || !api.texLoader) return null;
    if (!texs[n]) {
      const t = texs[n] = api.texLoader.load(`${api.DATA}fx/tex/${n}.webp`);
      t.colorSpace = THREE.NoColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping;   // only its alpha is read
    }
    return texs[n];
  };
  const v4 = (c, d) => { const a = col4(c, d); return new THREE.Vector4(a[0], a[1], a[2], a[3]); };
  // a fresh [depth, colour] pair (its own uniforms: a ghost's _Fade / _RimColor, ChameleonAfterimage.Apply's block)
  function spiritPair(d) {
    const p = d?.props || {}, tx = scaleTex(d);
    const uniforms = { uTime: time, uFade: { value: num(p._Fade, 1) }, uRimPower: { value: num(p._RimPower, 3) }, uRimEdge: { value: num(p._RimEdge, 0.5) },
      uInnerGlow: { value: num(p._InnerGlow, 0.3) }, uScaleSize: { value: num(p._ScaleSize, 1.5) }, uScaleSpeed: { value: num(p._ScaleSpeed, 0.4) },
      uWisp: { value: num(p._Wisp, 0.5) }, uWispScale: { value: num(p._WispScale, 2.2) }, uWispSpeed: { value: num(p._WispSpeed, 0.6) },
      uMaxGlow: { value: num(p._MaxGlow, 0.9) }, uHasTex: { value: tx ? 1 : 0 }, uScaleTex: { value: tx },
      uCore: { value: v4(p._CoreColor, [0.05, 0.2, 0.05, 0.28]) }, uRim: { value: v4(p._RimColor, [0.5, 1, 0.3, 0.6]) }, uScale: { value: v4(p._ScaleColor, [0, 0, 0, 0]) } };
    const colour = new THREE.ShaderMaterial({ vertexShader: SPIRIT_VERT, fragmentShader: SPIRIT_FRAG, uniforms, transparent: true,
      depthWrite: false, depthTest: true, side: THREE.FrontSide, blending: THREE.CustomBlending, blendSrc: THREE.OneFactor,
      blendDst: THREE.OneMinusSrcAlphaFactor, blendSrcAlpha: THREE.OneFactor, blendDstAlpha: THREE.OneMinusSrcAlphaFactor });
    const depth = new THREE.ShaderMaterial({ vertexShader: SPIRIT_VERT, fragmentShader: "void main() { gl_FragColor = vec4(0.0); }",
      transparent: true, depthWrite: true, depthTest: true, colorWrite: false, side: THREE.FrontSide });
    colour.userData.spirit = true; depth.userData.spiritDepth = true;
    return [depth, colour];
  }
  api.shader?.("shader:TTO/ChameleonSpirit", d => spiritPair(d));
  // Queue Transparent+1: drawn after the effects' own transparent meshes (renderOrder 0)
  const QUEUE_PLUS1 = 1;

  // ---------------------------------------------------------------- ChameleonLightning (parts T1)
  // Fields (dump.cs; .ctor@0x1C4E8E0 defaults): aura, segments 9, jag 0.18, maxJag 0.45, flicker 0.05, life 0.25, radius
  // 0.55, height 1.1, gap 0.12, autoBolt, localFrom, localTo, delay.
  // - Awake@0x1C4DBF0: the LineRenderer, segments + 1 points, c0 / c1 = its start / end colour, born = time; aura:
  //   useWorldSpace false, NewArc().
  // - Start@0x1C4E550: autoBolt and not set: delay > 0: waiting, wakeAt = time + delay, the line off; else
  //   Set(TransformPoint(localFrom), TransformPoint(localTo)).
  // - Set(from, to)@0x1C4E3C0 (the hero's code for the non-auto bolts: pseudo/Chameleon.c:35707 venomPhantom_echo,
  //   :38893 chainLightning_bolt / _boltHot): useWorldSpace true, a = from, b = to, set, born = time, Jag().
  // - Update@0x1C4E690: waiting and time >= wakeAt: the line on, Set(...). Aura: time >= nextArc: NewArc(), else
  //   time >= nextJag: Jag(); Fade(clamp01(1 - (time - born) / life)). Bolt: nothing until set; age = time - born;
  //   age >= life: Destroy(gameObject); else time >= nextJag: Jag(); Fade(1 - age / life).
  // - NewArc@0x1C4E250 (disasm :372-400): born = time; nextArc = time + gap + Range(0, gap); th1 = Range(0, 2 pi);
  //   th2 = th1 + Range(0.8, 2.2) x (value < 0.5 ? -1 : 1); a = (r cos th1, Range(0.05, height), r sin th1), b the same
  //   at th2; Jag().
  // - Jag@0x1C4DD90: nextJag = time + flicker; d = b - a; side = normalize(cross(d, up)) (cross(d, right) when its
  //   |.|^2 < 0.0001); n2 = cross(normalize(d), side); amp = min(|d| jag, maxJag); point i = a + d t (t = i / segments),
  //   the inner ones + (side Range(-1, 1) + n2 Range(-1, 1)) sin(pi t) amp.
  // - Fade(k)@0x1C4DCE0: startColor = (c0.rgb, c0.a k), endColor = (c1.rgb, c1.a k).
  // On the page: the node's LineRenderer (tto_sheep.js) driven: its pts written each Jag (the node's space for an aura,
  // the effect's Unity world for a bolt), its colour = its own gradient with the alpha x k (APPROX: Unity's start / end
  // colour setters reshape a gradient of more than two keys; exact for two), drawn every frame here. Awake and Start run
  // at the build (the spawn frame); a non-auto bolt's Set from the cue (from / to), as RabbitTracer's
  api.part("ChameleonLightning", (fx, node, c) => {
    const F = { aura: bool(c.aura), segments: Math.max(1, Math.round(num(c.segments, 9))), jag: num(c.jag, 0.18), maxJag: num(c.maxJag, 0.45),
      flicker: num(c.flicker, 0.05), life: num(c.life, 0.25), radius: num(c.radius, 0.55), height: num(c.height, 1.1), gap: num(c.gap, 0.12),
      autoBolt: bool(c.autoBolt), localFrom: v3(c.localFrom), localTo: v3(c.localTo), delay: num(c.delay, 0) };
    let line = null, base = null, k = 1, pts = [];
    let now = 0, born = 0, nextJag = 0, nextArc = 0, wakeAt = 0, set = false, waiting = false, on = true;
    const a = V(), b = V();
    const grab = () => {
      if (line) return line;
      line = fx.emitters.find(x => x.node === node && x.line) || null;
      if (line) {
        line.driven = true; line.world = !F.aura; base = line.color;
        line.color = u => { const q = base(u); return [q[0], q[1], q[2], q[3] * k]; };
      }
      return line;
    };
    const jag = () => {
      nextJag = now + F.flicker;
      const d = b.clone().sub(a), side = V().crossVectors(d, UP);
      if (side.lengthSq() < 0.0001) side.crossVectors(d, RIGHT);
      side.normalize();
      const n2 = V().crossVectors(d.clone().normalize(), side), amp = Math.min(d.length() * F.jag, F.maxJag), S = F.segments;
      pts = [];
      for (let i = 0; i <= S; i++) {
        const t = i / S, p = a.clone().addScaledVector(d, t);
        if (i > 0 && i < S) { const e = Math.sin(Math.PI * t) * amp; p.addScaledVector(side, rnd(-1, 1) * e).addScaledVector(n2, rnd(-1, 1) * e); }
        pts.push(p);
      }
    };
    const newArc = () => {
      born = now; nextArc = now + F.gap + rnd(0, F.gap);
      const th1 = rnd(0, 2 * Math.PI), th2 = th1 + rnd(0.8, 2.2) * (Math.random() < 0.5 ? -1 : 1), r = F.radius;
      a.set(r * Math.cos(th1), rnd(0.05, F.height), r * Math.sin(th1));
      b.set(r * Math.cos(th2), rnd(0.05, F.height), r * Math.sin(th2));
      jag();
    };
    const setFT = (from, to) => { a.copy(from); b.copy(to); set = true; born = now; jag(); };
    const tp = p => p.clone().applyMatrix4(uMat(fx, node));             // Transform.TransformPoint
    // Awake
    grab();
    if (F.aura) newArc();
    // the hero's Set() for a non-auto bolt (the cue's from / to); Start for an auto one
    else if (!F.autoBolt) {
      const to = vec(fx.at?.to);
      if (to) setFT(vec(fx.at?.from) || worldPos(fx, node), to);
      else console.warn("ChameleonLightning: a bolt with no cue `to` (the target's chest) is not drawn", fx.name);
    } else if (F.delay > 0) { waiting = true; wakeAt = now + F.delay; on = false; }
    else setFT(tp(F.localFrom), tp(F.localTo));
    return { node, update(dt, cam) {
      now += dt;
      grab();
      if (waiting && now >= wakeAt) { waiting = false; on = true; setFT(tp(F.localFrom), tp(F.localTo)); }
      if (F.aura) {
        if (now >= nextArc) newArc(); else if (now >= nextJag) jag();
        k = clamp01(1 - (now - born) / F.life);
      } else if (set) {
        const age = now - born;
        if (age >= F.life) return "destroy";                             // Destroy(gameObject)
        if (now >= nextJag) jag();
        k = 1 - age / F.life;
      }
      if (!line) return;
      line.pts = on && (F.aura || set) ? pts : [];
      line.draw(cam);
    } };
  });

  // ---------------------------------------------------------------- ChameleonAfterimage (parts T2, tto.md section 7)
  // Fields (.ctor@0x1C4DA50; the prefab): spirit chmRow6_phantomSpirit, fireFx venomPhantom_ghostFire, shatterFx
  // venomPhantom_ghostShatter, fadeIn 0.12, shatterTime 0.35, life 4, rim (0.5, 1, 0.3, 0.7), flare (0.9, 1, 0.7, 1).
  // - Bake(body, bowPoint)@0x1C4C190 (pseudo/Chameleon.c:364): bowLocal = InverseTransformPoint(bowPoint); every
  //   enabled renderer of the hero (Skip@0x1C4CFA0: name rules, literals unresolved) copied: a SkinnedMeshRenderer's
  //   BakeMesh (its pose frozen) or a MeshFilter's mesh, at the renderer's world pose, every submesh drawn with spirit,
  //   no shadows; Apply(0, rim).
  // - SlideTo(pos, rot, time)@0x1C4D2E0 (:385-423: Row6Ground(hero.TransformPoint(GhostSlots[ghosts % 5])),
  //   LookRotation(vFlat(to - spot)), GhostSlide 0.18): from the current pose, slideTime = max(0.01, time), slideAt = now.
  // - Update@0x1C4D3C0: age = now - born; age > life, not ending: Shatter. Slide: u = clamp01((now - slideAt) /
  //   slideTime), e = 1 - (1 - u)^2, SetPositionAndRotation(Lerp, Slerp by e), done at u 1. fade = clamp01(age / fadeIn)
  //   x (0.85 + 0.15 sin(7 age)); ending: k = clamp01((endAt - now) / shatterTime), fade x k, localScale 1 + 0.08 (1 - k),
  //   Destroy at now >= endAt. Colour rim; after Fire lerp(flare, rim, clamp01((now - firedAt) / 0.3)). Apply(fade, c).
  // - Fire@0x1C4CA80 (:12802): firedAt = now; fireFx at TransformPoint(bowLocal), its rotation.
  // - Shatter@0x1C4CD90 (:36425, ai_shatter.asm): only if not ending: endAt = now + shatterTime; shatterFx at
  //   position + up x 0.9 x lossyScale.y (its 0.9 is a height, not a scale: `mulss xmm7 (lossyScale.y), 0.9` then
  //   Vector3.up x that + position), its rotation.
  // - Apply(fade, c)@0x1C4BEF0: _Fade and _RimColor (the IL2CPP literals 0x37FDD60 / 0x3801228 read as the shader's
  //   properties, medium) on every copy.
  // On the page: the copy = every mesh of the dressed hero shown to the camera now (outfit, worn props, a skin cue's look;
  // the hover overlays and prop glow twins left out: APPROX for Skip's unresolved name rules), each vertex put through its
  // skin once into a static geometry in the ghost root's frame (normals too), drawn with this ghost's own spirit pair
  // (renderOrder 1: Queue Transparent+1). The hero's code around it: the hooks below (ghost k's Fire on a beam cue,
  // ClearGhosts on the rupture's and the coil's)
  const GHOST_SLOTS = [[1.5, 0, -0.3], [-1.5, 0, -0.3], [2.8, 0, -1.1], [-2.8, 0, -1.1], [0, 0, 1.6]];   // .cctor@0x1BD9650 :39953
  const GHOST_SLIDE = 0.18;                                             // dump.cs:105270-105284
  const ghosts = { gen: null, list: [] };                               // the hero's mGhosts, per play
  const ghostPlay = () => {
    const g = api.FX?.gen ?? 0;
    if (ghosts.gen !== g) { ghosts.gen = g; ghosts.list = []; }
    return ghosts;
  };
  // Chameleon::ClearGhosts(shatter)@0x1BCF440 (:36364): every ghost still there Shatter()ed (true) or destroyed at once
  // (false); the list emptied
  const clearGhosts = shatter => {
    const P = ghostPlay();
    for (const g of P.list) if (g.alive) { if (shatter) g.shatter(); else g.kill(); }
    P.list = [];
  };
  // a mesh's vertices in its present pose (three's skinning: bindMatrixInverse x sum(w bone.matrixWorld x boneInverse)
  // x bindMatrix, then matrixWorld) into the frame `inv` (root.matrixWorld^-1); the triangles turned round where that
  // matrix flips them (det < 0), so three's front faces stay the hero's
  function bakeMesh(o, inv) {
    const g0 = o.geometry, P = g0?.getAttribute("position");
    if (!P) return null;
    const Nn = g0.getAttribute("normal"), SI = g0.getAttribute("skinIndex"), SW = g0.getAttribute("skinWeight");
    const W = inv.clone().multiply(o.matrixWorld), n = P.count;
    const skin = o.isSkinnedMesh && o.skeleton && SI && SW;
    const bones = skin ? o.skeleton.bones.map((b, i) => new THREE.Matrix4().multiplyMatrices(b.matrixWorld, o.skeleton.boneInverses[i])) : null;
    const WB = skin ? W.clone().multiply(o.bindMatrixInverse) : null;
    const pos = new Float32Array(3 * n), nrm = Nn ? new Float32Array(3 * n) : null;
    const M = new THREE.Matrix4(), T = new THREE.Matrix4(), NM = new THREE.Matrix3(), v = V(), nv = V();
    if (!skin) { T.copy(W); NM.getNormalMatrix(T); }
    for (let i = 0; i < n; i++) {
      if (skin) {
        const e = M.elements; e.fill(0);
        for (let j = 0; j < 4; j++) {
          const w = SW.getComponent(i, j);
          if (!w) continue;
          const B = bones[SI.getComponent(i, j)];
          if (!B) continue;
          const be = B.elements;
          for (let q = 0; q < 16; q++) e[q] += w * be[q];
        }
        T.multiplyMatrices(WB, M).multiply(o.bindMatrix);
        if (nrm) NM.getNormalMatrix(T);
      }
      v.fromBufferAttribute(P, i).applyMatrix4(T);
      pos[3 * i] = v.x; pos[3 * i + 1] = v.y; pos[3 * i + 2] = v.z;
      if (nrm) { nv.fromBufferAttribute(Nn, i).applyMatrix3(NM).normalize(); nrm[3 * i] = nv.x; nrm[3 * i + 1] = nv.y; nrm[3 * i + 2] = nv.z; }
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    let idx = g0.index ? Array.from(g0.index.array) : Array.from({ length: n }, (_, i) => i);
    idx.length -= idx.length % 3;
    if (W.determinant() < 0) for (let i = 0; i < idx.length; i += 3) { const t = idx[i + 1]; idx[i + 1] = idx[i + 2]; idx[i + 2] = t; }
    g.setIndex(n > 65535 ? new THREE.Uint32BufferAttribute(idx, 1) : new THREE.Uint16BufferAttribute(idx, 1));
    if (nrm) g.setAttribute("normal", new THREE.BufferAttribute(nrm, 3)); else g.computeVertexNormals();
    g.addGroup(0, idx.length, 0); g.addGroup(0, idx.length, 1);         // pass 0 (depth), pass 1 (colour)
    return g;
  }
  function bake(root, into, mats) {
    const H = api.hero?.();
    if (!H?.root) return 0;
    H.root.updateMatrixWorld(true);
    root.updateWorldMatrix(true, false);
    const inv = root.matrixWorld.clone().invert(), cam = api.camera;
    let count = 0;
    (function walk(o) {
      if (!o.visible) return;
      const u = o.userData || {};
      if (o.isMesh && !(u.hoverOverlay && !u.lookCopy) && !u.heroClone && (!cam || cam.layers.test(o.layers))
          && [].concat(o.material).some(m => m && m.visible !== false)) {
        const g = bakeMesh(o, inv);
        if (g) {
          const m = new THREE.Mesh(g, mats);
          m.name = "afterimage_" + (o.name || count); m.frustumCulled = false; m.renderOrder = QUEUE_PLUS1; m.raycast = () => {};
          into.add(m); count++;
        }
      }
      for (const ch of o.children) walk(ch);
    })(H.root);
    return count;
  }
  api.part("ChameleonAfterimage", (fx, root, c, mat, nd, data) => {
    const fadeIn = num(c.fadeIn, 0.12), shatterTime = num(c.shatterTime, 0.35), life = num(c.life, 4);
    const rim = col4(c.rim, [0.5, 1, 0.3, 0.7]), flare = col4(c.flare, [0.9, 1, 0.7, 1]);
    const sn = typeof c.spirit === "string" ? c.spirit : c.spirit?.name;
    const pair = spiritPair(data?.materials?.[sn] || PHANTOM), u = pair[1].uniforms;
    const pre = prefixOf(fx);
    const fxName = (r, d) => pre + (typeof r === "string" ? r : r?.name || d);
    const fireName = fxName(c.fireFx, "venomPhantom_ghostFire"), shatterName = fxName(c.shatterFx, "venomPhantom_ghostShatter");
    const apply = (fade, cc) => { u.uFade.value = fade; u.uRim.value.set(cc[0], cc[1], cc[2], cc[3]); };
    // Bake(hero, bow)
    const body = new THREE.Group(); body.name = "afterimage"; root.add(body);
    if (!bake(root, body, pair)) console.warn("ChameleonAfterimage: no hero mesh to copy", fx.name);
    const bowW = vec(fx.at?.bow) || worldPos(fx, root);
    const bowLocal = bowW.applyMatrix4(uMat(fx, root).invert());
    apply(0, rim);
    // SlideTo(the slot on the ground, facing the foe, 0.18)
    const P = ghostPlay(), slots = Array.isArray(fx.at?.slots) && fx.at.slots.length ? fx.at.slots : GHOST_SLOTS;
    const sl = vec(slots[P.list.length % slots.length]) || V();
    const spot = V(sl.x, -(fx.liftY || 0), sl.z);                         // Row6Ground: the floor under the slot
    const face = vec(fx.at?.face) || V(0, 0.6, 10);
    const flat = face.clone().sub(spot); flat.y = 0;
    const slideFrom = root.position.clone(), turnFrom = root.quaternion.clone(), turnTo = lookRot(flat);
    const slideTime = Math.max(0.01, num(fx.at?.slide, GHOST_SLIDE)), scale0 = root.scale.clone();
    let t = 0, slideAt = 0, endAt = -1, firedAt = -1, killed = false;
    const me = {
      alive: true,
      fire() {                                                          // Fire@0x1C4CA80
        firedAt = t;
        const at = spawnAt(fx, uMat(fx, root).multiply(new THREE.Matrix4().makeTranslation(bowLocal.x, bowLocal.y, bowLocal.z)));
        if (at) api.spawn?.(fireName, at);
      },
      shatter() {                                                       // Shatter@0x1C4CD90
        if (endAt >= 0) return;
        endAt = t + shatterTime;
        const p = V(), q = new THREE.Quaternion(), s = V();
        uMat(fx, root).decompose(p, q, s);
        p.y += 0.9 * s.y;
        const at = spawnAt(fx, new THREE.Matrix4().compose(p, q, V(1, 1, 1)));
        if (at) api.spawn?.(shatterName, at);
      },
      kill() { killed = true; },                                        // Destroy(gameObject)
    };
    P.list.push(me);
    return { node: root,
      dispose() { me.alive = false; for (const m of pair) m.dispose(); },
      update(dt) {
        t += dt;
        if (killed) { me.alive = false; return "destroy"; }
        if (t > life && endAt < 0) me.shatter();
        if (slideAt >= 0) {
          const s = clamp01((t - slideAt) / slideTime), e = 1 - (1 - s) * (1 - s);
          root.position.lerpVectors(slideFrom, spot, e); root.quaternion.slerpQuaternions(turnFrom, turnTo, e);
          if (s >= 1) slideAt = -1;
        }
        let fade = clamp01(t / fadeIn) * (0.85 + 0.15 * Math.sin(7 * t));
        if (endAt >= 0) {
          const k = clamp01((endAt - t) / shatterTime);
          fade *= k; root.scale.copy(scale0).multiplyScalar(1 + 0.08 * (1 - k));
          if (t >= endAt) { me.alive = false; return "destroy"; }
        }
        const cc = firedAt >= 0 ? (w => flare.map((x, j) => x + (rim[j] - x) * w))(clamp01((t - firedAt) / 0.3)) : rim;
        apply(fade, cc);
      } };
  });
  // the hero's code on the ghosts (parts Verification 5, tto.md section 7): "fx:<effect>" parts, built on the effect's root
  // when it is made (index.html's Fx constructor), read the cue
  api.part("fx:tto/venomPhantom_coil", () => { clearGhosts(false); return null; });          // RPC_venomPhantom :21741
  api.part("fx:tto/venomPhantom_beam", fx => {                                               // RPC_phantomRequiem :12802
    const k = fx.at?.ghost;
    if (k != null && Number.isInteger(+k)) { const g = ghostPlay().list[+k]; if (g?.alive) g.fire(); }
    return null;
  });
  api.part("fx:tto/venomPhantom_rupture", fx => { if (fx.at?.shatterGhosts) clearGhosts(true); return null; });   // :12927

  // ---------------------------------------------------------------- ChameleonPreyReticle (parts T3, its Verification 6)
  // Fields (tto_prey.json; .ctor@0x1C4F890): ring (node 1: the Quad x 2.4, turned flat), crosshair (node 2: Quad x 0.7,
  // 1.6 up), tinted [both renderers], notches [] (none: the lit count never shows), lockIn 0.35, fadeOut 0.25, spin 40,
  // preview, previewStacks, lockOnly, colours gold (1, 0.82, 0.3, 1), dim, bug, tail, elem, mach.
  // - Start@0x1C4EA70: born = time; a MaterialPropertyBlock; cc = the parent's CharacterControl; tint = gold, or by its
  //   race (1 tail, 2-3 bug, 4 mach, 5 elem); feetY = cc's position.y, headY = its collider's bounds max y (no cc: the
  //   renderer's bounds, or parent y - 1 / feetY + 2); the ring's and crosshair's localScale kept; Paint(each, tint, 1).
  // - Update@0x1C4EF10: lockOnly: released (or the prey dead) -> goneAt = time once; else (the Prey status) goneAt while
  //   the status is gone. goneAt >= 0: x = (time - goneAt - 0.1) / fadeOut, x >= 1: Destroy, else k = 1 - clamp01(x).
  //   age = time - born, x = clamp01(age / lockIn), e = clamp01(1 - (1 - x)^2), s = 2.2 - 1.2 e. feetY eased toward the
  //   prey's y (clamp01(10 dt)). The ring: world position (x, feetY + 0.06, z), localRotation Euler(90, spin age, 0),
  //   localScale = kept x s. The crosshair: world position (x, headY + 0.7 + 0.08 sin(3 age), z), rotation
  //   LookRotation(itself - camera, camera.up), localScale = kept x (1.15 - 0.35 clamp01(lit / notches)) x s (1.15 s:
  //   no notches). Paint each tinted renderer (tint, clamp01(1.5 x) k) while fading or age < lockIn + 0.05.
  // - Paint(r, c, k)@0x1C4E920: the block's colour (_TintColor: the literal 0x3803008 unresolved, read as the additive
  //   material's tint, medium) = (0.5 c.rgb, min(1, 0.85 c.a k)).
  // - Release@0x1C4EA60: released = true (ClearApexLocks, pseudo/Chameleon.c:37147, :37236).
  // On the page: the root at the cue's spot = the prey's collider centre (AddApexLockFx; the standard body 0.6 m up), so
  // feetY = root y - 0.6, headY = root y + 0.5 (the body's top, 1.1); `release` = the Release's time after the spawn
  // (also the status' end without lockOnly); never released, it stands until the cue's kill. The tint on the renderer's own
  // copy of its material (fxMaterial's additive "add": colour 2 x tint.rgb, opacity 2 x tint.a; an alpha above 1
  // brightens the colour, as Unity's 2 x _TintColor does, tto_cat.js's Tint)
  const ownMats = (mesh, list) => {
    if (!mesh) return [];
    if (mesh.userData.fxOwn) return mesh.userData.fxOwn.mats;
    const arr = Array.isArray(mesh.material) ? mesh.material : [mesh.material];
    const cl = arr.map(m => {
      if (!m) return m;
      const x = m.clone(); x.onBeforeCompile = m.onBeforeCompile; x.customProgramCacheKey = m.customProgramCacheKey;
      x.userData.fxBlend = m.userData.fxBlend; list.push(x); return x;
    });
    if (Array.isArray(mesh.material)) mesh.material = cl; else mesh.material = cl[0];
    mesh.userData.fxOwn = { mats: cl, owner: "ChameleonPreyReticle" };
    return cl;
  };
  const meshOf = o => o?.userData?.fxStatic || o?.children?.find(x => x.isMesh) || null;
  api.part("ChameleonPreyReticle", (fx, root, c) => {
    const ring = ref(fx, c.ring), cross = ref(fx, c.crosshair), tinted = (c.tinted || []).map(r => ref(fx, r)).filter(Boolean);
    const lockIn = num(c.lockIn, 0.35), fadeOut = num(c.fadeOut, 0.25), spin = num(c.spin, 40);
    const gold = col4(c.gold, [1, 0.82, 0.3, 1]);
    const named = typeof fx.at?.tint === "string" && /^(gold|dim|bug|tail|elem|mach)$/.test(fx.at.tint) ? col4(c[fx.at.tint], null) : null;
    const tint = named || gold;
    const release = fx.at?.release != null && Number.isFinite(+fx.at.release) ? +fx.at.release : null;
    const ringScale = ring?.scale.clone(), crossScale = cross?.scale.clone();
    const at = worldPos(fx, root), feetY = at.y - 0.6, headY = at.y + 0.5;
    const mine = [];
    let t = 0, goneAt = -1, mats = null;
    const E = new THREE.Euler(), q = new THREE.Quaternion();
    const paint = k => {
      mats ||= tinted.flatMap(n => ownMats(meshOf(n), mine));
      const A = 2 * Math.min(1, 0.85 * tint[3] * k), b = Math.max(1, A);
      for (const m of mats) if (m?.color) { m.color.setRGB(tint[0] * b, tint[1] * b, tint[2] * b, THREE.SRGBColorSpace); m.opacity = clamp01(A); }
    };
    return { node: root,
      dispose() { for (const m of mine) m.dispose(); },
      update(dt, cam) {
        t += dt;
        if (goneAt < 0 && release != null && t >= release) goneAt = t;
        let k = 1;
        if (goneAt >= 0) { const x = (t - goneAt - 0.1) / fadeOut; if (x >= 1) return "destroy"; k = 1 - clamp01(x); }
        const x = clamp01(t / lockIn), e = clamp01(1 - (1 - x) * (1 - x)), s = 2.2 - 1.2 * e;
        if (ring) {
          setWorldPos(fx, ring, V(at.x, feetY + 0.06, at.z));
          ring.quaternion.setFromEuler(E.set(90 * DEG, spin * t * DEG, 0, "YXZ"));
          ring.scale.copy(ringScale).multiplyScalar(s);
        }
        if (cross) {
          const p = V(at.x, headY + 0.7 + 0.08 * Math.sin(3 * t), at.z);
          setWorldPos(fx, cross, p);
          setWorldRot(fx, cross, lookRot(p.clone().sub(camPos(fx)), cam?.up || UP, q));
          cross.scale.copy(crossScale).multiplyScalar(1.15 * s);
        }
        if (goneAt >= 0 || t < lockIn + 0.05) paint(clamp01(1.5 * x) * k);
      } };
  });

  // ---------------------------------------------------------------- Chameleon.ApexArrow (tto.md P5, CODE_MOVERS)
  // TTO1102:Chameleon.<ApexArrow>d__312::MoveNext@0x1BEC9D0 (pseudo/Chameleon.c:485-715; ApexVolley@0x1BCE570 starts it,
  // :37157): after its delay (0.04 x the arrow's index: 0 for the lone target), apexHunt_arrow spawned at from,
  // LookRotation(to - from) (Row6Spawn); each frame: to = Row6Chest(body) while it lives; u = clamp01((now - t0) / 0.12);
  // position = Lerp(from, to, u); rotation = LookRotation(to - from) while |to - from|^2 > a small epsilon; u < 1: next
  // frame; else Destroy(arrow, 0.3) (:660), ImpactFx at Row6Ground(to) (a cue), ApexHit.
  // On the page: from / its turn = where the cue put the root, to = the cue's `to` (the still target's chest, hero-
  // relative at the spawn); the goldSpirit ghost mesh (mesh.js's StaticMesh, the spirit pair) put on renderOrder 1 (Queue
  // Transparent+1) at the first update (its node is built after this root component)
  api.part("Chameleon.ApexArrow", (fx, root) => {
    const from = root.position.clone(), to = vec(fx.at?.to);
    if (!to) console.warn("Chameleon.ApexArrow: no cue `to` (the target's chest): the arrow stays where it was spawned", fx.name);
    let t = 0, end = -1, queued = false;
    const place = () => {
      const u = clamp01(t / 0.12);
      root.position.lerpVectors(from, to, u);
      const d = to.clone().sub(from);
      if (d.lengthSq() > 1e-5) lookRot(d, UP, root.quaternion);
      return u;
    };
    if (to) place();
    return { node: root, update(dt) {
      if (!queued) {
        queued = true;
        root.traverse(o => { if (o.isMesh && [].concat(o.material).some(m => m?.userData?.spirit)) o.renderOrder = QUEUE_PLUS1; });
      }
      t += dt;
      if (!to) return;
      if (end >= 0) return t >= end ? "destroy" : undefined;
      if (place() >= 1) end = t + 0.3;                                   // Destroy(arrow, 0.3)
    } };
  });
}
