// wardrobe/fxparts/particles.js: the game's particle shaders the page's fxMaterial does not draw (2026-11-13, the Bat:
// plans/fx_bat/parts.md part 9 and its Verification, decisions.md 40-41). Materials only, through api.shader(blend,
// make): index.html's fxMaterial asks FXSHADERS first (and caches what make returns per class / material name, FX.mats),
// so every emitter that takes fxMaterial's material (legacy particles, ImageEmitter, RingEmitter, LineEmitter, mesh.js's
// renderers, trail.js ...) draws through these unchanged: vertex colours (RGBA, the emitters' linear ramp), _MainTex
// with its saved scale / offset, repeat wrap, the material's opacity (a part's fade) scaling the vertex alpha, as
// fxMaterial's own branches.
//
// The data's blend names (pipeline/wardrobe_fx.py material(): "shader:" + the name in the game shader's first line;
// BUILTIN_BLEND for Unity's built-in ones):
//   multiply                          built-in 205, Unity 3.5's Particles/Multiply (24 materials in the rip: BlackTrail,
//                                     ShadowLine1-4, the Bat's Smoke4_multiply ...; decisions.md 40)
//   shader:Particles/MultiplyOffset   rip gameassets/shader/MultiplyOffset.shader:1-27 (blind, corruption, Shadow1, the
//                                     Wolf's darkEdge_hit, vitalityStrike_hit)
//   shader:Particles/AlphaOffset      AlphaOffset.shader:1-27 (the Wolf's doubleArt, the Sheep's retuunCast, freeCast,
//                                     instantCast, the Bat's nefariousWhip4 ...: 21 materials)
//   shader:Particles/AdditiveOffset   AdditiveOffset.shader (the Wolf's bladeFang_hit / bloodFang_hit, the Penguin's
//                                     nAttack_hit and 30 more)
// Before this module the three "shader:" ones fell to fxMaterial's last branch (alpha blended, 2 x tint) and 205 to
// "add" (the shadows glowed instead of darkening): their look changes (NOTES.md).
//
// The page's colour arithmetic, as fxMaterial's: the code below runs after three's colorspace_fragment, on the sRGB
// output values, so the game's gamma-space blends are made on gamma values. The canvas is transparent over the stage's
// CSS colour (premultiplied compositing: shown = rgb + stage x (1 - alpha)), which decides each alpha written.
// three keys a compiled program by onBeforeCompile's source text (Material.customProgramCacheKey's default), and a clone
// (a part's own copy, alphatimer.js) carries only onBeforeCompile: so each blend below has its own literal function, never
// one made by a shared helper from a string, or two blends would share one program.
export default function register(api) {
  const { THREE } = api;
  if (!api.shader) { console.warn("particles.js: api.shader missing (index.html), the Offset / 205 shaders draw as fxMaterial's"); return; }
  // fxMaterial's material basics: a transparent, unlit, double-sided particle material with the vertex colours, no depth
  // write (every shader here: ZWrite Off, Cull Off), and the _MainTex as fxMaterial's withMap loads it
  const make = (d, name, blend, opts, inject) => {
    const m = new THREE.MeshBasicMaterial({ vertexColors: true, transparent: true, depthWrite: false, side: THREE.DoubleSide, ...opts });
    if (d.tex) {
      const t = api.texLoader.load(`${api.DATA}fx/tex/${d.tex}.webp`);
      t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping;
      t.repeat.fromArray(d.scale || [1, 1]); t.offset.fromArray(d.offset || [0, 0]);
      m.map = t;
    }
    m.onBeforeCompile = inject;
    m.name = name; m.userData.fxBlend = blend;
    return m;
  };
  // Unity's "Offset factor, units" = GL's polygonOffset (the same mechanism: units x the depth buffer's smallest step;
  // -20000 brings the mark about half a metre nearer at the page's depth range, so it draws over the hero it sits in)
  const offset = units => ({ polygonOffset: true, polygonOffsetFactor: 0, polygonOffsetUnits: units });

  // ---- Particles/Multiply (205) and Particles/MultiplyOffset. Stage 1 combine texture * primary, stage 2 previous
  // lerp(previous) constant (1, 1, 1, 1): colour = lerp(white, texture x vertex colour, their alpha); Blend Zero SrcColor
  // (what is drawn x colour: white leaves it, darker darkens), ZWrite Off, Cull Off, Fog white (the page has no fog),
  // MultiplyOffset also Offset 0, -1. No _TintColor in either (a saved one is a leftover). As fxMaterial's multiply2 and
  // mesh.js's FX/DistortGlass: over the hero or another effect the page multiplies exactly that; over empty canvas there
  // is nothing to multiply, so the alpha carries the darkening (alpha = 1 - the colour's luminance, alpha blended One /
  // One so a drawn pixel stays opaque): shown = stage x luminance. APPROXIMATED as multiply2: over the empty canvas the
  // darkening is grey, not coloured
  // (one function for both: they are one shader apart from the Offset, which is GL state, not program text)
  const MULTIPLY = sh => { sh.fragmentShader = sh.fragmentShader.replace("#include <dithering_fragment>", "#include <dithering_fragment>"
    + "\n\tgl_FragColor.rgb = mix(vec3(1.0), gl_FragColor.rgb, clamp(gl_FragColor.a, 0.0, 1.0));"
    + "\n\tgl_FragColor.a = clamp(1.0 - dot(gl_FragColor.rgb, vec3(0.2126, 0.7152, 0.0722)), 0.0, 1.0);"); };
  const multiply = extra => (d, name) => make(d, name, d.blend, {
    blending: THREE.CustomBlending, blendEquation: THREE.AddEquation, blendSrc: THREE.ZeroFactor, blendDst: THREE.SrcColorFactor,
    blendSrcAlpha: THREE.OneFactor, blendDstAlpha: THREE.OneFactor, ...extra }, MULTIPLY);
  api.shader("multiply", multiply({}));
  api.shader("shader:Particles/MultiplyOffset", multiply(offset(-1)));

  // ---- Particles/AlphaOffset. Stage 1 texture * primary, stage 2 previous * previous alpha, previous alpha: rgb =
  // texture x vertex colour x a, alpha = a (a = texture alpha x vertex alpha); Blend SrcAlpha OneMinusSrcAlpha, so the
  // colour lands as rgb x a^2 over what is drawn x (1 - a); ZWrite Off, Cull Off, Offset 0, -20000, no _TintColor (so no
  // doubling: the saved tint, where there is one, is not the shader's). The page: three's normal blending (not
  // premultiplied: SrcAlpha / OneMinusSrcAlpha for the colour, One / OneMinusSrcAlpha for the alpha), the colour x a in
  // the fragment. Over the canvas the compositing then shows rgb x a^2 + stage x (1 - a), the game's blend, and no
  // channel runs above the alpha (rgb x a^2 <= a). ColorMask RGB is not drawn: three has only colorWrite for all four
  // channels at once, and the canvas needs the alpha written for the mark to show over the stage at all
  api.shader("shader:Particles/AlphaOffset", (d, name) => make(d, name, d.blend, { blending: THREE.NormalBlending, ...offset(-20000) },
    sh => { sh.fragmentShader = sh.fragmentShader.replace("#include <dithering_fragment>", "#include <dithering_fragment>"
      + "\n\tgl_FragColor.rgb *= gl_FragColor.a;"); }));

  // ---- Particles/AdditiveOffset. Stage 2 previous * previous alpha, Blend One OneMinusSrcColor: Unity's Additive (Soft)
  // combine, so fxMaterial's "addsoft" exactly (white colour, opacity 1, rgb x alpha by three's premultiplied_alpha
  // chunk, alpha written = the brightest channel so the added light shows over the CSS stage), plus Offset 0, -20000;
  // ColorMask RGB as AlphaOffset's (the alpha is the page's canvas trick, not the game's)
  api.shader("shader:Particles/AdditiveOffset", (d, name) => make(d, name, d.blend, {
    blending: THREE.CustomBlending, premultipliedAlpha: true, blendEquation: THREE.AddEquation,
    blendSrc: THREE.OneFactor, blendDst: THREE.OneMinusSrcColorFactor, blendSrcAlpha: THREE.OneFactor, blendDstAlpha: THREE.OneMinusSrcAlphaFactor,
    ...offset(-20000) }, sh => { sh.fragmentShader = sh.fragmentShader.replace("#include <dithering_fragment>", "#include <dithering_fragment>"
      + "\n\tgl_FragColor.a = max(gl_FragColor.r, max(gl_FragColor.g, gl_FragColor.b));"); }));
}
