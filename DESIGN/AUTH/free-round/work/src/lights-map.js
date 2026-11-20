/* ============ the map, drawn from the real data ============
   A calm cartographic drawing, never a targeting display: no coordinates on screen, no rings or reticles,
   soft lights rather than pinpoints, and an inset (a rounded box, the way atlases show a city) for Gaza City. */
(function () {
  var M = window.Masaha;
  var atlas = document.getElementById('atlas');
  var svg = atlas.querySelector('svg.map');
  var layer = atlas.querySelector('.labels');
  var NS = 'http://www.w3.org/2000/svg';
  var KX = 95.0, KY = 110.9;              /* km per degree of longitude (at 31.4°N) and of latitude */
  var LNG0 = 34.219, LAT0 = 31.5944;      /* west-most and north-most points of the outline */
  var STRIP_W = (34.564 - LNG0) * KX, STRIP_H = (LAT0 - 31.22) * KY;
  var CITY = { lat: 31.5228, lng: 34.4478, w: 3.0, h: 3.2 };   /* the inset's window over Gaza City, in km */
  /* label side for each light inside the inset, physical: e = right of the light, w = left (the map never mirrors) */
  var IN_CITY = { masahat: 'e', 'number-one': 'e', focus: 'w', branch: 'e', white: 'w', jreas: 'w', golden: 'w', pal: 'e', garden: 'w' };

  function el(name, attrs, parent) {
    var n = document.createElementNS(NS, name);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    (parent || svg).appendChild(n); return n;
  }
  function label(x, y, side, html, cls) {
    var d = document.createElement('div');
    d.className = 'lbl ' + side + (cls ? ' ' + cls : '');
    d.style.left = x.toFixed(1) + 'px'; d.style.top = y.toFixed(1) + 'px'; d.innerHTML = html;
    layer.appendChild(d); return d;
  }
  /* the outline is approximate, so draw it as a hand would: smooth coast and eastern border, sharp corners at the ends */
  function cr(points) {
    var d = '';
    for (var i = 0; i < points.length - 1; i++) {
      var p0 = points[i - 1] || points[i], p1 = points[i], p2 = points[i + 1], p3 = points[i + 2] || p2;
      d += 'C' + (p1[0] + (p2[0] - p0[0]) / 6).toFixed(1) + ',' + (p1[1] + (p2[1] - p0[1]) / 6).toFixed(1) + ' ' +
        (p2[0] - (p3[0] - p1[0]) / 6).toFixed(1) + ',' + (p2[1] - (p3[1] - p1[1]) / 6).toFixed(1) + ' ' + p2[0].toFixed(1) + ',' + p2[1].toFixed(1);
    }
    return d;
  }
  function M0(p) { return 'M' + p[0].toFixed(1) + ',' + p[1].toFixed(1); }
  function L0(p) { return 'L' + p[0].toFixed(1) + ',' + p[1].toFixed(1); }
  function outlinePath(pts) { return M0(pts[0]) + cr(pts.slice(0, 10)) + L0(pts[10]) + cr(pts.slice(10, 21)) + 'Z'; }
  function along(a, b, k) { return [b[0] + (b[0] - a[0]) * k, b[1] + (b[1] - a[1]) * k]; }
  function eastAt(pts, y) {
    for (var i = 10; i < 20; i++) { var a = pts[i], b = pts[i + 1]; if ((y - a[1]) * (y - b[1]) <= 0) return a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]); }
    return pts[20][0];
  }
  function coastAt(pts, y) { /* x of the coast at screen height y (outline points 0..9) */
    for (var i = 0; i < 9; i++) { var a = pts[i], b = pts[i + 1]; if ((y - a[1]) * (y - b[1]) <= 0) return a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]); }
    return pts[9][0];
  }
  function esc(s) { return s.replace(/[&<>]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }); }
  function isFrom(sp) { return M.state.from && M.state.from.slug === sp.slug; }

  function draw() {
    var W = atlas.clientWidth, H = atlas.clientHeight, lang = M.state.lang;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    svg.innerHTML = ''; layer.innerHTML = '';
    /* the full map (with Gaza City's inset) needs room; a narrow or short map gets the compact one: the whole Strip,
       its four place names to the east, the legend */
    var compact = W < 640 || H < 420;
    var s, ox, oy;
    if (!compact) {
      s = Math.min((H - 136) / STRIP_H, 24);
      ox = W - 120 - STRIP_W * s; oy = 64;
    } else {
      s = Math.min((H - 32) / STRIP_H, (W - 220) / STRIP_W);
      ox = Math.max(Math.round(W * 0.14), (W - STRIP_W * s) / 2 - 80); oy = (H - STRIP_H * s) / 2;
    }
    function P(lat, lng) { return [ox + (lng - LNG0) * KX * s, oy + (LAT0 - lat) * KY * s]; }
    var pts = M.OUTLINE.map(function (p) { return P(p[0], p[1]); });

    var defs = el('defs', {});
    var g = el('radialGradient', { id: 'glow' }, defs);
    el('stop', { offset: '0', style: 'stop-color:var(--glow);stop-opacity:.55' }, g);
    el('stop', { offset: '.45', style: 'stop-color:var(--glow);stop-opacity:.18' }, g);
    el('stop', { offset: '1', style: 'stop-color:var(--glow);stop-opacity:0' }, g);

    /* the sea: everything west of the coast, the coast carried on straight past both ends of the Strip.
       The land beyond the borders keeps the atlas's own ground. */
    var coast = pts.slice(0, 10);
    var north = along(coast[1], coast[0], 6), south = along(coast[8], coast[9], 30);
    el('path', { class: 'sea', d: M0(north) + L0(coast[0]) + cr(coast) + L0(south) + 'L-10,' + (H + 10) + 'L-10,-10L' + north[0].toFixed(1) + ',-10Z' });

    /* water lines: the coast repeated out to sea, wider apart as they go */
    var a = coast[0], b = coast[9], len = Math.hypot(b[0] - a[0], b[1] - a[1]);
    var nx = (b[1] - a[1]) / len, ny = -(b[0] - a[0]) / len;
    if (nx > 0) { nx = -nx; ny = -ny; }
    var ext = [along(coast[1], coast[0], 1.2)].concat(coast, [along(coast[8], coast[9], 3)]);
    var cd = M0(ext[0]) + cr(ext);
    var fade = el('linearGradient', { id: 'wfade', gradientUnits: 'userSpaceOnUse', x1: ext[0][0], y1: ext[0][1], x2: ext[ext.length - 1][0], y2: ext[ext.length - 1][1] }, defs);
    [[0, 0], [.18, 1], [.82, 1], [1, 0]].forEach(function (st) { el('stop', { offset: st[0], 'stop-color': '#fff', 'stop-opacity': st[1] }, fade); });
    var mk = el('mask', { id: 'wmask', maskUnits: 'userSpaceOnUse', x: 0, y: 0, width: W, height: H }, defs);
    el('rect', { x: 0, y: 0, width: W, height: H, fill: 'url(#wfade)' }, mk);
    var wg = el('g', { mask: 'url(#wmask)' });
    var off = 0, step = compact ? 4 : 7;
    for (var i = 0; i < (compact ? 6 : 14); i++) {
      off += step; step *= 1.14;
      el('path', { class: 'waterline', d: cd, transform: 'translate(' + (nx * off).toFixed(1) + ',' + (ny * off).toFixed(1) + ')', opacity: (0.5 * Math.pow(0.85, i)).toFixed(3) }, wg);
    }

    el('path', { class: 'land', d: outlinePath(pts) });

    var order = M.SPACES.slice().sort(function (p, q) { return q.lat - p.lat; });
    var lights = el('g', { class: 'lights' });
    function light(x, y, sp, i, parent, size) {
      var from = isFrom(sp);
      var gg = el('g', { class: 'light' + (from ? ' is-from' : ''), style: '--d:' + (200 + i * 90) + 'ms' }, parent || lights);
      el('circle', { class: 'light-glow', cx: x, cy: y, r: size * (from ? 4.2 : 3.2), fill: 'url(#glow)' }, gg);
      var z = from ? size * 1.35 : size;
      el('rect', { class: 'light-core', x: x - z / 2, y: y - z / 2, width: z, height: z, rx: z * 0.32 }, gg);
      return gg;
    }

    var city = P(CITY.lat, CITY.lng);
    var bw = CITY.w * KX / 95 * s * 1.0, bh = CITY.h * s;   /* the window over the city on the main map */

    if (!compact) {
      order.forEach(function (sp, i) { var p = P(sp.lat, sp.lng); light(p[0], p[1], sp, i, null, IN_CITY[sp.slug] ? 4 : 9); });

      /* the inset: a rounded box out at sea, north-west of the city */
      var IW = 300, IH = IW * (CITY.h / CITY.w);
      var ix = 40, iy = 64;
      var z = IW / CITY.w;   /* px per km inside the inset */
      el('rect', { class: 'city-window', x: city[0] - bw / 2, y: city[1] - bh / 2, width: bw, height: bh, rx: 6 });
      el('path', { class: 'tether', d: M0([city[0] - bw / 2, city[1] - bh / 2]) + L0([ix + IW, iy + 24]) });
      el('rect', { class: 'inset-shadow', x: ix, y: iy, width: IW, height: IH, rx: 16 });
      var clip = el('clipPath', { id: 'iclip' }, defs);
      el('rect', { x: ix, y: iy, width: IW, height: IH, rx: 16 }, clip);
      var ig = el('g', { 'clip-path': 'url(#iclip)' });
      el('rect', { class: 'inset-land-beyond', x: ix, y: iy, width: IW, height: IH }, ig);
      function IP(lat, lng) { return [ix + IW / 2 + (lng - CITY.lng) * KX * z, iy + IH / 2 + (CITY.lat - lat) * KY * z]; }
      var ipts = M.OUTLINE.map(function (p) { return IP(p[0], p[1]); });
      var icoast = ipts.slice(0, 10);
      var inorth = along(icoast[1], icoast[0], 3), isouth = along(icoast[2], icoast[3], 4);
      el('path', { class: 'sea', d: M0(inorth) + L0(icoast[0]) + cr(icoast.slice(0, 4)) + L0(isouth) + 'L' + (ix - 10) + ',' + (iy + IH + 10) + 'L' + (ix - 10) + ',' + (iy - 10) + 'Z' }, ig);
      var o2 = 0, st2 = 8, icd = M0(icoast[0]) + cr(icoast.slice(0, 5));
      for (var j = 0; j < 6; j++) { o2 += st2; st2 *= 1.16; el('path', { class: 'waterline', d: icd, transform: 'translate(' + (nx * o2).toFixed(1) + ',' + (ny * o2).toFixed(1) + ')', opacity: (0.45 * Math.pow(0.8, j)).toFixed(3) }, ig); }
      el('path', { class: 'land', d: outlinePath(ipts) }, ig);
      el('rect', { class: 'inset-frame', x: ix, y: iy, width: IW, height: IH, rx: 16 });
      var il = el('g', { class: 'lights' });
      order.forEach(function (sp, i) {
        if (!IN_CITY[sp.slug]) return;
        var p = IP(sp.lat, sp.lng), side = IN_CITY[sp.slug];
        light(p[0], p[1], sp, i, il, 10);
        label(p[0] + (side === 'e' ? 12 : -12), p[1], side, esc(sp[lang]), isFrom(sp) ? 'is-from' : '');
      });
      label(ix + (lang === 'ar' ? IW - 16 : 16), iy + 14, lang === 'ar' ? 'w top' : 'e top', esc(M.t('gaza')), 'inset-title');

      /* the four in the south: one label per place, the names stacked over the area, east of the border */
      [['elevate', 'coma'], ['al-salam'], ['masar']].forEach(function (group) {
        var sps = group.map(function (slug) { return M.SPACES.filter(function (x) { return x.slug === slug; })[0]; });
        var ps = sps.map(function (sp) { return P(sp.lat, sp.lng); });
        var y = ps.reduce(function (t, p) { return t + p[1]; }, 0) / ps.length;
        var ex = eastAt(pts, y) + 24;
        ps.forEach(function (p) { el('path', { class: 'leader', d: M0([p[0] + 8, p[1]]) + L0([ex - 8, y]) }); });
        var html = sps.map(function (sp) { return '<span' + (isFrom(sp) ? ' class="is-from"' : '') + '>' + esc(sp[lang]) + '</span>'; }).join('') +
          '<small>' + esc(sps[0][lang === 'ar' ? 'areaAr' : 'areaEn']) + '</small>';
        label(ex, y, 'e', html, 'names');
      });

      /* the sea, named along the coast */
      var my = P(31.35, 34.3)[1], mid = [Math.max(72, coastAt(pts, my) - 110), my], ang = Math.atan2(b[1] - a[1], b[0] - a[0]) * 180 / Math.PI + 180;
      var sl = label(mid[0], mid[1], '', esc(M.t('sea')), 'sea');
      sl.style.transform = 'translate(-50%, -50%) rotate(' + ang.toFixed(1) + 'deg)';
    } else {
      order.forEach(function (sp, i) { var p = P(sp.lat, sp.lng); light(p[0], p[1], sp, i, null, Math.max(5, Math.min(9, s * 0.9))); });
      var places = [['مدينة غزة', 'Gaza City', 31.522, -2], ['النصيرات', 'Nuseirat', 31.4483, -8], ['دير البلح', 'Deir al-Balah', 31.42013, 8], ['المواصي', 'Al-Mawasi', 31.36569, 4]];
      places.forEach(function (pl) {
        var y = P(pl[2], 34.4)[1];
        label(eastAt(pts, y) + 14, y + pl[3] * Math.max(1, s / 5), 'e', esc(lang === 'ar' ? pl[0] : pl[1]), s > 8 ? 'place' : 'place sm');
      });
    }
  }

  var raf;
  M.onChange(function () { cancelAnimationFrame(raf); raf = requestAnimationFrame(draw); });
  window.addEventListener('resize', function () { cancelAnimationFrame(raf); raf = requestAnimationFrame(draw); });
  if (document.fonts) document.fonts.ready.then(draw);
})();
