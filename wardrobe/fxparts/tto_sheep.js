// wardrobe/fxparts/tto_sheep.js: what the Sheep's TTO skills (Gleaming Breath, Lucent Barrier, Grand Codex) draw that no
// other part does (2026-11-10, plans/fx_sheep/tto.md "Probed 2026-11-10"). TTO1102 = DecompiledSource_TTO_2026-11-02
// (client/GameAssembly.dll); its methods read with Ghidra (the Bible's tools/run_ghidra.bat, read only: RabbitTracer's
// three methods, checks/fx_sheep_build/tto/RabbitTracer.c), the pseudo-C (pseudo/Sheep.c) and capstone for the floats
// Ghidra drops; TTO's shaders disassembled from their D3D11 bytecode (checks/fx_sheep_build/tto/dxbc_*.txt, Windows'
// D3DDisassemble over the Shader's compressedBlob).
//
//   shaders     TTO/Sheep/Celestial Ring, Celestial Ray, Prism Veil (TTO's own, procedural), Standard (the Codex book),
//               Particles/Standard Unlit (the Sparks' tto_Point): page materials through api.shader(blend, make)
//   LineRenderer          Unity's LineRenderer (lucentBarrier_beam, _reflectBeam), driven by RabbitTracer
//   TrailRendererModern   Unity 5.5+'s TrailRenderer (gleamingBreath_wisp's Trail / TrailCore, grandCodex_spear's
//                         Trail); wardrobe_fx_tto.py names it apart from Unity 3.5's (trail.js)
//   RabbitTracer          TTO's beam script (TTO.Game TypeDefIndex 3914)
//   Sheep.BreathFly       the wisp's flight (the coroutine, put on the wisp's root by wardrobe_fx_tto.py CODE_MOVERS)
//   Sheep.CodexOpen       the book's drop, bob and page turns (the same)
//
// Two parts need the point the game aims at, which the page has no character for: the cue option `to` ([x, y, d]:
// metres right, up and ahead of the hero, as the cue's own x / y / d), read as fx.at.to (index.html's Fx keeps its
// cue as `at`). Space: everything in the effect's Unity world (the mirror group's space, the hero's feet at y 0).
export default function register(api) {
  const { THREE, V } = api;
  const clamp01 = x => (x < 0 ? 0 : x > 1 ? 1 : x);
  const toLin = c => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
  const target = fx => (Array.isArray(fx.at?.to) ? V(fx.at.to[0], fx.at.to[1], fx.at.to[2]) : null);
  const camPos = fx => api.camera.getWorldPosition(V()).applyMatrix4(fx.mirrorInv);
  // a node's matrix in the effect's Unity world, fresh (fx.uMatrix needs fx.mirrorInv, which Fx.update sets after the
  // parts are built, and a part may have just moved the node)
  const uMat = (fx, o) => { o.updateWorldMatrix(true, false); return fx.mirror.matrixWorld.clone().invert().multiply(o.matrixWorld); };
  const worldPos = (fx, o) => V().setFromMatrixPosition(uMat(fx, o));
  // Transform.set_position: a Unity-world point back through the node's parent
  const setWorldPos = (fx, o, w) => {
    if (o.parent === fx.mirror) o.position.copy(w);
    else o.position.copy(w.clone().applyMatrix4(uMat(fx, o.parent).invert()));
    o.updateMatrixWorld(true);
  };
  // Quaternion.LookRotation(forward, Vector3.up) in Unity's numbers (Cross is the same formula in either hand)
  const lookRot = (f, q = new THREE.Quaternion()) => {
    const z = f.clone().normalize(), x = V().crossVectors(V(0, 1, 0), z);
    if (x.lengthSq() < 1e-12) x.set(1, 0, 0); x.normalize();
    return q.setFromRotationMatrix(new THREE.Matrix4().makeBasis(x, V().crossVectors(z, x), z));
  };

  // ---------------------------------------------------------------- materials
  // api.shader(blend, make): index.html's fxMaterial asks make(d, name, cls) for a material whose data blend is that
  // name (d = data.materials[name], its "props" = the material's floats and colours, wardrobe_fx_tto.py)
  if (!api.shader) console.warn("tto_sheep: api.shader missing (index.html), TTO's own shaders draw as plain alpha");
  const shader = (blend, make) => api.shader?.("shader:" + blend, make);
  const time = { get value() { return performance.now() / 1000; } };   // Unity's _Time.y (APPROX: the page's clock, so
                                                                        // only the phase of the orbit / scroll differs)
  // every TTO/Sheep shader's vertex program (dxbc_*.txt vs_4_0): colour = 2 x _TintColor x vertex colour, uv0 as it is
  // (no _MainTex_ST), the Prism Veil also its world normal and the view vector (o3 / o4); fog is not drawn
  const VERT = `
    uniform vec4 uTint;
    varying vec4 vC; varying vec2 vUv; varying vec3 vN; varying vec3 vV;
    void main() {
    #ifdef USE_COLOR_ALPHA
      vC = color * uTint;
    #else
      vC = uTint;
    #endif
      vUv = uv;
      vec4 mv = modelViewMatrix * vec4(position, 1.0);
      vN = normalMatrix * normal; vV = -mv.xyz;
      gl_Position = projectionMatrix * mv;
    }`;
  // their blend, Blend SrcAlpha One: the page's additive convention (index.html fxMaterial): the colour in the output
  // space x alpha, added, and the canvas alpha = its brightest channel, so the light shows over the CSS stage
  const ADD_OUT = `
      vec4 o = linearToOutputTexel(vec4(rgb, 1.0));
      o.rgb *= clamp(A, 0.0, 1.0);
      gl_FragColor = vec4(o.rgb, max(o.r, max(o.g, o.b)));`;
  const smooth = "float sm(float x) { x = clamp(x, 0.0, 1.0); return x * x * (3.0 - 2.0 * x); }";
  const additive = (d, frag, extra = {}) => {
    const t = d.props?._TintColor || d.tint || [0.5, 0.5, 0.5, 0.5];
    return new THREE.ShaderMaterial({
      vertexShader: VERT, fragmentShader: frag, vertexColors: true, transparent: true, depthWrite: false,
      side: extra.side ?? THREE.DoubleSide, blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor,
      blendSrcAlpha: THREE.OneFactor, blendDstAlpha: THREE.OneMinusSrcAlphaFactor,
      uniforms: { uTint: { value: new THREE.Vector4(toLin(2 * t[0]), toLin(2 * t[1]), toLin(2 * t[2]), 2 * t[3]) }, uTime: time, ...extra.uniforms },
    });
  };
  // TTO/Sheep/Celestial Ring (dxbc_Celestial_Ring.txt ps_4_0, Cull Off, ZWrite Off): no texture; a star chart drawn from
  // the uv: p = 2 (uv - 0.5), r = |p|, a = atan2(p.y, p.x) + _Time.y x _Speed (0.12, the orbit); rings at r 0.88 (0.003
  // wide), 0.95 (0.002, x 0.5), 0.75 (0.025, under 6 spokes cos(6a)^40), a band at 0.915 (0.012) shown on 3 arcs
  // (smoothstep((sin 3a + 0.3) / 0.35), x 0.75), 48 ticks cos(48a)^12 between r 0.81 and 0.86 (x 0.65), a glow
  // 2^(-64.92 |r - 0.89|) x 0.14; the line edges antialiased by fwidth(r) (min 0.002). alpha = that x vertex alpha
  shader("TTO/Sheep/Celestial Ring", d => additive(d, `
    uniform float uTime, uSpeed; varying vec4 vC; varying vec2 vUv;
    ${smooth}
    float line(float r, float c, float w, float iw) { return 1.0 - sm((abs(r - c) - w) * iw); }
    void main() {
      vec2 p = (vUv - 0.5) * 2.0;
      float r = length(p), a = atan(p.y, p.x) + uTime * uSpeed;
      float iw = 1.0 / max(abs(dFdx(r)) + abs(dFdy(r)), 0.002);
      float arc = sm((sin(3.0 * a) + 0.3) * 2.857143);
      float tot = line(r, 0.88, 0.003, iw) + 0.5 * line(r, 0.95, 0.002, iw) + 0.75 * arc * line(r, 0.915, 0.012, iw);
      tot += 0.65 * sm((r - 0.81) * 66.666733) * pow(max(cos(48.0 * a), 0.0), 12.0) * (1.0 - sm((r - 0.86) * 100.000099));
      tot += pow(max(cos(6.0 * a), 0.0), 40.0) * line(r, 0.75, 0.025, iw);
      float A = clamp(exp2(abs(r - 0.89) * -64.92128) * 0.14 + tot, 0.0, 1.0) * vC.a;
      vec3 rgb = vC.rgb;${ADD_OUT}
    }`, { uniforms: { uSpeed: { value: d.props?._Speed ?? 0.12 } } }));
  // TTO/Sheep/Celestial Ray (dxbc_Celestial_Ray.txt, Cull Off): along u a fade-in smoothstep(u / 0.12), a fade-out
  // 1 - smoothstep((u - 0.65) / 0.35), a shimmer 0.85 + 0.15 sin(18u - 4 _Time.y); across v a core
  // 0.3 e^(-18 w^2) + 0.7 e^(-160 w^2), w = 2 (v - 0.5)
  shader("TTO/Sheep/Celestial Ray", d => additive(d, `
    uniform float uTime; varying vec4 vC; varying vec2 vUv;
    ${smooth}
    void main() {
      float u = vUv.x, w = (vUv.y - 0.5) * 2.0;
      float prof = 0.3 * exp2(-w * w * 25.968512) + 0.7 * exp2(-w * w * 230.831207);
      float A = (sin(u * 18.0 - uTime * 4.0) * 0.15 + 0.85) * sm(u * 8.333334) * (1.0 - sm((u - 0.65) * 2.857143)) * prof * vC.a;
      vec3 rgb = vC.rgb;${ADD_OUT}
    }`));
  // TTO/Sheep/Prism Veil (dxbc_Prism_Veil.txt, Cull Back): a fresnel f = (1 - |n.v|)^2.6, the lattice texture's
  // luminance (0.3, 0.59, 0.11) x its alpha, a band b = (cos(2 pi (v - 0.22 _Time.y)) / 2 + 0.5)^24 scrolling up;
  // alpha = sat(0.72 f + lum (0.65 b + 0.1) + 0.09 b), colour = mix(vertex colour, (0.72, 0.96, 1), 0.5 f + 0.15 b).
  // Cull Back inside the mirror group (det < 0): three's BackSide keeps Unity's front faces
  shader("TTO/Sheep/Prism Veil", d => {
    const tx = d.tex ? api.texLoader.load(`${api.DATA}fx/tex/${d.tex}.webp`) : null;
    if (tx) { tx.colorSpace = THREE.SRGBColorSpace; tx.wrapS = tx.wrapT = THREE.RepeatWrapping; }
    const hi = [0.72, 0.96, 1].map(toLin);
    return additive(d, `
    uniform float uTime; uniform sampler2D map; varying vec4 vC; varying vec2 vUv; varying vec3 vN; varying vec3 vV;
    void main() {
      float f = pow(1.0 - min(abs(dot(normalize(vN), normalize(vV))), 1.0), 2.6);
      vec4 t = texture2D(map, vUv);
      float lum = dot(t.rgb, vec3(0.3, 0.59, 0.11)) * t.a;
      float b = pow(cos((vUv.y - uTime * 0.22) * 6.283185) * 0.5 + 0.5, 24.0);
      float A = clamp(b * 0.09 + lum * (b * 0.65 + 0.1) + f * 0.72, 0.0, 1.0) * vC.a;
      vec3 rgb = mix(vC.rgb, vec3(${hi.join(", ")}), f * 0.5 + b * 0.15);${ADD_OUT}
    }`, { side: THREE.BackSide, uniforms: { map: { value: tx } } });
  });
  // Standard (the Codex book's seven materials: _Color, _Metallic, _Glossiness, _EmissionColor, _MainTex): three's
  // MeshStandardMaterial with the same numbers (roughness = 1 - smoothness). APPROX: Unity lights it with its sky's
  // reflections; the page has no environment map, so the metal parts (antique gold 0.65) read darker than in the game.
  // Inside the mirror group Unity's front faces are three's back faces (det < 0 flips the winding): drawn double-sided
  // with the face direction turned round, so the normals light the outside
  shader("Standard", d => {
    const p = d.props || {}, c = d.color || [1, 1, 1, 1], e = p._EmissionColor || [0, 0, 0, 1];
    const m = new THREE.MeshStandardMaterial({ side: THREE.DoubleSide, metalness: p._Metallic ?? 0, roughness: 1 - (p._Glossiness ?? 0.5) });
    m.color.setRGB(c[0], c[1], c[2], THREE.SRGBColorSpace);
    m.emissive.setRGB(e[0], e[1], e[2], THREE.SRGBColorSpace);
    if (d.tex) {
      const t = api.texLoader.load(`${api.DATA}fx/tex/${d.tex}.webp`);
      t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping;
      t.repeat.fromArray(d.scale || [1, 1]); t.offset.fromArray(d.offset || [0, 0]);
      m.map = t;
    }
    // (onBeforeCompile sees the #include lines, not the chunks: the chunk goes in with its sign turned)
    m.onBeforeCompile = sh => { sh.fragmentShader = sh.fragmentShader.replace("#include <normal_fragment_begin>",
      THREE.ShaderChunk.normal_fragment_begin.replace("gl_FrontFacing ? 1.0 : - 1.0", "gl_FrontFacing ? - 1.0 : 1.0")); };
    return m;
  });
  // Particles/Standard Unlit (Unity's, tto_Point: _Mode 2 Fade, _SrcBlend 5 / _DstBlend 10, _ColorMode 0 multiply,
  // _Cull 0, _ZWrite 0, _Color 6.35 HDR): _Color x vertex colour x texture, blended by its own factors.
  // APPROX: the HDR _Color is used as a linear multiplier (the output clamps it, as an LDR screen does); soft particles
  // and camera fading (_SoftParticlesEnabled) are not drawn
  const BF = [THREE.ZeroFactor, THREE.OneFactor, THREE.DstColorFactor, THREE.SrcColorFactor, THREE.OneMinusDstColorFactor,
    THREE.SrcAlphaFactor, THREE.OneMinusSrcColorFactor, THREE.DstAlphaFactor, THREE.OneMinusDstAlphaFactor,
    THREE.SrcAlphaSaturateFactor, THREE.OneMinusSrcAlphaFactor];
  shader("Particles/Standard Unlit", d => {
    const p = d.props || {}, c = p._Color || d.color || [1, 1, 1, 1];
    const m = new THREE.MeshBasicMaterial({ vertexColors: true, transparent: true, depthWrite: !!p._ZWrite,
      side: p._Cull === 0 ? THREE.DoubleSide : THREE.BackSide, opacity: Math.min(1, c[3]), blending: THREE.CustomBlending,
      blendSrc: BF[p._SrcBlend ?? 5], blendDst: BF[p._DstBlend ?? 10], blendSrcAlpha: THREE.OneFactor, blendDstAlpha: THREE.OneMinusSrcAlphaFactor });
    m.color.setRGB(c[0], c[1], c[2]);
    if (d.tex) {
      const t = api.texLoader.load(`${api.DATA}fx/tex/${d.tex}.webp`);
      t.colorSpace = THREE.SRGBColorSpace; t.repeat.fromArray(d.scale || [1, 1]); t.offset.fromArray(d.offset || [0, 0]);
      m.map = t;
    }
    return m;
  });

  // ---------------------------------------------------------------- lines (Unity's LineRenderer / TrailRenderer)
  // A strip through the points, facing the camera (alignment 0, View: each point's side = tangent x (camera - point)),
  // width and colour by the share of the line's length (Unity's widthCurve x widthMultiplier and colorGradient), u
  // along the length 0..1 (textureMode 0, Stretch), v across. numCornerVertices / numCapVertices are 0 in every Sheep
  // line. The game's colours are gamma values: made linear as the page's vertex colours are
  const material = (fx, data, c, mat) => {
    const n = c.m_Materials?.[0];
    return n && data.materials?.[n] ? api.fxMaterial(fx.cls, n, data.materials[n]) : mat;
  };
  function drawLine(fx, node, mesh, L, wAt, cAt, cam) {
    const n = L.length;
    if (n < 2) { api.setMesh(mesh, [], [], [], []); return; }
    const um = uMat(fx, node);
    mesh.matrix.copy(um.clone().invert()); mesh.matrixWorldNeedsUpdate = true;   // the points are in Unity's world
    const eye = camPos(fx), acc = [0];
    for (let i = 1; i < n; i++) acc.push(acc[i - 1] + L[i].distanceTo(L[i - 1]));
    const len = acc[n - 1] || 1, pos = [], col = [], uv = [], idx = [];
    let side = cam.right.clone();
    for (let i = 0; i < n; i++) {
      const t = acc[i] / len, tan = L[Math.min(n - 1, i + 1)].clone().sub(L[Math.max(0, i - 1)]);
      const s = V().crossVectors(tan, eye.clone().sub(L[i]));
      if (s.lengthSq() > 1e-12) side = s.normalize();                       // seen end-on: keep the last good side
      const w = wAt(t) / 2, a = L[i].clone().addScaledVector(side, -w), b = L[i].clone().addScaledVector(side, w), k = cAt(t);
      pos.push(a.x, a.y, a.z, b.x, b.y, b.z); col.push(...k, ...k); uv.push(t, 0, t, 1);
      if (i) { const q = 2 * i - 2; idx.push(q, q + 1, q + 2, q + 2, q + 1, q + 3); }
    }
    api.setMesh(mesh, pos, col, uv, idx);
  }
  const lineMesh = (node, mat) => { const m = api.fxMesh(node, mat); m.matrixAutoUpdate = false; return m; };

  // LineRenderer: m_Positions (world with m_UseWorldSpace, else the node's own space), drawn every frame; a RabbitTracer
  // on the node drives it (positions, widths, colours: the fields below) and draws it after moving it
  api.part("LineRenderer", (fx, node, c, mat, nd, data) => {
    const C = api.curves, m0 = material(fx, data, c, mat);
    if (!C || !m0 || c.m_Enabled === false || nd.active === false) return null;
    const P = c.m_Parameters || {}, wc = C.curveFn(P.widthCurve), mult = P.widthMultiplier ?? 1, gc = C.gradFn(P.colorGradient);
    const mesh = lineMesh(node, m0);
    const line = { node, line: true, driven: false, world: !!c.m_UseWorldSpace,
      pts: (c.m_Positions || []).map(p => V(p.x, p.y, p.z)),
      width: t => wc(t) * mult, color: t => gc(t),
      draw(cam) {
        const um = uMat(fx, node), L = line.world ? line.pts : line.pts.map(p => p.clone().applyMatrix4(um));
        drawLine(fx, node, mesh, L, line.width, line.color, cam);
      },
      update(dt, cam) { if (!line.driven) line.draw(cam); } };
    return line;
  });

  // TrailRendererModern (Unity 5.5+'s TrailRenderer): a point where the node is once it has moved m_MinVertexDistance
  // from the last one (while m_Emitting), each kept m_Time seconds; the line runs from the node (t 0, the widthCurve's
  // and colorGradient's start) through the points newest to oldest (t 1). APPROX: Unity's own builder is not public;
  // t by the share of the trail's length, as its LineRenderer does
  api.part("TrailRendererModern", (fx, node, c, mat, nd, data) => {
    const C = api.curves, m0 = material(fx, data, c, mat);
    if (!C || !m0 || c.m_Enabled === false || nd.active === false) return null;
    const P = c.m_Parameters || {}, wc = C.curveFn(P.widthCurve), mult = P.widthMultiplier ?? 1, gc = C.gradFn(P.colorGradient);
    const mesh = lineMesh(node, m0), life = c.m_Time ?? 5, md2 = (c.m_MinVertexDistance ?? 0.1) ** 2, pts = [];
    let time = 0;
    return { node, update(dt, cam) {
      time += dt;
      const head = worldPos(fx, node);
      while (pts.length && time - pts[0].time > life) pts.shift();
      if (c.m_Emitting !== false && (!pts.length || pts[pts.length - 1].p.distanceToSquared(head) > md2)) pts.push({ p: head, time });
      if (c.m_Autodestruct && !pts.length) return "destroy";
      const L = [head];
      for (let i = pts.length - 1; i >= 0; i--) if (pts[i].p.distanceToSquared(L[L.length - 1]) > 1e-12) L.push(pts[i].p);
      drawLine(fx, node, mesh, L, t => wc(t) * mult, t => gc(t), cam);
    } };
  });

  // ---------------------------------------------------------------- RabbitTracer (TTO.Game TypeDefIndex 3914)
  // Fields: life (0.35 by its .ctor@0x1E6F4A0), travel (0.06), width (0.12), head (a Transform); the beam's prefab:
  // life 0.4, travel 0.08, width 0.34, head = its Head node (the Glint). Sheep::Row6Beam@0x1E5D640 spawns it at the
  // hand looking at the target's chest and calls Set(hand, chest):
  // - Set@0x1E6F280: mLine = GetComponent<LineRenderer>; useWorldSpace = true; 2 positions; mFrom, mTo; mStart =
  //   Time.time; mStartColor / mEndColor = the line's startColor / endColor (the gradient's ends); transform.position =
  //   from; Apply(0); Destroy(gameObject, life + 0.05)
  // - Update@0x1E6F420: Apply(Time.time - mStart) while mLine exists
  // - Apply(t)@0x1E6EF20 (constants read at their addresses: 1, 0.01, 0.85, 0.7, 0.5): h = travel > 0 ?
  //   clamp01(t / travel) : 1; f = clamp01((t - travel) / max(0.01, life - travel)); head = lerp(from, to, h);
  //   tail = lerp(from, to, clamp01(0.85 f^2)); SetPosition(0, tail), SetPosition(1, head); w = (1 - 0.7 f) x width:
  //   startWidth 0.5 w, endWidth w; startColor = mStartColor with alpha x (1 - f), endColor = mEndColor the same;
  //   head.position = head: the beam shoots out in `travel` seconds, then its tail runs after it as it thins and fades.
  // On the page: from = where the cue put the node, to = the cue's `to`; with no `to` there is no target and nothing is
  // drawn (the game always has one). APPROX: Unity's startWidth / endWidth and start / endColor setters reshape the
  // width curve and the gradient; the line is drawn as the straight lerp between the two ends (exact for the beam's
  // one-key width curve and two-key gradient)
  api.part("RabbitTracer", (fx, node, e) => {
    const line = fx.emitters.find(x => x.node === node && x.line), to = target(fx);
    if (!line || !to || e.enabled === false) {
      if (line && !to) console.warn("RabbitTracer: no cue `to` (the target's chest), the beam is not drawn", fx.name);
      if (line) line.driven = true, line.pts = [];
      return null;
    }
    const from = worldPos(fx, node), sc = line.color(0), ec = line.color(1);
    const head = e.head && typeof e.head === "object" && "node" in e.head ? fx.nodes[e.head.node] : null;
    const life = e.life ?? 0.35, travel = e.travel ?? 0.06, width = e.width ?? 0.12;
    line.driven = true; line.world = true;
    let t = 0, ws = 0, we = 0, fade = 0;
    line.width = u => ws + (we - ws) * u;
    line.color = u => [0, 1, 2].map(j => sc[j] + (ec[j] - sc[j]) * u).concat((sc[3] + (ec[3] - sc[3]) * u) * (1 - fade));
    const apply = t => {
      const h = travel > 0 ? clamp01(t / travel) : 1, f = clamp01((t - travel) / Math.max(0.01, life - travel));
      const hp = from.clone().lerp(to, h);
      line.pts = [from.clone().lerp(to, clamp01(0.85 * f * f)), hp];
      const w = (1 - 0.7 * f) * width; ws = 0.5 * w; we = w; fade = f;
      if (head?.parent) setWorldPos(fx, head, hp);                       // (not yet attached while the Fx is built)
    };
    apply(0);
    return { node, update(dt, cam) {
      t += dt;
      if (t >= life + 0.05) return "destroy";                            // Destroy(gameObject, life + 0.05)
      apply(t); line.draw(cam);
    } };
  });

  // ---------------------------------------------------------------- Sheep.BreathFly (TTO1102:Sheep.<BreathFly>d__261
  // ::MoveNext@0x1E72EA0, pseudo/Sheep.c:1-374): `to` = the target's chest (Row6Chest), or with no target
  // from + 3 x the Sheep's forward; flight = clamp(|to - from| x 0.0625, 0.15, 0.6) s; the wisp spawned at from (the
  // mouth). Every frame while now < t0 + flight: u = (now - t0) / flight, p = lerp(from, to, clamp01(u)) +
  // up x u x 0.9 x (1 - u) (a 0.225 m arc at the middle), the rotation LookRotation(p - position + forward x 0.0001)
  // (facing its motion; its first frame, not moving, looks along world forward), then the position; the first frame
  // past the flight: Destroy(wisp, 0.3) (the land / revive follow in the coroutine: cues). `to` follows a moving target
  // in the game: the page's is still. No `to` on the cue = the game's no-target path
  api.part("Sheep.BreathFly", (fx, node) => {
    const from = worldPos(fx, node), to = target(fx) || from.clone().add(V(0, 0, 3));
    const flight = Math.min(0.6, Math.max(0.15, from.distanceTo(to) * 0.0625));
    let age = 0, end = null;
    const q = new THREE.Quaternion();
    const place = () => {
      const u = age / flight, p = from.clone().lerp(to, clamp01(u)); p.y += u * 0.9 * (1 - u);
      const cur = worldPos(fx, node);
      node.quaternion.copy(lookRot(p.clone().sub(cur).add(V(0, 0, 0.0001)), q));
      setWorldPos(fx, node, p);
    };
    place();
    return { node, update(dt) {
      age += dt;
      if (end != null) return age >= end ? "destroy" : undefined;
      if (age < flight) place();
      else end = age + 0.3;
    } };
  });

  // ---------------------------------------------------------------- Sheep.CodexOpen (TTO1102:Sheep.<CodexOpen>d__265
  // ::MoveNext@0x1E73940, pseudo/Sheep.c:392-716): the book is spawned at hover + 3 up (hover = the spot + 2.6 up; the
  // cue places the node at hover) turned CodexRotation (the cue's rot). Each frame, for read k = 0..9 at readAt =
  // t0 + 2 (k + 1): while now < readAt, position = hover + up x CodexBob(now - t0) (Sheep::CodexBob@0x1E55980:
  // 0.12 sin(2.2 t) + 3 (1 - clamp01(t / 0.6))^2: the drop from 5.6 m over 0.6 s, then a 0.12 m bob) and FlipPivot's
  // local rotation = CodexFlipAngle(readAt - now) (@0x1E55A00: s = 1 - clamp01(left / 0.45), Euler(0, 0, -180 deg x
  // (3 s^2 - 2 s^3)): a page turning over the 0.45 s before the read); at the read FlipPivot snaps back to identity and
  // CodexRead spawns the page effects (cues); after the tenth, grandCodex_close (a cue) and Destroy(book, 0.1)
  api.part("Sheep.CodexOpen", (fx, node) => {
    const hover = node.position.clone();
    let flip = null;                         // Transform.Find("FlipPivot"): a child, attached after the root is built
    const bob = t => 0.12 * Math.sin(2.2 * t) + 3 * (1 - clamp01(t / 0.6)) ** 2;
    const E = new THREE.Euler();
    let age = 0, k = 0, end = null;
    const frame = () => {
      flip ||= fx.nodes.find(o => o.parent === node && o.name === "FlipPivot");
      while (k < 10 && age >= 2 * (k + 1)) { flip?.quaternion.identity(); k++; }   // the read (one per 2 s)
      if (k >= 10) { end ??= age + 0.1; return; }                                 // Destroy(book, 0.1)
      node.position.set(hover.x, hover.y + bob(age), hover.z);
      if (flip) {
        const s = 1 - clamp01((2 * (k + 1) - age) / 0.45);
        flip.quaternion.setFromEuler(E.set(0, 0, -Math.PI * (3 * s * s - 2 * s * s * s), "YXZ"));
      }
      node.updateMatrixWorld(true);
    };
    frame();
    return { node, update(dt) {
      age += dt;
      if (end != null && age >= end) return "destroy";
      if (end == null) frame();
    } };
  });
}
