// wardrobe/fxparts/mesh.js: an effect's meshes and its own legacy animation (plans/fx_wolf/parts.md "Animation",
// "SkinnedMeshRenderer", "StaticMesh + ShatterMesh"; the loader comment above FX_PART_FILES in index.html), agent C
// 2026-11-09. The data comes from pipeline/wardrobe_fx_mesh.py (its docstring has the shapes), in Unity's space: the
// meshes hang under their nodes inside the effect's mirror group, so every number is the game's own.
//   StaticMesh           a MeshFilter's mesh drawn with the node's MeshRenderer materials (mirrorBlade_mirror's pane)
//   SkinnedMeshRenderer  a mesh skinned to the effect's own nodes (bladeFang / bloodFang's fan)
//   Animation            the Animation component's default clip, played on the effect's nodes (Blade Fang, Crusader,
//                        Dual Brand 1 / 2 / 4 swing their slash nodes with it)
//   ShatterMesh          ShatterMesh.cs: the StaticMesh breaks into its triangles, which fly apart (Mirror Blade)
// Wolf: bladefang_underslash / upperslash, bloodfang_underslash / upperslash (Animation + SkinnedMeshRenderer), crusader,
// lawbringer, dualbrand_slash1 / 2 / 4 (Animation; their trails are trail.js), mirrorblade_mirror (StaticMesh +
// ShatterMesh).

