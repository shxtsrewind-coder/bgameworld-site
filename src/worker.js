// BGameWorld site Worker.
//
// The site itself is still plain static files (served straight from assets).
// This Worker adds two things:
//   1. Every 30 minutes (cron), it posts any Facebook puzzle from posts.json
//      whose time has come, using the Page ID and Page token stored as
//      Cloudflare secrets (FB_PAGE_ID, FB_PAGE_TOKEN).
//   2. GET /api/social/status shows what has been posted, what is scheduled
//      and any errors. It never shows the token.
//
//   3. TikTok drafts (src/tiktok.js): at each TikTok puzzle's time it sends the
//      slideshow to the connected account's TikTok inbox, ready to post.
//
// To pause posting: in the SOCIAL KV namespace, set the key PAUSED to 1.
// Delete the key (or set it to 0) to resume.
import posts from "./posts.json";
import { tiktokRoute, tiktokDue, tiktokStatus } from "./tiktok.js";

const GRAPH = "https://graph.facebook.com/v26.0";
const SITE = "https://bgameworld.com";
// A post is only sent within 6 hours of its time, so a long outage never
// dumps a backlog of old puzzles onto the Page at once.
const WINDOW_MS = 6 * 60 * 60 * 1000;
const ERROR_TTL = 14 * 24 * 60 * 60;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/social/status") return status(env);
    if (url.pathname.startsWith("/api/tiktok/")) return tiktokRoute(request, env, url);
    return env.ASSETS.fetch(request);
  },

  async scheduled(event, env, ctx) {
    const now = Date.now();
    ctx.waitUntil(Promise.all([postDue(env, now), tiktokDue(env, now)]));
  },
};

async function postDue(env, now) {
  if (!env.FB_PAGE_ID || !env.FB_PAGE_TOKEN) return;
  if ((await env.SOCIAL.get("PAUSED")) === "1") return;

  for (const p of posts) {
    const at = Date.parse(p.at);
    if (at > now || now - at > WINDOW_MS) continue;

    const key = `fb:${p.id}`;
    if (await env.SOCIAL.get(key)) continue;
    // Claim it first so an overlapping run can't post it twice.
    await env.SOCIAL.put(key, "posting", { expirationTtl: 3600 });

    try {
      const body = new URLSearchParams({
        url: `${SITE}/social/fb/${p.id}.png`,
        message: p.caption,
        access_token: env.FB_PAGE_TOKEN,
      });
      const res = await fetch(`${GRAPH}/${env.FB_PAGE_ID}/photos`, { method: "POST", body });
      const data = await res.json().catch(() => ({}));

      if (res.ok && (data.post_id || data.id)) {
        await env.SOCIAL.put(key, JSON.stringify({
          post_id: data.post_id || data.id,
          posted_at: new Date().toISOString(),
        }));
        await env.SOCIAL.delete(`err:${p.id}`);
      } else {
        // Release the claim so the next run retries (inside the 6-hour window).
        await env.SOCIAL.delete(key);
        const e = data.error || {};
        await env.SOCIAL.put(`err:${p.id}`, JSON.stringify({
          at: new Date().toISOString(),
          status: res.status,
          message: e.message || "Unexpected response from Facebook",
          code: e.code,
          type: e.type,
        }), { expirationTtl: ERROR_TTL });
      }
    } catch (err) {
      await env.SOCIAL.delete(key);
      await env.SOCIAL.put(`err:${p.id}`, JSON.stringify({
        at: new Date().toISOString(),
        message: String(err && err.message ? err.message : err),
      }), { expirationTtl: ERROR_TTL });
    }
  }
}

async function status(env) {
  const now = Date.now();
  const out = {
    facebook_configured: Boolean(env.FB_PAGE_ID && env.FB_PAGE_TOKEN),
    paused: (await env.SOCIAL.get("PAUSED")) === "1",
    now: new Date(now).toISOString(),
    posts: [],
  };
  for (const p of posts) {
    const done = await env.SOCIAL.get(`fb:${p.id}`);
    const err = await env.SOCIAL.get(`err:${p.id}`);
    const at = Date.parse(p.at);
    let state;
    if (done && done !== "posting") state = "posted";
    else if (done === "posting") state = "posting";
    else if (at > now) state = "scheduled";
    else if (now - at <= WINDOW_MS) state = "due";
    else state = "missed";
    const row = { id: p.id, game: p.game, at: p.at, state };
    if (done && done !== "posting") row.facebook = JSON.parse(done);
    if (err) row.last_error = JSON.parse(err);
    out.posts.push(row);
  }
  out.tiktok = await tiktokStatus(env, now);
  return new Response(JSON.stringify(out, null, 2), {
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });
}
