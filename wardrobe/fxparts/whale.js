// wardrobe/fxparts/whale.js: the Whale's own effect scripts and the hero's code acting on her effects (builder "whale",
// 2026-11-13; plans/fx_whale/parts.md "Each part" 1-4, 6 with its Verification 1, 4, 7, 8, attacks_emotes.md Verification 2
// (the guard's per-slot ticks), the overnight decisions plans/fx_whale/decisions.md 24-26, 37-41, 45, 53, 54, 60, and the
// loader comment above FX_PART_FILES in index.html). BB's DecompiledSource is the authority for every line cited here
// (D:\12tails\DecompiledSource\<file>, every opaque predicate worked by hand); the prefab facts are this build's read-only
// probes (checks/fx_whale_build/whale/probe.json, probe2.json: wardrobe_fx.py --probe, the knights with the LAYOUTS line in
// memory) and, for the colliders and rigidbodies the extractor drops, the BB rip's own prefabs (D:\12tails\RippedAssets\
// ExportedProject\Assets\Resources\gameassets\characters\heroes\whale\effects\javelin / flyingShield / homingShield
// .prefab); the flights checks/fx_whale_build/whale/sim.mjs -> sim.txt, the parts on a mock page parts_test.mjs -> .txt.
//   Whale_javelin         javelin: a copy of the worn lance thrown at 24 m/s under gravity, stuck in the floor, 3 s
//   Whale_flyingShield    flyingShield (node 1, moved by the root's clip): a copy of the worn shield, its 1 m trigger
//   Whale_homingShield    homingShield: a copy of the worn shield, spinning, homing at 12 m/s, a hit on every pass, 3 s
//   whale_kingdomKnight   kingdomKnight1 / kingdomKnight2: the summoned knight: its slot, its rise, Round Table's guard,
//                         its volley (built, never cued), its unsummon
//   fx:grandTide          the hero's code playing the wave's root clip at age 1 and ending it at the release
// Whale_overPresence (overPresence) draws nothing (a 6 m trigger handing enemies a status, Whale_overPresence.cs:56-185):
// no part. The cast ring's restart is bat.js's fx:castRing (the Whale let through its gate, decision 61).
// Space: every root here hangs in the effect's mirror group (Unity's world, the hero's feet at the origin, +z her facing,
// +x her right, y 0 the floor), so node.position is the game's transform.position and the numbers below are the game's own.
//
// The target (decision 60, parts.md Verification 8): ONE body for every part here, the Bat's capsule (bat.js BODY_HALF /
// BODY_R, Bat decision 4): a CharacterController with its centre at the cue's `to` (default (0, 0.6, 10)), height 1,
// radius 0.3, so its axis is the centre +- 0.2 m (y 0.4 .. 0.8) and a sphere of radius r touches it when its centre comes
// within r + 0.3 m of that axis.
//
// Page hooks used: api.propModel(slot, true) (index.html: a fresh Object3D of the piece worn in that slot, its weapon_fx
// particles along, root at 0 / identity / the prefab's scale; nothing worn: the class's starter piece, PROP_STARTER.whale =
// { R: "noviceLance", L: "noviceShield" }, decision 54; null while the slot's list is loading: asked again each frame);
// fx.clipFloor?.(node) (index.html, decision 45: every mesh under node drawn only above the hero's floor; called from an
// update, never in build); api.spawn(name, at) (index.html fxSpawn; an entry's "builds" puts flyingShield_hit /
// kingdomKnight_ring2 in fx.json); node.userData.fxAnim.play(name, fade, wrap) (mesh.js's Animation: Animation.Play, a clip
// already playing is not rewound; wrap = animation.wrapMode set after it: 1 Once, 2 Loop), looked up when a clip is due,
// never at build; fx.cutNow() (followState's end: the root's "destroy" clip and the after-life); fx.stopped; fx.uQuat /
// fx.uMatrix (a node's rotation / matrix in Unity's world).

import { lookEuler } from "./cat.js";

