// Compares the Chrome pass's before and after: every control whose painted colours changed, each run's
// main actions with their colours, hover and focus ring, axe, and the page's sideways overflow.
import { readFileSync, writeFileSync } from 'node:fs';

const HERE = 'C:/dev/masaha/workspace/TASKS/BERRY_PRIMARY/scripts';
const before = JSON.parse(readFileSync(`${HERE}/out-before.json`, 'utf8'));
const after = JSON.parse(readFileSync(`${HERE}/out-after.json`, 'utf8'));
const key = (c) => `${c.tag}|${c.slot}|${c.name}`;
const lines = [];
for (const base of Object.keys(after).filter((k) => k !== 'errors')) {
  const a = after[base];
  const b = before[base];
  if (a.error || b?.error) {
    lines.push(`${base}: ERROR ${a.error ?? b.error}`);
    continue;
  }
  const out = [`${base}: mains ${a.mains.length} ${a.mains.map((m) => `«${m.name}» ${m.bg} / ${m.color}`).join('; ')}`];
  if (a.interact?.hover) out.push(`  hover ${a.interact.hover.hovered} ${a.interact.hover.bg}`);
  if (a.interact?.focus) out.push(`  focus ${a.interact.focus.focusVisible} ${a.interact.focus.outline} offset ${a.interact.focus.offset}`);
  out.push(`  axe ${a.axe?.length ?? '-'} (before ${b?.axe?.length ?? '-'}) overflow ${a.state?.overflow ?? '-'}`);
  if (a.controls && b?.controls) {
    const pool = new Map();
    for (const c of b.controls) pool.set(key(c), [...(pool.get(key(c)) ?? []), c]);
    const changed = [];
    const added = [];
    for (const c of a.controls) {
      const list = pool.get(key(c));
      const was = list?.shift();
      if (!was) added.push(`${c.name} (${c.main ? 'main' : c.bg})`);
      else if (was.bg !== c.bg || was.color !== c.color || was.border !== c.border)
        changed.push(`«${c.name}»${c.main ? ' [main]' : ''} ${was.bg}→${c.bg} ${was.color}→${c.color}`);
    }
    const removed = [...pool.values()].flat().map((c) => c.name);
    out.push(`  changed ${changed.length}: ${changed.join(' | ')}`);
    if (added.length) out.push(`  added: ${added.join(' | ')}`);
    if (removed.length) out.push(`  removed: ${removed.join(' | ')}`);
  }
  lines.push(out.join('\n'));
}
lines.push(`page errors: before ${before.errors?.length}, after ${after.errors?.length}`);
writeFileSync(`${HERE}/compare.txt`, lines.join('\n'));
console.log(lines.join('\n'));
