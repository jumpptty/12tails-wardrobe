// wardrobe/fxparts/penguin.js: the Penguin's own effect scripts (agent penguin, 2026-11-10; plans/fx_penguin/parts.md
// "Each part" 1-8 and "Interfaces", the user's decisions plans/fx_penguin/decisions.md, the loader comment above
// FX_PART_FILES in index.html). BB's DecompiledSource is the authority for every line cited here; Penguin.cs lines are
// D:\12tails\DecompiledSource\Penguin.cs, the prefab facts plans/fx_penguin/probes/research/parts/probe*.txt.
//   Penguin_tornado        tornado1-3: the glide, the create / root / destroy clips, the cyclone loop's volume
//   Penguin_typhoon        typhoon1-3: the homing on the target, the same clips and loop, its 6 s
//   Penguin_arcticEmperor  arcticEmperor: the statue's two fades (AdditiveSaturate's tint alpha and emission alpha)
//   Penguin_cosmicFriday   cosmicFriday: the create / root / destroy clips and its end at the cut
//   Penguin_iceBlock       iceBlock: its 12 s
//   Penguin_nAttack        nAttack_fire, spreadShot_fire: the 14 m/s ball, its end on the ground, the Staff of Time mine
//   Penguin_manaMissile    manaMissile_fire: the 12 m/s homing missile
//   Penguin_snowMan        snowMan: hides the hero while the snowman stands (decision 17)
// Space: every root here hangs in the effect's mirror group (Unity's world, the hero's feet at the origin, +z her
// facing), so node.position is the game's transform.position and the numbers below are the game's own.
//
// Page hooks used (plans/fx_penguin/parts.md "Interfaces"): node.userData.fxAnim.play(name, fade, wrap) (mesh.js, the
// third argument = Unity's animation.wrapMode set right after Play: 1 Once, 2 Loop); the looping AudioSource's handle
// h.setVolume(v) (index.html Sound.play), found as fx.loops.find(l => l.node === node).h once the node's later comps are
// built (the AudioSource comes after the script in comps); fx.cutAt (the cue's cut, clip time) against api.FX.t, as
// EffectControl's followState (index.html Fx.update); an emitter's dispose() (index.html Fx.dispose -> e.dispose?.()).

