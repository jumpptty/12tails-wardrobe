// wardrobe/fxparts/tto_whale.js: TTO's two scripted movers of the Whale's released Leviathan Breach (builder "tto_whale",
// 2026-11-13; plans/fx_whale/decisions.md 44, 45, 62 with 14, 15, 35; plans/fx_whale/tto.md section 6 P1 / P2 and its
// note on fresh clocks, section 2.2, both Verifications (the checker's item 5: the cue's shape); plans/fx_whale/parts.md
// "TTO" table with its Verification 2-3). Both are scripts on their prefab's root, written there by the extractor under
// their own names (wardrobe_fx_tto.py: the root's comps hold {type: "WhaleDolphin"} / {type: "WhaleLeviathan"}, no fields:
// every number is a constant of the code). TTO1102 = DecompiledSource_TTO_2026-11-02 (client/GameAssembly.dll); neither
// type is in its pseudo/, so both were decompiled again here with the Bible's tools/run_ghidra.bat (read only) +
// tools/annotate.py into checks/fx_whale_build/tto/annot/, and the float arguments Ghidra drops read with capstone
// (checks/fx_whale_build/tto/dis.py -> dol_pose.asm, lev_flex.asm). Cited by method and RVA.
//
//   WhaleDolphin     tto/leviathanBreach_dolphin: one dolphin hopping along its lane (TypeDefIndex 4026)
//     Awake@0x1EF5410   mBody = transform.Find("body"); mTail[i] = Math.findChildObject(mBody, TailBones[i]) (tail1-5,
//                       .cctor@0x1EF7270), mFinL / mFinR = findChildObject(mBody, "fin_L" / "fin_R"), each one's
//                       localRotation kept as its rest; body SetActive(false); mSplash = Child("splash"), mTrail =
//                       Child("trail") (Child@0x1EF5870: findChildObject(transform, name), SetActive(false)).
//     Play(points)@0x1EF5C90   (the hero's DolphinLeap right after the Instantiate) mPoints = points; transform.position =
//                       points[0]; rotation = LookRotation(flat(last - first)) (forward when its square is <= 0.0001);
//                       mStart = Time.time; body SetActive(true); Pose(0).
//     Update@0x1EF6F00  n = points - 1 (the hops); t = Time.time - mStart; h = 2 t. While mSplashed <= n and h >=
//                       mSplashed - 0.12 (+ 0.24 for the first): Fire(points[mSplashed], 1 for the first and the last,
//                       else 0.8), mSplashed + 1. mTrail.SetActive(h < n - 0.1 and 0.1 < clamp01(h - floor h) < 0.9).
//                       h > n + 0.05: body SetActive(false), else Pose(min(h, n)). t >= 0.5 n + 2.5: Destroy.
//     Fire(at, scale)@0x1EF5930   Instantiate(mSplash, at, transform.rotation), localScale = one x scale, SetActive(true),
//                       Destroy(it, 3.5): a fresh copy of the `splash` subtree, its clocks starting then.
//     Point(h)@0x1EF5F80   s = clamp(floor h, 0, n - 1), u = clamp01(h - s); lerp(P[s] - 1.4 up, P[s + 1] - 1.4 up, u) + up
//                       (arc + 1.4) 4 u (1 - u), arc = clamp(0.45 |P[s] - P[s + 1]|, 1.8, 3.4).
//     Pose(h)@0x1EF6430   body.position = Point(h) (the world's); f = Point(min(h + 0.03, n)) - Point(max(h - 0.03, 0));
//                       when |f|^2 > 1e-6: body.rotation = LookRotation(normalize f, up) x Euler(0, 0, 20 sin(pi clamp01(h -
//                       floor h))); t = Time.time - mStart; right = body.right: tail i (0-4): localRotation = rest, then
//                       rotation = AngleAxis(18 (i + 1) / 5 sin(16 t - 0.9 i), right) x rotation (in the world, tail1
//                       first, so each bends on top of the ones before); forward = body.forward: fin_L the same with
//                       AngleAxis(12 sin(9 t), forward), fin_R with -12 (the xorps at 0x1EF6D25).
//   WhaleLeviathan   tto/leviathanBreach: the Leviathan's keyed rise, breach and dive (TypeDefIndex 4027)
//     Awake@0x1EF7450   mBody = transform.Find("body"); the tail, head and fin bones under it (findChildObject) and their
//                       rests; mGeyser / mTrail / mCrash / mPool = Child(name) (found, SetActive(false)); mRenderers =
//                       mBody.GetComponentsInChildren<Renderer>(true) (the inactive trail's too); body SetActive(false).
//     Play(spot, dir)@0x1EF8B50   position = spot; rotation = LookRotation(flat dir) (forward when tiny); mStart; body
//                       SetActive(true); Pose(0).
//     Update@0x1EF95D0  t = Time.time - mStart. Once at t >= 0.5: geyser and trail SetActive(true). Once at t >= 2.2:
//                       crash.localPosition = CrashPoint (0, 0, 1.5), crash and pool SetActive(true), trail (false). t >=
//                       7.2 (after the crash): pool SetActive(false). t > KeyT[last] + 0.1 = 3.3: body SetActive(false),
//                       else Pose(t). t >= 8: Destroy.
//     Pose(t)@0x1EF8DE0   i = the segment (while i < 5 and t > KeyT[i + 1]: i + 1), u = clamp01((t - KeyT[i]) / (KeyT[i +
//                       1] - KeyT[i])); body.localPosition = CatmullRom(K[max(i - 1, 0)], K[i], K[i + 1], K[min(i + 2, 6)],
//                       u) (CatmullRom@0x1EF7B30: 0.5 ((3 b - a - 3 c + d) u^3 + (2 a - 5 b + 4 c - d) u^2 + (c - a) u + 2
//                       b)); s = clamp01((3 - 2 u) u^2); body.localRotation = Euler(lerp(KeyPitch, s), 0, 0) x Euler(0, 0,
//                       lerp(KeyRoll, s)); Flex(t); Fade(t). KeyT / KeyPos / KeyPitch / KeyRoll / CrashPoint:
//                       .cctor@0x1EF9990 (the InitializeArray labels and the element stores).
//     Flex(t)@0x1EF8190   right = body.right; amp = t < 1.75 ? 1 : 0.45; bend = sin(pi (t - 1.9) / 0.6) inside 1.9 < t <
//                       2.5, else 0; tail i: rest, then rotation = AngleAxis(9 amp k sin(7 t - 0.8 i) - 10 bend k, right) x
//                       rotation, k = (i + 1) / 5; head: rest, then AngleAxis(3 sin(3.5 t) - 12 bend, right); fin_L: rest,
//                       then AngleAxis(18 sin(4 t), body.forward), fin_R with -18 (0x1EF897A).
//     Fade(t)@0x1EF7D70   a = clamp01((t - 0.4) / 0.3) x (1 - clamp01((t - 2.5) / 0.7)); for every material of every body
//                       renderer that has _TintColor, else _BaseColor, else _Color: that colour with its alpha x a, set
//                       through a MaterialPropertyBlock (the shared material untouched).
//
// On the page
// - The cues (tto.md section 7, unchanged; fx.at = the cue): `[t, "fx", "tto/leviathanBreach_dolphin", {x, d, to: [x, y, d],
//   hops}]`: the cue's own spot is lane[0], `to` the lane's end, the lane = hops + 1 points lerped (WhaleDolphin::Lane
//   @0x1EF5B10; the hero's Row6Ground puts each on the ground: y 0 here), `hops` the hero's LeviathanHops (3 at the 10 m
//   target; without it Hops(the lane's flat length)@0x1EF5AF0: 3 from 7 m, else 2). `[t, "fx", "tto/leviathanBreach",
//   {d}]`: the cue's placement is Play(spot, dir). No cue carries a kill: both parts end their effect themselves (the
//   dolphin 0.5 hops + 2.5 s after its spawn, the Leviathan after 8 s).
// - Clocks: t += dt from the first update (Play runs in the spawn frame). Every node is looked up BY NAME at the first
//   update, never at the build (the root's script is built before its children are named and placed: the Bat's gotcha)
//   and never by index.
// - SetActive on a child: a child the script keeps off starts hidden with its emitters taken out of fx.emitters (so
//   their clocks do not run: fxparts/tto_cat.js's Leash), put back when it is switched on (they start then); switched
//   off again it is hidden and its emitters taken out for good (the Leviathan's trail and pool are never switched on
//   twice). An emitter held out when the effect goes is disposed here (Fx.dispose reaches only fx.emitters).
// - A FRESH effect where the game makes or restarts one (decision 62; no emitter can be restarted in place): the same
//   prefab spawned again through api.spawn with the spawn-only option `only` (never in a cue file):
//     only: "splash"   Fire's copy: only the `splash` subtree shown and running (the body hidden, its emitters out), at
//                      the landing point with the dolphin's rotation and `scale`, `kill: 3.5`
//     only: "trail"    mTrail.SetActive(true) on each hop (Unity clears a deactivated TrailRenderer and ParticleSystem and
//                      starts them again): only the `trail` subtree, riding the dolphin's body (api.spawn's followNode),
//                      disposed when the trail goes off (the game's hide in that frame)
//   so the dolphin's own `splash` and `trail` stay hidden with their emitters held out. Each such spawn is tallied under
//   the prefab's own name in FX.spawned (one dolphin cue = 1 + 4 splashes + 3 trails at 3 hops).
// - Under the floor (decision 45): fx.clipFloor (index.html) on what is under `body` only (the model and core; the trail
//   in its own effect), never on the ground discs; it gives those meshes their own material copies, which Fade then
//   drives: opacity = the material's own x a, looked up on the mesh every frame (uvscroll.js swaps in its own copy on
//   its first update). Faded: the materials whose data holds a tint (_TintColor) or a color (_Color), the extractor's two
//   colour fields (the skins, eye and foam; the trail's mist); APPROXIMATED there: the saved properties stand for
//   Material.HasProperty.
// - The drops under the floor (2026-11-14, the QA pass): every ParticleSystem of the Leviathan and of a splash copy is
//   clipped at the floor as well (clipDrops): they fall through the ground, which the game's terrain hides.
// - Space: the mirror group = Unity's world, so every number above applies as it is (three's "YXZ" Euler = Unity's
//   Quaternion.Euler, setFromAxisAngle = AngleAxis); a bone's world rotation = the product of the local ones up to the
//   mirror (every scale on the way is 1).

