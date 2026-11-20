/* Sign in, About, Account settings, Favourites, 404 — one file, dispatched by <body data-page>. */
(function () {
  'use strict';
  const B = window.B;
  const { esc, ic, ltr, L, spaces, GOVS, card, page, prefs, stripMap, silhouette, signInPrompt, toast, km, num, USER } = B;
  const PAGE = document.currentScript && document.currentScript.dataset.page;
  const PLATFORM = { whatsapp: '+970597063545', email: 'masahatgaza@gmail.com' };
  const pinsOf = (list) => list.map((s) => ({ slug: s.slug, name: s.name, areaId: s.areaId, lat: s.location.lat, lng: s.location.lng, kind: s.state.kind }));
  const govCounts = (list) => { const c = {}; list.forEach((s) => { c[s.govId] = (c[s.govId] || 0) + 1; }); return c; };
  let maps = [];
  const resetMaps = () => { maps.forEach((m) => m.destroy()); maps = []; };

  function accountNav(T, current) {
    const A = T.site.account;
    return `<nav class="acct-nav" aria-label="${esc(A.navigation)}"><span class="nav-title" aria-hidden="true">${esc(A.navigation)}</span>
      <a href="favorites.html"${current === 'favorites' ? ' aria-current="page"' : ''}>${esc(A.favorites)}</a>
      <a href="404.html">${esc(A.reports)}</a>
      <a href="account.html"${current === 'account' ? ' aria-current="page"' : ''}>${esc(A.settings)}</a></nav>`;
  }

  /* ---------------- sign in ---------------- */
  if (PAGE === 'login') {
    let shown = false;
    page({
      key: 'login', nav: null,
      title: (T) => T.auth.signIn.title,
      main(T) {
        const A = T.auth;
        return `<div class="auth"><div class="auth-form-wrap wrap"><div class="auth-form">
            <div class="auth-thin">${silhouette({ w: 80, h: 96, pad: 2, dot: { lat: 31.5225, lng: 34.4475 }, dotR: 5, dw: '100%', dh: '100%' })}</div>
            <div><h1 class="t-h1">${esc(A.signIn.title)}</h1><p class="muted" style="margin-top:8px">${esc(A.signIn.description)}</p></div>
            <button type="button" class="btn g-btn btn-block" data-google>${esc(A.google)}</button>
            <p class="or">${esc(A.or)}</p>
            <form novalidate id="sf">
              <div class="field"><label for="em">${esc(A.fields.email)}</label><input class="input" id="em" name="email" type="email" autocomplete="email" dir="ltr" placeholder="${esc(A.fields.emailExample)}" aria-describedby="em-e"><p class="field-error" id="em-e" hidden></p></div>
              <div class="field"><div style="display:flex;align-items:baseline;justify-content:space-between;gap:12px"><label for="pw">${esc(A.fields.password)}</label><a class="link t-secondary" href="404.html">${esc(A.signIn.forgotPassword)}</a></div>
                <div class="input-wrap"><input class="input" id="pw" name="password" type="${shown ? 'text' : 'password'}" autocomplete="current-password" dir="ltr" aria-describedby="pw-e" style="padding-inline-end:48px"><button type="button" class="icon-btn" data-eye aria-label="${esc(shown ? A.hide : A.show)}" aria-pressed="${shown}">${ic(shown ? 'eye-off' : 'eye')}</button></div>
                <p class="field-error" id="pw-e" hidden></p></div>
              <button class="btn btn-primary btn-block" type="submit">${esc(A.signIn.submit)}</button>
            </form>
            <p>${esc(A.signIn.noAccount)} <a class="link" href="404.html">${esc(A.signIn.createAccount)}</a></p>
          </div></div>
          <div class="auth-side"><div id="authMap" style="position:absolute;inset:0"></div>
            <p class="cap">${esc(T.site.tagline.split('—')[1] ? T.site.tagline.split('—')[1].trim() : T.site.tagline)}<span>${esc(T.about.audience)}</span></p></div>
        </div>`;
      },
      mount(root, T) {
        resetMaps();
        const list = spaces();
        maps.push(stripMap(root.querySelector('#authMap'), { mode: 'mark', pins: pinsOf(list), labels: 'inside', pinR: 6.5,
          box(w, h) { return [0, 40, w, h - 240]; } }));
        const A = T.auth;
        const em = root.querySelector('#em'), pw = root.querySelector('#pw');
        const check = (el, show) => {
          const bad = el === em ? !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value.trim()) : el.value.length < 1;
          const msg = root.querySelector('#' + el.id + '-e');
          if (show) { el.setAttribute('aria-invalid', String(bad)); msg.hidden = !bad; msg.innerHTML = bad ? esc(el === em ? A.errors.email : A.errors.password) : ''; }
          else if (!bad && el.getAttribute('aria-invalid') === 'true') { el.removeAttribute('aria-invalid'); msg.hidden = true; }
          return !bad;
        };
        [em, pw].forEach((el) => { el.addEventListener('blur', () => { if (el.value) check(el, true); }); el.addEventListener('input', () => check(el, false)); });
        root.querySelector('#sf').addEventListener('submit', (e) => {
          e.preventDefault();
          const ok = [check(em, true), check(pw, true)];
          if (!ok[0]) em.focus(); else if (!ok[1]) pw.focus(); else location.href = 'account.html';
        });
        root.querySelector('[data-eye]').addEventListener('click', (e) => {
          shown = !shown; pw.type = shown ? 'text' : 'password';
          const b = e.currentTarget; b.setAttribute('aria-pressed', String(shown)); b.setAttribute('aria-label', shown ? A.hide : A.show); b.innerHTML = ic(shown ? 'eye-off' : 'eye');
        });
        root.querySelector('[data-google]').addEventListener('click', () => { location.href = 'account.html'; });
      },
    });
  }

  /* ---------------- about ---------------- */
  if (PAGE === 'about') {
    page({
      key: 'about', nav: 'about',
      title: (T) => T.site.links.about,
      main(T) {
        const A = T.about;
        const list = spaces();
        const govs = Object.keys(govCounts(list)).length;
        const pin = (k) => `<svg class="mapsvg" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><circle class="pin k-${k}" cx="12" cy="12" r="8"/>${k === 'full' ? '<rect class="pin-bar" x="7.5" y="11" width="9" height="2" rx="1"/>' : ''}</svg>`;
        return `<div class="wrap">
          <section class="about-open" aria-labelledby="h1">
            <div><h1 class="t-h1" id="h1">${esc(T.site.links.about)}</h1><div class="prose" style="margin-top:24px"><p>${esc(A.intro)}</p><p class="muted">${esc(A.audience)}</p></div></div>
            <figure class="about-strip" style="margin:0"><div id="aboutMap" style="position:absolute;inset:0"></div><figcaption>${esc(A.inGovs(list.length, govs))}</figcaption></figure>
          </section>
          <section class="sec" aria-labelledby="src-h"><div class="sec-head"><div><h2 class="t-h2" id="src-h">${esc(A.source.title)}</h2></div></div>
            <div class="two-col">
              <article><h3>${esc(A.verified.title)}</h3><p class="sub">${esc(A.verified.subtitle)}</p><p>${esc(A.verified.text)}</p></article>
              <article><h3>${esc(A.unverified.title)}</h3><p class="sub">${esc(A.unverified.subtitle)}</p><p>${esc(A.unverified.text)}</p></article>
            </div>
            <p class="prose muted" style="margin-top:32px">${esc(A.source.note)} ${esc(A.source.wrong)} <a class="link" href="#contact">${esc(A.source.wrongLink)}</a>${esc(A.source.wrongEnd)}</p>
          </section>
          <section class="sec" aria-labelledby="st-h"><div class="sec-head"><div><h2 class="t-h2" id="st-h">${esc(A.status.title)}</h2></div></div>
            <ul class="legend-list">
              <li>${pin('available')}<b>${esc(T.terms.available)}</b><p>${esc(A.status.available)}</p></li>
              <li>${pin('full')}<b>${esc(T.terms.full)}</b><p>${esc(A.status.full)}</p></li>
              <li>${pin('closed')}<b>${esc(T.terms.closedNow)}</b><p>${esc(A.status.closed)}</p></li>
              <li>${pin('none')}<b>${esc(T.dir.status.none)}</b><p>${esc(A.status.none)}</p></li>
            </ul></section>
          <section class="sec" id="contact" aria-labelledby="c-h" tabindex="-1"><div class="sec-head"><div><h2 class="t-h2" id="c-h">${esc(A.contact.title)}</h2><p>${esc(A.contact.text)}</p></div></div>
            <div class="contact-row"><a class="btn btn-primary" href="https://wa.me/${PLATFORM.whatsapp.replace(/\D/g, '')}" target="_blank" rel="noopener">${ic('message-circle')}${esc(A.whatsapp)} ${ltr(PLATFORM.whatsapp)}</a>
            <a class="btn btn-secondary" href="mailto:${PLATFORM.email}">${ic('mail')}${ltr(PLATFORM.email)}</a></div></section>
          <section class="sec" id="owners" aria-labelledby="o-h" tabindex="-1"><div class="sec-head"><div><h2 class="t-h2" id="o-h">${esc(A.owners.title)}</h2></div></div>
            <ol class="steps">${A.owners.steps.map((s) => `<li>${esc(s)}</li>`).join('')}</ol></section>
        </div>`;
      },
      mount(root) {
        resetMaps();
        const list = spaces();
        maps.push(stripMap(root.querySelector('#aboutMap'), { mode: 'mark', pins: pinsOf(list), labels: 'callout', counts: govCounts(list), inset: false, pinR: 6, calloutGap: 24,
          box(w, h) { return [8, 8, w - 170, h - 70]; } }));
        if (location.hash) { const t = document.querySelector(location.hash); if (t) setTimeout(() => t.scrollIntoView(), 0); }
      },
    });
  }

  /* ---------------- account settings ---------------- */
  if (PAGE === 'account') {
    let pwOpen = false, name = USER.name, saved = false;
    page({
      key: 'account', nav: null, account: true,
      title: (T) => T.users.settings.title,
      main(T) {
        const S = T.users.settings; const R = T.users.rules;
        const choice = prefs.themeChoice;
        return `<div class="wrap acct">${accountNav(T, 'account')}
          <div class="settings">
            <header><h1 class="t-h1">${esc(S.title)}</h1></header>
            <section class="sgroup" aria-labelledby="g1"><header><h2 id="g1">${esc(S.profile.title)}</h2></header>
              <form class="fields" id="pf" novalidate>
                <div class="field"><label for="nm">${esc(S.profile.name)}</label><input class="input" id="nm" value="${esc(name)}" autocomplete="name" style="max-width:420px"></div>
                <div class="field"><span class="label">${esc(S.profile.email)}</span><p class="ro">${ltr(esc(USER.email))}</p><p class="field-help">${esc(S.profile.emailNote)}</p></div>
                <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap"><button class="btn btn-primary" type="submit">${esc(S.profile.save)}</button><span class="saved" role="status">${saved ? ic('check', 'ico-16') + esc(S.profile.saved) : ''}</span></div>
              </form></section>
            <section class="sgroup" aria-labelledby="g2"><header><h2 id="g2">${esc(S.preferences.title)}</h2><p>${esc(S.preferences.description)}</p></header>
              <div class="fields">
                <div class="field"><span class="label" id="lg">${esc(S.preferences.language)}</span>
                  <div class="seg" role="radiogroup" aria-labelledby="lg">${['ar', 'en'].map((l) => `<label lang="${l}"><input type="radio" name="lang" value="${l}" ${prefs.lang === l ? 'checked' : ''}>${esc(T.users.languages[l])}</label>`).join('')}</div>
                  <p class="field-help">${esc(S.preferences.languageHelper)}</p></div>
                <div class="field"><span class="label" id="th">${esc(S.preferences.theme)}</span>
                  <div class="seg" role="radiogroup" aria-labelledby="th">${['light', 'dark', 'system'].map((t) => `<label><input type="radio" name="theme" value="${t}" ${choice === t ? 'checked' : ''}>${esc(S.preferences.themes[t])}</label>`).join('')}</div>
                  <p class="field-help">${esc(S.preferences.themeHelper)}</p></div>
              </div></section>
            <section class="sgroup" aria-labelledby="g3"><header><h2 id="g3">${esc(S.signIn.title)}</h2><p>${esc(S.signIn.description)}</p></header>
              <div class="fields"><div>
                <div class="method"><b>${esc(S.signIn.google)}</b><span class="tag">${ic('check', 'ico-16')}${esc(S.signIn.linked)}</span><p>${S.signIn.googleLine(ltr(esc(USER.email)))}</p></div>
                <div class="method"><b>${esc(S.signIn.password)}</b>${pwOpen ? '<span></span>' : `<button type="button" class="btn btn-secondary btn-sm" data-pw aria-expanded="false">${esc(S.signIn.change)}</button>`}<p>${esc(S.signIn.passwordLine)}</p>
                ${pwOpen ? `<form class="pw-form" id="pwf" novalidate>
                  <div class="field"><label for="cp">${esc(S.passwordForm.current)}</label><input class="input" id="cp" type="password" autocomplete="current-password" dir="ltr" style="max-width:420px"></div>
                  <div class="field"><label for="np">${esc(S.passwordForm.new)}</label><input class="input" id="np" type="password" autocomplete="new-password" dir="ltr" style="max-width:420px" aria-describedby="rl">
                    <ul class="rules" id="rl" aria-label="${esc(R.label)}"><li data-r="len">${ic('check', 'ico-16')}${esc(R.minLength)}</li><li data-r="let">${ic('check', 'ico-16')}${esc(R.letter)}</li><li data-r="dig">${ic('check', 'ico-16')}${esc(R.digit)}</li></ul></div>
                  <p class="field-help">${esc(S.passwordForm.othersLine)}</p>
                  <div style="display:flex;gap:12px;flex-wrap:wrap"><button class="btn btn-primary" type="submit">${esc(S.passwordForm.save)}</button><button type="button" class="btn btn-quiet" data-pwback>${esc(S.passwordForm.back)}</button></div>
                </form>` : ''}</div>
              </div></div></section>
          </div></div>`;
      },
      mount(root) {
        root.querySelectorAll('input[name="lang"]').forEach((i) => i.addEventListener('change', () => { B.setLang(i.value); const f = document.querySelector('input[name="lang"]:checked'); if (f) f.focus(); }));
        root.querySelectorAll('input[name="theme"]').forEach((i) => i.addEventListener('change', () => { B.setTheme(i.value); const f = document.querySelector('input[name="theme"]:checked'); if (f) f.focus(); }));
        root.querySelector('#pf').addEventListener('submit', (e) => { e.preventDefault(); name = root.querySelector('#nm').value; saved = true; B.setLang(prefs.lang); });
        const pb = root.querySelector('[data-pw]'); if (pb) pb.addEventListener('click', () => { pwOpen = true; B.setLang(prefs.lang); const c = document.querySelector('#cp'); if (c) c.focus(); });
        const back = root.querySelector('[data-pwback]'); if (back) back.addEventListener('click', () => { pwOpen = false; B.setLang(prefs.lang); const b = document.querySelector('[data-pw]'); if (b) b.focus(); });
        const np = root.querySelector('#np');
        if (np) np.addEventListener('input', () => { const v = np.value; const r = { len: v.length >= 8, let: /\p{L}/u.test(v), dig: /\d/.test(v) }; root.querySelectorAll('[data-r]').forEach((li) => li.classList.toggle('met', r[li.dataset.r])); });
        const pwf = root.querySelector('#pwf'); if (pwf) pwf.addEventListener('submit', (e) => { e.preventDefault(); });
      },
    });
  }

  /* ---------------- favourites ---------------- */
  if (PAGE === 'favorites') {
    const SAVED = ['branch-hub', 'focus-hub', 'coma-io', 'masahat', 'pal-hub'];
    const removed = new Set();
    let near = null;
    page({
      key: 'favorites', nav: null, account: true,
      title: (T) => T.favorites.title,
      main(T) {
        const F = T.favorites;
        let list = spaces().filter((s) => SAVED.includes(s.slug) && !removed.has(s.slug));
        list.sort((a, b) => SAVED.indexOf(a.slug) - SAVED.indexOf(b.slug));
        if (near) { list.forEach((s) => { s.dist = km(near, s.location); }); list.sort((a, b) => a.dist - b.dist); }
        const goneShown = !removed.has('noor-hub');
        const total = list.length + (goneShown ? 1 : 0);
        const cards = list.map((s) => card(s, { level: 2, saved: true, row: window.innerWidth < 768, noPhoto: s.slug === 'masahat', distance: near ? s.dist : null })).join('');
        const gone = goneShown ? `<article class="card gone${window.innerWidth < 768 ? ' row' : ''}"><div class="card-photo"><div class="nophoto">${silhouette({ w: 120, h: 150, pad: 4 })}</div></div>
          <div class="card-body"><div class="card-top"><h2 class="card-name">نور هب</h2></div><p class="gone-line">${esc(F.gone)}</p>
          <div><button type="button" class="btn btn-secondary btn-sm" data-gone>${esc(F.removeWord)}</button></div></div></article>` : '';
        return `<div class="wrap acct">${accountNav(T, 'favorites')}
          <div>
            <div class="fav-head"><div><h1 class="t-h1">${esc(F.title)}</h1><p>${esc(F.description)} · ${esc(F.count(total))}</p></div>
              <button type="button" class="ftrig near${near ? ' on' : ''}" data-near aria-pressed="${!!near}">${ic('locate-fixed', 'ico-16')}<span>${esc(T.dir.near.button)}</span></button></div>
            ${near ? `<p class="near-line" style="margin-bottom:24px">${ic('locate-fixed', 'ico-16')}<span>${esc(T.dir.near.sorted)} ${esc(T.dir.near.approximate)}</span></p>` : ''}
            ${total ? `<div class="fav-grid" role="region" aria-label="${esc(F.region)}">${cards}${gone}</div>`
              : `<div class="empty-line"><h2 class="t-h2">${esc(F.empty.title)}</h2><p class="muted">${esc(F.empty.text)}</p><a class="btn btn-secondary" href="spaces.html">${esc(T.site.browseSpaces)}</a></div>`}
          </div></div>`;
      },
      mount(root, T) {
        root.querySelectorAll('[data-heart]').forEach((b) => b.addEventListener('click', (e) => {
          e.preventDefault();
          const slug = b.dataset.heart;
          removed.add(slug); B.setLang(prefs.lang);
          toast(T.favorites.removed, { label: T.favorites.undo, run() { removed.delete(slug); B.setLang(prefs.lang); } });
        }));
        const g = root.querySelector('[data-gone]');
        if (g) g.addEventListener('click', () => { removed.add('noor-hub'); B.setLang(prefs.lang); toast(T.favorites.removed, { label: T.favorites.undo, run() { removed.delete('noor-hub'); B.setLang(prefs.lang); } }); });
        root.querySelector('[data-near]').addEventListener('click', () => { near = near ? null : { lat: 31.5236, lng: 34.4437 }; B.setLang(prefs.lang); const n = document.querySelector('[data-near]'); if (n) n.focus(); });
      },
    });
  }

  /* ---------------- 404 ---------------- */
  if (PAGE === '404') {
    page({
      key: '404', nav: null,
      title: (T) => T.status.notFound.title,
      main(T) {
        const N = T.status.notFound;
        return `<div class="wrap lost">
          <div class="lost-text"><h1 class="t-h1">${esc(N.title)}</h1><p class="sub">${esc(T.status.notOnMap)}</p><p>${esc(N.description)}</p>
            <div class="contact-row"><a class="btn btn-primary" href="spaces.html">${esc(T.site.browseSpaces)}</a><a class="btn btn-secondary" href="home.html">${esc(T.site.links.home)}</a></div></div>
          <div class="lost-map" id="lostMap"></div>
        </div>`;
      },
      mount(root) {
        resetMaps();
        maps.push(stripMap(root.querySelector('#lostMap'), { mode: 'mark', pins: pinsOf(spaces()), labels: 'inside', pinR: 5.5, pad: 12, draw: true }));
      },
    });
  }
  void GOVS; void num; void signInPrompt;
})();
