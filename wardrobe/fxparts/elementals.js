// wardrobe/fxparts/elementals.js: the Monkey's summons and armours (agent elementals, 2026-11-13; plans/fx_monkey/decisions.md
// 30-37, 39, 41, 48; parts.md parts 8-9 with its Verification 6-7; skills_b.md "Parts needed" 4 + Verification 2; skills_a.md
// Verification 2, 3, 5; effect_only.md Verification 1-2; tto.md P8 + Verification 8; the loader comment above FX_PART_FILES in
// index.html). Lines are D:\12tails\DecompiledSource\<file> (opaque predicates worked by hand; the same files are under
// C:\Users\Jump\Desktop\12tails on the office PC); TTO1102: = DecompiledSource_TTO_2026-11-02 (tto.md 2.1, 2.3).
//   Phoenix / Ja / Gadina / Buiten / Gaos   the summons' scripts on their prefab roots (Phoenix4, Ja4, Gadina4, Buiten4,
//                                           Gaos: whole characters from Resources/GameAssets/Characters/Elementals/,
//                                           wardrobe_fx.py EXTRA_FOLDERS["monkey"]), beside the root's Animation (mesh.js)
//                                           and CharacterControl (NOT_DRAWN). No AI (decision 41)
//   fx:phoenixArmor / fx:gadinaArmor / fx:blazingForm_fire   the hero's code playing the forms' armours (decisions 36-37)
//
// The summon coroutines (the default timeline; the hero code's spawn: Instantiate at mPos, LookRotation(tDir), then
// StartCoroutine(<x>.summon), Monkey.cs:11380-11740 and the same shape for the others, parts.md part 9):
//   Phoenix  $summon$18722 (Phoenix.cs:4564-5100): Play("summon") + Once (:4968), summon_ring at its position, identity,
//            localScale 0.5 x mSummonLv (Phoenix4: 4 -> 2, :4986-4991); Yield 1 s (:5072), then standby, where Phoenix's
//            Update crossfades root (0.2) (:775, :1001). (parts.md's :4297-4313 is RPC_rebirth's copy of the same block.)
//   Ja       $summon$18380 (Ja.cs:1702-2080): Play("summon") + Once (:1997), summon_ring at its position, identity, scale
//            0.5 x mSummonLv (Ja4: 2, :2013-2016); Yield 1 s (:2047); standby, root (0.2) (:462, :688)
//   Gadina   $summon$17985 (Gadina.cs:5944-6510): EquipSword / EquipShield (the cue's attach, decision 32), Play("summon") +
//            Once (:6243), summonEffect at its position, identity (:6269); the wait by GadinaType: 1 / 1 / 1.2 / 1.5 s
//            (Gadina1-4, :6498-6504: Gadina4 1.5); standby, root (0.2) (:971, :1197)
//   Buiten   $summon$17702 (Buiten.cs:557-830): Play("create") + Once (:761), PlayOneShot(buiten_summonFX) (:779),
//            summonEffect at its position AND rotation (:791); Yield 1 s (:812); standby. APPROX: Buiten.cs plays no
//            "root" anywhere (its Update only scans for its DEF aura); the page crossfades root (0.2, Loop) at 1 s as the
//            others (decision 30), so the statue idles instead of holding create's last pose
//   Gaos     $summon$18085 (Gaos.cs:4601-4950): Play("summon") + Once (:4873), createEffect(summon_ring, its position, its
//            rotation) (:4885); Yield 0.8 (:4921), the camera shake (left out, decision 50), Yield 0.7 (:4917), the motion
//            blur (left out), Yield 1.2 (:4925), standby: root (0.2) (:950, :1176) at 0.8 + 0.7 + 1.2 = 2.7 s
// The unsummon coroutines (cue option `end`, seconds after the spawn; decision 30; parts.md Verification 6):
//   Phoenix  $unsummon$18738 (Phoenix.cs:5127-5308): Rewind, Play("ko") + Once (:5261-5267), PlayOneShot(pheonix_unsummon)
//            (:5276); Yield 1 s (:5306), Destroy (:5222)
//   Ja       $unsummon$18387 (Ja.cs:2082-2250): Rewind, Play("ko") + Once (:2219); Yield 1 s (:2247), Destroy (:2177)
//   Gadina   $unsummon$18002 (Gadina.cs:6562-6830): Rewind, Play("unSummon") + Once (:6717), at once summonEffect at its
//            position, identity (:6742); then the wait by GadinaType 1 / 1 / 1.2 / 1.5 s (:6797-6804: Gadina4 1.5), Destroy
//            (:6786). Order: clip, effect, wait, Destroy
//   Buiten   $unsummon$17707 (Buiten.cs:843-1020): Play("unSummon") + Once (:974; no Rewind), PlayOneShot(buiten_unsummonFX)
//            (:995), summonEffect at its position, identity (:1001); Yield 1 s (:1016), Destroy (:938)
//   Gaos     $unsummon$18091 (Gaos.cs:4956-5170): Rewind, Play("unsummon") + Once (:5106), unsummon_ring at its position,
//            identity (:5137); Yield 1.5 s (:5164), Destroy (:5051)
// The summon's look already out (`standing`), its moves (`anims`, `hide`, `moves`, `turn`, `attach`) and TTO's `boost`:
// see the cue options below. Their sounds: the comps' AudioClip fields hold the exported names (wardrobe_fx.py
// SOUND_REFS: `<script, first letter lower>_<AudioClip name>`, the AudioClips Assets/AudioClip/pheonix_cry.wav,
// pheonix_unsummon.wav, gadina_cry.wav, buiten_summon.wav, buiten_unsummon.wav); the names below are the fallbacks when
// a field is empty, and what an entry's "builds" lists (decision 48).
//
// Cue options (fx.at) of a summon (all ages are seconds after the spawn, on the part's own clock from the spawn frame):
//   standing  true: already summoned (decision 31): no summon clip, no ring, no summon sound; root (Loop) from 0
//   anims     [[age, clip, fade?, wrap?], ...]: replaces the default clip timeline (decision 31); fade defaults to 0.2
//             for "root", else 0 (Play); wrap to Loop (2) for "root", else the clip's own Loop / PingPong / ClampForever,
//             else Once (1) (parts.md Verification 7). The script's cry plays with the clips its code pairs it with
//             (CRY below). The ring and the summon sound still come unless `standing`
//   end       the unsummon coroutine at that age (0 works: Titanic Earth Pulse, decision 34); every later anims item,
//             move, turn is dropped (the summon is dead); gone (Destroy) after the coroutine's wait
//   hide      [from, to]: every renderer under the summon off between those ages (Sky Crimson: GetComponentsInChildren
//             (Renderer).enabled = false / true, Phoenix.cs:3507-3529, :3743-3751); the meshes the page itself keeps hidden
//             (no material) stay hidden
//   moves     [[age, m/s], ...]: from each age it walks along its own forward at that speed (Instant Blaze: moveSpeed 12,
//             6, 0, Phoenix.cs:2826, :3156, :3075; the CharacterController's vMovement = forward); at the first move
//             phoenix_instantBlaze_ring rides it (createEffect(instantBlaze_ring, position, rotation), :2837: its
//             EffectControl follows its owner, InitEffectControl, CharacterControl.cs:24191-24220): api.spawn with
//             followNode = the root, local zero / identity. APPROX: followPosition taken as parented (the ring turns with it)
//   turn      age: LookAt the hero on the flat (vFlat(summoner) at its own height: yaw toward the origin, 180 from 2 m
//             ahead) and its cry (Phoenix.cs:1941-2020 RPC_summonDefense: LookAt :2000, PlayOneShot(pheonix_cry) :2009;
//             Gadina / Gaos the same shape with gadina_cry / gaos_cry, Gadina.cs:2234, Gaos.cs:1978)
//   attach    [[effect, bone], ...]: api.spawn(effect) with followNode = this summon's node of that name, local zero /
//             identity (Gadina.cs:544-631, :715-819: Instantiate, parent to mount_Hand_R / mount_Hand_L, localPosition
//             0, localRotation identity, localScale 1; decision 32). Spawned at the first frame (the bones are looked up
//             then); they go with the summon (fxSpawn's followNode: when the node leaves the stage). APPROX: the spawned
//             scale is kept (Unity: localScale 1 under the bone, so the bone's world scale would apply)
//   boost     TTO's boosted summon (tto.md P8, 2.1, 2.3; decision 39): level = clamp(4 + boost, 1, 6), and from level 5
//             Ja: tto/jaAscension_aura at the Ja, its rotation, parented (TTO1102:Ja::Ascend@0x1D3D0B0, Ja.c:2728-2819);
//             Buiten: the statue's localScale x 1.2 and tto/buitenBastion_aura at it, identity, parented with its world
//             pose kept, so not scaled with the statue (TTO1102:Buiten::Bastion@0x1D273E0, Buiten.c:1136-1265). Both
//             spawned with followNode = the root (followSnap keeps the aura's own scale: unscaled). The level changes no
//             other look (HP, follow distance). APPROX: the ring keeps the rank-4 scale (Ascend / Bastion run after the
//             summon coroutine's first step: RPC_ja_create / RPC_buiten_create start it, then boost)
// The page's own options keep working: kill (Fx.killAt), single (a live copy gets the new cue: fx.onSingle below), d / x
// / y / rot / scale (the spawn pose).
// fx.onSingle(cue) (for page_pipeline: index.html's `single` branch may call `own.onSingle?.(c)`): the live copy restarts
// its timeline from the new cue on its own clock, as already summoned / worn (the game: the command runs on the summon
// that stands). Without the call a reused copy keeps its first cue's timeline.
// Space: every root hangs in the effect's mirror group (Unity's world, the hero's feet at the origin, +z her facing, y 0
// the floor), so node.position / quaternion are the game's transform.position / rotation. The Animation is looked up when
// a clip is due (the Bat's gotcha: mesh.js's part on the same node may be built after this one).

