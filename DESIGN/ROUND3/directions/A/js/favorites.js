/* المفضّلة: the saved spaces as board rows with their state now; one that left the directory as a muted row. */
(function () {
  'use strict';
  var saved = ['branch-hub', 'focus-hub', 'coma-io', 'masahat', 'pal-hub'];
  var goneKept = true, near = false;
  /* Masahat is shown with its photo removed: the no-photo state (COMMON §2). */
  var NO_PHOTO = { masahat: true };

  function tabs() {
    var w = A.t().acc;
    return '<nav class="tabs" aria-label="' + w.nav + '"><a href="' + A.href('favorites.html') + '" aria-current="page">' + w.favorites + '</a>' +
      '<a href="#" data-act="notbuilt">' + w.reports + '</a><a href="' + A.href('account.html') + '">' + w.settings + '</a></nav>';
  }

  A.page({
    nav: '', signedIn: true,
    title: function () { return A.t().fav.title; },
    render: function () {
      var w = A.t(), f = w.fav, g = A.gaza();
      var list = saved.map(A.bySlug).filter(Boolean);
      if (near) list.sort(function (a, b) { return A.km(A.NEAR_POINT, a.location) - A.km(A.NEAR_POINT, b.location); });
      var n = list.length + (goneKept ? 1 : 0);
      var rows = list.map(function (s) { return A.row(s, { g: g, saved: true, noPhoto: NO_PHOTO[s.slug], near: near ? A.NEAR_POINT : null }); }).join('');
      if (goneKept) {
        var gname = A.state.lang === 'ar' ? 'نور هب' : 'Noor Hub';
        rows += '<li class="row gone"><span class="bar k-none"></span><span class="plate initial" aria-hidden="true">' + Array.from(gname)[0] + '</span>' +
          '<div class="row__main"><span class="row__name">' + gname + '</span><span class="row__area">' + f.gone + '</span></div>' +
          '<button type="button" class="btn btn-secondary" data-gone>' + f.removeBtn + '</button></li>';
      }
      var body = n
        ? '<ul class="rows" aria-label="' + f.region + '">' + A.rowsHead() + rows + '</ul>'
        : '<div class="rows empty"><h2 class="t-h2">' + f.emptyTitle + '</h2><p>' + f.emptyText + '</p><a class="btn btn-secondary" href="' + A.href('spaces.html') + '">' + w.browseSpaces + '</a></div>';
      return '<div class="wrap page-head"><h1 class="t-h1">' + f.title + '</h1><p class="c2">' + f.description + '</p></div>' +
        '<div class="wrap">' + tabs() +
        '<div class="results__bar" style="margin-block:24px 16px"><p class="count" aria-live="polite">' + f.count(n) + '</p>' +
        '<button type="button" class="btn btn-secondary" data-near aria-pressed="' + near + '">' + A.icon('locate-fixed') + w.dir.near.button + '</button></div>' +
        (near ? '<div class="near-line" role="status"><span>' + w.dir.near.sorted + ' ' + w.dir.near.approx + '</span></div>' : '') +
        body + '</div>';
    },
    mount: function () {
      var f = A.t().fav;
      document.querySelectorAll('[data-heart]').forEach(function (b) {
        b.onclick = function () {
          var slug = b.getAttribute('data-heart'), idx = saved.indexOf(slug), s = A.bySlug(slug);
          saved.splice(idx, 1); A.render();
          A.toast(f.removed + ' · ' + A.esc(A.nm(s)), { label: f.undo, run: function () { saved.splice(idx, 0, slug); A.render(); A.toast(f.added); } });
          var c = document.querySelector('.count'); if (c) c.setAttribute('tabindex', '-1'), c.focus();
        };
      });
      var gb = document.querySelector('[data-gone]');
      if (gb) gb.onclick = function () { goneKept = false; A.render(); A.toast(f.removedLeft(A.state.lang === 'ar' ? 'نور هب' : 'Noor Hub')); };
      var nb = document.querySelector('[data-near]');
      if (nb) nb.onclick = function () { near = !near; A.render(); document.querySelector('[data-near]').focus(); };
    }
  });
})();
