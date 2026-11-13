// wardrobe/fxparts/rabbit.js: the Rabbit's BB summon (builder rabbit, 2026-11-13; plans/fx_rabbit/decisions.md 30, 52,
// parts.md part 7; the loader comment above FX_PART_FILES in index.html). Lines are D:\12tails\DecompiledSource\<file>
// (C:\Users\Jump\Desktop\12tails\... on the office PC).
//   LightGolem   Contract's mercenary at sLv 3 (Rabbit.cs:11590-11611: Characters/Elementals/LightGolem/LightGolem at
//                about 3 m ahead, LookRotation(the hero's forward); wardrobe_fx.py EXTRA_FOLDERS["rabbit"]). Its AI, with no
//                foe in reach, stands in `root` CrossFaded with wrapMode Loop (LightGolem.cs:635-640, :763-768, :847-866):
//                on the page `root` looped from the spawn, no AI (Mole decision 32), no material swap (LightGolem2 is the
//                game's layer-9 look, skills_b verification 1). The cue's kill (10, the 10 s rule) ends it, not its 300 s
//                life (LightGolem.cs:44)
// Space: the root hangs in the effect's mirror group (Unity's world, the hero's feet at the origin, +z her facing). The
// Animation is looked up when due, on the first update (the Bat's gotcha: mesh.js may be built after this script).

export default function register(api) {
  const LOOP = 2;                                      // UnityEngine.WrapMode.Loop
  const fxAnim = (fx, node) => node.userData.fxAnim || fx.root?.userData.fxAnim
    || fx.nodes.find(o => o?.userData?.fxAnim)?.userData.fxAnim || null;

  api.part("LightGolem", (fx, node) => {
    if (fx.cls !== "rabbit") return null;
    let started = false;
    return { node, update() {
      if (started) return;
      started = true;
      const a = fxAnim(fx, node);
      if (!a?.play) console.warn("effect part (rabbit.js): no Animation play() on", fx.name, "(fxparts/mesh.js)");
      else if (!a.play("root", 0, LOOP)) console.warn("effect part (rabbit.js): no clip root on", fx.name);
    } };
  });
}
