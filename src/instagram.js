// Instagram posts through the Instagram API with Instagram Login (graph.instagram.com).
//
// Setup (once):
//   1. The Instagram account is a Professional account (Business or Creator).
//   2. In the Meta app (developers.facebook.com, a Business-type app): add the use case
//      "Manage messaging & content on Instagram", open "API setup with Instagram login",
//      add the BGameWorld Instagram account and click "Generate token".
//   3. Cloudflare secret INSTAGRAM_TOKEN = that token.
// The token lasts 60 days. This file refreshes it every few days and keeps the newest one in KV
// (ig:token), so it never runs out. Pasting a new token into Cloudflare always replaces it.
//
// What it posts: src/instagram.json (made by tools/social/instagram.py), each item at its time,
// within 6 hours, so an outage never dumps a backlog:
//   carousel  two JPEG slides from /social/ig/ (the puzzle, then the answer)
//   reel      a puzzle Short from /social/shorts/
// Instagram fetches the files from this site, then processes them; a Reel can take a minute or
// two, so a post may finish on the next 30-minute run. Pause: KV key INSTAGRAM_PAUSED = 1 (or PAUSED).
import items from "./instagram.json";

const API = "https://graph.instagram.com/v26.0";
const SITE = "https://bgameworld.com";
const WINDOW_MS = 6 * 60 * 60 * 1000;
const REFRESH_MS = 3 * 24 * 60 * 60 * 1000;     // refresh well before the 60 days run out (Instagram needs it to be a day old)
const ERROR_TTL = 14 * 24 * 60 * 60;
const MAX_PER_RUN = 3;

// ---------------------------------------------------------------- the scheduled run
export async function instagramDue(env, now) {
  if (!env.INSTAGRAM_TOKEN) return;
  if ((await env.SOCIAL.get("PAUSED")) === "1" || (await env.SOCIAL.get("INSTAGRAM_PAUSED")) === "1") return;
  const t = await refreshIfOld(env, await currentToken(env), now);
  const acct = await account(env, t);
  if (!acct) return;
  let n = 0;
  for (const it of items) {
    const at = Date.parse(it.at);
    if (at > now || now - at > WINDOW_MS) continue;
    if (await env.SOCIAL.get(`ig:s:${it.id}`)) continue;
    if (await env.SOCIAL.get(`ig:claim:${it.id}`)) continue;     // another run is on it
    if (++n > MAX_PER_RUN) break;
    await env.SOCIAL.put(`ig:claim:${it.id}`, "1", { expirationTtl: 600 });
    try {
      await step(env, t.token, acct, it, now);
    } catch (e) {
      await env.SOCIAL.put(`ig:err:${it.id}`, JSON.stringify({ at: new Date().toISOString(), message: String(e && e.message || e) }), { expirationTtl: ERROR_TTL });
    } finally {
      await env.SOCIAL.delete(`ig:claim:${it.id}`);
    }
  }
}

// One item moves on as far as it can: make the container, then publish it once Instagram has it ready.
async function step(env, token, acct, it, now) {
  const ck = `ig:c:${it.id}`;
  let c = JSON.parse((await env.SOCIAL.get(ck)) || "null");
  if (!c) {
    c = { id: await createContainer(token, acct, it), made_at: new Date(now).toISOString() };
    await env.SOCIAL.put(ck, JSON.stringify(c), { expirationTtl: 86400 });
  }
  const st = await get(`/${c.id}?fields=status_code,status`, token);
  if (st.status_code === "PUBLISHED") return done(env, it, { media_id: null });   // published, but the last run didn't get to note it
  if (st.status_code === "ERROR" || st.status_code === "EXPIRED") {
    await env.SOCIAL.delete(ck);                                                      // start again with a fresh one next run
    throw new Error(`Instagram couldn't process this ${it.kind} (${st.status || st.status_code})`);
  }
  if (st.status_code !== "FINISHED") return;                                         // still processing: try again next run
  const pub = await post(`/${acct.user_id}/media_publish`, { creation_id: c.id }, token);
  let permalink = null;
  try { permalink = (await get(`/${pub.id}?fields=permalink`, token)).permalink || null; } catch (_) {}
  await done(env, it, { media_id: pub.id, permalink });
}

async function done(env, it, r) {
  await env.SOCIAL.put(`ig:s:${it.id}`, JSON.stringify({ ...r, posted_at: new Date().toISOString() }));
  await env.SOCIAL.delete(`ig:c:${it.id}`);
  await env.SOCIAL.delete(`ig:err:${it.id}`);
}

async function createContainer(token, acct, it) {
  const me = `/${acct.user_id}/media`;
  if (it.kind === "reel") {
    return (await post(me, { media_type: "REELS", video_url: `${SITE}/${it.video}`, caption: it.caption, share_to_feed: "true" }, token)).id;
  }
  const children = [];
  for (const img of it.images) children.push((await post(me, { image_url: `${SITE}/${img}`, is_carousel_item: "true" }, token)).id);
  return (await post(me, { media_type: "CAROUSEL", children: children.join(","), caption: it.caption }, token)).id;
}

