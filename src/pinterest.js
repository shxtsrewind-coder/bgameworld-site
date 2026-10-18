// Pinterest video Pins through the Pinterest API (v5).
//
// Setup (once):
//   Secrets: PINTEREST_APP_ID, PINTEREST_APP_SECRET, PINTEREST_SETUP_KEY
//   Var (wrangler.jsonc): PINTEREST_ENV = "sandbox" while the app has Trial
//   access (Pins only visible to you), "production" once Standard access is granted.
//   Connect: https://bgameworld.com/api/pinterest/connect?key=<PINTEREST_SETUP_KEY>
//   Test:    https://bgameworld.com/api/pinterest/test?key=<PINTEREST_SETUP_KEY>
//            (posts the next video Pin straight away; record this for the Standard access review)
//
// Every day after 6 pm Lagos (17:00 UTC) the next video in src/pinvideos.json is
// uploaded; once Pinterest has processed it, a Pin is created on the "Puzzle Videos"
// board with a cover image and a link to the game. It's a queue, so nothing is lost
// if approval takes a while. Sandbox and production keep separate records.
//
// Pause: KV key PINTEREST_PAUSED = 1 (or PAUSED for everything).
import queue from "./pinvideos.json";

const SITE = "https://bgameworld.com";
const REDIRECT = `${SITE}/api/pinterest/callback`;
const SCOPES = "boards:read,boards:write,pins:read,pins:write,user_accounts:read";
const BOARD_NAME = "Puzzle Videos";
const DAILY_HOUR_UTC = 17;
const ERROR_TTL = 14 * 24 * 60 * 60;

const mode = (env) => (env.PINTEREST_ENV === "production" ? "production" : "sandbox");
const api = (env) => (mode(env) === "production" ? "https://api.pinterest.com/v5" : "https://api-sandbox.pinterest.com/v5");
const K = (env, k) => `pi:${mode(env)}:${k}`;
const configured = (env) => Boolean(env.PINTEREST_APP_ID && env.PINTEREST_APP_SECRET);

// ---------------------------------------------------------------- routes
export async function pinterestRoute(request, env, url) {
  const p = url.pathname;
  if (p === "/api/pinterest/connect") return connect(env, url);
  if (p === "/api/pinterest/callback") return callback(env, url);
  if (p === "/api/pinterest/test") return testPost(env, url);
  return page(404, "Not found", "There's nothing here.");
}

async function connect(env, url) {
  if (!configured(env) || !env.PINTEREST_SETUP_KEY) return page(503, "Pinterest isn't set up yet", "Add PINTEREST_APP_ID, PINTEREST_APP_SECRET and PINTEREST_SETUP_KEY as secrets in Cloudflare first.");
  if (!(await sameText(url.searchParams.get("key") || "", env.PINTEREST_SETUP_KEY))) return page(403, "Wrong setup key", "Open this link with ?key= followed by the PINTEREST_SETUP_KEY you saved in Cloudflare.");
  const state = randomHex(24);
  await env.SOCIAL.put(`pi:state:${state}`, "1", { expirationTtl: 600 });
  const q = new URLSearchParams({ client_id: env.PINTEREST_APP_ID, redirect_uri: REDIRECT, response_type: "code", scope: SCOPES, state });
  return new Response(null, { status: 302, headers: { location: `https://www.pinterest.com/oauth/?${q}`, "cache-control": "no-store" } });
}

async function callback(env, url) {
  const state = url.searchParams.get("state") || "";
  if (!state || !(await env.SOCIAL.get(`pi:state:${state}`))) return page(400, "This link has expired", "Start again from the connect link.");
  await env.SOCIAL.delete(`pi:state:${state}`);
  if (url.searchParams.get("error")) return page(400, "Pinterest didn't connect", `Pinterest said: ${url.searchParams.get("error_description") || url.searchParams.get("error")}`);
  const code = url.searchParams.get("code");
  if (!code) return page(400, "Pinterest didn't connect", "No code came back from Pinterest. Start again from the connect link.");
  const d = await tokenRequest(env, { grant_type: "authorization_code", code, redirect_uri: REDIRECT });
  if (!d.access_token) return page(400, "Pinterest didn't connect", `Pinterest said: ${d.message || d.error_description || d.error || "unexpected response"}`);
  await saveAuth(env, d, Date.now());
  await env.SOCIAL.delete(K(env, "err:auth"));
  return page(200, "Pinterest is connected", `BGameWorld can now post video Pins (${mode(env)} mode). You can close this page.`);
}

async function testPost(env, url) {
  if (!configured(env) || !env.PINTEREST_SETUP_KEY) return page(503, "Pinterest isn't set up yet", "Add the Pinterest secrets in Cloudflare first.");
  if (!(await sameText(url.searchParams.get("key") || "", env.PINTEREST_SETUP_KEY))) return page(403, "Wrong setup key", "Use the PINTEREST_SETUP_KEY you saved in Cloudflare.");
  const now = Date.now();
  const r = await advance(env, now, { force: true, wait: true });
  if (r.pin) return page(200, "Video Pin created", `“${r.item.title}” is on your ${BOARD_NAME} board (Pin ${r.pin}, ${mode(env)} mode).`);
  return page(r.error ? 500 : 202, r.error ? "Pinterest said no" : "Still processing", r.error || `The video for “${r.item ? r.item.title : "the next Pin"}” is uploaded and Pinterest is still processing it. It will be pinned automatically within 30 minutes.`);
}

