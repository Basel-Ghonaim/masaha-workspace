import io, os
os.chdir('C:/dev/masaha/app-b')
def edit(path, pairs):
    t = io.open(path, encoding='utf-8', newline='').read()
    for old, new in pairs:
        assert t.count(old) == 1, (path, old[:70], t.count(old))
        t = t.replace(old, new)
    io.open(path, 'w', encoding='utf-8', newline='').write(t)
def write(path, text):
    io.open(path, 'w', encoding='utf-8', newline='').write(text)

edit('docs/api/api-contract.md', [
("- **Errors:** `server` (500) when any job failed: the others still ran, and the failure is logged with the job's name, so the cron service shows it.",
 "- **Errors:** `server` (500) when any job failed: the others still ran, and the failure is logged with the job's name, so the cron service shows it. A job fails when any of its stays could not be closed: the stays after it are still closed, and each one not closed is logged with its id (`stay not closed`)."),
])
edit('docs/features/visits.md', [
("one failure must not undo the others, and a check-out at the desk meanwhile wins. 2026-10-20, #97.",
 "one failure must not undo the others, and a check-out at the desk meanwhile wins. 2026-10-20, #97. A visit that cannot be closed is logged, the next ones are still closed, and the job then fails, so the cron service shows it; a space without its settings row fails only its own visits. *Why:* one bad stay must not halt the job for every space (#97's review). 2026-10-20, #PRNUM."),
("- **Leaves** the transaction, the space's lock, and the decision under it of who may type a price to [`desk`](desk.md);",
 "- **Leaves** the check-out's transaction, the space's lock and the check-out's typed-price decision to [`desk`](desk.md);"),
("- Each change is audited by the audit writer, in the caller's transaction ([conventions §6](../backend/conventions.md#6-audit)).",
 "- It runs its own transactions for the auto check-out (one per visit) and the pricing of an unpriced visit (under the space's lock); the check-in and the check-out run in the desk's.\n- Each change is audited by the audit writer, in its transaction ([conventions §6](../backend/conventions.md#6-audit))."),
])
edit('docs/backend/conventions.md', [
("  | Scheduler | an in-process timer started by `server.ts` | `POST /api/v1/internal/jobs/run`, behind `JOBS_SECRET` ([api-contract › Internal](../api/api-contract.md#internal)), which an external cron calls every 5 minutes; locally, `server.ts` runs the same jobs every 5 minutes, the first 10 s after start |",
 "  | Scheduler | an in-process timer started by `server.ts`: the same jobs every 5 minutes, the first 10 s after start | `POST /api/v1/internal/jobs/run`, behind `JOBS_SECRET` ([api-contract › Internal](../api/api-contract.md#internal)), which an external cron calls every 5 minutes |"),
])
edit('apps/api/.env.example', [
("# characters, never committed; required in production. Empty locally: the endpoint is then not\n# mounted, and the API runs the jobs itself every 5 minutes.",
 "# characters, never committed; required in production. The API's own server runs the jobs every 5\n# minutes either way; without it, the endpoint is not mounted."),
])
edit('docs/development/setup.md', [
("with the header `Authorization: Bearer <JOBS_SECRET>`. A failed run",
 "with the header `Authorization: Bearer <JOBS_SECRET>`, written exactly so (`Bearer` with its capital, one space, the secret). A failed run"),
])

F = 'docs/architecture/findings/'
write(F + '111-the-check-ins-warnings-count-present-a-second-time.md', """# 111. The check-in's warnings count *present* a second time

**Status:** Open · **Date:** 2026-10-20

**Evidence:** `occupancy.service.ts`'s `checkInWarnings` adds `visits.openIn(…).length + subscriptions.openCheckInsIn(…).length` itself, while the live read (`peopleIn`) and the directory (`liveStatusFor`) have their own forms of *present*. The three agree today, but [occupancy](../../features/occupancy.md) calls *present* one definition, and the warnings load every open row only to count them (#95's review, nit 7).

**Resolves when:** one `occupancy` helper answers *present* for a space, and the live read and the check-in's warnings both use it.
""")
write(F + '112-a-key-that-closed-a-visit-with-no-payment-is-not-remembered.md', """# 112. A key that closed a visit with no payment is not remembered

**Status:** Open · **Date:** 2026-10-20

**Evidence:** the desk's check-out (`desk.service.ts`, `checkOutVisit`) recognises a retried key only through the payment it recorded. A check-out with key K that records no payment (all of it left unpaid, or an unpriced close) leaves no trace of K. If K is then sent for another visit, that visit is checked out as a new request, and a real retry of the first request is answered `conflict` ("a key that paid another item") instead of its first result. It needs a client that reuses a key across two actions, which is a client fault (#95's review, nit 8).

**Resolves when:** a check-out's key is remembered whatever it recorded, so its retry always answers its first result, or the owner accepts the rule as it is.
""")
write(F + '113-the-uncollected-read-grows-with-every-auto-closed-visit.md', """# 113. The uncollected read grows with every auto-closed visit

**Status:** Open · **Date:** 2026-10-20

**Evidence:** `payments.service.ts`'s `uncollectedIn` reads every visit of the space ever closed by the auto check-out (`visits.repository.ts`, `autoClosedIn`), sums all their payments, and sends every settled id back as bound parameters (`autoClosedPage`, `id: { notIn: [...] }`). The list only grows. At some tens of thousands of settled auto-closed visits in one space, the statement nears PostgreSQL's 65,535 bound parameters and the read answers 500; long before that, it is slow. The plan held it fine at v1's scale (#97's review, nit 7).

**Resolves when:** the settled visits are filtered in SQL (one query over the non-voided payments, owned by `payments`) or by a stored flag, so a read costs what its page holds; an architecture choice for the owner.
""")
edit(F + 'README.md', [
("- [100. An unpaid check-out moves a visit's customer to the phone's](100-an-unpaid-check-out-moves-a-visits-customer-to-the-phones.md)\n",
 "- [100. An unpaid check-out moves a visit's customer to the phone's](100-an-unpaid-check-out-moves-a-visits-customer-to-the-phones.md)\n- [111. The check-in's warnings count *present* a second time](111-the-check-ins-warnings-count-present-a-second-time.md)\n- [112. A key that closed a visit with no payment is not remembered](112-a-key-that-closed-a-visit-with-no-payment-is-not-remembered.md)\n- [113. The uncollected read grows with every auto-closed visit](113-the-uncollected-read-grows-with-every-auto-closed-visit.md)\n"),
])
print('ok')
