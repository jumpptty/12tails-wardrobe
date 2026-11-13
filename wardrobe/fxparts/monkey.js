// wardrobe/fxparts/monkey.js: the Monkey's own effect scripts and the hero's code acting on her effects (builder "monkey",
// 2026-11-13; plans/fx_monkey/parts.md parts 1, 2, 6 with its Verification 6, 7, 9; skills_b.md "Parts needed" 5,
// skills_a.md Verification 4, attacks_emotes.md Verification 2; the overnight decisions plans/fx_monkey/decisions.md 2, 3,
// 21, 22, 24, 38, which win over the reports; the loader comment above FX_PART_FILES in index.html). BB's DecompiledSource
// is the authority for every line cited here (C:\Users\Jump\Desktop\12tails\DecompiledSource\<file> at the office,
// D:\12tails\... at home; opaque predicates worked by hand).
//   Monkey_fireBall / Monkey_earthPulse / Phoenix_fireBall / Phoenix_skyCrimson_fire   the four straight shots: flight,
//                       the hit each spawns on the target body or the floor (part-spawned: the entries' "builds")
//   Monkey_lavu         the serpent: summon flight, standby circling, the trail chain, upheaval, unsummon (cue options
//                       lavu, release, unsummon)
//   fx:mikeBlink        Mike Blink: the worn R piece (or the starter noviceMike) carried on the effect's mount_Summon
// Not here: Rotate (fxparts/rotationcontrol.js), FX/Lavu (fxparts/mesh.js), rotationControl on the lavu's models
// (rotationcontrol.js, the Mole's), Monkey_runicFlame / _runicSand (data only: parts.md part 4, the cue's kill).
// Space: every root here hangs in the effect's mirror group (Unity's world, the hero's feet at the origin, +z her facing,
// y 0 the floor), so node.position is the game's transform.position and the numbers below are the game's own.
// APPROXIMATED throughout: the page's world is the hero's space (the game's Vector3.forward / Quaternion.identity / a
// world Euler are taken as the hero's, who faces +z: true for every cue here, the Monkey never turns in a tile).
//
// The target (Bat decision 4, every class): one standard body, ClosestPointOnBounds = a point clamped into its box x
// +-0.3, y 0.1..1.1, z 9.7..10.3; the floor is y 0. The page has no other collider (a shot missing both flies its life out).

