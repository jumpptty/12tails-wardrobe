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
//   only by Cat (Cat.cs:10603).
// On the page, by the material's shader (mesh.js tags each material with userData.fxBlend = its data blend):
//   add / alpha (Particles/Additive, Alpha Blended: _TintColor, no _Color): opacity = min(1, 2 x alpha), fxMaterial's
//     own rule for a saved tint (index.html fxMaterial);
//   shader:FX/Phoenix (_Color; its alpha = texture.a x _Color.a, Phoenix.shader:21): opacity = alpha;
//   opaque (Diffuse has _Color, but draws no alpha): nothing to see; addsoft (Additive (Soft): neither colour): off;
//   any other shader: its properties are unknown here, so off with a warning.
// Unity's renderer.material is the renderer's own copy of its first material (the others stay shared), so the first
// material is cloned per spawn: mesh.js and FX.mats share one material per class and name across spawns and effects.
// The clock runs as mesh.js's Animation's does (t += dt from the first update), so Eden's 1 s rise and 1 s fade-in agree.
export default function register(api) {
  const OPACITY = { add: a => Math.min(1, 2 * a), alpha: a => Math.min(1, 2 * a), "shader:FX/Phoenix": a => a };
  const NONE = new Set(["opaque", "addsoft"]);
  let owned = [];                                // [fx, material]: a clone is freed once its effect is gone
  // the renderer's own copy of its first material, or null when the timer has nothing to drive
  const own = mesh => {
    const list = Array.isArray(mesh.material) ? mesh.material : [mesh.material], m = list[0];
    const blend = m?.userData.fxBlend, set = OPACITY[blend];
    if (!set) {
      if (!NONE.has(blend)) console.warn("AlphaTimer: no _Color / _TintColor known for", blend, m?.name);
      return null;
    }
    const c = m.clone();
    c.onBeforeCompile = m.onBeforeCompile;       // Material.copy leaves it out: fxMaterial's additive alpha lives there
    if (Array.isArray(mesh.material)) mesh.material[0] = c; else mesh.material = c;
    return [c, set];
  };
  api.part("AlphaTimer", (fx, node, a, mat, nodeDef) => {
    if (a.enabled === false || nodeDef.active === false) return null;
    owned = owned.filter(([f, m]) => f.alive || (m.dispose(), false));
    const d = a.FadeDelay, i = d + a.FadeEaseIn, m = i + a.FadeMiddle, o = m + a.FadeEaseOut;
    const lerp = (x, y, u) => x + (y - x) * Math.min(1, Math.max(0, u));   // Mathf.Lerp clamps u
    let t = 0, target;                           // target: undefined until the first update, then [material, opacity] or null
    return { node, update(dt) {
      if (target === undefined) {                // the first update: every part of the node is built by now, in any order
        const mesh = node.children.find(x => x.isMesh);
        target = mesh ? own(mesh) : null;
        if (target) owned.push([fx, target[0]]);
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
      target[0].opacity = target[1](alpha);
    } };
  });
}
