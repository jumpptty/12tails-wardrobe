// wardrobe/fxparts/doubletexture.js: the game's Self-Illumin/DoubleTexture on an effect mesh (2026-11-13, the Chameleon:
// plans/fx_chameleon/parts.md part 5, decisions.md 57). Thunder Dragon's skeleton (thunderDragon_ring2's
// thunderDragon_skeletons, a 2,645-vertex dragon skeleton on node thunderDragon_skeleton_tri); the Rabbit's
// rabbit_stickygum later. Through api.shader, so mesh.js's material() (fxMaterial, api.shaders) gets it: mesh.js unedited.
// Shader (compiled in BB's sharedassets7.assets, checks/fx_chameleon_research/parts/shaders.txt:362-373; the rip's
// DoubleTexture.shader:1-11 is the same): one SubShader, one Pass, no Tags (Queue Geometry), no Blend, no Lighting, ZWrite
// and Cull at their defaults (on, Back): SetTexture [_MainTex] { combine texture * texture }: colour = the texel squared,
// alpha = texel alpha squared but never blended (opaque). _Color (default white; thunderDragon_skeletons' 0.784) is
// declared and never read. Fallback "Diffuse".
// The page: an unlit MeshBasicMaterial with the map, opaque (transparent false: the opaque list, alpha 1 on the canvas),
// depthWrite on, FrontSide (inside the mirror group three's front faces are Unity's, mesh.js). After map_fragment the
// colour is the texel squared AS A GAMMA VALUE, as the game's gamma-space combiner makes it: three hands the shader the
// decoded (linear) texel, so it is encoded back (three's own sRGBTransferOETF), squared, and decoded again (the sRGB
// curve's inverse); three's output encoding then writes g^2. (Squaring the linear texel instead would hold for a pure
// 2.2 power, (g^2.2)^2 = (g^2)^2.2, but three's sRGB curve is piecewise: up to 7.4 / 255 too dark at mid-dark texels, 169
// of the 256 levels off by more than one step; checks/fx_chameleon_build/shaders/probe.txt.) Alpha 1. No uniform of its
// own: one program for every DoubleTexture material (customProgramCacheKey). A material with no texture (none in the
// data) draws white (the property's default "" taken as white).
// APPROXIMATED: the scene's fog is not applied (the page has none); the combiner's 8-bit rounding
export default function register(api) {
  const { THREE, texLoader, DATA } = api;
  const texture = d => {
    const t = texLoader.load(`${DATA}fx/tex/${d.tex}.webp`);
    t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping;
    t.repeat.fromArray(d.scale || [1, 1]); t.offset.fromArray(d.offset || [0, 0]);
    return t;
  };
  api.shader("shader:Self-Illumin/DoubleTexture", d => {
    const m = new THREE.MeshBasicMaterial({ transparent: false, depthWrite: true, side: THREE.FrontSide });
    if (d.tex) m.map = texture(d);
    m.onBeforeCompile = sh => {
      sh.fragmentShader = sh.fragmentShader.replace("#include <map_fragment>", `#include <map_fragment>
#ifdef USE_MAP
	{   // DoubleTexture: combine texture * texture, in gamma space (the game's), then back to linear for three's output
		vec3 dtG = sRGBTransferOETF( vec4( sampledDiffuseColor.rgb, 1.0 ) ).rgb;
		dtG *= dtG;
		diffuseColor.rgb = diffuse * mix( pow( ( dtG + vec3( 0.055 ) ) / 1.055, vec3( 2.4 ) ), dtG / 12.92, vec3( lessThanEqual( dtG, vec3( 0.04045 ) ) ) );
	}
#endif
	diffuseColor.a = 1.0;   // DoubleTexture: no Blend, opaque`);
    };
    m.customProgramCacheKey = () => "fxDoubleTexture";
    return m;
  });
}
