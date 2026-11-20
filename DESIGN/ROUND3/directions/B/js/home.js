/* Home: the opening with the Strip; open now; the governorates north to south; for owners. */
(function () {
  'use strict';
  const { esc, ic, ltr, L, spaces, GOVS, govName, areaName, silhouette, stripMap, NOW, card, wireHearts, page, prefs, clock } = window.B;
  const wide = () => matchMedia('(min-width: 1024px)').matches;
  let map = null, lastWide = null;

  function counts(list) {
    const byGov = {}, byArea = {};
    list.forEach((s) => { byGov[s.govId] = (byGov[s.govId] || 0) + 1; byArea[s.areaId] = (byArea[s.areaId] || 0) + 1; });
    return { byGov, byArea };
  }

  page({
    key: 'home', nav: 'home', headerOnMap: true,
    bodyClass: () => 'ends-ink',
    title: (T) => T.site.links.home,
    main(T) {
      const list = spaces();
      const open = list.filter((s) => s.state.open);
      const { byGov, byArea } = counts(list);
      const day = new Intl.DateTimeFormat(prefs.lang === 'ar' ? 'ar-u-nu-latn' : 'en', { weekday: 'long', timeZone: 'Asia/Gaza' }).format(NOW.date);
      const govRows = GOVS.map((g) => {
        const n = byGov[g.id] || 0;
        const areas = g.areas.filter((a) => byArea[a.id]).map((a) => `<a href="spaces.html?area=${a.id}">${esc(areaName(a))}<span>${esc(T.home.count(byArea[a.id]))}</span></a>`).join('');
        return `<li class="gov-row">
          <span class="gthumb">${silhouette({ w: 72, h: 90, ink: g.id, pad: 1, dw: '100%', dh: '100%' })}</span>
          <div><h3 class="t-h2"><a href="spaces.html?gov=${g.id}">${esc(govName(g))}</a></h3><p class="gcount">${esc(T.home.count(n))}</p></div>
          <div class="gov-areas">${areas}</div>
        </li>`;
      }).join('');
      const openCards = open.map((s) => card(s, { level: 3 })).join('');
      const openBlock = open.length
        ? `<div class="rowscroll" id="openRow" tabindex="-1">${openCards}</div>`
        : `<div class="empty-line"><h3>${esc(T.home.empty.title)}</h3><p class="muted">${esc(T.home.empty.text)}</p><a class="btn btn-secondary" href="spaces.html">${esc(T.home.empty.action)}</a></div>`;
      return `
      <section class="home-open" aria-labelledby="h1">
        <div class="home-map" id="homeMap"></div>
        <div class="wrap home-hero">
          <div class="hero-text">
            <h1 class="t-display" id="h1">${esc(T.home.title)}</h1>
            <p class="lead">${esc(T.home.lead)}</p>
            <form class="hero-search" action="spaces.html" method="get" role="search">
              <label class="vh" for="q">${esc(T.home.search.label)}</label>
              <div class="row"><div class="input-wrap">${ic('search')}<input class="input has-ico" id="q" name="q" type="search" placeholder="${esc(T.home.search.placeholder)}" autocomplete="off"></div>
              <button class="btn btn-primary" type="submit">${esc(T.home.search.submit)}</button></div>
            </form>
            <div class="hero-alt">
              <a class="btn btn-secondary" href="spaces.html?near=1">${ic('locate-fixed')}${esc(T.dir.near.button)}</a>
              <p class="clock"><span class="dot k-${open.length ? 'open' : 'shut'}" aria-hidden="true"></span><span class="when">${T.home.clock(esc(day), ltr(clock(NOW.minute)))}</span><a class="link" href="spaces.html?open=1">${esc(T.home.openCount(open.length))}</a></p>
            </div>
          </div>
          <div class="hero-strip" id="heroStrip"></div>
        </div>
      </section>
      <section class="wrap sec" aria-labelledby="open-h">
        <div class="sec-head"><div><h2 class="t-h2" id="open-h">${esc(T.home.openNow)}</h2></div>
          <div class="tools">${open.length > 2 ? `<button type="button" class="icon-btn bordered tablet-up" data-scroll="-1" aria-label="${esc(T.home.previous)}">${ic('chevron-left', 'dir')}</button><button type="button" class="icon-btn bordered tablet-up" data-scroll="1" aria-label="${esc(T.home.next)}">${ic('chevron-right', 'dir')}</button>` : ''}
          <a class="btn btn-quiet btn-sm" href="spaces.html?open=1">${esc(T.home.viewAll)}</a></div></div>
        ${openBlock}
      </section>
      <section class="wrap sec" aria-labelledby="gov-h">
        <div class="sec-head"><div><h2 class="t-h2" id="gov-h">${esc(T.home.areasTitle)}</h2></div><a class="btn btn-quiet btn-sm" href="spaces.html">${esc(T.home.all)}</a></div>
        <ul class="govs">${govRows}</ul>
      </section>
      <section class="owners" aria-labelledby="own-h"><div class="wrap owners-in">
        <div><h2 class="t-h2" id="own-h">${esc(T.home.owners.title)}</h2><p>${esc(T.home.owners.text)}</p></div>
        <a class="btn" href="about.html#owners">${esc(T.home.owners.action)}</a>
      </div></section>`;
    },
    mount(root, T) {
      const list = spaces();
      wireHearts(root);
      const { byGov } = counts(list);
      const pins = list.map((s) => ({ slug: s.slug, name: s.name, areaId: s.areaId, lat: s.location.lat, lng: s.location.lng, kind: s.state.kind }));
      if (map) map.destroy();
      lastWide = wide();
      const heroStrip = root.querySelector('#heroStrip');
      if (lastWide) {
        const el = root.querySelector('#homeMap');
        map = stripMap(el, {
          mode: 'mark', pins, labels: 'callout', counts: byGov, inset: true, draw: true, pinR: 6.5,
          box(w, h) {
            const r = heroStrip.getBoundingClientRect(), o = el.getBoundingClientRect();
            const x = r.left - o.left, top = 72;
            return [x, top, r.width - 170, h - top - 8];
          },
          insetAt(v, R) { const [x, y] = window.B.P(v, 31.585, 34.33); return [x - R * 0.35, Math.max(y + R * 0.2, 72 + R + 24)]; },
        });
      } else {
        map = stripMap(heroStrip, {
          mode: 'mark', pins, labels: 'callout', counts: byGov, inset: true, draw: true, pinR: 5, calloutGap: 20,
          box(w, h) { return [8, 8, w - 150, h - 16]; },
          insetAt(v, R) { const [x, y] = window.B.P(v, 31.59, 34.30); return [x, y + R * 0.4]; },
          insetZoom: 4.6,
        });
      }
      root.querySelectorAll('[data-scroll]').forEach((b) => b.addEventListener('click', () => {
        const row = root.querySelector('#openRow'); if (!row) return;
        const step = row.firstElementChild ? row.firstElementChild.getBoundingClientRect().width + 32 : 300;
        const dirSign = document.documentElement.dir === 'rtl' ? -1 : 1;
        row.scrollBy({ left: +b.dataset.scroll * step * dirSign, behavior: 'smooth' });
      }));
    },
  });
  window.addEventListener('resize', () => { if (lastWide !== null && wide() !== lastWide) { lastWide = wide(); window.B.setLang(prefs.lang); } });
})();
