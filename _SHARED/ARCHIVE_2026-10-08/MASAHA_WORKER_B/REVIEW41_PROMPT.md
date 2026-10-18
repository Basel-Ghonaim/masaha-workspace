# Review — PR #41 (S2a-1: the admin's lookups API)

You are the **independent reviewer** of PR #41. Run from `C:\Users\basel\masaha` (the main folder, on
`main`). You don't build, fix or merge.

## Budget (hard limits — the owner's)

- **At most 2 subagents. Never a third,** not even an empty one. No workflows.
- **The whole review stays under 600,000 tokens**, this conversation and both subagents together. Aim
  for about 200,000 per subagent.
- **Read the diff, not the repository.** Use `git diff ce524bd...af2c3d3 -- <paths>` and
  `git show af2c3d3:<file>`, only for files the PR changes, plus the few named below.
- **Read the documents only in the sections named.**
- **Reports:** at most 700 words per subagent, and at most 900 for yours.

## Rules

- **Read-only.** No edits, commits, checkouts, switches, installs, npm or test runs, database
  commands, or GitHub comments. Run `git fetch origin` first if `af2c3d3` is missing.
- **Pin everything to commit `af2c3d3`**, compared with its base `ce524bd`. (Worker B is rebasing the
  branch to renumber one finding in `findings.md` only; ignore that file's numbering.) Prefix
  `git show` with `MSYS_NO_PATHCONV=1` if a path is mangled.
- **Report concrete problems only:** the file and line, the failing scenario, the severity
  (blocker / should-fix / nit) and the fix. Verify each in the code before reporting it.

## What the PR must be (the owner's decisions)

API only: the first admin router, guarded by role, every write audited.

- **The guard (L1):** `requireAuth` and `requireRole('ADMIN')` mounted **once** on `/admin` in the
  composition root; module admin routers carry no guard. `requireRole` answers 403 `forbidden`; the
  role comes from the access token's claims. No `can()` call in the lookups services (approved).
- **The audit writer `shared/audit`:** append-only (create only), the only writer of `audit_logs`,
  always in the caller's `tx` (required), knows no domain. Wired by the composition root, not by a
  default only tests replace. Audited: added, edited, hidden, restored, with stable action names
  `<entity>.<verb>`; a PATCH changing names and the flag writes two entries; a PATCH changing
  nothing writes nothing; reordering writes none.
- **Endpoints:** `GET /admin/governorates` (with areas, hidden included, ordered); `POST`/`PATCH`
  governorates and areas; `GET`/`POST`/`PATCH` amenities; three `PUT …/order` with `{ ids }`.
- **L2:** the admin's lookup lists are unpaginated, recorded as an exception in api-contract §4.
- **L3:** an order is the scope's full id set, applied in one transaction; missing, extra or repeated
  ids → 409 with nothing changed; safe to repeat; 204.
- **L4:** hide and restore are `isActive` in the same `PATCH`; the service derives the audited action.
- **L5:** no new domain codes; a duplicate is 409 `conflict` with `errors.<field> = ["not_unique"]`,
  on the database's unique keys only (governorate `nameAr`; area `nameAr` within its governorate; the
  amenity key). English names not unique: recorded as a finding (approved).
- **L6:** the amenity key is derived from `nameEn` (snake_case) at creation and never changes; a key
  collision, a retired amenity's included, is 409 on `nameEn`; an empty key is 422 on `nameEn`.
- **L7:** a new row goes last in its scope.
- **Fixed:** no delete; both names required; an area's governorate is not editable; no idempotency
  key; hiding a governorate changes none of its areas' flags.
- **Also built:** `parseId` (`shared/validation`), `signedIn` moved to `shared/auth` (used by lookups
  only; finding 25 gets a progress note), `db/uniqueViolation.ts`.
- **Project rules:** no production parameter, option or callback that only tests pass or nothing
  uses; one service / repository / controller per resource (*Growth*); levels (R3); commit subjects
  ≤ 50 characters.

## The split

### Subagent 1 — security, correctness and concurrency (`apps/api` code)

**Its files:** the PR's changes under `apps/api/src` (`shared/auth`, `shared/audit`,
`shared/validation`, `db/`, `modules/lookups`, `app.ts`) and `packages/shared/src/lookups`.

**It reads only:** `docs/backend/security.md` › the access token and *Authorization*;
`docs/backend/conventions.md` §3, §4, §6, §8 (R1–R8, *Transactions*).

**It checks:**
- **Authorization:** can any `/admin` lookups route be reached without the guard (mount order, a
  router mounted elsewhere, a method not covered)? A pending password change is still refused.
- **The audit writer:** truly append-only and in the caller's transaction; an entry can't commit
  without its change, or the change without its entry; `before`/`after` accurate (the row locked
  before it is read); actor id right; no secret or unrelated field in the payloads.
- **Concurrency:** the order check and update under the right locks; an area added during an order;
  two PATCHes on one row; the `max(sortOrder) + 1` race (acceptable if only ties result).
- **Errors:** every unique violation maps to the right field and 409; no P2002 or Prisma error leaks
  as a 500; `parseId` refuses out-of-range and non-decimal ids; validation strips unknown keys
  (`key`, `governorateId` on update).
- **The key derivation** (L6) and its edge cases.
- **Dependencies:** wired by the composition root; no test-only default or parameter.

### Subagent 2 — the tests, the contract, the documents and the conformance

**Its files:** the PR's API and unit test files; `packages/shared/src/lookups` tests;
`docs/api/api-contract.md` §4–§5; the status lines of `conventions.md` and `security.md`;
`docs/plans/v1-mvp.md`; `docs/architecture/findings.md` (content only); the commits; the PR body
(`gh pr view 41 --json body`, read-only).

**It reads only:** `docs/development/testing.md` §1–§4; `docs/api/api-contract.md` §1–§4.

**It checks:**
- **Every endpoint tested as guest 401, USER 403, OWNER 403, ADMIN, and ADMIN with a pending
  change** (testing.md §4). Each refusal and each decision L1–L7 has a test that would fail with
  broken code; titles match assertions; one behaviour in one lane (unit vs api).
- **The rollback test** truly proves that the change and its entry share one transaction.
- **The contract matches the code:** paths, bodies, statuses (201/200/204), response shapes, errors,
  the §4 exception. Nothing documented as built that isn't.
- **The status lines and the plan's "Built" line** are true; finding 25's note is accurate.
- **The commits:** atomic, Conventional, ≤ 50 characters, each a complete unit.

## Your output

Write **one file**, `C:\Users\basel\.prompt\MASAHA_WORKER_B\REVIEW41_REPORT.md`:
1. **A verdict in one line.**
2. **The findings,** most severe first, deduplicated. Each gives the severity, the file and line, the
   scenario and the fix.
3. **"Verified OK":** a short list.

State the total tokens used. Then stop. The owner's analyst verifies the findings and writes the
fixes list.
