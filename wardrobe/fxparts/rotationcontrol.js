// wardrobe/fxparts/rotationcontrol.js: BB's generic rotationControl script (agent robots, 2026-11-13; plans/fx_mole/parts.md
// part 5 and its "Who builds what" row B, the loader comment above FX_PART_FILES in index.html). Used by the Mole's
// flameCarnival_fire/fire_ctrl ((0, 180, 0), false: its three flame jets turn half a turn a second about the node's own y)
// and the Monkey's lavu. Lines are D:\12tails\DecompiledSource\rotationControl.cs (opaque predicates worked by hand).
//   fields  mRotation_x, mRotation_y, mRotation_z (degrees a second), useWorldRotation (:75-84; wardrobe_fx.py LAYOUTS)
//   Start   start = transform.rotation (world, :20-22)
//   Update  useWorldRotation: rotation = start x Euler(dt x (x, y, z)) (:38: a one-frame offset from the start each frame,
//           a jitter, not a spin: kept as the game has it); else transform.Rotate(dt x (x, y, z)) (:47: Space.Self,
//           rotation = rotation x Euler(..), accumulating)
// Inside the effect's mirror group the numbers are Unity's; Unity's Euler turns z, then x, then y = three's "YXZ".

export default function register(api) {
  const { THREE } = api;
  const D = Math.PI / 180;
  api.part("rotationControl", (fx, node, c) => {
    const v = [c.mRotation_x || 0, c.mRotation_y || 0, c.mRotation_z || 0];
    const e = new THREE.Euler(0, 0, 0, "YXZ"), q = new THREE.Quaternion();
    let start = null;                                  // the world rotation at Start (the first update: a bone cue has placed the root by then)
    return { node, update(dt) {
      q.setFromEuler(e.set(dt * v[0] * D, dt * v[1] * D, dt * v[2] * D, "YXZ"));
      if (!c.useWorldRotation) { node.quaternion.multiply(q); return; }
      start ||= fx.uQuat(node);
      // world = start x E, written as the local rotation under the node's parent (its world now)
      node.quaternion.copy(fx.uQuat(node.parent).invert().multiply(start).multiply(q));
    } };
  });
}