// ---------------------------------------------------------------- the flights' maths (plain [x, y, z] arrays, Unity's
// space), exported for the node probe (checks/fx_whale_build/whale/sim.mjs): the parts below step exactly these
export const STEP = 0.02;                              // Unity's fixed timestep (FixedUpdate, 50 per second)
export const GRAVITY = -9.8;                           // Physics.gravity.y (the PhysicsManager in mainData, cat.js)
export const BODY_HALF = 0.2, BODY_R = 0.3;            // the target's capsule: axis = centre +- 0.2 m, radius 0.3 m (bat.js)
export const BODY_CENTRE = [0, 0.6, 10];               // the standard target body's centre: the default aim
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const unit = a => { const l = Math.hypot(a[0], a[1], a[2]); return l > 0 ? [a[0] / l, a[1] / l, a[2] / l] : [0, 0, 0]; };
// v turned about the unit axis ax by ang (Rodrigues; the same numbers in Unity's left-handed space)
const turnAbout = (v, ax, ang) => {
  const c = Math.cos(ang), s = Math.sin(ang), d = dot(ax, v) * (1 - c), x = cross(ax, v);
  return [v[0] * c + x[0] * s + ax[0] * d, v[1] * c + x[1] * s + ax[1] * d, v[2] * c + x[2] * s + ax[2] * d];
};
// the distance from p to the target body's axis (the capsule's segment: its centre c +- BODY_HALF in height)
export const toBodyAxis = (p, c) => Math.hypot(p[0] - c[0], p[1] - Math.min(c[1] + BODY_HALF, Math.max(c[1] - BODY_HALF, p[1])), p[2] - c[2]);
// Vector3.RotateTowards's direction: the unit vector a turned toward b by at most maxRad (the magnitude dropped: the
// caller's LookRotation normalises it). Its three cases as Unity's own maths library writes them (Vector3.cpp
// RotateTowards / OrthoNormalVectorFast, read in the Unity 4 source; the 3.5 player's build was not disassembled): the
// same direction (dot > 1 - 1e-5): b's; opposite (dot < -1 + 1e-5): about a fixed perpendicular of a, (0, -a.z, a.y) /
// |..| when |a.z| > 1 / sqrt 2, else (-a.y, a.x, 0) / |..|; otherwise about a x b by min(maxRad, the angle between them)
export const rotateTowardsDir = (a, b, maxRad) => {
  const u = unit(a), w = unit(b), d = dot(u, w);
  if (d > 1 - 1e-5) return w;
  if (d < -1 + 1e-5) {
    const k = Math.abs(u[2]) > Math.SQRT1_2 ? 1 / Math.hypot(u[1], u[2]) : 1 / Math.hypot(u[0], u[1]);
    return turnAbout(u, Math.abs(u[2]) > Math.SQRT1_2 ? [0, -u[2] * k, u[1] * k] : [-u[1] * k, u[0] * k, 0], maxRad);
  }
  return turnAbout(u, unit(cross(u, w)), Math.min(maxRad, Math.acos(d)));
};

// Whale_javelin, one FixedUpdate and the physics step after it, on s = { p, v, f (the heading, unit), stuck }:
//   flying: gravity on v (the Rigidbody's, useGravity on), p += v x 0.02, the heading = v's (LookAt(position + velocity),
//     Whale_javelin.cs:165), then the trigger against the ground (OnTriggerEnter, layer 0, :191-198): its BoxCollider is
//     0.25 x 0.25 x 3 with its centre 0.5 m ahead of the node (the rip: from 1 m behind the node to 2 m ahead of it), so its
//     lowest point is the lower of the two ends, less the half height 0.125 x the heading's horizontal part (the box's up
//     axis; its right axis is level, LookAt keeps no roll): at or under y 0 -> stuck, useGravity off
//   stuck: velocity = Lerp(velocity, zero, 24 dt) = x (1 - 24 x 0.02) = x 0.52 (:174), no gravity, p += v x 0.02, the
//     heading kept (:161-165 turns it only while flying)
// APPROXIMATED: Unity's trigger against the terrain's own collider as the box's lowest point reaching the flat floor
// (parts.md "How sure": medium); the heading set after the step's move (the game's LookAt runs before the physics of
// the same step, one step's turn behind: 0.5 degrees).
export const JAVELIN_SPEED = 24, JAVELIN_LIFE = 3, JAVELIN_BRAKE = 24;
export const JAVELIN_BOX = [-1, 2, 0.125];             // the box's ends along the heading from the node, its half height
export const javelinStep = s => {
  const { p, v } = s;
  if (s.stuck) { const k = 1 - JAVELIN_BRAKE * STEP; v[0] *= k; v[1] *= k; v[2] *= k; }
  else v[1] += GRAVITY * STEP;
  p[0] += v[0] * STEP; p[1] += v[1] * STEP; p[2] += v[2] * STEP;
  if (s.stuck) return s;
  s.f = unit(v);
  const low = p[1] + Math.min(JAVELIN_BOX[0] * s.f[1], JAVELIN_BOX[1] * s.f[1]) - JAVELIN_BOX[2] * Math.hypot(s.f[0], s.f[2]);
  if (low <= 0) s.stuck = true;
  return s;
};

