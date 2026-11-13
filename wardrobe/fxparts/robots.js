// wardrobe/fxparts/robots.js: the Mole's robot summons (agent robots, 2026-11-13; plans/fx_mole/decisions.md 32-37,
// parts.md part 11 and "Summons", skills_a.md part 3; the loader comment above FX_PART_FILES in index.html). The robots
// are whole characters from Resources/GameAssets/Characters/Robots/ (wardrobe_fx.py EXTRA_FOLDERS["mole"]), each cued as
// an effect (AutoGyroGun4, BarrelBot4, KingKaiser_<r g b k w>) and cut at 10 s by the cue's kill. These parts are their
// scripts, on the prefab root beside its Animation (fxparts/mesh.js) and CharacterControl (NOT_DRAWN). Lines are
// D:\12tails\DecompiledSource\<file> (opaque predicates worked by hand); the TTO clip is TTO1102: (plans/fx_mole/tto.md 2.3).
//   AutoGyroGun  AutoGyroGun1-4: create (AutoGyroGun.cs:1651-1741: Play("create") and PlayOneShot(create_fx), 0.8 s
//                later Play("root") + Loop and the AI on), the AI (:733-990: in standby, from 2 s after Awake (:58), a
//                target within 8 + 4 mLv m (findAttackTarget :991-1031) and the 2 s "nAttack" lock clear: RPC_fire),
//                RPC_fire (:1159-1477: the 2 s lock, leg1 turned to FromToRotation(right, vFlat(tDir)) with its local
//                euler z - 90, CrossFade("fire") + Loop, PlayOneShot(nAttack_fx), autoGyroGun_fire at the turret +
//                TransformDirection(0, 0.7 / 0.8 / 1 / 1.2 by mLv, 0.5), FromToRotation(forward, vFlat(tDir)); 0.7 s later
//                CrossFade("root") + Loop, standby): shots at 2, 4, 6, 8 s. tDir is the target's bounds centre: the cue's
//                `to` (decision 32: the 10 m target, 0.6 m up). The hits (mChar.hit) draw nothing; Hidden Turret's hide
//                (:832-861) never comes while it has a target
//   BarrelBot    BarrelBot1-4: create (BarrelBot.cs:5940-6103: PlayOneShot(create_fx), Play("getUp") + Once, 0.8 s later
//                standby), then standing: the standby branch's CrossFade("root", 0.2) + Loop (:535-540). No AI (decision 32)
//   KingKaiser   KingKaiser_<colour>: summon (KingKaiser.cs:3821-4048: Play("create") + Once and PlayOneShot(kaiser_createFx),
//                3 s later standby), then the standby branch's CrossFade("root", 0.3) + Loop (:404-409). The colour is the
//                cue's pick ("pick": "color", index.html). Cue option "clip": a clip the Kaiser plays instead, standing
//                already (decision 37: "kaiserArsenal": TTO1102:KingKaiser.<RPC_kaiserArsenal>d__72, KingKaiser.c:308-329
//                CrossFade(arsenal, 0.2) + Once; standby at the clip's end, 4.4 s, :427-474: root as above). It is the host
//                of the cue option "host": "KingKaiser" (decision 37: the pods on its Arm_R / Arm_L): fx.host, fx.hostBone,
//                fx.hostSkin below
// Space: the root hangs in the effect's mirror group (Unity's world, the hero's feet at the origin, +z her facing), so
// node.position is the game's transform.position. Every clip switch looks the Animation up when it is due (the Bat's
// gotcha: mesh.js may be built after this script on another prefab).
// Sounds (the scripts' PlayOneShot of an AudioClip field; the rip's Assets/AudioClip, outside Resources): played as
// data/mole/sfx/<name>.mp3 under the names in SFX, each a Sound handle in fx.sounds (Fx.dispose stops it, as Destroy).

