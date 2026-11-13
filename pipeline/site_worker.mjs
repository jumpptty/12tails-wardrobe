// The public wardrobe's Worker (2026-11-11, community skins; NOTES.md "community skins"). The static copy
// (wardrobe_dist) is served as the Worker's assets; Cloudflare answers every request a file matches and runs this only
// for the rest: POST /api/submit, a visitor's own skin for one piece, checked and posted to a private Discord channel
// through a webhook, where the user approves it with a ✅; GET /api/community, the approved ones read live from that
// channel (below; pipeline/wardrobe_community.py is the PC's import into the data, the fallback). Deploy (from an empty
// folder, NOTES.md "Online copy"):
//   npx wrangler deploy D:/12tails-wardrobe/pipeline/site_worker.mjs --assets D:/12tails-wardrobe/wardrobe_dist
//     --name 12tails-wardrobe --compatibility-date 2026-11-07
// Secrets (the user sets them once: npx wrangler secret put <NAME> --name 12tails-wardrobe):
//   DISCORD_WEBHOOK   the channel's webhook URL            TURNSTILE_SECRET   the Turnstile widget's secret key
//   DISCORD_BOT_TOKEN the bot's token (reads the channel)  DISCORD_CHANNEL    the channel's id
// Without them a route answers 503 (the page hides the send action until it has a Turnstile site key).
// Nothing is stored here: no IP address or picture is kept or sent on, only what the visitor typed and the skin.

const CLASSES = { bat: "ค้างคาว", bison: "ไบซัน", cat: "แมว", chameleon: "กิ้งก่า", mole: "ตุ่น", monkey: "ลิง", panda: "แพนด้า",
  penguin: "เพนกวิน", rabbit: "กระต่าย", sheep: "แกะ", whale: "วาฬ", wolf: "หมาป่า" };
const KINDS = { outfits: "ชุด", weapons: "อาวุธ", accessories: "หมวก", trinkets: "ประดับหลัง" };
// a submission is a whole look (2026-11-12, "one-click change the whole sets"): up to 6 pieces, 8 texture files in all
// (Discord takes 10 attachments a message: the files + the preview + meta.json), their sum <= 9 MB (Discord's per-message
// limit is believed to be 10 MB: unverified, a 502 "upstream" is what too much looks like) and a small preview picture
export const LIMITS = { files: 8, pieces: 6, perPiece: 2, fileBytes: 4 << 20, setBytes: 9 << 20, previewBytes: 400 << 10, bodyBytes: 10 << 20,
  side: 4096, name: 40, title: 60, link: 200, perWindow: 5, windowSec: 600 };
const SLOT_KIND = { outfit: "outfits", R: "weapons", L: "weapons", Head: "accessories", Back: "trinkets" };
const DEFAULT_SLOT = { outfits: "outfit", weapons: "R", accessories: "Head", trinkets: "Back" };
const NAME_OK = /^[A-Za-z0-9_ .-]{1,64}$/, TEX_OK = /^[A-Za-z0-9_ .-]{0,80}$/;
const PNG = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

const json = (obj, status = 200) => new Response(JSON.stringify(obj), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });
const fail = (code, status = 400) => json({ ok: false, error: code }, status);

// a PNG's size from its IHDR, or null when the bytes are not a PNG
export function pngSize(b) {
  if (b.length < 24 || PNG.some((v, i) => b[i] !== v) || String.fromCharCode(...b.subarray(12, 16)) !== "IHDR") return null;
  const dv = new DataView(b.buffer, b.byteOffset, b.byteLength);
  return { w: dv.getUint32(16), h: dv.getUint32(20) };
}

// one line of plain text: control characters and Discord's mention / markdown triggers neutralised
export const clean = (s, max) => String(s ?? "").replace(/[\u0000-\u001f\u007f]/g, " ").replace(/\s+/g, " ").trim().slice(0, max);
export function cleanLink(s) {
  const t = clean(s, LIMITS.link);
  if (!t) return "";
  try { const u = new URL(t); return u.protocol === "https:" ? u.href : null; } catch { return null; }
}

