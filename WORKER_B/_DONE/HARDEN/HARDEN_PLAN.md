# HARDEN — the spaces API after #82 and #83: the owners' names in the transaction, one access rule, the missing tests, the race helper

> **The owner's approval — 2026-10-17 (binding).** §13's six decisions are approved as recommended:
> **S1** (no route check on the managed reads), **S2** (A1 by the reading backend's id; finding 71 the
> fallback), **S3** (conventions §2's route chain corrected), **S4** (A2 on `/admin`), **S5** (the
> warning guard, kept only if it goes red), **S6** (the race sentence in testing §3 rule 7). Everything
> else as written. **Executor:** Claude Code, Opus 5.5, effort medium (raise to high only while §12.2's
> first checks fail). **GALLERY (worker A) is in progress** in `C:\Users\basel\masaha` and will likely
> open #85 first: §12.7's number check decides; never run a full lane while worker A runs one.

**Work Item:** HARDEN · **Worker:** B · **Planner:** Claude Code, 2026-10-17, from `origin/main` = `93f152fe`
**Branch:** `fix/space-api-hardening`, cut with `--no-track` from the latest `origin/main`, in `C:\Users\basel\masaha-b`
**Ports / databases:** API 3321, web 5321 (not used) · `masaha_b_dev`, `masaha_b_test` in `masaha-postgres-1`
**Report:** `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\HARDEN_REPORT.md` (UTF-8, written in parts)
**Executor:** any capable coding agent. This plan stands alone: no step depends on a Claude skill (the
appendix is only a map). Where the planner could not be sure something works, the step is written as
**a check the executor makes first, with what to do if it fails** — the planner ran nothing.

Placeholders used below, and nowhere else: `#PRNUM` (the PR's number, replaced just before the push,
§12.7) and `<today>` (the date the line is written, `YYYY-MM-DD`). No other placeholder exists in this
plan.

---

## 1. Summary

Six commits on the API and its documents, no schema, no dependency, nothing in `apps/web` or
`packages/shared`:

1. **One race helper** (`waitingOnLock` in `apps/api/test/locks.ts`): every race test acts once its
   request is seen waiting on a lock, never after a fixed time. Finding 52 resolved.
2. **The owners' names are read inside the read's transaction** (`users.namesFor(…, tx)`, `ownersFor`'s
   `tx` required), and a transaction runs **one statement at a time** (no `Promise.all` on `tx`). A
   test proves which connection reads the names — deterministically, by the backend's id.
3. **The managed boundary decides through `can(actor, 'space.read', { links })`** — no second copy of
   the staff rule. `spaceAccess.api.test.ts` becomes a unit test of its one real case.
4. **`requireCan(action)`** in `shared/auth`: it replaces the routers' inline `space.read` checks and
   stands before the limiter and the body reader on the managed photo writes, so reception is refused
   before its upload is counted or read.
5. **The missing tests:** the managed read's payload for owner and reception; unknown and malformed ids
   and a guest; a hidden space; a link change racing a managed write.
6. **The records:** `#82`/`#83` on their lines, `v1-mvp.md`'s row, the code map, finding 59's dated
   line, and the no-hint 404 rule kept in `security.md` with every other document linking it.

#83's deliberate breaks, never run, are run on the head (D8) and recorded in the report.

## 2. The contract

### Scope

- `apps/api`: `ownersFor` and the single-space read and fact writes (D1, D2); `requireSpaceAccess`
  (D3); `requireCan` and the two manage routers (D4); the race helper and every race test (D7); the
  tests of D6.
- `docs`: `conventions.md`, `security.md`, `api-contract.md`, `features/spaces.md`,
  `features/space-links.md`, `plans/v1-mvp.md`, findings 52 and 59 and the findings index; with S6,
  `development/testing.md`; conditionally `project/overview.md`'s date (§4, D9).

### Acceptance criteria

- [ ] `ownersFor(spaceId, tx: Tx)` reads the names with `tx`; the parameter is required in
      `adminSpaces.service.ts`, `space.service.ts`'s and `groupEdit.ts`'s dependency types and
      `app.ts`'s two wirings.
- [ ] No `Promise.all` runs two statements on one `tx` in `space.service.ts` or `groupEdit.ts`.
- [ ] A test fails when the names are read outside the read's transaction (A1), or finding 71 is
      recorded and the report says why (§4, D6).
- [ ] `requireSpaceAccess` refuses with 404 exactly when `can(actor, 'space.read', { links })` is false;
      it holds no predicate of its own.
- [ ] `requireCan(action)` exists beside `requireRole`, exported from `shared/auth`; the routers hold no
      inline `can()`; on the three managed photo writes it stands before `limitRequests`,
      `validate` and `receiveFile`.
- [ ] Reception's managed photo upload is refused 403 before it is counted or read (T5).
- [ ] The tests T1–T6, U1, U2, A1 exist, each seen failing (§9), each break recorded.
- [ ] Every race test waits through `waitingOnLock`; no race test waits a fixed time. Finding 52 is
      Resolved, with its dated line and `#PRNUM`.
- [ ] D8's breaks are made once each on the head, seen red, restored, and recorded with their output.
- [ ] D9's documents: the 404 rule's one home is `security.md`; every edited document's *Last Updated*
      is `<today>`; `#82`/`#83` on their lines; `v1-mvp.md`'s row; the code map; finding 59's line.
- [ ] D5 recorded as a decision in `docs/features/spaces.md`.
- [ ] `lint`, `typecheck` (each commit), `test:unit`, `test:api`, `format:check`, `check:links` pass on
      the head; a real run on 3321; CI green and `CLEAN`.

### Out of scope

