// wardrobe/fxparts/vortex.js: BB's VortexEmitter (D:\12tails\DecompiledSource\VortexEmitter.cs; plans/fx_wolf/parts.md
// "VortexEmitter"), agent A 2026-11-09. Spiral arms drawn as one mesh in the node's own space (the game's MeshFilter on
// the node, the node's MeshRenderer material): each game frame adds vortexCount points on the spiral, every point lives
// Life seconds, and each arm is a strip joining a point to the same arm's point one frame older.
// Wolf: darkEdge_ring (6 arms, rises 2 m), dualBrand_slash3 (4 arms, drifts -6 m along the node's y).

// The game emits once per FRAME (VortexEmitter.cs:356-429: a frame counter, not a clock), so the spiral's length in time
// and the spacing of its points follow the game's frame rate. BB asks for 80 fps (Application.targetFrameRate = 80,
// LoginGui.cs:484); vSync on a 60 Hz monitor caps it at 60. The page emits on its own fixed tick at this rate, whatever
// the browser's frame rate. To compare: wardrobe/?vortexfps=60 (and the default 80) in two tabs.
const VORTEX_FPS_DEFAULT = 80;
const VORTEX_FPS = (() => {
  try { const v = Number(new URLSearchParams(location.search).get("vortexfps")); return v > 0 ? v : VORTEX_FPS_DEFAULT; }
  catch (e) { return VORTEX_FPS_DEFAULT; }
})();

