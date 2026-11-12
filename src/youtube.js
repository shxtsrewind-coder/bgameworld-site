// YouTube Shorts through the YouTube Data API v3.
//
// Setup (once):
//   1. Google Cloud project with "YouTube Data API v3" enabled.
//   2. OAuth consent screen: External, then "Publish app" so it's "In production"
//      (in "Testing", Google ends the connection after 7 days).
//   3. OAuth client ID, type "Web application", authorised redirect URI:
//        https://bgameworld.com/api/youtube/callback
//   4. Cloudflare secrets: YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_SETUP_KEY
//   5. Connect: https://bgameworld.com/api/youtube/connect?key=<YOUTUBE_SETUP_KEY>
//      Sign in with the Google account that owns the BGameWorld channel and pick that channel.
//   Test:  https://bgameworld.com/api/youtube/test?key=<YOUTUBE_SETUP_KEY>
//      uploads the next scheduled Short straight away.
//
// Each Short in src/shorts.json is uploaded as a public video at its time (within 6 hours, so an
// outage never dumps a backlog). The video files are this site's own /social/shorts/ and
// /social/reels/ files. Pause: KV key YOUTUBE_PAUSED = 1 (or PAUSED for everything).
import shorts from "./shorts.json";

const SITE = "https://bgameworld.com";
const REDIRECT = `${SITE}/api/youtube/callback`;
const SCOPES = "https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube.readonly";
const TOKEN_URL = "https://oauth2.googleapis.com/token";
const WINDOW_MS = 6 * 60 * 60 * 1000;
const CLAIM_MS = 20 * 60 * 1000;
const ERROR_TTL = 14 * 24 * 60 * 60;
const configured = (env) => Boolean(env.YOUTUBE_CLIENT_ID && env.YOUTUBE_CLIENT_SECRET);

// ---------------------------------------------------------------- routes
export async function youtubeRoute(request, env, url) {
  const p = url.pathname;
  if (p === "/api/youtube/connect") return connect(env, url);
  if (p === "/api/youtube/callback") return callback(env, url);
  if (p === "/api/youtube/test") return testUpload(env, url);
  return page(404, "Not found", "There's nothing here.");
}

async function connect(env, url) {
  if (!configured(env) || !env.YOUTUBE_SETUP_KEY) return page(503, "YouTube isn't set up yet", "Add YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET and YOUTUBE_SETUP_KEY as secrets in Cloudflare first.");
  if (!(await sameText(url.searchParams.get("key") || "", env.YOUTUBE_SETUP_KEY))) return page(403, "Wrong setup key", "Open this link with ?key= followed by the YOUTUBE_SETUP_KEY you saved in Cloudflare.");
  const state = randomHex(24);
  await env.SOCIAL.put(`yt:state:${state}`, "1", { expirationTtl: 600 });
  const q = new URLSearchParams({ client_id: env.YOUTUBE_CLIENT_ID, redirect_uri: REDIRECT, response_type: "code", scope: SCOPES,
    access_type: "offline", prompt: "consent select_account", include_granted_scopes: "true", state });
  return new Response(null, { status: 302, headers: { location: `https://accounts.google.com/o/oauth2/v2/auth?${q}`, "cache-control": "no-store" } });
}

async function callback(env, url) {
  const state = url.searchParams.get("state") || "";
  if (!state || !(await env.SOCIAL.get(`yt:state:${state}`))) return page(400, "This link has expired", "Start again from the connect link.");
  await env.SOCIAL.delete(`yt:state:${state}`);
  if (url.searchParams.get("error")) return page(400, "YouTube didn't connect", `Google said: ${url.searchParams.get("error")}`);
  const code = url.searchParams.get("code");
  if (!code) return page(400, "YouTube didn't connect", "No code came back from Google. Start again from the connect link.");
  const d = await tokenRequest(env, { grant_type: "authorization_code", code, redirect_uri: REDIRECT });
  if (!d.access_token) return page(400, "YouTube didn't connect", `Google said: ${d.error_description || d.error || "unexpected response"}`);
  if (!d.refresh_token) return page(400, "Connect again", "Google didn't give a lasting connection. Go to myaccount.google.com/permissions, remove the BGameWorld app, then open the connect link again.");
  if (!String(d.scope || "").includes("youtube.upload")) return page(400, "Upload permission missing", "Open the connect link again and tick the box that lets the app manage your YouTube videos.");
  const now = Date.now();
  await env.SOCIAL.put("yt:auth", JSON.stringify({ refresh_token: d.refresh_token, access_token: d.access_token, expires_at: now + (d.expires_in || 3600) * 1000, connected_at: new Date(now).toISOString() }));
  await env.SOCIAL.delete("yt:err:auth");
  const ch = await channelInfo(d.access_token);
  if (ch) await env.SOCIAL.put("yt:channel", JSON.stringify(ch));
  return page(200, "YouTube is connected", ch ? `Shorts will post to “${ch.title}”. You can close this page.` : "Shorts will post to the channel you picked. You can close this page.");
}

