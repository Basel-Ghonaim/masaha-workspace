# Post-merge review — PR #82 and PR #83

## 1. What was reviewed

| PR | Merge SHA | Commits | Base |
|---|---|---|---|
| #82 `feat(spaces): include owners in admin space reads` | `1efe2b8a` (head `8ed0a5fa`) | 1 | `a82541b1` |
| #83 `feat(spaces): add managed space API` | `72ceb047` (heads `d5726ddf`, `5e4e610b`) | 2 | `1efe2b8a` |

Today's state read for comparison: `origin/main` = `93f152fe` (includes PR #84).
Reviewed by reading commit objects only (`git fetch`, `git diff`, `git show`, `git show origin/main:<file>`). No tests were run, no branch cut, no file in any repository folder touched. Where a line number is given without a SHA, it is `origin/main` today; where a file is one of the two PRs', the line number is at the head that introduced it and is marked.

## 2. Verdict

**Both PRs are structurally right and honestly scoped — the managed boundary is correctly mounted, correctly refusing, and correctly reusing the admin's services, and the shared-contract slice is clean. What is not right is concentrated in one place: the owner-name reader added by #82 reads `users` outside the transaction it was injected into, and everything built on top of it inherits that.** Fix that one line, fold the middleware's copied rule into `can()`, and the rest is documentation hygiene and test coverage.

## 3. Findings, most severe first

### R82-83-001 — The owner-name read leaves the space's transaction and its lock

**Severity:** blocker · **Verified**

**File:** `apps/api/src/modules/space-links/admin-spaces/adminSpaces.service.ts:33` (at `8ed0a5fa` and at `origin/main`)

```ts
async ownersFor(spaceId: number, tx?: Tx) {
  const links = await repository.findOwnerLinks([spaceId], tx);   // tx  ✅
  const names = await users.namesFor([...new Set(links.map(({ userId }) => userId))]); // no tx  ❌
```

`users.namesFor(ids, tx?)` (`apps/api/src/modules/users/users.service.ts:372`) forwards to
`repository.findNames(ids, tx = db)` (`apps/api/src/modules/users/users.repository.ts`), so with no
second argument the names query runs on the **default Prisma client** — a different pooled
connection, outside the interactive transaction and outside the `FOR SHARE` lock the links were read
under.

**Failing scenario.** Two consequences, one of them a promise the documents now make.

1. *The lock guarantee is not the one #82 claimed.* `OWNERSREAD_PLAN.md` D3 and its acceptance
   criterion "Owner data and `isVerified` are read consistently under the existing `FOR SHARE` lock"
   are not met: the link set is locked, the names are not. `docs/features/space-links.md:45` states
   the false version as fact ("The names are read under the space share lock from `users`").
2. *Every single-space read now needs two pool connections per in-flight request.* The transaction
   holds one while the names read asks for another. The repository already knows this and says so in
   the file #82 edited — `apps/api/src/modules/spaces/facts/groupEdit.ts:71-72`: *"Read before the
   transaction opens: inside it, a read without `tx` waits on a second connection while the
   transaction holds one"* — which is why `platformSettings.stalenessThresholds()` is hoisted out of
   the callback. `apps/api/src/db/prisma.ts` builds the pool with no `max`, so `pg`'s default of 10
   applies and `connectionTimeoutMillis` guards the *handshake*, not acquisition. Ten concurrent
   `GET /admin/spaces/:spaceId` (or `GET /manage/spaces/:spaceId`, or ten concurrent fact writes)
   fill the pool; every one of them then waits for a connection only it can release. The API stops
   answering, and nothing logs an error. Plausible, not reproduced here, but the mechanism is
   plain and the rule is written in the repository.

**Fix.** `const names = await users.namesFor([...new Set(links.map(({ userId }) => userId))], tx);`
Then make the parameter non-optional — `ownersFor(spaceId: number, tx: Tx)` — so the next caller
cannot make the same omission; both call sites (`space.service.ts:102`, `groupEdit.ts:87`/`:105`)
already pass one, and `adminSpaces.service.ts:60`'s list composition is a different function.

**Where the fix belongs:** a fix item now (one line of production code, transaction/security).

---

### R82-83-002 — Two statements in flight on one transaction

**Severity:** should-fix · **Verified** as a rule violation; **plausible** that it re-creates finding 11's `pg` condition

**Files:** `apps/api/src/modules/spaces/space/space.service.ts:100-103`,
`apps/api/src/modules/spaces/facts/groupEdit.ts:85-88` and `:105`

```ts
const [facts, owners] = await Promise.all([readFacts(space.id, tx), ownersFor(space.id, tx)]);
```

**Failing scenario.** Both branches of an interactive transaction share one `pg` client, and
`Promise.all` puts two statements on it at once — exactly the shape
`docs/architecture/findings/11-nested-writes-in-an-interactive-transaction-trigger-a-pg-deprecation-warning.md`
was filed about, and exactly what the module says in a comment two files away:
`apps/api/src/modules/spaces/facts/facts.ts:34` — *"One query at a time: a transaction's connection
runs one statement at once (finding 11)."* `docs/backend/conventions.md` §8 *Transactions* states the
rule: *"Inside an interactive transaction, write one statement at a time, never a nested create."*
Nothing breaks today — `pg` queues the second statement and both see the same snapshot — but no test
can see it either: finding 11's guard, `createWithoutNestedWrites.api.test.ts`, watches the **first
creation** in the process and never touches `get` or a fact write, so the property is unproven in
exactly the two places it now applies.

It also compounds R82-83-001: the `ownersFor` half issues its link query on `tx` while `readFacts`
is still issuing its first, and then reaches out of the transaction for the names.

**Fix.** Sequential awaits in all three places:

```ts
const facts = await readFacts(space.id, tx);
const owners = await ownersFor(space.id, tx);
```

**Where the fix belongs:** the next branch touching `apps/api/src/modules/spaces/space/space.service.ts`
and `apps/api/src/modules/spaces/facts/groupEdit.ts` — or fold it into R82-83-001's fix item, which
already opens both files' call sites.

