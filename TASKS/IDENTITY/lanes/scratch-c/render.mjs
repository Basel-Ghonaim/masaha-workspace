// Lane C (IDENTITY): renders the browser icons' rasters in headless Chrome over CDP, with Node 24's
// built-in WebSocket (no dependency), then stops the Chrome it started by its PID.
//   node render.mjs            (through heavy.mjs: a Chrome batch is heavy)
// Each image: the SVG as an <img> at its pixel size, in a page whose viewport is exactly that size,
// at device scale 1, the default background overridden (transparent for the .ico art, white for
// the 180 and the 120), captured as PNG. Writes out/*.png; the 120 also to the Google path.
import { execFileSync, spawn } from 'node:child_process';
import { copyFileSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { createServer } from 'node:net';
import { join } from 'node:path';

const HERE = import.meta.dirname;
const LOGO = 'C:/dev/masaha/app-design-lane-c/docs/design/prototype/masaha/logo';
const APP_ICON = `${LOGO}/masaha-app-icon-berry.svg`;
const MARK = `${LOGO}/masaha-mark-berry.svg`;
const MARK_DARK = `${LOGO}/masaha-mark-dark-berry.svg`;
const FAVICON = join(HERE, 'favicon.svg');
const OUT = join(HERE, 'out');
const GOOGLE = 'C:/dev/masaha/workspace/TASKS/IDENTITY/google/masaha-logo-120.png';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
mkdirSync(OUT, { recursive: true });

const TRANSPARENT = { r: 0, g: 0, b: 0, a: 0 };
const WHITE = { r: 255, g: 255, b: 255, a: 1 };
const dataUrl = (path, type) => `data:${type};base64,${readFileSync(path).toString('base64')}`;
const svg = (path) => dataUrl(path, 'image/svg+xml');
const png = (path) => dataUrl(path, 'image/png');
const out = (name) => join(OUT, name);
const page = (body) =>
  `<!doctype html><html><head><style>html,body{margin:0;padding:0;background:transparent;overflow:hidden}img{display:block}</style></head><body>${body}</body></html>`;

const port = await new Promise((resolve, reject) => {
  const server = createServer();
  server.on('error', reject);
  server.listen(0, '127.0.0.1', () => {
    const { port: free } = server.address();
    server.close(() => resolve(free));
  });
});
const chrome = spawn(
  CHROME,
  [
    '--headless=new',
    `--remote-debugging-port=${port}`,
    `--user-data-dir=${join(HERE, 'cdp-profile')}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--hide-scrollbars',
    '--mute-audio',
    'about:blank',
  ],
  { stdio: 'ignore' },
);
console.log(`chrome pid ${chrome.pid}, port ${port}`);

let ws;
let nextId = 0;
const pending = new Map();
const send = (method, params = {}) =>
  new Promise((resolve, reject) => {
    const id = ++nextId;
    pending.set(id, { resolve, reject, method });
    ws.send(JSON.stringify({ id, method, params }));
  });
const evaluate = async (expression) => {
  const { result, exceptionDetails } = await send('Runtime.evaluate', {
    expression,
    awaitPromise: true,
    returnByValue: true,
  });
  if (exceptionDetails) throw new Error(exceptionDetails.exception?.description ?? exceptionDetails.text);
  return result.value;
};
const setPage = (html) =>
  evaluate(`(async () => {
    document.documentElement.innerHTML = ${JSON.stringify(html.replace(/^<!doctype html><html>|<\/html>$/g, ''))};
    await Promise.all([...document.images].map((img) => img.decode()));
    await new Promise((done) => requestAnimationFrame(() => requestAnimationFrame(done)));
    return true;
  })()`);
const scheme = (value) =>
  send('Emulation.setEmulatedMedia', { media: '', features: [{ name: 'prefers-color-scheme', value }] });

async function capture({ width, height, background, body, file }) {
  await send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: false });
  await send('Emulation.setDefaultBackgroundColorOverride', { color: background });
  await setPage(page(body));
  const size = await evaluate('[innerWidth, innerHeight, devicePixelRatio]');
  if (size[0] !== width || size[1] !== height || size[2] !== 1) throw new Error(`viewport ${size} for ${file}`);
  const { data } = await send('Page.captureScreenshot', { format: 'png' });
  writeFileSync(file, Buffer.from(data, 'base64'));
  const bytes = readFileSync(file);
  console.log(`${file}: ${bytes.readUInt32BE(16)} x ${bytes.readUInt32BE(20)}, ${bytes.length} bytes`);
  return file;
}

// In the page: an image's pixels through a canvas (data: URLs never taint it).
const PIXELS = `async function pixels(src, w, h) {
  const img = new Image(); img.src = src; await img.decode();
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  const ctx = c.getContext('2d'); ctx.drawImage(img, 0, 0, w, h);
  return ctx.getImageData(0, 0, w, h).data;
}`;

async function compare(a, b, size) {
  return evaluate(`(async () => { ${PIXELS}
    const [p, q] = await Promise.all([pixels(${JSON.stringify(png(a))}, ${size}, ${size}), pixels(${JSON.stringify(png(b))}, ${size}, ${size})]);
    let differing = 0, worst = 0;
    for (let i = 0; i < p.length; i += 4) {
      const d = Math.max(Math.abs(p[i]-q[i]), Math.abs(p[i+1]-q[i+1]), Math.abs(p[i+2]-q[i+2]), Math.abs(p[i+3]-q[i+3]));
      worst = Math.max(worst, d); if (d > 8) differing += 1;
    }
    return { differing, worst, of: p.length / 4 };
  })()`);
}

try {
  let target;
  for (let tries = 0; tries < 100 && !target; tries += 1) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
      target = list.find((entry) => entry.type === 'page')?.webSocketDebuggerUrl;
    } catch {
      // not up yet
    }
    if (!target) await new Promise((done) => setTimeout(done, 200));
  }
  if (!target) throw new Error('no page target');
  ws = new WebSocket(target);
  await new Promise((resolve, reject) => {
    ws.onopen = resolve;
    ws.onerror = reject;
  });
  ws.onmessage = ({ data }) => {
    const message = JSON.parse(data);
    const waiting = pending.get(message.id);
    if (!waiting) return;
    pending.delete(message.id);
    if (message.error) waiting.reject(new Error(`${waiting.method}: ${message.error.message}`));
    else waiting.resolve(message.result);
  };
  await send('Page.enable');
  await send('Runtime.enable');
  await scheme('light');

  // 1. The rasters.
  for (const px of [16, 32, 48]) {
    await capture({
      width: px,
      height: px,
      background: TRANSPARENT,
      body: `<img src="${svg(APP_ICON)}" width="${px}" height="${px}" alt="">`,
      file: out(`ico-${px}.png`),
    });
  }
  await capture({
    width: 180,
    height: 180,
    background: WHITE,
    body: `<img src="${svg(MARK)}" width="180" height="180" alt="">`,
    file: out('apple-touch-icon.png'),
  });

  // The 120: the mark at 96 px, centred (12 px of white all round its square), whole pixels so Chrome
  // draws the SVG at its size and never resamples a bitmap (a fractional size left a light seam where
  // the mark's two mirrored halves meet). The mark's drawn pixels are measured first, to prove its
  // farthest pixel stays within 80 % of the 120's circle (48 px): a round crop keeps >= 12 px clear.
  const N = 1556;
  const measure = await evaluate(`(async () => { ${PIXELS}
    const p = await pixels(${JSON.stringify(svg(MARK))}, ${N}, ${N});
    let minX = ${N}, minY = ${N}, maxX = -1, maxY = -1;
    for (let y = 0; y < ${N}; y += 1) for (let x = 0; x < ${N}; x += 1) if (p[(y * ${N} + x) * 4 + 3] > 0) {
      minX = Math.min(minX, x); maxX = Math.max(maxX, x); minY = Math.min(minY, y); maxY = Math.max(maxY, y);
    }
    const cx = (minX + maxX + 1) / 2, cy = (minY + maxY + 1) / 2;
    let maxR = 0;
    for (let y = minY; y <= maxY; y += 1) for (let x = minX; x <= maxX; x += 1) if (p[(y * ${N} + x) * 4 + 3] > 0) {
      const dx = Math.max(Math.abs(x - cx), Math.abs(x + 1 - cx)), dy = Math.max(Math.abs(y - cy), Math.abs(y + 1 - cy));
      maxR = Math.max(maxR, Math.hypot(dx, dy));
    }
    return { minX, minY, maxX, maxY, cx, cy, maxR };
  })()`);
  const layout = { size: 96, left: 12, top: 12 };
  const farthest = (measure.maxR * layout.size) / N;
  const offCentre = [measure.cx, measure.cy].map((c) => (c / N - 0.5) * layout.size);
  if (farthest > 48) throw new Error(`the mark's farthest pixel at ${farthest} px > 48`);
  console.log('the 120: farthest pixel', farthest.toFixed(2), 'px; the drawing\'s centre off by', offCentre.map((d) => d.toFixed(2)).join(', '), 'px');
  console.log('the mark at', N, 'px:', JSON.stringify(measure), '-> 120 layout', JSON.stringify(layout));
  await capture({
    width: 120,
    height: 120,
    background: WHITE,
    body: `<img src="${svg(MARK)}" style="position:absolute;left:${layout.left}px;top:${layout.top}px;width:${layout.size}px;height:${layout.size}px" alt="">`,
    file: out('masaha-logo-120.png'),
  });
  // Its check: every pixel at or beyond 56 px from the centre is pure white; the farthest ink's radius.
  const google = await evaluate(`(async () => { ${PIXELS}
    const p = await pixels(${JSON.stringify(png(out('masaha-logo-120.png')))}, 120, 120);
    let outside = 0, farthest = 0, inked = 0;
    for (let y = 0; y < 120; y += 1) for (let x = 0; x < 120; x += 1) {
      const i = (y * 120 + x) * 4, white = p[i] === 255 && p[i+1] === 255 && p[i+2] === 255 && p[i+3] === 255;
      const r = Math.hypot(x + 0.5 - 60, y + 0.5 - 60);
      if (!white) { inked += 1; farthest = Math.max(farthest, r); if (r >= 56) outside += 1; }
    }
    return { inked, farthest, notWhiteAtOrBeyond56: outside };
  })()`);
  console.log('120 check:', JSON.stringify(google));
  copyFileSync(out('masaha-logo-120.png'), GOOGLE);
  console.log(`copied to ${GOOGLE}`);

  // 2. The favicon SVG against the owner's marks, drawn at 64 px: light, then the browser's dark.
  for (const [value, reference] of [
    ['light', MARK],
    ['dark', MARK_DARK],
  ]) {
    await scheme(value);
    const ours = await capture({
      width: 64,
      height: 64,
      background: TRANSPARENT,
      body: `<img src="${svg(FAVICON)}" width="64" height="64" alt="">`,
      file: out(`favicon-${value}-64.png`),
    });
    const theirs = await capture({
      width: 64,
      height: 64,
      background: TRANSPARENT,
      body: `<img src="${svg(reference)}" width="64" height="64" alt="">`,
      file: out(`reference-${value}-64.png`),
    });
    console.log(`favicon.svg vs ${reference.split('/').pop()} (${value}):`, JSON.stringify(await compare(ours, theirs, 64)));
    for (const px of [16, 32]) {
      await capture({
        width: px,
        height: px,
        background: TRANSPARENT,
        body: `<img src="${svg(FAVICON)}" width="${px}" height="${px}" alt="">`,
        file: out(`favicon-${value}-${px}.png`),
      });
    }
  }
  await scheme('light');

  // 3. Previews to look at: each raster at 1x and 8x (pixelated) on a light and a dark tab strip.
  const tile = (src, px, zoom) =>
    `<img src="${src}" width="${px * zoom}" height="${px * zoom}" style="image-rendering:pixelated;margin:8px" alt="">`;
  const strip = (ground, items) =>
    `<div style="display:flex;align-items:center;background:${ground};padding:8px">${items.join('')}</div>`;
  const icoTiles = (zoom) => [16, 32, 48].map((px) => tile(png(out(`ico-${px}.png`)), px, zoom));
  await capture({
    width: 900,
    height: 560,
    background: WHITE,
    body:
      strip('#f1f3f4', [...icoTiles(1), ...icoTiles(4)]) +
      strip('#202124', [...icoTiles(1), ...icoTiles(4)]) +
      strip('#ffffff', [tile(png(out('ico-16.png')), 16, 8), tile(png(out('ico-32.png')), 32, 4)]),
    file: out('preview-ico.png'),
  });
  await capture({
    width: 700,
    height: 330,
    background: WHITE,
    body:
      strip('#f1f3f4', [
        tile(png(out('favicon-light-16.png')), 16, 1),
        tile(png(out('favicon-light-32.png')), 32, 1),
        tile(png(out('favicon-light-16.png')), 16, 8),
        tile(png(out('favicon-light-32.png')), 32, 4),
      ]) +
      strip('#202124', [
        tile(png(out('favicon-dark-16.png')), 16, 1),
        tile(png(out('favicon-dark-32.png')), 32, 1),
        tile(png(out('favicon-dark-16.png')), 16, 8),
        tile(png(out('favicon-dark-32.png')), 32, 4),
      ]),
    file: out('preview-favicon.png'),
  });
  await capture({
    width: 520,
    height: 520,
    background: { r: 200, g: 200, b: 200, a: 1 },
    body: `<div style="position:relative;margin:20px;width:480px;height:480px"><img src="${png(out('masaha-logo-120.png'))}" width="480" height="480" style="image-rendering:pixelated" alt=""><div style="position:absolute;inset:0;border-radius:50%;outline:2px solid #e00;outline-offset:-1px"></div><div style="position:absolute;inset:48px;border-radius:50%;outline:1px dashed #08f"></div></div>`,
    file: out('preview-120.png'),
  });
  // The bottom of the mark, close: the owner's mark at 778 px (one viewBox unit a pixel), its last 140
  // rows shown at 3x; and the 32 px favicon at 12x.
  await capture({
    width: 900,
    height: 820,
    background: WHITE,
    body: `<div style="width:${778 * 1}px;height:140px;overflow:hidden;transform:scale(1.1);transform-origin:0 0"><img src="${svg(MARK)}" width="778" height="778" style="margin-top:-638px" alt=""></div><div style="margin-top:60px">${tile(png(out('favicon-light-32.png')), 32, 12)}${tile(png(out('reference-light-64.png')), 64, 6)}</div>`,
    file: out('preview-bottom.png'),
  });
} finally {
  try {
    if (ws?.readyState === WebSocket.OPEN) ws.close();
  } catch {
    // closing anyway
  }
  // Stop the Chrome this script started, by its PID and its children only, never another Chrome.
  try {
    execFileSync('taskkill', ['/PID', String(chrome.pid), '/T', '/F'], { stdio: 'pipe' });
  } catch (error) {
    // A child already gone makes taskkill report an error; the check below is what counts.
    console.log(`taskkill ${chrome.pid}: ${String(error.stderr ?? error.message).trim()}`);
  }
  await new Promise((done) => setTimeout(done, 1000));
  const left = execFileSync('tasklist', ['/FI', `PID eq ${chrome.pid}`, '/NH'], { encoding: 'utf8' });
  console.log(
    left.includes(String(chrome.pid)) ? `chrome pid ${chrome.pid} STILL RUNNING` : `chrome pid ${chrome.pid} stopped, none left`,
  );
}