export default function register(api) {
  const { THREE, hermite, rnd, clamp01, fxMaterial, texLoader, DATA } = api;
  const mats = {};

  const texture = d => {
    const t = texLoader.load(`${DATA}fx/tex/${d.tex}.webp`);
    t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping;
    t.repeat.fromArray(d.scale || [1, 1]); t.offset.fromArray(d.offset || [0, 0]);
    return t;
  };
  // FX/DistortGlass (the Mirror Blade's pane; the game's own shader, plans/fx_wolf/parts.md): a GrabPass of the screen
  // times _MainTex, the grab read 32 texels off (a fixed shift of what is behind). APPROXIMATED as its fallback
  // SubShader, a multiply (Blend DstColor Zero) of what is already drawn, without the shift. The canvas is transparent
  // over the stage's CSS colour, and a plain multiply onto empty canvas gives nothing, so the alpha channel carries the
  // rest: rgb = drawn x texture (src Zero, dst SrcColor), alpha = 1 - the texture's luminance added to what is there
  // (One, One). Over the hero or another effect the result is the exact multiply; over empty canvas the browser's
  // premultiplied compositing gives stage x luminance(texture): a grey multiply of the backdrop
  const glass = d => {
    const m = new THREE.MeshBasicMaterial({ transparent: true, depthWrite: false, side: THREE.DoubleSide,
      blending: THREE.CustomBlending, blendEquation: THREE.AddEquation, blendSrc: THREE.ZeroFactor, blendDst: THREE.SrcColorFactor,
      blendSrcAlpha: THREE.OneFactor, blendDstAlpha: THREE.OneFactor });
    if (d.tex) m.map = texture(d);
    m.onBeforeCompile = sh => { sh.fragmentShader = sh.fragmentShader.replace("#include <dithering_fragment>",
      "#include <dithering_fragment>\n\tgl_FragColor.a = 1.0 - dot(gl_FragColor.rgb, vec3(0.2126, 0.7152, 0.0722));"); };
    return m;
  };
  // a renderer's material: the game's particle shaders through the page's fxMaterial; Diffuse (opaque) as a lit
  // Lambert, _Color x texture (both sides drawn: the mirror group flips the winding, and the effect meshes are thin);
  // DistortGlass as above; any other shader of the game's falls back to fxMaterial (alpha blended) with a warning
  const material = (fx, data, name) => {
    const d = name && data.materials?.[name];
    if (!d) return null;
    const k = fx.cls + "/" + name;
    if (mats[k]) return mats[k];
    let m;
    if (d.blend === "shader:FX/DistortGlass") m = glass(d);
    else if (d.blend === "opaque") {
      m = new THREE.MeshLambertMaterial({ side: THREE.DoubleSide });
      if (d.color) m.color.setRGB(d.color[0], d.color[1], d.color[2], THREE.SRGBColorSpace);
      if (d.tex) m.map = texture(d);
    } else {
      if (String(d.blend).startsWith("shader:")) console.warn("effect mesh: shader drawn as a particle material", d.blend, name);
      m = fxMaterial(fx.cls, name, d);
    }
    return (mats[k] = m);
  };
  // Unity draws submesh i with material i; materials past the last submesh draw the last submesh again; submeshes
  // past the last material are not drawn. Always a material list with one group each (three draws only the groups)
  const withMaterials = (g, c, list) => {
    const ms = list.filter(Boolean);
    if (!ms.length) return null;
    const sub = c.sub?.length ? c.sub : [[0, c.idx.length]];
    g.clearGroups();
    list.forEach((m, i) => { if (m) { const s = sub[Math.min(i, sub.length - 1)]; g.addGroup(s[0], s[1], ms.indexOf(m)); } });
    return ms;
  };
  // the mesh's geometry; no vertex colours in the data = white (fxMaterial multiplies by them)
  const geometry = c => {
    const g = new THREE.BufferGeometry(), n = c.verts;
    g.setAttribute("position", new THREE.Float32BufferAttribute(c.pos, 3));
    if (c.nrm) g.setAttribute("normal", new THREE.Float32BufferAttribute(c.nrm, 3));
    g.setAttribute("uv", new THREE.Float32BufferAttribute(c.uv || new Array(2 * n).fill(0), 2));
    g.setAttribute("color", new THREE.Float32BufferAttribute(c.col || new Array(4 * n).fill(1), 4));
    g.setIndex(c.idx);
    return g;
  };

  // ---- StaticMesh: a MeshFilter + MeshRenderer with no emitter (an emitter's own MeshFilter carries no mesh, so it
  // never comes here). Drawn as it is for the effect's whole life; a ShatterMesh on the node takes it over
  api.part("StaticMesh", (fx, node, c, mat, nd, data) => {
    const g = geometry(c), ms = withMaterials(g, c, (nd.mats || []).map(n => material(fx, data, n)));
    if (!ms) return null;
    const m = new THREE.Mesh(g, ms);
    m.frustumCulled = false; node.add(m);
    node.userData.fxStatic = m;
    return { node, update() {} };
  });

  // ---- SkinnedMeshRenderer: Unity skins each vertex as sum(weight x bone's world x bind pose x vertex), in world space
  // (the renderer's own transform only matters through m_RootBone, null in every Wolf skin). three's attached bind mode
  // gives world = mesh world x inverse(mesh world) x sum(weight x bone world x boneInverse x bindMatrix x vertex), so
  // boneInverse = the bind pose and bindMatrix = identity reproduce it exactly, the mirror included (the bones are inside
  // the mirror group, as finishProp binds a prop's skin)
  // (Fx.dispose frees geometry only: a skeleton's bone texture is freed here once its effect is gone)
  let skeletons = [];
  api.part("SkinnedMeshRenderer", (fx, node, c, mat, nd, data) => {
    skeletons = skeletons.filter(([f, s]) => f.alive || (s.dispose(), false));
    const g = geometry(c);
    g.setAttribute("skinIndex", new THREE.Uint16BufferAttribute(c.j, 4));
    g.setAttribute("skinWeight", new THREE.Float32BufferAttribute(c.w, 4));
    const ms = withMaterials(g, c, (c.mats || []).map(n => material(fx, data, n)));
    if (!ms) return null;
    const sm = new THREE.SkinnedMesh(g, ms);
    sm.frustumCulled = false; node.add(sm);
    const bones = c.bones.map(i => (i == null ? node : fx.nodes[i]));
    const inv = c.bones.map((_, i) => new THREE.Matrix4().fromArray(c.bind, 16 * i));
    sm.bind(new THREE.Skeleton(bones, inv), new THREE.Matrix4());
    skeletons.push([fx, sm.skeleton]);
    return { node, update() {} };
  });

  // ---- Animation: the legacy component plays its default clip on its own (m_PlayAutomatically) from the spawn,
  // sampled at the exact time every frame as the game does (the clip's Hermite keys through the page's hermite(); a
  // quaternion's four curves sampled apart, then normalised). The clip's wrap mode, else the component's: 0 Default and
  // 1 Once play once and the nodes keep the last pose (parts.md: the legacy end-of-clip hold, medium sure; it matters only
  // for crusader's last 0.6 s), 2 Loop, 4 PingPong, 8 ClampForever holds. No clip in any class has float curves or
  // events (wardrobe_fx_mesh.py). The effect's root (node 0) is never posed: the cue places it (no clip animates it)
  api.part("Animation", (fx, node, c) => {
    const clip = c.play && c.clips?.[c.clip];
    if (!clip) return null;
    const wrap = clip.wrap || c.wrap || 1, len = clip.len;
    const tracks = Object.entries(clip.tracks).map(([i, tr]) => ({ o: fx.nodes[+i], tr })).filter(x => x.o && x.o !== fx.nodes[0]);
    const local = t => {
      if (!(len > 0)) return 0;
      if (wrap === 2) return t % len;
      if (wrap === 4) { const k = t % (2 * len); return k > len ? 2 * len - k : k; }
      return Math.min(t, len);
    };
    const pose = t => {
      for (const { o, tr } of tracks) {
        if (tr.q) o.quaternion.fromArray(hermite(tr.q, 4, t)).normalize();
        if (tr.p) o.position.fromArray(hermite(tr.p, 3, t));
        if (tr.s) o.scale.fromArray(hermite(tr.s, 3, t));
      }
    };
    let t = 0;                                   // fxTick updates a new Fx before its first frame is drawn
    return { node, update(dt) {
      t += dt;
      pose(local(t));
      node.updateMatrixWorld(true);              // the parts after this one this frame (trails) read the new pose
    } };
  });

  // ---- ShatterMesh (ShatterMesh.cs, LateUpdate :53-165, CreateClone :169-397): its own clock from the spawn.
  // Until Delay: nothing (the pane stands whole). The first frame past Delay: CreateClone gives every triangle its own
  // three vertices (one submesh: mesh.triangles = 0..n-1, :269) and a velocity, all in the mesh's local space:
  //   normalize(cross(b - a, c - a)) times localVelocity axis by axis (:300-315), plus per axis with rndVelocity > 0
  //   Random.Range(-r, r + 1) (:320-355, the +1 is the game's), plus worldVelocity (:356, local despite the name);
  // that frame nothing moves. Each later frame until Delay + Life: vertex = its original + lerp(0, velocity,
  // clamp01((t - Delay) / Life)) (:98-149): the velocity is the whole travel. From Delay + Life on: left as the last
  // frame put it (:70). rndRotation is never read. Wolf: Delay 1.2, Life 0.6, local (0, 1, -3), random (3, 3, 6)
  api.part("ShatterMesh", (fx, node, e, mat, nd) => {
    const c = nd.comps.find(x => x.type === "StaticMesh");
    if (!c) return null;                         // "Shatter Mesh Error : MeshFilter doesn't exist" (:184)
    let t = 0, orig = null, vel = null, attr = null;
    const clone = m => {
      const n = c.idx.length, pos = new Float32Array(3 * n), uv = new Float32Array(2 * n), nrm = new Float32Array(3 * n),
            col = new Float32Array(4 * n);
      c.idx.forEach((v, i) => {
        for (let k = 0; k < 3; k++) { pos[3 * i + k] = c.pos[3 * v + k]; nrm[3 * i + k] = c.nrm ? c.nrm[3 * v + k] : 0; }
        for (let k = 0; k < 2; k++) uv[2 * i + k] = c.uv ? c.uv[2 * v + k] : 0;
        for (let k = 0; k < 4; k++) col[4 * i + k] = c.col ? c.col[4 * v + k] : 1;
      });
      orig = pos.slice(); vel = new Float32Array(n);   // 3 floats per triangle = n floats
      const A = new THREE.Vector3(), B = new THREE.Vector3(), C = new THREE.Vector3();
      for (let f = 0; f < n / 3; f++) {
        A.fromArray(pos, 9 * f); B.fromArray(pos, 9 * f + 3).sub(A); C.fromArray(pos, 9 * f + 6).sub(A);
        const v = B.cross(C);
        if (v.lengthSq() < 1e-10) v.set(0, 0, 0); else v.normalize();   // Unity's normalized: zero for a degenerate face
        const out = [v.x * e.localVelocity[0], v.y * e.localVelocity[1], v.z * e.localVelocity[2]];
        for (let k = 0; k < 3; k++) {
          if (e.rndVelocity[k] > 0) out[k] += rnd(-e.rndVelocity[k], e.rndVelocity[k] + 1);
          out[k] += e.worldVelocity[k];
          vel[3 * f + k] = out[k];
        }
      }
      const g = new THREE.BufferGeometry();
      attr = new THREE.Float32BufferAttribute(pos, 3);
      g.setAttribute("position", attr);
      g.setAttribute("normal", new THREE.Float32BufferAttribute(nrm, 3));
      g.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2));
      g.setAttribute("color", new THREE.Float32BufferAttribute(col, 4));
      if (Array.isArray(m.material)) m.material = m.material[0];   // one submesh from here on
      m.geometry.dispose(); m.geometry = g;
    };
    return { node, update(dt) {
      t += dt;
      if (t <= e.Delay || t >= e.Life + e.Delay) return;
      const m = node.userData.fxStatic;
      if (!m) return;
      if (!orig) { clone(m); return; }
      const u = clamp01((t - e.Delay) / e.Life), p = attr.array;
      for (let i = 0; i < p.length; i++) p[i] = orig[i] + vel[3 * Math.floor(i / 9) + (i % 3)] * u;
      attr.needsUpdate = true;
    } };
  });
}
