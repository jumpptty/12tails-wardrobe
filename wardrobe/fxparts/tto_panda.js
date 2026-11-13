// wardrobe/fxparts/tto_panda.js: what the Panda's TTO skills (Nine Dragons, Tempest Dance, Yin Yang Fist) draw that no
// other part does (2026-11-13; plans/fx_panda/parts.md T1-T4 and "Interfaces" 3-5, with parts.md's and tto.md's
// Verification sections, which win over the bodies; decisions.md 28, 29, 36, 54). TTO1102 = DecompiledSource_TTO_2026-11-02
// (dump.cs, methods.tsv, pseudo/Panda.c, client/GameAssembly.dll disassembled at the RVAs given).
//
//   HelixRibbonEmitter       TTO.Game TypeDefIndex 411 (tempestDance_aura / _end / _pulse, yinYang, yinYangFist_charge /
//                            _seal: 9 instances)
//   Panda.NineDragon         <NineDragon>d__336 (nineDragons_dragon x 8: put on the root by wardrobe_fx_tto.py CODE_MOVERS)
//   Panda.NineKing           <NineKing>d__339 (nineDragons_king, the same)
//   fx:tto/tempestDance_trails  Panda::TempestTrails (the hero's code: the four limb trails on her bones)
//   shaders                  ERB/Particles/Add_CenterGlow, ERB/Particles/Blend_CenterGlow, Particles/Standard Surface
//                            (yinYangFist_burst): page materials through api.shader
//
// Space: everything in the effect's Unity world (the mirror group's space: the hero's feet at the origin, +z her facing,
// y 0 the floor). Cue words read here (fx.at): k, to (the movers), off (the trails); x / y / d / rot / kill are the page's.
export default function register(api) {
  const { THREE, V } = api;
  const DEG = Math.PI / 180, UP = V(0, 1, 0);
  const clamp01 = x => (x < 0 ? 0 : x > 1 ? 1 : x);
  const num = (x, d = 0) => (x !== null && x !== "" && x !== undefined && Number.isFinite(+x) ? +x : d);
  const bool = x => x === true || x === 1 || x === "True" || x === "true";
  const toLin = c => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
  const col4 = (c, d = [1, 1, 1, 1]) => (Array.isArray(c) && c.length >= 3 ? [num(c[0]), num(c[1]), num(c[2]), num(c[3], 1)] : d);
  const lerp = (a, b, t) => a + (b - a) * t;
  // a node's matrix in the effect's Unity world, fresh (a part may have just moved it; fx.mirrorInv is set after the build)
  const uMat = (fx, o) => { o.updateWorldMatrix(true, false); return fx.mirror.matrixWorld.clone().invert().multiply(o.matrixWorld); };
  const worldPos = (fx, o) => V().setFromMatrixPosition(uMat(fx, o));
  // Transform.position = w (a Unity-world point back through the node's parent)
  const setWorldPos = (fx, o, w) => {
    if (o.parent === fx.mirror) o.position.copy(w);
    else o.position.copy(w.clone().applyMatrix4(uMat(fx, o.parent).invert()));
  };
  // Quaternion.LookRotation(f, Vector3.up) in Unity's numbers (Cross is the same formula in either hand)
  const lookRot = (f, q = new THREE.Quaternion()) => {
    const z = f.clone().normalize(), x = V().crossVectors(UP, z);
    if (x.lengthSq() < 1e-12) x.set(1, 0, 0); x.normalize();
    return q.setFromRotationMatrix(new THREE.Matrix4().makeBasis(x, V().crossVectors(z, x), z));
  };
  const target = fx => (Array.isArray(fx.at?.to) ? V(num(fx.at.to[0]), num(fx.at.to[1]), num(fx.at.to[2])) : null);
  const warned = {};
  const warnOnce = (k, ...m) => { if (!warned[k]) { warned[k] = true; console.warn(...m); } };

  // ---------------------------------------------------------------- HelixRibbonEmitter (parts.md T1)
  // Fields (dump.cs:11764-11810; .ctor@0x2265660 defaults): ribbons 3, turns 1, height 2, radiusBottom 0.6, radiusTop 1.2,
  // widthBottom 0.2, widthTop 0.4, segments 40, spin -360 (deg/s), scroll 1, uvTile 2, wobble 0, wobbleSpeed 3, Life 1,
  // Delay 0, fadeIn 0.2, fadeOut 0.3, repeatForever, radiusScaleStart / End 1, colorBottom / colorTop white, endFade 0.2.
  // - Awake@0x2264a90: a dynamic Mesh on its MeshFilter, ribbons x (segments + 1) x 2 vertices, triangles for ribbon r
  //   (base b = r (2 segments + 2)), segment s (i = b + 2 s): (i, i + 2, i + 1), (i + 1, i + 2, i + 3); startTime =
  //   Time.time; phaseOffset = Random.Range(0, 360); Rebuild(0, 0).
  // - LateUpdate@0x2264ef0: t = time - startTime - Delay; t < 0, or (!repeatForever and t > Life): renderer off, nothing
  //   else; else renderer on, a = fadeIn > 0 ? clamp01(t / fadeIn) : 1, x clamp01((Life - t) / fadeOut) when
  //   !repeatForever and fadeOut > 0; Rebuild(t, a).
  // - Ends(s, f)@0x2264e00: f <= 0 -> 1, else sm(clamp01(s / f)) x sm(clamp01((1 - s) / f)), sm(x) = 3x^2 - 2x^3.
  // - Rebuild(t, a)@0x2265090: k = (!repeatForever && Life > 0) ? clamp01(t / Life) : 0; rs = lerp(radiusScaleStart,
  //   radiusScaleEnd, k); M = (1 + wobble sin(t wobbleSpeed)) rs; flat = height <= 0.001; phase = t spin + phaseOffset
  //   (deg); uShift = t scroll; ribbon r: a0 = 360 r / ribbons + phase (deg); point s = 0..segments: u = s / segments,
  //   th = turns 2 pi u + a0 (rad), R = lerp(radiusBottom, radiusTop, u) M, W = lerp(widthBottom, widthTop, u),
  //   p = (R cos th, u height, R sin th) (the node's space), side = flat ? (cos th, 0, sin th) : up; vertices p -/+ side
  //   W / 2, uv (u uvTile - uShift, 0 / 1), colour lerp(colorBottom, colorTop, u) with alpha x Ends(u, endFade) x a.
  // On the page: the mesh on the node (api.fxMesh, the node's own material: addsoft windRibbon / inkStroke), so the node's
  // transform (and the effect's following) carries it, as Unity's MeshFilter. Colours lerped in the game's (gamma) values,
  // then made linear as the page's vertex colours are (trail.js's lin). The clock: the emitter's own from its build (the
  // node's age = Time.time - startTime). No stop(): TTO's EffectControl reaches only ParticleSystems, Image- and
  // RingEmitters (groundhug.js's note), so a repeatForever helix runs on to its effect's end, as in the game
  api.part("HelixRibbonEmitter", (fx, node, e, mat, nd) => {
    if (!mat || e.enabled === false || nd.active === false) return null;
    const F = {
      ribbons: Math.max(1, Math.round(num(e.ribbons, 3))), turns: num(e.turns, 1), height: num(e.height, 2),
      rB: num(e.radiusBottom, 0.6), rT: num(e.radiusTop, 1.2), wB: num(e.widthBottom, 0.2), wT: num(e.widthTop, 0.4),
      segments: Math.max(1, Math.round(num(e.segments, 40))), spin: num(e.spin, -360), scroll: num(e.scroll, 1),
      uvTile: num(e.uvTile, 2), wobble: num(e.wobble, 0), wobbleSpeed: num(e.wobbleSpeed, 3), Life: num(e.Life, 1),
      Delay: num(e.Delay, 0), fadeIn: num(e.fadeIn, 0.2), fadeOut: num(e.fadeOut, 0.3), loop: bool(e.repeatForever),
      rsS: num(e.radiusScaleStart, 1), rsE: num(e.radiusScaleEnd, 1), cB: col4(e.colorBottom), cT: col4(e.colorTop),
      endFade: num(e.endFade, 0.2),
    };
    const m = api.fxMesh(node, mat), S = F.segments, R = F.ribbons, idx = [];
    for (let r = 0; r < R; r++) for (let s = 0; s < S; s++) {
      const i = r * (2 * S + 2) + 2 * s;
      idx.push(i, i + 2, i + 1, i + 1, i + 2, i + 3);
    }
    const phaseOffset = Math.random() * 360;
    const sm = x => x * x * (3 - 2 * x);
    const ends = (s, f) => (f <= 0 ? 1 : sm(clamp01(s / f)) * sm(clamp01((1 - s) / f)));
    const rebuild = (t, a) => {
      const k = !F.loop && F.Life > 0 ? clamp01(t / F.Life) : 0, rs = lerp(F.rsS, F.rsE, k);
      const M = (1 + F.wobble * Math.sin(t * F.wobbleSpeed)) * rs, flat = F.height <= 0.001;
      const phase = t * F.spin + phaseOffset, uShift = t * F.scroll;
      const pos = [], col = [], uv = [];
      for (let r = 0; r < R; r++) {
        const a0 = 360 * r / R + phase;
        for (let s = 0; s <= S; s++) {
          const u = s / S, th = F.turns * 2 * Math.PI * u + a0 * DEG, ct = Math.cos(th), st = Math.sin(th);
          const rad = lerp(F.rB, F.rT, u) * M, hw = lerp(F.wB, F.wT, u) / 2;
          const px = rad * ct, py = u * F.height, pz = rad * st;
          const sx = flat ? ct : 0, sy = flat ? 0 : 1, sz = flat ? st : 0;
          pos.push(px - sx * hw, py - sy * hw, pz - sz * hw, px + sx * hw, py + sy * hw, pz + sz * hw);
          const U = u * F.uvTile - uShift;
          uv.push(U, 0, U, 1);
          const c = [0, 1, 2].map(j => toLin(lerp(F.cB[j], F.cT[j], u)));
          c.push(lerp(F.cB[3], F.cT[3], u) * ends(u, F.endFade) * a);
          col.push(...c, ...c);
        }
      }
      api.setMesh(m, pos, col, uv, idx);
    };
    let age = 0;
    m.visible = false;                                       // Awake's Rebuild(0, 0) draws nothing (alpha 0)
    return { node, update(dt) {
      age += dt;
      const t = age - F.Delay;
      if (t < 0 || (!F.loop && t > F.Life)) { m.visible = false; return; }
      m.visible = true;
      let a = F.fadeIn > 0 ? clamp01(t / F.fadeIn) : 1;
      if (!F.loop && F.fadeOut > 0) a *= clamp01((F.Life - t) / F.fadeOut);
      rebuild(t, a);
    } };
  });

  // ---------------------------------------------------------------- NineVanish (Panda::NineVanish@0x1D55070)
  // its children Body, HeadGlow, HeadHalo SetActive(false) (0x1D5520B), every ParticleSystem under it Stop(StopEmitting)
  // (the trail keeps fading out), Destroy(gameObject, 0.5). The nodes and emitters looked up now, when it is due (they are
  // built after the root's first component, the mover)
  const VANISH = new Set(["Body", "HeadGlow", "HeadHalo"]);
  const vanish = (fx, root, data) => {
    for (const o of fx.nodes) if (o.parent === root && VANISH.has(o.name)) o.visible = false;
    const def = data?.effects?.[fx.name]?.nodes || [];
    const ps = new Set(fx.nodes.filter((o, i) => def[i]?.comps?.some(c => c.type === "ParticleSystem")));
    for (const e of fx.emitters) if (ps.has(e.node)) e.stop?.();
  };
  // NineFly(d, last, p)@0x1D53F80: position p, rotation LookRotation(p - last) when it moved
  const fly = (fx, node, p, q) => {
    const d = p.clone().sub(worldPos(fx, node));
    if (d.lengthSq() > 1e-10) node.quaternion.copy(lookRot(d, q));
    setWorldPos(fx, node, p);
  };

  // ---------------------------------------------------------------- Panda.NineDragon (parts.md T2, tto.md Verification 2)
  // <NineDragon>d__336::MoveNext@0x1D6F860 (pseudo/Panda.c:75-401): from = the hand (the cue's spawn spot: tto.md's fk
  // table, rot = LookRotation(c1 - from) already applied by the page); fwd = Row6Fwd (the hero's flat forward: +z);
  // side = Cross(up, fwd) = +x for even k, -x for odd; end = NineAim (the prey + 0.6 up: the cue's `to`); flight =
  // clamp(1.6 |from - end| / 22, 0.35, 0.7); c1 = from + 1.4 fwd + (1.3 + 0.15 (k % 4)) side + (2.2 + 0.2 (k % 3)) up;
  // each frame while time < t0 + flight: c2 = end + 0.6 side + 2.4 up, p = Bezier(from, c1, c2, end, (time - t0) /
  // flight) (Panda::Bezier@0x1D51F00, the cubic), NineFly; then NineFly(end) and NineVanish. The bite, its punch sound and
  // the hit are cues (decision 29). `end` homes on a moving prey in the game; the page's stands still. APPROX: no `to` on
  // the cue (the game always has its prey or a fallback) = 10 m ahead, 0.6 up
  const bez = (a, b, c, d, t) => {
    const s = 1 - t;
    return a.clone().multiplyScalar(s * s * s).addScaledVector(b, 3 * s * s * t).addScaledVector(c, 3 * s * t * t).addScaledVector(d, t * t * t);
  };
  api.part("Panda.NineDragon", (fx, node, c, mat, nd, data) => {
    const k = Math.max(0, Math.round(num(fx.at?.k, 0)));
    const from = worldPos(fx, node), end = target(fx) || V(0, 0.6, 10), fwd = V(0, 0, 1);
    const side = V().crossVectors(UP, fwd).multiplyScalar(k % 2 ? -1 : 1);
    const flight = Math.min(0.7, Math.max(0.35, 1.6 * from.distanceTo(end) / 22));
    const c1 = from.clone().addScaledVector(fwd, 1.4).addScaledVector(side, 1.3 + 0.15 * (k % 4)).addScaledVector(UP, 2.2 + 0.2 * (k % 3));
    const q = new THREE.Quaternion();
    let age = 0, gone = null;
    return { node, update(dt) {
      age += dt;
      if (gone != null) return age >= gone ? "destroy" : undefined;     // Destroy(gameObject, 0.5) (the cue's kill too)
      if (age < flight) {
        const c2 = end.clone().addScaledVector(side, 0.6).addScaledVector(UP, 2.4);
        fly(fx, node, bez(from, c1, c2, end, age / flight), q);
        return;
      }
      fly(fx, node, end, q); vanish(fx, node, data); gone = age + 0.5;
    } };
  });

  // ---------------------------------------------------------------- Panda.NineKing (parts.md T2, tto.md Verification 2)
  // <NineKing>d__339::MoveNext@0x1D701C0 (pseudo/Panda.c:405-765, disasm_NineKing.txt): from = hero + 0.7 up + 0.4 fwd
  // (the cue's spawn spot); end = NineMark (the target's ground point: the cue's `to`); aim = end + 0.8 up; dir =
  // vFlat(aim - from) normalised (fwd when shorter than 0.01); side = Cross(up, dir); spawned LookRotation(dir). For 0.4 s,
  // u = (time - t0) / 0.4: p = lerp(from, aim, clamp01(u)) + 0.9 (1 - u) sin(2 pi u) side + 0.6 sin(pi u) up (the second
  // sin's argument u x pi read at 0x1D7088F), NineFly; then NineFly(aim) and NineVanish. kingRise, the strikes and the fall
  // are cues (decision 29). APPROX: no `to` on the cue = the ground 10 m ahead
  api.part("Panda.NineKing", (fx, node, c, mat, nd, data) => {
    const from = worldPos(fx, node), aim = (target(fx) || V(0, 0, 10)).add(V(0, 0.8, 0));
    const dir = V(aim.x - from.x, 0, aim.z - from.z);
    if (dir.length() < 0.01) dir.set(0, 0, 1); else dir.normalize();
    const side = V().crossVectors(UP, dir), q = new THREE.Quaternion();
    node.quaternion.copy(lookRot(dir, q));
    let age = 0, gone = null;
    return { node, update(dt) {
      age += dt;
      if (gone != null) return age >= gone ? "destroy" : undefined;
      const u = age / 0.4;
      if (u < 1) {
        const p = from.clone().lerp(aim, clamp01(u)).addScaledVector(side, 0.9 * (1 - u) * Math.sin(2 * Math.PI * u)).addScaledVector(UP, 0.6 * Math.sin(Math.PI * u));
        fly(fx, node, p, q);
        return;
      }
      fly(fx, node, aim, q); vanish(fx, node, data); gone = age + 0.5;
    } };
  });

  // ---------------------------------------------------------------- fx:tto/tempestDance_trails (parts.md T3, Interfaces 4-5)
  // Panda::TempestTrails@0x1D5F010 (pseudo/Panda.c:43467-43706): TempestTrails(true) instantiates each child of the prefab
  // (Hand_R, Hand_L, Foot_R, Foot_L: TrailRenderers of 0.3 / 0.3 / 0.38 / 0.38 s) under the hero's bone of its name,
  // localPosition 0, localRotation identity, Clear(); TempestTrails(false) (0.75 s into Tempest Dance End, :23442) sets each
  // trail's emitting false and Destroys it trail.time + 0.05 later (the cue's kill). On the page the children stay under
  // the effect's root and each frame take the bone's transform: local = root^-1 x api.boneMatrix(name, fx); the cue's `off`
  // (seconds after the spawn) calls emitOff() on each child's TrailRendererModern (fxparts/tto_sheep.js). The placer is put
  // at the head of fx.emitters, so each frame the nodes are on their bones before the trails sample them (no lag); a bone
  // the hero lacks leaves its node at the root (the hero's feet)
  api.part("fx:tto/tempestDance_trails", fx => {
    if (!api.boneMatrix) warnOnce("bm", "tto_panda: api.boneMatrix missing (index.html), the Tempest Dance trails stay at her feet");
    const root = fx.root || fx.nodes[0], off = fx.at?.off != null ? num(fx.at.off, Infinity) : Infinity;
    let age = 0, stopped = false;
    const place = {
      node: root,
      update(dt) {
        age += dt;
        const kids = fx.nodes.filter(o => o.parent === root);
        if (api.boneMatrix) {
          const inv = uMat(fx, root).invert();
          for (const o of kids) {
            const b = api.boneMatrix(o.name, fx);
            if (b) { inv.clone().multiply(b).decompose(o.position, o.quaternion, o.scale); o.updateMatrixWorld(true); }
          }
        }
        if (!stopped && age >= off) {
          stopped = true;
          for (const e of fx.emitters) if (kids.includes(e.node)) e.emitOff?.();
        }
      },
    };
    fx.emitters.unshift(place);                              // first in the frame (the constructor pushes a returned one last)
    return null;
  });

  // ---------------------------------------------------------------- shaders (parts.md T4)
  // Pass state from the bundles' parsed shader form (tto_mat_probe.json); the programs are not decoded (APPROX: the
  // fragment from the property set, as tto_monkey.js's Eric/URP shaders). In every Panda material _Usecenterglow 0,
  // _Usedepth 0 (no mask, no soft depth), _Flow empty, _SpeedMainTexUVNoiseZW (0, 0, 0, 0); so
  //   Add_CenterGlow (Blend One One, ZWrite Off, Cull _CullMode): rgb = main x noise x _Color x vertex colour x _Emission
  //     x alpha, alpha = main.a x noise.a x _Color.a x vertex alpha, added;
  //   Blend_CenterGlow (Blend SrcAlpha OneMinusSrcAlpha, ZWrite Off, Cull Off): the same colour, alpha x _Opacity, clamped.
  // uv = uv0 x _MainTex_ST + _Time.y x speed.xy; the noise's uv0 x _Noise_ST + _Time.y x speed.zw. _Noise = the material's
  // noiseTex / noiseScale / noiseOffset (wardrobe_fx_tto.py's material(), as tto_chameleon.js's scaleTex), white when
  // absent. The products in gamma (TTO's convention, tto_monkey.js), clamped to 0..1 as the game's 8-bit target, made
  // linear for the output; the additive one writes the page's additive convention (premultiplied, canvas alpha = its
  // brightest channel, index.html fxMaterial). _CullMode: 0 Off, 1 Front, 2 Back (inside the mirror group three's
  // FrontSide keeps Unity's front faces). The clock: the page's (APPROX: only the scroll's phase; every speed here is 0)
  const time = { get value() { return performance.now() / 1000; } };
  const texs = {};
  const tex = (n, srgb = true) => {
    if (!n || !api.texLoader) return null;
    const k = n + (srgb ? "" : "|raw");
    if (!texs[k]) {
      const t = texs[k] = api.texLoader.load(`${api.DATA}fx/tex/${n}.webp`);
      t.colorSpace = srgb ? THREE.SRGBColorSpace : THREE.NoColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping;
    }
    return texs[k];
  };
  const ERB_VERT = `
    uniform vec4 uST, uNST, uSpeed; uniform float uTime;
    varying vec4 vC; varying vec2 vUv; varying vec2 vNuv;
    void main() {
    #ifdef USE_COLOR_ALPHA
      vC = color;
    #elif defined(USE_COLOR)
      vC = vec4(color, 1.0);
    #else
      vC = vec4(1.0);
    #endif
      vUv = uv * uST.xy + uST.zw + uSpeed.xy * uTime;
      vNuv = uv * uNST.xy + uNST.zw + uSpeed.zw * uTime;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }`;
  const ERB_FRAG = alpha => `
    uniform sampler2D map, nmap; uniform float uHasMap, uHasN, uE, uOp; uniform vec4 uColor;
    varying vec4 vC; varying vec2 vUv; varying vec2 vNuv;
    vec3 lin3(vec3 c) { return mix(c / 12.92, pow((c + 0.055) / 1.055, vec3(2.4)), step(vec3(0.04045), c)); }
    vec3 gam3(vec3 c) { c = max(c, 0.0); return mix(c * 12.92, 1.055 * pow(c, vec3(1.0 / 2.4)) - 0.055, step(vec3(0.0031308), c)); }
    void main() {
      vec4 t = uHasMap > 0.5 ? texture2D(map, vUv) : vec4(1.0);
      vec4 n = uHasN > 0.5 ? texture2D(nmap, vNuv) : vec4(1.0);
      vec3 g = clamp(gam3(t.rgb * n.rgb * vC.rgb) * uColor.rgb * uE, 0.0, 1.0);
      float a = clamp(t.a * n.a * vC.a * uColor.a * uOp, 0.0, 1.0);
      vec4 o = linearToOutputTexel(vec4(lin3(g), 1.0));
      ${alpha ? "gl_FragColor = vec4(o.rgb, a);" : "o.rgb *= a; gl_FragColor = vec4(o.rgb, max(o.r, max(o.g, o.b)));"}
    }`;
  const erb = alpha => d => {
    const p = d.props || {}, c = col4(p._Color || d.color), s = p._SpeedMainTexUVNoiseZW || [0, 0, 0, 0];
    const cull = alpha ? 0 : num(p._CullMode), mt = tex(d.tex), nt = tex(d.noiseTex);
    return new THREE.ShaderMaterial({
      vertexShader: ERB_VERT, fragmentShader: ERB_FRAG(alpha), vertexColors: true, transparent: true, depthWrite: false,
      side: cull === 2 ? THREE.FrontSide : cull === 1 ? THREE.BackSide : THREE.DoubleSide,
      blending: alpha ? THREE.NormalBlending : THREE.CustomBlending,
      ...(alpha ? {} : { blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor, blendSrcAlpha: THREE.OneFactor, blendDstAlpha: THREE.OneMinusSrcAlphaFactor }),
      uniforms: { map: { value: mt }, uHasMap: { value: mt ? 1 : 0 }, nmap: { value: nt }, uHasN: { value: nt ? 1 : 0 },
        uColor: { value: new THREE.Vector4(...c) }, uE: { value: num(p._Emission, 1) }, uOp: { value: alpha ? num(p._Opacity, 1) : 1 },
        uST: { value: new THREE.Vector4(...(d.scale || [1, 1]), ...(d.offset || [0, 0])) },
        uNST: { value: new THREE.Vector4(...(d.noiseScale || [1, 1]), ...(d.noiseOffset || [0, 0])) },
        uSpeed: { value: new THREE.Vector4(...[0, 1, 2, 3].map(i => num(s[i]))) }, uTime: time },
    });
  };
  if (!api.shader) console.warn("tto_panda: api.shader missing (index.html), the ERB / Standard Surface shaders draw as plain alpha");
  api.shader?.("shader:ERB/Particles/Add_CenterGlow", erb(false));
  api.shader?.("shader:ERB/Particles/Blend_CenterGlow", erb(true));

  // Particles/Standard Surface (Unity's lit particle shader: tto_pandaRow6_bamboo / _bambooLeaf _Mode 1 Cutout, _Cutoff
  // 0.124 / 0.5, ZWrite On, _EmissionEnabled 1 with _EmissionColor 0.12 / 0.15; _smokePuff / _smokeWisp _Mode 2 Fade,
  // _SrcBlend 5 / _DstBlend 10, ZWrite Off; all _Cull 0): three's MeshStandardMaterial with vertex colours, color =
  // _Color, map = _MainTex (its ST), metalness _Metallic, roughness 1 - _Glossiness; Cutout -> alphaTest _Cutoff; Fade and
  // the blended modes -> transparent with _SrcBlend / _DstBlend (tto_sheep.js's BF table); emissive = _EmissionColor
  // with emissiveMap = the albedo when _EmissionEnabled (parts.md T4). Lit by the page's scene lights. APPROX: the
  // bamboo's _BumpMap (normal map) is not drawn (not exported, parts.md Q6); flat shading (the face normal from the screen
  // derivatives, always toward the camera): the billboard smoke has no normals (shuriken.js sends normals only for mesh
  // particles), and a lit billboard faces the camera in Unity too; the bamboo / leaf meshes light by their faces, not
  // their smooth normals; Unity's sky reflections are not drawn
  const BF = [THREE.ZeroFactor, THREE.OneFactor, THREE.DstColorFactor, THREE.SrcColorFactor, THREE.OneMinusDstColorFactor,
    THREE.SrcAlphaFactor, THREE.OneMinusSrcColorFactor, THREE.DstAlphaFactor, THREE.OneMinusDstAlphaFactor,
    THREE.SrcAlphaSaturateFactor, THREE.OneMinusSrcAlphaFactor];
  api.shader?.("shader:Particles/Standard Surface", d => {
    const p = d.props || {}, c = col4(p._Color || d.color), mode = num(p._Mode), cull = num(p._Cull);
    const m = new THREE.MeshStandardMaterial({ vertexColors: true, flatShading: true, metalness: num(p._Metallic), roughness: 1 - num(p._Glossiness, 0.5),
      side: cull === 2 ? THREE.FrontSide : cull === 1 ? THREE.BackSide : THREE.DoubleSide });
    m.color.setRGB(c[0], c[1], c[2], THREE.SRGBColorSpace);
    if (mode === 1) { m.alphaTest = num(p._Cutoff, 0.5); m.depthWrite = true; }
    else if (mode >= 2) {
      Object.assign(m, { transparent: true, depthWrite: !!num(p._ZWrite), opacity: Math.min(1, c[3]), blending: THREE.CustomBlending,
        blendSrc: BF[num(p._SrcBlend, 5)] ?? THREE.SrcAlphaFactor, blendDst: BF[num(p._DstBlend, 10)] ?? THREE.OneMinusSrcAlphaFactor,
        blendSrcAlpha: THREE.OneFactor, blendDstAlpha: THREE.OneMinusSrcAlphaFactor });
    }
    const t = d.tex ? api.texLoader.load(`${api.DATA}fx/tex/${d.tex}.webp`) : null;   // its own copy: its own ST
    if (t) {
      t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping;
      t.repeat.fromArray(d.scale || [1, 1]); t.offset.fromArray(d.offset || [0, 0]);
      m.map = t;
    }
    if (num(p._EmissionEnabled)) {
      const e = col4(p._EmissionColor, [0, 0, 0, 1]);
      m.emissive.setRGB(e[0], e[1], e[2], THREE.SRGBColorSpace);
      if (t) m.emissiveMap = t;
    }
    return m;
  });
}
