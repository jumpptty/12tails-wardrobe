// wardrobe/fxparts/bison.js: the Bison's own effect scripts (agent bison_parts, 2026-11-13; plans/fx_bison/parts.md
// parts 3 and 4, decision 39 in plans/fx_bison/decisions.md; the loader comment above FX_PART_FILES in index.html).
// BB's DecompiledSource is the authority for every line cited here.
//   Bison_earthRupture  Earth Rupture's travelling rock (earthRupture): the mover of its root
//   Bison_overLord      Over Lord's ally aura (overLord): draws nothing
// ProjectileControl (ProjectileControl.cs:21-87) has no Update: it is data only, read below.

export default function register(api) {
  const { vA } = api;

  // ---- Bison_earthRupture (0 serialized bytes; on the prefab's root with its ProjectileControl and the Rigidbody,
  // checks/fx_bison_research/parts/probe.txt "earthRupture" [0]; the root's parent is the mirror group, so node.position
  // is the Unity world position).
  // Awake (Bison_earthRupture.cs:20-84): its own ProjectileControl (:31), no collisions with other projectiles (:34-66).
  // FixedUpdate (:96-127): clock += Time.deltaTime (:103); clock >= ProjectileControl.life: Destroy(gameObject)
  //   (:106-110), which takes the root's children with it (the three skinned teeth, the dust and smoke emitters); else
  //   rigidbody.velocity = transform.TransformDirection(ProjectileControl.velocity) (:119) every step. The Rigidbody's
  //   rotation is frozen (m_Constraints 112) and it has no gravity, so the velocity is the spawn rotation's, constant:
  //   the prefab's (0, 0, 12) along the root's facing, level (the hero's fire point is 0.2 m up, Bison.cs:28634).
  // OnCollisionEnter (:131-198): a Player / Enemy collider is ignored from then on (:156) and hit (:186), with no
  //   Destroy: the rupture pierces every foe, so no target end here; no floor end either (it travels level; the game's
  //   walls stop it physically, and the page has none).
  // The life is the hero's code's, not the prefab's 0: projectileControl.life = 2 (Bison.cs:8797 in
  //   RPC_earthRupture_fire1, :8892 in RPC_earthRupture_fire2, the max rank's three ruptures at Euler(0, 25 i, 0),
  //   :8877): 2 s, 24 m.
  const RUPTURE_LIFE = 2, RUPTURE_V = [0, 0, 12];
  api.part("Bison_earthRupture", (fx, node, c, mat, nd) => {
    const v = nd?.comps?.find(x => x.type === "ProjectileControl")?.velocity || RUPTURE_V;
    // TransformDirection at the spawn: the cue's rot is already on the root (index.html Fx constructor), as sheep.js
    const vel = vA(v).applyQuaternion(fx.uQuat(node));
    let t = 0;
    return { node, update(dt) {
      t += dt;
      if (t >= RUPTURE_LIFE) return "destroy";
      node.position.addScaledVector(vel, dt);
    } };
  });

  // ---- Bison_overLord (0 serialized bytes): Init(nLv, ownerID) (Bison_overLord.cs:21-50) finds the owner; OnTriggerEnter
  // / Exit (:56-123, :126-190) give or take an ally the overLord status (:110, :173) inside its 10 m trigger sphere. It
  // draws nothing and moves nothing (parts.md part 4): registered so a spawn of it builds without a warning.
  api.part("Bison_overLord", () => null);
}
