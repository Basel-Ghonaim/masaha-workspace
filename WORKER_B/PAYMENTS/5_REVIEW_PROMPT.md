# Review — PAYMENTS (`feat/payments`, #114), one independent reviewer

You are the **independent reviewer** of worker B's PAYMENTS PR in Basel-Ghonaim/masaha (build map step 9, the
API): the owner voids a payment with a reason (`POST …/payments/:paymentId/void`), a written-off visit's payment
refused by the database until the write-off is undone (migration `payment_void_guard`), a priced visit closed by
hand with no customer listed uncollected once its payment is voided, and the payments list (`GET …/payments`:
the owner's whole ledger with filters and totals, reception's own today), opened by two commits carried from
#112's review. **Money and authorization:** trust nothing you have not seen in the code. Find the PR: `gh pr
view 114 --json number,headRefOid,mergeStateStatus`. Write the report to
`C:\dev\masaha\workspace\WORKER_B\PAYMENTS\6_REVIEW_CLAUDE_CODE.md`. **Work alone — no subagents.** This is a
review, not a Work Item: run no project skill, no branch.

## Rules

- **Read only, from `C:\dev\masaha\app-design`, commit objects only:** `git fetch origin` and `git fetch origin
  pull/114/head`; base = `origin/main`; `git diff origin/main...<head>`, `git show <commit>`, `git show
  <sha>:<path>` — **pin every read to the head's sha** (another process's fetch may overwrite `FETCH_HEAD`). No
  edits, checkout, switch or reset, no installs, no npm or test runs, no servers, no database commands, no
  comments on GitHub. The only file you write is the report. If a `git` command fails on a `.lock` file, wait
  30 s and retry once.
- First `gh pr checks 114` — a red or pending check: say so and stop. At the end, `gh pr view 114 --json
  headRefOid` again: say whether the head moved.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario (inputs →
  wrong result), severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say
  what you saw in the code and what you only read in the executor's report.** No praise, no tool attribution.
- Think like: a reception account voiding or reading the whole ledger; another space's owner guessing a payment
  id; two owners voiding one payment at once on a weak connection; a void racing a new payment, a write-off, an
  undo, a subscription's correction or a renewal's allocation; an owner reading a month's totals the day a
  payment is voided; a Gaza-midnight edge of the date range.

## What to read

1. The project's rules: `git show origin/main:CLAUDE.md`.
2. The approved plan `C:\dev\masaha\workspace\WORKER_B\PAYMENTS\2_PLAN.md` — **the owner's approval note at its
   top binds and wins** (Q1's correction: only a **priced** manual, customer-less visit is listed uncollected);
   then §1, §2, §3 *What the reading changed*, §4 D1–D10, §5 S1–S7 and *Rules the item touches*, §9, §10, §11,
   §12.2 and 12.5, Appendix A.
3. The carried file `C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\0_CARRIED_FROM_112.md` (items 1–6).
4. The executor's prompt `3_EXEC_PROMPT.md` and report `4_REPORT.md` (same folder): judge **every departure** —
   (1) tests written after their code, their red got by holding back the route or the schema: would each planned
   break really turn its test red? (2) D1's red through B4; (3) an existing uncollected test's fixture gained a
   customer; (4) B16 replaced by B16b; (5) the payments service gaining the clock; (6) `#PRNUM` replaced before
   the real run, **the migration's comment included, and `masaha_b_test`'s `_prisma_migrations` checksum row set
   by hand** — is the migration file on the head exactly what a fresh database applies (CI)? (7) the shared
   `UncollectedVisit` comment. And the executor's note: the payments list allows 92 days both ends included,
   while the check-ins list (the plan's precedent) allows 93 — which is right, and is a finding owed?

## Look hardest at

- **Authorization:** the void `requireCan('payments.void')` before the body, `can()` again under the space's
  lock; the list narrowed by `can()` before any query, reception's `from`/`to`/`recordedById` refused 403;
  another space's payment 404 everywhere; nothing owner-only reachable by reception.
- **The void (D6):** the space's lock, then the payment's row `FOR UPDATE`; a second void answers as it is with
  its first reason and voider and writes no audit; the trigger's written-off check (`FOR SHARE` on the visit)
  and its translation to `VISIT_WRITTEN_OFF`; the lock order against every other desk money write (no
  deadlock).
- **Downstream (D5):** a voided payment counts nowhere — the item's paid and balance, the customer's debt and
  credit, a fixed subscription's price floor, the uncollected visits, the list's totals; nothing else rewritten.
- **The uncollected widening (D8 + Q1):** only priced, customer-less manual visits that owe; unpriced ones and
  open ones never; the auto ones unchanged.
- **The list (D2–D4):** the Gaza-day window (both ends, `to` exclusive internally), the 92-day bound, the order,
  the paging, `meta.totals` over the filter but `voided` and the page, each row's names (no phone), the
  queries' count bounded per page.
- **The migration:** the function equals the payments migration's body plus the one read; nothing else in the
  schema; the trigger unchanged.
- **Carried from #112:** `start()`'s 365-day bound with its test; the five document fixes as decided.
- **Tests:** a behaviour §9 names with no test, or a test that would pass with the bug.
- **The documents:** the contract, data model, conventions, security, `payments.md`, `desk.md`,
  `subscriptions.md`, `announcements.md`, v1-mvp, overview — true to the code, one home per fact, only what this
  PR built, `#114` where the number goes.
- **Scope:** `apps/api`, `packages/shared`, `docs`, and only the two `errors.ts` lines of `VISIT_WRITTEN_OFF`.
  Commit subjects ≤ 50, each with a body.

## Your output

One file: the head, CI's state and whether the head moved; **a one-line verdict** (mergeable / mergeable after
a fix round / not mergeable); the findings, most severe first, each with **where its fix belongs** under the
owner's rule — **a serious or large fix: a fix round on this PR; a small one: worker B's next PR's first commit
(DESK_API, through `0_CARRIED_FROM_114.md`); or a finding to record (170 and on)**; the departures, each judged;
a short "Checked and fine" list. Then stop.
