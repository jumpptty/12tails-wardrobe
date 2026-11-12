// wardrobe/fxparts/bat.js: the Bat's own effect scripts (agent bat_parts, 2026-11-13; plans/fx_bat/parts.md "Each part"
// 1-4 and its Verification, plans/fx_bat/skills_a.md Parts 1 / 3, the overnight decisions plans/fx_bat/decisions.md 4, 5,
// 15, 24-26, 43, and the loader comment above FX_PART_FILES in index.html). BB's DecompiledSource is the authority for
// every line cited here (D:\12tails\DecompiledSource\<file>); the prefab facts are checks/fx_bat_research/parts/probe*.txt.
//   Bat_nAttack / Bat_illusionFire  nAttack, illusion_fire: the 15 m/s bolt, its end on the ground; the Homing Wand's homing
//   Bat_echoes                      echoes: Echoes' three homing orbs
//   Bat_mirageOrb                   mirageOrb: the fading orb, its flash on each tick and its end after the 11th
//   Bat_guardianOfTheNight          guardian: the summon's walk-in, its AI's attacks (blade, two hits, swing sound), its
//                                   unsummon
//   fx:castRing                     the channel coroutines restarting castRing's Animation on "root", looped, at 0.5 s
// Space: every root here hangs in the effect's mirror group (Unity's world, the hero's feet at the origin, +z her facing),
// so node.position is the game's transform.position and the numbers below are the game's own.
//
// The target (decisions.md 4, as the Penguin's decision 3): one body for every Bat cue, a Penguin-sized
// CharacterController (centre 0.6 m up, height 1, radius 0.3: its capsule's axis is the centre +- 0.2 m) standing at the
// cue's `to`; the homing parts aim at its centre (the cue's `to`, default (0, 0.6, 10)), the guardian and the Mirage Orb
// read its feet (default (0, 0, 10)), and the target faces the hero (the rot [0, 180, 0] rule: its forward (0, 0, -1)).
//
// Page hooks used: node.userData.fxAnim.play(name, fade, wrap) (mesh.js; wrap = Unity's animation.wrapMode set after the
// Play: 1 Once, 2 Loop); api.worn("R") (the main weapon's wardrobe name); api.spawn(name, at, opts) (index.html, the
// page_pipeline builder: an effect of the class's fx.json, placed by cue options, opts.followNode / opts.local to ride
// another effect's node); api.Sound.play(cls, name, vol, loop); the Opaque1 materials' two passes (mesh.js, userData.fxBlend
// / fxPass); an emitter's dispose() (index.html Fx.dispose).