export default function register(api) {
  const { THREE, ramp, clamp01, rnd, fxMesh, setMesh } = api;
  const lerp = (a, b, u) => a + (b - a) * u;

  api.part("VortexEmitter", (fx, node, e, mat) => {
    if (!mat) return null;                       // nothing to draw with (the game needs a MeshRenderer, :10-12)
    const m = fxMesh(node, mat);
    const vc = Math.max(1, e.vortexCount | 0);   // vortexCount < 1 becomes 1 (:344-355)
    const life = e.Life, step = 1 / VORTEX_FPS;
    // Time.time: the game's absolute clock, which also sets the spiral's starting angle (Rotation x Time.time, :379-384)
    // and Spin (:202, :251, :300). Here an arbitrary start (the page's clock at spawn) advanced by the page's dt, so a
    // paused move holds the vortex too.
    let time = performance.now() / 1000;
    let start = time;                            // Awake: VxFnYeUnJZC = Time.time (:118)
    let next = time;                             // the next game frame (the first LateUpdate runs in the spawn frame)
    let count = 0;                               // oMHnYIxVqj0, frames emitted (:356, :362)
    const pts = [];                              // aXonYJtAZSS: newest first (Unshift, :414), oldest popped (:183)
    let drawn = false;                           // false: the game left the mesh as it was this frame (before Delay, a restart)

    // one game LateUpdate at time T (:147-463); "destroy" when the emitter is done
    const lateUpdate = T => {
      if (T < start + e.Delay) { drawn = false; return; }                        // :155
      while (pts.length && T > pts[pts.length - 1].time + life) pts.pop();      // :167-189, the old end first
      if (count <= e.length) {                                                   // length + 1 frames of emission (:356)
        count++;                                                                 // :362
        for (let i = 0; i < vc; i++) {                                           // :372-424
          const th = e.Rotation * T + i * e.vortexRadian, s = Math.sin(th), c = Math.cos(th);
          // (cos - sin, 0, sin + cos): length sqrt 2, the game's own (:389-399); rnd 0..rndRadius (:404)
          pts.unshift({ x: c - s, z: s + c, rnd: rnd(0, e.rndRadius), time: T });
        }
      } else if (!pts.length) {                                                  // :430
        if (!e.repeatForever) return "destroy";                                  // Destroy(gameObject) (:456)
        count = 0; start = T; drawn = false;                                     // :442-452: no mesh rebuilt this frame
        return;
      }
      drawn = true;
    };

    // Spin (:190-343): the node's WORLD Euler x, then y, then z, each SET (not added) to 57.29578 x Time.time x Spin / Life
    // degrees (the absolute clock, so the angle doesn't start at 0), reading the rotation back between the three. Unity's
    // eulerAngles are its Euler(z, x, y) order, three's "YXZ"; Unity's world = the mirror group's space here (fx.uQuat).
    // Approximate only at gimbal lock (x = +-90 degrees), where Unity and three may split y / z differently.
    const spin = T => {
      const sp = e.Spin;
      if (!sp || !(sp[0] || sp[1] || sp[2])) return;
      const pInv = fx.uQuat(node.parent).invert(), eu = new THREE.Euler(0, 0, 0, "YXZ"), q = new THREE.Quaternion();
      ["x", "y", "z"].forEach((ax, k) => {
        if (!sp[k]) return;
        eu.setFromQuaternion(fx.uQuat(node), "YXZ");
        eu[ax] = T * sp[k] / life;              // 57.29578 x (rad) degrees = rad radians
        node.quaternion.copy(pInv).multiply(q.setFromEuler(eu));                  // transform.rotation = world
      });
    };

    // the mesh at time T (:464-735), in the node's own space
    const build = T => {
      // the points the game still holds at T (pruning is by time, :173; whole frames go together, so the strips stay whole)
      let n = pts.length;
      while (n && T > pts[n - 1].time + life) n--;
      const pos = [], col = [], uv = [], idx = [];
      for (let j = 0; j < n; j++) {
        const p = pts[j], u = T - p.time !== 0 ? clamp01((T - p.time) / life) : 0;   // :505-526
        const r = lerp(e.startRadius, e.endRadius, u) + p.rnd;                         // :537
        const hw = 0.5 * lerp(e.startWidth, e.endWidth, u);                            // :547
        const bx = e.localVelocity[0] * u, by = e.localVelocity[1] * u, bz = e.localVelocity[2] * u;   // the whole drift over life (:552)
        pos.push(p.x * r + bx, by, p.z * r + bz);                                      // inner (:557)
        if (!e.alwaysUp) pos.push(p.x * (r + hw) + bx, by, p.z * (r + hw) + bz);        // outer, out along the arm (:568)
        else pos.push(p.x * r + bx, hw + by, p.z * r + bz);                           // outer, up the node's y (:576)
        // UVTile 0: the game's 2n / (j + 1), integer division (:588-593); otherwise along the age (:601-606)
        const uu = e.UVTile === 0 ? Math.floor(2 * n / (j + 1)) : u * e.UVTile;
        uv.push(uu, 0, uu, 1);
        const c = ramp(e, u);                                                          // C1..C5 at 0 / .25 / .5 / .75 / 1 (:612-655)
        col.push(...c, ...c);
      }
      // each point to the same arm's point one frame older: index j + vortexCount (:674-717)
      const o = (vc - 1) * 2;
      for (let j = 0; j < Math.max(0, n - vc); j++)
        idx.push(j * 2, j * 2 + 1, j * 2 + 2 + o, j * 2 + 2 + o, j * 2 + 1, j * 2 + 3 + o);
      setMesh(m, pos, col, uv, idx);
    };

    // EffectControl's after-life stops only ParticleEmitters and ImageEmitters (EffectControl.cs:442, :469, :484), and no
    // other BB script touches a VortexEmitter, so there is no stop(): it runs until it ends or the effect is removed.
    return { node, update(dt) {
      time += dt;
      for (; next <= time; next += step) if (lateUpdate(next) === "destroy") return "destroy";
      // Emission stays on the fixed tick; between ticks the mesh is rebuilt at the page's own time (the game rebuilds it
      // every frame from the clock, so ages and Spin are smooth at any frame rate)
      if (!drawn) return;
      spin(time);
      build(time);
    } };
  });
}
