# Review — DESK_SCREENS PR 3 (`feat/customers-file`, #122), a light review on six axes (Claude Code)

You are the **independent reviewer** of worker A's PR 3 in Basel-Ghonaim/masaha, **web only** (`apps/web`, plus
`docs`): the space's customers list («الزبائن», screen 14), a customer's file («ملف الزبون», screen 15), edit /
archive / restore a customer, a subscription's statement and its early end, and the sign-in page saying a session
ended for idleness; plus two items carried from #119's review (F1, F2). The API is built and merged; this PR
changes **no** `apps/api` and **no** `packages/shared` code. Head expected `358765e3`, 81 files, 7 commits, CI
green. Write the report to `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\6_REVIEW_PR3_CLAUDE_CODE.md`, **as you
go** (a section per axis). **Work alone — no subagents.** This is a review, not a Work Item: run no project skill,
no branch.

**This is a light review, on purpose:** only the six axes below. Do not review copy wording, visual layout, CSS,
documentation style, file naming or anything lint, typecheck, Prettier, `check:*` or CI enforce. Do not read the
whole plan. A clean axis is one line ("✔ seen: …"), not a paragraph.

## Rules

- **Read only, from `C:\dev\masaha\app-design`, commit objects only:** `git fetch origin` and `git fetch origin
  pull/122/head`; base = `origin/main`; **pin every read to the head's sha** (`git show 358765e3:<path>`, `git diff
  origin/main...358765e3 -- <path>`). No edits, checkout, switch or reset, no installs, no npm or test runs, no
  servers, no database commands, no comments on GitHub. The only file you write is the report. A `git` command
  failing on a `.lock` file: wait 30 s, retry once.
- First `gh pr checks 122` — a red or pending check, or a head other than `358765e3…`: say so and stop. At the
  end, `gh pr view 122 --json headRefOid` again: say whether the head moved.
- Report **verified defects only**: file and line at `358765e3`, the scenario (user action → wrong result),
  severity (**blocker** — wrong money shown or recorded, a double write, a role sees or does what it must not, a
  page that breaks, a test that cannot fail · **should-fix** — a real defect a user can meet, a missing planned
  test · **nit**), and the fix. "Plausible" when unsure, with why. Say what you **saw in the code** and what you
  only **read in the report**. A point whose own conclusion is "no change needed" is not a finding. No praise.
- **Check the library's defaults before calling a bug** (TanStack Query v5: `enabled: false` sends nothing;
  `keepPreviousData` keeps the last data while the next loads; Radix names menu content by its trigger).

## What to read (and only this)

1. `git show origin/main:CLAUDE.md` — the project's rules.
2. `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\2_PLAN.md`: the **owner's approval note at its top** (binds);
   §5 **S3** and **S11** (search them); §10 *PR 3 · Commit 1* to *Commit 5*; §11 *PR 3* (tests 54–68).
3. `4_REPORT_PR3.md` (same folder): every *Departures in commit n*, *The real run* and *Decisions taken without
   the owner*.
4. The contract, at the head: `git show 358765e3:docs/api/api-contract.md` — only `GET …/customers`, `GET
   …/customers/:customerId`, `PATCH …/customers/:customerId`, `POST …/customers/:customerId/archive` and
   `/restore`, `GET …/subscriptions/:subscriptionId` (the statement), `POST …/subscriptions/:subscriptionId/end`,
   and `SESSION_IDLE` in §6.
5. The code: `git diff --stat origin/main...358765e3`, then the files each axis needs.

## The six axes — answer each (✔ seen / ✘ → F<n> / ? why)

**A1 — Money in the file and the statement.** Every amount (due, paid, left, balance, a payment) is the server's,
never computed in the browser (the report's `left` is "the server's balance, never below zero" — is anything
hidden by that floor?); a **voided payment** is struck with its reason and **never counted or shown as paid**;
`payStatus` (paid / partial / unpaid) right at the edges (nothing paid, overpaid, zero due); after a payment,
an edit, an archive or an end, which query keys are invalidated — can the file, the list or an open statement
show a stale balance?

**A2 — The edit (finding 123, S3).** Only the fields that differ from the customer **as loaded** are sent; a
cleared phone as `null`; nothing sent when nothing changed; **no `Idempotency-Key`** and never re-sent by the
transport; a lost answer is the user's to retry. What does "as loaded" mean if the file refetches while the
dialog is open — can a field the other desk changed be sent back?

**A3 — Archive and restore, and the roles.** The owner only: «أرشفة…», «استرجاع» and the list's `ARCHIVED` filter
(reception's `?status=ARCHIVED` falls back). A settled customer archived at once with «تراجع» (does the undo
restore exactly once?); one who owes asked first, naming the debt; one present refused. Remember **authorization
lives on the server** — a hidden control is not a defect, but a control shown to reception that the server
refuses is a should-fix.

**A4 — The end.** «إنهاء الاشتراك» offered only while the subscription is neither ended nor `EXPIRED`; the dialog
says the end the server will take (today; its start if not started; never past its end) — the same rule as the
contract; no key; sent once; the card read again after.

**A5 — The idle line.** `endedBy: 'idle'` set **only** when a refresh (the restore's or the transport's) is
refused 401 `SESSION_IDLE`, never for other refusals; cleared by any established session; the sign-in page's line
shown only while it holds. Can a non-reception user, or a normal sign-out, ever see it?

**A6 — The list's address (S11) and the tests.** `q`, `status`, `kind`, `payment`, `page` read by the contract's
rules (a value the server would refuse falls back); a change replaces the address and returns to page 1. Then,
for tests 54–68: present / missing / weaker, and **would each fail if its behaviour regressed after the code
exists** (66 and 68 count their red step as their break; 64 was broken on the trigger's label — accepted by the
owner). Also judge the routes test's `beforeAll` warm-up: does it hide a real slowness a user would meet?

**The executor's four decisions taken without the owner** (report's last section): one line each — accepted /
not, why.

## The report's shape

```
# Review — DESK_SCREENS PR 3 (#122) — Claude Code (light)
Head: <sha> · checks: <green/red> · head moved during the review: <yes/no>
Verdict: <mergeable | mergeable after small fixes | not mergeable>

## Findings (verified defects only, most severe first)
### F1 — <blocker|should-fix|nit> · <title>
- Where: <file>:<line> at 358765e3
- Seen in the code: <what>      (or: Only in the report: <what>)
- Scenario: <user action → wrong result>
- Fix: <what to change>
(None → "None.")

## Axes A1–A6
## Tests 54–68 (one line each)
## The four decisions
## Not checked, and why
```

Then stop.