---

### R82-83-003 — `requireSpaceAccess` re-implements the staff rule instead of asking `can()`

**Severity:** should-fix (security boundary) · **Verified**

**File:** `apps/api/src/shared/auth/spaceAccess.ts:15`

```ts
if (!links.some((link) => link.userId === userId && link.deactivatedAt === null)) {
  throw AppError.notFound();
}
```

**Failing scenario.** That predicate is a second home for ADR 0002 / ADR 0009's rule "the role at a
space comes only from the caller's active link", which `apps/api/src/shared/auth/can.ts` owns as
`roleAt()`. `docs/backend/security.md` says *"`can(actor, action, resource)` … Services call"* it and
names `can()` the decider; `docs/backend/conventions.md` §8 *Space access* says *"`can()` decides per
action."* Today the two agree, because `SpaceManagerRole` is exactly `OWNER | RECEPTION`
(`apps/api/prisma/schema.prisma:35`). The day a third role exists — a manager, a viewer, a
maintenance account — the middleware admits the caller and the service's own `can()` refuses with
**403**, which is precisely the existence hint the settled `404` decision exists to remove
(`MANAGE_PLAN.md`, decision 2). Nothing would catch it: `can.unit.test.ts` proves `can()` alone, and
`manage.api.test.ts` only exercises the two roles that exist.

**Fix.** One rule, and the `404` becomes a decision change rather than a rule change:

```ts
const actor = signedIn(req);
if (!can(actor, 'space.read', { links })) throw AppError.notFound();
```

**Where the fix belongs:** a fix item now (two lines, security; `can` is already exported from the
same folder).

---

### R82-83-004 — `conventions.md`'s header still lists the middleware that §8 now says is built

**Severity:** should-fix · **Verified**

**Files:** `docs/backend/conventions.md:3` (header) vs `docs/backend/conventions.md:195-197` (§8)

**Failing scenario.** Line 3 still reads **"Not yet built:** `optionalAuth` and the refusing space
middleware of `/manage` (§8); …"** — four lines above §8 gained the bullet **"Built:** it refuses a
caller with no active link at the space with `not_found` (404) …"** from PR #83. A Contract's header
is where `docs/architecture/documentation.md` §6 says a reader looks for which platform rules are
built, and §4 makes a declared class binding. The `Built:` sentence in the same header also still
enumerates `shared/auth` without `requireSpaceAccess`. The header's `Last Updated:` stayed at
2026-10-13. The document now contradicts itself on its first line and its 195th.

**Fix.** In the `Built:` sentence, extend the `shared/auth` list to name `requireSpaceAccess` on
`/manage/spaces/:spaceId`, and delete "`optionalAuth` and the refusing space middleware of `/manage`"
from **Not yet built**, leaving `optionalAuth`. Set **Last Updated:** 2026-10-15.

**Where the fix belongs:** a fix item now (documentation, one line + one clause + the date).

---

### R82-83-005 — `v1-mvp.md`'s managed fact-row breaks the table it sits in

**Severity:** should-fix · **Verified**

**File:** `docs/plans/v1-mvp.md:223`

```
| PUT | `/manage/spaces/:spaceId/{hours|prices|amenities|contacts}` | 🏢 | the fact groups, on the same logic as the admin's |
```

**Failing scenario.** Three unescaped `|` inside a four-column table row: Markdown parses it as six
cells, so the row renders wrong or is dropped, and the `{...}` form is not a real path — the server
mounts one literal route per group (`spaces.manage.routes.ts`, `for (const group of FACT_GROUPS)`).
The neighbouring photos row at `v1-mvp.md:227` escapes them correctly (`\|`), which is why the
reviewer reading for that row missed this one. `npm run format:check` does not catch table-cell
width; `npm run check:links` does not look inside tables, so CI stayed green.

**Fix.** `` `/manage/spaces/:spaceId/{hours\|prices\|amenities\|contacts}` `` — or, better, restore
the row's original `:group` placeholder, which is both valid Markdown and the shape
`api-contract.md:195` and the code use.

**Where the fix belongs:** a fix item now (documentation, one row).

---

*(sections 3–7 — remaining findings, the tests table, step 8's points, "Checked and fine", and the
decisions for the owner — are appended below.)*
---

### Remaining findings, less severe

### R82-83-006 — The managed read's `can()` is duplicated in two routers and cannot fail

**Severity:** should-fix · **Verified**

**Files:** `apps/api/src/modules/spaces/spaces.manage.routes.ts:40-43`,
`apps/api/src/modules/spaces/photos.manage.routes.ts:20-24`

```ts
router.get('/', async (req, res) => {
  const { userId, role } = signedIn(req);
  if (!can({ id: userId, role }, 'space.read', spaceOf(req))) throw AppError.forbidden();
  await space.get(req, res);
});
```

**Failing scenario.** `requireSpaceAccess` has already admitted an active `OWNER` or `RECEPTION`
link and put exactly those rows in `spaceOf(req).links`. `can(actor, 'space.read', …)` is `staff`,
which is `roleAt(...) !== undefined` — the identical predicate the middleware just applied
(R82-83-003). So both copies are `true` by construction on the only path that reaches them: dead
code that proves nothing, written twice. `MANAGE_PLAN.md` asked for the opposite — *"Extend the
shared read handler only if needed to call `can(actor, 'space.read', space)`. Do not add route-specific
role checks or duplicate handlers."* The check cannot simply move into `space.get`, because the
admin's read of an unverified space must not require `space.read` (`can.unit.test.ts:76` makes ADMIN
`false` for it) — which is exactly why the copy crept in, and why it needs a single home rather than
a deletion.

**Fix.** One `requireCan(action)` middleware in `shared/auth` (next to `requireRole`, on the same
`RequestHandler` shape), mounted on the managed read routes and — per R82-83-007 — on the managed
photo write routes. Two files stop holding their own copy.

**Where the fix belongs:** the next branch touching `spaces.manage.routes.ts` and
`photos.manage.routes.ts` (and `shared/auth/index.ts`).

---

