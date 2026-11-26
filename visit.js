/* Records where a visitor came from (Google, Pinterest, WhatsApp...), once per
   browser tab per site, for the admin page. Loaded by bgameworld.com and every
   game subdomain:
     <script src="https://bgameworld.com/visit.js" defer></script>
   Sends only: the site and page, the referring site, and any ?ref= / utm_ tag.
   Waits a few seconds so a guest's game account exists and the visit can be
   linked to the player (and so to their location and the games they played).
   Also loads the "save your progress" prompt for guests (account.js). */
(function () {
  var SB_URL = "https://hkcvtoozpeybwehqtiif.supabase.co";
  var SB_KEY = "sb_publishable_CGTFNipWN_1IeG28m4upSg_n2HSsGai";
  var host = location.hostname;
  if (!/(^|\.)bgameworld\.com$/.test(host)) return; // not on the live site
  if (navigator.webdriver) return; // automated browsers
  // Crawlers and scripted browsers aren't visitors. (The server checks again.)
  // ("Googlebot/2.1" yes, but not phones like "Cubot X50".)
  if (/\bbot\b|[a-z]bot\/|crawl|spider|slurp|headless|lighthouse|pagespeed|facebookexternalhit|python-|curl\/|wget\//i.test(navigator.userAgent)) return;

  // Offer guests an account (not on the admin page or the answer pages).
  if (!/^\/(admin|a)\//.test(location.pathname)) {
    var s = document.createElement("script");
    s.src = "https://bgameworld.com/account.js";
    s.defer = true;
    document.head.appendChild(s);
  }

  var once = "bgw-visit:" + host;
  try { if (sessionStorage.getItem(once)) return; sessionStorage.setItem(once, "1"); } catch (e) { return; }

  function cookie(name) {
    var pre = name + "=", parts = document.cookie.split("; ");
    for (var i = 0; i < parts.length; i++) if (parts[i].indexOf(pre) === 0) return parts[i].slice(pre.length);
    return null;
  }

  var q = new URLSearchParams(location.search);
  var info = {
    p_site: host,
    p_path: location.pathname,
    p_referrer: document.referrer || null,
    p_tag: q.get("ref") || q.get("utm_source") || q.get("src") || null,
    p_medium: q.get("utm_medium"),
    p_campaign: q.get("utm_campaign"),
    p_content: q.get("utm_content"), // which post or Pin, e.g. p047
  };

  // Where the person first arrived from, kept for 30 minutes across all
  // *.bgameworld.com sites. A click from an answer page into a game then counts
  // for Pinterest (or wherever they came from), not for the tag written into
  // our own link.
  var refHost = "";
  try { refHost = new URL(document.referrer).hostname; } catch (e) { /* no referrer */ }
  var internal = /(^|\.)bgameworld\.com$/.test(refHost);
  if (internal) {
    var entry = null;
    try { entry = JSON.parse(decodeURIComponent(cookie("bgw-entry") || "")); } catch (e) { /* none */ }
    if (entry) { info.p_referrer = entry.r; info.p_tag = entry.t; info.p_medium = entry.m; info.p_campaign = entry.c; info.p_content = entry.n || null; }
    else { info.p_tag = info.p_medium = info.p_campaign = info.p_content = null; }
  } else if (info.p_referrer || info.p_tag) {
    var val = encodeURIComponent(JSON.stringify({
      r: (info.p_referrer || "").slice(0, 200) || null, t: info.p_tag, m: info.p_medium, c: info.p_campaign,
      // the post they came from (or the answer page they landed on)
      n: (info.p_content || (location.pathname.match(/^\/a\/(p\d+)/) || [])[1] || null),
    }));
    document.cookie = "bgw-entry=" + val + "; Domain=.bgameworld.com; Path=/; Max-Age=1800; SameSite=Lax; Secure";
  }

  // The shared sign-in (see shared-auth.js) keeps the session in cookies bgw-auth.0, bgw-auth.1, ...
  function token() {
    var raw = "", v;
    for (var i = 0; (v = cookie("bgw-auth." + i)) !== null; i++) raw += v;
    if (!raw) return null;
    try {
      var s = JSON.parse(decodeURIComponent(raw));
      return s && s.access_token && s.expires_at * 1000 > Date.now() + 30000 ? s.access_token : null;
    } catch (e) { return null; }
  }

  // Signs of a real browser, checked on the server too.
  info.p_signals = {
    webdriver: !!navigator.webdriver,
    langs: (navigator.languages || []).length,
    w: (window.screen && screen.width) || 0,
    h: (window.screen && screen.height) || 0,
    hop: internal, // came from another of our pages (so not a new click from outside)
  };

  // Count a page only once it has actually been on screen (not prerendered or
  // opened in the background by a crawler).
  var seen = document.visibilityState === "visible";
  if (!seen) document.addEventListener("visibilitychange", function onVis() {
    if (document.visibilityState === "visible") { seen = true; document.removeEventListener("visibilitychange", onVis); setTimeout(send, 1500); }
  });

  var tries = 0, sent = false;
  function send(now) {
    if (sent || !seen) return;
    var t = token();
    if (!t && !now && ++tries < 8) return setTimeout(send, 1000); // give the game a moment to sign the guest in
    sent = true;
    var h = { "Content-Type": "application/json", apikey: SB_KEY };
    if (t) h.Authorization = "Bearer " + t;
    fetch(SB_URL + "/rest/v1/rpc/log_visit", { method: "POST", keepalive: true, headers: h, body: JSON.stringify(info) })
      .catch(function () {});
  }
  setTimeout(send, 1500);
  addEventListener("pagehide", function () { send(true); }); // leaving early: record it anyway
  window.bgwVisitFlush = function () { send(true); }; // answer pages call this just before moving on to the game
})();
