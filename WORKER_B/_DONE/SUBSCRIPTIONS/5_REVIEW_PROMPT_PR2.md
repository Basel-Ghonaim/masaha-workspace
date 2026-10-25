# Review — SUBSCRIPTIONS PR 2 (`feat/subscriptions`, #106), one independent reviewer

You are the **independent reviewer** of worker B's SUBSCRIPTIONS PR 2 in Basel-Ghonaim/masaha: a space's
subscriptions and their money on the API — subscribing a customer (from a package or custom terms, with a
payment that covers old debts oldest first), a subscription's payment, renewing at most once, the statement,
the staff's corrections (the name, A3; the owner's price never below what was paid, S2), ending early — opened
by two commits carried from #102's review (the phone found in any form; the documents and findings 121–123) and
the migration `subscription_terms` (with an index for the balances' visits branch and finding 80 folded).
Claude Code built it in another conversation (phase 1); OpenCode ran the lanes and the real run, set the PR
number and opened the PR (phase 2). You start fresh and trust nothing you have not seen in the code. Find the
PR: `gh pr view 106 --json number,headRefOid,mergeStateStatus`. Write the report to
`C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\6_REVIEW_PR2_CLAUDE_CODE.md`: first the verdict and the five
most important findings, then the rest. **Work alone — no subagents.**

## Rules
- **This is a review, not a Work Item:** run no project skill (no `start-work-item`, no branch).
- **Run from `C:\dev\masaha\app-design`, read only commit objects:** `git fetch origin` and
  `git fetch origin pull/106/head`; base = `origin/main`; `git diff origin/main...<head>`, `git show
  <commit>`, `git show <head>:<file>`. No edits, checkouts, installs, npm or test runs, servers, database
  commands, no GitHub comments. A planner may read in the same worktree: never switch or reset it. Confirm
  `gh pr checks 106` is green first; if a lane is red or pending, say so and stop. At the end, check the head
  has not moved.
- **Read the plan by its parts:** in `2_PLAN.md`, the approval note at its top, §2 for PR 2, §4 D5–D10, D14,
  D15's PR 2 part, §5 S2, S3, S6, S7, S8, §9 *PR 2*, §10, §11 *PR 2*, §13; not PR 1's or PR 3's parts unless a
  finding needs them.
- Report **concrete problems only**, each verified in the code: file and line, the failing scenario,
  severity (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. **Say what you saw
  in the code and what you only read in the executor's report.** Think like an attacker on every route (a
  reception account of another space, a reception account reaching an owner's action, a guessed id), like two
  desks on a weak connection paying and renewing one subscription at once, and like an accountant reading the
  statement a year later. No praise, no tool attribution.

## What the PR must be
The plan `C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\2_PLAN.md` — **the owner's approval note at its top
binds** (§13 as planned; A3 taken: a subscription's name correctable by the staff; the codes' Arabic as Q2
approved them). The carried items `0_CARRIED_FROM_102.md` (1–6) with #102's review `6_REVIEW_PR1_CLAUDE_CODE.md`.
The prompts `3_EXEC_PROMPT_PR2_CLAUDE.md` and `3_EXEC_PROMPT_PR2_OPENCODE.md` (the owner's two-phase split; the
PR kept as one at 74 files by the owner). The report `4_REPORT_PR2.md`: judge every departure — **the renewal's
unique key on (renewalOfId, customerId) instead of renewalOfId alone** (does it still allow one renewal only?);
no "checked by the service" line for the same-customer renewal; a usage-based subscription's payment answering
a balance below zero while it holds credit; custom terms' errors on `custom.endsOn` and `custom.shiftId`; the
tests seen only green before their code (T25, the corrections' not-found, T31 resting on B38) — and every break.
The real run changed the demo data in `masaha_b_dev` as the report says (read only).

Look hardest at:
- **Money:** every amount in agorot, integers; a payment never above a fixed price's due (`PAYMENT_EXCEEDS_DUE`)
  in the service and the database trigger (S2's ceiling); the debt allocated **oldest first**, the same in the
  quote, the subscription and the statement; a renewal paying old debts first; a voided payment counted
  nowhere; the hand-typed price's reason required; `PRICE_BELOW_PAID` at every path that lowers a price; the
  statement's sums equal to the payments it lists.
- **Concurrency and idempotency (D14, S3, S6):** the space's lock around subscribe, pay, renew, correct and end;
  `balancesOf` read under that lock; a renewal at most once under a race (the unique key and its 409); each
  write's idempotency key, a retry answering the same body (S7's "as of now" stated); a renewal's payments
  deriving their keys from the request's (S6).
- **Authorization:** each route under `requireSpaceAccess` and `can()`; the owner-only corrections (the price),
  reception's (the name, A3), ending early by whom the plan says; nothing of another space reachable by id
  (a customer, a package, a subscription, a payment, a shift).
- **The carried items:** each of 1–6 as decided — the phone search in any form (`normalisePhone`, the suffix
  match with the separators); the three documents; the archived file kept for reception; the error's comment;
  findings 121–123; **item 6's index** (`visits_customer_id_closed_idx`: the columns, and whether the
  reported `EXPLAIN` before and after supports it).
- **The migration `subscription_terms`:** created once, nothing dropped, the trigger and constraints as D9
  says, finding 80 folded (S8), the index; applied to both B databases.
- **The documents:** the contract (the routes, the four new codes and their glosses), the data model, ADR
  0015's *Revised* line, conventions, security, `subscriptions.md`, `customers.md`, `payments.md`, `desk.md`,
  `packages.md`, findings 80 and 121–123, the index — true to the code, one home per fact, only what this PR
  built, `#106` where the number goes.
- Scope: `apps/api`, `packages/shared`, `docs`, the web's two errors catalogues. Commit subjects (≤ 50) and
  bodies.

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** under the owner's rule — **a serious or large fix: a fix round on this PR; a small one: the next
PR of worker B (SUBSCRIPTIONS PR 3's first commit, through `0_CARRIED_FROM_106.md`); or a finding to
record**; a short "Checked and fine" list; then stop.