// the pieces the form names: the `pieces` JSON [{slot, kind, item, textures: [{tex, field}]}] (a texture's file is the form
// field `field`), or the first format's single piece (kind, item, tex0 / skin0, tex1 / skin1) from a page not reloaded yet
function pieceDefs(form) {
  if (!form.has("pieces")) {
    return [{ kind: String(form.get("kind") || ""), item: String(form.get("item") || ""),
      textures: [0, 1].map(i => ({ tex: String(form.get("tex" + i) ?? ""), field: "skin" + i })) }];
  }
  try { const d = JSON.parse(String(form.get("pieces"))); return Array.isArray(d) ? d : null; } catch { return null; }
}
const jpegOrPng = b => (pngSize(b) ? "png" : b.length > 3 && b[0] === 0xff && b[1] === 0xd8 && b[2] === 0xff ? "jpg" : null);

// the form's fields -> the submission, or an error code (the page shows each in Thai)
export async function readSubmission(form) {
  const cls = String(form.get("cls") || "");
  if (!(cls in CLASSES) && cls !== "all") return { error: "piece" };
  const defs = pieceDefs(form);
  if (!defs || !defs.length || defs.length > LIMITS.pieces) return { error: "piece" };
  const seen = new Set();
  for (const d of defs) {                                                          // the names first, the files after
    if (!d || !(d.kind in KINDS) || !NAME_OK.test(String(d.item)) || !Array.isArray(d.textures) || d.textures.length > LIMITS.perPiece) return { error: "piece" };
    if (d.slot != null && SLOT_KIND[d.slot] !== d.kind) return { error: "piece" };
    const key = (d.slot || DEFAULT_SLOT[d.kind]) + "|" + d.item;
    if (seen.has(key)) return { error: "piece" };
    seen.add(key);
  }
  const face = form.has("face") && form.get("face") !== "" ? Number(form.get("face")) : null;
  if (face !== null && !(Number.isInteger(face) && face >= 0 && face < 200)) return { error: "piece" };
  if (form.get("consent") !== "1") return { error: "consent" };
  // ชื่อผลงาน, the work's own title (user 2026-11-13), optional
  const name = clean(form.get("name"), LIMITS.name), title = clean(form.get("title"), LIMITS.title), link = cleanLink(form.get("link"));
  if (!name) return { error: "name" };
  if (link === null) return { error: "link" };
  const pieces = [];
  let files = 0, total = 0;
  for (const d of defs) {
    const textures = [];
    for (const t of d.textures) {
      const f = form.get(String(t?.field));
      if (!f || typeof f === "string") continue;
      const tex = String(t.tex ?? "");
      if (!TEX_OK.test(tex)) return { error: "piece" };
      if (f.size > LIMITS.fileBytes) return { error: "big" };
      const bytes = new Uint8Array(await f.arrayBuffer()), size = pngSize(bytes);
      if (!size || !size.w || !size.h || size.w > LIMITS.side || size.h > LIMITS.side) return { error: "png" };
      if (++files > LIMITS.files || (total += bytes.length) > LIMITS.setBytes) return { error: "big" };
      textures.push({ tex, bytes, ...size });
    }
    if (!textures.length) return { error: "png" };
    pieces.push({ slot: d.slot || DEFAULT_SLOT[d.kind], kind: d.kind, item: String(d.item), textures });
  }
  let preview = null;
  const pv = form.get("preview");
  if (pv && typeof pv !== "string") {                                              // the whole character, a small picture
    if (pv.size > LIMITS.previewBytes) return { error: "big" };
    const bytes = new Uint8Array(await pv.arrayBuffer()), ext = jpegOrPng(bytes);
    if (!ext) return { error: "png" };
    preview = { bytes, ext };
  }
  return { cls, name, title, link, face, preview, pieces };
}