// Whale_homingShield.Update on the 0.02 s step (decision 53), on s = { p, f (its forward, unit) }: a =
// RotateTowards(forward, aim - position, 4 dt, 1) (Whale_homingShield.cs:278); rotation = LookRotation(Scale(a, (1, 0.2,
// 1))) (:281: the climb cut to a fifth, renormalised); Translate(12 dt x forward) (:284, along the new forward).
// `nudge` (metres, signed) moves it that far to its own right after the step: see the part for why.
export const HOMING_SPEED = 12, HOMING_TURN = 4, HOMING_FLAT = 0.2, HOMING_LIFE = 3;
export const homingStep = (s, aim, nudge = 0) => {
  const { p } = s, to = [aim[0] - p[0], aim[1] - p[1], aim[2] - p[2]];
  if (Math.hypot(to[0], to[1], to[2]) > 1e-5) {        // (on the aim itself: the heading kept)
    const a = rotateTowardsDir(s.f, to, HOMING_TURN * STEP);
    const f = unit([a[0], HOMING_FLAT * a[1], a[2]]);
    if (f[0] || f[1] || f[2]) s.f = f;
  }
  const f = s.f, d = HOMING_SPEED * STEP;
  p[0] += d * f[0]; p[1] += d * f[1]; p[2] += d * f[2];
  if (nudge) { const h = Math.hypot(f[0], f[2]); if (h > 0) { p[0] += nudge * f[2] / h; p[2] -= nudge * f[0] / h; } }   // right = up x forward
  return s;
};

