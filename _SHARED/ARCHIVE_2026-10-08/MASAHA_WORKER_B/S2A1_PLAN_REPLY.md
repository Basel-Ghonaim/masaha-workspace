The plan is approved, with the answers and four adjustments below. Build it.

## Your three challenges — all accepted
1. **Duplicates = the database's keys.** Ship L5 on the existing unique keys; record a finding
   proposing unique English names (and an amenity's Arabic name) in a later migration.
2. **No `can()` call in the lookups services.** The `/admin` guard is the authorization; reword the
   `can.ts` comment as you proposed.
3. **The order endpoints answer 204.**

## Four adjustments
A. **No empty admin router.** Commit 1 as planned would mount `/admin` with nothing behind it, so
   `requireRole` lands with no consumer. Fold `requireRole`, its unit test, the `/admin` mount and
   the `can.ts` comment into the governorates commit, its first consumer (as you did for the audit
   writer). Three commits: governorates (with the guard, the writer, `parseId`, the helpers),
   areas, amenities.

B. **No third copy of `signedIn`.** Finding 25 says the helper is already written twice and that its
   home is `shared/auth`, beside `requireAuth`. Put it there now (`shared/auth/signedIn.ts`,
   exported) and use it in the lookups controllers only. Do not touch the `users` or `space-links`
   controllers (out of scope); add a one-line *Progress* note to finding 25 saying the shared helper
   exists and the two old copies remain.

C. **The audit writer is wired by the composition root.** A dependency that only tests ever pass
   breaks the owner's rule, so `app.ts` passes `audit: writeAudit` (and `runInTransaction`)
   explicitly to the three services, as it does for `users`. Tests pass their fakes the same way.

D. **The rebase rule changed (the owner, today).** At `open-pr`: do not rebase on `main` by default.
   Fetch and push; rebase only if GitHub shows the PR in conflict (`DIRTY`). If it is `CLEAN` and CI
   ran after main's last change, leave it ready for review. (workflow.md §9 still says otherwise; a
   later docs item corrects it. Don't edit it here.)

Everything else stands: the design, the files, the audit names and payloads, the locking, the key
rule, the schemas, the tests, the documents, the shared-file declarations. Checks: lint and
typecheck per commit; the full lanes once on the head, one at a time. Report once CI is green.
