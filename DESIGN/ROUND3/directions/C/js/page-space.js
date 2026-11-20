/* A space's page — an entry spread: the name, the composed sentence, the ink fact box, then the rest in U8's order. */
(function () {
  var slug = new URLSearchParams(location.search).get('slug') || 'branch-hub';
  var SAT_FIRST = [6, 0, 1, 2, 3, 4, 5];
  var CHANNEL = {
    WHATSAPP: function (v) { return 'https://wa.me/' + v.replace(/[^\d]/g, ''); }, PHONE: function (v) { return 'tel:' + v; },
    EMAIL: function (v) { return 'mailto:' + v; }
  };
  function href(c) { return CHANNEL[c.type] ? CHANNEL[c.type](c.value) : c.value; }
  function upd(s, g) {
    var t = M.t().sp, iso = s.updatedAt[g]; if (!iso) return '';
    return '<p class="t-meta">' + t.updated[g] + M.esc(M.t().ago(iso)) + (s.stale.indexOf(g) >= 0 ? ' · ' + t.stale : '') + '</p>';
  }

  function factBox(s) {
    var t = M.t(), sp = t.sp, stt = M.state(s), td = M.today(s), n = M.now();
    var sub = stt.live ? t.st.live : stt.kind === 'none' ? (s.verified ? t.st.unset : t.st.unverified) : t.st.byHours;
    var todayLine = !td ? sp.noHours : td.closed ? t.sen.closedToday : td.allDay ? sp.today + ' · ' + sp.allDay : sp.todayRange(M.ltr(td.range));
    var html = '<section class="fact-box" aria-labelledby="fb-h"><h2 id="fb-h" class="vh">' + sp.statusContact + '</h2>' +
      '<div class="fb-state"><p class="word">' + M.mark(stt, true) + stt.word + '</p><p class="t-fact">' + todayLine + '</p><p class="sub">' + sub + '</p></div>';
    if (s.days) {
      html += '<div class="rule"><table class="week"><caption class="fb-h">' + sp.hoursCaption + '</caption><tbody>' + SAT_FIRST.map(function (i) {
        var d = s.days[i], today = i === n.day;
        var v = !d ? '<span class="closed-day">' + sp.closed + '</span>' : (d.opensMinute === 0 && d.closesMinute >= 1440) ? sp.allDay : M.ltr(M.time(d.opensMinute) + '–' + M.time(d.closesMinute));
        return '<tr' + (today ? ' class="today"' : '') + '><th scope="row">' + (today ? '<span class="mark live" aria-hidden="true"></span>' : '') + t.days[i] + (today ? '<span class="vh"> (' + sp.today + ')</span>' : '') + '</th><td>' + v + '</td></tr>';
      }).join('') + '</tbody></table>' + (s.updatedAt.hours ? '<p class="sub" style="margin-top:8px">' + sp.updated.hours + M.esc(t.ago(s.updatedAt.hours)) + '</p>' : '') + '</div>';
    }
    var gen = M.periodOrder.map(function (p) { return M.lowest(s, p); }).filter(Boolean);
    if (gen.length) html += '<div class="rule"><p class="fb-h">' + sp.lowest + '</p><div class="fb-prices">' + gen.map(function (p) { return '<div><span>' + sp.periods[p.period] + '</span><span>' + M.ltr(M.money(p.amount)) + '</span></div>'; }).join('') + '</div></div>';
    var wa = s.contacts.filter(function (c) { return c.type === 'WHATSAPP'; })[0], ph = s.contacts.filter(function (c) { return c.type === 'PHONE'; })[0];
    var others = s.contacts.filter(function (c) { return c.type !== 'WHATSAPP' && c.type !== 'PHONE'; });
    html += '<div class="rule fb-actions">' +
      (wa ? '<a class="btn btn-primary btn-block" href="' + href(wa) + '" target="_blank" rel="noopener">' + M.icon('message-circle') + sp.types.WHATSAPP + ' <span class="num">' + M.ltr(wa.value) + '</span></a>' : '') +
      (ph ? '<a class="btn btn-secondary btn-block" href="' + href(ph) + '">' + M.icon('phone') + sp.call + '</a>' : '') +
      '<a class="btn btn-secondary btn-block" href="https://www.google.com/maps/dir/?api=1&amp;destination=' + s.loc.lat + ',' + s.loc.lng + '" target="_blank" rel="noopener">' + M.icon('navigation') + sp.directions + '</a>' +
      (others.length ? '<p class="fb-links">' + others.map(function (c) { return '<a href="' + M.esc(href(c)) + '" target="_blank" rel="noopener">' + (sp.types[c.type] || sp.types.OTHER) + '</a>'; }).join('') + '</p>' : '') +
      (!wa && !ph && !others.length ? '<p class="sub">' + sp.noContacts + '</p>' : '') +
      (s.updatedAt.contacts ? '<p class="sub">' + sp.updated.contacts + M.esc(t.ago(s.updatedAt.contacts)) + '</p>' : '') + '</div>';
    return html + '</section>';
  }

  function spread(s) {
    var t = M.t().sp, nm = M.name(s), ph = s.photos;
    var fig = function (p, i, cls) {
      return '<figure class="plate ' + (p.real ? 'real' : 'poster') + ' ' + (cls || '') + '"' + (cls === 'big' ? ' style="--ar:' + Math.max(4 / 3, Math.min(21 / 9, p.w / p.h)).toFixed(3) + '"' : '') + '><a class="frame" href="' + M.photo(p.page) + '" aria-label="' + M.esc(M.lang === 'ar' ? 'الصورة ' + (i + 1) + ' من ' + ph.length + ' — ' + nm : 'Photo ' + (i + 1) + ' of ' + ph.length + ' — ' + nm) + '">' +
        '<img src="' + M.photo(i === 0 && ph.length > 1 ? p.page : p.page) + '" alt="" width="' + p.w + '" height="' + p.h + '"' + (i ? ' loading="lazy"' : '') + '></a><figcaption>' + M.esc(nm) + ' · ' + t.photoFrom + '</figcaption></figure>';
    };
    if (ph.length > 1) return '<div class="spread" role="group" aria-label="' + M.esc(t.photos(nm)) + '">' + fig(ph[0], 0, 'big') + '<div class="side">' + ph.slice(1).map(function (p, i) { return fig(p, i + 1); }).join('') + '</div></div>';
    if (ph.length === 1 && ph[0].real) return '<div class="spread one">' + fig(ph[0], 0, 'big') + '</div>';
    return '';
  }

  M.boot({
    id: 'space',
    title: function () { var s = M.bySlug(slug); return s ? M.name(s) : M.t().sp.notFound; },
    render: function () {
      var t = M.t(), sp = t.sp, s = M.bySlug(slug), main = document.getElementById('main');
      if (!s) { main.innerHTML = '<div class="wrap page-head"><h1 class="t-h1">' + sp.notFound + '</h1><p class="t-stand">' + sp.notFoundText + '</p><p style="margin-top:24px"><a class="btn btn-primary" href="spaces.html">' + sp.back + '</a></p></div>'; return; }
      var nm = M.esc(M.name(s)), other = M.otherName(s), stt = M.state(s), g = M.govOf(s);
      var saved = M.signedIn && M.favs().indexOf(s.slug) >= 0;
      var poster = s.photos.length === 1 && !s.photos[0].real ? s.photos[0] : null;
      var html = '<div class="wrap">' +
        '<nav class="crumbs" aria-label="' + sp.breadcrumb + '"><ol><li><a href="home.html">' + t.links.home + '</a></li><li>' + M.icon('chevron-right', 'dir') + '<a href="spaces.html">' + t.links.spaces + '</a></li><li>' + M.icon('chevron-right', 'dir') + '<a href="spaces.html?area=' + s.areaId + '">' + M.esc(M.areaName(s)) + '</a></li><li>' + M.icon('chevron-right', 'dir') + '<span aria-current="page">' + nm + '</span></li></ol></nav>' +
        '<header class="sp-head"><div class="sp-title"><h1 class="t-h1">' + nm + '</h1><button class="btn btn-icon heart" type="button" data-heart="' + s.slug + '" aria-pressed="' + saved + '" aria-label="' + M.esc(saved ? sp.remove(M.name(s)) : sp.save(M.name(s))) + '">' + M.icon('heart') + '</button></div>' +
        (other ? '<p class="other-name t-fact"><bdi lang="' + (M.lang === 'ar' ? 'en' : 'ar') + '">' + M.esc(other) + '</bdi> · ' + M.esc(M.gname(g)) + '</p>' : '') +
        '<p class="t-stand standfirst">' + M.mark(stt) + M.sentence(s) + '</p></header>' +
        '<div class="g sp-body"><aside class="g-start sp-aside"><div class="sticky-box">' + factBox(s) +
        (poster ? '<figure class="plate poster aside-plate"><a class="frame" href="' + M.photo(poster.page) + '" aria-label="' + M.esc(sp.photos(M.name(s))) + '"><img src="' + M.photo(poster.card) + '" alt="" width="640" height="360"></a><figcaption>' + nm + ' · ' + sp.photoFrom + '</figcaption></figure>' : '') +
        '</div></aside><div class="g-main sp-main">' + spread(s);
      if (!s.verified) html += '<div class="note-quiet"><p>' + sp.unverified(M.esc(t.ago(s.updatedAt.profile))) + '</p><button class="link" type="button" id="run-it">' + sp.runIt + '</button></div>';
      if (s.announce) html += '<section class="announce" aria-labelledby="ann-h"><h2 class="t-meta" id="ann-h">' + sp.announcement + '</h2><p class="t-lede">' + sp.demoAnnounce + '</p></section>';
      /* prices */
      var gen = s.prices.filter(function (p) { return p.audience === 'GENERAL'; }), stu = s.prices.filter(function (p) { return p.audience === 'STUDENT'; });
      var rows = M.periodOrder.filter(function (p) { return s.prices.some(function (x) { return x.period === p; }); }).map(function (p) {
        var gp = gen.filter(function (x) { return x.period === p; })[0], sp2 = stu.filter(function (x) { return x.period === p; })[0];
        return '<tr><th scope="row">' + sp.periods[p] + '</th><td class="price">' + (gp ? M.ltr(M.money(gp.amount)) : '—') + '</td>' + (stu.length ? '<td class="price">' + (sp2 ? M.ltr(M.money(sp2.amount)) : '—') + '</td>' : '') + '</tr>';
      }).join('');
      html += '<section class="section" aria-labelledby="pr-h"><div class="section-head"><h2 class="t-h2" id="pr-h">' + sp.prices + '</h2>' + upd(s, 'prices') + '</div>' +
        (rows ? '<table class="tbl"><thead><tr><th scope="col">' + sp.subscription + '</th><th scope="col">' + sp.price + '</th>' + (stu.length ? '<th scope="col">' + sp.students + '</th>' : '') + '</tr></thead><tbody>' + rows + '</tbody></table><p class="t-meta">' + sp.displayOnly + '. ' + sp.check + '</p>'
          : '<p class="t-body muted">' + sp.noPrices + '</p>') + '</section>';
      html += '<section class="section" aria-labelledby="am-h"><div class="section-head"><h2 class="t-h2" id="am-h">' + sp.amenities + '</h2>' + upd(s, 'amenities') + '</div>' +
        (s.amenities.length ? '<ul class="words">' + s.amenities.map(function (a) { return '<li>' + M.esc(a[M.lang]) + '</li>'; }).join('') + '</ul>' : '<p class="t-body muted">' + sp.noAmenities + '</p>') + '</section>';
      var desc = M.lang === 'ar' ? (s.descAr || s.descEn) : (s.descEn || s.descAr);
      if (desc) html += '<section class="section" aria-labelledby="ab-h"><div class="section-head"><h2 class="t-h2" id="ab-h">' + sp.about + '</h2>' + upd(s, 'profile') + '</div>' +
        '<blockquote class="their-words"><p class="t-meta">' + sp.inTheirWords + '</p><p class="words-text" dir="auto">' + M.esc(desc.trim()) + '</p></blockquote></section>';
      var addr = M.lang === 'ar' ? (s.addrAr || s.addrEn) : (s.addrEn || s.addrAr);
      html += '<section class="section" aria-labelledby="lo-h"><div class="section-head"><h2 class="t-h2" id="lo-h">' + sp.location + '</h2></div>' +
        '<div class="loc"><div class="map-frame loc-map" id="loc-map" role="img" aria-label="' + M.esc(sp.mapOf(M.name(s))) + '"></div><div class="loc-text">' +
        (addr ? '<p class="t-body" dir="auto">' + M.esc(addr) + '</p>' : '') + '<p class="t-meta">' + M.esc(M.areaName(s)) + ' · ' + M.esc(M.gname(g)) + '</p>' +
        '<a class="btn btn-secondary" href="https://www.google.com/maps/dir/?api=1&amp;destination=' + s.loc.lat + ',' + s.loc.lng + '" target="_blank" rel="noopener">' + M.icon('navigation') + sp.directions + '</a></div></div></section>';
      html += '<p class="report"><button class="link t-fact" type="button" id="report">' + sp.report + '</button></p>';
      html += '</div></div></div>';
      var wa = s.contacts.filter(function (c) { return c.type === 'WHATSAPP'; })[0], ph = s.contacts.filter(function (c) { return c.type === 'PHONE'; })[0];
      if (wa || ph) html += '<div class="sp-bar" role="region" aria-label="' + sp.bar + '">' + (wa ? '<a class="btn btn-primary" href="' + href(wa) + '" target="_blank" rel="noopener">' + M.icon('message-circle') + sp.types.WHATSAPP + '</a>' : '') + (ph ? '<a class="btn btn-secondary" href="' + href(ph) + '">' + M.icon('phone') + sp.call + '</a>' : '') + '</div>';
      main.innerHTML = html;
      document.body.classList.toggle('has-bar', !!(wa || ph));
      new GuideMap(document.getElementById('loc-map'), { spaces: [s], selected: s.slug, static: true, focusLoc: s.loc });
      var r = document.getElementById('run-it'); if (r) r.addEventListener('click', function () { M.contactDialog(sp.dialogTitle, sp.dialogText); });
      document.getElementById('report').addEventListener('click', function () { if (M.signedIn) location.href = 'login.html'; else M.signInPrompt('report'); });
    }
  });
})();
