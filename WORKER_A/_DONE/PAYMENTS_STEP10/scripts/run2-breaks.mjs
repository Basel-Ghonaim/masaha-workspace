// The real run's width breaks (plan §13): a layout drawn by classes alone, broken once from a backup copy on the
// dev server (Vite reloads it), measured and shot, then restored by copy. Also the card's heart's touch area.
// Usage: node run2-breaks.mjs
import { copyFileSync, readFileSync, writeFileSync } from 'node:fs';
import { byText, driver, launch } from './cdp2.mjs';

const APP = 'C:/dev/masaha/app/apps/web/src/';
const S = 'C:/dev/masaha/workspace/WORKER_A/PAYMENTS_STEP10/scripts/';
const env = readFileSync('C:/dev/masaha/app/apps/api/.env', 'utf8');
const PASSWORD = /^SEED_DEMO_PASSWORD=(.*)$/m.exec(env)?.[1]?.trim().replace(/^["']|["']$/g, '');

async function signedIn(width, landing) {
  const b = await launch();
  const d = driver(b);
  d.b = b;
  await d.viewport(width, 900);
  await d.go('/');
  await d.prefs('ar', 'light');
  await d.go(`/login?next=${encodeURIComponent(landing)}`);
  await d.until(`!!document.querySelector('input[type=email]')`, 'login form');
  await d.type('input[type=email]', 'demo-reception@example.com');
  await d.type('input[type=password]', PASSWORD);
  await d.click(`document.querySelector('form button[type=submit]')`, 'sign in');
  await d.until(`location.pathname === ${JSON.stringify(landing)}`, 'landing', 20000);
  await d.prefs('ar', 'light');
  await d.go(landing);
  await d.sleep(2500);
  return { b, d };
}

async function withBreak(file, from, to, run) {
  const bak = `${S}bak-run-break-${file.split('/').pop()}`;
  copyFileSync(APP + file, bak);
  try {
    const source = readFileSync(APP + file, 'utf8');
    if (!source.includes(from)) throw new Error(`no ${from} in ${file}`);
    writeFileSync(APP + file, source.split(from).join(to));
    await new Promise((r) => setTimeout(r, 1500));
    await run();
  } finally {
    copyFileSync(bak, APP + file);
    console.log('restored', readFileSync(APP + file, 'utf8') === readFileSync(bak, 'utf8'));
  }
}

const grid = (d) =>
  d.evaluate(`(() => { const t = document.querySelector('[role=dialog] input[type=time]'); const g = t?.closest('.grid'); return g ? getComputedStyle(g).gridTemplateColumns : 'none'; })()`);
const favGrid = (d) =>
  d.evaluate(`(() => { const g = [...document.querySelectorAll('main .grid')].find((x) => x.querySelector('a[href^="/spaces/"]')); return g ? getComputedStyle(g).gridTemplateColumns : 'none'; })()`);

// The favourites' grid at 1440: three columns, then two with `xl:grid-cols-3` removed.
{
  const { b, d } = await signedIn(1440, '/me/favorites');
  console.log('favourites at 1440:', await favGrid(d));
  await d.shot('4b-favorites-grid-reception-ar-light-1440', 1400);
  await withBreak('features/directory/components/favorites/FavoritesView.tsx', 'grid gap-4 md:grid-cols-2 xl:grid-cols-3">\n', 'grid gap-4 md:grid-cols-2">\n', async () => {
    await d.go('/me/favorites');
    await d.sleep(2500);
    console.log('favourites at 1440, the break:', await favGrid(d));
    await d.shot('break-favorites-grid-reception-ar-light-1440', 1400);
  });
  // The card's heart, with touch emulation at 390.
  await d.viewport(390, 900);
  await d.b.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  await d.go('/spaces');
  await d.sleep(3000);
  console.log(
    'touch, the card heart:',
    await d.evaluate(`(() => { const el = [...document.querySelectorAll('main button[aria-pressed]')].find((x) => /المفضّلة/.test(x.getAttribute('aria-label') ?? '')); const r = el.getBoundingClientRect(); return Math.round(r.width) + 'x' + Math.round(r.height) + ' ' + el.getAttribute('aria-label'); })()`),
  );
  b.chrome.kill();
}
process.exit(0);
