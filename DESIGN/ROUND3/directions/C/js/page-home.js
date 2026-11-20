/* Home — the cover, «مفتوحة الآن», the chapters, for owners. */
M.boot({
  id: 'home',
  title: function () { return M.t().links.home; },
  render: function () {
    var t = M.t(), h = t.home, all = M.spaces(), n = M.now();
    var open = all.filter(M.isOpenNow);
    var rank = function (s) { var k = M.state(s).kind; return k === 'available' ? 0 : k === 'open' ? 1 : k === 'full' ? 2 : 3; };
    var byNews = function (a, b) { return (b.latest || '').localeCompare(a.latest || ''); };
    open.sort(function (a, b) { return rank(a) - rank(b) || byNews(a, b); });

    var html = '<div class="wrap">';
    /* (1) the cover */
    html += '<section class="cover" aria-labelledby="cover-h"><h1 id="cover-h" class="t-display">' + h.title + '</h1>' +
      '<div class="g"><div class="g-start dateline"><p class="clock">' + t.days[n.day] + ' · <strong>' + M.ltr(n.hhmm) + '</strong> ' + h.gazaTime + '</p>' +
      '<p class="openrow">' + (open.length ? '<span class="mark live" aria-hidden="true"></span>' : '<span class="mark closed" aria-hidden="true"></span>') + '<a class="openline" href="spaces.html?open=1">' + h.openOf(open.length, all.length) + '</a></p></div>' +
      '<div class="g-main"><p class="t-stand">' + h.lead + '</p>' +
      '<form class="search" action="spaces.html" method="get" role="search"><label class="vh" for="home-q">' + h.searchLabel + '</label>' +
      '<div class="field-wrap">' + M.icon('search') + '<input class="input" id="home-q" name="q" type="search" placeholder="' + h.searchPh + '" autocomplete="off"></div>' +
      '<button class="btn btn-primary" type="submit">' + h.searchSubmit + '</button></form></div></div></section>';

    /* (2) open now — or, when nothing is, what opens next */
    var list = open.slice(0, 4), title = h.openNow, empty = '';
    if (!open.length) {
      var nx = all.filter(function (s) { return s.days; }).map(function (s) { var o = M.nextOpen(s); return { s: s, k: o ? o.k * 1440 + (s.days[o.day].opensMinute) : 1e9 }; });
      nx.sort(function (a, b) { return a.k - b.k; });
      list = nx.slice(0, 4).map(function (x) { return x.s; }); title = h.openingNext;
      empty = '<div class="note-quiet" style="margin-bottom:24px"><p class="t-fact"><strong>' + h.empty.title + '</strong></p><p class="t-fact muted">' + h.empty.text + '</p></div>';
    }
    html += '<section class="chapter g" aria-labelledby="open-h"><div class="g-start chapter-head"><h2 id="open-h" class="t-h2">' + title + '</h2>' +
      '<a class="more t-fact" href="spaces.html' + (open.length ? '?open=1' : '') + '">' + (open.length ? h.viewAll : h.empty.action) + '</a></div>' +
      '<div class="g-main">' + empty + '<ul class="entries pair">' + list.map(function (s) { return '<li>' + M.entry(s) + '</li>'; }).join('') + '</ul></div></section>';

    /* (3) the chapters: the guide's contents */
    var rows = M.govs.map(function (g) {
      var sp = all.filter(function (s) { return M.govOf(s).id === g.id; });
      if (!sp.length) return '';
      var openN = sp.filter(M.isOpenNow).length;
      var areas = g.areas.map(function (a) { var c = sp.filter(function (s) { return s.areaId === a.id; }).length; return c ? '<li><a href="spaces.html?area=' + a.id + '"><span class="nm">' + M.esc(M.aname(a)) + '</span><span class="lead" aria-hidden="true"></span><span class="ct">' + t.count(c) + '</span></a></li>' : ''; }).join('');
      return '<div class="g gov-row"><div class="g-start"><h3 class="gname">' + (openN ? '<span class="mark live" aria-hidden="true"></span>' : '') + M.esc(M.gname(g)) + '</h3>' +
        '<p class="sub">' + t.count(sp.length) + (openN ? ' · ' + h.chapterOpen(openN) : '') + '</p></div><div class="g-main"><ul class="toc">' + areas + '</ul></div></div>';
    }).join('');
    html += '<section class="chapter" aria-labelledby="areas-h"><div class="g"><div class="g-start"><h2 id="areas-h" class="t-h2">' + h.areas + '</h2></div>' +
      '<div class="g-main"><ul class="toc"><li><a href="spaces.html"><span class="nm">' + h.all + '</span><span class="lead" aria-hidden="true"></span><span class="ct">' + h.strip + ' · ' + t.count(all.length) + '</span></a></li></ul></div></div>' + rows + '</section>';

    /* (4) for owners */
    html += '<section class="chapter g owners" aria-labelledby="own-h"><div class="g-start"><h2 id="own-h" class="t-h2">' + h.owners.title + '</h2></div>' +
      '<div class="g-main"><p class="t-stand">' + h.owners.text + '</p><button class="btn btn-secondary" type="button" id="own-btn">' + h.owners.action + '</button></div></section>';
    html += '</div>';
    document.getElementById('main').innerHTML = html;
    document.getElementById('own-btn').addEventListener('click', function () { M.contactDialog(t.about.owners, h.owners.text); });
  }
});
