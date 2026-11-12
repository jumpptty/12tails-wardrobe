// wardrobe/fxparts/cat.js: the Cat's own effect scripts and the hero's code acting on her effects (builder "cat",
// 2026-11-13; plans/fx_cat/parts.md parts 2, 3, 4 with its Verification (corrections 1, 2 win), the overnight decisions
// plans/fx_cat/decisions.md 6, 48, 49, 50, and the loader comment above FX_PART_FILES in index.html). BB's
// DecompiledSource is the authority for every line cited here (D:\12tails\DecompiledSource\<file>); the prefab facts are
// checks/fx_cat_research/parts/probe.txt, the flight checks/fx_cat_research/parts/calc.txt.
//   Cat_grandCasinoArcade     grandCasinoArcade (node 1): the machine's sign materials [1] / [2] blinking in counter-phase
//   fx:grandCasinoArcade      the hero's coroutine playing the machine's fire / destroy clips (the cue's `anims`), and its
//                             end (the standby) at age 15.5
//   Cat_supportFire           supportFire_fire: the cannonball's flight, its supportFire_hit on the floor
//   fx:supportFire_cannon     Support Fire's barrage (a random cannon every 0.24-0.35 s) and the cannons' fade at the cut
// Space: every root here hangs in the effect's mirror group (Unity's world, the hero's feet at the origin, +z her facing,
// y 0 the floor), so node.position is the game's transform.position and the numbers below are the game's own.
//
// Page hooks used: node.userData.fxAnim.play(name) and .rewind() (mesh.js's Animation; rewind = Animation.Rewind, and the
// cannon's Animation is built although its `play` is off: plans/fx_cat/parts.md Interfaces 1, decision 51); an AlphaTimer
// emitter's fadeOut(sec) (alphatimer.js, AlphaTimerFadeOut: Interfaces 2); api.spawn(name, at) (index.html fxSpawn; the
// Support Fire entry's "builds" puts supportFire_fire / _smoke / _hit in fx.json); api.FX.gen (counts the picks, fxClear),
// api.FX.t / fx.cutAt (the cue's cut, on the playing step's clock); an emitter's dispose() (index.html Fx.dispose).

// ---------------------------------------------------------------- Math.getTrajectoryVector (Math.cs:885-1000)
// The guards worked by hand (parts.md part 3, its Verification): the high-arc tangent used as the angle from vertical
// (the low arc), then the y < 0.1 correction. In the game's signs (gravity y negative, so num < 0):
//   flat = vFlat(target - pos), d = |flat|, y = (target - pos).y, g = Physics.gravity.y
//   d < |v^2 / g| - 1: num = atan((v^2 + sqrt(v^4 - g (g d^2 (+ 2 v^2 y when y > 0)))) / (g d)), else num = -1.15
//   y < 0.1: f = 2 atan(y / d); num += num - num cos f - 0.1 d / v
//   direction = sin(num) x vFlat(pos - target).normalized + cos(num) x up (not normalised: it is a unit vector)
// Support Fire (target at the muzzle's height, 24..47 m): elevation 2.99 (24 m) .. 6.41 deg (47 m), calc.txt.
// A pure function of plain [x, y, z] arrays (exported for the node probe, checks/fx_cat_build/cat/probe.mjs).
export const trajectoryVector = (pos, target, v, g = -9.8) => {
  const fx = target[0] - pos[0], fz = target[2] - pos[2], d = Math.hypot(fx, fz), y = target[1] - pos[1];
  let num;
  if (d < Math.abs(v * v / g) - 1) {
    const n3 = y > 0 ? v * v + Math.sqrt(v ** 4 - g * (g * d * d + 2 * v * v * y)) : v * v + Math.sqrt(v ** 4 - g * (g * d * d));
    num = Math.atan(n3 / (g * d));
  } else num = -1.15;
  if (y < 0.1) {
    const f = 2 * Math.atan(y / d);
    num += num - num * Math.cos(f) - 0.1 * d / v;
  }
  const s = Math.sin(num), back = d > 0 ? [-fx / d, -fz / d] : [0, 0];   // vFlat(pos - target).normalized
  return [s * back[0], Math.cos(num), s * back[1]];
};
// Unity Euler degrees [x, y, z] of LookRotation(dir) (a cue's rot: Quaternion.Euler turns z, x, y = three's "YXZ")
export const lookEuler = dir => {
  const h = Math.hypot(dir[0], dir[2]), deg = 180 / Math.PI;
  return [-Math.atan2(dir[1], h) * deg, Math.atan2(dir[0], dir[2]) * deg, 0];
};

