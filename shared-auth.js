/* One sign-in for every BGameWorld game. Same logic as src/lib/sharedAuth.ts in
   the game repos: the login lives in a cookie for the whole .bgameworld.com
   domain, so signing in once works on bgameworld.com and in every game. */
(function () {
  var KEY = "bgw-auth", LEGACY = "sb-hkcvtoozpeybwehqtiif-auth-token", CHUNK = 3000, MAX_AGE = 60 * 60 * 24 * 400;
  function domain() { var h = location.hostname; return h === "bgameworld.com" || /\.bgameworld\.com$/.test(h) ? ".bgameworld.com" : null; }
  function read(name) { var p = name + "=", a = document.cookie.split("; "); for (var i = 0; i < a.length; i++) if (a[i].indexOf(p) === 0) return a[i].slice(p.length); return null; }
  function write(d, name, value, age) { document.cookie = name + "=" + value + "; Domain=" + d + "; Path=/; Max-Age=" + age + "; SameSite=Lax; Secure"; }
  function clear(d, key, from) { for (var i = from; read(key + "." + i) !== null; i++) write(d, key + "." + i, "", 0); }
  var storage = {
    getItem: function (key) {
      var d = domain();
      if (!d) { try { return localStorage.getItem(key); } catch (e) { return null; } }
      var parts = []; for (var i = 0; ; i++) { var v = read(key + "." + i); if (v === null) break; parts.push(v); }
      if (!parts.length) return null;
      try { return decodeURIComponent(parts.join("")); } catch (e) { return null; }
    },
    setItem: function (key, value) {
      var d = domain();
      if (!d) { try { localStorage.setItem(key, value); } catch (e) {} return; }
      var enc = encodeURIComponent(value), n = Math.ceil(enc.length / CHUNK);
      for (var i = 0; i < n; i++) write(d, key + "." + i, enc.slice(i * CHUNK, (i + 1) * CHUNK), MAX_AGE);
      clear(d, key, n);
    },
    removeItem: function (key) {
      var d = domain();
      if (!d) { try { localStorage.removeItem(key); } catch (e) {} return; }
      clear(d, key, 0);
    }
  };
  function registered(raw) { try { var s = raw ? JSON.parse(raw) : null; return !!(s && s.user && !s.user.is_anonymous && s.refresh_token); } catch (e) { return false; } }
  function adopt() {
    if (!domain()) return;
    var legacy = null; try { legacy = localStorage.getItem(LEGACY); } catch (e) { return; }
    if (!legacy) return;
    var shared = storage.getItem(KEY);
    if (!shared || (registered(legacy) && !registered(shared))) storage.setItem(KEY, legacy);
    try { localStorage.removeItem(LEGACY); } catch (e) {} // move, don't copy, so signing out sticks
  }
  window.bgwSharedAuth = function () { adopt(); return { storage: storage, storageKey: KEY, persistSession: true, autoRefreshToken: true }; };
})();