export default function register(api) {
  const { THREE, V } = api;
  const ONCE = 1, LOOP = 2, FADE = 0.3;                // UnityEngine.WrapMode; Animation.CrossFade's default fadeLength
  const SFX = { gunCreate: "autoGyroGun_create", gunFire: "autoGyroGun_nAttack", botCreate: "barrelBot_create",
                kaiserCreate: "kingKaiser_kaiser_create" };   // fallbacks: the comps' AudioClip fields hold the exported names (wardrobe_fx.py SOUND_REFS)
  const FIRE_FX = "autoGyroGun_fire";                  // AutoGyroGun's prefab field autoGyroGun_fire (decision 54)
  const TARGET = [0, 0.6, 10];                         // the target body's centre (Bat decision 4), when the cue has no `to`
  const warned = new Set();
  const warnOnce = (k, ...m) => { if (!warned.has(k)) { warned.add(k); console.warn(...m); } };
  // Animation.Play / CrossFade + wrapMode (mesh.js play(name, fade, wrap))
  const anim = (fx, node, name, fade, wrap) => {
    const a = node.userData.fxAnim;
    if (!a?.play) return warnOnce("anim:" + fx.name, "effect part (robots.js): no Animation play() on", fx.name, "(fxparts/mesh.js)");
    if (!a.play(name, fade, wrap)) warnOnce("clip:" + fx.name + name, "effect part (robots.js): no clip", name, "on", fx.name);
  };
  const sound = (fx, n) => fx.sounds.push({ node: fx.root, comp: null, h: api.Sound.play(fx.cls, n) });
  // [seconds after the spawn, fn] run in order on the effect's clock (the first update is the spawn frame)
  const run = (node, ev) => {
    let t = 0, i = 0;
    ev.sort((a, b) => a[0] - b[0]);
    return { node, update(dt) { t += dt; while (i < ev.length && t >= ev[i][0]) ev[i++][1](); } };
  };

  // ---- AutoGyroGun
  const RZ = new THREE.Quaternion().setFromAxisAngle(V(0, 0, 1), -Math.PI / 2);   // localEulerAngles.z - 90 = local x Euler(0, 0, -90)
  const HEIGHT = { 1: 0.7, 2: 0.8, 3: 1, 4: 1.2 };     // RPC_fire's TransformDirection(0, h, 0.5) by mLv
  api.part("AutoGyroGun", (fx, node, c) => {
    const lv = c.mLv || 4, to = Array.isArray(fx.at?.to) ? fx.at.to : TARGET;
    const fire = () => {
      const p = node.position, d = V(to[0] - p.x, 0, to[2] - p.z);   // vFlat(tDir)
      if (d.length() > 8 + 4 * lv || d.lengthSq() < 1e-10) return;  // Hate.findEnemies' reach: no target, no shot
      d.normalize();
      const leg1 = fx.nodes.find(o => o.name === "leg1");           // Awake: transform.Find("AutoGyroGun_tri/base/leg1")
      if (leg1) leg1.quaternion.copy(fx.uQuat(leg1.parent).invert().multiply(new THREE.Quaternion().setFromUnitVectors(V(1, 0, 0), d))).multiply(RZ);
      anim(fx, node, "fire", FADE, LOOP);
      sound(fx, c.nAttack_fx || SFX.gunFire);
      const f = V(0, HEIGHT[lv] ?? 1.2, 0.5).applyQuaternion(fx.uQuat(node)).add(p);
      api.spawn(FIRE_FX, { x: f.x, y: f.y, d: f.z, rot: [0, Math.atan2(d.x, d.z) * 180 / Math.PI, 0] });   // FromToRotation(forward, d)
    };
    const ev = [[0, () => { anim(fx, node, "create", 0, ONCE); sound(fx, c.create_fx || SFX.gunCreate); }],
                [0.8, () => anim(fx, node, "root", 0, LOOP)]];
    // ponytail: the shots are scheduled up to the summon's chaAdjust(120) life; the cue's kill (10 s) ends them first
    for (let s = 2; s < 120; s += 2) ev.push([s, fire], [s + 0.7, () => anim(fx, node, "root", FADE, LOOP)]);
    return run(node, ev);
  });

  // ---- BarrelBot
  api.part("BarrelBot", (fx, node, c) => run(node, [
    [0, () => { sound(fx, c.create_fx || SFX.botCreate); anim(fx, node, "getUp", 0, ONCE); }],
    [0.8, () => anim(fx, node, "root", 0.2, LOOP)]]));

  // ---- KingKaiser
  api.part("KingKaiser", (fx, node, c, mat, nd) => {
    // the host of a cue's "host": "KingKaiser" (index.html): its bones by name, and its skinned material (the pods' Wear)
    fx.host = "KingKaiser";
    fx.hostBone = name => fx.nodes.find(o => o.name === name) || null;
    fx.hostSkin = () => {
      let m = null;
      node.traverse(o => { if (!m && o.isSkinnedMesh) m = [].concat(o.material)[0]; });
      return m;
    };
    const clip = fx.at?.clip;
    if (clip) {
      const len = nd.comps.find(x => x.type === "Animation")?.clips?.[clip]?.len || 4.4;
      return run(node, [[0, () => anim(fx, node, clip, 0.2, ONCE)], [len, () => anim(fx, node, "root", FADE, LOOP)]]);
    }
    return run(node, [[0, () => { anim(fx, node, "create", 0, ONCE); sound(fx, c.kaiser_createFx || SFX.kaiserCreate); }],
                      [3, () => anim(fx, node, "root", FADE, LOOP)]]);
  });
}