// the token is Cloudflare's to judge; the site key is limited to the site's hostname in the Turnstile dashboard
async function turnstileOk(secret, token, ip) {
  if (!token) return false;
  const body = new FormData();
  body.append("secret", secret); body.append("response", String(token));
  if (ip) body.append("remoteip", ip);
  const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body });
  const v = r.ok ? await r.json() : {};
  return !!v.success;
}

// a few sends per visitor per window, counted in the data centre's cache (rough on purpose: Turnstile is the real gate)
async function overLimit(ip) {
  if (!ip || typeof caches === "undefined") return false;
  const key = new Request(`https://rate.wardrobe.invalid/${encodeURIComponent(ip)}`), c = caches.default;
  const hit = await c.match(key), n = hit ? (Number(await hit.text()) || 0) : 0;
  if (n >= LIMITS.perWindow) return true;
  await c.put(key, new Response(String(n + 1), { headers: { "cache-control": `max-age=${LIMITS.windowSec}` } }));
  return false;
}

// the Discord message: the skin as the embed's picture, every field as plain text, no mention can ping anyone, and a
// meta.json the import reads (wardrobe_community.py), so nothing has to be parsed out of the message text
export function discordBody(s, at) {
  let n = 0;                                                                       // skin<n>.png: one running number over every piece
  const meta = { v: 2, cls: s.cls, name: s.name, title: s.title || "", link: s.link, face: s.face, at,
    pieces: s.pieces.map(p => ({ slot: p.slot, kind: p.kind, item: p.item,
      textures: p.textures.map(t => ({ tex: t.tex, file: `skin${n++}.png`, w: t.w, h: t.h })) })) };
  const flat = s.pieces.flatMap(p => p.textures), pv = s.preview ? `preview.${s.preview.ext}` : null;
  const fields = [
    { name: "ตัวละคร", value: s.cls === "all" ? "ทุกอาชีพ" : CLASSES[s.cls], inline: true },
    { name: "ชื่อผลงาน", value: s.title || "-", inline: true },
    { name: "ลายโดย", value: s.name, inline: true },
    { name: "ลิงก์", value: s.link || "-", inline: true },
    { name: "ชิ้น", value: s.pieces.map(p => `${KINDS[p.kind]}: ${p.item}`).join("\n"), inline: false },
    { name: "ขนาด", value: flat.map(t => `${t.w}×${t.h}`).join(", "), inline: true },
  ];
  const footer = META_TAG + JSON.stringify(meta);
  const payload = { username: "ห้องแต่งตัว", allowed_mentions: { parse: [] },
    content: s.pieces.length > 1 ? `ชุดลายใหม่จากผู้เล่น (${s.pieces.length} ชิ้น): กด ✅ เพื่ออนุมัติทั้งชุด` : "ลายใหม่จากผู้เล่น: กด ✅ เพื่ออนุมัติ",
    // the meta again in the footer: the live list reads it from the message itself, one Discord call per 100 messages
    // (a meta.json download per skin hit the free plan's 50 calls at about 40 skins; meta.json stays for the PC import);
    // a footer holds 2048 characters: a long set leaves it out and the list falls back to meta.json
    embeds: [{ title: (s.title ? s.title + " · " : "") + (s.pieces.length > 1 ? `ชุดลาย ${s.pieces.length} ชิ้น` : `${s.pieces[0].item} (${KINDS[s.pieces[0].kind]})`), fields,
      image: { url: `attachment://${pv || "skin0.png"}` }, timestamp: at, ...(footer.length <= 2048 ? { footer: { text: footer } } : {}) }],
    attachments: [...flat.map((t, i) => ({ id: i, filename: `skin${i}.png` })),
      ...(pv ? [{ id: flat.length, filename: pv }] : []), { id: flat.length + (pv ? 1 : 0), filename: "meta.json" }] };
  const fd = new FormData();
  fd.append("payload_json", JSON.stringify(payload));
  flat.forEach((t, i) => fd.append(`files[${i}]`, new Blob([t.bytes], { type: "image/png" }), `skin${i}.png`));
  if (pv) fd.append(`files[${flat.length}]`, new Blob([s.preview.bytes], { type: s.preview.ext === "png" ? "image/png" : "image/jpeg" }), pv);
  fd.append(`files[${flat.length + (pv ? 1 : 0)}]`, new Blob([JSON.stringify(meta, null, 1)], { type: "application/json" }), "meta.json");
  return fd;
}

