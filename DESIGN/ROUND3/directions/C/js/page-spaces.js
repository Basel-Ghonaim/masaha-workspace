/* The directory — the refine bar, the refine panel (under the bar; a sheet on the phone), the chapters or one list,
   and the printed map. The filters filter the 13 spaces for real. */
(function () {
  var Q = new URLSearchParams(location.search);
  var S = {
    q: Q.get('q') || '', areas: Q.get('area') ? [+Q.get('area')] : [], period: '', from: '', to: '',
    openNow: Q.get('open') === '1', evening: false, friday: false, verified: false, students: false, womens: false,
    sort: 'updated', near: false, view: Q.get('view') === 'map' ? 'map' : 'list', panel: Q.get('filters') === 'open', selected: null
  };
  if (S.panel) S.period = 'MONTH';
  if (Q.get('gov')) M.govs.forEach(function (g) { if (g.id === +Q.get('gov')) S.areas = g.areas.map(function (a) { return a.id; }).filter(function (id) { return M.spaces().some(function (s) { return s.areaId === id; }); }); });
  var gmap = null;
  var phone = function () { return window.innerWidth < 768; };

  function money(v) { return String(v); }
  function priceOk(s) {
    if (!S.period) return true;
    var lp = M.lowest(s, S.period); if (!lp) return false;
    var v = lp.amount / 100, f = parseFloat(S.from), t = parseFloat(S.to);
    if (!isNaN(f) && f > 0 && v < f) return false;
    if (!isNaN(t) && t > 0 && (isNaN(f) || t >= f) && v > t) return false;
    return true;
  }
  function match(s) {
    if (S.q.trim()) {
      var q = S.q.trim().toLowerCase(), a = M.areas[s.areaId].area;
      var hay = [s.nameAr, s.nameEn, a.nameAr, a.nameEn].join(' ').toLowerCase();
      if (hay.indexOf(q) < 0) return false;
    }
    if (S.areas.length && S.areas.indexOf(s.areaId) < 0) return false;
    if (!priceOk(s)) return false;
    if (S.openNow && !M.isOpenNow(s)) return false;
    if (S.evening && !s.worksEvenings) return false;
    if (S.friday && !(s.days && s.days[5])) return false;
    if (S.verified && !s.verified) return false;
    if (S.students && !s.prices.some(function (p) { return p.audience === 'STUDENT'; })) return false;
    if (S.womens && !s.womensHall) return false;
    return true;
  }
  function results() {
    var list = M.spaces().filter(match);
    var byNews = function (a, b) { return (b.latest || '').localeCompare(a.latest || ''); };
    if (S.near) { list.forEach(function (s) { s._km = M.km(M.HERE, s.loc); }); list.sort(function (a, b) { return a._km - b._km; }); }
    else if (S.sort === 'name') list.sort(function (a, b) { return M.name(a).localeCompare(M.name(b), M.lang); });
    else if ((S.sort === 'priceAsc' || S.sort === 'priceDesc') && S.period) list.sort(function (a, b) { var d = M.lowest(a, S.period).amount - M.lowest(b, S.period).amount; return S.sort === 'priceAsc' ? d : -d; });
    else list.sort(byNews);
    return list;
  }
  function activeCount() {
    return S.areas.length + (S.period ? 1 : 0) + ['openNow', 'evening', 'friday', 'verified', 'students', 'womens'].filter(function (k) { return S[k]; }).length;
  }
  function filterSentence() {
    var t = M.t().dir.s, parts = [];
    if (S.q.trim()) parts.push(t.q(M.esc(S.q.trim())));
    if (S.areas.length) {
      var names = S.areas.map(function (id) { return M.esc(M.aname(M.areas[id].area)); });
      var joined = M.lang === 'ar' ? names.join(t.and) : names.length > 1 ? names.slice(0, -1).join(', ') + t.and + names[names.length - 1] : names[0];
      parts.push(t.inAreas(joined));
    }
    ['openNow', 'evening', 'friday'].forEach(function (k) { if (S[k]) parts.push(t[k]); });
    if (S.period) {
      var f = parseFloat(S.from), to = parseFloat(S.to), r = '';
      if (f > 0 && to > 0 && to >= f) r = ' ' + t.between(M.ltr(money(f)), M.ltr(money(to)));
      else if (f > 0) r = ' ' + t.fromOnly(M.ltr(money(f)));
      else if (to > 0) r = ' ' + t.toOnly(M.ltr(money(to)));
      parts.push(t.per[S.period] + r);
    }
    ['verified', 'students', 'womens'].forEach(function (k) { if (S[k]) parts.push(t[k]); });
    return parts.join(t.comma);
  }

  /* ---------- the refine panel ---------- */
  function panelHtml() {
    var t = M.t(), d = t.dir, all = M.spaces();
    var areas = M.govs.map(function (g) {
      var rows = g.areas.map(function (a) { var c = all.filter(function (s) { return s.areaId === a.id; }).length; if (!c) return '';
        return '<label class="check"><input type="checkbox" name="area" value="' + a.id + '"' + (S.areas.indexOf(a.id) >= 0 ? ' checked' : '') + '><span>' + M.esc(M.aname(a)) + '</span><span class="count">' + c + '</span></label>'; }).join('');
      return rows ? '<div class="sub-group"><p class="gov-label">' + M.esc(M.gname(g)) + '</p>' + rows + '</div>' : '';
    }).join('');
    var per = ['', 'HOUR', 'DAY', 'WEEK', 'MONTH'];
    var seg = '<div class="seg" role="radiogroup" aria-label="' + d.subscription + '">' + per.map(function (p) { return '<label><input type="radio" name="period" value="' + p + '"' + (S.period === p ? ' checked' : '') + '><span>' + (p ? d.periods[p] : d.allP) + '</span></label>'; }).join('') + '</div>';
    var range = S.period ? (function () {
      var r = M.ranges[S.period];
      return '<div class="range"><div class="field"><label for="p-from">' + d.from + '</label><input class="input" id="p-from" inputmode="numeric" dir="ltr" value="' + M.esc(S.from) + '" placeholder="' + r.minAgorot / 100 + '" aria-describedby="p-help"></div>' +
        '<div class="field"><label for="p-to">' + d.to + '</label><input class="input" id="p-to" inputmode="numeric" dir="ltr" value="' + M.esc(S.to) + '" placeholder="' + r.maxAgorot / 100 + '" aria-describedby="p-help"></div></div>' +
        '<p class="help" id="p-help">' + d.rangeHelp(d.priceNames[S.period]) + '</p><p class="error" id="p-err" hidden>' + d.belowMin + '</p>';
    })() : '<p class="help">' + d.subHint + '</p>';
    var chk = function (k, label) { return '<label class="check"><input type="checkbox" name="' + k + '"' + (S[k] ? ' checked' : '') + '><span>' + label + '</span></label>'; };
    var n = results().length;
    return '<div class="rp-head"><h2 class="t-h2" id="rp-title">' + d.refineTitle + '</h2><p class="t-meta">' + d.applied + '</p>' +
      '<button class="btn btn-icon rp-close" type="button" id="rp-close" aria-label="' + d.close + '">' + M.icon('x') + '</button></div>' +
      '<div class="rp-groups">' +
      '<fieldset class="rp-group"><legend>' + d.area + '</legend>' + areas + '</fieldset>' +
      '<fieldset class="rp-group"><legend>' + d.price + '</legend><p class="label" id="sub-l">' + d.subscription + '</p>' + seg + '<div id="range-slot">' + range + '</div></fieldset>' +
      '<fieldset class="rp-group"><legend>' + d.schedule + '</legend>' + chk('openNow', d.openNow) + chk('evening', d.evening) + chk('friday', d.friday) + '</fieldset>' +
      '<fieldset class="rp-group"><legend>' + d.other + '</legend>' + chk('verified', d.verified) + chk('students', d.students) + chk('womens', d.womens) + '</fieldset>' +
      '</div><div class="rp-foot"><button class="btn btn-primary" type="button" id="rp-show"' + (n ? '' : ' aria-disabled="true"') + '>' + d.show(n) + '</button>' +
      '<button class="btn btn-quiet" type="button" data-clear>' + d.clearFilters + '</button></div>';
  }

  /* ---------- the results ---------- */
  function listHtml(list) {
    var t = M.t(), d = t.dir;
    if (!list.length) return '<div class="g chapter-first"><div class="g-start"></div><div class="g-main empty"><h2 class="t-h2">' + d.noMatch.title + '</h2><p class="t-body">' + d.noMatch.text + '</p><button class="btn btn-secondary" type="button" data-clear>' + d.clearFilters + '</button></div></div>';
    var entry = function (s) { return '<li>' + M.entry(s, { km: S.near ? s._km : null, price: S.period ? M.lowest(s, S.period) : null }) + '</li>'; };
    if (S.sort === 'updated' && !S.near) {
      return M.govs.map(function (g, i) {
        var sp = list.filter(function (s) { return M.govOf(s).id === g.id; }); if (!sp.length) return '';
        var openN = sp.filter(M.isOpenNow).length;
        return '<section class="g chapter-block" aria-labelledby="ch-' + g.id + '"><div class="g-start chapter-head sticky-head"><h2 class="t-h2 ch-title" id="ch-' + g.id + '">' + (openN ? '<span class="mark live" aria-hidden="true"></span>' : '') + M.esc(M.gname(g)) + '</h2>' +
          '<p class="t-meta">' + d.chapterCount(sp.length) + (openN ? ' · ' + t.home.chapterOpen(openN) : '') + '</p></div><div class="g-main"><ul class="entries">' + sp.map(entry).join('') + '</ul></div></section>';
      }).join('');
    }
    var sortName = S.near ? d.sorts.distance : S.sort === 'name' ? d.sorts.name : S.sort === 'priceAsc' ? d.priceAsc[S.period] : d.priceDesc[S.period];
    return '<section class="g chapter-block" aria-labelledby="ch-all"><div class="g-start chapter-head sticky-head"><h2 class="t-h2" id="ch-all">' + d.oneList + '</h2><p class="t-meta">' + d.sortLabel + ': ' + sortName + '</p></div>' +
      '<div class="g-main"><ul class="entries">' + list.map(entry).join('') + '</ul></div></section>';
  }
  function mapHtml(list) {
    var t = M.t(), st = t.st;
    var leg = [['live', st.available], ['full', st.full], ['byhours', st.open + ' (' + st.byHoursShort + ')'], ['closed', st.closed], ['none', st.none]];
    var govs = M.govs.map(function (g) { var n = list.filter(function (s) { return M.govOf(s).id === g.id; }).length; return n ? '<li><button type="button" class="gov-jump" data-gov="' + g.id + '"><span class="nm">' + M.esc(M.gname(g)) + '</span><span class="ct">' + t.count(n) + '</span></button></li>' : ''; }).join('');
    return '<div class="map-layout"><div class="map-wrap"><div class="map-frame dir-map" id="map" role="region" aria-label="' + t.map.label + '"></div>' +
      '<div class="map-tools" role="group" aria-label="' + t.map.label + '"><button type="button" id="z-in" aria-label="' + t.map.zoomIn + '">' + M.icon('plus') + '</button><button type="button" id="z-out" aria-label="' + t.map.zoomOut + '">' + M.icon('minus') + '</button><button type="button" id="z-all" aria-label="' + t.map.whole + '">' + M.icon('maximize') + '</button></div>' +
      '<div id="map-panel-over" class="panel-over"></div></div>' +
      '<aside class="map-aside"><div id="map-panel-aside"></div>' +
      '<section aria-labelledby="mj-h"><h2 class="aside-h" id="mj-h">' + t.home.areas + '</h2><ul class="gov-jumps"><li><button type="button" class="gov-jump" data-gov="all"><span class="nm">' + t.map.whole + '</span><span class="ct">' + t.count(list.length) + '</span></button></li>' + govs + '</ul></section>' +
      '<section aria-labelledby="lg-h"><h2 class="aside-h" id="lg-h">' + t.map.legend + '</h2><dl class="legend">' + leg.map(function (l) { return '<div><dt><span class="mark ' + l[0] + '" aria-hidden="true"></span><span class="vh">·</span></dt><dd>' + l[1] + '</dd></div>'; }).join('') + '</dl></section>' +
      '<p class="t-meta map-note">' + t.map.style + '</p></aside></div>';
  }
  function mapPanel() {
    var wide = window.innerWidth >= 1024;
    var over = document.getElementById('map-panel-over'), aside = document.getElementById('map-panel-aside'); if (!over) return;
    var slot = wide ? aside : over; (wide ? over : aside).innerHTML = '';
    var s = S.selected && M.bySlug(S.selected);
    if (!s) { slot.innerHTML = ''; return; }
    var t = M.t();
    slot.innerHTML = '<div class="map-panel" role="region" aria-labelledby="mp-h"><div class="top"><h2 class="t-entry" id="mp-h">' + M.esc(M.name(s)) + '</h2><button class="btn btn-icon" type="button" id="mp-close" aria-label="' + t.map.close + '">' + M.icon('x') + '</button></div>' +
      '<p class="t-lede">' + M.mark(M.state(s)) + ' ' + M.sentence(s) + '</p><p class="t-meta">' + M.esc(M.stateMeta(s)) + '</p>' +
      '<a class="btn btn-primary" href="space.html?slug=' + s.slug + '">' + t.map.details + '</a></div>';
  }

  function update(opts) {
    opts = opts || {};
    var t = M.t(), d = t.dir, list = results(), n = activeCount();
    var sum = document.getElementById('summary');
    var sentence = filterSentence();
    sum.innerHTML = sentence ? d.matching(list.length) + ' — ' + sentence + '.' : d.all(list.length);
    document.getElementById('sum-clear').hidden = !sentence;
    var rb = document.getElementById('refine-btn');
    rb.querySelector('.n').textContent = n ? ' (' + n + ')' : '';
    var nl = document.getElementById('near-line');
    nl.hidden = !S.near;
    if (S.near) nl.innerHTML = '<span class="mark live" aria-hidden="true"></span>' + d.sortedNear + ' ' + d.approx + ' <span class="muted">' + d.nearDemo + '</span> <button class="btn btn-quiet" type="button" id="near-stop">' + d.stopNear + '</button>';
    var nb = document.getElementById('near-btn'); nb.setAttribute('aria-pressed', String(S.near));
    var show = document.getElementById('rp-show');
    if (show) { show.textContent = d.show(list.length); if (list.length) show.removeAttribute('aria-disabled'); else show.setAttribute('aria-disabled', 'true'); }
    var res = document.getElementById('results');
    if (S.view === 'map') {
      if (!gmap || opts.remap) {
        res.innerHTML = mapHtml(list);
        gmap = new GuideMap(document.getElementById('map'), { spaces: list, selected: S.selected, you: S.near ? M.HERE : null, onSelect: function (slug) { S.selected = slug; mapPanel(); } });
      } else gmap.set({ spaces: list, you: S.near ? M.HERE : null });
      mapPanel();
    } else { gmap = null; res.innerHTML = listHtml(list); }
  }
  function openPanel(open, focus) {
    S.panel = open;
    var p = document.getElementById('refine'), b = document.getElementById('refine-btn');
    b.setAttribute('aria-expanded', String(open));
    if (open) {
      p.innerHTML = panelHtml(); p.hidden = false;
      document.body.classList.toggle('sheet-open', phone());
      requestAnimationFrame(function () { p.classList.add('in'); });
      if (focus) { var f = phone() ? document.getElementById('rp-close') : p.querySelector('input'); if (f) f.focus(); }
    } else {
      p.classList.remove('in'); p.hidden = true; document.body.classList.remove('sheet-open');
      if (focus) b.focus();
    }
  }
  function syncView() { var u = new URL(location.href); if (S.view === 'map') u.searchParams.set('view', 'map'); else u.searchParams.delete('view'); u.searchParams.delete('filters'); try { history.replaceState(null, '', u); } catch (e) {} }

  M.boot({
    id: 'spaces',
    title: function () { return M.t().dir.title; },
    render: function () {
      var t = M.t(), d = t.dir;
      var sortOpts = [['updated', d.sorts.updated], ['name', d.sorts.name]];
      if (S.period) sortOpts.push(['priceAsc', d.priceAsc[S.period]], ['priceDesc', d.priceDesc[S.period]]);
      document.getElementById('main').innerHTML = '<div class="wrap">' +
        '<header class="page-head dir-head"><h1 class="t-h1">' + d.title + '</h1><p class="t-stand count-line"><span id="summary"></span> <button class="btn btn-quiet sum-clear" type="button" id="sum-clear" data-clear hidden>' + d.clear + '</button></p></header>' +
        '<div class="refine-bar">' +
        '<div class="rb-search" role="search"><label class="vh" for="dir-q">' + d.searchLabel + '</label>' + M.icon('search') + '<input class="input" id="dir-q" type="search" placeholder="' + d.searchPh + '" value="' + M.esc(S.q) + '" autocomplete="off"></div>' +
        '<button class="btn btn-secondary" type="button" id="refine-btn" aria-expanded="false" aria-controls="refine">' + M.icon('sliders-horizontal') + '<span>' + d.refine + '<span class="n"></span></span></button>' +
        '<div class="rb-sort"><label for="dir-sort">' + d.sortLabel + '</label><span class="select-wrap"><select class="select quiet" id="dir-sort"' + (S.near ? ' disabled' : '') + '>' + sortOpts.map(function (o) { return '<option value="' + o[0] + '"' + (S.sort === o[0] ? ' selected' : '') + '>' + o[1] + '</option>'; }).join('') + '</select>' + M.icon('chevron-down') + '</span></div>' +
        '<button class="btn btn-secondary" type="button" id="near-btn" aria-pressed="false">' + M.icon('locate-fixed') + '<span>' + d.near + '</span></button>' +
        '<div class="seg rb-view" role="group" aria-label="' + d.view + '"><button type="button" data-view="list" aria-pressed="' + (S.view === 'list') + '">' + M.icon('list') + d.list + '</button><button type="button" data-view="map" aria-pressed="' + (S.view === 'map') + '">' + M.icon('map') + d.map + '</button></div>' +
        '</div>' +
        '<div class="refine-panel" id="refine" role="region" aria-labelledby="rp-title" hidden></div>' +
        '<p class="near-line t-fact" id="near-line" hidden></p>' +
        '<div id="results" class="results"></div></div>';
      gmap = null;
      update({ remap: true });
      if (S.panel) openPanel(true, false);
    }
  });

  /* ---------- events ---------- */
  var tq;
  document.addEventListener('input', function (e) {
    if (e.target.id === 'dir-q') { clearTimeout(tq); tq = setTimeout(function () { S.q = e.target.value; update(); }, 120); }
    if (e.target.id === 'p-from' || e.target.id === 'p-to') {
      S[e.target.id === 'p-from' ? 'from' : 'to'] = e.target.value.replace(/[^\d.]/g, '');
      var bad = parseFloat(S.to) > 0 && parseFloat(S.from) > 0 && parseFloat(S.to) < parseFloat(S.from);
      var er = document.getElementById('p-err'); if (er) er.hidden = !bad;
      document.getElementById('p-to').setAttribute('aria-invalid', String(bad));
      update();
    }
  });
  document.addEventListener('change', function (e) {
    var el = e.target;
    if (el.name === 'area') { var id = +el.value; S.areas = el.checked ? S.areas.concat(id) : S.areas.filter(function (x) { return x !== id; }); update(); }
    else if (el.name === 'period') {
      S.period = el.value; S.from = ''; S.to = ''; if (!S.period && /price/.test(S.sort)) S.sort = 'updated';
      M.page.render(); openPanel(true, false); var r = document.querySelector('input[name=period][value="' + S.period + '"]'); if (r) r.focus();
    }
    else if (['openNow', 'evening', 'friday', 'verified', 'students', 'womens'].indexOf(el.name) >= 0) { S[el.name] = el.checked; update(); }
    else if (el.id === 'dir-sort') { S.sort = el.value; update(); }
  });
  document.addEventListener('click', function (e) {
    var b;
    if ((b = e.target.closest('#refine-btn'))) { openPanel(!S.panel, true); return; }
    if ((b = e.target.closest('#rp-close'))) { openPanel(false, true); return; }
    if ((b = e.target.closest('#rp-show'))) { if (b.getAttribute('aria-disabled') === 'true') return; openPanel(false, false); var r = document.getElementById('results'); r.setAttribute('tabindex', '-1'); r.focus(); return; }
    if ((b = e.target.closest('[data-clear]'))) {
      Object.assign(S, { q: '', areas: [], period: '', from: '', to: '', openNow: false, evening: false, friday: false, verified: false, students: false, womens: false, sort: S.sort === 'name' ? 'name' : 'updated' });
      var wasOpen = S.panel; M.page.render(); if (wasOpen) openPanel(true, false); document.getElementById('dir-q').focus(); return;
    }
    if ((b = e.target.closest('#near-btn'))) {
      if (S.near) { S.near = false; update(); return; }
      var lbl = b.querySelector('span'); lbl.textContent = M.t().dir.locating; b.setAttribute('aria-busy', 'true');
      setTimeout(function () { b.removeAttribute('aria-busy'); lbl.textContent = M.t().dir.near; S.near = true; update(); document.getElementById('dir-sort').disabled = true; }, 500);
      return;
    }
    if ((b = e.target.closest('#near-stop'))) { S.near = false; update(); document.getElementById('dir-sort').disabled = false; document.getElementById('near-btn').focus(); return; }
    if ((b = e.target.closest('[data-view]'))) {
      S.view = b.getAttribute('data-view'); S.selected = null; syncView();
      document.querySelectorAll('[data-view]').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      update({ remap: true }); return;
    }
    if ((b = e.target.closest('#z-in'))) { gmap.zoom(1.6); return; }
    if ((b = e.target.closest('#z-out'))) { gmap.zoom(1 / 1.6); return; }
    if ((b = e.target.closest('#z-all'))) { gmap.whole(); return; }
    if ((b = e.target.closest('[data-gov]'))) {
      var gid = b.getAttribute('data-gov'), lst = results();
      if (gid === 'all') gmap.whole(); else gmap.fitTo(lst.filter(function (s) { return M.govOf(s).id === +gid; }));
      return;
    }
    if ((b = e.target.closest('#mp-close'))) { S.selected = null; gmap.set({ selected: null }); mapPanel(); return; }
    if (S.panel && phone() && e.target.classList && e.target.classList.contains('refine-panel')) openPanel(false, true);
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && S.panel) openPanel(false, true); });
})();
