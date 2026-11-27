/* BGameWorld across every game. Loaded by visit.js on bgameworld.com and on
   every game site.

   1. Welcome: a new player, arriving on any page from any link, is asked once
      (for all BGameWorld sites, not per game) to make a free BGameWorld
      account or play as a guest. Accounts are made only on bgameworld.com/join/.
   2. Play next: when a game is finished (each game fires a "bgw:finished"
      event), suggest three other games, today's Daily Seven first. Guests also
      get a link to save their progress.
   3. Someone who started signing up but hasn't tapped the email link gets a
      small daily reminder. */
(function () {
  if (window.__bgwAccount) return;
  window.__bgwAccount = true;
  if (/^\/(join|admin|a)\//.test(location.pathname)) return;

  var SB_URL = "https://hkcvtoozpeybwehqtiif.supabase.co";
  var SB_KEY = "sb_publishable_CGTFNipWN_1IeG28m4upSg_n2HSsGai";
  var SITE = "https://bgameworld.com";
  var DAY = 864e5;

  // art id (same as on bgameworld.com), name, address, artwork, colour
  var GAMES = [
    ["wordezy", "Wordezy", "https://wordezy.bgameworld.com", "wordezy", "Guess the daily word in six tries."],
    ["wordsearch", "Wordezy Search", "https://wordezysearch.bgameworld.com", "wordezy-search", "Find the hidden words."],
    ["scramble", "Wordezy Scramble", "https://wordezyscramble.bgameworld.com", "wordezy-scramble", "Unscramble five words."],
    ["ladder", "Wordezy Ladder", "https://wordezyladder.bgameworld.com", "wordezy-ladder", "Change one letter at a time."],
    ["warmezy", "Warmezy", "https://warmezy.bgameworld.com", "warmezy", "Find the secret word by meaning."],
    ["letterezy", "Letterezy", "https://letterezy.bgameworld.com", "letterezy", "Spell words from a bag of letters."],
    ["lingoezy", "Lingoezy", "https://lingoezy.bgameworld.com", "lingoezy", "Dodge the false friends."],
    ["sortezy", "Sortezy", "https://sortezy.bgameworld.com", "sortezy", "Pour until every tube is one colour."],
    ["linkezy", "Linkezy", "https://linkezy.bgameworld.com", "linkezy", "Join the dots without crossing."],
    ["mergezy", "Mergezy", "https://mergezy.bgameworld.com", "mergezy", "Join three to merge them up."],
    ["timeguess", "When & Where", "https://whenandwhere.bgameworld.com", "when-and-where", "Date and place a real photo."],
  ].map(function (g) { return { art: g[0], name: g[1], url: g[2], guide: g[3], line: g[4] }; });
  var current = GAMES.filter(function (g) { return g.url.indexOf("//" + location.hostname) > 0; })[0];

  function store(k, v) {
    try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; }
  }
  function cookie(name) {
    var pre = name + "=", parts = document.cookie.split("; ");
    for (var i = 0; i < parts.length; i++) if (parts[i].indexOf(pre) === 0) return parts[i].slice(pre.length);
    return null;
  }
  function setCookie(name, val, maxAge) {
    var dom = /(^|\.)bgameworld\.com$/.test(location.hostname) ? "; Domain=.bgameworld.com" : "";
    document.cookie = name + "=" + val + dom + "; Path=/; Max-Age=" + maxAge + "; SameSite=Lax; Secure";
  }
  function session() {
    var raw = "", v;
    for (var i = 0; (v = cookie("bgw-auth." + i)) !== null; i++) raw += v;
    if (raw) raw = decodeURIComponent(raw); else { try { raw = localStorage.getItem("bgw-auth") || ""; } catch (e) { /* none */ } }
    try { return JSON.parse(raw); } catch (e) { return null; }
  }
  function token() {
    var s = session();
    return s && s.access_token && s.expires_at * 1000 > Date.now() + 15000 ? s.access_token : null;
  }
  function registered() { var s = session(); return !!(s && s.user && !s.user.is_anonymous); }
  function status() {
    var t = token();
    if (!t) return Promise.resolve(null);
    return fetch(SB_URL + "/rest/v1/rpc/bgw_guest_status", {
      method: "POST", body: "{}",
      headers: { "Content-Type": "application/json", apikey: SB_KEY, Authorization: "Bearer " + t },
    }).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; });
  }
  function joinUrl(mode) {
    return SITE + "/join/?" + (mode === "login" ? "mode=login&" : "") + "next=" + encodeURIComponent(location.href.split("#")[0]);
  }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }

  // ---------- one panel at a time, in a shadow root so game styles can't touch it ----------
  var host = null;
  var CSS = ":host{all:initial}" +
    "*{box-sizing:border-box}" +
    ".back{position:fixed;inset:0;z-index:2147483000;background:rgba(12,6,22,.62);display:flex;align-items:center;justify-content:center;padding:16px;font:15px/1.45 system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;color:#15171a;animation:fade .2s ease-out}" +
    ".back.sheet{background:none;align-items:flex-end;pointer-events:none;padding:0 12px 12px}" +
    "@keyframes fade{from{opacity:0}}@keyframes up{from{transform:translateY(24px);opacity:0}}" +
    ".card{pointer-events:auto;position:relative;width:100%;max-width:420px;background:#fff;border-radius:20px;padding:24px 20px 18px;box-shadow:0 24px 70px rgba(0,0,0,.35);max-height:calc(100vh - 24px);overflow:auto;animation:up .28s ease-out;text-align:center}" +
    ".x{position:absolute;top:8px;right:8px;width:36px;height:36px;border:0;border-radius:50%;background:none;font-size:22px;line-height:1;color:#6b717c;cursor:pointer}" +
    ".logo{width:128px;height:auto;display:block;margin:0 auto 10px}" +
    "h2{margin:0 0 6px;font-size:21px;line-height:1.25}" +
    "p{margin:0 0 14px;color:#3f444d}" +
    "ul{list-style:none;margin:0 0 16px;padding:0;text-align:left;display:grid;gap:5px}li{position:relative;padding-left:24px;color:#3f444d;font-size:14.5px}li:before{content:'\\2713';position:absolute;left:3px;color:#1e7d4a;font-weight:800}" +
    "a.primary,button.primary{display:block;width:100%;padding:13px;border:0;border-radius:12px;background:linear-gradient(90deg,#8b3dff,#d946ef);color:#fff;font:inherit;font-weight:700;text-decoration:none;cursor:pointer;margin-bottom:8px}" +
    "a.secondary{display:block;padding:12px;border-radius:12px;border:1px solid #d5d8de;color:#15171a;font-weight:600;text-decoration:none;margin-bottom:4px}" +
    "button.link,a.link{border:0;background:none;color:#5b6170;font:inherit;font-size:14px;text-decoration:underline;cursor:pointer;padding:8px;display:inline-block}" +
    ".games{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:4px 0 14px}" +
    ".g{display:block;text-decoration:none;color:#15171a;font-size:13px;font-weight:700;line-height:1.2}" +
    ".g img{display:block;width:100%;aspect-ratio:5/7;object-fit:cover;border-radius:12px;background:#24123a;margin-bottom:6px}" +
    ".g .tag{display:block;font-size:11px;font-weight:700;color:#a1460f;margin-top:2px}" +
    ".save{border-top:1px solid #eceef2;margin-top:4px;padding-top:12px;font-size:14px;color:#3f444d}" +
    ".save a{color:#7c2fe0;font-weight:700}" +
    "@media (prefers-color-scheme:dark){.card{background:#1d1229;color:#f5f0fc}p,li,.save{color:#cdc1e2}.g{color:#f5f0fc}a.secondary{color:#f5f0fc;border-color:#3d2b55}.save{border-color:#33244a}.save a{color:#d8b4fe}button.link,a.link,.x{color:#a797c2}.g .tag{color:#ffb86b}}";

  function close() { if (host) host.remove(); host = null; }
  function open(html, opts, wire) {
    close();
    host = document.createElement("div");
    host.setAttribute("data-bgw", "account");
    var root = host.attachShadow ? host.attachShadow({ mode: "open" }) : host;
    root.innerHTML = "<style>" + CSS + "</style><div class='back" + (opts.sheet ? " sheet" : "") + "'><div class='card' role='dialog' aria-modal='" + !opts.sheet + "' aria-label='" + esc(opts.label) + "'>" +
      "<button class='x' type='button' aria-label='Close'>&times;</button>" + html + "</div></div>";
    document.body.appendChild(host);
    var dismiss = function () { if (opts.onClose) opts.onClose(); close(); };
    root.querySelector(".x").onclick = dismiss;
    if (!opts.sheet) root.querySelector(".back").onclick = function (e) { if (e.target === e.currentTarget) dismiss(); };
    var onKey = function (e) { if (e.key === "Escape" && host) { document.removeEventListener("keydown", onKey); dismiss(); } };
    document.addEventListener("keydown", onKey);
    if (wire) wire(root, dismiss);
    var first = root.querySelector("a.primary,button.primary");
    if (first && !opts.sheet) setTimeout(function () { first.focus(); }, 50);
  }

  // ---------- 1. welcome, once for all BGameWorld sites ----------
  function welcomed() { return cookie("bgw-welcomed") === "1" || store("bgw-welcomed") === "1"; }
  function markWelcomed() { setCookie("bgw-welcomed", "1", 60 * 60 * 24 * 365); store("bgw-welcomed", "1"); }
  function welcome() {
    open(
      "<img class='logo' src='" + SITE + "/logo.webp' alt='BGameWorld'>" +
      "<h2>Welcome to BGameWorld</h2>" +
      "<p>" + (current ? esc(current.name) + " is one of our free daily games. " : "Free daily puzzles, new every day. ") + "Make one free account for all of them:</p>" +
      "<ul><li>Play the members-only Daily Seven and build a streak</li><li>Your name on every game's leaderboard</li><li>Your progress saved on every device</li></ul>" +
      "<a class='primary' href='" + joinUrl() + "'>Create free account</a>" +
      "<a class='secondary' href='" + joinUrl("login") + "'>I already have an account</a>" +
      "<button class='link' type='button' data-guest>Play as a guest</button>",
      { label: "Welcome to BGameWorld", onClose: markWelcomed },
      function (r, dismiss) { r.querySelector("[data-guest]").onclick = dismiss; r.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", markWelcomed); }); }
    );
  }

  // ---------- 2. play next ----------
  function pick(st) {
    var seven = (st && st.seven) || [], today = (st && st.today) || [];
    var cand = GAMES.filter(function (g) { return !current || g.art !== current.art; });
    function score(g) {
      var s = Math.random();
      if (today.indexOf(g.art) < 0) s += 2;          // not played today
      if (seven.indexOf(g.art) >= 0) s += 1.5;       // in today's Daily Seven
      return s;
    }
    return cand.map(function (g) { return [score(g), g]; }).sort(function (a, b) { return b[0] - a[0]; }).slice(0, 3).map(function (x) { return x[1]; });
  }
  // Record every finished game, guests included (most games only save results
  // for players with a name, so guest play would otherwise be invisible).
  function logFinish(e) {
    var game = e && e.detail && e.detail.game;
    if (!game) return;
    var t = token(), h = { "Content-Type": "application/json", apikey: SB_KEY };
    if (t) h.Authorization = "Bearer " + t;
    fetch(SB_URL + "/rest/v1/rpc/log_finish", {
      method: "POST", keepalive: true, headers: h, body: JSON.stringify({ p_game: game, p_site: location.hostname }),
    }).catch(function () {});
  }
  window.addEventListener("bgw:finished", logFinish);

  var lastFinish = 0;
  function playNext() {
    if (Date.now() - lastFinish < 10000) return; // one card per finish
    lastFinish = Date.now();
    var guest = !registered();
    status().then(function (st) {
      setTimeout(function () {
        if (document.querySelector('[role="dialog"][aria-modal="true"]') && !host) return; // the game's own dialog is up
        var seven = (st && st.seven) || [], today = (st && st.today) || [];
        var memberLeft = !guest ? seven.filter(function (a) { return today.indexOf(a) < 0; }).length : 0;
        var games = pick(st).map(function (g) {
          var tag = seven.indexOf(g.art) >= 0 && today.indexOf(g.art) < 0 ? "<span class='tag'>Daily Seven</span>" : "";
          return "<a class='g' href='" + g.url + "/'><img src='" + SITE + "/art/" + g.guide + "-poster.webp' alt='' loading='lazy'>" + esc(g.name) + tag + "</a>";
        }).join("");
        open(
          "<h2>Nice one! Play next</h2>" +
          "<p>" + (!guest && seven.length ? (memberLeft ? memberLeft + " of today's Daily Seven still to go. Finish them all to grow your streak." : "You've finished today's Daily Seven. Your streak is safe!") : "Three more free puzzles for today:") + "</p>" +
          "<div class='games'>" + games + "</div>" +
          (guest ? "<p class='save'>Playing as a guest. <a href='" + joinUrl() + "'>Create a free BGameWorld account</a> to keep your progress and join the Daily Seven.</p>" : "") +
          "<a class='link' href='" + SITE + "/#challenge'>See all games and the Daily Seven</a>",
          { label: "Play next", sheet: true }
        );
      }, 2200); // let them see their result first
    });
  }
  window.addEventListener("bgw:finished", playNext);

  // ---------- 3. unconfirmed sign-up reminder ----------
  function reminder(email) {
    store("bgw-remind", String(Date.now()));
    open(
      "<h2>Finish signing up</h2>" +
      "<p>We sent a link to <b>" + esc(email) + "</b>. Tap it to finish your BGameWorld account. Check your spam folder too.</p>" +
      "<a class='primary' href='" + SITE + "/join/?next=" + encodeURIComponent(location.href.split("#")[0]) + "'>Send it again or change email</a>" +
      "<button class='link' type='button' data-ok>Later</button>",
      { label: "Finish signing up", sheet: true },
      function (r, dismiss) { r.querySelector("[data-ok]").onclick = dismiss; }
    );
  }

  // ---------- more games: a showcase every game places with <div data-bgw-more-games> ----------
  // The game's own plain links stay inside the element as a fallback; this
  // draws over them in a shadow root, so the game's styles can't clash.
  var SEVEN_POOL = ["wordezy", "wordsearch", "scramble", "ladder", "warmezy", "letterezy", "sortezy", "mergezy"];
  function fnv(str) { var h = 2166136261; for (var i = 0; i < str.length; i++) { h = (h ^ str.charCodeAt(i)) >>> 0; h = Math.imul(h, 16777619) >>> 0; } return h; }
  function sevenToday() {
    var d = new Date().toISOString().slice(0, 10);
    return SEVEN_POOL.map(function (a) { return [fnv(d + ":" + a), a]; }).sort(function (x, y) { return x[0] - y[0] || (x[1] < y[1] ? -1 : 1); }).slice(0, 7).map(function (x) { return x[1]; });
  }
  var HOOK = {
    wordezy: "Guess today's 5-letter word in 6 tries", wordsearch: "Find every hidden word on today's board",
    scramble: "Unscramble five words against the clock", ladder: "Turn one word into another, a letter at a time",
    warmezy: "Find the secret word by how close each guess is", letterezy: "Spell big words from a bag of letters",
    lingoezy: "Spot the right translation, dodge the traps", sortezy: "Pour the colours until every tube matches",
    linkezy: "Join the dots without crossing a line", mergezy: "Merge three of a kind to climb higher",
    timeguess: "Guess when and where a real photo was taken",
  };
  var MORE_CSS = ":host{all:initial;display:block;width:100%}" +
    "*{box-sizing:border-box}" +
    ".panel{font:15px/1.4 system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;color:#1d1530;text-align:left;border-radius:22px;padding:20px 16px 16px;margin:8px 0 4px;" +
    "background:linear-gradient(160deg,#fff7e6 0%,#fde9f6 45%,#ece6ff 100%);box-shadow:0 10px 30px -14px rgba(90,40,160,.45),inset 0 0 0 1px rgba(120,60,200,.15)}" +
    ".kick{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#a1401b}" +
    ".kick i{font-style:normal;display:inline-block;animation:tw 1.6s ease-in-out infinite}@keyframes tw{50%{transform:scale(1.35) rotate(15deg)}}" +
    "h3{margin:6px 0 2px;font-size:22px;line-height:1.15;font-weight:900;letter-spacing:-.01em}" +
    ".sub{margin:0 0 14px;color:#5b4f6e;font-size:14px}" +
    ".seven{display:flex;align-items:center;gap:10px;text-decoration:none;color:#fff;border-radius:14px;padding:11px 14px;margin:0 0 14px;font-weight:700;font-size:14px;" +
    "background:linear-gradient(90deg,#7c3aed,#db2777,#f59e0b);background-size:200% 100%;animation:sh 6s linear infinite;box-shadow:0 6px 18px -8px rgba(219,39,119,.8)}" +
    "@keyframes sh{to{background-position:200% 0}}.seven span{flex:1}.seven b{font-size:18px}" +
    ".grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}@media (min-width:460px){.grid{grid-template-columns:repeat(3,1fr)}}" +
    "a.card{display:flex;flex-direction:column;text-decoration:none;color:inherit;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 14px -8px rgba(40,20,80,.45),0 0 0 1px rgba(40,20,80,.06);transition:transform .18s,box-shadow .18s}" +
    "a.card:hover,a.card:focus-visible{transform:translateY(-3px);box-shadow:0 12px 26px -10px rgba(90,40,160,.55),0 0 0 2px #7c3aed;outline:none}" +
    ".pic{position:relative;aspect-ratio:4/3;background:#24123a;overflow:hidden}.pic img{width:100%;height:100%;object-fit:cover;object-position:center 35%;display:block;transition:transform .3s}" +
    "a.card:hover .pic img{transform:scale(1.06)}" +
    ".badge{position:absolute;left:8px;top:8px;font-size:10.5px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;padding:3px 8px;border-radius:999px;background:#fbbf24;color:#3b2300}" +
    ".badge.done{background:rgba(255,255,255,.9);color:#1e7d4a}" +
    ".body{padding:9px 10px 10px;display:flex;flex-direction:column;gap:3px;flex:1}" +
    ".name{font-weight:800;font-size:14.5px;line-height:1.2}.hook{font-size:12.5px;color:#6a5f7a;line-height:1.3;flex:1}" +
    ".go{margin-top:6px;align-self:flex-start;font-size:12.5px;font-weight:800;color:#fff;background:#1d1530;border-radius:999px;padding:5px 12px}" +
    "a.card:hover .go{background:#7c3aed}" +
    "a.card.played{opacity:.72}" +
    ".all{display:block;text-align:center;margin-top:14px;font-weight:800;color:#5b21b6;text-decoration:none;font-size:14px}.all:hover{text-decoration:underline}" +
    "@media (prefers-color-scheme:dark){.panel{color:#f5f0fc;background:linear-gradient(160deg,#2a1645 0%,#331a3f 50%,#1f1d4a 100%);box-shadow:0 10px 30px -14px rgba(0,0,0,.8),inset 0 0 0 1px rgba(216,180,254,.18)}" +
    ".kick{color:#fbbf24}.sub{color:#cdc1e2}a.card{background:#1d1229;box-shadow:0 0 0 1px rgba(216,180,254,.14)}.hook{color:#b9acd0}.go{background:#a855f7}.all{color:#d8b4fe}}" +
    "@media (prefers-reduced-motion:reduce){.kick i,.seven{animation:none}a.card,.pic img{transition:none}}";

  function renderMore(el) {
    el.setAttribute("data-bgw-done", "1");
    var here = el.getAttribute("data-game") || (current && current.art);
    var root = el.attachShadow ? el.attachShadow({ mode: "open" }) : null;
    if (!root) return; // very old browser: the game's own links stay
    function draw(st) {
      var seven = (st && st.seven) || sevenToday(), today = (st && st.today) || [], member = registered();
      var list = GAMES.filter(function (g) { return g.art !== here; }).map(function (g) {
        var played = today.indexOf(g.art) >= 0, inSeven = seven.indexOf(g.art) >= 0;
        return { g: g, played: played, inSeven: inSeven, rank: (played ? 0 : 4) + (inSeven ? 2 : 0) + Math.random() };
      }).sort(function (a, b) { return b.rank - a.rank; }).slice(0, 6);
      var left = seven.filter(function (a) { return today.indexOf(a) < 0; }).length;
      var strip = member
        ? (left ? "<a class='seven' href='" + SITE + "/#challenge'><b>&#128293;</b><span>Daily Seven: " + (7 - left) + " of 7 done. Finish all seven to grow your streak.</span>&rsaquo;</a>"
                : "<a class='seven' href='" + SITE + "/#challenge'><b>&#127942;</b><span>Daily Seven complete! See today's leaderboard.</span>&rsaquo;</a>")
        : "<a class='seven' href='" + joinUrl() + "'><b>&#10022;</b><span>Play the Daily Seven: join free, build a streak, top the leaderboard.</span>&rsaquo;</a>";
      root.innerHTML = "<style>" + MORE_CSS + "</style><section class='panel' aria-label='More free games'>" +
        "<span class='kick'><i>&#10022;</i> More free puzzles today</span>" +
        "<h3>Play your next game</h3><p class='sub'>New puzzles every day. Free, no download.</p>" + strip +
        "<div class='grid'>" + list.map(function (x) {
          var badge = x.played ? "<span class='badge done'>&#10003; Played</span>" : x.inSeven ? "<span class='badge'>Daily Seven</span>" : "";
          return "<a class='card" + (x.played ? " played" : "") + "' href='" + x.g.url + "/'>" +
            "<span class='pic'><img src='" + SITE + "/art/" + x.g.guide + "-poster.webp' alt='' loading='lazy'>" + badge + "</span>" +
            "<span class='body'><span class='name'>" + esc(x.g.name) + "</span><span class='hook'>" + esc(HOOK[x.g.art] || x.g.line) + "</span>" +
            "<span class='go'>" + (x.played ? "Play again" : "Play now") + " &#9656;</span></span></a>";
        }).join("") + "</div>" +
        "<a class='all' href='" + SITE + "/'>See all " + GAMES.length + " games on BGameWorld &rarr;</a></section>";
    }
    draw(null);                 // straight away, then again with what they've played today
    status().then(function (st) { if (st) draw(st); });
    window.addEventListener("bgw:finished", function () { setTimeout(function () { status().then(function (st) { if (st) draw(st); }); }, 1500); });
  }
  function findMore() {
    var els = document.querySelectorAll("[data-bgw-more-games]:not([data-bgw-done])");
    for (var i = 0; i < els.length; i++) renderMore(els[i]);
  }
  findMore();
  // Games draw their pages after loading, so watch for the spot to appear (checked at most twice a second).
  var moreTimer = null;
  if (window.MutationObserver) new MutationObserver(function () {
    if (!moreTimer) moreTimer = setTimeout(function () { moreTimer = null; findMore(); }, 500);
  }).observe(document.documentElement, { childList: true, subtree: true });

  // ---------- start ----------
  setTimeout(function () {
    if (registered()) { markWelcomed(); return; }
    if (!welcomed()) return welcome();
    if (Date.now() - Number(store("bgw-remind") || 0) < DAY) return;
    status().then(function (st) { if (st && st.guest && st.pending_email && !host) reminder(st.pending_email); });
  }, location.hostname === "bgameworld.com" ? 1200 : 900);
})();
