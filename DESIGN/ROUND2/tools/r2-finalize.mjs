// r2-finalize — copies each issue's frame from the evidence pack to the review's shots folder,
// named after the issue, as the report's evidence lines say:
//   - **evidence:** `R2-PU-DF-001.png` (frame B12-390-ar-dark)
// Usage: node r2-finalize.mjs <REVIEW>      (e.g. PU-DF)
// It never overwrites a capture that differs; it reports every line it could not resolve.

import { readFileSync, existsSync, mkdirSync, copyFileSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROUND2 = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const REVIEW = process.argv[2];
if (!REVIEW) { console.error('usage: node r2-finalize.mjs <REVIEW>'); process.exit(2); }

const report = join(ROUND2, 'REPORT', `R2-${REVIEW}_REPORT.md`);
const frames = join(ROUND2, 'packs', REVIEW, 'frames');
const shots = join(ROUND2, 'shots', 'r2-shots', REVIEW);
mkdirSync(shots, { recursive: true });

const text = readFileSync(report, 'utf8');
const re = new RegExp('`(R2-' + REVIEW + '-\\d{3}[a-z]?\\.png)`\\s*\\(frame\\s+(B\\d+-\\d+-(?:ar|en)-(?:light|dark))(\\.full)?\\)', 'g');
let copied = 0; const problems = []; const seen = new Set();
for (const m of text.matchAll(re)) {
  const [, name, frame, full] = m;
  if (seen.has(name)) { problems.push(`${name}: named twice`); continue; }
  seen.add(name);
  const src = join(frames, frame + (full ? '.full' : '') + '.png');
  if (!existsSync(src)) { problems.push(`${name}: frame ${frame} not in the pack`); continue; }
  copyFileSync(src, join(shots, name)); copied++;
}
const ids = new Set([...text.matchAll(new RegExp('^#{2,4}\\s*(R2-' + REVIEW + '-\\d{3})', 'gm'))].map((m) => m[1]));
for (const id of ids) if (![...seen].some((n) => n.startsWith(id))) problems.push(`${id}: no evidence line in the expected form`);
for (const p of problems) console.log('problem: ' + p);
console.log(`${REVIEW}: ${ids.size} issues, ${copied} captures copied to ${shots}${problems.length ? `, ${problems.length} problems` : ''}`);
