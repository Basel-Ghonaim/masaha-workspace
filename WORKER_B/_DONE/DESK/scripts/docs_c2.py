import io, os
os.chdir('C:/dev/masaha/app-b')


def sub(p, old, new):
    s = io.open(p, encoding='utf-8', newline='').read()
    assert s.count(old) == 1, (p, old[:60], s.count(old))
    io.open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new))


c = 'docs/api/api-contract.md'
sub(c, "\n### Lookups (public)\n", """
### Internal

The timed jobs ([ADR 0014](../architecture/decisions/0014-deployment.md); [conventions §12](../backend/conventions.md#12-environments-and-adapters)): online, an external cron calls this endpoint every 5 minutes; locally, the server runs the same jobs from a timer. It carries no access token, so the general limit counts it by address ([security › Rate limits](../backend/security.md#rate-limits)). Built 2026-10-20, #PRNUM.

#### `POST /internal/jobs/run`
- **Mounted only when `JOBS_SECRET` is set;** otherwise `not_found` (404), as any unknown path.
- **Auth:** `Authorization: Bearer <JOBS_SECRET>`, compared in constant time; a missing or wrong secret is `unauthorized` (401), no code, and runs nothing.
- **Runs** each job in turn, each at the run's time: `visits.autoCheckOut` and `subscriptions.autoCheckOut` close every open stay whose due time has passed, at that due time, never at the run's ([data-model › Front desk and money](../architecture/data-model.md#front-desk-and-money), *Auto check-out*), up to 500 a job a run; `remaining` counts the due stays left to the next run. A second run closes nothing more.
- **200:** `{ ranAt, jobs: [{ name, done }] }`, `done` each job's counts (`{ visits, remaining }`, `{ checkIns, remaining }`).
- **Errors:** `server` (500) when any job failed: the others still ran, and the failure is logged with the job's name, so the cron service shows it.
- **Audit:** `visit.autoCheckedOut` (`after`: `{ checkedOutAt, chargeAgorot }`) and `checkIn.autoCheckedOut` (`after`: `{ checkedOutAt }`), each with no actor, in the closing's own transaction.

### Lookups (public)
""")

v = 'docs/backend/conventions.md'
sub(v, "the ledger's translation table (§4, §13). **Not yet built:** `optionalAuth` (§7); the audit reader (§6); every other module; the scheduler port (§12) ·",
    "the ledger's translation table (§4, §13); the scheduler port (§12), with the auto check-out of `visits` and `subscriptions`. **Not yet built:** `optionalAuth` (§7); the audit reader (§6); every other module ·")
sub(v, "an internal, secret-protected endpoint that an external cron calls every few minutes. The slice that builds it adds its path to the API contract |",
    "`POST /api/v1/internal/jobs/run`, behind `JOBS_SECRET` ([api-contract › Internal](../api/api-contract.md#internal)), which an external cron calls every 5 minutes; locally, `server.ts` runs the same jobs every 5 minutes, the first 10 s after start |")

s = 'docs/backend/security.md'
sub(s, "- **`CLOUDINARY_URL` is a secret:**",
    "- **`JOBS_SECRET` is a secret:** the timed jobs' endpoint ([api-contract › Internal](../api/api-contract.md#internal)) is mounted only when it is set, and production requires it. At least 32 characters; compared in constant time, through the SHA-256 digests of the header and of `Bearer <JOBS_SECRET>`; never logged (the request logger redacts the `authorization` header). 2026-10-20, #PRNUM.\n- **`CLOUDINARY_URL` is a secret:**")
sub(s, "the photo upload's limits, its content check and its re-encoding. **Not yet built:**",
    "the photo upload's limits, its content check and its re-encoding; the timed jobs' secret (`JOBS_SECRET`). **Not yet built:**")

u = 'docs/development/setup.md'
sub(u, "\n## The API test lane\n", """
### Timed jobs

The auto check-out runs as a timed job ([api-contract › Internal](../api/api-contract.md#internal)). Locally, the API runs it itself: 10 s after start, then every 5 minutes, logging one `job ran` line per job. `JOBS_SECRET` is optional locally: without it, the endpoint is not mounted.

Online, set `JOBS_SECRET` (a random value of at least 32 characters) in the host's settings, and create one job on a free external cron service (for example cron-job.org): `POST https://<host>/api/v1/internal/jobs/run` every 5 minutes, with the header `Authorization: Bearer <JOBS_SECRET>`. A failed run answers 500, which the service shows; a missed run is caught up by the next.

## The API test lane
""")
sub(u, "> **Status:** Active · **Last Updated:** 2026-10-10 ·", "> **Status:** Active · **Last Updated:** 2026-10-20 ·")

