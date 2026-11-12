// wardrobe/fxparts/uvscroll.js: BB's UVScroll (agent bison_parts, 2026-11-13; plans/fx_bison/parts.md part 1, decision
// 36 in plans/fx_bison/decisions.md; the loader comment above FX_PART_FILES in index.html). It draws nothing: it scrolls
// the main texture of its own node's renderer, the mesh StaticMesh / SkinnedMeshRenderer (mesh.js) hung there.
// Bison: aspect_slam (StaticMesh, UVScroll, AlphaTimer), aspect_trample's two hordes (SkinnedMeshRenderer, AlphaTimer,
// UVScroll); later the Cat's deltaStrike and the Whale's bowlingWhale.
//
// Fields (UVScroll.cs:67, :70): scroll_x, scroll_y; the constructor's defaults 0.1 / 0.1 (:26, :29); every Bison instance
// is (0.2, -0.2) (checks/fx_bison_research/parts/probe.txt).
// Update (:42-46): offset = (Repeat(Time.time x scroll_x, 100), Repeat(Time.time x scroll_y, 100)), then
// renderer.material.SetTextureOffset("_MainTex", offset) (:45): the renderer's own material copy, its main texture's
// offset REPLACED (the saved offset is lost), from the game's absolute clock, so every UVScroll in the scene scrolls in
// step (the two Trample hordes move together). Here T = the page's absolute clock, performance.now() / 1000 (decision
// 36, as tto_sheep.js's time), and Repeat is Unity's positive modulo. Unity's and three's uv offsets have the same sense
// (fxMaterial and mesh.js set the texture's offset from the data's _MainTex offset as is), so no sign change; the
// texture's repeat (the data's _MainTex scale) is kept.
// three keeps offset and repeat on the Texture object, which mesh.js / fxMaterial share across every material, spawn and
// effect of that texture: the part scrolls its own clone of the copy's map (Texture.clone shares the image source, so
// no second download), put on every pass of the copy, made once the picture has arrived (a clone made before would be a
// texture marked for update with no image: three warns every frame until it loads; nothing of it shows until then).
// APPROXIMATED: the phase (the game's Time.time counts from the client's start; here from the page's).
//
// THE SHARED PER-RENDERER COPY (plans/fx_bison/parts.md Interfaces 3, decision 38; the same comment heads alphatimer.js):
// every part that needs Unity's renderer.material (AlphaTimer, UVScroll, any later one) takes it through ownMats(mesh,
// owner) below, so the parts on one renderer share ONE copy, in either component order (aspect_slam: StaticMesh,
// UVScroll, AlphaTimer; aspect_trample: SkinnedMeshRenderer, AlphaTimer, UVScroll). The first part to need it clones
// mesh.material[0] and, when that one is a pass 1 (userData.fxPass === 0), the next entry, its pass 2 (fxPass === 1),
// keeping onBeforeCompile / customProgramCacheKey (Material.copy leaves them out), writes them back in place and sets
// mesh.userData.fxOwn = { mats: [pass 1, pass 2?], owner: <that part's emitter> }. A later part that finds fxOwn uses
// those materials as they are and never clones again. Only the owner frees them (alphatimer.js: its owned list, once
// the effect is gone; here: dispose()). UVScroll's own clone of the copy's map is mesh.userData.fxOwnMap (freed by the
// UVScroll that made it, in its dispose()).
export default function register(api) {
  // the shared per-renderer copy (above; the same code as alphatimer.js's): [its materials, true when this call made them]
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
  const repeat = (x, l) => x - Math.floor(x / l) * l;   // Mathf.Repeat: in [0, l), negative x included
  api.part("UVScroll", (fx, node, c) => {
    if (c.enabled === false) return null;
    const sx = c.scroll_x ?? 0.1, sy = c.scroll_y ?? 0.1;   // the constructor's defaults (:26, :29)
    let mesh, mats = null, mine = false, map = null, mapMine = false, done = false;
    const em = { node, update() {
      if (done) return;
      if (mesh === undefined) {                  // the first update: every part of the node is built by now, in any order
        mesh = node.isMesh ? node : node.children.find(x => x.isMesh) || null;
        if (!mesh) { done = true; return; }
        [mats, mine] = ownMats(mesh, em);
      }
      if (!map) {
        if (mesh.userData.fxOwnMap) map = mesh.userData.fxOwnMap;   // another UVScroll on this renderer made it
        else {
          const src = mats[0].map;
          if (!src) { done = true; return; }     // no _MainTex: nothing to scroll
          if (!src.image) return;                // its picture not arrived yet (above)
          map = mesh.userData.fxOwnMap = src.clone(); mapMine = true;
          for (const p of mats) {
            if (p.map === src) p.map = map;
            if (p.emissiveMap === src) p.emissiveMap = map;   // FX/Phoenix draws its map as its emission too (mesh.js)
          }
        }
      }
      const T = performance.now() / 1000;
      map.offset.set(repeat(T * sx, 100), repeat(T * sy, 100));
    }, dispose() {
      if (mapMine) map.dispose();
      if (mine) for (const p of mats) p.dispose();
      mapMine = mine = false;
    } };
    return em;
  });
}