### R82-83-007 — Reception's refused photo upload is buffered into memory first

**Severity:** should-fix · **Verified**

**Files:** `apps/api/src/modules/spaces/photos.manage.routes.ts:26-32`, refused at
`apps/api/src/modules/spaces/photos/photos.service.ts:86`

**Failing scenario.** The order matches `/admin` exactly — `limitRequests` → `receiveFile('photo',
PHOTO_MAX_BYTES)` → `photos.upload` — and that is what the plan asked for. But on `/admin` the
non-admin never reaches the router at all (`requireRole('ADMIN')` is mounted above it,
`app.ts` "The platform's routes: guarded once here"), so `receiveFile` only ever runs for a caller
who may upload. On `/manage` `requireSpaceAccess` admits reception, so a reception user walks
`limitRequests` (consuming one of 30 `PHOTO_UPLOAD` counters per 15 minutes, `spaces.limits.ts`) →
`receiveFile` (full multipart parse, up to `PHOTO_MAX_BYTES` held in `req.file.buffer`) →
`photos.upload` → the cheap `can()` refusal at line 86. Thirty times a quarter, per reception
account, each one a discarded multi-megabyte buffer. `docs/features/spaces.md:97` claims "a refused
upload costs no decoding and no store" — true, and the file has nonetheless already been read.
`manage.api.test.ts:99-105` proves the 403 and cannot see the cost.

**Fix.** Mount the permission before the body reader, using R82-83-006's `requireCan`:
`requireCan('space.photos.manage'), limitRequests(…), receiveFile(…), photos.upload`. The service's
own check at line 86 stays — it is the one decided under the lock and stays authoritative.

**Where the fix belongs:** the next branch touching the manage photo routes; same branch as
R82-83-006.

---

### R82-83-008 — The no-hint `404` rule is written out in eight places

**Severity:** should-fix · **Verified**

**Files:** `docs/api/api-contract.md:177-181`, `:185`, `:207-208`;
`docs/backend/conventions.md:195-197`; `docs/backend/security.md:77-81`;
`docs/features/spaces.md:36-38`; `docs/features/space-links.md:41-43`;
`docs/plans/v1-mvp.md:216-218`

**Failing scenario.** The analyst counted five; it is eight, three of them inside the document that
owns the fact. `docs/architecture/documentation.md` §1 gives security rules one home in `security.md`
and says every other document links; §3 says a capability document "must not contain … a restated
mechanism, a security rule". Both `spaces.md` and `space-links.md` now restate it in full — including
the hidden-space exception, which is the part most likely to change — and `conventions.md` restates
it a third time while its own header still says the middleware is unbuilt (R82-83-004). A future
change to the boundary (a third role, a `403`, a hidden-space exception) has to be found in eight
documents; the likeliest outcome is that it is applied in one and seven go on lying.

