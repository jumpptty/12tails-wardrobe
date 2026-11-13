// wardrobe/fxparts/mole.js: the Mole's own effect scripts and the hero's code acting on her effects (builder "mole",
// 2026-11-13; plans/fx_mole/parts.md "Each part" 1-3, 6, 7 and fx:flameCarnival / fx:detonate, with its Verification;
// the overnight decisions plans/fx_mole/decisions.md 18-27, 41, 55 (which win over the reports); the loader comment
// above FX_PART_FILES in index.html). BB's DecompiledSource is the authority for every line cited here
// (C:\Users\Jump\Desktop\12tails\DecompiledSource\<file> at the office, D:\12tails\... at home); TTO's lines are TTO1102
// (DecompiledSource_TTO_2026-11-02, pseudo/Mole.c); the prefab facts checks/fx_mole_research/parts/probe.txt (home).
//   Mole_nAttack / _mortarShot / _stunGrenade / _grenadeCluster / _napalm / _bazooka   the six shells: flight, the hit
//                             they spawn on the floor or the target body; the worn cannon's firePoint (cue firePoint + to)
//   Mole_missile              BB missile_fire and TTO tto/missileBot_fire / _fire_bot (one script in both games): homing,
//                             the hit it spawns, Twin Warhead's gold blast (the cue's pair), the egg's eight-way split
//   Mole_warMissile           warMissile (War Capital's volleys; not cued: decision 50): the same homing, 12 m/s
//   Mole_cartBomb             cartBomb_fire: the hero's drive at 6 m/s, stopped by the target body, the 3 s fuse
//   Mole_timeNuke             timeNuke1 / 2: the OnGUI countdown in GMO24 (fx.json "fonts"), detonate(), the blast
//   Mole_warCapital           warCapital: open, then root looped from 1 s
//   fx:detonate               Detonate's SendMessage("detonate") to the nuke at its spot
//   fx:flameCarnival          the trap's trigger (cue option `trigger`; no tile sets it: decision 26)
//   Mole_mine / Mole_stunMine / Mole_flameCarnival   data only on the owner's screen (parts.md part 4): nothing drawn
// Not here: the Chopper's engine (decision 46: the page's generic cue option playAudio, no fx:chopper part).
// Space: every root here hangs in the effect's mirror group (Unity's world, the hero's feet at the origin, +z her facing,
// y 0 the floor), so node.position is the game's transform.position and the numbers below are the game's own.
//
// The target (Bat decision 4, every class; parts.md "Each part"): one standard body, a CharacterController centred
// (0, 0.6, 10), height 1, radius 0.3 (its capsule's axis the centre +- 0.2 m); ClosestPointOnBounds = a point clamped into
// its box x +-0.3, y 0.1..1.1, z 9.7..10.3. The floor is y 0. The page has no other collider (APPROXIMATED: a shot that
// misses both flies its life out). A cue's `to` is the aim (the shells' re-aim from a firePoint; the missiles' homing
// point, default the body's centre 0.6 m up: Penguin decision 3); the body itself stays where it is.
//
// Page hooks used: api.spawn(name, at) (index.html fxSpawn; each entry's "builds" puts the hits in fx.json); api.hero()
// (C: C.props[slot] is the worn prop, its nodes' userData.label the prefab node names: buildProp); fx.uQuat / fx.mirror /
// fx.group / fx.nodes / fx.sounds; node.userData.fxAnim.play(name, fade, wrap) (mesh.js); api.FX.live / api.FX.gen /
// api.FX.t; api.Sound.play; api.camera / api.renderer / api.texLoader / api.DATA (the countdown label).
import { trajectoryVector, lookEuler } from "./cat.js";

// ---------------------------------------------------------------- Math.getMortarVector (Math.cs:1011-1086)
// Every opaque predicate worked by hand (the `continue`s dead): flat = vFlat(pos - target), d = |flat|, g =
// Physics.gravity.y (-9.8, the PhysicsManager); d < |v^2 / g| - 1: f = 0.5 asin(d g / v^2) (:1043-1049), else f = -0.5
// (:1057); direction = (sin(f) flat.normalized + cos(f) up).normalized (:1063-1085). g < 0 makes f < 0, so sin(f) x the
// backward flat points ahead: the high lob, |f| from vertical. From (0.2, 1, 0.6) at (0, 0, 10), v 20: Euler [-83.34,
// -1.22, 0] (skills_b.md Verification; at d 10: 82.9 deg up, about 4.05 s in the air). Plain [x, y, z] arrays.
export const mortarVector = (pos, target, v, g = -9.8) => {
  const bx = pos[0] - target[0], bz = pos[2] - target[2], d = Math.hypot(bx, bz);
  const f = d < Math.abs(v * v / g) - 1 ? 0.5 * Math.asin(d * g / (v * v)) : -0.5;
  const s = Math.sin(f), n = d > 1e-5 ? [bx / d, bz / d] : [0, 0];   // vFlat(..).normalized: zero below 1e-5
  const o = [s * n[0], Math.cos(f), s * n[1]], m = Math.hypot(o[0], o[1], o[2]) || 1;
  return [o[0] / m, o[1] / m, o[2] / m];
};

