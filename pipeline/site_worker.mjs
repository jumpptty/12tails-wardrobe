// The public wardrobe's Worker (2026-11-11, community skins; NOTES.md "community skins"). The static copy
// (wardrobe_dist) is served as the Worker's assets; Cloudflare answers every request a file matches and runs this only
// for the rest, so the one route here is POST /api/submit: a visitor's own skin for one piece, checked and posted to a
// private Discord channel through a webhook, where the user approves it with a reaction (pipeline/wardrobe_community.py
// imports the approved ones). Deploy (from an empty folder, NOTES.md "Online copy"):
//   npx wrangler deploy D:/12tails-wardrobe/pipeline/site_worker.mjs --assets D:/12tails-wardrobe/wardrobe_dist
//     --name 12tails-wardrobe --compatibility-date 2026-11-07
// Secrets (the user sets them once: npx wrangler secret put <NAME> --name 12tails-wardrobe):
//   DISCORD_WEBHOOK   the channel's webhook URL            TURNSTILE_SECRET   the Turnstile widget's secret key
// Without them the route answers 503 (the page hides the send action until it has a Turnstile site key).
// Nothing is stored here: no IP address or picture is kept or sent on, only what the visitor typed and the skin.

const CLASSES = { bat: "ค้างคาว", bison: "ไบซัน", cat: "แมว", chameleon: "กิ้งก่า", mole: "ตุ่น", monkey: "ลิง", panda: "แพนด้า",
  penguin: "เพนกวิน", rabbit: "กระต่าย", sheep: "แกะ", whale: "วาฬ", wolf: "หมาป่า" };
const KINDS = { outfits: "ชุด", weapons: "อาวุธ", accessories: "หมวก", trinkets: "ประดับหลัง" };
export const LIMITS = { files: 2, fileBytes: 4 << 20, bodyBytes: 9 << 20, side: 4096, name: 40, link: 200, perWindow: 5, windowSec: 600 };
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

// the form's fields -> the submission, or an error code (the page shows each in Thai)
export async function readSubmission(form) {
  const cls = String(form.get("cls") || ""), kind = String(form.get("kind") || ""), item = String(form.get("item") || "");
  if (!(cls in CLASSES) && cls !== "all") return { error: "piece" };
  if (!(kind in KINDS) || !/^[A-Za-z0-9_ .-]{1,64}$/.test(item)) return { error: "piece" };
  if (form.get("consent") !== "1") return { error: "consent" };
  const name = clean(form.get("name"), LIMITS.name), link = cleanLink(form.get("link"));
  if (!name) return { error: "name" };
  if (link === null) return { error: "link" };
  const textures = [];
  for (let i = 0; i < LIMITS.files; i++) {
    const f = form.get("skin" + i);
    if (!f || typeof f === "string") continue;
    const tex = String(form.get("tex" + i) ?? "");
    if (!/^[A-Za-z0-9_ .-]{0,80}$/.test(tex)) return { error: "piece" };
    if (f.size > LIMITS.fileBytes) return { error: "big" };
    const bytes = new Uint8Array(await f.arrayBuffer()), size = pngSize(bytes);
    if (!size || !size.w || !size.h || size.w > LIMITS.side || size.h > LIMITS.side) return { error: "png" };
    textures.push({ tex, bytes, ...size });
  }
  if (!textures.length) return { error: "png" };
  return { cls, kind, item, name, link, textures };
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
  const meta = { v: 1, cls: s.cls, kind: s.kind, item: s.item, name: s.name, link: s.link, at,
    textures: s.textures.map((t, i) => ({ tex: t.tex, file: `skin${i}.png`, w: t.w, h: t.h })) };
  const fields = [
    { name: "ตัวละคร", value: s.cls === "all" ? "ทุกอาชีพ" : CLASSES[s.cls], inline: true },
    { name: "ช่อง", value: KINDS[s.kind], inline: true },
    { name: "ชิ้น", value: s.item, inline: true },
    { name: "ลายโดย", value: s.name, inline: true },
    { name: "ลิงก์", value: s.link || "-", inline: true },
    { name: "ขนาด", value: s.textures.map(t => `${t.w}×${t.h}`).join(", "), inline: true },
  ];
  const payload = { username: "ห้องแต่งตัว", allowed_mentions: { parse: [] },
    content: "ลายใหม่จากผู้เล่น: กด ✅ เพื่ออนุมัติ",
    embeds: [{ title: `${s.item} (${KINDS[s.kind]})`, fields, image: { url: "attachment://skin0.png" }, timestamp: at }],
    attachments: [...s.textures.map((t, i) => ({ id: i, filename: `skin${i}.png` })), { id: s.textures.length, filename: "meta.json" }] };
  const fd = new FormData();
  fd.append("payload_json", JSON.stringify(payload));
  s.textures.forEach((t, i) => fd.append(`files[${i}]`, new Blob([t.bytes], { type: "image/png" }), `skin${i}.png`));
  fd.append(`files[${s.textures.length}]`, new Blob([JSON.stringify(meta, null, 1)], { type: "application/json" }), "meta.json");
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

export default {
  async fetch(request, env) {
    const { pathname } = new URL(request.url);
    if (pathname === "/api/submit") return submit(request, env);
    return new Response("Not found", { status: 404 });                          // no file matched: as before the Worker
  },
};
