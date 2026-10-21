# Review — DESK PR 4 (`feat/visit-debts`, #100), one independent reviewer

You are the **independent reviewer** of worker B's DESK PR 4 in Basel-Ghonaim/masaha: collecting a visit's
debt and writing one off, on the API — a payment after the check-out on the general `POST …/payments`,
«تسجيل دينًا» (`PUT …/visits/:visitId/customer`), the owner's write-off and its undo, the ledger trigger's
fourth rule — opened by two commits carried from #97's review (every stay closed by its day's end; the jobs
keep closing past a failing stay). Claude Code executed it in another conversation; you start fresh and trust
nothing you have not seen in the code. Find the PR: `gh pr view 100 --json number,headRefOid,mergeStateStatus`.
Write the report to `C:\dev\masaha\workspace\WORKER_B\DESK\6_REVIEW_PR4_CLAUDE_CODE.md`: first the verdict
and the five most important findings, then the rest. **Work alone — no subagents.**

## Rules
- **Run from `C:\dev\masaha\app-design`, read only commit objects:** `git fetch origin` and
  `git fetch origin pull/100/head`; base = `origin/main`; `git diff origin/main...<head>`, `git show
  <commit>`, `git show <head>:<file>`. No edits, checkouts, installs, npm or test runs, servers, database
  commands, no GitHub comments. Another review may read in the same worktree: never switch or reset it.
  Confirm `gh pr checks 100` is green first; if a lane is red or pending, say so and stop. At the end, check
  the head has not moved.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario,
  severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say what you saw
  in the code and what you only read in the executor's report.** Think like an attacker on every route and
  like a cashier and an owner on a weak connection, at the same visit. No praise, no tool attribution, no
  project skill.

## What the PR must be
The plan `C:\dev\masaha\workspace\WORKER_B\DESK\2_PLAN_PR4.md` — **the owner's approval note at its top
binds** (§13 Q1–Q7; the Arabic as written; findings 110–113); the carried items `0_CARRIED_FROM_97.md`
(items 1–7; item 2 the owner's choice (b), widened); the prompt `3_EXEC_PROMPT_PR4.md`; the report
`4_REPORT_PR4.md`: judge every departure (`balanceOfVisit` for one visit; `customerFor` comparing the stored
phone; D1/D2's red through B5/B6; the schema edited by hand) and every break — **including the full API lane
killed for memory and CI as its judge, under the owner's standing rule**.

Look hardest at:
- **Money:** a payment only on a closed, priced, not written-off visit, never above the balance; the
  written-off refusal in the ledger trigger (S1) and the race with a write-off; the unpaid part's phone and
  the customer kept (finding 100 folded); a retry's answer (S5); idempotency keys.
- **The write-off and its undo:** owner only (`can()` at the route and under the lock), only the remainder,
  a required reason, the `CHECK` (together, non-blank, closed and priced), audited both ways, a second one
  harmless; the uncollected visits and the customer's debt leaving it out; ADR 0009's new row.
- **«تسجيل دينًا»:** the space's customer found or created by phone under the lock; `VISIT_HAS_CUSTOMER`;
  `VISIT_ALREADY_PAID`; written-off refused.
- **The carried commits:** every stay due by 23:59 of its check-in's Gaza day (the three branches); the jobs
  continuing past a failing stay and answering 500 when any failed; findings 111–113 and #95's nit 9.
- **The migration:** created once, the trigger's function copied whole with only the new rule added, both
  databases.
- **The documents:** the contract, the data model, conventions §9 and §13, security, `payments.md`,
  `visits.md`, `desk.md`, `v1-mvp.md` (step 7 and 9's lines), `overview.md`, finding 110 — true to the code.
- Scope: `apps/api`, `packages/shared`, `docs`, the two errors catalogues. Commit subjects (≤ 50) and bodies.

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** under the owner's rule — **a serious or large fix: a fix round on this PR; a small one: the next
PR of worker B (SUBSCRIPTIONS PR 1); or a finding to record**; a short "Checked and fine" list; then stop.
