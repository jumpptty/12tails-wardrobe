// Tests for pipeline/site_worker.mjs (the /api/submit route). Turnstile and Discord are stubbed through fetch.
//   node --test pipeline/test_site_worker.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import worker, { pngSize, cleanLink, clean, LIMITS, META_TAG } from "./site_worker.mjs";

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
  assert.deepEqual([meta.v, meta.cls, meta.name, meta.link, meta.face], [2, "sheep", "นักวาด", "https://example.com/me", null]);
  assert.deepEqual(meta.pieces, [{ slot: "R", kind: "weapons", item: "halloweenLantern",
    textures: [{ tex: "Sheep_halloweenWeapon.png", file: "skin0.png", w: 512, h: 512 }] }]);       // the first format reads as one piece
  assert.deepEqual(JSON.parse(payload.embeds[0].footer.text.slice(META_TAG.length)), meta);   // the live list reads this
  assert.ok(payload.embeds[0].footer.text.length <= 2048);
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

test("community: the ✅ webhook messages, live; a picture only while approved; errors let the page fall back", async () => {
  const env = { ...ENV, DISCORD_BOT_TOKEN: "﻿bot\r\n", DISCORD_CHANNEL: "42" };
  const cdn = n => `https://cdn.discordapp.com/attachments/42/${n}?ex=1&is=2&hm=3`;
  const msg = (id, ok, extra = {}) => ({ id, webhook_id: ok === null ? undefined : "9", timestamp: "2026-11-12T00:00:0" + id.slice(-1) + "Z",
    reactions: ok ? [{ emoji: { name: "✅" }, count: 1 }] : [], attachments: [{ filename: "meta.json", url: cdn(id + "/meta.json") }],
    embeds: [{ image: { url: cdn(id + "/skin0.png") } }], ...extra });
  const metaOf = id => ({ v: 1, cls: "sheep", kind: "weapons", item: "mothLatern", name: "คนวาด" + id, link: "", at: "2026-11-12T00:00:0" + id.slice(-1) + "Z",
    textures: [{ tex: "Sheep_mothLantern.png", file: "skin0.png", w: 128, h: 128 }] });
  // 104: a message since the footer meta (no meta.json download needed); 101: an older one (its meta.json)
  const withFooter = msg("104", true, { attachments: [] });
  withFooter.embeds[0].footer = { text: META_TAG + JSON.stringify(metaOf("104")) };
  // 105: a whole look (v2): two pieces, its footer meta, a preview picture; the embed's picture is the preview
  const look = msg("105", true, { attachments: [{ filename: "skin0.png", url: cdn("105/skin0.png") }, { filename: "skin1.png", url: cdn("105/skin1.png") }],
    embeds: [{ image: { url: cdn("105/preview.jpg") }, footer: { text: META_TAG + JSON.stringify({ v: 2, cls: "cat", name: "ผู้ส่งชุด", link: "https://x.example/a", face: 38, at: "2026-11-12T00:00:05Z",
      pieces: [{ slot: "outfit", kind: "outfits", item: "champion", textures: [{ tex: "", file: "skin0.png", w: 128, h: 128 }] },
        { slot: "Head", kind: "accessories", item: "default", textures: [{ tex: "Cat_default.png", file: "skin1.png", w: 32, h: 32 }] }] }) } }] });
  let messages = [look, withFooter, msg("101", true), msg("102", false), msg("103", null)], discordStatus = 200;
  const calls = [];
  globalThis.fetch = async (url, init) => {
    url = String(url); calls.push({ url, init });
    if (url.startsWith("https://discord.com/api/v10/channels/42/messages")) return new Response(JSON.stringify(messages), { status: discordStatus });
    if (url.includes("/preview.jpg")) return new Response(JPEG, { headers: { "content-type": "image/jpeg" } });
    const m = url.match(/attachments\/42\/(\d+)\/(meta\.json|skin\d\.png)/);
    if (m && m[2] === "meta.json") return new Response(JSON.stringify(metaOf(m[1])));
    if (m) return new Response(png(128, 128));
    throw new Error("unexpected fetch " + url);
  };
  const get = p => worker.fetch(new Request(HOST + p), env);
  const r = await get("/api/community");
  assert.equal(r.status, 200);
  const { sets } = await r.json();
  // the first format's skins read as sets of one (slot from the kind, no preview, no face)
  const row = id => ({ id, cls: "sheep", name: "คนวาด" + id, link: "", at: "2026-11-12T00:00:0" + id.slice(-1) + "Z", face: null, thumb: null,
    pieces: [{ slot: "R", kind: "weapons", item: "mothLatern", tex: { "Sheep_mothLantern.png": `api/community/${id}/0.png` } }] });
  assert.deepEqual(sets, [row("101"), row("104"), { id: "105", cls: "cat", name: "ผู้ส่งชุด", link: "https://x.example/a", at: "2026-11-12T00:00:05Z", face: 38,
    thumb: "api/community/105/preview", pieces: [{ slot: "outfit", kind: "outfits", item: "champion", tex: { "": "api/community/105/0.png" } },
      { slot: "Head", kind: "accessories", item: "default", tex: { "Cat_default.png": "api/community/105/1.png" } }] }]);   // no ✅, no webhook: left out; oldest first; no Discord URL leaks
  assert.equal(calls[0].init.headers.authorization, "Bot bot");
  assert.deepEqual(calls.filter(c => c.url.includes("meta.json")).map(c => c.url.split("/42/")[1].split("/")[0]), ["101"]);   // 104 and 105 read from their footers
  const img = await get("/api/community/101/0.png");
  assert.equal(img.headers.get("content-type"), "image/png");
  assert.equal(new Uint8Array(await img.arrayBuffer()).length, 33);
  assert.equal((await get("/api/community/105/1.png")).status, 200);              // the second piece's texture
  const pv = await get("/api/community/105/preview");
  assert.equal(pv.headers.get("content-type"), "image/jpeg");
  assert.equal((await get("/api/community/101/preview")).status, 404);            // no preview there
  assert.equal((await get("/api/community/102/0.png")).status, 404);              // not approved: no picture
  messages = [msg("101", false)];                                                  // the ✅ taken away
  assert.deepEqual((await (await get("/api/community")).json()).sets, []);
  assert.equal((await get("/api/community/105/preview")).status, 404);
  assert.equal((await get("/api/community/101/0.png")).status, 404);
  discordStatus = 500;
  assert.equal((await get("/api/community")).status, 502);
  assert.equal((await worker.fetch(new Request(HOST + "/api/community"), ENV)).status, 503);   // no bot secrets yet
});

