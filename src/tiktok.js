// TikTok drafts for BGameWorld.
//
// TikTok only allows apps that have passed its audit to post publicly, and it
// doesn't audit tools that post to your own account. So instead of posting,
// this sends each puzzle slideshow to the account's TikTok inbox as a draft
// (Content Posting API, MEDIA_UPLOAD). Open the TikTok notification, add a
// sound and tap Post.
//
// Setup (once):
//   Secrets: TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET, TIKTOK_SETUP_KEY
//   Visit https://bgameworld.com/api/tiktok/connect?key=<TIKTOK_SETUP_KEY>
//   and approve on TikTok. The tokens are kept in the SOCIAL KV namespace
//   (key tt:auth) and refreshed automatically; they are never shown.
//
// Schedule: src/tiktok.json. Slides live at /social/tt/<id>-<n>.jpg (JPEG,
// 1080x1920), which must sit on a domain verified in the TikTok app.
//
// Pause TikTok only: set KV key TIKTOK_PAUSED to 1 (PAUSED pauses everything).
import queue from "./tiktok.json";

const SITE = "https://bgameworld.com";
const REDIRECT = `${SITE}/api/tiktok/callback`;
const AUTH_URL = "https://www.tiktok.com/v2/auth/authorize/";
const API = "https://open.tiktokapis.com/v2";
const SCOPES = "user.info.basic,video.upload";
const WINDOW_MS = 6 * 60 * 60 * 1000;
const ERROR_TTL = 14 * 24 * 60 * 60;
const DONE = new Set(["SEND_TO_USER_INBOX", "PUBLISH_COMPLETE", "FAILED"]);

// ---------------------------------------------------------------- routes
export async function tiktokRoute(request, env, url) {
  if (url.pathname === "/api/tiktok/connect") return connect(env, url);
  if (url.pathname === "/api/tiktok/callback") return callback(env, url);
  return page(404, "Not found", "There's nothing here.");
}

async function connect(env, url) {
  if (!env.TIKTOK_CLIENT_KEY || !env.TIKTOK_CLIENT_SECRET || !env.TIKTOK_SETUP_KEY) {
    return page(503, "TikTok isn't set up yet", "Add TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET and TIKTOK_SETUP_KEY as secrets in Cloudflare first.");
  }
  if (!(await sameText(url.searchParams.get("key") || "", env.TIKTOK_SETUP_KEY))) {
    return page(403, "Wrong setup key", "Open this link with ?key= followed by the TIKTOK_SETUP_KEY you saved in Cloudflare.");
  }
  const state = randomHex(24);
  await env.SOCIAL.put(`tt:state:${state}`, "1", { expirationTtl: 600 });
  const q = new URLSearchParams({ client_key: env.TIKTOK_CLIENT_KEY, response_type: "code", scope: SCOPES, redirect_uri: REDIRECT, state });
  return new Response(null, { status: 302, headers: { location: `${AUTH_URL}?${q}`, "cache-control": "no-store" } });
}

async function callback(env, url) {
  const state = url.searchParams.get("state") || "";
  const known = state && (await env.SOCIAL.get(`tt:state:${state}`));
  if (!known) return page(400, "This link has expired", "Start again from the connect link.");
  await env.SOCIAL.delete(`tt:state:${state}`);
  if (url.searchParams.get("error")) {
    return page(400, "TikTok didn't connect", `TikTok said: ${url.searchParams.get("error_description") || url.searchParams.get("error")}`);
  }
  const code = url.searchParams.get("code");
  if (!code) return page(400, "TikTok didn't connect", "No code came back from TikTok. Start again from the connect link.");

  const data = await tokenRequest(env, { code, grant_type: "authorization_code", redirect_uri: REDIRECT });
  if (!data.access_token) {
    return page(400, "TikTok didn't connect", `TikTok said: ${data.error_description || data.error || "unexpected response"}`);
  }
  if (!String(data.scope || "").split(",").includes("video.upload")) {
    return page(400, "One permission is missing", "Connect again and leave “Upload content to TikTok” ticked.");
  }
  await saveAuth(env, data, Date.now());
  await env.SOCIAL.delete("tterr:auth");
  return page(200, "TikTok is connected", "BGameWorld will send each puzzle slideshow to your TikTok inbox at its scheduled time. You can close this page.");
}

