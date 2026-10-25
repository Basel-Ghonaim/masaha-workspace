// The real run of ANNOUNCEMENTS PR 1 (plan §12.6, PR 1) against the API on 3321 and masaha_b_dev, on the demo
// space. Self-judging: one line per case, `PASS|FAIL <case> <status> <code>`, then the audit log's last ten
// actions; the exit code is 1 when any case fails. It never prints a secret or a phone number.
//
// Run with the API up on 3321 (npm run dev -w @masaha/api) and the demo data seeded:
//   node C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\scripts\realrun1.mjs
// It writes: two announcements on the demo space (a closure, ended; a general one, deleted), one visit,
// checked in and out, and its payment when it has a charge. Run it once.
import { execFileSync } from 'node:child_process';
import { randomUUID } from 'node:crypto';
import { readFileSync } from 'node:fs';

const ENV = 'C:\\dev\\masaha\\app-b\\apps\\api\\.env';
const BASE = 'http://localhost:3321/api/v1';

/** A variable of apps/api/.env, never printed. */
function envOf(name) {
  const line = readFileSync(ENV, 'utf8')
    .split(/\r?\n/)
    .find((row) => row.startsWith(`${name}=`));
  if (!line) throw new Error(`${name} is not set in apps/api/.env`);
  return line.slice(name.length + 1).trim().replace(/^"(.*)"$/, '$1');
}

const password = envOf('SEED_DEMO_PASSWORD');

