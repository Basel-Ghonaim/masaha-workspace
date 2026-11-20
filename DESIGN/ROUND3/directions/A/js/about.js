/* About: what Masaha is, where its information comes from (verified · unverified), what the states
   mean (the real row marks on the board), how to reach us, and the owners' three steps. */
(function () {
  'use strict';
  A.page({
    nav: 'about',
    title: function () { return A.t().about; },
    render: function () {
      var w = A.t(), a = w.aboutT, st = w.st, c = window.MD.contact;
      var states = [['live', st.live, a.sAvailable], ['full', st.full, a.sFull], ['closed', st.closedLive, a.sClosed], ['hours', st.open + ' · ' + st.closedHours, w.page.byHours], ['none', st.none, a.sNone]];
      return '<div class="wrap page-head"><h1 class="t-display">' + w.about + '</h1>' +
        '<p class="prose" style="font-size:19px;line-height:1.7;margin-block-start:24px">' + a.intro + '</p><p class="prose c2" style="margin-block-start:16px">' + a.audience + '</p></div>' +
        '<section class="wrap section" aria-labelledby="src-h"><h2 class="t-h2" id="src-h">' + a.sourceTitle + '</h2>' +
        '<div class="cmp" style="margin-block-start:24px"><div><div class="mk"><span class="bar k-live" aria-hidden="true"></span><h3 class="t-row">' + a.vTitle + '</h3></div><p class="sub">' + a.vSub + '</p><p>' + a.vText + '</p></div>' +
        '<div><div class="mk"><span class="bar k-none" aria-hidden="true"></span><h3 class="t-row">' + a.uTitle + '</h3></div><p class="sub">' + a.uSub + '</p><p>' + a.uText + '</p></div></div>' +
        '<p class="prose c2" style="margin-block-start:24px">' + a.note + '</p><p class="prose c2" style="margin-block-start:8px">' + a.wrong + ' <a href="#contact">' + a.wrongLink + '</a>' + a.wrongEnd + '</p></section>' +
        '<section class="wrap section" aria-labelledby="st-h"><h2 class="t-h2" id="st-h">' + a.statusTitle + '</h2>' +
        '<div class="board ink" style="border-radius:12px;margin-block-start:24px;padding:8px 0"><ul class="rows states">' + states.map(function (s) {
          return '<li class="row"><span class="bar k-' + s[0] + '"></span><span class="state"><span class="dot k-' + s[0] + '"></span>' + s[1] + '</span><div class="row__main"><p>' + s[2] + '</p></div></li>';
        }).join('') + '</ul></div></section>' +
        '<section class="wrap section duo"><div id="contact" tabindex="-1"><h2 class="t-h2">' + a.contactTitle + '</h2><p class="c2" style="margin-block-start:8px;max-width:56ch">' + a.contactText + '</p>' +
        '<div class="contact-lines"><a href="https://wa.me/' + c.whatsapp.replace(/\D/g, '') + '" target="_blank" rel="noopener">' + A.icon('message-circle') + '<span class="k">' + a.whatsapp + '</span><span class="v">' + A.ltr(c.whatsapp) + '</span></a>' +
        '<a href="mailto:' + c.email + '">' + A.icon('mail') + '<span class="k">' + a.email + '</span><span class="v">' + A.ltr(c.email) + '</span></a></div></div>' +
        '<div><h2 class="t-h2">' + a.ownersTitle + '</h2><ol class="steps" style="margin-block-start:16px">' + a.steps.map(function (s) { return '<li><span>' + s + '</span></li>'; }).join('') + '</ol></div></section>';
    }
  });
})();