- R015 (a report outside the repository: D8 replaces its missing evidence).
- Anything in `apps/web` or `packages/shared`; packages, staff, capacity (step 5b and later).
- Finding 69 (worker A records it); the deleted-spaces item's (#84's) lines (GALLERY's commit 0).
- The admin's own photo routes' order (a trusted account; §10, Review Focus), except S4's test.
- Any schema change, migration or dependency.

## 3. The reading done

From `origin/main` (`93f152fe`): `CLAUDE.md`; `docs/development/workflow.md`; `docs/development/testing.md`;
`docs/backend/conventions.md` (header, §1, §2, §7–§8, §13); `docs/backend/security.md` (header,
Authorization, Rate limits, HTTP hardening); `docs/api/api-contract.md` (Managed spaces, Spaces (the
admin) › Photos, Owners (the admin), the auth endpoints); `docs/features/spaces.md`;
`docs/features/space-links.md`; `docs/architecture/documentation.md`; ADR 0002, ADR 0009; findings 11,
43, 52, 59 and the index; `docs/plans/v1-mvp.md` (the managed rows; and the pre-#83 row at `1efe2b8a`);
`docs/project/overview.md`'s header and Spaces line; `docs/README.md`'s deferred documents.

Code: `shared/auth/{spaceAccess,spaceLinks,can,index,requireRole,signedIn}.ts`,
`requireRole.unit.test.ts`, `spaceLinks.unit.test.ts`, `spaceAccess.api.test.ts`;
`modules/spaces/{spaces.manage.routes,photos.manage.routes,spaces.admin.routes,spaces.limits,index}.ts`,
`facts/{groupEdit,facts}.ts`, `confirm/confirm.service.ts`, `space/space.service.ts`,
`photos/{photos.controller,photos.service}.ts` (upload, `lockFor`), `spaces.repository.ts`
(`findSummaries`); `space-links/admin-spaces/adminSpaces.service.ts`, `space-links.repository.ts`,
`space-links.service.ts` (`linksAt`); `users.repository.ts` (`findNames`); `db/{prisma,transaction}.ts`;
`app.ts` (composition, mounts); `shared/http/receiveFile.ts`; `shared/rate-limit/{limiter,counter}.ts`;
the `RateLimit` model; `packages/shared/src/spaces/responses.ts` (`AdminSpace`); `vitest.config.ts`.
Tests: `manage.api.test.ts`; `space/space.api.test.ts` (matrix, finding-43 test, owners tests);
`space/createWithoutNestedWrites.api.test.ts`; `test/{locks,spaces,admin,factories}.ts`;
`auth/sessionLock.api.test.ts` (its helper and inline wait); the fixed waits in
`admin-owners/adminOwners.api.test.ts`, `hours/hours.api.test.ts`, `prices/prices.api.test.ts`;
`photos/photosRace.api.test.ts`; the `whileHeld` users found by `git grep`.

Outside the repository: the prompt; `REVIEW82-83_OPENCODE_REPORT.md` (whole); `OWNERSREAD_PLAN.md` and
`MANAGE_PLAN.md` (planned tests and breaks); worker A's `GALLERY_PLAN.md` §7 and §14 (its files).
`gh pr list --state open` was empty on 2026-10-17; the latest issue/PR number was 84.

## 4. The prompt's settled decisions, as they will be built

### D1 — the owners' names inside the transaction (R001, R009)

- `apps/api/src/modules/space-links/admin-spaces/adminSpaces.service.ts`, `ownersFor`:
  signature `async ownersFor(spaceId: number, tx: Tx): Promise<{ id: number; name: string }[]>`;
  the names line becomes
  `const names = await users.namesFor([...new Set(links.map(({ userId }) => userId))], tx);`.
  Its doc comment: "Read with the caller's transaction, so under its lock and on its connection."
  *Reason:* without `tx` the names leave the transaction and take a second pool connection.
- `space/space.service.ts` and `facts/groupEdit.ts`: the dependency type becomes
  `ownersFor: (spaceId: number, tx: Tx) => Promise<AdminSpace['owners']>;` (required `tx`).
  *Reason:* the next caller cannot leave it out.
- `apps/api/src/app.ts`, both wirings: `ownersFor: (spaceId: number, tx: Tx) => adminSpaces.ownersFor(spaceId, tx),`.
- `adminSpaces.service.ts`'s `list` is unchanged (no transaction there).
- `docs/features/space-links.md`'s sentence becomes true; reworded in C2 (§11).

### D2 — one statement at a time on a transaction (R002)

In `space.service.ts` `get` and in both places of `groupEdit.ts` (`if (!change)` and the end):

```ts
// One statement at a time: a transaction's connection runs one at once (finding 11).
const facts = await readFacts(space.id, tx);
const owners = await ownersFor(space.id, tx);
```

*Reason:* conventions §8 *Transactions* and `facts.ts`'s own comment. Its test: S5 (conditional).

### D3 — the boundary decides through `can()` (R003)

`apps/api/src/shared/auth/spaceAccess.ts`, whole body:

```ts
/**
 * The managed-space boundary (docs/backend/security.md › Authorization): it loads the space's links
 * and admits only a caller `can()` allows to read the space; anyone else is told it does not exist.
 */
export function requireSpaceAccess(loader: LinksLoader): RequestHandler {
  return async (req, _res, next) => {
    const id = parseId(req.params.spaceId);
    const { userId, role } = signedIn(req);
    const links = await loader(id);
    if (!can({ id: userId, role }, 'space.read', { links })) throw AppError.notFound();
    req.space = { id, links, linksUnder: (tx) => loader(id, tx) };
    next();
  };
}
```

Imports: `can` from `./can.ts`; drop the `LoadedSpace` type import if unused. *Reason:* one home for
the staff rule (`roleAt` in `can.ts`); a future role cannot make the boundary and the service
disagree. `signedIn` moves before the loader: a request without claims is refused before any query.
**No behaviour changes today** (the two predicates are equal while `SpaceManagerRole` is
`OWNER | RECEPTION`), so no test can fail for D3; the existing matrix staying green is its evidence.

### D4 — one `requireCan(action)` middleware (R006, R007)

New `apps/api/src/shared/auth/requireCan.ts`:

```ts
import type { RequestHandler } from 'express';

import { AppError } from '../errors/index.ts';
import { can, type SpaceAction } from './can.ts';
import { signedIn } from './signedIn.ts';
import { spaceOf } from './spaceLinks.ts';

/**
 * The guard of one action on the route's space, mounted after the space's links are loaded: 403
 * when can() refuses it (docs/backend/security.md › Authorization). It refuses before the request's
 * body is read or counted; the service's own can(), under the space's lock, still decides.
 */
export function requireCan(action: SpaceAction): RequestHandler {
  return (req, _res, next) => {
    const { userId, role } = signedIn(req);
    if (!can({ id: userId, role }, action, spaceOf(req))) throw AppError.forbidden();
    next();
  };
}
```

- `shared/auth/index.ts`: `export { requireCan } from './requireCan.ts';` (beside `requireRole`).
- `modules/spaces/spaces.manage.routes.ts`: `router.get('/', requireCan('space.read'), space.get);`;
  drop the `can`, `signedIn`, `spaceOf`, `AppError` imports it no longer uses.
- `modules/spaces/photos.manage.routes.ts`:

  ```ts
  const mayManagePhotos = requireCan('space.photos.manage');
  router.get('/', requireCan('space.read'), photos.list);
  router.post(
    '/',
    mayManagePhotos,
    limitRequests(limiter, (req) =>
      Promise.resolve({ policy: PHOTO_UPLOAD, by: [String(signedIn(req).userId)] }),
    ),
    receiveFile('photo', PHOTO_MAX_BYTES),
    photos.upload,
  );
  router.put('/order', mayManagePhotos, validate(photoOrderSchema), photos.reorder);
  router.delete('/:photoId', mayManagePhotos, photos.remove);
  ```

  "The managed photo writes" are read as all three (upload, order, removal): each is refused before
  its body is read. The services' own `can()` (cheap, then under the lock) stays authoritative.
- **With S1 approved** (§5), the two `GET`s carry no `requireCan('space.read')`:
  `router.get('/', space.get)` and `router.get('/', photos.list)`.
- **Executor check, first:** `npm run typecheck` accepts `can({…}, action, spaceOf(req))` with
  `action: SpaceAction` (a union, as `groupEdit.ts` already passes one). *If it refuses:* make the
  function generic, `requireCan<A extends SpaceAction>(action: A)`; if that is refused too, stop and ask
  (no cast).

### D5 — reception receives the owners' names and ids, as built (review D-a, option A)

No code. An API decision in `docs/features/spaces.md` (C5, text in §11). Proven by T1.

### D6 — the missing tests

All written in §9: T1 (payload, owner and reception), T2 (unknown, malformed, guest), T3 (hidden),
T4 (a link change racing a managed write, on D7's helper), T5 (reception refused before the read),
T6 (the limit before the file is read), U1 (`requireCan`), U2 (`spaceAccess.unit.test.ts`, the
transaction-identity case only; `spaceAccess.api.test.ts` is deleted), A1 (the names' transaction).

**The names' test — the review's form cannot fail.** Renaming the owner inside the holder transaction
and expecting the committed name proves nothing: the read waits for the holder's lock, so its names
query starts after the commit, and under read committed a statement started after a commit sees it,
on `tx` or on any other connection. The one observable difference is **which connection** reads the
names. A1 (§9) observes it deterministically: it holds the users table in a second test transaction
and checks that the backend waiting for it is the one that waited for the space's lock. This is S2.
**If A1 cannot be made red deterministically** (§12.2, check 3), A1 is not kept and **finding 71** is
recorded instead (text in §6), and the report says so.

### D7 — one race helper (finding 52)

`apps/api/test/locks.ts` — remove `WAIT_MS`; add:

```ts
/** How long a request may take to reach the lock it waits on, bcrypt included; under Vitest's 5 s. */
const REACH_MS = 4_000;
const POLL_MS = 20;

/**
 * Waits until `count` backends of the test database wait on a lock — the requests a race test
 * started, blocked on what its transaction holds — and answers their process ids, smallest first.
 * With `on`, only those waiting for that table's lock. Fails after REACH_MS, so a race whose request
 * never reached the lock fails instead of passing without interleaving (finding 52).
 */
export async function waitingOnLock({ count = 1, on }: { count?: number; on?: string } = {}): Promise<number[]>
```

- Without `on`: `SELECT pid FROM pg_stat_activity WHERE datname = current_database() AND
  wait_event_type = 'Lock' ORDER BY pid`, polled on the default `prisma` client (each poll its own
  statement, so its own statistics snapshot); returns when at least `count` rows; else waits `POLL_MS`;
  after `REACH_MS` throws `new Error(\`${count} request(s) never waited on a lock\`)`.
  `datname = current_database()` keeps worker A's tests, on `masaha_test` in the same container, out.
- With `on` (added in **C2**, with its one user, A1 — never before): `SELECT pid FROM pg_locks WHERE
  NOT granted AND relation = to_regclass(${on}) ORDER BY pid`.
- `whileHeld`: `await new Promise(…WAIT_MS)` becomes `await waitingOnLock();`. Signature unchanged;
  its transaction keeps `{ timeout: 10_000 }`; its comment says it waits until the request waits.
- `apps/api/src/modules/auth/sessionLock.api.test.ts`: delete its `WAIT_MS`; `whileLocked` keeps its
  name and signature and becomes `return whileHeld((tx) => lockUsers(tx, userId), call, meanwhile);`
  (`lockUsers` takes the row `FOR UPDATE`, as its raw query did). The inline test (*"answers
  RESET_TOKEN_INVALID, not a 500, when the link ends while the check binds it"*) replaces its
  `setTimeout(WAIT_MS)` with `await waitingOnLock();`.
- Every other race test's fixed wait becomes `await waitingOnLock()`:
  - `space-links/admin-owners/adminOwners.api.test.ts`: delete `aWhile`; its three calls →
    `await waitingOnLock()`, except *"makes a person a user again when their two links end at once"*,
    which starts two requests → `await waitingOnLock({ count: 2 })`; *"refuses an email another
    creation took while this one waited for the space"* → `await waitingOnLock()` (its comment: the
    add's read of the email and its hash are done once it waits for the space).
  - `spaces/hours/hours.api.test.ts` (*"refuses the admin when an owner joined while the save waited
    for the space's lock (finding 43)"*), `spaces/prices/prices.api.test.ts` (*"waits for the
    space's lock, then checks the shifts as they are…"*), `spaces/space/space.api.test.ts` (*"waits
    for a change in progress and answers it whole…"*).
  - The `whileHeld` users (`directory/page`, `admin-roles/adminRoles`, `photos/photosRace`,
    `users/issueTemporaryPassword`, `users/suspension`) change nothing: they run through `whileHeld`.
- Docs: finding 52 Resolved; the index moves it (C1, §11); with S6, `testing.md`'s rule 7.

### D8 — #83's deliberate breaks, run now

Made once each on the head, seen red, restored from a backup copy (§12.5), recorded with their output:

| # | Property | The break (one edit) | Run | Must go red |
|---|---|---|---|---|
| 8.1 | Reception refused on every write | `can.ts`: `'space.facts.update': 'staff'` | `manage.api.test.ts`, `can.unit.test.ts` | *lets reception read photos but refuses every mutation* (the fact `PUT`s and their confirms), and `can.unit`'s table |
| 8.2 | the same | `can.ts`: `'space.profile.update': 'staff'` | the same | the `PATCH` and the profile's confirm |
| 8.3 | the same | `can.ts`: `'space.photos.manage': 'staff'` | the same | the photo writes; T5 |
| 8.4 | No link → 404 | `spaceAccess.ts`: delete the `if (!can(…)) throw AppError.notFound();` line | `manage.api.test.ts` | *refuses every protected route for strangers, unrelated owners and unlinked admins* (reads answer 200, writes 403); *does not admit a deactivated link or a deleted space* |
| 8.5 | The admin refused on `/manage` | `spaceAccess.ts`: `if (role !== 'ADMIN' && !can(…))` | `manage.api.test.ts` | the admin's cases in the same test |
| 8.6 | The lock-aware decision | `groupEdit.ts`: `const locked = { links: space.links };` | `manage.api.test.ts`, `hours.api.test.ts` | T4; hours' finding-43 test |
| 8.7 | the same, for photos | `photos.service.ts` `lockFor`: `can(actor, 'space.photos.manage', space)` | `photosRace.api.test.ts` | *decides on the links under the space's lock: an owner linked meanwhile refuses the admin* |

### D9 — the documents (R004, R005, R008, R010, R011, R016, R017)

All texts in §11. Two readings to state:

- **R011 — *Last Updated*:** every document this item edits gets `<today>`. `docs/project/overview.md`
  is not otherwise edited here; GALLERY edits its *Built* line in parallel, which moves its date.
  **Executor check at C6:** if no open PR edits `docs/project/overview.md` and its header still reads
  `2026-10-14`, set it to `2026-10-15` (the date #83 and #84 changed it); otherwise leave it, and say
  which in the report. *Reason:* a date-only edit would add a header conflict for nothing.
- **History lines** keep the documents' own form, `- #NN — …` (documentation §5: *History*, the PRs);
  decision lines end `<date>, #NN.`.

## 5. Stronger decisions

Each is a proposal; nothing here is built unless the owner's reply approves it. The default build is
the prompt's decisions as written (§4).

### S1 — the managed reads carry no route check of their own

- **What:** drop `requireCan('space.read')` from the two managed `GET`s; the boundary (D3) is that
  decision.
- **Why:** after D3, `requireSpaceAccess` admits a caller exactly when `can(…, 'space.read', …)` is
  true, on the same links. A second `requireCan('space.read')` behind it can never refuse — R006's
  "dead code that proves nothing, written twice", moved rather than removed — and no test can fail
  for it (testing §3 rule 6: every test names its break; this check has none).
- **Cost:** the routers no longer name the read action; the boundary names it, once.
- **Recommendation:** adopt. D4's other half (the photo writes) is unchanged.

### S2 — A1 in the form that can fail

- **What:** A1 proves the names' transaction by the reading backend's id (§9), not by a renamed owner.
- **Why:** the review's form cannot fail under read committed (§4, D6); the owner's fallback (finding
  71) is then needed only if this form also fails to be deterministic.
- **Cost:** an intricate test (two test transactions, `LOCK TABLE users`), and the helper's `on`
  option for it.
- **Recommendation:** adopt; finding 71 stays the fallback, as the owner settled.

### S3 — `conventions.md` §2's route chain, corrected (a rule the item would otherwise contradict)

- **What:** §2 *Layers › Routes* says the chain is "rate limiter → auth guard → role guard →
  `validate(schema)` → controller". D4 puts `requireCan` **before** the photo limiter — as `/admin`'s
  guards already stand before its photo limiter (they are mounted on the prefix). Reword the cell's
  first sentence to (rest of the cell unchanged):
  "The per-endpoint chain: auth guard → role or space guard (`requireRole`, `requireSpaceAccess`) →
  permission guard (`requireCan`) → rate limiter → `validate(schema)` or the file reader →
  controller; a route with no signed-in caller starts at its limiter, and the general limit runs
  before every route. A guard refuses before anything of the request's body is read."
- **Why:** a per-user limit needs its caller, so it can only follow the guards; the chain as written is
  true for no route that has a guard and a limit.
- **Cost:** one cell of a platform contract.
- **Recommendation:** adopt. **If not approved:** §2 is left as it is and finding **75** is recorded:
  "conventions §2's route chain puts the rate limiter before the guards", evidence
  `spaces.admin.routes.ts` and `photos.manage.routes.ts`, *resolves when* §2 states the order the
  routes follow.

### S4 — the limit's order also proven on `/admin`

- **What:** A2 (§9) in `photos/photos.api.test.ts`, T6's shape on the admin's upload.
- **Why:** `spaces.admin.routes.ts` holds its own `limitRequests → receiveFile` order; swapping it
  there fails no test today, and T6 cannot see it (the review: "on either audience").
- **Cost:** one test, one file.
- **Recommendation:** adopt.

### S5 — a guard for D2, if it can fail

- **What:** a file of its own, `apps/api/src/modules/spaces/space/readOneStatementAtATime.api.test.ts`,
  modelled on `createWithoutNestedWrites.api.test.ts`: a `process.on('warning')` listener at the top;
  the process's first `GET /admin/spaces/:spaceId` of a space with an owner, then a `PUT …/contacts`
  that changes nothing and one that changes the group (both `groupEdit` paths); title *"reads a space
  and saves a group with one statement at a time on its transaction"*; expects no warning whose
  message includes `already executing a query`.
- **Executor check, first (before D2's code):** run it on `origin/main`'s `Promise.all`. *If red:* keep
  it, D2 makes it green. *If green:* delete the file, and the report says D2 has no failing test
  because the adapter queued the two statements (as finding 11's probe found); D2 stands on
  conventions §8's rule.
- **Cost:** one file, one check.
- **Recommendation:** adopt.

### S6 — the race rule written where tests are ruled

- **What:** `docs/development/testing.md` §3 rule 7 gains one sentence: "A race's test acts only once
  its request is seen waiting on the lock (`apps/api/test/locks.ts`), never after a fixed time."
- **Why:** otherwise the rule lives only in a resolved finding and a helper's comment, and the next
  race test may copy a fixed wait again.
- **Cost:** one line in an authoritative document (its *Last Updated* moves).
- **Recommendation:** adopt.

### Rules the item touches, stated

- **Workflow phase 4** asks every lane, `build` and `check:build`; the prompt lists `lint`,
  `typecheck`, `test:unit`, `test:api`, `format:check`, `check:links`. The prompt is followed (CLAUDE.md
  precedence 1); `test:component`, `build`, `check:build`, `check:classes` are not run, because no
  file in `apps/web` or `packages/shared` changes; CI runs them. Said in the report and the PR.
- **Documentation §1, records:** a finding changes by its status and a dated resolution. Finding 59's
  dated line (R017) records progress without a status change; it is dated, so it reads "as of that
  date". Kept as the owner decided.

## 6. Related findings

- **52 — the race tests wait a fixed time:** **folded** (D7). Resolved in C1. Cost: six test files.
- **59 — the verified space's editor cannot name its owner:** one dated line (D9, R017); stays Open.
- **11 — nested writes / one statement at a time:** not changed (Resolved). D2 applies its rule; S5 may
  add its second guard.
- **43 — two races around a space's facts:** not changed (Resolved). T4 extends its proof to `/manage`.
- **63 — a photo's files can outlive it:** not related (the upload's work after `requireCan` is
  unchanged).
- **17, 21, 23** (sweeps, token grace, per-address ceiling): not related.
- **69** is worker A's (GALLERY's commit 0); **73–74** GALLERY's.
- **New, only if needed:** **71** — only if A1 cannot be made red (§4, D6):
  `docs/architecture/findings/71-the-owners-names-transaction-has-no-failing-test.md`, title
  "71. The owners' names' transaction has no test that can fail", Status Open, Date `<today>`,
  Evidence: D1 reads the names with `tx`; under read committed a rename cannot tell `tx` from another
  connection; the backend-id form of A1 was tried and (the observed result); Resolves when: a test
  fails when `namesFor` loses `tx`. Index under *Open*. **75** — only if S3 is not approved (§5).
  **72 and 76** are not used.

## 7. The files it edits

No licence in another layer. **28 files** by default (+1–2 conditional; +3 with S4–S6; at most 33):

| # | Path | Commit | What |
|---|---|---|---|
| 1 | `apps/api/test/locks.ts` | C1, C2 | `waitingOnLock`; `whileHeld` uses it; `on` in C2 |
| 2 | `apps/api/src/modules/auth/sessionLock.api.test.ts` | C1 | D7 |
| 3 | `apps/api/src/modules/space-links/admin-owners/adminOwners.api.test.ts` | C1 | D7 |
| 4 | `apps/api/src/modules/spaces/hours/hours.api.test.ts` | C1 | D7 |
| 5 | `apps/api/src/modules/spaces/prices/prices.api.test.ts` | C1 | D7 |
| 6 | `apps/api/src/modules/spaces/space/space.api.test.ts` | C1, C2 | D7's wait; A1 |
| 7 | `docs/architecture/findings/52-the-race-tests-wait-a-fixed-time.md` | C1 | Resolved |
| 8 | `docs/architecture/findings/README.md` | C1 (C2 if 71) | 52 moved; 71 if recorded |
| 9 | `apps/api/src/modules/space-links/admin-spaces/adminSpaces.service.ts` | C2 | D1 |
| 10 | `apps/api/src/modules/spaces/space/space.service.ts` | C2 | D1 type, D2 |
| 11 | `apps/api/src/modules/spaces/facts/groupEdit.ts` | C2 | D1 type, D2 |
| 12 | `apps/api/src/app.ts` | C2 | D1 wiring types |
| 13 | `docs/features/space-links.md` | C2, C3, C6 | §11 |
| 14 | `docs/features/spaces.md` | C2, C3, C4, C5, C6 | §11 |
| 15 | `apps/api/src/shared/auth/spaceAccess.ts` | C3 | D3 |
| 16 | `apps/api/src/shared/auth/spaceAccess.api.test.ts` | C3 | deleted (`git mv` to 17) |
| 17 | `apps/api/src/shared/auth/spaceAccess.unit.test.ts` | C3 | U2 |
| 18 | `docs/backend/security.md` | C3, C4 | §11 |
| 19 | `docs/backend/conventions.md` | C3, C4 | §11 |
| 20 | `docs/api/api-contract.md` | C3, C4 | §11 |
| 21 | `apps/api/src/shared/auth/requireCan.ts` | C4 | new, D4 |
| 22 | `apps/api/src/shared/auth/requireCan.unit.test.ts` | C4 | U1 |
| 23 | `apps/api/src/shared/auth/index.ts` | C4 | export |
| 24 | `apps/api/src/modules/spaces/spaces.manage.routes.ts` | C4 | D4 |
| 25 | `apps/api/src/modules/spaces/photos.manage.routes.ts` | C4 | D4 |
| 26 | `apps/api/src/modules/spaces/manage.api.test.ts` | C4, C5 | T5, T6; T1–T4 |
| 27 | `docs/plans/v1-mvp.md` | C6 | R005 |
| 28 | `docs/architecture/findings/59-the-verified-spaces-editor-cannot-name-its-owner.md` | C6 | R017 |
| c | `docs/project/overview.md` | C6 | date only, conditional (§4, D9) |
| c | `docs/architecture/findings/71-the-owners-names-transaction-has-no-failing-test.md` | C2 | only if A1 fails |
| S4 | `apps/api/src/modules/spaces/photos/photos.api.test.ts` | C4 | A2 |
| S5 | `apps/api/src/modules/spaces/space/readOneStatementAtATime.api.test.ts` | C2 | conditional |
| S6 | `docs/development/testing.md` | C1 | rule 7's sentence |

**Shared with another open item — GALLERY (worker A, expected open as #85; its plan names nothing in
`apps/api` or `packages/shared`):**

- `docs/features/spaces.md` — HARDEN owns: the header's date; *How it composes* (the managed routers'
  bullet); *Behaviour › Photos*' upload line; the *API decisions* lines 159 and two appended; *Code
  map › API*; *API history*. GALLERY owns the *Web* parts, *Open findings*, and its commit 0's lines
  (the "stale only" wording, the delete dialog's and the restore's decisions, #84's lines).
- `docs/features/space-links.md` — HARDEN: the header's date; *How it composes* (managed routes, the
  single-space read); *API decisions* line 105; *API history*. GALLERY's commit 0: the list's lines
  67 and 72, *Open findings*, *Web decisions*, #84's lines.
- `docs/architecture/findings/README.md` — HARDEN: 52 to *Resolved* (and 71 if any); GALLERY: 69,
  70, 73, 74 under *Open*.
- `docs/project/overview.md` — only conditionally (§4, D9).

A conflict in these is documents-only: the fast path (workflow §9, *Conflicts*). **The PR number:**
GALLERY's plan writes `#85`; whichever PR opens first takes it. This plan never assumes a number
(§12.7); the report states the number taken and that GALLERY's plan assumed 85.

## 8. Design issues

None: this item builds or changes no screen.

## 9. Tests — lane, title, the break each catches

Every test is seen failing first (testing §3 rules 5–7): a new behaviour's test before its code; a test
of existing code by making its break once. **Every red run's output goes into the report.**

### Unit lane (`npm run test:unit`)

**U1 — `apps/api/src/shared/auth/requireCan.unit.test.ts`** (C4), modelled on `requireRole.unit.test.ts`
(the guard called directly with `{ auth, space } as unknown as Request`; no network):
- *lets the caller through when can() allows the action on the route's space* — an `OWNER` link of
  user 7 on a verified space, `space.photos.manage` → `next` once.
- *answers 403 when can() refuses the action: reception may not manage photos* — a `RECEPTION` link →
  `{ type: 'forbidden', code: undefined }`, `next` not called.
- *answers 401 when no claims are on the request* → `unauthorized`.
- *answers 404 when no space was loaded for the route* → `not_found` (`spaceOf`).
- **Seen failing:** write the file with `requireCan` as a stub that calls `next()` → the 403 case red;
  then the real body. **Break:** `next()` before the check → red.

**U2 — `apps/api/src/shared/auth/spaceAccess.unit.test.ts`** (C3; `git mv` from `spaceAccess.api.test.ts`,
rewritten in `spaceLinks.unit.test.ts`'s style — the middleware called directly, no express app, no
supertest):
- *reads the space's links again with the transaction it is given* — a loader that records
  `{ id, tx }` and answers an active `OWNER` link of the signed-in user 7; after
  `spaceOf(req).linksUnder(tx)`: `asked` equals `[{ id: 12, tx: undefined }, { id: 12, tx }]` and
  `asked[1].tx` is the same object (`toBe`).
- **Break:** `linksUnder: () => loader(id)` → red. The two old cases (accept; 404 for a deactivated
  link) are dropped: `manage.api.test.ts` proves them on the real path (testing §1).

### API lane (`npm run test:api`)

All in `apps/api/src/modules/spaces/manage.api.test.ts` unless named; its `beforeEach`, `manage()`
helper and callers as they are.

**T1** (C5) *answers the owner and reception the same whole space: its facts, its verification and its
owners*
- Setup: seven open days as `space.api.test.ts`'s finding-43 test seeds them
  (`spaceHours.createMany`, 480–1080), and `hoursUpdatedAt: new Date()` on the space.
- Owner `GET` → 200; `dataOf` `toMatchObject` by hand: `id: spaceId`, `isVerified: true`,
  `isHidden: false`, `owners: [{ id: owner.id, name: 'Ahmad' }]`, `hours: { days: 7 × { opensMinute:
  480, closesMinute: 1080 }, shifts: [] }`, `prices: []`, `amenityIds: []`, `ownAmenities: []`,
  `contacts: []`, `staleGroups: []`, `missingGroups: ['prices', 'amenities', 'contacts']`.
- Reception `GET` → 200, and `expect(dataOf(receptionRead)).toEqual(dataOf(ownerRead))`.
- **Executor check:** if `createSpace()` leaves the profile undated, `missingGroups` gains `'profile'`;
  write what the model gives, by hand.
- **Breaks:** `ownersFor` answering `[]` → red; a read without the facts → red.

**T2** (C5) *answers not_found for an unknown or malformed space id, and 401 to a guest*
- Owner `GET /api/v1/manage/spaces/999999`, `/abc`, `/2147483648` → each 404 `not_found`.
- No `Authorization`: `GET /api/v1/manage/spaces/<spaceId>` → 401 `unauthorized`.
- **Breaks:** `Number(req.params.spaceId)` for `parseId` in `spaceAccess.ts` → `abc` and `2147483648`
  answer 500 → red; the boundary reading the caller as optional and refusing a guest with its 404
  (`const actor = req.auth; if (!actor || !can(…)) throw notFound()`) → red.

**T3** (C5) *keeps a hidden space open to its owner and reception*
- `isHidden: true` on the space; owner `GET` → 200 with `isHidden: true`; owner `PATCH { nameEn:
  'Branch Hub' }` → 200; reception `GET` and `GET /photos` → 200.
- **Break:** `findSummaries` (`spaces.repository.ts`) filtering `isHidden: false` → 404 → red.

**T4** (C5) *decides a managed save on the links under the space's lock: an owner unlinked meanwhile is
refused*
- `whileHeld(hold the space FOR NO KEY UPDATE, () => manage(owner, 'put', '/contacts', { contacts: [] }),
  (tx) => tx.spaceManager.update({ where: { spaceId_userId: { spaceId, userId: owner.id } }, data:
  { deactivatedAt: new Date() } }))` → 403 `forbidden`; the space's `contactsUpdatedAt` is `null`;
  `auditEntries()` is `[]`.
- **Break:** D8.6 → 200 → red. **Helper break (D7's evidence):** remove the hold from T4 → the
  helper's error "1 request(s) never waited on a lock" → red.

**T5** (C4) *refuses reception's photo writes before reading them, and counts no upload*
- Reception: `POST /photos` with no file → 403 (without D4: 422 `photo: required`);
  `PUT /photos/order` with `{ ids: 'all' }` → 403 (without: 422); `DELETE /photos/abc` → 403 (without:
  404); then `prisma.rateLimit.count({ where: { key: { startsWith: 'photo-upload:' } } })` is 0.
- **Seen failing:** before D4's routers → 422. **Breaks:** `requireCan` after `receiveFile` → 422;
  `requireCan` between `limitRequests` and `receiveFile` → the count is 1; `requireCan` dropped from
  the order or the removal → 422 / 404.

**T6** (C4) *counts an upload before reading its file: thirty unreadable uploads use the limit, and the
next photo is refused 429*
- Owner, thirty times: `POST /photos` `.attach('other', Buffer.from('x'), 'x.txt')` → 400
  `bad_request` each; then a real JPEG (`image('jpeg')`) → 429 `rate_limit`;
  `prisma.spacePhoto.count()` is 0.
- **Executor check:** the unreadable upload answers 400 (multer's unexpected file); if it answers
  anything else, use a second file under `photo` (also 400 by `receiveFile`'s contract).
- **Seen failing (existing code):** swap `receiveFile` before `limitRequests` in
  `photos.manage.routes.ts` → the thirty are not counted → the photo answers 201 → red.

**A1** (C2) `spaces/space/space.api.test.ts`: *reads the owners' names on the read's own connection,
inside its transaction* (20 s timeout). The sequence — every step waits on an observed lock, never a
time:
1. `const space = await createSpace(); const owner = await link(space.id, 'OWNER');` (committed).
2. Holder A, `prisma.$transaction`: `SELECT id FROM spaces WHERE id = … FOR NO KEY UPDATE`; start
   `pending = adminRequest(app, admin, 'get', path(space.id))`; `[readWaiter] = await
   waitingOnLock()` (the read waits for the space, on its transaction's backend).
3. Still inside A: start holder B, a second `prisma.$transaction` (`timeout: 15_000`) that runs
   `` LOCK TABLE users IN ACCESS EXCLUSIVE MODE ``, then signals "taken" and waits on a promise the
   test resolves later (assign its resolver before signalling). A waits for "taken", then returns
   (commits).
4. `const [namesWaiter] = await waitingOnLock({ on: 'users' });` — the backend waiting for the users
   table: the read, at its names.
5. Release B; `await` B; `const response = await pending;`.
6. Then assert: 200; `owners` `toEqual([{ id: owner.id, name: 'Sara' }])`;
   `expect(namesWaiter).toBe(readWaiter)`.
- Assertions come after B is released, so a red run ends cleanly instead of hanging.
- **Seen failing:** on `origin/main`'s `ownersFor` (no `tx`) → `namesWaiter` is another backend → red;
  green after D1. **Break (D1):** drop `tx` from the `namesFor` call → red.
- Why it is deterministic: the read's first `users` access after the space lock is `namesFor`
  (`linksAt`, `findSummaries`, `findOwnerLinks` and the facts read no `users`); `requireAuth`'s
  `users` read is done before the read waits on the space (step 2 waits for it).

**A2 — with S4** (C4) `spaces/photos/photos.api.test.ts`: *counts an admin's upload before reading its
file: the next photo after thirty unreadable ones is refused 429* — T6's shape on
`/api/v1/admin/spaces/:spaceId/photos` (an unverified space, the admin). Break: swap in
`spaces.admin.routes.ts` → 201 → red.

**S5's guard** — §5.

**The converted race tests (C1)** — evidence: each file green three times running; T4's helper break
(above) shows a race that never interleaves now fails.

### Not testable, and said

- D3 changes nothing observable today (§4). D4's `requireCan('space.read')` on the reads cannot refuse
  (S1). D2 is testable only through S5's warning, if it fires.

## 10. Review Focus — the inputs no planned test exercises

- A third `SpaceManagerRole` (D3's reason): none exists; D3 is structural.
- Reception's fact writes with an invalid body still answer 422 (validation before the service's
  `can()`); only the photo writes refuse before reading.
- On `/admin`, the admin's upload to a verified space is still read before its 403 (one trusted
  account; unchanged).
- Many concurrent managed reads exhausting the pool (R001's second consequence): the fix removes the
  second connection; no test fills the pool.
- A reception upload larger than 4 MiB now answers 403, not 413 (refused before multer).
- `requireCan('space.read')` on the reads, if S1 is not approved: unreachable as a refusal.
- `waitingOnLock` counts any waiting backend of the test database: a test with two requests passes
  `count: 2`; a test whose request waits on something it did not intend would pass the helper.
- A1's assumption that nothing between the space's lock and `namesFor` reads `users` (§9): a future
  read of `users` there would make A1 pass for the wrong reason.
- The confirm routes have no body: their refusal order is unchanged and untested.

## 11. Every document edit, written out

`<today>` and `#PRNUM` as defined at the top. Each edited document's header *Last Updated* →
`<today>` (in the first commit that edits it).

**C1**
- Finding 52: `**Status:** Open · **Date:** 2026-10-12` → `**Status:** Resolved · **Date:** 2026-10-12`;
  append: "*Resolved (<today>, #PRNUM):* every race test acts once its request is seen waiting on a
  lock. `waitingOnLock` in `apps/api/test/locks.ts` polls `pg_stat_activity` for a backend of the test
  database waiting on a lock and fails after four seconds; `whileHeld` and the tests that hold their
  own transaction call it. A race whose request never reached its lock now fails instead of passing
  without interleaving: with a test's hold removed, the helper's error failed the run."
- Index: remove 52 from *Open*; add it under *Resolved* between 51 and 60.
- With S6: `testing.md` §3 rule 7, the sentence of S6.

**C2**
- `space-links.md` *How it composes*, the single-space read's bullet: "The names are read under the
  space share lock from `users`." → "The names are read from `users` in the read's own transaction,
  under the space's share lock."
- `space-links.md` *API history*, appended: "- #PRNUM — `ownersFor` reads the names in its caller's
  transaction."
- `spaces.md` *API history*, appended: "- #PRNUM — the read and the fact writes read one statement at a
  time, the owners' names in their transaction."

**C3**
- `security.md` *Authorization*, the bullet "The managed-space boundary checks…" replaced by:
  "- **The managed-space boundary**, `requireSpaceAccess`, mounted once on `/manage/spaces/:spaceId`,
  admits a caller only when `can()` allows them `space.read` there: an active `OWNER` or `RECEPTION`
  link. Anyone else (no link, a deactivated one, an unknown or a soft-deleted space) gets `not_found`
  (404), so an unrelated caller cannot learn whether the space exists; a hidden live space stays open
  to its active links. Each write is then decided by its own owner-only `can()` action, in its service,
  under the space's lock."
- `security.md` header *Built*: after "`requireRole`, mounted once on `/admin`;" add
  "`requireSpaceAccess`, mounted once on `/manage/spaces/:spaceId`;".
- `conventions.md` header (R004): in *Built*, `shared/auth (…)` gains "`requireSpaceAccess` on
  `/manage/spaces/:spaceId`"; *Not yet built:* "`optionalAuth` and the refusing space middleware of
  `/manage` (§8)" → "`optionalAuth` (§7)".
- `conventions.md` §8 *Space access*, the "**Built:** it refuses…" bullet replaced by: "- It refuses
  whom `can()` refuses `space.read` at the space, as [security › Authorization](security.md#authorization)
  says, and otherwise puts the space's links on the request: the `SpaceResource` from which `can()`
  reads the caller's role and whether the space is verified."
- `api-contract.md` *Managed spaces*, the paragraph "Managed routes require an active…" replaced by:
  "Every route below needs an active `OWNER` or `RECEPTION` link at the named live space; without one,
  and for an unknown or soft-deleted space, it answers `not_found` (404)
  ([security › Authorization](../backend/security.md#authorization)). Reads reuse `AdminSpace` and
  the admin photo shapes; writes reuse the same services, validation, locks and audit action names as
  the admin routes." In *Managed photos*, the last bullet becomes "- Reception may list photos but
  cannot upload, remove or reorder them." (its 404 sentence dropped: the paragraph above says it).
- `spaces.md` *How it composes*, the managed routers' bullet → "- **The managed routers sit below
  `/manage/spaces/:spaceId`, behind the one boundary** that admits the space's staff
  ([security › Authorization](../backend/security.md#authorization)); the shared controllers and
  services keep the admin's validation, locks and audit names."
- `space-links.md` *How it composes*, the managed routes' bullet → "- **Managed routes** take their
  access from these links: the boundary on `/manage/spaces/:spaceId` reads them through the links
  loader ([security › Authorization](../backend/security.md#authorization))."

**C4**
- `security.md`, the managed-space bullet gains: "The managed photo writes ask `can()` first, at the
  route, through `requireCan(action)`: a caller who may not change the photos is refused (403) before
  the request is counted or its body read; the service still decides under the lock." (If S1 is not
  approved, add: "; the managed reads name `space.read` at the route the same way".) Header
  *Built*: "`requireSpaceAccess`, mounted once on `/manage/spaces/:spaceId`, and `requireCan` on its
  photo writes;".
- `conventions.md` §1, the `auth/` line: "the access-token codec, requireAuth, optionalAuth,
  requireRole, requireSpaceAccess and requireCan (§8), can(), signedIn (the claims a guard set)",
  wrapped as the block wraps. Header *Built*: `shared/auth (…)` gains "`requireCan`". With S3, §2's
  cell (§5). §8 *Space access*, a bullet after "Modules read the links…": "- **`requireCan(action)`**
  (`shared/auth`) asks `can()` for one action at the route, from the links on the request, where a
  refusal must come before the request's body is read
  ([security › Authorization](security.md#authorization)); the service's own `can()`, under the
  space's lock, still decides."
- `api-contract.md` *Managed photos*, the last bullet → "- Reception may list photos; its upload,
  removal or order answers `forbidden` (403) before the request is counted or its body read."
- `spaces.md` *Behaviour › Photos*, the upload line: after "…so a refused upload costs no decoding and
  no store" insert "; on the managed route, `can()` is asked before the upload is even counted or read
  ([security › Authorization](../backend/security.md#authorization))".
- `spaces.md` *API decisions*, appended: "- **The managed photo writes ask `can()` at the route, through
  `requireCan`, before the upload is counted or its body read;** the service's own `can()`, under the
  space's lock, still decides (the owner's D4). *Why:* reception's refused upload was read into memory
  first, and the managed reads' two copies of the `space.read` check needed one home. <today>,
  #PRNUM." (If S1 is approved, the *Why* ends: "…one home: the boundary, which is that check.")
- `spaces.md` *API history*, the C2 line extended: "…; a managed photo write refused before it is read;
  the managed read's payload and its races tested."

**C5**
- `spaces.md` *API decisions*, appended: "- **Reception reads the space whole, its owners' names and ids
  included** (the owner's D5, the review's option A). *Why:* the staff who work the space every day
  know its owner, and a reception-only shape would be a second contract and a rule no lane tests.
  Revisit when staff management (step 5b) lands. <today>, #PRNUM."

**C6**
- `spaces.md` decision 159: "… 2026-10-15." → "… 2026-10-15, #82."; `space-links.md` decision 105: the
  same.
- `spaces.md` *API history*: "- MANAGE — the owner/reception managed-space API, … upload path." →
  "- #82 — the single-space read and the fact writes carry the space's active owners." and "- #83 —
  the owner/reception managed-space API, reusing the admin services and response shapes; reception
  reads, owners write, and managed photos share the admin upload path." (before the `#PRNUM` line).
- `space-links.md` *API history*: "- MANAGE — the active-link access boundary…" → "- #82 — the active
  owners of one space, for the single-space admin read (`ownersFor`)." and "- #83 — the active-link
  access boundary used by the owner/reception managed-space API." (before the `#PRNUM` line).
- `spaces.md` *Code map › API* (R016): "`apps/api/src/modules/spaces/`, entry `index.ts`: `space/`
  (create, read, hide, delete, restore), `profile/` (the edit), `facts/` (the one save path of a
  group, and every group's read), `hours/` (the hours and the shifts, with the pure rule of how a save
  changes the shifts), `prices/`, `amenities/` (the links and the own amenities), `contacts/`,
  `confirm/` (a group confirmed unchanged), `photos/` (the gallery: its sizes, its order and cover,
  the upload's order of work), `listing/` (the page the admin's list reads), `public/` (the public
  listing and the public page, for the directory); the pure rules beside them (the slug, staleness and
  missing groups, the profile's fields); the summaries in the module's root service; the admin router,
  and a manage router each for the space and its photos, on the same controllers and services."
- `v1-mvp.md` (R005), the row `| PUT | \`/manage/spaces/:spaceId/{hours|prices|amenities|contacts}\` | …`
  → `| PUT | \`/manage/spaces/:spaceId/:group\` | 🏢 | the facts, one group at a time (\`hours\` with
  the shifts, \`prices\`, \`amenities\`, \`contacts\`), on the same logic as the admin's
  ([api-contract §5](../api/api-contract.md#spaces-the-admin)) |` (the pre-#83 row; `:group` as its
  neighbouring confirm row writes it — the contract writes the `{a|b}` form only in headings).
- Finding 59, under *Evidence* (R017): "*2026-10-15, #82:* the API half landed — the single-space read
  carries its owners. The editor's notice and the unlink dialog remain, so the finding stays Open."
- `overview.md`: only per §4, D9's check.

## 12. The procedure

### 12.1 Before the branch

```powershell
Set-Location C:\Users\basel\masaha-b
git fetch origin
git status --short --branch          # must be clean and detached
git log --oneline -5 origin/main
gh pr list --state open --json number,title,headRefName,headRefOid
git diff --name-status 93f152fe origin/main
```

If `origin/main` moved past `93f152fe` and changed any file of §7's code rows, re-read those files; if
the change contradicts this plan, stop and ask. If an open PR edits any code file of §7, stop and ask.
Then:

```powershell
git switch --no-track -c fix/space-api-hardening origin/main
docker start masaha-postgres-1       # never npm run db:up
```

`apps/api/.env` must point at `masaha_b_dev` / `masaha_b_test` and `PORT=3321` (check the names only;
never print the file).

**One full test run at a time on this machine.** Before each full lane run:

```powershell
Get-CimInstance Win32_Process -Filter "Name = 'node.exe'" |
  Where-Object { $_.CommandLine -match 'vitest' } | Select-Object ProcessId, CommandLine
```

If a line shows `C:\Users\basel\masaha\` (not `masaha-b`), wait for it to end. Focused runs of one or
two files are not full runs.

### 12.2 First checks (before writing code)

1. **D4's type** (§4): after writing `requireCan.ts`, `npm run typecheck`; fallback in §4.
2. **The helper** (D7): write `waitingOnLock`, convert `whileHeld` only, run
   `npm run test:api -w @masaha/api -- src/modules/spaces/photos/photosRace.api.test.ts` three times.
   *If the helper times out* though the request should wait: check `track_activities` is on
   (`SHOW track_activities`) and that the poll runs on `prisma`, not on the holder's `tx` (a
   transaction caches `pg_stat_activity`); find the root cause before any other change; after three
   failed fixes, stop and ask.
3. **A1's determinism** (S2): with A1 written and D1 **not** applied, run
   `npm run test:api -w @masaha/api -- src/modules/spaces/space/space.api.test.ts -t "own connection"`
   three times: red each time on `namesWaiter`. Apply D1: green three times. Check `to_regclass` takes
   the text parameter and `LOCK TABLE` is allowed to the test role. *If any run disagrees,* or the
   test hangs or deadlocks: do not keep A1; record finding 71 (§6) in C2; say so in the report.
4. **S5** (if approved): §5.

### 12.3 Implement, commit by commit (each red first, each break recorded)

Stage **by path**; `git status` before each commit; after each commit `npm run lint` and
`npm run typecheck`. Focused runs: `npm run test:api -w @masaha/api -- <files>` and
`npm run test:unit -w @masaha/api -- <files>`.

| Commit | Subject (chars) | Content |
|---|---|---|
| C1 | `test(api): wait for a race to reach its lock` (44) | D7 (all of §4's D7 but `on`); finding 52 and the index; S6 |
| C2 | `fix(spaces): read owner names in the transaction` (48) | D1, D2; `waitingOnLock`'s `on`; A1 (or finding 71); S5; §11's C2 lines |
| C3 | `refactor(api): let can() decide managed access` (46) | D3; U2 (`git mv` + rewrite); §11's C3 lines |
| C4 | `fix(spaces): guard managed routes with requireCan` (49) | D4; U1; T5, T6; S4's A2; §11's C4 lines; S3's §2 cell |
| C5 | `test(spaces): cover the managed read and races` (46) | T1–T4; D5's decision |
| C6 | `docs(spaces): correct the managed API's records` (47) | R005, R010, R016, R017; the overview's date if §4's check says so |

Commit bodies say *why* (one or two lines each); no tool attribution, no trailer.

The order of work inside each: the test first, seen red (or, for existing code, its break made and
seen red), then the code, then green, then the documents. C1 is test-only: its evidence is the
converted files green and T4's helper break (made in C5; recorded then).

**A fix before the push** folds into its commit:

```powershell
git commit --fixup=<sha> -- <paths>
$env:GIT_SEQUENCE_EDITOR=':'; git rebase -i --autosquash $(git merge-base HEAD origin/main); Remove-Item Env:GIT_SEQUENCE_EDITOR
```

Then lint and typecheck at every rewritten commit:
`git rebase -x "npm run lint && npm run typecheck" $(git merge-base HEAD origin/main)`.

### 12.4 Verification on the head (phase 4)

One at a time, after §12.1's check: `npm run lint` · `npm run typecheck` · `npm run test:unit` ·
`npm run test:api` · `npm run format:check` · `npm run check:links`. Not run, with why: §5 (*Rules
the item touches*). Also `git grep -n "WAIT_MS\|aWhile\|setTimeout(resolve, " -- apps/api` must find no
race wait (a non-race `setTimeout` may remain; say which).

### 12.5 D8's breaks

For each row of D8: copy the file to `$env:TEMP\harden-breaks\` (a backup), make the one edit, run the
named files, copy the red output (failing titles and assertion lines) into the report, restore from
the backup (never `git checkout`), then `git diff --stat` must be empty. A break that stays green:
stop and ask.

### 12.6 The real run (API on 3321)

1. `npm run dev -w @masaha/api` in the background; `curl.exe -s http://localhost:3321/health`.
2. Data in `masaha_b_dev`, through the API: sign in the seeded admin (`POST /api/v1/auth/login`, the
   `SEED_ADMIN_*` account; never print the password); `POST /api/v1/admin/spaces` (a space in an
   active area); `POST /api/v1/admin/owners` `{ name, email, spaceId }` → the temporary password; sign
   in as it; `POST /api/v1/me/password` → the owner's token. Register two users
   (`POST /api/v1/auth/register`): reception and a stranger. Link reception — no API exists for it
   yet (step 5b) — in the dev database only:
   `docker exec masaha-postgres-1 psql -U masaha -d masaha_b_dev -c "INSERT INTO space_managers (space_id, user_id, role, created_at, updated_at) VALUES (<space>, <reception>, 'RECEPTION', now(), now())"`
   (the user name from `apps/api/.env`'s URL; the password never printed).
3. Requests, each status recorded: owner `GET /manage/spaces/<id>` → 200 with `owners`; reception the
   same → 200, the same body; reception `POST /manage/spaces/<id>/photos` with no file → 403 and with
   a JPEG → 403, then `SELECT count(*) FROM rate_limits WHERE key LIKE 'photo-upload:%'` → 0; owner
   `PUT /manage/spaces/<id>/contacts` `{ "contacts": [] }` → 200; admin `GET /manage/spaces/<id>` →
   404; stranger → 404; owner `GET /manage/spaces/999999` and `/abc` → 404; no token → 401.
4. Stop the server by its process id (a backgrounded dev task can leave `tsx watch` on the port), then
   `Get-NetTCPConnection -LocalPort 3321 -ErrorAction SilentlyContinue` must print nothing.

### 12.7 The PR number, push and PR

Just before the push, in Git Bash:

```bash
n=$(( $(gh api "repos/{owner}/{repo}/issues?state=all&per_page=1&sort=created&direction=desc" --jq '.[0].number') + 1 ))
base=$(git merge-base HEAD origin/main)
git filter-branch -f --tree-filter "grep -rl '#PRNUM' docs | xargs -r sed -i 's/#PRNUM/#$n/g'" $base..HEAD
git for-each-ref --format='%(refname)' refs/original/ | xargs -r -n1 git update-ref -d
git grep -n '#PRNUM' ; echo "expect nothing above; PR will be #$n"
git push -u origin fix/space-api-hardening
```

Then at once `gh label list` (create `fix`, `area:api`, `area:docs` if missing, with a description and
a colour), and:

```powershell
gh pr create --assignee @me --label fix --label area:api --label area:docs `
  --title "fix(spaces): read owner names in the transaction" --body-file <the description below, saved as a file>
```

Confirm the number GitHub gave equals `n`; if not, replace it in the documents (a fixup into the
commits that hold it), `git push --force-with-lease`.

### 12.8 CI, CLEAN, conflicts, report

- `gh pr checks <n> --watch`; then `gh pr view <n> --json headRefOid,mergeStateStatus,statusCheckRollup`:
  CI green **on the pushed head** and `CLEAN`. Never merge. Never rebase a `CLEAN` PR.
- **Conflicts, early:** for every other open PR (GALLERY expected),
  `git merge-tree --write-tree HEAD <its headRefOid>`; record clean, or the conflicted paths. A
  documents-only conflict takes the fast path when its turn comes (a rebase keeping both sides,
  `format:check`, one push); a conflict in code: stop and ask.
- **The report**, `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\HARDEN_REPORT.md`, written in parts
  with an editor (UTF-8; never through a lossy shell redirect): the head and the commits; each
  command run and not run; each test's red-first output; each break of §9 and D8 with its red output;
  the first checks' results (§12.2); the real run's statuses; the problems and their solutions;
  anything unexpected, even unsolved; the conflict check; departures from this plan, each with its
  reason; the PR number, and that GALLERY's plan assumed #85.

### 12.9 The PR description (written out; fill the evidence from the runs)

```markdown
## Summary
Hardens the spaces API after #82 and #83, from their post-merge review:
- the owners' names are read in the read's own transaction (`ownersFor`'s `tx` required), and a
  transaction runs one statement at a time;
- the managed boundary decides through `can(actor, 'space.read', …)`, with no rule of its own;
- `requireCan(action)` (`shared/auth`) replaces the routers' inline checks and refuses a managed
  photo write before it is counted or read;
- one race helper, `waitingOnLock`: every race test acts once its request is seen waiting on a lock
  (finding 52 resolved);
- the missing tests: the managed read's payload for owner and reception, unknown and malformed ids
  and a guest, a hidden space, the limit before the file, a link change racing a managed write, and
  which connection reads the owners' names;
- the documents: the no-hint 404 rule's one home in `security.md`; #82/#83 on their lines;
  `v1-mvp.md`'s row; the code map; finding 59's dated line; D5 recorded.

## Scope
<§2 Scope>
## Acceptance criteria
<§2's checklist, ticked>
## Out of scope
R015; `apps/web`; `packages/shared`; packages, staff, capacity; finding 69; #84's lines.

## Change type
fix — API code, tests and documents. No schema, migration or dependency.

## Evidence
- `npm run lint`, `npm run typecheck` (each commit), `npm run test:unit`, `npm run test:api`,
  `npm run format:check`, `npm run check:links`: <results>.
- Seen failing first: <each test, its red line>.
- Deliberate breaks (testing §3 rule 7), each red then restored: <D8.1–D8.7 and §9's breaks>.
- Real run on 3321: <statuses>.
- Not run: `test:component`, `build`, `check:build`, `check:classes` — no file in `apps/web` or
  `packages/shared` changed; CI runs them.

## Screenshots
None: API and documents only.

## Definition of Done checklist
- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean.
- [x] Tests added in the owning lane, each seen failing.
- [x] No user-facing text added.
- [x] Authorization enforced on the server (the boundary and `requireCan`; the services still decide).
- [x] Triggered documentation updated in this PR; no deferred document triggered.
- [x] One home per fact: the 404 rule in `security.md`, linked elsewhere.
- [x] Every claim names its test or command.
- [x] Atomic history, pushed.
```

## 13. Decisions needed from the owner

1. **S1** — drop the route check on the managed reads (recommended), or keep D4 as written.
2. **S2** — A1 by the reading backend's id (recommended), finding 71 as the fallback.
3. **S3** — correct conventions §2's route chain (recommended), or record finding 75.
4. **S4** — A2, the limit's order on `/admin` (recommended).
5. **S5** — D2's warning guard, kept only if it can go red (recommended).
6. **S6** — the race rule in testing §3 rule 7 (recommended).

## 14. Stop and ask

- `origin/main` changed a code file of §7 in a way this plan does not cover, or an open PR edits one.
- A change is needed in `packages/shared`, `apps/web`, the schema, a migration or a dependency.
- More than about 40 files would change.
- `requireCan`'s typing fails both ways in §4 (no cast).
- The helper times out on a race test and three root-cause fixes fail.
- A D8 or §9 break stays green (a security, transaction or ordering property without a proving test).
- A test fails for a reason not understood after three fixes; CI fails for a reason not reproduced
  locally after three.
- GALLERY's PR conflicts with this branch in a code file.
- Anything in this plan proves false against the code at execution time.

## Appendix — skill map (a map only; no step depends on a skill)

| Step | Claude Code skill |
|---|---|
| §12.1 — the folder, the reading, the branch | `start-work-item` |
| Saving this plan | `write-plan` |
| §12.3 — red first, the breaks | `superpowers:test-driven-development` (optional, workflow §10) |
| §12.2, §14 — a failure's root cause | `superpowers:systematic-debugging` (optional) |
| §12.4–§12.7 — scope, commits, push, PR | `open-pr` |
| §12.8 — the report after CI and `CLEAN` | `final-report` |
