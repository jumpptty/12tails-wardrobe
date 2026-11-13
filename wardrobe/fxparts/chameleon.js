// wardrobe/fxparts/chameleon.js: the Chameleon's own effect scripts (agent chameleon, 2026-11-13; plans/fx_chameleon/parts.md
// parts 1-2 with its Verification 1 and 3, attacks_emotes.md "Parts needed" P1, skills_a.md "Parts" 5 + Verification 2,
// skills_b.md item 6 P2 + Verification 4, the overnight decisions plans/fx_chameleon/decisions.md 22, 23, 30, 43, 48, 50,
// 51, 55, 56, and the loader comment above FX_PART_FILES in index.html). BB's DecompiledSource is the authority for every
// line cited here (D:\12tails\DecompiledSource\<file>); the prefab facts are checks/fx_chameleon_research/parts/probe.txt.
//   Chameleon_nAttack       nAttack, clearArrow: every Combo / Left Stride / Double Strider arrow: the worn arrow copied,
//                           40 m/s, its end (life, floor, the target body), Fatal Strike's blood on it (fatal); Clear
//                           Arrow's worn-arrow mesh in its own FX/Invisible material
//   Chameleon_needlePrison  needlePrison: 16 needlePrison_arrow, one every 0.05 s, on its ring
//   fx:doubleStrider_left / fx:doubleStrider_right   the Double Strider clone moved by the hero's code (strafe + to)
// Chameleon_campFire (campFire1 / 2) draws nothing (its Update heals sitting allies and ends the fire at its timer,
// Chameleon_campFire.cs:52-183; the cue's kill does that): no part; its 4-byte layout is the extractor's.
// Space: every root here hangs in the effect's mirror group (Unity's world, the hero's feet at the origin, +z her facing,
// y 0 the floor), so node.position is the game's transform.position and the numbers below are the game's own.
//
// The target (Bat decisions 3-4, Chameleon decision 23): the standard body, a CharacterController (centre (0, 0.6, 10) =
// the cue's `to`, height 1, radius 0.3: its capsule's axis is the centre +- 0.2 m; AABB x +-0.3, y 0.1..1.1, z 9.7..10.3).
//
// Page hooks used: api.propModel(slot) (index.html, the lead's Interfaces 1: a fresh Object3D of the piece worn in that
// slot, its weapon_fx particles along, root at 0 / identity / the prefab's scale, userData.rootMesh = { geometry, maxY } or
// null; null when the slot is empty); api.propModel({ item }) for the starter arrow when nothing is worn (decision 50), if
// the page takes that form; api.worn("R"); api.spawn(name, at, opts) with opts.followNode / opts.local (index.html fxSpawn);
// node.userData.fxStatic (mesh.js's StaticMesh: the clear arrow's mesh); fx.cutAt / api.FX.t (the cue's cut, clip time);
// an emitter's dispose() (index.html Fx.dispose, which runs before its geometry sweep).

