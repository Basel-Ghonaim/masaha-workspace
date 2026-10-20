# Review — DESK PR 3 (`feat/auto-checkout`, #97), one independent reviewer

You are the **independent reviewer** of worker B's DESK PR 3 in Basel-Ghonaim/masaha: the scheduler and the
auto check-out on the API — the jobs port (a local timer, a secret-protected endpoint for an external cron),
closing open stays at their due time, pricing an unpriced visit, the uncollected visits — opened by a commit
carried from #95's review. Claude Code executed it in another conversation; you start fresh and trust nothing
you have not seen in the code. Find the PR: `gh pr view 97 --json number,headRefOid,mergeStateStatus`. Write
the report to `C:\dev\masaha\workspace\WORKER_B\DESK\6_REVIEW_PR3_CLAUDE_CODE.md`: first the verdict and the
five most important findings, then the rest. **Work alone — no subagents.**

## Rules
- **Run from `C:\dev\masaha\app-design`, read only commit objects:** `git fetch origin` and
  `git fetch origin pull/97/head`; base = `origin/main`; `git diff origin/main...<head>`, `git show
  <commit>`, `git show <head>:<file>`. No edits, checkouts, installs, npm or test runs, servers, database
  commands, no GitHub comments. Confirm `gh pr checks 97` is green first; if a lane is red or pending, say
  so and stop. At the end, check the head has not moved.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario,
  severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say what you saw
  in the code and what you only read in the executor's report.** Think like an attacker on the jobs endpoint
  and like an owner reading the money a day later. No praise, no tool attribution, no project skill.

## What the PR must be
The plan `C:\dev\masaha\workspace\WORKER_B\DESK\2_PLAN.md` — **the owner's approval note at its top binds**
(A1: the unpriced close was #95's; PR 3 keeps the reads and the pricing) — PR 3 only; the carried items
`0_CARRIED_FROM_95.md`; the prompt `3_EXEC_PROMPT_PR3.md`; the report `4_REPORT_PR3.md`: judge every
departure (the job registered as two; the reworded breaks; `priceVisitSchema` moved to `visits`; the pricing
route's `requireCan`) and every break.

Look hardest at:
- **The jobs endpoint and secret:** comparison in constant time, refusal without or with a wrong secret
  (and what it reveals), the secret required in production, never logged; the local timer; the rate.
- **The auto check-out:** a stay closed at its **due time** (closing time or the stay limit), never the run's
  time; idempotent and catching up; days the space is closed, a stay over midnight, a settings change between
  check-in and the run; Gaza time; visits and subscription check-ins both; one job's failure not undoing the
  other's closings; locks and races with a desk's check-out at the same moment.
- **Pricing an unpriced visit:** who may (`can()`, `receptionMayTypePrices`, the required reason), once only
  (`VISIT_ALREADY_PRICED`), audited.
- **The uncollected visits:** the definition (data model), the balance composed without repeating it
  (conventions §5, §9), paging, scoped to the space, staff only.
- **The carried commit:** the check-out before its check-in refused (422); the lost-race payment refused
  (409 `VISIT_ALREADY_CLOSED`, a request without a payment unchanged); finding 100; the two documents. Judge
  the executor's leaving nits 7–10 of #95's review undone.
- **The documents:** the contract (*Internal*), conventions, security, setup's runbook, `.env.example`,
  `visits.md`, `desk.md`, `payments.md`, `overview.md`, `v1-mvp.md` — true to the code, one home per fact.
- Scope: `apps/api`, `packages/shared`, `docs`, the two errors catalogues; no dependency, no migration.
  Commit subjects (≤ 50) and bodies.

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** under the owner's rule — **a serious or large fix: a fix round on this PR; a small one: the next
PR's first commit (DESK PR 4); or a finding to record**; a short "Checked and fine" list; then stop.
