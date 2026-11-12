// wardrobe/fxparts/worldcollider.js: Unity 3.5's built-in WorldParticleCollider (2026-11-13, the Cat: plans/fx_cat/parts.md
// part 5 and its Verification, decisions.md 53). No game source: the 3.5 manual's "World Particle Collider". On a legacy
// emitter's node, each particle moving through a collider on a "Collides With" layer bounces: its velocity reflected on
// the surface normal and multiplied by Bounce Factor ("similar to the Particle Animator's Damping": the WHOLE velocity,
// decision 53, not only the part off the surface), its energy (life left) minus Collision Energy Loss seconds (killed
// below 0), killed when its speed after the hit is under Min Kill Velocity; Send Collision Message is not drawn.
// The Cat's luckyDice (dice) and treasureHunt (coins): bounce 0.5, loss 0, mask 1 (layer 0, the ground), min kill 0
// (checks/fx_cat_research/parts/probe_ps.txt); the Chameleon and the Rabbit reuse it. wardrobe_fx.py stores the
// component's fields as they are, as Light / TrailRenderer ("WorldParticleCollider": m_BounceFactor,
// m_CollisionEnergyLoss, m_CollidesWith {m_Bits}, m_MinKillVelocity, m_SendCollisionMessage).
// The page: the node's legacy emitter (index.html legacyParticles, built before the node's scripts, so it is in
// fx.emitters: e.node === node && e.setEmit) calls its collide(p, world) after each particle's move; a false return
// removes the particle. The test runs in the effect's Unity world (inside the mirror group, the floor at y 0):
// world-space particles as they are, local ones through fx.uMatrix(node) (fxparts/shuriken.js collide() the model).
// APPROXIMATED: the floor (y 0) is the page's only collider (the game's layer 0 also holds walls and props); a particle
// is a point (no size); the hit is taken at the end of the frame's move (the particle put back on the floor), not at
// the crossing; medium sure on the bounce maths (TTO's own conversion of luckyDice keeps the tangential speed:
// Shuriken m_Bounce 0.5, m_Dampen 0; only how far the dice skid differs)
export default function register(api) {
  const { THREE } = api;
  api.part("WorldParticleCollider", (fx, node, c) => {
    const mw = c.m_CollidesWith, bits = typeof mw === "number" ? mw : mw?.m_Bits ?? -1;   // Unity's default: every layer
    if (!(bits & 1)) return null;                                          // layer 0 (the floor) not in the mask
    const e = fx.emitters.find(x => x.node === node && x.setEmit);
    if (!e) { console.warn("WorldParticleCollider: no legacy emitter on its node", fx.name, node.name); return null; }
    const bounce = +(c.m_BounceFactor ?? 0.5), loss = +(c.m_CollisionEnergyLoss ?? 0), minKill = +(c.m_MinKillVelocity ?? 0);
    const W = new THREE.Vector3(), Vw = new THREE.Vector3(), M = new THREE.Matrix4(), Mi = new THREE.Matrix4(),
      L = new THREE.Matrix3(), Li = new THREE.Matrix3();
    // the hit, in the effect's Unity world: false = the particle dies
    const hit = (pw, vw, p) => {
      if (pw.y >= 0 || vw.y >= 0) return null;                             // above the floor, or already leaving it
      pw.y = 0;
      vw.set(vw.x, -vw.y, vw.z).multiplyScalar(bounce);
      p.age += loss;
      return !(vw.length() < minKill || p.age >= p.energy);
    };
    e.collide = (p, world) => {
      if (world) { const r = hit(p.p, p.v, p); return r !== false; }
      // local space: the particle's position and velocity are the node's (legacyParticles moves p.p by p.v in it)
      M.copy(fx.uMatrix(node));
      W.copy(p.p).applyMatrix4(M);
      if (W.y >= 0) return true;
      L.setFromMatrix4(M); Vw.copy(p.v).applyMatrix3(L);
      const r = hit(W, Vw, p);
      if (r === null) return true;
      p.p.copy(W.applyMatrix4(Mi.copy(M).invert()));
      p.v.copy(Vw.applyMatrix3(Li.copy(L).invert()));
      return r;
    };
    return null;                                                           // nothing of its own to update
  });
}
