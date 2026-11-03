// Probe: one role, one path, one language; prints the page's exceptions and console errors, and its main text.
// Usage: node probe.mjs <owner|admin|reception> <path> <ar|en>
import { readFileSync } from 'node:fs';
import { driver, launch } from './cdp.mjs';

const env = readFileSync('C:/dev/masaha/app/apps/api/.env', 'utf8');
const value = (name) =>
  new RegExp(`^${name}=(.*)$`, 'm').exec(env)?.[1]?.trim().replace(/^["']|["']$/g, '');
const ACCOUNTS = {
  owner: ['demo-owner@example.com', value('SEED_DEMO_PASSWORD')],
  reception: ['demo-reception@example.com', value('SEED_DEMO_PASSWORD')],
  admin: [value('SEED_ADMIN_EMAIL'), value('SEED_ADMIN_PASSWORD')],
};
const [role, path, language] = process.argv.slice(2);
const b = await launch();
const d = driver(b);
const errors = [];
b.on((m) => {
  if (m.method === 'Runtime.exceptionThrown') {
    const e = m.params.exceptionDetails;
    errors.push(`EXC ${e.exception?.description ?? e.text}`.slice(0, 1500));
  }
  if (m.method === 'Runtime.consoleAPICalled' && m.params.type !== 'log' && m.params.type !== 'debug') {
    errors.push(`CONSOLE ${m.params.args.map((a) => a.value ?? a.description ?? '').join(' ')}`.slice(0, 1500));
  }
});
await d.viewport(1440, 900);
await d.go('/');
await d.prefs(language, language === 'en' ? 'dark' : 'light');
const [email, password] = ACCOUNTS[role];
await d.go('/login');
await d.until(`!!document.querySelector('input[type=email]')`, 'login form');
await d.type('input[type=email]', email);
await d.type('input[type=password]', password);
await d.click(`document.querySelector('form button[type=submit]')`, 'sign in');
await d.until(`location.pathname !== '/login'`, 'signed in', 20000);
await d.sleep(1500);
if ((await d.evaluate('document.documentElement.lang')) !== language) {
  const label = language === 'en' ? 'English' : 'العربية';
  await d.click(`[...document.querySelectorAll('button')].find((el) => el.textContent.trim() === ${JSON.stringify(label)} && el.offsetParent !== null)`, 'toggle');
  await d.sleep(1500);
}
await d.go(path);
await d.sleep(4000);
console.log('lang', await d.evaluate('document.documentElement.lang'), 'path', await d.evaluate('location.pathname'));
console.log('TEXT', (await d.evaluate(`document.body.innerText`)).replace(/\s+/g, ' ').slice(0, 600));
for (const e of errors) console.log(e);
b.chrome.kill();