export async function submit(request, env) {
  if (request.method !== "POST") return fail("method", 405);
  // trimmed: a secret piped in from Windows PowerShell arrives with a BOM (U+FEFF, which trim() removes), and the webhook
  // URL then failed to parse (2026-11-12, the first live sends)
  const hook = String(env.DISCORD_WEBHOOK ?? "").trim(), secret = String(env.TURNSTILE_SECRET ?? "").trim();
  if (!hook || !secret) return fail("closed", 503);
  const url = new URL(request.url), origin = request.headers.get("origin");
  if (origin && origin !== url.origin) return fail("origin", 403);               // only the page itself may send
  if (Number(request.headers.get("content-length") || 0) > LIMITS.bodyBytes) return fail("big", 413);
  let form;
  try { form = await request.formData(); } catch { return fail("form"); }
  const ip = request.headers.get("cf-connecting-ip") || "";
  if (!(await turnstileOk(secret, form.get("token"), ip))) return fail("bot", 403);
  const s = await readSubmission(form);
  if (s.error) return fail(s.error);
  if (await overLimit(ip)) return fail("rate", 429);
  const r = await fetch(hook + (hook.includes("?") ? "&" : "?") + "wait=true",
    { method: "POST", body: discordBody(s, new Date().toISOString()) });
  if (!r.ok) { console.error("discord", r.status, await r.text().catch(() => "")); return fail("upstream", 502); }
  return json({ ok: true });
}