async function testUpload(env, url) {
  if (!configured(env) || !env.YOUTUBE_SETUP_KEY) return page(503, "YouTube isn't set up yet", "Add the YouTube secrets in Cloudflare first.");
  if (!(await sameText(url.searchParams.get("key") || "", env.YOUTUBE_SETUP_KEY))) return page(403, "Wrong setup key", "Use the YOUTUBE_SETUP_KEY you saved in Cloudflare.");
  const now = Date.now();
  let next = null;
  for (const s of shorts) {
    if (Date.parse(s.at) < now - WINDOW_MS) continue;
    const rec = await env.SOCIAL.get(`yt:s:${s.id}`);
    if (!rec) { next = s; break; }
  }
  if (!next) return page(404, "Nothing left to post", "Every Short in src/shorts.json has been posted or missed. Add more.");
  const r = await upload(env, next, now);
  if (r.video_id) return page(200, "Short posted", `“${next.title}” is live: https://youtube.com/shorts/${r.video_id}`);
  return page(500, "YouTube said no", r.error || "Unexpected response from YouTube.");
}

// ---------------------------------------------------------------- cron
export async function youtubeDue(env, now) {
  if (!configured(env)) return;
  if ((await env.SOCIAL.get("PAUSED")) === "1" || (await env.SOCIAL.get("YOUTUBE_PAUSED")) === "1") return;
  if (!(await env.SOCIAL.get("yt:auth"))) return;
  for (const s of shorts) {
    const at = Date.parse(s.at);
    if (at > now || now - at > WINDOW_MS) continue;
    if (await env.SOCIAL.get(`yt:s:${s.id}`)) continue;
    await upload(env, s, now);
    return;                                   // one upload per run keeps each run short
  }
}

async function upload(env, s, now) {
  const key = `yt:s:${s.id}`;
  const claim = await env.SOCIAL.get(`yt:claim:${s.id}`);
  if (claim && now - Number(claim) < CLAIM_MS) return { error: "already uploading" };
  await env.SOCIAL.put(`yt:claim:${s.id}`, String(now), { expirationTtl: 3600 });
  try {
    const token = await accessToken(env, now);
    if (!token) return fail(env, s, "auth", "Not connected to YouTube (or Google ended the connection). Open the connect link again.", now);
    const file = await env.ASSETS.fetch(new Request(`${SITE}/${s.file}`));
    if (!file.ok) return fail(env, s, "read video", `video file missing (${file.status})`, now);
    const bytes = await file.arrayBuffer();
    const meta = {
      snippet: { title: s.title, description: s.description, tags: s.tags, categoryId: "20", defaultLanguage: "en", defaultAudioLanguage: "en" },
      status: { privacyStatus: "public", selfDeclaredMadeForKids: false, embeddable: true },
    };
    const start = await fetch("https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status", {
      method: "POST",
      headers: { authorization: `Bearer ${token}`, "content-type": "application/json; charset=UTF-8",
        "x-upload-content-type": "video/mp4", "x-upload-content-length": String(bytes.byteLength) },
      body: JSON.stringify(meta),
    });
    const loc = start.headers.get("location");
    if (!start.ok || !loc) return fail(env, s, "start upload", await googleError(start), now);
    const put = await fetch(loc, { method: "PUT", headers: { "content-type": "video/mp4" }, body: bytes });
    const v = await put.json().catch(() => ({}));
    if (!put.ok || !v.id) return fail(env, s, "upload", v.error ? (v.error.message || JSON.stringify(v.error)) : `upload returned ${put.status}`, now);
    await env.SOCIAL.put(key, JSON.stringify({ video_id: v.id, posted_at: new Date(now).toISOString(), upload_status: v.status && v.status.uploadStatus }));
    await env.SOCIAL.delete(`yt:err:${s.id}`);
    await env.SOCIAL.delete(`yt:claim:${s.id}`);
    return { video_id: v.id };
  } catch (e) {
    return fail(env, s, "upload", String(e && e.message ? e.message : e), now);
  }
}

async function fail(env, s, step, message, now) {
  await env.SOCIAL.delete(`yt:claim:${s.id}`);   // the next run (30 minutes later) tries again, inside the window
  await env.SOCIAL.put(`yt:err:${s.id}`, JSON.stringify({ at: new Date(now).toISOString(), step, message }), { expirationTtl: ERROR_TTL });
  return { error: `${step}: ${message}` };
}

