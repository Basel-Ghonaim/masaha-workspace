// The lead's grant of a heavy run (3_EXEC_PROMPT_LEAD.md §5), adapted from PAYMENTS_STEP10's: at most
// two heavy runs at once on the machine, each only with at least 4 GB free; never two `test:api` runs
// started within the same minute. A run takes one of two slots (a directory made atomically), checks
// the free memory, and waits 2 minutes between tries while either is short (bounded: 60 tries, then it
// exits 75 without running). Every grant, wait and end is logged to heavy-grants.log (UTC), which the
// lead reads.
// Usage (from the worktree's root): node <this file> <lane> <command...>
//   e.g. node C:/dev/masaha/workspace/WORKER_A/FINAL/scripts/heavy.mjs lane-a1 npm run lint
import { execSync, spawnSync } from 'node:child_process';
import { appendFileSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const HERE = import.meta.dirname;
const LOG = join(HERE, 'heavy-grants.log');
const SLOTS = [join(HERE, 'heavy-slot-1'), join(HERE, 'heavy-slot-2')];
const LAST_API = join(HERE, 'heavy-last-api.txt');
// The lead's request waiting: the lanes let it go first (the foundation and the joins are the
// critical path). Stale after 5 minutes, so a lead that died never blocks the lanes.
const LEAD_WAITING = join(HERE, 'heavy-lead-waiting.txt');
const MIN_FREE_KB = 4 * 1024 * 1024;
const WAIT_MS = 120_000;
const TRIES = 60;

const [lane, ...command] = process.argv.slice(2);
if (!lane || command.length === 0) {
  console.error('usage: node heavy.mjs <lane> <command...>');
  process.exit(2);
}
const line = command.join(' ');
const isApi = /test:api/.test(line);
const stamp = () => new Date().toISOString().replace('T', ' ').slice(0, 19);
const log = (text) => appendFileSync(LOG, `${stamp()}  ${lane.padEnd(8)} ${text}\n`);

function freeKb() {
  const out = execSync(
    'powershell -NoProfile -Command "(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory"',
    { encoding: 'utf8' },
  );
  return Number.parseInt(out.trim(), 10);
}

function lastApiStart() {
  try {
    return Number.parseInt(readFileSync(LAST_API, 'utf8'), 10) || 0;
  } catch {
    return 0;
  }
}

function leadWaiting() {
  if (lane === 'lead') return false;
  try {
    return Date.now() - Number.parseInt(readFileSync(LEAD_WAITING, 'utf8'), 10) < 300_000;
  } catch {
    return false;
  }
}

function takeSlot() {
  if (leadWaiting()) return undefined;
  for (const slot of SLOTS) {
    try {
      mkdirSync(slot);
      return slot;
    } catch {
      // taken
    }
  }
  return undefined;
}

const sleep = (ms) => Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);

let slot;
for (let attempt = 1; attempt <= TRIES; attempt += 1) {
  slot = takeSlot();
  if (slot) {
    const free = freeKb();
    const soon = apiTooSoon();
    if (free >= MIN_FREE_KB && !soon) {
      if (isApi) writeFileSync(LAST_API, String(Date.now()));
      if (lane === 'lead') rmSync(LEAD_WAITING, { force: true });
      log(`GRANT  ${slot.slice(-6)} free ${free} KB  ${line}  (cwd ${process.cwd()})`);
      break;
    }
    rmSync(slot, { recursive: true, force: true });
    slot = undefined;
    log(
      soon
        ? `WAIT   another test:api started this minute (try ${attempt})  ${line}`
        : `WAIT   memory ${free} KB < 4 GB (try ${attempt})  ${line}`,
    );
  } else {
    log(`WAIT   ${leadWaiting() ? "the lead's request first" : 'both slots taken'} (try ${attempt})  ${line}`);
  }
  if (lane === 'lead') writeFileSync(LEAD_WAITING, String(Date.now()));
  console.error(`[heavy] waiting (try ${attempt} of ${TRIES})`);
  sleep(apiTooSoon() ? 61_000 : lane === 'lead' ? 30_000 : WAIT_MS);
}
function apiTooSoon() {
  return isApi && Date.now() - lastApiStart() < 60_000;
}
if (!slot) {
  log(`GIVEUP after ${TRIES} tries  ${line}`);
  process.exit(75);
}

let status = 1;
try {
  const started = Date.now();
  const result = spawnSync(line, { shell: true, stdio: 'inherit' });
  status = result.status ?? (result.signal ? 137 : 1);
  log(
    `END    ${slot.slice(-6)} exit ${status}${result.signal ? ` signal ${result.signal}` : ''} after ${Math.round((Date.now() - started) / 1000)} s, free ${freeKb()} KB  ${line}`,
  );
} finally {
  rmSync(slot, { recursive: true, force: true });
}
process.exit(status);
