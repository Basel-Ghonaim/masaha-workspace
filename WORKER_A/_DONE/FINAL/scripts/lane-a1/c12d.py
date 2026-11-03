def edit(p, pairs):
    s = open(p, encoding='utf8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)
D = r'C:\dev\masaha\app-lane-a1\docs'
edit(D + r'\architecture\data-model.md', [
("for reception's idle end (2026-10-25, #118) ([security › Tokens and cookies](../backend/security.md#tokens-and-cookies)). Cascades from its user.",
 "for reception's idle end (2026-10-25, #118) ([security › Tokens and cookies](../backend/security.md#tokens-and-cookies)). Cascades from its user. A timed job deletes the rows past their own expiry or their session's end (2026-10-29, #PRNUM)."),
("- **PasswordResetToken** — a single-use reset token, stored hashed, with an expiry. Cascades from its user.",
 "- **PasswordResetToken** — a single-use reset token, stored hashed, with an expiry. Cascades from its user. A timed job deletes the expired rows (2026-10-29, #PRNUM)."),
("and may hold the reset link checked in its browser, with which it ends. It cascades from its user and from that link.",
 "and may hold the reset link checked in its browser, with which it ends. It cascades from its user and from that link. A timed job deletes the expired rows (2026-10-29, #PRNUM)."),
("The rate limits and the reset email's caps share it ([security.md](../backend/security.md#rate-limits-fixed-window)). It belongs to no user.",
 "The rate limits and the reset email's caps share it ([security.md](../backend/security.md#rate-limits-fixed-window)). It belongs to no user. A timed job deletes the rows whose window has ended (2026-10-29, #PRNUM)."),
])
edit(D + r'\backend\security.md', [
("""- `express-rate-limit`, approved in the foundation plan, is **not used**.""",
"""- **Ended windows are swept:** a timed job, `rateLimits.sweepExpired`, deletes the rows whose window has ended (`reset_at` by the run's time), at most 5,000 a run, the earliest ended first; the window's end is checked again on each row deleted, so a key hit at that moment keeps its new window. A key hit again only starts a new window, so an ended row holds nothing a limit reads. Beside it, `sessions.sweepExpired` deletes the refresh tokens past their own expiry or their session's end, the reset tokens and the recoveries past theirs, 5,000 a table a run ([finding 17](../architecture/findings/17-expired-rate-limit-counters-and-abandoned-sessions-are-never-swept.md); [api-contract › Internal](../api/api-contract.md#internal)). 2026-10-29, #PRNUM.
- `express-rate-limit`, approved in the foundation plan, is **not used**."""),
])
edit(D + r'\api\api-contract.md', [
("""A second run closes nothing more.
- **200:** `{ ranAt, jobs: [{ name, done }] }`, `done` each job's counts (`{ visits, remaining, failed }`, `{ checkIns, remaining, failed }`).""",
"""A second run closes nothing more. Then `sessions.sweepExpired` deletes the refresh tokens past their own expiry or their session's end, the reset tokens and the recoveries past theirs, and `rateLimits.sweepExpired` the rate-limit counters whose window has ended, each at most 5,000 rows a table a run, oldest first ([security › Rate limits](../backend/security.md#rate-limits-fixed-window); 2026-10-29, #PRNUM).
- **200:** `{ ranAt, jobs: [{ name, done }] }`, `done` each job's counts (`{ visits, remaining, failed }`, `{ checkIns, remaining, failed }`, `{ refreshTokens, resetTokens, recoveries }`, `{ counters }`)."""),
])
p = D + r'\architecture\findings\17-expired-rate-limit-counters-and-abandoned-sessions-are-never-swept.md'
s = open(p, encoding='utf8').read()
old = '**Status:** Open · **Date:** 2026-10-01 · **Corrected:** 2026-10-02'
assert s.count(old) == 1
s = s.replace(old, '**Status:** Resolved · **Date:** 2026-10-01 · **Corrected:** 2026-10-02 · **Resolved:** 2026-10-29')
s = s.rstrip('\n') + '\n\n**Resolution (#PRNUM):** Two timed jobs sweep the expired refresh tokens, reset tokens, recoveries and rate-limit counters, 5,000 rows a table a run (D1.2).\n'
open(p, 'w', encoding='utf8', newline='').write(s)
edit(D + r'\features\auth.md', [("- #PRNUM — a replay within the grace gets its token's one successor.",
 "- #PRNUM — a replay within the grace gets its token's one successor; the ended tokens and recoveries swept by a timed job.")])
