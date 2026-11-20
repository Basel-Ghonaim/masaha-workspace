// watch-pr — waits for the identity PR (head branch feat/ink-berry-identity) to be open with CI green.
// Polls every 5 minutes, at most 8 hours. Logs each poll to watch-pr.log beside this file.
// Exits 0 when open and green (printing "READY <number> <head sha>"), 3 when merged (printing "MERGED <number> <sha>"),
// 4 on timeout.
// Usage: node watch-pr.mjs
import { execSync } from 'node:child_process';
import { appendFileSync } from 'node:fs';
import { join } from 'node:path';

const LOG = join(import.meta.dirname, 'watch-pr.log');
const REPO_DIR = 'C:\\dev\\masaha\\app';
const BRANCH = 'feat/ink-berry-identity';
const EVERY_MS = 5 * 60 * 1000;
const MAX_MS = 8 * 60 * 60 * 1000;
const stamp = () => new Date().toISOString().replace('T', ' ').slice(0, 19);
const log = (t) => appendFileSync(LOG, `${stamp()}  ${t}\n`);
const sh = (c) => execSync(c, { cwd: REPO_DIR, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const t0 = Date.now();
while (Date.now() - t0 < MAX_MS) {
  try {
    const prs = JSON.parse(sh(`gh pr list --head ${BRANCH} --state all --json number,state,headRefOid`));
    const open = prs.find((p) => p.state === 'OPEN');
    const merged = prs.find((p) => p.state === 'MERGED');
    if (open) {
      const view = JSON.parse(sh(`gh pr view ${open.number} --json headRefOid,statusCheckRollup,mergeStateStatus`));
      const checks = view.statusCheckRollup || [];
      const states = checks.map((c) => (c.conclusion || c.state || c.status || '').toUpperCase());
      const pending = checks.filter((c) => (c.status && c.status !== 'COMPLETED') || (!c.conclusion && c.state === 'PENDING')).length;
      const failed = states.filter((s) => ['FAILURE', 'CANCELLED', 'TIMED_OUT', 'ACTION_REQUIRED', 'ERROR'].includes(s)).length;
      const green = checks.length > 0 && pending === 0 && failed === 0;
      log(`PR #${open.number} open, head ${view.headRefOid.slice(0, 8)}, checks ${checks.length}, pending ${pending}, failed ${failed}, merge ${view.mergeStateStatus}`);
      if (green) {
        console.log(`READY ${open.number} ${view.headRefOid}`);
        log(`READY ${open.number} ${view.headRefOid}`);
        process.exit(0);
      }
    } else if (merged) {
      log(`PR #${merged.number} merged, head ${merged.headRefOid}`);
      console.log(`MERGED ${merged.number} ${merged.headRefOid}`);
      process.exit(3);
    } else {
      log('no PR yet');
    }
  } catch (e) {
    log('poll error: ' + String(e.message || e).split('\n')[0]);
  }
  await sleep(EVERY_MS);
}
log('TIMEOUT after 8 hours');
console.log('TIMEOUT');
process.exit(4);
