// wardrobe/fxparts/tto_rabbit.js: what the Rabbit's TTO skills (Bounty Hunt, Coin Ricochet, Medic Turret: the released
// three) draw that no other part does (builder rabbit, 2026-11-13; plans/fx_rabbit/decisions.md 28-33, 51, parts.md "TTO"
// T1-T5 and Interfaces 3-4 with its Verification 2-3, tto.md section 6 P1-P5 with its Verification 2, which wins: the
// turret's part owns every beat, nothing of a beat is cued). TTO1102 = DecompiledSource_TTO_2026-11-02 (client/
// GameAssembly.dll): pseudo/Rabbit.c and pseudo_c6_extra/rabbit/RabbitMedicTurret.c ("RMT.c"), cited by line; the
// constants from dump.cs:120553-120562 (RabbitMedicTurret's statics: they are not serialized, so they are written here).
//
//   RabbitSpin             coinRicochet_coin/Coin (TypeDefIndex 3913, dump.cs:120616; Update@0x1E6EE30):
//                          transform.Rotate(axis, degreesPerSecond x dt, Space.Self); its fields from the data (the
//                          prefab's (0, 1, 0), 900)
//   PowerUpRotation        bountyHunt_claim's dollar (dump.cs:416004, Update@0x33AD20): Rotate(0, 0, rotationSpeed x dt),
//                          Self (`reverse` never read); the claim is built, not cued (decision 45), the part built anyway
//                          (decision 51: every missing part is built). Not class-guarded: a generic store script, drawn
//                          the same wherever it sits
//   Rabbit.PosterFly       bountyHunt_poster (<PosterFly>d__353@0x1E28850, Rabbit.c:556-786; CODE_MOVERS): s = 4 age,
//                          position = Lerp(from, to, clamp01(s)) + up x 0.8 s (1 - s) (:628-715), Rotate(forward, 900 dt,
//                          Self); Destroyed at 0.25 (the cue's kill 0.25 too). The end is the chest + 0.6 up (:650-654,
//                          the cue's `to` [0, 1.2, 10], decision 28); the pin it spawns at the chest (:747-764) is a cue
//                          (parts Verification 2): it spawns nothing here
//   Rabbit.CoinRise        coinRicochet_coin (<CoinRise>d__346@0x1E27890, Rabbit.c:440-539): u = clamp01((age - delay) /
//                          0.35), e = 1 - (1 - u)^2, position = Lerp(from, to, e) + up x 0.08 sin(40 delay + 6 now)
//                          (:469-519); now = Time.time from the cast = the cue's clip time fx.at.at + age (decision 29), so
//                          the cued tracers meet the coin; it hangs until the cue's kill (the shot)
//   Rabbit.TurretCapsule   medicTurret_capsule (<TurretCapsule>d__338@0x1E7AA60, Rabbit.c:24911-25140): position =
//                          Lerp(from, to, clamp01(4 age)) (:24985-25026), Rotate(right, 1080 dt, Self) (:25049); at 0.25
//                          Destroyed (:25067), medicTurret_hit at `to`, identity (:25097), and by kind lifeShot / boostShot
//                          / heatShot at `ally` (the feet), identity, Destroy(2) (:25119-25130)
//   RabbitMedicTurret      tto/medicTurret's root (RMT.c; decisions 31-33). Init (:142-161): Model localScale 0.01, the
//                          first beat at +0.75. Update (:177-421): Model localScale = max(0.01, k (1 + 0.18 sin(1.5 pi k)
//                          (1 - k))), k = clamp01(age / 0.45) (:225-252); the Head turned toward vFlat(mAimDir) at 540 deg/s
//                          (Slerp by 540 dt / angle, :314-351; mAimDir = its forward from Awake until the first beat, so
//                          it first turns at that beat's snap); a beat each 1.5 s from 0.75, at most 10 (:397-404), only
//                          while age < `end`. Fire (<Fire>d__29, :1181-1392): medicTurret_beat at the turret, identity
//                          (BeatFx :1251 -> Rabbit.c:40376); mAimDir = ally - turret, the Head snapped to LookRotation(
//                          vFlat(it)) (:1321-1327); the muzzle = the Muzzle node after the snap (:1351; get_Muzzle's
//                          fallback 0.85 up, :629-686); MedicTurretShotFx (Rabbit.c:40218-40344): medicTurret_shot there,
//                          identity, its RabbitTracer to the ally's chest, and the capsule (kind Random.Range(1, 4), RMT.c:471:
//                          a third each). Die -> <RPC_dead>d__31 (:1393-1537): medicTurret_break at the turret (Rabbit.c:
//                          40593), the Model shrunk linearly to 0.01 over 0.4 s (:1501-1526), Destroy (:1507). The older
//                          turret's Destroy at a recast (Rabbit.c:39906-39916) is the cue's `replace` (index.html, decision
//                          33), not this part's
//
// Cue / spawn options read (fx.at; [x, y, d] = metres right / up / ahead of the hero, the effect's Unity world):
//   to      the movers' end point (PosterFly, CoinRise, TurretCapsule)
//   delay   CoinRise's start and bob phase (default 0)
//   ally    the turret's ally chest (default [0, 0.7, 0]: the Rabbit herself, her collider centre, decision 32);
//           TurretCapsule's drop point, the ally's feet (default [to x, 0, to d])
//   kind    TurretCapsule's drop ("lifeShot" | "boostShot" | "heatShot"; spawn-only, decision 56)
//   end     the turret's Die, seconds after the spawn (default its Life 15; the cue's 10, kill 10.4)
// The turret spawns (api.spawn, at its own Unity-world spots: equal to the hero-relative cue frame while she stands still,
// as fxparts/robots.js): "tto/medicTurret_beat", "tto/medicTurret_shot" {to: ally}, "tto/medicTurret_capsule" {to: ally,
// ally: [ally x, 0, ally d], kind}, "tto/medicTurret_break"; the capsule "tto/medicTurret_hit" and its kind with kill 2
// (the entry's "builds": ["lifeShot", "boostShot", "heatShot"]).
// Space: everything in the effect's Unity world (the mirror group: the hero's feet at the origin, facing +z); Unity's
// local numbers apply inside the mirror as they are. A node of the effect is looked up when due (the first update), not at
// the build (the Bat's gotcha: the root's scripts are built before its children are placed).
export default function register(api) {
  const { THREE, V } = api;
  const DEG = Math.PI / 180;
  const clamp01 = x => (x < 0 ? 0 : x > 1 ? 1 : x);
  const num = (x, d = 0) => (x !== null && x !== "" && x !== undefined && Number.isFinite(+x) ? +x : d);
  const vec = a => (Array.isArray(a) && a.length >= 3 ? V(num(a[0]), num(a[1]), num(a[2])) : null);
  const v3 = (o, d) => (Array.isArray(o) ? V(num(o[0]), num(o[1]), num(o[2])) : o && typeof o === "object" ? V(num(o.x), num(o.y), num(o.z)) : d);
  const UP = V(0, 1, 0), RIGHT = V(1, 0, 0), FWD = V(0, 0, 1);
  const warned = new Set();
  const warnOnce = (k, ...m) => { if (!warned.has(k)) { warned.add(k); console.warn(...m); } };
  const spawn = (name, at) => {
    const f = api.spawn?.(name, at);
    if (!f) warnOnce("miss:" + name, `effect part (tto_rabbit.js): ${name} not spawned (not in fx.json: SKILL_FX / the entry's "builds")`);
    return f;
  };
  const at = (p, more) => ({ x: p.x, y: p.y, d: p.z, ...more });   // a spawn at a Unity-world point, identity
  // a node's Unity-world rotation / position (the mirror group's space), and Transform.set_rotation (as tto_chameleon.js)
  const uQuat = (fx, o) => { const q = new THREE.Quaternion(); for (; o && o !== fx.mirror; o = o.parent) q.premultiply(o.quaternion); return q; };
  const worldPos = (fx, o) => { o.updateWorldMatrix(true, false); return V().setFromMatrixPosition(fx.mirror.matrixWorld.clone().invert().multiply(o.matrixWorld)); };
  const setWorldRot = (fx, o, q) => o.quaternion.copy(uQuat(fx, o.parent).invert().multiply(q));
  const lookRot = (f, q = new THREE.Quaternion()) => {             // Quaternion.LookRotation(f, up) in Unity's numbers
    const z = f.clone().normalize(), x = V().crossVectors(UP, z);
    if (x.lengthSq() < 1e-12) x.set(1, 0, 0); x.normalize();
    return q.setFromRotationMatrix(new THREE.Matrix4().makeBasis(x, V().crossVectors(z, x), z));
  };
  // transform.Rotate(axis, deg, Space.Self): rotation = rotation x AngleAxis(deg, axis)
  const rotSelf = (node, axis, deg, q = new THREE.Quaternion()) => node.quaternion.multiply(q.setFromAxisAngle(axis, deg * DEG));

  // ---------------------------------------------------------------- RabbitSpin (P1, T5)
  api.part("RabbitSpin", (fx, node, c) => {
    if (fx.cls !== "rabbit") return null;
    const axis = v3(c.axis, V(0, 1, 0)), speed = num(c.degreesPerSecond, 900), q = new THREE.Quaternion();
    if (axis.lengthSq() < 1e-12) return null;
    axis.normalize();                                               // Quaternion.AngleAxis normalizes
    return { node, update(dt) { rotSelf(node, axis, speed * dt, q); } };
  });

  // ---------------------------------------------------------------- PowerUpRotation (decision 51)
  api.part("PowerUpRotation", (fx, node, c) => {
    const speed = num(c.rotationSpeed, 0), q = new THREE.Quaternion();
    return { node, update(dt) { rotSelf(node, FWD, speed * dt, q); } };   // Euler(0, 0, a) = AngleAxis(a, forward)
  });

  // ---------------------------------------------------------------- Rabbit.PosterFly (P3, T3)
  api.part("Rabbit.PosterFly", (fx, root) => {
    if (fx.cls !== "rabbit") return null;
    const from = root.position.clone(), to = vec(fx.at?.to), q = new THREE.Quaternion();
    if (!to) warnOnce("to:" + fx.name, "Rabbit.PosterFly: no cue `to` (the chest + 0.6 up): the poster stays where it was spawned", fx.name);
    return { node: root, update(dt) {
      const s = clamp01(4 * fx.age);
      if (to) { root.position.lerpVectors(from, to, s); root.position.y += 0.8 * s * (1 - s); }
      rotSelf(root, FWD, 900 * dt, q);
      if (fx.age >= 0.25) return "destroy";                          // Destroy(poster): nothing spawned (the pin is a cue)
    } };
  });

  // ---------------------------------------------------------------- Rabbit.CoinRise (P2, T4)
  api.part("Rabbit.CoinRise", (fx, root) => {
    if (fx.cls !== "rabbit") return null;
    const from = root.position.clone(), to = vec(fx.at?.to) || from.clone();
    const delay = num(fx.at?.delay), t0 = num(fx.at?.at);
    return { node: root, update() {
      const u = clamp01((fx.age - delay) / 0.35), e = 1 - (1 - u) * (1 - u);
      root.position.lerpVectors(from, to, e);
      root.position.y += 0.08 * Math.sin(40 * delay + 6 * (t0 + fx.age));
    } };
  });

  // ---------------------------------------------------------------- Rabbit.TurretCapsule (P4, T2)
  api.part("Rabbit.TurretCapsule", (fx, root) => {
    if (fx.cls !== "rabbit") return null;
    const from = root.position.clone(), to = vec(fx.at?.to), q = new THREE.Quaternion();
    if (!to) warnOnce("to:" + fx.name, "Rabbit.TurretCapsule: no `to` (the ally's chest): the capsule stays at the muzzle", fx.name);
    return { node: root, update(dt) {
      if (to) root.position.lerpVectors(from, to, clamp01(4 * fx.age));
      rotSelf(root, RIGHT, 1080 * dt, q);
      if (fx.age < 0.25) return;
      const end = to || root.position, feet = vec(fx.at?.ally) || V(end.x, 0, end.z), kind = fx.at?.kind;
      spawn("tto/medicTurret_hit", at(end));
      if (kind && kind !== "fx") spawn(kind, at(feet, { kill: 2 }));
      return "destroy";
    } };
  });

  // ---------------------------------------------------------------- RabbitMedicTurret (P5, T1)
  const BEATS = 10, GAP = 1.5, FIRST = 0.75, DEPLOY = 0.45, LIFE = 15, TURN = 540, SHRINK = 0.4;
  const KINDS = ["lifeShot", "boostShot", "heatShot"];              // kind 1 / 2 / 3
  api.part("RabbitMedicTurret", (fx, root) => {
    if (fx.cls !== "rabbit") return null;
    const ally = vec(fx.at?.ally) || V(0, 0.7, 0), end = num(fx.at?.end, LIFE);
    const node = name => fx.nodes.find(o => o.name === name) || null;
    let model, head, muzzle, found = false, beats = 0, next = FIRST, aim = null, dead = -1, s0 = 1;
    const fire = () => {
      const here = root.position;
      spawn("tto/medicTurret_beat", at(here));
      const d = V(ally.x - here.x, 0, ally.z - here.z);
      if (d.lengthSq() > 1e-10) { aim = lookRot(d); if (head) setWorldRot(fx, head, aim); }
      const m = muzzle ? worldPos(fx, muzzle) : here.clone().addScaledVector(UP, 0.85);
      const to = [ally.x, ally.y, ally.z], kind = KINDS[Math.floor(Math.random() * 3)];
      spawn("tto/medicTurret_shot", at(m, { to }));
      const cap = spawn("tto/medicTurret_capsule", at(m, { to, ally: [ally.x, 0, ally.z], kind }));
      // ponytail: api.spawn writes kind "fx" over the option (index.html fxSpawn); put back here, read only at arrival
      if (cap) cap.at.kind = kind;
    };
    return { node: root, update(dt) {
      if (!found) { found = true; model = node("Model"); head = node("Head"); muzzle = node("Muzzle"); }
      const age = fx.age;
      if (dead < 0 && age >= end) {                                  // Die -> RPC_dead
        dead = age; s0 = model ? model.scale.x : 1;
        spawn("tto/medicTurret_break", at(root.position));
      }
      if (dead >= 0) {
        const u = clamp01((age - dead) / SHRINK);
        model?.scale.setScalar(s0 + (0.01 - s0) * u);
        return u >= 1 ? "destroy" : undefined;
      }
      const k = clamp01(age / DEPLOY);
      model?.scale.setScalar(Math.max(0.01, k * (1 + 0.18 * Math.sin(1.5 * Math.PI * k) * (1 - k))));
      if (head && aim) {                                             // toward the aim at 540 deg/s
        const cur = uQuat(fx, head), a = cur.angleTo(aim);
        if (a > 1e-6) setWorldRot(fx, head, cur.slerp(aim, Math.min(1, TURN * DEG * dt / a)));
      }
      while (beats < BEATS && age >= next && age < end) { beats++; next += GAP; fire(); }
    } };
  });
}