async function googleError(res) {
  const d = await res.json().catch(() => ({}));
  const e = d.error || {};
  const reason = e.errors && e.errors[0] && e.errors[0].reason;
  return `${res.status} ${e.message || "unexpected response"}${reason ? ` (${reason})` : ""}`;
}

// ---------------------------------------------------------------- auth
async function tokenRequest(env, fields) {
  const body = new URLSearchParams({ client_id: env.YOUTUBE_CLIENT_ID, client_secret: env.YOUTUBE_CLIENT_SECRET, ...fields });
  const res = await fetch(TOKEN_URL, { method: "POST", body });
  return res.json().catch(() => ({}));
}

async function accessToken(env, now) {
  const a = JSON.parse((await env.SOCIAL.get("yt:auth")) || "null");
  if (!a) return null;
  if (a.access_token && a.expires_at - 120000 > now) return a.access_token;
  const d = await tokenRequest(env, { grant_type: "refresh_token", refresh_token: a.refresh_token });
  if (!d.access_token) {
    await env.SOCIAL.put("yt:err:auth", JSON.stringify({ at: new Date(now).toISOString(), message: d.error_description || d.error || "token refresh failed" }), { expirationTtl: ERROR_TTL });
    return null;
  }
  a.access_token = d.access_token; a.expires_at = now + (d.expires_in || 3600) * 1000; a.refreshed_at = new Date(now).toISOString();
  await env.SOCIAL.put("yt:auth", JSON.stringify(a));
  return a.access_token;
}

async function channelInfo(token) {
  const r = await fetch("https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true", { headers: { authorization: `Bearer ${token}` } });
  const d = await r.json().catch(() => ({}));
  const c = d.items && d.items[0];
  return c ? { id: c.id, title: c.snippet && c.snippet.title } : null;
}

// ---------------------------------------------------------------- status
export async function youtubeStatus(env, now) {
  const a = JSON.parse((await env.SOCIAL.get("yt:auth")) || "null");
  const out = { configured: configured(env), connected: Boolean(a), paused: (await env.SOCIAL.get("YOUTUBE_PAUSED")) === "1", shorts: [] };
  const ch = await env.SOCIAL.get("yt:channel");
  if (ch) out.channel = JSON.parse(ch);
  const ae = await env.SOCIAL.get("yt:err:auth");
  if (ae) out.auth_error = JSON.parse(ae);
  for (const s of shorts) {
    const at = Date.parse(s.at);
    if (now - at > 3 * 86400000 && !(await env.SOCIAL.get(`yt:err:${s.id}`))) {
      const done = await env.SOCIAL.get(`yt:s:${s.id}`);
      if (!done) continue;                          // old and never posted: leave it out of the list
    }
    const done = await env.SOCIAL.get(`yt:s:${s.id}`);
    const err = await env.SOCIAL.get(`yt:err:${s.id}`);
    let state = done ? "posted" : at > now ? "scheduled" : now - at <= WINDOW_MS ? "due" : "missed";
    const row = { id: s.id, at: s.at, state, title: s.title };
    if (done) { const r = JSON.parse(done); row.url = `https://youtube.com/shorts/${r.video_id}`; row.posted_at = r.posted_at; }
    if (err) row.last_error = JSON.parse(err);
    out.shorts.push(row);
  }
  return out;
}

// ---------------------------------------------------------------- helpers
// Setup keys are typed by hand (often on a phone), so stray spaces and an
// auto-capitalised first letter don't count.
async function sameText(a, b) {
  const norm = (s) => String(s || "").trim().toLowerCase();
  a = norm(a); b = norm(b);
  if (!b) return false;
  const enc = new TextEncoder();
  const [x, y] = (await Promise.all([crypto.subtle.digest("SHA-256", enc.encode(a)), crypto.subtle.digest("SHA-256", enc.encode(b))])).map((h) => new Uint8Array(h));
  let diff = 0;
  for (let i = 0; i < x.length; i++) diff |= x[i] ^ y[i];
  return diff === 0;
}

function randomHex(n) {
  const b = new Uint8Array(n); crypto.getRandomValues(b);
  return [...b].map((x) => x.toString(16).padStart(2, "0")).join("");
}

function page(status, title, text) {
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>${esc(title)} | BGameWorld</title>
<style>body{margin:0;background:#fff;color:#121212;font:400 17px/1.6 "Libre Franklin",Arial,sans-serif}main{max-width:560px;margin:0 auto;padding:56px 20px}h1{font:700 34px/1.1 "Zilla Slab",Georgia,serif;margin:0 0 12px}p{color:#4A4A4A;word-break:break-word}</style></head>
<body><main><h1>${esc(title)}</h1><p>${esc(text)}</p></main></body></html>`;
  return new Response(html, { status, headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" } });
}
