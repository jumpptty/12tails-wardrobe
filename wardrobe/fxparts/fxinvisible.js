// wardrobe/fxparts/fxinvisible.js: the game's FX/Invisible on an effect mesh (2026-11-13, the Chameleon:
// plans/fx_chameleon/parts.md part 3, decisions.md 51, 57). Clear Arrow's arrow (clearArrow: the worn arrow's root mesh
// in material clearArrow, the own-team view: 35 % white with a blue rim); the hero look of the same name is index.html's
// HERO_SKINS (part 10), on the same shell helper. Through api.shader, so mesh.js's material() (fxMaterial, api.shaders)
// gets it: mesh.js unedited.
// Shader (compiled in BB's resources.assets, checks/fx_chameleon_research/parts/shaders.txt:255-360; the rip's .shader is
// a stub): SubShader Tags Queue Transparent, two passes over the same triangles:
//   pass 1 (:262-270)  Fog off (colour 0), Blend SrcAlpha OneMinusSrcAlpha, ColorMask RGB, ZWrite and Cull at their
//                      defaults (on, Back), no Lighting, SetTexture [_MainTex] { ConstantColor (1,1,1,0.35) combine
//                      texture, constant alpha }: rgb = the texel, alpha = 0.35 whatever the texel's alpha (_Color unread)
//   pass 2 (:271-349)  Cull Front, Blend SrcAlpha SrcColor, ColorMask RGB, ZWrite on (default); vertex program: clip
//                      position, then xy += (n.x P[0][0], n.y P[1][1]) x clip z x 0.003 (n = the view-space normal,
//                      invtrans modelview x normal), colour constant (0.3, 0.6, 1, 0.75); fragment = that colour. Drawn
//                      after pass 1, whose depth hides the shell inside the silhouette: a blue rim outside it
// The fixed-function SubShader (:351-358, Color (0.3, 0.6, 1, 0.75), Blend SrcAlpha SrcColor) and Fallback
// "Transparent/Diffuse" are for cards without vertex programs: not drawn. clearArrow.mat: _MainTex none ("white" default),
// _Color white; its _TintColor (0, 1, 0.35, 0.14) and _Emission are leftovers no pass reads (mesh_probe.txt).
// The page: material() gets the list [pass 1, pass 2] (mesh.js withMaterials gives one group per pass over the same
// range, in that order; both in three's transparent list, whose sort is stable within one object, so pass 2 draws after
// pass 1; userData.fxPass 0 / 1 as mesh.js's other two-pass shaders):
//   pass 1  unlit MeshBasic, the map when the material has a texture (else none: white), transparent, the alpha set to
//           opacity 0.35 after map_fragment (the constant alpha: the texel's alpha not multiplied in), depthWrite on,
//           FrontSide (Cull Back: inside the mirror group three's front faces are Unity's, mesh.js), NormalBlending
//   pass 2  api.shellMaterial({ color: [0.3, 0.6, 1], alpha: 0.75, k: 0.003, blend: "srcColor" }) (index.html's shared
//           shell, parts.md Interfaces 3: CosmicRift's vertex push with k 0.003, BackSide = Unity's Cull Front,
//           CustomBlending SrcAlpha / SrcColor for rgb, depthWrite on), marked transparent here if it is not, so it draws
//           after pass 1 and not in the opaque list before it. If the page has no api.shellMaterial, a warning (once) and
//           pass 1 alone: the 35 % arrow without its rim
// APPROXIMATED: ColorMask RGB (three's colorWrite is all or nothing): pass 1 writes the canvas alpha as three's normal
// blend does (a + dst.a (1 - a)), so over the transparent canvas the stage's CSS colour stands for the game's framebuffer
// behind (as fxMaterial's "alpha"; where something is already drawn dst.a is 1 and stays 1, as ColorMask RGB keeps it);
// the canvas alpha of pass 2's SrcColor blend is the shell helper's convention (its brightest channel x alpha, as
// fxMaterial's additive trick: Interfaces 3); the game's gamma-space blending (the blends are made on three's sRGB output)
export default function register(api) {
  const { THREE, texLoader, DATA } = api;
  const texture = d => {
    const t = texLoader.load(`${DATA}fx/tex/${d.tex}.webp`);
    t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping;
    t.repeat.fromArray(d.scale || [1, 1]); t.offset.fromArray(d.offset || [0, 0]);
    return t;
  };
  let warned = false;
  api.shader("shader:FX/Invisible", d => {
    const p1 = new THREE.MeshBasicMaterial({ transparent: true, opacity: 0.35, depthWrite: true, side: THREE.FrontSide });
    if (d.tex) p1.map = texture(d);
    p1.onBeforeCompile = sh => {
      sh.fragmentShader = sh.fragmentShader.replace("#include <map_fragment>",
        "#include <map_fragment>\n\tdiffuseColor.a = opacity;   // FX/Invisible pass 1: ConstantColor (1,1,1,0.35), combine texture, constant alpha");
    };
    p1.customProgramCacheKey = () => "fxInvisible1";
    p1.userData.fxPass = 0;
    if (typeof api.shellMaterial !== "function") {
      if (!warned) { warned = true; console.warn("FX/Invisible: api.shellMaterial missing, the effect mesh drawn without its blue rim"); }
      return [p1];
    }
    const p2 = api.shellMaterial({ color: [0.3, 0.6, 1], alpha: 0.75, k: 0.003, blend: "srcColor" });
    if (!p2) return [p1];
    if (!p2.transparent) p2.transparent = true;   // the transparent list, after pass 1 (Queue Transparent)
    p2.userData.fxPass = 1;
    return [p1, p2];
  });
}
