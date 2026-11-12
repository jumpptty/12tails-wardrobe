// wardrobe/fxparts/alphatimer.js: BB's AlphaTimer (agent alphatimer, 2026-11-10; plans/fx_sheep/parts.md "AlphaTimer",
// the loader comment above FX_PART_FILES in index.html). It draws nothing: it fades the material of its own node's
// renderer (this.renderer, AlphaTimer.cs:63, :283-312), the mesh StaticMesh / SkinnedMeshRenderer (mesh.js) hung there.
// Sheep: lullaby_ring, soulOfArms (x4 weapons), edenSanctuary, divinityAxe / Spear / Sword.
//
// Fields (AlphaTimer.cs:378-402): MinAlpha, MaxAlpha, FadeDelay, FadeEaseIn, FadeMiddle, FadeEaseOut, eraseShadow,
// repeat, endDestroy.
// - Start (:38-100): the phase ends d = FadeDelay, i = d + FadeEaseIn, m = i + FadeMiddle, o = m + FadeEaseOut from the
//   spawn; the colour it drives: _Color if the shader has it (mode 1, :63), else _TintColor (mode 2, :74), else the
//   component turns itself off (:85-87).
// - Update (:104-321), t = time since Start, alpha starts at 0 (:115): d > t MinAlpha; i > t lerp Min -> Max; m > t
//   MaxAlpha; o > t lerp Max -> Min; t > o: repeat restarts the clock (:169-199, that frame keeps 0), endDestroy destroys
//   the node (:201-207), else MinAlpha (:215). Strict tests: an empty phase is skipped, nothing divides by 0. Then
//   color.a = alpha into renderer.material's _Color or _TintColor (:276-321).
// - eraseShadow (:222-275) only switches shadow casting: the page casts none. AlphaTimerFadeOut (:328-357) is called
//   only by Cat (Cat.cs:10603: Support Fire's end, BroadcastMessage("AlphaTimerFadeOut", 0.5) to every cannon): the
//   emitter's fadeOut(sec) (2026-11-13, plans/fx_cat/parts.md part 4, Interfaces 2, decisions.md 51). It zeroes the delay
//   / ease-in / middle ends and sets the middle end = now, the out end = now + sec (Time.time; the clock is not touched),
//   so from now the alpha lerps MaxAlpha -> MinAlpha over sec (Update's fourth phase, :151-157), then MinAlpha (or the
//   repeat / endDestroy ends). On the page the phase ends count from the timer's start: d = i = 0, m = t, o = t + sec.
// On the page, by the material's shader (mesh.js tags each material with userData.fxBlend = its data blend):
//   add / alpha (Particles/Additive, Alpha Blended: _TintColor, no _Color): opacity = min(1, 2 x alpha), fxMaterial's
//     own rule for a saved tint (index.html fxMaterial);
//   shader:FX/Phoenix (_Color; its alpha = texture.a x _Color.a, Phoenix.shader:21): opacity = alpha;
//   opaque (Diffuse has _Color, but draws no alpha): nothing to see; addsoft (Additive (Soft): neither colour): off;
//   any other shader: its properties are unknown here, so off with a warning.
//   shader:Transparent/Opaque1 and Opaque2 (2026-11-13, the Bison's earthSmasher / massStun rock; plans/fx_bison/parts.md
//     part 2, decision 37): _Color in both passes (Material { Diffuse [_Color] }, Opaque1.shader:10-18), alpha =
//     _Color.a x texture.a with no "double" (mesh.js:103-126): opacity = alpha, on BOTH passes (mesh.js opaque1() /
//     opaque2() give pass 1 then pass 2, userData.fxPass 0 / 1). While the alpha is under 0.95 pass 1's alpha test
//     draws nothing and pass 2 blends: the game's own fade (earthSmasher holds 0.8 s, out 0.2 s; massStun 0.5, 0.3).
// Unity's renderer.material is the renderer's own copy of its first material (the others stay shared), ONE copy driving
// every pass of that material's shader, so the first material and its other passes are cloned per spawn: mesh.js and
// FX.mats share one material per class and name across spawns and effects.
// The clock runs as mesh.js's Animation's does (t += dt from the first update), so Eden's 1 s rise and 1 s fade-in agree.
//
// THE SHARED PER-RENDERER COPY (plans/fx_bison/parts.md Interfaces 3, decision 38; the same comment heads uvscroll.js):
// every part that needs Unity's renderer.material (AlphaTimer, UVScroll, any later one) takes it through ownMats(mesh,
// owner) below, so the parts on one renderer share ONE copy, in either component order (aspect_slam: StaticMesh,
// UVScroll, AlphaTimer; aspect_trample: SkinnedMeshRenderer, AlphaTimer, UVScroll). The first part to need it clones
// mesh.material[0] and, when that one is a pass 1 (userData.fxPass === 0), the next entry, its pass 2 (fxPass === 1),
// keeping onBeforeCompile / customProgramCacheKey (Material.copy leaves them out), writes them back in place and sets
// mesh.userData.fxOwn = { mats: [pass 1, pass 2?], owner: <that part's emitter> }. A later part that finds fxOwn uses
// those materials as they are and never clones again. Only the owner frees them (here: the owned list, once the effect
// is gone; uvscroll.js: its dispose()). UVScroll's own clone of the copy's map is mesh.userData.fxOwnMap (uvscroll.js).
export default function register(api) {
  const OPACITY = { add: a => Math.min(1, 2 * a), alpha: a => Math.min(1, 2 * a), "shader:FX/Phoenix": a => a,
    "shader:Transparent/Opaque1": a => a, "shader:Transparent/Opaque2": a => a };
  const NONE = new Set(["opaque", "addsoft"]);
  let owned = [];                                // [fx, material]: a clone is freed once its effect is gone
  // the shared per-renderer copy (above): [its materials, true when this call made them]
  const ownMats = (mesh, owner) => {
    if (mesh.userData.fxOwn) return [mesh.userData.fxOwn.mats, false];
    const arr = Array.isArray(mesh.material), list = arr ? mesh.material : [mesh.material];
    const n = list[0]?.userData.fxPass === 0 && list[1]?.userData.fxPass === 1 ? 2 : 1;
    const mats = list.slice(0, n).map(m => {
      const c = m.clone();
      c.onBeforeCompile = m.onBeforeCompile;     // Material.copy leaves it out: fxMaterial's additive alpha lives there
      c.customProgramCacheKey = m.customProgramCacheKey;
      return c;
    });
    if (arr) mats.forEach((c, k) => { mesh.material[k] = c; }); else mesh.material = mats[0];
    mesh.userData.fxOwn = { mats, owner };
    return [mats, true];
  };
  // the renderer's own copy of its first material (all its passes) and the opacity rule, or null when the timer has
  // nothing to drive
  const own = (mesh, owner) => {
    const list = Array.isArray(mesh.material) ? mesh.material : [mesh.material], m = list[0];
    const blend = m?.userData.fxBlend, set = OPACITY[blend];
    if (!set) {
      if (!NONE.has(blend)) console.warn("AlphaTimer: no _Color / _TintColor known for", blend, m?.name);
      return null;
    }
    const [mats, mine] = ownMats(mesh, owner);
    return [mats, set, mine];
  };
  api.part("AlphaTimer", (fx, node, a, mat, nodeDef) => {
    if (a.enabled === false || nodeDef.active === false) return null;
    owned = owned.filter(([f, m]) => f.alive || (m.dispose(), false));
    let d = a.FadeDelay, i = d + a.FadeEaseIn, m = i + a.FadeMiddle, o = m + a.FadeEaseOut;   // let: fadeOut moves them
    const lerp = (x, y, u) => x + (y - x) * Math.min(1, Math.max(0, u));   // Mathf.Lerp clamps u
    let t = 0, target;                           // target: undefined until the first update, then [materials, opacity, mine] or null
    const em = { node, update(dt) {
      if (target === undefined) {                // the first update: every part of the node is built by now, in any order
        const mesh = node.isMesh ? node : node.children.find(x => x.isMesh);
        target = mesh ? own(mesh, em) : null;
        if (target?.[2]) for (const c of target[0]) owned.push([fx, c]);
      }
      if (!target) return;                       // enabled = false (:87)
      t += dt;
      let alpha = 0;
      if (d > t) alpha = a.MinAlpha;
      else if (i > t) alpha = lerp(a.MinAlpha, a.MaxAlpha, (t - d) / (i - d));
      else if (m > t) alpha = a.MaxAlpha;
      else if (o > t) alpha = lerp(a.MaxAlpha, a.MinAlpha, (t - m) / (o - m));
      else if (t > o) {
        if (a.repeat) t = 0;                     // the clock restarts; this frame writes alpha 0 (the game's own)
        else if (a.endDestroy) return "destroy";
        else alpha = a.MinAlpha;
      }
      const op = target[1](alpha);
      for (const c of target[0]) c.opacity = op;
    },
    // AlphaTimer.AlphaTimerFadeOut(sec) (AlphaTimer.cs:328-357, the header above): Max -> Min over sec from now
    fadeOut(sec) { d = 0; i = 0; m = t; o = t + Math.max(0, +sec || 0); } };
    return em;
  });
}
