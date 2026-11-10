// Node check of wardrobe/fxparts/tto_sheep.js + shuriken.js on the Sheep's probed data (no browser): builds the parts on
// a stub of index.html's Fx and runs them, asserting the game's numbers.
// usage: node checks/fx_sheep_build/tto/parts_check.mjs <three.module.js> <probe2.json>
import { pathToFileURL } from "url";
import fs from "fs";
const [threePath, probePath] = process.argv.slice(2);
const THREE = await import(pathToFileURL(threePath).href);
const sheep = (await import(pathToFileURL("wardrobe/fxparts/tto_sheep.js").href)).default;
const shur = (await import(pathToFileURL("wardrobe/fxparts/shuriken.js").href)).default;
const data = JSON.parse(fs.readFileSync(probePath, "utf8"));
const V = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);
const PARTS = {}, SH = {};
const camera = new THREE.PerspectiveCamera(40, 1, 0.1, 100); camera.position.set(3, 2, 8); camera.lookAt(0, 1, 0); camera.updateMatrixWorld();
const fxMesh = (p, m) => { const o = new THREE.Mesh(new THREE.BufferGeometry(), m); p.add(o); return o; };
const setMesh = (m, pos, col, uv, idx) => { const g = m.geometry; g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute("color", new THREE.Float32BufferAttribute(col, 4)); g.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2)); g.setIndex(idx); };
const mats = {};
const api = { THREE, V, part: (t, b) => { PARTS[t] = b; }, shader: (n, mk) => { SH[n] = mk; }, camera, fxMesh, setMesh,
  texLoader: { load: () => new THREE.Texture() }, DATA: "", fxMaterial: (cls, n, d) => (mats[n] ||= SH[d.blend] ? SH[d.blend](d, n, cls) : new THREE.MeshBasicMaterial()) };
shur(api); sheep(api);
const assert = (c, m) => { if (!c) { console.error("FAIL", m); process.exitCode = 1; } else console.log("ok  ", m); };
for (const b of ["shader:TTO/Sheep/Celestial Ring", "shader:TTO/Sheep/Celestial Ray", "shader:TTO/Sheep/Prism Veil", "shader:Standard", "shader:Particles/Standard Unlit"])
  assert(SH[b], "shader hook " + b);
for (const [n, d] of Object.entries(data.materials)) if (SH[d.blend]) assert(SH[d.blend](d, n, "sheep"), "material " + n);

// a minimal Fx (index.html's constructor and update loop)
function makeFx(name, at) {
  const def = data.effects[name], fx = { cls: "sheep", name, at, emitters: [], age: 0 };
  fx.group = new THREE.Group(); fx.mirror = new THREE.Group(); fx.mirror.scale.set(-1, 1, 1); fx.group.add(fx.mirror);
  fx.nodes = def.nodes.map(() => new THREE.Object3D());
  fx.uMatrix = o => fx.mirrorInv.clone().multiply(o.matrixWorld);
  fx.uQuat = o => { const q = new THREE.Quaternion(); for (; o && o !== fx.mirror; o = o.parent) q.premultiply(o.quaternion); return q; };
  fx.uDir = v => v.clone().transformDirection(fx.mirrorInv);
  def.nodes.forEach((n, i) => {
    const o = fx.nodes[i]; o.name = n.name;
    if (n.parent < 0) { o.position.set(at.x || 0, at.y || 0, at.d || 0); if (at.rot) o.quaternion.setFromEuler(new THREE.Euler(...at.rot.map(v => v * Math.PI / 180), "YXZ")); fx.mirror.add(o); }
    else { o.position.fromArray(n.pos); o.quaternion.fromArray(n.rot); o.scale.fromArray(n.scale); fx.nodes[n.parent].add(o); }
    const mat = n.mats?.[0] ? api.fxMaterial("sheep", n.mats[0], data.materials[n.mats[0]]) : null;
    for (const c of n.comps) if (PARTS[c.type]) { const e = PARTS[c.type](fx, o, c, mat, n, data); if (e) fx.emitters.push(e); }
  });
  fx.root = fx.nodes[0]; fx.group.updateMatrixWorld(true); fx.alive = true;
  return fx;
}
function step(fx, dt) {
  fx.age += dt; fx.group.updateMatrixWorld(true); fx.mirrorInv = fx.mirror.matrixWorld.clone().invert();
  const cam = { right: fx.uDir(V(1, 0, 0).applyQuaternion(camera.quaternion)), up: fx.uDir(V(0, 1, 0).applyQuaternion(camera.quaternion)), fwd: fx.uDir(V(0, 0, -1).applyQuaternion(camera.quaternion)) };
  for (const e of fx.emitters) if (e.update(dt, cam) === "destroy" && e.node === fx.root) { fx.alive = false; return; }
}
const run = (fx, T, dt = 1 / 60, each) => { for (let t = 0; t < T && fx.alive; t += dt) { step(fx, dt); each?.(fx); } return fx; };

