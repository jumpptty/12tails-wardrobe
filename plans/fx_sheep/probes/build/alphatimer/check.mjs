// node checks/fx_sheep_build/alphatimer/check.mjs: AlphaTimer's curve (Eden's 0 / 1 / 11 / 1, max 0.5, tint -> 2a) and
// the Animation part's play(name, fade) with a stub THREE (no browser). Exits non-zero on a failure.
import assert from "node:assert/strict";
const dir = new URL("../../../wardrobe/fxparts/", import.meta.url);
class V3 { constructor(x = 0, y = 0, z = 0) { Object.assign(this, { x, y, z }); }
  fromArray(a) { [this.x, this.y, this.z] = a; return this; } clone() { return new V3(this.x, this.y, this.z); }
  lerpVectors(a, b, w) { for (const k of "xyz") this[k] = a[k] + (b[k] - a[k]) * w; return this; } }
class Q { constructor() { this.v = [0, 0, 0, 1]; } fromArray(a) { this.v = a.slice(); return this; } normalize() { return this; }
  clone() { return new Q().fromArray(this.v); } copy(q) { this.v = q.v.slice(); return this; }
  slerp(q, w) { this.v = this.v.map((x, i) => x + (q.v[i] - x) * w); return this; } }
const node = () => ({ position: new V3(), scale: new V3(1, 1, 1), quaternion: new Q(), children: [], userData: {}, updateMatrixWorld() {} });
const parts = {};
const lin = (keys, n, t) => { const [a, b] = keys; const u = Math.min(1, Math.max(0, (t - a[0]) / (b[0] - a[0]))); return a.slice(1, 1 + n).map((x, i) => x + (b[1 + i] - x) * u); };
const api = { THREE: { Quaternion: Q }, hermite: lin, part: (t, b) => { parts[t] = b; } };
for (const f of ["alphatimer.js", "mesh.js"]) (await import(new URL(f, dir).href)).default(api);

// AlphaTimer on an additive mesh (Eden: Min 0, Max 0.5, 0 / 1 / 11 / 1)
const n = node(), mat = { userData: { fxBlend: "add" }, opacity: 0, clone() { return { ...this, userData: { ...this.userData } }; } };
const mesh = { isMesh: true, material: [mat] }; n.children.push(mesh);
const fx = { alive: true, nodes: [node(), node()] };
const at = parts.AlphaTimer(fx, n, { MinAlpha: 0, MaxAlpha: 0.5, FadeDelay: 0, FadeEaseIn: 1, FadeMiddle: 11, FadeEaseOut: 1 }, null, {});
const step = (dt, k = 1) => { for (let i = 0; i < k; i++) at.update(dt); return mesh.material[0].opacity; };
assert.ok(Math.abs(step(0.5) - 0.5) < 1e-9, "half way in: alpha 0.25 -> opacity 0.5");
assert.notEqual(mesh.material[0], mat, "the shared material is cloned");
assert.equal(mat.opacity, 0, "the shared material is left alone");
assert.ok(Math.abs(step(0.5, 2) - 1) < 1e-9, "the hold: alpha 0.5 -> opacity 1");
assert.ok(Math.abs(step(1, 11) - 0.5) < 1e-9, "12.5 s: half way out");
assert.equal(step(1), 0, "after 13 s: MinAlpha");

// Animation: auto-plays create, play("destroy", 0.2) cross-fades from the held pose
const clip = y0 => ({ len: 1, tracks: { 1: { p: [[0, 0, y0, 0], [1, 0, y0 === 0 ? -10 : 0, 0]] } } });
const root = fx.nodes[0], o = fx.nodes[1];
const an = parts.Animation(fx, root, { play: true, clip: "create", wrap: 0, clips: { create: clip(-10), destroy: clip(0) } });
assert.equal(root.userData.fxAnim, an);
an.update(0.5); assert.equal(o.position.y, -5);
an.update(0.5); assert.equal(o.position.y, 0);
an.update(11);
an.play("destroy", 0.2); assert.equal(o.position.y, 0, "cross-fade weight 0 at the call");
an.update(0.1); assert.ok(Math.abs(o.position.y - 0.5 * -1) < 1e-9, "weight 0.5 of destroy's -1 at 0.1 s");
an.play("destroy"); assert.ok(Math.abs(o.position.y - 0.5 * -1) < 1e-9, "a playing clip is not rewound");
an.update(0.9); assert.equal(o.position.y, -10);
an.play("create"); assert.equal(o.position.y, -10, "an ended clip plays again from its start (a cut)");
an.update(0.5); assert.equal(o.position.y, -5);
assert.equal(an.play("nope"), false);
console.log("OK");
