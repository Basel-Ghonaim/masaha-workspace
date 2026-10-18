# Review — PR #86, HARDEN (independent reviewer)

**Head:** `e2a34570a03172cfb42cf285898335ceae390e15` · **Base:** `93f152fe` · **Reviewer:** OpenCode · **Date:** 2026-10-17

## Verdict

Pass — no blocker found; the PR meets its acceptance criteria as implemented, with five minor observations below (none needs a fix round before merge).

## The five most important findings

1. **`waitingOnLock` counts any waiting backend of the test database** — `apps/api/test/locks.ts:34-46`. A run whose intended request never reaches its lock can still pass once `count` is satisfied by an unrelated waiter, and a request that takes longer than `REACH_MS` (4 s) fails on a slow machine (the default test timeout is 5 s). **Severity: nit (plausible).** **Fix:** pass `on` (the relation) in every call, or make the helper take the lock target and the expected count's relation; raise `REACH_MS`/the test timeout for the bcrypt-bearing races. **Where its fix belongs:** a finding to record / a later hardening round, not this PR.

2. **A1's transaction proof is conditional on an unstated invariant** — `apps/api/src/modules/spaces/space/space.service.ts:95-100` (the `get` path). It holds only because nothing between `lockShared` and `namesFor` reads `users` (verified: `linksUnder`, `readFacts`, `findOwnerLinks` do not). A future edit that reads `users` there would make `namesWaiter === readWaiter` pass for the wrong reason. **Severity: nit.** **Fix:** keep the comment in `space.service.ts` and the assumption note in the test; enforce with a grep/contract check when the module changes. **Where its fix belongs:** a finding to record.

3. **`users.namesFor` keeps an optional `tx`, so the required-`tx` rule stops at `ownersFor`** — `apps/api/src/modules/users/users.service.ts:372` and `users.repository.ts:78`. `ownersFor(spaceId, tx)` is required, but its callee can still be called without a transaction, so the "no second connection" rule is not enforced at the reader. **Severity: nit.** **Fix:** make `namesFor(ids, tx)` required (internal callers are `ownersFor` and the transaction-less `list`, which would pass `undefined` deliberately — so keep the default at the repository, but type the service's parameter as `Tx | undefined` and document why). **Where its fix belongs:** a finding to record.

4. **T2's guest break is a combined break, not the boundary alone** — `apps/api/src/modules/spaces/manage.api.test.ts` (T2). `requireAuth()` is mounted before `requireSpaceAccess` on `/manage/spaces/:spaceId`, so the boundary's optional-caller branch cannot be exercised by a single break; the suite records the combined break (drop `requireAuth` plus make the boundary optional) as the substitute. **Severity: nit.** **Fix:** none required — the property is proven by the diagnostic break; record that the suite's break differs from the plan's. **Where its fix belongs:** recorded in the report (departure 1).

5. **D2 has no failing test** — `apps/api/src/modules/spaces/facts/groupEdit.ts:85-88` and `:105`, `space.service.ts:98-99`. S5's warning guard stayed green on `origin/main`'s `Promise.all` (the adapter queued the two statements), so per S5 it was deleted; the rule stands on `conventions.md` §8 and `facts.ts`'s comment only. **Severity: nit (known, accepted).** **Fix:** none — D2 is kept on the documented rule. **Where its fix belongs:** recorded in the report (departure 4).

## Checked and fine

- **Security:** `requireSpaceAccess` decides solely through `can(actor, 'space.read', { links })` and answers 404 (`spaceAccess.ts:10-18`); `signedIn` runs before the loader; `requireCan` stands before `limitRequests`, `validate` and `receiveFile` on upload/order/removal (`photos.manage.routes.ts:20-33`); fact/profile writes are decided by the service's own `can()` under the lock, so an invalid body still answers 422 before 403 (by design); no admin-only route is mounted under `/manage` (`app.ts:340-361`); the services still decide through `can()` under the lock (`groupEdit.ts:78`, `photos.service.ts:62`).
- **Transaction:** `ownersFor(spaceId, tx)` is required in `adminSpaces.service.ts`, both dependency types and both `app.ts` wirings; `namesFor(..., tx)` is passed in `ownersFor`; the three `Promise.all` sites in `space.service.ts` and `groupEdit.ts` are sequential; `adminSpaces.list` is the only remaining `Promise.all` and runs outside any transaction.
- **Race helper:** query matches the plan (`datname = current_database()`, `wait_event_type = 'Lock'`, polled on `prisma`; `on` uses `pg_locks ... NOT granted ... to_regclass`); `whileHeld` waits on it; converted sites use `waitingOnLock()` / `waitingOnLock({ count: 2 })` with no fixed waits (`git grep` finds only the timer port and the helper's own 20 ms poll); A1 and T4 prove a race that never interleaves now fails.
- **A1:** deterministic as written and goes red when `tx` is dropped (verified three runs each way); the backend-id comparison is `toBe`.
- **Tests:** T1–T6, U1, U2, A1, A2 present; each break was run and recorded; `spaceAccess.unit.test.ts` is a pure middleware unit test (no database, no express app); the managed read's payload is asserted for both audiences.
- **Documents:** the no-hint 404 rule lives only in `security.md` and the others link it; `conventions.md` header lists `requireSpaceAccess` and `requireCan`, `optionalAuth` alone under "Not yet built", and §2's route chain matches the code; finding 52 is Resolved and moved in the index; finding 59 keeps Status Open with a dated line; D5 is recorded in `spaces.md`; the code map is a folder/entry-point enumeration, not a file list; `v1-mvp.md`'s row uses `:group`; `testing.md` rule 7 carries S6's sentence; `#82`/`#83`/`#86` appear on their lines.
- **Commits:** six, subjects 44–49 characters, each a complete unit (lint + typecheck at every commit via rebase -x); no schema, migration or dependency; nothing in `apps/web` or `packages/shared`.
- **CI:** lint, typecheck, test:unit, test:api, test:component, build, check:classes, check:links, format:check all pass on `e2a34570`; `mergeStateStatus` is `CLEAN`; the real run on 3321 matched every expected status (owner and reception both 200 with identical bodies; reception's uploads 403 with 0 rate-limit rows; admin and stranger 404; `/abc` 404; no token 401).

## Stop

No further action requested by this review.