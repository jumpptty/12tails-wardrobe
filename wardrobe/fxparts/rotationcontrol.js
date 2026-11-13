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

  // Rotate (builder "monkey", 2026-11-13; plans/fx_monkey/parts.md part 3, decisions.md 58): an Assembly-UnityScript-
  // firstpass script, not in BB's decompile; its source is Reborn's, DecompiledSource_Reborn/Assembly-UnityScript-firstpass/
  // Rotate.cs:7-9 (fields speed (Vector3, degrees a second; ctor default (10, 15, 19), :13), useWorldSpace) and :17-27
  // (Update: transform.Rotate(speed x dt, useWorldSpace ? Space.World : Space.Self)); BB's 16 bytes match (wardrobe_fx.py
  // LAYOUTS). The Monkey's runicFlame_ring / runicSand_ring magicRune: (0, 0, 180) / (0, 0, 120), Self: the rune spins flat.
  // Self: rotation = rotation x Euler(..) (local, as rotationControl's false branch); World: rotation = Euler(..) x rotation
  // in Unity's world, written under the parent: local = P^-1 x E x P x local (P the parent's world rotation)
  api.part("Rotate", (fx, node, c) => {
    const s = Array.isArray(c.speed) ? c.speed : [10, 15, 19];
    const e = new THREE.Euler(0, 0, 0, "YXZ"), q = new THREE.Quaternion();
    return { node, update(dt) {
      q.setFromEuler(e.set(dt * (s[0] || 0) * D, dt * (s[1] || 0) * D, dt * (s[2] || 0) * D, "YXZ"));
      if (!c.useWorldSpace) { node.quaternion.multiply(q); return; }
      const p = fx.uQuat(node.parent);
      node.quaternion.premultiply(p.clone().invert().multiply(q).multiply(p));
    } };
  });
}
