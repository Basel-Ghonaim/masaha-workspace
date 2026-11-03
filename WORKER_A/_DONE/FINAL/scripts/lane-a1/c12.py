def edit(p, pairs):
    s = open(p, encoding='utf8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)
A = r'C:\dev\masaha\app-lane-a1\apps\api\src'
edit(A + r'\shared\rate-limit\counter.ts', [
("""export function createCounter(db: PrismaClient = prisma): Counter {""",
"""/** How many rows a sweep deletes at most a table a run, so a run stays within the function's time. */
export const SWEEP_BATCH = 5_000;

/**
 * Deletes the counters whose window has ended by `now`, at most `SWEEP_BATCH`, the earliest ended
 * first: a key hit again starts a new window anyway, so an ended row only takes room (finding 17).
 * The window's end is checked again on the row deleted, so a hit that has just started a new
 * window keeps it. How many it deleted.
 */
export function sweepEndedWindows(now: Date, db: PrismaClient = prisma): Promise<number> {
  return db.$executeRaw`
    DELETE FROM rate_limits
    WHERE reset_at <= ${now} AND key IN (
      SELECT key FROM rate_limits WHERE reset_at <= ${now} ORDER BY reset_at, key LIMIT ${SWEEP_BATCH}
    )`;
}

export function createCounter(db: PrismaClient = prisma): Counter {"""),
])
edit(A + r'\shared\rate-limit\index.ts', [("export { createCounter, type Count, type Counter } from './counter.ts';",
 "export {\n  createCounter,\n  SWEEP_BATCH,\n  sweepEndedWindows,\n  type Count,\n  type Counter,\n} from './counter.ts';")])
edit(A + r'\modules\sessions\sessions.repository.ts', [
("""    /** A new reset token. Earlier ones stay until this one is delivered. Its id. */""",
"""    /**
     * Deletes the rows ended by `now`, at most `limit` a table, oldest first: the recoveries past
     * their end, the reset tokens past theirs (a recovery bound to one ends with it), and the refresh
     * tokens past their own expiry or their session's end. Each condition is checked again on the row
     * deleted. How many of each it deleted.
     */
    async sweepExpired(
      now: Date,
      limit: number,
      tx: Tx = db,
    ): Promise<{ refreshTokens: number; resetTokens: number; recoveries: number }> {
      const recoveries = await tx.$executeRaw`
        DELETE FROM password_recoveries WHERE expires_at <= ${now} AND id IN (
          SELECT id FROM password_recoveries WHERE expires_at <= ${now} ORDER BY id LIMIT ${limit}
        )`;
      const resetTokens = await tx.$executeRaw`
        DELETE FROM password_reset_tokens WHERE expires_at <= ${now} AND id IN (
          SELECT id FROM password_reset_tokens WHERE expires_at <= ${now} ORDER BY id LIMIT ${limit}
        )`;
      const refreshTokens = await tx.$executeRaw`
        DELETE FROM refresh_tokens
        WHERE (expires_at <= ${now} OR session_ends_at <= ${now}) AND id IN (
          SELECT id FROM refresh_tokens WHERE expires_at <= ${now} OR session_ends_at <= ${now}
          ORDER BY id LIMIT ${limit}
        )`;
      return { refreshTokens, resetTokens, recoveries };
    },

    /** A new reset token. Earlier ones stay until this one is delivered. Its id. */"""),
])
edit(A + r'\modules\sessions\sessions.service.ts', [
("""/** How many more links one recovery may ask for. */
export const RECOVERY_MAX_RESENDS = 3;""", """/** How many more links one recovery may ask for. */
export const RECOVERY_MAX_RESENDS = 3;
/** How many rows the sweep deletes at most a table a run, so a run stays within the function's time. */
export const SWEEP_BATCH = 5_000;"""),
("""    /** Ends every session of the user. */""", """    /**
     * The timed sweep (finding 17): deletes the refresh tokens, reset tokens and recoveries that
     * ended by `at`, at most `SWEEP_BATCH` a table a run. A session that is never refreshed again
     * would otherwise keep its rows. How many of each it deleted.
     */
    sweepExpired(at: Date): Promise<{ refreshTokens: number; resetTokens: number; recoveries: number }> {
      return repository.sweepExpired(at, SWEEP_BATCH);
    },

    /** Ends every session of the user. */"""),
])
edit(A + r'\app.ts', [
("""      { name: 'subscriptions.autoCheckOut', run: (at) => subscriptions.autoCheckOut(at) },
    ],""", """      { name: 'subscriptions.autoCheckOut', run: (at) => subscriptions.autoCheckOut(at) },
      // The ended rows of identity and of the rate limits, swept (finding 17).
      { name: 'sessions.sweepExpired', run: (at) => sessions.sweepExpired(at) },
      {
        name: 'rateLimits.sweepExpired',
        run: async (at) => ({ counters: await sweepEndedWindows(at) }),
      },
    ],"""),
])