export default function register(api) {
  const { THREE, V } = api;
  const STEP = 0.02;                                   // Unity's fixed timestep (FixedUpdate, 50 per second)
  const GRAVITY = -9.8;                                // Physics.gravity.y (the PhysicsManager in mainData, probe_ps.txt)
  const clamp01 = x => Math.min(1, Math.max(0, x));
  const warned = new Set();
  const warnOnce = (k, ...m) => { if (!warned.has(k)) { warned.add(k); console.warn(...m); } };
  // Quaternion.LookRotation(forward, Vector3.up) in Unity's numbers (bat.js's / penguin.js's)
  const lookRot = (f, q = new THREE.Quaternion()) => {
    const z = f.clone().normalize(), x = V().crossVectors(V(0, 1, 0), z);
    if (x.lengthSq() < 1e-12) x.set(1, 0, 0); x.normalize();
    return q.setFromRotationMatrix(new THREE.Matrix4().makeBasis(x, V().crossVectors(z, x), z));
  };
  // a cloned material keeping fxMaterial's onBeforeCompile (Material.copy leaves it out: the additive alpha lives there;
  // alphatimer.js own())
  const cloneMat = m => {
    const c = m.clone();
    c.onBeforeCompile = m.onBeforeCompile;
    c.customProgramCacheKey = m.customProgramCacheKey;
    return c;
  };

  // ---------------------------------------------------------------- Cat_grandCasinoArcade (grandCasinoArcade, node 1)
  // Field mRenderer (Cat_grandCasinoArcade.cs:144: the SkinnedMeshRenderer on the same node, probe.txt [0, 75936]).
  // Awake (:21-83; every opaque predicate worked by hand, parts.md Verification): mRenderer.materials (Unity: per-renderer
  // copies of every material) [1] -> sQp (:38), [2] -> NH5 (:50). Update (:87-123), every frame: num = 0.15 sin(4
  // Time.time) (:94); sQp._TintColor = (0.5, 0.5, 0.5, num) (:103); NH5._TintColor = (0.5, 0.5, 0.5, 0.15 - num) (:115):
  // GrandCasinoArcade2 pulses alpha -0.15 .. 0.15 and GrandCasinoArcade3 0 .. 0.3, in counter-phase, period 2 pi / 4 =
  // 1.571 s. Both are built-in 200 `add` (Particles/Additive: a negative alpha draws nothing), so fxMaterial's rule for a
  // tint: opacity = min(1, 2 x tint.a), colour = min(1, 2 x tint.rgb) = 1 (index.html fxMaterial). GrandCasinoArcade3's saved
  // tint alpha is 0: without this script it never shows.
  // Here: the mesh's material list (mesh.js withMaterials: one entry per pass, and the three materials here are one pass
  // each: Phoenix, add, add) gets its own clones of [1] and [2] (mesh.js shares one material per class and name across
  // spawns), written back in place and freed with the effect. T = the page's absolute clock (as uvscroll.js: Time.time
  // counts from the client's start, here from the page's; APPROXIMATED: the phase).
  api.part("Cat_grandCasinoArcade", (fx, node, c) => {
    if (c?.enabled === false) return null;
    let mesh, m1 = null, m2 = null, done = false;
    return { node, update() {
      if (done) return;
      if (mesh === undefined) {                        // the first update: every part of the node is built by now
        mesh = node.isMesh ? node : node.children.find(x => x.isMesh) || null;
        const list = mesh && Array.isArray(mesh.material) ? mesh.material : null;
        if (!list || list.length < 3 || !list[1] || !list[2]) {
          warnOnce("gca:" + fx.name, "effect part Cat_grandCasinoArcade: no materials [1] / [2] on", fx.name, "(fxparts/mesh.js)");
          done = true; return;
        }
        m1 = list[1] = cloneMat(list[1]);              // sQp (:38)
        m2 = list[2] = cloneMat(list[2]);              // NH5 (:50)
        m1.color.setRGB(1, 1, 1, THREE.SRGBColorSpace); m2.color.setRGB(1, 1, 1, THREE.SRGBColorSpace);   // rgb 0.5 x 2
      }
      const n = 0.15 * Math.sin(4 * (performance.now() / 1000));   // :94
      m1.opacity = clamp01(2 * n);                     // :103, alpha num
      m2.opacity = clamp01(2 * (0.15 - n));            // :115, alpha 0.15 - num
    }, dispose() {
      m1?.dispose(); m2?.dispose(); m1 = m2 = null; done = true;
    } };
  });

  // ---------------------------------------------------------------- fx:grandCasinoArcade (the hero's coroutine)
  // Cat.cs, coroutine $RPC_grandCasinoArcade$21905, max rank sLv 2 (Bible cat-skill-reference.md:23): the effect is made at
  // clip 0.4 (Yield 2 :28796, createEffect :27838); mGrandCasinoAnimation = effect.transform.Find("grandCasinoArcade")
  // (:27858) = node 1 (its Animation: create 1.467 s plays by itself, fire 2.5 s, destroy 1.0 s). Each of the five spins
  // (while i < 2 sLv + 1, :28507) Play("fire") (:28554); after the 5th Play("destroy") (:28513-28531); then standby
  // (:28454). In effect age: fire at 1.3 + 2.7 k (k = 0..4), destroy at 14.5, standby at 15.5 (clip 15.9).
  // The ages come from the cue's `anims` option ([[age, clip], ...], decision 50, skills_a.md's block), each played once
  // when the effect's age passes it. The cue has no `cut` (parts.md Verification 1: a cue's cut is read on the playing
  // step's clock), so the part ends the effect itself at age 15.5: fx.cutAt = -Infinity makes the page's followState end
  // run (index.html Fx.update: age = life 16, then the 1 s afterLife; the root has no Animation, so no second destroy, as
  // EffectControl.cs:252-291 plays "destroy" only on its own node's Animation). After an earlier end (fx.stopped: the
  // break out of attack, IL_20BD) nothing more plays. Played as Animation.Play: a clip not playing restarts (fire's
  // 2.5 s is over when the next spin comes 2.7 s later, mesh.js play()).
  const GCA_END = 15.5;
  api.part("fx:grandCasinoArcade", fx => {
    if (fx.cls !== "cat") return null;
    const anims = Array.isArray(fx.at?.anims) ? fx.at.anims.filter(a => Array.isArray(a) && a.length >= 2).slice().sort((a, b) => a[0] - b[0]) : [];
    if (!anims.length) warnOnce("gca-anims", "effect part fx:grandCasinoArcade: the cue has no anims option (fx_cues/cat.json): the machine plays only its create clip");
    const machine = fx.nodes.find((o, i) => i > 0 && o.name === "grandCasinoArcade") || fx.nodes[1];
    let t = 0, k = 0, ended = false;
    return { node: fx.root, update(dt) {
      if (ended) return;
      t += dt;
      if (fx.stopped) { ended = true; return; }
      while (k < anims.length && t >= anims[k][0]) {
        const [, clip] = anims[k++];
        const a = machine?.userData.fxAnim;
        if (!a?.play) warnOnce("gca-anim", "effect part fx:grandCasinoArcade: no Animation play() on node 1 (fxparts/mesh.js)");
        else if (!a.play(clip)) warnOnce("gca-clip:" + clip, "effect part fx:grandCasinoArcade: no clip", clip);
      }
      if (t >= GCA_END) { ended = true; fx.cutAt = -Infinity; }   // the standby: the followState end (next frame)
    } };
  });

  // ---------------------------------------------------------------- Cat_supportFire (supportFire_fire)
  // Cat_supportFire.cs: ctor mVelocity = (0, 0, 30) (:26; the prefab keeps it, field at :240); Init (:38-63, called in the
  // spawn frame, Cat.cs:10753): life 10 (:48), rigidbody.velocity = TransformDirection(mVelocity) (:54): 30 m/s along the
  // spawn rotation (LookRotation(fireDir), Cat.cs:10741: the cue's rot). FixedUpdate (:67-98): life -= dt (:74), Destroy at
  // 0 (:81), else transform.LookAt(position + velocity) (:90). Physics (probe.txt): Rigidbody mass 1, drag 0, gravity on
  // (-9.8, probe_ps.txt); BoxCollider trigger 0.25 x 0.25 x 0.5. OnTriggerEnter (:102-219) on the ground (layer 0):
  // cat.RPC_supportFire_hit (:179) -> Instantiate(supportFire_hit, hitPos, Quaternion.identity) (Cat.cs:10802), then
  // Destroy(gameObject) (:206): the ball and its Cloud1 trail go.
  // Here (decision 49): on the 0.02 s grid v.y -= 9.8 x 0.02, then pos += v x 0.02 (Unity's semi-implicit step, calc.py),
  // the root turned along v; the ground test as calc.py: the box's lowest corner, y - (0.125 cos p + 0.25 |sin p|) with p
  // the pitch, at or below the floor -> supportFire_hit at the point under the ball (y 0, identity: the cue's default
  // facing), "destroy". Drawn between steps along the velocity. From the 1 m muzzle it lands 18-26 m ahead after 0.6-0.9 s.
  api.part("Cat_supportFire", (fx, node, c) => {
    const mv = Array.isArray(c?.mVelocity) ? c.mVelocity : [0, 0, 30];
    const vel = V(mv[0], mv[1], mv[2]).applyQuaternion(fx.uQuat(node));   // TransformDirection at the spawn (:54)
    const p = node.position.clone(), q = new THREE.Quaternion();
    let acc = 0, k = 0;
    const LIFE_STEPS = Math.round(10 / STEP);          // life 10 (:48), -= 0.02 each FixedUpdate (:74)
    return { node, update(dt) {
      acc += dt;
      while (acc >= STEP) {
        acc -= STEP;
        if (++k >= LIFE_STEPS) return "destroy";       // life <= 0: Destroy (:81)
        vel.y += GRAVITY * STEP;
        p.addScaledVector(vel, STEP);
        const pitch = Math.atan2(-vel.y, Math.hypot(vel.x, vel.z));   // the downward pitch
        if (p.y - (0.125 * Math.cos(pitch) + 0.25 * Math.abs(Math.sin(pitch))) <= 0) {
          node.position.copy(p);
          if (api.spawn) { if (!api.spawn("supportFire_hit", { x: p.x, y: 0, d: p.z })) warnOnce("hit", "effect part Cat_supportFire: supportFire_hit not in fx.json (the entry's builds)"); }
          else warnOnce("spawn", "effect part Cat_supportFire: no api.spawn (index.html)");
          return "destroy";                            // Destroy(gameObject) (:206)
        }
      }
      node.position.copy(p).addScaledVector(vel, acc);
      node.quaternion.copy(lookRot(vel, q));           // LookAt(position + velocity) (:90)
      node.updateMatrixWorld(true);                    // the trail's emitter after this part sees the move
    } };
  });

  // ---------------------------------------------------------------- fx:supportFire_cannon (Support Fire's barrage)
  // Cat.cs, coroutine $RPC_supportFire$22224: at clip 0 six cannons createEffect'd at (3i - 10.5, 0, -2), the hero's
  // rotation (:41060, :41084; the six cues). Case 2 at 1.0: mUpdateTime = now + 0.25 (:40842), then every FixedUpdate
  // (Yield 3, :41334) the loop IL_729 (:41110-): when mUpdateTime <= now, mUpdateTime = now + 0.01 x Random.Range(24, 36)
  // (:41174: 0.24-0.35 s), a random cannon (:41185), muzzle = cannon + its TransformDirection(0, 1, 3) (:41207), fireDir =
  // getTrajectoryVector(muzzle, muzzle + (24 + Random.Range(0, 24)) x the Cat's forward, 30) (:41212), RPC_supportFire_fire
  // (:41217): the cannon's animation.Rewind(); Play("fire") (:10672-10677), supportFire_smoke and supportFire_fire at the
  // muzzle, LookRotation(fireDir) (:10711, :10741). The end, RPC_supportFire0 (:10547-10630): standby (:10566), every
  // cannon BroadcastMessage("AlphaTimerFadeOut", 0.5) (:10603: Max -> Min over 0.5 s, AlphaTimer.cs:328-357); the
  // cannons' EffectControl (life 99, afterLife 0.5, followState) removes them 0.5 s later; shells in flight fly on.
  // Here (decision 48): every cannon of one play registers in a module map keyed by api.FX.gen (the six cues are built in
  // the same frame, before any of them updates; a looping tile's next round keeps the gen, so a group closes at its
  // first update and the next round's cannons make a new group). The first living member drives the group's clock (from
  // its first update = the spawn, so age = clip time): from 1.25, on the 0.02 s grid, until the cut. The cut = the cue's
  // cut on the playing step's clock (api.FX.t >= fx.cutAt: supportFire2's, decision 6: 2.95) or the effect's own end
  // (fx.stopped): every cannon's emitters fadeOut?.(0.5), and no more shots. No SP model (parts.md Q3). The Cat's forward
  // is the effect's +z (the cannons stand at the hero's rotation; the aim follows the Cat, not the cannon, :41212).
  // The SP drain (:41255) and the move-key end (:41140, :41148) are the hero's, not drawn.
  const FIRST = 1.25;                                  // case 2 at 1.0 + 0.25 (:40842)
  const groups = new Map();                            // api.FX.gen -> { members: [Fx], open, k, next, cut }
  const shoot = (g, T) => {
    const live = g.members.filter(m => m.alive);
    if (!live.length) return;
    const cn = live[Math.floor(Math.random() * live.length)];   // Random.Range(0, cannons.length) (:41185)
    const a = cn.root.userData.fxAnim;
    if (!a?.play) warnOnce("cannon-anim", "effect part fx:supportFire_cannon: no Animation on the cannon (fxparts/mesh.js: play off)");
    else {
      if (a.rewind) a.rewind(); else warnOnce("cannon-rewind", "effect part fx:supportFire_cannon: no Animation rewind() (fxparts/mesh.js)");
      a.play("fire");                                  // Rewind(); Play("fire") (:10672-10677)
    }
    const mz = cn.root.position.clone().add(V(0, 1, 3).applyQuaternion(cn.uQuat(cn.root)));   // :41207
    const dist = 24 + Math.floor(Math.random() * 24);  // 24 + Random.Range(0, 24) (:41212)
    const m = [mz.x, mz.y, mz.z], dir = trajectoryVector(m, [m[0], m[1], m[2] + dist], 30);   // the Cat's forward = +z
    const at = { x: mz.x, y: mz.y, d: mz.z, rot: lookEuler(dir) };   // LookRotation(fireDir) (:10711, :10741)
    if (!api.spawn) return warnOnce("spawn", "effect part fx:supportFire_cannon: no api.spawn (index.html)");
    if (!api.spawn("supportFire_smoke", { ...at })) warnOnce("smoke", "effect part fx:supportFire_cannon: supportFire_smoke not in fx.json (the entry's builds)");
    if (!api.spawn("supportFire_fire", { ...at })) warnOnce("fire", "effect part fx:supportFire_cannon: supportFire_fire not in fx.json (the entry's builds)");
    g.next = T + 0.01 * (24 + Math.floor(Math.random() * 12));   // now + 0.01 x Random.Range(24, 36) (:41174)
  };
  const cut = g => {
    g.cut = true;                                      // BroadcastMessage("AlphaTimerFadeOut", 0.5) to every cannon (:10603)
    let faded = false;
    for (const m of g.members) if (m.alive) for (const e of m.emitters) if (e.fadeOut) { e.fadeOut(0.5); faded = true; }
    if (!faded) warnOnce("fadeOut", "effect part fx:supportFire_cannon: no AlphaTimer fadeOut() (fxparts/alphatimer.js)");
  };
  api.part("fx:supportFire_cannon", fx => {
    if (fx.cls !== "cat") return null;
    for (const [key, g] of groups) if (!g.members.some(m => m.alive)) groups.delete(key);   // played-out groups
    const gen = api.FX.gen;
    let g = groups.get(gen);
    if (!g || !g.open) { g = { members: [], open: true, k: 0, acc: 0, next: FIRST, cut: false }; groups.set(gen, g); }
    g.members.push(fx);
    const em = { node: fx.root, update(dt) {
      g.open = false;                                  // the play's cannons are all built by now
      if (!g.cut && (fx.stopped || (fx.cutAt != null && api.FX.t >= fx.cutAt))) cut(g);
      if (g.members.find(m => m.alive) !== fx) return;   // the first living cannon drives the clock
      g.acc += dt;
      while (g.acc >= STEP) {
        g.acc -= STEP;
        const T = ++g.k * STEP;
        if (!g.cut && T >= g.next - 1e-9) shoot(g, T); // mUpdateTime <= now, on a fixed step
      }
    }, dispose() {
      if (groups.get(gen) === g && !g.members.some(m => m.alive && m !== fx)) groups.delete(gen);
    } };
    return em;
  });
}
