/* "Save your progress": invites guests to make a free account, on every
   BGameWorld game. Loaded by visit.js.

   When it shows:
   - right after a guest finishes a game (the moment they have something to keep), or
   - when a guest who has already played 2+ games opens any game,
   at most once a day, and never again after "Don't ask again".
   Someone who started signing up but hasn't confirmed their email instead gets
   a small reminder with a "send the link again" button.

   The account is the guest's own account, upgraded in place, so every score
   and streak they already have stays. One account works on every game. */
(function () {
  if (window.__bgwAccount) return;
  window.__bgwAccount = true;

  var SB_URL = "https://hkcvtoozpeybwehqtiif.supabase.co";
  var SB_KEY = "sb_publishable_CGTFNipWN_1IeG28m4upSg_n2HSsGai";
  var DAY = 864e5;

  function store(k, v) {
    try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; }
  }
  if (store("bgw-acct-never") === "1") return;

  function cookie(name) {
    var pre = name + "=", parts = document.cookie.split("; ");
    for (var i = 0; i < parts.length; i++) if (parts[i].indexOf(pre) === 0) return parts[i].slice(pre.length);
    return null;
  }
  function session() {
    var raw = "", v;
    for (var i = 0; (v = cookie("bgw-auth." + i)) !== null; i++) raw += v;
    if (!raw) { try { raw = localStorage.getItem("bgw-auth") || ""; } catch (e) { /* none */ } } else raw = decodeURIComponent(raw);
    try {
      var s = JSON.parse(raw);
      return s && s.access_token && s.expires_at * 1000 > Date.now() + 15000 ? s : null;
    } catch (e) { return null; }
  }
  function api(path, opts) {
    var s = session();
    if (!s) return Promise.reject(new Error("no session"));
    opts = opts || {};
    opts.headers = { "Content-Type": "application/json", apikey: SB_KEY, Authorization: "Bearer " + s.access_token };
    return fetch(SB_URL + path, opts).then(function (r) {
      return r.text().then(function (t) {
        var body = null;
        try { body = t ? JSON.parse(t) : null; } catch (e) { body = t; }
        if (!r.ok) {
          var msg = (body && (body.msg || body.message || body.error_description || body.error)) || "Something went wrong. Please try again.";
          throw new Error(msg);
        }
        return body;
      });
    });
  }
  function status() { return api("/rest/v1/rpc/bgw_guest_status", { method: "POST", body: "{}" }); }

  // ---------- the panel ----------
  var host, root;
  var CSS = ":host{all:initial}" +
    ".wrap{position:fixed;left:0;right:0;bottom:0;z-index:2147483000;display:flex;justify-content:center;padding:0 12px 12px;pointer-events:none;font:15px/1.45 system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;color:#15171a}" +
    ".card{pointer-events:auto;width:100%;max-width:440px;background:#fff;border:1px solid #e3e5ea;border-radius:16px;box-shadow:0 12px 40px rgba(0,0,0,.22);padding:18px 18px 16px;animation:up .28s ease-out;box-sizing:border-box;max-height:calc(100vh - 24px);overflow:auto}" +
    "@keyframes up{from{transform:translateY(24px);opacity:0}to{transform:none;opacity:1}}" +
    ".x{float:right;border:0;background:none;font-size:22px;line-height:1;color:#6b717c;cursor:pointer;padding:2px 4px;margin:-4px -4px 0 8px}" +
    "h2{font-size:19px;line-height:1.25;margin:0 0 6px;font-weight:700}" +
    "p{margin:0 0 12px;color:#3f444d}" +
    "ul{margin:0 0 14px;padding:0;list-style:none}li{padding-left:24px;position:relative;margin:4px 0;color:#3f444d}li:before{content:'\\2713';position:absolute;left:2px;color:#1e7d4a;font-weight:700}" +
    "label{display:block;font-size:13px;font-weight:600;margin:10px 0 4px;color:#3f444d}" +
    "input{box-sizing:border-box;width:100%;font:inherit;padding:10px 12px;border:1px solid #cfd3da;border-radius:10px;background:#fff;color:#15171a}" +
    "input:focus{outline:2px solid #2860d8;outline-offset:0;border-color:#2860d8}" +
    ".go{display:block;width:100%;margin-top:14px;padding:12px;border:0;border-radius:10px;background:#1e7d4a;color:#fff;font:inherit;font-weight:700;cursor:pointer}" +
    ".go:disabled{opacity:.6;cursor:default}" +
    ".row{display:flex;gap:10px;margin-top:10px}.row button{flex:1}" +
    ".lnk{border:0;background:none;color:#3f444d;font:inherit;font-size:13.5px;text-decoration:underline;cursor:pointer;padding:6px}" +
    ".err{color:#b3261e;font-size:13.5px;margin:10px 0 0}" +
    ".small{font-size:12.5px;color:#6b717c;margin:10px 0 0;text-align:center}" +
    "@media (prefers-color-scheme:dark){.card{background:#1a1d23;border-color:#2c3039;color:#eef0f3}p,li,label,.lnk{color:#c6cad2}input{background:#111317;border-color:#3a3f4a;color:#eef0f3}.x,.small{color:#8f95a0}}";

  function close() {
    if (host) host.remove();
    host = root = null;
  }
  function open(html, wire) {
    close();
    host = document.createElement("div");
    host.setAttribute("data-bgw", "account");
    root = host.attachShadow ? host.attachShadow({ mode: "open" }) : host;
    root.innerHTML = "<style>" + CSS + "</style><div class='wrap'><div class='card' role='dialog' aria-label='Save your progress'>" +
      "<button class='x' type='button' aria-label='Close'>&times;</button>" + html + "</div></div>";
    document.body.appendChild(host);
    root.querySelector(".x").onclick = function () { store("bgw-acct-last", String(Date.now())); close(); };
    if (wire) wire(root);
  }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }

  function showInvite(plays, justWon) {
    store("bgw-acct-last", String(Date.now()));
    open(
      "<h2>" + (justWon ? "Nice one! Save your progress" : "Keep your progress safe") + "</h2>" +
      "<p>You've played " + plays + " game" + (plays === 1 ? "" : "s") + " as a guest. If you clear your browser or change phones, it's gone. A free account keeps it.</p>" +
      "<ul><li>Your streaks and scores on every device</li><li>Your name on the daily leaderboards</li><li>One account for all BGameWorld games</li></ul>" +
      "<form novalidate>" +
      "<label for='n'>Your name on the leaderboard</label><input id='n' maxlength='20' autocomplete='nickname' placeholder='e.g. WordWizard'>" +
      "<label for='e'>Email</label><input id='e' type='email' autocomplete='email' placeholder='you@example.com'>" +
      "<label for='p'>Password</label><input id='p' type='password' autocomplete='new-password' placeholder='At least 6 characters'>" +
      "<div class='err' role='alert'></div>" +
      "<button class='go' type='submit'>Save my progress &ndash; it's free</button></form>" +
      "<div class='row'><button class='lnk' type='button' data-later>Maybe later</button><button class='lnk' type='button' data-never>Don't ask again</button></div>",
      function (r) {
        var err = r.querySelector(".err"), btn = r.querySelector(".go");
        r.querySelector("[data-later]").onclick = close;
        r.querySelector("[data-never]").onclick = function () { store("bgw-acct-never", "1"); close(); };
        r.querySelector("form").onsubmit = function (ev) {
          ev.preventDefault();
          var name = r.querySelector("#n").value.trim(), email = r.querySelector("#e").value.trim(), pw = r.querySelector("#p").value;
          err.textContent = "";
          if (name.length < 2) return (err.textContent = "Please choose a name (2 to 20 characters).");
          if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return (err.textContent = "Please enter a valid email address.");
          if (pw.length < 6) return (err.textContent = "Please choose a password of at least 6 characters.");
          btn.disabled = true; btn.textContent = "Saving...";
          api("/rest/v1/rpc/bgw_set_display_name", { method: "POST", body: JSON.stringify({ p_display_name: name }) })
            .then(function () {
              return api("/auth/v1/user?redirect_to=" + encodeURIComponent(location.origin + "/"), {
                method: "PUT", body: JSON.stringify({ email: email, password: pw }),
              });
            })
            .then(function () { showCheckEmail(email, true); })
            .catch(function (e) {
              var m = e.message || "";
              if (/already (been )?registered|exists/i.test(m)) m = "That email already has an account. Log in from the game's menu instead.";
              else if (/rate limit|too many/i.test(m)) m = "Too many sign-ups right now. Please try again in a few minutes.";
              err.textContent = m;
              btn.disabled = false; btn.innerHTML = "Save my progress &ndash; it's free";
            });
        };
        setTimeout(function () { var n = r.querySelector("#n"); if (n && window.innerWidth > 640) n.focus(); }, 300);
      }
    );
  }

  function showCheckEmail(email, fresh) {
    open(
      "<h2>" + (fresh ? "Check your email" : "Finish signing up") + "</h2>" +
      "<p>" + (fresh ? "We sent" : "We sent") + " a confirmation link to <b>" + esc(email) + "</b>. Tap it to finish. " +
      "Can't see it? Look in your spam or promotions folder. It comes from Supabase Auth.</p>" +
      "<p>Your progress is already saved on this device while you wait.</p>" +
      "<div class='err' role='status'></div>" +
      "<button class='go' type='button' data-ok>" + (fresh ? "Got it, keep playing" : "Keep playing") + "</button>" +
      "<div class='row'><button class='lnk' type='button' data-resend>Send the link again</button><button class='lnk' type='button' data-other>Use a different email</button></div>",
      function (r) {
        var msg = r.querySelector(".err");
        r.querySelector("[data-ok]").onclick = close;
        r.querySelector("[data-other]").onclick = function () { status().then(function (s) { showInvite((s && s.plays) || 0, false); }); };
        r.querySelector("[data-resend]").onclick = function () {
          msg.style.color = ""; msg.textContent = "Sending...";
          api("/auth/v1/user?redirect_to=" + encodeURIComponent(location.origin + "/"), { method: "PUT", body: JSON.stringify({ email: email }) })
            .then(function () { msg.style.color = "#1e7d4a"; msg.textContent = "Sent. Check your inbox and spam folder."; })
            .catch(function (e) { msg.style.color = ""; msg.textContent = /rate|seconds/i.test(e.message) ? "Please wait a minute before sending it again." : e.message; });
        };
      }
    );
  }

  // ---------- when to show it ----------
  var lastPlays = null, timer = null;
  function quietToday() { return Date.now() - Number(store("bgw-acct-last") || 0) < DAY; }
  function busy() {
    // Don't cover the game's own sign-up or menu dialogs.
    return !!document.querySelector('[role="dialog"][aria-modal="true"]') || !!host;
  }

  function check(first) {
    if (document.hidden) return;
    status().then(function (s) {
      if (!s || !s.guest) { if (s && !s.guest) stop(); return; }
      var justWon = lastPlays !== null && s.plays > lastPlays;
      lastPlays = s.plays;
      if (busy()) return;
      if (s.pending_email) {
        if (first && !quietToday()) { store("bgw-acct-last", String(Date.now())); showCheckEmail(s.pending_email, false); }
        return;
      }
      if (justWon && (!quietToday() || !store("bgw-acct-won-" + new Date().toDateString()))) {
        store("bgw-acct-won-" + new Date().toDateString(), "1");
        setTimeout(function () { if (!busy()) showInvite(s.plays, true); }, 2500); // let them see their result first
      } else if (first && s.plays >= 2 && !quietToday()) {
        showInvite(s.plays, false);
      }
    }).catch(function () { /* no session yet, or offline */ });
  }
  function stop() { if (timer) clearInterval(timer); timer = null; }

  setTimeout(function () {
    check(true);
    timer = setInterval(function () { check(false); }, 20000);
    document.addEventListener("visibilitychange", function () { if (!document.hidden) check(false); });
  }, 6000);
})();