// ---------- the approved skins, live from the channel (2026-11-12; user: "upload player skin data thru phone after I
// approved in discord"): GET /api/community lists every Worker message in the channel with a ✅ (the channel is
// private: only the user reacts), cached 60 s per data centre; GET /api/community/<message id>/<n>.png serves one
// skin. Nothing is checked again here: the Worker checked each skin when it was sent (fields, PNG, size), and the page
// skips a piece it lacks or a TTO piece and draws each skin at the original's size. Secrets: DISCORD_BOT_TOKEN,
// DISCORD_CHANNEL; without them (or when Discord fails) the route answers an error and the page falls back to the
// published community.json (pipeline/wardrobe_community.py, the PC import).
const LIST_SEC = 60, cacheKey = path => new Request("https://community.wardrobe.invalid/" + path);
export const META_TAG = "meta ";
const footerMeta = m => {                             // the meta the Worker wrote into the embed's footer (since 2026-11-12)
  for (const e of m.embeds || []) { const t = e.footer?.text || ""; if (t.startsWith(META_TAG)) try { return JSON.parse(t.slice(META_TAG.length)); } catch {} }
  return null;
};
async function cached(path, sec, make) {             // the data centre's cache when there is one (not in node tests)
  const c = typeof caches === "undefined" ? null : caches.default, hit = c && await c.match(cacheKey(path));
  if (hit) return hit.json();
  const v = await make();
  if (c) await c.put(cacheKey(path), new Response(JSON.stringify(v), { headers: { "cache-control": `max-age=${sec}` } }));
  return v;
}
export function filesOf(m) {                          // attachments + the embed's picture (Discord moves skin0.png there)
  const f = Object.fromEntries((m.attachments || []).map(a => [a.filename, a.url]));
  for (const e of m.embeds || []) { const u = e.image?.url || ""; if (u.startsWith("https://")) f[new URL(u).pathname.split("/").pop()] ??= u; }
  return f;
}
// a message's meta -> the set the page shows ({ id, cls, name, link, at, face, thumb, pieces: [{ slot, kind, item, tex }] }),
// with the Discord URLs it reads kept apart (src: the textures in the order the picture routes count them, prev: the
// preview): meta v2 has `pieces`, the first format one piece's kind / item / textures
function setOf(m, meta, files) {
  const defs = Array.isArray(meta.pieces) ? meta.pieces : [{ kind: meta.kind, item: meta.item, textures: meta.textures }];
  const pieces = [], src = [];
  for (const d of defs) {
    const tex = {};
    for (const t of d?.textures || []) {
      const u = files[t.file];
      if (u) { tex[String(t.tex ?? "")] = `api/community/${m.id}/${src.length}.png`; src.push(u); }
    }
    if (Object.keys(tex).length) pieces.push({ slot: SLOT_KIND[d.slot] === d.kind ? d.slot : DEFAULT_SLOT[d.kind] || null, kind: d.kind, item: d.item, tex });
  }
  if (!pieces.length) return null;
  const prev = files["preview.jpg"] || files["preview.png"] || null;
  return { id: m.id, cls: meta.cls, name: meta.name, ...(meta.title ? { title: String(meta.title) } : {}), link: meta.link || "", at: meta.at || m.timestamp,
    face: Number.isInteger(meta.face) ? meta.face : null, thumb: prev ? `api/community/${m.id}/preview` : null, pieces, src, prev };
}
async function approvedSets(env) {
  const token = String(env.DISCORD_BOT_TOKEN ?? "").trim(), ch = String(env.DISCORD_CHANNEL ?? "").trim();
  if (!token || !ch) throw new Error("closed");
  return cached("sets", LIST_SEC, async () => {
    const sets = [];
    for (let before = ""; ;) {
      const r = await fetch(`https://discord.com/api/v10/channels/${ch}/messages?limit=100${before && "&before=" + before}`,
        { headers: { authorization: "Bot " + token, "user-agent": "DiscordBot (https://12tails-wardrobe.jumpthai.workers.dev, 1)" } });
      if (!r.ok) throw new Error("discord " + r.status);
      const page = await r.json();
      for (const m of page) {
        if (!m.webhook_id || !(m.reactions || []).some(x => x.emoji?.name === "✅")) continue;
        const files = filesOf(m);
        const meta = footerMeta(m) || (files["meta.json"] &&     // older messages: their meta.json, once a day per data centre
          await cached("meta/" + m.id, 86400, () => fetch(files["meta.json"]).then(x => x.ok ? x.json() : null)).catch(() => null));
        const s = meta && setOf(m, meta, files);
        if (s) sets.push(s);
      }
      if (page.length < 100) break;
      before = page.at(-1).id;
    }
    return sets.sort((a, b) => (a.at > b.at) - (a.at < b.at));
  });
}
export async function community(request, env) {
  if (request.method !== "GET") return fail("method", 405);
  let sets;
  try { sets = await approvedSets(env); } catch (e) { return fail(e.message === "closed" ? "closed" : "upstream", e.message === "closed" ? 503 : 502); }
  const path = new URL(request.url).pathname, m = path.match(/^\/api\/community\/(\d+)\/(\d)\.png$/), pm = path.match(/^\/api\/community\/(\d+)\/preview$/);
  if (!m && !pm) return new Response(JSON.stringify({ sets: sets.map(({ src, prev, ...s }) => s) }),
    { headers: { "content-type": "application/json; charset=utf-8", "cache-control": `public, max-age=${LIST_SEC}` } });
  const found = sets.find(s => s.id === (m || pm)[1]);                     // only a set that is approved now
  const url = m ? found?.src[+m[2]] : found?.prev;
  if (!url) return new Response("Not found", { status: 404 });
  const r = await fetch(url);
  if (!r.ok) return fail("upstream", 502);
  const type = m ? "image/png" : (r.headers.get("content-type") || "").startsWith("image/") ? r.headers.get("content-type") : "image/jpeg";
  return new Response(r.body, { headers: { "content-type": type, "cache-control": "public, max-age=3600" } });
}
export default {
  async fetch(request, env) {
    const { pathname } = new URL(request.url);
    if (pathname === "/api/submit") return submit(request, env);
    if (pathname === "/api/community" || pathname.startsWith("/api/community/")) return community(request, env);
    return new Response("Not found", { status: 404 });                          // no file matched: as before the Worker
  },
};
