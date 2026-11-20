// EC13: the prototype beside production, 1440, light and dark: the primary button (rest and
// hovered), the sidebar's current item, a chip that is on, a hover. Serves docs/design/prototype with
// python's http.server on a free port, stopped by its PID at the end.
import { execSync, spawn } from 'node:child_process';
import { createServer } from 'node:net';
import { launch, RAW, sleep } from './lib.mjs';
import { curate, Results } from './checks.mjs';

const results = new Results('proto');
const port = await new Promise((resolve) => {
  const s = createServer();
  s.listen(0, '127.0.0.1', () => {
    const { port: p } = s.address();
    s.close(() => resolve(p));
  });
});
const server = spawn('python', ['-m', 'http.server', String(port), '--bind', '127.0.0.1', '--directory', 'C:/dev/masaha/app-design/docs/design/prototype'], { stdio: 'ignore' });
const page = await launch('proto');
page.log(`http.server pid ${server.pid} on ${port}`);
const P = `http://127.0.0.1:${port}`;

const READ = `(() => {
  const v = window.__vp;
  const vis = (e) => v.visible(e);
  const first = (q, f = () => true) => [...document.querySelectorAll(q)].filter(vis).find(f);
  const primary = first('button, a', (e) => /(^|\\s)bg-primary(\\s|$)/.test(e.getAttribute('class') || ''));
  const current = first('[data-slot=sidebar-menu-button][data-active=true], [data-sidebar=menu-button][data-active=true], [aria-current=page]');
  const chipOn = first('[data-slot=toggle-group-item][data-state=on], [role=radio][data-state=on][data-slot=toggle-group-item]');
  const chipOff = first('[data-slot=toggle-group-item][data-state=off]');
  const sideOther = first('[data-slot=sidebar-menu-button]:not([data-active=true]), [data-sidebar=menu-button]:not([data-active=true])');
  const outline = first('button, a', (e) => /border-\\(--card-border\\)|variant-outline|(^|\\s)bg-card(\\s|$)/.test(e.getAttribute('class') || '') && /hover:bg/.test(e.getAttribute('class') || ''));
  const d = (e) => e ? { ...v.describe(e), cls: (e.getAttribute('class') || '').slice(0, 300) } : null;
  return { identity: document.documentElement.dataset.identity ?? null, theme: document.documentElement.dataset.theme ?? 'light', primary: d(primary), current: d(current), chipOn: d(chipOn), chipOff: d(chipOff), sideOther: d(sideOther), outline: d(outline),
    tokens: Object.fromEntries(['primary', 'accent', 'hover', 'spark', 'ring', 'sidebar-accent', 'hover-on-muted', 'primary-hover'].map((t) => [t, v.hex(v.parse(v.token(t))) + (v.parse(v.token(t))?.a < 1 ? '@' + v.parse(v.token(t)).a.toFixed(2) : '')])) };
})()`;

async function hoverRead(expr) {
  const r = await page.evaluate(`(() => { const e = (${expr}); if (!e) return null; e.scrollIntoView({ block: 'center' }); const b = e.getBoundingClientRect(); return { x: b.left + b.width / 2, y: b.top + b.height / 2 }; })()`);
  if (!r) return null;
  await page.mouse(r.x, r.y);
  await sleep(500);
  const out = await page.evaluate(`(() => { const e = (${expr}); return e ? window.__vp.describe(e) : null; })()`);
  await page.mouse(2, 2);
  await sleep(300);
  return out;
}

try {
  await page.viewport(1440, 900);
  const pages = ['Desk.html', 'Directory.html', 'Owner overview.html', 'Admin spaces.html'];
  for (const file of pages) {
    for (const theme of ['light', 'dark']) {
      const url = `${P}/${encodeURI(file)}?lang=en${theme === 'dark' ? '&theme=dark' : ''}`;
      await page.goto(url);
      await sleep(2500);
      await page.waitIdle({ quiet: 800 });
      const read = await page.evaluate(READ);
      const vis = `(q, f = () => true) => [...document.querySelectorAll(q)].filter((e) => window.__vp.visible(e)).find(f)`;
      read.primaryHover = await hoverRead(`(${vis})('button, a', (e) => /(^|\\s)bg-primary(\\s|$)/.test(e.getAttribute('class') || ''))`);
      read.sideOtherHover = await hoverRead(`(${vis})('[data-slot=sidebar-menu-button]:not([data-active=true])')`);
      read.currentHover = await hoverRead(`(${vis})('[data-slot=sidebar-menu-button][data-active=true]')`);
      read.chipOffHover = await hoverRead(`(${vis})('[data-slot=toggle-group-item][data-state=off]')`);
      read.chipOnHover = await hoverRead(`(${vis})('[data-slot=toggle-group-item][data-state=on]')`);
      read.outlineHover = await hoverRead(`(${vis})('button, a', (e) => /hover:bg-hover/.test(e.getAttribute('class') || '') && /border/.test(e.getAttribute('class') || ''))`);
      read.console = page.takeConsole().filter((c) => !/favicon/.test(c.text)).slice(0, 5);
      const shot = `${RAW}/proto-${file.replace(/\W+/g, '-')}-${theme}.png`;
      await page.shot(shot);
      if (file === 'Desk.html') curate(results, shot, `52-prototype-desk-${theme}-en-1440.png`);
      results.data.ec[`${file}-${theme}`] = read;
      results.save();
      page.log(`proto ${file} ${theme}: identity ${read.identity}; primary ${read.primary?.bgHex}/${read.primaryHover?.bgHex}; current ${read.current?.bgHex} bar ${read.current?.before?.bgHex}; chip on ${read.chipOn?.bgHex} border ${read.chipOn?.border}; hover side ${read.sideOtherHover?.bgHex} chip ${read.chipOffHover?.bgHex} outline ${read.outlineHover?.bgHex}; tokens ${JSON.stringify(read.tokens)}`);
    }
  }
} catch (error) {
  page.log(`ERROR ${error.stack}`);
  results.note(`ERROR ${error.message}`);
} finally {
  results.save();
  results.data.chrome = await page.close();
  try {
    execSync(`taskkill /PID ${server.pid} /T /F`, { stdio: 'ignore' });
  } catch {
    // gone
  }
  await sleep(800);
  const free = await new Promise((resolve) => {
    const s = createServer();
    s.once('error', () => resolve(false));
    s.listen(port, '127.0.0.1', () => s.close(() => resolve(true)));
  });
  results.data.httpServer = { pid: server.pid, port, portFreeAfter: free };
  page.log(`http.server ${server.pid} stopped by PID; port ${port} free: ${free}`);
  results.save();
}