export default function register(api) {
  const { THREE, V } = api;
  const DEG = Math.PI / 180;
  const ONCE = 1, LOOP = 2;                             // UnityEngine.WrapMode
  const warned = new Set();
  const warnOnce = (k, ...m) => { if (!warned.has(k)) { warned.add(k); console.warn(...m); } };
  const num = (x, d) => (Number.isFinite(+x) && x !== null && x !== "" ? +x : d);
  const eulerOf = q => { const e = new THREE.Euler().setFromQuaternion(q, "YXZ"); return [e.x / DEG, e.y / DEG, e.z / DEG]; };
  const fxAnim = fx => fx.root?.userData.fxAnim || fx.nodes.find(o => o?.userData?.fxAnim)?.userData.fxAnim || null;
  // Animation.Play / CrossFade + wrapMode (mesh.js play(name, fade, wrap)); defaults as the cue options say
  // (the clip's own wrap from any node's Animation of the effect's data: def = data.effects[fx.name])
  const clipWrap = (def, clip) => {
    for (const n of def?.nodes || []) {
      const w = n.comps?.find(x => x.type === "Animation" && x.clips?.[clip])?.clips[clip].wrap;
      if (w != null) return w === 2 || w === 4 || w === 8 ? w : ONCE;
    }
    return ONCE;
  };
  const anim = (fx, def, clip, fade, wrap) => {
    const a = fxAnim(fx);
    if (!a?.play) return warnOnce("anim:" + fx.name, "effect part (elementals.js): no Animation play() on", fx.name, "(fxparts/mesh.js)");
    const f = num(fade, clip === "root" ? 0.2 : 0), w = num(wrap, clip === "root" ? LOOP : clipWrap(def, clip));
    if (!a.play(clip, f, w)) warnOnce("clip:" + fx.name + clip, "effect part (elementals.js): no clip", clip, "on", fx.name);
  };
  const items = list => (Array.isArray(list) ? list.filter(a => Array.isArray(a) && a.length >= 2 && Number.isFinite(+a[0])) : []);
  const sound = (fx, n) => { if (n) fx.sounds.push({ node: fx.root, comp: null, h: api.Sound.play(fx.cls, n) }); };
  const spawn = (who, name, at, opts) => {
    const f = api.spawn?.(name, at, opts);
    if (!f) warnOnce("miss:" + name, `effect part ${who}: ${name} not spawned (not in fx.json: the entry's "builds")`);
    return f;
  };
  // the cue options of an effect at this summon's present pose (its root is a child of the mirror group: Unity's world)
  const here = (node, rot, scale) => ({ x: node.position.x, y: node.position.y, d: node.position.z,
    rot: rot ? eulerOf(node.quaternion) : [0, 0, 0], ...(scale ? { scale } : {}) });

  // ---------------------------------------------------------------- the summons
  // first: the summon clip; ring: its summon look [name, its rotation?, scale by level?]; wait(lv): the coroutine's wait to
  // standby; snd: the summon's PlayOneShot [field, fallback]; un: the unsummon coroutine; cry: [field, fallback] with the
  // clips the code pairs it with
  const SUMMONS = {
    Phoenix: { first: "summon", ring: ["phoenix_summon_ring", false, lv => 0.5 * lv], wait: () => 1,
               un: { clip: "ko", rewind: true, snd: ["pheonix_unsummon", "phoenix_pheonix_unsummon"], gone: () => 1 },
               // nAttack Phoenix.cs:2594 / :2612, skyCrimson1 :3908 / :3932, instantBlaze :3240 / :3258 (the cry in the same step)
               cry: ["pheonix_cry", "phoenix_pheonix_cry"], cryClips: ["nAttack", "skyCrimson1", "instantBlaze"] },
    Ja:      { first: "summon", ring: ["ja_summon_ring", false, lv => 0.5 * lv], wait: () => 1,
               un: { clip: "ko", rewind: true, gone: () => 1 }, aura: "tto/jaAscension_aura" },
    // planetBreak Gadina.cs:5817 / :5857, guard :5313 / :5343
    Gadina:  { first: "summon", ring: ["gadina_summonEffect", false, null], wait: lv => GADINA_WAIT[lv] ?? 1.5,
               un: { clip: "unSummon", rewind: true, fx: "gadina_summonEffect", gone: lv => GADINA_WAIT[lv] ?? 1.5 },
               cry: ["gadina_cry", "gadina_gadina_cry"], cryClips: ["planetBreak", "guard"] },
    Buiten:  { first: "create", ring: ["buiten_summonEffect", true, null], wait: () => 1, snd: ["buiten_summonFX", "buiten_buiten_summon"],
               un: { clip: "unSummon", rewind: false, snd: ["buiten_unsummonFX", "buiten_buiten_unsummon"], fx: "buiten_summonEffect", gone: () => 1 },
               aura: "tto/buitenBastion_aura", auraScale: 1.2 },
    Gaos:    { first: "summon", ring: ["gaos_summon_ring", true, null], wait: () => 0.8 + 0.7 + 1.2,
               un: { clip: "unsummon", rewind: true, fx: "gaos_unsummon_ring", gone: () => 1.5 },
               cry: ["gaos_cry", "gaos_gaos_cry"], cryClips: [] },
  };
  const GADINA_WAIT = { 1: 1, 2: 1, 3: 1.2, 4: 1.5 };   // Gadina.cs:6498-6504 (summon), :6797-6804 (unsummon)
  const field = (c, f) => (f ? (typeof c?.[f[0]] === "string" && c[f[0]] ? c[f[0]] : f[1]) : null);

  for (const [script, S] of Object.entries(SUMMONS)) api.part(script, (fx, node, c, mat, nd, data) => {
    if (fx.cls !== "monkey") return null;
    const def = data?.effects?.[fx.name];
    const who = script + " (elementals.js)";
    const lv = +(/(\d)$/.exec(fx.name)?.[1] || 4);       // Phoenix4 / Ja4 / Gadina4 / Buiten4; Gaos has one rank
    const at = fx.at || {};
    const boost = num(at.boost, 0), boosted = boost > 0 && Math.min(6, Math.max(1, lv + boost)) >= 5;
    if (boosted && S.auraScale) node.scale.multiplyScalar(S.auraScale);   // Buiten::Bastion's localScale x 1.2 (the spawn frame)
    const cry = () => sound(fx, field(c, S.cry));
    let t = 0, ev = [], i = 0, speed = 0, moving = false, hidden = null;
    const setHidden = on => {
      if (on && !hidden) { hidden = []; node.traverse(o => { if ((o.isMesh || o.isPoints || o.isLine) && o.visible) { o.visible = false; hidden.push(o); } }); }
      else if (!on && hidden) { for (const o of hidden) o.visible = true; hidden = null; }
    };
    // the timeline from a cue (standing: the summon is out already)
    const load = (q, standing) => {
      t = 0; i = 0; speed = 0; moving = false; setHidden(false);
      ev = [];
      const end = q.end != null && Number.isFinite(+q.end) ? +q.end : null;
      const given = items(q.anims);
      if (!standing) ev.push([0, () => {
        anim(fx, def, S.first, 0, ONCE);
        sound(fx, field(c, S.snd));
        const [name, own, scale] = S.ring;
        spawn(who, name, here(node, own, scale?.(lv)));
      }]);
      if (given.length) for (const [age, clip, fade, wrap] of given) ev.push([+age, () => {
        anim(fx, def, clip, fade, wrap);
        if (S.cryClips?.includes(clip)) cry();
      }]);
      else if (standing) ev.push([0, () => anim(fx, def, "root", 0, LOOP)]);
      else ev.push([S.wait(lv), () => anim(fx, def, "root", 0.2, LOOP)]);
      // the first frame: what rides it (the bones looked up when due)
      ev.push([0, () => {
        for (const a of Array.isArray(q.attach) ? q.attach.filter(a => Array.isArray(a) && a.length >= 2) : []) {
          const bone = fx.nodes.find(o => o.name === a[1]);
          if (!bone) { warnOnce("bone:" + a[1], `effect part ${who}: no node ${a[1]} on ${fx.name}`); continue; }
          spawn(who, String(a[0]), {}, { followNode: bone, local: {} });
        }
        if (boosted && S.aura) spawn(who, S.aura, {}, { followNode: node, local: {} });
      }]);
      if (Number.isFinite(+q.turn) && q.turn !== null) ev.push([+q.turn, () => {
        const p = node.position;
        if (p.x * p.x + p.z * p.z > 1e-10) node.quaternion.setFromAxisAngle(V(0, 1, 0), Math.atan2(-p.x, -p.z));
        cry();
      }]);
      const moves = items(q.moves);
      moves.forEach(([age, v], k) => ev.push([+age, () => {
        speed = num(v, 0); moving = true;
        if (k === 0) { spawn(who, "phoenix_instantBlaze_ring", {}, { followNode: node, local: {} }); }
      }]));
      if (Array.isArray(q.hide) && q.hide.length >= 2) {
        ev.push([num(q.hide[0], 0), () => setHidden(true)], [num(q.hide[1], Infinity), () => setHidden(false)]);
      }
      ev.sort((a, b) => a[0] - b[0]);                    // stable: the summon's own first-frame steps keep their order
      if (end != null) {                                 // the unsummon: nothing after it plays
        ev = ev.filter(e => e[0] <= end);                // (sorted, so the unsummon below comes after the rest at its age)
        const U = S.un;
        ev.push([end, () => {
          speed = 0; moving = false; setHidden(false);
          const a = fxAnim(fx);
          if (U.rewind) a?.rewind?.();
          anim(fx, def, U.clip, 0, ONCE);
          sound(fx, field(c, U.snd));
          if (U.fx) spawn(who, U.fx, here(node, false));
        }], [end + U.gone(lv), () => "destroy"]);
      }
    };
    load(at, !!at.standing);
    fx.onSingle = q => load(q || {}, true);
    const fwd = V();
    return { node, update(dt) {
      t += dt;
      while (i < ev.length && t >= ev[i][0]) if (ev[i++][1]() === "destroy") return "destroy";
      if (moving && speed) node.position.addScaledVector(fwd.set(0, 0, 1).applyQuaternion(node.quaternion), speed * dt);
    }, dispose() { setHidden(false); } };
  });

  // ---------------------------------------------------------------- fx:phoenixArmor, fx:gadinaArmor, fx:blazingForm_fire
  // Monkey.cs (effect_only.md P1 + Verification 1-2, parts.md part 8): the Fire Avatar armour Effects/phoenixArmor and the
  // Earth Form armour gadinaArmor (parented to the hero, local 0 / identity, :38395-38438, :40732-40747) and the fire form
  // blazingForm_fire are played by the hero's code: Play("summon") at creation (phoenixArmor 1.0 s, gadinaArmor 0.8 s),
  // then Update's CrossFade("root", 0.2) + Loop while she stands (:509, :523; :573, :587); the form's attack Rewind +
  // Play("nAttack") (:39219-39229); Blazing Form's Play("blazingForm1") (:40001), Play("blazingForm2") + Loop
  // (:39595-39600), the release's CrossFade("root", 0.5) (:40360); the armour's materials[0].color.a lerped 0.7 -> 0 over
  // 0.8-1.0 s, the renderer off at 1.0 (:39871, :39900-39927), on again and 0 -> 0.7 over 0.2 s at the release (:40392,
  // :40436-40447); the fire form's Play("root") at 1.0 s (:39882; its "destroy" comes with the page's followState end).
  // Cue options: anims [[age, clip, fade?, wrap?], ...] (as the summons': a cue's anims replaces the default; none
  // given: summon, then root), alpha [[age, a], ...]: the opacity of this effect's OWN copies of its skinned materials
  // (mesh.js shares one material per name, so a shared one would fade every live armour: effect_only Verification 2;
  // alphatimer.js's pattern): untouched before the first key, linear between keys, held after; 0 = the renderer off.
  // The copies are made once, at the first cue with alpha, and freed in dispose. fx.onSingle(cue): the timeline again
  // from the new cue (decision 37: the form's tiles reuse the armour already worn)
  const armour = dflt => (fx, node, c, mat, nd, data) => {
    if (fx.cls !== "monkey") return null;
    const def = data?.effects?.[fx.name];
    let anims = [], keys = [], t = 0, k = 0;
    const meshes = [], own = [];
    const copies = () => {
      if (own.length) return;
      fx.root.traverse(o => {
        if (!o.isSkinnedMesh) return;
        const list = [].concat(o.material).map(m => {
          const cp = m.clone(); cp.onBeforeCompile = m.onBeforeCompile; cp.customProgramCacheKey = m.customProgramCacheKey;
          own.push(cp); return cp;
        });
        o.material = Array.isArray(o.material) ? list : list[0];
        meshes.push([o, list]);
      });
    };
    const load = q => {
      const given = items(q?.anims);
      anims = (given.length ? given : dflt).slice().sort((a, b) => a[0] - b[0]);
      keys = items(q?.alpha).slice().sort((a, b) => a[0] - b[0]);
      if (keys.length) copies();
      t = 0; k = 0;
    };
    load(fx.at);
    fx.onSingle = load;
    return { node: fx.root, update(dt) {
      t += dt;
      while (k < anims.length && t >= anims[k][0]) { const [, clip, fade, wrap] = anims[k++]; anim(fx, def, clip, fade, wrap); }
      if (!keys.length || t < keys[0][0]) return;
      const j = keys.findIndex(q => q[0] > t);
      const a = j < 0 ? keys[keys.length - 1][1]
        : keys[j - 1][1] + (keys[j][1] - keys[j - 1][1]) * (t - keys[j - 1][0]) / (keys[j][0] - keys[j - 1][0]);
      for (const [o, list] of meshes) { o.visible = a > 0; for (const m of list) m.opacity = a; }
    }, dispose() { for (const m of own) m.dispose(); own.length = 0; } };
  };
  api.part("fx:phoenixArmor", armour([[0, "summon", 0, ONCE], [1.0, "root", 0.2, LOOP]]));   // summon 1.0 s (parts.md part 8)
  api.part("fx:gadinaArmor", armour([[0, "summon", 0, ONCE], [0.8, "root", 0.2, LOOP]]));    // summon 0.8 s
  api.part("fx:blazingForm_fire", armour([]));
}
