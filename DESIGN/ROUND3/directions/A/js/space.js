/* A space's page: the space's board (name, state, today, price, the ways in), the unverified line, the
   filmstrip, then the facts (start column) and contact & location (end column, sticky). */
(function () {
  'use strict';
  var slug = A.Q.get('slug') || 'branch-hub';
  var lbIndex = 0;
  var K = Math.cos(31.4 * Math.PI / 180);
  function P(lat, lng) { return [(lng - 34.2) * 111.32 * K, (31.6 - lat) * 110.57]; }
  var OUTLINE = window.MD.outline;

  function photosOrdered(s) {
    var real = s.photos.filter(function (p) { return p.real; }), rest = s.photos.filter(function (p) { return !p.real; });
    return real.slice(0, 1).concat(rest, real.slice(1));
  }
  function updLine(s, key) {
    var w = A.t().page, iso = s.updatedAt[key]; if (!iso) return '';
    var stale = s.staleGroups && s.staleGroups.indexOf(key) >= 0;
    return '<span class="t-meta">' + w.upd[key](A.ago(iso)) + (stale ? ' · <span class="stale">' + w.stale + '</span>' : '') + '</span>';
  }
  function contactHref(c) {
    var v = c.value;
    if (c.type === 'WHATSAPP') return 'https://wa.me/' + v.replace(/\D/g, '');
    if (c.type === 'PHONE') return 'tel:' + v.replace(/\s/g, '');
    if (c.type === 'EMAIL') return 'mailto:' + v;
    return v;
  }
  function contactValue(c) {
    if (c.type === 'INSTAGRAM' || c.type === 'FACEBOOK' || c.type === 'TIKTOK' || c.type === 'X') { var m = c.value.match(/\/([^\/?#]+)\/?$/); return m ? '@' + m[1] : c.value; }
    return c.value;
  }
  var CICON = { WHATSAPP: 'message-circle', PHONE: 'phone', EMAIL: 'mail' };

  function board(s) {
    var w = A.t(), pg = w.page, g = A.gaza(), st = A.statusOf(s, g);
    var sub = st.live ? pg.live : (st.kind === 'open' || st.kind === 'closedHours') ? pg.byHours : st.verifiedUnset ? pg.unset : pg.unverifiedLine;
    var r = s.days ? s.days[g.dow] : undefined, today;
    if (!s.days) today = '<span class="quiet">' + w.card.noHours + '</span>';
    else if (!r) { var nx = A.nextOpening(s, g); today = '<span class="quiet">' + w.card.closedToday + '</span>' + (nx ? '<span class="t-sec c2">' + nx.text + '</span>' : ''); }
    else if (r.opensMinute === 0 && r.closesMinute === 1440) today = '<span class="quiet">' + pg.allDay + '</span>';
    else today = '<span class="t-board">' + A.ltr(A.clockOf(r.opensMinute) + '–' + A.clockOf(r.closesMinute)) + '</span>';
    var hp = A.headlinePrice(s, null);
    var price = hp ? '<span class="price">' + w.board.fromPrice(A.ltr(A.money(hp.amount)), w.card.periods[hp.period]) + '</span>' : '<span class="quiet">' + pg.noPrices + '</span>';
    var wa = s.contacts.filter(function (c) { return c.type === 'WHATSAPP'; })[0], ph = s.contacts.filter(function (c) { return c.type === 'PHONE'; })[0];
    var dirUrl = 'https://www.google.com/maps/dir/?api=1&destination=' + s.location.lat + ',' + s.location.lng;
    var acts = (wa ? '<a class="btn btn-primary" href="' + contactHref(wa) + '" target="_blank" rel="noopener">' + A.icon('message-circle') + pg.whatsapp + '</a>' : '') +
      (ph ? '<a class="btn btn-secondary" href="' + contactHref(ph) + '">' + A.icon('phone') + pg.call + '</a>' : '') +
      '<a class="btn ' + (wa ? 'btn-secondary' : 'btn-primary') + '" href="' + dirUrl + '" target="_blank" rel="noopener">' + A.icon('navigation') + pg.directions + '</a>';
    return '<section class="board sboard ink" aria-labelledby="h1"><div class="wrap">' +
      '<nav class="crumbs" aria-label="' + pg.breadcrumb + '"><a href="' + A.href('home.html') + '">' + w.home + '</a>' + A.chevronFwd('s16') + '<a href="' + A.href('spaces.html') + '">' + w.spaces + '</a>' + A.chevronFwd('s16') + '<span aria-current="page">' + A.esc(A.nm(s)) + '</span></nav>' +
      '<div class="sboard__id">' + A.plate(s) + '<div><h1 class="t-display" id="h1">' + A.esc(A.nm(s)) + '</h1>' +
      '<p class="other" lang="' + (A.state.lang === 'ar' ? 'en' : 'ar') + '">' + A.esc(A.other(s)) + '</p><p class="where">' + A.esc(A.areaLine(s)) + (s.isVerified ? ' · <span style="color:var(--text);font-weight:500">' + w.card.verified + '</span>' : '') + '</p></div>' +
      '<button type="button" class="btn btn-icon btn-secondary heart" data-heart aria-pressed="false" aria-label="' + A.esc(w.fav.save(A.nm(s))) + '">' + A.icon('heart') + '</button></div>' +
      '<div class="facts3"><div><span class="lbl">' + pg.status + '</span><span class="stv" data-row="' + s.slug + '"><span class="bar k-' + st.mark + '"></span><span class="stw">' + A.stateWord(st) + '</span></span><span class="t-sec c2">' + sub + '</span></div>' +
      '<div><span class="lbl">' + w.board.todayCol + '</span>' + today + '</div>' +
      '<div><span class="lbl">' + w.board.priceCol + '</span>' + price + '</div></div>' +
      '<div class="sboard__acts">' + acts + '</div></div></section>';
  }

  function film(s) {
    var w = A.t().page, ph = photosOrdered(s); if (!ph.length) return '';
    var firstReal = true;
    var items = ph.map(function (p, i) {
      var wide = p.real && firstReal; if (p.real) firstReal = false;
      var style = p.real ? (wide ? 'aspect-ratio:8/3' : 'aspect-ratio:4/3') : 'aspect-ratio:16/9';
      return '<button type="button" class="' + (p.real ? 'real' : 'poster') + '" style="' + style + '" data-lb="' + i + '" aria-label="' + A.esc(w.viewPhoto(i + 1)) + '"><img src="../_shared/photos/' + p.page + '" alt="" loading="lazy"></button>';
    }).join('');
    return '<section class="wrap" aria-label="' + A.esc(w.gallery(A.nm(s))) + '"><div class="film">' + items + '</div>' +
      (ph.length > 1 ? '<div class="film-foot"><button type="button" class="btn btn-secondary" data-lb="0">' + A.icon('images') + w.allPhotos(ph.length) + '</button></div>' : '') + '</section>' +
      '<dialog class="dlg lightbox" id="lb" aria-labelledby="lbcap"><div class="dlg__in"><figure><img id="lbimg" alt="" src="../_shared/photos/' + ph[0].page + '"><figcaption id="lbcap" style="margin-block-start:8px"></figcaption></figure>' +
      '<div class="dlg__actions" style="justify-content:space-between"><div style="display:flex;gap:8px">' +
      (ph.length > 1 ? '<button type="button" class="btn btn-secondary" data-lbstep="-1">' + A.icon(A.state.lang === 'ar' ? 'chevron-right' : 'chevron-left') + w.prev + '</button><button type="button" class="btn btn-secondary" data-lbstep="1">' + w.next + A.icon(A.state.lang === 'ar' ? 'chevron-left' : 'chevron-right') + '</button>' : '') +
      '</div><button type="button" class="btn btn-primary" data-lbclose>' + w.close + '</button></div></div></dialog>';
  }

  function sections(s) {
    var w = A.t(), pg = w.page, g = A.gaza(), out = '';
    if (s.announcements && s.announcements.length) {
      out += '<section aria-labelledby="ann-h"><div class="ann"><span class="edge" aria-hidden="true"></span><div><h2 class="t-sec w5" id="ann-h">' + pg.announcement + '</h2><p>' + w.demoAnnouncement + '</p></div></div></section>';
    }
    /* prices */
    var hasStudent = s.prices.some(function (p) { return p.audience === 'STUDENT'; });
    var periods = A.ORDER.filter(function (p) { return s.prices.some(function (x) { return x.period === p; }); });
    var ptable = periods.length
      ? '<table class="ptable"><thead><tr><th scope="col"><span class="sr">' + w.dir.f.subscription + '</span></th><th scope="col">' + w.board.generalCol + '</th>' + (hasStudent ? '<th scope="col">' + pg.students + '</th>' : '') + '</tr></thead><tbody>' +
        periods.map(function (p) {
          var gp = A.priceOf(s, p, 'GENERAL'), sp = A.priceOf(s, p, 'STUDENT');
          return '<tr><th scope="row">' + pg.periods[p] + '</th>' + (gp != null ? '<td>' + A.ltr(A.money(gp)) + '</td>' : '<td class="na">—</td>') + (hasStudent ? (sp != null ? '<td>' + A.ltr(A.money(sp)) + '</td>' : '<td class="na">—</td>') : '') + '</tr>';
        }).join('') + '</tbody></table><p class="paynote">' + pg.displayOnly + '</p>'
      : '<p class="c2">' + pg.noPrices + '</p>';
    out += '<section aria-labelledby="p-h"><div class="shead"><h2 class="t-h2" id="p-h">' + pg.sections.prices + '</h2>' + updLine(s, 'prices') + '</div>' + ptable + '</section>';
    /* hours: the week, Saturday first, today with the spark bar */
    var hours;
    if (!s.days) hours = '<p class="c2">' + pg.noHours + '</p>';
    else {
      var order = [6, 0, 1, 2, 3, 4, 5];
      hours = '<table class="htable"><caption class="sr">' + pg.hoursCaption + '</caption><thead class="sr"><tr><th scope="col">' + pg.days + '</th><th scope="col">' + pg.hoursCol + '</th></tr></thead><tbody>' + order.map(function (d) {
        var r = s.days[d], today = d === g.dow;
        var v = !r ? pg.closed : (r.opensMinute === 0 && r.closesMinute === 1440) ? pg.allDay : A.ltr(A.clockOf(r.opensMinute) + '–' + A.clockOf(r.closesMinute));
        return '<tr' + (today ? ' class="today"' : '') + '><th scope="row">' + w.dayNames[d] + (today ? '<span class="tod">' + pg.today + '</span>' : '') + '</th><td' + (!r ? ' class="closed"' : '') + '>' + v + '</td></tr>';
      }).join('') + '</tbody></table>';
    }
    out += '<section aria-labelledby="h-h"><div class="shead"><h2 class="t-h2" id="h-h">' + pg.sections.hours + '</h2>' + updLine(s, 'hours') + '</div>' + hours + '</section>';
    if (s.amenities.length) {
      out += '<section aria-labelledby="a-h"><div class="shead"><h2 class="t-h2" id="a-h">' + pg.sections.amenities + '</h2>' + updLine(s, 'amenities') + '</div><ul class="amen">' +
        s.amenities.map(function (a) { return '<li>' + A.icon(a.icon, 's16') + '<span>' + A.esc(A.L(a, 'name')) + '</span></li>'; }).join('') + '</ul></section>';
    }
    var desc = A.L(s, 'description');
    if (desc) out += '<section aria-labelledby="d-h"><div class="shead"><h2 class="t-h2" id="d-h">' + pg.sections.about + '</h2>' + updLine(s, 'profile') + '</div><p class="desc"' + (!s['description' + (A.state.lang === 'ar' ? 'Ar' : 'En')] ? ' lang="ar" dir="rtl"' : '') + '>' + A.esc(desc) + '</p></section>';
    return out;
  }

  function side(s) {
    var w = A.t(), pg = w.page, c = '';
    if (s.contacts.length) {
      c = '<h2 class="t-row">' + pg.sections.contacts + '</h2><div class="contacts">' + s.contacts.map(function (ct) {
        var ext = !(ct.type === 'PHONE' || ct.type === 'EMAIL');
        return '<a href="' + A.esc(contactHref(ct)) + '"' + (ext ? ' target="_blank" rel="noopener"' : '') + '>' + A.icon(CICON[ct.type] || 'at-sign') + '<span><span class="k">' + pg.types[ct.type] + '</span><span class="v">' + A.ltr(A.esc(contactValue(ct))) + '</span></span></a>';
      }).join('') + '</div>' + (s.updatedAt.contacts ? '<div class="upd">' + updLine(s, 'contacts') + '</div>' : '');
    }
    /* The whole Strip, fitted to a 340 x 220 frame, the space's pin and its area's name: where it is. */
    var VW = 340, VH = 220, pad = 14;
    var pts = OUTLINE.map(function (q) { return P(q[0], q[1]); });
    var xs = pts.map(function (q) { return q[0]; }), ys = pts.map(function (q) { return q[1]; });
    var x0 = Math.min.apply(0, xs), x1 = Math.max.apply(0, xs), y0 = Math.min.apply(0, ys), y1 = Math.max.apply(0, ys);
    var k = Math.min((VW - 2 * pad) / (x1 - x0), (VH - 2 * pad) / (y1 - y0));
    var ox = (VW - (x1 - x0) * k) / 2, oy = (VH - (y1 - y0) * k) / 2;
    function px(q) { return [ox + (q[0] - x0) * k, oy + (q[1] - y0) * k]; }
    var land = pts.map(function (q) { var r = px(q); return r[0].toFixed(1) + ' ' + r[1].toFixed(1); }).join('L');
    var pin = px(P(s.location.lat, s.location.lng));
    var area = A.esc(A.L(s.area, 'name'));
    var mini = '<svg class="minimap map" viewBox="0 0 ' + VW + ' ' + VH + '" role="img" aria-label="' + A.esc(pg.onMap(A.nm(s))) + ' — ' + area + '">' +
      '<path class="land" d="M' + land + 'Z"/>' +
      '<g class="you"><circle class="halo" cx="' + pin[0].toFixed(1) + '" cy="' + pin[1].toFixed(1) + '" r="11"/><circle class="o" cx="' + pin[0].toFixed(1) + '" cy="' + pin[1].toFixed(1) + '" r="6" stroke-width="2.5"/></g>' +
      '<g class="tag" data-tag-at="' + pin[0].toFixed(1) + ',' + pin[1].toFixed(1) + '"><rect rx="4"/><text font-size="13" text-anchor="end" x="' + (pin[0] - 16).toFixed(1) + '" y="' + (pin[1] + 4.5).toFixed(1) + '">' + area + '</text></g></svg>';
    var addr = A.L(s, 'address');
    return '<aside class="side" aria-label="' + pg.sections.location + '">' + c +
      '<h2 class="t-row"' + (c ? ' style="border-block-start:1px solid var(--border)"' : '') + '>' + pg.sections.location + '</h2>' + mini +
      '<div class="loc">' + (addr ? '<p' + (!s['address' + (A.state.lang === 'ar' ? 'Ar' : 'En')] ? ' lang="ar" dir="rtl" style="text-align:start"' : '') + '>' + A.esc(addr) + '</p>' : '') +
      '<p class="t-sec c2">' + A.esc(A.areaLine(s)) + '</p>' +
      '<a class="btn btn-secondary" href="https://www.google.com/maps/dir/?api=1&destination=' + s.location.lat + ',' + s.location.lng + '" target="_blank" rel="noopener">' + A.icon('navigation') + pg.directions + '</a></div></aside>';
  }

  A.page({
    nav: 'spaces',
    title: function () { var s = A.bySlug(slug); return s ? A.nm(s) : A.t().page.notFoundTitle; },
    render: function () {
      var s = A.bySlug(slug), w = A.t(), pg = w.page;
      if (!s) {
        return '<section class="board ink"><div class="wrap" style="padding-block:64px"><h1 class="t-h1">' + pg.notFoundTitle + '</h1><p class="c2" style="margin-block:8px 24px">' + pg.notFoundText + '</p><a class="btn btn-primary" href="' + A.href('spaces.html') + '">' + pg.back + '</a></div></section>';
      }
      var notice = !s.isVerified ? '<div class="wrap"><div class="notice-line"><span>' + pg.unverified(A.ago(s.updatedAt.profile)) + '</span><button type="button" class="btn btn-secondary" data-claim>' + pg.claim + '</button></div></div>' : '';
      var wa = s.contacts.filter(function (c) { return c.type === 'WHATSAPP'; })[0], ph = s.contacts.filter(function (c) { return c.type === 'PHONE'; })[0];
      var qbar = (wa || ph) ? '<div class="qbar" role="region" aria-label="' + pg.bar + '">' + (wa ? '<a class="btn btn-primary" href="' + contactHref(wa) + '" target="_blank" rel="noopener">' + A.icon('message-circle') + pg.whatsapp + '</a>' : '') + (ph ? '<a class="btn btn-secondary" href="' + contactHref(ph) + '">' + A.icon('phone') + pg.call + '</a>' : '') + '</div>' : '';
      var c = window.MD.contact;
      var dlg = '<dialog class="dlg" id="claim" aria-labelledby="claim-h"><div class="dlg__in"><div class="dlg__head"><h2 class="t-h2" id="claim-h">' + pg.dlgTitle + '</h2><button type="button" class="btn btn-icon" data-claimclose aria-label="' + pg.close + '">' + A.icon('x') + '</button></div><p class="c2">' + pg.dlgText + '</p>' +
        '<div class="contact-lines"><a href="https://wa.me/' + c.whatsapp.replace(/\D/g, '') + '" target="_blank" rel="noopener">' + A.icon('message-circle') + '<span class="k">' + w.aboutT.whatsapp + '</span><span class="v">' + A.ltr(c.whatsapp) + '</span></a><a href="mailto:' + c.email + '">' + A.icon('mail') + '<span class="k">' + w.aboutT.email + '</span><span class="v">' + A.ltr(c.email) + '</span></a></div></div></dialog>';
      return board(s) + notice + film(s) +
        '<div class="wrap sbody"><div class="main">' + sections(s) +
        '<div class="report"><button type="button" data-report>' + A.icon('flag', 's16') + w.page.report + '</button></div></div>' + side(s) + '</div>' + qbar + dlg;
    },
    mount: function () {
      var s = A.bySlug(slug);
      document.body.classList.toggle('has-qbar', !!document.querySelector('.qbar'));
      var hb = document.querySelector('[data-heart]'); if (hb) hb.onclick = function () { A.signInPrompt('favorite', hb); };
      var rb = document.querySelector('[data-report]'); if (rb) rb.onclick = function () { A.signInPrompt('report', rb); };
      var cd = document.getElementById('claim'), cb = document.querySelector('[data-claim]');
      if (cb) cb.onclick = function () { cd.showModal(); };
      var cc = document.querySelector('[data-claimclose]'); if (cc) cc.onclick = function () { cd.close(); };
      if (cd) cd.addEventListener('close', function () { if (cb) cb.focus(); });
      var tg = document.querySelector('.minimap .tag');
      if (tg) { var bb = tg.querySelector('text').getBBox(), rc = tg.querySelector('rect'); rc.setAttribute('x', bb.x - 7); rc.setAttribute('y', bb.y - 3); rc.setAttribute('width', bb.width + 14); rc.setAttribute('height', bb.height + 6); }
      var bar = document.querySelector('.qbar'), acts = document.querySelector('.sboard__acts');
      if (bar && acts && 'IntersectionObserver' in window) {
        bar.classList.add('away');
        new IntersectionObserver(function (es) { var e = es[es.length - 1]; bar.classList.toggle('away', e.isIntersecting || e.boundingClientRect.top > 0); }).observe(acts);
      }
      if (!s) return;
      var ph = photosOrdered(s), lb = document.getElementById('lb'), opener = null;
      function show(i) { lbIndex = (i + ph.length) % ph.length; document.getElementById('lbimg').src = '../_shared/photos/' + ph[lbIndex].page; document.getElementById('lbcap').textContent = A.t().page.photo(lbIndex + 1, ph.length, A.nm(s)); }
      document.querySelectorAll('[data-lb]').forEach(function (b) { b.onclick = function () { opener = b; show(+b.getAttribute('data-lb')); lb.showModal(); }; });
      document.querySelectorAll('[data-lbstep]').forEach(function (b) { b.onclick = function () { show(lbIndex + +b.getAttribute('data-lbstep')); }; });
      var lc = document.querySelector('[data-lbclose]'); if (lc) lc.onclick = function () { lb.close(); };
      if (lb) {
        lb.addEventListener('close', function () { if (opener) opener.focus(); });
        lb.addEventListener('keydown', function (e) { if (ph.length < 2) return; var rtl = A.state.lang === 'ar'; if (e.key === 'ArrowLeft') show(lbIndex + (rtl ? 1 : -1)); if (e.key === 'ArrowRight') show(lbIndex + (rtl ? -1 : 1)); });
      }
    }
  });
})();
