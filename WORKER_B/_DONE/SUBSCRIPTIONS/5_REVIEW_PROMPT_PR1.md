# Review — SUBSCRIPTIONS PR 1 (`feat/customers`, #102), one independent reviewer

You are the **independent reviewer** of worker B's SUBSCRIPTIONS PR 1 in Basel-Ghonaim/masaha: the space's
customers on the API — create and edit, archive and restore, the customers list (paged, searched, filtered by
subscription status and by payment) and the customer's file, the subscription's derived status and progress,
the debts computed in the database — opened by four commits carried from #100's review (the jobs answering
200 when only stays failed; a desk check-out charged up to the stay's day's end; the documents; the undo's
refusals) and closed by the uncollected visits paged in SQL. Claude Code executed it in another conversation;
you start fresh and trust nothing you have not seen in the code. Find the PR: `gh pr view 102 --json
number,headRefOid,mergeStateStatus`. Write the report to
`C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\6_REVIEW_PR1_CLAUDE_CODE.md`: first the verdict and the five
most important findings, then the rest. **Work alone — no subagents.**

## Rules
- **This is a review, not a Work Item:** run no project skill (no `start-work-item`, no branch).
- **Run from `C:\dev\masaha\app-design`, read only commit objects:** `git fetch origin` and
  `git fetch origin pull/102/head`; base = `origin/main`; `git diff origin/main...<head>`, `git show
  <commit>`, `git show <head>:<file>`. No edits, checkouts, installs, npm or test runs, servers, database
  commands, no GitHub comments. A planner may read in the same worktree: never switch or reset it. Confirm
  `gh pr checks 102` is green first; if a lane is red or pending, say so and stop. At the end, check the head
  has not moved.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario,
  severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say what you saw
  in the code and what you only read in the executor's report.** Think like an attacker on every route (a
  reception account of another space, a reception account reaching an owner's action, a guessed id), like two
  desks on a weak connection editing one customer, and like an owner whose space holds tens of thousands of
  customers. No praise, no tool attribution.

## What the PR must be
The plan `C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\2_PLAN.md` — **the owner's approval note at its top
binds** (§13 Q1–Q11: S1 `subscription_usage`; the nine codes with the Arabic as written, `CUSTOMER_ARCHIVED`
among them; the migrations; S4 `UPCOMING`, S5; S3, S6; finding 113 folded as C6; the list by name, then id);
the carried items `0_CARRIED_FROM_100.md` (items 1–5: findings 114 and 116 resolved, 115 recorded Open); the
prompt `3_EXEC_PROMPT_PR1.md`; the report `4_REPORT_PR1.md`: judge every departure — the two migrations by the
plan's fallbacks (`migrate diff`, a folder by hand); **the list's ids read through `unnest` instead of `=
ANY`** (the measured 45.8 s → 0.2 s at 40,000 ids) and T26 lowered to 20,000 ids with an `ANALYZE` in its seed;
T16–T20 calling the repository's queries; the breaks B25, B36 and C6-d replaced by B25b, B36b, C6-d2; the
archive's *present* check reusing the open reads (`desk` → `subscriptions`); the overdue cap extended to the
quote and the charges so far; the jobs' 500 unit-tested; 84 files in one PR — and every break.

Look hardest at:
- **Authorization:** each customers route under `requireSpaceAccess` and `can()`; archive and restore the
  owner's only, at the route and under the lock; reception refused `?status=ARCHIVED`; nothing of another
  space reachable by id (the customer, its visits, its payments, its subscriptions); a customer's phone only
  through a paged, searched list (no export, no whole list — `OPEN_DECISIONS.md` point 3).
- **Money:** the debts and the payment filter computed in SQL by `payments` alone (decision 6, D5); written-off
  visits and voided payments counted nowhere; the debt in the file equal to the list's; the carried check-out
  cap (`min(quote, due time)`, every path) and what `checkedOutAt` records.
- **The customer:** the phone normalised and unique per space (`PHONE_TAKEN`), the idempotency key on create
  (`customer_key`), a retry answering the same row; edit by both roles; `CUSTOMER_ARCHIVED` where an archived
  customer is used; a present customer not archived (S11); an owing one archived after its confirm (DK-014).
- **Status and progress (D13, S4, S5):** Gaza dates, Saturday-to-Friday weeks, the end date or the total
  whichever comes first, `UPCOMING`, `EXPIRED` at once when ended; `subscription_usage` (S1) agreeing with
  the pure rule.
- **Performance and bounds:** every list paged (api-contract §4), the ids through one parameter, the query
  plans at the plan's scale; the uncollected visits paged in SQL (finding 113); no read of every row into
  memory.
- **The migrations:** created once, applied to both B databases, nothing dropped, the functions and indexes as
  D3 and D9 say.
- **The documents:** the contract (customers, the codes' glosses), the data model, conventions §5, §9, §13,
  security, ADR 0009's rows and ADR 0015's line, `payments.md`, `visits.md`, `desk.md`, the customers'
  document, `v1-mvp.md`, `overview.md`, findings 114–116, 120 and the index — true to the code, one home per
  fact, only what this PR built.
- Scope: `apps/api`, `packages/shared`, `docs`, the web's two errors catalogues. Commit subjects (≤ 50) and
  bodies.

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** under the owner's rule — **a serious or large fix: a fix round on this PR; a small one: the next
PR of worker B (SUBSCRIPTIONS PR 2's first commit, through `0_CARRIED_FROM_102.md`); or a finding to
record**; a short "Checked and fine" list; then stop.
