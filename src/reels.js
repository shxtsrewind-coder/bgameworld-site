// Facebook Reels: gameplay videos posted to the BGameWorld Page on schedule.
//
// Uses the Page Reels API in three steps, the same Page token as the photo
// posts (FB_PAGE_ID, FB_PAGE_TOKEN):
//   1. start   POST /{page}/video_reels upload_phase=start      -> video_id
//   2. upload  POST rupload.facebook.com/video-upload/...  with the MP4 bytes
//              (read from this site's /social/reels/ files)
//   3. finish  POST /{page}/video_reels upload_phase=finish video_state=PUBLISHED
// If Facebook is still processing the video at step 3, the next run (30 min
// later) tries step 3 again, inside the 6-hour window.
//
// Schedule and captions: src/reels.json. Pause Reels only: KV key REELS_PAUSED = 1.
import reels from "./reels.json";

const GRAPH = "https://graph.facebook.com/v26.0";
const RUPLOAD = "https://rupload.facebook.com/video-upload/v26.0";
const SITE = "https://bgameworld.com";
const WINDOW_MS = 6 * 60 * 60 * 1000;
const CLAIM_MS = 15 * 60 * 1000;
const ERROR_TTL = 14 * 24 * 60 * 60;

export async function reelsDue(env, now) {
  if (!env.FB_PAGE_ID || !env.FB_PAGE_TOKEN) return;
  if ((await env.SOCIAL.get("PAUSED")) === "1" || (await env.SOCIAL.get("REELS_PAUSED")) === "1") return;
  const token = env.FB_PAGE_TOKEN;

  for (const r of reels) {
    const at = Date.parse(r.at);
    const key = `rl:${r.id}`;
    let rec = JSON.parse((await env.SOCIAL.get(key)) || "null");

    // Follow up on Reels published in the last day, for the status page.
    if (rec && rec.stage === "published") {
      if (!rec.final && now - at <= 24 * 60 * 60 * 1000) await followUp(env, key, rec, token, now);
      continue;
    }
    if (at > now || now - at > WINDOW_MS) continue;
    if (rec && rec.stage === "working" && now - rec.t < CLAIM_MS) continue;

    try {
      if (!rec || rec.stage === "working") {
        await env.SOCIAL.put(key, JSON.stringify({ stage: "working", t: now }), { expirationTtl: 3600 });
        const s = await post(`${GRAPH}/${env.FB_PAGE_ID}/video_reels`, { upload_phase: "start", access_token: token });
        if (!s.data.video_id) { await env.SOCIAL.delete(key); await fail(env, r.id, "start", s, now); continue; }
        // Send the file itself (Facebook couldn't fetch it from a file_url: 422 on Oct 19).
        const file = await env.ASSETS.fetch(new Request(`${SITE}/social/reels/${r.video}`));
        if (!file.ok) { await env.SOCIAL.delete(key); await fail(env, r.id, "read video", { status: file.status, data: { error: { message: "video file missing" } } }, now); continue; }
        const bytes = await file.arrayBuffer();
        const up = await fetch(s.data.upload_url || `${RUPLOAD}/${s.data.video_id}`, {
          method: "POST",
          headers: { authorization: `OAuth ${token}`, offset: "0", file_size: String(bytes.byteLength), "content-type": "application/octet-stream" },
          body: bytes,
        });
        const upData = await up.json().catch(() => ({}));
        if (!up.ok || !upData.success) { await env.SOCIAL.delete(key); await fail(env, r.id, "upload", { status: up.status, data: upData }, now); continue; }
        rec = { stage: "uploaded", video_id: s.data.video_id, t: now };
        await env.SOCIAL.put(key, JSON.stringify(rec));
      }
      const f = await post(`${GRAPH}/${env.FB_PAGE_ID}/video_reels`, {
        access_token: token, video_id: rec.video_id, upload_phase: "finish", video_state: "PUBLISHED", description: r.caption,
      });
      if (f.data.success) {
        await env.SOCIAL.put(key, JSON.stringify({ stage: "published", video_id: rec.video_id, published_at: new Date(now).toISOString(), post_id: f.data.post_id }));
        await env.SOCIAL.delete(`rlerr:${r.id}`);
      } else {
        await fail(env, r.id, "finish", f, now);   // stays "uploaded"; the next run tries to publish again
      }
    } catch (e) {
      if (!rec || rec.stage === "working") await env.SOCIAL.delete(key);
      await env.SOCIAL.put(`rlerr:${r.id}`, JSON.stringify({ at: new Date(now).toISOString(), message: String(e && e.message ? e.message : e) }), { expirationTtl: ERROR_TTL });
    }
  }
}

async function followUp(env, key, rec, token, now) {
  const res = await fetch(`${GRAPH}/${rec.video_id}?fields=status&access_token=${encodeURIComponent(token)}`);
  const d = await res.json().catch(() => ({}));
  if (!d.status) return;
  rec.video_status = d.status.video_status;
  rec.publish_status = d.status.publishing_phase && d.status.publishing_phase.publish_status;
  const perr = d.status.processing_phase && d.status.processing_phase.error;
  if (perr) rec.processing_error = perr.message || String(perr);
  rec.final = rec.video_status === "ready" || rec.video_status === "error" || rec.publish_status === "published";
  rec.checked_at = new Date(now).toISOString();
  await env.SOCIAL.put(key, JSON.stringify(rec));
}

async function post(url, fields) {
  const res = await fetch(url, { method: "POST", body: new URLSearchParams(fields) });
  return { status: res.status, data: await res.json().catch(() => ({})) };
}

async function fail(env, id, step, r, now) {
  const e = (r.data && (r.data.error || r.data.debug_info)) || {};   // rupload errors come back as debug_info
  await env.SOCIAL.put(`rlerr:${id}`, JSON.stringify({
    at: new Date(now).toISOString(), step, status: r.status, message: e.message || JSON.stringify(r.data || {}).slice(0, 300) || "Unexpected response from Facebook", code: e.code, type: e.type,
  }), { expirationTtl: ERROR_TTL });
}

export async function reelsStatus(env, now) {
  const out = { paused: (await env.SOCIAL.get("REELS_PAUSED")) === "1", reels: [] };
  for (const r of reels) {
    const rec = JSON.parse((await env.SOCIAL.get(`rl:${r.id}`)) || "null");
    const err = await env.SOCIAL.get(`rlerr:${r.id}`);
    const at = Date.parse(r.at);
    let state;
    if (rec && rec.stage === "published") state = "posted";
    else if (rec && rec.stage === "uploaded") state = "processing";
    else if (rec && rec.stage === "working") state = "posting";
    else if (at > now) state = "scheduled";
    else if (now - at <= WINDOW_MS) state = "due";
    else state = "missed";
    const row = { id: r.id, level: r.level, at: r.at, state };
    if (rec && rec.stage === "published") row.facebook = { video_id: rec.video_id, published_at: rec.published_at, video_status: rec.video_status, publish_status: rec.publish_status, processing_error: rec.processing_error };
    if (err) row.last_error = JSON.parse(err);
    out.reels.push(row);
  }
  return out;
}
