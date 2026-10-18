> **Approved by the owner, 2026-10-17:** every decision in §1 as written. Planner: Claude Code.

# HARDEN — the spaces API after #82 and #83: the owner names' lock, one access rule, the missing tests, the race helper — PLAN ONLY

**No branch, no checkout, no file edit in the repository, no commit, no install, no test run, no
server, no database command.** You write one file — the plan — then stop.
**No trial build anywhere either:** no temporary copy of the repository, no `git worktree add`, no
`git stash`, no scratch or temp folder holding code, no `node` / `tsx` / `tsc` / `vitest` / `psql` /
`npm` run — not in the repository, not in a scratchpad, not in a temp directory. The only commands are
`git fetch`, `git show`, `git log`, `git ls-tree`, `git grep`, read-only `gh`, and reading files. You
plan by reading; the executor proves the plan by its red runs. Where you are unsure that something
works (a test's determinism, a `pg_stat_activity` query, a middleware's order), write it in the plan as
**a check the executor makes first, with what to do if it fails** — never try it yourself. Read only
the files the plan needs, each once.
**Plan:** `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\HARDEN_PLAN.md`.
If you are Claude Code: use `write-plan` for its discipline; otherwise follow §0.

**Where you read.** Worker A is executing GALLERY in `C:\Users\basel\masaha` — never work there. Work in
`C:\Users\basel\masaha-b` (detached, clean; never check anything out): `git fetch origin`, then read only
`origin/main`'s commit objects — `git show origin/main:<path>`, `git ls-tree -r --name-only origin/main <dir>`,
`git grep <pattern> origin/main -- <paths>`.

## 0. The plan must stand alone

A fresh conversation executes it — possibly OpenCode, Copilot or Codex — from the latest `origin/main`;
another tool reviews. So: every decision with its one-line reason; the files; each new function or
middleware with its interface; each test with its lane, title and the break that must make it fail
(`docs/development/testing.md` §3 rule 7 — **every break run and its red output recorded in the
report**); the commits, subjects counted (≤ 50); a fix before the push folds into its commit
(`git commit --fixup` + `git rebase -i --autosquash`, with `GIT_SEQUENCE_EDITOR=:`); every new decision
and history line ends with its date and **the PR's number** (issues and PRs share one sequence — the
executor checks the next number before the push); the procedure with its commands (branch
`fix/space-api-hardening` from the latest `origin/main` in `C:\Users\basel\masaha-b`; ports 3321/5321;
B's databases `masaha_b_dev` / `masaha_b_test`; Docker by `docker start masaha-postgres-1`, never
`db:up`; **one full test run at a time on this machine** — check worker A's folder runs none; `lint`,
`typecheck`, `test:unit`, `test:api`, `format:check`, `check:links`; push;
`gh pr create --assignee @me --label fix --label area:api --label area:docs` with the description
written out; `gh pr checks` and `CLEAN`; the conflict check with `git merge-tree --write-tree` against
any open PR — GALLERY will be open and both touch `docs/features/spaces.md` and `space-links.md`: a
documents-only conflict takes the fast path; the report to
`C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\HARDEN_REPORT.md`, UTF-8, written in parts); a
**"Stop and ask"** list; an appendix mapping steps to Claude's skills, "only a map". No step may depend
on a Claude skill. Never merge; no tool attribution; stage by path.

## 1. The task — the owner's decisions (2026-10-17)

Source: `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\REVIEW82-83_OPENCODE_REPORT.md` (17 findings,
`R82-83-001`…`017`) — read it whole; it is the evidence. Settled:

- **D1 — the owner names inside the transaction (R001, R009):** `users.namesFor(…, tx)` in
  `ownersFor`; `ownersFor(spaceId, tx: Tx)` with `tx` required. Then the sentence "the names are read
  under the space share lock" becomes true.
- **D2 — one statement at a time on a transaction (R002):** sequential reads in `space.service.ts`
  `get` and the two places in `facts/groupEdit.ts`.
