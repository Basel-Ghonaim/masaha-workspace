/* About — an essay: the intro as a standfirst, the sections' headings in the start column. */
M.boot({
  id: 'about',
  title: function () { return M.t().links.about; },
  render: function () {
    var t = M.t(), a = t.about, st = t.st, c = M.contact;
    var sec = function (id, title, body) { return '<section class="chapter g" aria-labelledby="' + id + '-h" id="' + id + '"><div class="g-start"><h2 class="t-h2" id="' + id + '-h">' + title + '</h2></div><div class="g-main">' + body + '</div></section>'; };
    var row = function (mark, term, text) { return '<div class="row"><dt><span class="mark ' + mark + ' big" aria-hidden="true"></span>' + term + '</dt><dd>' + text + '</dd></div>'; };
    var html = '<div class="wrap">' +
      '<header class="page-head about-head g"><div class="g-start"></div><div class="g-main"><h1 class="t-h1">' + t.links.about + '</h1><p class="t-stand">' + a.intro + '</p><p class="t-body">' + a.audience + '</p></div></header>';
    html += sec('source', a.source,
      '<div class="defs"><div class="def"><h3>' + a.verified + '</h3><p class="t-meta">' + a.verifiedSub + '</p><p class="t-body">' + a.verifiedText + '</p></div>' +
      '<div class="def"><h3>' + a.unverified + '</h3><p class="t-meta">' + a.unverifiedSub + '</p><p class="t-body">' + a.unverifiedText + '</p></div></div>' +
      '<p class="t-body" style="margin-top:32px">' + a.note + ' ' + a.wrong + ' <a href="#contact">' + a.wrongLink + '</a>' + a.wrongEnd + '</p>');
    html += sec('status', a.status,
      '<div class="states"><p class="grp">' + a.liveGroup + '</p><dl>' + row('live', st.available, a.available) + row('full', st.full, a.full) + row('closed', st.closedNow, a.closed) +
      '</dl><p class="grp">' + a.hoursGroup + '</p><dl>' + row('byhours', a.byHoursTerm, a.byHours) + row('none', st.none, a.none) + '</dl></div>');
    html += sec('contact', a.contact,
      '<p class="t-stand">' + a.contactText + '</p><div class="contact-acts">' +
      '<a class="btn btn-primary" href="https://wa.me/' + c.whatsapp.replace('+', '') + '" target="_blank" rel="noopener">' + M.icon('message-circle') + t.whatsapp + ' <span class="num">' + M.ltr(c.whatsapp) + '</span></a>' +
      '<a class="btn btn-secondary" href="mailto:' + c.email + '">' + M.icon('mail') + M.ltr(c.email) + '</a></div>');
    html += sec('owners', a.owners, '<ol class="steps">' + a.steps.map(function (s, i) { return '<li><span class="n" aria-hidden="true">' + (i + 1) + '</span><p>' + s + '</p></li>'; }).join('') + '</ol>');
    html += '</div>';
    document.getElementById('main').innerHTML = html;
  }
});
