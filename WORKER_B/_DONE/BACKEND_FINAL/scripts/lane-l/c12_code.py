p = r"C:\dev\masaha\app-b-lane-l\apps\api\src\modules\sessions\sessions.repository.ts"
s = open(p, encoding="utf-8", newline="").read()
old = """    /** When the session was last used, by its newest token; nothing once it has no token. */
    async familyActivity(familyId: number, tx: Tx = db): Promise<Date | undefined> {
      const newest = await tx.refreshToken.findFirst({
        where: { familyId },
        orderBy: { id: 'desc' },
        select: { lastActivityAt: true },
      });
      return newest?.lastActivityAt;
    },
"""
new = """    /**
     * When the session was last used, the latest of its tokens: a renewal racing a rotation renews
     * the presented token alone (finding 170). Nothing once it has no token.
     */
    async familyActivity(familyId: number, tx: Tx = db): Promise<Date | undefined> {
      const { _max } = await tx.refreshToken.aggregate({
        where: { familyId },
        _max: { lastActivityAt: true },
      });
      return _max.lastActivityAt ?? undefined;
    },
"""
assert s.count(old) == 1
s = s.replace(old, new, 1)
open(p, "w", encoding="utf-8", newline="").write(s)

p = r"C:\dev\masaha\app-b-lane-l\apps\api\src\modules\sessions\sessions.service.ts"
s = open(p, encoding="utf-8", newline="").read()
old = """      if (stored.expiresAt <= at) return { outcome: 'invalid' };
      if (
        idleAfterMs !== undefined &&
        at.getTime() - stored.lastActivityAt.getTime() > idleAfterMs
      ) {
"""
new = """      if (stored.expiresAt <= at) return { outcome: 'invalid' };
      // The session's last use is its family's latest, which the new token carries on.
      const lastActivityAt =
        (await repository.familyActivity(stored.familyId, tx)) ?? stored.lastActivityAt;
      if (idleAfterMs !== undefined && at.getTime() - lastActivityAt.getTime() > idleAfterMs) {
"""
assert s.count(old) == 1
s = s.replace(old, new, 1)
old = """      const next = await issueInFamily(stored.userId, stored, at, tx);
"""
new = """      const next = await issueInFamily(stored.userId, { ...stored, lastActivityAt }, at, tx);
"""
assert s.count(old) == 1
s = s.replace(old, new, 1)
open(p, "w", encoding="utf-8", newline="").write(s)