// the wisp: mouth (0.35 ahead, 1.21 up) -> the ally's chest 10 m ahead (0.8 up): flight 0.6 s, gone 0.3 s later
{
  const fx = makeFx("tto/gleamingBreath_wisp", { d: 0.35, y: 1.21, to: [0, 0.8, 10] });
  let peak = 0, gone = null;
  run(fx, 2, 1 / 60, f => { peak = Math.max(peak, f.root.position.y - (1.21 + (0.8 - 1.21) * Math.min(1, f.age / 0.6))); if (!f.alive && gone == null) gone = f.age; });
  assert(Math.abs(peak - 0.225) < 0.01, `wisp arc peak ${peak.toFixed(3)} (0.225)`);
  assert(!fx.alive && Math.abs(fx.age - 0.9) < 0.05, `wisp destroyed at ${fx.age.toFixed(3)} (0.6 + 0.3)`);
  const tr = fx.emitters.filter(e => e.node.name.startsWith("Trail"));
  assert(tr.length === 2, "wisp has its two TrailRendererModern parts");
}
// the beam: hand (0.49 ahead, 1.12 up) -> her own chest (0, 0.8, 0)
{
  const fx = makeFx("tto/lucentBarrier_beam", { d: 0.49, y: 1.12, rot: [33, 180, 0], to: [0, 0.8, 0] });
  const line = fx.emitters.find(e => e.line);
  run(fx, 0.04);
  const mid = line.pts[1].clone();
  run(fx, 0.06);
  assert(mid.distanceTo(V(0, 0.8, 0)) > 0.2 && line.pts[1].distanceTo(V(0, 0.8, 0)) < 1e-6, "beam head halfway at 0.04 s, at the chest after travel 0.08");
  run(fx, 1);
  assert(!fx.alive && Math.abs(fx.age - 0.45) < 0.03, `beam destroyed at ${fx.age.toFixed(3)} (life 0.4 + 0.05)`);
}
// the book: hover 10 m ahead at 2.6 m; at 0.6 s it sits 2.6 + 0.12 sin(1.32); destroyed 20.1 s after spawn
{
  const fx = makeFx("tto/grandCodex_book", { d: 10, y: 2.6, rot: [-35, 0, 0] });
  const flip = fx.nodes.find(o => o.name === "FlipPivot");
  let y06 = null, maxFlip = 0;
  run(fx, 25, 1 / 60, f => { if (y06 == null && f.age >= 0.6) y06 = f.root.position.y; if (f.age > 1.6 && f.age < 2) maxFlip = Math.max(maxFlip, 2 * Math.acos(Math.min(1, Math.abs(flip.quaternion.w)))); });
  assert(Math.abs(y06 - (2.6 + 0.12 * Math.sin(2.2 * 0.6))) < 0.02, `book height at 0.6 s ${y06.toFixed(3)}`);
  assert(maxFlip > 2.9, `page turns before the first read (${(maxFlip * 180 / Math.PI).toFixed(0)} deg)`);
  assert(!fx.alive && Math.abs(fx.age - 20.1) < 0.05, `book destroyed at ${fx.age.toFixed(2)} (20.1)`);
}
// every Sheep TTO effect builds and runs 3 s without throwing (shuriken mesh particles, collision, lines)
for (const name of Object.keys(data.effects)) {
  try { const fx = makeFx(name, { d: 1, y: 1, to: [0, 0.8, 5] }); run(fx, 3); console.log("ok   runs", name, fx.emitters.length, "parts"); }
  catch (e) { console.error("FAIL", name, e.stack); process.exitCode = 1; }
}