export default function register(api) {
  const { THREE, V } = api;
  const STEP = 0.02;                                   // Unity's fixed timestep (FixedUpdate, 50 per second)
  const DEG = Math.PI / 180;
  const warned = new Set();
  const warnOnce = (k, ...m) => { if (!warned.has(k)) { warned.add(k); console.warn(...m); } };
  // Quaternion.Euler(x, y, z) in Unity's numbers: z, then x, then y (three's intrinsic "YXZ", as a cue's rot)
  const euler = (x, y, z) => new THREE.Quaternion().setFromEuler(new THREE.Euler(x * DEG, y * DEG, z * DEG, "YXZ"));
  // a quaternion back to a cue's rot (Unity Euler degrees, "YXZ"): what api.spawn's opts.local.rot takes
  const eulerOf = q => { const e = new THREE.Euler().setFromQuaternion(q, "YXZ"); return [e.x / DEG, e.y / DEG, e.z / DEG]; };
  const vec = (a, dflt) => (Array.isArray(a) && a.length >= 3 ? V(+a[0] || 0, +a[1] || 0, +a[2] || 0) : dflt.clone());
  const spawn = (who, name, at, opts) => {
    if (!api.spawn) { warnOnce("spawn", `effect part ${who}: no api.spawn (index.html):`, name, "not drawn"); return null; }
    const f = api.spawn(name, at, opts);
    if (!f) warnOnce("miss:" + name, `effect part ${who}: ${name} not in fx.json (the entry's "builds")`);
    return f;
  };

  // ---------------------------------------------------------------- Chameleon_nAttack (nAttack, clearArrow)
  // Awake (Chameleon_nAttack.cs:21-38): rigidbody.velocity = TransformDirection(0, 0, 30) (:34): along its spawn rotation
  // (RPC_nAttack_fire's LookRotation(fireDir), Chameleon.cs:8473; RPC_clearArrow_fire :9009: the cue's rot). Init (:74-325):
  // Bow Mastery #401 sets TransformDirection(0, 0, 40) (:94-100): 40 m/s with the passives on (parts.md Q6; fx.at.speed
  // overrides). FixedUpdate (:46-66): clock += dt, Destroy at ProjectileControl.life (:53-62) = (0.4 + 0.1 x Far Reach 4) x
  // rangeMod 1 = 0.8 s (Chameleon.cs:8482, :9018; CharacterControl.cs:154). Rigidbody: no gravity, rotation frozen.
  // The end (OnTriggerEnter, :336-400, the ground counts; decisions 22, 23, 55): the arrow goes when its root reaches the
  // floor (y 0) going down: the Normal Attack's untargeted shot at the 10 m ground point, 9.1241 m / 40 m/s = 0.2281 s;
  // with a cue `to` (the target body's centre), in the first 0.02 s step whose trigger BoxCollider (size 0.3 x 0.3 x 1.5,
  // centre (0, 0, 1): local z 0.25 .. 1.75, probe.txt) overlaps the body: 0.18 s after the spawn from (0, 1.5, 1) at
  // (0, 0.6, 10) (parts/calc.txt), Left Stride's shot + 0.174 s continuous (skills_a Verification 2: the hit cues there).
  // APPROXIMATED: the box against the capsule by points along its centre line every 0.05 m, a hit within 0.45 m (0.3 + half
  // the box's 0.3 width) of the capsule's axis (as calc.py / box_hit2.py); the test on the 0.02 s grid from the spawn (the
  // game's own steps are on its global fixed clock, up to one step apart); the floor and the life on the frame clock.
  // The look, nClearLv == 0 (nAttack, :106-260): Instantiate(weapon == "w_chm25" ? mWep1 : mWep2) (:114-128), parent the
  // projectile, localPosition 0, localRotation Euler(0, 270, 270) (:140-150: the model's +y onto the flight's +z), every
  // renderer on (:155-182). mWep2 = the right-hand piece, the arrow = the page's slot L (ChameleonEquipment.cs:1712-1715);
  // with the Snooker set (w_chm25 = snookerBall R + snookerCue L) the ball, slot R. Nothing worn: the starter noviceArrow
  // (w_chm1), the projectile only (decision 50).
  // Fatal Strike (fx.at.fatal, decision 43: the skill's charges; the Combo tile has none): Instantiate(fatalStrike,
  // Vector3.zero, Quaternion.identity) (:205), parent = the copy (:212: the world pose kept), localPosition (0,
  // mesh.bounds.max.y - 0.1, 0) of the copy root's MeshFilter mesh (:215-233), or (0, 0.8, 0) when that mesh is null
  // (:241), localScale 1 (:247). Its turn stays world identity (parts.md Verification 3): local.rot = the inverse of the
  // arrow's spawn turn (for the 10 m shot's rot [9.4623, 0, 0], [-9.4623, 0, 0]); its spot is the copy's local point, so
  // the copy's scale counts. The page rides it on the projectile root (the copy hangs there at a fixed local pose).
  // APPROXIMATED: (0, 0.8, 0) also when the copy root has no MeshFilter at all, where the game breaks out (:222-224) and
  // leaves the blood at its world spawn point (the map's origin: a quirk not drawn); the blood's own scale is its spawned
  // 1 (Unity: localScale 1 under the copy, so the copy's scale too; every Chameleon arrow's prefab scale is 1).
  // The look, nClearLv != 0 (clearArrow, :272-318): the child "arrow" (:274), for her own team (:283, the page's view,
  // decision 51) its MeshFilter's mesh = mWep2's root MeshFilter sharedMesh (:287-305), when both exist: the node keeps its
  // own FX/Invisible material (another part file's api.shader) and its own rotation (0.5, -0.5, -0.5, 0.5) (the same +y ->
  // +z turn, parts/mesh_probe.txt); never Fatal Strike's child (the clear branch skips it, parts.md "Read this first" 9).
  // The shared mesh is drawn by one THREE.Mesh per material pass on the arrow node (the pass order kept by renderOrder),
  // the node's own mesh hidden; they are taken off the node in dispose(), so Fx.dispose's sweep never frees the prop
  // data's geometry (Interfaces 1: share, don't dispose).
  const ARROW_SPEED = 40, ARROW_LIFE = 0.8;
  const BOX_Z0 = 0.25, BOX_Z1 = 1.75, BOX_DZ = 0.05, BOX_REACH = 0.3 + 0.15;
  const BODY_HALF = 0.2;                               // the capsule's axis: centre +- (height / 2 - radius)
  const COPY_TURN = euler(0, 270, 270);
  const STARTER = "noviceArrow";
  const onAxis = V(), probe = V();
  const toAxis = (p, c) => p.distanceTo(onAxis.set(c.x, Math.min(c.y + BODY_HALF, Math.max(c.y - BODY_HALF, p.y)), c.z));
  const boxHits = (pos, fwd, c) => {
    for (let z = BOX_Z0; z <= BOX_Z1 + 1e-9; z += BOX_DZ) if (toAxis(probe.copy(pos).addScaledVector(fwd, z), c) <= BOX_REACH) return true;
    return false;
  };
  // the worn piece's copy; the starter arrow when the slot is empty (decision 50)
  const model = (fx, slot) => {
    if (typeof api.propModel !== "function") {
      warnOnce("propModel", "effect part Chameleon_nAttack: no api.propModel (index.html, parts.md Interfaces 1): the arrow is not drawn");
      return null;
    }
    let m = null;
    try { m = api.propModel(slot); } catch (e) { warnOnce("pm:" + slot, "effect part Chameleon_nAttack: api.propModel", slot, e); }
    if (!m) try { m = api.propModel({ item: STARTER }); } catch (e) { m = null; }
    if (!m) warnOnce("pmnone:" + fx.name, "effect part Chameleon_nAttack: no model for slot", slot, "nor", STARTER, "(", fx.name, ")");
    return m || null;
  };
  api.part("Chameleon_nAttack", (fx, node, comp, mat, nodeDef, data) => {
    // the clear branch: the prefab with the child "arrow" (clearArrow; nAttack has no child, probe.txt)
    const at = fx.at || {}, clear = fx.name === "clearArrow" || !!data?.effects?.[fx.name]?.nodes?.some(n => n.name === "arrow");
    const q0 = fx.uQuat(node);                         // the spawn rotation (the cue's rot), in Unity's world
    const fwd = V(0, 0, 1).applyQuaternion(q0);
    const speed = at.speed != null && at.speed !== "" && Number.isFinite(+at.speed) ? +at.speed : ARROW_SPEED;
    const p0 = node.position.clone(), vel = fwd.clone().multiplyScalar(speed);
    const to = Array.isArray(at.to) ? vec(at.to, V(0, 0.6, 10)) : null;
    const stepPos = V();
    let t = 0, k = 0, started = false, copy = null, swapped = [], hidden = null;

    if (!clear) {
      const slot = at.slot || (api.worn?.("R") === "snookerBall" ? "R" : "L");
      copy = model(fx, slot);
      if (copy) {
        copy.position.set(0, 0, 0);
        copy.quaternion.copy(COPY_TURN);
        node.add(copy);
        copy.updateMatrix();
      }
    }
    // the first frame: the clear arrow's mesh swap (mesh.js builds the arrow node's StaticMesh after this root's parts),
    // Fatal Strike's spawn (after this effect is on the stage and in FX.live, so it follows this frame's move)
    const start = () => {
      started = true;
      if (clear) {
        const arrow = fx.nodes.find(o => o.name === "arrow");
        const mine = arrow?.userData?.fxStatic;
        if (!arrow || !mine) { warnOnce("clearmesh", "effect part Chameleon_nAttack: clearArrow has no arrow mesh (mesh.js StaticMesh)"); return; }
        const src = model(fx, at.slot || "L");       // mWep2's root MeshFilter (:290): the arrow piece, slot L
        const rm = src?.userData?.rootMesh;
        if (!rm?.geometry) return;                     // no root mesh: the prefab's own arrow mesh stays
        const passes = [].concat(mine.material).filter(Boolean);
        passes.forEach((m, i) => {
          const o = new THREE.Mesh(rm.geometry, m);
          o.frustumCulled = false; o.renderOrder = (mine.renderOrder || 0) + i;
          o.layers.mask = mine.layers.mask;
          arrow.add(o); swapped.push(o);
        });
        hidden = mine; mine.visible = false;
        return;
      }
      if (at.fatal && copy) {
        const maxY = copy.userData?.rootMesh?.maxY;
        const local = V(0, Number.isFinite(maxY) ? maxY - 0.1 : 0.8, 0).applyMatrix4(copy.matrix);   // the copy's local point, its scale too
        spawn("Chameleon_nAttack", "fatalStrike", {}, { followNode: node, local: { pos: [local.x, local.y, local.z], rot: eulerOf(q0.clone().invert()) } });
      }
    };

    return {
      node,
      update(dt) {
        if (!started) start();
        t += dt;
        if (t >= ARROW_LIFE) return "destroy";         // clock >= life (:53-62)
        if (to) {                                      // the trigger, after each physics step (OnTriggerEnter :336-400)
          while ((k + 1) * STEP <= t + 1e-9) {
            k++;
            if (boxHits(stepPos.copy(p0).addScaledVector(vel, k * STEP), fwd, to)) { node.position.copy(stepPos); return "destroy"; }
          }
        }
        node.position.copy(p0).addScaledVector(vel, t);
        if (vel.y < 0 && node.position.y <= 0) return "destroy";   // met the floor (decision 22)
        node.updateMatrixWorld(true);                  // the parts after this one this frame (Fatal Strike's follow) see the move
      },
      dispose() {
        for (const o of swapped) o.parent?.remove(o);  // the prop data's geometry: not freed by Fx.dispose's sweep
        swapped = [];
        if (hidden) hidden.visible = true;
      },
    };
  });

  // ---------------------------------------------------------------- Chameleon_needlePrison (needlePrison)
  // The look (CharacterControl.cs:36622-36650): needlePrison at the target's feet, Quaternion.identity (:36629), parented
  // to it, Init(Clamp(2 x mChar.radius, 0.5, 2)) (:36650) = 0.6 m on the standard body (fx.at.r; `radius` too). Init(nRadius)
  // (Chameleon_needlePrison.cs:23-25), its state machine (:144-213): i = 0 (:205); while i < 16 (:172): pos =
  // transform.position + Math.rotateH(nRadius x Vector3.forward, 67.5 i) (:187; Math.cs:840-841: x = -r sin a, z = r cos a),
  // Instantiate(mPrisonArrow, pos, LookRotation(Vector3.up)) (:192; = Euler(-90, 0, 0)), parent = the prison (:197: the world
  // pose kept), Yield(0.05) (:211), i++ (:158): one needle every 0.05 s from 0 to 0.75 s, at 0, 67.5, 135 ... degrees (three
  // turns filling 16 points 22.5 degrees apart). They go with the prison (followNode: the status end's Destroy by name,
  // CharacterControl.cs:16558-16570; the cue's kill 5, decision 25). The world forward / up are taken in the prison's own
  // space at its spawn (identity in the cue: the same numbers). APPROXIMATED: the needles on the effect's own frame clock
  // (the game's coroutine yields on its frame clock too, so up to a frame late each).
  const NEEDLES = 16, NEEDLE_EVERY = 0.05, NEEDLE_TURN = 67.5, NEEDLE_UP = euler(-90, 0, 0);
  api.part("Chameleon_needlePrison", (fx, node) => {
    const at = fx.at || {};
    const r = Number.isFinite(+at.r) && at.r != null ? +at.r : Number.isFinite(+at.radius) && at.radius != null ? +at.radius : 0.6;
    const qi = fx.uQuat(node).invert();               // world -> the prison's local (its parenting keeps the world pose)
    let i = 0, t = 0;
    return { node, update(dt) {
      if (i >= NEEDLES) return;
      t += dt;
      for (; i < NEEDLES && i * NEEDLE_EVERY <= t + 1e-9; i++) {
        const a = NEEDLE_TURN * i * DEG;
        const pos = V(-r * Math.sin(a), 0, r * Math.cos(a)).applyQuaternion(qi);
        spawn("Chameleon_needlePrison", "needlePrison_arrow", {}, { followNode: node,
          local: { pos: [pos.x, pos.y, pos.z], rot: eulerOf(qi.clone().multiply(NEEDLE_UP)) } });
      }
    } };
  });

  // ---------------------------------------------------------------- fx:doubleStrider_left / fx:doubleStrider_right
  // Double Strider #423's clone (doubleStrider_left / _right, at the hero with her rotation: Chameleon.cs:27137-27207,
  // :28523-28547), moved by the hero's coroutine every FixedUpdate: doubleStrideLeft (:27725-27795): if tPos != zero
  // LookAt(vFlat(tPos) + up x the clone's y) (:27769), then Translate((runSpeed + 1) x transform.right x Time.deltaTime,
  // Space.World) (:27775); doubleStrideRight (:29026-29212) the same with x -1 (:29162-29168). runSpeed = 0.01 x (400 + 2
  // AGI - 4 weight) = 4.02 at the page's stats (CharacterDataClass.cs:979, CharacterControl.cs:1458), so the cue's `strafe`
  // is +5.02 (Left Stride) / -5.02 (Right Stride) m/s along the clone's own right (decision 30); `to` = the point it faces
  // ([0, 0, 10], the target). It moves until the cue's followState cut (the standby, 2.298 s) or its EffectControl's end.
  // The steps as the clip researchers' stride sims (skills_a stride_sim.py, verify_b_eo stride502.py), whose shot spots the
  // cues use: the first at the spawn, then every 0.02 s; the position held between steps (no interpolation, as Translate in
  // FixedUpdate). APPROXIMATED: the steps on the effect's own 0.02 s grid from its spawn (the game's on its global fixed
  // clock), the cut tested per step on the spawn's clip time plus the step's age.
  const strider = (fx, node) => {
    if (fx.cls !== "chameleon") return null;
    const at = fx.at || {}, strafe = +at.strafe || 0;
    const to = vec(at.to, V(0, 0, 10));
    const look = new THREE.Matrix4(), up = V(0, 1, 0), flat = V(), right = V();
    let next = 0, t0 = null, done = false;
    const cut = age => (fx.cutAt != null && t0 + age >= fx.cutAt) || (fx.ec && age >= fx.ec.life);
    return { node, update() {
      if (done) return;
      if (t0 == null) t0 = api.FX.t - fx.age;          // the spawn's time on the playing step's clock
      if (fx.stopped) { done = true; return; }
      while (next <= fx.age + 1e-9) {
        if (cut(next)) { done = true; return; }
        if (to.x || to.y || to.z) {                    // tPos != Vector3.zero
          flat.set(to.x, node.position.y, to.z);
          if (flat.distanceToSquared(node.position) > 1e-12) {   // Transform.LookAt (forward to the point, world up)
            look.lookAt(flat, node.position, up);      // three's Matrix4.lookAt(eye, target, up) points +z from target to eye
            node.quaternion.setFromRotationMatrix(look);
          }
        }
        if (strafe) node.position.addScaledVector(right.set(1, 0, 0).applyQuaternion(node.quaternion), strafe * STEP);
        next += STEP;
      }
      node.updateMatrixWorld(true);
    } };
  };
  api.part("fx:doubleStrider_left", strider);
  api.part("fx:doubleStrider_right", strider);
}
