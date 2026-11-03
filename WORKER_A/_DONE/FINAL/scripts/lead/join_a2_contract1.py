import re

p = 'C:/dev/masaha/app-lane-a2/docs/api/api-contract.md'
s = open(p, encoding='utf8').read()
merged = (
    "- **Runs** each job in turn, each at the run's time: `visits.autoCheckOut` and `subscriptions.autoCheckOut` close "
    "every open stay whose due time has passed, at that due time, never at the run's ([data-model › Front desk and "
    "money](../architecture/data-model.md#front-desk-and-money), *Auto check-out*), up to 500 a job a run; `remaining` "
    "counts the due stays left to the next run. A second run closes nothing more. Then `sessions.sweepExpired` deletes "
    "the refresh tokens past their own expiry or their session's end, the reset tokens and the recoveries past theirs, "
    "and `rateLimits.sweepExpired` the rate-limit counters whose window has ended, each at most 5,000 rows a table a "
    "run, oldest first ([security › Rate limits](../backend/security.md#rate-limits-fixed-window); 2026-10-29, "
    "#PRNUM).\n"
    "- **200:** `{ ranAt, jobs: [{ name, done }] }`, `done` each job's counts (`{ visits, remaining, failed }`, "
    "`{ checkIns, remaining, failed }`, `{ refreshTokens, resetTokens, recoveries }`, `{ counters }`). `failed` counts "
    "the stays the job could not close: the stays after one are still closed, and each one not closed is logged with "
    "its id (`stay not closed`); the run still answers 200, so one bad stay never turns every call red (2026-10-21, "
    "#102). A job whose failures filled the batch it took, closing nothing, adds `stalled: true` to its `done` "
    "(2026-10-29, #PRNUM).\n"
    "- **Errors:** `server` (500) when a job itself threw, so it could not run: the others still ran, and the failure "
    "is logged with the job's name (`job failed`), so the cron service shows it. Also `server` (500) when a job "
    "stalled: no later run could get past those stays by itself; the others still ran, and the job is logged with its "
    "name and its count of failures (`job stalled`) (2026-10-29, #PRNUM).\n"
)
new, n = re.subn(r"<<<<<<< HEAD\n.*?\n=======\n.*?\n>>>>>>> [^\n]*\n", lambda m: merged, s, count=1, flags=re.S)
assert n == 1
assert '<<<<<<<' not in new
open(p, 'w', encoding='utf8', newline='').write(new)
print('ok')
