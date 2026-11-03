p='heavy.mjs'
s=open(p,encoding='utf8').read()
s=s.replace("""const LAST_API = join(HERE, 'heavy-last-api.txt');""","""const LAST_API = join(HERE, 'heavy-last-api.txt');
// The lead's request waiting: the lanes let it go first (the foundation and the joins are the
// critical path). Stale after 5 minutes, so a lead that died never blocks the lanes.
const LEAD_WAITING = join(HERE, 'heavy-lead-waiting.txt');""")
s=s.replace("""function takeSlot() {""","""function leadWaiting() {
  if (lane === 'lead') return false;
  try {
    return Date.now() - Number.parseInt(readFileSync(LEAD_WAITING, 'utf8'), 10) < 300_000;
  } catch {
    return false;
  }
}

function takeSlot() {
  if (leadWaiting()) return undefined;""")
s=s.replace("""      if (isApi) writeFileSync(LAST_API, String(Date.now()));""","""      if (isApi) writeFileSync(LAST_API, String(Date.now()));
      if (lane === 'lead') rmSync(LEAD_WAITING, { force: true });""")
s=s.replace("""  console.error(`[heavy] waiting 2 minutes (try ${attempt} of ${TRIES})`);
  sleep(apiTooSoon() ? 61_000 : WAIT_MS);""","""  if (lane === 'lead') writeFileSync(LEAD_WAITING, String(Date.now()));
  console.error(`[heavy] waiting (try ${attempt} of ${TRIES})`);
  sleep(apiTooSoon() ? 61_000 : lane === 'lead' ? 30_000 : WAIT_MS);""")
s=s.replace("""    log(`WAIT   both slots taken (try ${attempt})  ${line}`);""","""    log(`WAIT   ${leadWaiting() ? "the lead's request first" : 'both slots taken'} (try ${attempt})  ${line}`);""")
open(p,'w',encoding='utf8',newline='').write(s)
