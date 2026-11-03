# Review — PAYMENTS_STEP10 PR 1 (`feat/payments`), one independent reviewer (Claude Code)

You are the **independent reviewer** of worker A's first PAYMENTS_STEP10 PR in Basel-Ghonaim/masaha, **web only**
(`apps/web`, plus `docs`): the day's words moved to `shared/lib/time`; **the void of a payment** (the owner only) from
the desk's subscription statement (S10) and from the ledger; **the owner's payments ledger** («الدفعات»: today by
default, a Gaza-calendar period up to the server's window, method / kind / staff filters, voided shown or hidden, the
server's totals); and **reception's «دفعاتي اليوم»** (its own payments today, the handover figures). The API is built
and merged (#114); this PR changes **no** `apps/api` and **no** `packages/shared` code. **Money, roles and the
void:** trust nothing you have not seen in the code. Find the PR: `gh pr list --head feat/payments --state open
--json number,headRefOid,mergeStateStatus` (expected #127, head `27bcd1a0`). Write the report to
`C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\6_REVIEW_PR1_CLAUDE_CODE.md`, **as you go** (a section per part).
**Work alone — no subagents.** This is a review, not a Work Item: run no project skill, no branch.

## Rules

- **Read only, from `C:\dev\masaha\app-design`, commit objects only:** `git fetch origin` and `git fetch origin
  pull/<n>/head`; base = `origin/main`; **pin every read to the head's sha** (`git show <sha>:<path>`, `git diff
  origin/main...<sha>`). No edits, checkout, switch or reset, no installs, no npm or test runs, no servers, no
  database commands, no comments on GitHub. The only file you write is the report. A `git` command failing on a
  `.lock` file: wait 30 s, retry once.
- First `gh pr checks <n>` — a red or pending check: say so and stop. At the end, `gh pr view <n> --json
  headRefOid` again: say whether the head moved.
- Report **verified defects only**: file and line at the head, the scenario (user action → wrong result),
  severity (**blocker** — wrong money shown, sent or recorded, a total the web computes that the server answers, a
  role offered what it must not, a void sent without its reason or twice, a page that breaks, a test that cannot
  fail · **should-fix** — a real defect a user can meet, a missing planned test, a document that says something
  false · **nit**), and the fix. "Plausible" when unsure, with why. Say what you **saw in the code** and what you
  only **read in the report**. A point whose own conclusion is "no change needed" is not a finding. No praise.
- **Check the library's defaults before calling a bug** (TanStack Query v5, Radix — `AlertDialog`'s auto focus,
  `onCloseAutoFocus`; react-hook-form; react-day-picker v9; `Intl.DateTimeFormat#formatRange`).
- Do not report what lint, typecheck, Prettier, `check:*` or CI enforce and passed.

## What to read

1. `git show origin/main:CLAUDE.md` — the project's rules.
2. `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\2_PLAN.md`: the **owner's approval note at its top** (binds:
   S10 taken, the ledger opens on today, DI-1 … DI-61 and §9's Arabic approved as written); §2 *Scope* and
   *Acceptance criteria* (PR 1's); §4; §5 (the S-decisions PR 1 uses); §7 *PR 1 — payments*; §8 *PR 1*; §9 *PR 1 ·
   Commit 1* to *Commit 4* (interfaces, words, states); §10 *PR 1* and *Review Focus*; §11 (PR 1's focus); §13's
   *Real run*.
3. `3_EXEC_PROMPT_PR1.md` and `4_REPORT_PR1.md` (same folder). The executor ran **under the owner's autonomy
   rule** (`C:\dev\masaha\workspace\_SHARED\AUTONOMY_2026-10-25.md`): judge **every departure and every decision
   taken without the owner (D1–D12)** — above all **D1** (the void's ability rides on `CustomerFile`'s `owner`, not
   `DeskAbilities`), **D3/D5** (the focus handed on when the «⋯» leaves under it), **D9** (finding 169: the
   react-day-picker calendar now in the site's first download, +84,506 bytes, recorded not fixed — is (c) sound, and
   is the measurement right?), **D10** (the void dialog's first focus) and **D11** (finding 172 recorded).
4. The contract, at the head (`docs/api/api-contract.md`): `GET /manage/spaces/:spaceId/payments` (its query —
   `from`, `to`, the window's limit, `method`, `kind`, `recordedById`, `voided`; reception's rule: today only, its
   own; `meta`'s totals and the voided figures), `POST …/payments/:paymentId/void` (the reason, no idempotency key,
   its refusals), and the shared `paymentsQuerySchema` and types the web imports.

## Look hardest at

- **The void (money):** offered to the **owner only** — in the statement (`voids={owner}`) and in the ledger — never
  to reception, never on a voided row; the reason required and trimmed before it is sent; **no idempotency key**, no
  re-send by the transport (test 4); a 403 / 404 / 409 (already voided) / 429 / lost answer each shown truthfully,
  the dialog not claiming a void that did not happen; after success the statement / ledger / «دفعاتي اليوم» and any
  desk card showing the payment refreshed (which query keys are invalidated, and are any missed — the customer's
  balance, the uncollected card, the subscription card).
- **The ledger's request:** the period on **Gaza's calendar** (never the browser's zone), the server's window
  enforced on the address (a longer range falls back to today, not sent), `recordedById` only for the owner,
  `voided=INCLUDE|EXCLUDE` as the toggle says, page and limit; the filters read from and written to the URL; a
  cleared filter really cleared.
- **The totals:** every figure (total, cash, transfer, count, voided count and amount) **from `meta`**, never summed
  from the rows; the period's words (`periodText`, `formatRange`) right in both languages.
- **«دفعاتي اليوم»:** no range, no `recordedById` sent; the handover figures the server's; voided rows struck and
  not counted; the transfer's helper line on a phone.
- **Roles and routes:** the ledger's page only for the owner (`SPACE_PAGES.payments`), «دفعاتي اليوم» for
  reception; what the page shows when the server refuses (403) — the server is the authority, the UI may only hide.
- **Focus and accessibility:** the void dialog's first focus on the reason (D10) in a real browser's Radix, the
  focus after close (the «⋯» if still there, else the next row / the statement's heading); the «⋯» named with the
  amount and the person; 44 px on touch.
- **The staff filter:** `useStaffPeople` shares `staffKeys.list` (no second request), the deactivated kept, the
  owner named «(أنت)»; finding 166 true.
- **Tests 1–23 (§10 PR 1)** and 6b: present / missing / weaker, and would each fail if its behaviour regressed
  after the code exists.
- **Documents:** `payments.md`, `desk.md`, `space-links.md`, `architecture.md` §2, `overview.md`, findings 162
  (evidence), 165, 166, 169, 172 and the index — true to the code, one home per fact, `#127` where the number goes.
- **Copy:** every new string in both languages, through the catalogue; D6's reuse of `desk.uncollected.today` /
  `yesterday`.
- **Scope:** `apps/web` and `docs` only; commit subjects ≤ 50, each with a body; no `fixup!`, no tool attribution.

## Your output

```
# Review — PAYMENTS_STEP10 PR 1 (#<n>) — Claude Code
Head: <sha> · checks: <green/red> · head moved during the review: <yes/no>
Verdict: <mergeable | mergeable after a fix round | not mergeable>

## Findings (verified defects only, most severe first)
### F1 — <blocker|should-fix|nit> · <title>
- Where: <file>:<line> at <sha>
- Seen in the code: <what>      (or: Only in the report: <what>)
- Scenario: <user action → wrong result>
- Fix: <what to change> · Belongs: <a fix round on this PR | the next PR's first commit | a finding (173 and on)>
(None → "None.")

## Tests 1–23 and 6b (one line each)
## Finding 169 (the first download) as measured and recorded
## Departures and decisions taken without the owner (D1–D12), judged
## Checked and fine
## Not checked, and why
```

Then stop.
