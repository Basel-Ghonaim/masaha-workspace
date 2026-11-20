/* Direction C — the printed map, drawn as SVG from the real coordinates (no tiles, no library).
   The Strip turns to fit its frame: lying along a wide frame (north-east to the right), standing in a tall one. */
(function () {
  /* the Strip: _shared/data/strip-outline.json (the lead's outline; every space falls inside it) */
  var OUT = [[31.5944,34.4898],[31.56,34.463],[31.523,34.43],[31.49,34.403],[31.46,34.376],[31.43,34.341],[31.39,34.294],[31.36,34.256],[31.33,34.23],[31.316,34.219],[31.22,34.267],[31.248,34.288],[31.29,34.323],[31.33,34.36],[31.38,34.395],[31.425,34.42],[31.46,34.45],[31.495,34.49],[31.525,34.515],[31.552,34.542],[31.588,34.564],[31.5944,34.4898]];
  var LABELS = [
    { ar: 'شمال غزة', en: 'North Gaza', lat: 31.553, lng: 34.523 },
    { ar: 'غزة', en: 'Gaza City', lat: 31.478, lng: 34.432 },
    { ar: 'الوسطى', en: 'Middle Area', lat: 31.398, lng: 34.352 },
    { ar: 'خان يونس', en: 'Khan Younis', lat: 31.335, lng: 34.300 },
    { ar: 'رفح', en: 'Rafah', lat: 31.275, lng: 34.268 }
  ];
  var K = Math.cos(31.4 * Math.PI / 180);
  function P(lat, lng) { return [(lng - 34.39) * 111.32 * K, -(lat - 31.41) * 110.57]; }
  function rot(p, a) { var c = Math.cos(a), s = Math.sin(a); return [p[0] * c - p[1] * s, p[0] * s + p[1] * c]; }
  function bounds(pts) { var b = [1e9, 1e9, -1e9, -1e9]; pts.forEach(function (p) { b[0] = Math.min(b[0], p[0]); b[1] = Math.min(b[1], p[1]); b[2] = Math.max(b[2], p[0]); b[3] = Math.max(b[3], p[1]); }); return b; }

  /* el: the frame; o: { spaces, selected, onSelect(slug|null), you, static, focus } */
  window.GuideMap = function (el, o) {
    var self = this, w, h, a, view, rtl;
    function project(lat, lng) { return rot(P(lat, lng), a); }
    function scr(p) { return [w / 2 + (p[0] - view.cx) * view.s, h / 2 + (p[1] - view.cy) * view.s]; }
    function fit(b, pad) { var s = Math.min((w - 2 * pad) / Math.max(b[2] - b[0], .01), (h - 2 * pad) / Math.max(b[3] - b[1], .01)); view = { cx: (b[0] + b[2]) / 2, cy: (b[1] + b[3]) / 2, s: Math.min(s, 900) }; }
    function stripB() { return bounds(OUT.map(function (q) { return project(q[0], q[1]); })); }
    self.whole = function () { fit(stripB(), Math.min(w, h) > 400 ? 40 : 20); draw(); };
    self.zoom = function (f) { view.s = Math.max(4, Math.min(900, view.s * f)); draw(); };
    self.fitTo = function (list) {
      var pts = list.map(function (s) { return project(s.loc.lat, s.loc.lng); }), b = bounds(pts);
      var m = .35; b = [b[0] - m, b[1] - m, b[2] + m, b[3] + m]; fit(b, 64); draw();
    };
    self.set = function (patch) { Object.assign(o, patch); draw(); };
    function path(list) { return 'M' + list.map(function (q) { var p = scr(project(q[0], q[1])); return p[0].toFixed(1) + ' ' + p[1].toFixed(1); }).join('L') + 'Z'; }

    function draw() {
      var t = M.t(), lang = M.lang, svg = '';
      svg += '<rect width="' + w + '" height="' + h + '" fill="var(--sea)"/>';
      svg += '<path d="' + path(OUT) + '" fill="var(--strip)" stroke="var(--strip-edge)" stroke-width="1.5" stroke-linejoin="round"/>';
      var fs = Math.max(15, Math.min(24, view.s * .9)), placed = [];
      LABELS.forEach(function (L) {
        var p = scr(project(L.lat, L.lng));
        if (p[0] < -100 || p[0] > w + 100 || p[1] < -40 || p[1] > h + 40) return;
        var hw = L[lang].length * fs * .29 + 6, box = [p[0] - hw, p[1] - fs * .6, p[0] + hw, p[1] + fs * .6];
        if (placed.some(function (b) { return box[0] < b[2] && box[2] > b[0] && box[1] < b[3] && box[3] > b[1]; })) return;
        placed.push(box);
        svg += '<text x="' + p[0].toFixed(1) + '" y="' + p[1].toFixed(1) + '" text-anchor="middle" dominant-baseline="middle" class="map-gov" style="font-size:' + fs.toFixed(0) + 'px">' + M.esc(L[lang]) + '</text>';
      });
      if (o.you) { var y = scr(project(o.you.lat, o.you.lng)); svg += '<circle cx="' + y[0] + '" cy="' + y[1] + '" r="7" fill="none" stroke="var(--text)" stroke-width="2"/><circle cx="' + y[0] + '" cy="' + y[1] + '" r="2.5" fill="var(--text)"/>'; }
      /* north arrow and scale */
      var nv = rot([0, -1], a), cx = 36, cy = h - 44;
      if (!o.static || w > 300) {
        svg += '<g class="map-north" transform="translate(' + cx + ' ' + cy + ')"><circle r="18" fill="var(--surface)" stroke="var(--border)"/>' +
          '<line x1="' + (-nv[0] * 9).toFixed(1) + '" y1="' + (-nv[1] * 9).toFixed(1) + '" x2="' + (nv[0] * 10).toFixed(1) + '" y2="' + (nv[1] * 10).toFixed(1) + '" stroke="var(--text)" stroke-width="1.5"/>' +
          '<circle cx="' + (nv[0] * 10).toFixed(1) + '" cy="' + (nv[1] * 10).toFixed(1) + '" r="2.5" fill="var(--text)"/></g>';
        var km = [1, 2, 5, 10].filter(function (k) { return k * view.s <= 140; }).pop() || 1, bar = km * view.s;
        var sx = w - 24 - bar, sy = h - 28;
        svg += '<g class="map-scale"><line x1="' + sx + '" y1="' + sy + '" x2="' + (sx + bar) + '" y2="' + sy + '" stroke="var(--text)" stroke-width="2"/>' +
          '<line x1="' + sx + '" y1="' + (sy - 5) + '" x2="' + sx + '" y2="' + (sy + 1) + '" stroke="var(--text)" stroke-width="2"/><line x1="' + (sx + bar) + '" y1="' + (sy - 5) + '" x2="' + (sx + bar) + '" y2="' + (sy + 1) + '" stroke="var(--text)" stroke-width="2"/>' +
          '<text x="' + (sx + bar / 2) + '" y="' + (sy - 9) + '" text-anchor="middle" class="map-km">' + M.esc(t.map.km(km)) + '</text></g>';
      }
      el.querySelector('svg.map-svg').setAttribute('viewBox', '0 0 ' + w + ' ' + h);
      el.querySelector('svg.map-svg').innerHTML = svg;
      pins();
    }
    function pins() {
      var t = M.t(), layer = el.querySelector('.map-pins'), list = o.spaces.filter(function (s) { return s.loc; }), groups = [];
      list.forEach(function (s) {
        var p = scr(project(s.loc.lat, s.loc.lng));
        if (p[0] < -20 || p[0] > w + 20 || p[1] < -20 || p[1] > h + 20) return;
        var g = o.static ? null : groups.filter(function (g) { return Math.abs(g.p[0] - p[0]) < 30 && Math.abs(g.p[1] - p[1]) < 30; })[0];
        if (g && s.slug !== o.selected) g.items.push(s); else groups.push({ p: p, items: [s] });
      });
      var html = '';
      groups.forEach(function (g) {
        var x = rtl ? w - g.p[0] : g.p[0], pos = 'inset-inline-start:' + x.toFixed(1) + 'px;inset-block-start:' + g.p[1].toFixed(1) + 'px';
        if (g.items.length > 1) {
          var anyOpen = g.items.some(function (s) { var k = M.state(s).kind; return k === 'open' || k === 'available'; });
          html += '<button type="button" class="pin cluster" style="' + pos + '" data-cluster="' + g.items.map(function (s) { return s.slug; }).join(',') + '" aria-label="' + M.esc(t.map.cluster(g.items.length)) + '">' +
            '<span class="ct">' + g.items.length + '</span>' + (anyOpen ? '<span class="mark live" aria-hidden="true"></span>' : '') + '</button>';
        } else {
          var s = g.items[0], stt = M.state(s), sel = s.slug === o.selected, nm = M.name(s);
          html += '<button type="button" class="pin' + (sel ? ' sel' : '') + '" style="' + pos + '" data-slug="' + s.slug + '" aria-pressed="' + sel + '" aria-label="' + M.esc(t.map.pin(nm, stt.word)) + '"' + (o.static ? ' tabindex="-1" disabled' : '') + '>' +
            '<span class="mark ' + stt.mark + '" aria-hidden="true"></span><span class="lbl" aria-hidden="true">' + M.esc(nm) + '</span></button>';
        }
      });
      layer.innerHTML = html;
    }
    function size() {
      rtl = document.documentElement.dir === 'rtl';
      w = Math.max(200, el.clientWidth); h = Math.max(200, el.clientHeight);
      a = 0; /* north up, always */
    }
    el.innerHTML = '<svg class="map-svg" aria-hidden="true" focusable="false" preserveAspectRatio="none"></svg><div class="map-pins"></div>';
    size();
    if (o.focusLoc) { var fp = project(o.focusLoc.lat, o.focusLoc.lng), b = stripB(); fit(b, 20); }
    else self.whole();
    draw();
    if (!o.static) {
      el.addEventListener('click', function (e) {
        var b = e.target.closest('[data-slug]'), c = e.target.closest('[data-cluster]');
        if (c) { var slugs = c.getAttribute('data-cluster').split(','); self.fitTo(o.spaces.filter(function (s) { return slugs.indexOf(s.slug) >= 0; })); var f = el.querySelector('[data-slug="' + slugs[0] + '"]'); if (f) f.focus(); return; }
        if (b) { o.selected = b.getAttribute('data-slug'); pins(); var nb = el.querySelector('[data-slug="' + o.selected + '"]'); if (nb) nb.focus(); if (o.onSelect) o.onSelect(o.selected); }
      });
      /* drag to pan */
      var drag = null;
      el.addEventListener('pointerdown', function (e) { if (e.target.closest('button')) return; drag = { x: e.clientX, y: e.clientY, cx: view.cx, cy: view.cy }; el.setPointerCapture(e.pointerId); el.classList.add('dragging'); });
      el.addEventListener('pointermove', function (e) { if (!drag) return; view.cx = drag.cx - (e.clientX - drag.x) / view.s; view.cy = drag.cy - (e.clientY - drag.y) / view.s; draw(); });
      el.addEventListener('pointerup', function () { drag = null; el.classList.remove('dragging'); });
    }
    var rz; window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(function () { if (!el.isConnected) return; var ow = w, oh = h; size(); if (ow !== w || oh !== h) { if (o.static) { fit(stripB(), 20); draw(); } else self.whole(); } }, 120); });
  };
})();
