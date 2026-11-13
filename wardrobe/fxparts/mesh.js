// wardrobe/fxparts/mesh.js: an effect's meshes and its own legacy animation (plans/fx_wolf/parts.md "Animation",
// "SkinnedMeshRenderer", "StaticMesh + ShatterMesh"; the loader comment above FX_PART_FILES in index.html), agent C
// 2026-11-09. The data comes from pipeline/wardrobe_fx_mesh.py (its docstring has the shapes), in Unity's space: the
// meshes hang under their nodes inside the effect's mirror group, so every number is the game's own.
//   StaticMesh           a MeshFilter's mesh drawn with the node's MeshRenderer materials (mirrorBlade_mirror's pane)
//   SkinnedMeshRenderer  a mesh skinned to the effect's own nodes (bladeFang / bloodFang's fan)
//   Animation            the Animation component's default clip, played on the effect's nodes (Blade Fang, Crusader,
//                        Dual Brand 1 / 2 / 4 swing their slash nodes with it); node.userData.fxAnim.play(name, fade,
//                        wrap) switches the clip (Eden Sanctuary's destroy; the Penguin's tornado / typhoon / cosmicFriday);
//                        one that does not play by itself stands idle until a part plays it; fxAnim.rewind() (the Cat)
//   ShatterMesh          ShatterMesh.cs: the StaticMesh breaks into its triangles, which fly apart (Mirror Blade)
// Wolf: bladefang_underslash / upperslash, bloodfang_underslash / upperslash (Animation + SkinnedMeshRenderer), crusader,
// lawbringer, dualbrand_slash1 / 2 / 4 (Animation; their trails are trail.js), mirrorblade_mirror (StaticMesh +
// ShatterMesh). Sheep (2026-11-10): the FX/Phoenix material (Soul of Arms, Divinity Spear / Sword), faded by
// alphatimer.js. Penguin (2026-11-10, plans/fx_penguin/parts.md "Who builds what" row A, Interfaces 1 and 5): the
// materials Transparent/AdditiveSaturate (two passes: material() returns a list for one name), Transparent/Opaque1,
// Transparent/Opaque2 and DiffuseAmbient; Animation's play(name, fade, wrap). Cat (2026-11-13, plans/fx_cat/parts.md
// part 4, Interfaces 1, decisions.md 51): the Animation part built also when its play is off, and rewind().

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
  // FX/Phoenix (the game's own; rip Assets/Resources/gameassets/shader/Phoenix.shader:1-23; the Sheep's Soul of Arms
  // weapons, Divinity Spear / Sword, Penguin's absoluteZero): fixed-function lit, Material { Ambient [_Color] Diffuse
  // [_Color] Emission [_Emission] } (:12-16), SetTexture combine texture * primary double, texture alpha * primary alpha
  // (:21: rgb = 2 x texture x (_Emission + _Color x the lights), alpha = texture.a x _Color.a), Blend SrcAlpha
  // OneMinusSrcAlpha, AlphaTest Greater 0, ZWrite and Cull left at their defaults (on, Back). As a Lambert: map x
  // 2 _Color x the page's lights + map x 2 _Emission (emissiveMap = map), the gamma colours as sRGB; the default _Color
  // (1, 1, 1, 1) and _Emission (0, 0, 0, 0) (:3-4) when the data has none. Front faces only: inside the mirror group
  // three flips the front face with the negative determinant, so its front faces are Unity's. AlphaTimer drives opacity.
  // APPROXIMATED: the game's own ambient and light colours (the page's lights instead); the game clamps the lit colour at
  // 1 before the doubling (with the Sheep's colours the page's lights, about 1.1 at most, stay under it); ColorMask RGB (:20)
  // leaves the frame's alpha alone, but here the canvas is transparent over the stage's CSS colour, so alpha is written
  const phoenix = d => {
    const c = d.color || [1, 1, 1, 1], e = d.emission || [0, 0, 0, 0];
    const m = new THREE.MeshLambertMaterial({ transparent: true, opacity: c[3], alphaTest: 1e-4, side: THREE.FrontSide });
    m.color.setRGB(2 * c[0], 2 * c[1], 2 * c[2], THREE.SRGBColorSpace);
    m.emissive.setRGB(2 * e[0], 2 * e[1], 2 * e[2], THREE.SRGBColorSpace);
    if (d.tex) m.map = m.emissiveMap = texture(d);
    return m;
  };
  // Transparent/AdditiveSaturate (the game's own; rip Assets/Resources/gameassets/shader/AdditiveSaturate.shader:1-45;
  // the Penguin's arcticEmperor statue, also Wolf_heartRing and ShadowPortal_0, not cued): TWO passes over the same
  // triangles, both BindChannels vertex / color / texcoord (:11-15, :29-33: the vertex colour is "primary"), ZWrite Off,
  // Cull Off, Fog black, AlphaTest Greater 0.01, ColorMask RGB (:16-23, :34-41):
  //   pass 1 (:9-26)  Blend SrcAlpha OneMinusSrcAlpha; constant _TintColor x primary (:24), then texture x previous
  //                   double (:25): rgb = 2 x tint x vcol x texture, alpha = 2 x tint.a x vcol.a x texture.a
  //   pass 2 (:27-43) Blend SrcAlpha One; one stage, constant _Emission x previous double (:42), and a pass's first
  //                   "previous" is primary: rgb = 2 x emission x vcol, alpha = 2 x emission.a x vcol.a, NO texture (the
  //                   SetTexture binds _MainTex but its combine never reads it): the whole shape glows
  // Defaults _TintColor (0.5, 0.5, 0.5, 0.5), _Emission (0, 0, 0, 0) (:3-4). The fixed-function combiner saturates at 1
  // after the doubling, so the colour and opacity uniforms are left unclamped (2 x tint, 2 x emission, 2 x their alphas)
  // and the clamp is applied in the shader after the texture and vertex colour are in (min(1) in linear space = the
  // combiner's min(1) in gamma, the curve being monotonic): a bright _Emission (0.75 x 2) times a dim vertex colour stays
  // as dim as the game's. Pass 1 blends as fxMaterial's "alpha" (normal blending); pass 2 as fxMaterial's "add" (the
  // premultiplied colour, alpha = its brightest channel, so the transparent canvas keeps the added light over the stage's
  // CSS colour). The list order is the draw order (withMaterials puts pass 1's group first; three's transparent sort is
  // stable within one object). userData.fxPass = 0 / 1 (the part that drives _TintColor.a / _Emission.a,
  // Penguin_arcticEmperor, finds each pass by it).
  // APPROXIMATED: "double" taken to double the alpha too (a combine without its own alpha part applies the same
  // operation to alpha, and the page's particle shaders already double it, index.html fxMaterial); three's alphaTest keeps
  // a = 0.01 that the game's Greater drops (no 8-bit alpha is exactly 0.01); the game's gamma-space blending
  const saturate = d => {
    const tint = d.tint || [.5, .5, .5, .5], e = d.emission || [0, 0, 0, 0];
    const p1 = new THREE.MeshBasicMaterial({ vertexColors: true, transparent: true, depthWrite: false, side: THREE.DoubleSide,
      alphaTest: 0.01, opacity: 2 * tint[3] });
    p1.color.setRGB(2 * tint[0], 2 * tint[1], 2 * tint[2], THREE.SRGBColorSpace);
    if (d.tex) p1.map = texture(d);
    p1.onBeforeCompile = sh => { sh.fragmentShader = sh.fragmentShader.replace("#include <color_fragment>",
      "#include <color_fragment>\n\tdiffuseColor = min( diffuseColor, vec4( 1.0 ) );   // AdditiveSaturate pass 1: the combiner's saturate"); };
    const p2 = new THREE.MeshBasicMaterial({ vertexColors: true, transparent: true, depthWrite: false, side: THREE.DoubleSide,
      alphaTest: 0.01, opacity: 2 * e[3], premultipliedAlpha: true, blending: THREE.CustomBlending,
      blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor, blendSrcAlpha: THREE.OneFactor, blendDstAlpha: THREE.OneMinusSrcAlphaFactor });
    p2.color.setRGB(2 * e[0], 2 * e[1], 2 * e[2], THREE.SRGBColorSpace);
    p2.onBeforeCompile = sh => { sh.fragmentShader = sh.fragmentShader.replace("#include <color_fragment>",
      "#include <color_fragment>\n\tdiffuseColor = min( diffuseColor, vec4( 1.0 ) );   // AdditiveSaturate pass 2: the combiner's saturate")
      .replace("#include <dithering_fragment>",
      "#include <dithering_fragment>\n\tgl_FragColor.a = max(gl_FragColor.r, max(gl_FragColor.g, gl_FragColor.b));"); };
    p1.userData.fxPass = 0; p2.userData.fxPass = 1;
    return [p1, p2];
  };
  // Transparent/Opaque1 and Transparent/Opaque2 (the game's own; rip .../shader/Opaque1.shader:1-32, Opaque2.shader:1-34;
  // the Penguin's cosmicFriday disc (Opaque1) and iceBlock (Opaque2); also Bison earthSmasher and Cat supportFire_cannon
  // (Opaque1), not cued yet). Both passes of each: Lighting On, Material { Ambient [_Color] Diffuse [_Color] }, Blend
  // SrcAlpha OneMinusSrcAlpha, SetTexture combine primary x texture double, primary alpha x texture alpha (Opaque1
  // :10-18, :22-28; Opaque2 :10-17, :21-30): rgb = 2 x texture x _Color x the lights, alpha = _Color.a x texture.a (the
  // alpha part has no "double"; a lit primary's alpha is the material's diffuse alpha). No BindChannels: no vertex colour.
  //   Opaque1 pass 1 (:8-19)  ZWrite Off, AlphaTest GEqual 0.95     pass 2 (:20-29)  ZWrite On, Cull Back (defaults)
  //   Opaque2 pass 1 (:8-18)  ZWrite On, AlphaTest GEqual 0.95      pass 2 (:19-31)  ZWrite Off, Cull Off, AlphaTest Less 0.95
  // Pass 1 can pass only where _Color.a x texture.a >= 0.95. Opaque2 builds it only when the saved _Color.a reaches 0.95;
  // below that (iceblock 0.75) it never draws a pixel and material() returns pass 2 alone (one material, as before).
  // Opaque1 builds both passes always (2026-11-13, plans/fx_bat/parts.md part 10, Interfaces 5): the Bat's guardian wings
  // (guardian2, _Color.a 0 in the prefab) are faded 0 -> 1 by its script (Bat_guardianOfTheNight.cs:383-406), so a part
  // drives both passes' opacity (= _Color.a: three's alphaTest compares opacity x texture alpha, the game's test exactly);
  // at a saved alpha below 0.95 (cosmicFriday 0.46) pass 1 discards every pixel, as the game's. With both, the list is
  // pass 1 then pass 2 (userData.fxPass 0 / 1). three's alphaTest discards a < alphaTest, the game's GEqual exactly;
  // Opaque2's "Less" is a discard of a >= 0.95 after three's alpha test.
  // Default _Color (1, 1, 1, 1) (:3). As phoenix(): a Lambert, color = 2 x _Color as sRGB, front faces only where the
  // game culls (the mirror group's flipped winding makes three's front faces Unity's).
  // APPROXIMATED: the game's own ambient and light colours (the page's hemisphere + sun instead); the game clamps the lit
  // colour at 1 before the doubling. A part that animates an Opaque2 _Color.a across 0.95 would need its pass 1 too: none
  // does yet (alphatimer.js drives Opaque1 / Opaque2's opacity on every pass it finds, 2026-11-13, plans/fx_bison/parts.md
  // part 2; an Opaque2 saved under 0.95 has pass 2 alone, which discards alpha >= 0.95)
  const lit = (d, map, o) => {
    const c = d.color || [1, 1, 1, 1];
    const m = new THREE.MeshLambertMaterial({ transparent: true, opacity: c[3], ...o });
    m.color.setRGB(2 * c[0], 2 * c[1], 2 * c[2], THREE.SRGBColorSpace);
    if (map) m.map = map;
    return m;
  };
  const opaque1 = d => {
    const map = d.tex ? texture(d) : null;
    const p2 = lit(d, map, { depthWrite: true, side: THREE.FrontSide });
    const p1 = lit(d, map, { depthWrite: false, side: THREE.FrontSide, alphaTest: 0.95 });   // both passes always (above)
    p1.userData.fxPass = 0; p2.userData.fxPass = 1;
    return [p1, p2];
  };
  const opaque2 = d => {
    const map = d.tex ? texture(d) : null, c = d.color || [1, 1, 1, 1];
    const p2 = lit(d, map, { depthWrite: false, side: THREE.DoubleSide });
    p2.onBeforeCompile = sh => { sh.fragmentShader = sh.fragmentShader.replace("#include <alphatest_fragment>",
      "#include <alphatest_fragment>\n\tif ( diffuseColor.a >= 0.95 ) discard;   // Opaque2 pass 2: AlphaTest Less 0.95"); };
    if (!(c[3] >= 0.95)) return p2;
    const p1 = lit(d, map, { depthWrite: true, side: THREE.FrontSide, alphaTest: 0.95 });
    p1.userData.fxPass = 0; p2.userData.fxPass = 1;
    return [p1, p2];
  };
  // DiffuseAmbient (the game's own; rip .../shader/diffuseambient.shader:1-19; the Penguin's snowMan): one opaque pass,
  // Lighting On, SeparateSpecular On (no Specular colour: black), Material { Ambient [_Ambient] Diffuse [_Color] }
  // (:9-14), combine primary x texture double (:15): rgb = 2 x texture x (_Ambient x the ambient light + _Color x the
  // lights); ZWrite on, Cull Back; defaults _Color and _Ambient (1, 1, 1, 1) (:3-4). As a Lambert with color = 2 x _Color
  // (the lights' part), its ambient part rebuilt from the same irradiance with 2 x _Ambient in place of 2 x _Color (the
  // uniform fxAmbient; a uniform, not text, so materials with other _Ambient values share one program correctly). The
  // data's "ambient" (the material's _Ambient) when the extractor saves it, else the shader default white (the rip's
  // snowman_0.mat: (0.95, 1, 0.995), so 5 % off in red without it).
  // APPROXIMATED: the game's own lights (the page's hemisphere light stands for its ambient, the sun for its lights); the
  // game clamps the lit colour at 1 before the doubling
  const diffuseAmbient = d => {
    const c = d.color || [1, 1, 1, 1], a = d.ambient || [1, 1, 1, 1];
    const m = new THREE.MeshLambertMaterial({ side: THREE.FrontSide });
    m.color.setRGB(2 * c[0], 2 * c[1], 2 * c[2], THREE.SRGBColorSpace);
    if (d.tex) m.map = texture(d);
    const amb = new THREE.Color().setRGB(2 * a[0], 2 * a[1], 2 * a[2], THREE.SRGBColorSpace);
    m.onBeforeCompile = sh => {
      sh.uniforms.fxAmbient = { value: amb };
      sh.fragmentShader = "uniform vec3 fxAmbient;\n" + sh.fragmentShader.replace("#include <lights_fragment_end>",
        "#include <lights_fragment_end>\n#ifdef USE_MAP\n\treflectedLight.indirectDiffuse = irradiance * BRDF_Lambert( fxAmbient * sampledDiffuseColor.rgb );\n" +
        "#else\n\treflectedLight.indirectDiffuse = irradiance * BRDF_Lambert( fxAmbient );\n#endif");
    };
    return m;
  };
  // a renderer's material: the game's particle shaders through the page's fxMaterial; Diffuse (opaque) as a lit
  // Lambert, _Color x texture (both sides drawn); DistortGlass, Phoenix, AdditiveSaturate, Opaque1 / Opaque2 and
  // DiffuseAmbient as above; any other shader of the game's falls back to fxMaterial (alpha blended) with a warning.
  // A multi-pass shader gives a LIST (its passes in draw order) for one material name; withMaterials draws every pass
  // over that material's submesh. userData.fxBlend = the data's blend on each (alphatimer.js reads it)
  const material = (fx, data, name) => {
    const d = name && data.materials?.[name];
    if (!d) return null;
    const k = fx.cls + "/" + name;
    if (mats[k]) return mats[k];
    let m;
    if (d.blend === "shader:FX/DistortGlass") m = glass(d);
    else if (d.blend === "shader:FX/Phoenix" || d.blend === "shader:FX/Lavu") m = phoenix(d);   // FX/Lavu: Phoenix's pass without the Transparent queue tag (plans/fx_monkey/parts.md part 7)
    else if (d.blend === "shader:Transparent/AdditiveSaturate") m = saturate(d);
    else if (d.blend === "shader:Transparent/Opaque1") m = opaque1(d);
    else if (d.blend === "shader:Transparent/Opaque2") m = opaque2(d);
    else if (d.blend === "shader:DiffuseAmbient") m = diffuseAmbient(d);
    else if (d.blend === "opaque") {
      m = new THREE.MeshLambertMaterial({ side: THREE.DoubleSide });
      if (d.color) m.color.setRGB(d.color[0], d.color[1], d.color[2], THREE.SRGBColorSpace);
      if (d.tex) m.map = texture(d);
    } else {
      // a shader a part module draws itself (api.shader: fxparts/tto_sheep.js's Standard ...) comes back from fxMaterial
      if (String(d.blend).startsWith("shader:") && !api.shaders?.[d.blend]) console.warn("effect mesh: shader drawn as a particle material", d.blend, name);
      m = fxMaterial(fx.cls, name, d);
    }
    for (const p of [].concat(m)) p.userData.fxBlend = d.blend;
    return (mats[k] = m);
  };
  // Unity draws submesh i with material i; materials past the last submesh draw the last submesh again; submeshes
  // past the last material are not drawn. Always a material list with one group each (three draws only the groups); a
  // material that is a list of passes (material() above) gives one group per pass over the same range, in pass order
  const withMaterials = (g, c, list) => {
    const ms = list.flatMap(m => (m ? [].concat(m) : []));
    if (!ms.length) return null;
    const sub = c.sub?.length ? c.sub : [[0, c.idx.length]];
    g.clearGroups();
    list.forEach((m, i) => {
      if (!m) return;
      const s = sub[Math.min(i, sub.length - 1)];
      for (const p of [].concat(m)) g.addGroup(s[0], s[1], ms.indexOf(p));
    });
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
  // events (wardrobe_fx_mesh.py). The effect's root (node 0) is never posed: the cue places it (no clip animates it).
  // Another part switches the clip with node.userData.fxAnim.play(name, fade, wrap) (2026-11-10, Eden Sanctuary's
  // CrossFade("destroy", 0.2), Sheep_edenSanctuary.cs:409), as Unity's legacy Animation does it:
  //   play(name)        Animation.Play: a cut to the clip from its start; a clip already playing is not rewound
  //   play(name, fade)  Animation.CrossFade: the same, its weight rising 0 -> 1 over fade seconds
  //   play(name, fade, wrap)  then animation.wrapMode = wrap (2026-11-10, the Penguin: Penguin_tornado.cs:768-771
  //                     Play("create") + wrapMode = Once, :744-749 Play("root") + Loop, :925-931 Play("destroy") + Once;
  //                     Penguin_typhoon.cs:902-907, :733-738; Penguin_cosmicFriday.cs:391-394, :330-335, :566-569). The
  //                     tornado's / typhoon's clips carry wrap 0 under a Loop component, so without it "create" would
  //                     loop. Unity's setter writes the mode into every AnimationState of the component, so it holds for
  //                     the clip just started and for every later play() too, whatever the clip's own wrap (no wrap
  //                     given = left as it is; 0 = Default clears it: back to the clip's, else the component's). It is
  //                     set after the "still playing" test, as the scripts set it after Play. Values: 1 Once, 2 Loop,
  //                     4 PingPong, 8 ClampForever (as the clips' own)
  // The pose is set at once (Unity samples the animation after Update, in the same frame). Returns false for a clip the
  // component lacks. APPROXIMATED in the cross-fade: the outgoing side is the pose at the moment of the call, held (a
  // clip that is still playing would run on in Unity while it fades out), and rotations blend by slerp; Eden's two clips
  // meet at the same pose (plans/fx_sheep/parts.md), so there the result is the game's. Medium sure: that the wrapMode
  // setter reaches every state (and so later clips); every Penguin script sets it again right after each Play, so there it
  // cannot matter.
  // 2026-11-13, the Cat (plans/fx_cat/parts.md part 4, Interfaces 1, decisions.md 51): an Animation whose play
  // (m_PlayAutomatically) is off is built too, idle: nothing is posed (Unity: the prefab's pose stands, the nodes as the
  // data places them) until a part calls play(name), from then on as any other (Support Fire's cannons: play off, the
  // hero's RPC_supportFire_fire plays "fire", Cat.cs:10672-10677; Grand Casino Arcade's machine plays by itself, its
  // "fire" / "destroy" played by fxparts/cat.js). Before 2026-11-13 such a component built nothing.
  //   rewind()          Animation.Rewind: the current clip's time back to 0 (posed so at once), so a play() of the same
  //                     clip right after restarts it (a clip still playing is not rewound by play() alone: the same cannon
  //                     picked twice within its 0.5 s "fire"); nothing before the first play(). APPROXIMATED: a Once
  //                     clip that had ended runs again from the rewind on (Unity keeps a stopped state stopped until
  //                     Play); the game's only caller plays it right after (Rewind(); Play("fire"))
  api.part("Animation", (fx, node, c) => {
    if (!c.clips || !(c.play ? c.clips[c.clip] : Object.keys(c.clips).length)) return null;
    let cur = null, wrap, len, tracks = [], t = 0, fade = 0, from = null, forced = 0;   // forced: animation.wrapMode set by a part; cur null: idle (play off)
    const use = name => {
      const clip = c.clips[name];
      cur = name; wrap = forced || clip.wrap || c.wrap || 1; len = clip.len;
      tracks = Object.entries(clip.tracks).map(([i, tr]) => ({ o: fx.nodes[+i], tr })).filter(x => x.o && x.o !== fx.nodes[0]);
    };
    const local = t => {
      if (!(len > 0)) return 0;
      if (wrap === 2) return t % len;
      if (wrap === 4) { const k = t % (2 * len); return k > len ? 2 * len - k : k; }
      return Math.min(t, len);
    };
    const q = new THREE.Quaternion();
    const pose = () => {
      const k = local(t), w = from ? Math.min(1, t / fade) : 1;
      for (const { o, tr } of tracks) {
        if (tr.q) o.quaternion.fromArray(hermite(tr.q, 4, k)).normalize();
        if (tr.p) o.position.fromArray(hermite(tr.p, 3, k));
        if (tr.s) o.scale.fromArray(hermite(tr.s, 3, k));
        const f = w < 1 && from.get(o);
        if (!f) continue;
        o.position.lerpVectors(f.p, o.position, w); o.scale.lerpVectors(f.s, o.scale, w);
        o.quaternion.copy(q.copy(f.q).slerp(o.quaternion, w));
      }
      if (w >= 1) from = null;
      node.updateMatrixWorld(true);              // the parts after this one this frame (trails) read the new pose
    };
    if (c.play) use(c.clip);                     // fxTick updates a new Fx before its first frame is drawn; play off: idle
    const em = { node, update(dt) { if (cur == null) return; t += dt; pose(); },
      rewind() { if (cur == null) return; t = 0; from = null; pose(); },
      play(name, fadeLen = 0, wrapMode) {
        if (!c.clips[name]) return false;
        const setWrap = () => {                  // animation.wrapMode = wrapMode, after the Play (see above)
          if (wrapMode == null) return;
          forced = wrapMode || 0;
          const clip = c.clips[cur];
          wrap = forced || clip.wrap || c.wrap || 1;
        };
        if (name === cur && (wrap === 2 || wrap === 4 || wrap === 8 || t < len)) { setWrap(); return true; }   // still playing
        use(name);
        from = fadeLen > 0 ? new Map(tracks.map(({ o }) => [o, { p: o.position.clone(), q: o.quaternion.clone(), s: o.scale.clone() }])) : null;
        t = 0; fade = fadeLen;
        setWrap();
        pose();
        return true;
      } };
    node.userData.fxAnim = em;
    return em;
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
      // one submesh from here on (mesh.triangles = ..., :269; the renderer's materials are left alone, ShatterMesh.cs never
      // touches them): by Unity's rule every material past the last submesh draws it again, so each of the renderer's
      // materials, and each pass of a multi-pass one (arcticEmperor's AdditiveSaturate), draws the whole clone, in order.
      // One material (the Wolf's mirror pane) stays a single material, as before
      if (Array.isArray(m.material)) {
        if (m.material.length === 1) m.material = m.material[0];
        else m.material.forEach((_, i) => g.addGroup(0, n, i));
      }
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
