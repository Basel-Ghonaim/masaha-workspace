// r3-index — checks the round 3 pack against the inventory and writes, per part, the measured leads
// (summary.md: each fact once per base, with the frames it was measured on) and the pack's index
// (..\pack\INDEX.md: every base, its frames and sheets, and the checks: missing or failed frames,
// a wrong language or theme, a PNG of the wrong width or suspiciously small).
// Usage: node r3-index.mjs <inventory.json>

import { readFileSync, readdirSync, existsSync, writeFileSync, statSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROUND3 = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const inventory = JSON.parse(readFileSync(resolve(process.argv[2]), 'utf8'));
const WIDTHS = [390, 768, 1440], LANGS = ['ar', 'en'], THEMES = ['light', 'dark'];
const pngWidth = (f) => readFileSync(f).readUInt32BE(16);
const parts = [...new Set(inventory.map((b) => b.part))];
const index = ['# Round 3 — the evidence pack', '', `Built ${new Date().toISOString().slice(0, 16)} UTC by \`tools\\r3-index.mjs\`. Each frame: \`<ID>-<width>-<lang>-<theme>\` — \`.png\` (first screen), \`.full.png\` (whole page, capped at 9000 px), \`.json\` (measured facts). Sheets: \`<ID>-<width>.png\` (the four first screens) and \`<ID>-<width>-full.png\` (the four whole pages).`, ''];
const totals = { frames: 0, expected: 0, missing: 0, wrong: 0, small: 0, sheets: 0, sheetsExpected: 0 };
const problems = [];
const global = new Map(); // fact (without the frame) → Set of base ids, across parts

for (const part of parts) {
  const dir = join(ROUND3, 'pack', part); const frames = join(dir, 'frames'); const sheets = join(dir, 'sheets');
  const have = existsSync(frames) ? new Set(readdirSync(frames)) : new Set();
  const haveSheets = existsSync(sheets) ? new Set(readdirSync(sheets)) : new Set();
  const lines = [`# Measured leads — ${part}`, '', 'Each fact is listed once per base state, with the frames it was measured on. A lead is not yet an issue: open the frame before writing one. Contrast is measured on every visible text against the colour painted under it (text over a photo or the map is skipped and counted); targets below 40 px (44 px on a coarse pointer, emulated at 390 and 768) exclude links inside running text; "Sea" is any of the old identity\'s 22 ramp values still painted; "spark" is any of the berry ramp\'s values as text, on an action, or as a mark.', ''];
  index.push(`## ${part}`, '', '| ID | screen | state | role | URL | frames | sheets |', '|---|---|---|---|---|---|---|');
  for (const b of inventory.filter((x) => x.part === part)) {
    if (b.skip) { index.push(`| ${b.id} | ${b.screen} | ${b.state} | ${b.role} | \`${typeof b.url === 'string' ? b.url : b.url.ar}\` | not captured: ${b.skip} | |`); continue; }
    const ws = b.widths || WIDTHS, ls = b.langs || LANGS, ts = b.themes || THEMES;
    let got = 0, exp = 0; const facts = new Map();
    const add = (key, frame) => {
      if (!facts.has(key)) facts.set(key, []); facts.get(key).push(frame);
      const g = key.replace(/«[^»]*»/g, '«…»').replace(/\d+×\d+ \(hit \d+x\d+\)/, 'small');
      if (!global.has(g)) global.set(g, new Set()); global.get(g).add(b.id);
    };
    for (const w of ws) for (const l of ls) for (const t of ts) {
      exp++; const id = `${b.id}-${w}-${l}-${t}`; const short = `${w}-${l}-${t}`;
      if (!have.has(id + '.json') || !have.has(id + '.png') || !have.has(id + '.full.png')) { problems.push(`${part} ${id}: missing`); totals.missing++; continue; }
      got++;
      const f = JSON.parse(readFileSync(join(frames, id + '.json'), 'utf8'));
      if (!f.langOk || !f.themeOk) { problems.push(`${part} ${id}: language or theme wrong (lang ${f.firstScreen.htmlLang}/${f.firstScreen.dir}, theme ${f.firstScreen.theme})`); totals.wrong++; }
      for (const s of ['.png', '.full.png']) { const p = join(frames, id + s); if (pngWidth(p) !== w || statSync(p).size < 4000) { problems.push(`${part} ${id}${s}: width ${pngWidth(p)}, ${statSync(p).size} bytes`); totals.small++; } }
      const fs = f.firstScreen, wp = typeof f.wholePage === 'object' ? f.wholePage : fs;
      for (const e of f.consoleErrors) add('console: ' + e.slice(0, 200), short);
      for (const e of f.apiErrors) add('API answered ' + e.replace(/\d{2,}/g, (m) => m), short);
      if (fs.horizontalPageOverflow) add(`page scrolls sideways: scrollWidth ${fs.page.scrollWidth} > ${fs.page.clientWidth}`, short);
      if (fs.textLength < 60) add(`near-blank: ${fs.textLength} characters of text`, short);
      for (const i of wp.brokenImages || []) add('broken image: ' + i, short);
      for (const c of wp.contrast.fails) add(`contrast ${c.ratio}:1 < ${c.need} — «${c.text}» ${c.fg} on ${c.ground} (${c.size}px/${c.weight || ''}) ${c.el}`, short);
      for (const s of wp.targets.small) add(`target ${s.w}×${s.h} (hit ${s.hit}) < ${s.need} — ${s.el}`, short);
      for (const s of wp.seaValues) add(`Sea value ${s.value} (${s.sea}) as ${s.prop} — ${s.el}`, short);
      for (const s of wp.sparkAsText) add(`spark as text: ${s.value} as ${s.prop} — ${s.el}${s.inAction ? ' (inside an action)' : ''}`, short);
      for (const s of wp.sparkOnAction) add(`spark on an action: ${s.value} as ${s.prop} — ${s.el} ${s.state}`, short);
      for (const c of wp.clipped) add(`clipped ${c.axis}: ${c.el} — content ${c.content}px in ${c.box}px${c.ellipsis ? ' (ellipsis)' : ''}`, short);
      for (const o of wp.offscreen) add(`off the screen: ${o.el} — left ${o.left}, right ${o.right}`, short);
      const tab = f.focusAfterTab || [];
      tab.forEach((s, i) => { if (s.el !== '(body)' && (s.outline === 'none' && !s.boxShadow)) add(`Tab ${i + 1}: ${s.el} — no outline or shadow`, short); else if (s.outlineVsGround !== null && s.outlineVsGround < 3) add(`Tab ${i + 1}: ${s.el} — outline ${s.outline} at ${s.outlineVsGround}:1 on ${s.ground}`, short); else if (s.inViewport === false) add(`Tab ${i + 1}: ${s.el} — focused outside the viewport`, short); });
    }
    totals.frames += got; totals.expected += exp;
    const sh = []; for (const w of ws) for (const s of ['', '-full']) { totals.sheetsExpected++; const n = `${b.id}-${w}${s}.png`; if (haveSheets.has(n)) { sh.push(n); totals.sheets++; } else problems.push(`${part} sheet ${n}: missing`); }
    index.push(`| ${b.id} | ${b.screen} | ${b.state} | ${b.role} | \`${typeof b.url === 'string' ? b.url : b.url.ar}\`${b.hold ? ' (held ' + b.hold.url + ')' : ''}${[].concat(b.fail || []).map((f) => ' (' + (f.status || 500) + ' on ' + f.url + ')').join('')}${[].concat(b.mock || []).map((m) => ' (mocked ' + m.url + ')').join('')} | ${got}/${exp} | ${sh.length}/${ws.length * 2} |`);
    const n = ws.length * ls.length * ts.length;
    lines.push(`## ${b.id} — ${b.screen} · ${b.state} (${b.role})`, '', '`' + (typeof b.url === 'string' ? b.url : JSON.stringify(b.url)) + '`' + (b.steps ? ` · ${b.steps.length} steps` : ''), '');
    if (!facts.size) lines.push('- nothing measured', '');
    else { for (const [k, fr] of [...facts].sort((a, c) => c[1].length - a[1].length)) lines.push(`- ${k} — ${fr.length === n ? 'all frames' : fr.join(', ')}`); lines.push(''); }
  }
  writeFileSync(join(dir, 'summary.md'), lines.join('\n') + '\n');
  index.push('');
}
index.push('## Checks', '', `- frames: ${totals.frames} of ${totals.expected} (${totals.missing} missing)`, `- a wrong language or theme: ${totals.wrong}`, `- PNGs of the wrong width or under 4 KB: ${totals.small}`, `- sheets: ${totals.sheets} of ${totals.sheetsExpected}`, '', ...(problems.length ? ['### Problems', '', ...problems.slice(0, 300).map((p) => '- ' + p)] : ['No problems.']));
writeFileSync(join(ROUND3, 'pack', 'INDEX.md'), index.join('\n') + '\n');
const KINDS = [['console', 'Console errors'], ['API answered', 'API errors (real answers)'], ['page scrolls', 'Page overflow'], ['contrast', 'Contrast below AA'], ['target', 'Targets below 40 / 44 px'], ['Sea value', 'Sea values still painted'], ['spark as text', 'The spark as text'], ['spark on an action', 'The spark on an action'], ['Tab', 'Focus after Tab'], ['clipped', 'Clipped text'], ['off the screen', 'Text off the screen'], ['near-blank', 'Near-blank frames'], ['broken image', 'Broken images']];
const leads = ['# Measured leads across every part', '', 'Each fact once, with every base it was measured on (names inside «» folded to «…», a target\'s size folded to "small"). Built from the frames\' JSON by `tools\\r3-index.mjs`; a lead is not an issue until a frame is looked at.', ''];
for (const [prefix, title] of KINDS) {
  const rows = [...global].filter(([k]) => k.startsWith(prefix)).sort((a, c) => c[1].size - a[1].size);
  leads.push(`## ${title} (${rows.length})`, '');
  for (const [k, set] of rows.slice(0, 120)) leads.push(`- ${k} — ${set.size} base${set.size > 1 ? 's' : ''}: ${[...set].join(', ')}`);
  if (rows.length > 120) leads.push(`- … ${rows.length - 120} more in the parts' summary.md`);
  leads.push('');
}
writeFileSync(join(ROUND3, 'pack', 'LEADS-ALL.md'), leads.join('\n'));
console.log(`index: ${totals.frames}/${totals.expected} frames, ${totals.missing} missing, ${totals.wrong} wrong lang/theme, ${totals.small} bad PNGs, ${totals.sheets}/${totals.sheetsExpected} sheets`);
