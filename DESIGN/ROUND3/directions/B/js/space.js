/* A space's page: photos (as the imagery rule says), the facts in the start column, the sticky place panel. */
(function () {
  'use strict';
  const B = window.B;
  const { esc, ic, ltr, L, spaces, card, page, prefs, price, clock, ago, NOW, stripMap, silhouette, dialog, signInPrompt, Q } = B;
  const REAL = new Set(['coma-io-1-card.webp', 'branch-hub-2-card.webp', 'branch-hub-3-card.webp']);
  const PERIODS = ['HOUR', 'DAY', 'WEEK', 'MONTH'];
  const WEEK = [['sat', 6], ['sun', 0], ['mon', 1], ['tue', 2], ['wed', 3], ['thu', 4], ['fri', 5]];
  const PLATFORM = { whatsapp: '+970597063545', email: 'masahatgaza@gmail.com' };
  const slug = Q.get('slug') || 'branch-hub';
  let allDays = false, mini = null, miniPhone = null;

  function weekRows(days, H) {
    const val = (r) => (r == null ? H.closed : (r.opensMinute === 0 && r.closesMinute === 1440 ? H.allDay : ltr(`${clock(r.opensMinute)}–${clock(r.closesMinute)}`)));
    if (allDays) return WEEK.map(([k, i]) => ({ label: H.dayNames[k], value: val(days[i]), today: i === NOW.day, closed: !days[i] }));
    const groups = [];
    WEEK.forEach(([k, i]) => {
      const v = val(days[i]); const last = groups[groups.length - 1];
      if (last && last.value === v) { last.keys.push(k); last.today = last.today || i === NOW.day; }
      else groups.push({ keys: [k], value: v, closed: !days[i], today: i === NOW.day });
    });
    return groups.map((g) => {
      const names = g.keys.map((k) => H.dayNames[k]);
      const label = names.length === 1 ? names[0] : (names.length === 2 ? H.pair(names[0], names[1]) : H.run(names[0], names[names.length - 1]));
      return { label, value: g.value, today: g.today, closed: g.closed };
    });
  }
  function contactHref(c) {
    if (c.type === 'WHATSAPP') return `https://wa.me/${c.value.replace(/\D/g, '')}`;
    if (c.type === 'PHONE') return `tel:${c.value}`;
    if (c.type === 'EMAIL') return `mailto:${c.value}`;
    return c.value;
  }
  const CICON = { WHATSAPP: 'message-circle', PHONE: 'phone', EMAIL: 'mail', INSTAGRAM: 'camera', FACEBOOK: 'external-link', WEBSITE: 'external-link', OTHER: 'external-link' };
  function fromPrice(sp, T) {
    const gen = sp.prices.filter((p) => p.audience === 'GENERAL');
    const pick = ['DAY', 'HOUR', 'WEEK', 'MONTH'].map((per) => gen.filter((p) => p.period === per)).find((a) => a.length);
    if (!pick) return null;
    const p = pick.reduce((a, b) => (a.amountAgorot <= b.amountAgorot ? a : b));
    return T.dir.page.from(ltr(esc(price(p.amountAgorot))), T.dir.card.periods[p.period]);
  }
  const fresh = (fn, iso, stale) => (iso ? `<p class="fresh">${esc(fn(ago(iso)))}${stale ? `<span class="stale">${esc(L().dir.page.stale)}</span>` : ''}</p>` : '');

  function contactsBlock(det, T, where) {
    const cs = det.contacts || [];
    const wa = cs.find((c) => c.type === 'WHATSAPP');
    const ph = cs.find((c) => c.type === 'PHONE');
    const rest = cs.filter((c) => c !== wa && c !== ph);
    let s = '';
    if (wa || ph) {
      s += `<div class="acts${wa && ph ? '' : ' solo'}">`;
      if (wa) s += `<a class="btn btn-primary" href="${esc(contactHref(wa))}" rel="noopener" target="_blank">${ic('message-circle')}${esc(T.dir.page.contacts.WHATSAPP)}</a>`;
      if (ph) s += `<a class="btn btn-secondary" href="${esc(contactHref(ph))}">${ic('phone')}${esc(T.dir.page.contacts.PHONE)}</a>`;
      s += '</div>';
    }
    if (rest.length) s += `<div class="more-contacts">${rest.map((c) => `<a class="link" href="${esc(contactHref(c))}"${c.type === 'EMAIL' ? '' : ' rel="noopener" target="_blank"'}>${ic(CICON[c.type] || 'external-link', 'ico-16')}${esc(T.dir.page.contacts[c.type] || c.type)}</a>`).join('')}</div>`;
    if (where === 'panel' && det.updatedAt && det.updatedAt.contacts) s += fresh(T.dir.page.updated.contacts, det.updatedAt.contacts, det.staleGroups.includes('contacts'));
    return s;
  }
  function statusBlock(sp, T, big) {
    const P = T.dir.page.liveStatus;
    const src = { live: P.live, hours: P.byHours, unset: P.unset, unverified: P.unverified }[sp.state.source];
    return `<p class="big-state k-${sp.state.kind}"${big ? '' : ' style="font-size:20px"'}><span class="dot k-${sp.state.kind}"></span>${esc(sp.state.word)}</p><p class="src">${esc(src)}</p>`;
  }
  function factsDl(sp, T) {
    const r = sp.days ? sp.days[NOW.day] : undefined;
    const today = !sp.days ? T.dir.card.noHours : (!r ? T.dir.card.closedToday : (r.opensMinute === 0 && r.closesMinute === 1440 ? T.dir.page.hours.allDay : ltr(`${clock(r.opensMinute)}–${clock(r.closesMinute)}`)));
    const fp = fromPrice(sp, T);
    return `<dl><dt>${esc(T.dir.page.todayLabel)}</dt><dd>${today}</dd><dt>${esc(T.dir.page.priceLabel)}</dt><dd>${fp || esc(T.dir.page.prices.none)}</dd></dl>`;
  }
  function locBlock(sp, det, T, id) {
    const addr = (prefs.lang === 'en' ? det.addressEn : null) || det.addressAr || det.addressEn || '';
    const gm = `https://www.google.com/maps/dir/?api=1&destination=${det.location.lat},${det.location.lng}`;
    return `<div class="loc"><div class="mini" id="${id}" role="img" aria-label="${esc(T.dir.page.mapOf(sp.name))}"></div>
      ${addr ? `<p class="addr"${prefs.lang === 'en' && !det.addressEn ? ' lang="ar" dir="rtl"' : ''}>${esc(addr)}</p>` : ''}
      <a class="btn btn-secondary" href="${gm}" target="_blank" rel="noopener">${ic('navigation')}${esc(T.dir.page.directions)}</a></div>`;
  }

  page({
    key: 'space', nav: 'spaces',
    bodyClass: () => {
      const det = B.D.details[slug];
      return det && (det.contacts || []).some((c) => c.type === 'WHATSAPP' || c.type === 'PHONE') ? 'has-bar' : '';
    },
    title: (T) => { const sp = spaces().find((s) => s.slug === slug); return sp ? sp.name : T.site.links.space; },
    main(T) {
      const sp = spaces().find((s) => s.slug === slug);
      if (!sp) {
        return `<div class="wrap"><div class="lost"><div class="lost-map">${silhouette({ w: 300, h: 380, dw: '100%', dh: '100%' })}</div>
          <div class="lost-text"><h1 class="t-h1">${esc(T.dir.page.notFound.title)}</h1><p>${esc(T.dir.page.notFound.text)}</p><a class="btn btn-primary" href="spaces.html">${esc(T.dir.page.back)}</a></div></div></div>`;
      }
      const det = sp.detail; const PG = T.dir.page;
      const photos = (det.photos || []).slice().sort((a, b) => (REAL.has(b.card.split('/').pop()) ? 1 : 0) - (REAL.has(a.card.split('/').pop()) ? 1 : 0));
      const hasReal = photos.some((p) => REAL.has(p.card.split('/').pop()));
      const lead = photos.length > 1 || hasReal;
      const alt = (i) => PG.photo(i + 1, photos.length, sp.name);
      let gallery = '';
      if (lead) {
        gallery = `<div class="gallery tablet-up" role="group" aria-label="${esc(PG.galleryLabel(sp.name))}"${photos.length === 1 ? ' style="grid-template-columns:1fr"' : ''}>
          <div class="g-main${B.frameCls(photos[0].page)}"><img src="${esc(photos[0].page)}" alt="${esc(alt(0))}" width="1200" height="900"></div>
          ${photos.length > 1 ? `<div class="g-side">${photos.slice(1, 3).map((p, i) => `<div class="${B.frameCls(p.card).trim()}"><img src="${esc(p.card)}" alt="${esc(alt(i + 1))}" loading="lazy" width="600" height="450"></div>`).join('')}</div>` : ''}
        </div>
        <div class="phone-only" style="position:relative;margin-block-end:24px"><div class="strip-photos" role="group" aria-label="${esc(PG.galleryLabel(sp.name))}" tabindex="0" id="sph">${photos.map((p, i) => `<div class="${B.frameCls(p.card).trim()}"><img src="${esc(p.card)}" alt="${esc(alt(i))}" width="400" height="300"${i ? ' loading="lazy"' : ''}></div>`).join('')}</div>
          ${photos.length > 1 ? `<span class="photo-count" aria-hidden="true"><bdi dir="ltr" id="phc">1 / ${photos.length}</bdi></span>` : ''}</div>`;
      }
      const poster = !lead && photos.length ? `<div class="poster${B.frameCls(photos[0].card)}"><img src="${esc(photos[0].card)}" alt="${esc(alt(0))}" width="400" height="300"></div>`
        : (!photos.length ? `<div class="poster"><div class="nophoto">${silhouette({ w: 120, h: 150, dot: sp.location, dotR: 6, pad: 4 })}<span class="np-area">${esc(PG.noPhotos)}</span></div></div>` : '');
      const heart = `<button type="button" class="icon-btn bordered heart" aria-pressed="false" aria-label="${esc(T.favorites.save(sp.name))}" data-heart>${ic('heart')}</button>`;
      // prices
      const gen = PERIODS.map((p) => sp.prices.find((x) => x.period === p && x.audience === 'GENERAL')).filter(Boolean);
      const stu = PERIODS.map((p) => sp.prices.find((x) => x.period === p && x.audience === 'STUDENT')).filter(Boolean);
      const ptable = (rows, cap, vh) => `<table class="ptable"><caption${vh ? ' class="vh"' : ''}>${esc(cap)}</caption><tbody>${rows.map((p) => `<tr><th scope="row">${esc(PG.prices.periods[p.period])}</th><td>${ltr(esc(price(p.amountAgorot)))}</td></tr>`).join('')}</tbody></table>`;
      const pricesSec = `<section class="sp-sec" aria-labelledby="s-prices"><h2 id="s-prices">${esc(PG.sections.prices)}</h2>
        ${gen.length || stu.length ? `<div class="prices${gen.length && stu.length ? ' two' : ''}">${gen.length ? ptable(gen, PG.prices.general, true) : ''}${stu.length ? ptable(stu, PG.prices.students) : ''}</div>
        <p class="t-secondary muted">${esc(PG.prices.displayOnly)}</p>` : `<p class="muted">${esc(PG.prices.none)}</p>`}
        ${fresh(PG.updated.prices, det.updatedAt.prices, det.staleGroups.includes('prices'))}</section>`;
      // hours
      const H = PG.hours;
      const rows = sp.days ? weekRows(sp.days, H) : [];
      const canExpand = sp.days && weekRows(sp.days, H).length > 2 || allDays;
      const hoursSec = `<section class="sp-sec" aria-labelledby="s-hours"><h2 id="s-hours">${esc(PG.sections.hours)}</h2>
        ${sp.days ? `<table class="hours"><caption class="vh">${esc(H.caption)}</caption><thead class="vh"><tr><th scope="col">${esc(H.days)}</th><th scope="col">${esc(H.hours)}</th></tr></thead><tbody>
          ${rows.map((r) => `<tr class="${r.today ? 'today' : ''}${r.closed ? ' closed' : ''}"><th scope="row">${r.today ? `<span class="today-mark">${esc(r.label)}<span class="dot" aria-hidden="true"></span><span class="today-word">${esc(H.today)}</span></span>` : esc(r.label)}</th><td>${r.value}</td></tr>`).join('')}
          </tbody></table>${canExpand ? `<div><button type="button" class="btn btn-quiet btn-sm" data-days aria-expanded="${allDays}">${esc(allDays ? H.showLess : H.showAll)}</button></div>` : ''}` : `<p class="muted">${esc(H.none)}</p>`}
        ${fresh(PG.updated.hours, det.updatedAt.hours, det.staleGroups.includes('hours'))}</section>`;
      const amenSec = det.amenities && det.amenities.length ? `<section class="sp-sec" aria-labelledby="s-amen"><h2 id="s-amen">${esc(PG.sections.amenities)}</h2>
        <ul class="amen">${det.amenities.map((a) => `<li>${ic(a.icon)}<span>${esc(prefs.lang === 'en' ? a.nameEn : a.nameAr)}</span></li>`).join('')}</ul>
        ${fresh(PG.updated.amenities, det.updatedAt.amenities, det.staleGroups.includes('amenities'))}</section>` : '';
      const desc = (prefs.lang === 'en' ? det.descriptionEn : det.descriptionAr) || det.descriptionAr || det.descriptionEn;
      const aboutSec = desc ? `<section class="sp-sec" aria-labelledby="s-about"><h2 id="s-about">${esc(PG.sections.about)}</h2>
        <div class="prose">${desc.split(/\n+/).map((p) => `<p>${esc(p)}</p>`).join('')}</div>${fresh(PG.updated.profile, det.updatedAt.profile, det.staleGroups.includes('profile'))}</section>` : '';
      const notice = !sp.verified ? `<div class="notice" role="note">${ic('info')}<div><p>${esc(PG.unverified(ago(det.updatedAt.profile)))}</p>
        <button type="button" class="report" style="color:var(--text)" data-owner>${esc(PG.unverifiedContact)}</button></div></div>` : '';
      const ann = sp.announcement ? `<div class="notice info" role="note">${ic('megaphone')}<div><p><b>${esc(T.terms.announcement)} · ${esc(PG.announcementType)}</b></p><p>${esc(PG.demoAnnouncement)}</p></div></div>` : '';
      const hasCall = (det.contacts || []).some((c) => c.type === 'WHATSAPP' || c.type === 'PHONE');
      const wa = (det.contacts || []).find((c) => c.type === 'WHATSAPP'); const ph = (det.contacts || []).find((c) => c.type === 'PHONE');
      return `<div class="wrap">
        <a class="back" href="spaces.html">${ic('arrow-left', 'dir')}${esc(PG.back)}</a>
        ${gallery}
        <div class="sp-grid">
          <div class="sp-main">
            <div class="sp-title-row${poster ? ' with-poster' : ''}">
              <div class="sp-title">
                <div class="card-top" style="align-items:flex-start;gap:16px"><h1 class="t-h1" style="flex:1">${esc(sp.name)}</h1>${heart}</div>
                ${sp.otherName ? `<p class="other" lang="${prefs.lang === 'ar' ? 'en' : 'ar'}">${esc(sp.otherName)}</p>` : ''}
                <p class="where">${esc(sp.place)}${sp.verified ? ` · <span class="verified" style="font-size:16px">${ic('badge-check', 'ico-16')}${esc(T.dir.card.verified)}</span>` : ''}</p>
              </div>
              ${poster}
            </div>
            <div class="phone-panel">${statusBlock(sp, T, true)}<div class="ppanel" style="padding:0">${factsDl(sp, T)}</div>
              ${(det.contacts || []).filter((c) => c.type !== 'WHATSAPP' && c.type !== 'PHONE').length ? `<div class="ppanel" style="padding:0">${contactsBlock({ contacts: det.contacts.filter((c) => c.type !== 'WHATSAPP' && c.type !== 'PHONE') }, T)}</div>` : ''}</div>
            ${notice}${ann}
            ${pricesSec}${hoursSec}${amenSec}${aboutSec}
            <section class="sp-sec phone-loc" aria-labelledby="s-loc"><h2 id="s-loc">${esc(PG.sections.location)}</h2>${locBlock(sp, det, T, 'miniPhone')}</section>
            <div><button type="button" class="report" data-report>${ic('flag', 'ico-16')}${esc(PG.report)}</button></div>
          </div>
          <aside class="sp-aside" aria-labelledby="s-panel"><div class="ppanel-wrap"><div class="panel ppanel">
            <h2 class="vh" id="s-panel">${esc(PG.statusContact)}</h2>
            ${statusBlock(sp, T, true)}
            ${factsDl(sp, T)}
            ${contactsBlock(det, T, 'panel')}
            ${locBlock(sp, det, T, 'miniAside')}
          </div></div></aside>
        </div>
      </div>
      ${hasCall ? `<div class="callbar${wa && ph ? '' : ' solo'}" role="region" aria-label="${esc(PG.bar.label)}">${wa ? `<a class="btn btn-primary" href="${esc(contactHref(wa))}" target="_blank" rel="noopener">${ic('message-circle')}${esc(PG.bar.whatsapp)}</a>` : ''}${ph ? `<a class="btn btn-secondary" href="${esc(contactHref(ph))}">${ic('phone')}${esc(PG.bar.call)}</a>` : ''}</div>` : ''}`;
    },
    mount(root, T) {
      const sp = spaces().find((s) => s.slug === slug);
      if (!sp) return;
      [mini, miniPhone].forEach((m) => m && m.destroy());
      const pin = [{ slug: sp.slug, name: sp.name, lat: sp.location.lat, lng: sp.location.lng, kind: sp.state.kind }];
      const ma = root.querySelector('#miniAside'), mp = root.querySelector('#miniPhone');
      mini = stripMap(ma, { mode: 'mark', pins: pin, pinR: 7, pad: 14, label: T.dir.page.mapOf(sp.name) });
      miniPhone = stripMap(mp, { mode: 'mark', pins: pin, pinR: 7, pad: 14, label: T.dir.page.mapOf(sp.name) });
      root.querySelectorAll('[data-heart]').forEach((b) => b.addEventListener('click', () => signInPrompt('favorite')));
      const rep = root.querySelector('[data-report]'); if (rep) rep.addEventListener('click', () => signInPrompt('report'));
      const d = root.querySelector('[data-days]'); if (d) d.addEventListener('click', () => { allDays = !allDays; B.setLang(prefs.lang); const again = document.querySelector('[data-days]'); if (again) again.focus(); });
      const ow = root.querySelector('[data-owner]');
      if (ow) ow.addEventListener('click', () => {
        const D2 = T.dir.page.dialog;
        dialog(`<div class="dialog-head"><h2 id="%ID%">${esc(D2.title)}</h2><button class="icon-btn" data-close aria-label="${esc(D2.close)}">${ic('x')}</button></div>
          <p class="muted">${esc(D2.text)}</p>
          <div class="dialog-actions"><a class="btn btn-primary" href="https://wa.me/${PLATFORM.whatsapp.replace(/\D/g, '')}" target="_blank" rel="noopener">${ic('message-circle')}${esc(T.about.whatsapp)}</a>
          <a class="btn btn-secondary" href="mailto:${PLATFORM.email}">${ic('mail')}${esc(T.about.email)}</a></div>`);
      });
      const sph = root.querySelector('#sph');
      if (sph) sph.addEventListener('scroll', () => { const n = Math.round(Math.abs(sph.scrollLeft) / sph.clientWidth) + 1; const c = root.querySelector('#phc'); if (c) c.textContent = `${n} / ${sph.children.length}`; }, { passive: true });
    },
  });
})();
