/* 404: the board with one row — the page that isn't there — then what is open now, so the way back is content. */
(function () {
  'use strict';
  A.page({
    nav: '',
    title: function () { return A.t().nf.title; },
    render: function () {
      var w = A.t(), g = A.gaza(), all = A.allSpaces();
      var open = all.filter(function (s) { return A.statusOf(s, g).openNow; });
      var rows, head;
      if (open.length) { head = w.homeT.openNow; rows = open.map(function (s) { return A.row(s, { g: g }); }).join(''); }
      else {
        head = w.board.next;
        rows = all.map(function (s) { return { s: s, n: A.nextOpening(s, g) }; }).filter(function (x) { return x.n; }).sort(function (a, b) { return a.n.k - b.n.k || a.n.minute - b.n.minute; })
          .map(function (x) { return A.row(x.s, { g: g, next: x.n.text }); }).join('');
      }
      return '<section class="board ink nf" aria-labelledby="h1"><div class="wrap">' +
        '<div class="board__line"><div class="clock"><span class="t-board" data-clock>' + g.hhmm + '</span><span class="clock__label"><span>' + w.board.now + '</span><b>' + w.dayNames[g.dow] + '</b></span></div>' +
        '<div class="count-now' + (open.length ? '' : ' zero') + '"><span class="t-board" aria-hidden="true">' + open.length + '</span><span class="lbl" aria-hidden="true">' + w.homeT.openNow + '</span><span class="sr">' + w.board.openCount(open.length) + '</span></div></div>' +
        '<ul class="rows" style="border-block-end:0"><li class="row"><span class="bar k-none"></span><div class="row__main"><h1 class="t-display" id="h1">' + w.nf.title + '</h1>' +
        '<p class="c2" style="margin-block-start:8px;font-size:18px">' + w.nf.description + '</p><div class="acts"><a class="btn btn-primary" href="' + A.href('spaces.html') + '">' + w.browseSpaces + '</a>' +
        '<a class="btn btn-secondary" href="' + A.href('home.html') + '">' + w.nf.home + '</a></div></div></li></ul></div></section>' +
        '<section class="wrap section" aria-labelledby="open-h"><h2 class="t-h2" id="open-h">' + head + '</h2><ul class="rows" style="margin-block-start:16px">' + A.rowsHead() + rows + '</ul></section>';
    },
    mount: function () {
      document.querySelectorAll('[data-heart]').forEach(function (b) { b.onclick = function () { A.signInPrompt('favorite', b); }; });
    }
  });
})();
