p = r'C:\dev\masaha\app-lane-a1\apps\api\src\modules\sessions\sessions.service.unit.test.ts'
s = open(p, encoding='utf8').read()
n = s.count('createSessionsService({')
s = s.replace('createSessionsService({', 'createSessionsService({ successorKey: KEY,')
def rep(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)
rep("import { hashToken } from './tokens.ts';", "import { hashToken, successorKeyOf, successorOf } from './tokens.ts';")
rep("const at = (ms: number) => new Date(NOW.getTime() + ms);", "const at = (ms: number) => new Date(NOW.getTime() + ms);\nconst KEY = successorKeyOf('a-test-secret-of-at-least-32-characters');")
rep("""/** A repository holding one stored token, which records what the service asks of it. */
function fakeRepository(stored: StoredRefreshToken | null, { rotates = true } = {}) {
  const calls: string[] = [];
  const created: { expiresAt: Date; familyId?: number }[] = [];
  const repository = {
    findRefreshToken: () => Promise.resolve(stored),""", """/**
 * A repository holding one stored token, `t`, and its successor while `successor` holds, which
 * records what the service asks of it.
 */
function fakeRepository(
  stored: StoredRefreshToken | null,
  { rotates = true, successor = true } = {},
) {
  const calls: string[] = [];
  const created: { expiresAt: Date; familyId?: number; tokenHash?: string }[] = [];
  const repository = {
    findRefreshToken: (tokenHash: string) => {
      if (tokenHash === hashToken('t')) return Promise.resolve(stored);
      const found = successor && tokenHash === hashToken(successorOf('t', KEY));
      return Promise.resolve(found && stored ? { ...stored, id: 2, rotatedAt: null } : null);
    },""")
rep("""    createRefreshToken: (token: { expiresAt: Date; familyId?: number }) => {""", """    createRefreshToken: (token: { expiresAt: Date; familyId?: number; tokenHash?: string }) => {""")
rep("""  it('rotates a fresh token, marks it, and keeps its family', async () => {
    const { calls, created, repository } = fakeRepository(token(null));
    const sessions = createSessionsService({ successorKey: KEY, repository, now: () => NOW });

    const rotation = await sessions.rotate('t', tx);

    expect(rotation.outcome).toBe('rotated');
    expect(calls).toEqual(['markRotated']);
    expect(created[0]?.familyId).toBe(1);
  });

  it('honours a token rotated 30,000 ms ago, and adds a sibling without marking it again', async () => {
    const { calls, repository } = fakeRepository(token(NOW));
    const sessions = createSessionsService({ successorKey: KEY, repository, now: () => at(30_000) });

    expect((await sessions.rotate('t', tx)).outcome).toBe('rotated');
    expect(calls).toEqual([]);
  });
""", """  it('rotates a fresh token to its successor, marks it, and keeps its family', async () => {
    const { calls, created, repository } = fakeRepository(token(null));
    const sessions = createSessionsService({ successorKey: KEY, repository, now: () => NOW });

    const rotation = await sessions.rotate('t', tx);

    expect(rotation).toEqual({
      outcome: 'rotated',
      issued: { token: successorOf('t', KEY), familyId: 1 },
    });
    expect(calls).toEqual(['markRotated']);
    expect(created[0]?.familyId).toBe(1);
    expect(created[0]?.tokenHash).toBe(hashToken(successorOf('t', KEY)));
  });

  it('answers a token rotated 30,000 ms ago with its successor, adding nothing', async () => {
    const { calls, created, repository } = fakeRepository(token(NOW));
    const sessions = createSessionsService({
      successorKey: KEY,
      repository,
      now: () => at(30_000),
    });

    expect(await sessions.rotate('t', tx)).toEqual({
      outcome: 'rotated',
      issued: { token: successorOf('t', KEY), familyId: 1 },
    });
    expect(calls).toEqual([]);
    expect(created).toEqual([]);
  });

  it('refuses a token within the grace whose successor has ended', async () => {
    const { repository } = fakeRepository(token(NOW), { successor: false });
    const sessions = createSessionsService({
      successorKey: KEY,
      repository,
      now: () => at(1_000),
    });

    expect((await sessions.rotate('t', tx)).outcome).toBe('invalid');
  });
""")
open(p, 'w', encoding='utf8', newline='').write(s)
print(n)
