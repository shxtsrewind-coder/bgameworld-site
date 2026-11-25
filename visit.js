/* Records where a visitor came from (Google, Facebook, WhatsApp, another
   BGameWorld page...), once per browser tab per site, for the admin page.
   Loaded by bgameworld.com and every game subdomain:
     <script src="https://bgameworld.com/visit.js" defer></script>
   Sends only: the site and page, the referring site, and any ?ref= / utm_ tag.
   Waits a few seconds so a guest's game account exists and the visit can be
   linked to the player (and so to their location and the games they played). */
(function () {
  var SB_URL = "https://hkcvtoozpeybwehqtiif.supabase.co";
  var SB_KEY = "sb_publishable_CGTFNipWN_1IeG28m4upSg_n2HSsGai";
  var host = location.hostname;
  if (!/(^|\.)bgameworld\.com$/.test(host)) return; // not on the live site
  if (navigator.webdriver) return; // automated browsers
  var once = "bgw-visit:" + host;
  try { if (sessionStorage.getItem(once)) return; sessionStorage.setItem(once, "1"); } catch (e) { return; }

  var q = new URLSearchParams(location.search);
  var info = {
    p_site: host,
    p_path: location.pathname,
    p_referrer: document.referrer || null,
    p_tag: q.get("ref") || q.get("utm_source") || q.get("src") || null,
    p_medium: q.get("utm_medium"),
    p_campaign: q.get("utm_campaign"),
  };

  function cookie(name) {
    var pre = name + "=", parts = document.cookie.split("; ");
    for (var i = 0; i < parts.length; i++) if (parts[i].indexOf(pre) === 0) return parts[i].slice(pre.length);
    return null;
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

  var tries = 0, sent = false;
  function send(now) {
    if (sent) return;
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
})();
