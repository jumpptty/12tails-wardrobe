// wardrobe/fxparts/sheep.js: the Sheep's own effect scripts (agent sheep_parts, 2026-11-10; plans/fx_sheep/parts.md
// "ProjectileControl + Sheep_nAttack / Sheep_homingLight / Sheep_cAttack" and "Sheep_edenSanctuary"; the loader comment
// above FX_PART_FILES in index.html). BB's DecompiledSource is the authority for every line cited here.
//   Sheep_nAttack / Sheep_homingLight / Sheep_cAttack  the three projectile movers (nAttack, homingLight, cAttack)
//   Sheep_edenSanctuary                                 Eden Sanctuary's clip switch and end (edenSanctuary)
// ProjectileControl (ProjectileControl.cs:21-87) has no Update: it is data only, read below; Sheep_seal draws nothing
// (parts.md "Sheep_seal"): neither needs a part (an unknown type is skipped).

export default function register(api) {
  const { vA } = api;

  // ---- the projectile movers. All three do the same (parts.md, checked against the sources):
  // Awake: rigidbody.velocity = transform.TransformDirection(v), taken once at the spawn, with
  //   Sheep_nAttack      v = ProjectileControl.velocity (Sheep_nAttack.cs:51; the prefab's (0, 0, 12))
  //   Sheep_homingLight  v = its own (0, 0, 12) (Sheep_homingLight.cs:26, :51)
  //   Sheep_cAttack      v = its own (0, 0, 8) (Sheep_cAttack.cs:28, :57)
  // The Rigidbody has no gravity, drag 0 and frozen rotation (m_Constraints 112), so the speed is constant.
  // FixedUpdate: Destroy(gameObject) once its clock reaches ProjectileControl.life (Sheep_nAttack.cs:73-79,
  // Sheep_homingLight.cs:77-86, Sheep_cAttack.cs:112-121). That life is the HERO's code's, not the prefab's 0 / 0 / 10:
  // 1.7 x rangeMod for nAttack (Sheep.cs:9343) and homingLight (:11472), 5 x rangeMod for cAttack (:9838); rangeMod = 1
  // (CharacterControl.cs:154). So 1.7 s (20.4 m), 1.7 s (20.4 m), 5 s (40 m) if nothing is met.
  // Homing (every 0.1 s RotateTowards the target by 0.15 rad, Sheep_homingLight.cs:92-113; 0.1 rad, Sheep_cAttack.cs:
  // 127-148) runs only with a target GameObject (InitTarget / Init(tObject), Sheep.cs:11500-11511, :9869-9872): the
  // page has none, so the ball flies straight, as the game's untargeted shot does.
  // The end on the ground (decision 3, plans/fx_sheep/decisions.md): OnTriggerEnter destroys the ball on any collider
  // that is not on the owner's layer or layer 1 / 2 (Sheep_nAttack.cs:223-241, Sheep_homingLight.cs:261-279,
  // Sheep_cAttack.cs:223-238, :388), and the Destroy takes its legacy particles with it (the ParticleRenderer is on the
  // ball), tail included: here the whole effect goes in that frame. The hit effect it then asks for (RPC_nAttack_hit at
  // the contact point, Sheep_homingLight.cs:302, Sheep_nAttack.cs:264; RPC_cAttack_hit / RPC_whiteBurst_hit,
  // Sheep_cAttack.cs:274, :294) is a separate effect: the cue's, not this part's.
  // APPROXIMATED: the game's trigger fires when the 0.3 m (cAttack 0.5 m) SphereCollider first overlaps a collider, and
  // which one depends on what stands there. The user's rule is "where it meets the ground at the 10 m target point", the
  // point the shot is aimed at (the cue's pitch: parts.md "Cue options", 5.89 degrees down from 1 m up and 0.3 m ahead),
  // so the ball ends when its CENTRE reaches the floor (y 0, the hero's feet; the mirror group's space = Unity's world):
  // 9.75 m / 12 = 0.81 s for homingLight / nAttack. A level shot (no pitch) never meets the floor and lives its full life.
  // These scripts sit on the prefab's root in all three (the Rigidbody's node, checks/fx_sheep_research/parts/probe.txt
  // lines 2-11, 13-22, 29-38), whose parent is the mirror group, so node.position is the Unity world position.
  const LIFE = { Sheep_nAttack: 1.7, Sheep_homingLight: 1.7, Sheep_cAttack: 5 };
  const OWN_V = { Sheep_homingLight: [0, 0, 12], Sheep_cAttack: [0, 0, 8] };
  // Sheep_cAttack.Init(tObject, cDmg), called in the spawn frame (Sheep.cs:9872), before any particle is emitted: the
  // ball's own emitter (this.particleEmitter, the root's) gets minSize and maxSize + clamp(0.004 x cDmg, 0, 2.5)
  // (Sheep_cAttack.cs:76, :79); the child sparks are untouched. Decision 8 (BB's max: Charge Attack 4, full charge):
  //   cDmg = clamp((1 + 0.2 x Benediction) x n x ATK, ATK, 100 x Lv) (Sheep.cs:9787-9810; Over Limit #462 never on BB)
  //   n = floor(4.8 + 0.5 - 1.3) = 4 on the tile's hold, so 4 x ATK >= 400 for any ATK >= 100: cDmg = 400
  //   0.004 x 400 = 1.6 m (the glow goes from 0.3-0.5 to 1.9-2.1 m)
  const CHARGE_GROWTH = 1.6;

  const mover = (fx, node, c, mat, nd) => {
    const v = OWN_V[c.type] || nd.comps.find(x => x.type === "ProjectileControl")?.velocity;
    if (!v) { console.warn("effect part", c.type, "has no ProjectileControl velocity (LAYOUTS in wardrobe_fx.py)", fx.name); return null; }
    // TransformDirection at the spawn: the cue's rot is already on the root (index.html Fx constructor)
    const vel = vA(v).applyQuaternion(fx.uQuat(node));
    if (c.type === "Sheep_cAttack") {
      // legacyParticles is built for this node before its scripts (index.html: the emitter first, then the comps),
      // so the root's emitter is already in fx.emitters here, and has not emitted yet
      const glow = fx.emitters.find(e => e.node === node && e.addSize);
      if (glow) glow.addSize(CHARGE_GROWTH);
      else console.warn("effect part Sheep_cAttack: the particle emitter has no addSize(metres) (index.html legacyParticles)");
    }
    const life = LIFE[c.type];
    let t = 0;
    return { node, update(dt) {
      t += dt;
      if (t >= life) return "destroy";
      node.position.addScaledVector(vel, dt);
      if (vel.y < 0 && node.position.y <= 0) return "destroy";   // met the floor (decision 3, above)
    } };
  };
  for (const type of Object.keys(LIFE)) api.part(type, mover);

  // ---- Sheep_edenSanctuary (0 serialized bytes). InitEdenSanctuary, by SendMessage in the spawn frame (Sheep.cs:37142):
  // animation.Play("create") (Sheep_edenSanctuary.cs:64), wrapMode Once (:67), the end at now + 12 s (:73). The
  // Animation part (mesh.js) already plays the default clip "create" from the spawn (m_PlayAutomatically), the same frame.
  // Update: once end < Time.time (strict, :129), DestroySanctuary (:135): CrossFade("destroy", 0.2) (:409), wrapMode
  // Once (:412), WaitForSeconds(1) (:423), then Destroy(gameObject) (:372): the effect goes about 13 s in, its
  // repeatForever rings and vortex with it. The heal ticks (owner only, every 2 s, 18 m: :144-205) draw nothing.
  // The cross-fade is mesh.js's play(name, 0.2) (its approximation: the outgoing pose held); the two poses it joins are
  // equal (create ends at y 0, destroy starts at y 0: checks/fx_sheep_research/parts/probe4.txt), so it is the game's.
  api.part("Sheep_edenSanctuary", (fx, node) => {
    let t = 0, endAt = null;
    return { node, update(dt) {
      t += dt;
      if (endAt == null && t > 12) {
        endAt = t + 1;
        const anim = node.userData.fxAnim;
        if (anim?.play) anim.play("destroy", 0.2);   // CrossFade("destroy", 0.2), Sheep_edenSanctuary.cs:409
        else console.warn("effect part Sheep_edenSanctuary: no Animation play(name) on its node (fxparts/mesh.js)", fx.name);
      }
      if (endAt != null && t >= endAt) return "destroy";
    } };
  });

  // ---- the hero's own code acting on a spawned effect ("fx:<effect>" parts, index.html's Fx constructor; 2026-11-10, the
  // editor: plans/fx_sheep/attacks_emotes.md question 4, own_skills.md holyLight3)

  // The held charge ball (cAttack_charge, made 2.7 m up 0.8 s into cAttack1, Sheep.cs:18698-18710): every 0.1 s while
  // the charge holds (Yield(3, 0.1) :18972) RPC_cAttack1 rewrites its own particleEmitter's sizes (:18952, :18957), with
  // t = Time.time - actionTime (cAttack1's start), L the Charge Attack rank, B Benediction's, O = hasSkill(462) (never on
  // BB, so 0):
  //   minSize = Clamp((t - 0.7) x k, 0, 0.4 (L + 0.2 L O) - 0.3)     maxSize = Clamp((t - 0.4) x k, 0.3, 0.4 (L + 0.2 L O))
  //   k = ATK x 0.25 x (0.01 + 0.0015 B)
  // At BB's max (decision 8: Charge Attack 4, Benediction 3): k = 0.003625 x ATK, full size 1.3-1.6 m. APPROXIMATED: the
  // page has no ATK; it takes ATK 101, the least that fills the ball by the tile's release at t = 0.8 + 4 = 4.8 s
  // ((4.8 - 0.4) x 0.003625 x 101 = 1.61 >= 1.6), so the release shows the full charge. The first write is made in the
  // spawn frame (the coroutine's next pass, under 0.1 s off); particles keep the size they were born with, as Unity's.
  const CHARGE_K = 0.25 * (0.01 + 0.0015 * 3) * 101, CHARGE_TOP = 0.4 * 4;
  api.part("fx:cAttack_charge", (fx, node) => {
    if (fx.cls !== "sheep") return null;   // the hook is keyed by effect name only: the Rabbit's star burst is not resized (plans/fx_rabbit/parts.md part 8)
    const ball = fx.emitters.find(e => e.node === node && e.setSize);
    if (!ball) { console.warn("effect part fx:cAttack_charge: the ball's particle emitter has no setSize (index.html legacyParticles)"); return null; }
    const cl = (x, a, b) => Math.min(b, Math.max(a, x));
    let t = 0.8, wait = 0;
    const write = () => ball.setSize(cl((t - 0.7) * CHARGE_K, 0, CHARGE_TOP - 0.3), cl((t - 0.4) * CHARGE_K, 0.3, CHARGE_TOP));
    write();
    return { node, update(dt) { t += dt; if ((wait += dt) >= 0.1) { wait -= 0.1; write(); } } };
  });

  // World Encarta's status look (worldEncarta, 2026-11-10 QA: the prefab is only an Animation turning worldEncarta_ctrl
  // and eight empty nodes, so it drew nothing). The status apply fills them (CharacterControl.cs:39886-39975): Instantiate
  // worldEncarta at the target's collider centre in its rotation, parented to it; then, with the CASTER's mWep1 (her
  // equipped weapon: SheepEquipment.cs:1100-1192 sets mWep1 to the weapon it instantiates, null with none), for node =
  // 1..8: a copy of mWep1 parented to worldEncarta_ctrl/node<k>, localPosition 0, localRotation Euler(0, 0, 90),
  // localScale 1.5. The page's mWep1 is the worn main weapon (อาวุธหลัก, hero().props.R); with none worn the game draws
  // nothing either. The copy is the weapon model as it hangs in the prop (its root's own transform replaced, as Unity's
  // assignments replace it), wrapped back from three's space into the effect's Unity space (the page's models are
  // Unity's mirrored in x, wardrobe_data.py). APPROXIMATED: an animated weapon's own clip is not played on the copies.
  api.part("fx:worldEncarta", (fx) => {
    const wep = api.hero()?.props?.R;
    if (!wep) return null;
    const { THREE } = api, geos = new Map();
    // the prop's nodes and meshes (not Object3D.clone: the prop's userData links back to itself); own geometry copies,
    // since Fx.dispose frees its meshes' geometry and the worn weapon keeps its own; a skinned piece stays in its bind pose
    const copy = (o, root) => {
      const g = o.geometry && (geos.get(o.geometry) || geos.set(o.geometry, o.geometry.clone()).get(o.geometry));
      const c = g ? new THREE.Mesh(g, o.material) : new THREE.Object3D();
      if (!root) { c.position.copy(o.position); c.quaternion.copy(o.quaternion); c.scale.copy(o.scale); }
      c.visible = o.visible;
      for (const ch of o.children) c.add(copy(ch, false));
      return c;
    };
    for (let k = 1; k <= 8; k++) {
      const node = fx.nodes.find(o => o.name === "node" + k && o.parent?.name === "worldEncarta_ctrl");
      if (!node) { console.warn("effect part fx:worldEncarta: no worldEncarta_ctrl/node" + k, fx.name); continue; }
      const t = new THREE.Group(), m = new THREE.Group();
      t.quaternion.setFromEuler(new THREE.Euler(0, 0, Math.PI / 2, "YXZ")); t.scale.setScalar(1.5);   // Unity's Euler(0, 0, 90), 1.5
      m.scale.set(-1, 1, 1);                     // three's model space -> the effect's Unity space
      m.add(copy(wep, true)); t.add(m); node.add(t);
    }
    return null;
  });

  // Holy Light's ring (holylight_ring, made at holyLight3's start, Sheep.cs:28100-28112): 0.1 s into holyLight4 (Yield(5,
  // 0.1) :28410), which starts 0.4 s after it (Yield(4, 0.4) :28400), the code restarts its Animation on the "root" clip
  // (mHolyLightRing.animation.Play("root"), :27700): 0.4 + 0.1 = 0.5 s after the spawn. The game's per-step clock is the
  // page's effect age here (the steps run back to back)
  api.part("fx:holylight_ring", (fx, node) => {
    let t = 0;
    return { node, update(dt) {
      if (t >= 0.5 || (t += dt) < 0.5) return;
      if (!node.userData.fxAnim?.play("root")) console.warn("effect part fx:holylight_ring: no root clip on its Animation (fxparts/mesh.js)", fx.name);
    } };
  });
}