async function call(method, path, { token, body, key } = {}) {
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers.Authorization = `Bearer ${token}`;
  if (key) headers['Idempotency-Key'] = key;
  const response = await fetch(`${BASE}${path}`, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const json = await response.json().catch(() => null);
  return {
    status: response.status,
    json,
    data: json?.data,
    meta: json?.meta,
    code: json?.error?.code ?? '-',
  };
}

let failures = 0;
/** One case: PASS when the status and the code are the expected ones and `check` holds. */
function report(name, answer, expected, check = () => true) {
  let held = false;
  try {
    held = check();
  } catch {
    held = false;
  }
  const ok = answer.status === expected.status && (expected.code ?? '-') === answer.code && held;
  if (!ok) failures += 1;
  console.log(`${ok ? 'PASS' : 'FAIL'} ${name} ${answer.status} ${answer.code}`);
  return ok;
}

const signIn = async (email) =>
  (await call('POST', '/auth/login', { body: { email, password } })).data?.accessToken;
const owner = await signIn('demo-owner@example.com');
const reception = await signIn('demo-reception@example.com');
const directoryOwner = await signIn('demo-directory-owner@example.com');
if (!owner || !reception || !directoryOwner) {
  console.log('FAIL sign-in - -');
  process.exit(1);
}
const mine = (await call('GET', '/manage/spaces', { token: reception })).data?.[0];
const spaceId = mine?.spaceId;
const slug = mine?.slug;
const base = `/manage/spaces/${spaceId}`;
const path = `${base}/announcements`;

// Preconditions: the demo space is publicly listed, verified, and under no running closure.
const before = await call('GET', `/spaces/${slug}/occupancy`);
const runningBefore = await call('GET', `${path}?state=RUNNING`, { token: reception });
report(
  `precondition: the demo space (${slug}) listed, its live status not CLOSED, no running closure`,
  before,
  { status: 200 },
  () =>
    before.data.status !== 'CLOSED' &&
    !runningBefore.data.some((announcement) => announcement.type === 'CLOSURE'),
);
console.log(`     live status before: ${before.data?.status}`);

// 1–2. Reception posts a closure starting now, with key K; K again answers the same.
const K = randomUUID();
const closureBody = { type: 'CLOSURE', textAr: 'مغلق اليوم للصيانة.', startsAt: new Date().toISOString() };
const posted = await call('POST', path, { token: reception, body: closureBody, key: K });
report('reception posts a CLOSURE starting now → 201 RUNNING', posted, { status: 201 }, () =>
  posted.data.state === 'RUNNING' && posted.data.type === 'CLOSURE',
);
const closureId = posted.data?.id;
const retried = await call('POST', path, { token: reception, body: closureBody, key: K });
report('the same key again → 201, the same id', retried, { status: 201 }, () =>
  retried.data.id === closureId,
);

// 3. The managed list: it, with extension null.
const running = await call('GET', `${path}?state=RUNNING`, { token: reception });
report('GET ?state=RUNNING → it, extension: null', running, { status: 200 }, () =>
  running.data.some((row) => row.id === closureId && row.extension === null),
);

// 4–5. The public page carries it; the live status is CLOSED.
const pageOpen = await call('GET', `/spaces/${slug}`);
report('anonymous GET /spaces/<slug> → it in announcements', pageOpen, { status: 200 }, () =>
  pageOpen.data.announcements.some((row) => row.id === closureId && !('state' in row)),
);
const closedNow = await call('GET', `/spaces/${slug}/occupancy`);
report('GET /spaces/<slug>/occupancy → CLOSED', closedNow, { status: 200 }, () =>
  closedNow.data.status === 'CLOSED',
);

// 6. A visit's check-in during the closure: 201 with CLOSURE_IN_FORCE.
const visitIn = await call('POST', `${base}/visits`, {
  token: reception,
  body: { visitorName: 'زائر الإعلانات' },
  key: randomUUID(),
});
report('reception checks a visitor in → 201 with CLOSURE_IN_FORCE', visitIn, { status: 201 }, () =>
  visitIn.meta.warnings.includes('CLOSURE_IN_FORCE'),
);
console.log(`     warnings: ${JSON.stringify(visitIn.meta?.warnings)}`);

// 7. Its check-out, so no stay is left open: paid its quote's charge; with no rate, the owner types one.
const visitId = visitIn.data?.id;
const quoted = await call('GET', `${base}/visits/${visitId}`, { token: reception });
const quote = quoted.data?.quote;
let checkOut;
let how;
if (quote?.chargeAgorot === null) {
  how = 'no rate: the owner typed a charge of 1000 with a reason, paid in cash';
  checkOut = await call('POST', `${base}/visits/${visitId}/check-out`, {
    token: owner,
    key: randomUUID(),
    body: {
      checkedOutAt: quote.at,
      charge: { amountAgorot: 1_000, reason: 'تشغيل تجريبي للإعلانات' },
      payment: { amountAgorot: 1_000, method: 'CASH' },
    },
  });
} else if (quote?.chargeAgorot === 0) {
  how = 'a charge of 0: closed with no payment';
  checkOut = await call('POST', `${base}/visits/${visitId}/check-out`, {
    token: reception,
    key: randomUUID(),
    body: { checkedOutAt: quote.at },
  });
} else {
  how = `reception paid its quote's charge, ${quote?.chargeAgorot} agorot, in cash`;
  checkOut = await call('POST', `${base}/visits/${visitId}/check-out`, {
    token: reception,
    key: randomUUID(),
    body: { checkedOutAt: quote?.at, payment: { amountAgorot: quote?.chargeAgorot, method: 'CASH' } },
  });
}
report('its check-out → 200, closed', checkOut, { status: 200 }, () =>
  checkOut.data.visit.checkedOutAt !== null,
);
console.log(`     check-out: ${how}`);

// 8–10. Edit the text; end it now; the page shows it no more.
const edited = await call('PATCH', `${path}/${closureId}`, {
  token: reception,
  body: { textAr: 'مغلق اليوم للصيانة، ونعود غدًا.' },
});
report('PATCH the text → 200', edited, { status: 200 }, () =>
  edited.data.textAr === 'مغلق اليوم للصيانة، ونعود غدًا.' && edited.data.state === 'RUNNING',
);
const ended = await call('POST', `${path}/${closureId}/end`, { token: reception });
report('POST …/end → 200 ENDED', ended, { status: 200 }, () => ended.data.state === 'ENDED');
const pageEnded = await call('GET', `/spaces/${slug}`);
report('the page no longer shows it', pageEnded, { status: 200 }, () =>
  !pageEnded.data.announcements.some((row) => row.id === closureId),
);
const reopened = await call('GET', `/spaces/${slug}/occupancy`);
report('the live status is no longer CLOSED by it', reopened, { status: 200 }, () =>
  reopened.data.status !== 'CLOSED',
);

// 11–13. An upcoming GENERAL tomorrow; start it now; delete it, twice.
const tomorrow = new Date(Date.now() + 86_400_000).toISOString();
const upcoming = await call('POST', path, {
  token: owner,
  key: randomUUID(),
  body: { type: 'GENERAL', textAr: 'ورشة عمل غدًا.', textEn: 'A workshop tomorrow.', startsAt: tomorrow },
});
report('an upcoming GENERAL tomorrow → 201 UPCOMING', upcoming, { status: 201 }, () =>
  upcoming.data.state === 'UPCOMING',
);
const generalId = upcoming.data?.id;
const started = await call('POST', `${path}/${generalId}/start`, { token: owner });
report('POST …/start → 200 RUNNING', started, { status: 200 }, () => started.data.state === 'RUNNING');
const deleted = await call('DELETE', `${path}/${generalId}`, { token: reception });
report('DELETE → 204', deleted, { status: 204 });
const deletedAgain = await call('DELETE', `${path}/${generalId}`, { token: reception });
report('DELETE again → 204', deletedAgain, { status: 204 });

// 14. The summary.
const summary = await call('GET', `${path}/summary`, { token: owner });
report('GET …/summary → 200', summary, { status: 200 }, () =>
  ['running', 'upcoming', 'ended', 'closuresAwaitingExtension'].every(
    (key) => typeof summary.data[key] === 'number',
  ),
);
console.log(`     summary: ${JSON.stringify(summary.data)}`);

// 15. The directory owner, who has no link at the demo space: not_found.
const strangerList = await call('GET', path, { token: directoryOwner });
report('the directory owner lists the demo space\'s announcements → 404', strangerList, {
  status: 404,
});
const strangerPost = await call('POST', path, {
  token: directoryOwner,
  key: randomUUID(),
  body: { type: 'GENERAL', textAr: 'لا' },
});
report('the directory owner posts on the demo space → 404', strangerPost, { status: 404 });

// The audit log's last ten actions, from masaha_b_dev (the database's user from DATABASE_URL, not printed).
const url = new URL(envOf('DATABASE_URL'));
const actions = execFileSync(
  'docker',
  [
    'exec',
    'masaha-postgres-1',
    'psql',
    '-U',
    decodeURIComponent(url.username),
    '-d',
    url.pathname.slice(1),
    '-tA',
    '-c',
    'SELECT action FROM audit_logs ORDER BY id DESC LIMIT 10',
  ],
  { encoding: 'utf8' },
);
console.log('audit (latest first):', actions.trim().split(/\r?\n/).join(', '));

console.log(failures === 0 ? 'ALL PASS' : `${failures} FAIL`);
process.exit(failures === 0 ? 0 : 1);