// ---------------------------------------------------------------- cron
export async function pinterestDue(env, now) {
  if (!configured(env)) return;
  if ((await env.SOCIAL.get("PAUSED")) === "1" || (await env.SOCIAL.get("PINTEREST_PAUSED")) === "1") return;
  if (!(await env.SOCIAL.get(K(env, "auth")))) return;
  await advance(env, now, { force: false, wait: false });
}

// Moves the queue forward by one step: finish an item in progress, or start today's.
async function advance(env, now, { force, wait }) {
  const token = await accessToken(env, now);
  if (!token) return { error: "Not connected to Pinterest yet (or the connection expired). Open the connect link again." };
  const H = { authorization: `Bearer ${token}`, "content-type": "application/json" };

  let item = null, rec = null;
  for (const q of queue) {
    const raw = await env.SOCIAL.get(K(env, `v:${q.id}`));
    const r = raw ? JSON.parse(raw) : null;
    if (r && r.stage === "pinned") continue;
    item = q; rec = r; break;
  }
  if (!item) return { error: "Every video in the queue has been pinned. Add more to src/pinvideos.json." };

  if (!rec) {
    const day = new Date(now).toISOString().slice(0, 10);
    if (!force) {
      if (new Date(now).getUTCHours() < DAILY_HOUR_UTC) return {};
      if (await env.SOCIAL.get(K(env, `day:${day}`))) return {};
      if (await env.SOCIAL.get(K(env, "backoff"))) return {};   // a failed upload waits 2 hours before trying again
    }
    try {
      const reg = await (await fetch(`${api(env)}/media`, { method: "POST", headers: H, body: JSON.stringify({ media_type: "video" }) })).json();
      if (!reg.media_id || !reg.upload_url) return fail(env, item, "register", reg, now);
      const file = await env.ASSETS.fetch(new Request(`${SITE}/social/reels/${item.video}`));
      if (!file.ok) return fail(env, item, "read video", { message: `video file missing (${file.status})` }, now);
      const form = new FormData();
      for (const [k, v] of Object.entries(reg.upload_parameters || {})) form.append(k, v);
      form.append("file", new Blob([await file.arrayBuffer()], { type: "video/mp4" }), item.video);
      const up = await fetch(reg.upload_url, { method: "POST", body: form });
      if (up.status !== 204 && !up.ok) return fail(env, item, "upload", { message: `upload returned ${up.status}` }, now);
      rec = { stage: "uploaded", media_id: reg.media_id, t: now };
      await env.SOCIAL.put(K(env, `v:${item.id}`), JSON.stringify(rec));
      await env.SOCIAL.put(K(env, `day:${day}`), item.id, { expirationTtl: 3 * 86400 });
    } catch (e) {
      return fail(env, item, "upload", { message: String(e && e.message ? e.message : e) }, now);
    }
  }

  // Wait for Pinterest to process the video, then create the Pin.
  for (let tries = 0; ; tries++) {
    const m = await (await fetch(`${api(env)}/media/${rec.media_id}`, { headers: H })).json().catch(() => ({}));
    if (m.status === "succeeded") break;
    if (m.status === "failed") {
      await env.SOCIAL.delete(K(env, `v:${item.id}`));   // start this video again next time
      return fail(env, item, "processing", { message: "Pinterest couldn't process the video" }, now);
    }
    if (!wait || tries >= 8) return { item, pending: true };
    await new Promise((r) => setTimeout(r, 4000));
  }
  const board = await boardId(env, H);
  if (!board) return fail(env, item, "board", { message: `couldn't find or create the ${BOARD_NAME} board` }, now);
  const pinRes = await fetch(`${api(env)}/pins`, {
    method: "POST", headers: H,
    body: JSON.stringify({
      board_id: board, title: item.title, description: item.description, link: item.link, alt_text: item.alt,
      media_source: { source_type: "video_id", media_id: rec.media_id, cover_image_url: `${SITE}/social/reels/${item.cover}` },
    }),
  });
  const pin = await pinRes.json().catch(() => ({}));
  if (!pin.id) return fail(env, item, "create pin", pin, now);
  await env.SOCIAL.put(K(env, `v:${item.id}`), JSON.stringify({ stage: "pinned", media_id: rec.media_id, pin_id: pin.id, pinned_at: new Date(now).toISOString() }));
  await env.SOCIAL.delete(K(env, `err:${item.id}`));
  return { item, pin: pin.id };
}

