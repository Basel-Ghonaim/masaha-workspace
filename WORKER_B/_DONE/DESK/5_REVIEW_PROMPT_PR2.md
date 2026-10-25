# Review — DESK PR 2 (`feat/desk-visits`, #95), one independent reviewer

You are the **independent reviewer** of worker B's DESK PR 2 in Basel-Ghonaim/masaha: the front desk's
visits on the API — the check-in, the check-out and its payment, the unpriced close, the visit's read and
terms — opened by two commits carried from #94's review. Claude Code executed it in another conversation;
you start fresh and trust nothing you have not seen in the code. Find the PR: `gh pr view 95 --json
number,headRefOid,mergeStateStatus`. Write the report to
`C:\dev\masaha\workspace\WORKER_B\DESK\6_REVIEW_PR2_CLAUDE_CODE.md`: first the verdict and the five most
important findings, then the rest. **Work alone — no subagents** (the owner's choice, to save tokens).

## Rules
- **Run from `C:\dev\masaha\app-design`, read only commit objects:** `git fetch origin` and
  `git fetch origin pull/95/head`; base = `origin/main`; `git diff origin/main...<head>`, `git show
  <commit>`, `git show <head>:<file>`. No edits, checkouts, installs, npm or test runs, servers, database
  commands, no GitHub comments. Confirm `gh pr checks 95` is green first; if a lane is red or pending, say
  so and stop. At the end, check the head has not moved.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario,
  severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say what you saw
  in the code and what you only read in the executor's report.** Think like an attacker on every route and
  like a cashier on a weak connection. No praise, no tool attribution, no project skill.

## What the PR must be
The plan `C:\dev\masaha\workspace\WORKER_B\DESK\2_PLAN.md` — **the owner's approval note at its top binds**
(the quote's age at most 5 minutes; the check-out's audit records both the quote time used and the request's
own time; A1: the unpriced close and `VISIT_NOT_PRICED` in this PR) — PR 2 only; the carried items
`0_CARRIED_FROM_94.md` (items 1–5, two commits); the prompts `3_EXEC_PROMPT_PR2.md`, `3b_REBASE_ON_93.md`,
`3c_RESUME_PR2.md` (finding 98 recorded, `occupancy.md` not trimmed — by design); the report
`4_REPORT_PR2.md`: judge every departure and every break.

Look hardest at:
- **Money and its integrity:** the visit's charge (`visitCharge.ts`, rounding, the cap, student prices, a
  shift without a price), the payment never above what is due (`PAYMENT_EXCEEDS_DUE`), part payment and the
  customer found or created by phone, the hand-typed price (`can()`, `receptionMayTypePrices`, the reason
  recorded), the unpriced close; the migration (the reason column, the trigger split) and what the database
  itself refuses.
- **Concurrency and retries:** the idempotency key checked first, under the space's lock (S1); a retried
  check-in and check-out answering the same body; the lock order (no deadlock); a check-out racing another;
  the quote's age; `SPACE_FULL` as a warning that still records the check-in.
- **Authorization and privacy:** every route behind the managed boundary, `requireCan` and `can()` again
  under the lock; reception vs owner; no customer data or count on any public answer (ADR 0002, 0008).
- **The carried commits:** the closure and override inputs proven on the directory side; the override
  refused during a closure and on an unverified space; the staff's answer showing the override only while
  the rule uses it; `SPACE_NOT_OPEN`'s line.
- **The documents:** the contract, the data model, `visits.md`, `desk.md`, `payments.md`, `occupancy.md`,
  conventions, security, `overview.md`, `v1-mvp.md`, finding 98 — true to the code, one home per fact.
- Scope: `apps/api`, `packages/shared`, `docs`, the two errors catalogues; no dependency. Commit subjects
  (≤ 50) and bodies.

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** under the owner's rule — **a serious or large fix: a fix round on this PR; a small one: the next
PR's first commit (PR 3); or a finding to record**; a short "Checked and fine" list; then stop.
