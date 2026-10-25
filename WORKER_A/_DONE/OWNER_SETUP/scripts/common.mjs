// Pieces shared by PR 2's real-run scripts. Passwords are read from apps/api/.env and never printed.
import { readFileSync, writeFileSync } from 'node:fs';
import { byText, driver, launch, SHOTS } from './cdp.mjs';

const ENV = Object.fromEntries(
  readFileSync('C:/dev/masaha/app/apps/api/.env', 'utf8')
    .split(/\r?\n/)
    .filter((line) => /^[A-Z_]+=/.test(line))
    .map((line) => {
      const at = line.indexOf('=');
      return [line.slice(0, at), line.slice(at + 1).replace(/^"|"$/g, '')];
    }),
);

export const OWNER = { email: 'demo-owner@example.com', password: ENV.SEED_DEMO_PASSWORD };
export const RECEPTION = { email: 'demo-reception@example.com', password: ENV.SEED_DEMO_PASSWORD };
export const ADMIN = { email: ENV.SEED_ADMIN_EMAIL, password: ENV.SEED_ADMIN_PASSWORD };
export { byText };

export const log = (...a) => console.log('·', ...a);

/** Starts Chrome at `width`, the run's language and theme, signed in as `who`, on `path`. */
export async function start({ language, theme, width = 1440, who, path }) {
  const b = await launch();
  console.log('chrome pid', b.pid);
  const d = driver(b);
  // The API calls the page makes, for the network log.
  const requests = [];
  await b.send('Network.enable');
  b.on((m) => {
    if (m.method === 'Network.requestWillBeSent' && m.params.request.url.includes('/api/v1/')) {
      requests.push(`${m.params.request.method} ${m.params.request.url.replace(/^.*\/api\/v1/, '')}`);
    }
  });
  d.requests = requests;
  await d.viewport(width, 900);
  await d.theme(theme === 'dark');
  await d.go('/login');
  await d.prefs(language, theme);
  await d.go(`/login?next=${encodeURIComponent(path)}`);
  await d.until(`!!document.querySelector('input[type=email]')`, 'login form');
  await d.type('input[type=email]', who.email);
  await d.type('input[type=password]', who.password);
  await d.click(`document.querySelector('form button[type=submit]')`, 'sign in');
  await d.until(`location.pathname === ${JSON.stringify(path)}`, 'landing on ' + path, 20000);
  await d.sleep(1200);
  // A sign-in takes the account's language: set the run's again, and reload once.
  await d.prefs(language, theme);
  await d.go(path);
  d.nav = async (to) => {
    await d.evaluate(
      `history.pushState(null, '', ${JSON.stringify(to)}); dispatchEvent(new PopStateEvent('popstate')); true`,
    );
    await d.sleep(1200);
  };
  d.toasts = () =>
    d.evaluate(
      `[...document.querySelectorAll('[data-sonner-toast]')].map((t) => t.innerText.replace(/[\\u2066-\\u2069]/g, '').replace(/\\n/g, ' / ')).join(' || ')`,
    );
  d.dialogText = () =>
    d.evaluate(
      `(() => { const el = [...document.querySelectorAll('[role=dialog],[role=alertdialog]')].pop(); return el ? el.innerText.replace(/[\\u2066-\\u2069]/g, '').replace(/\\n+/g, ' / ') : null; })()`,
    );
  /** The card of the section whose h2 is `title`. */
  d.section = (title) =>
    `[...document.querySelectorAll('[data-slot=card]')].find((c) => c.querySelector('h2')?.textContent === ${JSON.stringify(title)})`;
  d.sectionText = (title) => d.text(d.section(title));
  /** Scrolls the section into view and shoots the viewport. */
  d.shotSection = async (title, name, height) => {
    await d.evaluate(`(() => { const el = ${d.section(title)}; el?.scrollIntoView({ block: 'start' }); return true; })()`);
    await d.sleep(400);
    await d.shot(name, height);
  };
  /** Types `text` into the element `expression` gives, its old value selected first. */
  d.typeAt = async (expression, text) => {
    const ok = await d.evaluate(`(() => { const el = ${expression}; if (!el) return false; el.scrollIntoView({ block: 'center' }); el.focus(); el.select?.(); return true; })()`);
    if (!ok) throw new Error('no field to type in');
    await b.send('Input.insertText', { text });
    await d.sleep(150);
  };
  d.saveLog = (name) => writeFileSync(`${SHOTS}/${name}.txt`, requests.join('\n') + '\n');
  return { b, d };
}

export async function step(name, body) {
  try {
    await body();
  } catch (error) {
    console.log('FAILED', name, String(error.message ?? error));
  }
}

export function stop(b) {
  try {
    b.chrome.kill();
  } catch {
    /* gone */
  }
}