async function boardId(env, H) {
  const saved = await env.SOCIAL.get(K(env, "board"));
  if (saved) return saved;
  let bookmark = "";
  for (let i = 0; i < 5; i++) {
    const r = await (await fetch(`${api(env)}/boards?page_size=100${bookmark ? `&bookmark=${encodeURIComponent(bookmark)}` : ""}`, { headers: H })).json().catch(() => ({}));
    const hit = (r.items || []).find((b) => (b.name || "").toLowerCase() === BOARD_NAME.toLowerCase());
    if (hit) { await env.SOCIAL.put(K(env, "board"), hit.id); return hit.id; }
    if (!r.bookmark) break;
    bookmark = r.bookmark;
  }
  const c = await (await fetch(`${api(env)}/boards`, { method: "POST", headers: H, body: JSON.stringify({
    name: BOARD_NAME, description: "Gameplay videos of BGameWorld's free daily puzzles. Can you solve them in a minute? Play free at bgameworld.com.", privacy: "PUBLIC",
  }) })).json().catch(() => ({}));
  if (!c.id) return null;
  await env.SOCIAL.put(K(env, "board"), c.id);
  return c.id;
}

// ---------------------------------------------------------------- tokens
async function tokenRequest(env, fields) {
  const res = await fetch(`${api(env)}/oauth/token`, {
    method: "POST",
    headers: { authorization: `Basic ${btoa(`${env.PINTEREST_APP_ID}:${env.PINTEREST_APP_SECRET}`)}`, "content-type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams(fields),
  });
  return res.json().catch(() => ({ error: `http_${res.status}` }));
}

async function saveAuth(env, d, now, prev = {}) {
  await env.SOCIAL.put(K(env, "auth"), JSON.stringify({
    access_token: d.access_token,
    expires_at: now + (Number(d.expires_in) || 2592000) * 1000,
    refresh_token: d.refresh_token || prev.refresh_token,
    refresh_expires_at: d.refresh_token_expires_at ? Number(d.refresh_token_expires_at) * 1000
      : d.refresh_token_expires_in ? now + Number(d.refresh_token_expires_in) * 1000 : prev.refresh_expires_at,
    scope: d.scope || prev.scope,
    updated_at: new Date(now).toISOString(),
  }));
}

async function accessToken(env, now) {
  const raw = await env.SOCIAL.get(K(env, "auth"));
  if (!raw) return null;
  const a = JSON.parse(raw);
  // Refresh with a week to spare; the continuous refresh token lasts 60 days and renews on every refresh.
  if (a.expires_at - now > 7 * 86400 * 1000) return a.access_token;
  const d = await tokenRequest(env, { grant_type: "refresh_token", refresh_token: a.refresh_token });
  if (!d.access_token) {
    await env.SOCIAL.put(K(env, "err:auth"), JSON.stringify({ at: new Date(now).toISOString(), message: d.message || d.error || "refresh failed" }), { expirationTtl: ERROR_TTL });
    return a.expires_at > now ? a.access_token : null;
  }
  await saveAuth(env, d, now, a);
  await env.SOCIAL.delete(K(env, "err:auth"));
  return d.access_token;
}

// ---------------------------------------------------------------- status (no tokens)
export async function pinterestStatus(env) {
  const out = { configured: configured(env), mode: mode(env), connected: false, paused: (await env.SOCIAL.get("PINTEREST_PAUSED")) === "1", videos: [] };
  const raw = await env.SOCIAL.get(K(env, "auth"));
  if (raw) { const a = JSON.parse(raw); out.connected = true; out.token_refreshed_at = a.updated_at; out.scope = a.scope; }
  const ae = await env.SOCIAL.get(K(env, "err:auth"));
  if (ae) out.auth_error = JSON.parse(ae);
  out.board_id = await env.SOCIAL.get(K(env, "board"));
  for (const q of queue) {
    const r = JSON.parse((await env.SOCIAL.get(K(env, `v:${q.id}`))) || "null");
    const e = await env.SOCIAL.get(K(env, `err:${q.id}`));
    const row = { id: q.id, level: q.level, state: r ? (r.stage === "pinned" ? "pinned" : "processing") : "queued" };
    if (r && r.pin_id) { row.pin_id = r.pin_id; row.pinned_at = r.pinned_at; }
    if (e) row.last_error = JSON.parse(e);
    out.videos.push(row);
  }
  return out;
}

// ---------------------------------------------------------------- helpers
async function fail(env, item, step, d, now) {
  if (["register", "read video", "upload"].includes(step)) await env.SOCIAL.put(K(env, "backoff"), "1", { expirationTtl: 7200 });
  const msg = d.message || (d.error && (d.error.message || d.error)) || "Unexpected response from Pinterest";
  await env.SOCIAL.put(K(env, `err:${item.id}`), JSON.stringify({ at: new Date(now).toISOString(), step, message: msg, code: d.code }), { expirationTtl: ERROR_TTL });
  return { item, error: `${step}: ${msg}` };
}

function randomHex(n) {
  const b = new Uint8Array(n); crypto.getRandomValues(b);
  return Array.from(b, (x) => x.toString(16).padStart(2, "0")).join("");
}

async function sameText(a, b) {
  const enc = new TextEncoder();
  const [x, y] = (await Promise.all([crypto.subtle.digest("SHA-256", enc.encode(a)), crypto.subtle.digest("SHA-256", enc.encode(b))])).map((h) => new Uint8Array(h));
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