// ---------------------------------------------------------------- tokens
async function tokenRequest(env, fields) {
  const body = new URLSearchParams({ client_key: env.TIKTOK_CLIENT_KEY, client_secret: env.TIKTOK_CLIENT_SECRET, ...fields });
  const res = await fetch(`${API}/oauth/token/`, {
    method: "POST",
    headers: { "content-type": "application/x-www-form-urlencoded", "cache-control": "no-cache" },
    body,
  });
  return res.json().catch(() => ({ error: `http_${res.status}` }));
}

async function saveAuth(env, d, now) {
  await env.SOCIAL.put("tt:auth", JSON.stringify({
    open_id: d.open_id,
    scope: d.scope,
    access_token: d.access_token,
    expires_at: now + (Number(d.expires_in) || 86400) * 1000,
    refresh_token: d.refresh_token,
    refresh_expires_at: now + (Number(d.refresh_expires_in) || 31536000) * 1000,
    updated_at: new Date(now).toISOString(),
  }));
}

async function accessToken(env, now) {
  const raw = await env.SOCIAL.get("tt:auth");
  if (!raw) return null;
  const auth = JSON.parse(raw);
  if (auth.expires_at - now > 10 * 60 * 1000) return auth.access_token;
  const d = await tokenRequest(env, { grant_type: "refresh_token", refresh_token: auth.refresh_token });
  if (!d.access_token) {
    await env.SOCIAL.put("tterr:auth", JSON.stringify({ at: new Date(now).toISOString(), message: d.error_description || d.error || "refresh failed" }), { expirationTtl: ERROR_TTL });
    return null;
  }
  await saveAuth(env, { ...d, open_id: d.open_id || auth.open_id, scope: d.scope || auth.scope }, now);
  await env.SOCIAL.delete("tterr:auth");
  return d.access_token;
}

// ---------------------------------------------------------------- sending drafts
export async function tiktokDue(env, now) {
  if (!env.TIKTOK_CLIENT_KEY || !env.TIKTOK_CLIENT_SECRET) return;
  if ((await env.SOCIAL.get("PAUSED")) === "1" || (await env.SOCIAL.get("TIKTOK_PAUSED")) === "1") return;
  if (!(await env.SOCIAL.get("tt:auth"))) return;

  const due = queue.filter((p) => { const at = Date.parse(p.at); return at <= now && now - at <= WINDOW_MS; });
  const recent = queue.filter((p) => { const at = Date.parse(p.at); return at <= now && now - at <= 24 * 60 * 60 * 1000; });
  if (!due.length && !recent.length) return;
  const token = await accessToken(env, now);
  if (!token) return;

  for (const p of due) {
    const key = `tt:${p.id}`;
    if (await env.SOCIAL.get(key)) continue;
    await env.SOCIAL.put(key, "sending", { expirationTtl: 3600 });
    try {
      const images = Array.from({ length: p.slides }, (_, i) => `${SITE}/social/tt/${p.id}-${i + 1}.jpg`);
      const res = await fetch(`${API}/post/publish/content/init/`, {
        method: "POST",
        headers: { authorization: `Bearer ${token}`, "content-type": "application/json; charset=UTF-8" },
        body: JSON.stringify({
          post_info: { title: p.title, description: p.caption },
          source_info: { source: "PULL_FROM_URL", photo_cover_index: 0, photo_images: images },
          post_mode: "MEDIA_UPLOAD",
          media_type: "PHOTO",
        }),
      });
      const data = await res.json().catch(() => ({}));
      const err = data.error || {};
      if (res.ok && err.code === "ok" && data.data && data.data.publish_id) {
        await env.SOCIAL.put(key, JSON.stringify({ publish_id: data.data.publish_id, sent_at: new Date(now).toISOString(), status: "PROCESSING_DOWNLOAD" }));
        await env.SOCIAL.delete(`tterr:${p.id}`);
      } else {
        await env.SOCIAL.delete(key);   // retry on the next run, inside the 6-hour window
        await env.SOCIAL.put(`tterr:${p.id}`, JSON.stringify({ at: new Date(now).toISOString(), status: res.status, code: err.code, message: err.message || "Unexpected response from TikTok", log_id: err.log_id }), { expirationTtl: ERROR_TTL });
      }
    } catch (e) {
      await env.SOCIAL.delete(key);
      await env.SOCIAL.put(`tterr:${p.id}`, JSON.stringify({ at: new Date(now).toISOString(), message: String(e && e.message ? e.message : e) }), { expirationTtl: ERROR_TTL });
    }
  }

  // Follow up on drafts sent in the last day until TikTok says they reached the inbox (or failed).
  for (const p of recent) {
    const raw = await env.SOCIAL.get(`tt:${p.id}`);
    if (!raw || raw === "sending") continue;
    const rec = JSON.parse(raw);
    if (DONE.has(rec.status)) continue;
    const res = await fetch(`${API}/post/publish/status/fetch/`, {
      method: "POST",
      headers: { authorization: `Bearer ${token}`, "content-type": "application/json; charset=UTF-8" },
      body: JSON.stringify({ publish_id: rec.publish_id }),
    });
    const data = await res.json().catch(() => ({}));
    if (data.data && data.data.status) {
      rec.status = data.data.status;
      if (data.data.fail_reason) rec.fail_reason = data.data.fail_reason;
      rec.checked_at = new Date(now).toISOString();
      await env.SOCIAL.put(`tt:${p.id}`, JSON.stringify(rec));
    }
  }
}

