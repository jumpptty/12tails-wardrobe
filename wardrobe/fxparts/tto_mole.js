// wardrobe/fxparts/tto_mole.js: what the Mole's released TTO skills (Barrel Railgun, Missile with Twin Warhead, Kaiser
// Arsenal) draw that no other part does (builder "tto_mole", 2026-11-13; plans/fx_mole/parts.md agent C, the TTO table,
// with its Verification 2-3; plans/fx_mole/tto.md sections 1, 2, 6 with its Verification; decisions.md 10, 22, 30, 31,
// 37, 40, 41). TTO1102 = DecompiledSource_TTO_2026-11-02 (client/GameAssembly.dll): pseudo_c6_extra/mole/<Class>.c and
// pseudo/Mole.c, cited by method and RVA; KaiserArsenalPod and MoleLockReticle (never decompiled before) decompiled here
// with the Bible's tools/run_ghidra.bat (read only) + tools/annotate.py into the session's scratch, cited by RVA.
//
//   MoleRailTurret   barrelRailgun_turret: the 13-part assembly (Steps), the boot / flash / check wobble, Finish, Grow,
//                    the shot's Kick; and the hero's code on it (RPC_barrelRailgun d__418's ride: the ground line, the
//                    charge tiers with teslaCoil, Fire + Kick each 2.4 s cycle; d__430's end: SetTier(0), the shrink)
//   MoleRailgun      the turret's gun (node Gun): SetTier / Fire, the orb, the glows' and channel's _TintColor, the arcs
//   MoleRailBeam     barrelRailgun_beam: Shoot(from, to, tier) at the spawn, the core / glow stretched, the slug, arcs
//   MoleRailArc      barrelRailgun_arc: a jagged bolt on its LineRenderer (tto_sheep.js's, driven), Set / follow, fade
//   MoleRailShock    barrelRailgun_hit / _shock / _lock: pulled toward the camera, two bursts of arcs
//   fx:tto/barrelRailgun_trench    Mole.<RailTrenchSparks>d__427: 2.4 s of arcs along the lane
//   fx:tto/barrelRailgun_overload  Mole.<RPC_barrelRailgun_overload>d__429: 3 shocks 0.7 s apart, then the aura goes
//   MoleLaunchPad    missilePad: rise, hatches, rack, the kicks, the sink; with the cue's `launch` also the 8 launches
//                    (missilePad_launch + the missile: the mole builder's Mole_missile part flies it, through api.spawn)
//   MoleLockReticle  missile_lock: kept at its spot, pulled toward the camera
//   KaiserArsenalPod kaiserArsenalPod: unfold, the 4 locks (PodLock), the kicks (ArsenalShot: the muzzle flash and a
//                    KaiserWarhead from the next muzzle), the fold; Wear (the standing King Kaiser's material)
//   KaiserWarhead    kaiserWarhead: 12 m/s, turning 0.4 rad every 0.15 s, Land on contact or at its life (3.5 s):
//                    kaiserArsenal_hit there (part-made hits)
//
// Cue options read (fx.at = the cue; [x, y, d] = metres right / up / ahead of the hero, the effect's Unity world):
//   barrelRailgun_turret  finish (s after the spawn: Finish, default 6), ride (the ride's start, default finish + 0.65),
//                         rideEnd (RPC_barrelRailgun_end, default ride + 20; the cue's 10 s cut: ride + 10). The shots
//                         are the game's cycle (ride + 2.2 + 2.4 k while the ride lasts), so `shots` is not read
//   barrelRailgun_beam    to (the beam's end, default the spawn spot + 45 m along its forward), tier (default 3)
//   barrelRailgun_trench  from (mRailSpot, default the spawn spot 1 m back along its forward)
//   missilePad            sink (s after the spawn: sinkAt, SinkIn's end), kicks ([s, ...]: each launch's Kick), launch
//                         (true: this part also spawns each kick's missilePad_launch and missile; then the cue file
//                         carries none of them), egg (the egg's chance, default 0.05: every missile a missileBot_fire_bot),
//                         to (the missiles' aim, default the target body (0, 0.6, 10))
//   kaiserArsenalPod      kicks ([s, ...]: the shots from this pod), fold (s: Fold), to (the warheads' target, default
//                         the target body (0, 0.6, 10)), host (the name prefix of the standing King Kaiser whose material
//                         the pod wears, default "KingKaiser")
//   kaiserWarhead         to (the target's bounds centre, default (0, 0.6, 10)), life (ProjectileControl.life, default
//                         3.5: KingKaiser::FireWarhead's arsenal life)
// Space: every root hangs in its effect's mirror group (Unity's world, the hero's feet at the origin, +z her facing, y 0
// the floor); Unity's local numbers apply inside it as they are (three's "YXZ" Euler = Unity's Quaternion.Euler). An
// effect a script Instantiates (api.spawn) is placed from the hero's PRESENT root pose, so every spot handed over goes
// through the world (spawnAt / spawnPoint below): the Barrel Railgun's hero is lifted onto the seat while it shoots
// (decision 40). The target body (Bat decision 4): a cylinder about (0, 0.6, 10), radius 0.3, y 0.1..1.1.
export default function register(api) {
  const { THREE, V } = api;
  const DEG = Math.PI / 180;
  const clamp01 = x => (x < 0 ? 0 : x > 1 ? 1 : x);
  const num = (x, d = 0) => (x !== null && x !== "" && x !== undefined && Number.isFinite(+x) ? +x : d);
  const rnd = (a, b) => a + Math.random() * (b - a);                     // Random.Range(float, float)
  const vec = a => (Array.isArray(a) && a.length >= 3 ? V(num(a[0]), num(a[1]), num(a[2])) : null);
  const ref = (fx, r) => (r && typeof r === "object" && typeof r.node === "number" ? fx.nodes[r.node] || null : null);
  const UP = V(0, 1, 0), FWD = V(0, 0, 1), BODY = [0, 0.6, 10];
  const smooth = x => { x = clamp01(x); return (3 - 2 * x) * x * x; };   // KaiserArsenalPod::Smooth@0x1C82410
  const back = (x, a, b) => { x = clamp01(x) - 1; return (x * a + b) * x * x + 1; };   // ::Back: (2.6, 1.6); MoleLaunchPad::Back: (2.7, 1.7)
  const warned = new Set();
  const warnOnce = (k, ...m) => { if (!warned.has(k)) { warned.add(k); console.warn("tto_mole:", ...m); } };
  // a node's matrix in the effect's Unity world, fresh (fx.uMatrix needs fx.mirrorInv, set after the parts are built)
  const uMat = (fx, o) => { o.updateWorldMatrix(true, false); return fx.mirror.matrixWorld.clone().invert().multiply(o.matrixWorld); };
  const worldPos = (fx, o) => V().setFromMatrixPosition(uMat(fx, o));
  const lossyX = (fx, o) => V().setFromMatrixScale(uMat(fx, o)).x;
  const setWorldPos = (fx, o, w) => {                                   // Transform.set_position
    if (o.parent === fx.mirror) o.position.copy(w);
    else o.position.copy(w.clone().applyMatrix4(uMat(fx, o.parent).invert()));
  };
  const uQuat = (fx, o) => { const q = new THREE.Quaternion(); for (; o && o !== fx.mirror; o = o.parent) q.premultiply(o.quaternion); return q; };
  const setWorldRot = (fx, o, q) => o.quaternion.copy(uQuat(fx, o.parent).invert().multiply(q));   // Transform.set_rotation
  const fwdOf = (fx, o) => FWD.clone().applyQuaternion(uQuat(fx, o));
  // Quaternion.LookRotation(forward, up) in Unity's numbers (Cross is the same formula in either hand; tto_sheep.js)
  const lookRot = (f, q = new THREE.Quaternion()) => {
    if (f.lengthSq() < 1e-12) return q.identity();
    const z = f.clone().normalize(), x = V().crossVectors(UP, z);
    if (x.lengthSq() < 1e-12) x.set(1, 0, 0); x.normalize();
    return q.setFromRotationMatrix(new THREE.Matrix4().makeBasis(x, V().crossVectors(z, x), z));
  };
  const angleAxis = (deg, axis) => new THREE.Quaternion().setFromAxisAngle(axis.clone().normalize(), deg * DEG);
  // Vector3.RotateTowards's direction (the magnitude is not used: every caller takes LookRotation of it)
  const rotateTowards = (a, b, maxRad) => {
    const u = a.clone().normalize(), v = b.clone().normalize(), ang = u.angleTo(v);
    if (ang <= maxRad || ang < 1e-7) return v;
    const ax = V().crossVectors(u, v);
    if (ax.lengthSq() < 1e-12) ax.set(0, 1, 0);
    return u.applyAxisAngle(ax.normalize(), maxRad);
  };
  // the effect's Unity world <-> the page's world (three)
  const toWorld = (fx, p) => { fx.mirror.updateWorldMatrix(true, false); return p.clone().applyMatrix4(fx.mirror.matrixWorld); };
  const fromWorld = (fx, w) => { fx.mirror.updateWorldMatrix(true, false); return w.clone().applyMatrix4(fx.mirror.matrixWorld.clone().invert()); };
  const camPos = fx => fromWorld(fx, api.camera.getWorldPosition(V()));
  const prefixOf = fx => { const i = String(fx.name).lastIndexOf("/"); return i >= 0 ? fx.name.slice(0, i + 1) : ""; };
  // the cue options of an effect a script Instantiates at a pose given as a matrix in fx's Unity world: api.spawn puts
  // its group at the hero root's present pose, so the pose goes through the world into that frame (tto_chameleon.js)
  const heroFrameInv = () => {
    const H = api.hero?.();
    if (!H?.root) return null;
    H.root.updateWorldMatrix(true, false);
    const p = V(), q = new THREE.Quaternion();
    H.root.getWorldPosition(p); H.root.getWorldQuaternion(q);
    return new THREE.Matrix4().compose(p, q, V(1, 1, 1)).multiply(new THREE.Matrix4().makeScale(-1, 1, 1)).invert();
  };
  const spawnAt = (fx, M) => {
    const F = heroFrameInv();
    if (!F) return null;
    fx.mirror.updateWorldMatrix(true, false);
    const pos = V(), rq = new THREE.Quaternion(), s = V();
    F.multiply(fx.mirror.matrixWorld).multiply(M).decompose(pos, rq, s);
    const e = new THREE.Euler().setFromQuaternion(rq, "YXZ");
    return { x: pos.x, y: pos.y, d: pos.z, rot: [e.x / DEG, e.y / DEG, e.z / DEG] };
  };
  const pose = (p, q) => new THREE.Matrix4().compose(p, q || new THREE.Quaternion(), V(1, 1, 1));
  const spawnPoint = (fx, p) => { const a = spawnAt(fx, pose(p)); return a ? [a.x, a.y, a.d] : null; };
  const spawn = (name, at, opts) => {
    if (!at) return null;
    const f = api.spawn?.(name, at, opts);
    if (!f) warnOnce("spawn:" + name, name, "not spawned (not in fx.json: the entry's builds)");
    return f;
  };
  const sound = (fx, name, vol) => { const h = api.Sound?.play(fx.cls, name, vol); if (h) fx.sounds?.push({ node: fx.root, comp: null, h }); };
  // the renderer's own material copies (Unity's MaterialPropertyBlock / renderer.material), shared with any other part
  // that took them first (mesh.userData.fxOwn, uvscroll.js); freed by this part's dispose
  const ownMats = (mesh, mine) => {
    if (mesh.userData.fxOwn) return mesh.userData.fxOwn.mats;
    const cl = [].concat(mesh.material).map(m => {
      if (!m) return m;
      const x = m.clone(); x.onBeforeCompile = m.onBeforeCompile; x.customProgramCacheKey = m.customProgramCacheKey;
      x.userData.fxBlend = m.userData.fxBlend; mine.push(x); return x;
    });
    mesh.material = Array.isArray(mesh.material) ? cl : cl[0];
    mesh.userData.fxOwn = { mats: cl, owner: "tto_mole" };
    return cl;
  };
  // _TintColor (r, g, b, a) on an additive renderer: Unity's Particles/Additive draws 2 x tint.rgb x 2 x tint.a x the
  // texture; fxMaterial's "add" is colour x opacity (premultiplied), so opacity = min(1, 2a) and the colour carries the
  // rest, 2 rgb x max(1, 2a) (an alpha above 0.5 brightens, as in the game)
  const tint = (mesh, c, a, mine) => {
    if (!mesh) return;
    const A = 2 * clamp01(a), b = 2 * Math.max(1, A);
    for (const m of ownMats(mesh, mine)) if (m?.color) { m.color.setRGB(c[0] * b, c[1] * b, c[2] * b, THREE.SRGBColorSpace); m.opacity = Math.min(1, A); }
  };
  const meshOf = o => o?.userData?.fxStatic || null;                  // mesh.js's StaticMesh on that node
  const disposeAll = list => { for (const m of list) m.dispose(); list.length = 0; };

  // ---------------------------------------------------------------- MoleRailArc (barrelRailgun_arc)
  // Fields (the prefab): segments 7, jag 0.16, maxJag 0.6, flicker 0.04, life 0.2 (the callers set it before Set).
  // - Awake@0x1C82C10: its LineRenderer, segments + 1 points, world space; c0 / c1 = its start / end colour.
  // - Set(from, to)@0x1C832B0: a, b, no follow, set, born = now, Jag().
  // - Update@0x1C83430: not set: nothing; age = now - born >= life (or a followed transform gone): Destroy; following:
  //   a / b = the two transforms' positions; now >= nextJag: Jag(); k = 1 - age / life; start / end colour alpha x k.
  // - Jag@0x1C82DC0: nextJag = now + flicker; d = b - a, |d| < 0.0001: every point at a; else dn = d / |d|, side =
  //   normalize(cross(dn, up)) (cross(dn, right) when |.|^2 < 0.0001), n2 = cross(side, dn), amp = min(|d| jag, maxJag);
  //   point i = a + d i / segments, the inner ones + (side Range(-1, 1) + n2 Range(-1, 1)) sin(pi i / segments) amp.
  // On the page: the arc is its own effect (api.spawn: the callers' Instantiate), its points in that effect's Unity
  // world; the callers hand page-world points (setWorld / followW), so spots in another effect's frame come over exactly.
  // An arc nobody Set by its first update is removed (every caller sets it in the spawn frame, as in the game)
  api.part("MoleRailArc", (fx, node, c) => {
    const S = Math.max(1, Math.round(num(c.segments, 7))), jagK = num(c.jag, 0.16), maxJag = num(c.maxJag, 0.6), flicker = num(c.flicker, 0.04);
    let line = null, base = null, k = 1, pts = [], t = 0, born = 0, nextJag = 0, set = false;
    const a = V(), b = V();
    const grab = () => {
      if (line) return line;
      line = fx.emitters.find(x => x.node === node && x.line) || null;
      if (line) {
        line.driven = true; line.world = true; base = line.color;
        line.color = u => { const q = base(u); return [q[0], q[1], q[2], q[3] * k]; };
      } else warnOnce("arcline", "MoleRailArc: no LineRenderer on", fx.name, "(fxparts/tto_sheep.js)");
      return line;
    };
    const jag = () => {
      nextJag = t + flicker;
      const d = b.clone().sub(a), L = d.length();
      pts = [];
      if (L < 0.0001) { for (let i = 0; i <= S; i++) pts.push(a.clone()); return; }
      const dn = d.clone().divideScalar(L), side = V().crossVectors(dn, UP);
      if (side.lengthSq() < 0.0001) side.crossVectors(dn, V(1, 0, 0));
      side.normalize();
      const n2 = V().crossVectors(side, dn), amp = Math.min(L * jagK, maxJag);
      for (let i = 0; i <= S; i++) {
        const u = i / S, p = a.clone().addScaledVector(d, u);
        if (i > 0 && i < S) { const e = Math.sin(Math.PI * u) * amp; p.addScaledVector(side, rnd(-1, 1) * e).addScaledVector(n2, rnd(-1, 1) * e); }
        pts.push(p);
      }
    };
    const em = { node, railArc: true, life: num(c.life, 0.2), followW: null,
      setWorld(aw, bw) { a.copy(fromWorld(fx, aw)); b.copy(fromWorld(fx, bw)); set = true; born = t; jag(); },
      update(dt, cam) {
        t += dt;
        if (!set) return "destroy";
        const age = t - born;
        if (age >= em.life) return "destroy";
        if (em.followW) {
          const aw = em.followW[0](), bw = em.followW[1]();
          if (!aw || !bw) return "destroy";                             // a followed transform is gone
          a.copy(fromWorld(fx, aw)); b.copy(fromWorld(fx, bw));
        }
        if (t >= nextJag) jag();
        k = 1 - age / em.life;
        if (!grab()) return;
        line.pts = pts; line.draw(cam);
      } };
    grab();
    return em;
  });
  // Instantiate(arcPrefab) + life + Set(a, b): a / b in the source effect's Unity world; follow: [getA, getB] page-world
  // getters (MoleRailgun::Arc's coil and muzzle transforms)
  const arcName = (fx, r) => {
    const n = typeof r === "string" ? r : r && typeof r === "object" ? r.name || r.effect || "" : "";
    return n ? (n.includes("/") ? n : prefixOf(fx) + n) : prefixOf(fx) + "barrelRailgun_arc";   // the empty reference: decision 56
  };
  const spawnArc = (fx, name, aU, bU, life, follow) => {
    const f = spawn(name, { x: 0, y: 0, d: 0 });
    const em = f?.emitters.find(e => e.railArc);
    if (!em) { if (f) f.dispose(); return; }
    em.life = life;
    em.setWorld(toWorld(fx, aU), toWorld(fx, bU));
    if (follow) em.followW = follow;
  };

  // ---------------------------------------------------------------- MoleRailShock (barrelRailgun_hit / _shock / _lock)
  // Fields: arcPrefab, arcs, reachMin 0.7, reachMax 1.4, secondWave 0.1, pull.
  // - Start@0x1C84700: with a camera and pull > 0: d = camera - position; |d|^2 > 0.0001: position += normalize(d) x
  //   min(pull x lossyScale.x, |d| / 2); born = now; Burst().
  // - Update@0x1C849D0: the second Burst once now - born >= secondWave.
  // - Burst@0x1C84340: s = lossyScale.x, p = position; per arc: dir = Euler(Range(-50, 25), Range(0, 360), 0) x forward
  //   (the world's, not the node's), an arc with life Range(0.09, 0.17), Set(p + dir 0.15 s, p + dir Range(reachMin,
  //   reachMax) s).
  // On the page Start runs at the first update (the node's pose is built then)
  api.part("MoleRailShock", (fx, node, c) => {
    const arcs = Math.round(num(c.arcs, 5)), lo = num(c.reachMin, 0.7), hi = num(c.reachMax, 1.4), second = num(c.secondWave, 0.1), pull = num(c.pull, 0.6);
    const name = arcName(fx, c.arcPrefab);
    let t = -1, done2 = false;
    const burst = () => {
      const s = lossyX(fx, node), p = worldPos(fx, node);
      for (let i = 0; i < arcs; i++) {
        const dir = FWD.clone().applyQuaternion(new THREE.Quaternion().setFromEuler(new THREE.Euler(rnd(-50, 25) * DEG, rnd(0, 360) * DEG, 0, "YXZ")));
        const life = rnd(0.09, 0.17);
        spawnArc(fx, name, p.clone().addScaledVector(dir, 0.15 * s), p.clone().addScaledVector(dir, rnd(lo, hi) * s), life);
      }
    };
    return { node, update(dt) {
      if (t < 0) {                                                      // Start
        t = 0;
        if (pull > 0 && api.camera) {
          const p = worldPos(fx, node), d = camPos(fx).sub(p);
          if (d.lengthSq() > 0.0001) setWorldPos(fx, node, p.addScaledVector(d.clone().normalize(), Math.min(pull * lossyX(fx, node), d.length() * 0.5)));
        }
        burst();
        return;
      }
      t += dt;
      if (!done2 && t >= second) { done2 = true; burst(); }
    } };
  });

  // ---------------------------------------------------------------- MoleRailBeam (barrelRailgun_beam)
  // Fields: core (node 2), glow (node 1), slug (node 3), arcPrefab, coreColor (1, 1, 1, 1), glowColor (0.45, 0.85, 1, 1),
  // life 0.55, slugSpeed 160; Width (.cctor@0x1C84230) [0.4, 0.55, 0.85, 1.3].
  // - Awake@0x1C83690: core and glow off.
  // - Shoot(a, b, tier)@0x1C83C10 (the hero's code, RPC_barrelRailgun_fire d__424: muzzle, muzzle + 45 dir, 3): from / to,
  //   width = Width[clamp(tier, 0, 3)], born, shot, core and glow on, the slug at a turned along b - a, Draw(0).
  // - Update@0x1C83ED0: age >= life: Destroy; Draw(age); every 0.03 s while age < 0.7 life: an arc, life Range(0.06,
  //   0.14), Set(from + u s, from + u (s + Range(1.5, 3.5))), s = Range(0, max(0, |d| - 3)), u = d / max(|d|, 0.001).
  // - Draw(age)@0x1C83730: d = to - from, L = max(0.01, |d|), f = min(1, age slugSpeed / L), k = 1 - age / life; w =
  //   width x (age < 0.06 ? 1.3 : clamp01(k) 0.85 + 0.15); len = max(0.05, f L); look = LookRotation(d); Place(core, look,
  //   w, len, coreColor, k), Place(glow, look, 2.4 w, len, glowColor, 0.8 k); the slug at Lerp(from, to, clamp01(f)),
  //   shown while f < 1.
  // - Place(r, look, w, len, c, alpha)@0x1C83A80: the renderer's transform at from, look; localScale (w, w, len);
  //   _TintColor (c.rgb, clamp01(alpha) 0.5). The ribbon meshes run 0..1 along z, 1 x 1 across (barrelRailgun_ribbon)
  const BEAM_W = [0.4, 0.55, 0.85, 1.3];
  api.part("MoleRailBeam", (fx, root, c) => {
    const core = ref(fx, c.core), glow = ref(fx, c.glow), slug = ref(fx, c.slug), name = arcName(fx, c.arcPrefab);
    const coreC = c.coreColor || [1, 1, 1, 1], glowC = c.glowColor || [0.45, 0.85, 1, 1], life = num(c.life, 0.55), speed = num(c.slugSpeed, 160);
    const mine = [];
    let t = -1, nextArc = 0, from = null, to = null, width = 0;
    const place = (o, look, w, len, col, alpha) => {
      if (!o) return;
      setWorldPos(fx, o, from); setWorldRot(fx, o, look); o.scale.set(w, w, len);
      tint(meshOf(o), col, alpha * 0.5, mine);
    };
    const draw = age => {
      const d = to.clone().sub(from), L = Math.max(0.01, d.length()), f = Math.min(1, age * speed / L), k = 1 - age / life;
      const w = width * (age < 0.06 ? 1.3 : clamp01(k) * 0.85 + 0.15), len = Math.max(0.05, f * L), look = lookRot(d);
      place(core, look, w, len, coreC, clamp01(k));
      place(glow, look, 2.4 * w, len, glowC, clamp01(0.8 * k));
      if (slug) { setWorldPos(fx, slug, from.clone().lerp(to, clamp01(f))); slug.visible = f < 1; }
    };
    return { node: root, dispose: () => disposeAll(mine), update(dt) {
      if (t < 0) {                                                      // Awake, then the hero's Shoot in the spawn frame
        t = 0;
        from = worldPos(fx, root);
        to = vec(fx.at?.to) || from.clone().addScaledVector(fwdOf(fx, root), 45);
        width = BEAM_W[Math.max(0, Math.min(3, Math.round(num(fx.at?.tier, 3))))];
        if (slug) setWorldRot(fx, slug, lookRot(to.clone().sub(from)));
        draw(0);
        return;
      }
      t += dt;
      if (t >= life) return "destroy";
      draw(t);
      if (t >= nextArc && t < life * 0.7) {
        nextArc = t + 0.03;
        const d = to.clone().sub(from), L = d.length(), s = rnd(0, Math.max(0, L - 3)), u = d.divideScalar(Math.max(L, 0.001));
        spawnArc(fx, name, from.clone().addScaledVector(u, s), from.clone().addScaledVector(u, s + rnd(1.5, 3.5)), rnd(0.06, 0.14));
      }
    } };
  });

  // ---------------------------------------------------------------- MoleRailgun (barrelRailgun_turret's Gun)
  // Fields: glows [Glow1-3], coils [ArcTop1-3], channel, orb, muzzle, arcPrefab, glowColor (0.45, 0.85, 1, 1), size;
  // .cctor@0x1C87B90: OrbSize [0, 0.6, 1, 1.5], ArcGap [0, 0.35, 0.18, 0.08]; .ctor: firedAt -99.
  // - Awake@0x1C87120: the orb's localScale 0; Paint. SetTier(t)@0x1C87850: tier = clamp(t, 0, 3), tierAt = now.
  //   Fire@0x1C87220: firedAt = now, tier 0.
  // - Update@0x1C87890: tier > 0 and now >= nextArc: nextArc = now + Range(0.6, 1.4) ArcGap[tier], Arc(). The orb's
  //   scale moves toward OrbSize[tier] (2 within 0.08 s of a shot) at 6 / s (2.5 / s from 0.6 s after it); localScale =
  //   that x (1 + 0.12 sin(47 now)); Paint.
  // - Paint@0x1C87320: f = clamp01((now - firedAt) / 0.6), draining = f < 1. Glow i: draining: a = 1 - f, colour
  //   lerp(white, glowColor, f); else i < tier: a = 0.65 + 0.2 sin(31 now + 1.7 i) (+ 0.5 clamp01(1 - 4 (now - tierAt))
  //   on the newest, i = tier - 1), else 0; shown while a > 0.01; _TintColor (colour, clamp01(a)). The channel: draining:
  //   1.2 (1 - f), white; else (0.75 + 0.25 sin(53 now)) tier / 3, glowColor; shown while > 0.01; _TintColor (colour,
  //   0.8 clamp01(.)).
  // - Arc@0x1C86E70: n = min(coils, tier); n < 1: none; a = a random coil of the first n; b = another random one (60 %,
  //   n >= 2) else the muzzle (also when it drew a); an arc of life Range(0.08, 0.16) following a and b.
  // The turret part drives it through this emitter (setTier, fire); `now` = the effect's age, the turret's clock too
  const ORB = [0, 0.6, 1, 1.5], ARC_GAP = [0, 0.35, 0.18, 0.08];
  api.part("MoleRailgun", (fx, node, c) => {
    const glowC = c.glowColor || [0.45, 0.85, 1, 1], name = arcName(fx, c.arcPrefab), mine = [];
    const glows = (c.glows || []).map(r => ref(fx, r)), coils = (c.coils || []).map(r => ref(fx, r)).filter(Boolean);
    const channel = ref(fx, c.channel), orb = ref(fx, c.orb), muzzle = ref(fx, c.muzzle);
    let tier = 0, tierAt = 0, firedAt = -99, nextArc = 0, orbScale = 0, started = false;
    const now = () => fx.age;
    const show = (o, on) => { const m = meshOf(o); if (m) m.visible = on; return m; };
    const paint = () => {
      const T = now(), f = clamp01((T - firedAt) / 0.6), draining = f < 1;
      glows.forEach((g, i) => {
        if (!g) return;
        let a = 0;
        if (draining) a = 1 - f;
        else if (i < tier) a = 0.65 + 0.2 * Math.sin(31 * T + 1.7 * i) + (i === tier - 1 ? 0.5 * clamp01(1 - 4 * (T - tierAt)) : 0);
        const m = show(g, a > 0.01);
        const col = draining ? glowC.map(x => 1 + (x - 1) * f) : glowC;
        tint(m, col, clamp01(a), mine);
      });
      if (!channel) return;
      const ch = draining ? (1 - f) * 1.2 : (0.75 + 0.25 * Math.sin(53 * T)) * (tier / 3);
      tint(show(channel, ch > 0.01), draining ? [1, 1, 1] : glowC, 0.8 * clamp01(ch), mine);
    };
    const arc = () => {
      const n = Math.min(coils.length, tier);
      if (n < 1) return;
      const a = coils[Math.floor(Math.random() * n)];
      let b = n >= 2 && Math.random() < 0.6 ? coils[Math.floor(Math.random() * n)] : muzzle;
      if (!b || b === a) b = muzzle;
      if (!a || !b) return;
      const at = o => () => (fx.alive && fx.attached(o) ? o.getWorldPosition(V()) : null);
      spawnArc(fx, name, worldPos(fx, a), worldPos(fx, b), rnd(0.08, 0.16), [at(a), at(b)]);
    };
    const em = { node, railgun: true, dispose: () => disposeAll(mine),
      setTier(t) { tier = Math.max(0, Math.min(3, t)); tierAt = now(); },
      fire() { firedAt = now(); tier = 0; },
      update(dt) {
        const T = now();
        if (!started) { started = true; if (orb) orb.scale.setScalar(0); }   // Awake (the orb node is built after this one)
        if (tier > 0 && T >= nextArc) { nextArc = T + rnd(0.6, 1.4) * ARC_GAP[tier]; arc(); }
        const since = T - firedAt, goal = since < 0.08 ? 2 : ORB[tier], rate = since < 0.6 ? 6 : 2.5;
        orbScale = Math.abs(goal - orbScale) > dt * rate ? orbScale + Math.sign(goal - orbScale) * dt * rate : goal;
        if (orb) orb.scale.setScalar(orbScale * (1 + 0.12 * Math.sin(47 * T)));
        paint();
      } };
    return em;
  });

  // ---------------------------------------------------------------- MoleRailTurret (barrelRailgun_turret) + the ride
  // Fields: head (node 1), cradle (6), seat (24), gun (7's MoleRailgun); KickBack 0.22, KickNod 7, KickTime 0.45,
  // Timeline 6, BootCharge 5.62, BootFlash 5.85, CheckFrom 5.62, CheckTo 6, CheckYaw 12; Steps (.cctor@0x1C86030,
  // tto.md 2.1 and its Verification: part, from, to, offset, axis, spin; the clank is the cued lock's, decision 31).
  // - Awake@0x1C85200: cradleRest; each step's part (found by name under the turret), its rest pose, its renderers.
  // - Assemble(t, total)@0x1C84A40 (T = 6 t / total): per step, every renderer of its part (names starting "Glow",
  //   "Channel", "Ball" left to the gun) on from its `from`; from `from`: k = clamp01((T - from) / max(to - from, 0.01)),
  //   localPosition = rest + offset (1 - BackOut(k)), localRotation = rest x AngleAxis((1 - k)^3 spin, axis) (BackOut@
  //   0x1C856D0: 1 + 2.7 (k - 1)^3 + 1.7 (k - 1)^2). Boot at T >= 5.62: the gun's tier 3, tierAt; flash at 5.85: its
  //   firedAt, tier 0; the check wobble f = clamp01((T - 5.62) / 0.38), checkYaw = sin(2 pi f) 12 (1 - f) inside (0, 1);
  //   head rotation = Euler(0, yaw + checkYaw, 0); T >= 6: Finish.
  // - Finish@0x1C859F0: checkYaw 0, every part at rest and shown, the gun's tier 0.
  // - Grow(k)@0x1C85D40: k < 0.8: 1.08 SmoothStep(k / 0.8), else lerp(1.08, 1, (k - 0.8) / 0.2); localScale = max(0.001, .).
  // - Kick@0x1C85E60 / LateUpdate@0x1C85E80: u = (now - kickedAt) / 0.45 in [0, 1): v = u < 0.12 ? u / 0.12 : 1 -
  //   SmoothStep((u - 0.12) / 0.88), else 0; cradle at cradleRest - (0, 0, 0.22 v), localRotation Euler(-7 v, 0, 0).
  // The hero's code on it (TTO1102:Mole.<RPC_barrelRailgun>d__418::MoveNext@0x1C606D0, pseudo/Mole.c:2754-3382):
  // Grow(1) and Assemble(elapsed, 6) through the cast, Finish at 6; the ride from `ride`: barrelRailgun_line at the
  // turret's spot, the head's rotation, parented to the head, its GroundHugEmitters 3.2 wide (:3154-3174); each 2.4 s
  // cycle k: SetTier(0), tiers 1-3 at 0.6 / 1.3 / 2.0 with teslaCoil 0.4 + 0.15 t (while the cycle's shot <= 20.01 s of
  // ride); the shot at c >= 2.2 (while the ride <= 20): Fire + Kick (RPC_barrelRailgun_fire d__424 :3784-3803; its beam
  // and blasts are cued). The end (<RPC_barrelRailgun_end>d__430@0x1C61B20, :3444-3621) at `rideEnd`: SetTier(0), the line
  // destroyed, Grow(1 - clamp01(2 (t - 0.3))), Destroy at 0.8. The head's yaw stays the hero's facing (no one steers)
  const STEPS = [                                                       // part, from, to, offset, axis, spin
    ["Plate", 0.2, 0.7, [0, -0.35, 0], UP, 0], ["Pedestal", 0.75, 1.35, [0, 2.6, 0], UP, 0],
    ["Cap", 1.4, 1.85, [0, 0.9, 0], UP, 360], ["Ring", 1.9, 2.3, [0, 0.7, 0], UP, -180],
    ["Yoke", 2.3, 2.85, [0, 1.8, 0], V(1, 0, 0), 40], ["Seat", 2.85, 3.35, [0, 0.35, -1.4], V(1, 0, 0), -70],
    ["Grips", 3.35, 3.75, [0, 0.45, -0.25], V(1, 0, 0), 50], ["Drum", 3.8, 4.35, [0, 1.3, -1.5], FWD, 180],
    ["Breech", 4.2, 4.65, [0, 1.2, 0], UP, 90], ["Rails", 4.6, 5.05, [0, 0, -1.25], FWD, 0],
    ["Coil1", 5.0, 5.25, [0, 0.8, 0], FWD, 270], ["Coil2", 5.18, 5.43, [0, 0.8, 0], FWD, -270], ["Coil3", 5.36, 5.61, [0, 0.8, 0], FWD, 270]];
  const TIER_AT = [0, 0.6, 1.3, 2.0];
  const backOut = k => { k -= 1; return 2.7 * k * k * k + 1 + 1.7 * k * k; };
  // the effect data with every GroundHugEmitter of `name` widened (the hero's code writing startWidth / endWidth on the
  // spawned line; the class's own data is shared by every spawn, so a copy of that one effect)
  const widened = (cls, name, w) => {
    const d = api.FX?.json?.[cls], def = d?.effects?.[name];
    if (!def) return null;
    const nodes = def.nodes.map(n => ({ ...n, comps: n.comps.map(c => (c.type === "GroundHugEmitter" ? { ...c, startWidth: w, endWidth: w } : c)) }));
    return { ...d, effects: { ...d.effects, [name]: { ...def, nodes } } };
  };
  api.part("MoleRailTurret", (fx, root, c) => {
    const head = ref(fx, c.head), cradle = ref(fx, c.cradle), pre = prefixOf(fx);
    const finishAt = num(fx.at?.finish, 6), rideAt = num(fx.at?.ride, finishAt + 0.65), rideEnd = num(fx.at?.rideEnd, rideAt + 20);
    let parts = null, gun = null, cradleRest = null, baseScale = null, finished = false, kickedAt = -10;
    let booted = false, flashed = false, riding = false, ended = false, cycle = -1, shown = 0, fired = -1, line = null;
    const find = n => fx.nodes.find((o, i) => i > 0 && o.name === n) || null;
    const underIt = (o, p) => { for (; o && o !== fx.mirror; o = o.parent) if (o === p) return true; return false; };
    const awake = () => {
      cradleRest = cradle?.position.clone() || null;
      baseScale = root.scale.clone();
      parts = STEPS.map(([n, from, to, off, axis, spin]) => {
        const o = find(n);
        if (!o) { warnOnce("part:" + n, "MoleRailTurret: no part", n); return null; }
        const own = fx.nodes.filter(x => underIt(x, o) && !/^(Glow|Channel$|Ball$)/.test(x.name));
        return { o, from, to, off: V(...off), axis, spin, rest: o.position.clone(), restQ: o.quaternion.clone(), own };
      }).filter(Boolean);
    };
    const showPart = (p, on) => { for (const x of p.own) { const m = meshOf(x); if (m) m.visible = on; } };
    const setYaw = check => { if (head) head.quaternion.setFromEuler(new THREE.Euler(0, check * DEG, 0, "YXZ")); };   // the root keeps the hero's facing
    const grow = k => {
      let s;
      if (k < 0.8) { const u = clamp01(k / 0.8); s = (3 * u * u - 2 * u * u * u) * 1.08; }
      else s = 1.08 - 0.08 * clamp01((Math.min(k, 1) - 0.8) / 0.2);
      root.scale.copy(baseScale).multiplyScalar(Math.max(0.001, s));
    };
    const assemble = T => {
      for (const p of parts) {
        showPart(p, T >= p.from);
        if (T < p.from) continue;
        const k = clamp01((T - p.from) / Math.max(p.to - p.from, 0.01));
        p.o.position.copy(p.rest).addScaledVector(p.off, 1 - backOut(k));
        p.o.quaternion.copy(p.restQ).multiply(angleAxis((1 - k) ** 3 * p.spin, p.axis));
      }
      if (gun && !booted && T >= 5.62) { booted = true; gun.setTier(3); }
      if (gun && !flashed && T >= 5.85) { flashed = true; gun.fire(); }
      const f = clamp01((T - 5.62) / 0.38);
      setYaw(f > 0 && f < 1 ? Math.sin(2 * Math.PI * f) * 12 * (1 - f) : 0);
    };
    const finish = () => {
      finished = true; setYaw(0);
      for (const p of parts) { p.o.position.copy(p.rest); p.o.quaternion.copy(p.restQ); showPart(p, true); }
      gun?.setTier(0);
    };
    const startRide = () => {
      riding = true;
      const name = pre + "barrelRailgun_line", data = widened(fx.cls, name, 3.2);
      if (!data) { warnOnce("line", "MoleRailTurret:", name, "not in fx.json (the entry's builds)"); return; }
      const rp = worldPos(fx, root), hq = head ? uQuat(fx, head) : uQuat(fx, root);
      const local = head ? rp.clone().applyMatrix4(uMat(fx, head).invert()) : V();
      line = spawn(name, spawnAt(fx, pose(rp, hq)), { data, followNode: head || root, local: { pos: [local.x, local.y, local.z] } });
    };
    const endRide = () => {
      ended = true; gun?.setTier(0);
      line?.dispose(); line = null;
    };
    const ride = T => {
      const r = T - rideAt, k = Math.floor(r / 2.4), cc = r - 2.4 * k;
      if (k !== cycle) { cycle = k; shown = 0; gun?.setTier(0); }
      if (2.4 * k + 2.2 <= 20.01) for (let t = shown + 1; t <= 3 && cc >= TIER_AT[t]; t++) {
        shown = t; gun?.setTier(t); sound(fx, "teslaCoil", 0.4 + 0.15 * t);
      }
      if (cc >= 2.2 && fired !== k && r <= 20) { fired = k; gun?.fire(); kickedAt = T; }
    };
    const kick = T => {                                                 // LateUpdate
      if (!cradle) return;
      const u = (T - kickedAt) / 0.45;
      const v = u < 0 || u >= 1 ? 0 : u < 0.12 ? u / 0.12 : 1 - smooth((u - 0.12) / 0.88);
      cradle.position.copy(cradleRest).add(V(0, 0, -0.22 * v));
      cradle.quaternion.setFromEuler(new THREE.Euler(-7 * v * DEG, 0, 0, "YXZ"));
    };
    return { node: root, dispose() { line?.dispose(); line = null; }, update(dt) {
      const T = fx.age;
      if (!parts) { awake(); grow(1); }
      gun ||= fx.emitters.find(e => e.railgun) || null;
      if (!finished) { if (T >= finishAt) finish(); else assemble(T); }
      if (finished && !ended && T >= rideAt) {
        if (!riding) startRide();
        if (T >= rideEnd) endRide(); else ride(T);
      }
      if (ended) {
        const g = T - rideEnd;
        if (g >= 0.8) return "destroy";
        grow(1 - clamp01(2 * (g - 0.3)));
      }
      kick(T);
      root.updateMatrixWorld(true);
    } };
  });

  // ---------------------------------------------------------------- the hero's code on the shot's trench and overload
  // fx:tto/barrelRailgun_trench: TTO1102:Mole.<RailTrenchSparks>d__427::MoveNext@0x1C93C70 (Mole.c:24736-24882): until
  // 2.4 s after its start, an arc now, then every Range(0.05, 0.11) s: life Range(0.08, 0.18), a = from + dir Range(1.5,
  // 43) + 0.15 up, b = a + (Euler(0, Range(-35, 35), 0) dir) Range(1, 2.5) + 0.25 up (from = mRailSpot, dir = the shot's)
  api.part("fx:tto/barrelRailgun_trench", fx => {
    let t = 0, next = 0, from = null, dir = null;
    const name = prefixOf(fx) + "barrelRailgun_arc";
    return { node: fx.root, update(dt) {
      if (!from) { dir = fwdOf(fx, fx.root); from = vec(fx.at?.from) || worldPos(fx, fx.root).sub(dir); }
      if (next >= 2.4) return;
      t += dt;
      while (next <= t && next < 2.4) {
        const a = from.clone().addScaledVector(dir, rnd(1.5, 43)).add(V(0, 0.15, 0));
        const turn = dir.clone().applyAxisAngle(UP, rnd(-35, 35) * DEG);
        spawnArc(fx, name, a, a.clone().addScaledVector(turn, rnd(1, 2.5)).add(V(0, 0.25, 0)), rnd(0.08, 0.18));
        next += rnd(0.05, 0.11);
      }
    } };
  });
  // fx:tto/barrelRailgun_overload: <RPC_barrelRailgun_overload>d__429::MoveNext@0x1C62C00 (Mole.c:3955-4295): 3 x
  // (Waits 0.7, barrelRailgun_shock at the foe + 1 up, identity); after the third the aura is destroyed (the arcs to
  // other foes within 4 m: none on the page). The part owns the end: a cue kill at or before 2.1 is dropped, so the
  // third shock is not lost to it
  api.part("fx:tto/barrelRailgun_overload", fx => {
    let t = 0, n = 0, first = true;
    const name = prefixOf(fx) + "barrelRailgun_shock";
    return { node: fx.root, update(dt) {
      if (first) { first = false; if (fx.killAt != null && fx.killAt <= 2.1 + 1e-6) fx.killAt = null; }
      t += dt;
      while (n < 3 && t >= 0.7 * (n + 1)) {
        n++;
        spawn(name, spawnAt(fx, pose(worldPos(fx, fx.root).add(V(0, 1, 0)))));
      }
      if (n >= 3) return "destroy";
    } };
  });

  // ---------------------------------------------------------------- MoleLaunchPad (missilePad)
  // Fields: body (node 1), hatches [HatchHinge1, 2], rack (RackPivot), muzzles [Muzzle0-3]; RiseTime 0.45, Depth 0.8,
  // OpenAt 0.42 - 0.6, HatchOpen 115, RackAt 0.52 - 0.72, RackLift 0.22, SinkTime 0.55, MaxLife 4; Locks (the cued
  // MissilePadLock, decision 31).
  // - Awake@0x1C81D50: Sample(0, -1). Begin@0x1C81DC0 (SpawnPadMissile, at the spawn): bornAt = now. Kick@0x1C81DF0:
  //   kickAt = now. NextMuzzle@0x1C81E10: muzzles[nextTube++ % 4].
  // - Update@0x1C82450: t = now - bornAt; no sink yet and t > 4: sink now; f = now - sinkAt once reached, else -1;
  //   Sample(t, f); f >= 0.55: Destroy.
  // - Sample(t, f)@0x1C81E50: rise = Back((t) / 0.45), hatch = Back((t - 0.42) / 0.18), rack = Smooth((t - 0.52) /
  //   0.2) (Back@0x1C81D70: (x - 1)^2 ((x - 1) 2.7 + 1.7) + 1); sinking: rack = min(rack, 1 - Smooth(f / 0.15)), hatch =
  //   min(hatch, 1 - Smooth((f - 0.1) / 0.15)), rise = min(rise, 1 - Smooth((f - 0.25) / 0.3)); body at (0, -0.8 (1 -
  //   rise), 0); each hatch AngleAxis(-sign(x) 115 hatch, forward); the rack at (0, 0.22 rack - 0.06 j^2, 0), j =
  //   max(0, 1 - (now - kickAt) / 0.12).
  // The launches (TTO1102:Mole.<RPC_missile>d__344 :16316-16333, RPC_missile_fire@0x1C34DE0, FireMissile@0x1C2B3C0),
  // with the cue's `launch`: missile i at kick i: the pad's NextMuzzle, dir = normalize(rotateH(forward, 45 i) x 0.45 +
  // up x 1.4) (rotateH turns left: yaw -45 i), Kick, missilePad_launch at the muzzle, LookRotation(dir), and
  // missileBot_fire (the egg: missileBot_fire_bot, one 5 % roll per cast, MissileBotLevel) at muzzle + dir,
  // LookRotation(dir), `to` its target, `twin` true and `pair` (a new pair on even i, NextTwinPair); the flight and its
  // hits are Mole_missile's (fxparts/mole.js)
  let twinPair = 0;                                                     // Mole::NextTwinPair's counter
  api.part("MoleLaunchPad", (fx, root, c) => {
    const body = ref(fx, c.body), hatches = (c.hatches || []).map(r => ref(fx, r)).filter(Boolean), rack = ref(fx, c.rack);
    const muzzles = (c.muzzles || []).map(r => ref(fx, r)).filter(Boolean), pre = prefixOf(fx);
    const kicks = (Array.isArray(fx.at?.kicks) ? fx.at.kicks.map(x => num(x, NaN)).filter(Number.isFinite) : []).sort((a, b) => a - b);
    const launch = !!fx.at?.launch, egg = launch && Math.random() < num(fx.at?.egg, 0.05);
    let t = 0, sinkAt = fx.at?.sink != null ? num(fx.at.sink, -1) : -1, kickAt = -10, nextTube = 0, k = 0, pair = 0;
    const fire = i => {
      const m = muzzles.length ? muzzles[nextTube++ % muzzles.length] : root;
      const yaw = -45 * i * DEG, dir = V(Math.sin(yaw) * 0.45, 1.4, Math.cos(yaw) * 0.45).normalize();
      kickAt = t;
      if (!launch) return;
      const p = worldPos(fx, m), q = lookRot(dir);
      spawn(pre + "missilePad_launch", spawnAt(fx, pose(p, q)));
      if (i % 2 === 0) pair = ++twinPair;
      const at = spawnAt(fx, pose(p.clone().add(dir), q));
      const to = spawnPoint(fx, vec(fx.at?.to) || V(...BODY));
      if (at) spawn(pre + (egg ? "missileBot_fire_bot" : "missileBot_fire"), { ...at, to, twin: true, pair });
    };
    const sample = (T, f) => {
      let rise = back(T / 0.45, 2.7, 1.7), hatch = back((T - 0.42) / 0.18, 2.7, 1.7), rk = smooth((T - 0.52) / 0.2);
      if (f >= 0) {
        rk = Math.min(rk, 1 - smooth(f / 0.15));
        hatch = Math.min(hatch, 1 - smooth((f - 0.1) / 0.15));
        rise = Math.min(rise, 1 - smooth((f - 0.25) / 0.3));
      }
      if (body) body.position.set(0, -0.8 * (1 - rise), 0);
      for (const h of hatches) h.quaternion.copy(angleAxis(-(h.position.x >= 0 ? 1 : -1) * 115 * hatch, FWD));
      if (rack) { const j = Math.max(0, 1 - (T - kickAt) / 0.12); rack.position.set(0, 0.22 * rk - 0.06 * j * j, 0); }
    };
    return { node: root, update(dt) {
      t += dt;
      while (k < kicks.length && t >= kicks[k]) fire(k++);
      if (sinkAt < 0 && t > 4) sinkAt = t;                             // MaxLife
      const f = sinkAt >= 0 && sinkAt <= t ? t - sinkAt : -1;
      sample(t, f);
      root.updateMatrixWorld(true);
      if (f >= 0.55) return "destroy";
    } };
  });

  // ---------------------------------------------------------------- MoleLockReticle (missile_lock)
  // LateUpdate@0x1C82870 (decompiled here): the first frame, anchor = its position (in its parent's space when it has
  // one); every frame p = the anchor (through the parent), moved toward the camera by min(pull, |camera - p| / 2) when
  // that distance^2 > 0.0001; position = p. pull 1.2 (the prefab; .ctor@0x1C82C00 1.2). On the page the reticle hangs
  // in the mirror group (the target is not a transform), so the anchor is its spawn spot
  api.part("MoleLockReticle", (fx, root, c) => {
    const pull = num(c.pull, 1.2);
    let anchor = null;
    return { node: root, update() {
      anchor ||= root.position.clone();
      const p = anchor.clone();
      if (api.camera) {
        const d = camPos(fx).sub(p), L = d.length();
        if (L * L > 0.0001) p.addScaledVector(d.divideScalar(L), Math.min(pull, L * 0.5));
      }
      root.position.copy(p);
      root.updateMatrixWorld(true);
    } };
  });

  // ---------------------------------------------------------------- KaiserWarhead (kaiserWarhead)
  // Fields mTarget, arsenal; ProjectileControl (0, 0, 12), life set by KingKaiser::FireWarhead@0x1CAF780 (3.5 for the
  // arsenal); Rigidbody no gravity, rotation frozen; trigger box 0.2 x 0.2 x 0.5 centred 0.25 ahead, the root x 1.8.
  // - Awake@0x1CADB20: layer 1, velocity = TransformDirection(pc.velocity).
  // - Update@0x1CAE4A0: age += dt; age >= life: Land(position). With a target, when now > nextTurn: nextTurn = now +
  //   0.15, forward = RotateTowards(forward, the target collider's bounds centre - position, 0.4, 1), rotation =
  //   LookRotation(forward), velocity = TransformDirection(pc.velocity) (the relock to the nearest within 8 m is for a
  //   dead target: none here).
  // - OnTriggerEnter@0x1CAE060: a collider not on the owner's layer, 1 or 2 -> Land(other.ClosestPointOnBounds(position)).
  // - Land(at)@0x1CADC40 -> KingKaiser::WarheadLanded@0x1CB2E70 -> RPC_kaiserArsenal_hit@0x1CB0CA0: kaiserArsenal_hit at
  //   `at`, the Kaiser's rotation (= the hero's facing: rot 0), scale 1; Destroy.
  // On the page: the target body round `to` (its bounds centre, default (0, 0.6, 10): radius 0.3, 1 m tall) and the floor
  // are the colliders; the box is tested as its centre line (back to front) against the cylinder grown by the box's half
  // width, moved on a 0.02 s grid (Unity's physics step) between the frame's turns
  api.part("KaiserWarhead", (fx, root, c, mat, nd) => {
    const pc = nd.comps.find(x => x.type === "ProjectileControl"), speed = vec(pc?.velocity)?.length() || 12;
    const life = num(fx.at?.life, 3.5), to = vec(fx.at?.to) || V(...BODY), name = prefixOf(fx) + "kaiserArsenal_hit";
    let age = 0, nextTurn = 0, fwd = null, s = 1;
    const land = p => {
      spawn(name, spawnAt(fx, pose(p)));
      return "destroy";
    };
    const hit = p => {                                                  // the contact point, or null
      const half = 0.1 * s, len = 0.5 * s;
      for (let i = 0; i <= 4; i++) {
        const q = p.clone().addScaledVector(fwd, len * i / 4);
        if (q.y - half <= 0) return V(p.x, 0, p.z);                     // the floor: ClosestPointOnBounds = under it
        if (Math.hypot(q.x - to.x, q.z - to.z) <= 0.3 + half && q.y >= to.y - 0.5 - half && q.y <= to.y + 0.5 + half)
          return V(Math.max(to.x - 0.3, Math.min(to.x + 0.3, p.x)), Math.max(to.y - 0.5, Math.min(to.y + 0.5, p.y)), Math.max(to.z - 0.3, Math.min(to.z + 0.3, p.z)));
      }
      return null;
    };
    // (the clock and the turns run on the 0.02 s steps, as Mole_missile's: a long frame (a stalled first frame, a tab
    // coming back from the background) would otherwise fly the warhead straight for the whole frame; 2026-11-13, the
    // Mole's QA)
    return { node: root, update(dt) {
      if (!fwd) { fwd = fwdOf(fx, root); s = Math.abs(lossyX(fx, root)) || 1; }
      for (let left = dt; left > 1e-9; left -= 0.02) {
        const h0 = Math.min(0.02, left);
        age += h0;
        if (age >= life) return land(root.position.clone());
        if (age > nextTurn) {
          nextTurn = age + 0.15;
          fwd = rotateTowards(fwd, to.clone().sub(root.position), 0.4);
          lookRot(fwd, root.quaternion);
        }
        root.position.addScaledVector(fwd, speed * h0);
        const h = hit(root.position);
        if (h) return land(h);
      }
      root.updateMatrixWorld(true);                                     // the smoke trail after this part sees the move
    } };
  });

  // ---------------------------------------------------------------- KaiserArsenalPod (kaiserArsenalPod)
  // Fields: ring (node 1), petals [PetalHinge1-4], rack (RackPivot), fins [FinHinge1, 2], muzzles [Muzzle0-6]; .cctor@
  // 0x1CAD990 Locks [4, 3] = (0.38, 0.6, 0), (0.68, 1.0, 1), (0.85, 0.45, 2), (0.98, 0.5, 3) (time after Unfold, clank,
  // lock point); .ctor: unfoldAt / foldAt -1, kickAt -10. Decompiled here (Ghidra over names.tsv, read only):
  // - Awake@0x1CAC8A0: Pose(0, 0, 0, 0, 0). Unfold@0x1CAD650 (SpawnPods, at the spawn): unfoldAt = now, foldAt -1,
  //   locked 0. Fold@0x1CAC920: foldAt = now (once). Kick@0x1CAC950: muzzles[nextTube++ % 7], kickAt = now, spin += 360 / 7.
  // - Update@0x1CAD680: t = now - unfoldAt; each lock whose time has come: while not folding, OnLock(LockPoint(part),
  //   clank) (KingKaiser::PodLock@0x1CB08B0: barrelRailgun_lock there, identity, scale 1.2 + 1.2 clank; TwinSound
  //   megaPunch_hit (clank >= 0.7) or nAttack_hit at 0.3 + 0.4 clank); Sample(t, folding ? now - foldAt : -1).
  // - Sample(t, f)@0x1CAD1D0: pop = Smooth(t / 0.12), petal = Back((t - 0.1) / 0.28), slide = Smooth((t - 0.3) / 0.38),
  //   twist = Back((t - 0.6) / 0.25), fin = Back((t - 0.75) / 0.23) (Back@0x1CAC8D0: (x - 1)^2 ((x - 1) 2.6 + 1.6) + 1);
  //   folding: fin = min(fin, 1 - Smooth(f / 0.15)), twist min 1 - Smooth((f - 0.1) / 0.15), slide min 1 - Smooth((f -
  //   0.2) / 0.25), petal min 1 - Smooth((f - 0.4) / 0.18), pop min 1 - Smooth((f - 0.58) / 0.12); Pose.
  // - Pose(pop, petal, slide, twist, fin)@0x1CACB60: localScale = 0.999 clamp01(pop) + 0.001; each petal hinge
  //   AngleAxis(42 petal, cross(forward, normalize(its (x, y, 0)))); the rack at (0, 0, 0.75 slide - 0.12 j^2), j = max(0,
  //   1 - (now - kickAt) / 0.12), its spinShown toward spin at 900 deg/s, AngleAxis(60 twist + spinShown, forward); each fin
  //   hinge AngleAxis((1 - fin) (x >= 0 ? -1 : 1) 90, forward).
  // - LockPoint(part)@0x1CAC9D0: 0 the ring's position, 3 the first fin's, else rack.TransformPoint(0, 0, 1.25).
  // - Wear(m)@0x1CAD8C0: every renderer below gets m (the King Kaiser's skinned material: the pods take its colour).
  // The Kaiser's code (TTO1102:KingKaiser.<RPC_kaiserArsenal>d__72 :484-603; ArsenalShot@0x1CAF000): at each of the
  // cue's `kicks`, Kick -> its muzzle, dir = normalize(muzzle.forward + 0.35 up); kaiserArsenal_muzzle at the muzzle,
  // LookRotation(dir) (its TwinSound missile_fire 0.55 is cued); FireWarhead: kaiserWarhead there, LookRotation(dir),
  // the target, life 3.5. The fold at `fold`; DropPods is the cue's kill. Wear: the newest standing effect named
  // <host>* (the King Kaiser the robots part builds), its first skinned mesh's material, looked up when the pod first
  // updates; none: the pod keeps its own tto_KingKaiser_k
  const POD_LOCKS = [[0.38, 0.6, 0], [0.68, 1.0, 1], [0.85, 0.45, 2], [0.98, 0.5, 3]];
  const wear = (fx, host) => {
    const k = [...(api.FX?.live || [])].reverse().find(f => f !== fx && f.alive && f.group && String(f.name).startsWith(host));
    let m = null;
    k?.group.traverse(o => { if (!m && o.isSkinnedMesh) m = [].concat(o.material)[0] || null; });
    if (!m) { warnOnce("wear", "KaiserArsenalPod: no standing", host, "to wear (the pod keeps its own material)"); return; }
    for (const o of fx.nodes) { const ms = meshOf(o); if (ms) ms.material = Array.isArray(ms.material) ? ms.material.map(() => m) : m; }
  };
  api.part("KaiserArsenalPod", (fx, root, c) => {
    const ring = ref(fx, c.ring), petals = (c.petals || []).map(r => ref(fx, r)).filter(Boolean), rack = ref(fx, c.rack);
    const fins = (c.fins || []).map(r => ref(fx, r)).filter(Boolean), muzzles = (c.muzzles || []).map(r => ref(fx, r)).filter(Boolean), pre = prefixOf(fx);
    const kicks = (Array.isArray(fx.at?.kicks) ? fx.at.kicks.map(x => num(x, NaN)).filter(Number.isFinite) : []).sort((a, b) => a - b);
    const foldAge = fx.at?.fold != null ? num(fx.at.fold, -1) : -1, to = vec(fx.at?.to) || V(...BODY), host = String(fx.at?.host || "KingKaiser");
    let t = -1, foldAt = -1, locked = 0, kickAt = -10, spin = 0, spinShown = 0, nextTube = 0, k = 0, base = null;
    const lockPoint = part => {
      if (part === 0) return worldPos(fx, ring || root);
      if (part === 3) return worldPos(fx, fins[0] || root);
      return rack ? V(0, 0, 1.25).applyMatrix4(uMat(fx, rack)) : worldPos(fx, root);
    };
    const podPose = (pop, petal, slide, twist, fin, dt) => {
      root.scale.copy(base).multiplyScalar(clamp01(pop) * 0.999 + 0.001);
      for (const h of petals) {
        const n = V(h.position.x, h.position.y, 0);
        h.quaternion.copy(n.lengthSq() > 1e-10 ? angleAxis(petal * 42, V().crossVectors(FWD, n.normalize())) : new THREE.Quaternion());
      }
      if (rack) {
        const j = Math.max(0, 1 - (t - kickAt) / 0.12);
        rack.position.set(0, 0, slide * 0.75 - 0.12 * j * j);
        spinShown = Math.abs(spin - spinShown) > dt * 900 ? spinShown + Math.sign(spin - spinShown) * dt * 900 : spin;
        rack.quaternion.copy(angleAxis(twist * 60 + spinShown, FWD));
      }
      for (const h of fins) h.quaternion.copy(angleAxis((1 - fin) * (h.position.x >= 0 ? -1 : 1) * 90, FWD));
    };
    const sample = (T, f, dt) => {
      let pop = smooth(T / 0.12), petal = back((T - 0.1) / 0.28, 2.6, 1.6), slide = smooth((T - 0.3) / 0.38);
      let twist = back((T - 0.6) / 0.25, 2.6, 1.6), fin = back((T - 0.75) / 0.23, 2.6, 1.6);
      if (f >= 0) {
        fin = Math.min(fin, 1 - smooth(f / 0.15)); twist = Math.min(twist, 1 - smooth((f - 0.1) / 0.15));
        slide = Math.min(slide, 1 - smooth((f - 0.2) / 0.25)); petal = Math.min(petal, 1 - smooth((f - 0.4) / 0.18));
        pop = Math.min(pop, 1 - smooth((f - 0.58) / 0.12));
      }
      podPose(pop, petal, slide, twist, fin, dt);
    };
    const shot = () => {                                                // Kick + ArsenalShot
      const m = muzzles.length ? muzzles[nextTube++ % muzzles.length] : root;
      kickAt = t; spin += 360 / Math.max(1, muzzles.length);
      const p = worldPos(fx, m), dir = fwdOf(fx, m).add(V(0, 0.35, 0)).normalize(), q = lookRot(dir);
      spawn(pre + "kaiserArsenal_muzzle", spawnAt(fx, pose(p, q)));
      const at = spawnAt(fx, pose(p, q));
      if (at) spawn(pre + "kaiserWarhead", { ...at, to: spawnPoint(fx, to), life: 3.5 });
    };
    return { node: root, update(dt) {
      if (t < 0) { t = 0; base = root.scale.clone(); wear(fx, host); podPose(0, 0, 0, 0, 0, 0); }   // Awake + Unfold (+ Wear)
      t += dt;
      if (foldAt < 0 && foldAge >= 0 && t >= foldAge) foldAt = t;
      while (locked < POD_LOCKS.length && t >= POD_LOCKS[locked][0]) {
        const [, clank, part] = POD_LOCKS[locked++];
        if (foldAt >= 0) continue;
        const at = spawnAt(fx, pose(lockPoint(part)));
        if (at) spawn(pre + "barrelRailgun_lock", { ...at, scale: 1.2 + 1.2 * clank });
        sound(fx, clank >= 0.7 ? "megaPunch_hit" : "nAttack_hit", 0.3 + 0.4 * clank);
      }
      sample(t, foldAt >= 0 ? t - foldAt : -1, dt);
      root.updateMatrixWorld(true);
      while (k < kicks.length && t >= kicks[k]) { k++; shot(); }
    } };
  });
}
