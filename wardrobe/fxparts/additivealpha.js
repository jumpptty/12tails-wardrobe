// wardrobe/fxparts/additivealpha.js: the game's Transparent/AdditiveAlpha on an effect mesh (2026-11-13, the Cat:
// plans/fx_cat/parts.md part 3 "Its material", decisions.md 52). The Support Fire shell (supportFire_fire's
// PirateCannon_fire, material PirateCannon_Fire: a dark iron top over a flame glow, _Color 0.784, _AdditiveRange 0.9);
// the Mole's napalm / nAttack materials later. The props' copy of the same shader is index.html's glowTwin (the champion
// weapons' glass edges): this is its effect-mesh twin, through api.shader, so mesh.js's material() (fxMaterial) gets it.
// Shader (rip Assets/Resources/gameassets/shader/AdditiveAlpha.shader:1-34), two passes over the same triangles:
//   pass 1 (:10-19)  Lighting On, Material { Ambient [_Color] Diffuse [_Color] }, AlphaTest GEqual [_AdditiveRange],
//                    combine primary x texture double, primary alpha x texture alpha; ZWrite and Cull at their
//                    defaults (on, Back); no Blend: opaque where it passes
//   pass 2 (:20-32)  no Lighting (off), ZWrite Off, Cull Off, Blend SrcAlpha One, AlphaTest LEqual [_AdditiveRange],
//                    combine texture, texture alpha: the texels under the cut added as light
// Defaults _Color (1, 1, 1, 1), _AdditiveRange 0.9 (:3, :5); _AdditiveColor (:4) is declared but no pass reads it.
// The page: material() returns the list [pass 1, pass 2] (mesh.js withMaterials gives one group per pass in that order;
// mesh.js sets userData.fxBlend on each; userData.fxPass 0 / 1 as mesh.js's other two-pass shaders). d.cut = the
// material's _AdditiveRange (wardrobe_fx.py material(), the lead's), d.color = _Color.
//   pass 1  a Lambert as mesh.js's lit(): color = 2 x _Color as sRGB (the gamma value), opacity = _Color.a (three's
//           alphaTest compares opacity x texture alpha: the game's primary alpha x texture alpha), alphaTest = cut (three
//           discards a < cut: GEqual exactly), not transparent (three writes alpha 1: opaque), FrontSide (inside the
//           mirror group three's front faces are Unity's, mesh.js)
//   pass 2  unlit MeshBasic with the map, no colour; discard a > cut (LEqual); Blend SrcAlpha One as the page's additive
//           convention (index.html fxMaterial, glowTwin): rgb x alpha added (One / One on the premultiplied colour, the
//           same sum), the canvas alpha = its brightest channel (the canvas is transparent over the stage's CSS colour);
//           depthWrite off, DoubleSide. The cut is a uniform, so materials with other cuts share one program
// APPROXIMATED: the game's own ambient and light colours (the page's hemisphere + sun); the game clamps the lit colour at
// 1 before the doubling; the game's gamma-space blending (the add is made on three's sRGB output, as glowTwin)
export default function register(api) {
  const { THREE, texLoader, DATA } = api;
  const texture = d => {
    const t = texLoader.load(`${DATA}fx/tex/${d.tex}.webp`);
    t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping;
    t.repeat.fromArray(d.scale || [1, 1]); t.offset.fromArray(d.offset || [0, 0]);
    return t;
  };
  api.shader("shader:Transparent/AdditiveAlpha", d => {
    const c = d.color || [1, 1, 1, 1], cut = d.cut ?? 0.9, map = d.tex ? texture(d) : null;
    const p1 = new THREE.MeshLambertMaterial({ transparent: false, opacity: c[3], alphaTest: cut, side: THREE.FrontSide });
    p1.color.setRGB(2 * c[0], 2 * c[1], 2 * c[2], THREE.SRGBColorSpace);
    if (map) p1.map = map;
    const p2 = new THREE.MeshBasicMaterial({ transparent: true, depthWrite: false, side: THREE.DoubleSide,
      blending: THREE.CustomBlending, blendEquation: THREE.AddEquation, blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor,
      blendSrcAlpha: THREE.OneFactor, blendDstAlpha: THREE.OneMinusSrcAlphaFactor });
    if (map) p2.map = map;
    const uCut = { value: cut };
    p2.onBeforeCompile = sh => {
      sh.uniforms.fxCut = uCut;
      sh.fragmentShader = "uniform float fxCut;\n" + sh.fragmentShader
        .replace("#include <alphatest_fragment>", "if ( diffuseColor.a > fxCut ) discard;   // AdditiveAlpha pass 2: AlphaTest LEqual")
        .replace("#include <dithering_fragment>", "#include <dithering_fragment>\n\tgl_FragColor.rgb *= gl_FragColor.a;"
          + "\n\tgl_FragColor.a = max(gl_FragColor.r, max(gl_FragColor.g, gl_FragColor.b));");
    };
    p2.customProgramCacheKey = () => "fxAdditiveAlpha2";
    p1.userData.fxPass = 0; p2.userData.fxPass = 1;
    return [p1, p2];
  });
}
