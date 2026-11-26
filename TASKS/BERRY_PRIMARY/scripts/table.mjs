import { readFileSync } from 'node:fs';
const full = JSON.parse(readFileSync('out-audit-full.json', 'utf8'));
const re = JSON.parse(readFileSync('out-audit-recheck.json', 'utf8'));
Object.assign(full.routes, re.routes); Object.assign(full.overlays, re.overlays); Object.assign(full.dark, re.dark);
const E = (p) => {
  const s = p.replace('/dashboard/spaces/26', 'S').replace('/dashboard/admin', 'A');
  const m = {
    '/': '1 «بحث»', '/spaces': 'none (directory)', '/spaces/pal-hub': '1 WhatsApp', '/about': '1 «تصفّح المساحات»', '/privacy': 'none (not named)',
    '/login': '1 submit', '/register': '1 submit', '/forgot-password': '1 submit', '/reset-password': '1 (the state\'s link)', '/no-such-page': 'none (state)',
    'S': 'none (not named)', 'S/desk': '1 top bar / action bar; rows ink', 'S/customers': '1 toolbar', 'S/payments': 'none (not named)', 'S/finance': 'none (not named)',
    'S/packages': '1 header', 'S/profile': 'none (editor page)', 'S/announcements': '1 header', 'S/reports': 'none (not named)', 'S/staff': '1 toolbar', 'S/audit': 'none (not named)',
    'S/settings': 'none (cards)', 'S/customers/17': '1 first state action', 'A': 'none (not named)', 'A/spaces': '1 «إضافة مساحة»', 'A/spaces/new': '1 submit',
    'A/owners': '1 AddOwner', 'A/reports': 'none (not named)', 'A/users': 'none (not named)', 'A/lookups': 'none (cards)', 'A/audit': 'none (not named)', 'A/settings': 'none (cards)',
    'A/spaces/34': 'none (editor page)', '/me/favorites': 'none (state/list)', '/me/reports': 'none (list)', '/me/settings': 'none (cards)',
  };
  return m[s] ?? '?';
};
const rows = [];
for (const [k, v] of Object.entries(full.routes)) {
  if (!v.mains) { rows.push(`| ${k} | — | — | — | error | ${v.error} |`); continue; }
  const [role, width] = k.split('-');
  const page = v.mains.filter((m) => m.where === 'page');
  const exp = E(v.path); const want = exp.startsWith('1') ? 1 : 0;
  const found = page.length ? page.map((m) => m.name + (m.inView ? '' : ' (below the fold)')).join(', ') : '0';
  rows.push(`| ${v.path} | ${role} | ${width} | ${exp} | ${found} | ${page.length === want ? 'ok' : 'CHECK'} |`);
}
console.log('| Screen | Role | Width | Expected | Found (painted `main`) | Verdict |\n|---|---|---|---|---|---|\n' + rows.join('\n'));
const orow = [];
for (const [k, v] of Object.entries(full.overlays)) {
  const [role, width, ...rest] = k.split('-');
  if (!v.mains) { orow.push(`| ${rest.join('-')} | ${role} | ${width} | 1 confirm | not opened (trigger «${v.missing}» not matched) | by code |`); continue; }
  const o = v.mains.filter((m) => m.where === 'overlay');
  const p = v.mains.filter((m) => m.where === 'page');
  const exp = rest.join('-') === 'site-menu' ? 'none (navigation)' : /subscription/.test(k) ? 'none (destructive: «End subscription» opened)' : '1 confirm';
  const want = exp.startsWith('1') ? 1 : 0;
  orow.push(`| ${rest.join('-')} (${v.overlay.join(' / ') || '—'}) | ${role} | ${width} | ${exp} | ${o.map((m) => m.name).join(', ') || '0'}${p.length ? ` · behind the scrim: ${p.map((m) => m.name).join(', ')}` : ''} | ${o.length === want ? 'ok' : 'CHECK'} |`);
}
console.log('\n| Overlay | Role | Width | Expected | Found | Verdict |\n|---|---|---|---|---|---|\n' + orow.join('\n'));
const d = Object.entries(full.dark).map(([k, v]) => `| ${v.path} | ${k.split('-')[1]} | ${k.split('-')[2]} | no berry | berry ${v.berry.length}, main-slot ${v.mains.length} (${v.mains.map((m) => m.bg).join(', ')}) | ${v.berry.length === 0 ? 'ok' : 'CHECK'} |`);
console.log('\n| Dark screen | Role | Width | Expected | Found | Verdict |\n|---|---|---|---|---|---|\n' + d.join('\n'));
