// The real run of ANNOUNCEMENTS PR 2 (plan §12.6, PR 2) against the API on 3321 and masaha_b_dev, on the demo
// set. Self-judging: one line per case, `PASS|FAIL <case> <status> <code>`, then `ALL PASS` and exit 0, or exit
// 1 when any case fails. It never prints a secret, a token or a phone number.
//
// Run with the API up on 3321 (npm run dev -w @masaha/api) and the demo data seeded:
//   node C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\scripts\realrun2.mjs
// It writes (demo-reception's, every request counted by the report limit, so the cases run in this order):
// a PRICES report on a verified set space, resolved by its owner; an HOURS report on an unverified set space,
// dismissed by the admin; a CONTACT report on the verified space, left open; the limit's counter rows.
// Run it once: a second run within the hour meets the limit early.
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

async function call(method, path, { token, body } = {}) {
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers.Authorization = `Bearer ${token}`;
  const response = await fetch(`${BASE}${path}`, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const text = await response.text();
  let json = null;
  try {
    json = JSON.parse(text);
  } catch {
    json = null;
  }
  return {
    status: response.status,
    text,
    json,
    data: json?.data,
    meta: json?.meta,
    code: json?.error?.code ?? '-',
    retryAfter: response.headers.get('retry-after'),
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

async function signIn(email, password) {
  const answer = await call('POST', '/auth/login', { body: { email, password } });
  return answer.data ? { token: answer.data.accessToken, user: answer.data.user } : null;
}
const demoPassword = envOf('SEED_DEMO_PASSWORD');
const reporter = await signIn('demo-reception@example.com', demoPassword);
const directoryOwner = await signIn('demo-directory-owner@example.com', demoPassword);
const admin = await signIn(envOf('SEED_ADMIN_EMAIL'), envOf('SEED_ADMIN_PASSWORD'));
if (!reporter || !directoryOwner || !admin) {
  console.log('FAIL sign-in - -');
  process.exit(1);
}
console.log(`     reporter: user ${reporter.user.id}, role ${reporter.user.role}`);

// The set: a verified space the directory owner owns, and an unverified one, both listed.
const listed = (await call('GET', '/spaces?limit=50')).data ?? [];
const owned = (await call('GET', '/manage/spaces', { token: directoryOwner.token })).data ?? [];
const ownedIds = new Set(owned.filter((link) => link.role === 'OWNER').map((link) => link.spaceId));
const verified = listed.find((space) => space.isVerified && ownedIds.has(space.id));
const unverified = listed.find((space) => !space.isVerified);
if (!verified || !unverified) {
  console.log('FAIL precondition: a listed verified space of the directory owner and a listed unverified one - -');
  process.exit(1);
}
console.log(`     verified: ${verified.slug} (${verified.id}); unverified: ${unverified.slug} (${unverified.id})`);

let counted = 0;
const post = (slug, body) => {
  counted += 1;
  return call('POST', `/spaces/${slug}/reports`, { token: reporter.token, body });
};

// 1–2. A report on the verified space, then the same again: the open one, nothing new.
const first = await post(verified.slug, { field: 'PRICES' });
report('reporter POST verified { PRICES } → 201 OPEN', first, { status: 201 }, () =>
  first.data.status === 'OPEN' && first.data.space.listed === true,
);
const again = await post(verified.slug, { field: 'PRICES' });
report('the same again → 200, the same id', again, { status: 200 }, () => again.data.id === first.data.id);

// 3–4. On the unverified space; «أخرى» without a message.
const hours = await post(unverified.slug, { field: 'HOURS' });
report('reporter POST unverified { HOURS } → 201', hours, { status: 201 });
const other = await post(unverified.slug, { field: 'OTHER' });
report('{ OTHER } without a message → 422 required', other, { status: 422 }, () =>
  other.json.error.errors.message.includes('required'),
);

// 5. The reporter's own: both open.
const mineOpen = await call('GET', '/me/reports', { token: reporter.token });
report('GET /me/reports → both OPEN', mineOpen, { status: 200 }, () =>
  [first.data.id, hours.data.id].every((id) =>
    mineOpen.data.some((row) => row.id === id && row.status === 'OPEN'),
  ),
);

// 6. The directory owner's list: the report, and no reporter anywhere.
const ownerList = await call('GET', `/manage/spaces/${verified.id}/data-reports`, {
  token: directoryOwner.token,
});
report('owner GET …/data-reports → the report, no reporter anywhere', ownerList, { status: 200 }, () =>
  ownerList.data.some((row) => row.id === first.data.id) &&
  !ownerList.text.includes(reporter.user.name) &&
  !ownerList.text.includes(reporter.user.email) &&
  !ownerList.text.includes('userId') &&
  !new RegExp(`:${reporter.user.id}[,}]`).test(ownerList.text),
);

// 7–8. The owner resolves it; another decision is refused.
const resolved = await call('PATCH', `/manage/spaces/${verified.id}/data-reports/${first.data.id}`, {
  token: directoryOwner.token,
  body: { status: 'RESOLVED', note: 'حُدّثت الأسعار' },
});
report('owner PATCH { RESOLVED, note } → 200', resolved, { status: 200 }, () =>
  resolved.data.decision.repliedBy === 'SPACE',
);
const twice = await call('PATCH', `/manage/spaces/${verified.id}/data-reports/${first.data.id}`, {
  token: directoryOwner.token,
  body: { status: 'DISMISSED', note: 'غير ذلك' },
});
report('owner PATCH { DISMISSED } → 409 REPORT_ALREADY_DECIDED', twice, {
  status: 409,
  code: 'REPORT_ALREADY_DECIDED',
});

// 9–11. The admin: the list with the reporter's name; the verified space's refused; the unverified one's.
const adminList = await call('GET', '/admin/data-reports?limit=50', { token: admin.token });
report("admin GET /admin/data-reports → the reporter's name", adminList, { status: 200 }, () =>
  adminList.data.some(
    (row) => row.id === hours.data.id && row.reporter.name === reporter.user.name && !row.space.verified,
  ),
);
const adminVerified = await call('PATCH', `/admin/data-reports/${first.data.id}`, {
  token: admin.token,
  body: { status: 'RESOLVED' },
});
report("admin PATCH the verified space's → 403", adminVerified, { status: 403 });
const bare = await call('PATCH', `/admin/data-reports/${hours.data.id}`, {
  token: admin.token,
  body: { status: 'DISMISSED' },
});
report('admin PATCH { DISMISSED } without a note → 422', bare, { status: 422 });
const dismissed = await call('PATCH', `/admin/data-reports/${hours.data.id}`, {
  token: admin.token,
  body: { status: 'DISMISSED', note: 'الساعات صحيحة' },
});
report('admin PATCH { DISMISSED, note } → 200 MASAHA', dismissed, { status: 200 }, () =>
  dismissed.data.decision.repliedBy === 'MASAHA',
);

// 12. The reporter's decided ones: SPACE and MASAHA.
const decided = await call('GET', '/me/reports?status=DECIDED', { token: reporter.token });
report('GET /me/reports?status=DECIDED → repliedBy SPACE and MASAHA', decided, { status: 200 }, () =>
  decided.data.some((row) => row.id === first.data.id && row.decision.repliedBy === 'SPACE') &&
  decided.data.some((row) => row.id === hours.data.id && row.decision.repliedBy === 'MASAHA'),
);

// 13. The limit, last: CONTACT once, then the same until the 11th request of the hour.
const contact = await post(verified.slug, { field: 'CONTACT' });
report('reporter POST verified { CONTACT } → 201', contact, { status: 201 });
let limited = null;
while (counted < 12) {
  const repeat = await post(verified.slug, { field: 'CONTACT' });
  if (repeat.status === 429) {
    limited = repeat;
    break;
  }
  if (repeat.status !== 200 || repeat.data.id !== contact.data.id) {
    report('a repeat of CONTACT → 200, the same id', repeat, { status: 200 });
    break;
  }
}
if (limited) {
  report(`the ${counted}th report request of the hour → 429 with Retry-After`, limited, { status: 429 }, () =>
    counted === 11 && Number(limited.retryAfter) > 0,
  );
} else {
  failures += 1;
  console.log(`FAIL no 429 after ${counted} requests - -`);
}
console.log(`     report requests sent: ${counted}`);
const contacts = await call('GET', '/me/reports?status=OPEN', { token: reporter.token });
report('the repeats wrote nothing: one open CONTACT report', contacts, { status: 200 }, () =>
  contacts.data.filter((row) => row.field === 'CONTACT' && row.space.id === verified.id).length === 1,
);

console.log(failures === 0 ? 'ALL PASS' : `${failures} FAILED`);
process.exit(failures === 0 ? 0 : 1);
