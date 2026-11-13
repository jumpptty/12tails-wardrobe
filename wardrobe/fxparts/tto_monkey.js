// wardrobe/fxparts/tto_monkey.js: what the Monkey's released TTO skills (Ja Ascension's passive and active, Buiten
// Bastion's passive, Rune Golem) draw that no other part does (builder "tto_monkey", 2026-11-13; plans/fx_monkey/
// decisions.md 29, 40, 54, 61, 63; tto.md sections 1, 2.2, 2.5, 5, 6 with its checker Verification 1, 4, 6; parts.md T2-T5
// with its Verification 5, 6, 10, 11). TTO1102 = DecompiledSource_TTO_2026-11-02 (client/GameAssembly.dll): pseudo/Monkey.c
// and pseudo_c6_extra/monkey/RuneGolem.c cited by line; the bodies never decompiled (MonkeyRow6Rise, RuneGolem::Once /
// Loop) read here with capstone over the client's GameAssembly.dll (calls named from methods.tsv), cited by RVA.
//
//   shaders   Eric/URP Particles/Additive, Eric/URP Particles/Alpha Blended (Hovl's particle shaders, 39 + 2 materials):
//             page materials through api.shader
//   Animator  the Sigils' FX_Magic_Circle controller (jaAscension_callFx, runeGolem_circle, jaAscension_aura): its one
//             clip's _MainTex_ST.w curve on the bound renderer's own material copy, looping
//   SunCrownFx        solarCrown: the halo over the hero's head and the orbiting sun (LateUpdate@0x1D6DED0)
//   Monkey.SunComet   sunAvatar_comet's flight (<RPC_sunAvatar_cast>d__352, CODE_MOVERS)
//   Monkey.SolarCollapse  sunAvatar_dive's rise and dive (TTO1102 <RPC_solarCollapse>d__363, CODE_MOVERS)
//   RuneGolem         the summon itself: Rise, the aura pulses with Stone Aegis on the hero, Think (quake / walk / pound /
//                     fist), its glow, CrumbleAway at the cue's `end`
//   MonkeyRow6Rise    runeGolem_quake's six spikes (Awake / Update / Place, capstone)
// Not built (decision 54): SunburnFx, BastionWardFx, MonkeyBuitenOffering (no released tile spawns them).
//
// Cue options read (fx.at; [x, y, d] = metres right / up / ahead of the hero, re-read from her present pose each frame):
//   sunAvatar_comet  to (the end: her head, default [0, 1.95, 0]), rise (the Bezier's lift over the midpoint, default 4.24)
//   solarCrown       head (HeadHeight, default 1.35: the Monkey's CharacterController top, tto.md section 1)
//   sunAvatar_dive   top (the rise's end: a y, or [x, y, d]; default the spawn + 5 up), to (the dive's end, default her
//                    feet + 0.5 up: TTO1102's, decision 29), dive (the dive's time, default 0.3)
//   RuneGolem        to (the target's feet, default [0, 0, 10]; its body r 0.3, Bat decision 4), end (seconds after the
//                    spawn when it crumbles: the standing 10 s cut, default 10)
// Space: everything in the effect's Unity world (the mirror group's space: the hero's feet at the origin when the effect
// was made, facing +z, the floor at y 0); Unity's local numbers apply inside the mirror as they are (three's "YXZ" =
// Unity's Euler). An effect a script Instantiates (api.spawn) is placed from the hero's PRESENT pose, so every spot handed
// over goes through the world (spawnAt, as tto_mole.js). Clocks: t += dt from the first update.
export default function register(api) {
  const { THREE, V } = api;
  const DEG = Math.PI / 180;
  const clamp01 = x => (x < 0 ? 0 : x > 1 ? 1 : x);
  const num = (x, d = 0) => (x !== null && x !== "" && x !== undefined && Number.isFinite(+x) ? +x : d);
  const vec = (a, d) => (Array.isArray(a) && a.length >= 3 ? V(num(a[0]), num(a[1]), num(a[2])) : d);
  const UP = V(0, 1, 0), FWD = V(0, 0, 1);
  const toLin = c => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
  const warned = new Set();
  const warnOnce = (k, ...m) => { if (!warned.has(k)) { warned.add(k); console.warn("tto_monkey:", ...m); } };
  // the effect's Unity world <-> the page's world; the hero's own Unity frame (her root x the mirror) in the page's world
  const heroFrame = () => {
    const H = api.hero?.();
    if (!H?.root) return null;
    H.root.updateWorldMatrix(true, false);
    const p = V(), q = new THREE.Quaternion();
    H.root.getWorldPosition(p); H.root.getWorldQuaternion(q);
    return new THREE.Matrix4().compose(p, q, V(1, 1, 1)).multiply(new THREE.Matrix4().makeScale(-1, 1, 1));
  };
  const mirrorInv = fx => { fx.mirror.updateWorldMatrix(true, false); return fx.mirror.matrixWorld.clone().invert(); };
  // a point given in the hero's frame ([x, y, d] at her present pose) in fx's Unity world (the effect's own frame when
  // the hero is missing)
  const heroPoint = (fx, p) => { const H = heroFrame(); return H ? p.clone().applyMatrix4(H).applyMatrix4(mirrorInv(fx)) : p.clone(); };
  const heroQuat = fx => {                                               // her rotation in fx's Unity world
    const H = heroFrame(), q = new THREE.Quaternion();
    if (H) H.premultiply(mirrorInv(fx)).decompose(V(), q, V());
    return q;
  };
  // the cue options of an effect Instantiated at a pose (position p, rotation q) of fx's Unity world (tto_mole.js)
  const spawnAt = (fx, p, q) => {
    const H = heroFrame();
    if (!H) return null;
    fx.mirror.updateWorldMatrix(true, false);
    const pos = V(), rq = new THREE.Quaternion();
    H.invert().multiply(fx.mirror.matrixWorld).multiply(new THREE.Matrix4().compose(p, q || new THREE.Quaternion(), V(1, 1, 1))).decompose(pos, rq, V());
    const e = new THREE.Euler().setFromQuaternion(rq, "YXZ");
    return { x: pos.x, y: pos.y, d: pos.z, rot: [e.x / DEG, e.y / DEG, e.z / DEG] };
  };
  const prefixOf = fx => { const i = String(fx.name).lastIndexOf("/"); return i >= 0 ? fx.name.slice(0, i + 1) : ""; };
  const spawn = (fx, name, p, q) => {
    const at = spawnAt(fx, p, q);
    const f = at && api.spawn?.(prefixOf(fx) + name, at);
    if (!f) warnOnce("spawn:" + name, prefixOf(fx) + name, "not spawned (not in fx.json: the entry's builds)");
    return f;
  };
  // Transform.set_position / set_rotation for a node under the root (its parent's Unity-world matrix undone)
  const uMat = (fx, o) => { o.updateWorldMatrix(true, false); return mirrorInv(fx).multiply(o.matrixWorld); };
  const setWorldPos = (fx, o, w) => { o.position.copy(o.parent === fx.mirror ? w : w.clone().applyMatrix4(uMat(fx, o.parent).invert())); };
  const setWorldRot = (fx, o, q) => {
    const pq = new THREE.Quaternion();
    if (o.parent !== fx.mirror) uMat(fx, o.parent).decompose(V(), pq, V());
    o.quaternion.copy(pq.invert().multiply(q));
  };
  // Quaternion.LookRotation(forward, up) in Unity's numbers (tto_sheep.js)
  const lookRot = (f, q = new THREE.Quaternion()) => {
    const z = f.clone().normalize(), x = V().crossVectors(UP, z);
    if (x.lengthSq() < 1e-12) x.set(1, 0, 0); x.normalize();
    return q.setFromRotationMatrix(new THREE.Matrix4().makeBasis(x, V().crossVectors(z, x), z));
  };
  const flat = v => V(v.x, 0, v.z);
  const T = () => performance.now() / 1000;    // Unity's Time.time for the scene-clock parts (APPROX: the phase only)
  const time = { get value() { return T(); } };

  // ---------------------------------------------------------------- Eric/URP Particles/Additive, Alpha Blended
  // Hovl Studio's particle shaders (parts.md T2 with its Verification 10, tto.md Verification 4; the compiled programs are
  // not in the bundles: APPROX from the property set). Pass state (shader_v.py): Additive Blend One [_Blend2] (every
  // material saves _Blend2 1: One One), Cull [_CullMode], ZWrite Off, ColorMask RGB; Alpha Blended SrcAlpha
  // OneMinusSrcAlpha, ZWrite Off. The stale _SrcBlend / _DstBlend / _ZWrite some materials save (no such property in
  // either shader) and their _TintColor are ignored. _Noise / _Flow / _Mask are unset, _Usecenterglow / _Usedepth /
  // _Usecustomrandom 0 in every Monkey material, so the fragment is
  //   col = tex(uv) x _Color x vertex colour x _Emission (rgb), a = tex.a x _Color.a x vertex alpha (x _Opacity: Alpha Blended)
  //   uv = uv0 x _MainTex_ST.xy + _MainTex_ST.zw + _Time.y x _SpeedMainTexUVNoiseZW.xy (tto_Trail_01_1: v -0.8 / s)
  //   Additive: rgb x a added (One One); Alpha Blended: rgb over by a.
  // On the page the products are made in gamma (TTO's convention, tto_sheep.js / tto_penguin.js: the texture and the
  // vertex colours arrive linear, so their product is taken back to gamma), clamped to 0..1 as the game's 8-bit target
  // clamps them (the HDR _Color 5.28 of tto_flare_h47s10 saturates there, no clamp before), then made linear for the
  // output. The additive one writes the page's additive convention (premultiplied, canvas alpha = its brightest channel,
  // index.html fxMaterial). _CullMode: 0 Off (every Monkey material), 1 Front, 2 Back (inside the mirror group three's
  // FrontSide keeps Unity's front faces, tto_penguin.js). Fog is not drawn. The clock: the page's (APPROX: the phase).
  // uniforms.uST is the renderer's _MainTex_ST (the Animator part below writes its own material copy's)
  const ERIC_VERT = `
    uniform vec4 uST; uniform vec2 uSpeed; uniform float uTime;
    varying vec4 vC; varying vec2 vUv;
    void main() {
    #ifdef USE_COLOR_ALPHA
      vC = color;
    #elif defined(USE_COLOR)
      vC = vec4(color, 1.0);
    #else
      vC = vec4(1.0);
    #endif
      vUv = uv * uST.xy + uST.zw + uSpeed * uTime;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }`;
  const ERIC_FRAG = alpha => `
    uniform sampler2D map; uniform float uHasMap, uE, uOp; uniform vec4 uColor;
    varying vec4 vC; varying vec2 vUv;
    vec3 lin3(vec3 c) { return mix(c / 12.92, pow((c + 0.055) / 1.055, vec3(2.4)), step(vec3(0.04045), c)); }
    vec3 gam3(vec3 c) { return mix(c * 12.92, 1.055 * pow(c, vec3(1.0 / 2.4)) - 0.055, step(vec3(0.0031308), c)); }
    void main() {
      vec4 t = uHasMap > 0.5 ? texture2D(map, vUv) : vec4(1.0);
      vec3 g = clamp(gam3(t.rgb * vC.rgb) * uColor.rgb * uE, 0.0, 1.0);
      float a = clamp(t.a * vC.a * uColor.a * uOp, 0.0, 1.0);
      vec4 o = linearToOutputTexel(vec4(lin3(g), 1.0));
      ${alpha ? "gl_FragColor = vec4(o.rgb, a);" : "o.rgb *= a; gl_FragColor = vec4(o.rgb, max(o.r, max(o.g, o.b)));"}
    }`;
  const eric = alpha => d => {
    const p = d.props || {}, c = p._Color || d.color || [1, 1, 1, 1], s = p._SpeedMainTexUVNoiseZW || [0, 0, 0, 0];
    const cull = num(p._CullMode), tex = d.tex ? api.texLoader.load(`${api.DATA}fx/tex/${d.tex}.webp`) : null;
    if (tex) { tex.colorSpace = THREE.SRGBColorSpace; tex.wrapS = tex.wrapT = THREE.RepeatWrapping; }
    return new THREE.ShaderMaterial({
      vertexShader: ERIC_VERT, fragmentShader: ERIC_FRAG(alpha), vertexColors: true, transparent: true, depthWrite: false,
      side: cull === 2 ? THREE.FrontSide : cull === 1 ? THREE.BackSide : THREE.DoubleSide,
      blending: alpha ? THREE.NormalBlending : THREE.CustomBlending,
      ...(alpha ? {} : { blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor, blendSrcAlpha: THREE.OneFactor, blendDstAlpha: THREE.OneMinusSrcAlphaFactor }),
      uniforms: { map: { value: tex }, uHasMap: { value: tex ? 1 : 0 }, uColor: { value: new THREE.Vector4(...c.map(x => num(x, 1))) },
        uE: { value: num(p._Emission, 1) }, uOp: { value: alpha ? num(p._Opacity, 1) : 1 },
        uST: { value: new THREE.Vector4(...(d.scale || [1, 1]), ...(d.offset || [0, 0])) },
        uSpeed: { value: new THREE.Vector2(num(s[0]), num(s[1])) }, uTime: time },
    });
  };
  if (!api.shader) console.warn("tto_monkey: api.shader missing (index.html), the Eric shaders draw as plain alpha");
  api.shader?.("shader:Eric/URP Particles/Additive", eric(false));
  api.shader?.("shader:Eric/URP Particles/Alpha Blended", eric(true));

  // ---------------------------------------------------------------- Animator (FX_Magic_Circle)
  // A Mecanim controller with one 2 s looping clip (tto.md section 5; parts.md Verification 11, decision 63) that animates
  // a ParticleSystemRenderer's material vector _MainTex_ST: x, y, z constant (1, 1, 0), w (the V offset) 0 -> -1 over 2 s.
  // wardrobe_fx_tto.py writes it {"type": "Animator", "uv": {"len": 2, "w": [[0, 0], [2, -1]], path?}} (only the animated
  // components; the constant ones are the material's own). The binding's path is relative to the Animator's node: probed
  // here (the clip's genericBindings path 2170003325 = CRC32("glow/line"): the Sigil's grandchild `line`, the only renderer
  // it moves; the Sigil's own renderer is m_Enabled false), so "glow/line" stands in while the export carries no path.
  // That `line` renderer is m_Enabled false itself in all three probed Sigils (and the clip animates nothing else), so
  // the scroll shows nothing, in the game either: built as decision 63 asks, it acts only where a renderer is drawn.
  // Unity writes it through the renderer (a MaterialPropertyBlock): here the bound renderer's own material copy (its
  // Eric shader's uST uniform; any other material: its own clone of the map, set once the picture is in, as uvscroll.js),
  // freed in dispose. The curve: linear between its keys (the streamed keys' cubic is linear here: c -0.5 / s, d 0 ->
  // -1), the clock the Animator's own from the spawn, looping at len (m_LoopTime). Unity's and three's offsets share the
  // sense (uvscroll.js), so no sign change
  const curve = (keys, t) => {
    if (!Array.isArray(keys) || !keys.length) return null;
    if (t <= keys[0][0]) return num(keys[0][1]);
    for (let i = 1; i < keys.length; i++) if (t <= keys[i][0]) {
      const [a, va] = keys[i - 1], [b, vb] = keys[i];
      return b > a ? num(va) + (num(vb) - num(va)) * (t - a) / (b - a) : num(vb);
    }
    return num(keys[keys.length - 1][1]);
  };
  api.part("Animator", (fx, node, c) => {
    const uv = c.uv;
    if (!uv || c.enabled === false || !(num(uv.len) > 0)) return null;
    const path = typeof uv.path === "string" ? uv.path : "glow/line";
    let t = 0, mesh, mat = null, map = null, mine = [];
    const find = () => {                                     // late: the bound node is built after this one
      let o = node;
      for (const n of path.split("/").filter(Boolean)) { o = o?.children.find(x => x.name === n); }
      if (!o) { warnOnce("anim:" + fx.name, fx.name, "Animator: no node at", path); return null; }
      // (a disabled renderer draws no mesh: nothing to scroll; so in every probed Sigil, whose `line` renderer is
      // m_Enabled false, as the game draws it)
      const m = o.children.find(x => x.isMesh) || null;
      if (!m?.material || Array.isArray(m.material)) return null;
      const m0 = m.material, cl = m0.clone();
      cl.onBeforeCompile = m0.onBeforeCompile; cl.customProgramCacheKey = m0.customProgramCacheKey;
      cl.userData.fxBlend = m0.userData.fxBlend;
      if (cl.uniforms) {                                     // cloneUniforms copied the texture and froze the clock
        if (m0.uniforms.map) cl.uniforms.map.value = m0.uniforms.map.value;
        if (m0.uniforms.uTime) cl.uniforms.uTime = m0.uniforms.uTime;
      }
      m.material = cl; mine.push(cl); mat = cl;
      return m;
    };
    return { node, update(dt) {
      if (mesh === undefined) mesh = find();
      if (!mesh) return;
      t += dt;
      const k = t % num(uv.len), st = [curve(uv.x, k), curve(uv.y, k), curve(uv.z, k), curve(uv.w, k)];
      if (mat.uniforms?.uST) { const u = mat.uniforms.uST.value; st.forEach((x, i) => { if (x != null) u.setComponent(i, x); }); return; }
      if (!map) {
        if (!mat.map?.image) return;                         // no picture yet (uvscroll.js)
        map = mat.map.clone(); mine.push(map); mat.map = map;
      }
      if (st[0] != null) map.repeat.x = st[0]; if (st[1] != null) map.repeat.y = st[1];
      if (st[2] != null) map.offset.x = st[2]; if (st[3] != null) map.offset.y = st[3];
    }, dispose() { for (const m of mine) m.dispose(); mine = []; } };
  });

  // ---------------------------------------------------------------- SunCrownFx (solarCrown)
  // SunCrownFx::LateUpdate@0x1D6DED0 (never decompiled; tto.md 2.2 from suncrown_late.asm): each frame
  //   halo.position = holder.position + up x (HeadHeight + 0.35) - holder.forward x 0.25, halo.rotation = holder.rotation;
  //   ring.localRotation = Euler(0, 0, Time.time x ringSpeed) (ring null in this prefab);
  //   orbit.localPosition = (orbitRadius cos a, 0.25 sin 2a, orbitRadius sin a), a = Time.time x orbitSpeed x Deg2Rad
  // (fields from the prefab: halo node 1, orbit node 6, 0.75, 140, 40). The holder is the hero (the status look sits on
  // her, CharacterControl::AddMonkeyRow6Fx@0x24AD6A0); HeadHeight = the cue's `head` (1.35). Not drawn: its renderer
  // switch by the holder's hiding statuses (none on the page)
  api.part("SunCrownFx", (fx, node, c) => {
    const ref = r => (r && typeof r.node === "number" ? fx.nodes[r.node] : null);
    const head = num(fx.at?.head, 1.35), rad = num(c.orbitRadius, 0.75), spd = num(c.orbitSpeed, 140), rs = num(c.ringSpeed, 40);
    const eu = new THREE.Euler();
    return { node, update() {
      const halo = ref(c.halo), ring = ref(c.ring), orbit = ref(c.orbit), now = T();
      if (halo) {
        const q = heroQuat(fx), p = heroPoint(fx, V());
        setWorldPos(fx, halo, p.addScaledVector(UP, head + 0.35).addScaledVector(FWD.clone().applyQuaternion(q), -0.25));
        setWorldRot(fx, halo, q);
      }
      if (ring) ring.quaternion.setFromEuler(eu.set(0, 0, now * rs * DEG, "YXZ"));
      if (orbit) { const a = now * spd * DEG; orbit.position.set(rad * Math.cos(a), 0.25 * Math.sin(2 * a), rad * Math.sin(a)); }
    } };
  });

  // ---------------------------------------------------------------- Monkey.SunComet (sunAvatar_comet)
  // TTO1102:Monkey.<RPC_sunAvatar_cast>d__352::MoveNext@0x1D20100 (pseudo/Monkey.c:20689-20826): every frame to 0.9 s the
  // comet's position = Monkey::Bezier(start, mid + up x rise, end, s) (Monkey.c:44450-44475: (1-s)^2 a + 2(1-s)s b + s^2 c),
  // start = its spawn (the Ja + 1.2 up), end = the hero + up x (HeadHeight + 0.6), re-read each frame (:20772-20790),
  // mid = (start + end) / 2, s = (3 - 2u) u^2, u = age / 0.9 (:20811); its rotation untouched (identity). Destroyed at 0.9
  // (the cue's kill)
  api.part("Monkey.SunComet", (fx, node) => {
    let t = 0, start = null;
    const rise = num(fx.at?.rise, 4.24), to = vec(fx.at?.to, V(0, 1.95, 0));
    return { node, update(dt) {
      if (!start) start = node.position.clone();
      t += dt;
      const end = heroPoint(fx, to), u = clamp01(t / 0.9), s = (3 - 2 * u) * u * u, n = 1 - s;
      const b = start.clone().add(end).multiplyScalar(0.5).addScaledVector(UP, rise);
      node.position.copy(start).multiplyScalar(n * n).addScaledVector(b, 2 * n * s).addScaledVector(end, s * s);
    } };
  });

  // ---------------------------------------------------------------- Monkey.SolarCollapse (sunAvatar_dive)
  // TTO1102:Monkey.<RPC_solarCollapse>d__363::MoveNext@0x1D15280 (pseudo/Monkey.c:17382-17739; decision 29: TTO1102, the
  // sun falls on the Monkey): from the spawn (her head + 0.6), top = from + 5 up; 0.5 s: position = Lerp(from, top, k),
  // k = clamp01(1 - (1 - 2t)^2) (:17693-17718); then over 0.3 s Lerp(top, the Monkey + 0.5 up (re-read each frame), k),
  // k = clamp01(u^2) (:17650-17687); then the sun destroyed (the cue's kill) and the supernova (a cue). TTO1106+ aims the
  // dive at a selected foe over 0.3 + 0.015 x its flat distance: the cue's `to` / `dive` give that variant
  api.part("Monkey.SolarCollapse", (fx, node) => {
    let t = 0, from = null, top = null;
    const dive = Math.max(1e-3, num(fx.at?.dive, 0.3)), to = vec(fx.at?.to, V(0, 0.5, 0));
    return { node, update(dt) {
      if (!from) {
        from = node.position.clone();
        const tp = fx.at?.top;
        top = Array.isArray(tp) ? heroPoint(fx, vec(tp, V())) : typeof tp === "number" ? V(from.x, tp, from.z) : from.clone().addScaledVector(UP, 5);
      }
      t += dt;
      if (t < 0.5) { const k = 1 - 2 * t; node.position.lerpVectors(from, top, clamp01(1 - k * k)); }
      else { const u = (t - 0.5) / dive; node.position.lerpVectors(top, heroPoint(fx, to), clamp01(u * u)); }
    } };
  });

  // ---------------------------------------------------------------- MonkeyRow6Rise (runeGolem_quake's spikes)
  // Disassembled (capstone, TTO1102 GameAssembly.dll; fields dump.cs:112319: delay 0x20, depth 0x24, riseTime 0x28, hold
  // 0x2c, sinkTime 0x30, overshoot 0x34, tilt 0x38, mRest 0x3c, mRestRot 0x48, mBorn 0x58):
  //   Awake@0x1d16800: mRest = localPosition, mRestRot = localRotation, mBorn = Time.time, Place(0)
  //   Update@0x1d16c70: t = now - mBorn - delay; u = 0 when t <= 0; while t < riseTime an ease-out-back, x = t / riseTime,
  //     c = overshoot x 1.70158 / 0.1 (0x1d16cf7-0x1d16d03), u = 1 + (c + 1)(x - 1)^3 + c (x - 1)^2; then 1 until
  //     riseTime + hold; then 1 - clamp01((t - riseTime - hold) / max(0.01, sinkTime)) (0x1d16cbc-0x1d16cec); Place(u)
  //   Place@0x1d16880: localPosition = mRest + (0, -depth (1 - u), 0); if tilt != 0: axis = Cross(n, up), n = the rest
  //     position's flat direction normalized (Vector3.right when |flat|^2 <= 0.0001), localRotation =
  //     AngleAxis(clamp01(u) x tilt, axis) x mRestRot (0x1d16933-0x1d16c2a)
  api.part("MonkeyRow6Rise", (fx, node, c) => {
    const delay = num(c.delay), depth = num(c.depth), rise = num(c.riseTime), hold = num(c.hold), sink = Math.max(0.01, num(c.sinkTime));
    const ov = num(c.overshoot) * 1.70158 / 0.1, tilt = num(c.tilt);
    const rest = node.position.clone(), restRot = node.quaternion.clone(), n = flat(rest);
    const axis = n.lengthSq() > 1e-4 ? V().crossVectors(n.normalize(), UP) : V(1, 0, 0), q = new THREE.Quaternion();
    const place = u => {
      node.position.set(rest.x, rest.y - depth * (1 - u), rest.z);
      if (tilt) node.quaternion.copy(q.setFromAxisAngle(axis, clamp01(u) * tilt * DEG)).multiply(restRot);
    };
    place(0);
    let t = 0;
    return { node, update(dt) {
      t += dt;
      const s = t - delay;
      let u;
      if (s <= 0) u = 0;
      else if (s < rise) { const x = s / rise - 1; u = 1 + (ov + 1) * x * x * x + ov * x * x; }
      else if (s < rise + hold) u = 1;
      else u = 1 - clamp01((s - rise - hold) / sink);
      place(u);
    } };
  });

  // ---------------------------------------------------------------- RuneGolem (tto/RuneGolem's root)
  // TTO1102 RuneGolem (dump.cs:113918-114070; pseudo_c6_extra/monkey/RuneGolem.c), run as the game runs it on the page's one
  // target (decision 40, tto.md 2.5 with Verification 6; parts.md Verification 5). Golem time g from the spawn (the
  // create); Init@0x1D6AAA0 (:1073-1182): aura from 0.7, quake from 4, pound from 2.9 + 3, mLive, the Rise coroutine.
  //   Rise (<Rise>d__83@0x1D7C000, :667-972): state attack (busy), Stop, Once("summon", 0), Flare to 2.9, runeGolem_rise
  //     at its pose; the Model child at localPosition (0, -h (1 - u)^3, 0), u = g / 0.7, h = ModelHeight; at 0.7 (0, 0, 0),
  //     runeGolem_riseBurst at its pose (the shake and the r 6 hit: no look); 2.05 runeGolem_roar at TransformPoint(RoarAt3
  //     (0.12, 3.22, 0.52)); 2.9 standby (the AI's start).
  //   Update@0x1D6D170 (:1299-1385): while live, every 1.5 s from mNextAura the Aura, then (not busy, not ending) Think.
  //   Aura@0x1D69950 (:3118-3224): runeGolem_auraPulse at its position, identity; each player of its side within r 8 h 4
  //     (Damage.FindAreaTarget) gets Stone Aegis (0x396) for 3 s: the status look tto/stoneAegis on the hero, one kept
  //     while renewed (CharacterControl::AddMonkeyRow6Fx, tto.md section 1), gone 3 s after the last pulse.
  //   Think@0x1D6CA90 (:1388-1612), the target the cue's `to` (within VisionRange 14; else back to the owner, Idle within
  //     6 m): quake when g >= mNextQuake and the foe within 7 m (mNextQuake = g + 12, Face snap); else walk while the flat
  //     distance > 3.4 + the target collider's min(extent x, z) (0.3: 3.7 m); else pound when g >= mNextPound (mNextPound
  //     = g + 7, mNextFist = max(mNextFist, g + FistLength[2])); else Idle + Face (turning) until mNextFist; else a fist
  //     (mFistSide toggles, mNextFist = g + 1.6), Face snap.
  //   MoveToward@0x1D6B030 (:1755-1925): turn toward the flat direction at 360 deg/s (Slerp by min(1, dt 360 / angle)),
  //     state run, moveSpeed += (runSpeed - moveSpeed) min(1, 4 dt) (runSpeed: the prefab's CharacterControl, 3.25),
  //     Loop("run"), Footfall. Idle@0x1D6A940: mLastWalkPhase -1, standby, moveSpeed -> 0 by min(1, 6 dt) (0 under
  //     0.1), Loop("root"). Stop@0x1D6CA20: moveSpeed 0. Face@0x1D6A200: LookRotation(flat), snapped or turned 360 deg/s.
  //   Footfall@0x1D6A590 (:1926-2010): phase = frac(run state time / 1.2): runeGolem_step at TransformPoint(StepL
  //     (-0.99, 0, 0.22)) when the phase wraps, StepR (0.99, 0, 0.22) when it passes 0.5 (Step@0x1D6C940: its rotation).
  //   Fist (<Fist>d__84@0x1D6EF50, :130-442; .cctor FistHitAt [0.42, 0.42, 0.62], FistLength [1.0, 1.0, 1.35]): Face
  //     snap, Once("attack<step + 1>", 0.15) (capstone 0x1D6F77B); at FistHitAt: step 2 runeGolem_pound at
  //     TransformPoint(PoundAt (0, 0, 2.05)), else runeGolem_fistHit at TransformPoint(FistHitR (0.88, 1.63, 3.11) on
  //     step 0 / FistHitL (-0.87, 1.61, 3.11) on step 1), its rotation; Done (standby) at FistLength.
  //   Quake (<Quake>d__85@0x1D70C70, :445-585): Once("quake", 0.15), Flare 1.6, runeGolem_quakeCharge at its pose; at
  //     0.78 runeGolem_quake at TransformPoint(QuakeAt (0, 0, 2.02)) (Rune Fracture on the foe: no look, decision 51);
  //     Done at 1.6.
  //   LateUpdate@0x1D6ACF0 (:1203-1280): the body renderer's material 1 (tto_runeGolem_glow, Particles/Additive) gets
  //     _TintColor = (GlowColor (1, 0.55, 0.25), a), a = 0.85 while flaring (g < mFlareUntil), else 0.28 + 0.1 sin(2.4
  //     Time.time); not live: max(0, a - 0.6). (The cel body, material 0, is never touched.)
  //   The end: no limit in the game; at the cue's `end` the unsummon (unsummon@0x1D6DE00 -> Crumble@0x1D69F00: not live,
  //     ending, StopAllCoroutines, state dead, Stop) -> CrumbleAway (<CrumbleAway>d__87@0x1D6EBD0, :1-128):
  //     Once("collapse", 0.15), runeGolem_crumble at its pose; at 0.9 runeGolem_dust at its position, identity, and the
  //     Model sinks to (0, -h ((t - 0.9) / 1.5)^2, 0); Destroy at 2.4.
  //   Once@0x1D6B480 (capstone): the state's time = 0, CrossFade(clip, fade), its wrapMode 8 (ClampForever); Loop@0x1D6AEA0:
  //     CrossFade(clip, 0.25), animation.wrapMode = 2 (Loop). ModelHeight@0x1D6AF70: max(1, 2 x the collider's extent y +
  //     0.3) = 5.1 (CharacterController height 4.8).
  // APPROXIMATED: the CharacterControl's own mover (not traced: position += forward x moveSpeed x dt in run / standby,
  // never while attacking; its status caps do not apply); the run state's time restarts when the run starts again;
  // the network (ActionEvent), hits, shakes and the camera's onSummon are not drawn; Time.time = g (the glow's phase).
  const FIST_HIT_AT = [0.42, 0.42, 0.62], FIST_LEN = [1.0, 1.0, 1.35];
  const FIST_R = V(0.88, 1.63, 3.11), FIST_L = V(-0.87, 1.61, 3.11), POUND_AT = V(0, 0, 2.05), QUAKE_AT = V(0, 0, 2.02);
  const ROAR_AT = V(0.12, 3.22, 0.52), STEP_L = V(-0.99, 0, 0.22), STEP_R = V(0.99, 0, 0.22), GLOW = [1, 0.55, 0.25];
  api.part("RuneGolem", (fx, node, c, mat, nd) => {
    const cc = nd.comps.find(x => x.type === "CharacterController") || {}, ch = nd.comps.find(x => x.type === "CharacterControl") || {};
    const runSpeed = num(ch.runSpeed, 3.25) * num(ch.moveMod, 1);
    const height = () => Math.max(1, Math.max(num(cc.m_Height, 4.8), 2 * num(cc.m_Radius, 1.425)) * node.scale.y + 0.3);
    const to = vec(fx.at?.to, V(0, 0, 10)), end = num(fx.at?.end, 10), REACH = 3.4 + 0.3;
    let g = 0, dt = 0, state = "attack", command = "summon", live = true, ending = false, co = null;
    let nextAura = 0.7, nextQuake = 4, nextPound = 2.9 + 3, nextFist = 0, fistSide = 0, flareUntil = 0;
    let moveSpeed = 0, lastPhase = 0, runT = 0, clip = null, aegis = null, model, anim, glowMat = null, body;
    const fwd = () => FWD.clone().applyQuaternion(node.quaternion);
    const tp = p => { node.updateMatrix(); return p.clone().applyMatrix4(node.matrix); };   // Transform.TransformPoint
    const fxAt = (name, p, q = node.quaternion) => spawn(fx, name, p, q);
    const flare = s => { flareUntil = Math.max(flareUntil, g + s); };
    const once = (name, fade) => { if (!anim) return; if (clip === name) anim.rewind(); anim.play(name, fade, 8); clip = name; };
    const loop = name => { if (!anim) return; if (clip !== name) runT = 0; anim.play(name, 0.25, 2); clip = name; };
    const face = (at, snap) => {
      const d = flat(at.clone().sub(node.position));
      if (d.lengthSq() < 1e-4) return;
      const q = lookRot(d);
      if (snap) node.quaternion.copy(q); else node.quaternion.rotateTowards(q, 360 * DEG * dt);
    };
    const idle = () => {
      lastPhase = -1; state = "standby";
      moveSpeed += (0 - moveSpeed) * clamp01(6 * dt);
      if (moveSpeed < 0.1) moveSpeed = 0;
      loop("root");
    };
    const footfall = () => {
      const phase = clamp01((runT / 1.2) % 1);
      if (lastPhase >= 0) {
        if (phase < lastPhase) fxAt("runeGolem_step", tp(STEP_L));
        else if (lastPhase < 0.5 && phase >= 0.5) fxAt("runeGolem_step", tp(STEP_R));
      }
      lastPhase = phase;
    };
    const moveToward = at => {
      const d = flat(at.clone().sub(node.position));
      if (d.length() <= 1e-5) { idle(); return; }
      node.quaternion.rotateTowards(lookRot(d), 360 * DEG * dt);
      state = "run";
      moveSpeed += (runSpeed - moveSpeed) * clamp01(4 * dt);
      loop("run");
      footfall();
    };
    const setModelY = y => { if (model) model.position.set(0, y, 0); };
    // the coroutines (JS generators, one at a time: Rise, Fist, Quake, CrumbleAway; each yield = one frame)
    function* rise() {
      state = "attack"; command = "summon"; moveSpeed = 0;
      once("summon", 0); flare(2.9);
      fxAt("runeGolem_rise", node.position.clone());
      const h = height();
      while (g < 0.7 && live) { const u = 1 - g / 0.7; setModelY(-h * u * u * u); yield; }
      setModelY(0);
      if (!live) return;
      fxAt("runeGolem_riseBurst", node.position.clone());
      while (g < 2.05) yield;
      if (!live) return;
      fxAt("runeGolem_roar", tp(ROAR_AT));
      while (g < 2.9) yield;
      if (!live || command !== "summon") return;
      state = "standby"; command = "none";
    }
    function* fist(step, target) {
      face(target, true);
      once("attack" + (step + 1), 0.15);
      state = "attack"; command = "fist" + step;
      const t0 = g;
      while (g < t0 + FIST_HIT_AT[step]) yield;
      if (command === "fist" + step) {
        if (step === 2) fxAt("runeGolem_pound", tp(POUND_AT));
        else fxAt("runeGolem_fistHit", tp(step === 0 ? FIST_R : FIST_L));
      }
      while (g < t0 + FIST_LEN[step]) yield;
      if (command === "fist" + step) { state = "standby"; command = "none"; }   // Done@0x1D6A0F0
    }
    function* quake() {
      once("quake", 0.15); flare(1.6);
      state = "attack"; command = "quake";
      fxAt("runeGolem_quakeCharge", node.position.clone());
      const t0 = g;
      while (g < t0 + 0.78) yield;
      fxAt("runeGolem_quake", tp(QUAKE_AT));
      while (g < t0 + 1.6) yield;
      state = "standby"; command = "none";
    }
    function* crumbleAway() {
      once("collapse", 0.15);
      fxAt("runeGolem_crumble", node.position.clone());
      const t0 = g;
      while (g < t0 + 0.9) yield;
      fxAt("runeGolem_dust", node.position.clone(), new THREE.Quaternion());
      const t1 = g, h = height();
      while (g < t1 + 1.5) { const u = (g - t1) / 1.5; setModelY(-h * u * u); yield; }
      return "destroy";
    }
    const start = gen => { co = gen; return co.next().value; };
    const think = () => {
      const target = heroPoint(fx, to), owner = heroPoint(fx, V());
      const dist = flat(target.clone().sub(node.position)).length();
      if (dist > 14) {                                        // PickTarget: nothing within VisionRange
        if (flat(owner.clone().sub(node.position)).lengthSq() <= 36) idle(); else moveToward(owner);
        return;
      }
      if (g >= nextQuake && target.distanceTo(node.position) <= 7) {
        nextQuake = g + 12; face(target, true); start(quake()); return;
      }
      if (dist > REACH) { moveToward(target); return; }
      let step;
      if (g >= nextPound) { nextPound = g + 7; step = 2; nextFist = Math.max(nextFist, g + FIST_LEN[2]); }
      else if (g < nextFist) { idle(); face(target, false); return; }
      else { step = fistSide; fistSide = 1 - step; nextFist = g + 1.6; }
      face(target, true);
      start(fist(step, target));
    };
    const aura = () => {
      fxAt("runeGolem_auraPulse", node.position.clone(), new THREE.Quaternion());
      const owner = heroPoint(fx, V()), d = owner.clone().sub(node.position);
      if (flat(d).length() > 8 || Math.abs(d.y) > 4) return;
      if (!aegis?.alive) {
        aegis = api.spawn?.(prefixOf(fx) + "stoneAegis", {});
        if (!aegis) warnOnce("aegis", "stoneAegis not spawned (not in fx.json: the entry's builds)");
      }
      if (aegis) aegis.killAt = aegis.age + 3;                // AuraTime 3, renewed (one look while it lasts)
    };
    const glow = () => {
      if (!glowMat) return;
      const a0 = g < flareUntil ? 0.85 : 0.28 + 0.1 * Math.sin(2.4 * g), a = live ? a0 : Math.max(0, a0 - 0.6);
      // Particles/Additive: 2 x tint.rgb x 2 x tint.a; fxMaterial's "add" = colour x opacity (tto_mole.js's tint)
      const A = 2 * a, b = 2 * Math.max(1, A);
      glowMat.color.setRGB(GLOW[0] * b, GLOW[1] * b, GLOW[2] * b, THREE.SRGBColorSpace);
      glowMat.opacity = Math.min(1, A);
    };
    return { node, update(d) {
      dt = d;
      if (g === 0 && !co) {                                   // the first frame: every node is built (late look-ups)
        model = fx.nodes.find(o => o.name === "Model" && o.parent === node) || null;
        anim = node.userData.fxAnim || null;
        node.traverse(o => { if (!body && o.isSkinnedMesh) body = o; });
        if (body && Array.isArray(body.material) && body.material.length >= 2 && body.material[1]?.color) {
          const m0 = body.material[1], m = m0.clone();
          m.onBeforeCompile = m0.onBeforeCompile; m.customProgramCacheKey = m0.customProgramCacheKey; m.userData.fxBlend = m0.userData.fxBlend;
          body.material[1] = glowMat = m;
        }
        if (!anim) warnOnce("anim", fx.name, "RuneGolem: no Animation on its root");
        start(rise());
      }
      g += dt;
      if (live && g >= end) {                                 // unsummon -> Crumble(true)
        live = false; ending = true; state = "dead"; command = "none"; moveSpeed = 0;
        start(crumbleAway());
      }
      if (live) {                                             // Update
        if (g >= nextAura) { nextAura = g + 1.5; aura(); }
        if (state !== "attack" && !ending) think();
      }
      if (clip === "run") runT += dt;
      if (state === "run" || state === "standby") node.position.addScaledVector(fwd(), moveSpeed * dt);
      if (co) { const r = co.next(); if (r.done) { co = null; if (r.value === "destroy") return "destroy"; } }
      glow();                                                 // LateUpdate
    }, dispose() { glowMat?.dispose(); glowMat = null; } };
  });
}
