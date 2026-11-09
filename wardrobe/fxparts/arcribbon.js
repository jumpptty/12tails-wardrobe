// wardrobe/fxparts/arcribbon.js: TTO's ArcRibbonEmitter (agent F, 2026-11-09; plans/fx_wolf/build_rules.md, tto.md 3).
// Read from TTO's machine code: Ghidra (the Bible's tools/run_ghidra.bat, read only, over names.tsv) on every method
// below, capstone where Ghidra dropped an argument (TTO1102 = DecompiledSource_TTO_2026-11-02, client/GameAssembly.dll);
// FUN_180308640 = cosf, FUN_180308bd0 = sinf, FUN_180306c80 = powf, identified by running them under unicorn.
//
// Fields (dump.cs TypeDefIndex 402): Life, Delay, flat, profile (0 Crescent, 1 Comet), taper, centre (v3), start/endRadius,
// start/endHead, start/endTail (DEGREES), easeHead, easeTail, start/endHeight, lean, uvTile, uvScroll, Color1..5,
// segments, trail, trailStep, trailFade; private mesh, clock, history (List<Pose {time, pos, rot}>).
//
// What the game does (all from the code):
// - Awake@0x225D2A0: a new dynamic Mesh "ArcRibbon" on the node's MeshFilter.
// - LateUpdate@0x225DD80: clock += dt; when clock > max(0, trail) x trailStep + Life + Delay: Mesh.Clear and the
//   script disables itself (the node stays). Else: history.Add({Time.time, transform.position, transform.rotation});
//   while history.Count > 2 and history[1].time < now - (max(0, trail) x trailStep + 0.1): RemoveAt(0). Then copies
//   k = 0..trail: tk = clock - Delay - k x trailStep, drawn while 0 <= tk <= Life; copy 0 at the newest pose, fade 1;
//   copy k >= 1 at PoseAt(now - k x trailStep) (skipped when the history is younger), fade = (1 - (k - 1) / trail) x
//   trailFade; Build(pose, tk / max(Life, 1e-4), fade, Scale = max(|lossyScale.x|, 0.01)). So the trail is the ribbon
//   as it looked k steps ago, where the node was k steps ago (the Resonance Claw waves fly at 36 m/s: ghosts behind).
// - PoseAt(t)@0x225E3D0: false when the history is empty or t < history[0].time; else the last entry with time <= t
//   (itself if it is the newest) blended to the next: position lerp, rotation Quaternion.Slerp, by
//   (t - t_i) / max(t_i+1 - t_i, 1e-5).
// - Ease(t, e)@0x225DD40 = e == 1 ? t : 1 - (1 - t)^e (clamped 0..1 where Build uses it).
// - Build(pose, t, fade, s)@0x225D370: R = lerp(startRadius, endRadius, clamp01 t) x s; head = lerp(startHead, endHead,
//   Ease(t, easeHead)), tail = lerp(startTail, endTail, Ease(t, easeTail)) (degrees -> radians); H = lerp(startHeight,
//   endHeight, clamp01 t) x s; drawn only when R > 0.001, H > 0.001 and |head - tail| >= 1e-4. Colour = Ramp(t)@0x225E660
//   (the 5-key ramp, the page's ramp). n = max(2, segments); for i = 0..n: f = i / n, a = lerp(tail, head, f);
//   p = profile Crescent ? sin(f pi) : f; w = taper > 0 ? max(p, 0)^taper : 1; the arc point
//   (sin a x R, 0, cos a x R) + centre x s (angle 0 = the node's +z, Unity's yaw);
//   not flat (a standing band): bottom = point - up x H w / 2, top = (sin a x R', 0, cos a x R') + centre x s + up x H w / 2
//   with R' = R + lean x s x w (the top leans out); flat (lying in the node's XZ plane): inner at radius max(0, R - w H),
//   outer at R; vertex alpha = colour.a x sqrt(w) x fade; uv (f x uvTile + clock x uvScroll, 0 inner / bottom, 1 outer /
//   top); quads (2i, 2i+1, 2i+2), (2i+2, 2i+1, 2i+3).
// - Add@0x225D080: world = pose.pos + pose.rot x local, stored through transform.InverseTransformPoint (the CURRENT
//   transform), so a trail copy stays where the node was.
// On the page: poses are read in the mirror group's space (= Unity's world for the effect) from fx.uMatrix / fx.uQuat,
// and vertices go back into the node's space with the inverse of fx.uMatrix(node). Time.time = this emitter's own clock
// (only differences of it are used, so this is exact). No stop(): TTO's EffectControl::Update@0x1A233A0 at the
// after-life reaches ParticleSystems, ImageEmitters and RingEmitters only. Nothing approximated.
export default function register(api) {
  const { V, ramp, fxMesh, setMesh } = api;
  const clamp01 = x => Math.min(1, Math.max(0, x));
  const ease = (t, e) => (e === 1 ? t : 1 - Math.pow(1 - t, e));
  const D2R = Math.PI / 180;

  api.part("ArcRibbonEmitter", (fx, node, e, mat, nodeDef) => {
    if (!mat || e.enabled === false || nodeDef.active === false) return null;
    const m = fxMesh(node, mat);
    const trail = Math.max(0, e.trail | 0), cen = e.centre || [0, 0, 0];
    let clock = 0, now = 0, done = false;
    const history = [];
    const poseAt = t => {                                                  // PoseAt@0x225E3D0
      if (!history.length || t < history[0].time) return null;
      let i = history.length - 1;
      while (i >= 0 && t < history[i].time) i--;
      if (i < 0) return null;
      if (i === history.length - 1) return history[i];
      const a = history[i], b = history[i + 1], f = (t - a.time) / Math.max(b.time - a.time, 1e-5);
      return { time: t, pos: a.pos.clone().lerp(b.pos, clamp01(f)), rot: a.rot.clone().slerp(b.rot, clamp01(f)) };
    };
    return { node, update(dt) {
      if (done) return;
      clock += dt; now += dt;
      if (clock > trail * e.trailStep + e.Life + e.Delay) { done = true; setMesh(m, [], [], [], []); return; }
      const um = fx.uMatrix(node), inv = um.clone().invert();
      history.push({ time: now, pos: V().setFromMatrixPosition(um), rot: fx.uQuat(node) });
      const keep = trail * e.trailStep + 0.1;
      while (history.length > 2 && history[1].time < now - keep) history.shift();
      const s = Math.max(0.01, Math.abs(V().setFromMatrixScale(um).x));
      const pos = [], col = [], uv = [], idx = [];
      for (let k = 0; k <= trail; k++) {
        const tk = clock - e.Delay - k * e.trailStep;
        if (!(tk >= 0 && tk <= e.Life)) continue;
        const P = k === 0 ? history[history.length - 1] : poseAt(now - k * e.trailStep);
        if (!P) continue;
        const fade = k === 0 ? 1 : (1 - (k - 1) / trail) * e.trailFade;
        build(P, tk / Math.max(e.Life, 1e-4), fade, s);
      }
      setMesh(m, pos, col, uv, idx);

      function build(P, t, fade, s) {                                      // Build@0x225D370
        const tc = clamp01(t), R = (e.startRadius + (e.endRadius - e.startRadius) * tc) * s;
        const eh = clamp01(ease(t, e.easeHead)), et = clamp01(ease(t, e.easeTail));
        const H = (e.startHeight + (e.endHeight - e.startHeight) * tc) * s;
        if (!(R > 0.001 && H > 0.001)) return;
        const tail = (e.startTail + (e.endTail - e.startTail) * et) * D2R, head = (e.startHead + (e.endHead - e.startHead) * eh) * D2R;
        if (!(Math.abs(head - tail) >= 1e-4)) return;
        const c0 = ramp(e, t), n = Math.max(2, e.segments), base = pos.length / 3;
        const cx = cen[0] * s, cy = cen[1] * s, cz = cen[2] * s;
        const add = (x, y, z, u, v, a) => {
          const p = V(x, y, z).applyQuaternion(P.rot).add(P.pos).applyMatrix4(inv);
          pos.push(p.x, p.y, p.z); uv.push(u, v); col.push(c0[0], c0[1], c0[2], a);
        };
        for (let i = 0; i <= n; i++) {
          const f = i / n, a = tail + (head - tail) * clamp01(f);
          const p = e.profile === 0 ? Math.sin(f * Math.PI) : f;
          const w = e.taper > 0 ? Math.pow(Math.max(p, 0), e.taper) : 1;
          const sn = Math.sin(a), cs = Math.cos(a), alpha = c0[3] * Math.sqrt(w) * fade, u = f * e.uvTile + clock * e.uvScroll;
          if (!e.flat) {
            const hh = H * 0.5 * w, R2 = R + e.lean * s * w;
            add(sn * R + cx, cy - hh, cs * R + cz, u, 0, alpha);
            add(sn * R2 + cx, cy + hh, cs * R2 + cz, u, 1, alpha);
          } else {
            const Ri = Math.max(0, R - w * H);
            add(sn * Ri + cx, cy, cs * Ri + cz, u, 0, alpha);
            add(sn * R + cx, cy, cs * R + cz, u, 1, alpha);
          }
        }
        for (let i = 0; i < n; i++) { const q = base + 2 * i; idx.push(q, q + 1, q + 2, q + 2, q + 1, q + 3); }
      }
    } };
  });
}