// ---------------------------------------------------------------- the scripts' maths (plain numbers and [x, y, z] arrays:
// no three, so checks/fx_whale_build/tto/paths.mjs runs the very functions the parts use)
const c01 = x => (x < 0 ? 0 : x > 1 ? 1 : x);
const mix = (a, b, k) => a + (b - a) * k;
const mix3 = (a, b, k) => [mix(a[0], b[0], k), mix(a[1], b[1], k), mix(a[2], b[2], k)];
export const DOLPHIN = { hop: 0.5, sink: 1.4, afterLife: 2.5, arcMin: 1.8, arcMax: 3.4, arcPerMetre: 0.45, splashLife: 3.5, tails: 5 };
export const dolphinHops = len => (len >= 7 ? 3 : 2);                                    // Hops@0x1EF5AF0
export const dolphinLane = (from, to, hops) => Array.from({ length: hops + 1 }, (_, k) => mix3(from, to, c01(k / hops)));
export const dolphinPoint = (P, h) => {                                                  // Point@0x1EF5F80
  const s = Math.max(0, Math.min(Math.floor(h), P.length - 2)), u = c01(h - s), a = P[s], b = P[s + 1];
  const arc = Math.min(DOLPHIN.arcMax, Math.max(DOLPHIN.arcMin, DOLPHIN.arcPerMetre * Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2])));
  const p = mix3(a, b, u);
  p[1] += (arc + DOLPHIN.sink) * 4 * u * (1 - u) - DOLPHIN.sink;
  return p;
};
export const dolphinForward = (P, h) => {                                                // Pose's f (not normalised)
  const a = dolphinPoint(P, Math.min(h + 0.03, P.length - 1)), b = dolphinPoint(P, Math.max(h - 0.03, 0));
  return [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
};
export const dolphinRoll = h => 20 * Math.sin(Math.PI * c01(h - Math.floor(h)));         // degrees about the body's forward
export const dolphinTail = (i, t) => 18 * (i + 1) / DOLPHIN.tails * Math.sin(16 * t - 0.9 * i);
export const dolphinFin = t => 12 * Math.sin(9 * t);                                     // fin_L; fin_R the negative
export const dolphinSplashH = k => k - 0.12 + (k === 0 ? 0.24 : 0);                      // splash k is due once h >= this
export const dolphinSplashScale = (k, hops) => (k !== 0 && k !== hops ? 0.8 : 1);
export const dolphinTrailOn = (h, hops) => { const f = c01(h - Math.floor(h)); return !(hops - 0.1 <= h) && f > 0.1 && f < 0.9; };
export const dolphinBodyOn = (h, hops) => !(h > hops + 0.05);
export const dolphinLife = hops => DOLPHIN.hop * hops + DOLPHIN.afterLife;

export const LEVIATHAN = {
  keyT: [0.4, 0.6, 1.3, 1.75, 2.2, 2.7, 3.2],
  keyPos: [[0, -9, 0], [0, -5, 0], [0, 7.5, 0.6], [0, 9, 2], [0, 1.2, 3], [0, -2.6, 3.6], [0, -6.5, 4]],
  keyPitch: [-90, -88, -76, -22, 10, 20, 30], keyRoll: [0, 0, 70, 145, 180, 190, 200],
  crashPoint: [0, 0, 1.5], geyserAt: 0.5, crashAt: 2.2, poolOff: 7.2, bodyOff: 3.2 + 0.1, life: 8, tails: 5 };
export const leviathanKey = t => {                                                       // Pose@0x1EF8DE0
  const T = LEVIATHAN.keyT, K = LEVIATHAN.keyPos;
  let i = 0;
  while (i < T.length - 2 && t > T[i + 1]) i++;
  const u = c01((t - T[i]) / (T[i + 1] - T[i])), u2 = u * u, u3 = u2 * u;
  const a = K[Math.max(i - 1, 0)], b = K[i], c = K[i + 1], d = K[Math.min(i + 2, K.length - 1)];
  const pos = [0, 1, 2].map(j => 0.5 * ((3 * b[j] - a[j] - 3 * c[j] + d[j]) * u3 + (2 * a[j] - 5 * b[j] + 4 * c[j] - d[j]) * u2 + (c[j] - a[j]) * u + 2 * b[j]));
  const s = c01((3 - 2 * u) * u2);
  return { i, u, pos, pitch: mix(LEVIATHAN.keyPitch[i], LEVIATHAN.keyPitch[i + 1], s), roll: mix(LEVIATHAN.keyRoll[i], LEVIATHAN.keyRoll[i + 1], s) };
};
export const leviathanFlex = t => {                                                      // Flex@0x1EF8190, degrees
  const amp = t < 1.75 ? 1 : 0.45, bend = t <= 1.9 || t >= 2.5 ? 0 : Math.sin((t - 1.9) * Math.PI / 0.6);
  const tail = Array.from({ length: LEVIATHAN.tails }, (_, i) => { const k = (i + 1) / LEVIATHAN.tails; return Math.sin(7 * t - 0.8 * i) * (amp * 9 * k) - bend * 10 * k; });
  return { tail, head: 3 * Math.sin(3.5 * t) - 12 * bend, fin: 18 * Math.sin(4 * t) };    // fin: fin_L; fin_R the negative
};
export const leviathanFade = t => c01((t - 0.4) / 0.3) * (1 - c01((t - 2.5) / 0.7));    // Fade@0x1EF7D70

export default function register(api) {
  const { THREE, V } = api;
  const DEG = Math.PI / 180;
  const num = (x, d = 0) => (x !== null && x !== "" && x !== undefined && Number.isFinite(+x) ? +x : d);
  const arr3 = a => (Array.isArray(a) && a.length >= 3 ? [num(a[0]), num(a[1]), num(a[2])] : null);
  const UP = V(0, 1, 0), RIGHT = V(1, 0, 0), FWD = V(0, 0, 1);
  const TAILS = ["tail1", "tail2", "tail3", "tail4", "tail5"];                           // TailBones (both .cctors)
  const warned = new Set();
  const warnOnce = (k, ...m) => { if (!warned.has(k)) { warned.add(k); console.warn("tto_whale:", ...m); } };
  const uEuler = (x, y, z) => new THREE.Quaternion().setFromEuler(new THREE.Euler(x * DEG, y * DEG, z * DEG, "YXZ"));
  const angleAxis = (deg, axis) => new THREE.Quaternion().setFromAxisAngle(axis, deg * DEG);
  // Quaternion.LookRotation(forward, Vector3.up) in Unity's numbers (as tto_sheep.js / tto_cat.js)
  const lookRot = f => {
    const q = new THREE.Quaternion();
    if (f.lengthSq() < 1e-12) return q;
    const z = f.clone().normalize(), x = V().crossVectors(UP, z);
    if (x.lengthSq() < 1e-12) x.set(1, 0, 0); x.normalize();
    return q.setFromRotationMatrix(new THREE.Matrix4().makeBasis(x, V().crossVectors(z, x), z));
  };
  // a node's rotation in the effect's Unity world, and Transform.set_rotation
  const uQuat = (fx, o) => { const q = new THREE.Quaternion(); for (; o && o !== fx.mirror; o = o.parent) q.premultiply(o.quaternion); return q; };
  const setWorldRot = (fx, o, q) => o.quaternion.copy(uQuat(fx, o.parent).invert().multiply(q)).normalize();   // (the data's quaternions hold 6 digits)
  // rest, then rotation = AngleAxis(deg, axis) x rotation (Pose / Flex: a turn in the world on top of the rest pose)
  const bend = (fx, o, rest, deg, axis) => { if (!o) return; o.quaternion.copy(rest); setWorldRot(fx, o, angleAxis(deg, axis).multiply(uQuat(fx, o))); };
  // the effect's own nodes by name: Transform.Find (a direct child) and BB's Math.findChildObject (Math.cs:1325-1391; TTO's
  // the same call: the direct child of that name, else the first found down each child in turn). An emitter's mesh hangs
  // under its node too: never a node
  const kid = (t, name) => t?.children.find(o => !o.isMesh && o.name === name) || null;
  const find = (t, name) => {
    if (!t) return null;
    const k = kid(t, name);
    if (k) return k;
    for (const c of t.children) { if (c.isMesh) continue; const r = find(c, name); if (r) return r; }
    return null;
  };
  // ---- GameObject.SetActive on a child of the effect (the header's third point)
  const under = (o, top) => { for (; o; o = o.parent) if (o === top) return true; return false; };
  const sw = node => ({ node, held: [], on: true });
  const hold = (fx, s) => {                                // SetActive(false): hidden, its emitters out (their clocks stand)
    if (!s.node || !s.on) return;
    s.on = false; s.node.visible = false;
    for (let i = fx.emitters.length - 1; i >= 0; i--) {
      const e = fx.emitters[i];
      if (e.node && e.node !== fx.root && under(e.node, s.node)) { s.held.unshift(e); fx.emitters.splice(i, 1); }
    }
  };
  const release = (fx, s) => {                             // SetActive(true): shown, its emitters start now
    if (!s.node || s.on) return;
    s.on = true; s.node.visible = true;
    fx.emitters.push(...s.held); s.held = [];
  };
  const drop = (fx, list) => {                             // the effect goes: the emitters still held out (Fx.dispose's part)
    for (const s of list) {
      for (const e of s.held) try { e.dispose?.(); } catch (x) { console.warn("effect part dispose", fx.name, x); }
      s.held = [];
    }
  };
  // ---- an effect the script Instantiates at a pose of fx's Unity world: api.spawn puts its group at the hero root's
  // PRESENT pose, so the pose goes through the world into that frame (as tto_mole.js / tto_chameleon.js)
  const heroFrameInv = () => {
    const H = api.hero?.();
    if (!H?.root) return null;
    H.root.updateWorldMatrix(true, false);
    const p = V(), q = new THREE.Quaternion();
    H.root.getWorldPosition(p); H.root.getWorldQuaternion(q);
    return new THREE.Matrix4().compose(p, q, V(1, 1, 1)).multiply(new THREE.Matrix4().makeScale(-1, 1, 1)).invert();
  };
  const spawnAt = (fx, p, q) => {
    const M = new THREE.Matrix4().compose(p, q, V(1, 1, 1)), F = heroFrameInv();
    if (F) { fx.mirror.updateWorldMatrix(true, false); M.premultiply(fx.mirror.matrixWorld).premultiply(F); }
    const pos = V(), rq = new THREE.Quaternion(), s = V();
    M.decompose(pos, rq, s);
    const e = new THREE.Euler().setFromQuaternion(rq, "YXZ");
    return { x: pos.x, y: pos.y, d: pos.z, rot: [e.x / DEG, e.y / DEG, e.z / DEG] };
  };
  const spawn = (name, at, opts) => {
    const f = api.spawn?.(name, at, opts);
    if (!f) warnOnce("spawn:" + name, name, "not spawned (not in the class's fx.json: wardrobe_fx_tto.py SKILL_FX)");
    return f || null;
  };
  // every mesh under `node` drawn only above the floor, on its own material copies (fx.clipFloor, index.html); a page
  // without it: the copies alone (Fade must never reach a shared material), freed by Fx.dispose as the clipped ones are
  const ownAll = node => node.traverse(o => {
    if (!o.isMesh || !o.material || o.userData.ownMaterial) return;
    const mine = o.userData.fxOwn?.mats || [];
    const cp = m => {
      if (!m || mine.includes(m)) return m;
      const c = m.clone(); c.onBeforeCompile = m.onBeforeCompile; c.customProgramCacheKey = m.customProgramCacheKey;
      return c;
    };
    o.material = Array.isArray(o.material) ? o.material.map(cp) : cp(o.material);
    o.userData.ownMaterial = true;
  });
  const clip = (fx, node) => {
    if (!node) return;
    if (typeof fx.clipFloor === "function") fx.clipFloor(node);
    else { warnOnce("clipFloor", "fx.clipFloor missing (index.html): nothing hidden under the floor"); ownAll(node); }
  };
  // The drops (2026-11-14, the QA pass): the prefabs' ParticleSystems have no Collision module and fall on under gravity
  // (the crash's rain: up at 10-20 m/s under 2.2 g for 1.4-2.2 s, ending up to 30 m under the ground; the geyser's jet,
  // the splashes' jets and drops the same on a smaller scale), and the game's ground hides them there. Here they showed
  // as a blue column under the pool. So every ParticleSystem node of the effect (under `top`, when given) is clipped at
  // the floor too; the flat discs and bands on the ground are not ParticleSystems and stay whole (decision 45)
  const clipDrops = (fx, data, top) => (data?.effects?.[fx.name]?.nodes || []).forEach((n, i) => {
    const o = fx.nodes?.[i];
    if (o && o !== fx.root && (!top || under(o, top)) && (n.comps || []).some(x => x.type === "ParticleSystem")) clip(fx, o);
  });

  // ---------------------------------------------------------------- WhaleDolphin (tto.md P1)
  api.part("WhaleDolphin", (fx, root, c, mat, nd, data) => {
    const at = fx.at || {}, only = at.only, shut = [];
    let ready = false;
    // ---- the spawn-only copies (the header's fourth point): nothing but one subtree, no script
    if (only === "splash" || only === "trail") {
      return { node: root, update() {
        if (ready) return;
        ready = true;
        const body = kid(root, "body");
        if (only === "splash") { const s = sw(body); shut.push(s); hold(fx, s); clipDrops(fx, data, find(root, "splash")); return; }
        const trail = find(root, "trail");
        for (const o of [find(root, "splash"), ...(body ? body.children.filter(o => !o.isMesh && o !== trail) : [])]) {
          const s = sw(o); shut.push(s); hold(fx, s);
        }
        clip(fx, trail);
      }, dispose() { drop(fx, shut); } };
    }
    // ---- the dolphin. Play(points): the lane from the cue's spot to `to`, the root turned along it
    const from = root.position.toArray(), to = arr3(at.to);
    if (!to) warnOnce("to:" + fx.name, fx.name, "has no cue `to` (the lane's end): the dolphin hops in place");
    const end = to || from, flatLen = Math.hypot(end[0] - from[0], end[2] - from[2]);
    const hops = Math.max(1, Math.trunc(num(at.hops, dolphinHops(flatLen))));
    const P = dolphinLane(from, end, hops);
    root.quaternion.copy(flatLen * flatLen <= 1e-4 ? lookRot(FWD) : lookRot(V(end[0] - from[0], 0, end[2] - from[2])));
    const rootInv = root.quaternion.clone().invert();
    const bodyS = sw(null), splashS = sw(null), trailS = sw(null);
    shut.push(bodyS, splashS, trailS);
    let t = 0, body = null, tails = [], rests = [], finL = null, finR = null, finLRest = null, finRRest = null;
    let splashed = 0, trailFx = null, noTrail = false;      // noTrail: the data lacks the prefab (said once, not asked again)
    const pose = h => {                                     // Pose(h)@0x1EF6430
      if (!body) return;
      const f = dolphinForward(P, h);
      // Transform.set_position / set_rotation on the root's child
      body.position.fromArray(dolphinPoint(P, h)).sub(root.position).applyQuaternion(rootInv).divide(root.scale);
      if (f[0] * f[0] + f[1] * f[1] + f[2] * f[2] > 1e-6) body.quaternion.copy(rootInv).multiply(lookRot(V(f[0], f[1], f[2])).multiply(uEuler(0, 0, dolphinRoll(h)))).normalize();
      const bq = uQuat(fx, body), right = RIGHT.clone().applyQuaternion(bq), fwd = FWD.clone().applyQuaternion(bq), fin = dolphinFin(t);
      tails.forEach((o, i) => bend(fx, o, rests[i], dolphinTail(i, t), right));
      bend(fx, finL, finLRest, fin, fwd); bend(fx, finR, finRRest, -fin, fwd);
    };
    const init = () => {                                    // Awake, then Play's end
      ready = true;
      body = bodyS.node = kid(root, "body");
      if (!body) { warnOnce("body:" + fx.name, fx.name, "has no `body` node"); return; }
      tails = TAILS.map(n => find(body, n)); rests = tails.map(o => o?.quaternion.clone());
      finL = find(body, "fin_L"); finR = find(body, "fin_R");
      finLRest = finL?.quaternion.clone(); finRRest = finR?.quaternion.clone();
      splashS.node = find(root, "splash"); trailS.node = find(root, "trail");
      hold(fx, splashS); hold(fx, trailS);                  // never switched on here: their fresh copies are spawned
      for (const o of body.children) if (!o.isMesh && o !== trailS.node) clip(fx, o);   // the model and the core
      pose(0);
    };
    // the trail's own effect ends: in this frame, at its own update (it is after this one in FX.live: killAt 0), or at
    // once when this effect goes
    const trailOff = now => { if (trailFx?.alive) { if (now) trailFx.dispose(); else trailFx.killAt = 0; } trailFx = null; };
    return { node: root, update(dt) {
      if (!ready) init();
      t += dt;
      const h = 2 * t;                                      // Update@0x1EF6F00
      for (; splashed <= hops && h >= dolphinSplashH(splashed); splashed++)                // Fire(points[k], scale)
        spawn(fx.name, { ...spawnAt(fx, V().fromArray(P[splashed]), root.quaternion), scale: dolphinSplashScale(splashed, hops),
          kill: DOLPHIN.splashLife, only: "splash" });
      if (body) {
        const on = bodyS.on && dolphinTrailOn(h, hops);     // mTrail.SetActive(...)
        if (on && !trailFx?.alive && !noTrail) noTrail = !(trailFx = spawn(fx.name, { only: "trail" }, { followNode: body }));
        else if (!on) trailOff();
        if (!dolphinBodyOn(h, hops)) { trailOff(); hold(fx, bodyS); }
        else pose(Math.min(h, hops));
      }
      if (t >= dolphinLife(hops)) return "destroy";
    }, dispose() { trailOff(true); drop(fx, shut); } };
  });

  // ---------------------------------------------------------------- WhaleLeviathan (tto.md P2)
  api.part("WhaleLeviathan", (fx, root, c, mat, nd, data) => {
    // Play(spot, dir): the cue's placement; the rotation flattened as the script's LookRotation(flat dir)
    const dir = FWD.clone().applyQuaternion(root.quaternion); dir.y = 0;
    root.quaternion.copy(dir.lengthSq() <= 1e-4 ? lookRot(FWD) : lookRot(dir));
    const L = LEVIATHAN, nodesDef = data?.effects?.[fx.name]?.nodes || [];
    const bodyS = sw(null), geyser = sw(null), trail = sw(null), crash = sw(null), pool = sw(null), shut = [bodyS, geyser, trail, crash, pool];
    let ready = false, t = 0, body = null, tails = [], rests = [], head = null, headRest = null, finL = null, finR = null, finLRest = null, finRRest = null;
    let geysered = false, crashed = false;
    // Fade's test (HasProperty _TintColor / _BaseColor / _Color) by the data: the mesh's node names its materials
    const fades = new WeakMap();
    const fadeable = mesh => {
      if (fades.has(mesh)) return fades.get(mesh);
      const n = nodesDef[fx.nodes.indexOf(mesh.parent)];
      const names = [...(n?.mats || []), ...(n?.comps || []).flatMap(x => (Array.isArray(x.mats) ? x.mats : []))].filter(x => typeof x === "string");
      const yes = !names.length || !data?.materials || names.some(x => { const m = data.materials[x]; return !m || !!(m.tint || m.color); });
      fades.set(mesh, yes);
      return yes;
    };
    const fade = a => body.traverse(o => {                  // Fade(t)@0x1EF7D70 (the mesh's present materials: the header)
      if (!o.isMesh || !o.material || !fadeable(o)) return;
      for (const m of [].concat(o.material)) {
        if (!m || typeof m.opacity !== "number") continue;
        if (typeof m.userData.fxFade0 !== "number") m.userData.fxFade0 = m.opacity;
        m.opacity = m.userData.fxFade0 * a;
      }
    });
    const pose = () => {                                    // Pose(t)@0x1EF8DE0
      if (!body) return;
      const k = leviathanKey(t), F = leviathanFlex(t);
      body.position.fromArray(k.pos);
      body.quaternion.copy(uEuler(k.pitch, 0, 0).multiply(uEuler(0, 0, k.roll)));
      const bq = uQuat(fx, body), right = RIGHT.clone().applyQuaternion(bq), fwd = FWD.clone().applyQuaternion(bq);
      tails.forEach((o, i) => bend(fx, o, rests[i], F.tail[i], right));                   // Flex(t)@0x1EF8190
      bend(fx, head, headRest, F.head, right);
      bend(fx, finL, finLRest, F.fin, fwd); bend(fx, finR, finRRest, -F.fin, fwd);
      fade(leviathanFade(t));
    };
    const init = () => {                                    // Awake, then Play's end
      ready = true;
      body = bodyS.node = kid(root, "body");
      if (!body) { warnOnce("body:" + fx.name, fx.name, "has no `body` node"); return; }
      tails = TAILS.map(n => find(body, n)); rests = tails.map(o => o?.quaternion.clone());
      head = find(body, "head"); finL = find(body, "fin_L"); finR = find(body, "fin_R");
      headRest = head?.quaternion.clone(); finLRest = finL?.quaternion.clone(); finRRest = finR?.quaternion.clone();
      geyser.node = find(root, "geyser"); trail.node = find(root, "trail"); crash.node = find(root, "crash"); pool.node = find(root, "pool");
      for (const s of [geyser, trail, crash, pool]) hold(fx, s);
      clip(fx, body);                                       // the body alone (its trail with it), never the ground discs
      clipDrops(fx, data);                                  // and the geyser's, the crash's and the pool's drops
      pose();
    };
    return { node: root, update(dt) {
      if (!ready) init();
      t += dt;                                              // Update@0x1EF95D0
      if (!geysered && t >= L.geyserAt) { geysered = true; release(fx, geyser); if (bodyS.on) release(fx, trail); }
      if (!crashed && t >= L.crashAt) {
        crashed = true;
        crash.node?.position.fromArray(L.crashPoint);
        release(fx, crash); release(fx, pool); hold(fx, trail);
      }
      if (crashed && t >= L.poolOff) hold(fx, pool);
      if (t > L.bodyOff) hold(fx, bodyS);
      else pose();
      if (t >= L.life) return "destroy";
    }, dispose() { drop(fx, shut); } };
  });
}