export default function register(api) {
  const { THREE, V } = api;
  const STEP = 0.02;                                   // Unity's fixed timestep (FixedUpdate, 50 per second)
  const ONCE = 1, LOOP = 2;                            // UnityEngine.WrapMode
  const warned = new Set();
  const warnOnce = (k, ...m) => { if (!warned.has(k)) { warned.add(k); console.warn(...m); } };
  const cut = fx => fx.cutAt != null && api.FX.t >= fx.cutAt;
  const target = (fx, dflt) => (Array.isArray(fx.at?.to) ? V(fx.at.to[0], fx.at.to[1], fx.at.to[2]) : dflt.clone());
  // Animation.Play / CrossFade with the wrap mode the script sets right after it (mesh.js play(name, fade, wrap))
  const play = (fx, node, name, fade, wrap) => {
    const a = node.userData.fxAnim;
    if (!a?.play) return warnOnce("anim:" + fx.name, "effect part (penguin.js): no Animation play() on", fx.name, "(fxparts/mesh.js)");
    if (!a.play(name, fade, wrap)) warnOnce("clip:" + fx.name + name, "effect part (penguin.js): no clip", name, "on", fx.name);
  };
  // the node's looping AudioSource handle and its volume (audio.volume written in FixedUpdate)
  const loopOf = (fx, node) => fx.loops.find(l => l.node === node)?.h || null;
  const setVol = (fx, h, v) => {
    if (!h || h.off) return;                           // no loop, or stopped (SFX off)
    if (h.setVolume) h.setVolume(v);
    else warnOnce("vol", "effect part (penguin.js): Sound.play's handle has no setVolume(v) (index.html): the", fx.name, "loop stays at its prefab volume");
  };
  // Quaternion.LookRotation(forward, Vector3.up) in Unity's numbers (fxparts/tto_sheep.js's; Cross is the same formula
  // in either hand)
  const lookRot = (f, q = new THREE.Quaternion()) => {
    const z = f.clone().normalize(), x = V().crossVectors(V(0, 1, 0), z);
    if (x.lengthSq() < 1e-12) x.set(1, 0, 0); x.normalize();
    return q.setFromRotationMatrix(new THREE.Matrix4().makeBasis(x, V().crossVectors(z, x), z));
  };
  // Vector3.RotateTowards's direction: from a toward b by at most maxRad (the magnitude is dropped: LookRotation and
  // TransformDirection(0, 0, 12) use only the direction, Penguin_manaMissile.cs:128-134)
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
  // A rigidbody stepped at Unity's 50 Hz: step(k) runs FixedUpdate k (k = 1, 2, ...) and returns the velocity the physics
  // integrates that step (p += v x STEP) or "destroy". The draw between steps follows the segment the next step will
  // take (p + vNext x the time into the step), so the drawn path is the stepped one exactly, with no lag; a step's
  // velocity depends only on the position before it (the FixedUpdate before the physics), so vNext is known in advance.
  const stepper = (node, step, after) => {
    let acc = 0, k = 0, vNext = step(++k);
    const p = node.position.clone();
    return dt => {
      if (vNext === "destroy") return "destroy";
      acc += dt;
      while (acc >= STEP) {
        acc -= STEP;
        p.addScaledVector(vNext, STEP);
        node.position.copy(p);                         // the position the next FixedUpdate and the trigger tests read
        if (after?.(p) === "destroy") return "destroy";
        vNext = step(++k);
        if (vNext === "destroy") return "destroy";
      }
      node.position.copy(p).addScaledVector(vNext, acc);
      node.updateMatrixWorld(true);                    // the parts after this one this frame (trails, emitters) see the move
    };
  };

  // ---------------------------------------------------------------- Penguin_tornado / Penguin_typhoon
  // The two scripts share their clips and loop (the same funnel, prefab nodes Penguin_tornado_tri / tornado1-3, and the
  // AudioSource sounds/cyclone at m_Volume 0, loop on: probe2.txt) and differ in how they move and end.
  // Both roots are instantiated with Quaternion.identity (Penguin.cs:10987 tornado3, :11260 typhoon3) and pushed along
  // owner.transform.forward (Penguin_tornado.cs:98, Penguin_typhoon.cs:848): the hero's +z here, whatever the cue's rot
  // (the funnel is round). Rigidbody (probe2.txt): mass 1, drag 2 from Init (Penguin_tornado.cs:103, Penguin_typhoon.cs:
  // 853), rotation frozen (m_Constraints 112), gravity on but the capsule's bottom is at the root, on the floor: no fall.
  // APPROXIMATED: PhysX 2's linear drag as v x (1 - drag x dt) per step (parts.md "Physics", medium: 1 / (1 + drag dt)
  // would end the tornado's glide 2.5 m out instead of 2.4 m).
  // A new cast destroys the old one at once (RPC_tornado_fire's Destroy(this.TARwEJavxD), Penguin.cs:10845;
  // RPC_typhoon_fire's Destroy(this.aGdw94Yq62), :11150): one live funnel of each kind
  const lastOf = {};
  const cyclone = (kind, fx, node, c) => {
    const me = { fx, gone: false };
    const prev = lastOf[kind];
    if (prev && prev.fx.alive) prev.gone = true;
    lastOf[kind] = me;
    const DRAG = 2, mLv = c.mLv ?? 3;
    // onCreate (Penguin_tornado.cs:744-778) / Init (Penguin_typhoon.cs:902-927), in the spawn frame: Play("create"),
    // wrapMode Once; Yield(2, 0.4); then Play("root"), wrapMode Loop unless it is already dying
    play(fx, node, "create", 0, ONCE);
    let t = 0, created = false, dyingAt = null, vol = 0, h, hLooked = false;
    const dying = () => dyingAt != null;
    // onDestroy (Penguin_tornado.cs:884-940, Penguin_typhoon.cs:1067-1126): Play("destroy"), wrapMode Once; Yield(2, 0.4);
    // Destroy(gameObject) (Penguin_tornado.cs:898, Penguin_typhoon.cs:1081), the loop with it
    const die = () => { if (!dying()) { dyingAt = t; play(fx, node, "destroy", 0, ONCE); } };
    let v, step;
    if (kind === "tornado") {
      // Init: velocity = 5 x owner forward (Penguin_tornado.cs:98). FixedUpdate (:409-560): the owner's movement keys add
      // (11 - mLv) x input (:460-472): the page has no keys, so no force, and it glides 2.4 m and stops (parts.md calc);
      // the 30 / 40 m/s caps (:478-515) and the 30 m pull-back (:522-531) never act at this speed. Volume (:416-442):
      // + dt per step clamped 0..1 while active (Init sets it, :179) and alive, - dt while dying
      v = V(0, 0, 5);
      step = () => {
        vol = Math.min(1, Math.max(0, vol + (dying() ? -STEP : STEP)));
        v.multiplyScalar(1 - DRAG * STEP);
        return v;
      };
    } else {
      // Init (Penguin_typhoon.cs:712-927): velocity = Math.rotateH(5 x owner forward, (tID - 1) x 120) (:848), tID the
      // target's Photon actor number (:830-837). rotateH (Math.cs:838-843) gives (-5 sin a, 0, 5 cos a) for forward (0, 0, 5).
      // Decision 12: a = 0, 120 or 240 degrees at random on each play (the page has no actor numbers)
      const a = [0, 120, 240][Math.floor(Math.random() * 3)] * Math.PI / 180;
      v = V(-5 * Math.sin(a), 0, 5 * Math.cos(a));
      // FixedUpdate (:307-475), from the spawn on (the not-yet-active and the dying paths both reach the steering at
      // IL_432, :314-336, :465-475): AddForce((11 - mLv) x vFlat(target.position - position).normalized) (:356-372), 8 N on
      // 1 kg at mLv 3; caps 30 / 40 m/s (:379-416) and the 30 m pull-back (:423-436) never act (terminal 3.84 m/s).
      // The target is the cast's: the cue's `to` (its feet; vFlat drops the height), else the 10 m point.
      // Volume: + dt clamped 0..0.6 while active (from 0.4 s, :330), - dt while dying (:472)
      const to = target(fx, V(0, 0, 10)), F = 11 - mLv, d = V();
      step = () => {
        if (dying()) vol = Math.max(0, vol - STEP);
        else if (created) vol = Math.min(0.6, vol + STEP);
        d.set(to.x - node.position.x, 0, to.z - node.position.z);
        if (d.lengthSq() > 1e-10) v.addScaledVector(d.normalize(), F * STEP);   // Vector3.zero is skipped (:366)
        v.multiplyScalar(1 - DRAG * STEP);
        return v;
      };
    }
    const move = stepper(node, step);
    return { node, update(dt) {
      if (me.gone) return "destroy";                  // a newer cast's Destroy: no destroy clip
      t += dt;
      if (!hLooked) { hLooked = true; h = loopOf(fx, node); }
      if (!created && t >= 0.4) { created = true; if (!dying()) play(fx, node, "root", 0, LOOP); }
      if (!dying()) {
        // Penguin_tornado.Update (:199-397), from the spawn: once the owner's actionState != "attack" or myCommand !=
        // "tornado" (:225-231), onDestroy (:391): the cue's cut (the clip time the channel ends); none = never, as the
        // game with the key held. Penguin_typhoon.Update (:49-295), once active (0.4 s): its end time = Init's time +
        // chaAdjust(6) (:772; Penguin.cs:11305; 6 s at CHA 1 / LCK 1, CharacterControl.cs:20593), destroyed once
        // end < Time.time (:81), via RPC_typhoon_destroy -> onDestroy (:270-287, Penguin.cs:11360-11378); its other ends
        // (target gone :81, owner down :87, its hp < 0 :93: 306 hp less the damage it deals) need a fight the page has
        // not. Typhoon has no channel check: a cue's cut still ends it, if the lead gives one
        if (kind === "tornado" ? cut(fx) : created && (t > 6 || cut(fx))) die();
      }
      if (dying() && t >= dyingAt + 0.4) return "destroy";
      const r = move(dt);
      setVol(fx, h, vol);
      return r;
    } };
  };
  api.part("Penguin_tornado", (fx, node, c) => cyclone("tornado", fx, node, c));
  api.part("Penguin_typhoon", (fx, node, c) => cyclone("typhoon", fx, node, c));

  // ---------------------------------------------------------------- Penguin_arcticEmperor
  // The AlphaTimer pattern twice (Penguin_arcticEmperor.cs): Start (:41-62) the phase ends d = FadeDelay (:51), i = d +
  // FadeEaseIn (:54), m = i + FadeMiddle (:57), o = m + FadeEaseOut (:60); Update (:74-200) d > t Min; i > t lerp Min ->
  // Max; m > t Max; o > t lerp Max -> Min; t > o Min (strict tests, no repeat, no destroy), for alpha (MinAlpha / MaxAlpha)
  // and emission (MinEmission / MaxEmission) alike; then renderer.material's _TintColor.a = alpha (:175-181) and
  // _Emission.a = emission (:184-190). Values (probe.txt): alpha 0 -> 0.25, emission 0 -> 0.035, phases 0 / 0.3 / 8 / 9 s.
  // The material is Transparent/AdditiveSaturate, two passes (mesh.js material(): pass 1 alpha blend from _TintColor,
  // pass 2 additive from _Emission): pass 1 opacity = min(1, 2 alpha), pass 2 opacity = min(1, 2 emission) (the page's
  // "double" convention for the particle shaders, fxMaterial's 2 x tint; APPROXIMATED as parts.md says: whether the
  // shader's "double" doubles alpha too). Unity's renderer.material is the renderer's one copy driving both passes: both
  // pass materials are cloned per spawn (mesh.js shares them per class and name). The pass is the material's
  // userData.fxPass (0 / 1, mesh.js saturate()), else its order in the mesh's list (pass 1 first, parts.md Interfaces 5).
  // The statue's ShatterMesh (8 s, probe.txt) keeps the mesh's material list, these clones included.
  let ownedMats = [];                                  // [fx, material]: freed once their effect is gone
  const freeMats = () => { ownedMats = ownedMats.filter(([f, m]) => f.alive || (m.dispose(), false)); };
  const SAT = "shader:Transparent/AdditiveSaturate";
  api.part("Penguin_arcticEmperor", (fx, node, c) => {
    freeMats();
    const d = c.FadeDelay, i = d + c.FadeEaseIn, m = i + c.FadeMiddle, o = m + c.FadeEaseOut;
    const lerp = (x, y, u) => x + (y - x) * Math.min(1, Math.max(0, u));   // Mathf.Lerp clamps u
    const fade = (t, lo, hi) => (d > t ? lo : i > t ? lerp(lo, hi, (t - d) / (i - d)) : m > t ? hi
      : o > t ? lerp(hi, lo, (t - m) / (o - m)) : lo);
    let t = 0, passes;                                 // passes: undefined until the first update, then [pass 1, pass 2] or null
    const mine = [];
    return { node, dispose() { for (const x of mine) x.dispose(); mine.length = 0; },
      update(dt) {
        if (passes === undefined) {                    // the first update: every part of the node is built by now
          passes = null;
          const mesh = node.userData.fxStatic || node.children.find(x => x.isMesh);
          const list = mesh && (Array.isArray(mesh.material) ? mesh.material : [mesh.material]);
          const sat = (list || []).map((x, k) => [x, k]).filter(([x]) => x?.userData?.fxBlend === SAT);
          if (sat.length < 2) warnOnce("sat", "effect part Penguin_arcticEmperor: the statue has", sat.length,
            "AdditiveSaturate pass materials, not 2 (fxparts/mesh.js material())", fx.name);
          if (sat.length) {
            const cl = new Map(sat.map(([x, k]) => {
              const y = x.clone(); y.onBeforeCompile = x.onBeforeCompile;   // Material.copy leaves it out
              ownedMats.push([fx, y]); mine.push(y);
              return [k, y];
            }));
            const arr = list.map((x, k) => cl.get(k) || x);
            mesh.material = Array.isArray(mesh.material) ? arr : arr[0];
            const ms = [...cl.values()];
            const byTag = n => ms.find(y => y.userData.fxPass === n);
            passes = [byTag(0) || ms[0], byTag(1) || ms[1] || null];
          }
        }
        if (!passes) return;
        t += dt;
        passes[0].opacity = Math.min(1, 2 * fade(t, c.MinAlpha, c.MaxAlpha));
        if (passes[1]) passes[1].opacity = Math.min(1, 2 * fade(t, c.MinEmission, c.MaxEmission));
      } };
  });

  // ---------------------------------------------------------------- Penguin_cosmicFriday
  // InitCosmicFriday (by SendMessage in the spawn frame, Penguin.cs:39279; Penguin_cosmicFriday.cs): Play("create"),
  // wrapMode Once (:391-394), Yield(2, 0.5) (:406); then Play("root"), wrapMode Loop (:330-335), active (:340).
  // Update (:31-93), active only: follows the owner (:60; the hero stands still here) and, once her actionState !=
  // "attack" or myCommand != "cosmicFriday" (:72-78), DestroyCosmicFriday (:87): CrossFade("destroy", 0.2), wrapMode
  // Once (:566-569), Yield(2, 0.5) (:580), Destroy(gameObject) (:529). The end is the cue's cut (the clip time she
  // leaves "attack"); none = never. No EffectControl: it lives until destroyed, its looping cosmicFriday sound with it.
  api.part("Penguin_cosmicFriday", (fx, node) => {
    play(fx, node, "create", 0, ONCE);                // the component's default clip already (probe.txt); Once
    let t = 0, active = false, endAt = null;
    return { node, update(dt) {
      t += dt;
      if (!active && t >= 0.5) { active = true; play(fx, node, "root", 0, LOOP); }
      if (active && endAt == null && cut(fx)) { endAt = t + 0.5; play(fx, node, "destroy", 0.2, ONCE); }
      if (endAt != null && t >= endAt) return "destroy";
    } };
  });

  // ---------------------------------------------------------------- Penguin_iceBlock
  // Init(life, lv, owner) in the spawn frame (Penguin.cs:10744): mLife = (int)(life + Time.time) (Penguin_iceBlock.cs:51),
  // life = chaAdjust(6) + 6 = 12 s at CHA 1 / LCK 1 (Penguin.cs:10744, CharacterControl.cs:20593); Update (:101-230)
  // destroys the block once mLife < Time.time (:116-120). APPROXIMATED: the int cuts the fraction of Time.time, so the game's
  // block lives 11-12 s; the page takes the spawn at a whole second, 12 s. Its other ends (owner gone :127-131, down
  // :138-142) don't happen here; the ice ticks on foes (:157-211) are logic only. No EffectControl.
  api.part("Penguin_iceBlock", (fx, node) => {
    let t = 0;
    return { node, update(dt) { if ((t += dt) > 12) return "destroy"; } };
  });

  // ---------------------------------------------------------------- Penguin_nAttack (nAttack_fire, spreadShot_fire)
  // Init(owner, ownerID) in the spawn frame (Penguin.cs RPC_nAttack_fire :9672-9681, RPC_spreadShot_fire :11518-11535):
  // velocity = TransformDirection(0, 0, 14) (Penguin_nAttack.cs:103), 14 m/s along its spawn rotation (the cue's rot,
  // on the root); its own life 1.4 s (:25), FixedUpdate life -= dt, Destroy at 0 (:44-53) (the hero's ProjectileControl.life
  // = 1.4 x rangeMod, Penguin.cs:9681, is the same and draws nothing). Rigidbody: no gravity, drag 0, rotation frozen
  // (probe2b.txt): a straight line at constant speed.
  // The end on the ground (decision 1, as the Sheep's decision 3): OnTriggerEnter destroys the ball on any collider not on
  // the owner's layer or layer 1 / 2 (:211-229), the floor included, and its particles (children) go with it. As the
  // Sheep's balls (fxparts/sheep.js), the ball ends when its CENTRE reaches the floor (y 0, the hero's feet): the cue's
  // pitch 4.514 deg from 0.75 m up puts that at the 10 m target point after 0.6807 s (attacks_emotes.md); the game's
  // 0.35 m trigger radius is not counted (decision 1). A level ball never meets the floor and lives its 1.4 s.
  // Staff of Time (decision 18): with the weapon w_pgn59 worn (`weapon == "w_pgn59"`, :115) its life is 12 s (:124), its
  // velocity TransformDirection(0, 0, 0.01) (:127), its trigger 3 m (:139) and the mine flag set (:145), which makes
  // OnTriggerEnter skip layer 0 (:196-202): the floor no longer ends it. The page's worn weapon: the hero's main-hand slot,
  // api.hero().state.R, holding the wardrobe's name for the item: w_pgn59 = "specialScepter" (wardrobe/data/item_map.json,
  // the only code with that model). The weapon is read when the ball is made, as Init reads it.
  const STAFF_OF_TIME = "specialScepter";
  api.part("Penguin_nAttack", (fx, node) => {
    const staff = api.hero()?.state?.R === STAFF_OF_TIME;
    const life = staff ? 12 : 1.4;
    const vel = V(0, 0, staff ? 0.01 : 14).applyQuaternion(fx.uQuat(node));   // TransformDirection at the spawn
    let t = 0;
    return { node, update(dt) {
      t += dt;
      if (t >= life) return "destroy";
      node.position.addScaledVector(vel, dt);
      if (!staff && vel.y < 0 && node.position.y <= 0) return "destroy";   // met the floor (decision 1, above)
      node.updateMatrixWorld(true);
    } };
  });

  // ---------------------------------------------------------------- Penguin_manaMissile (manaMissile_fire)
  // Penguin_manaMissile.cs: its speed (0, 0, 12) (ctor :26); Awake: velocity = TransformDirection(speed) (:45-51), along
  // the spawn rotation (the cue's rot: LookRotation(aim - fire) x Euler(-0.2 |a|, a, 0), Penguin.cs:10220); Init(target,
  // dmg) (:63-79, Penguin.cs:10245). FixedUpdate (:91-134): clock += dt, Destroy at ProjectileControl.life (:98-107) = 3 x
  // rangeMod = 3 s (Penguin.cs:10235); with a target, unless next >= Time.time (:119): next = now + 0.1 (:125), forward =
  // RotateTowards(forward, target.collider.bounds.center - position, 0.15 rad, 1) (:128), rotation = LookRotation(forward)
  // (:131), velocity = TransformDirection(speed) (:134). next starts at 0, so the first FixedUpdate turns already.
  // The turn period: Time.time steps by 0.02 and the test is >=, so the step 0.1 s on (5 steps) is skipped and the turn
  // comes every 6 steps, 0.12 s (Unity's float clock emulated in checks/fx_penguin_build/penguin/missile_sim.py turns every
  // 6 steps but for an odd 5; APPROXIMATED as always 6). Rigidbody: no gravity (probe2b.txt).
  // The target (decision 3): its collider.bounds.center, 0.6 m up at the 10 m point (a Penguin-sized body, the
  // CharacterController h 1, r 0.3, centre 0.6, Penguin.prefab:683-688): the cue's `to`, else (0, 0.6, 10).
  // The end: OnTriggerEnter (:150-214) destroys it on any collider not on the owner's layer or layer 1 / 2 (:193-211).
  //   the target: the missile's 0.3 m trigger sphere (probe2b.txt) meets the body's capsule, i.e. its centre comes within
  //     0.3 + 0.3 m of the capsule's axis (the centre +- 0.2 m in height);
  //   the floor: as decision 1, when the centre reaches y 0 (the outer missiles pass the target and dive onto the floor
  //     behind it: missile_sim.py);
  //   3 s, else.
  // The hit effect it then asks for (manaMissile_hit, RPC_manaMissile_hit) is the cue's, not this part's.
  const BODY_HALF = 0.2, BODY_REACH = 0.6;
  api.part("Penguin_manaMissile", (fx, node) => {
    const to = target(fx, V(0, 0.6, 10));
    let fwd = V(0, 0, 1).applyQuaternion(fx.uQuat(node)), next = -1;   // next in steps: 0 s, before the first step
    const toward = V(), q = new THREE.Quaternion(), onAxis = V();
    const move = stepper(node, k => {
      if (k * STEP >= 3 - 1e-9) return "destroy";      // clock >= life (:101-107)
      if (!(next >= k)) {                              // next >= Time.time: skip (:119)
        next = k + 5;                                  // Time.time + 0.1 (:125), in steps
        fwd = rotateTowards(fwd, toward.subVectors(to, node.position), 0.15);
        node.quaternion.copy(lookRot(fwd, q));         // :131 (the root's own rotation: the cue's rot was the spawn's)
      }
      return fwd.clone().multiplyScalar(12);
    }, p => {
      onAxis.set(to.x, Math.min(to.y + BODY_HALF, Math.max(to.y - BODY_HALF, p.y)), to.z);
      if (p.distanceTo(onAxis) <= BODY_REACH || p.y <= 0) return "destroy";
    });
    return { node, update: dt => move(dt) };
  });

  // ---------------------------------------------------------------- Penguin_snowMan (snowMan) and hiding the hero
  // The snowMan status (CharacterControl.cs:38650-38711): actionState = "snowMan" (:38669), every Renderer under the
  // character switched off (GetComponentsInChildren(typeof(Renderer)) :38678, enabled = false :38692), then Effects/snowMan
  // instantiated at its position, Quaternion.identity (:38705), Init(owner) (:38711). Penguin_snowMan.Init (:20-79) turns it
  // to the owner's rotation (:45: the cue's rot) and scales it by the owner's collider height when taller than 1 m (:48-63;
  // a Penguin-sized body is 1 m: scale 1); Update (:82-135) follows the owner (:116; nobody moves here) while her actionState
  // is "snowMan" (:110), else destroys itself (:124-129). The status's end turns every Renderer on again
  // (removeStatus("snowMan"): actionState "standby" CharacterControl.cs:17449, enabled = true :17455-17469).
  // Decision 17: the page hides the HERO for the snowman's time, through the page's api.heroHide(key, on) (index.html
  // lookSync: every mesh under the hero, outfit, worn props and a skin cue's look, taken off the camera's layers; their
  // visible flags, which the piece viewer and the prop nodes own, and the camera fit's box stay as they are; ignored
  // while VFX is off, so with no snowman drawn she shows). From the spawn until the cue's cut (the snowman's end:
  // "destroy") or the effect's dispose (its kill, a new pick's fxClear, a class switch; fxClear also clears every key).
  // Overlapping snowmen hold one key each: she shows when the last one ends (a piece put on meanwhile is hidden too).
  // (editor 2026-11-10: was a visible = false walk of its own; one hiding mechanism with the page's now.)
  // A cue's hideHero: false leaves her shown: Snow Ball's leftover snowman (the one Snow Man left at the target, standing
  // its last 0.4 s, cast_b.md "snowBall"): decision 17 is Snow Man's own snowman; without it she would blink out 0.4 s.
  // NOTE: in the game the renderers hidden are the snowmanned character's, and Snow Man is cast on an enemy
  // (plans/fx_penguin/cast_b.md: the snowman at the 10 m target, rot 180), so the hero is never hidden there. Decision 17
  // hides her anyway; HIDE_ONLY_ON_HERO = true would hide her only for a snowman spawned on her (within 1 m of her feet),
  // the game's rule.
  const HIDE_ONLY_ON_HERO = false;
  api.part("Penguin_snowMan", (fx, node) => {
    const onHer = Math.hypot(fx.at?.x || 0, fx.at?.d || 0) <= 1;
    const hide = fx.at?.hideHero !== false && (!HIDE_ONLY_ON_HERO || onHer);
    const key = {};                                    // this snowman's own hold
    let on = false;
    const set = v => { if (v !== on) { on = v; api.heroHide(key, v); } };
    if (hide) {
      // Fx.dispose calls each emitter's dispose() (index.html, parts.md Interfaces 3); this Fx's own dispose is wrapped
      // too, so she shows whatever ends it
      const base = fx.dispose;
      fx.dispose = function (...args) { set(false); return base.apply(this, args); };
      set(true);
    }
    return { node, dispose: () => set(false), update() {
      if (cut(fx)) { set(false); return "destroy"; }   // actionState left "snowMan" (:110, :124-129)
    } };
  });
}
