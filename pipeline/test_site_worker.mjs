// Tests for pipeline/site_worker.mjs (the /api/submit route). Turnstile and Discord are stubbed through fetch.
//   node --test pipeline/test_site_worker.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import worker, { pngSize, cleanLink, clean, LIMITS } from "./site_worker.mjs";

const HOST = "https://12tails-wardrobe.jumpthai.workers.dev";
const ENV = { DISCORD_WEBHOOK: "https://discord.test/api/webhooks/1/abc", TURNSTILE_SECRET: "s3cret" };

function png(w, h, extra = 0) {
  const b = new Uint8Array(33 + extra);
  b.set([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0, 0, 0, 13, 73, 72, 68, 82]);
  const dv = new DataView(b.buffer); dv.setUint32(16, w); dv.setUint32(20, h);
  return b;
}
function form(over = {}) {
  const f = new FormData();
  const v = { token: "tok", cls: "sheep", kind: "weapons", item: "halloweenLantern", name: "นักวาด", link: "https://example.com/me", consent: "1", tex0: "Sheep_halloweenWeapon.png", ...over };
  for (const [k, x] of Object.entries(v)) if (x != null) f.append(k, x);
  if (!("skin0" in over)) f.append("skin0", new Blob([png(512, 512)], { type: "image/png" }), "skin.png");
  else if (over.skin0) f.set("skin0", over.skin0, "skin.png");
  return f;
}
const post = (f, headers = {}) => new Request(HOST + "/api/submit", { method: "POST", body: f, headers: { origin: HOST, ...headers } });

function stub({ turnstile = { success: true, hostname: "12tails-wardrobe.jumpthai.workers.dev" }, discord = 200 } = {}) {
  const calls = [];
  globalThis.fetch = async (url, init) => {
    calls.push({ url: String(url), init });
    if (String(url).startsWith("https://challenges.cloudflare.com/")) return new Response(JSON.stringify(turnstile));
    if (String(url).startsWith(ENV.DISCORD_WEBHOOK)) return new Response("{}", { status: discord });
    throw new Error("unexpected fetch " + url);
  };
  return calls;
}

test("a good submission reaches Discord with the skin, plain fields and no mentions", async () => {
  const calls = stub();
  const r = await worker.fetch(post(form()), ENV);
  assert.equal(r.status, 200);
  assert.deepEqual(await r.json(), { ok: true });
  const d = calls.find(c => c.url.startsWith(ENV.DISCORD_WEBHOOK));
  assert.ok(d.url.endsWith("?wait=true"));
  const body = d.init.body, payload = JSON.parse(body.get("payload_json"));
  assert.deepEqual(payload.allowed_mentions, { parse: [] });
  assert.equal(payload.embeds[0].image.url, "attachment://skin0.png");
  const meta = JSON.parse(await body.get("files[1]").text());
  assert.deepEqual([meta.cls, meta.kind, meta.item, meta.name, meta.link], ["sheep", "weapons", "halloweenLantern", "นักวาด", "https://example.com/me"]);
  assert.deepEqual(meta.textures, [{ tex: "Sheep_halloweenWeapon.png", file: "skin0.png", w: 512, h: 512 }]);
  assert.equal((await body.get("files[0]").arrayBuffer()).byteLength, 33);
});

test("secrets piped in from Windows PowerShell (a BOM, a newline) still work", async () => {
  const calls = stub();
  const env = { DISCORD_WEBHOOK: "﻿" + ENV.DISCORD_WEBHOOK + "\r\n", TURNSTILE_SECRET: "﻿" + ENV.TURNSTILE_SECRET + "\r\n" };
  const r = await worker.fetch(post(form()), env);
  assert.equal(r.status, 200);
  assert.equal(calls.find(c => c.url.startsWith("https://challenges")).init.body.get("secret"), ENV.TURNSTILE_SECRET);
  assert.equal(calls.at(-1).url, ENV.DISCORD_WEBHOOK + "?wait=true");
});

test("closed without secrets; other paths 404; GET refused", async () => {
  stub();
  assert.equal((await worker.fetch(post(form()), {})).status, 503);
  assert.equal((await worker.fetch(new Request(HOST + "/nothing"), ENV)).status, 404);
  assert.equal((await worker.fetch(new Request(HOST + "/api/submit"), ENV)).status, 405);
});

test("refusals: another origin, a failed Turnstile, bad fields, not a PNG, too large, Discord down", async () => {
  const code = async (f, opts, headers) => { stub(opts); const r = await worker.fetch(post(f, headers), ENV); return [r.status, (await r.json()).error]; };
  assert.deepEqual(await code(form(), {}, { origin: "https://evil.example" }), [403, "origin"]);
  assert.deepEqual(await code(form(), { turnstile: { success: false } }), [403, "bot"]);
  assert.deepEqual(await code(form({ consent: null })), [400, "consent"]);
  assert.deepEqual(await code(form({ name: "   " })), [400, "name"]);
  assert.deepEqual(await code(form({ link: "javascript:alert(1)" })), [400, "link"]);
  assert.deepEqual(await code(form({ link: "http://plain.example" })), [400, "link"]);
  assert.deepEqual(await code(form({ cls: "dragon" })), [400, "piece"]);
  assert.deepEqual(await code(form({ item: "../../etc" })), [400, "piece"]);
  assert.deepEqual(await code(form({ skin0: new Blob([new Uint8Array(40)]) })), [400, "png"]);
  assert.deepEqual(await code(form({ skin0: new Blob([png(8192, 8)]) })), [400, "png"]);
  assert.deepEqual(await code(form({ skin0: new Blob([png(64, 64, LIMITS.fileBytes)]) })), [400, "big"]);
  assert.deepEqual(await code(form(), { discord: 500 }), [502, "upstream"]);
});

test("an empty link is fine; text is one plain line", async () => {
  const calls = stub();
  const r = await worker.fetch(post(form({ link: "", name: "a\nb\u0007  c" })), ENV);
  assert.equal(r.status, 200);
  const meta = JSON.parse(await calls.at(-1).init.body.get("files[1]").text());
  assert.equal(meta.link, ""); assert.equal(meta.name, "a b c");
  assert.equal(clean("x".repeat(99), LIMITS.name).length, LIMITS.name);
  assert.equal(cleanLink("https://a.example/x?y=1"), "https://a.example/x?y=1");
  assert.equal(pngSize(png(3, 7)).h, 7);
});
