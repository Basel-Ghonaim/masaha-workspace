p = r'C:\dev\masaha\app-lane-a1\apps\api\src\modules\sessions\sessions.service.ts'
s = open(p, encoding='utf8').read()
def rep(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)
rep("import { hashToken, newToken } from './tokens.ts';", "import { hashToken, newToken, successorOf } from './tokens.ts';")
rep("""interface Dependencies {
  repository?: SessionsRepository;""", """interface Dependencies {
  /** Names each refresh token's successor (`successorKeyOf`, from the access tokens' secret). */
  successorKey: Buffer;
  repository?: SessionsRepository;""")
rep("""export function createSessionsService({
  repository = createSessionsRepository(),
  now = () => new Date(),
}: Dependencies = {}) {
  async function issueInFamily(
    userId: number,
    family: { familyId: number; sessionEndsAt: Date; lastActivityAt: Date } | undefined,
    at: Date,
    tx?: Tx,
  ) {
    const token = newToken();""", """export function createSessionsService({
  successorKey,
  repository = createSessionsRepository(),
  now = () => new Date(),
}: Dependencies) {
  async function issueInFamily(
    userId: number,
    family: { familyId: number; sessionEndsAt: Date; lastActivityAt: Date } | undefined,
    at: Date,
    tx?: Tx,
    token = newToken(),
  ) {""")
rep("""      // A session that keeps refreshing never signs in again, so its expired rows go here: a
      // live session keeps the tokens of its last 7 days, which reuse detection needs.
      await repository.deleteExpired(stored.userId, at, tx);
      const next = await issueInFamily(stored.userId, { ...stored, lastActivityAt }, at, tx);
      // Within the grace window the token already has its successor, and the new token joins the
      // session beside it. Otherwise it is marked rotated now: the session lock means no concurrent
      // refresh can have done it first.
      if (!stored.rotatedAt && !(await repository.markRotated(stored.id, next.stored.id, at, tx))) {
        throw new Error('A refresh token was rotated concurrently, despite the session lock');
      }
      return { outcome: 'rotated', issued: next.issued };""", """      // A token has one successor, named by the token itself (finding 21): within the grace window
      // it already has it, and gets it again as it is, so a copy presented then gains nothing it
      // could keep apart. A successor gone with its session leaves nothing to renew.
      const successor = successorOf(token, successorKey);
      if (stored.rotatedAt) {
        const existing = await repository.findRefreshToken(hashToken(successor), tx);
        return existing
          ? { outcome: 'rotated', issued: { token: successor, familyId: existing.familyId } }
          : { outcome: 'invalid' };
      }

      // A session that keeps refreshing never signs in again, so its expired rows go here: a
      // live session keeps the tokens of its last 7 days, which reuse detection needs.
      await repository.deleteExpired(stored.userId, at, tx);
      const next = await issueInFamily(
        stored.userId,
        { ...stored, lastActivityAt },
        at,
        tx,
        successor,
      );
      // Marked rotated now: the session lock means no concurrent refresh can have done it first.
      if (!(await repository.markRotated(stored.id, next.stored.id, at, tx))) {
        throw new Error('A refresh token was rotated concurrently, despite the session lock');
      }
      return { outcome: 'rotated', issued: next.issued };""")
open(p, 'w', encoding='utf8', newline='').write(s)