// a whole look (2026-11-12): the pieces JSON, the textures in form fields f0.., a preview picture, a face
function setForm(pieces, extra = {}) {
  const f = new FormData();
  let n = 0;
  const defs = pieces.map(p => ({ slot: p.slot, kind: p.kind, item: p.item, textures: p.texs.map(t => { const field = "f" + n++; f.append(field, new Blob([png(t.size || 64, t.size || 64)], { type: "image/png" }), field + ".png"); return { tex: t.tex, field }; }) }));
  f.append("pieces", JSON.stringify(defs));
  for (const [k, v] of Object.entries({ token: "tok", cls: "cat", name: "นักวาด", link: "", consent: "1", face: "38", ...extra })) if (v != null) f.append(k, v);
  return f;
}
const LOOK = [{ slot: "outfit", kind: "outfits", item: "champion", texs: [{ tex: "", size: 128 }] },
  { slot: "Head", kind: "accessories", item: "default", texs: [{ tex: "Cat_default.png", size: 32 }] }];
const JPEG = new Uint8Array([0xff, 0xd8, 0xff, 0xe0, 0, 16, 0x4a, 0x46, 0x49, 0x46, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0]);

test("a whole look: every piece, the face and the preview reach Discord as one message", async () => {
  const calls = stub();
  const f = setForm(LOOK, {}); f.append("preview", new Blob([JPEG], { type: "image/jpeg" }), "preview.jpg");
  const r = await worker.fetch(post(f), ENV);
  assert.equal(r.status, 200);
  const body = calls.find(c => c.url.startsWith(ENV.DISCORD_WEBHOOK)).init.body, payload = JSON.parse(body.get("payload_json"));
  const meta = JSON.parse(await body.get("files[3]").text());                  // skin0, skin1, the preview, meta.json
  assert.deepEqual(meta.pieces.map(p => [p.slot, p.item, p.textures.map(t => t.file)]), [["outfit", "champion", ["skin0.png"]], ["Head", "default", ["skin1.png"]]]);
  assert.equal(meta.face, 38);
  assert.equal(payload.embeds[0].image.url, "attachment://preview.jpg");       // the preview is the picture, not the first skin
  assert.equal(body.get("files[2]").type, "image/jpeg");
  assert.deepEqual(payload.attachments.map(a => a.filename), ["skin0.png", "skin1.png", "preview.jpg", "meta.json"]);
  assert.ok(payload.content.includes("2 ชิ้น"));
  assert.deepEqual(JSON.parse(payload.embeds[0].footer.text.slice(META_TAG.length)), meta);
});

