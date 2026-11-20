// The visual pass's in-page checks (IDENTITY T23), injected on every new document as window.__vp.
(() => {
  if (window.__vp) return;
  if (document.contentType !== 'text/html') return;
  const SEA = new Set(
    '#eafbfc #d5f4f5 #b3e6e8 #85d0d4 #50b3b8 #15959b #02787d #096165 #05494c #023235 #001d1f #f4fcfe #eaf5f7 #dbe6e9 #c7d1d4 #9da7a9 #747e80 #5c6567 #464f51 #2a3234 #182022 #0c1315'.split(
      ' ',
    ),
  );
  const SPARK = { light: '#b55bb3', dark: '#d27ed0' };
  let mutations = 0;
  let lastMutation = performance.now();
  const startObserver = () => {
    if (!document.documentElement) return setTimeout(startObserver, 10);
    new MutationObserver(() => {
      mutations += 1;
      lastMutation = performance.now();
    }).observe(document.documentElement, { subtree: true, childList: true, attributes: true, characterData: true });
  };
  startObserver();

  // ---------- colours
  const toLinear = (c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
  const fromLinear = (c) => (c <= 0.0031308 ? 12.92 * c : 1.055 * c ** (1 / 2.4) - 0.055);
  function oklabToRgb(L, a, b) {
    const l_ = L + 0.3963377774 * a + 0.2158037573 * b;
    const m_ = L - 0.1055613458 * a - 0.0638541728 * b;
    const s_ = L - 0.0894841775 * a - 1.291485548 * b;
    const l = l_ ** 3;
    const m = m_ ** 3;
    const s = s_ ** 3;
    const r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s;
    const g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s;
    const bb = -0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s;
    return [r, g, bb].map((v) => Math.min(1, Math.max(0, fromLinear(v))) * 255);
  }
  const num = (token, scale = 1) => {
    if (token === 'none') return 0;
    if (token.endsWith('%')) return (Number.parseFloat(token) / 100) * scale;
    return Number.parseFloat(token);
  };
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = 1;
  const ctx = canvas.getContext('2d', { willReadFrequently: true });
  const cache = new Map();
  /** A computed colour string → { r, g, b (0–255, unrounded), a (0–1) }. */
  function parse(str) {
    if (!str) return null;
    if (cache.has(str)) return cache.get(str);
    let out = null;
    const s = str.trim();
    let m;
    if ((m = s.match(/^rgba?\(([^)]+)\)$/))) {
      const parts = m[1].split(/[\s,/]+/).filter(Boolean);
      out = { r: +parts[0], g: +parts[1], b: +parts[2], a: parts[3] === undefined ? 1 : num(parts[3]) };
    } else if ((m = s.match(/^oklab\(([^)]+)\)$/))) {
      const [main, alpha] = m[1].split('/');
      const [L, a, b] = main.trim().split(/\s+/);
      const [r, g, bb] = oklabToRgb(num(L), num(a, 0.4), num(b, 0.4));
      out = { r, g, b: bb, a: alpha === undefined ? 1 : num(alpha.trim()) };
    } else if ((m = s.match(/^oklch\(([^)]+)\)$/))) {
      const [main, alpha] = m[1].split('/');
      const [L, C, H] = main.trim().split(/\s+/);
      const h = (num(H) * Math.PI) / 180;
      const c = num(C, 0.4);
      const [r, g, bb] = oklabToRgb(num(L), c * Math.cos(h), c * Math.sin(h));
      out = { r, g, b: bb, a: alpha === undefined ? 1 : num(alpha.trim()) };
    } else if ((m = s.match(/^color\(srgb ([^)]+)\)$/))) {
      const [main, alpha] = m[1].split('/');
      const [r, g, b] = main.trim().split(/\s+/).map((v) => num(v) * 255);
      out = { r, g, b, a: alpha === undefined ? 1 : num(alpha.trim()) };
    } else if (s === 'transparent') {
      out = { r: 0, g: 0, b: 0, a: 0 };
    } else if (s !== 'none' && !s.startsWith('url(')) {
      ctx.clearRect(0, 0, 1, 1);
      ctx.fillStyle = '#000';
      ctx.fillStyle = s;
      ctx.fillRect(0, 0, 1, 1);
      const [r, g, b, a] = ctx.getImageData(0, 0, 1, 1).data;
      out = { r, g, b, a: a / 255, approx: true };
    }
    cache.set(str, out);
    return out;
  }
  const clamp = (v) => Math.max(0, Math.min(255, Math.round(v)));
  const hex = (c) => (c ? `#${[c.r, c.g, c.b].map((v) => clamp(v).toString(16).padStart(2, '0')).join('')}` : null);
  const over = (top, bottom) => {
    const a = top.a + bottom.a * (1 - top.a);
    if (a === 0) return { r: 0, g: 0, b: 0, a: 0 };
    const mix = (k) => (top[k] * top.a + bottom[k] * bottom.a * (1 - top.a)) / a;
    return { r: mix('r'), g: mix('g'), b: mix('b'), a };
  };
  const lum = (c) => {
    const [r, g, b] = [c.r, c.g, c.b].map((v) => toLinear(clamp(v) / 255));
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };
  const ratio = (x, y) => {
    const [a, b] = [lum(x), lum(y)].sort((p, q) => q - p);
    return (a + 0.05) / (b + 0.05);
  };
  const COLOUR_RE = /(rgba?\([^)]*\)|oklab\([^)]*\)|oklch\([^)]*\)|color\([^)]*\)|#[0-9a-fA-F]{3,8}\b)/g;
  const coloursIn = (value) => (value && value !== 'none' ? value.match(COLOUR_RE) ?? [] : []);

  // ---------- describing elements
  function sel(el) {
    if (!el || el.nodeType !== 1) return String(el);
    const parts = [];
    let node = el;
    for (let depth = 0; node && node.nodeType === 1 && depth < 4; depth += 1) {
      let part = node.tagName.toLowerCase();
      if (node.id) part += `#${node.id}`;
      const slot = node.getAttribute('data-slot');
      if (slot) part += `[data-slot=${slot}]`;
      const role = node.getAttribute('role');
      if (role) part += `[role=${role}]`;
      const label = node.getAttribute('aria-label');
      if (label) part += `[aria-label="${label.slice(0, 30)}"]`;
      parts.unshift(part);
      if (node.id) break;
      node = node.parentElement;
    }
    return parts.join(' > ');
  }
  const textOf = (el) => (el.innerText || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 60);
  const theme = () => document.documentElement.dataset.theme;

  function visible(el) {
    if (!el.checkVisibility || !el.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true })) return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  }
  function hiddenClip(el) {
    for (let node = el, d = 0; node && node.nodeType === 1 && d < 6; node = node.parentElement, d += 1) {
      const cs = getComputedStyle(node);
      if (cs.clipPath && cs.clipPath.startsWith('inset(50%')) return true;
      if (cs.clip && cs.clip.startsWith('rect(0px, 0px, 0px, 0px)')) return true;
      const r = node.getBoundingClientRect();
      if ((r.width <= 1 || r.height <= 1) && cs.overflow !== 'visible') return true;
    }
    return false;
  }

  // ---------- Sea, the spark
  const SCAN_PROPS = [
    'color',
    'background-color',
    'border-top-color',
    'border-right-color',
    'border-bottom-color',
    'border-left-color',
    'outline-color',
    'fill',
    'stroke',
    'box-shadow',
    'text-decoration-color',
    'background-image',
    'caret-color',
    'column-rule-color',
  ];
  function painted(cs, prop) {
    if (prop.startsWith('border-')) {
      const side = prop.split('-')[1];
      return cs[`border-${side}-style`] !== 'none' && Number.parseFloat(cs[`border-${side}-width`]) > 0;
    }
    if (prop === 'outline-color') return cs.outlineStyle !== 'none' && Number.parseFloat(cs.outlineWidth) > 0;
    if (prop === 'text-decoration-color') return cs.textDecorationLine !== 'none';
    return true;
  }
  function seaScan() {
    const hits = [];
    const els = document.querySelectorAll('*');
    for (const el of els) {
      for (const pseudo of [null, '::before', '::after']) {
        const cs = getComputedStyle(el, pseudo);
        if (pseudo && (cs.content === 'none' || cs.content === 'normal')) continue;
        for (const prop of SCAN_PROPS) {
          const value = cs.getPropertyValue(prop);
          for (const c of coloursIn(value)) {
            const h = hex(parse(c));
            if (h && SEA.has(h)) {
              hits.push({ el: sel(el) + (pseudo ?? ''), prop, value: c, hex: h, painted: painted(cs, prop), visible: visible(el) });
            }
          }
        }
      }
      // A data: image's own colours (an SVG marker, a background).
      const src = el.getAttribute && (el.getAttribute('src') || '');
      if (src.startsWith('data:image/svg')) {
        const svg = decodeURIComponent(src);
        for (const h of svg.match(/#[0-9a-fA-F]{6}\b/g) ?? []) {
          if (SEA.has(h.toLowerCase())) hits.push({ el: sel(el), prop: 'src (data: svg)', value: h, hex: h.toLowerCase() });
        }
      }
    }
    // The stylesheets' own text (a rule not applied here still carries the old value).
    const sheetHits = [];
    for (const sheet of document.styleSheets) {
      let rules;
      try {
        rules = sheet.cssRules;
      } catch {
        continue;
      }
      const text = [...rules].map((r) => r.cssText).join('\n');
      for (const h of text.match(/#[0-9a-fA-F]{6}\b/g) ?? []) {
        if (SEA.has(h.toLowerCase())) sheetHits.push(`${sheet.href ?? 'inline'}: ${h}`);
      }
    }
    return { elements: els.length, hits: hits.slice(0, 50), hitCount: hits.length, sheetHits: [...new Set(sheetHits)] };
  }
  function directText(el) {
    for (const n of el.childNodes) if (n.nodeType === 3 && n.textContent.trim()) return n.textContent.trim().slice(0, 40);
    return '';
  }
  function sparkScan() {
    const spark = SPARK[theme()];
    const textHits = [];
    const buttonHits = [];
    for (const el of document.querySelectorAll('*')) {
      const cs = getComputedStyle(el);
      if (hex(parse(cs.color)) === spark && directText(el)) textHits.push({ el: sel(el), text: directText(el) });
      if (el.matches('button, [role=button], a[data-slot=button]')) {
        const bg = hex(parse(cs.backgroundColor));
        const borders = ['top', 'right', 'bottom', 'left'].filter(
          (s) => hex(parse(cs[`border-${s}-color`])) === spark && Number.parseFloat(cs[`border-${s}-width`]) > 0,
        );
        if ((bg === spark && parse(cs.backgroundColor).a > 0) || borders.length) {
          buttonHits.push({ el: sel(el), text: textOf(el), bg: bg === spark, borders });
        }
      }
    }
    return { spark, textHits, buttonHits };
  }

  // ---------- painted contrast
  const IMAGE_TAGS = new Set(['IMG', 'VIDEO', 'CANVAS', 'PICTURE', 'IFRAME']);
  function groundAt(textEl, x, y) {
    const stack = document.elementsFromPoint(x, y);
    let index = stack.findIndex((e) => e === textEl || textEl.contains(e));
    if (index < 0) index = stack.findIndex((e) => e.contains(textEl));
    if (index < 0) return { offscreen: true };
    // Covered: something above it, not its own, with a fill.
    for (let i = 0; i < index; i += 1) {
      const e = stack[i];
      if (e.contains(textEl) || textEl.contains(e)) continue;
      const bg = parse(getComputedStyle(e).backgroundColor);
      if (bg && bg.a >= 0.3) return { covered: sel(e) };
    }
    const layers = [];
    let image = null;
    for (let i = index; i < stack.length; i += 1) {
      const e = stack[i];
      const cs = getComputedStyle(e);
      if (IMAGE_TAGS.has(e.tagName) || (cs.backgroundImage && cs.backgroundImage !== 'none' && !cs.backgroundImage.startsWith('linear-gradient(rgba(0, 0, 0, 0)'))) {
        image = sel(e);
        break;
      }
      if (e.tagName === 'svg' || e.closest('svg')) continue;
      const bg = parse(cs.backgroundColor);
      if (bg && bg.a > 0) {
        layers.push({ c: bg, el: e });
        if (bg.a >= 0.999) break;
      }
    }
    let ground = { r: 255, g: 255, b: 255, a: 1 };
    const bottomOpaque = layers.length && layers[layers.length - 1].c.a >= 0.999;
    if (!bottomOpaque && !image) {
      // The canvas: the root's background, else white.
      const root = parse(getComputedStyle(document.documentElement).backgroundColor);
      const body = parse(getComputedStyle(document.body).backgroundColor);
      ground = root && root.a > 0 ? over(root, ground) : body && body.a > 0 ? over(body, ground) : ground;
    }
    for (let i = layers.length - 1; i >= 0; i -= 1) ground = over(layers[i].c, ground);
    return { ground, image, layers: layers.map((l) => hex(l.c) + (l.c.a < 1 ? `@${l.c.a.toFixed(2)}` : '')) };
  }
  function contrastScan({ limit = 60 } = {}) {
    const style = document.createElement('style');
    style.textContent = '* { pointer-events: auto !important; }';
    document.head.appendChild(style);
    const out = { checked: 0, failures: [], images: [], skipped: { covered: 0, offscreen: 0, disabled: 0 } };
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const seen = new Set();
    for (let node = walker.nextNode(); node; node = walker.nextNode()) {
      const text = node.textContent.trim();
      if (!text) continue;
      const el = node.parentElement;
      if (!el || seen.has(el) && seen.size > 4000) continue;
      if (['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE', 'OPTION'].includes(el.tagName)) continue;
      if (!visible(el) || hiddenClip(el)) continue;
      const range = document.createRange();
      range.selectNodeContents(node);
      const rects = [...range.getClientRects()].filter((r) => r.width > 2 && r.height > 2);
      if (!rects.length) continue;
      const r = rects[0];
      const x = Math.min(innerWidth - 1, Math.max(0, r.left + Math.min(r.width / 2, 6)));
      const y = Math.min(innerHeight - 1, Math.max(0, r.top + r.height / 2));
      if (r.bottom < 0 || r.top > innerHeight || r.right < 0 || r.left > innerWidth) {
        out.skipped.offscreen += 1;
        continue;
      }
      if (el.closest('[disabled], [aria-disabled=true], [data-disabled]')) {
        out.skipped.disabled += 1;
        continue;
      }
      const cs = getComputedStyle(el);
      let fg = parse(cs.color);
      if (!fg) continue;
      let opacity = 1;
      for (let n = el; n && n.nodeType === 1; n = n.parentElement) opacity *= Number.parseFloat(getComputedStyle(n).opacity);
      const g = groundAt(el, x, y);
      if (g.offscreen) {
        out.skipped.offscreen += 1;
        continue;
      }
      if (g.covered) {
        out.skipped.covered += 1;
        continue;
      }
      out.checked += 1;
      const size = Number.parseFloat(cs.fontSize);
      const weight = Number.parseInt(cs.fontWeight, 10);
      const large = size >= 24 || (size >= 18.66 && weight >= 700);
      const min = large ? 3 : 4.5;
      if (g.image) {
        out.images.push({ el: sel(el), text: text.slice(0, 40), image: g.image, rect: [r.left, r.top, r.width, r.height].map(Math.round), fg: hex(fg), fgAlpha: fg.a * opacity, min, layers: g.layers });
        continue;
      }
      const shown = over({ ...fg, a: fg.a * opacity }, g.ground);
      const k = ratio(shown, g.ground);
      if (k < min) {
        out.failures.push({ el: sel(el), text: text.slice(0, 40), fg: hex(fg) + (fg.a < 1 ? `@${fg.a.toFixed(2)}` : ''), opacity: +opacity.toFixed(2), ground: hex(g.ground), layers: g.layers, ratio: +k.toFixed(2), min, size, weight });
      }
    }
    style.remove();
    out.failures = out.failures.slice(0, limit);
    return out;
  }

  // ---------- the logo, status colours, focus, overflow
  function logoScan() {
    return [...document.querySelectorAll('svg[data-slot=logo]')].map((svg) => {
      const r = svg.getBoundingClientRect();
      const transforms = [];
      for (let n = svg; n && n.nodeType === 1 && n !== document.body; n = n.parentElement) {
        const t = getComputedStyle(n).transform;
        if (t && t !== 'none') transforms.push(`${sel(n).split(' > ').pop()}: ${t}`);
        if (n.tagName === 'HEADER') break;
      }
      const link = svg.closest('a');
      const container = svg.parentElement;
      const ccs = getComputedStyle(container);
      const cr = container.getBoundingClientRect();
      const dir = getComputedStyle(svg).direction;
      const startGap =
        dir === 'rtl'
          ? cr.right - Number.parseFloat(ccs.paddingRight) - Number.parseFloat(ccs.borderRightWidth) - r.right
          : r.left - (cr.left + Number.parseFloat(ccs.paddingLeft) + Number.parseFloat(ccs.borderLeftWidth));
      return {
        where: sel(svg.parentElement),
        cls: svg.getAttribute('class'),
        size: [+r.width.toFixed(2), +r.height.toFixed(2)],
        pos: [Math.round(r.left), Math.round(r.top)],
        visible: visible(svg) && !hiddenClip(svg),
        viewBox: svg.getAttribute('viewBox'),
        role: svg.getAttribute('role'),
        label: svg.getAttribute('aria-label'),
        hidden: svg.getAttribute('aria-hidden'),
        transforms,
        link: link ? { href: link.getAttribute('href'), name: link.getAttribute('aria-label') || link.textContent.trim() || svg.getAttribute('aria-label') } : null,
        fills: [...svg.querySelectorAll('path')].map((p) => hex(parse(getComputedStyle(p).fill))),
        dir,
        startGap: +startGap.toFixed(2),
      };
    });
  }
  const STATUS = {
    light: { destructive: '#be222a', success: '#137d41', warning: '#b27406', info: '#1f6cb0' },
    dark: { destructive: '#fc6e68', success: '#63b77c', warning: '#d6912b', info: '#64a6e9' },
  };
  const probe = document.createElement('div');
  function token(name) {
    probe.style.cssText = `position:absolute;visibility:hidden;background-color:var(--${name})`;
    document.body.appendChild(probe);
    const v = getComputedStyle(probe).backgroundColor;
    probe.remove();
    return v;
  }
  function statusScan() {
    const t = theme();
    const tokens = Object.fromEntries(Object.keys(STATUS[t]).map((k) => [k, hex(parse(token(k)))]));
    const tokenMismatch = Object.entries(STATUS[t]).filter(([k, v]) => tokens[k] !== v).map(([k, v]) => `${k}: ${tokens[k]} (want ${v})`);
    const PROP = { text: 'color', bg: 'background-color', border: 'border-top-color', fill: 'fill', stroke: 'stroke', outline: 'outline-color' };
    const samples = {};
    const mismatches = [];
    for (const el of document.querySelectorAll('[class*="destructive"], [class*="success"], [class*="warning"], [class*="info"]')) {
      if (!visible(el)) continue;
      const cls = typeof el.className === 'string' ? el.className : el.getAttribute('class') ?? '';
      for (const m of cls.matchAll(/(?:^|\s)((?:[a-z-]+:)*)(text|bg|border|fill|stroke|outline)-(destructive|success|warning|info)(?:-(subtle|foreground|subtle-foreground))?(?=\s|$)/g)) {
        if (m[1]) continue; // a variant (hover:, data-…:) is a state, not the rest look
        const name = m[3] + (m[4] ? `-${m[4]}` : '');
        const want = hex(parse(token(name)));
        const got = hex(parse(getComputedStyle(el).getPropertyValue(PROP[m[2]])));
        const key = `${m[2]}-${name}`;
        samples[key] = samples[key] ?? { want, got, count: 0, el: sel(el) };
        samples[key].count += 1;
        if (want !== got) mismatches.push({ el: sel(el), cls: key, want, got });
      }
    }
    return { theme: t, tokens, tokenMismatch, samples, mismatches: mismatches.slice(0, 20) };
  }
  function focusInfo() {
    const el = document.activeElement;
    if (!el || el === document.body) return { el: 'body' };
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    const inView = r.bottom > 0 && r.top < innerHeight && r.right > 0 && r.left < innerWidth;
    const top = document.elementFromPoint(Math.min(innerWidth - 1, Math.max(0, r.left + r.width / 2)), Math.min(innerHeight - 1, Math.max(0, r.top + r.height / 2)));
    return {
      el: sel(el),
      text: textOf(el),
      focusVisible: el.matches(':focus-visible'),
      outline: { style: cs.outlineStyle, width: cs.outlineWidth, color: hex(parse(cs.outlineColor)), offset: cs.outlineOffset },
      boxShadow: cs.boxShadow,
      ring: hex(parse(token('ring'))),
      sidebarRing: hex(parse(token('sidebar-ring'))),
      rect: [r.left, r.top, r.width, r.height].map(Math.round),
      inView,
      onTop: top ? el === top || el.contains(top) || top.contains(el) : false,
      inDialog: !!el.closest('[role=dialog], [role=alertdialog]'),
      inSidebar: !!el.closest('[data-slot=sidebar]'),
      inCard: !!el.closest('[data-slot=card]'),
    };
  }
  function overflow() {
    const d = document.documentElement;
    const wide = [];
    if (d.scrollWidth > d.clientWidth) {
      for (const el of document.body.querySelectorAll('*')) {
        const r = el.getBoundingClientRect();
        if ((r.right > d.clientWidth + 1 || r.left < -1) && visible(el)) {
          // only the outermost offenders
          if (!wide.some((w) => w.node.contains(el))) wide.push({ node: el, rect: [Math.round(r.left), Math.round(r.right)] });
        }
        if (wide.length > 8) break;
      }
    }
    return { scrollWidth: d.scrollWidth, clientWidth: d.clientWidth, over: d.scrollWidth > d.clientWidth, offenders: wide.map((w) => ({ el: sel(w.node), rect: w.rect })) };
  }
  function settled() {
    const busy = document.querySelector('[data-slot=skeleton], [aria-busy=true]');
    return performance.now() - lastMutation > 300 && !busy;
  }
  function rectOf(selector, index = 0) {
    const els = [...document.querySelectorAll(selector)].filter(visible);
    const el = els[index];
    if (!el) return null;
    el.scrollIntoView({ block: 'center', inline: 'center' });
    const r = el.getBoundingClientRect();
    return { x: r.left + r.width / 2, y: r.top + r.height / 2, w: r.width, h: r.height, left: r.left, top: r.top, text: textOf(el), el: sel(el), count: els.length };
  }
  function styleOf(el, pseudo = null) {
    const cs = getComputedStyle(el, pseudo);
    return {
      bg: cs.backgroundColor,
      bgHex: hex(parse(cs.backgroundColor)),
      bgAlpha: parse(cs.backgroundColor)?.a,
      color: hex(parse(cs.color)),
      border: hex(parse(cs.borderTopColor)),
      borderStart: hex(parse(getComputedStyle(el).direction === 'rtl' ? cs.borderRightColor : cs.borderLeftColor)),
      borderWidth: cs.borderTopWidth,
      outline: `${cs.outlineStyle} ${cs.outlineWidth} ${hex(parse(cs.outlineColor))}`,
      shadow: cs.boxShadow,
    };
  }
  /** The painted ground under an element's centre (its own fill composited over what lies below). */
  function paintedAt(el) {
    const r = el.getBoundingClientRect();
    const x = r.left + r.width / 2;
    const y = r.top + r.height / 2;
    const stack = document.elementsFromPoint(x, y);
    let i = stack.indexOf(el);
    if (i < 0) i = 0;
    const layers = [];
    for (; i < stack.length; i += 1) {
      const bg = parse(getComputedStyle(stack[i]).backgroundColor);
      if (bg && bg.a > 0) {
        layers.push(bg);
        if (bg.a >= 0.999) break;
      }
    }
    let ground = { r: 255, g: 255, b: 255, a: 1 };
    for (let k = layers.length - 1; k >= 0; k -= 1) ground = over(layers[k], ground);
    return hex(ground);
  }
  function describe(el) {
    if (!el) return null;
    return { el: sel(el), text: textOf(el), ...styleOf(el), painted: paintedAt(el), before: styleOf(el, '::before'), after: styleOf(el, '::after') };
  }
  window.__vp = { parse, hex, ratio, over, seaScan, sparkScan, contrastScan, logoScan, statusScan, focusInfo, overflow, settled, rectOf, styleOf, paintedAt, describe, sel, token, textOf, visible, mutations: () => mutations };
})();