export default function register(api) {
  const { THREE, V } = api;
  const STEP = 0.02;                                   // Unity's fixed timestep (FixedUpdate, 50 per second)
  const DEG = Math.PI / 180;
  const BODY_MIN = V(-0.3, 0.1, 9.7), BODY_MAX = V(0.3, 1.1, 10.3);
  const warned = new Set();
  const warnOnce = (k, ...m) => { if (!warned.has(k)) { warned.add(k); console.warn(...m); } };
  const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
  const num = (x, dflt) => (x != null && x !== "" && Number.isFinite(+x) ? +x : dflt);
  const spawn = (who, name, at) => {
    if (!api.spawn) { warnOnce("spawn", `effect part ${who}: no api.spawn (index.html):`, name, "not drawn"); return null; }
    const f = api.spawn(name, at);
    if (!f) warnOnce("miss:" + name, `effect part ${who}: ${name} not in fx.json (the entry's "builds")`);
    return f;
  };
  // Quaternion.LookRotation(forward, Vector3.up) in Unity's numbers (mole.js's): a vertical forward keeps x = (1, 0, 0),
  // as Unity's (LookRotation(up) = Euler(-90, 0, 0))
  const lookRot = (f, q = new THREE.Quaternion()) => {
    const z = f.clone().normalize(), x = V().crossVectors(V(0, 1, 0), z);
    if (x.lengthSq() < 1e-12) x.set(1, 0, 0); x.normalize();
    return q.setFromRotationMatrix(new THREE.Matrix4().makeBasis(x, V().crossVectors(z, x), z));
  };
  // Vector3.RotateTowards's direction (mole.js's / bat.js's): from a toward b by at most maxRad, unit length
  const rotateTowards = (a, b, maxRad) => {
    const u = a.clone().normalize(), w = b.clone().normalize(), ang = Math.acos(clamp(u.dot(w), -1, 1));
    if (ang <= maxRad || ang < 1e-9) return w;
    const s = Math.sin(ang);
    if (s < 1e-6) return u.applyAxisAngle(Math.abs(u.y) < 0.99 ? V().crossVectors(u, V(0, 1, 0)).normalize() : V(1, 0, 0), maxRad);
    return u.multiplyScalar(Math.sin(ang - maxRad) / s).addScaledVector(w, Math.sin(maxRad) / s);
  };
  // Vector3.Slerp(a, b, t): the direction turned by the angle, the length lerped; t clamped to 0..1 (Unity's)
  const slerpV = (a, b, t) => {
    t = clamp(t, 0, 1);
    const la = a.length(), lb = b.length();
    if (la < 1e-6 || lb < 1e-6) return a.clone().lerp(b, t);
    const ang = Math.acos(clamp(a.dot(b) / (la * lb), -1, 1)), s = Math.sin(ang);
    if (s < 1e-6) return a.clone().lerp(b, t);         // APPROXIMATED: (anti)parallel, a lerp
    const d = a.clone().multiplyScalar(Math.sin((1 - t) * ang) / (s * la)).addScaledVector(b, Math.sin(t * ang) / (s * lb));
    return d.multiplyScalar(la + (lb - la) * t);
  };

  // ---------------------------------------------------------------- the straight shots (parts.md part 1, decisions 21-22)
  // One pattern on each prefab's root (ProjectileControl + the script + a trigger BoxCollider 0.25 x 0.25 x 0.5 centred on
  // the root + Rigidbody, gravity off, rotation frozen 112: re-probed 13/11/2026 from BB's resources.assets for all four):
  // the ctor's private velocity, Awake rigidbody.velocity = TransformDirection(it) along the spawn rotation (the cue's rot)
  // once; FixedUpdate the clock against ProjectileControl.life, Destroy at it; no LookAt (no gravity: the heading holds).
  // OnTriggerEnter: any collider not on the owner's layer / 1 / 2 -> Destroy and the hit RPC at mCollider.
  // ClosestPointOnBounds(this.collider.bounds.center): the shot's centre clamped into what it touched.
  //   script                    v (ctor)                     life                           hit, rotation
  //   Monkey_fireBall           30 (Monkey_fireBall.cs:26)   2 x rangeMod (Monkey.cs:11278)  fireBall_hit, the hero's (Monkey.cs:11318)
  //   Monkey_earthPulse         15 (Monkey_earthPulse.cs:26) 3 (Monkey.cs:13113)             earthPulse_hit, world Euler(270, 90, 0)
  //                                                                                          (Monkey.cs:32818; skills_a Verification 4)
  //   Phoenix_fireBall          30 (Phoenix_fireBall.cs:26)  2 x rangeMod (Phoenix.cs:1661)  phoenix_fireBall_hit, identity (Phoenix.cs:1768)
  //   Phoenix_skyCrimson_fire   16 (Phoenix_skyCrimson_fire.cs:28)  2 x rangeMod (Phoenix.cs:1822)  phoenix_skyCrimson_hit, identity
  //                             (Phoenix.cs:1856); it bursts ONLY on layer 0, the floor (Phoenix_skyCrimson_fire.cs:143-179):
  //                             the ball passes through the target body
  // (lives x rangeMod 1). Each 0.02 s step p += v x 0.02, then the contact: the target body (the shot's box, as its world
  // axis-aligned bounds from the spawn rotation, overlapping the body's box; hit = the centre clamped into the body box),
  // else the floor (the bounds' lowest point <= 0; hit under the centre, y 0). Drawn between steps along the velocity.
  // Monkey_earthPulse's hit is spawned by its RPC_earthPulse_hit coroutine at once (its five growing hits draw nothing).
  const SHOT = {
    Monkey_fireBall: { v: 30, life: 2, hit: "fireBall_hit", rot: [0, 0, 0], body: true },
    Monkey_earthPulse: { v: 15, life: 3, hit: "earthPulse_hit", rot: [270, 90, 0], body: true },
    Phoenix_fireBall: { v: 30, life: 2, hit: "phoenix_fireBall_hit", rot: [0, 0, 0], body: true },
    Phoenix_skyCrimson_fire: { v: 16, life: 2, hit: "phoenix_skyCrimson_hit", rot: [0, 0, 0], body: false },
  };
  const HALF = [0.125, 0.125, 0.25];
  const shot = type => (fx, node) => {
    const S = SHOT[type], q = fx.uQuat(node);
    const vel = V(0, 0, S.v).applyQuaternion(q);       // TransformDirection at the spawn (Awake)
    const m = new THREE.Matrix4().makeRotationFromQuaternion(q).elements;   // column-major
    const ext = [0, 1, 2].map(i => Math.abs(m[i]) * HALF[0] + Math.abs(m[4 + i]) * HALF[1] + Math.abs(m[8 + i]) * HALF[2]);
    const p = node.position.clone(), LIFE_STEPS = Math.round(S.life / STEP);
    let acc = 0, k = 0;
    const onBody = () => Math.abs(p.x - (BODY_MIN.x + BODY_MAX.x) / 2) <= 0.3 + ext[0] && p.y + ext[1] >= BODY_MIN.y &&
      p.y - ext[1] <= BODY_MAX.y && Math.abs(p.z - (BODY_MIN.z + BODY_MAX.z) / 2) <= 0.3 + ext[2];
    const land = hp => spawn(type, S.hit, { x: hp.x, y: hp.y, d: hp.z, rot: S.rot });
    return { node, update(dt) {
      acc += dt;
      while (acc >= STEP) {
        acc -= STEP;
        if (++k >= LIFE_STEPS) return "destroy";       // the clock at ProjectileControl.life: Destroy (FixedUpdate)
        p.addScaledVector(vel, STEP);
        if (S.body && onBody()) { node.position.copy(p); land(p.clone().clamp(BODY_MIN, BODY_MAX)); return "destroy"; }
        if (p.y - ext[1] <= 0) { node.position.copy(p); land(V(p.x, 0, p.z)); return "destroy"; }
      }
      node.position.copy(p).addScaledVector(vel, acc);
      node.updateMatrixWorld(true);                    // the trail's emitter after this part sees the move
    } };
  };
  for (const type of Object.keys(SHOT)) api.part(type, shot(type));

  // ---------------------------------------------------------------- Monkey_lavu (parts.md part 2, decisions 24, 38)
  // Monkey_lavu.cs (every field private, 0 bytes). Nodes: the root (the head end), its children body1-5 / tail 3 m apart
  // behind (z -3 .. -18), head, particle (Acid3, a legacy emitter). Cue options (fx.at):
  //   lavu      "summon" (default): summon() (:333-466): the six segments Find("body1".."body5", "tail") (:353-383), the
  //             trail h[8] = root, the six, tail (:388-420), the next sample 0.25 s on (:425); then each FixedUpdate
  //             Translate(10 forward dt) (:457) until t0 + 2 (:436) -> standby. Spawn (Monkey.cs:13899): hero +
  //             TransformDirection(0, -2, 3), LookRotation(forward) x Euler(-90, 0, 0): the cue's y -2 d 3 rot [-90, 0, 0],
  //             so it bursts up out of the floor and climbs 20 m in 2 s
  //             "upheaval": spawned already summoned (the same set-up), then upheaval() (:600-686) at once: while the
  //             summoner's action is "attack" with command "upheaval" (until `release`): target = summoner +
  //             rotateH(6 forward, Repeat(120 (t - t0), 360)) + up sin(4 t) (:632; Math.cs:838-842); the first 3 s position =
  //             Slerp(position, target, 0.33 (t - t0)), rotation = LookRotation(target - position) (:637-648), then position =
  //             target, rotation = Euler(-30 cos(4 t), -Repeat(90 + 120 (t - t0), 360), 0) (:657-662); then standby (:672)
  //   release   seconds after the spawn: the Upheaval channel ends (Monkey.cs RPC_upheaval0), the coroutine falls to standby
  //   unsummon  seconds after the spawn: unsummon() (:886-930): the particle emitter's emit off (:892-912), every renderer
  //             with a _Color gets alpha Lerp(0.86, 0, t - t0) (:861-867; here its opacity x that / 0.86), Translate(8
  //             forward dt) each FixedUpdate (:839), Destroy at t0 + 1 (:819-825)
  // Update (:23-140) once started: standby: forward = RotateTowards(forward, summoner + 4 up - position, dt, 1) (:48: 1 rad/s
  // at most), Translate(8 forward dt) along the old forward (:53), rotation = LookRotation(forward) (:58); every state: when
  // t > next (:64) next = t + 0.25, h shifted down, h[0] = position (:70-97); then segment j (0..5) position = Lerp(h[j],
  // h[j + 1], 4 (next - t)), rotation = LookRotation(Slerp(h[j] - h[j + 1], h[j + 1] - h[j + 2], 4 (next - t))) (:103-125).
  // The summoner is the hero's feet, (0, 0, 0) here; the cue's kill ends it otherwise.
  // The segments are the root's children: each frame their world pose is written as root^-1 x world (they keep their
  // children: the models' rotationControl spins, fxparts/rotationcontrol.js). Looked up on the first update (the Bat's
  // gotcha: they are not parented yet when the root's part is built).
  // APPROXIMATED: Time.time is the part's own clock (the sin / cos phases of the circle start at 0); the upheaval's
  // position Slerp is a lerp (Unity slerps the two positions as vectors from the map's origin, far off on any map, where
  // it is all but a lerp; from the hero's feet it would swing round her); the unsummon's rgb (0.86) left as the material's
  // (0.777: Lavu.mat); the summoner never moves (the hero is in place).
  const SEG = ["body1", "body2", "body3", "body4", "body5", "tail"];
  api.part("Monkey_lavu", (fx, root) => {
    const at = fx.at || {}, upheaval = at.lavu === "upheaval";
    const release = num(at.release, null), unsummonAt = num(at.unsummon, null);
    const SUMMONER = V(0, 0, 0), HEAD = V(0, 4, 0);    // the summoner's feet; + 4 up (standby)
    let t = 0, tf = 0, acc = 0, t0 = 0, next = 0, state = null, parts = null, h = null, fade = null, gone = false;
    const fwd = () => V(0, 0, 1).applyQuaternion(root.quaternion);
    const world = n => n.position.clone().multiply(root.scale).applyQuaternion(root.quaternion).add(root.position);
    const setWorld = (n, p, q) => {                    // a child of the root: local = root^-1 x world
      const qi = root.quaternion.clone().invert();
      n.position.copy(p).sub(root.position).applyQuaternion(qi).divide(root.scale);
      n.quaternion.copy(qi).multiply(q);
    };
    const start = () => {                              // summon()'s set-up (:333-430)
      parts = SEG.map(s => root.children.find(o => o.name === s) || null);   // transform.Find: direct children
      if (parts.some(o => !o)) warnOnce("lavu:nodes", "effect part Monkey_lavu: missing segment nodes in", fx.name);
      h = [root.position.clone(), ...parts.map(o => (o ? world(o) : root.position.clone())), null];
      h[7] = h[6].clone();
      next = t + 0.25; t0 = tf;
      state = upheaval ? "upheaval" : "summon";
    };
    const unsummon = () => {                           // unsummon()'s set-up (:886-919)
      state = "unsummon"; t0 = tf;
      const particle = root.children.find(o => o.name === "particle");
      for (const e of fx.emitters) if (particle && e.node === particle) e.stop?.();   // emit = false
      fade = [];
      root.traverse(o => {
        if (!o.isMesh || Array.isArray(o.material) || !o.material) return;
        const b = o.material.userData?.fxBlend;
        if (b !== "shader:FX/Lavu" && b !== "shader:FX/Phoenix") return;   // HasProperty("_Color"): the meshes, not Acid3's particles
        if (!o.userData.ownMaterial) {                 // Unity's renderer.material: its own copy (Fx.dispose frees it)
          const m0 = o.material, c = m0.clone();
          c.onBeforeCompile = m0.onBeforeCompile; c.customProgramCacheKey = m0.customProgramCacheKey;
          o.material = c; o.userData.ownMaterial = true;
        }
        fade.push([o.material, o.material.opacity]);
      });
    };
    const fixed = () => {                              // the coroutines' WaitForFixedUpdate steps
      tf += STEP;
      if (state === "summon") {
        if (tf >= t0 + 2) { state = "standby"; t0 = tf; }   // :436-443
        else root.position.addScaledVector(fwd(), 10 * STEP);   // :457
      } else if (state === "upheaval") {
        if (release != null && tf >= release) { state = "standby"; t0 = tf; return; }   // :672-675
        const a = (120 * (tf - t0)) % 360 * DEG, r = 6;  // rotateH(6 forward, a): x = -6 sin a, z = 6 cos a
        const target = V(-r * Math.sin(a), Math.sin(4 * tf), r * Math.cos(a)).add(SUMMONER);
        if (tf < t0 + 3) {
          root.position.lerp(target, clamp(0.33 * (tf - t0), 0, 1));
          const d = target.clone().sub(root.position);
          if (d.lengthSq() > 1e-12) lookRot(d, root.quaternion);
        } else {
          root.position.copy(target);
          root.quaternion.setFromEuler(new THREE.Euler(-30 * Math.cos(4 * tf) * DEG, -((90 + 120 * (tf - t0)) % 360) * DEG, 0, "YXZ"));
        }
      } else if (state === "unsummon") {
        if (tf >= t0 + 1) return "destroy";            // :819-825
        root.position.addScaledVector(fwd(), 8 * STEP);   // :839
        const k = clamp(0.86 + (0 - 0.86) * (tf - t0), 0, 0.86) / 0.86;   // Mathf.Lerp(0.86, 0, t - t0) (:867)
        for (const [m, a0] of fade) m.opacity = a0 * k;
      }
    };
    return { node: root, update(dt) {
      if (gone) return "destroy";
      if (!state) start();
      t += dt;
      if (unsummonAt != null && state !== "unsummon" && t >= unsummonAt) unsummon();
      for (acc += dt; acc >= STEP; acc -= STEP) if (fixed() === "destroy") { gone = true; return "destroy"; }
      if (state === "standby") {                       // Update :42-58
        const f = rotateTowards(fwd(), HEAD.clone().sub(root.position), dt);
        root.position.addScaledVector(fwd(), 8 * dt);
        lookRot(f, root.quaternion);
      }
      if (t > next) {                                  // :64-97
        next = t + 0.25;
        for (let i = 7; i > 0; i--) h[i] = h[i - 1];
        h[0] = root.position.clone();
      }
      const u = 4 * (next - t), q = new THREE.Quaternion();
      for (let j = 0; j < 6; j++) {                    // :103-125
        if (!parts[j]) continue;
        const dir = slerpV(h[j].clone().sub(h[j + 1]), h[j + 1].clone().sub(h[j + 2]), u);
        if (dir.lengthSq() > 1e-12) lookRot(dir, q); else q.identity();   // LookRotation(zero) = identity
        setWorld(parts[j], h[j].clone().lerp(h[j + 1], clamp(u, 0, 1)), q);
      }
      root.updateMatrixWorld(true);                    // the particle emitter after this part sees the move
    } };
  });

  // ---------------------------------------------------------------- fx:mikeBlink (parts.md part 6, decisions 2-3)
  // Monkey.cs $RPC_mikeBlink1 (:35895-35943): mikeBlink at mPos + tDir, LookRotation(vFlat(tDir)) x Euler(270, 90, 0) (the
  // cue's d 10 rot [270, 90, 0]); mWep1.transform.parent = mikeBlink/mount_Summon, localPosition 0, localRotation identity
  // (:35920-35943); the prefab's Animation root (1.1 s, Once) flies that node; resetMikeBlink (:14015-14058) puts it back
  // on the hero and destroys the effect (the cue's kill). mWep1 = the page's slot R (placements.json weapons.monkey
  // fallback bone mount_Summon); nothing worn: the starter noviceMike (PROP_STARTER.monkey, Chameleon decision 50). The
  // hand's own piece is hidden by the cue's hideProp R. The copy hangs at local 0 / identity / its prefab root scale
  // (api.propModel's), freed with the effect: its geometry by Fx.dispose's sweep, its materials (fresh per call) here.
  // Asked for again each frame until it comes (null while the prop list loads). fx.at.slot is ignored (always R).
  api.part("fx:mikeBlink", fx => {
    if (fx.cls !== "monkey") return null;
    if (typeof api.propModel !== "function") { warnOnce("propModel", "effect part fx:mikeBlink: no api.propModel (index.html)"); return null; }
    let model = null, tries = 0;
    return { node: fx.root, update() {
      if (model || tries > 600) return;                // about 10 s of asking at most
      tries++;
      const mount = fx.nodes.find(o => o.name === "mount_Summon");
      if (!mount) { tries = Infinity; warnOnce("mb:mount", "effect part fx:mikeBlink: no mount_Summon in", fx.name); return; }
      try { model = api.propModel("R", true); } catch (e) { warnOnce("mb:pm", "effect part fx:mikeBlink: api.propModel", e); tries = Infinity; }
      if (model) mount.add(model);                     // propModel: position 0, identity, the prefab's root scale
    }, dispose() {
      model?.traverse(o => { for (const m of [].concat(o.material || [])) m.dispose?.(); });
    } };
  });
}
