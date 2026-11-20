/* The directory: list (rows in one container) and map (an SVG of the Strip), the filter rail / sheet,
   the sort, near me and the search. The filters filter the 13 real spaces. */
(function () {
  'use strict';
  var Q = A.Q;
  var F = {
    q: Q.get('q') || '',
    areas: (Q.get('area') || '').split(',').filter(Boolean).map(Number),
    period: Q.get('period') || '',
    from: Q.get('from') || '', to: Q.get('to') || '',
    open: Q.get('open') === '1', evening: Q.get('evening') === '1', friday: Q.get('friday') === '1',
    verified: Q.get('verified') === '1', students: Q.get('students') === '1', womens: Q.get('womens') === '1',
    sort: Q.get('sort') || 'updated',
    near: Q.get('near') === '1',
    view: Q.get('view') === 'map' ? 'map' : 'list'
  };
  var sheetOpen = false, locating = false;
  var wantsOpen = Q.get('filters') === 'open';
  if (wantsOpen && !F.period) F.period = 'MONTH';
  var openGovs = {};
  F.areas.forEach(function (id) { var s = window.MD.governorates.filter(function (g) { return g.areas.some(function (a) { return a.id === id; }); })[0]; if (s) openGovs[s.id] = true; });
  var map = null; /* map view state */
  var selected = null;

  function norm(x) { return String(x || '').toLowerCase().replace(/[ً-ٰٟـ]/g, '').replace(/[أإآ]/g, 'ا').replace(/ة/g, 'ه').replace(/ى/g, 'ي').trim(); }
  function amount(v) { var n = parseFloat(String(v).replace(/,/g, '')); return isFinite(n) && n > 0 ? n : null; }
  function rangeError() {
    if (F.from && amount(F.from) === null) return 'from';
    if (F.to && amount(F.to) === null) return 'to';
    if (amount(F.from) !== null && amount(F.to) !== null && amount(F.to) < amount(F.from)) return 'order';
    return null;
  }
  function periodPrice(s) {
    var g = A.priceOf(s, F.period, 'GENERAL'); if (g != null) return g;
    return A.priceOf(s, F.period, 'STUDENT');
  }
  function appliedCount() {
    return F.areas.length + (F.period ? 1 : 0) + (F.open ? 1 : 0) + (F.evening ? 1 : 0) + (F.friday ? 1 : 0) + (F.verified ? 1 : 0) + (F.students ? 1 : 0) + (F.womens ? 1 : 0);
  }
  function filtered() {
    var g = A.gaza(), q = norm(F.q);
    var list = A.allSpaces().filter(function (s) {
      if (q) {
        var gv = A.gov(s.govId) || {};
        var hay = [s.nameAr, s.nameEn, s.area.nameAr, s.area.nameEn, gv.nameAr, gv.nameEn].map(norm).join(' ');
        if (hay.indexOf(q) < 0) return false;
      }
      if (F.areas.length && F.areas.indexOf(s.area.id) < 0) return false;
      if (F.period) {
        var p = periodPrice(s); if (p == null) return false;
        if (!rangeError()) {
          var lo = amount(F.from), hi = amount(F.to);
          if (lo !== null && p / 100 < lo) return false;
          if (hi !== null && p / 100 > hi) return false;
        }
      }
      if (F.open && !A.statusOf(s, g).openNow) return false;
      if (F.evening && !s.worksEvenings) return false;
      if (F.friday && !(s.days && s.days[5])) return false;
      if (F.verified && !s.isVerified) return false;
      if (F.students && !s.prices.some(function (p) { return p.audience === 'STUDENT'; })) return false;
      if (F.womens && !s.womensHall) return false;
      return true;
    });
    var lang = A.state.lang;
    var sort = F.near ? 'distance' : F.sort;
    if ((sort === 'asc' || sort === 'desc') && !F.period) sort = 'updated';
    list.sort(function (a, b) {
      if (sort === 'distance') return A.km(A.NEAR_POINT, a.location) - A.km(A.NEAR_POINT, b.location);
      if (sort === 'name') return A.nm(a).localeCompare(A.nm(b), lang);
      if (sort === 'asc' || sort === 'desc') {
        var pa = periodPrice(a), pb = periodPrice(b);
        return sort === 'asc' ? pa - pb : pb - pa;
      }
      return A.lastUpdated(b) - A.lastUpdated(a);
    });
    return list;
  }

  /* ───────── the rail / sheet ───────── */
  function check(name, label, on, count) {
    return '<label class="check"><input type="checkbox" data-f="' + name + '"' + (on ? ' checked' : '') + '><span class="box">' + A.icon('check') + '</span><span>' + label + '</span>' + (count != null ? '<span class="count">' + count + '</span>' : '') + '</label>';
  }
  function rail() {
    var w = A.t(), f = w.dir.f, all = A.allSpaces();
    var govs = window.MD.governorates.map(function (g) {
      var n = all.filter(function (s) { return s.govId === g.id; }).length;
      var chosen = g.areas.filter(function (a) { return F.areas.indexOf(a.id) >= 0; }).length;
      return '<details class="gov" data-gov="' + g.id + '"' + (openGovs[g.id] ? ' open' : '') + '><summary><span>' + A.esc(A.L(g, 'name')) + '</span><span class="sum">' + (chosen ? '<span class="sr">' + f.applied(chosen) + '</span>' + chosen + ' / ' : '') + n + '</span>' + A.icon('chevron-down', 's16') + '</summary><div class="opts">' +
        g.areas.map(function (a) { var c = all.filter(function (s) { return s.area.id === a.id; }).length; return '<label class="check' + (c ? '' : ' zero') + '"><input type="checkbox" data-area="' + a.id + '"' + (F.areas.indexOf(a.id) >= 0 ? ' checked' : '') + '><span class="box">' + A.icon('check') + '</span><span>' + A.esc(A.L(a, 'name')) + '</span><span class="count">' + c + '</span></label>'; }).join('') +
        '</div></details>';
    }).join('');
    var periods = ['', 'HOUR', 'DAY', 'WEEK', 'MONTH'];
    var seg = '<div class="seg fill" role="radiogroup" aria-label="' + f.subscription + '">' + periods.map(function (p) {
      return '<button type="button" role="radio" data-period="' + p + '" aria-checked="' + (F.period === p) + '" tabindex="' + (F.period === p ? 0 : -1) + '">' + (p ? f.periods[p] : f.all) + '</button>';
    }).join('') + '</div>';
    var err = rangeError();
    var range = F.period
      ? '<div class="range"><div class="field"><label for="pfrom">' + f.from + '</label><div class="unit"><span aria-hidden="true">' + f.currency + '</span><input class="input num" id="pfrom" inputmode="decimal" dir="ltr" value="' + A.esc(F.from) + '" placeholder="' + (window.MD.priceRanges[F.period].minAgorot / 100) + '"' + (err === 'from' ? ' aria-invalid="true" aria-describedby="perr"' : '') + '></div></div>' +
        '<div class="field"><label for="pto">' + f.to + '</label><div class="unit"><span aria-hidden="true">' + f.currency + '</span><input class="input num" id="pto" inputmode="decimal" dir="ltr" value="' + A.esc(F.to) + '" placeholder="' + (window.MD.priceRanges[F.period].maxAgorot / 100) + '"' + (err === 'to' || err === 'order' ? ' aria-invalid="true" aria-describedby="perr"' : '') + '></div></div></div>' +
        (err ? '<p class="err" id="perr" style="margin-block-start:8px">' + (err === 'order' ? f.belowMin : f.invalid) + '</p>' : '') +
        '<p class="help" style="margin-block-start:8px">' + f.rangeHelp(f.priceNames[F.period]) + '</p>'
      : '<p class="help" style="margin-block-start:8px">' + f.hint + '</p>';
    var n = filtered().length;
    return '<div class="sheet-backdrop" data-open="' + sheetOpen + '" data-sheet-close></div>' +
      '<aside class="rail" id="rail" data-open="' + sheetOpen + '" aria-labelledby="ftitle"' + (sheetOpen ? ' role="dialog" aria-modal="true"' : '') + '>' +
      '<div class="rail__head"><div><h2 class="t-row" id="ftitle">' + f.title + '</h2><p class="t-meta c2">' + f.description + '</p></div>' +
      '<div style="display:flex;gap:4px">' + (appliedCount() ? '<button type="button" class="btn btn-quiet" data-clear>' + f.clear + '</button>' : '') +
      '<button type="button" class="btn btn-icon sheet-close" data-sheet-close aria-label="' + f.close + '">' + A.icon('x') + '</button></div></div>' +
      '<div class="rail__scroll">' +
      '<fieldset class="fgroup"><legend>' + f.area + '</legend>' + govs + '</fieldset>' +
      '<fieldset class="fgroup"><legend>' + f.price + '</legend>' + seg + range + '</fieldset>' +
      '<fieldset class="fgroup"><legend>' + f.schedule + '</legend>' + check('open', f.openNow, F.open) + check('evening', f.evening, F.evening) + check('friday', f.friday, F.friday) + '</fieldset>' +
      '<fieldset class="fgroup"><legend>' + f.other + '</legend>' + check('verified', f.verified, F.verified) + check('students', f.students, F.students) + check('womens', f.womens, F.womens) + '</fieldset>' +
      '</div>' +
      '<div class="rail__foot"><button type="button" class="btn btn-primary" style="flex:1" data-sheet-close' + (n ? '' : ' aria-disabled="true"') + '>' + f.show(n) + '</button>' + (appliedCount() ? '<button type="button" class="btn btn-secondary" data-clear>' + f.clear + '</button>' : '') + '</div>' +
      '</aside>';
  }

  /* ───────── results ───────── */
  function sortBox() {
    var d = A.t().dir, opts = [];
    if (F.near) opts.push(['distance', d.sorts.distance]);
    else {
      opts.push(['updated', d.sorts.updated], ['name', d.sorts.name]);
      if (F.period) opts.push(['asc', d.asc[F.period]], ['desc', d.desc[F.period]]);
    }
    var cur = F.near ? 'distance' : F.sort;
    return '<div class="sortbox"><label for="sort">' + d.sort + '</label><div class="select"><select class="input" id="sort"' + (F.near ? ' disabled' : '') + '>' +
      opts.map(function (o) { return '<option value="' + o[0] + '"' + (o[0] === cur ? ' selected' : '') + '>' + o[1] + '</option>'; }).join('') +
      '</select>' + A.icon('chevron-down', 's16') + '</div></div>';
  }
  function nearLine() {
    var d = A.t().dir.near;
    if (locating) return '<div class="near-line" role="status">' + A.icon('locate-fixed', 's16') + '<span>' + d.locating + '</span><span>' + d.privacy + '</span></div>';
    if (!F.near) return '';
    return '<div class="near-line" role="status"><span>' + d.sorted + ' ' + d.approx + '</span><button type="button" class="btn btn-quiet" data-near-stop style="text-decoration:underline">' + d.stop + '</button></div>';
  }
  function results() {
    var d = A.t().dir, list = filtered(), g = A.gaza();
    var bar = '<div class="results__bar"><p class="count" aria-live="polite">' + (appliedCount() || F.q ? d.matching(list.length) : d.all(list.length)) + '</p>' + (F.view === 'list' ? sortBox() : '') + '</div>' + nearLine();
    if (F.view === 'map') return bar + '<div class="mapwrap" id="mapwrap"></div>';
    if (!list.length) {
      return bar + '<div class="rows empty"><h2 class="t-h2">' + d.noMatchTitle + '</h2><p>' + d.noMatchText + '</p><button type="button" class="btn btn-secondary" data-clear>' + d.clearFilters + '</button></div>';
    }
    return bar + '<h2 class="sr">' + d.results + '</h2><ul class="rows">' + A.rowsHead() + list.map(function (s) { return A.row(s, { g: g, period: F.period || null, near: F.near ? A.NEAR_POINT : null }); }).join('') + '</ul>' +
      '<p class="listfoot">' + d.range(A.ltr('1–' + list.length), list.length) + '</p>';
  }

  function toolbar() {
    var d = A.t().dir, n = appliedCount();
    return '<div class="toolbar"><div class="wrap toolbar__in">' +
      '<div class="search with-icon" role="search">' + A.icon('search') + '<label class="sr" for="dq">' + d.searchLabel + '</label><input class="input" id="dq" type="search" placeholder="' + d.placeholder + '" value="' + A.esc(F.q) + '" autocomplete="off"></div>' +
      '<div class="tail">' +
      '<button type="button" class="btn btn-secondary filters-btn" data-sheet-open aria-controls="rail" aria-expanded="' + sheetOpen + '">' + A.icon('sliders-horizontal') + d.f.title + (n ? ' <span class="badge-n" aria-hidden="true">' + n + '</span><span class="sr">' + d.f.applied(n) + '</span>' : '') + '</button>' +
      '<button type="button" class="btn btn-secondary near" data-near aria-pressed="' + F.near + '">' + A.icon('locate-fixed') + d.near.button + '</button>' +
      '<div class="seg view" role="group" aria-label="' + d.view.label + '">' +
      '<button type="button" data-view="list" aria-pressed="' + (F.view === 'list') + '" aria-label="' + d.view.list + '">' + A.icon('list') + '<span>' + d.view.list + '</span></button>' +
      '<button type="button" data-view="map" aria-pressed="' + (F.view === 'map') + '" aria-label="' + d.view.map + '">' + A.icon('map') + '<span>' + d.view.map + '</span></button></div>' +
      '</div></div></div>';
  }

  function syncURL() {
    var q = new URLSearchParams();
    if (F.q) q.set('q', F.q);
    if (F.areas.length) q.set('area', F.areas.join(','));
    if (F.period) q.set('period', F.period);
    if (F.from) q.set('from', F.from);
    if (F.to) q.set('to', F.to);
    ['open', 'evening', 'friday', 'verified', 'students', 'womens', 'near'].forEach(function (k) { if (F[k]) q.set(k, '1'); });
    if (F.sort !== 'updated') q.set('sort', F.sort);
    if (F.view === 'map') q.set('view', 'map');
    if (wantsOpen) q.set('filters', 'open');
    q.set('lang', A.state.lang);
    if (A.state.themePref !== 'system') q.set('theme', A.state.themePref);
    if (A.state.demo) q.set('demo', '1');
    try { history.replaceState(null, '', location.pathname + '?' + q.toString()); } catch (e) { /* file:// */ }
  }

  /* Re-draw the parts that depend on the filters, keeping the focus where it was. */
  function update(focusSel) {
    syncURL();
    var ae = document.activeElement, key = focusSel || (ae && (ae.id ? '#' + ae.id : ae.getAttribute('data-f') ? '[data-f="' + ae.getAttribute('data-f') + '"]' : ae.getAttribute('data-area') ? '[data-area="' + ae.getAttribute('data-area') + '"]' : ae.getAttribute('data-period') != null ? '[data-period="' + ae.getAttribute('data-period') + '"]' : ae.hasAttribute('data-near') ? '.toolbar [data-near]' : ae.getAttribute('data-view') ? '[data-view="' + ae.getAttribute('data-view') + '"]' : null));
    var scroll = document.querySelector('.rail__scroll') ? document.querySelector('.rail__scroll').scrollTop : 0, railScroll = document.querySelector('.rail') ? document.querySelector('.rail').scrollTop : 0;
    var caret = ae && ae.selectionStart != null ? ae.selectionStart : null;
    document.getElementById('dirbody').innerHTML = rail() + '<div class="results" id="results">' + results() + '</div>';
    var tb = document.querySelector('.toolbar'); var tmp = document.createElement('div'); tmp.innerHTML = toolbar();
    var qv = document.getElementById('dq'); var keepQ = qv && document.activeElement === qv;
    if (!keepQ) tb.replaceWith(tmp.firstChild); else {
      var fresh = tmp.firstChild; tb.querySelector('.tail').replaceWith(fresh.querySelector('.tail'));
    }
    if (document.querySelector('.rail__scroll')) document.querySelector('.rail__scroll').scrollTop = scroll;
    if (document.querySelector('.rail')) document.querySelector('.rail').scrollTop = railScroll;
    if (key) { var el = document.querySelector(key); if (el && el !== document.activeElement) { el.focus(); if (caret != null && el.setSelectionRange) try { el.setSelectionRange(caret, caret); } catch (e) { } } }
    bind();
    if (F.view === 'map') drawMap();
  }

  function bind() {
    var dq = document.getElementById('dq');
    if (dq && !dq._b) { dq._b = 1; dq.addEventListener('input', function () { F.q = dq.value; update('#dq'); }); }
    document.querySelectorAll('[data-f]').forEach(function (i) { i.onchange = function () { F[i.getAttribute('data-f')] = i.checked; update(); }; });
    document.querySelectorAll('[data-area]').forEach(function (i) { i.onchange = function () { var id = +i.getAttribute('data-area'); F.areas = i.checked ? F.areas.concat(id) : F.areas.filter(function (x) { return x !== id; }); update(); }; });
    document.querySelectorAll('details.gov').forEach(function (d) { d.ontoggle = function () { openGovs[d.getAttribute('data-gov')] = d.open; }; });
    var radios = Array.prototype.slice.call(document.querySelectorAll('[data-period]'));
    radios.forEach(function (b, i) {
      b.onclick = function () { F.period = b.getAttribute('data-period'); F.from = ''; F.to = ''; if (!F.period && (F.sort === 'asc' || F.sort === 'desc')) F.sort = 'updated'; update('[data-period="' + F.period + '"]'); };
      b.onkeydown = function (e) {
        var k = e.key, rtl = A.state.lang === 'ar', d = 0;
        if (k === 'ArrowRight') d = rtl ? -1 : 1; else if (k === 'ArrowLeft') d = rtl ? 1 : -1; else if (k === 'ArrowDown') d = 1; else if (k === 'ArrowUp') d = -1; else return;
        e.preventDefault(); radios[(i + d + radios.length) % radios.length].click();
      };
    });
    ['pfrom', 'pto'].forEach(function (id) {
      var el = document.getElementById(id); if (!el) return;
      el.onchange = function () { F[id === 'pfrom' ? 'from' : 'to'] = el.value.trim(); update('#' + id); };
    });
    var sort = document.getElementById('sort'); if (sort) sort.onchange = function () { F.sort = sort.value; update('#sort'); };
    document.querySelectorAll('[data-clear]').forEach(function (b) { b.onclick = function () { F.areas = []; F.period = ''; F.from = ''; F.to = ''; F.open = F.evening = F.friday = F.verified = F.students = F.womens = false; F.q = ''; var dq2 = document.getElementById('dq'); if (dq2) dq2.value = ''; wantsOpen = false; update(sheetOpen ? '[data-sheet-close]' : '#dq'); }; });
    document.querySelectorAll('[data-near]').forEach(function (b) {
      b.onclick = function () {
        if (F.near) { F.near = false; update('.toolbar [data-near]'); return; }
        locating = true; update('.toolbar [data-near]');
        setTimeout(function () { locating = false; F.near = true; update('.toolbar [data-near]'); }, 700);
      };
    });
    document.querySelectorAll('[data-near-stop]').forEach(function (b) { b.onclick = function () { F.near = false; update('.toolbar [data-near]'); }; });
    document.querySelectorAll('[data-view]').forEach(function (b) { b.onclick = function () { F.view = b.getAttribute('data-view'); selected = null; update('[data-view="' + F.view + '"]'); }; });
    document.querySelectorAll('[data-sheet-open]').forEach(function (b) { b.onclick = function () { sheetOpen = true; update('.rail__head h2'); var h = document.querySelector('#rail [data-sheet-close].sheet-close'); if (h) h.focus(); }; });
    document.querySelectorAll('[data-sheet-close]').forEach(function (b) { b.onclick = function () { sheetOpen = false; wantsOpen = false; update('[data-sheet-open]'); }; });
    document.querySelectorAll('[data-heart]').forEach(function (b) { b.onclick = function () { A.signInPrompt('favorite', b); }; });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && sheetOpen) { sheetOpen = false; wantsOpen = false; update('[data-sheet-open]'); }
    if (e.key === 'Tab' && sheetOpen && window.innerWidth < 1024) {
      var f = Array.prototype.slice.call(document.querySelectorAll('#rail button, #rail input, #rail summary')).filter(function (x) { return x.offsetParent; });
      if (!f.length) return;
      if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    }
  });

  /* ───────── the map: the Strip drawn from its outline, the spaces at their real coordinates ───────── */
  /* The Strip's outline: _shared/data/strip-outline.json (the lead's, all 13 spaces inside). */
  var OUTLINE = window.MD.outline;
  var K = Math.cos(31.4 * Math.PI / 180);
  function P(lat, lng) { return [(lng - 34.2) * 111.32 * K, (31.6 - lat) * 110.57]; }
  /* Label points for the governorates the product lists (approximate centres, inside the Strip). */
  var GOV_AT = { 1: [31.558, 34.512], 2: [31.476, 34.452], 3: [31.398, 34.384], 4: [31.322, 34.300] };

  function drawMap() {
    var wrap = document.getElementById('mapwrap'); if (!wrap) return;
    var W = wrap.clientWidth, H = wrap.clientHeight;
    var pts = OUTLINE.map(function (p) { return P(p[0], p[1]); });
    var xs = pts.map(function (p) { return p[0]; }), ys = pts.map(function (p) { return p[1]; });
    var bx0 = Math.min.apply(0, xs), bx1 = Math.max.apply(0, xs), by0 = Math.min.apply(0, ys), by1 = Math.max.apply(0, ys);
    var fit = Math.min((W - 48) / (bx1 - bx0), (H - 48) / (by1 - by0));
    if (!map || map.W !== W || map.H !== H) map = { W: W, H: H, fit: fit, s: map && map.s ? Math.max(fit, map.s * fit / map.fit) : fit, cx: map ? map.cx : (bx0 + bx1) / 2, cy: map ? map.cy : (by0 + by1) / 2 };
    var w = A.t().dir;
    wrap.innerHTML = '<svg class="map" role="group" aria-label="' + w.map.label + '" xmlns="http://www.w3.org/2000/svg"><path class="land" d=""/><g class="labels"></g><g class="pins"></g></svg>' +
      '<div class="zoom"><button type="button" data-zoom="1" aria-label="' + w.map.zoomIn + '" title="' + w.map.zoomIn + '">' + A.icon('plus') + '</button><button type="button" data-zoom="-1" aria-label="' + w.map.zoomOut + '" title="' + w.map.zoomOut + '">' + A.icon('minus') + '</button></div>' +
      legend() + '<div id="mapsel"></div>';
    var svg = wrap.querySelector('svg');
    paint();
    wrap.querySelectorAll('[data-zoom]').forEach(function (b) { b.onclick = function () { zoomBy(b.getAttribute('data-zoom') === '1' ? 1.8 : 1 / 1.8); }; });
    svg.addEventListener('wheel', function (e) { e.preventDefault(); var r = svg.getBoundingClientRect(); zoomBy(e.deltaY < 0 ? 1.4 : 1 / 1.4, e.clientX - r.left, e.clientY - r.top); }, { passive: false });
    var drag = null;
    svg.addEventListener('pointerdown', function (e) { if (e.target.closest('.pin,.cluster')) return; drag = { x: e.clientX, y: e.clientY, cx: map.cx, cy: map.cy, moved: false }; svg.setPointerCapture(e.pointerId); });
    svg.addEventListener('pointermove', function (e) { if (!drag) return; var dx = e.clientX - drag.x, dy = e.clientY - drag.y; if (Math.abs(dx) + Math.abs(dy) > 3) drag.moved = true; map.cx = drag.cx - dx / map.s; map.cy = drag.cy - dy / map.s; paint(); });
    svg.addEventListener('pointerup', function () { drag = null; });
    if (selected) showSel(selected, false);
  }
  function zoomBy(f, px, py) {
    var ns = Math.max(map.fit, Math.min(map.fit * 24, map.s * f));
    if (px != null) { var wx = map.cx + (px - map.W / 2) / map.s, wy = map.cy + (py - map.H / 2) / map.s; map.cx = wx - (px - map.W / 2) / ns; map.cy = wy - (py - map.H / 2) / ns; }
    map.s = ns; paint();
  }
  function legend() {
    var w = A.t(), st = w.st;
    var items = [['live', st.live], ['hours', st.open], ['full', st.full], ['closed', st.closedHours], ['none', st.none]];
    return '<div class="legend"><h3>' + w.dir.map.legend + '</h3><ul>' + items.map(function (i) { return '<li><span class="bar k-' + i[0] + '"></span>' + i[1] + '</li>'; }).join('') + '</ul></div>';
  }
  function paint() {
    var wrap = document.getElementById('mapwrap'); if (!wrap) return;
    var svg = wrap.querySelector('svg'), s = map.s;
    /* drawn in screen pixels, so pins and labels keep their size at every zoom */
    svg.setAttribute('viewBox', '0 0 ' + map.W + ' ' + map.H);
    function px(x, y) { return [(x - map.cx) * s + map.W / 2, (y - map.cy) * s + map.H / 2]; }
    var land = OUTLINE.map(function (q) { var k = P(q[0], q[1]), p = px(k[0], k[1]); return p[0].toFixed(1) + ' ' + p[1].toFixed(1); });
    svg.querySelector('.land').setAttribute('d', 'M' + land.join('L') + 'Z');
    var w = A.t(), g = A.gaza();
    svg.querySelector('.labels').innerHTML = window.MD.governorates.map(function (gv) {
      var at = GOV_AT[gv.id]; if (!at) return '';
      var k = P(at[0], at[1]), p = px(k[0], k[1]);
      return '<text class="gov" x="' + p[0].toFixed(1) + '" y="' + p[1].toFixed(1) + '" font-size="12" text-anchor="middle">' + A.esc(A.L(gv, 'name')) + '</text>';
    }).join('');
    var list = filtered();
    var items = list.map(function (sp) { var k = P(sp.location.lat, sp.location.lng); return { sp: sp, x: k[0], y: k[1] }; });
    var clusters = [];
    items.forEach(function (it) {
      var c = null;
      for (var i = 0; i < clusters.length; i++) { var dx = (clusters[i].x - it.x) * s, dy = (clusters[i].y - it.y) * s; if (dx * dx + dy * dy < 22 * 22) { c = clusters[i]; break; } }
      if (c) { c.m.push(it); c.x = c.m.reduce(function (a, b) { return a + b.x; }, 0) / c.m.length; c.y = c.m.reduce(function (a, b) { return a + b.y; }, 0) / c.m.length; }
      else clusters.push({ x: it.x, y: it.y, m: [it] });
    });
    var html = '';
    clusters.forEach(function (c, ci) {
      var p = px(c.x, c.y);
      if (c.m.length > 1) {
        html += '<g class="cluster" role="button" tabindex="0" data-cluster="' + ci + '" aria-label="' + A.esc(w.board.cluster(c.m.length)) + '"><circle cx="' + p[0] + '" cy="' + p[1] + '" r="15" stroke-width="2"/><text x="' + p[0] + '" y="' + (p[1] + 4.5) + '" font-size="13" text-anchor="middle">' + c.m.length + '</text></g>';
      } else {
        var it = c.m[0], st = A.statusOf(it.sp, g), sel = selected === it.sp.slug, r = sel ? 10 : 6;
        html += '<g class="pin" role="button" tabindex="0" data-slug="' + it.sp.slug + '" aria-pressed="' + sel + '" aria-label="' + A.esc(w.dir.map.pin(A.nm(it.sp), A.stateWord(st))) + '">' +
          '<circle class="pin-focus" cx="' + p[0] + '" cy="' + p[1] + '" r="' + (r + 6) + '" stroke-width="2"/>' +
          (sel ? '<circle class="p-ring" cx="' + p[0] + '" cy="' + p[1] + '" r="' + (r + 3) + '" stroke-width="2.5"/>' : '') +
          '<circle class="p-' + st.mark + '" cx="' + p[0] + '" cy="' + p[1] + '" r="' + r + '" stroke-width="2"/></g>';
      }
    });
    if (F.near) { var yk = P(A.NEAR_POINT.lat, A.NEAR_POINT.lng), y = px(yk[0], yk[1]); html += '<g class="you" aria-label="' + w.dir.map.you + '" role="img"><circle class="o" cx="' + y[0] + '" cy="' + y[1] + '" r="7" stroke-width="3"/></g>'; }
    var selIt = items.filter(function (i) { return i.sp.slug === selected; })[0];
    if (selIt && clusters.some(function (c) { return c.m.length === 1 && c.m[0] === selIt; })) {
      var sp2 = px(selIt.x, selIt.y);
      html += '<g class="tag" aria-hidden="true"><rect rx="4"/><text x="' + sp2[0] + '" y="' + (sp2[1] - 24) + '" font-size="14" text-anchor="middle">' + A.esc(A.nm(selIt.sp)) + '</text></g>';
    }
    svg.querySelector('.pins').innerHTML = html;
    var tag = svg.querySelector('.tag');
    if (tag) { var bb = tag.querySelector('text').getBBox(), rc = tag.querySelector('rect'); rc.setAttribute('x', bb.x - 8); rc.setAttribute('y', bb.y - 3); rc.setAttribute('width', bb.width + 16); rc.setAttribute('height', bb.height + 6); }
    svg.querySelectorAll('.cluster').forEach(function (el) {
      var go = function () { var c = clusters[+el.getAttribute('data-cluster')]; map.cx = c.x; map.cy = c.y; var spread = Math.max.apply(0, c.m.map(function (m) { return Math.hypot(m.x - c.x, m.y - c.y); })) || 0.2; map.s = Math.min(map.fit * 24, Math.max(map.s * 2, 70 / spread)); paint(); var f = svg.querySelector('.pin,.cluster'); if (f) f.focus(); };
      el.addEventListener('click', go); el.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
    });
    svg.querySelectorAll('.pin').forEach(function (el) {
      var go = function () { selected = el.getAttribute('data-slug'); paint(); showSel(selected, true); };
      el.addEventListener('click', go); el.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
    });
  }
  function showSel(slug, focus) {
    var box = document.getElementById('mapsel'), sp = A.bySlug(slug); if (!box || !sp) return;
    var w = A.t().dir.map;
    box.innerHTML = '<div class="mapsel" role="region" aria-label="' + A.esc(A.nm(sp)) + '"><ul class="rows">' + A.row(sp, { near: F.near ? A.NEAR_POINT : null, period: F.period || null }) + '</ul>' +
      '<div class="mapsel__foot"><a class="btn btn-primary" href="' + A.href('space.html', { slug: slug }) + '">' + w.details + '</a><button type="button" class="btn btn-quiet" data-selclose>' + w.close + '</button></div></div>';
    box.querySelector('[data-selclose]').onclick = function () { var s0 = selected; selected = null; box.innerHTML = ''; paint(); var p = document.querySelector('.pin[data-slug="' + s0 + '"]'); if (p) p.focus(); };
    box.querySelectorAll('[data-heart]').forEach(function (b) { b.onclick = function () { A.signInPrompt('favorite', b); }; });
    if (focus) box.querySelector('.row__name').focus();
  }
  window.addEventListener('resize', function () { if (F.view === 'map' && document.getElementById('mapwrap')) { clearTimeout(window._mr); window._mr = setTimeout(drawMap, 120); } });

  A.page({
    nav: 'spaces',
    title: function () { return F.view === 'map' ? A.t().dir.title + ' — ' + A.t().dir.view.map : A.t().dir.title; },
    render: function () {
      if (wantsOpen && window.innerWidth < 1024) sheetOpen = true;
      var w = A.t(), g = A.gaza(), on = A.allSpaces().filter(function (x) { return A.statusOf(x, g).openNow; }).length;
      return '<div class="board ink dir-band"><div class="wrap dir-head"><h1 class="t-h1">' + w.dir.title + '</h1>' +
        '<div class="mini-clock"><span class="t-sec c2">' + w.board.now + '</span><span class="tm" data-clock>' + g.hhmm + '</span><span class="sep" aria-hidden="true"></span><span class="dot k-' + (on ? 'live' : 'closed') + '" aria-hidden="true"></span><span class="t-sec">' + w.board.openCount(on) + '</span></div></div></div>' + toolbar() +
        '<div class="wrap"><div class="dir" id="dirbody">' + rail() + '<div class="results" id="results">' + results() + '</div></div></div>';
    },
    mount: function () { bind(); if (F.view === 'map') { map = null; requestAnimationFrame(drawMap); } }
  });
})();
