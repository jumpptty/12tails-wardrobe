// wardrobe/fxparts/control.js (agent D, 2026-11-09; plans/fx_wolf/parts.md "EmitterControl", "EffectControl(child)"):
// the game's two timer scripts that switch other parts on and off.
//
// EmitterControl (EmitterControl.cs): Delay / Life / AfterLife over the legacy ParticleEmitter on its OWN node (Start
//   and LateUpdate both use gameObject.GetComponent, :45, so emitters further down are never touched), and Destroy of
//   its node (and so everything under it) at Delay + Life + AfterLife (:101-105).
// EffectControl below an effect's root (EffectControl.cs): the page keeps the root's own EffectControl in class Fx;
//   one further down never gets an owner (CharacterControl.createEffect calls InitEffectControl on the root's only,
//   CharacterControl.cs:24211, and cAttack2 / skySlasher are plain Instantiates), so it runs the no-owner paths:
//   velocity, the followState / followPosition jump to the after-life, the after-life stop of the legacy emitters and
//   ImageEmitters on its node and below, and Destroy at life + afterLife.
// Both work on the page's emitter objects (fx.emitters, each with .node): a "destroy" from update() makes class Fx
// remove this node and everything under it, as the game's Destroy(gameObject).
export default function register(api) {
  const { THREE, V, vA, nz, camera } = api;
  const LEGACY = /ParticleEmitter$/;                       // EllipsoidParticleEmitter, MeshParticleEmitter
  const defOf = (fx, data, o) => data.effects[fx.name]?.nodes[fx.nodes.indexOf(o)];

  // ---------- EmitterControl ----------
  api.part("EmitterControl", (fx, node, c, mat, nodeDef) => {
    // Start (:45-84): no ParticleEmitter on this node = an error in the log and the script disabled (it never destroys)
    if (!nodeDef.comps.some(k => LEGACY.test(k.type))) { console.warn("EmitterControl without a ParticleEmitter", fx.name, node.name); return null; }
    // the page's legacyParticles for this node: class Fx pushes it before it builds the node's components (index.html
    // Fx constructor), so it is this node's first emitter; null when the page does not draw that kind (MeshParticleEmitter):
    // the timer still runs and destroys the node
    const em = nodeDef.comps.some(k => k.type === "EllipsoidParticleEmitter") ? fx.emitters.find(e => e.node === node) : null;
    let warned = false;
    const setEmit = on => {
      if (!em) return;
      if (em.setEmit) return em.setEmit(on);
      if (!on) return em.stop?.();                         // a page without legacyParticles' setEmit: off still works
      if (!warned) { warned = true; console.warn("EmitterControl: legacyParticles has no setEmit(on), cannot switch", node.name, "on"); }
    };
    // Start (:52-64): a Delay turns the emitter off. Built after the emitter and before its first update, as Start runs
    // before the first frame, so a saved emit = true never bursts early
    if (c.Delay > 0) setEmit(false);
    let t = 0;
    return { node, update(dt) {
      // LateUpdate (:98-150). Each branch sets the state every frame it holds (the game sets it whenever it differs, the
      // same thing), so the root's after-life stop inside Delay..Delay + Life is undone the same frame, as in the game
      // (EffectControl.Update turns emit off, this LateUpdate turns it back on)
      t += dt;
      if (t >= c.Life + c.Delay + c.AfterLife) return "destroy";
      if (t >= c.Life + c.Delay) setEmit(false);
      else if (t > c.Delay) setEmit(true);
      // the page updates this after the node's emitter (it was pushed first), so the emitter reacts on the next frame:
      // the game's LateUpdate also runs after that frame's emission
    } };
  });

  // ---------- EffectControl below the root ----------
  const STOPPED = /ParticleEmitter$|^ImageEmitter$/;       // what the after-life stops (EffectControl.cs:430-498)
  api.part("EffectControl", (fx, node, c, mat, nodeDef, data) => {
    // Awake (:69-75): velocity into a world direction once (rotation only), from the node's spawn rotation. "World" here
    // = the effect's Unity space (the mirror group), the hero's own frame; the hero never moves on the page
    const vel = (c.velocity || []).some(x => x) ? vA(c.velocity).applyQuaternion(fx.uQuat(node)) : null;
    let t = 0, stopping = true;                            // stopping = the game's PX4cOk0le2j (true from the constructor, :38)
    const parentQ = () => fx.uQuat(node.parent);           // identity when the parent is the mirror group
    const setWorldQuat = q => node.quaternion.copy(parentQ().invert().multiply(q));
    const under = o => { for (; o; o = o.parent) if (o === node) return true; return false; };
    return { node, update(dt, cam) {
      t += dt;                                             // :164
      if (vel) {                                           // :167-173: transform.position += velocity x deltaTime (world)
        const P = node.parent === fx.mirror ? null : fx.uMatrix(node.parent), w = node.position.clone();
        if (P) w.applyMatrix4(P);
        w.addScaledVector(vel, dt);
        if (P) w.applyMatrix4(P.invert());
        node.position.copy(w); node.updateMatrixWorld(true);   // children drawn later this frame see the move
      }
      if (t >= c.life + c.afterLife) return "destroy";     // :179-189
      if (t < c.life) {
        // :194-210 followState with no owner: straight to the after-life. It takes effect next frame: this frame's
        // branch is already the live one, so with afterLife 0 the next frame destroys the node (cAttack2_dust and
        // skySlasher's DustEmitter, life 60 / afterLife 0 / followState: their one-shot burst is shown for about one
        // frame and gone, as in the game, where they are effectively never seen)
        if (c.followState) t = c.life;
        // :303-416 the rotation modes, no owner
        const mode = c.effectRotationMode;
        if (mode === 0) { if (c.followPosition) t = c.life; }                // normal: :311-326, no owner = the after-life
        else if (mode === 2) {                                                // faceCamera: :372 transform.LookAt(camera)
          const me = V().setFromMatrixPosition(fx.uMatrix(node));
          const f = nz(camera.getWorldPosition(V()).applyMatrix4(fx.mirrorInv).sub(me));
          const x = nz(V().crossVectors(V(0, 1, 0), f));                      // Quaternion.LookRotation(f, up): x = up x f
          if (f.lengthSq() && x.lengthSq())
            setWorldQuat(new THREE.Quaternion().setFromRotationMatrix(new THREE.Matrix4().makeBasis(x, V().crossVectors(f, x), f)));
          // followPosition would then read the missing owner's transform (:381): a NullReferenceException that ends the
          // game's Update there, so nothing more
        } else if (mode === 3) {                                              // faceUp: :398 FromToRotation(forward, vFlat(camera forward))
          const f = nz(V(cam.fwd.x, 0, cam.fwd.z));                           // Math.vFlat (Math.cs:824-827)
          if (f.lengthSq()) setWorldQuat(new THREE.Quaternion().setFromUnitVectors(V(0, 0, 1), f));
          // followPosition: the same missing owner (:407), nothing more
        }
        // followObject (1) and freeze (4) do nothing without an owner (:343-345, :392-394)
      } else if (stopping) {
        // :421-512 once: the legacy ParticleEmitters (emit = false) and ImageEmitters (repeatForever = false) on this
        // node and below (GetComponentsInChildren includes the node itself). Picked by the node's data, then each
        // emitter object of that node gets stop(): approximate only where such a node also carries another kind of
        // emitter with a stop() (that one stops too; none in the Wolf's effects)
        stopping = false;
        for (const e of fx.emitters)
          if (e.stop && under(e.node) && defOf(fx, data, e.node)?.comps.some(k => STOPPED.test(k.type))) e.stop();
      }
    } };
  });
}
