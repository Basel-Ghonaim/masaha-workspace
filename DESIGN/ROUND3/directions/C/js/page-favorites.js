/* «المفضّلة» — the same entries as the directory, with their state now; Masahat shown without its photo (the
   no-photo state: no frame at all); «نور هب» left the directory and stays as a muted entry. */
(function () {
  var near = false;
  var GONE = { slug: 'noor-hub', nameAr: 'نور هب', nameEn: 'Noor Hub' };
  function draw() {
    var t = M.t(), f = t.fav, favs = M.favs();
    var list = M.spaces().filter(function (s) { return favs.indexOf(s.slug) >= 0; });
    if (near) { list.forEach(function (s) { s._km = M.km(M.HERE, s.loc); }); list.sort(function (a, b) { return a._km - b._km; }); }
    else list.sort(function (a, b) { return favs.indexOf(a.slug) - favs.indexOf(b.slug); });
    var gone = favs.indexOf(GONE.slug) >= 0;
    var n = list.length + (gone ? 1 : 0);
    document.getElementById('fav-count').textContent = f.count(n);
    var nb = document.getElementById('fav-near'); nb.setAttribute('aria-pressed', String(near));
    document.getElementById('fav-near-line').hidden = !near;
    var html = list.map(function (s) { return '<li>' + M.entry(s, { h: 'h2', remove: true, noPhoto: s.slug === 'masahat', km: near ? s._km : null }) + '</li>'; }).join('');
    if (gone) html += '<li><article class="entry gone"><div class="body"><div class="name-row"><h2 class="t-entry">' + M.esc(M.lang === 'ar' ? GONE.nameAr : GONE.nameEn) + '</h2>' +
      '<div class="entry-actions"><button class="btn btn-quiet" type="button" data-remove="' + GONE.slug + '" aria-label="' + M.esc(f.removeName(M.lang === 'ar' ? GONE.nameAr : GONE.nameEn)) + '">' + f.remove + '</button></div></div>' +
      '<p class="t-fact muted">' + f.gone + '</p></div></article></li>';
    document.getElementById('fav-list').innerHTML = n ? '<ul class="entries">' + html + '</ul>' :
      '<div class="empty"><h2 class="t-h2">' + f.empty + '</h2><p class="t-body">' + f.emptyText + '</p><a class="btn btn-secondary" href="spaces.html">' + t.browse + '</a></div>';
  }
  M.boot({
    id: 'favorites', signedIn: true,
    title: function () { return M.t().fav.title; },
    render: function () {
      var t = M.t(), f = t.fav, d = t.dir;
      document.getElementById('main').innerHTML = '<div class="wrap">' +
        '<header class="page-head g"><div class="g-start"></div><div class="g-main"><h1 class="t-h1">' + f.title + '</h1><p class="t-stand">' + f.description + '</p>' +
        '<div class="fav-tools"><p class="t-fact muted" id="fav-count"></p><button class="btn btn-secondary" type="button" id="fav-near" aria-pressed="false">' + M.icon('locate-fixed') + d.near + '</button></div>' +
        '<p class="near-line t-fact" id="fav-near-line" hidden><span class="mark live" aria-hidden="true"></span>' + d.sortedNear + ' ' + d.approx + ' <span class="muted">' + d.nearDemo + '</span></p></div></header>' +
        '<div class="g" style="margin-top:48px"><div class="g-start">' + M.accountNav('favorites') + '</div><div class="g-main" id="fav-list" role="region" aria-label="' + f.region + '"></div></div></div>';
      draw();
    }
  });
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-remove]');
    if (b) {
      var slug = b.getAttribute('data-remove'), favs = M.favs(), i = favs.indexOf(slug);
      favs.splice(i, 1); M.setFavs(favs); draw();
      M.toast(M.t().fav.removed, function () { var f2 = M.favs(); f2.splice(i, 0, slug); M.setFavs(f2); draw(); });
      return;
    }
    if (e.target.closest('#fav-near')) { near = !near; draw(); }
  });
})();
