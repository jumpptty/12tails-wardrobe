// wardrobe/fxparts/tto_bat.js: what the Bat's TTO skill (Nightfall Swarm, the released one) draws that no other part
// does (2026-11-13, plans/fx_bat/tto.md sections 2.1, 5, 6 P1 / P2 and its Verification; plans/fx_bat/parts.md "TTO:
// Nightfall Swarm's parts" with its Verification corrections 2-3; plans/fx_bat/decisions.md 10, 11, 44). TTO1102 =
// DecompiledSource_TTO_2026-11-02 (client/GameAssembly.dll), read in its pseudo-C (pseudo/Bat.c, cited by line) and
// with capstone for the floats Ghidra drops (checks/fx_bat_research/tto/movenext.asm, flap.asm).
//
//   BatSwarmFlap         TTO's script on nightfallSwarm_bat's root: the two wings' beat (Awake / Update)
//   Bat.NightfallSwarm   the 28 bats' flight and Regather, the coroutine <RPC_nightfallSwarm>d__336 put on the bat's
//                        root by wardrobe_fx_tto.py CODE_MOVERS (state 2 + <Regather>d__337), and the hero hidden
//                        while she is the swarm (HideBody / ShowBody)
//
// Cue options read (fx.at = the cue as index.html's cueOf keeps it): `i` (the bat's index 0-27: its lag behind the
// swarm), `to` ([x, y, d], metres right / up / ahead of the hero: the road's end, the landing; [0, 0, 12.5] for the
// 10 m target, decision 11), `kill` (0.75, the Fx's own: the same Destroy as Regather's). Space: the effect's Unity
// world (the mirror group's space): the hero's feet at the origin, facing +z (Row6Begin turns the Bat to the skill's
// dir, Bat.c:45321), the page's floor at y 0; the hero stays where she stands (variant A, in place, decision 10).
// Time.time = the page's render clock (api.FX.t: it stops with the move on Space, as the move does).
export default function register(api) {
  const { THREE, V, rnd } = api;
  const clamp01 = x => (x < 0 ? 0 : x > 1 ? 1 : x);
  const DEG = Math.PI / 180, UP = V(0, 1, 0), FWD = V(0, 0, 1);
  const now = () => (typeof api.FX?.t === "number" ? api.FX.t : performance.now() / 1000);
  // the mirror group's world matrix, inverted, fresh (Fx.update sets fx.mirrorInv only after the parts are built)
  const mirrorInv = fx => { fx.mirror.updateWorldMatrix(true, false); return fx.mirror.matrixWorld.clone().invert(); };
  const setPos = (fx, o, w) => {                       // Transform.set_position (the bat's root hangs on the mirror)
    if (o.parent === fx.mirror) o.position.copy(w);
    else { o.parent.updateWorldMatrix(true, false); o.position.copy(w.clone().applyMatrix4(mirrorInv(fx).multiply(o.parent.matrixWorld).invert())); }
    o.updateMatrixWorld(true);
  };
  // the hero's feet in the effect's Unity world, read live (C.root: where the Fx group was put at the spawn)
  const heroFeet = fx => {
    const h = api.hero?.();
    return h?.root ? h.root.getWorldPosition(V()).applyMatrix4(mirrorInv(fx)) : V();
  };
  // Quaternion.LookRotation(forward, Vector3.up) in Unity's numbers (as tto_sheep.js / tto_penguin.js)
  const lookRot = (f, q = new THREE.Quaternion()) => {
    const z = f.clone().normalize(), x = V().crossVectors(UP, z);
    if (x.lengthSq() < 1e-12) x.set(1, 0, 0); x.normalize();
    return q.setFromRotationMatrix(new THREE.Matrix4().makeBasis(x, V().crossVectors(z, x), z));
  };
  const ref = (fx, r) => (r && typeof r === "object" && typeof r.node === "number" ? fx.nodes[r.node] || null : null);

  // ---------------------------------------------------------------- BatSwarmFlap (TTO1102, dump.cs:98919-98938; not
  // in pseudo/, read with capstone: flap.asm). Fields: wingL (a Transform: node 4, named WingR), wingR (node 3, WingL),
  // beatsPerSecond 9, amplitude 55, lift 10 (degrees).
  // - Awake@0x1B1AEB0: restL / restR = wingL / wingR.localRotation; phase = Random.Range(0, 6.28319); beatsPerSecond *=
  //   Random.Range(0.85, 1.15) (drawn in that order).
  // - Update@0x1B1AFC0: a = sin(Time.time x beatsPerSecond x 6.28319 + phase) x amplitude + lift (flap.asm
  //   0x1B1B000-0x1B1B04C); wingL.localRotation = restL x AngleAxis(a, Vector3.up), wingR.localRotation = restR x
  //   AngleAxis(-a, up) (the whole angle, lift too, negated: 0x1B1B265 xorps); the product rest x q as written.
  // On the page: the wings' local quaternions are Unity's numbers inside the mirror group (no conversion), and three's
  // setFromAxisAngle is Unity's AngleAxis. The rest = the prefab's local rotation (the node's data; Awake runs after
  // the whole prefab is made, while this part is built before the wing nodes are placed)
  api.part("BatSwarmFlap", (fx, root, c, mat, nd, data) => {
    const wl = ref(fx, c.wingL), wr = ref(fx, c.wingR);
    if (!wl && !wr) { console.warn("BatSwarmFlap: no wing nodes", fx.name, c); return null; }
    const nodes = data?.effects?.[fx.name]?.nodes;
    const restOf = r => (Array.isArray(nodes?.[r?.node]?.rot) ? new THREE.Quaternion().fromArray(nodes[r.node].rot) : null);
    let restL = restOf(c.wingL), restR = restOf(c.wingR);
    const phase = rnd(0, 6.28319), bps = (c.beatsPerSecond ?? 9) * rnd(0.85, 1.15);
    const amp = c.amplitude ?? 55, lift = c.lift ?? 10, q = new THREE.Quaternion();
    return { node: root, update() {
      restL ||= wl?.quaternion.clone(); restR ||= wr?.quaternion.clone();       // no data: the node as built (Awake)
      const a = (Math.sin(now() * bps * 6.28319 + phase) * amp + lift) * DEG;
      if (wl) wl.quaternion.copy(restL).multiply(q.setFromAxisAngle(UP, a));
      if (wr) wr.quaternion.copy(restR).multiply(q.setFromAxisAngle(UP, -a));
    } };
  });

  // ---------------------------------------------------------------- Bat.NightfallSwarm (TTO1102:Bat.<RPC_nightfallSwarm>
  // d__336::MoveNext@0x1B0EFC0, Bat.c:18584-19497, and <Regather>d__337::MoveNext@0x1B25130, Bat.c:25281-25507)
  // State 0 (:18712-18849): dir = normalize(vFlat(offset)), or the forward when about zero; end = mPos + offset; road =
  // SwarmPath(mPos, dir, |offset| + 0.01)@0x1AD2D30 (a ground point every 0.5 m, end added or put in the last point's
  // place), RoadAt(road, len, f)@0x1ACE080 = the point at fraction f of its arc length. State 1 (0.4 s, :18898-19032):
  // HideBody (:18898); side = normalize(Cross(up, dir)) = the hero's right (:18914-18936); per bat i (0x1c of them,
  // :18943-19013), drawn in this order (capstone 0x1B0F52B-0x1B0F672): lane = side x U(-1.1, 1.1) + up x U(0.3, 2.1) +
  // dir x U(-0.6, 0.6), phase = U(0, 6.28); the bat at Row6Chest(Bat) + insideUnitSphere x 0.3, LookRotation(dir);
  // t0 = now, flight = 0x3effffff = 0.49999997 s (:19030-19032), and the state-2 block runs in the same frame.
  // State 2, every frame (:19036-19337): p = clamp01((now - t0) / flight), S = (3 - 2p) p^2; per bat (:19237-19333):
  // u = clamp01(S - ((i % 7) x 0.12 / 7) x (1 - p)) (:19249-19256); position = RoadAt(u) + up x 0.9 + sin(pi p) x (lane +
  // side x 0.3 cos(7 T + phase) + up x 0.35 sin(9 T + phase)), T = Time.time (:19246, :19273-19328); then, when the
  // step's square is over DAT_182f3ff60 (1e-6, capstone 0x1B0FD67), rotation = LookRotation(step / |step|, up)
  // (:19340-19377). The frame p reaches 1 (:19400-19466, after that frame's moves): Regather(bats) (:19418), ShowBody
  // (:19420). Regather: from = each bat's position, t0 = now; each frame (the test first, :25391): at t0 + 0.25 <= now
  // every bat is destroyed (:25406); else k = 4 (now - t0), position = lerp(from, Row6Chest(Bat), clamp01(k^2)) (the
  // chest read every frame, :25421), localScale = one x (1 - 0.8 clamp01(k)) (:25484-25496). Its first pass runs in the
  // landing frame (k 0: the bats stay, scale 1).
  // On the page: mPos = the hero's feet at the spawn (the origin), end = the cue's `to` (the hero stays: variant A), the
  // road flat on the floor, so RoadAt(f) = lerp(mPos, end, f) on a straight road (the ground points all at y 0 and the
  // end past the last one); Row6Chest(Bat) = the hero's feet + 0.9 up (her CharacterController's centre, Bat.prefab:911,
  // TTO's cc.txt), read live. The hero hide (decision 44): a heroHide key per bat from its spawn (HideBody comes in the
  // same 0.4 s frame) to its landing (ShowBody), let go in dispose too. The spawn spot is the cue's (the chest, y 0.9)
  // with no insideUnitSphere jitter, so the first frame's step is 0 and the bat keeps LookRotation(dir) for it (tto.md
  // Verification correction 3: the game faces a random way for that one frame, invisible at 30-60 fps).
  // APPROXIMATED: the game's walls, steps and drops that end the road early (SwarmPath, SwarmLanding): the page's floor
  // is flat and open; the abort (a newer Row6 skill: every bat destroyed, ShowBody) never happens here
  const FLIGHT = 0.49999997;
  api.part("Bat.NightfallSwarm", (fx, root) => {
    let i = fx.at?.i;
    if (typeof i !== "number") { console.warn("Bat.NightfallSwarm: no cue `i` (the bat's index), taken as 0", fx.name); i = 0; }
    const from = heroFeet(fx);
    const to = Array.isArray(fx.at?.to) ? V(fx.at.to[0], fx.at.to[1], fx.at.to[2]) : null;
    if (!to) console.warn("Bat.NightfallSwarm: no cue `to` (the landing), the road taken as 18 m ahead (the no-target length)", fx.name);
    const end = to ? V(to.x, from.y, to.z) : from.clone().addScaledVector(FWD, 18);   // the road on the flat floor
    const flat = V(end.x - from.x, 0, end.z - from.z);
    const dir = flat.lengthSq() > 1e-8 ? flat.normalize() : FWD.clone();
    const side = V().crossVectors(UP, dir).normalize();
    const lane = V().addScaledVector(side, rnd(-1.1, 1.1)).addScaledVector(UP, rnd(0.3, 2.1)).addScaledVector(dir, rnd(-0.6, 0.6));
    const phase = rnd(0, 6.28), lag = ((i % 7) * 0.12) / 7;
    const key = {};                                   // this bat's hold on the hero hide
    api.heroHide?.(key, true);
    root.quaternion.copy(lookRot(dir));               // Instantiate(..., LookRotation(dir))
    root.updateMatrixWorld(true);
    let age = 0, land = null, gather = null, hidden = true;
    const show = () => { if (hidden) { hidden = false; api.heroHide?.(key, false); } };
    const q = new THREE.Quaternion();
    const fly = () => {
      const p = clamp01(age / FLIGHT), S = (3 - 2 * p) * p * p, u = clamp01(S - lag * (1 - p)), T = now();
      const env = Math.sin(Math.PI * p);
      const w = lane.clone().addScaledVector(side, 0.3 * Math.cos(7 * T + phase)).addScaledVector(UP, 0.35 * Math.sin(9 * T + phase));
      const pos = from.clone().lerp(end, u).addScaledVector(UP, 0.9).addScaledVector(w, env);
      const step = pos.clone().sub(root.position);    // the root hangs on the mirror: its position is its Unity world one
      setPos(fx, root, pos);
      if (step.lengthSq() > 1e-6) { root.quaternion.copy(lookRot(step, q)); root.updateMatrixWorld(true); }
      if (p >= 1) {                                    // the landing: Regather starts (its first pass: k 0), ShowBody
        land = age; gather = root.position.clone(); show();
      }
    };
    const regather = () => {
      const tau = age - land;
      if (tau >= 0.25) return "destroy";              // Destroy(bat) at t0 + 0.25 <= now (:25391-25406)
      const k = 4 * tau, chest = heroFeet(fx).addScaledVector(UP, 0.9);
      setPos(fx, root, gather.clone().lerp(chest, clamp01(k * k)));
      root.scale.setScalar(1 - 0.8 * clamp01(k));
      root.updateMatrixWorld(true);
    };
    fly();
    return {
      node: root,
      update(dt) {
        age += dt;
        if (land == null) { fly(); return; }
        return regather();
      },
      dispose() { show(); },
    };
  });
}
