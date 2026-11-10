// Self-check of wardrobe/fxparts/sheep.js without a browser: minimal vector / quaternion stubs stand in for three.js.
// Run: node checks/fx_sheep_build/sheep_parts/check_sheep.mjs (from the repo root, or any folder: the path is resolved
// from this file). Checks the homingLight ball's end on the floor (0.81 s), a level shot's full life (1.7 s), the
// cAttack glow growth (1.6 m) and Eden Sanctuary's clip switch at 12 s and end at 13 s.
import assert from "node:assert/strict";
import { pathToFileURL, fileURLToPath } from "node:url";
import path from "node:path";

class Vec { constructor(x = 0, y = 0, z = 0) { Object.assign(this, { x, y, z }); }
  addScaledVector(v, s) { this.x += v.x * s; this.y += v.y * s; this.z += v.z * s; return this; }
  applyQuaternion(q) {   // three's formula
    const { x, y, z } = this, { x: qx, y: qy, z: qz, w: qw } = q;
    const tx = 2 * (qy * z - qz * y), ty = 2 * (qz * x - qx * z), tz = 2 * (qx * y - qy * x);
    this.x = x + qw * tx + qy * tz - qz * ty; this.y = y + qw * ty + qz * tx - qx * tz; this.z = z + qw * tz + qx * ty - qy * tx;
    return this; } }
const vA = a => new Vec(...a);
const parts = {};
const here = path.dirname(fileURLToPath(import.meta.url));
const mod = await import(pathToFileURL(path.join(here, "../../../wardrobe/fxparts/sheep.js")));
mod.default({ vA, part: (t, b) => { parts[t] = b; } });

const pitchDown = deg => { const h = deg * Math.PI / 360; return { x: Math.sin(h), y: 0, z: 0, w: Math.cos(h) }; };   // Unity Euler x +deg
const run = (type, q, start, comps = [], emitters = []) => {
  const node = { position: new Vec(...start), userData: {} };
  const fx = { name: type, emitters, uQuat: () => q };
  const em = parts[type](fx, node, { type }, null, { comps });
  let t = 0; const dt = 1 / 600;
  while (t < 20) { t += dt; if (em.update(dt) === "destroy") return { t, node }; }
  return { t: Infinity, node };
};

// homingLight aimed at the floor 10 m ahead: fired 1 m up, 0.3 m ahead, pitch atan(1 / 9.7) = 5.89 degrees
const pitch = Math.atan(1 / 9.7) * 180 / Math.PI;
const hit = run("Sheep_homingLight", pitchDown(pitch), [0, 1, 0.3]);
assert.ok(Math.abs(hit.t - Math.hypot(9.7, 1) / 12) < 0.01, `homingLight ends at ${hit.t}`);
assert.ok(Math.abs(hit.node.position.z - 10) < 0.05, `homingLight ends at z ${hit.node.position.z}`);
// a level shot: the code's life 1.7 s, 20.4 m
const level = run("Sheep_homingLight", { x: 0, y: 0, z: 0, w: 1 }, [0, 1, 0.3]);
assert.ok(Math.abs(level.t - 1.7) < 0.01 && Math.abs(level.node.position.z - 0.3 - 20.4) < 0.05, `level ${level.t}`);
// nAttack reads ProjectileControl.velocity
const na = run("Sheep_nAttack", { x: 0, y: 0, z: 0, w: 1 }, [0, 1, 0], [{ type: "ProjectileControl", velocity: [0, 0, 12] }]);
assert.ok(Math.abs(na.node.position.z - 20.4) < 0.05);
// cAttack: 5 s level (40 m), its root emitter grown by 1.6 m once
let grown = 0;
const ca = run("Sheep_cAttack", { x: 0, y: 0, z: 0, w: 1 }, [0, 3, 0], [], [{ node: null, addSize: a => { grown += a; } }]);
assert.equal(grown, 0, "only the node's own emitter grows");
let mine = 0; const node = { position: new Vec(0, 3, 0), userData: {} };
parts.Sheep_cAttack({ name: "cAttack", uQuat: () => ({ x: 0, y: 0, z: 0, w: 1 }), emitters: [{ node, addSize: a => { mine += a; } }] }, node, { type: "Sheep_cAttack" }, null, { comps: [] });
assert.equal(mine, 1.6);
assert.ok(Math.abs(ca.t - 5) < 0.01 && Math.abs(ca.node.position.z - 40) < 0.05);

// Eden Sanctuary: play("destroy") once just past 12 s, gone 1 s later
const played = [], en = { userData: { fxAnim: { play: n => played.push([n, tt]) } } };
const ed = parts.Sheep_edenSanctuary({ name: "edenSanctuary" }, en);
let tt = 0, end = null;
while (tt < 20 && end == null) { tt += 1 / 60; if (ed.update(1 / 60) === "destroy") end = tt; }
assert.equal(played.length, 1); assert.equal(played[0][0], "destroy");
assert.ok(played[0][1] > 12 && played[0][1] < 12.02 && Math.abs(end - 13) < 0.04, `eden ${played[0][1]} ${end}`);
console.log("OK", { homingLight: +hit.t.toFixed(3), level: +level.t.toFixed(3), cAttack: +ca.t.toFixed(3), edenSwitch: +played[0][1].toFixed(3), edenEnd: +end.toFixed(3) });
