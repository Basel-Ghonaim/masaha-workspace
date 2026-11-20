// The lead's grant of a heavy run (3_EXEC_PROMPT_PROD.md §2), adapted from
// WORKER_B\_DONE\BACKEND_FINAL\scripts\heavy.mjs: at most two heavy runs at once on the machine,
// each only with at least 4 GB free, the lead first. A run takes one of two slots (a directory made
// atomically), checks the free memory, and waits between tries while either is short (bounded: 45
// tries, then it exits 75 without running). While the lead waits it leaves a marker
// (heavy-lead-waiting) and no lane takes a slot, so the lead's run is granted first. Every grant,
// wait and end is logged to heavy-grants.log (UTC), which the lead reads.
// Since 2026-11-12 (after a run stopped for low memory, the supervisor's word): while less than
// 8 GB is free, one heavy run at a time on the whole machine — a run then takes only slot 1, and
// only while slot 2 is free; a second slot is granted only with 8 GB or more free.
// Heavy = lint, typecheck, any test lane or test file run, a build, npm ci, a Chrome batch.
// Usage (from the worktree's root): node <this file> <lane> <command...>
//   e.g. node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs lane-a npm run typecheck
import { execSync, spawnSync } from 'node:child_process';
import { appendFileSync, existsSync, mkdirSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const HERE = import.meta.dirname;
const LOG = join(HERE, 'heavy-grants.log');
const SLOTS = [join(HERE, 'heavy-slot-1'), join(HERE, 'heavy-slot-2')];
const LEAD_WAITING = join(HERE, 'heavy-lead-waiting');
const MIN_FREE_KB = 4 * 1024 * 1024;
const SINGLE_BELOW_KB = 8 * 1024 * 1024;
const TRIES = 45;
const STALE_MARKER_MS = 2 * 60 * 60 * 1000;

const [lane, ...command] = process.argv.slice(2);
if (!lane || command.length === 0) {
  console.error('usage: node heavy.mjs <lane> <command...>');
  process.exit(2);
}
const isLead = lane === 'lead';
const WAIT_MS = isLead ? 60_000 : 120_000;
const line = command.join(' ');
const stamp = () => new Date().toISOString().replace('T', ' ').slice(0, 19);
const log = (text) => appendFileSync(LOG, `${stamp()}  ${lane.padEnd(7)} ${text}\n`);

// A reading that fails (PowerShell itself can fail to start when memory is short) counts as no
// memory, so the run waits instead of crashing with a slot taken (seen 2026-11-12).
function freeKb() {
  try {
    const out = execSync(
      'powershell -NoProfile -Command "(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory"',
      { encoding: 'utf8' },
    );
    const kb = Number.parseInt(out.trim(), 10);
    return Number.isFinite(kb) ? kb : 0;
  } catch {
    return 0;
  }
}

function leadIsWaiting() {
  try {
    return Date.now() - statSync(LEAD_WAITING).mtimeMs < STALE_MARKER_MS;
  } catch {
    return false;
  }
}

function takeSlot(slots) {
  for (const slot of slots) {
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
const clearLeadMarker = () => {
  if (isLead) rmSync(LEAD_WAITING, { force: true });
};

let slot;
for (let attempt = 1; attempt <= TRIES; attempt += 1) {
  if (!isLead && leadIsWaiting()) {
    log(`WAIT   the lead is waiting (try ${attempt})  ${line}`);
  } else {
    const before = freeKb();
    const single = before < SINGLE_BELOW_KB;
    slot = takeSlot(single ? SLOTS.slice(0, 1) : SLOTS);
    if (slot) {
      const free = freeKb();
      const alone = !single || !existsSync(SLOTS[1]);
      if (free >= MIN_FREE_KB && alone) {
        log(`GRANT  ${slot.slice(-6)} free ${free} KB${single ? ' (single)' : ''}  ${line}  (cwd ${process.cwd()})`);
        break;
      }
      rmSync(slot, { recursive: true, force: true });
      slot = undefined;
      log(
        free < MIN_FREE_KB
          ? `WAIT   memory ${free} KB < 4 GB (try ${attempt})  ${line}`
          : `WAIT   under 8 GB free, another run holds slot 2 (try ${attempt})  ${line}`,
      );
    } else {
      log(`WAIT   ${single ? 'under 8 GB free, one run at a time, slot 1 taken' : 'both slots taken'} (try ${attempt})  ${line}`);
    }
  }
  if (isLead) writeFileSync(LEAD_WAITING, `${stamp()} ${line}\n`);
  console.error(`[heavy] waiting ${WAIT_MS / 1000} s (try ${attempt} of ${TRIES})`);
  sleep(WAIT_MS);
}
clearLeadMarker();
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
