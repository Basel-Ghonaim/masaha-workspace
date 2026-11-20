/* Home: the board leads (Gaza's time, what is open now), then the areas as an index, then the owners' line. */
(function () {
  'use strict';
  var near = false;

  function boardLine(g, openCount) {
    var w = A.t();
    return '<div class="board__line">' +
      '<div class="clock"><span class="t-board" data-clock>' + g.hhmm + '</span><span class="clock__label"><span>' + w.board.now + '</span><b>' + w.dayNames[g.dow] + '</b></span></div>' +
      '<div class="count-now' + (openCount ? '' : ' zero') + '"><span class="t-board" aria-hidden="true">' + openCount + '</span><span class="lbl" aria-hidden="true">' + w.homeT.openNow + '</span><span class="sr">' + w.board.openCount(openCount) + '</span></div>' +
      '<button type="button" class="btn btn-secondary near" data-near aria-pressed="' + near + '">' + A.icon('locate-fixed') + w.dir.near.button + '</button>' +
      '</div>';
  }

  function list(g) {
    var w = A.t(), all = A.allSpaces();
    var open = all.filter(function (s) { return A.statusOf(s, g).openNow; });
    var html = '';
    if (near) {
      var pts = all.slice().sort(function (a, b) { return A.km(A.NEAR_POINT, a.location) - A.km(A.NEAR_POINT, b.location); }).slice(0, 6);
      html = '<div class="sec-head"><h2 class="t-h2">' + w.homeT.nearest + '</h2></div>' +
        '<p class="t-sec c2" style="margin-block:8px 16px">' + w.dir.near.sorted + ' ' + w.dir.near.approx + ' <button type="button" class="btn btn-quiet" data-near style="text-decoration:underline">' + w.dir.near.stop + '</button></p>' +
        '<ul class="rows">' + A.rowsHead() + pts.map(function (s) { return A.row(s, { g: g, near: A.NEAR_POINT }); }).join('') + '</ul>';
    } else if (open.length) {
      html = '<div class="sec-head"><h2 class="t-h2">' + w.homeT.openNow + '</h2></div>' +
        '<ul class="rows" style="margin-block-start:16px">' + A.rowsHead() + open.map(function (s) { return A.row(s, { g: g }); }).join('') + '</ul>';
    } else {
      var next = all.map(function (s) { return { s: s, n: A.nextOpening(s, g) }; }).filter(function (x) { return x.n; })
        .sort(function (a, b) { return a.n.k - b.n.k || a.n.minute - b.n.minute; });
      html = '<div class="sec-head"><h2 class="t-h2">' + w.homeT.emptyTitle + '</h2></div><p class="c2" style="margin-block:8px 16px;max-width:60ch">' + w.homeT.emptyText + '</p>' +
        '<h3 class="t-sec w5 c2" style="margin-block:24px 8px">' + w.board.next + '</h3>' +
        '<ul class="rows">' + A.rowsHead() + next.map(function (x) { return A.row(x.s, { g: g, next: x.n.text }); }).join('') + '</ul>';
    }
    html += '<div class="board__foot"><span class="t-sec c2">' + w.dir.all(all.length) + '</span><a class="btn btn-primary" href="' + A.href('spaces.html') + '">' + (open.length || near ? w.homeT.viewAll : w.homeT.emptyAction) + '</a></div>';
    return { html: html, count: open.length };
  }

  function areas() {
    var w = A.t(), all = A.allSpaces(), cols = '';
    window.MD.governorates.forEach(function (g) {
      var items = g.areas.map(function (a) { return { a: a, n: all.filter(function (s) { return s.area.id === a.id; }).length }; }).filter(function (x) { return x.n; });
      if (!items.length) return;
      cols += '<div><h3>' + A.esc(A.L(g, 'name')) + '</h3><ul>' + items.map(function (x) {
        return '<li><a href="' + A.href('spaces.html', { area: x.a.id }) + '"><span class="an">' + A.esc(A.L(x.a, 'name')) + '</span><span class="ac">' + w.homeT.count(x.n) + '</span></a></li>';
      }).join('') + '</ul></div>';
    });
    return '<section class="wrap section" aria-labelledby="areas-h"><div class="sec-head"><h2 class="t-h2" id="areas-h">' + w.homeT.areas + '</h2>' +
      '<a class="inline-link w5" href="' + A.href('spaces.html') + '">' + w.homeT.allAreas + ' · ' + w.homeT.count(all.length) + '</a></div>' +
      '<div class="areas">' + cols + '</div></section>';
  }

  A.page({
    nav: 'home',
    title: function () { return A.t().home; },
    render: function () {
      var w = A.t(), g = A.gaza(), L = list(g);
      return '<section class="board ink" aria-labelledby="h1"><div class="wrap">' + boardLine(g, L.count) +
        '<div class="board__intro"><div><h1 class="t-display" id="h1">' + w.homeT.title + '</h1><p class="lead">' + w.homeT.lead + '</p></div>' +
        '<form action="spaces.html" method="get" role="search"><input type="hidden" name="lang" value="' + A.state.lang + '">' +
        '<label class="sr" for="q">' + w.homeT.searchLabel + '</label><div class="searchbar"><div class="with-icon">' + A.icon('search') +
        '<input class="input" id="q" name="q" type="search" placeholder="' + w.homeT.placeholder + '" autocomplete="off"></div>' +
        '<button class="btn btn-primary" type="submit">' + w.homeT.submit + '</button></div></form></div>' +
        '<div class="board__list" id="boardlist">' + L.html + '</div></div></section>' +
        areas() +
        '<section class="wrap section"><div class="owners"><div><h2 class="t-h2">' + w.homeT.ownersTitle + '</h2><p>' + w.homeT.ownersText + '</p></div>' +
        '<a class="btn btn-secondary" href="' + A.href('about.html') + '#contact">' + w.contact + '</a></div></section>';
    },
    mount: function () {
      document.querySelectorAll('[data-near]').forEach(function (b) {
        b.addEventListener('click', function () { near = !near; A.render(); var nb = document.querySelector('.board__line [data-near]'); if (nb) nb.focus(); });
      });
      document.querySelectorAll('[data-heart]').forEach(function (b) { b.addEventListener('click', function () { A.signInPrompt('favorite', b); }); });
      var f = document.querySelector('form[role="search"]');
      if (A.state.themePref !== 'system') { var h = document.createElement('input'); h.type = 'hidden'; h.name = 'theme'; h.value = A.state.themePref; f.appendChild(h); }
      if (A.state.demo) { var d = document.createElement('input'); d.type = 'hidden'; d.name = 'demo'; d.value = '1'; f.appendChild(d); }
    },
    tick: function (g) {
      var c = document.querySelector('.count-now .t-board');
      var n = A.allSpaces().filter(function (s) { return A.statusOf(s, g).openNow; }).length;
      if (c && c.textContent !== String(n)) A.render();
    }
  });
})();
