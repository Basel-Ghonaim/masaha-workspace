# Review — PR #62 (USERS: suspension, role and the admin's temporary password, API)

You are an **independent reviewer** of PR #62 in the Masaha repository (Basel-Ghonaim/masaha).
Write your report to `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\REVIEW62_<YOU>_REPORT.md`, where
`<YOU>` is your tool's name in capitals (`CLAUDE`, `CODEX`, `COPILOT`, `OPENCODE`).

## Rules

- **Run from `C:\Users\basel\masaha`** (the main folder), never `masaha-b` (worker B's) or
  `masaha-design`.
- **Read-only.** No edits, commits, checkouts, switches, installs, npm or test runs, database or
  Docker commands, and no GitHub comments. Read only from commit objects: `git fetch origin`, then pin
  to **the PR's current head**: `gh pr view 62 --json headRefOid`, written at the top of your report;
  check it again at the end, and if it changed, say so. Base: `d7d800e`. Use
  `git diff d7d800e...<head> -- <paths>` and `git show <head>:<file>`.
- **You are the independent review.** An earlier review was written by the conversation that built
  the PR, and its fixes are in. Do not read `REVIEW62_CLAUDE_REPORT.md` or the PR's comments until
  your own findings are written; then you may check whether you missed anything it found.
- **Report concrete problems only,** each verified in the code: file and line, the failing scenario
  (input or interleaving → wrong result), the severity (**blocker / should-fix / nit**) and the fix.
  No praise, no summary. If unsure, say "plausible" and why.
- **No tool attribution** in what you write.

## What the PR must be (the owner's decisions)

API only (plus four error codes' lines in the web's two catalogues). 5 commits, no schema
change, no dependency. The approved plan is `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\USERS_PLAN.md`
(with its reply `PROMPT\USERS_PLAN_REPLY.md`); the worker's report is `REPORT\USERS_REPORT.md`.
- **D7 (commit 1, docs only):** workflow §9 *Merging* — a merge into `main` that deletes or renames
  no file and changes none of the PR's files needs no rebase and no new CI run.
- **D5 — the guard reads the account** (ADR 0003 and ADR 0002 revised): `requireAuth` takes an
  account reader wired by the composition root, one primary-key read per signed-in request. Order: no
  valid token → 401; no account → 401; suspended → **401, no code**; the account pending a change
  while the token is not (a temporary password issued after the token) → **401, no code**, on every
  route; the token pending → 403 `PASSWORD_CHANGE_REQUIRED` unless the route allows it. The
  token no longer carries `role`; `req.auth.role` is the stored role, which `requireRole` and `can()`
  read.
- **Suspension** — `PUT /admin/users/:userId/suspended` `{ isSuspended }`, 204, idempotent, audited;
  suspending ends every session and every pending reset link; the links are kept (the space stays
  verified). A password change checks the suspension under the session lock (S4).
- **The admin-set lock:** one statement locking the target and every active admin, by id
  (`FOR NO KEY UPDATE`); refusals `OWN_ACCOUNT` (oneself, before any lock) and `LAST_ADMIN` (no
  active admin would remain).
- **Role** — `PUT /admin/users/:userId/role` `{ role: USER | ADMIN }`, in `space-links` (L2), 204,
  idempotent, audited, ending sessions; refused `ACCOUNT_HAS_LINKS` while the person holds any active
  link (a deleted space's included), and for `USER` on an `OWNER`.
- **The admin's temporary password** — `POST /admin/users/:userId/temporary-password`, 200
  `{ temporaryPassword }`, `no-store`, `mustChangePassword`, every session and reset link ended,
  audited without it; refused for oneself, a suspended account (`ACCOUNT_SUSPENDED`), a Google-only
  account (`GOOGLE_ONLY_ACCOUNT`); issuing again replaces the pending one (finding 49 resolved).
- **Finding 51** recorded (open): an access token outlives the end of its session after a password
  change or reset.

## Look at these, in this order

1. **The guard (D5), on every signed-in route:** any route or helper still reading the role or the
   pending flag from the token; any path that skips the reader (the refresh, the links loader, the
   general rate limit, the request log); a suspended account reaching anything; a demoted admin
   keeping `/admin`; the order of the checks; the 401 versus 403 choices and what the web does with
   each (`apps/web` transport: `refreshOn401`, `refresh`).
2. **The admin-set lock:** the statement's correctness under read committed (re-checked rows, a
   concurrent promotion), its lock order against every other path (sign-in, refresh, password change,
   link/unlink, facts save, the handover, the temporary password) — any deadlock; `LAST_ADMIN`
   reachable as claimed; `OWN_ACCOUNT` before the lock.
3. **Revocation:** suspension, role change and the temporary password each end the sessions and
   reset links in the same transaction, after the write; an idempotent repeat ends none; restore ends
   none. The worker reports two planned breaks did not fail alone (the revocation runs after the row
   update anyway) — judge whether the tests still prove what their titles say.
4. **The temporary password:** generation reused from #60; never in a log, audit `after`, error or
   Prisma argument; `no-store`; Google-only detection (an account with Google **and** a password gets
   one); replacing a pending one; a race with a password change or a suspension.
5. **Authorization:** each new route behind `/admin`'s guard; refused as guest, USER, OWNER and an
   ADMIN with a pending change; `ACCOUNT_HAS_LINKS` counting exactly what the global role counts.
6. **Module levels:** `users` (L1) imports nothing above it; `shared/` imports no module; the role
   change in `space-links` (L2) uses `users` only through its index.
7. **The tests:** each would fail if its code broke; the races really interleave; the **temporary
   database trigger** in `lookups/governorates/governorates.api.test.ts` is always dropped (a failure
   between create and drop must not leave it for other files); the two new helpers are test-only and
   live under `test/`; expectations written by hand.
8. **The documents:** ADR 0003 and ADR 0002 *Revised* lines, security.md (Built line, tokens, the
   guard, revocation, recovery), conventions §13, api-contract (the three routes, the guard's 401,
   `/me/password`, §6), users.md, space-links.md, the plan's API table, overview's *Built*, findings
   49 (resolved) and 51 (new) and the index, workflow §9 and `open-pr` step 3 — each states the code
   truly, one home per fact.
9. **The commits:** five; count each subject (≤ 50).

## Your output

One file (the path above): a one-line verdict; the findings, most severe first (severity, file:line,
scenario, fix); a short "Checked and fine" list; then stop.
