/* 404 — the display line, the sentence, and the guide's chapters as the way back. No icon. */
M.boot({
  id: '404',
  title: function () { return M.t().nf.title; },
  render: function () {
    var t = M.t(), all = M.spaces();
    var rows = M.govs.map(function (g) {
      var sp = all.filter(function (s) { return M.govOf(s).id === g.id; }); if (!sp.length) return '';
      var openN = sp.filter(M.isOpenNow).length;
      return '<li><a href="spaces.html?gov=' + g.id + '"><span class="nm">' + M.esc(M.gname(g)) + '</span><span class="lead" aria-hidden="true"></span>' +
        (openN ? '<span class="opn">' + t.home.chapterOpen(openN) + '</span>' : '') + '<span class="ct">' + t.count(sp.length) + '</span></a></li>';
    }).join('');
    document.getElementById('main').innerHTML = '<div class="wrap">' +
      '<header class="cover nf-head"><h1 class="t-display">' + t.nf.title + '</h1><div class="g"><div class="g-start">' + M.dateline() + '</div><div class="g-main"><p class="t-stand">' + t.nf.text + '</p></div></div></header>' +
      '<section class="chapter g" aria-labelledby="way-h"><div class="g-start"><h2 class="t-h2" id="way-h">' + t.nf.way + '</h2></div><div class="g-main"><ul class="toc">' +
      '<li><a href="spaces.html"><span class="nm">' + t.home.all + '</span><span class="lead" aria-hidden="true"></span><span class="ct">' + t.home.strip + ' · ' + t.count(all.length) + '</span></a></li>' + rows + '</ul>' +
      '<p style="margin-top:24px"><a class="btn btn-secondary" href="home.html">' + t.nf.home + '</a></p></div></section></div>';
  }
});
