/* Sign in: the form at the start; beside it (≥ 1024) the board, live — what is open in Gaza now. */
(function () {
  'use strict';
  var showPw = false, errs = {};

  function boardPanel() {
    var w = A.t(), g = A.gaza(), all = A.allSpaces();
    var open = all.filter(function (s) { return A.statusOf(s, g).openNow; });
    var rows, head;
    if (open.length) { head = w.homeT.openNow; rows = open.slice(0, 6).map(function (s) { return A.row(s, { g: g, save: false }); }).join(''); }
    else {
      head = w.board.next;
      rows = all.map(function (s) { return { s: s, n: A.nextOpening(s, g) }; }).filter(function (x) { return x.n; }).sort(function (a, b) { return a.n.k - b.n.k || a.n.minute - b.n.minute; }).slice(0, 6)
        .map(function (x) { return A.row(x.s, { g: g, save: false, next: x.n.text }); }).join('');
    }
    return '<section class="auth-board board ink" aria-labelledby="ab-h"><div class="board__line">' +
      '<div class="clock"><span class="t-board" data-clock>' + g.hhmm + '</span><span class="clock__label"><span>' + w.board.now + '</span><b>' + w.dayNames[g.dow] + '</b></span></div>' +
      '<div class="count-now' + (open.length ? '' : ' zero') + '"><span class="t-board" aria-hidden="true">' + open.length + '</span><span class="lbl" aria-hidden="true">' + w.homeT.openNow + '</span><span class="sr">' + w.board.openCount(open.length) + '</span></div></div>' +
      '<h2 class="sr" id="ab-h">' + head + '</h2><ul class="rows">' + A.rowsHead() + rows + '</ul>' +
      '<div class="foot"><a class="inline-link" href="' + A.href('spaces.html') + '">' + w.browseSpaces + '</a></div></section>';
  }

  A.page({
    nav: '',
    title: function () { return A.t().auth.title; },
    render: function () {
      var w = A.t(), a = w.auth, g = A.gaza();
      var n = A.allSpaces().filter(function (s) { return A.statusOf(s, g).openNow; }).length;
      return '<div class="strip ink board"><div class="wrap"><span>' + w.board.now + ' · ' + w.dayNames[g.dow] + '</span><span><span class="t" data-clock>' + g.hhmm + '</span> · ' + w.board.openCount(n) + '</span></div></div>' +
        '<div class="wrap auth"><div class="auth-form"><h1 class="t-h1">' + a.title + '</h1><p class="c2" style="margin-block:8px 32px">' + a.description + '</p>' +
        '<form id="signin" novalidate>' +
        '<button type="button" class="btn btn-secondary btn-block gbtn" data-google>' + a.google + '</button>' +
        '<p class="or">' + a.or + '</p>' +
        '<div class="field"><label for="em">' + a.email + '</label><input class="input" id="em" type="email" autocomplete="email" dir="ltr" placeholder="name@example.com"' + (errs.email ? ' aria-invalid="true" aria-describedby="em-e"' : '') + '>' + (errs.email ? '<p class="err" id="em-e">' + a.emailInvalid + '</p>' : '') + '</div>' +
        '<div class="field"><div style="display:flex;justify-content:space-between;align-items:baseline;gap:8px"><label for="pw">' + a.password + '</label><a class="inline-link t-sec" href="#" data-act="notbuilt">' + a.forgot + '</a></div>' +
        '<div class="with-end"><input class="input" id="pw" type="' + (showPw ? 'text' : 'password') + '" autocomplete="current-password" dir="ltr"' + (errs.pw ? ' aria-invalid="true" aria-describedby="pw-e"' : '') + '>' +
        '<button type="button" class="btn btn-icon end" data-showpw aria-pressed="' + showPw + '" aria-label="' + (showPw ? a.hide : a.show) + '">' + A.icon(showPw ? 'eye-off' : 'eye') + '</button></div>' +
        (errs.pw ? '<p class="err" id="pw-e">' + a.passwordEmpty + '</p>' : '') + '</div>' +
        '<button type="submit" class="btn btn-primary btn-block">' + a.submit + '</button>' +
        '<p class="alt">' + a.noAccount + ' <a class="inline-link" href="#" data-act="notbuilt">' + a.create + '</a></p>' +
        '</form></div>' + boardPanel() + '</div>';
    },
    mount: function () {
      var f = document.getElementById('signin');
      document.querySelector('[data-showpw]').onclick = function () {
        var pw = document.getElementById('pw'); showPw = !showPw; pw.type = showPw ? 'text' : 'password';
        this.setAttribute('aria-pressed', String(showPw)); this.setAttribute('aria-label', showPw ? A.t().auth.hide : A.t().auth.show); this.innerHTML = A.icon(showPw ? 'eye-off' : 'eye');
      };
      document.getElementById('em').addEventListener('blur', function () {
        var v = this.value.trim(); var bad = v && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
        if (!!bad !== !!errs.email) { errs.email = bad; var val = this.value; A.render(); var e = document.getElementById('em'); e.value = val; }
      });
      document.getElementById('em').addEventListener('input', function () { if (errs.email) { errs.email = false; this.removeAttribute('aria-invalid'); var e = document.getElementById('em-e'); if (e) e.remove(); } });
      document.querySelector('[data-google]').onclick = function () { location.href = A.href('favorites.html'); };
      f.onsubmit = function (e) {
        e.preventDefault();
        var em = document.getElementById('em').value.trim(), pw = document.getElementById('pw').value;
        errs = { email: !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em), pw: !pw };
        if (errs.email || errs.pw) { A.render(); document.getElementById('em').value = em; var first = document.querySelector('[aria-invalid="true"]'); if (first) first.focus(); return; }
        location.href = A.href('favorites.html');
      };
    }
  });
})();
