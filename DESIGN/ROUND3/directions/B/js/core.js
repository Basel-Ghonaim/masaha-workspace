/* Direction B — core: preferences, helpers, data (with the Demo-states overlay), the Strip map, the shell,
   dialogs and the space card. Loaded in <head> after data.js, icons.js, copy.js; pages call B.page(). */
(function () {
  'use strict';
  const D = window.MASAHA_DATA;
  const Q = new URLSearchParams(location.search);
  const html = document.documentElement;
  const store = {
    get(k) { try { return localStorage.getItem('masaha.b.' + k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem('masaha.b.' + k, v); } catch (e) { /* storage blocked */ } },
  };
  const deviceDark = () => { try { return matchMedia('(prefers-color-scheme: dark)').matches; } catch (e) { return false; } };

  const prefs = {
    lang: ['ar', 'en'].includes(Q.get('lang')) ? Q.get('lang') : (['ar', 'en'].includes(store.get('lang')) ? store.get('lang') : 'ar'),
    themeChoice: ['light', 'dark'].includes(Q.get('theme')) ? Q.get('theme') : (['light', 'dark', 'system'].includes(store.get('theme')) ? store.get('theme') : 'system'),
    demo: Q.has('demo') ? Q.get('demo') === '1' : store.get('demo') === '1',
  };
  if (Q.get('lang')) store.set('lang', prefs.lang);
  if (Q.get('theme')) store.set('theme', prefs.themeChoice);
  if (Q.has('demo')) store.set('demo', prefs.demo ? '1' : '0');
  const theme = () => (prefs.themeChoice === 'system' ? (deviceDark() ? 'dark' : 'light') : prefs.themeChoice);
  function applyPrefs() {
    html.lang = prefs.lang;
    html.dir = prefs.lang === 'ar' ? 'rtl' : 'ltr';
    html.dataset.theme = theme();
  }
  applyPrefs();
  function syncAddress() {
    const u = new URL(location.href);
    u.searchParams.set('lang', prefs.lang);
    if (prefs.themeChoice === 'system') u.searchParams.delete('theme'); else u.searchParams.set('theme', prefs.themeChoice);
    try { history.replaceState(null, '', u.href); } catch (e) { /* file:// may refuse */ }
  }

  /* ---------- helpers ---------- */
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const ic = (name, cls) => `<svg class="ico${cls ? ' ' + cls : ''}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">${(window.ICONS || {})[name] || ''}</svg>`;
  const ltr = (s) => `<bdi dir="ltr">${s}</bdi>`;
  const L = () => window.COPY[prefs.lang];
  const loc = () => (prefs.lang === 'ar' ? 'ar-u-nu-latn' : 'en');
  const clock = (m) => `${String(Math.floor(m / 60)).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`;
  const WD = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
  function gaza(now) {
    const d = now || new Date();
    const p = {};
    new Intl.DateTimeFormat('en-US', { timeZone: 'Asia/Gaza', weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23', year: 'numeric', month: '2-digit', day: '2-digit' })
      .formatToParts(d).forEach((x) => { p[x.type] = x.value; });
    return { day: WD[p.weekday], minute: (+p.hour % 24) * 60 + +p.minute, ymd: `${p.year}-${p.month}-${p.day}`, date: d };
  }
  const NOW = gaza();
  const price = (agorot) => new Intl.NumberFormat(loc(), { style: 'currency', currency: 'ILS', minimumFractionDigits: agorot % 100 ? 2 : 0, maximumFractionDigits: agorot % 100 ? 2 : 0 }).format(agorot / 100);
  const num = (n, frac) => new Intl.NumberFormat(loc(), { maximumFractionDigits: frac || 0 }).format(n);
  function ago(iso) {
    if (!iso) return '';
    const day = (ymd) => { const [y, m, dd] = ymd.split('-').map(Number); return Date.UTC(y, m - 1, dd); };
    const then = gaza(new Date(iso)).ymd;
    const days = Math.round((day(NOW.ymd) - day(then)) / 86400000);
    return new Intl.RelativeTimeFormat(loc(), { numeric: 'auto' }).format(-days, 'day');
  }
  function km(a, b) {
    const R = 6371, r = Math.PI / 180;
    const dLat = (b.lat - a.lat) * r, dLng = (b.lng - a.lng) * r;
    const h = Math.sin(dLat / 2) ** 2 + Math.cos(a.lat * r) * Math.cos(b.lat * r) * Math.sin(dLng / 2) ** 2;
    return 2 * R * Math.asin(Math.sqrt(h));
  }
  let uidN = 0;
  const uid = () => 'u' + (++uidN);

  /* ---------- data: lookups, governorates, the demo overlay ---------- */
  const GOVS = D.lookups.governorates;
  const AREA = {};
  GOVS.forEach((g) => g.areas.forEach((a) => { AREA[a.id] = { ...a, gov: g }; }));
  const DEMO = {
    'branch-hub': 'AVAILABLE', 'focus-hub': 'FULL', 'garden-hub': 'AVAILABLE', 'number-one-hub': 'CLOSED', 'elevate-hub': 'AVAILABLE',
  };
  const openByHours = (days, t) => {
    if (!days) return null;
    const r = days[(t || NOW).day];
    if (!r) return false;
    const m = (t || NOW).minute;
    return m >= r.opensMinute && m < r.closesMinute;
  };
  function stateOf(sp) {
    const T = L();
    const byHours = openByHours(sp.days);
    if (sp.verified) {
      if (!sp.live) return { kind: 'none', word: T.dir.status.none, source: 'unset', open: !!byHours };
      if (byHours === false || sp.live === 'CLOSED') return { kind: 'closed', word: T.terms.closedNow, source: 'live', open: false };
      if (sp.live === 'FULL') return { kind: 'full', word: T.terms.full, source: 'live', open: true };
      return { kind: 'available', word: T.terms.available, source: 'live', open: true };
    }
    if (byHours === null) return { kind: 'none', word: T.dir.status.none, source: 'unverified', open: false };
    return byHours ? { kind: 'open', word: T.dir.status.open, source: 'hours', open: true } : { kind: 'shut', word: T.dir.status.closed, source: 'hours', open: false };
  }
  function todayText(days) {
    const T = L().dir.card;
    if (!days) return T.noHours;
    const r = days[NOW.day];
    if (!r) return T.closedToday;
    if (r.opensMinute === 0 && r.closesMinute === 1440) return T.openAllDay;
    return T.today(ltr(`${clock(r.opensMinute)}–${clock(r.closesMinute)}`));
  }
  function spaces() {
    const en = prefs.lang === 'en';
    return D.spaces.map((s, i) => {
      const det = D.details[s.slug];
      const demoLive = prefs.demo ? DEMO[s.slug] : undefined;
      const verified = demoLive ? true : s.isVerified;
      const a = AREA[s.area.id];
      const sp = {
        slug: s.slug, order: i,
        name: en ? s.nameEn : (s.nameAr || s.nameEn),
        otherName: en ? s.nameAr : (s.nameAr && s.nameEn !== s.nameAr ? s.nameEn : null),
        nameAr: s.nameAr, nameEn: s.nameEn,
        areaId: s.area.id, area: en ? s.area.nameEn : s.area.nameAr,
        govId: a ? a.gov.id : null, gov: a ? (en ? a.gov.nameEn : a.gov.nameAr) : '',
        verified, live: demoLive || (verified ? s.liveStatus : null),
        days: s.days, worksEvenings: s.worksEvenings, womensHall: s.womensHall,
        cover: s.cover, location: s.location, detail: det,
        prices: det ? det.prices : [],
        announcement: prefs.demo && s.slug === 'branch-hub',
      };
      sp.place = sp.area === sp.gov || !sp.gov ? sp.area : `${sp.area} · ${sp.gov}`;
      sp.state = stateOf(sp);
      sp.today = todayText(sp.days);
      sp.openByHours = openByHours(sp.days);
      return sp;
    });
  }
  const govName = (g) => (prefs.lang === 'en' ? g.nameEn : g.nameAr);
  const areaName = (a) => (prefs.lang === 'en' ? a.nameEn : a.nameAr);

  /* ---------- the Strip: geometry and the map ---------- */
  /* the lead's outline (../_shared/data/strip-outline.json): north-west corner, the coast to Rafah, the Egyptian
     border, the eastern border back north; closed (its last point repeats the first) */
  const OUTLINE = D.outline.slice(0, -1);
  const COAST = OUTLINE.slice(0, 10);
  const SEA = [[33, 33], [33, 35.2], [31.95, 34.75], [31.70, 34.585]].concat(COAST, [[31.27, 34.13], [31.10, 33.70], [30, 33.2], [30, 33]]);
  const CONTOURS = [[0.010, -0.012], [0.024, -0.029], [0.044, -0.053]];
  /* governorate boundaries, each a line from a coast point to a border point (approximate, schematic) */
  const CUTS = [
    { c: [31.70, 34.45], e: [31.66, 34.62] },
    { c: [31.556, 34.4595], e: [31.528, 34.518] },
    { c: [31.468, 34.383], e: [31.430, 34.4234] },
    { c: [31.385, 34.288], e: [31.345, 34.3705] },
    { c: [31.325, 34.226], e: [31.285, 34.319] },
    { c: [31.15, 34.12], e: [31.10, 34.36] },
  ];
  const BANDS = [1, 2, 3, 4, 'rafah'];
  const BAND_ANCHOR = { 1: [31.571, 34.516], 2: [31.488, 34.447], 3: [31.410, 34.362], 4: [31.338, 34.300], rafah: [31.272, 34.268] };
  const BAND_EAST = { 1: [31.570, 34.553], 2: [31.478, 34.470], 3: [31.400, 34.406], 4: [31.318, 34.349], rafah: [31.258, 34.296] };
  const STRIP_BOUNDS = { s: 31.22, n: 31.5944, w: 34.219, e: 34.564 };
  const GAZA_CITY = { lat: 31.5225, lng: 34.4475 };
  const INSET_C = { lat: 31.5235, lng: 34.4405 };
  const K = Math.cos(31.4 * Math.PI / 180);

  function fit(w, h, b, pad, box) {
    const bx = box || [0, 0, w, h];
    const p = pad == null ? 24 : pad;
    const s = Math.min((bx[2] - 2 * p) / ((b.e - b.w) * K), (bx[3] - 2 * p) / (b.n - b.s));
    const lat = (b.n + b.s) / 2, lng = (b.e + b.w) / 2;
    // shift the centre so the bounds sit in the middle of the box
    const cx = bx[0] + bx[2] / 2, cy = bx[1] + bx[3] / 2;
    return { lat: lat + (cy - h / 2) / s, lng: lng - (cx - w / 2) / (K * s), s, w, h };
  }
  const P = (v, lat, lng) => [v.w / 2 + (lng - v.lng) * K * v.s, v.h / 2 - (lat - v.lat) * v.s];
  const U = (v, x, y) => ({ lat: v.lat - (y - v.h / 2) / v.s, lng: v.lng + (x - v.w / 2) / (K * v.s) });
  const f1 = (n) => Math.round(n * 10) / 10;
  const path = (v, pts, close) => pts.map((p, i) => { const [x, y] = P(v, p[0], p[1]); return (i ? 'L' : 'M') + f1(x) + ' ' + f1(y); }).join('') + (close === false ? '' : 'Z');
  function bandPoly(i) {
    const a = CUTS[i], b = CUTS[i + 1];
    const ext = (cut, k) => [cut.c[0] + (cut.c[0] - cut.e[0]) * k, cut.c[1] + (cut.c[1] - cut.e[1]) * k];
    const extE = (cut, k) => [cut.e[0] + (cut.e[0] - cut.c[0]) * k, cut.e[1] + (cut.e[1] - cut.c[1]) * k];
    return [ext(a, 0.8), extE(a, 0.8), extE(b, 0.8), ext(b, 0.8)];
  }
  function groundLayers(v, id, o) {
    const opt = o || {};
    let s = `<rect class="land-out" x="-10" y="-10" width="${v.w + 20}" height="${v.h + 20}"/>`;
    s += `<path class="sea" d="${path(v, SEA)}"/>`;
    CONTOURS.forEach(([dLat, dLng], i) => {
      const pts = [[31.95, 34.75], [31.70, 34.585]].concat(COAST, [[31.27, 34.13], [31.10, 33.70]]).map((p) => [p[0] + dLat, p[1] + dLng]);
      s += `<path class="sea-line" style="opacity:${1 - i * 0.28}" d="${path(v, pts, false)}"/>`;
    });
    s += `<clipPath id="${id}-c"><path d="${path(v, OUTLINE)}"/></clipPath><g clip-path="url(#${id}-c)">`;
    BANDS.forEach((g, i) => {
      const cls = ['band'];
      if (i % 2) cls.push('alt');
      if (opt.ink === g) cls.push('ink');
      s += `<path class="${cls.join(' ')}" data-gov="${g}" style="animation-delay:${i * 100}ms" d="${path(v, bandPoly(i))}"/>`;
    });
    CUTS.slice(1, 5).forEach((c, i) => { s += `<path class="band-line" style="animation-delay:${(i + 1) * 100}ms" d="${path(v, [c.c, c.e], false)}"/>`; });
    s += `</g><path class="edge" d="${path(v, OUTLINE)}"/>`;
    return s;
  }
  /* a pin: open = spark fill; full = amber with a bar; closed = hollow; none = dashed hollow */
  function pinSvg(x, y, kind, r) {
    let s = `<circle class="pin k-${kind}" cx="${f1(x)}" cy="${f1(y)}" r="${r}"/>`;
    if (kind === 'full') s += `<rect class="pin-bar" x="${f1(x - r * 0.55)}" y="${f1(y - 1)}" width="${f1(r * 1.1)}" height="2" rx="1"/>`;
    return s;
  }
  const KIND_ORDER = { none: 0, shut: 1, closed: 1, full: 2, open: 3, available: 3 };

  /** A silhouette of the Strip (no sea): for thumbnails, the footer, a no-photo frame. */
  function silhouette(o) {
    const w = o.w, h = o.h;
    const v = fit(w, h, STRIP_BOUNDS, o.pad == null ? 2 : o.pad);
    const id = uid();
    let s = `<svg class="mapsvg${o.cls ? ' ' + o.cls : ''}" viewBox="0 0 ${w} ${h}" width="${o.dw || w}" height="${o.dh || h}" aria-hidden="true" focusable="false">`;
    if (o.ink != null) {
      s += `<clipPath id="${id}-c"><path d="${path(v, OUTLINE)}"/></clipPath><g clip-path="url(#${id}-c)">`;
      BANDS.forEach((g, i) => { s += `<path class="${g === o.ink ? 'silh-ink' : 'silh'}" d="${path(v, bandPoly(i))}"/>`; });
      s += '</g>';
    } else {
      s += `<path class="silh" d="${path(v, OUTLINE)}"/>`;
    }
    if (o.dot) { const [x, y] = P(v, o.dot.lat, o.dot.lng); s += `<circle class="silh-dot" cx="${f1(x)}" cy="${f1(y)}" r="${o.dotR || 5}"/>`; }
    return s + '</svg>';
  }

  /**
   * The map. mode 'mark': a still drawing (Home, About, sign-in, 404) with optional callout labels and a Gaza City
   * inset; mode 'work': the directory's map (zoom, pan, clusters, select). Re-renders on resize.
   */
  function stripMap(el, opts) {
    const o = Object.assign({ mode: 'mark', pins: [], labels: 'none', inset: false, pad: 24, draw: false }, opts);
    const id = uid();
    let view = null, w = 0, h = 0, sel = o.selected || null, raised = null, you = o.you || null, drawn = false;
    function base() { return fit(w, h, STRIP_BOUNDS, o.pad, o.box ? o.box(w, h) : null); }
    function pinsView() {
      const b = { s: Math.min(...o.pins.map((p) => p.lat)), n: Math.max(...o.pins.map((p) => p.lat)), w: Math.min(...o.pins.map((p) => p.lng)), e: Math.max(...o.pins.map((p) => p.lng)) };
      const m = 0.025; b.s -= m; b.n += m; b.w -= m; b.e += m;
      return clampView(fit(w, h, b, 32));
    }
    function pinsAt(v) {
      return o.pins.map((p) => { const [x, y] = P(v, p.lat, p.lng); return Object.assign({ x, y }, p); })
        .sort((a, b) => (KIND_ORDER[a.kind] || 0) - (KIND_ORDER[b.kind] || 0));
    }
    function labelText(cls, x, y, text, anchorEnd) {
      const rtl = prefs.lang === 'ar';
      const anchor = anchorEnd ? (rtl ? 'start' : 'end') : (rtl ? 'end' : 'start');
      return `<text class="${cls}" x="${f1(x)}" y="${f1(y)}" direction="${rtl ? 'rtl' : 'ltr'}" text-anchor="${anchor}">${esc(text)}</text>`;
    }
    function render() {
      w = el.clientWidth; h = el.clientHeight;
      if (!w || !h) return;
      if (!view || o.mode !== 'work') view = o.mode === 'work' && o.initial === 'pins' && o.pins.length > 1 ? pinsView() : base();
      const v = view;
      const T = L();
      let s = `<svg class="mapsvg map-abs${o.draw && !drawn ? ' draw' : ''}" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" role="${o.mode === 'work' || o.labels === 'callout' ? 'group' : 'img'}" aria-label="${esc(o.label || T.home.onMap)}">`;
      s += groundLayers(v, id, { ink: o.ink });
      const pins = pinsAt(v);
      let inset = null;
      if (o.inset) {
        const R = Math.max(64, Math.min(140, Math.min(w, h) * 0.18));
        const zoom = o.insetZoom || 3.4;
        const [gx, gy] = P(v, GAZA_CITY.lat, GAZA_CITY.lng);
        let [ix, iy] = o.insetAt ? o.insetAt(v, R) : P(v, 31.60, 34.32);
        ix = Math.max(R + 12, Math.min(w - R - 12, ix)); iy = Math.max(R + 12, Math.min(h - R - 12, iy));
        const r0 = R / zoom + 6;
        inset = { R, zoom, gx, gy, ix, iy, r0 };
      }
      // governorate labels
      if (o.labels === 'inside') {
        s += '<g class="gov-labels" aria-hidden="true">';
        BANDS.forEach((g) => {
          if (o.mode === 'work' && v.s > base().s * 3.2) return;
          const [x, y] = P(v, BAND_ANCHOR[g][0], BAND_ANCHOR[g][1]);
          const name = g === 'rafah' ? T.geo.rafah : govName(GOVS.find((x2) => x2.id === g));
          s += `<text class="glabel" x="${f1(x)}" y="${f1(y)}" text-anchor="middle" direction="${prefs.lang === 'ar' ? 'rtl' : 'ltr'}">${esc(name)}</text>`;
        });
        s += '</g>';
      }
      // pins
      s += '<g class="pins">';
      if (o.mode === 'work') {
        const clusters = [];
        pins.forEach((p) => {
          const c = clusters.find((k) => Math.hypot(k.x - p.x, k.y - p.y) < 26);
          if (c) c.items.push(p); else clusters.push({ x: p.x, y: p.y, items: [p] });
        });
        clusters.forEach((c) => {
          if (c.items.length === 1) {
            const p = c.items[0];
            const isSel = p.slug === sel;
            const r = isSel ? 12 : 7;
            s += `<g class="pin-g${isSel ? ' sel' : ''}${p.slug === raised ? ' raised' : ''}" data-slug="${p.slug}">`;
            if (isSel) s += `<circle class="sel-ring" cx="${f1(p.x)}" cy="${f1(p.y)}" r="${r + 3}"/>`;
            s += pinSvg(p.x, p.y, p.kind, r);
            s += `<circle class="focus-ring" cx="${f1(p.x)}" cy="${f1(p.y)}" r="${r + 6}"/>`;
            s += `<circle class="hit" cx="${f1(p.x)}" cy="${f1(p.y)}" r="22" tabindex="0" role="button" aria-pressed="${isSel}" aria-label="${esc(T.dir.map.pin(p.name, p.word))}" data-slug="${p.slug}"/>`;
            s += '</g>';
          } else {
            const open = c.items.some((p) => p.kind === 'open' || p.kind === 'available');
            const hasSel = c.items.some((p) => p.slug === sel);
            const hasRaised = c.items.some((p) => p.slug === raised);
            const cx = c.items.reduce((a, p) => a + p.x, 0) / c.items.length, cy = c.items.reduce((a, p) => a + p.y, 0) / c.items.length;
            c.cx = cx; c.cy = cy;
            s += `<g class="cluster pin-g${hasSel ? ' sel' : ''}${hasRaised ? ' raised' : ''}">`;
            if (hasSel) s += `<circle class="c-sel" cx="${f1(cx)}" cy="${f1(cy)}" r="21"/>`;
            s += `<circle class="c" cx="${f1(cx)}" cy="${f1(cy)}" r="15"/>`;
            if (open && !hasSel) s += `<circle class="c-open" cx="${f1(cx)}" cy="${f1(cy)}" r="19"/>`;
            s += `<text x="${f1(cx)}" y="${f1(cy + 4.5)}" text-anchor="middle">${num(c.items.length)}</text>`;
            s += `<circle class="focus-ring" cx="${f1(cx)}" cy="${f1(cy)}" r="24"/>`;
            s += `<circle class="hit" cx="${f1(cx)}" cy="${f1(cy)}" r="24" tabindex="0" role="button" aria-label="${esc(T.dir.map.cluster(c.items.length))}" data-cluster="${c.items.map((p) => p.slug).join(',')}"/>`;
            s += '</g>';
          }
        });
        if (you) {
          const [x, y] = P(v, you.lat, you.lng);
          s += `<circle class="you-halo" cx="${f1(x)}" cy="${f1(y)}" r="18"/><circle class="you" cx="${f1(x)}" cy="${f1(y)}" r="7"><title>${esc(T.dir.map.you)}</title></circle>`;
        }
        // the selected space's name, in a tag
        const sp = sel && pins.find((p) => p.slug === sel);
        if (sp) {
          const c = clusters.find((k) => k.items.includes(sp));
          const tx = c.items.length > 1 ? c.cx : sp.x, ty = (c.items.length > 1 ? c.cy - 26 : sp.y - 20);
          s += `<g class="tag" aria-hidden="true"><rect rx="8" ry="8" fill="var(--surface)" stroke="var(--border-strong)"/><text x="${f1(tx)}" y="${f1(ty - 8)}" text-anchor="middle" direction="${prefs.lang === 'ar' ? 'rtl' : 'ltr'}" style="font:500 14px var(--font-text);fill:var(--text)">${esc(sp.name)}</text></g>`;
        }
      } else {
        const r = o.pinR || (w < 500 ? 5 : 6.5);
        pins.forEach((p) => {
          if (inset && Math.hypot(p.x - inset.gx, p.y - inset.gy) < inset.r0 - 4) return;
          s += pinSvg(p.x, p.y, p.kind, r);
        });
      }
      s += '</g>';
      // the Gaza City inset
      if (inset) {
        const vi = { lat: INSET_C.lat, lng: INSET_C.lng, s: v.s * inset.zoom, w: inset.R * 2, h: inset.R * 2 };
        const ox = inset.ix - inset.R, oy = inset.iy - inset.R;
        const d = Math.hypot(inset.ix - inset.gx, inset.iy - inset.gy) || 1;
        const ux = (inset.ix - inset.gx) / d, uy = (inset.iy - inset.gy) / d;
        s += `<g class="inset-g"><circle class="inset-ring" cx="${f1(inset.gx)}" cy="${f1(inset.gy)}" r="${f1(inset.r0)}"/>`;
        s += `<path class="leader" d="M${f1(inset.gx + ux * inset.r0)} ${f1(inset.gy + uy * inset.r0)}L${f1(inset.ix - ux * inset.R)} ${f1(inset.iy - uy * inset.R)}"/>`;
        s += `<clipPath id="${id}-i"><circle cx="${f1(inset.ix)}" cy="${f1(inset.iy)}" r="${f1(inset.R)}"/></clipPath>`;
        s += `<g clip-path="url(#${id}-i)"><g transform="translate(${f1(ox)} ${f1(oy)})">${groundLayers(vi, id + 'i', {})}`;
        const byArea = {};
        o.pins.forEach((p) => { if (p.areaId == null || !AREA[p.areaId] || AREA[p.areaId].gov.id !== 2) return; (byArea[p.areaId] = byArea[p.areaId] || []).push(p); });
        Object.keys(byArea).forEach((aid) => {
          const ps = byArea[aid]; const lat = ps.reduce((a, p) => a + p.lat, 0) / ps.length, lng = ps.reduce((a, p) => a + p.lng, 0) / ps.length;
          if (inset.R < 100) return;
          const ex = ps.map((p) => P(vi, p.lat, p.lng));
          const side = { 2: 'w', 3: 'n', 9: 's' }[aid] || 's';
          let x, y, anchor = 'middle';
          if (side === 'w') { x = Math.min(...ex.map((q) => q[0])) - 12; y = ex.reduce((a, q) => a + q[1], 0) / ex.length + 4; anchor = 'end'; }
          else if (side === 'e') { x = Math.max(...ex.map((q) => q[0])) + 12; y = ex.reduce((a, q) => a + q[1], 0) / ex.length + 4; anchor = 'start'; }
          else if (side === 'n') { x = ex.reduce((a, q) => a + q[0], 0) / ex.length; y = Math.min(...ex.map((q) => q[1])) - 12; }
          else { x = ex.reduce((a, q) => a + q[0], 0) / ex.length; y = Math.max(...ex.map((q) => q[1])) + 20; }
          void lat; void lng;
          if (prefs.lang === 'ar' && anchor !== 'middle') anchor = anchor === 'end' ? 'start' : 'end';
          s += `<text class="alabel" x="${f1(x)}" y="${f1(y)}" text-anchor="${anchor}" direction="${prefs.lang === 'ar' ? 'rtl' : 'ltr'}">${esc(areaName(AREA[aid]))}</text>`;
        });
        pinsAt(vi).forEach((p) => { s += pinSvg(p.x, p.y, p.kind, o.pinR ? o.pinR + 1 : 7); });
        s += `</g></g><circle class="inset-edge" cx="${f1(inset.ix)}" cy="${f1(inset.iy)}" r="${f1(inset.R)}"/></g>`;
      }
      // callout labels: the governorates named along the Strip, at its eastern edge
      if (o.labels === 'callout') {
        s += '<g class="gov-labels">';
        const counts = o.counts || {};
        BANDS.forEach((g) => {
          const [ex, ey] = P(v, BAND_EAST[g][0], BAND_EAST[g][1]);
          const lx = ex + (o.calloutGap || 36);
          const name = g === 'rafah' ? T.geo.rafah : govName(GOVS.find((x2) => x2.id === g));
          const count = g === 'rafah' ? '' : T.home.count(counts[g] || 0);
          s += `<path class="callout" d="M${f1(ex + 3)} ${f1(ey)}H${f1(lx - 6)}"/>`;
          if (g === 'rafah') {
            s += `<g class="glink geo" aria-hidden="true"><rect class="gl-bg"/>${labelText('gl-name geo', lx, ey + 5, name)}</g>`;
          } else {
            s += `<a class="glink" href="spaces.html?gov=${g}" data-gov="${g}" aria-label="${esc(T.home.line(name, count))}"><rect class="gl-bg" rx="10" ry="10"/>${labelText('gl-name', lx, ey - 2, name)}${labelText('gl-count', lx, ey + 16, count)}</a>`;
          }
        });
        s += '</g>';
      }
      s += '</svg>';
      el.innerHTML = s;
      drawn = true;
      after();
    }
    function after() {
      const svg = el.querySelector('svg');
      svg.querySelectorAll('.tag').forEach((g) => {
        const t = g.querySelector('text'); const b = t.getBBox();
        const r = g.querySelector('rect');
        r.setAttribute('x', f1(b.x - 10)); r.setAttribute('y', f1(b.y - 4)); r.setAttribute('width', f1(b.width + 20)); r.setAttribute('height', f1(b.height + 8));
      });
      svg.querySelectorAll('.glink').forEach((a) => {
        const texts = a.querySelectorAll('text'); if (!texts.length) return;
        let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
        texts.forEach((t) => { const b = t.getBBox(); x0 = Math.min(x0, b.x); y0 = Math.min(y0, b.y); x1 = Math.max(x1, b.x + b.width); y1 = Math.max(y1, b.y + b.height); });
        const r = a.querySelector('rect');
        r.setAttribute('x', f1(x0 - 8)); r.setAttribute('y', f1(y0 - 5)); r.setAttribute('width', f1(x1 - x0 + 16)); r.setAttribute('height', f1(Math.max(44, y1 - y0 + 10)));
        if (y1 - y0 + 10 < 44) r.setAttribute('y', f1((y0 + y1) / 2 - 22));
        const g = a.dataset.gov;
        if (!g) return;
        const on = () => svg.querySelectorAll(`.band[data-gov="${g}"]`).forEach((b) => b.classList.add('hl'));
        const off = () => svg.querySelectorAll('.band.hl').forEach((b) => b.classList.remove('hl'));
        a.addEventListener('mouseenter', on); a.addEventListener('mouseleave', off);
        a.addEventListener('focus', on); a.addEventListener('blur', off);
      });
      if (o.mode === 'work') wire(svg);
    }
    /* work mode: select, zoom, pan */
    let drag = null;
    function wire(svg) {
      svg.querySelectorAll('.hit').forEach((hEl) => {
        const act = () => {
          if (hEl.dataset.cluster) {
            const slugs = hEl.dataset.cluster.split(',');
            const pts = o.pins.filter((p) => slugs.includes(p.slug));
            const b = { s: Math.min(...pts.map((p) => p.lat)), n: Math.max(...pts.map((p) => p.lat)), w: Math.min(...pts.map((p) => p.lng)), e: Math.max(...pts.map((p) => p.lng)) };
            const pad = 0.004; b.s -= pad; b.n += pad; b.w -= pad; b.e += pad;
            const nv = fit(w, h, b, 48);
            view = clampView(Object.assign(nv, { s: Math.min(nv.s, view.s * 4) }));
            render();
            const first = el.querySelector('.hit'); if (first && document.activeElement === document.body) first.focus();
          } else {
            sel = hEl.dataset.slug === sel ? null : hEl.dataset.slug;
            render();
            const again = el.querySelector(`.hit[data-slug="${hEl.dataset.slug}"]`); if (again) again.focus();
            if (o.onSelect) o.onSelect(sel);
          }
        };
        hEl.addEventListener('click', (e) => { e.stopPropagation(); if (!moved) act(); });
        hEl.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); act(); } });
      });
      svg.addEventListener('pointerdown', (e) => {
        if (e.target.classList.contains('hit')) { moved = false; return; }
        drag = { x: e.clientX, y: e.clientY, v: Object.assign({}, view) }; moved = false;
        svg.setPointerCapture(e.pointerId);
      });
      svg.addEventListener('pointermove', (e) => {
        if (!drag) return;
        const dx = e.clientX - drag.x, dy = e.clientY - drag.y;
        if (Math.abs(dx) + Math.abs(dy) > 3) moved = true;
        if (!moved) return;
        view = clampView(Object.assign({}, drag.v, { lat: drag.v.lat + dy / drag.v.s, lng: drag.v.lng - dx / (K * drag.v.s) }));
        if (!raf) raf = requestAnimationFrame(() => { raf = 0; render(); });
      });
      svg.addEventListener('pointerup', () => {
        const wasMoved = moved; drag = null;
        if (!wasMoved && sel) { /* a click on the ground clears the selection */ }
        setTimeout(() => { moved = false; }, 0);
      });
      svg.addEventListener('click', (e) => { if (!e.target.classList.contains('hit') && !moved && sel) { sel = null; render(); if (o.onSelect) o.onSelect(null); } });
      svg.addEventListener('wheel', (e) => {
        e.preventDefault();
        const r = svg.getBoundingClientRect();
        zoomAt(e.deltaY < 0 ? 1.4 : 1 / 1.4, e.clientX - r.left, e.clientY - r.top);
      }, { passive: false });
    }
    let moved = false, raf = 0;
    function clampView(nv) {
      const b0 = base();
      nv.s = Math.max(b0.s, Math.min(b0.s * 14, nv.s));
      const m = 0.02;
      nv.lat = Math.max(STRIP_BOUNDS.s - m, Math.min(STRIP_BOUNDS.n + m, nv.lat));
      nv.lng = Math.max(STRIP_BOUNDS.w - m, Math.min(STRIP_BOUNDS.e + m, nv.lng));
      if (nv.s === b0.s) { nv.lat = b0.lat; nv.lng = b0.lng; }
      nv.w = w; nv.h = h;
      return nv;
    }
    function zoomAt(f, x, y) {
      const before = U(view, x, y);
      const nv = Object.assign({}, view, { s: view.s * f });
      const after = U(nv, x, y);
      nv.lat += before.lat - after.lat; nv.lng += before.lng - after.lng;
      view = clampView(nv);
      render();
    }
    const ro = new ResizeObserver(() => { if (el.clientWidth !== w || el.clientHeight !== h) { if (view && o.mode === 'work') { const keep = view; view = null; w = el.clientWidth; h = el.clientHeight; const b0 = base(); view = keep.s <= b0.s * 1.001 ? b0 : clampView(Object.assign({}, keep)); } render(); } });
    ro.observe(el);
    render();
    return {
      render,
      zoom(f) { zoomAt(f, w / 2, h / 2); },
      whole() { view = base(); render(); },
      select(slug, focusIt) {
        sel = slug;
        if (slug) {
          const p = o.pins.find((x) => x.slug === slug);
          if (p) { const [x, y] = P(view, p.lat, p.lng); if (x < 40 || y < 40 || x > w - 40 || y > h - 140) { view = clampView(Object.assign({}, view, { lat: p.lat - 40 / view.s, lng: p.lng })); } }
        }
        render();
        if (focusIt) { const t = el.querySelector(`.hit[data-slug="${slug}"]`); if (t) t.focus(); }
      },
      raise(slug) { raised = slug; el.querySelectorAll('.pin-g').forEach((g) => { const hit = g.querySelector('.hit'); const slugs = hit ? (hit.dataset.slug ? [hit.dataset.slug] : (hit.dataset.cluster || '').split(',')) : []; g.classList.toggle('raised', !!slug && slugs.includes(slug)); }); },
      setPins(p) { o.pins = p; render(); },
      setYou(pt) { you = pt; render(); },
      destroy() { ro.disconnect(); },
    };
  }

  /* ---------- dialogs and toasts ---------- */
  function dialog(htmlInner, opts) {
    const back = document.createElement('div');
    back.className = 'dialog-back';
    const tid = uid();
    back.innerHTML = `<div class="dialog" role="dialog" aria-modal="true" aria-labelledby="${tid}">${htmlInner.replace('%ID%', tid)}</div>`;
    const prev = document.activeElement;
    document.body.appendChild(back);
    const box = back.querySelector('.dialog');
    const focusables = () => [...box.querySelectorAll('a[href],button,input,select,textarea,[tabindex]:not([tabindex="-1"])')];
    const close = () => { back.remove(); document.removeEventListener('keydown', key, true); if (prev && prev.focus) prev.focus(); };
    const key = (e) => {
      if (e.key === 'Escape') { e.preventDefault(); close(); }
      if (e.key === 'Tab') {
        const f = focusables(); if (!f.length) return;
        if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
      }
    };
    document.addEventListener('keydown', key, true);
    back.addEventListener('click', (e) => { if (e.target === back) close(); });
    box.querySelectorAll('[data-close]').forEach((b) => b.addEventListener('click', close));
    const first = (opts && opts.focus && box.querySelector(opts.focus)) || focusables()[0];
    if (first) first.focus();
    return { close, box };
  }
  function signInPrompt(kind) {
    const T = L().site.signInPrompt;
    const k = T[kind];
    dialog(`<div class="dialog-head"><h2 id="%ID%">${esc(k.title)}</h2><button class="icon-btn" data-close aria-label="${esc(T.close)}">${ic('x')}</button></div>
      <p class="muted">${esc(k.text)}</p>
      <div class="dialog-actions"><a class="btn btn-primary" href="login.html">${esc(T.signIn)}</a><a class="btn btn-secondary" href="404.html">${esc(T.register)}</a></div>`);
  }
  let toastT = 0;
  function toast(text, action) {
    document.querySelectorAll('.toast').forEach((t) => t.remove());
    const t = document.createElement('div');
    t.className = 'toast'; t.setAttribute('role', 'status');
    t.innerHTML = `<span>${esc(text)}</span>${action ? `<button type="button">${esc(action.label)}</button>` : ''}`;
    document.body.appendChild(t);
    if (action) t.querySelector('button').addEventListener('click', () => { t.remove(); action.run(); });
    clearTimeout(toastT); toastT = setTimeout(() => t.remove(), 5000);
  }

  /* real interior photos fill their frame; every other cover is the space's own poster and sits whole on a mat */
  const REAL_PHOTOS = new Set(['coma-io-1', 'branch-hub-2', 'branch-hub-3']);
  const isPoster = (src) => !!src && !REAL_PHOTOS.has(String(src).split('/').pop().replace(/-(card|page)\.webp$/, ''));
  const frameCls = (src) => (isPoster(src) ? ' mat' : '');

  /* ---------- the space card: the photo is the frame; the facts sit on the ground ---------- */
  function card(sp, o) {
    const opt = o || {};
    const T = L();
    const hl = opt.level || 3;
    const photo = opt.noPhoto || !sp.cover
      ? `<div class="nophoto">${silhouette({ w: 120, h: 150, dot: sp.location, dotR: 6, pad: 4 })}<span class="np-area">${esc(sp.area)}</span></div>`
      : `<img src="${esc(sp.cover)}" alt="" loading="lazy" width="400" height="300">`;
    const extra = [];
    if (sp.verified) extra.push(`<span class="verified">${ic('badge-check', 'ico-16')}${esc(T.dir.card.verified)}</span>`);
    if (opt.distance != null) extra.push(`<span>${esc(T.dir.card.distance(num(opt.distance, opt.distance < 10 ? 1 : 0)))}</span>`);
    if (opt.price) extra.push(`<b>${opt.price}</b>`);
    const saved = !!opt.saved;
    return `<article class="card${opt.row ? ' row' : ''}${opt.sel ? ' sel' : ''}" data-slug="${sp.slug}">
      <div class="card-photo${opt.noPhoto ? '' : frameCls(sp.cover)}">${photo}</div>
      <div class="card-body">
        <div class="card-top"><h${hl} class="card-name"><a href="space.html?slug=${sp.slug}">${esc(sp.name)}</a></h${hl}>
          <button type="button" class="icon-btn heart" aria-pressed="${saved}" aria-label="${esc(saved ? T.favorites.remove(sp.name) : T.favorites.save(sp.name))}" data-heart="${sp.slug}">${ic('heart')}</button></div>
        <p class="card-place">${esc(sp.place)}</p>
        <p class="card-facts"><span class="state k-${sp.state.kind}"><span class="dot k-${sp.state.kind}"></span>${esc(sp.state.word)}</span><span class="today">${sp.today}</span></p>
        ${extra.length ? `<p class="card-extra">${extra.join('')}</p>` : ''}
      </div>
    </article>`;
  }
  function wireHearts(root, onToggle) {
    root.querySelectorAll('[data-heart]').forEach((b) => b.addEventListener('click', (e) => {
      e.preventDefault(); e.stopPropagation();
      if (onToggle) onToggle(b.dataset.heart, b); else signInPrompt('favorite');
    }));
  }

  /* ---------- the shell ---------- */
  const USER = { name: 'سلمى الأغا', nameEn: 'Salma Al-Agha', email: 'demo-user@example.com' };
  function header(def) {
    const T = L();
    const S = T.site;
    const cur = def.nav;
    const navLinks = [['home', 'home.html'], ['spaces', 'spaces.html'], ['about', 'about.html']]
      .map(([k, href]) => `<a href="${href}"${cur === k ? ' aria-current="page"' : ''}>${esc(S.links[k])}</a>`).join('');
    const themeLabel = S.switchTheme[theme()];
    const userName = USER.name;
    const account = def.account
      ? `<button type="button" class="user-btn wide-only" data-act="user" aria-haspopup="true" aria-expanded="false" aria-label="${esc(T.users.menu(userName))}"><span>${esc(userName.split(' ')[0])}</span><span class="avatar" aria-hidden="true">${esc(userName[0])}</span></button>`
      : `<a class="btn btn-secondary btn-sm wide-only" href="login.html"${def.key === 'login' ? ' aria-current="page"' : ''}>${ic('log-in', 'dir')}${esc(S.signIn)}</a>`;
    return `<a class="skip" href="#main">${esc(S.skip)}</a>
    <header class="hdr${def.headerOnMap ? ' on-map' : ''}"><div class="wrap hdr-in">
      <a class="logo" href="home.html"><img class="lg-light" src="../_shared/logo/masaha-logo-berry.svg" alt="${esc(S.wordmark)}" width="110" height="40"><img class="lg-dark" src="../_shared/logo/masaha-logo-dark-berry.svg" alt="${esc(S.wordmark)}" width="110" height="40"></a>
      <nav class="nav" aria-label="${esc(S.navigation)}">${navLinks}</nav>
      <div class="hdr-actions">
        <button type="button" class="btn btn-quiet btn-sm lang-btn wide-only" data-act="lang" lang="${prefs.lang === 'ar' ? 'en' : 'ar'}">${ic('languages')}${esc(S.otherLanguage)}</button>
        <button type="button" class="icon-btn wide-only" data-act="theme" aria-label="${esc(themeLabel)}" title="${esc(themeLabel)}">${ic(theme() === 'dark' ? 'sun' : 'moon')}</button>
        ${account}
        <button type="button" class="icon-btn menu-btn" data-act="menu" aria-label="${esc(S.menu)}" aria-expanded="false">${ic('menu')}</button>
      </div>
    </div></header>`;
  }
  function footer() {
    const S = L().site;
    return `<footer class="ftr"><div class="wrap"><div class="ftr-in">
      <div class="ftr-mark">${silhouette({ w: 40, h: 48, pad: 1 })}<p class="ftr-tag">${esc(S.tagline)}</p></div>
      <ul class="ftr-links">
        <li><a href="home.html">${esc(S.links.home)}</a></li><li><a href="spaces.html">${esc(S.links.spaces)}</a></li>
        <li><a href="about.html">${esc(S.links.about)}</a></li><li><a href="about.html#contact">${esc(S.contact)}</a></li>
        <li><a href="404.html">${esc(S.links.privacy)}</a></li>
      </ul></div></div></footer>`;
  }
  function reviewPanel() {
    const sl = D.spaces.map((s) => `<li><a href="space.html?slug=${s.slug}">space · ${esc(s.nameEn)}</a></li>`).join('');
    return `<div class="review" lang="en" dir="ltr"><button type="button" aria-expanded="false" data-rv>مراجعة / Review</button>
      <div class="rv-panel" hidden>
        <h2>Direction B — The Strip</h2>
        <label><input type="checkbox" data-demo ${prefs.demo ? 'checked' : ''}> حالات تجريبية / Demo states</label>
        <p>Off = the live data of 2026-11-14. On = Branch, Focus, Garden, Number One verified with live states; Elevate «متاح»; an announcement on Branch Hub.</p>
        <ul>
          <li><a href="home.html">home</a></li><li><a href="spaces.html">spaces (list)</a></li><li><a href="spaces.html?filters=open">spaces?filters=open</a></li>
          <li><a href="spaces.html?view=map">spaces?view=map</a></li><li><a href="login.html">login</a></li><li><a href="about.html">about</a></li>
          <li><a href="account.html">account</a></li><li><a href="favorites.html">favorites</a></li><li><a href="404.html">404</a></li>
        </ul>
        <h2>Every space</h2><ul>${sl}</ul>
      </div></div>`;
  }
  function phoneMenu(def) {
    const T = L(); const S = T.site;
    const el = document.createElement('div');
    el.className = 'sheet-menu'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-modal', 'true'); el.setAttribute('aria-label', S.menu);
    const links = [['home', 'home.html'], ['spaces', 'spaces.html'], ['about', 'about.html']].map(([k, h]) => `<a href="${h}"${def.nav === k ? ' aria-current="page"' : ''}>${esc(S.links[k])}</a>`).join('');
    const acct = def.account
      ? `<a href="favorites.html"${def.key === 'favorites' ? ' aria-current="page"' : ''}>${esc(S.account.favorites)}</a><a href="404.html">${esc(S.account.reports)}</a><a href="account.html"${def.key === 'account' ? ' aria-current="page"' : ''}>${esc(S.account.settings)}</a>`
      : '';
    el.innerHTML = `<div class="hdr-in"><a class="logo" href="home.html"><img class="lg-light" src="../_shared/logo/masaha-logo-berry.svg" alt="${esc(S.wordmark)}" width="110" height="40"><img class="lg-dark" src="../_shared/logo/masaha-logo-dark-berry.svg" alt="${esc(S.wordmark)}" width="110" height="40"></a>
      <div class="hdr-actions"><button type="button" class="icon-btn" data-close aria-label="${esc(S.closeMenu)}">${ic('x')}</button></div></div>
      <nav aria-label="${esc(S.navigation)}">${links}${acct}</nav>
      <div class="sheet-row">
        <button type="button" class="btn btn-secondary" data-act="lang" lang="${prefs.lang === 'ar' ? 'en' : 'ar'}">${ic('languages')}${esc(S.otherLanguage)}</button>
        <button type="button" class="btn btn-secondary" data-act="theme">${ic(theme() === 'dark' ? 'sun' : 'moon')}${esc(S.switchTheme[theme()])}</button>
        ${def.account ? `<a class="btn btn-quiet" href="home.html">${ic('log-out', 'dir')}${esc(T.users.signOut)}</a>` : `<a class="btn btn-primary" href="login.html">${ic('log-in', 'dir')}${esc(S.signIn)}</a>`}
      </div>`;
    return el;
  }

  let current = null;
  function setLang(l) { prefs.lang = l; store.set('lang', l); applyPrefs(); syncAddress(); if (current) current.render(); }
  function toggleTheme() { prefs.themeChoice = theme() === 'dark' ? 'light' : 'dark'; store.set('theme', prefs.themeChoice); applyPrefs(); syncAddress(); if (current) current.render(); }
  function setTheme(choice) { prefs.themeChoice = choice; store.set('theme', choice); applyPrefs(); syncAddress(); if (current) current.render(); }

  function page(def) {
    function render() {
      const T = L();
      const focusedAct = document.activeElement && document.activeElement.dataset ? document.activeElement.dataset.act : null;
      document.title = T.site.documentTitle(def.title(T));
      document.body.className = def.bodyClass ? def.bodyClass() : '';
      const app = document.getElementById('app');
      const content = def.main(T);
      app.innerHTML = (def.wrapHeader ? def.wrapHeader(header(def), content) : header(def) + `<main id="main" tabindex="-1">${content}</main>`) + (def.noFooter ? '' : footer()) + reviewPanel();
      wireShell(def);
      if (def.mount) def.mount(document.getElementById('main'), T);
      if (focusedAct) { const b = document.querySelector(`.hdr [data-act="${focusedAct}"]`); if (b) b.focus(); }
    }
    current = { render, def };
    const start = () => { render(); document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeUserMenu(); }); };
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
    try { matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => { if (prefs.themeChoice === 'system') { applyPrefs(); render(); } }); } catch (e) { /* old engines */ }
  }
  function closeUserMenu() { document.querySelectorAll('.menu-pop').forEach((m) => m.remove()); const b = document.querySelector('[data-act="user"]'); if (b) b.setAttribute('aria-expanded', 'false'); }
  function wireShell(def) {
    const T = L();
    document.querySelectorAll('[data-act="lang"]').forEach((b) => b.addEventListener('click', () => { document.querySelectorAll('.sheet-menu').forEach((m) => m.remove()); setLang(prefs.lang === 'ar' ? 'en' : 'ar'); }));
    document.querySelectorAll('[data-act="theme"]').forEach((b) => b.addEventListener('click', () => { document.querySelectorAll('.sheet-menu').forEach((m) => m.remove()); toggleTheme(); }));
    const mb = document.querySelector('[data-act="menu"]');
    if (mb) mb.addEventListener('click', () => {
      const m = phoneMenu(def);
      document.body.appendChild(m);
      mb.setAttribute('aria-expanded', 'true');
      const close = () => { m.remove(); mb.setAttribute('aria-expanded', 'false'); mb.focus(); document.removeEventListener('keydown', esc1, true); };
      const esc1 = (e) => { if (e.key === 'Escape') close(); };
      document.addEventListener('keydown', esc1, true);
      m.querySelector('[data-close]').addEventListener('click', close);
      m.querySelectorAll('[data-act="lang"]').forEach((b) => b.addEventListener('click', () => { m.remove(); setLang(prefs.lang === 'ar' ? 'en' : 'ar'); }));
      m.querySelectorAll('[data-act="theme"]').forEach((b) => b.addEventListener('click', () => { m.remove(); toggleTheme(); }));
      m.querySelector('[data-close]').focus();
    });
    const ub = document.querySelector('[data-act="user"]');
    if (ub) ub.addEventListener('click', (e) => {
      e.stopPropagation();
      if (document.querySelector('.menu-pop')) { closeUserMenu(); return; }
      const name = USER.name;
      const m = document.createElement('div');
      m.className = 'menu-pop';
      m.innerHTML = `<div class="who"><b>${esc(name)}</b><span>${ltr(esc(USER.email))}</span></div>
        <a href="favorites.html"${def.key === 'favorites' ? ' aria-current="page"' : ''}>${ic('heart')}${esc(T.site.account.favorites)}</a>
        <a href="404.html">${ic('flag')}${esc(T.site.account.reports)}</a>
        <a href="account.html"${def.key === 'account' ? ' aria-current="page"' : ''}>${ic('user')}${esc(T.site.account.settings)}</a>
        <a href="home.html">${ic('log-out', 'dir')}${esc(T.users.signOut)}</a>`;
      document.querySelector('.hdr').appendChild(m);
      ub.setAttribute('aria-expanded', 'true');
      m.querySelector('a').focus();
      document.addEventListener('click', function off(ev) { if (!m.contains(ev.target)) { closeUserMenu(); document.removeEventListener('click', off); } });
    });
    const rv = document.querySelector('[data-rv]');
    rv.addEventListener('click', () => { const p = rv.nextElementSibling; p.hidden = !p.hidden; rv.setAttribute('aria-expanded', String(!p.hidden)); });
    document.querySelector('[data-demo]').addEventListener('change', (e) => { prefs.demo = e.target.checked; store.set('demo', prefs.demo ? '1' : '0'); const u = new URL(location.href); u.searchParams.set('demo', prefs.demo ? '1' : '0'); try { history.replaceState(null, '', u.href); } catch (x) { /* */ } current.render(); const b = document.querySelector('[data-rv]'); b.click(); document.querySelector('[data-demo]').focus(); });
  }

  window.B = {
    D, Q, prefs, L, esc, ic, ltr, clock, gaza, NOW, price, num, ago, km, uid, theme,
    GOVS, AREA, spaces, stateOf, todayText, govName, areaName, openByHours,
    silhouette, stripMap, isPoster, frameCls, STRIP_BOUNDS, P, fit,
    dialog, signInPrompt, toast, card, wireHearts, page, setLang, setTheme, USER,
  };
})();