test("ชื่อผลงาน: one plain line, cut at its limit, in the meta, the message and the live list", async () => {
  const calls = stub();
  const r = await worker.fetch(post(setForm(LOOK, { title: " อัศวิน\nแมว  " + "x".repeat(99) })), ENV);
  assert.equal(r.status, 200);
  const body = calls.find(c => c.url.startsWith(ENV.DISCORD_WEBHOOK)).init.body, payload = JSON.parse(body.get("payload_json"));
  const meta = JSON.parse(await body.get("files[2]").text());
  assert.ok(meta.title.startsWith("อัศวิน แมว x")); assert.equal(meta.title.length, LIMITS.title);
  assert.ok(payload.embeds[0].title.startsWith(meta.title + " · "));
  assert.equal(payload.embeds[0].fields.find(f => f.name === "ชื่อผลงาน").value, meta.title);
  const env = { ...ENV, DISCORD_BOT_TOKEN: "bot", DISCORD_CHANNEL: "43" };
  globalThis.fetch = async url => (String(url).startsWith("https://discord.com/") ? new Response(JSON.stringify([{ id: "201", webhook_id: "9",
    timestamp: "2026-11-13T00:00:00Z", reactions: [{ emoji: { name: "✅" } }], attachments: [{ filename: "skin0.png", url: "https://cdn.discordapp.com/attachments/43/201/skin0.png" }],
    embeds: [{ footer: { text: payload.embeds[0].footer.text } }] }])) : new Response("{}"));
  const { sets } = await (await worker.fetch(new Request(HOST + "/api/community"), env)).json();
  assert.equal(sets[0].title, meta.title);
});

test("a look is refused when it is too big, doubled, mis-slotted or its preview is not a picture", async () => {
  const code = async f => { stub(); const r = await worker.fetch(post(f), ENV); return [r.status, (await r.json()).error]; };
  const many = Array.from({ length: LIMITS.pieces + 1 }, (_, i) => ({ slot: "R", kind: "weapons", item: "w" + i, texs: [{ tex: "a.png" }] }));
  assert.deepEqual(await code(setForm(many)), [400, "piece"]);
  assert.deepEqual(await code(setForm([LOOK[0], LOOK[0]])), [400, "piece"]);                         // the same piece twice
  assert.deepEqual(await code(setForm([{ ...LOOK[1], slot: "R" }])), [400, "piece"]);                // a hat in the weapon slot
  assert.deepEqual(await code(setForm([{ ...LOOK[0], texs: [{ tex: "", size: 64 }, { tex: "b.png" }, { tex: "c.png" }] }])), [400, "piece"]);   // 3 textures
  const bad = setForm(LOOK); bad.append("preview", new Blob([new Uint8Array(30)]), "x.jpg");
  assert.deepEqual(await code(bad), [400, "png"]);
  assert.deepEqual(await code(setForm(LOOK, { face: "-3" })), [400, "piece"]);
  const files = Array.from({ length: 5 }, (_, i) => ({ slot: i ? "R" : "outfit", kind: i ? "weapons" : "outfits", item: "x" + i, texs: [{ tex: "a.png" }, { tex: "b.png" }] }));
  assert.deepEqual(await code(setForm(files.slice(0, 5))), [400, "big"]);                            // 10 files: over the 8
  // each file under 4 MB, the sum over 9 MB: a 3.2 MB PNG (a header + padding) x 3
  const pad = (w, extra) => { const b = new Uint8Array(33 + extra); b.set(png(w, w)); return b; };
  const bigForm = setForm([{ slot: "outfit", kind: "outfits", item: "a", texs: [{ tex: "" }] }]);
  const fat = new FormData();
  const defs = [0, 1, 2].map(i => ({ slot: ["outfit", "R", "L"][i], kind: i ? "weapons" : "outfits", item: "p" + i, textures: [{ tex: "", field: "f" + i }] }));
  defs.forEach((d, i) => fat.append("f" + i, new Blob([pad(64, 3.2 * 1024 * 1024)], { type: "image/png" }), "f.png"));
  for (const [k, v] of Object.entries({ pieces: JSON.stringify(defs), token: "tok", cls: "cat", name: "x", consent: "1" })) fat.append(k, v);
  assert.deepEqual(await code(fat), [400, "big"]);});

test("an empty link is fine; text is one plain line", async () => {
  const calls = stub();
  const r = await worker.fetch(post(form({ link: "", name: "a\nb\u0007  c" })), ENV);
  assert.equal(r.status, 200);
  const meta = JSON.parse(await calls.at(-1).init.body.get("files[1]").text());
  assert.equal(meta.link, ""); assert.equal(meta.name, "a b c"); assert.equal(meta.title, "");   // ชื่อผลงาน is optional
  assert.equal(clean("x".repeat(99), LIMITS.name).length, LIMITS.name);
  assert.equal(cleanLink("https://a.example/x?y=1"), "https://a.example/x?y=1");
  assert.equal(pngSize(png(3, 7)).h, 7);
});