**Fix.** `security.md` keeps the rule; `conventions.md` §8 links it instead of restating it; the two
capability documents say what *they* own — "`space-links`'s links decide the managed routes' access
([security › Authorization](../backend/security.md#authorization))" — and drop the 404 prose;
`v1-mvp.md`'s "Built:" line keeps one clause; `api-contract.md` keeps the status on the endpoints
(its own job, §2 of the ownership table) and drops the standalone paragraph at 177-181 and the
duplicate at 207-208.

**Where the fix belongs:** the next branch touching `docs/api/api-contract.md` and
`docs/features/spaces.md` + `docs/features/space-links.md` — this is the natural follow-on to the
next web screen (step 5b), which will edit the same paragraphs.

---

### R82-83-009 — `space-links.md` states the names are read under the share lock; they are not

**Severity:** should-fix · **Verified**

**Files:** `docs/features/space-links.md:45`, repeated at `:105` and `docs/features/spaces.md:159`

> "The names are read under the space share lock from `users`."

**Failing scenario.** False as of #82 — see R82-83-001. `CLAUDE.md` ("Claim only what is true") and
`documentation.md` §1 ("Nothing unbuilt is described as built") both apply; here the code says the
opposite of the sentence. It becomes true the moment R82-83-001 is fixed, so the two belong in one
commit.

**Fix.** With R82-83-001 applied, the sentence is correct as written and nothing else changes. If
R82-83-001 is deferred, reword to: "the links are read under the space share lock from
`space-links`; the names follow from `users`."

**Where the fix belongs:** the same fix item as R82-83-001 (documentation rides with the code,
workflow.md §7).

---

### R82-83-010 — The new decision and history lines name no PR, and two of them are labelled "MANAGE"

**Severity:** should-fix · **Verified**

**Files:** `docs/features/spaces.md:159` and `:243`; `docs/features/space-links.md:105` and `:153`

**Failing scenario.** `documentation.md` §5.7: *Decisions* are "each with its reason, its date and its
**PR**"; §5.10: *History* is "**the PRs**". Every neighbouring decision line in both documents ends
`2026-10-XX, #NN` (`spaces.md:109-123`, `space-links.md:96-105`). The four new lines end
`2026-10-15.` or `- MANAGE — …`, so neither the decision nor the history points at `#82` / `#83`,
and "MANAGE" is a work-item identifier where every sibling uses a human label ("the deleted-spaces
item", "the users item").

**Fix.**
- `spaces.md:159` → end `2026-10-15, #82`.
- `space-links.md:105` → end `2026-10-15, #82`.
- `spaces.md:243` → `- #83 — the owner/reception managed-space API, reusing the admin services and response shapes; …`
- `space-links.md:153` → `- #83 — the active-link access boundary used by the owner/reception managed-space API.`

**Where the fix belongs:** a fix item now (documentation, four lines).

---

### R82-83-011 — No edited document's `Last Updated:` header was bumped by either PR

**Severity:** should-fix · **Verified**

**Files (as at `72ceb047`):** `docs/api/api-contract.md:3` (2026-10-13),
`docs/backend/security.md:3` (2026-10-13), `docs/backend/conventions.md:3` (2026-10-13),
`docs/project/overview.md:3` (2026-10-14), `docs/plans/v1-mvp.md:3` (2026-10-13),
`docs/features/spaces.md:3` (2026-10-14), `docs/features/space-links.md:3` (2026-10-13)

**Failing scenario.** Seven documents were edited across the two merges; every header kept its
pre-merge date. `documentation.md` §5.1 makes "last updated" part of a capability document's header,
and §10 ("Not adopted: a version number per document") says Git holds every version and "each header
has its date" — which is only useful if it moves. `workflow.md` §7 lists "A capability's behaviour,
decisions or code map" as a same-PR documentation trigger, which implies the header follows.
(#84 later bumped `spaces.md` and `space-links.md` to 2026-10-15 for its own change; the other five
are still behind.)

**Fix.** Set the six remaining headers to 2026-10-15 in the fix branch.

**Where the fix belongs:** a fix item now (documentation).

---

### R82-83-012 — The owner-name transaction property has no proving test, and the limitation was not recorded as a finding

**Severity:** should-fix · **Verified**

**Files:** `OWNERSREAD_PLAN.md` test 5; `apps/api/src/modules/spaces/space/space.api.test.ts:273-310`;
`C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\OWNERSREAD_REPORT.md:28`

**Failing scenario.** `OWNERSREAD_REPORT.md` states the result without hedging: *"Removed the
transaction argument from the owner reader using a backup copy. The focused lane stayed green because
the existing test cannot expose an owner query moved outside the read transaction."* The code agrees:
the finding-43 test holds `FOR NO KEY UPDATE` on the space, inserts the owner link, starts the GET
inside that transaction and only then releases it — so the GET's `lockShared` blocks until the commit,
and by the time `ownersFor` runs there is nothing left to observe. `testing.md` §3 rule 7 ("For a
security, transaction or ordering property, the author makes that change once, sees the test fail, and
restores it") is therefore unmet for the one property the plan itself classified as a transaction
property, and `workflow.md` §4/§8 require the observation to become a finding in
`docs/architecture/findings/` — `git ls-tree origin/main docs/architecture/findings` shows no such
entry. The limitation lives only in a PR report, which is not a home any document points at. The
next branch that touches `ownersFor` can drop `tx` again with no red test and no recorded finding.

**Fix — record a finding** (allowed always, `CLAUDE.md`): *"The single-space read's owner names are
read outside the space's transaction, and no test can be made to fail for it."*
**Resolves when:** `namesFor` receives the caller's `tx` **and** a test fails when it does not. The
deterministic form available today: in the existing lock test, assert the owner name is read through
the blocked transaction by renaming the owner's user row *inside* the holder transaction and asserting
the GET answers the committed name — with `tx` it must, without it the read races the holder. If
that cannot be made deterministic, the alternative resolution is to strike the acceptance criterion
from the plan's record and say so, rather than leave a promise no lane owns.

**Where the fix belongs:** a finding to record; the code half belongs with R82-83-001.

---

### R82-83-013 — Four of #83's thirteen planned tests are missing or weaker, and the load-bearing gap is the managed read's payload

**Severity:** should-fix · **Verified**

**File:** `apps/api/src/modules/spaces/manage.api.test.ts` (at `5e4e610b`) — full detail in §4.

**Failing scenario.** No test anywhere asserts **what `GET /manage/spaces/:spaceId` answers**.
`manage.api.test.ts:55` asserts `status === 200` and stops. The contract says the managed read
answers `AdminSpace` "including all fact groups and active owners" (`api-contract.md:184`); a
regression that returned a reduced payload, dropped `owners`, or leaked a field nobody decided on
would pass every lane and reach reception's browser. Reception's receipt of the owners' names and ids
— the item in §7 that needs the owner's decision — is therefore *entirely unproven*. Also absent:
an **unknown** space id on the managed path (planned test 3 covers only the soft-deleted half), a
**hidden** live space (planned test 9's first half), and the **rate limit before the file read**
(planned test 8, on either audience).

**Fix.** Assert the managed read's payload for both audiences — at minimum `owners`, `isVerified`,
`staleGroups` and the fact groups — in `manage.api.test.ts:55`; add the unknown-id and hidden-space
cases; add a `rate_limit` (429) case on `POST …/photos` that sends a file and asserts it is refused
before any decode.

**Where the fix belongs:** the next branch touching `apps/api/src/modules/spaces/manage.api.test.ts`.

---

### R82-83-014 — `spaceAccess.api.test.ts` sits in the API lane but exercises no request path that exists in production

**Severity:** nit · **Verified**

**File:** `apps/api/src/shared/auth/spaceAccess.api.test.ts` (64 lines, two cases)

**Failing scenario.** Both cases build a bare `express()` app, set `req.auth` by hand, and pass a
**stub loader** that ignores `tx` and returns a fixed array; `linksUnder` is invoked with a synthetic
`transaction = {}`. No PostgreSQL, no `spaceLinks.linksAt`, no `requireAuth`, no `parseId`. `testing.md`
§2 gives the API lane "Endpoints end to end: validation, **authorization per role and per space**,
persistence, error envelope" — a file with no database belongs to no lane, and §1's test
("if this test were deleted, would the behaviour still be proven elsewhere?") answers *yes* for both
cases: `manage.api.test.ts:111` and `:139` prove the same refusals through the real request path with
the real loader. The plan asked this file to prove "active-link acceptance, no-link 404, deleted/unknown
404, and `linksUnder(tx)` preservation **through the real request path**"; the stub cannot reach the
deleted/unknown half at all. Its one genuine contribution is the Codex-requested transaction-identity
assertion (`expect(calls[1]?.tx).toBe(transaction)`), which is cheap and worth keeping.

**Fix.** Keep the transaction-identity case and rename it `spaceAccess.unit.test.ts` (it is a pure
middleware unit test); drop the two cases `manage.api.test.ts` already proves, or keep one of them
there explicitly as the stub-rejection case. Either way the API lane should not contain a test that
never reaches the database.

**Where the fix belongs:** the next branch touching `apps/api/src/shared/auth/spaceAccess*.test.ts`.

---

### R82-83-015 — `MANAGE_REPORT.md` no longer holds the implementation PR's evidence, and every em dash in it is corrupted

**Severity:** should-fix · **Verified**

**File:** `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\MANAGE_REPORT.md` (1,684 bytes; begins with a
blank line and `## Review fixes`; every `—` is a literal `?`, byte `0x3F`)

**Failing scenario.** Two problems with one file.

1. *Content.* The file describes only the review-fix commit `5e4e610b`. `workflow.md` phase 6
   requires the report to give "the head and the commits; what was run and what was not; the breaks
   made; the problems met and how they were solved; **anything that behaved unexpectedly**, even
   unsolved; the early conflict check; any departure from the prompt". None of that survives for
   `d5726ddf`: **no deliberate break is recorded at all**, although `MANAGE_PLAN.md` names four (its
   tests 1, 2, 5, 12) and `testing.md` §3 rule 7 requires the break for exactly the authorization and
   locking properties this PR introduced. Nor is there any record of the manual verification plan
   step 7 required — owner read/write, reception read **and refused write**, a stranger's `404`, the
   admin refused on `/manage`. The two properties the owner is relying on — reception refused on
   every write, and the lock-aware path — therefore have **no recorded break evidence anywhere**.
   The one line about breaks is `REVIEW_MANAGE_CODEX_REPORT.md`'s, not the worker's.
2. *Encoding.* The em dashes are `?` (0x3F), so the file renders with `?` where a dash should be on
   every verification line. It was written through a lossy encoding step.

**Fix.** Append rather than replace: re-add a `## Pull request and head` / `## Verification` /
`## Deliberate breaks` section for `d5726ddf` (head, both commits, the full lane list from plan
step 8, the four deliberate breaks with their red output, the 3321 transcript, the conflict check,
and the departures), keep the existing `## Review fixes` section as the second half, and write the
file as UTF-8.

**Where the fix belongs:** a fix item now (records).

---

### R82-83-016 — `spaces.md`'s code map lost its module map and gained a file list

**Severity:** nit · **Verified**

**File:** `docs/features/spaces.md:212-214`

**Failing scenario.** `documentation.md` §5.8: "**Code map:** folders and entry points only, **never
a file list**". PR #83 replaced the enumeration (`space/`… `listing/`, `public/`, "the pure rules
beside them", "the admin router") with "the same modules as the admin plus `spaces.manage.routes.ts`
and `photos.manage.routes.ts` for the managed API". That deletes the entry point a reader starts
from — the one place that says where `createGroupEdit` lives — and substitutes two filenames that
go stale with the next rename.

**Fix.** Restore the module enumeration and add one clause without filenames: "… and one manage
router each for the spaces and their photos, sharing the admin's controllers and services."

**Where the fix belongs:** the next branch touching `docs/features/spaces.md`.

---

### R82-83-017 — Finding 59's evidence now reads as present tense about something #82 changed

**Severity:** nit · **Verified**

**File:** `docs/architecture/findings/59-the-verified-spaces-editor-cannot-name-its-owner.md:5`

**Failing scenario.** Its status is correctly still **Open** and *Resolves when* is still unmet (the
unlink dialog is the remaining half) — nothing was falsely claimed, and both PRs honoured D4. But
the evidence says "`AdminSpace` … carries none of its owners", which was true on 2026-10-13 and is
false since `1efe2b8a`. `documentation.md` §1 lets a record repeat a fact "as of that date", but the
sentence carries no date in the body, so the reader takes it as current.

**Fix.** Add one dated line under the evidence — "*2026-10-15, #82: the API half landed — the single-space
read carries its owners. The editor's notice and the unlink dialog remain, so the finding stays Open.*"
— without touching the status. That is the mechanism §1 allows a finding ("a finding gains its status
and a dated resolution").

**Where the fix belongs:** the next branch that resolves 59, or a fix item now.

---

## 4. The tests, against both plans

Every test each plan names, with where it landed. "Break" answers the plan's own question: *would the
deliberate break this test was written for have made it fail?* Line numbers are at the head that
introduced the test (`8ed0a5fa`, `5e4e610b`).

### 4.1 `OWNERSREAD_PLAN.md` — six planned tests, all in `space.api.test.ts`

| # | Planned test | Where | State | Planned break → would it fail? |
|---|---|---|---|---|
| 1 | Active owner names oldest first, excluding reception and deactivated links | `space.api.test.ts:312` | **present** | **yes** — four owners created with deliberately staggered `createdAt` (−4000 … −1000 ms) and an exact `toEqual` on `[{id,name}]`; including a reception link, keeping a deactivated one, losing the order, or returning `users` order all fail it |
| 2 | An unverified space answers `owners: []`, also with reception/deactivated links | `space.api.test.ts:370` | **present** | **yes** — asserts `[]` for a space with no links *and* after an active `RECEPTION` plus a deactivated `OWNER` link; a "any manager is an owner" or `null`/omitted implementation fails both |
| 3 | The owner reader omits a link with no matching user name | `space.api.test.ts:382` | **present** | **yes** — inserts a `space_manager` row for user `99999` with triggers disabled and asserts the array holds only the real owner; `nameById.get(id) ?? ''` would add `{id:99999,name:''}` and fail |
| 4 | All `AdminSpace` write responses retain owners | `space.api.test.ts:403` | **weaker than planned** — profile `PATCH` and profile `confirm` only; the four fact `PUT`s are not asserted (the plan allowed "one focused case") | **yes** for what it asserts |
| 5 | The read's owners and verification state stay lock-consistent (finding 43) | `space.api.test.ts:273-310` (the pre-existing lock test, extended with `owners: [{id, name:'Ahmad'}]`) | **weaker than planned** — the plan's first case is met; its optional second case ("attempt a blocked owner-link change… assert the response cannot show a stale verification flag beside fresh owners") was not written | **no** for the `tx` half — see R82-83-012; the report records the break staying green. **yes** for the `FOR SHARE` half, which the report records failing 1 of 104 |
| 6 | Existing authorization and not-found matrix stays green | `space.api.test.ts:155-202`, `:255-271`, `:483`, `:588` (unchanged) | **present** | **yes** — guest, USER, another-space owner, this-space owner, pending-password admin, soft-deleted, unknown |

Also landed, un-planned but required: `create.api.test.ts:107` adds `owners: []` to the create
fixture. Declared as a departure in the report and justified (the now-required shared field). Fine.

### 4.2 `MANAGE_PLAN.md` — thirteen planned tests plus the `can()` unit cases

| # | Planned test | Where | State | Planned break → would it fail? |
|---|---|---|---|---|
| 1 | `requireSpaceAccess` accepts an active owner and reception | `spaceAccess.api.test.ts:9` (stubbed) **and** `manage.api.test.ts:55`, `:75` (real) | **present** | **yes** on the real path (reception reads, owner reads); the stubbed copy proves nothing about the loader |
| 2 | A stranger, unrelated owner, unlinked user and admin receive `404` | `manage.api.test.ts:111` | **present** | **yes** — 12 read/write/upload calls per caller, all asserted `404` + `not_found` |
| 3 | Unknown **and** soft-deleted spaces receive `not_found` | `manage.api.test.ts:139` covers the deactivated link and the soft-deleted space | **partial** — an unknown id (e.g. `/manage/spaces/999999`) and a non-numeric id are **not** tested on the managed path | **yes** for the present half |
| 4 | Reception can `GET` the complete space and photos | `manage.api.test.ts:55`, `:89` — `status === 200` only | **weaker than planned** — "the complete space" is never asserted; no body is read | **plausible** — a payload regression (a dropped `owners`, a reduced `AdminSpace`) passes |
| 5 | Reception cannot profile/fact edit, confirm, upload, delete or reorder | `manage.api.test.ts:89` | **present** — all four fact `PUT`s, all five confirms, `PATCH`, order, delete, upload | **yes** — every one asserted `403` + `forbidden`. This was the fix `5e4e610b` added |
| 6 | The owner can profile/fact edit and confirm | `manage.api.test.ts:65` | **present** — all four `PUT`s and all five confirms, status only | **yes** |
| 7 | The owner can list/upload/delete/reorder photos; reception is read-only | `manage.api.test.ts:75`, `:89` | **present** | **yes** |
| 8 | Photo upload is limited **before** the file is read | — | **missing** (on both audiences; no rate-limit test exists for any photo upload) | n/a — see R82-83-013 |
| 9 | A hidden linked space remains manageable; a deleted one does not | `manage.api.test.ts:139` — the deleted half only | **partial** — the hidden half is untested | **no** — there is nothing to fail |
| 10 | Admin routes retain their unverified/verified behaviour | the unchanged admin suites (`space.api.test.ts`, `photos.api.test.ts`) | **present** | **yes** |
| 11 | A fact write and confirmation preserve audit action names and response shape | `manage.api.test.ts:65` — status `200` only | **weaker than planned** — no audit entry is read, no response body inspected | **no** on this lane; the action name is asserted only on the admin path. Defensible under `testing.md` §1's redundancy rule (same service object), but not what the plan asked for |
| 12 | A link change racing a managed write is decided under the space lock | — | **missing as a test.** The *property* holds in code: `groupEdit.ts:78` and `photos.service.ts:62` both read `space.linksUnder(tx)` and decide there | n/a |
| 13 | An owner of another space cannot mutate this space | `manage.api.test.ts:111` | **present** | **yes** |
| — | `can.unit.test.ts`: `space.read` owner/reception/other-space/stranger/admin | `can.unit.test.ts:76` (`'space.read': STAFF`) | **present** — all six actors × verified/unverified, from an expectations table written independently of `can.ts` | **yes** |

### 4.3 Tests that do not run the real request path

- **`apps/api/src/shared/auth/spaceAccess.api.test.ts`, both cases.** Bare `express()` app, `req.auth`
  assigned by hand, stub loader that ignores `tx` and returns a constant array, synthetic
  `transaction = {}`; no PostgreSQL, no `spaceLinks.linksAt`, no `requireAuth`, no `parseId`. It sits
  in the API integration lane but proves nothing the lane owns. Its transaction-identity assertion is
  the one thing worth keeping. See R82-83-014.

No other new test stubs a boundary. `space.api.test.ts` and `manage.api.test.ts` both go through
`createTestApp()` and the real database; the trigger-disabling in `space.api.test.ts:386-392` is a
real `ALTER TABLE` against the test database, not a mock.

### 4.4 Authorization and transaction properties with no proving test

| Property | Planned in | Status |
|---|---|---|
| The managed read answers the full `AdminSpace`, `owners` included, to owner **and** reception | #83 acceptance criteria; `api-contract.md:184` | **no test** — status only (`manage.api.test.ts:55`) |
| Reception is refused **before** any file is read on upload | #83 test 8 (spirit) / #7 executor step | **no test** |
| A hidden live space stays manageable through `/manage` | #83 test 9 | **no test** |
| An unknown space id is refused on `/manage` | #83 test 3 | **no test** |
| A link change racing a managed write is decided under the space lock | #83 test 12 | **no test** (property holds in code) |
| Owner names are read inside the space's transaction | #82 test 5 / D3 | **no test** — the break stayed green (R82-83-012) |
| A guest gets `401`, not `404`, on `/manage/spaces/:spaceId` | implicit (`requireAuth` before `requireSpaceAccess`) | **no test** on the managed path (the `me` router's own suite covers `401` on `/manage/spaces`) |
| A reception account of **another** space is refused on the managed read | `testing.md` §4 | unit-proved (`can.unit.test.ts:76`, `receptionOfAnother: false`); at the API level it is indistinguishable from the stranger case, which is proved |

**Deliberate breaks (testing.md §3 rule 7).** #82 recorded two: the `FOR SHARE` removal failed the
lock test (1 failed, 103 passed) — a real red; and the `tx` removal stayed green, recorded as a
limitation. #83's `MANAGE_REPORT.md` records **none**, though its plan named four. So of the six
security/transaction properties these two PRs introduced, **one** has a recorded red break, one has a
recorded green (which is the finding), and four have none. That is the single largest gap in the
evidence the owner has for these merges.

---

## 5. Step 8 — the analyst's earlier points, checked against the code

| | Point | Verdict | Evidence |
|---|---|---|---|
| (a) | `namesFor` is called without `tx` | **confirmed** | `apps/api/src/modules/space-links/admin-spaces/adminSpaces.service.ts:33` — `users.namesFor([...])` with no second argument; `users.service.ts:372` forwards to `findNames(ids, tx = db)`, so it runs on the default client. The same omission at `:60` is the *list* composition, which is outside any transaction and therefore harmless there |
| (b) | `Promise.all` on one transaction | **confirmed** | `space.service.ts:100-103`, `groupEdit.ts:85-88`, `groupEdit.ts:105`; rule in `facts/facts.ts:34` ("One query at a time … finding 11") and `conventions.md` §8 *Transactions*; only `createWithoutNestedWrites.api.test.ts` guards creation, per finding 11's own resolution |
| (c) | Removing `tx` from the owner reader left the tests green, and no finding was recorded | **partly confirmed** | The green lane is confirmed twice over: the report says so (`OWNERSREAD_REPORT.md:28`) and the code shows why (`space.api.test.ts:273-310` blocks on `lockShared` until the holder commits, so no name read can be observed out of transaction). "No finding recorded" is confirmed for `docs/architecture/findings/`; it *was* written in the PR report, which is not one of the three homes §1 allows a record |
| (d) | #83's planned tests 3, 8, 9, 11, 12 missing, and no deliberate break run | **partly confirmed** | Test 3: soft-deleted present (`manage.api.test.ts:139`), unknown id missing. Test 8: missing. Test 9: the deleted half present, the hidden half missing. Test 11: asserted as a status only, so weaker than planned (the action name is proved on the admin path instead). Test 12: missing as a test, though the production property holds (`groupEdit.ts:78`, `photos.service.ts:62`). "No deliberate break run" is confirmed — `MANAGE_REPORT.md` records none, and the report for `d5726ddf` itself is gone (R82-83-015) |
| (e) | `conventions.md`'s header still lists the refusing middleware as not built | **confirmed** | `conventions.md:3` — **Not yet built:** "`optionalAuth` and the refusing space middleware of `/manage` (§8)" — against the **Built:** bullet PR #83 added at `conventions.md:195`. Still true at `origin/main` |
| (f) | An unescaped `\|` in the `v1-mvp.md` managed row | **confirmed**, and in a different row than one would expect | `v1-mvp.md:223` — `` `/manage/spaces/:spaceId/{hours|prices|amenities|contacts}` `` in a four-column table. The **photos** row at `:227` escapes correctly (`\|`), which is why the analyst's read landed there |
| (g) | The `404` rule is written in five documents | **confirmed, and it is eight** | `api-contract.md:177-181`, `:185`, `:207-208` (three inside the owning document); `conventions.md:195-197`; `security.md:77-81`; `spaces.md:36-38`; `space-links.md:41-43`; `v1-mvp.md:216-218` |
| (h) | Reception's upload is read into memory before the refusal | **confirmed** | `photos.manage.routes.ts:26-32` — `limitRequests` → `receiveFile('photo', PHOTO_MAX_BYTES)` → `photos.upload`; the refusal is at `photos.service.ts:86`. On `/admin` the non-admin never reaches the router (`requireRole('ADMIN')` is mounted above it), so `/manage` is the first audience for which this order costs a full buffer on a refused request |
| (i) | `space-links.md` says the names are read under the share lock | **confirmed, and it is false** | `space-links.md:45` — "The names are read under the space share lock from `users`." They are read on the default client, outside the transaction (R82-83-001). Repeated in substance at `space-links.md:105` and `spaces.md:159` |

---

## 6. Checked and fine

- **The boundary is mounted once, in the right order.** `app.ts` mounts
  `/manage/spaces` (the `me` list, `requireAuth` inside it) first, then
  `api.use('/manage/spaces/:spaceId', requireAuth(), requireSpaceAccess((id, tx) => spaceLinks.linksAt(id, tx)), manage)`.
  A guest therefore gets `401`, not the no-hint `404`; an unauthenticated caller never reaches the
  middleware.
- **Nothing admin-only is reachable under `/manage`.** `createSpacesManageRouter` mounts `GET`, `PATCH`,
  four fact `PUT`s and five `POST …/confirm`; `createPhotosManageRouter` mounts the four photo
  routes. `space.setHidden`, `space.remove`, `space.restore` and `space.create` live on the shared
  controller object and are simply not mounted — hiding, deleting and restoring stay on `/admin`.
- **The `404` shapes are right.** `parseId` answers `not_found` for `abc`, for `0` and for an id past
  `2^31-1`; `linksAt` returns `[]` when `spaces.summariesFor` finds nothing, and `findSummaries` filters
  `deletedAt: null`; it does **not** filter `isHidden`, so a hidden live space stays manageable, as the
  plan settled. A soft-deleted space is also refused on the write paths independently, by
  `groupEdit.ts:75` and `photos.service.ts:61`.
- **Every managed write reaches the same service instance as `/admin`** — `createSpaceController`,
  `createProfileController`, … are built once in `app.ts` and handed to both routers. `can()` and the
  space lock therefore stay authoritative (`groupEdit.ts:78-80` reads `space.linksUnder(tx)` *inside*
  the transaction; `photos.service.ts:106` → `lockFor` does the same), and the audit names come from
  the one `space.<group><Verb>` template in `groupEdit.ts:96`.
- **Photo upload order and limits match `/admin` exactly**: `limitRequests(PHOTO_UPLOAD)` →
  `receiveFile('photo', PHOTO_MAX_BYTES)` → `photos.upload`, with the same shared policy object
  (`spaces.limits.ts`, 30 per 15 minutes) and the same `PHOTO_MAX_BYTES`. Cheap refusals before decode
  and storage remain in the service.
- **`space.read` lives in the one permission table** (`can.ts`, `'space.read': 'staff'`) and
  `can.unit.test.ts:76` proves all six actors on both a verified and an unverified space from an
  expectations table written independently of `can.ts`. ADMIN is deliberately not staff, so
  `/manage` refusing an admin without a link is consistent with ADR 0009 rather than a second rule.
- **`/admin` is untouched by #83**: `requireRole('ADMIN')`, the non-refusing `loadSpaceLinks`, the
  unverified-space admin rules and `createWithoutNestedWrites` all survive unchanged; #83 touches no
  `apps/web` or `packages/shared` file.
- **`ownersFor` is a well-behaved reader**: it reuses `findOwnerLinks`
  (`role: 'OWNER'`, `deactivatedAt: null`, `orderBy: createdAt asc, userId asc`), never touches Prisma
  from the service, never returns a fabricated empty name (`flatMap` + `undefined` check), and its
  omission case is proved with a real trigger-disabled insert rather than a mock.
- **Every `AdminSpace` producer was found** — `create` answers `owners: []` (`space.service.ts:198`),
  `get` and all five fact/confirm responses answer the read set. `typecheck` on both heads proves no
  producer was missed, and the only fixtures needing the field were the two licensed web ones plus the
  one `create.api.test.ts` fixture the report declares.
- **Finding 59 is still `Open`** and neither PR claims otherwise — D4 honoured.
- **`space-links.md`'s "Staff (reception accounts) are not built."** occurred exactly once and that
  occurrence is the one #83 replaced (a diff hunk heading makes it look like three; `grep` over
  `origin/main` finds none).
- **Commit hygiene**: `feat(spaces): include owners in admin space reads` (46 chars) and
  `feat(spaces): add managed space API` (36) — both ≤ 50, imperative, lowercase, no period, no tool
  trailer; every file was staged by path; no tool attribution in either commit body.
- **#82's out-of-licence file** (`space/create.api.test.ts`) is declared in its report with a
  justification. That is the right way to handle it.

### Two findings #84 already settled — recorded for completeness only

- **`docs/features/spaces.md`'s Authority line.** #83's rewrite dropped three true built facts — the
  web's add-space page, the space editor and the list's row actions, and what the public directory
  reads. #84 (`60b2236c`) restored all of them and bumped the header to 2026-10-15. Nothing to do.
- **`docs/project/overview.md`'s Spaces *Built* line.** #83 condensed ~40 words of accurate built
  detail to "the admin's API and dashboard space management". #84 restored the detail and added the
  managed routes. Nothing to do.

---

## 7. Decisions for the owner

### D-a. Do reception accounts receive the owners' names and user ids?

**The fact, as built.** `GET /manage/spaces/:spaceId` answers `AdminSpace` unchanged
(`api-contract.md:184`), so a reception account with an active link receives `owners` — every active
owner's `{ id, name }` — on every read and on every write response. It also receives `isHidden` (the
admin's moderation flag) and `staleGroups` / `missingGroups` / `updatedAt`, which are derived from the
**platform's** staleness thresholds. The only new datum about *another person* is the owners' name and
numeric user id.

| Option | What it costs | What it gives |
|---|---|---|
| **A. As built** — reception reads `AdminSpace` whole | nothing; this is what merged | the owner's identity is available to the staff who work the space daily; reception already sees its own link and role through `GET /manage/spaces` and the session |
| B. A `ManageSpace` response that omits `owners` (and, if you want, `isHidden`/`staleGroups`) for a non-owner | a new type in `packages/shared`, a second mapper or a mapper flag, a second web contract, and the editor will later need the owners anyway | the smallest possible payload for reception |
| C. Keep `AdminSpace` and strip the fields at the edge for a non-owner | no new type, but a per-field filter the contract then has to describe and a web that must handle two shapes of one endpoint | a smaller payload, at the price of a rule that exists nowhere else |

**Recommendation: A for v1.** Reception staff work the space every day; the owner's identity is not a
secret from them, and the numeric id is already exposed to every signed-in user through their own
`SessionUser.spaces` and `/manage/spaces`. Option B is the honest fix if you ever want the separation,
but it is a shared-contract decision, and #83's plan explicitly put it out of scope. Option C is the
one to avoid: it makes "what reception may see" a second, undocumented rule that no lane can test.
Revisit at step 5b, when `/manage/spaces/:spaceId/staff` lands and reception will see the full staff
list regardless.

### D-b. Should a reception upload be refused before the file is read?

**Recommendation: yes — fix it (R82-83-007).** The cost is one `requireCan('space.photos.manage')`
middleware in `shared/auth`, which also removes the two duplicated read checks (R82-83-006). It
restores the property `/admin` has always had — that `receiveFile` only ever runs for a caller who may
upload — and makes R82-83-006's fix and R82-83-007's fix the same commit. If you prefer not to touch
it now, then `docs/features/spaces.md:97` should say "a refused upload costs no decoding and no
store, but on a managed route the file has already been read", and that sentence belongs with the
next branch that edits that paragraph.

### D-c. Should the no-hint boundary decide through `can()`?

**Recommendation: yes — fix it (R82-83-003).** `requireSpaceAccess` exists to turn one `can()` answer
into a `404` instead of a `403`. Written as `links.some(...)`, it is a second copy of the rule that
will drift the first time `SpaceManagerRole` grows a value, and the drift shows up as an existence
hint. `can(actor, 'space.read', { links })` is two lines, needs no new export, and makes the no-hint
decision a *status* choice rather than a *rule* choice. Keep the 404; change what decides it.

### D-d. Where the missing tests land

The three that matter are the managed read's payload (including `owners` for both audiences), the
hidden-space case, and the rate-limit-before-read case. The first belongs with the next branch that
touches `manage.api.test.ts` — which will be step 5b or the packages work. The second is free: add
`isHidden: true` to the existing `manage.api.test.ts:139` case. The third is the one I would argue for
explicitly: without it, the "limited before the file is read" claim in `MANAGE_PLAN.md`'s acceptance
criteria and in `api-contract.md:202-203` has been true in the code since #77 and unproven since, on
both audiences. Your call whether it waits for the branch that reorders the upload.
