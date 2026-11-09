// wardrobe/fxparts/groundfollower.js: TTO's GroundFollower (agent F, 2026-11-09; plans/fx_wolf/build_rules.md, tto.md 3).
// Read from TTO's machine code (Ghidra on TTO1102 client/GameAssembly.dll through the Bible's tools/run_ghidra.bat, read
// only; FUN_18030cf20 = expf, identified by running it under unicorn).
//
// Fields (dump.cs, token 0x2000199): smoothing (public; 12 on the Resonance Claw waves), clearance and ready (private).
// - Start@0x2261030: clearance = position.y - GroundHugEmitter.Ground(position, position.y); ready = true.
// - LateUpdate@0x2260ED0 (when ready): g = Ground(position, position.y - clearance);
//   k = clamp01(1 - exp(-smoothing x Time.deltaTime)); position.y += (g + clearance - position.y) x k
//   (x and z untouched): the node keeps its height above the terrain, easing to it at `smoothing` per second.
// - Ground(p, near) = GroundHugEmitter::Ground@0x2263100: a ray from (p.x, near + 12, p.z) straight down, 36 m, layer
//   mask 1, the hit whose y is nearest `near`; no hit -> near.
// On the page the floor is flat at y 0 (the hero's feet; the mirror group's space = Unity's world for the effect), so a
// wave keeps the height it was spawned at: the same as the game on flat ground. Fully reimplemented, nothing
// approximated except the terrain itself (the page has none). Runs after the effect's EffectControl velocity in the
// frame (Fx.update moves the root first), as Unity runs LateUpdate after the move.
export default function register(api) {
  const { V } = api;
  const ground = near => (near + 12 >= 0 && near - 24 <= 0 ? 0 : near);
  api.part("GroundFollower", (fx, node, e, mat, nodeDef) => {
    if (e.enabled === false || nodeDef.active === false) return null;
    let clearance = 0, ready = false;
    const worldPos = () => V().setFromMatrixPosition(fx.uMatrix(node));
    return { node, update(dt) {
      const p = worldPos();
      if (!ready) { clearance = p.y - ground(p.y); ready = true; }            // Start, then this frame's LateUpdate
      const g = ground(p.y - clearance);
      const k = Math.min(1, Math.max(0, 1 - Math.exp(-(e.smoothing ?? 12) * dt)));
      const y = p.y + (g + clearance - p.y) * k;
      if (Math.abs(y - p.y) < 1e-7) return;
      // set the world y back through the parent (Transform.set_position)
      const parentM = node.parent === fx.mirror ? null : fx.uMatrix(node.parent);
      const w = V(p.x, y, p.z), local = parentM ? w.applyMatrix4(parentM.invert()) : w;
      node.position.copy(local);
      node.updateMatrixWorld(true);
    } };
  });
}
