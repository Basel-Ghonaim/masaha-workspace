// r3-inventory — merges tools\inv\<PART>.json into tools\inventory.json (what r3-pack reads) and writes
// ROUND3\INVENTORY.md: every route of the web at the head, mapped to foundation §13's screens and to one
// part, then every base state the pack captures, how it is reached, and what is left out and why.
// Usage: node r3-inventory.mjs <head sha>
import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROUND3 = resolve(HERE, '..');
const HEAD = process.argv[2] || '(not pinned yet)';
const PARTS = ['PU', 'AU', 'OW', 'DK', 'AD', 'SH'];
const all = PARTS.flatMap((p) => JSON.parse(readFileSync(join(HERE, 'inv', p + '.json'), 'utf8')));
writeFileSync(join(HERE, 'inventory.json'), JSON.stringify(all, null, 1));

const ROUTES = [
  ['`/`', 'site', '1 Home', 'PU', 'visitor, user'],
  ['`/spaces`', 'site', '2 Directory (list; `?view=map` the map)', 'PU', 'visitor, user'],
  ['`/spaces/:slug`', 'site', '3 Space details', 'PU', 'visitor, user'],
  ['`/about`', 'site', '4 About / Contact', 'PU', 'visitor, user'],
  ['`/privacy`', 'site', '33 Privacy policy', 'PU', 'visitor, user'],
  ['`*` (site)', 'site', '8 404', 'PU', 'visitor, user'],
  ['`/login`', 'focus', '5 Sign in', 'AU', 'visitor'],
  ['`/register`', 'focus', '6 Register', 'AU', 'visitor'],
  ['`/forgot-password`', 'focus', '7 Forgot password', 'AU', 'visitor'],
  ['`/reset-password#token=…`', 'focus', '7 Reset password', 'AU', 'anyone'],
  ['`/change-password`', 'focus (sign-out only)', '9 (the forced change)', 'AU', 'user with a temporary password'],
  ['`/me`', 'site › account', '9 Profile & settings', 'AU', 'user (any signed-in role)'],
  ['`/me/favorites`', 'site › account', '10 Favourites', 'AU', 'user'],
  ['`/me/reports`', 'site › account', '11 My reports', 'AU', 'user'],
  ['`/dashboard`', 'none (redirect)', '— the landing: to the admin, the owner\'s overview or reception\'s desk', 'SH', 'owner, reception, admin'],
  ['`/dashboard/spaces/:id`', 'space dashboard', '12 Overview (O)', 'OW', 'owner'],
  ['`/dashboard/spaces/:id/desk`', 'space dashboard', '13 Front desk (O+R)', 'DK', 'owner, reception'],
  ['`/dashboard/spaces/:id/customers`', 'space dashboard', '14 Customers (O+R)', 'DK', 'owner, reception'],
  ['`/dashboard/spaces/:id/customers/:customerId`', 'space dashboard', '15 Customer details (O+R); 16 New subscription opens from it and the desk', 'DK', 'owner, reception'],
  ['`/dashboard/spaces/:id/payments`', 'space dashboard', '17 Payments (O: the ledger)', 'OW', 'owner'],
  ['`/dashboard/spaces/:id/my-payments`', 'space dashboard', '17 Payments (R: my payments today)', 'DK', 'reception'],
  ['`/dashboard/spaces/:id/finance`', 'space dashboard', '19 Finance & statistics (O)', 'OW', 'owner'],
  ['`/dashboard/spaces/:id/packages`', 'space dashboard', '21 Prices & packages (O)', 'OW', 'owner'],
  ['`/dashboard/spaces/:id/profile`', 'space dashboard', '20 Space profile (O)', 'OW', 'owner'],
  ['`/dashboard/spaces/:id/announcements`', 'space dashboard', '18 Announcements (O+R)', 'OW (owner) · DK (reception\'s view)', 'owner, reception'],
  ['`/dashboard/spaces/:id/reports`', 'space dashboard', '23 Data reports (O)', 'OW', 'owner'],
  ['`/dashboard/spaces/:id/staff`', 'space dashboard', '22 Staff (O)', 'OW', 'owner'],
  ['`/dashboard/spaces/:id/audit`', 'space dashboard', '31 Audit log (the owner\'s, O13)', 'OW', 'owner'],
  ['`/dashboard/spaces/:id/settings`', 'space dashboard', '24 Settings (O)', 'OW', 'owner'],
  ['`/dashboard/spaces/:id/*`', 'space dashboard', '404 / 403 inside the shell', 'SH', 'owner, reception'],
  ['`/dashboard/admin`', 'admin dashboard', '25 Overview', 'AD', 'admin'],
  ['`/dashboard/admin/spaces`', 'admin dashboard', '26 Spaces', 'AD', 'admin'],
  ['`/dashboard/admin/spaces/new`', 'admin dashboard', '26 Spaces (add)', 'AD', 'admin'],
  ['`/dashboard/admin/spaces/:spaceId`', 'admin dashboard', '26 Spaces (the editor; 27 linking an owner from it)', 'AD', 'admin'],
  ['`/dashboard/admin/owners`', 'admin dashboard', '27 Space owners', 'AD', 'admin'],
  ['`/dashboard/admin/reports`', 'admin dashboard', '28 Data reports', 'AD', 'admin'],
  ['`/dashboard/admin/users`', 'admin dashboard', '29 Users', 'AD', 'admin'],
  ['`/dashboard/admin/lookups`', 'admin dashboard', '30 Lookups', 'AD', 'admin'],
  ['`/dashboard/admin/audit`', 'admin dashboard', '31 Audit log (the admin\'s)', 'AD', 'admin'],
  ['`/dashboard/admin/settings`', 'admin dashboard', '32 Settings', 'AD', 'admin'],
  ['`/dashboard/admin/*`', 'admin dashboard', '404 inside the shell', 'SH', 'admin'],
  ['`/__showcase[/<category>[/<slug>]]`', 'development only', 'the design system (foundation §3, §12)', 'SH', 'anyone, development'],
];

