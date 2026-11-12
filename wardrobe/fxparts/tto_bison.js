// wardrobe/fxparts/tto_bison.js: what the Bison's TTO skills (Unchained Fury, Titan Drop, Magma Quake: the released
// three) draw that no other part does (2026-11-13, plans/fx_bison/parts.md parts 8, 9, 10 with its Verification
// corrections 1-3; plans/fx_bison/tto.md section 4 B1-B4, B6 and its Verification; plans/fx_bison/decisions.md 41, 44, 47).
// TTO1102 = DecompiledSource_TTO_2026-11-02 (client/GameAssembly.dll), methods by RVA (pseudo/Bison.c, capstone);
// TTO's shaders from their D3D11 bytecode (checks/fx_bison_research/parts/dxbc_EnergyArc.txt, dxbc_MoltenCrust.txt).
//
//   shaders      TTO/Bison/EnergyArc (the crescents' tto_c6_energyArc: procedural, additive), TTO/Bison/MoltenCrust
//                (Magma Quake's lava pool tto_c6_moltenCrust on magmaQuake_magmaField's GroundHugEmitter discs):
//                page materials through api.shader(blend, make)
//   Bison_c6Arc  the ground / air crescents: 42 arcs in 11 skill prefabs + tto/unchained's two (repeat true), diameters
//                3.1 (unchainedFury_roar's air spirals, hug false) to 60 (magmaQuake_quakeField)
//   Bison_row6Fx unchainedFury_chains' rings and sigil, tto/unchained's sigil and orbit (bob 0.08 at bobRate 3)
//   GroundConformParticles  a no-op on the page's flat floor (decision 41; part 10)
//
// Space: everything in the effect's Unity world (the mirror group's space: the hero's feet at the origin, the floor at
// y 0); Unity's local numbers (Euler degrees, quaternions) apply inside the mirror as they are (index.html Fx: "inside
// the mirror Unity's numbers apply as they are"), three's "YXZ" Euler = Unity's Quaternion.Euler (z, then x, then y).
// Clocks: as alphatimer.js, t += dt from the first update (OnEnable's Time.time is the spawn frame).
// The game's colours are gamma values: made linear as tto_sheep.js's additive() does (uTint = toLin(2 x tint)); the
// MoltenCrust arithmetic, whose thresholds read the texture's numbers, is done on gamma values (texture loaded raw).
export default function register(api) {
  const { THREE, V } = api;
  const DEG = Math.PI / 180;
  const clamp01 = x => (x < 0 ? 0 : x > 1 ? 1 : x);
  const S = x => { x = clamp01(x); return x * x * (3 - 2 * x); };       // the shaders' / scripts' smoothstep
  const toLin = c => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
  const lerp = (a, b, u) => a + (b - a) * u;
  const num = (x, d = 0) => (Number.isFinite(+x) ? +x : d);
  const bool = x => x === true || x === "True" || x === "true" || x === 1;
  const uEuler = (x, y, z, q = new THREE.Quaternion()) => q.setFromEuler(new THREE.Euler(x * DEG, y * DEG, z * DEG, "YXZ"));
  // Unity's _Time.y: the page's clock (tto_sheep.js's `time`; APPROX: only the noise's phase differs). A getter, so a
  // material made with it must not be cloned (UniformsUtils.clone would freeze the value): MoltenCrust is never cloned
  const time = { get value() { return performance.now() / 1000; } };
  // a node's matrix in the effect's Unity world, fresh (fx.uMatrix needs fx.mirrorInv, which Fx.update sets after the
  // parts are built, and this part has just moved the node: as tto_sheep.js's uMat)
  const uMat = (fx, o) => { o.updateWorldMatrix(true, false); return fx.mirror.matrixWorld.clone().invert().multiply(o.matrixWorld); };
  // GroundHugEmitter.Ground(p, near) on the page's flat floor (groundhug.js:62-63): the ray from near + 12 down 36 m
  // meets the floor (y 0) when it lies in that span, else the reference height
  const ground = near => (near + 12 >= 0 && near - 24 <= 0 ? 0 : near);

  if (!api.shader) console.warn("tto_bison: api.shader missing (index.html), TTO/Bison/* draw as plain alpha");
  const shader = (blend, make) => api.shader?.("shader:" + blend, make);

  // ---------------------------------------------------------------- TTO/Bison/EnergyArc (tto B3)
  // dxbc_EnergyArc.txt: Blend SrcAlpha One, ZWrite Off, Cull Off, Queue Transparent, no texture read (_MainTex unused,
  // _InvFade unused by the programs drawn). vs_4_0: o1 = 2 x (vertex colour x _TintColor) (`add o1 = r0 + r0`), o2 = uv0.
  // ps_4_0: alpha = S(10 u) x (1 - S(10 (u - 0.9))) x v x vcol.a, rgb = vcol.rgb ((u, v) = uv0: u along the crescent,
  // v across; the mesh c6_crescent has vertex alpha 0 on its inner edge). The page's additive convention as
  // tto_sheep.js's ADD_OUT: colour in the output space x alpha, added; canvas alpha = its brightest channel.
  // uTint (= 2 x _TintColor, made linear) is the material's; Bison_c6Arc drives a clone per renderer (its property block)
  const ARC_VERT = `
    uniform vec4 uTint;
    varying vec4 vC; varying vec2 vUv;
    void main() {
    #ifdef USE_COLOR_ALPHA
      vC = color * uTint;
    #else
      vC = uTint;
    #endif
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }`;
  const ARC_FRAG = `
    varying vec4 vC; varying vec2 vUv;
    float sm(float x) { x = clamp(x, 0.0, 1.0); return x * x * (3.0 - 2.0 * x); }
    void main() {
      float A = sm(vUv.x * 10.0) * (1.0 - sm((vUv.x - 0.9) * 10.0)) * vUv.y * vC.a;
      vec4 o = linearToOutputTexel(vec4(vC.rgb, 1.0));
      o.rgb *= clamp(A, 0.0, 1.0);
      gl_FragColor = vec4(o.rgb, max(o.r, max(o.g, o.b)));
    }`;
  const tintVec = (t, v = new THREE.Vector4()) => v.set(toLin(2 * t[0]), toLin(2 * t[1]), toLin(2 * t[2]), 2 * t[3]);
  shader("TTO/Bison/EnergyArc", d => {
    const t = d.props?._TintColor || d.tint || [0.5, 0.5, 0.5, 0.5];
    const m = new THREE.ShaderMaterial({
      vertexShader: ARC_VERT, fragmentShader: ARC_FRAG, vertexColors: true, transparent: true, depthWrite: false,
      side: THREE.DoubleSide, blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor,
      blendSrcAlpha: THREE.OneFactor, blendDstAlpha: THREE.OneMinusSrcAlphaFactor,
      uniforms: { uTint: { value: tintVec(t) } },
    });
    m.userData.energyArc = true;                  // Bison_c6Arc clones these (Material.copy keeps userData)
    return m;
  });

  // ---------------------------------------------------------------- TTO/Bison/MoltenCrust (tto B4, parts part 10)
  // dxbc_MoltenCrust.txt: Blend SrcAlpha OneMinusSrcAlpha, ZWrite Off, Cull Off, Queue Transparent. vs_4_0: o2 = vertex
  // colour x _TintColor (not doubled), o1 = uv0 (no _MainTex_ST), o3 = the world position. ps_4_0, T = _Time.y,
  // n(p) = value noise: i = floor p, f = fract p, mix(mix(h(i), h(i + (1, 0)), s.x), mix(h(i + (0, 1)), h(i + (1, 1)),
  // s.x), s.y), s = f^2 (3 - 2f), h(p) = fract(sin(dot(p, (127.1, 311.7))) x 43758.5453):
  //   n1 = n(3.1 world.xz - (0.16 T, 0)), n2 = n(0.7 world.xz + (0.28 T, -0.15 T)); m = 0.7 n2 + 0.3 n1;
  //   base = m (0.55, 0.32, 0.026) + (0.45, 0.04, 0.009); glow = sat(1.65 n1 n2)^3; tex = _MainTex(uv);
  //   crust = S(sat((tex.r - 1.25 max(tex.g, tex.b) - 0.07) x 2.857143)); hot = S(sat((tex.r - 0.38) x 2.380952)) x crust;
  //   lava = hot (0.7, 0.42, 0.13) glow + base; rgb = mix(tex.rgb (0.7, 0.78, 0.87), lava, crust) x vcol.rgb;
  //   the ragged rim: e = 0.91 + 0.035 n(36 uv), r = length(2 uv - 1), alpha = tex.a x vcol.a x (1 - S(sat((r - e) /
  //   (0.995 - e)))).
  // On the page: the arithmetic on gamma values (the texture raw, NoColorSpace; the page's linear vertex colours taken
  // back to gamma), the result made linear for linearToOutputTexel; normal blending (three's: colour SrcAlpha /
  // OneMinusSrcAlpha, the canvas alpha One / OneMinusSrcAlpha). World xz from modelMatrix in the page's world (the
  // mirror's x flip and the stage's placement only move the field: the noise needs a stable one). APPROX: T = the page
  // clock (the noise's phase); fog not drawn
  const CRUST_VERT = `
    varying vec4 vCol; varying vec2 vUv; varying vec3 vW;
    void main() {
    #ifdef USE_COLOR_ALPHA
      vCol = color;
    #else
      vCol = vec4(1.0);
    #endif
      vUv = uv;
      vec4 w = modelMatrix * vec4(position, 1.0);
      vW = w.xyz;
      gl_Position = projectionMatrix * viewMatrix * w;
    }`;
  const CRUST_FRAG = `
    uniform vec4 uTint; uniform float uTime; uniform sampler2D map; uniform float uHasMap;
    varying vec4 vCol; varying vec2 vUv; varying vec3 vW;
    float sm(float x) { x = clamp(x, 0.0, 1.0); return x * x * (3.0 - 2.0 * x); }
    float hsh(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
    float vn(vec2 p) {
      vec2 i = floor(p), f = fract(p), s = f * f * (3.0 - 2.0 * f);
      return mix(mix(hsh(i), hsh(i + vec2(1.0, 0.0)), s.x), mix(hsh(i + vec2(0.0, 1.0)), hsh(i + vec2(1.0, 1.0)), s.x), s.y);
    }
    vec3 gm(vec3 c) { c = max(c, 0.0); return mix(c * 12.92, 1.055 * pow(c, vec3(1.0 / 2.4)) - 0.055, step(0.0031308, c)); }
    vec3 ln(vec3 c) { c = max(c, 0.0); return mix(c / 12.92, pow((c + 0.055) / 1.055, vec3(2.4)), step(0.04045, c)); }
    void main() {
      vec4 vc = vec4(gm(vCol.rgb), vCol.a) * uTint;
      float T = uTime;
      float n1 = vn(vW.xz * 3.1 - vec2(0.16 * T, 0.0)), n2 = vn(vW.xz * 0.7 + vec2(0.28 * T, -0.15 * T));
      float m = 0.7 * n2 + 0.3 * n1;
      vec3 base = m * vec3(0.55, 0.32, 0.026) + vec3(0.45, 0.04, 0.009);
      float g = clamp(1.65 * n1 * n2, 0.0, 1.0), glow = g * g * g;
      vec4 tex = uHasMap > 0.5 ? texture2D(map, vUv) : vec4(1.0);
      float crust = sm((tex.r - 1.25 * max(tex.g, tex.b) - 0.07) * 2.857143);
      float hot = sm((tex.r - 0.38) * 2.380952) * crust;
      vec3 lava = hot * vec3(0.7, 0.42, 0.13) * glow + base;
      vec3 rgb = mix(tex.rgb * vec3(0.7, 0.78, 0.87), lava, crust) * vc.rgb;
      float e = 0.91 + 0.035 * vn(vUv * 36.0), r = length(vUv * 2.0 - 1.0);
      float A = tex.a * vc.a * (1.0 - sm((r - e) / (0.995 - e)));
      gl_FragColor = linearToOutputTexel(vec4(ln(rgb), clamp(A, 0.0, 1.0)));
    }`;
  shader("TTO/Bison/MoltenCrust", d => {
    const t = d.props?._TintColor || d.tint || [1, 1, 1, 1];
    const tx = d.tex ? api.texLoader.load(`${api.DATA}fx/tex/${d.tex}.webp`) : null;
    if (tx) tx.colorSpace = THREE.NoColorSpace;   // the shader's numbers are the texture's own (gamma) values
    return new THREE.ShaderMaterial({
      vertexShader: CRUST_VERT, fragmentShader: CRUST_FRAG, vertexColors: true, transparent: true, depthWrite: false,
      side: THREE.DoubleSide, blending: THREE.NormalBlending,
      uniforms: { uTint: { value: new THREE.Vector4(t[0], t[1], t[2], t[3]) }, uTime: time, map: { value: tx }, uHasMap: { value: tx ? 1 : 0 } },
    });
  });

  // ---------------------------------------------------------------- Bison_c6Arc (tto B2, parts part 8)
  // Fields (dump.cs Bison_c6Arc): delay, duration, diameter, angle, spin, repeat, color, hug, lift. Every instance:
  // angle 25 (Sweep0) / 205 (Sweep1), spin 140, lift 0.25; repeat false except tto/unchained's two (duration 0.9,
  // diameter 3.6, colour (0.85, 0.09, 0.045, 0.65)); hug true except unchainedFury_roar's RoarSpiral0-2 Sweeps.
  // - Awake@0x1B9B7C0: its MeshRenderer and a MaterialPropertyBlock (.cctor@0x1B9C280: the property is _TintColor);
  //   with hug its own copy of the mesh (Instantiate<Mesh>) and the flat vertices kept.
  // - OnEnable@0x1B9BDB0: started = Time.time; the renderer off.
  // - Update@0x1B9BDF0: t = Time.time - started - delay, d = max(0.01, duration); t < 0, or t >= d with repeat false:
  //   renderer off, done. Else k = t / d (repeat: fmod(t, d) / d):
  //   localScale = diameter x (0.65 + 0.4 x (1 - (1 - k)^2)) x one (eased out, overriding the saved scale);
  //   localRotation = Euler(0, angle + spin x t, 0) (t not wrapped, repeat or not);
  //   _TintColor (the block) = 0.5 x (lerp(c.r, 1, f), lerp(c.g, 0.38, f), lerp(c.b, 0.08, f), 0.75 (1 - S(k)) S(k /
  //   0.08) c.a), f = clamp01(0.45 k): it warms toward orange, fades in over the first 8 %, out along the rest;
  //   with hug, Drape@0x1B9B9A0: every flat vertex to world (TransformPoint), y = GroundHugEmitter.Ground(world,
  //   transform.position.y) + lift, back (InverseTransformPoint), the mesh's vertices replaced: the crescent lies `lift`
  //   above the ground whatever its parent's tilt; the renderer on.
  // On the page: the node's StaticMesh (node.userData.fxStatic, mesh.js; one geometry per spawn, so its position
  // attribute is rewritten in place) is found at the first update; the property block = its own clone of each EnergyArc
  // material (or, when another part already made the renderer's own copies, mesh.userData.fxOwn, those: parts.md
  // Interfaces 3), its uTint = the 0.5-scaled colour made linear and doubled as the shader's vertex program does
  api.part("Bison_c6Arc", (fx, node, c, mat, nodeDef) => {
    if (c.enabled === false || nodeDef?.active === false) return null;
    const delay = num(c.delay), dur = Math.max(0.01, num(c.duration, 1)), diameter = num(c.diameter, 1);
    const angle = num(c.angle), spin = num(c.spin), repeat = bool(c.repeat), hug = bool(c.hug), lift = num(c.lift);
    const col = Array.isArray(c.color) ? c.color.map(x => num(x, 1)) : [1, 1, 1, 1];
    let t = 0, mesh = null, mats = [], clones = [], flat = null, warned = false;
    if (node.userData.fxStatic) node.userData.fxStatic.visible = false;   // OnEnable: the renderer off (taken over at the first update)
    const setup = () => {
      mesh = node.userData.fxStatic || null;
      if (!mesh) { if (!warned) console.warn("Bison_c6Arc: no StaticMesh on the node", fx.name, node.name); warned = true; return false; }
      const list = Array.isArray(mesh.material) ? mesh.material : [mesh.material];
      if (mesh.userData.fxOwn) mats = list.filter(m => m?.uniforms?.uTint);   // the renderer's own copies (Interfaces 3)
      else {
        const out = list.map(m => {
          if (!m?.userData?.energyArc) return m;
          const k = m.clone(); clones.push(k); mats.push(k); return k;
        });
        mesh.material = Array.isArray(mesh.material) ? out : out[0];
      }
      if (hug) {
        const p = mesh.geometry?.getAttribute("position");
        if (p) flat = Float32Array.from(p.array);
      }
      return true;
    };
    const w = V(), tint = [0, 0, 0, 0];
    const drape = () => {
      const p = mesh.geometry.getAttribute("position"), a = p.array;
      const um = uMat(fx, mesh), inv = um.clone().invert();
      const gy = ground(V().setFromMatrixPosition(uMat(fx, node)).y) + lift;
      for (let i = 0; i < flat.length; i += 3) {
        w.set(flat[i], flat[i + 1], flat[i + 2]).applyMatrix4(um);
        w.y = gy;
        w.applyMatrix4(inv);
        a[i] = w.x; a[i + 1] = w.y; a[i + 2] = w.z;
      }
      p.needsUpdate = true;
    };
    return { node, update(dt) {
      if (!mesh && !setup()) return;
      t += dt;
      const tt = t - delay;
      if (tt < 0 || (!repeat && tt >= dur)) { mesh.visible = false; return; }
      const k = (repeat ? tt % dur : tt) / dur;
      node.scale.setScalar(diameter * (0.65 + 0.4 * (1 - (1 - k) ** 2)));
      uEuler(0, angle + spin * tt, 0, node.quaternion);
      const f = clamp01(0.45 * k);
      tint[0] = 0.5 * lerp(col[0], 1, f); tint[1] = 0.5 * lerp(col[1], 0.38, f); tint[2] = 0.5 * lerp(col[2], 0.08, f);
      tint[3] = 0.5 * 0.75 * (1 - S(k)) * S(k / 0.08) * (col[3] ?? 1);
      for (const m of mats) tintVec(tint, m.uniforms.uTint.value);
      if (hug && flat) drape();
      mesh.visible = true;
    },
    dispose() { for (const m of clones) m.dispose(); clones = []; } };
  });

  // ---------------------------------------------------------------- Bison_row6Fx (tto B1, parts part 9)
  // Fields (dump.cs Bison_row6Fx): spin, tightenFrom, tightenTime, tremble, pulse, strainTime, bob, bobRate.
  // unchainedFury_chains: Ring0-2 (spin 30 / -30 / 30, tightenFrom 1.7 / 1.85 / 2.0, tightenTime 0.1 / 0.13 / 0.16,
  // tremble 7, pulse 0.05, strainTime 0.62), Mark (spin -40, tightenTime 0.12, strainTime 0.6); tto/unchained: Sigil
  // (spin 50, tightenTime 0.12, strainTime 0.6) and Orbit (spin 120, bob 0.08, bobRate 3).
  // - Awake@0x1B9CDE0: base localScale / localPosition / localRotation kept; seed = Random.value x 100.
  // - OnEnable@0x1B9CE90: t0 = Time.time.
  // - Update@0x1B9CEB0, t = Time.time - t0: e = tightenTime > 0 ? 1 - (1 - clamp01(t / tightenTime))^2 : 1;
  //   s = strainTime > 0 ? clamp01(t / strainTime)^2 : 0;
  //   localScale = base x (1 + sin(47 t + seed) x s x pulse) x lerp(tightenFrom, 1, e);
  //   localRotation = baseRot x Euler(0, spin x t, 0) x Euler(sin(61 t + seed) x s x tremble, 0, sin(53 t + 2 seed) x s
  //   x tremble) (the products' order read from the quaternion arithmetic: base x spin x tremble);
  //   localPosition = base + up x bob x sin(bobRate x t + seed) when bob != 0.
  // On the page: the same on the node, Unity's numbers inside the mirror; applied once at build (t 0) so the first
  // frame drawn is the game's, then each update
  api.part("Bison_row6Fx", (fx, node, c, mat, nodeDef) => {
    if (c.enabled === false || nodeDef?.active === false) return null;
    const spin = num(c.spin), from = num(c.tightenFrom, 1), tt = num(c.tightenTime), tremble = num(c.tremble);
    const pulse = num(c.pulse), st = num(c.strainTime), bob = num(c.bob), bobRate = num(c.bobRate);
    const bScale = node.scale.clone(), bPos = node.position.clone(), bRot = node.quaternion.clone();
    const seed = Math.random() * 100;
    const qs = new THREE.Quaternion(), qt = new THREE.Quaternion();
    let t = 0;
    const apply = () => {
      const e = tt > 0 ? 1 - (1 - clamp01(t / tt)) ** 2 : 1;
      const s = st > 0 ? clamp01(t / st) ** 2 : 0;
      node.scale.copy(bScale).multiplyScalar((1 + Math.sin(47 * t + seed) * s * pulse) * lerp(from, 1, e));
      uEuler(0, spin * t, 0, qs);
      uEuler(Math.sin(61 * t + seed) * s * tremble, 0, Math.sin(53 * t + 2 * seed) * s * tremble, qt);
      node.quaternion.copy(bRot).multiply(qs).multiply(qt);
      node.position.copy(bPos);
      if (bob !== 0) node.position.y += bob * Math.sin(bobRate * t + seed);
    };
    apply();
    return { node, update(dt) { t += dt; apply(); } };
  });

  // ---------------------------------------------------------------- GroundConformParticles (tto B6, parts part 10)
  // Fields radius, spacing, maxStep; on all six magmaQuake roots (magmaTick, quakeTick, magmaField, quakeField,
  // magmaSlam, quakeSlam). Sample@0x2260BF0 keeps origin = transform.position and an n x n grid of
  // GroundHugEmitter.Ground heights; LateUpdate@0x2260850 adds GroundAt(x, z) - origin.y (GroundAt@0x2260680: the grid
  // bilinear, origin.y outside it) to each newborn particle's y of every World-space system under it, when over 0.01.
  // On the page's flat floor Ground is 0 everywhere and every Magma Quake root is spawned on the floor, so the shift is
  // 0: registered as built, drawing nothing (decision 41). (Spawned above the floor it would drop new particles to y 0.)
  api.part("GroundConformParticles", () => null);
}
