# Review — PR #44 (S2b-1: the admin's spaces API and the public lookups read)

You are the **independent reviewer** of PR #44. Run from `C:\Users\basel\masaha` (the main folder).
You don't build, fix or merge.

## Budget (hard limits — the owner's)

- **At most 2 subagents. Never a third,** not even an empty one. No workflows.
- **Do not run Superpowers' workflow skills** (brainstorming, subagent-driven development,
  requesting-code-review, worktrees, finishing a branch): this prompt is the owner's explicit
  instruction to skip them.
- **The whole review stays under 600,000 tokens**, this conversation and both subagents together.
  Aim for about 200,000 per subagent.
- **Read the diff, not the repository.** Use `git diff c9db4d8...92d04ba -- <paths>` and
  `git show 92d04ba:<file>`, only for files the PR changes, plus the few named below.
- **Read the documents only in the sections named.**
- **Reports:** at most 700 words per subagent, and at most 900 for yours.

## Rules

- **Read-only.** No edits, commits, checkouts, switches, installs, npm or test runs, dev servers,
  database or migration commands, or GitHub comments. Another worker may be using the main folder's
  working tree: read only from commit objects. Run `git fetch origin` first if `92d04ba` is missing.
- **Pin everything to commit `92d04ba`**, compared with its base `c9db4d8`. Prefix `git show` with
  `MSYS_NO_PATHCONV=1` if a path is mangled.
- **Report concrete problems only:** the file and line, the failing scenario, the severity
  (blocker / should-fix / nit) and the fix. **Verify each in the code before reporting it;** drop
  anything speculative.

## What the PR must be (the owner's decisions)

API only (plus one stated web exception): build step 2's admin spaces, first of four items.
- **S1 — the name rule flips:** a space's English name is required, the Arabic optional (migration:
  fill a missing `name_en` from the slug, then `NOT NULL`; `name_ar` nullable; two optional landmark
  columns, `landmark_ar` / `landmark_en`). The shared `ManagedSpace` follows; the web space switcher's
  name fallback is the one approved web edit.
- **S2 — the slug:** derived from the English name, kebab-case, a numeric suffix on collision,
  **soft-deleted spaces included** (never reused), never changed; a unique-violation race retries the
  transaction (up to 3 attempts).
- **S3 — the location** is required at creation and refused outside the Gaza Strip box with a margin
  (`out_of_range`), by a shared pure helper.
- **S4 — the admin's list is paginated** (api-contract §4).
- **S5 — `GET /lookups`** (public): active governorates with their active areas, active amenities, in
  order, unpaginated (an exception recorded in §4).
- **S6 — a link to a soft-deleted space no longer counts** in the session's links and the user's
  spaces (resolves finding 18); deleting writes nothing in `space_managers`.
- **S7 — the admin may hide, unhide, soft-delete and restore any space;** only the profile (and later
  the facts) is limited to unverified spaces (`can('space.profile.update')`).
- **S8 — "stale" is computed on the server** from the platform's thresholds, per fact group.
- **S9 — the admin's and the owner's edits are separate endpoints over one service logic;** only the
  admin's is built.
- **Approved during planning:** `POST /admin/spaces/:spaceId/restore` (audited `space.restored`);
  `paragraphSchema` in `@masaha/shared/core` for the two descriptions (line breaks allowed, nothing
  else relaxed); "last update" = the latest of the five group dates; finding 36 (a new space's empty
  groups count as fresh).
- **Creation:** one transaction, flat sequential writes (the space, then its settings copied from
  `newSpaceDefaults` through `platform-settings` and `space-settings`, then the audit); nothing
  written if the defaults are missing or invalid; resolves finding 11.
- **The admin's list is composed by `space-links`** (conventions §9): the verified filter resolves to
  ids first, then `spaces` filters and paginates, then owners and area names are added, one query per
  module.
- **The links loader** on `/admin/spaces/:spaceId` **without the refusal** (conventions §8), so
  "verified" is known; `spaces` never imports `space-links`.
