// wardrobe/fxparts/tto_cat.js: what the Cat's TTO skills (Royal Flush, Crescent Eclipse, Drop Anchor: the released ones)
// draw that no other part does (2026-11-13, plans/fx_cat/tto.md sections 2.1-2.3, 5, 6 with its Verification corrections
// 1 and 3; plans/fx_cat/parts.md "TTO" table with its Verification 3; plans/fx_cat/decisions.md 39, 41, 57). TTO1102 =
// DecompiledSource_TTO_2026-11-02 (client/GameAssembly.dll), read in its pseudo-C (pseudo/Cat.c, cited by line) and with
// capstone for the floats Ghidra drops (checks/fx_cat_research/tto/dis.py; the constants' table reads in
// checks/fx_cat_build/tto_cat/rdata.py).
//
//   shaders              Unity's built-in Unlit/Color (the cards' rim, the sword's and blades' edges) and Unlit/Texture
//                        (the card face atlas and back): page materials through api.shader
//   Cat_royalCard        royalFlush_card: SetCard, Deal, Flip, GlowPulse, Gather (Shatter is the other hands' fold:
//                        the page always deals the Royal Flush, decision 39)
//   Cat_royalHandBanner  royalFlush_hand: Show(hand) and its LateUpdate (pop-in, fade, camera-facing, rays' turn)
//   Cat_eclipseFx        crescentEclipse_moon (mode 0: Rise, Eclipse, Set, camera-facing) and crescentEclipse_blade
//                        (mode 1: HoldWeapon = a copy of the hero's worn main-hand weapon, Fling, Recall)
//   Cat.RoyalSwordFall   royalFlush_sword's fall, the coroutine <RoyalSwordFall>d__308 put on its root by
//                        wardrobe_fx_tto.py CODE_MOVERS
//   Cat.DropAnchorFlight dropAnchor_anchor's flight and landing (<DropAnchorFlightAndLand>d__389, CODE_MOVERS), its
//                        inactive Leash's two RingEmitters held back until the landing
//
// Cue options read (fx.at = the cue as index.html's cueOf keeps it; [x, y, d] = metres right / up / ahead of the hero):
//   card     i (which card of the deal: 0-4), to (its slot), flip / pulse / gather (seconds after its spawn: the Flip, the
//            first of the five burst pulses 0.16 s apart, the Gather), gatherTo ([x, y, d]); card (a fixed card number
//            rank + 6 x suit, instead of the deal's: not used by the cues)
//   banner   hand (0-9, 9 = Royal Flush)
//   moon     eclipse (seconds after its spawn when Eclipse() runs)
//   blade    to (its slot), recall (seconds after its spawn), home ([x, y, d], the hero + 1 up), centre ([x, y, d], what
//            the planted blade faces; the hero's feet when left out: the skill drawn in place, decisions 4 / tto Q4)
//   sword    to (the centre it falls to)
//   anchor   to (the spot it lands on); kill (index.html's own) ends it
// Space: everything in the effect's Unity world (the mirror group's space: the hero's feet at the origin, facing +z, the
// floor at y 0); Unity's local numbers (Euler degrees, quaternions) apply inside the mirror as they are; three's "YXZ"
// Euler = Unity's Quaternion.Euler. Every root moved here hangs on the mirror, so its position / quaternion are Unity's
// world ones. Clocks: t += dt from the first update (the coroutines' Time.time from their start, the spawn frame).
// _TintColor (Unity's MaterialPropertyBlock) on the page: the renderer's own copy of its material (freed in dispose),
// colour = the Tint argument's rgb (gamma, as fxMaterial's 2 x _TintColor) and opacity = its alpha; the shared FX.mats
// material is never changed.
export default function register(api) {
  const { THREE, V } = api;
  const DEG = Math.PI / 180;
  const clamp01 = x => (x < 0 ? 0 : x > 1 ? 1 : x);
  const S = x => { x = clamp01(x); return x * x * (3 - 2 * x); };          // the scripts' smoothstep (-2x^3 + 3x^2)
  const num = (x, d = 0) => (Number.isFinite(+x) && x !== null && x !== "" ? +x : d);
  const UP = V(0, 1, 0), DOWN = V(0, -1, 0), RIGHT = V(1, 0, 0), FWD = V(0, 0, 1);
  const uEuler = (x, y, z, q = new THREE.Quaternion()) => q.setFromEuler(new THREE.Euler(x * DEG, y * DEG, z * DEG, "YXZ"));
  const axisAngle = (axis, deg, q = new THREE.Quaternion()) => q.setFromAxisAngle(axis, deg * DEG);
  const vec = a => (Array.isArray(a) && a.length >= 3 ? V(num(a[0]), num(a[1]), num(a[2])) : null);
  const ref = (fx, r) => (r && typeof r === "object" && typeof r.node === "number" ? fx.nodes[r.node] || null : null);
  const meshOf = o => o?.userData?.fxStatic || o?.children?.find(x => x.isMesh) || null;
  // Quaternion.LookRotation(forward, Vector3.up) in Unity's numbers (as tto_sheep.js / tto_penguin.js)
  const lookRot = (f, q = new THREE.Quaternion()) => {
    if (f.lengthSq() < 1e-12) return q.identity();
    const z = f.clone().normalize(), x = V().crossVectors(UP, z);
    if (x.lengthSq() < 1e-12) x.set(1, 0, 0); x.normalize();
    return q.setFromRotationMatrix(new THREE.Matrix4().makeBasis(x, V().crossVectors(z, x), z));
  };
  // Quaternion.Slerp (t clamped) and SlerpUnclamped (three's slerp runs past 1 as Unity's unclamped one)
  const slerp = (a, b, t) => a.clone().slerp(b, clamp01(t));
  const slerpU = (a, b, t) => (t === 1 ? b.clone() : a.clone().slerp(b, t));
  const mirrorInv = fx => { fx.mirror.updateWorldMatrix(true, false); return fx.mirror.matrixWorld.clone().invert(); };
  const camPos = fx => api.camera.getWorldPosition(V()).applyMatrix4(mirrorInv(fx));
  const play = (fx, node, name, vol) => {                // AudioSource.PlayOneShot on the effect (stopped with it)
    if (!name || !api.Sound?.play) return;
    fx.sounds?.push({ node, comp: null, h: api.Sound.play(fx.cls, name, vol) });
  };
  const psOf = (fx, node) => (node ? fx.emitters.find(e => e.node === node && typeof e.play === "function") : null);

  // ---------------------------------------------------------------- materials: the renderer's own copy (_TintColor)
  // A copy of material k of a StaticMesh (mesh.material is always a list there, mesh.js withMaterials); index 0 also
  // as mesh.userData.fxOwn (alphatimer.js's shared per-renderer copy: a later part uses it, never clones again).
  // Material.copy leaves onBeforeCompile / customProgramCacheKey out: fxMaterial's additive alpha lives there
  const UNLIT_TEX = new WeakMap();                        // an Unlit/Texture material -> its texture (per-card copies)
  const ownMat = (mesh, k, list, owner) => {
    if (!mesh) return null;
    if (k === 0 && mesh.userData.fxOwn) return mesh.userData.fxOwn.mats[0];
    const arr = Array.isArray(mesh.material) ? mesh.material : [mesh.material], m = arr[k];
    if (!m) return null;
    let c;
    if (UNLIT_TEX.has(m)) c = unlitTexture(UNLIT_TEX.get(m), m.uniforms.uST.value.toArray());
    else { c = m.clone(); c.onBeforeCompile = m.onBeforeCompile; c.customProgramCacheKey = m.customProgramCacheKey; }
    c.userData.fxBlend = m.userData.fxBlend;
    if (Array.isArray(mesh.material)) mesh.material[k] = c; else mesh.material = c;
    if (k === 0) mesh.userData.fxOwn = { mats: [c], owner };
    list.push(c);
    return c;
  };
  // Tint(r, c): _TintColor = 0.5 c (Cat_eclipseFx::Tint@0x1BE9DE0, Cat_royalCard::SetGlow@0x1BEB210): colour c.rgb,
  // opacity c.a. APPROX: an alpha above 1 (GlowPulse's 1.6 peak) cannot raise opacity: it brightens the colour instead
  const tint = (m, c) => {
    if (!m?.color) return;
    const k = Math.max(1, c[3]);
    m.color.setRGB(c[0] * k, c[1] * k, c[2] * k, THREE.SRGBColorSpace);
    m.opacity = clamp01(c[3]);
  };

  // ---------------------------------------------------------------- Unity's Unlit/Color and Unlit/Texture
  // Unity's built-ins (one pass, Queue Geometry, opaque, ZWrite On, Cull Back): Unlit/Color returns _Color, Unlit/Texture
  // tex2D(_MainTex, uv x _MainTex_ST.xy + _MainTex_ST.zw) (alpha 1). The game's colours are gamma values: _Color made
  // linear (setRGB in sRGB), the texture sampled as sRGB, the output encoded back. Cull Back: inside the mirror group three
  // turns the front face round with the negative determinant, so its front faces are Unity's (as tto_penguin.js's cel
  // shader, mesh.js's FX/Phoenix). Unlit/Texture is a ShaderMaterial with the scale / offset as a uniform (uST), so a
  // card's own copy (SetCard's _MainTex_ST) shares the texture. APPROX: Unity's fog not drawn
  const UT_VERT = `
    uniform vec4 uST;
    varying vec2 vUv;
    void main() {
      vUv = uv * uST.xy + uST.zw;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }`;
  const UT_FRAG = `
    uniform sampler2D map; uniform float uHasMap;
    varying vec2 vUv;
    void main() {
      vec3 c = uHasMap > 0.5 ? texture2D(map, vUv).rgb : vec3(1.0);
      gl_FragColor = linearToOutputTexel(vec4(c, 1.0));
    }`;
  function unlitTexture(tex, st) {
    const m = new THREE.ShaderMaterial({ vertexShader: UT_VERT, fragmentShader: UT_FRAG, side: THREE.FrontSide,
      uniforms: { map: { value: tex }, uHasMap: { value: tex ? 1 : 0 }, uST: { value: new THREE.Vector4(...st) } } });
    UNLIT_TEX.set(m, tex);
    return m;
  }
  if (!api.shader) console.warn("tto_cat: api.shader missing (index.html), Unlit/Color and Unlit/Texture draw as plain alpha");
  api.shader?.("shader:Unlit/Texture", d => {
    let tex = null;
    if (d.tex) {
      tex = api.texLoader.load(`${api.DATA}fx/tex/${d.tex}.webp`);
      tex.colorSpace = THREE.SRGBColorSpace; tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
    }
    return unlitTexture(tex, [...(d.scale || [1, 1]), ...(d.offset || [0, 0])]);
  });
  api.shader?.("shader:Unlit/Color", d => {
    const c = d.props?._Color || d.color || [1, 1, 1, 1];
    const m = new THREE.MeshBasicMaterial({ side: THREE.FrontSide });
    m.color.setRGB(c[0], c[1], c[2], THREE.SRGBColorSpace);
    return m;
  });

  // ---------------------------------------------------------------- Cat_royalCard (tto P1)
  // Fields (probe): model (node 3, Card: materials face / back / rim), faceIndex 0, pivot (node 1), glow (node 2, Halo:
  // tto_royalFlush_halo, additive), plant (node 5, ParticleSystem, playOnAwake off), shards (node 6, Shatter's), sound
  // (the root's AudioSource), dealSound throw1, flipSound twoPair, shatterSound throw_hit, tiltIn 8.
  // - Awake@0x1BEAAA0: SetGlow(0). SetGlow(k)@0x1BEB210 (Cat.c:47604): mGlow = k; glow.enabled = k > 0.01; _TintColor =
  //   (mGlowBase.rgb x 0.5, k x 0.5); mGlowBase is (0, 0, 0, 0) until the Flip (black: an additive glow draws nothing).
  // - SetCard(card)@0x1BEB0B0 (:47512): face material's _MainTex_ST = (1/6, 1/4, (card % 6) / 6, (3 - card / 6) x 0.25).
  //   The cards (Cat::DealHand@0x1B805E0, :39394): hand 9 = ranks 1-5 of one suit (System.Random: here one random suit
  //   per play, decision 39), the five in a shuffled order; card = rank + 6 x suit (0 spade, 1 heart, 2 diamond, 3 club).
  // - Deal(from, to, planted, 0.35, 1.6): <DealRun>d__27::MoveNext@0x1BED260 (:46565-46871): Play(dealSound, 0.7); lean
  //   = planted x Euler(-tiltIn, 0, 0); while u = e / flight < 1: position = from + (to - from) clamp01(1 - (1 - u)^1.35)
  //   + up arc 4u(1 - u) + (planted x right) 0.45 sin(pi u); rotation = Slerp(planted x Euler(90, 0, 0) x AngleAxis(720 u,
  //   forward), lean, S((u - 0.6) / 0.4)); localScale = 0.35 + 0.65 clamp01(sqrt u). Landing: position to, rotation lean,
  //   scale 1, plant.Play(), Play(dealSound, 1), GlowPulse(0.6, 0.25); then 0.16 s: rotation = lean x Euler(12 sin(2 pi s)
  //   (1 - s), 0, 0), s = e / 0.16; then lean.
  // - Flip(0.18): <FlipRun>d__29::MoveNext@0x1BEF0C0 (:46892-47112): Play(flipSound, 0.8); mGlowBase = SuitColors[suit]
  //   (.cctor@0x1BEB650 :48020: (0.55, 0.65, 1), (1, 0.3, 0.42), (1, 0.82, 0.28), (0.4, 1, 0.55), alpha 1); a = pivot's
  //   localRotation, b = a x Euler(0, 180, 0); s = S(e / time): pivot.localRotation = SlerpUnclamped(a, b, s + 0.12
  //   sin(pi s)), localPosition = up 0.42 sin(pi s); then b, zero, GlowPulse(1, 0.4).
  // - GlowPulse(peak, time)@0x1BEAE90: stops the running pulse, starts <Pulse>d__31::MoveNext@0x1BF07D0 (:47359): peak =
  //   max(mGlow, peak); SetGlow(peak + (0.25 - peak) clamp01(1 - (1 - e / time)^2)) (the 2 from capstone 0x1BF086A);
  //   then SetGlow(0.25). The bursts (<RoyalFlushBursts>d__307, :25896-25916): every card GlowPulse(1, 0.3), the last 1.6.
  // - Gather(to, 0.35): <GatherRun>d__34::MoveNext@0x1BEF6F0 (:47135-47334): from / r0 = position / rotation; SetGlow(1);
  //   while u < 1: position = from + (to - from) clamp01(u^2) + (normalize(to - from) x up 1.2 + up 1.5) sin(pi u);
  //   rotation = r0 x AngleAxis(540 u^2, up); localScale = 1 - 0.8 clamp01(u^2); then Destroy.
  // On the page: from / planted = where the cue put the card (hero + 0.45 face + 1.3 up, LookRotation of the slot), to =
  // the cue's `to`; the hero's calls at the cue's times (flip, pulse + 0.16 k, gather) after the spawn. Events falling in
  // one frame run in time order
  const SUIT = [[0.55, 0.65, 1, 1], [1, 0.3, 0.42, 1], [1, 0.82, 0.28, 1], [0.4, 1, 0.55, 1]];
  let deal = null;                                       // this play's hand: { gen, suit, order, used }
  const shuffle = a => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const dealCard = i => {
    const gen = api.FX?.gen ?? 0;
    if (!deal || deal.gen !== gen || deal.used.has(i)) deal = { gen, suit: Math.floor(Math.random() * 4), order: shuffle([1, 2, 3, 4, 5]), used: new Set() };
    deal.used.add(i);
    return deal.order[((i % 5) + 5) % 5] + 6 * deal.suit;
  };
  api.part("Cat_royalCard", (fx, root, c) => {
    const at = fx.at || {};
    const pivot = ref(fx, c.pivot), modelN = ref(fx, c.model), glowN = ref(fx, c.glow), plantN = ref(fx, c.plant);
    const faceIndex = num(c.faceIndex), tiltIn = num(c.tiltIn, 8);
    const from = root.position.clone(), planted = root.quaternion.clone(), to = vec(at.to) || from.clone();
    const lean = planted.clone().multiply(uEuler(-tiltIn, 0, 0));
    const spun = planted.clone().multiply(uEuler(90, 0, 0)), plantedRight = RIGHT.clone().applyQuaternion(planted);
    let i = typeof at.i === "number" ? at.i : deal && deal.gen === (api.FX?.gen ?? 0) ? deal.used.size : 0;
    const card = typeof at.card === "number" ? at.card : dealCard(i), suit = card < 0 ? 0 : Math.floor(card / 6);
    const mats = [];
    let t = 0, ready = false, glowMat = null, glowMesh = null, glowK = 0, glowBase = [0, 0, 0, 0], pulse = null;
    let landed = false, settled = false, flip = null, gather = null;
    const setGlow = k => {
      glowK = k;
      if (glowMesh) glowMesh.visible = k > 0.01;
      tint(glowMat, [glowBase[0], glowBase[1], glowBase[2], k]);
    };
    const glowPulse = (peak, time, t0) => { pulse = { start: t0, peak: Math.max(glowK, peak), time }; };
    const dealPose = u => {
      const e = clamp01(1 - (1 - u) ** 1.35), arc = 1.6 * 4 * u * (1 - u), side = 0.45 * Math.sin(Math.PI * u);
      root.position.copy(from).lerp(to, e).addScaledVector(UP, arc).addScaledVector(plantedRight, side);
      root.quaternion.copy(slerp(spun.clone().multiply(axisAngle(FWD, 720 * u)), lean, S((u - 0.6) / 0.4)));
      root.scale.setScalar(0.35 + 0.65 * clamp01(Math.sqrt(Math.max(0, u))));
    };
    dealPose(0);                                         // the spawn frame: DealRun's first step
    // the hero's calls and the coroutines' own steps, at their times after the spawn
    const events = [];
    if (typeof at.flip === "number") events.push([at.flip, "flip"]);
    if (typeof at.pulse === "number") for (let k = 0; k < 5; k++) events.push([at.pulse + 0.16 * k, "pulse", k === 4 ? 1.6 : 1]);
    if (typeof at.gather === "number") events.push([at.gather, "gather"]);
    const gatherTo = vec(at.gatherTo);
    events.sort((a, b) => a[0] - b[0]);
    const init = () => {
      ready = true;
      const face = meshOf(modelN);
      const fm = ownMat(face, faceIndex, mats, null);
      if (fm?.uniforms?.uST) fm.uniforms.uST.value.set(1 / 6, 0.25, (((card % 6) + 6) % 6) / 6, (3 - Math.floor(card / 6)) * 0.25);
      else if (face) console.warn("Cat_royalCard: the face material is not Unlit/Texture (api.shader): no SetCard", fx.name);
      glowMesh = meshOf(glowN);
      glowMat = ownMat(glowMesh, 0, mats, null);
      setGlow(0);                                        // Awake
      play(fx, root, c.dealSound, 0.7);                  // DealRun's start
    };
    const step = T => {                                  // what happens at time T (an event's, or this frame's)
      if (!landed) {
        if (T < 0.35) { dealPose(T / 0.35); return; }
        landed = true;
        root.position.copy(to); root.quaternion.copy(lean); root.scale.setScalar(1);
        psOf(fx, plantN)?.play();
        play(fx, root, c.dealSound, 1);
        glowPulse(0.6, 0.25, 0.35);
      }
      if (!settled && !gather) {
        const s = (T - 0.35) / 0.16;
        if (s < 1) root.quaternion.copy(lean).multiply(uEuler(12 * Math.sin(2 * Math.PI * s) * (1 - s), 0, 0));
        else { settled = true; root.quaternion.copy(lean); }
      }
      if (flip && !flip.done && pivot) {
        const s = S((T - flip.t0) / 0.18);
        if (T - flip.t0 < 0.18) {
          pivot.quaternion.copy(slerpU(flip.a, flip.b, s + 0.12 * Math.sin(Math.PI * s)));
          pivot.position.copy(UP).multiplyScalar(0.42 * Math.sin(Math.PI * s));
        } else {
          flip.done = true;
          pivot.quaternion.copy(flip.b); pivot.position.set(0, 0, 0);
          glowPulse(1, 0.4, flip.t0 + 0.18);
        }
      }
      if (pulse) {
        const e = T - pulse.start;
        if (e >= pulse.time) { pulse = null; setGlow(0.25); }
        else setGlow(pulse.peak + (0.25 - pulse.peak) * clamp01(1 - (1 - e / pulse.time) ** 2));
      }
      if (gather) {
        const u = (T - gather.t0) / 0.35;
        if (u >= 1) return "destroy";
        const u2 = clamp01(u * u), s = Math.sin(Math.PI * u);
        root.position.copy(gather.from).lerp(gather.to, u2).addScaledVector(gather.side, 1.2 * s).addScaledVector(UP, 1.5 * s);
        root.quaternion.copy(gather.r0).multiply(axisAngle(UP, 540 * u * u));
        root.scale.setScalar(1 - 0.8 * u2);
      }
    };
    const fire = (T, ev) => {
      if (ev[1] === "flip" && !flip && pivot) {
        play(fx, root, c.flipSound, 0.8);
        glowBase = SUIT[suit] || SUIT[0];
        const a = pivot.quaternion.clone();
        flip = { t0: T, a, b: a.clone().multiply(uEuler(0, 180, 0)), done: false };
      } else if (ev[1] === "pulse") glowPulse(ev[2], 0.3, T);
      else if (ev[1] === "gather" && !gather && gatherTo) {
        const gf = root.position.clone(), d = gatherTo.clone().sub(gf);
        const n = d.length() > 1e-5 ? d.clone().divideScalar(d.length()) : V();
        gather = { t0: T, from: gf, to: gatherTo, r0: root.quaternion.clone(), side: V().crossVectors(n, UP) };
        setGlow(1);
      }
    };
    return { node: root, update(dt) {
      if (!ready) init();
      const t1 = t + dt;
      while (events.length && events[0][0] <= t1) {     // the calls in this frame, in time order
        const ev = events.shift();
        if (step(Math.max(t, ev[0])) === "destroy") return "destroy";
        fire(Math.max(t, ev[0]), ev);
      }
      t = t1;
      return step(t);
    }, dispose() { for (const m of mats) m.dispose(); mats.length = 0; } };
  });

  // ---------------------------------------------------------------- Cat_royalHandBanner (tto P2)
  // Fields (probe): hands (10 textures tto_royalFlush_hand0-9), banner (node 4, alpha), glow (node 3, additive), rays (node
  // 2, additive), plate (node 1), life 1.7, fadeTime 0.45.
  // - Awake@0x1BEB980: mBorn = now; base = position; Apply(0, 0).
  // - Show(hand)@0x1BEBE80 (Cat.c:48122): hand clamped to hands; f = hand / 9: mScale = 0.8 + 0.5 min(f, 1) (0.4999999),
  //   mRays = 0.25 + 0.75 min(f, 1); banner's _MainTex = hands[hand] (a property block); mBorn = now.
  // - LateUpdate@0x1BEB9E0 (:48349): e = now - mBorn; e > life: Destroy. rotation = LookRotation(position - camera, up);
  //   pop = e < 0.12: 1.18 S(e / 0.12); e < 0.24: 1.18 - 0.18 clamp01((e - 0.12) / 0.12); else 1 + 0.03 (e - 0.24);
  //   Apply(pop, clamp01(e / 0.08) x clamp01((life - e) / fadeTime)); position = base + up 0.25 clamp01((e - 0.3) / (life -
  //   0.3)); rays' localRotation = Euler(0, 0, -25 e).
  // - Apply(pop, alpha)@0x1BEB830: plate.localScale = max(0.001, pop x mScale); Tint(banner, alpha), Tint(glow, 0.8
  //   alpha), Tint(rays, mRays alpha). Tint@0x1BEC070: the shared material's _TintColor with its alpha x clamp01(alpha).
  // On the page: hand = the cue's `hand` (9 without one); the banner's own material copy carries its texture; opacity =
  // the material's own x clamp01(alpha) (its _TintColor alpha scaled)
  api.part("Cat_royalHandBanner", (fx, root, c) => {
    const hands = Array.isArray(c.hands) ? c.hands : [];
    let hand = Math.trunc(num(fx.at?.hand, 9));
    hand = hand < 0 ? 0 : Math.min(hand, Math.max(0, hands.length - 1));
    const f = Math.min(hand / 9, 1), mScale = 0.8 + 0.4999999 * Math.max(0, f), mRays = 0.25 + 0.75 * Math.max(0, f);
    const life = num(c.life, 1.7), fade = Math.max(1e-4, num(c.fadeTime, 0.45));
    const plate = ref(fx, c.plate), raysN = ref(fx, c.rays), base = root.position.clone();
    const mats = [], tex = [];
    let t = 0, R = null;                                 // R: [[material, its own opacity, alpha factor]]
    const init = () => {                                 // (the plate's own transform is set after this root part is built)
      R = [];
      for (const [r, k] of [[c.banner, 1], [c.glow, 0.8], [c.rays, mRays]]) {
        const m = ownMat(meshOf(ref(fx, r)), 0, mats, null);
        if (m) R.push([m, m.opacity, k]);
      }
      const bm = R[0]?.[0], name = hands[hand];
      if (bm && name && "map" in bm) {                   // Show: _MainTex = hands[hand]
        const tx = api.texLoader.load(`${api.DATA}fx/tex/${name}.webp`);
        tx.colorSpace = THREE.SRGBColorSpace; tx.wrapS = tx.wrapT = THREE.RepeatWrapping;
        bm.map = tx; bm.needsUpdate = true; tex.push(tx);
      }
    };
    const apply = (pop, alpha) => {
      if (plate) plate.scale.setScalar(Math.max(0.001, pop * mScale));
      for (const [m, o, k] of R) m.opacity = o * clamp01(alpha * k);
    };
    return { node: root, update(dt) {
      if (!R) init();
      t += dt;
      if (t > life) return "destroy";
      root.quaternion.copy(lookRot(root.position.clone().sub(camPos(fx))));
      const pop = t < 0.12 ? 1.18 * S(t / 0.12) : t < 0.24 ? 1.18 - 0.18 * clamp01((t - 0.12) / 0.12) : 1 + 0.03 * (t - 0.24);
      apply(pop, clamp01(t / 0.08) * clamp01((life - t) / fade));
      root.position.copy(base).addScaledVector(UP, 0.25 * clamp01((t - 0.3) / (life - 0.3)));
      if (raysN) uEuler(0, 0, -25 * t, raysN.quaternion);
    }, dispose() { for (const m of mats) m.dispose(); for (const x of tex) x.dispose(); mats.length = tex.length = 0; } };
  });

  // ---------------------------------------------------------------- Cat_eclipseFx (tto P4)
  // Fields (probe): mode (0 moon, 1 blade), pivot, glow, disc, shadow, corona (Renderers), bite (ParticleSystem,
  // playOnAwake off), sound, landSound disarm_hit, igniteSound none, moonSize 7.
  // - Awake@0x1BE8070 (Cat.c:44891): mBorn = now; mTrail = the pivot's TrailRenderer; mCoronaScale = corona's
  //   localScale. Blade: Tint(glow, (1, 1, 1, 0.6)) (the constant at 0x1830052D0). Moon: Tint(disc / glow / corona,
  //   (1, 1, 1, 0)), shadow localPosition (-1.2, 0, -0.02), Tint(shadow, (1, 1, 1, 0)), StartCoroutine(Rise).
  // - LateUpdate@0x1BE9930: moon only: rotation = LookRotation(position - camera, up).
  // - Moon: <Rise>d__24::MoveNext@0x1BF3A20 (:44552-44716), while not eclipsed: top = the spawn; for 0.6 s s = S(e / 0.6):
  //   position = top - up 2.5 (1 - s), localScale = moonSize (0.6 + 0.4 s), Tint(disc, (1, 1, 1, s)), Tint(glow, (0.75,
  //   0.85, 1, 0.7 s)); then top, moonSize, and until mBorn + 6 Tint(glow, (0.75, 0.85, 1, 0.7 (0.85 + 0.15 sin(5 e))));
  //   then Set(0.5, false). Eclipse()@0x1BE83D0: once: mEclipsed (Rise stops), igniteSound (none), EclipseRun.
  //   <EclipseRun>d__26::MoveNext@0x1BEDE70 (:43483-43677): localScale = moonSize; 0.18 s, s = S(e / 0.18): shadow
  //   localPosition (1.2 s - 1.2, 0, -0.02), Tint(shadow, (1, 1, 1, s)), Tint(corona, (1, 1, 1, s)), Tint(glow, (1, 0.25,
  //   0.2, 0.9 s)), Tint(disc, (1, 0.55, 0.5, 1)) (0x1830052E0); then 0.9 s, p = e / 0.9: corona localScale =
  //   mCoronaScale (1 + 0.18 sin(pi min(1, 2.5 p))), localRotation Euler(0, 0, 32 p), Tint(glow, (1, 0.25, 0.2, 0.65 + 0.25
  //   exp(-5 p))) (capstone 0x1BEE32E: FUN_18030cf20 = expf, continuous with the 0.9 before); then Set(0.7, true).
  //   <Set>d__27::MoveNext@0x1BF5230 (:44739-44844): from = position; u = e / time < 1, f = 1 - u: Tint(disc, (1, red ?
  //   0.55 : 1, red ? 0.5 : 1, f)), Tint(shadow / corona, (1, 1, 1, f)), Tint(glow, red ? (1, 0.25, 0.2, 0.9 f) : (0.75,
  //   0.85, 1, 0.7 f)), position = from + up 0.8 u; then Destroy.
  // - Blade: HoldWeapon(weapon)@0x1BE8660 (:45235-45843), the worn weapon when active: a copy under a new holder (local
  //   identity), its scripts / joints / colliders / rigidbodies / audio / animators stripped; the bounds of every mesh
  //   renderer's mesh (8 corners, TransformPoint then the copy's InverseTransformPoint) -> centre c, size z; the longest
  //   axis a (x unless x < y or x < z; then z when y < z, else y), turned toward its far end from the copy's origin
  //   (reach = c + z/2 along a, or -(c - z/2) and -a when that is longer); s = |weapon.lossyScale.x| x 1.5 (HeldScale); rot =
  //   FromToRotation(a, down); the copy under pivot with localRotation rot, localScale s, localPosition (-p.x, s reach - 0.2
  //   z_a s, -p.z), p = rot x (s c): the far end down, 0.2 of its length below the pivot; pivot's "Model" and glow switched
  //   off (glow = null), mTrail's localPosition (0, -0.2 z_a s, 0) (the tip); mHeld = true. No mesh bounds: nothing.
  //   Fling(from, to, centre, 0.22): <FlingRun>d__31::MoveNext@0x1BEE430 (:43698-44117): planted = LookRotation(vFlat(centre
  //   - to) or forward) x Euler(mHeld ? 30 : -25, 0, 0); dir = normalize(to - from), flying = LookRotation(dir); u = e /
  //   flight < 1: position = from + (to - from) clamp01(u^2) + (normalize(up x dir) 0.65 + up 0.8) sin(pi u); rotation =
  //   Slerp(flying, planted, k), k = S((u - 0.72) / 0.28); pivot localRotation = AngleAxis(-1080 (1 - k) u, right).
  //   Landing: position to, rotation planted, pivot identity, bite.Play(), PlayOneShot(landSound, 0.7), Tint(glow, (1, 1,
  //   1, 1)); then until mEclipsed, q = now - landed: pivot localRotation = Euler(14 sin(38 q) exp(-14 q), 0, 0), Tint(glow,
  //   (0.82, 0.7, 1, 0.65 + 0.2 sin(12 q))) (capstone 0x1BEF002).
  //   Recall(to, 0.14)@0x1BE9B80: once (mEclipsed): StopAllCoroutines, pivot identity; <RecallRun>d__33::MoveNext@0x1BF31E0
  //   (:44267-44529): from / q0 / s0 = position / rotation / localScale; inbound = LookRotation(normalize(to - from)) x
  //   Euler(-90, 0, 0) (q0 when closer than 0.01); u = e / flight < 1: position = from + (to - from) clamp01(u^2) + up 0.6
  //   sin(pi u); rotation = Slerp(q0, inbound, min(1, 3 u)); localScale = s0 (1 - 0.6 clamp01(4 (u - 0.75))); Tint(glow,
  //   (1, 1 - 0.7 u, 1 - 0.7 u, 1 - 0.5 u)); then mTrail unparented (SetParent(null)) with autodestruct, Destroy.
  // On the page: the weapon = api.hero().props.R (the built prop: it is drawn in the hero's mirrored rig, so the copy sits
  // under a scale (-1, 1, 1) group: its Unity numbers are the prop's; geometry copied (freed in dispose), materials
  // shared with the worn prop); its lossy scale = the prop's world scale in the effect's Unity world. The trail node is
  // moved to the mirror at the recall's end and the rest hidden; the effect goes once the trail's points have run out
  // (m_Time). APPROX: a skinned piece of the weapon is copied in its bind pose (Animator stripped: the game keeps its
  // copied bones' current pose); only meshes the page shows count (the game enables every renderer); the weapon's own
  // particle effects are not copied (weapon_fx.json follows the worn prop only)
  const copyTree = (src, geos) => {
    if (src.userData?.hoverOverlay || src.userData?.lookCopy) return null;
    let o;
    if (src.isMesh && src.geometry) {
      const g = src.geometry.clone(); geos.push(g);
      o = new THREE.Mesh(g, src.material); o.castShadow = src.castShadow; o.receiveShadow = src.receiveShadow; o.renderOrder = src.renderOrder;
    } else o = new THREE.Object3D();
    o.position.copy(src.position); o.quaternion.copy(src.quaternion); o.scale.copy(src.scale); o.visible = src.visible;
    for (const ch of src.children) { const k = copyTree(ch, geos); if (k) o.add(k); }
    return o;
  };
  // HoldWeapon on the page: the copy (cp) to put under the pivot, the tip's local y, or null
  const holdWeapon = (fx, prop, geos) => {
    const content = copyTree(prop, geos);
    if (!content) return null;
    content.position.set(0, 0, 0); content.quaternion.identity(); content.scale.set(1, 1, 1);   // local identity
    const cp = new THREE.Object3D(), W = new THREE.Group(); W.scale.set(-1, 1, 1); W.add(content); cp.add(W);
    cp.updateMatrixWorld(true);
    const box = new THREE.Box3(), corner = V();
    let any = false;
    content.traverse(o => {
      if (!o.isMesh) return;
      for (let p = o; p && p !== cp; p = p.parent) if (!p.visible) return;
      o.geometry.computeBoundingBox();
      const b = o.geometry.boundingBox;
      if (!b || b.isEmpty()) return;
      for (let k = 0; k < 8; k++) {
        corner.set(k & 1 ? b.max.x : b.min.x, k & 2 ? b.max.y : b.min.y, k & 4 ? b.max.z : b.min.z).applyMatrix4(o.matrixWorld);
        box.expandByPoint(corner); any = true;
      }
    });
    if (!any) return null;
    const cen = box.getCenter(V()), size = box.getSize(V());
    const ax = !(size.x < size.y || size.x < size.z) ? 0 : size.y < size.z ? 2 : 1;
    const comp = v => (ax === 0 ? v.x : ax === 1 ? v.y : v.z);
    const a = ax === 0 ? V(1, 0, 0) : ax === 1 ? V(0, 1, 0) : V(0, 0, 1);
    const lo = comp(cen) - comp(size) / 2, hi = comp(cen) + comp(size) / 2;
    let reach = hi;
    if (hi < -lo) { a.negate(); reach = -lo; }
    prop.updateWorldMatrix(true, false);
    const lossyX = V().setFromMatrixColumn(mirrorInv(fx).multiply(prop.matrixWorld), 0).length();
    const s = lossyX * 1.5, len = comp(size) * 0.2 * s;
    const rot = new THREE.Quaternion().setFromUnitVectors(a, DOWN);
    const p = cen.clone().multiplyScalar(s).applyQuaternion(rot);
    cp.quaternion.copy(rot); cp.scale.setScalar(s); cp.position.set(-p.x, s * reach - len, -p.z);
    content.traverse(o => o.layers.set(0));              // the hero's hidden / re-skinned layers are not the copy's
    return { cp, tip: -len };
  };
  api.part("Cat_eclipseFx", (fx, root, c, mat, nd, data) => {
    const at = fx.at || {}, mode = num(c.mode), moonSize = num(c.moonSize, 7);
    const nodesDef = data?.effects?.[fx.name]?.nodes || [];
    const mats = [], geos = [];
    let t = 0, ready = false;
    const M = r => { const mesh = meshOf(ref(fx, r)); return mesh ? ownMat(mesh, 0, mats, null) : null; };
    if (mode === 0) {
      // ---- the moon
      const top = root.position.clone(), shadowN = ref(fx, c.shadow), coronaN = ref(fx, c.corona);
      const coronaScale = Array.isArray(nodesDef[c.corona?.node]?.scale) ? V().fromArray(nodesDef[c.corona.node].scale) : V(1, 1, 1);
      let disc, glow, shadow, corona, eclipsed = false, run = null, set = null;
      root.position.copy(top).addScaledVector(UP, -2.5); root.scale.setScalar(moonSize * 0.6);   // Rise's first step
      const startSet = (T, time, red) => { set = { t0: T, time, red, from: root.position.clone() }; };
      return { node: root, update(dt) {
        if (!ready) {                                    // Awake (the renderers are built by now)
          ready = true;
          disc = M(c.disc); glow = M(c.glow); shadow = M(c.shadow); corona = M(c.corona);
          tint(disc, [1, 1, 1, 0]); tint(glow, [1, 1, 1, 0]); tint(corona, [1, 1, 1, 0]);
          shadowN?.position.set(-1.2, 0, -0.02); tint(shadow, [1, 1, 1, 0]);
        }
        t += dt;
        if (!eclipsed && typeof at.eclipse === "number" && t >= at.eclipse && !set) { eclipsed = true; run = { t0: t }; root.scale.setScalar(moonSize); }
        if (set) {
          const u = (t - set.t0) / set.time;
          if (u >= 1) return "destroy";
          const f = 1 - u;
          tint(disc, [1, set.red ? 0.55 : 1, set.red ? 0.5 : 1, f]); tint(shadow, [1, 1, 1, f]); tint(corona, [1, 1, 1, f]);
          tint(glow, set.red ? [1, 0.25, 0.2, 0.9 * f] : [0.75, 0.85, 1, 0.7 * f]);
          root.position.copy(set.from).addScaledVector(UP, 0.8 * u);
        } else if (run) {                                // EclipseRun
          const e = t - run.t0;
          if (e < 0.18) {
            const s = S(e / 0.18);
            shadowN?.position.set(1.2 * s - 1.2, 0, -0.02);
            tint(shadow, [1, 1, 1, s]); tint(corona, [1, 1, 1, s]); tint(glow, [1, 0.25, 0.2, 0.9 * s]); tint(disc, [1, 0.55, 0.5, 1]);
          } else if (e < 0.18 + 0.9) {
            if (shadowN) shadowN.position.set(0, 0, -0.02);
            const p = (e - 0.18) / 0.9;
            if (coronaN) { coronaN.scale.copy(coronaScale).multiplyScalar(1 + 0.18 * Math.sin(Math.PI * Math.min(1, 2.5 * p))); uEuler(0, 0, 32 * p, coronaN.quaternion); }
            tint(glow, [1, 0.25, 0.2, 0.65 + 0.25 * Math.exp(-5 * p)]);
          } else startSet(t, 0.7, true);
        } else if (t < 0.6) {                            // Rise
          const s = S(t / 0.6);
          root.position.copy(top).addScaledVector(UP, -2.5 * (1 - s));
          root.scale.setScalar(moonSize * (0.6 + 0.4 * s));
          tint(disc, [1, 1, 1, s]); tint(glow, [0.75, 0.85, 1, 0.7 * s]);
        } else if (t < 6) {
          root.position.copy(top); root.scale.setScalar(moonSize);
          tint(disc, [1, 1, 1, 1]);
          tint(glow, [0.75, 0.85, 1, 0.7 * (0.85 + 0.15 * Math.sin(5 * t))]);
        } else startSet(t, 0.5, false);
        root.quaternion.copy(lookRot(root.position.clone().sub(camPos(fx))));   // LateUpdate
      }, dispose() { for (const m of mats) m.dispose(); mats.length = 0; } };
    }
    // ---- the blade (mode 1)
    const pivot = ref(fx, c.pivot), glowN = ref(fx, c.glow), biteN = ref(fx, c.bite);
    const kids = pivot ? nodesDef.map((n, j) => (n.parent === c.pivot.node ? j : -1)).filter(j => j >= 0) : [];
    const modelN = fx.nodes[kids.find(j => nodesDef[j].name === "Model")] || null;   // pivot.Find("Model") (names: the data's, the nodes are named later)
    const trailJ = nodesDef.findIndex((n, j) => n.comps?.some(x => x.type === "TrailRendererModern") && (() => {
      for (let p = n.parent; p >= 0; p = nodesDef[p]?.parent ?? -1) if (p === c.pivot?.node) return true;
      return false;
    })());
    const trailN = trailJ >= 0 ? fx.nodes[trailJ] : null;
    const trailLife = num(nodesDef[trailJ]?.comps?.find(x => x.type === "TrailRendererModern")?.m_Time, 0.2);
    const from = root.position.clone(), to = vec(at.to) || from.clone(), centre = vec(at.centre) || V(0, 0, 0);
    const home = vec(at.home) || V(0, 1, 0), recallAt = typeof at.recall === "number" ? at.recall : null;
    const flight = 0.22;
    let glow = null, held = false, phase = "fling", landedAt = 0, rc = null, endAt = 0;
    const dir = to.clone().sub(from); if (dir.length() > 1e-5) dir.normalize(); else dir.set(0, 0, 0);
    const flying = lookRot(dir), side = V().crossVectors(UP, dir); if (side.length() > 1e-5) side.normalize(); else side.set(0, 0, 0);
    let planted = null;
    const flingPose = u => {
      const k = S((u - 0.72) / 0.28);
      root.position.copy(from).lerp(to, clamp01(u * u)).addScaledVector(side, 0.65 * Math.sin(Math.PI * u)).addScaledVector(UP, 0.8 * Math.sin(Math.PI * u));
      root.quaternion.copy(slerp(flying, planted, k));
      if (pivot) axisAngle(RIGHT, -1080 * (1 - k) * u, pivot.quaternion);
    };
    const init = () => {
      ready = true;
      glow = glowN ? M(c.glow) : null;
      tint(glow, [1, 1, 1, 0.6]);                        // Awake
      const prop = api.hero?.()?.props?.R;               // HoldWeapon(the worn main-hand weapon)
      if (pivot && prop?.parent) {
        try {
          const h = holdWeapon(fx, prop, geos);
          if (h) {
            pivot.add(h.cp);
            if (modelN) modelN.visible = false;
            if (glowN) glowN.visible = false;
            glow = null;
            if (trailN) trailN.position.set(0, h.tip, 0);
            held = true;
          }
        } catch (e) { console.warn("Cat_eclipseFx: HoldWeapon", e); }
      }
      const out = centre.clone().sub(to); out.y = 0;     // FlingRun's planted
      if (out.lengthSq() < 1e-4) out.copy(FWD);
      planted = lookRot(out).multiply(uEuler(held ? 30 : -25, 0, 0));
    };
    return { node: root, update(dt) {
      if (!ready) init();
      t += dt;
      if (phase !== "recall" && phase !== "gone" && recallAt != null && t >= recallAt) {   // Recall(home, 0.14)
        phase = "recall";
        if (pivot) pivot.quaternion.identity();
        const rf = root.position.clone(), d = home.clone().sub(rf);
        rc = { t0: t, from: rf, q0: root.quaternion.clone(), s0: root.scale.clone(),
          inbound: d.lengthSq() <= 1e-4 ? root.quaternion.clone() : lookRot(d).multiply(uEuler(-90, 0, 0)) };
      }
      if (phase === "fling") {
        if (t < flight) { flingPose(t / flight); return; }
        phase = "planted"; landedAt = flight;
        root.position.copy(to); root.quaternion.copy(planted);
        if (pivot) pivot.quaternion.identity();
        psOf(fx, biteN)?.play();
        play(fx, root, c.landSound, 0.7);
        tint(glow, [1, 1, 1, 1]);
      }
      if (phase === "planted") {
        const q = t - landedAt;
        if (pivot) uEuler(14 * Math.sin(38 * q) * Math.exp(-14 * q), 0, 0, pivot.quaternion);
        tint(glow, [0.82, 0.7, 1, 0.65 + 0.2 * Math.sin(12 * q)]);
      } else if (phase === "recall") {
        const u = (t - rc.t0) / 0.14;
        if (u < 1) {
          root.position.copy(rc.from).lerp(home, clamp01(u * u)).addScaledVector(UP, 0.6 * Math.sin(Math.PI * u));
          root.quaternion.copy(slerp(rc.q0, rc.inbound, Math.min(1, 3 * u)));
          root.scale.copy(rc.s0).multiplyScalar(1 - 0.6 * clamp01((u - 0.75) * 4));
          tint(glow, [1, 1 - 0.7 * u, 1 - 0.7 * u, 1 - 0.5 * u]);
          return;
        }
        // the trail unparented (autodestruct), Destroy(blade): the rest hidden, the effect kept until the trail runs out
        phase = "gone"; endAt = t + trailLife + 0.02;
        if (trailN && trailN.parent) fx.mirror.attach(trailN);
        for (const ch of root.children) ch.visible = false;
        if (!trailN) return "destroy";
      }
      if (phase === "gone" && t >= endAt) return "destroy";
    }, dispose() { for (const m of mats) m.dispose(); for (const g of geos) g.dispose(); mats.length = geos.length = 0; } };
  });

  // ---------------------------------------------------------------- Cat.RoyalSwordFall (tto P3, CODE_MOVERS)
  // TTO1102:Cat.<RoyalSwordFall>d__308::MoveNext@0x1BF4840 (Cat.c:26104-26412; RoyalFlushBursts spawns royalFlush_sword
  // at centre + 5 up, LookRotation(face), :25981, and starts it with (sword, rot, point = the spawn, centre)): while e <
  // 0.8: s = S(e / 0.35): localScale = 0.15 + 0.85 s, rotation = rot x AngleAxis(360 (1 - s), up); e < 0.68: position =
  // point + up 1.2 S((e - 0.35) / 0.33); else lerp(point + 1.2 up, centre - 1.1 up, clamp01(((e - 0.68) / 0.12)^2)). Then
  // position centre - 1.1 up, rotation rot, Waits.Get(0.6); then 0.5 s, k = 2 (now - s0): position = centre - up (2.5 k^2
  // + 1.1), localScale = 1 - 0.4 k; then Destroy (2.75 + 1.9 = 4.65 in the skill, tto.md 2.1).
  // On the page: point / rot = where the cue put the sword, centre = the cue's `to` (the target 10 m ahead)
  api.part("Cat.RoyalSwordFall", (fx, root) => {
    const point = root.position.clone(), rot = root.quaternion.clone();
    const centre = vec(fx.at?.to) || point.clone().addScaledVector(UP, -5);
    if (!vec(fx.at?.to)) console.warn("Cat.RoyalSwordFall: no cue `to` (the centre): 5 m below the spawn", fx.name);
    const low = centre.clone().addScaledVector(UP, -1.1), high = point.clone().addScaledVector(UP, 1.2);
    let t = 0;
    const place = () => {
      if (t < 0.8) {
        const s = S(t / 0.35);
        root.scale.setScalar(0.15 + 0.85 * s);
        root.quaternion.copy(rot).multiply(axisAngle(UP, 360 * (1 - s)));
        if (t < 0.68) root.position.copy(point).addScaledVector(UP, 1.2 * S((t - 0.35) / 0.33));
        else root.position.copy(high).lerp(low, clamp01(((t - 0.68) / 0.12) ** 2));
      } else if (t < 1.4) {
        root.position.copy(low); root.quaternion.copy(rot);
      } else if (t < 1.9) {
        const k = 2 * (t - 1.4);
        root.position.copy(centre).addScaledVector(UP, -(2.5 * k * k + 1.1));
        root.scale.setScalar(1 - 0.4 * k);
      } else return "destroy";
    };
    place();
    return { node: root, update(dt) { t += dt; return place(); } };
  });

  // ---------------------------------------------------------------- Cat.DropAnchorFlight (tto P5, CODE_MOVERS)
  // TTO1102:Cat.<DropAnchorFlightAndLand>d__389::MoveNext@0x1B9D6C0 (Cat.c:138-384; RPC_dropAnchor spawns the anchor at
  // hero + 0.4 face + 1.6 up, LookRotation(face), :7246-7273): upright = LookRotation(face, up); while u = e / 0.35 < 1:
  // position = lerp(from, spot, clamp01(u)) + up 12 u (1 - u) (a 3 m arc), rotation = upright x AngleAxis(360 u, right)
  // (one flip); then position spot, rotation upright, transform.Find("Leash").SetActive(true) (:251-260), the slam
  // (a cue) and AnchorHold; ClearAnchor destroys it (the cue's kill).
  // The Leash (node 2, m_IsActive false in the prefab) holds the Edge and Pull RingEmitters (nodes 3, 4), which the page
  // builds and runs from the spawn (tto.md Verification 3: ringEmitter never reads `active`): held back here, taken out
  // of fx.emitters at the first update (they are built after this root component, and run after it in the frame) and
  // node 2 hidden; at the landing node 2 shown and the emitters put back, their clocks unrun (SetActive(true) starts
  // them then). Any emitter under an inactive node of the anchor is held the same way.
  // On the page: from / upright = where the cue put the anchor, spot = the cue's `to`
  api.part("Cat.DropAnchorFlight", (fx, root, c, mat, nd, data) => {
    const from = root.position.clone(), upright = root.quaternion.clone(), spot = vec(fx.at?.to);
    if (!spot) console.warn("Cat.DropAnchorFlight: no cue `to` (the spot): it stays where it was spawned", fx.name);
    const nodesDef = data?.effects?.[fx.name]?.nodes || [];
    const off = nodesDef.map((n, j) => (n.active === false ? j : -1)).filter(j => j > 0).map(j => fx.nodes[j]).filter(Boolean);
    for (const o of off) o.visible = false;
    const under = o => { for (let p = o; p && p !== fx.mirror; p = p.parent) if (off.includes(p)) return true; return false; };
    let t = 0, held = null, landed = !spot;
    if (spot) { root.position.copy(from); root.quaternion.copy(upright); }
    return { node: root, update(dt) {
      if (!held) {
        held = fx.emitters.filter(e => e.node && e.node !== root && under(e.node));
        for (const e of held) fx.emitters.splice(fx.emitters.indexOf(e), 1);
        if (landed) { for (const o of off) o.visible = true; fx.emitters.push(...held); }
      }
      if (landed) return;
      t += dt;
      const u = t / 0.35;
      if (u < 1) {
        root.position.copy(from).lerp(spot, clamp01(u)).addScaledVector(UP, 12 * u * (1 - u));
        root.quaternion.copy(upright).multiply(axisAngle(RIGHT, 360 * u));
        return;
      }
      landed = true;
      root.position.copy(spot); root.quaternion.copy(upright);
      for (const o of off) o.visible = true;
      fx.emitters.push(...held);
    } };
  });
}
