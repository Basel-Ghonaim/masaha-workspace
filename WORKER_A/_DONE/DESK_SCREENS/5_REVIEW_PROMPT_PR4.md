# Review — DESK_SCREENS PR 4 (`feat/subscription-sheet`), one independent reviewer (Claude Code)

You are the **independent reviewer** of worker A's last DESK_SCREENS PR in Basel-Ghonaim/masaha, **web only**
(`apps/web`, plus `docs`): the end sheet full width below 768 px (design system, S12); the desk reading the
space's offered packages; **the subscription sheet** (screen 16) — a new customer then their subscription (two
requests, two keys), or a known customer's new subscription, from a package, a **published week or month price**
(spec D as built in #118: `published: { period, audience, shiftId?, name }`) or «مخصّص» (the owner's terms and
reason), with the prior debts and the payment; and **the renewal** with its debts. It opens with items carried
from #122's review (F1–F4). The API is built and merged; this PR changes **no** `apps/api` and **no**
`packages/shared` code. **Money, idempotency keys and roles:** trust nothing you have not seen in the code. Find
the PR: `gh pr list --head feat/subscription-sheet --state open --json number,headRefOid,mergeStateStatus`. Write
the report to `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\6_REVIEW_PR4_CLAUDE_CODE.md`, **as you go** (a section
per part). **Work alone — no subagents.** This is a review, not a Work Item: run no project skill, no branch.

## Rules

- **Read only, from `C:\dev\masaha\app-design`, commit objects only:** `git fetch origin` and `git fetch origin
  pull/<n>/head`; base = `origin/main`; **pin every read to the head's sha** (`git show <sha>:<path>`, `git diff
  origin/main...<sha>`). No edits, checkout, switch or reset, no installs, no npm or test runs, no servers, no
  database commands, no comments on GitHub. The only file you write is the report. A `git` command failing on a
  `.lock` file: wait 30 s, retry once.
- First `gh pr checks <n>` — a red or pending check: say so and stop. At the end, `gh pr view <n> --json
  headRefOid` again: say whether the head moved.
- Report **verified defects only**: file and line at the head, the scenario (user action → wrong result),
  severity (**blocker** — wrong money shown, sent or recorded, a double customer or subscription, a role offered
  what it must not, a page that breaks, a test that cannot fail · **should-fix** — a real defect a user can meet, a
  missing planned test, a document that says something false · **nit**), and the fix. "Plausible" when unsure,
  with why. Say what you **saw in the code** and what you only **read in the report**. A point whose own
  conclusion is "no change needed" is not a finding. No praise.
- **Check the library's defaults before calling a bug** (TanStack Query v5, Radix, react-hook-form).
- Do not report what lint, typecheck, Prettier, `check:*` or CI enforce and passed.

## What to read

1. `git show origin/main:CLAUDE.md` — the project's rules.
2. `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\2_PLAN.md`: the **owner's approval note at its top** (binds:
   spec D's `published` with the name inside, never a `priceId`); §4 decision 3 (finding 125 (c), no preview); §5
   S4 and S12; §6 **Spec D**; §8 *PR 4* (DI-37, DI-45, DI-50–DI-53); §10 *PR 4 · Commit 1* to *Commit 4* (the
   words table); §11 *PR 4* (tests 69–77) and *Review Focus*.
3. `0_CARRIED_FROM_122.md` (same folder; items 1–4).
4. `3_EXEC_PROMPT_PR4.md` and `4_REPORT_PR4.md` (same folder). The executor ran **under the owner's autonomy
   rule** (`C:\dev\masaha\workspace\_SHARED\AUTONOMY_2026-10-25.md`): judge **every departure and every decision
   taken without the owner**, and the supervisor's provisional choice for **finding 171** (the sheet re-reads the
   prices on opening, the toast states the server's amount, a refused published subscribe keeps the fields and
   re-reads; 171 left Open) — is it built as said, and does it leave a hole?
5. The contract, at the head: `POST …/customers`, `POST …/customers/:customerId/subscriptions` (its three forms,
   `startsOn`, `renewalOfId`, `payment`, `meta.warnings`), the statement's `renewal`, where the prices are read,
   and §6's `CUSTOMER_HAS_DEBT`, `SUBSCRIPTION_ALREADY_RENEWED`, `CUSTOMER_ARCHIVED`, `PHONE_TAKEN`,
   `PAYMENT_EXCEEDS_DUE`, `invalid_choice`. The shared types the web imports.

## Look hardest at

- **Keys (S4):** the new customer and the subscription each with its **own** key, one per intent, kept across a
  retry and a double press, never renewed on an error; a refused subscribe keeps the customer (DI-37) and «حفظ
  الاشتراك» sends the subscription alone with its key; a retry after a lost answer cannot create a second customer
  or subscription.
- **The request (money):** exactly one of `packageId`, `published`, `custom`; a package's request carries only
  its id (no price, DI-50); `published` carries `{ period, audience, shiftId?, name }` with the name in the desk's
  language, never a `priceId`; «مخصّص» carries its terms and the reason, and is offered only when the role may type
  a price; `payment.amountAgorot` is the amount **recorded**, never the form's total by default when the user typed
  less; the due shown = prior debts + the new price; nothing computed that the server answers.
- **The toast:** the parts and the remaining debt **from the answer**, `CUSTOMER_HAS_DEBT`'s warning when in
  `meta.warnings`, the amount charged the server's (finding 171).
- **Dates:** `endOf` (`start + validity − 1`, both days), a week 7 days and a month 30 (spec D, the owner's
  §14.4), on Gaza's calendar; the renewal's start from the statement's `renewal.startsOn`, `null` →
  `SUBSCRIPTION_ALREADY_RENEWED`'s line.
- **Roles:** reception may subscribe from a package and a published price, not type a price; the phone required of
  a **new** customer only while something stays owed (K2), a known one without a phone gets the non-blocking line
  (DI-53).
- **Carried from #122:** F1 — the focus really returns to «⋯» after the edit and the archive dialogs (ref passed,
  tested); F2 — the phone compared once normalised; F3 retitled; F4's test fails under its break.
- **S12:** the sheet `w-full` below 768 px only; the showcase unchanged; finding 101 resolved truthfully.
- **Tests 69–77** (and the carried ones): present / missing / weaker, and would each fail if its behaviour
  regressed after the code exists.
- **Documents:** `desk.md`, `customers.md`, `subscriptions.md`, `packages.md`, `foundation.md` §12, finding 125
  resolved, finding 171 untouched — true to the code, one home per fact, the PR's number where it goes.
- **Scope:** `apps/web` and `docs` only (no `errors.ts` change expected — if changed, why); commit subjects ≤ 50,
  each with a body; no `fixup!`, no tool attribution.

## Your output

```
# Review — DESK_SCREENS PR 4 (#<n>) — Claude Code
Head: <sha> · checks: <green/red> · head moved during the review: <yes/no>
Verdict: <mergeable | mergeable after a fix round | not mergeable>

## Findings (verified defects only, most severe first)
### F1 — <blocker|should-fix|nit> · <title>
- Where: <file>:<line> at <sha>
- Seen in the code: <what>      (or: Only in the report: <what>)
- Scenario: <user action → wrong result>
- Fix: <what to change> · Belongs: <a fix round on this PR | the next PR's first commit | a finding (165 and on)>
(None → "None.")

## Tests 69–77 and the carried tests (one line each)
## Finding 171 as built
## Departures and decisions taken without the owner, judged
## Checked and fine
## Not checked, and why
```

Then stop.
