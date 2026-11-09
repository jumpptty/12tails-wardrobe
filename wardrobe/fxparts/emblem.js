// wardrobe/fxparts/emblem.js: BB's EmblemEmitter (D:\12tails\DecompiledSource\EmblemEmitter.cs; plans/fx_wolf/parts.md
// "EmblemEmitter"), agent A 2026-11-09. Not a 3D emitter: a GUI picture (GUI.DrawTexture in OnGUI) centred on the node's
// point on the screen, its size in screen pixels, fading through five alpha keys, drawn over everything.
// Wolf: holyArmor_ring (holyShield), holySword_ring (holySword), resurrection_ring (resurrection); also valor_emblem.
//
// Drawn here as a THREE.Sprite with sizeAttenuation off (its scale is then a fraction of the view, whatever the
// distance) under the node, so it follows the node and goes with it, and is part of the canvas (screenshots, captures).
// The picture is comp.imageTex, exported by pipeline/wardrobe_fx.py to data/fx/tex/<imageTex>.webp; its pixel size (the
// game multiplies by image.width / image.height, :256-259) is read from the loaded picture, or from comp.imageSize
// [w, h] if the extractor ever stores it (the export keeps the game's pixels: wardrobe_fx.py saves image as it is).

export default function register(api) {
  const { THREE, clamp01, texLoader, camera, DATA } = api;
  const lerp = (a, b, u) => a + (b - a) * u;
  const texs = {};
  const tex = n => {
    if (texs[n]) return texs[n];
    const t = texLoader.load(`${DATA}fx/tex/${n}.webp`);
    t.colorSpace = THREE.SRGBColorSpace;     // GUI.DrawTexture shows the picture's own colours
    return (texs[n] = t);
  };
  // a quad of its own (THREE.Sprite's default geometry is shared by every sprite; Fx.dispose disposes geometries)
  const quad = () => {
    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.Float32BufferAttribute([-.5, -.5, 0, .5, -.5, 0, .5, .5, 0, -.5, .5, 0], 3));
    g.setAttribute("uv", new THREE.Float32BufferAttribute([0, 0, 1, 0, 1, 1, 0, 1], 2));
    g.setIndex([0, 1, 2, 0, 2, 3]);
    return g;
  };
  const v = new THREE.Vector3(), sx = new THREE.Vector3(), sy = new THREE.Vector3();

  api.part("EmblemEmitter", (fx, node, e) => {
    if (!e.imageTex) return null;              // the extractor found no picture
    const map = tex(e.imageTex);
    // GUI.DrawTexture: the GUI's own alpha blending (not additive), GUI.color = white with the ramp's alpha (:129-246);
    // GUI.depth 5 over the 3D view (:120): no depth test, drawn last
    const mat = new THREE.SpriteMaterial({ map, transparent: true, depthTest: false, depthWrite: false, sizeAttenuation: false,
      toneMapped: false, fog: false, side: THREE.DoubleSide });   // DoubleSide: never culled, whatever the mirror's winding
    const s = new THREE.Sprite(mat);
    s.geometry = quad(); s.renderOrder = 1e6; s.frustumCulled = false; s.visible = false;
    node.add(s);
    let t = 0;                                 // Awake: start = Time.time + Delay (:85); here the time since spawn
    return { node, update(dt) {
      t += dt;
      s.visible = false;
      if (t < e.Delay) return;                                    // :103-109
      if (t >= e.Delay + e.Life) return "destroy";                // Destroy(gameObject) (:276-283): the node and its children
      const u = clamp01((t - e.Delay) / e.Life);                  // :114
      // alpha1..alpha5 at 0 / .25 / .5 / .75 / 1 (Mathf.Lerp clamps, :123-246)
      const i = u < .25 ? 0 : u < .5 ? 1 : u < .75 ? 2 : 3;
      mat.opacity = lerp(e["alpha" + (i + 1)], e["alpha" + (i + 2)], clamp01(4 * (u - i * .25)));
      const img = map.image, size = e.imageSize || (img && [img.naturalWidth || img.width, img.naturalHeight || img.height]);
      if (!size || !size[0]) return;                              // the picture is still loading
      // WorldToScreenPoint's z: the distance along the camera's view (:117); not drawn from 40 m on (:247)
      node.updateWorldMatrix(true, false);
      v.setFromMatrixPosition(node.matrixWorld).applyMatrix4(camera.matrixWorldInverse);
      const z = -v.z;
      // Approximation: behind the camera (z <= 0) the game still draws, at the point's flipped screen position; not drawn here
      if (!(z > 0 && z < 40)) return;
      const k = Math.min(1, Math.max(.2, 5 / z));                 // clamp(5 / z, 0.2, 1) (:253)
      // the game: width = image.width x Screen.width / 1024 x lerp(startWidth, endWidth) x k pixels (:84, :256), height the
      // same with image.height and the heights (:259). As a fraction of the view's width / height (camera.aspect = the
      // stage's width / height, Screen.width / Screen.height):
      const fw = size[0] / 1024 * lerp(e.startWidth, e.endWidth, u) * k;
      const fh = size[1] / 1024 * camera.aspect * lerp(e.startHeight, e.endHeight, u) * k;
      // sizeAttenuation off: the sprite spans scale x P[0] (P[5]) of clip space, 2 = the whole view; the node's own world
      // scale is divided out (the game's size ignores the transform's scale)
      const P = camera.projectionMatrix.elements;
      sx.setFromMatrixColumn(node.matrixWorld, 0); sy.setFromMatrixColumn(node.matrixWorld, 1);
      s.scale.set(2 * fw / P[0] / (sx.length() || 1), 2 * fh / P[5] / (sy.length() || 1), 1);
      s.visible = true;
    } };
  });
}
