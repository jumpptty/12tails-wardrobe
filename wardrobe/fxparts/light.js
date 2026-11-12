// wardrobe/fxparts/light.js: Unity's built-in Light on an effect node (2026-11-13, the Bat: plans/fx_bat/parts.md part 7,
// decisions.md 42). The Bat's drainLife (pink, (1, 0.53, 1)) and mindControl_ring (cyan, (0.085, 0.92, 1)), the Wolf's
// crusader_hit / lawbringer_hit: each a point light (m_Type 2), intensity 1, range 2, render mode 2 (ForceVertex, "not
// important": per vertex), no shadows, no cookie (checks/fx_bat_research/parts/probe.txt). wardrobe_fx.py stores the
// component's fields as they are ("Light", m_Color {r, g, b, a}, m_Intensity, m_Range, m_Type, m_Enabled ...).
// In Unity 3.5 it lights the lit materials within its range (the hero, whose hand casts the bolt, and lit effect meshes:
// Phoenix / Opaque / Lambert); the particle shaders are unlit, as the page's.
//
// The page: three recompiles every lit material when the number of lights changes, so the page keeps a pool of point
// lights in the scene from the start (index.html, the lead's): api.pointLight() lends one (null when every one is out),
// api.releaseLight(l) gives it back (dark). The light lives in the scene, not under the node, so each frame it takes the
// node's world position; it is dark while the effect is hidden (VFX off, a hidden branch). The falloff (Unity's
// 1 / (1 + 25 (d / range)^2), nothing past the range) is the page's patch of three's getDistanceAttenuation; here
// distance = m_Range. Colour: m_Color as the game's gamma value (sRGB). Intensity 2 x pi x m_Intensity: Unity 3.5's lit
// shaders double the light, three's Lambert divides it by pi. APPROXIMATED: that scale (checked by eye on the dark
// stage), and three's per-pixel lighting for the game's per-vertex.
// Its life: a Light shines until its GameObject is destroyed, the after-life too (EffectControl stops only emitters), so
// the light goes back to the pool with the effect (dispose) or with its node (a destroyed branch: three's "removed" on
// the node or any node above it), not at stop().
export default function register(api) {
  const { THREE } = api;
  let warned = false;
  api.part("Light", (fx, node, c) => {
    if (c.m_Enabled === 0 || c.m_Enabled === false) return null;
    if (c.m_Type !== 2) { console.warn("Light: only point lights are drawn", fx.name, node.name, c.m_Type); return null; }
    if (!api.pointLight) { if (!warned) console.warn("Light: api.pointLight missing (index.html), no effect light drawn"); warned = true; return null; }
    let l = api.pointLight();
    if (!l) { console.warn("Light: every pooled point light is in use", fx.name, node.name); return null; }
    const col = c.m_Color || { r: 1, g: 1, b: 1 }, I = 2 * Math.PI * (+c.m_Intensity || 0);
    l.color.setRGB(col.r, col.g, col.b, THREE.SRGBColorSpace);
    l.distance = +c.m_Range || 0;
    l.intensity = 0;                              // dark until its first frame puts it at the node
    const release = () => { if (!l) return; l.intensity = 0; api.releaseLight?.(l); l = null; for (const o of watched) o.removeEventListener("removed", release); };
    // the node and the nodes above it inside the effect: removing any of them (Fx.update's destroyed branch, a child's own
    // EffectControl) takes the light's GameObject with it; Fx.update stops calling a detached node's part, so this does it
    const watched = [];
    for (let o = node; o && o !== fx.mirror; o = o.parent) { o.addEventListener("removed", release); watched.push(o); }
    const p = new THREE.Vector3();
    return { node,
      update() {
        if (!l) return;
        let shown = true;
        for (let o = node; o && shown; o = o.parent) shown = o.visible;   // the effect's group: VFX off, a hidden prop
        node.updateWorldMatrix(true, false);
        p.setFromMatrixPosition(node.matrixWorld);
        if (l.parent && l.parent !== api.scene) l.parent.worldToLocal(p);
        l.position.copy(p);
        l.intensity = shown ? I : 0;
      },
      dispose: release };
  });
}