export default function register(api) {
  const { THREE, V } = api;
  const STEP = 0.02;                                   // Unity's fixed timestep (FixedUpdate, 50 per second)
  const F = Math.fround, STEPF = F(0.02);              // Unity's float clock (Time.time, fixedTime) and its float step
  const ONCE = 1, LOOP = 2;                            // UnityEngine.WrapMode
  const BODY_HALF = 0.2, BODY_R = 0.3;                 // the target's capsule: axis = centre +- 0.2 m, radius 0.3 m
  const warned = new Set();
  const warnOnce = (k, ...m) => { if (!warned.has(k)) { warned.add(k); console.warn(...m); } };
  const clamp01 = x => Math.min(1, Math.max(0, x));
  const lerp = (a, b, u) => a + (b - a) * clamp01(u);  // Mathf.Lerp clamps u
  const target = (fx, dflt) => (Array.isArray(fx.at?.to) ? V(fx.at.to[0], fx.at.to[1], fx.at.to[2]) : dflt.clone());
  // Animation.Play / CrossFade with the wrap mode the script sets right after it (mesh.js play(name, fade, wrap))
  const play = (fx, node, name, fade, wrap) => {
    const a = node.userData.fxAnim;
    if (!a?.play) return warnOnce("anim:" + fx.name, "effect part (bat.js): no Animation play() on", fx.name, "(fxparts/mesh.js)");
    if (!a.play(name, fade, wrap)) warnOnce("clip:" + fx.name + name, "effect part (bat.js): no clip", name, "on", fx.name);
  };
  // Quaternion.LookRotation(forward, Vector3.up) in Unity's numbers (penguin.js's)
  const lookRot = (f, q = new THREE.Quaternion()) => {
    const z = f.clone().normalize(), x = V().crossVectors(V(0, 1, 0), z);
    if (x.lengthSq() < 1e-12) x.set(1, 0, 0); x.normalize();
    return q.setFromRotationMatrix(new THREE.Matrix4().makeBasis(x, V().crossVectors(z, x), z));
  };
  // Vector3.RotateTowards's direction (penguin.js's): from a toward b by at most maxRad, the magnitude dropped
  const rotateTowards = (a, b, maxRad) => {
    const u = a.clone().normalize(), w = b.clone().normalize(), ang = Math.acos(Math.min(1, Math.max(-1, u.dot(w))));
    if (ang <= maxRad || ang < 1e-9) return w;
    const s = Math.sin(ang);
    if (s < 1e-6) {                                    // opposite: Unity turns about some perpendicular axis
      const ax = Math.abs(u.y) < 0.99 ? V().crossVectors(u, V(0, 1, 0)).normalize() : V(1, 0, 0);
      return u.applyAxisAngle(ax, maxRad);
    }
    return u.multiplyScalar(Math.sin(ang - maxRad) / s).addScaledVector(w, Math.sin(maxRad) / s);
  };
  // penguin.js's stepper: a rigidbody stepped at Unity's 50 Hz, step(k) = FixedUpdate k's velocity (or "destroy"), after(p)
  // = the trigger test once the physics moved it; drawn between steps along the segment the next step takes
  const stepper = (node, step, after) => {
    let acc = 0, k = 0, vNext = step(++k);
    const p = node.position.clone();
    return dt => {
      if (vNext === "destroy") return "destroy";
      acc += dt;
      while (acc >= STEP) {
        acc -= STEP;
        p.addScaledVector(vNext, STEP);
        node.position.copy(p);
        if (after?.(p) === "destroy") return "destroy";
        vNext = step(++k);
        if (vNext === "destroy") return "destroy";
      }
      node.position.copy(p).addScaledVector(vNext, acc);
      node.updateMatrixWorld(true);                    // the parts after this one this frame (trails, emitters) see the move
    };
  };
  // the distance from p to the target body's axis (the capsule's segment: its centre c +- BODY_HALF in height)
  const onAxis = V();
  const toAxis = (p, c) => p.distanceTo(onAxis.set(c.x, Math.min(c.y + BODY_HALF, Math.max(c.y - BODY_HALF, p.y)), c.z));

  // ---------------------------------------------------------------- Bat_nAttack / Bat_illusionFire (nAttack, illusion_fire)
  // The same code twice (Bat_nAttack.cs, Bat_illusionFire.cs): Awake velocity = TransformDirection(ProjectileControl.velocity)
  // = (0, 0, 15) (:51 in both; prefab, probe.txt): 15 m/s along the spawn rotation (the cue's rot,
  // FromToRotation(forward, fireDir), Bat.cs:10746-10788). Life = 1.25 x rangeMod (Bat.cs:10762, :10883): FixedUpdate's clock
  // += dt, Destroy at it (Bat_nAttack.cs:86-89). Rigidbody: no gravity, rotation frozen; SphereCollider 0.4 m.
  // The end on the ground (decisions.md 1, the Penguin's decision 1 / the Sheep's 3): OnTriggerEnter destroys the bolt on any
  // collider not on the owner's layer nor 1 / 2, the floor included (:138-366); the bolt ends when its CENTRE reaches y 0, the
  // cue's aim putting that at the 10 m target point; its children (ImageEmitters, VortexEmitter, the TrailRenderer:
  // vortex.js, trail.js) hang under the root and go with it. The hit effect it asks for (RPC_nAttack_hit) is the cue's.
  // The Homing Wand (decision 15; parts.md Q2): InitHoming only with weapon == "w_bat59" and a target (Bat.cs:10765-10788;
  // the clones' bolts need the clone's copied weapon w_bat59 and Illusion Effect #401, Bat_illusionFire.cs:103-124, on with
  // the passives rule): w_bat59 = "specialWand" (wardrobe/data/item_map.json, the only code with that model), the worn main
  // weapon read when the bolt is made, as InitHoming reads it. Homing FixedUpdate (Bat_nAttack.cs:79-125): unless next >=
  // Time.time (:107): next = now + 0.1 (:113), forward = RotateTowards(forward, target.collider.bounds.center - position,
  // 0.1 rad, 1) (:116), rotation = LookRotation (:119), velocity = TransformDirection((0, 0, 16)) (:122, the ctor's :26):
  // 16 m/s from the first turn, which is the first FixedUpdate (next starts at 0). Ends: the 0.4 m sphere touching the body
  // (its centre within 0.4 + 0.3 m of the capsule's axis), the floor (centre at y 0), or the 1.25 s life. From (0, 1.3, 1)
  // it meets the body 0.54 s after the spawn (checks/fx_bat_research/parts/calc.txt; stage 3's side bolts at +-1 m, yaw
  // +-15, come back and meet it at 0.54 s too).
  // APPROXIMATED: the turn every 5 fixed steps (0.1 s, the spec); the game's float Time.time makes the `>=` skip the 5th
  // step now and then (the Penguin's missile_sim.py found mostly 6-step turns at the game's clock values), a few mm here.
  const HOMING_WAND = "specialWand", BOLT_LIFE = 1.25, BOLT_REACH = 0.4 + BODY_R;
  const bolt = (fx, node) => {
    const homing = api.worn?.("R") === HOMING_WAND;
    const q0 = fx.uQuat(node);
    if (!homing) {
      const vel = V(0, 0, 15).applyQuaternion(q0);   // TransformDirection at the spawn
      let t = 0;
      return { node, update(dt) {
        t += dt;
        if (t >= BOLT_LIFE) return "destroy";
        node.position.addScaledVector(vel, dt);
        if (vel.y < 0 && node.position.y <= 0) return "destroy";   // met the floor (decisions.md 1)
        node.updateMatrixWorld(true);
      } };
    }
    const to = target(fx, V(0, 0.6, 10));
    let fwd = V(0, 0, 1).applyQuaternion(q0);
    const toward = V(), q = new THREE.Quaternion();
    const move = stepper(node, k => {
      if (k * STEP >= BOLT_LIFE - 1e-9) return "destroy";          // clock >= life (:86-89)
      if ((k - 1) % 5 === 0) {                                      // the first FixedUpdate, then every 0.1 s
        fwd = rotateTowards(fwd, toward.subVectors(to, node.position), 0.1);
        node.quaternion.copy(lookRot(fwd, q));
      }
      return fwd.clone().multiplyScalar(16);
    }, p => {
      if (toAxis(p, to) <= BOLT_REACH || p.y <= 0) return "destroy";
    });
    return { node, update: dt => move(dt) };
  };
  api.part("Bat_nAttack", bolt);
  api.part("Bat_illusionFire", bolt);

  // ---------------------------------------------------------------- Bat_echoes (echoes)
  // Awake (Bat_echoes.cs:23-46): velocity = TransformDirection(ProjectileControl.velocity) = (0, 0, 4) (:36): 4 m/s along
  // the spawn rotation (RPC_echoes_fire's LookRotation(fireDir), Bat.cs:11835; the cue's rot: Math.rotateH(forward, 120 i)
  // = yaw 0 / -120 / +120, Math.cs:838-843). ProjectileControl.life = 5 x rangeMod (Bat.cs:11844). Update (:48-188), per
  // frame: clock += dt, at life RPC_echoes_hit at its own spot and Destroy (:66-141); with a target, unless next >= Time.time
  // (:153): next = now + 0.1 (:159), forward = RotateTowards(forward, target.collider.bounds.center - position, 0.5 rad, 1)
  // (:164), rotation = LookRotation (:169), velocity re-set to TransformDirection((0, 0, 4)) (:174). The Rigidbody (no
  // gravity, rotation frozen) moves it at 50 Hz between those Updates. OnTriggerEnter (:190-555): its 0.3 m BoxCollider
  // (half 0.15) meeting a foe's collider destroys it (:287), the hit effect echoes_hit at the target's ClosestPointOnBounds
  // (:308; the cue's, at d 9.7: parts.md Verification correction 1); the bounce to another foe (:369-530) needs a second
  // foe: none here. The floor is not a foe (the tag test): it flies on through it.
  // On the page: the turn on the frame clock (the first at once), the move in 50 Hz steps, the contact after each step when
  // the centre comes within 0.15 + 0.3 m of the body's axis (calc.txt's sim: contact 2.42 s after the spawn for orb 0, 2.60 s
  // for the +-120 ones, the same at 30-144 fps), else the 5 s life.
  // APPROXIMATED: a turn falls due when the frame clock reaches next to within 1e-6 s (calc.py's own tolerance). The game's
  // strict `<` on its float clock makes a frame landing exactly 0.1 s on a coin flip; taken as passing, the turns come every
  // 0.1 s at 30 / 60 fps and the contacts match the cues' 2.42 / 2.60 s (strict, the +-120 orbs met it 1-2 frames late).
  const ECHO_REACH = 0.15 + BODY_R, TURN_EPS = 1e-6;
  api.part("Bat_echoes", (fx, node) => {
    const to = target(fx, V(0, 0.6, 10));
    let fwd = V(0, 0, 1).applyQuaternion(fx.uQuat(node)), t = 0, next = -1, acc = 0;
    const vel = fwd.clone().multiplyScalar(4), p = node.position.clone(), toward = V(), q = new THREE.Quaternion();
    return { node, update(dt) {
      if (t >= 5) return "destroy";                    // clock >= life (:66-69)
      if (next < t + TURN_EPS) {                       // next >= Time.time: skip (:153)
        next = t + 0.1;
        fwd = rotateTowards(fwd, toward.subVectors(to, p), 0.5);
        node.quaternion.copy(lookRot(fwd, q));
        vel.copy(fwd).multiplyScalar(4);
      }
      t += dt; acc += dt;
      while (acc >= STEP) {                            // the physics: p += v x 0.02, then the trigger
        acc -= STEP;
        p.addScaledVector(vel, STEP);
        if (toAxis(p, to) <= ECHO_REACH) { node.position.copy(p); return "destroy"; }
      }
      node.position.copy(p).addScaledVector(vel, acc);
      node.updateMatrixWorld(true);
    } };
  });

  // ---------------------------------------------------------------- Bat_mirageOrb (mirageOrb)
  // ctor: its colour (0.5, 0.5, 0.5, 0.5) (Bat_mirageOrb.cs:26). Init (:45-130; Bat.cs:12799): L = sLv + (Distant Orb #403 ?
  // 2 : 0) = 6 at max with the passive; isVisible true for the owner's side (:96). Update (:134-258): destroyed at its end
  // time (chaAdjust(30), 30 s: the cue's kill 10 covers it, the 10 s rule), its owner gone or down, or once its damage total
  // > 60 L - 10 = 350 (:185, :208); else every frame a = Lerp(a, 0.05, 5 dt) (:230) and renderer.material's _TintColor =
  // (0.5, 0.5, 0.5, a) (:244). OnTriggerStay (:263-360): a foe inside its 1 m SphereCollider, unless next >= Time.time
  // (:286): next = now + 0.5 (:316), a = 0.4 (:319, the flash), total += 6 L - 1 = 35 (:343). So with the target inside
  // (Distant Orb puts the orb at the target's feet: decisions.md 5) a flash at 0, 0.5, ... 5.0 s and gone after the 11th
  // (385 > 350): at 5.0 s. Without one it fades to 0.05 and lives to the cue's kill.
  // On the page: renderer.material is the renderer's own copy (alphatimer.js's own(): cloned per spawn, onBeforeCompile kept);
  // the mesh's additive material (Particles/Additive, _TintColor) takes opacity = min(1, 2 a) (fxMaterial's saved-tint rule).
  // Inside = the cue's `to` (the target's feet, default (0, 0, 10)) within 1 + 0.3 m of the orb horizontally and the body's
  // height (0 .. 1 m above its feet) overlapping the sphere's (+-1 m). OnTriggerStay runs in the physics, so the ticks
  // are counted on 50 Hz steps from the spawn: the first at once, then every 25 steps (0.5 s; the game's float `>=` makes
  // a step landing exactly on next a coin flip, taken as passing, as parts.md's 5.0 s); before Update, whose destroy test
  // after the 11th tick comes on the next update, so the last flash is drawn once.
  const ORB_R = 1, ORB_TICKS = 11, ORB_EVERY = 25;
  let orbMats = [];                                    // [fx, material]: a clone freed once its effect is gone
  api.part("Bat_mirageOrb", (fx, node) => {
    orbMats = orbMats.filter(([f, m]) => f.alive || (m.dispose(), false));
    const to = target(fx, V(0, 0, 10));
    let mat, a = 0.5, acc = 0, k = 0, next = 0, ticks = 0, done = false, mine = null;
    return { node,
      dispose() { if (mine) { mine.dispose(); mine = null; } },
      update(dt) {
        if (mat === undefined) {                       // the first update: every part of the node is built by now
          mat = null;
          const mesh = node.children.find(x => x.isMesh);
          const list = mesh && (Array.isArray(mesh.material) ? mesh.material : [mesh.material]);
          const m = list?.[0];
          if (!m) warnOnce("orb:" + fx.name, "effect part Bat_mirageOrb: no mesh material on", fx.name, "(fxparts/mesh.js)");
          else {
            mat = mine = m.clone(); mat.onBeforeCompile = m.onBeforeCompile;   // Material.copy leaves it out
            if (Array.isArray(mesh.material)) mesh.material[0] = mat; else mesh.material = mat;
            orbMats.push([fx, mat]);
          }
        }
        if (done) return "destroy";                    // total > 60 L - 10 (:185)
        const p = node.position;
        const inside = Math.hypot(to.x - p.x, to.z - p.z) <= ORB_R + BODY_R && to.y + 1 >= p.y - ORB_R && to.y <= p.y + ORB_R;
        const tick = () => {                           // OnTriggerStay, unless next >= Time.time (:286, :316-343)
          if (!inside || done || k < next) return;
          next = k + ORB_EVERY; a = 0.4;
          if (++ticks >= ORB_TICKS) done = true;
        };
        if (k === 0 && next === 0) tick();             // the first at once
        for (acc += dt; acc >= STEP; acc -= STEP) { k++; tick(); }
        a += (0.05 - a) * Math.min(1, 5 * dt);         // Lerp(a, 0.05, 5 dt) (:230)
        if (mat) mat.opacity = Math.min(1, 2 * a);
      } };
  });

  // ---------------------------------------------------------------- Bat_guardianOfTheNight (guardian)
  // The summon (Bat.cs:30549-30609): Instantiate(guardian, hero - 4 x forward, hero rotation) (:30561; the cue's d -4),
  // StartCoroutine(Init(bat, sLv)) (:30586), the AI's first scan 4 s on (:30614 Qypvswnda4 = Time.time + 4: decisions.md
  // 24; parts.md's "the frame after the summon" is wrong). State (eGuardianOfTheNightState): init, standby, attack,
  // castSpell, unsummon; ONE clock t0 (a4pGjxUjoI) shared by every coroutine.
  //   Init (WaitForFixedUpdate, Bat_guardianOfTheNight.cs:283-470): t0 = now, Play("walk") Loop (:433-439); each fixed step
  //     until t0 + 1 <= now (:323): position = Lerp(owner - 4 fwd, owner - 2 fwd, now - t0) (:338), materials[0].color.a =
  //     Lerp(0, 0.8, ...) (:351-378), materials[1].color.a = Lerp(0, 1, ...) (:383-406); then state = standby, t0 = now
  //     (:306-311).
  //   Update (:32-105), standby only: farther than 3 m from the owner (:57) CrossFade("walk", 0.1) Loop, position =
  //     Lerp(position, owner + 2 dir, dt), rotation = Lerp(rotation, LookRotation(-dir), 2 dt) (:63-80); else
  //     CrossFade("root", 0.2) Loop (:86-91).
  //   The Bat's AI (Bat.GuardianOfTheNight, Bat.cs:12275-12442, from her Update): while her timer runs (:12298), unless
  //     Qypvswnda4 >= Time.time (:12313): Qypvswnda4 = now + 2.5 (:12321), a random living foe within FindAreaTarget(Bat,
  //     32, 12) (:12331-12345), closer than 16 m (:12394) -> RPC_guardian_attack(foe.position, foe.forward) (:12400); else
  //     50 % castSpell (:12414-12422: only beyond 16 m, never with the 10 m target: not built). Timer out ->
  //     RPC_guardian_unsummon (:12436-12442).
  //   attack(mPos, tDir) (WaitForFixedUpdate, :622-1420), tDir = the FOE's forward: only from standby (:1375-1381): state =
  //     attack, t0 = now, CrossFade("root", 0.2) Loop (:1384-1393); five phases, each ending at the first resume with
  //     t0 + 0.5 <= now, its end setting t0 = now and running the next phase's step at once; every resume first checks
  //     state == attack (:637-677: an unsummon aborts it):
  //       A (:1111-1179) body a = Lerp(0.8, 0, 2 (now - t0)), wings Lerp(1, 0, ..): fade out where it stands; its end
  //         (:1015-1100): position = mPos - 6 tDir, rotation = LookRotation(tDir), Play("nAttack") Once, PlayOneShot Shade4
  //         Sounds/nAttack (:1047-1059), guardianBlade instantiated on the `sword` bone, localPosition (-1.1, 0, 0),
  //         localRotation Euler(0, 180, 90) (:1079-1094)
  //       B (:927-1012) position = Lerp(mPos - 8 tDir, mPos - 2 tDir, 2 (now - t0)), fade in (0 -> 0.8 / 1); its end
  //         (:809-918): every foe within FindAreaTarget(guardian, 4, 3) -> RPC_guardian_hit(its ClosestPointOnBounds(
  //         guardian + up)) (:848-893): Shade4 Effects/nAttack_hit there, Quaternion.identity (Bat.cs:12606-12619)
  //       C (:1367) position = Slerp(mPos - 2 tDir, mPos + tDir, ..) (alphas as B left them); its end the second hit
  //         (:1276-1358)
  //       D (:729-806) position = Slerp(mPos + tDir, mPos + 4 tDir, ..), fade out; its end (:694-720): Play("root") Loop,
  //         position = owner - 2 owner.forward
  //       E (:1217-1271) fade in, Lerp(0, 0.8 / 1, (now - t0) / 0.5); its end (:1184-1195): state = standby, t0 = now
  //   unsummon (:1998-2121): state = unsummon, Play("ko") Once (:2030-2036), both alphas full (0.8 / 1, :2057-2090),
  //     WaitForSeconds(2) (:2119), Destroy (:2012): its looping guardian_ring sound (a Shade4 clip) goes with it.
  // On the page (parts.md part 4, decisions.md 24-26): the owner is the hero (origin, facing +z), the foe the target at the
  // cue's `to` (its feet, default (0, 0, 10)) facing the hero (forward (0, 0, -1), the rot [0, 180, 0] rule), so every scan
  // that finds the guardian in standby attacks: behind the target at z 16, the dash z 18 -> 12, hit 1 at (0, 1, 10.3), the
  // cut through to z 9, hit 2 at (0, 1, 9.7), on to z 6, back 2 m behind the hero, fade in. The unsummon at the cue's `end`
  // (seconds after the spawn, the 10 s rule; skills_a's `unsummon` taken too), "destroy" 2 s after it. The hits, the blade
  // trail and the swing sound are this part's (decisions.md 26): api.spawn / api.Sound.
  // The clocks: the frame clock (now, the page's dt sum) for Update, the AI and the unsummon's wait; the fixed steps at
  // float sums of 0.02 from the spawn, run before Update each frame (Unity's order), Init before attack in a step (it was
  // started first); every Time.time compare in float (Math.fround). An attack starts inside the Bat's Update (the
  // coroutine's first pass runs in StartCoroutine): its t0 is the frame's time and its first phase-A step runs at once.
  // The two materials: Unity's renderer.materials are the renderer's own copies, so the skinned mesh's whole list is cloned
  // per spawn (mesh.js shares one per class and name): materials[0] guardian1 FX/Phoenix -> opacity = a (alphatimer.js's
  // Phoenix rule: alpha = texture.a x _Color.a); materials[1] guardian2 Transparent/Opaque1 -> every pass's opacity = a
  // (both passes: pass 1 ZWrite Off, AlphaTest GEqual 0.95; pass 2 ZWrite On). Its legacy emitter on Spine1 hangs under the
  // bone node the Animation poses, so it follows the skinned body as it is.
  // APPROXIMATED: Vector3.Slerp of two world positions as a lerp (far from the world origin in the game it is one to within
  // mm: parts.md); the float clock counted from the spawn, not the game's absolute Time.time (which phase step lands on
  // t0 + 0.5 can differ by one step, 0.02 s); Quaternion.Lerp as a slerp (standby's walk-after, never used here).
  const GUARD_ATTACK_R2 = 256, GUARD_SCAN_R = 32, GUARD_HIT_R = 4;
  const PHOENIX = "shader:FX/Phoenix", OPAQUE1 = "shader:Transparent/Opaque1";
  let guardMats = [];                                  // [fx, material]: clones freed once their effect is gone
  api.part("Bat_guardianOfTheNight", (fx, node) => {
    guardMats = guardMats.filter(([f, m]) => f.alive || (m.dispose(), false));
    const INIT = 0, STANDBY = 1, ATTACK = 2, UNSUMMON = 4;
    const owner = V(0, 0, 0), ownerFwd = V(0, 0, 1);
    const mPos = target(fx, V(0, 0, 10)), tDir = V(0, 0, -1);
    const end = Number(fx.at?.end ?? fx.at?.unsummon ?? 10);
    // the sword bone, looked up when the blade is due: this part is built with the root node, before the later nodes are
    // named (index.html Fx: nodes are filled in order), so a lookup here finds nothing
    let sword = null;
    let state = INIT, t0 = 0, now = 0, T = 0, started = false, scanAt = F(4), unsummonAt = null;
    let bodyA = 0, wingA = 0, body = [], wings = [], matsFound = false;
    const mine = [], blades = [], sounds = [];
    const at = (a, k, b) => V().copy(a).addScaledVector(b, k);    // a + k x b
    const setPos = v => { node.position.copy(v); };
    const alphas = (b, w) => { bodyA = b; wingA = w; };
    const apply = () => {
      if (!matsFound) {                                // the first update: the skinned mesh (node Shade4_tri) is built by now
        matsFound = true;
        let mesh = null;
        for (const o of fx.nodes) { mesh = o.children.find(x => x.isSkinnedMesh) || null; if (mesh) break; }
        const list = mesh && (Array.isArray(mesh.material) ? mesh.material : [mesh.material]);
        if (!list?.length) warnOnce("guard:" + fx.name, "effect part Bat_guardianOfTheNight: no skinned mesh materials on", fx.name, "(fxparts/mesh.js)");
        else {
          const cl = list.map(m => { const c = m.clone(); c.onBeforeCompile = m.onBeforeCompile; mine.push(c); guardMats.push([fx, c]); return c; });
          mesh.material = Array.isArray(mesh.material) ? cl : cl[0];
          body = cl.filter(m => m.userData?.fxBlend === PHOENIX);
          wings = cl.filter(m => m.userData?.fxBlend === OPAQUE1);
          if (!body.length || !wings.length) warnOnce("guardmats:" + fx.name, "effect part Bat_guardianOfTheNight:", body.length,
            "FX/Phoenix and", wings.length, "Transparent/Opaque1 materials on", fx.name, "(expected guardian1 / guardian2)");
        }
      }
      for (const m of body) m.opacity = bodyA;
      for (const m of wings) m.opacity = wingA;
    };
    const spawn = (name, where, opts) => {
      if (!api.spawn) { warnOnce("spawn", "effect part Bat_guardianOfTheNight: no api.spawn (index.html):", name, "not drawn"); return null; }
      return api.spawn(name, where, opts);
    };
    // the hit: RPC_guardian_hit at the foe's ClosestPointOnBounds(guardian + up), when it stands within FindAreaTarget(
    // guardian, 4, 3); the target's box: x / z +- 0.3 about its feet, y from 0.1 to 1.1 above them (the body above)
    const hit = () => {
      const p = node.position;
      if (Math.hypot(mPos.x - p.x, mPos.z - p.z) > GUARD_HIT_R) return;
      const c = V(Math.min(mPos.x + BODY_R, Math.max(mPos.x - BODY_R, p.x)),
        Math.min(mPos.y + 0.6 + 0.5, Math.max(mPos.y + 0.6 - 0.5, p.y + 1)),
        Math.min(mPos.z + BODY_R, Math.max(mPos.z - BODY_R, p.z)));
      spawn("guardian_hit", { x: c.x, y: c.y, d: c.z });   // Quaternion.identity: no rot
    };
    // ---- the coroutines, each a step(T) run at a fixed step (or, for attack's first pass, in Update): false = finished
    const co = [];
    const init = { step(T) {
      if (F(t0 + 1) <= T) { state = STANDBY; t0 = T; return false; }   // :306-323
      const u = F(T - t0);
      setPos(V().lerpVectors(at(owner, -4, ownerFwd), at(owner, -2, ownerFwd), clamp01(u)));
      alphas(lerp(0, 0.8, u), lerp(0, 1, u));
      return true;
    } };
    const attack = () => {
      let phase = 0;
      const u2 = T => F(2 * F(T - t0));
      const steps = [
        T => alphas(lerp(0.8, 0, u2(T)), lerp(1, 0, u2(T))),                                                   // A
        T => { setPos(V().lerpVectors(at(mPos, -8, tDir), at(mPos, -2, tDir), clamp01(u2(T)))); alphas(lerp(0, 0.8, u2(T)), lerp(0, 1, u2(T))); },   // B
        T => setPos(V().lerpVectors(at(mPos, -2, tDir), at(mPos, 1, tDir), clamp01(u2(T)))),                   // C
        T => { setPos(V().lerpVectors(at(mPos, 1, tDir), at(mPos, 4, tDir), clamp01(u2(T)))); alphas(lerp(0.8, 0, u2(T)), lerp(1, 0, u2(T))); },     // D
        T => { const u = F(F(T - t0) / 0.5); alphas(lerp(0, 0.8, u), lerp(0, 1, u)); },                       // E
      ];
      const ends = [
        () => {                                                                                                // A
          setPos(at(mPos, -6, tDir)); node.quaternion.copy(lookRot(tDir));
          play(fx, node, "nAttack", 0, ONCE);
          sounds.push(api.Sound.play(fx.cls, "guardian_nAttack"));
          sword ||= fx.nodes.find(o => o.name === "sword") || null;
          if (!sword) warnOnce("sword:" + fx.name, "effect part Bat_guardianOfTheNight: no `sword` node on", fx.name);
          else { const b = spawn("guardian_blade", {}, { followNode: sword, local: { pos: [-1.1, 0, 0], rot: [0, 180, 90] } }); if (b) blades.push(b); }
        },
        hit,                                                                                                   // B
        hit,                                                                                                   // C
        () => { play(fx, node, "root", 0, LOOP); setPos(at(owner, -2, ownerFwd)); },                          // D
        () => { state = STANDBY; },                                                                            // E
      ];
      return { step(T) {
        if (state !== ATTACK) return false;            // every resume (:637-677)
        if (F(t0 + 0.5) <= T) {
          ends[phase]();
          t0 = T;
          if (++phase > 4) return false;
        }
        steps[phase](T);
        return true;
      } };
    };
    const startAttack = () => {                        // RPC_guardian_attack -> StartCoroutine(attack), in the Bat's Update
      if (state !== STANDBY) return;                   // :1375-1381
      state = ATTACK; t0 = F(now);
      play(fx, node, "root", 0.2, LOOP);
      const a = attack();
      if (a.step(t0)) co.push(a);                      // its first pass, up to the first WaitForFixedUpdate
    };
    const unsummon = () => {                           // RPC_guardian_unsummon
      state = UNSUMMON; unsummonAt = now;
      play(fx, node, "ko", 0, ONCE);
      alphas(0.8, 1);
    };
    const q = new THREE.Quaternion();
    return { node,
      dispose() {
        for (const m of mine) m.dispose(); mine.length = 0;
        for (const b of blades) if (b.alive) b.dispose();      // the blade hangs on its sword bone: Destroy takes it too
        for (const h of sounds) h?.stop?.();                   // PlayOneShot on its own AudioSource
      },
      update(dt) {
        if (!started) {                                // Init's first pass, in the spawn's frame (:433-439)
          started = true; t0 = 0;
          play(fx, node, "walk", 0, LOOP);
          if (init.step(0)) co.push(init);
        }
        now += dt;
        // the fixed steps due by this frame, each resuming the coroutines in the order they were started
        for (let Tn = F(T + STEPF); Tn <= now; Tn = F(T + STEPF)) {
          T = Tn;
          for (let i = 0; i < co.length; i++) if (!co[i].step(T)) co.splice(i--, 1);
        }
        // Update: the Bat's (her timer, the AI's scan), then the guardian's (the standby follow)
        if (unsummonAt == null) {
          if (!(F(end) >= F(now))) unsummon();          // xMnv4YLKcX >= Time.time, else unsummon (:12298, :12436)
          else if (!(scanAt >= F(now))) {               // Qypvswnda4 >= Time.time: skip (:12313)
            scanAt = F(F(now) + 2.5);
            const d2 = (mPos.x - owner.x) ** 2 + (mPos.z - owner.z) ** 2;
            if (d2 <= GUARD_SCAN_R * GUARD_SCAN_R) {
              if (d2 + (mPos.y - owner.y) ** 2 < GUARD_ATTACK_R2) startAttack();
              else warnOnce("cast", "effect part Bat_guardianOfTheNight: a foe beyond 16 m means castSpell, not built");
            }
          }
        } else if (now >= unsummonAt + 2) return "destroy";      // WaitForSeconds(2), Destroy (:2012, :2119)
        if (state === STANDBY) {
          const a = V().subVectors(node.position, owner);
          if (a.lengthSq() > 9) {
            play(fx, node, "walk", 0.1, LOOP);
            node.position.lerp(at(owner, 2, a.clone().normalize()), clamp01(dt));
            node.quaternion.slerp(lookRot(a.clone().negate(), q), clamp01(2 * dt));
          } else play(fx, node, "root", 0.2, LOOP);
        }
        apply();
        node.updateMatrixWorld(true);                  // the parts after this one (the Spine1 emitter, the blade) see the move
      } };
  });

  // ---------------------------------------------------------------- fx:castRing (the Bat's castRing)
  // The channel coroutines restart the ring's Animation 0.5 s after spawning it: animation.Play("root"), wrapMode = Loop
  // (Bat.cs:29968-29973 Guardian of the Night, :42864-42869 Nefarious Whip, :44323-44328 Black Servant; cast1's :23102-23107,
  // where the cut at 0.65 s comes first) (skills_a.md Parts 3, decisions.md 43): 0.2 + 0.5 = 0.7 s into bigCast1, the ring
  // then turning on its 2 s root loop until the release cuts it. Not after a cut (followState already played "destroy").
  // The Bat's only: the hook is keyed by the effect's name, and the Sheep's / Penguin's castRing (their own prefabs, their
  // own code) are not traced here.
  api.part("fx:castRing", (fx, node) => {
    if (fx.cls !== "bat") return null;
    let t = 0, done = false;
    return { node, update(dt) {
      if (done || (t += dt) < 0.5) return;
      done = true;
      if (fx.stopped || (fx.cutAt != null && api.FX.t >= fx.cutAt)) return;
      const a = node.userData.fxAnim;
      if (!a?.play) warnOnce("ring:" + fx.name, "effect part fx:castRing: no Animation play() on", fx.name, "(fxparts/mesh.js)");
      else if (!a.play("root", 0, LOOP)) warnOnce("ringclip:" + fx.name, "effect part fx:castRing: no root clip on", fx.name);
    } };
  });
}