e = 'apps/api/.env.example'
sub(e, "\n# fatal | error | warn | info | debug | trace | silent (default: info)\n", """
# The secret an external cron sends to run the timed jobs (the auto check-out): POST
# /api/v1/internal/jobs/run with Authorization: Bearer <JOBS_SECRET>. A random value of at least 32
# characters, never committed; required in production. Empty locally: the endpoint is then not
# mounted, and the API runs the jobs itself every 5 minutes.
JOBS_SECRET=

# fatal | error | warn | info | debug | trace | silent (default: info)
""")

d = 'docs/architecture/data-model.md'
sub(d, "a stay never crosses into the next day, nor is it due before its check-in (2026-10-20, #PRNUM).",
    "a stay never crosses into the next day, nor is it due before its check-in (2026-10-20, #PRNUM). The job closes each stay at its due time, never at the run's, and charges a visit for the stay up to then, by its rates and the rounding and cap in force at the run; a change of the settings applies from then on, so a stay limit set later closes an open stay at its new due time, possibly past (2026-10-20, #PRNUM).")

f = 'docs/features/visits.md'
sub(f, "- Answers the open visits of a space, how many, and what each costs so far, for *present* ([occupancy](occupancy.md)).",
    "- Answers the open visits of a space, how many, and what each costs so far, for *present* ([occupancy](occupancy.md)).\n- Closes every open visit whose auto check-out time has passed, at that time, charged to it: the timed job `visits.autoCheckOut`.")
sub(f, "- **`occupancy`**, which reads the open visits for *present*. No web screen reads it yet.",
    "- **`occupancy`**, which reads the open visits for *present*. No web screen reads it yet.\n- **The timed jobs** (`shared/jobs`, wired in the composition root), which run its auto check-out.")
sub(f, "- **Reads** the space's prices and shifts from [`spaces`](spaces.md), and the settings",
    "- **Reads** the space's prices and shifts, its week and a stay's auto check-out time from [`spaces`](spaces.md), and the settings")
sub(f, "\n## Decisions\n", """
**The auto check-out.** Every open visit, of every space, a soft-deleted or hidden one's too, the earliest first; the weeks and the settings of their spaces, as they are now, in one query each; each visit's due time by `spaces`' rule; the ones due by the run's time, up to 500. Each in its own transaction: its row locked (`FOR UPDATE`) only while still open, so a check-out at the desk meanwhile wins and is left as it is; closed `AUTO` at its due time, charged for the stay up to then (none without a rate, left uncollected with no customer), and audited `visit.autoCheckedOut` with no actor.

## Decisions
""")
sub(f, "both times say which (the owner's decision). 2026-10-20, #95.",
    """both times say which (the owner's decision). 2026-10-20, #95.
- **The auto check-out closes a visit at its due time, never at the run's, each in its own transaction under its row's lock.** *Why:* a run every 5 minutes, or one after a pause, must charge what the closing would have; one failure must not undo the others, and a check-out at the desk meanwhile wins. 2026-10-20, #PRNUM.
- **It reads the week and the settings at the run.** *Why:* a change applies from then on, so a stay limit set later closes an open stay at its new due time (data model, *Auto check-out*). 2026-10-20, #PRNUM.
- **At most 500 visits a run; the rest are counted in `remaining` and closed by the next.** *Why:* one run stays short, online as locally; a backlog is caught up run by run. 2026-10-20, #PRNUM.""")
sub(f, "the service, the repository, the mapper, the controller and the manage router, and the rates and charge rules (`visitCharge.ts`).",
    "the service (the auto check-out included), the repository, the mapper, the controller and the manage router, and the rates and charge rules (`visitCharge.ts`).")
sub(f, "the quote, the terms and the charges so far.\n",
    "the quote, the terms and the charges so far.\n- #PRNUM — the auto check-out of visits.\n")

k = 'docs/features/desk.md'
sub(k, "- Checks a visit out: the charge at the quote's time,",
    "- Leaves the stays it does not close to the auto check-out, which [`visits`](visits.md) and `subscriptions` run as timed jobs.\n- Checks a visit out: the charge at the quote's time,")
print('ok')
