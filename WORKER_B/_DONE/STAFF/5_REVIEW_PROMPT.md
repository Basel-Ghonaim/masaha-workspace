# Review — PR #90, STAFF (an independent reviewer)

You are the **independent reviewer** of PR **#90** (`feat/space-staff`, head `ea56e225`) in
Basel-Ghonaim/masaha: seven commits, a migration, security work on accounts created by someone else. It was
executed by Claude Code in another conversation; the owner chose Claude Code for this review too, so you
start fresh: trust nothing you have not seen in the code. Write your report to
`D:\masahaWorkspace\WORKER_B\STAFF\6_REVIEW_CLAUDE_CODE.md`, in parts as you go: first the verdict and the
five most important findings, then the rest.

## Rules
- **Run from `C:\Users\basel\masaha-design`, read only commit objects:** `git fetch origin` and
  `git fetch origin pull/90/head`; base = `origin/main` (`02b1067a`); `git diff 02b1067a...<head>`,
  `git show <commit>`, `git show <head>:<file>`. No edits, checkouts, installs, npm or test runs, servers,
  database commands, no GitHub comments.
- **First:** `gh pr view 90 --json headRefOid,mergeStateStatus` and `gh pr checks 90`. If the head is no
  longer `ea56e225`, review the new head and say so. CI must be green on the head you review (it was still
  running when this prompt was written); if a lane is red or pending, wait or report that and stop. At the
  end, check the head has not moved.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario,
  severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say what you saw
  in the code and what you only read in the executor's report.** No praise, no tool attribution, no project
  skill.

## What the PR must be
The plan `D:\masahaWorkspace\WORKER_B\STAFF\2_PLAN.md` — the owner's approval note at its top binds (its
amendment included) — and the report `D:\masahaWorkspace\WORKER_B\STAFF\4_REPORT_PR1.md`: judge its five
departures. Scope: `apps/api`, `packages/shared`, `docs`, and in `apps/web` only `receptionSpaces: []` added
to test literals.

## Look at these, in this order — think like an attacker, then beyond the plan
1. **Part A, every account created by someone else:** no reset by email while a temporary password is
   pending — at the request, the check **and** the reset (S2); the email confirmed or corrected only at the
   forced change, 422 elsewhere, the unique key and its rollback; the expiry (7 days) enforced at sign-in and
   at `confirm` under the lock; Google sign-in and Google linking refused while pending (S1). Find a path
   around any of them.
2. **Departure 1 — the test T2 and break B4:** the executor rewrote T2 after B4 stayed green. Does T2 now
   prove the race the guard exists for (settled at the request, pending before the resend)? Could the guard
   be removed with every test still green?
3. **Part B, authorization on the server:** an owner acts only on staff of a space they own; a receptionist
   or another owner gets nothing (and the status codes reveal nothing); new accounts only (B1); deactivate /
   reactivate (the session dies at its next request); re-issue only while pending and refused for an account
   that holds anything else (S5); the 10/hour limit counting the re-issue (S3); the routes' order.
4. **The migration:** the backfill before the `CHECK` (S4), existing rows, the down path (if any), and that
   the schema, the client and the `CHECK` agree.
5. **Commit 7 and the cross-PR trap:** `AdminUserRow.receptionSpaces` made required; every literal on
   `main` fixed. PR #89 (worker A, still open, a fix round coming) will add more literals — note which ones
   the second merge must fix.
6. **Section 10 of the plan (Review Focus)** — the races and inputs no test exercises; take each in turn.
7. **The tests:** each planned test exists and would fail with its planned break; departure 4 (B16 as a
   lookup before the insert) and 5 (seeded settings) sound.
8. Rules: error codes in `packages/shared` and both catalogues; ADR 0009 rule 4's revision; the contract,
   `security.md`, `users.md`, `space-links.md`, findings 84–86 true to the code, one home per fact;
   departure 2 (the `v1-mvp.md` row); commit subjects counted (≤ 50) and bodies saying why.

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** (a fix round on this PR / a later item / a finding to record); a short "Checked and fine" list;
then stop.
