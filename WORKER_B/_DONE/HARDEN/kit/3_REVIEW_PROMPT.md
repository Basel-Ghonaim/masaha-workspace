# Review — PR #86, HARDEN (an independent reviewer)

You are the **independent reviewer** of PR **#86** (`fix/space-api-hardening`, head `e2a34570`) in
Basel-Ghonaim/masaha. It was planned and executed by Claude Code; you are another tool. Write your report
to `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\REVIEW86_<YOU>_REPORT.md` (`<YOU>` = your tool's name in
capitals), in parts: first the verdict and the five most important findings, then the rest.

## Rules
- **Run from `C:\Users\basel\masaha-b`, read only commit objects:** `git fetch origin`; base = `93f152fe`;
  `git diff 93f152fe...e2a34570`, `git show <commit>`, `git show e2a34570:<file>`. No edits, checkouts,
  installs, npm or test runs, servers, database commands, no GitHub comments. **Do not run the tests:**
  CI ran every lane on this head. At the end, check the head has not moved (`gh pr view 86 --json headRefOid`).
- Report **concrete problems only**, each verified: file and line, the failing scenario, the severity
  (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. No praise. No tool
  attribution. **Do not use any project skill.**

## What the PR must be
The plan `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\HARDEN_PLAN.md` (the owner's approval at its top:
S1–S6), the post-merge review it answers
`C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\REVIEW82-83_OPENCODE_REPORT.md`, and the executor's report
`C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\HARDEN_REPORT.md` (judge each of its six departures, the
T2 guest break changed after a stop-and-ask, and S5's guard deleted because it stayed green).
Scope: `apps/api` and `docs` only.

## Look at these, in this order
1. **Security:** `requireSpaceAccess` decides only through `can(…, 'space.read', …)` and answers 404;
   `requireCan` stands **before** `limitRequests`, `validate` and `receiveFile` on all three managed photo
   writes; nothing on `/manage` lost a guard; the services' own `can()` under the lock still decides; no
   admin-only route reachable. Each with the test that proves it.
2. **The transaction:** `ownersFor(spaceId, tx)` required everywhere; `namesFor(…, tx)`; no `Promise.all`
   on a `tx` left in `space.service.ts` or `groupEdit.ts`; anything else in the module still reading
   outside its transaction.
3. **The race helper** `waitingOnLock`: correct query (`datname = current_database()`, polled on its own
   client, not the holder's transaction); its timeout under Vitest's; every former fixed wait converted
   (`git grep` the head for `WAIT_MS`, `aWhile`, `setTimeout(resolve`); a test that starts two requests
   waits for two; can it pass for the wrong reason or flake on a slow CI run?
4. **A1** (the names read on the read's own connection): is it deterministic as written, and would it fail
   if `tx` were dropped? Its assumption that nothing between the space lock and `namesFor` reads `users`.
5. **The tests** T1–T6, U1, U2, A2: each would fail with its planned break; expectations written by hand;
   `spaceAccess.unit.test.ts` really a unit test.
6. **The documents:** the no-hint 404 rule only in `security.md`, the others linking it; `conventions.md`'s
   header and §2's route chain (S3) true to the code; `#82`/`#83` on their lines; the code map without a
   file list; finding 52 Resolved and 59's dated line; D5 recorded; testing §3 rule 7's sentence (S6).
7. The commits: count each subject's characters yourself (≤ 50); each commit a complete unit.

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** (a fix round on this PR / a finding to record); a short "Checked and fine" list; then stop.