export default function register(api) {
  const { THREE, V } = api;
  const STEP = 0.02;                                   // Unity's fixed timestep (FixedUpdate, 50 per second)
  const GRAVITY = -9.8;                                // Physics.gravity.y (probe_ps.txt)
  const DEG = Math.PI / 180;
  const LOOP = 2;                                      // UnityEngine.WrapMode.Loop
  const BODY = V(0, 0.6, 10), BODY_HALF = 0.2, BODY_R = 0.3, BODY_BOX = V(0.3, 0.5, 0.3);
  const warned = new Set();
  const warnOnce = (k, ...m) => { if (!warned.has(k)) { warned.add(k); console.warn(...m); } };
  const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
  const num = (x, dflt) => (x != null && x !== "" && Number.isFinite(+x) ? +x : dflt);
  const vec = (a, dflt) => (Array.isArray(a) && a.length >= 3 ? V(+a[0] || 0, +a[1] || 0, +a[2] || 0) : dflt.clone());
  // Quaternion.LookRotation(forward, Vector3.up) in Unity's numbers (cat.js's / bat.js's)
  const lookRot = (f, q = new THREE.Quaternion()) => {
    const z = f.clone().normalize(), x = V().crossVectors(V(0, 1, 0), z);
    if (x.lengthSq() < 1e-12) x.set(1, 0, 0); x.normalize();
    return q.setFromRotationMatrix(new THREE.Matrix4().makeBasis(x, V().crossVectors(z, x), z));
  };
  // Vector3.RotateTowards's direction (bat.js's): from a toward b by at most maxRad, unit length
  const rotateTowards = (a, b, maxRad) => {
    const u = a.clone().normalize(), w = b.clone().normalize(), ang = Math.acos(clamp(u.dot(w), -1, 1));
    if (ang <= maxRad || ang < 1e-9) return w;
    const s = Math.sin(ang);
    if (s < 1e-6) return u.applyAxisAngle(Math.abs(u.y) < 0.99 ? V().crossVectors(u, V(0, 1, 0)).normalize() : V(1, 0, 0), maxRad);
    return u.multiplyScalar(Math.sin(ang - maxRad) / s).addScaledVector(w, Math.sin(maxRad) / s);
  };
  // a quaternion back to a cue's rot (Unity Euler degrees, "YXZ"; chameleon.js's)
  const eulerOf = q => { const e = new THREE.Euler().setFromQuaternion(q, "YXZ"); return [e.x / DEG, e.y / DEG, e.z / DEG]; };
  // the yaw of LookRotation(vFlat(f).normalized); LookRotation(zero) = identity
  const flatYaw = f => (Math.hypot(f.x, f.z) < 1e-5 ? 0 : Math.atan2(f.x, f.z) / DEG);
  const spawn = (who, name, at, opts) => {
    if (!api.spawn) { warnOnce("spawn", `effect part ${who}: no api.spawn (index.html):`, name, "not drawn"); return null; }
    const f = api.spawn(name, at, opts);
    if (!f) warnOnce("miss:" + name, `effect part ${who}: ${name} not in fx.json (the entry's "builds")`);
    return f;
  };
  const at3 = (p, rot, more) => ({ x: p.x, y: p.y, d: p.z, rot, ...more });
  // the trigger box against the body: its centre line from z0 to z1 along fwd (unit), every 0.05 m, within w + the body's
  // radius of the capsule's axis (chameleon.js's test; APPROXIMATED: a box as a swept sphere of its half width)
  const onAxis = V(), probe = V();
  const toAxis = p => p.distanceTo(onAxis.set(BODY.x, clamp(p.y, BODY.y - BODY_HALF, BODY.y + BODY_HALF), BODY.z));
  const boxOnBody = (pos, fwd, z0, z1, w) => {
    for (let z = z0; z <= z1 + 1e-9; z += 0.05) if (toAxis(probe.copy(pos).addScaledVector(fwd, z)) <= w + BODY_R) return true;
    return false;
  };
  // mCollider.ClosestPointOnBounds(the shot's bounds centre): clamped into the body's box
  const onBounds = c => V(clamp(c.x, BODY.x - BODY_BOX.x, BODY.x + BODY_BOX.x), clamp(c.y, BODY.y - BODY_BOX.y, BODY.y + BODY_BOX.y),
    clamp(c.z, BODY.z - BODY_BOX.z, BODY.z + BODY_BOX.z));

  // ---------------------------------------------------------------- the worn cannon's firePoint (decision 19)
  // RPC_nAttack1 / 2 (Mole.cs:20396-20418, :21158-21174), RPC_mortarShot (:24696-24712), RPC_napalm (:37106-37122),
  // RPC_stunGrenade (:27343-27365): firePos = the weapon's child "firePoint" when it has one, else position +
  // TransformDirection(0.2, 1, 0.6); fireDir = tDir - fireOffset, so firePos + fireDir is the aim whatever the muzzle: the
  // cue's `to`. Here: the worn prop (slot = the cue's firePoint, "R") has a node named firePoint (the prefab's names are
  // its nodes' userData.label, index.html buildProp): the shell starts there (its world position read in the spawn frame,
  // the pose of that frame), turned along the game's vector from it to `to`. No such node (a bare hand, Double Cannon,
  // the Trumpet, a cannon without one): the cue's own x / y / d / rot, which aim from the default point.
  const firePoint = (fx, slot) => {
    const prop = api.hero?.()?.props?.[slot];
    let fp = null;
    prop?.traverse(o => { if (!fp && o.userData?.label === "firePoint") fp = o; });
    if (!fp) return null;
    fx.mirror.updateWorldMatrix(true, false); fp.updateWorldMatrix(true, false);
    return fp.getWorldPosition(V()).applyMatrix4(fx.mirror.matrixWorld.clone().invert());
  };

  // ---------------------------------------------------------------- the six shells (parts.md part 1, decisions 18-24)
  // One pattern on each prefab's root (ProjectileControl + the script + a trigger BoxCollider + Rigidbody): the ctor's
  // private velocity, Awake rigidbody.velocity = TransformDirection(it) along the spawn rotation (the cue's rot), each
  // FixedUpdate the clock against the hero code's life (Destroy at it) and transform.LookAt(position + velocity) (not the
  // Bazooka's); OnTriggerEnter on any collider not the owner's layer / 1 / 2 (the floor counts) -> the hit RPC at
  // ClosestPointOnBounds, then Destroy (the root's legacy smoke trail goes with it). Gravity -9.8 on all but the Bazooka.
  //   script                v (ctor)   life (Mole.cs)   box (trigger)        hit, rotation
  //   Mole_nAttack          15 (:28)   10  :10089        0.25 x 0.25 x 0.5    nAttack_hit, identity (:10105)
  //   Mole_mortarShot       20 (:26)   5   :10780        0.25 x 0.25 x 0.5    mortarShot_hit, identity (:10830)
  //   Mole_stunGrenade      15 (:28)   3   :11307        0.25 cube            nAttack_hit, identity (Mole_stunGrenade.cs:193)
  //   Mole_grenadeCluster    6 (:28)   5   :13819        0.25 cube            grenadeCluster_hit, LookRotation(zero) (:13865)
  //   Mole_napalm           20 (:26)   5   :13749        0.25 x 0.25 x 0.5    napalm_hit, LookRotation(vFlat fwd) (:37769)
  //   Mole_bazooka          24 (:28)   2   :41361        0.25 x 0.25 x 0.5    bazooka_hit, LookRotation(vFlat fwd) (:14036)
  // (lives x rangeMod 1). Each 0.02 s step (cat.js's Cat_supportFire): v.y += g x 0.02, p += v x 0.02, then the contact:
  // the target body first (the box's centre line within its half width + 0.3 of the axis; the hit at the box centre
  // clamped into the body's box), then the floor (the box's lowest corner, y - (half.y cos pitch + half.z |sin pitch|) <=
  // 0; the hit under the box, y 0). Drawn between steps along the velocity. APPROXIMATED: the box centred on the root
  // (the probe gave its size, not its centre).
  //   aim     the vector a firePoint re-aim uses (decision 19): getTrajectoryVector 15 / getMortarVector 20
  //   tilt    Grenade Cluster (decision 24): RPC_grenadeCluster (:38002-38014): dir = rotateH(forward + 0.1 Random.Range(3,
  //           10) up, 45 i).normalized, spawned at (0, 1, 0.5) + 0.5 dir, LookRotation(dir) (:13810): the cue gives the
  //           yaw (rot [0, -45 i, 0]), the spot (0, 1, 0.5) and tilt [3, 9]; the part draws k (an int 3..9) per grenade
  // From the default point the Normal Attack's shell (rot [-6.753, -1.219, 0]) reaches the body's front low at ~9.45 m
  // after ~0.6 s (the floor would have had it at 9.83 m: attacks_emotes.md geom.txt); the mortar's lob falls onto the
  // body's top (y 1.1) after ~4 s; the Bazooka's shells meet its front at 9.7 m, 1 m up, 0.35 s after each shot.
  const SHELL = {
    Mole_nAttack: { v: 15, g: true, life: 10, look: true, half: [0.125, 0.125, 0.25], hit: "nAttack_hit", flat: false, aim: "traj" },
    Mole_mortarShot: { v: 20, g: true, life: 5, look: true, half: [0.125, 0.125, 0.25], hit: "mortarShot_hit", flat: false, aim: "mortar" },
    Mole_stunGrenade: { v: 15, g: true, life: 3, look: true, half: [0.125, 0.125, 0.125], hit: "nAttack_hit", flat: false, aim: "traj" },
    Mole_grenadeCluster: { v: 6, g: true, life: 5, look: true, half: [0.125, 0.125, 0.125], hit: "grenadeCluster_hit", flat: false },
    Mole_napalm: { v: 20, g: true, life: 5, look: true, half: [0.125, 0.125, 0.25], hit: "napalm_hit", flat: true, aim: "mortar" },
    Mole_bazooka: { v: 24, g: false, life: 2, look: false, half: [0.125, 0.125, 0.25], hit: "bazooka_hit", flat: true },
  };
  const shell = type => (fx, node) => {
    const S = SHELL[type], at = fx.at || {};
    if (S.aim && at.firePoint && Array.isArray(at.to)) {
      const fp = firePoint(fx, at.firePoint);
      if (fp) {
        const p = [fp.x, fp.y, fp.z], to = [num(at.to[0], 0), num(at.to[1], 0), num(at.to[2], 0)];
        const d = S.aim === "mortar" ? mortarVector(p, to, S.v, GRAVITY) : trajectoryVector(p, to, S.v, GRAVITY);
        node.position.copy(fp); lookRot(V(d[0], d[1], d[2]), node.quaternion);
      }
    }
    if (S === SHELL.Mole_grenadeCluster && Array.isArray(at.tilt)) {
      const lo = Math.round(num(at.tilt[0], 3)), hi = Math.round(num(at.tilt[1], 9));
      const k = lo + Math.floor(Math.random() * (hi - lo + 1));   // Random.Range(3, 10): an int 3 .. 9 (:38009)
      const dir = V(0, 0.1 * k, 1).normalize().applyQuaternion(node.quaternion);
      node.position.addScaledVector(dir, 0.5); lookRot(dir, node.quaternion);   // firePos + 0.5 dir, LookRotation(dir)
    }
    const vel = V(0, 0, S.v).applyQuaternion(fx.uQuat(node));   // TransformDirection at the spawn (Awake)
    const p = node.position.clone(), dir = V(), [hx, hy, hz] = S.half;
    const LIFE_STEPS = Math.round(S.life / STEP);
    let acc = 0, k = 0;
    const land = hp => spawn(type, S.hit, at3(hp, S.flat ? [0, flatYaw(vel), 0] : [0, 0, 0]));
    return { node, update(dt) {
      acc += dt;
      while (acc >= STEP) {
        acc -= STEP;
        if (++k >= LIFE_STEPS) return "destroy";       // the clock at ProjectileControl.life: Destroy (FixedUpdate)
        if (S.g) vel.y += GRAVITY * STEP;
        p.addScaledVector(vel, STEP);
        dir.copy(vel).normalize();
        if (boxOnBody(p, dir, -hz, hz, hx)) { node.position.copy(p); land(onBounds(p)); return "destroy"; }
        const pitch = Math.atan2(-vel.y, Math.hypot(vel.x, vel.z));
        if (p.y - (hy * Math.cos(pitch) + hz * Math.abs(Math.sin(pitch))) <= 0) { node.position.copy(p); land(V(p.x, 0, p.z)); return "destroy"; }
      }
      node.position.copy(p).addScaledVector(vel, acc);
      if (S.look) lookRot(vel, node.quaternion);       // LookAt(position + velocity) (FixedUpdate)
      node.updateMatrixWorld(true);                    // the trail's emitter after this part sees the move
    } };
  };
  for (const type of Object.keys(SHELL)) api.part(type, shell(type));

  // ---------------------------------------------------------------- Mole_missile, Mole_warMissile (part 2, decisions 22, 41)
  // BB Mole_missile.cs (Mole_warMissile.cs the same code): Awake velocity = TransformDirection(ProjectileControl.velocity)
  // (:34; the prefab's (0, 0, 8) / (0, 0, 12)); Update (:46-179, the frame clock): clock += dt (:64); at life (missile 5 x
  // rangeMod, Mole.cs:13149; warMissile the prefab's 12) RPC_missile_hit(position, forward) (:118) and Destroy: it explodes
  // where it is; else every 0.2 s, the first on the first frame (:151-157): forward = RotateTowards(forward,
  // mTarget.collider.bounds.center - position, 0.3 rad, 1) (:162), LookRotation (:167), velocity = TransformDirection(v)
  // (:172). OnTriggerEnter (:188-301): any collider not the owner's layer / 1 / 2 -> RPC_missile_hit(ClosestPointOnBounds,
  // forward) and Destroy. No gravity; trigger box 0.2 x 0.2 x 0.5 centred 0.25 ahead. Hits: missile_hit with the HERO's
  // rotation (Mole.cs:13208), warMissile_hit LookRotation(hitDir) = the missile's forward (:14615).
  // TTO's Mole_missile is the same script (TTO1102 Mole_missile::Update@0x1CA0660, OnTriggerEnter@0x1C9FDC0; fields mTarget,
  // scatter, twin, pair, dump.cs:108651), on tto/missileBot_fire and the egg's tto/missileBot_fire_bot: life 10 x rangeMod
  // with Twin Warhead (Mole::FireMissile@0x1C2B3C0), its hit tto/missileBot_hit at the hit point with the hero's rotation
  // (RPC_missile_hit@0x1C35100); then, for the egg (scatter), MissileBotScatter@0x1C2E1E0: 8 tto/missileBot_fire from the
  // hit + 1 up, dir = normalize(rotateH(the hero's forward + 0.3 up, 45 i)) (Mole.c:36986-37064; rotateH turns left,
  // Math.cs:838-843), each at the target, carrying the last pair's id with twin set (tto.md Verification 3: FireMissile
  // never resets pendingTwinPair); then, the target hit and twin set, WarheadHit@0x1C3FFE0: the pair's second hit within
  // 0.5 s of the first -> RPC_twinImpact@0x1C39D90: tto/twinImpact there, LookRotation(vFlat(dir)) (Mole.c:37519-37588).
  // The egg keeps the gold blasts (tto.md Verification 2). The cue: `pair` (0-3, missiles 2j and 2j + 1 share pair j),
  // `to` the homing point (default the body's centre, 0.6 m up), no `kill` (decision 22: the part spawns every hit).
  // Here: the turn on the frame clock, the move in 0.02 s steps with the contact after each (bat.js's Bat_echoes); the
  // contact: the box's centre line (0 .. 0.5 ahead) within 0.1 + 0.3 of the body's axis, the hit at the box's centre
  // clamped into the body's box; or the box's lowest point at the floor (the hit under the box centre, y 0; no twin). Life's
  // end: the hit where it is, no split, no twin. The pairs of one play (api.FX.gen) are kept in `plays`: their first hit's
  // time on the play's clock (api.FX.t at the launch + the missile's own clock; a split inherits its parent's).
  // APPROXIMATED: WarheadHit's bookkeeping read as "a second hit within 0.5 s blasts and clears the pair, else the hit
  // starts it" (medium sure: tto.md Verification 3, read from the pseudo-C, not run).
  const MISSILE_TURN = 0.2, MISSILE_RAD = 0.3, TWIN_GAP = 0.5, SPLITS = 8, MISSILE_W = 0.1, MISSILE_Z = 0.5;
  const plays = new Map();                             // api.FX.gen -> { pairs: Map(pair -> the first hit's time), last }
  const playOf = () => {
    const g = api.FX.gen;
    for (const k of plays.keys()) if (k !== g) plays.delete(k);
    let pl = plays.get(g);
    if (!pl) plays.set(g, pl = { pairs: new Map(), last: null });
    return pl;
  };
  const homing = war => (fx, node, c, mat, nd) => {
    const who = war ? "Mole_warMissile" : "Mole_missile", at = fx.at || {}, tto = fx.name.startsWith("tto/");
    const pc = nd?.comps?.find(x => x.type === "ProjectileControl"), pv = Array.isArray(pc?.velocity) ? pc.velocity : null;
    const speed = (pv && Math.hypot(+pv[0] || 0, +pv[1] || 0, +pv[2] || 0)) || (war ? 12 : 8);
    const life = war ? num(pc?.life, 0) || 12 : tto ? 10 : 5;
    const aim = vec(at.to, BODY);
    const play = playOf(), pair = num(at.pair, null);
    if (pair != null && !at.split) play.last = pair;   // NextTwinPair at the launch
    const twin = tto && pair != null;
    const scatter = !at.split && fx.name === "tto/missileBot_fire_bot";   // the egg's prefab (FireMissile picks it)
    const t0 = num(at.t0, api.FX.t);
    const hitName = war ? "warMissile_hit" : tto ? "tto/missileBot_hit" : "missile_hit";
    const p = node.position.clone(), toward = V(), box = V();
    let fwd = V(0, 0, 1).applyQuaternion(fx.uQuat(node)), vel = fwd.clone().multiplyScalar(speed);
    let clock = 0, next = 0, acc = 0;
    const hit = hp => spawn(who, hitName, at3(hp, war ? lookEuler([fwd.x, fwd.y, fwd.z]) : [0, 0, 0]));
    const contact = (hp, onBody) => {
      hit(hp);
      const now = t0 + clock;
      if (scatter) for (let i = 0; i < SPLITS; i++) {
        const a = 45 * i * DEG;                        // rotateH((0, 0.3, 1), 45 i): +a turns left
        spawn(who, "tto/missileBot_fire", { x: hp.x, y: hp.y + 1, d: hp.z, rot: lookEuler([-Math.sin(a), 0.3, Math.cos(a)]),
          to: [aim.x, aim.y, aim.z], pair: play.last, split: true, t0: now });
      }
      if (twin && onBody) {
        const first = play.pairs.get(pair);
        if (first != null && now - first <= TWIN_GAP) { play.pairs.delete(pair); spawn(who, "tto/twinImpact", at3(hp, [0, flatYaw(fwd), 0])); }
        else play.pairs.set(pair, now);
      }
    };
    // (the clock and the turns run on the 0.02 s steps too, not once per frame: 2026-11-13, the editor's gate, a 3.9 s
    // headless frame flew every missile straight for 3.9 s, so they hit the floor and no pair ever blasted; at the page's
    // frame rates the two clocks agree within a step)
    return { node, update(dt) {
      acc += dt;
      while (acc >= STEP) {                            // the physics: p += v x 0.02, then the trigger
        acc -= STEP;
        if (clock >= life) { hit(p); return "destroy"; }   // the life's end: the hit where it is
        if (next <= clock + 1e-6) {                    // every 0.2 s, the first on the first step
          next = clock + MISSILE_TURN;
          fwd = rotateTowards(fwd, toward.subVectors(aim, p), MISSILE_RAD);
          lookRot(fwd, node.quaternion);
          vel = fwd.clone().multiplyScalar(speed);
        }
        clock += STEP;
        p.addScaledVector(vel, STEP);
        if (boxOnBody(p, fwd, 0, MISSILE_Z, MISSILE_W)) {
          node.position.copy(p); contact(onBounds(box.copy(p).addScaledVector(fwd, MISSILE_Z / 2)), true); return "destroy";
        }
        if (Math.min(p.y, p.y + MISSILE_Z * fwd.y) - MISSILE_W <= 0) {
          node.position.copy(p); box.copy(p).addScaledVector(fwd, MISSILE_Z / 2); contact(V(box.x, 0, box.z), false); return "destroy";
        }
      }
      node.position.copy(p).addScaledVector(vel, acc);
      node.updateMatrixWorld(true);
    } };
  };
  api.part("Mole_missile", homing(false));
  api.part("Mole_warMissile", homing(true));

  // ---------------------------------------------------------------- Mole_cartBomb (part 3 + Verification 5, decision 23)
  // Mole_cartBomb.cs: Update (:52-157): t += dt (:83); while t <= 3 (:88) and the owner still attacks with myCommand
  // "cartBomb" (:94-100): nothing; else RPC_cartBomb_hit(position, forward) (:127) and Destroy (:146). The hero's drive
  // (coroutine $RPC_cartBomb$24030): spawned at getSpawnPos(hero + 0.5 forward), the hero's rotation (:43088-43106),
  // Yield(3, 0.2) (:43544), then every FixedUpdate rotation = LookRotation(dir), velocity = 6 dir, dir the hero's forward
  // (no move keys on the page) (:43267-43296). The cart is a solid capsule (radius 0.5): the target body stops it, its
  // centre 0.5 + 0.3 from the body's axis (9.2 m straight ahead, ~1.65 s after the spawn), where it waits for the fuse.
  // cartBomb_hit at the cart, LookRotation(its forward) (Mole.cs:14154), 3 s after the spawn. The hero's action holds
  // until the cart is gone (:43248-43254), so on the page only the fuse ends it. APPROXIMATED: Unity's contact solver as
  // a stop at first touch (parts.md: medium sure).
  const CART_V = 6, CART_FROM = 0.2, CART_FUSE = 3, CART_R = 0.5;
  api.part("Mole_cartBomb", (fx, node) => {
    const fwd = V(0, 0, 1).applyQuaternion(fx.uQuat(node)).setY(0);
    if (fwd.lengthSq() < 1e-10) fwd.set(0, 0, 1); fwd.normalize();
    const p = node.position.clone(), rel = V();
    let t = 0, acc = 0, k = 0, stopped = false;
    const R = CART_R + BODY_R;
    return { node, update(dt) {
      t += dt;
      if (t > CART_FUSE) {                             // t <= 3 no longer holds (:88)
        spawn("Mole_cartBomb", "cartBomb_hit", at3(p, [0, flatYaw(fwd), 0]));
        return "destroy";
      }
      acc += dt;
      while (acc >= STEP) {
        acc -= STEP;
        if (++k * STEP <= CART_FROM + 1e-9 || stopped) continue;
        // |rel + s fwd| = R on the flat: the touch along this step, if it comes within it
        rel.set(p.x - BODY.x, 0, p.z - BODY.z);
        const b = rel.dot(fwd), disc = b * b - rel.lengthSq() + R * R, s = disc >= 0 ? -b - Math.sqrt(disc) : Infinity;
        const step = CART_V * STEP;
        if (s >= -1e-9 && s <= step) { p.addScaledVector(fwd, Math.max(0, s)); stopped = true; }
        else p.addScaledVector(fwd, step);
      }
      node.position.copy(p);
      node.updateMatrixWorld(true);
    } };
  });

  // ---------------------------------------------------------------- Mole_timeNuke (part 6, decisions 27, 55)
  // Mole_timeNuke.cs: fields mLv (:341; 1 / 2 by prefab), isVisible (:344, ctor true), timeNuke_explosion (:350).
  // Init (:42-119): start = Time.time (:56), state 1 (:59), a GUIStyle: GameGui/Fonts/GMO24 (:65), text colour (0.8, 0.3,
  // 0.3, 1) (:68), centred (:71). OnGUI (:142-178), while state 1 and isVisible: v = Camera.main.WorldToScreenPoint(position
  // + (0.2 mLv + 0.6) up) (:157: 1.0 m up for timeNuke2), drawn only when 0 < v.z < 30 (:160-168), GUI.Label(Rect(v.x - 15,
  // Screen.height - v.y - 15, 30, 30), floor(start + 60 - Time.time)) (:175): 60 for the first instant, then 59, 58 ...
  // Update (:191-287): start + 60 <= now + 1 -> state 2, the label gone at 59 s (:241-247); start + 60 <= now -> state 3,
  // doExplode (:263-276). detonate() (SendMessage from Detonate, Mole.cs:31102, :31148; :436-524): in state 1, state 3,
  // Yield 0.5 (:523), doExplode (:451). doExplode (:644-921): Instantiate(timeNuke_explosion, position, rotation) (:796),
  // the nuke's renderers off (:801-828), four damage waves 0.1 s apart, Destroy 0.4 s after (:911).
  // The label (decision 55): a Sprite in the effect's group (no mirror: a screen picture), never depth-tested, over the
  // scene, its size kept at 30 x 30 CSS px each frame from the camera's projection and the canvas height (Screen pixels:
  // the page's CSS pixels), its canvas redrawn when the number changes: the digits from the GMO24 bitmap font in fx.json
  // "fonts" (parts.md Interfaces 3; the exporter is the page_pipeline builder's), each glyph at 1 px a texel (GUI.Label
  // draws a bitmap font 1:1), laid out by its vert rect and advance width, tinted (0.8, 0.3, 0.3); with no font data (or
  // before its picture arrives), a bold 18 px sans in the same colour. Centred by the MEASURED INK in the 30 x 30 box
  // (CLAUDE.md "Thai text: centring by eye": no marks here, the same rule): the composed digits' alpha scanned for their
  // bounds, those bounds centred (rounded to whole pixels). APPROXIMATED: GUI's MiddleCenter centres the line box (the
  // font's ascent / line height), so the game's digits sit a pixel or two off the point; the page centres the ink.
  // The font's data shape (agreed in parts.md Interfaces 3; exporter = page_pipeline): data.fonts.GMO24 = { tex: "GMO24",
  // ascent: 19, chars: { "0": { uv: [x, y, w, h], vert: [x, y, w, h], width }, ... "9" } }, as Unity's m_CharacterRects
  // ("0": uv [0.39453125, 0.9609375, 0.03125, 0.03515625] (Unity's bottom-left origin), vert [0, -10, 8, -9], width 9),
  // the picture data/fx/tex/<tex>.webp with the glyphs' coverage in its ALPHA (the rip's Font Texture is Alpha8: an RGBA
  // export keeps rgb 0 and the coverage in a; a lossy webp must keep the alpha).
  const NUKE_FUSE = 60, NUKE_LABEL_END = 59, NUKE_DETONATE = 0.5, NUKE_GONE = 0.4, LABEL_PX = 30, LABEL_FAR = 30;
  const NUKE_RGB = "rgb(204, 77, 77)";                 // (0.8, 0.3, 0.3), the game's gamma values
  const fontTex = new Map();                           // the font picture's url -> its THREE.Texture (image set when loaded)
  const composeDigits = (text, font, img) => {
    const c = document.createElement("canvas"), g0 = () => c.getContext("2d");
    const chars = font?.chars;
    if (img && chars && [...text].every(ch => chars[ch])) {
      let w = 0;
      for (const ch of text) w += Math.max(num(chars[ch].width, 0), Math.abs(num(chars[ch].vert?.[2], 0)) + num(chars[ch].vert?.[0], 0));
      c.width = Math.ceil(w) + 8; c.height = 64;
      const g = g0(), base = 32, W = img.naturalWidth || img.width, H = img.naturalHeight || img.height;
      g.imageSmoothingEnabled = false;
      let x = 4;
      for (const ch of text) {
        const cr = chars[ch], [u, v, uw, uh] = (cr.uv || [0, 0, 0, 0]).map(Number), [vx, vy, vw, vh] = (cr.vert || [0, 0, 0, 0]).map(Number);
        const sx = Math.min(u, u + uw) * W, sy = (1 - Math.max(v, v + uh)) * H, sw = Math.abs(uw) * W, sh = Math.abs(uh) * H;
        if (sw > 0 && sh > 0) g.drawImage(img, sx, sy, sw, sh, x + Math.min(vx, vx + vw), base - Math.max(vy, vy + vh), Math.abs(vw), Math.abs(vh));
        x += num(cr.width, Math.abs(vw));
      }
      g.globalCompositeOperation = "source-in"; g.fillStyle = NUKE_RGB; g.fillRect(0, 0, c.width, c.height);
      return c;
    }
    c.width = 64; c.height = 40;
    const g = g0();
    g.font = "bold 18px sans-serif"; g.fillStyle = NUKE_RGB; g.textBaseline = "alphabetic"; g.fillText(text, 4, 28);
    return c;
  };
  const inkBounds = c => {                             // the drawn pixels' bounds [x0, y0, x1, y1), or null
    let d;
    try { d = c.getContext("2d").getImageData(0, 0, c.width, c.height).data; } catch (e) { return [0, 0, c.width, c.height]; }
    let x0 = c.width, y0 = c.height, x1 = -1, y1 = -1;
    for (let y = 0; y < c.height; y++) for (let x = 0; x < c.width; x++) if (d[(y * c.width + x) * 4 + 3] > 0) {
      if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y;
    }
    return x1 < 0 ? null : [x0, y0, x1 + 1, y1 + 1];
  };
  api.part("Mole_timeNuke", (fx, node, c, mat, nd, data) => {
    const lv = num(c?.mLv, 2), up = 0.2 * lv + 0.6, visible = c?.isVisible !== false;
    const font = data?.fonts?.GMO24 || null;
    let tex = null;
    if (font?.tex && typeof document !== "undefined") {
      const url = `${api.DATA}fx/tex/${font.tex}.webp`;
      tex = fontTex.get(url) || null;
      if (!tex && api.texLoader) fontTex.set(url, tex = api.texLoader.load(url));
    } else if (!font) warnOnce("gmo24:" + fx.cls, "effect part Mole_timeNuke: no fonts.GMO24 in fx.json (the exporter): the countdown in a plain bold font");
    const dpr = Math.max(1, api.renderer?.getPixelRatio?.() || 1), N = Math.round(LABEL_PX * dpr);
    const canvas = document.createElement("canvas"); canvas.width = canvas.height = N;
    const ctex = new THREE.CanvasTexture(canvas);
    ctex.colorSpace = THREE.SRGBColorSpace; ctex.minFilter = ctex.magFilter = THREE.NearestFilter; ctex.generateMipmaps = false;
    const smat = new THREE.SpriteMaterial({ map: ctex, sizeAttenuation: false, depthTest: false, depthWrite: false, transparent: true });
    const label = new THREE.Sprite(smat);
    label.renderOrder = 1e6; label.frustumCulled = false; label.visible = false;
    fx.group.add(label);
    let t = 0, state = 1, shown = null, hadImg = false, boomAt = null, goneAt = null;
    const wp = V(), cp = V();
    const draw = n => {
      const img = tex?.image || null, text = String(n);
      const src = composeDigits(text, font, img), b = inkBounds(src);
      const g = canvas.getContext("2d");
      g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, N, N);
      if (b) {
        const bw = b[2] - b[0], bh = b[3] - b[1], dx = Math.round((LABEL_PX - bw) / 2), dy = Math.round((LABEL_PX - bh) / 2);
        g.imageSmoothingEnabled = false;
        g.drawImage(src, b[0], b[1], bw, bh, dx * dpr, dy * dpr, bw * dpr, bh * dpr);
      }
      ctex.needsUpdate = true; shown = n; hadImg = !!img;
    };
    const explode = () => {
      spawn("Mole_timeNuke", "timeNuke_explosion", at3(node.position, eulerOf(fx.uQuat(node))));
      goneAt = t + NUKE_GONE;
    };
    const em = { node,
      detonate() {                                     // Mole_timeNuke.detonate (:436-524): only in state 1
        if (state !== 1) return false;
        state = 3; boomAt = t + NUKE_DETONATE; label.visible = false;
        return true;
      },
      update(dt) {
        t += dt;
        if (state === 1 && t >= NUKE_LABEL_END) state = 2;                 // start + 60 <= now + 1 (:241-247)
        if (state < 3 && t >= NUKE_FUSE) { state = 3; boomAt = t; }        // start + 60 <= now: doExplode (:263-276)
        if (boomAt != null && goneAt == null && t >= boomAt) explode();
        if (goneAt != null) {
          node.traverse(o => { if (o.isMesh) o.visible = false; });       // its renderers off (:801-828)
          label.visible = false;
          return t >= goneAt ? "destroy" : undefined;  // Destroy 0.4 s after the blast (:911)
        }
        if (state !== 1 || !visible) { label.visible = false; return; }
        const cam = api.camera;
        node.getWorldPosition(wp).y += up;             // position + (0.2 mLv + 0.6) up (:157); world up = Unity's up here
        cp.copy(wp).applyMatrix4(cam.matrixWorldInverse);
        const depth = -cp.z;                           // WorldToScreenPoint's z
        label.visible = depth > 0 && depth < LABEL_FAR;
        if (!label.visible) return;
        const n = Math.floor(NUKE_FUSE - t);
        if (n !== shown || (!hadImg && tex?.image)) draw(n);
        fx.group.worldToLocal(label.position.copy(wp));
        const H = api.renderer?.domElement?.clientHeight || 600, P11 = cam.projectionMatrix.elements[5] || 1;
        const s = 2 * LABEL_PX / (P11 * H);            // sizeAttenuation off: s x P11 x H / 2 = 30 px
        label.scale.set(s, s, 1);
      },
      dispose() {
        label.parent?.remove(label);                   // before Fx.dispose's sweep (a Sprite's geometry is three's shared one)
        smat.dispose(); ctex.dispose();
      } };
    return em;
  });

  // ---------------------------------------------------------------- fx:detonate (part 6, decision 27)
  // Detonate (Mole.cs, the skill's coroutine): at clip 0.6 (Yield(2, 0.6) :31458) the detonate effect at each of her
  // nukes, identity (:31125, :31171), and SendMessage("detonate") to it (:31102, :31148); the skill refuses to start with
  // none ("Cannot find TimeNuke to detonate", :6762). Here: the hook on the detonate effect, on its first update (every
  // effect's matrices are current then), finds the living Fx whose emitter has detonate() (Mole_timeNuke) nearest its
  // spot within 0.5 m and calls it; the nuke's own part explodes it 0.5 s later.
  api.part("fx:detonate", fx => {
    let done = false;
    return { node: fx.root, update() {
      if (done) return;
      done = true;
      const here = fx.root.getWorldPosition(V()), there = V();
      let best = null, bd = 0.5;
      for (const f of api.FX.live) {
        if (f === fx || !f.alive || !f.emitters) continue;
        const e = f.emitters.find(x => typeof x.detonate === "function");
        if (!e) continue;
        const d = f.root.getWorldPosition(there).distanceTo(here);
        if (d <= bd) { best = e; bd = d; }
      }
      if (!best) warnOnce("detonate", "effect part fx:detonate: no Time Nuke within 0.5 m (the cue lays timeNuke2 first: decision 27)");
      else best.detonate();
    } };
  });

  // ---------------------------------------------------------------- Mole_warCapital (part 7)
  // Mole_warCapital.cs: InitWarCapital (SendMessage in the spawn frame, Mole.cs:14451; coroutine :313-382):
  // animation.Play("open") Once (:366-369; the default clip, playing from the spawn), Yield(2, 1) (:381), Play("root"),
  // wrapMode Loop (:327-332). The operational message (:342) is a game message: left out (decision 51). Its volleys come
  // after the 10 s cut (decision 50); it stands until its cue's kill. The Animation is looked up when due (the root's
  // parts are built before its later components).
  api.part("Mole_warCapital", (fx, node) => {
    let done = false;
    return { node, update() {
      if (done || fx.age < 1) return;
      done = true;
      const a = node.userData.fxAnim || fx.nodes.find(o => o.userData.fxAnim)?.userData.fxAnim;
      if (!a?.play) warnOnce("wc-anim", "effect part Mole_warCapital: no Animation on warCapital (fxparts/mesh.js)");
      else if (!a.play("root", 0, LOOP)) warnOnce("wc-root", "effect part Mole_warCapital: no clip root");
    } };
  });

  // ---------------------------------------------------------------- fx:flameCarnival (part 4, decision 26: built, unused)
  // The trap is never triggered on the page (the 10 m target is outside its 4 m sphere), so no cue sets `trigger`; when one
  // does (`trigger`: the effect's age at which a foe walks in), the hero's coroutine $RPC_flameCarnival_fire$23930
  // (Mole.cs:38844-39256) runs: the trap's animation.Play("open") + audio.Play() (:39198-39201), Yield(2, 0.3) (:39252),
  // flameCarnival_fire at the trap, identity (:38980; its rotationControl spin is rotationcontrol.js's), 20 pulses 0.3 s
  // apart (the damage only, :39033), Play("close") (:39047), Yield(4, 0.5) (:39248), Destroy the trap (:39014). The
  // entry would then build flameCarnival_fire. (Unity's AudioSource.Play restarts the clip: the old handle stopped, a new
  // one put in its fx.sounds entry, so Fx.dispose stops it: audiocontrol.js's way.)
  api.part("fx:flameCarnival", fx => {
    const T = num(fx.at?.trigger, null);
    if (T == null) return null;
    let k = 0;
    const anim = clip => {
      const a = fx.nodes.find(o => o.userData.fxAnim)?.userData.fxAnim;
      if (!a?.play?.(clip)) warnOnce("fc:" + clip, "effect part fx:flameCarnival: no clip", clip, "on flameCarnival");
    };
    return { node: fx.root, update() {
      const age = fx.age;
      if (k === 0 && age >= T) {
        k = 1; anim("open");
        const s = fx.sounds?.[0];
        if (s?.comp?.clip) { s.h?.stop(); s.h = api.Sound.play(fx.cls, s.comp.clip, s.comp.volume, !!s.comp.loop); }
      }
      if (k === 1 && age >= T + 0.3) { k = 2; spawn("fx:flameCarnival", "flameCarnival_fire", at3(fx.root.position, [0, 0, 0])); }
      if (k === 2 && age >= T + 6.3) { k = 3; anim("close"); }
      if (k === 3 && age >= T + 6.8) return "destroy";
    } };
  });

  // ---------------------------------------------------------------- data only (parts.md part 4)
  // Mole_mine / Mole_stunMine / Mole_flameCarnival: Init (Mole_mine.cs:31-114, Mole_stunMine.cs:31-114,
  // Mole_flameCarnival.cs:21-110) turns every renderer off only on an ENEMY's screen; the owner sees the device (the page's
  // view); the life (60 / 60 / 90 s) is the cue's kill 10 (decision 26); the trigger never comes. Nothing to draw.
  for (const type of ["Mole_mine", "Mole_stunMine", "Mole_flameCarnival"]) api.part(type, () => null);
}
