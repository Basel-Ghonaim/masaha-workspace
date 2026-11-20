/* Direction C — the shared core: preferences, Gaza's clock, the state rules, the composed sentence, the shell
   (header, footer, review panel), the entry, dialogs and toasts. Classic script; works from file://. */
(function () {
  var D = window.MASAHA_DATA, C = window.COPY, ICONS = window.ICONS;
  var M = window.M = {};
  var Q = new URLSearchParams(location.search);
  function store(k, v) {
    try { if (v === undefined) return localStorage.getItem(k); if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) { return null; }
    return null;
  }
  M.store = store; M.q = function (k) { return Q.get(k); };

  /* ---------- preferences ---------- */
  var ql = Q.get('lang'), qt = Q.get('theme');
  M.lang = (ql === 'ar' || ql === 'en') ? ql : (store('masaha-c-lang') === 'en' ? 'en' : (store('masaha-c-lang') === 'ar' ? 'ar' : 'ar'));
  var dev = false; try { dev = matchMedia('(prefers-color-scheme: dark)').matches; } catch (e) {}
  var st = store('masaha-c-theme');
  M.themePref = (qt === 'light' || qt === 'dark') ? qt : (st === 'light' || st === 'dark' || st === 'system' ? st : 'system');
  M.theme = M.themePref === 'system' ? (dev ? 'dark' : 'light') : M.themePref;
  var qd = Q.get('demo');
  M.demo = qd ? qd === '1' : store('masaha-c-demo') === '1';
  M.signedIn = false;
  M.t = function () { return C[M.lang]; };

  function syncUrl() {
    var u = new URL(location.href);
    u.searchParams.set('lang', M.lang); u.searchParams.set('theme', M.theme);
    try { history.replaceState(null, '', u.toString()); } catch (e) {}
  }
  function applyPrefs() {
    var h = document.documentElement;
    h.lang = M.lang; h.dir = M.lang === 'ar' ? 'rtl' : 'ltr'; h.setAttribute('data-theme', M.theme);
  }
  M.setLang = function (l) { M.lang = l; store('masaha-c-lang', l); syncUrl(); applyPrefs(); M.renderAll('lang-btn'); };
  M.setTheme = function (pref) {
    M.themePref = pref; M.theme = pref === 'system' ? (dev ? 'dark' : 'light') : pref;
    store('masaha-c-theme', pref); syncUrl(); applyPrefs(); M.renderAll('theme-btn');
  };
  M.setDemo = function (on) { M.demo = on; store('masaha-c-demo', on ? '1' : '0'); M.renderAll('rv-demo'); };
  applyPrefs();

  /* ---------- helpers ---------- */
  M.esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  M.icon = function (n, cls) { return '<svg class="icon ' + (cls || '') + '" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' + (ICONS[n] || '') + '</svg>'; };
  M.ltr = function (s) { return '<bdi dir="ltr">' + M.esc(s) + '</bdi>'; };
  var pad = function (n) { return (n < 10 ? '0' : '') + n; };
  M.time = function (min) { if (min >= 1440) min = 0; return pad(Math.floor(min / 60)) + ':' + pad(min % 60); };
  M.money = function (agorot) {
    var v = agorot / 100, s = v % 1 ? v.toFixed(2) : String(v);
    s = s.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return M.lang === 'ar' ? s + ' ₪' : '₪' + s;
  };
  M.photo = function (f) { return '../_shared/photos/' + f; };

  /* ---------- Gaza's clock ---------- */
  M.now = function () {
    var p = {}; new Intl.DateTimeFormat('en-US', { timeZone: 'Asia/Gaza', weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' })
      .formatToParts(new Date()).forEach(function (x) { p[x.type] = x.value; });
    var day = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(p.weekday);
    var h = +p.hour % 24, m = +p.minute;
    return { day: day, min: h * 60 + m, hhmm: pad(h) + ':' + pad(m) };
  };

  /* ---------- the data, with the review panel's demo states ---------- */
  var DEMO = { 'branch-hub': 'AVAILABLE', 'focus-hub': 'FULL', 'garden-hub': 'AVAILABLE', 'number-one-hub': 'CLOSED', 'elevate-hub': 'AVAILABLE' };
  var AREAS = {};
  D.governorates.forEach(function (g) { g.areas.forEach(function (a) { AREAS[a.id] = { area: a, gov: g }; }); });
  M.areas = AREAS; M.govs = D.governorates; M.contact = D.contact; M.ranges = D.ranges;
  M.spaces = function () {
    return D.spaces.map(function (s) {
      var c = Object.assign({}, s);
      if (M.demo && DEMO[s.slug]) { c.verified = true; c.liveStatus = DEMO[s.slug]; }
      if (M.demo && s.slug === 'branch-hub') c.announce = true;
      return c;
    });
  };
  M.bySlug = function (slug) { return M.spaces().filter(function (s) { return s.slug === slug; })[0]; };
  M.name = function (s) { return M.lang === 'ar' ? (s.nameAr || s.nameEn) : (s.nameEn || s.nameAr); };
  M.otherName = function (s) { return M.lang === 'ar' ? s.nameEn : s.nameAr; };
  M.areaName = function (s) { var a = AREAS[s.areaId].area; return M.lang === 'ar' ? a.nameAr : a.nameEn; };
  M.govOf = function (s) { return AREAS[s.areaId].gov; };
  M.gname = function (g) { return M.lang === 'ar' ? g.nameAr : g.nameEn; };
  M.aname = function (a) { return M.lang === 'ar' ? a.nameAr : a.nameEn; };

  /* ---------- the state rules (ADR 0008) ---------- */
  M.openByHours = function (s, n) {
    n = n || M.now(); if (!s.days) return null; var d = s.days[n.day];
    return !!d && n.min >= d.opensMinute && n.min < d.closesMinute;
  };
  M.state = function (s) {
    var t = M.t().st, n = M.now(), open = M.openByHours(s, n);
    if (s.verified && s.liveStatus) {
      if (s.liveStatus === 'CLOSED' || open === false) return { kind: 'closed', live: true, word: t.closedNow, mark: 'closed' };
      if (s.liveStatus === 'FULL') return { kind: 'full', live: true, word: t.full, mark: 'full' };
      return { kind: 'available', live: true, word: t.available, mark: 'live' };
    }
    if (s.verified || !s.days) return { kind: 'none', live: false, word: t.none, mark: 'none', unset: !!s.verified };
    return open ? { kind: 'open', live: false, word: t.open, mark: 'byhours' } : { kind: 'closed', live: false, word: t.closed, mark: 'closed' };
  };
  /* the directory's «مفتوحة الآن»: by the hours, and not closed by a live state */
  M.isOpenNow = function (s) { return !!M.openByHours(s) && !(s.verified && s.liveStatus === 'CLOSED'); };
  M.today = function (s) {
    if (!s.days) return null; var n = M.now(), d = s.days[n.day];
    if (!d) return { closed: true };
    if (d.opensMinute === 0 && d.closesMinute >= 1440) return { allDay: true, opens: 0, closes: 1440 };
    return { opens: d.opensMinute, closes: d.closesMinute, range: M.time(d.opensMinute) + '–' + M.time(d.closesMinute) };
  };
  M.nextOpen = function (s) {
    if (!s.days) return null; var n = M.now();
    for (var k = 0; k < 8; k++) {
      var day = (n.day + k) % 7, d = s.days[day];
      if (d && (k > 0 || n.min < d.opensMinute)) return { k: k, day: day, time: M.time(d.opensMinute) };
    }
    return null;
  };
  var ORDER = ['HOUR', 'DAY', 'WEEK', 'MONTH'];
  M.periodOrder = ORDER;
  M.lowest = function (s, period) {
    var g = s.prices.filter(function (p) { return p.audience === 'GENERAL' && (!period || p.period === period); });
    if (!g.length) return null;
    g.sort(function (a, b) { return ORDER.indexOf(a.period) - ORDER.indexOf(b.period) || a.amount - b.amount; });
    if (period) g.sort(function (a, b) { return a.amount - b.amount; });
    return g[0];
  };

  /* ---------- the composed sentence (DESIGN › Components): only the data, never an adjective ---------- */
  M.sentence = function (s, opts) {
    var t = M.t().sen, stt = M.state(s), td = M.today(s), lead = null, L = M.ltr;
    if (stt.kind === 'available') lead = t.available(L(M.time(td.closes)));
    else if (stt.kind === 'full') lead = t.full(L(M.time(td.closes)));
    else if (stt.kind === 'open') lead = td.allDay ? t.openAllDay : t.open(L(M.time(td.closes)));
    else if (stt.kind === 'closed') {
      if (stt.live && M.openByHours(s)) lead = t.liveClosed;
      else { var no = M.nextOpen(s); lead = no ? t.closedOpens(no.k === 0 ? t.today : no.k === 1 ? t.tomorrow : M.t().days[no.day], L(no.time)) : t.closed; }
    } else if (s.days) lead = td.closed ? t.closedToday : td.allDay ? M.t().sp.allDay : t.todayRange(L(td.range));
    var area = M.esc(M.areaName(s)), parts = lead ? [lead, t.inArea(area)] : [t.inAreaCap(area)];
    var lp = (opts && opts.price) || M.lowest(s);
    if (lp) parts.push(t.price(L(M.money(lp.amount)), t.per[lp.period]));
    var html = parts.join(t.sep) + t.end;
    if (!s.days) html += ' ' + t.noHours;
    return html;
  };
  /* the line under it: where the state comes from */
  M.stateMeta = function (s) {
    var t = M.t().st, stt = M.state(s);
    if (stt.live) return t.verified + ' · ' + t.live;
    if (stt.kind === 'none') return t.none + (s.verified ? ' · ' + t.verified : '');
    return t.byHoursShort;
  };
  M.mark = function (stt, big) { return '<span class="mark ' + stt.mark + (big ? ' big' : '') + '" aria-hidden="true"></span>'; };

  M.km = function (a, b) {
    var R = 6371, toR = Math.PI / 180, dLat = (b.lat - a.lat) * toR, dLng = (b.lng - a.lng) * toR;
    var x = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(a.lat * toR) * Math.cos(b.lat * toR) * Math.sin(dLng / 2) * Math.sin(dLng / 2);
    return 2 * R * Math.asin(Math.sqrt(x));
  };
  M.HERE = { lat: 31.5166, lng: 34.4441 }; /* the mock-up's simulated point in الرمال */

  /* ---------- favourites (sample user) ---------- */
  M.user = { name: 'سلمى الأغا', nameEn: 'Salma Al-Agha', email: 'demo-user@example.com' };
  var FAV0 = ['branch-hub', 'focus-hub', 'coma-io', 'masahat', 'pal-hub', 'noor-hub'];
  M.favs = function () { var v = store('masaha-c-favs'); try { return v ? JSON.parse(v) : FAV0.slice(); } catch (e) { return FAV0.slice(); } };
  M.setFavs = function (a) { store('masaha-c-favs', JSON.stringify(a)); };

  /* ---------- the entry: type on the ground, a plate at the start ---------- */
  M.plate = function (s, ph, cls) {
    return '<figure class="plate ' + (ph.real ? 'real' : 'poster') + ' ' + (cls || '') + '"><div class="frame"><img src="' + M.photo(ph.card) + '" alt="" loading="lazy" width="640" height="360"></div>' +
      '<figcaption>' + M.esc(M.t().sp.photoFrom) + '</figcaption></figure>';
  };
  M.entry = function (s, o) {
    o = o || {}; var t = M.t(), stt = M.state(s), nm = M.esc(M.name(s)), ph = o.noPhoto ? null : s.photos[0];
    var h = o.h || 'h3';
    var act = '';
    if (o.remove) act = '<div class="entry-actions"><button class="btn btn-quiet" type="button" data-remove="' + s.slug + '" aria-label="' + M.esc(t.fav.removeName(M.name(s))) + '">' + t.fav.remove + '</button></div>';
    else if (o.heart !== false) {
      var saved = M.signedIn && M.favs().indexOf(s.slug) >= 0;
      act = '<button class="btn btn-icon heart" type="button" data-heart="' + s.slug + '" aria-pressed="' + saved + '" aria-label="' + M.esc(saved ? t.sp.remove(M.name(s)) : t.sp.save(M.name(s))) + '">' + M.icon('heart') + '</button>';
    }
    var meta = '<span>' + M.esc(M.stateMeta(s)) + '</span>';
    if (o.km != null) meta += '<span>' + M.esc(t.dir.distance(o.km.toFixed(1))) + '</span>';
    return '<article class="entry' + (ph ? ' has-plate' : '') + '">' + (ph ? M.plate(s, ph) : '') +
      '<div class="body"><div class="name-row"><' + h + ' class="t-entry"><a href="space.html?slug=' + s.slug + '">' + nm + '</a></' + h + '>' +
      '<p class="t-meta meta">' + meta + '</p>' + act + '</div>' +
      '<p class="t-lede lede">' + M.mark(stt) + M.sentence(s, { price: o.price }) + '</p></div></article>';
  };

  M.accountNav = function (cur) {
    var t = M.t().account, L = [['favorites', 'favorites.html', t.favorites], ['reports', '404.html', t.reports], ['settings', 'account.html', t.settings]];
    return '<nav class="acct-nav" aria-label="' + t.nav + '"><p class="t-meta">' + t.nav + '</p><ul>' + L.map(function (l) { return '<li><a href="' + l[1] + '"' + (cur === l[0] ? ' aria-current="page"' : '') + '>' + l[2] + '</a></li>'; }).join('') + '</ul></nav>';
  };
  M.dateline = function () {
    var t = M.t(), n = M.now(), all = M.spaces(), open = all.filter(M.isOpenNow).length;
    return '<div class="dateline"><p class="clock">' + t.days[n.day] + ' · <strong>' + M.ltr(n.hhmm) + '</strong> ' + t.home.gazaTime + '</p>' +
      '<p class="openrow"><span class="mark ' + (open ? 'live' : 'closed') + '" aria-hidden="true"></span><a class="openline" href="spaces.html?open=1">' + t.home.openOf(open, all.length) + '</a></p></div>';
  };

  /* ---------- dialogs & toasts ---------- */
  M.dialog = function (o) {
    var prev = document.activeElement, d = document.createElement('dialog');
    d.className = 'dlg'; d.setAttribute('aria-labelledby', 'dlg-t');
    d.innerHTML = '<h2 id="dlg-t">' + M.esc(o.title) + '</h2><p class="t-fact">' + M.esc(o.text) + '</p><div class="acts">' +
      o.actions.map(function (a, i) { return a.href ? '<a class="btn ' + (a.kind || 'btn-secondary') + '" href="' + a.href + '"' + (a.ext ? ' target="_blank" rel="noopener"' : '') + '>' + (a.icon ? M.icon(a.icon) : '') + M.esc(a.label) + '</a>' : '<button class="btn ' + (a.kind || 'btn-secondary') + '" type="button" data-i="' + i + '">' + M.esc(a.label) + '</button>'; }).join('') + '</div>';
    document.body.appendChild(d);
    d.addEventListener('click', function (e) { var b = e.target.closest('button[data-i]'); if (b) d.close(); if (e.target === d) d.close(); });
    d.addEventListener('close', function () { d.remove(); if (prev && prev.focus) prev.focus(); });
    d.showModal();
  };
  M.toast = function (text, undo) {
    var old = document.querySelector('.toast'); if (old) old.remove();
    var el = document.createElement('div'); el.className = 'toast'; el.setAttribute('role', 'status');
    el.innerHTML = '<span>' + M.esc(text) + '</span>' + (undo ? '<button type="button">' + M.esc(M.t().fav.undo) + '</button>' : '');
    document.body.appendChild(el);
    if (undo) el.querySelector('button').addEventListener('click', function () { el.remove(); undo(); });
    setTimeout(function () { if (el.isConnected) el.remove(); }, 6000);
  };
  M.signInPrompt = function (kind) {
    var t = M.t().sp;
    M.dialog({ title: kind === 'report' ? t.signInReport : t.signInFav, text: kind === 'report' ? t.signInReportText : t.signInFavText,
      actions: [{ label: M.t().signIn, href: 'login.html', kind: 'btn-primary' }, { label: t.register, href: 'login.html' }, { label: M.t().dir.close }] });
  };
  M.contactDialog = function (title, text) {
    var t = M.t();
    M.dialog({ title: title, text: text, actions: [
      { label: t.whatsapp, href: 'https://wa.me/' + D.contact.whatsapp.replace('+', ''), kind: 'btn-primary', icon: 'message-circle', ext: true },
      { label: t.email, href: 'mailto:' + D.contact.email, icon: 'mail' }, { label: t.dir.close }] });
  };

  /* ---------- the shell ---------- */
  var LOGO = { light: '../_shared/logo/masaha-logo-berry.svg', dark: '../_shared/logo/masaha-logo-dark-berry.svg' };
  function header(page) {
    var t = M.t(), nav = [['home', 'home.html'], ['spaces', 'spaces.html'], ['about', 'about.html']];
    var links = nav.map(function (n) { return '<a href="' + n[1] + '"' + (page === n[0] ? ' aria-current="page"' : '') + '>' + t.links[n[0]] + '</a>'; }).join('');
    var themeBtn = '<button class="textbtn" type="button" id="theme-btn" data-theme-toggle>' + M.icon(M.theme === 'dark' ? 'sun' : 'moon') + '<span>' + t.theme[M.theme] + '</span></button>';
    var langBtn = '<button class="textbtn" type="button" id="lang-btn" data-lang-toggle lang="' + (M.lang === 'ar' ? 'en' : 'ar') + '" aria-label="' + t.langLabel + '">' + t.langName + '</button>';
    var who = M.lang === 'ar' ? M.user.name : M.user.nameEn;
    var acct = M.signedIn
      ? '<div class="user-menu"><button class="textbtn" type="button" id="user-btn" aria-expanded="false" aria-haspopup="true" aria-controls="user-pop" aria-label="' + M.esc(t.account.menu(who)) + '">' + M.icon('user') + '<span>' + M.esc(who) + '</span>' + M.icon('chevron-down') + '</button>' +
        '<div class="popover" id="user-pop" hidden><div class="who"><strong>' + M.esc(who) + '</strong>' + M.ltr(M.user.email) + '</div>' +
        '<a href="favorites.html"' + (page === 'favorites' ? ' aria-current="page"' : '') + '>' + t.account.favorites + '</a><a href="404.html">' + t.account.reports + '</a><a href="account.html"' + (page === 'account' ? ' aria-current="page"' : '') + '>' + t.account.settings + '</a><hr>' +
        '<button type="button" data-signout>' + M.icon('log-out', 'dir') + t.account.signOut + '</button></div></div>'
      : '<a class="btn btn-secondary" href="login.html"' + (page === 'login' ? ' aria-current="page"' : '') + '>' + t.signIn + '</a>';
    return '<a class="skip" href="#main">' + t.skip + '</a>' +
      '<header class="site-header"><div class="wrap">' +
      '<a class="logo" href="home.html" aria-label="' + (M.lang === 'ar' ? 'مساحة — ' : 'Masaha — ') + t.links.home + '"><img src="' + LOGO[M.theme] + '" alt="" width="110" height="40"></a>' +
      '<nav class="nav" aria-label="' + t.nav + '">' + links + '</nav>' +
      '<div class="head-actions"><span class="wide">' + langBtn + themeBtn + '</span>' + '<span class="wide-acct">' + acct + '</span>' +
      '<button class="textbtn menu-btn" type="button" id="menu-btn" aria-expanded="false" aria-controls="drawer">' + t.menu + '</button></div></div>' +
      '<div class="drawer" id="drawer" hidden><div class="wrap"><nav aria-label="' + t.nav + '">' + nav.map(function (n) { return '<a href="' + n[1] + '"' + (page === n[0] ? ' aria-current="page"' : '') + '>' + t.links[n[0]] + M.icon('chevron-right', 'dir') + '</a>'; }).join('') + '</nav>' +
      '<div class="row-2">' + langBtn.replace('id="lang-btn"', 'id="lang-btn-2"') + themeBtn.replace('id="theme-btn"', 'id="theme-btn-2"') + '</div></div></div></header>';
  }
  function footer() {
    var t = M.t(), wa = D.contact.whatsapp;
    return '<footer class="site-footer"><div class="wrap grid"><p class="tag">' + t.tagline + '</p>' +
      '<p class="contact">' + t.footerContact + '<br><a href="https://wa.me/' + wa.replace('+', '') + '" target="_blank" rel="noopener">' + M.ltr(wa) + '</a><br><a href="mailto:' + D.contact.email + '">' + M.ltr(D.contact.email) + '</a></p>' +
      '<nav aria-label="' + t.tagline.split(' — ')[0] + '"><ul><li><a href="spaces.html">' + t.browse + '</a></li><li><a href="about.html">' + t.links.about + '</a></li><li><a href="about.html#contact">' + t.contact + '</a></li></ul></nav>' +
      '</div></footer>';
  }
  function review() {
    var t = M.t(), P = [['home.html', 'Home'], ['spaces.html', 'Directory — list'], ['spaces.html?filters=open', 'Directory — refine open'], ['spaces.html?view=map', 'Directory — map'],
      ['space.html?slug=branch-hub', 'Space — Branch Hub'], ['space.html?slug=elevate-hub', 'Space — Elevate Hub'], ['space.html?slug=jreas-hub', 'Space — Jreas Hub (no hours)'], ['space.html?slug=number-one-hub', 'Space — Number One (students)'], ['space.html?slug=coma-io', 'Space — coma,io (photo)'],
      ['login.html', 'Sign in'], ['about.html', 'About'], ['account.html', 'Account settings'], ['favorites.html', 'Favourites'], ['404.html', '404']];
    return '<div class="review" lang="en" dir="ltr"><button type="button" id="rv-btn" aria-expanded="false" aria-controls="rv-body">' + t.review.button + '</button>' +
      '<div class="rv-body" id="rv-body" hidden><strong>Direction C — the guide</strong>' + P.map(function (p) { return '<a href="' + p[0] + '">' + p[1] + '</a>'; }).join('') +
      '<label><input type="checkbox" id="rv-demo"' + (M.demo ? ' checked' : '') + '> ' + t.review.demo + '</label><p class="rv-note">' + M.esc(t.review.demoNote) + '</p>' +
      '<p class="rv-note">Gaza time now: ' + M.now().hhmm + '</p></div></div>';
  }

  /* ---------- boot ---------- */
  M.renderAll = function (focusId) {
    var p = M.page; document.title = M.t().title(p.title());
    document.getElementById('shell-h').innerHTML = header(p.id);
    document.getElementById('shell-f').innerHTML = footer();
    document.getElementById('shell-r').innerHTML = review();
    p.render();
    if (focusId) { var el = document.getElementById(focusId); if (el && el.offsetParent) el.focus(); else { el = document.getElementById(focusId + '-2'); if (el && el.offsetParent) el.focus(); } }
  };
  function toggle(btn, el) { var open = btn.getAttribute('aria-expanded') !== 'true'; btn.setAttribute('aria-expanded', String(open)); el.hidden = !open; return open; }
  document.addEventListener('click', function (e) {
    var b;
    if ((b = e.target.closest('[data-lang-toggle]'))) { M.setLang(M.lang === 'ar' ? 'en' : 'ar'); return; }
    if ((b = e.target.closest('[data-theme-toggle]'))) { M.setTheme(M.theme === 'dark' ? 'light' : 'dark'); return; }
    if ((b = e.target.closest('#menu-btn'))) { var o = toggle(b, document.getElementById('drawer')); b.textContent = o ? M.t().closeMenu : M.t().menu; return; }
    if ((b = e.target.closest('#rv-btn'))) { toggle(b, document.getElementById('rv-body')); return; }
    if ((b = e.target.closest('#user-btn'))) { toggle(b, document.getElementById('user-pop')); return; }
    if ((b = e.target.closest('[data-signout]'))) { store('masaha-c-signed', null); location.href = 'home.html'; return; }
    if ((b = e.target.closest('[data-heart]'))) {
      if (!M.signedIn) { M.signInPrompt('fav'); return; }
      var f = M.favs(), slug = b.getAttribute('data-heart'), i = f.indexOf(slug), sp = M.bySlug(slug);
      if (i >= 0) f.splice(i, 1); else f.push(slug); M.setFavs(f);
      b.setAttribute('aria-pressed', String(i < 0)); b.setAttribute('aria-label', i < 0 ? M.t().sp.remove(M.name(sp)) : M.t().sp.save(M.name(sp)));
      M.toast(i < 0 ? M.t().sp.added : M.t().sp.removed); return;
    }
    var pop = document.getElementById('user-pop');
    if (pop && !pop.hidden && !e.target.closest('.user-menu')) { pop.hidden = true; document.getElementById('user-btn').setAttribute('aria-expanded', 'false'); }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var pop = document.getElementById('user-pop'), ub = document.getElementById('user-btn');
    if (pop && !pop.hidden) { pop.hidden = true; ub.setAttribute('aria-expanded', 'false'); ub.focus(); }
    var rv = document.getElementById('rv-body'); if (rv && !rv.hidden) { rv.hidden = true; var rb = document.getElementById('rv-btn'); rb.setAttribute('aria-expanded', 'false'); rb.focus(); }
  });
  document.addEventListener('change', function (e) { if (e.target.id === 'rv-demo') M.setDemo(e.target.checked); });

  M.boot = function (page) {
    M.page = page;
    M.signedIn = !!page.signedIn || store('masaha-c-signed') === '1';
    if (Q.get('lang') || Q.get('theme')) syncUrl();
    var b = document.body;
    b.insertAdjacentHTML('afterbegin', '<div id="shell-h"></div>');
    var main = document.getElementById('main');
    main.insertAdjacentHTML('afterend', '<div id="shell-f"></div><div id="shell-r"></div>');
    M.renderAll();
  };
})();