// ---------------------------------------------------------------- the token and the account
async function currentToken(env) {
  const from = await fingerprint(env.INSTAGRAM_TOKEN);
  let t = JSON.parse((await env.SOCIAL.get("ig:token")) || "null");
  if (!t || t.from !== from) {                      // first run, or a new token was pasted into Cloudflare
    t = { token: env.INSTAGRAM_TOKEN, from, since: Date.now() };
    await env.SOCIAL.put("ig:token", JSON.stringify(t));
    await env.SOCIAL.delete("ig:me");
  }
  return t;
}

async function refreshIfOld(env, t, now) {
  if (now - (t.refreshed_at || t.since) < REFRESH_MS) return t;
  if (await env.SOCIAL.get("ig:refresh_wait")) return t;
  await env.SOCIAL.put("ig:refresh_wait", "1", { expirationTtl: 6 * 3600 });     // at most one try every 6 hours
  const r = await fetch(`https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=${encodeURIComponent(t.token)}`);
  const d = await r.json().catch(() => ({}));
  if (!d.access_token) {
    await env.SOCIAL.put("ig:err:token", JSON.stringify({ at: new Date().toISOString(), message: (d.error && d.error.message) || `refresh failed (${r.status})` }), { expirationTtl: ERROR_TTL });
    return t;
  }
  t = { ...t, token: d.access_token, refreshed_at: now, expires_at: now + (d.expires_in || 5184000) * 1000 };
  await env.SOCIAL.put("ig:token", JSON.stringify(t));
  await env.SOCIAL.delete("ig:err:token");
  return t;
}

async function account(env, t) {
  const cached = await env.SOCIAL.get("ig:me");
  if (cached) return JSON.parse(cached);
  try {
    const d = await get("/me?fields=user_id,username", t.token);
    const a = { user_id: d.user_id || d.id, username: d.username };
    await env.SOCIAL.put("ig:me", JSON.stringify(a));
    await env.SOCIAL.delete("ig:err:auth");
    return a;
  } catch (e) {
    await env.SOCIAL.put("ig:err:auth", JSON.stringify({ at: new Date().toISOString(), message: String(e && e.message || e) }), { expirationTtl: ERROR_TTL });
    return null;
  }
}

// ---------------------------------------------------------------- status (never shows the token)
export async function instagramStatus(env, now) {
  const out = { configured: Boolean(env.INSTAGRAM_TOKEN), paused: (await env.SOCIAL.get("INSTAGRAM_PAUSED")) === "1", posts: [] };
  if (out.configured) {
    const t = await currentToken(env);
    const a = await account(env, t);                // checks the connection straight away after the secret is added
    out.connected = Boolean(a);
    if (a) out.account = a.username;
    if (t.refreshed_at) out.token_refreshed_at = new Date(t.refreshed_at).toISOString();
    if (t.expires_at) out.token_expires_at = new Date(t.expires_at).toISOString();
  }
  for (const k of ["auth", "token"]) {
    const e = await env.SOCIAL.get(`ig:err:${k}`);
    if (e) out[`${k}_error`] = JSON.parse(e);
  }
  for (const it of items) {
    const at = Date.parse(it.at);
    const s = await env.SOCIAL.get(`ig:s:${it.id}`);
    const err = await env.SOCIAL.get(`ig:err:${it.id}`);
    if (now - at > 3 * 86400000 && !s && !err) continue;      // old and never posted: leave it out
    const waiting = await env.SOCIAL.get(`ig:c:${it.id}`);
    const state = s ? "posted" : waiting ? "processing" : at > now ? "scheduled" : now - at <= WINDOW_MS ? "due" : "missed";
    const row = { id: it.id, at: it.at, kind: it.kind, state };
    if (s) { const r = JSON.parse(s); row.url = r.permalink; row.posted_at = r.posted_at; }
    if (err) row.last_error = JSON.parse(err);
    out.posts.push(row);
  }
  return out;
}

// ---------------------------------------------------------------- helpers
async function get(path, token) {
  const r = await fetch(`${API}${path}${path.includes("?") ? "&" : "?"}access_token=${encodeURIComponent(token)}`);
  return check(r);
}

async function post(path, params, token) {
  const r = await fetch(`${API}${path}`, { method: "POST", body: new URLSearchParams({ ...params, access_token: token }) });
  return check(r);
}

async function check(r) {
  const d = await r.json().catch(() => ({}));
  if (!r.ok || d.error) {
    const e = d.error || {};
    throw new Error(`${e.message || `Instagram said ${r.status}`}${e.code ? ` (code ${e.code}${e.error_subcode ? `/${e.error_subcode}` : ""})` : ""}`);
  }
  return d;
}

async function fingerprint(s) {
  const h = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(String(s)));
  return [...new Uint8Array(h)].slice(0, 8).map((b) => b.toString(16).padStart(2, "0")).join("");
}
