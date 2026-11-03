// The lead's grant of a heavy run (3_EXEC_PROMPT_LEAD.md §5): at most two heavy runs at once on the
// machine, each only with at least 4 GB free. A run takes one of two slots (a directory made
// atomically), checks the free memory, and waits 2 minutes between tries while either is short
// (bounded: 45 tries, then it exits 75 without running). Every grant, wait and end is logged to
// heavy-grants.log, which the lead reads.
// Usage (from the worktree's root): node <this file> <lane> <command...>
//   e.g. node C:/dev/masaha/workspace/WORKER_B/BACKEND_FINAL/scripts/heavy.mjs lane-l npm run lint
import { execSync, spawnSync } from 'node:child_process';
import { appendFileSync, mkdirSync, rmSync } from 'node:fs';
import { join } from 'node:path';

const HERE = import.meta.dirname;
const LOG = join(HERE, 'heavy-grants.log');
const SLOTS = [join(HERE, 'heavy-slot-1'), join(HERE, 'heavy-slot-2')];
const MIN_FREE_KB = 4 * 1024 * 1024;
const WAIT_MS = 120_000;
const TRIES = 45;

const [lane, ...command] = process.argv.slice(2);
if (!lane || command.length === 0) {
  console.error('usage: node heavy.mjs <lane> <command...>');
  process.exit(2);
}
const line = command.join(' ');
const stamp = () => new Date().toISOString().replace('T', ' ').slice(0, 19);
const log = (text) => appendFileSync(LOG, `${stamp()}  ${lane.padEnd(7)} ${text}\n`);

function freeKb() {
  const out = execSync(
    'powershell -NoProfile -Command "(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory"',
    { encoding: 'utf8' },
  );
  return Number.parseInt(out.trim(), 10);
}

function takeSlot() {
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
    if (free >= MIN_FREE_KB) {
      log(`GRANT  ${slot.slice(-6)} free ${free} KB  ${line}  (cwd ${process.cwd()})`);
      break;
    }
    rmSync(slot, { recursive: true, force: true });
    slot = undefined;
    log(`WAIT   memory ${free} KB < 4 GB (try ${attempt})  ${line}`);
  } else {
    log(`WAIT   both slots taken (try ${attempt})  ${line}`);
  }
  console.error(`[heavy] waiting 2 minutes (try ${attempt} of ${TRIES})`);
  sleep(WAIT_MS);
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
