# Review — DESK_SCREENS PR 1b (#117, `feat/desk-uncollected`): one independent reviewer, read-only (OpenCode)

You are an **independent code reviewer** of one pull request in the Git repository at
`C:\dev\masaha\app-design`. This file is self-contained: every command, file and question is written here. You
did not write the code; another agent did. **Trust nothing you have not seen in the code.**

**Your report file** (write only this file, nothing else anywhere):
`C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\6_REVIEW_PR1B_OPENCODE.md` — write it **as you go** (a section
after each part of §4), so nothing is lost if you stop early.

## 0. What the PR is

Masaha is a bilingual (Arabic right-to-left / English) web platform for coworking spaces. The previous PR
(#116, merged) built the front desk's visits screen. **This PR adds two cards to that desk page, in the web app
only (`apps/web`, plus `docs`):**
- **«غير محصّل» — the uncollected visits:** visits closed but not fully paid. For each: «تحصيل» (collect: record
  a payment, with one idempotency key per intent; a remainder on a visit with no customer needs a phone),
  «تسجيل دين» (leave the debt to a customer by phone; no key), and — **owner only** — «لن يُحصَّل…» (write it off,
  with a required reason; no key) and its undo «تراجع» from the toast (no key).
- **«بدون سعر» — the unpriced visits:** visits closed with no price; whoever may type a price
  (`mayTypePrice`, the server's) prices each with an amount and a required reason.

The API is built and merged; **this PR changes no API code.** Since the plan was written, a merged API change
(#114) widened the uncollected list: besides the auto check-out's unpaid visits, it now holds a **priced visit
closed by hand with no customer whose payment was voided**. The web must list what the server answers and never
filter rows by how they were closed.

- **PR:** #117 · **head:** `a1193e77a63f57ed7110195fd70f2440206e4dc2` · **base:** `origin/main` · 48 files, 2
  commits.
- **The approved plan:** `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\2_PLAN.md` (long; read only the parts §3
  names). **The owner's approval note at its top binds and wins** where the plan below it differs.
- **The executor's prompt and report:** `3_EXEC_PROMPT_PR1B.md` and `4_REPORT_PR1B.md` (same folder).

## 1. Rules — read-only, always

- **Never** edit, create or delete a file in the repository; never `git checkout`, `git switch`, `git reset`,
  `git stash`, `git commit`, `git push`, `git rebase`; never install anything; **never run `npm`, `node`, `npx`,
  tests, builds or servers**; never touch a database; never comment on GitHub.
- **Allowed commands only** (PowerShell, from `C:\dev\masaha\app-design`): `git fetch origin`, `git log`, `git
  show`, `git diff`, `git grep`, `git ls-tree`, and read-only `gh pr view` / `gh pr checks`. Read the workspace
  files named here with your file reader.
- **Read every repository file at the head's sha, never from the working tree** (it is an older commit): `git
  show a1193e77:<path>`. If a `git` command fails on a `.lock` file, wait 30 seconds and run it again once;
  never delete a `.lock` file.
- **A finding is a defect you verified, nothing else.** Each one needs: the file and line (at `a1193e77`), the
  scenario (what a user does → what goes wrong), the severity, and the fix. **Do not list as a finding** a point
  whose own conclusion is "no change needed", a departure you accept, or the plan's own wording: those go in
  the checklist or the departures section. If you are not sure, write **"plausible"** and why. Say clearly what
  you **saw in the code** and what you only **read in the executor's report**. No praise.
- **Before calling something a bug, check the library's defaults** (for example TanStack Query v5:
  `refetchIntervalInBackground` is `false` by default; `keepPreviousData` keeps the last page while the next
  loads). A finding built on a wrong assumption about a library is worse than no finding.
- **Severity:** **blocker** (wrong money recorded or shown, a double payment, a page that breaks, a security or
  privacy hole, a test that cannot fail) · **should-fix** (a real defect a user can meet; a missing planned
  test; a document that says something false) · **nit** (style, wording, small cleanup).
- **Do not report** what lint, typecheck, Prettier or CI already enforce and passed; CI is green on this head.

## 2. First steps (in this order)

```powershell
cd C:\dev\masaha\app-design
git fetch origin
gh pr checks 117
gh pr view 117 --json headRefOid,mergeStateStatus,files
git fetch origin pull/117/head
git log --format="%h %s%n%b" origin/main..a1193e77
git diff --stat origin/main...a1193e77
```
If a check is red or pending, or the head is not `a1193e77…`, write that at the top of your report and stop.
Write in the report: the head, the checks, the two commit subjects with their lengths (each ≤ 50 characters,
each with a body), and whether a commit message names an AI tool or has a `Co-Authored-By` line.

## 3. What to read (and only this)

1. `git show a1193e77:CLAUDE.md` — the project's rules (they bind the code you review).
2. In `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\2_PLAN.md`: the **approval note at its top**; §2 *Scope*,
   *Acceptance criteria* and *Out of scope* for **PR 1** (the uncollected and unpriced parts); §8 *PR 1* (the
   design issues of commits 5–6, among them DI-3, DI-9, DI-11, DI-19, DI-29); §10 *PR 1 · Commit 5* and *Commit
   6*; §11 *PR 1* — **tests 31–39 and 41**; §13 *The real run* (PR 1b's writes).
3. `4_REPORT_PR1B.md` — its *Departures* section and its run results.
4. The contract: `git show a1193e77:docs/api/api-contract.md` — the sections for `GET …/uncollected-visits`,
   `GET …/unpriced-visits`, `PUT …/visits/:visitId/charge`, `POST …/payments`, `PUT …/visits/:visitId/customer`,
   `POST`/`DELETE …/visits/:visitId/write-off`, and §6's error codes; and the shared types
   `git show a1193e77:packages/shared/src/payments/responses.ts` and `…/visits/*.ts`.
5. The code: every file of the diff, one group at a time (`git diff origin/main...a1193e77 -- <path>`):
   - **A. Data:** `apps/web/src/features/desk/repository/deskRepository.ts` and its test,
     `apps/web/src/features/desk/hooks/queryKeys.ts`, `hooks/uncollected/useUncollectedQuery.ts`,
     `hooks/unpriced/useUnpricedQuery.ts`, `types/UncollectedItem.ts`, `types/DeskAbilities.ts`.
   - **B. Collect:** `hooks/collect/*`, `components/collect/CollectDialog.tsx`.
   - **C. Debt:** `hooks/debt/*`, `components/debt/DebtDialog.tsx`.
   - **D. Write-off:** `hooks/write-off/*`, `components/write-off/WriteOffDialog.tsx`, `components/toast/deskToasts.tsx`.
   - **E. The cards:** `hooks/uncollected/useUncollectedCard.ts` and its test,
     `components/uncollected/{UncollectedCard,UncollectedRow}.tsx` and its test, `services/dayWord.ts` and its test.
   - **F. Unpriced:** `hooks/unpriced/*`, `components/unpriced/{UnpricedCard,PriceDialog}.tsx`.
   - **G. The page and words:** `apps/web/src/pages/dashboard/space/desk/DeskPage.tsx`,
     `apps/web/src/features/desk/index.ts`, `apps/web/src/shared/copy/{arabic,english}/desk.ts`,
     `apps/web/src/test/deskVisit.ts`.
   - **H. Documents:** `docs/features/{desk,payments,visits}.md`, `docs/architecture/findings/README.md` and
     findings 110, 112, 115, 164.

## 4. The checklist — answer every line (✔ seen / ✘ finding / ? could not tell, and why)

**4.1 Collect («تحصيل») — money and the key**
- One idempotency key per collect intent: kept across a retry and a double press, **never renewed on an error**,
  renewed only after a success or a new opening. Does the request send it as `Idempotency-Key`?
- The amount defaults to what the row owes; the amount sent is never above what it owes; a remainder on a row
  with **no customer** asks a phone (and a name, if the plan says) before sending; `VISIT_WRITTEN_OFF` and
  `PAYMENT_EXCEEDS_DUE` are worded.
- After success, the uncollected list (and anything showing the same visit) is refreshed — which query keys are
  invalidated?

**4.2 Debt («تسجيل دين») and the write-off — no key, never re-sent**
- «تسجيل دين», the write-off and its undo carry **no** key and are **never retried automatically** (the transport
  retries only keyed writes): read `useDeskWrite` / the repository and the hooks. A lost answer says so and
  lets the user decide; it does not re-send by itself (finding 115).
- The write-off requires a reason; it is **offered to the owner only** (`DeskAbilities.writeOff`, from the
  session's link role) **and** a 403 from the server is worded if reception reaches it anyway.
- The undo is offered from the write-off's toast, which stays until closed (DI-29); it undoes once; a second
  press does nothing harmful.
- An **unpriced** row has no «⋯» (the server refuses its write-off): check the departure is consistent with the
  contract's write-off rule.

**4.3 The uncollected list (and #114)**
- No filter by checkout method or by customer in the web: every row the server answers is shown. A hand-closed
  row reads «خروج يدوي · …» (a departure): is that line true for every such row?
- Counts come from the page's `meta` (no money total, DI-3); three rows then «عرض الكل» (or as the plan says);
  the page number sits in the address (`uncollectedPage`, a departure): does a stale page past the last fall
  back to the last page (the list helper `usePageInRange`)?
- Days read «اليوم» / «أمس» / a date on **Gaza's** calendar (`dayWord.ts`), not the browser's zone.

**4.4 The unpriced list — the main departure to judge**
- The report says: **«بدون سعر» shows the first page only, no pages, while its title counts all.** Read
  `useUnpricedQuery.ts` / `useUnpricedCard.ts` / `UnpricedCard.tsx` and the contract's page size. **Scenario
  to judge:** a space with more unpriced visits than one page — can the staff ever reach and price the rest
  (after pricing the first page, does the next batch appear)? Say exactly what a user sees, and whether this is
  a should-fix or acceptable as written in the plan (quote the plan's line if it allows it).
- Only whoever may type a price sees the card (`mayTypePrice`, the server's), and the server refuses others
  (`PRICE_TYPING_NOT_ALLOWED` worded). The price needs an amount **and** a reason; `VISIT_ALREADY_PRICED` (or
  the contract's code) worded.

**4.5 Words, accessibility, RTL**
- Every user-facing string in both catalogues with the same keys; counted lines through the plural helpers; no
  hard-coded text in components or hooks.
- Dialogs titled, focus in and back to the control that opened them; each row's «⋯» named by the visit; touch
  targets (the report measured ≥ 44 px); amounts through the money formatter, left-to-right digits; names in
  the other language carry `lang`/`dir`.

**4.6 Tests (each must be able to fail)**
- For each test 31–39 and 41 of the plan's §11 *PR 1*: present / missing / weaker than planned, with its file.
- Test 38's first break stayed green (the executor's own test defect, fixed): does the final test 38 really fail
  if the pricing stops working?
- Tests 35, 37, 39 count their red step as their break: would a regression after the code exists still turn
  them red?

**4.7 Architecture, scope, documents**
- `shared/` never imports `features/` or `pages/`; `features/desk` imports other features only through their
  `index.ts`; no API or `packages/shared` change; semantic tokens only.
- `desk.md`, `payments.md`, `visits.md`: their web parts describe what this PR built and no more; decision and
  history lines end with a date and `#117`; no `#PRNUM` left (`git grep -n PRNUM a1193e77 -- docs apps`).
- Findings 110, 112, 115, 164: what each file now says is true to the code; finding 112's evidence line (owed by
  PR 1a, written here) is accurate.

**4.8 The executor's departures** (from `4_REPORT_PR1B.md`) — judge each: accepted / not accepted, why.

## 5. The report's shape

```
# Review — DESK_SCREENS PR 1b (#117) — OpenCode
Head: <sha> · checks: <green/red> · head moved during the review: <yes/no>
Verdict: <mergeable | mergeable after small fixes | not mergeable>

## Findings (verified defects only, most severe first)
### F1 — <blocker|should-fix|nit> · <one-line title>
- Where: <file>:<line> at a1193e77
- Seen in the code: <what>      (or: Only in the report: <what>)
- Scenario: <user action → wrong result>
- Fix: <what to change>
...
(If there is none, write "None.")

## Checklist 4.1 – 4.8
<each line: ✔ / ✘ (→ F<n>) / ? (why)>

## Tests table (4.6)
| # | file | present / missing / weaker |

## Departures judged (4.8)

## Not checked, and why
```

At the very end run `gh pr view 117 --json headRefOid` again and fill "head moved". Then stop.