- **D3 — the boundary decides through `can()` (R003):** `requireSpaceAccess` refuses with 404 when
  `can(actor, 'space.read', { links })` is false — no second copy of the staff rule.
- **D4 — one `requireCan(action)` middleware (R006, R007):** in `shared/auth` beside `requireRole`;
  replaces the inline `can('space.read')` copies in the two manage routers, and stands **before**
  `limitRequests` / `receiveFile` on the managed photo writes, so a reception upload is refused before
  the file is read. The services' own `can()` under the lock stays authoritative.
- **D5 — reception receives the owners' names and ids, as built (review D-a, option A):** recorded as a
  decision in `docs/features/spaces.md`; revisit when staff (step 5b) lands.
- **D6 — the missing tests (R012, R013, R014, and #83's planned 3, 8, 9, 11, 12):**
  - the managed read's **payload** for owner and reception (`owners`, `isVerified`, the fact groups);
  - an unknown and a non-numeric id on `/manage/spaces/:spaceId` → 404; a guest → 401;
  - a **hidden** linked space stays manageable;
  - a **429 before the file is read** on a photo upload (the limiter's order);
  - a link change racing a managed write, decided under the space lock (#83's test 12), on D7's helper;
  - the owner names read inside the transaction — the review's deterministic form (rename the owner's
    user inside the holder transaction; the GET must answer the committed name). **If no lane can make
    it fail deterministically, record finding 71 instead and say so;**
  - `spaceAccess.api.test.ts` → `spaceAccess.unit.test.ts`, keeping only the transaction-identity case.
- **D7 — finding 52 resolved here:** one race helper that waits until the request is seen waiting on a
  lock (`pg_stat_activity.wait_event_type = 'Lock'` for its backend), with a timeout, used by every race
  test (`apps/api/test/locks.ts` and `sessionLock.api.test.ts`'s own helper). Resolve finding 52.
- **D8 — the deliberate breaks of #83, run now:** reception refused on every write, no link → 404, the
  admin refused on `/manage`, the lock-aware decision — each made once, seen red, restored; recorded in
  the report (`MANAGE_REPORT.md` has none).
- **D9 — the documents (R004, R005, R008, R010, R011, R016, R017):** `conventions.md`'s status header;
  `v1-mvp.md:223`'s row (`:group`, as the contract writes it); the no-hint 404 rule kept in
  `security.md` (and the contract's endpoint lines), every other document **links** it; `#82` / `#83`
  on their decision and history lines; *Last Updated* on every document edited; `spaces.md`'s code map
  back to folders, no file list; finding 59 gains one dated line ("2026-10-15, #82: the API half
  landed") and stays Open.
- **Not in this item:** R015 (a report outside the repository — D8 replaces its missing evidence);
  anything in `apps/web`; packages, staff, capacity (step 5b and later); finding 69 (A records it).

**If the plan finds more than about 40 files, or a decision the owner must take, propose it in
"Decisions needed" — do not decide alone.**

## 2. Read first (from `origin/main`)

`CLAUDE.md`; `docs/development/workflow.md`; `docs/development/testing.md`; `docs/backend/conventions.md`
(§8 transactions, space access, concurrency); `docs/backend/security.md`; `docs/api/api-contract.md` ›
managed spaces and photos; `docs/features/spaces.md`, `docs/features/space-links.md`;
`docs/architecture/documentation.md` (one home per fact; decisions carry date and PR); ADR 0002, 0009;
findings 11, 43, 52, 59; the plans `MASAHA_WORKER_B\PLAN\OWNERSREAD_PLAN.md` and `MANAGE_PLAN.md` (their
planned tests and breaks); the code the review names, file by file.

## 3. Findings

New findings this item may record: **71–72** (OWNERSREAD's reserved numbers) and **75–76** (MANAGE's).
They are **finding** numbers in `docs/architecture/findings/`, **not** GitHub Issues.

## 4. Boundaries

`apps/api` and `docs` only; nothing in `packages/shared` (if a change there is needed, stop and say so)
and nothing in `apps/web`. No schema change, no migration.