const how = (b) => {
  const h = [];
  if (b.steps) h.push(b.steps.length + ' step' + (b.steps.length > 1 ? 's' : ''));
  if (b.hold) h.push('held ' + b.hold.url);
  for (const f of [].concat(b.fail || [])) h.push((f.status === 0 ? 'aborted' : f.status) + ' on ' + f.url);
  for (const m of [].concat(b.mock || [])) h.push('mocked ' + m.url);
  for (const p of [].concat(b.patch || [])) h.push('patched ' + p.url);
  if (b.geo) h.push('location ' + (b.geo === 'denied' ? 'refused' : 'granted'));
  return h.join(' · ') || 'by address';
};
const md = ['# Round 3 — the inventory', '', `Built ${new Date().toISOString().slice(0, 16)} UTC by \`tools\\r3-inventory.mjs\` at the head \`${HEAD}\`. The routes come from the route files at that head (\`apps/web/src/pages/site/routes.tsx\`, \`pages/dashboard/routes.tsx\`, \`pages/dashboard/navigation.ts\`, \`pages/site/navigation.ts\`); the states from three read-only surveys of the source and the database copy (\`tools\\survey-site.md\`, \`survey-space.md\`, \`survey-admin.md\`).`, '',
  '**Captured:** every base × 390 / 768 / 1440 × ar / en × light / dark (a state that exists at some widths only, such as a phone menu, at those). 390 and 768 are emulated as touch (coarse pointer); 1440 as a mouse.', '',
  '**How a state is reached:** by address; by steps (clicks, typing, keys, by the catalogue\'s words in each language); a request held (loading); a failure or a 429 answered by the capture tool at the network layer (simulated, the contract\'s envelope, `Retry-After: 60`); a request answered with mocked data (an empty list, a recovery position); a real answer patched (one field set, one item added); the location granted or refused. Nothing a capture does writes to the database: every write a state needs is a **named state** (below), done before the capture.', '',
  '## 1. Routes → screens → parts', '', '| Route | Shell | Screen (foundation §13) | Part | Roles |', '|---|---|---|---|---|',
  ...ROUTES.map((r) => `| ${r.join(' | ')} |`), '',
  'Shared by every part, judged by **SH**: the site header, the phone menu and the footer; the focus shell; the dashboard\'s sidebars, rail, drawer, top bar and account menu; toasts, dialogs and Sheets; loading, empty, failure, offline, 403 and 404 states; the identity across the product.', '',
  '## 2. The base states, by part', ''];
for (const p of PARTS) {
  const list = all.filter((b) => b.part === p);
  md.push(`### ${p} — ${list.length} bases`, '', '| ID | Screen | State | Role | URL | How | Widths |', '|---|---|---|---|---|---|---|');
  for (const b of list) md.push(`| ${b.id} | ${b.screen} | ${b.state} | ${b.role} | \`${typeof b.url === 'string' ? b.url : b.url.ar}\` | ${how(b)} | ${(b.widths || [390, 768, 1440]).join(', ')} |`);
  md.push('');
}
md.push('## 3. Named states written to `masaha_dr_dev`', '',
  '- **NS1** — people present at Pal Hub (space 26): two visits («ريم أبو عمرة», «Omar Saleh») and two subscribers (subscriptions 17 and 31) checked in by reception, through the API.',
  '- **NS2** — payments today: reception 20 ₪ cash on subscription 20; the owner 50 ₪ by transfer on subscription 17, through the API.',
  '- **NS4** — a long Arabic name on unverified space 19 («دار النصيرات للدراسة والعمل المشترك للطلاب والخريجين»), by SQL on `name_ar` only.',
  '- `rate_limits` rows of `masaha_dr_dev` are cleared between capture batches (allowed by the prompt).', '',
  '## 4. States not captured, and why', '',
  '- **The closure extension dialog (O11):** the only closure is already extended; reaching it needs a write or two mocked answers whose shapes the review did not pin. Its text and rules are judged from the source by OW.',
  '- **The price-a-visit dialog:** Pal Hub has no unpriced visit; it needs a write. DK judges it from the source.',
  '- **The one-time password after adding an owner or staff:** needs an account created; the admin\'s users page shows the same dialog through a mocked issue answer (AD-21).',
  '- **A space switcher with two live spaces:** the demo owner has one live space; needs a second link (a write).',
  '- **A space FULL in the lists** (the directory\'s card and pin): a manual override lasts until closing (Friday 20:00 in Gaza); FULL is captured on a space\'s page through a patched answer (PU-14).',
  '- **Hover states and motion:** a still frame cannot show them; SH checks them live and in the source.',
  '- **Google sign-in itself:** not used (the prompt); its button is shown as the page draws it.', '');
writeFileSync(join(ROUND3, 'INVENTORY.md'), md.join('\n'));
console.log(`inventory: ${all.length} bases → tools\\inventory.json and INVENTORY.md`);