// ---------------------------------------------------------------- status (no tokens)
export async function tiktokStatus(env, now) {
  const out = { configured: Boolean(env.TIKTOK_CLIENT_KEY && env.TIKTOK_CLIENT_SECRET), connected: false,
    paused: (await env.SOCIAL.get("TIKTOK_PAUSED")) === "1", posts: [] };
  const raw = await env.SOCIAL.get("tt:auth");
  if (raw) {
    const a = JSON.parse(raw);
    out.connected = true;
    out.scope = a.scope;
    out.token_refreshed_at = a.updated_at;
    out.reconnect_by = new Date(a.refresh_expires_at).toISOString();
  }
  const authErr = await env.SOCIAL.get("tterr:auth");
  if (authErr) out.auth_error = JSON.parse(authErr);
  for (const p of queue) {
    const done = await env.SOCIAL.get(`tt:${p.id}`);
    const err = await env.SOCIAL.get(`tterr:${p.id}`);
    const at = Date.parse(p.at);
    let state;
    if (done && done !== "sending") state = "sent";
    else if (done === "sending") state = "sending";
    else if (at > now) state = "scheduled";
    else if (now - at <= WINDOW_MS) state = "due";
    else state = "missed";
    const row = { id: p.id, game: p.game, at: p.at, state };
    if (done && done !== "sending") { const r = JSON.parse(done); row.tiktok = { status: r.status, sent_at: r.sent_at, fail_reason: r.fail_reason }; }
    if (err) row.last_error = JSON.parse(err);
    out.posts.push(row);
  }
  return out;
}

// ---------------------------------------------------------------- helpers
function randomHex(n) {
  const b = new Uint8Array(n); crypto.getRandomValues(b);
  return Array.from(b, (x) => x.toString(16).padStart(2, "0")).join("");
}

async function sameText(a, b) {
  const enc = new TextEncoder();
  const [ha, hb] = await Promise.all([crypto.subtle.digest("SHA-256", enc.encode(a)), crypto.subtle.digest("SHA-256", enc.encode(b))]);
  const x = new Uint8Array(ha), y = new Uint8Array(hb);
  let diff = 0;
  for (let i = 0; i < x.length; i++) diff |= x[i] ^ y[i];
  return diff === 0;
}

function page(status, title, text) {
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>${esc(title)} | BGameWorld</title>
<style>body{margin:0;background:#0A0F2E;color:#EAEFF7;font:17px/1.6 Inter,-apple-system,Segoe UI,Helvetica,Arial,sans-serif}main{max-width:520px;margin:0 auto;padding:56px 20px}h1{font-size:28px;line-height:1.2;margin:0 0 12px}p{color:rgba(234,239,247,.75);margin:0 0 20px}a{color:#FFD140}</style></head>
<body><main><h1>${esc(title)}</h1><p>${esc(text)}</p><p><a href="/">bgameworld.com</a></p></main></body></html>`;
  return new Response(html, { status, headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store", "x-robots-tag": "noindex" } });
}