export default function register(api) {
  const { THREE, V } = api;
  const DEG = Math.PI / 180;
  const ONCE = 1, LOOP = 2;                            // UnityEngine.WrapMode
  const warned = new Set();
  const warnOnce = (k, ...m) => { if (!warned.has(k)) { warned.add(k); console.warn(...m); } };
  const arr = v => [v.x, v.y, v.z];
  // the target body's centre: the cue's `to`, else the standard body's (0, 0.6, 10)
  const target = fx => (Array.isArray(fx.at?.to) && fx.at.to.length >= 3 ? fx.at.to.slice(0, 3).map(x => +x || 0) : BODY_CENTRE.slice());
  // Quaternion.LookRotation(forward, Vector3.up) in Unity's numbers (bat.js's / cat.js's)
  const lookRot = (f, q = new THREE.Quaternion()) => {
    const z = V(f[0], f[1], f[2]).normalize(), x = V().crossVectors(V(0, 1, 0), z);
    if (x.lengthSq() < 1e-12) x.set(1, 0, 0); x.normalize();
    return q.setFromRotationMatrix(new THREE.Matrix4().makeBasis(x, V().crossVectors(z, x), z));
  };
  // Quaternion.Euler(x, y, z) in Unity's numbers: z, then x, then y (three's intrinsic "YXZ", as a cue's rot)
  const euler = (x, y, z) => new THREE.Quaternion().setFromEuler(new THREE.Euler(x * DEG, y * DEG, z * DEG, "YXZ"));
  const spawn = (who, name, at) => {
    if (!api.spawn) { warnOnce("spawn", `effect part ${who}: no api.spawn (index.html):`, name, "not drawn"); return null; }
    const f = api.spawn(name, at);
    if (!f) warnOnce("miss:" + name, `effect part ${who}: ${name} not in fx.json (the entry's "builds")`);
    return f;
  };
  // Animation.Play(name) with the wrap mode the script sets right after it (mesh.js play(name, fade, wrap)); the Animation
  // is looked up now, when the clip is due
  const play = (who, fx, node, name, wrap) => {
    const a = node.userData.fxAnim;
    if (!a?.play) return warnOnce("anim:" + fx.name, `effect part ${who}: no Animation play() on`, fx.name, "(fxparts/mesh.js)");
    if (!a.play(name, 0, wrap)) warnOnce("clip:" + fx.name + name, `effect part ${who}: no clip`, name, "on", fx.name);
  };
  // Instantiate(owner.mWep1 / mWep2) parented to the projectile at local zero and the given local rotation: a fresh copy
  // of the piece worn in the slot (mWep1 = the mount_Hand_L piece, the shield, the page's slot L; mWep2 = mount_Hand_R, the
  // lance, slot R: WhaleEquipment.cs:1645, 1677, 1707-1710), the starter piece with nothing worn (decision 54). Null while
  // the slot's prop list is still loading: the part asks again each frame (said once if still nothing 1 s on)
  const wornCopy = (who, fx, node, slot, turn, age) => {
    if (typeof api.propModel !== "function") { warnOnce("propModel", `effect part ${who}: no api.propModel (index.html): the worn piece's copy is not drawn`); return null; }
    let m = null;
    try { m = api.propModel(slot, true); } catch (e) { warnOnce("pm:" + slot, `effect part ${who}: api.propModel`, slot, e); }
    if (!m) { if (age > 1) warnOnce("pmnone:" + fx.name, `effect part ${who}: no model for slot`, slot, "nor a starter piece (PROP_STARTER.whale, index.html) on", fx.name); return null; }
    m.position.set(0, 0, 0);
    if (turn) m.quaternion.copy(turn); else m.quaternion.identity();
    node.add(m);
    return m;
  };

  // ---------------------------------------------------------------- Whale_javelin (javelin)
  // Whale_javelin.cs: ctor a local velocity (0, 0, 24) (:25); Awake (:37-55): rigidbody.velocity = TransformDirection of it
  // (:50): 24 m/s along the spawn rotation (RPC_javelin_fire's LookRotation(fireDir), Whale.cs:8791-8794: the cue's rot,
  // getTrajectoryVector from hero + (1.2, 2.2, 1) at the target's centre, :22919-22952: [2.878, -7.595, 0]). Init(owner, lv)
  // (:62-136, in the spawn frame): Instantiate(owner.mWep2, zero, identity), parent = the javelin, localPosition zero,
  // localRotation identity (:82-91), every Renderer under it on (:94-108): a copy of the worn lance (the cue's slot, "R").
  // FixedUpdate (:140-182): clock += dt (:147), Destroy at ProjectileControl.life (:150-154; 3 x rangeMod 1,
  // Whale.cs:8803); flying: LookAt(position + velocity) (:165); stuck: velocity = Lerp(velocity, zero, 24 dt) (:174).
  // OnTriggerEnter (:186-205): a layer 0 collider (the ground) -> stuck, useGravity off. OnTriggerStay (:210-325): damage
  // only, every 0.1 s, while flying: it pierces the target, no effect and no destroy, so the body is not tested here (no
  // hit is drawn, decision 24: javelin_hit is never spawned and BB has no such prefab). Its AudioSource (javelin) is the page's.
  // Here: javelinStep on the 0.02 s grid (decision 53), drawn between steps along the next step's velocity; the copy asked
  // for each frame until the page has it, then clipped at the floor once (decision 45: its buried tip). From the cue's
  // (1.2, 2.2, 1): past the body at 0.38 s, into the floor at 0.46 s 11.9 m ahead pitched 13 degrees down, sliding 0.5 m
  // further in as it brakes (sim.txt), standing there to its 3 s.
  api.part("Whale_javelin", (fx, node) => {
    const v0 = V(0, 0, JAVELIN_SPEED).applyQuaternion(fx.uQuat(node));   // TransformDirection at the spawn (:50)
    const s = { p: arr(node.position), v: arr(v0), f: unit(arr(v0)), stuck: false };
    const END = Math.round(JAVELIN_LIFE / STEP), q = new THREE.Quaternion();
    let acc = 0, k = 0, t = 0, copy = null;
    return { node, update(dt) {
      t += dt;
      if (!copy) {
        copy = wornCopy("Whale_javelin", fx, node, fx.at?.slot || "R", null, t);
        if (copy) fx.clipFloor?.(copy);
      }
      acc += dt;
      while (acc >= STEP) {
        acc -= STEP;
        if (++k >= END) return "destroy";              // clock >= life: Destroy (:150-154)
        javelinStep(s);
      }
      const b = s.stuck ? 1 - JAVELIN_BRAKE * STEP : 1;  // the next step's velocity (its gravity left out: 4 mm at most)
      node.position.set(s.p[0] + s.v[0] * b * acc, s.p[1] + s.v[1] * b * acc, s.p[2] + s.v[2] * b * acc);
      node.quaternion.copy(lookRot(s.f, q));
      node.updateMatrixWorld(true);                    // the copy's weapon_fx particles after this part see the move
    } };
  });

  // ---------------------------------------------------------------- Whale_flyingShield (flyingShield, node 1)
  // The root (EffectControl life 1, Animation flyingShield 1 s, AudioSource javelin: all the page's) is made at the hero
  // with her rotation x Euler(270, 90, 0) (Whale.cs:24807: the cue's rot); its clip carries the child `flyingShield` (this
  // part's node: Whale_flyingShield + a trigger SphereCollider radius 1 + a Rigidbody, no gravity) round a 1 s loop 1.36 m
  // up, from the left hand out to 11.98 m ahead and back on the right. Init(owner, lv) (Whale_flyingShield.cs:37-110;
  // Whale.cs:24818-24840): Instantiate(owner.mWep1, position, rotation), parented, localPosition zero, localRotation
  // identity (:96-105): a copy of the worn shield. OnTriggerEnter (:126-215): a Player / Enemy of another layer (not 2):
  // RPC_flyingShield_hit(transform.position, transform.forward) (:199) = flyingShield_hit at the shield,
  // LookRotation(its forward) (Whale.cs:8942-8965), and the hit; no destroy: every entry is a hit.
  // Here: each frame, after the root's Animation posed the node, its Unity position against the target body (the 1 m
  // sphere within 1 + 0.3 m of the capsule's axis); on the frame it enters: flyingShield_hit there. At the standard target
  // it never enters (its closest pass, at 0.44 s, is 1.94 m from the axis = 1.64 m from the body's side, sim.txt): built
  // for the rule, drawn as the game's no-hit at this target (decision 25). APPROXIMATED: the test once a frame, not on the
  // physics steps (the node moves up to 0.6 m a frame at 60 fps).
  const FLY_R = 1;
  api.part("Whale_flyingShield", (fx, node) => {
    const to = target(fx), pos = V(), fwd = V();
    let copy = null, inside = false, t = 0;
    return { node, update(dt) {
      t += dt;
      if (!copy) copy = wornCopy("Whale_flyingShield", fx, node, "L", null, t);
      node.updateWorldMatrix(true, false);
      pos.setFromMatrixPosition(fx.uMatrix(node));
      const now = toBodyAxis(arr(pos), to) <= FLY_R + BODY_R;
      if (now && !inside) {
        fwd.set(0, 0, 1).applyQuaternion(fx.uQuat(node));
        spawn("Whale_flyingShield", "flyingShield_hit", { x: pos.x, y: pos.y, d: pos.z, rot: lookEuler(arr(fwd)) });
      }
      inside = now;
    } };
  });

  // ---------------------------------------------------------------- Whale_homingShield (homingShield)
  // Made at hero + TransformDirection(0, 1, 1), LookRotation(her forward), with the target (RPC_homingShield_fire,
  // Whale.cs:10371-10431, :35194: the cue's y 1, d 1). Init(life, owner, target) (Whale_homingShield.cs:20-180): its end =
  // now + life (:31; chaAdjust(3) = 3 s at CHA 1), the aim = the target's collider.bounds.center (:55, read again each
  // frame :272); Instantiate(owner.mWep1), every MeshRenderer on (:109), parented, localPosition zero, localRotation
  // Euler(0, 0, 90) (:132-135): a copy of the worn shield on its edge. Update (:183-335): past the end ->
  // RPC_homingShield_destroy (draws nothing) and Destroy (:231-249); the turn, the flattening and the move (:278-284:
  // homingStep above); the copy Rotate(1200 dt, 0, 0) about its own x (:324). OnTriggerEnter (:340-430; the root's
  // SphereCollider radius 0.5, Rigidbody without gravity): a Player / Enemy of another layer: the hit, and
  // RPC_flyingShield_hit(position, forward) (:409-418) = flyingShield_hit at the shield, LookRotation(its forward)
  // (Whale.cs:8942-8965). No destroy on contact: it flies on, turns back and hits again on each pass (decision 26).
  // Here: homingStep on the 0.02 s grid (decision 53: the same flight on a long first frame), the aim = the cue's `to`,
  // else the body's centre (0, 0.6, 10); after each step the 0.5 m sphere against the body (its centre within 0.5 + 0.3 m
  // of the capsule's axis): every entry spawns flyingShield_hit; gone on the first step past 3 s. The copy's spin runs on
  // the frame clock from the spawn (also while the page is still loading the piece).
  // The float nudge (APPROXIMATED): on its way in the shield locks onto the line to its aim (a turn smaller than 4 dt
  // lands on it exactly), so it passes dead over the aim's centre and then flies straight away from it; RotateTowards
  // turns it in the plane of its forward and the line back to the aim, which is then upright: the turn is all pitch, and
  // the x 0.2 flattening undoes it. In exact arithmetic the shield flies on level for good (sim.txt, no nudge: one pass,
  // 37 m ahead at 3 s; one pass too at an aim 1 m off her line). That state is unstable: an offset to one side grows 2-5
  // times a step once it is past the body (checks/fx_whale_build/whale/explore2.mjs), so in the game, whose
  // single-precision positions are never exact, the shield swings round to one side or the other, by chance. The page
  // stands in for that rounding with 2e-6 m (float32's rounding of a coordinate of some tens of metres) to its own right
  // or left each step, the side picked at random per throw. With it, from the cue's (0, 1, 1): through the body 0.70 s
  // after the spawn at (0, 0.87, 9.40), the swing round from 1.16 s, 8.8 m past the body at its farthest, and through the
  // body again at 2.52 s from behind and one side (sim.txt; a nudge of 1e-8 .. 1e-4 m moves the second pass over 2.70 ..
  // 2.40 s); gone at 3.02 s.
  const HOMING_R = 0.5, HOMING_NUDGE = 2e-6, SHIELD_TURN = euler(0, 0, 90), SHIELD_SPIN = 1200 * DEG;
  api.part("Whale_homingShield", (fx, node) => {
    const aim = target(fx);
    const s = { p: arr(node.position), f: unit(arr(V(0, 0, 1).applyQuaternion(fx.uQuat(node)))) };
    const nudge = (Math.random() < 0.5 ? -1 : 1) * HOMING_NUDGE;
    const q = new THREE.Quaternion(), spin = new THREE.Quaternion(), X = V(1, 0, 0);
    let acc = 0, k = 0, t = 0, copy = null, inside = false;
    return { node, update(dt) {
      t += dt;
      if (!copy) copy = wornCopy("Whale_homingShield", fx, node, "L", SHIELD_TURN, t);
      if (copy) copy.quaternion.copy(SHIELD_TURN).multiply(spin.setFromAxisAngle(X, (SHIELD_SPIN * t) % (2 * Math.PI)));   // :324
      acc += dt;
      while (acc >= STEP) {
        acc -= STEP;
        if (++k * STEP > HOMING_LIFE + 1e-9) return "destroy";     // Time.time > its end (:231-249)
        homingStep(s, aim, nudge);
        const now = toBodyAxis(s.p, aim) <= HOMING_R + BODY_R;     // OnTriggerEnter, after the move
        if (now && !inside) spawn("Whale_homingShield", "flyingShield_hit", { x: s.p[0], y: s.p[1], d: s.p[2], rot: lookEuler(s.f) });
        inside = now;
      }
      const d = HOMING_SPEED * acc;
      node.position.set(s.p[0] + d * s.f[0], s.p[1] + d * s.f[1], s.p[2] + d * s.f[2]);
      node.quaternion.copy(lookRot(s.f, q));
      node.updateMatrixWorld(true);                    // the copy's weapon_fx particles after this part see the move
    } };
  });

  // ---------------------------------------------------------------- whale_kingdomKnight (kingdomKnight1 / kingdomKnight2)
  // The prefab (probe2.json): the root's Animation (root 1.0 s Loop, the default, playing by itself; nAttack 1.2 s, cAttack
  // 0.5 s, unsummon 1.0 s; none moves the root) + this script; Shrimp_tri (the skinned body), the lance's TrailRenderer.
  // No EffectControl: it lives until its script destroys it (or the cue's kill).
  //   Init(owner, lv, slot) (whale_kingdomKnight.cs:23-150; Whale.cs:28506): the slot's offset (:45-117): 0 (1.6, 0, 1.6),
  //     1 (-1.6, 0, 1.6), 2 (1.6, 0, -1.6), 3 (-1.6, 0, -1.6), 4 (2.2, 0, 0), 5 (-2.2, 0, 0); position = owner +
  //     TransformDirection(offset) - up (:120: 1 m under the floor), rotation = the owner's (:123);
  //     Instantiate(kingdomKnight_ring2, position + up, rotation) (:126-132: on the floor at the slot); state standby (:144).
  //   Update (:163-249): the owner gone -> Destroy (:242); in standby: the owner in "attack" with myCommand "cAttack1" and
  //     Knight of the Deep #273 -> StartCoroutine(knightGuard()) (:202-220); else position = Lerp(position, owner +
  //     TransformDirection(offset), 4 dt), rotation = Lerp(rotation, the owner's, 4 dt) (:229-234): it rises to its slot and
  //     turns back to her facing. No lerp in any other state.
  //   knightGuard (:631-763): only from standby (:740); state guard (:749), WaitForSeconds(0.1 x slot) (:761); then each
  //     pass: the owner still charging (:670-676) -> rotation = LookRotation(vFlat(Random.onUnitSphere)) (:682: a flat
  //     facing, every direction as likely), animation.Play("cAttack"), wrapMode Loop (:687-692), WaitForSeconds(0.5) (:756);
  //     else standby, Play("root"), Loop (:700-710). Play, not Rewind + Play: the script has no Rewind anywhere, so the
  //     looping cAttack is started by the first pass and runs on through the later ones (Animation.Play leaves a playing
  //     clip alone: mesh.js's play()); each pass only turns the knight.
  //   knightAttack(target) (:409-524; from Whale.KingdomKnight() every 3 s on the nearest enemy within 8 m of her,
  //     Whale.cs:9650-9729): only from standby (:489); rotation = LookRotation(vFlat(target - position)) (:498), state
  //     attack (:501), Play("nAttack"), Once (:504-507), 0.5 s, the hit (:439: damage, nothing drawn), 0.5 s, standby,
  //     Play("root"), Loop (:454-464). Never on the page: the target stands 10 m from her (decision 39).
  //   unsummon (:867-915; RPC_kingdomKnight_unsummon, Whale.cs:9827-9868, at the status's end and at a recast): state
  //     unsummon (:899), Play("unsummon"), Once (:902-905), WaitForSeconds(1) (:913), Destroy (:881).
  // The cue's options (fx.at; parts.md Interfaces 1): slot (0-5, required), end (age: the unsummon, gone 1 s later),
  // standing (true: at its slot on the floor from the start, no ring: Knight of the Deep's tile, decision 40), guard
  // ([from, to] ages: the owner's charge as the knight sees it: guarding from `from`, a pass at from + 0.1 x slot and every
  // 0.5 s while before `to`, back to root at `to`: the cue puts `to` on the slot's own pass, attacks_emotes.md Verification
  // 2), attack ([ages]: knightAttack at the target body; built, never cued). The owner is the hero at the cue's own spot
  // and rot (the origin, facing +z).
  // The rise (decision 37): the code's Lerp(.., 4 dt) without a frame rate, y = -e^(-4 t): each frame in standby the
  // offset to the slot x e^(-4 dt), and the turn back to her facing a slerp by 1 - e^(-4 dt). What is under the floor is
  // hidden, as the game's ground hides it (fx.clipFloor on the whole knight at the first update, decision 45: the rise and
  // whatever the unsummon clip sinks).
  // APPROXIMATED: Quaternion.Lerp as a slerp; the events on the effect's own clock at their exact ages (the game's
  // WaitForSeconds resume on the first frame past each); the guard's start at `from` (the game's Update sees the charge
  // one frame after the press).
  const KNIGHT_SLOTS = [[1.6, 1.6], [-1.6, 1.6], [1.6, -1.6], [-1.6, -1.6], [2.2, 0], [-2.2, 0]];   // (x, z) (:45-117)
  const KNIGHT_RATE = 4, GUARD_WAIT = 0.1, GUARD_EVERY = 0.5, ATTACK_LEN = 1.0, UNSUMMON_LEN = 1;
  api.part("whale_kingdomKnight", (fx, node) => {
    const WHO = "whale_kingdomKnight", at = fx.at || {};
    const STANDBY = 0, GUARD = 1, ATTACK = 2, UNSUMMON = 3;
    let slot = Number.isInteger(+at.slot) && at.slot != null && at.slot !== "" ? +at.slot : -1;
    if (!(slot >= 0 && slot < KNIGHT_SLOTS.length)) {
      warnOnce("slot", `effect part ${WHO}: the cue has no slot 0-5 (fx_cues/whale.json):`, fx.name, "stands at slot 0");
      slot = 0;
    }
    const num = x => (x != null && x !== "" && Number.isFinite(+x) ? +x : null);
    const standing = !!at.standing;
    const guard = Array.isArray(at.guard) && num(at.guard[0]) != null && num(at.guard[1]) != null ? [+at.guard[0], +at.guard[1]] : null;
    const attacks = [].concat(at.attack ?? []).map(num).filter(x => x != null).sort((a, b) => a - b);
    let end = num(at.end);
    // the owner's spot and facing = the cue's (the root as the page placed it); the slot in her frame
    const q0 = node.quaternion.clone();
    const home = node.position.clone().add(V(KNIGHT_SLOTS[slot][0], 0, KNIGHT_SLOTS[slot][1]).applyQuaternion(q0));
    node.position.copy(home);
    if (!standing) node.position.y -= 1;               // - up (:120)
    const body = target(fx), Y = V(0, 1, 0);
    let state = STANDBY, t = 0, started = false;
    let guardDue = !!guard, guardNext = 0, attackI = 0, attackEnd = 0, goneAt = 0, free = 0;   // free: when it last came back to standby
    const face = yaw => node.quaternion.setFromAxisAngle(Y, yaw);   // LookRotation of a flat direction
    const events = {
      unsummon(now) {
        state = UNSUMMON; goneAt = now + UNSUMMON_LEN; end = null;
        play(WHO, fx, node, "unsummon", ONCE);
      },
      gone() { return "destroy"; },
      guardStart(now) {
        guardDue = false;
        if (now >= guard[1]) return;                   // the charge is over already
        state = GUARD; guardNext = now + GUARD_WAIT * slot;
      },
      guardPass(now) {
        face(2 * Math.PI * Math.random());             // vFlat(Random.onUnitSphere): a uniform flat facing (:682)
        play(WHO, fx, node, "cAttack", LOOP);          // (:687-692; already looping after the first pass: left alone)
        guardNext = now + GUARD_EVERY;
      },
      guardEnd(now) {
        state = STANDBY; free = now;
        play(WHO, fx, node, "root", LOOP);             // (:700-710)
      },
      attackDue(now) {
        attackI++;
        if (state !== STANDBY) return;                 // only from standby (:489): this volley is skipped
        const dx = body[0] - node.position.x, dz = body[2] - node.position.z;
        if (dx || dz) face(Math.atan2(dx, dz));        // LookRotation(vFlat(target - position)) (:498)
        state = ATTACK; attackEnd = now + ATTACK_LEN;
        play(WHO, fx, node, "nAttack", ONCE);          // (:504-507)
      },
      attackDone(now) {
        state = STANDBY; free = now;
        play(WHO, fx, node, "root", LOOP);             // (:454-464)
      },
    };
    return { node, update(dt) {
      if (!started) {                                  // the spawn's frame: every node and mesh of the effect is built by now
        started = true;
        fx.clipFloor?.(fx.root);
        if (!standing) spawn(WHO, "kingdomKnight_ring2", { x: home.x, y: home.y, d: home.z, ...(Array.isArray(at.rot) ? { rot: at.rot } : {}) });   // (:126-132)
      }
      t += dt;
      // every event due by now, in the order of their times
      for (;;) {
        let when = Infinity, what = null;
        const offer = (time, name) => { if (time < when) { when = time; what = name; } };
        if (state === UNSUMMON) offer(goneAt, "gone");
        else {
          if (end != null) offer(end, "unsummon");
          if (state === GUARD) { if (guardNext < guard[1] - 1e-9) offer(guardNext, "guardPass"); else offer(guard[1], "guardEnd"); }
          else if (state === ATTACK) offer(attackEnd, "attackDone");
          else if (guardDue) offer(Math.max(guard[0], free), "guardStart");
          if (attackI < attacks.length) offer(attacks[attackI], "attackDue");
        }
        if (!what || when > t + 1e-9) break;
        if (events[what](when) === "destroy") return "destroy";   // WaitForSeconds(1), Destroy (:881, :913)
      }
      if (state === STANDBY) {                         // the Lerps (:229-234)
        const u = 1 - Math.exp(-KNIGHT_RATE * dt);
        node.position.lerp(home, u);
        node.quaternion.slerp(q0, u);
      }
      node.updateMatrixWorld(true);                    // the skinned body and the lance's trail after this part see the move
    } };
  });

  // ---------------------------------------------------------------- fx:grandTide (the hero's code on the wave)
  // Whale.cs, coroutine $RPC_grandTide$28979 (:37257-37990): grandTide by createEffect at the hero 1.0 s into grandTide1
  // (:37424-37436; EffectControl life 99, afterLife 1, followPosition, followState) and its Animation Play("create"), Once
  // (:37449-37454: also the default clip, playing by itself); Yield(3, 1) (:37939): 1 s later Play("root"), Loop
  // (:37509-37514); then while myCommand stays grandTide (the SEQ's grandTide2, 3 s); the release: Play("destroy"), Once
  // (:37706-37711) as the action changes, where followState's after-life (1 s) begins (EffectControl.cs:194-300).
  // The effect is made in grandTide1 and released two step edges later, which a cue's cut cannot reach (decision 41): the
  // cue's `release` (seconds after the spawn: 4) calls fx.cutNow() once = the destroy clip and the after-life, the game's
  // end exactly; the wrap mode Once is set after it, as the code does (the Loop set with "root" holds for every later
  // clip, mesh.js: the 1 s destroy clip would wrap on the after-life's last frame). Nothing after a cut or a stop
  // (fx.stopped: the page's own end came first).
  api.part("fx:grandTide", (fx, node) => {
    if (fx.cls !== "whale") return null;
    const r = fx.at?.release, release = r != null && r !== "" && Number.isFinite(+r) ? +r : null;
    let t = 0, rooted = false, done = false;
    return { node, update(dt) {
      if (done) return;
      if (fx.stopped) { done = true; return; }
      t += dt;
      if (release != null && t >= release - 1e-9) {
        done = true;
        fx.cutNow();                                   // Play("destroy") (:37706) and followState's after-life
        play("fx:grandTide", fx, node, "destroy", ONCE);   // wrapMode = Once (:37711): the clip is playing, so only the mode is set
        return;
      }
      if (!rooted && t >= 1 - 1e-9) { rooted = true; play("fx:grandTide", fx, node, "root", LOOP); }   // (:37509-37514)
      if (rooted && release == null) done = true;
    } };
  });
}
