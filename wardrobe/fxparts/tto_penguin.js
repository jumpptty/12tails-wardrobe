// wardrobe/fxparts/tto_penguin.js: what the Penguin's TTO skills (Constellation, Frost Field, Emperor's March) draw that
// no other part does (2026-11-10, plans/fx_penguin/tto.md section 6 and "Built 2026-11-10"). TTO1102 =
// DecompiledSource_TTO_2026-11-02 (client/GameAssembly.dll), read in its pseudo-C (pseudo/Penguin.c, cited by line);
// TTO's shader disassembled from its D3D11 bytecode (checks/fx_penguin_build/tto/dxbc_cel.txt, cel_parsed.json:
// Windows' D3DDisassemble over the Shader's compressedBlob, as plans/fx_sheep/probes/build/tto/shader_dxbc.py).
//
//   shader               FlexibleCelShader/Cel No Outline (the flock's ice penguins, material tto_SmallIcePenguin):
//                        a page material through api.shader, skinned by mesh.js's SkinnedMeshRenderer
//   Penguin.StarLines    Constellation's lines (constellation_line's two LineRenderers), the coroutine
//                        <StarLines>d__341 put on the line's root by wardrobe_fx_tto.py CODE_MOVERS
//   Penguin.EmperorShot  Emperor's March's ball: its drop (<RPC_emperorPenguin>d__356 state 3-4) and roll (<EmperorShot>d__358)
//   Penguin.FlockRise    the flock's penguins: their rise (<FlockRise>d__357) and whirl after the ball (EmperorShot's flock)
//
// Cue options read (fx.at = the cue as index.html's cueOf keeps it): `at` (the cue's clip time: the coroutines' clock is
// the clip's, so a part's time = at + its age), `to` ([x, y, d], metres right / up / ahead of the hero: the line's end =
// the next star's mark; the ball's Goal, whose distance ahead sets the reach), `ignite` (the line: seconds after its
// spawn when it widens; without it kill - 0.6, the game's ClearStarFx always coming 0.6 s after the ignite), `i` / `n`
// (a penguin's index and the flock size; without them the index is read from where the cue put it, n = 5). Space:
// the effect's Unity world (the mirror group's space): the hero's feet at the origin, facing +z (Row6Begin turns the
// Penguin to the skill's direction, Penguin.c:41406, so the game's dir is the hero's forward), the page's floor at y 0.
export default function register(api) {
  const { THREE, V } = api;
  const clamp01 = x => (x < 0 ? 0 : x > 1 ? 1 : x);
  const DEG = Math.PI / 180;
  const UP = V(0, 1, 0), FWD = V(0, 0, 1), RIGHT = V(1, 0, 0);
  // a node's matrix in the effect's Unity world, fresh (a part may have just moved it)
  const uMat = (fx, o) => { o.updateWorldMatrix(true, false); return fx.mirror.matrixWorld.clone().invert().multiply(o.matrixWorld); };
  const worldPos = (fx, o) => V().setFromMatrixPosition(uMat(fx, o));
  const setPos = (fx, o, w) => {                       // Transform.set_position (every node moved here hangs on the mirror)
    if (o.parent === fx.mirror) o.position.copy(w);
    else o.position.copy(w.clone().applyMatrix4(uMat(fx, o.parent).invert()));
    o.updateMatrixWorld(true);
  };
  const camPos = fx => api.camera.getWorldPosition(V()).applyMatrix4(fx.mirror.matrixWorld.clone().invert());
  // Quaternion.LookRotation(forward, Vector3.up) in Unity's numbers (as tto_sheep.js)
  const lookRot = (f, q = new THREE.Quaternion()) => {
    const z = f.clone().normalize(), x = V().crossVectors(UP, z);
    if (x.lengthSq() < 1e-12) x.set(1, 0, 0); x.normalize();
    return q.setFromRotationMatrix(new THREE.Matrix4().makeBasis(x, V().crossVectors(z, x), z));
  };
  const cueTo = fx => (Array.isArray(fx.at?.to) ? V(fx.at.to[0], fx.at.to[1], fx.at.to[2]) : null);
  const cueAt = (fx, d) => (typeof fx.at?.at === "number" ? fx.at.at : d);

  // ---------------------------------------------------------------- FlexibleCelShader/Cel No Outline
  // The shader (cel_parsed.json: Queue Geometry, RenderType Opaque; FORWARD Blend One Zero, FORWARD_DELTA One One, a
  // shadow caster; Cull Back, ZWrite On) is a surface shader with TTO's own lighting. Its FORWARD fragment program for
  // DIRECTIONAL LIGHTPROBE_SH (dxbc_cel.txt program 33; $Globals: _LightColor0 cb0[2], _Color [4], _MainTex_ST [5],
  // _NormalTex_ST [6], _EmmisTex_ST [7], _RampLevels [8].x, _LightScalar [8].y, _HighIntensity [8].z, _HighColor [9],
  // _LowIntensity [10].x, _LowColor [11], _RimPower [12].x, _RimAlpha [12].y, _RimColor [13], _RimDropOff [14].x,
  // _FresnelBrightness [14].y, _FresnelPower [14].z, _FresnelColor [15], _FresnelShadowDropoff [16].x, _SceneLighting
  // [16].y, _TTOCelSceneLightCut [16].z):
  //   N = the normal map's normal in the tangent frame (no _NormalTex on this material: Unity's flat "bump", N = the
  //   vertex normal); levels = max(round(_RampLevels) - 1, 1); band = round(sat(dot(N, L) x _LightScalar) x levels) /
  //   levels (2 levels: lit 1 / unlit 0, the step at dot 0.5);
  //   scene = 1 + _SceneLighting (1 - _TTOCelSceneLightCut) (min((_LightColor0 band + SH) / (0.65 band + 0.42), 1.8) - 1),
  //   per channel (TTO's light normalisation: the map's light over what the shader expects);
  //   base = _MainTex x _Color x lerp(_LowColor x _LowIntensity, _HighColor x _HighIntensity, band) x 0.5;
  //   colour = base x scene + fresnel (10 _FresnelBrightness (1 - N.V)^(10 (1 - _FresnelPower)) x _FresnelColor x ...)
  //   and a hard rim where N.V <= _RimPower mixed by _RimAlpha; then lerp to _EmmisTex by its brightest channel.
  // tto_SmallIcePenguin: _RampLevels 2, _LightScalar 1, _HighIntensity 1.5, _LowIntensity 1, white colours,
  // _FresnelBrightness 0, _RimAlpha 0 (no fresnel, no rim), no _EmmisTex (default black: no emission), _SceneLighting 1,
  // _TTOCelSceneLightCut unset (a global, 0). So: texture x 0.75 lit, x 0.5 unlit, times the scene factor; opaque.
  // On the page: L = the page's sun (its first DirectionalLight), _LightColor0 and SH = the sun's colour and the sky's
  // (HemisphereLight + ambient) irradiance at N as three's Lambert receives them (x 1/pi). The game's arithmetic is on
  // gamma values (the convention of every TTO material here, tto_sheep.js): the factor's product is taken in gamma and
  // made linear before it multiplies the (linear) texture, exact for a pure 2.2 power curve.
  // APPROXIMATED: the page's lights stand in for the map's; no shadows (this variant reads none), no fog
  if (!api.shader) console.warn("tto_penguin: api.shader missing (index.html), the cel penguins draw as plain alpha");
  const CEL_VERT = `
    #include <common>
    #include <skinning_pars_vertex>
    uniform vec4 uST;
    varying vec2 vUv; varying vec3 vN;
    void main() {
      vUv = uv * uST.xy + uST.zw;
      #include <beginnormal_vertex>
      #include <skinbase_vertex>
      #include <skinnormal_vertex>
      #include <defaultnormal_vertex>
      vN = transformedNormal;
      #include <begin_vertex>
      #include <skinning_vertex>
      #include <project_vertex>
    }`;
  const CEL_FRAG = `
    #include <common>
    #include <lights_pars_begin>
    uniform sampler2D map; uniform float uHasMap;
    uniform vec4 uColor, uHigh, uLow;
    uniform float uRamp, uLightScalar, uHI, uLI, uScene, uCut;
    varying vec2 vUv; varying vec3 vN;
    vec3 lin3(vec3 c) { return mix(c / 12.92, pow((c + 0.055) / 1.055, vec3(2.4)), step(vec3(0.04045), c)); }
    void main() {
      vec3 N = normalize(vN);
      float ndl = 0.0; vec3 lc = vec3(0.0);
      #if NUM_DIR_LIGHTS > 0
        ndl = dot(N, directionalLights[0].direction); lc = directionalLights[0].color;
      #endif
      vec3 sh = ambientLightColor;
      #if NUM_HEMI_LIGHTS > 0
        for (int i = 0; i < NUM_HEMI_LIGHTS; i++) sh += getHemisphereLightIrradiance(hemisphereLights[i], N);
      #endif
      lc *= RECIPROCAL_PI; sh *= RECIPROCAL_PI;
      float levels = max(floor(uRamp + 0.5) - 1.0, 1.0);
      float band = floor(clamp(ndl * uLightScalar, 0.0, 1.0) * levels + 0.5) / levels;
      vec3 scene = 1.0 + uScene * (1.0 - uCut) * (min((lc * band + sh) / (band * 0.65 + 0.42), vec3(1.8)) - 1.0);
      vec3 k = uColor.rgb * mix(uLow.rgb * uLI, uHigh.rgb * uHI, band) * 0.5 * scene;
      vec3 tex = uHasMap > 0.5 ? texture2D(map, vUv).rgb : vec3(1.0);
      gl_FragColor = linearToOutputTexel(vec4(tex * lin3(max(k, 0.0)), 1.0));
    }`;
  api.shader?.("shader:FlexibleCelShader/Cel No Outline", d => {
    const p = d.props || {}, c4 = x => new THREE.Vector4(...(x || [1, 1, 1, 1]));
    const u = THREE.UniformsUtils.merge([THREE.UniformsLib.lights, {
      map: { value: null }, uHasMap: { value: 0 }, uST: { value: new THREE.Vector4(...(d.scale || [1, 1]), ...(d.offset || [0, 0])) },
      uColor: { value: c4(p._Color || d.color) }, uHigh: { value: c4(p._HighColor) }, uLow: { value: c4(p._LowColor) },
      uRamp: { value: p._RampLevels ?? 2 }, uLightScalar: { value: p._LightScalar ?? 1 }, uHI: { value: p._HighIntensity ?? 1.5 },
      uLI: { value: p._LowIntensity ?? 1 }, uScene: { value: p._SceneLighting ?? 1 }, uCut: { value: p._TTOCelSceneLightCut ?? 0 },
    }]);
    if (d.tex) {
      const t = api.texLoader.load(`${api.DATA}fx/tex/${d.tex}.webp`);
      t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping;
      u.map.value = t; u.uHasMap.value = 1;
    }
    if ((p._FresnelBrightness || 0) > 0 || (p._RimAlpha || 0) > 0)
      console.warn("tto_penguin: the cel shader's fresnel / rim are not drawn", d);
    // Cull Back: inside the mirror group three turns the front face round with the negative determinant, so its
    // front faces are Unity's (as mesh.js's FX/Phoenix)
    return new THREE.ShaderMaterial({ vertexShader: CEL_VERT, fragmentShader: CEL_FRAG, uniforms: u, lights: true, side: THREE.FrontSide });
  });

  // ---------------------------------------------------------------- lines (Constellation)
  // A LineRenderer's strip as Unity draws a 2-point line with alignment 0 (View): each point's side = the line's
  // direction x the line to the camera, width widthCurve(t) x widthMultiplier, colour colorGradient(t) (gamma, made
  // linear), u along the length (textureMode 0 Stretch), v across; numCornerVertices / numCapVertices 0 (the probe)
  function drawLine(fx, node, mesh, a, b, w, cAt, eye) {
    const um = uMat(fx, node);
    mesh.matrix.copy(um.invert()); mesh.matrixWorldNeedsUpdate = true;          // the points are in Unity's world
    const tan = b.clone().sub(a);
    if (tan.lengthSq() < 1e-12) { api.setMesh(mesh, [], [], [], []); return; }
    const pos = [], col = [], uv = [];
    [a, b].forEach((p, i) => {
      let s = V().crossVectors(tan, eye.clone().sub(p));
      if (s.lengthSq() < 1e-12) s = V(1, 0, 0); s.normalize();
      const h = w(i) / 2, k = cAt(i), l = p.clone().addScaledVector(s, -h), r = p.clone().addScaledVector(s, h);
      pos.push(l.x, l.y, l.z, r.x, r.y, r.z); col.push(...k, ...k); uv.push(i, 0, i, 1);
    });
    api.setMesh(mesh, pos, col, uv, [0, 1, 2, 2, 1, 3]);
  }

  // Penguin.StarLines (TTO1102:Penguin.<StarLines>d__341::MoveNext@0x1E2C220, Penguin.c:22423-23060). RPC_constellation
  // spawns one constellation_line per segment at StarAt(star i), identity (:6948-6995), its LineRenderers disabled
  // (m_Enabled false, world space, 2 points). Every frame from 0.4 s, per line i and each of its LineRenderers
  // (:22622-22703): SetPosition(0, fixedAt[i] + up) (the mark of star i, 1 m over its ground spot), f = clamp01((now -
  // (start + 0.4 + 0.12 i)) / 0.12) (0.12 = DAT_1830046e4), SetPosition(1, lerp(from, fixedAt[(i + 1) % n] + up, f)),
  // set_enabled(f > 0) (capstone 0x1E2CA35, plans/fx_penguin/tto.md 2.1); at the ignite (lastImpact + 0.05, :22778) every
  // LineRenderer's widthMultiplier x 2.2 (:22833-22834, capstone 0x1E2CE9A); 0.6 s later ClearStarFx destroys the lines
  // (:22966; the cue's kill). On the page: from = where the cue put the line (its star's mark), to = the cue's `to` (the
  // next mark); the cue stands at the line's draw start, 0.4 + 0.12 i (the game's spawn at 0.4 is hidden until then),
  // so f = clamp01(age / 0.12). The marks follow their foes in the game (:22580-22621); the page's foes stand still.
  // The two LineRenderers are drawn here (tto_sheep.js's LineRenderer part leaves disabled ones unbuilt; were it to
  // build them, they are taken over: driven, no points)
  api.part("Penguin.StarLines", (fx, root, comp, mat, nd, data) => {
    const C = api.curves, def = data.effects?.[fx.name];
    if (!C || !def) { console.warn("Penguin.StarLines: no curve readers (shuriken.js) or effect data", fx.name); return null; }
    const lines = [];
    def.nodes.forEach((n, j) => {
      for (const c of n.comps) {
        if (c.type !== "LineRenderer" || n.active === false) continue;
        const mn = c.m_Materials?.[0], md = mn && data.materials?.[mn];
        if (!md) continue;
        const P = c.m_Parameters || {}, o = fx.nodes[j];
        const mesh = api.fxMesh(o, api.fxMaterial(fx.cls, mn, md)); mesh.matrixAutoUpdate = false; mesh.renderOrder = c.m_SortingOrder || 0;
        lines.push({ o, mesh, wc: C.curveFn(P.widthCurve), mult: P.widthMultiplier ?? 1, gc: C.gradFn(P.colorGradient) });
      }
    });
    const to = cueTo(fx);
    if (!to) console.warn("Penguin.StarLines: no cue `to` (the next star's mark), the line is not drawn", fx.name);
    let age = 0, ignited = false, first = true;
    return { node: root, update(dt) {
      age += dt;
      if (first) {                                        // a LineRenderer part's own line on these nodes: ours now
        first = false;
        for (const L of lines) { const e = fx.emitters.find(x => x.node === L.o && x.line); if (e) { e.driven = true; e.pts = []; } }
      }
      const ig = fx.at?.ignite ?? (fx.killAt != null ? fx.killAt - 0.6 : null);
      if (!ignited && ig != null && age >= ig) { ignited = true; for (const L of lines) L.mult *= 2.2; }
      if (!to) return;
      const f = clamp01(age / 0.12), from = worldPos(fx, root), end = from.clone().lerp(to, f), eye = camPos(fx);
      for (const L of lines) {
        L.mesh.visible = f > 0;                           // set_enabled(f > 0)
        drawLine(fx, L.o, L.mesh, from, end, i => L.wc(i) * L.mult, i => L.gc(i), eye);
      }
    } };
  });

  // ---------------------------------------------------------------- Emperor's March
  // Penguin.EmperorShot: the ball. RPC_emperorPenguin state 3 (Penguin.c:8892-8935): ballAt = hero + 0.45 dir + 0.2 up,
  // the ball spawned at ballAt + 0.8 up, identity (EmperorSpawn), drop0 = now; state 4 every frame until start + 0.8
  // (:9019-9055): u = clamp01(4 (now - drop0)), position = ballAt + up x (1 - u^2) x 0.8; then (state 5, 0.85 s)
  // EmperorShot(ball, flock, ballAt, dir) (:9068) = <EmperorShot>d__358::MoveNext@0x1DC1520 (:103-969): reach = 22
  // (0x41B00000, :284), or 0.3 short of a wall the 22 m ray meets, at least 0.5 (:290-330; the page has no walls);
  // side = normalize(Cross(up, dir)) (:417-426: the hero's right); t0 = now (:409); each frame (:436-580) d = min(28 (now
  // - t0), reach), ballPos = from + dir d, its y = the ground under it (a 5 m ray down from 2 m above) + 0.45 (:466-479),
  // ball.position = ballPos, ball.Rotate(side, deltaTime x 900) (:563-578: Space.Self, the ball's own side axis = the
  // world's, its only turn being about it); at d >= reach (:817) the Goal (GoalFx: a cue) and Destroy(ball) (:842).
  // The 10 m target does not stop the ball (decision 7: only a foe of weight >= 60 or a structure would).
  // On the page: ballAt = where the cue put the ball - 0.8 up; dir = +z; the reach = the cue `to`'s distance ahead -
  // ballAt's (22.45 - 0.45 = 22), or 22 without one; the ground y 0. APPROXIMATED: between 0.8 and 0.85 s the game holds
  // the last drop frame (at most one frame above ballAt): held at ballAt
  api.part("Penguin.EmperorShot", (fx, root) => {
    const T0 = cueAt(fx, 0.55), ballAt = worldPos(fx, root).sub(V(0, 0.8, 0)), to = cueTo(fx);
    const reach = to ? Math.max(0.5, to.z - ballAt.z) : 22;
    const spin = new THREE.Quaternion();
    let age = 0;
    const place = (dt) => {
      const T = T0 + age;
      if (T < 0.85) {
        const u = T < 0.8 ? clamp01(4 * age) : 1;
        setPos(fx, root, ballAt.clone().addScaledVector(UP, (1 - u * u) * 0.8));
        return;
      }
      const d = Math.min(28 * (T - 0.85), reach);
      setPos(fx, root, V(ballAt.x, 0.45, ballAt.z).addScaledVector(FWD, d));
      root.quaternion.multiply(spin.setFromAxisAngle(RIGHT, 900 * DEG * dt));
      if (d >= reach) return "destroy";                    // the Goal: Destroy(ball)
    };
    place(0);
    return { node: root, update(dt) { age += dt; return place(dt); } };
  });

  // Penguin.FlockRise: a penguin of the flock. RPC_emperorPenguin state 2 (Penguin.c:8766-8829): q = LookRotation(dir) x
  // Euler(45, 0, 0), axis = q x up; penguin i spawned at FlockSpot(dir, i, n) - 0.7 axis, turned q (the cue's spot and
  // rot); FlockSpot@0x1DA4BF0: a = (150 i / (n - 1) - 75) deg, r 1.25 (1.9 for i >= 5), spot = hero + (right sin a +
  // dir cos a) r. <FlockRise>d__357::MoveNext@0x1DC31F0 (:986-1167): from = each penguin's position, t0 = now; while now
  // < t0 + 0.25: s = 4 (now - t0), h = (1 - (1 - s)^2) x 0.7 + 0.15 sin(s pi), position = from + axis h; then from +
  // 0.7 axis (the spot) and it ends. EmperorShot (0.85 s, :588-700), each frame for penguin i: start / startRot = its
  // position and rotation at the shot's start; delay = 0.06 + 0.035 i, s = clamp01((e - delay) / 0.18) (e = now - t0);
  // target = from + dir max(0, d - 28 delay) + (up sin th + side cos th) 0.65 + 0.15 up, th = 2 pi i / n + 540 deg x e
  // (capstone 0x1DC2287-0x1DC22B3), from = ballAt; position = lerp(start, target, s); when it moved (|step|^2 over a
  // small epsilon, DAT_182f3ff60, :664), rotation = Slerp(startRot, LookRotation(step) x Euler(80, 0, 0), s) (:660-682); at
  // the Goal (d >= reach) Scatter@0x1DB09F0 (:844) puts a poof at it (a cue) and destroys it.
  // On the page: ballAt = the hero + 0.45 ahead + 0.2 up (the ball's cue spot, :8892), the reach from the cue `to` as the
  // ball's; i = the cue's `i`, else from the spot's angle (a = atan2(x, d) of from + 0.7 axis); n = the cue's `n`, else 5
  // (decision 14: Emperor's March alone). APPROXIMATED: the epsilon (its value not read) is taken as 1e-8
  api.part("Penguin.FlockRise", (fx, root) => {
    const T0 = cueAt(fx, 0.3), from = worldPos(fx, root), to = cueTo(fx);
    const axis = UP.clone().applyQuaternion(fx.uQuat(root));
    const ballAt = V(0, 0.2, 0.45), reach = to ? Math.max(0.5, to.z - ballAt.z) : 22;
    const n = Math.max(1, fx.at?.n ?? 5);
    let i = fx.at?.i;
    if (typeof i !== "number") {
      const spot = from.clone().addScaledVector(axis, 0.7), a = Math.atan2(spot.x, spot.z) / DEG;
      i = n > 1 ? Math.min(n - 1, Math.max(0, Math.round((a + 75) / 150 * (n - 1)))) : 0;
    }
    const delay = 0.06 + 0.035 * i, E80 = new THREE.Quaternion().setFromEuler(new THREE.Euler(80 * DEG, 0, 0, "YXZ"));
    const look = new THREE.Quaternion(), rot = new THREE.Quaternion();
    let age = 0, start = null, startRot = null, prev = null;
    const place = () => {
      const T = T0 + age;
      if (T < 0.85) {
        const s = 4 * age;
        const h = s < 1 ? (1 - (1 - s) * (1 - s)) * 0.7 + 0.15 * Math.sin(s * Math.PI) : 0.7;
        setPos(fx, root, from.clone().addScaledVector(axis, h));
        return;
      }
      if (!start) { start = worldPos(fx, root); startRot = root.quaternion.clone(); prev = start.clone(); }
      const e = T - 0.85, d = Math.min(28 * e, reach), s = clamp01((e - delay) / 0.18), th = 2 * Math.PI * i / n + 3 * Math.PI * e;
      const target = ballAt.clone().addScaledVector(FWD, Math.max(0, d - 28 * delay))
        .addScaledVector(UP, Math.sin(th) * 0.65 + 0.15).addScaledVector(RIGHT, Math.cos(th) * 0.65);
      const p = start.clone().lerp(target, s), step = p.clone().sub(prev);
      setPos(fx, root, p); prev = p;
      if (step.lengthSq() > 1e-8) root.quaternion.copy(rot.copy(startRot).slerp(lookRot(step, look).multiply(E80), s));
      if (d >= reach) return "destroy";                    // Scatter: Destroy(penguin)
    };
    place();
    return { node: root, update(dt) { age += dt; return place(); } };
  });
}
