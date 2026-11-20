/* The directory: the filter bar (popovers; a sheet on the phone), the list and the map side by side from 1024. */
(function () {
  'use strict';
  const B = window.B;
  const { esc, ic, ltr, L, spaces, GOVS, govName, areaName, stripMap, card, wireHearts, page, prefs, price, num, km, Q, D } = B;
  const PERIODS = ['HOUR', 'DAY', 'WEEK', 'MONTH'];
  const RIMAL = { lat: 31.5236, lng: 34.4437 }; // the simulated device point, in الرمال
  const W = () => window.innerWidth;

  const st = {
    q: Q.get('q') || '', areas: new Set(), period: null, from: '', to: '',
    openNow: Q.get('open') === '1', evening: false, friday: false, verified: false, students: false, women: false,
    sort: 'updated', near: null, locating: false,
    view: Q.get('view') === 'map' ? 'map' : 'list', pop: null, sheet: false, sel: null,
  };
  if (Q.get('area')) Q.get('area').split(',').forEach((a) => st.areas.add(+a));
  if (Q.get('gov')) { const g = GOVS.find((x) => x.id === +Q.get('gov')); if (g) g.areas.forEach((a) => st.areas.add(a.id)); }
  if (Q.get('filters') === 'open') { st.period = 'MONTH'; st.from = '250'; st.to = '400'; if (W() < 768) st.sheet = true; else st.pop = 'price'; }
  const wantNear = Q.get('near') === '1';

  let map = null, bound = false;
  const norm = (s) => String(s || '').toLowerCase().replace(/[ً-ْـ]/g, '').replace(/[إأآ]/g, 'ا').replace(/ة/g, 'ه').replace(/ى/g, 'ي').trim();
  const priceOf = (s, period) => { const p = s.prices.filter((x) => x.period === period); if (!p.length) return null; const g = p.filter((x) => x.audience === 'GENERAL'); return Math.min(...(g.length ? g : p).map((x) => x.amountAgorot)); };
  const rangeBad = () => st.from !== '' && st.to !== '' && +st.to < +st.from;

  function filtered() {
    const all = spaces();
    const q = norm(st.q);
    let list = all.filter((s) => {
      if (q) {
        const hay = [s.nameAr, s.nameEn, B.AREA[s.areaId] && B.AREA[s.areaId].nameAr, B.AREA[s.areaId] && B.AREA[s.areaId].nameEn, s.gov].map(norm).join(' ');
        if (!hay.includes(q)) return false;
      }
      if (st.areas.size && !st.areas.has(s.areaId)) return false;
      if (st.period) {
        const p = priceOf(s, st.period);
        if (p == null) return false;
        if (!rangeBad()) {
          if (st.from !== '' && p < +st.from * 100) return false;
          if (st.to !== '' && p > +st.to * 100) return false;
        }
      }
      if (st.openNow && !s.state.open) return false;
      if (st.evening && !s.worksEvenings) return false;
      if (st.friday && !(s.days && s.days[5])) return false;
      if (st.verified && !s.verified) return false;
      if (st.students && !s.prices.some((p) => p.audience === 'STUDENT')) return false;
      if (st.women && !s.womensHall) return false;
      return true;
    });
    if (st.near) list.forEach((s) => { s.dist = km(st.near, s.location); });
    const coll = new Intl.Collator(prefs.lang);
    const sort = st.near ? 'distance' : st.sort;
    list.sort((a, b) => {
      if (sort === 'distance') return a.dist - b.dist;
      if (sort === 'name') return coll.compare(a.name, b.name);
      if (sort === 'priceAsc' || sort === 'priceDesc') {
        const pa = priceOf(a, st.period), pb = priceOf(b, st.period);
        if (pa == null) return 1; if (pb == null) return -1;
        return sort === 'priceAsc' ? pa - pb : pb - pa;
      }
      return a.order - b.order;
    });
    return { all, list };
  }
  const activeCount = () => st.areas.size + (st.period ? 1 : 0) + ['openNow', 'evening', 'friday', 'verified', 'students', 'women'].filter((k) => st[k]).length + (st.q ? 1 : 0);

  /* ---------- trigger values ---------- */
  function trigValue(key, T) {
    const F = T.dir.filters;
    if (key === 'area') {
      if (!st.areas.size) return null;
      const names = [...st.areas].map((id) => areaName(B.AREA[id]));
      return names.length === 1 ? names[0] : `${names[0]} +${num(names.length - 1)}`;
    }
    if (key === 'price') {
      if (!st.period) return null;
      let v = F.periods[st.period];
      if (st.from !== '' || st.to !== '') v += ` · ⁦${st.from || '0'}–${st.to || '∞'} ₪⁩`;
      return v;
    }
    if (key === 'schedule') { const on = [['openNow', F.openNow], ['evening', F.evening], ['friday', F.openFriday]].filter(([k]) => st[k]).map(([, w]) => w); return on.length ? (on.length === 1 ? on[0] : `${on[0]} +${num(on.length - 1)}`) : null; }
    if (key === 'other') { const on = [['verified', F.verified], ['students', F.studentPrices], ['women', F.womensHall]].filter(([k]) => st[k]).map(([, w]) => w); return on.length ? (on.length === 1 ? on[0] : `${on[0]} +${num(on.length - 1)}`) : null; }
    return null;
  }
  function sortName(T) {
    if (st.near) return T.dir.sort.options.distance;
    if (st.sort === 'priceAsc') return T.dir.sort.priceAsc[st.period];
    if (st.sort === 'priceDesc') return T.dir.sort.priceDesc[st.period];
    return T.dir.sort.options[st.sort];
  }
  const GROUP_LABEL = (key, T) => ({ area: T.dir.filters.area, price: T.dir.filters.price, schedule: T.dir.filters.schedule, other: T.dir.filters.other, sort: T.dir.sort.label }[key]);
  function trigger(key, T) {
    const v = key === 'sort' ? null : trigValue(key, T);
    const label = key === 'sort' ? T.dir.sort.value(sortName(T)) : (v || GROUP_LABEL(key, T));
    const on = !!v;
    return `<button type="button" class="ftrig${on ? ' on' : ''}" data-trig="${key}" aria-expanded="${st.pop === key}" aria-controls="pop-${key}"${on ? ` aria-label="${esc(GROUP_LABEL(key, T) + ': ' + v)}"` : ''}>${key === 'sort' ? `<span class="v v-long">${esc(label)}</span><span class="v v-short">${esc(T.dir.sort.label)}</span>` : `<span class="v">${esc(label)}</span>`}${ic('chevron-down', 'ico-16')}</button>`;
  }

  /* ---------- group bodies (shared by popovers and the phone sheet) ---------- */
  function groupBody(key, T, where) {
    const F = T.dir.filters;
    const id = (x) => `${where}-${x}`;
    if (key === 'area') {
      const all = spaces();
      const n = {}; all.forEach((s) => { n[s.areaId] = (n[s.areaId] || 0) + 1; });
      return `<div class="areas-cols">${GOVS.map((g) => `<fieldset style="border:0;margin:0;padding:0"><legend class="vh">${esc(govName(g))}</legend><h4 aria-hidden="true">${esc(govName(g))}</h4>${g.areas.map((a) => `<label class="check"><input type="checkbox" data-area="${a.id}" ${st.areas.has(a.id) ? 'checked' : ''}><span>${esc(areaName(a))}</span><span class="count">${num(n[a.id] || 0)}</span></label>`).join('')}</fieldset>`).join('')}</div>`;
    }
    if (key === 'price') {
      const r = D.priceRanges[st.period || 'MONTH'];
      return `<fieldset style="border:0;margin:0;padding:0"><legend class="field-help" style="padding:0;margin-bottom:8px">${esc(F.subscription)}</legend>
        <div class="seg" role="radiogroup">${[['', F.all]].concat(PERIODS.map((p) => [p, F.periods[p]])).map(([p, w]) => `<label><input type="radio" name="${id('period')}" value="${p}" data-period ${(st.period || '') === p ? 'checked' : ''}>${esc(w)}</label>`).join('')}</div></fieldset>
        ${st.period ? `<div class="range">
          <div class="field"><label for="${id('from')}">${esc(F.from)}</label><div class="money"><input class="input" id="${id('from')}" data-range="from" inputmode="numeric" value="${esc(st.from)}" placeholder="${num(r.minAgorot / 100)}" aria-describedby="${id('rh')}"><span class="cur" aria-hidden="true">₪</span></div></div>
          <div class="field"><label for="${id('to')}">${esc(F.to)}</label><div class="money"><input class="input" id="${id('to')}" data-range="to" inputmode="numeric" value="${esc(st.to)}" placeholder="${num(r.maxAgorot / 100)}" aria-describedby="${id('rh')}" ${rangeBad() ? 'aria-invalid="true"' : ''}><span class="cur" aria-hidden="true">₪</span></div></div>
        </div><p class="field-help" id="${id('rh')}" style="margin-top:8px">${esc(F.rangeHelp(F.priceNames[st.period]))}</p>${rangeBad() ? `<p class="field-error" role="alert">${esc(F.belowMin)}</p>` : ''}`
        : `<p class="field-help" style="margin-top:12px;max-width:36ch">${esc(F.subscriptionHint)}</p>`}`;
    }
    if (key === 'schedule') return [['openNow', F.openNow], ['evening', F.evening], ['friday', F.openFriday]].map(([k, w]) => `<label class="check"><input type="checkbox" data-flag="${k}" ${st[k] ? 'checked' : ''}><span>${esc(w)}</span></label>`).join('');
    if (key === 'other') return [['verified', F.verified], ['students', F.studentPrices], ['women', F.womensHall]].map(([k, w]) => `<label class="check"><input type="checkbox" data-flag="${k}" ${st[k] ? 'checked' : ''}><span>${esc(w)}</span></label>`).join('');
    if (key === 'sort') {
      const opts = [['updated', T.dir.sort.options.updated], ['name', T.dir.sort.options.name]];
      if (st.period) opts.push(['priceAsc', T.dir.sort.priceAsc[st.period]], ['priceDesc', T.dir.sort.priceDesc[st.period]]);
      if (st.near) return `<p class="field-help" style="max-width:32ch">${esc(T.dir.near.sorted)}</p><button type="button" class="btn btn-secondary btn-sm" data-stopnear style="margin-top:8px">${esc(T.dir.near.stop)}</button>`;
      return `<fieldset style="border:0;margin:0;padding:0"><legend class="vh">${esc(T.dir.sort.label)}</legend>${opts.map(([k, w]) => `<label class="check"><input type="radio" name="${id('sort')}" value="${k}" data-sort ${st.sort === k ? 'checked' : ''}><span>${esc(w)}</span></label>`).join('')}</fieldset>${!st.period ? `<p class="field-help" style="max-width:32ch">${esc(T.dir.filters.subscriptionHint)}</p>` : ''}`;
    }
    return '';
  }
  function popover(key, T) {
    return `<div class="pop panel" id="pop-${key}" role="dialog" aria-label="${esc(GROUP_LABEL(key, T))}">
      <h3>${esc(GROUP_LABEL(key, T))}</h3><div class="pop-body">${groupBody(key, T, 'p')}</div>
      ${key !== 'sort' ? `<div class="pop-foot"><span class="t-meta">${esc(T.dir.filters.description)}</span><button type="button" class="btn btn-quiet btn-sm" data-clear="${key}">${esc(T.dir.filters.clear)}</button></div>` : ''}
    </div>`;
  }

  page({
    key: 'spaces', nav: 'spaces',
    bodyClass: () => (st.view === 'map' ? 'view-map' : ''),
    title: (T) => T.dir.title,
    main(T) {
      const F = T.dir.filters;
      const groups = ['area', 'price', 'schedule', 'other'];
      return `<div class="wrap">
        <div class="dir-head"><h1 class="t-h1">${esc(T.dir.title)}</h1><p class="count" id="count" aria-live="polite"></p>
          <div class="seg view-tabs" role="group" aria-label="${esc(T.dir.view.label)}"><button type="button" data-view="list" aria-pressed="${st.view === 'list'}">${ic('list')}&nbsp;${esc(T.dir.view.list)}</button><button type="button" data-view="map" aria-pressed="${st.view === 'map'}">${ic('map')}&nbsp;${esc(T.dir.view.map)}</button></div></div>
        <div class="fbar" id="fbar">
          <form class="search" role="search" onsubmit="return false"><label class="vh" for="dq">${esc(T.dir.search.label)}</label><div class="input-wrap">${ic('search')}<input class="input has-ico" id="dq" type="search" value="${esc(st.q)}" placeholder="${esc(T.dir.search.placeholder)}" autocomplete="off"></div></form>
          <button type="button" class="ftrig phone-only" data-sheet>${ic('sliders-horizontal', 'ico-16')}<span>${esc(F.title)}</span><span class="badge" id="fcount" hidden></span></button>
          ${groups.map((g) => `<div class="fgroup tablet-up" data-group="${g}">${trigger(g, T)}</div>`).join('')}
          <div class="fgroup" data-group="sort">${trigger('sort', T)}</div>
          <button type="button" class="ftrig near${st.near ? ' on' : ''}" data-near aria-pressed="${!!st.near}">${ic('locate-fixed', 'ico-16')}<span>${esc(st.locating ? T.dir.near.locating : T.dir.near.button)}</span></button>
        </div>
        <div id="nearLine"></div>
        <div class="split">
          <div class="listcol"><h2 class="vh">${esc(T.dir.results)}</h2><div class="list" id="list"></div></div>
          <div class="mapcol" aria-label="${esc(T.dir.map.label)}" role="region">
            <div class="map-box"><div id="mapEl" style="position:absolute;inset:0"></div>
              <div class="map-ctrl"><button type="button" data-zoom="in" aria-label="${esc(T.dir.map.zoomIn)}" title="${esc(T.dir.map.zoomIn)}">${ic('plus')}</button><button type="button" data-zoom="out" aria-label="${esc(T.dir.map.zoomOut)}" title="${esc(T.dir.map.zoomOut)}">${ic('minus')}</button><button type="button" data-zoom="whole" aria-label="${esc(T.dir.map.whole)}" title="${esc(T.dir.map.whole)}">${ic('maximize')}</button></div>
              <div class="legend"><h3>${esc(T.dir.map.legend)}</h3><ul>
                <li><span class="dot k-open"></span>${esc(T.terms.available)} · ${esc(T.dir.status.open)}</li>
                <li><span class="dot k-full"></span>${esc(T.terms.full)}</li>
                <li><span class="dot k-closed"></span>${esc(T.terms.closedNow)} · ${esc(T.dir.status.closed)}</li>
                <li><span class="dot k-none"></span>${esc(T.dir.status.none)}</li></ul></div>
              <div id="place"></div>
            </div>
          </div>
        </div>
      </div>
      <button type="button" class="btn btn-primary float-toggle" data-flip>${ic(st.view === 'map' ? 'list' : 'map')}${esc(st.view === 'map' ? T.dir.view.list : T.dir.view.map)}</button>`;
    },
    mount(root, T) {
      if (map) { map.destroy(); map = null; }
      bind(root);
      update();
      if (st.pop) openPop(st.pop, false);
      if (st.sheet) openSheet(false);
      if (wantNear && !st.near && !st.locating) locate();
    },
  });

  function rowMode() { const w = W(); return w < 768 || (w >= 1024 && w < 1280 && st.view !== 'map'); }

  function update() {
    const T = L();
    const { list } = filtered();
    const root = document.getElementById('main');
    if (!root) return;
    const count = root.querySelector('#count');
    count.textContent = activeCount() ? T.dir.countMatching(list.length) : T.dir.countAll(list.length);
    const fc = root.querySelector('#fcount');
    const n = activeCount() - (st.q ? 1 : 0);
    fc.hidden = !n; fc.textContent = num(n);
    root.querySelectorAll('.fgroup').forEach((g) => {
      const key = g.dataset.group;
      const old = g.querySelector('.ftrig');
      const tmp = document.createElement('div'); tmp.innerHTML = trigger(key, T);
      const nb = tmp.firstElementChild;
      old.className = nb.className; old.innerHTML = nb.innerHTML; old.setAttribute('aria-expanded', String(st.pop === key));
      if (nb.hasAttribute('aria-label')) old.setAttribute('aria-label', nb.getAttribute('aria-label')); else old.removeAttribute('aria-label');
    });
    const nearBtn = root.querySelector('[data-near]');
    nearBtn.className = 'ftrig near' + (st.near ? ' on' : '');
    nearBtn.setAttribute('aria-pressed', String(!!st.near));
    nearBtn.querySelector('span').textContent = st.locating ? T.dir.near.locating : T.dir.near.button;
    root.querySelector('#nearLine').innerHTML = st.near
      ? `<p class="near-line">${ic('locate-fixed', 'ico-16')}<span>${esc(T.dir.near.sorted)} ${esc(T.dir.near.approximate)}</span><button type="button" data-stopnear>${esc(T.dir.near.stop)}</button></p>`
      : (st.locating ? `<p class="near-line"><span>${esc(T.dir.near.privacy)}</span></p>` : '');
    const row = rowMode();
    const L2 = root.querySelector('#list');
    L2.innerHTML = list.length ? list.map((s) => card(s, {
      level: 3, row, sel: s.slug === st.sel,
      distance: st.near ? s.dist : null,
      price: st.period && priceOf(s, st.period) != null ? T.dir.card.price(ltr(esc(price(priceOf(s, st.period)))), T.dir.card.periods[st.period]) : null,
    })).join('') : `<div class="nomatch"><h2>${esc(T.dir.noMatch.title)}</h2><p class="muted">${esc(T.dir.noMatch.text)}</p><button type="button" class="btn btn-secondary" data-clearall>${esc(T.dir.clearFilters)}</button></div>`;
    wireHearts(L2);
    L2.querySelectorAll('.card').forEach((c) => {
      const s = c.dataset.slug;
      c.addEventListener('mouseenter', () => map && map.raise(s));
      c.addEventListener('mouseleave', () => map && map.raise(null));
      c.addEventListener('focusin', () => map && map.raise(s));
      c.addEventListener('focusout', () => map && map.raise(null));
    });
    const ca = L2.querySelector('[data-clearall]'); if (ca) ca.addEventListener('click', clearAll);
    const pins = list.map((s) => ({ slug: s.slug, name: s.name, word: s.state.word, lat: s.location.lat, lng: s.location.lng, kind: s.state.kind }));
    if (st.sel && !list.some((s) => s.slug === st.sel)) { st.sel = null; }
    if (map) { map.setPins(pins); map.setYou(st.near); }
    else {
      map = stripMap(root.querySelector('#mapEl'), { mode: 'work', pins, labels: 'inside', pad: 28, initial: st.view === 'map' ? 'pins' : 'strip', label: T.dir.map.label, selected: st.sel, you: st.near,
        onSelect(slug) { st.sel = slug; markSel(); place(); } });
    }
    place();
    root.querySelectorAll('[data-stopnear]').forEach((b) => b.addEventListener('click', () => { st.near = null; closePop(); update(); }));
    const sheetCount = document.querySelector('[data-sheetshow]');
    if (sheetCount) sheetCount.textContent = T.dir.filters.show(list.length);
  }
  function markSel() {
    document.querySelectorAll('#list .card').forEach((c) => c.classList.toggle('sel', c.dataset.slug === st.sel));
    if (st.sel && W() >= 1024 && st.view === 'list') { const c = document.querySelector(`#list .card[data-slug="${st.sel}"]`); if (c) c.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); }
  }
  function place() {
    const T = L();
    const el = document.getElementById('place');
    if (!el) return;
    const showSheet = st.sel && (st.view === 'map' || W() >= 1024);
    const box = el.closest('.map-box'); if (box) box.classList.toggle('has-place', !!showSheet);
    if (!showSheet) { el.innerHTML = ''; return; }
    const s = spaces().find((x) => x.slug === st.sel);
    if (!s) { el.innerHTML = ''; return; }
    el.innerHTML = `<div class="place panel" role="region" aria-label="${esc(s.name)}">
      <div class="ph${B.frameCls(s.cover)}">${s.cover ? `<img src="${esc(s.cover)}" alt="">` : ''}</div>
      <div class="body"><h3>${esc(s.name)}</h3><p class="t-secondary muted">${esc(s.place)}</p>
        <p class="facts"><span class="state k-${s.state.kind}"><span class="dot k-${s.state.kind}"></span>${esc(s.state.word)}</span><span>${s.today}</span></p>
        <div class="acts"><a class="btn btn-primary btn-sm" href="space.html?slug=${s.slug}">${esc(T.dir.map.view)}</a></div></div>
      <button type="button" class="icon-btn x" data-closeplace aria-label="${esc(T.dir.map.close)}">${ic('x')}</button></div>`;
    el.querySelector('[data-closeplace]').addEventListener('click', () => { const s0 = st.sel; st.sel = null; map.select(null); markSel(); place(); const h = document.querySelector(`.hit[data-slug="${s0}"]`); if (h) h.focus(); });
  }

  /* ---------- popovers ---------- */
  function openPop(key, focus) {
    closePop(true);
    st.pop = key;
    const T = L();
    const g = document.querySelector(`.fgroup[data-group="${key}"]`);
    if (!g) return;
    g.insertAdjacentHTML('beforeend', popover(key, T));
    const pop = g.querySelector('.pop');
    const r = pop.getBoundingClientRect();
    if (r.left < 8 || r.right > window.innerWidth - 8) pop.classList.add('end');
    const r2 = pop.getBoundingClientRect();
    if (r2.left < 8 || r2.right > window.innerWidth - 8) { pop.classList.remove('end'); pop.style.insetInlineStart = 'auto'; }
    g.querySelector('.ftrig').setAttribute('aria-expanded', 'true');
    bindGroup(pop, () => {
      const body = pop.querySelector('.pop-body');
      const active = document.activeElement && document.activeElement.id;
      body.innerHTML = groupBody(key, L(), 'p');
      bindGroup(pop, null, true);
      if (active) { const a = document.getElementById(active); if (a) { a.focus(); if (a.setSelectionRange && a.value) a.setSelectionRange(a.value.length, a.value.length); } }
    });
    const c = pop.querySelector('[data-clear]');
    if (c) c.addEventListener('click', () => { clearGroup(key); pop.querySelector('.pop-body').innerHTML = groupBody(key, L(), 'p'); bindGroup(pop, null, true); update(); });
    if (focus) { const f = pop.querySelector('input:checked, input, button'); if (f) f.focus(); }
  }
  function closePop(silent) {
    const open = document.querySelector('.fbar .pop');
    if (!open) { st.pop = null; return; }
    const g = open.closest('.fgroup');
    open.remove();
    const t = g.querySelector('.ftrig'); t.setAttribute('aria-expanded', 'false');
    if (!silent) t.focus();
    st.pop = null;
  }
  let rebind = null;
  function bindGroup(scope, onStructure, isRebind) {
    if (onStructure) rebind = onStructure;
    const re = () => { if (rebind) rebind(); };
    scope.querySelectorAll('[data-area]').forEach((i) => i.addEventListener('change', () => { if (i.checked) st.areas.add(+i.dataset.area); else st.areas.delete(+i.dataset.area); update(); }));
    scope.querySelectorAll('[data-flag]').forEach((i) => i.addEventListener('change', () => { st[i.dataset.flag] = i.checked; update(); }));
    scope.querySelectorAll('[data-period]').forEach((i) => i.addEventListener('change', () => {
      st.period = i.value || null; st.from = ''; st.to = '';
      if (!st.period && (st.sort === 'priceAsc' || st.sort === 'priceDesc')) st.sort = 'updated';
      update(); re(); const sel = scope.querySelector('[data-period]:checked'); if (sel) sel.focus();
    }));
    scope.querySelectorAll('[data-range]').forEach((i) => i.addEventListener('input', () => {
      i.value = i.value.replace(/[^0-9]/g, '');
      st[i.dataset.range] = i.value; update();
      const wasBad = scope.querySelector('.field-error'); if (!!wasBad !== rangeBad()) re();
    }));
    scope.querySelectorAll('[data-sort]').forEach((i) => i.addEventListener('change', () => { st.sort = i.value; update(); }));
    scope.querySelectorAll('[data-stopnear]').forEach((b) => b.addEventListener('click', () => { st.near = null; closePop(); update(); }));
    void isRebind;
  }
  function clearGroup(key) {
    if (key === 'area') st.areas.clear();
    if (key === 'price') { st.period = null; st.from = ''; st.to = ''; if (st.sort.startsWith('price')) st.sort = 'updated'; }
    if (key === 'schedule') { st.openNow = st.evening = st.friday = false; }
    if (key === 'other') { st.verified = st.students = st.women = false; }
  }
  function clearAll() { ['area', 'price', 'schedule', 'other'].forEach(clearGroup); st.q = ''; const q = document.getElementById('dq'); if (q) q.value = ''; update(); }

  /* ---------- the phone sheet ---------- */
  function openSheet(focus) {
    const T = L(); const F = T.dir.filters;
    st.sheet = true;
    const el = document.createElement('div');
    el.className = 'fsheet'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-modal', 'true'); el.setAttribute('aria-labelledby', 'fsh');
    const render = () => {
      const { list } = filtered();
      el.innerHTML = `<div class="fsheet-head"><h2 id="fsh">${esc(F.title)}</h2><button type="button" class="icon-btn" data-x aria-label="${esc(F.close)}">${ic('x')}</button></div>
        <div class="fsheet-body"><p class="field-help" style="padding-top:12px">${esc(F.description)}</p>
        ${['area', 'price', 'schedule', 'other'].map((k) => `<section aria-labelledby="sh-${k}"><h3 id="sh-${k}">${esc(GROUP_LABEL(k, T))}</h3><div data-sbody="${k}">${groupBody(k, T, 's')}</div></section>`).join('')}</div>
        <div class="fsheet-foot"><button type="button" class="btn btn-secondary" data-sclear>${esc(F.clear)}</button><button type="button" class="btn btn-primary" data-x data-sheetshow>${esc(F.show(list.length))}</button></div>`;
      el.querySelectorAll('[data-x]').forEach((b) => b.addEventListener('click', close));
      el.querySelector('[data-sclear]').addEventListener('click', () => { clearAll(); render(); });
      el.querySelectorAll('[data-sbody]').forEach((b) => bindGroup(b, () => { const a = document.activeElement && document.activeElement.id; render(); if (a) { const x = document.getElementById(a); if (x) x.focus(); } }));
    };
    const close = () => { el.remove(); st.sheet = false; document.removeEventListener('keydown', key, true); const t = document.querySelector('[data-sheet]'); if (t) t.focus(); };
    const key = (e) => { if (e.key === 'Escape') close(); };
    document.addEventListener('keydown', key, true);
    render();
    document.body.appendChild(el);
    if (focus !== false) el.querySelector('[data-x]').focus();
  }

  function locate() {
    st.locating = true; update();
    setTimeout(() => { st.locating = false; st.near = RIMAL; update(); }, 700);
  }

  function bind(root) {
    const q = root.querySelector('#dq');
    q.addEventListener('input', () => { st.q = q.value; update(); });
    root.querySelectorAll('.fgroup').forEach((g) => g.addEventListener('click', (e) => {
      const t = e.target.closest('.ftrig'); if (!t) return;
      const key = g.dataset.group;
      if (st.pop === key) closePop(); else openPop(key, true);
    }));
    if (!bound) {
      bound = true;
      document.addEventListener('click', (e) => { if (st.pop && !e.target.closest('.fgroup')) closePop(true); });
      document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && st.pop) closePop(); });
    }
    root.querySelector('[data-sheet]').addEventListener('click', () => openSheet(true));
    root.querySelector('[data-near]').addEventListener('click', () => { if (st.near) { st.near = null; update(); } else locate(); });
    root.querySelectorAll('[data-view]').forEach((b) => b.addEventListener('click', () => setView(b.dataset.view)));
    document.querySelector('[data-flip]').addEventListener('click', () => setView(st.view === 'map' ? 'list' : 'map'));
    root.querySelectorAll('[data-zoom]').forEach((b) => b.addEventListener('click', () => { if (!map) return; const z = b.dataset.zoom; if (z === 'in') map.zoom(1.6); else if (z === 'out') map.zoom(1 / 1.6); else map.whole(); }));
  }
  function setView(v) {
    st.view = v;
    const u = new URL(location.href); if (v === 'map') u.searchParams.set('view', 'map'); else u.searchParams.delete('view');
    try { history.replaceState(null, '', u.href); } catch (e) { /* */ }
    if (map) { map.destroy(); map = null; }
    B.setLang(prefs.lang);
  }
  let lastRow = null;
  window.addEventListener('resize', () => { const r = rowMode(); if (lastRow !== null && r !== lastRow) update(); lastRow = r; });
})();