- **Project rules:** levels R1–R8 (a module imports only lower levels, through `index.ts`); **no
  parameter, option or callback that only tests pass or nothing uses** — a service creates its own
  repository, the composition root passes only real dependencies (finding 31); every write audited in
  its own transaction; one service / repository / controller per resource; commit subjects ≤ 50.

## The split

### Subagent 1 — security, data integrity and correctness (`apps/api`, `packages/shared`)

**Its files:** the PR's changes under `apps/api/src` (`shared/auth`, `modules/spaces`,
`modules/space-links`, `modules/platform-settings`, `modules/space-settings`, `modules/lookups`,
`modules/users`, `app.ts`), `apps/api/prisma` (the schema and the migration), and
`packages/shared/src` (`spaces`, `space-links`, `lookups`, `core`).

**It reads only:** `docs/backend/conventions.md` §2–§9 and §13; `docs/backend/security.md` ›
*Authorization*; `docs/architecture/data-model.md` › *Spaces* and *Derived values*.

**It checks:**
- **Authorization:** every `/admin/spaces*` route behind the `/admin` guard; the non-refusing loader
  can't be mounted where a refusal is needed or reached by a non-admin; the profile edit refused on a
  verified space; nothing lets an owner act through the admin's routes; `GET /lookups` exposes only
  active rows and no admin-only field.
- **Finding 18:** links to deleted spaces dropped everywhere the session and the dashboard read them
  (the session's links, `mySpaces`, the space role guard's data), restore brings them back.
- **The migration:** correct and safe on existing rows (the backfill, `NOT NULL`, nullable, new
  columns), and nothing else in the schema changed.
- **Creation:** the defaults copied in the same transaction; rollback when they are missing; the slug
  rule, deleted spaces counted, the retry bounded and safe; the Gaza box and its margin; the area must
  be active with an active governorate.
- **The composed list:** filtering before paginating (full pages, right totals), the verified and
  hidden states consistent, the stale rule identical in the row and the filter, no N+1, search
  safe (no injection, case-insensitive in both languages).
- **Writes:** hide, delete and restore idempotent; the audit entries and their payloads (no secret,
  correct actor and `spaceId`); `paragraphSchema` relaxes only line breaks.
- **Levels and dependencies:** R3 respected; no test-only default or parameter.

### Subagent 2 — the tests, the contract, the documents and the conformance

**Its files:** the PR's test files (`*.api.test.ts`, `*.unit.test.ts`), the web change under
`apps/web/src/features/space-links`, `docs/` (api-contract.md §4–§5, data-model.md, localisation.md,
conventions.md and security.md status lines, `v1-mvp.md`, findings.md), the commits, and the PR body
(`gh pr view 44 --json body`, read-only).

**It reads only:** `docs/development/testing.md` §1–§4; `docs/api/api-contract.md` §1–§4.

**It checks:**
- **Every protected endpoint tested as a guest, a USER, an OWNER of another space, the OWNER of this
  space, the ADMIN, and an admin with a pending password change** (testing.md §4).
- **Each decision S1–S9 and each approved addition has a test that would fail with broken code;**
  titles match assertions; one behaviour in one lane. Judge finding 11's test honestly (the PR says it
  is a guard, not a reproduction): is the claim in the finding's resolution true and sufficient?
- **The contract matches the code:** paths, bodies, statuses, shapes, errors, the §4 exceptions.
- **The documents state the code truly:** the name rule in data-model.md, the status lines, the
  "Built" lines, findings 11, 18 and 36; nothing claims more than is built.
- **The web exception** is minimal and correct (the switcher's fallback, `lang` on the English name).
- **The commits:** atomic, Conventional, ≤ 50 characters, each a complete unit.

## Your output

Write **one file**, `C:\Users\basel\.prompt\MASAHA_WORKER_A\REVIEW44_REPORT.md`:
1. **A verdict in one line.**
2. **The findings,** most severe first, deduplicated. Each gives the severity, the file and line, the
   scenario and the fix.
3. **"Verified OK":** a short list, grouped by the two subagents' areas.

State the total tokens used. Then stop. The owner's analyst verifies the findings and writes the
fixes list.
