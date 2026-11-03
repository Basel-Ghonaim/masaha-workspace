def edit(p, pairs):
    s = open(p, encoding='utf8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)
A = r'C:\dev\masaha\app-lane-a1\apps\api\src'
p = A + r'\shared\rate-limit\counter.api.test.ts'
s = open(p, encoding='utf8').read()
s = s.replace("import { createCounter } from './counter.ts';", "import { SWEEP_BATCH } from '../jobs/index.ts';\nimport { createCounter, sweepEndedWindows } from './counter.ts';")
s = s.rstrip('\n') + """

describe('sweepEndedWindows', () => {
  it('a sweep deletes ended rate-limit windows, at most 5,000 a run', async () => {
    const now = new Date('2026-10-29T10:00:00Z');
    await prisma.$executeRaw`
      INSERT INTO rate_limits (key, hits, reset_at, updated_at)
      SELECT 'ended:' || n, 1, ${now}::timestamptz - n * interval '1 second', ${now}
      FROM generate_series(0, ${SWEEP_BATCH}) AS n`;
    await counter.hit('live', MINUTE, now);

    expect(SWEEP_BATCH).toBe(5_000);
    expect(await sweepEndedWindows(now)).toBe(5_000);
    // The earliest ended go first: the one left ended last, at `now` itself.
    expect((await prisma.rateLimit.findMany({ orderBy: { key: 'asc' } })).map(({ key }) => key)).toEqual([
      'ended:0',
      'live',
    ]);
    expect(await sweepEndedWindows(now)).toBe(1);
    expect(await prisma.rateLimit.count()).toBe(1);
  });
});
"""
open(p, 'w', encoding='utf8', newline='').write(s)
p = A + r'\shared\jobs\jobs.api.test.ts'
s = open(p, encoding='utf8').read()
old1 = """        { name: 'subscriptions.autoCheckOut', done: { checkIns: 0, remaining: 0, failed: 0 } },
      ],"""
new1 = """        { name: 'subscriptions.autoCheckOut', done: { checkIns: 0, remaining: 0, failed: 0 } },
        SWEPT_NOTHING.sessions,
        SWEPT_NOTHING.rateLimits,
      ],"""
assert s.count(old1) == 1
s = s.replace(old1, new1)
old2 = """        { name: 'subscriptions.autoCheckOut', done: { checkIns: 1, remaining: 0, failed: 0 } },
      ],"""
assert s.count(old2) == 1
s = s.replace(old2, """        { name: 'subscriptions.autoCheckOut', done: { checkIns: 1, remaining: 0, failed: 0 } },
        SWEPT_NOTHING.sessions,
        SWEPT_NOTHING.rateLimits,
      ],""")
old3 = """      jobs: [{ name: 'visits.autoCheckOut', done: { visits: 1, remaining: 0, failed: 1 } }, {}],"""
assert s.count(old3) == 1
s = s.replace(old3, """      jobs: [
        { name: 'visits.autoCheckOut', done: { visits: 1, remaining: 0, failed: 1 } },
        {},
        {},
        {},
      ],""")
old4 = """      { level: 30, job: 'subscriptions.autoCheckOut', checkIns: 0, failed: 0 },
    ]);"""
assert s.count(old4) == 1
s = s.replace(old4, """      { level: 30, job: 'subscriptions.autoCheckOut', checkIns: 0, failed: 0 },
      { level: 30, job: 'sessions.sweepExpired', refreshTokens: 0 },
      { level: 30, job: 'rateLimits.sweepExpired', counters: 0 },
    ]);""")
old5 = """const stored = () => prisma.visit.findUniqueOrThrow({ where: { id: visitId } });"""
s = s.replace(old5, old5 + """

/** The sweeps' answers when nothing has ended: every row here is live. */
const SWEPT_NOTHING = {
  sessions: { name: 'sessions.sweepExpired', done: { refreshTokens: 0, resetTokens: 0, recoveries: 0 } },
  rateLimits: { name: 'rateLimits.sweepExpired', done: { counters: 0 } },
};""")
open(p, 'w', encoding='utf8', newline='').write(s)
