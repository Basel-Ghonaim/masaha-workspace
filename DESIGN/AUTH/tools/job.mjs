// job — writes a shoot.mjs job: node job.mjs <out.json> <outDir> <pages> <designs> <widths> <themes> <langs> [states] [--full] [--scale 2]
// pages: signin,register,forgot,reset,change ; designs: orig,slate,coast,dots ; states: default or names
import { writeFileSync } from 'node:fs';
const a = process.argv.slice(2);
const [file, out, pages, designs, widths, themes, langs, states = 'default'] = a;
const PAGE = { signin: ['Sign in', 1, 'sign-in'], register: ['Register', 2, 'register'], forgot: ['Forgot password', 3, 'forgot-password'], reset: ['Reset password', 4, 'reset-password'], change: ['Change password', 5, 'change-password'] };
const shots = [];
for (const p of pages.split(',')) for (const d of designs.split(',')) for (const st of states.split(',')) for (const w of widths.split(',')) for (const t of themes.split(',')) for (const l of langs.split(',')) {
  const [file, n, slug] = PAGE[p];
  const q = ['switcher=0', d !== 'orig' ? 'v=' + d : '', st !== 'default' ? 'state=' + st : ''].filter(Boolean).join('&');
  shots.push({ name: `${n}-${slug}-${d === 'orig' ? 'original' : d}${st !== 'default' ? '-' + st : ''}-${w}-${t}${l === 'en' ? '-en' : ''}`, path: `${file}.html?${q}`, width: +w, theme: t, lang: l });
}
writeFileSync(file, JSON.stringify({ base: 'http://localhost:5410/', out, scale: a.includes('--scale') ? +a[a.indexOf('--scale') + 1] : 1, full: a.includes('--full'), probe: true, shots }, null, 1));
console.log(shots.length + ' shots');
